# Azure DevOps Interview Questions (7-14 LPA Level)

---

## Fundamentals

### Q1: "What is Azure DevOps and what services does it include?"
**Expected Answer:**
> Azure DevOps is Microsofts suite of DevOps tools:
> - **Azure Repos** — Git repositories (unlimited private repos)
> - **Azure Pipelines** — CI/CD (Linux, Windows, Mac agents)
> - **Azure Boards** — Agile project management (Kanban, backlogs)
> - **Azure Test Plans** — Manual and exploratory testing
> - **Azure Artifacts** — Package management (NuGet, npm, Maven)
>
> Unlike GitHub Actions (which is CI/CD only), Azure DevOps is a complete ALM (Application Lifecycle Management) platform.

---

### Q2: "What is a YAML pipeline? How is it different from the classic editor?"
**Expected Answer:**
> YAML pipeline is a code-based pipeline definition stored in the repository as `azure-pipelines.yml`. Benefits over classic editor:
> - **Version controlled** — pipeline changes go through PR review
> - **Portable** — copy to another project, change variables only
> - **Reusable** — templates for common patterns
> - **Auditable** — git blame shows who changed what
>
> Classic editor stores configuration in Azure DevOps database (no version control, harder to review).

---

### Q3: "Explain the structure of a YAML pipeline"
**Expected Answer:**
```yaml
trigger:
  - main           # When to run (branch push)

pool:
  vmImage: 'ubuntu-latest'  # Where to run (agent)

variables:
  buildConfig: 'Release'    # Pipeline-wide values

stages:
  - stage: Build            # Logical grouping
    jobs:
      - job: BuildJob
        steps:
          - script: dotnet build --configuration $(buildConfig)
```

**Hierarchy:** Pipeline -> Stages -> Jobs -> Steps

---

## Intermediate

### Q4: "How do you handle secrets in Azure DevOps?"
**Expected Answer:**
> - **Variable Groups linked to Key Vault:** Store secrets in Azure Key Vault and reference them in pipelines via Variable Groups
> - **Pipeline secrets:** `$(password)` — masked in logs, encrypted at rest
> - **Never hardcode secrets** in YAML files (theyre in git!)
> - **Azure Key Vault task:** Download secrets as pipeline variables at runtime
>
> ```yaml
> variables:
>   - group: prod-secrets   # Linked to Azure Key Vault
>   - name: database-password
>     value: $(kv-db-password)  # Retrieved from KV at runtime
> ```

---

### Q5: "What is a Service Connection? Give an example"
**Expected Answer:**
> A Service Connection is a secure way for Azure DevOps to authenticate to external services (Azure, GitHub, Docker Hub, etc.).
>
> For Azure: Creates a Service Principal in Azure AD with specific permissions (e.g., Contributor on a subscription). The pipeline uses this SPN to create/modify Azure resources.
>
> ```yaml
> - task: AzureCLI@2
>   inputs:
>     azureSubscription: 'my-service-connection'  # References the connection
>     scriptType: 'pscore'
>     scriptLocation: 'inlineScript'
>     inlineScript: 'az vm list'
> ```

---

### Q6: "How would you set up a Terraform pipeline in Azure DevOps?"
**Expected Answer:**
> 1. **Service Connection** to Azure (with Contributor permission)
> 2. **Variable Group** for Terraform backend config + sensitive vars
> 3. **Multi-stage pipeline:**
>    - Stage 1 (Validate): `terraform init`, `terraform validate`, `terraform fmt`
>    - Stage 2 (Plan): `terraform plan -out=tfplan`, publish plan as artifact
>    - Stage 3 (Apply Dev): Deploy to dev environment
>    - Stage 4 (Apply Prod): Requires manual approval, then deploy
> 4. **Environment approvals:** Prod environment requires DevOps lead approval
> 5. **Artifact:** Save the plan file so apply uses the exact same plan

---

### Q7: "What is a self-hosted agent vs Microsoft-hosted agent?"
**Expected Answer:**
> **Microsoft-hosted:** Pre-configured VMs (ubuntu-latest, windows-latest). Limited to 60 minutes free (public), then charged. No customization.
>
> **Self-hosted:** Your own VM or on-prem machine running Azure DevOps agent. Benefits:
> - Full control over software installed
> - No time limits
> - Access to corporate network
> - Consistent environment for builds
>
> Downside: You maintain it (updates, security patches, scaling).

---

### Q8: "How do you implement approvals for production deployments?"
**Expected Answer:**
> Azure DevOps Environments with approval checks:
> 1. Create Environment "prod" in Azure DevOps
> 2. Add Approver (e.g., DevOps Lead) to the environment
> 3. In pipeline YAML, reference the environment:
>    ```yaml
>    - stage: Deploy_Prod
>      environment: prod   # <-- This triggers the approval
>    ```
> 4. Pipeline pauses at this stage until approver manually approves
> 5. Additional checks: Branch policy (only main), time window, etc.

---

### Q9: "How do you organize pipelines for a microservices architecture?"
**Expected Answer:**
> Option 1 — **Monorepo with Terraform-based multistage pipeline:**
> ```yaml
> # Single pipeline per microservice, triggered on service folder changes
> trigger:
>   paths:
>     include:
>       - services/payment/*
> ```
>
> Option 2 — **Azure Pipeline Templates for reuse:**
> ```yaml
> # template.yml (shared)
> parameters:
>   serviceName: ''
> steps:
>   - script: echo "Building ${{ parameters.serviceName }}"
> ```
>
> ```yaml
> # service-pipeline.yml
> steps:
>   - template: templates/build.yml
>     parameters:
>       serviceName: 'payment'
> ```
>
> Option 3 — **Separation of concerns:** Separate pipelines for infra (Terraform) vs app (build/test/deploy)

---

## Advanced

### Q10: "How do you handle rollbacks in Azure DevOps?"
**Expected Answer:**
> Depends on what you deployed:
> - **Application rollback:** Re-run previous successful pipeline run (re-deploy old artifact)
> - **Infrastructure rollback:** `terraform plan` shows what changed. Run `terraform apply` with previous state file
> - **Database rollback:** Flyway/Knex migration rollback (run `undo` on previous migration)
> - **Container rollback:** Re-tag previous image version, redeploy
>
> Key: Always keep previous successful artifact/image for 7+ days. Infrastructure rollback is harder — always plan for it.

---

## Quick Comparison: Azure DevOps vs GitHub Actions

| Feature | Azure DevOps | GitHub Actions |
|---------|-------------|----------------|
| Pipeline as code | YAML | YAML |
| Hosted agents | Windows, Linux, Mac | Windows, Linux, Mac |
| Free minutes | 1800/month (private) | 2000/month (private) |
| Self-hosted agents | Yes | Yes |
| Terraform integration | Native Azure CLI tasks | Community actions |
| Stage approvals | Built-in (Environments) | Environment protection rules |
| Variable groups | Built-in | Secrets + Environments |
| Multi-stage pipelines | Native | Native |
| Price | Free for 5 users | Free for public repos |

---

## Must-Know Interview Answers

1. **"Why use Azure DevOps over Jenkins?"**
   > Managed service (no server to maintain), native Azure integration, built-in artifact storage, YAML pipeline as code, variable groups with Key Vault integration.

2. **"How do you debug a failing pipeline?"**
   > Check pipeline logs first. Enable debug mode (`system.debug=true`). Check agent diagnostics. If self-hosted, check agent logs on the VM.

3. **"How do you cache dependencies in Azure DevOps?"**
   > ```yaml
   > - task: Cache@2
   >   inputs:
   >     key: 'npm | "$(Agent.OS)" | package-lock.json'
   >     path: '$(npm_config_cache)'
   > ```

---

*Last updated: 21 May 2026 | Use with study-plan.md*

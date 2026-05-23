# Azure DevOps Study Plan

**Target Level:** Mid-level DevOps (3+ YOE) | 7-14 LPA interviews
**Context:** Azure DevOps Pipelines is mentioned in 60% of JDs. You need to know YAML pipelines, Terraform integration, and CI/CD patterns.
**Prerequisite:** Azure fundamentals (study-plan.md in azure/ folder)

---

## Why Azure DevOps?

Indian product companies use Azure DevOps for:
- **CI/CD pipelines** — build, test, deploy
- **Azure Repos** — git hosting (alternative to GitHub)
- **Azure Artifacts** — package management (NuGet, npm, Maven)
- **Variable Groups** — environment-specific configuration
- **Service Connections** — secure Azure authentication

**Interview angle:** Most candidates know GitHub Actions. If you also know Azure DevOps, you show platform flexibility.

---

## Week 5: Azure DevOps Pipelines

### Day 1: Azure DevOps Organization + Project Structure (TOPIC 01)
- Organization -> Project -> Repo -> Pipeline
- Organization settings: parallel jobs, agents, extensions
- Project settings: permissions, service hooks, boards
- **Key concept:** Understand the hierarchy — dont need to memorize UI

### Day 2: YAML Pipeline Basics (TOPIC 02)
- Pipeline structure:
  ```yaml
  trigger:
    - main
  
  pool:
    vmImage: 'ubuntu-latest'
  
  steps:
    - script: echo "Hello, Azure DevOps!"
      displayName: 'Run a one-line script'
  ```
- Triggers: CI (branch push), PR, scheduled, manual
- Pool: Microsoft-hosted agents (ubuntu-latest, windows-latest, macos-latest)
- Steps: script, task, checkout

### Day 3: Pipeline Tasks + Jobs (TOPIC 03)
- Common tasks: CopyFiles, PublishBuildArtifacts, DownloadBuildArtifacts
- PowerShell/Bash tasks for custom logic
- Jobs: sequential vs parallel, dependencies
- Multiple jobs in one pipeline:
  ```yaml
  jobs:
    - job: Build
      steps:
        - script: npm install && npm run build
    
    - job: Test
      dependsOn: Build
      steps:
        - script: npm test
    
    - job: Deploy
      dependsOn: Test
      condition: succeeded()
      steps:
        - script: echo "Deploying..."
  ```

### Day 4: Variables + Variable Groups (TOPIC 04)
- Pipeline variables: `$(variableName)`
- Variable Groups: share variables across pipelines
  ```yaml
  variables:
    - group: prod-variables  # Linked to Key Vault
    - name: environment
      value: production
  ```
- Runtime vs compile-time variables
- **Security:** Variable Groups linked to Azure Key Vault for secrets

### Day 5: Terraform Pipeline (TOPIC 05) — CRITICAL
- Full Terraform pipeline in Azure DevOps:
  ```yaml
  trigger:
    - main
  
  pool:
    vmImage: 'ubuntu-latest'
  
  variables:
    - group: terraform-variables
    - name: tf_working_dir
      value: '$(System.DefaultWorkingDirectory)/terraform'
  
  stages:
    - stage: Validate
      jobs:
        - job: TerraformValidate
          steps:
            - script: terraform init -backend-config=backend.tfvars
              displayName: 'Terraform Init'
              workingDirectory: '$(tf_working_dir)'
            - script: terraform validate
              displayName: 'Terraform Validate'
              workingDirectory: '$(tf_working_dir)'
            - script: terraform plan -out=tfplan
              displayName: 'Terraform Plan'
              workingDirectory: '$(tf_working_dir)'
    
    - stage: Deploy_Dev
      dependsOn: Validate
      condition: succeeded()
      jobs:
        - deployment: DeployInfra
          environment: dev
          strategy:
            runOnce:
              deploy:
                steps:
                  - script: terraform apply -auto-approve tfplan
                    displayName: 'Terraform Apply'
                    workingDirectory: '$(tf_working_dir)'
    
    - stage: Deploy_Prod
      dependsOn: Deploy_Dev
      condition: succeeded()
      jobs:
        - deployment: DeployInfra
          environment: prod
          strategy:
            runOnce:
              deploy:
                steps:
                  - checkout: self
                  - script: terraform init -backend-config=backend.tfvars
                  - script: terraform plan -out=tfplan
                  - script: terraform apply -auto-approve tfplan
          # Manual approval gate configured in Azure DevOps environment
  ```

**Key pipeline features used:**
- Stages with dependencies
- Environment-based approvals (manual gate for prod)
- Variable Groups for secrets
- Terraform init -> validate -> plan -> apply flow

### Day 6: Service Connections + Authentication (TOPIC 06)
- Azure Service Connection: authenticate Azure DevOps to Azure
  - Service Principal (app registration in Azure AD)
  - Managed Identity (if using self-hosted agents)
- Creating Service Connection: Project Settings -> Service Connections -> Azure Resource Manager
- **Interview question:** "How does Azure DevOps authenticate to Azure?"
  - Answer: Service Principal with Contributor permissions on the target subscription. Created during Service Connection setup.

### Day 7: Multi-Stage Pipelines + Approvals (TOPIC 07)
```yaml
stages:
  - stage: Build
    jobs:
      - job: BuildApp
        steps:
          - script: echo "Building..."

  - stage: Deploy_Dev
    dependsOn: Build
    condition: succeeded()
    environment: dev
    jobs:
      - deployment: Deploy
        strategy:
          runOnce:
            deploy:
              steps:
                - script: echo "Deploying to dev..."

  - stage: Deploy_Prod
    dependsOn: Deploy_Dev
    condition: succeeded()
    environment: prod
    jobs:
      - deployment: Deploy
        strategy:
          runOnce:
            deploy:
              steps:
                - script: echo "Deploying to prod..."
```

**Approval gates:** Configured in Azure DevOps Environments UI
- Prod environment requires approval from specific users/groups
- Pipeline waits until approval is given
- Shows DevOps maturity in interviews

---

## Week 6: Containers + Integration

### Day 8: Docker Fundamentals (in docker-k8s/ folder)
### Day 9: Docker Compose + Multi-stage Builds (in docker-k8s/ folder)
### Day 10: Build and Push Docker Image in Azure DevOps
### Day 11: Azure Kubernetes Service (AKS) + Azure DevOps
### Day 12-14: Integration Project

---

## Interview Depth Guide

| Topic | Must Know | Nice to Know | Dont Bother |
|-------|-----------|-------------|-------------|
| YAML Pipelines | triggers, steps, jobs, stages | templates, extends, parameters | Classic editor (UI) pipelines |
| Variable Groups | create, link to KV, use in pipeline | Library security, variable group permissions | Variable group Azure API |
| Service Connections | Create, SPN, permissions | Workload identity federation | Managed identity for pipelines |
| Terraform + ADO | Full pipeline with plan/apply stages | Terraform Cloud integration | Atlantis |
| Approvals | Environment-based approval gates | Branch policies, check gates | Pipeline decorators |
| Artifacts | Publish and download build artifacts | Pipeline caching, artifact feeds | Universal packages |

---

## Common Interview Questions

1. "How does a YAML pipeline differ from the classic editor?"
2. "Explain the stages in a Terraform pipeline"
3. "How do you securely pass secrets in Azure DevOps?"
4. "What is a Service Connection and how does it work?"
5. "How would you set up approval gates for production deployments?"
6. "Whats the difference between a variable and a variable group?"
7. "How do you organize pipelines for microservices architecture?"
8. "Explain multi-stage pipeline vs multi-job pipeline"

---

## Quick Reference: Terraform CI/CD Pipeline Pattern

```
Pipeline Flow:
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│ Validate  │ -> │   Plan   │ -> │ Approval │ -> │  Apply   │
│ (init,    │    │ (show    │    │ (manual  │    │ (execute │
│  format,  │    │  changes)│    │  gate)   │    │  plan)   │
│  validate)│    └──────────┘    └──────────┘    └──────────┘
└──────────┘
    Dev               Dev               Dev                Dev
                                        ├──────── Prod approval (separate)
                                        │
                                    ┌───┴───┐
                                    │  Prod  │ -> Apply to Prod
                                    │ Approv │
                                    └───────┘
```

**Key rule:** Never run `apply` without first saving a `plan`. CI/CD pipelines should always: plan -> save plan -> (approval) -> apply saved plan.

---

*Last updated: 21 May 2026 | Next: topics/01-ado-organization-structure.md*

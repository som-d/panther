# CI/CD Interview Questions (7-14 LPA)

---

### Q1: "Explain the difference between CI, CD, and Continuous Deployment"
> **CI** — Every code change is built and tested automatically. Merging to main triggers build + test. Catches bugs early.
> **CD (Continuous Delivery)** — Every change that passes CI is deployable to production. But deployment may require manual approval.
> **Continuous Deployment** — Every change that passes CI goes to production automatically. No human gate. Rare in practice.

### Q2: "What is build once, deploy many?"
> Build the artifact ONCE (e.g., Docker image tagged with commit SHA). Use the EXACT same artifact in dev, staging, and prod. This ensures what was tested in staging is what runs in production. No "works on my machine" issues.

### Q3: "How do you handle database migrations in CI/CD?"
> Migrations should be backward-compatible. Pattern:
> 1. Pre-deploy: Run migration (add column, new table — never remove/modify)
> 2. Deploy new code (works with old AND new schema)
> 3. Post-deploy: Clean up old schema if needed
>
> Never combine breaking migrations with code deploy. Always make migrations reversible.

### Q4: "Explain blue-green deployment"
> Two identical environments: BLUE (current) and GREEN (new). Deploy to GREEN, run tests, switch traffic to GREEN. If issues, switch back to BLUE. Zero downtime, instant rollback. Downside: double infrastructure cost.

### Q5: "What is a canary release?"
> Route a small percentage of traffic (5%) to the new version. Monitor errors. Gradually increase (25%, 50%, 100%). Minimizes blast radius. Used by Netflix, Google, Amazon. Needs good monitoring and traffic routing.

### Q6: "How do you secure a CI/CD pipeline?"
> - Secrets in vault/KV (never in YAML files)
> - Least privilege for service connections
> - Branch protection (no direct push to main)
> - Code scanning (SAST) in pipeline
> - Dependency scanning (SCA) for vulnerabilities
> - Signed commits and artifacts
> - Audit logs for pipeline changes

### Q7: "What is trunk-based development?"
> Developers commit to main multiple times a day. Feature branches are short-lived (hours, not days). Enables true CI — every commit is validated. Avoids merge hell. Used by Google, Netflix, Facebook.

### Q8: "How do you rollback a failed deployment?"
> Depends on strategy:
> - **Rolling:** Re-deploy previous artifact version
> - **Blue-Green:** Switch traffic back to BLUE
> - **Canary:** Route traffic back to old version
> - **Terraform:** `terraform apply` with previous state
>
> Key: Always keep previous successful artifact for 7+ days. Practice rollbacks regularly.

---

## Quick Comparison

| Feature | GitHub Actions | Azure DevOps | GitLab CI |
|---------|---------------|-------------|-----------|
| Pipeline as code | YAML | YAML | YAML |
| Self-hosted | Yes | Yes | Yes |
| Free minutes | 2000/mo | 1800/mo | 400/mo |
| Best for | GitHub repos | Azure stack | GitLab repos |
| Terraform | hashicorp/setup-terraform | AzureCLI task | Built-in |

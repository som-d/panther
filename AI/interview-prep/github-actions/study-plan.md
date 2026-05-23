# GitHub Actions Study Plan

**Target:** DevOps Engineer, 3+ YOE | 7-14 LPA interviews
**Why separate folder:** GitHub Actions is the #1 CI/CD tool at Indian product companies. Azure DevOps is #2. You need both.
**Prerequisite:** CI/CD fundamentals covered in `cicd/study-plan.md`

---

## 1. Why GitHub Actions Matters

At Indian product companies:
- **Postman** uses GitHub Actions for CI/CD
- **BrowserStack** uses GitHub Actions for test automation
- **Razorpay** uses GitHub Actions for Terraform pipelines
- **Freshworks** uses GitHub Actions + Azure DevOps
- **Chargebee** uses GitHub Actions for deployment

GitHub Actions is built into GitHub — no separate server, no setup cost. Every repo gets CI/CD for free.

---

## 2. Core Concepts

### Workflow = Pipeline
```yaml
# .github/workflows/ci.yml
name: CI                    # Workflow name (shown in GitHub UI)
on: [push]                  # Trigger: run on every push

jobs:
  build:
    runs-on: ubuntu-latest  # Runner: where the job runs
    steps:
      - uses: actions/checkout@v4   # Checkout code
      - run: echo "Hello World"     # Run a command
```

### Key Terms
| Term | What It Is | Example |
|------|-----------|---------|
| **Workflow** | A CI/CD pipeline defined in YAML | `.github/workflows/ci.yml` |
| **Job** | A unit of work (runs on one runner) | `build`, `test`, `deploy` |
| **Step** | Individual task within a job | `actions/checkout@v4`, `npm test` |
| **Runner** | Machine that executes jobs | `ubuntu-latest`, `windows-latest`, self-hosted |
| **Action** | Reusable unit of code | `actions/checkout@v4`, `actions/setup-node@v4` |
| **Event** | What triggers the workflow | `push`, `pull_request`, `schedule` |

---

## 3. Trigger Events (Know These)

```yaml
on:
  push:
    branches: [main]                    # Push to main
  pull_request:
    branches: [main]                    # PR targeting main
  schedule:
    - cron: '0 6 * * 1'                 # Every Monday 6 AM UTC
  workflow_dispatch:                     # Manual trigger (button in UI)
  release:
    types: [published]                   # New release published
```

**Path filtering** (run only when specific files change — CRITICAL for monorepos):
```yaml
on:
  push:
    paths:
      - 'terraform/**'                   # Only when terraform/ changes
      - '!terraform/README.md'           # But NOT when README changes
```

---

## 4. Jobs + Dependencies

### Sequential Jobs
```yaml
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm run lint

  test:
    needs: lint                      # Runs AFTER lint succeeds
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm test

  deploy:
    needs: test                      # Runs AFTER test succeeds
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'  # Only main branch
    steps:
      - run: echo "Deploying..."
```

### Parallel Jobs (Matrix Builds)
```yaml
jobs:
  test:
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest]
        node: [18, 20]
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node }}
      - run: npm test
```
This creates 4 jobs (2 OS x 2 Node versions) running in PARALLEL. Interviewers love this.

---

## 5. Environments + Approvals

```yaml
jobs:
  deploy-prod:
    runs-on: ubuntu-latest
    environment: production          # Links to GitHub Environment
    steps:
      - run: echo "Deploying to prod"
```

**Environment features:**
- **Required reviewers:** Deploy pauses until approved
- **Wait timer:** Delay before deployment
- **Protection rules:** Branch restrictions
- **Environment secrets:** Isolated secrets per env

**Interview answer:**
> "I use GitHub Environments with required reviewers for production. The pipeline pauses, Slack notifies the DevOps lead, they review the changes, and approve or reject. Zero chance of accidental production deployment."

---

## 6. Secrets + Variables

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Login to Azure
        uses: azure/login@v2
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}

      - name: Deploy with Terraform
        run: terraform apply -auto-approve
        env:
          ARM_CLIENT_ID: ${{ secrets.ARM_CLIENT_ID }}
          ARM_CLIENT_SECRET: ${{ secrets.ARM_CLIENT_SECRET }}
```

**Secrets vs Variables:**
- **Secrets:** Encrypted, masked in logs, stored in Settings > Secrets > Actions
- **Variables:** Plain text, visible in logs, stored in Settings > Variables > Actions

**Organization-level secrets:** Share across all repos in your org

---

## 7. Artifacts (Pass Files Between Jobs)

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - run: npm run build
      - uses: actions/upload-artifact@v4
        with:
          name: build-output
          path: dist/

  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: build-output
      - run: echo "Deploy from dist/"
```

---

## 8. Caching Dependencies

```yaml
steps:
  - uses: actions/setup-node@v4
    with:
      node-version: '20'
      cache: 'npm'               # Auto-caches node_modules

  - run: npm ci                  # Faster than npm install
```

**What to cache:**
- `node_modules` (Node.js)
- `~/.m2/repository` (Maven)
- `~/.nuget/packages` (NuGet)
- Docker layers

---

## 9. Terraform Pipeline in GitHub Actions (CRITICAL)

```yaml
name: Terraform CI/CD

on:
  push:
    branches: [main]
    paths: ['terraform/**']
  pull_request:
    paths: ['terraform/**']

env:
  ARM_CLIENT_ID: ${{ secrets.ARM_CLIENT_ID }}
  ARM_CLIENT_SECRET: ${{ secrets.ARM_CLIENT_SECRET }}
  ARM_SUBSCRIPTION_ID: ${{ secrets.ARM_SUBSCRIPTION_ID }}
  ARM_TENANT_ID: ${{ secrets.ARM_TENANT_ID }}
  TF_VERSION: '1.9.0'

jobs:
  plan:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: ./terraform
    steps:
      - uses: actions/checkout@v4

      - uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: ${{ env.TF_VERSION }}

      - name: Terraform Init
        run: terraform init
        id: init

      - name: Terraform Format
        run: terraform fmt -check
        id: fmt

      - name: Terraform Validate
        run: terraform validate
        id: validate

      - name: Terraform Plan
        run: terraform plan -out=tfplan -no-color
        id: plan
        continue-on-error: true

      - name: Upload Plan
        uses: actions/upload-artifact@v4
        with:
          name: tfplan
          path: ./terraform/tfplan

  apply:
    needs: plan
    if: github.ref == 'refs/heads/main' && success()
    runs-on: ubuntu-latest
    environment: production
    defaults:
      run:
        working-directory: ./terraform
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: ${{ env.TF_VERSION }}

      - name: Download Plan
        uses: actions/download-artifact@v4
        with:
          name: tfplan
          path: ./terraform

      - name: Terraform Apply
        run: terraform apply -no-color tfplan
```

**Key pattern:** Plan in CI (on every PR), Apply only from main with environment approval. Never `apply` without a saved `plan`.

---

## 10. GitHub Actions vs Azure DevOps (Interview Question)

| Feature | GitHub Actions | Azure DevOps |
|---------|---------------|-------------|
| Pipeline as code | YAML | YAML |
| Hosted runners | ubuntu, windows, macos | ubuntu, windows, macos |
| Free minutes | 2000/month (private) | 1800/month (private) |
| Self-hosted runners | Yes | Yes |
| Terraform support | `hashicorp/setup-terraform` | `AzureCLI@2` task |
| Approvals | Environments | Environments (richer) |
| Variable groups | Org secrets + env secrets | Library variable groups |
| Best for | GitHub-native projects | Azure-native projects |
| Learning curve | Low | Medium |

**Interview answer when asked:**
> "I prefer GitHub Actions for its simplicity — it's built into GitHub, zero setup, and the marketplace has actions for everything. But if the company uses Azure heavily, Azure DevOps has tighter integration. I'm comfortable with both."

---

## Interview Questions (GitHub Actions Specific)

### Q1: "What is the difference between a workflow, job, and step?"
> Workflow is the entire pipeline (one YAML file). Jobs run on separate runners and can be parallel or sequential. Steps are individual commands within a job. A workflow has multiple jobs, a job has multiple steps.

### Q2: "How do you run jobs in parallel vs sequential?"
> Parallel by default — jobs run simultaneously unless you add `needs:`. Sequential: add `needs: [previous-job]` to wait for it. Matrix builds are a special kind of parallel — same job but with different parameters.

### Q3: "How do you pass data between jobs?"
> Use artifacts. `actions/upload-artifact` in the first job saves files. `actions/download-artifact` in the next job restores them. Artifacts are stored in GitHub and retained for 90 days by default.

### Q4: "How do you handle secrets in GitHub Actions?"
> Store in Settings > Secrets > Actions. Reference with `${{ secrets.MY_SECRET }}`. Never print secrets (GitHub masks them in logs). Use environment-specific secrets for different deploy targets.

### Q5: "How do you trigger a workflow only for specific files?"
> Path filtering: `on: push: paths: ['terraform/**']`. This only runs the workflow when files in `terraform/` change. Critical for monorepos.

---

## Quick Reference

```yaml
# Common triggers
on: [push]                                              # Every push
on: pull_request                                        # Every PR
on: workflow_dispatch                                   # Manual
on: schedule: - cron: '0 0 * * 0'                       # Weekly

# Common actions
- uses: actions/checkout@v4                             # Checkout code
- uses: actions/setup-node@v4                           # Setup Node.js
- uses: actions/setup-python@v5                         # Setup Python
- uses: hashicorp/setup-terraform@v3                    # Setup Terraform
- uses: azure/login@v2                                  # Azure login
- uses: docker/login-action@v3                          # Docker login

# Common patterns
if: github.ref == 'refs/heads/main'                     # Only main
if: success()                                           # Only if previous succeeded
if: cancelled()                                         # Only if cancelled
if: failure()                                           # Only if failed
continue-on-error: true                                 # Don't fail the job
timeout-minutes: 10                                     # Max runtime
```

---

*Next: cicd/study-plan.md for general CI/CD concepts and deployment strategies*

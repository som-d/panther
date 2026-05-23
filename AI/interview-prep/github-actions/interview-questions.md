# GitHub Actions Interview Questions (7-14 LPA)

---

### Q1: "Explain the structure of a GitHub Actions workflow"

> A workflow is a YAML file in `.github/workflows/`. It has:
> - **Name:** Workflow display name
> - **On:** Trigger events (push, pull_request, schedule)
> - **Env:** Environment variables for all jobs
> - **Jobs:** Units of work that run on runners
> - **Steps:** Individual commands within a job

```yaml
name: CI
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm test
```

### Q2: "How do you run jobs in parallel in GitHub Actions?"

> Jobs run in PARALLEL by default. If you want them sequential, use `needs:`.
>
> **Parallel:** Just define multiple jobs — they all start at once.
> **Matrix:** Same job with multiple configurations:
> ```yaml
> strategy:
>   matrix:
>     os: [ubuntu, windows]
>     node: [18, 20]
> ```
> This creates 4 parallel runs (2 OS x 2 Node).

### Q3: "How do you secure a GitHub Actions pipeline?"

> - **Secrets:** Store in Settings > Secrets > Actions, reference with `${{ secrets.NAME }}`
> - **Environment protection:** Use Environments with required reviewers for prod
> - **Branch protection:** Require status checks to pass before merging
> - **Least privilege:** Use granular GITHUB_TOKEN permissions
> - **Pin actions to SHA:** `uses: actions/checkout@<commit-sha>` instead of `@v4`
> - **OpenID Connect (OIDC):** Instead of long-lived secrets, use OIDC to get short-lived tokens from cloud providers

### Q4: "What is the difference between GitHub Actions and Azure DevOps?"

> Both are CI/CD platforms, but:
> - **GitHub Actions** is simpler, GitHub-native, larger marketplace
> - **Azure DevOps** has richer Azure integration, better variable groups, test plans, and boards
>
> I choose based on the company's stack. GitHub Actions for GitHub-centric teams, Azure DevOps for Azure-heavy infrastructure.

### Q5: "How do you deploy to Azure using GitHub Actions?"

> Use the `azure/login` action with Azure credentials, then native actions:
> ```yaml
> - uses: azure/login@v2
>   with:
>     creds: ${{ secrets.AZURE_CREDENTIALS }}
> - uses: azure/webapps-deploy@v3
>   with:
>     app-name: myapp
>     package: .
> ```
> For Terraform: Use `hashicorp/setup-terraform` with Azure env vars.

### Q6: "How do you handle monorepo CI/CD with GitHub Actions?"

> Path filtering:
> ```yaml
> on:
>   push:
>     paths:
>       - 'service-a/**'
>       - 'service-b/**'
>       - '!**.md'
> ```
> Each service has its own workflow file. Only the affected service's pipeline runs. Saves time and resources.

### Q7: "What is a self-hosted runner and when would you use it?"

> Self-hosted runners are machines you manage (on-prem or VM) that run GitHub Actions jobs. Use when:
> - Need access to internal/corporate network
> - Need specific software not available on GitHub-hosted runners
> - Need more resources (CPU, memory) than GitHub provides
> - Compliance reasons (data cannot leave your network)

### Q8: "How do you cache dependencies in GitHub Actions?"

> ```yaml
> - uses: actions/setup-node@v4
>   with:
>     node-version: '20'
>     cache: 'npm'
> - run: npm ci
> ```
> Cache key is based on the lock file. If `package-lock.json` changes, cache invalidates. Reduces install time from minutes to seconds.

### Q9: "What is GITHUB_TOKEN and how do you use it?"

> GITHUB_TOKEN is an automatically-generated secret available to every workflow. It has permissions scoped to the repo. Use it to:
> - Push to the repo: `GITHUB_TOKEN`
> - Create issues: `GITHUB_TOKEN`
> - Comment on PRs: `GITHUB_TOKEN`
> - Deploy to GitHub Pages: `GITHUB_TOKEN`
>
> Permissions can be customized in the workflow:
> ```yaml
> permissions:
>   contents: read
>   issues: write
>   pull-requests: write
> ```

### Q10: "How do you implement approval gates in GitHub Actions?"

> Using Environments:
> 1. Create an Environment (Settings > Environments)
> 2. Add "Required reviewers" to the environment
> 3. Reference it in the workflow:
> ```yaml
> jobs:
>   deploy-prod:
>     environment: production
> ```
> The pipeline pauses, notifies reviewers, and waits for approval before proceeding.

# CI/CD Interview Study Plan

**Target:** DevOps Engineer, 3+ YOE | 7-14 LPA interviews
**Scope:** General CI/CD concepts + GitHub Actions + Deployment Strategies
**Why separate from Azure DevOps:** Product companies use GitHub Actions, GitLab CI, Jenkins alongside Azure DevOps. You need to know CI/CD patterns, not just one tool.

---

## Part 1: CI/CD Fundamentals (Days 1-2)

**Note:** GitHub Actions has its own folder at `github-actions/`. This file covers general concepts only.

### What is CI/CD?

| Term | Meaning | What It Does |
|------|---------|-------------|
| **Continuous Integration (CI)** | Merge code frequently, build + test automatically | Catches bugs early, every PR is validated |
| **Continuous Delivery (CD)** | Keep code always deployable | Every change that passes CI could go to production |
| **Continuous Deployment** | Automatically deploy to production | Every change that passes CI goes to prod (no manual gate) |

### Standard CI/CD Pipeline Flow

```
Developer pushes code
        │
        ▼
   ┌──────────┐
   │  BUILD   │  Compile, install dependencies
   └────┬─────┘
        │
   ┌────▼─────┐
   │  TEST    │  Unit tests, linting, security scan
   └────┬─────┘
        │
   ┌────▼──────┐
   │  BUILD    │  Build Docker image, tag with commit SHA
   │  ARTIFACT │
   └────┬──────┘
        │
   ┌────▼─────┐
   │  STAGE   │  Deploy to staging, integration tests
   └────┬─────┘
        │
   ┌────▼────┐
   │ APPROVAL│  Manual gate (for prod)
   └────┬────┘
        │
   ┌────▼─────┐
   │  PROD    │  Deploy to production
   └──────────┘
```

### Key CI/CD Concepts (Interview Gold)

| Concept | What It Means | Why It Matters |
|---------|--------------|----------------|
| **Build once, deploy many** | One artifact goes through all environments | Same binary tested in staging goes to prod — no rebuild |
| **Immutable artifacts** | Never change a built artifact | If it passed tests, its the same thing going to prod |
| **Trunk-based development** | Short-lived branches, merge to main daily | Avoids merge hell, enables CI |
| **Feature flags** | Toggle features without deployment | Decouple release from deploy |
| **Shift left** | Test earlier in the pipeline | Catch issues in CI, not in production |

---

## Part 2: GitHub Actions (Quick Reference)

**GitHub Actions has its own folder:** `github-actions/study-plan.md` for full coverage.
This section is just key comparison points for interviews.

| Feature | What It Is | 
|---------|-----------|
| Workflow | Pipeline defined in `.github/workflows/*.yml` |
| Job | Unit of work running on a runner |
| Step | Individual command within a job |
| Runner | Machine executing jobs (`ubuntu-latest`, etc.) |
| Action | Reusable unit of code (`actions/checkout@v4`) |
| Matrix | Run same job with multiple OS/version combos |

**Key comparison — GitHub Actions vs Azure DevOps:**
> GitHub Actions is simpler, GitHub-native, larger marketplace. Azure DevOps has richer Azure integration and variable groups. I'm comfortable with both.

**Terraform CI/CD pattern (same approach, different syntax):**
> The pattern is identical regardless of CI/CD tool: init -> validate -> plan (save artifact) -> approval -> apply (use saved plan). See `github-actions/` for full YAML.

---

## Part 3: Jenkins (Day 3 — Overview Only)

### Why Jenkins Is Still Relevant
- Many legacy product companies still use it
- If you can explain Jenkins, it shows breadth

### Key Differences

| Feature | GitHub Actions | Jenkins |
|---------|---------------|---------|
| Hosting | Managed by GitHub | Self-hosted |
| Setup | Zero (built into GitHub) | Install on server/VM |
| Pipeline syntax | YAML | Groovy (Jenkinsfile) |
| Plugins | Marketplace | Extensive plugin ecosystem |
| When to use | New projects, GitHub repos | Complex pipelines, on-prem |

### Jenkins Pipeline (For comparison)
```groovy
pipeline {
    agent any
    
    stages {
        stage('Build') {
            steps {
                sh 'npm install'
            }
        }
        stage('Test') {
            steps {
                sh 'npm test'
            }
        }
        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                sh 'echo Deploying...'
            }
        }
    }
}
```

---

## Part 4: Deployment Strategies (Day 6)

**Interview question:** "How do you deploy without downtime?"

### Strategy 1: Rolling Update
```
Old: [VM1] [VM2] [VM3] [VM4] [VM5]
Step 1: [NEW] [VM2] [VM3] [VM4] [VM5]  ← 1 server updated
Step 2: [NEW] [NEW] [VM3] [VM4] [VM5]  ← 2 servers updated
Step 3: [NEW] [NEW] [NEW] [VM4] [VM5]  ← continue...
Final:  [NEW] [NEW] [NEW] [NEW] [NEW]
```
**Pros:** Zero downtime, no extra capacity needed
**Cons:** Slow, clients hit both old and new during transition

### Strategy 2: Blue-Green
```
Before: [BLUE] → active  |  [GREEN] → idle
Step 1: Deploy new version to GREEN
Step 2: Run tests on GREEN
Step 3: Switch router to GREEN
After:  [BLUE] → idle    |  [GREEN] → active
```
**Pros:** Instant switch, easy rollback (switch back to BLUE)
**Cons:** Double the infrastructure cost

### Strategy 3: Canary Release
```
Step 1: Route 5% traffic to new version
Step 2: Monitor for errors
Step 3: Route 25% traffic
Step 4: Route 50%
Step 5: Route 100%
```
**Pros:** Real traffic testing, minimized blast radius
**Cons:** Complex routing, long rollout time

---

## Part 5: CI/CD Interview Questions

### Q1: "What is the difference between CI and CD?"
> CI means every code change is built and tested automatically. CD means every change that passes CI could be deployed to production. CI catches bugs early; CD makes deployment a non-event.

### Q2: "What happens when a build fails in CI?"
> The pipeline stops. The team is notified (Slack, email). Fix is prioritized. Main branch should always be green — broken builds block everyone.

### Q3: "How do you handle database migrations in CI/CD?"
> Migrations are part of the deployment. Pattern:
> 1. Run migration as pre-deploy step (backward-compatible)
> 2. Deploy new code
> 3. Run post-deploy migrations if needed
> Key: Migrations must be backward-compatible with old code (add columns, dont remove)

### Q4: "What is build once, deploy many?"
> Build the artifact ONCE (e.g., Docker image with commit SHA as tag). Use that EXACT same artifact in dev, staging, and prod. This way, what was tested in staging is what runs in production. No "works on my machine" issues.

### Q5: "How do you secure a CI/CD pipeline?"
> - Secrets in vault/KV, never in YAML
> - Least privilege for service connections
> - Code scanning (SAST) in pipeline
> - Dependency scanning (SCA)
> - Signed commits
> - Branch protection (no direct push to main)

---

## Quick Reference: CI/CD Tool Comparison

| Feature | GitHub Actions | Azure DevOps | Jenkins | GitLab CI |
|---------|---------------|-------------|---------|-----------|
| Pipeline as code | YAML | YAML | Groovy | YAML |
| Managed | Yes | Yes | No | Yes |
| Free minutes | 2000/mo | 1800/mo | Unlimited | 400/mo |
| Terraform support | hashicorp/setup-terraform | AzureCLI task | Plugin | Built-in |
| Container support | Native | Native | Plugin | Native |
| Learning curve | Low | Medium | High | Low |

---

## Key CI/CD Principles For Interviews

```
1. FAIL FAST — fail early, fail loudly
2. BUILD ONCE — same artifact through all environments
3. SHIFT LEFT — test earlier, find bugs sooner
4. IMMUTABLE — never modify a built artifact
5. SECRETS NEVER IN CODE — always from vault/env
6. MAIN IS ALWAYS GREEN — broken builds are emergencies
7. APPROVAL FOR PROD — always a human gate for production
```

---

*Next: topics/01-github-actions-deep-dive.md (if needed)*

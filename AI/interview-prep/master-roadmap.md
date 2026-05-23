# Master Roadmap: Beast Mode — 7-14 LPA Interview-Ready

**Target:** DevOps Engineer, 3 YOE | Indian Product Companies | Azure + Terraform Stack
**Salary Band:** INR 7-14 LPA (current: ~3 LPA)
**Duration:** 8 weeks × 14h/week = 112h total
**Method:** Every concept = LEARN + BUILD + PRODUCTION STORY + INTERVIEW DRILL
**Portfolio Project:** `soham-devops/infrastructure-pipeline` (built across all 8 weeks)

---

## Complete Tool Audit

| # | Skill | Folder | JD% | Required Depth for 7-14 LPA | Weeks |
|---|-------|--------|-----|---------------------------|-------|
| 1 | **Terraform** | `terraform/` | 90% | State, HCL, modules, backend, workspaces, import, lifecycle, CI/CD, debugging | 1-4, 7 |
| 2 | **Git** | `git/` | 90% | Branching strategies, merge vs rebase, PR workflow, revert, reset, cherry-pick | 1, 5, 7 |
| 3 | **GitHub Actions** | `github-actions/` | 85% | Workflows, triggers, matrix, OIDC, plan-on-PR, apply-on-merge, approvals | 3, 7 |
| 4 | **Azure Networking** | `azure/topics/01-vnet-architecture.md` | 80% | VNet, CIDR, subnets, NSG, ASG, VNet peering, App Gateway, WAF | 1-2, 4, 7 |
| 5 | **Azure Compute** | `azure/` | 80% | VM, VMSS, LB (internal/public), availability zones, scale sets | 2, 7 |
| 6 | **Azure Security** | `azure/` | 70% | IAM, RBAC, Managed Identity, Key Vault, NSG, Azure Firewall | 2, 4, 7 |
| 7 | **Azure Storage** | `azure/` | 70% | Blob tiers, SAS tokens, lifecycle, Azure Files | 2, 7 |
| 8 | **Docker** | `docker-k8s/` | 70% | Dockerfile, layer caching, multi-stage, compose, ACR, CI/CD integration | 3, 7 |
| 9 | **Ansible** | `ansible/` | 70% | Playbooks, roles, vault, dynamic inventory, Terraform integration | 5, 7 |
| 10 | **LogicMonitor** | `logicmonitor/` | 70%* | Interview articulation, STAR stories, real incidents (you already know the tool) | 6 |
| 11 | **Linux + Bash** | `linux-scripting/` | 60% | 30 essential commands, health check script, troubleshooting | 5, 7 |
| 12 | **Azure DevOps** | `azure-devops/` | 60% | YAML pipelines, service connections, variable groups, Terraform integration | 3, 7 |
| 13 | **Azure Monitor** | `azure/` | 50% | Log Analytics, metric alerts, diagnostic settings, action groups | 4, 7 |
| 14 | **Azure Cost + Gov** | `azure/` | 40% | Tags, budgets, Azure Policy, reservations (1 day only) | 4 |

\* LM: you already use it daily — articulation takes minimal time.

**EXCLUDED (zero ROI for 7-14 LPA):**
- Kubernetes/AKS (35% JD — not asked at this level)
- Prometheus / Grafana / ELK (you use LogicMonitor)
- System Design (30% JD — senior role topic)
- Helm, Service Mesh, DevSecOps (senior topics)
- Jenkins (covered conceptually in CI/CD)

---

## 8-Week Beast Structure

### Week 1: Foundation + First Deploy
**Theme:** Deploy something real on Day 1. Build confidence immediately.

| Day | Topic | Builds Project |
|-----|-------|---------------|
| 1 | Terraform State + HCL | main.tf → Azure RG + VM |
| 2 | Azure VNet + Subnets + CIDR | VNet + 2 subnets in Terraform |
| 3 | Variables + Outputs + Locals | Parameterized config |
| 4 | NSG + Security Rules | NSG + ASG + tags |
| 5 | Remote State (Azure Storage) | backend.tf, state migration |
| 6 | Git Branching + PR Workflow | GitHub repo, branch protection |
| **Sun** | **MOCK 1** | Record + critique |

### Week 2: Terraform Deep + Azure Compute
**Theme:** Build scalable infrastructure with industry-standard patterns.

| Day | Topic | Builds Project |
|-----|-------|---------------|
| 8 | Terraform Modules | VNet module + NSG module |
| 9 | Azure VM + VMSS + LB | VMSS module + LB module |
| 10 | Lifecycle + DAG | create_before_destroy rules |
| 11 | App Gateway + WAF + SSL | App Gateway module |
| 12 | Workspaces + Environments | dev/staging/prod configs |
| 13 | Azure Storage Deep | Storage account module |
| **Sun** | **MOCK 2** | Record + critique |

### Week 3: CI/CD Pipeline + Docker
**Theme:** Automate everything. Build your first full pipeline.

| Day | Topic | Builds Project |
|-----|-------|---------------|
| 15 | GitHub Actions Fundamentals | validate + fmt on PR |
| 16 | GitHub Actions Terraform Pipeline | OIDC, plan → apply |
| 17 | Azure DevOps Pipelines | Equivalent ADO pipeline |
| 18 | Dockerfile + Layer Caching | Dockerfile for app |
| 19 | Multi-stage + Compose | Optimized Dockerfile |
| 20 | ACR + Docker Push in CI/CD | Build → push → deploy |
| **Sun** | **MOCK 3** | Record + critique |

### Week 4: Security + State Ops + Deployment Strategies
**Theme:** Production-grade patterns. Junior vs senior distinction.

| Day | Topic | Builds Project |
|-----|-------|---------------|
| 22 | IAM + RBAC + Managed Identity | MI + RBAC in Terraform |
| 23 | Key Vault + Secrets Management | KV module, secrets |
| 24 | Terraform Import + State Surgery | Import existing resource |
| 25 | Blue-Green + Rolling + Canary | App Service slots |
| 26 | Azure Monitor + Log Analytics | Diagnostic settings, alerts |
| 27 | Azure Cost + Governance | Budgets, Policy, tags |
| **Sun** | **MOCK 4** | Record + critique |

### Week 5: Ansible + Linux + Git Advanced
**Theme:** Complete the deployment stack.

| Day | Topic | Builds Project |
|-----|-------|---------------|
| 29 | Ansible Architecture + Playbooks | First playbook, inventory |
| 30 | Ansible Roles + Vault + Dynamic Inventory | Role structure, Vault |
| 31 | Terraform + Ansible Integration | TF triggers Ansible |
| 32 | 30 Essential Linux Commands | Reference card |
| 33 | Bash Scripting | Health check script |
| 34 | Git Advanced | Rebase, cherry-pick, revert |
| **Sun** | **MOCK 5** | Record + critique |

### Week 6: LogicMonitor + Integration + Wipro Story
**Theme:** Turn your existing experience into interview gold. Connect all tools.

| Day | Topic | Builds Project |
|-----|-------|---------------|
| 36 | LM Interview Reframe | 3 versions of LM story |
| 37 | LM Q&A + STAR | 15 LM questions answered |
| 38 | Full Pipeline from Memory | Rebuild pipeline without notes |
| 39 | Wipro → Product Answers | Tell me about yourself |
| 40 | 5 STAR Stories | Problem, failure, conflict, above-beyond, leadership |
| 41 | Company Research | 5 target companies analyzed |
| **Sun** | **MOCK 6** | Record + critique |

### Week 7: Rapid Fire + Resume + Salary Strategy
**Theme:** Build speed. Prepare logistics.

| Day | Topic | Action |
|-----|-------|--------|
| 43 | Resume Tailoring | 3 versions, keywords, quantified |
| 44 | Salary Strategy | 3→14 LPA justification script |
| 45 | Terraform Rapid Fire | 60 Q&A in 30 min |
| 46 | Azure Rapid Fire | 50 Q&A in 25 min |
| 47 | CI/CD + Docker + Git Rapid Fire | 40 Q&A in 20 min |
| 48 | Ansible + Linux + LM Rapid Fire | 30 Q&A in 15 min |
| **Sun** | **MOCK 7** | Record + critique |

### Week 8: Final Mock + Applications + Buffer
**Theme:** Execute. Apply. Interview. Win.

| Day | Action |
|-----|--------|
| 50 | FINAL MOCK 8 — 1 hour, no notes, recorded |
| 51 | Apply Tier 1: Freshworks + Razorpay + BrowserStack |
| 52 | Screening Prep — record + practice each answer |
| 53 | Apply Tier 2: Postman + Atlassian India + Chargebee |
| 54 | Whiteboard Drill — draw to camera, explain while drawing |
| 55 | Apply Tier 3 + Follow-ups |
| 56 | Confidence Day — review weak spots, rehearse salary |
| 57-60 | Buffer for actual interviews |

---

## How Each Day Works

```
STEP 1: Select "Teacher" from agent list
STEP 2: Say "Start Day [NUMBER]"
STEP 3: Teacher checks .teacher-context.json
STEP 4: Teacher reads today's lesson from DAILY_PLAN.md
STEP 5: Execute 4-Block:
        ┌────────────────────────────────────────────┐
        │ 30 min LEARN    → Deep concept explanation  │
        │ 30 min BUILD    → Add to project            │
        │ 30 min PRODUCE  → Production story + WHY    │
        │ 30 min DRILL    → Interview Q&A out loud    │
        └────────────────────────────────────────────┘
STEP 6: Teacher updates .teacher-context.json
STEP 7: (Sunday) Mock interview → record → critique → redo
```

---

## Interview Answer Strategy (Indian Product Companies)

| Question Type | Approach | Example Answer |
|--------------|----------|---------------|
| "Tell me about yourself" | Current role → skills → impact → why product company | "I'm a DevOps engineer at Wipro. I manage 40+ Azure VMs, automate infrastructure with Terraform, run CI/CD pipelines on GitHub Actions, and monitor everything with LogicMonitor. I reduced deployment time by 60% through automation. I'm looking for a product company where my infrastructure decisions directly impact end users." |
| "Why leave Wipro?" | Want product impact + faster growth + modern stack | "Wipro gave me great foundational experience, but I want to work on a single product where I can deeply understand the application and optimize infrastructure for it. Product companies offer that depth and ownership." |
| "Why Azure?" | Enterprise-grade, strong DevOps integration | "Azure has the best Terraform integration of any cloud. Its DevOps tooling — Azure DevOps, GitHub Actions, Managed Identity — makes infrastructure automation seamless." |
| "Terraform vs Ansible?" | They complement, not compete | "Terraform is for provisioning infrastructure — it's declarative, stateful, perfect for cloud resources. Ansible is for configuration — it's procedural, agentless, perfect for setting up servers. I use both: Terraform creates the VM, Ansible configures it." |
| "Current vs expected CTC" | Market-based + skill justification | "My current CTC is 3 LPA. Based on my expanded skillset — Terraform, Azure, CI/CD, Docker — and market rates for 3 YOE DevOps engineers in product companies, I'm looking at 10-14 LPA range." |
| "Describe a complex problem" | STAR with quantified results | "Situation: Our deployment process was manual and took 4 hours. Task: Automate it. Action: Built a Terraform + GitHub Actions pipeline with blue-green deployment. Result: Deployment time reduced to 10 minutes with zero downtime." |

---

## Company Target List

### Tier 1 (Best Fit — Azure + Terraform heavy)
- **Freshworks** (Chennai) — Azure primary, Terraform used, good DevOps culture
- **Razorpay** (Bangalore) — Heavy Terraform user, multi-cloud, strong engineering
- **Postman** (Bangalore) — Azure DevOps openings, strong engineering culture
- **BrowserStack** (Mumbai) — Azure-based infra, DevOps-first culture

### Tier 2 (Good Fit)
- **Atlassian India** (Bangalore) — Azure + AWS, Terraform standard, remote-friendly
- **Chargebee** (Chennai) — Azure + Terraform, product company
- **Microsoft India** (Hyderabad/Bangalore) — Azure native, DevOps roles
- **Uber India** (Bangalore) — Multi-cloud, Terraform heavy

### Tier 3 (Mid-size, Salary Match)
- **Groww** (Bangalore) — Azure + K8s (K8s is minimal at this level)
- **Druva** (Pune) — Azure native, SaaS product
- **Zoho** (Chennai) — Own cloud, strong engineering culture
- **Intuit India** (Bangalore) — AWS primary but Azure roles exist

---

## After You Get The Job (6 months later)

Once you're in a product company at 10-14 LPA, next growth path:
- **14-20 LPA:** Deeper Terraform, K8s introduction, Helm, platform engineering
- **20-30 LPA:** Senior DevOps — architecture, cost optimization, mentoring, multi-cloud
- **30+ LPA:** Staff/Principal — org-wide platform strategy

But first: crush the 7-14 LPA interviews. One step at a time.

---

*Beast Mode initialized. Let's get you hired.*

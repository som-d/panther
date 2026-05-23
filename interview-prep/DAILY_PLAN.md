# Beast Mode: 7-14 LPA Interview-Ready Plan

**Purpose:** Turn you into a DevOps engineer that every product company wants to hire.
**Method:** Every concept = LEARN + BUILD + PRODUCTION STORY + INTERVIEW DRILL.
**Time:** 2h/day Mon-Sat + 2h Sunday mock = 14h/week × 8 weeks = 112h total.
**Stack:** (Linux + Git) + (Terraform + Azure) — integrated learning path:
- **Phase 1:** Git CLI + Linux terminal foundations taught together (every command teaches Linux as byproduct)
- **Phase 2 onward:** Terraform + Azure simultaneously — every Azure concept built WITH Terraform code
- **Teaching style:** Command-first — every flag, pipe, operator, and output explained before execution
- **Environment:** CLI-only (VS Code Remote SSH), no desktop/UI, SSH-only for compliance
**Credits:** Azure for Students — $100 free credits (365 days). Every BUILD block deploys real resources.

---

## The Daily 4-Block Formula (2 hours)

Every single day follows this exact structure:

```
┌──────────────────────────────────────────────────────────────┐
│                    2-HOUR DAILY SESSION                       │
├──────────────────────────────────────────────────────────────┤
│ Block 1 │ 30 min │ LEARN     │ Deep concept with Teacher     │
│ Block 2 │ 30 min │ BUILD     │ Add to your portfolio project │
│ Block 3 │ 30 min │ PRODUCE   │ Production story + WHY it     │
│         │        │           │ matters in real companies     │
│ Block 4 │ 30 min │ DRILL     │ Interview Q&A out loud        │
│         │        │           │ (record if possible)          │
└──────────────────────────────────────────────────────────────┘
```

## The Sunday Mock Formula (2 hours)

```
┌──────────────────────────────────────────────────────────────┐
│                   SUNDAY MOCK INTERVIEW                       │
├──────────────────────────────────────────────────────────────┤
│ 30 min │ Full technical drill on week's topics               │
│ 30 min │ Behavioral + STAR stories                           │
│ 30 min │ Watch recording, identify hesitation points         │
│ 30 min │ Re-do weak answers until smooth                     │
└──────────────────────────────────────────────────────────────┘
```

**Progression:** Mock 1 will be rough. Mock 8 will be interview-ready. Trust the process.

---

## Drift Prevention: How We Stay On Track

### The 5-Layer Tracking System

```
LAYER 1: DAILY GATE CHECK ──── "Can I answer today's drill question smoothly?"
  ↓ Pass → Move to next day
  ↓ Fail → Teacher re-teaches, you re-do drill, try again tomorrow
  If you can't answer the drill question without pausing → NOT ready → repeat

LAYER 2: WEEKLY GATE CHECK (Sunday Mock) ──── "Can I pass the 10-question test?"
  ↓ 8/10 correct → Move to next week
  ↓ < 8/10 → Teacher identifies weak days, you re-do them Mon-Tue, re-test Wed
  The Sunday mock is NOT optional. It's the gate that prevents weak foundations.

LAYER 3: VISUAL DASHBOARD ──── "Where am I right now?"
  See the Progress Dashboard below — one glance tells you everything.

LAYER 4: TEACHER ENFORCEMENT ──── "The teacher won't let you skip."
  Every session starts with checking .teacher-context.json.
  Teacher won't proceed to Day N+1 until Day N drill is passed.
  No "I'll come back to this later" — basics must be solid before advancing.

LAYER 5: WEEKLY RETROSPECTIVE ──── "What did I actually learn this week?"
  After Sunday mock, write down:
  - 3 things I understood well
  - 2 things I'm still shaky on
  - 1 thing I need to review
  Logged in .teacher-context.json. Reviewed at start of next week.
```

### What "Ready to Move On" Looks Like

For each day, the gate is simple:

| Block | You're Ready When... |
|-------|---------------------|
| LEARN | You can explain the concept in your own words without looking at notes |
| BUILD | The code compiles/runs and you understand what each line does |
| PRODUCE | You can retell the production story with the key lesson |
| DRILL | You answer the interview question smoothly, without "um" or long pauses |

If any block fails → repeat that block tomorrow before new content.

### What "Behind" Looks Like & How We Fix It

```
SCENARIO                    DIAGNOSIS                    FIX
───────────────────────     ────────────────────────     ──────────────────────
Missed 1-2 days            Life happens, no problem     Catch up on weekend
Missed 3-5 days            Motivation dip? Overwhelmed? Teacher does compressed review (30 min per missed day)
Missed 1+ weeks            Something wrong              Reset to last gate that was passed. Restart from there.
Stuck on one topic         Concept not clicking         Teacher tries different approach. More analogies. No pressure.
Confidence score < 3/5     Didn't truly understand      Re-teach + re-drill until confidence ≥ 3
```

**No shame in repeating.** A beast has solid foundations, not rushed progress.

---

## Integrated Learning Path: How It Actually Works

```
PHASE 1: GIT CLI + LINUX TERMINAL (Pre-Day 1, ~2-3 sessions)
┌─────────────────────────────────────────────────────────────┐
│ Every command teaches 2-3 things at once:                   │
│                                                             │
│  echo 'resource "rg" {}' > main.tf                          │
│  ├── Linux: echo + redirection (>)                         │
│  ├── Git: this file will be tracked                         │
│  └── Terraform: HCL syntax (preview)                        │
│                                                             │
│  git add main.tf && git commit -m "first"                   │
│  ├── Git: staging area + commit snapshot                    │
│  ├── Linux: && chaining, string quoting                    │
│  └── Workflow: code → stage → save                          │
└─────────────────────────────────────────────────────────────┘

PHASE 2+: TERRAFORM + AZURE SIMULTANEOUS (Weeks 1-8)
┌─────────────────────────────────────────────────────────────┐
│ Every Azure concept is deployed VIA Terraform.              │
│ No isolated Azure Portal clicking.                          │
│                                                             │
│  Learn Azure VNet  →  Write terraform resource              │
│  Learn NSG rules   →  Write azurerm_network_security_group  │
│  Learn VMSS        →  Write azurerm_linux_virtual_machine   │
└─────────────────────────────────────────────────────────────┘
```

**Why integrated?**
- Linux fluency is a **byproduct** of doing everything in terminal — no separate Linux lectures
- Git is learned by **using it every session** — not as a one-off topic
- Terraform + Azure together because **Terraform IS how you interact with Azure** in real DevOps jobs
- Every command you type builds **3 skills at once** — faster progress, better retention

---

## Learning Progression: How Every New Topic Is Taught

For tools you've NEVER used (Terraform, Docker, GitHub Actions — brand new):

```
LEARN BLOCK (30 min)
├── STEP 1: What Is It? (5 min)
│   └── Simplest explanation. One analogy. 
│   └── Example: "Terraform is like a blueprint for your cloud. You write what you want, it builds it."
│
├── STEP 2: Why Does It Matter? (5 min)
│   └── Problem it solves. What life was like before.
│   └── Example: "Before Terraform, engineers clicked buttons in Azure Portal. Manual = mistakes."
│
├── STEP 3: How Does It Work? (10 min) 
│   └── Core mechanics. Key concepts. No syntax yet.
│   └── Example: "Terraform reads .tf files → builds a dependency graph → compares with state → applies changes."
│
├── STEP 4: How Do You Use It? (8 min)
│   └── Syntax. Commands. Practical example you can type.
│   └── Example: "Here's a simple main.tf. Let me explain every line."
│
└── STEP 5: Where Does It Fit? (2 min)
    └── In the overall pipeline. How it connects to yesterday's topic.
```

For tools you ALREADY know (Ansible, LogicMonitor, Git basics — daily use):

```
LEARN BLOCK (30 min) — COMPRESSED
├── STEP 1: Quick Reframe (3 min)
│   └── "You use this daily. Here's how to talk about it in interviews."
│
├── STEP 2: Interview Angle (7 min)
│   └── What interviewers ask about this tool. Key buzzwords.
│
├── STEP 3: Production Stories (10 min)
│   └── Your real experiences → reframe for product companies.
│
└── STEP 4: Gaps & Deepening (10 min)
    └── What you don't know yet about this tool. Fill the gaps.
```

### Topic Newness Map (so you know what to expect)

```
LAYER 1: ALWAYS-ON FOUNDATION (not separate days — learned by doing)
────────────────────────────────────────────────────────────────────
Linux terminal    ├── pwd, ls, cd, mkdir, touch, echo, cat, nano
                  ├── pipes (|), redirection (> >>), chaining (&& ;)
                  └── permissions, paths, environment variables

Git CLI           ├── init, add, commit, status, log, diff
                  ├── remote add, push, pull, branch
                  └── .gitignore, restore, reset, amend

Both learned simultaneously through every command in every session.
No isolated "Linux lecture" or "Git lecture."


LAYER 2: MAIN CURRICULUM
BRAND NEW (full 5-step LEARN)     SOME EXPOSURE (hybrid)     KNOWN (compressed)
────────────────────────────      ─────────────────────      ─────────────────
Terraform (HCL, state, mods)      Azure (VMs, VNet, IAM)     Ansible
GitHub Actions                    Linux (beyond basics)      LogicMonitor
Docker / Docker Compose                                       
Azure DevOps YAML
CI/CD patterns
Bash scripting
```

---

## Progress Dashboard

### Weekly Overview

```
PHASE  STATUS       DAYS DONE    GATE PASSED    CONFIDENCE
─────  ──────────   ─────────    ───────────    ─────────────────
PreR   Git+Terminal ✅✅✅⬜⬜⬜  3/6 ✅ Pass    ★★★★☆ Ready for Wk1
Wk 1   ⬜⬜⬜⬜⬜⬜   0/6          ❌ Not yet      ★★★★★ Start Day 1
Wk 2   ⬜⬜⬜⬜⬜⬜   0/6          ❌ Not yet      —
Wk 3   ⬜⬜⬜⬜⬜⬜   0/6          ❌ Not yet      —
Wk 4   ⬜⬜⬜⬜⬜⬜   0/6          ❌ Not yet      —
Wk 5   ⬜⬜⬜⬜⬜⬜   0/6          ❌ Not yet      —
Wk 6   ⬜⬜⬜⬜⬜⬜   0/6          ❌ Not yet      —
Wk 7   ⬜⬜⬜⬜⬜⬜   0/6          ❌ Not yet      —
Wk 8   ⬜⬜⬜⬜⬜⬜   0/6+2        ❌ Not yet      —
```

Each day completed = ⬛. Each day missed/weak = ⬜ with note.

### Gate Pass/Fail History

```
PHASE  MOCK RESULT                 GATE?   ACTIONS
─────  ───────────────────────────  ─────   ─────────────────────────────────────
PreR   Phase 1: Git+Terminal ✅    ✅ Pass Steps 1-3 complete. Ready for Wk1 Day 1
Wk 1   —                            ❌      Not taken yet
Wk 2   —                            ❌      Not taken yet
Wk 3   —                            ❌      Not taken yet
Wk 4   —                            ❌      Not taken yet
Wk 5   —                            ❌      Not taken yet
Wk 6   —                            ❌      Not taken yet
Wk 7   —                            ❌      Not taken yet
Wk 8   —                            ❌      Not taken yet
```

**Updated by Teacher after every session and every Sunday mock.**

### Drill Confidence Tracker

```
PHASE 1 — GIT CLI + TERMINAL FOUNDATIONS (Pre-Day 1)
DAY  DRILL QUESTION                           CONFIDENCE (1-5)
───  ───────────────────────────────────────  ─────────────────
P1   What does `ls -la` tell you?             ★★★★☆ ✅ Covered
P1   Explain git staging vs commit            ★★★★☆ ✅ Covered
P1   What does `git remote add` do?           ★★★★☆ ✅ Covered
P1   What is `git reset --soft` vs --hard?    ★★★☆☆ ✅ Covered (drill next)
P1   How to undo a commit?                    ★★★☆☆ ✅ Covered (drill next)
P1   What is `git checkout --orphan`?         ★★★☆☆ ✅ Covered (drill next)
P1   GitHub Push Protection — what is it?     ★★★★☆ ✅ Covered
```

**Each drill gets a confidence score. < 3 = re-do before moving on.**

---

## How The Teacher Enforces This

Every session, Teacher:
1. Reads `.teacher-context.json` — checks your exact position
2. Checks last day's drill confidence — if < 3, you re-do it first
3. Checks spaced repetition queue — reviews due topics
4. Checks weak spots list — any topic with confidence < 3 gets re-drilled
5. Only THEN proceeds to new content

**You cannot skip. You cannot fake it. The teacher tracks everything.**

---

## The Portfolio Project (Build Across All 8 Weeks)

```
GitHub: github.com/som-d/AzureVM/panther/
├── .github/workflows/
│   ├── terraform-plan.yml          # Plan on PR
│   ├── terraform-apply.yml         # Apply on merge to main
│   └── docker-build-push.yml       # Build + push to ACR
├── terraform/
│   ├── modules/
│   │   ├── networking/             # VNet, subnets, NSG
│   │   ├── compute/                # VMSS, LB, App Gateway
│   │   ├── security/               # Key Vault, RBAC, MI
│   │   └── storage/                # Storage account
│   ├── environments/
│   │   ├── dev/                    # Dev workspace + tfvars
│   │   ├── staging/                # Staging workspace + tfvars
│   │   └── prod/                   # Prod workspace + tfvars
│   └── main.tf                     # Root module
├── docker/
│   ├── Dockerfile                  # Multi-stage build
│   └── docker-compose.yml          # Local development
├── ansible/
│   ├── playbooks/                  # Post-deploy configuration
│   └── roles/                      # Web server, app server
├── scripts/
│   └── health-check.sh             # Bash health monitoring
└── README.md                       # Architecture documentation
```

**Interview answer ready by Week 8:**
> *"Here's my GitHub. I built a complete infrastructure pipeline from scratch — Terraform provisions Azure infrastructure, Docker containerizes the app, Ansible configures servers, and GitHub Actions automates the entire flow from commit to production. Let me walk you through the architecture."*

---

## WEEK 1: Foundation + First Deploy

**Theme:** Deploy something real on Day 1. Build confidence immediately.

**Learning Progression:**
- Days 1-5: **BRAND NEW** (Terraform, Azure networking, remote state) → Full Step 1-5 LEARN
- Day 6: **KNOWN** (Git basics) → Compressed LEARN, focus on interview depth
- Azure: **SOME EXPOSURE** → Faster through basics, more time on Terraform integration

| Day | LEARN (30m) | BUILD (30m) | PRODUCTION STORY (30m) | INTERVIEW DRILL (30m) |
|-----|------------|------------|----------------------|---------------------|
| 1 | **BRAND NEW:** Terraform State + HCL basics
What→Why→How→Use→Fit | Write main.tf with Azure provider → deploy RG + VM | "Someone deleted the state file — took 2 days to manually import 50 resources back. After that: Azure Storage backend + locking + soft-delete." | **"Explain Terraform state to a non-technical person in 30 seconds."** → Record yourself, redo until smooth |
| 2 | **SOME EXP:** Azure VNet + Subnets + CIDR
Faster basics → Deep Terraform integration | Add VNet with 2 subnets (public/private) to Terraform | "A startup used /16 for everything — ran out of IPs in 6 months. Always plan CIDR for growth." | **"Design a VNet for a 3-tier web application. Walk me through your CIDR design."** |
| 3 | **BRAND NEW:** Terraform variables + outputs + locals
What→Why→How→Use→Fit | Parameterize: env prefix, CIDR, location, naming convention | "My first Terraform was 4000 lines of main.tf. Unreadable. Variables + modules fixed it." | **"How do you handle environment differences in Terraform?"** |
| 4 | **SOME EXP:** Azure NSG + security rules
Faster basics → Deep Terraform integration | NSG with SSH/HTTP/HTTPS, ASG for web/app tiers, tagging | "Someone opened SSH to 0.0.0.0/0 on production. Crypto miner in 4 hours. $12K bill." | **"How do you secure Azure infrastructure? Walk me through your NSG design."** |
| 5 | **BRAND NEW:** Remote state + state locking (Azure Storage)
What→Why→How→Use→Fit | Create backend.tf, migrate state to Azure Storage blob | "Two engineers ran apply simultaneously → corrupted state file. After that: state locking + blob soft-delete." | **"Why remote state? What happens if you lose the state file? Explain state locking."** |
| 6 | **KNOWN:** Git branching + PR workflow
Quick reframe → Interview depth | Git init, .gitignore, feature branch, PR, merge, branch protection | "A junior dev force-pushed to main → lost 2 days of work. After that: branch protection + mandatory PRs." | **"What's your Git branching strategy? When do you rebase vs merge?"** |
| **Sun** | **MOCK 1** | **30 min tech (Terraform + Azure + Git) + 15 min behavioral → RECORD + SELF-CRITIQUE** | | |
| | | **Gate Check:** Can you explain Terraform state + VNet design + Git branching without hesitation? If not → repeat weak days Mon-Tue, re-mock Wed. | | |

---

## WEEK 2: Terraform Deep + Azure Compute

**Theme:** Build scalable infrastructure with industry-standard patterns.

**Learning Progression:**
- Days 8-10, 12-13: **BRAND NEW** (Modules, lifecycle, workspaces, storage) → Full Step 1-5 LEARN
- Days 11: **SOME EXPOSURE** (App Gateway, you know LB basics) → Faster through basics

| Day | LEARN (30m) | BUILD (30m) | PRODUCTION STORY (30m) | INTERVIEW DRILL (30m) |
|-----|------------|------------|----------------------|---------------------|
| 8 | Terraform modules (structure, input/output, registry) | Extract VNet module + NSG module. Root uses modules. | "Monorepo Terraform had 20,000 lines. Impossible to review. Modules reduced it to 500 lines per team." | **"Why Terraform modules? Design a module structure for a microservice architecture."** |
| 9 | Azure VM + VMSS + Load Balancer (types, health probes, scaling) | VMSS module + LB module. VMSS behind internal LB. | "VMSS without health probes → serving failed instances for 3 hours before anyone noticed." | **"How do you achieve high availability for a web application on Azure?"** |
| 10 | Terraform lifecycle + DAG (create_before_destroy, prevent_destroy) | Apply lifecycle rules: update VMSS without downtime | "Wrong lifecycle config → Terraform wanted to destroy the production database (prevent_destroy saved us)." | **"How does Terraform handle dependencies? What is the DAG? Explain create_before_destroy."** |
| 11 | Azure App Gateway + WAF + SSL | App Gateway module, WAF policy, SSL from Key Vault | "DDoS attack hit the web tier. WAF blocked it. App Gateway saved $50K in compute costs." | **"App Gateway vs Load Balancer? How do you protect web apps from OWASP top 10?"** |
| 12 | Workspaces + environment strategy (dev/staging/prod) | 3 workspace configs with tfvars, consistent naming | "No environment separation → pipeline deployed test changes to production. Customer-facing outage." | **"How do you manage dev/staging/prod with Terraform? Workspace strategy?"** |
| 13 | Azure Storage deep (Blob tiers, SAS tokens, lifecycle) | Storage account module, blob containers, SAS generator | "Production logs filled premium blob storage → $10K unnecessary cost. Lifecycle rules moved to cool tier." | **"Azure Storage options? When Blob vs Disk vs Files? How do you secure storage access?"** |
| **Sun** | **MOCK 2** | **Modules + Compute + Lifecycle + Workspaces + Storage → RECORD + CRITIQUE** | | |
| | | **Focus areas:** Module design reasoning, zero-downtime patterns, environment strategy. | | |

---

## WEEK 3: CI/CD Pipeline + Docker

**Theme:** Automate everything end-to-end. First full pipeline from code to deployment.

**Learning Progression:**
- Days 15-20: **BRAND NEW** (GitHub Actions, Docker — never touched) → Full Step 1-5 LEARN
- Day 17: **BRAND NEW** (Azure DevOps — new tool) → Full Step 1-5 LEARN
- This week is the HEAVIEST new learning. Take it slow. No rushing.

| Day | LEARN (30m) | BUILD (30m) | PRODUCTION STORY (30m) | INTERVIEW DRILL (30m) |
|-----|------------|------------|----------------------|---------------------|
| 15 | **BRAND NEW:** GitHub Actions workflows + triggers
What is CI/CD? → Why automate? → How GH Actions works → Syntax → Pipeline fit | First workflow: `terraform validate` + `fmt` on every PR | "No CI on PR → broken Terraform merged to main. All dev environments broken for a day." | **"Walk me through your CI/CD pipeline from code commit to infrastructure deployment."** |
| 16 | **BRAND NEW:** GH Actions Terraform pipeline
What is OIDC? → Why plan-on-PR? → How approval gates work → Full pipeline | Full pipeline: validate → plan → comment → approve → apply | "Plan on PR caught a subnet CIDR overlap. Would have taken down production networking." | **"How does your Terraform CI/CD pipeline work? How do you handle approval gates?"** |
| 17 | **BRAND NEW:** Azure DevOps YAML pipelines
What is ADO? → Why two CI/CD tools? → How YAML pipelines differ → Compare | Equivalent ADO pipeline for same Terraform workflow | "Client used ADO. Had to migrate from GitHub Actions. Same logic, different syntax." | **"GitHub Actions vs Azure DevOps — pros and cons for Terraform deployments? When would you use each?"** |
| 18 | **BRAND NEW:** Docker: images vs containers
What is Docker? → Why containers? → How images work → Dockerfile syntax → Pipeline fit | Write Dockerfile for a simple web app (Nginx/Python) | "A dev wrote a 2GB Docker image. Pull times: 10 minutes. Multi-stage build: 150MB, 30 seconds." | **"What's the difference between a Docker image and a container? How do Docker layers work?"** |
| 19 | **BRAND NEW:** Multi-stage builds + Docker Compose
What is multi-stage? → Why smaller images? → How compose works for local dev | Multi-stage Dockerfile + docker-compose.yml for local dev | "'Works on my machine' — devs running different versions. Compose fixed it." | **"Why multi-stage builds? Write a multi-stage Dockerfile for a Node.js app."** |
| 20 | **BRAND NEW:** ACR + Docker push in CI/CD
What is container registry? → Why ACR? → How CI/CD pushes images → Tagging strategy | CI/CD pipeline: build image → push to ACR → Terraform pulls on VM | "Wrong image tag → production ran a dev build for 2 days. Always pin versions." | **"How do you manage container images in CI/CD? Tagging strategy? Image retention?"** |
| **Sun** | **MOCK 3** | **Full pipeline walkthrough: git push → CI/CD → Terraform → Docker → Azure → RECORD + CRITIQUE** | | |
| | | **Gate Check:** Can you explain GitHub Actions workflow, Dockerfile layers, and describe the full CI/CD flow without pausing? If not → repeat weak days. This is the most important gate — the pipeline is YOUR story. | | |

---

## WEEK 4: Security + State Operations + Deployment Strategies

**Theme:** Production-grade patterns. What separates junior from senior DevOps.

**Learning Progression:**
- Days 22-23: **SOME EXPOSURE** (Azure IAM, Key Vault — you know Azure basics) → Faster through basics, focus on Terraform integration
- Days 24-27: **BRAND NEW** (State surgery, deployment strategies, monitoring, cost) → Full Step 1-5 LEARN

| Day | LEARN (30m) | BUILD (30m) | PRODUCTION STORY (30m) | INTERVIEW DRILL (30m) |
|-----|------------|------------|----------------------|---------------------|
| 22 | **SOME EXP:** Azure IAM + RBAC + Managed Identity
Quick reframe → Terraform integration depth | Terraform creates Managed Identity, assigns RBAC roles | "Service Principal secret leaked in GitHub → crypto miner deployed on 50 VMs. Now: Managed Identity only, no secrets." | **"How do you authenticate Terraform to Azure? Managed Identity vs Service Principal?"** |
| 23 | **SOME EXP:** Key Vault + secrets management
Quick reframe → Terraform integration depth | Key Vault module, store app secrets, reference in VM via MI | "DB passwords in plaintext app config → audit found it. Now: Key Vault + Managed Identity." | **"How do you manage secrets in Terraform? How do applications access secrets on Azure?"** |
| 24 | **BRAND NEW:** Terraform import + state surgery
What is import? → Why needed? → How state surgery works → Commands | Import an existing Azure resource into state | "Someone deleted a resource via portal. Terraform couldn't plan. Import + state mv fixed it." | **"How do you handle configuration drift? Someone manually changes Azure — what do you do?"** |
| 25 | **BRAND NEW:** Deployment strategies
What is zero-downtime? → Why blue-green? → How slots work → Compare strategies | App Service with deployment slots. CI/CD: deploy → swap → smoke test. | "Blue-green saved us during a DB migration. Rollback in 30 seconds instead of 2 hours." | **"How do you deploy without downtime? Explain blue-green deployment on Azure. Compare with rolling update."** |
| 26 | **BRAND NEW:** Azure Monitor + Log Analytics
What is observability? → Why monitoring? → How Diagnostic Settings + Alerts work | Diagnostic settings (Terraform), Log Analytics, metric alert for CPU > 80% | "Deploy broke the app at 3 AM. No alerts. Customer complaints at 7 AM. 4-hour outage." | **"How do you monitor Azure infrastructure? What metrics do you track? How do you set up alerts?"** |
| 27 | **BRAND NEW:** Azure Cost Management
What is FinOps? → Why governance? → How budgets + policies work | Budget alert, Azure Policy (enforce tags), cost optimization | "Cloud bill went from $5K to $15K overnight. No budget alerts. No tagging for cost allocation." | **"How do you manage cloud costs? How do you enforce governance with Azure Policy and tagging?"** |
| **Sun** | **MOCK 4** | **Security + State operations + Deployment strategies + Monitoring + Cost → RECORD + CRITIQUE** | | |
| | | **Gate Check:** Can you explain Managed Identity, Terraform import, blue-green deployment, and Azure monitoring setup without notes? If confidence < 3 on any → re-drill. This week separates junior from senior. | | |

---

## WEEK 5: Ansible Integration + Linux + Git Advanced

**Theme:** Complete the deployment stack. Terraform → Ansible → Docker pipeline.

**Learning Progression:**
- Days 29-31: **KNOWN** (Ansible — you use it daily) → Quick reframe, interview depth, gap filling
- Days 32-33: **SOME EXPOSURE** (Linux commands, you know basics) → Faster through basics, focus on interview-worthy scenarios
- Day 34: **KNOWN** (Git basics) → Focus on advanced patterns you haven't used

| Day | LEARN (30m) | BUILD (30m) | PRODUCTION STORY (30m) | INTERVIEW DRILL (30m) |
|-----|------------|------------|----------------------|---------------------|
| 29 | **KNOWN:** Ansible architecture
Quick reframe → How to articulate → Interview depth → Gap fill | First playbook: install nginx, configure index.html | "Terraform provisions the VM. Ansible configures it. They complement each other perfectly." | **"Terraform vs Ansible — how do they complement each other? When do you use each?"** |
| 30 | **KNOWN:** Ansible roles + Vault + dynamic inventory
What you DON'T know yet → Fill those gaps | Role for web server, Ansible Vault for secrets, Azure dynamic inventory | "Playbooks in GitHub with plaintext passwords. Ansible Vault encrypts them. Dynamic inventory means no hardcoded IPs." | **"How do you manage secrets in Ansible? How does dynamic inventory work with Azure?"** |
| 31 | **KNOWN:** Terraform + Ansible integration
You know both tools → Now connect them in a pipeline | Terraform triggers Ansible after VM creation | "Full production pattern: Terraform creates VM + NSG → Ansible configures app → Docker runs containers." | **"Walk me through a complete deployment: Terraform creates, Ansible configures. How do they work together?"** |
| 32 | **SOME EXP:** 30 essential Linux commands
Quick review → Commands you DON'T know → Deep scenarios | Create reference card, practice each with real scenarios | "Prod server down at 2 AM. Only SSH access. These 15 commands found the issue in 5 minutes." | **"5 Linux commands you use daily as a DevOps engineer? What do they do? Give an example."** |
| 33 | **SOME EXP:** Bash scripting
What you know → What you DON'T know → Script patterns | Health check script: check service + disk + memory, alert on failure | "Manual server checks at 3 AM every day. Automated with a bash script + cron. Saved 10 hours/week." | **"Write a bash script that checks if a service is running and restarts it if not. Include logging."** |
| 34 | **KNOWN:** Git advanced
You know add/commit/push → Advanced: rebase, cherry-pick, revert | Simulate messy commit history → clean up with interactive rebase | "Accidentally committed to main. Revert? Reset? Lost commits? Here's how to recover from each mistake." | **"git revert vs git reset? When to rebase? How do you recover a deleted commit?"** |
| **Sun** | **MOCK 5** | **Ansible + Linux + Terraform + Git → RECORD + CRITIQUE** | | |
| | | **Gate Check:** Can you articulate the Terraform vs Ansible difference, demonstrate 5 Linux commands, explain git revert vs reset? These are LOW-HANGING-FRUIT interview questions. Must be perfect. | | |

---

## WEEK 6: LogicMonitor (Your Superpower) + Integration Week

**Theme:** You already use LogicMonitor daily. Turn that into interview gold. Connect ALL tools into one story.

**Learning Progression:**
- Days 36-37: **KNOWN** (LogicMonitor — you use it daily) → Quick reframe, interview articulation, STAR stories
- Days 38-41: **INTEGRATION** (connecting everything you've learned) → No new tools, just connecting dots

| Day | LEARN (30m) | BUILD (30m) | PRODUCTION STORY (30m) | INTERVIEW DRILL (30m) |
|-----|------------|------------|----------------------|---------------------|
| 36 | **KNOWN:** LogicMonitor interview reframe
Quick reframe → How to talk about LM → What interviewers care about | Write 3 versions of your LM story (30s / 60s / 120s) | **YOUR REAL STORIES:** Alerts you resolved, dashboards you built, incidents you handled. No fake stories needed. | **"Tell me about your experience with LogicMonitor. What do you monitor? How do you respond to alerts?"** |
| 37 | **KNOWN:** LogicMonitor + Azure Monitor
Where LM fits vs Azure Monitor → Integration story | 15 LM interview questions with STAR answers | **YOUR REAL INCIDENT:** "I detected [X] via LM, root caused to [Y], fixed with [Z], saved [impact]." | **"Describe a complex incident you resolved using LogicMonitor." (STAR format)** |
| 38 | **INTEGRATION:** Full pipeline from memory
No new learning → Can you connect all 12 tools? | Re-create complete pipeline: GitHub → CI/CD → Terraform → VM → Docker → Ansible → LM | All 12 tools working together as ONE system. | **"Walk me through your complete infrastructure pipeline from code commit to production monitoring."** (10 min version) |
| 39 | **INTEGRATION:** Wipro → product company
Reframe your experience → Interview storytelling | "Tell me about yourself" (DevOps version, 60 sec) + 5 common answers | "At Wipro, I manage [X] VMs, use [tools], handle [scale]. I want to move to product companies for deeper impact." | **"Tell me about yourself." (record, critique, redo until smooth) + "Why leaving Wipro?"** |
| 40 | **INTEGRATION:** STAR stories
No new tools → Your real stories framed for DevOps | Write 5 stories (STAR format): Complex problem, Failure, Conflict, Above-beyond, Leadership | Your REAL Wipro experiences. Reframe for DevOps interviews. | Practice each story out loud (2 min each). Record. Are you confident? Natural? Quantified? |
| 41 | **INTEGRATION:** Target company research
No new tools → Know your targets | Per company: what they do, tech stack, recent news, JD keywords | "At Razorpay, they use Terraform heavily. Their blog talks about multi-region Azure deployment." | **"Why do you want to work at [Company]?" (specific, researched answer per company)** |
| **Sun** | **MOCK 6** | **FULL MOCK: All tools + behavioral + "Why [Company]?" → RECORD + CRITIQUE** | | |
| | | **Gate Check:** Can you walk through the entire pipeline without pausing? Are your LM stories natural and confident? Can you answer "Why [Company]?" specifically? This is the FINAL practice gate before applications start next week. | | |

---

## WEEK 7: Rapid Fire + Resume + Salary Strategy

**Theme:** Build speed and confidence across all topics. Prepare the logistics.

**Learning Progression:**
- Days 43-44: **INTEGRATION** (Resume, salary — no new tools)
- Days 45-48: **RAPID FIRE** (All tools — measuring what you know, not learning new)

**Key difference this week:** The LEARN block is for building SPEED, not depth. The DRILL block is the MAIN event (180 questions total).

| Day | LEARN (30m) | BUILD (30m) | PRODUCTION STORY (30m) | INTERVIEW DRILL (30m) |
|-----|------------|------------|----------------------|---------------------|
| 43 | **INTEGRATION:** Resume tailoring
No new tools → How to present what you've learned → Keywords | 3 versions: product focus / general DevOps / monitoring-heavy | "Your resume gets 6 seconds. Keywords must match the JD. Quantify everything." | **"Walk me through your resume." (2 min version, confident, flowing)** |
| 44 | **INTEGRATION:** Salary strategy
No new tools → Market positioning → Negotiation tactics | Script for: current CTC / expected CTC / why 14 LPA / negotiation tactics | "Market research: 3 YOE DevOps with Terraform + Azure = 8-12 LPA. With your specific skillset = 14 LPA." | **"What's your current CTC? Expected CTC? Why should we pay you 14 LPA?"** (Practice until it sounds natural, not rehearsed) |
| 45 | **RAPID FIRE:** Terraform (60 Q&A)
No new learning → How fast can you answer? | Mark weak spots. Drill until no hesitation. | Mix of conceptual, scenario, compare, fix-it questions | Rapid fire format: question → answer in 30 seconds. Repeat weak ones. |
| 46 | **RAPID FIRE:** Azure (50 Q&A)
No new learning → How fast can you answer? | Mark weak spots. Focus on WHY answers. | Terraform + Azure cross-questions | Rapid fire format: networking, compute, storage, security, monitoring, governance |
| 47 | **RAPID FIRE:** CI/CD + Docker + Git (40 Q&A)
No new learning → Cross-tool questions | Mark weak spots. Cross-tool questions. | "How do Terraform + GitHub Actions + Docker work together in your pipeline?" | Rapid fire format: workflows, images, branching, deployment strategies |
| 48 | **RAPID FIRE:** Ansible + Linux + LM (30 Q&A)
No new learning → STAR stories under pressure | Mark weak spots. STAR story practice. | Your 5 STAR stories told smoothly, with confidence, quantified. | Rapid fire: Ansible, Linux commands, bash, LM, behavioral |
| **Sun** | **MOCK 7** | **Full mock: 45 min tech + 15 min behavioral. No notes allowed. → RECORD + CRITIQUE** | | |
| | | **Gate Check:** Can you answer 180 questions at 30 sec each? Can you say your salary justification without stumbling? Compare with Mock 1 recording — you should see a COMPLETELY different person. | | |

---

## WEEK 8: Final Mock + Applications + Buffer

**Theme:** Execute. Apply. Interview. Win.

**Learning Progression:**
- Day 50: **FINAL VERIFICATION** — This is the gate for everything. If Mock 8 isn't good, delay applications by 1 week.
- Days 51-56: **EXECUTION** — No more learning. Just applying what you've built.
- Days 57-60: **LIVE INTERVIEWS** — Real calls. Real feedback. Real improvement.

| Day | FOCUS | GATE CHECK | ACTION |
|-----|-------|-----------|--------|
| 50 | **FINAL MOCK 8** | **GATE:** If you hesitate on >3 questions, delay applications 1 week. Re-do weak days. | Full 1 hour mock. No notes. Timed. Record. Compare with Week 1 recording — see how far you've come. |
| 51 | **APPLY TIER 1** | Must pass Mock 8 gate first | 3 applications: Freshworks + Razorpay + BrowserStack. Tailored resume per company. AI-generated cover letter via AUTOMATION_HUB. Log all in applications.csv. |
| 52 | **SCREENING PREP** | Can you answer screening Qs without notes? | Recruiter screening: 30 sec intro, current role, why leaving, expected CTC, notice period. Record and practice each answer. |
| 53 | **APPLY TIER 2** | Applications must be submitted, not drafted | 3 applications: Postman + Atlassian India + Chargebee. Tailored. Logged. Tracked. |
| 54 | **WHITEBOARD DRILL** | Can you draw + explain without pausing? | Draw to camera: VNet for 3-tier app / CI/CD pipeline / Terraform state workflow / Container deployment strategy. Explain as you draw. |
| 55 | **APPLY TIER 3 + FOLLOW-UPS** | All applications sent? Follow-ups done? | 2 more applications. Check email_log.csv — follow up on any responses from Week 8 applications. |
| 56 | **CONFIDENCE DAY** | Weak spots reviewed? Salary answer ready? | Scan all rapid fire weak spots. Rehearse salary negotiation. Review STAR stories. Mental prep: "I am a 14 LPA DevOps engineer." |
| **57-60** | **BUFFER** | **Live interviews — this is where you prove it.** | As interview calls come in, use Teacher agent for focused prep on weak areas. Each interview makes you better. |

---

## TOTAL INVESTMENT

```
Week 1: Foundation + First Deploy   ─── 14h ─── ⬛⬛⬛⬛⬛⬛⬛
Week 2: Terraform Deep + Compute    ─── 14h ─── ⬛⬛⬛⬛⬛⬛⬛
Week 3: CI/CD + Docker              ─── 14h ─── ⬛⬛⬛⬛⬛⬛⬛
Week 4: Security + State Ops        ─── 14h ─── ⬛⬛⬛⬛⬛⬛⬛
Week 5: Ansible + Linux + Git       ─── 14h ─── ⬛⬛⬛⬛⬛⬛⬛
Week 6: LM + Integration            ─── 14h ─── ⬛⬛⬛⬛⬛⬛⬛
Week 7: Rapid Fire + Resume + Salary─── 14h ─── ⬛⬛⬛⬛⬛⬛⬛
Week 8: Final Mock + Apply          ─── 14h ─── ⬛⬛⬛⬛⬛⬛⬛
                                    ─────────
    TOTAL:                           112 hours

    2h/day + 2h Sunday = 14h/week × 8 weeks = 112h total
```

---

## Beast Mode vs Previous Plan

```
METRIC              OLD PLAN (94h)         BEAST MODE (112h)
──────────────────  ───────────────────    ──────────────────────
Interview drills    0 (until Day 39)       56 sessions (every day)
Mock interviews     3 (at very end)        8 recorded + critiqued
Production stories  Not enforced           56 built-in stories
Portfolio project   None                   Full GitHub repo
Cross-tool          Siloed phases          Daily integrated practice
Salary prep         Not included           Full negotiation module
STAR stories        1 session              5 stories + weekly practice
Resume tailoring    1 session              Multi-version per company
Whiteboard prep     None                   1 full day
Rapid fire drills   None (quiz days)       4 days (180 Q&A)
```

---

## How To Study Each Day

```
1. Select "Teacher" from the agent list
2. Say the day number: "Start Day 1" / "Start Day 8" / etc.
3. Teacher:
   a. Reads today's lesson from DAILY_PLAN.md
   b. Teaches the LEARN concept (interview-focused, production-aware)
   c. Guides you through BUILD step on your project
   d. Tells the PRODUCTION STORY and discusses WHY it matters
   e. Runs INTERVIEW DRILL (asks question, waits for answer, gives feedback)
   f. Updates .teacher-context.json with progress + confidence score
4. On Sunday: Teacher runs full mock interview, records weak spots
```

**Rule:** No zero days. Even 30 minutes of review counts.
**Rule:** Record yourself during drills. Hearing yourself is the fastest way to improve.
**Rule:** By Mock 5 (Week 6), you should be able to answer any question without pausing.
**Rule:** By Mock 8 (Week 8), you should sound like you've been doing this for years.

---

## Quick Reference

```
WANT TO...                          SAY TO TEACHER
─────────────────────────            ──────────────────────────
Start from Day 1                    "Start Day 1"
Continue today's lesson             "Continue my lesson"
Review past topic                   "Review [topic name]"
Practice specific Q                 "Drill me on Terraform state"
Sunday mock                         "Run the week 1 mock"
Track my progress                   "How am I doing?"
Know what I'm weak at               "What are my weak spots?"
Prepare for upcoming interview      "I have an interview at [Company]"
```

# Beast Mode: Workflow Tree

```
                          ┌───────────────────────────────────────────────────┐
                          │    TARGET: 7-14 LPA DevOps Engineer              │
                          │    Current: 3 YOE, ~3 LPA @ Wipro                │
                          │    Plan: 8 weeks × 14h/week = 112h total         │
                          │    Select "Teacher" from agent list               │
                           │    Portfolio: github.com/som-d/AzureVM/panther/     │
                          └───────────────────────┬───────────────────────────┘
                                                  │
        ┌──────────────────────┬──────────────────┼──────────────────┬──────────────────────┐
        │                      │                  │                  │                      │
        ▼                      ▼                  ▼                  ▼                      ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│   WEEKS 1-2   │    │   WEEKS 3-4   │    │   WEEKS 5-6   │    │   WEEK 7     │    │   WEEK 8     │
│   BUILD CORE  │    │   AUTOMATE    │    │   INTEGRATE   │    │   POLISH     │    │   EXECUTE     │
│               │    │               │    │               │    │               │    │               │
│ Terraform     │    │ CI/CD full    │    │ Ansible+TF    │    │ Resume       │    │ FINAL MOCK   │
│ State → HCL   │    │ GitHub Actions│    │ Linux bash    │    │ Salary strat │    │ Apply Tier 1 │
│ VNet → NSG    │    │ Docker+ACR    │    │ Git advanced  │    │ Rapid fire   │    │ Screening    │
│ Remote state  │    │ Security      │    │ LM stories    │    │ 180 Q&A      │    │ Apply Tier 2 │
│ Git workflow  │    │ State surgery │    │ STAR stories  │    │ Weak spots   │    │ Whiteboard   │
│ Modules       │    │ Deploy strat  │    │ Company res.  │    │              │    │ Apply Tier 3 │
│ VMSS+LB       │    │ Monitor+cost  │    │               │    │              │    │ Buffer       │
│ Workspaces    │    │               │    │               │    │              │    │              │
└───────┬───────┘    └───────┬───────┘    └───────┬───────┘    └───────┬───────┘    └───────┬───────┘
        │                    │                    │                    │                    │
        ▼                    ▼                    ▼                    ▼                    ▼
   ┌─────────┐         ┌─────────┐          ┌─────────┐          ┌─────────┐          ┌─────────┐
   │ MOCK 1  │         │ MOCK 3  │          │ MOCK 5  │          │ MOCK 7  │          │ MOCK 8  │
   │ MOCK 2  │         │ MOCK 4  │          │ MOCK 6  │          │         │          │  APPLY  │
   └─────────┘         └─────────┘          └─────────┘          └─────────┘          └─────────┘
```

## The Pipeline You Build

```
                          GITHUB ACTIONS CI/CD PIPELINE
                          ┌──────────────────────────────────────┐
                          │                                      │
    git push ──────────►  │  PR → terraform plan + comment       │
    (feature)             │  Merge → terraform apply + approve   │
                          │      → docker build → push to ACR    │
                          │      → ansible configure             │
                          │      → deploy to Azure               │
                          └──────────────────┬───────────────────┘
                                             │
                                             ▼
                                     ┌───────────────┐
                                     │    AZURE       │
                                     │  ┌─────────┐  │
                                     │  │ VNet    │  │
                                     │  │ Subnets │  │
                                     │  │ NSG     │  │
                                     │  │ VMSS    │  │
                                     │  │ LB      │  │
                                     │  │ KV      │  │
                                     │  │ Storage │  │
                                     │  └─────────┘  │
                                     └───────┬───────┘
                                             │
                                             ▼
                                    ┌────────────────┐
                                    │   LOGICMONITOR  │
                                    │   Monitoring    │
                                    │   + Alerts      │
                                    └────────────────┘
```

---

## Drift Prevention: Progress Dashboard

### Weekly Gate Status

```
PHASE       DAYS COMPLETE   GATE PASSED?  CONFIDENCE  NEXT ACTION
───────     ─────────────   ────────────  ──────────  ───────────────────────────────
Pre-Req     ✅✅✅⬜⬜⬜    ✅ Yes        ★★★★☆    Phase 1 Steps 1-3 done
(repo+git)                                                                          
Wk 1         ⬜⬜⬜⬜⬜⬜    ❌ Not yet    ★★★★★    Start Terraform Day 1
Wk 2         ⬜⬜⬜⬜⬜⬜    ❌ Not yet    ★★★★★    --
Wk 3         ⬜⬜⬜⬜⬜⬜    ❌ Not yet    ★★★★★    --
Wk 4         ⬜⬜⬜⬜⬜⬜    ❌ Not yet    ★★★★★    --
Wk 5         ⬜⬜⬜⬜⬜⬜    ❌ Not yet    ★★★★★    --
Wk 6         ⬜⬜⬜⬜⬜⬜    ❌ Not yet    ★★★★★    --
Wk 7         ⬜⬜⬜⬜⬜⬜    ❌ Not yet    ★★★★★    --
Wk 8         ⬜⬜⬜⬜⬜⬜    ❌ Not yet    ★★★★★    --
```

### Daily Confidence Tracker

```
DAY  TOPIC                               CONFIDENCE  GATE  READY FOR NEXT?
───  ───────────────────────────────────  ──────────  ────  ──────────────────────────────
P1   Phase 1: Git+Terminal Foundations   ★★★★☆       ✅   Yes → Start Week 1
     (pwd, ls, mkdir, nano, scripts,
      git init, commit, push, reset,
      --orphan, --force, push protection,
      nested repo cleanup, .gitignore)
────────────────────────────────────────────────────────────────────────────────────────
1    Terraform State + HCL               ★☆☆☆☆       ❌   Next up!
2    Azure VNet + Subnets + CIDR         ★☆☆☆☆       ❌   --
3    Variables + Outputs + Locals        ★☆☆☆☆       ❌   --
4    Azure NSG + Security                ★☆☆☆☆       ❌   --
5    Remote State + Locking              ★☆☆☆☆       ❌   --
6    Git Branching + PR Workflow         ★☆☆☆☆       ❌   --
```

### How Gates Work

```
EACH DAY:  Drill confidence ≥ 3/5 → move to next day
           Drill confidence < 3/5 → repeat day before new content

EACH WEEK: Sunday mock ≥ 8/10 → move to next week
           Sunday mock < 8/10 → identify weak days → re-do Mon-Tue → re-test Wed

BIG GATES:
           Mock 3 (Week 3) → Pipeline must be smooth. Most important gate.
           Mock 8 (Week 8) → Final check. If not ready → delay applications.
```

### If You Get Lost (Emergency Recovery)

```
SCENARIO                      FIX
─────────                     ───────────────────────────────────────
Missed 1-2 days               Catch up on weekend (30 min per day)
Missed 3-5 days               Teacher does compressed review
Missed 1+ week                Reset to last passed gate, restart from there
Stuck on 1 topic (confidence  Teacher reteaches with different approach. More
consistently < 3/5)           analogies. Break concept into smaller pieces.
Feeling overwhelmed           Take 1 day off. Then re-do last passed day.
                              Confidence > speed. A beast has solid foundations.
```

---

## Mock Interview Progression

```
MOCK 0    Pre-Req ─── Git+Terminal foundations set         ✅⬜⬜⬜⬜⬜⬜⬜
MOCK 1    Week 1  ─── Rough, hesitant, "ums" and pauses    ⬜
MOCK 2    Week 2  ─── Better structure, still searching    ⬜⬜
MOCK 3    Week 3  ─── Pipeline walkthrough getting smooth  ⬜⬜⬜
MOCK 4    Week 4  ─── Security mindset showing             ⬜⬜⬜⬜
MOCK 5    Week 5  ─── Full stack integration flowing       ⬜⬜⬜⬜⬜
MOCK 6    Week 6  ─── Production stories are compelling    ⬜⬜⬜⬜⬜⬜
MOCK 7    Week 7  ─── Rapid fire — no hesitation           ⬜⬜⬜⬜⬜⬜⬜
MOCK 8    Week 8  ─── Interview ready. Confident. Smooth.  ⬜⬜⬜⬜⬜⬜⬜⬜
```

## ROI-Based Priority (7-14 LPA Level)

```
RANK  TOOL GROUP              JD%    WEEKS        WHY THIS DEPTH
────  ─────────────────────── ───    ───────────  ─────────────────────────────
 1    Terraform                90%   1-2,4,7      Deep: state, modules, import, CI/CD, lifecycle, workspaces
 2    Git                      90%   1,5,7        Branching, merge/rebase, PR workflow, recovery
 3    CI/CD (GH Actions)       85%   3,4,7        Full pipeline: plan, apply, approve, OIDC
 4    Azure (Network, Compute) 80%   1-2,4,7      VNet, NSG, VMSS, LB, App Gateway, IAM, KV, Storage
 5    Docker                   70%   3,7          Dockerfile, multi-stage, compose, ACR, CI/CD integration
 6    Ansible                  70%   5,7          Playbooks, roles, vault, dynamic inventory, TF integration
 7    LogicMonitor             70%*  6,7          Story reframe, STAR incidents, interview articulation
 8    Linux + Bash             60%   5,7          30 commands, health check script, troubleshooting
 9    Azure DevOps Pipelines   60%   3,7          YAML pipelines, service connections, variable groups
10    Monitoring (Azure)       50%   4,7          Log Analytics, metric alerts, action groups, diagnostic
11    Azure Cost + Governance  40%   4            Tags, budgets, policies, reservations (1 day only)
12    K8s                      CUT   35%          Not needed at 7-14 LPA level
```

## Quick Decision Flow

```
START HERE
    │
    ▼
What's today?
    │
    ├── Mon-Sat 6 PM? ──► Daily 4-block session (2h)
    │                      └── LEARN → BUILD → PRODUCE → DRILL
    │
    ├── Sunday?         ──► Mock Interview (2h)
    │                      └── Record → Self-critique → Re-do weak answers
    │
    └── Morning?        ──► Light review (30 min)
                           └── Review yesterday's drill answers
                                Read weak spots from last session

AFTER EACH SESSION:
    └── Teacher updates .teacher-context.json
         └── Confidence score
         └── Weak areas logged
         └── Next session's focus areas
```

## Key Milestones

```
PRE-REQ DONE:  Git+Terminal foundations ✅ — 20+ commands, git reset/amend/orphan/force,
               push protection, nested repo cleanup, .gitignore, health-check script
END OF WEEK 2:  Can deploy a complete 3-tier Azure infra with Terraform from scratch
END OF WEEK 4:  Full CI/CD pipeline working. Docker + Terraform + Security integrated.
END OF WEEK 6:  All 12 tools integrated into one pipeline. LM stories polished.
END OF WEEK 7:  Rapid fire — 180 questions, zero hesitation. Resume + salary ready.
END OF WEEK 8:  3+ applications sent. Interview ready. Confident. Hired.
```

---

> **The difference between "covered" and "beast":**
> Covered = "Terraform has a state file that stores resource mappings."
> Beast = "I built a complete infrastructure pipeline. Here's the GitHub repo. Let me walk you through every layer — Terraform modules for reusable Azure infrastructure, CI/CD with GitHub Actions that plans on PR and applies on merge, Docker multi-stage builds pushed to ACR, Ansible for post-deploy configuration, and LogicMonitor for observability. I also learned the hard way — like the time someone deleted the state file and I had to recover it."

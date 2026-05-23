# Session Memory — Complete Context Dump

> **Purpose:** Portable memory file. Share this + `.teacher-context.json` with the AI when starting a new chat on a new VM to continue exactly where we left off.
> **Last updated:** May 23, 2026
> **To restore context on new VM:** Send both `SESSION_MEMORY.md` + `.teacher-context.json` to the AI. These two files contain everything needed to continue.

---

## 1. STUDENT PROFILE

| Field | Value |
|-------|-------|
| Name | Soham Deshmukh |
| Current Role | DevOps Engineer at Wipro |
| Experience | 3 years |
| Current CTC | ~3 LPA |
| Target CTC | 7-14 LPA (2.5-4.5x jump) |
| Long-term Target | AI Infrastructure / GPU Platform Engineer (25-40+ LPA, 5-10 year horizon) |
| Phase 1 Strategy | DevOps skills → Indian product companies (Freshworks, Razorpay, Postman, BrowserStack, Atlassian India, Chargebee) |
| Phase 2 Pivot | After 1-2 years at product company → AI Infrastructure / GPU Platform Engineering (NOT MLOps) |
| Known Tools | Ansible (daily), Azure (basic), Linux (basic), Git (basic), LogicMonitor (daily) |
| Brand New Tools | Terraform, Docker, GitHub Actions, CI/CD pipelines |
| Actual Repo | github.com/som-d/AzureVM (folder: `panther/`) |

---

## 2. INFRASTRUCTURE SETUP

### Primary Workspace
| Component | Detail |
|-----------|--------|
| **VM Provider** | AWS EC2 (t3.small) |
| **Region** | Mumbai (ap-south-1) |
| **OS** | Ubuntu 26.04 LTS "resolute" |
| **Storage** | 20 GB EBS (expanded from 8 GB → 20 GB, 12 GB free ✅) |
| **Access** | VS Code Remote SSH from Mac M1 |
| **Key Pair** | `spidy-key.pem` (located on Mac at `~/.ssh/spidy-key.pem`) |
| **User** | `ubuntu` |

### Tools Installed on VM
| Tool | Version | Status |
|------|---------|--------|
| Terraform | v1.15.4 | ✅ Installed |
| Azure CLI | 2.86.0 | ✅ Installed (via Noble repo workaround for Resolute) |
| Git | 2.53.0 | ✅ Installed |
| Ansible | Removed (was installed via PPA, removed for disk space, will reinstall properly later) |

### Repo Structure
```
/home/ubuntu/AzureVM/panther/
├── .gitignore
├── ansible/
├── index.html
├── notes.txt
└── terraform/
```

### Other Accounts
| Account | Credits | Purpose |
|---------|---------|---------|
| Azure for Students | $100 (365 days remaining) | Deploy resources via Terraform |
| AWS Free | ~100 days remaining | VM hosting (t3.small) |
| Oracle Cloud Free Tier | N/A | Considered but unreliable (accounts get banned, ARM capacity always out of stock) |

---

## 3. LEARNING APPROACH

### Core Principles (Not Negotiable)
1. **Integrated Learning:** Linux, Git, Terraform, Azure taught simultaneously — every command teaches Linux as a byproduct
2. **CLI-Only:** No UI, no desktop. Everything through VS Code terminal (SSH to VM)
3. **Command-first teaching:** Every command comes with explanation of flags, pipes, operators, and output interpretation
4. **Production stories required:** User has ZERO production experience with Terraform, Docker, CI/CD — every topic needs a real company incident story
5. **Interview drill every session:** Answer out loud, get feedback, re-answer
6. **Beast Mode 8-week plan:** 4-block daily formula (LEARN → BUILD → PRODUCE → DRILL)

### Beast Mode Plan Structure (112 hours)
- 2h/day Mon-Sat + 2h Sunday mock = 14h/week × 8 weeks
- Week 1-2: Terraform + Azure fundamentals
- Week 3: CI/CD + Docker
- Week 4: Security + Deploy strategies
- Week 5: Ansible + Linux + Git advanced
- Week 6: LogicMonitor reframe + Wipro stories
- Week 7: Rapid fire + Resume + Salary strategy
- Week 8: Final mock + Applications

### Topic Newness Map
| BRAND NEW (5-step LEARN) | SOME EXPOSURE (hybrid) | KNOWN (compressed) |
|---------------------------|----------------------|-------------------|
| Terraform | Azure (basic VMs) | Ansible |
| Docker | Linux (basic cmds) | LogicMonitor |
| GitHub Actions | Git (add/commit/push) | |
| Azure DevOps | | |
| CI/CD patterns | | |
| Bash scripting | | |

### Excluded Topics (Low ROI for 7-14 LPA)
- Kubernetes / AKS (35% of JDs but asked at senior level)
- Prometheus / Grafana (user uses LogicMonitor)
- Jenkins deep dive (mention conceptually only)
- Helm charts, Service mesh, DevSecOps (senior topics)
- System design (30% of JDs, asked at 15+ LPA level)

---

## 4. COMPLIANCE & ACCESS CONSTRAINTS

| Constraint | Detail |
|------------|--------|
| **Office laptop** | Mac M1, Zscaler monitors all traffic |
| **Software on Mac** | Cannot install anything. Only browser + VS Code (already SSH'd) |
| **Previous flag** | Got compliance email for accessing `private-ip:port` in browser — DO NOT repeat |
| **Safe pattern** | SSH to AWS VM (port 22) only — looks like normal DevOps work |
| **NOT safe** | Direct VNC/RDP to VM IP on non-standard ports, accessing private IPs via browser |
| **Alternative access method** | Chrome Remote Desktop (looks like HTTPS to Google) is safest if desktop needed |
| **Home laptop** | Windows Home (16 GB RAM, 500 GB SSD) — no RDP server built-in |
| **Home laptop access** | RDP Wrapper was attempted but failed ("Not Listening"), VNC considered but abandoned due to compliance risk |

**Decision:** Continue with CLI-only learning on AWS VM via VS Code Remote SSH. No desktop needed.

---

## 5. CURRENT PROGRESS (Exact State)

### Where We Are Right Now
| Item | Status |
|------|--------|
| Phase 1: Terminal + Git CLI Foundations | **In progress — Step 1 of 6** |
| Step 1: What just learned `pwd` | ✅ Done — understands Print Working Directory |
| Step 1: Next command to run | `ls -la` |
| Step 2: Create project structure | ⏳ Not started |
| Step 3: Git init + first commit | ⏳ Not started |
| Step 4: Git remote add (linking to GitHub) | ⏳ Not started |
| Step 5: Symlinks + .gitignore + undo | ⏳ Not started |
| Step 6: git log + git diff + git branch | ⏳ Not started |
| Phase 2: Terraform Day 1 | ⏳ Not started |

### What Was Covered in Session So Far

#### Infrastructure Setup (ALL DONE ✅)
1. Azure CLI installed via Noble repo workaround (Ubuntu 26.04 "resolute" not officially supported)
2. Disk full (6.7 GB) → cleaned apt cache + removed Ansible packages + expanded EBS to 20 GB
3. Commands: `growpart /dev/nvme0n1 1` (expand partition), `resize2fs /dev/root` (expand filesystem)
4. `df -h` (disk free human-readable), `lsblk` (list block devices)
5. Azure CLI 2.86.0 installed, Terraform v1.15.4, Git 2.53.0 — all confirmed

#### Phase 1 Step 1: pwd + ls -la (IN PROGRESS)
| Topic | Status | Details Learned |
|-------|--------|----------------|
| `pwd` | ✅ Done | Print Working Directory — shows current location in filesystem |
| `ls -la` | ⏳ To be run | Will learn: permissions (drwxr-xr-x), hidden files, file types, ownership |
| `.` vs `..` | ⏳ Pending | Current directory vs parent directory |
| File permissions | ⏳ Pending | rwx, user/group/others, first char = type (d, -, l) |

#### Troubleshooting Commands Learned (during setup)
| Command | What It Does | When Used |
|---------|-------------|-----------|
| `df -h` | Disk free, human-readable | Check disk space |
| `lsblk` | List block devices | Check partition layout |
| `du -sh` | Disk usage, summary, human-readable | Find what's eating space |
| `sort -rh` | Sort by human-readable size descending | Find biggest files |
| `head -10` | First 10 lines of output | See top results |
| `grep` | Search text in output | Filter command output |
| `journalctl --disk-usage` | Check system log size | Find disk space used by logs |

---

## 6. KEY DECISIONS MADE

| # | Decision | Rationale | When |
|---|----------|-----------|------|
| 1 | **CLI-only learning** | No UI needed, user is learning CLI anyway, compliance safe | Today |
| 2 | **VS Code Remote SSH as primary interface** | Works through Zscaler (SSH only), no software install on Mac | Today |
| 3 | **No desktop/RDP/VNC** | Compliance risk, not needed for CLI learning | Today |
| 4 | **Don't fight Windows Home RDP** | RDP Wrapper failed, not worth the effort | Today |
| 5 | **No Oracle Cloud** | Account ban risk, unreliable ARM capacity | Today |
| 6 | **Integrated Linux+Git+Terraform+Azure** | Every command teaches multiple things simultaneously | Today |
| 7 | **Command-first teaching with flag explanations** | User wants to understand every flag, pipe, and operator | Today |
| 8 | **Portfolio repo: github.com/som-d/AzureVM/panther/** | Actual path, updated from incorrect `soham-devops/infrastructure-pipeline` | Today |
| 9 | **Teacher agent mode: primary** | Shows in agent list, not hidden as subagent | Earlier |
| 10 | **Beast Mode 8-week plan** | Adopted over original 94h sequential plan | Earlier |
| 11 | **Indian product companies first** | More realistic at 3 YOE, build brand-name for later Europe move | Earlier |
| 12 | **AI Infrastructure / GPU Platform Engineer** | Long-term target (not MLOps), infra layer more durable | Earlier |

---

## 7. FILE LOCATIONS (for reference)

| File | Path | Purpose |
|------|------|---------|
| Memory dump | `D:\Resume\interview-prep\SESSION_MEMORY.md` | This file — portable context |
| Teacher context | `D:\Resume\interview-prep\.teacher-context.json` | Schema v2.0, 8-week curriculum |
| Daily plan | `D:\Resume\interview-prep\DAILY_PLAN.md` | Beast Mode 8-week schedule |
| Workflow tree | `D:\Resume\interview-prep\WORKFLOW_TREE.md` | Beast mode workflow + milestones |
| Master roadmap | `D:\Resume\interview-prep\master-roadmap.md` | Full 8-week project-based structure |
| Teacher agent | `D:\Resume\.opencode\agents\teacher.md` | Agent definition (mode: primary) |
| Teacher skill | `D:\Resume\.opencode\skills\teacher\SKILL.md` | Teaching protocol + production stories |
| Original resume PDF | `D:\Resume\Soham_D_Resume_Ansible.pdf` | Source of truth for skills |
| Automation hub | `D:\Resume\AUTOMATION_HUB\` | Job application automation (CLI tool) |

---

## 8. NEXT STEPS

### Immediate (this session)
```
Phase 1 Step 1: Run `ls -la` → learn to read permissions, file types, hidden files
Phase 1 Step 2: mkdir -p, touch, echo, cat, nano
Phase 1 Step 3: git init, add, commit
Phase 1 Step 4: git remote add, push
Phase 1 Step 5: .gitignore, symlinks, undo commands
Phase 1 Step 6: git log, diff, branch
Phase 2: Terraform Day 1 (HCL + deploy Azure RG)
```

### Before Next Session
- Copy `D:\Resume\interview-prep\` folder to new VM
- Share `SESSION_MEMORY.md` with AI in new chat to restore context
- Ensure SSH key + VS Code Remote SSH set up on new VM

---

*End of memory dump. Everything needed to restore full context on a new machine.*

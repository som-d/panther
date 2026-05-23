# Session Memory — Complete Context Dump

> **Purpose:** Portable memory file. Share this + `.teacher-context.json` with the AI when starting a new chat on a new VM to continue exactly where we left off.
> **Last updated:** May 23, 2026 (after Day 1 — Session 2)
> **To restore context on new VM:** Send both `SESSION_MEMORY.md` + `.teacher-context.json` to the AI.

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
| Portfolio Repo | github.com/som-d/AzureVM (subfolder: `panther/`) |

---

## 2. INFRASTRUCTURE SETUP

### Primary Workspace
| Component | Detail |
|-----------|--------|
| **VM Provider** | AWS EC2 (t3.small) |
| **Region** | Mumbai (ap-south-1) |
| **OS** | Ubuntu 26.04 LTS "resolute" |
| **Storage** | 20 GB EBS (12 GB free) |
| **Access** | VS Code Remote SSH from Mac M1 |
| **Key Pair** | `spidy-key.pem` (on Mac at `~/.ssh/spidy-key.pem`) |
| **User** | `ubuntu` |

### Tools Installed on VM
| Tool | Version | Status |
|------|---------|--------|
| Terraform | v1.15.4 | ✅ Installed |
| Azure CLI | 2.86.0 | ✅ Installed |
| Git | 2.53.0 | ✅ Installed |
| Ansible | Removed (was installed via PPA, removed for disk space, will reinstall later) |

### Repo Structure at `panther/`
```
/home/ubuntu/AzureVM/panther/
├── AI/                          # Teaching agent config + automation hub
│   ├── AUTOMATION_HUB/
│   ├── data/
│   ├── infrastructure-pipeline/ # (separate git repo — was nested, now properly ignored)
│   ├── linkedin/
│   ├── MASTER_PLAN.md
│   ├── outreach/
│   ├── README.md
│   ├── reports/
│   └── resumes/
├── ansible/                     # (empty — future use)
├── docker/                      # (empty — future use)
├── interview-prep/              # ← THIS FILE, .teacher-context.json + topic study files
│   ├── .teacher-context.json
│   ├── SESSION_MEMORY.md        # ← you are here
│   ├── DAILY_PLAN.md
│   ├── WORKFLOW_TREE.md
│   ├── master-roadmap.md
│   ├── day1_notes.md
│   ├── terraform/
│   ├── azure/
│   ├── ansible/
│   ├── git/
│   ├── github-actions/
│   ├── azure-devops/
│   ├── cicd/
│   ├── docker-k8s/
│   ├── linux-scripting/
│   └── logicmonitor/
├── scripts/
│   └── health-check.sh          # Working bash script (uptime, memory, disk)
├── terraform/
│   ├── main.tf                  # Azure Resource Group (starting point)
│   ├── modules/                 # (empty — future use)
│   ├── environments/            # (empty — future use)
│   ├── backend.tf               # (empty — future use)
│   └── variables.tf             # (empty — future use)
├── .github/
│   └── workflows/               # (empty — future use)
├── .gitignore
├── README.md
└── index.html
```

### AzureVM Root Repo Structure
```
/home/ubuntu/AzureVM/
├── .gitignore                   # Has panther/ + infrastructure-pipeline/ entries
├── panther/                     # ← main portfolio repo (has own .git)
└── .opencode/                   # OpenCode config
```

### Other Accounts
| Account | Credits | Purpose |
|---------|---------|---------|
| Azure for Students | $100 (365 days remaining) | Deploy resources via Terraform |
| AWS Free | ~100 days remaining | VM hosting (t3.small) |

---

## 3. LEARNING APPROACH

### Core Principles (Not Negotiable)
1. **Integrated Learning:** Linux, Git, Terraform, Azure taught simultaneously
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

**Decision:** Continue with CLI-only learning on AWS VM via VS Code Remote SSH. No desktop needed.

---

## 5. CURRENT PROGRESS (Exact State)

### Phase 1: Git CLI + Terminal Foundations — STATUS
| Step | Topic | Status | What Was Covered |
|------|-------|--------|------------------|
| 1 | Navigation + File Ops | ✅ **Completed** | `pwd`, `ls -la` (permissions, file types, hidden files), `mkdir -p`, `touch`, `echo > / >>`, `cat`, `nano`, `chmod +x`, `./script.sh`, `mv` |
| 2 | Git init + add + commit | ✅ **Completed** | `git init`, `git add .`, `git status`, `git commit -m`, `git log --oneline`, staging area concept |
| 3 | Git remote + push | ✅ **Completed** | `git remote add origin`, `git push -u origin master`, GitHub Push Protection (PAT blocked), `git reset --soft` to remove secret, `git commit --amend`, force push |
| 4 | Symlinks + .gitignore + undo | ⏳ **In Progress** | Did: `.gitignore` patterns, `git rm --cached` (nested repos), `git checkout --orphan`, `git branch -D`, `git push --force`. Remaining: symlinks, `git restore`, `git reset --hard`, `git commit --amend` alternatives |
| 5 | Git branch + diff + log --graph | ❌ **Not started** | |
| 6 | Git PR workflow | ❌ **Not started** | |

### What Was Covered in Session 2 (Today — May 23, 2026)

#### ✅ ALL commands learned:
```
# Linux/File Ops
pwd                              # Print Working Directory
ls -la                           # Long format + all files (permissions, owner, size, date)
ls -l                            # Long format only
ls -lah                          # Long + all + human-readable sizes
ls -R                            # Recursive (list subdirs)
mkdir -p                         # Create parent directories
touch                            # Create empty file / update timestamp
echo "text" > file               # Overwrite file
echo "text" >> file              # Append to file
cat                              # Read file contents
nano                             # Edit file interactively
chmod +x                         # Add execute permission
./script.sh                      # Run a script in current dir
mv                               # Move/rename file

# Git
git init                         # Initialize new repo
git add .                        # Stage all files
git add file                     # Stage specific file
git status                       # Check staged/unstaged/untracked
git commit -m "msg"              # Commit staged changes
git log --oneline                # Compact commit history
git log --oneline -3             # Last 3 commits
git branch -m old new            # Rename branch
git branch -D branch             # Force delete branch
git rm --cached file             # Remove from git tracking, keep file
git reset --soft HEAD~1          # Undo commit, keep changes staged
git commit --amend               # Replace last commit (with --no-edit to keep message)
git commit --amend -m "new msg"  # Replace last commit + change message
git checkout --orphan new-branch # Create branch with zero history
git remote add origin <url>      # Link to remote
git push -u origin master        # Push + set upstream
git push origin --force          # Force push (overwrite remote history)
git push origin master --force   # Force push (verbose)
```

#### 🔴 INCIDENT: GitHub Push Protection blocked a push
- A GitHub Personal Access Token was in `panther/AI/notes:2`
- GitHub detected it and blocked the push
- Solution: `git reset --soft eedd728` → `git commit -m "fix commit"` → `git push origin master --force`
- Lesson: Never commit secrets. Use `.gitignore` or environment variables.

#### 🔴 NESTED REPO CLEANUP
- `panther/` and `infrastructure-pipeline/` each had their own `.git` folders
- Root `AzureVM` repo was tracking them as regular files
- Fixed: `git rm --cached -r panther/` → added to `.gitignore` → `git commit --amend`
- Both repos now fully independent

#### 🔴 AZUREVM ROOT CLEANUP
- `AzureVM` root history had messy commits from all phases
- Fixed: `git checkout --orphan clean-main` → staged fresh → committed → `git branch -D main` → `git branch -m main` → `git push origin main --force`
- Now has 2 clean commits only

### Troubleshooting Commands Learned
| Command | What It Does | When Used |
|---------|-------------|-----------|
| `df -h` | Disk free, human-readable | Check disk space |
| `sudo growpart /dev/nvme0n1 1` | Expand partition | Increased EBS from 8GB→20GB |
| `sudo resize2fs /dev/root` | Expand filesystem | After partition expand |
| `lsblk` | List block devices | Check partition layout |
| `du -sh *` | Disk usage, summary, human-readable | Find what's eating space |
| `sort -rh` | Sort by human-readable size descending | Find biggest files |
| `head -10` | First 10 lines of output | See top results |

---

## 6. PRODUCTION STORIES COVERED

| Story | Tool | What Happened |
|-------|------|---------------|
| **Push Protection saved the team** | Git/GitHub | Engineer committed AWS keys to a public repo → GitHub blocked it. Company saved potential $50K crypto mining bill. |
| **Junior dev force-pushed to main** | Git | Engineer did `git push --force` on shared branch → lost 3 PRs of work → restore from `git reflog` took 2 hours. |
| **Force push culture at startup** | Git | Company with 100+ engineers used force push on feature branches → no issues because `main` was protected. Branch protection is the safety net. |

---

## 7. FILE LOCATIONS (Linux paths — actual VM)

| File | Path | Purpose |
|------|------|---------|
| Memory dump | `/home/ubuntu/AzureVM/panther/interview-prep/SESSION_MEMORY.md` | This file — portable context |
| Teacher context | `/home/ubuntu/AzureVM/panther/interview-prep/.teacher-context.json` | Schema v2.0, 8-week curriculum |
| Day 1 notes | `/home/ubuntu/AzureVM/panther/interview-prep/day1_notes.md` | Command reference + deep dives |
| Daily plan | `/home/ubuntu/AzureVM/panther/interview-prep/DAILY_PLAN.md` | Beast Mode 8-week schedule |
| Workflow tree | `/home/ubuntu/AzureVM/panther/interview-prep/WORKFLOW_TREE.md` | Beast mode workflow + milestones |
| Master roadmap | `/home/ubuntu/AzureVM/panther/interview-prep/master-roadmap.md` | Full 8-week project-based structure |
| AzureVM root repo | `/home/ubuntu/AzureVM/` | Root AzureVM repo (clean history) |
| Portfolio repo | `/home/ubuntu/AzureVM/panther/` | Main project repo (independent git) |
| Terraform main | `/home/ubuntu/AzureVM/panther/terraform/main.tf` | Azure RG defined (starting point) |
| Health check script | `/home/ubuntu/AzureVM/panther/scripts/health-check.sh` | Working bash script |

---

## 8. KEY DECISIONS MADE

| # | Decision | Rationale | When |
|---|----------|-----------|------|
| 1 | **CLI-only learning** | No UI needed, user is learning CLI anyway, compliance safe | Setup |
| 2 | **VS Code Remote SSH as primary interface** | Works through Zscaler (SSH only), no software install on Mac | Setup |
| 3 | **No desktop/RDP/VNC** | Compliance risk, not needed for CLI learning | Setup |
| 4 | **No Oracle Cloud** | Account ban risk, unreliable ARM capacity | Setup |
| 5 | **Integrated Linux+Git+Terraform+Azure** | Every command teaches multiple things simultaneously | Setup |
| 6 | **Command-first teaching with flag explanations** | User wants to understand every flag, pipe, and operator | Setup |
| 7 | **Portfolio repo: github.com/som-d/AzureVM/panther/** | Actual path for portfolio project | Setup |
| 8 | **Teacher agent mode: primary** | Shows in agent list, not hidden as subagent | Setup |
| 9 | **Beast Mode 8-week plan** | Adopted over original 94h sequential plan | Setup |
| 10 | **Indian product companies first** | More realistic at 3 YOE, build brand-name for later Europe move | Setup |
| 11 | **AI Infrastructure / GPU Platform Engineer** | Long-term target (not MLOps), infra layer more durable | Setup |
| 12 | **`git reset --soft` over `--hard`** | Kept all current working files intact while erasing bad commits | Today |
| 13 | **`git checkout --orphan` for root repo** | Got completely fresh history instead of cherry-picking | Today |
| 14 | **Added both nested repos to `.gitignore`** | Each is its own independent repo — should not be tracked by root | Today |
| 15 | **Force push after history rewrites only** | Safe because user works alone on both repos — no collaborators | Today |
| 16 | **Hiding `ghp_` PAT in remote URL** | PAT embedded in AzureVM root remote URL (from earlier setup). Fine for now but should switch to SSH. | Today |

---

## 9. SPACED REPETITION QUEUE

| Topic | Due Date | Interval | Confidence |
|-------|----------|----------|------------|
| `ls -la` output decoding (permissions, file types) | 2026-05-24 | 1d | N/A |
| GitHub Push Protection & secret removal | 2026-05-24 | 1d | N/A |
| `git add` vs `commit` staging area concept | 2026-05-26 | 3d | N/A |
| `git reset --soft` vs `--hard` | 2026-05-30 | 7d | N/A |

**Next review:** Tomorrow (May 24) — drill on `ls -la` output and Push Protection before new content.

---

## 10. NEXT SESSION PLAN (Day 2 — May 24, 2026)

### Doubts to Clear First
1. What exactly is HEAD? (pointer to current position)
2. `git reset --soft` vs `--hard` vs `--mixed` — what changes?
3. What does `--orphan` really mean? (branch with no parent commit)
4. What's the difference between `--force` and `--force-with-lease`?
5. Why did the root repo have two origin URLs? (PAT embedded issue)

### New Content for Day 2
```
Phase 1 Step 4 (continued): symlinks (ln -s), .gitignore deeper patterns, 
                            git restore, reset --hard, --mixed
Phase 1 Step 5: git log --graph, git diff, git branch
Phase 1 Step 6: PR workflow basics
Phase 2 (if time): Terraform Day 1 — HCL syntax + deploy Azure RG
```

### Portfolio Project — By End of Day 2
- Terraform `main.tf` with:
  - Azure Resource Group
  - Variables file with RG name + location
  - Outputs file with RG ID + name

---

*End of memory dump. Everything needed to restore full context on a new machine.*

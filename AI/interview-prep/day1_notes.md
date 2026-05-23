# Day 1 Notes — Phase 1: Linux Terminal + Git CLI Foundations
> Date: 2026-05-23 | Session: ~2h | Streak: Day 1

---

## 1. ls — The Most Important Command

| Command | What it does | Use Case |
|---------|-------------|----------|
| `ls -l` | Long format (permissions, owner, size, date) | See details |
| `ls -a` | Show ALL files including hidden (dotfiles) | Find configs |
| `ls -la` | Both combined — full detail + hidden | **Default first command on any server** |
| `ls -lah` | Same + human-readable sizes (K, M, G) | Check file sizes |
| `ls -R` | Recursive — lists everything inside subdirs | See full tree |

### Reading `ls -la` Output

```
drwxrwxr-x  6 ubuntu ubuntu 4096 May 23 11:47 .
1           2 3       4       5    6           7
```

| # | Meaning | Example |
|---|---------|---------|
| 1 | File type (`d`=dir, `-`=file, `l`=symlink) + permissions (rwx) | `d` = directory, owner can rwx, group can rwx, others can r-x |
| 2 | Link count | `6` |
| 3 | Owner | `ubuntu` |
| 4 | Group | `ubuntu` |
| 5 | Size (bytes) | `4096` for dirs |
| 6 | Last modified | `May 23 11:47` |
| 7 | Name | `.`=this dir, `..`=parent |

### Hidden Files
- Any file starting with `.` is hidden
- `ls -a` to see them: `.gitignore`, `.env`, `.git/`, `.opencode/`

---

## 2. File Operations

| Command | What it does | Key Flags |
|---------|-------------|-----------|
| `pwd` | Print Working Directory | — |
| `mkdir dir` | Make directory | `-p` = create parent dirs too |
| `touch file` | Create empty file / update timestamp | — |
| `echo "text"` | Print text | `>` = overwrite file, `>>` = append to file |
| `cat file` | Show file contents | — |
| `nano file` | Text editor | Ctrl+O = save, Ctrl+X = exit |
| `mv old new` | Move or rename | — |
| `chmod +x file` | Add execute permission | — |
| `./script.sh` | Run script from current dir | — |

### Silence = Success
Linux only prints errors. No news is good news.

---

## 3. Git Basics — The 3 Areas

```
Working Directory  ──[git add]──►  Staging Area  ──[git commit]──►  Local Repo
(your files)           (prepare)         (snapshot)
```

### Commands

| Command | What it does |
|---------|-------------|
| `git init` | Create a new git repo in current dir |
| `git add .` | Stage ALL changed files |
| `git commit -m "msg"` | Take a permanent snapshot of staging |
| `git status` | Show staged (green) vs unstaged (red) |
| `git log --oneline` | Show commit history (one line each) |
| `git branch -m newname` | Rename current branch |

### Interview Q: `git add` vs `git commit`
- `git add` = **choose** what goes in to the snapshot
- `git commit` = **take** the snapshot permanently
- Staging exists so you can craft **clean, intentional commits**

### Scenario Q
> You `git add file1.txt`, then edit it again, then `git commit`. Does the commit include the second edit?

**A:** No. `git add` snaps the content **at that moment**. Edit again = need `git add` again.

---

## 4. GitHub Remote & Push

| Command | What it does |
|---------|-------------|
| `git remote add origin URL` | Link local repo to GitHub |
| `git push origin main` | Push local commits up to GitHub |
| `git push origin main --force` | **Overwrite** remote history to match local |

### Production Story: GitHub Push Protection
- GitHub scans every push for secrets (API keys, tokens, passwords)
- If found → push is **blocked** with a red error
- Automated bots scrape public repos for secrets → spin up crypto miners → **$12K+ bill**
- **Fix:** Remove the file from git, amend the commit, force push

---

## 5. 🔥 DEEP DIVE: Git Cleanup Commands (What We Actually Did)

### The Problem
File `panther/AI/notes` contained a GitHub Personal Access Token (PAT). We couldn't push because GitHub blocked it. We needed to:
1. **Remove the secret file** from git tracking
2. **Erase it from history** so no one can find it
3. **Push the clean version** to GitHub

### Step-by-step: What Each Command Means

#### `git rm --cached <file>`
```bash
git rm --cached AI/notes
```
- `rm` = remove
- `--cached` = **only remove from git's index (staging), KEEP the local file**
- Your file stays on disk. Git just stops tracking it.
- Without `--cached`: would delete the file from disk too

#### `git commit --amend --no-edit`
```bash
git commit --amend --no-edit
```
- `--amend` = **replace** the very last commit with a new one
- The old commit (with the secret) is **gone forever**
- `--no-edit` = keep the same commit message (don't open editor)
- **Think of it like:** You took a photo, realized you had your eyes closed, so you take a new photo and throw the old one away

#### `git reset --soft <commit>`
```bash
git reset --soft eedd728
```
This is the command you were confused about. Let me break it down:

### What is HEAD?

```
HEAD ──► points to your CURRENT commit (where you are right now)

Before reset:
  a75a276 (HEAD -> master) add                 ← YOU ARE HERE
  df98f9f notes removed
  5461a14 .ignore added
  b2451b2 ok
  eedd728 initial commit                        ← We want to go back here

After git reset --soft eedd728:
  eedd728 (HEAD -> master) initial commit       ← HEAD MOVED HERE
  ⚠ b2451b2, 5461a14, df98f9f, a75a276 are GONE
```

### The 3 Reset Modes

| Mode | HEAD moves? | Working directory? | Staging area? | When to use |
|------|-------------|-------------------|---------------|-------------|
| `--soft` | ✅ Yes — moves back | ❌ Unchanged — files stay as-is | ✅ **Kept** — files remain staged | "I want a do-over on the commit but keep all my work" |
| `--mixed` *(default)* | ✅ Yes — moves back | ❌ Unchanged — files stay as-is | ❌ **Cleared** — need `git add` again | "I want to re-choose what files go in the commit" |
| `--hard` | ✅ Yes — moves back | ✅ **Overwritten** — files REVERT to old state | ❌ Cleared | **DANGER**. "I want to completely discard all changes since that commit" |

### Visual: --soft vs --hard

```
BEFORE:
Working Dir:   [notes.txt, main.tf, Dockerfile, ...]  ← latest versions
Staging:       [notes.txt ✓, main.tf ✓, ...]          ← all staged
HEAD ──►      a75a276 "add" (has secret commit)

git reset --soft eedd728:
Working Dir:   [notes.txt, main.tf, Dockerfile, ...]  ← SAME files (unchanged)
Staging:       [DELETED: notes.txt ✓, ...]             ← only changes FROM eedd728 are "delete notes.txt"
HEAD ──►      eedd728 "initial commit" (clean)

We then committed:
  f3824e0 "fix commit" = "delete notes.txt and .env"
  This is a BRAND NEW commit with NO secret
```

**Key insight:** The old commits (`a75a276`, `df98f9f`, etc.) are **gone** from the new history. But your current working files are **untouched**.

#### `git checkout --orphan <name>`
```bash
git checkout --orphan clean-main
```
- `--orphan` = create a branch with **ZERO history** — like a newborn repo
- All your current files remain on disk, unstaged
- You then `git add .` and `git commit -m "..."` to create a **brand new first commit**
- The old branch with all its messy history still exists until you delete it

**Think of it like:** You're building a house (your files). The foundation (git history) is cracked. `--orphan` says "let's build a new foundation under the same house."

#### `git branch -D <name>` vs `git branch -d <name>`
```bash
git branch -D main     # FORCE delete, even if changes aren't merged
git branch -d main     # Safe delete — only if changes are merged
```
- `-D` (capital) = **force delete** — "I don't care, just delete it"
- `-d` (lowercase) = **safe delete** — "only delete if it's safe"
- We used `-D` because we were replacing the whole branch

### The Full Flow We Ran (Annotated)

```bash
# === PANTHER REPO CLEANUP ===

# Step 1: See the messy history
git log --oneline -5
# a75a276 add
# df98f9f notes removed
# 5461a14 .ignore added
# b2451b2 ok
# eedd728 initial commit          ← The last clean commit

# Step 2: Move HEAD back to clean commit, KEEP all current files
git reset --soft eedd728
# HEAD now points to eedd728
# Working files: UNCHANGED
# Staging shows: "deleted AI/notes, deleted AI/AUTOMATION_HUB/.env"

# Step 3: Make a new commit (replaces the bad history)
git commit -m "fix commit"
# New commit f3824e0 created with NO secrets

# Step 4: Force push (overwrites remote history)
git push origin master --force
```

```bash
# === AZUREVM ROOT REPO CLEANUP ===

# Step 1: Create empty branch with ZERO history
git checkout --orphan clean-main
# All old commits gone. Files still on disk.

# Step 2: Stage only the files we want
git add .gitignore infrastructure-pipeline/ spidy/ .opencode/

# Step 3: Create the one and only commit
git commit -m "Initial commit: project structure"

# Step 4: Delete the old messy branch
git branch -D main

# Step 5: Rename current branch to main
git branch -m main

# Step 6: Force push (replaces ALL remote history with our clean commit)
git push origin main --force
```

### After Cleanup — Removing panther/ from Root

```bash
# panther/ has its own .git — it's a separate repo
# Root should NOT track it

# Remove panther/ from root's tracking (keep local files)
git rm --cached -r panther/

# Add to gitignore so it's never re-added
echo "panther/" >> .gitignore
git add .gitignore

# Amend the last commit (replace with cleaner version)
git commit --amend --no-edit
git push origin main --force
```

### When To Use Each Cleanup Technique

| Situation | Command |
|-----------|---------|
| Secret accidentally in last commit, NOT pushed | `git rm --cached file` + `git commit --amend` |
| Secret in last commit, ALREADY pushed | `git rm --cached file` + `git commit --amend` + `git push --force` |
| Secret in OLDER commit | Use `git filter-branch` or interactive rebase |
| Whole repo history is messy | `git checkout --orphan` + fresh commit |
| Want to undo last commit but keep work | `git reset --soft HEAD~1` |
| Want to undo and discard work | `git reset --hard HEAD~1` (DANGEROUS) |

---

## 6. Production Stories Covered

| Story | Lesson |
|-------|--------|
| Crypto miner from leaked AWS key ($12K in 4 hours) | Never commit secrets. Push Protection saved you. |
| Deleted state file → 2 days to recover 50 resources | Use remote state + locking + soft-delete |
| Bot scrapes GitHub for patterns like "AKIA", "ghp_" | Secrets in commits = automated crypto mining |

---

## 7. Project Structure Created

```
panther/
├── .github/workflows/terraform-plan.yml    # CI/CD pipeline (placeholder)
├── terraform/
│   ├── main.tf                             # Azure Resource Group
│   ├── modules/
│   │   ├── networking/main.tf
│   │   ├── compute/main.tf
│   │   ├── security/main.tf
│   │   └── storage/main.tf
│   └── environments/
│       ├── dev/terraform.tfvars
│       ├── staging/terraform.tfvars
│       └── prod/terraform.tfvars
├── docker/Dockerfile
├── scripts/health-check.sh                 # Working! Shows uptime, mem, disk
└── README.md                               # Pipeline overview
```

---

## 8. Full Command History (Annotated)

> Lines 1-100: VM setup (git, terraform, azure-cli, docker, disk expansion)
> Lines 101-200: ls flags, mkdir, touch, echo, cat, nano, chmod, health-check script
> Lines 201-264: git init → add → commit → push → secret blocked → cleanup → force push
> Lines 265-990: git checkout --orphan → fresh commit → delete old branch → rename → force push → remove nested repos

### Key Commands from History

| Line | Command | What We Learned |
|------|---------|----------------|
| 166 | `ls -la` | Read file permissions (first column) |
| 168 | `mkdir -p .github/workflow` | `-p` creates parent dirs |
| 195-196 | `echo >` vs `echo >>` | Overwrite vs append |
| 198-199 | `nano script.sh` + `chmod +x` | Write and make executable |
| 203 | `git init` | Start tracking |
| 206 | `git add .` | Stage everything |
| 208 | `git commit -m "msg"` | Take snapshot |
| 210-212 | `git rm --cached` | Remove from git, keep local |
| 224 | `git push origin main --force` | **DANGER**: overwrite remote |
| 234 | `git reset --soft eedd728` | Move HEAD back, keep files |
| 237-238 | `git commit -m "fix"` + `git push --force` | New clean commit + push |
| 248 | `git checkout --orphan clean-main` | Fresh branch, zero history |
| 252 | `git branch -D main` | Force delete old branch |
| 253 | `git branch -m main` | Rename current to main |
| 254 | `git push origin main --force` | Replace remote history |
| 255-258 | `git rm --cached -r panther/` + amend | Remove nested repo from root |
| 260-263 | Same for `infrastructure-pipeline/` | Keep root clean |

---

## 9. Commands Mastery Checklist

- [ ] `ls -la` — decode every column (file type, permissions, owner, size, date)
- [ ] `mkdir -p` — create nested directories in one command
- [ ] `echo >` vs `echo >>` — overwrite vs append to file
- [ ] `chmod +x` — make a script executable
- [ ] `./script.sh` — run a script from current directory
- [ ] `git init` → `git add .` → `git commit -m ""` — the basic flow
- [ ] `git status` — read green (staged) vs red (unstaged/untracked)
- [ ] `git log --oneline` — see commit history compactly
- [ ] `git rm --cached` — remove from git tracking, keep file on disk
- [ ] `git commit --amend` — **replace** the last commit (new hash)
- [ ] `git reset --soft <commit>` — move HEAD back, **keep** all current files staged
- [ ] `git reset --hard <commit>` — **DANGER**: discard all changes since that commit
- [ ] `git checkout --orphan <name>` — create branch with **zero history**
- [ ] `git branch -D <name>` — force delete a branch
- [ ] `git branch -m <name>` — rename current branch
- [ ] `git push origin main --force` — overwrite remote (use only when you mean it)

---

## 10. Questions to Review Tomorrow (Spaced Repetition)

These will come up in tomorrow's session:

1. **ls -la output:** What does `-rw-r--r--` mean? (file type, owner rw, group r, others r)
2. **Git staging:** You `git add` file1, edit it, `git commit`. What gets committed?
3. **git reset --soft vs --hard:** Which one keeps your working files? Which one destroys them?
4. **HEAD:** What is HEAD in git?
5. **--force:** Why is `git push --force` dangerous? When is it okay to use?
6. **GitHub Push Protection:** What happens when you push a secret? Why does this exist?

---

## 11. What's Next (Tomorrow)

1. **Clear doubts** on all git cleanup commands (HEAD, reset modes, --orphan, --force)
2. **Phase 1 Step 4-5:** Symlinks, .gitignore patterns, undo commands
3. **Phase 1 Step 6:** git branch, diff, log --graph
4. Then → **Week 1 Day 1: Terraform State + HCL** (deploy real Azure resources!)

---

*"Every command teaches Linux as a byproduct. Every session adds to your portfolio. Trust the process."*



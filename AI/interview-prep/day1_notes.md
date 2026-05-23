# Day 1 Notes — Phase 1: Linux Terminal + Git CLI Foundations
> Date: 2026-05-23 | Session: 2h | Streak: Day 1

---

## 1. ls — The Most Important Command

### Flag Combinations

| Command | What it does | Use Case |
|---------|-------------|----------|
| `ls -l` | Long format (permissions, owner, size, date) | See details |
| `ls -a` | Show ALL files including hidden (dotfiles) | Find configs |
| `ls -la` | Both combined — full detail + hidden | **Default first command on any server** |
| `ls -lah` | Same + human-readable sizes (K, M, G) | Check file sizes |
| `ls -R` | Recursive — lists everything inside subdirs | See full tree |

### Reading `ls -la` Output (10 Columns)

```
drwxrwxr-x  6 ubuntu ubuntu 4096 May 23 11:47 .
↑↑↑↑↑↑↑↑↑↑  ↑ ↑↑↑↑↑↑ ↑↑↑↑↑↑ ↑↑↑↑ ↑↑↑↑↑↑↑↑↑↑↑↑ ↑↑
1          2 3       4       5    6           7
```

| Column | Meaning | Example |
|--------|---------|---------|
| 1: File type | `d` = dir, `-` = file, `l` = symlink | `drwxrwxr-x` |
| 1: Permissions | r=read(4), w=write(2), x=execute(1) | Owner `rwx`, Group `rwx`, Others `r-x` |
| 2 | Link count | `6` |
| 3 | Owner | `ubuntu` |
| 4 | Group | `ubuntu` |
| 5 | Size (bytes) | `4096` (dirs always 4096) |
| 6 | Last modified | `May 23 11:47` |
| 7 | Name | `.` = current, `..` = parent |

### Hidden Files
- Any file starting with `.` (dot) is hidden
- `ls -a` needed to see them
- Examples: `.gitignore`, `.env`, `.git/`, `.opencode/`

---

## 2. File Operations

| Command | What it does | Flags |
|---------|-------------|-------|
| `pwd` | Print Working Directory | — |
| `mkdir dirname` | Make directory | `-p` = create parents |
| `touch file.txt` | Create empty file / update timestamp | — |
| `echo "text"` | Print text to terminal | `>` = overwrite file, `>>` = append |
| `cat file.txt` | Show file contents | — |
| `nano file.txt` | Open text editor | Ctrl+O = save, Ctrl+X = exit |
| `mv old new` | Move or rename file | — |
| `chmod +x file` | Add execute permission | — |
| `./script.sh` | Run script from current dir | — |

### Key Concept: Silence = Success
Linux only prints errors. No news is good news.

### `>` vs `>>`
```bash
echo "hello" > file.txt    # Creates or OVERWRITES file.txt
echo "world" >> file.txt   # APPENDS to file.txt
```

---

## 3. Git Basics

### The 3 Areas of Git
```
Working Directory  ──[git add]──►  Staging Area  ──[git commit]──►  Local Repo
(your files)           (prepare)         (snapshot)
```

### Commands You Ran

| Command | What it does | Example |
|---------|-------------|---------|
| `git init` | Initialize git in current dir | `git init` |
| `git add .` | Stage ALL changes | `git add file.txt` |
| `git commit -m "msg"` | Snapshot staging with message | `git commit -m "first"` |
| `git status` | See staged (green) vs unstaged (red) | `git status` |
| `git branch -m newname` | Rename current branch | `git branch -m main` |
| `git rm --cached file` | Remove from git tracking, keep locally | `git rm --cached secret.txt` |

### Interview Question: `git add` vs `git commit`
- `git add` = move files to staging (choose WHAT goes in)
- `git commit` = take a permanent snapshot of staging (SAVE)
- The staging area exists so you can craft commits deliberately

### Scenario Question
> You `git add file1.txt`, edit it again, then `git commit`. Does the commit include the second edit?

**Answer:** No. `git add` snapshots the content at that moment. You need `git add` again after editing.

---

## 4. Git Remote & Push

| Command | What it does |
|---------|-------------|
| `git remote add origin URL` | Link local repo to GitHub |
| `git push origin main` | Push local commits to GitHub |
| `git push origin main --force` | Overwrite remote history (DANGEROUS) |

### Production Story: GitHub Push Protection
- GitHub automatically scans all pushes for secrets (API keys, passwords, tokens)
- If detected → push is **blocked** with error message
- The secret file: `panther/AI/notes` contained a GitHub PAT
- **Why?** Automated bots scrape GitHub for secrets → launch crypto miners → $12K+ bill

---

## 5. Git History Cleanup (CRITICAL SKILL)

### Removing a Secret from Latest Commit (Not Pushed)

```bash
git rm --cached secrets.txt          # Stop tracking, keep local
echo "secrets.txt" >> .gitignore     # Don't re-add
git add .gitignore
git commit --amend --no-edit         # Replace last commit (no secret)
git push origin main --force         # Force push (you rewrote history)
```

### Removing a Secret from Pushed Commit

```bash
# WARNING: Rewrites shared history
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch secrets.txt" \
  --prune-empty --tag-name-filter cat -- --all
git push origin main --force
```

### Full Repo Reset (Clean Slate)

```bash
git checkout --orphan clean-branch   # New branch with ZERO history
git add .                            # Stage current files only
git commit -m "Fresh start"          # One clean commit
git branch -D main                   # Delete old branch
git branch -m main                   # Rename current to main
git push origin main --force         # Replace remote
```

### `git reset --soft` vs `--hard`

| Flag | HEAD Movement | Working Dir | Staging | Use Case |
|------|--------------|-------------|---------|----------|
| `--soft` | Moves back | Unchanged | Kept | Fix last commit |
| `--mixed` (default) | Moves back | Unchanged | Cleared | Unstage files |
| `--hard` | Moves back | Overwritten | Cleared | DANGEROUS — discard changes |

---

## 6. Production Stories Covered

| Story | Lesson |
|-------|--------|
| Crypto miner from leaked AWS key | Never commit secrets. GitHub Push Protection is your friend. |
| Deleted state file → 2 days recovery | Always use remote state + locking |
| Deleted state file → 2 days recovery | Soft-delete + RBAC on Azure Storage |

---

## 7. Project Structure Created

```
panther/
├── .github/workflows/terraform-plan.yml   # CI/CD (placeholder)
├── terraform/
│   ├── main.tf                            # Azure RG definition
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
├── scripts/health-check.sh                # Working health script
└── README.md
```

---

## 8. Commands Mastery Checklist

- [ ] `ls -la` — decode every column
- [ ] `mkdir -p` — create nested directories
- [ ] `echo >` vs `echo >>` — overwrite vs append
- [ ] `chmod +x` — make script executable
- [ ] `./script.sh` — run current directory script
- [ ] `git init` → `add` → `commit` flow
- [ ] `git status` — read green (staged) vs red (unstaged)
- [ ] `git commit --amend` — replace last commit
- [ ] `git reset --soft` — undo commit, keep changes
- [ ] `git checkout --orphan` — fresh branch no history
- [ ] `git push --force` — WARNING: rewrites remote

---

## 9. What's Next (Tomorrow)

Phase 1 Step 4-5: Symlinks, .gitignore patterns, undo commands (restore, reset, amend)
Phase 1 Step 6: git branch, diff, log --graph
Then → **Week 1 Day 1: Terraform State + HCL** (deploy real Azure resources)

---

*"Every command teaches Linux as a byproduct. Every session adds to your portfolio. Trust the process."*

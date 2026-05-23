# Git Interview Study Plan

**Why Git Matters:** Git questions appear in EVERY DevOps interview. They test:
1. Do you understand branching strategies?
2. Can you handle merge conflicts?
3. Do you know how to undo mistakes?
4. Can you work in a team workflow?

**Context:** You use git at Wipro, but product companies have different branching strategies and expect deeper knowledge.

---

## 1. Branching Strategies (THE #1 Git Interview Topic)

### GitFlow (Traditional — Know It, Dont Use It)
```
main        ───●──────────────────●───
                │                  │
develop        ──●────●────●────●───
                │    │    │    │
feature/xyz    ──●───────●           (feature branch)
                │         │
release/1.0    ────────────●──●──●    (release branch)
                            │
hotfix/1.0.1   ────────────────●──●   (hotfix branch)
```

**Interview answer:** "GitFlow has main, develop, feature, release, and hotfix branches. It's good for scheduled releases but adds complexity. Most product companies prefer something simpler."

### Trunk-Based Development (Modern — Product Companies Use This)
```
main  ──●──●──●──●──●──●──●──●──  (small, frequent commits)
         │  │      │
         │  │      short-lived feature branch (merged in hours, not days)
         │  │
         │  feature-branch (1-2 days max)
         │
         bug-fix (merged immediately)
```

**Interview answer:** "Trunk-based development means everyone commits to main multiple times a day. Feature branches are short-lived (hours, not days). This enables true CI — every commit is validated and could go to production."

### GitHub Flow (Common in Product Companies)
```
main  ──●────────────────────●────  (production-ready, protected)
         │                    │
         feature-branch    PR → merge
```

**Interview answer:** "GitHub Flow is simpler: create a branch, make changes, open a PR, merge to main. Only main is protected. Deploy from main. Works great for continuous deployment."

### Which one for interviews?
| Strategy | When to mention | Why |
|----------|----------------|------|
| GitFlow | Legacy companies, scheduled releases | Shows you've seen it |
| Trunk-based | Modern product companies | Shows you understand CI |
| GitHub Flow | Startups, simple deployments | Most common for 3-5 YOE roles |

**Your answer:** "I prefer trunk-based development or GitHub Flow. Feature branches are short-lived, PRs are reviewed, main is always deployable. GitFlow adds complexity without much benefit for a DevOps team doing CI/CD."

---

## 2. Git Commands You MUST Know (Not Just Use)

### Everyday Commands
```bash
git clone <url>
git checkout -b feature/new-thing   # Create and switch to branch
git add -p                          # Interactive staging (chunk by chunk)
git commit -m "feat: add login"     # Semantic commit
git push origin feature/new-thing
git pull --rebase                   # Pull with rebase (cleaner history)
```

### Merge vs Rebase (CRITICAL Interview Topic)

**Merge:**
```
      A---B---C feature
     /         \
D---E---F---G---H---I main
```
```bash
git checkout main
git merge feature   # Creates merge commit H
```
**Pros:** Preserves history, safe, easy to understand
**Cons:** Ugly history with merge bubbles, hard to bisect

**Rebase:**
```
              A'--B'--C' feature
             /
D---E---F---G---I main
```
```bash
git checkout feature
git rebase main    # Replays feature commits on top of main
```
**Pros:** Clean linear history, easy git bisect
**Cons:** Rewrites history (NEVER rebase shared branches)

**Interview answer:**
> "I rebase feature branches to keep history clean. Before pushing, I rebase onto main to incorporate latest changes. But I NEVER rebase shared branches (main, develop) — that rewrites history and breaks other developers."

### Undoing Mistakes (Asked in Every Interview)

| Mistake | Command | What It Does |
|---------|---------|-------------|
| Last commit wrong message | `git commit --amend -m "new message"` | Fix last commit message |
| Forgot to add a file | `git add forgotten.txt && git commit --amend --no-edit` | Add file to last commit |
| Staged wrong file | `git restore --staged file.txt` | Unstage file (keep changes) |
| Want to discard local changes | `git restore file.txt` | Discard uncommitted changes |
| Committed to wrong branch | `git reset HEAD~1 && git stash && git checkout correct-branch && git stash pop` | Move commit to correct branch |
| Want to undo a pushed commit | `git revert <commit-hash>` | Create NEW commit that undoes changes (safe for shared branches) |

**Critical distinction:**
- `git reset` — moves branch pointer BACK (rewrites history — DANGEROUS)
- `git revert` — creates NEW commit that undoes changes (SAFE for shared branches)

---

## 3. Git in DevOps — What Product Companies Expect

### PR Workflow
```
1. git checkout -b feat/TER-123-add-login
2. Make changes, commit with semantic message
3. git push origin feat/TER-123-add-login
4. Open PR on GitHub/Azure Repos
5. PR triggers CI pipeline (lint, test, build)
6. Team reviews code
7. Merge to main (squash or merge commit)
8. Main branch triggers CD pipeline
```

### Branch Protection Rules (Azure DevOps / GitHub)
- Require PR review (at least 1 approver)
- Require status checks to pass (CI pipeline must pass)
- Require up-to-date branches (must rebase on latest main)
- No direct pushes to main

### Git Hooks (Bonus — Impressive to Know)
```bash
# .git/hooks/pre-commit — runs before each commit
#!/bin/bash
echo "Running linter..."
npx eslint .
if [ $? -ne 0 ]; then
    echo "Linting failed. Commit rejected."
    exit 1
fi
```

### Commit Message Conventions (Conventional Commits)
```
feat: add login page                # New feature
fix: resolve timeout issue          # Bug fix
chore: update dependencies           # Maintenance
docs: update README                 # Documentation
refactor: simplify auth logic        # Code restructuring
test: add auth unit tests            # Tests
ci: optimize build pipeline          # CI/CD changes
```

---

## 4. Git Interview Questions

### Q1: "Whats the difference between git merge and git rebase?"
> Merge creates a commit that joins two histories — preserves everything but creates merge bubbles. Rebase rewrites commits on top of another branch — creates clean linear history but rewrites commit SHAs. I rebase feature branches before merging to main. I never rebase shared branches.

### Q2: "How do you resolve a merge conflict?"
> ```bash
> git merge feature-branch
> # CONFLICT in file.txt
> # Fix conflicts manually in file.txt (look for <<<<<<<, =======, >>>>>>>)
> git add file.txt
> git commit
> ```
> To avoid conflicts: communicate with team, rebase frequently, break PRs into smaller chunks.

### Q3: "What is git stash? When do you use it?"
> `git stash` temporarily saves uncommitted changes when you need to switch branches urgently. `git stash pop` restores them. Use when: "I'm working on feature A, need to fix a production bug on main immediately."

### Q4: "Explain git reset vs git revert"
> `git reset` moves the branch pointer backward — rewrites history. USE ONLY on local branches. `git revert` creates a new commit that undoes changes — SAFE for shared branches. Never `git reset` on main.

### Q5: "What is git bisect?"
> `git bisect` binary searches through commit history to find where a bug was introduced. You mark commits as "good" or "bad", and git bisect narrows down to the exact commit that caused the bug. Essential for debugging regressions.

---

## Quick Reference

| Scenario | Command |
|----------|---------|
| Create branch | `git checkout -b feat/xyz` |
| Interactive stage | `git add -p` |
| Fix last commit | `git commit --amend` |
| Clean linear history | `git pull --rebase` |
| Undo pushed commit | `git revert <hash>` |
| Discard local changes | `git restore .` |
| Save work temporarily | `git stash` |
| View history as graph | `git log --oneline --graph --all` |
| Find bug introduction | `git bisect` |
| See what changed | `git diff` / `git diff --staged` |

---

*Git is 90% interview, 10% usage. Nail the theory here.*

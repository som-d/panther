# Git Interview Questions (7-14 LPA)

---

### Q1: "What is the difference between git merge and git rebase?"
> **Merge** creates a new commit that joins two histories. Preserves full history but creates merge bubbles. Safe for shared branches.
> **Rebase** replays commits on top of another branch. Creates clean linear history but rewrites commit SHAs (changes history).
> 
> **My practice:** Rebase feature branches before merging (keeps history clean). Never rebase shared branches (main, develop).

### Q2: "How do you undo a commit that was already pushed?"
> Use `git revert <commit-hash>` — creates a NEW commit that undoes the changes. Safe for shared branches because it doesn't rewrite history. Never use `git reset` on pushed commits (rewrites history, breaks other developers).

### Q3: "Explain GitFlow vs Trunk-Based Development"
> **GitFlow:** main, develop, feature, release, hotfix branches. Good for scheduled releases. Complex for CI/CD.
> **Trunk-Based:** Everyone commits to main daily. Short-lived feature branches. Enables true CI. Simpler. Preferred by product companies doing continuous deployment.

### Q4: "How do you resolve a merge conflict?"
> ```bash
> git merge feature-branch
> # CONFLICT in file.txt — look for <<<<<<<, =======, >>>>>>>
> # Fix conflicts manually
> git add file.txt
> git commit
> ```
> To avoid conflicts: communicate with team, rebase frequently, break PRs into smaller chunks (< 200 lines).

### Q5: "What is git stash and when do you use it?"
> `git stash` temporarily saves uncommitted changes when you need to switch branches urgently. `git stash pop` restores them. Use case: "I'm working on feature A, need to fix a production bug on main immediately."

### Q6: "What is git bisect?"
> Binary search through commit history to find where a bug was introduced. Mark commits as "good" or "bad". Git narrows down to the exact commit that caused the bug. Essential for debugging regressions in production.

### Q7: "Explain the difference between git reset, git revert, and git restore"
> - `git reset` — moves branch pointer (rewrites history). Use only on local/unpushed commits.
> - `git revert` — creates new commit that undoes changes (safe for shared branches).
> - `git restore` — discards working directory changes (unstaged changes).

### Q8: "What is a detached HEAD state?"
> When you checkout a specific commit instead of a branch. You're not on any branch. Any commits made here are lost when you checkout another branch (unless you create a new branch from them). Fix: `git checkout -b new-branch-name`.

### Q9: "What is a pull request workflow?"
> 1. Create feature branch from main
> 2. Make changes, commit with semantic messages
> 3. Push branch, open PR
> 4. PR triggers CI (lint, test, build)
> 5. Team reviews code
> 6. Merge (squash or merge commit)
> 7. Delete feature branch

### Q10: "How do you maintain clean git history?"
> - Use `git pull --rebase` instead of `git pull` (avoids merge commits)
> - Rebase feature branches before merging
> - Squash commits before merging (one commit per feature)
> - Use conventional commits (feat, fix, chore, docs)
> - Never force push to shared branches

---

## Quick Reference

| Scenario | Command |
|----------|---------|
| Create branch | `git checkout -b feat/xyz` |
| Interactive stage | `git add -p` |
| Fix last commit | `git commit --amend` |
| Clean pull | `git pull --rebase` |
| Undo pushed commit | `git revert <hash>` |
| Discard local changes | `git restore .` |
| Save work temporarily | `git stash` |
| Find bug introduction | `git bisect` |
| View history graph | `git log --oneline --graph --all` |
| List conflicts | `git diff --name-only --diff-filter=U` |

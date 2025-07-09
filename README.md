
# ✅ Git Branch & Pull Request Checklist

## 🏗️ Before Starting a Branch
- [ ] Pull the latest `main` branch  
  `git checkout main && git pull origin main`
- [ ] Create a new branch with a descriptive name  
  `git checkout -b feature/your-task-name`

---

## 🧑‍💻 While Working on the Branch
- [ ] Keep changes focused on **one feature or fix**
- [ ] Avoid unrelated "quick fixes" — make a note and do them later
- [ ] Commit frequently with meaningful messages:
  - `feat:`, `fix:`, `refactor:`, `docs:`, `chore:`, etc.
  - Example: `feat(auth): add GitHub OAuth login`
- [ ] Run and test your code locally before pushing

---

## 🔄 Before Pushing or Opening a PR
- [ ] Merge latest `main` into your branch  
  `git fetch origin && git merge origin/main`
- [ ] Resolve any conflicts cleanly
- [ ] Push your branch  
  `git push origin feature/your-task-name`

---

## 🚀 Creating a Pull Request
- [ ] PR title is clear and describes the purpose (avoid vague titles)
- [ ] Description explains what was changed and why
- [ ] Screenshots or GIFs included if UI is affected
- [ ] Linked to relevant issues or tasks (e.g., `Closes #42`)
- [ ] Add reviewers or labels (if in a team)

---

## 🧹 After PR is Merged
- [ ] Delete the feature branch (on GitHub or via `git push origin --delete`)
- [ ] Pull the updated `main` to your local  
  `git checkout main && git pull origin main`

---

## ✨ Pro Tips (Optional)
- Use `draft` PRs if work is still in progress
- Use `squash & merge` to keep commit history clean
- Tag releases with version numbers for important milestones
"""

# Save to a markdown file
file_path = "/mnt/data/git-branch-pr-checklist.md"
with open(file_path, "w") as f:
    f.write(checklist_md)

file_path

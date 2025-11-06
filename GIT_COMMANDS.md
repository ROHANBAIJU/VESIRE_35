# Quick Git Commands Reference - AgriScan

## 🚀 Initial Setup (First Time Only)

```bash
# Navigate to project directory
cd Z:\VESIRE_35

# Initialize git (if not already initialized)
git init

# Add the gitignore and gitattributes
git add .gitignore .gitattributes
git commit -m "Add Git configuration files"

# Add all project files
git add .
git commit -m "Initial commit: AgriScan plant disease detection system"

# Connect to GitHub repository
git remote add origin https://github.com/ROHANBAIJU/VESIRE_35.git
git branch -M main
git push -u origin main
```

---

## 📝 Daily Git Workflow

### Check Status
```bash
# See what files have changed
git status

# See detailed changes
git diff
```

### Stage Changes
```bash
# Stage specific files
git add Backend/api/app.py
git add ar_test_app/lib/main.dart

# Stage all changed files
git add .

# Stage by type
git add *.py
git add *.dart
```

### Commit Changes
```bash
# Commit with message
git commit -m "Add webcam detection feature"

# Commit with detailed message
git commit -m "Fix: Async Gemini diagnosis

- Implemented threading for non-blocking Gemini calls
- Bounding boxes now stay visible during diagnosis
- Improved UX with status messages"
```

### Push to GitHub
```bash
# Push to main branch
git push origin main

# Force push (use carefully!)
git push -f origin main
```

---

## 🌿 Branch Management

### Create and Switch Branches
```bash
# Create new branch
git branch feature/ar-overlay

# Switch to branch
git checkout feature/ar-overlay

# Create and switch in one command
git checkout -b feature/gemini-integration
```

### Merge Branches
```bash
# Switch to main
git checkout main

# Merge feature branch
git merge feature/ar-overlay

# Delete merged branch
git branch -d feature/ar-overlay
```

---

## 🔄 Update from Remote

```bash
# Fetch changes
git fetch origin

# Pull changes
git pull origin main

# Pull with rebase
git pull --rebase origin main
```

---

## 📦 Specific File Operations

### Add AI Models
```bash
# Add trained model
git add Backend/models/agriscan_plantdoc/weights/best.pt

# Add all models
git add Backend/models/
```

### Add Documentation
```bash
# Add all markdown files
git add *.md
git add **/*.md
```

### Ignore Specific Files After They're Tracked
```bash
# Remove from tracking but keep locally
git rm --cached Backend/data/agriscan.db

# Remove directory
git rm --cached -r __pycache__/
```

---

## 🔍 View History

```bash
# View commit history
git log

# View compact history
git log --oneline

# View with graph
git log --graph --oneline --all

# View file history
git log -- Backend/webcam_detection.py
```

---

## ↩️ Undo Changes

### Before Commit
```bash
# Discard changes in file
git checkout -- Backend/api/app.py

# Unstage file
git reset HEAD Backend/api/app.py

# Discard all changes
git reset --hard
```

### After Commit
```bash
# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1

# Create new commit that undoes previous commit
git revert HEAD
```

---

## 🏷️ Tags (Releases)

```bash
# Create tag
git tag -a v1.0.0 -m "Release v1.0.0: AgriScan MVP"

# Push tag to GitHub
git push origin v1.0.0

# Push all tags
git push origin --tags

# List tags
git tag -l
```

---

## 🔧 Configuration

```bash
# Set username
git config --global user.name "ROHANBAIJU"

# Set email
git config --global user.email "your.email@example.com"

# View config
git config --list

# Set default editor
git config --global core.editor "code --wait"
```

---

## 🚨 Emergency Commands

### Fix Merge Conflicts
```bash
# See conflicted files
git status

# After resolving conflicts manually
git add .
git commit -m "Resolve merge conflicts"
```

### Reset to Remote State
```bash
# WARNING: This discards all local changes!
git fetch origin
git reset --hard origin/main
```

### Stash Changes
```bash
# Save changes temporarily
git stash

# List stashes
git stash list

# Apply latest stash
git stash apply

# Apply and remove stash
git stash pop
```

---

## 📊 Useful Aliases

Add to `~/.gitconfig`:

```ini
[alias]
    st = status
    co = checkout
    br = branch
    cm = commit -m
    lg = log --graph --oneline --all
    undo = reset --soft HEAD~1
    
    # Quick add and commit
    ac = !git add . && git commit -m
    
    # Quick push
    p = push origin main
    
    # View changes
    changes = diff --name-status
```

Usage:
```bash
git st              # git status
git co main         # git checkout main
git ac "message"    # git add . && git commit -m "message"
git lg              # pretty log
```

---

## 💡 Best Practices

### Commit Messages
```bash
# Good ✅
git commit -m "Add async Gemini diagnosis with threading"
git commit -m "Fix: Bounding box visibility during API calls"
git commit -m "Docs: Update API documentation with new endpoints"

# Bad ❌
git commit -m "fixed stuff"
git commit -m "update"
git commit -m "changes"
```

### Commit Types
- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting)
- **refactor**: Code refactoring
- **test**: Adding tests
- **chore**: Maintenance tasks

Example:
```bash
git commit -m "feat: Add real-time webcam detection"
git commit -m "fix: Resolve Gemini model deprecation issue"
git commit -m "docs: Add Git setup guide"
```

---

## 🎯 Project-Specific Commands

### Update Models
```bash
# After training new model
git add Backend/models/agriscan_plantdoc/weights/best.pt
git commit -m "Update trained model with improved accuracy"
git push
```

### Update API
```bash
# After API changes
git add Backend/api/
git commit -m "feat: Add new diagnosis endpoints"
git push
```

### Update Frontend
```bash
# After Flutter changes
git add ar_test_app/lib/
git commit -m "feat: Implement AR bounding box overlay"
git push
```

---

## 📱 GitHub Specific

### Create Pull Request
```bash
# Push feature branch
git push origin feature/new-feature

# Then create PR on GitHub website
```

### Clone Repository
```bash
# Clone your repo
git clone https://github.com/ROHANBAIJU/VESIRE_35.git

# Clone specific branch
git clone -b feature/branch https://github.com/ROHANBAIJU/VESIRE_35.git
```

---

## ✅ Pre-Push Checklist

Before `git push`:
- [ ] All tests pass
- [ ] No sensitive data (API keys, passwords)
- [ ] Code is formatted
- [ ] Documentation is updated
- [ ] Commit message is clear
- [ ] No debug code left in

---

## 🆘 Help

```bash
# Get help for any command
git help <command>
git help commit
git help push

# Quick help
git <command> --help
git commit --help
```

---

**Keep this file handy for quick reference!** 🚀

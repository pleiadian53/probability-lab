# GitHub Setup Guide

**Complete guide for publishing probability-lab to GitHub and using GitLens**

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Initial Git Setup](#initial-git-setup)
3. [Creating GitHub Repository](#creating-github-repository)
4. [Pushing to GitHub](#pushing-to-github)
5. [GitLens Setup](#gitlens-setup)
6. [Common Git Workflows](#common-git-workflows)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Tools

1. **Git** - Version control system
   ```bash
   # Check if installed
   git --version
   
   # Install on macOS (if needed)
   brew install git
   ```

2. **GitHub CLI** - Command-line tool for GitHub
   ```bash
   # Check if installed
   gh --version
   
   # Install on macOS (if needed)
   brew install gh
   ```

3. **GitHub Account** - Create at https://github.com/signup

### Verify Your Setup

```bash
# Check git configuration
git config --global user.name
git config --global user.email

# If not set, configure:
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

---

## Initial Git Setup

### Step 1: Initialize Git Repository

```bash
# Navigate to project directory
cd /Users/pleiadian53/work/probability-lab

# Initialize git repository
git init

# Rename default branch to 'main' (modern convention)
git branch -m main
```

**What this does:**
- Creates `.git/` directory (hidden)
- Sets up version control tracking
- Configures 'main' as the default branch

### Step 2: Verify .gitignore

Your `.gitignore` is already configured to exclude:
- `*.egg-info/` - Package metadata ✅
- `__pycache__/` - Python bytecode ✅
- `dev/` - Private development notes ✅
- `*.pyc`, `*.pyo` - Compiled Python ✅
- Virtual environments ✅

```bash
# Verify .gitignore is working
git status

# Should NOT see:
# - probability_lab.egg-info/
# - __pycache__/
# - *.pyc files
```

### Step 3: Stage Files

```bash
# Add all files (respects .gitignore)
git add .

# Check what will be committed
git status

# Or see a shorter view
git status --short
```

**Expected output:**
```
A  .gitignore
A  README.md
A  docs/
A  prob_lab/
A  pyproject.toml
... (all tracked files)
```

### Step 4: Create Initial Commit

```bash
# Create initial commit with descriptive message
git commit -m "Initial commit: probability-lab with comprehensive documentation

- Core probability/statistics functionality
- Hydra-based experiment management
- Comprehensive documentation (setup, dependencies, Hydra guides)
- Streamlit app for interactive exploration
- Support for survival analysis and extreme value theory"
```

**What this does:**
- Creates a snapshot of your project
- Records who, when, and what changed
- Generates a unique commit hash (e.g., `aa0b55b`)

### Step 5: Verify Commit

```bash
# View commit history
git log

# Or one-line format
git log --oneline

# See what files were committed
git show --stat
```

---

## Creating GitHub Repository

### Method 1: Using GitHub CLI (Recommended)

#### Step 1: Authenticate with GitHub

```bash
gh auth login
```

**Interactive prompts:**
1. **What account do you want to log into?** → `GitHub.com`
2. **What is your preferred protocol?** → `HTTPS` (easier) or `SSH` (if you have keys)
3. **How would you like to authenticate?** → `Login with a web browser` (easiest)
4. Copy the one-time code shown
5. Press Enter to open browser
6. Paste code and authorize

**Verify authentication:**
```bash
gh auth status
```

#### Step 2: Create Repository and Push

**Option A: Public Repository (Recommended for Open Source)**

```bash
gh repo create probability-lab \
  --public \
  --source=. \
  --remote=origin \
  --push \
  --description "Probability and statistics toolkit with survival analysis, extreme value theory, and Hydra-based experiment management"
```

**Option B: Private Repository**

```bash
gh repo create probability-lab \
  --private \
  --source=. \
  --remote=origin \
  --push \
  --description "Probability and statistics toolkit with survival analysis, extreme value theory, and Hydra-based experiment management"
```

**What this command does:**
- ✅ Creates repository on GitHub
- ✅ Adds remote named "origin"
- ✅ Pushes your code
- ✅ Sets up branch tracking
- ✅ Opens repository in browser

#### Step 3: Verify Repository

```bash
# Check remote configuration
git remote -v

# Should show:
# origin  https://github.com/YOUR_USERNAME/probability-lab.git (fetch)
# origin  https://github.com/YOUR_USERNAME/probability-lab.git (push)

# View repository in browser
gh repo view --web
```

### Method 2: Using GitHub Web UI

If you prefer creating the repository through the browser:

#### Step 1: Create Repository on GitHub

1. Go to https://github.com/new
2. **Repository name:** `probability-lab`
3. **Description:** "Probability and statistics toolkit with survival analysis, extreme value theory, and Hydra-based experiment management"
4. **Visibility:** Public or Private
5. **DO NOT** initialize with README, .gitignore, or license (you already have these)
6. Click **Create repository**

#### Step 2: Add Remote and Push

```bash
# Add GitHub as remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/probability-lab.git

# Push code to GitHub
git push -u origin main
```

**The `-u` flag:**
- Sets up tracking between local `main` and remote `origin/main`
- Future pushes can just use `git push`

---

## Pushing to GitHub

### First Push (Already Done Above)

```bash
# Push main branch and set upstream
git push -u origin main
```

### Subsequent Pushes

After making changes:

```bash
# 1. Check what changed
git status

# 2. Stage changes
git add .
# Or stage specific files
git add docs/new-file.md

# 3. Commit with message
git commit -m "Add new feature or fix bug"

# 4. Push to GitHub
git push
```

### Pushing Tags

```bash
# Create a version tag
git tag -a v0.1.0 -m "Initial release"

# Push tag to GitHub
git push origin v0.1.0

# Or push all tags
git push --tags
```

---

## GitLens Setup

### What is GitLens?

GitLens is a powerful VS Code extension that supercharges Git capabilities:
- 📊 Inline blame annotations
- 📈 Commit history visualization
- 🔍 File and line history
- 🌳 Repository visualization
- 👥 Authorship insights

### Installation

#### Step 1: Install GitLens Extension

**In VS Code:**
1. Open Extensions (⌘+Shift+X on Mac, Ctrl+Shift+X on Windows/Linux)
2. Search for "GitLens"
3. Click **Install** on "GitLens — Git supercharged" by GitKraken
4. Reload VS Code if prompted

**Or via command line:**
```bash
code --install-extension eamodio.gitlens
```

#### Step 2: Verify Installation

After installation, you should see:
- GitLens icon in the Activity Bar (left sidebar)
- Inline blame annotations in your code
- Git information in the status bar

### GitLens Features

#### 1. Inline Blame Annotations

**What you'll see:**
```python
def fit_distribution(data, dist='weibull_min'):  # John Doe, 2 days ago • Initial commit
    """Fit distribution to data"""
    ...
```

**Toggle blame:**
- Click GitLens icon in status bar
- Or use Command Palette: `GitLens: Toggle Line Blame`

#### 2. File History

**View file history:**
1. Open any file
2. Click GitLens icon in Activity Bar
3. Expand "File History"
4. See all commits that modified this file

**Or right-click file:**
- "Open File History"
- "Open File History in Side Bar"

#### 3. Line History

**See who changed a specific line:**
1. Place cursor on any line
2. Hover over the line
3. See commit details, author, date
4. Click to see full commit

**Or:**
- Right-click line → "Show Line History"

#### 4. Repository View

**Explore repository:**
1. Click GitLens icon in Activity Bar
2. See sections:
   - **Commits** - Commit history
   - **Branches** - All branches
   - **Remotes** - Remote repositories
   - **Stashes** - Stashed changes
   - **Tags** - Version tags
   - **Contributors** - Who contributed what

#### 5. Commit Graph

**Visualize commit history:**
1. Command Palette (⌘+Shift+P)
2. Type "GitLens: Show Commit Graph"
3. See visual representation of commits and branches

#### 6. Compare Changes

**Compare files or commits:**
- Right-click file → "Open Changes with Previous Revision"
- Right-click file → "Open Changes with Working File"
- In Commit view → Click commit → See changed files

### GitLens Configuration

#### Recommended Settings

**Open Settings (⌘+,) and search for "gitlens":**

```json
{
  // Show inline blame by default
  "gitlens.currentLine.enabled": true,
  
  // Show blame annotations on hover
  "gitlens.hovers.enabled": true,
  
  // Show file history in Side Bar
  "gitlens.views.fileHistory.enabled": true,
  
  // Show line history in Side Bar
  "gitlens.views.lineHistory.enabled": true,
  
  // Compact commit messages
  "gitlens.views.commits.showBranchComparison": "working",
  
  // Show avatars in views
  "gitlens.views.showAvatars": true
}
```

#### Customizing Blame Format

```json
{
  "gitlens.currentLine.format": "${author}, ${agoOrDate} • ${message}",
  "gitlens.currentLine.scrollable": false
}
```

### Using GitLens with probability-lab

#### 1. View Documentation History

```bash
# See who wrote/modified documentation
# Open docs/dependencies.md
# GitLens will show: "You, 2 hours ago • Add dependencies documentation"
```

#### 2. Track Code Changes

```bash
# See evolution of core modules
# Open prob_lab/distributions/scipy_wrappers.py
# View File History to see all changes
```

#### 3. Understand Hydra Configuration

```bash
# See when Hydra configs were added
# Open conf/config.yaml
# Hover over lines to see commit details
```

#### 4. Review Experiment Scripts

```bash
# Track changes to experiment runner
# Open prob_lab/exp/run.py
# Use Line History to see specific changes
```

### GitLens Keyboard Shortcuts

| Action | Shortcut (Mac) | Shortcut (Windows/Linux) |
|--------|----------------|--------------------------|
| Toggle File Blame | `⌘+Shift+G B` | `Ctrl+Shift+G B` |
| Show Commit Details | `⌘+Shift+G C` | `Ctrl+Shift+G C` |
| Show File History | `⌘+Shift+G H` | `Ctrl+Shift+G H` |
| Compare with Previous | `⌘+Shift+G [` | `Ctrl+Shift+G [` |
| Show Commit Graph | `⌘+Shift+G G` | `Ctrl+Shift+G G` |

---

## Common Git Workflows

### Daily Development Workflow

```bash
# 1. Start working
mamba activate prob-lab
cd /Users/pleiadian53/work/probability-lab

# 2. Check current status
git status

# 3. Create a new branch for feature (optional but recommended)
git checkout -b feature/new-distribution

# 4. Make changes to code
# ... edit files ...

# 5. See what changed
git diff

# 6. Stage and commit
git add prob_lab/distributions/new_dist.py
git commit -m "Add new distribution: Gamma"

# 7. Push to GitHub
git push -u origin feature/new-distribution

# 8. Create Pull Request (via GitHub or gh CLI)
gh pr create --title "Add Gamma distribution" --body "Implements Gamma distribution with MLE fitting"
```

### Updating Documentation

```bash
# 1. Make changes to docs
# ... edit docs/dependencies.md ...

# 2. Stage and commit
git add docs/dependencies.md
git commit -m "docs: Update dependencies with new packages"

# 3. Push
git push
```

### Syncing with Remote

```bash
# Pull latest changes from GitHub
git pull origin main

# Or if you have local changes
git stash          # Save local changes
git pull           # Get remote changes
git stash pop      # Reapply local changes
```

### Creating Releases

```bash
# 1. Update version in pyproject.toml
# version = "0.1.0" → "0.2.0"

# 2. Commit version bump
git add pyproject.toml
git commit -m "Bump version to 0.2.0"

# 3. Create tag
git tag -a v0.2.0 -m "Release v0.2.0: Add Bayesian inference support"

# 4. Push commits and tags
git push origin main
git push origin v0.2.0

# 5. Create GitHub release
gh release create v0.2.0 \
  --title "v0.2.0: Bayesian Inference Support" \
  --notes "Added PyMC integration for Bayesian parameter estimation"
```

### Viewing History

```bash
# View commit history
git log

# One-line format
git log --oneline

# With graph
git log --oneline --graph --all

# Filter by author
git log --author="Your Name"

# Filter by date
git log --since="2 weeks ago"

# Filter by file
git log -- docs/dependencies.md

# See what changed in a commit
git show <commit-hash>
```

---

## Troubleshooting

### Issue: "No repository detected" in GitLens

**Problem:** GitLens shows "No repository detected"

**Solution:**
```bash
# Verify git is initialized
ls -la .git

# If missing, initialize
git init
git branch -m main

# Reload VS Code
# Command Palette → "Developer: Reload Window"
```

### Issue: Authentication Failed

**Problem:** `git push` fails with authentication error

**Solution:**
```bash
# Re-authenticate with GitHub CLI
gh auth login

# Or use personal access token
# 1. Generate token: https://github.com/settings/tokens
# 2. Use token as password when prompted
```

### Issue: Remote Already Exists

**Problem:** `fatal: remote origin already exists`

**Solution:**
```bash
# Remove existing remote
git remote remove origin

# Add correct remote
git remote add origin https://github.com/YOUR_USERNAME/probability-lab.git
```

### Issue: Diverged Branches

**Problem:** Local and remote have diverged

**Solution:**
```bash
# Option 1: Pull and merge
git pull origin main

# Option 2: Pull and rebase (cleaner history)
git pull --rebase origin main

# Option 3: Force push (DANGEROUS - only if you're sure)
git push --force origin main
```

### Issue: Accidentally Committed Large Files

**Problem:** Committed files that should be ignored

**Solution:**
```bash
# Remove from git but keep locally
git rm --cached path/to/file

# Update .gitignore
echo "path/to/file" >> .gitignore

# Commit the removal
git add .gitignore
git commit -m "Remove large file from tracking"
```

### Issue: GitLens Not Showing Blame

**Problem:** Inline blame annotations not visible

**Solution:**
1. Check GitLens is enabled: Click GitLens icon in status bar
2. Check settings: `"gitlens.currentLine.enabled": true`
3. Reload window: Command Palette → "Developer: Reload Window"

---

## Best Practices

### Commit Messages

**Good commit messages:**
```bash
git commit -m "feat: Add Gamma distribution support"
git commit -m "fix: Correct MLE estimation for censored data"
git commit -m "docs: Update Hydra tutorial with multirun examples"
git commit -m "refactor: Simplify distribution registry"
git commit -m "test: Add unit tests for extreme value distributions"
```

**Conventional Commits format:**
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style (formatting, no logic change)
- `refactor:` - Code restructuring
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks

### Branch Strategy

**For solo development:**
```bash
# Work directly on main
git checkout main
# ... make changes ...
git commit -m "Add feature"
git push
```

**For collaborative development:**
```bash
# Create feature branches
git checkout -b feature/bayesian-inference
# ... make changes ...
git commit -m "Add PyMC integration"
git push -u origin feature/bayesian-inference
# Create PR on GitHub
```

### .gitignore Best Practices

Your `.gitignore` already covers:
- ✅ Python artifacts (`__pycache__/`, `*.pyc`)
- ✅ Package metadata (`*.egg-info/`)
- ✅ Virtual environments
- ✅ IDE files (`.vscode/`, `.idea/`)
- ✅ Data files (with exceptions for examples)
- ✅ Private notes (`dev/`)

**Keep it updated:**
```bash
# Add new patterns as needed
echo "outputs/" >> .gitignore
echo "*.log" >> .gitignore
git add .gitignore
git commit -m "Update .gitignore"
```

---

## Summary

### Quick Reference

**Initial Setup:**
```bash
git init
git branch -m main
git add .
git commit -m "Initial commit"
gh auth login
gh repo create probability-lab --public --source=. --remote=origin --push
```

**Daily Workflow:**
```bash
git status              # Check changes
git add .               # Stage changes
git commit -m "msg"     # Commit changes
git push                # Push to GitHub
```

**GitLens:**
- Install from VS Code Extensions
- View inline blame, file history, commit graph
- Use GitLens icon in Activity Bar
- Hover over lines for commit details

**Resources:**
- Git documentation: https://git-scm.com/doc
- GitHub CLI: https://cli.github.com/manual/
- GitLens: https://gitlens.amod.io/
- GitHub Guides: https://guides.github.com/

Your probability-lab project is now ready for GitHub! 🚀

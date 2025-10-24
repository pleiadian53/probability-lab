# Complete Environment Setup Guide

**Purpose**: Step-by-step instructions to replicate the exact development environment for the Probability Lab project on a new computer.

**Last Updated**: October 23, 2025  
**Environment**: `prob-lab` with Python 3.11  
**Package Manager**: Mamba (faster alternative to Conda)

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installing Miniforge](#installing-miniforge)
3. [Complete Installation Steps](#complete-installation-steps)
4. [Understanding Editable Mode](#understanding-editable-mode)
5. [Verification](#verification)
6. [Daily Development Workflow](#daily-development-workflow)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software
- **Git** - For cloning the repository
- **Miniforge** - Provides mamba package manager
- **Text editor or IDE** - VS Code, PyCharm, or similar

### System Requirements
- **OS**: macOS, Linux, or Windows
- **Disk Space**: ~2-3 GB for environment
- **Internet**: Required for downloading packages

---

## Installing Miniforge

Miniforge provides `mamba`, a faster reimplementation of conda.

### macOS (Apple Silicon or Intel)

```bash
# Download and run installer
curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
bash Miniforge3-$(uname)-$(uname -m).sh

# Follow prompts, then restart terminal
rm Miniforge3-$(uname)-$(uname -m).sh
```

### Linux

```bash
wget "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
bash Miniforge3-$(uname)-$(uname -m).sh
rm Miniforge3-$(uname)-$(uname -m).sh
```

### Windows
Download from: https://github.com/conda-forge/miniforge/releases  
Run `Miniforge3-Windows-x86_64.exe` and use "Miniforge Prompt" for commands.

### Verify Installation

```bash
mamba --version  # Should show version number
```

---

## Complete Installation Steps

### Step 0: Clone Repository

```bash
cd ~/work  # or your preferred location
git clone <repository-url> probability-lab
cd probability-lab
```

### Step 1: Create Environment

```bash
mamba create -n prob-lab python=3.11 pip -y
```

**What this does:**
- Creates isolated environment named `prob-lab`
- Installs Python 3.11 and pip
- Location: `~/miniforge3/envs/prob-lab/`

### Step 2: Activate Environment

```bash
mamba activate prob-lab
```

**Verify:**
```bash
which python  # Should show: .../miniforge3/envs/prob-lab/bin/python
python --version  # Should show: Python 3.11.x
```

### Step 3: Install Compiled Dependencies

```bash
mamba install -c conda-forge \
  numpy scipy pandas polars matplotlib plotly lifelines -y
```

**Why mamba for these?**
- Packages have C/Fortran extensions
- Better binary dependency resolution
- Especially important on Apple Silicon

**Time**: 2-5 minutes

### Step 4: Install Pure-Python Dependencies

```bash
pip install pydantic typer rich hydra-core omegaconf
```

**Why pip for these?**
- Pure Python, no compilation
- Often more up-to-date on PyPI

**Packages installed**:
- `pydantic`, `typer`, `rich` - Core utilities
- `hydra-core`, `omegaconf` - Experiment configuration management

**Time**: 30 seconds - 1 minute

### Step 5: Install in Editable Mode ⭐

```bash
cd /path/to/probability-lab
pip install -e .
```

**What this does:**
- Creates symbolic link from `site-packages` → your source code
- Changes are immediately available (no reinstall needed!)
- Package importable from anywhere

**Expected output:**
```
Successfully built probability-lab
Installing collected packages: probability-lab
Successfully installed probability-lab-0.1.0
```

**Time**: 10-30 seconds

### Step 6: Install Dev Tools (Optional)

```bash
pip install -e ".[dev]"
```

**Installs:**
- pytest (testing)
- black (formatter)
- ruff (linter)
- ipykernel (Jupyter support)

**Time**: 1-2 minutes

### Step 7: Optional Frameworks

**For PyTorch + Pyro:**
```bash
pip install -e ".[torch]"
```

**For PyMC + ArviZ:**
```bash
pip install -e ".[pymc]"
```

---

## Understanding Editable Mode

### What is `pip install -e .`?

The `-e` flag means "editable mode". Instead of copying files, pip creates a **symbolic link**.

### Traditional vs Editable Installation

#### Traditional (`pip install .`)
```
Your Code                        site-packages
───────────                      ─────────────
/path/to/probability-lab/        /env/lib/python3.11/site-packages/
├── prob_lab/                    ├── prob_lab/  ← COPIED
│   ├── __init__.py              │   ├── __init__.py
│   └── ...                      │   └── ...

❌ Changes require reinstall
```

#### Editable (`pip install -e .`)
```
Your Code                        site-packages
───────────                      ─────────────
/path/to/probability-lab/        /env/lib/python3.11/site-packages/
├── prob_lab/                    ├── probability-lab.egg-link
│   ├── __init__.py              │   (points to your source)
│   └── ...                      

✅ Changes immediately available
```

### How Python Finds Your Package

1. **Python's search path** (`sys.path`) automatically includes `site-packages`
   ```python
   import sys
   print([p for p in sys.path if 'site-packages' in p])
   # ['/path/to/miniforge3/envs/prob-lab/lib/python3.11/site-packages']
   ```

2. **The `.egg-link` file** in `site-packages` tells Python where to find your code:
   ```
   # Contents of probability-lab.egg-link
   /Users/pleiadian53/work/probability-lab
   .
   ```

3. **Result**: Import works from anywhere when environment is activated
   ```python
   # Works from any directory!
   from prob_lab.distributions import SomeDistribution
   ```

### Why This Matters for Development

```python
# 1. Edit your code
# File: prob_lab/distributions/my_dist.py
class MyDistribution:
    def fit(self, data):
        return "fitted!"

# 2. Use immediately (no reinstall!)
from prob_lab.distributions.my_dist import MyDistribution
dist = MyDistribution()
dist.fit([1, 2, 3])  # Works!

# 3. Make changes, save file

# 4. Reload (or restart Python)
import importlib
import prob_lab.distributions.my_dist
importlib.reload(prob_lab.distributions.my_dist)
```

### Key Benefits

✅ **Immediate feedback** - No reinstall after changes  
✅ **Works everywhere** - Import from any directory  
✅ **Jupyter integration** - Notebooks use latest code  
✅ **Testing integration** - Tests use latest code

### Package Discovery Configuration

In `pyproject.toml`, we specify what to include:

```toml
[tool.setuptools.packages.find]
where = ["."]
include = ["prob_lab*"]
exclude = ["dev*", "apps*", "scripts*", "examples*", "docs*"]
```

**Why?**
- Only `prob_lab/` is installed as a package
- Excludes utility directories
- Prevents "Multiple top-level packages" error

---

## Verification

### Check Installation

```bash
# Verify package is installed
pip list | grep probability-lab
# Output: probability-lab    0.1.0    /path/to/probability-lab

# Test import
python -c "import prob_lab; print('✓ Success')"

# Check location (should be your source directory!)
python -c "import prob_lab; print(prob_lab.__file__)"
# Output: /path/to/probability-lab/prob_lab/__init__.py
```

### Check Dependencies

```bash
python -c "import numpy, scipy, pandas, polars, matplotlib, plotly, lifelines, pydantic, typer, rich; print('✓ All loaded')"
```

### Test Editable Mode

```bash
# Create test file
echo 'def test(): return "Editable works!"' > prob_lab/test_editable.py

# Import without reinstall
python -c "from prob_lab.test_editable import test; print(test())"
# Output: Editable works!

# Clean up
rm prob_lab/test_editable.py
```

---

## Daily Development Workflow

### Start Work Session

```bash
mamba activate prob-lab
cd /path/to/probability-lab
```

### Make Changes

```bash
# Edit files - changes are immediately available!
vim prob_lab/distributions/my_dist.py
```

### Test Changes

**Option 1: Python REPL**
```bash
python
>>> from prob_lab.distributions import MyDistribution
>>> dist = MyDistribution()
```

**Option 2: Run script**
```bash
python scripts/test_script.py
```

**Option 3: Jupyter**
```bash
jupyter notebook
# Changes available immediately in notebooks
```

**Option 4: Tests**
```bash
pytest                              # All tests
pytest tests/test_distributions.py  # Specific file
pytest -v                           # Verbose
```

### Code Quality

```bash
black prob_lab/              # Format code
ruff check prob_lab/         # Lint
ruff check --fix prob_lab/   # Auto-fix
```

### Reload in Running Python

```python
# If Python is already running
import importlib
import prob_lab.your_module
importlib.reload(prob_lab.your_module)

# Or restart Python/Jupyter kernel (easier!)
```

### End Session

```bash
git add .
git commit -m "Your changes"
git push
mamba deactivate  # Optional
```

---

## Troubleshooting

### Can't Import prob_lab

```bash
# Check environment
which python  # Should show prob-lab environment

# Check installation
pip list | grep probability-lab

# Reinstall if needed
cd /path/to/probability-lab
pip install -e .
```

### Changes Not Reflected

```python
# Reload module
import importlib
import prob_lab.your_module
importlib.reload(prob_lab.your_module)

# Or restart Python/Jupyter
```

### Multiple Top-Level Packages Error

Ensure `pyproject.toml` has:
```toml
[tool.setuptools.packages.find]
where = ["."]
include = ["prob_lab*"]
exclude = ["dev*", "apps*", "scripts*", "examples*", "docs*"]
```

Then: `pip install -e .`

### Missing Dependencies

```bash
# Reinstall dependencies
mamba install -c conda-forge numpy scipy pandas polars matplotlib plotly lifelines -y
pip install pydantic typer rich hydra-core omegaconf
pip install -e .
```

### Mamba Not Found

```bash
# Initialize shell
conda init zsh  # or bash
# Restart terminal

# Or use conda instead
conda activate prob-lab
```

---

## Quick Reference

### Environment Commands
```bash
mamba env list                 # List environments
mamba activate prob-lab        # Activate
mamba deactivate              # Deactivate
mamba env remove -n prob-lab  # Delete
```

### Package Commands
```bash
pip list                      # List packages
pip show probability-lab      # Package details
pip install -e .              # Editable install
pip install -e ".[dev]"       # With dev tools
```

### Development Commands
```bash
pytest                        # Run tests
black prob_lab/              # Format
ruff check prob_lab/         # Lint
python -m prob_lab.module    # Run module
```

---

## Complete Setup Script

Save as `setup_environment.sh`:

```bash
#!/bin/bash
set -e

echo "Creating environment..."
mamba create -n prob-lab python=3.11 pip -y

echo "Activating..."
eval "$(conda shell.bash hook)"
mamba activate prob-lab

echo "Installing compiled dependencies..."
mamba install -c conda-forge numpy scipy pandas polars matplotlib plotly lifelines -y

echo "Installing pure-Python dependencies..."
pip install pydantic typer rich hydra-core omegaconf

echo "Installing in editable mode..."
pip install -e .

echo "Installing dev tools..."
pip install -e ".[dev]"

echo "Verifying..."
python -c "import prob_lab; print('✓ Success')"

echo ""
echo "Setup complete! Activate with: mamba activate prob-lab"
```

Usage:
```bash
chmod +x setup_environment.sh
./setup_environment.sh
```

---

## Summary

**Key Concept**: Editable mode (`pip install -e .`) creates a symbolic link from your environment's `site-packages` to your source code, making changes immediately available without reinstalling.

**Installation Order**:
1. Create environment with Python 3.11
2. Install compiled deps via mamba (numpy, scipy, etc.)
3. Install pure-Python deps via pip (pydantic, typer, rich)
4. Install your package in editable mode: `pip install -e .`
5. Optional: Install dev tools with `pip install -e ".[dev]"`

**Daily Workflow**:
- Activate environment: `mamba activate prob-lab`
- Edit code → changes immediately available
- Test with Python/Jupyter/pytest
- No reinstall needed!

**For more details**, see:
- `docs/installation.md` - Detailed installation guide
- `docs/quick-start.md` - Quick reference
- `docs/setup-summary.md` - Setup decisions and rationale

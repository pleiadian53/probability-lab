# Setup Replication Guide

**Quick reference for setting up this project on a new computer.**

---

## Prerequisites

1. Install [Miniforge](https://github.com/conda-forge/miniforge) (provides mamba)
2. Clone this repository
3. Have ~2-3 GB disk space available

---

## Complete Setup (5-10 minutes)

```bash
# 1. Navigate to project
cd /path/to/probability-lab

# 2. Create environment
mamba create -n prob-lab python=3.11 pip -y

# 3. Activate environment
mamba activate prob-lab

# 4. Install compiled dependencies (via mamba)
mamba install -c conda-forge \
  numpy scipy pandas polars matplotlib plotly lifelines -y

# 5. Install pure-Python dependencies (via pip)
pip install pydantic typer rich hydra-core omegaconf

# 6. Install this package in editable mode
pip install -e .

# 7. Install development tools (optional)
pip install -e ".[dev]"

# 8. Verify installation
python -c "import prob_lab; print('✓ Success!')"
python -c "import prob_lab; print(f'Location: {prob_lab.__file__}')"
```

---

## What is Editable Mode?

**Command**: `pip install -e .`

**What it does**: Creates a symbolic link from your environment's `site-packages` to your source code.

**Why it matters**: 
- ✅ Code changes are **immediately available** (no reinstall needed)
- ✅ Package is **importable from anywhere**: `from prob_lab import ...`
- ✅ Works with **Jupyter notebooks** automatically
- ✅ **Tests use latest code** automatically

**How it works**:
```
Your Source Code                    site-packages
────────────────                    ─────────────
/path/to/probability-lab/           /env/lib/python3.11/site-packages/
├── prob_lab/  ← SOURCE             ├── probability-lab.egg-link
│   ├── __init__.py                 │   (points to your source)
│   └── ...                         └── (Python imports from YOUR source!)
```

---

## Daily Workflow

```bash
# Start work
mamba activate prob-lab
cd /path/to/probability-lab

# Edit code
vim prob_lab/distributions/my_file.py

# Test immediately (no reinstall!)
python -c "from prob_lab.distributions import ..."
# OR
pytest
# OR
jupyter notebook
```

---

## Why This Approach?

### Hybrid Package Management

**Mamba for compiled libraries**:
- numpy, scipy, pandas, polars, matplotlib, plotly, lifelines
- Better binary dependency resolution
- Especially important on Apple Silicon Macs

**pip for pure-Python packages**:
- pydantic, typer, rich
- Often more up-to-date on PyPI
- Simpler dependency chains

**pip with `-e` for our package**:
- Enables active development workflow
- Changes immediately available

### Package Configuration

In `pyproject.toml`:
```toml
[tool.setuptools.packages.find]
where = ["."]
include = ["prob_lab*"]
exclude = ["dev*", "apps*", "scripts*", "examples*", "docs*"]
```

This ensures only `prob_lab/` is installed as a package.

---

## Verification

```bash
# Check environment
which python
# Should show: .../miniforge3/envs/prob-lab/bin/python

# Check package location (should be your source directory!)
python -c "import prob_lab; print(prob_lab.__file__)"
# Should show: /path/to/probability-lab/prob_lab/__init__.py

# Check all dependencies
python -c "import numpy, scipy, pandas, polars, matplotlib, plotly, lifelines, pydantic, typer, rich; print('✓ All loaded')"
```

---

## Troubleshooting

### Can't import prob_lab
```bash
mamba activate prob-lab
cd /path/to/probability-lab
pip install -e .
```

### Changes not reflected
```python
# In Python/Jupyter
import importlib
import prob_lab.your_module
importlib.reload(prob_lab.your_module)
# Or restart Python/Jupyter kernel
```

### Multiple top-level packages error
Ensure `pyproject.toml` has the package discovery configuration above, then:
```bash
pip install -e .
```

---

## Complete Documentation

For detailed explanations, see:

- **[docs/environment-setup-guide.md](docs/environment-setup-guide.md)** - Complete step-by-step guide
- **[docs/editable-mode-deep-dive.md](docs/editable-mode-deep-dive.md)** - Technical details of editable mode
- **[docs/quick-start.md](docs/quick-start.md)** - Quick reference
- **[docs/installation.md](docs/installation.md)** - Detailed installation guide
- **[docs/README.md](docs/README.md)** - Documentation index

---

## Key Files

- `pyproject.toml` - Project configuration and dependencies
- `.gitignore` - Excludes `dev/` and Python artifacts
- `requirements.txt` - Dependency list (reference only)
- `docs/` - All documentation

---

## Project Structure

```
probability-lab/
├── prob_lab/              # Main package (installed in editable mode)
│   ├── distributions/     # Distribution implementations
│   ├── survival/          # Survival analysis
│   ├── timeseries/        # Time series analysis
│   ├── fitting/           # Distribution fitting
│   └── visualize/         # Visualization
├── scripts/               # Utility scripts (NOT installed)
├── apps/                  # Applications (NOT installed)
├── examples/              # Example data (NOT installed)
├── docs/                  # Documentation (NOT installed)
├── dev/                   # Dev notes (gitignored, NOT installed)
└── pyproject.toml         # Configuration
```

Only `prob_lab/` is installed. Everything else stays in your project directory.

---

## Summary

**The key insight**: `pip install -e .` creates a link (not a copy) from `site-packages` to your source code, making development seamless.

**Result**: Edit code → Test immediately → No reinstall needed!

This is the standard professional workflow for Python package development.

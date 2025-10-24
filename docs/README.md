# Project Documentation

This directory contains project-level documentation for the Probability Lab project.

## Quick Start

**New to this project?** Start here:

1. 📦 **[Environment Setup Guide](environment-setup-guide.md)** - Complete setup instructions for new computers
2. ⚡ **[Quick Start](quick-start.md)** - TL;DR for daily workflow
3. 🔧 **[Installation Guide](installation.md)** - Detailed installation with explanations

## Documentation Index

### Setup & Installation

| Document | Purpose | Audience |
|----------|---------|----------|
| **[Environment Setup Guide](environment-setup-guide.md)** | Complete step-by-step setup for new computers | New developers |
| **[Installation Guide](installation.md)** | Detailed installation with explanations | All developers |
| **[Quick Start](quick-start.md)** | Quick reference for daily workflow | Experienced developers |
| **[Setup Summary](setup-summary.md)** | What was done and why | Reference |

### Technical Deep Dives

| Document | Purpose | Audience |
|----------|---------|----------|
| **[Dependencies Guide](dependencies.md)** | Complete reference for all project dependencies | All developers |
| **[Editable Mode Deep Dive](editable-mode-deep-dive.md)** | How `pip install -e .` works technically | Curious developers |
| **[GitHub Setup Guide](github-setup.md)** | Publishing to GitHub and using GitLens | All developers |
| **[Hydra Configuration Guide](hydra/README.md)** | Experiment management with Hydra | All developers |
| **[Hydra Tutorial](hydra/tutorial.md)** | Step-by-step Hydra examples | New to Hydra |

### Key Concepts

#### Editable Mode (`pip install -e .`)

The most important concept for active development:

- **What**: Creates symbolic link from `site-packages` to your source code
- **Why**: Changes are immediately available without reinstalling
- **How**: See [Editable Mode Deep Dive](editable-mode-deep-dive.md)
- **When**: Always use for active development

#### Hybrid Package Management

We use both mamba and pip:

- **Mamba**: For compiled libraries (numpy, scipy, matplotlib)
  - Better binary dependency resolution
  - Especially important on Apple Silicon
  
- **pip**: For pure-Python packages (pydantic, typer, rich)
  - Often more up-to-date
  - Simpler for packages without compiled extensions

## Documentation Structure

This project maintains three levels of documentation:

### 1. Project-Level (`/docs`) ← You are here

High-level project documentation:
- Setup and installation guides
- Architecture and design decisions
- Contributing guidelines
- API reference (future)

### 2. Package-Level (`/prob_lab/*/docs`)

Module-specific documentation:
- `/prob_lab/distributions/docs` - Distribution implementations
- `/prob_lab/survival/docs` - Survival analysis tools
- `/prob_lab/timeseries/docs` - Time series analysis
- `/prob_lab/fitting/docs` - Distribution fitting utilities

### 3. Development Notes (`/dev`)

Private development notes (gitignored, not version controlled):
- Development diaries
- Temporary notes and memos
- Experimental ideas
- Not meant for public sharing

## Common Tasks

### First Time Setup

```bash
# See environment-setup-guide.md for complete instructions
mamba create -n prob-lab python=3.11 pip -y
mamba activate prob-lab
mamba install -c conda-forge numpy scipy pandas polars matplotlib plotly lifelines -y
pip install pydantic typer rich hydra-core omegaconf
cd /path/to/probability-lab
pip install -e .
pip install -e ".[dev]"
```

### Daily Workflow

```bash
# Activate environment
mamba activate prob-lab

# Make changes to code
# Changes are immediately available!

# Test
pytest

# Format and lint
black prob_lab/
ruff check prob_lab/
```

### Verification

```bash
# Check installation
python -c "import prob_lab; print(prob_lab.__file__)"
# Should show: /path/to/probability-lab/prob_lab/__init__.py

# Check dependencies
python -c "import numpy, scipy, pandas; print('✓ All loaded')"
```

## Environment Details

**Environment Name**: `prob-lab`  
**Python Version**: 3.11  
**Package Manager**: Mamba (conda-forge)  
**Installation Mode**: Editable (`pip install -e .`)

### Core Dependencies

- **numpy, scipy** - Numerical/scientific computing
- **pandas, polars** - Data manipulation
- **matplotlib, plotly** - Visualization
- **lifelines** - Survival analysis
- **pydantic** - Data validation
- **typer, rich** - CLI framework
- **hydra-core, omegaconf** - Experiment configuration management

### Development Tools

- **pytest** - Testing framework
- **black** - Code formatter
- **ruff** - Fast linter
- **ipykernel** - Jupyter support

## Getting Help

### Documentation

1. Check the relevant guide in this directory
2. Check package-level docs in `/prob_lab/*/docs`
3. Check the main [README](../README.md)

### Troubleshooting

Common issues and solutions:

**Can't import prob_lab**
```bash
mamba activate prob-lab
pip install -e .
```

**Changes not reflected**
```python
import importlib
import prob_lab.your_module
importlib.reload(prob_lab.your_module)
# Or restart Python/Jupyter
```

**Multiple top-level packages error**
- Ensure `pyproject.toml` has correct `[tool.setuptools.packages.find]` configuration
- See [Environment Setup Guide](environment-setup-guide.md#troubleshooting)

### More Help

- See [Troubleshooting](environment-setup-guide.md#troubleshooting) section
- Check [Quick Reference](quick-start.md#troubleshooting)

## Contributing

(Future: Add contributing guidelines here)

## Related Files

- `../pyproject.toml` - Project configuration
- `../requirements.txt` - Dependency list (reference)
- `../.gitignore` - Git ignore rules
- `../README.md` - Project README

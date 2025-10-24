# Installation Guide

This guide covers the installation process for the Probability Lab project using mamba for environment management.

## Prerequisites

- [Miniforge](https://github.com/conda-forge/miniforge) or [Mambaforge](https://github.com/conda-forge/miniforge) installed
- Python 3.9 or higher

## Installation Steps

### 1. Create the Environment

Create a new mamba environment with Python 3.11:

```bash
mamba create -n prob-lab python=3.11 pip -y
```

### 2. Activate the Environment

```bash
mamba activate prob-lab
```

### 3. Install Compiled Dependencies

Install packages with C/Fortran extensions via mamba (recommended for better dependency resolution, especially on Apple Silicon):

```bash
mamba install -c conda-forge \
  numpy scipy pandas polars matplotlib plotly lifelines -y
```

**Why mamba for these packages?**
- Packages like `scipy`, `matplotlib`, and `pandas` have compiled extensions
- Mamba handles binary dependencies and platform-specific builds better than pip
- Avoids wheel-building errors, especially on M1/M2 Macs

### 4. Install Pure-Python Dependencies

Install pure-Python packages via pip:

```bash
pip install pydantic typer rich
```

### 5. Install probability-lab in Editable Mode

Navigate to the project directory and install in editable mode:

```bash
cd /Users/pleiadian53/work/probability-lab
pip install -e .
```

**What does `-e` (editable mode) do?**
- Creates a symbolic link from your environment's `site-packages` to your local source code
- Code changes are immediately available without reinstalling
- Allows you to import the package from anywhere: `from prob_lab.distributions import ...`

### 6. Install Development Tools (Optional)

Install development dependencies (pytest, black, ruff, ipykernel):

```bash
pip install -e ".[dev]"
```

### 7. Install Probabilistic Programming Frameworks (Optional)

Choose one or both based on your needs:

**For PyTorch + Pyro:**
```bash
pip install -e ".[torch]"
```

**For PyMC + ArviZ:**
```bash
pip install -e ".[pymc]"
```

## Verification

Verify the installation by importing the package:

```bash
python -c "import prob_lab; print('Success!')"
```

Check that all core dependencies are available:

```bash
python -c "import numpy, scipy, pandas, polars, matplotlib, plotly, lifelines, pydantic, typer, rich; print('All dependencies loaded!')"
```

## Package Location

With editable mode, your package is installed as a link:

```bash
python -c "import prob_lab; print(prob_lab.__file__)"
# Output: /Users/pleiadian53/work/probability-lab/prob_lab/__init__.py
```

This confirms that Python is using your local source code, not a copy in `site-packages`.

## Troubleshooting

### Multiple Top-Level Packages Error

If you encounter an error about multiple top-level packages during `pip install -e .`, ensure your `pyproject.toml` includes:

```toml
[tool.setuptools.packages.find]
where = ["."]
include = ["prob_lab*"]
exclude = ["dev*", "apps*", "scripts*", "examples*", "docs*"]
```

This explicitly tells setuptools to only include the `prob_lab` package and exclude other directories.

### Environment Not Found

If `mamba activate prob-lab` fails, ensure:
1. Miniforge/Mambaforge is properly installed
2. Your shell is configured for conda/mamba (run `mamba init`)
3. Restart your terminal after initialization

## Updating Dependencies

To update dependencies in the future:

```bash
# Update mamba packages
mamba update -c conda-forge numpy scipy pandas polars matplotlib plotly lifelines

# Update pip packages
pip install --upgrade pydantic typer rich

# Reinstall the package (if dependencies changed)
pip install -e .
```

## Deactivating the Environment

When you're done working:

```bash
mamba deactivate
```

## Removing the Environment

To completely remove the environment:

```bash
mamba env remove -n prob-lab
```

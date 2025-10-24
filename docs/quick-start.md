# Quick Start Guide

## TL;DR - Complete Installation

```bash
# Create and activate environment
mamba create -n prob-lab python=3.11 pip -y
mamba activate prob-lab

# Install compiled dependencies
mamba install -c conda-forge numpy scipy pandas polars matplotlib plotly lifelines -y

# Install pure-Python dependencies
pip install pydantic typer rich hydra-core omegaconf

# Install probability-lab in editable mode
cd /Users/pleiadian53/work/probability-lab
pip install -e .

# Optional: Install dev tools
pip install -e ".[dev]"

# Verify installation
python -c "import prob_lab; print('✓ Success!')"
```

## Daily Workflow

### Starting Work

```bash
# Activate environment
mamba activate prob-lab

# Navigate to project
cd /Users/pleiadian53/work/probability-lab
```

### Working with the Code

Since the package is installed in **editable mode** (`pip install -e .`):

- ✅ Edit any file in `prob_lab/` and changes are immediately available
- ✅ No need to reinstall after code changes
- ✅ Import from anywhere: `from prob_lab.distributions import ...`

### Running Scripts

```bash
# Run a script
python scripts/your_script.py

# Run with module syntax
python -m prob_lab.fit_demo

# Run tests (if installed with [dev])
pytest
```

### Ending Work

```bash
# Deactivate environment
mamba deactivate
```

## Project Structure

```
probability-lab/
├── prob_lab/              # Main package (installed in editable mode)
│   ├── distributions/     # Distribution implementations
│   ├── survival/          # Survival analysis tools
│   ├── timeseries/        # Time series analysis
│   ├── fitting/           # Distribution fitting utilities
│   └── visualize/         # Visualization tools
├── scripts/               # General-purpose scripts
├── apps/                  # Applications (e.g., Streamlit)
├── examples/              # Example data and notebooks
├── docs/                  # Project documentation
├── dev/                   # Development notes (gitignored)
└── pyproject.toml         # Project configuration
```

## Common Tasks

### Import the Package

```python
# Import the main package
import prob_lab

# Import specific modules
from prob_lab.distributions import ...
from prob_lab.survival import ...
from prob_lab.fitting import ...
```

### Run Jupyter Notebook

```bash
# Start Jupyter (if ipykernel is installed)
jupyter notebook

# Or use VS Code's built-in Jupyter support
```

### Format Code

```bash
# Format with black (if installed with [dev])
black prob_lab/

# Lint with ruff
ruff check prob_lab/
```

### Run Tests

```bash
# Run all tests (if pytest is installed with [dev])
pytest

# Run specific test file
pytest tests/test_distributions.py

# Run with verbose output
pytest -v
```

## Key Concepts

### Editable Mode (`pip install -e .`)

- Creates a **symbolic link** from `site-packages` → your source code
- Changes to code are **immediately visible** (no reinstall needed)
- Package behaves like it's installed, but uses your local files

### Why Mamba + pip?

- **Mamba**: For compiled libraries (numpy, scipy, matplotlib)
  - Better dependency resolution
  - Handles binary dependencies
  - Faster than conda
  
- **pip**: For pure-Python packages (pydantic, typer, rich)
  - Often more up-to-date
  - Simpler for packages without compiled extensions

### site-packages

- Automatically included in Python's module search path (`sys.path`)
- Where pip/mamba install packages
- Editable install adds a `.egg-link` file pointing to your source code

## Troubleshooting

### Can't import prob_lab

```bash
# Check if environment is activated
which python  # Should show path to prob-lab environment

# Verify installation
pip list | grep probability-lab

# Check import path
python -c "import prob_lab; print(prob_lab.__file__)"
```

### Changes not reflected

If using editable mode and changes aren't visible:

```python
# In Python/Jupyter, reload the module
import importlib
import prob_lab.distributions
importlib.reload(prob_lab.distributions)
```

### Environment issues

```bash
# List all environments
mamba env list

# Recreate environment if needed
mamba env remove -n prob-lab
# Then follow installation steps again
```

## Next Steps

- Read the [Installation Guide](installation.md) for detailed explanations
- Explore package-level documentation in `prob_lab/*/docs/`
- Check out examples in `examples/`
- Review the main [README](../README.md)

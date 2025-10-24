# Project Dependencies

**Complete reference for all dependencies used in probability-lab**

---

## Table of Contents

1. [Overview](#overview)
2. [Core Dependencies](#core-dependencies)
3. [Development Dependencies](#development-dependencies)
4. [Optional Dependencies](#optional-dependencies)
5. [Dependency Management](#dependency-management)
6. [Version Requirements](#version-requirements)

---

## Overview

The probability-lab project uses a **hybrid dependency management** approach:

- **Compiled libraries** (numpy, scipy, matplotlib, etc.) → Installed via **mamba/conda**
- **Pure-Python packages** (pydantic, typer, hydra, etc.) → Installed via **pip**
- **Optional frameworks** (PyTorch, PyMC) → Installed on-demand

This approach ensures:
- ✅ Optimal binary dependency resolution (especially on Apple Silicon)
- ✅ Fast installation times
- ✅ Flexibility for different use cases

---

## Core Dependencies

### Numerical Computing

#### **NumPy** (`numpy>=1.24`)
- **Purpose**: Fundamental package for numerical computing in Python
- **Use Cases**:
  - Array operations and linear algebra
  - Random number generation
  - Foundation for scipy, pandas, and other scientific packages
- **Why Required**: Core data structure for all numerical operations
- **Installation**: `mamba install -c conda-forge numpy`
- **Documentation**: https://numpy.org/doc/

#### **SciPy** (`scipy>=1.11`)
- **Purpose**: Scientific computing and technical computing
- **Use Cases**:
  - Statistical distributions (scipy.stats)
  - Optimization and fitting algorithms
  - Special functions
  - Integration and interpolation
- **Why Required**: Provides all probability distributions and MLE fitting
- **Installation**: `mamba install -c conda-forge scipy`
- **Documentation**: https://docs.scipy.org/

### Data Manipulation

#### **Pandas** (`pandas>=2.0`)
- **Purpose**: Data manipulation and analysis
- **Use Cases**:
  - Loading CSV/Excel files
  - Data cleaning and preprocessing
  - Time series operations
  - Survival data handling
- **Why Required**: Primary data structure for tabular data
- **Installation**: `mamba install -c conda-forge pandas`
- **Documentation**: https://pandas.pydata.org/docs/

#### **Polars** (`polars>=1.5.0`)
- **Purpose**: Fast DataFrame library (Rust-based)
- **Use Cases**:
  - High-performance data processing
  - Large dataset handling
  - Lazy evaluation for complex queries
  - Alternative to pandas for speed-critical operations
- **Why Required**: Performance optimization for large datasets
- **Installation**: `mamba install -c conda-forge polars`
- **Documentation**: https://pola-rs.github.io/polars/

### Visualization

#### **Matplotlib** (`matplotlib>=3.8`)
- **Purpose**: Comprehensive plotting library
- **Use Cases**:
  - PDF/CDF plots
  - QQ plots and PP plots
  - Histograms and density plots
  - Publication-quality figures
- **Why Required**: Core plotting functionality
- **Installation**: `mamba install -c conda-forge matplotlib`
- **Documentation**: https://matplotlib.org/stable/

#### **Plotly** (`plotly>=5.20`)
- **Purpose**: Interactive plotting library
- **Use Cases**:
  - Interactive visualizations
  - Web-based dashboards
  - 3D plots
  - Hover tooltips and zoom
- **Why Required**: Interactive exploration in Streamlit app
- **Installation**: `mamba install -c conda-forge plotly`
- **Documentation**: https://plotly.com/python/

### Domain-Specific

#### **Lifelines** (`lifelines>=0.28`)
- **Purpose**: Survival analysis library
- **Use Cases**:
  - Kaplan-Meier estimation
  - Cox proportional hazards models
  - Parametric survival models (Weibull, log-normal, etc.)
  - Time-to-event analysis
- **Why Required**: Specialized survival analysis functionality
- **Installation**: `mamba install -c conda-forge lifelines`
- **Documentation**: https://lifelines.readthedocs.io/

### Utilities

#### **Pydantic** (`pydantic>=2.6`)
- **Purpose**: Data validation using Python type annotations
- **Use Cases**:
  - Configuration validation
  - Data model definitions
  - Type checking at runtime
  - API request/response validation
- **Why Required**: Ensures data integrity and type safety
- **Installation**: `pip install pydantic`
- **Documentation**: https://docs.pydantic.dev/

#### **Typer** (`typer>=0.12.3`)
- **Purpose**: CLI application framework
- **Use Cases**:
  - Command-line interfaces
  - Argument parsing
  - Help text generation
  - Type-safe CLI commands
- **Why Required**: Powers CLI tools like `fit_demo`
- **Installation**: `pip install typer`
- **Documentation**: https://typer.tiangolo.com/

#### **Rich** (`rich>=13.7`)
- **Purpose**: Rich text and formatting for terminal
- **Use Cases**:
  - Colored output
  - Progress bars
  - Tables and panels
  - Syntax highlighting
- **Why Required**: Enhanced CLI user experience
- **Installation**: `pip install rich`
- **Documentation**: https://rich.readthedocs.io/

### Configuration Management

#### **Hydra** (`hydra-core>=1.3`)
- **Purpose**: Framework for elegantly configuring complex applications
- **Use Cases**:
  - Composable YAML configurations
  - Command-line overrides
  - Experiment management
  - Multi-run sweeps
- **Why Required**: Manages experiment configurations
- **Installation**: `pip install hydra-core`
- **Documentation**: https://hydra.cc/docs/intro/

#### **OmegaConf** (`omegaconf>=2.3`)
- **Purpose**: YAML-based configuration system
- **Use Cases**:
  - Configuration parsing
  - Variable interpolation
  - Type-safe config access
  - Merging configurations
- **Why Required**: Backend for Hydra configurations
- **Installation**: `pip install omegaconf`
- **Documentation**: https://omegaconf.readthedocs.io/

---

## Development Dependencies

These are installed with `pip install -e ".[dev]"`:

### Testing

#### **pytest** (`pytest`)
- **Purpose**: Testing framework
- **Use Cases**:
  - Unit tests
  - Integration tests
  - Fixtures and parametrization
  - Test coverage
- **Installation**: Included in `[dev]` extras
- **Documentation**: https://docs.pytest.org/

### Code Quality

#### **Black** (`black`)
- **Purpose**: Opinionated code formatter
- **Use Cases**:
  - Automatic code formatting
  - Consistent style across project
  - PEP 8 compliance
- **Installation**: Included in `[dev]` extras
- **Documentation**: https://black.readthedocs.io/

#### **Ruff** (`ruff`)
- **Purpose**: Fast Python linter
- **Use Cases**:
  - Code linting
  - Import sorting
  - Error detection
  - Style checking
- **Installation**: Included in `[dev]` extras
- **Documentation**: https://docs.astral.sh/ruff/

### Jupyter Support

#### **ipykernel** (`ipykernel`)
- **Purpose**: IPython kernel for Jupyter
- **Use Cases**:
  - Jupyter notebooks
  - Interactive development
  - Exploratory data analysis
  - Documentation notebooks
- **Installation**: Included in `[dev]` extras
- **Documentation**: https://ipython.readthedocs.io/

---

## Optional Dependencies

### Probabilistic Programming (PyTorch)

Install with `pip install -e ".[torch]"`:

#### **PyTorch** (`torch>=2.1`)
- **Purpose**: Deep learning framework
- **Use Cases**:
  - Neural networks
  - GPU acceleration
  - Automatic differentiation
  - Tensor operations
- **Documentation**: https://pytorch.org/docs/

#### **Pyro** (`pyro-ppl>=1.9`)
- **Purpose**: Probabilistic programming on PyTorch
- **Use Cases**:
  - Bayesian inference
  - Variational inference
  - Stochastic variational inference (SVI)
  - Deep probabilistic models
- **Documentation**: https://pyro.ai/

### Probabilistic Programming (PyMC)

Install with `pip install -e ".[pymc]"`:

#### **PyMC** (`pymc>=5.13`)
- **Purpose**: Bayesian statistical modeling
- **Use Cases**:
  - MCMC sampling
  - Bayesian inference
  - Hierarchical models
  - Model comparison
- **Documentation**: https://www.pymc.io/

#### **ArviZ** (`arviz>=0.17`)
- **Purpose**: Exploratory analysis of Bayesian models
- **Use Cases**:
  - Posterior visualization
  - Model diagnostics
  - Trace plots
  - Posterior predictive checks
- **Documentation**: https://arviz-devs.github.io/arviz/

---

## Dependency Management

### Installation Methods

#### Method 1: Using environment.yml (Recommended)

```bash
mamba env create -f environment.yml
mamba activate probability-lab
pip install -e .
pip install -e ".[dev]"  # Optional
```

**Advantages**:
- Single command setup
- Reproducible environments
- Handles all conda packages

#### Method 2: Manual Installation

```bash
# Create environment
mamba create -n prob-lab python=3.11 pip -y
mamba activate prob-lab

# Install compiled dependencies
mamba install -c conda-forge \
  numpy scipy pandas polars matplotlib plotly lifelines -y

# Install pure-Python dependencies
pip install pydantic typer rich hydra-core omegaconf

# Install package
pip install -e .
```

**Advantages**:
- More control over versions
- Can skip optional dependencies
- Better for troubleshooting

#### Method 3: Using requirements.txt

```bash
pip install -r requirements.txt
pip install -e .
```

**Note**: This installs everything via pip, which may not optimize binary dependencies as well as conda/mamba.

### Dependency Groups

| Group | Installation | Purpose |
|-------|--------------|---------|
| **Core** | `pip install -e .` | Required for basic functionality |
| **Dev** | `pip install -e ".[dev]"` | Development tools (testing, linting) |
| **PyTorch** | `pip install -e ".[torch]"` | Pyro probabilistic programming |
| **PyMC** | `pip install -e ".[pymc]"` | PyMC Bayesian inference |

---

## Version Requirements

### Why These Versions?

#### Minimum Versions

- **numpy>=1.24**: Required for modern array API
- **pandas>=2.0**: Major performance improvements and new features
- **scipy>=1.11**: Latest statistical distributions and optimizations
- **matplotlib>=3.8**: Modern plotting features
- **python>=3.9**: Type hints and modern syntax support

#### Compatibility

All dependencies are tested on:
- ✅ **macOS** (Intel and Apple Silicon)
- ✅ **Linux** (x86_64)
- ✅ **Windows** (x86_64)

### Updating Dependencies

#### Check for Updates

```bash
# Check outdated packages
pip list --outdated

# Check conda packages
mamba list --outdated
```

#### Update Safely

```bash
# Update specific package
mamba update numpy
pip install --upgrade pydantic

# Update all (be careful!)
mamba update --all
pip install --upgrade -r requirements.txt
```

#### Test After Updates

```bash
# Run tests
pytest

# Verify imports
python -c "import prob_lab; print('✓ OK')"
```

---

## Dependency Tree

### Core Dependencies

```
probability-lab
├── numpy (numerical computing)
│   └── (no Python deps)
├── scipy (scientific computing)
│   └── numpy
├── pandas (data manipulation)
│   ├── numpy
│   └── python-dateutil
├── polars (fast dataframes)
│   └── (Rust-based, minimal deps)
├── matplotlib (plotting)
│   ├── numpy
│   ├── pillow
│   └── cycler
├── plotly (interactive plots)
│   └── (minimal deps)
├── lifelines (survival analysis)
│   ├── numpy
│   ├── scipy
│   ├── pandas
│   └── autograd
├── pydantic (validation)
│   └── typing-extensions
├── typer (CLI)
│   ├── click
│   └── rich (optional)
├── rich (terminal formatting)
│   ├── markdown-it-py
│   └── pygments
├── hydra-core (config management)
│   ├── omegaconf
│   ├── antlr4-python3-runtime
│   └── packaging
└── omegaconf (config parsing)
    └── PyYAML
```

### Development Dependencies

```
dev extras
├── pytest (testing)
│   ├── pluggy
│   └── iniconfig
├── black (formatting)
│   ├── click
│   └── platformdirs
├── ruff (linting)
│   └── (Rust-based, minimal deps)
└── ipykernel (Jupyter)
    ├── ipython
    ├── jupyter-client
    └── traitlets
```

---

## Troubleshooting Dependencies

### Common Issues

#### Issue: Import Errors

```python
ImportError: No module named 'numpy'
```

**Solution**:
```bash
mamba activate prob-lab
pip install -e .
```

#### Issue: Version Conflicts

```
ERROR: pip's dependency resolver does not currently take into account all the packages that are installed.
```

**Solution**:
```bash
# Create fresh environment
mamba env remove -n prob-lab
mamba env create -f environment.yml
```

#### Issue: Compilation Errors (scipy, numpy)

```
error: command 'gcc' failed with exit status 1
```

**Solution**: Use conda/mamba instead of pip for compiled packages:
```bash
mamba install -c conda-forge numpy scipy matplotlib
```

#### Issue: Apple Silicon (M1/M2) Compatibility

**Solution**: All dependencies have native ARM64 builds via conda-forge:
```bash
mamba install -c conda-forge <package>
```

### Checking Dependencies

```bash
# List installed packages
pip list
mamba list

# Show package details
pip show numpy
mamba info numpy

# Check dependency tree
pip install pipdeptree
pipdeptree -p probability-lab
```

---

## Best Practices

### 1. Pin Versions for Reproducibility

In `environment.yml` or `requirements.txt`, specify exact versions for production:

```yaml
# Development (flexible)
dependencies:
  - numpy>=1.24

# Production (pinned)
dependencies:
  - numpy==1.24.3
```

### 2. Separate Environments

```bash
# Development environment
mamba create -n prob-lab-dev python=3.11
mamba activate prob-lab-dev
pip install -e ".[dev]"

# Production environment
mamba create -n prob-lab-prod python=3.11
mamba activate prob-lab-prod
pip install -e .
```

### 3. Document Custom Dependencies

If you add new dependencies:

1. Add to `pyproject.toml`
2. Add to `environment.yml`
3. Add to `requirements.txt`
4. Update this document
5. Test installation from scratch

### 4. Regular Updates

```bash
# Monthly: Check for security updates
pip list --outdated | grep -i security

# Quarterly: Update all dependencies
mamba update --all
pip install --upgrade -r requirements.txt

# Always: Test after updates
pytest
```

---

## Summary

### Core Stack

- **Numerical**: NumPy, SciPy
- **Data**: Pandas, Polars
- **Visualization**: Matplotlib, Plotly
- **Domain**: Lifelines (survival analysis)
- **Utilities**: Pydantic, Typer, Rich
- **Configuration**: Hydra, OmegaConf

### Installation Strategy

1. **Compiled libraries** → mamba/conda (better binary handling)
2. **Pure-Python** → pip (often more up-to-date)
3. **Optional frameworks** → on-demand installation

### Key Points

- ✅ All dependencies have stable, well-maintained releases
- ✅ Compatible with Python 3.9+
- ✅ Work on all major platforms (macOS, Linux, Windows)
- ✅ Optimized for Apple Silicon via conda-forge
- ✅ Minimal dependency conflicts

For installation instructions, see:
- [Environment Setup Guide](environment-setup-guide.md)
- [Quick Start](quick-start.md)
- [Installation Guide](installation.md)

# Editable Mode Deep Dive: How `pip install -e .` Works

**Purpose**: Technical explanation of editable mode installation for active development.

---

## What is Editable Mode?

Editable mode (also called "development mode") allows you to install a Python package in a way that links to your source code rather than copying it. This is enabled by the `-e` flag in pip.

```bash
pip install -e .
# -e = editable
# .  = current directory (where pyproject.toml is)
```

---

## The Problem It Solves

### Without Editable Mode

```bash
# Traditional installation
pip install .

# Your workflow:
1. Edit code
2. pip install .          # Reinstall
3. Test
4. Edit code again
5. pip install .          # Reinstall again
6. Test again
# ... repeat forever
```

**Problem**: Every code change requires reinstallation, which is slow and tedious.

### With Editable Mode

```bash
# Editable installation (once)
pip install -e .

# Your workflow:
1. Edit code
2. Test                   # No reinstall needed!
3. Edit code again
4. Test again             # Still no reinstall!
# ... changes are immediately available
```

**Solution**: Code changes are immediately available without reinstalling.

---

## How It Works Technically

### 1. Traditional Installation Process

When you run `pip install .`:

```
Source Directory                     site-packages
────────────────                     ─────────────
/path/to/probability-lab/            /env/lib/python3.11/site-packages/
├── prob_lab/                        
│   ├── __init__.py                  
│   ├── distributions/               
│   │   ├── __init__.py              
│   │   └── normal.py                
│   └── config.py                    
└── pyproject.toml                   

                    ↓ pip copies files ↓

Source Directory                     site-packages
────────────────                     ─────────────
/path/to/probability-lab/            /env/lib/python3.11/site-packages/
├── prob_lab/                        ├── prob_lab/  ← COPIED HERE
│   ├── __init__.py                  │   ├── __init__.py
│   ├── distributions/               │   ├── distributions/
│   │   ├── __init__.py              │   │   ├── __init__.py
│   │   └── normal.py                │   │   └── normal.py
│   └── config.py                    │   └── config.py
└── pyproject.toml                   └── probability_lab-0.1.0.dist-info/
```

**Result**: Python imports from the COPY in site-packages, not your source.

### 2. Editable Installation Process

When you run `pip install -e .`:

```
Source Directory                     site-packages
────────────────                     ─────────────
/path/to/probability-lab/            /env/lib/python3.11/site-packages/
├── prob_lab/                        
│   ├── __init__.py                  
│   ├── distributions/               
│   │   ├── __init__.py              
│   │   └── normal.py                
│   └── config.py                    
└── pyproject.toml                   

                    ↓ pip creates link ↓

Source Directory                     site-packages
────────────────                     ─────────────
/path/to/probability-lab/            /env/lib/python3.11/site-packages/
├── prob_lab/  ← SOURCE              ├── __editable___probability_lab_0_1_0_finder.py
│   ├── __init__.py                  ├── __editable__.probability_lab-0.1.0.pth
│   ├── distributions/               └── probability_lab-0.1.0.dist-info/
│   │   ├── __init__.py                  ├── METADATA
│   │   └── normal.py                    ├── RECORD
│   └── config.py                        └── direct_url.json
└── pyproject.toml                   
                                     ↑ These files tell Python to look
                                       in your source directory
```

**Result**: Python imports from your SOURCE directory, not a copy.

---

## The Files Created

### 1. The `.pth` File

**Location**: `site-packages/__editable__.probability_lab-0.1.0.pth`

**Contents**:
```python
import __editable___probability_lab_0_1_0_finder; __editable___probability_lab_0_1_0_finder.install()
```

**What it does**:
- Python automatically executes `.pth` files when it starts
- This imports and runs the finder module

### 2. The Finder Module

**Location**: `site-packages/__editable___probability_lab_0_1_0_finder.py`

**Simplified contents**:
```python
from importlib.machinery import ModuleSpec
from importlib.util import spec_from_file_location
from pathlib import Path

# Mapping of package names to source locations
MAPPING = {
    'prob_lab': Path('/path/to/probability-lab/prob_lab'),
}

class EditableFinder:
    @classmethod
    def find_spec(cls, name, path=None, target=None):
        if name in MAPPING:
            origin = MAPPING[name] / '__init__.py'
            return spec_from_file_location(name, origin, submodule_search_locations=[str(MAPPING[name])])
        return None

def install():
    import sys
    sys.meta_path.insert(0, EditableFinder)
```

**What it does**:
- Intercepts import requests for `prob_lab`
- Redirects Python to your source directory
- Allows submodule imports to work correctly

### 3. The Metadata Directory

**Location**: `site-packages/probability_lab-0.1.0.dist-info/`

**Contents**:
- `METADATA` - Package information (name, version, dependencies)
- `RECORD` - List of installed files
- `INSTALLER` - Says "pip"
- `direct_url.json` - Points to your source directory

**What it does**:
- Tells pip the package is installed
- Allows `pip list`, `pip show`, etc. to work
- Enables `pip uninstall`

---

## Python's Import Process with Editable Mode

### Step-by-Step

1. **You write**: `import prob_lab`

2. **Python checks** `sys.meta_path` (import hooks)
   - Finds `EditableFinder` (installed by the `.pth` file)

3. **EditableFinder checks** if `prob_lab` is in its mapping
   - Yes! Maps to `/path/to/probability-lab/prob_lab`

4. **Python loads** from your source directory
   - Reads `/path/to/probability-lab/prob_lab/__init__.py`

5. **Subsequent imports** work the same way
   - `from prob_lab.distributions import X` → loads from your source

### Visual Flow

```
import prob_lab
    ↓
sys.meta_path (import hooks)
    ↓
EditableFinder.find_spec('prob_lab')
    ↓
Check MAPPING: 'prob_lab' → '/path/to/probability-lab/prob_lab'
    ↓
Load from: /path/to/probability-lab/prob_lab/__init__.py
    ↓
✓ Module loaded from YOUR SOURCE CODE
```

---

## Why site-packages is Always in sys.path

### Python's Module Search Path

When Python starts, it builds `sys.path` in this order:

1. **Current directory** (where you ran `python`)
2. **PYTHONPATH** environment variable (if set)
3. **Standard library** locations
4. **site-packages** directory ← Always included!

### Checking sys.path

```python
import sys
print('\n'.join(sys.path))

# Example output (with prob-lab activated):
# /path/to/current/directory
# /path/to/miniforge3/envs/prob-lab/lib/python311.zip
# /path/to/miniforge3/envs/prob-lab/lib/python3.11
# /path/to/miniforge3/envs/prob-lab/lib/python3.11/lib-dynload
# /path/to/miniforge3/envs/prob-lab/lib/python3.11/site-packages  ← HERE!
```

### Why This Matters

- `site-packages` is **automatically** in the search path
- No need to set `PYTHONPATH`
- No need to manually add directories
- Editable mode leverages this automatic inclusion

---

## Package Discovery Configuration

### The Problem

By default, setuptools tries to find all packages in your project:

```
probability-lab/
├── prob_lab/        ← Package
├── dev/             ← Not a package (but has __init__.py?)
├── apps/            ← Not a package
├── scripts/         ← Not a package
└── examples/        ← Not a package
```

Without configuration, setuptools might think `dev`, `apps`, etc. are packages!

### The Solution

In `pyproject.toml`:

```toml
[tool.setuptools.packages.find]
where = ["."]                    # Look in current directory
include = ["prob_lab*"]          # Include prob_lab and subpackages
exclude = ["dev*", "apps*", "scripts*", "examples*", "docs*"]
```

**What this does**:
- Explicitly tells setuptools: "Only `prob_lab` is a package"
- Excludes utility directories
- Prevents "Multiple top-level packages" error

### How It Works

```python
# Setuptools internally does something like:
packages = find_packages(
    where='.',
    include=['prob_lab*'],
    exclude=['dev*', 'apps*', 'scripts*', 'examples*', 'docs*']
)
# Result: packages = ['prob_lab', 'prob_lab.distributions', 'prob_lab.survival', ...]
```

Only these packages get the editable link.

---

## Practical Examples

### Example 1: Adding a New Module

```bash
# 1. Create new file
cat > prob_lab/distributions/gamma.py << 'EOF'
class GammaDistribution:
    def __init__(self, alpha, beta):
        self.alpha = alpha
        self.beta = beta
    
    def fit(self, data):
        return f"Fitted Gamma({self.alpha}, {self.beta})"
EOF

# 2. Use immediately (no reinstall!)
python -c "from prob_lab.distributions.gamma import GammaDistribution; print(GammaDistribution(2, 3).fit([]))"
# Output: Fitted Gamma(2, 3)
```

### Example 2: Modifying Existing Code

```python
# File: prob_lab/config.py (before)
DEFAULT_BINS = 10

# Change it to:
DEFAULT_BINS = 20

# Test immediately (no reinstall!)
python -c "from prob_lab.config import DEFAULT_BINS; print(DEFAULT_BINS)"
# Output: 20
```

### Example 3: Working with Jupyter

```python
# In Jupyter notebook

# Cell 1: Import
from prob_lab.distributions import MyDistribution
dist = MyDistribution()
print(dist.fit([1, 2, 3]))
# Output: "old behavior"

# Now edit prob_lab/distributions/my_distribution.py
# Change the fit() method

# Cell 2: Reload and test
import importlib
import prob_lab.distributions
importlib.reload(prob_lab.distributions)

from prob_lab.distributions import MyDistribution
dist = MyDistribution()
print(dist.fit([1, 2, 3]))
# Output: "new behavior"
```

### Example 4: Running Tests

```bash
# Edit code
vim prob_lab/distributions/normal.py

# Run tests immediately (no reinstall!)
pytest tests/test_normal.py

# Tests use your latest code automatically
```

---

## Limitations and Edge Cases

### 1. Module Reloading

**Problem**: Python caches imported modules

```python
# First import
import prob_lab.config
print(prob_lab.config.VALUE)  # Output: 10

# You edit config.py and change VALUE to 20

# Import again (still cached!)
import prob_lab.config
print(prob_lab.config.VALUE)  # Output: 10 (old value!)
```

**Solution**: Reload the module

```python
import importlib
importlib.reload(prob_lab.config)
print(prob_lab.config.VALUE)  # Output: 20 (new value!)
```

**Better solution**: Restart Python/Jupyter kernel

### 2. Structural Changes

**Problem**: Adding/removing files or changing `pyproject.toml`

```bash
# Add new top-level package
mkdir prob_lab/new_module
touch prob_lab/new_module/__init__.py

# May not be immediately available
```

**Solution**: Reinstall

```bash
pip install -e .
```

### 3. Entry Points / Console Scripts

**Problem**: Changes to entry points require reinstall

```toml
# In pyproject.toml
[project.scripts]
prob-lab = "prob_lab.cli:main"
```

If you change the entry point, you must:

```bash
pip install -e .
```

### 4. Dependencies

**Problem**: Adding new dependencies to `pyproject.toml`

```toml
dependencies = [
    "numpy>=1.24",
    "new-package>=1.0",  # Added this
]
```

**Solution**: Reinstall

```bash
pip install -e .
```

### 5. Not for Production

**Problem**: Editable mode is for development only

**For production**:
```bash
# Build a wheel
python -m build

# Or regular install
pip install .

# Or install from git
pip install git+https://github.com/user/probability-lab.git
```

---

## Comparison with Other Approaches

### Approach 1: Manual PYTHONPATH

```bash
# Add to PYTHONPATH
export PYTHONPATH="/path/to/probability-lab:$PYTHONPATH"

# Now you can import
python -c "import prob_lab"
```

**Drawbacks**:
- Must set PYTHONPATH every time
- Doesn't work in Jupyter easily
- No package metadata (pip doesn't know it's installed)
- Dependencies not automatically installed

### Approach 2: sys.path.append()

```python
import sys
sys.path.append('/path/to/probability-lab')
import prob_lab
```

**Drawbacks**:
- Must add to every script
- Doesn't work across sessions
- No package metadata
- Dependencies not automatically installed

### Approach 3: Editable Mode (Best!)

```bash
pip install -e .
```

**Benefits**:
- ✅ Works everywhere automatically
- ✅ Works in Jupyter
- ✅ Package metadata available
- ✅ Dependencies installed
- ✅ Can use `pip list`, `pip show`, etc.
- ✅ Professional development workflow

---

## Advanced: Multiple Editable Packages

You can have multiple packages in editable mode:

```bash
# Install package A
cd /path/to/package-a
pip install -e .

# Install package B
cd /path/to/package-b
pip install -e .

# Both are now editable
python -c "import package_a, package_b"
```

**Use case**: Developing multiple related packages simultaneously

---

## Debugging Editable Installations

### Check if Package is Editable

```bash
pip show probability-lab
# Look for: Location: /path/to/probability-lab (your source, not site-packages)
```

### Check Import Location

```python
import prob_lab
print(prob_lab.__file__)
# Should show: /path/to/probability-lab/prob_lab/__init__.py
```

### Check sys.path

```python
import sys
print('\n'.join(sys.path))
# Should include site-packages (where the .pth file is)
```

### Check for .pth File

```bash
ls -la $(python -c "import site; print(site.getsitepackages()[0])")/\*editable\*.pth
# Should show the .pth file
```

### Check Finder Module

```bash
ls -la $(python -c "import site; print(site.getsitepackages()[0])")/\*editable\*finder.py
# Should show the finder module
```

---

## Summary

**Key Concept**: `pip install -e .` creates a symbolic link mechanism using:
1. A `.pth` file that runs on Python startup
2. A finder module that intercepts imports
3. Metadata that tells pip the package is installed

**Result**: Python imports from your source directory, making changes immediately available without reinstalling.

**Best Practice**: Always use editable mode for active development of your own packages.

**Remember**: 
- `site-packages` is always in `sys.path`
- Editable mode leverages this to redirect imports
- Changes to code are immediate
- Structural changes may require reinstall
- Not for production use

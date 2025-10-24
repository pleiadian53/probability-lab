# Hydra Configuration Guide

**Experiment management with composable YAML configs for probability-lab**

---

## Table of Contents

1. [Overview](#overview)
2. [Why Hydra?](#why-hydra)
3. [Quick Start](#quick-start)
4. [Configuration Structure](#configuration-structure)
5. [Usage Examples](#usage-examples)
6. [Advanced Features](#advanced-features)
7. [Best Practices](#best-practices)
8. [Troubleshooting](#troubleshooting)

---

## Overview

Hydra provides a powerful framework for managing experiment configurations in probability-lab. Instead of hardcoding parameters or using command-line arguments, you can:

- **Compose** configurations from modular YAML files
- **Override** any parameter from the command line
- **Track** experiments with automatic timestamped output directories
- **Reproduce** results by saving complete configurations

### What Gets Configured?

- **Data**: Which dataset, columns, file paths
- **Fitting**: Which distribution, MLE/Bayesian methods
- **Extreme Value Theory**: Block maxima (GEV) or peaks-over-threshold (GPD)
- **Visualization**: Which plots to generate
- **Output**: Where to save results

---

## Why Hydra?

### Problem Without Hydra

```python
# Messy command-line arguments
python run.py --data-path examples/data.csv --data-column time \
  --dist weibull_min --mle true --bayes false \
  --extreme-mode block_maxima --block-size 30 \
  --viz-qq true --viz-cdf true \
  --output-dir outputs/exp1
```

### Solution With Hydra

```bash
# Clean, composable configs
python -m prob_lab.exp.run fit=weibull_min extreme=block_maxima

# Easy overrides
python -m prob_lab.exp.run extreme.block_size=20 output_dir=outputs/exp2
```

### Key Benefits

1. **Composability**: Mix and match config groups (data, fit, extreme, viz)
2. **Reproducibility**: Complete config saved with each run
3. **Experimentation**: Quickly try different parameter combinations
4. **Organization**: Automatic timestamped output directories
5. **Type Safety**: OmegaConf provides runtime type checking

---

## Quick Start

### Installation

Hydra dependencies are included in the base installation:

```bash
pip install -e .
```

This installs:
- `hydra-core>=1.3`
- `omegaconf>=2.3`

### Run Default Experiment

```bash
python -m prob_lab.exp.run
```

This uses the default configuration:
- Data: `examples/survival_synthetic.csv`
- Fit: Weibull distribution (MLE)
- Extreme: Disabled
- Viz: QQ plot + CDF overlay

### Output Structure

```
outputs/
└── 2025-10-23/
    └── 21-30-45/              # Timestamp: HH-MM-SS
        ├── .hydra/
        │   ├── config.yaml    # Complete merged config
        │   ├── hydra.yaml     # Hydra runtime config
        │   └── overrides.yaml # CLI overrides used
        ├── cdf_overlay.png    # Visualization
        ├── qq.png             # Visualization
        └── summary.json       # Fit results
```

---

## Configuration Structure

### Directory Layout

```
conf/
├── config.yaml                 # Main config with defaults
├── data/                       # Data source configs
│   ├── survival_synth.yaml
│   └── csv_template.yaml
├── fit/                        # Distribution fitting configs
│   ├── weibull_min.yaml
│   └── lognorm.yaml
├── extreme/                    # Extreme value configs
│   ├── disabled.yaml
│   ├── block_maxima.yaml
│   └── peaks_over_threshold.yaml
└── viz/                        # Visualization configs
    └── default.yaml
```

### Main Config (`conf/config.yaml`)

```yaml
defaults:
  - data: survival_synth        # Default data config
  - fit: weibull_min            # Default fitting config
  - viz: default                # Default viz config
  - extreme: disabled           # Default extreme config
  - _self_                      # Apply overrides last

output_dir: outputs

hydra:
  run:
    dir: ${output_dir}/${now:%Y-%m-%d}/${now:%H-%M-%S}
```

**Key points**:
- `defaults` list specifies which configs to load from each group
- `_self_` ensures CLI overrides take precedence
- `${now:...}` creates timestamped directories

### Config Groups

#### Data Configs (`conf/data/`)

**`survival_synth.yaml`** (default):
```yaml
name: survival_synth
kind: csv
path: examples/survival_synthetic.csv
column: time
event_column: null
engine: pandas
```

**`csv_template.yaml`** (for custom data):
```yaml
name: custom
kind: csv
path: /path/to/your/data.csv
column: value
event_column: null
engine: pandas
```

#### Fit Configs (`conf/fit/`)

**`weibull_min.yaml`**:
```yaml
dist: weibull_min
mle: true
bayes: false
```

**`lognorm.yaml`**:
```yaml
dist: lognorm
mle: true
bayes: false
```

#### Extreme Value Configs (`conf/extreme/`)

**`disabled.yaml`** (default):
```yaml
enabled: false
mode: null
block_size: 30
threshold: null
```

**`block_maxima.yaml`** (GEV for block maxima):
```yaml
enabled: true
mode: block_maxima
block_size: 30        # Size of each block
threshold: null
```

**`peaks_over_threshold.yaml`** (GPD for threshold exceedances):
```yaml
enabled: true
mode: peaks_over_threshold
block_size: null
threshold: 0.95       # Quantile (0-1) or absolute value
```

#### Visualization Configs (`conf/viz/`)

**`default.yaml`**:
```yaml
qq: true              # Generate QQ plot
cdf_overlay: true     # Generate CDF overlay
save: true            # Save plots to disk
```

---

## Usage Examples

### Basic Examples

#### 1. Default Run

```bash
python -m prob_lab.exp.run
```

Uses: survival_synth + weibull_min + disabled extreme + default viz

#### 2. Change Distribution

```bash
python -m prob_lab.exp.run fit=lognorm
```

Switches to log-normal distribution

#### 3. Enable Extreme Value Analysis

```bash
# Block maxima (GEV)
python -m prob_lab.exp.run extreme=block_maxima

# Peaks over threshold (GPD)
python -m prob_lab.exp.run extreme=peaks_over_threshold
```

#### 4. Use Custom Data

```bash
python -m prob_lab.exp.run data=csv_template \
  data.path=/path/to/your.csv \
  data.column=value
```

### Advanced Examples

#### 5. Multiple Overrides

```bash
python -m prob_lab.exp.run \
  fit=lognorm \
  extreme=block_maxima \
  extreme.block_size=20 \
  output_dir=outputs/lognorm_exp
```

#### 6. Adjust EVT Parameters

```bash
# Change block size for GEV
python -m prob_lab.exp.run extreme=block_maxima extreme.block_size=50

# Use 99th percentile threshold for GPD
python -m prob_lab.exp.run extreme=peaks_over_threshold extreme.threshold=0.99

# Use absolute threshold value
python -m prob_lab.exp.run extreme=peaks_over_threshold extreme.threshold=100.0
```

#### 7. Disable Visualizations

```bash
python -m prob_lab.exp.run viz.qq=false viz.cdf_overlay=false
```

#### 8. Custom Output Directory

```bash
python -m prob_lab.exp.run output_dir=outputs/experiments/exp_001
```

### Combining Multiple Options

```bash
# Complete custom experiment
python -m prob_lab.exp.run \
  data.path=data/hospital_los.csv \
  data.column=length_of_stay \
  fit=lognorm \
  extreme=peaks_over_threshold \
  extreme.threshold=0.95 \
  viz.qq=true \
  viz.cdf_overlay=true \
  output_dir=outputs/hospital_los_analysis
```

---

## Advanced Features

### 1. Config Inspection

View the complete merged configuration without running:

```bash
python -m prob_lab.exp.run --cfg job
```

View Hydra's configuration:

```bash
python -m prob_lab.exp.run --cfg hydra
```

### 2. Multirun (Sweeps)

Run multiple experiments with different parameters:

```bash
# Try multiple distributions
python -m prob_lab.exp.run --multirun fit=weibull_min,lognorm,gamma

# Try multiple block sizes
python -m prob_lab.exp.run --multirun extreme=block_maxima extreme.block_size=10,20,30,50

# Grid search
python -m prob_lab.exp.run --multirun \
  fit=weibull_min,lognorm \
  extreme.block_size=20,30,40
```

Each run gets its own timestamped directory.

### 3. Accessing Config in Code

```python
@hydra.main(config_path='../../conf', config_name='config', version_base='1.3')
def main(cfg: DictConfig) -> None:
    # Access nested config
    data_path = cfg.data.path
    dist_name = cfg.fit.dist
    block_size = cfg.extreme.block_size
    
    # Check if enabled
    if cfg.extreme.enabled:
        print(f"EVT mode: {cfg.extreme.mode}")
    
    # Convert to dict if needed
    config_dict = OmegaConf.to_container(cfg, resolve=True)
    
    # Print full config
    print(OmegaConf.to_yaml(cfg))
```

### 4. Variable Interpolation

Use variables in configs:

```yaml
# In config.yaml
data_dir: /path/to/data
output_dir: ${data_dir}/outputs  # References data_dir

# In data config
path: ${data_dir}/myfile.csv     # References top-level data_dir
```

### 5. Environment Variables

```yaml
# Use environment variables
path: ${oc.env:DATA_PATH}
api_key: ${oc.env:API_KEY,default_value}
```

---

## Best Practices

### 1. Organizing Experiments

```bash
# Use descriptive output directories
python -m prob_lab.exp.run output_dir=outputs/weibull_baseline
python -m prob_lab.exp.run output_dir=outputs/lognorm_comparison
python -m prob_lab.exp.run output_dir=outputs/evt_sensitivity
```

### 2. Creating New Config Groups

To add a new distribution:

```bash
# Create conf/fit/gamma.yaml
cat > conf/fit/gamma.yaml << 'EOF'
dist: gamma
mle: true
bayes: false
EOF

# Use it
python -m prob_lab.exp.run fit=gamma
```

### 3. Documenting Experiments

Each run automatically saves:
- `.hydra/config.yaml` - Complete configuration
- `.hydra/overrides.yaml` - What you changed from defaults
- `summary.json` - Fit results

### 4. Reproducibility

To reproduce a run:

```bash
# Original run
python -m prob_lab.exp.run fit=lognorm extreme.block_size=25

# Later, check outputs/YYYY-MM-DD/HH-MM-SS/.hydra/overrides.yaml
# It shows: ['fit=lognorm', 'extreme.block_size=25']

# Reproduce exactly
python -m prob_lab.exp.run fit=lognorm extreme.block_size=25
```

### 5. Version Control

**Do commit**:
- `conf/` directory (all YAML configs)
- `prob_lab/exp/run.py` (experiment script)

**Don't commit**:
- `outputs/` directory (add to `.gitignore`)
- `.hydra/` directories (automatically in `outputs/`)

---

## Troubleshooting

### Problem: Config Not Found

```
ConfigCompositionException: Cannot find primary config 'config'
```

**Solution**: Ensure you're running from the project root or the `config_path` is correct:

```python
@hydra.main(config_path='../../conf', config_name='config', version_base='1.3')
```

### Problem: Config Group Not Found

```
ConfigCompositionException: Could not find 'my_config' in data
```

**Solution**: Check the file exists at `conf/data/my_config.yaml`

### Problem: Override Not Working

```bash
python -m prob_lab.exp.run extreme.block_size=50
# But it still uses 30
```

**Solution**: Ensure `_self_` is in the defaults list (it should be last):

```yaml
defaults:
  - data: survival_synth
  - fit: weibull_min
  - viz: default
  - extreme: disabled
  - _self_              # ← Must be here
```

### Problem: Path Not Found

```
FileNotFoundError: examples/survival_synthetic.csv
```

**Solution**: Use Hydra's `to_absolute_path`:

```python
from hydra.utils import to_absolute_path as abspath

df = pd.read_csv(abspath(cfg.data.path))
```

### Problem: Output Directory Not Created

**Solution**: Hydra automatically changes to the output directory. Use:

```python
outdir = os.getcwd()  # Already in the right place!
```

---

## Integration with prob_lab

### Current Implementation

The experiment runner (`prob_lab/exp/run.py`) demonstrates:

1. **Data loading** with configurable paths and columns
2. **MLE fitting** with any scipy distribution
3. **Extreme value analysis** (GEV/GPD)
4. **Visualization** (QQ plots, CDF overlays)
5. **Results saving** (JSON summary + plots)

### Extending the Runner

To add new features:

```python
@hydra.main(config_path='../../conf', config_name='config', version_base='1.3')
def main(cfg: DictConfig) -> None:
    # ... existing code ...
    
    # Add Bayesian fitting
    if cfg.fit.bayes:
        from prob_lab.fitting.bayes import fit_pymc
        bayes_result = fit_pymc(cfg.fit.dist, x)
        results['bayes'] = bayes_result
    
    # Add time series analysis
    if cfg.get('timeseries', {}).get('enabled', False):
        from prob_lab.timeseries import fit_ar
        ar_result = fit_ar(x, order=cfg.timeseries.order)
        results['timeseries'] = ar_result
```

Then create `conf/timeseries/ar1.yaml`:

```yaml
enabled: true
order: 1
method: yule_walker
```

---

## Additional Resources

### Hydra Documentation

- [Official Docs](https://hydra.cc/docs/intro/)
- [Tutorials](https://hydra.cc/docs/tutorials/intro/)
- [Config Groups](https://hydra.cc/docs/tutorials/basic/your_first_app/config_groups/)
- [Multirun](https://hydra.cc/docs/tutorials/basic/running_your_app/multi-run/)

### Related prob_lab Documentation

- [Environment Setup](../environment-setup-guide.md)
- [Quick Start](../quick-start.md)
- [Installation](../installation.md)

---

## Summary

**Hydra provides**:
- ✅ Composable YAML configs
- ✅ Command-line overrides
- ✅ Automatic experiment tracking
- ✅ Reproducible results
- ✅ Clean separation of code and configuration

**Usage pattern**:
```bash
python -m prob_lab.exp.run [config_group=choice] [param.override=value]
```

**Best for**:
- Running multiple experiments
- Comparing different distributions
- Sensitivity analysis
- Reproducible research

Start with the defaults and override what you need!

# Hydra Tutorial: Step-by-Step

**Hands-on tutorial for using Hydra in probability-lab experiments**

---

## Tutorial 1: Your First Hydra Experiment

### Step 1: Run with Defaults

```bash
cd /path/to/probability-lab
mamba activate prob-lab

python -m prob_lab.exp.run
```

**What happens**:
1. Hydra loads `conf/config.yaml`
2. Merges configs from defaults (data, fit, viz, extreme)
3. Creates timestamped output directory
4. Runs the experiment
5. Saves results and config

**Check the output**:
```bash
ls outputs/$(date +%Y-%m-%d)/
# You'll see a timestamped directory like: 14-30-45/

ls outputs/$(date +%Y-%m-%d)/14-30-45/
# Contents:
# .hydra/           - Hydra metadata
# cdf_overlay.png   - CDF plot
# qq.png            - QQ plot
# summary.json      - Fit results
```

### Step 2: Inspect the Config

```bash
python -m prob_lab.exp.run --cfg job
```

**Output**:
```yaml
data:
  name: survival_synth
  kind: csv
  path: examples/survival_synthetic.csv
  column: time
  event_column: null
  engine: pandas
fit:
  dist: weibull_min
  mle: true
  bayes: false
viz:
  qq: true
  cdf_overlay: true
  save: true
extreme:
  enabled: false
  mode: null
  block_size: 30
  threshold: null
output_dir: outputs
```

This is the complete merged configuration.

---

## Tutorial 2: Changing Distributions

### Try Different Distributions

```bash
# Log-normal
python -m prob_lab.exp.run fit=lognorm

# Gamma
python -m prob_lab.exp.run fit=gamma

# Exponential
python -m prob_lab.exp.run fit=expon
```

### Create a New Distribution Config

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

### Compare Multiple Distributions

```bash
# Run multirun to try several distributions
python -m prob_lab.exp.run --multirun fit=weibull_min,lognorm,gamma
```

This creates separate output directories for each run.

---

## Tutorial 3: Extreme Value Analysis

### Block Maxima (GEV)

```bash
# Enable block maxima with default block size (30)
python -m prob_lab.exp.run extreme=block_maxima

# Try different block sizes
python -m prob_lab.exp.run extreme=block_maxima extreme.block_size=20
python -m prob_lab.exp.run extreme=block_maxima extreme.block_size=50
```

**What it does**:
- Splits data into blocks of size `block_size`
- Takes maximum of each block
- Fits Generalized Extreme Value (GEV) distribution

### Peaks Over Threshold (GPD)

```bash
# Use 95th percentile as threshold
python -m prob_lab.exp.run extreme=peaks_over_threshold

# Use 99th percentile
python -m prob_lab.exp.run extreme=peaks_over_threshold extreme.threshold=0.99

# Use absolute threshold value
python -m prob_lab.exp.run extreme=peaks_over_threshold extreme.threshold=100.0
```

**What it does**:
- Identifies values exceeding threshold
- Fits Generalized Pareto Distribution (GPD) to exceedances

### Sensitivity Analysis

```bash
# Try multiple block sizes
python -m prob_lab.exp.run --multirun \
  extreme=block_maxima \
  extreme.block_size=10,20,30,40,50
```

---

## Tutorial 4: Custom Data

### Using Your Own CSV

```bash
# Option 1: Override data config
python -m prob_lab.exp.run \
  data.path=/path/to/your/data.csv \
  data.column=your_column_name

# Option 2: Create a new data config
cat > conf/data/my_data.yaml << 'EOF'
name: my_data
kind: csv
path: /path/to/your/data.csv
column: value
event_column: null
engine: pandas
EOF

# Use it
python -m prob_lab.exp.run data=my_data
```

### Example: Hospital Length of Stay

```bash
# Create config
cat > conf/data/hospital_los.yaml << 'EOF'
name: hospital_los
kind: csv
path: data/hospital_admissions.csv
column: length_of_stay
event_column: null
engine: pandas
EOF

# Run analysis
python -m prob_lab.exp.run \
  data=hospital_los \
  fit=lognorm \
  extreme=peaks_over_threshold \
  extreme.threshold=0.95
```

---

## Tutorial 5: Complete Experiment Workflow

### Scenario: Analyzing Survival Data

**Goal**: Fit multiple distributions, compare with EVT, generate diagnostics

```bash
# 1. Baseline: Weibull fit only
python -m prob_lab.exp.run \
  output_dir=outputs/survival_baseline

# 2. Compare distributions
python -m prob_lab.exp.run --multirun \
  fit=weibull_min,lognorm,gamma \
  output_dir=outputs/survival_comparison

# 3. Add extreme value analysis
python -m prob_lab.exp.run \
  fit=weibull_min \
  extreme=block_maxima \
  extreme.block_size=30 \
  output_dir=outputs/survival_evt_block

python -m prob_lab.exp.run \
  fit=weibull_min \
  extreme=peaks_over_threshold \
  extreme.threshold=0.95 \
  output_dir=outputs/survival_evt_pot

# 4. Sensitivity to block size
python -m prob_lab.exp.run --multirun \
  fit=weibull_min \
  extreme=block_maxima \
  extreme.block_size=10,20,30,40,50 \
  output_dir=outputs/survival_evt_sensitivity
```

### Review Results

```bash
# Check all experiments
ls -R outputs/survival_*

# Compare AIC values
for dir in outputs/survival_*/; do
  echo "=== $dir ==="
  cat "$dir"/summary.json | grep -A2 "aic"
done
```

---

## Tutorial 6: Advanced Config Patterns

### Using Variable Interpolation

```yaml
# conf/config.yaml
data_root: /data/projects/probability-lab
output_root: ${data_root}/outputs

# conf/data/my_data.yaml
path: ${data_root}/datasets/myfile.csv
```

### Conditional Logic

```python
# In run.py
if cfg.extreme.enabled:
    if cfg.extreme.mode == 'block_maxima':
        # GEV fitting
        pass
    elif cfg.extreme.mode == 'peaks_over_threshold':
        # GPD fitting
        pass
```

### Environment Variables

```yaml
# conf/data/secure.yaml
path: ${oc.env:DATA_PATH}/sensitive_data.csv
api_key: ${oc.env:API_KEY}
```

```bash
export DATA_PATH=/secure/storage
export API_KEY=your_key_here
python -m prob_lab.exp.run data=secure
```

---

## Tutorial 7: Organizing Experiments

### Directory Structure

```bash
outputs/
├── baseline/                    # Baseline experiments
│   ├── weibull/
│   └── lognorm/
├── evt_analysis/                # EVT experiments
│   ├── block_maxima/
│   └── peaks_over_threshold/
└── sensitivity/                 # Sensitivity analyses
    ├── block_size/
    └── threshold/
```

### Using Descriptive Names

```bash
# Bad: Generic names
python -m prob_lab.exp.run output_dir=outputs/exp1
python -m prob_lab.exp.run output_dir=outputs/exp2

# Good: Descriptive names
python -m prob_lab.exp.run output_dir=outputs/baseline/weibull_mle
python -m prob_lab.exp.run output_dir=outputs/evt/gev_block30
python -m prob_lab.exp.run output_dir=outputs/sensitivity/gpd_threshold_sweep
```

### Experiment Log

Create `experiments.md`:

```markdown
# Experiment Log

## 2025-10-23

### Baseline Analysis
- **Run**: `outputs/baseline/weibull_mle`
- **Config**: Weibull MLE, no EVT
- **Result**: AIC=1234.5, good fit on QQ plot

### EVT Block Maxima
- **Run**: `outputs/evt/gev_block30`
- **Config**: Weibull MLE + GEV (block=30)
- **Result**: GEV shape=-0.15 (Weibull-like tail)

### Sensitivity Analysis
- **Run**: `outputs/sensitivity/block_size_sweep`
- **Config**: Block sizes 10,20,30,40,50
- **Result**: Stable estimates for block>=20
```

---

## Tutorial 8: Debugging and Troubleshooting

### Check Config Before Running

```bash
# Dry run - see config without executing
python -m prob_lab.exp.run --cfg job

# Check specific override
python -m prob_lab.exp.run extreme.block_size=25 --cfg job | grep block_size
```

### Verbose Output

```bash
# See Hydra's internal operations
python -m prob_lab.exp.run --hydra-help

# See available config groups
python -m prob_lab.exp.run --help
```

### Common Errors

**Error**: `ConfigCompositionException: Could not find 'my_config'`

**Fix**: Check file exists at correct path:
```bash
ls conf/fit/my_config.yaml
```

**Error**: `FileNotFoundError: examples/data.csv`

**Fix**: Use absolute path or ensure file exists:
```bash
python -m prob_lab.exp.run data.path=$(pwd)/examples/data.csv
```

**Error**: Override not taking effect

**Fix**: Ensure `_self_` is in defaults:
```yaml
defaults:
  - data: survival_synth
  - _self_              # Must be here!
```

---

## Tutorial 9: Integration with Jupyter

### Using Hydra in Notebooks

```python
# notebook.ipynb
from hydra import compose, initialize
from omegaconf import OmegaConf

# Initialize Hydra
initialize(config_path="../conf", version_base="1.3")

# Compose config
cfg = compose(config_name="config", overrides=["fit=lognorm", "extreme.block_size=25"])

# Use config
print(OmegaConf.to_yaml(cfg))

# Access values
data_path = cfg.data.path
dist_name = cfg.fit.dist
```

### Running Experiments from Notebooks

```python
# Run experiment programmatically
from prob_lab.exp.run import main
from hydra import compose, initialize

initialize(config_path="../conf", version_base="1.3")
cfg = compose(config_name="config", overrides=["fit=weibull_min"])

# Run
main(cfg)
```

---

## Tutorial 10: Best Practices Summary

### DO

✅ Use descriptive output directory names
✅ Create config files for reusable settings
✅ Use multirun for parameter sweeps
✅ Check configs with `--cfg job` before running
✅ Keep experiment logs
✅ Version control your `conf/` directory

### DON'T

❌ Hardcode paths in code
❌ Use generic names like "exp1", "test2"
❌ Commit `outputs/` directory
❌ Modify configs in place (use overrides)
❌ Forget to document experiments

### Workflow Template

```bash
# 1. Plan experiment
# 2. Check config
python -m prob_lab.exp.run [overrides] --cfg job

# 3. Run experiment
python -m prob_lab.exp.run [overrides] output_dir=outputs/descriptive_name

# 4. Review results
ls outputs/descriptive_name/
cat outputs/descriptive_name/summary.json

# 5. Document in experiment log
echo "## Experiment: descriptive_name" >> experiments.md
echo "Config: ..." >> experiments.md
echo "Results: ..." >> experiments.md
```

---

## Next Steps

1. **Read the main guide**: [docs/hydra/README.md](README.md)
2. **Explore configs**: Check `conf/` directory
3. **Try examples**: Run the tutorials above
4. **Create your own**: Add custom configs for your data
5. **Share**: Document your experiments for reproducibility

Happy experimenting! 🎯

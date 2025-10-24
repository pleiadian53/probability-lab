# Hydra Documentation Index

**Experiment management with composable configurations**

---

## Quick Links

- 📖 **[Main Guide](README.md)** - Complete Hydra reference
- 🎓 **[Tutorial](tutorial.md)** - Step-by-step examples
- ✅ **[Summary](SUMMARY.md)** - Verification and recommendations

---

## What is Hydra?

Hydra is a framework for elegantly configuring complex applications. In probability-lab, it enables:

- **Composable configs** - Mix and match YAML files for different experiments
- **CLI overrides** - Change any parameter from command line
- **Automatic tracking** - Timestamped directories with complete configs
- **Reproducibility** - Save and replay experiments exactly

---

## Getting Started

### 1. Quick Start

```bash
# Run with defaults
python -m prob_lab.exp.run

# Change distribution
python -m prob_lab.exp.run fit=lognorm

# Enable extreme value analysis
python -m prob_lab.exp.run extreme=block_maxima
```

### 2. Read the Documentation

**New to Hydra?** Start with the [Tutorial](tutorial.md)

**Need reference?** Check the [Main Guide](README.md)

**Want to verify?** See the [Summary](SUMMARY.md)

---

## Documentation Structure

### [README.md](README.md) - Main Guide

Complete reference covering:
- Why Hydra?
- Configuration structure
- Usage examples (basic to advanced)
- Multirun/sweeps
- Best practices
- Troubleshooting

**Best for**: Understanding the full system

### [tutorial.md](tutorial.md) - Step-by-Step Tutorial

10 hands-on tutorials:
1. Your first experiment
2. Changing distributions
3. Extreme value analysis
4. Custom data
5. Complete workflow
6. Advanced patterns
7. Organizing experiments
8. Debugging
9. Jupyter integration
10. Best practices

**Best for**: Learning by doing

### [SUMMARY.md](SUMMARY.md) - Verification & Recommendations

- Implementation verification
- What was done
- Enhancement suggestions
- Next steps

**Best for**: Understanding what's implemented and what's possible

---

## Configuration Files

Your Hydra configs are at `conf/`:

```
conf/
├── config.yaml              # Main config
├── data/                    # Data sources
├── fit/                     # Distributions
├── extreme/                 # EVT configs
└── viz/                     # Visualization
```

See [Main Guide - Configuration Structure](README.md#configuration-structure) for details.

---

## Common Tasks

### Run an Experiment

```bash
python -m prob_lab.exp.run [config_group=choice] [param=value]
```

### View Config

```bash
python -m prob_lab.exp.run --cfg job
```

### Parameter Sweep

```bash
python -m prob_lab.exp.run --multirun fit=weibull_min,lognorm,gamma
```

### Custom Data

```bash
python -m prob_lab.exp.run data.path=/path/to/data.csv data.column=value
```

---

## Examples

### Basic

```bash
# Weibull with block maxima EVT
python -m prob_lab.exp.run extreme=block_maxima

# Log-normal with peaks-over-threshold
python -m prob_lab.exp.run fit=lognorm extreme=peaks_over_threshold
```

### Advanced

```bash
# Complete custom experiment
python -m prob_lab.exp.run \
  data.path=data/hospital.csv \
  data.column=los \
  fit=lognorm \
  extreme=peaks_over_threshold \
  extreme.threshold=0.95 \
  output_dir=outputs/hospital_analysis
```

### Multirun

```bash
# Try multiple distributions
python -m prob_lab.exp.run --multirun fit=weibull_min,lognorm,gamma

# Sensitivity analysis
python -m prob_lab.exp.run --multirun \
  extreme=block_maxima \
  extreme.block_size=10,20,30,40,50
```

---

## Output Structure

Each run creates a timestamped directory:

```
outputs/
└── 2025-10-23/
    └── 21-30-45/
        ├── .hydra/
        │   ├── config.yaml      # Complete config
        │   └── overrides.yaml   # CLI overrides
        ├── cdf_overlay.png
        ├── qq.png
        └── summary.json
```

---

## Integration with prob_lab

### Current Features

- ✅ Data loading (CSV with configurable paths/columns)
- ✅ MLE fitting (any scipy distribution)
- ✅ Extreme value analysis (GEV/GPD)
- ✅ Visualization (QQ plots, CDF overlays)
- ✅ Results saving (JSON + plots)

### Extending

See [Main Guide - Integration](README.md#integration-with-prob_lab) for how to add:
- Bayesian fitting
- Time series analysis
- Cross-validation
- Custom metrics

---

## Resources

### Internal

- [Main README](../../README.md) - Project overview
- [Environment Setup](../environment-setup-guide.md) - Installation
- [Quick Start](../quick-start.md) - Daily workflow

### External

- [Hydra Official Docs](https://hydra.cc/docs/intro/)
- [OmegaConf Docs](https://omegaconf.readthedocs.io/)
- [Hydra Tutorials](https://hydra.cc/docs/tutorials/intro/)

---

## Quick Reference

### Config Groups

- `data=X` - Choose data source (survival_synth, csv_template)
- `fit=X` - Choose distribution (weibull_min, lognorm, gamma)
- `extreme=X` - Choose EVT mode (disabled, block_maxima, peaks_over_threshold)
- `viz=X` - Choose visualization (default)

### Common Overrides

- `data.path=PATH` - Custom data file
- `data.column=COL` - Data column name
- `fit.dist=DIST` - Distribution name
- `extreme.block_size=N` - Block size for GEV
- `extreme.threshold=T` - Threshold for GPD (0-1 for quantile, >1 for absolute)
- `output_dir=DIR` - Output directory

### Flags

- `--cfg job` - Show config without running
- `--multirun` - Run multiple experiments
- `--help` - Show available options

---

## Support

### Troubleshooting

See [Main Guide - Troubleshooting](README.md#troubleshooting) for common issues.

### Questions?

1. Check the [Tutorial](tutorial.md) for examples
2. Review the [Main Guide](README.md) for detailed explanations
3. Look at existing configs in `conf/`
4. Check [Hydra docs](https://hydra.cc/docs/intro/)

---

## Summary

**Hydra provides**:
- Composable YAML configs
- Command-line overrides  
- Automatic experiment tracking
- Reproducible results

**Start here**:
1. Read [Tutorial](tutorial.md) for hands-on learning
2. Reference [Main Guide](README.md) as needed
3. Check [Summary](SUMMARY.md) for what's implemented

**Run experiments**:
```bash
python -m prob_lab.exp.run [config_group=choice] [param=value]
```

Happy experimenting! 🎯

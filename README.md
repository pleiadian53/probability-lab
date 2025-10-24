
# probability-lab

A modular, extensible playground to **fit, diagnose, and visualize probability distributions** on real-world(ish) data,
with first-class support for **time series**, **survival analysis**, **extreme values (min/max)**, and (optionally) **Bayesian** fitting.

- Batteries-included MLE via SciPy
- Publication-ready diagnostics: PDF/ECDF overlays, QQ and PP plots, residuals
- Survival analysis via `lifelines` (Kaplan–Meier, Aalen–Johansen, Cox PH fit + parametric survival)
- Extreme value theory (GEV/GPD) for block maxima/minima & threshold exceedances
- Optional Bayesian fitting via PyMC *or* Pyro
- Frontend: a simple **Streamlit** app for interactive exploration and beautiful plots
- Data layer: load from CSV/Parquet or generate realistic synthetic EHR-like & survival datasets

## Install

```bash
pip install -e .[dev]        # editable install (recommended for hacking)
# or minimal
pip install -e .
```

## Quickstart

```bash
# 1) Run the demo CLI to fit a distribution and write plots to ./outputs
python -m prob_lab.fit_demo --csv examples/survival_synthetic.csv --column time --dist weibull_min

# 2) Launch the Streamlit explorer
streamlit run apps/streamlit_app.py
```

## Project layout

```
probability-lab/
 ├─ prob_lab/
 │   ├─ __init__.py
 │   ├─ config.py
 │   ├─ registry.py
 │   ├─ data/loaders.py
 │   ├─ distributions/
 │   │   ├─ base.py
 │   │   ├─ scipy_wrappers.py
 │   │   └─ extreme_value.py
 │   ├─ fitting/
 │   │   ├─ mle.py
 │   │   └─ bayes.py
 │   ├─ survival/lifelines_adapter.py
 │   ├─ timeseries/ar_models.py
 │   └─ visualize/plot.py
 ├─ apps/streamlit_app.py
 ├─ examples/survival_synthetic.csv
 ├─ pyproject.toml
 └─ README.md
```

## M1/M2 Macs
All dependencies have CPU builds. Optional extras (`torch`, `pyro`, `pymc`) can be installed if supported by your environment.

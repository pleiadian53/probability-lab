
from __future__ import annotations
import importlib
import numpy as np
from typing import Any, Dict

def fit_lognorm_pymc(x: np.ndarray, draws=1000, chains=2) -> Dict[str, Any]:
    if importlib.util.find_spec("pymc") is None:
        raise ImportError("pymc not installed. Try: pip install pymc arviz")
    import pymc as pm
    import arviz as az
    with pm.Model() as m:
        mu = pm.Normal("mu", 0, 2)
        sigma = pm.HalfNormal("sigma", 1)
        pm.Lognormal("obs", mu=mu, sigma=sigma, observed=x)
        idata = pm.sample(draws=draws, chains=chains, target_accept=0.9, progressbar=False)
    return {"model": m, "idata": idata, "summary": az.summary(idata).to_dict()}

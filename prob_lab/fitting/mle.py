
from __future__ import annotations
import numpy as np
from typing import Dict
from ..distributions.scipy_wrappers import fit_scipy
from ..distributions.base import FitResult

def try_many(x: np.ndarray, dist_names=("expon","weibull_min","lognorm","gamma","gompertz")) -> Dict[str, FitResult]:
    results = {}
    for name in dist_names:
        try:
            results[name] = fit_scipy(name, x)
        except Exception as e:
            results[name] = e  # store error for visibility
    return results

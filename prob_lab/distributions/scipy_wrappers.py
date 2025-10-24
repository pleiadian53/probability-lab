
from __future__ import annotations
import numpy as np
from scipy import stats
from .base import Distribution, FitResult
from typing import Tuple

class ScipyDistribution(Distribution):
    def __init__(self, dist_name: str):
        self.name = dist_name
        self.dist = getattr(stats, dist_name)
    def fit(self, x: np.ndarray) -> FitResult:
        params = self.dist.fit(x)
        *arg, loc, scale = params
        loglik = np.sum(self.dist.logpdf(x, *arg, loc=loc, scale=scale))
        n = len(x)
        k = len(arg) + 2  # shape params + loc + scale
        aic = 2*k - 2*loglik
        bic = k*np.log(n) - 2*loglik
        return FitResult(self.name, tuple(arg), loc, scale, aic, bic, loglik, n)
    def pdf(self, x: np.ndarray) -> np.ndarray:
        return self.dist.pdf(x, *getattr(self, "params_", ()), loc=getattr(self, "loc_", 0), scale=getattr(self, "scale_", 1))
    def cdf(self, x: np.ndarray) -> np.ndarray:
        return self.dist.cdf(x, *getattr(self, "params_", ()), loc=getattr(self, "loc_", 0), scale=getattr(self, "scale_", 1))

def fit_scipy(dist_name: str, x: np.ndarray) -> FitResult:
    model = ScipyDistribution(dist_name)
    fr = model.fit(x)
    # store for convenience
    model.params_, model.loc_, model.scale_ = fr.params, fr.loc, fr.scale
    return fr

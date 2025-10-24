
from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from typing import Dict, Any, Tuple

@dataclass
class FitResult:
    name: str
    params: Tuple[float, ...]
    loc: float
    scale: float
    aic: float
    bic: float
    loglik: float
    n: int

class Distribution:
    name: str
    def fit(self, x: np.ndarray) -> FitResult:
        raise NotImplementedError
    def pdf(self, x: np.ndarray) -> np.ndarray:
        raise NotImplementedError
    def cdf(self, x: np.ndarray) -> np.ndarray:
        raise NotImplementedError

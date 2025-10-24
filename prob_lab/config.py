
from pydantic import BaseModel, Field
from typing import Optional, List

class FitConfig(BaseModel):
    dist: str = Field(..., description="scipy.stats distribution name (e.g. 'weibull_min')")
    column: str = Field(..., description="column name to fit")
    weights_column: Optional[str] = None
    right_censor_column: Optional[str] = None
    left_censor_column: Optional[str] = None
    # plotting
    output_dir: str = "outputs"
    n_points: int = 400

class AppConfig(BaseModel):
    theme: str = "light"
    default_distributions: List[str] = ["expon", "weibull_min", "lognorm", "gamma", "genextreme", "gpd"]

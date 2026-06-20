from dataclasses import dataclass


@dataclass
class DataModel:
    exponents: list[float]
    errors: list[list[float]]
    labels: list[str]
    colors: list[str]
    linestyles: list[str]
    m: int
    n_reps: int
    exp_min: float
    exp_max: float

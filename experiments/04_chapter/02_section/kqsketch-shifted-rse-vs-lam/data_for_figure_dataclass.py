from dataclasses import dataclass


@dataclass
class DataModel:
    lambda_range: list[float]
    b_sweep: list[int]
    b_sweep_shifted: list[int]
    rse_kq: dict[str, list[float]]       # str(b) -> RSE values
    rse_shifted: dict[str, list[float]]   # str(b) -> RSE values
    m: int
    n_reps: int

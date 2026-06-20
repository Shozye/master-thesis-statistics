from dataclasses import dataclass


@dataclass
class BResult:
    b: int
    rse_newton: list[float]
    rse_qsketch: float


@dataclass
class DataModel:
    k_values: list[float]
    b_results: list[BResult]
    n_reps: int
    m: int
    lam: float
    n_elems: int

from dataclasses import dataclass


@dataclass
class DataModel:
    # Left/middle subplots: vs m
    ms: list[int]
    time_direct: list[float]
    time_cold: list[float]
    time_warm: list[float]
    iters_cold_m: list[float]
    iters_warm_m: list[float]
    # Right subplot: vs Lambda
    exponents: list[float]
    iters_cold_lam: list[float]
    iters_warm_lam: list[float]
    # Caption params
    lam_fixed: float
    m_fixed: int
    n_reps: int
    k: float
    b_bits: int

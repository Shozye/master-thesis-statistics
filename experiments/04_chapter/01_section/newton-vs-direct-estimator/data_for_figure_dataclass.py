from dataclasses import dataclass


@dataclass
class DataModel:
    # Left subplot: RSE vs log10(Lambda) at fixed m
    exponents: list[float]
    rse_d1: list[float]
    rse_c1: list[float]
    rse_w1: list[float]
    # Right subplot: RSE vs m at fixed Lambda
    ms: list[int]
    rse_d2: list[float]
    rse_c2: list[float]
    rse_w2: list[float]
    # Caption params
    m_fixed: int
    lam_fixed: float
    n_reps: int
    k: float
    b_bits: int

from dataclasses import dataclass


@dataclass
class DataModel:
    # Left subplot: empirical RSE vs m at fixed k
    ms: list[int]
    rse_floor_m: list[float]
    rse_round_m: list[float]
    # Right subplot: empirical RSE vs k at fixed m (plotted as RSE * sqrt(m))
    ks: list[float]
    rse_floor_k: list[float]
    rse_round_k: list[float]
    # Caption / theory params
    m_fixed: int
    lam: float
    k_fixed: float
    b_bits: int
    n_stream: int
    n_reps: int

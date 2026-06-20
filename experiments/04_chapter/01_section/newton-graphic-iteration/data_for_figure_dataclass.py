from dataclasses import dataclass


@dataclass
class DataModel:
    # Newton map g(Lambda) sampled per panel
    lam_cold: list[float]
    g_cold: list[float]
    lam_warm: list[float]
    g_warm: list[float]
    # Iterate trajectories Lambda_0, Lambda_1, ...
    cold_traj: list[float]
    warm_traj: list[float]
    # Key points
    root: float
    cold_start: float
    warm_start: float
    # Iteration counts as reported by the library counter
    cold_iters: int
    warm_iters: int
    # Caption params
    lambda_true: float
    m: int
    k: float
    b_bits: int

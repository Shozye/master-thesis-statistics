from dataclasses import dataclass


@dataclass
class DataModel:
    exponents: list[float]
    rse_exp: list[float]
    rse_kqsk: list[float]
    rse_round: list[float]
    rse_round_corrected: list[float]
    m: int
    k: float
    b_bits: int
    n_reps: int

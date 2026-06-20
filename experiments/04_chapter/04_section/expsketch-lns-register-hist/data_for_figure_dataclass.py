from dataclasses import dataclass


@dataclass
class DataModel:
    counts: list[list[int]]  # counts[i] = histogram for each weight
    labels: list[str]
    amount_bits: int
    v_max: float
    m: int

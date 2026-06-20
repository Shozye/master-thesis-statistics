from dataclasses import dataclass


@dataclass
class DataModel:
    # Left plot: counts_left[i] = register counts array for WEIGHTS[i]
    counts_left: list[list[int]]
    weights_left: list[float]
    labels_left: list[str]
    q_bits: int
    p_bits: int
    m: int
    # Right plot: counts_right[i] = register counts array for M_VALUES[i]
    counts_right: list[list[int]]
    m_values: list[int]
    q_bits_2: int
    p_bits_2: int

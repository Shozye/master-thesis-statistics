from dataclasses import dataclass


@dataclass
class DataModel:
    # rse_data[q_idx][j_idx] = list of RSE values over p_values
    rse_data: list[list[list[float]]]
    q_values: list[int]
    p_values: list[int]
    j_values: list[float]
    m: int

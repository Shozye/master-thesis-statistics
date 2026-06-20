from dataclasses import dataclass


@dataclass
class DataModel:
    log_lambdas: list[float]
    # errors_by_p[i] = list of RSE values for P_VALUES[i]
    errors_by_p: list[list[float]]
    p_values: list[int]
    errors_float64: list[float]
    q_bits: int
    m: int

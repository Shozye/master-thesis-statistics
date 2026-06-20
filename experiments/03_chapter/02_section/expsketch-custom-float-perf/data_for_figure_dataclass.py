from dataclasses import dataclass


@dataclass
class DataModel:
    log_lambdas: list[float]
    rse_custom_float: list[float]
    rse_float32: list[float]
    p: int
    q: int
    m: int

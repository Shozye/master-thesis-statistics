from dataclasses import dataclass


@dataclass
class DataModel:
    exponents: list[float]
    errors_float16: list[float]
    errors_float32: list[float]
    errors_float64: list[float]
    m: int
    n_reps: int

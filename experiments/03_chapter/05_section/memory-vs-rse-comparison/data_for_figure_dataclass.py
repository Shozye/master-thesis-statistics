from dataclasses import dataclass


@dataclass
class DataModel:
    memory_values: list[list[int]]
    rse_values: list[list[float]]
    labels: list[str]
    m_values: list[list[int]]
    n_reps: int
    b: int

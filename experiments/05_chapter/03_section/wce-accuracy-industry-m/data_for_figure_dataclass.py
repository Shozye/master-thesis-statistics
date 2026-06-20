from dataclasses import dataclass


@dataclass
class DataModel:
    m_values: list[int]
    rse_values: list[list[float]]
    labels: list[str]
    n_reps: int
    n_elements: int

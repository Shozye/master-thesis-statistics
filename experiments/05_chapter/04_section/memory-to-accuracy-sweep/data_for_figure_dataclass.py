from dataclasses import dataclass


@dataclass
class DataModel:
    memory_values: list[list[int]]
    rse_values: list[list[float]]
    m_values: list[list[int]]
    labels: list[str]
    n_reps: int
    n_elements: int
    total_weight: float
    dist_name: str
    k_base: float

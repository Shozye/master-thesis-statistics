from dataclasses import dataclass


@dataclass
class DataModel:
    m_values: list[int]
    update_times_us: list[list[float]]
    labels: list[str]
    n_elements: int
    n_reps: int

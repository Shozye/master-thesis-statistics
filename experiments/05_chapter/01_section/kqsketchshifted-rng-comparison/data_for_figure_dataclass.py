from dataclasses import dataclass


@dataclass
class DataModel:
    ms: list[int]
    times: dict[str, list[float]]
    errors: dict[str, list[float]]
    n_reps: int
    n_elements: int

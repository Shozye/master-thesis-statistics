from dataclasses import dataclass


@dataclass
class DataModel:
    bounds: dict[int, float]
    best_p: int
    bound_value: float
    bound_tex: str

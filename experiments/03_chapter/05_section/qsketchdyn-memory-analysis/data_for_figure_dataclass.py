from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class DataModel:
    b: int
    # rows: list of (name, m, rse, reg, hist, fast, total, t_us, e_us)
    rows: List[Tuple[str, int, float, int, int, int, int, float, float]]

from dataclasses import dataclass
from typing import List


@dataclass
class DataModel:
    m: int
    n_reps: int
    lambda_val: float
    regs_7: List[int]
    regs_5: List[int]

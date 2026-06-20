from dataclasses import dataclass


@dataclass
class DataModel:
    # left panel: varying m
    m_values: list[int]
    regs_by_m: dict[str, list[int]]  # str(m) -> register values
    offsets_by_m: dict[str, int]     # str(m) -> offset
    # right panel: varying k
    k_values: list[float]
    regs_by_k: dict[str, list[int]]  # str(k) -> register values
    offsets_by_k: dict[str, int]     # str(k) -> offset
    b: int
    k_fixed: float
    m_fixed: int
    lam: float

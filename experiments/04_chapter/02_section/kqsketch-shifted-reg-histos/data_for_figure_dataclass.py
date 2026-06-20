from dataclasses import dataclass


@dataclass
class DataModel:
    regs_kq_rel: list[int]
    regs_sh_rel: list[int]
    b: int
    offset: int
    m: int
    lam: float

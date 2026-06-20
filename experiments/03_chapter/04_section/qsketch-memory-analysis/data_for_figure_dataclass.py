from dataclasses import dataclass


@dataclass
class DataModel:
    m: int
    b: int
    rse_exp32: float
    rse_fast32: float
    rse_qsk: float
    exp32_registers: int
    exp32_fast: int
    exp32_total: int
    base_qsk_registers: int
    base_qsk_fast: int
    base_qsk_total: int
    fast32_registers: int
    fast32_fast: int
    fast32_total: int
    qsk_registers: int
    qsk_fast: int
    qsk_total: int

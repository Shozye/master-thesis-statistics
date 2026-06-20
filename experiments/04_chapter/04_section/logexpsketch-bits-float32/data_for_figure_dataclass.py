from dataclasses import dataclass


@dataclass
class DataModel:
    m: int
    v_max: float
    # --- Panel (a): cardinality RSE vs log10(Lambda) ---
    log_lambdas: list[float]
    panel_a_labels: list[str]
    # panel_a_rse[series_idx][lambda_idx]
    panel_a_rse: list[list[float]]
    # --- Panel (b): Jaccard RSE vs bits b ---
    b_values: list[int]
    j_values: list[float]
    # panel_b_rse[j_idx][b_idx]
    panel_b_rse: list[list[float]]

# ---
# description: QSketch memory breakdown table comparing ExpSketchFloat32, FastExpSketchFloat32, QSketch(b=8) at m=100
# ---
"""
Experiment: Generate a LaTeX table showing full memory breakdown of three sketches.

Columns: m, RSE, Registers, Fast, Total, Ratio, Theoretical Total.
Seeds are counted as 0 bytes (computable in O(1) from index).
BaseQSketch is QSketch without Fast framework (no Fisher-Yates).
Ratio: ExpSketch=1 baseline for BaseQSketch, FastExpSketch=1 baseline for QSketch.

Output: generated_output/03_chapter/qsketch-memory-analysis/
"""

import math
import numpy as np
import tqdm

from weighted_cardinality_estimation import ExpSketchFloat32, FastExpSketchFloat32, QSketch
from generated_output_manager import DRAFT, DraftLevel, GeneratedOutputManager
from data_for_figure_dataclass import DataModel

# REVIEWED AND ACCEPTED DRAFT VARIABLES. Table output shows RSE to 2 decimal places; 10K reps gives ±0.05pp stability.
# BENCHMARK: DRAFT=0: 2.8s, DRAFT=1: 5.6s, DRAFT=2: 1.0s.
match DRAFT:
    case DraftLevel.DRAFT_FINAL_VERSION:
        N_REPS = 10_000
    case DraftLevel.DRAFT_FOR_HUMAN_TO_VIEW_LATEX:
        N_REPS = 25_000
    case DraftLevel.DRAFT_TO_FIX_EXPERIMENT_OR_SEE_IF_IT_COMPILES:
        N_REPS = 200

M = 100
B = 8
LAMBDA = 1e4


def measure_rse(make_sketch, m: int) -> float:
    estimates = []
    TOTAL_PBAR_VALUE = N_REPS
    pbar = tqdm.tqdm(total=TOTAL_PBAR_VALUE, desc=f"RSE m={m}", colour="cyan", unit="trial", mininterval=10.0)
    for trial in range(N_REPS):
        s = make_sketch(m, trial)
        s.add_many(["x0"], [LAMBDA])
        estimates.append(s.estimate())
        pbar.update(1)
    pbar.close()
    estimates = np.array(estimates)
    return float(np.std(estimates) / LAMBDA)


def compact_vector_bytes(size: int, bits: int) -> int:
    """Approximate: ceil(size*bits / 8)"""
    return math.ceil(size * bits / 8)


def main() -> None:
    out = GeneratedOutputManager(__file__)

    # Measure RSE
    rse_exp32 = measure_rse(lambda m, s: ExpSketchFloat32(m, seed=s), M)
    rse_fast32 = measure_rse(lambda m, s: FastExpSketchFloat32(m, seed=s), M)
    rse_qsk = measure_rse(lambda m, s: QSketch(m, seed=s, amount_bits=B), M)

    # Component breakdown (seeds counted as 0)
    ceil_log2_m = math.ceil(math.log2(M))
    fy_bytes = 2 * compact_vector_bytes(M, ceil_log2_m) + 32
    qsk_reg = (
        compact_vector_bytes(M, B) + 4 + 4 + 1 + 4
    )  # M_.bytes() + r_max + r_min + amount_bits + j_star

    # ExpSketch[f32]: registers=4m, no fast
    exp32_registers = M * 4
    exp32_fast = 0
    exp32_total = exp32_registers + 8

    # BaseQSketch[b=8]: registers only (no Fisher-Yates), same RSE as QSketch
    base_qsk_registers = qsk_reg
    base_qsk_fast = 0
    base_qsk_total = base_qsk_registers + 8

    # FastExpSketch[f32]: registers=4m, FY + max
    fast32_registers = M * 4
    fast32_fast = fy_bytes + 4  # FY + max
    fast32_total = fast32_registers + fast32_fast + 8

    # QSketch[b=8]: registers + FY
    qsk_registers = qsk_reg
    qsk_fast = fy_bytes
    qsk_total = qsk_registers + qsk_fast + 8

    out.save_dataclass(
        DataModel(
            m=M, b=B,
            rse_exp32=rse_exp32, rse_fast32=rse_fast32, rse_qsk=rse_qsk,
            exp32_registers=exp32_registers, exp32_fast=exp32_fast, exp32_total=exp32_total,
            base_qsk_registers=base_qsk_registers, base_qsk_fast=base_qsk_fast, base_qsk_total=base_qsk_total,
            fast32_registers=fast32_registers, fast32_fast=fast32_fast, fast32_total=fast32_total,
            qsk_registers=qsk_registers, qsk_fast=qsk_fast, qsk_total=qsk_total,
        ),
        DataModel,
    )


if __name__ == "__main__":
    main()

# ---
# description: QSketch memory breakdown table at equal RSE (QSketch uses m=108 to match ExpSketch m=100)
# ---
"""
Experiment: Same memory breakdown as qsketch-memory-analysis but QSketch uses
higher m to equalize RSE with ExpSketch.

Output: generated_output/03_chapter/qsketch-memory-equivalence/
"""

import math
import numpy as np
import tqdm

from weighted_cardinality_estimation import ExpSketchFloat32, FastExpSketchFloat32, QSketch
from generated_output_manager import DRAFT, DraftLevel, GeneratedOutputManager
from data_for_figure_dataclass import DataModel

# REVIEWED AND ACCEPTED DRAFT VARIABLES. Table output shows RSE to 2 decimal places; 10K reps gives ±0.05pp stability.
# BENCHMARK: DRAFT=0: 3.0s, DRAFT=1: 5.8s, DRAFT=2: 1.6s.
match DRAFT:
    case DraftLevel.DRAFT_FINAL_VERSION:
        N_REPS = 10_000
    case DraftLevel.DRAFT_FOR_HUMAN_TO_VIEW_LATEX:
        N_REPS = 25_000
    case DraftLevel.DRAFT_TO_FIX_EXPERIMENT_OR_SEE_IF_IT_COMPILES:
        N_REPS = 200

M_EXP = 100
M_QSK = 108
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
    rse_exp32 = measure_rse(lambda m, s: ExpSketchFloat32(m, seed=s), M_EXP)
    rse_fast32 = measure_rse(lambda m, s: FastExpSketchFloat32(m, seed=s), M_EXP)
    rse_qsk = measure_rse(lambda m, s: QSketch(m, seed=s, amount_bits=B), M_QSK)

    # Component breakdown (seeds counted as 0)
    ceil_log2_exp = math.ceil(math.log2(M_EXP))
    ceil_log2_qsk = math.ceil(math.log2(M_QSK))

    # ExpSketch[f32] m=100
    exp32_registers = M_EXP * 4
    exp32_fast = 0
    exp32_total = exp32_registers + 8

    # BaseQSketch[b=8] m=109 (no Fast)
    base_qsk_registers = compact_vector_bytes(M_QSK, B) + 4 + 4 + 1 + 4
    base_qsk_fast = 0
    base_qsk_total = base_qsk_registers + 8

    # FastExpSketch[f32] m=100
    fast32_registers = M_EXP * 4
    fast32_fast = 2 * compact_vector_bytes(M_EXP, ceil_log2_exp) + 32 + 4
    fast32_total = fast32_registers + fast32_fast + 8

    # QSketch[b=8] m=109
    qsk_registers = compact_vector_bytes(M_QSK, B) + 4 + 4 + 1 + 4
    qsk_fast = 2 * compact_vector_bytes(M_QSK, ceil_log2_qsk) + 32
    qsk_total = qsk_registers + qsk_fast + 8

    out.save_dataclass(
        DataModel(
            m_exp=M_EXP, m_qsk=M_QSK, b=B,
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

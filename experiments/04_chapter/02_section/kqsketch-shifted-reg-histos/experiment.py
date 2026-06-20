# ---
# description: kQSketchShifted vs kQSketch register value distribution histograms
# ---
"""Register histograms comparing kQSketch and kQSketchShifted at b=5, Lambda=5e4."""

import numpy as np

from weighted_cardinality_estimation import kQSketch, kQSketchShifted
from weighted_cardinality_estimation.stat import weighted_stream, Uniform
from generated_output_manager import DRAFT, DraftLevel, GeneratedOutputManager
from data_for_figure_dataclass import DataModel

M = 10_000
K = 2.0
LAMBDA = 5e4
N_ELEMS = 1000
B = 5


def main():
    out = GeneratedOutputManager(__file__)

    # REVIEWED AND ACCEPTED DRAFT VARIABLES. Deterministic single-run; no repetitions needed.
    # BENCHMARK: DRAFT=0: 1.0s, DRAFT=1: 1.0s, DRAFT=2: 1.0s.
    match DRAFT:
        case DraftLevel.DRAFT_FINAL_VERSION:
            n_reps = 1
        case DraftLevel.DRAFT_FOR_HUMAN_TO_VIEW_LATEX:
            n_reps = 1
        case DraftLevel.DRAFT_TO_FIX_EXPERIMENT_OR_SEE_IF_IT_COMPILES:
            n_reps = 1

    elems, weights = weighted_stream(N_ELEMS, LAMBDA, Uniform(), seed=0)
    sk_kq = kQSketch(M, seed=42, amount_bits=B, logarithm_base=K)
    sk_sh = kQSketchShifted(M, seed=42, amount_bits=B, logarithm_base=K)
    sk_kq.add_many(elems, weights)
    sk_sh.add_many(elems, weights)

    rmin = -2 ** (B - 1) + 1
    regs_kq_rel = (np.array(sk_kq.get_registers()) - rmin).tolist()
    regs_sh_rel = list(sk_sh.get_registers())

    out.save_dataclass(
        DataModel(
            regs_kq_rel=regs_kq_rel,
            regs_sh_rel=regs_sh_rel,
            b=B,
            offset=int(sk_sh.get_offset()),
            m=M,
            lam=LAMBDA,
        ),
        DataModel,
    )


if __name__ == "__main__":
    main()

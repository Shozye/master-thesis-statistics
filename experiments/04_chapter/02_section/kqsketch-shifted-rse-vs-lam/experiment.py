# ---
# description: kQSketchShifted vs kQSketch RSE across Lambda range for multiple bit widths
# ---
"""RSE vs Lambda sweep comparing kQSketchShifted and kQSketch at m=64."""

import numpy as np
import tqdm

from weighted_cardinality_estimation import kQSketch, kQSketchShifted
from weighted_cardinality_estimation.stat import weighted_stream, relative_error, Uniform
from generated_output_manager import DRAFT, DraftLevel, GeneratedOutputManager
from data_for_figure_dataclass import DataModel

M = 64
K = 2.0
N_ELEMS = 1000
B_SWEEP = [4, 5, 6, 7]
B_SWEEP_SHIFTED = [4, 5]
LAMBDA_RANGE = np.logspace(-30, 30, 30)


def main():
    out = GeneratedOutputManager(__file__)

    # REVIEWED AND ACCEPTED DRAFT VARIABLES. RSE vs Lambda sweep; 300 reps for stable curves.
    # BENCHMARK: DRAFT=0: >50s, DRAFT=1: 5.0s, DRAFT=2: 1.0s.
    match DRAFT:
        case DraftLevel.DRAFT_FINAL_VERSION:
            n_reps = 1000
        case DraftLevel.DRAFT_FOR_HUMAN_TO_VIEW_LATEX:
            n_reps = 30
        case DraftLevel.DRAFT_TO_FIX_EXPERIMENT_OR_SEE_IF_IT_COMPILES:
            n_reps = 10

    rse_kq = {b: [] for b in B_SWEEP}
    rse_shifted = {b: [] for b in B_SWEEP_SHIFTED}

    TOTAL_PBAR_VALUE = len(LAMBDA_RANGE)
    pbar = tqdm.tqdm(total=TOTAL_PBAR_VALUE, desc="RSE vs Lambda", colour="green", unit="lam", mininterval=10.0)
    for lam in LAMBDA_RANGE:
        for b in B_SWEEP:
            errors = []
            for rep in range(n_reps):
                elems, weights = weighted_stream(N_ELEMS, lam, Uniform())
                sk = kQSketch(M, seed=rep, amount_bits=b, logarithm_base=K)
                sk.add_many(elems, weights)
                errors.append(relative_error(sk.estimate(), lam))
            rse_kq[b].append(float(np.sqrt(np.mean(np.array(errors) ** 2))))
        for b in B_SWEEP_SHIFTED:
            errors = []
            for rep in range(n_reps):
                elems, weights = weighted_stream(N_ELEMS, lam, Uniform())
                sk = kQSketchShifted(M, seed=rep, amount_bits=b, logarithm_base=K)
                sk.add_many(elems, weights)
                errors.append(relative_error(sk.estimate(), lam))
            rse_shifted[b].append(float(np.sqrt(np.mean(np.array(errors) ** 2))))
        pbar.update(1)
    pbar.close()

    out.save_dataclass(
        DataModel(
            lambda_range=LAMBDA_RANGE.tolist(),
            b_sweep=B_SWEEP,
            b_sweep_shifted=B_SWEEP_SHIFTED,
            rse_kq={str(b): v for b, v in rse_kq.items()},
            rse_shifted={str(b): v for b, v in rse_shifted.items()},
            m=M,
            n_reps=n_reps,
        ),
        DataModel,
    )


if __name__ == "__main__":
    main()

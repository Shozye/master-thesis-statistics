# ---
# description: RSE of kQSketchShifted with b=5 varying m (left) and varying k (right)
# ---
"""kQSketchShifted register histograms: varying m (left) and varying k (right)."""

import tqdm

from weighted_cardinality_estimation import kQSketchShifted
from weighted_cardinality_estimation.stat import weighted_stream, Uniform
from generated_output_manager import DRAFT, DraftLevel, GeneratedOutputManager
from data_for_figure_dataclass import DataModel



def main():
    out = GeneratedOutputManager(__file__)

    B = 5
    K_FIXED = 2.0
    M_FIXED = 1000
    LAMBDA = 1000.0
    N_ELEMS = 1000
    M_VALUES = [50, 1000, 10000]
    K_VALUES = [2.0, 1.7, 1.4]

    # REVIEWED AND ACCEPTED DRAFT VARIABLES. Deterministic; fixed seed=42, n_reps=1.
    # BENCHMARK: DRAFT=0: 1.1s, DRAFT=1: 1.1s, DRAFT=2: 1.2s.
    match DRAFT:
        case DraftLevel.DRAFT_FINAL_VERSION:
            n_reps = 1
        case DraftLevel.DRAFT_FOR_HUMAN_TO_VIEW_LATEX:
            n_reps = 1
        case DraftLevel.DRAFT_TO_FIX_EXPERIMENT_OR_SEE_IF_IT_COMPILES:
            n_reps = 1

    regs_by_m = {}
    offsets_by_m = {}
    regs_by_k = {}
    offsets_by_k = {}

    steps = [("m", m) for m in M_VALUES] + [("k", k) for k in K_VALUES]
    TOTAL_PBAR_VALUE = len(steps)
    pbar = tqdm.tqdm(total=TOTAL_PBAR_VALUE, desc="kQSketch-Shifted params", colour="green", unit="cfg", mininterval=10.0)
    for kind, val in steps:
        elems, weights = weighted_stream(N_ELEMS, LAMBDA, Uniform(), seed=42)
        if kind == "m":
            sk = kQSketchShifted(int(val), seed=42, amount_bits=B, logarithm_base=K_FIXED)
            sk.add_many(elems, weights)
            regs_by_m[str(int(val))] = list(sk.get_registers())
            offsets_by_m[str(int(val))] = sk.get_offset()
        else:
            sk = kQSketchShifted(M_FIXED, seed=42, amount_bits=B, logarithm_base=float(val))
            sk.add_many(elems, weights)
            regs_by_k[str(val)] = list(sk.get_registers())
            offsets_by_k[str(val)] = sk.get_offset()
        pbar.update(1)
    pbar.close()

    out.save_dataclass(
        DataModel(
            m_values=M_VALUES,
            regs_by_m=regs_by_m,
            offsets_by_m=offsets_by_m,
            k_values=K_VALUES,
            regs_by_k=regs_by_k,
            offsets_by_k=offsets_by_k,
            b=B,
            k_fixed=K_FIXED,
            m_fixed=M_FIXED,
            lam=LAMBDA,
        ),
        DataModel,
    )


if __name__ == "__main__":
    main()

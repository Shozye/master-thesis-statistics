# ---
# description: LogExpSketch register value distribution histogram for varying Lambda and b
# ---

from weighted_cardinality_estimation import LogExpSketchFastNoShifted
from generated_output_manager import DRAFT, DraftLevel, GeneratedOutputManager
from data_for_figure_dataclass import DataModel

AMOUNT_BITS = 8
V_MAX = 128.0  # was exp_bits=4: v_min=2^-7, v_max=2^7=128
EXPONENTS = [-4, -2, 1]
LAMBDAS = [2**e for e in EXPONENTS]
LABELS = [rf"$\Lambda = 2^{{{e}}}$" for e in EXPONENTS]

# REVIEWED AND ACCEPTED DRAFT VARIABLES. Deterministic; M controls histogram smoothness.
# BENCHMARK: DRAFT=0: 1.1s, DRAFT=1: 1.0s, DRAFT=2: 1.0s.
match DRAFT:
    case DraftLevel.DRAFT_FINAL_VERSION:
        M = 20000
    case DraftLevel.DRAFT_FOR_HUMAN_TO_VIEW_LATEX:
        M = 2000
    case DraftLevel.DRAFT_TO_FIX_EXPERIMENT_OR_SEE_IF_IT_COMPILES:
        M = 500


def main() -> None:
    out = GeneratedOutputManager(__file__)
    n_buckets = 2**AMOUNT_BITS
    counts = []
    for lam in LAMBDAS:
        sk = LogExpSketchFastNoShifted(M, seed=42, amount_bits=AMOUNT_BITS, v_max=V_MAX)
        sk.add("x0", lam)
        regs = sk.get_registers()
        hist = [0] * n_buckets
        for v in regs:
            hist[v] += 1
        counts.append(hist)
    out.save_dataclass(
        DataModel(counts=counts, labels=LABELS, amount_bits=AMOUNT_BITS, v_max=V_MAX, m=M),
        DataModel,
    )


if __name__ == "__main__":
    main()

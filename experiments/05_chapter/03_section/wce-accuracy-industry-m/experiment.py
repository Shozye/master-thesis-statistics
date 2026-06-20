# ---
# description: "RSE of mergeable weighted cardinality sketches at industry-standard m values"
# ---
"""
Experiment: Measures RSE at m values used by production systems (512, 4096, 16384, 32768).
Only mergeable weighted cardinality sketches are included.
"""

import numpy as np
import tqdm

from weighted_cardinality_estimation import (
    FastExpSketch,
    FastExpSketchFloat32,
    LogExpSketchFastNoShifted,
    QSketch,
    kQSketchShifted,
    stat,
)
from generated_output_manager import DRAFT, DraftLevel, GeneratedOutputManager
from data_for_figure_dataclass import DataModel

match DRAFT:
    case DraftLevel.DRAFT_FINAL_VERSION:
        N_REPS = 10000
        N_ELEMENTS = 1
    case DraftLevel.DRAFT_FOR_HUMAN_TO_VIEW_LATEX:
        N_REPS = 200
        N_ELEMENTS = 1
    case DraftLevel.DRAFT_TO_FIX_EXPERIMENT_OR_SEE_IF_IT_COMPILES:
        N_REPS = 5
        N_ELEMENTS = 1

TOTAL_WEIGHT = 100_000.0
K_BASE = 1.5
M_VALUES = [512, 4096, 16384, 32768]


def measure_rse(make_sketch, m: int) -> float:
    estimates = np.empty(N_REPS)
    for rep in range(N_REPS):
        s = make_sketch(m, rep)
        s.add("element_0", TOTAL_WEIGHT)
        estimates[rep] = stat.relative_error(s.estimate(), TOTAL_WEIGHT)
    return float(np.sqrt(np.mean(estimates**2)))


def main() -> None:
    out = GeneratedOutputManager(__file__)

    configs = [
        ("FastExpSketch", lambda m, s: FastExpSketch(m, seed=s)),
        ("FastExpSketchFloat32", lambda m, s: FastExpSketchFloat32(m, seed=s)),
        ("QSketch(b=8)", lambda m, s: QSketch(m, seed=s, amount_bits=8)),
        ("kQSketchShifted(b=6)", lambda m, s: kQSketchShifted(m, seed=s, amount_bits=6, logarithm_base=K_BASE)),
        (r"LogExpSketch(b=11, $v_{\max}\approx 1.70\cdot10^{38}$)", lambda m, s: LogExpSketchFastNoShifted(m, seed=s, amount_bits=11, v_max=2.0 ** 127)),
        (r"LogExpSketch(b=14, $v_{\max}\approx 6.70\cdot10^{153}$)", lambda m, s: LogExpSketchFastNoShifted(m, seed=s, amount_bits=14, v_max=2.0 ** 511)),
    ]

    all_rse: list[list[float]] = []

    TOTAL_PBAR_VALUE = len(configs)
    pbar = tqdm.tqdm(total=TOTAL_PBAR_VALUE, desc="Accuracy at industry m-values", colour="#00cc88", unit="sketch", mininterval=10.0)
    for label, make_sketch in configs:
        rse_for_sketch: list[float] = []
        for m in M_VALUES:
            rse_for_sketch.append(measure_rse(make_sketch, m))
        all_rse.append(rse_for_sketch)
        pbar.update(1)
    pbar.close()

    out.save_dataclass(
        DataModel(
            m_values=M_VALUES,
            rse_values=all_rse,
            labels=[c[0] for c in configs],
            n_reps=N_REPS,
            n_elements=N_ELEMENTS,
        ),
        DataModel,
    )


if __name__ == "__main__":
    main()

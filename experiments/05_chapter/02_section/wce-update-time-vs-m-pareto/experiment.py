# ---
# description: "Update time (microseconds) vs number of registers m for weighted cardinality estimation sketches"
# ---
"""
Experiment: Measures add_many update time vs m for key WCE sketches.
Shows how throughput scales with sketch size.
"""

import time

import numpy as np
import tqdm

from weighted_cardinality_estimation import (
    ExpSketch,
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
        N_REPS = 10
        N_ELEMENTS = 4_000
        M_VALUES = [16, 32, 64, 100, 200, 400, 800, 1600, 3200, 6400, 10000]
    case DraftLevel.DRAFT_FOR_HUMAN_TO_VIEW_LATEX:
        N_REPS = 1
        N_ELEMENTS = 5_000
        M_VALUES = [16, 64, 100, 400, 1600, 6400, 10000]
    case DraftLevel.DRAFT_TO_FIX_EXPERIMENT_OR_SEE_IF_IT_COMPILES:
        N_REPS = 1
        N_ELEMENTS = 5_000
        M_VALUES = [16, 100, 400]

TOTAL_WEIGHT = N_ELEMENTS * 5.5
K_BASE = 1.5
rng = np.random.default_rng()

def measure_update_time_us(make_sketch, m: int) -> float:
    """Measure mean time (μs) for add_many of N_ELEMENTS elements."""
    elems, weights = stat.weighted_stream(N_ELEMENTS, TOTAL_WEIGHT, dist=stat.Uniform(1, 10))
    times = np.empty(N_REPS)
    for rep in range(N_REPS):
        s = make_sketch(m, rng.integers(1,999_999_999))
        t0 = time.perf_counter()
        s.add_many(elems, weights)
        t1 = time.perf_counter()
        times[rep] = (t1 - t0) * 1e6
    return float(np.median(times))


def main() -> None:
    out = GeneratedOutputManager(__file__)

    configs = [
        ("FastExpSketch", lambda m, s: FastExpSketch(m, seed=s)),
        ("FastExpSketchFloat32", lambda m, s: FastExpSketchFloat32(m, seed=s)),
        ("QSketch(b=8)", lambda m, s: QSketch(m, seed=s, amount_bits=8)),
        ("kQSketchShifted(b=6)", lambda m, s: kQSketchShifted(m, seed=s, amount_bits=6, logarithm_base=K_BASE)),
        (r"LogExpSketch(b=11, $v_{\max}\approx 1.70\cdot10^{38}$)", lambda m, s: LogExpSketchFastNoShifted(m, seed=s, amount_bits=11, v_max=2.0 ** 127)),
        (r"LogExpSketch(b=13, $v_{\max}\approx 6.70\cdot10^{153}$)", lambda m, s: LogExpSketchFastNoShifted(m, seed=s, amount_bits=13, v_max=2.0 ** 511)),
        ("ExpSketch", lambda m, s: ExpSketch(m, seed=s)),
    ]

    all_times: list[list[float]] = []

    TOTAL_PBAR_VALUE = len(configs)
    pbar = tqdm.tqdm(total=TOTAL_PBAR_VALUE, desc="Update time benchmarks", colour="#ffa500", unit="sketch", mininterval=10.0)
    for label, make_sketch in configs:
        times_for_sketch: list[float] = []
        for m in M_VALUES:
            times_for_sketch.append(measure_update_time_us(make_sketch, m))
        all_times.append(times_for_sketch)
        pbar.update(1)
    pbar.close()

    out.save_dataclass(
        DataModel(
            m_values=M_VALUES,
            update_times_us=all_times,
            labels=[c[0] for c in configs],
            n_elements=N_ELEMENTS,
            n_reps=N_REPS,
        ),
        DataModel,
    )


if __name__ == "__main__":
    main()

# ---
# description: QSketchDyn performance table comparing memory and update time against ExpSketch and FastExpSketch at m=100 and m=400
# ---
"""
Experiment: Generate a LaTeX table showing memory breakdown + update time of QSketchDyn
vs ExpSketch[f32] and FastExpSketch[f32] at m=100 and m=400, b=8.

Output: generated_output/03_chapter/qsketchdyn-memory-analysis/
"""

import math
import time
import numpy as np
import tqdm

from weighted_cardinality_estimation import (
    ExpSketchFloat32,
    FastExpSketchFloat32,
    QSketch,
    QSketchDyn,
)
from weighted_cardinality_estimation.stat import weighted_stream, Constant, Uniform
from generated_output_manager import DRAFT, DraftLevel, GeneratedOutputManager
from data_for_figure_dataclass import DataModel

# REVIEWED AND ACCEPTED DRAFT VARIABLES. Table output shows RSE to 2 decimal places; 10K reps gives ±0.05pp stability.
# BENCHMARK: DRAFT=0: 60.5s, DRAFT=1: 19.0s, DRAFT=2: 9.4s.
match DRAFT:
    case DraftLevel.DRAFT_FINAL_VERSION:
        N_REPS = 10_000
    case DraftLevel.DRAFT_FOR_HUMAN_TO_VIEW_LATEX:
        N_REPS = 2_000
    case DraftLevel.DRAFT_TO_FIX_EXPERIMENT_OR_SEE_IF_IT_COMPILES:
        N_REPS = 200

B = 8
LAMBDA = 1e4
N_ELEMENTS = 1000


def measure_rse(make_sketch, m: int, n_elements: int = 1) -> float:
    estimates = []
    TOTAL_PBAR_VALUE = N_REPS
    pbar = tqdm.tqdm(total=TOTAL_PBAR_VALUE, desc=f"RSE m={m}", colour="cyan", unit="trial", mininterval=10.0)
    for trial in range(N_REPS):
        s = make_sketch(m, trial)
        if n_elements > 1:
            elems, weights = weighted_stream(n_elements, LAMBDA, Uniform())
            true_val = sum(weights)
            s.add_many(elems, weights)
            estimates.append(s.estimate() / true_val)
        else:
            elems, weights = weighted_stream(n_elements, LAMBDA, Constant())
            s.add_many(elems, weights)
            estimates.append(s.estimate() / LAMBDA)
        pbar.update(1)
    pbar.close()
    estimates = np.array(estimates)
    return float(np.std(estimates))


def measure_update_time_us(make_sketch, m: int, n_elements: int) -> float:
    """Measure average time per add() call in microseconds."""
    elems, weights = weighted_stream(n_elements, LAMBDA, Uniform(), seed=0)

    # Warmup
    s = make_sketch(m, 0)
    s.add_many(elems, weights)

    # Timed runs
    n_runs = 50
    times = []
    for _ in range(n_runs):
        s = make_sketch(m, 0)
        start = time.perf_counter()
        s.add_many(elems, weights)
        elapsed = time.perf_counter() - start
        times.append(elapsed / n_elements)

    return float(np.median(times) * 1e6)  # microseconds


def measure_estimate_time_us(make_sketch, m: int, n_elements: int) -> float:
    """Measure time per estimate() call in microseconds."""
    elems, weights = weighted_stream(n_elements, LAMBDA, Uniform(), seed=0)

    s = make_sketch(m, 0)
    s.add_many(elems, weights)

    # Warmup
    for _ in range(100):
        s.estimate()

    # Timed runs
    n_calls = 10_000
    start = time.perf_counter()
    for _ in range(n_calls):
        s.estimate()
    elapsed = time.perf_counter() - start

    return float(elapsed / n_calls * 1e6)  # microseconds


def compact_vector_bytes(size: int, bits: int) -> int:
    return math.ceil(size * bits / 8)


def main() -> None:
    out = GeneratedOutputManager(__file__)

    m_values = [100, 400]
    all_rows = []

    for m in m_values:
        rse_exp = measure_rse(lambda m_, s: ExpSketchFloat32(m_, seed=s), m)
        rse_fast = measure_rse(lambda m_, s: FastExpSketchFloat32(m_, seed=s), m)
        rse_qsk = measure_rse(lambda m_, s: QSketch(m_, seed=s, amount_bits=B), m)
        rse_qsd = measure_rse(lambda m_, s: QSketchDyn(m_, seed=s, amount_bits=B, g_seed=42), m, n_elements=N_ELEMENTS)

        t_exp = measure_update_time_us(lambda m_, s: ExpSketchFloat32(m_, seed=s), m, N_ELEMENTS)
        t_fast = measure_update_time_us(lambda m_, s: FastExpSketchFloat32(m_, seed=s), m, N_ELEMENTS)
        t_qsk = measure_update_time_us(lambda m_, s: QSketch(m_, seed=s, amount_bits=B), m, N_ELEMENTS)
        t_qsd = measure_update_time_us(lambda m_, s: QSketchDyn(m_, seed=s, amount_bits=B, g_seed=42), m, N_ELEMENTS)

        e_exp = measure_estimate_time_us(lambda m_, s: ExpSketchFloat32(m_, seed=s), m, N_ELEMENTS)
        e_fast = measure_estimate_time_us(lambda m_, s: FastExpSketchFloat32(m_, seed=s), m, N_ELEMENTS)
        e_qsk = measure_estimate_time_us(lambda m_, s: QSketch(m_, seed=s, amount_bits=B), m, N_ELEMENTS)
        e_qsd = measure_estimate_time_us(lambda m_, s: QSketchDyn(m_, seed=s, amount_bits=B, g_seed=42), m, N_ELEMENTS)

        ceil_log2_m = math.ceil(math.log2(m))
        fy_bytes = 2 * compact_vector_bytes(m, ceil_log2_m) + 32

        exp_reg = m * 4
        exp_total = exp_reg + 8

        fast_reg = m * 4
        fast_fast = fy_bytes + 4
        fast_total = fast_reg + fast_fast + 8

        qsd_reg = compact_vector_bytes(m, B) + 4 + 4 + 1
        qsd_hist = compact_vector_bytes(2**B, ceil_log2_m)
        qsd_state = 4 + 8 + 8 + 8
        qsd_total = qsd_reg + qsd_hist + qsd_state

        qsk_reg = (
            compact_vector_bytes(m, B) + 4 + 4 + 1 + 4
        )  # R_ + r_min + r_max + amount_bits + j_star
        qsk_fast = fy_bytes
        qsk_total = qsk_reg + qsk_fast + 8

        all_rows.append(
            [
                ("ExpSketch[f32]", m, rse_exp, exp_reg, 0, 0, exp_total, t_exp, e_exp),
                (
                    "FastExpSketch[f32]",
                    m,
                    rse_fast,
                    fast_reg,
                    0,
                    fast_fast,
                    fast_total,
                    t_fast,
                    e_fast,
                ),
                (rf"QSketch \(b={B}\)", m, rse_qsk, qsk_reg, 0, qsk_fast, qsk_total, t_qsk, e_qsk),
                (rf"QSketchDyn \(b={B}\)", m, rse_qsd, qsd_reg, qsd_hist, 0, qsd_total, t_qsd, e_qsd),
            ]
        )

    out.save_dataclass(
        DataModel(b=B, rows=[row for group in all_rows for row in group]),
        DataModel,
    )


if __name__ == "__main__":
    main()

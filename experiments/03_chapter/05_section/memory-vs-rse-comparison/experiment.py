# ---
# description: Memory vs RSE comparison for QSketchDyn, QSketch, and WeightedHyperLogLogFloat32
# ---
"""
Experiment: Memory (bytes) vs RSE for three sketches from chapter 3.

Memory is calculated analytically (seeds=0, best-case) following the same
approach as the QSketch memory analysis in section 4.1.

Stream: 10000 elements, Uniform(1,10) weights.
Vary m to produce different memory/RSE points per sketch.
"""

import numpy as np
import tqdm

from weighted_cardinality_estimation import (
    MemoryFlag, QSketch, QSketchDyn, WeightedHyperLogLog, WeightedHyperLogLogFloat32, stat,
)
from generated_output_manager import DRAFT, DraftLevel, GeneratedOutputManager
from data_for_figure_dataclass import DataModel

# REVIEWED AND ACCEPTED DRAFT VARIABLES. Memory vs RSE comparison; 1000 reps for stable RSE measurements.
# BENCHMARK: DRAFT=0: >80s, DRAFT=1: 20.1s, DRAFT=2: 1.2s.
match DRAFT:
    case DraftLevel.DRAFT_FINAL_VERSION:
        N_REPS = 3000
        N_POINTS = 50
        N_ELEMENTS = 1000
    case DraftLevel.DRAFT_FOR_HUMAN_TO_VIEW_LATEX:
        N_REPS = 80
        N_POINTS = 12
        N_ELEMENTS = 1000
    case DraftLevel.DRAFT_TO_FIX_EXPERIMENT_OR_SEE_IF_IT_COMPILES:
        N_REPS = 5
        N_POINTS = 3
        N_ELEMENTS = 10

M_START = 16
MAX_MEMORY_BYTES = 1000

B = 8
TOTAL_WEIGHT = N_ELEMENTS * 5.5  # mean of Uniform(1,10)
MEM_FLAGS = MemoryFlag.TOTAL
rng = np.random.default_rng()

def get_memory(make_sketch, m: int) -> int:
    s = make_sketch(m, rng.integers(1, 999999999))
    return s.memory_usage(MEM_FLAGS)


def measure_rse(make_sketch, m: int) -> float:
    estimates = np.empty(N_REPS)
    for rep in range(N_REPS):
        elems, weights = stat.weighted_stream(
            N_ELEMENTS, TOTAL_WEIGHT, dist=stat.Uniform(1, 10)
        )
        s = make_sketch(m, rep)
        s.add_many(elems, weights)
        estimates[rep] = stat.relative_error(s.estimate(), TOTAL_WEIGHT)
    return float(np.sqrt(np.mean(estimates**2)))


def main() -> None:
    out = GeneratedOutputManager(__file__)

    configs = [
        ("QSketchDyn", lambda m, s: QSketchDyn(m, seed=s, amount_bits=B, g_seed=42)),
        ("QSketch", lambda m, s: QSketch(m, seed=s, amount_bits=B)),
        ("WeightedHyperLogLogFloat32", lambda m, s: WeightedHyperLogLogFloat32(m, seed=s)),
        ("WeightedHyperLogLog", lambda m, s: WeightedHyperLogLog(m, seed=s)),
    ]

    all_memory: list[list[int]] = []
    all_rse: list[list[float]] = []
    all_m_values: list[list[int]] = []
    labels: list[str] = []

    TOTAL_PBAR_VALUE = len(configs)
    pbar = tqdm.tqdm(total=TOTAL_PBAR_VALUE, desc="memory vs RSE sketches", colour="#00bfff", unit="sketch", mininterval=10.0)
    for label, make_sketch in configs:
        max_m = M_START
        while get_memory(make_sketch, max_m + 1) <= MAX_MEMORY_BYTES:
            max_m += 1
        m_list = sorted(set(int(x) for x in np.linspace(M_START, max_m, N_POINTS)))

        mem_list: list[int] = []
        rse_list: list[float] = []
        for m in m_list:
            mem_list.append(get_memory(make_sketch, m))
            rse_list.append(measure_rse(make_sketch, m))
        all_memory.append(mem_list)
        all_rse.append(rse_list)
        all_m_values.append(m_list)
        labels.append(label)
        pbar.update(1)
    pbar.close()

    out.save_dataclass(
        DataModel(
            memory_values=all_memory,
            rse_values=all_rse,
            labels=labels,
            m_values=all_m_values,
            n_reps=N_REPS,
            b=B,
        ),
        DataModel,
    )


if __name__ == "__main__":
    main()

# ---
# description: "RSE vs total memory budget (512-4096 bytes) for five weighted cardinality sketches on a weighted stream, picking the largest m that fits each budget"
# ---
"""
Experiment: Memory-to-accuracy sweep.

For each sketch and each total-memory budget in [512, 4096] bytes we pick the
largest register count m whose total memory footprint fits the budget, then
measure the empirical RSE. Each repetition inserts a fresh weighted stream of
n distinct elements whose weights are drawn from a Uniform distribution and
normalised to sum to the target weighted cardinality Lambda.

The quantized sketches (QSketch, kQSketch*, LogExpSketch) pack more registers
into the same number of bytes than FastExpSketchFloat32, so at a fixed memory
budget they reach a lower RSE.

Parallelism: set the WORKERS env var (e.g. WORKERS=8) to fan the per-cell RSE
computations out over a process pool. Each (sketch, memory budget) cell is an
independent task; the tqdm bar advances as reps complete (per-cell granularity,
since worker processes cannot update the parent's bar directly). Seeds come from
a single SeedSequence, so the result is identical regardless of how many workers
run or the order cells finish in.
"""

import os

import numpy as np
import tqdm

from weighted_cardinality_estimation import (
    FastExpSketchFloat32,
    LogExpSketchFastNoShifted,
    LogExpSketchSlowShifted,
    QSketch,
    kQSketchRounding,
    kQSketchShifted,
    MemoryFlag,
    stat,
)
from generated_output_manager import DRAFT, DraftLevel, GeneratedOutputManager
from data_for_figure_dataclass import DataModel

# REVIEWED AND ACCEPTED DRAFT VARIABLES. Each rep now inserts a weighted stream
# of N_ELEMENTS items, so per-rep cost is ~N_ELEMENTS larger than the old
# single-element stream; reps/points reduced accordingly.
# BENCHMARK: DRAFT=0: minutes, DRAFT=1: ~40s, DRAFT=2: ~2s.
match DRAFT:
    case DraftLevel.DRAFT_FINAL_VERSION:
        N_REPS = 100000
        N_POINTS = 50
    case DraftLevel.DRAFT_FOR_HUMAN_TO_VIEW_LATEX:
        N_REPS = 100
        N_POINTS = 10
    case DraftLevel.DRAFT_TO_FIX_EXPERIMENT_OR_SEE_IF_IT_COMPILES:
        N_REPS = 5
        N_POINTS = 6

N_ELEMENTS = 10              # distinct elements per stream
TOTAL_WEIGHT = 1000.0          # true weighted cardinality Lambda (sum of weights)
WEIGHT_DIST = stat.Uniform()   # weight distribution before normalisation
DIST_NAME = "uniform"

MEM_MIN_BYTES = 512
MEM_MAX_BYTES = 8192
K_BASE = 1.5
MEM_FLAGS = MemoryFlag.TOTAL

BASE_SEED = 1234
WORKERS = int(os.environ.get("WORKERS", "16"))

# Picklable sketch specs (lambdas can't cross a process boundary). Each spec is a
# (label, dict) pair consumed by make_sketch_from_spec below.
LOGEXPSKETCH_SHIFTED_B = 6
LOGEXPSKETCH_SHIFTED_VMAX = 5*1e7
LOGEXPSKETCH_SHIFTED_B_TEXT = "$b=" + str(LOGEXPSKETCH_SHIFTED_B) + "$"
LOGEXPSKETCH_SHIFTED_VMAX_TEXT = r"$ v_{\max} = " + str(LOGEXPSKETCH_SHIFTED_VMAX) + r"$"

LOGEXPSKETCH_SHIFTED_2_B = 10
LOGEXPSKETCH_SHIFTED_2_VMAX = 5*1e7
LOGEXPSKETCH_SHIFTED_2_B_TEXT = "$b=" + str(LOGEXPSKETCH_SHIFTED_2_B) + "$"
LOGEXPSKETCH_SHIFTED_2_VMAX_TEXT = r"$ v_{\max} = " + str(LOGEXPSKETCH_SHIFTED_2_VMAX) + r"$"

CONFIGS = [
    ("FastExpSketchFloat32", {"kind": "float32"}),
    ("QSketch(b=8)", {"kind": "qsketch", "b": 8}),
    ("kQSketchShifted(b=6)", {"kind": "kqshifted", "b": 6}),
    ("kQSketchRounding(b=8)", {"kind": "kqrounding", "b": 8}),
    # (r"LogExpSketch(b=11, $v_{\max}\approx 1.70\cdot10^{38}$)", {"kind": "logexp", "b": 11, "v_max": 2.0 ** 127}),
    # Slow shifted variant — there is no fast-shifted implementation yet, so we run the
    # slow one but charge it the Fisher-Yates memory the fast version would carry (see
    # get_memory / cheat_fisher_yates), keeping the byte budget comparison honest.
    (f"LogExpSketch Shifted({LOGEXPSKETCH_SHIFTED_2_B_TEXT},{LOGEXPSKETCH_SHIFTED_2_VMAX_TEXT})", 
     {"kind": "logexp_shifted_slow", "b": LOGEXPSKETCH_SHIFTED_2_B, "v_max": LOGEXPSKETCH_SHIFTED_2_VMAX, "cheat_fisher_yates": True}),
    (f"LogExpSketch Shifted({LOGEXPSKETCH_SHIFTED_B_TEXT},{LOGEXPSKETCH_SHIFTED_VMAX_TEXT})", 
     {"kind": "logexp_shifted_slow", "b": LOGEXPSKETCH_SHIFTED_B, "v_max": LOGEXPSKETCH_SHIFTED_VMAX, "cheat_fisher_yates": True}),
]


def make_sketch_from_spec(spec: dict, m: int, seed: int):
    """Picklable sketch factory (lambdas can't cross a process boundary)."""
    kind = spec["kind"]
    if kind == "float32":
        return FastExpSketchFloat32(m, seed=seed)
    if kind == "qsketch":
        return QSketch(m, seed=seed, amount_bits=spec["b"])
    if kind == "kqshifted":
        return kQSketchShifted(m, seed=seed, amount_bits=spec["b"], logarithm_base=K_BASE)
    if kind == "kqrounding":
        return kQSketchRounding(m, seed=seed, amount_bits=spec["b"], logarithm_base=K_BASE)
    if kind == "logexp_shifted_slow":
        return LogExpSketchSlowShifted(m, seed=seed, amount_bits=spec["b"], v_max=spec["v_max"])
    return LogExpSketchFastNoShifted(m, seed=seed, amount_bits=spec["b"], v_max=spec["v_max"])


def get_memory(spec: dict, m: int) -> int:
    s = make_sketch_from_spec(spec, m, 0).memory_usage(MEM_FLAGS)
    if spec.get("cheat_fisher_yates"):
        # The slow shifted sketch has no Fisher-Yates permutation, so its memory_usage
        # omits that term; the eventual fast version would carry it. Charge for it here
        # (it depends only on m) so the chosen m reflects the fast version's footprint.
        s += FastExpSketchFloat32(m, seed=0).memory_usage(MemoryFlag.FISHER_YATES)
    return s


def find_m_for_bytes(spec: dict, target_bytes: int) -> int:
    """Largest register count m whose total memory fits within target_bytes."""
    hi = 1
    while get_memory(spec, hi) <= target_bytes:
        hi *= 2
    lo = 1
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if get_memory(spec, mid) <= target_bytes:
            lo = mid
        else:
            hi = mid - 1
    return lo


def _cell_task(args):
    """One (config, budget) cell: pick m for the budget, then RSE over N_REPS streams.

    Returns (cfg_idx, point_idx, m, memory, rse, N_REPS).
    """
    cfg_idx, point_idx, spec, target, seed_seq = args
    rng = np.random.default_rng(seed_seq)

    def get_seed() -> int:
        return int(rng.integers(np.iinfo(np.int32).max))

    m = find_m_for_bytes(spec, target)
    memory = get_memory(spec, m)
    estimates = np.empty(N_REPS)
    for rep in range(N_REPS):
        elements, weights = stat.weighted_stream(
            N_ELEMENTS, TOTAL_WEIGHT, WEIGHT_DIST, seed=get_seed()
        )
        s = make_sketch_from_spec(spec, m, get_seed())
        s.add_many(elements, weights)
        estimates[rep] = stat.relative_error(s.estimate(), TOTAL_WEIGHT)
    rse = float(np.sqrt(np.mean(estimates**2)))
    return (cfg_idx, point_idx, m, memory, rse, N_REPS)


def main() -> None:
    out = GeneratedOutputManager(__file__)

    labels = [label for label, _ in CONFIGS]
    byte_budgets = [int(b) for b in np.linspace(MEM_MIN_BYTES, MEM_MAX_BYTES, N_POINTS)]

    all_memory: list[list[int]] = [[0] * N_POINTS for _ in CONFIGS]
    all_rse: list[list[float]] = [[0.0] * N_POINTS for _ in CONFIGS]
    all_m_values: list[list[int]] = [[0] * N_POINTS for _ in CONFIGS]

    # One independent, reproducible seed per cell, so the result is identical
    # regardless of WORKERS or the order cells complete in.
    seeds = np.random.SeedSequence(BASE_SEED).spawn(len(CONFIGS) * N_POINTS)
    tasks = []
    k = 0
    for cfg_idx, (_, spec) in enumerate(CONFIGS):
        for point_idx, target in enumerate(byte_budgets):
            tasks.append((cfg_idx, point_idx, spec, target, seeds[k]))
            k += 1

    TOTAL_PBAR_VALUE = len(CONFIGS) * N_POINTS * N_REPS
    pbar = tqdm.tqdm(
        total=TOTAL_PBAR_VALUE,
        desc=f"memory-to-accuracy sweep (workers={WORKERS})",
        colour="#9467bd",
        unit="rep",
        mininterval=10.0,
    )

    def store(result) -> None:
        cfg_idx, point_idx, m, memory, rse, n_reps = result
        all_m_values[cfg_idx][point_idx] = m
        all_memory[cfg_idx][point_idx] = memory
        all_rse[cfg_idx][point_idx] = rse
        pbar.update(n_reps)

    if WORKERS > 1:
        from concurrent.futures import ProcessPoolExecutor, as_completed

        with ProcessPoolExecutor(max_workers=WORKERS) as executor:
            futures = [executor.submit(_cell_task, args) for args in tasks]
            for future in as_completed(futures):
                store(future.result())
    else:
        for args in tasks:
            store(_cell_task(args))

    pbar.close()

    out.save_dataclass(
        DataModel(
            memory_values=all_memory,
            rse_values=all_rse,
            m_values=all_m_values,
            labels=labels,
            n_reps=N_REPS,
            n_elements=N_ELEMENTS,
            total_weight=TOTAL_WEIGHT,
            dist_name=DIST_NAME,
            k_base=K_BASE,
        ),
        DataModel,
    )


if __name__ == "__main__":
    main()

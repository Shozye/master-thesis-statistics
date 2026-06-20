# ---
# description: Mean addition time and mean relative error vs m for FastExpSketch across 4 RNG engines, combined into one figure with 2 subplots
# ---
"""
Measures mean addition time (μs/element) and mean relative error as a function
of sketch size m for FastExpSketch, separately for each of the four RNG engines.
Demonstrates that RNG engine choice has no material effect on performance or
accuracy; findings extrapolate to all Fisher-Yates-based sketches.
"""

import time

import numpy as np
import tqdm

from weighted_cardinality_estimation import (
    FastExpSketch,
    RngEngine,
    stat,
)
from generated_output_manager import DRAFT, DraftLevel, GeneratedOutputManager
from data_for_figure_dataclass import DataModel

# REVIEWED AND ACCEPTED DRAFT VARIABLES.
# BENCHMARK: DRAFT=0: >80s, DRAFT=1: ~57s, DRAFT=2: 1.3s.
match DRAFT:
    case DraftLevel.DRAFT_FINAL_VERSION:
        N_REPS = 5000
        N_POINTS = 30
        M_MAX = 200
    case DraftLevel.DRAFT_FOR_HUMAN_TO_VIEW_LATEX:
        N_REPS = 500
        N_POINTS = 15
        M_MAX = 100
    case DraftLevel.DRAFT_TO_FIX_EXPERIMENT_OR_SEE_IF_IT_COMPILES:
        N_REPS = 5
        N_POINTS = 5
        M_MAX = 100

N_ELEMENTS = 1000
LAMBDA = 10.0
M_RANGE = (50, M_MAX)
RNGS = [
    ("PCG64", RngEngine.PCG64),
    ("MT19937", RngEngine.MT19937),
    ("XOSHIRO128PP", RngEngine.XOSHIRO128PP),
    ("XOSHIRO256PP", RngEngine.XOSHIRO256PP),
]


def main() -> None:
    out = GeneratedOutputManager(__file__)

    ms = np.linspace(M_RANGE[0], M_RANGE[1], N_POINTS, dtype=int).tolist()
    elems, weights = stat.weighted_stream(N_ELEMENTS, LAMBDA, seed=37)

    times: dict[str, list[float]] = {}
    errors: dict[str, list[float]] = {}

    TOTAL_PBAR_VALUE = len(RNGS) * len(ms)
    pbar = tqdm.tqdm(total=TOTAL_PBAR_VALUE, desc="FastExpSketch RNG comparison", colour="green", unit="pt", mininterval=10.0)

    for rng_name, rng_enum in RNGS:
        time_per_m: list[float] = []
        error_per_m: list[float] = []
        rng = np.random.default_rng(100)

        for m in ms:
            durations = []
            errs = []
            for rep in range(N_REPS):
                sk = FastExpSketch(m, int(rng.integers(0, 2**63)), rng_enum)
                t0 = time.perf_counter()
                sk.add_many(elems, weights)
                t1 = time.perf_counter()
                durations.append((t1 - t0) * 1e6 / N_ELEMENTS)
                errs.append(stat.relative_error(sk.estimate(), LAMBDA))
            time_per_m.append(float(np.mean(durations)))
            error_per_m.append(float(np.mean(errs)))
            pbar.update(1)

        times[rng_name] = time_per_m
        errors[rng_name] = error_per_m

    pbar.close()

    out.save_dataclass(
        DataModel(
            ms=ms,
            times=times,
            errors=errors,
            n_reps=N_REPS,
            n_elements=N_ELEMENTS,
        ),
        DataModel,
    )


if __name__ == "__main__":
    main()

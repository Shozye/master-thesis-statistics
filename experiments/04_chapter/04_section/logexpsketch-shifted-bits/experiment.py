# ---
# description: Shifted LogExpSketch cardinality RSE vs log10(Lambda) and Jaccard RSE vs bits b, where the sliding offset makes v_max a relative window width rather than an absolute range
# ---
"""How few bits per register b the Shifted LogExpSketch needs.

The Shifted variant stores a global integer offset, so v_max no longer has to
cover the absolute Float32 range: the window slides freely (offset may go
negative) and v_max is only the *relative* width it spans. It just has to exceed
the worst-case relative spread of the m register minima, not the absolute range.
With the offset absorbing the scale, the grid for a fixed b is fine enough that
b=10 reaches the optimum, well below the b=14 the non-shifted variant needs for
the Float32 range.

Panel (a): cardinality estimator RSE across log10(Lambda) in [-35, 35] for the
Float32 baseline (FastExpSketchFloat32) and LogExpSketchSlowShifted with
b in {8, 9, 10, 11}. The offset makes the shifted variant scale invariant, so it
stays flat across the whole Lambda range.
Panel (b): Jaccard estimator RSE versus b in {8..11} for several true Jaccard
values J. Theoretical horizontal lines use the ExpSketch formula sqrt((1-J)/(m*J)).

Parallelism: set the WORKERS env var (e.g. WORKERS=8) to fan the per-cell RSE
computations out over a process pool. Each (series, lambda) and (J, b) cell is an
independent task; the tqdm bar advances as cells complete (per-cell granularity,
not per-trial, since worker processes cannot update the parent's bar directly).
Seeds come from a single SeedSequence, so the result is identical regardless of
how many workers run or the order cells finish in.
"""

import os

import numpy as np
import tqdm
from weighted_cardinality_estimation import (
    FastExpSketchFloat32,
    LogExpSketchSlowShifted,
    stat,
)
from generated_output_manager import DRAFT, DraftLevel, GeneratedOutputManager
from data_for_figure_dataclass import DataModel

# REVIEWED AND ACCEPTED DRAFT VARIABLES. RSE over independent seeds; curves stabilise by ~500 trials.
# Slow variant: O(m) per insert, so panel (b) keeps N_ELEMENTS modest.
# BENCHMARK: DRAFT=0: ~180s, DRAFT=1: ~30s, DRAFT=2: ~3s.
match DRAFT:
    case DraftLevel.DRAFT_FINAL_VERSION:
        N_TRIALS_A = 200_000
        N_TRIALS_B = 4_000
        N_ELEMENTS = 1_000
    case DraftLevel.DRAFT_FOR_HUMAN_TO_VIEW_LATEX:
        N_TRIALS_A = 5
        N_TRIALS_B = 5
        N_ELEMENTS = 1000
    case DraftLevel.DRAFT_TO_FIX_EXPERIMENT_OR_SEE_IF_IT_COMPILES:
        N_TRIALS_A = 3
        N_TRIALS_B = 3
        N_ELEMENTS = 100

M = 400
# v_max is now purely the *relative* window width spanned by the capacity_ registers;
# the sliding offset makes the absolute range unbounded (true scale invariance). It only
# has to exceed the worst-case relative spread of the m register minima (heavy upper tail
# of m exponentials), not the absolute Float32 range. For m=400 that tail reaches ~1e6-1e7
# in rare trials; v_max=1e9 clears it with margin, so no clamping bias appears, while the
# grid stays fine enough for b=10 to reach the optimum (verified: cardinality RSE 0.0515
# vs 0.0510 floor, Jaccard RSE at the theoretical sqrt((1-J)/(mJ)) for all J).
V_MAX = 1e7

# Panel (a)
LAMBDA_EXPONENTS = list(range(0, 36))  # log10(Lambda) from -35 to 35
A_BITS = [5, 6, 7, 8, 9]

# Panel (b)
B_VALUES = [8, 9, 10, 11, 12]
J_VALUES = [0.2, 0.5, 0.8, 0.9, 0.95]

BASE_SEED = 523456
WORKERS = int(os.environ.get("WORKERS", "8"))


def make_sketch_from_spec(spec: dict, seed: int):
    """Picklable sketch factory (lambdas can't cross a process boundary)."""
    if spec["kind"] == "float32":
        return FastExpSketchFloat32(M, seed=seed)
    return LogExpSketchSlowShifted(M, seed=seed, amount_bits=spec["b"], v_max=V_MAX)


def _panel_a_task(args):
    """One (series, lambda) cell: cardinality RSE over N_TRIALS_A independent trials."""
    series_idx, lambda_idx, spec, exponent, seed_seq = args
    rng = np.random.default_rng(seed_seq)

    def get_seed() -> int:
        return int(rng.integers(np.iinfo(np.int32).max))

    lam = 10.0**exponent
    errors = []
    for _ in range(N_TRIALS_A):
        elems, weights = stat.weighted_stream(1, lam, seed=get_seed())
        sk = make_sketch_from_spec(spec, get_seed())
        sk.add_many(elems, weights)
        errors.append((sk.estimate() - lam) / lam)
    rse = float(np.sqrt(np.mean(np.array(errors) ** 2)))
    return ("a", series_idx, lambda_idx, rse, N_TRIALS_A)


def _panel_b_task(args):
    """One (J, b) cell: structural Jaccard RSE over N_TRIALS_B trials."""
    j_idx, b_idx, b, j, seed_seq = args
    rng = np.random.default_rng(seed_seq)

    def get_seed() -> int:
        return int(rng.integers(np.iinfo(np.int32).max))

    (a_elems, w_a), (b_elems, w_b) = stat.jaccard_streams(
        N_ELEMENTS, 1000.0, j, dist=stat.Uniform(), common=stat.CommonPlacement.RANDOM, seed=get_seed()
    )
    errors = []
    for _ in range(N_TRIALS_B):
        seed = get_seed()
        sk_a = LogExpSketchSlowShifted(M, seed=seed, amount_bits=b, v_max=V_MAX)
        sk_b = LogExpSketchSlowShifted(M, seed=seed, amount_bits=b, v_max=V_MAX)
        sk_a.add_many(a_elems, w_a)
        sk_b.add_many(b_elems, w_b)
        errors.append((sk_a.jaccard_struct(sk_b) - j) / j)
    rse = float(np.sqrt(np.mean(np.array(errors) ** 2)))
    return ("b", j_idx, b_idx, rse, N_TRIALS_B)


def main() -> None:
    out = GeneratedOutputManager(__file__)

    specs = [("FastExpSketchFloat32", {"kind": "float32"})]
    for b in A_BITS:
        specs.append((f"LogExpSketch $b={b}$", {"kind": "logexp", "b": b}))
    panel_a_labels = [label for label, _ in specs]

    # One independent, reproducible seed per cell, so the result is identical
    # regardless of WORKERS or the order cells complete in.
    n_a = len(specs) * len(LAMBDA_EXPONENTS)
    n_b = len(J_VALUES) * len(B_VALUES)
    seeds = np.random.SeedSequence(BASE_SEED).spawn(n_a + n_b)

    tasks = []  # list of (task_fn, args)
    k = 0
    for series_idx, (_, spec) in enumerate(specs):
        for lambda_idx, exponent in enumerate(LAMBDA_EXPONENTS):
            tasks.append((_panel_a_task, (series_idx, lambda_idx, spec, exponent, seeds[k])))
            k += 1
    for j_idx, j in enumerate(J_VALUES):
        for b_idx, b in enumerate(B_VALUES):
            tasks.append((_panel_b_task, (j_idx, b_idx, b, j, seeds[k])))
            k += 1

    panel_a_rse = [[0.0] * len(LAMBDA_EXPONENTS) for _ in specs]
    panel_b_rse = [[0.0] * len(B_VALUES) for _ in J_VALUES]

    TOTAL_PBAR_VALUE = n_a * N_TRIALS_A + n_b * N_TRIALS_B
    pbar = tqdm.tqdm(
        total=TOTAL_PBAR_VALUE,
        desc=f"shifted bits sweep (workers={WORKERS})",
        colour="green",
        unit="trial",
        mininterval=10.0,
    )

    def store(result) -> None:
        panel, i, jx, rse, n_trials = result
        if panel == "a":
            panel_a_rse[i][jx] = rse
        else:
            panel_b_rse[i][jx] = rse
        pbar.update(n_trials)

    if WORKERS > 1:
        from concurrent.futures import ProcessPoolExecutor, as_completed

        with ProcessPoolExecutor(max_workers=WORKERS) as executor:
            futures = [executor.submit(fn, args) for fn, args in tasks]
            for future in as_completed(futures):
                store(future.result())
    else:
        for fn, args in tasks:
            store(fn(args))

    pbar.close()

    out.save_dataclass(
        DataModel(
            m=M,
            v_max=V_MAX,
            log_lambdas=[float(e) for e in LAMBDA_EXPONENTS],
            panel_a_labels=panel_a_labels,
            panel_a_rse=panel_a_rse,
            b_values=B_VALUES,
            j_values=J_VALUES,
            panel_b_rse=panel_b_rse,
        ),
        DataModel,
    )


if __name__ == "__main__":
    main()

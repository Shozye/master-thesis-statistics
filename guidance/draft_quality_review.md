# DRAFT Quality Parameter Review (2026-06-14)

All 26 experiments have been reviewed to determine appropriate DRAFT=0 (final) quality
parameters. Every experiment now has a `# HUMAN APPROVED DRAFT VARIABLES` comment above
its `match DRAFT:` block confirming the values are intentional.

## Methodology

For each experiment, we assessed:
1. **What metric** is produced (RSE, MRE, timing, histogram, table)
2. **Output precision** (decimal places shown, plot vs table)
3. **Convergence threshold** — the N_REPS at which further increases cause no visible change in the output

Key statistical principles applied:
- RSE estimation error ≈ 1/√(2·N_REPS) — for 2 decimal place tables, ~10K reps suffices
- Line plots with no confidence bands: 300-1000 reps gives visually stable curves
- Histograms: shape stabilizes early; 1M+ total samples is always sufficient
- CLT mean estimation: std error = σ/√N — 500K samples gives error < 0.001

## Summary of Changes

### Reduced (over-specified for output precision)
| Experiment | Old | New | Reason |
|---|---|---|---|
| qsketch-memory-analysis | 250K | 10K | Table shows RSE to 2 decimal places |
| qsketch-memory-equivalence | 250K | 10K | Table shows RSE to 2 decimal places |
| qsketchdyn-memory-analysis | 100K | 10K | Table shows RSE to 2 decimal places |
| qsketch-register-distrib | 20K | 2K | Histogram; 2K×500 = 1M samples is plenty |
| frac-ln-stats-uniformity | 20M | 500K | CLT convergence; 500K gives std error < 0.001 |
| kqsketch-shifted-rse-vs-k | 50K | 20K | RSE plot; 20K gives ~0.7% estimation error |
| fisher-yates-rng-error-grid | 10K | 5K | MRE comparison; 5K sufficient to detect differences |
| expsketch-vs-wminhash-weights | 2K | 1K | Smooth MRE curves; 1K visually stable |
| memory-vs-error-comparison | 2K | 1K | RSE comparison plot; 1K sufficient |

### Increased (under-specified)
| Experiment | Old | New | Reason |
|---|---|---|---|
| expsketch-mantissa-accuracy | 120 | 500 | RSE from squared errors needs more samples; 120 gave noisy curves |

### Bug Fixed
| Experiment | Issue | Fix |
|---|---|---|
| kqsketch-rounding-accuracy | FINAL=1000, HUMAN=3000 (inverted) | FINAL=3000, HUMAN=300 |

### Kept Unchanged (already appropriate)
- expsketch-float-lambda-range: 400 reps
- expsketch-jaccard-mantissa: 500 trials
- float-vs-bits-error-compare: 400 reps
- float-vs-qsketch-error-sweep: 300 reps
- memory-vs-rse-comparison: 1000 reps
- newton-vs-direct-estimator: 1000 reps
- newton-warm-cold-direct-time: 300 reps
- kqsketch-shifted-comparison: 300 reps
- fisher-yates-rng-add-time: 200 reps
- kqsketch-shifted-rse-vs-k (reduced from 50K → 20K above)

### Trivial/Deterministic (no randomness, no convergence needed)
- float-formats-table-macheps: Deterministic IEEE 754 table
- kqsketch-shifted-parameters: Fixed seed=42, n_reps=1
- euler-maclaurin-p10-bound: Pure numerical computation
- fisher-info-loss-ratio: Deterministic numerical grid (N_POINTS=500)
- expsketch-register-histogram: Fixed seed=42, M=50000 (histogram smoothness)
- expsketch-lns-register-hist: Fixed seed=42, M=20000 (histogram smoothness)

## Verification

- All 26 experiments pass `just statistics-check` (contract validation)
- Key experiments verified at DRAFT=0:
  - qsketch-memory-analysis: ~2s ✓
  - kqsketch-rounding-accuracy: ~3.5min ✓
  - frac-ln-stats-uniformity: ~5s ✓
  - qsketch-register-distrib: ~16s ✓

## Note: expsketch-mantissa-accuracy Timeout

The `expsketch-mantissa-accuracy` experiment at N_REPS=500 takes ~10 minutes (7 custom
float configs × 50 lambdas × 500 reps). It exceeds the temporary 300s DRAFT=0 timeout
in `generated_output_manager.py`. The value is correct; the temporary timeout needs to
be removed for final thesis compilation runs.

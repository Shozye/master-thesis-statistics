# ---
# description: Fisher information loss ratio of k-QSketch vs ExpSketch for varying k and Lambda
# ---
"""
Fisher information loss ratio ρ(λ,k) = I_X(λ) / I_Z(λ) for k-QSketch with b=8 bits.

I_X(λ) = 1/λ²  (Fisher info of Exp(λ) with rate parameterization)
I_Z(λ) = Σ_{r=r_min}^{r_max} P(r) · (-∂²/∂λ² ln P(r))   [finite sum, eq. (4.8)]

where r_min = -2^{b-1}+1, r_max = 2^{b-1}-1 (for b=8: r_min=-127, r_max=127).
The r_min term vanishes. The r_max boundary term and middle terms follow
from the Ψ(k,Λ,b) distribution second derivatives.

ρ = I_X / I_Z ≥ 1; tells how many more registers k-QSketch needs vs ExpSketch.

Two subplots:
  Left:  ρ vs λ (linear, 1 to 8) for several fixed k — shows near-constancy
  Right: ρ vs k (linear, 1.1 to 2.5) for several fixed λ — shows main dependence
"""

import numpy as np
import mpmath

from generated_output_manager import DRAFT, DraftLevel, GeneratedOutputManager
from data_for_figure_dataclass import DataModel

# REVIEWED AND ACCEPTED DRAFT VARIABLES. Deterministic; N_POINTS controls curve smoothness.
# BENCHMARK: DRAFT=0: 56.0s, DRAFT=1: 28.6s, DRAFT=2: 6.6s.
match DRAFT:
    case DraftLevel.DRAFT_FINAL_VERSION:
        N_POINTS = 100
    case DraftLevel.DRAFT_FOR_HUMAN_TO_VIEW_LATEX:
        N_POINTS = 50
    case DraftLevel.DRAFT_TO_FIX_EXPERIMENT_OR_SEE_IF_IT_COMPILES:
        N_POINTS = 10

B_BITS = 8
R_MIN = -2 ** (B_BITS - 1) + 1  # -127
R_MAX = 2 ** (B_BITS - 1) - 1   # 127
mpmath.mp.dps = 300

# Left subplot: fixed k values, sweep λ from 1 to 8
K_FIXED = [1.2, 1.5, 1.75, 2.0, 2.5]
LAMBDA_RANGE = (1.0, 8.0)

# Right subplot: fixed λ values, sweep k from 1.2 to 2.5
LAMBDA_FIXED = [1e-5, 1, 1e5]
K_RANGE = (1.2, 2.5)


def fisher_info_kqsketch(lam: float, k: float) -> float:
    """Compute I_Z(λ,k) via finite sum of -P(r)·∂²/∂λ² ln P(r), r in [r_min, r_max]."""
    lam_mp = mpmath.mpf(lam)
    k_mp = mpmath.mpf(k)
    total = mpmath.mpf(0)

    # r_min term vanishes (second derivative is 0)

    # Middle terms: r_min+1 to r_max-1
    for r in range(R_MIN + 1, R_MAX):
        kr = k_mp ** (-r)
        kr1 = k_mp ** (-(r + 1))
        denom = mpmath.exp(-lam_mp * kr1) - mpmath.exp(-lam_mp * kr)
        if denom <= 0:
            continue
        numer = (kr1 - kr) ** 2 * mpmath.exp(-lam_mp * (kr1 + kr))
        total += numer / denom

    # r_max boundary term
    kr_max = k_mp ** (-R_MAX)
    exp_term = mpmath.exp(-lam_mp * kr_max)
    denom_max = 1 - exp_term
    if denom_max > 0:
        total += kr_max ** 2 * exp_term / denom_max

    return float(total)


def info_loss_ratio(lam: float, k: float) -> float:
    """ρ = I_X(λ) / I_Z(λ,k) where I_X = 1/λ²."""
    iz = fisher_info_kqsketch(lam, k)
    if iz <= 0:
        return float("nan")
    ix = 1.0 / (lam ** 2)
    return ix / iz


def main() -> None:
    out = GeneratedOutputManager(__file__)

    lambdas = np.linspace(LAMBDA_RANGE[0], LAMBDA_RANGE[1], N_POINTS)
    ks = np.linspace(K_RANGE[0], K_RANGE[1], N_POINTS)

    # Precompute all data
    rhos_left = [[info_loss_ratio(lam, k) for lam in lambdas] for k in K_FIXED]
    rhos_right = [[info_loss_ratio(lam, k) for k in ks] for lam in LAMBDA_FIXED]
    rho_at_k2 = info_loss_ratio(1.0, 2.0)
    ks_fit = ks[ks >= 1.4]
    rhos_fit = [info_loss_ratio(1.0, k) for k in ks_fit]
    coeffs = np.polyfit(ks_fit, rhos_fit, 1)

    out.save_dataclass(DataModel(
        lambdas=lambdas.tolist(),
        k_fixed=K_FIXED,
        rhos_left=rhos_left,
        ks=ks.tolist(),
        lambda_fixed=LAMBDA_FIXED,
        rhos_right=rhos_right,
        rho_at_k2=float(rho_at_k2),
        linear_fit_coeffs=coeffs.tolist(),
        n_points=N_POINTS,
        b_bits=B_BITS,
        r_min=R_MIN,
        r_max=R_MAX,
    ), DataModel)


if __name__ == "__main__":
    main()

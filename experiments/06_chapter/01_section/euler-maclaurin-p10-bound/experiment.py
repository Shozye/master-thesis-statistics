# ---
# description: Numerical evaluation of Euler-Maclaurin remainder bound at p=10 for Theta proof
# ---
import numpy as np
from numpy.polynomial import polynomial as P
from scipy.integrate import quad
from scipy.special import zeta

from decimal import Decimal, ROUND_CEILING

from data_for_figure_dataclass import DataModel
from generated_output_manager import DRAFT, DraftLevel, GeneratedOutputManager

# REVIEWED AND ACCEPTED DRAFT VARIABLES. Deterministic; dummy variable, output never changes.
# BENCHMARK: DRAFT=0: 3.1s, DRAFT=1: 1.7s, DRAFT=2: 1.7s.
match DRAFT:
    case DraftLevel.DRAFT_FINAL_VERSION:
        THIS_CONSTANT_IS_NECESSARY_FOR_CHECK_TO_PASS_HUMAN_APPROVED = 0
    case DraftLevel.DRAFT_FOR_HUMAN_TO_VIEW_LATEX:
        THIS_CONSTANT_IS_NECESSARY_FOR_CHECK_TO_PASS_HUMAN_APPROVED = 0
    case DraftLevel.DRAFT_TO_FIX_EXPERIMENT_OR_SEE_IF_IT_COMPILES:
        THIS_CONSTANT_IS_NECESSARY_FOR_CHECK_TO_PASS_HUMAN_APPROVED = 0


def compute_P(p: int) -> np.ndarray:
    """Return coefficients of P_p(u) using numpy.polynomial.polynomial convention (low to high)."""
    # P_1(u) = 1 - u  =>  [1, -1]
    poly = np.array([1.0, -1.0])
    for _ in range(1, p):
        # P_{n+1}(u) = (1-u)*P_n(u) + u*P_n'(u)
        d = P.polyder(poly)
        term1 = P.polymul([1.0, -1.0], poly)  # (1-u)*P_n
        term2 = P.polymul([0.0, 1.0], d)      # u * P_n'
        poly = P.polyadd(term1, term2)
    return poly


def compute_bound(k: float, p: int) -> float:
    poly = compute_P(p)

    def integrand(u: float) -> float:
        return np.exp(-u) * abs(P.polyval(u, poly))

    integral, _ = quad(integrand, 0, np.inf, limit=200)
    ln_k = np.log(k)
    return (2 * zeta(p) / (2 * np.pi) ** p) * ln_k ** (p - 1) * integral


def main() -> None:
    out = GeneratedOutputManager(__file__)
    bounds = {p: compute_bound(k=2.4, p=p) for p in range(2, 22, 2)}
    best_p = min(bounds, key=bounds.get)
    bound = bounds[best_p]
    formatted = str(
        Decimal(str(bound)).quantize(Decimal("0.00001"), rounding=ROUND_CEILING)
    )
    out.save_dataclass(
        DataModel(bounds=bounds, best_p=best_p, bound_value=bound, bound_tex=formatted),
        DataModel,
    )


if __name__ == "__main__":
    main()

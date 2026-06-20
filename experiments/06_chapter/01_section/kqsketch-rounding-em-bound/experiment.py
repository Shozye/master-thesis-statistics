# ---
# description: Numerical evaluation of the Euler-Maclaurin remainder bound for the kQSketchRounding dequantizer constant
# ---
import numpy as np
from numpy.polynomial import polynomial as P
from scipy.integrate import quad
from scipy.special import zeta

from decimal import Decimal, ROUND_CEILING

from data_for_figure_dataclass import DataModel
from generated_output_manager import DRAFT, DraftLevel, GeneratedOutputManager

# REVIEWED AND ACCEPTED DRAFT VARIABLES. Deterministic; dummy variable, output never changes.
# BENCHMARK: DRAFT=0: 2.0s, DRAFT=1: 2.0s, DRAFT=2: 2.0s.
match DRAFT:
    case DraftLevel.DRAFT_FINAL_VERSION:
        THIS_CONSTANT_IS_NECESSARY_FOR_CHECK_TO_PASS_HUMAN_APPROVED = 0
    case DraftLevel.DRAFT_FOR_HUMAN_TO_VIEW_LATEX:
        THIS_CONSTANT_IS_NECESSARY_FOR_CHECK_TO_PASS_HUMAN_APPROVED = 0
    case DraftLevel.DRAFT_TO_FIX_EXPERIMENT_OR_SEE_IF_IT_COMPILES:
        THIS_CONSTANT_IS_NECESSARY_FOR_CHECK_TO_PASS_HUMAN_APPROVED = 0


def compute_Q(n: int, c: float) -> np.ndarray:
    """Coefficients (low to high) of the polynomial Q_n^c, defined so that the n-th derivative
    of x -> k^x e^{-c k^x} equals (ln k)^n * t * Q_n^c(t) * e^{-c t} with t = k^x.
    Recurrence: Q_0 = 1, Q_{n+1}(t) = (1 - c t) Q_n(t) + t Q_n'(t)."""
    poly = np.array([1.0])  # Q_0 = 1
    for _ in range(n):
        d = P.polyder(poly)
        term1 = P.polymul([1.0, -c], poly)  # (1 - c t) Q_n
        term2 = P.polymul([0.0, 1.0], d)    # t Q_n'
        poly = P.polyadd(term1, term2)
    return poly


def compute_bound(k: float, n: int) -> float:
    """Euler-Maclaurin remainder bound (times Lambda) at derivative order n for the rounding
    dequantizer, where g(t) = (t/Lambda)[e^{-t k^{-1/2}} - e^{-t k^{1/2}}]. The 2n-th derivative
    of f(x) = g(Lambda k^x) is integrated exactly as a single (polynomial)x(exponential), keeping
    the cancellation between the two exponential terms."""
    a, b = k**-0.5, k**0.5
    Qa, Qb = compute_Q(n, a), compute_Q(n, b)

    def integrand(t: float) -> float:
        return abs(P.polyval(t, Qa) * np.exp(-a * t) - P.polyval(t, Qb) * np.exp(-b * t))

    integral, _ = quad(integrand, 0, np.inf, limit=400)
    ln_k = np.log(k)
    return (2 * zeta(n) / (2 * np.pi) ** n) * ln_k ** (n - 1) * integral


def main() -> None:
    out = GeneratedOutputManager(__file__)
    bounds = {n: compute_bound(k=2.4, n=n) for n in range(2, 22, 2)}
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

# ---
# description: Numerical evaluation of the Euler-Maclaurin remainder bound for the floor second-moment constant
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


def compute_Q(n: int, c: float, m: int) -> np.ndarray:
    """Coefficients (low to high) of the polynomial Q_n, defined via the operator L = t d/dt so that
    L^n[t^m e^{-c t}] = t^m Q_n(t) e^{-c t}. Recurrence: Q_0 = 1, Q_{n+1}(t) = (m - c t) Q_n(t) + t Q_n'(t)."""
    poly = np.array([1.0])  # Q_0 = 1
    for _ in range(n):
        d = P.polyder(poly)
        term1 = P.polymul([float(m), -c], poly)  # (m - c t) Q_n
        term2 = P.polymul([0.0, 1.0], d)         # t Q_n'
        poly = P.polyadd(term1, term2)
    return poly


def compute_bound(k: float, n: int) -> float:
    """Euler-Maclaurin remainder bound (times Lambda^2) at even derivative order n for the floor
    second moment, where g(t) = t^2 e^{-t}/Lambda^2. Since f(x) = g(Lambda k^x) satisfies
    f^{(n)}(x) = (ln k)^n L^n g(t) with L = t d/dt, the n-th derivative is integrated exactly as a
    single (polynomial)x(exponential)."""
    Q = compute_Q(n, c=1.0, m=2)

    def integrand(t: float) -> float:
        return t * abs(P.polyval(t, Q)) * np.exp(-t)

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

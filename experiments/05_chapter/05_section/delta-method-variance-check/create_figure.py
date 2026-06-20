import numpy as np
import matplotlib.pyplot as plt

from generated_output_manager import GeneratedOutputManager
from data_for_figure_dataclass import DataModel

FIGURE_KEY = "delta-method-variance-check"

FLOOR_COLOR = "#1f77b4"
ROUND_COLOR = "#d62728"


def coef_floor(k: np.ndarray | float) -> np.ndarray | float:
    """Delta-method variance coefficient for floor quantization (kQSketch).

    Built from the floor-specific moments (Lambda = 1, coefficient is
    Lambda-invariant): the first moment mu, the second moment E[k^{-2R}], the
    register variance sigma_Y^2, and the estimator-map derivative f'(mu).
    """
    ln = np.log(k)
    mu = (k - 1.0) / ln                       # E[k^{-R}], floor
    e2 = (k**2 - 1.0) / ln                     # E[k^{-2R}], floor
    sigma2 = e2 - mu**2                         # register variance
    fprime_sq = (ln / (k - 1.0)) ** 2          # f'(mu)^2 with f(t) = (k-1)/(ln k . t)
    return fprime_sq * sigma2


def coef_round(k: np.ndarray | float) -> np.ndarray | float:
    """Delta-method variance coefficient for rounding quantization (kQSketchRounded).

    Built from the rounding-specific moments, which differ from the floor ones:
    the dequantizer constant C(k) is the first moment, E[k^{-2R}] carries a
    factor 1/k relative to floor, and f'(mu) = 1/C(k).
    """
    ln = np.log(k)
    c_k = (k - 1.0) / (np.sqrt(k) * ln)        # C(k) = E[k^{-R}], rounding
    mu = c_k
    e2 = (k - 1.0 / k) / ln                     # E[k^{-2R}], rounding (= floor / k)
    sigma2 = e2 - mu**2                          # register variance
    fprime_sq = (1.0 / c_k) ** 2                 # f'(mu)^2 with f(t) = C(k)/t
    return fprime_sq * sigma2


def get_caption(k_fixed: float, m_fixed: int, lam: float, n_reps: int) -> str:
    return (
        rf"Empirical RSE of the \kQSketch{{}} (floor) and \kQSketchRounded{{}} (rounding) "
        rf"direct estimators against their delta-method guarantees \(\sqrt{{c(k)/m}}\), "
        rf"where \(c(k)\) is computed separately from each rule's first and second "
        rf"register moments. Left: varying \(m\) at \(k={k_fixed:.0f}\). "
        rf"Right: varying \(k\) at \(m={m_fixed}\), normalised by \(\sqrt{{m}}\). "
        rf"\(\Lambda={lam:.0f}\), {n_reps} trials per point."
    )


def get_test_caption() -> str:
    return get_caption(k_fixed=2.0, m_fixed=1000, lam=1000.0, n_reps=5000)


def main() -> None:
    out = GeneratedOutputManager(__file__)
    data = out.load_dataclass(DataModel)

    ms = np.array(data.ms, dtype=float)
    ks = np.array(data.ks, dtype=float)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5))

    # ─── Left: RSE vs m at fixed k ───────────────────────────────────────────
    m_dense = np.geomspace(ms.min(), ms.max(), 200)
    ax1.plot(m_dense, np.sqrt(coef_floor(data.k_fixed) / m_dense), color=FLOOR_COLOR,
             linewidth=1.8, linestyle="--", label=r"floor theory $\sqrt{c_{\mathrm{floor}}(k)/m}$")
    ax1.plot(m_dense, np.sqrt(coef_round(data.k_fixed) / m_dense), color=ROUND_COLOR,
             linewidth=1.8, linestyle=":", label=r"round theory $\sqrt{c_{\mathrm{round}}(k)/m}$")
    ax1.plot(ms, data.rse_floor_m, color=FLOOR_COLOR, marker="o", linestyle="none",
             markersize=6, label="kQSketch (floor)")
    ax1.plot(ms, data.rse_round_m, color=ROUND_COLOR, marker="s", linestyle="none",
             markersize=6, markerfacecolor="none", label="kQSketchRounded")
    ax1.set_xscale("log")
    ax1.set_yscale("log")
    ax1.set_xlabel(r"$m$")
    ax1.set_ylabel("empirical RSE")
    ax1.set_title(rf"Varying $m$ at $k={data.k_fixed:.0f}$")
    ax1.legend()
    ax1.grid(True, which="both", alpha=0.3, linestyle="--")

    # ─── Right: RSE * sqrt(m) vs k at fixed m ───────────────────────────────
    k_dense = np.linspace(ks.min(), ks.max(), 200)
    sqrt_m = np.sqrt(data.m_fixed)
    ax2.plot(k_dense, np.sqrt(coef_floor(k_dense)), color=FLOOR_COLOR, linewidth=1.8,
             linestyle="--", label=r"floor theory $\sqrt{c_{\mathrm{floor}}(k)}$")
    ax2.plot(k_dense, np.sqrt(coef_round(k_dense)), color=ROUND_COLOR, linewidth=1.8,
             linestyle=":", label=r"round theory $\sqrt{c_{\mathrm{round}}(k)}$")
    ax2.plot(ks, np.array(data.rse_floor_k) * sqrt_m, color=FLOOR_COLOR, marker="o",
             linestyle="none", markersize=6, label="kQSketch (floor)")
    ax2.plot(ks, np.array(data.rse_round_k) * sqrt_m, color=ROUND_COLOR, marker="s",
             linestyle="none", markersize=6, markerfacecolor="none", label="kQSketchRounded")
    ax2.set_xlabel(r"$k$")
    ax2.set_ylabel(r"$\mathrm{RSE}\cdot\sqrt{m}$")
    ax2.set_title(rf"Varying $k$ at $m={data.m_fixed}$")
    ax2.legend()
    ax2.grid(True, alpha=0.3, linestyle="--")

    fig.tight_layout()
    out.savefig(fig, FIGURE_KEY)
    out.save_tex_figure(
        FIGURE_KEY,
        caption=get_caption(k_fixed=data.k_fixed, m_fixed=data.m_fixed,
                            lam=data.lam, n_reps=data.n_reps),
        label="delta-method-variance-check",
    )


if __name__ == "__main__":
    main()

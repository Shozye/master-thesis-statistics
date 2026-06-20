import numpy as np
import matplotlib.pyplot as plt

from generated_output_manager import GeneratedOutputManager
from data_for_figure_dataclass import DataModel

FIGURE_KEY = "newton-vs-direct-estimator"


def get_caption(m_fixed: int, lam_fixed: float, n_reps: int, k: float = 2.0, b_bits: int = 8) -> str:
    return (
        rf"RSE of Direct, Newton-Cold, and Newton-Warm estimators for \(k\)-QSketch "
        rf"(\(k={k:.0f}\), \(b={b_bits}\)). "
        rf"Left: fixed \(m={m_fixed}\), varying \(\Lambda\). "
        rf"Right: fixed \(\Lambda={lam_fixed:.0f}\), varying \(m\). "
        rf"{n_reps} repetitions per point."
    )


def get_test_caption() -> str:
    return get_caption(m_fixed=400, lam_fixed=1000, n_reps=50)


def main() -> None:
    out = GeneratedOutputManager(__file__)
    data = out.load_dataclass(DataModel)

    exponents = np.array(data.exponents)
    ms = np.array(data.ms)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5))

    for ax, x, rd, rc, rw, xlabel, title in [
        (ax1, exponents, data.rse_d1, data.rse_c1, data.rse_w1, r"$\log_{10}(\Lambda)$",
         rf"Fixed $m={data.m_fixed}$, varying $\Lambda$"),
        (ax2, ms, data.rse_d2, data.rse_c2, data.rse_w2, r"$m$",
         rf"Fixed $\Lambda={data.lam_fixed:.0f}$, varying $m$"),
    ]:
        ax.plot(x, rd, color="#d62728", linewidth=2, label="Direct")
        ax.plot(x, rc, color="#2ca02c", linewidth=2, linestyle="-.", label="Newton-Cold")
        ax.plot(x, rw, color="#1f77b4", linewidth=2, linestyle="--", label="Newton-Warm")
        ax.set_xlabel(xlabel)
        ax.set_ylabel("RSE")
        ax.set_title(title)
        ax.legend()
        ax.grid(True, alpha=0.3, linestyle="--")
    inner = np.abs(np.array(exponents)) <= 35
    all_vals = np.concatenate([np.array(data.rse_d1)[inner], np.array(data.rse_c1)[inner],
                               np.array(data.rse_w1)[inner]])
    ax1.set_ylim(np.nanmin(all_vals) * 0.9, np.nanmax(all_vals) * 1.1)

    fig.tight_layout()
    out.savefig(fig, FIGURE_KEY)
    out.save_tex_figure(
        FIGURE_KEY,
        caption=get_caption(m_fixed=data.m_fixed, lam_fixed=data.lam_fixed, n_reps=data.n_reps,
                            k=data.k, b_bits=data.b_bits),
        label="newton-vs-direct-estimator",
    )


if __name__ == "__main__":
    main()

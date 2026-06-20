import numpy as np
import matplotlib.pyplot as plt

from generated_output_manager import GeneratedOutputManager
from data_for_figure_dataclass import DataModel

FIGURE_KEY = "newton-warm-cold-direct-time"


def get_caption(lam_fixed: float, m_fixed: int, n_reps: int, k: float = 2.0, b_bits: int = 8) -> str:
    return (
        rf"Estimation cost for \(k\)-QSketch (\(k={k:.0f}\), \(b={b_bits}\)). "
        rf"Left: time vs \(m\) (\(\Lambda={lam_fixed:.0f}\)). "
        rf"Middle: iterations vs \(m\) (\(\Lambda={lam_fixed:.0f}\)). "
        rf"Right: iterations vs \(\Lambda\) (\(m={m_fixed}\)). "
        rf"{n_reps} repetitions per point."
    )


def get_test_caption() -> str:
    return get_caption(lam_fixed=1000, m_fixed=400, n_reps=50)


def main() -> None:
    out = GeneratedOutputManager(__file__)
    data = out.load_dataclass(DataModel)

    ms = np.array(data.ms)
    exponents = np.array(data.exponents)

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 4.5))

    # Left: time vs m
    ax1.plot(ms, np.array(data.time_direct) * 1e6, color="#d62728", linewidth=2, label="Direct")
    ax1.plot(ms, np.array(data.time_cold) * 1e6, color="#2ca02c", linewidth=2, linestyle="-.",
             label="Newton-Cold")
    ax1.plot(ms, np.array(data.time_warm) * 1e6, color="#1f77b4", linewidth=2, linestyle="--",
             label="Newton-Warm")
    ax1.set_xlabel(r"$m$")
    ax1.set_ylabel(r"Time [$\mu$s]")
    ax1.set_title(rf"Time, $\Lambda={data.lam_fixed:.0f}$")
    ax1.legend()
    ax1.grid(True, alpha=0.3, linestyle="--")

    # Middle: iterations vs m
    ax2.plot(ms, data.iters_cold_m, color="#2ca02c", linewidth=2, linestyle="-.", label="Newton-Cold")
    ax2.plot(ms, data.iters_warm_m, color="#1f77b4", linewidth=2, linestyle="--", label="Newton-Warm")
    ax2.set_xlabel(r"$m$")
    ax2.set_ylabel("Iterations")
    ax2.set_title(rf"Iterations, $\Lambda={data.lam_fixed:.0f}$")
    ax2.legend()
    ax2.grid(True, alpha=0.3, linestyle="--")

    # Right: iterations vs Lambda
    ax3.plot(exponents, data.iters_cold_lam, color="#2ca02c", linewidth=2, linestyle="-.",
             label="Newton-Cold")
    ax3.plot(exponents, data.iters_warm_lam, color="#1f77b4", linewidth=2, linestyle="--",
             label="Newton-Warm")
    ax3.set_xlabel(r"$\log_{10}(\Lambda)$")
    ax3.set_ylabel("Iterations")
    ax3.set_title(rf"Iterations, $m={data.m_fixed}$")
    ax3.legend()
    ax3.grid(True, alpha=0.3, linestyle="--")

    fig.tight_layout()
    out.savefig(fig, FIGURE_KEY)
    out.save_tex_figure(
        FIGURE_KEY,
        caption=get_caption(lam_fixed=data.lam_fixed, m_fixed=data.m_fixed, n_reps=data.n_reps,
                            k=data.k, b_bits=data.b_bits),
        label="newton-time-iterations",
    )


if __name__ == "__main__":
    main()

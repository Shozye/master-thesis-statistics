import numpy as np
import matplotlib.pyplot as plt

from generated_output_manager import GeneratedOutputManager
from data_for_figure_dataclass import DataModel

FIGURE_KEY = "newton-graphic-iteration"

COLOR_DIAGONAL = "#7f7f7f"
COLOR_MAP = "#9467bd"
COLOR_COBWEB = "#2ca02c"
COLOR_START = "#d62728"
COLOR_ITER = "#1f77b4"
COLOR_FIXED = "#ff7f0e"


def get_caption(lambda_true: float, m: int, k: float, b_bits: int) -> str:
    return (
        rf"Newton-Raphson estimation for \(k\)-QSketch (\(m={m}\), \(k={k:.0f}\), "
        rf"\(b={b_bits}\), \(\Lambda={lambda_true:.0e}\)) seen as a fixed-point map "
        rf"\(g\). Left: cold start \(\Lambda_0=k^{{r_{{\min}}}}\). "
        rf"Right: warm start from the direct estimator, zoomed near the fixed point."
    )


def get_test_caption() -> str:
    return get_caption(lambda_true=1e6, m=256, k=2.0, b_bits=8)


def cobweb_path(traj: list[float]) -> tuple[list[float], list[float]]:
    """Build the staircase of a fixed-point iteration from its iterates."""
    xs = [traj[0]]
    ys = [traj[0]]
    for w, w_next in zip(traj[:-1], traj[1:]):
        xs += [w, w_next]
        ys += [w_next, w_next]
    return xs, ys


def draw_panel(ax, lam, g, traj, start, root, n_steps_label: str) -> None:
    lo = min(lam)
    hi = max(lam)
    diag = np.array([lo, hi])

    ax.plot(diag, diag, color=COLOR_DIAGONAL, linewidth=1.5, linestyle="--",
            label=r"$y=\Lambda$")
    ax.plot(lam, g, color=COLOR_MAP, linewidth=2.2, label=r"$g(\Lambda)$")

    cx, cy = cobweb_path(traj)
    ax.plot(cx, cy, color=COLOR_COBWEB, linewidth=1.4, label="graphic iteration")

    # Intermediate iterates Lambda_1, Lambda_2, ... sit on the diagonal.
    mid = traj[1:-1]
    if mid:
        ax.plot(mid, mid, "o", color=COLOR_ITER, markersize=6,
                label=r"$\Lambda_n\ (n\geq1)$", zorder=5)
    ax.plot([start], [start], "o", color=COLOR_START, markersize=8,
            label=r"$\Lambda_0$", zorder=6)
    ax.plot([root], [root], "*", color=COLOR_FIXED, markersize=14,
            label="fixed point", zorder=7)

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(lo, hi)
    ax.set_ylim(lo, hi)
    ax.set_xlabel(r"$\Lambda_n$")
    ax.set_ylabel(r"$\Lambda_{n+1}$")
    ax.set_title(n_steps_label)
    ax.grid(True, alpha=0.3, linestyle="--")
    ax.legend(loc="upper left", fontsize=9)


def main() -> None:
    out = GeneratedOutputManager(__file__)
    data: DataModel = out.load_dataclass(DataModel)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.2))

    draw_panel(
        ax1, data.lam_cold, data.g_cold, data.cold_traj,
        data.cold_start, data.root,
        rf"Cold start ({data.cold_iters} iterations)",
    )
    draw_panel(
        ax2, data.lam_warm, data.g_warm, data.warm_traj,
        data.warm_start, data.root,
        rf"Warm start ({data.warm_iters} iterations)",
    )

    fig.tight_layout()
    out.savefig(fig, FIGURE_KEY)
    out.save_tex_figure(
        FIGURE_KEY,
        caption=get_caption(lambda_true=data.lambda_true, m=data.m, k=data.k,
                            b_bits=data.b_bits),
        label="newton-graphic-iteration",
    )


if __name__ == "__main__":
    main()

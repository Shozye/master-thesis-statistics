import numpy as np
import matplotlib.pyplot as plt

from generated_output_manager import GeneratedOutputManager
from data_for_figure_dataclass import DataModel

FIGURE_KEY = "kqsketch-shifted-parameters"


def get_caption(b: int, k_fixed: float, m_fixed: int, lam: float) -> str:
    return (
        rf"\textbf{{(a)}}~Register histograms of \kQSketchShifted{{}} for "
        rf"\(b={b}\), \(k={k_fixed}\), \(\Lambda={int(lam)}\), varying \(m\). "
        rf"\textbf{{(b)}}~Register histograms for \(b={b}\), \(m={m_fixed}\), "
        rf"\(\Lambda={int(lam)}\), varying \(k\)."
    )


def get_test_caption() -> str:
    return get_caption(b=5, k_fixed=2.0, m_fixed=100, lam=1000)


def _plot_hist(ax, regs_dict, labels, colors, normalize=False):
    """Plot register histograms as bars + step outline."""
    all_regs = [np.array(v) for v in regs_dict.values()]
    lo = min(int(r.min()) for r in all_regs)
    hi = max(int(r.max()) for r in all_regs)
    full_x = np.arange(lo, hi + 1)

    for regs, color, label in zip(all_regs, colors, labels):
        counts = np.zeros(len(full_x), dtype=float)
        for v in regs:
            counts[v - lo] += 1
        if normalize:
            counts /= len(regs)
        ax.bar(full_x, counts, color=color, alpha=0.25, width=1.0)
        ax.step(full_x, counts, where="mid", color=color, linewidth=1.8, label=label)

    ax.set_xlabel("Relative register value")
    ax.set_ylabel("Fraction" if normalize else "Number of registers")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3, linestyle="--", axis="y")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def main():
    out = GeneratedOutputManager(__file__)
    d = out.load_dataclass(DataModel)

    fig, (ax_l, ax_r) = plt.subplots(1, 2, figsize=(14, 5))

    # Left: varying m
    colors_m = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]
    labels_m = [rf"$m={m}$" for m in d.m_values]
    _plot_hist(ax_l, d.regs_by_m, labels_m, colors_m, normalize=True)
    ax_l.set_title(rf"(a) $b={d.b}$, $k={d.k_fixed}$, varying $m$")

    # Right: varying k
    colors_k = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]
    labels_k = [rf"$k={k}$" for k in d.k_values]
    _plot_hist(ax_r, d.regs_by_k, labels_k, colors_k)
    ax_r.set_title(rf"(b) $b={d.b}$, $m={d.m_fixed}$, varying $k$")

    fig.tight_layout()
    out.savefig(fig, FIGURE_KEY)
    out.save_tex_figure(
        FIGURE_KEY,
        caption=get_caption(d.b, d.k_fixed, d.m_fixed, d.lam),
        label="kqsketch-shifted-parameters",
        width=r"0.96\textwidth",
        placement="ht",
    )


if __name__ == "__main__":
    main()

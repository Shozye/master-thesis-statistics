import numpy as np
import matplotlib.pyplot as plt

from generated_output_manager import GeneratedOutputManager
from data_for_figure_dataclass import DataModel

FIGURE_KEY = "logexpsketch-shifted-bits"


def theoretical_rse(j: float, m: int) -> float:
    """Theoretical Jaccard RSE, same formula as ExpSketch: sqrt((1-J)/(m*J))."""
    return np.sqrt((1 - j) / (m * j))


def get_caption(m: int) -> str:
    return (
        rf"""Influence of the register width \(b\) on Shifted \LogExpSketch{{}}"""
        r"""Dashed lines on panel (b) mark the theoretical optimum \(\sqrt{(1-J)/(mJ)}\)"""
    )


def get_test_caption() -> str:
    return get_caption(m=400)


def main() -> None:
    out = GeneratedOutputManager(__file__)
    data = out.load_dataclass(DataModel)

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5), constrained_layout=True)
    ax_a, ax_b = axes

    # --- Panel (a): cardinality RSE vs log10(Lambda) ---
    cmap_a = plt.cm.viridis
    n_a = len(data.panel_a_labels)
    for idx, (label, rse) in enumerate(zip(data.panel_a_labels, data.panel_a_rse)):
        is_baseline = idx == 0
        ax_a.plot(
            data.log_lambdas,
            rse,
            color="black" if is_baseline else cmap_a((idx - 1) / max(1, n_a - 2)),
            linestyle="--" if is_baseline else "-",
            marker="" if is_baseline else "o",
            markersize=3,
            linewidth=1.8 if is_baseline else 1.5,
            label=label,
        )
    # ax_a.set_ylim(0.045, 0.1)
    ax_a.set_xlabel(r"$\log_{10} \Lambda$")
    ax_a.set_ylabel("RSE")
    ax_a.set_title("(a) Weighted cardinality")
    ax_a.grid(True, alpha=0.3, linestyle="--")
    ax_a.spines["top"].set_visible(False)
    ax_a.spines["right"].set_visible(False)
    ax_a.legend(loc="upper center", fontsize=8, ncol=2)

    # --- Panel (b): Jaccard RSE vs bits b ---
    cmap_b = plt.cm.viridis
    colors_b = [cmap_b(i / (len(data.j_values) - 1)) for i in range(len(data.j_values))]
    for j, color in zip(data.j_values, colors_b):
        ax_b.axhline(theoretical_rse(j, data.m), color=color, linestyle="--", alpha=0.5, linewidth=1)
    for j, color, rse in zip(data.j_values, colors_b, data.panel_b_rse):
        ax_b.plot(
            data.b_values,
            rse,
            color=color,
            marker="o",
            markersize=3,
            linewidth=1.5,
            label=f"$J = {j}$",
        )
    ax_b.set_xlabel("Bits per register $b$")
    ax_b.set_ylabel("RSE")
    ax_b.set_title("(b) Jaccard similarity")
    ax_b.set_xticks(data.b_values)
    ax_b.grid(True, alpha=0.3, linestyle="--")
    ax_b.spines["top"].set_visible(False)
    ax_b.spines["right"].set_visible(False)
    ax_b.legend(loc="upper right", fontsize=8)

    out.savefig(fig, FIGURE_KEY)
    out.save_tex_figure(
        FIGURE_KEY,
        caption=get_caption(m=data.m),
        label=FIGURE_KEY,
        width=r"\textwidth",
    )


if __name__ == "__main__":
    main()

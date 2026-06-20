import numpy as np
import matplotlib.pyplot as plt

from generated_output_manager import GeneratedOutputManager
from data_for_figure_dataclass import DataModel

FIGURE_KEY = "expsketch-jaccard-mantissa"


def theoretical_rse(j: float, m: int) -> float:
    return np.sqrt((1 - j) / (m * j))


def get_caption(m: int) -> str:
    return rf"""RSE of ExpSketch structural Jaccard estimator as a function of mantissa bits~\(p\) for \(m = {m}\) registers."""


def get_test_caption() -> str:
    return get_caption(m=100)


def main() -> None:
    out = GeneratedOutputManager(__file__)
    data = out.load_dataclass(DataModel)

    keep = [i for i, q in enumerate(data.q_values) if q != 7]
    q_values = [data.q_values[i] for i in keep]
    rse_data = [data.rse_data[i] for i in keep]

    fig, axes = plt.subplots(1, 2, figsize=(10, 4.5), constrained_layout=True)
    cmap = plt.cm.viridis
    colors = [cmap(i / (len(data.j_values) - 1)) for i in range(len(data.j_values))]

    for ax, q, rse_q in zip(axes, q_values, rse_data):
        for j, color in zip(data.j_values, colors):
            rse_theo = theoretical_rse(j, data.m)
            ax.axhline(rse_theo, color=color, linestyle="--", alpha=0.5, linewidth=1)

        for j, color, rse_values in zip(data.j_values, colors, rse_q):
            ax.plot(
                data.p_values,
                rse_values,
                color=color,
                marker="o",
                markersize=3,
                linewidth=1.5,
                label=f"$J = {j}$",
            )

        ax.set_xlabel("Mantissa bits $p$")
        ax.set_title(f"$q = {q}$")
        ax.set_xticks(data.p_values)
        ax.grid(True, alpha=0.3, linestyle="--")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    axes[0].set_ylabel("RSE")
    axes[-1].legend(loc="upper right", fontsize=8)

    out.savefig(fig, FIGURE_KEY)
    out.save_tex_figure(
        FIGURE_KEY,
        caption=get_caption(m=data.m),
        label="expsketch-jaccard-mantissa",
        width=r"\textwidth",
    )


if __name__ == "__main__":
    main()

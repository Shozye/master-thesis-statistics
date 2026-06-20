import matplotlib.pyplot as plt

from generated_output_manager import GeneratedOutputManager
from data_for_figure_dataclass import DataModel

FIGURE_KEY = "memory-vs-rse-comparison"

COLORS = ["#2ca02c", "#1f77b4", "#ff7f0e", "#d62728"]
LINESTYLES = ["-", "--", "-.", ":"]


def get_caption(n_reps: int, b: int) -> str:
    return (
        rf"Total memory vs.\ RSE for QSketchDyn, QSketch, and WeightedHyperLogLogFloat32"
        rf" with \(b={b}\). Seeds counted as 0 bytes. \(\Lambda = 10^4\), {n_reps} trials per point."
    )


def get_test_caption() -> str:
    return get_caption(n_reps=5000, b=8)


def main() -> None:
    out = GeneratedOutputManager(__file__)
    data = out.load_dataclass(DataModel)

    fig, ax = plt.subplots(figsize=(8, 5))
    for label, color, ls, xs, ys in zip(
        data.labels, COLORS, LINESTYLES, data.memory_values, data.rse_values
    ):
        ax.plot(
            xs, ys, color=color, linestyle=ls, linewidth=1.8,
            marker="o", markersize=3, label=label,
        )

    ax.set_xlabel("Total memory (bytes)", fontsize=10)
    ax.set_ylabel("RSE", fontsize=10)
    ax.legend(fontsize=9, loc="upper right")
    ax.grid(True, alpha=0.3, linestyle="--")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.tight_layout()
    out.savefig(fig, FIGURE_KEY)
    out.save_tex_figure(
        FIGURE_KEY,
        caption=get_caption(n_reps=data.n_reps, b=data.b),
        label="ch3-memory-vs-rse-comparison",
        placement="ht",
    )


if __name__ == "__main__":
    main()

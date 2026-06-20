import matplotlib.pyplot as plt
from matplotlib.ticker import LogLocator, FuncFormatter

from generated_output_manager import GeneratedOutputManager
from data_for_figure_dataclass import DataModel

FIGURE_KEY = "memory-to-accuracy-sweep"

COLORS = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b"]
LINESTYLES = ["-", "--", "-.", ":", "-", "--"]
MARKERS = ["o", "s", "^", "D", "v", "P"]


def get_caption(n_elements: int, n_reps: int, total_weight: float, dist_name: str) -> str:
    return (
        rf"Empirical \RSE{{}} versus total memory footprint for weighted"
        rf" cardinality sketches. For each byte budget the largest \(\SketchSize\)"
        rf" that fits is chosen. \(\Lambda = {total_weight:g}\),"
        rf" {n_reps} repetitions per point."
    )


def get_test_caption() -> str:
    return get_caption(n_elements=1000, n_reps=10000, total_weight=1000.0, dist_name="uniform")


def main() -> None:
    out = GeneratedOutputManager(__file__)
    data = out.load_dataclass(DataModel)

    def fmt_label(label: str) -> str:
        if "kQSketch" in label:
            return label + rf", $k={data.k_base:g}$"
        return label

    fig, ax = plt.subplots(figsize=(8, 5))
    for label, color, ls, marker, xs, ys in zip(
        data.labels, COLORS, LINESTYLES, MARKERS, data.memory_values, data.rse_values
    ):
        ax.plot(
            xs, ys, color=color, linestyle=ls, linewidth=1.6,
            marker=marker, markersize=3, label=fmt_label(label),
        )

    ax.set_yscale("log")
    ax.set_ylim(None, 0.1)

    ax.yaxis.set_major_locator(LogLocator(base=10, numticks=10))
    ax.yaxis.set_minor_locator(LogLocator(base=10, subs=[2, 3, 4, 5, 6, 7, 8, 9], numticks=50))

    def pct_fmt(x, _):
        pct = x * 100
        return f"{pct:.0f}%" if pct >= 1 else f"{pct:.1f}%"

    ax.yaxis.set_major_formatter(FuncFormatter(pct_fmt))

    ax.set_xlabel("Total memory (bytes)", fontsize=10)
    ax.set_ylabel("RSE", fontsize=10)
    ax.legend(fontsize=9, loc="upper right")
    ax.grid(True, which="major", alpha=0.3, linestyle="--")
    ax.grid(True, which="minor", alpha=0.12, linestyle=":")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.tight_layout()
    out.savefig(fig, FIGURE_KEY)
    out.save_tex_figure(
        FIGURE_KEY,
        caption=get_caption(
            n_elements=data.n_elements,
            n_reps=data.n_reps,
            total_weight=data.total_weight,
            dist_name=data.dist_name,
        ),
        label="ch5-memory-to-accuracy-sweep",
        placement="ht",
    )


if __name__ == "__main__":
    main()

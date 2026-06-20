import matplotlib.pyplot as plt

from generated_output_manager import GeneratedOutputManager
from data_for_figure_dataclass import DataModel

FIGURE_KEY = "wce-update-time-vs-m-pareto"

COLORS = ["#1f77b4", "#aec7e8", "#2ca02c", "#d62728", "#ff7f0e", "#e377c2", "#9467bd"]
LINESTYLES = ["-", "--", "-", "-.", "-", "--", ":"]


def get_caption(n_elements: int, n_reps: int) -> str:
    return (
        rf"Update time for {n_elements} weighted elements vs.\ number of registers \(\SketchSize\)."
        rf" Median over {n_reps} repetitions. Log-log scale."
    )


def get_test_caption() -> str:
    return get_caption(n_elements=100000, n_reps=10)


def main() -> None:
    out = GeneratedOutputManager(__file__)
    data = out.load_dataclass(DataModel)

    fig, ax = plt.subplots(figsize=(8, 5))
    for i, (label, times) in enumerate(zip(data.labels, data.update_times_us)):
        ax.plot(
            data.m_values, times,
            color=COLORS[i], linestyle=LINESTYLES[i], linewidth=1.8,
            marker="o", markersize=4, label=label,
        )

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel(r"Number of registers $m$", fontsize=10)
    ax.set_ylabel(rf"Update time for $n={data.n_elements}$ elements ($\mu$s)", fontsize=10)
    ax.legend(fontsize=9, loc="upper left")
    ax.grid(True, alpha=0.3, linestyle="--", which="both")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.tight_layout()
    out.savefig(fig, FIGURE_KEY)
    out.save_tex_figure(
        FIGURE_KEY,
        caption=get_caption(n_elements=data.n_elements, n_reps=data.n_reps),
        label="ch5-wce-update-time-pareto",
        placement="ht",
    )


if __name__ == "__main__":
    main()

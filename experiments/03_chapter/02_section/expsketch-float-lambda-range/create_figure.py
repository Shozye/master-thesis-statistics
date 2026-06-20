import numpy as np
import matplotlib.pyplot as plt

from weighted_cardinality_estimation import stat
from generated_output_manager import GeneratedOutputManager
from data_for_figure_dataclass import DataModel

FIGURE_KEY = "expsketch-float-lambda-range"

FLOAT_CONFIGS = [
    {"name": "float16", "color": "#d62728", "dtype": np.float16},
    {"name": "float32", "color": "#1f77b4", "dtype": np.float32},
    {"name": "float64", "color": "#2ca02c", "dtype": np.float64},
]


def lam_range_for_dtype(dtype) -> tuple[float, float]:
    fi = np.finfo(dtype)
    return 1.0 / float(fi.max), 1.0 / float(fi.tiny)


def plot_range_bars(ax: plt.Axes) -> None:
    for i, cfg in enumerate(FLOAT_CONFIGS):
        lam_min, lam_max = lam_range_for_dtype(cfg["dtype"])
        lo, hi = np.log10(lam_min), np.log10(lam_max)
        ax.barh(
            i,
            hi - lo,
            left=lo,
            height=0.5,
            color=cfg["color"],
            alpha=0.85,
            edgecolor="black",
            linewidth=0.8,
        )
        ax.text(
            (lo + hi) / 2,
            i,
            cfg["name"],
            ha="center",
            va="center",
            fontsize=9,
            fontweight="bold",
            color="white",
        )

    ax.set_yticks(range(len(FLOAT_CONFIGS)))
    ax.set_yticklabels([c["name"] for c in FLOAT_CONFIGS], fontsize=9)
    ax.set_xlabel(r"$\log_{10}(\Lambda)$", fontsize=10)
    ax.set_title(r"(a) Representable $\Lambda$ range per register type", fontsize=10)
    ax.set_xlim(-300, 300)
    ax.xaxis.grid(True, linestyle="--", alpha=0.4, linewidth=0.7)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def plot_relative_error(ax: plt.Axes, data: DataModel) -> None:
    configs = [
        ("#d62728", "-.", r"ExpSketch(float16), $q=5$", data.errors_float16),
        ("#1f77b4", "--", r"ExpSketch(float32), $q=8$", data.errors_float32),
        ("#2ca02c", "-", r"ExpSketch(float64), $q=11$", data.errors_float64),
    ]

    for color, ls, label, errors in configs:
        ax.plot(data.exponents, errors, color=color, linestyle=ls, linewidth=1.8, label=label)

    ax.set_xlim(-300, 300)
    ax.set_ylim(0, 1)
    ax.set_xlabel(r"$\log_{10}(\Lambda)$", fontsize=10)
    ax.set_ylabel(r"Mean relative error", fontsize=10)
    ax.set_title(rf"(b) Relative error vs.\ $\Lambda$ ($m={data.m}$, {data.n_reps} trials)", fontsize=10)
    ax.legend(fontsize=8, loc="upper right")
    ax.grid(True, alpha=0.3, linestyle="--")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def get_caption(m: int, n_reps: int) -> str:
    return rf"""\textbf{{(a)}} Representable \(\Lambda\) range for \texttt{{float16}}, \texttt{{float32}}, and \texttt{{float64}} registers. \textbf{{(b)}} Mean relative error vs.\ \(\Lambda\) (\(m = {m}\), {n_reps} trials). Error is near-constant within the valid range and spikes at the float type's boundaries."""


def get_test_caption() -> str:
    return get_caption(m=100, n_reps=50)


def main() -> None:
    out = GeneratedOutputManager(__file__)
    data = out.load_dataclass(DataModel)

    fig, (ax_a, ax_b) = plt.subplots(1, 2, figsize=(12, 4))
    plot_range_bars(ax_a)
    plot_relative_error(ax_b, data)
    fig.tight_layout(pad=2.0)
    out.savefig(fig, FIGURE_KEY)
    out.save_tex_figure(
        FIGURE_KEY,
        caption=get_caption(m=data.m, n_reps=data.n_reps),
        label="expsketch-float-range",
        placement="ht",
    )


if __name__ == "__main__":
    main()

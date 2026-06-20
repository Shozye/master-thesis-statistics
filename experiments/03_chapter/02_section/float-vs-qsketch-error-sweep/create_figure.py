import numpy as np
import matplotlib.pyplot as plt

from generated_output_manager import GeneratedOutputManager
from data_for_figure_dataclass import DataModel

FIGURE_KEY = "float-vs-qsketch-error-sweep"


def get_caption(m: int, n_reps: int) -> str:
    return rf"""Valid working ranges for ExpSketch and QSketch, \(m = {m}\), {n_reps} trials."""


def get_test_caption() -> str:
    return get_caption(m=50, n_reps=30)


def main() -> None:
    out = GeneratedOutputManager(__file__)
    data = out.load_dataclass(DataModel)

    fig, ax = plt.subplots(figsize=(9, 5))
    for label, color, ls, errors in zip(data.labels, data.colors, data.linestyles, data.errors):
        ax.plot(data.exponents, errors, color=color, linestyle=ls, linewidth=1.8, label=label)

    ax.set_xlim(data.exp_min - 15, data.exp_max + 15)
    ax.set_ylim(0, 1)
    tiny_exp = np.log10(np.nextafter(0.0, 1.0))
    max_exp = np.log10(np.finfo(np.float64).max)
    ax.axvline(
        tiny_exp, color="black", linewidth=1.2, linestyle="-",
        label=f"float64_tiny=$10^{{{tiny_exp:.0f}}}$",
    )
    ax.axvline(
        max_exp, color="black", linewidth=1.2, linestyle="-",
        label=f"float64_max=$10^{{{max_exp:.0f}}}$",
    )
    ax.set_xlabel(r"$\log_{10}(\Lambda)$", fontsize=11)
    ax.set_ylabel(r"Mean relative error", fontsize=11)
    ax.set_title(rf"Relative error vs.\ $\Lambda$ ($m={data.m}$, {data.n_reps} trials)", fontsize=10)
    ax.legend(fontsize=9, loc="upper right")
    ax.grid(True, alpha=0.3, linestyle="--")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()

    out.savefig(fig, FIGURE_KEY)
    out.save_tex_figure(
        FIGURE_KEY,
        caption=get_caption(m=data.m, n_reps=data.n_reps),
        label="float-bits-error-comparison",
        width=r"0.9\textwidth",
        placement="ht",
    )


if __name__ == "__main__":
    main()

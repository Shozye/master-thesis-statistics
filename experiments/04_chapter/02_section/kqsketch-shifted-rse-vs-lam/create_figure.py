import numpy as np
import matplotlib.pyplot as plt

from generated_output_manager import GeneratedOutputManager
from data_for_figure_dataclass import DataModel

FIGURE_KEY = "kqsketch-shifted-rse-vs-lam"

COLORS = {4: "#ff7f0e", 5: "#2ca02c", 6: "#9467bd", 7: "#8c564b"}


def get_caption(m: int, n_reps: int) -> str:
    return (
        rf"RSE vs \(\Lambda\) for \kQSketchShifted{{}} (\(b=4,5\)) "
        rf"and \kQSketch{{}} (\(b=4,5,6,7\)), \(m={m}\), {n_reps} trials."
    )


def get_test_caption() -> str:
    return get_caption(m=64, n_reps=300)


def main():
    out = GeneratedOutputManager(__file__)
    d = out.load_dataclass(DataModel)

    log_lam = np.log10(d.lambda_range)

    fig, ax = plt.subplots(figsize=(7, 4.5))

    for b in d.b_sweep_shifted:
        ax.plot(log_lam, d.rse_shifted[str(b)], "s-", color=COLORS[b], linewidth=1.5,
                label=rf"$k$-QSketch-Shifted $b={b}$", markersize=4)
    for b in d.b_sweep:
        ax.plot(log_lam, d.rse_kq[str(b)], "o--", color=COLORS[b], linewidth=1.0,
                label=rf"$k$-QSketch $b={b}$", markersize=3, alpha=0.7)

    ax.set_xlabel(r"$\log_{10}\Lambda$")
    ax.set_ylabel("RSE")
    ax.set_ylim(0, 1)
    ax.legend(fontsize=7, ncol=2)
    ax.grid(alpha=0.3, linestyle="--")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    out.savefig(fig, FIGURE_KEY)
    out.save_tex_figure(
        FIGURE_KEY,
        caption=get_caption(d.m, d.n_reps),
        label="kqsketch-shifted-rse-vs-lam",
        width=r"0.7\textwidth",
        placement="ht",
    )


if __name__ == "__main__":
    main()

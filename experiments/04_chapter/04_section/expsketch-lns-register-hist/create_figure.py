import numpy as np
import matplotlib.pyplot as plt

from data_for_figure_dataclass import DataModel
from generated_output_manager import GeneratedOutputManager

FIGURE_KEY = "expsketch-lns-register-hist"

COLORS = ["#1f77b4", "magenta", "#2ca02c"]


def get_caption(m: int) -> str:
    return (
        r"LogExpSketch-Slow-NoShifted (\(b=8\), \(v_{\max}=128\)) register index distribution"
        rf" after inserting a single element, \(m={m}\)."
    )


def get_test_caption() -> str:
    return get_caption(m=100)


def main() -> None:
    out = GeneratedOutputManager(__file__)
    d = out.load_dataclass(DataModel)

    n_buckets = 2**d.amount_bits
    xs = np.arange(n_buckets)

    fig, ax = plt.subplots(figsize=(9, 4))

    for i, (counts, label, color) in enumerate(zip(d.counts, d.labels, COLORS)):
        ys = np.array(counts, dtype=float)
        ax.bar(xs, ys, color=color, alpha=0.45, width=1.0, label=label)
        ax.step(xs, ys, color=color, linewidth=1.4, where="mid")

    ax.set_xlabel("Register index", fontsize=11)
    ax.set_ylabel("Number of registers", fontsize=11)
    ax.set_xlim(-0.5, n_buckets - 0.5)
    ax.legend(fontsize=9)
    ax.grid(True, axis="y", alpha=0.3, linestyle="--")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()

    out.savefig(fig, FIGURE_KEY)
    out.save_tex_figure(
        FIGURE_KEY,
        caption=get_caption(m=d.m),
        label="expsketch-lns-register-histogram",
        width=r"0.75\textwidth",
    )


if __name__ == "__main__":
    main()

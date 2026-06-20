import numpy as np
import matplotlib.pyplot as plt

from generated_output_manager import GeneratedOutputManager
from data_for_figure_dataclass import DataModel

FIGURE_KEY = "expsketch-register-histogram"

S_BITS = 0
M_COLORS = ["#1f77b4", "magenta", "#2ca02c"]
WEIGHTS_COLORS = ["#1f77b4", "magenta", "#2ca02c"]


def all_positive_custom_float_values(q: int, p: int) -> np.ndarray:
    bias = 2 ** (q - 1) - 1
    n_mant = 2**p
    values = []
    for m in range(1, n_mant):
        values.append(2.0 ** (1 - bias) * (m / n_mant))
    for e in range(1, 2**q - 1):
        for m in range(n_mant):
            values.append(2.0 ** (e - bias) * (1 + m / n_mant))
    return np.array(sorted(values))


def _plot_from_counts(ax, q_bits, p_bits, counts_list, colors, labels):
    possible_values = all_positive_custom_float_values(q_bits, p_bits)
    float_min = possible_values[0]
    float_max = possible_values[-1]

    for counts, color, label in zip(counts_list, colors, labels):
        counts = np.array(counts)
        mask = counts > 0
        ax.bar(np.where(mask)[0], counts[mask], color=color, alpha=0.25, width=1.0)
        xs = np.arange(len(possible_values))
        ax.step(xs, counts, where="mid", color=color, linewidth=1.8, label=label)

    ax.axvline(0, color="black", linestyle="-", linewidth=1.5, label=f"MIN = {float_min:.3g}")
    ax.axvline(
        len(possible_values) - 1,
        color="black",
        linestyle="--",
        linewidth=1.5,
        label=f"MAX = {float_max:.3g}",
    )

    n_ticks = 10
    tick_indices = np.linspace(0, len(possible_values) - 1, n_ticks, dtype=int)
    ax.set_xticks(tick_indices)
    ax.set_xticklabels(
        [f"{possible_values[i]:.3g}" for i in tick_indices], rotation=45, fontsize=7
    )
    ax.set_xlabel("Register value (custom float representable values)")
    ax.set_ylabel("Number of registers")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3, linestyle="--", axis="y")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def get_caption() -> str:
    return (
        rf"Register value distribution in ExpSketchCustomFloat after inserting a single element. "
        rf"Left: \(s={S_BITS}\), \(q=5\), \(p=5\) with varying \(\Lambda\). "
        rf"Right: \(s={S_BITS}\), \(q=4\), \(p=5\), \(\Lambda=2^0\) with varying \(m\). "
        rf"Each representable value occupies equal width on the \(x\)-axis."
    )


def get_test_caption() -> str:
    return get_caption()


def main() -> None:
    out = GeneratedOutputManager(__file__)
    data = out.load_dataclass(DataModel)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    ax1.set_title(rf"(a) $q={data.q_bits}$, $p={data.p_bits}$, $m={data.m}$, varying $\Lambda$", fontsize=10)
    _plot_from_counts(ax1, data.q_bits, data.p_bits, data.counts_left, WEIGHTS_COLORS, data.labels_left)

    m_labels = [rf"$m={m}$" for m in data.m_values]
    ax2.set_title(rf"(b) $q={data.q_bits_2}$, $p={data.p_bits_2}$, $\Lambda=2^0$, varying $m$", fontsize=10)
    _plot_from_counts(ax2, data.q_bits_2, data.p_bits_2, data.counts_right, M_COLORS, m_labels)

    fig.tight_layout()
    out.savefig(fig, FIGURE_KEY)
    out.save_tex_figure(
        FIGURE_KEY,
        caption=get_caption(),
        label="expsketch-register-histogram",
        width=r"0.92\textwidth",
    )


if __name__ == "__main__":
    main()

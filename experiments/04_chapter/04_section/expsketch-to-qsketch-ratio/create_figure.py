import math

import numpy as np
import matplotlib.pyplot as plt

from generated_output_manager import GeneratedOutputManager
from data_for_figure_dataclass import DataModel

FIGURE_KEY = "expsketch-to-qsketch-ratio"


def _sci(m: int) -> str:
    """m in scientific notation, e.g. 2.68\\times10^{8}. A unit mantissa is
    dropped so a clean power of ten renders as just 10^{6}."""
    e = int(math.floor(math.log10(m)))
    mant = m / 10 ** e
    if abs(mant - 1.0) < 5e-3:
        return rf"10^{{{e}}}"
    return rf"{mant:.2f}\times10^{{{e}}}"


def _fmt_m(m: int) -> str:
    """Bottom-axis label for a guide point. Below 10^4 the integer is written in
    full; otherwise scientific notation is used, with exact powers of two
    rendered as 2^{k}\\approx a\\times10^{b}."""
    if m < 10_000:
        return rf"${m}$"
    exp = int(round(math.log2(m)))
    if 2 ** exp == m:
        return rf"$2^{{{exp}}}\approx {_sci(m)}$"
    return rf"${_sci(m)}$"


def get_caption() -> str:
    return (
        r"""Total memory ratio \(T_{E(7,8)}/T_{Q8}\) of FastExpSketchCustomFloat\((p{=}7,\,q{=}8)\) """
        r"""to QSketch\((b{=}8)\) at equal \(\RSE\)"""
    )


def get_test_caption() -> str:
    return get_caption()


def main() -> None:
    out = GeneratedOutputManager(__file__)
    data = out.load_dataclass(DataModel)

    ms = np.array(data.ms)
    ratio = np.array(data.t_e) / np.array(data.t_q)

    guide_left = list(
        zip(
            data.guide_ms_left,
            (np.array(data.guide_t_e_left) / np.array(data.guide_t_q_left)).tolist(),
        )
    )
    guide_right = list(
        zip(
            data.guide_ms_right,
            (np.array(data.guide_t_e_right) / np.array(data.guide_t_q_right)).tolist(),
        )
    )

    # Smooth analytic envelopes of the sawtooth. With k = log2(m) and the
    # additive byte constants dropped, the ratio of the two bit totals reduces
    # to (1/rho) * (2k + 15) / (2k + c): c = 8 on the plateaus (both index
    # widths equal) and c = 10 in the dips (QSketch's index width has already
    # ticked up by one bit while ExpSketch's has not).
    rho = data.rho
    k = np.log2(ms)
    env_top = (2 * k + 15) / (rho * (2 * k + 8))
    env_bottom = (2 * k + 15) / (rho * (2 * k + 10))

    fig, ax = plt.subplots(figsize=(8, 4.5), constrained_layout=True)

    ax.plot(ms, ratio, color="#1f77b4", linewidth=1.8, label=r"$T_{E(7,8)}/T_{Q8}$")
    ax.plot(
        ms, env_top, color="#2ca02c", linestyle="--", linewidth=1.3,
        label=r"top env. $\frac{1}{\rho}\cdot\frac{2\log_2 m + 15}{2\log_2 m + 8}$",
    )
    ax.plot(
        ms, env_bottom, color="#9467bd", linestyle="--", linewidth=1.3,
        label=r"bottom env. $\frac{1}{\rho}\cdot\frac{2\log_2 m + 15}{2\log_2 m + 10}$",
    )

    ax.set_xscale("log")
    x_left = float(ms.min()) * 0.8
    x_right = float(ms.max())
    ax.set_xlim(left=x_left, right=x_right)
    y_bottom = 0.98
    ax.set_ylim(y_bottom, 1.2)

    # Dashed guide lines: from each highlighted m down to the OX axis (with the
    # m value labelled at the bottom) and horizontally left to the OY axis, so
    # the ratio value can be read off directly. The value label is placed on the
    # left of OY ("left") or just to the right of it, inside the plot ("right").
    def draw_guide(m: int, r: float, side: str) -> None:
        ax.plot([m, m], [y_bottom, r], color="gray", linestyle="--", linewidth=1.0)
        ax.plot([x_left, m], [r, r], color="gray", linestyle="--", linewidth=1.0)
        ax.plot([m], [r], marker="o", color="#d62728", markersize=5, zorder=5)
        ax.annotate(
            _fmt_m(m),
            xy=(m, y_bottom),
            xytext=(0, 3),
            textcoords="offset points",
            fontsize=8,
            color="#222222",
            ha="center",
        )
        if side == "left":
            ha, dx = "right", -4
        else:
            ha, dx = "left", 4
        ax.annotate(
            f"{r:.3f}",
            xy=(x_left, r+0.002),
            xytext=(dx, 0),
            textcoords="offset points",
            fontsize=8,
            color="#222222",
            ha=ha,
            va="center",
            annotation_clip=False,
        )

    for m, r in guide_left:
        draw_guide(m, r, "left")
    for m, r in guide_right:
        draw_guide(m, r, "right")

    ax.set_xlabel(r"Sketch size $m$")
    ax.set_ylabel(r"$T_{E(7,8)}/T_{Q8}$")
    ax.grid(True, alpha=0.3, linestyle="--")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(loc="upper right", fontsize=9)

    out.savefig(fig, FIGURE_KEY)
    out.save_tex_figure(
        FIGURE_KEY,
        caption=get_caption(),
        label=FIGURE_KEY,
        width=r"\textwidth",
    )


if __name__ == "__main__":
    main()

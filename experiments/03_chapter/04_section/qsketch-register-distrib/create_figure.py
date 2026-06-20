import numpy as np
import matplotlib.pyplot as plt

from data_for_figure_dataclass import DataModel
from generated_output_manager import GeneratedOutputManager

FIGURE_KEY = "qsketch-register-distrib"


def trimmed_pmf(b: int, lam: float) -> tuple[np.ndarray, np.ndarray]:
    r_min = -(2 ** (b - 1) - 1)
    r_max = 2 ** (b - 1) - 1
    values = np.arange(r_min, r_max + 1)
    probs = np.zeros(len(values))
    for i, v in enumerate(values):
        if v == r_min:
            probs[i] = np.exp(-lam * 2.0 ** (-r_min))
        elif v == r_max:
            probs[i] = 1.0 - np.exp(-lam * 2.0 ** (-r_max))
        else:
            probs[i] = np.exp(-lam * 2.0 ** (-(v + 1))) - np.exp(-lam * 2.0 ** (-v))
    return values, probs


def plot_subplot(ax: plt.Axes, b: int, all_regs: np.ndarray, m: int, n_reps: int, lam: float, title: str) -> None:
    r_min = -(2 ** (b - 1) - 1)
    r_max = 2 ** (b - 1) - 1

    theo_values, theo_probs = trimmed_pmf(b, lam)
    theo_counts = theo_probs * m * n_reps

    mask = theo_probs > 1e-6
    if mask.any():
        plot_min = max(r_min, theo_values[mask].min() - 2)
        plot_max = min(r_max, theo_values[mask].max() + 2)
    else:
        plot_min, plot_max = r_min, r_max

    bins = np.arange(plot_min - 0.5, plot_max + 1.5, 1)
    ax.hist(
        all_regs,
        bins=bins,
        color="#1f77b4",
        alpha=0.75,
        edgecolor="white",
        linewidth=0.4,
        label=f"Empirical ({n_reps} sketches)",
    )

    pmf_mask = (theo_values >= plot_min) & (theo_values <= plot_max)
    ax.plot(
        theo_values[pmf_mask],
        theo_counts[pmf_mask],
        color="#d62728",
        linewidth=1.8,
        marker="o",
        markersize=3,
        label="Trimmed PMF (scaled)",
    )

    ax.axvline(r_min, color="gray", linestyle=":", linewidth=1, alpha=0.7)
    ax.axvline(r_max, color="gray", linestyle=":", linewidth=1, alpha=0.7)
    ax.text(
        r_min,
        ax.get_ylim()[1] * 0.9 if ax.get_ylim()[1] > 0 else 1,
        f"r_min={r_min}",
        fontsize=7,
        ha="left",
        color="gray",
    )
    ax.text(
        r_max,
        ax.get_ylim()[1] * 0.9 if ax.get_ylim()[1] > 0 else 1,
        f"r_max={r_max}",
        fontsize=7,
        ha="right",
        color="gray",
    )

    ax.set_xlabel(r"Register value $v$", fontsize=10)
    ax.set_ylabel("Count", fontsize=10)
    ax.set_title(title, fontsize=10)
    ax.set_xlim(r_min - 1, r_max + 1)
    ax.legend(fontsize=8, loc="upper right")
    ax.grid(True, alpha=0.3, linestyle="--")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def _latex_lambda(lam: float) -> str:
    import math
    exp = math.log10(lam)
    return rf"10^{{{int(exp)}}}" if exp == int(exp) else str(lam)


def get_caption(m: int, n_reps: int, b_a: int, b_b: int, lambda_val: float) -> str:
    r_min_a, r_max_a = -(2 ** (b_a - 1) - 1), 2 ** (b_a - 1) - 1
    r_min_b, r_max_b = -(2 ** (b_b - 1) - 1), 2 ** (b_b - 1) - 1
    lam = _latex_lambda(lambda_val)
    return (
        rf"\protect\Agreed{{Histogram of QSketch register values overlaid with the theoretical PMF:}}"
        rf" \textbf{{(a)}}~\(b={b_a}\) (\(r \in [{r_min_a}, {r_max_a}]\)),"
        rf" \textbf{{(b)}}~\(b={b_b}\) (\(r \in [{r_min_b}, {r_max_b}]\))."
        rf" \protect\Agreed{{Both plots use \(\Lambda = {lam}\), \(\SketchSize = {m}\), and {n_reps:,} trials."
        rf" A substantial portion of the register range remains unused.}}"
    )


def get_test_caption() -> str:
    return get_caption(m=100, n_reps=50, b_a=7, b_b=5, lambda_val=1e6)


def main() -> None:
    out = GeneratedOutputManager(__file__)
    d = out.load_dataclass(DataModel)

    regs_7 = np.array(d.regs_7)
    regs_5 = np.array(d.regs_5)

    fig, (ax_a, ax_b) = plt.subplots(1, 2, figsize=(13, 4.5))
    plot_subplot(ax_a, 7, regs_7, d.m, d.n_reps, d.lambda_val, rf"(a) QSketch $b=7$, $\Lambda=10^6$, $m={d.m}$")
    plot_subplot(ax_b, 5, regs_5, d.m, d.n_reps, d.lambda_val, rf"(b) QSketch $b=5$, $\Lambda=10^6$, $m={d.m}$")

    fig.tight_layout()
    out.savefig(fig, FIGURE_KEY)
    out.save_tex_figure(
        FIGURE_KEY,
        caption=get_caption(m=d.m, n_reps=d.n_reps, b_a=7, b_b=5, lambda_val=d.lambda_val),
        label="qsketch-register-histogram",
        width=r"0.96\textwidth",
        placement="ht",
    )


if __name__ == "__main__":
    main()

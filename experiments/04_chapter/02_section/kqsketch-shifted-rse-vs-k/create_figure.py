import matplotlib.pyplot as plt

from generated_output_manager import GeneratedOutputManager
from data_for_figure_dataclass import BResult, DataModel

FIGURE_KEY = "kqsketch-shifted-rse-vs-k"

COLORS = {4: "#e377c2", 5: "#1f77b4", 6: "#2ca02c", 7: "#ff7f0e"}


def get_caption(m: int, lam: float, n_elems: int, n_reps: int) -> str:
    return (
        rf"RSE of \kQSketchShifted{{}} as a function of \(k\) "
        rf"for \(b \in \{{5,6,7\}}\) "
        rf"(\(m={m}\), \(\Lambda={int(lam)}\), \(n={n_elems}\), "
        rf"{n_reps} trials). "
        rf"Dashed line shows QSketch \(b=8\) baseline."
    )


def get_test_caption() -> str:
    return get_caption(m=400, lam=1, n_elems=10, n_reps=1000)


def main() -> None:
    out = GeneratedOutputManager(__file__)
    d = out.load_dataclass(DataModel)
    d.b_results = [BResult(**br) if isinstance(br, dict) else br for br in d.b_results]

    fig, ax = plt.subplots(figsize=(7, 4.5))

    for br in d.b_results:
        c = COLORS[br.b]
        ax.plot(d.k_values, br.rse_newton, "o-", color=c, linewidth=2, markersize=4,
                label=rf"$k$-QSketch-Shifted $b={br.b}$")

    # Single QSketch b=8 baseline (same value in all BResults)
    ax.axhline(d.b_results[0].rse_qsketch, color="#d62728", linestyle="--", linewidth=2,
               label=r"QSketch $b=8$")

    # Clip y-axis: from 5% below the global min to 20% above the max QSketch baseline
    y_top = d.b_results[0].rse_qsketch * 1.1
    y_bot = min(min(br.rse_newton) for br in d.b_results)
    y_bot = max(0, y_bot - 0.05 * (y_top - y_bot))
    ax.set_ylim(y_bot, y_top)

    ax.set_xlabel(r"Logarithm base $k$")
    ax.set_ylabel("RSE")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3, linestyle="--")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    out.savefig(fig, FIGURE_KEY)
    out.save_tex_figure(
        FIGURE_KEY,
        caption=get_caption(d.m, d.lam, d.n_elems, d.n_reps),
        label="kqsketch-shifted-rse-vs-k",
        width=r"0.7\textwidth",
        placement="ht",
    )


if __name__ == "__main__":
    main()

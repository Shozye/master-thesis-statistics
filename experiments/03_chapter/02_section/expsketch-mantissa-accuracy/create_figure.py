import numpy as np
import matplotlib.pyplot as plt

from generated_output_manager import GeneratedOutputManager
from data_for_figure_dataclass import DataModel

FIGURE_KEY = "expsketch-mantissa-accuracy"


def get_caption(q_bits: int, m: int) -> str:
    return rf"""Mean relative error of ExpSketchCustomFloat (\(q={q_bits}\), \(m={m}\)) as a function of \(\log_{{10}}(\Lambda)\) for different mantissa bit counts \(p\). Dashed line shows the theoretical RSE \(= 1/\sqrt{{m-2}}\)."""


def get_test_caption() -> str:
    return get_caption(q_bits=6, m=100)


def main() -> None:
    out = GeneratedOutputManager(__file__)
    data = out.load_dataclass(DataModel)

    fig, ax = plt.subplots(figsize=(9, 5))
    cmap = plt.cm.viridis
    colors = [cmap(i / (len(data.p_values) - 1)) for i in range(len(data.p_values))]

    for p, color, errors in zip(data.p_values, colors, data.errors_by_p):
        ax.plot(data.log_lambdas, errors, color=color, linewidth=1.5, label=f"$p = {p}$")

    ax.plot(
        data.log_lambdas, data.errors_float64, color="red", linewidth=2, linestyle="-.",
        label="ExpSketch float64"
    )

    rse = 1.0 / np.sqrt(data.m - 2)
    ax.axhline(rse, color="black", linestyle="--", linewidth=1.2, label=r"RSE $= 1/\sqrt{m-2}$")

    ax.set_xlabel(r"$\log_{10}(\Lambda)$", fontsize=11)
    ax.set_ylabel("Root mean squared relative error", fontsize=11)
    ax.legend(fontsize=8, loc="upper left")
    ax.set_ylim(0.05, 0.30)
    ax.grid(True, alpha=0.3, linestyle="--")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()

    out.savefig(fig, FIGURE_KEY)
    out.save_tex_figure(
        FIGURE_KEY,
        caption=get_caption(q_bits=data.q_bits, m=data.m),
        label="expsketch-mantissa-accuracy",
        width=r"0.92\textwidth",
    )


if __name__ == "__main__":
    main()

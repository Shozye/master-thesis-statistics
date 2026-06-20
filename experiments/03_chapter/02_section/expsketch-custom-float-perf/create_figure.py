# ---
# description: RSE comparison of FastExpSketchCustomFloat(p=7,q=8) vs ExpSketchFloat32 across Lambda range
# ---
import numpy as np
import matplotlib.pyplot as plt

from generated_output_manager import GeneratedOutputManager
from data_for_figure_dataclass import DataModel

FIGURE_KEY = "expsketch-custom-float-perf"


def get_caption(p: int, q: int, m: int) -> str:
    return rf"""RSE of FastExpSketchCustomFloat(\(p={p}\), \(q={q}\)) vs FastExpSketchFloat32 across \(\log_{{10}}(\Lambda)\) at \(m={m}\)."""


def get_test_caption() -> str:
    return get_caption(p=7, q=8, m=400)


def main() -> None:
    out = GeneratedOutputManager(__file__)
    data = out.load_dataclass(DataModel)

    fig, ax = plt.subplots(figsize=(9, 4.5))

    ax.plot(
        data.log_lambdas, data.rse_custom_float,
        color="#1f77b4", linewidth=2.0, label=f"CustomFloat($p={data.p}$, $q={data.q}$)"
    )
    ax.plot(
        data.log_lambdas, data.rse_float32,
        color="#d62728", linewidth=2.0, linestyle="--", label="FastExpSketchFloat32"
    )

    rse_theory = 1.0 / np.sqrt(data.m - 2)
    ax.axhline(rse_theory, color="black", linestyle=":", linewidth=1.2, label=r"RSE $= 1/\sqrt{m-2}$")

    ax.set_xlabel(r"$\log_{10}(\Lambda)$", fontsize=11)
    ax.set_ylabel("RSE", fontsize=11)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3, linestyle="--")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()

    out.savefig(fig, FIGURE_KEY)
    out.save_tex_figure(
        FIGURE_KEY,
        caption=get_caption(p=data.p, q=data.q, m=data.m),
        label="expsketch-custom-float-perf",
        width=r"0.92\textwidth",
    )


if __name__ == "__main__":
    main()

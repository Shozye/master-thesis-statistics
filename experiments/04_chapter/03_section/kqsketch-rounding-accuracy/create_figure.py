import numpy as np
import matplotlib.pyplot as plt

from generated_output_manager import GeneratedOutputManager
from data_for_figure_dataclass import DataModel

FIGURE_KEY = "kqsketch-rounding-accuracy"


def get_caption(m: int, n_reps: int, k: float, b_bits: int) -> str:
    return (
        rf"RSE vs \(\log_{{10}}(\Lambda)\) for ExpSketch, "
        rf"\(k\)-QSketch (\(k={k:.0f}\), \(b={b_bits}\), Newton-Warm), "
        rf"\kQSketchRounded{{}} (\(k={k:.0f}\), \(b={b_bits}\)), and "
        rf"\kQSketchRounded{{}} (\(k={k:.0f}\), \(b={b_bits}\), asymptotic correction), "
        rf"each with \(m={m}\) registers and {n_reps} repetitions per point."
    )


def get_test_caption() -> str:
    return get_caption(m=100, n_reps=50, k=2.0, b_bits=8)


def main() -> None:
    out = GeneratedOutputManager(__file__)
    data = out.load_dataclass(DataModel)

    exponents = np.array(data.exponents)

    fig, ax = plt.subplots(1, 1, figsize=(8, 5))
    ax.plot(exponents, data.rse_exp,   color="#1f77b4", linewidth=2, label="ExpSketch")
    ax.plot(exponents, data.rse_kqsk,  color="#2ca02c", linewidth=2,
            label=f"kQSketch (k={data.k:.0f}, b={data.b_bits}) Newton-Warm")
    ax.plot(exponents, data.rse_round, color="#d62728", linewidth=2,
            label=f"kQSketchRounding (k={data.k:.0f}, b={data.b_bits})")
    ax.plot(exponents, data.rse_round_corrected, color="#8c1b1b", linewidth=2, linestyle="--",
            label=f"kQSketchRounding corrected (k={data.k:.0f}, b={data.b_bits})")
    ax.set_xlabel(r"$\log_{10}(\Lambda)$")
    ax.set_ylabel("RSE")
    ax.legend()
    ax.grid(True, alpha=0.3, linestyle="--")
    fig.tight_layout()

    out.savefig(fig, FIGURE_KEY)
    out.save_tex_figure(
        FIGURE_KEY,
        caption=get_caption(m=data.m, n_reps=data.n_reps, k=data.k, b_bits=data.b_bits),
        label="kqsketch-rounding-accuracy",
    )


if __name__ == "__main__":
    main()

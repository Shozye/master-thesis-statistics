import numpy as np
import matplotlib.pyplot as plt

from generated_output_manager import GeneratedOutputManager
from data_for_figure_dataclass import DataModel

FIGURE_KEY = "fisher-info-loss-ratio"

B_BITS = 8
R_MIN = -2 ** (B_BITS - 1) + 1
R_MAX = 2 ** (B_BITS - 1) - 1
LAMBDA_FIXED = [1e-5, 1, 1e5]


def get_caption(n_points: int) -> str:
    return (
        rf"Fisher information loss ratio \(\rho = I_X(\Lambda)/I_Z(\Lambda)\) "
        rf"for \(b={B_BITS}\) bits (\(r_{{\min}}={R_MIN}\), \(r_{{\max}}={R_MAX}\)). "
        rf"Left: \(\rho\) vs \(\Lambda\) for fixed \(k\). "
        rf"Right: \(\rho\) vs \(k\) for fixed \(\Lambda\). "
        rf"{n_points} points per curve."
    )


def get_test_caption() -> str:
    return get_caption(n_points=50)


def main() -> None:
    out = GeneratedOutputManager(__file__)
    data = out.load_dataclass(DataModel)

    lambdas = np.array(data.lambdas)
    ks = np.array(data.ks)
    coeffs = np.array(data.linear_fit_coeffs)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5))

    # Left: ρ vs λ for fixed k
    colors_left = plt.cm.tab10(np.linspace(0, 0.4, len(data.k_fixed)))
    for k, color, rhos in zip(data.k_fixed, colors_left, data.rhos_left):
        ax1.plot(lambdas, rhos, label=rf"$k={k}$", color=color, linewidth=2)
    ax1.set_xlabel(r"$\Lambda$")
    ax1.set_ylabel(r"$\rho(\Lambda, k)$")
    ax1.set_title(r"Fixed $k$, varying $\Lambda$")
    ax1.legend()
    ax1.grid(True, alpha=0.3, linestyle="--")

    # Right: ρ vs k for fixed λ
    colors_right = ["#1f77b4", "#2ca02c", "#d62728"]
    linestyles = ["-", (0, (5, 3)), (0, (1, 1))]
    for (lam, color, ls, rhos) in zip(LAMBDA_FIXED, colors_right, linestyles, data.rhos_right):
        if lam == 1:
            lbl = r"$\Lambda=1$"
        else:
            exp = int(np.log10(lam))
            lbl = rf"$\Lambda=10^{{{exp}}}$"
        ax2.plot(ks, rhos, label=lbl, color=color, linewidth=2, linestyle=ls)

    # Annotate k=2
    ax2.axvline(x=2.0, color="gray", linestyle=":", linewidth=1, zorder=1)
    ax2.axhline(y=data.rho_at_k2, color="gray", linestyle=":", linewidth=1, zorder=1)
    ax2.plot(2.0, data.rho_at_k2, "ko", markersize=5, zorder=5)

    current_yticks = ax2.get_yticks()
    new_yticks = sorted([*current_yticks, data.rho_at_k2])
    ax2.set_yticks(new_yticks)

    ks_draw = ks[ks >= 1.3]
    ax2.plot(
        ks_draw, np.polyval(coeffs, ks_draw),
        color="black", linestyle=(0, (8, 5)), linewidth=0.8, alpha=0.5,
        label=rf"linear fit: $\rho \approx {coeffs[0]:.3f}\,k {coeffs[1]:+.3f}$",
    )

    ax2.set_xlabel(r"$k$")
    ax2.set_ylabel(r"$\rho(\Lambda, k)$")
    ax2.set_title(r"Fixed $\Lambda$, varying $k$")
    ax2.legend()
    ax2.grid(True, alpha=0.3, linestyle="--")

    fig.tight_layout()

    out.savefig(fig, FIGURE_KEY)
    out.save_tex_figure(
        FIGURE_KEY,
        caption=get_caption(n_points=data.n_points),
        label="fisher-info-loss-ratio",
    )


if __name__ == "__main__":
    main()

import numpy as np
import matplotlib.pyplot as plt

from generated_output_manager import GeneratedOutputManager
from data_for_figure_dataclass import DataModel

FIGURE_KEY = "kqsketch-shifted-reg-histos"


def get_caption(b: int, lam: float, m: int) -> str:
    return (
        rf"Register value histograms at \(b={b}\), \(\Lambda={lam:.0e}\), \(m={m}\). "
        rf"\textbf{{(a)}}~\kQSketch{{}}. \textbf{{(b)}}~\kQSketchShifted{{}}."
    )


def get_test_caption() -> str:
    return get_caption(b=5, lam=5e4, m=10000)


def main():
    out = GeneratedOutputManager(__file__)
    d = out.load_dataclass(DataModel)

    regs_kq_rel = np.array(d.regs_kq_rel)
    regs_sh_rel = np.array(d.regs_sh_rel)
    capacity = 2**d.b - 1
    rmin = -2 ** (d.b - 1) + 1
    rmax = 2 ** (d.b - 1) - 1
    bins = np.arange(-0.5, capacity + 1.5, 1)

    fig, (ax_a, ax_b) = plt.subplots(1, 2, figsize=(12, 4.5), sharey=True)

    # (a) kQSketch
    ax_a.hist(regs_kq_rel, bins=bins, alpha=0.7, color="#d62728",
              edgecolor="#d62728", linewidth=1.5,
              weights=np.ones_like(regs_kq_rel) / len(regs_kq_rel))
    ax_a.axvline(0, color="black", linestyle="--", linewidth=2, label=rf"$r_{{\min}}={rmin}$")
    ax_a.axvline(capacity, color="black", linestyle=":", linewidth=2, label=rf"$r_{{\max}}={rmax}$")
    ax_a.set_xlabel("Relative register value")
    ax_a.set_ylabel("Ratio")
    ax_a.set_ylim(0, 1)
    ax_a.set_title(r"(a) $k$-QSketch")
    ax_a.legend(fontsize=8)
    ax_a.grid(alpha=0.3, linestyle="--")

    # (b) kQSketchShifted
    ax_b.hist(regs_sh_rel, bins=bins, alpha=0.7, color="#1f77b4",
              edgecolor="#1f77b4", linewidth=1.5,
              weights=np.ones_like(regs_sh_rel) / len(regs_sh_rel))
    ax_b.axvline(0, color="black", linestyle="--", linewidth=2, label=rf"offset$={d.offset}$")
    ax_b.axvline(capacity, color="black", linestyle=":", linewidth=2, label=rf"capacity$={capacity}$")
    ax_b.set_xlabel("Relative register value")
    ax_b.set_title(r"(b) $k$-QSketch-Shifted")
    ax_b.legend(fontsize=8)
    ax_b.grid(alpha=0.3, linestyle="--")

    fig.tight_layout()
    out.savefig(fig, FIGURE_KEY)
    out.save_tex_figure(
        FIGURE_KEY,
        caption=get_caption(d.b, d.lam, d.m),
        label="kqsketch-shifted-reg-histos",
        width=r"0.95\textwidth",
        placement="ht",
    )


if __name__ == "__main__":
    main()

import matplotlib.pyplot as plt

from generated_output_manager import GeneratedOutputManager
from data_for_figure_dataclass import DataModel

FIGURE_KEY = "kqsketchshifted-rng-comparison"

RNG_COLORS = {
    "PCG64": "#1f77b4",
    "MT19937": "#ff7f0e",
    "XOSHIRO128PP": "#2ca02c",
    "XOSHIRO256PP": "#d62728",
}


def get_caption() -> str:
    return (
        rf"Mean per-element addition time and mean relative error vs sketch size $m$ "
        rf"for \kQSketchShifted{{}} ($b = 8$, $k = 2$) across four RNG engines."
    )


def get_test_caption() -> str:
    return get_caption()


def main() -> None:
    out = GeneratedOutputManager(__file__)
    data = out.load_dataclass(DataModel)

    fig, (ax_time, ax_err) = plt.subplots(1, 2, figsize=(10, 4))

    for rng_name, color in RNG_COLORS.items():
        ax_time.plot(data.ms, data.times[rng_name], linewidth=1.5, color=color, label=rng_name)
        ax_err.plot(data.ms, data.errors[rng_name], linewidth=1.5, color=color, label=rng_name)

    ax_time.set_title("Mean addition time", fontsize=10)
    ax_time.set_xlabel("$m$", fontsize=9)
    ax_time.set_ylabel(r"$\mu$s/element", fontsize=9)
    ax_time.grid(True, alpha=0.3, linestyle="--")
    ax_time.tick_params(labelsize=8)
    ax_time.legend(fontsize=8)

    ax_err.set_title("Mean relative error", fontsize=10)
    ax_err.set_xlabel("$m$", fontsize=9)
    ax_err.set_ylabel("MRE", fontsize=9)
    ax_err.grid(True, alpha=0.3, linestyle="--")
    ax_err.tick_params(labelsize=8)

    fig.tight_layout()

    out.savefig(fig, FIGURE_KEY)
    out.save_tex_figure(FIGURE_KEY, caption=get_caption(), label=FIGURE_KEY, width=r"0.8\textwidth")


if __name__ == "__main__":
    main()

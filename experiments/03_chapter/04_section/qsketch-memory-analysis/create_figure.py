import math

from data_for_figure_dataclass import DataModel
from generated_output_manager import DRAFT, DraftLevel, GeneratedOutputManager

FIGURE_KEY = "qsketch-memory-analysis"


def get_caption() -> str:
    return r"""NO CAPTION NEEDED"""


def get_test_caption() -> str:
    return get_caption()


def main() -> None:
    out = GeneratedOutputManager(__file__)
    d = out.load_dataclass(DataModel)

    M, B = d.m, d.b

    ratio_exp32 = 1.0
    ratio_base_qsk = d.base_qsk_total / d.exp32_total
    ratio_fast32 = 1.0
    ratio_qsk = d.qsk_total / d.fast32_total

    theo_exp32 = r"\(4m + 8\)"
    theo_base_qsk = r"\(\lceil mb/8 \rceil + 21\)"
    theo_fast32 = r"\(4m + \lceil 2m\lceil\log_2 m\rceil / 8 \rceil + 44\)"
    theo_qsk = r"\(\lceil mb/8 \rceil + \lceil 2m\lceil\log_2 m\rceil / 8 \rceil + 53\)"

    def fmt_bytes(v: int) -> str:
        return f"{v:,}".replace(",", r"\,")

    def fmt_rse(v: float) -> str:
        return rf"\({v * 100:.2f}\)"

    def fmt_ratio(v: float) -> str:
        if v == 1.0:
            return r"\(1\)"
        return rf"\({v:.2f}\)"

    rows = [
        (r"ExpSketch[f32]", M, d.rse_exp32, d.exp32_registers, d.exp32_fast, d.exp32_total, ratio_exp32, theo_exp32),
        (rf"BaseQSketch \(b={B}\)", M, d.rse_qsk, d.base_qsk_registers, d.base_qsk_fast, d.base_qsk_total, ratio_base_qsk, theo_base_qsk),
        (r"FastExpSketch[f32]", M, d.rse_fast32, d.fast32_registers, d.fast32_fast, d.fast32_total, ratio_fast32, theo_fast32),
        (rf"QSketch \(b={B}\)", M, d.rse_qsk, d.qsk_registers, d.qsk_fast, d.qsk_total, ratio_qsk, theo_qsk),
    ]

    lines = []
    for i, (name, m, rse, regs, fast, total, ratio, theo) in enumerate(rows):
        fast_str = fmt_bytes(fast) if fast > 0 else "---"
        lines.append(
            f"  {name} & {m} & {fmt_rse(rse)} & {fmt_bytes(regs)} & {fast_str} & {fmt_bytes(total)} & {fmt_ratio(ratio)} & {theo} \\\\"
        )
        if i == 1:
            lines.append(r"  \midrule")

    caption = rf"Full memory breakdown of ExpSketch[f32], FastExpSketch[f32] and QSketch(\(b={B}\)) at \(m={M}\)."
    if DRAFT != DraftLevel.DRAFT_FINAL_VERSION:
        experiment_path = r"experiments/03\_chapter/01\_section/qsketch-memory-analysis"
        caption += rf" \texttt{{\small {experiment_path}}}"

    table = rf"""\begin{{table}}[ht]
\centering
\caption{{{caption}}}
\label{{tab:qsketch-memory-analysis}}
\small
\begin{{tabular}}{{@{{}}lcrrrrrc@{{}}}}
\toprule
\textbf{{Sketch}} & \textbf{{\(m\)}} & \textbf{{RSE}} & \textbf{{Registers}} & \textbf{{Fast}} & \textbf{{Total}} & \textbf{{Ratio}} & \textbf{{Theoretical Total}} \\
 & & \% & bytes & bytes & bytes & & \\
\midrule
{chr(10).join(lines)}
\bottomrule
\end{{tabular}}
\end{{table}}"""

    out.save_text(table, FIGURE_KEY + ".tex")


if __name__ == "__main__":
    main()

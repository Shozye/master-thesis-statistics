from data_for_figure_dataclass import DataModel
from generated_output_manager import DRAFT, DraftLevel, GeneratedOutputManager

FIGURE_KEY = "qsketchdyn-memory-analysis"


def get_caption() -> str:
    return r"""NO CAPTION NEEDED"""


def get_test_caption() -> str:
    return get_caption()


def main() -> None:
    out = GeneratedOutputManager(__file__)
    d = out.load_dataclass(DataModel)

    B = d.b
    # Reconstruct groups: 4 rows per m value
    all_rows = [d.rows[i:i+4] for i in range(0, len(d.rows), 4)]

    def fmt_bytes(v: int) -> str:
        return f"{v:,}".replace(",", r"\,")

    def fmt_rse(v: float) -> str:
        return rf"\({v * 100:.2f}\)"

    def fmt_time(v: float) -> str:
        return rf"\({v:.2f}\)"

    lines = []
    for group_idx, group in enumerate(all_rows):
        for name, m, rse, reg, hist, fast, total, t_us, e_us in group:
            hist_str = fmt_bytes(hist) if hist > 0 else "---"
            fast_str = fmt_bytes(fast) if fast > 0 else "---"
            lines.append(
                f"  {name} & {m} & {fmt_rse(rse)} & {fmt_bytes(reg)}"
                f" & {hist_str} & {fast_str} & {fmt_bytes(total)} & {fmt_time(t_us)} & {fmt_time(e_us)} \\\\"
            )
        if group_idx < len(all_rows) - 1:
            lines.append(r"  \midrule")

    caption = rf"Performance of QSketchDyn(\(b={B}\)) vs ExpSketch and FastExpSketch at \(m=100\) and \(m=400\)."
    if DRAFT != DraftLevel.DRAFT_FINAL_VERSION:
        experiment_path = r"experiments/03\_chapter/01\_section/qsketchdyn-memory-analysis"
        caption += rf" \texttt{{\small {experiment_path}}}"

    table = rf"""\begin{{table}}[ht]
\centering
\caption{{{caption}}}
\label{{tab:qsketchdyn-memory-analysis}}
\small
\begin{{tabular}}{{@{{}}lcrrrrrrr@{{}}}}
\toprule
\textbf{{Sketch}} & \textbf{{\(m\)}} & \textbf{{RSE}} & \textbf{{Registers}} & \textbf{{Histogram}} & \textbf{{Fast}} & \textbf{{Total}} & \textbf{{Update}} & \textbf{{Estimate}} \\
 & & \% & bytes & bytes & bytes & bytes & \(\mu\)s & \(\mu\)s \\
\midrule
{chr(10).join(lines)}
\bottomrule
\end{{tabular}}
\end{{table}}"""

    out.save_text(table, FIGURE_KEY + ".tex")


if __name__ == "__main__":
    main()

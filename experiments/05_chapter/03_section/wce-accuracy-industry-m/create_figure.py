from generated_output_manager import GeneratedOutputManager
from data_for_figure_dataclass import DataModel

FIGURE_KEY = "wce-accuracy-industry-m"


def get_caption(n_elements: int, n_reps: int) -> str:
    return (
        rf"Empirical \RSE{{}} (\%) of mergeable weighted cardinality sketches at industry-standard"
        rf" \(\SketchSize\) values. Stream of \(n = {n_elements}\) elements with"
        rf" \(\DistUnif[1,10]\) weights. Average over {n_reps} repetitions."
    )


def get_test_caption() -> str:
    return get_caption(n_elements=10000, n_reps=5000)


def main() -> None:
    out = GeneratedOutputManager(__file__)
    data = out.load_dataclass(DataModel)

    # Build LaTeX table
    m_cols = " ".join(rf"r" for _ in data.m_values)
    header = " & ".join(rf"\({m:,}\)" for m in data.m_values)
    header = header.replace(",", r"\,")

    lines = [
        r"\begin{table}[ht]",
        r"\centering",
        rf"\caption{{{get_caption(data.n_elements, data.n_reps)}}}",
        r"\label{tab:ch5-wce-accuracy-industry-m}",
        rf"\begin{{tabular}}{{l {m_cols}}}",
        r"\toprule",
        rf"\textbf{{Sketch}} & {header} \\",
        r"\midrule",
    ]

    for label, rse_row in zip(data.labels, data.rse_values):
        cells = " & ".join(f"{rse * 100:.2f}\\%" for rse in rse_row)
        lines.append(rf"{label} & {cells} \\")

    lines += [
        r"\bottomrule",
        r"\end{tabular}",
        r"\end{table}",
    ]

    out.save_text("\n".join(lines), f"{FIGURE_KEY}.tex")


if __name__ == "__main__":
    main()

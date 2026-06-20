from generated_output_manager import GeneratedOutputManager
from data_for_figure_dataclass import DataModel

FIGURE_KEY = "float-formats-table-macheps"


def get_caption() -> str:
    return r"""Floating-point formats referenced in this thesis. \(s\)~is the number of sign bits, \(q\)~the number of exponent bits, \(p\)~the number of mantissa bits. \(\varepsilon_{\mathrm{mach}}\) is the gap between \(1\) and the next representable number above~\(1\). Features lists which special values the format supports (sub = subnormals)."""


def get_test_caption() -> str:
    return get_caption()


def main() -> None:
    out = GeneratedOutputManager(__file__)
    data = out.load_dataclass(DataModel)

    table_body = " \\\\\n    ".join(data.rows)
    tex = (
        "\\begin{table}[ht]\n"
        "  \\centering\n"
        "  \\begin{tabular}{llccccccc}\n"
        "    \\toprule\n"
        r"      Origin & Common name & \(s\) & \(q\) & \(p\) & Bits & Smallest positive & \(\varepsilon_{\mathrm{mach}}\) & Features"
        " \\\\\n"
        "    \\midrule\n"
        f"      {table_body} \\\\\n"
        "    \\bottomrule\n"
        "  \\end{tabular}\n"
        f"  \\caption{{{get_caption()}}}\n"
        "  \\label{tab:float-formats}\n"
        "\\end{table}\n"
    )
    out.save_text(tex, FIGURE_KEY + ".tex")


if __name__ == "__main__":
    main()

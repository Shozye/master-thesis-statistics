# ---
# description: Table of common IEEE 754 float formats with macheps and smallest positive value
# ---
"""
Experiment: Generate a LaTeX table of floating-point formats.

Columns: origin, common name, s, q, p, total bits, smallest positive (subnormal), macheps.
Output: generated_output/03_chapter/float-formats-table-macheps/
"""

import numpy as np

from generated_output_manager import DRAFT, DraftLevel, GeneratedOutputManager
from data_for_figure_dataclass import DataModel

# REVIEWED AND ACCEPTED DRAFT VARIABLES. Deterministic; dummy variable, output never changes.
# BENCHMARK: DRAFT=0: .9s, DRAFT=1: 1.0s, DRAFT=2: 1.0s.
# Variables below exist only to meet the validator.
match DRAFT:
    case DraftLevel.DRAFT_FINAL_VERSION:
        THIS_CONSTANT_IS_NECESSARY_FOR_CHECK_TO_PASS_HUMAN_APPROVED = 0
    case DraftLevel.DRAFT_FOR_HUMAN_TO_VIEW_LATEX:
        THIS_CONSTANT_IS_NECESSARY_FOR_CHECK_TO_PASS_HUMAN_APPROVED = 0
    case DraftLevel.DRAFT_TO_FIX_EXPERIMENT_OR_SEE_IF_IT_COMPILES:
        THIS_CONSTANT_IS_NECESSARY_FOR_CHECK_TO_PASS_HUMAN_APPROVED = 0

# (name, origin, s, q, p, numpy_dtype_or_None, has_subnormals, features)
# features: subset of {NaN, ±∞, ±0, subnormals}
FORMATS = [
    ("FP8 E4M3", "NVIDIA", 1, 4, 3, None, True, r"NaN, $\pm 0$, sub"),
    ("FP8 E5M2", "NVIDIA", 1, 5, 2, None, True, r"NaN, $\pm\infty$, $\pm 0$, sub"),
    ("10-bit ufloat", "Vulkan/OpenGL", 0, 5, 5, None, True, r"NaN, $+\infty$, $+0$, sub"),
    ("11-bit ufloat", "Vulkan/OpenGL", 0, 5, 6, None, True, r"NaN, $+\infty$, $+0$, sub"),
    ("float16", "IEEE 754", 1, 5, 10, np.float16, True, r"NaN, $\pm\infty$, $\pm 0$, sub"),
    ("bfloat16", "Google", 1, 8, 7, None, True, r"NaN, $\pm\infty$, $\pm 0$, sub"),
    # IBM DLFloat: no subnormals; a single merged NaN/Inf encoding.
    ("DLFloat16", "IBM", 1, 6, 9, None, False, r"NaN/$\infty$ merged, $\pm 0$"),
    ("TF32", "NVIDIA", 1, 8, 10, None, True, r"NaN, $\pm\infty$, $\pm 0$, sub"),
    ("float32", "IEEE 754", 1, 8, 23, np.float32, True, r"NaN, $\pm\infty$, $\pm 0$, sub"),
    ("float64", "IEEE 754", 1, 11, 52, np.float64, True, r"NaN, $\pm\infty$, $\pm 0$, sub"),
]


def smallest_positive(s: int, q: int, p: int, has_subnormals: bool = True) -> float | None:
    """Smallest positive value. With subnormals: 2^(emin - p). Without: 2^emin."""
    if p == 0:
        return None
    if s == 0 and q == 5:
        # Unsigned Vulkan floats: bias=15
        emin = 1 - 15
    else:
        emin = 2 - 2 ** (q - 1)
    if has_subnormals:
        return 2.0 ** (emin - p)
    return 2.0 ** emin


def macheps(p: int) -> float | None:
    """Machine epsilon: 2^(-p). None if p=0."""
    if p == 0:
        return None
    return 2.0 ** (-p)


def fmt_power(exp: int) -> str:
    return rf"\(2^{{{exp}}}\)"



def main() -> None:
    out = GeneratedOutputManager(__file__)

    rows = []
    for name, origin, s, q, p, dtype, has_subnormals, features in FORMATS:
        total = s + q + p
        eps = macheps(p)
        tiny = smallest_positive(s, q, p, has_subnormals=has_subnormals)

        if dtype is not None:
            fi = np.finfo(dtype)
            assert eps == fi.eps, f"{name}: eps mismatch {eps} vs {fi.eps}"
            assert tiny == fi.smallest_subnormal, (
                f"{name}: tiny mismatch {tiny} vs {fi.smallest_subnormal}"
            )

        tiny_str = fmt_power(int(np.log2(tiny))) if tiny is not None else "---"
        eps_str = fmt_power(-p) if eps is not None else "---"

        row = rf"{origin} & \texttt{{{name}}} & {s} & {q} & {p} & {total} & {tiny_str} & {eps_str} & {features}"
        rows.append(row)

    # Add custom row for thesis format: no sign, no NaN/Inf/zero/subnormals
    row = r"This thesis & \(E\{q\}M\{p\}\) & \(0\) & \(q\) & \(p\) & \(q+p\) & \(2^{(2-2^{q-1})}\) & \(2^{-p}\) & none"
    rows.append(row)

    out.save_dataclass(DataModel(rows=rows), DataModel)


if __name__ == "__main__":
    main()

# ---
# description: Total memory ratio of FastExpSketchCustomFloat(p=7,q=8) to QSketch(b=8) at equal RSE, swept over sketch size m.
# ---
"""
Experiment: Compare total memory of the parametrized ExpSketch register format
FastExpSketchCustomFloat(p=7, q=8) (15 bits/register) against QSketch(b=8) at
equal RSE, as a function of sketch size m.

To match ExpSketch's RSE, QSketch needs m' = ceil(rho * m) registers, where
rho ~ 1.0747 is the Fisher information loss ratio (b=8, k=2). Both totals use
the fast-update framework (Fisher-Yates + PCG64) and count seeds as 0 bytes,
following the memory model of qsketch-memory-analysis. The output is the ratio
T_E(7,8) / T_Q8 over a log-spaced sweep of m.

Output: generated_output/04_chapter/04_section/expsketch-to-qsketch-ratio/
"""

import math
import numpy as np

from generated_output_manager import DRAFT, DraftLevel, GeneratedOutputManager
from data_for_figure_dataclass import DataModel

# Memory is computed analytically (no sampling), so DRAFT only controls how many
# points are placed on the m-axis for plot smoothness.
match DRAFT:
    case DraftLevel.DRAFT_FINAL_VERSION:
        N_POINTS = 10000
    case DraftLevel.DRAFT_FOR_HUMAN_TO_VIEW_LATEX:
        N_POINTS = 2000
    case DraftLevel.DRAFT_TO_FIX_EXPERIMENT_OR_SEE_IF_IT_COMPILES:
        N_POINTS = 1000

# Fisher information loss ratio for QSketch(b=8) at k=2 (see Section 4.1.2).
RHO = 1.0747
M_MIN = 100
M_MAX = 1_000_000_000
# Parametrized ExpSketch register width: q=8 exponent + p=7 mantissa bits.
EXP_BITS = 8
MANT_BITS = 7
CUSTOM_FLOAT_BITS = EXP_BITS + MANT_BITS  # 15
B = 8  # QSketch bits per register

RNG_BYTES = 32  # PCG64 state
AUX_BYTES = 8   # auxiliary instance variables


def compact_vector_bytes(size: int, bits: int) -> int:
    """ceil(size * bits / 8): bytes used by a bit-packed compact vector."""
    return math.ceil(size * bits / 8)


def fisher_yates_bytes(m: int) -> int:
    """Two permutations over m elements plus the RNG state."""
    return 2 * compact_vector_bytes(m, math.ceil(math.log2(m))) + RNG_BYTES


def total_expsketch_custom_float(m: int) -> int:
    """FastExpSketchCustomFloat(p=7, q=8) total bytes (fast framework)."""
    registers = compact_vector_bytes(m, CUSTOM_FLOAT_BITS)
    fast = fisher_yates_bytes(m) + 4  # + register MAX
    return registers + fast + AUX_BYTES


def total_qsketch(mp: int) -> int:
    """QSketch(b=8) total bytes (fast framework)."""
    # registers + r_max + r_min + amount_bits + j_star
    registers = compact_vector_bytes(mp, B) + 4 + 4 + 1 + 4
    fast = fisher_yates_bytes(mp)
    return registers + fast + AUX_BYTES


def main() -> None:
    out = GeneratedOutputManager(__file__)

    ms = np.unique(
        np.geomspace(M_MIN, M_MAX, N_POINTS).round().astype(int)
    ).tolist()
    mps = [math.ceil(RHO * m) for m in ms]
    t_e = [total_expsketch_custom_float(m) for m in ms]
    t_q = [total_qsketch(mp) for mp in mps]

    m_ref = 100
    mp_ref = math.ceil(RHO * m_ref)

    # Guide points read off the left OY axis (value annotated on the left).
    guide_ms_left = [100, 1000]
    # Guide points read off the right side (value annotated on the right). Using
    # an exact power of two (2^28) so the bottom label renders as 2^28 ~ 2.68e8.
    guide_ms_right = [1_000_000, 2 ** 28]

    out.save_dataclass(
        DataModel(
            rho=RHO,
            asymptote=1.0 / RHO,
            ms=ms,
            mps=mps,
            t_e=t_e,
            t_q=t_q,
            m_ref=m_ref,
            mp_ref=mp_ref,
            t_e_ref=total_expsketch_custom_float(m_ref),
            t_q_ref=total_qsketch(mp_ref),
            guide_ms_left=guide_ms_left,
            guide_t_e_left=[total_expsketch_custom_float(m) for m in guide_ms_left],
            guide_t_q_left=[total_qsketch(math.ceil(RHO * m)) for m in guide_ms_left],
            guide_ms_right=guide_ms_right,
            guide_t_e_right=[total_expsketch_custom_float(m) for m in guide_ms_right],
            guide_t_q_right=[total_qsketch(math.ceil(RHO * m)) for m in guide_ms_right],
        ),
        DataModel,
    )


if __name__ == "__main__":
    main()

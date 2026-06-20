from dataclasses import dataclass


@dataclass
class DataModel:
    # QSketch register inflation factor needed to match ExpSketch RSE (Fisher
    # information loss ratio at b=8, k=2).
    rho: float
    # Asymptotic ratio T_E/T_Q as m -> infinity (Fisher-Yates term dominates).
    asymptote: float

    # Sweep over sketch size.
    ms: list[int]          # ExpSketch register count m
    mps: list[int]         # QSketch register count m' = ceil(rho * m)
    t_e: list[int]         # FastExpSketchCustomFloat(p=7,q=8) total bytes
    t_q: list[int]         # QSketch(b=8) total bytes

    # Reference point at m = 100 (used in the surrounding prose).
    m_ref: int
    mp_ref: int
    t_e_ref: int
    t_q_ref: int

    # Guide points highlighted on the plot: the ratio value at each is marked
    # with dashed lines down to the OX axis and across to an OY axis. "left"
    # points have their value annotated on the left axis, "right" points on the
    # right side.
    guide_ms_left: list[int]
    guide_t_e_left: list[int]
    guide_t_q_left: list[int]
    guide_ms_right: list[int]
    guide_t_e_right: list[int]
    guide_t_q_right: list[int]

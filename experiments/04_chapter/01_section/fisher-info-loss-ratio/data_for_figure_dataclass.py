from dataclasses import dataclass


@dataclass
class DataModel:
    # Left subplot: rho vs lambda for fixed k values
    lambdas: list[float]
    k_fixed: list[float]
    rhos_left: list[list[float]]  # rhos_left[i] = rhos for k_fixed[i]
    # Right subplot: rho vs k for fixed lambda values
    ks: list[float]
    lambda_fixed: list[float]
    rhos_right: list[list[float]]  # rhos_right[i] = rhos for lambda_fixed[i]
    rho_at_k2: float
    linear_fit_coeffs: list[float]  # [slope, intercept]
    # Caption params
    n_points: int
    b_bits: int
    r_min: int
    r_max: int

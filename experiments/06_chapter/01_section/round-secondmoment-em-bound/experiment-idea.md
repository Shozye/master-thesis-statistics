---
description: Numerically evaluate the Euler-Maclaurin remainder bound for the rounding second-moment constant
---
# Idea eksperymentu

## Cel
Compute the tight Euler-Maclaurin remainder bound for the rounding second moment E[k^{-2R}],
R = round(-log_k S), used in the kQSketchRounding delta-method variance. The integrand is the exact
high-order derivative of the two-rate function g(t) = (t/Lambda)^2 [e^{-t k^{-1/2}} - e^{-t k^{1/2}}],
formed via the operator L = t d/dt as a single (polynomial)x(exponential) so the cancellation between
the two exponential terms is preserved. The quadratic prefactor t^2 changes the derivatives, so the
first-moment constant does not transfer.

## Co pokazuje wykres
A single numeric value: the upper bound |R_p| Lambda^2 at k = 2.4.

## Oczekiwany wniosek
The bound is small (about 4.5e-3), an order of magnitude larger than the first-moment constant but
still negligible; the tightest value is attained at even derivative order 10.

# Output

## Ile subplotów
0 (numeric output only, no figure)

## Rozkład subplotów (rzędy x kolumny)
N/A

## Osie
N/A

## Legenda
N/A

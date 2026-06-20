---
description: Numerically evaluate the Euler-Maclaurin remainder bound for the floor second-moment constant
---
# Idea eksperymentu

## Cel
Compute the tight Euler-Maclaurin remainder bound for the floor second moment E[k^{-2R}],
R = floor(-log_k X), used in the floor delta-method variance. The integrand is the exact
high-order derivative of g(t) = t^2 e^{-t}/Lambda^2, formed via the operator L = t d/dt as a single
(polynomial)x(exponential). This is the second-moment analogue of the Theta first-moment bound:
the quadratic prefactor t^2 changes the derivatives, so the first-moment constant does not transfer.

## Co pokazuje wykres
A single numeric value: the upper bound |R_p| Lambda^2 at k = 2.4.

## Oczekiwany wniosek
The bound is small (about 2e-3), an order of magnitude larger than the first-moment constant but
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

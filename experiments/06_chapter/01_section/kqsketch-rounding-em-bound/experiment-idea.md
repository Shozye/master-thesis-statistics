---
description: Numerically evaluate the Euler-Maclaurin remainder bound for the kQSketchRounding dequantizer constant
---
# Idea eksperymentu

## Cel
Compute the tight Euler-Maclaurin remainder bound for the rounding dequantizer expectation
E[k^{-R}], R = round(-log_k S), used in the kQSketchRounding constant proof. The integrand is
the exact high-order derivative of the two-rate function g(t) = (t/Lambda)[e^{-t k^{-1/2}} -
e^{-t k^{1/2}}], formed as a single (polynomial)x(exponential) so the cancellation between the
two exponential terms is preserved.

## Co pokazuje wykres
A single numeric value: the upper bound |R_p| at k = 2.4.

## Oczekiwany wniosek
The bound is small (< 0.0005), confirming the Euler-Maclaurin approximation is tight; the
tightest value is attained at derivative order 10.

# Output

## Ile subplotów
0 (numeric output only, no figure)

## Rozkład subplotów (rzędy x kolumny)
N/A

## Osie
N/A

## Legenda
N/A

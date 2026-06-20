# ---
# description: Graphic iteration (cobweb) of the Newton-Raphson fixed-point map for kQSketch cold vs warm start
# variables:
#   independent: [Lambda]
#   dependent: [newton_map]
# parameters:
#   k: 2
#   b: 8
#   m: 256
#   Lambda: 1e6
# ---

# Idea eksperymentu

## Cel
Visualise Newton-Raphson for the k-QSketch maximum-likelihood estimator as a
fixed-point iteration Lambda_{n+1} = g(Lambda_n), in the same cobweb style as the
quadratic-map graphic iteration. Contrast the cold start (Lambda_0 = k^{r_min})
with the warm start (direct estimator).

## Co pokazuje wykres
Both panels draw the diagonal y = Lambda, the Newton map g(Lambda), and the
staircase of successive iterates. Left panel: cold start over the full climb.
Right panel: warm start zoomed near the fixed point.

## Oczekiwany wniosek
The cold start sits far from the fixed point and needs a long staircase, while
the warm start begins essentially on the fixed point and settles in a couple of
steps.

# Output

## Ile subplotów
2

## Rozkład subplotów (rzędy x kolumny)
1 x 2

## Osie
- Left: OX = Lambda_n (log), OY = Lambda_{n+1} (log)
- Right: OX = Lambda_n (log), OY = Lambda_{n+1} (log)

## Legenda
- y = Lambda, g(Lambda), graphic iteration, Lambda_0, fixed point

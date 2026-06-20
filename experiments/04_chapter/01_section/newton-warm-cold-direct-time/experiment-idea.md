# ---
# description: Compare estimation time and Newton iteration counts for Direct, Newton-Cold, and Newton-Warm
# variables:
#   independent: [m]
#   dependent: [time, iterations]
# parameters:
#   k: 2
#   b: 8
#   Lambda: 1000
#   m_range: [100, 400]
# ---

# Idea eksperymentu

## Cel
Show computational cost differences between Direct, Newton-Cold, and Newton-Warm estimators as sketch size m varies.

## Co pokazuje wykres
Left subplot shows wall-clock time for each estimator. Right subplot shows Newton-Raphson iteration count for cold and warm starts.

## Oczekiwany wniosek
Direct is fastest (no iteration). Newton-Warm needs fewer iterations than Newton-Cold due to better starting point. Time scales linearly with m.

# Output

## Ile subplotów
2

## Rozkład subplotów (rzędy x kolumny)
1 x 2

## Osie
- Left: OX = m, OY = time (μs)
- Right: OX = m, OY = iterations

## Legenda
- Left: Direct, Newton-Cold, Newton-Warm
- Right: Newton-Cold, Newton-Warm

---
status: done
---
# Idea eksperymentu

RSE of kQSketchShifted with b=5, Lambda=1000 for varying m and varying k.

## Cel

Show how sketch size m and logarithm base k affect RSE independently.

## Co pokazuje wykres

Left: RSE decreases as m grows (k=2 fixed). Right: RSE increases with k (m=100 fixed).

## Oczekiwany wniosek

RSE scales as ~1/sqrt(m). Smaller k gives lower RSE but needs more bits to avoid overflow.

# Output

## Ile subplotów

2

## Rozkład subplotów (rzędy x kolumny)

1x2

## Osie

Left: OX = m, OY = RSE. Right: OX = k, OY = RSE.

## Legenda

No legend needed (single line per subplot).

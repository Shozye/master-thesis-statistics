---
status: done
---
# Idea eksperymentu

## Cel
Show how kQSketchShifted and kQSketch RSE behaves across a wide Lambda range for different bit widths.

## Co pokazuje wykres
RSE vs log10(Lambda) for kQSketchShifted (b=4,5) and kQSketch (b=4,5,6,7) at m=64.

## Oczekiwany wniosek
kQSketch degrades at extreme Lambda values while kQSketchShifted remains stable across the full range with fewer bits.

# Output

## Ile subplotów
1

## Rozkład subplotów (rzędy x kolumny)
1x1

## Osie
OX = log10(Lambda) from -30 to 30, OY = RSE (0..1)

## Legenda
Lines for each sketch/bit combination: Shifted b=4, Shifted b=5, kQSketch b=4,5,6,7

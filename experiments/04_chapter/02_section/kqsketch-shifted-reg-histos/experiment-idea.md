---
status: done
---
# Idea eksperymentu

## Cel
Visualize register value distributions of kQSketch vs kQSketchShifted to show saturation in kQSketch.

## Co pokazuje wykres
Overlapping histograms of register values for kQSketch and kQSketchShifted at b=5, Lambda=5e4, m=10000.

## Oczekiwany wniosek
kQSketch registers saturate at rmin/rmax boundaries while kQSketchShifted uses the full dynamic range.

# Output

## Ile subplotów
1

## Rozkład subplotów (rzędy x kolumny)
1x1

## Osie
OX = relative register value, OY = ratio (fraction of registers)

## Legenda
Two overlapping histograms: k-QSketch, k-QSketch-Shifted, with boundary lines for rmin/rmax/offset/capacity

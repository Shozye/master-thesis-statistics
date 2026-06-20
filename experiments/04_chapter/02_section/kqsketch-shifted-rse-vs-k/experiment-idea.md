---
status: done
---
# Idea eksperymentu

RSE of kQSketchShifted (Newton warm) vs logarithm base k for multiple bit widths b={4,5,6,7}.

## Cel

Show how k affects RSE for different register bit widths and compare against QSketch baseline.

## Co pokazuje wykres

One curve per b showing RSE vs k from 1.2 to 2.4, with QSketch dashed baselines. Y-axis clipped to the interesting region around QSketch performance.

## Oczekiwany wniosek

For each b there is an optimal k range where kQSketchShifted beats or matches QSketch; beyond that, RSE skyrockets.

# Output

## Ile subplotów

1

## Rozkład subplotów (rzędy x kolumny)

1x1

## Osie

OX: logarithm base k. OY: RSE (clipped).

## Legenda

One solid line per b, one dashed QSketch baseline per b (matching colors).

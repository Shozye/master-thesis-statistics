# Idea eksperymentu

## Cel
Compare the RSE of kQSketchRounding against ExpSketch, QSketch(b=8), and kQSketch(k=2,b=8) with warm Newton estimator across a wide Lambda range.

## Co pokazuje wykres
Single plot showing RSE vs log10(Lambda) for all four sketches, demonstrating how rounding quantization compares to floor quantization.

## Oczekiwany wniosek
kQSketchRounding with the ExpSketch estimator achieves comparable or better accuracy than floor-based kQSketch across the full Lambda range.

# Output

## Ile subplotów
1

## Rozkład subplotów (rzędy x kolumny)
1 x 1

## Osie
- OX: log10(Lambda) from -11 to 11
- OY: RSE

## Legenda
Four lines: ExpSketch, QSketch(b=8), kQSketch(k=2,b=8) Newton-Warm, kQSketchRounding(k=2,b=8)

# Idea eksperymentu

## Cel
Wygenerować tabelę porównującą pełne zużycie pamięci QSketchDyn vs ExpSketch/FastExpSketch
przy m=100 i m=400, b=8. Pokazać że histogram T jest istotnym kosztem.

## Co pokazuje wykres
Kolumny: Sketch, m, RSE, Registers, Histogram, Fast, Total, Ratio.
Dwie grupy wierszy (m=100 i m=400), każda z ExpSketch, FastExpSketch, QSketchDyn.

## Oczekiwany wniosek
QSketchDyn nie oszczędza 1/8 pamięci bo histogram T jest duży.
Realistyczny stosunek to ~0.5 z seedami, ~0.25 bez seedów.

# Output

## Ile subplotów

TODO

## Rozkład subplotów (rzędy x kolumny)

TODO

## Osie

TODO

## Legenda

TODO

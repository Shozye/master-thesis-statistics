# Idea eksperymentu

## Cel
Wygenerować tabelę porównującą pełne zużycie pamięci (w bajtach) trzech szkiców:
ExpSketchFloat32, FastExpSketchFloat32 i QSketch(b=8) przy m=400.

## Co pokazuje wykres
Tabela z kolumnami: m, RSE, Registers, Fisher-Yates, Seeds, Total, Theoretical Total.
W komórkach Registers/Fisher-Yates/Seeds podana jest ilość bajtów.
Kolumna "Theoretical Total" podaje wzór obliczony ręcznie, np. m·⌈log₂m⌉ + 32 itp.

## Oczekiwany wniosek
QSketch z b=8 wcale nie oszczędza 8× pamięci w stosunku do ExpSketch float32,
bo pamięć seeds i Fisher-Yates dominuje nad pamięcią rejestrów.
Realne oszczędności są dużo mniejsze niż deklarowane 1/8.

# Output

## Ile subplotów

TODO

## Rozkład subplotów (rzędy x kolumny)

TODO

## Osie

TODO

## Legenda

TODO

# Idea eksperymentu

## Cel
Pokazanie, że FastExpSketchCustomFloat z p=7, q=8 daje identyczną dokładność jak ExpSketchFloat32 na pełnym zakresie Lambda. Uzasadnia to użycie 15-bitowego rejestru zamiast 32-bitowego bez straty dokładności.

## Co pokazuje wykres
Wykres: RSE vs log10(Lambda) dla FastExpSketchCustomFloat(p=7,q=8) i ExpSketchFloat32. Obie krzywe powinny się pokrywać.

## Oczekiwany wniosek
Obie krzywe są identyczne — 15-bitowy custom float (p=7, q=8) w pełni odwzorowuje dokładność float32.

# Output

## Ile subplotów
1

## Rozkład subplotów (rzędy x kolumny)
1x1

## Osie
OX: log10(Lambda), OY: RSE

## Legenda
CustomFloat(p=7, q=8), ExpSketchFloat32, RSE = 1/sqrt(m-2)

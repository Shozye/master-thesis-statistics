# Idea eksperymentu

## Cel

Pokazać, jak topnieje przewaga pamięciowa QSketch nad ExpSketch, gdy rejestry
ExpSketch zostaną sparametryzowane do FastExpSketchCustomFloat(p=7, q=8), czyli
15 bitów na rejestr zamiast 32. Porównanie przy wyrównanym RSE: QSketch używa
m' = ceil(rho * m) rejestrów (rho ~ 1.0747).

## Co pokazuje wykres

Stosunek całkowitej pamięci T_E(7,8) / T_Q8 w funkcji rozmiaru szkicu m
(oś X w skali logarytmicznej), wraz z linią parytetu (y=1) i asymptotą 1/rho.

## Oczekiwany wniosek

Przewaga QSketch spada z 43% (wobec float32) do skromnych ~7-15%, maleje wraz z
m i dąży do progu opłacalności dopiero przy nierealistycznie dużym m (~2^43),
bo wspólny narzut Fisher-Yatesa, skalowany przez większe m', zaczyna dominować.

# Output

## Ile subplotów

1

## Rozkład subplotów (rzędy x kolumny)

1 x 1

## Osie

OX: rozmiar szkicu m (skala log). OY: stosunek pamięci T_E(7,8) / T_Q8.

## Legenda

Krzywa stosunku, linia parytetu (y=1) oraz asymptota 1/rho.

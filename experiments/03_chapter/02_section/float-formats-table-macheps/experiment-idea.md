# Idea eksperymentu

## Cel
Wygenerowanie tabelki z najczesciej uzywanymi formatami zmiennoprzecinkowymi IEEE 754.
Tabelka uzywa sie w sekcji o ExpSketch zeby czytelnik mial pod reka konkretne wartosci
macheps, najmniejszej liczby i calkowitej liczby bitow.

## Co pokazuje wykres
Tabelka z kolumnami: nazwa formatu, bity eksponenty, bity mantysy, calkowita liczba bitow,
najmniejsza liczba (subnormal, najblizsza 0), macheps (eps_mach).

## Oczekiwany wniosek
Czytelnik widzi ze float16 ma macheps ~10^-3 wiec rejestry blisko 1 moga reprezentowac
tylko ~1000 roznych wartosci, a blisko 0 rozdzielczosc jest duzo lepsza.

# Output

## Ile subplotów

TODO

## Rozkład subplotów (rzędy x kolumny)

TODO

## Osie

TODO

## Legenda

TODO

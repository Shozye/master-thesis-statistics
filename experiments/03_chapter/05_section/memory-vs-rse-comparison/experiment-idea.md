# Idea eksperymentu

## Cel
Porównanie pamięć vs RSE dla QSketchDyn, QSketch, WeightedHyperLogLog.
Pokazanie efektywności informacyjnej różnych szkiców z rozdziału 3.
Pamięć liczona jak w analizie pamięci QSketch (seeds=0 bytes, best-case).

## Co pokazuje wykres
- OŚ X: całkowita pamięć szkicu (bajty)
- OŚ Y: RSE (relative standard error)

## Oczekiwany wniosek
QSketchDyn i QSketch mają lepszą efektywność pamięciową niż WeightedHyperLogLog.
Przy tej samej pamięci mają niższy RSE.

# Output

## Ile subplotów

1

## Rozkład subplotów (rzędy x kolumny)

1x1

## Osie

- OX: Total memory (bytes), liniowa
- OY: RSE, liniowa

## Legenda

Trzy linie: QSketchDyn, QSketch, WeightedHyperLogLog

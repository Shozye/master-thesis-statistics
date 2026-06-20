# Idea eksperymentu

## Cel
Zmierzyć czas aktualizacji (add_many) różnych szkiców ważonej kardynalności w zależności od m.
Porównać throughput (elementy/sekundę) dla m=100, m=400, m=10000.

## Co pokazuje wykres
- OŚ X: m (liczba rejestrów)
- OŚ Y: czas aktualizacji n=1000 elementów (μs)
- Każda linia to inna rodzina szkiców

## Oczekiwany wniosek
FastExpSketch/Float32 są najszybsze. kQSketch/LogExpSketch mają mały narzut.
ExpSketch jest wolny (O(n) porównań). Czas rośnie liniowo z m dla wolnych wariantów.

# Output

## Ile subplotów

1

## Rozkład subplotów (rzędy x kolumny)

1x1

## Osie

- OX: m (number of registers), logarytmiczna
- OY: Update time for n=1000 elements (μs), logarytmiczna

## Legenda

Linie: FastExpSketch, FastExpSketchFloat32, QSketch(b=8), kQSketchShifted(b=6), LogExpSketchFastNoShifted(b=8,e=5), ExpSketch

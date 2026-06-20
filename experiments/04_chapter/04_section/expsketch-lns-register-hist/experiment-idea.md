# ---
# description: LogExpSketch register value distribution histogram for varying Lambda and b
# ---

# Idea eksperymentu

## Cel
Pokazanie jak LogExpSketch rozkłada wartości rejestrów po siatce geometrycznej
po wstawieniu jednego elementu z różnymi wagami (Lambda).

## Co pokazuje wykres
Histogram wystąpień indeksów rejestrów.
Oś X: indeks rejestru (0 do 2^b - 1), Oś Y: liczba rejestrów o danym indeksie.
Trzy nałożone histogramy dla Lambda = 2^0, 2^5, 2^-5.

## Oczekiwany wniosek
Siatka geometryczna LNS rozkłada wartości bardziej równomiernie niż IEEE 754 custom float,
unikając artefaktu schodkowego widocznego na histogramie ExpSketchCustomFloat.

# Output

## Ile subplotów
1

## Rozkład subplotów (rzędy x kolumny)
1 x 1

## Osie
X: indeks rejestru (0..255), Y: liczba rejestrów

## Legenda
Lambda = 2^-5, Lambda = 2^0, Lambda = 2^5

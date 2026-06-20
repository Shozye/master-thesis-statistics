# Idea eksperymentu

## Cel
Compare the RSE (relative standard error) of the Newton-Raphson estimator vs the Direct estimator for kQSketch with k=2 and b=8 bits.

## Co pokazuje wykres
Two subplots showing that both estimators achieve similar accuracy across different Lambda values and sketch sizes.

## Oczekiwany wniosek
The direct estimator performs comparably to the Newton-Raphson method, confirming that it is a valid standalone estimator.

# Output

## Ile subplotów
2

## Rozkład subplotów (rzędy x kolumny)
1 x 2

## Osie
- Left: OX = log10(Lambda), OY = RSE
- Right: OX = m, OY = RSE

## Legenda
Two lines per subplot: Direct estimator, Newton-Raphson (warm start)

# Idea eksperymentu

## Cel
Empirically confirm that the direct estimators of kQSketch (floor quantization)
and kQSketchRounding (rounding quantization) meet the delta-method variance
guarantee derived in the appendix:
    Var[Lambda_bar] ≈ (Lambda^2 / m) * c(k),   c(k) = (k+1) ln(k) / (k-1) - 1,
equivalently RSE(k, m) = sqrt(c(k) / m).

## Co pokazuje wykres
Two subplots overlaying measured RSE on the theoretical prediction.
- Left: RSE vs m at fixed k=2, on log-log axes, against the line sqrt(c(2)/m).
- Right: RSE * sqrt(m) vs k at fixed m, against the constant curve sqrt(c(k)),
  which collapses the 1/sqrt(m) scaling so the coefficient is read directly.

## Oczekiwany wniosek
The empirical markers for both sketches sit on the theoretical curve across the
swept m and k (k <= 2.4), confirming the estimators attain the predicted
variance and that floor and rounding quantization share the same coefficient.

# Output

## Ile subplotów
2

## Rozkład subplotów (rzędy x kolumny)
1 x 2

## Osie
- Left: OX = m (log), OY = empirical RSE (log)
- Right: OX = k, OY = RSE * sqrt(m)

## Legenda
Three series per subplot: theory line, kQSketch (floor), kQSketchRounded.

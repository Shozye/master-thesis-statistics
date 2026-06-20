---
description: Fisher information loss ratio of k-QSketch registers vs full ExpSketch registers across lambda and k values
---

# Idea eksperymentu

## Cel
Pokazać, ile informacji Fishera traci k-QSketch względem ExpSketch w zależności od λ i k. Współczynnik ρ = I_X(λ)/I_Z(λ,k) mówi, ile razy więcej rejestrów potrzebuje k-QSketch by osiągnąć tę samą wariancję.

## Co pokazuje wykres
Krzywe ρ(λ, k) dla kilku wartości k (1.5, 2, 3, 4, 5, 8) na osi X w skali logarytmicznej (λ od 0.01 do 10000).

## Oczekiwany wniosek
ρ ≥ 1 zawsze; dla większego k współczynnik jest bliższy 1 (mniejsza utrata informacji). Zależność od λ jest słaba (lekka oscylacja lub plateau), co sugeruje, że ρ jest niemal stałe.

# Output

## Ile subplotów
1

## Rozkład subplotów (rzędy x kolumny)
1 x 1

## Osie
- OX: λ (log-scale, 0.01–10000)
- OY: ρ(λ, k) — Fisher information loss ratio

## Legenda
Jedna krzywa na wartość k; legenda po prawej.

# Idea eksperymentu

## Cel
Demonstrate that RNG engine choice has no material effect on FastExpSketch performance or accuracy. Measures both mean addition time and mean relative error across the four supported RNG engines (PCG64, MT19937, XOSHIRO128PP, XOSHIRO256PP). Results are presented as representative of all Fisher-Yates-based sketches.

## Co pokazuje wykres
One figure with 2 subplots. Left: mean addition time (μs/element) vs m for 4 RNG engines. Right: mean relative error vs m for 4 RNG engines.

## Oczekiwany wniosek
All four RNG engines produce essentially identical timing and accuracy curves, confirming that FastExpSketch — and by extension all Fisher-Yates-based sketches — is indifferent to RNG engine choice.

# Output

## Ile subplotów
2

## Rozkład subplotów (rzędy x kolumny)
1 x 2

## Osie
- OX: m (sketch size)
- OY left: mean addition time (μs per element)
- OY right: mean relative error

## Legenda
4 lines per subplot: PCG64, MT19937, XOSHIRO128PP, XOSHIRO256PP (shown in left subplot).

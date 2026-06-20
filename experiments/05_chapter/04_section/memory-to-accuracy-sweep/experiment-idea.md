# Idea eksperymentu

## Cel
Porównanie dokładności (RSE) pięciu szkiców ważonej kardynalności przy ustalonym
budżecie pamięci. Dla każdego budżetu bajtów (512–4096) dobieramy największe `m`
mieszczące się w budżecie i mierzymy RSE. Pokazuje, który szkic najlepiej
wykorzystuje pamięć: kwantyzowane szkice (QSketch, kQSketch, LogExpSketch)
upakowują więcej rejestrów w tej samej pamięci niż FastExpSketchFloat32.

## Co pokazuje wykres
- OŚ X: całkowita pamięć szkicu (bajty), od 512 do 4096
- OŚ Y: RSE (relative standard error)
Każda linia to jeden szkic; dla danego budżetu pamięci większe `m` daje niższy RSE.

## Oczekiwany wniosek
Przy tym samym budżecie pamięci szkice kwantyzowane (zwłaszcza kQSketchShifted(b=6)
i QSketch(b=8)) osiągają niższy RSE niż FastExpSketchFloat32, ponieważ mieszczą
więcej rejestrów `m` w tej samej liczbie bajtów.

# Output

## Ile subplotów

1

## Rozkład subplotów (rzędy x kolumny)

1x1

## Osie

- OX: Total memory (bytes), liniowa
- OY: RSE, liniowa

## Legenda

Pięć linii: FastExpSketchFloat32, QSketch(b=8), kQSketchShifted(b=6),
kQSketchRounding(b=8), LogExpSketch(b=11,e=8).

# Idea eksperymentu

## Cel
Wziecie różnych szkiców expsketch - float16, float32, float64 i dla tych szkicow sprawdzenie jak dzialaja gdy suma wag w strumieniu zbliza sie do zakresu floata. Szkice powinny miec relatywnie male m ~ 150(+/- 100)

## Co pokazuje wykres
Dwa wykresy
- Jeden wykres pokazuje zakresy floatow
- Drugi wykres posiada blad wzgledny estymacji, gdy na osi OX jest sumaryczna waga strumienia od 10^-300 do 10^300. Os OX jest zlogarytmizowana, ale jako ze matplotlib nie da rady z 10^-300 to na osi OX dajemy po prostu wartosci od -300 do 300. Os OY ograinczona 0 do 1

## Oczekiwany wniosek
Powinno byc widac ze blad wzgledny sie w sumie nie zmienia w zaleznosci od rodzaju zmiennej, jedyne co sie zmienia to zakres rozwiazywanego problemu. Czyli float64 jest w stanie caly zakres prawie, a float32 i float16 wczesniej wyskakuje w nieskonczonosc.

# Output

## Ile subplotów

TODO

## Rozkład subplotów (rzędy x kolumny)

TODO

## Osie

TODO

## Legenda

TODO

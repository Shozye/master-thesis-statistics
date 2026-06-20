# Idea eksperymentu

## Cel
Zbadanie jak ExpSketch wykorzystuje zakres rejestru dla formatu custom float z q=5, p=5.

jednego wykresu ktory ma w sobie histogramy
jeden jest dla szkicu ktory ma w rejestrze dodana pojedyncza wartosc o wadze 1

Wygenerowanie histogramu wszystkich teoretycznie możliwych wartości w rejestrze 

jeden histogram ma dodany jeden element o wadze 2^0
drugi histogram ma dodany jeden element o wadze 2^5
trzeci istogram ma dodany jeden element o wadze 2^-5
na osi OX znajduje sie kazda mozliwa wartosc dostepna w tym custom float q=5,p=5
powinien to byc histogram czyli kazdy mozliwa wartosc ma tyle samo miejsca.
waga powinna byc oznaczona symbolem duzej lambdy


## Co pokazuje wykres
Histogram częstości występowania poszczególnych wartości w rejestrach.
Oś X: możliwe wartości rejestru, Oś Y: liczba rejestrów z daną wartością.
na wykresie powinien sie rowniez znajdowac Float(s=0,p=5,q=5) MIN oraz MAX jako pionowe kreski

## Oczekiwany wniosek
Zobaczymy jak ExpSketch rozkłada wartości po rejestrach i jak dobrze (lub źle) wykorzystuje dostępny zakres custom float.

# Output

## Ile subplotów

TODO

## Rozkład subplotów (rzędy x kolumny)

TODO

## Osie

TODO

## Legenda

TODO

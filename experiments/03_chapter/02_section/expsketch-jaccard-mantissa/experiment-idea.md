# Idea eksperymentu

## Cel
Zbadanie tego jak parametry $q$ i $p$ wplywaja na Jaccard Similarity 
Zbadanie tego, od jakiego $p$ błąd względny Jaccard Similarity sie nie rozni od teoretycznego minimum
Sprawdzenie tego dla roznych wartosci $q$


Zbadanie czy estymacja Jaccard similarity jest bardziej wrażliwa na redukcję mantysy niż estymacja kardynalności. 
sweep p od 1 do 9.
ExpSketchCustomFloat q=11
m=100

Dla kazdego $p$ powinnismy zrobic eksperymenty ze strumieniami ktore maja jaccard similarity takie jakie jest
Czyli majac podane $p$ i $q$ i $J$ wyobrazam sobie ze tworzymy 
N_TRIALS par ExpSketchy. Na kaźdy trial inna ilość seedów. 
W każdym trialu tworzymy 3 strumienie: A_ONLY, B_ONLY, COMMON
tak by A_ONLY + COMMON mialo Jaccard similarity $J$ gdy porownamy z B_ONLY + COMMON
A_ONLY jest rozlaczone do B_ONLY

uzywaj add_many, sprobuj to jakos przyspieszyc.
Dobrym sposobem przyspieszenia moze byc uzycie "clone_with(p,q)" Jako ze:
Stworzenie szkicu z p = stworzenie szkicu z duzym p i obciecie do p
podobnie obciecie z q


## Co pokazuje wykres
Wyobrazam sobie wykres z 3 subplotami 1 rzad 3 kolumy
w pierwszym jest q=5
q drugim q=7
w trzecim q=9
Na kazdym z wykresów mamy 4 eksperymenty - dla J= 0.2, J=0.5, J=0.80, J=0.95, J=0.97
Posiadamy tez 4 dashed kreski oznaczajace teoretyczne RSE minimum dla danego $J$

Punkt (x, y) oznacza że dla bitów mantysy $p$ mielismy RSE y

## Oczekiwany wniosek
Spodziewamy sie ze jak bity mantysy $p$ zaczynaja byc wieksze niz 5 to wynik sie stabilizuje do teoretycznego minimum
nie wiem jak $q$ na to wplywa
# Output

## Ile subplotów

TODO

## Rozkład subplotów (rzędy x kolumny)

TODO

## Osie

TODO

## Legenda

TODO

# Idea eksperymentu

## Cel
Pokazanie ile bitów na rejestr $b$ potrzebuje LogExpSketch, aby obsłużyć zakres
$\mathrm{Float32}$ (czyli $v_{\max} = \mathrm{float32\_max}$, $v_{\min} = 1/v_{\max}$).
Badamy zarówno estymator kardynalności ważonej, jak i estymator Jaccard Similarity.

Dla kardynalności: dla różnych wartości $\Lambda$ (jeden ważony element o wadze
$\Lambda$, więc rejestry są rozkładu wykładniczego o rzędzie $\Lambda$) mierzymy RSE
estymatora. Przy $m=400$ teoretyczne RSE to ok. $0.05$. Porównujemy
FastExpSketchFloat32 (linia odniesienia) z LogExpSketchFastNoShifted dla $b=9,10,11$.

Dla Jaccarda: tworzymy pary strumieni o zadanym Jaccardzie $J$ i mierzymy RSE
estymatora `jaccard_struct` dla $b=9..14$. Im więcej bitów, tym drobniejsza siatka
i mniej przypadkowych kolizji, więc RSE zbiega do teoretycznego minimum.

## Co pokazuje wykres
Panel (a): RSE estymatora kardynalności w funkcji $\log_{10}\Lambda$ od $-35$ do $35$.
Pokazuje od jakiego $b$ LogExpSketch jest nieodróżnialny od ExpSketch na całym
zakresie Float32 (oś OY ograniczona do $[0.02, 0.3]$).

Panel (b): RSE estymatora Jaccarda w funkcji liczby bitów $b \in \{9,..,14\}$ dla
$J \in \{0.2, 0.5, 0.8, 0.9, 0.95\}$, wraz z poziomymi liniami teoretycznego RSE
liczonego tym samym wzorem co dla ExpSketch: $\sqrt{(1-J)/(mJ)}$.

## Oczekiwany wniosek
Spodziewamy się, że $b=11$ wystarcza, by LogExpSketch był nieodróżnialny od
ExpSketch na zakresie Float32 (panel a), a estymator Jaccarda osiąga teoretyczne
minimum od tego samego $b$ (panel b). Dla $b=9,10$ widać obciążenie na krańcach
zakresu.

# Output

## Ile subplotów
2

## Rozkład subplotów (rzędy x kolumny)
1 x 2

## Osie
Panel (a): OX = $\log_{10}\Lambda$ ($-35$ do $35$), OY = RSE (ograniczone do $[0.02, 0.3]$).
Panel (b): OX = liczba bitów $b$ ($9..14$), OY = RSE.

## Legenda
Panel (a): FastExpSketchFloat32 oraz LogExpSketch dla $b=9,10,11$.
Panel (b): krzywe dla $J=0.2,0.5,0.8,0.9,0.95$ i odpowiadające im teoretyczne linie przerywane.

# Idea eksperymentu

## Cel
Pokazanie, że wariant Shifted \LogExpSketch{} pozwala drastycznie zmniejszyć
liczbę bitów na rejestr $b$ względem wariantu bez przesunięcia. Dzięki globalnemu
offsetowi okno przesuwa się swobodnie (offset może być ujemny), więc $v_{\max}$
nie jest już bezwzględnym zakresem, lecz tylko *względną* szerokością okna —
musi przekroczyć jedynie rozrzut $m$ minimów rejestrów, a nie cały zakres
$\mathrm{Float32}$. Ponieważ offset pochłania skalę, siatka przy ustalonym $b$
jest dość gęsta, by $b=10$ osiągało optimum (zamiast $b=14$ potrzebnego w
wariancie bez przesunięcia).

Wybieramy $v_{\max} = 10^{9}$. Względny rozrzut $m$ minimów wykładniczych ma ciężki
ogon górny: dla $m=400$ w rzadkich powtórzeniach sięga $10^{6}$–$10^{7}$. Wartość
$v_{\max}=10^{9}$ przekracza ten ogon z zapasem, więc nie pojawia się obcięcie
(clamping) ani obciążenie, a jednocześnie siatka pozostaje wystarczająco gęsta
dla $b=10$. (Zweryfikowane: RSE kardynalności 0.0515 wobec teoretycznego progu
0.0510, RSE Jaccarda na poziomie $\sqrt{(1-J)/(mJ)}$ dla wszystkich $J$ od $b=10$.)

Dla kardynalności: dla różnych $\Lambda$ (jeden ważony element) mierzymy RSE.
Offset czyni estymator niezależnym od skali, więc krzywa jest płaska na całym
zakresie $\log_{10}\Lambda$.

Dla Jaccarda: tworzymy pary strumieni o zadanym $J$ i mierzymy RSE estymatora
`jaccard_struct` dla $b=8..11$.

## Co pokazuje wykres
Panel (a): RSE estymatora kardynalności w funkcji $\log_{10}\Lambda$ od $-35$ do
$35$ dla FastExpSketchFloat32 (odniesienie) i Shifted LogExpSketch dla
$b=8,9,10,11$. Pokazuje, że dzięki offsetowi wariant Shifted jest płaski na całym
zakresie.

Panel (b): RSE estymatora Jaccarda w funkcji liczby bitów $b \in \{8,..,11\}$ dla
$J \in \{0.2, 0.5, 0.8, 0.9, 0.95\}$, wraz z poziomymi liniami teoretycznego RSE
$\sqrt{(1-J)/(mJ)}$.

## Oczekiwany wniosek
Spodziewamy się, że przy $v_{\max}=10^{9}$ wariant Shifted osiąga teoretyczne
minimum estymatora Jaccarda już od $b=10$, a estymator kardynalności jest
nieobciążony na całym zakresie skal. Dla $b=8,9$ widać niewielką degradację
(zwłaszcza przy małym $J$). To pokazuje optymalizację względem wariantu bez
przesunięcia, który potrzebował $b=14$.

# Output

## Ile subplotów
2

## Rozkład subplotów (rzędy x kolumny)
1 x 2

## Osie
Panel (a): OX = $\log_{10}\Lambda$ ($-35$ do $35$), OY = RSE.
Panel (b): OX = liczba bitów $b$ ($8..11$), OY = RSE.

## Legenda
Panel (a): FastExpSketchFloat32 oraz Shifted LogExpSketch dla $b=8,9,10,11$.
Panel (b): krzywe dla $J=0.2,0.5,0.8,0.9,0.95$ i odpowiadające im teoretyczne linie przerywane.

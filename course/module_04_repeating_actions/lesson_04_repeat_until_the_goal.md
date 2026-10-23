# Lekcja 4.4: Powtarzanie aż do osiągnięcia celu

**Polski** · [English](lesson_04_repeat_until_the_goal.en.md) · [Opis kursu](../../README.md)

> **Moduł 4, lekcja 4** · około 70–85 minut
> **Potrzebujesz:** katalogu `cpp-workspace` i oryginalnego projektu `lesson_05_first_program`, jak dotąd. Debugger nie jest w tej lekcji potrzebny.
> **Wersja pilotażowa.** Programy z tej lekcji sprawdzamy automatycznie na Windowsie, Ubuntu i macOS, także z podanymi danymi wejściowymi.

## Zanim zaczniesz

Ta lekcja zakłada, że po lekcjach 4.1–4.3:

- piszesz pętle `while` i `for` i śledzisz je w tabeli, w której ostatnie sprawdzenie warunku daje `false` i nie jest przebiegiem;
- wiesz, że pętla może wykonać się zero razy;
- gromadzisz wynik w akumulatorze przez `+=` i zwiększasz licznik przez `++`;
- sprawdzasz dane przez `if`, zanim program zacznie liczyć (lekcja 3.5).

## Sytuacja

W lekcjach 4.1–4.3 o liczbie powtórzeń decydował licznik: „wypisz 3 okrążenia”, „zsumuj liczby do N”, „rozpisz 5 rund”. Często jednak myślimy inaczej: **„powtarzaj, aż osiągniesz cel”**. Odkładaj pieniądze, aż uzbierasz potrzebną kwotę. Czytaj, aż przeczytasz zaplanowaną liczbę stron.

Program nie potrzebuje wtedy zaplanowanej liczby powtórzeń. Po każdym przebiegu sprawdza, **jak daleko jest od celu**, i na tej podstawie decyduje, czy powtarzać dalej. Do tego służy `while`, który już znasz. Dziś jego warunek będzie zależał od zmieniającego się stanu, a nie od licznika.

Po tej lekcji będziesz:

- odróżniać pętlę sterowaną licznikiem od pętli sterowanej osiągnięciem celu;
- wskazywać stan, od którego zależy warunek pętli, i zapisywać warunek „powtarzaj, dopóki cel nie jest osiągnięty”;
- wyjaśniać, dlaczego pętla się kończy, i sprawdzać dane, zanim pętla się zacznie;
- odróżniać dokładne osiągnięcie celu od jego przekroczenia i znajdować błąd jednego przebiegu za dużo;
- rozpoznawać, bez uruchamiania, pętlę, która nie robi postępu;
- pisać pętlę, w której krok zmienia się z przebiegu na przebieg.

## 1. Przygotuj projekt

W `cpp-workspace` utwórz katalog `lesson_4_4` i skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program`. Programy z punktów 2–9 wpisujesz w `main.cpp` tego katalogu.

## 2. Oszczędzanie na cel

Ktoś chce uzbierać określoną kwotę, wpłacając za każdym razem tyle samo pełnych złotych. Program zna cel i kwotę jednej wpłaty. Powtarza wpłaty, **dopóki zebrana suma jest mniejsza od celu**. Cel może wynosić od 0 do 500 zł, a wpłata od 25 do 100 zł. Zakładamy, że użytkownik wpisuje liczby całkowite.

<!-- example: savings -->
```cpp
#include <iostream>

int main() {
    int goal{0};
    int payment{0};

    std::cout << "Enter goal in zl (0-500):\n";
    std::cin >> goal;
    std::cout << "Enter payment in zl (25-100):\n";
    std::cin >> payment;

    const bool goal_ok{goal >= 0 && goal <= 500};
    const bool payment_ok{payment >= 25 && payment <= 100};

    if (goal_ok && payment_ok) {
        int saved{0};
        int payment_count{0};

        while (saved < goal) {
            saved += payment;
            ++payment_count;
            std::cout << "Payment " << payment_count << ": saved " << saved << " zl\n";
        }

        std::cout << "Payments: " << payment_count << "\n";
        std::cout << "Saved: " << saved << " zl\n";
    } else {
        std::cout << "Invalid savings data\n";
    }
}
```

- `goal` to **cel**: kwota, którą chcemy zebrać. W pętli się nie zmienia.
- `payment` to **krok**: o tyle rośnie suma w jednym przebiegu.
- `saved` to **postęp**: ile zebrano do tej chwili. To akumulator z lekcji 4.2.
- `payment_count` liczy wykonane wpłaty.
- Warunek `saved < goal` zależy od **zebranej sumy**, a nie od licznika wpłat. Licznik tylko zapisuje, ile było wpłat. Nie decyduje, kiedy skończyć.
- Po każdej wpłacie `saved` rośnie. Gdy suma osiągnie cel albo go przekroczy, warunek daje `false` i pętla się kończy.

W tym przykładzie liczbę wpłat dałoby się obliczyć z góry. Nie o to jednak chodzi. Program **sam** decyduje o powtarzaniu, na podstawie aktualnego postępu, i nigdzie nie zapisuje zaplanowanej liczby przebiegów.

**Przewidź** dla celu 100 zł i wpłat po 30 zł: ile będzie wpłat, jak będzie rosła suma, czy ostatnia wpłata trafi dokładnie w cel i ile wyniesie końcowa kwota? Zapisz odpowiedzi, a potem uruchom program.

<!-- input: savings -->
```text
100
30
```

<details>
<summary>Standardowe wyjście dla 100 i 30</summary>

<!-- output: savings -->
```text
Enter goal in zl (0-500):
Enter payment in zl (25-100):
Payment 1: saved 30 zl
Payment 2: saved 60 zl
Payment 3: saved 90 zl
Payment 4: saved 120 zl
Payments: 4
Saved: 120 zl
```

</details>

## 3. Tabela postępu

Tabela dla celu 100 zł i wpłat po 30 zł:

| Sprawdzenie warunku | `saved` przy sprawdzeniu | `saved < goal` | Wpłata w ciele | `saved` po wpłacie | `payment_count` po wpłacie |
|---|---|---|---|---|---|
| 1 | 0 | `true` | 30 | 30 | 1 |
| 2 | 30 | `true` | 30 | 60 | 2 |
| 3 | 60 | `true` | 30 | 90 | 3 |
| 4 | 90 | `true` | 30 | 120 | 4 |
| 5 | 120 | `false` | **brak**: pętla się kończy | — | — |

- Warunek sprawdzono **5 razy**, a wpłat było **4**. Piąte sprawdzenie daje `false` i nie jest przebiegiem.
- Przy 90 zł brakuje jeszcze 10 zł, więc program wykonuje kolejną, **pełną** wpłatę. Suma przekracza cel o 20 zł. To w porządku: wpłacamy zawsze tę samą kwotę, a program nie oblicza wpłaty częściowej. To ćwiczenie z powtarzania do spełnienia warunku, a nie system bankowy.

## 4. Cel, postęp i krok

| Pojęcie | Co to jest | W przykładzie |
|---|---|---|
| **cel** | stan, który chcemy osiągnąć | `goal` |
| **postęp** | wartość, która zmienia się w kolejnych przebiegach i jest porównywana z celem | `saved` |
| **krok** | o ile zmienia się postęp w jednym przebiegu | `payment` |

To nie są nowe typy C++, tylko nazwy, które pomagają zrozumieć pętlę. W tym przykładzie krok jest **stały**: każda wpłata jest taka sama. W misji na końcu lekcji krok będzie się zmieniał. W obu przypadkach pętla kończy się po osiągnięciu celu.

## 5. Dokładnie w cel

Teraz cel to 100 zł, a wpłata to 25 zł. **Przewidź**: ile będzie wpłat i ile wyniesie suma? Czy po wpłacie, która da dokładnie 100 zł, potrzebna jest jeszcze jedna?

<!-- input: savings -->
```text
100
25
```

<details>
<summary>Standardowe wyjście dla 100 i 25 oraz wyjaśnienie</summary>

<!-- output: savings -->
```text
Enter goal in zl (0-500):
Enter payment in zl (25-100):
Payment 1: saved 25 zl
Payment 2: saved 50 zl
Payment 3: saved 75 zl
Payment 4: saved 100 zl
Payments: 4
Saved: 100 zl
```

Po czwartej wpłacie suma wynosi dokładnie 100 zł. Piąte sprawdzenie, `100 < 100`, daje `false`, więc pętla się kończy. **Osiągnięty cel nie wymaga dodatkowej wpłaty.**

</details>

Warunek `saved < goal` pyta: **czy jeszcze czegoś brakuje?** Gdy suma równa się celowi, niczego nie brakuje i program przestaje wpłacać. Warunek, który dawałby `true` także przy równej sumie, prowadziłby do wpłaty, której nikt nie potrzebuje. Taki błąd znajdziesz w punkcie 9.

## 6. Zero, jeden i wiele przebiegów

**Przewidź.** Przepisz tabelę i wypełnij ją, zanim uruchomisz program.

| Cel | Wpłata | Liczba wpłat | Końcowa suma |
|---|---|---|---|
| 0 | 25 | | |
| 25 | 25 | | |
| 500 | 25 | | |

Potem uruchom program trzy razy.

<!-- input: savings -->
```text
0
25
```

<details>
<summary>Standardowe wyjście dla 0 i 25</summary>

<!-- output: savings -->
```text
Enter goal in zl (0-500):
Enter payment in zl (25-100):
Payments: 0
Saved: 0 zl
```

`saved` zaczyna od 0, a warunek `0 < 0` jest fałszywy już przy pierwszym sprawdzeniu. Nie trzeba niczego wpłacać: cel 0 zł jest osiągnięty od początku. Ciało pętli nie wykonuje się ani razu, `payment_count` zostaje równe 0, a podsumowanie za pętlą i tak się wypisuje. To poprawne zachowanie, a nie błąd danych: cel 0 mieści się w dopuszczalnym zakresie.

</details>

<!-- input: savings -->
```text
25
25
```

<details>
<summary>Standardowe wyjście dla 25 i 25</summary>

<!-- output: savings -->
```text
Enter goal in zl (0-500):
Enter payment in zl (25-100):
Payment 1: saved 25 zl
Payments: 1
Saved: 25 zl
```

</details>

<!-- input: savings -->
```text
500
25
```

<details>
<summary>Standardowe wyjście dla 500 i 25</summary>

<!-- output: savings -->
```text
Enter goal in zl (0-500):
Enter payment in zl (25-100):
Payment 1: saved 25 zl
Payment 2: saved 50 zl
Payment 3: saved 75 zl
Payment 4: saved 100 zl
Payment 5: saved 125 zl
Payment 6: saved 150 zl
Payment 7: saved 175 zl
Payment 8: saved 200 zl
Payment 9: saved 225 zl
Payment 10: saved 250 zl
Payment 11: saved 275 zl
Payment 12: saved 300 zl
Payment 13: saved 325 zl
Payment 14: saved 350 zl
Payment 15: saved 375 zl
Payment 16: saved 400 zl
Payment 17: saved 425 zl
Payment 18: saved 450 zl
Payment 19: saved 475 zl
Payment 20: saved 500 zl
Payments: 20
Saved: 500 zl
```

Największy cel i najmniejsza wpłata dają najwięcej przebiegów: 20.

</details>

## 7. Sprawdzenie danych przed pętlą

Program sprawdza oba zakresy, **zanim** wejdzie do pętli. Dla danych spoza zakresu wypisuje tylko `Invalid savings data` i kończy się normalnie, bez żadnej wpłaty.

**Przewidź**, co wypisze program dla wpłaty 0 zł i celu 100 zł, a potem sprawdź ten i pozostałe przypadki.

<!-- input: savings -->
```text
100
0
```

<details>
<summary>Standardowe wyjście dla 100 i 0 oraz dla pozostałych danych spoza zakresu</summary>

<!-- output: savings -->
```text
Enter goal in zl (0-500):
Enter payment in zl (25-100):
Invalid savings data
```

Tak samo kończą się wpłata 24 zł (tuż pod zakresem) i 101 zł (tuż nad nim) oraz cel -1 zł i 501 zł:

<!-- input: savings -->
```text
100
24
```

<!-- output: savings -->
```text
Enter goal in zl (0-500):
Enter payment in zl (25-100):
Invalid savings data
```

<!-- input: savings -->
```text
100
101
```

<!-- output: savings -->
```text
Enter goal in zl (0-500):
Enter payment in zl (25-100):
Invalid savings data
```

<!-- input: savings -->
```text
-1
50
```

<!-- output: savings -->
```text
Enter goal in zl (0-500):
Enter payment in zl (25-100):
Invalid savings data
```

<!-- input: savings -->
```text
501
50
```

<!-- output: savings -->
```text
Enter goal in zl (0-500):
Enter payment in zl (25-100):
Invalid savings data
```

</details>

**Dlaczego przed pętlą?** Sprawdzenie chroni samą pętlę:

- wpłata 0 zł nie zmienia sumy, więc `saved < goal` przy dodatnim celu dawałoby `true` bez końca;
- wpłata ujemna **oddala** sumę od dodatniego celu;
- w obu przypadkach warunek końca nigdy nie stałby się fałszywy.

Sprawdzenie w pętli byłoby za późno: zła wpłata już by się wykonała. W tej lekcji złe dane kończą program komunikatem. Ponowne pytanie o dane poznasz w następnej lekcji.

## 8. Co gwarantuje zakończenie?

Dla dopuszczalnych danych pętla zawsze się kończy, **bo suma rośnie w każdym przebiegu o co najmniej 25 zł, a cel nie przekracza 500 zł**. Po 20 wpłatach suma wynosi co najmniej 500 zł, więc warunek `saved < goal` musi stać się fałszywy najpóźniej wtedy. Nie trzeba tego formalnie dowodzić, ale warto umieć odpowiedzieć na cztery pytania:

1. Czy każdy przebieg przybliża program do celu?
2. Czy cel może przez cały czas pozostawać poza zasięgiem?
3. Co musi się zmienić, żeby warunek stał się fałszywy?
4. Dlaczego potrzebujemy ograniczeń danych?

Przykładowe odpowiedzi są w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

Zakres od 0 do 500 zł nie jest ograniczeniem typu `int`, tylko **wymaganiem tego zadania**. Dzięki niemu pętla ma najwyżej 20 przebiegów, więc wynik jest krótki i łatwy do sprawdzenia.

## 9. Znajdź błąd: jedna wpłata za dużo

Wymaganie jest takie jak w punkcie 2: program wpłaca, **dopóki suma jest mniejsza od celu**. W tej wersji ktoś zmienił warunek pętli:

<!-- example: savings_bug -->
```cpp
#include <iostream>

int main() {
    int goal{0};
    int payment{0};

    std::cout << "Enter goal in zl (0-500):\n";
    std::cin >> goal;
    std::cout << "Enter payment in zl (25-100):\n";
    std::cin >> payment;

    const bool goal_ok{goal >= 0 && goal <= 500};
    const bool payment_ok{payment >= 25 && payment <= 100};

    if (goal_ok && payment_ok) {
        int saved{0};
        int payment_count{0};

        while (saved <= goal) {
            saved += payment;
            ++payment_count;
            std::cout << "Payment " << payment_count << ": saved " << saved << " zl\n";
        }

        std::cout << "Payments: " << payment_count << "\n";
        std::cout << "Saved: " << saved << " zl\n";
    } else {
        std::cout << "Invalid savings data\n";
    }
}
```

1. Przeczytaj wymaganie i zapisz, ile wpłat i jaką sumę **powinien** dać program dla trzech par: cel 0 i wpłata 25, cel 100 i wpłata 25, cel 100 i wpłata 30.
2. Przewidź, co wypisze **ten** program. Pomoże Ci tabela przebiegu dla celu 0.
3. Uruchom program dla tych trzech par.
4. Znajdź pierwszy przypadek, w którym wynik nie zgadza się z wymaganiem.
5. Popraw warunek.
6. Sprawdź ponownie wszystkie trzy przypadki.

Wyniki przed poprawką i poprawka są w części [Przykładowe rozwiązania](#przykładowe-rozwiązania). Zajrzyj tam po własnej próbie.

## 10. Pętla, która nie robi postępu

Ten fragment **przeanalizuj na papierze, nie uruchamiaj go**. Ktoś pomylił zmienne i w ciele zwiększa cel zamiast sumy:

<!-- fragment -->
```cpp
int saved{0};
int payment_count{0};

while (saved < goal) {
    goal += payment;
    ++payment_count;
    std::cout << "Payment " << payment_count << ": saved " << saved << " zl\n";
}
```

Dla celu 100 zł i wpłat po 30 zł:

| Sprawdzenie warunku | `saved` | `goal` | `saved < goal` | Po ciele: `goal` | Po ciele: `payment_count` |
|---|---|---|---|---|---|
| 1 | 0 | 100 | `true` | 130 | 1 |
| 2 | 0 | 130 | `true` | 160 | 2 |
| 3 | 0 | 160 | `true` | 190 | 3 |
| … | 0 | … | `true` | rośnie dalej | rośnie dalej |

W pętli coś się zmienia, i to w każdym przebiegu: rośnie `goal`, rośnie `payment_count`. Warunek porównuje jednak `saved` z `goal`, a `saved` stoi w miejscu, podczas gdy cel ucieka. Odpowiedź „nie” nigdy nie nadejdzie, a program wypisywałby kolejne linijki bez końca.

**Nie wystarczy, że w pętli coś się zmienia. Musi zmieniać się to, co rzeczywiście prowadzi do zakończenia powtarzania:** tu postęp `saved`, w stronę celu.

Gdyby taka pętla uruchomiła się przez pomyłkę, przerwij program, jak w lekcji 4.1: <kbd>Ctrl</kbd> + <kbd>C</kbd> w terminalu albo przycisk **Stop** w CLionie.

## 11. Misja: cel czytelniczy

Program symuluje plan czytania. Użytkownik podaje cel, czyli łączną liczbę stron do przeczytania, i liczbę stron na pierwszy dzień. W tej uproszczonej symulacji każdego kolejnego dnia czyta się **dwa razy więcej** stron niż poprzedniego. Program symuluje kolejne dni, aż łączna liczba przeczytanych stron osiągnie cel albo go przekroczy. To prosty model do ćwiczenia, a nie porada, jak czytać.

**Wymagania:**

- Cel to liczba całkowita od 0 do 100 stron.
- Liczba stron na pierwszy dzień to liczba całkowita od 1 do 10.
- Program pyta o obie wartości, w tej kolejności: `Enter page goal (0-100):` i `Enter pages for day 1 (1-10):`.
- Dla każdego dnia program wypisuje linijkę `Day D: read P, total T`, czyli numer dnia, liczbę stron przeczytanych tego dnia i łączną liczbę przeczytanych stron.
- Po ostatnim dniu wypisuje `Days: D` i `Total pages: T`.
- Dla celu 0 program nie symuluje żadnego dnia.
- Jeśli którakolwiek wartość jest spoza zakresu, program wypisuje tylko `Invalid reading data`. Nie pyta ponownie o dane.
- Zakładamy, że użytkownik wpisuje liczby całkowite.

W `cpp-workspace` utwórz katalog `reading_goal`, skopiuj do niego `CMakeLists.txt` z oryginalnego `lesson_05_first_program`, utwórz pusty `main.cpp` i napisz program samodzielnie.

Dla celu 20 stron i 3 stron pierwszego dnia standardowe wyjście ma być takie:

<!-- input: reading_goal -->
```text
20
3
```

<!-- output: reading_goal -->
```text
Enter page goal (0-100):
Enter pages for day 1 (1-10):
Day 1: read 3, total 3
Day 2: read 6, total 9
Day 3: read 12, total 21
Days: 3
Total pages: 21
```

**To nie jest program z oszczędzaniem z nowymi nazwami.** Tam krok był stały: każda wpłata była taka sama. Tutaj **krok zmienia się po każdym przebiegu**: liczba stron w danym dniu jest dwa razy większa niż poprzedniego. Liczba dni wynika z osiąganego postępu. Musisz samodzielnie zdecydować:

1. która zmienna przechowuje łączny postęp, a która liczbę stron na bieżący dzień;
2. jaką wartość początkową ma licznik dni i co sprawdza warunek `while`;
3. w jakiej kolejności w jednym przebiegu: dodać strony dnia do sumy, wypisać linijkę dnia i podwoić liczbę stron na następny dzień;
4. jak uniknąć dodatkowego dnia po osiągnięciu celu i co program robi dla celu 0.

Do podwojenia wystarczy znane mnożenie (lekcja 2.4). Żaden nowy operator nie jest potrzebny.

**Zanim napiszesz program**, przygotuj dwie rzeczy:

- tabelę przebiegu dla celu 20 i 3 stron: numer dnia, strony tego dnia, suma po tym dniu i strony na następny dzień;
- tabelę przypadków testowych: cel 0, cel osiągnięty po jednym dniu, cel osiągnięty dokładnie, cel przekroczony, największy cel z najmniejszym startem i wartości tuż poza zakresem obu danych. Przy każdym przypadku zapisz oczekiwane standardowe wyjście.

### Kryterium sukcesu

- Program buduje się jako C++20, a jego standardowe wyjście dla celu 20 i 3 stron jest dokładnie takie jak powyżej.
- Dla każdej dopuszczalnej pary danych program wypisuje właściwe dni i kończy po pierwszym dniu, w którym suma osiągnęła cel albo go przekroczyła. Dla danych spoza zakresu wypisuje tylko `Invalid reading data`.
- Powtarzaniem steruje pętla `while`, której warunek porównuje postęp z celem.
- Łączna liczba stron jest gromadzona w akumulatorze, a liczba stron na dzień podwaja się po każdym dniu.
- Zakres obu wartości jest sprawdzany, zanim program zacznie symulować dni.
- Tabela przebiegu i tabela przypadków powstały przed uruchomieniem programu.
- Umiesz wyjaśnić, dlaczego pętla się kończy i dlaczego dla celu 0 nie ma żadnego dnia.

Gdy wynik się zgadza, możesz zapisać projekt w Gicie, jak w lekcji 1.5.

<details>
<summary>Podpowiedź 1</summary>

Rozpisz trzy pojęcia z punktu 4 dla tej misji: co jest celem, co jest postępem, a co krokiem? Które z nich zmieniają się z dnia na dzień i jak?

</details>

<details>
<summary>Podpowiedź 2</summary>

Linijka dnia ma pokazać strony **tego** dnia i sumę **po** tym dniu. Co musi się więc stać przed wypisaniem, a co dopiero po nim, żeby następny dzień dostał podwojoną liczbę stron?

</details>

<details>
<summary>Podpowiedź 3</summary>

Warunek `while` odpowiada na pytanie: czy łącznie przeczytano jeszcze mniej, niż wynosi cel? Sprawdź go w tabeli przebiegu dla celu 3 i 1 strony: po ilu dniach powinien dać `false`?

</details>

<details>
<summary>Pełna lista przypadków kontrolnych: otwórz po przygotowaniu własnej tabeli</summary>

| Cel | Pierwszy dzień | Strony kolejnych dni | Dni | Strony łącznie | Co sprawdza |
|---|---|---|---|---|---|
| 20 | 3 | 3, 6, 12 | 3 | 21 | cel przekroczony ostatnim dniem |
| 0 | 3 | — | 0 | 0 | zero przebiegów |
| 1 | 1 | 1 | 1 | 1 | jeden dzień, cel osiągnięty dokładnie |
| 3 | 1 | 1, 2 | 2 | 3 | cel osiągnięty dokładnie po dwóch dniach |
| 10 | 2 | 2, 4, 8 | 3 | 14 | cel przekroczony |
| 10 | 10 | 10 | 1 | 10 | jeden dzień, cel osiągnięty dokładnie |
| 100 | 1 | 1, 2, 4, 8, 16, 32, 64 | 7 | 127 | największy cel i najmniejszy start: najwięcej dni |
| -1 | 3 | — | — | — | cel tuż pod zakresem |
| 101 | 3 | — | — | — | cel tuż nad zakresem |
| 20 | 0 | — | — | — | pierwszy dzień tuż pod zakresem |
| 20 | 11 | — | — | — | pierwszy dzień tuż nad zakresem |

Przypadki z kreskami w kolumnie „Dni” kończą się linijką `Invalid reading data`. Przypadek z celem 20 i 3 stronami jest sprawdzony wyżej, przy treści misji.

<!-- input: reading_goal -->
```text
0
3
```

<!-- output: reading_goal -->
```text
Enter page goal (0-100):
Enter pages for day 1 (1-10):
Days: 0
Total pages: 0
```

<!-- input: reading_goal -->
```text
1
1
```

<!-- output: reading_goal -->
```text
Enter page goal (0-100):
Enter pages for day 1 (1-10):
Day 1: read 1, total 1
Days: 1
Total pages: 1
```

<!-- input: reading_goal -->
```text
3
1
```

<!-- output: reading_goal -->
```text
Enter page goal (0-100):
Enter pages for day 1 (1-10):
Day 1: read 1, total 1
Day 2: read 2, total 3
Days: 2
Total pages: 3
```

<!-- input: reading_goal -->
```text
10
2
```

<!-- output: reading_goal -->
```text
Enter page goal (0-100):
Enter pages for day 1 (1-10):
Day 1: read 2, total 2
Day 2: read 4, total 6
Day 3: read 8, total 14
Days: 3
Total pages: 14
```

<!-- input: reading_goal -->
```text
10
10
```

<!-- output: reading_goal -->
```text
Enter page goal (0-100):
Enter pages for day 1 (1-10):
Day 1: read 10, total 10
Days: 1
Total pages: 10
```

<!-- input: reading_goal -->
```text
100
1
```

<!-- output: reading_goal -->
```text
Enter page goal (0-100):
Enter pages for day 1 (1-10):
Day 1: read 1, total 1
Day 2: read 2, total 3
Day 3: read 4, total 7
Day 4: read 8, total 15
Day 5: read 16, total 31
Day 6: read 32, total 63
Day 7: read 64, total 127
Days: 7
Total pages: 127
```

<!-- input: reading_goal -->
```text
-1
3
```

<!-- output: reading_goal -->
```text
Enter page goal (0-100):
Enter pages for day 1 (1-10):
Invalid reading data
```

<!-- input: reading_goal -->
```text
101
3
```

<!-- output: reading_goal -->
```text
Enter page goal (0-100):
Enter pages for day 1 (1-10):
Invalid reading data
```

<!-- input: reading_goal -->
```text
20
0
```

<!-- output: reading_goal -->
```text
Enter page goal (0-100):
Enter pages for day 1 (1-10):
Invalid reading data
```

<!-- input: reading_goal -->
```text
20
11
```

<!-- output: reading_goal -->
```text
Enter page goal (0-100):
Enter pages for day 1 (1-10):
Invalid reading data
```

</details>

Przykładowe rozwiązanie jest w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 12. Gdy coś pójdzie inaczej

| Co widzisz | Co to znaczy | Co zrobić |
|---|---|---|
| Po osiągnięciu celu jest jeszcze jeden przebieg | Warunek daje `true` także wtedy, gdy postęp równa się celowi, na przykład `<=` zamiast `<`. | Sprawdź przypadek, w którym cel zostaje osiągnięty dokładnie (punkt 9). |
| Dla celu 0 pojawia się jeden przebieg | Ten sam błąd: warunek nie wyklucza równości. | Wstaw do warunku wartości początkowe i sprawdź, czy daje `false`. |
| Ta sama linijka albo rosnące liczby pojawiają się bez końca | Pętla nie robi postępu: zmienia się nie ta zmienna albo krok jest zerowy. | Przerwij program. W tabeli przebiegu sprawdź, czy zmienna z warunku zbliża się do celu (punkt 10). |
| Pierwszy dzień pokazuje podwojoną liczbę stron | Krok jest podwajany przed wypisaniem i dodaniem do sumy. | Ustal kolejność w ciele: najpierw bieżący dzień, potem przygotowanie następnego. |
| Suma jest za mała albo za duża | Do sumy trafia nie ta wartość albo akumulator jest zerowany w ciele. | Sprawdź w tabeli, czy suma po każdym dniu to suma stron wypisanych do tej chwili. |
| Dla błędnych danych program zaczyna przebiegi | Sprawdzenie zakresu stoi za pętlą albo w niej. | Sprawdź dane przez `if`, zanim program wejdzie do pętli. |

## 13. Wyjaśnij

Odpowiedz krótko, najlepiej na piśmie. Dopiero potem porównaj z przykładową odpowiedzią.

**1.** Czym różni się pętla sterowana licznikiem od pętli sterowanej osiągnięciem celu?

<details>
<summary>Przykładowa odpowiedź</summary>

W pętli z licznikiem warunek pyta, czy licznik doszedł do zaplanowanej liczby powtórzeń. W pętli do celu warunek pyta, czy postęp, na przykład zebrana suma, osiągnął już cel. Liczba przebiegów wynika wtedy z tego, jak szybko postęp rośnie.

</details>

**2.** Od której zmiennej zależy warunek w programie z oszczędzaniem i dlaczego nie od `payment_count`?

<details>
<summary>Przykładowa odpowiedź</summary>

Od `saved`, czyli od zebranej sumy. Cel dotyczy kwoty, a nie liczby wpłat. `payment_count` tylko zapisuje, ile było wpłat.

</details>

**3.** Dlaczego dla celu 0 nie ma żadnej wpłaty i dlaczego to poprawne?

<details>
<summary>Przykładowa odpowiedź</summary>

Bo `saved` zaczyna od 0, a warunek `0 < 0` jest fałszywy od razu. Cel 0 zł jest osiągnięty, zanim cokolwiek wpłacimy, więc żadna wpłata nie jest potrzebna.

</details>

**4.** Czym różni się dokładne osiągnięcie celu od jego przekroczenia? Ile przebiegów jest potrzebnych w każdym przypadku?

<details>
<summary>Przykładowa odpowiedź</summary>

Przy dokładnym osiągnięciu ostatni przebieg daje sumę równą celowi, na przykład 4 wpłaty po 25 zł dają 100 zł. Przy przekroczeniu ostatni przebieg daje więcej niż cel, na przykład 4 wpłaty po 30 zł dają 120 zł. W obu przypadkach pętla kończy się zaraz po przebiegu, który dał sumę co najmniej równą celowi. Dodatkowy przebieg nigdy nie jest potrzebny.

</details>

**5.** Dlaczego przypadek 100 zł i 30 zł nie ujawnił błędu z punktu 9?

<details>
<summary>Przykładowa odpowiedź</summary>

Bo suma nigdy nie równa się celowi: po 90 zł jest od razu 120 zł. `<` i `<=` różnią się tylko wtedy, gdy postęp jest dokładnie równy celowi. Taki przypadek ujawniają cel 0 i cel 100 przy wpłatach po 25 zł.

</details>

**6.** Dlaczego program z punktu 10 może nigdy się nie skończyć, choć w każdym przebiegu coś się zmienia?

<details>
<summary>Przykładowa odpowiedź</summary>

Bo zmienia się cel, a nie postęp. `saved` zostaje równe 0, a `goal` rośnie, więc `saved < goal` zawsze daje `true`. Aktualizacja jakiejś zmiennej nie gwarantuje końca. Postęp musi zbliżać się do celu.

</details>

**7.** Dlaczego misja z czytaniem kończy się najpóźniej po 7 dniach?

<details>
<summary>Przykładowa odpowiedź</summary>

Bo pierwszego dnia czyta się co najmniej 1 stronę, a każdego następnego dwa razy więcej. Nawet przy najmniejszym starcie suma po 7 dniach wynosi 1 + 2 + 4 + 8 + 16 + 32 + 64 = 127, czyli więcej niż największy cel, 100 stron. Większy start kończy pętlę jeszcze wcześniej.

</details>

## Podsumowanie

- Pętla może trwać, **dopóki cel nie jest osiągnięty**. Warunek porównuje wtedy zmieniający się postęp z celem, a liczba przebiegów wynika z postępu.
- **Cel** to stan, który chcemy osiągnąć, **postęp** to wartość zmieniająca się w kolejnych przebiegach, a **krok** to zmiana postępu w jednym przebiegu. Krok może być stały albo zmieniać się z przebiegu na przebieg.
- Warunek `postęp < cel` pyta, czy jeszcze czegoś brakuje. Osiągnięty cel nie wymaga dodatkowego przebiegu. Cel osiągnięty od początku oznacza zero przebiegów.
- Ostatni przebieg może trafić dokładnie w cel albo go przekroczyć. Oba przypadki trzeba sprawdzić, bo tylko dokładne trafienie ujawnia błąd `<=`.
- Pętla kończy się tylko wtedy, gdy każdy przebieg przybliża postęp do celu. Dane, które by to uniemożliwiły, na przykład wpłatę 0 zł, sprawdzaj **przed** pętlą.
- Nie wystarczy, że w pętli coś się zmienia. Musi zmieniać się to, od czego zależy warunek, i to w stronę celu.

## Co dalej

Jak dotąd złe dane kończyły program komunikatem. W lekcji 4.5 pętla będzie powtarzać pytanie, **dopóki użytkownik nie poda dopuszczalnej wartości**: celem będzie wtedy poprawna odpowiedź: [Lekcja 4.5: Ponawianie pytania o poprawną wartość](lesson_05_ask_again.md).

---

## Przykładowe rozwiązania

Zajrzyj tutaj **po własnej próbie**. Twoje nazwy mogą się różnić, jeśli standardowe wyjście jest takie, jak wymagane.

<details>
<summary>Punkt 6: tabela przewidywań</summary>

| Cel | Wpłata | Liczba wpłat | Końcowa suma |
|---|---|---|---|
| 0 | 25 | 0 | 0 |
| 25 | 25 | 1 | 25 |
| 500 | 25 | 20 | 500 |

</details>

<details>
<summary>Punkt 8: cztery pytania o zakończenie</summary>

1. Tak. Każda wpłata to co najmniej 25 zł, więc suma rośnie w każdym przebiegu.
2. Nie. Cel się nie zmienia i wynosi najwyżej 500 zł, a suma rośnie bez przerwy, więc w końcu go dogoni.
3. Suma `saved` musi osiągnąć cel albo go przekroczyć. Wtedy `saved < goal` daje `false`.
4. Bez nich wpłata 0 zł albo ujemna nie przybliżałaby sumy do celu i pętla mogłaby się nie skończyć. Górna granica celu sprawia też, że przebiegów jest najwyżej 20.

</details>

<details>
<summary>Punkt 9: wyniki przed poprawką i poprawka</summary>

Przed poprawką:

<!-- input: savings_bug -->
```text
0
25
```

<!-- output: savings_bug -->
```text
Enter goal in zl (0-500):
Enter payment in zl (25-100):
Payment 1: saved 25 zl
Payments: 1
Saved: 25 zl
```

<!-- input: savings_bug -->
```text
100
25
```

<!-- output: savings_bug -->
```text
Enter goal in zl (0-500):
Enter payment in zl (25-100):
Payment 1: saved 25 zl
Payment 2: saved 50 zl
Payment 3: saved 75 zl
Payment 4: saved 100 zl
Payment 5: saved 125 zl
Payments: 5
Saved: 125 zl
```

<!-- input: savings_bug -->
```text
100
30
```

<!-- output: savings_bug -->
```text
Enter goal in zl (0-500):
Enter payment in zl (25-100):
Payment 1: saved 30 zl
Payment 2: saved 60 zl
Payment 3: saved 90 zl
Payment 4: saved 120 zl
Payments: 4
Saved: 120 zl
```

- **Pierwszy niezgodny przypadek** to cel 0: wymaganie nie potrzebuje żadnej wpłaty, a program robi jedną, bo `0 <= 0` daje `true`.
- **Cel 100 przy wpłatach po 25 zł:** po czterech wpłatach suma wynosi dokładnie 100 zł, a `100 <= 100` daje `true`. Program robi piątą, zbędną wpłatę.
- **Cel 100 przy wpłatach po 30 zł** daje ten sam wynik co poprawny program, bo suma przeskakuje ze 90 zł od razu na 120 zł i nigdy nie równa się celowi. **Nie każdy zestaw danych wykryje błąd:** ten ujawniają tylko przypadki, w których postęp trafia dokładnie w cel.
- **Poprawka:** `while (saved < goal)`. Poprawiony program to program z punktu 2. Jego wyniki dla tych trzech par są sprawdzone w punktach 2, 5 i 6.

</details>

<details>
<summary>Punkt 11: misja, cel czytelniczy</summary>

<!-- example: reading_goal -->
```cpp
#include <iostream>

int main() {
    int page_goal{0};
    int first_day_pages{0};

    std::cout << "Enter page goal (0-100):\n";
    std::cin >> page_goal;
    std::cout << "Enter pages for day 1 (1-10):\n";
    std::cin >> first_day_pages;

    const bool goal_ok{page_goal >= 0 && page_goal <= 100};
    const bool pages_ok{first_day_pages >= 1 && first_day_pages <= 10};

    if (goal_ok && pages_ok) {
        int total_pages{0};
        int pages_today{first_day_pages};
        int day{0};

        while (total_pages < page_goal) {
            ++day;
            total_pages += pages_today;
            std::cout << "Day " << day << ": read " << pages_today << ", total " << total_pages << "\n";
            pages_today = pages_today * 2;
        }

        std::cout << "Days: " << day << "\n";
        std::cout << "Total pages: " << total_pages << "\n";
    } else {
        std::cout << "Invalid reading data\n";
    }
}
```

| Sprawdzenie warunku | `total_pages` przy sprawdzeniu | `total_pages < 20` | Dzień | Strony tego dnia | `total_pages` po dniu | Strony na następny dzień |
|---|---|---|---|---|---|---|
| 1 | 0 | `true` | 1 | 3 | 3 | 6 |
| 2 | 3 | `true` | 2 | 6 | 9 | 12 |
| 3 | 9 | `true` | 3 | 12 | 21 | 24 |
| 4 | 21 | `false` | — | — | — | — |

- **Cel, postęp i krok:** `page_goal` się nie zmienia. `total_pages` to postęp i akumulator. `pages_today` to krok, który po każdym dniu się podwaja.
- **Kolejność w ciele:** numer dnia, dodanie stron dnia do sumy, wypisanie linijki, a dopiero na końcu podwojenie liczby stron na następny dzień. Dzięki temu pierwszy dzień pokazuje liczbę podaną przez użytkownika.
- **Licznik dni** zaczyna od 0 i rośnie na początku każdego przebiegu, więc po pętli równa się liczbie dni. Dla celu 0 zostaje 0.
- **Zakończenie i bezpieczeństwo:** krok to co najmniej 1 strona i rośnie z każdym dniem, więc suma rośnie w każdym przebiegu, a dla celu najwyżej 100 stron pętla kończy się najpóźniej po 7 dniach. Dla wszystkich dopuszczalnych danych największa liczba stron jednego dnia to 96 (cel 100, start 6: 6, 12, 24, 48, 96), a największa suma to 189 (cel 100, start 3), więc wszystkie wartości mieszczą się w `int` z ogromnym zapasem.
- Po ostatnim dniu `pages_today` ma już wartość dla dnia, który się nie odbędzie. To nie szkodzi, bo tej wartości program nie wypisuje.

</details>

**Poprzednia lekcja:** [Lekcja 4.3: Pętla `for`: licznik, warunek i aktualizacja w jednym miejscu](lesson_03_the_for_loop.md) · **Następna lekcja:** [Lekcja 4.5: Ponawianie pytania o poprawną wartość](lesson_05_ask_again.md) · [Opis kursu](../../README.md)

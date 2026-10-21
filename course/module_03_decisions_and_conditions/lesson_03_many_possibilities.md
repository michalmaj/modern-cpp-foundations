# Lekcja 3.3: Wybór spośród wielu możliwości (`else if`)

**Polski** · [English](lesson_03_many_possibilities.en.md) · [Opis kursu](../../README.md)

> **Moduł 3, lekcja 3** · około 75 minut
> **Potrzebujesz:** katalogu `cpp-workspace` i oryginalnego projektu `lesson_05_first_program`, jak dotąd. Debugger nie jest w tej lekcji potrzebny.
> **Wersja pilotażowa.** Programy z tej lekcji sprawdzamy automatycznie na Windowsie, Ubuntu i macOS, także z podanymi danymi wejściowymi.

## Zanim zaczniesz

Ta lekcja zakłada, że po lekcjach 3.1 i 3.2:

- piszesz `if` i `if`/`else` z klamrami i porównaniami `<`, `<=`, `>`, `>=`, `==`, `!=`;
- wiesz, że w `if`/`else` wykonuje się dokładnie jedna z dwóch gałęzi;
- sprawdzasz program dokładnie na granicy i tuż obok niej;
- wiesz, że zmienna zadeklarowana w bloku istnieje tylko w nim.

## Sytuacja

W lekcji 3.2 program wybierał jedną z dwóch dróg: `Passed` albo `Not passed`. Często jednak możliwości jest więcej: ocena może być słaba, dostateczna, dobra albo bardzo dobra, a bilet ulgowy, normalny albo seniorski. Dziś poznasz `else if`, czyli sposób na wybór **jednej z kilku** dróg. Nauczysz się też **planować przypadki testowe** dla wszystkich granic, zanim uruchomisz program.

Po tej lekcji będziesz:

- rozpoznawać, kiedy `if`/`else` przestaje wystarczać;
- wybierać jedną z kilku gałęzi łańcuchem `if`, `else if` i `else`;
- wyjaśniać, że warunki są sprawdzane po kolei, a wykonuje się gałąź pierwszego spełnionego warunku;
- znajdować błędy wynikające z kolejności warunków;
- wiedzieć, kiedy łańcuch potrzebuje końcowego `else`;
- odróżniać osobne `if` od jednego łańcucha;
- przygotowywać tabelę przypadków granicznych przed napisaniem programu.

## 1. Przygotuj projekt

W `cpp-workspace` utwórz katalog `lesson_3_3` i skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program`. Programy z punktów 2–7 wpisujesz w `main.cpp` tego katalogu.

## 2. Więcej niż dwa wyniki

Program dostaje liczbę punktów od 0 do 100 i ma przydzielić jeden z czterech poziomów:

| Liczba punktów | Wynik |
|---|---|
| 0–49 | `Needs work` |
| 50–74 | `Pass` |
| 75–89 | `Good` |
| 90–100 | `Excellent` |

Jedno `if`/`else` daje tylko dwie drogi, a tu są cztery. Potrzebny jest **łańcuch** warunków:

<!-- example: score_level -->
```cpp
#include <iostream>

int main() {
    int score{0};

    std::cout << "Enter score (0-100):\n";
    std::cin >> score;

    if (score >= 90) {
        std::cout << "Excellent\n";
    } else if (score >= 75) {
        std::cout << "Good\n";
    } else if (score >= 50) {
        std::cout << "Pass\n";
    } else {
        std::cout << "Needs work\n";
    }

    std::cout << "Score checked\n";
}
```

**Przewidź**, co wypisze program dla 49, 75 i 90. Zapisz odpowiedzi, a potem uruchom program trzy razy.

<!-- input: score_level -->
```text
49
```

<details>
<summary>Standardowe wyjście dla 49</summary>

<!-- output: score_level -->
```text
Enter score (0-100):
Needs work
Score checked
```

</details>

<!-- input: score_level -->
```text
75
```

<details>
<summary>Standardowe wyjście dla 75</summary>

<!-- output: score_level -->
```text
Enter score (0-100):
Good
Score checked
```

</details>

<!-- input: score_level -->
```text
90
```

<details>
<summary>Standardowe wyjście dla 90</summary>

<!-- output: score_level -->
```text
Enter score (0-100):
Excellent
Score checked
```

</details>

## 3. Jak działa łańcuch

Łańcuch zaczyna się od `if`, potem są kolejne `else if` (każde to słowo `else` i za nim nowe `if` z warunkiem), a na końcu `else`. Program przechodzi go **od góry**:

1. Sprawdza pierwszy warunek, `score >= 90`.
2. Jeśli nie jest spełniony, sprawdza następny, `score >= 75`, i tak dalej.
3. Gdy któryś warunek jest spełniony, wykonuje **jego** gałąź.
4. Pozostałe gałęzie tego łańcucha **pomija**: ich warunków już nie sprawdza.
5. Jeśli żaden warunek nie jest spełniony, wykonuje gałąź końcowego `else`.
6. Po łańcuchu program idzie dalej: `Score checked` pojawia się zawsze.

**Przewidź wynik dla 95.** 95 spełnia `score >= 90`, ale też `score >= 75` i `score >= 50`. Co wypisze program? Sprawdź.

<!-- input: score_level -->
```text
95
```

<details>
<summary>Standardowe wyjście dla 95 i wyjaśnienie</summary>

<!-- output: score_level -->
```text
Enter score (0-100):
Excellent
Score checked
```

Tylko `Excellent`. Program nie oblicza wszystkich warunków, żeby potem wybrać najlepszy. Idzie **w kolejności zapisanej w kodzie**: pierwszy warunek, `score >= 90`, jest spełniony, więc wykonuje się pierwsza gałąź, a reszta łańcucha zostaje pominięta. To, że 95 spełnia też dalsze warunki, nie ma już znaczenia.

</details>

Dlatego w tym łańcuchu progi idą **od najwyższego**: do `else if (score >= 75)` program dochodzi tylko wtedy, gdy `score >= 90` nie było spełnione. Ta gałąź obsługuje więc dokładnie wyniki od 75 do 89.

## 4. Zaplanuj przypadki testowe

Program sprawdzono dla 49, 75, 90 i 95. Czy to wystarczy? **Zanim zajrzysz dalej:**

1. Wypisz wartości, które warto sprawdzić. Pomyśl o każdej granicy między poziomami: sama granica i wartość tuż obok niej, po drugiej stronie.
2. Przy każdej wartości zapisz przewidywany wynik.
3. Uruchom program dla swoich wartości i porównaj.

Pytania pomocnicze: co wypisze program dla 50? Dla 74? Dla 89? Dlaczego dla 100 wynik to nadal `Excellent`? Czy program może wypisać więcej niż jeden poziom naraz?

<details>
<summary>Pełna lista przypadków kontrolnych: otwórz po własnej próbie</summary>

Każda z trzech granic (50, 75, 90) jest sprawdzona z obu stron, a do tego oba końce zakresu, 0 i 100:

| Punkty | Wynik | Dlaczego ta wartość |
|---|---|---|
| 0 | `Needs work` | dolny koniec zakresu |
| 49 | `Needs work` | tuż pod granicą 50 |
| 50 | `Pass` | granica 50 |
| 74 | `Pass` | tuż pod granicą 75 |
| 75 | `Good` | granica 75 |
| 89 | `Good` | tuż pod granicą 90 |
| 90 | `Excellent` | granica 90 |
| 100 | `Excellent` | górny koniec zakresu |

<!-- input: score_level -->
```text
0
```

<!-- output: score_level -->
```text
Enter score (0-100):
Needs work
Score checked
```

<!-- input: score_level -->
```text
50
```

<!-- output: score_level -->
```text
Enter score (0-100):
Pass
Score checked
```

<!-- input: score_level -->
```text
74
```

<!-- output: score_level -->
```text
Enter score (0-100):
Pass
Score checked
```

<!-- input: score_level -->
```text
89
```

<!-- output: score_level -->
```text
Enter score (0-100):
Good
Score checked
```

<!-- input: score_level -->
```text
100
```

<!-- output: score_level -->
```text
Enter score (0-100):
Excellent
Score checked
```

Wartości 49, 75 i 90 sprawdzono już w punkcie 2. Dla każdej wartości program wypisuje **dokładnie jeden** poziom, bo w łańcuchu wykonuje się najwyżej jedna gałąź. Dla 100 wynik to `Excellent`, bo 100 spełnia `score >= 90`.

</details>

## 5. Znajdź błąd: zła kolejność

Ten program ma te same wymagania co program z punktu 2. Kompiluje się bez błędów, ale ktoś ułożył warunki w innej kolejności:

<!-- example: score_order_bug -->
```cpp
#include <iostream>

int main() {
    int score{0};

    std::cout << "Enter score (0-100):\n";
    std::cin >> score;

    if (score >= 50) {
        std::cout << "Pass\n";
    } else if (score >= 75) {
        std::cout << "Good\n";
    } else if (score >= 90) {
        std::cout << "Excellent\n";
    } else {
        std::cout << "Needs work\n";
    }

    std::cout << "Score checked\n";
}
```

1. Przeczytaj wymagania z tabeli w punkcie 2.
2. **Przewidź**, co **powinien** wypisać program dla 30, 60, 80 i 90.
3. Przeczytaj warunki w kolejności, w jakiej program je sprawdza. Co się stanie dla 80?
4. Uruchom program dla tych czterech wartości.
5. Znajdź pierwszą wartość, dla której wybrana gałąź nie zgadza się z wymaganiami.
6. Popraw program.
7. Sprawdź ponownie wszystkie granice z punktu 4.

Wyniki programu przed poprawką i dwie poprawne wersje są w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

Każdy z tych warunków osobno jest poprawny: `score >= 75` naprawdę oznacza „co najmniej 75”. Błąd tkwi w **kolejności**. Gdy pierwszy jest warunek `score >= 50`, przechwytuje on wszystkie wyniki od 50 w górę, więc do gałęzi `Good` i `Excellent` program nigdy nie dochodzi. Nie zawsze wystarczy więc poprawić pojedynczy operator: czasem trzeba ułożyć warunki od nowa.

## 6. Końcowe `else` i brakujący przypadek

W tym łańcuchu nie ma końcowego `else`:

<!-- example: score_no_else -->
```cpp
#include <iostream>

int main() {
    int score{0};

    std::cout << "Enter score (0-100):\n";
    std::cin >> score;

    if (score >= 90) {
        std::cout << "Excellent\n";
    } else if (score >= 75) {
        std::cout << "Good\n";
    } else if (score >= 50) {
        std::cout << "Pass\n";
    }

    std::cout << "Score checked\n";
}
```

**Przewidź**, co wypisze program dla 80, a co dla 30.

<!-- input: score_no_else -->
```text
80
```

<!-- output: score_no_else -->
```text
Enter score (0-100):
Good
Score checked
```

<!-- input: score_no_else -->
```text
30
```

<details>
<summary>Standardowe wyjście dla 30</summary>

<!-- output: score_no_else -->
```text
Enter score (0-100):
Score checked
```

</details>

Dla 30 żaden warunek nie jest spełniony, a końcowego `else` nie ma, więc **nie wykonuje się żadna gałąź** łańcucha. Program nie wypisał poziomu.

Czy każdy łańcuch musi mieć końcowe `else`? **To zależy od wymagań.** Ostrzeżenie o kończących się miejscach z lekcji 3.1 było celowo opcjonalne: czasem nie trzeba nic robić. Tutaj jednak wymaganie mówi, że **każdy** wynik od 0 do 100 ma dostać poziom. Wtedy końcowe `else` jest naturalne: obsługuje wszystko, czego nie obsłużyły wcześniejsze gałęzie.

## 7. Osobne `if` to nie łańcuch

W lekcji 3.2 program miał dwie niezależne decyzje. Porównaj ten program z łańcuchem z punktu 2:

<!-- example: separate_ifs -->
```cpp
#include <iostream>

int main() {
    int score{0};

    std::cout << "Enter score (0-100):\n";
    std::cin >> score;

    if (score >= 50) {
        std::cout << "At least 50\n";
    }
    if (score >= 75) {
        std::cout << "At least 75\n";
    }
    if (score >= 90) {
        std::cout << "At least 90\n";
    }
}
```

**Przewidź**, ile linijek wypisze ten program dla 95, a ile dla 60. Ile poziomów wypisał dla 95 łańcuch z punktu 2?

<!-- input: separate_ifs -->
```text
95
```

<details>
<summary>Standardowe wyjście dla 95</summary>

<!-- output: separate_ifs -->
```text
Enter score (0-100):
At least 50
At least 75
At least 90
```

</details>

<!-- input: separate_ifs -->
```text
60
```

<details>
<summary>Standardowe wyjście dla 60</summary>

<!-- output: separate_ifs -->
```text
Enter score (0-100):
At least 50
```

</details>

Tu nie ma `else`, więc to trzy **osobne** decyzje: każdy `if` sprawdza swój warunek niezależnie od pozostałych, a dla 95 wykonują się wszystkie trzy bloki. W jednym łańcuchu `if`/`else if`/`else` wykonuje się **najwyżej jedna** gałąź. Kiedy kategorie się wykluczają, a wynik ma być jeden, potrzebny jest łańcuch.

**Zakres zmiennych.** Programy w tej lekcji wypisują wynik od razu w gałęzi i to wystarczy. Gdyby nazwa poziomu była potrzebna **po** łańcuchu, obowiązuje wzorzec z lekcji 3.2: zmienną `std::string` deklarujesz przed łańcuchem, a w gałęziach tylko przypisujesz jej wartość.

## 8. Misja: kategoria biletu

Muzeum ustala kategorię biletu według wieku zwiedzającej osoby:

| Wiek | Kategoria |
|---|---|
| 0–6 | `Free` |
| 7–17 | `Youth` |
| 18–64 | `Regular` |
| 65 i więcej | `Senior` |

W `cpp-workspace` utwórz katalog `ticket_category`, skopiuj do niego `CMakeLists.txt` z oryginalnego `lesson_05_first_program`, utwórz pusty `main.cpp` i napisz program samodzielnie. Program odczytuje jedną liczbę całkowitą, wiek, i wypisuje dokładnie jedną kategorię. Zakładamy, że odczyt się udaje, a wiek jest sensowny: liczbą nieujemną.

Dla wieku 30 standardowe wyjście ma być takie:

<!-- input: ticket_category -->
```text
30
```

<!-- output: ticket_category -->
```text
Enter age:
Category: Regular
```

**Zanim napiszesz program**, przygotuj tabelę przypadków testowych: wybierz wartości, które sprawdzą każdą granicę z obu stron, i przy każdej zapisz oczekiwaną kategorię. Potem napisz program i sprawdź go dla wszystkich swoich wartości.

### Kryterium sukcesu

- Program buduje się jako C++20 i dla każdego wieku wypisuje prośbę i dokładnie jedną linijkę `Category: …`, zgodnie z tabelą.
- Wiek jest zmienną `int` z wartością początkową, odczytaną przez `std::cin`.
- Kategorie wybiera łańcuch `if`, `else if` i `else`, z klamrami przy każdej gałęzi.
- Warunki są w takiej kolejności, że każda gałąź jest osiągalna. Umiesz wyjaśnić, dlaczego ta kolejność jest poprawna.
- Tabela przypadków powstała przed uruchomieniem programu i sprawdza wszystkie granice z obu stron.
- Ten sam program obsługuje wszystkie przypadki, bez zmiany kodu.

Gdy wynik się zgadza, możesz zapisać projekt w Gicie, jak w lekcji 1.5.

<details>
<summary>Podpowiedź 1</summary>

Ile jest granic między kategoriami? Przy każdej sprawdź samą granicę i wiek o jeden rok młodszy.

</details>

<details>
<summary>Podpowiedź 2</summary>

Ułóż warunki tak jak w punkcie 2: od najwyższego progu do najniższego, każdy z `>=`. Najmłodszą kategorię obsłuży końcowe `else`. Progi możesz zapisać jako stałe `const int` z nazwami, które mówią, od jakiego wieku zaczyna się kategoria.

</details>

<details>
<summary>Pełna lista przypadków kontrolnych: otwórz po własnej próbie</summary>

| Wiek | Kategoria | Granica |
|---|---|---|
| 6 | `Free` | tuż pod 7 |
| 7 | `Youth` | 7 |
| 17 | `Youth` | tuż pod 18 |
| 18 | `Regular` | 18 |
| 64 | `Regular` | tuż pod 65 |
| 65 | `Senior` | 65 |

<!-- input: ticket_category -->
```text
6
```

<!-- output: ticket_category -->
```text
Enter age:
Category: Free
```

<!-- input: ticket_category -->
```text
7
```

<!-- output: ticket_category -->
```text
Enter age:
Category: Youth
```

<!-- input: ticket_category -->
```text
17
```

<!-- output: ticket_category -->
```text
Enter age:
Category: Youth
```

<!-- input: ticket_category -->
```text
18
```

<!-- output: ticket_category -->
```text
Enter age:
Category: Regular
```

<!-- input: ticket_category -->
```text
64
```

<!-- output: ticket_category -->
```text
Enter age:
Category: Regular
```

<!-- input: ticket_category -->
```text
65
```

<!-- output: ticket_category -->
```text
Enter age:
Category: Senior
```

</details>

### Wariant: Senior od 60 lat

Muzeum zmienia regułę: kategoria `Senior` zaczyna się od 60 lat. Zmień w programie **jeden próg**, zaproponuj nowe wartości graniczne, przewidź wyniki i sprawdź, czy program nadal przydziela dokładnie jedną kategorię.

<details>
<summary>Nowe przypadki graniczne: otwórz po własnej próbie</summary>

<!-- input: ticket_category_variant -->
```text
59
```

<!-- output: ticket_category_variant -->
```text
Enter age:
Category: Regular
```

<!-- input: ticket_category_variant -->
```text
60
```

<!-- output: ticket_category_variant -->
```text
Enter age:
Category: Senior
```

Pozostałe granice (7 i 18) się nie zmieniły, więc ich przypadki dają te same wyniki co wcześniej.

</details>

Przykładowe rozwiązania są w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 9. Gdy coś pójdzie inaczej

| Co widzisz | Co to znaczy | Co zrobić |
|---|---|---|
| Wyższe kategorie nigdy się nie pojawiają | Wcześniejszy warunek przechwytuje wszystkie te wartości, na przykład `>= 50` stoi przed `>= 75`. | Ułóż progi od najwyższego do najniższego albo zmień warunki tak, żeby każda gałąź była osiągalna. |
| Dla niektórych wartości nie pojawia się żadna kategoria | Łańcuch nie ma końcowego `else`, a żaden warunek nie jest spełniony. | Jeśli każda wartość ma dostać kategorię, dodaj końcowe `else`. |
| Pojawiają się dwie albo więcej kategorii | To osobne `if`, a nie jeden łańcuch. | Połącz je w łańcuch: `else if` zamiast kolejnego samodzielnego `if`. |
| Zły wynik dokładnie na granicy | Pomylono `>` z `>=` albo próg jest przesunięty o jeden. | Sprawdź każdą granicę z obu stron, według tabeli przypadków. |
| Błąd kompilacji przy `else if` | Brakuje klamry przed `else` albo nawiasów wokół warunku. | Każda gałąź kończy się `}`, a po nim stoi `else if (…) {`. |

## 10. Wyjaśnij

Odpowiedz własnymi słowami, najlepiej na piśmie. Dopiero potem porównaj z przykładową odpowiedzią.

**1.** W jakiej kolejności program sprawdza warunki łańcucha i kiedy przestaje je sprawdzać?

<details>
<summary>Przykładowa odpowiedź</summary>

Od góry, w kolejności zapisanej w kodzie. Gdy trafi na pierwszy spełniony warunek, wykonuje jego gałąź, a pozostałych warunków tego łańcucha już nie sprawdza.

</details>

**2.** Dlaczego dla 95 punktów program z punktu 2 wypisuje tylko `Excellent`, choć 95 spełnia też `score >= 75`?

<details>
<summary>Przykładowa odpowiedź</summary>

Bo pierwszy warunek, `score >= 90`, jest spełniony, więc wykonuje się pierwsza gałąź, a reszta łańcucha zostaje pominięta. Dalszych warunków program już nie sprawdza.

</details>

**3.** Co było źle w programie z punktu 5, skoro każdy warunek osobno był poprawny?

<details>
<summary>Przykładowa odpowiedź</summary>

Kolejność. `score >= 50` stało pierwsze i przechwytywało wszystkie wyniki od 50 w górę, więc gałęzie `Good` i `Excellent` były nieosiągalne.

</details>

**4.** Kiedy łańcuch powinien kończyć się `else`?

<details>
<summary>Przykładowa odpowiedź</summary>

Gdy wymagania mówią, że każda wartość musi dostać jeden z wyników. Wtedy `else` obsługuje wszystko, czego nie obsłużyły wcześniejsze gałęzie. Gdy działanie jest opcjonalne, `else` nie jest potrzebne.

</details>

**5.** Czym różnią się trzy osobne `if` od łańcucha `if`/`else if`/`else`?

<details>
<summary>Przykładowa odpowiedź</summary>

Osobne `if` to osobne decyzje: może wykonać się kilka bloków. W łańcuchu wykonuje się najwyżej jedna gałąź.

</details>

## Podsumowanie

- Łańcuch `if`, `else if`, …, `else` wybiera **jedną z kilku** gałęzi. `else if` to `else` z kolejnym `if`, a nie osobne słowo kluczowe.
- Warunki są sprawdzane **po kolei**. Wykonuje się gałąź **pierwszego** spełnionego warunku, a reszta łańcucha zostaje pominięta.
- Kolejność ma znaczenie: przy progach z `>=` układaj je od najwyższego, inaczej część gałęzi stanie się nieosiągalna.
- Końcowe `else` obsługuje wszystko, czego nie obsłużyły wcześniejsze gałęzie. Jest potrzebne, gdy każda wartość musi dostać wynik.
- Osobne `if` podejmują osobne decyzje i mogą wykonać kilka bloków. W łańcuchu wykonuje się najwyżej jedna gałąź.
- Przed uruchomieniem przygotuj tabelę przypadków: każdą granicę sprawdź z obu stron, a także końce zakresu.

## Co dalej

Twoje programy wybierają już jedną z wielu dróg, a dobrze ułożony łańcuch wystarczył do wszystkich kategorii. Czasem jednak trzeba sprawdzić **dwa warunki naraz**, na przykład czy wartość mieści się w przedziale od 1 do 10. W lekcji 3.4 poznasz łączenie warunków. **Lekcja 3.4 jest w przygotowaniu.**

---

## Przykładowe rozwiązania

Zajrzyj tutaj **po własnej próbie**. Twoje nazwy mogą się różnić, jeśli standardowe wyjście jest takie, jak wymagane.

<details>
<summary>Punkt 5: wyniki przed poprawką i poprawione programy</summary>

Przed poprawką, dla 30, 60, 80 i 90:

<!-- input: score_order_bug -->
```text
30
```

<!-- output: score_order_bug -->
```text
Enter score (0-100):
Needs work
Score checked
```

<!-- input: score_order_bug -->
```text
60
```

<!-- output: score_order_bug -->
```text
Enter score (0-100):
Pass
Score checked
```

<!-- input: score_order_bug -->
```text
80
```

<!-- output: score_order_bug -->
```text
Enter score (0-100):
Pass
Score checked
```

<!-- input: score_order_bug -->
```text
90
```

<!-- output: score_order_bug -->
```text
Enter score (0-100):
Pass
Score checked
```

Pierwsza niezgodna wartość to 80: wymaganie mówi `Good`, a program wypisuje `Pass`. Dla 90 też jest `Pass` zamiast `Excellent`.

**Poprawka 1: progi od najwyższego.** To program z punktu 2: `>= 90`, potem `>= 75`, potem `>= 50`, na końcu `else`. Jego granice sprawdza pełna lista z punktu 4.

**Poprawka 2: progi od najniższego, z `<`.** Kolejność może być też odwrotna, jeśli warunki pytają „poniżej”:

<!-- example: score_ascending -->
```cpp
#include <iostream>

int main() {
    int score{0};

    std::cout << "Enter score (0-100):\n";
    std::cin >> score;

    if (score < 50) {
        std::cout << "Needs work\n";
    } else if (score < 75) {
        std::cout << "Pass\n";
    } else if (score < 90) {
        std::cout << "Good\n";
    } else {
        std::cout << "Excellent\n";
    }

    std::cout << "Score checked\n";
}
```

<!-- input: score_ascending -->
```text
49
```

<!-- output: score_ascending -->
```text
Enter score (0-100):
Needs work
Score checked
```

<!-- input: score_ascending -->
```text
50
```

<!-- output: score_ascending -->
```text
Enter score (0-100):
Pass
Score checked
```

<!-- input: score_ascending -->
```text
74
```

<!-- output: score_ascending -->
```text
Enter score (0-100):
Pass
Score checked
```

<!-- input: score_ascending -->
```text
75
```

<!-- output: score_ascending -->
```text
Enter score (0-100):
Good
Score checked
```

<!-- input: score_ascending -->
```text
89
```

<!-- output: score_ascending -->
```text
Enter score (0-100):
Good
Score checked
```

<!-- input: score_ascending -->
```text
90
```

<!-- output: score_ascending -->
```text
Enter score (0-100):
Excellent
Score checked
```

Obie wersje są poprawne. Liczy się to, czy przy zapisanej kolejności każda gałąź obsługuje dokładnie swój przedział.

</details>

<details>
<summary>Punkt 8: misja, kategoria biletu</summary>

<!-- example: ticket_category -->
```cpp
#include <iostream>

int main() {
    const int youth_from_age{7};
    const int regular_from_age{18};
    const int senior_from_age{65};
    int age{0};

    std::cout << "Enter age:\n";
    std::cin >> age;

    if (age >= senior_from_age) {
        std::cout << "Category: Senior\n";
    } else if (age >= regular_from_age) {
        std::cout << "Category: Regular\n";
    } else if (age >= youth_from_age) {
        std::cout << "Category: Youth\n";
    } else {
        std::cout << "Category: Free\n";
    }
}
```

- Progi idą od najwyższego, więc do każdej gałęzi program dochodzi tylko wtedy, gdy wyższe progi nie były spełnione. Gałąź `Regular` obsługuje więc dokładnie wiek od 18 do 64.
- Najmłodszą kategorię obsługuje końcowe `else`: każdy wiek dostaje dokładnie jedną kategorię.
- Stałe z progami mówią, od jakiego wieku zaczyna się kategoria, i każdy próg jest zapisany tylko raz.

</details>

<details>
<summary>Punkt 8: wariant, Senior od 60 lat</summary>

<!-- example: ticket_category_variant -->
```cpp
#include <iostream>

int main() {
    const int youth_from_age{7};
    const int regular_from_age{18};
    const int senior_from_age{60};
    int age{0};

    std::cout << "Enter age:\n";
    std::cin >> age;

    if (age >= senior_from_age) {
        std::cout << "Category: Senior\n";
    } else if (age >= regular_from_age) {
        std::cout << "Category: Regular\n";
    } else if (age >= youth_from_age) {
        std::cout << "Category: Youth\n";
    } else {
        std::cout << "Category: Free\n";
    }
}
```

Zmienił się tylko próg `senior_from_age`. Nowa granica to 60, więc sprawdzasz 59 i 60.

</details>

**Poprzednia lekcja:** [Lekcja 3.2: Dwie możliwości (`else`), równość i `bool`](lesson_02_two_ways.md) · **Następna lekcja:** w przygotowaniu · [Opis kursu](../../README.md)

# Lekcja 6.1: Pierwszy `std::vector` i pętla zakresowa `for`

**Polski** · [English](lesson_01_the_first_vector.en.md) · [Opis kursu](../../README.md)

> **Moduł 6, lekcja 1** · około 60–75 minut
> **Potrzebujesz:** katalogu `cpp-workspace` i oryginalnego projektu `lesson_05_first_program`, jak dotąd. Debugger nie jest w tej lekcji potrzebny.
> **Wersja pilotażowa.** Programy z tej lekcji sprawdzamy automatycznie na Windowsie, Ubuntu i macOS. Żaden z nich nie pyta o dane: wszystkie wartości są zapisane w kodzie.

## Zanim zaczniesz

Ta lekcja zakłada, że po Modułach 4 i 5:

- gromadzisz wynik w akumulatorze i liczysz zdarzenia licznikiem (lekcja 4.2);
- piszesz pętlę `for` z licznikiem i śledzisz ją w tabeli przebiegu (lekcja 4.3);
- wiesz, że inicjalizacja przez `{}` nie pozwala na konwersję zawężającą (lekcja 2.5);
- wywołujesz funkcję składową przez kropkę, jak `std::cin.fail()` (lekcja 4.5).

Własne funkcje z Modułu 5 nie są w tej lekcji potrzebne: wszystkie programy mieszczą się w `main`.

## Sytuacja

Stacja pomiarowa z lekcji 4.7 odczytywała kolejne temperatury i od razu aktualizowała sumę i liczniki. Po pętli znała sumę i liczbę pomiarów, ale **nie znała już samych pomiarów**. Każdy odczyt nadpisywał poprzednią wartość.

Co, jeśli po obliczeniu podsumowania chcesz wrócić do wcześniejszych wartości? Na przykład wskazać temperatury wyższe od średniej albo sprawdzić, ile razy powtórzyła się najwyższa z nich. Z samej sumy i liczby pomiarów tego nie odczytasz: suma 15 z trzech pomiarów to może być 3, 7 i 5, ale też 5, 5 i 5.

W tej lekcji poznasz **`std::vector`**: zmienną, która przechowuje wiele wartości tego samego typu w ustalonej kolejności, oraz pętlę, która kolejno je przegląda.

Po tej lekcji będziesz:

- wyjaśniać, dlaczego osobne zmienne na każdą wartość przestają wystarczać;
- definiować `std::vector<int>` z wartościami początkowymi i wskazywać typ jego elementów;
- odczytywać liczbę elementów przez `size()`;
- pisać pętlę zakresową `for` i wyjaśniać, skąd zmienna pętli bierze wartość;
- liczyć sumę i zdarzenia na elementach wektora;
- przechodzić po tym samym wektorze kilka razy, gdy drugie przejście potrzebuje wyniku pierwszego;
- przewidywać, ile razy wykona się pętla dla jednego, kilku i zera elementów;
- samodzielnie projektować proste przetwarzanie zbioru danych.

## 1. Przygotuj projekt

W `cpp-workspace` utwórz katalog `lesson_6_1` i skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program`. Programy z punktów 3–9 wpisujesz w `main.cpp` tego katalogu.

## 2. Osobna zmienna na każdą wartość

Gdyby stacja miała zapamiętać trzy pomiary, mogłaby zapisać każdy w osobnej zmiennej:

<!-- fragment -->
```cpp
const int first{3};
const int second{7};
const int third{5};
```

To poprawny kod. Ale każdy nowy pomiar to nowa nazwa i nowy składnik sumy `first + second + third`. Przy 24 pomiarach byłoby 24 nazwy. Pętla tu nie pomoże: nie da się w kolejnych przebiegach sięgać po kolei do `first`, `second` i `third`. Potrzebujesz **jednej** zmiennej na **wszystkie** pomiary.

## 3. Pierwszy wektor

<!-- example: measurements_stored -->
```cpp
#include <iostream>
#include <vector>

int main() {
    const std::vector<int> measurements{3, 7, 5, 9};

    std::cout << "Measurements stored: " << measurements.size() << "\n";
}
```

<!-- output: measurements_stored -->
```text
Measurements stored: 4
```

| W kodzie | Znaczenie |
|---|---|
| `#include <vector>` | Udostępnia `std::vector`, tak jak `<iostream>` udostępnia `std::cout`. |
| `std::vector<int>` | Typ zmiennej: **wektor**, czyli uporządkowana kolekcja wartości. W nawiasach ostrych `< >` stoi typ elementów: każdy element tego wektora to `int`. |
| `measurements` | Nazwa zmiennej. Jedna nazwa na całą kolekcję. |
| `{3, 7, 5, 9}` | Wartości początkowe, czyli **elementy** wektora. Wektor zachowuje ich kolejność: pierwszy jest 3, ostatni 9. |
| `const` | Ten program nie zmienia wektora, więc, jak przy innych zmiennych, oznaczamy go `const` (lekcja 2.2). |
| `measurements.size()` | Liczba elementów wektora, tutaj 4. `size()` to funkcja składowa wektora, wywoływana przez kropkę, jak `std::cin.fail()` w lekcji 4.5. |

Wszystkie elementy jednego wektora mają ten sam typ, w tej lekcji `int`. Pisz `#include <vector>` w każdym programie z wektorem: na niektórych systemach program zbuduje się i bez niego, ale na innych nie.

**Liczbę elementów wypisuj bezpośrednio**, jak tutaj. `size()` podaje ją w osobnym typie przeznaczonym do rozmiarów, a nie w `int`. Zapisanie tego wyniku w zmiennej `int` z `{}` kompilator odrzuci jako konwersję zawężającą, jak w lekcji 2.5. Właściwy typ poznasz w jednej z kolejnych lekcji.

## 4. Pętla zakresowa `for`

Ten program wypisuje wszystkie pomiary, każdy w osobnej linijce:

<!-- example: measurements_listed -->
```cpp
#include <iostream>
#include <vector>

int main() {
    const std::vector<int> measurements{3, 7, 5, 9};

    for (const int measurement : measurements) {
        std::cout << measurement << "\n";
    }
}
```

**Przewidź**, co wypisze program i w jakiej kolejności. Potem go uruchom.

<details>
<summary>Standardowe wyjście</summary>

<!-- output: measurements_listed -->
```text
3
7
5
9
```

</details>

To **pętla zakresowa `for`** (ang. *range-based for*). Jej nagłówek czytaj: „dla każdego `measurement` z `measurements`”.

| Część | Znaczenie |
|---|---|
| `for` | To samo słowo co w lekcji 4.3: powtarzanie. |
| `const int measurement` | **Zmienna pętli.** W każdym przebiegu dostaje wartość kolejnego elementu. Jej typ to typ elementów wektora: `int`. `const`, bo ciało tylko ją odczytuje. |
| `:` | Dwukropek oddziela zmienną pętli od kolekcji, którą pętla przegląda. |
| `measurements` | Wektor, którego elementy przeglądasz. |
| ciało w `{ }` | Wykonuje się raz dla każdego elementu. |

W pętli z lekcji 4.3 trzeba było zapisać wartość początkową licznika, warunek i aktualizację. Tutaj nie ma żadnej z tych części. Pętla sama bierze elementy po kolei i kończy się po ostatnim, więc nie ma licznika do zwiększania ani warunku, w którym można się pomylić o jeden.

Nazwy dobieraj tak, żeby się czytały: wektor w liczbie mnogiej (`measurements`), zmienna pętli w pojedynczej (`measurement`).

## 5. Przebieg pętli krok po kroku

| Przebieg | Wartość `measurement` | Na ekranie |
|---|---|---|
| 1 | 3, pierwszy element | `3` |
| 2 | 7 | `7` |
| 3 | 5 | `5` |
| 4 | 9, ostatni element | `9` |
| — | nie ma kolejnego elementu: pętla się kończy | |

Odpowiedz, zanim otworzysz odpowiedzi:

1. Ile razy wykonuje się ciało pętli?
2. Jaka wartość pojawia się jako pierwsza?
3. Jaka pojawia się jako ostatnia?
4. Czy kolejność jest taka sama jak w nawiasach klamrowych?
5. Czy w ciele trzeba pisać `++`, żeby przejść do kolejnego elementu?
6. Co się zmieni, jeśli dopiszesz do nawiasów klamrowych piąty element? A ile razy wykona się ciało dla wektora `{6}`?

<details>
<summary>Odpowiedzi</summary>

1. Cztery razy: raz dla każdego z czterech elementów.
2. 3, czyli pierwszy element w nawiasach klamrowych.
3. 9, czyli ostatni element.
4. Tak. Pętla zakresowa przegląda elementy w kolejności, w jakiej są przechowywane, a wektor przechowuje je w kolejności z inicjalizacji.
5. Nie. Pętla sama przechodzi do kolejnego elementu. W tej pętli nie ma żadnego licznika do zwiększania.
6. Ciało wykona się pięć razy, a ostatni wypisany będzie nowy element. Samej pętli nie trzeba zmieniać: sprawdzisz to w następnym punkcie. Dla wektora `{6}` ciało wykona się raz.

</details>

## 6. Więcej danych, ta sama pętla

Dopisz pomiar 4 na końcu nawiasów klamrowych i dodaj linijkę z liczbą elementów:

<!-- example: measurements_five -->
```cpp
#include <iostream>
#include <vector>

int main() {
    const std::vector<int> measurements{3, 7, 5, 9, 4};

    std::cout << "Measurements stored: " << measurements.size() << "\n";

    for (const int measurement : measurements) {
        std::cout << measurement << "\n";
    }
}
```

**Przewidź** wszystkie linijki standardowego wyjścia i uruchom program.

<details>
<summary>Standardowe wyjście</summary>

<!-- output: measurements_five -->
```text
Measurements stored: 5
3
7
5
9
4
```

</details>

Zmieniła się tylko linijka z danymi. Pętla jest taka sama i przegląda tyle elementów, ile wektor ma. Przy osobnych zmiennych z punktu 2 nowy pomiar oznaczałby nową nazwę i nową linijkę z `std::cout`.

## 7. Suma i licznik na danych z wektora

Wektor przechowuje dane, a przetwarzasz je tak jak dotąd. Trasa wycieczki składa się z etapów o długości w kilometrach. Program liczy długość całej trasy i liczbę długich etapów, czyli takich, które mają co najmniej 12 km:

<!-- example: route_summary -->
```cpp
#include <iostream>
#include <vector>

int main() {
    const std::vector<int> stages{12, 8, 15, 10};

    int total{0};
    int long_stages{0};

    for (const int stage : stages) {
        total += stage;

        if (stage >= 12) {
            ++long_stages;
        }
    }

    std::cout << "Total distance: " << total << " km\n";
    std::cout << "Long stages: " << long_stages << "\n";
}
```

**Przewidź** obie linijki wyniku i uruchom program.

<details>
<summary>Standardowe wyjście</summary>

<!-- output: route_summary -->
```text
Total distance: 45 km
Long stages: 2
```

</details>

`total` to akumulator, a `long_stages` licznik zdarzeń, oba zadeklarowane **przed** pętlą, jak w lekcji 4.2. Nowe jest tylko źródło wartości: elementy wektora zamiast licznika albo wejścia.

## 8. Drugie przejście po tych samych danych

Teraz program ma dodatkowo wypisać po każdym etapie, ile kilometrów zostało do końca trasy. Pierwsza taka linijka wymaga długości **całej** trasy, a ta jest znana dopiero po przejrzeniu wszystkich etapów. Dlatego program przegląda wektor drugi raz:

<!-- example: route_plan -->
```cpp
#include <iostream>
#include <vector>

int main() {
    const std::vector<int> stages{12, 8, 15, 10};

    int total{0};
    int long_stages{0};

    for (const int stage : stages) {
        total += stage;

        if (stage >= 12) {
            ++long_stages;
        }
    }

    std::cout << "Total distance: " << total << " km\n";
    std::cout << "Long stages: " << long_stages << "\n";

    int remaining{total};

    for (const int stage : stages) {
        remaining -= stage;
        std::cout << "Left after stage: " << remaining << " km\n";
    }
}
```

**Przewidź** cztery linijki `Left after stage` i uruchom program.

<details>
<summary>Standardowe wyjście</summary>

<!-- output: route_plan -->
```text
Total distance: 45 km
Long stages: 2
Left after stage: 33 km
Left after stage: 25 km
Left after stage: 10 km
Left after stage: 0 km
```

</details>

- **Pierwsze przejście** liczy długość trasy. **Drugie** zaczyna od niej i odejmuje kolejne etapy. Ostatnia linijka to 0 km, co potwierdza, że oba przejścia objęły te same etapy.
- **Dane nie znikają po pierwszej pętli.** Pętla zakresowa tylko odczytuje elementy, więc wektor ma potem te same etapy w tej samej kolejności. W lekcji 4.7 każda wartość była dostępna tylko w jednym przebiegu.
- Drugie przejście jest potrzebne, bo **korzysta z wyniku pierwszego**. Gdy wystarcza jedno przejście, jak przy średniej z lekcji 4.7, przechowywanie wszystkich wartości nie jest konieczne.

## 9. Pusty wektor

Wektor może nie mieć żadnego elementu. Wtedy nawiasy klamrowe są puste:

<!-- example: measurements_empty -->
```cpp
#include <iostream>
#include <vector>

int main() {
    const std::vector<int> measurements{};

    std::cout << "Measurements stored: " << measurements.size() << "\n";

    for (const int measurement : measurements) {
        std::cout << measurement << "\n";
    }

    std::cout << "End of list\n";
}
```

**Przewidź**, ile razy wykona się ciało pętli i co wypisze program.

<details>
<summary>Standardowe wyjście i wyjaśnienie</summary>

<!-- output: measurements_empty -->
```text
Measurements stored: 0
End of list
```

Ciało nie wykonało się ani razu: nie ma żadnego elementu, więc pętla od razu się kończy. To poprawne i bezpieczne zachowanie, jak pętla z zerem przebiegów w lekcji 4.1.

</details>

Nie każdy wynik ma sens dla pustej kolekcji. Długość trasy bez etapów to 0 km. Ale najdłuższego etapu trasy bez etapów nie ma. Jak sprawdzić, czy wektor jest pusty, poznasz w kolejnej lekcji.

## 10. Misja: deszczowe dni

Program analizuje opady deszczu w kolejnych dniach. Opad z każdego dnia to mała, nieujemna liczba całkowita milimetrów. Wartości są wpisane w kodzie:

<!-- fragment -->
```cpp
const std::vector<int> rainfall{0, 5, 2, 5, 1, 0};
```

**Wymagania:**

- Program przechowuje opady w `std::vector<int>` z wartościami początkowymi, jak wyżej. Nie odczytuje niczego z wejścia.
- Wypisuje trzy linijki: łączną sumę opadów (`Total rainfall: N`), największy opad zanotowany jednego dnia (`Highest daily rainfall: N`) i liczbę dni, w których wystąpił ten największy opad (`Days at highest rainfall: N`).
- Zakładamy, że wektor ma co najmniej jeden element i że wszystkie wartości są nieujemne. Pustego wektora nie obsługujesz: suma 0 miałaby sens, ale największego opadu by nie było, a program, który wypisze wtedy 0, poda wartość spoza danych.
- Po zmianie samych wartości w nawiasach klamrowych program podaje poprawne wyniki dla nowych danych, bez żadnej innej zmiany w kodzie.
- Elementy przeglądasz pętlą zakresową `for`. Wystarczą konstrukcje z tej lekcji i z poprzednich modułów.

W `cpp-workspace` utwórz katalog `rainy_days`, skopiuj do niego `CMakeLists.txt` z oryginalnego `lesson_05_first_program`, utwórz pusty `main.cpp` i napisz program samodzielnie.

Dla danych powyżej standardowe wyjście ma być takie:

<!-- output: rainfall_report -->
```text
Total rainfall: 13
Highest daily rainfall: 5
Days at highest rainfall: 2
```

**To nie jest program z trasą z innymi napisami.** Tam program był gotowy. Tutaj nikt nie mówi, ile przejść potrzeba ani co liczy każde z nich. Musisz samodzielnie zdecydować:

1. jak znaleźć największą wartość, przeglądając kolejne dni;
2. jakie zmienne przechowają wyniki i od jakich wartości zaczynają;
3. w którym momencie programu znasz już ostateczny największy opad;
4. czy jedno przejście po wektorze wystarczy, czy potrzebujesz kolejnego;
5. jak policzyć wszystkie dni z największym opadem, także gdy jest ich kilka.

**Zanim napiszesz program**, przygotuj tabelę przypadków testowych. Każdy przypadek to inne wartości w nawiasach klamrowych. Uwzględnij: dane z wymagań, jeden dzień, wszystkie dni z tym samym opadem, same zera, największy opad tylko pierwszego dnia i największy opad tylko ostatniego dnia. Przy każdym przypadku zapisz, jakie trzy liczby powinien wypisać program.

**Potem pracuj w tej kolejności:**

1. Napisz program i uruchom go dla danych z wymagań.
2. Porównaj wynik z oczekiwanym standardowym wyjściem.
3. Zmieniaj kolejno wartości w nawiasach klamrowych na pozostałe przypadki z tabeli. Przed każdym uruchomieniem przewidź wynik.
4. Przy każdej niezgodności sprawdź, czy błąd jest w programie, czy w tabeli.

### Kryterium sukcesu

- Program buduje się jako C++20, a dla danych z wymagań wypisuje dokładnie trzy linijki pokazane wyżej.
- Dla każdego przypadku z tabeli podaje poprawną sumę, największy opad i liczbę dni z największym opadem, po zmianie samych wartości w nawiasach klamrowych.
- Dni z największym opadem są policzone wszystkie, także gdy jest ich kilka albo gdy wszystkie dni mają ten sam opad.
- Program nie odczytuje danych z wejścia i nie używa niczego spoza tej lekcji i poprzednich modułów.
- Tabela przypadków powstała przed uruchomieniem programu.
- Umiesz wyjaśnić, w którym momencie Twój program zna ostateczny największy opad.

Gdy wynik się zgadza, możesz zapisać projekt w Gicie, jak w lekcji 1.5.

<details>
<summary>Podpowiedź 1</summary>

Jakie informacje o opadach możesz obliczyć podczas pierwszego przeglądania wszystkich dni?

</details>

<details>
<summary>Podpowiedź 2</summary>

Aby policzyć dni z największym opadem, musisz najpierw wiedzieć, jaka była największa wartość.

</details>

<details>
<summary>Podpowiedź 3</summary>

Po znalezieniu największego opadu możesz ponownie przejrzeć te same zapisane wartości i zliczyć elementy równe maksimum.

</details>

<details>
<summary>Pełna lista przypadków kontrolnych: otwórz po przygotowaniu własnej tabeli</summary>

| Przypadek | Wartości w nawiasach klamrowych | Suma | Największy opad | Dni z największym opadem | Co sprawdza |
|---|---|---|---|---|---|
| A | `0, 5, 2, 5, 1, 0` | 13 | 5 | 2 | dane z wymagań: największy opad dwa razy |
| B | `3, 3, 3` | 9 | 3 | 3 | wszystkie dni z tym samym opadem |
| C | `7` | 7 | 7 | 1 | jeden dzień |
| D | `0, 0, 0` | 0 | 0 | 3 | brak opadów: największy opad to 0 |
| E | `8, 2, 1, 3` | 14 | 8 | 1 | największy opad tylko pierwszego dnia |
| F | `1, 2, 3, 9` | 15 | 9 | 1 | największy opad tylko ostatniego dnia |

Dla każdego przypadku standardowe wyjście ma te same trzy linijki co dla A, z liczbami z tabeli. Przypadek A jest sprawdzony wyżej, przy treści misji.

</details>

Przykładowe rozwiązanie jest w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 11. Znajdź błąd: za dużo dni z największym opadem

To zadanie wykonaj **po misji**. Inna osoba rozwiązała tę samą misję, ale chciała przejrzeć wektor tylko raz. Jej program jest poniżej, w zwiniętej części, żeby nie podpowiadał rozwiązania misji.

<details>
<summary>Program do sprawdzenia: otwórz po napisaniu własnego programu</summary>

<!-- example: rainfall_bug -->
```cpp
#include <iostream>
#include <vector>

int main() {
    const std::vector<int> rainfall{0, 5, 2, 5, 1, 0};

    int total{0};
    int highest{0};
    int days_at_highest{0};

    for (const int amount : rainfall) {
        total += amount;

        if (amount > highest) {
            highest = amount;
        }

        if (amount == highest) {
            ++days_at_highest;
        }
    }

    std::cout << "Total rainfall: " << total << "\n";
    std::cout << "Highest daily rainfall: " << highest << "\n";
    std::cout << "Days at highest rainfall: " << days_at_highest << "\n";
}
```

1. Zapisz, jakie standardowe wyjście **powinno** się pojawić dla tych danych (przypadek A).
2. **Przewidź**, co wypisze **ten** program. Pomóż sobie tabelą przebiegu z kolumnami: `amount`, `highest` po pierwszym `if`, `days_at_highest` po drugim `if`.
3. Uruchom program.
4. Porównaj wynik z wymaganiem.
5. Znajdź dzień, który został policzony niepotrzebnie, i wyjaśnij, dlaczego program go policzył.
6. Popraw program.
7. Sprawdź poprawiony program dla przypadku A, z powtórzonym największym opadem. Potem przypadki C i E. Dlaczego błędny program dawał dla nich poprawny wynik?

</details>

Wynik programu przed poprawką i poprawione wersje są w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 12. Gdy coś pójdzie inaczej

| Co widzisz | Co to znaczy | Co zrobić |
|---|---|---|
| Błąd kompilacji przy `std::vector` | Brakuje `#include <vector>` albo w nazwie jest literówka. | Dopisz `#include <vector>` na początku pliku. |
| Kilka błędów w nagłówku pętli, na przykład `expected ';' in 'for' statement specifier` | Zamiast dwukropka stoi średnik: `for (const int x ; values)`. | Między zmienną pętli a wektorem stoi `:`. |
| `cannot assign to variable ... with const-qualified type 'const int'` | Ciało pętli próbuje zmienić zmienną pętli, która jest `const`. | W tej lekcji zmienna pętli służy tylko do odczytu. Wynik zapisuj w osobnej zmiennej, zadeklarowanej przed pętlą. |
| `cannot be narrowed` przy `size()` | Wynik `size()` trafia do zmiennej `int` z `{}`. | Wypisuj `size()` bezpośrednio (punkt 3). |
| Suma albo licznik pokazuje tylko ostatni element | Akumulator albo licznik jest zadeklarowany w ciele pętli i w każdym przebiegu zaczyna od nowa. | Zadeklaruj go przed pętlą, jak w lekcji 4.2. |
| Za dużo dni z największym opadem | Dni są liczone, zanim program zna ostateczny największy opad (punkt 11). | Prześledź program w tabeli dla przypadków A i F. |
| Program nic nie wypisuje i czeka | To nie powinno się zdarzyć: programy z tej lekcji nie odczytują wejścia. | Sprawdź, czy w kodzie nie został `std::cin` z innego programu. |

## 13. Wyjaśnij

Odpowiedz własnymi słowami, najlepiej na piśmie. Dopiero potem porównaj z przykładowymi odpowiedziami.

1. Czym jest `std::vector<int>`?
2. Dlaczego dołączamy `<vector>`?
3. Co oznacza `int` wewnątrz `std::vector<int>`?
4. Do czego służą wartości w nawiasach klamrowych przy definicji wektora?
5. Czy elementy wektora mają określoną kolejność?
6. Czym pętla zakresowa różni się od pętli `for` z licznikiem?
7. Co oznacza dwukropek w pętli zakresowej?
8. Skąd zmienna pętli bierze wartość?
9. Czy w pętli zakresowej trzeba ręcznie przechodzić do kolejnego elementu?
10. Co daje `const int` przy zmiennej pętli?
11. Ile przebiegów wykona pętla zakresowa dla pustego wektora?
12. Czy można kilka razy przejść po tym samym wektorze?
13. Dlaczego wektor przydaje się, gdy później chcemy wrócić do wcześniejszych danych?
14. Co podaje `size()`?
15. Dlaczego nie zapisujemy wyniku `size()` w zmiennej `int`?
16. Dlaczego w misji liczenie dni z największym opadem może wymagać drugiego przejścia?

<details>
<summary>Przykładowe odpowiedzi</summary>

1. Zmienna, która przechowuje uporządkowaną kolekcję wartości typu `int`, czyli elementów wektora.
2. Bo to w nim jest `std::vector`. Bez niego program może się nie zbudować, nawet jeśli na jednym systemie przypadkiem się buduje.
3. Typ elementów: każdy element tego wektora to `int`.
4. To wartości początkowe: elementy, które wektor ma od chwili utworzenia, w podanej kolejności. Puste nawiasy `{}` dają wektor bez elementów.
5. Tak. Wektor przechowuje elementy w kolejności z inicjalizacji i w tej kolejności przegląda je pętla zakresowa.
6. W pętli z licznikiem trzeba zapisać wartość początkową, warunek i aktualizację. Pętla zakresowa nie ma licznika: bierze po kolei każdy element kolekcji i kończy się po ostatnim.
7. Oddziela zmienną pętli od kolekcji, którą pętla przegląda. Nagłówek czyta się „dla każdego `measurement` z `measurements`”.
8. W każdym przebiegu dostaje wartość kolejnego elementu wektora, od pierwszego do ostatniego.
9. Nie. Pętla sama przechodzi do kolejnego elementu, więc nie ma `++` ani warunku do napisania.
10. Ciało może zmienną odczytać, ale nie może jej zmienić. Kompilator zgłosi błąd, gdyby ciało próbowało. Zmienna pętli to i tak osobna wartość: jej zmiana nie zmieniłaby elementu wektora.
11. Zero. Ciało nie wykona się ani razu, a program przejdzie za pętlę.
12. Tak. Pętla zakresowa tylko odczytuje elementy, więc po niej wektor ma te same elementy w tej samej kolejności i można go przejrzeć znowu.
13. Bo przechowuje wszystkie wartości. Program, który tylko aktualizuje sumę i liczniki, jak w lekcji 4.7, nie może wrócić do wcześniejszej wartości.
14. Liczbę elementów wektora.
15. Bo `size()` podaje wynik w osobnym typie przeznaczonym do rozmiarów, a inicjalizacja przez `{}` nie pozwala zamienić go na `int` (konwersja zawężająca, lekcja 2.5). Na razie wypisujemy `size()` bezpośrednio.
16. Bo dzień można uznać za dzień z największym opadem dopiero wtedy, gdy znany jest ostateczny największy opad. W pierwszym przejściu ta wartość może się jeszcze zmienić. Drugie przejście porównuje każdy dzień z ostateczną wartością. To nie jest jedyny możliwy sposób, ale jest najprostszy do sprawdzenia.

</details>

## Podsumowanie

- **`std::vector<int>`** przechowuje wiele wartości typu `int` w jednej zmiennej, w ustalonej kolejności. Wymaga `#include <vector>`.
- Wartości początkowe zapisujesz w nawiasach klamrowych: `const std::vector<int> measurements{3, 7, 5, 9};`. Puste `{}` dają wektor bez elementów.
- `measurements.size()` podaje liczbę elementów. Na razie wypisuj ją bezpośrednio, bez zapisywania w `int`.
- **Pętla zakresowa** `for (const int measurement : measurements)` wykonuje ciało raz dla każdego elementu, od pierwszego do ostatniego. Nie ma licznika, warunku ani aktualizacji do napisania.
- Dla pustego wektora pętla zakresowa nie wykonuje ani jednego przebiegu.
- Na elementach wektora działają znane akumulatory, liczniki i warunki.
- Po zakończeniu pętli dane nadal są w wektorze. Drugie przejście ma sens, gdy potrzebuje wyniku pierwszego, na przykład sumy albo największej wartości.
- Nie każdy wynik ma sens dla pustej kolekcji. Suma tak, największa wartość nie.

## Co dalej

W tej lekcji wszystkie elementy były wpisane w kod, zanim program się uruchomił. W kolejnej lekcji wektor będzie przyjmował nowe elementy w trakcie działania programu, a program sprawdzi, czy w ogóle jakieś dostał: [Lekcja 6.2: Dodawanie danych do wektora: `push_back()` i `empty()`](lesson_02_adding_to_a_vector.md).

---

## Przykładowe rozwiązania

Zajrzyj tutaj **po własnej próbie**. Twoje nazwy mogą się różnić, jeśli standardowe wyjście jest takie, jak wymagane.

<details>
<summary>Punkt 10: misja, deszczowe dni</summary>

<!-- example: rainfall_report -->
```cpp
#include <iostream>
#include <vector>

int main() {
    const std::vector<int> rainfall{0, 5, 2, 5, 1, 0};

    int total{0};
    int highest{0};

    for (const int amount : rainfall) {
        total += amount;

        if (amount > highest) {
            highest = amount;
        }
    }

    int days_at_highest{0};

    for (const int amount : rainfall) {
        if (amount == highest) {
            ++days_at_highest;
        }
    }

    std::cout << "Total rainfall: " << total << "\n";
    std::cout << "Highest daily rainfall: " << highest << "\n";
    std::cout << "Days at highest rainfall: " << days_at_highest << "\n";
}
```

- **Wektor przechowuje wszystkie dni**, więc po pierwszej pętli opady wciąż są dostępne. Bez niego program nie mógłby sprawdzić żadnego dnia drugi raz.
- **Pierwsze przejście** liczy sumę i szuka największego opadu. `highest` pamięta największą wartość spośród dni przejrzanych do tej pory. Gdy bieżący dzień ma większy opad, ten opad staje się nową wartością `highest`.
- **Wartość początkowa 0** jest bezpieczna tylko dzięki założeniom misji: wszystkie opady są nieujemne, a dzień jest co najmniej jeden. Dla danych `0, 0, 0` największy opad to rzeczywiście 0, bo taki opad był w danych. Dla pustego wektora program też wypisałby 0, ale takiego dnia nie byłoby w danych. Dlatego pusty wektor jest poza zakresem misji.
- **Drugie przejście** liczy dni równe największemu opadowi. Po pierwszej pętli `highest` ma już ostateczną wartość, więc każdy dzień jest porównywany z właściwą liczbą.
- **Powtórzony największy opad** to najważniejszy przypadek: w danych A pojawia się dwa razy, a w danych B i D wszystkie dni są równe. Gdyby program liczył zawsze tylko jeden taki dzień, przypadki C, E i F nie wykryłyby tego błędu.
- **Zmiana liczby elementów** zmienia tylko liczbę przebiegów obu pętli. Kod pętli zostaje ten sam.
- Dwa przejścia to czytelna strategia, ale nie jedyna. Poprawne rozwiązanie z jednym przejściem jest przy punkcie 11.

</details>

<details>
<summary>Punkt 11: wynik przed poprawką i poprawione wersje</summary>

Przed poprawką:

<!-- output: rainfall_bug -->
```text
Total rainfall: 13
Highest daily rainfall: 5
Days at highest rainfall: 3
```

| Dzień | `amount` | `highest` po pierwszym `if` | `days_at_highest` po drugim `if` |
|---|---|---|---|
| 1 | 0 | 0 | 1 |
| 2 | 5 | 5 | 2 |
| 3 | 2 | 5 | 2 |
| 4 | 5 | 5 | 3 |
| 5 | 1 | 5 | 3 |
| 6 | 0 | 5 | 3 |

- Suma i największy opad są poprawne. Błędna jest liczba dni: 3 zamiast 2.
- **Przyczyna:** licznik jest aktualizowany w złym miejscu, w tej samej pętli, w której program dopiero szuka największego opadu. Pierwszego dnia największym opadem „do tej pory” jest 0, więc ten dzień zostaje policzony. Potem największy opad rośnie do 5, ale licznik nie zapomina wcześniej policzonego dnia.
- **Dlaczego C i E dawały dobry wynik:** w obu przypadkach największy opad jest w pierwszym dniu, więc „największy do tej pory” od początku jest ostateczny. Tak samo jest w B i D, gdzie wszystkie dni są równe. Błąd ujawniają dane, w których przed największym opadem jest dzień z mniejszym: dla A program wypisuje 3 zamiast 2, a dla F (`1, 2, 3, 9`) 4 zamiast 1, bo każdy dzień jest na chwilę największym opadem.

**Poprawka z dwoma przejściami:** przenieś drugi `if` z licznikiem do osobnej pętli, za pierwszą. Otrzymasz rozwiązanie misji pokazane wyżej.

**Poprawka z jednym przejściem:** gdy pojawia się nowy największy opad, wcześniejsze liczenie przestaje mieć znaczenie, więc licznik zaczyna od zera:

<!-- example: rainfall_one_pass -->
```cpp
#include <iostream>
#include <vector>

int main() {
    const std::vector<int> rainfall{0, 5, 2, 5, 1, 0};

    int total{0};
    int highest{0};
    int days_at_highest{0};

    for (const int amount : rainfall) {
        total += amount;

        if (amount > highest) {
            highest = amount;
            days_at_highest = 0;
        }

        if (amount == highest) {
            ++days_at_highest;
        }
    }

    std::cout << "Total rainfall: " << total << "\n";
    std::cout << "Highest daily rainfall: " << highest << "\n";
    std::cout << "Days at highest rainfall: " << days_at_highest << "\n";
}
```

<!-- output: rainfall_one_pass -->
```text
Total rainfall: 13
Highest daily rainfall: 5
Days at highest rainfall: 2
```

Po wyzerowaniu licznika drugi `if` od razu liczy bieżący dzień, bo jego opad jest równy nowemu `highest`. Ta wersja jest krótsza, ale trudniej ją sprawdzić w głowie. Obie są poprawne dla wszystkich przypadków kontrolnych.

</details>

**Poprzednia lekcja:** [Lekcja 5.7: Program z własnych funkcji (sprawdzian Modułu 5)](../module_05_functions/lesson_07_a_program_of_functions.md) · **Następna lekcja:** [Lekcja 6.2: Dodawanie danych do wektora: `push_back()` i `empty()`](lesson_02_adding_to_a_vector.md) · [Opis kursu](../../README.md)

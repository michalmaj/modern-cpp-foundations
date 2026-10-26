# Lekcja 6.4: Wektor jako parametr funkcji: `const&`

**Polski** · [English](lesson_04_a_vector_as_a_parameter.en.md) · [Opis kursu](../../README.md)

> **Moduł 6, lekcja 4** · około 70–85 minut
> **Potrzebujesz:** katalogu `cpp-workspace` i oryginalnego projektu `lesson_05_first_program`, jak dotąd. Debugger nie jest w tej lekcji potrzebny.
> **Wersja pilotażowa.** Programy z tej lekcji sprawdzamy automatycznie na Windowsie, Ubuntu i macOS, także z podanymi danymi wejściowymi. Wpisywanie danych w oknie **Run** CLiona opisujemy bez ręcznego sprawdzenia na każdym systemie.

## Zanim zaczniesz

Ta lekcja zakłada, że po Module 5 i lekcjach 6.1–6.3:

- definiujesz własne funkcje z parametrami i wynikiem, przed `main` (lekcje 5.1–5.3);
- wiesz, że parametr `int` dostaje własną kopię wartości argumentu (lekcja 5.2);
- dzielisz program na funkcje obliczeniowe i `main`, który wypisuje wyniki, i sprawdzasz funkcje wydrukami testowymi (lekcja 5.5);
- przeglądasz wektor pętlą zakresową, dodajesz elementy przez `push_back` i sprawdzasz `empty()` (lekcje 6.1–6.3).

## Sytuacja

Funkcje i wektory były dotąd osobnymi tematami: funkcje dostawały pojedyncze liczby, a wektory przetwarzał `main`. Dwie stacje zapisały temperatury:

<!-- fragment -->
```cpp
const std::vector<int> north_temperatures{3, -2, 0, -5};
const std::vector<int> south_temperatures{7, 4, 2};
```

Dla każdej stacji chcesz policzyć dni z temperaturą poniżej zera. Pętlę, która to liczy, znasz. Ale nie chcesz pisać jej dwa razy. W lekcji 5.5 taki fragment trafiał do funkcji: **obliczenie z jasnym zadaniem, które ma działać dla różnych danych, to dobry kandydat na funkcję.** Tylko jak przekazać funkcji **wszystkie** odczyty z wybranego wektora? Osobny parametr `int` dla każdego odczytu nie wchodzi w grę: wektory mają różne długości.

Po tej lekcji będziesz:

- pisać funkcje z parametrem `const std::vector<int>&` i wyjaśniać role `const` i `&`;
- wyjaśniać, dlaczego taka funkcja nie tworzy kopii całego wektora;
- wywoływać tę samą funkcję dla różnych wektorów i wykorzystywać jej wynik w `main`;
- łączyć w jednej funkcji parametr-wektor z parametrem `int` przekazywanym przez wartość;
- projektować sensowny wynik funkcji dla pustego wektora;
- sprawdzać funkcje na wektorach, także pustych, i wykrywać pomylony argument wywołania.

## 1. Przygotuj projekt

W `cpp-workspace` utwórz katalog `lesson_6_4` i skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program`. Programy z punktów 2–6 wpisujesz w `main.cpp` tego katalogu.

## 2. Pierwsza funkcja, która dostaje wektor

<!-- example: cold_days -->
```cpp
#include <iostream>
#include <vector>

int count_cold_days(const std::vector<int>& temperatures) {
    int cold_days{0};

    for (const int temperature : temperatures) {
        if (temperature < 0) {
            ++cold_days;
        }
    }

    return cold_days;
}

int main() {
    const std::vector<int> north_temperatures{3, -2, 0, -5};
    const std::vector<int> south_temperatures{7, 4, 2};

    std::cout << "North cold days: " << count_cold_days(north_temperatures) << "\n";
    std::cout << "South cold days: " << count_cold_days(south_temperatures) << "\n";
}
```

**Przewidź** obie linijki wyniku i uruchom program.

<details>
<summary>Standardowe wyjście</summary>

<!-- output: cold_days -->
```text
North cold days: 2
South cold days: 0
```

</details>

- `temperatures` to **nazwa parametru**. W `main` nie ma wektora o tej nazwie: funkcja nie musi znać nazw wektorów z `main`. Argumentem może być dowolny wektor `std::vector<int>`.
- Funkcja odczytuje wartości z wektora, który dostała, liczy dni poniżej zera i **zwraca** wynik `int`, jak funkcje z lekcji 5.3.
- **Wypisuje `main`**, a funkcja tylko liczy, jak w lekcji 5.5.
- Pętla stoi w kodzie raz, a działa dla obu stacji.

## 3. Co znaczy `const std::vector<int>&`

| Część | Znaczenie |
|---|---|
| `std::vector<int>` | Typ: wektor liczb `int`. |
| `&` | Parametr jest **referencją**: odnosi się do istniejącego wektora z miejsca wywołania, a nie jest jego osobną kopią. |
| `const` | Przez ten parametr funkcja może wektor tylko **odczytywać**, nie może go zmieniać. |
| `temperatures` | Nazwa parametru, której funkcja używa w swoim ciele. |

Prosty model: **funkcja dostaje możliwość odczytania istniejącego wektora, bez tworzenia jego kopii.** Słowo „referencja” znaczy tu tyle, że `temperatures` to w czasie wywołania inna nazwa tego samego wektora, który przekazał `main`.

**Porównaj z lekcją 5.2.** Tam `void count_down(int remaining)` dostawało własną kopię liczby, a zmiana `remaining` nie zmieniała zmiennej w `main`. Kopia jednej liczby `int` nic nie kosztuje, więc pojedyncze liczby nadal przekazujemy przez wartość. Wektor może mieć bardzo wiele elementów, a funkcja, która go tylko czyta, nie potrzebuje kopii. Dlatego wektor do odczytu przekazujemy przez `const&`. Przekazywanie wektora przez wartość też jest poprawnym C++. Wzorca `const&` używamy wtedy, gdy funkcja ma kolekcję **tylko czytać**.

**Nie myl dwóch zapisów.** `const std::vector<int>& temperatures` w nagłówku funkcji to referencja do **całego wektora**. `for (const int temperature : temperatures)` w ciele to pętla zakresowa z lekcji 6.1: w każdym przebiegu kopiuje jedną liczbę `int`. Kopiowanie pojedynczej liczby to nie kopiowanie całej kolekcji.

**`const` dotyczy dostępu przez parametr.** Funkcja z parametrem `const&` nie może zmienić wektora **przez ten parametr**. To nie znaczy, że wektor staje się niezmienny na zawsze: jeśli w `main` wektor nie ma `const`, `main` nadal może go zmieniać:

<!-- example: cold_days_later -->
```cpp
#include <iostream>
#include <vector>

int count_cold_days(const std::vector<int>& temperatures) {
    int cold_days{0};

    for (const int temperature : temperatures) {
        if (temperature < 0) {
            ++cold_days;
        }
    }

    return cold_days;
}

int main() {
    std::vector<int> readings{};
    std::cout << "Cold days: " << count_cold_days(readings) << "\n";

    readings.push_back(-1);
    readings.push_back(4);
    std::cout << "Cold days: " << count_cold_days(readings) << "\n";
}
```

**Przewidź** obie linijki, także dla pierwszego wywołania z pustym wektorem. Potem uruchom program.

<details>
<summary>Standardowe wyjście</summary>

<!-- output: cold_days_later -->
```text
Cold days: 0
Cold days: 1
```

</details>

- Pierwsze wywołanie dostaje **pusty** wektor. Funkcja nie ma na to specjalnego warunku, a i tak zwraca 0: licznik zaczyna od 0, pętla zakresowa nie wykonuje ani jednego przebiegu, a `return` zwraca 0.
- `main` dodaje dwa elementy. Drugie wywołanie odczytuje ten sam, już zmieniony wektor i zwraca 1.

## 4. Przebieg wywołania

Dla `count_cold_days(north_temperatures)` z punktu 2:

| Krok | Co się dzieje |
|---|---|
| 1 | `main` ma wektor `north_temperatures` z czterema wartościami: 3, −2, 0, −5. |
| 2 | `main` wywołuje `count_cold_days(north_temperatures)`. |
| 3 | Parametr `temperatures` odnosi się do `north_temperatures`. Wektor nie jest kopiowany. |
| 4 | Pętla odczytuje kolejno 3, −2, 0 i −5. |
| 5 | Licznik rośnie dwa razy: dla −2 i dla −5. 0 nie jest poniżej zera. |
| 6 | Funkcja zwraca 2. |
| 7 | `main` wypisuje otrzymany wynik. |

**Przewidź:** co się zmieni w tej tabeli dla `count_cold_days(south_temperatures)`?

<details>
<summary>Odpowiedź</summary>

Parametr `temperatures` odnosi się teraz do `south_temperatures`. Pętla odczytuje 7, 4 i 2, czyli tylko trzy wartości, i licznik ani razu nie rośnie. Funkcja zwraca 0. Kod funkcji jest ten sam, zmienił się tylko wektor, do którego odnosi się parametr.

</details>

**Nie każde obliczenie ma naturalny wynik dla pustego wektora.** Liczba dni poniżej zera w pustym zbiorze to po prostu 0, tak samo suma. Ale średnia i największa wartość pustego zbioru nie istnieją (lekcje 6.1 i 6.2), więc funkcja, która je liczy, wymaga osobnej decyzji projektowej. W tej lekcji wybieramy obliczenia, dla których pusty wektor ma jednoznaczny wynik.

## 5. `const&` nie pozwala zmieniać wektora

Ktoś dopisał do funkcji linijkę, która dodaje odczyt:

<!-- broken: push_through_const_ref at=5:18 errors=1 error=^no matching member function for call to 'push_back'$ -->
```cpp
#include <iostream>
#include <vector>

int count_cold_days(const std::vector<int>& temperatures) {
    temperatures.push_back(10);

    int cold_days{0};

    for (const int temperature : temperatures) {
        if (temperature < 0) {
            ++cold_days;
        }
    }

    return cold_days;
}

int main() {
    const std::vector<int> north_temperatures{3, -2, 0, -5};

    std::cout << "North cold days: " << count_cold_days(north_temperatures) << "\n";
}
```

**Przewidź**, czy program się zbuduje.

<details>
<summary>Co zgłasza kompilator i dlaczego</summary>

Program się nie zbuduje. Kompilator zgłasza w linijce 5 `no matching member function for call to 'push_back'`, ten sam komunikat co w lekcji 6.2. W linijkach `note:` dodaje, że `temperatures` ma typ `const std::vector<int>`. Ogranicza to `const` w typie parametru: przez `temperatures` wektor można tylko czytać.

**Poprawka:** usuń linijkę z `push_back`. Zadaniem tej funkcji jest odczyt i liczenie, a nie zmienianie danych. Otrzymasz program z punktu 2.

</details>

## 6. Wektor i dodatkowa liczba

Funkcja może mieć kilka parametrów różnego rodzaju. Na przykład liczenie dni poniżej wybranego progu mogłoby mieć taki nagłówek:

<!-- fragment -->
```cpp
int count_below(const std::vector<int>& values, int threshold)
```

Wektor do odczytu idzie przez `const&`, a próg, mała liczba, przez wartość, jak w lekcji 5.2. Wywołanie podaje oba argumenty w kolejności parametrów: `count_below(north_temperatures, 0)`. Liczby `int` nie przekazujemy przez referencję: jej kopia nic nie kosztuje.

## 7. Misja: dwa tygodnie czytania

Program porównuje czytanie w dwóch tygodniach. Każdy tydzień to osobny wektor z liczbą stron przeczytanych w kolejnych dniach. Tydzień może mieć od 0 do 6 zapisanych dni, a każda wartość jest z zakresu 0–30. Dane są wpisane w kodzie:

<!-- fragment -->
```cpp
const std::vector<int> week_a{12, 0, 8, 15, 9};
const std::vector<int> week_b{5, 18, 11, 16};
```

**Wymagania:**

- Oba wektory są zdefiniowane w `main` jako `const std::vector<int>`. Program nie odczytuje niczego z wejścia.
- Dla każdego tygodnia program wypisuje łączną liczbę stron i liczbę dni, w których przeczytano **co najmniej** 10 stron. Dokładnie 10 stron spełnia cel. Dzień z 0 stron to zwykły dzień danych.
- Potem porównuje **łączne liczby stron** i wypisuje, w którym tygodniu przeczytano więcej, albo remis. Liczba dni z celem nie decyduje o wyniku.
- Program ma co najmniej dwie własne funkcje obliczeniowe:
  - funkcję, która zwraca sumę wartości z przekazanego wektora, jako `int`;
  - funkcję, która zwraca liczbę elementów osiągających próg, jako `int`, z progiem przekazanym jako dodatkowy parametr `int`.
- Obie funkcje dostają wektor przez `const std::vector<int>&`, są zdefiniowane przed `main` i niczego nie wypisują. Nazwy funkcji i parametrów wybierasz samodzielnie.
- Sumy i liczniki liczą funkcje, a nie `main`. `main` przygotowuje dane, wywołuje funkcje, porównuje wyniki i wypisuje raport.
- Oba wektory mogą być puste: program działa poprawnie także wtedy.

Standardowe wyjście ma dokładnie takie linijki, w tej kolejności: `Week A pages: N`, `Week A goal days: N`, `Week B pages: N`, `Week B goal days: N` i na końcu jedna z trzech: `More pages: Week A`, `More pages: Week B` albo `More pages: Tie`.

W `cpp-workspace` utwórz katalog `reading_weeks`, skopiuj do niego `CMakeLists.txt` z oryginalnego `lesson_05_first_program`, utwórz pusty `main.cpp` i napisz program samodzielnie.

Dla danych powyżej standardowe wyjście ma być takie:

<!-- output: reading_weeks -->
```text
Week A pages: 44
Week A goal days: 2
Week B pages: 50
Week B goal days: 3
More pages: Week B
```

Wartości są małe: tydzień ma najwyżej 6 dni po najwyżej 30 stron, więc sumy i liczniki bezpiecznie mieszczą się w `int`.

**To nie jest program ze stacjami z innymi napisami.** Tam była jedna gotowa funkcja. Musisz samodzielnie zdecydować:

1. jakie zadanie ma każda z dwóch funkcji i jak je nazwać;
2. jakie parametry mają funkcje i w jakiej kolejności;
3. od jakich wartości zaczynają się suma i licznik;
4. jak sprawić, żeby wartość równa progowi się liczyła;
5. jak wywołać obie funkcje dla obu tygodni;
6. jak `main` wybiera zwycięzcę i rozpoznaje remis;
7. co program wypisze dla pustych tygodni.

**Najpierw sprawdź każdą funkcję osobno**, jak w lekcji 5.5, zanim złożysz cały raport:

1. Przygotuj w `main` kilka małych wektorów `const`: dla funkcji sumującej pusty, jednoelementowy i kilkuelementowy; dla funkcji z progiem pusty, z wartościami poniżej progu, z wartością dokładnie 10 i z wartościami powyżej.
2. Przy każdym zapisz oczekiwany wynik.
3. Wywołaj funkcję i tymczasowo wypisz wynik.
4. Porównaj z oczekiwanym.
5. Usuń wydruki testowe z docelowego programu.

**Potem sprawdź cały program.** Uruchom go dla danych z wymagań, a następnie zmień wartości w nawiasach klamrowych na dwa, trzy przypadki z pełnej listy kontrolnej, na przykład remis sum i dwa puste tygodnie. Pozostałe przypadki z listy są sprawdzone automatycznie, więc nie musisz wpisywać ich wszystkich.

### Kryterium sukcesu

- Program buduje się jako C++20, a dla danych z wymagań wypisuje dokładnie pięć linijek pokazanych wyżej.
- Obie funkcje przyjmują wektor przez `const std::vector<int>&`, zwracają `int` i niczego nie wypisują. Próg jest parametrem `int`.
- Każda funkcja jest wywołana dla obu tygodni. Obliczenia nie są powtórzone w `main`.
- Wynik porównania zależy od sumy stron, także gdy liczby dni z celem są różne.
- Program działa dla pustych tygodni i dla wartości równej progowi.
- Wydruki testowe funkcji powstały przed złożeniem raportu i zostały usunięte z docelowego programu.
- Umiesz wyjaśnić, dlaczego wektor idzie przez `const&`, a próg przez wartość.

Gdy wynik się zgadza, możesz zapisać projekt w Gicie, jak w lekcji 1.5.

<details>
<summary>Podpowiedź 1</summary>

Które obliczenia wykonujesz zarówno dla tygodnia A, jak i B? Czy każde z nich może stać się jedną funkcją?

</details>

<details>
<summary>Podpowiedź 2</summary>

Funkcja nie musi wiedzieć, czy otrzymała dane tygodnia A, czy B. Potrzebuje jedynie wektora, a czasem dodatkowej wartości określającej próg.

</details>

<details>
<summary>Podpowiedź 3</summary>

Zaprojektuj osobno funkcję sumującą strony i funkcję liczącą dni spełniające cel. Wywołaj obie dla obu tygodni, a porównanie łącznych wyników pozostaw w `main()`.

</details>

<details>
<summary>Pełna lista przypadków kontrolnych: otwórz po przygotowaniu własnych testów</summary>

| | Tydzień A | Tydzień B | Strony A, dni z celem A | Strony B, dni z celem B | Ostatnia linijka | Co sprawdza |
|---|---|---|---|---|---|---|
| A | `{12, 0, 8, 15, 9}` | `{5, 18, 11, 16}` | 44, 2 | 50, 3 | `More pages: Week B` | dane z wymagań |
| B | `{20, 10}` | `{5, 0}` | 30, 2 | 5, 0 | `More pages: Week A` | wygrywa A |
| C | `{20, 0}` | `{10, 10}` | 20, 1 | 20, 2 | `More pages: Tie` | remis sum przy różnych dniach z celem |
| D | `{}` | `{}` | 0, 0 | 0, 0 | `More pages: Tie` | oba tygodnie puste |
| E | `{}` | `{10}` | 0, 0 | 10, 1 | `More pages: Week B` | jeden tydzień pusty |
| F | `{9}` | `{10}` | 9, 0 | 10, 1 | `More pages: Week B` | dokładnie na progu |
| G | `{9, 9}` | `{8}` | 18, 0 | 8, 0 | `More pages: Week A` | wszystkie wartości poniżej progu |
| H | `{10, 10, 10}` | `{30}` | 30, 3 | 30, 1 | `More pages: Tie` | remis sum przy innym rozkładzie |
| I | `{12, 0, 8, 15, 9}` | `{12, 0, 8, 15, 9}` | 44, 2 | 44, 2 | `More pages: Tie` | dwa identyczne tygodnie (punkt 8) |

**Testy automatyczne i Twoje próby.** Wszystkie przypadki z tabeli są sprawdzone automatycznie przez program kontrolny. To ten sam raport i te same funkcje co w rozwiązaniu referencyjnym, ale oba tygodnie odczytuje z wejścia: liczbę dni i strony tygodnia A, potem tygodnia B. Program kontrolny i jego wyniki są w części [Przykładowe rozwiązania](#przykładowe-rozwiązania), bo zawierają rozwiązanie. Ręcznie wystarczy, że sprawdzisz kilka przypadków, jak opisano wyżej.

</details>

Przykładowe rozwiązanie jest w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 8. Znajdź błąd: pomylony tydzień

To zadanie wykonaj **po misji**: program poniżej zawiera obie funkcje misji. Funkcje działają poprawnie, a program buduje się bez błędów. Odczytuje oba tygodnie z wejścia, tak jak program kontrolny.

<details>
<summary>Program do sprawdzenia: otwórz po napisaniu własnego programu</summary>

<!-- example: weeks_argument_bug -->
```cpp
#include <iostream>
#include <vector>

int total_pages(const std::vector<int>& pages) {
    int total{0};

    for (const int day_pages : pages) {
        total += day_pages;
    }

    return total;
}

int count_goal_days(const std::vector<int>& pages, int goal) {
    int goal_days{0};

    for (const int day_pages : pages) {
        if (day_pages >= goal) {
            ++goal_days;
        }
    }

    return goal_days;
}

int main() {
    std::vector<int> week_a{};
    std::vector<int> week_b{};
    int day_count{0};

    std::cin >> day_count;

    for (int day{1}; day <= day_count; ++day) {
        int day_pages{0};
        std::cin >> day_pages;
        week_a.push_back(day_pages);
    }

    std::cin >> day_count;

    for (int day{1}; day <= day_count; ++day) {
        int day_pages{0};
        std::cin >> day_pages;
        week_b.push_back(day_pages);
    }

    if (std::cin.fail()) {
        std::cout << "Input could not be read\n";
    } else {
        const int daily_goal{10};
        const int pages_a{total_pages(week_a)};
        const int pages_b{total_pages(week_a)};

        std::cout << "Week A pages: " << pages_a << "\n";
        std::cout << "Week A goal days: " << count_goal_days(week_a, daily_goal) << "\n";
        std::cout << "Week B pages: " << pages_b << "\n";
        std::cout << "Week B goal days: " << count_goal_days(week_b, daily_goal) << "\n";

        if (pages_a > pages_b) {
            std::cout << "More pages: Week A\n";
        } else if (pages_b > pages_a) {
            std::cout << "More pages: Week B\n";
        } else {
            std::cout << "More pages: Tie\n";
        }
    }
}
```

1. Przeczytaj wymaganie misji i **przewidź** raport dla dwóch identycznych tygodni `{12, 0, 8, 15, 9}`, czyli dla danych `5`, `12`, `0`, `8`, `15`, `9`, `5`, `12`, `0`, `8`, `15`, `9`.
2. Uruchom program z tymi danymi. Czy raport jest poprawny?
3. Uruchom go z danymi przykładu A: `5`, `12`, `0`, `8`, `15`, `9`, `4`, `5`, `18`, `11`, `16`.
4. Porównaj oba raporty z wymaganiem. Dlaczego pierwszy test nie ujawnia błędu?
5. Znajdź wywołanie z niewłaściwym argumentem.
6. Popraw je.
7. Ponownie porównaj wyniki dla obu zestawów danych.

</details>

Wyniki programu przed poprawką i poprawiony program są w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 9. Gdy coś pójdzie inaczej

| Co widzisz | Co to znaczy | Co zrobić |
|---|---|---|
| `no matching member function for call to 'push_back'` w funkcji | Funkcja próbuje zmienić wektor przez parametr `const&` (punkt 5). | Funkcja do odczytu nie zmienia wektora. Usuń zmianę albo przenieś ją do `main`. |
| `no matching function for call to ...` przy wywołaniu | Liczba albo kolejność argumentów nie pasuje do parametrów. | Porównaj wywołanie z nagłówkiem funkcji: najpierw wektor, potem próg, jeśli tak zapisano parametry. |
| Dzień z dokładnie 10 stronami się nie liczy | Warunek `>` zamiast `>=`. | Sprawdź przypadek F: dla `{10}` wynik to 1. |
| Przy równych sumach program wskazuje tydzień | Zwycięzcę wybiera liczba dni z celem albo brakuje gałęzi remisu. | Sprawdź przypadki C i H: wynik to `Tie`. |
| Oba tygodnie mają te same wyniki, choć dane są różne | Funkcja jest wywołana dwa razy z tym samym wektorem (punkt 8). | Sprawdź argumenty wszystkich wywołań. |
| Suma albo licznik jest za duży przy kolejnym wywołaniu | Akumulator nie jest zmienną lokalną funkcji. | Suma i licznik powinny być zadeklarowane w ciele funkcji, przed pętlą. |

## 10. Wyjaśnij

Odpowiedz własnymi słowami, najlepiej na piśmie. Dopiero potem porównaj z przykładowymi odpowiedziami.

1. Dlaczego funkcja może potrzebować całego wektora jako parametru?
2. Co oznacza `const std::vector<int>&`?
3. Czym to się różni od parametru `int` przekazywanego przez wartość?
4. Czy funkcja z takim parametrem tworzy kopię całego wektora?
5. Czy tę samą funkcję można wywołać dla dwóch różnych wektorów? Czy musi znać ich nazwy z `main`?
6. Czy przez parametr `const&` można wykonać `push_back()`?
7. Czy wektor w `main` musi mieć `const`, żeby przekazać go do takiej funkcji?
8. Czy funkcja z parametrem-wektorem może zwrócić zwykły wynik `int`?
9. Co zwracają funkcje z misji dla pustego wektora i dlaczego?
10. Dlaczego próg przekazujemy jako zwykły `int`?
11. Dlaczego test na dwóch identycznych wektorach może ukryć pomylenie argumentów?

<details>
<summary>Przykładowe odpowiedzi</summary>

1. Bo jej zadanie dotyczy wszystkich wartości kolekcji, na przykład policzenia sumy, a liczba wartości jest różna dla różnych wektorów. Osobny parametr dla każdej wartości nie byłby możliwy.
2. Parametr jest referencją do wektora liczb `int`: odnosi się do wektora z miejsca wywołania, bez kopiowania go, a `const` sprawia, że przez ten parametr wektor można tylko czytać.
3. Parametr `int` dostaje własną kopię wartości argumentu. Parametr `const std::vector<int>&` nie dostaje kopii, tylko odnosi się do istniejącego wektora i pozwala go czytać.
4. Nie. Funkcja odczytuje wektor, który przekazał wywołujący.
5. Tak. Za każdym razem parametr odnosi się do wektora podanego w wywołaniu. Funkcja zna tylko nazwę swojego parametru.
6. Nie. `const` w typie parametru zabrania zmian przez ten parametr, więc kompilator zgłasza błąd.
7. Nie. Można przekazać też wektor bez `const`. Funkcja i tak nie może go zmienić przez swój parametr, ale `main` nadal może go zmieniać.
8. Tak. Typ wyniku nie zależy od typu parametrów: funkcja może przyjąć wektor i zwrócić `int`.
9. 0. Suma i licznik zaczynają od 0, pętla zakresowa dla pustego wektora nie wykonuje żadnego przebiegu, więc funkcje zwracają wartość początkową. Dla sumy i liczby dni to jednoznaczny, sensowny wynik.
10. Bo to jedna mała liczba, której kopia nic nie kosztuje, a funkcja jej nie zmienia. Referencja nie daje tu żadnej korzyści.
11. Bo przy identycznych wektorach wywołanie z niewłaściwym wektorem daje ten sam wynik co z właściwym. Błąd ujawniają dopiero różne dane.

</details>

## Podsumowanie

- Funkcja, która ma przeanalizować cały wektor, dostaje go jako parametr: `int count_cold_days(const std::vector<int>& temperatures)`.
- `&` znaczy, że parametr jest **referencją**: odnosi się do wektora z miejsca wywołania, bez kopiowania go. `const` znaczy, że przez ten parametr wektor można tylko czytać.
- Tę samą funkcję wywołujesz dla różnych wektorów. Funkcja nie zna ich nazw z `main`.
- Pojedyncze liczby, jak próg, nadal przekazujesz przez wartość.
- `const&` ogranicza tylko dostęp przez parametr. Wektor bez `const` w `main` może się nadal zmieniać w `main`.
- Funkcja zwraca wynik, a `main` go wypisuje i porównuje.
- Dla pustego wektora suma i licznik mają naturalny wynik 0. Średnia i maksimum wymagają osobnej decyzji.
- Funkcje sprawdzasz osobno, także na pustym wektorze, a różne dane w testach ujawniają pomylone argumenty.

## Co dalej

Funkcje z tej lekcji zwracały pojedyncze liczby. W kolejnej lekcji funkcja zwróci nowy wektor, na przykład zbudowany z wybranych elementów innego wektora: [Lekcja 6.5: Funkcja tworzy i zwraca nowy wektor](lesson_05_a_function_returns_a_vector.md).

---

## Przykładowe rozwiązania

Zajrzyj tutaj **po własnej próbie**. Twoje nazwy mogą się różnić, jeśli standardowe wyjście jest takie, jak wymagane.

<details>
<summary>Punkt 7: misja, dwa tygodnie czytania</summary>

<!-- example: reading_weeks -->
```cpp
#include <iostream>
#include <vector>

int total_pages(const std::vector<int>& pages) {
    int total{0};

    for (const int day_pages : pages) {
        total += day_pages;
    }

    return total;
}

int count_goal_days(const std::vector<int>& pages, int goal) {
    int goal_days{0};

    for (const int day_pages : pages) {
        if (day_pages >= goal) {
            ++goal_days;
        }
    }

    return goal_days;
}

int main() {
    const std::vector<int> week_a{12, 0, 8, 15, 9};
    const std::vector<int> week_b{5, 18, 11, 16};

    const int daily_goal{10};
    const int pages_a{total_pages(week_a)};
    const int pages_b{total_pages(week_b)};

    std::cout << "Week A pages: " << pages_a << "\n";
    std::cout << "Week A goal days: " << count_goal_days(week_a, daily_goal) << "\n";
    std::cout << "Week B pages: " << pages_b << "\n";
    std::cout << "Week B goal days: " << count_goal_days(week_b, daily_goal) << "\n";

    if (pages_a > pages_b) {
        std::cout << "More pages: Week A\n";
    } else if (pages_b > pages_a) {
        std::cout << "More pages: Week B\n";
    } else {
        std::cout << "More pages: Tie\n";
    }
}
```

1. **Obie funkcje przyjmują `const&`**, bo tylko czytają tydzień: nie potrzebują jego kopii i nie mają go zmieniać.
2. **Próg `goal` idzie przez wartość**: to jedna liczba `int`, a funkcja jej nie zmienia.
3. **Funkcje działają dla obu tygodni**, bo nie zależą od nazw z `main`. Parametr `pages` odnosi się za każdym razem do wektora z wywołania: raz do `week_a`, raz do `week_b`.
4. **Jedna implementacja wystarczy:** pętla sumująca i pętla licząca stoją w kodzie po razie. Zmiana reguły, na przykład progu z `>=` na inny warunek, wymaga zmiany w jednym miejscu.
5. **Pusty wektor:** `total` i `goal_days` zaczynają od 0, a pętla nie wykonuje żadnego przebiegu, więc obie funkcje zwracają 0. Dla sumy i liczby dni to właściwy wynik.
6. **Wybór tygodnia należy do `main`**, bo to decyzja o raporcie, która potrzebuje wyników obu tygodni. Funkcje obliczeniowe wiedzą tylko o jednym wektorze naraz.
7. `main` zapamiętuje sumy w `pages_a` i `pages_b`, bo potrzebuje ich dwa razy: do wypisania i do porównania. Liczby dni z celem wypisuje od razu.

To jeden z możliwych podziałów. Poprawne jest też na przykład zapamiętanie wszystkich czterech wyników w zmiennych albo inna kolejność parametrów funkcji z progiem, jeśli wywołania jej odpowiadają.

**Program kontrolny** sprawdza wszystkie przypadki z listy kontrolnej. Funkcje są te same co wyżej, a część `main` od `const int daily_goal{10};` jest taka sama, poza wcięciem. Różni się źródło danych: oba tygodnie są odczytywane z wejścia przez `push_back`, jak w lekcji 6.2, więc wektory nie mają `const`. Program nie wypisuje pytań, więc jego standardowe wyjście jest takie jak wynik misji.

<!-- example: reading_weeks_check -->
```cpp
#include <iostream>
#include <vector>

int total_pages(const std::vector<int>& pages) {
    int total{0};

    for (const int day_pages : pages) {
        total += day_pages;
    }

    return total;
}

int count_goal_days(const std::vector<int>& pages, int goal) {
    int goal_days{0};

    for (const int day_pages : pages) {
        if (day_pages >= goal) {
            ++goal_days;
        }
    }

    return goal_days;
}

int main() {
    std::vector<int> week_a{};
    std::vector<int> week_b{};
    int day_count{0};

    std::cin >> day_count;

    for (int day{1}; day <= day_count; ++day) {
        int day_pages{0};
        std::cin >> day_pages;
        week_a.push_back(day_pages);
    }

    std::cin >> day_count;

    for (int day{1}; day <= day_count; ++day) {
        int day_pages{0};
        std::cin >> day_pages;
        week_b.push_back(day_pages);
    }

    if (std::cin.fail()) {
        std::cout << "Input could not be read\n";
    } else {
        const int daily_goal{10};
        const int pages_a{total_pages(week_a)};
        const int pages_b{total_pages(week_b)};

        std::cout << "Week A pages: " << pages_a << "\n";
        std::cout << "Week A goal days: " << count_goal_days(week_a, daily_goal) << "\n";
        std::cout << "Week B pages: " << pages_b << "\n";
        std::cout << "Week B goal days: " << count_goal_days(week_b, daily_goal) << "\n";

        if (pages_a > pages_b) {
            std::cout << "More pages: Week A\n";
        } else if (pages_b > pages_a) {
            std::cout << "More pages: Week B\n";
        } else {
            std::cout << "More pages: Tie\n";
        }
    }
}
```

Dane wejściowe to liczba dni i strony tygodnia A, potem liczba dni i strony tygodnia B. Przypadki są w kolejności z listy kontrolnej, od A do I.

<!-- input: reading_weeks_check -->
```text
5
12
0
8
15
9
4
5
18
11
16
```

<!-- output: reading_weeks_check -->
```text
Week A pages: 44
Week A goal days: 2
Week B pages: 50
Week B goal days: 3
More pages: Week B
```

<!-- input: reading_weeks_check -->
```text
2
20
10
2
5
0
```

<!-- output: reading_weeks_check -->
```text
Week A pages: 30
Week A goal days: 2
Week B pages: 5
Week B goal days: 0
More pages: Week A
```

<!-- input: reading_weeks_check -->
```text
2
20
0
2
10
10
```

<!-- output: reading_weeks_check -->
```text
Week A pages: 20
Week A goal days: 1
Week B pages: 20
Week B goal days: 2
More pages: Tie
```

<!-- input: reading_weeks_check -->
```text
0
0
```

<!-- output: reading_weeks_check -->
```text
Week A pages: 0
Week A goal days: 0
Week B pages: 0
Week B goal days: 0
More pages: Tie
```

<!-- input: reading_weeks_check -->
```text
0
1
10
```

<!-- output: reading_weeks_check -->
```text
Week A pages: 0
Week A goal days: 0
Week B pages: 10
Week B goal days: 1
More pages: Week B
```

<!-- input: reading_weeks_check -->
```text
1
9
1
10
```

<!-- output: reading_weeks_check -->
```text
Week A pages: 9
Week A goal days: 0
Week B pages: 10
Week B goal days: 1
More pages: Week B
```

<!-- input: reading_weeks_check -->
```text
2
9
9
1
8
```

<!-- output: reading_weeks_check -->
```text
Week A pages: 18
Week A goal days: 0
Week B pages: 8
Week B goal days: 0
More pages: Week A
```

<!-- input: reading_weeks_check -->
```text
3
10
10
10
1
30
```

<!-- output: reading_weeks_check -->
```text
Week A pages: 30
Week A goal days: 3
Week B pages: 30
Week B goal days: 1
More pages: Tie
```

<!-- input: reading_weeks_check -->
```text
5
12
0
8
15
9
5
12
0
8
15
9
```

<!-- output: reading_weeks_check -->
```text
Week A pages: 44
Week A goal days: 2
Week B pages: 44
Week B goal days: 2
More pages: Tie
```

</details>

<details>
<summary>Punkt 8: wyniki przed poprawką i poprawiony program</summary>

Przed poprawką, dla dwóch identycznych tygodni:

<!-- input: weeks_argument_bug -->
```text
5
12
0
8
15
9
5
12
0
8
15
9
```

<!-- output: weeks_argument_bug -->
```text
Week A pages: 44
Week A goal days: 2
Week B pages: 44
Week B goal days: 2
More pages: Tie
```

Dla danych przykładu A:

<!-- input: weeks_argument_bug -->
```text
5
12
0
8
15
9
4
5
18
11
16
```

<!-- output: weeks_argument_bug -->
```text
Week A pages: 44
Week A goal days: 2
Week B pages: 44
Week B goal days: 3
More pages: Tie
```

- Dla identycznych tygodni raport jest poprawny: suma tygodnia B jest liczona z tygodnia A, ale oba tygodnie mają te same dane, więc wynik wychodzi taki sam.
- Dla przykładu A tydzień B ma 50 stron, a program wypisuje 44 i ogłasza remis. Liczba dni z celem dla B, 3, jest poprawna, bo to wywołanie dostaje właściwy wektor.
- **Przyczyna:** `const int pages_b{total_pages(week_a)};`. Argument to `week_a`, a powinien być `week_b`. Kompilator tego nie wykryje: oba wektory mają ten sam typ, więc wywołanie jest poprawnym C++. To błąd logiki.
- **Poprawka:** `const int pages_b{total_pages(week_b)};`.

Poprawiony program to program kontrolny z punktu 7: różni się od programu z błędem tylko tym argumentem. Dla obu zestawów danych daje wyniki z listy kontrolnej: przypadek I (identyczne tygodnie) i przypadek A (`More pages: Week B`).

</details>

**Poprzednia lekcja:** [Lekcja 6.3: Pozycje elementów i sąsiednie wartości w `std::vector`](lesson_03_positions_and_neighbours.md) · **Następna lekcja:** [Lekcja 6.5: Funkcja tworzy i zwraca nowy wektor](lesson_05_a_function_returns_a_vector.md) · [Opis kursu](../../README.md)

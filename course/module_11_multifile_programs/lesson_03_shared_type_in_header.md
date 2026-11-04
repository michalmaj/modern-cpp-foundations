# Lekcja 11.3: Wspólny typ w nagłówku

**Polski** · [English](lesson_03_shared_type_in_header.en.md) · [Opis kursu](../../README.md)

> **Moduł 11, lekcja 3** · około 85–105 minut, możesz ją podzielić na dwa podejścia: punkty 1–6 i punkty 7–11
> **Potrzebujesz:** katalogu `cpp-workspace` z projektami `lesson_11_2` i `ticket_cost_header` z [lekcji 11.2](lesson_02_own_header_file.md). Debugger nie jest w tej lekcji potrzebny.
> **Wersja pilotażowa.** Programy z tej lekcji, zbudowane z kilku plików, sprawdzamy automatycznie na Windowsie, Ubuntu i macOS, z podanymi danymi wejściowymi, razem z błędami kompilacji z punktów 8 i 9. Kroki w CLionie opisujemy według dokumentacji CLion 2026.2, bez ręcznego sprawdzenia na każdym systemie.

## Zanim zaczniesz

Ta lekcja zakłada, że:

- definiujesz własny typ przez `struct`, tworzysz rekord z wartościami w `{}` i korzystasz z jego pól operatorem kropki (lekcje 8.1 i 8.2);
- przekazujesz rekord, który funkcja tylko odczytuje, przez `const&` (lekcja 8.3);
- budujesz program z dwóch plików `.cpp` i własnego nagłówka z `#pragma once` (lekcje 11.1 i 11.2).

## Sytuacja

W lekcji 11.2 funkcja `calculate_points` dostawała dwie osobne liczby. Liczba zadań i premia opisują jednak razem jeden wynik, a takie dane w Module 8 łączyliśmy w rekord. Tylko że w Module 8 typ, funkcje i `main` stały w jednym pliku. Teraz rekord tworzy `main.cpp`, a jego pola odczytuje funkcja z `points.cpp`, więc **oba pliki muszą znać ten sam typ**. W tej lekcji umieścisz jego definicję we wspólnym nagłówku.

Po tej lekcji będziesz:

- umieszczać definicję własnego typu w nagłówku, razem z deklaracją funkcji, która z niego korzysta;
- tworzyć rekord w `main.cpp` i przekazywać go przez `const&` do funkcji z innego pliku `.cpp`;
- wyjaśniać, przed czym chroni `#pragma once`, gdy nagłówek zawiera definicję typu;
- rozpoznawać błąd ponownej definicji typu i nagłówek, który nie dołącza potrzebnego mu typu.

## 1. Przygotuj projekt

W `cpp-workspace` utwórz katalog `lesson_11_3` i skopiuj do niego z `lesson_11_2` cztery pliki: `main.cpp`, `points.hpp`, `points.cpp` i `CMakeLists.txt`. Katalogów budowania nie kopiuj. Otwórz katalog w CLionie albo przejdź do niego w terminalu, jak w lekcji 11.1, punkt 1. W punktach 2 i 3 zmienisz trzy pliki z kodem. `CMakeLists.txt` zostaje bez zmian.

## 2. Typ w nagłówku

Dopisz do `points.hpp` definicję typu `TaskResult` i zmień deklarację funkcji tak, żeby przyjmowała rekord:

**`points.hpp`**:

<!-- file: points points.hpp -->
```cpp
#pragma once

struct TaskResult {
    int solved;
    int bonus;
};

int calculate_points(const TaskResult& result);
```

- **`TaskResult` to nazwa typu,** zdefiniowanego jak typy z Modułu 8. Każdy rekord tego typu ma dwa pola: liczbę rozwiązanych zadań i premię. Sama definicja nie tworzy żadnego rekordu.
- **Definicja typu stoi przed deklaracją funkcji,** bo funkcja korzysta z typu w swoim parametrze, jak w lekcji 8.3.
- **`const TaskResult& result`:** funkcja odczytuje istniejący rekord, bez kopii i bez możliwości zmiany jego pól (lekcja 8.3).
- **Nagłówek zawiera teraz definicję typu i deklarację funkcji.** Razem to wspólna informacja dla obu plików `.cpp`: jak wygląda rekord i jak wywołać funkcję.

Dlaczego w nagłówku jest pełna **definicja** typu, a nie sama deklaracja, jak przy funkcji? Plik, który tworzy rekord albo odczytuje jego pola, musi wiedzieć, z jakich pól rekord się składa. Wywołanie funkcji z innego pliku łączy linker (lekcja 11.1), ale pól typu żaden linker nie dopisze: kompilator potrzebuje ich w każdym pliku `.cpp`, który z nich korzysta. Dlatego definicja typu może stać w nagłówku dołączanym przez kilka plików `.cpp`. **Definicja zwykłej funkcji nadal zostaje w pliku `.cpp`** (lekcja 11.2, punkt 2).

## 3. `main.cpp` i `points.cpp` korzystają z typu

`main.cpp` tworzy rekord, wpisuje do jego pól odczytane liczby i przekazuje go funkcji:

**`main.cpp`**:

<!-- example: points -->
```cpp
#include <iostream>

#include "points.hpp"

int main() {
    TaskResult result{0, 0};

    std::cin >> result.solved;
    std::cin >> result.bonus;

    std::cout << "Points: " << calculate_points(result) << "\n";
}
```

| Zapis | Co robi |
|---|---|
| `#include "points.hpp"` | daje `main.cpp` definicję `TaskResult` i deklarację `calculate_points` |
| `TaskResult result{0, 0};` | tworzy rekord z wartościami początkowymi obu pól, tak jak `int solved{0};` w lekcji 11.2 |
| `std::cin >> result.solved;` | zapisuje odczytaną liczbę w polu `solved` tego rekordu |
| `calculate_points(result)` | przekazuje funkcji cały rekord, zamiast dwóch liczb |

- **`result` nie ma `const`,** bo `>>` zapisuje w jego polach. Pole obiektu bez `const` może być celem `>>`, tak jak zmienna, podobnie jak w lekcji 8.2 zmieniało się przez `=`.
- **W Module 10 rekord powstawał dopiero po sprawdzeniu danych.** Ten program, jak programy z lekcji 11.1 i 11.2, danych nie sprawdza, więc wystarczy odczyt prosto do pól.

Definicja funkcji w `points.cpp` dostaje nowy parametr. Obliczenie się nie zmienia:

**`points.cpp`**:

<!-- file: points points.cpp -->
```cpp
#include "points.hpp"

int calculate_points(const TaskResult& result) {
    const int points_per_task{3};
    return result.solved * points_per_task + result.bonus;
}
```

- **`points.cpp` też dołącza `points.hpp`,** bo żeby odczytać `result.solved`, musi znać pola `TaskResult`. Deklaracja i definicja funkcji znowu stoją w jednej jednostce translacji.
- **W `points.cpp` nie ma drugiej definicji `TaskResult`.** Typ jest zdefiniowany tylko w nagłówku.
- **Wspólna jest definicja typu, a nie jeden obiekt.** Rekord `result` powstaje w `main` i tylko tam istnieje. `points.cpp` nie ma własnego rekordu: funkcja przez `const&` odczytuje ten, który dostała w wywołaniu. Gdyby inny plik utworzył własny rekord `TaskResult`, byłby to osobny obiekt, jak `first` i `second` w lekcji 8.1.

| | Moduł 8 | Ta lekcja |
|---|---|---|
| definicja typu | w `main.cpp`, nad funkcjami | w `points.hpp` |
| funkcja z parametrem `const&` | w tym samym pliku co `main` | w `points.cpp` |
| tworzenie rekordu | w `main` | w `main`, w `main.cpp` |
| które pliki znają typ | jeden plik | każdy plik, który dołącza nagłówek |

Sama struktura działa tak jak w Module 8: nagłówek zmienia tylko miejsce jej definicji.

## 4. Jedna definicja typu, a nie dwie kopie

Typ można by przecież zdefiniować osobno w `main.cpp` i w `points.cpp`, kopiując te same linijki. Wtedy trzeba by ręcznie pilnować, żeby obie kopie były zawsze takie same. Wyobraź sobie, że rekord dostaje trzecie pole, a ktoś dopisze je tylko w jednej kopii. Każdy plik `.cpp` kompiluje się osobno, więc kompilator `main.cpp` nie widzi kopii z `points.cpp` i nie musi zauważyć różnicy. Taki projekt łatwo zepsuć.

Wspólny nagłówek usuwa ten problem: **typ jest zdefiniowany w jednym miejscu,** oba pliki `.cpp` dołączają ten nagłówek i każdy z nich dostaje dokładnie tę samą definicję. Zmiana typu to zmiana jednego pliku.

## 5. `#pragma once` przy definicji typu

W lekcji 11.2 nagłówek zawierał tylko deklarację funkcji. Zgodną deklarację można powtórzyć, więc `#pragma once` nie był tam potrzebny do kompilacji. **Z definicją typu jest inaczej:** w jednej jednostce translacji `struct TaskResult` może być zdefiniowany tylko raz.

```text
main.cpp:    #include "points.hpp"   ──►  TaskResult raz  ┐  dwie osobne jednostki translacji:
points.cpp:  #include "points.hpp"   ──►  TaskResult raz  ┘  poprawnie

main.cpp:    #include "points.hpp"   ──►  bez #pragma once TaskResult dwa razy
             #include "points.hpp"        w jednej jednostce translacji: błąd
```

- **Dwa pliki `.cpp`, z których każdy dołącza `points.hpp`, to nie powtórzona definicja.** Każdy plik `.cpp` jest osobno przygotowywany i kompilowany, więc każdy dostaje typ raz.
- **Ten sam nagłówek dwa razy w jednym pliku `.cpp`** to już dwie definicje w jednej jednostce translacji. Może się to zdarzyć przez przypadek, na przykład przez skopiowaną linijkę `#include` albo przez nagłówek, który sam dołącza `points.hpp` (punkt 9).
- **`#pragma once` sprawia, że drugie dołączenie zostaje pominięte,** więc definicja trafia do jednostki translacji raz. Nie dotyczy to dołączania w różnych plikach `.cpp` i nie zastępuje linkowania.

Jak taki błąd wygląda, zobaczysz w punkcie 8.

## 6. Zbuduj i uruchom

`CMakeLists.txt` się nie zmienia:

<!-- cmake: points -->
```cmake
cmake_minimum_required(VERSION 3.28)
project(first_program LANGUAGES CXX)

add_executable(first_program main.cpp points.cpp)
target_compile_features(first_program PRIVATE cxx_std_20)
set_target_properties(first_program PROPERTIES CXX_EXTENSIONS OFF)
```

Nagłówek, także z definicją typu, kompiluje się jako część plików `.cpp`, które go dołączają, i nie powstaje z niego osobny plik obiektowy. Dlatego w projekcie z tego kursu `add_executable` nadal wymienia tylko pliki `.cpp`. To zasada naszego prostego projektu, a nie reguła CMake (lekcja 11.2, punkt 5).

Zbuduj i uruchom program jak w lekcji 11.1, punkt 5. Dla danych:

<!-- input: points -->
```text
4 2
```

program wypisuje:

<!-- output: points -->
```text
Points: 14
```

**Przewidź** wyniki dla `0 5` i `3 0`. Uruchomienie jest nieobowiązkowe.

<!-- input: points -->
```text
0 5
```

<details>
<summary>Standardowe wyjście dla 0 5</summary>

<!-- output: points -->
```text
Points: 5
```

</details>

<!-- input: points -->
```text
3 0
```

<details>
<summary>Standardowe wyjście dla 3 0</summary>

<!-- output: points -->
```text
Points: 9
```

</details>

Wyniki `14` i `5` są takie same jak w lekcjach 11.1 i 11.2. **Rekord zamiast dwóch argumentów i typ w nagłówku zmieniają organizację danych i wygląd funkcji, a nie regułę obliczeń.** Program nie działa przez to szybciej.

## 7. Misja: zamówienie biletów jako rekord

Zaprojektuj dane programu z biletami jako rekord. W `cpp-workspace` utwórz katalog `ticket_order` i skopiuj do niego cztery pliki z projektu `ticket_cost_header` z lekcji 11.2: `main.cpp`, nagłówek, drugi plik `.cpp` i `CMakeLists.txt`. Oryginał zostaw bez zmian: posłuży do porównania wyników. Jeśli nie masz tego projektu, odtwórz go z [rozwiązania misji z lekcji 11.2](lesson_02_own_header_file.md#przykładowe-rozwiązania).

**Wymagania:**

- Bilet zwykły kosztuje 12 jednostek, ulgowy 7. Program odczytuje dwie liczby: liczbę biletów zwykłych i ulgowych.
- **Obie liczby trafiają do pól jednego rekordu** Twojego własnego typu, zdefiniowanego **tylko** w nagłówku, z `#pragma once` w pierwszej linijce.
- Funkcja dostaje ten rekord przez `const&` i zwraca łączny koszt. Jej deklaracja stoi w nagłówku, a definicja w drugim pliku `.cpp`.
- **Oba pliki `.cpp` dołączają nagłówek.** Żaden plik `.cpp` nie definiuje typu drugi raz.
- `main` tworzy rekord, odczytuje dane do jego pól, wywołuje funkcję i wypisuje `Total cost: N`.
- `add_executable` wymienia dwa pliki `.cpp`, a reszta `CMakeLists.txt` się nie zmienia.
- Nazwy plików możesz zachować z lekcji 11.2. Typ nazwij od wielkiej litery, a pola i funkcję w `snake_case`, jak dotąd w kursie.
- Dane są nieujemne i niewielkie. Nie dodawaj sprawdzania danych ani nowych rodzajów biletów.

Wyniki mają być takie same jak w lekcji 11.2. **Dane A:**

<!-- input: tickets -->
```text
2 3
```

<!-- output: tickets -->
```text
Total cost: 45
```

**Dane B:**

<!-- input: tickets -->
```text
0 4
```

<!-- output: tickets -->
```text
Total cost: 28
```

**Dane C:**

<!-- input: tickets -->
```text
0 0
```

<!-- output: tickets -->
```text
Total cost: 0
```

**Przewidź D:** `3 0`, same bilety zwykłe.

<!-- input: tickets -->
```text
3 0
```

<details>
<summary>Standardowe wyjście dla danych D</summary>

<!-- output: tickets -->
```text
Total cost: 36
```

</details>

**Zdecyduj samodzielnie:**

1. jak nazwać własny typ;
2. jakie pola ma mieć i jakiego typu;
3. gdzie zdefiniować typ;
4. jak nazwać nagłówek;
5. jak nazwać funkcję;
6. jak zapisać jej deklarację z `const&`;
7. jak zapisać jej definicję;
8. gdzie stoją linijki `#include` z nazwą nagłówka;
9. jak w `main` utworzyć rekord i wypełnić jego pola;
10. jak porównać wyniki z projektem z lekcji 11.2.

**Potem** zbuduj program i uruchom go dla danych A i jednego przypadku granicznego: B albo C. Porównaj wyniki z projektem `ticket_cost_header` dla tych samych danych. Pozostałe przypadki przewidź. Wszystkie są sprawdzone automatycznie w rozwiązaniu referencyjnym.

### Kryterium sukcesu

- Program buduje się jako C++20, a dla danych A oraz B albo C wypisuje dokładnie pokazany wynik, ten sam co projekt z lekcji 11.2.
- Nagłówek zaczyna się od `#pragma once` i zawiera definicję typu oraz deklarację funkcji z parametrem `const&`.
- Typ jest zdefiniowany tylko w nagłówku: ani `main.cpp`, ani drugi plik `.cpp` nie zawierają jego kopii.
- Oba pliki `.cpp` dołączają nagłówek, a drugi plik `.cpp` zawiera jedyną definicję funkcji, zgodną z deklaracją.
- `main` tworzy rekord, wpisuje dane do jego pól i przekazuje go funkcji.
- `add_executable` wymienia dwa pliki `.cpp`, bez nagłówka.

Poprawne wyniki nie dowodzą, że pliki są dobrze zorganizowane: kopia typu albo deklaracji w niewłaściwym pliku czasem też by się zbudowała. Dlatego sprawdź pliki według listy powyżej. Twoje nazwy mogą być inne niż w rozwiązaniu referencyjnym.

<details>
<summary>Podpowiedź 1</summary>

Kto musi znać definicję typu? `main.cpp` tworzy rekord i wpisuje dane do jego pól, a drugi plik `.cpp` odczytuje te pola w funkcji.

</details>

<details>
<summary>Podpowiedź 2</summary>

W którym pliku najlepiej zdefiniować ten typ, żeby nie powielać kodu? Plik ten dołączają już oba pliki `.cpp`.

</details>

<details>
<summary>Podpowiedź 3</summary>

Co powinny dołączać oba pliki `.cpp` i jak wygląda deklaracja funkcji z `const&`? Pomyśl o `calculate_points` z punktu 2: typ wyniku, nazwa funkcji, a w nawiasie `const`, nazwa typu, `&` i nazwa parametru.

</details>

Przykładowe rozwiązanie jest w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 8. Znajdź błąd: typ zdefiniowany dwa razy

To zadanie wykonaj **po misji**. Ktoś usunął z `points.hpp` linijkę `#pragma once`, uznając ją za zbędną, a w `main.cpp` przez przypadek skopiował linijkę `#include "points.hpp"`. Odtwórz ten projekt: w `cpp-workspace` utwórz katalog `points_twice_check`, skopiuj do niego cztery pliki z `lesson_11_3` i wprowadź obie zmiany. `points.cpp` i `CMakeLists.txt` zostają takie jak w punktach 3 i 6.

**`points.hpp`** w tym projekcie, bez `#pragma once`:

<!-- file: points_twice_check points.hpp -->
```cpp
struct TaskResult {
    int solved;
    int bonus;
};

int calculate_points(const TaskResult& result);
```

**`main.cpp`** w tym projekcie:

<!-- broken: points_twice_check in=points.hpp at=1:8 errors=1 error=^redefinition of 'TaskResult'$ -->
```cpp
#include <iostream>

#include "points.hpp"
#include "points.hpp"

int main() {
    TaskResult result{0, 0};

    std::cin >> result.solved;
    std::cin >> result.bonus;

    std::cout << "Points: " << calculate_points(result) << "\n";
}
```

<details>
<summary>Pozostałe pliki, bez zmian względem punktów 3 i 6</summary>

**`points.cpp`**:

<!-- file: points_twice_check points.cpp -->
```cpp
#include "points.hpp"

int calculate_points(const TaskResult& result) {
    const int points_per_task{3};
    return result.solved * points_per_task + result.bonus;
}
```

**`CMakeLists.txt`**:

<!-- cmake: points_twice_check -->
```cmake
cmake_minimum_required(VERSION 3.28)
project(first_program LANGUAGES CXX)

add_executable(first_program main.cpp points.cpp)
target_compile_features(first_program PRIVATE cxx_std_20)
set_target_properties(first_program PROPERTIES CXX_EXTENSIONS OFF)
```

</details>

**Zanim zbudujesz**, odpowiedz na piśmie:

1. **Przewidź:** na którym etapie budowanie się nie uda, kompilacji czy linkowania?
2. Czy obie definicje `TaskResult` pochodzą z dwóch różnych plików `.cpp`?
3. Ile razy treść `points.hpp` trafia do jednostki translacji `main.cpp`?
4. Jaka definicja pojawia się w niej dwa razy?

**Potem:**

5. Zbuduj projekt. Skonfiguruj go jak nowy projekt w lekcji 11.1, punkt 5.
6. Przeczytaj wynik budowania, w oknie **Build** albo w terminalu. Który plik `.cpp` się kompilował, w którym pliku i której linijce jest błąd?
7. Dopisz `#pragma once` w pierwszej linijce `points.hpp`. **Oba** `#include` w `main.cpp` na razie zostaw.
8. Zbuduj projekt ponownie i uruchom go dla `4 2`.
9. Usuń powtórzoną linijkę `#include "points.hpp"` z `main.cpp`: nie jest potrzebna, a utrudnia czytanie.
10. Wyjaśnij, dlaczego w lekcji 11.2 powtórzona deklaracja funkcji nie dawała takiego błędu.

<details>
<summary>Co się dzieje i dlaczego: otwórz po zbudowaniu błędnego projektu</summary>

1. **To błąd kompilacji, a nie linkowania.** Nie udaje się kompilacja `main.cpp`, więc do linkowania nie dochodzi. Zmiana `CMakeLists.txt` niczego tu nie naprawi: oba pliki `.cpp` są w `add_executable`, a błąd tkwi w treści jednego z nich.
2. **Komunikat wskazuje nagłówek,** choć kompiluje się `main.cpp`. W wyniku budowania wygląda to mniej więcej tak (ścieżki skrócone):

   ```text
   In file included from main.cpp:4:
   points.hpp:1:8: error: redefinition of 'TaskResult'
   main.cpp:3:10: note: 'points.hpp' included multiple times, additional include site here
   main.cpp:4:10: note: 'points.hpp' included multiple times, additional include site here
   points.hpp:1:8: note: unguarded header; consider using #ifdef guards or #pragma once
   ```

   Pierwsza linijka mówi, **skąd** nagłówek przyszedł: z linijki 4 `main.cpp`. Druga mówi, **gdzie** jest błąd: w `points.hpp`, w linijce 1, w kolumnie 8, przy nazwie `TaskResult`. Linijki z `note:` to wskazówki: pokazują obie linijki `#include` i podpowiadają ochronę nagłówka. Wymieniają też strażniki nagłówka z `#ifdef`, a w tym kursie stosujemy `#pragma once`. Na Windowsie i na innych systemach ścieżki wyglądają inaczej, a treść błędu jest ta sama.
3. **Obie definicje pochodzą z tego samego nagłówka, w jednej jednostce translacji.** Dwa `#include` wstawiają treść `points.hpp` do `main.cpp` dwa razy, więc kompilator widzi `struct TaskResult` dwa razy w jednym pliku. `points.cpp` dołącza nagłówek raz i sam w sobie jest poprawny.
4. **Deklaracja funkcji też stoi w nagłówku dwa razy, ale tu nie przeszkadza:** zgodną deklarację wolno powtórzyć. Dwóch definicji typu w jednej jednostce translacji powtórzyć nie wolno. Dlatego w lekcji 11.2 błędu nie było.
5. **Po dopisaniu `#pragma once`** drugie dołączenie zostaje pominięte, więc program buduje się nawet z dwoma `#include`. Wypisuje `Points: 14`, tak jak w punkcie 6: `#pragma once` nie zmienia działania funkcji. Powtórzonej linijki nie zostawiaj jednak w kodzie, bo tylko utrudnia czytanie.

</details>

Poprawiony projekt jest w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 9. Na papierze: nagłówek, który nie dołącza swojego typu

To zadanie jest **nieobowiązkowe** i nie wymaga uruchamiania. Projekt z kalkulatorem rośnie i typ dostaje osobny nagłówek `task_result.hpp`, bo w przyszłości będą z niego korzystać też inne nagłówki. `points.hpp` zawiera teraz tylko deklarację funkcji:

**`task_result.hpp`**:

<!-- file: points_order_check task_result.hpp -->
```cpp
#pragma once

struct TaskResult {
    int solved;
    int bonus;
};
```

**`points.hpp`**:

<!-- file: points_order_check points.hpp -->
```cpp
#pragma once

int calculate_points(const TaskResult& result);
```

`main.cpp` dołącza najpierw `"task_result.hpp"`, a potem `"points.hpp"`. `points.cpp` dołącza tylko `"points.hpp"`. `add_executable` wymienia oba pliki `.cpp`.

**Odpowiedz:** który plik `.cpp` się skompiluje, który nie i w którym pliku kompilator wskaże błąd? Jak go poprawić, nie dopisując nowych linijek `#include` w plikach `.cpp`?

<details>
<summary>Odpowiedź</summary>

- **`main.cpp` się kompiluje, ale tylko przez przypadek.** Dołącza `task_result.hpp` przed `points.hpp`, więc gdy kompilator dochodzi do deklaracji funkcji, zna już `TaskResult`.
- **`points.cpp` się nie kompiluje.** Dołącza tylko `points.hpp`, w którym `TaskResult` jest nieznany. Błąd jest w nagłówku: `points.hpp:3:28: error: unknown type name 'TaskResult'`, a zaraz po nim ten sam błąd w definicji funkcji w `points.cpp`.
- **Poprawka:** `points.hpp` sam dołącza nagłówek z typem, którego używa: `#include "task_result.hpp"` pod `#pragma once`. Wtedy każdy plik, który dołącza `points.hpp`, dostaje też `TaskResult`, niezależnie od kolejności swoich `#include`.
- **Dopisywanie kolejnych `#include` w plikach `.cpp` nie jest poprawką,** bo `points.hpp` nadal zależałby od tego, co ktoś dołączył przed nim.
- **`main.cpp` dostaje teraz `task_result.hpp` dwa razy:** bezpośrednio i przez `points.hpp`. Dzięki `#pragma once` w `task_result.hpp` typ trafia do tej jednostki translacji raz. To ta sama ochrona co w punkcie 8.

Taką zasadę nazywamy **samowystarczalnością nagłówka**: nagłówek sam dołącza nagłówki, których potrzebuje do swoich deklaracji.

</details>

<details>
<summary>Pełny błędny projekt, sprawdzony automatycznie (nieobowiązkowy)</summary>

**`main.cpp`**:

<!-- broken: points_order_check in=points.hpp at=3:28 errors=1 error=^unknown type name 'TaskResult'$ -->
```cpp
#include <iostream>

#include "task_result.hpp"
#include "points.hpp"

int main() {
    TaskResult result{0, 0};

    std::cin >> result.solved;
    std::cin >> result.bonus;

    std::cout << "Points: " << calculate_points(result) << "\n";
}
```

**`points.cpp`**:

<!-- file: points_order_check points.cpp -->
```cpp
#include "points.hpp"

int calculate_points(const TaskResult& result) {
    const int points_per_task{3};
    return result.solved * points_per_task + result.bonus;
}
```

**`CMakeLists.txt`**:

<!-- cmake: points_order_check -->
```cmake
cmake_minimum_required(VERSION 3.28)
project(first_program LANGUAGES CXX)

add_executable(first_program main.cpp points.cpp)
target_compile_features(first_program PRIVATE cxx_std_20)
set_target_properties(first_program PROPERTIES CXX_EXTENSIONS OFF)
```

</details>

Poprawiony projekt jest w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 10. Gdy coś pójdzie inaczej

| Co widzisz | Co to znaczy | Co zrobić |
|---|---|---|
| `redefinition of 'TaskResult'` wskazujące nagłówek | Nagłówek bez `#pragma once` trafił do jednego pliku `.cpp` dwa razy (punkt 8). | Dopisz `#pragma once` w pierwszej linijce nagłówka i usuń powtórzone `#include`. |
| `redefinition of 'TaskResult'`, choć nagłówek ma `#pragma once` | W którymś pliku `.cpp` została ręcznie zapisana druga definicja typu. | Usuń kopię. Typ definiuje tylko nagłówek. |
| `unknown type name 'TaskResult'` w pliku `.cpp` | Plik nie dołącza nagłówka z typem albo dołącza go poniżej miejsca, w którym typu używa. | Dopisz `#include "points.hpp"` na początku pliku. |
| `unknown type name 'TaskResult'` w nagłówku | Nagłówek używa typu z innego nagłówka, którego sam nie dołącza (punkt 9). | Dopisz brakujący `#include` w tym nagłówku. |
| `no member named 'solve' in 'TaskResult'` | Nazwa pola różni się od tej z definicji typu. | Porównaj nazwę z definicją w nagłówku. |
| `no matching function for call to 'calculate_points'` | `main` wywołuje funkcję po staremu, z dwiema liczbami, a deklaracja przyjmuje rekord. | Przekaż funkcji rekord: `calculate_points(result)`. |
| Błąd linkowania z nazwą `calculate_points`, choć oba pliki `.cpp` są w `add_executable` | Definicja w `points.cpp` ma inne parametry niż deklaracja, na przykład nadal dwie liczby. | Zmień parametr definicji na `const TaskResult& result`, jak w nagłówku. |

## 11. Wyjaśnij

Odpowiedz własnymi słowami, najlepiej na piśmie. Dopiero potem porównaj z przykładowymi odpowiedziami.

1. Co jest teraz w `points.hpp`, a co w `points.cpp`? Czy `points.hpp` trafia do `add_executable`?
2. Dlaczego definicja `TaskResult` stoi w nagłówku, a nie w jednym z plików `.cpp`?
3. Dlaczego nie kopiujemy definicji typu do obu plików `.cpp`?
4. Czym jest `TaskResult`, a czym `result`? Czy `points.cpp` ma dostęp do jakiegoś wspólnego, globalnego rekordu?
5. Co daje parametr `const TaskResult& result`?
6. Dlaczego `points.hpp` dołączają oba pliki `.cpp`?
7. Co robi `#pragma once` i dlaczego przy definicji typu ma większe znaczenie niż w lekcji 11.2?
8. Czy to, że `main.cpp` i `points.cpp` dołączają `points.hpp`, jest powtórzeniem definicji? A dwa takie same `#include` w jednym pliku `.cpp`?
9. Czy `redefinition of 'TaskResult'` to błąd kompilacji, czy linkowania? Czym różni się od błędu z lekcji 11.2, punkt 8?
10. Co znaczy, że nagłówek jest samowystarczalny?

<details>
<summary>Przykładowe odpowiedzi</summary>

1. W `points.hpp` jest `#pragma once`, definicja typu `TaskResult` i deklaracja `calculate_points`. W `points.cpp` jest `#include "points.hpp"` i definicja funkcji. `add_executable` wymienia tylko `main.cpp` i `points.cpp`: nagłówek kompiluje się jako ich część.
2. Bo potrzebują jej dwa pliki: `main.cpp` tworzy rekord i wpisuje dane do jego pól, a `points.cpp` odczytuje te pola. Każdy z nich musi znać pola typu, a nagłówek daje im tę samą definicję.
3. Bo dwie kopie trzeba by ręcznie utrzymywać takie same. Pliki `.cpp` kompilują się osobno, więc kompilator nie musi zauważyć, że kopie się rozjechały. Jedna definicja w nagłówku to jedno miejsce do zmiany.
4. `TaskResult` to typ, a `result` to obiekt tego typu, czyli jeden rekord. Nie ma wspólnego rekordu: wspólna jest tylko definicja typu. `points.cpp` odczytuje rekord z `main` wyłącznie przez parametr funkcji.
5. Funkcja odczytuje istniejący rekord, bez tworzenia kopii, i nie może zmienić jego pól.
6. `main.cpp` potrzebuje definicji typu i deklaracji funkcji, żeby utworzyć rekord i wywołać funkcję. `points.cpp` potrzebuje definicji typu, żeby odczytać pola, a dołączając nagłówek, ma deklarację i definicję funkcji w jednej jednostce translacji.
7. Sprawia, że w jednej jednostce translacji nagłówek jest przetwarzany najwyżej raz. W lekcji 11.2 nagłówek zawierał tylko deklarację funkcji, którą wolno powtórzyć. Definicji typu w jednej jednostce translacji powtórzyć nie wolno, więc bez `#pragma once` drugie dołączenie daje błąd.
8. Nie: każdy plik `.cpp` to osobna jednostka translacji i każdy dostaje typ raz. Dwa `#include` w jednym pliku `.cpp` wstawiają definicję do tej samej jednostki translacji dwa razy. Bez `#pragma once` to błąd `redefinition`.
9. Błąd kompilacji: nie udaje się kompilacja `main.cpp`, więc linkowanie się nie zaczyna. W lekcji 11.2, punkt 8, wszystko się kompilowało, a linker nie znalazł definicji funkcji.
10. Nagłówek sam dołącza nagłówki, których potrzebuje do swoich deklaracji, na przykład `points.hpp` dołącza `task_result.hpp`. Wtedy działa w każdym pliku, który go dołącza, niezależnie od kolejności `#include`.

</details>

## Podsumowanie

- Definicję własnego typu, z którego korzysta kilka plików `.cpp`, umieszczamy we wspólnym nagłówku. Każdy plik, który tworzy rekord albo odczytuje jego pola, dołącza ten nagłówek.
- Wspólna jest definicja typu, a nie obiekt: rekord istnieje tam, gdzie go utworzono, a funkcja z innego pliku dostaje go przez parametr `const&`.
- Typ definiujemy w jednym miejscu, a nie w kopiach w każdym pliku `.cpp`. Definicja zwykłej funkcji nadal zostaje w pliku `.cpp`.
- W jednej jednostce translacji typ może być zdefiniowany tylko raz. `#pragma once` chroni przed ponownym przetworzeniem nagłówka w tym samym pliku `.cpp`. Dołączanie nagłówka przez różne pliki `.cpp` jest poprawne.
- `redefinition` to błąd kompilacji, a komunikat wskazuje miejsce w nagłówku. Linijka `In file included from` mówi, skąd nagłówek przyszedł.
- Nagłówek powinien sam dołączać nagłówki, których potrzebuje, zamiast zależeć od kolejności `#include` w plikach `.cpp`.
- Zmiana organizacji plików i interfejsu funkcji nie zmienia wyników programu.

## Co dalej

Program z tej lekcji ma jeden typ i jedną funkcję. Większe programy z Modułów 8–10 miały kilka funkcji, które czytały dane, analizowały je i wypisywały wyniki. W [lekcji 11.4: Podział programu według odpowiedzialności](lesson_04_splitting_responsibilities.md) taki program trafi do kilku plików, każdy z własną rolą.

---

## Przykładowe rozwiązania

Zajrzyj tutaj **po własnej próbie**. Twoje nazwy mogą się różnić, jeśli standardowe wyjście jest takie, jak wymagane.

<details>
<summary>Punkt 7: misja, zamówienie biletów jako rekord</summary>

**`tickets.hpp`**:

<!-- file: tickets tickets.hpp -->
```cpp
#pragma once

struct TicketOrder {
    int regular_tickets;
    int reduced_tickets;
};

int total_cost(const TicketOrder& order);
```

**`tickets.cpp`**:

<!-- file: tickets tickets.cpp -->
```cpp
#include "tickets.hpp"

int total_cost(const TicketOrder& order) {
    const int regular_price{12};
    const int reduced_price{7};
    return order.regular_tickets * regular_price + order.reduced_tickets * reduced_price;
}
```

**`main.cpp`**:

<!-- example: tickets -->
```cpp
#include <iostream>

#include "tickets.hpp"

int main() {
    TicketOrder order{0, 0};

    std::cin >> order.regular_tickets;
    std::cin >> order.reduced_tickets;

    std::cout << "Total cost: " << total_cost(order) << "\n";
}
```

**`CMakeLists.txt`**, taki sam jak w lekcji 11.2:

<!-- cmake: tickets -->
```cmake
cmake_minimum_required(VERSION 3.28)
project(first_program LANGUAGES CXX)

add_executable(first_program main.cpp tickets.cpp)
target_compile_features(first_program PRIVATE cxx_std_20)
set_target_properties(first_program PROPERTIES CXX_EXTENSIONS OFF)
```

Wyniki dla danych A–D: 45, 28, 0 i 36, takie same jak w lekcji 11.2.

To jedno z poprawnych rozwiązań:

1. **`TicketOrder` jest zdefiniowany w `tickets.hpp`,** bo korzystają z niego oba pliki `.cpp`: `main.cpp` tworzy rekord, a `tickets.cpp` odczytuje jego pola.
2. **Pola `regular_tickets` i `reduced_tickets`** mają typ `int`, jak wcześniej parametry funkcji. Nazwa typu jest od wielkiej litery, a pola w `snake_case`.
3. **Deklaracja `int total_cost(const TicketOrder& order);`** stoi pod definicją typu, bo z niego korzysta.
4. **Definicja funkcji zostaje w `tickets.cpp`** i odczytuje pola przez `order.`, bez zmieniania rekordu.
5. **Oba pliki `.cpp` dołączają `tickets.hpp`.** Żaden nie zawiera kopii `TicketOrder`.
6. **`TicketOrder order{0, 0};`** tworzy rekord z wartościami początkowymi, a dwa odczyty `>>` wpisują dane do jego pól. `order` nie ma `const`, bo `>>` zapisuje w jego polach.
7. **`total_cost(order)`** przekazuje cały rekord. Funkcja dostaje go przez `const&`, więc bez kopii.
8. **`#pragma once`** chroni definicję typu przed powtórzeniem w jednej jednostce translacji.
9. **`add_executable` wymienia dwa pliki `.cpp`,** bez nagłówka.
10. **Wyniki się nie zmieniły,** bo ceny i wzór są takie same. Zmieniła się tylko organizacja danych.

Inne poprawne rozwiązania: inne nazwy typu, pól, funkcji i plików, na przykład `struct Order` w `prices.hpp`, jeśli zachowujesz pliki z lekcji 11.2.

</details>

<details>
<summary>Punkt 8: poprawiony projekt</summary>

`points.hpp` znowu zaczyna się od `#pragma once`. W `main.cpp` są jeszcze oba `#include`, jak przy pierwszym sprawdzeniu poprawki w kroku 8. Potem powtórzoną linijkę usuń.

**`points.hpp`**:

<!-- file: points_twice_fixed points.hpp -->
```cpp
#pragma once

struct TaskResult {
    int solved;
    int bonus;
};

int calculate_points(const TaskResult& result);
```

**`main.cpp`**, z obiema linijkami `#include`, jak w kroku 8:

<!-- example: points_twice_fixed -->
```cpp
#include <iostream>

#include "points.hpp"
#include "points.hpp"

int main() {
    TaskResult result{0, 0};

    std::cin >> result.solved;
    std::cin >> result.bonus;

    std::cout << "Points: " << calculate_points(result) << "\n";
}
```

**`points.cpp`**, bez zmian:

<!-- file: points_twice_fixed points.cpp -->
```cpp
#include "points.hpp"

int calculate_points(const TaskResult& result) {
    const int points_per_task{3};
    return result.solved * points_per_task + result.bonus;
}
```

**`CMakeLists.txt`**, bez zmian:

<!-- cmake: points_twice_fixed -->
```cmake
cmake_minimum_required(VERSION 3.28)
project(first_program LANGUAGES CXX)

add_executable(first_program main.cpp points.cpp)
target_compile_features(first_program PRIVATE cxx_std_20)
set_target_properties(first_program PROPERTIES CXX_EXTENSIONS OFF)
```

Dla tych samych danych co w punkcie 6:

<!-- input: points_twice_fixed -->
```text
4 2
```

<!-- output: points_twice_fixed -->
```text
Points: 14
```

</details>

<details>
<summary>Punkt 9: samowystarczalny nagłówek</summary>

Zmienia się tylko `points.hpp`: sam dołącza `task_result.hpp`. `main.cpp` i `points.cpp` zostają takie jak w błędnym projekcie.

**`points.hpp`**:

<!-- file: points_order_fixed points.hpp -->
```cpp
#pragma once

#include "task_result.hpp"

int calculate_points(const TaskResult& result);
```

**`task_result.hpp`**, bez zmian:

<!-- file: points_order_fixed task_result.hpp -->
```cpp
#pragma once

struct TaskResult {
    int solved;
    int bonus;
};
```

**`main.cpp`**, bez zmian:

<!-- example: points_order_fixed -->
```cpp
#include <iostream>

#include "task_result.hpp"
#include "points.hpp"

int main() {
    TaskResult result{0, 0};

    std::cin >> result.solved;
    std::cin >> result.bonus;

    std::cout << "Points: " << calculate_points(result) << "\n";
}
```

**`points.cpp`**, bez zmian:

<!-- file: points_order_fixed points.cpp -->
```cpp
#include "points.hpp"

int calculate_points(const TaskResult& result) {
    const int points_per_task{3};
    return result.solved * points_per_task + result.bonus;
}
```

**`CMakeLists.txt`**, bez zmian:

<!-- cmake: points_order_fixed -->
```cmake
cmake_minimum_required(VERSION 3.28)
project(first_program LANGUAGES CXX)

add_executable(first_program main.cpp points.cpp)
target_compile_features(first_program PRIVATE cxx_std_20)
set_target_properties(first_program PROPERTIES CXX_EXTENSIONS OFF)
```

<!-- input: points_order_fixed -->
```text
4 2
```

<!-- output: points_order_fixed -->
```text
Points: 14
```

`main.cpp` dostaje `task_result.hpp` dwa razy, bezpośrednio i przez `points.hpp`, a dzięki `#pragma once` typ trafia do tej jednostki translacji raz. `main.cpp` może zachować własne `#include "task_result.hpp"`, bo sam korzysta z `TaskResult`.

</details>

**Poprzednia lekcja:** [Lekcja 11.2: Własny plik nagłówkowy](lesson_02_own_header_file.md) · **Następna lekcja:** [Lekcja 11.4: Podział programu według odpowiedzialności](lesson_04_splitting_responsibilities.md) · [Opis kursu](../../README.md)

# Lekcja 11.4: Podział programu według odpowiedzialności

**Polski** · [English](lesson_04_splitting_responsibilities.en.md) · [Opis kursu](../../README.md)

> **Moduł 11, lekcja 4** · około 100–120 minut, możesz ją podzielić na dwa podejścia: punkty 1–7 i punkty 8–11
> **Potrzebujesz:** katalogu `cpp-workspace` z projektem `workshop_orders` z [lekcji 10.3](../module_10_input_records/lesson_03_building_a_vector_of_records.md). Debugger nie jest w tej lekcji potrzebny.
> **Wersja pilotażowa.** Programy z tej lekcji, zbudowane z kilku plików, sprawdzamy automatycznie na Windowsie, Ubuntu i macOS, z danymi z lekcji 10.3, razem z błędem linkowania z punktu 9. Kroki w CLionie są takie jak w lekcjach 11.1–11.3 i nie zostały ręcznie sprawdzone na każdym systemie.

## Zanim zaczniesz

Ta lekcja zakłada, że:

- odczytujesz listę rekordów z zapowiedzianą liczbą, sprawdzasz odczyt przed zasadami i przy pierwszym błędzie kończysz program bez raportu (lekcja 10.3);
- przekazujesz wektor rekordów i jego elementy przez `const&` (lekcje 8.3 i 8.4);
- budujesz program z kilku plików `.cpp` i własnego nagłówka ze wspólnym typem (lekcje 11.1–11.3).

## Sytuacja

Program z listą przesyłek z lekcji 10.3 robi wszystko w jednym `main`: odczytuje dane, sprawdza je, buduje wektor, liczy sumę paczek i wypisuje raport. Przy 60 linijkach da się to jeszcze ogarnąć, ale żeby zmienić wygląd raportu, trzeba przeczytać cały odczyt, a żeby sprawdzić sumowanie, trzeba szukać go między instrukcjami wypisania. W tej lekcji podzielisz ten program na pliki **według odpowiedzialności**: odczyt i sterowanie, obliczenia oraz raport, ze wspólnym nagłówkiem.

Po tej lekcji będziesz:

- planować podział programu na pliki według tego, za co odpowiada każda część;
- umieszczać wspólny typ i deklaracje funkcji potrzebnych innym plikom we wspólnym nagłówku;
- oddzielać obliczanie wyniku od wypisywania raportu i wywoływać funkcje zdefiniowane w różnych plikach `.cpp`;
- rozpoznawać błąd linkowania, gdy ta sama funkcja jest zdefiniowana w dwóch plikach.

## 1. Przygotuj projekt

W `cpp-workspace` utwórz katalog `lesson_11_4` i skopiuj do niego `CMakeLists.txt` z oryginalnego `lesson_05_first_program`. Programem wyjściowym jest lista przesyłek z [lekcji 10.3, punkt 2](../module_10_input_records/lesson_03_building_a_vector_of_records.md#2-lista-przesyłek). Jeśli Twój `main.cpp` w `lesson_10_3` zawiera już inny program, skopiuj kod z tamtego punktu. W tej lekcji nie zmieniasz jego działania, tylko rozkładasz go na cztery pliki.

## 2. Najpierw plan podziału

Zanim utworzysz pliki, zdecyduj, kto za co odpowiada:

| Odpowiedzialność | Potrzebne dane | Plik | Funkcja albo operacja | Wynik |
|---|---|---|---|---|
| odczyt, sprawdzanie danych, budowanie listy i sterowanie programem | standardowe wejście | `main.cpp` | `main` | wektor poprawnych przesyłek albo komunikat `Input error` lub `Invalid shipments` |
| wspólny typ i deklaracje | — | `shipments.hpp` | `struct Shipment`, deklaracje dwóch funkcji | umowa, z której korzystają pozostałe pliki |
| obliczenia | wektor przesyłek | `shipments_analysis.cpp` | `total_boxes` | suma paczek, liczba `int` |
| raport | wektor przesyłek | `shipments_report.cpp` | `print_shipments` | linie raportu na standardowym wyjściu |

Przepływ danych i wywołań:

```text
main  ──odczytuje poprawne rekordy──►  std::vector<Shipment>
main  ──const std::vector<Shipment>&──►  print_shipments   (shipments_report.cpp)
print_shipments  ──ten sam wektor──►  total_boxes   (shipments_analysis.cpp)
total_boxes  ──zwraca sumę──►  print_shipments  ──►  raport na standardowym wyjściu
```

Dlaczego takie granice:

- **Odczyt i sterowanie zostają w `main`,** bo to `main` decyduje, czy dane są poprawne i czy w ogóle powstanie raport.
- **Obliczenie stoi osobno,** bo nie zależy od tego, jak wynik zostanie wypisany. Zmiana wyglądu raportu nie wymaga wtedy zmiany sumowania.
- **Raport stoi osobno,** bo wypisuje gotowe dane i nie musi wiedzieć, jak je odczytano.
- **Typ i deklaracje są wspólne,** więc nikt ich nie kopiuje (lekcje 11.2 i 11.3).

Łatwiej wtedy znaleźć kod, który odpowiada za dany problem, a obliczenia nie mieszają się z wypisywaniem. Sam podział na pliki nie zmienia działania programu i nie przyspiesza go. To jeden rozsądny podział, a nie jedyna architektura każdego programu. Czego ten podział **nie** oznacza:

- **Nie każda funkcja ma własny plik.** Kilka powiązanych funkcji może stać w jednym pliku `.cpp`, co zobaczysz w misji.
- **Nagłówek deklaruje to, czego potrzebują inne pliki,** a nie wszystko z całego programu. Funkcja pomocnicza używana tylko w jednym pliku `.cpp` nie musi trafić do wspólnego nagłówka.
- **Plik dołącza nagłówki, których sam potrzebuje,** a nie wszystkie nagłówki projektu.
- **Kolejność plików w `add_executable` nie ustala kolejności działania.** Program zawsze zaczyna się od `main`, a funkcje wykonują się wtedy, gdy ktoś je wywoła.

## 3. Wspólny nagłówek: umowa między plikami

**`shipments.hpp`**:

<!-- file: shipments shipments.hpp -->
```cpp
#pragma once

#include <string>
#include <vector>

struct Shipment {
    std::string destination;
    int boxes;
};

int total_boxes(const std::vector<Shipment>& shipments);
void print_shipments(const std::vector<Shipment>& shipments);
```

- **Nagłówek to umowa.** Mówi, jak wygląda przesyłka i jakie funkcje można wywołać, a nie jak działają. Implementacja stoi w plikach `.cpp`, a `main.cpp` łączy wszystko w przebieg programu.
- **`Shipment` to ten sam typ co w lekcji 10.3,** przeniesiony do nagłówka jak `TaskResult` w lekcji 11.3.
- **Dwie deklaracje,** bo z tych funkcji korzystają inne pliki: `main.cpp` wywołuje `print_shipments`, a `shipments_report.cpp` wywołuje `total_boxes`.
- **`void`,** bo `print_shipments` niczego nie zwraca, tylko wypisuje (lekcja 5.1).
- **Nagłówek jest samowystarczalny:** sam dołącza `<string>` i `<vector>`, bo potrzebują ich jego deklaracje (lekcja 11.3, punkt 9). Nie zawiera definicji zwykłych funkcji (lekcja 11.2).

## 4. Obliczenia: `shipments_analysis.cpp`

<!-- file: shipments shipments_analysis.cpp -->
```cpp
#include "shipments.hpp"

int total_boxes(const std::vector<Shipment>& shipments) {
    int total{0};

    for (const Shipment& shipment : shipments) {
        total += shipment.boxes;
    }

    return total;
}
```

- **Dostaje wektor przez `const&` i przegląda elementy przez `const Shipment&`,** bez kopii i bez zmian (lekcja 8.4).
- **Niczego nie odczytuje ani nie wypisuje:** tylko zwraca wynik.
- **Dołącza tylko `shipments.hpp`,** bo z niego ma typ i deklarację, którą definiuje. Ze standardowego wejścia ani wyjścia nie korzysta.

## 5. Raport: `shipments_report.cpp`

<!-- file: shipments shipments_report.cpp -->
```cpp
#include <iostream>

#include "shipments.hpp"

void print_shipments(const std::vector<Shipment>& shipments) {
    std::cout << "Shipments: " << shipments.size() << "\n";

    for (const Shipment& shipment : shipments) {
        std::cout << shipment.destination << ": " << shipment.boxes << "\n";
    }

    std::cout << "Total boxes: " << total_boxes(shipments) << "\n";
}
```

- **Wypisuje raport w tym samym formacie co w lekcji 10.3:** liczbę przesyłek, każdą przesyłkę w kolejności z wektora i sumę.
- **Sumy nie liczy sam.** Wywołuje `total_boxes`, która jest zdefiniowana w innym pliku. Kompilator zna ją z deklaracji w `shipments.hpp`, a wywołanie z definicją łączy linker, jak `main` z `calculate_points` w lekcji 11.1. **Funkcje z różnych plików współpracują bez dołączania plików `.cpp`.**
- **Dołącza `<iostream>`,** bo sam wypisuje, i `shipments.hpp`, bo korzysta z typu i obu deklaracji.

## 6. Odczyt i sterowanie: `main.cpp`

**`main.cpp`**:

<!-- example: shipments -->
```cpp
#include <iostream>
#include <string>
#include <vector>

#include "shipments.hpp"

int main() {
    std::vector<Shipment> shipments{};
    int count{0};
    std::cin >> count;

    if (std::cin.fail()) {
        std::cout << "Input error\n";
        return 0;
    }

    if (count < 0 || count > 5) {
        std::cout << "Invalid shipments\n";
        return 0;
    }

    for (int index{0}; index < count; ++index) {
        std::string rest{};
        std::getline(std::cin, rest);

        std::string destination{};
        int boxes{0};
        std::getline(std::cin, destination);
        std::cin >> boxes;

        if (std::cin.fail()) {
            std::cout << "Input error\n";
            return 0;
        }

        if (destination.empty() || boxes < 0) {
            std::cout << "Invalid shipments\n";
            return 0;
        }

        const Shipment shipment{destination, boxes};
        shipments.push_back(shipment);
    }

    print_shipments(shipments);
}
```

- **Odczyt i sprawdzanie są takie jak w lekcji 10.3:** liczba przesyłek, dokańczanie linii, `std::cin.fail()` przed zasadami, rekord dopiero po obu sprawdzeniach (lekcja 10.3, punkty 3–6). Zmieniło się tylko zakończenie.
- **Zamiast sumowania i wypisywania jest jedno wywołanie:** `print_shipments(shipments);`. Raport powstaje dopiero po udanym odczycie wszystkich przesyłek.
- **`Input error` i `Invalid shipments` zostają w `main`,** bo to reakcja na błąd w odczycie i w sterowaniu programem, a nie część raportu. Przy błędzie `return 0;` kończy program, zanim dojdzie do wywołania.
- **`main.cpp` zachowuje swoje `#include` z lekcji 10.3,** bo sam odczytuje tekst przez `std::getline` i buduje wektor, a dokłada `shipments.hpp`.

## 7. Zbuduj i porównaj wyniki

`add_executable` wymienia teraz trzy pliki `.cpp`, w jednej linijce, bez nagłówka:

<!-- cmake: shipments -->
```cmake
cmake_minimum_required(VERSION 3.28)
project(first_program LANGUAGES CXX)

add_executable(first_program main.cpp shipments_analysis.cpp shipments_report.cpp)
target_compile_features(first_program PRIVATE cxx_std_20)
set_target_properties(first_program PROPERTIES CXX_EXTENSIONS OFF)
```

Zbuduj i uruchom program jak w lekcji 11.1, punkt 5. W wyniku budowania są trzy linijki `Building CXX object` i jedna `Linking`. Dla danych A, tych samych co w lekcji 10.3:

<!-- input: shipments -->
```text
2
North Hub
4
South Depot
7
```

<!-- output: shipments -->
```text
Shipments: 2
North Hub: 4
South Depot: 7
Total boxes: 11
```

**Przewidź**, a potem porównaj wyniki dla danych B (pusta lista), C (błąd w późniejszym rekordzie) i D (słowo zamiast liczby). Uruchomienie jest nieobowiązkowe.

<!-- input: shipments -->
```text
0
```

<details>
<summary>Standardowe wyjście dla danych B</summary>

<!-- output: shipments -->
```text
Shipments: 0
Total boxes: 0
```

</details>

<!-- input: shipments -->
```text
2
North Hub
4
South Depot
-2
```

<details>
<summary>Standardowe wyjście dla danych C</summary>

<!-- output: shipments -->
```text
Invalid shipments
```

</details>

<!-- input: shipments -->
```text
2
North Hub
4
South Depot
seven
```

<details>
<summary>Standardowe wyjście dla danych D</summary>

<!-- output: shipments -->
```text
Input error
```

</details>

**Wyniki są dokładnie takie jak w lekcji 10.3,** dla tych samych danych. Poprawny raport dla danych A nie dowodzi jednak, że wszystkie zasady z lekcji 10.3 nadal działają. Dlatego program jest automatycznie sprawdzany na wszystkich 11 przypadkach z tamtej lekcji:

<details>
<summary>Pozostałe przypadki z lekcji 10.3, sprawdzone automatycznie</summary>

Słowo zamiast liczby przesyłek:

<!-- input: shipments -->
```text
two
```

<!-- output: shipments -->
```text
Input error
```

Zapowiedziane 3 przesyłki, a w danych tylko 2:

<!-- input: shipments -->
```text
3
North Hub
4
South Depot
7
```

<!-- output: shipments -->
```text
Input error
```

Liczba przesyłek poza zakresem 0–5:

<!-- input: shipments -->
```text
-1
```

<!-- output: shipments -->
```text
Invalid shipments
```

<!-- input: shipments -->
```text
6
```

<!-- output: shipments -->
```text
Invalid shipments
```

Pusta nazwa późniejszej przesyłki:

<!-- input: shipments -->
```text
2
North Hub
4

7
```

<!-- output: shipments -->
```text
Invalid shipments
```

Jedna przesyłka:

<!-- input: shipments -->
```text
1
East Gate
3
```

<!-- output: shipments -->
```text
Shipments: 1
East Gate: 3
Total boxes: 3
```

Pięć przesyłek:

<!-- input: shipments -->
```text
5
Central Hub
2
North Hub
4
River Port
0
South Depot
7
West End Depot
1
```

<!-- output: shipments -->
```text
Shipments: 5
Central Hub: 2
North Hub: 4
River Port: 0
South Depot: 7
West End Depot: 1
Total boxes: 14
```

</details>

Te same wyniki dają dane, które kończą się zaraz po ostatniej liczbie, bez końca linii. Tego przypadku testy automatyczne nie uruchamiają, tak jak w lekcji 10.3.

## 8. Misja: zlecenia w pracowni, w kilku plikach

Podziel według odpowiedzialności swój program `workshop_orders` z [misji lekcji 10.3](../module_10_input_records/lesson_03_building_a_vector_of_records.md#8-misja-zlecenia-w-pracowni). W `cpp-workspace` utwórz katalog `workshop_orders_split` i skopiuj do niego `CMakeLists.txt` z `lesson_11_4`. Oryginał zostaw bez zmian: posłuży do porównania wyników. Jeśli nie masz tego projektu, odtwórz go z [rozwiązania lekcji 10.3](../module_10_input_records/lesson_03_building_a_vector_of_records.md#przykładowe-rozwiązania).

**Umowa się nie zmienia:** od 0 do 5 zleceń, niepusta nazwa klienta ze spacjami, zaplanowane jednostki większe od zera, ukończone nieujemne i nie większe od zaplanowanych. Odczyt jest sprawdzany przed zasadami. Nieudany odczyt daje `Input error`, niedozwolona wartość `Invalid orders`, a po błędzie nie ma części raportu. Szczegóły odczytu, spacji, dokańczania linii i końca danych są takie jak w lekcji 10.3, punkt 8.

**Wymagania:**

1. **Najpierw plan.** Zanim utworzysz pliki, zapisz tabelę jak w punkcie 2: odpowiedzialność, dane, plik, funkcja, wynik.
2. **`main.cpp`** odczytuje i sprawdza dane, tworzy rekordy, buduje wektor, wypisuje komunikaty błędów i dopiero po sukcesie wywołuje raport.
3. **Wspólny nagłówek** definiuje typ zlecenia i deklaruje funkcje potrzebne innym plikom, z `#pragma once`. Jest samowystarczalny.
4. **Plik analityczny** zawiera dwie funkcje: pozostałe jednostki jednego zlecenia i sumę pozostałych jednostek całej listy. Nie odczytuje i nie wypisuje.
5. **Plik raportu** wypisuje liczbę zleceń, każde zlecenie i sumę, a obie wartości bierze z funkcji analitycznych. Wzór na pozostałe jednostki stoi w jednym miejscu.
6. **Kolekcja i elementy tylko odczytywane** są przekazywane przez `const&`.
7. **`add_executable`** wymienia wszystkie trzy pliki `.cpp` w jednej linijce, bez nagłówka.
8. Nazwy plików składają się z małych liter angielskich, cyfr i `_` i kończą na `.cpp` albo `.hpp`. Przykładowe rozwiązanie używa `orders.hpp`, `orders_analysis.cpp` i `orders_report.cpp`.

Wyniki mają być dokładnie takie jak w lekcji 10.3. **Dane A:**

<!-- input: orders -->
```text
3
North Library
12 5
City Archive
8 8
Green Workshop
6 0
```

<!-- output: orders -->
```text
Orders: 3
North Library: planned 12, completed 5, remaining 7
City Archive: planned 8, completed 8, remaining 0
Green Workshop: planned 6, completed 0, remaining 6
Remaining total: 13
```

**Dane B:**

<!-- input: orders -->
```text
0
```

<!-- output: orders -->
```text
Orders: 0
Remaining total: 0
```

**Dane C**, niedozwolona wartość w drugim zleceniu:

<!-- input: orders -->
```text
2
North Library
12 5
City Archive
8 9
```

<!-- output: orders -->
```text
Invalid orders
```

**Przewidź D**, słowo zamiast liczby w drugim zleceniu, i **E**: zero zaplanowanych jednostek, a potem słowo zamiast drugiej liczby.

<!-- input: orders -->
```text
2
North Library
12 5
City Archive
8 done
```

<details>
<summary>Standardowe wyjście dla danych D</summary>

<!-- output: orders -->
```text
Input error
```

</details>

<!-- input: orders -->
```text
2
North Library
12 5
City Archive
0 done
```

<details>
<summary>Standardowe wyjście dla danych E</summary>

<!-- output: orders -->
```text
Input error
```

</details>

E chroni kolejność z lekcji 10.3: nieudany odczyt ma pierwszeństwo przed sprawdzaniem wartości.

**Zdecyduj samodzielnie:**

1. jak nazwać pliki;
2. jak nazwać typ i jego pola;
3. jak nazwać funkcje;
4. które funkcje zadeklarować w nagłówku;
5. które funkcje zdefiniować w pliku analitycznym;
6. która funkcja przygotowuje raport;
7. jak dane przechodzą między funkcjami;
8. jakich `#include` potrzebuje każdy plik;
9. jakie źródła wymienić w `add_executable`;
10. jak porównać wyniki z jednoplikową wersją z lekcji 10.3.

**Potem** zbuduj program i uruchom go dla danych A i jednego z przypadków B albo C. Porównaj wyniki z projektem `workshop_orders` dla tych samych danych. Pozostałe przypadki przewidź. Wszystkie 19 przypadków z lekcji 10.3 jest sprawdzonych automatycznie w rozwiązaniu referencyjnym.

### Kryterium sukcesu

- Program buduje się jako C++20, a dla danych A oraz B albo C wypisuje dokładnie pokazany wynik, ten sam co projekt z lekcji 10.3.
- Plan podziału powstał przed plikami, a każdy plik ma jedną, opisaną w nim rolę.
- Typ jest zdefiniowany tylko we wspólnym nagłówku, a nagłówek zawiera tylko definicję typu i deklaracje, z `#pragma once` i potrzebnymi `#include`.
- `main.cpp` nie liczy pozostałych jednostek i nie wypisuje szczegółów raportu. Plik raportu nie powtarza wzoru z pliku analitycznego.
- Każda funkcja jest zdefiniowana dokładnie raz, w swoim pliku `.cpp`.
- `add_executable` wymienia trzy pliki `.cpp`.

Poprawne wyniki dowodzą zachowania, a nie organizacji: program z całym kodem w `main` też by je wypisał. To, gdzie stoją obliczenia i raport, sprawdzasz według listy powyżej.

<details>
<summary>Podpowiedź 1</summary>

Jak oddzielić część, która odczytuje dane, od części, która oblicza wynik? Po czym poznać, gdzie w programie z lekcji 10.3 kończy się odczyt, a zaczyna raport?

</details>

<details>
<summary>Podpowiedź 2</summary>

Które dane i deklaracje muszą być wspólne dla kilku plików? Pomyśl, kto tworzy rekordy, kto je odczytuje i kto wywołuje czyje funkcje.

</details>

<details>
<summary>Podpowiedź 3</summary>

Jak zorganizować plik analityczny i plik raportu, żeby wzór na pozostałe jednostki stał w jednym miejscu? Funkcja dla jednego zlecenia może służyć i do sumy, i do linii raportu.

</details>

Przykładowe rozwiązanie jest w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 9. Znajdź błąd: ta sama funkcja w dwóch plikach

To zadanie wykonaj **po misji**. Ktoś przenosił sumowanie do `shipments_analysis.cpp`, ale zapomniał usunąć poprzednią wersję funkcji z pliku raportu. Odtwórz ten projekt: w `cpp-workspace` utwórz katalog `shipments_twice_check`, skopiuj do niego pięć plików z `lesson_11_4` i w `shipments_report.cpp` dopisz drugą definicję `total_boxes`, taką samą jak w pliku analitycznym:

**`shipments_report.cpp`** w tym projekcie:

<!-- file: shipments_twice_check shipments_report.cpp -->
```cpp
#include <iostream>

#include "shipments.hpp"

int total_boxes(const std::vector<Shipment>& shipments) {
    int total{0};

    for (const Shipment& shipment : shipments) {
        total += shipment.boxes;
    }

    return total;
}

void print_shipments(const std::vector<Shipment>& shipments) {
    std::cout << "Shipments: " << shipments.size() << "\n";

    for (const Shipment& shipment : shipments) {
        std::cout << shipment.destination << ": " << shipment.boxes << "\n";
    }

    std::cout << "Total boxes: " << total_boxes(shipments) << "\n";
}
```

<details>
<summary>Pozostałe pliki, bez zmian względem punktów 3–7</summary>

**`main.cpp`**:

<!-- broken: shipments_twice_check stage=link error=multiple definition of .total_boxes\(|duplicate symbol: int __cdecl total_boxes\(|duplicate symbol 'total_boxes\( -->
```cpp
#include <iostream>
#include <string>
#include <vector>

#include "shipments.hpp"

int main() {
    std::vector<Shipment> shipments{};
    int count{0};
    std::cin >> count;

    if (std::cin.fail()) {
        std::cout << "Input error\n";
        return 0;
    }

    if (count < 0 || count > 5) {
        std::cout << "Invalid shipments\n";
        return 0;
    }

    for (int index{0}; index < count; ++index) {
        std::string rest{};
        std::getline(std::cin, rest);

        std::string destination{};
        int boxes{0};
        std::getline(std::cin, destination);
        std::cin >> boxes;

        if (std::cin.fail()) {
            std::cout << "Input error\n";
            return 0;
        }

        if (destination.empty() || boxes < 0) {
            std::cout << "Invalid shipments\n";
            return 0;
        }

        const Shipment shipment{destination, boxes};
        shipments.push_back(shipment);
    }

    print_shipments(shipments);
}
```

**`shipments.hpp`**:

<!-- file: shipments_twice_check shipments.hpp -->
```cpp
#pragma once

#include <string>
#include <vector>

struct Shipment {
    std::string destination;
    int boxes;
};

int total_boxes(const std::vector<Shipment>& shipments);
void print_shipments(const std::vector<Shipment>& shipments);
```

**`shipments_analysis.cpp`**:

<!-- file: shipments_twice_check shipments_analysis.cpp -->
```cpp
#include "shipments.hpp"

int total_boxes(const std::vector<Shipment>& shipments) {
    int total{0};

    for (const Shipment& shipment : shipments) {
        total += shipment.boxes;
    }

    return total;
}
```

**`CMakeLists.txt`**:

<!-- cmake: shipments_twice_check -->
```cmake
cmake_minimum_required(VERSION 3.28)
project(first_program LANGUAGES CXX)

add_executable(first_program main.cpp shipments_analysis.cpp shipments_report.cpp)
target_compile_features(first_program PRIVATE cxx_std_20)
set_target_properties(first_program PROPERTIES CXX_EXTENSIONS OFF)
```

</details>

**Zanim zbudujesz**, odpowiedz na piśmie:

1. **Przewidź:** na którym etapie budowanie się nie uda, kompilacji czy linkowania?
2. Czy każdy z trzech plików `.cpp` z osobna jest poprawnym kodem C++?
3. Ile definicji `total_boxes` dostanie linker?
4. Czy `#pragma once` w `shipments.hpp` może tu pomóc?

**Potem:**

5. Zbuduj projekt. Skonfiguruj go jak nowy projekt w lekcji 11.1, punkt 5.
6. Przeczytaj wynik budowania: ile plików się skompilowało i co zgłasza linker?
7. Usuń drugą definicję `total_boxes` z `shipments_report.cpp`. Zostaw definicję w `shipments_analysis.cpp`, bo obliczenia należą do tego pliku.
8. Zbuduj projekt ponownie i uruchom go dla danych A z punktu 7.
9. Wyjaśnij, dlaczego usunięcie `shipments_analysis.cpp` z `add_executable` nie byłoby poprawką.

<details>
<summary>Co się dzieje i dlaczego: otwórz po zbudowaniu błędnego projektu</summary>

1. **Wszystkie trzy pliki się kompilują:** są trzy linijki `Building CXX object`. Każdy plik z osobna jest poprawny: `shipments_report.cpp` definiuje dwie funkcje, a `shipments_analysis.cpp` jedną.
2. **Linkowanie się nie udaje,** bo linker dostaje dwie definicje tej samej zwykłej funkcji, z dwóch plików obiektowych, i nie wie, której użyć. Komunikat wymienia `total_boxes`: na Ubuntu `multiple definition of`, na macOS `duplicate symbol`, na Windowsie `duplicate symbol:`, a na końcu `linker command failed`.
3. **`#pragma once` tu nie pomaga.** Działa w obrębie jednej jednostki translacji (lekcja 11.3), a te dwie definicje stoją w dwóch różnych plikach `.cpp`, które kompilują się osobno.
4. **Inny błąd niż wcześniej:**
   - w lekcji 11.1 definicji brakowało, bo plik nie był budowany;
   - w lekcji 11.2 definicja miała inną nazwę;
   - w lekcji 11.3 typ był zdefiniowany dwa razy w jednej jednostce translacji, co zgłaszał kompilator;
   - tu jest za dużo definicji funkcji, w dwóch jednostkach, co zgłasza linker.
5. **Poprawka to jedna definicja we właściwym pliku.** Usunięcie `shipments_analysis.cpp` z `add_executable` usunęłoby błąd, ale zostawiłoby obliczenia w pliku raportu, czyli zepsuło podział. Po usunięciu kopii pliki są takie same jak w punktach 3–7, a program dla danych A wypisuje ten sam raport.

</details>

## 10. Gdy coś pójdzie inaczej

| Co widzisz | Co to znaczy | Co zrobić |
|---|---|---|
| `multiple definition of` albo `duplicate symbol` z nazwą funkcji | Ta sama funkcja jest zdefiniowana w dwóch plikach `.cpp` (punkt 9), albo któryś plik dołącza plik `.cpp`. | Zostaw jedną definicję w pliku, który za nią odpowiada. Nie dołączaj plików `.cpp`. |
| `undefined reference`, `undefined symbol` albo `referenced from` z `total_boxes` lub `print_shipments` | Plik z definicją nie jest w `add_executable` albo definicja ma inną nazwę lub inne parametry niż deklaracja (lekcje 11.1 i 11.2). | Sprawdź `add_executable` i porównaj definicję z nagłówkiem. |
| `use of undeclared identifier 'Shipment'` albo `unknown type name 'Shipment'` | Plik nie dołącza `shipments.hpp`. | Dopisz `#include "shipments.hpp"`. |
| `no member named 'cout' in namespace 'std'` w pliku raportu | Plik wypisuje, ale nie dołącza `<iostream>`. | Dopisz `#include <iostream>` w tym pliku. |
| Raport różni się od lekcji 10.3, na przykład suma stoi przed przesyłkami | Inna kolejność instrukcji w funkcji raportu. | Porównaj kolejność linii z raportem z lekcji 10.3. |
| Przy błędnych danych pojawia się część raportu | Raport jest wywoływany przed końcem odczytu albo mimo błędu. | Wywołaj funkcję raportu dopiero po pętli, gdy wszystkie rekordy są poprawne. |

## 11. Wyjaśnij

Odpowiedz własnymi słowami, najlepiej na piśmie. Dopiero potem porównaj z przykładowymi odpowiedziami.

1. Za co odpowiada `main.cpp`, a za co pozostałe pliki `.cpp`?
2. Dlaczego obliczenie sumy stoi w innym pliku niż wypisywanie raportu?
3. Dlaczego `Shipment` jest zdefiniowany w nagłówku?
4. Dlaczego nagłówek deklaruje właśnie `total_boxes` i `print_shipments`?
5. Jakie `#include` ma `shipments_report.cpp` i dlaczego właśnie takie?
6. Jak `print_shipments` wywołuje `total_boxes`, skoro ta funkcja jest zdefiniowana w innym pliku?
7. Dlaczego wszystkie trzy pliki `.cpp` muszą być w `add_executable`? Czy ich kolejność ustala kolejność działania programu?
8. Jak wykazać, że podział nie zmienił działania programu? Czego nie dowodzi samo porównanie standardowego wyjścia?
9. Dlaczego ta sama funkcja zdefiniowana w dwóch plikach `.cpp` to błąd linkowania, a nie kompilacji? Czy `#pragma once` mógłby go usunąć?
10. Czy każda funkcja powinna mieć własny plik i deklarację we wspólnym nagłówku?

<details>
<summary>Przykładowe odpowiedzi</summary>

1. `main.cpp` odczytuje i sprawdza dane, buduje wektor, wypisuje komunikaty błędów i decyduje, czy powstanie raport. `shipments_analysis.cpp` oblicza sumę paczek, a `shipments_report.cpp` wypisuje raport.
2. Bo obliczenie nie zależy od wyglądu raportu. Można zmienić format wypisywania bez zmiany sumowania i sprawdzić sumowanie bez czytania instrukcji wypisania.
3. Bo korzystają z niego wszystkie trzy pliki `.cpp`: `main.cpp` tworzy rekordy, a pozostałe odczytują ich pola. Definicja w jednym nagłówku nie jest kopiowana.
4. Bo z tych funkcji korzystają inne pliki: `main.cpp` wywołuje `print_shipments`, a `shipments_report.cpp` wywołuje `total_boxes`. Nagłówek deklaruje to, czego potrzebują inne pliki.
5. `<iostream>`, bo plik sam wypisuje, i `shipments.hpp`, bo korzysta z `Shipment` i obu deklaracji. `<string>` i `<vector>` daje samowystarczalny nagłówek, którego deklaracje ich wymagają.
6. Kompilator zna `total_boxes` z deklaracji w `shipments.hpp`, więc kompiluje wywołanie. Z definicją w `shipments_analysis.cpp` łączy je linker. Żaden plik nie dołącza pliku `.cpp`.
7. Bo każdy z nich zawiera definicję potrzebną w programie, a linker łączy tylko pliki z `add_executable`. Kolejność na liście nie ma znaczenia dla działania: program zaczyna się od `main`, a funkcje wykonują się, gdy ktoś je wywoła.
8. Uruchomić program dla tych samych danych co w lekcji 10.3, także błędnych, i porównać pełne wyjście. Porównanie nie dowodzi, że kod jest dobrze podzielony: program z całym kodem w `main` dałby te same wyniki. Organizację sprawdza się, czytając pliki.
9. Bo każdy plik `.cpp` z osobna jest poprawny i kompilator kompiluje je osobno. Dopiero linker widzi dwie definicje tej samej funkcji. `#pragma once` działa w jednej jednostce translacji, więc nie usunie definicji z dwóch różnych plików.
10. Nie. Powiązane funkcje mogą stać w jednym pliku, jak dwie funkcje w pliku analitycznym w misji. Nagłówek deklaruje tylko to, czego potrzebują inne pliki.

</details>

## Podsumowanie

- Większy program dzielimy na pliki według odpowiedzialności: odczyt i sterowanie w `main.cpp`, obliczenia w jednym pliku `.cpp`, raport w drugim.
- Wspólny nagłówek to umowa: definiuje wspólny typ i deklaruje funkcje, których potrzebują inne pliki. Pliki `.cpp` zawierają implementację.
- Funkcje z różnych plików `.cpp` współpracują przez deklaracje z nagłówka, a łączy je linker. Pliku `.cpp` nie dołącza się do innego.
- Każdy plik dołącza nagłówki, których sam potrzebuje. Wszystkie pliki `.cpp` stoją w `add_executable`, ale ich kolejność nie ustala kolejności działania.
- Podział na pliki nie zmienia zachowania programu: wyniki porównujesz na tych samych danych, także błędnych.
- Ta sama zwykła funkcja zdefiniowana w dwóch plikach `.cpp` to błąd linkowania. Poprawką jest jedna definicja we właściwym pliku, a nie `#pragma once` ani usuwanie plików z `add_executable`.
- Nie każda funkcja potrzebuje własnego pliku ani miejsca we wspólnym nagłówku.

## Co dalej

W lekcjach 11.1–11.4 program przeszedł od jednego pliku do kilku plików `.cpp` ze wspólnym nagłówkiem, a każdy z nich ma swoją rolę. W [lekcji 11.5: Sprawdzian — samodzielny program wieloplikowy](lesson_05_multifile_checkpoint.md) zaprojektujesz taki program samodzielnie, od planu po diagnostykę.

---

## Przykładowe rozwiązania

Zajrzyj tutaj **po własnej próbie**. Twoje nazwy mogą się różnić, jeśli standardowe wyjście jest takie, jak wymagane.

<details>
<summary>Punkt 8: misja, zlecenia w pracowni w kilku plikach</summary>

**Plan:**

| Odpowiedzialność | Potrzebne dane | Plik | Funkcja albo operacja | Wynik |
|---|---|---|---|---|
| odczyt, sprawdzanie, budowanie listy i sterowanie | standardowe wejście | `main.cpp` | `main` | wektor poprawnych zleceń albo komunikat `Input error` lub `Invalid orders` |
| wspólny typ i deklaracje | — | `orders.hpp` | `struct Order`, deklaracje trzech funkcji | umowa dla pozostałych plików |
| obliczenia | jedno zlecenie albo wektor zleceń | `orders_analysis.cpp` | `remaining_units`, `remaining_total` | pozostałe jednostki, liczby `int` |
| raport | wektor zleceń | `orders_report.cpp` | `print_orders` | linie raportu |

**`orders.hpp`**:

<!-- file: orders orders.hpp -->
```cpp
#pragma once

#include <string>
#include <vector>

struct Order {
    std::string client;
    int planned_units;
    int completed_units;
};

int remaining_units(const Order& order);
int remaining_total(const std::vector<Order>& orders);
void print_orders(const std::vector<Order>& orders);
```

**`orders_analysis.cpp`**:

<!-- file: orders orders_analysis.cpp -->
```cpp
#include "orders.hpp"

int remaining_units(const Order& order) {
    return order.planned_units - order.completed_units;
}

int remaining_total(const std::vector<Order>& orders) {
    int total{0};

    for (const Order& order : orders) {
        total += remaining_units(order);
    }

    return total;
}
```

**`orders_report.cpp`**:

<!-- file: orders orders_report.cpp -->
```cpp
#include <iostream>

#include "orders.hpp"

void print_orders(const std::vector<Order>& orders) {
    std::cout << "Orders: " << orders.size() << "\n";

    for (const Order& order : orders) {
        std::cout << order.client << ": planned " << order.planned_units << ", completed " << order.completed_units
                  << ", remaining " << remaining_units(order) << "\n";
    }

    std::cout << "Remaining total: " << remaining_total(orders) << "\n";
}
```

**`main.cpp`**:

<!-- example: orders -->
```cpp
#include <iostream>
#include <string>
#include <vector>

#include "orders.hpp"

int main() {
    std::vector<Order> orders{};
    int count{0};
    std::cin >> count;

    if (std::cin.fail()) {
        std::cout << "Input error\n";
        return 0;
    }

    if (count < 0 || count > 5) {
        std::cout << "Invalid orders\n";
        return 0;
    }

    for (int index{0}; index < count; ++index) {
        std::string rest{};
        std::getline(std::cin, rest);

        std::string client{};
        int planned_units{0};
        int completed_units{0};
        std::getline(std::cin, client);
        std::cin >> planned_units;
        std::cin >> completed_units;

        if (std::cin.fail()) {
            std::cout << "Input error\n";
            return 0;
        }

        if (client.empty() || planned_units <= 0 || completed_units < 0 || completed_units > planned_units) {
            std::cout << "Invalid orders\n";
            return 0;
        }

        const Order order{client, planned_units, completed_units};
        orders.push_back(order);
    }

    print_orders(orders);
}
```

**`CMakeLists.txt`**:

<!-- cmake: orders -->
```cmake
cmake_minimum_required(VERSION 3.28)
project(first_program LANGUAGES CXX)

add_executable(first_program main.cpp orders_analysis.cpp orders_report.cpp)
target_compile_features(first_program PRIVATE cxx_std_20)
set_target_properties(first_program PROPERTIES CXX_EXTENSIONS OFF)
```

To jedno z poprawnych rozwiązań:

1. **`Order` jest zdefiniowany w `orders.hpp`,** bo korzystają z niego wszystkie trzy pliki `.cpp`. To ten sam typ co w lekcji 10.3.
2. **Nagłówek deklaruje trzy funkcje,** bo każdej używa inny plik: `main.cpp` wywołuje `print_orders`, a `orders_report.cpp` wywołuje `remaining_units` i `remaining_total`.
3. **`remaining_units` i `remaining_total` stoją w jednym pliku,** bo obie należą do obliczeń. Nie każda funkcja potrzebuje własnego pliku.
4. **Wzór `planned_units - completed_units` stoi raz,** w `remaining_units`. Korzystają z niego i suma, i linia raportu.
5. **Wektor i elementy są przekazywane przez `const&`,** bo funkcje tylko je odczytują.
6. **`orders_analysis.cpp` niczego nie odczytuje ani nie wypisuje,** a `orders_report.cpp` niczego nie oblicza sam.
7. **`main.cpp` ma odczyt i sprawdzanie z lekcji 10.3 bez zmian,** a zamiast sumowania i wypisywania jedno wywołanie `print_orders(orders);` po pętli.
8. **Komunikaty błędów zostają w `main`,** a przy błędzie `return 0;` kończy program przed raportem. Częściowego raportu nie ma.
9. **`add_executable` wymienia trzy pliki `.cpp`,** w jednej linijce, bez nagłówka.
10. **Wyniki są takie jak w lekcji 10.3** dla wszystkich 19 przypadków, bo odczyt, zasady i format raportu się nie zmieniły.

Inne poprawne rozwiązania: inne nazwy plików, typu i funkcji; jedna funkcja analityczna z pętlą, jeśli pozostałe jednostki liczy tylko ona i raport bierze je z niej; deklaracje bez nazw parametrów.

</details>

<details>
<summary>Punkt 8: pełna lista przypadków kontrolnych z lekcji 10.3</summary>

Te same przypadki co w tabeli z lekcji 10.3, punkt 8, z tymi samymi wynikami. Wszystkie są sprawdzone automatycznie dla rozwiązania powyżej.

Ujemna liczba zleceń:

<!-- input: orders -->
```text
-1
```

<!-- output: orders -->
```text
Invalid orders
```

Jedno, dwa i pięć zleceń, także ten sam klient dwa razy:

<!-- input: orders -->
```text
1
Harbor Office
10 3
```

<!-- output: orders -->
```text
Orders: 1
Harbor Office: planned 10, completed 3, remaining 7
Remaining total: 7
```

<!-- input: orders -->
```text
2
Park School
9 4
City Archive
8 2
```

<!-- output: orders -->
```text
Orders: 2
Park School: planned 9, completed 4, remaining 5
City Archive: planned 8, completed 2, remaining 6
Remaining total: 11
```

<!-- input: orders -->
```text
5
Art Room
4 1
Book Club
6 6
Art Room
3 0
Main Office
10 9
Tool Shed
2 1
```

<!-- output: orders -->
```text
Orders: 5
Art Room: planned 4, completed 1, remaining 3
Book Club: planned 6, completed 6, remaining 0
Art Room: planned 3, completed 0, remaining 3
Main Office: planned 10, completed 9, remaining 1
Tool Shed: planned 2, completed 1, remaining 1
Remaining total: 8
```

Liczba zleceń większa od 5 i słowo zamiast liczby zleceń:

<!-- input: orders -->
```text
6
```

<!-- output: orders -->
```text
Invalid orders
```

<!-- input: orders -->
```text
three
```

<!-- output: orders -->
```text
Input error
```

Pusta nazwa pierwszego i późniejszego zlecenia:

<!-- input: orders -->
```text
2

12 5
City Archive
8 8
```

<!-- output: orders -->
```text
Invalid orders
```

<!-- input: orders -->
```text
2
North Library
12 5

8 8
```

<!-- output: orders -->
```text
Invalid orders
```

Zero zaplanowanych jednostek, ujemne zaplanowane i ujemne ukończone:

<!-- input: orders -->
```text
2
North Library
12 5
City Archive
0 0
```

<!-- output: orders -->
```text
Invalid orders
```

<!-- input: orders -->
```text
1
North Library
-4 0
```

<!-- output: orders -->
```text
Invalid orders
```

<!-- input: orders -->
```text
1
North Library
12 -1
```

<!-- output: orders -->
```text
Invalid orders
```

Słowo zamiast pierwszej liczby, brak zapowiedzianego zlecenia i brak ostatniej liczby:

<!-- input: orders -->
```text
2
North Library
twelve 5
City Archive
8 8
```

<!-- output: orders -->
```text
Input error
```

<!-- input: orders -->
```text
2
North Library
12 5
```

<!-- output: orders -->
```text
Input error
```

<!-- input: orders -->
```text
2
North Library
12 5
City Archive
8
```

<!-- output: orders -->
```text
Input error
```

</details>

<details>
<summary>Punkt 9: poprawiony projekt</summary>

Po usunięciu drugiej definicji `total_boxes` z `shipments_report.cpp` wszystkie pięć plików jest takich samych jak w punktach 3–7. Funkcja sumująca jest zdefiniowana raz, w `shipments_analysis.cpp`, a plik raportu ją wywołuje. Program buduje się i dla danych A wypisuje ten sam raport co w punkcie 7. Ten projekt, z wszystkimi 11 przypadkami, jest sprawdzany automatycznie.

</details>

**Poprzednia lekcja:** [Lekcja 11.3: Wspólny typ w nagłówku](lesson_03_shared_type_in_header.md) · **Następna lekcja:** [Lekcja 11.5: Sprawdzian — samodzielny program wieloplikowy](lesson_05_multifile_checkpoint.md) · [Opis kursu](../../README.md)

# Lekcja 11.5: Samodzielny program wieloplikowy (sprawdzian Modułu 11)

**Polski** · [English](lesson_05_multifile_checkpoint.en.md) · [Opis kursu](../../README.md)

> **Moduł 11, lekcja 5: sprawdzian** · około 100–120 minut, w dwóch podejściach
> **Potrzebujesz:** katalogu `cpp-workspace` i oryginalnego projektu `lesson_05_first_program`.
> **Wersja pilotażowa.** Rozwiązanie referencyjne i projekt z diagnostyki sprawdzamy automatycznie na Windowsie, Ubuntu i macOS, z podanymi danymi wejściowymi. Twojego projektu nic nie ocenia automatycznie: sprawdzasz go samodzielnie, według kryteriów. Kroki w CLionie są takie jak w lekcjach 11.1–11.4 i nie zostały ręcznie sprawdzone na każdym systemie.

## Jak przebiega ten sprawdzian

Ta lekcja nie wprowadza niczego nowego. Sprawdzasz, czy potrafisz **samodzielnie zaprojektować, zbudować i sprawdzić niewielki program w kilku plikach**, bez gotowego podziału i bez gotowych funkcji. Łączysz w nim lekcje 11.1–11.4 z odczytem listy rekordów z lekcji 10.3.

Sprawdzian ma trzy części i omówienie:

- **Część A: projekt.** Plan podziału programu na pliki, zanim napiszesz kod.
- **Część B: implementacja i testy.** Program według specyfikacji, sprawdzony przypadkami kontrolnymi. To największa część pracy.
- **Część C: diagnostyka i uzasadnienie.** Błąd linkowania w gotowym projekcie i pytania o Twoje decyzje. Wykonaj ją po części B.
- **Sprawdzenie i omówienie:** podpowiedzi, pełna lista przypadków, projekt do diagnostyki, rozwiązanie referencyjne, odpowiedzi i samoocena. Przejdź tam dopiero po częściach A i B albo wtedy, gdy świadomie zrezygnujesz z dalszej samodzielnej próby.

Zajrzenie do podpowiedzi albo do wcześniejszych lekcji nie jest porażką. Ważne jest, żeby **uczciwie zanotować, co zrobiono samodzielnie, a co z pomocą**. Proponowany podział na dwa podejścia:

- **pierwsze:** specyfikacja, część A i wspólny nagłówek;
- **drugie:** pliki `.cpp`, `CMakeLists.txt`, przypadki kontrolne i część C.

**Możesz używać:** CLiona albo terminala, CMake i Ninja, jak dotąd; `CMakeLists.txt` skopiowanego z oryginalnego `lesson_05_first_program`; lekcji 10.3 i 11.1–11.4 jako przypomnienia; tabel przypadków. Debugger nie jest potrzebny. Wszystko, czego potrzebujesz, znasz z Modułów 1–11.

---

## Specyfikacja: wolne miejsca w salach warsztatowych

Organizator prowadzi kilka sal warsztatowych. O każdej wie, jak się nazywa, ile ma wszystkich miejsc i ile z nich jest już zajętych. Program odczytuje listę sal i wypisuje, ile wolnych miejsc ma każda sala i ile jest ich razem. Nie modeluje terminów, rezerwacji ani uczestników.

**Przygotowanie:** w `cpp-workspace` utwórz katalog `workshop_rooms` i skopiuj do niego `CMakeLists.txt` z oryginalnego `lesson_05_first_program`. Pozostałe pliki utworzysz samodzielnie.

### Dane wejściowe

Pierwsza linia podaje liczbę sal. Potem każda sala zajmuje dwie linie:

1. nazwa sali, która może zawierać spacje;
2. dwie liczby całkowite oddzielone spacją: pojemność, czyli liczba wszystkich miejsc, i liczba miejsc zajętych.

### Zasady

- Sal jest od 0 do 5.
- Nazwa sali nie może być pusta. W danych zgodnych z umową nie ma spacji na jej początku ani końcu, a program ich nie sprawdza ani nie usuwa. Nazwy mogą się powtarzać: każda sala jest osobnym rekordem.
- Pojemność wynosi od 1 do 100.
- Liczba zajętych miejsc wynosi od 0 do pojemności sali.
- Wszystkie dane są tekstem ASCII. Tekst po drugiej liczbie jest poza umową i program go nie sprawdza.

### Błędy

- Gdy nie uda się odczytać wymaganych danych, program wypisuje dokładnie `Input error`.
- Gdy odczyt się udał, ale liczba sal albo wartości którejś sali łamią zasady, program wypisuje dokładnie `Invalid rooms`.
- Przy pierwszym błędzie program wypisuje komunikat i kończy pracę, bez żadnej części raportu.
- **Najpierw odczyt, potem zasady,** jak w lekcji 10.3: program sprawdza, czy udał się odczyt **obu** liczb bieżącej sali, a dopiero potem ich wartości. Po nieudanym odczycie nie próbuje czytać dalej.

### Raport

Dla poprawnych danych program wypisuje liczbę sal, jedną linię na każdą salę, w kolejności z danych, i łączną liczbę wolnych miejsc:

```text
Rooms: LICZBA_SAL
NAZWA: capacity POJEMNOŚĆ, occupied ZAJĘTE, free WOLNE
Free seats total: SUMA
```

Wolne miejsca sali to pojemność minus zajęte miejsca, a suma to suma wolnych miejsc wszystkich sal. **Obliczenie wolnych miejsc stoi w programie w jednym miejscu.** Program nie sortuje sal i nie usuwa powtórzeń.

### Wymagana struktura

- **`main.cpp`** odczytuje i sprawdza dane, buduje kolekcję sal, wypisuje komunikaty błędów i uruchamia raport dopiero po poprawnym odczycie wszystkich sal.
- **Przynajmniej jeden wspólny nagłówek,** samowystarczalny, z `#pragma once`: typ sali i deklaracje funkcji, których potrzebują inne pliki.
- **Osobny plik `.cpp` z obliczeniami:** wolne miejsca jednej sali i ich suma dla wszystkich sal. Nie odczytuje, nie wypisuje i nie zmienia rekordów.
- **Osobny plik `.cpp` z raportem:** wypisuje raport i korzysta z funkcji obliczeniowych.
- **`CMakeLists.txt`** z lekcji 0.5, w którym `add_executable(first_program ...)` wymienia wszystkie potrzebne pliki `.cpp`.

Nie dołączaj plików `.cpp` przez `#include` i nie kopiuj definicji funkcji między plikami. Program, którego cały kod stoi w `main.cpp`, nie spełnia wymagań, nawet jeśli wypisuje dobre wyniki.

**Zdecyduj samodzielnie:**

1. jak nazwać pliki z obliczeniami i z raportem oraz nagłówek;
2. jak nazwać typ sali;
3. jak nazwać jego pola;
4. jak nazwać funkcje;
5. jakie parametry mają funkcje;
6. jakie typy zwracają;
7. które deklaracje są potrzebne innym plikom;
8. jak podzielić obliczenia i raport;
9. jakie nagłówki standardowe dołącza każdy plik;
10. jakie pliki wymienić w `add_executable`;
11. jak przekazywać kolekcję sal;
12. jak sprawdzić, że rozwiązanie jest poprawne.

Przypomnienie znajdziesz w lekcjach [11.1](lesson_01_second_source_file.md) (drugi plik i `add_executable`), [11.2](lesson_02_own_header_file.md) (nagłówek), [11.3](lesson_03_shared_type_in_header.md) (typ w nagłówku) i [11.4](lesson_04_splitting_responsibilities.md) (podział według odpowiedzialności), a odczyt listy rekordów w [lekcji 10.3](../module_10_input_records/lesson_03_building_a_vector_of_records.md).

---

# Część A: projekt

Zanim napiszesz kod, przygotuj na piśmie tabelę dla wszystkich plików swojego projektu:

| Plik | Odpowiedzialność | Dane wejściowe | Wynik |
|---|---|---|---|
| | | | |

Odpowiedz też krótko:

1. Co musi być wspólne dla kilku plików?
2. Które funkcje mogą pozostać szczegółem jednego pliku `.cpp`?
3. Od którego pliku zaczyna się działanie programu?
4. Które pliki kompiluje CMake?
5. Jak wynik obliczeń trafia do raportu?

Plan jest obowiązkową częścią sprawdzianu i jest oceniany razem z programem.

---

# Część B: implementacja i testy

Napisz program według specyfikacji i swojego planu. **Przed uruchomieniem** przygotuj tabelę przypadków: dane i przewidywany wynik. Wyniki poniżej wynikają wprost z umowy.

**A**, trzy sale: nazwy ze spacjami, sala częściowo zajęta, pełna i pusta:

<!-- input: rooms -->
```text
3
North Hall
12 7
South Lab
8 8
Quiet Room
6 0
```

<!-- output: rooms -->
```text
Rooms: 3
North Hall: capacity 12, occupied 7, free 5
South Lab: capacity 8, occupied 8, free 0
Quiet Room: capacity 6, occupied 0, free 6
Free seats total: 11
```

**B**, brak sal:

<!-- input: rooms -->
```text
0
```

<!-- output: rooms -->
```text
Rooms: 0
Free seats total: 0
```

**C**, w drugiej sali więcej zajętych miejsc niż pojemność. Pierwsza sala była poprawna, ale nie ma częściowego raportu:

<!-- input: rooms -->
```text
2
North Hall
12 7
South Lab
8 9
```

<!-- output: rooms -->
```text
Invalid rooms
```

**D**, słowo zamiast liczby zajętych miejsc w drugiej sali:

<!-- input: rooms -->
```text
2
North Hall
12 7
South Lab
8 done
```

<!-- output: rooms -->
```text
Input error
```

**E**, pojemność 0 w drugiej sali, a potem słowo zamiast drugiej liczby. Nieudany odczyt ma pierwszeństwo przed sprawdzaniem wartości, więc to nie jest `Invalid rooms`:

<!-- input: rooms -->
```text
2
North Hall
12 7
South Lab
0 done
```

<!-- output: rooms -->
```text
Input error
```

**F**, pusta nazwa sali:

<!-- input: rooms -->
```text
1

12 7
```

<!-- output: rooms -->
```text
Invalid rooms
```

**G**, pojemność 0:

<!-- input: rooms -->
```text
1
North Hall
0 0
```

<!-- output: rooms -->
```text
Invalid rooms
```

**H**, więcej niż 5 sal:

<!-- input: rooms -->
```text
6
```

<!-- output: rooms -->
```text
Invalid rooms
```

**I**, słowo zamiast liczby sal:

<!-- input: rooms -->
```text
three
```

<!-- output: rooms -->
```text
Input error
```

**J**, dwie sale o tej samej nazwie: obie zostają w raporcie:

<!-- input: rooms -->
```text
2
East Wing
10 3
East Wing
5 0
```

<!-- output: rooms -->
```text
Rooms: 2
East Wing: capacity 10, occupied 3, free 7
East Wing: capacity 5, occupied 0, free 5
Free seats total: 12
```

**Uruchom obowiązkowo:** A, B i jeden z przypadków C albo D. Pozostałe przewidź w swojej tabeli i porównaj z pełną listą przypadków w części „Sprawdzenie i omówienie”. Wszystkie są sprawdzone automatycznie dla rozwiązania referencyjnego. Dane, które kończą się zaraz po ostatniej liczbie, bez końca linii, dają ten sam wynik. Tego przypadku testy automatyczne nie uruchamiają, jak w lekcji 10.3.

---

# Część C: diagnostyka i uzasadnienie

Wykonaj tę część **po części B**.

## Diagnostyka: brakująca definicja

Projekt `rooms_link_check` jest w części [Sprawdzenie i omówienie](#projekt-do-diagnostyki). Ma stałe nazwy plików: `main.cpp`, `rooms.hpp`, `rooms_analysis.cpp`, `rooms_report.cpp` i `CMakeLists.txt`. Zawiera kod bardzo zbliżony do rozwiązania referencyjnego, dlatego otwórz go dopiero teraz. Odtwórz go w katalogu `rooms_link_check`, zbuduj i:

1. ustal, na którym etapie budowanie się nie udaje;
2. wyjaśnij, co oznacza komunikat o brakującej definicji;
3. sprawdź deklaracje w nagłówku i definicje w plikach `.cpp`;
4. sprawdź listę plików w `add_executable`;
5. popraw projekt, zbuduj go ponownie i uruchom dla danych A;
6. wyjaśnij, dlaczego `#include "rooms_analysis.cpp"` nie jest właściwą poprawką.

**Na koniec, na piśmie:** czym różni się ten problem od sytuacji, w której ta sama funkcja jest zdefiniowana w dwóch plikach `.cpp`?

## Uzasadnienie

Odpowiedz własnymi słowami, odnosząc się do swojego projektu:

1. Po co w Twoim projekcie jest wspólny nagłówek i co w nim stoi?
2. Czym różni się deklaracja funkcji od jej definicji? Gdzie stoi jedna, a gdzie druga?
3. Dlaczego żaden plik nie dołącza pliku `.cpp`?
4. Czy każda Twoja funkcja musi być zadeklarowana we wspólnym nagłówku?
5. Dlaczego pliki `.cpp` trzeba wymienić w `add_executable`?
6. Po czym poznać, czy błąd pochodzi z kompilacji, czy z linkowania?
7. Dlaczego obliczenia stoją w innym pliku niż raport?
8. Co daje przekazanie kolekcji sal przez `const&`?
9. Czego przypadki kontrolne nie mówią o strukturze programu? Jak sprawdzić, że zmiana podziału nie zmieniła jego działania?

---

## Lista kontrolna przed oddaniem

Sprawdzian jest zaliczony, gdy spełniasz **wszystkie** punkty tej listy. Twój podział na funkcje i pliki może być inny niż w rozwiązaniu referencyjnym, jeśli spełnia specyfikację.

- [ ] Plan z części A powstał przed kodem i zgadza się z programem.
- [ ] Typ sali jest zdefiniowany raz, we wspólnym nagłówku z `#pragma once`, który sam dołącza potrzebne nagłówki standardowe.
- [ ] Nagłówek zawiera definicję typu i deklaracje, bez definicji funkcji.
- [ ] Obliczenia i raport stoją w dwóch osobnych plikach `.cpp`, a każda funkcja jest zdefiniowana dokładnie raz.
- [ ] Wolne miejsca liczy jedna funkcja, a suma i raport z niej korzystają.
- [ ] Plik z obliczeniami niczego nie odczytuje ani nie wypisuje.
- [ ] Kolekcja i elementy, które są tylko odczytywane, są przekazywane przez `const&`.
- [ ] `main.cpp` sprawdza odczyt obu liczb przed zasadami, a przy błędzie kończy pracę bez części raportu.
- [ ] `add_executable` wymienia wszystkie pliki `.cpp`, bez nagłówka, a żaden plik nie dołącza pliku `.cpp`.
- [ ] Dla A, B oraz C albo D wynik zgadza się co do znaku, a pozostałe przypadki z tabeli zgadzają się z pełną listą.
- [ ] Część C jest wykonana: błąd z diagnostyki jest poprawiony i sprawdzony, a odpowiedzi z uzasadnienia odnoszą się do Twojego projektu.

## Kryteria oceny

Rubryka służy do samooceny albo do oceny przez prowadzącego. Kurs nie ma skali ocen ani progu punktowego: punkty pokazują, które obszary są opanowane, a które wymagają powtórki. O zaliczeniu decyduje lista kontrolna powyżej, a nie liczba punktów.

| Obszar | Punkty | Pełne punkty, gdy |
|---|---:|---|
| Plan podziału odpowiedzialności | 15 | tabela powstała przed kodem, każdy plik ma opisaną rolę, dane i wynik, a odpowiedzi na pięć pytań zgadzają się z programem |
| Wspólny nagłówek, typ i deklaracje | 15 | typ jest zdefiniowany raz, nagłówek ma `#pragma once`, jest samowystarczalny i deklaruje funkcje potrzebne innym plikom, bez ich definicji |
| Pliki implementacyjne i CMake | 15 | obliczenia i raport w osobnych plikach `.cpp`, każda funkcja zdefiniowana raz, żaden plik nie dołącza `.cpp`, a `add_executable` wymienia wszystkie pliki `.cpp` |
| Odczyt i sprawdzanie danych | 20 | odczyt obu liczb jest sprawdzany przed zasadami, wszystkie zasady są sprawdzane, komunikaty są dokładne, a po błędzie nie ma części raportu |
| Obliczenia, raport i przekazywanie danych | 15 | wolne miejsca liczy jedna funkcja, suma z niej korzysta, raport bierze obie wartości z obliczeń, kolekcja i elementy są przekazywane przez `const&` |
| Poprawność wyników i testowanie | 10 | A, B oraz C albo D dają dokładny wynik, a tabela przypadków powstała przed uruchomieniem i zgadza się z pełną listą |
| Diagnostyka i uzasadnienie | 10 | błąd linkowania jest rozpoznany i poprawiony przez `add_executable`, a odpowiedzi z części C są poprawne i odnoszą się do projektu |
| **Razem** | **100** | |

- **Poprawny wynik nie daje automatycznie wszystkich punktów:** obszary planu, nagłówka i plików ocenia się, czytając projekt.
- **Program w jednym pliku** nie spełnia wymagań struktury: nie dostaje punktów za nagłówek ani za pliki implementacyjne i CMake, nawet z dobrym wynikiem.
- **Błędny `add_executable`**, na przykład bez pliku z obliczeniami albo z dołączonym plikiem `.cpp`, oznacza brak punktów za pliki implementacyjne i CMake.
- **Częściowy raport po błędzie** narusza umowę: oznacza brak punktów za odczyt i sprawdzanie danych w tej części.
- **Inne nazwy** typu, pól, funkcji i plików nie odbierają punktów. Inny, uzasadniony podział, na przykład dwa nagłówki, ocenia się według tych samych kompetencji, a nie według zgodności z rozwiązaniem referencyjnym.

**Co sprawdza automat, a co nie.** Testy kursu sprawdzają, że rozwiązanie referencyjne się buduje i daje pokazane wyniki. Twoje uruchomienia przypadków kontrolnych sprawdzają zachowanie Twojego programu dla tych danych. **Jakości podziału, samodzielności i uzasadnienia nie sprawdza żaden automat:** ocenia je człowiek, czytając plan i pliki.

---

# Sprawdzenie i omówienie

Przejdź tutaj **dopiero po częściach A i B** albo wtedy, gdy świadomie zrezygnujesz z dalszej samodzielnej próby. Dalej jest kod bardzo zbliżony do rozwiązania.

## Podpowiedzi

<details>
<summary>Podpowiedź 1: struktura</summary>

Które działania programu zależą od danych wejściowych, które tylko liczą, a które tylko wypisują? Każdej z tych grup przypisz jeden plik.

</details>

<details>
<summary>Podpowiedź 2: interfejs</summary>

Który typ i które funkcje są używane w więcej niż jednym pliku? To one należą do wspólnego nagłówka. Pamiętaj, jakie nagłówki standardowe są potrzebne samym deklaracjom.

</details>

<details>
<summary>Podpowiedź 3: przepływ i CMake</summary>

`main` przekazuje gotową kolekcję do raportu, a raport prosi obliczenia o wolne miejsca jednej sali i o sumę. Linker połączy te wywołania tylko z definicjami z plików wymienionych w `add_executable`.

</details>

## Pełna lista przypadków kontrolnych

<details>
<summary>Przypadki K–T, sprawdzone automatycznie dla rozwiązania referencyjnego</summary>

**K**, jedna sala o największej pojemności:

<!-- input: rooms -->
```text
1
Main Hall
100 99
```

<!-- output: rooms -->
```text
Rooms: 1
Main Hall: capacity 100, occupied 99, free 1
Free seats total: 1
```

**L**, pięć sal, także o pojemności 1:

<!-- input: rooms -->
```text
5
Room One
10 2
Room Two
20 20
Room Three
1 0
Room Four
100 50
Room Five
7 3
```

<!-- output: rooms -->
```text
Rooms: 5
Room One: capacity 10, occupied 2, free 8
Room Two: capacity 20, occupied 20, free 0
Room Three: capacity 1, occupied 0, free 1
Room Four: capacity 100, occupied 50, free 50
Room Five: capacity 7, occupied 3, free 4
Free seats total: 63
```

**M**, ujemna liczba sal:

<!-- input: rooms -->
```text
-1
```

<!-- output: rooms -->
```text
Invalid rooms
```

**N**, ujemna pojemność:

<!-- input: rooms -->
```text
1
North Hall
-5 0
```

<!-- output: rooms -->
```text
Invalid rooms
```

**O**, pojemność 101:

<!-- input: rooms -->
```text
1
North Hall
101 0
```

<!-- output: rooms -->
```text
Invalid rooms
```

**P**, ujemna liczba zajętych miejsc:

<!-- input: rooms -->
```text
1
North Hall
12 -1
```

<!-- output: rooms -->
```text
Invalid rooms
```

**Q**, zapowiedziane 2 sale, a dane kończą się w miejscu nazwy drugiej. To nie jest pusta nazwa, jak w F, tylko nieudany odczyt:

<!-- input: rooms -->
```text
2
North Hall
12 7
```

<!-- output: rooms -->
```text
Input error
```

**R**, brak obu liczb sali:

<!-- input: rooms -->
```text
1
North Hall
```

<!-- output: rooms -->
```text
Input error
```

**S**, brak drugiej liczby sali:

<!-- input: rooms -->
```text
1
North Hall
12
```

<!-- output: rooms -->
```text
Input error
```

**T**, słowo zamiast pojemności:

<!-- input: rooms -->
```text
1
North Hall
twelve 7
```

<!-- output: rooms -->
```text
Input error
```

</details>

## Projekt do diagnostyki

<details>
<summary>Projekt rooms_link_check: otwórz po części B</summary>

**`CMakeLists.txt`**:

<!-- cmake: rooms_link_check -->
```cmake
cmake_minimum_required(VERSION 3.28)
project(first_program LANGUAGES CXX)

add_executable(first_program main.cpp rooms_report.cpp)
target_compile_features(first_program PRIVATE cxx_std_20)
set_target_properties(first_program PROPERTIES CXX_EXTENSIONS OFF)
```

**`main.cpp`**:

<!-- broken: rooms_link_check stage=link error=undefined reference to .free_seats\(Room const&\)'|undefined symbol: int __cdecl free_seats\(struct Room const &\)|"free_seats\(Room const&\)", referenced from -->
```cpp
#include <iostream>
#include <string>
#include <vector>

#include "rooms.hpp"

int main() {
    std::vector<Room> rooms{};
    int count{0};
    std::cin >> count;

    if (std::cin.fail()) {
        std::cout << "Input error\n";
        return 0;
    }

    if (count < 0 || count > 5) {
        std::cout << "Invalid rooms\n";
        return 0;
    }

    for (int index{0}; index < count; ++index) {
        std::string rest{};
        std::getline(std::cin, rest);

        std::string name{};
        int capacity{0};
        int occupied{0};
        std::getline(std::cin, name);
        std::cin >> capacity;
        std::cin >> occupied;

        if (std::cin.fail()) {
            std::cout << "Input error\n";
            return 0;
        }

        if (name.empty() || capacity < 1 || capacity > 100 || occupied < 0 || occupied > capacity) {
            std::cout << "Invalid rooms\n";
            return 0;
        }

        const Room room{name, capacity, occupied};
        rooms.push_back(room);
    }

    print_rooms(rooms);
}
```

**`rooms.hpp`**:

<!-- file: rooms_link_check rooms.hpp -->
```cpp
#pragma once

#include <string>
#include <vector>

struct Room {
    std::string name;
    int capacity;
    int occupied;
};

int free_seats(const Room& room);
int free_seats_total(const std::vector<Room>& rooms);
void print_rooms(const std::vector<Room>& rooms);
```

**`rooms_analysis.cpp`**:

<!-- file: rooms_link_check rooms_analysis.cpp -->
```cpp
#include "rooms.hpp"

int free_seats(const Room& room) {
    return room.capacity - room.occupied;
}

int free_seats_total(const std::vector<Room>& rooms) {
    int total{0};

    for (const Room& room : rooms) {
        total += free_seats(room);
    }

    return total;
}
```

**`rooms_report.cpp`**:

<!-- file: rooms_link_check rooms_report.cpp -->
```cpp
#include <iostream>

#include "rooms.hpp"

void print_rooms(const std::vector<Room>& rooms) {
    std::cout << "Rooms: " << rooms.size() << "\n";

    for (const Room& room : rooms) {
        std::cout << room.name << ": capacity " << room.capacity << ", occupied " << room.occupied
                  << ", free " << free_seats(room) << "\n";
    }

    std::cout << "Free seats total: " << free_seats_total(rooms) << "\n";
}
```

</details>

## Rozwiązanie referencyjne

<details>
<summary>Plan i pięć plików rozwiązania referencyjnego</summary>

To jedno z poprawnych rozwiązań, a nie jedyna dopuszczalna struktura.

| Plik | Odpowiedzialność | Dane wejściowe | Wynik |
|---|---|---|---|
| `main.cpp` | odczyt, sprawdzanie danych, budowanie kolekcji i sterowanie | standardowe wejście | wektor poprawnych sal albo komunikat `Input error` lub `Invalid rooms` |
| `rooms.hpp` | wspólny typ i deklaracje | — | `struct Room` i deklaracje trzech funkcji |
| `rooms_analysis.cpp` | obliczenia | jedna sala albo wektor sal | wolne miejsca sali i ich suma, liczby `int` |
| `rooms_report.cpp` | raport | wektor sal | linie raportu na standardowym wyjściu |

**`rooms.hpp`**:

<!-- file: rooms rooms.hpp -->
```cpp
#pragma once

#include <string>
#include <vector>

struct Room {
    std::string name;
    int capacity;
    int occupied;
};

int free_seats(const Room& room);
int free_seats_total(const std::vector<Room>& rooms);
void print_rooms(const std::vector<Room>& rooms);
```

**`rooms_analysis.cpp`**:

<!-- file: rooms rooms_analysis.cpp -->
```cpp
#include "rooms.hpp"

int free_seats(const Room& room) {
    return room.capacity - room.occupied;
}

int free_seats_total(const std::vector<Room>& rooms) {
    int total{0};

    for (const Room& room : rooms) {
        total += free_seats(room);
    }

    return total;
}
```

**`rooms_report.cpp`**:

<!-- file: rooms rooms_report.cpp -->
```cpp
#include <iostream>

#include "rooms.hpp"

void print_rooms(const std::vector<Room>& rooms) {
    std::cout << "Rooms: " << rooms.size() << "\n";

    for (const Room& room : rooms) {
        std::cout << room.name << ": capacity " << room.capacity << ", occupied " << room.occupied
                  << ", free " << free_seats(room) << "\n";
    }

    std::cout << "Free seats total: " << free_seats_total(rooms) << "\n";
}
```

**`main.cpp`**:

<!-- example: rooms -->
```cpp
#include <iostream>
#include <string>
#include <vector>

#include "rooms.hpp"

int main() {
    std::vector<Room> rooms{};
    int count{0};
    std::cin >> count;

    if (std::cin.fail()) {
        std::cout << "Input error\n";
        return 0;
    }

    if (count < 0 || count > 5) {
        std::cout << "Invalid rooms\n";
        return 0;
    }

    for (int index{0}; index < count; ++index) {
        std::string rest{};
        std::getline(std::cin, rest);

        std::string name{};
        int capacity{0};
        int occupied{0};
        std::getline(std::cin, name);
        std::cin >> capacity;
        std::cin >> occupied;

        if (std::cin.fail()) {
            std::cout << "Input error\n";
            return 0;
        }

        if (name.empty() || capacity < 1 || capacity > 100 || occupied < 0 || occupied > capacity) {
            std::cout << "Invalid rooms\n";
            return 0;
        }

        const Room room{name, capacity, occupied};
        rooms.push_back(room);
    }

    print_rooms(rooms);
}
```

**`CMakeLists.txt`**:

<!-- cmake: rooms -->
```cmake
cmake_minimum_required(VERSION 3.28)
project(first_program LANGUAGES CXX)

add_executable(first_program main.cpp rooms_analysis.cpp rooms_report.cpp)
target_compile_features(first_program PRIVATE cxx_std_20)
set_target_properties(first_program PROPERTIES CXX_EXTENSIONS OFF)
```

1. **`Room` jest zdefiniowany w `rooms.hpp`,** bo korzystają z niego wszystkie trzy pliki `.cpp`. Nagłówek sam dołącza `<string>` i `<vector>`, których wymagają jego deklaracje.
2. **Nagłówek deklaruje trzy funkcje,** bo każdej używa inny plik: `main.cpp` wywołuje `print_rooms`, a `rooms_report.cpp` wywołuje `free_seats` i `free_seats_total`.
3. **Wzór `room.capacity - room.occupied` stoi raz,** w `free_seats`. Korzystają z niego suma i linia raportu.
4. **`free_seats_total` sumuje wyniki `free_seats`,** zamiast powtarzać wzór.
5. **Kolekcja i elementy są przekazywane przez `const&`,** bo funkcje tylko je odczytują.
6. **`rooms_analysis.cpp` niczego nie odczytuje ani nie wypisuje,** a `rooms_report.cpp` niczego nie oblicza sam.
7. **`main.cpp` dokańcza linię liczbową przed każdą nazwą** przez `std::getline` do zmiennej `rest`, jak w lekcji 10.3. Pusta nazwa zostaje więc pustym tekstem, a nie jest pomijana.
8. **Odczyt obu liczb jest sprawdzany jednym `std::cin.fail()` przed zasadami,** więc dla E wynik to `Input error`. Przy błędzie `return 0;` kończy program przed wywołaniem `print_rooms`, więc nie ma częściowego raportu.
9. **Rekord powstaje i trafia do wektora dopiero po obu sprawdzeniach,** a raport opisuje wektor: liczba sal pochodzi z `size()`.
10. **`add_executable` wymienia trzy pliki `.cpp`,** w jednej linijce, bez nagłówka.

Inne poprawne rozwiązania: inne nazwy; obliczenia i raport w plikach o innych nazwach; osobny nagłówek z typem i drugi z deklaracjami, jeśli drugi sam dołącza pierwszy; jedna funkcja analizująca, jeśli wzór nadal stoi w jednym miejscu.

</details>

## Diagnostyka: wyjaśnienie i poprawka

<details>
<summary>Otwórz po wykonaniu diagnostyki</summary>

1. **Kompilują się dwa pliki:** `main.cpp` i `rooms_report.cpp`, bo tylko one są w `add_executable`. Oba są poprawne: znają `free_seats` i `free_seats_total` z deklaracji w `rooms.hpp`.
2. **Linkowanie się nie udaje,** bo `rooms_report.cpp` wywołuje te funkcje, a ich definicje stoją w `rooms_analysis.cpp`, którego nikt nie kompiluje. Komunikat wymienia brakujące funkcje: na Ubuntu `undefined reference to`, na macOS `referenced from`, na Windowsie `undefined symbol:`, a na końcu `linker command failed`. Programu nie ma.
3. **Deklaracje i definicje są poprawne** i do siebie pasują. Problem jest tylko w liście plików.
4. **Poprawka:** dopisz `rooms_analysis.cpp` do `add_executable`, czyli `add_executable(first_program main.cpp rooms_analysis.cpp rooms_report.cpp)`, a w CLionie wczytaj ponownie projekt CMake (lekcja 11.1). Po zbudowaniu program dla danych A wypisuje raport z części B, bo pliki są takie same jak w rozwiązaniu referencyjnym.
5. **`#include "rooms_analysis.cpp"` nie jest poprawką.** Wstawiłoby definicje do pliku, który je dołącza: w tym projekcie błąd by zniknął, ale gdy ktoś później dopisze `rooms_analysis.cpp` do `add_executable`, te same funkcje będą zdefiniowane dwa razy. Pliki `.cpp` łączy linker, a nie `#include` (lekcja 11.2).

**Odpowiedź na pytanie z części C.** Tu definicji brakuje: wywołanie nie ma czego połączyć, linker zgłasza `undefined reference` albo `undefined symbol`, a poprawką jest dopisanie pliku do `add_executable`. Gdy ta sama funkcja jest zdefiniowana w dwóch plikach `.cpp`, definicji jest za dużo: linker zgłasza `multiple definition` albo `duplicate symbol`, a poprawką jest usunięcie jednej definicji (lekcja 11.4). W obu przypadkach każdy plik z osobna się kompiluje, a błąd zgłasza linker.

</details>

## Odpowiedzi do pytań z części C

<details>
<summary>Przykładowe odpowiedzi, dla rozwiązania referencyjnego</summary>

1. Żeby typ sali i deklaracje funkcji istniały w jednym miejscu. Nagłówek definiuje `Room` i deklaruje funkcje, których używają inne pliki.
2. Deklaracja podaje nazwę, typ wyniku i parametry, ze średnikiem: stoi w nagłówku. Definicja zawiera też ciało funkcji: stoi w jednym pliku `.cpp`.
3. Bo dołączony plik `.cpp` wstawiłby definicje do innej jednostki translacji, a pliki `.cpp` łączy linker. Groziłoby to podwójną definicją.
4. Nie. Nagłówek deklaruje funkcje, których potrzebują inne pliki. Funkcja pomocnicza używana tylko w jednym pliku `.cpp` nie musi tam trafiać.
5. Bo CMake kompiluje i linkuje tylko pliki z tej listy. Plik spoza listy nie trafia do programu, więc jego definicji brakuje przy linkowaniu.
6. Błąd kompilacji wskazuje plik i linijkę w kodzie i pojawia się przy `Building CXX object`. Błąd linkowania pojawia się dopiero przy `Linking`, wymienia nazwę funkcji i kończy się `linker command failed`.
7. Bo obliczenie nie zależy od wyglądu raportu. Można zmienić format wypisywania bez zmiany obliczeń i sprawdzić obliczenia bez czytania wypisywania.
8. Funkcja odczytuje istniejącą kolekcję bez kopiowania jej i bez możliwości jej zmiany.
9. Przypadki sprawdzają zachowanie, a nie podział: program w jednym pliku dałby te same wyniki. Strukturę sprawdza się, czytając pliki. Zachowanie po zmianie podziału sprawdza się, uruchamiając te same przypadki, także błędne, i porównując pełne wyniki.

</details>

## Samoocena

Przy każdej kompetencji zaznacz jedną odpowiedź:

| Kompetencja | Samodzielnie | Z podpowiedzią | Po zajrzeniu do rozwiązania | Do powtórki |
|---|---|---|---|---|
| Plan odpowiedzialności plików | | | | |
| Deklaracje i definicje w odpowiednich plikach | | | | |
| Wspólny typ w nagłówku | | | | |
| Potrzebne `#include` w każdym pliku | | | | |
| Przekazywanie danych między funkcjami i plikami | | | | |
| Obliczenia oddzielone od raportu | | | | |
| `add_executable` z wszystkimi plikami `.cpp` | | | | |
| Umowa wejścia i wyjścia, bez częściowego raportu | | | | |
| Błędy kompilacji i linkowania | | | | |
| Przypadki normalne, graniczne i błędne | | | | |

Jeśli w kolumnie „Do powtórki” jest coś zaznaczone, wróć do odpowiedniej lekcji:

| Temat | Lekcja |
|---|---|
| drugi plik źródłowy, `add_executable`, brakujący plik przy linkowaniu | [11.1](lesson_01_second_source_file.md) |
| własny nagłówek, `#include "..."`, deklaracja a definicja | [11.2](lesson_02_own_header_file.md) |
| typ w nagłówku, `#pragma once`, samowystarczalny nagłówek | [11.3](lesson_03_shared_type_in_header.md) |
| podział według odpowiedzialności, podwójna definicja | [11.4](lesson_04_splitting_responsibilities.md) |
| odczyt listy rekordów, najpierw odczyt, potem zasady | [10.3](../module_10_input_records/lesson_03_building_a_vector_of_records.md) |

---

## Podsumowanie Modułu 11

Po pięciu lekcjach potrafisz:

- budować program z kilku plików `.cpp` i wymieniać je w `add_executable`;
- trzymać deklaracje funkcji i wspólne typy we własnym, samowystarczalnym nagłówku z `#pragma once`;
- dzielić program według odpowiedzialności: odczyt i sterowanie, obliczenia oraz raport;
- wywoływać funkcje zdefiniowane w innych plikach przez deklaracje z nagłówka, bez dołączania plików `.cpp`;
- odróżniać błędy kompilacji od błędów linkowania: brakującej i podwójnej definicji;
- sprawdzać, że zmiana organizacji plików nie zmieniła działania programu.

## Co dalej

To koniec Modułu 11. W Module 12, „Dane z plików tekstowych”, programy będą same otwierać pliki tekstowe i odczytywać z nich dane. Zacznij od pierwszej lekcji: [Lekcja 12.1: Pierwszy plik z danymi](../module_12_text_files/lesson_01_first_data_file.md).

**Poprzednia lekcja:** [Lekcja 11.4: Podział programu według odpowiedzialności](lesson_04_splitting_responsibilities.md) · **Następna lekcja:** [Lekcja 12.1: Pierwszy plik z danymi](../module_12_text_files/lesson_01_first_data_file.md) · [Opis kursu](../../README.md)

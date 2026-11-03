# Lekcja 11.2: Własny plik nagłówkowy

**Polski** · [English](lesson_02_own_header_file.en.md) · [Opis kursu](../../README.md)

> **Moduł 11, lekcja 2** · około 80–100 minut, możesz ją podzielić na dwa podejścia: punkty 1–6 i punkty 7–10
> **Potrzebujesz:** katalogu `cpp-workspace` z projektami `lesson_11_1` i `ticket_cost` z [lekcji 11.1](lesson_01_second_source_file.md). Debugger nie jest w tej lekcji potrzebny.
> **Wersja pilotażowa.** Programy z tej lekcji, zbudowane z kilku plików, sprawdzamy automatycznie na Windowsie, Ubuntu i macOS, z podanymi danymi wejściowymi. Kroki w CLionie (nowy plik nagłówkowy, wpisywanie danych w oknie **Run**) opisujemy według dokumentacji CLion 2026.2, bez ręcznego sprawdzenia na każdym systemie.

## Zanim zaczniesz

Ta lekcja zakłada, że:

- budujesz program z dwóch plików `.cpp`: deklaracja funkcji stoi w `main.cpp`, definicja w drugim pliku, a `add_executable` wymienia oba pliki (lekcja 11.1);
- wiesz, że preprocesor obsługuje linijki zaczynające się od `#`, a `#include <iostream>` wstawia deklaracje z biblioteki standardowej (lekcja 1.4);
- sprawdzasz, czy deklaracja pasuje do definicji (lekcje 5.6 i 11.1).

## Sytuacja

W lekcji 11.1 `main.cpp` miał własną kopię deklaracji `calculate_points`. Jeśli funkcję wywoła też trzeci plik `.cpp`, potrzebuje kolejnej kopii. Gdy funkcja dostanie nowy parametr, trzeba poprawić wszystkie kopie, a kompilator nie porówna ich ze sobą. W tej lekcji zapiszesz deklarację **raz**, we własnym **pliku nagłówkowym** `.hpp`, i dołączysz go do każdego pliku, który jej potrzebuje.

Po tej lekcji będziesz:

- tworzyć własny plik nagłówkowy z deklaracją funkcji i `#pragma once`;
- dołączać go przez `#include "points.hpp"` do pliku, który wywołuje funkcję, i do pliku z jej definicją;
- wyjaśniać, dlaczego definicja zostaje w pliku `.cpp`, a `add_executable` nadal wymienia tylko pliki `.cpp`;
- rozpoznawać błąd linkowania, gdy nagłówek zawiera deklarację, ale nigdzie nie ma pasującej definicji.

## 1. Przygotuj projekt

W `cpp-workspace` utwórz katalog `lesson_11_2` i skopiuj do niego z `lesson_11_1` trzy pliki: `main.cpp`, `points.cpp` i `CMakeLists.txt`. Katalogów budowania nie kopiuj, jak w lekcji 1.1. To ten sam kalkulator punktów co w lekcji 11.1, więc możesz skupić się na deklaracji. Otwórz katalog w CLionie albo przejdź do niego w terminalu, jak w lekcji 11.1, punkt 1.

## 2. Plik nagłówkowy `points.hpp`

**Plik nagłówkowy** (ang. *header file*) to plik z deklaracjami, które inne pliki dołączają przez `#include`. W tym kursie ma rozszerzenie `.hpp`. Spotkasz też `.h`, częste w starszym kodzie i w języku C.

Utwórz w katalogu `lesson_11_2`, obok `main.cpp`, plik `points.hpp`:

- **W CLionie** (według dokumentacji CLion 2026.2): w oknie **Project** kliknij prawym przyciskiem myszy katalog projektu i wybierz **New | C/C++ Header File**. Wpisz nazwę `points` i w polu typu wybierz `.hpp`, jeśli CLion proponuje inne rozszerzenie. Nie dodawaj pliku do targetu `first_program` (punkt 5). Nowy nagłówek CLiona domyślnie zawiera już linijki `#ifndef`, `#define` i `#endif`. Zastąp całą zawartość pliku tekstem poniżej.
- **W innym edytorze tekstu**: zapisz plik jako `points.hpp` w tym samym katalogu co `main.cpp`.

Potem **wytnij** deklarację `calculate_points` z `main.cpp` i wklej ją do `points.hpp`, pod linijką `#pragma once`:

**`points.hpp`**:

<!-- file: points points.hpp -->
```cpp
#pragma once

int calculate_points(int solved, int bonus);
```

- Nagłówek zawiera **deklarację**, zakończoną średnikiem, bez ciała funkcji.
- **Definicja zostaje w `points.cpp`.** Nagłówek dołączą dwa pliki `.cpp`, więc definicja zapisana w nagłówku trafiłaby do programu dwa razy, a linker zgłosiłby, że funkcja jest zdefiniowana więcej niż raz.

## 3. `#pragma once`

`#pragma once` stoi w pierwszej linijce własnego nagłówka. Mówi preprocesorowi: jeśli ten nagłówek został już dołączony do tej jednostki translacji (lekcja 11.1, punkt 6), nie przetwarzaj go drugi raz. Tak się może stać, gdy plik dołącza ten sam nagłówek pośrednio, przez inne nagłówki.

- **Działa w obrębie jednego pliku `.cpp`,** a nie całego programu. `main.cpp` i `points.cpp` kompilują się osobno i każdy z nich dostaje deklarację z nagłówka.
- **Nie zastępuje definicji i nie zmienia linkowania.**
- **To nie dzięki niemu ten program się kompiluje.** Nagłówek zawiera tylko deklarację funkcji, a zgodną deklarację można powtórzyć. `#pragma once` to nawyk, którego znaczenie będzie lepiej widać, gdy w nagłówku pojawi się definicja własnego typu.

`#pragma once` nie należy do standardu ISO C++20, ale obsługują go Clang i inne popularne kompilatory. W cudzym kodzie i w szablonie nowego nagłówka CLiona zobaczysz zamiast niego trzy linijki, `#ifndef`, `#define` i `#endif`, tak zwane strażniki nagłówka (ang. *include guards*). Służą temu samemu. W tym kursie ich nie piszesz.

## 4. `#include "points.hpp"` w obu plikach `.cpp`

W miejscu usuniętej deklaracji `main.cpp` dostaje `#include "points.hpp"`:

**`main.cpp`**:

<!-- example: points -->
```cpp
#include <iostream>

#include "points.hpp"

int main() {
    int solved{0};
    int bonus{0};

    std::cin >> solved;
    std::cin >> bonus;

    std::cout << "Points: " << calculate_points(solved, bonus) << "\n";
}
```

Ten sam nagłówek dołącza na początku `points.cpp`. Definicja się nie zmienia:

**`points.cpp`**:

<!-- file: points points.cpp -->
```cpp
#include "points.hpp"

int calculate_points(int solved, int bonus) {
    const int points_per_task{3};
    return solved * points_per_task + bonus;
}
```

**Co robi `#include`.** Gdy preprocesor przygotowuje plik do kompilacji (lekcja 1.4), `#include "points.hpp"` wstawia w tym miejscu treść nagłówka. Kompilator widzi więc w `main.cpp` deklarację, jakby była tam wpisana. `#include` niczego nie uruchamia i nie kompiluje ani nie linkuje `points.cpp`: to nadal robią CMake, Ninja i linker.

| Zapis | Co dołącza | Gdzie jest plik |
|---|---|---|
| `#include <iostream>` | nagłówek biblioteki standardowej | w katalogach biblioteki standardowej, które zna kompilator |
| `#include "points.hpp"` | własny nagłówek z projektu | w tym samym katalogu co dołączający plik |

**Dlaczego oba pliki.** `main.cpp` potrzebuje deklaracji, żeby skompilować wywołanie. `points.cpp` dołącza ją, żeby deklaracja i definicja stały obok siebie w jednej jednostce translacji. Deklaracja istnieje w jednym miejscu: po zmianie funkcji poprawiasz nagłówek i definicję, a każdy plik, który dołącza nagłówek, dostaje nową wersję.

**Zgodność nadal trzeba sprawdzać.** Nagłówek w `points.cpp` nie gwarantuje, że funkcja zdefiniowana pod nim jest tą zadeklarowaną. Funkcja o innej nazwie albo z innymi typami parametrów to dla C++ po prostu inna funkcja: kompilator tego nie zgłosi. Porównuj więc nazwę, typ wyniku i typy parametrów, jak w lekcji 11.1. Taką pomyłkę zobaczysz w punkcie 8.

## 5. `CMakeLists.txt` bez zmian

`CMakeLists.txt` zostaje taki jak w lekcji 11.1:

<!-- cmake: points -->
```cmake
cmake_minimum_required(VERSION 3.28)
project(first_program LANGUAGES CXX)

add_executable(first_program main.cpp points.cpp)
target_compile_features(first_program PRIVATE cxx_std_20)
set_target_properties(first_program PROPERTIES CXX_EXTENSIONS OFF)
```

- **Nagłówek nie jest osobno kompilowany ani linkowany.** Jego treść kompiluje się jako część każdego pliku `.cpp`, który go dołącza. Nie powstaje z niego osobny plik obiektowy.
- **W projekcie z tego kursu `add_executable` wymienia tylko pliki `.cpp`.** CMake pozwala dopisać do targetu także nagłówki, na przykład żeby środowisko programistyczne pokazywało je przy projekcie. Ten kurs tego nie robi: to zasada naszego prostego projektu, a nie reguła CMake. Jeśli CLion dopisał `points.hpp` do `add_executable`, usuń tę nazwę.

## 6. Zbuduj i uruchom

Zbuduj i uruchom program jak w lekcji 11.1, punkt 5. `CMakeLists.txt` się nie zmienił. Jeśli w CLionie albo w terminalu konfigurujesz nowy katalog `lesson_11_2`, konfiguracja jest taka sama jak tam.

W wyniku budowania nadal są **dwie** linijki `Building CXX object`, dla `main.cpp` i `points.cpp`, i jedna `Linking`. Dla `points.hpp` nie ma osobnej linijki:

```text
points.hpp ──#include──► main.cpp    ──►  kompilacja  ──►  main.cpp.o    ──┐
           ──#include──► points.cpp  ──►  kompilacja  ──►  points.cpp.o  ──┴──►  linkowanie  ──►  first_program
```

Dla danych:

<!-- input: points -->
```text
4 2
```

program wypisuje:

<!-- output: points -->
```text
Points: 14
```

**Przewidź** wynik dla `0 5`. Uruchomienie jest nieobowiązkowe.

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

To dokładnie te same wyniki co w lekcji 11.1. **Dodanie nagłówka zmienia organizację kodu, a nie wynik obliczeń.** Program nie działa też szybciej: korzyść dotyczy utrzymania deklaracji w jednym miejscu.

## 7. Misja: bilety z nagłówkiem

Przekształć swój projekt `ticket_cost` z lekcji 11.1 w projekt z własnym nagłówkiem. W `cpp-workspace` utwórz katalog `ticket_cost_header` i skopiuj do niego `main.cpp`, drugi plik `.cpp` i `CMakeLists.txt` z `ticket_cost`. Oryginał zostaw bez zmian: posłuży do porównania wyników. Jeśli nie masz tego projektu, odtwórz go z [rozwiązania misji z lekcji 11.1](lesson_01_second_source_file.md#przykładowe-rozwiązania).

**Wymagania:**

- Obliczenie się nie zmienia: bilet zwykły kosztuje 12 jednostek, ulgowy 7, funkcja zwraca łączny koszt, a `main` odczytuje obie liczby i wypisuje `Total cost: N`.
- Deklaracja funkcji stoi **tylko** w nagłówku, z `#pragma once` w pierwszej linijce.
- Definicja zostaje w drugim pliku `.cpp`. Nagłówek nie zawiera definicji.
- **Oba pliki `.cpp` dołączają ten sam nagłówek** przez `#include "..."`.
- `add_executable` nadal wymienia dwa pliki `.cpp`, bez nagłówka. Program ma jedno `main`.
- Nazwy funkcji i plików z lekcji 11.1 możesz zachować. Nazwa nagłówka składa się z małych liter angielskich, cyfr i `_` i kończy na `.hpp`. Przykładowe rozwiązanie używa `tickets.hpp`.
- Nie dodawaj nowych reguł ani sprawdzania danych.

Wyniki mają być takie same jak w lekcji 11.1. **Dane A:**

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

1. jak nazwać nagłówek;
2. co w nim zapisać;
3. gdzie stoi `#pragma once`;
4. gdzie stoi deklaracja funkcji;
5. co zostaje w `main.cpp`;
6. co zostaje w drugim pliku `.cpp`;
7. gdzie stoją obie linijki `#include` z nazwą nagłówka;
8. czy zostawić starą deklarację w `main.cpp`;
9. jakie pliki wymienia `CMakeLists.txt`;
10. jak wykazać, że zmiana organizacji nie zmieniła wyników.

**Potem** zbuduj program i uruchom go dla danych A i jednego przypadku granicznego: B albo C. Porównaj wyniki z wynikami projektu `ticket_cost` dla tych samych danych. Pozostałe przypadki przewidź. Wszystkie są sprawdzone automatycznie w rozwiązaniu referencyjnym.

### Kryterium sukcesu

- Program buduje się jako C++20, a dla danych A oraz B albo C wypisuje dokładnie pokazany wynik, ten sam co projekt z lekcji 11.1.
- Nagłówek zaczyna się od `#pragma once` i zawiera deklarację funkcji, bez definicji.
- W `main.cpp` nie ma ręcznie zapisanej deklaracji: jest `#include` nagłówka.
- Drugi plik `.cpp` dołącza ten sam nagłówek i zawiera jedyną definicję funkcji, zgodną z deklaracją.
- `add_executable` wymienia dwa pliki `.cpp`, bez nagłówka.
- Żaden plik nie dołącza pliku `.cpp`.

To, że program się buduje i wypisuje dobre wyniki, nie dowodzi jeszcze, że organizacja plików jest właściwa: zbędna kopia deklaracji w `main.cpp` też by się zbudowała. Dlatego sprawdź pliki według listy powyżej. Gdy wszystko się zgadza, możesz zapisać projekt w Gicie. Do commita należą teraz cztery pliki, także nagłówek.

<details>
<summary>Podpowiedź 1</summary>

W którym pliku powinna teraz mieszkać deklaracja funkcji? Zostaje jedna, a każdy plik, który jej potrzebuje, korzysta z tej samej.

</details>

<details>
<summary>Podpowiedź 2</summary>

Co powinny dołączać `main.cpp` i drugi plik `.cpp`, żeby korzystały z jednej deklaracji? W obu potrzebna jest ta sama linijka `#include`, z nazwą nagłówka w cudzysłowie.

</details>

<details>
<summary>Podpowiedź 3</summary>

Co powinno zostać w `add_executable`, a co powinno być w nagłówku? Lista plików do zbudowania się nie zmienia, a nagłówek zawiera tylko `#pragma once` i deklarację.

</details>

Przykładowe rozwiązanie jest w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 8. Znajdź błąd: deklaracja nie jest definicją

To zadanie wykonaj **po misji**. Ktoś poprawiał kalkulator punktów i w `points.cpp` przy definicji zgubił jedną literę: `calculate_point` zamiast `calculate_points`. Odtwórz ten projekt: w `cpp-workspace` utwórz katalog `points_name_check`, skopiuj do niego cztery pliki z `lesson_11_2` i w `points.cpp` usuń końcowe `s` z nazwy funkcji w definicji.

**`points.cpp`** w tym projekcie:

<!-- file: points_name_check points.cpp -->
```cpp
#include "points.hpp"

int calculate_point(int solved, int bonus) {
    const int points_per_task{3};
    return solved * points_per_task + bonus;
}
```

<details>
<summary>Pozostałe pliki, bez zmian względem punktów 4 i 5</summary>

**`main.cpp`**:

<!-- broken: points_name_check stage=link error=undefined reference to .calculate_points\(int, int\)'|undefined symbol: int __cdecl calculate_points\(int, int\)|"calculate_points\(int, int\)", referenced from -->
```cpp
#include <iostream>

#include "points.hpp"

int main() {
    int solved{0};
    int bonus{0};

    std::cin >> solved;
    std::cin >> bonus;

    std::cout << "Points: " << calculate_points(solved, bonus) << "\n";
}
```

**`points.hpp`**:

<!-- file: points_name_check points.hpp -->
```cpp
#pragma once

int calculate_points(int solved, int bonus);
```

**`CMakeLists.txt`**:

<!-- cmake: points_name_check -->
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
2. Co deklaruje `points.hpp`?
3. Porównaj nazwę funkcji w wywołaniu w `main`, w nagłówku i w definicji.
4. Czy oba pliki `.cpp` są w `add_executable`?

**Potem:**

5. Zbuduj projekt. Skonfiguruj go jak nowy projekt w lekcji 11.1, punkt 5.
6. Przeczytaj wynik budowania: które pliki się skompilowały i co zgłasza linker?
7. Popraw nazwę w definicji na `calculate_points`.
8. Zbuduj projekt ponownie.
9. Uruchom go i wpisz `4 2`.
10. Wyjaśnij, dlaczego sam nagłówek nie dostarczył definicji.

<details>
<summary>Co się dzieje i dlaczego: otwórz po zbudowaniu błędnego projektu</summary>

1. **Oba pliki się kompilują:** są dwie linijki `Building CXX object`. `main.cpp` zna `calculate_points` z nagłówka. `points.cpp` dołącza ten nagłówek i definiuje funkcję `calculate_point`, a dla kompilatora to po prostu inna funkcja.
2. **Linkowanie się nie udaje.** `main` wywołuje `calculate_points`, a w żadnym pliku obiektowym nie ma jej definicji. Komunikat jest taki sam jak w lekcji 11.1: na Ubuntu ``undefined reference to `calculate_points(int, int)'``, na macOS `"calculate_points(int, int)", referenced from`, na Windowsie `undefined symbol: int __cdecl calculate_points(int, int)`, a na końcu `linker command failed`.
3. **Nagłówek zawiera tylko deklarację.** Mówi, że funkcja istnieje i jak ją wywołać, ale jej nie definiuje. Definicję musi dostarczyć któryś plik `.cpp` z `add_executable`.

**Inny problem niż w lekcji 11.1, ten sam komunikat.** Tam definicja była poprawna, ale jej plik nie był budowany. Tu plik jest budowany, ale definiuje inną funkcję. Błąd linkowania nie zawsze oznacza więc pominięty plik `.cpp`: najpierw sprawdź `add_executable`, potem porównaj nazwy i typy w nagłówku i w definicji.

Po poprawieniu nazwy program wypisuje `Points: 14`, tak jak w punkcie 6.

</details>

**Na papierze, bez uruchamiania.** Co się stanie, jeśli `main.cpp` i `points.cpp` dołączają `points.hpp`, ale w `main.cpp` została jeszcze ręcznie zapisana, identyczna deklaracja `calculate_points`?

<details>
<summary>Odpowiedź</summary>

Program nadal się kompiluje i działa: zgodną deklarację zwykłej funkcji można powtórzyć. Ta kopia jest jednak zbędna. Gdy funkcja się zmieni, a ktoś poprawi tylko nagłówek, kopia w `main.cpp` przestanie pasować. Dlatego deklarację trzymamy w jednym miejscu, w nagłówku.

</details>

Poprawiony projekt jest w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 9. Gdy coś pójdzie inaczej

| Co widzisz | Co to znaczy | Co zrobić |
|---|---|---|
| `'points.hpp' file not found` | Nagłówka nie ma obok pliku, który go dołącza, albo ma inną nazwę, na przykład `points.h` lub `points.hpp.txt`. | Sprawdź nazwę poleceniem `ls` i porównaj ją z linijką `#include`. |
| `file not found with <angled> include; use "quotes" instead` | Własny nagłówek jest dołączony w nawiasach ostrych. | Własne nagłówki dołączaj w cudzysłowie: `#include "points.hpp"`. |
| ostrzeżenie `non-portable path to file` albo `file not found` przy nazwie z wielką literą | Wielkość liter w `#include` różni się od nazwy pliku, na przykład `Points.hpp`. Na Windowsie i macOS plik się znajdzie, z ostrzeżeniem, a na Linuksie nie. | Wpisz nazwę dokładnie tak jak na dysku. |
| `use of undeclared identifier` z nazwą funkcji w `main.cpp` | `main.cpp` nie dołącza nagłówka albo dołącza go poniżej wywołania. | Dopisz `#include "points.hpp"` na początku `main.cpp`. |
| `undefined reference`, `undefined symbol` albo `referenced from`, choć oba pliki `.cpp` są w `add_executable` | Definicja ma inną nazwę albo inne typy parametrów niż deklaracja w nagłówku (punkt 8). | Porównaj definicję z deklaracją w nagłówku. |
| Linker zgłasza, że funkcja jest zdefiniowana więcej niż raz, na przykład `duplicate symbol` albo `multiple definition` | Definicja trafiła do nagłówka, który dołączają dwa pliki `.cpp`. | W nagłówku zostaw deklarację ze średnikiem, a definicję w pliku `.cpp`. |
| W `add_executable` jest `points.hpp` albo w nagłówku są linijki `#ifndef`, `#define` i `#endif` | Tak plik przygotował CLion (punkt 2). | Usuń nazwę nagłówka z `add_executable`, a zawartość nagłówka zastąp tekstem z punktu 2. |

## 10. Wyjaśnij

Odpowiedz własnymi słowami, najlepiej na piśmie. Dopiero potem porównaj z przykładowymi odpowiedziami.

1. Co jest w `points.hpp`, a co w `points.cpp`?
2. Dlaczego `points.hpp` dołącza `main.cpp`? I dlaczego dołącza go też `points.cpp`?
3. Co robi `#include "points.hpp"`, a czego nie robi? Czym różni się od `#include <iostream>`?
4. Co robi `#pragma once`, a czego nie robi?
5. Czy nagłówek jest osobno kompilowany albo linkowany?
6. Dlaczego w projekcie z tego kursu `points.hpp` nie stoi w `add_executable`? Czy CMake by na to pozwolił?
7. Czy sam nagłówek dostarcza definicję funkcji?
8. Czy błąd linkowania zawsze oznacza plik `.cpp` pominięty w `add_executable`?
9. Program z lekcji 10.5 miał własny typ, z którego korzystały dwie funkcje i `main`. Gdyby podzielić go na pliki, co musiałby wiedzieć o tym typie każdy plik, który go używa?

<details>
<summary>Przykładowe odpowiedzi</summary>

1. W `points.hpp` jest `#pragma once` i deklaracja `calculate_points`. W `points.cpp` jest `#include "points.hpp"` i definicja funkcji, czyli jej ciało z obliczeniem.
2. `main.cpp` potrzebuje deklaracji, żeby skompilować wywołanie. `points.cpp` dołącza ten sam nagłówek, żeby deklaracja i definicja stały w jednej jednostce translacji, a deklaracja istniała tylko w jednym miejscu. Nie gwarantuje to jednak, że definicja pasuje: funkcja o innej nazwie albo z innymi typami parametrów byłaby po prostu inną funkcją.
3. Wstawia treść nagłówka w miejscu tej linijki, zanim plik zostanie skompilowany. Nie uruchamia kodu i nie kompiluje ani nie linkuje `points.cpp`. Cudzysłów oznacza własny nagłówek z katalogu projektu, a nawiasy ostre nagłówek biblioteki standardowej.
4. Sprawia, że w jednej jednostce translacji nagłówek jest przetwarzany najwyżej raz, nawet jeśli dołączono go kilka razy. Nie ogranicza dołączania do jednego pliku w całym programie, nie dostarcza definicji i nie zmienia linkowania.
5. Nie. Jego treść kompiluje się jako część każdego pliku `.cpp`, który go dołącza. Osobnego pliku obiektowego nie ma.
6. Bo `add_executable` wymienia w tym kursie pliki, które są kompilowane, a nagłówek się do nich nie zalicza. CMake pozwoliłby dopisać nagłówek, na przykład dla wygody środowiska programistycznego. Pomijanie go to zasada naszego prostego projektu, a nie reguła CMake.
7. Nie. Zawiera deklarację, a definicję musi dostarczyć plik `.cpp` z `add_executable`. W punkcie 8 nagłówek był dołączony, a mimo to definicji brakowało.
8. Nie. W lekcji 11.1 plik był pominięty, a w punkcie 8 plik był budowany, ale definiował funkcję o innej nazwie. Ten sam komunikat może mieć różne przyczyny.
9. Każdy taki plik potrzebuje definicji typu, czyli tego, z jakich pól się składa, a nie tylko deklaracji. Taka definicja też może trafić do wspólnego nagłówka. Wtedy `#pragma once` ma większe znaczenie.

</details>

## Podsumowanie

- Plik nagłówkowy `.hpp` zawiera deklaracje, które inne pliki dołączają przez `#include "..."`. Deklaracja funkcji istnieje wtedy w jednym miejscu.
- `#include` wstawia treść nagłówka do pliku przed kompilacją. Nie kompiluje ani nie linkuje innych plików.
- Nagłówek dołączają plik, który wywołuje funkcję, i plik z jej definicją. Nazwę, typ wyniku i typy parametrów nadal trzeba porównywać.
- Definicja zostaje w pliku `.cpp`. Nagłówek nie dostarcza definicji.
- `#pragma once` zapobiega ponownemu przetworzeniu nagłówka w jednej jednostce translacji. Nie należy do standardu, ale obsługują go popularne kompilatory.
- Nagłówek nie jest osobno kompilowany ani linkowany. W projekcie z tego kursu `add_executable` wymienia tylko pliki `.cpp`.
- Ten sam komunikat linkera może oznaczać pominięty plik `.cpp` albo definicję, która nie pasuje do deklaracji.

## Co dalej

Nagłówek z tej lekcji zawiera tylko deklarację funkcji. Programy z Modułów 8–10 miały też własne typy, z których korzystało kilka funkcji. W następnej lekcji Modułu 11 definicja takiego typu trafi do wspólnego nagłówka. Ta lekcja jest w przygotowaniu.

---

## Przykładowe rozwiązania

Zajrzyj tutaj **po własnej próbie**. Twoje nazwy mogą się różnić, jeśli standardowe wyjście jest takie, jak wymagane.

<details>
<summary>Punkt 7: misja, bilety z nagłówkiem</summary>

**`tickets.hpp`**:

<!-- file: tickets tickets.hpp -->
```cpp
#pragma once

int total_cost(int regular_tickets, int reduced_tickets);
```

**`tickets.cpp`**:

<!-- file: tickets tickets.cpp -->
```cpp
#include "tickets.hpp"

int total_cost(int regular_tickets, int reduced_tickets) {
    const int regular_price{12};
    const int reduced_price{7};
    return regular_tickets * regular_price + reduced_tickets * reduced_price;
}
```

**`main.cpp`**:

<!-- example: tickets -->
```cpp
#include <iostream>

#include "tickets.hpp"

int main() {
    int regular_tickets{0};
    int reduced_tickets{0};

    std::cin >> regular_tickets;
    std::cin >> reduced_tickets;

    std::cout << "Total cost: " << total_cost(regular_tickets, reduced_tickets) << "\n";
}
```

**`CMakeLists.txt`**, taki sam jak w lekcji 11.1:

<!-- cmake: tickets -->
```cmake
cmake_minimum_required(VERSION 3.28)
project(first_program LANGUAGES CXX)

add_executable(first_program main.cpp tickets.cpp)
target_compile_features(first_program PRIVATE cxx_std_20)
set_target_properties(first_program PROPERTIES CXX_EXTENSIONS OFF)
```

Wyniki dla danych A–D: 45, 28, 0 i 36, takie same jak w lekcji 11.1.

1. **Deklaracja jest w nagłówku,** bo potrzebują jej dwa pliki, a ma istnieć w jednym miejscu.
2. **Definicja zostaje w `tickets.cpp`,** bo nagłówek dołączają dwa pliki `.cpp`. Definicja w nagłówku trafiłaby do programu dwa razy.
3. **Oba pliki `.cpp` dołączają nagłówek:** `main.cpp`, żeby skompilować wywołanie, a `tickets.cpp`, żeby deklaracja i definicja stały obok siebie.
4. **W `main.cpp` nie ma drugiej, ręcznej deklaracji.** Zbudowałaby się, ale przy zmianie funkcji mogłaby przestać pasować do nagłówka.
5. **`#pragma once`** sprawia, że w jednej jednostce translacji nagłówek jest przetwarzany najwyżej raz.
6. **Nie blokuje dołączania w różnych plikach `.cpp`:** `main.cpp` i `tickets.cpp` kompilują się osobno i każdy dostaje deklarację.
7. **`add_executable` wymienia dwa pliki `.cpp`,** bo tylko one są kompilowane. Nagłówek kompiluje się jako ich część.
8. **Pliku `.cpp` nie dołącza się do innego `.cpp`:** definicja trafiłaby do programu dwa razy, a pliki `.cpp` łączy linker.
9. **Linkowanie nadal jest konieczne:** wywołanie z `main.cpp.o` musi zostać połączone z definicją z `tickets.cpp.o`.
10. **Wyniki się nie zmieniły,** bo obliczenie i `main` są takie same. Zmieniło się tylko miejsce deklaracji.

Inne poprawne rozwiązania: nazwy z Twojego projektu z lekcji 11.1, na przykład `prices.hpp` obok `prices.cpp`, albo deklaracja bez nazw parametrów, `int total_cost(int, int);`.

</details>

<details>
<summary>Punkt 8: poprawiony projekt</summary>

W porównaniu z błędnym projektem zmienia się jedna linijka `points.cpp`: definicja nazywa się znowu `calculate_points`.

**`points.cpp`**:

<!-- file: points_name_fixed points.cpp -->
```cpp
#include "points.hpp"

int calculate_points(int solved, int bonus) {
    const int points_per_task{3};
    return solved * points_per_task + bonus;
}
```

**`main.cpp`**, bez zmian:

<!-- example: points_name_fixed -->
```cpp
#include <iostream>

#include "points.hpp"

int main() {
    int solved{0};
    int bonus{0};

    std::cin >> solved;
    std::cin >> bonus;

    std::cout << "Points: " << calculate_points(solved, bonus) << "\n";
}
```

**`points.hpp`**, bez zmian:

<!-- file: points_name_fixed points.hpp -->
```cpp
#pragma once

int calculate_points(int solved, int bonus);
```

**`CMakeLists.txt`**, bez zmian:

<!-- cmake: points_name_fixed -->
```cmake
cmake_minimum_required(VERSION 3.28)
project(first_program LANGUAGES CXX)

add_executable(first_program main.cpp points.cpp)
target_compile_features(first_program PRIVATE cxx_std_20)
set_target_properties(first_program PROPERTIES CXX_EXTENSIONS OFF)
```

Dla tych samych danych co w punkcie 6:

<!-- input: points_name_fixed -->
```text
4 2
```

<!-- output: points_name_fixed -->
```text
Points: 14
```

</details>

**Poprzednia lekcja:** [Lekcja 11.1: Drugi plik źródłowy](lesson_01_second_source_file.md) · **Następna lekcja:** w przygotowaniu · [Opis kursu](../../README.md)

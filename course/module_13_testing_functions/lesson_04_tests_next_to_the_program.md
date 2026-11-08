# Lekcja 13.4: Testy obok programu

**Polski** · [English](lesson_04_tests_next_to_the_program.en.md) · [Opis kursu](../../README.md)

> **Moduł 13, lekcja 4** · około 90–110 minut, można ją podzielić na dwa podejścia
> **Potrzebujesz:** katalogu `cpp-workspace` i oryginalnego projektu `lesson_05_first_program`, jak dotąd. Przyda się też Twoje rozwiązanie misji z lekcji 13.2 z funkcją `is_valid_slot`.
> **Wersja pilotażowa.** Projekty z tej lekcji sprawdzamy automatycznie na Windowsie, Ubuntu i macOS: budujemy w każdym oba programy i uruchamiamy program testowy, razem z jego kodem zakończenia. Kroki w CLionie (nowe pliki, ponowne wczytanie projektu CMake, wybór programu w pasku narzędzi, **Build Project**) opisujemy według dokumentacji CLion 2026.3, bez ręcznego sprawdzenia na każdym systemie.

## Zanim zaczniesz

Ta lekcja zakłada, że:

- piszesz program testowy z lekcji 13.1–13.3: wynik oczekiwany z kontraktu, funkcja sprawdzająca, taka jak `check_int` albo `check_bool`, liczniki sprawdzeń i niepowodzeń, podsumowanie `Checks: N, failed: F` i kod zakończenia 0 albo 1;
- budujesz program z kilku plików: deklaracje w nagłówku `.hpp` z `#pragma once`, definicje w pliku `.cpp`, który dołącza ten nagłówek, i każdy plik `.cpp` wymieniony w `add_executable` (lekcje 11.1–11.4);
- odróżniasz błąd kompilacji od błędu linkowania i wiesz, że dwie definicje tej samej funkcji w dwóch plikach `.cpp` zgłasza linker (lekcja 11.4);
- po zmianie `CMakeLists.txt` wczytujesz projekt CMake ponownie w CLionie (lekcja 11.1);
- wiesz, że CLion uruchamia program według konfiguracji uruchomienia, takiej jak `first_program` (lekcja 12.1).

## Sytuacja

Automat parkingowy przy bibliotece wylicza opłatę funkcją `parking_fee` z lekcji 13.1. Jej testy powstały wtedy w osobnym programie, w którym funkcja była napisana jeszcze raz, obok testów. Na początek to wystarczało. Teraz program automatu i testy mają działać obok siebie przez dłuższy czas, a cennik kiedyś się zmieni. W tej lekcji odpowiesz na pytanie: **jak zorganizować projekt, żeby testy sprawdzały dokładnie tę funkcję, której używa program?**

Po tej lekcji będziesz:

- rozdzielać program właściwy i program testowy na dwa pliki, każdy z własną funkcją `main`;
- umieszczać deklarację sprawdzanej funkcji we wspólnym nagłówku, a jej jedyną definicję w jednym pliku `.cpp`;
- opisywać w `CMakeLists.txt` dwa programy, które korzystają z tego samego pliku `.cpp`;
- budować oba programy i uruchamiać każdy z nich osobno w CLionie;
- rozpoznawać regresję: zmiana we wspólnym pliku psuje coś, co wcześniej działało, a testy to wykrywają;
- odróżniać błąd linkowania z dwiema funkcjami `main` w jednym programie od `FAIL` w testach.

## 1. Dwie kopie jednej funkcji

Zacznij od organizacji, którą znasz. Są dwa osobne projekty, każdy z jednym plikiem `main.cpp`:

```text
projekt automatu                    projekt testów, jak w lekcji 13.1
  main.cpp                            main.cpp
    parking_fee   <- kopia 1            parking_fee   <- kopia 2
    main: wypisuje opłatę               check_int i main: PASS albo FAIL
```

Testy sprawdzają kopię 2, a automat liczy kopią 1. Dopóki obie kopie są identyczne, wynik testów mówi coś także o automacie. Ale nikt tego nie pilnuje:

| Co się stało | Program automatu | Program testowy |
|---|---|---|
| Ktoś zmienił `parking_fee` w automacie i popełnił błąd | liczy źle | nadal `PASS`: sprawdza starą kopię |
| Ktoś poprawił błąd tylko w programie testowym | nadal liczy źle | `PASS` |
| Ktoś zmienił cennik w automacie, ale nie w testach | liczy według nowego cennika | sprawdza stary cennik |

W każdym z tych przypadków testy przechodzą albo nie przechodzą z powodu **kopii**, a nie funkcji, której używa automat. **Testy kopii sprawdzają kopię.**

Rozwiązanie: jedna definicja funkcji, z której korzystają oba programy. Program i jego testy stają się wtedy jednym projektem.

**Nie każdy mały program potrzebuje od razu osobnego programu testowego.** Ćwiczenie z jedną funkcją i jednym uruchomieniem obejdzie się bez niego. Taka organizacja opłaca się, gdy:

- program rośnie, a funkcji przybywa;
- funkcja jest używana w kilku miejscach programu;
- testy mają zostać na dłużej, a nie tylko na jedno sprawdzenie;
- implementacja funkcji będzie się zmieniać;
- po każdej zmianie chcesz uruchamiać te same sprawdzenia.

## 2. Plan: jedna funkcja, dwa programy

**Najważniejsza idea tej lekcji: program i testy mają osobne funkcje `main`, ale korzystają z tych samych funkcji.**

Projekt ma pięć plików:

| Plik | Rola | Zawiera | Nie zawiera |
|---|---|---|---|
| `rules.hpp` | wspólny nagłówek | deklarację `parking_fee` | definicji |
| `rules.cpp` | **wspólna implementacja** (ang. *shared implementation*) | jedyną definicję `parking_fee` | funkcji `main` |
| `main.cpp` | **program właściwy** (ang. *application program*) | `main` automatu: wywołanie funkcji i wypisanie opłaty | definicji `parking_fee`, testów |
| `function_tests.cpp` | **program testowy** (ang. *test program*) | `check_int` i `main` z testami | definicji `parking_fee` |
| `CMakeLists.txt` | plan budowania | dwa programy i ich pliki | |

```text
                      rules.hpp (deklaracja)
                     /                      \
             main.cpp                        function_tests.cpp
          + rules.cpp                      + rules.cpp
                |                                  |
         program właściwy                   program testowy
```

- Każdy program ma **dokładnie jedną** funkcję `main`, od której zaczyna się jego wykonywanie. Dlatego `main.cpp` i `function_tests.cpp` należą do dwóch różnych programów.
- Oba programy powstają z **tego samego** pliku `rules.cpp`. Nie ma drugiej kopii funkcji, więc nie ma czego pilnować.
- Program właściwy nie wie nic o testach. Program testowy nie wie nic o tym, co wypisuje automat. Łączy je tylko `rules.hpp` i `rules.cpp`.

## 3. Przygotuj pliki projektu

W `cpp-workspace` utwórz katalog `lesson_13_4` i skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program`. Otwórz go w CLionie jak w lekcji 11.1: **File | Open**, potem **Trust Project** i profil **Debug**.

Utwórz obok `main.cpp` trzy nowe pliki, tak jak w Module 11:

- `rules.hpp`: **New | C/C++ Header File**, typ `.hpp`, a zawartość szablonu CLiona zastąp tekstem poniżej (lekcja 11.2);
- `rules.cpp` i `function_tests.cpp`: **New | C/C++ Source File**, typ `.cpp`, bez opcji **Create an associated header** (lekcja 11.1).

Jeśli CLion zaproponuje dodanie pliku do targetu (**Add to targets**), nie musisz z tego korzystać: obie listy plików wpiszesz w punkcie 4 i porównasz z pokazanymi.

**`rules.hpp`**, deklaracja:

<!-- file: parking_project rules.hpp -->
```cpp
#pragma once

int parking_fee(int hours);
```

**`rules.cpp`**, jedyna definicja. To funkcja z lekcji 13.1, bez zmian. Plik dołącza swój nagłówek, jak w lekcji 11.2:

<!-- file: parking_project rules.cpp -->
```cpp
#include "rules.hpp"

int parking_fee(int hours) {
    if (hours < 0 || hours > 8) {
        return -1;
    }

    if (hours == 0) {
        return 0;
    }

    return 5 + 3 * (hours - 1);
}
```

**`main.cpp`**, program właściwy. Zastąp nim zawartość skopiowanego pliku:

<!-- example: parking_project target=function_tests -->
```cpp
#include <iostream>

#include "rules.hpp"

int main() {
    const int hours{2};

    std::cout << "Parking hours: " << hours << "\n";
    std::cout << "Fee: " << parking_fee(hours) << "\n";
}
```

Program nie odczytuje danych: liczba godzin jest stałą, żeby wynik zależał tylko od funkcji. Prawdziwy automat odczytywałby ją, jak programy z Modułu 10.

**`function_tests.cpp`**, program testowy:

<!-- file: parking_project function_tests.cpp -->
```cpp
#include <iostream>
#include <string>

#include "rules.hpp"

void check_int(const std::string& name, int expected, int actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << expected << ", actual " << actual << "\n";
        ++failed;
    }
}

int main() {
    int checks{0};
    int failed{0};

    check_int("parking_fee(0)", 0, parking_fee(0), checks, failed);
    check_int("parking_fee(1)", 5, parking_fee(1), checks, failed);
    check_int("parking_fee(2)", 8, parking_fee(2), checks, failed);
    check_int("parking_fee(3)", 11, parking_fee(3), checks, failed);
    check_int("parking_fee(8)", 26, parking_fee(8), checks, failed);
    check_int("parking_fee(9)", -1, parking_fee(9), checks, failed);

    std::cout << "Checks: " << checks << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

- `check_int` i licznik sprawdzeń `checks` są takie jak w lekcji 13.3. Każdy przypadek to tu jedno sprawdzenie.
- **W tym pliku nie ma definicji `parking_fee`.** Każde wywołanie `parking_fee(...)` trafia do funkcji z `rules.cpp`, tej samej, której używa `main.cpp`.
- Wyniki oczekiwane to liczby z kontraktu z lekcji 13.1, a nie wywołania funkcji ani kopia jej wzoru (lekcja 13.1, punkt 9):

| Przypadek | `hours` | Wynik oczekiwany | Skąd |
|---|---:|---:|---|
| A | 0 | 0 | brak postoju |
| B | 1 | 5 | pierwsza godzina |
| C | 2 | 8 | 5 + 3 |
| D | 3 | 11 | 5 + 3 + 3 |
| E | 8 | 26 | 5 + 7 · 3 |
| F | 9 | -1 | poza zakresem 0–8 |

Programu jeszcze nie budujesz: najpierw trzeba opisać oba programy w `CMakeLists.txt`.

## 4. Dwa targety w `CMakeLists.txt`

Od lekcji 0.5 `CMakeLists.txt` opisuje jeden program: linijka `add_executable(first_program main.cpp)`. W Module 11 na tej liście, po `main.cpp`, przybywało kolejnych plików `.cpp`. Tutaj zmienisz plik w dwóch krokach:

1. **Program właściwy**, jak w Module 11: `first_program` budujesz z `main.cpp` i `rules.cpp`.
2. **Program testowy, nowość:** pod spodem pusta linijka i trzy linijki dla drugiego programu, `function_tests`.

Cały plik:

<!-- cmake: parking_project -->
```cmake
cmake_minimum_required(VERSION 3.28)
project(first_program LANGUAGES CXX)

add_executable(first_program main.cpp rules.cpp)
target_compile_features(first_program PRIVATE cxx_std_20)
set_target_properties(first_program PROPERTIES CXX_EXTENSIONS OFF)

add_executable(function_tests function_tests.cpp rules.cpp)
target_compile_features(function_tests PRIVATE cxx_std_20)
set_target_properties(function_tests PROPERTIES CXX_EXTENSIONS OFF)
```

- **Target** (po polsku: cel budowania) to coś, co CMake buduje, tu: program. Jego nazwą jest pierwsze słowo w `add_executable`. Od lekcji 0.5 znasz jeden target, `first_program`. Teraz projekt ma dwa: `first_program` i `function_tests`.
- **Nazwa targetu nie musi być nazwą pliku.** `first_program` powstaje z `main.cpp` i `rules.cpp`. Plik z `main` programu testowego nazywa się tu tak samo jak jego target, żeby łatwo je skojarzyć, ale CMake tego nie wymaga.
- **Każdy target ma własną listę plików**, a na niej dokładnie jeden plik z funkcją `main`: `first_program` ma `main.cpp`, a `function_tests` ma `function_tests.cpp`.
- **`rules.cpp` stoi na obu listach.** To jeden plik w katalogu projektu, bez kopiowania. CMake kompiluje go osobno dla każdego programu, więc powstaną dwa pliki obiektowe z tego samego źródła. Zmiana w `rules.cpp` trafi do obu programów, gdy tylko je przebudujesz.
- **`rules.hpp` nie stoi na żadnej liście**, jak każdy nagłówek (lekcja 11.2). Dołączają go `main.cpp`, `function_tests.cpp` i `rules.cpp`.
- **Dwie linijki właściwości powtarzasz dla `function_tests`.** Ustawienia należą do targetu, więc bez nich program testowy mógłby się kompilować według innego standardu C++ niż program właściwy.
- Pozostałe linijki pliku z lekcji 0.5 zostają bez zmian. W tym kursie każdy plik źródłowy stoi w jednej linijce `add_executable`, a obie listy oddziela pusta linijka.

`function_tests.cpp` **nie trafia** na listę `first_program`, a `main.cpp` na listę `function_tests`. Co się dzieje, gdy ktoś to pomyli, zobaczysz w punkcie 8.

## 5. Zbuduj i uruchom oba programy

**To pierwsze obowiązkowe uruchomienie.**

**W CLionie** (według dokumentacji CLion 2026.3, bez ręcznego sprawdzenia na każdym systemie):

1. Po zmianie `CMakeLists.txt` wczytaj projekt ponownie: kliknij informację o zmianie albo wybierz **Tools | CMake | Reload CMake Project**.
2. W pasku narzędzi, w wyborze programu do uruchomienia, CLion pokazuje konfiguracje uruchomienia. Po ponownym wczytaniu powinny tam być dwie: `first_program` i `function_tests`. Jeśli brakuje `function_tests`, sprawdź linijkę `add_executable(function_tests ...)` i wczytaj projekt jeszcze raz.
3. Wybierz **Build | Build Project**. To polecenie buduje wszystkie programy projektu, tu oba. W oknie **Build** znajdziesz mniej więcej takie linijki:

   ```text
   Building CXX object CMakeFiles/first_program.dir/main.cpp.o
   Building CXX object CMakeFiles/first_program.dir/rules.cpp.o
   Building CXX object CMakeFiles/function_tests.dir/function_tests.cpp.o
   Building CXX object CMakeFiles/function_tests.dir/rules.cpp.o
   Linking CXX executable first_program
   Linking CXX executable function_tests
   ```

   Są cztery kompilacje, w tym **dwie** kompilacje `rules.cpp`, po jednej dla każdego programu, i dwa linkowania. Kolejność linijek może być inna. Na Windowsie pliki obiektowe kończą się na `.obj`, a programy na `.exe`.
4. Wybierz `first_program` i kliknij **Run** (▶). **Przewidź** wynik, zanim go zobaczysz.
5. Wybierz `function_tests` i kliknij **Run**. **Przewidź** wynik każdej linijki i kod zakończenia.

<details>
<summary>Standardowe wyjście obu programów</summary>

`first_program`, program właściwy:

```text
Parking hours: 2
Fee: 8
```

`function_tests`, program testowy:

<!-- output: parking_project -->
```text
PASS parking_fee(0)
PASS parking_fee(1)
PASS parking_fee(2)
PASS parking_fee(3)
PASS parking_fee(8)
PASS parking_fee(9)
Checks: 6, failed: 0
```

Oba programy kończą się kodem 0: `Process finished with exit code 0`.

</details>

**Skąd wiesz, który program się uruchomił?** Z wyboru w pasku narzędzi, z nazwy konfiguracji, którą CLion pokazuje w oknie **Run**, i z treści: program właściwy wypisuje opłatę, a program testowy linijki `PASS` albo `FAIL` i podsumowanie.

**Build i Run to dwie różne czynności:**

- **Build | Build Project** buduje wszystkie programy projektu i niczego nie uruchamia.
- **Run** uruchamia **jeden** program, ten wybrany w pasku narzędzi. Przed uruchomieniem CLion buduje ten program, jeśli coś się w nim zmieniło. Nie musi przy tym budować drugiego programu.
- Inne polecenia budowania, na przykład z nazwą wybranej konfiguracji w menu **Build**, budują tylko wybrany program.

Dlatego po każdej zmianie zaczynaj od **Build Project**. Gdyby po zmianie kliknąć tylko **Run** przy wybranym `function_tests`, błąd w `main.cpp` mógłby pozostać niezauważony, aż do wybrania `first_program`.

**W terminalu** (nieobowiązkowo): skonfiguruj projekt w katalogu `build-terminal` jak w lekcji 11.1, punkt 5. Polecenie `cmake --build build-terminal` buduje oba programy, bo nie wskazuje żadnego targetu. Potem uruchom każdy z nich: `./build-terminal/first_program` i `./build-terminal/function_tests` (Windows: `.\build-terminal\first_program.exe` i `.\build-terminal\function_tests.exe`). Kod zakończenia odczytuj w CLionie, jak w lekcji 13.1: terminal go nie wypisuje.

**Co sprawdzamy automatycznie.** Automatyczne sprawdzanie kursu buduje z tych pięciu plików oba programy, uruchamia program testowy i porównuje jego wyjście i kod zakończenia z lekcją. Wyjście programu właściwego pokazujemy jako przykład uruchomienia w CLionie: nie jest sprawdzane automatycznie.

## 6. Zmiana we wspólnym pliku

**To drugie obowiązkowe uruchomienie.**

Ktoś poprawiał cennik i pomylił się: każda kolejna godzina kosztuje teraz 2 zamiast 3. Zmień w `rules.cpp` tylko ostatnią linijkę funkcji:

<!-- fragment -->
```cpp
    return 5 + 2 * (hours - 1);
```

Nie zmieniaj niczego innego: ani `rules.hpp`, ani `main.cpp`, ani `function_tests.cpp`, ani `CMakeLists.txt`, ani wyników oczekiwanych.

1. **Przewidź:** które sprawdzenia dadzą `FAIL`, z jakim wynikiem rzeczywistym, jaki będzie kod zakończenia programu testowego i co wypisze program właściwy?
2. Wybierz **Build | Build Project**.
3. Uruchom `function_tests`, a potem `first_program`.

<details>
<summary>Standardowe wyjście obu programów i kod zakończenia</summary>

`function_tests`:

<!-- output: parking_project_bug -->
```text
PASS parking_fee(0)
PASS parking_fee(1)
FAIL parking_fee(2): expected 8, actual 7
FAIL parking_fee(3): expected 11, actual 9
FAIL parking_fee(8): expected 26, actual 19
PASS parking_fee(9)
Checks: 6, failed: 3
```

CLion pokazuje `Process finished with exit code 1`.

`first_program`:

```text
Parking hours: 2
Fee: 7
```

</details>

<details>
<summary>Wszystkie pliki projektu z usterką</summary>

Te same pliki co w punktach 3 i 4, poza ostatnią linijką `parking_fee`. Nie musisz ich przepisywać: zmieniasz jedną linijkę w swoim `rules.cpp`.

**`main.cpp`**:

<!-- example: parking_project_bug target=function_tests exit=1 -->
```cpp
#include <iostream>

#include "rules.hpp"

int main() {
    const int hours{2};

    std::cout << "Parking hours: " << hours << "\n";
    std::cout << "Fee: " << parking_fee(hours) << "\n";
}
```

**`rules.hpp`**:

<!-- file: parking_project_bug rules.hpp -->
```cpp
#pragma once

int parking_fee(int hours);
```

**`rules.cpp`**, z usterką:

<!-- file: parking_project_bug rules.cpp -->
```cpp
#include "rules.hpp"

int parking_fee(int hours) {
    if (hours < 0 || hours > 8) {
        return -1;
    }

    if (hours == 0) {
        return 0;
    }

    return 5 + 2 * (hours - 1);
}
```

**`function_tests.cpp`**:

<!-- file: parking_project_bug function_tests.cpp -->
```cpp
#include <iostream>
#include <string>

#include "rules.hpp"

void check_int(const std::string& name, int expected, int actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << expected << ", actual " << actual << "\n";
        ++failed;
    }
}

int main() {
    int checks{0};
    int failed{0};

    check_int("parking_fee(0)", 0, parking_fee(0), checks, failed);
    check_int("parking_fee(1)", 5, parking_fee(1), checks, failed);
    check_int("parking_fee(2)", 8, parking_fee(2), checks, failed);
    check_int("parking_fee(3)", 11, parking_fee(3), checks, failed);
    check_int("parking_fee(8)", 26, parking_fee(8), checks, failed);
    check_int("parking_fee(9)", -1, parking_fee(9), checks, failed);

    std::cout << "Checks: " << checks << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

**`CMakeLists.txt`**:

<!-- cmake: parking_project_bug -->
```cmake
cmake_minimum_required(VERSION 3.28)
project(first_program LANGUAGES CXX)

add_executable(first_program main.cpp rules.cpp)
target_compile_features(first_program PRIVATE cxx_std_20)
set_target_properties(first_program PROPERTIES CXX_EXTENSIONS OFF)

add_executable(function_tests function_tests.cpp rules.cpp)
target_compile_features(function_tests PRIVATE cxx_std_20)
set_target_properties(function_tests PROPERTIES CXX_EXTENSIONS OFF)
```

</details>

**Co tu się stało:**

- Oba programy się zbudowały: to nie jest błąd kompilacji ani linkowania.
- Nie udały się trzy sprawdzenia: dla 2, 3 i 8 godzin. Zmieniony wzór liczy tylko kolejne godziny, a dla 1 godziny daje nadal 5 + 2 · 0 = 5. Dla 0 i 9 godzin funkcja kończy się wcześniej, na pierwszych warunkach.
- Każda linijka `FAIL` podaje wynik oczekiwany z kontraktu i rzeczywisty wynik zmienionej funkcji. `failed` wynosi 3, więc program testowy zwraca 1. Kod 1 oznacza tu, że **testy wykryły błąd w funkcji**, a nie że zawiódł program testowy.
- **Program właściwy też się zmienił:** wypisuje `Fee: 7` zamiast `Fee: 8`. Oba programy używają tego samego `rules.cpp`, więc jedna zmiana trafiła do obu. Przy dwóch kopiach z punktu 1 testy by jej nie zauważyły.

Taka sytuacja ma swoją nazwę: **regresja** (ang. *regression*), czyli zmiana kodu, która niechcący psuje zachowanie działające wcześniej. Zachowane testy wykryły ją od razu po przebudowaniu, zanim ktokolwiek zapłacił za postój według złego cennika.

**Napraw funkcję.** Przywróć w `rules.cpp` linijkę `return 5 + 3 * (hours - 1);`, wybierz **Build Project** i uruchom `function_tests` jeszcze raz: znowu sześć razy `PASS`, `Checks: 6, failed: 0` i kod 0. Pliki są znowu takie jak w punkcie 3, więc oba programy wypisują to samo co w punkcie 5, a `first_program` znowu `Fee: 8`.

**Nie poprawiamy testu, żeby pasował do błędnej funkcji. Poprawiamy funkcję, żeby spełniała kontrakt.** Wyniki oczekiwane pochodzą z kontraktu, a kontrakt się nie zmienił, więc nie zmieniają się też testy. Gdyby zmienił się sam cennik, nowe wyniki oczekiwane trzeba by policzyć z nowego kontraktu, a nie odczytać z tego, co zwraca funkcja.

Sześć razy `PASS` znaczy, że funkcja zgadza się z kontraktem w sześciu sprawdzonych przypadkach. Nie dowodzi, że jest poprawna dla wszystkich danych (lekcja 13.2).

## 7. Czy testy na pewno sprawdzają `rules.cpp`?

Dwa targety, `rules.cpp` na obu listach, wspólny nagłówek i dwa zbudowane programy to **warunki konieczne**. Same nie gwarantują, że każde sprawdzenie w `function_tests.cpp` wywołuje funkcję z `rules.cpp`. Każdy z tych projektów zbuduje się poprawnie, a testy nie sprawdzą właściwej funkcji:

- `function_tests.cpp` zawiera ręcznie skopiowany wzór, na przykład w funkcji sprawdzającej;
- testy wywołują drugą funkcję pod inną nazwą, na przykład `parking_fee_copy`, zdefiniowaną w pliku testów;
- wyniki oczekiwane są wyznaczane przez wywołanie tej samej funkcji, więc testy powtarzają jej błąd (lekcja 13.1, punkt 9);
- funkcja sprawdzająca wypisuje `PASS` bez porównania wyników.

Kopia pod **tą samą** nazwą co funkcja z `rules.cpp` się nie zbuduje: linker zgłosi dwie definicje, jak w lekcji 11.4. Kopia pod inną nazwą przejdzie bez żadnego komunikatu.

**Praktyczna kontrola:** celowa usterka w `rules.cpp` z punktu 6 dała `FAIL`. To dowód, że **te konkretne testy** wywołują funkcję z `rules.cpp`. Nie jest to dowód dla każdego testu, który napiszesz później: po dopisaniu nowego sprawdzenia warto znowu celowo zepsuć funkcję i zobaczyć, że to sprawdzenie zgłasza `FAIL` (lekcja 13.2).

## 8. Znajdź błąd: dwa programy zbudowane jako jeden

**To trzecie obowiązkowe uruchomienie: jedna czynność diagnostyczna.**

Ktoś chciał mieć testy w tym samym projekcie, ale zamiast drugiego targetu dopisał `function_tests.cpp` do listy `first_program`. Odtwórz ten projekt: w `cpp-workspace` utwórz katalog `parking_one_target`, skopiuj do niego cztery pliki `.cpp` i `.hpp` z `lesson_13_4`, z poprawnym `rules.cpp`, i zapisz w nim taki `CMakeLists.txt`:

<!-- cmake: parking_one_target -->
```cmake
cmake_minimum_required(VERSION 3.28)
project(first_program LANGUAGES CXX)

add_executable(first_program main.cpp rules.cpp function_tests.cpp)
target_compile_features(first_program PRIVATE cxx_std_20)
set_target_properties(first_program PROPERTIES CXX_EXTENSIONS OFF)
```

<details>
<summary>Pozostałe pliki, bez zmian względem punktu 3</summary>

**`main.cpp`**:

<!-- broken: parking_one_target stage=link error=multiple definition of .main'|duplicate symbol: main\b|duplicate symbol '_main' in: -->
```cpp
#include <iostream>

#include "rules.hpp"

int main() {
    const int hours{2};

    std::cout << "Parking hours: " << hours << "\n";
    std::cout << "Fee: " << parking_fee(hours) << "\n";
}
```

**`rules.hpp`**:

<!-- file: parking_one_target rules.hpp -->
```cpp
#pragma once

int parking_fee(int hours);
```

**`rules.cpp`**:

<!-- file: parking_one_target rules.cpp -->
```cpp
#include "rules.hpp"

int parking_fee(int hours) {
    if (hours < 0 || hours > 8) {
        return -1;
    }

    if (hours == 0) {
        return 0;
    }

    return 5 + 3 * (hours - 1);
}
```

**`function_tests.cpp`**:

<!-- file: parking_one_target function_tests.cpp -->
```cpp
#include <iostream>
#include <string>

#include "rules.hpp"

void check_int(const std::string& name, int expected, int actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << expected << ", actual " << actual << "\n";
        ++failed;
    }
}

int main() {
    int checks{0};
    int failed{0};

    check_int("parking_fee(0)", 0, parking_fee(0), checks, failed);
    check_int("parking_fee(1)", 5, parking_fee(1), checks, failed);
    check_int("parking_fee(2)", 8, parking_fee(2), checks, failed);
    check_int("parking_fee(3)", 11, parking_fee(3), checks, failed);
    check_int("parking_fee(8)", 26, parking_fee(8), checks, failed);
    check_int("parking_fee(9)", -1, parking_fee(9), checks, failed);

    std::cout << "Checks: " << checks << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

</details>

**Zanim zbudujesz**, odpowiedz na piśmie:

1. **Przewidź:** na którym etapie budowanie się nie uda: przy konfiguracji CMake, kompilacji czy linkowaniu?
2. Czy każdy z trzech plików `.cpp` z osobna jest poprawnym kodem C++?
3. Ile funkcji `main` dostanie linker dla programu `first_program`?
4. Czy to będzie `FAIL` w testach?

**Potem:**

5. Otwórz projekt w CLionie i wybierz **Build | Build Project**. W terminalu skonfiguruj go jak nowy projekt w lekcji 11.1, punkt 5.
6. Przeczytaj wynik budowania: ile plików się skompilowało i jaką funkcję wymienia linker?
7. Popraw `CMakeLists.txt`: każdy plik z `main` w osobnym targecie, czyli plik z punktu 4. Wczytaj projekt ponownie.
8. Wybierz **Build Project** i potwierdź, że powstały oba programy. Uruchom `function_tests`: sześć razy `PASS` i kod 0.

<details>
<summary>Co się dzieje i dlaczego: otwórz po zbudowaniu błędnego projektu</summary>

1. **Konfiguracja i kompilacja się udają.** CMake nie wie, w którym pliku jest `main`: lista jest dla niego poprawna, bo wszystkie pliki istnieją i każdy stoi na niej raz. Każdy z trzech plików `.cpp` jest poprawnym kodem, więc kompilator kompiluje wszystkie trzy: są trzy linijki `Building CXX object`.
2. **Linkowanie się nie udaje.** Linker łączy trzy pliki obiektowe w jeden program i dostaje dwie definicje `main`: z `main.cpp` i z `function_tests.cpp`. Komunikat wymienia `main`: na Ubuntu `multiple definition of`, na macOS `duplicate symbol '_main'`, na Windowsie `duplicate symbol: main`, a na końcu `linker command failed`. Dokładna treść zależy od systemu, więc szukaj nazwy funkcji i słów o powtórzonej definicji.
3. **Dwie funkcje `main` mogą być w jednym projekcie, ale nie w jednym programie.** Program ma jeden punkt startu. Każdy `main` potrzebuje własnego targetu.
4. **To nie jest `FAIL`.** Program testowy w ogóle nie powstał, więc nic się nie uruchomiło. `FAIL` pojawia się wtedy, gdy program testowy się zbudował, uruchomił i znalazł niezgodność z kontraktem. Tutaj błąd jest w liście plików, a nie w testach ani w funkcji.
5. **Poprawka to osobny target**, a nie usunięcie jednej z funkcji `main`. Po powrocie do pliku z punktu 4 projekt buduje dwa programy, a `function_tests` daje ten sam wynik co w punkcie 5.
6. **Dwa różne sposoby wykrywania tego błędu.** Na Twoim komputerze ten błąd zgłasza linker, bo CMake i CLion nie zaglądają do treści plików. Automatyczne sprawdzanie kursu dla projektów z dwoma targetami dodatkowo odrzuca, jeszcze przed budowaniem, listę, na której stoi plik z `main` drugiego programu. To jego własna kontrola struktury, a nie zachowanie CMake.

</details>

## 9. Misja: rezerwacja sali w dwóch programach

Recepcja szkoły ma program, który sprawdza rezerwację sali funkcją `is_valid_slot` z misji lekcji 13.2. Testy tej funkcji masz już w swoim programie z lekcji 13.2, razem z jej kopią. Przenieś funkcję i testy do jednego projektu z dwoma programami.

**Kontrakt funkcji `bool is_valid_slot(int start_hour, int end_hour)`**, bez zmian względem lekcji 13.2:

- przedział jest poprawny **wtedy i tylko wtedy**, gdy jednocześnie: zaczyna się nie wcześniej niż o 8, kończy się nie później niż o 20, początek jest wcześniejszy niż koniec (`start_hour < end_hour`) i trwa najwyżej trzy godziny;
- długość przedziału to `end_hour - start_hour`;
- nie ma dat, minut ani kalendarza.

W `cpp-workspace` utwórz katalog `lesson_13_4_mission` z pięcioma plikami:

```text
lesson_13_4_mission/
├── CMakeLists.txt
├── main.cpp
├── function_tests.cpp
├── rules.cpp
└── rules.hpp
```

**Wymagania:**

- `rules.hpp` deklaruje `is_valid_slot`;
- `rules.cpp` zawiera **jedyną** definicję `is_valid_slot`;
- `main.cpp` dołącza `rules.hpp`, wywołuje `is_valid_slot` dla przedziału 8–11 i wypisuje `Slot 8-11: valid` albo `Slot 8-11: invalid`, zależnie od wyniku. Nie odczytuje danych i nie zawiera testów;
- `function_tests.cpp` dołącza `rules.hpp`, sprawdza wyniki `bool`, wypisuje `PASS` albo `FAIL` z wynikiem oczekiwanym i rzeczywistym, liczy sprawdzenia i niepowodzenia, wypisuje podsumowanie `Checks: N, failed: F` i kończy się kodem 0 albo 1;
- `CMakeLists.txt` opisuje dokładnie dwa programy, `first_program` i `function_tests`, oba z `rules.cpp`, i nie łączy dwóch funkcji `main` w jednym programie.

**Kolejność pracy:**

1. **Najpierw plan.** Dla każdego z pięciu plików zapisz jednym zdaniem, co w nim będzie, jak w tabeli z punktu 2.
2. **Tabela przypadków.** Przygotuj tabelę z wynikami oczekiwanymi z kontraktu. Możesz wziąć swoją tabelę z lekcji 13.2. Zadbaj o granice początku (8 i 7), końca (20 i 21) i długości (3 i 4 godziny) oraz o zerową długość.
3. Napisz `rules.hpp` i `rules.cpp`. Funkcję możesz przenieść ze swojego rozwiązania z lekcji 13.2: po przeniesieniu ma być tylko w `rules.cpp`.
4. Napisz `main.cpp` i `function_tests.cpp`. Funkcje `bool_text` i `check_bool` znasz z lekcji 13.2 i 13.3.
5. Napisz `CMakeLists.txt` z dwoma targetami.
6. **To czwarte obowiązkowe uruchomienie:** wybierz **Build Project**, uruchom `first_program`, a potem `function_tests`. Program właściwy powinien wypisać `Slot 8-11: valid`, wszystkie testy powinny przejść, a kod zakończenia testów powinien wynosić 0.
7. **Celowy błąd.** Zmień **tylko** `rules.cpp` tak, żeby funkcja odrzucała przedział trwający dokładnie trzy godziny, a poza tym działała tak samo. Przewidź, które sprawdzenia dadzą `FAIL` i co wypisze program właściwy.
8. **To piąte obowiązkowe uruchomienie:** wybierz **Build Project** i uruchom oba programy. Zapisz, które sprawdzenia się nie udały, jaki był kod zakończenia testów i co wypisał program właściwy. Potem przywróć poprawną funkcję, zbuduj projekt i uruchom testy jeszcze raz: wszystkie powinny przejść, z kodem 0.
9. **Wyjaśnij** w dwóch, trzech zdaniach, co pokazało `FAIL` po celowym błędzie, a czego nie pokazało.

<details>
<summary>Przypadki: otwórz po przygotowaniu własnej tabeli</summary>

Osiem przypadków z tabeli lekcji 13.2, z nowymi literami: przedział 17–20 był tam przypadkiem I.

| Przypadek | `start_hour` | `end_hour` | Wynik oczekiwany | Skąd |
|---|---:|---:|---|---|
| A | 8 | 9 | `true` | początek dokładnie o 8 |
| B | 8 | 11 | `true` | dokładnie trzy godziny |
| C | 8 | 12 | `false` | cztery godziny, za długo |
| D | 7 | 10 | `false` | początek przed 8 |
| E | 19 | 20 | `true` | koniec dokładnie o 20 |
| F | 20 | 20 | `false` | zerowa długość |
| G | 18 | 21 | `false` | koniec po 20 |
| H | 17 | 20 | `true` | trzy godziny i koniec dokładnie o 20 |

</details>

### Kryterium sukcesu

- Projekt ma dwa targety, `first_program` i `function_tests`, każdy z własnym plikiem z `main`.
- `rules.cpp` stoi na obu listach, a `rules.hpp` dołączają `main.cpp` i `function_tests.cpp`.
- Oba programy się budują, a program właściwy wypisuje `Slot 8-11: valid`.
- Z poprawną funkcją wszystkie testy dają `PASS`, a kod zakończenia testów wynosi 0.
- W `function_tests.cpp` nie ma definicji `is_valid_slot`, kopii jej warunków ani wyników oczekiwanych wyznaczanych przez jej wywołanie.
- Po celowej zmianie w `rules.cpp` testy przedziałów trwających dokładnie trzy godziny dają `FAIL`, kod zakończenia wynosi 1, a program właściwy wypisuje `Slot 8-11: invalid`.
- Po przywróceniu funkcji wszystkie testy znowu dają `PASS`, bez zmiany żadnego wyniku oczekiwanego.
- Umiesz pokazać, w którym pliku jest jedyna definicja funkcji, i wyjaśnić, dlaczego jedna zmiana w nim zmieniła wynik obu programów.

Gdy wynik się zgadza, możesz zapisać projekt w Gicie, jak w lekcji 1.5: pięć plików, bez katalogu budowania.

<details>
<summary>Podpowiedź 1: role plików</summary>

Gdzie powinna znaleźć się deklaracja funkcji, gdzie jej definicja, a gdzie każda z dwóch funkcji `main`? Który plik musi dołączyć nagłówek, żeby kompilator znał `is_valid_slot`? Porównaj swój plan z tabelą z punktu 2: zmienia się funkcja, a nie role plików.

</details>

<details>
<summary>Podpowiedź 2: dwa targety</summary>

Które pliki powinny stać w `add_executable(first_program ...)`, a które w `add_executable(function_tests ...)`? Na każdej liście musi być dokładnie jeden plik z `main`. Który plik musi stać na obu listach, żeby oba programy korzystały z tej samej funkcji?

</details>

<details>
<summary>Podpowiedź 3: regresja</summary>

Dlaczego po zmianie `rules.cpp` trzeba ponownie zbudować projekt i uruchomić testy, i dlaczego nie zmieniasz przy tym żadnego wyniku oczekiwanego? Skąd pochodzą wyniki oczekiwane i czy kontrakt się zmienił?

</details>

## 10. Gdy coś pójdzie inaczej

| Co widzisz | Co to znaczy | Co zrobić |
|---|---|---|
| W pasku narzędzi nie ma konfiguracji `function_tests` | Projekt CMake nie został wczytany ponownie albo linijka `add_executable(function_tests ...)` ma błąd. | Sprawdź tę linijkę i wybierz **Tools \| CMake \| Reload CMake Project**. |
| `multiple definition of` albo `duplicate symbol` z nazwą `main` | Plik z `main` jednego programu stoi na liście drugiego (punkt 8). | Każdy plik z `main` tylko na liście własnego targetu. |
| `multiple definition of` albo `duplicate symbol` z nazwą sprawdzanej funkcji | Plik testów zawiera kopię funkcji o tej samej nazwie (punkt 7). | Usuń kopię. Funkcja ma być tylko w `rules.cpp`. |
| `undefined reference`, `undefined symbol` albo `referenced from` z nazwą sprawdzanej funkcji przy linkowaniu jednego programu | Na liście tego programu brakuje `rules.cpp` albo definicja ma inną nazwę lub inne parametry niż deklaracja (lekcje 11.1 i 11.2). | Dopisz `rules.cpp` do obu list. Porównaj definicję z nagłówkiem. |
| `use of undeclared identifier` z nazwą sprawdzanej funkcji | Plik wywołuje funkcję, ale nie dołącza `rules.hpp`. | Dopisz `#include "rules.hpp"`. |
| W oknie **Run** widać opłatę albo `Slot ...` zamiast linijek `PASS` | Uruchomił się program właściwy. | Wybierz `function_tests` w pasku narzędzi i uruchom go jeszcze raz. |
| Po zmianie w `rules.cpp` wynik się nie zmienił | Uruchomiony program nie został przebudowany albo testy sprawdzają kopię funkcji (punkt 7). | Wybierz **Build Project** i uruchom testy jeszcze raz. Sprawdź, czy w pliku testów nie ma kopii. |
| Testy dają `FAIL`, a CLion pokazuje `exit code 1` | Testy wykryły niezgodność z kontraktem. Program się zbudował. | Porównaj wynik oczekiwany z kontraktem. Popraw funkcję albo, jeśli to wynik oczekiwany jest błędny, test. |

## 11. Wyjaśnij

Odpowiedz własnymi słowami, najlepiej na piśmie. Dopiero potem porównaj z przykładowymi odpowiedziami.

1. Co oznacza target w CMake?
2. Dlaczego jeden projekt może mieć dwie funkcje `main`?
3. Dlaczego nie mogą one trafić do jednego programu wykonywalnego?
4. Które pliki są wspólne dla obu targetów i w jaki sposób?
5. Dlaczego nie kopiujemy implementacji funkcji do programu testowego?
6. Co się stanie z oboma programami po zmianie w `rules.cpp`?
7. Dlaczego po zmianie implementacji trzeba ponownie zbudować projekt?
8. Czym różni się zbudowanie targetu od jego uruchomienia?
9. Dlaczego kod zakończenia 1 programu testowego nie oznacza błędu kompilacji?
10. Co potwierdza celowa usterka w `rules.cpp`, a czego nie potwierdza?

<details>
<summary>Przykładowe odpowiedzi</summary>

1. Coś, co CMake buduje, w tej lekcji program wykonywalny. Nazwą targetu jest pierwsze słowo w `add_executable`, a po nim stoi lista jego plików źródłowych.
2. Bo projekt może budować kilka programów. Każdy program ma własną funkcję `main`, w innym pliku i w innym targecie.
3. Bo program ma jeden punkt startu. Linker, który łączy pliki obiektowe jednego programu, dostałby dwie definicje `main` i zgłosiłby błąd.
4. `rules.cpp` stoi na listach obu targetów i jest kompilowany osobno dla każdego programu. `rules.hpp` nie stoi na żadnej liście: dołączają go `main.cpp`, `function_tests.cpp` i `rules.cpp`.
5. Bo testy sprawdzałyby wtedy kopię, a nie funkcję, której używa program. Zmiana w programie nie trafiłaby do testów, a zmiana w testach do programu.
6. Po przebudowaniu oba programy używają zmienionej funkcji: program właściwy wypisuje inny wynik, a testy porównują ten nowy wynik z wynikami oczekiwanymi.
7. Bo programy powstają z plików podczas budowania. Dopóki ich nie przebudujesz, uruchamiasz programy zbudowane ze starej wersji `rules.cpp`.
8. Zbudowanie tworzy program z plików, a uruchomienie wykonuje gotowy program. **Build Project** buduje oba programy i niczego nie uruchamia. **Run** uruchamia jeden, wybrany program.
9. Bo program, który się nie skompilował, w ogóle nie powstaje i nie może się uruchomić ani zwrócić żadnego kodu. Kod 1 zwrócił program testowy, który się zbudował, wykonał wszystkie sprawdzenia i znalazł niezgodność z kontraktem.
10. Potwierdza, że te konkretne testy wywołują funkcję z `rules.cpp` i wykrywają tę zmianę. Nie potwierdza, że funkcja jest poprawna dla wszystkich danych ani że każdy przyszły test będzie sprawdzał właściwą funkcję.

</details>

## Podsumowanie

- Testy kopii funkcji sprawdzają kopię. Żeby testy sprawdzały funkcję programu, oba programy muszą korzystać z jednej definicji.
- **Program i testy mają osobne funkcje `main`, ale korzystają z tych samych funkcji:** deklaracja we wspólnym nagłówku, jedyna definicja we wspólnym pliku `.cpp`.
- **Target** to coś, co CMake buduje. Jeden `CMakeLists.txt` może opisywać dwa programy: `first_program` z `main.cpp` i `function_tests` z `function_tests.cpp`, oba z `rules.cpp`.
- **Build Project** buduje oba programy. **Run** uruchamia jeden, wybrany w pasku narzędzi.
- Zmiana we wspólnym pliku trafia do obu programów po przebudowaniu. **Regresję** wykrywają zachowane testy, uruchomione ponownie bez zmiany wyników oczekiwanych.
- Poprawia się funkcję, żeby spełniała kontrakt, a nie test, żeby pasował do funkcji.
- Dwie funkcje `main` w jednym programie to błąd linkowania, a nie `FAIL`: program testowy w ogóle nie powstaje.
- Wspólne pliki nie gwarantują, że każde sprawdzenie wywołuje właściwą funkcję. Celowa usterka, która daje `FAIL`, pokazuje to dla konkretnych testów.

## Co dalej

Umiesz już sprawdzać wyniki funkcji, dobierać przypadki, testować odczyt bez pliku i trzymać testy obok programu, który korzysta z tych samych funkcji. Następna lekcja Modułu 13, jego sprawdzian, jest w przygotowaniu.

---

## Przykładowe rozwiązania

Zajrzyj tutaj **po własnej próbie**. Twoje nazwy przypadków i kolejność sprawdzeń mogą być inne, jeśli każda granica kontraktu jest sprawdzona, a pliki mają role z punktu 2.

<details>
<summary>Punkt 9: misja, rezerwacja sali w dwóch programach</summary>

**`rules.hpp`**:

<!-- file: slot_project rules.hpp -->
```cpp
#pragma once

bool is_valid_slot(int start_hour, int end_hour);
```

**`rules.cpp`**, jedyna definicja, przeniesiona z rozwiązania lekcji 13.2 bez zmian:

<!-- file: slot_project rules.cpp -->
```cpp
#include "rules.hpp"

bool is_valid_slot(int start_hour, int end_hour) {
    if (start_hour < 8 || end_hour > 20) {
        return false;
    }

    if (start_hour >= end_hour) {
        return false;
    }

    return end_hour - start_hour <= 3;
}
```

**`main.cpp`**, program właściwy:

<!-- example: slot_project target=function_tests -->
```cpp
#include <iostream>

#include "rules.hpp"

int main() {
    const int start_hour{8};
    const int end_hour{11};

    std::cout << "Slot " << start_hour << "-" << end_hour << ": ";

    if (is_valid_slot(start_hour, end_hour)) {
        std::cout << "valid\n";
    } else {
        std::cout << "invalid\n";
    }
}
```

**`function_tests.cpp`**, program testowy:

<!-- file: slot_project function_tests.cpp -->
```cpp
#include <iostream>
#include <string>

#include "rules.hpp"

std::string bool_text(bool value) {
    if (value) {
        return "true";
    }

    return "false";
}

void check_bool(const std::string& name, bool expected, bool actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << bool_text(expected) << ", actual " << bool_text(actual) << "\n";
        ++failed;
    }
}

int main() {
    int checks{0};
    int failed{0};

    check_bool("A 8-9", true, is_valid_slot(8, 9), checks, failed);
    check_bool("B 8-11", true, is_valid_slot(8, 11), checks, failed);
    check_bool("C 8-12", false, is_valid_slot(8, 12), checks, failed);
    check_bool("D 7-10", false, is_valid_slot(7, 10), checks, failed);
    check_bool("E 19-20", true, is_valid_slot(19, 20), checks, failed);
    check_bool("F 20-20", false, is_valid_slot(20, 20), checks, failed);
    check_bool("G 18-21", false, is_valid_slot(18, 21), checks, failed);
    check_bool("H 17-20", true, is_valid_slot(17, 20), checks, failed);

    std::cout << "Checks: " << checks << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

**`CMakeLists.txt`**:

<!-- cmake: slot_project -->
```cmake
cmake_minimum_required(VERSION 3.28)
project(first_program LANGUAGES CXX)

add_executable(first_program main.cpp rules.cpp)
target_compile_features(first_program PRIVATE cxx_std_20)
set_target_properties(first_program PROPERTIES CXX_EXTENSIONS OFF)

add_executable(function_tests function_tests.cpp rules.cpp)
target_compile_features(function_tests PRIVATE cxx_std_20)
set_target_properties(function_tests PROPERTIES CXX_EXTENSIONS OFF)
```

`first_program` wypisuje:

```text
Slot 8-11: valid
```

`function_tests` wypisuje:

<!-- output: slot_project -->
```text
PASS A 8-9
PASS B 8-11
PASS C 8-12
PASS D 7-10
PASS E 19-20
PASS F 20-20
PASS G 18-21
PASS H 17-20
Checks: 8, failed: 0
```

Kod zakończenia testów: 0.

- **Współdzielenie:** `is_valid_slot` jest zdefiniowana tylko w `rules.cpp`, a ten plik stoi na listach obu targetów. `main.cpp` i `function_tests.cpp` znają funkcję z `rules.hpp`.
- **Testy:** wyniki oczekiwane to wartości z tabeli przypadków, wpisane jako `true` i `false`. Żaden nie powstał przez wywołanie `is_valid_slot`, a w pliku testów nie ma jej warunków.
- **Program właściwy** wybiera tekst według wyniku funkcji, więc sam nie powtarza żadnego warunku z kontraktu.

**Celowy błąd:** `end_hour - start_hour < 3` zamiast `<= 3`, tylko w `rules.cpp`. Program testowy i wyniki oczekiwane się nie zmieniają.

`function_tests` wypisuje:

<!-- output: slot_project_bug -->
```text
PASS A 8-9
FAIL B 8-11: expected true, actual false
PASS C 8-12
PASS D 7-10
PASS E 19-20
PASS F 20-20
PASS G 18-21
FAIL H 17-20: expected true, actual false
Checks: 8, failed: 2
```

Kod zakończenia testów: 1. `first_program` wypisuje:

```text
Slot 8-11: invalid
```

- **Które sprawdzenia:** B i H, oba przedziały trwające dokładnie trzy godziny. Dla nich `3 < 3` jest fałszem, więc funkcja zwraca `false` zamiast `true`.
- **Dlaczego pozostałe przechodzą:** A i E są krótsze niż trzy godziny, C jest za długi w obu wersjach, a D, F i G są odrzucane przez wcześniejsze warunki, zanim funkcja sprawdzi długość.
- **Program właściwy** pokazuje ten sam błąd, bo przedział 8–11 trwa dokładnie trzy godziny.
- **Po poprawce** plik `rules.cpp` jest znowu taki jak wyżej, więc oba programy wypisują to samo co w pierwszej wersji, a testy kończą się kodem 0.
- **Co to pokazuje:** te osiem sprawdzeń wywołuje funkcję z `rules.cpp` i dwa z nich wykrywają tę zmianę. Nie pokazuje to, że funkcja jest poprawna dla wszystkich godzin.

<details>
<summary>Wszystkie pliki wersji z usterką</summary>

Te same pliki co wyżej, poza ostatnią linijką `is_valid_slot`.

**`main.cpp`**:

<!-- example: slot_project_bug target=function_tests exit=1 -->
```cpp
#include <iostream>

#include "rules.hpp"

int main() {
    const int start_hour{8};
    const int end_hour{11};

    std::cout << "Slot " << start_hour << "-" << end_hour << ": ";

    if (is_valid_slot(start_hour, end_hour)) {
        std::cout << "valid\n";
    } else {
        std::cout << "invalid\n";
    }
}
```

**`rules.hpp`**:

<!-- file: slot_project_bug rules.hpp -->
```cpp
#pragma once

bool is_valid_slot(int start_hour, int end_hour);
```

**`rules.cpp`**, z usterką:

<!-- file: slot_project_bug rules.cpp -->
```cpp
#include "rules.hpp"

bool is_valid_slot(int start_hour, int end_hour) {
    if (start_hour < 8 || end_hour > 20) {
        return false;
    }

    if (start_hour >= end_hour) {
        return false;
    }

    return end_hour - start_hour < 3;
}
```

**`function_tests.cpp`**:

<!-- file: slot_project_bug function_tests.cpp -->
```cpp
#include <iostream>
#include <string>

#include "rules.hpp"

std::string bool_text(bool value) {
    if (value) {
        return "true";
    }

    return "false";
}

void check_bool(const std::string& name, bool expected, bool actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << bool_text(expected) << ", actual " << bool_text(actual) << "\n";
        ++failed;
    }
}

int main() {
    int checks{0};
    int failed{0};

    check_bool("A 8-9", true, is_valid_slot(8, 9), checks, failed);
    check_bool("B 8-11", true, is_valid_slot(8, 11), checks, failed);
    check_bool("C 8-12", false, is_valid_slot(8, 12), checks, failed);
    check_bool("D 7-10", false, is_valid_slot(7, 10), checks, failed);
    check_bool("E 19-20", true, is_valid_slot(19, 20), checks, failed);
    check_bool("F 20-20", false, is_valid_slot(20, 20), checks, failed);
    check_bool("G 18-21", false, is_valid_slot(18, 21), checks, failed);
    check_bool("H 17-20", true, is_valid_slot(17, 20), checks, failed);

    std::cout << "Checks: " << checks << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

**`CMakeLists.txt`**:

<!-- cmake: slot_project_bug -->
```cmake
cmake_minimum_required(VERSION 3.28)
project(first_program LANGUAGES CXX)

add_executable(first_program main.cpp rules.cpp)
target_compile_features(first_program PRIVATE cxx_std_20)
set_target_properties(first_program PROPERTIES CXX_EXTENSIONS OFF)

add_executable(function_tests function_tests.cpp rules.cpp)
target_compile_features(function_tests PRIVATE cxx_std_20)
set_target_properties(function_tests PROPERTIES CXX_EXTENSIONS OFF)
```

</details>

</details>

**Poprzednia lekcja:** [Lekcja 13.3: Testowanie odczytu bez pliku](lesson_03_testing_input_without_a_file.md) · **Następna lekcja:** w przygotowaniu · [Opis kursu](../../README.md)

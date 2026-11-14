# Lekcja 11.1: Drugi plik źródłowy

**Polski** · [English](lesson_01_second_source_file.en.md) · [Opis kursu](../../README.md)

> **Moduł 11, lekcja 1** · około 80–100 minut
> **Potrzebujesz:** katalogu `cpp-workspace` i oryginalnego projektu `lesson_05_first_program`, jak dotąd. Debugger nie jest w tej lekcji potrzebny.
> **Wersja pilotażowa.** Programy z tej lekcji, także te zbudowane z dwóch plików źródłowych, sprawdzamy automatycznie na Windowsie, Ubuntu i macOS, z podanymi danymi wejściowymi. Kroki w CLionie (nowy plik, ponowne wczytanie projektu CMake, wpisywanie danych w oknie **Run**) opisujemy według dokumentacji CLion 2026.2, bez ręcznego sprawdzenia na każdym systemie.

## Zanim zaczniesz

Ta lekcja zakłada, że:

- wiesz, że budowanie ma dwa etapy: kompilator tłumaczy plik źródłowy na plik obiektowy, a linker łączy go z kodem biblioteki i kodem startowym w program (lekcja 1.4);
- znasz linijki `CMakeLists.txt` i wiesz, że `add_executable` podaje nazwę programu i jego plik źródłowy (lekcja 1.4);
- odróżniasz deklarację funkcji od jej definicji i wiesz, że brak definicji wywoływanej funkcji to błąd linkowania (lekcja 5.6);
- piszesz funkcje z parametrami, które zwracają wynik (lekcje 5.2 i 5.3).

## Sytuacja

Programy z ostatnich modułów rosły. Rozwiązanie sprawdzianu z lekcji 10.5 ma w jednym pliku typ, dwie funkcje i `main`. Im dłuższy plik, tym trudniej znaleźć w nim potrzebną funkcję. Dlatego większe programy składają się z kilku plików źródłowych. W tej lekcji przeniesiesz jedną funkcję do drugiego pliku `.cpp` i odpowiesz na dwa pytania: **co `main.cpp` musi wiedzieć o funkcji, której definicja jest w innym pliku?** I **skąd narzędzia wiedzą, że program składa się z dwóch plików?**

Po tej lekcji będziesz:

- budować jeden program z dwóch plików `.cpp`;
- umieszczać w `main.cpp` deklarację funkcji, a jej definicję w drugim pliku;
- sprawdzać, czy deklaracja pasuje do definicji;
- dopisywać plik źródłowy do `add_executable` w `CMakeLists.txt`;
- wyjaśniać, że każdy plik `.cpp` jest kompilowany osobno, a linker łączy wyniki w jeden program;
- rozpoznawać błąd linkowania, gdy plik z definicją istnieje, ale nie jest budowany, i naprawiać go w `CMakeLists.txt`.

## 1. Przygotuj projekt

W `cpp-workspace` utwórz katalog `lesson_11_1` i skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program`. W tej lekcji zmienisz w tym katalogu oba pliki i dodasz trzeci.

Jeśli pracujesz w CLionie, otwórz ten katalog jak w lekcji 1.1: **File | Open**, potem **Trust Project** i profil **Debug**. W oknie **CMake** sprawdź, że kompilator to `Clang 22`.

Programy z tej lekcji nie wypisują pytań. Po uruchomieniu od razu wpisz obie liczby, oddzielone spacją, i naciśnij **Enter**. Zakładamy poprawne dane: dwie niewielkie liczby nieujemne. Programy nie sprawdzają odczytu, żeby nic nie odciągało uwagi od podziału na pliki. Program, który ma przyjmować dowolne dane, sprawdzałby odczyt, jak w lekcji 4.5.

## 2. Punkt wyjścia: deklaracja i definicja w jednym pliku

Program liczy punkty za rozwiązane zadania. Każde rozwiązane zadanie daje 3 punkty, a do wyniku dochodzą punkty bonusowe. Wpisz go do `main.cpp` w katalogu `lesson_11_1`:

<!-- example: points_one_file -->
```cpp
#include <iostream>

int calculate_points(int solved, int bonus);

int main() {
    int solved{0};
    int bonus{0};

    std::cin >> solved;
    std::cin >> bonus;

    std::cout << "Points: " << calculate_points(solved, bonus) << "\n";
}

int calculate_points(int solved, int bonus) {
    const int points_per_task{3};
    return solved * points_per_task + bonus;
}
```

To układ z lekcji 5.6: deklaracja, `main`, definicja. Uruchomienie jest nieobowiązkowe. Dla danych `4 2`:

<!-- input: points_one_file -->
```text
4 2
```

<!-- output: points_one_file -->
```text
Points: 14
```

Ta sama sygnatura występuje tu w dwóch rolach:

| Zapis | Co to jest | Do czego służy |
|---|---|---|
| `int calculate_points(int solved, int bonus);` | **deklaracja**: nazwa, typ wyniku i typy parametrów, zakończone średnikiem | mówi kompilatorowi, że funkcja istnieje i jak ją wywołać, więc wywołanie w `main` się kompiluje |
| ta sama sygnatura z ciałem w klamrach | **definicja** | dostarcza działanie: instrukcje, które wykonują się przy każdym wywołaniu. Linker musi ją znaleźć |

Dzięki deklaracji kompilator może skompilować wywołanie, zanim zobaczy definicję. Dlatego definicja może stać pod `main`, a w następnym punkcie: w innym pliku.

## 3. Drugi plik źródłowy

Teraz przeniesiesz definicję do nowego pliku. Utwórz w katalogu `lesson_11_1`, obok `main.cpp`, plik `points.cpp`:

- **W CLionie** (według dokumentacji CLion 2026.2): w oknie **Project** kliknij prawym przyciskiem myszy katalog projektu, ten sam, w którym jest `main.cpp`, i wybierz **New | C/C++ Source File**. Wpisz nazwę `points` i zostaw typ `.cpp`. Nie zaznaczaj opcji **Create an associated header**: własne pliki nagłówkowe poznasz w następnej lekcji. W tym samym oknie CLion może zaproponować dodanie pliku do targetu `first_program` (**Add to targets**). Możesz z tego skorzystać albo nie: w punkcie 4 i tak sprawdzisz `CMakeLists.txt`. Jeśli CLion wstawi do nowego pliku komentarz, na przykład z nazwą pliku i datą, możesz go zostawić albo usunąć: komentarz nie zmienia programu.
- **W innym edytorze tekstu**, który zapisuje zwykły tekst: zapisz plik jako `points.cpp` w tym samym katalogu co `main.cpp`.

Potem:

1. **Wytnij** z `main.cpp` całą definicję `calculate_points`, od sygnatury do zamykającej klamry.
2. **Wklej** ją do `points.cpp`.
3. **Zostaw** w `main.cpp` `#include <iostream>`, deklarację i `main`.

Nie kopiuj definicji: po przeniesieniu ma być tylko w `points.cpp`.

**`main.cpp`** po zmianie:

<!-- example: points -->
```cpp
#include <iostream>

int calculate_points(int solved, int bonus);

int main() {
    int solved{0};
    int bonus{0};

    std::cin >> solved;
    std::cin >> bonus;

    std::cout << "Points: " << calculate_points(solved, bonus) << "\n";
}
```

**`points.cpp`**:

<!-- file: points points.cpp -->
```cpp
int calculate_points(int solved, int bonus) {
    const int points_per_task{3};
    return solved * points_per_task + bonus;
}
```

| Plik | Co zawiera | Czego nie zawiera |
|---|---|---|
| `main.cpp` | `#include <iostream>`, deklarację `calculate_points` i `main`: odczyt, wywołanie i wypisanie wyniku | definicji `calculate_points` |
| `points.cpp` | definicję `calculate_points` | `main`, odczytu, wypisywania i `#include <iostream>` |

- `points.cpp` nie potrzebuje `#include <iostream>`: funkcja niczego nie odczytuje i nie wypisuje, korzysta tylko z `int`.
- Program ma jedno `main`, w `main.cpp`. Od niego zaczyna się wykonywanie, jak dotąd.

Programu jeszcze nie budujesz: najpierw trzeba powiedzieć narzędziom, że ma dwa pliki źródłowe.

## 4. Dopisz plik do `CMakeLists.txt`

Sam plik `points.cpp` w katalogu projektu jeszcze niczego nie zmienia. Narzędzia budują tylko te pliki źródłowe, które wymienia `add_executable`, a w skopiowanym `CMakeLists.txt` jest tylko `main.cpp`. Zmień w nim jedną linijkę, tak żeby cały plik wyglądał tak:

<!-- cmake: points -->
```cmake
cmake_minimum_required(VERSION 3.28)
project(first_program LANGUAGES CXX)

add_executable(first_program main.cpp points.cpp)
target_compile_features(first_program PRIVATE cxx_std_20)
set_target_properties(first_program PROPERTIES CXX_EXTENSIONS OFF)
```

- **Jedyna zmiana** wobec pliku z lekcji 0.5: w linijce `add_executable` po `main.cpp` jest spacja i `points.cpp`. Pozostałe linijki zostają bez zmian.
- Dopisujesz **nazwę pliku**, a nie nazwę funkcji. CMake nie wie, jakie funkcje są w plikach. Zapisuje plan: skompilować każdy wymieniony plik i połączyć wyniki w program `first_program`.
- **Kolejność nazw nie jest kolejnością wykonywania.** Zapis `add_executable(first_program points.cpp main.cpp)` zbuduje ten sam program. Wykonywanie zawsze zaczyna się od `main`.
- Jeśli `points.cpp` dopisał CLion, porównaj tę linijkę z pokazaną wyżej. W tej lekcji wszystkie pliki źródłowe stoją w jednej linijce `add_executable`, oddzielone spacjami.

## 5. Zbuduj i uruchom program z dwóch plików

**W CLionie** (według dokumentacji CLion 2026.2, bez ręcznego sprawdzenia na każdym systemie):

1. Po zmianie `CMakeLists.txt` CLion pokazuje informację, że projekt CMake trzeba wczytać ponownie. Kliknij ją albo wybierz **Tools | CMake | Reload CMake Project**. Gdy plik do targetu dodał sam CLion, wczytuje on projekt ponownie automatycznie.
2. Wybierz **Build | Build Project**.
3. Kliknij **Run** (▶), wpisz w oknie **Run** `4 2` i naciśnij **Enter**.

**W terminalu:**

1. Przejdź do katalogu `lesson_11_1`, jak w lekcji 0.6.
2. Skonfiguruj projekt w katalogu `build-terminal`, tym samym poleceniem co w lekcji 1.4:

   | System | Konfiguracja |
   |---|---|
   | Windows | `cmake -S . -B build-terminal -G Ninja -DCMAKE_BUILD_TYPE=Debug "-DCMAKE_CXX_COMPILER=C:\Program Files\LLVM\bin\clang++.exe"` |
   | macOS | `cmake -S . -B build-terminal -G Ninja -DCMAKE_BUILD_TYPE=Debug -DCMAKE_CXX_COMPILER=/opt/homebrew/opt/llvm@22/bin/clang++` |
   | Ubuntu | `cmake -S . -B build-terminal -G Ninja -DCMAKE_BUILD_TYPE=Debug -DCMAKE_CXX_COMPILER=/usr/bin/clang++-22` |

   Na macOS z procesorem Intel zamiast `/opt/homebrew/opt/llvm@22` wpisz `/usr/local/opt/llvm@22`, jak w lekcji 0.6.
3. Zbuduj: `cmake --build build-terminal`. Jeśli `build-terminal` istniał już przed zmianą `CMakeLists.txt`, konfiguracji nie musisz powtarzać: jak w lekcji 1.4, Ninja zauważy zmianę i najpierw sam uruchomi CMake (`Re-running CMake...`).
4. Uruchom program: `.\build-terminal\first_program.exe` (macOS i Ubuntu: `./build-terminal/first_program`), wpisz `4 2` i naciśnij **Enter**.

W wyniku budowania, w oknie **Build** albo w terminalu, znajdź linijki o kompilacji i linkowaniu. Wyglądają mniej więcej tak:

```text
Building CXX object CMakeFiles/first_program.dir/main.cpp.o
Building CXX object CMakeFiles/first_program.dir/points.cpp.o
Linking CXX executable first_program
```

Są **dwie** linijki `Building CXX object`, po jednej dla każdego pliku `.cpp`, i **jedna** linijka `Linking`. Na Windowsie pliki obiektowe kończą się na `.obj`, a program na `.exe`. Kolejność dwóch pierwszych linijek może być inna, a wcześniejsze kroki, na przykład `Scanning ... for CXX dependencies`, przygotowują budowanie.

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

To samo co program z jednego pliku w punkcie 2: logika funkcji się nie zmieniła, zmieniło się tylko miejsce jej definicji.

**Przewidź**, co program wypisze dla danych `0 5`, i porównaj ze zwiniętym wynikiem. Uruchomienie jest nieobowiązkowe.

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

Zero rozwiązanych zadań daje 0 punktów za zadania, więc wynik to same punkty bonusowe: `0 * 3 + 5`.

</details>

## 6. Jak współpracują kompilator i linker

```text
main.cpp    ──►  kompilacja  ──►  main.cpp.o    ──┐
                                                 ├──►  linkowanie  ──►  first_program
points.cpp  ──►  kompilacja  ──►  points.cpp.o  ──┘
```

- **Każdy plik `.cpp` jest kompilowany osobno.** Kompilując `main.cpp`, kompilator nie widzi `points.cpp`, a kompilując `points.cpp`, nie widzi `main.cpp`. Z każdego pliku powstaje osobny plik obiektowy. Plik źródłowy razem z tym, co wstawiają do niego linijki `#include`, nazywa się **jednostką translacji** (ang. *translation unit*). Ta nazwa nie będzie Ci potrzebna w zadaniach.
- **Do skompilowania wywołania wystarcza deklaracja.** W `main.cpp` kompilator zna z deklaracji nazwę, typ wyniku i typy parametrów `calculate_points`, więc może przygotować wywołanie. Ciała funkcji nie potrzebuje.
- **Definicja jest kompilowana w drugim pliku.** Instrukcje funkcji trafiają do `points.cpp.o`.
- **Linker łączy oba pliki obiektowe w jeden program.** Wywołanie z `main.cpp.o` potrzebuje pasującej definicji, a linker znajduje ją w `points.cpp.o`. W lekcji 5.6 program miał jeden plik obiektowy, a teraz linker szuka we wszystkich, które dostaje.
- **Plików nie sklejasz ręcznie.** Wystarczy, że oba są w `add_executable`: CMake i Ninja kompilują każdy z nich i przekazują linkerowi oba pliki obiektowe.

**Deklaracja i definicja muszą być zgodne**, jak w lekcji 5.6:

| Co | W deklaracji (`main.cpp`) | W definicji (`points.cpp`) |
|---|---|---|
| nazwa funkcji | `calculate_points` | `calculate_points` |
| typ wyniku | `int` | `int` |
| liczba parametrów | 2 | 2 |
| typy parametrów, w tej samej kolejności | `int`, `int` | `int`, `int` |

Nazwy parametrów mogą się różnić. Kompilator, który kompiluje `main.cpp`, nie widzi definicji, więc nie porówna jej z deklaracją. Porównaj je samodzielnie, za każdym razem, gdy zmieniasz jedną z nich. Skutków niezgodności w tej lekcji nie omawiamy: trzymaj deklarację i definicję zgodne.

**Plików `.cpp` nie łączymy przez `#include`.** `#include` wstawia tekst innego pliku (lekcja 1.4). Pliki źródłowe programu łączy linker, a ich listę podaje `add_executable`. Dlaczego `#include "points.cpp"` byłoby złym pomysłem, wyjaśnia pytanie 9 w punkcie 10.

## 7. Misja: koszt biletów

Kasa kina sprzedaje dwa rodzaje biletów: **zwykły** za 12 jednostek i **ulgowy** za 7 jednostek. Program odczytuje liczbę biletów obu rodzajów i wypisuje łączny koszt.

**Wymagania:**

- Program odczytuje dwie liczby całkowite oddzielone spacją: najpierw liczbę biletów zwykłych, potem liczbę biletów ulgowych. Nie wypisuje pytań.
- Łączny koszt to liczba biletów zwykłych razy 12 plus liczba biletów ulgowych razy 7.
- Program wypisuje dokładnie jedną linię, `Total cost: N`, bez dodatkowych komunikatów.
- **Koszt oblicza Twoja funkcja, której definicja stoi w drugim pliku `.cpp`.** Nazwy funkcji i parametrów wybierasz samodzielnie.
- `main.cpp` zawiera deklarację funkcji i `main`: odczyt, wywołanie funkcji i wypisanie wyniku. Nie zawiera definicji funkcji.
- Drugi plik `.cpp` zawiera tylko definicję funkcji: bez `main`, bez odczytu i bez wypisywania.
- `CMakeLists.txt` to plik z lekcji 0.5 z drugim plikiem dopisanym w linijce `add_executable`.
- Nie dołączaj drugiego pliku przez `#include` i nie kopiuj definicji do `main.cpp`.
- Wartości są nieujemne i niewielkie, a wynik mieści się w `int`. Program nie musi sprawdzać danych ani radzić sobie z błędnym odczytem.

W `cpp-workspace` utwórz katalog `ticket_cost`, skopiuj do niego `CMakeLists.txt` z oryginalnego `lesson_05_first_program` i utwórz pusty `main.cpp` oraz drugi plik `.cpp` o wybranej przez siebie nazwie. Nazwa drugiego pliku składa się z małych liter angielskich, cyfr i `_`, zaczyna się od litery i kończy na `.cpp`, na przykład `prices.cpp`. Nie może to być `main.cpp`. Napisz program samodzielnie.

**Dane A:** dwa bilety zwykłe i trzy ulgowe.

<!-- input: tickets -->
```text
2 3
```

<!-- output: tickets -->
```text
Total cost: 45
```

**Dane B:** bez biletów zwykłych.

<!-- input: tickets -->
```text
0 4
```

<!-- output: tickets -->
```text
Total cost: 28
```

**Dane C:** bez żadnych biletów.

<!-- input: tickets -->
```text
0 0
```

<!-- output: tickets -->
```text
Total cost: 0
```

**Przewidź D:** same bilety zwykłe, trzy sztuki.

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

**To nie jest kalkulator punktów z innymi nazwami.** Funkcja ma dwie ceny i inne parametry, a projekt tworzysz od pustego `main.cpp`. Musisz samodzielnie zdecydować:

1. jak nazwać funkcję;
2. jak nazwać jej parametry;
3. jak zapisać deklarację;
4. jak zapisać definicję, żeby pasowała do deklaracji;
5. gdzie stoi deklaracja;
6. gdzie stoi definicja;
7. co zawiera `main()`;
8. jak nazwać drugi plik `.cpp`;
9. jakie pliki wymienić w `add_executable`;
10. jakimi danymi sprawdzić program.

**Zanim napiszesz program**, przygotuj krótką tabelę: dane A–D i co najmniej jeden własny przypadek, z oczekiwanym wynikiem policzonym na kartce.

**Potem** uruchom program dla danych A i jednego przypadku granicznego: B albo C. Pozostałe przypadki porównaj z wynikami z tabeli. Wszystkie przypadki A–D są sprawdzone automatycznie w rozwiązaniu referencyjnym.

### Kryterium sukcesu

- Program buduje się jako C++20 z dwóch plików `.cpp`, a dla danych A oraz B albo C wypisuje dokładnie pokazany wynik.
- Przewidywania dla pozostałych przypadków zgadzają się z wynikami podanymi wyżej.
- W `main.cpp` jest deklaracja funkcji i `main`, a definicji nie ma. Drugi plik zawiera tylko definicję: bez `main`, odczytu i wypisywania.
- Deklaracja pasuje do definicji: ta sama nazwa, typ wyniku, liczba i typy parametrów.
- `CMakeLists.txt` różni się od pliku z lekcji 0.5 tylko nazwą drugiego pliku w linijce `add_executable`.
- Przy pierwszym budowaniu w wyniku widać kompilację obu plików `.cpp`.
- Żaden plik nie dołącza pliku `.cpp` przez `#include`.
- Umiesz powiedzieć, co kompilator wie o funkcji, gdy kompiluje każdy z plików, i co łączy linker.

Gdy wynik się zgadza, możesz zapisać projekt w Gicie, jak w lekcji 1.5. Tym razem do commita należą trzy pliki: `main.cpp`, drugi plik `.cpp` i `CMakeLists.txt`. Przed commitem sprawdź w `git status`, że jest wśród nich drugi plik `.cpp`.

<details>
<summary>Podpowiedź 1</summary>

Co musi wiedzieć `main.cpp` o funkcji zdefiniowanej w innym pliku? Kompilator, który kompiluje `main.cpp`, nie zagląda do drugiego pliku. To, czego potrzebuje w miejscu wywołania, podaje jedna linijka zakończona średnikiem.

</details>

<details>
<summary>Podpowiedź 2</summary>

Dlaczego definicja powinna znajdować się w drugim `.cpp`, a plik musi zostać dodany do CMake'a? Definicja to funkcja z ciałem, czyli z obliczeniem. Plik, którego nie ma w `add_executable`, nie jest kompilowany, więc linker nie dostanie jego definicji.

</details>

<details>
<summary>Podpowiedź 3</summary>

Jak porównać deklarację i definicję oraz sprawdzić listę źródeł `add_executable`? Zapisz obie sygnatury jedna pod drugą i porównaj nazwę, typ wyniku, liczbę i typy parametrów. W `add_executable` muszą stać `main.cpp` i nazwa drugiego pliku, dokładnie taka jak na dysku.

</details>

Przykładowe rozwiązanie jest w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 8. Znajdź błąd: plik istnieje, ale nie jest budowany

To zadanie wykonaj **po misji**. Ktoś przygotował nowy projekt kalkulatora punktów tak jak w każdej dotychczasowej lekcji: skopiował `CMakeLists.txt` z oryginalnego `lesson_05_first_program`, a `main.cpp` i `points.cpp` z katalogu `lesson_11_1`. Oba pliki źródłowe istnieją i są poprawne.

Odtwórz ten projekt: w `cpp-workspace` utwórz katalog `points_link_check` i skopiuj do niego `main.cpp` i `points.cpp` z `lesson_11_1` oraz `CMakeLists.txt` z oryginalnego `lesson_05_first_program`. Niczego w nich nie zmieniaj.

<details>
<summary>Pliki projektu do sprawdzenia: otwórz po misji</summary>

**`main.cpp`**, taki sam jak w punkcie 3:

<!-- broken: points_link_check stage=link error=undefined reference to .calculate_points\(int, int\)'|undefined symbol: int __cdecl calculate_points\(int, int\)|"calculate_points\(int, int\)", referenced from -->
```cpp
#include <iostream>

int calculate_points(int solved, int bonus);

int main() {
    int solved{0};
    int bonus{0};

    std::cin >> solved;
    std::cin >> bonus;

    std::cout << "Points: " << calculate_points(solved, bonus) << "\n";
}
```

**`points.cpp`**, taki sam jak w punkcie 3:

<!-- file: points_link_check points.cpp -->
```cpp
int calculate_points(int solved, int bonus) {
    const int points_per_task{3};
    return solved * points_per_task + bonus;
}
```

**`CMakeLists.txt`**, taki sam jak w oryginalnym `lesson_05_first_program`:

<!-- cmake: points_link_check -->
```cmake
cmake_minimum_required(VERSION 3.28)
project(first_program LANGUAGES CXX)

add_executable(first_program main.cpp)
target_compile_features(first_program PRIVATE cxx_std_20)
set_target_properties(first_program PROPERTIES CXX_EXTENSIONS OFF)
```

</details>

**Zanim zbudujesz**, odpowiedz na piśmie:

1. **Przewidź:** czy budowanie się uda? Jeśli nie, na którym etapie: kompilacji czy linkowania?
2. W którym pliku jest definicja `calculate_points`?
3. Jakie pliki wymienia `add_executable` w `CMakeLists.txt`?
4. Dlaczego sam plik `points.cpp` w katalogu projektu nie wystarcza?

**Potem:**

5. Zbuduj projekt: w terminalu (konfiguracja `build-terminal` jak w punkcie 5, potem `cmake --build build-terminal`) albo w CLionie (otwórz katalog jak w punkcie 1 i wybierz **Build | Build Project**). Przeczytaj wynik budowania: które pliki były kompilowane i co zgłasza linker?
6. Dopisz `points.cpp` do `add_executable`, jak w punkcie 4. Nie zmieniaj `main.cpp` ani `points.cpp`.
7. Zbuduj projekt ponownie (w CLionie najpierw wczytaj ponownie projekt CMake), uruchom program i wpisz `4 2`. Porównaj wynik z punktem 5.
8. Wyjaśnij, dlaczego naprawa nie wymagała zmiany kodu funkcji.

<details>
<summary>Co się dzieje i dlaczego: otwórz po zbudowaniu błędnego projektu</summary>

1. **Kompilacja się udaje.** W wyniku budowania jest jedna linijka `Building CXX object`, dla `main.cpp`. Kompilator zna `calculate_points` z deklaracji, więc wywołanie się kompiluje. `points.cpp` nie jest kompilowany wcale, bo nie ma go w `add_executable`.
2. **Linkowanie się nie udaje.** Linker dostaje tylko plik obiektowy `main.cpp`. Szuka definicji `calculate_points`, bo `main` ją wywołuje, i nie znajduje jej. Komunikat zależy od systemu: na Ubuntu ``undefined reference to `calculate_points(int, int)'``, na macOS `"calculate_points(int, int)", referenced from`, a na Windowsie `undefined symbol: int __cdecl calculate_points(int, int)`. Na końcu jest `linker command failed`.
3. **Program nie powstaje.**

To ten sam rodzaj błędu co w lekcji 5.6, punkt 7: wywołana funkcja nie ma w programie definicji. Różnica: tam definicji nie było nigdzie, a tu jest w pliku, którego narzędzia nie budują. Dla CMake'a plik na dysku nie jest jeszcze częścią programu. Częścią programu jest plik wymieniony w `add_executable`.

Po dopisaniu `points.cpp` Ninja najpierw sam uruchamia CMake, a potem kompiluje `points.cpp` i linkuje program. `main.cpp` może nie być kompilowany ponownie: nie zmienił się, a jego plik obiektowy już istnieje. Program wypisuje `Points: 14`, tak jak w punkcie 5.

Kod C++ był poprawny od początku. Błąd nie leżał w żadnym pliku `.cpp`, tylko w liście plików do zbudowania, dlatego naprawa dotyczy wyłącznie `CMakeLists.txt`.

| Sytuacja | Etap, który się nie udaje | Przyczyna | Naprawa |
|---|---|---|---|
| wywołanie bez deklaracji w `main.cpp` | kompilacja `main.cpp` | kompilator nie zna funkcji w miejscu wywołania | dopisz deklarację przed `main` |
| `points.cpp` nie ma w `add_executable` (ten punkt) | linkowanie | definicja nie trafia do programu | dopisz `points.cpp` do `add_executable` |
| `add_executable` wymienia plik, którego nie ma w katalogu projektu | konfiguracja (CMake) | CMake nie znajduje pliku źródłowego | popraw nazwę w `add_executable` albo nazwę pliku |
| oba pliki w `add_executable`, deklaracja zgodna z definicją | budowanie się udaje | | |

</details>

Poprawiony projekt jest w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 9. Gdy coś pójdzie inaczej

| Co widzisz | Co to znaczy | Co zrobić |
|---|---|---|
| `undefined reference`, `undefined symbol` albo `referenced from` z nazwą Twojej funkcji, a na końcu `linker command failed` | Kompilacja się udała, ale linker nie znajduje definicji: drugiego pliku nie ma w `add_executable` albo definicja nie pasuje do deklaracji. | Sprawdź linijkę `add_executable`. Potem porównaj deklarację z definicją: nazwę, typ wyniku, liczbę i typy parametrów. |
| Przy pierwszym budowaniu jest tylko jedna linijka `Building CXX object`, dla `main.cpp`, albo CLion po zmianie `CMakeLists.txt` buduje tak, jakby zmiany nie było | Drugi plik nie jest budowany: nie ma go w `add_executable` albo CLion nie wczytał jeszcze zmienionego `CMakeLists.txt`. | Dopisz plik do `add_executable`. W CLionie kliknij informację o ponownym wczytaniu albo wybierz **Tools \| CMake \| Reload CMake Project**. |
| `CMake Error at CMakeLists.txt:4 (add_executable):` i `Cannot find source file:` | Nazwa w `add_executable` nie zgadza się z plikiem w katalogu projektu: literówka, inna wielkość liter, plik w innym katalogu albo dodatkowe rozszerzenie dopisane przez edytor, na przykład `points.cpp.txt` (Windows domyślnie ukrywa znane rozszerzenia). Kompilator jeszcze nie ruszył (lekcja 1.4). | Sprawdź nazwę pliku w terminalu poleceniem `ls` i porównaj ją z nazwą w `add_executable`, litera po literze. |
| `use of undeclared identifier` z nazwą funkcji, w `main.cpp` | W `main.cpp` brakuje deklaracji albo stoi ona pod wywołaniem. Definicja w drugim pliku nie wystarcza kompilatorowi. | Dopisz deklarację przed `main`. |
| Linker zgłasza, że funkcja albo `main` jest zdefiniowana więcej niż raz, na przykład `duplicate symbol` albo `multiple definition` | Ta sama definicja jest w dwóch plikach: definicję skopiowano zamiast przenieść, w obu plikach jest `main` albo `main.cpp` dołącza drugi plik przez `#include`. | Zostaw definicję funkcji tylko w drugim pliku, a `main` tylko w `main.cpp`. Nie dołączaj plików `.cpp` przez `#include`. |
| Obok `points.cpp` powstał plik nagłówkowy, a w `points.cpp` jest linijka `#include` z jego nazwą | W oknie nowego pliku w CLionie zaznaczono **Create an associated header**. | Usuń ten plik, linijkę `#include` z `points.cpp` i nazwę pliku nagłówkowego z `add_executable`, jeśli CLion ją tam dopisał. Własne pliki nagłówkowe poznasz w następnej lekcji. |
| Program nic nie wypisuje i czeka | Czeka na drugą liczbę. | Wpisz obie liczby i naciśnij **Enter**. |

## 10. Wyjaśnij

Odpowiedz własnymi słowami, najlepiej na piśmie. Dopiero potem porównaj z przykładowymi odpowiedziami.

1. Co jest w `main.cpp`, a co w `points.cpp`? Czego w `points.cpp` nie ma i dlaczego?
2. Po co w `main.cpp` deklaracja `calculate_points`, skoro definicja jest w `points.cpp`?
3. Co dostarcza definicja i kiedy wykonują się jej instrukcje?
4. Co musi być takie samo w deklaracji i w definicji? Dlaczego zgodność trzeba sprawdzić samodzielnie?
5. Co zmieniło się w `CMakeLists.txt`? Czy kolejność nazw w `add_executable` decyduje o kolejności wykonywania?
6. `points.cpp` leży w katalogu projektu. Dlaczego to nie wystarcza, żeby był częścią programu?
7. Co robi kompilator, a co linker, gdy budujesz demonstrację? Ile powstaje plików obiektowych?
8. Po czym poznać, że błąd z punktu 8 to błąd linkowania? Dlaczego wystarczyła naprawa `CMakeLists.txt`?
9. Dlaczego nie dołączamy `points.cpp` do `main.cpp` przez `#include "points.cpp"`?
10. Program z dwóch plików wypisuje dla `4 2` to samo co program z jednego pliku. Dlaczego? I co trzeba by zrobić, gdyby `calculate_points` wywoływał też trzeci plik `.cpp`?

<details>
<summary>Przykładowe odpowiedzi</summary>

1. W `main.cpp` są `#include <iostream>`, deklaracja `calculate_points` i `main` z odczytem, wywołaniem i wypisaniem wyniku. W `points.cpp` jest tylko definicja funkcji. Nie ma w nim `main`, bo program ma jedno `main`, ani odczytu i wypisywania, bo to zadania `main`. Nie ma też `#include <iostream>`, bo funkcja z niego nie korzysta.
2. Bo kompilator kompiluje `main.cpp` osobno i nie zagląda do `points.cpp`. W miejscu wywołania musi znać nazwę, typ wyniku i typy parametrów, a podaje mu je deklaracja. Bez niej kompilacja `main.cpp` zakończyłaby się błędem `use of undeclared identifier`.
3. Ciało funkcji, czyli instrukcje obliczenia. Wykonują się przy każdym wywołaniu, gdy program działa. Deklaracja niczego nie wykonuje.
4. Nazwa funkcji, typ wyniku, liczba parametrów i ich typy w tej samej kolejności. Nazwy parametrów mogą się różnić. Kompilator, który kompiluje `main.cpp`, nie widzi definicji z `points.cpp`, więc ich nie porówna.
5. W linijce `add_executable` doszła nazwa `points.cpp`: nazwa pliku do zbudowania, a nie funkcji. Kolejność nazw nie ma znaczenia dla wykonywania, bo wykonywanie zawsze zaczyna się od `main`.
6. Bo narzędzia budują tylko pliki wymienione w `add_executable`. CMake nie przegląda katalogu w poszukiwaniu plików `.cpp`. Plik spoza listy nie jest kompilowany, więc jego definicje nie trafiają do programu.
7. Kompilator pracuje dwa razy, osobno dla każdego pliku `.cpp`, i tworzy dwa pliki obiektowe: `main.cpp.o` i `points.cpp.o` (na Windowsie `.obj`). Linker łączy oba, razem z kodem biblioteki i kodem startowym, w jeden program `first_program`. Wywołanie `calculate_points` z `main` dopasowuje do definicji z `points.cpp.o`.
8. Kompilacja `main.cpp` się udała: jest linijka `Building CXX object`, a żaden komunikat nie wskazuje błędu w linijce `main.cpp`. Wynik kończy się `linker command failed` i komunikatem z nazwą `calculate_points`. Kod C++ był poprawny, a brakowało tylko `points.cpp` na liście plików do zbudowania. Po dopisaniu go definicja trafiła do programu.
9. `#include` wstawia cały tekst pliku, więc definicja zostałaby skompilowana razem z `main.cpp`. Gdy `points.cpp` jest też w `add_executable`, definicja trafiłaby do programu dwa razy i linker zgłosiłby, że funkcja jest zdefiniowana więcej niż raz. Bez `points.cpp` w `add_executable` program byłby w praktyce znowu jednym plikiem. Pliki `.cpp` łączy linker, a ich listę podaje `add_executable`.
10. Bo `main` i funkcja zawierają te same instrukcje. Podział na pliki zmienia organizację kodu i przebieg budowania, a nie to, co program oblicza. Trzeci plik potrzebowałby własnej kopii deklaracji, a każdą kopię trzeba by poprawiać przy każdej zmianie funkcji. Na ten problem odpowiada następna lekcja.

</details>

## Podsumowanie

- Jeden program może się składać z kilku plików `.cpp`. Program ma jedno `main`.
- W pliku, który wywołuje funkcję, wystarcza deklaracja. Definicja może stać w innym pliku `.cpp`.
- Deklaracja i definicja muszą być zgodne: nazwa, typ wyniku, liczba i typy parametrów. Kompilator nie porówna ich między plikami, więc porównaj je samodzielnie.
- Narzędzia budują tylko pliki wymienione w `add_executable`. Każdy nowy plik `.cpp` dopisujesz w tej linijce. Kolejność nazw nie zmienia kolejności wykonywania.
- Każdy plik `.cpp` jest kompilowany osobno, do własnego pliku obiektowego. Linker łączy pliki obiektowe w jeden program.
- Plik z definicją, którego nie ma w `add_executable`, daje błąd linkowania. Naprawia go dopisanie pliku w `CMakeLists.txt`, bez zmian w kodzie C++.
- Plików `.cpp` nie dołącza się przez `#include`.

## Co dalej

W tej lekcji deklaracja `calculate_points` stała w `main.cpp`. Co jednak, jeśli z tej samej funkcji mają korzystać różne pliki? Każdy potrzebowałby wtedy własnej kopii deklaracji, a przy każdej zmianie funkcji trzeba by poprawić wszystkie kopie. W następnej lekcji Modułu 11 deklaracja trafi do jednego wspólnego miejsca: własnego pliku nagłówkowego. Przejdź do [lekcji 11.2: Własny plik nagłówkowy](lesson_02_own_header_file.md).

---

## Przykładowe rozwiązania

Zajrzyj tutaj **po własnej próbie**. Twoje nazwy funkcji, parametrów i drugiego pliku mogą się różnić, jeśli standardowe wyjście jest takie, jak wymagane.

<details>
<summary>Punkt 7: misja, koszt biletów</summary>

**`main.cpp`**:

<!-- example: tickets -->
```cpp
#include <iostream>

int total_cost(int regular_tickets, int reduced_tickets);

int main() {
    int regular_tickets{0};
    int reduced_tickets{0};

    std::cin >> regular_tickets;
    std::cin >> reduced_tickets;

    std::cout << "Total cost: " << total_cost(regular_tickets, reduced_tickets) << "\n";
}
```

**`tickets.cpp`**, obok `main.cpp`:

<!-- file: tickets tickets.cpp -->
```cpp
int total_cost(int regular_tickets, int reduced_tickets) {
    const int regular_price{12};
    const int reduced_price{7};
    return regular_tickets * regular_price + reduced_tickets * reduced_price;
}
```

**`CMakeLists.txt`**:

<!-- cmake: tickets -->
```cmake
cmake_minimum_required(VERSION 3.28)
project(first_program LANGUAGES CXX)

add_executable(first_program main.cpp tickets.cpp)
target_compile_features(first_program PRIVATE cxx_std_20)
set_target_properties(first_program PROPERTIES CXX_EXTENSIONS OFF)
```

| Dane | Standardowe wyjście | Co sprawdza |
|---|---|---|
| A: `2 3` | `Total cost: 45` | oba rodzaje biletów |
| B: `0 4` | `Total cost: 28` | bez biletów zwykłych |
| C: `0 0` | `Total cost: 0` | bez żadnych biletów |
| D: `3 0` | `Total cost: 36` | same bilety zwykłe |

- **Organizacja plików:** `main.cpp` odczytuje dane, wywołuje funkcję i wypisuje wynik. `tickets.cpp` zawiera tylko definicję `total_cost`. `CMakeLists.txt` wymienia oba pliki w linijce `add_executable`, a pozostałe linijki są takie jak w lekcji 0.5.
- **Deklaracja i definicja:** deklaracja na początku `main.cpp` ma tę samą nazwę, typ wyniku i typy parametrów co definicja w `tickets.cpp`. Dzięki niej kompiluje się wywołanie w `main`.
- **Ceny są stałymi w definicji.** Należą do reguły obliczania kosztu, więc stoją w funkcji, a nie w `main`. Gdy cena się zmieni, zmieniasz tylko `tickets.cpp`.
- **Kompilacja i linkowanie:** kompilator tworzy dwa pliki obiektowe, `main.cpp.o` i `tickets.cpp.o`. Linker łączy je w jeden program i dopasowuje wywołanie `total_cost` do definicji.
- **Inne poprawne rozwiązania:** inne nazwy funkcji, parametrów i pliku, na przykład `ticket_cost` i `prices.cpp`; wynik zapisany najpierw w zmiennej `const int` w `main`; deklaracja bez nazw parametrów, `int total_cost(int, int);`; pliki w `add_executable` w innej kolejności.

</details>

<details>
<summary>Punkt 8: poprawiony projekt</summary>

W porównaniu z błędnym projektem zmienia się jedna linijka `CMakeLists.txt`: `add_executable(first_program main.cpp)` staje się `add_executable(first_program main.cpp points.cpp)`.

**`CMakeLists.txt`**:

<!-- cmake: points_link_fixed -->
```cmake
cmake_minimum_required(VERSION 3.28)
project(first_program LANGUAGES CXX)

add_executable(first_program main.cpp points.cpp)
target_compile_features(first_program PRIVATE cxx_std_20)
set_target_properties(first_program PROPERTIES CXX_EXTENSIONS OFF)
```

**`main.cpp`**, bez zmian:

<!-- example: points_link_fixed -->
```cpp
#include <iostream>

int calculate_points(int solved, int bonus);

int main() {
    int solved{0};
    int bonus{0};

    std::cin >> solved;
    std::cin >> bonus;

    std::cout << "Points: " << calculate_points(solved, bonus) << "\n";
}
```

**`points.cpp`**, bez zmian:

<!-- file: points_link_fixed points.cpp -->
```cpp
int calculate_points(int solved, int bonus) {
    const int points_per_task{3};
    return solved * points_per_task + bonus;
}
```

Dla tych samych danych co w punkcie 5:

<!-- input: points_link_fixed -->
```text
4 2
```

<!-- output: points_link_fixed -->
```text
Points: 14
```

Kompilacja i linkowanie udają się: `points.cpp` jest teraz na liście plików do zbudowania, więc jego definicja trafia do programu.

</details>

**Poprzednia lekcja:** [Lekcja 10.5: Zapisy na warsztaty (sprawdzian Modułu 10)](../module_10_input_records/lesson_05_workshop_registrations.md) · **Następna lekcja:** [Lekcja 11.2: Własny plik nagłówkowy](lesson_02_own_header_file.md) · [Opis kursu](../../README.md)

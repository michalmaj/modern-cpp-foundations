# Lekcja 1.4: Od kodu źródłowego do programu wykonywalnego

**Polski** · [English](lesson_04_from_source_code_to_an_executable.en.md) · [Opis kursu](../../README.md)

> **Moduł 1, lekcja 4** · około 75 minut
> **Potrzebujesz:** katalogu `cpp-workspace`, oryginalnego projektu `lesson_05_first_program` i poleceń terminala z [lekcji 0.6](../module_00_tooling/lesson_06_same_program_without_clion.md).
> **Wersja pilotażowa:** polecenia terminala w tej lekcji sprawdzamy automatycznie na Windowsie, Ubuntu i macOS. Kroki w CLionie opisujemy według dokumentacji CLion 2026.2.

## Zanim zaczniesz

Ta lekcja zakłada, że:

- umiesz w terminalu przejść do katalogu, skonfigurować i zbudować projekt przez CMake oraz uruchomić program (lekcja 0.6);
- czytasz komunikaty kompilatora metodą z lekcji 1.2;
- wiesz, że `main` to funkcja, od której zaczyna się wykonywanie programu (lekcja 1.3).

## Sytuacja

Wiele razy klikano już **Build** i wpisywano `cmake --build`, a potem pojawiał się program. Co dzieje się po drodze? Dziś wykonasz te kroki ręcznie, zobaczysz, na którym z nich powstają różne rodzaje błędów, i przeczytasz plik `CMakeLists.txt`, który opisuje projekt.

Najważniejsza umiejętność tej lekcji: **gdy budowanie się nie udaje, rozpoznać, na którym etapie, i na tej podstawie szukać przyczyny.** Komunikatów nie trzeba zapamiętywać.

Po tej lekcji będziesz:

- wyjaśniać drogę od kodu źródłowego do programu: preprocesor i kompilacja, plik obiektowy, linkowanie, plik wykonywalny;
- kompilować i linkować program w dwóch osobnych krokach i odróżniać plik obiektowy od pliku wykonywalnego;
- rozpoznawać, czy budowanie zatrzymało się na kompilacji, na linkowaniu, czy już na konfiguracji CMake;
- wyjaśniać, co robią CMake i Ninja oraz co mówi każda linijka `CMakeLists.txt`;
- zmieniać nazwę programu w `CMakeLists.txt`.

## 1. Przygotuj kopię i terminal

1. W `cpp-workspace` utwórz katalog `lesson_1_4` i skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program`.
2. Otwórz terminal i przejdź do `cpp-workspace/lesson_1_4`, tak jak w lekcji 0.6 (`cd` i ścieżka w cudzysłowie). Sprawdź `ls` (na macOS i Ubuntu `ls -F`): są tylko dwa pliki.

Plik `main.cpp` to znany program:

<!-- example: original source=../module_00_tooling/lesson_05_first_program/main.cpp -->
```cpp
#include <iostream>

int main() {
    std::cout << "Hello! My first C++20 program works.\n";
}
```

<!-- output: original -->
```text
Hello! My first C++20 program works.
```

Kod możesz zmieniać w CLionie (otwórz w nim ten katalog) albo w innym edytorze tekstu, który zapisuje zwykły tekst. Budować i uruchamiać będziesz w terminalu.

## 2. Od kodu do programu

Budowanie programu to kilka kroków:

```text
main.cpp  ──►  preprocesor i kompilacja  ──►  main.o  ──►  linkowanie  ──►  program
(kod źródłowy)                            (plik obiektowy)              (plik wykonywalny)
```

- **Kod źródłowy** (`main.cpp`) to tekst programu w C++. Piszą go ludzie, czyta go kompilator.
- **Preprocesor** to pierwszy krok kompilacji. Obsługuje linijki zaczynające się od `#`. Na przykład `#include <iostream>` wstawia deklaracje z biblioteki standardowej, między innymi `std::cout`. Robi to, zanim zacznie się właściwa kompilacja (lekcja 1.2).
- **Kompilacja** sprawdza C++ w **tym jednym pliku** i tłumaczy go na kod maszynowy, czyli instrukcje dla procesora. Wszystkie błędy z lekcji 1.2 i 1.3 pochodziły właśnie stąd. Wynikiem jest **plik obiektowy**, na przykład `main.o`.
- **Plik obiektowy to jeszcze nie program.** Brakuje w nim dwóch rzeczy:
  - gotowego kodu biblioteki standardowej, który naprawdę wypisuje tekst. `#include` dało kompilatorowi tylko deklarację `std::cout`, czyli informację, że coś takiego istnieje;
  - **kodu startowego**: krótkiego fragmentu, który ma każdy program. Przygotowuje on działanie programu i wywołuje Twoją funkcję `main`.
- **Linkowanie** wykonuje **linker**. Łączy plik obiektowy z kodem biblioteki standardowej i z kodem startowym w jeden **plik wykonywalny**. Sprawdza przy tym, czy wszystko, czego program potrzebuje, naprawdę istnieje.

**Kto to wszystko robi?** Wpisujesz jedno polecenie, `clang++`, ale `clang++` to także **sterownik** (ang. *driver*): uruchamia za Ciebie właściwe narzędzia. Do kompilacji używa kompilatora Clang, a do linkowania uruchamia linker Twojego systemu: na Ubuntu i macOS program `ld` (to dwa różne linkery o tej samej nazwie), a na Windowsie `lld-link`. W lekcji 0.6 jedno polecenie `clang++ … -o …` wykonało oba etapy naraz. Dziś je rozdzielisz.

## 3. Eksperyment A: dwa etapy budowania

### Krok 1: tylko kompilacja

**Przewidź:** jakie nowe pliki pojawią się w katalogu? Czy powstanie program, który da się uruchomić?

| System | Polecenie |
|---|---|
| Windows | `clang++ -std=c++20 -c main.cpp` |
| macOS | `/opt/homebrew/opt/llvm@22/bin/clang++ -std=c++20 -c main.cpp` |
| Ubuntu | `clang++-22 -std=c++20 -c main.cpp` |

`-c` znaczy „tylko kompiluj”. Na macOS z procesorem Intel zamiast `/opt/homebrew/opt/llvm@22` wpisz `/usr/local/opt/llvm@22`, jak w lekcji 0.6.

Polecenie nic nie wypisze. Sprawdź `ls` (na macOS i Ubuntu `ls -F`). Pojawił się plik **`main.o`**, na wszystkich trzech systemach pod tą samą nazwą. To plik obiektowy. Programu jeszcze nie ma i nie próbuj uruchamiać `main.o`: to nie jest program.

### Krok 2: linkowanie

**Przewidź:** co powstanie teraz? Co wypisze program?

| System | Linkowanie | Uruchomienie |
|---|---|---|
| Windows | `clang++ main.o -o hello.exe` | `.\hello.exe` |
| macOS | `/opt/homebrew/opt/llvm@22/bin/clang++ main.o -o hello` | `./hello` |
| Ubuntu | `clang++-22 main.o -o hello` | `./hello` |

To polecenie dostaje plik obiektowy, a nie `main.cpp`. `clang++` wie więc, że kompilacja jest już zrobiona, i uruchamia tylko linker. Dlatego nie ma tu `-std=c++20`: nie ma już czego kompilować.

Powstał plik wykonywalny `hello` (na Windowsie `hello.exe`), który wypisuje znany komunikat.

### To samo w CMake

Te same dwa etapy wykonuje za Ciebie CMake z Ninja. W wyniku `cmake --build` (lekcja 0.6) i w oknie Build w CLionie widać je było jako dwie linijki:

```text
Building CXX object CMakeFiles/first_program.dir/main.cpp.o
Linking CXX executable first_program
```

`Building CXX object` to kompilacja, a `Linking CXX executable` to linkowanie. Nazwy plików wybiera narzędzie: CMake nazywa plik obiektowy `main.cpp.o`, a na Windowsie `main.cpp.obj`. Sam `clang++` nazwał go `main.o`. Numery w nawiasach, na przykład `[3/4]`, zależą od projektu i wersji narzędzi, więc nie warto się do nich przywiązywać.

## 4. Eksperyment B: pierwszy błąd linkowania

Tym razem mniej podpowiedzi. Zastąp zawartość `main.cpp` tym kodem: `main` zmieniło się w `mian`, a na końcu jest `return 0;`.

<!-- broken: mian stage=link error=undefined reference to .main'|undefined symbol: main\b|"_main", referenced from -->
```cpp
#include <iostream>

int mian() {
    std::cout << "Hello! My first C++20 program works.\n";
    return 0;
}
```

**Przewidź:** czy krok 1 (kompilacja) się uda? A krok 2 (linkowanie)? Potem wykonaj oba kroki tymi samymi poleceniami co w eksperymencie A.

Kompilacja przechodzi bez żadnego komunikatu i znów powstaje `main.o`. Linkowanie się nie udaje. Wynik zależy od systemu:

**Ubuntu:**

```text
/usr/bin/ld: /lib/x86_64-linux-gnu/Scrt1.o: in function `_start':
(.text+0x1b): undefined reference to `main'
clang++-22: error: linker command failed with exit code 1 (use -v to see invocation)
```

**macOS:**

```text
Undefined symbols for architecture arm64:
  "_main", referenced from:
      <initial-undefines>
ld: symbol(s) not found for architecture arm64
clang++: error: linker command failed with exit code 1 (use -v to see invocation)
```

**Windows:**

```text
lld-link: error: subsystem must be defined
clang++: error: linker command failed with exit code 1 (use -v to see invocation)
```

**Nie zapamiętuj tych komunikatów.** Odpowiedz na pytania, a potem sprawdź.

**1.** Na którym etapie zatrzymało się budowanie? Po czym to poznajesz?

<details>
<summary>Odpowiedź</summary>

Na linkowaniu. Kompilacja się udała, bo powstał `main.o` i nie było komunikatu. Nie udał się krok 2, a na wszystkich systemach ostatnia linijka mówi `linker command failed`. Żaden komunikat nie wskazuje linijki w `main.cpp` (`main.cpp:4:5` i podobnych), bo linker nie czyta kodu źródłowego: dostaje gotowy plik obiektowy.

</details>

**2.** Dlaczego kompilator nie zgłosił błędu?

<details>
<summary>Odpowiedź</summary>

Bo `mian` to poprawna nazwa funkcji w C++. Kompilator sprawdza tylko, czy ten jeden plik jest poprawnym C++. Nie wie, że ten plik ma być całym programem i że brakuje w nim `main`.

</details>

**3.** Kto potrzebuje funkcji `main`?

<details>
<summary>Odpowiedź</summary>

Kod startowy, który linker dołącza do każdego programu: to on wywołuje `main`. Na Ubuntu widać, że szuka jej `_start`, a na macOS linker wymienia brakujące `_main` (nazwa z dodatkowym `_`, to normalne na tym systemie). Na Windowsie `lld-link` po samej funkcji `main` rozpoznaje rodzaj programu (program do terminala), więc bez niej pisze, że ten rodzaj (*subsystem*) nie jest określony. Komunikaty są różne, ale przyczyna ta sama: nie ma `main`.

</details>

**Zauważ jeszcze jedno:** program `hello` z eksperymentu A zniknął. `clang++` usuwa plik, którego nie udało się zbudować, żeby nie został po nim niedokończony program. Gdy nie uda się sama kompilacja, linkowanie w ogóle się nie zaczyna, a stary program zostaje (lekcja 1.2).

**Napraw:** zmień `mian` z powrotem na `main`, wykonaj oba kroki jeszcze raz i uruchom program.

<!-- example: main_with_return -->
```cpp
#include <iostream>

int main() {
    std::cout << "Hello! My first C++20 program works.\n";
    return 0;
}
```

<!-- output: main_with_return -->
```text
Hello! My first C++20 program works.
```

### Błąd kompilacji a błąd linkowania

| | Brakujący średnik (lekcja 1.2) | `mian` zamiast `main` |
|---|---|---|
| Etap | kompilacja | linkowanie |
| Plik obiektowy | nie powstaje | powstaje |
| Kto zgłasza | kompilator | linker (przez `clang++`) |
| Miejsce w komunikacie | `main.cpp:linijka:pozycja` | brak linijki w `main.cpp`; nazwa tego, czego brakuje |
| Co jest nie tak | kod nie jest poprawnym C++ | kod jest poprawny, ale brakuje części potrzebnej do zbudowania programu |

Pusty `main.cpp`, przed którego budowaniem ostrzegała lekcja 1.3, daje ten sam rodzaj błędu: pusty plik kompiluje się bez problemu, ale nie ma w nim `main`.

## 5. CMake, Ninja i `CMakeLists.txt`

Gdy budujesz przez CMake, nie musisz pamiętać poleceń z eksperymentów A i B:

- **CMake** (konfiguracja, `cmake -S . -B …`) czyta `CMakeLists.txt`, sprawdza kompilator i zapisuje **plan budowania**: jakie polecenia trzeba wykonać i w jakiej kolejności;
- **Ninja** (budowanie, `cmake --build …`) wykonuje ten plan: uruchamia `clang++` do kompilacji, a potem do linkowania. Ponownie robi tylko to, co trzeba, na przykład po zmianie `main.cpp`.

To dwa różne zadania: CMake planuje, Ninja wykonuje.

### Co mówi `CMakeLists.txt`

```cmake
cmake_minimum_required(VERSION 3.28)
project(first_program LANGUAGES CXX)

add_executable(first_program main.cpp)
target_compile_features(first_program PRIVATE cxx_std_20)
set_target_properties(first_program PROPERTIES CXX_EXTENSIONS OFF)
```

| Linijka | Co mówi narzędziom |
|---|---|
| `cmake_minimum_required(VERSION 3.28)` | Ten projekt wymaga CMake 3.28 lub nowszego. Starszy CMake zatrzyma się z komunikatem o wymaganej wersji. |
| `project(first_program LANGUAGES CXX)` | Nazwa całego **projektu** i jego język: `CXX` to w CMake nazwa C++. Tu CMake szuka kompilatora C++ i sprawdza, czy działa. |
| `add_executable(first_program main.cpp)` | Zbuduj **program wykonywalny** o nazwie `first_program` z pliku `main.cpp`. W CMake taki program nazywa się **targetem** (ang. *target*, cel budowania). |
| `target_compile_features(first_program PRIVATE cxx_std_20)` | Kompiluj ten program jako C++20. Dlatego w poleceniach widać `-std=c++20`. `PRIVATE` na razie pomiń. |
| `set_target_properties(first_program PROPERTIES CXX_EXTENSIONS OFF)` | Używaj samego standardowego C++20, bez dodatków konkretnego kompilatora. |

Nazwa projektu i nazwa programu są tu takie same (`first_program`), ale to dwie różne rzeczy: projekt to całość, a target to jeden program w nim.

**Debug i Release** znasz z lekcji 0.5. Tej konfiguracji nie zapisuje się w `CMakeLists.txt`: wybierasz ją przy konfiguracji (`-DCMAKE_BUILD_TYPE=Debug`) albo w profilu CMake w CLionie. W kursie na razie zawsze używamy Debug.

### Eksperyment C: zmień nazwę programu

1. Przywróć oryginalny `main.cpp`: skopiuj go jeszcze raz z `lesson_05_first_program` i zastąp nim plik w `lesson_1_4`.
2. Skonfiguruj i zbuduj projekt w terminalu poleceniami z lekcji 0.6, w katalogu `build-terminal`, i uruchom program:

   | System | Konfiguracja |
   |---|---|
   | Windows | `cmake -S . -B build-terminal -G Ninja -DCMAKE_BUILD_TYPE=Debug "-DCMAKE_CXX_COMPILER=C:\Program Files\LLVM\bin\clang++.exe"` |
   | macOS | `cmake -S . -B build-terminal -G Ninja -DCMAKE_BUILD_TYPE=Debug -DCMAKE_CXX_COMPILER=/opt/homebrew/opt/llvm@22/bin/clang++` |
   | Ubuntu | `cmake -S . -B build-terminal -G Ninja -DCMAKE_BUILD_TYPE=Debug -DCMAKE_CXX_COMPILER=/usr/bin/clang++-22` |

   Potem `cmake --build build-terminal` i `.\build-terminal\first_program.exe` (macOS i Ubuntu: `./build-terminal/first_program`).
3. W `CMakeLists.txt` zamień `first_program` na `hello_cmake` w **trzech** linijkach: `add_executable`, `target_compile_features` i `set_target_properties`. Linijkę `project(…)` zostaw bez zmian. Zapisz plik.

**Przewidź:** co pojawi się w `build-terminal` po ponownym budowaniu? Czy zniknie `first_program`?

4. Zbuduj ponownie: `cmake --build build-terminal`. Nie musisz sam konfigurować: Ninja zauważy zmianę w `CMakeLists.txt` i najpierw sam uruchomi CMake. Zobaczysz to jako `Re-running CMake...` na początku wyniku. Potem kompilacja i `Linking CXX executable hello_cmake`.
5. Sprawdź `ls build-terminal` (na macOS i Ubuntu `ls -F build-terminal`) i uruchom nowy program: `.\build-terminal\hello_cmake.exe` (macOS i Ubuntu: `./build-terminal/hello_cmake`).

<details>
<summary>Co się stało</summary>

W `build-terminal` są teraz **oba** programy: nowy `hello_cmake` i stary `first_program`. Nazwę programu ustala `add_executable`, więc powstał nowy plik. Starego nikt nie usunął: CMake i Ninja dbają o to, co mają zbudować, i nie sprzątają plików, które powstały wcześniej. Tak jak w lekcji 0.5: każdy plik wykonywalny jest osobnym plikiem.

</details>

**Wróć do pierwotnej wersji.** Najbezpieczniej skopiować jeszcze raz `CMakeLists.txt` z oryginalnego `lesson_05_first_program` i zastąpić nim zmieniony plik. Potem `cmake --build build-terminal`. Plik `hello_cmake` zostanie w `build-terminal`, dopóki go nie usuniesz. Możesz też usunąć cały katalog `build-terminal`: to wynik budowania, a następna konfiguracja utworzy go od nowa.

## 6. Misja: Który etap protestuje?

Ktoś z zespołu zgłasza cztery problemy. W każdym przypadku zmieniono **jedną rzecz** w działającym projekcie. Twoje zadanie: ustalić, na którym etapie coś jest nie tak, i to naprawić.

**Przygotuj projekt:**

1. W `cpp-workspace` utwórz `build_detective` i skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program`.
2. Zastąp zawartość `main.cpp` działającą wersją:

<!-- example: mission -->
```cpp
#include <iostream>

int main() {
    std::cout << "Build: OK\n";
    std::cout << "Run: OK\n";
    return 0;
}
```

3. Skonfiguruj `build-terminal` jak w eksperymencie C, zbuduj i uruchom program. Oczekiwany wynik:

<!-- output: mission -->
```text
Build: OK
Run: OK
```

**Zgłoszenia.** Zawsze zaczynaj od działającej wersji powyżej: przed każdym zgłoszeniem przywróć ją (w `main.cpp` i, przy zgłoszeniu C, w `CMakeLists.txt`). Potem wprowadź opisaną zmianę.

**Zgłoszenie A.** `main.cpp` wygląda tak:

<!-- broken: mission_main stage=link error=undefined reference to .main'|undefined symbol: main\b|"_main", referenced from -->
```cpp
#include <iostream>

int Main() {
    std::cout << "Build: OK\n";
    std::cout << "Run: OK\n";
    return 0;
}
```

**Zgłoszenie B.** `main.cpp` wygląda tak:

<!-- example: mission_newline -->
```cpp
#include <iostream>

int main() {
    std::cout << "Build: OK";
    std::cout << "Run: OK\n";
    return 0;
}
```

**Zgłoszenie C.** `main.cpp` jest działający, ale w `CMakeLists.txt` jedna linijka wygląda tak:

```cmake
add_executable(first_program program.cpp)
```

**Zgłoszenie D.** `main.cpp` wygląda tak:

<!-- broken: mission_quote at=4:18 errors=1 error=^expected expression$ -->
```cpp
#include <iostream>

int main() {
    std::cout << "Build: OK\n;
    std::cout << "Run: OK\n";
    return 0;
}
```

**Dla każdego zgłoszenia:**

1. **Przewidź**, zanim cokolwiek uruchomisz: czy budowanie się uda? A uruchomienie?
2. Zbuduj (`cmake --build build-terminal`) i, jeśli się da, uruchom program.
3. Ustal **etap**: konfiguracja (CMake), kompilacja, linkowanie, czy działanie programu (buduje się, ale wynik jest zły).
4. Znajdź **pierwszą istotną informację** i ją przepisz.
5. Zapisz **przyczynę**, popraw **jedną rzecz** i sprawdź wynik.

Zapisuj wyniki w tabeli, na przykład w notatkach:

| Zgłoszenie | Przewidywanie | Etap | Pierwsza istotna informacja | Przyczyna | Poprawka | Wynik |
|---|---|---|---|---|---|---|
| A | | | | | | |
| B | | | | | | |
| C | | | | | | |
| D | | | | | | |

### Kryterium sukcesu

- Każde zgłoszenie ma przypisany właściwy etap i **cytat z wyniku narzędzi**, który to potwierdza. Przy zgłoszeniu, w którym nikt nie zgłasza błędu, dowodem jest wynik programu.
- Każde zgłoszenie naprawiono jedną zmianą, a po naprawie program buduje się i wypisuje oczekiwane dwie linijki.
- Przy każdym zgłoszeniu umiesz w jednym zdaniu powiedzieć, **dlaczego** problem zatrzymał budowanie właśnie na tym etapie, albo dlaczego żaden etap go nie zatrzymał.

<details>
<summary>Podpowiedź 1</summary>

Zanim przeczytasz komunikaty, odpowiedz na dwa pytania: czy powstał plik obiektowy? Czy powstał program? Odpowiedzi często wskazują etap.

</details>

<details>
<summary>Podpowiedź 2</summary>

Sprawdź, kto pisze pierwszy komunikat: CMake (`CMake Error`), kompilator (`main.cpp:` z numerem linijki) czy linker (`linker command failed`)? A może nikt nic nie pisze, a mimo to coś jest nie tak? Pierwszą istotną informacją bywa też `warning`.

</details>

Przykładowe rozwiązanie jest w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 7. Gdy coś pójdzie inaczej

| Co widzisz | Co to znaczy | Co zrobić |
|---|---|---|
| Po `clang++ -c` nie ma pliku `main.o` | Kompilacja się nie udała albo terminal jest w innym katalogu. | Przeczytaj komunikaty kompilatora (lekcja 1.2). Sprawdź `pwd` i `ls`. |
| `no such file or directory: 'main.o'` albo podobny komunikat przy linkowaniu | Nie ma pliku obiektowego do połączenia. | Najpierw wykonaj krok 1, w tym samym katalogu. |
| macOS: polecenie `clang++` działa, ale to kompilator Apple | Samo `clang++` to na macOS kompilator Apple (lekcja 0.4). | Użyj pełnej ścieżki z tabeli. |
| `linker command failed` | Kompilacja się udała, nie udało się linkowanie. | Sprawdź, czego brakuje: często `main` z literówką albo inną wielkością liter. |
| `CMake Error at CMakeLists.txt:…` | Problem jest w opisie projektu, a nie w kodzie C++. Kompilator jeszcze nie ruszył. | Przeczytaj, której linijki `CMakeLists.txt` dotyczy błąd. Najbezpieczniej przywróć oryginalny plik i wprowadź zmianę jeszcze raz. |
| Po zmianie nazwy programu uruchamia się stary program | Stary plik wykonywalny został w `build-terminal`. | Uruchom program o nowej nazwie albo usuń `build-terminal` i skonfiguruj od nowa. |
| CLion po zmianie `CMakeLists.txt` pokazuje komunikaty w oknie CMake | CLion też czyta `CMakeLists.txt` i wczytuje projekt ponownie. | Ta lekcja buduje w terminalu. W CLionie możesz tylko edytować pliki. |

## 8. Wyjaśnij

Odpowiedz własnymi słowami, najlepiej na piśmie. Dopiero potem porównaj z przykładową odpowiedzią.

**1.** Czym różni się plik obiektowy od pliku wykonywalnego?

<details>
<summary>Przykładowa odpowiedź</summary>

Plik obiektowy to skompilowany kod jednego pliku źródłowego, bez kodu biblioteki standardowej i bez kodu startowego, więc nie da się go uruchomić. Plik wykonywalny powstaje z niego przez linkowanie: to kompletny program.

</details>

**2.** Dlaczego program z `mian` daje się skompilować, ale nie zlinkować?

<details>
<summary>Przykładowa odpowiedź</summary>

Kompilator sprawdza tylko, czy kod jest poprawnym C++, a `mian` to poprawna nazwa funkcji. Dopiero linker, budując cały program, szuka `main`, którą wywołuje kod startowy, i jej nie znajduje.

</details>

**3.** Po czym w wyniku budowania poznasz, że problem zgłosił linker, a nie kompilator?

<details>
<summary>Przykładowa odpowiedź</summary>

Kompilacja się udała, bo powstał plik obiektowy. W wyniku jest `linker command failed`, a komunikaty nie wskazują linijki w `main.cpp`, tylko nazwę czegoś, czego brakuje.

</details>

**4.** Co robi CMake, a co Ninja?

<details>
<summary>Przykładowa odpowiedź</summary>

CMake czyta `CMakeLists.txt` i przygotowuje plan budowania. Ninja wykonuje ten plan: uruchamia `clang++` do kompilacji i do linkowania, i tylko wtedy, gdy coś się zmieniło.

</details>

**5.** Dlaczego po zmianie nazwy programu w `CMakeLists.txt` stary program został w `build-terminal`?

<details>
<summary>Przykładowa odpowiedź</summary>

Bo zmiana nazwy w `add_executable` mówi narzędziom, co zbudować od teraz. Nie każe usuwać plików, które powstały wcześniej. Stary plik wykonywalny zostaje, dopóki go nie usuniesz.

</details>

## Podsumowanie

- Droga od kodu do programu: **kod źródłowy → preprocesor i kompilacja → plik obiektowy → linkowanie → program wykonywalny**.
- Kompilacja sprawdza C++ jednego pliku. Linkowanie łączy plik obiektowy z kodem biblioteki standardowej i kodem startowym i sprawdza, czy niczego nie brakuje, na przykład `main`.
- `clang++` jest też sterownikiem: z `-c` tylko kompiluje, a dla pliku obiektowego uruchamia linker.
- Etap błędu poznasz po dowodach: `CMake Error` (konfiguracja), `main.cpp:linijka:pozycja` (kompilacja), `linker command failed` (linkowanie), zły wynik bez komunikatu (działanie programu). Komunikaty linkerów różnią się między systemami. Liczy się etap i przyczyna, nie dokładne słowa.
- CMake planuje budowanie na podstawie `CMakeLists.txt`, a Ninja wykonuje plan. `add_executable` ustala nazwę programu i plik źródłowy.

## Co dalej

Po czterech lekcjach Modułu 1 potrafisz napisać mały program, poprawić błędy i wiesz, jak powstaje plik wykonywalny. **Lekcja 1.5 jest w przygotowaniu.**

---

## Przykładowe rozwiązania

Zajrzyj tutaj **po własnej próbie**. Twoje cytaty mogą wyglądać inaczej na Twoim systemie. Liczy się to, czy wskazują ten sam etap.

<details>
<summary>Misja: przykładowa tabela</summary>

| Zgłoszenie | Przewidywanie | Etap | Pierwsza istotna informacja | Przyczyna | Poprawka | Wynik |
|---|---|---|---|---|---|---|
| A | Skompiluje się, nie zlinkuje. | linkowanie | Ubuntu: ``undefined reference to `main'``; macOS: `"_main", referenced from`; Windows: `undefined symbol: main`. Na każdym: `linker command failed`. | `Main` to inna nazwa niż `main`: wielkość liter ma znaczenie. Kod startowy nie znajduje `main`. | `Main` → `main` | Buduje się, wynik poprawny. |
| B | Zbuduje się i uruchomi. | działanie programu | Nikt nie zgłasza błędu. Program wypisuje `Build: OKRun: OK` w jednej linijce. | W pierwszym napisie brakuje `\n`. | Dopisać `\n` | Dwie linijki, jak oczekiwano. |
| C | Nie zbuduje się. | konfiguracja (CMake) | `CMake Error at CMakeLists.txt:4 (add_executable):` `Cannot find source file:` `program.cpp` | `CMakeLists.txt` wskazuje plik, którego nie ma. Kompilator nawet nie ruszył. | `program.cpp` → `main.cpp` | Buduje się, wynik poprawny. |
| D | Nie skompiluje się. | kompilacja | `main.cpp:4:18: warning: missing terminating '"' character`, a zaraz potem `main.cpp:4:18: error: expected expression` | Napis w linijce 4 nie ma cudzysłowu zamykającego. Ostrzeżenie mówi o przyczynie dokładniej niż sam błąd. | Dopisać `"` przed `;` | Buduje się, wynik poprawny. |

- **Zgłoszenie A przez CMake:** na Windowsie komunikat brzmi `undefined symbol: main`, a nie `subsystem must be defined` jak w eksperymencie B. CMake sam mówi linkerowi, że to program do terminala. Inny komunikat, ten sam etap i ta sama przyczyna.
- **Zgłoszenie C:** zgłasza je `cmake --build`, bo Ninja widzi zmianę w `CMakeLists.txt` i najpierw uruchamia CMake. Pierwsza linijka to `Re-running CMake...`, a dalej są komunikaty `CMake Error`.

Wynik programu w zgłoszeniu B:

<!-- output: mission_newline -->
```text
Build: OKRun: OK
```

</details>

**Poprzednia lekcja:** [Lekcja 1.3: Program od pustej kartki](lesson_03_a_program_from_a_blank_page.md) · **Następna lekcja:** w przygotowaniu · [Opis kursu](../../README.md)

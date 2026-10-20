# Lekcja 0.5: Twój pierwszy działający program w CLionie

**Polski** · [English](lesson_05_first_program_in_clion.en.md) · [Opis kursu](../../README.md)

> **Moduł 0, lekcja 5** · około 45–60 minut
> **Potrzebujesz:** narzędzi zainstalowanych w [lekcji 0.4](lesson_04_installing_the_tools.md) i dostępu do internetu, żeby pobrać projekt.
> **Wersja pilotażowa:** kroki w CLionie opisujemy według dokumentacji CLion 2026.2. W Twojej wersji nazwy przycisków mogą się nieznacznie różnić.

## Zanim zaczniesz

Ta lekcja zakłada, że:

- umiesz otworzyć terminal, poruszać się po katalogach i uruchomić program, podając jego ścieżkę (lekcje 0.1–0.3);
- wiesz, że **kompilator** zamienia kod źródłowy w plik wykonywalny (lekcja 0.3);
- masz zainstalowane LLVM 22, CMake, Ninja i CLion, a w terminalu sprawdzono ich wersje (lekcja 0.4).

## Sytuacja

Warsztat jest gotowy. Teraz zobaczysz go w działaniu: weźmiesz gotowy plik z kodem źródłowym w C++, zamienisz go w program i uruchomisz.

**Nie musisz jeszcze rozumieć kodu.** Znaczenie każdej linijki poznasz w Module 1. Dziś liczy się droga od pliku do działającego programu.

Po tej lekcji będziesz:

- wskazywać w CLionie właściwy zestaw narzędzi (toolchain) i sprawdzać, którego kompilatora używa projekt;
- otwierać gotowy projekt i rozpoznawać pliki `main.cpp` i `CMakeLists.txt`;
- budować program w konfiguracji Debug i uruchamiać go w CLionie;
- odróżniać edytowanie kodu, budowanie i uruchamianie;
- wyjaśniać, dlaczego zapisanie zmian w kodzie nie zmienia już zbudowanego programu.

## 1. Zrozum: edytowanie, budowanie, uruchamianie

Praca z programem to trzy różne czynności:

1. **Edytowanie:** zmieniasz tekst w pliku z kodem źródłowym, tutaj `main.cpp`.
2. **Budowanie:** narzędzia zamieniają kod źródłowy w **plik wykonywalny**. CMake przygotowuje plan, Ninja go wykonuje, a kompilator `clang++` robi właściwą zamianę.
3. **Uruchamianie:** komputer wykonuje gotowy plik wykonywalny, a program wypisuje wynik.

**Toolchain** to w CLionie zestaw narzędzi do budowania: kompilator, CMake i Ninja. Trzeba go wskazać, bo CLion sam może wybrać inny zestaw, na przykład dołączony do niego kompilator MinGW na Windowsie albo kompilator Apple na macOS. Program pewnie by się zbudował, ale nie naszym kompilatorem.

Program można zbudować w różnych **konfiguracjach**. **Debug** to wersja do nauki i szukania błędów; jest domyślna i użyjesz jej w tej lekcji. **Release** to wersja przygotowana do udostępnienia innym; na razie jej nie potrzebujesz.

## 2. Pobierz projekt

Projekt do tej lekcji jest w repozytorium kursu na GitHubie. Nie potrzebujesz Gita.

1. Otwórz stronę kursu: [github.com/michalmaj/modern-cpp-foundations](https://github.com/michalmaj/modern-cpp-foundations).
2. Kliknij zielony przycisk **Code**, a potem **Download ZIP**.
3. Rozpakuj pobrany plik. Na Windowsie kliknij go prawym przyciskiem myszy i wybierz **Wyodrębnij wszystkie**. Na macOS kliknij go dwukrotnie. Na Ubuntu kliknij prawym przyciskiem myszy i wybierz **Rozpakuj**.
4. W rozpakowanym katalogu `modern-cpp-foundations-main` przejdź do `course/module_00_tooling/lesson_05_first_program`. Czasem katalog `modern-cpp-foundations-main` jest w środku drugiego katalogu o tej samej nazwie; to normalne.

W katalogu `lesson_05_first_program` są dwa pliki:

| Plik | Co to jest |
|---|---|
| `main.cpp` | **Kod źródłowy** programu w C++. |
| `CMakeLists.txt` | **Opis projektu** dla CMake: z jakich plików powstaje program i że to C++20. |

Tak wygląda `main.cpp`:

```cpp
#include <iostream>

int main() {
    std::cout << "Hello! My first C++20 program works.\n";
}
```

Nie musisz rozumieć tych linijek. Zauważ tylko tekst w cudzysłowie: to komunikat, który program wypisze.

<details>
<summary>Nie możesz pobrać pliku ZIP?</summary>

Utwórz projekt w CLionie: **File | New Project**, wybierz **C++ Executable** i standard **C++20**. Potem zastąp całą zawartość dwóch wygenerowanych plików tekstem poniżej. Skopiuj go i wklej; nie przepisuj ręcznie.

`CMakeLists.txt`:

```cmake
cmake_minimum_required(VERSION 3.28)
project(first_program LANGUAGES CXX)

add_executable(first_program main.cpp)
target_compile_features(first_program PRIVATE cxx_std_20)
set_target_properties(first_program PROPERTIES CXX_EXTENSIONS OFF)
```

`main.cpp`: taki jak w przykładzie powyżej.

Zastąp oba pliki, a nie tylko `main.cpp`: plik `CMakeLists.txt` z kreatora może wymagać nowszego CMake, niż mają niektóre systemy.

</details>

## 3. Otwórz projekt w CLionie

1. Uruchom CLion. Na ekranie powitalnym kliknij **Open** (albo w otwartym już oknie wybierz **File | Open**).
2. Wskaż katalog `lesson_05_first_program` i potwierdź.
3. CLion zapyta, czy ufasz projektowi. Wybierz **Trust Project**. Projekt pochodzi z kursu, a bez zaufania CLion nie zbuduje programu.
4. Przy pierwszym otwarciu CLion pokaże okno **CMake Profiles** z profilem **Debug**. Zostaw ustawienia domyślne i zatwierdź (**OK**). Toolchain wskażesz za chwilę.

CLion wczyta projekt. Postęp zobaczysz w oknie **CMake** na dole ekranu.

## 4. Wskaż właściwy toolchain

Otwórz ustawienia: na Windowsie i Ubuntu **File | Settings**, a na macOS **CLion | Settings**. Przejdź do **Build, Execution, Deployment | Toolchains** i kliknij **+**.

### Windows

1. Wybierz **Visual Studio**.
2. W polu nazwy (**Name**) wpisz na przykład `LLVM 22`.
3. **Toolset:** CLion powinien sam znaleźć Build Tools z lekcji 0.4, zwykle w `C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools`. Jeśli pole jest puste, wskaż ten katalog.
4. **Architecture:** `amd64`.
5. **C Compiler:** `C:\Program Files\LLVM\bin\clang.exe`
6. **C++ Compiler:** `C:\Program Files\LLVM\bin\clang++.exe`
7. Pól CMake i Build Tool nie zmieniaj: CLion użyje swoich wbudowanych CMake i Ninja.

> **Wersja pilotażowa:** tej konfiguracji nie sprawdziliśmy jeszcze w CLionie na Windowsie. Jeśli CLion zgłosi, że kompilator nie pasuje do toolchainu Visual Studio, wypróbuj zamiast niego **+ → System** z tymi samymi ścieżkami kompilatorów. Do budowania i uruchamiania programu powinno to wystarczyć. Debugger, którym zajmiemy się później, może w tym wariancie wymagać innych ustawień.

### macOS

1. Wybierz **System** i wpisz nazwę, na przykład `LLVM 22`.
2. W terminalu sprawdź, gdzie Homebrew zainstalował LLVM: `brew --prefix llvm@22`. Na komputerach z procesorem Apple (M1 i nowszymi) zwykle jest to `/opt/homebrew/opt/llvm@22`, a na komputerach z procesorem Intel `/usr/local/opt/llvm@22`.
3. **C Compiler:** ta ścieżka z dopiskiem `/bin/clang`, na przykład `/opt/homebrew/opt/llvm@22/bin/clang`.
4. **C++ Compiler:** ta ścieżka z dopiskiem `/bin/clang++`, na przykład `/opt/homebrew/opt/llvm@22/bin/clang++`.

Nie wybieraj `/usr/bin/clang++`: to kompilator Apple.

### Ubuntu

1. Wybierz **System** i wpisz nazwę, na przykład `LLVM 22`.
2. **C Compiler:** `/usr/bin/clang-22`
3. **C++ Compiler:** `/usr/bin/clang++-22`

Nie wybieraj `/usr/bin/c++`, `/usr/bin/g++` ani `/usr/bin/clang++`: to inne kompilatory.

### Wszystkie systemy: użyj nowego toolchainu w profilu Debug

1. W ustawieniach przejdź do **Build, Execution, Deployment | CMake**.
2. Wybierz profil **Debug**. W polu **Toolchain** wybierz utworzony toolchain `LLVM 22`.
3. Kliknij **OK**. CLion wczyta projekt ponownie, tym razem z naszym kompilatorem.

## 5. Sprawdź, którego kompilatora używa projekt

Otwórz okno **CMake** (na dole ekranu albo **View | Tool Windows | CMake**). Znajdź dwie linijki:

```text
-- The CXX compiler identification is Clang 22.1.8
-- Check for working CXX compiler: /usr/bin/clang++-22 - skipped
```

- W pierwszej musi być **`Clang 22`**. Na Windowsie dodatkowo `with GNU-like command-line`.
- W drugiej jest ścieżka do kompilatora, którą wpisano w toolchainie (na Windowsie `C:/Program Files/LLVM/bin/clang++.exe`, na macOS ścieżka z Homebrew).

Jeśli widzisz coś innego, projekt używa niewłaściwego kompilatora:

| W pierwszej linijce widzisz | Czyj to kompilator |
|---|---|
| `GNU 15…` (Windows) | MinGW dołączony do CLiona |
| `AppleClang …` (macOS) | kompilator Apple |
| `GNU 13…` albo `Clang 18…` (Ubuntu) | systemowy GCC albo starszy Clang |
| `Clang 22… with MSVC-like command-line` (Windows) | `clang-cl` zamiast `clang++` |

Wtedy wróć do punktu 4. Potem wybierz **Tools | CMake | Reset Cache and Reload Project**, żeby CLion zapomniał poprzedni kompilator.

Sprawdź też konfigurację: na samej górze okna CMake jest polecenie, którym CLion uruchomił CMake. Powinno zawierać `-DCMAKE_BUILD_TYPE=Debug`, a katalog budowania nazywa się `cmake-build-debug`.

## 6. Zbuduj i uruchom program

**Budowanie.** Wybierz **Build | Build Project** (<kbd>Ctrl</kbd> + <kbd>F9</kbd> na Windowsie i Ubuntu, <kbd>⌘ Cmd</kbd> + <kbd>F9</kbd> na macOS). W oknie **Build** zobaczysz kolejne kroki. Ostatnie dwa wyglądają mniej więcej tak:

```text
[3/4] Building CXX object CMakeFiles/first_program.dir/main.cpp.o
[4/4] Linking CXX executable first_program
```

Liczby w nawiasach mogą być inne, a wcześniejsze kroki przygotowują budowanie. Na Windowsie nazwy plików kończą się na `.obj` i `.exe`. W katalogu projektu pojawił się katalog `cmake-build-debug`, a w nim plik wykonywalny `first_program` (na Windowsie `first_program.exe`). To jest Twój program.

**Uruchamianie.** Na pasku narzędzi u góry wybrana jest konfiguracja uruchomienia `first_program`. Kliknij obok niej zielony przycisk **Run** (▶). W oknie **Run** pojawi się:

```text
Hello! My first C++20 program works.

Process finished with exit code 0
```

`exit code 0` oznacza, że program zakończył się bez błędu.

Przed uruchomieniem **Run** sam buduje program, jeśli to potrzebne. Dlatego Run zwykle „po prostu działa”, ale pod spodem są to dwie czynności: budowanie i uruchamianie. Eksperyment w następnym punkcie je rozdziela.

## 7. Eksperyment: kod źródłowy a gotowy program

**Krok 1. Uruchom gotowy program bez CLiona.** Otwórz terminal wbudowany w CLion: **View | Tool Windows | Terminal** (<kbd>Alt</kbd> + <kbd>F12</kbd>, na macOS <kbd>⌥ Option</kbd> + <kbd>F12</kbd>). Terminal startuje w katalogu projektu; możesz to sprawdzić poleceniem `pwd`. Uruchom plik wykonywalny, podając jego ścieżkę:

| Windows | macOS i Ubuntu |
|---|---|
| `.\cmake-build-debug\first_program.exe` | `./cmake-build-debug/first_program` |

Kropka na początku to bieżący katalog, który znasz z lekcji 0.2. Programu z własnego katalogu nie uruchomisz samą nazwą, bo tego katalogu nie ma na liście `PATH` (lekcja 0.3). Program wypisze ten sam komunikat co w oknie Run.

**Krok 2. Zmień kod.** W `main.cpp` zmień tylko tekst **między cudzysłowami**, na przykład na `I changed this message!`. Nie usuwaj cudzysłowów ani znaków wokół nich. Na razie nie używaj polskich liter: nie każdy terminal wyświetla je poprawnie (wrócimy do tego później). Zapisz plik: **File | Save All** (<kbd>Ctrl</kbd> + <kbd>S</kbd>, na macOS <kbd>⌘ Cmd</kbd> + <kbd>S</kbd>).

**Krok 3. Przewidź, zanim sprawdzisz.** Plik `main.cpp` już się zmienił, ale niczego jeszcze nie budowano. Co wypisze program uruchomiony z terminala tak samo jak w kroku 1: stary czy nowy komunikat?

Sprawdź, wpisując to samo polecenie co w kroku 1. Zobaczysz **stary** komunikat.

**Krok 4. Zbuduj ponownie.** Wybierz **Build | Build Project**. W oknie Build widać, że kompilator znowu pracował. Uruchom program z terminala jeszcze raz. Teraz zobaczysz **nowy** komunikat.

**Krok 5. Zbuduj bez zmian.** Wybierz **Build | Build Project** jeszcze raz, nic nie zmieniając. W oknie Build zobaczysz komunikat w rodzaju `ninja: no work to do`: nic się nie zmieniło, więc nie było czego budować.

**Krok 6. Run.** Kliknij **Run** (▶). Zobaczysz nowy komunikat: CLion sprawdził, czy trzeba coś zbudować, a potem uruchomił program.

**Co się stało?** Plik wykonywalny w `cmake-build-debug` to osobny plik, który powstał przy budowaniu. Zmiana i zapisanie `main.cpp` zmienia tylko kod źródłowy. Program zmienia się dopiero wtedy, gdy zbudujesz go ponownie.

## 8. Ta sama praca bez CLiona

Ten sam projekt da się zbudować w zwykłym terminalu, bez CLiona. Nie musisz tego teraz robić: dokładnie przejdziemy to w [następnej lekcji](lesson_06_same_program_without_clion.md). Dla ciekawych: w katalogu projektu wystarczą dwa polecenia.

```text
cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Debug -DCMAKE_CXX_COMPILER=<ścieżka do clang++>
cmake --build build
```

Jako `<ścieżka do clang++>` wpisz tę samą ścieżkę co w toolchainie: na Windowsie `"C:\Program Files\LLVM\bin\clang++.exe"` (w cudzysłowie, bo zawiera spację), na macOS ścieżkę z Homebrew, na Ubuntu `/usr/bin/clang++-22`. Program pojawi się w katalogu `build`.

## 9. Misja: Twój komunikat

Spraw, żeby program wypisywał wybrany przez Ciebie komunikat, bez polskich liter, i zbierz trzy dowody.

1. **Właściwy kompilator:** linijka z okna CMake z `Clang 22`.
2. **Twój program działa:** okno Run z Twoim komunikatem i `Process finished with exit code 0`.
3. **Wyjaśnienie:** dwa, trzy zdania, dlaczego w kroku 3 eksperymentu program z terminala wypisał stary komunikat.

### Kryterium sukcesu

- Okno CMake pokazuje `Clang 22` (na Windowsie z `GNU-like command-line`) i ścieżkę do naszego kompilatora.
- Okno Run pokazuje Twój komunikat i `exit code 0`.
- Wyjaśnienie odróżnia kod źródłowy (`main.cpp`) od pliku wykonywalnego i mówi, że plik wykonywalny zmienia się dopiero po zbudowaniu.

## 10. Gdy coś pójdzie inaczej

| Co widzisz | Co to znaczy | Co zrobić |
|---|---|---|
| Okno CMake pokazuje inny kompilator niż `Clang 22` | Profil Debug używa innego toolchainu. | Punkt 4, a potem **Tools \| CMake \| Reset Cache and Reload Project**. |
| Windows: toolchain Visual Studio nie znajduje Build Tools | CLion nie wykrył instalacji z lekcji 0.4. | Wskaż katalog `C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools`. Jeśli go nie ma, wróć do lekcji 0.4. |
| Windows: CLion zgłasza, że kompilator nie pasuje do toolchainu | Ta konfiguracja nie jest jeszcze sprawdzona. | Wypróbuj wariant **System** z ramki w punkcie 4. |
| Przycisk Run jest nieaktywny albo nie ma konfiguracji `first_program` | Projekt nie został wczytany. | Sprawdź okno CMake: czy są błędy? Czy wybrano **Trust Project**? Jeśli projekt jest w trybie bezpiecznym (Safe Mode), wybierz **Trust Project** w komunikacie u góry okna. |
| Budowanie zgłasza `'iostream' file not found` albo `could not open 'kernel32.lib'` | Brakuje narzędzi systemowych. | Wróć do lekcji 0.4, punkt 4, „Narzędzia systemowe”. |
| `CMake 3.28 or higher is required` | CLion używa starszego CMake. | W ustawieniach toolchainu przywróć wbudowany CMake (**Bundled**). |
| Terminal: program nie jest znaleziony | Albo program nie został jeszcze zbudowany, albo ścieżka jest inna. | Zbuduj projekt. Sprawdź `pwd` i `ls cmake-build-debug`. Na Windowsie pamiętaj o `.\` i `.exe`. |
| Polskie litery w komunikacie wyglądają dziwnie | Terminal inaczej odczytuje polskie znaki. | Na razie używaj liter bez polskich znaków. |

## 11. Wyjaśnij

**1.** Jaka jest różnica między edytowaniem, budowaniem i uruchamianiem programu?

<details>
<summary>Odpowiedź</summary>

Edytowanie zmienia kod źródłowy. Budowanie zamienia kod źródłowy w plik wykonywalny. Uruchamianie wykonuje ten plik.

</details>

**2.** Dlaczego po zmianie `main.cpp` program uruchomiony z terminala wypisał stary komunikat?

<details>
<summary>Odpowiedź</summary>

Plik wykonywalny jest osobnym plikiem, który powstał przy poprzednim budowaniu. Zmiana `main.cpp` go nie zmienia. Nowy plik wykonywalny powstaje dopiero po ponownym zbudowaniu.

</details>

**3.** Dlaczego przycisk Run w CLionie od razu pokazał nowy komunikat?

<details>
<summary>Odpowiedź</summary>

Bo przed uruchomieniem CLion sam buduje program, jeśli kod się zmienił.

</details>

**4.** Po co wskazywać CLionowi toolchain, skoro program i tak się zbudował?

<details>
<summary>Odpowiedź</summary>

Bo CLion może sam wybrać inny kompilator, na przykład MinGW na Windowsie albo kompilator Apple na macOS. Program by się zbudował, ale nie tym kompilatorem, którego używamy w kursie i którego wyniki opisują lekcje.

</details>

## Podsumowanie

- Projekt C++ to tutaj dwa pliki: kod źródłowy `main.cpp` i opis projektu `CMakeLists.txt`.
- **Toolchain** to zestaw narzędzi do budowania. Sprawdzasz go w oknie CMake: musi być `Clang 22`.
- **Budowanie** tworzy plik wykonywalny w `cmake-build-debug`. **Run** buduje, jeśli trzeba, a potem uruchamia program.
- Zmiana kodu nie zmienia programu, dopóki go nie zbudujesz.

**Poprzednia lekcja:** [Lekcja 0.4: Przygotuj warsztat: instalacja narzędzi](lesson_04_installing_the_tools.md) · **Następna lekcja:** [Lekcja 0.6: Ten sam program bez CLiona](lesson_06_same_program_without_clion.md) · [Opis kursu](../../README.md)

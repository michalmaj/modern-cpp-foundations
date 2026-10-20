# Lekcja 0.6: Ten sam program bez CLiona

**Polski** · [English](lesson_06_same_program_without_clion.en.md) · [Opis kursu](../../README.md)

> **Moduł 0, lekcja 6** · około 45 minut
> **Potrzebujesz:** projektu `lesson_05_first_program` z [lekcji 0.5](lesson_05_first_program_in_clion.md) i narzędzi z [lekcji 0.4](lesson_04_installing_the_tools.md).

## Zanim zaczniesz

Ta lekcja zakłada, że po lekcjach 0.1–0.5:

- umiesz otworzyć terminal, przejść do katalogu (`cd`) i sprawdzić, gdzie jesteś (`pwd`, `ls`);
- uruchamiasz program z bieżącego katalogu, podając jego ścieżkę (`./…` albo `.\…`);
- masz projekt `lesson_05_first_program`.

Jeśli nie masz projektu, pobierz go tak jak w [lekcji 0.5, punkt 2](lesson_05_first_program_in_clion.md#2-pobierz-projekt). Do tej lekcji wystarczą pliki projektu: nie musi istnieć program zbudowany wcześniej w CLionie.

## Sytuacja

W lekcji 0.5 CLion zbudował i uruchomił program jednym kliknięciem. Czy to znaczy, że bez CLiona nie da się tego zrobić? Nie. CLion nie ma własnego, ukrytego kompilatora: wywołał te same narzędzia, które zainstalowano w lekcji 0.4. Dziś wywołasz je sam, w zwykłym terminalu.

Po tej lekcji będziesz:

- przechodzić w terminalu do katalogu projektu i rozpoznawać jego pliki;
- konfigurować i budować projekt przez CMake z właściwym kompilatorem `clang++`;
- uruchamiać zbudowany program bez CLiona;
- kompilować `main.cpp` bezpośrednio poleceniem `clang++`;
- wyjaśniać, co robią kompilator, CMake i Ninja;
- odróżniać konfigurację, budowanie i uruchamianie.

## 1. Przypomnienie: co jest czym

| Element | Co to jest |
|---|---|
| `main.cpp` | **Kod źródłowy**: tekst programu w C++. |
| `CMakeLists.txt` | **Opis projektu** dla CMake: z czego powstaje program i że to C++20. |
| program w katalogu budowania CLiona, zwykle `cmake-build-debug` | **Plik wykonywalny**, który zbudował CLion w lekcji 0.5 (jeśli zbudował). |
| **budowanie** | Zamiana kodu źródłowego w plik wykonywalny. |

W lekcji 0.5 CLion wywołał za Ciebie trzy narzędzia: **CMake**, który przygotował plan budowania, **Ninja**, który ten plan wykonał, i kompilator **`clang++`**, który zamienił kod w program. Teraz wywołasz je sam.

## 2. Wypróbuj: wejdź do katalogu projektu

Otwórz **zwykły terminal**, nie ten w CLionie. Przejdź do katalogu `lesson_05_first_program`.

Najprostszy sposób, żeby nie przepisywać długiej ścieżki: otwórz ten katalog w oknie plików i skopiuj jego ścieżkę.

- **Windows:** kliknij katalog prawym przyciskiem myszy i wybierz **Kopiuj jako ścieżkę**.
- **macOS:** w Finderze przytrzymaj <kbd>⌥ Option</kbd> i kliknij katalog prawym przyciskiem myszy. W menu pojawi się polecenie kopiowania ścieżki tego katalogu.
- **Ubuntu:** w oknie plików naciśnij <kbd>Ctrl</kbd> + <kbd>L</kbd> i skopiuj ścieżkę z paska adresu.

Potem w terminalu wpisz `cd`, spację i wklej ścieżkę w cudzysłowie, na przykład:

```text
cd "C:\Users\ola\Downloads\modern-cpp-foundations-main\course\module_00_tooling\lesson_05_first_program"
```

Sprawdź, czy jesteś na miejscu (na macOS i Ubuntu zamiast `ls` wpisz `ls -F`):

```text
pwd
ls
```

Na liście muszą być `main.cpp` i `CMakeLists.txt`.

Jeśli w lekcji 0.5 CLion zbudował program, zobaczysz też katalog budowania CLiona, zwykle `cmake-build-debug`; jego nazwa może być trochę inna. Możesz uruchomić ten program, wpisując nazwę katalogu, którą widzisz:

| Windows | macOS i Ubuntu |
|---|---|
| `.\cmake-build-debug\first_program.exe` | `./cmake-build-debug/first_program` |

Zobaczysz komunikat z lekcji 0.5, być może zmieniony w misji. Ten plik działa, choć CLion jest zamknięty. Jeśli takiego katalogu nie masz, pomiń ten krok: dalsza część lekcji go nie potrzebuje.

## 3. Zrozum: konfiguracja, budowanie, uruchamianie

Z terminala program powstaje w **trzech krokach**:

| Krok | Polecenie | Co się dzieje |
|---|---|---|
| 1. **Konfiguracja** | `cmake -S . -B build-terminal …` | CMake czyta `CMakeLists.txt`, sprawdza kompilator i zapisuje **plan budowania** w katalogu `build-terminal`. |
| 2. **Budowanie** | `cmake --build build-terminal` | CMake prosi Ninja o wykonanie planu, a Ninja uruchamia `clang++`. Powstaje plik wykonywalny. |
| 3. **Uruchamianie** | `./build-terminal/first_program` | Komputer wykonuje gotowy program. |

Konfigurację robisz **raz**. Po każdej zmianie kodu wystarczy budowanie.

Polecenie konfiguracji ma kilka części. Nie musisz ich zapamiętywać:

- `-S .`: kod źródłowy jest tutaj, w bieżącym katalogu (`.` znasz z lekcji 0.2);
- `-B build-terminal`: pliki budowania trafią do katalogu `build-terminal`, osobnego od katalogu, którego używa CLion;
- `-G Ninja`: budowanie wykona Ninja;
- `-DCMAKE_BUILD_TYPE=Debug`: konfiguracja Debug, jak w CLionie;
- `-DCMAKE_CXX_COMPILER=…`: pełna ścieżka do naszego kompilatora, żeby CMake nie wybrał innego.

## 4. Wypróbuj: zbuduj i uruchom z terminala

Wpisz trzy polecenia dla swojego systemu.

**Windows (PowerShell):**

```text
cmake -S . -B build-terminal -G Ninja -DCMAKE_BUILD_TYPE=Debug "-DCMAKE_CXX_COMPILER=C:\Program Files\LLVM\bin\clang++.exe"
cmake --build build-terminal
.\build-terminal\first_program.exe
```

Cudzysłów obejmuje **cały** ostatni element polecenia konfiguracji, bo ścieżka zawiera spację (`Program Files`). Bez niego PowerShell podzieliłby go na dwie części.

**macOS:**

```text
cmake -S . -B build-terminal -G Ninja -DCMAKE_BUILD_TYPE=Debug -DCMAKE_CXX_COMPILER=/opt/homebrew/opt/llvm@22/bin/clang++
cmake --build build-terminal
./build-terminal/first_program
```

Na komputerze z procesorem Intel zamiast `/opt/homebrew/opt/llvm@22` wpisz `/usr/local/opt/llvm@22`. Pewną ścieżkę pokaże `brew --prefix llvm@22`.

**Ubuntu:**

```text
cmake -S . -B build-terminal -G Ninja -DCMAKE_BUILD_TYPE=Debug -DCMAKE_CXX_COMPILER=/usr/bin/clang++-22
cmake --build build-terminal
./build-terminal/first_program
```

**Sprawdź po każdym kroku:**

1. **Konfiguracja:** w wyniku są linijki `The CXX compiler identification is Clang 22…`, `Check for working CXX compiler:` ze ścieżką do naszego kompilatora i na końcu `Build files have been written to: …build-terminal`. To te same linijki, które w lekcji 0.5 widać było w oknie CMake w CLionie.
2. **Budowanie:** ostatnia linijka mówi `Linking CXX executable first_program` (na Windowsie `first_program.exe`).
3. **Uruchamianie:** program wypisuje ten sam komunikat co wersja z CLiona. To ten sam kod, więc i ten sam wynik.

## 5. Eksperyment: kompilator bez CMake

Nasz program to jeden krótki plik, więc kompilator poradzi sobie z nim sam. Wpisz:

| System | Kompilacja | Uruchomienie |
|---|---|---|
| Windows | `clang++ -std=c++20 main.cpp -o first_program_direct.exe` | `.\first_program_direct.exe` |
| macOS | `/opt/homebrew/opt/llvm@22/bin/clang++ -std=c++20 main.cpp -o first_program_direct` | `./first_program_direct` |
| Ubuntu | `clang++-22 -std=c++20 main.cpp -o first_program_direct` | `./first_program_direct` |

- `-std=c++20` mówi kompilatorowi, że to C++20; w projekcie CMake to samo zapisano w `CMakeLists.txt`.
- `-o first_program_direct` nadaje programowi nazwę, żeby nie pomylić go z wersją zbudowaną przez CMake.
- Na macOS podajesz pełną ścieżkę, bo samo `clang++` to kompilator Apple (lekcja 0.4).

Program wypisze ten sam komunikat.

**Dlaczego wystarczyło jedno polecenie?** Program ma jeden plik i nie potrzebuje żadnych dodatkowych ustawień, więc `clang++` sam wykonuje wszystkie kroki potrzebne do powstania pliku wykonywalnego.

**Po co więc CMake?** Prawdziwe programy mają wiele plików i ustawień. CMake zapamiętuje je w `CMakeLists.txt`, a ten sam opis działa w CLionie i w terminalu, na każdym systemie. Dlatego **w kursie budujemy przez CMake**. Bezpośrednie wywołanie `clang++` było tylko eksperymentem, żeby zobaczyć, co robi sam kompilator.

## 6. Eksperyment: jeden kod, kilka programów

Masz teraz dwa albo trzy pliki wykonywalne zbudowane z tego samego `main.cpp`:

- `build-terminal/first_program` (zbudował CMake w terminalu);
- `first_program_direct` (zbudował bezpośrednio `clang++`);
- jeśli masz go z lekcji 0.5: program w katalogu budowania CLiona, na przykład `cmake-build-debug/first_program`.

**Krok 1.** Zmień kod, używając CLiona tylko jako edytora. Otwórz w nim projekt tak jak w lekcji 0.5 (**Open** i katalog `lesson_05_first_program`), kliknij `main.cpp` i zmień tekst między cudzysłowami, na przykład na `Three programs, one source.` Na razie bez polskich liter. Zapisz plik (<kbd>Ctrl</kbd> + <kbd>S</kbd>, na macOS <kbd>⌘ Cmd</kbd> + <kbd>S</kbd>).

**Nie klikaj Build ani Run.** Edytowanie i zapisanie pliku w CLionie niczego nie buduje: program zbudujesz w terminalu, swoimi poleceniami. Jeśli CLion pokaże przy tym komunikaty o projekcie, do samej edycji nie są potrzebne. Inne edytory tekstu potrafią niepostrzeżenie zmieniać znaki, na przykład cudzysłowy, dlatego na razie zostań przy CLionie.

**Krok 2. Przewidź:** co wypisze każdy z programów, jeśli uruchomisz je teraz, przed jakimkolwiek budowaniem? Zapisz przewidywania w tabeli:

| Program | Przewidywanie | Wynik |
|---|---|---|
| `build-terminal/first_program` | | |
| `first_program_direct` | | |
| program CLiona (jeśli go masz) | | |

Uruchom każdy po jego ścieżce i uzupełnij kolumnę „Wynik”.

**Krok 3.** Zbuduj tylko wersję terminalową: `cmake --build build-terminal`. Bez ponownej konfiguracji: plan już istnieje. Przewidź, który program teraz wypisze nowy komunikat, i sprawdź wszystkie.

**Krok 4.** Skompiluj ponownie `first_program_direct` poleceniem z punktu 5 i uruchom go.

**Co się stało?** Każdy plik wykonywalny jest osobnym plikiem. Zmienia się tylko ten program, który zbudujesz ponownie. Pozostałe nadal wypisują stary komunikat. Jeśli masz program z CLiona, on też ma starą wersję: CLion niczego nie budował.

## 7. Misja końcowa Modułu 0

Ta misja zbiera wszystko, czego nauczył Cię Moduł 0. Budowanie i uruchamianie wykonaj w zwykłym terminalu, bez CLiona. Zapisuj wyniki kolejnych kroków, na przykład w notatkach albo jako zrzuty ekranu.

1. **Znajdź projekt:** przejdź do katalogu `lesson_05_first_program` i sprawdź `pwd` oraz listę plików.
2. **Sprawdź kompilator:** sprawdź wersję kompilatora (polecenie z lekcji 0.4) i znajdź linijkę `The CXX compiler identification is Clang 22…` w wyniku konfiguracji.
3. **Skonfiguruj i zbuduj:** użyj nowego katalogu budowania, na przykład `build-mission`.
4. **Uruchom** zbudowany program.
5. **Zmień komunikat** na własny (w CLionie, tak jak w punkcie 6), **zbuduj ponownie** (bez konfiguracji) i sprawdź nowy wynik.
6. **Wyjaśnij** własnymi słowami, w jednym zdaniu dla każdego, do czego służą: `main.cpp`, kompilator `clang++`, CMake, Ninja i plik wykonywalny.

### Kryterium sukcesu

- Konfiguracja pokazuje `Clang 22` i ścieżkę do naszego kompilatora.
- Program z `build-mission` wypisuje najpierw stary, a po zmianie i ponownym zbudowaniu Twój komunikat.
- Budowanie i uruchamianie wykonano w terminalu; CLion służył najwyżej jako edytor.
- Wyjaśnienia odróżniają kod źródłowy od pliku wykonywalnego oraz rolę CMake (plan), Ninja (wykonanie planu) i kompilatora (zamiana kodu w program).

## 8. Gdy coś pójdzie inaczej

Gdy coś się nie udaje, **czytaj komunikaty od początku** i znajdź pierwszą informację, która wyjaśnia przyczynę. Często jest to pierwszy komunikat `CMake Error` albo `error:`, ale bywa nią też wcześniejsze ostrzeżenie (`Warning`), linijka konfiguracji, na przykład z niewłaściwym kompilatorem, albo informacja o brakującym pliku. Dalsze linijki to zwykle skutki tego pierwszego problemu.

| Co widzisz | Co to znaczy | Co zrobić |
|---|---|---|
| `The source directory … does not appear to contain CMakeLists.txt` | Terminal jest w innym katalogu niż projekt. | Sprawdź `pwd` i `ls`. Przejdź do `lesson_05_first_program`. |
| Windows: `Ignoring extra path from command line: "Files\LLVM\bin\clang++.exe"`, a dalej `The CXX compiler identification is unknown` | Brakuje cudzysłowu: PowerShell podzielił ścieżkę na spacji w `Program Files`. | Weź w cudzysłów cały element `"-DCMAKE_CXX_COMPILER=C:\Program Files\LLVM\bin\clang++.exe"`. |
| Konfiguracja pokazuje inny kompilator niż `Clang 22` | Wpisano inną ścieżkę kompilatora. | Sprawdź ścieżkę z punktu 4. |
| Komunikat o zmianie ustawień i usuwaniu cache (`You have changed variables that require your cache to be deleted`) | W tym katalogu budowania była już konfiguracja z innym kompilatorem. CMake zaczyna ją od nowa. | Sprawdź, czy teraz widać `Clang 22`. Jeśli coś dalej się nie zgadza, usuń katalog budowania w oknie plików (trafi do Kosza) i skonfiguruj ponownie. |
| Budowanie kończy się błędem i programu nie ma | Plik wykonywalny nie powstał. | Znajdź w wyniku budowania pierwszy komunikat, który wyjaśnia przyczynę. Jeśli zmieniano kod, sprawdź, czy nie usunięto cudzysłowu albo innego znaku. |
| Program wypisuje stary komunikat | Uruchomiono program, którego nie zbudowano po zmianie kodu. | Zbuduj ten program ponownie albo sprawdź, czy wpisano ścieżkę do właściwego pliku. |
| Program nie jest rozpoznawany, gdy wpisujesz samą nazwę | Programu z bieżącego katalogu nie ma na liście `PATH` (lekcja 0.3). | Dopisz ścieżkę: `./` na macOS i Ubuntu, `.\` na Windowsie. |
| macOS: `clang++ -std=c++20 …` działa, ale to kompilator Apple | Samo `clang++` to na macOS kompilator Apple. | Użyj pełnej ścieżki z punktu 5. |

## 9. Wyjaśnij

**1.** Czym różni się konfiguracja od budowania?

<details>
<summary>Odpowiedź</summary>

Konfiguracja (`cmake -S . -B …`) przygotowuje plan budowania i sprawdza kompilator. Budowanie (`cmake --build …`) wykonuje ten plan i tworzy plik wykonywalny.

</details>

**2.** Dlaczego po zmianie `main.cpp` wystarczyło `cmake --build`, bez ponownej konfiguracji?

<details>
<summary>Odpowiedź</summary>

Plan budowania już istniał, a w samym projekcie nic się nie zmieniło. Ninja zauważył zmieniony plik i zbudował program ponownie.

</details>

**3.** Dlaczego `first_program_direct` wypisywał stary komunikat po `cmake --build build-terminal`?

<details>
<summary>Odpowiedź</summary>

Bo `cmake --build build-terminal` zbudował tylko program w `build-terminal`. `first_program_direct` to osobny plik, który zmienia się dopiero po ponownej kompilacji poleceniem `clang++`.

</details>

**4.** Czy do zbudowania programu potrzebny jest CLion? Do czego więc służy?

<details>
<summary>Odpowiedź</summary>

Nie. Program budują CMake, Ninja i kompilator. CLion wywołuje te same narzędzia i ułatwia pracę: edytor, przyciski, okna z wynikami, a później debugger.

</details>

## Podsumowanie lekcji

- Z terminala program powstaje w trzech krokach: **konfiguracja** (CMake przygotowuje plan), **budowanie** (Ninja wykonuje plan, wywołując `clang++`) i **uruchamianie**.
- Konfiguracja raz, budowanie po każdej zmianie kodu.
- Jeden plik `main.cpp` można też skompilować bezpośrednio `clang++`, ale w kursie budujemy przez CMake.
- Każdy plik wykonywalny zmienia się dopiero po ponownym zbudowaniu.

## Podsumowanie Modułu 0

Spójrz, jaka droga jest już za Tobą:

1. **Lekcja 0.1:** pliki, katalogi, ścieżki i pierwsze polecenia w terminalu.
2. **Lekcja 0.2:** poruszanie się między katalogami.
3. **Lekcja 0.3:** czym są polecenia i programy, kod źródłowy i kompilator.
4. **Lekcja 0.4:** przygotowanie warsztatu: kompilator, CMake, Ninja i CLion.
5. **Lekcja 0.5:** pierwszy program zbudowany i uruchomiony w CLionie.
6. **Lekcja 0.6:** ten sam program zbudowany i uruchomiony samodzielnie, w terminalu.

Na początku Modułu 0 terminal mógł być czymś zupełnie nowym. Teraz potrafisz sam zbudować i uruchomić program w C++.

## Co dalej: Moduł 1

W Module 1 zaczniesz naprawdę rozumieć i pisać kod w C++20. Dowiesz się, co znaczą linijki w `main.cpp`, i napiszesz pierwsze własne programy. Zacznij od [lekcji 1.1: Pierwszy program od środka](../module_01_first_programs/lesson_01_first_program_inside.md). Moduł 1 jest rozwijany: kolejne lekcje są w przygotowaniu.

**Poprzednia lekcja:** [Lekcja 0.5: Twój pierwszy działający program w CLionie](lesson_05_first_program_in_clion.md) · **Następna lekcja:** [Lekcja 1.1: Pierwszy program od środka](../module_01_first_programs/lesson_01_first_program_inside.md) · [Opis kursu](../../README.md)

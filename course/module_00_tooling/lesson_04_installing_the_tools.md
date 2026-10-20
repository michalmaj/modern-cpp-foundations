# Lekcja 0.4: Przygotuj warsztat: instalacja narzędzi

**Polski** · [English](lesson_04_installing_the_tools.en.md) · [Opis kursu](../../README.md)

> **Moduł 0, lekcja 4** · zwykle od 30 minut do 2 godzin, zależnie od komputera i szybkości internetu
> **Potrzebujesz:** komputera z Windows 10/11, macOS albo Ubuntu 24.04, dostępu do internetu, kilku gigabajtów wolnego miejsca na dysku i **uprawnień administratora** (patrz [punkt 2](#2-zanim-zaczniesz-instalować)).

## Zanim zaczniesz

Ta lekcja zakłada, że po lekcjach [0.1](lesson_01_files_and_terminal.md), [0.2](lesson_02_moving_between_folders.md) i [0.3](lesson_03_commands_and_programs.md):

- umiesz otworzyć terminal i poruszać się po katalogach;
- wiesz, że polecenie może uruchomić osobny program, a powłoka szuka programów w katalogach z listy `PATH`;
- wiesz, że **kompilator** zamienia kod źródłowy w program.

## Sytuacja

Z lekcji 0.3 znasz drogę od tekstu do programu:

```text
kod źródłowy  →  kompilator  →  program
```

Na Twoim komputerze nie ma jeszcze kompilatora C++. W tej lekcji przygotujesz cały warsztat: zainstalujesz potrzebne narzędzia i sprawdzisz, czy są na miejscu. W następnej lekcji użyjesz ich, żeby uruchomić pierwszy program w C++.

Po tej lekcji będziesz:

- wiedzieć, do czego służy każde instalowane narzędzie;
- mieć zainstalowane narzędzia kursu w swoim systemie;
- umieć sprawdzić ich wersje w terminalu;
- umieć rozpoznać, czy używasz właściwego kompilatora.

## 1. Zrozum: co instalujesz i po co

| Narzędzie | Do czego służy | Kiedy go użyjesz |
|---|---|---|
| **LLVM/Clang 22** z kompilatorem `clang++` | Kompilator C++: zamienia Twój kod w program. | W następnej lekcji, przy pierwszym programie |
| **Narzędzia systemowe**: na Windowsie *Visual Studio Build Tools*, na macOS *Command Line Tools*, na Ubuntu pakiety, które system doinstaluje razem z Clangiem | Gotowe części, z których korzysta każdy program w C++, na przykład **biblioteka standardowa** (gotowy kod do wypisywania tekstu czy liczenia), oraz pliki systemu operacyjnego potrzebne do zbudowania programu. | Za każdym razem, gdy kompilujesz, choć nie uruchamiasz ich samodzielnie |
| **CMake** | Opisuje, z jakich plików składa się projekt i jak go zbudować. | Od następnej lekcji |
| **Ninja** | Szybko wykonuje kroki budowania, które przygotował CMake. | Od następnej lekcji, „w tle” |
| **CLion** | Środowisko programistyczne (IDE): tu piszesz, uruchamiasz i sprawdzasz programy. | Od następnej lekcji |

Nie musisz jeszcze rozumieć, jak te narzędzia działają w środku. Wystarczy, że wiesz, po co są.

Większość z nich zainstalujesz **menedżerem pakietów**. To program, który pobiera i instaluje inne programy z zaufanego źródła i pilnuje ich wersji. Na Windowsie będzie to **Chocolatey**, na macOS **Homebrew**, a na Ubuntu wbudowany **apt**.

## 2. Zanim zaczniesz instalować

- **Uprawnienia administratora.** Instalowanie narzędzi systemowych wymaga konta z uprawnieniami administratora. Na Windowsie uruchomisz terminal „jako administrator”. Na macOS i Ubuntu system poprosi o Twoje hasło.
- **Komputer szkolny, uczelniany albo służbowy.** Często nie ma na nim uprawnień administratora. Wtedy poproś administratora tego komputera o instalację narzędzi wymienionych w tej lekcji. Nie szukaj w internecie sposobów na obejście blokad: łatwo wtedy zainstalować coś innego, niż potrzebujesz.
- **Wpisywanie hasła w terminalu.** Gdy terminal pyta o hasło, **nie widać wpisywanych znaków**, nawet gwiazdek. To normalne. Wpisz hasło i naciśnij <kbd>Enter</kbd>.
- **Długie polecenia.** Część poleceń w tej lekcji jest długa. Możesz je skopiować i wkleić. Na Windowsie i macOS zrób to zwykłym skrótem, a w terminalu Ubuntu skrótem <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>V</kbd>.
- **Zrób tylko część dla swojego systemu.** Punkt 3 ma osobne instrukcje dla Windows, macOS i Ubuntu.

## 3. Zainstaluj narzędzia

### Windows

**Krok 1. Visual Studio Build Tools.**

1. Pobierz instalator ze strony Microsoftu: [Build Tools for Visual Studio 2022](https://aka.ms/vs/17/release/vs_buildtools.exe).
2. Uruchom pobrany plik. Otworzy się *Visual Studio Installer*.
3. Na karcie **Workloads** (Obciążenia) zaznacz **Desktop development with C++** (Programowanie aplikacji klasycznych w języku C++). Pozostałych ustawień nie zmieniaj.
4. Kliknij **Install** i poczekaj na koniec instalacji. To może potrwać, a instalacja zajmuje kilka gigabajtów. Jeśli instalator poprosi o ponowne uruchomienie komputera, zrób to.

Nie instalujesz w ten sposób programu Visual Studio. Dostajesz tylko części, z których skorzysta `clang++`: bibliotekę standardową i pliki systemu Windows.

**Krok 2. Chocolatey.**

1. Otwórz terminal **jako administrator**:
   - **Windows 11:** w menu Start wpisz `Terminal`, kliknij prawym przyciskiem myszy **Terminal** i wybierz **Uruchom jako administrator**.
   - **Windows 10:** w menu Start wpisz `PowerShell`, kliknij prawym przyciskiem myszy **Windows PowerShell** i wybierz **Uruchom jako administrator**. To ta sama powłoka co w lekcji 0.1, tylko z uprawnieniami administratora.

   System zapyta, czy pozwolić tej aplikacji na wprowadzanie zmian. Zgódź się.
2. Wejdź na stronę [chocolatey.org/install](https://chocolatey.org/install), wybierz instalację **Individual** i skopiuj podane tam polecenie.
3. Wklej polecenie do terminala i naciśnij <kbd>Enter</kbd>.
4. Gdy instalacja się skończy, **zamknij terminal i otwórz nowy, znowu jako administrator**. Nowy terminal zna już nowe programy (pamiętasz `PATH` z lekcji 0.3).

**Krok 3. LLVM, CMake i Ninja.** W terminalu administratora wpisz po kolei:

```text
choco install llvm --version=22.1.8 -y
choco install cmake --installargs '"ADD_CMAKE_TO_PATH=System"' -y
choco install ninja -y
```

Dopisek `--installargs '"ADD_CMAKE_TO_PATH=System"'` prosi instalator CMake, żeby dodał CMake do listy `PATH`. Bez niego polecenie `cmake` nie zadziała w terminalu.

**Krok 4.** Zamknij terminal administratora i otwórz **zwykły** terminal. Sprawdzanie i dalsza praca odbywają się już bez uprawnień administratora.

### macOS

**Krok 1. Command Line Tools.** W terminalu wpisz:

```text
xcode-select --install
```

Otworzy się okno z pytaniem o instalację narzędzi. Kliknij **Zainstaluj** i poczekaj. Dostaniesz pliki systemu macOS, linker i inne narzędzia, z których skorzysta kompilator. Jeśli zobaczysz komunikat, że narzędzia są już zainstalowane, przejdź dalej.

**Krok 2. Homebrew.**

1. Wejdź na stronę [brew.sh](https://brew.sh), skopiuj polecenie instalacyjne z sekcji *Install Homebrew* i wklej je do terminala.
2. Instalator zapyta o hasło do Twojego konta.
3. Na końcu instalator wypisze sekcję **Next steps** z kilkoma poleceniami. **Wykonaj je**: dodają Homebrew do listy `PATH`.
4. Zamknij terminal i otwórz nowy. Sprawdź `brew --version`.

**Krok 3. LLVM 22, CMake i Ninja.**

```text
brew install llvm@22 cmake ninja
```

Formuła `llvm@22` to LLVM w serii 22. Homebrew celowo **nie dodaje** jej do listy `PATH`, żeby nie zasłonić kompilatora dostarczonego przez Apple. Dlatego w punkcie 4 uruchomisz ją po pełnej ścieżce.

### Ubuntu 24.04

**Krok 1. Programy potrzebne do dodania źródła pakietów.**

```text
sudo apt update
sudo apt install -y wget gnupg ca-certificates
```

`sudo` oznacza „wykonaj jako administrator”, więc system zapyta o Twoje hasło. Na większości komputerów z Ubuntu te programy już są, a wtedy `apt` po prostu to zgłosi.

**Krok 2. Dodaj źródło pakietów LLVM.** Ubuntu ma w swoich pakietach starszą wersję Clanga, a my potrzebujemy wersji 22. Dlatego dopisujesz do systemu oficjalne źródło pakietów projektu LLVM ([apt.llvm.org](https://apt.llvm.org)):

```text
wget -qO- https://apt.llvm.org/llvm-snapshot.gpg.key | sudo tee /etc/apt/trusted.gpg.d/apt.llvm.org.asc
echo "deb https://apt.llvm.org/noble/ llvm-toolchain-noble-22 main" | sudo tee /etc/apt/sources.list.d/llvm-22.list
```

Pierwsze polecenie zapisuje klucz, dzięki któremu system sprawdzi, czy pakiety naprawdę pochodzą od LLVM. Drugie dopisuje adres źródła. Oba wypiszą w terminalu to, co zapisały. To normalne.

**Krok 3. LLVM 22, CMake i Ninja.**

```text
sudo apt update
sudo apt install -y clang-22 cmake ninja-build
```

Razem z `clang-22` system sam doinstaluje bibliotekę standardową C++ i pozostałe narzędzia systemowe, z których korzysta kompilator. Nie musisz ich wybierać ręcznie.

### CLion (każdy system)

1. Pobierz CLion ze strony [jetbrains.com/clion/download](https://www.jetbrains.com/clion/download/) i zainstaluj go jak zwykły program. Na Ubuntu możesz też użyć polecenia `sudo snap install clion --classic`.
2. Uruchom CLion. Przy pierwszym uruchomieniu wybierz licencję. Jeśli uczysz się samodzielnie, możesz wybrać darmową licencję **do użytku niekomercyjnego**. Wymaga ona konta JetBrains i warunkiem jest wysyłanie do JetBrains anonimowych statystyk użycia, czego nie da się wyłączyć. Szkoły i uczelnie mają osobne licencje dla pracowni, więc na komputerze szkolnym zapytaj nauczyciela albo administratora.
3. Jeśli CLion zaproponuje utworzenie projektu albo konfigurację narzędzi, możesz to okno zamknąć. Skonfigurujesz go w następnej lekcji.

## 4. Sprawdź: czy warsztat jest gotowy?

Otwórz **nowy** zwykły terminal i wpisz polecenia dla swojego systemu.

### Kompilator

| System | Polecenie | Czego szukać w wyniku |
|---|---|---|
| Windows | `clang++ --version` | `clang version 22.1.8` oraz `Target: x86_64-pc-windows-msvc` |
| Windows | `Get-Command clang++` | ścieżka `C:\Program Files\LLVM\bin\clang++.exe` |
| macOS | `brew --prefix llvm@22`, a potem pełna ścieżka z wyniku i `/bin/clang++ --version`, na przykład `/opt/homebrew/opt/llvm@22/bin/clang++ --version` | `Homebrew clang version 22.1.8` |
| Ubuntu | `clang++-22 --version` | `clang version 22.1.8`, na przykład `Ubuntu clang version 22.1.8 (++…)` |

Liczy się **główny numer wersji: 22**. Ostatnie cyfry mogą być wyższe niż w tabeli, na przykład `22.1.9`: to w porządku.

### Czy to właściwy kompilator?

Na jednym komputerze może być kilka kompilatorów o podobnych nazwach. Z lekcji 0.3 wiesz, że powłoka uruchamia pierwszy znaleziony program o danej nazwie. Sprawdź:

- **macOS:** wpisz samo `clang++ --version`. Zobaczysz `Apple clang version …`. To **kompilator Apple**, a nie nasz. Jest w systemie i niczemu nie przeszkadza, ale w kursie używamy Homebrew clang, podając jego pełną ścieżkę.
- **Ubuntu:** samo `clang++ --version` może pokazać starszą wersję, na przykład `Ubuntu clang version 18…`, albo zgłosić, że polecenia nie ma. Nasz kompilator to `clang++-22`, z numerem w nazwie.
- **Windows:** `Get-Command clang++` musi wskazywać katalog `C:\Program Files\LLVM\bin`. Jeśli wskazuje inny, na przykład katalog Visual Studio albo MinGW, zobacz punkt 6.

### CMake i Ninja

| Polecenie | Czego szukać |
|---|---|
| `cmake --version` | `cmake version 3.28` albo nowszej (na przykład 4.x) |
| `ninja --version` | numer wersji, na przykład `1.11.1` albo `1.13.2` |

### Narzędzia systemowe

- **Windows:** otwórz z menu Start program **Visual Studio Installer**. Na liście powinno być **Visual Studio Build Tools 2022** z zainstalowanym obciążeniem *Desktop development with C++*.
- **macOS:** `xcode-select -p` pokazuje ścieżkę, na przykład `/Library/Developer/CommandLineTools`.
- **Ubuntu:** instalują się automatycznie razem z `clang-22`. Nie musisz ich osobno sprawdzać.

## 5. Misja: raport z warsztatu

Wypełnij tabelę dla swojego komputera:

| Narzędzie | Jak sprawdzasz (punkt 4) | Twój wynik | Właściwe? (tak/nie) |
|---|---|---|---|
| kompilator `clang++` (LLVM 22) | | | |
| CMake | | | |
| Ninja | | | |
| narzędzia systemowe | | | |
| CLion | uruchomienie programu | | |

W kolumnie „Twój wynik” wpisz to, co pokazał sposób sprawdzenia z punktu 4. Dla kompilatora, CMake i Ninja będzie to numer wersji. Dla narzędzi systemowych: na Windowsie „Build Tools 2022 na liście”, na macOS ścieżka z `xcode-select -p`, na Ubuntu „instalują się razem z clang-22”. Dla CLiona: „uruchamia się”.

Do każdego wiersza dopisz jednym zdaniem, **do czego** to narzędzie posłuży w następnej lekcji.

### Kryterium sukcesu

- Kompilator zgłasza **wersję 22** i jest to **nasz** kompilator: na Windowsie z katalogu `C:\Program Files\LLVM\bin`, na macOS „Homebrew clang” (nie „Apple clang”), na Ubuntu `clang++-22`.
- `cmake --version` pokazuje 3.28 lub nowszą, a `ninja --version` wypisuje wersję.
- Narzędzia systemowe są zainstalowane (sprawdzone sposobem z punktu 4).
- CLion się uruchamia.

Jeśli wszystko się zgadza, Twój warsztat jest gotowy. Nie musisz jeszcze niczego kompilować: zrobisz to w następnej lekcji.

## 6. Gdy coś pójdzie inaczej

| Co widzisz | Co to znaczy | Co zrobić |
|---|---|---|
| Polecenie nie jest rozpoznawane zaraz po instalacji (`… is not recognized…` albo `command not found`) | Terminal otwarty przed instalacją ma starą listę `PATH`. | Zamknij terminal i otwórz nowy. Jeśli to nie pomoże, sprawdź, czy instalacja zakończyła się bez błędów. |
| Windows: Chocolatey zgłasza, że nie działa w terminalu z uprawnieniami administratora | Instalacja wymaga uprawnień administratora. | Otwórz terminal przez **Uruchom jako administrator** (punkt 3, krok 2). |
| Brak uprawnień administratora na komputerze szkolnym lub służbowym | Bez nich nie zainstalujesz tych narzędzi. | Poproś administratora tego komputera o instalację. Nie stosuj obejść z internetu. |
| Ubuntu: `E: Unable to locate package clang-22` | System nie zna źródła pakietów LLVM. | Sprawdź, czy wykonano oba polecenia z kroku 2, a potem `sudo apt update`. |
| macOS: `clang++ --version` pokazuje `Apple clang` | To kompilator Apple, a nie nasz. | Tak ma być. Nasz kompilator uruchamiasz pełną ścieżką z punktu 4. |
| Ubuntu: `clang++ --version` pokazuje wersję 18 | To starszy Clang z pakietów Ubuntu. | Używaj `clang++-22`. |
| Windows: `Get-Command clang++` pokazuje inną ścieżkę niż `C:\Program Files\LLVM\bin` | Na komputerze jest inny `clang++`, który powłoka znajduje pierwszy. | Nie odinstalowuj niczego na ślepo. Zapisz tę ścieżkę. W następnej lekcji podamy CLionowi pełną ścieżkę do właściwego kompilatora. |
| Windows: instalator Build Tools prosi o ponowne uruchomienie | Część plików zostanie dokończona po restarcie. | Uruchom komputer ponownie, a potem przejdź do kroku 2. |
| Kompilator jest zainstalowany, ale później pierwsza kompilacja zgłasza brak plików, na przykład `'iostream' file not found` albo na Windowsie `lld-link: error: could not open 'kernel32.lib'` | Brakuje narzędzi systemowych z biblioteką standardową. | Wróć do tej lekcji i sprawdź narzędzia systemowe (punkt 4). Taki problem widać dopiero przy kompilacji, w następnej lekcji. |

## 7. Wyjaśnij

Odpowiedz własnymi słowami, a dopiero potem rozwiń odpowiedź.

**1.** Po co instalujesz narzędzia systemowe (na Windowsie Build Tools, na macOS Command Line Tools), skoro masz już kompilator? Co z tym robi Ubuntu?

<details>
<summary>Odpowiedź</summary>

Kompilator sam nie wystarczy. Programy w C++ korzystają z biblioteki standardowej i z plików systemu operacyjnego, a te dostarczają właśnie narzędzia systemowe. Na Ubuntu system instaluje je automatycznie razem z `clang-22`.

</details>

**2.** Dlaczego po instalacji trzeba otworzyć nowy terminal?

<details>
<summary>Odpowiedź</summary>

Terminal wczytuje listę `PATH` przy starcie. Stary terminal nie wie o katalogach, które instalator dopisał później.

</details>

**3.** Na macOS `clang++ --version` pokazuje „Apple clang”, a pełna ścieżka do Homebrew pokazuje „Homebrew clang version 22”. Jak to możliwe, skoro polecenie nazywa się tak samo?

<details>
<summary>Odpowiedź</summary>

To dwa różne programy o tej samej nazwie, w różnych katalogach. Powłoka uruchamia pierwszy znaleziony na liście `PATH`, a pełna ścieżka wskazuje konkretny plik, tak jak `whoami` po pełnej ścieżce w lekcji 0.3.

</details>

**4.** Do czego posłużą CMake i Ninja w następnej lekcji?

<details>
<summary>Odpowiedź</summary>

CMake opisze, jak zbudować projekt, a Ninja wykona kroki budowania. Razem zamienią kod źródłowy w program przy użyciu kompilatora.

</details>

## Podsumowanie

- Masz gotowy warsztat C++: kompilator `clang++` z LLVM 22, narzędzia systemowe, CMake, Ninja i CLion.
- Wiesz, do czego służy każde z tych narzędzi.
- Umiesz sprawdzić ich wersje i rozpoznać, czy używasz właściwego kompilatora.
- Po instalacji otwieraj nowy terminal.

**Poprzednia lekcja:** [Lekcja 0.3: Co się dzieje, gdy wpisujesz polecenie?](lesson_03_commands_and_programs.md) · **Następna lekcja:** [Lekcja 0.5: Twój pierwszy działający program w CLionie](lesson_05_first_program_in_clion.md) · [Opis kursu](../../README.md)

# Lekcja 0.3: Co się dzieje, gdy wpisujesz polecenie?

**Polski** · [English](lesson_03_commands_and_programs.en.md) · [Opis kursu](../../README.md)

> **Moduł 0, lekcja 3** · około 30 minut
> **Potrzebujesz:** komputera z Windows, macOS albo Linuksem. Nie musisz niczego instalować.

## Zanim zaczniesz

Ta lekcja zakłada, że po [lekcji 0.1](lesson_01_files_and_terminal.md) i [lekcji 0.2](lesson_02_moving_between_folders.md):

- wiesz, czym są terminal i powłoka;
- znasz ścieżki i potrafisz używać `pwd`, `ls` i `cd`;
- wiesz, że w PowerShellu `pwd`, `ls` i `cd` to aliasy (lekcja 0.2, punkt 9).

Nie potrzebujesz żadnych plików z poprzednich lekcji.

## Sytuacja

Wpisywało się już dziesiątki poleceń: `pwd`, `ls`, `cd`. Za każdym razem coś się działo. Ale kto właściwie to zrobił? Czy gdzieś na dysku leży coś, co nazywa się `pwd`?

Odpowiedź na to pytanie prowadzi prosto do celu tego modułu: uruchomienia programu napisanego w C++.

Po tej lekcji będziesz wiedzieć:

- czym jest polecenie i co robi z nim powłoka;
- że nie każde polecenie jest osobnym programem;
- czym jest program i plik wykonywalny;
- czym program różni się od kodu źródłowego;
- dlaczego zainstalowane narzędzia można uruchamiać, wpisując samą ich nazwę.

## 1. Zrozum: co robi powłoka po naciśnięciu Enter

**Polecenie** to tekst, który wpisujesz w terminalu i przekazujesz powłoce klawiszem <kbd>Enter</kbd>. Pierwsze słowo to **nazwa polecenia**. Reszta mówi, na czym polecenie ma działać, na przykład `krakow` w `cd krakow`.

Gdy naciśniesz <kbd>Enter</kbd>, powłoka patrzy na nazwę i ma dwie możliwości:

1. **Robi to sama.** Niektóre polecenia są **wbudowane** w powłokę. To jej własne umiejętności.
2. **Uruchamia osobny program.** **Program** to plik na dysku z instrukcjami, które komputer potrafi wykonać. Taki plik nazywa się **plikiem wykonywalnym**.

Na Windowsie jest jeszcze krok wcześniej, znany z lekcji 0.2: jeśli nazwa jest **aliasem**, PowerShell najpierw zamienia ją na właściwe polecenie.

Za chwilę sprawdzisz, która możliwość zachodzi dla poleceń, których już używasz.

## 2. Wypróbuj: uruchom program

Wpisz polecenie (takie samo w każdym systemie):

```text
whoami
```

Nazwa pochodzi z angielskiego *who am I?*, czyli „kim jestem?”. **Przewidź**, co pokaże terminal, i sprawdź.

| System | Przykładowy wynik |
|---|---|
| Windows | `laptop\ola` |
| macOS i Linux | `ola` |

Zobaczysz nazwę swojego konta. Na Windowsie jest przed nią nazwa komputera i znak `\`. To nie ścieżka, tylko zapis „komputer\konto”.

Ten wynik przygotował **program** `whoami`: zapytał system, kto jest zalogowany, i wypisał odpowiedź w terminalu.

## 3. Eksperyment: zapytaj powłokę, czym jest polecenie

Powłoka może Ci powiedzieć, co kryje się pod daną nazwą. Służy do tego inne polecenie w każdym systemie:

| Windows (PowerShell) | macOS i Linux |
|---|---|
| `Get-Command whoami` | `type whoami` |

Wynik na Windowsie:

```text
CommandType     Name                Version    Source
-----------     ----                -------    ------
Application     whoami.exe          10.0.26... C:\Windows\system32\whoami.exe
```

Wynik na macOS i Linuksie (przykład):

```text
whoami is /usr/bin/whoami
```

Obie odpowiedzi mówią to samo: `whoami` to **osobny program**, a powłoka podaje ścieżkę do jego pliku. Na Windowsie wskazuje na to `Application` w kolumnie `CommandType`. Kolumnę `Version` możesz pominąć. Ścieżka na Twoim komputerze może wyglądać trochę inaczej.

**Przewidź:** co powłoka powie o `cd`? Czy znajdzie dla niego plik? Sprawdź:

| Windows (PowerShell) | macOS i Linux |
|---|---|
| `Get-Command cd` | `type cd` |

- **macOS i Linux:** `cd is a shell builtin`, czyli polecenie wbudowane w powłokę. Nie ma żadnego pliku.
- **Windows:** `Alias` i `cd -> Set-Location`. Sprawdź jeszcze `Get-Command Set-Location`. Zobaczysz `Cmdlet`, czyli polecenie wbudowane w PowerShell. W kolumnie `Source` nie ma ścieżki do pliku, tylko nazwa części PowerShella.

**Wniosek:** „polecenie” nie znaczy „plik”. Część poleceń to umiejętności samej powłoki, a część uruchamia osobne programy.

## 4. Zastosuj: program to plik

Skoro `whoami` to plik, można go uruchomić, podając pełną ścieżkę. Wpisz ścieżkę, którą pokazała Ci powłoka w punkcie 3, na przykład:

| Windows | macOS i Linux |
|---|---|
| `C:\Windows\system32\whoami.exe` | `/usr/bin/whoami` |

Wynik jest taki sam jak po wpisaniu samego `whoami`. Na Windowsie nazwy programów zwykle kończą się na `.exe`, ale wpisując polecenie, można tę końcówkę pominąć.

Skąd powłoka wiedziała, gdzie szukać, gdy wpisano samo `whoami`? Ma listę katalogów, w których szuka programów. Ta lista nazywa się **`PATH`**. Nie musisz jej teraz oglądać ani zmieniać.

To ważne na najbliższe lekcje. Gdy zainstalujesz kompilator, instalator zwykle dopisze jego katalog do tej listy. Wtedy wystarczy wpisać jego nazwę, tak jak `whoami`. Twój własny program będzie natomiast leżał w Twoim katalogu, którego na liście nie ma. Dlatego uruchomisz go, podając ścieżkę. Zobaczysz to pod koniec modułu.

## 5. Zrozum: program a kod źródłowy

Plik `whoami` nie jest tekstem, który da się wygodnie przeczytać. Zawiera instrukcje dla komputera, a nie dla człowieka. Nie musisz go otwierać.

Ktoś kiedyś napisał ten program jako zwykły tekst w **języku programowania**. Taki tekst to **kod źródłowy**. Potem specjalne narzędzie, **kompilator**, zamieniło kod źródłowy w plik wykonywalny:

```text
kod źródłowy (tekst)  →  kompilator  →  program (plik wykonywalny)  →  uruchomienie  →  wynik w terminalu
```

To dwa różne pliki:

- **Kod źródłowy** czytasz i zmieniasz. To tekst, podobnie jak `lista.txt` z lekcji 0.1.
- **Program** uruchamiasz. Zmiana kodu źródłowego nie zmienia programu, dopóki kompilator nie zbuduje go od nowa.

Właśnie tego nauczysz się w tym kursie: pisać kod źródłowy w C++ i zamieniać go w działający program. W kolejnych lekcjach przygotujesz potrzebne narzędzia, czyli kompilator i CLion. Na końcu tego modułu uruchomisz pierwszy program w C++.

## 6. Misja: detektyw poleceń

Sprawdź cztery polecenia, których już używasz: `pwd`, `cd`, `ls` i `whoami`. Dla każdego najpierw **przewidź**, czym jest, a potem sprawdź poleceniem `Get-Command` (Windows) albo `type` (macOS, Linux).

| Polecenie | Twoje przewidywanie | Co pokazała powłoka | Rodzaj: wbudowane, alias czy osobny program? |
|---|---|---|---|
| `pwd` | | | |
| `cd` | | | |
| `ls` | | | |
| `whoami` | | | |

Na koniec odpowiedz w dwóch, trzech zdaniach: **skąd wziął się wynik polecenia `whoami`?**

### Kryterium sukcesu

- Rodzaj w każdym wierszu zgadza się z tym, co pokazała powłoka **na Twoim komputerze**. Wyniki mogą się różnić między systemami i to jest w porządku.
- W tabeli jest co najmniej jedno polecenie, za którym nie stoi osobny plik, i co najmniej jedno, które jest osobnym programem.
- Odpowiedź o `whoami` mówi, że powłoka uruchomiła osobny program (plik), a to ten program wypisał wynik.

Nie musisz zapamiętywać ścieżek do programów. Na różnych komputerach mogą być inne.

<details>
<summary>Typowe wyniki</summary>

| Polecenie | Windows (PowerShell) | macOS (zsh) | Linux (bash, np. Ubuntu) |
|---|---|---|---|
| `pwd` | alias (`Get-Location`, wbudowane w PowerShell) | wbudowane | wbudowane |
| `cd` | alias (`Set-Location`, wbudowane w PowerShell) | wbudowane | wbudowane |
| `ls` | alias (`Get-ChildItem`, wbudowane w PowerShell) | osobny program, np. `/bin/ls` | zwykle alias (`ls --color=auto`), który uruchamia osobny program `ls` |
| `whoami` | osobny program, `whoami.exe` | osobny program | osobny program |

To samo słowo `ls` jest więc na Windowsie poleceniem PowerShella, a na macOS osobnym programem. Tak jak w lekcji 0.2: ta sama nazwa nie oznacza tego samego narzędzia.

</details>

## 7. Gdy coś pójdzie inaczej

| Co widzisz | Co to znaczy | Co zrobić |
|---|---|---|
| Windows: po `type whoami` komunikat `Cannot find path '…\whoami' because it does not exist.` | W PowerShellu `type` to alias zupełnie innego polecenia (`Get-Content`), które pokazuje zawartość pliku. | Na Windowsie używaj `Get-Command`. |
| macOS i Linux: `command not found: Get-Command` albo `Get-Command: command not found` | `Get-Command` to polecenie PowerShella. | Na macOS i Linuksie używaj `type`. |
| Linux (bash): `whoami is hashed (/usr/bin/whoami)` | Bash zapamiętał, gdzie znalazł ten program. To wciąż osobny plik. | Nic nie trzeba robić. |
| Linux: ``ls is aliased to `ls --color=auto'`` | `ls` to tu alias: system dodaje opcję, dzięki której `ls` koloruje wyniki. Pod spodem i tak uruchamia się program `ls`. | Zapisz w misji „alias”. |
| Komunikat `type` po polsku, na przykład że polecenie jest wbudowane w powłokę | Bash tłumaczy komunikaty na język systemu. | Liczy się znaczenie komunikatu, nie jego język. |
| Windows: `The term '…' is not recognized…`<br>macOS i Linux: `… not found` | Powłoka nie zna takiego polecenia: nie jest wbudowane i nie znalazła programu o tej nazwie. | Sprawdź pisownię. Ten sam komunikat może się pojawić po instalacji narzędzia, jeśli coś poszło nie tak. Wrócimy do tego przy instalacji. |
| Ścieżka do programu jest inna niż w przykładzie, na przykład `/usr/bin/ls` zamiast `/bin/ls` | Systemy różnie układają swoje katalogi. | Nic nie trzeba robić. Liczy się to, że w ogóle jest ścieżka do pliku. |

## 8. Wyjaśnij

Odpowiedz własnymi słowami, najlepiej na głos albo na kartce. Dopiero potem rozwiń odpowiedź.

**1.** Wpisujesz `cd krakow`, a potem `whoami`. Oba polecenia wpisuje się tak samo. Co innego dzieje się po naciśnięciu <kbd>Enter</kbd> w każdym z tych przypadków?

<details>
<summary>Odpowiedź</summary>

`cd` wykonuje sama powłoka (na Windowsie przez alias do polecenia wbudowanego w PowerShell). `whoami` to osobny program: powłoka znajduje jego plik i go uruchamia, a wynik wypisuje sam program.

</details>

**2.** Ktoś twierdzi: „Każde polecenie to plik gdzieś na dysku”. Czy ma rację? Podaj przykład ze swojego systemu.

<details>
<summary>Odpowiedź</summary>

Nie. `cd` nie ma swojego pliku: na macOS i Linuksie jest wbudowane w powłokę, a na Windowsie to alias polecenia wbudowanego w PowerShell. Plik ma na przykład `whoami`.

</details>

**3.** Dlaczego można wpisać samo `whoami`, bez pełnej ścieżki? Co musi się stać, żeby po zainstalowaniu kompilatora dało się go uruchomić tak samo, samą nazwą?

<details>
<summary>Odpowiedź</summary>

Powłoka szuka programów w katalogach z listy `PATH`, a katalog z `whoami` jest na tej liście. Katalog z kompilatorem też musi się na niej znaleźć. Zwykle robi to instalator.

</details>

**4.** Masz plik z kodem źródłowym w C++. Czy można go od razu uruchomić jak `whoami`? Czego brakuje?

<details>
<summary>Odpowiedź</summary>

Nie. Kod źródłowy to tekst dla człowieka. Najpierw kompilator musi zamienić go w plik wykonywalny, i dopiero ten plik można uruchomić.

</details>

## Podsumowanie

- **Polecenie** to tekst przekazywany powłoce. Powłoka wykonuje je sama (polecenie **wbudowane**), zamienia alias na właściwe polecenie albo uruchamia **osobny program**.
- **Program** (plik wykonywalny) to plik z instrukcjami, które komputer potrafi wykonać. Wynik, który widzisz, wypisuje sam program.
- Nie każde polecenie jest plikiem. Sprawdzisz to poleceniem `Get-Command` (Windows) albo `type` (macOS, Linux).
- Programy można uruchamiać po nazwie, bo powłoka szuka ich w katalogach z listy `PATH`.
- **Kod źródłowy** to tekst napisany przez człowieka. **Kompilator** zamienia go w program.

**Poprzednia lekcja:** [Lekcja 0.2: Poruszanie się między katalogami](lesson_02_moving_between_folders.md) · **Następna lekcja:** [Lekcja 0.4: Przygotuj warsztat: instalacja narzędzi](lesson_04_installing_the_tools.md) · [Opis kursu](../../README.md)

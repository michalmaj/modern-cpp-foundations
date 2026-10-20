# Lekcja 0.1: Pliki, katalogi i pierwsze spotkanie z terminalem

**Polski** · [English](lesson_01_files_and_terminal.en.md) · [Opis kursu](../../README.md)

> **Moduł 0, lekcja 1** · około 30–45 minut
> **Potrzebujesz:** komputera z Windows, macOS albo Linuksem. Nie musisz niczego instalować.

## Sytuacja

Pobierasz z internetu bilet na koncert. Przeglądarka pokazuje „Pobrano”, zamykasz ją i… gdzie właściwie jest teraz ten plik?

Komputer wie to dokładnie. W tej lekcji nauczysz się go o to pytać tak, jak robią to programiści: wpisując polecenia w **terminalu**.

Po tej lekcji będziesz:

- odróżniać plik od katalogu;
- rozumieć, czym jest ścieżka;
- wiedzieć, do czego służą terminal i powłoka;
- umieć otworzyć terminal w swoim systemie;
- umieć sprawdzić, w jakim katalogu jesteś, i wyświetlić jego zawartość.

## 1. Zrozum: pliki, katalogi i ścieżki

**Plik** to porcja danych zapisana pod jakąś nazwą: zdjęcie, dokument, piosenka, program.

**Katalog** (inaczej **folder**, oba słowa znaczą to samo) to nazwany pojemnik, w którym leżą pliki i inne katalogi. Plik nie może zawierać innych plików, a katalog może.

Katalogi umieszczone w katalogach tworzą drzewo:

```text
ola                    ← katalog
├── Documents          ← katalog
│   └── bilet.pdf      ← plik
├── Downloads          ← katalog
└── Pictures           ← katalog
    └── wakacje.jpg    ← plik
```

`ola` to tu przykładowy **katalog domowy**, czyli katalog, który system przydziela każdej osobie korzystającej z komputera. Na Twoim komputerze nazywa się on inaczej, zwykle tak jak Twoje konto.

**Ścieżka** to adres pliku albo katalogu. Zapisuje się w niej kolejne katalogi, od początku dysku aż do celu, oddzielone specjalnym znakiem, czyli **separatorem**. Ścieżka do biletu wygląda tak:

| System | Ścieżka do `bilet.pdf` |
|---|---|
| Windows | `C:\Users\ola\Documents\bilet.pdf` |
| macOS | `/Users/ola/Documents/bilet.pdf` |
| Linux | `/home/ola/Documents/bilet.pdf` |

Czytaj ścieżkę od lewej do prawej. Na Windowsie: „na dysku `C:`, w katalogu `Users`, w katalogu `ola`, w katalogu `Documents` jest plik `bilet.pdf`”. Na Windowsie separatorem jest `\`, a na macOS i Linuksie `/`. Ścieżki na macOS i Linuksie zaczynają się od samego `/`, czyli od początku dysku.

<details>
<summary>Sprawdź się: jak wygląda ścieżka do <code>wakacje.jpg</code> w Twoim systemie?</summary>

- Windows: `C:\Users\ola\Pictures\wakacje.jpg`
- macOS: `/Users/ola/Pictures/wakacje.jpg`
- Linux: `/home/ola/Pictures/wakacje.jpg`

</details>

## 2. Zrozum: terminal i powłoka

Na co dzień obsługujesz komputer myszką: klikasz ikony i otwierasz okna. Można też inaczej: **wpisać polecenie** i przeczytać odpowiedź komputera. Do tego służy terminal.

- **Terminal** to okno, w którym wpisujesz polecenia i czytasz odpowiedzi.
- **Powłoka** (ang. *shell*) to program działający w tym oknie. Odczytuje Twoje polecenie, wykonuje je i wypisuje wynik. Na Windowsie używamy powłoki **PowerShell**. Na macOS domyślna powłoka to **zsh**, a na Linuksie zwykle **bash**.

Po co to wszystko, skoro jest myszka? Większość narzędzi programisty obsługuje się właśnie poleceniami, w tym narzędzie, które zamienia napisany tekst w działający program. Poznasz je w tym kursie. Terminal pokazuje też dokładnie, co się wydarzyło i w którym miejscu na dysku.

Powłoka zawsze „jest” w jakimś katalogu, tak jak okno plików zawsze pokazuje jeden katalog naraz. Ten katalog to **bieżący katalog**. Polecenia działają w nim, chyba że wskażesz inne miejsce.

## 3. Wypróbuj: otwórz terminal

| System | Jak otworzyć terminal |
|---|---|
| Windows 11 | Otwórz menu Start, wpisz `Terminal` i uruchom aplikację **Terminal**. |
| Windows 10 | Otwórz menu Start, wpisz `PowerShell` i uruchom **Windows PowerShell**. |
| macOS | Naciśnij <kbd>⌘ Cmd</kbd> + <kbd>Spacja</kbd>, wpisz `Terminal` i naciśnij <kbd>Enter</kbd>. |
| Linux | Zależy od systemu. Na Ubuntu naciśnij <kbd>Ctrl</kbd> + <kbd>Alt</kbd> + <kbd>T</kbd> albo wyszukaj **Terminal** wśród aplikacji. |

Zobaczysz okno z krótkim tekstem i migającym kursorem, na przykład:

```text
PS C:\Users\ola>              ← Windows
ola@MacBook-Air ~ %           ← macOS
ola@laptop:~$                 ← Linux
```

To **znak zachęty** (ang. *prompt*): powłoka czeka na polecenie. Na Twoim komputerze wygląda trochę inaczej. Nie przepisuj go: w tej lekcji wpisujesz tylko to, co pokazujemy jako polecenie. Na macOS i Linuksie znak `~` w znaku zachęty oznacza katalog domowy.

> **Windows:** znak zachęty powinien zaczynać się od `PS`. Jeśli nie, to otworzyło się okno innej powłoki („Wiersz polecenia”). Zamknij je i otwórz Terminal albo PowerShell.

Polecenia w tej lekcji są krótkie, więc wpisuj je ręcznie. Każde zatwierdzasz klawiszem <kbd>Enter</kbd>.

## 4. Wypróbuj: gdzie jestem?

Zanim cokolwiek wpiszesz, zastanów się: w jakim katalogu jest teraz Twoja powłoka?

Wpisz polecenie (takie samo w każdym systemie):

```text
pwd
```

`pwd` to skrót od *print working directory*, czyli „wypisz bieżący katalog”. Wynik wygląda mniej więcej tak.

Windows:

```text
Path
----
C:\Users\ola
```

macOS: `/Users/ola`. Linux: `/home/ola`.

W Twoim wyniku będzie nazwa Twojego katalogu domowego, i tak ma być. Ważne, że to **ścieżka**: adres miejsca, w którym jesteś. Nowo otwarty terminal zwykle zaczyna w katalogu domowym.

## 5. Wypróbuj: co tu jest?

Teraz wyświetl zawartość bieżącego katalogu. Tu polecenia różnią się między systemami:

| Windows (PowerShell) | macOS i Linux |
|---|---|
| `ls` | `ls -F` |

`ls` to skrót od *list*, czyli „wypisz”. Na macOS i Linuksie dopisek `-F` to **opcja**: prosi `ls`, żeby oznaczył katalogi znakiem `/` na końcu nazwy. Na Windowsie tej opcji nie dodawaj, bo PowerShell pokazuje rodzaj elementu w osobnej kolumnie.

Wynik na Windowsie (fragment):

```text
    Directory: C:\Users\ola

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-----        10/20/2026   9:12 AM                Desktop
d-----        10/20/2026   9:12 AM                Documents
d-----        10/20/2026   9:12 AM                Downloads
```

Wynik na macOS albo Linuksie (przykład):

```text
Desktop/    Documents/  Downloads/  Music/      Pictures/
```

Jak to czytać:

- **Windows:** jeśli kolumna `Mode` zaczyna się od `d` (od *directory*), to jest katalog. Jeśli zaczyna się od `-`, to jest plik. Pozostałe kolumny na razie możesz pominąć.
- **macOS i Linux:** `/` na końcu nazwy oznacza katalog, a nazwa bez `/` to plik. Jeśli zobaczysz na końcu inne znaki, na przykład `*` albo `@`, na razie je pomiń.

Twoja lista będzie inna niż w przykładzie. Daty i układ kolumn też mogą wyglądać inaczej. Najpewniej zobaczysz same katalogi, bo w katalogu domowym rzadko leżą luźne pliki. To się zaraz zmieni.

## 6. Zastosuj: terminal i okno plików pokazują to samo miejsce

Wpisz polecenie, które otworzy bieżący katalog w zwykłym oknie plików:

| Windows | macOS | Linux |
|---|---|---|
| `explorer .` | `open .` | `xdg-open .` |

Kropka `.` to najkrótsza możliwa ścieżka: oznacza „bieżący katalog”. Całe polecenie znaczy więc „otwórz w oknie plików katalog, w którym teraz jestem”.

Porównaj okno z wynikiem `ls`: widzisz te same katalogi. Okno plików i terminal to dwa sposoby patrzenia na te same dane na dysku.

Drobne różnice są normalne. Na przykład na macOS `ls -F` pokazuje katalog `Library/`, który Finder ukrywa. A okno plików może wyświetlać przetłumaczone nazwy (więcej w punkcie 9).

Teraz w tym oknie utwórz nowy katalog o nazwie `pierwszy-eksperyment`:

- **Windows:** kliknij prawym przyciskiem myszy puste miejsce, wybierz **Nowy → Folder**, wpisz nazwę i naciśnij <kbd>Enter</kbd>.
- **macOS:** kliknij prawym przyciskiem myszy puste miejsce, wybierz **Nowy folder**, wpisz nazwę i naciśnij <kbd>Enter</kbd>.
- **Linux:** kliknij prawym przyciskiem myszy puste miejsce, wybierz **Nowy katalog** (albo **Nowy folder**), wpisz nazwę i zatwierdź.

Nazwa nie ma spacji ani polskich liter celowo: takie nazwy łatwiej wpisuje się w terminalu.

**Przewidź, zanim sprawdzisz:** czy `pierwszy-eksperyment` pojawi się w wyniku `ls`? Po czym poznasz, że to katalog, a nie plik?

Wróć do terminala i jeszcze raz wpisz `ls` (Windows) albo `ls -F` (macOS, Linux). Wśród wyników powinien być nowy katalog:

- Windows: wiersz z `d-----` w kolumnie `Mode` i nazwą `pierwszy-eksperyment`;
- macOS i Linux: `pierwszy-eksperyment/`.

## 7. Zadanie: miejsce na plan wyjazdu

Planujesz wyjazd. W katalogu `pierwszy-eksperyment` potrzebujesz katalogu na notatki i pustego pliku na listę rzeczy do spakowania.

**Krok 1.** W oknie plików wejdź do katalogu `pierwszy-eksperyment` i utwórz w nim katalog `notatki`, tak jak poprzednio.

**Krok 2.** Plik utworzysz z terminala. Nie zmieniaj bieżącego katalogu (to wciąż Twój katalog domowy) i wpisz:

| Windows | macOS i Linux |
|---|---|
| `New-Item pierwszy-eksperyment\lista.txt` | `touch pierwszy-eksperyment/lista.txt` |

Zwróć uwagę na ścieżkę `pierwszy-eksperyment\lista.txt`. Czytasz ją tak: „w katalogu `pierwszy-eksperyment` plik `lista.txt`”. Nie zaczyna się od `C:\` ani od `/`, więc powłoka szuka katalogu `pierwszy-eksperyment` w bieżącym katalogu. Taka ścieżka to **ścieżka względna**: liczy się od miejsca, w którym jesteś. Ścieżki, które wypisuje `pwd`, zaczynają się od początku dysku. To **ścieżki bezwzględne**.

Na Windowsie `New-Item` od razu wypisze informację o nowym pliku. Wartość `0` w kolumnie `Length` oznacza, że plik jest pusty. Na macOS i Linuksie `touch` nic nie wypisuje, jeśli wszystko się udało.

> Polecenia są bezpieczne. Jeśli plik `lista.txt` już istnieje, `New-Item` zgłosi błąd i niczego nie zmieni, a `touch` nie ruszy jego zawartości.

**Krok 3.** Sprawdź wynik, nie otwierając okna plików:

| Windows | macOS i Linux |
|---|---|
| `ls pierwszy-eksperyment` | `ls -F pierwszy-eksperyment` |

### Kryterium sukcesu

Wynik pokazuje **dokładnie dwa elementy**: katalog `notatki` i plik `lista.txt`.

Windows:

```text
    Directory: C:\Users\ola\pierwszy-eksperyment

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-----        10/20/2026   9:30 AM                notatki
-a----        10/20/2026   9:31 AM              0 lista.txt
```

macOS i Linux:

```text
lista.txt  notatki/
```

Kolejność może być inna, a na Windowsie w kolumnie `Mode` może być mniej kresek. Liczy się to, że `notatki` jest oznaczone jako katalog (`d` albo `/`), a `lista.txt` jako plik.

## 8. Sprawdź: zbuduj pełną ścieżkę

Zapisz **ścieżkę bezwzględną** do pliku `lista.txt` na swoim komputerze. Weź wynik `pwd` i dopisz do niego kolejne nazwy, oddzielone separatorem Twojego systemu.

Potem sprawdź, czy ścieżka jest poprawna:

| Windows | macOS i Linux |
|---|---|
| `ls C:\Users\ola\pierwszy-eksperyment\lista.txt` | `ls -F /Users/ola/pierwszy-eksperyment/lista.txt` |

To przykłady dla katalogu domowego `ola`. Wpisz swoją ścieżkę. Na Linuksie zaczyna się ona zwykle od `/home/`.

- Jeśli ścieżka jest poprawna, zobaczysz plik `lista.txt`.
- Jeśli nie, powłoka zgłosi, że nie może znaleźć takiej ścieżki. Porównaj wtedy swoją ścieżkę z wynikiem `pwd`, litera po literze.

> **Windows:** jeśli w ścieżce jest spacja (na przykład `C:\Users\Jan Kowalski`), weź całą ścieżkę w cudzysłów:
> `ls "C:\Users\Jan Kowalski\pierwszy-eksperyment\lista.txt"`

## 9. Gdy coś pójdzie inaczej

Najpierw **przeczytaj komunikat**. Zwykle mówi, czego powłoka nie zrozumiała albo czego nie znalazła, i cytuje to, co wpisano. Popraw jedną rzecz i spróbuj ponownie. Komunikaty mogą być po angielsku albo po polsku, zależnie od ustawień systemu.

| Co widzisz | Co to znaczy | Co zrobić |
|---|---|---|
| Windows: `The term 'lss' is not recognized…`<br>macOS: `zsh: command not found: lss`<br>Linux: `lss: command not found` | Powłoka nie zna polecenia o takiej nazwie. Najczęściej to literówka. | Porównaj wpisane polecenie z lekcją, znak po znaku. |
| Windows: `…the parameter name 'F' is ambiguous…` | Na Windowsie wpisano polecenie w wersji dla macOS i Linuksa. | Na Windowsie wpisz samo `ls`. |
| Windows: `Cannot find path '…' because it does not exist.`<br>macOS i Linux: `No such file or directory` | Pod podaną ścieżką nic nie ma. Albo nazwa jest inna, albo jesteś w innym katalogu, niż myślisz. | Sprawdź `pwd` i pisownię nazwy. Na Windowsie komunikat pokazuje pełną ścieżkę, której szukała powłoka, więc porównaj ją z wynikiem `pwd`. |
| Windows: znak zachęty nie zaczyna się od `PS`, a `pwd` jest nieznanym poleceniem | Otworzył się „Wiersz polecenia”, czyli inna powłoka. | Otwórz Terminal albo PowerShell (zobacz punkt 3). |
| Okno plików pokazuje inne nazwy niż terminal, na przykład **Pobrane** zamiast `Downloads` albo **Użytkownicy** zamiast `Users` | Windows i macOS mogą wyświetlać przetłumaczone nazwy katalogów. Terminal pokazuje prawdziwe nazwy. To te same katalogi. | Nic nie trzeba robić. Na Linuksie w polskiej wersji systemu prawdziwe nazwy mogą być po polsku, i wtedy terminal też je tak pokaże. |
| `pierwszy-eksperyment` nie pojawia się w wyniku `ls` | Katalog powstał w innym miejscu albo ma inną nazwę, na przykład „Nowy folder”. | Otwórz okno poleceniem z punktu 6 i sprawdź, czy katalog tam jest i jak się nazywa. |
| Linux: `xdg-open` nie działa | Twój system nie ma tego polecenia. | Otwórz okno plików ręcznie (na przykład aplikację **Pliki**) i przejdź do katalogu domowego (zwykle **Katalog domowy** albo **Home**). Nie używaj na Linuksie `open`, bo to zupełnie inne polecenie. |
| macOS pyta, czy Terminal może uzyskać dostęp do plików w jakimś katalogu | System chroni niektóre katalogi, na przykład `Documents`. | W tej lekcji nie jest to potrzebne. Możesz odmówić. |

## 10. Wyjaśnij

Odpowiedz własnymi słowami, najlepiej na głos albo na kartce. Dopiero potem rozwiń odpowiedź.

**1.** Ola na Windowsie i Bartek na macOS wpisują `pwd` i dostają zupełnie różne wyniki. Czy ktoś z nich popełnił błąd? Co łączy oba wyniki?

<details>
<summary>Odpowiedź</summary>

Nikt nie popełnił błędu. Oba wyniki są ścieżkami bezwzględnymi do bieżącego katalogu, zwykle katalogu domowego. Różnią się, bo każde z nich ma inną nazwę konta, a ich systemy inaczej zapisują ścieżki: Windows zaczyna od litery dysku i używa `\`, macOS zaczyna od `/` i używa `/`.

</details>

**2.** Polecenie `ls pierwszy-eksperyment` (albo `ls -F pierwszy-eksperyment`) zadziałało, gdy bieżącym katalogiem był katalog domowy. Co by się stało, gdyby bieżącym katalogiem był `Downloads`? Jak zapisać polecenie, żeby działało bez względu na bieżący katalog?

<details>
<summary>Odpowiedź</summary>

Powłoka zgłosiłaby, że nie znalazła takiej ścieżki. `pierwszy-eksperyment` to ścieżka względna, więc powłoka szuka jej w bieżącym katalogu, a w `Downloads` takiego katalogu nie ma. Ścieżka bezwzględna, na przykład `C:\Users\ola\pierwszy-eksperyment` albo `/Users/ola/pierwszy-eksperyment`, działa bez względu na bieżący katalog.

</details>

**3.** Po czym w terminalu rozpoznajesz, że `notatki` to katalog, a `lista.txt` to plik? Czy wystarczy sprawdzić, czy w nazwie jest kropka?

<details>
<summary>Odpowiedź</summary>

Po oznaczeniu, które dodaje terminal: `d` w kolumnie `Mode` na Windowsie albo `/` na końcu nazwy na macOS i Linuksie. Kropka w nazwie niczego nie przesądza. Końcówka `.txt` to tylko część nazwy. Katalog może nazywać się `wersja.2`, a plik może nie mieć kropki w ogóle.

</details>

**4.** Bieżący katalog przez cały czas był katalogiem domowym. Dlaczego więc plik `lista.txt` powstał w katalogu `pierwszy-eksperyment`?

<details>
<summary>Odpowiedź</summary>

Bo polecenie dostało ścieżkę `pierwszy-eksperyment\lista.txt` (albo `pierwszy-eksperyment/lista.txt`). Bieżący katalog to tylko punkt startowy ścieżki względnej: powłoka zaczęła od katalogu domowego, weszła do `pierwszy-eksperyment` i tam utworzyła plik.

</details>

## Podsumowanie

- **Plik** przechowuje dane. **Katalog** przechowuje pliki i inne katalogi.
- **Ścieżka** to adres. Ścieżka **bezwzględna** zaczyna się od początku dysku, a **względna** od bieżącego katalogu.
- **Terminal** to okno do wpisywania poleceń, a **powłoka** to program, który je wykonuje.
- Powłoka zawsze ma **bieżący katalog**.

| Do czego | Windows (PowerShell) | macOS | Linux |
|---|---|---|---|
| Pokaż bieżący katalog | `pwd` | `pwd` | `pwd` |
| Pokaż zawartość katalogu | `ls` | `ls -F` | `ls -F` |
| Otwórz bieżący katalog w oknie plików | `explorer .` | `open .` | `xdg-open .` |
| Utwórz pusty plik | `New-Item ścieżka` | `touch ścieżka` | `touch ścieżka` |

Katalog `pierwszy-eksperyment` możesz zostawić albo usunąć w oknie plików. Trafi wtedy do Kosza. Usuwania z terminala celowo jeszcze nie używamy: kasuje ono od razu, z pominięciem Kosza.

Następna lekcja jest w przygotowaniu. Wróć do [opisu kursu](../../README.md).

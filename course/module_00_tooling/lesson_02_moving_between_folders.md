# Lekcja 0.2: Poruszanie się między katalogami

**Polski** · [English](lesson_02_moving_between_folders.en.md) · [Opis kursu](../../README.md)

> **Moduł 0, lekcja 2** · około 30–40 minut
> **Potrzebujesz:** komputera z Windows, macOS albo Linuksem. Nie musisz niczego instalować.

## Zanim zaczniesz

Ta lekcja zakłada, że po [lekcji 0.1](lesson_01_files_and_terminal.md) wiesz:

- czym różni się plik od katalogu;
- czym jest ścieżka oraz czym różni się ścieżka względna od bezwzględnej;
- jak otworzyć terminal;
- co robią `pwd` i `ls` (na macOS i Linuksie: `ls -F`).

Jeśli coś z tego brzmi obco, wróć na chwilę do lekcji 0.1. Plików z tamtej lekcji nie potrzebujesz: wszystko, czego użyjesz, przygotujesz od nowa.

## Sytuacja

W lekcji 0.1, żeby zajrzeć do katalogu `pierwszy-eksperyment`, wpisywało się jego nazwę w każdym poleceniu: `ls pierwszy-eksperyment`. Przy jednym katalogu to nie problem. A teraz wyobraź sobie katalog ukryty trzy poziomy głębiej i dziesięć poleceń z rzędu, każde z tą samą długą ścieżką.

W oknie plików po prostu klikasz dwukrotnie katalog i jesteś w środku. W terminalu też da się „wejść” do katalogu. Tego nauczysz się w tej lekcji.

Po tej lekcji będziesz:

- zmieniać bieżący katalog poleceniem `cd`;
- przechodzić do katalogu nadrzędnego poleceniem `cd ..`;
- rozumieć, co znaczą `.` i `..` w ścieżkach;
- wiedzieć, że zmiana bieżącego katalogu niczego nie przenosi na dysku;
- przewidywać, co pokażą `pwd` i `ls` po przejściu do innego katalogu;
- docierać do wskazanego katalogu, korzystając ze ścieżek względnych i bezwzględnych.

## 1. Zrozum: zmiana bieżącego katalogu

Z lekcji 0.1 wiesz, że powłoka zawsze jest w jakimś **bieżącym katalogu** i że od niego liczą się ścieżki względne.

Polecenie **`cd`** (od *change directory*, czyli „zmień katalog”) zmienia ten bieżący katalog. Po słowie `cd` podajesz ścieżkę do katalogu, do którego chcesz przejść.

Ważne: `cd` **niczego nie przenosi**. To jak chodzenie po budynku: Ty zmieniasz pokój, a pokoje zostają na swoich miejscach. Zmienia się tylko jedno: punkt, od którego powłoka liczy ścieżki względne.

Jeśli wszystko się uda, `cd` niczego nie wypisuje. Dlatego po każdym przejściu sprawdzaj, gdzie jesteś, poleceniem `pwd`.

## 2. Wypróbuj: wróć do domu

Terminal nie zawsze startuje w katalogu domowym. Zależy to od systemu, ustawień i tego, skąd go uruchomiono. Dlatego najpierw przejdź do miejsca, które na pewno znasz:

```text
cd ~
```

Znak `~` (tylda) oznacza Twój katalog domowy. Polecenie działa tak samo w PowerShellu, w zsh i w bashu.

**Przewidź:** co pokaże teraz `pwd`? Wpisz `pwd` i sprawdź.

Powinna się pokazać ścieżka do Twojego katalogu domowego, na przykład `C:\Users\ola`, `/Users/ola` albo `/home/ola`. Jeśli kiedykolwiek się zgubisz, `cd ~` zawsze zabierze Cię z powrotem.

## 3. Przygotuj: mały plan podróży

Do ćwiczeń potrzebujesz niewielkiego drzewa katalogów. Planujesz wyjazd do Krakowa i Gdańska:

```text
plan-podrozy
├── krakow
│   └── muzea
└── gdansk
    └── plaze
```

Utworzysz je myszką, tak jak w lekcji 0.1. Najpierw otwórz katalog domowy w oknie plików (jesteś w nim po `cd ~`):

| Windows | macOS | Linux |
|---|---|---|
| `explorer .` | `open .` | `xdg-open .` |

Potem w oknie plików:

1. Utwórz katalog `plan-podrozy` i wejdź do niego (kliknij go dwukrotnie).
2. W środku utwórz dwa katalogi: `krakow` i `gdansk`.
3. Wejdź do `krakow` i utwórz w nim `muzea`.
4. Wróć poziom wyżej (strzałką „Wstecz” w oknie), wejdź do `gdansk` i utwórz w nim `plaze`.

Nazwy celowo nie mają polskich liter.

> Jeśli `plan-podrozy` już istnieje, bo robisz tę lekcję drugi raz, sprawdź, czy ma powyższe katalogi, i dodaj brakujące.

Sprawdź w terminalu, czy wszystko jest na miejscu:

| Windows | macOS i Linux |
|---|---|
| `ls plan-podrozy` | `ls -F plan-podrozy` |

Powinny się pokazać dwa katalogi: `gdansk` i `krakow`.

## 4. Eksperyment: wejdź do katalogu

Jesteś w katalogu domowym.

**Przewidź:** co się stanie, jeśli wpiszesz `ls krakow` (Windows) albo `ls -F krakow` (macOS, Linux)?

Sprawdź. Powłoka zgłosi błąd: nie znajdzie takiej ścieżki. To nie jest pomyłka w lekcji. Ścieżka `krakow` jest względna, więc powłoka szuka jej w bieżącym katalogu, czyli w katalogu domowym. A `krakow` leży w `plan-podrozy`.

Teraz wejdź do `plan-podrozy`:

```text
cd plan-podrozy
```

**Przewidź**, co pokaże `pwd`, i sprawdź. Na końcu ścieżki powinno być teraz `plan-podrozy`.

Wpisz jeszcze raz `ls krakow` (albo `ls -F krakow`). Tym razem zobaczysz katalog `muzea`. Polecenie jest identyczne jak przed chwilą, ale bieżący katalog jest inny, więc ta sama ścieżka względna prowadzi gdzie indziej.

Zerknij też na znak zachęty. Często pokazuje, gdzie jesteś, na przykład `PS C:\Users\ola\plan-podrozy>` na Windowsie. Zależnie od systemu może pokazywać całą ścieżkę albo tylko ostatnią nazwę. Pewną odpowiedź daje zawsze `pwd`.

## 5. Eksperyment: w górę, czyli `..`

Z lekcji 0.1 znasz już `.`, czyli „bieżący katalog”. Jego partnerem są **dwie kropki** `..`, czyli **katalog nadrzędny**: ten, który zawiera bieżący katalog. Katalogiem nadrzędnym dla `plan-podrozy` jest Twój katalog domowy.

**Przewidź:** jesteś w `plan-podrozy`. Gdzie trafisz po `cd ..`? Sprawdź: `cd ..`, a potem `pwd`. Między `cd` a `..` musi być spacja.

Teraz zejdź kilka poziomów w dół jednym poleceniem. Ścieżka może składać się z kilku nazw, tak jak w lekcji 0.1:

| Windows | macOS i Linux |
|---|---|
| `cd plan-podrozy\krakow\muzea` | `cd plan-podrozy/krakow/muzea` |

**Przewidź** wynik `pwd` i sprawdź.

Teraz trudniejsze pytanie. Jesteś w `muzea`. **Przewidź**, co pokaże `ls ..` (na macOS i Linuksie `ls -F ..`). Zapisz odpowiedź, a dopiero potem sprawdź.

<details>
<summary>Wyjaśnienie</summary>

Zobaczysz `muzea`. Wiele osób spodziewa się tu słowa `krakow`, ale `..` to sam katalog `krakow`, a `ls` pokazuje jego **zawartość**. W `krakow` jest tylko `muzea`. Zauważ też, że `ls ..` nigdzie Cię nie przeniosło: sprawdź `pwd`.

</details>

`..` można łączyć: `..\..` na Windowsie albo `../..` na macOS i Linuksie oznacza „dwa poziomy w górę”. Sprawdź, co pokaże `ls` z taką ścieżką, wpisane z katalogu `muzea`.

### Jak wysoko można wejść?

Wróć do domu (`cd ~`) i kilka razy powtórz `cd ..`, za każdym razem sprawdzając `pwd`:

| Windows | macOS | Linux |
|---|---|---|
| `C:\Users` → `C:\` → `C:\` | `/Users` → `/` → `/` | `/home` → `/` → `/` |

W pewnym momencie `pwd` przestaje się zmieniać. Jesteś wtedy w **katalogu głównym**, czyli w najwyższym katalogu drzewa (`C:\` na Windowsie, `/` na macOS i Linuksie). Nad nim nic już nie ma, więc `cd ..` niczego nie zmienia. Możesz tu zajrzeć przez `ls`, ale niczego nie zmieniaj: to katalogi systemowe.

Wróć do domu: `cd ~`.

## 6. Zastosuj: `cd` niczego nie przenosi

Przejdź do katalogu `krakow`:

| Windows | macOS i Linux |
|---|---|
| `cd plan-podrozy\krakow` | `cd plan-podrozy/krakow` |

Teraz spójrz na okno plików, które otworzyło się w punkcie 3. Czy coś się w nim zmieniło? Sprawdź też w terminalu, co jest w katalogu domowym, nie wychodząc z `krakow`:

| Windows | macOS i Linux |
|---|---|
| `ls ~` | `ls -F ~` |

`plan-podrozy` wciąż leży w katalogu domowym. Nic się nie przesunęło: zmieniło się tylko miejsce, w którym „stoi” powłoka. Przenoszenie plików i katalogów to zupełnie inna operacja. Poznasz ją później.

## 7. Zastosuj: ścieżka bezwzględna działa zewsząd

Ścieżka względna zależy od bieżącego katalogu, a bezwzględna nie. Złóż ścieżkę bezwzględną do katalogu `gdansk`: weź wynik `pwd` z punktu 2 i dopisz `plan-podrozy` oraz `gdansk`.

| System | Przykład dla katalogu domowego `ola` |
|---|---|
| Windows | `cd C:\Users\ola\plan-podrozy\gdansk` |
| macOS | `cd /Users/ola/plan-podrozy/gdansk` |
| Linux (zwykle) | `cd /home/ola/plan-podrozy/gdansk` |

Wpisz swoją wersję. Nie jest ważne, gdzie teraz jesteś: ta ścieżka prowadzi w to samo miejsce z każdego katalogu. Sprawdź `pwd`.

> **Windows:** jeśli w ścieżce jest spacja, weź ją w cudzysłów, tak jak w lekcji 0.1, na przykład `cd "C:\Users\Jan Kowalski\plan-podrozy\gdansk"`.

## 8. Misja: z muzeum na plażę

Zwiedzanie muzeów skończone, czas na plażę. Twoim zadaniem jest przejść z katalogu `muzea` do katalogu `plaze`.

**Start:** wpisz `cd ~`, a potem `cd plan-podrozy\krakow\muzea` (Windows) albo `cd plan-podrozy/krakow/muzea` (macOS, Linux). Sprawdź `pwd`.

**Część A: krok po kroku.** Przejdź do `plaze`, zmieniając katalog **o jeden poziom na raz**: używaj tylko `cd ..` albo `cd` z pojedynczą nazwą katalogu. Przed każdym poleceniem zapisz, czym według Ciebie będzie się kończył wynik `pwd`. Po każdym poleceniu sprawdź `pwd`.

| Krok | Polecenie | Przewidywany koniec `pwd` | Wynik zgodny? |
|---|---|---|---|
| 1 | | | |
| 2 | | | |
| … | | | |

<details>
<summary>Podpowiedź: ile kroków?</summary>

Wystarczą cztery: dwa razy w górę, dwa razy w dół.

</details>

**Część B: jednym poleceniem.** Wróć na start (do `muzea`) i dotrzyj do `plaze` **jednym** poleceniem `cd` ze ścieżką względną.

**Część C: z powrotem.** Będąc w `plaze`, wróć do katalogu domowego. Zrób to na dwa sposoby: raz poleceniem z `~`, a raz używając wyłącznie `..`. Ile `..` potrzebujesz?

### Kryterium sukcesu

- Po części A i po części B wynik `pwd` kończy się na `plan-podrozy\gdansk\plaze` (Windows) albo `plan-podrozy/gdansk/plaze` (macOS, Linux).
- W `plaze` polecenie `ls` (albo `ls -F`) **nic nie wypisuje**. To dobrze: katalog jest pusty. Brak wyniku to nie błąd. Błąd wyglądałby jak komunikat z punktu 4.
- Po części C `pwd` pokazuje Twój katalog domowy.

<details>
<summary>Przykładowe rozwiązanie</summary>

Na macOS i Linuksie (na Windowsie zamiast `/` użyj `\`):

- Część A: `cd ..` (→ `krakow`), `cd ..` (→ `plan-podrozy`), `cd gdansk`, `cd plaze`.
- Część B: `cd ../../gdansk/plaze`.
- Część C: `cd ~` albo `cd ../../..` (trzy poziomy w górę: `gdansk`, `plan-podrozy`, katalog domowy).

</details>

## 9. Te same nazwy, różne narzędzia

Na Windowsie wpisujesz `cd`, `pwd` i `ls`, tak samo jak na macOS i Linuksie. W PowerShellu są to jednak **aliasy**, czyli dodatkowe, krótsze nazwy jego własnych poleceń:

| Wpisujesz | W PowerShellu to naprawdę |
|---|---|
| `cd` | `Set-Location` |
| `pwd` | `Get-Location` |
| `ls` | `Get-ChildItem` |

Wyglądają tak samo, ale to inne narzędzia niż na macOS i Linuksie, więc w szczegółach działają inaczej. Dlatego `ls -F` z lekcji 0.1 nie działa na Windowsie, a w tabeli poniżej znajdziesz kilka kolejnych różnic. Zasada na przyszłość: **ta sama nazwa nie oznacza tego samego narzędzia**. Gdy coś działa inaczej niż w przykładzie, sprawdź wersję polecenia dla swojego systemu.

## 10. Gdy coś pójdzie inaczej

Najpierw sprawdź `pwd`: większość niespodzianek przy `cd` bierze się z tego, że jesteś w innym katalogu, niż myślisz. Jeśli się zgubisz, `cd ~` zabierze Cię do domu.

| Co widzisz | Co to znaczy | Co zrobić |
|---|---|---|
| Windows: `Cannot find path '…' because it does not exist.`<br>macOS: `cd: no such file or directory: krakow`<br>Linux: `bash: cd: krakow: No such file or directory` | W bieżącym katalogu nie ma takiej ścieżki. | Sprawdź `pwd` i `ls`: czy katalog jest tam, gdzie go szukasz, i czy nazwa jest dobrze napisana? |
| macOS i Linux: `command not found: cd..` albo `cd..: command not found` | Brakuje spacji między `cd` a `..`. | Wpisz `cd ..`, ze spacją. W PowerShellu `cd..` akurat działa, ale używaj spacji wszędzie. |
| `cd Krakow` (wielka litera) działa na Windowsie i zwykle na macOS, ale nie na Linuksie | Linux rozróżnia wielkie i małe litery w nazwach. Windows i macOS zwykle nie, choć `pwd` może wtedy pokazać nazwę w takiej pisowni, w jakiej ją wpisano. | Wpisuj nazwy dokładnie tak, jak je widzisz w `ls`. |
| Samo `cd` (bez niczego) na macOS i Linuksie przenosi do domu, a na Windowsie, zależnie od wersji PowerShella, do domu albo nigdzie | To jedna z różnic między powłokami. | Do domu wracaj poleceniem `cd ~`. Działa wszędzie. |
| macOS i Linux: po `cd plan-podrozy\krakow` komunikat o braku katalogu `plan-podrozykrakow` | Na macOS i Linuksie separatorem jest `/`. Znak `\` ma tam inne znaczenie i powłoka go usuwa, dlatego nazwa w komunikacie jest sklejona. | Użyj `/`. PowerShell na Windowsie akceptuje oba separatory, ale w kursie na Windowsie piszemy `\`. |
| `ls` w `plaze` nic nie wypisuje | Katalog jest pusty. | Wszystko w porządku. |

## 11. Wyjaśnij

Odpowiedz własnymi słowami, najlepiej na głos albo na kartce. Dopiero potem rozwiń odpowiedź.

**1.** Jesteś w `krakow` i wpisujesz `cd muzea`. Co się zmieniło na dysku, a co w powłoce?

<details>
<summary>Odpowiedź</summary>

Na dysku nic. `muzea` jest tam, gdzie było. W powłoce zmienił się bieżący katalog, a razem z nim punkt startowy ścieżek względnych.

</details>

**2.** Ola jest w `plan-podrozy`, a Bartek w `krakow`. Oboje wpisują `cd gdansk`. Komu się uda i dlaczego? Jak polecenie może zapisać druga osoba, żeby trafić do `gdansk`?

<details>
<summary>Odpowiedź</summary>

Udało się Oli, bo `gdansk` leży w `plan-podrozy`. W `krakow` nie ma katalogu `gdansk`, więc Bartek zobaczy błąd. Bartek może wpisać `cd ..\gdansk` (Windows) albo `cd ../gdansk` (macOS, Linux), czyli „poziom w górę, potem do `gdansk`”, albo użyć ścieżki bezwzględnej.

</details>

**3.** Jesteś w `muzea`, a `ls ..` pokazuje `muzea`. Dlaczego nie `krakow`?

<details>
<summary>Odpowiedź</summary>

Bo `..` oznacza katalog `krakow`, a `ls` pokazuje to, co jest **w środku** wskazanego katalogu. W `krakow` jest tylko `muzea`.

</details>

**4.** Dlaczego `cd` ze ścieżką bezwzględną działa niezależnie od bieżącego katalogu, a ze ścieżką względną nie?

<details>
<summary>Odpowiedź</summary>

Ścieżka bezwzględna zaczyna się od katalogu głównego, więc opisuje miejsce w całym drzewie. Ścieżka względna opisuje drogę od bieżącego katalogu, więc z innego punktu startowego prowadzi gdzie indziej albo donikąd.

</details>

## Podsumowanie

- `cd ścieżka` zmienia bieżący katalog i niczego nie przenosi na dysku.
- `.` to bieżący katalog, a `..` to katalog nadrzędny. Oba można wstawiać do ścieżek, na przykład `..\gdansk` albo `../gdansk`.
- `~` to katalog domowy. `cd ~` to bezpieczny powrót z dowolnego miejsca.
- Na samej górze drzewa jest katalog główny: `C:\` (na Windowsie, dla dysku `C:`) albo `/` (na macOS i Linuksie).
- Ścieżka względna zależy od bieżącego katalogu, a bezwzględna nie.
- Po każdym `cd` sprawdzaj, gdzie jesteś, poleceniem `pwd`.

Katalog `plan-podrozy` możesz zostawić albo usunąć w oknie plików.

**Poprzednia lekcja:** [Lekcja 0.1: Pliki, katalogi i pierwsze spotkanie z terminalem](lesson_01_files_and_terminal.md) · **Następna lekcja:** w przygotowaniu · [Opis kursu](../../README.md)

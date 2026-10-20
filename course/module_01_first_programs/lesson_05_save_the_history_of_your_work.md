# Lekcja 1.5: Zapisz historię swojej pracy

**Polski** · [English](lesson_05_save_the_history_of_your_work.en.md) · [Opis kursu](../../README.md)

> **Moduł 1, lekcja 5** · około 75 minut
> **Potrzebujesz:** katalogu `cpp-workspace` z projektami z lekcji 1.1–1.4, terminala oraz, na Windowsie i Ubuntu, uprawnień administratora do instalacji Gita (jak w [lekcji 0.4](../module_00_tooling/lesson_04_installing_the_tools.md)).
> **Wersja pilotażowa:** polecenia Gita z tej lekcji sprawdzamy automatycznie w Windows PowerShell 5.1, PowerShell 7, bashu na Ubuntu i zsh na macOS.

## Zanim zaczniesz

Ta lekcja zakłada, że:

- masz w katalogu domowym katalog `cpp-workspace` z projektami z lekcji 1.1–1.4, na przykład `cinema_ticket` z misji lekcji 1.3;
- umiesz w terminalu przejść do katalogu, wyświetlić jego zawartość i uruchomić program (Moduł 0);
- wiesz, które pliki projektu piszesz sam, a które tworzą narzędzia (lekcja 1.4).

## Sytuacja

Twój program z biletem do kina działa. Chcesz go zmienić, ale boisz się, że coś zepsujesz i nie będziesz pamiętać, jak wyglądała działająca wersja.

Najprostszy pomysł to kopie: `cinema_ticket_final`, `cinema_ticket_final_2`, `cinema_ticket_final_naprawde`. Po tygodniu nie wiadomo już, która kopia jest która, czym się różnią i która działała. Każda kopia ciągnie za sobą katalogi budowania. Łatwo też poprawić nie tę kopię, co trzeba.

Programiści rozwiązują ten problem **systemem kontroli wersji**. To program, który na Twoje polecenie zapisuje wersje wybranych plików, z opisem, autorem i datą. Potem pokazuje, co zmieniło się między wersjami, i pozwala zobaczyć każdą wcześniejszą wersję. Najpopularniejszy taki system to **Git**.

Po tej lekcji będziesz:

- wyjaśniać, do czego służy kontrola wersji, i odróżniać Git od GitHuba;
- instalować Git i sprawdzać jego wersję;
- tworzyć lokalne repozytorium i wiedzieć, po co jest katalog `.git`;
- sprawdzać stan plików (`git status`) i zmiany (`git diff`);
- wybierać pliki do zapisania (`git add`) i tworzyć commity z sensownym opisem (`git commit`);
- przeglądać historię (`git log`);
- pomijać pliki wygenerowane przez narzędzia za pomocą `.gitignore`.

## 1. Git i GitHub

| | Git | GitHub |
|---|---|---|
| Co to jest | Program na Twoim komputerze. | Usługa w internecie. |
| Do czego służy | Zapisuje historię zmian w plikach i ją pokazuje. | Przechowuje repozytoria Gita w sieci i pomaga ludziom nad nimi współpracować. |
| Czego potrzebuje | Niczego poza instalacją. Działa bez internetu i bez konta. | Konta i internetu. |
| W tej lekcji | Tak. | **Nie.** Nie zakładasz konta i niczego nie publikujesz. |

GitHub i podobne usługi poznasz, gdy będziesz chcieć dzielić się pracą z innymi. Dziś cała historia zostaje na Twoim komputerze.

Trzy nowe słowa:

- **Repozytorium** to katalog, którego historię prowadzi Git.
- **Commit** to jedna zapisana wersja, z opisem, autorem i datą.
- **Kontrola wersji** to właśnie zapisywanie takich wersji i porównywanie ich.

## 2. Zainstaluj Git

### Windows

Git zainstalujesz tak samo jak narzędzia w lekcji 0.4, przez Chocolatey.

1. Otwórz terminal **jako administrator** (lekcja 0.4, punkt 3).
2. Wpisz:

   ```text
   choco install git -y
   ```

3. Gdy instalacja się skończy, zamknij terminal i otwórz **nowy, zwykły** terminal. Dopiero nowy terminal zna nowy program (`PATH`, lekcja 0.3).

### macOS

Git już masz: Apple dołącza go do *Command Line Tools*, które zainstalowano w lekcji 0.4. Niczego nie instalujesz, tylko sprawdzasz wersję.

Jeśli w kroku sprawdzania pojawi się okno z prośbą o instalację narzędzi deweloperskich, brakuje *Command Line Tools*. Wróć wtedy do lekcji 0.4. Nowszego Gita możesz zainstalować przez Homebrew (`brew install git`), ale do tej lekcji nie jest to potrzebne.

### Ubuntu

W terminalu wpisz:

```text
sudo apt install -y git
```

System zapyta o Twoje hasło, jak w lekcji 0.4.

### Sprawdź

We wszystkich systemach:

```text
git --version
```

Zobaczysz numer wersji, na przykład `git version 2.56.0.windows.2` (Windows), `git version 2.39.5 (Apple Git-154)` (macOS) albo `git version 2.43.0` (Ubuntu). Twój numer może być inny. Do tej lekcji wystarczy każda wersja z ostatnich kilku lat.

## 3. Utwórz repozytorium w `cpp-workspace`

Jedno repozytorium obejmie cały Twój `cpp-workspace`: wszystkie Twoje projekty będą miały wspólną historię. Repozytorium tworzysz w swoim katalogu roboczym, a nie w katalogu z materiałami kursu.

**Krok 1. Przejdź do `cpp-workspace`:**

```text
cd ~
cd cpp-workspace
```

Sprawdź `ls` (na macOS i Ubuntu `ls -F`). Widzisz swoje projekty: `lesson_1_1`, `parcel_label`, `cinema_ticket` i inne.

**Krok 2. Upewnij się, że to jeszcze nie jest repozytorium:**

```text
git status
```

Oczekiwany wynik to **błąd**, i to jest dobra wiadomość:

```text
fatal: not a git repository (or any of the parent directories): .git
```

Git sprawdził ten katalog i wszystkie katalogi nad nim i nigdzie nie znalazł repozytorium. Możesz więc bezpiecznie utworzyć nowe. Jeśli zamiast tego widzisz `On branch …`, **zatrzymaj się** i przeczytaj punkt 10.

**Krok 3. Utwórz repozytorium:**

```text
git init
```

Ostatnia linijka wyniku to na przykład:

```text
Initialized empty Git repository in /home/ola/cpp-workspace/.git/
```

Przed nią mogą pojawić się linijki zaczynające się od `hint:`, z podpowiedzią o nazwie gałęzi (*branch*). Na razie je pomiń. Gałęzie poznasz później, a nazwa `master` czy `main` nie ma dziś znaczenia.

`git init` utworzył ukryty katalog **`.git`**. Git przechowuje w nim całą historię. Nie zmieniaj w nim niczego ręcznie i **nigdy go nie usuwaj**: usunięcie `.git` usuwa całą historię. Możesz go zobaczyć poleceniem `ls -Force` (Windows) albo `ls -a` (macOS i Ubuntu).

**Krok 4. Zobacz stan repozytorium:**

```text
git status
```

```text
On branch master

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        build_detective/
        cinema_ticket/
        lesson_1_1/
        ...

nothing added to commit but untracked files present (use "git add" to track)
```

**Opisz, co widzisz:** co znaczą `No commits yet` i `Untracked files`?

<details>
<summary>Odpowiedź</summary>

`No commits yet`: w historii nie ma jeszcze żadnej wersji. `Untracked files`: pliki, których Git jeszcze nie śledzi. Widzi je w katalogu, ale nie są w historii. Na liście są katalogi Twoich projektów. Na macOS może być też plik `.DS_Store`, który tworzy Finder.

</details>

## 4. Przedstaw się Gitowi

Każdy commit zapisuje, **kto** go utworzył: imię lub nazwę i adres e-mail. Ustaw je dla tego repozytorium, w katalogu `cpp-workspace`:

```text
git config user.name "<Twoje imię i nazwisko albo pseudonim>"
git config user.email "<Twój adres e-mail>"
```

Zamiast tekstu w nawiasach ostrych wpisz **własne** dane i usuń znaki `<` i `>`. Cudzysłowy zostają. Sprawdź:

```text
git config user.name
```

**Lokalnie czy globalnie?**

- Bez dodatkowej opcji, tak jak tutaj, ustawienie dotyczy **tylko tego repozytorium**. Jest zapisane w `.git` i nie wpływa na inne projekty na Twoim komputerze.
- Z opcją `--global` dotyczyłoby **wszystkich** repozytoriów Twojego konta. Dziś jej nie używasz.

**Prywatność.** Imię i e-mail zostają w historii każdego commita. Jeśli kiedyś opublikujesz repozytorium, zobaczą je wszyscy. Możesz użyć pseudonimu. Jak ukryć adres e-mail przy publikowaniu, dowiesz się, gdy przyjdzie na to pora.

## 5. Co ma trafić do historii? `.gitignore`

Zobacz **wszystkie** pliki, które Git widzi, łącznie z tymi wewnątrz katalogów:

```text
git status --untracked-files=all
```

Lista jest długa. Oto jej fragment:

```text
cinema_ticket/.idea/workspace.xml
cinema_ticket/CMakeLists.txt
cinema_ticket/cmake-build-debug/CMakeCache.txt
cinema_ticket/cmake-build-debug/first_program
cinema_ticket/main.cpp
...
lesson_1_4/build-terminal/CMakeCache.txt
lesson_1_4/build-terminal/first_program
lesson_1_4/build-terminal/hello_cmake
lesson_1_4/hello
lesson_1_4/main.o
```

U Ciebie lista będzie zależeć od tego, co budowano i co otwierano w CLionie. Pliki dzielą się na cztery grupy:

| Grupa | Przykłady | Do historii? |
|---|---|---|
| **Twój kod** | `main.cpp`, `CMakeLists.txt` | **Tak.** To Twoja praca. |
| **Wyniki budowania** | `build-terminal/`, `cmake-build-debug/`, `main.o`, `hello`, pliki `.exe` | **Nie.** Narzędzia odtworzą je w każdej chwili z Twojego kodu. Zmieniają się przy każdym budowaniu, zajmują dużo miejsca i zawierają ścieżki Twojego komputera. |
| **Ustawienia CLiona** | katalogi `.idea/` | **Nie.** To ustawienia CLiona dla tego komputera, a nie część programu. |
| **Pliki systemu** | `.DS_Store` (macOS) | **Nie.** Tworzy je Finder. |

Plik **`.gitignore`** mówi Gitowi, których plików ma nie pokazywać i nie dodawać. Utwórz go w `cpp-workspace` jednym poleceniem:

**Windows (PowerShell):**

```text
Set-Content .gitignore 'build-terminal/', 'cmake-build-*/', '.idea/', '*.o', '*.obj', '*.exe', '/lesson_1_4/hello', '.DS_Store'
```

**macOS i Ubuntu:**

```text
printf '%s\n' 'build-terminal/' 'cmake-build-*/' '.idea/' '*.o' '*.obj' '*.exe' '/lesson_1_4/hello' '.DS_Store' > .gitignore
```

Zobacz, co powstało: `Get-Content .gitignore` (Windows) albo `cat .gitignore` (macOS i Ubuntu). To zwykły plik tekstowy, po jednej regule w linijce:

| Reguła | Co pomija |
|---|---|
| `build-terminal/` | katalogi budowania z terminala, w każdym projekcie |
| `cmake-build-*/` | katalogi budowania CLiona, na przykład `cmake-build-debug/` |
| `.idea/` | ustawienia CLiona |
| `*.o`, `*.obj` | pliki obiektowe (lekcja 1.4) |
| `*.exe` | programy na Windowsie |
| `/lesson_1_4/hello` | program `hello` z lekcji 1.4 na macOS i Ubuntu. To jeden konkretny plik, żeby nie ukryć przypadkiem projektu o podobnej nazwie. |
| `.DS_Store` | pliki Findera na macOS |

Plik jest ten sam na wszystkich systemach. Reguły, które Twojego systemu nie dotyczą, po prostu nic nie robią.

Sprawdź jeszcze raz:

```text
git status --untracked-files=all
```

Teraz w każdym projekcie zostały tylko `main.cpp` i `CMakeLists.txt`, plus nowy `.gitignore`. Narzędzia nadal mogą tworzyć te pliki i katalogi, a Git po prostu je pomija.

**Ważne:** `.gitignore` działa tylko na pliki, których Git **jeszcze nie śledzi**. Jeśli jakiś plik już trafił do historii, dopisanie go do `.gitignore` go z niej nie usunie (punkt 10). Dlatego `.gitignore` tworzysz **przed** pierwszym commitem.

## 6. Pierwszy commit

Zaczniesz od jednego, skończonego projektu: biletu do kina z misji lekcji 1.3. Jeśli nie masz katalogu `cinema_ticket`, wybierz inny skończony projekt i w poleceniach wpisz jego nazwę.

**Krok 1. Wybierz pliki.** Wymień je dokładnie, po nazwach:

```text
git add .gitignore cinema_ticket/main.cpp cinema_ticket/CMakeLists.txt
```

Ścieżki zapisujesz z `/` na wszystkich systemach, także w PowerShellu. Git je rozumie.

Na Windowsie może pojawić się ostrzeżenie:

```text
warning: in the working copy of 'cinema_ticket/main.cpp', LF will be replaced by CRLF the next time Git touches it
```

Systemy różnie oznaczają koniec linijki w plikach tekstowych: Windows dwoma znakami (CRLF), macOS i Linux jednym (LF). Git na Windowsie jest tak ustawiony, żeby w historii zapisywać jedną formę, a w Twoim katalogu używać formy Windowsa. Ostrzeżenie mówi tylko o tym. Twój plik i program są w porządku i nic nie musisz robić.

**Krok 2. Sprawdź, co jest przygotowane:**

```text
git status
```

```text
On branch master

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
        new file:   .gitignore
        new file:   cinema_ticket/CMakeLists.txt
        new file:   cinema_ticket/main.cpp

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        build_detective/
        lesson_1_1/
        ...
```

`git add` nie zapisuje jeszcze wersji. Kopiuje aktualną zawartość wybranych plików do **przechowalni** (ang. *staging area*): miejsca, w którym kompletujesz następny commit. `Changes to be committed` to właśnie zawartość przechowalni. Pozostałe projekty czekają w `Untracked files` i nie trafią do tego commita.

Treść przygotowanych zmian zobaczysz poleceniem `git diff --staged`. Gdy wynik jest dłuższy niż ekran, Git pokazuje go stronami: <kbd>Spacja</kbd> to następna strona, a <kbd>q</kbd> kończy przeglądanie.

**Krok 3. Zapisz wersję:**

```text
git commit -m "Dodaj bilet do kina i plik .gitignore"
```

`-m` podaje **opis commita** (*commit message*). Dobry opis mówi krótko, co ta wersja wnosi. W tym kursie piszemy opisy bez polskich znaków, z tego samego powodu co komunikaty programów: nie każda konsola na Windowsie wyświetli je poprawnie. Wynik:

```text
[master (root-commit) 6d29aa9] Dodaj bilet do kina i plik .gitignore
 3 files changed, 25 insertions(+)
 create mode 100644 .gitignore
 create mode 100644 cinema_ticket/CMakeLists.txt
 create mode 100644 cinema_ticket/main.cpp
```

`6d29aa9` to początek **identyfikatora commita**. U Ciebie będzie inny, bo zależy od treści, autora i czasu.

**Krok 4. Sprawdź stan:** `git status`. Pliki biletu zniknęły z listy, bo są zapisane w historii i od tamtej pory się nie zmieniły. Zostały tylko pozostałe projekty.

**Krok 5. Zobacz historię:**

```text
git log
```

```text
commit 6d29aa9f9b6ce4e27c45ff2258689f60a553dc0c
Author: (tu Twoje imię i adres e-mail z punktu 4)
Date:   Tue Oct 20 18:28:10 2026 +0000

    Dodaj bilet do kina i plik .gitignore
```

U Ciebie będą Twoje dane, Twoja data i Twój identyfikator. Jeśli wynik się nie mieści, <kbd>q</kbd> kończy przeglądanie.

**Zapisanie pliku a commit.** <kbd>Ctrl</kbd> + <kbd>S</kbd> w edytorze zapisuje plik na dysku: jest tylko jedna, aktualna treść, a poprzednią nadpisujesz. Commit zapisuje **wersję w historii**: powstaje tylko wtedy, gdy o tym zdecydujesz, a wszystkie wcześniejsze wersje zostają.

## 7. Zmień program i zapisz drugą wersję

Teraz mniej podpowiedzi.

1. W `cinema_ticket/main.cpp` zmień numer rzędu i miejsca, na przykład `Row 7, seat 12` na `Row 9, seat 5`. Zbuduj i uruchom program tak jak w lekcji 1.3, żeby sprawdzić, że działa.
2. **Przewidź**, co pokaże `git status`, i sprawdź.
3. Zobacz zmianę: `git diff`.
4. Przygotuj zmianę do commita i sprawdź, co jest w przechowalni.
5. Zapisz drugi commit z opisem, który mówi, co się zmieniło.
6. Zobacz historię w skrócie: `git log --oneline`.

<details>
<summary>Podpowiedź: które polecenia?</summary>

Te same co w punkcie 6: najpierw sprawdzasz (`git status`, `git diff`), potem wybierasz (`git add` z nazwą pliku), sprawdzasz jeszcze raz (`git status` albo `git diff --staged`) i zapisujesz (`git commit -m "…"`).

</details>

`git diff` pokazuje różnicę między ostatnią zapisaną wersją a plikiem na dysku:

```text
diff --git a/cinema_ticket/main.cpp b/cinema_ticket/main.cpp
index 9483a09..7c49361 100644
--- a/cinema_ticket/main.cpp
+++ b/cinema_ticket/main.cpp
@@ -3,7 +3,7 @@
 int main() {
     std::cout << "CINEMA TICKET\n";
     std::cout << "Film: \"The Long Night\"\n";
-    std::cout << "Row 7, seat 12\n";
+    std::cout << "Row 9, seat 5\n";
     // Each \\ in the code prints one backslash.
     std::cout << "File: C:\\tickets\\night.txt\n";
     std::cout << "Enjoy the film!\n";
```

Linijka z `-` to stara treść, z `+` to nowa. Pozostałe linijki to otoczenie, żeby było wiadomo, gdzie jest zmiana. `@@ -3,7 +3,7 @@` mówi, od której linijki zaczyna się pokazany fragment.

Po `git add` zwykły `git diff` nic już nie pokazuje, bo plik zgadza się z przechowalnią. Zmianę w przechowalni pokazuje `git diff --staged`.

`git log --oneline` po drugim commicie:

```text
63f6aee Nowe miejsce na bilecie
6d29aa9 Dodaj bilet do kina i plik .gitignore
```

**Zobacz poprzednią wersję.** To jest odpowiedź na problem z początku lekcji. Weź identyfikator **pierwszego** commita z `git log --oneline` i wpisz:

```text
git show 6d29aa9:cinema_ticket/main.cpp
```

Zamiast `6d29aa9` wpisz swój identyfikator. Ścieżkę pliku zapisz z `/`, także na Windowsie. Git wypisze plik **w tamtej wersji**, z `Row 7, seat 12`. Twój plik na dysku się nie zmienił: dalej ma nową wersję. Git przechowuje wszystkie zapisane wersje i każdą możesz obejrzeć.

## 8. Misja: zachowaj dwa etapy pracy

Wybierz **inny** swój projekt z `cpp-workspace`, na przykład `parcel_label`, `shopping_list` albo `build_detective`. Twoje zadanie:

1. Sprawdź stan repozytorium.
2. Zapisz w commicie działającą wersję tego projektu: tylko jego pliki źródłowe.
3. Wprowadź w programie konkretną zmianę, na przykład dodaj linijkę wyniku albo zmień tekst. Zbuduj i uruchom program.
4. Zobacz różnicę.
5. Zapisz drugi commit.
6. Wyjaśnij własnymi słowami, co zmieniło się między tymi dwiema wersjami.

### Kryterium sukcesu

- `git log --oneline` pokazuje dwa nowe commity z opisami, które mówią, co każda wersja wnosi.
- `git status` nie pokazuje plików tego projektu: ani zmienionych, ani nieśledzonych.
- `git ls-files <katalog projektu>` (lista plików zapisanych w historii) pokazuje tylko `main.cpp` i `CMakeLists.txt` tego projektu: żadnych wyników budowania ani ustawień CLiona.
- Umiesz wskazać, które linijki się zmieniły i dlaczego, na przykład na podstawie `git show <identyfikator>`, które pokazuje zmiany wprowadzone przez dany commit.

<details>
<summary>Podpowiedź 1</summary>

Najpierw sprawdzasz, potem wybierasz, potem sprawdzasz jeszcze raz, na końcu zapisujesz. Wróć do kolejności z punktu 7.

</details>

<details>
<summary>Podpowiedź 2</summary>

Które polecenie pokazuje zmianę **przed** `git add`, a które **po**? Jeśli `git status` po commicie nadal pokazuje pliki projektu, coś zostało w przechowalni albo poza nią.

</details>

Przykładowy przebieg jest w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 9. Dla chętnych: pozostałe projekty

Gdy wiesz już, że `.gitignore` działa, możesz dodać całe katalogi projektów, a nie pojedyncze pliki:

```text
git add lesson_1_1 lesson_1_2 lesson_1_3 lesson_1_4 shopping_list build_detective
```

Wpisz tylko te katalogi, które naprawdę masz i których jeszcze nie zapisano. **Zanim zrobisz commit**, sprawdź `git status`: w `Changes to be committed` mają być tylko pliki `main.cpp` i `CMakeLists.txt`. Potem zapisz commit, na przykład `git commit -m "Dodaj pozostale projekty"`.

W tym kursie nie dodajesz wszystkiego naraz (`git add .`). Wybierasz pliki albo katalogi świadomie i sprawdzasz je przed zapisaniem.

**Git w CLionie.** CLion też potrafi pokazywać zmiany i historię Gita (okna **Commit** i **Git**). Nie są potrzebne w tym kursie: polecenia w terminalu robią to samo i działają tak samo w każdym środowisku.

## 10. Gdy coś pójdzie inaczej

| Co widzisz | Co to znaczy | Co zrobić |
|---|---|---|
| `git` nie jest rozpoznawany | Terminal nie zna jeszcze Gita. | Zamknij terminal i otwórz nowy (na Windowsie zwykły, nie administratora). Sprawdź `git --version`. Jeśli dalej nie działa, powtórz instalację. Nie zmieniaj ręcznie zmiennej `PATH`. |
| `git status` **przed** `git init` pokazuje `On branch …` | Katalog jest już wewnątrz innego repozytorium. | **Nie wykonuj `git init`** i niczego nie usuwaj. `git rev-parse --show-toplevel` pokaże, gdzie zaczyna się to repozytorium. Sprawdź, czy `cpp-workspace` jest tam, gdzie powinien (w katalogu domowym, lekcja 1.1). |
| `Author identity unknown` i `Please tell me who you are` przy `git commit` | Git nie wie, kim jesteś. | Ustaw imię i e-mail (punkt 4) i powtórz `git commit`. |
| Otworzył się edytor tekstu w terminalu | Commit bez `-m "…"`: Git czeka na opis w edytorze. | Najprościej zrezygnować i powtórzyć z `-m`. W edytorze *Vim* (często na Windowsie i macOS) naciśnij <kbd>Esc</kbd>, wpisz `:q!` i <kbd>Enter</kbd>. W edytorze *nano* (często na Ubuntu) naciśnij <kbd>Ctrl</kbd> + <kbd>X</kbd>. Commit nie powstanie. |
| Wynik `git log`/`git diff` się nie kończy, a na dole jest `:` | Git pokazuje długi wynik stronami. | <kbd>Spacja</kbd> to następna strona, <kbd>q</kbd> kończy przeglądanie. |
| `LF will be replaced by CRLF` (Windows) | Informacja o końcach linijek (punkt 6). | Nic nie rób. |
| Do przechowalni trafił niewłaściwy plik | `git add` wybrał za dużo. | `git restore --staged <plik>` wyjmuje go z przechowalni. Plik na dysku się nie zmienia. |
| `The following paths are ignored by one of your .gitignore files` | Próbujesz dodać plik pomijany przez `.gitignore`. | To ochrona przed pomyłką. Nie dodawaj go. |
| Plik budowania już jest w historii | Dodano go, zanim był `.gitignore`. | `git rm --cached <plik>`, a potem commit. Plik zostaje na dysku, znika tylko z następnych wersji w historii. |
| `git show` z `\` w ścieżce nie znajduje pliku (Windows) | W `identyfikator:ścieżka` Git oczekuje `/`. | Wpisz ścieżkę z `/`, na przykład `cinema_ticket/main.cpp`. |

Nie usuwaj katalogu `.git`, żeby „zacząć od nowa”: tracisz wtedy całą historię. Każdy problem z tej tabeli rozwiązuje się bez tego.

## 11. Wyjaśnij

Odpowiedz własnymi słowami, najlepiej na piśmie. Dopiero potem porównaj z przykładową odpowiedzią.

**1.** Czym różni się Git od GitHuba? Czy do tej lekcji potrzebny jest internet?

<details>
<summary>Przykładowa odpowiedź</summary>

Git to program na moim komputerze, który zapisuje historię zmian. GitHub to usługa w internecie do przechowywania repozytoriów i współpracy. Do tej lekcji internet był potrzebny tylko do instalacji Gita. Repozytorium i commity są na moim komputerze.

</details>

**2.** Po co jest `git add`, skoro i tak trzeba wykonać `git commit`?

<details>
<summary>Przykładowa odpowiedź</summary>

`git add` wybiera, co trafi do następnego commita (przechowalnia), a `git commit` zapisuje dokładnie to, co wybrano. Dzięki temu decyduję, które pliki i zmiany zapisuję, i mogę je sprawdzić przed zapisaniem.

</details>

**3.** Dlaczego `build-terminal/` i `.idea/` nie trafiają do historii?

<details>
<summary>Przykładowa odpowiedź</summary>

Bo to nie mój kod. Wyniki budowania narzędzia odtworzą w każdej chwili, a ustawienia CLiona dotyczą tylko tego komputera. W historii zajmowałyby miejsce i zaśmiecały każdą zmianę.

</details>

**4.** Czym różni się wynik `git diff` od `git diff --staged`?

<details>
<summary>Przykładowa odpowiedź</summary>

`git diff` pokazuje zmiany w plikach na dysku, których jeszcze nie przygotowano do commita. `git diff --staged` pokazuje zmiany przygotowane w przechowalni, czyli to, co zapisze najbliższy commit.

</details>

**5.** Czym zapisanie pliku w edytorze różni się od commita?

<details>
<summary>Przykładowa odpowiedź</summary>

Zapisanie pliku nadpisuje jego treść na dysku i zostaje tylko ostatnia wersja. Commit zapisuje wybraną wersję w historii, z opisem, autorem i datą, a wcześniejsze wersje zostają i można je obejrzeć.

</details>

## Podsumowanie

- Git zapisuje historię wybranych plików lokalnie, bez internetu i bez konta. GitHub to osobna usługa w internecie.
- Repozytorium tworzy `git init`, a jego historia jest w ukrytym katalogu `.git`. Przed `git init` sprawdź `git status`: oczekiwany wynik to `not a git repository`.
- Tożsamość ustawiasz dla repozytorium (`git config user.name`, `git config user.email`), bez `--global`.
- `.gitignore`, utworzony przed pierwszym commitem, pomija wyniki budowania i ustawienia IDE.
- Praca z Gitem to pętla: **sprawdź (`git status`, `git diff`) → wybierz (`git add` z nazwami) → sprawdź (`git diff --staged`) → zapisz (`git commit -m "…"`) → obejrzyj (`git log`)**.
- Każdą wcześniejszą wersję możesz obejrzeć (`git show <identyfikator>:<ścieżka>`), nie zmieniając plików na dysku.

## Co dalej

Masz już historię swojej pracy. **Lekcja 1.6 jest w przygotowaniu.**

---

## Przykładowe rozwiązania

Zajrzyj tutaj **po własnej próbie**. Twoje identyfikatory, daty i opisy będą inne.

<details>
<summary>Punkt 7: przykładowy przebieg</summary>

```text
git status
git diff
git add cinema_ticket/main.cpp
git diff --staged
git commit -m "Nowe miejsce na bilecie"
git log --oneline
```

Po zmianie `git status` pokazuje `modified:   cinema_ticket/main.cpp` w części `Changes not staged for commit`. Po `git add` ten sam plik jest w `Changes to be committed`, a po commicie znika z wyniku `git status`.

</details>

<details>
<summary>Punkt 8: misja, przykładowy przebieg dla <code>parcel_label</code></summary>

```text
git status
git add parcel_label/main.cpp parcel_label/CMakeLists.txt
git status
git commit -m "Dodaj etykiete paczki"
```

Potem zmiana w `parcel_label/main.cpp`, budowanie i uruchomienie programu, a następnie:

```text
git diff
git add parcel_label/main.cpp
git diff --staged
git commit -m "Dodaj adres nadawcy na etykiecie"
git log --oneline
git ls-files parcel_label
```

`git ls-files parcel_label` pokazuje tylko:

```text
parcel_label/CMakeLists.txt
parcel_label/main.cpp
```

Wyjaśnienie zmiany, na przykład: „W drugiej wersji program wypisuje dodatkową linijkę z adresem nadawcy. `git diff` pokazał ją jako jedną linijkę z `+` i żadnej z `-`, bo niczego nie usunięto”.

</details>

**Poprzednia lekcja:** [Lekcja 1.4: Od kodu źródłowego do programu wykonywalnego](lesson_04_from_source_code_to_an_executable.md) · **Następna lekcja:** w przygotowaniu · [Opis kursu](../../README.md)

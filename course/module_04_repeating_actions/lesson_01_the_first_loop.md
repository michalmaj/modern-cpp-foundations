# Lekcja 4.1: Pierwsza pętla (`while`)

**Polski** · [English](lesson_01_the_first_loop.en.md) · [Opis kursu](../../README.md)

> **Moduł 4, lekcja 1** · około 60–75 minut
> **Potrzebujesz:** katalogu `cpp-workspace` i oryginalnego projektu `lesson_05_first_program`, jak dotąd. Debugger nie jest w tej lekcji potrzebny.
> **Wersja pilotażowa.** Programy z tej lekcji sprawdzamy automatycznie na Windowsie, Ubuntu i macOS, także z podanymi danymi wejściowymi. Zatrzymywanie programu w CLionie opisujemy bez ręcznego sprawdzenia na każdym systemie.

## Zanim zaczniesz

Ta lekcja zakłada, że po Module 3:

- piszesz `if` i `if`/`else` z klamrami i łączysz warunki przez `&&`;
- wiesz, że `if` sprawdza warunek z **aktualną** wartością zmiennej;
- zmieniasz wartość zmiennej przypisaniem, także na podstawie jej starej wartości, na przykład `count = count + 1;` (lekcja 2.2);
- sprawdzasz program dla wartości na granicy i tuż obok niej.

## Sytuacja

Organizator treningu chce, żeby program wypisał numery kolejnych okrążeń. Dla trzech okrążeń wystarczą trzy instrukcje:

<!-- fragment -->
```cpp
std::cout << "Lap 1\n";
std::cout << "Lap 2\n";
std::cout << "Lap 3\n";
```

A gdyby okrążeń było 10? Albo 100? Albo gdyby ich liczbę podawał użytkownik, a program nie znał jej w chwili pisania kodu? Przepisywanie tej samej instrukcji przestaje mieć sens. Potrzebny jest sposób, żeby program **wrócił do tego samego fragmentu kodu** i wykonał go jeszcze raz, i żeby **wiedział, kiedy przestać**. Dziś poznasz pierwszą pętlę: `while`.

Po tej lekcji będziesz:

- wyjaśniać, po co programowi powtarzanie;
- wskazywać w pętli `while` wartość początkową licznika, warunek, ciało pętli i zmianę licznika;
- wyjaśniać, kiedy program sprawdza warunek i dlaczego pętla się kończy;
- śledzić przebieg pętli w tabeli i przewidywać liczbę powtórzeń, także zero;
- znajdować błąd o jeden krok i dobierać przypadki, które go ujawniają;
- rozpoznawać pętlę, która nie robi postępu, bez jej uruchamiania;
- przerywać program, który działa zbyt długo;
- pisać własną pętlę z licznikiem.

## 1. Przygotuj projekt

W `cpp-workspace` utwórz katalog `lesson_4_1` i skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program`. Programy z punktów 2–6 wpisujesz w `main.cpp` tego katalogu.

## 2. Pierwsza pętla: trzy okrążenia

<!-- example: laps_three -->
```cpp
#include <iostream>

int main() {
    const int total_laps{3};
    int lap{1};

    while (lap <= total_laps) {
        std::cout << "Lap " << lap << "\n";
        lap = lap + 1;
    }

    std::cout << "Finished, lap is now " << lap << "\n";
}
```

Zanim uruchomisz program, **odpowiedz na piśmie**:

1. Jakie numery okrążeń wypisze program?
2. Ile razy wykona się blok w klamrach po `while`?
3. Jaką wartość będzie miało `lap` po zakończeniu pętli?
4. Dlaczego ostatnia linijka mówi właśnie to, co mówi?

Teraz uruchom program.

<details>
<summary>Wynik programu</summary>

<!-- output: laps_three -->
```text
Lap 1
Lap 2
Lap 3
Finished, lap is now 4
```

Ostatnia linijka mówi `4`, a nie `3`. Dlaczego, wyjaśniają punkty 3 i 4.

</details>

## 3. Cztery części pętli

`while` (po polsku „dopóki”) powtarza blok w klamrach **dopóki** warunek jest spełniony. Ta pętla ma cztery części:

| Część | W programie | Rola |
|---|---|---|
| **Wartość początkowa** | `int lap{1};` | Przed pętlą: od tej wartości zaczyna licznik. Ta linijka wykonuje się **raz**. |
| **Warunek** | `while (lap <= total_laps)` | Przed każdym wykonaniem bloku program sprawdza, czy warunek jest spełniony. „Tak”: wykonuje blok. „Nie”: pętla się kończy. |
| **Ciało pętli** | instrukcje między `{` a `}` | To, co ma się powtarzać: tu wypisanie numeru okrążenia. |
| **Zmiana stanu** | `lap = lap + 1;` | Ostatnia instrukcja ciała: licznik dostaje nową wartość, o 1 większą od starej. |

Liczba powtórzeń nie jest nigdzie zapisana wprost. **Wynika** z tych części: licznik zaczyna od 1, po każdym wykonaniu ciała rośnie o 1, a warunek przestaje być spełniony, gdy licznik przekroczy 3.

**`while` a `if`.** Z lekcji 3.1 znasz `if`: sprawdza warunek i jeśli odpowiedź brzmi „tak”, wykonuje blok, a potem program idzie dalej. `while` sprawdza warunek tak samo, ale **po wykonaniu bloku wraca do warunku** i sprawdza go jeszcze raz, z nową wartością `lap`. Dopiero gdy odpowiedź brzmi „nie”, program pomija blok i wykonuje instrukcje stojące za pętlą.

- Warunek jest sprawdzany **przed każdym** wykonaniem ciała, z aktualną wartością licznika.
- Po wykonaniu ciała program nie przechodzi od razu za pętlę. **Wraca do warunku.**
- `while` **niczego sam nie zmienia**. Licznik rośnie tylko dlatego, że w ciele stoi instrukcja `lap = lap + 1;`.

Jedno wykonanie ciała pętli to **przebieg** (iteracja).

## 4. Tabela przebiegu

Przebieg pętli najlepiej widać w tabeli. Każdy wiersz to **jedno sprawdzenie warunku**:

| Sprawdzenie warunku | `lap` przy sprawdzeniu | `lap <= total_laps` | Ciało pętli | `lap` po ciele |
|---|---|---|---|---|
| 1 | 1 | `true` | wypisuje `Lap 1`, potem `lap = lap + 1;` | 2 |
| 2 | 2 | `true` | wypisuje `Lap 2`, potem `lap = lap + 1;` | 3 |
| 3 | 3 | `true` | wypisuje `Lap 3`, potem `lap = lap + 1;` | 4 |
| 4 | 4 | `false` | **nie wykonuje się**: pętla się kończy | — |

- Warunek sprawdzono **4 razy**, a ciało wykonało się **3 razy**. Ostatnie sprawdzenie to nie przebieg: jego wynik `false` kończy pętlę.
- Po trzecim przebiegu `lap` ma wartość 4. Pętla kończy się właśnie dlatego, że 4 nie spełnia warunku `lap <= 3`. Ta wartość zostaje w zmiennej, więc ostatnia linijka mówi `lap is now 4`.

**Twoja kolej.** Wyobraź sobie, że w programie stoi `const int total_laps{2};`. Przepisz tabelę i wypełnij ją dla tego przypadku: ile będzie sprawdzeń warunku, ile przebiegów i jaka będzie ostatnia linijka programu? Odpowiedź jest w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 5. Liczba okrążeń z wejścia

Teraz liczbę okrążeń podaje użytkownik. Żeby przykłady były krótkie, program przyjmuje tylko od 0 do 5 okrążeń. Dla innych liczb wypisuje komunikat i w ogóle nie zaczyna pętli. Zakładamy, że użytkownik wpisuje liczbę całkowitą.

<!-- example: laps_input -->
```cpp
#include <iostream>

int main() {
    int total_laps{0};

    std::cout << "Enter number of laps (0-5):\n";
    std::cin >> total_laps;

    if (total_laps >= 0 && total_laps <= 5) {
        int lap{1};

        while (lap <= total_laps) {
            std::cout << "Lap " << lap << "\n";
            lap = lap + 1;
        }

        std::cout << "Finished\n";
    } else {
        std::cout << "Number of laps must be from 0 to 5\n";
    }
}
```

- `if` z lekcji 3.5 sprawdza dane, zanim program zacznie powtarzanie. Pętla stoi w gałęzi dla dopuszczalnych danych.
- `total_laps` to liczba **zamówionych** okrążeń. Odczytana raz, w pętli się nie zmienia.
- `lap` to licznik, który **zmienia się** w każdym przebiegu.
- Liczba **wykonanych** przebiegów wynika z obu tych wartości.

**Przewidź.** Przepisz tabelę i wypełnij ją dla trzech uruchomień: 0, 1 i 3.

| `total_laps` | Wypisane okrążenia | Liczba przebiegów | `lap` po pętli |
|---|---|---|---|
| 0 | | | |
| 1 | | | |
| 3 | | | |

Potem uruchom program trzy razy, bez zmiany kodu.

<!-- input: laps_input -->
```text
0
```

<details>
<summary>Standardowe wyjście dla 0</summary>

<!-- output: laps_input -->
```text
Enter number of laps (0-5):
Finished
```

</details>

<!-- input: laps_input -->
```text
1
```

<details>
<summary>Standardowe wyjście dla 1</summary>

<!-- output: laps_input -->
```text
Enter number of laps (0-5):
Lap 1
Finished
```

</details>

<!-- input: laps_input -->
```text
3
```

<details>
<summary>Standardowe wyjście dla 3</summary>

<!-- output: laps_input -->
```text
Enter number of laps (0-5):
Lap 1
Lap 2
Lap 3
Finished
```

</details>

Uzupełnioną tabelę porównaj z częścią [Przykładowe rozwiązania](#przykładowe-rozwiązania).

**Zero przebiegów.** Dla 0 okrążeń pierwsze sprawdzenie warunku, `1 <= 0`, daje `false`. Ciało pętli nie wykonuje się **ani razu**, a program od razu przechodzi do `Finished`. To nie błąd: dla zera okrążeń tak właśnie ma być. Pętla `while` może wykonać się zero razy, bo warunek sprawdza **przed** pierwszym przebiegiem.

**A dla 9?** Przewidź, co wypisze program dla liczby spoza zakresu i czy pętla się wykona. Potem sprawdź.

<!-- input: laps_input -->
```text
9
```

<details>
<summary>Standardowe wyjście dla 9 i wyjaśnienie</summary>

<!-- output: laps_input -->
```text
Enter number of laps (0-5):
Number of laps must be from 0 to 5
```

Pętla nie wykonuje się, ale z innego powodu niż dla 0: program w ogóle do niej nie dochodzi, bo wybiera gałąź `else`.

</details>

## 6. Gdzie stoi zmiana licznika?

W tym programie zmiana licznika stoi **przed** wypisaniem, a nie po nim. Reszta się nie zmieniła:

<!-- example: laps_update_first -->
```cpp
#include <iostream>

int main() {
    const int total_laps{3};
    int lap{1};

    while (lap <= total_laps) {
        lap = lap + 1;
        std::cout << "Lap " << lap << "\n";
    }

    std::cout << "Finished, lap is now " << lap << "\n";
}
```

**Przewidź**, jakie numery okrążeń pojawią się teraz na ekranie. Przyjrzyj się szczególnie trzeciemu przebiegowi: jaką wartość ma `lap` tuż przed wypisaniem? Zapisz odpowiedź, a potem uruchom program.

<details>
<summary>Wynik programu i wyjaśnienie</summary>

<!-- output: laps_update_first -->
```text
Lap 2
Lap 3
Lap 4
Finished, lap is now 4
```

W trzecim przebiegu `lap = lap + 1;` zmienia 3 na 4. Wartość 4 nie spełnia już warunku `lap <= 3`, a mimo to program wypisuje `Lap 4`. **Program nie opuszcza ciała pętli w połowie**, gdy warunek przestaje być spełniony. Wykonuje ciało do końca, a warunek sprawdza dopiero potem, przy powrocie na górę. Wtedy 4 daje `false` i pętla się kończy.

Obie wersje wykonują ciało trzy razy, ale tylko pierwsza wypisuje okrążenia od 1 do 3. Kolejność instrukcji w ciele ma znaczenie: zmiana licznika na końcu ciała oznacza, że w całym przebiegu pracujesz jeszcze ze „starą” wartością.

</details>

## 7. Znajdź błąd: o jeden krok

Wymaganie: program wypisuje okrążenia **od 1 do `total_laps` włącznie**. W tej wersji ktoś zmienił warunek pętli:

<!-- example: laps_bug -->
```cpp
#include <iostream>

int main() {
    int total_laps{0};

    std::cout << "Enter number of laps (0-5):\n";
    std::cin >> total_laps;

    if (total_laps >= 0 && total_laps <= 5) {
        int lap{1};

        while (lap < total_laps) {
            std::cout << "Lap " << lap << "\n";
            lap = lap + 1;
        }

        std::cout << "Finished\n";
    } else {
        std::cout << "Number of laps must be from 0 to 5\n";
    }
}
```

1. Przeczytaj wymaganie i **przewidź**, co program **powinien** wypisać dla 0, 1 i 3 okrążeń.
2. Przewidź, co wypisze **ten** program. Pomoże Ci tabela przebiegu dla 1 okrążenia.
3. Uruchom program dla 0, 1 i 3.
4. Znajdź pierwszy przypadek, w którym wynik nie zgadza się z wymaganiem.
5. Popraw program.
6. Sprawdź ponownie wszystkie trzy przypadki.

Wyniki programu przed poprawką i poprawka są w części [Przykładowe rozwiązania](#przykładowe-rozwiązania). Zajrzyj tam po własnej próbie.

## 8. Pętla, która nie robi postępu

Warunek `lap <= total_laps` zależy od `lap`. Co, jeśli w ciele nie ma instrukcji, która zmienia `lap`? Ten fragment **przeanalizuj na papierze, nie uruchamiaj go**:

<!-- fragment -->
```cpp
const int total_laps{3};
int lap{1};

while (lap <= total_laps) {
    std::cout << "Lap " << lap << "\n";
}
```

| Sprawdzenie warunku | `lap` przy sprawdzeniu | `lap <= total_laps` | Ciało pętli | `lap` po ciele |
|---|---|---|---|---|
| 1 | 1 | `true` | wypisuje `Lap 1` | 1 |
| 2 | 1 | `true` | wypisuje `Lap 1` | 1 |
| 3 | 1 | `true` | wypisuje `Lap 1` | 1 |
| … | 1 | `true` | wypisuje `Lap 1` | 1 |

Każde sprawdzenie widzi tę samą wartość `lap`, więc daje ten sam wynik: `true`. Nic w ciele nie zbliża programu do odpowiedzi „nie”, więc pętla **nie ma jak się skończyć**. Program wypisywałby `Lap 1` bez końca. Taką pętlę nazywa się **nieskończoną**.

Dlatego przy każdej pętli zadawaj pytanie: **co zmienia się w ciele i czy ta zmiana prowadzi do tego, że warunek kiedyś przestanie być spełniony?** W tej lekcji odpowiedzią jest zmiana licznika. W kolejnych lekcjach zobaczysz pętle, które kończą się z innych powodów, bo ich warunek zależy od innych zmieniających się wartości.

## 9. Jak zatrzymać program, który działa za długo?

Jeśli przez pomyłkę uruchomisz pętlę, która się nie kończy, przerwij program:

- **w terminalu** (PowerShell, macOS i Linux): naciśnij <kbd>Ctrl</kbd> + <kbd>C</kbd>;
- **w CLionie:** kliknij przycisk **Stop** (czerwony kwadrat) w oknie **Run** albo na górnym pasku narzędzi.

Program zatrzymuje się, a Ty możesz poprawić kod i zbudować go ponownie. Niczego nie psujesz: przerywasz tylko własny program.

Program może też **czekać na dane**, jak w lekcji 2.6, wtedy również nic się nie dzieje. Zapytaj więc: czy program poprosił o dane, których jeszcze nie wpisano? Jeśli tak, to czeka. Jeśli dane wpisano, a na ekranie bez końca przybywa tych samych linijek, to pętla się nie kończy.

## 10. Misja: odliczanie

Przed rozpoczęciem wydarzenia program odlicza na głos. Użytkownik podaje długość odliczania `N`: liczbę całkowitą od 0 do 5. Program wypisuje kolejno `N`, `N - 1` i tak dalej, aż do `1`, każdą liczbę w osobnej linijce, a na końcu `Liftoff!`. Dla 0 nie wypisuje żadnej liczby, tylko `Liftoff!`.

Jeśli liczba jest spoza zakresu od 0 do 5, program wypisuje tylko `Countdown length must be from 0 to 5` i nie zaczyna odliczania. Zakładamy, że użytkownik wpisuje liczbę całkowitą.

W `cpp-workspace` utwórz katalog `countdown`, skopiuj do niego `CMakeLists.txt` z oryginalnego `lesson_05_first_program`, utwórz pusty `main.cpp` i napisz program samodzielnie.

Dla 3 standardowe wyjście ma być takie:

<!-- input: countdown -->
```text
3
```

<!-- output: countdown -->
```text
Enter countdown length:
3
2
1
Liftoff!
```

Dla 0:

<!-- input: countdown -->
```text
0
```

<!-- output: countdown -->
```text
Enter countdown length:
Liftoff!
```

**To nie jest pętla z okrążeń.** Licznik okrążeń zaczynał od 1, rósł i kończył po przekroczeniu górnego limitu. Licznik odliczania zaczyna od wartości podanej przez użytkownika, **maleje** i kończy przy dolnej granicy. Musisz samodzielnie zdecydować:

1. od jakiej wartości zaczyna licznik;
2. jaki warunek oznacza „licz dalej”;
3. jak zmienia się licznik w każdym przebiegu;
4. gdzie stoi `Liftoff!`, żeby pojawiło się dokładnie raz.

**Zanim napiszesz program**, przygotuj dwie rzeczy:

- tabelę przebiegu dla `N` = 3, z każdym sprawdzeniem warunku, także ostatnim;
- tabelę przypadków testowych: zero przebiegów, jeden przebieg, kilka przebiegów, największa dopuszczalna długość i wartości tuż poza zakresem z obu stron. Przy każdym przypadku zapisz oczekiwane standardowe wyjście.

### Kryterium sukcesu

- Program buduje się jako C++20, a jego standardowe wyjście dla 3 i 0 jest dokładnie takie jak powyżej.
- Dla każdej długości od 0 do 5 program wypisuje odpowiednie liczby i `Liftoff!`, a dla każdej innej liczby tylko `Countdown length must be from 0 to 5`.
- Odliczanie wykonuje pętla `while` z klamrami. Licznik zmienia się jawnym przypisaniem, w ciele pętli.
- Zakres jest sprawdzany przez `if`/`else`, zanim program zacznie odliczać.
- Tabela przebiegu i tabela przypadków powstały przed uruchomieniem programu.
- Ten sam program obsługuje wszystkie przypadki, bez zmiany kodu.
- Umiesz wyjaśnić, dlaczego pętla się kończy i dlaczego dla 0 ciało nie wykonuje się ani razu.

Gdy wynik się zgadza, możesz zapisać projekt w Gicie, jak w lekcji 1.5.

<details>
<summary>Podpowiedź 1</summary>

Warunek pętli zależy od licznika. Jeśli licznik się nie zmienia, warunek daje za każdym razem tę samą odpowiedź (punkt 8). Która instrukcja w ciele zmienia licznik?

</details>

<details>
<summary>Podpowiedź 2</summary>

Ustal dwie wartości graniczne: jaką liczbę program wypisuje jako pierwszą, a jaką jako ostatnią? Pierwsza podpowiada wartość początkową licznika. Ostatnia podpowiada, kiedy warunek ma jeszcze dawać „tak”.

</details>

<details>
<summary>Podpowiedź 3</summary>

Okrążenia rosły, a odliczanie maleje. Jak zapisać nową wartość licznika, która jest o 1 **mniejsza** od starej? Sprawdź w tabeli przebiegu dla `N` = 1, czy pętla wypisuje dokładnie jedną liczbę.

</details>

<details>
<summary>Pełna lista przypadków kontrolnych: otwórz po przygotowaniu własnej tabeli</summary>

| `N` | Standardowe wyjście po prośbie o dane | Co sprawdza |
|---|---|---|
| 3 | `3`, `2`, `1`, `Liftoff!` | kilka przebiegów |
| 0 | `Liftoff!` | zero przebiegów |
| 1 | `1`, `Liftoff!` | jeden przebieg |
| 5 | `5`, `4`, `3`, `2`, `1`, `Liftoff!` | największa dopuszczalna długość |
| -1 | `Countdown length must be from 0 to 5` | tuż pod zakresem |
| 6 | `Countdown length must be from 0 to 5` | tuż nad zakresem |

Przypadki 3 i 0 są sprawdzone wyżej, przy treści misji.

<!-- input: countdown -->
```text
1
```

<!-- output: countdown -->
```text
Enter countdown length:
1
Liftoff!
```

<!-- input: countdown -->
```text
5
```

<!-- output: countdown -->
```text
Enter countdown length:
5
4
3
2
1
Liftoff!
```

<!-- input: countdown -->
```text
-1
```

<!-- output: countdown -->
```text
Enter countdown length:
Countdown length must be from 0 to 5
```

<!-- input: countdown -->
```text
6
```

<!-- output: countdown -->
```text
Enter countdown length:
Countdown length must be from 0 to 5
```

</details>

Przykładowe rozwiązanie jest w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 11. Gdy coś pójdzie inaczej

| Co widzisz | Co to znaczy | Co zrobić |
|---|---|---|
| Ta sama linijka pojawia się bez końca | Licznik się nie zmienia albo zmienia się w złą stronę, więc warunek zawsze daje „tak”. | Przerwij program (punkt 9). Wypełnij tabelę przebiegu dla dwóch, trzech sprawdzeń i znajdź instrukcję, która powinna zbliżać licznik do końca. |
| Brakuje ostatniej liczby albo pojawia się jedna za dużo | Błąd o jeden krok: zła wartość początkowa albo `<` zamiast `<=` (lub odwrotnie). | Sprawdź przypadek z jednym przebiegiem i największą wartość. Wypełnij tabelę przebiegu. |
| Pętla nie wykonuje się ani razu, choć powinna | Warunek jest fałszywy już przy pierwszym sprawdzeniu. | Wstaw do warunku wartość początkową licznika i sprawdź, czy odpowiedź brzmi „tak”. |
| Wypisane wartości są przesunięte o jeden | Zmiana licznika stoi przed instrukcją, która go wypisuje. | Zastanów się, którą wartość ma pokazać przebieg: przed zmianą czy po niej (punkt 6). |
| Końcowy komunikat pojawia się kilka razy | Stoi w ciele pętli, przed zamykającą klamrą. | Przenieś go za `}` pętli. |
| Program nic nie robi i czeka | Czeka na dane, jak w lekcji 2.6. | Wpisz liczbę i naciśnij **Enter**. |
| Błąd kompilacji przy `while` | Zwykle brakuje nawiasu okrągłego albo klamry. | Warunek w `( )`, ciało w `{ }`. Każdy nawias i każda klamra ma swoją parę. |

## 12. Wyjaśnij

Odpowiedz własnymi słowami, najlepiej na piśmie. Dopiero potem porównaj z przykładową odpowiedzią.

**1.** Kiedy dokładnie `while` sprawdza swój warunek?

<details>
<summary>Przykładowa odpowiedź</summary>

Przed każdym przebiegiem: pierwszy raz zanim ciało wykona się po raz pierwszy, a potem za każdym razem, gdy program po wykonaniu ciała wraca na górę pętli.

</details>

**2.** Dlaczego `while` może wykonać się zero razy?

<details>
<summary>Przykładowa odpowiedź</summary>

Bo warunek jest sprawdzany przed pierwszym przebiegiem. Jeśli od razu daje `false`, jak `1 <= 0` dla zera okrążeń, ciało zostaje pominięte, a program idzie dalej za pętlą.

</details>

**3.** Dlaczego w punkcie 2 po zakończeniu pętli `lap` wynosi 4?

<details>
<summary>Przykładowa odpowiedź</summary>

Bo w trzecim przebiegu `lap = lap + 1;` zmienia 3 na 4. Przy czwartym sprawdzeniu 4 nie spełnia `lap <= 3`, więc pętla się kończy, a wartość 4 zostaje w zmiennej.

</details>

**4.** Czy zmiana licznika na wartość, która nie spełnia warunku, natychmiast przerywa bieżący przebieg?

<details>
<summary>Przykładowa odpowiedź</summary>

Nie. Program wykonuje ciało do końca, a warunek sprawdza dopiero przy powrocie na górę pętli. Dlatego w punkcie 6 pojawiło się `Lap 4`.

</details>

**5.** Co się stanie, jeśli licznik nie będzie się zmieniał?

<details>
<summary>Przykładowa odpowiedź</summary>

Każde sprawdzenie warunku zobaczy tę samą wartość i da ten sam wynik. Jeśli był to `true`, pętla nie ma jak się skończyć i program powtarza ciało bez końca.

</details>

**6.** Czym różni się `lap < total_laps` od `lap <= total_laps`? Który przypadek z punktu 7 tego nie ujawnia?

<details>
<summary>Przykładowa odpowiedź</summary>

`lap < total_laps` daje `false` już wtedy, gdy `lap` równa się `total_laps`, więc pomija ostatnie okrążenie: dla 3 wypisuje tylko dwa. `<=` dopuszcza też równość. Dla 0 oba warianty niczego nie wypisują, więc ten przypadek błędu nie ujawnia. Ujawniają go 1 i 3.

</details>

**7.** Dlaczego licznik w misji odliczania się zmniejsza, a nie zwiększa?

<details>
<summary>Przykładowa odpowiedź</summary>

Bo odliczanie wypisuje coraz mniejsze liczby i kończy się przy dolnej granicy. Zmniejszanie licznika przybliża go do wartości, przy której warunek przestaje być spełniony. Zwiększanie oddalałoby go od niej i pętla nigdy by się nie skończyła.

</details>

**8.** Co sprawia, że po zakończeniu pętli program działa dalej?

<details>
<summary>Przykładowa odpowiedź</summary>

Gdy warunek daje `false`, program pomija ciało i wykonuje instrukcje stojące za zamykającą klamrą pętli, od góry do dołu, jak dotąd. Pętla nie kończy programu, kończy tylko powtarzanie.

</details>

## Podsumowanie

- `while (warunek) { … }` powtarza ciało pętli, dopóki warunek jest spełniony.
- Warunek jest sprawdzany **przed każdym** przebiegiem. Po wykonaniu ciała program wraca do warunku. Gdy odpowiedź brzmi „nie”, idzie dalej za pętlą.
- Pętla z licznikiem ma cztery części: wartość początkową przed pętlą, warunek, ciało i zmianę licznika w ciele. `while` niczego sam nie zmienia.
- Liczba przebiegów wynika z wartości początkowej, warunku i zmiany. Warunek sprawdza się zawsze o jeden raz więcej, niż wykonuje się ciało: ostatnie sprawdzenie daje `false`.
- Pętla może wykonać się zero razy, gdy warunek jest fałszywy od początku.
- Program nie opuszcza ciała w połowie. Warunek jest sprawdzany dopiero po wykonaniu całego ciała.
- Jeśli nic w ciele nie zbliża warunku do odpowiedzi „nie”, pętla się nie kończy. Przerwiesz program przez <kbd>Ctrl</kbd> + <kbd>C</kbd> w terminalu albo przyciskiem **Stop** w CLionie.
- Pętlę testuj dla zera przebiegów, jednego, kilku i największej dopuszczalnej wartości. Błąd o jeden krok często ujawnia dopiero jeden z tych przypadków.

## Co dalej

Twoja pętla liczy już przebiegi. W lekcji 4.2 nauczy się w każdym przebiegu **dodawać** kolejną wartość do wyniku, na przykład sumować minuty treningu z kolejnych dni: [Lekcja 4.2: Sumowanie i akumulatory](lesson_02_sums_and_accumulators.md).

---

## Przykładowe rozwiązania

Zajrzyj tutaj **po własnej próbie**. Twoje nazwy mogą się różnić, jeśli standardowe wyjście jest takie, jak wymagane.

<details>
<summary>Punkt 4: tabela przebiegu dla dwóch okrążeń</summary>

| Sprawdzenie warunku | `lap` przy sprawdzeniu | `lap <= total_laps` | Ciało pętli | `lap` po ciele |
|---|---|---|---|---|
| 1 | 1 | `true` | wypisuje `Lap 1`, potem `lap = lap + 1;` | 2 |
| 2 | 2 | `true` | wypisuje `Lap 2`, potem `lap = lap + 1;` | 3 |
| 3 | 3 | `false` | nie wykonuje się: pętla się kończy | — |

Trzy sprawdzenia warunku, dwa przebiegi. Ostatnia linijka programu to `Finished, lap is now 3`.

</details>

<details>
<summary>Punkt 5: zero, jeden i trzy przebiegi</summary>

| `total_laps` | Wypisane okrążenia | Liczba przebiegów | `lap` po pętli |
|---|---|---|---|
| 0 | żadne | 0 | 1 |
| 1 | `Lap 1` | 1 | 2 |
| 3 | `Lap 1`, `Lap 2`, `Lap 3` | 3 | 4 |

`lap` po pętli jest zawsze o 1 większe od liczby okrążeń, bo pętla kończy się przy pierwszej wartości, która przekracza `total_laps`. Program tej wartości nie wypisuje. Możesz ją zobaczyć, dopisując na chwilę `std::cout` za pętlą.

</details>

<details>
<summary>Punkt 7: wyniki przed poprawką i poprawka</summary>

Przed poprawką, dla 0, 1 i 3:

<!-- input: laps_bug -->
```text
0
```

<!-- output: laps_bug -->
```text
Enter number of laps (0-5):
Finished
```

<!-- input: laps_bug -->
```text
1
```

<!-- output: laps_bug -->
```text
Enter number of laps (0-5):
Finished
```

<!-- input: laps_bug -->
```text
3
```

<!-- output: laps_bug -->
```text
Enter number of laps (0-5):
Lap 1
Lap 2
Finished
```

- **Pierwszy niezgodny przypadek** to 1: wymaganie mówi `Lap 1`, a program nie wypisuje żadnego okrążenia. Dla 3 brakuje `Lap 3`.
- **Dlaczego 0 nie wystarczyło:** dla zera obie wersje warunku dają przy pierwszym sprawdzeniu `false` (`1 < 0` i `1 <= 0`), więc obie poprawnie nie wypisują niczego. Jeden test nie wystarczył.
- **Przyczyna:** `lap < total_laps` jest fałszywe, gdy `lap` **równa się** `total_laps`, więc ostatnie okrążenie zostaje pominięte. Wymaganie mówi „włącznie”.
- **Poprawka:** `while (lap <= total_laps)`. Poprawiony program to program z punktu 5. Jego wyniki dla 0, 1 i 3 są sprawdzone tam.

</details>

<details>
<summary>Punkt 10: misja, odliczanie</summary>

<!-- example: countdown -->
```cpp
#include <iostream>

int main() {
    int length{0};

    std::cout << "Enter countdown length:\n";
    std::cin >> length;

    if (length >= 0 && length <= 5) {
        int count{length};

        while (count >= 1) {
            std::cout << count << "\n";
            count = count - 1;
        }

        std::cout << "Liftoff!\n";
    } else {
        std::cout << "Countdown length must be from 0 to 5\n";
    }
}
```

| Sprawdzenie warunku | `count` przy sprawdzeniu | `count >= 1` | Ciało pętli | `count` po ciele |
|---|---|---|---|---|
| 1 | 3 | `true` | wypisuje `3`, potem `count = count - 1;` | 2 |
| 2 | 2 | `true` | wypisuje `2`, potem `count = count - 1;` | 1 |
| 3 | 1 | `true` | wypisuje `1`, potem `count = count - 1;` | 0 |
| 4 | 0 | `false` | nie wykonuje się: pętla się kończy | — |

- **Wartość początkowa:** pierwszą wypisaną liczbą jest `N`, więc licznik zaczyna od odczytanej długości.
- **Warunek:** ostatnią wypisaną liczbą jest 1, więc pętla trwa, dopóki licznik jest co najmniej 1. Warunek `count > 0` działa tak samo dla liczb całkowitych.
- **Zmiana:** `count = count - 1;` zmniejsza licznik i przybliża go do 0, przy którym warunek daje `false`.
- **`Liftoff!`** stoi za pętlą, więc pojawia się dokładnie raz, także dla 0, gdy ciało nie wykonuje się ani razu.
- Zamiast osobnego licznika `count` możesz zmniejszać samo `length`. Osobna zmienna zostawia odczytaną długość bez zmian, gdyby była potrzebna później.

</details>

**Poprzednia lekcja:** [Lekcja 3.6: Program podejmuje decyzje (sprawdzian Modułu 3)](../module_03_decisions_and_conditions/lesson_06_the_program_decides.md) · **Następna lekcja:** [Lekcja 4.2: Sumowanie i akumulatory](lesson_02_sums_and_accumulators.md) · [Opis kursu](../../README.md)

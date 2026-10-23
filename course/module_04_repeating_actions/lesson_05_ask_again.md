# Lekcja 4.5: Ponawianie pytania o poprawną wartość

**Polski** · [English](lesson_05_ask_again.en.md) · [Opis kursu](../../README.md)

> **Moduł 4, lekcja 5** · około 75–90 minut
> **Potrzebujesz:** katalogu `cpp-workspace` i oryginalnego projektu `lesson_05_first_program`, jak dotąd. Debugger nie jest w tej lekcji potrzebny.
> **Wersja pilotażowa.** Programy z tej lekcji sprawdzamy automatycznie na Windowsie, Ubuntu i macOS, także z podanymi danymi wejściowymi. Wpisywanie danych w oknie **Run** CLiona opisujemy bez ręcznego sprawdzenia na każdym systemie.

## Zanim zaczniesz

Ta lekcja zakłada, że:

- sprawdzasz poprawnie odczytaną wartość przez `if` i odróżniasz złą wartość od nieudanego odczytu (lekcja 3.5);
- łączysz warunki przez `&&`, `||` i `!` (lekcja 3.4);
- piszesz pętlę `while`, która powtarza działanie, dopóki cel nie jest osiągnięty, i wyjaśniasz, dlaczego się kończy (lekcje 4.1 i 4.4);
- zwiększasz licznik przez `++` (lekcja 4.3).

## Sytuacja

Program pyta o liczbę sesji nauki. Dopuszczalne są wartości od 1 do 5. W Module 3 umiesz już sprawdzić odczytaną liczbę: jeśli pasuje, program ją przyjmuje, a jeśli nie, wypisuje komunikat i kończy pracę.

Teraz wymaganie się zmienia: **jeśli użytkownik poda liczbę spoza zakresu, program ma zapytać ponownie**. Program ma powtarzać pytanie, dopóki nie dostanie odpowiedniej wartości, czyli dopóki nie osiągnie celu, jak w lekcji 4.4. Po drodze wyjdzie na jaw coś nowego: czasem nie da się w ogóle odczytać liczby. Program musi to zauważyć, zanim zacznie sprawdzać wartość.

Po tej lekcji będziesz:

- ponawiać pytanie w pętli `while`, dopóki odczytana wartość nie spełnia wymagań;
- sprawdzać przez `std::cin.fail()`, czy odczyt liczby się udał, i rozumieć wywołanie funkcji składowej przez kropkę;
- sprawdzać wartość dopiero po udanym odczycie;
- kończyć pętlę z dwóch powodów: po przyjęciu wartości albo po nieudanym odczycie;
- wyjaśniać, dlaczego koniec danych nie może prowadzić do pytania bez końca;
- odróżniać wartość odrzuconą od nieudanego odczytu i planować testy z kilkoma kolejnymi próbami.

## 1. Przygotuj projekt

W `cpp-workspace` utwórz katalog `lesson_4_5` i skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program`. Programy z punktów 3–7 wpisujesz w `main.cpp` tego katalogu.

## 2. Jedno sprawdzenie to za mało

Tak sprawdzało się wartość w Module 3:

<!-- fragment -->
```cpp
std::cout << "Enter session count (1-5):\n";
std::cin >> sessions;

if (sessions >= 1 && sessions <= 5) {
    std::cout << "Accepted sessions: " << sessions << "\n";
} else {
    std::cout << "Session count out of range\n";
}
```

**Zastanów się:** co musiałoby się zmienić, żeby po złej wartości program zapytał jeszcze raz? `if` wybiera jedną drogę i program idzie dalej. Do odczytu nie wraca. Żeby zapytać ponownie, program musi **wrócić do odczytu**. A powrót do tego samego fragmentu kodu to zadanie pętli.

## 3. Pytaj, dopóki wartość jest zła

Pierwsza, **uproszczona** wersja zakłada, że każdy odczyt liczby się udaje i że użytkownik w końcu poda wartość z zakresu. To nie jest jeszcze rozwiązanie kompletne. Pokazuje tylko, jak pętla wraca do pytania.

<!-- example: sessions_simple -->
```cpp
#include <iostream>

int main() {
    int sessions{0};

    std::cout << "Enter session count (1-5):\n";
    std::cin >> sessions;

    while (sessions < 1 || sessions > 5) {
        std::cout << "Session count out of range\n";
        std::cout << "Enter session count (1-5):\n";
        std::cin >> sessions;
    }

    std::cout << "Accepted sessions: " << sessions << "\n";
}
```

**Przewidź**, co wypisze program, gdy użytkownik poda najpierw 0, a potem 3. A gdy poda 9, potem 6, a potem 2? Potem sprawdź.

<!-- input: sessions_simple -->
```text
0
3
```

<details>
<summary>Standardowe wyjście dla 0 i 3</summary>

<!-- output: sessions_simple -->
```text
Enter session count (1-5):
Session count out of range
Enter session count (1-5):
Accepted sessions: 3
```

</details>

<!-- input: sessions_simple -->
```text
9
6
2
```

<details>
<summary>Standardowe wyjście dla 9, 6 i 2</summary>

<!-- output: sessions_simple -->
```text
Enter session count (1-5):
Session count out of range
Enter session count (1-5):
Session count out of range
Enter session count (1-5):
Accepted sessions: 2
```

</details>

Warunek `while` sprawdza wartość **po każdej próbie**. Dopóki odczytana liczba jest spoza zakresu, ciało pętli wypisuje komunikat i odczytuje kolejną liczbę. Pierwsza wartość z zakresu sprawia, że warunek daje `false`, i pętla się kończy.

**A co, jeśli zamiast liczby pojawi się tekst albo dane się skończą?** Wtedy odczyt liczby się **nie udaje**. Strumień wejścia zapamiętuje, że odczyt się nie powiódł, i każdy kolejny odczyt tą samą metodą też od razu się nie udaje, bez czekania na nowe dane. Zmienna `sessions` nie dostaje nowej, wpisanej przez użytkownika wartości, a warunek pętli sprawdza wartość, na której nie można polegać. Taka pętla mogłaby pytać bez końca. Dlatego ten program uruchamiamy tylko dla danych, które kończą się poprawną liczbą. Kompletna wersja musi najpierw sprawdzać, **czy odczyt się udał**.

## 4. Czy odczyt się udał? `std::cin.fail()`

`std::cin` to standardowe wejście programu. Po każdym odczycie można zapytać, czy się powiódł:

<!-- fragment -->
```cpp
std::cin >> sessions;

if (std::cin.fail()) {
    std::cout << "Input could not be read\n";
}
```

- `std::cin` reprezentuje standardowy strumień wejścia, z którego program czyta dane.
- **Kropka** po `std::cin` pozwala odwołać się do funkcji związanej z tym obiektem, czyli do jego **funkcji składowej**. `std::cin.fail()` to pytanie zadane strumieniowi `std::cin`.
- `fail` to nazwa tej funkcji. **Nawiasy** `()` oznaczają, że funkcja zostaje wywołana, czyli że pytanie zostaje zadane teraz.
- Wynik jest typu `bool`: `true`, gdy strumień jest w stanie błędu odczytu, i `false`, gdy ostatnie odczyty się udały. Dlatego `std::cin.fail()` może stać w warunku `if`.

**Co dokładnie oznacza `true`?** Że odczyt się nie powiódł. **Nie** mówi, dlaczego. Przyczyną może być tekst zamiast liczby, ale też to, że dane po prostu się skończyły. W tej lekcji tych przyczyn nie rozróżniamy, dlatego program wypisuje neutralny komunikat `Input could not be read`, a nie „wpisano tekst” albo „koniec danych”.

## 5. Dwie przyczyny zakończenia

Kompletny program może zakończyć pętlę z dwóch powodów i każdy z nich ma własną zmienną `bool`:

- `accepted`: otrzymaliśmy wartość spełniającą wymagania;
- `read_failed`: odczyt się nie powiódł.

To zwykłe zmienne `bool`, czyli **flagi** opisujące stan programu, a nie nowy typ. Pętla działa, dopóki żadna z nich nie jest ustawiona: `!accepted && !read_failed`.

<!-- example: sessions -->
```cpp
#include <iostream>

int main() {
    int sessions{0};
    bool accepted{false};
    bool read_failed{false};

    while (!accepted && !read_failed) {
        std::cout << "Enter session count (1-5):\n";
        std::cin >> sessions;

        if (std::cin.fail()) {
            read_failed = true;
        } else if (sessions >= 1 && sessions <= 5) {
            accepted = true;
        } else {
            std::cout << "Session count out of range\n";
        }
    }

    if (accepted) {
        std::cout << "Accepted sessions: " << sessions << "\n";
    } else {
        std::cout << "Input could not be read\n";
    }
}
```

W każdym przebiegu kolejność jest zawsze taka sama:

1. Program wypisuje pytanie.
2. Próbuje odczytać liczbę, **raz na przebieg**.
3. Sprawdza, czy odczyt się udał.
4. Jeśli nie, ustawia `read_failed` i nie ponawia pytania.
5. Jeśli tak, sprawdza, czy liczba należy do zakresu.
6. Jeśli nie należy, wypisuje komunikat. Flagi się nie zmieniają, więc pętla pyta ponownie.
7. Jeśli należy, ustawia `accepted` i pętla się kończy.

**Sprawdzenie zakresu nie zastępuje sprawdzenia odczytu.** Łańcuch `if`/`else if` sprawdza najpierw `std::cin.fail()`. Do porównania `sessions` z zakresem program dochodzi tylko wtedy, gdy odczyt się udał. Po nieudanym odczycie żadna decyzja nie opiera się na wartości `sessions`, bo program nie wie, czy ta wartość ma cokolwiek wspólnego z danymi użytkownika. Kolejność warunków w łańcuchu ma znaczenie, tak jak w lekcji 3.3.

Po pętli wystarczy sprawdzić jedną flagę: jeśli `accepted` nie jest ustawione, pętla musiała zakończyć się przez nieudany odczyt.

## 6. Prześledź kolejne próby

Użytkownik wpisuje kolejno `0`, `6` i `3`. **Przewidź**: przepisz tabelę i wypełnij ją, zanim uruchomisz program.

| Próba | Odczytana wartość | Odczyt udany? | Spełnia wymagania? | `accepted` po próbie | `read_failed` po próbie | Następne pytanie? |
|---|---|---|---|---|---|---|
| 1 | | | | | | |
| 2 | | | | | | |
| 3 | | | | | | |

Ile było prób odczytu, a ile wartości odrzuconych? Wypełnioną tabelę znajdziesz w części [Przykładowe rozwiązania](#przykładowe-rozwiązania). Teraz uruchom program dla tych danych, a także dla 3 i 5 podanych od razu.

<!-- input: sessions -->
```text
0
6
3
```

<details>
<summary>Standardowe wyjście dla 0, 6 i 3</summary>

<!-- output: sessions -->
```text
Enter session count (1-5):
Session count out of range
Enter session count (1-5):
Session count out of range
Enter session count (1-5):
Accepted sessions: 3
```

</details>

<!-- input: sessions -->
```text
3
```

<details>
<summary>Standardowe wyjście dla 3</summary>

<!-- output: sessions -->
```text
Enter session count (1-5):
Accepted sessions: 3
```

</details>

<!-- input: sessions -->
```text
5
```

<details>
<summary>Standardowe wyjście dla 5</summary>

<!-- output: sessions -->
```text
Enter session count (1-5):
Accepted sessions: 5
```

</details>

## 7. Gdy dane się kończą

Dane nie zawsze wpisuje człowiek, który poda kolejną liczbę. Mogą pochodzić z pliku albo z automatycznego testu, a wtedy po prostu **się kończą**. Tak sprawdzamy programy z tego kursu: dane są przekazywane programowi w całości, a po ostatniej linijce więcej już nie przychodzi.

Program dostaje tylko `0`. **Przewidź**: ile razy zapyta o liczbę, co wypisze i czy się zakończy?

<!-- input: sessions -->
```text
0
```

<details>
<summary>Standardowe wyjście, gdy po 0 dane się kończą</summary>

<!-- output: sessions -->
```text
Enter session count (1-5):
Session count out of range
Enter session count (1-5):
Input could not be read
```

| Próba | Co się dzieje | `accepted` | `read_failed` | Następne pytanie? |
|---|---|---|---|---|
| 1 | odczyt udany: 0, poza zakresem, komunikat | `false` | `false` | tak |
| 2 | odczyt **nieudany**: nie ma już danych | `false` | `true` | nie: pętla się kończy |

Program pyta po raz drugi, próbuje odczytać liczbę, stwierdza, że odczyt się nie udał, i kończy pracę normalnie. To nie jest „kolejna zła liczba”. Program niczego nie odczytał.

</details>

Najkrótszy przypadek: danych nie ma od samego początku. Program dostaje tylko pustą linijkę i żadnej liczby.

<!-- input: sessions -->
```text
```

<details>
<summary>Standardowe wyjście, gdy nie ma żadnej liczby</summary>

<!-- output: sessions -->
```text
Enter session count (1-5):
Input could not be read
```

</details>

**Program z pętlą wejścia nie może pytać bez końca, gdy skończą się dane.** Nie może zakładać, że nowe dane na pewno przyjdą. Ten program kończy się sam, dzięki fladze `read_failed`, a nie dlatego, że ktoś go przerwał. Automatyczne testy kursu mają wprawdzie limit czasu, ale ten limit tylko **wykrywa** program, który się nie kończy. Poprawny program nigdy na nim nie polega.

## 8. Tekst zamiast liczby

Program prosi o liczbę, a użytkownik wpisuje `abc`. **Przewidź**, co się stanie. A jeśli najpierw wpisze `7`, a potem `abc`?

<!-- input: sessions -->
```text
abc
```

<details>
<summary>Standardowe wyjście dla abc</summary>

<!-- output: sessions -->
```text
Enter session count (1-5):
Input could not be read
```

</details>

<!-- input: sessions -->
```text
7
abc
```

<details>
<summary>Standardowe wyjście dla 7, a potem abc</summary>

<!-- output: sessions -->
```text
Enter session count (1-5):
Session count out of range
Enter session count (1-5):
Input could not be read
```

</details>

Po `abc` odczyt liczby się nie udaje, więc program nie sprawdza wartości i nie pyta ponownie. To świadome ograniczenie tej lekcji. Po nieudanym odczycie strumień jest w stanie błędu i kolejny taki sam odczyt też by się nie udał. W lekcji 4.6 nauczysz się przywracać strumień do stanu, w którym można czytać dalej, i odróżniać tekst od końca danych.

Jedno uczciwe zastrzeżenie: odczyt liczby przez `>>` nie sprawdza całej wpisanej linijki. Po wpisaniu `12abc` program odczyta liczbę 12, a znaki `abc` zostaną w strumieniu na później. Sprawdzanie całych linijek nie należy do tej lekcji.

## 9. Wartość odrzucona, nieudany odczyt, koniec danych

| Sytuacja | Przykład | Co się stało | Co robi program |
|---|---|---|---|
| **Wartość odrzucona** | `6` | Odczyt się udał: to poprawna liczba `int`, ale nie spełnia wymagań. | Wypisuje komunikat i bezpiecznie pyta ponownie. |
| **Nieudany odczyt** | `abc` | Odczyt liczby się nie powiódł. Strumień jest w stanie błędu i nie pozwala po prostu powtórzyć takiego samego odczytu. | Kończy pracę z komunikatem `Input could not be read`. |
| **Koniec danych** | po `0` nic więcej | Dane się skończyły, więc kolejny odczyt się nie udaje. Program nie może zakładać, że przyjdą nowe. | To też nieudany odczyt: ten sam komunikat i to samo zakończenie. |

W tej lekcji oba rodzaje nieudanego odczytu kończą się tak samo, bezpiecznie. W lekcji 4.6 ten model się rozszerzy.

## 10. Przeanalizuj: pętla, która nie sprawdza odczytu

Ten fragment **przeanalizuj na papierze, nie uruchamiaj go**. Ma tylko jedną flagę i sprawdza wyłącznie zakres:

<!-- fragment -->
```cpp
bool accepted{false};

while (!accepted) {
    std::cout << "Enter session count (1-5):\n";
    std::cin >> sessions;

    if (sessions >= 1 && sessions <= 5) {
        accepted = true;
    } else {
        std::cout << "Session count out of range\n";
    }
}
```

Odpowiedz na pytania, zanim zajrzysz do rozwiązania:

1. Co się stanie, gdy użytkownik od razu poda poprawną liczbę, na przykład 3?
2. Co się stanie, gdy poda liczbę spoza zakresu, na przykład 6?
3. Co się stanie, gdy odczyt się nie powiedzie, na przykład po `abc` albo po końcu danych?
4. Dlaczego kolejny odczyt w następnym przebiegu nie rozwiązuje problemu sam z siebie?
5. Jakie dodatkowe sprawdzenie jest konieczne?

Odpowiedzi i tabela przebiegu są w części [Przykładowe rozwiązania](#przykładowe-rozwiązania). Poprawiony, bezpieczny program to program z punktu 5.

## 11. Misja: wybór stanowiska w pracowni

W pracowni dostępne są stanowiska od 1 do 3 i od 7 do 9. Stanowiska od 4 do 6 są niedostępne. Program prosi o numer stanowiska. Jeśli wybrane stanowisko jest niedostępne, informuje o tym i pyta ponownie. Jeśli jest dostępne, kończy pytanie i wypisuje wybrane stanowisko oraz liczbę **poprawnie odczytanych, ale niedostępnych** numerów, które odrzucił przed wyborem. Jeśli odczyt numeru się nie powiedzie, program kończy pracę bez zatwierdzenia wyboru.

**Wymagania:**

- Pętla `while` z dwiema przyczynami zakończenia: wybrane stanowisko albo nieudany odczyt.
- W każdym przebiegu program wypisuje `Enter station number:` i odczytuje liczbę całkowitą.
- Najpierw sprawdza, czy odczyt się udał. Dopiero potem sprawdza dostępność stanowiska.
- Dla niedostępnego numeru wypisuje `Station unavailable` i pyta ponownie.
- Liczy wyłącznie odrzucone wartości liczbowe. Nieudany odczyt nie jest odrzuconym numerem.
- Po wyborze wypisuje `Selected station: N` i `Rejected selections: R`.
- Po nieudanym odczycie wypisuje tylko `Input could not be read`, bez raportu wyboru.

W `cpp-workspace` utwórz katalog `station_choice`, skopiuj do niego `CMakeLists.txt` z oryginalnego `lesson_05_first_program`, utwórz pusty `main.cpp` i napisz program samodzielnie.

Standardowe wyjście dla czterech sytuacji ma być takie. Wybór od razu, przy wpisanym `2`:

<!-- input: station_choice -->
```text
2
```

<!-- output: station_choice -->
```text
Enter station number:
Selected station: 2
Rejected selections: 0
```

Jeden niedostępny numer, przy wpisanych `5` i `8`:

<!-- input: station_choice -->
```text
5
8
```

<!-- output: station_choice -->
```text
Enter station number:
Station unavailable
Enter station number:
Selected station: 8
Rejected selections: 1
```

Dane kończą się po wpisanym `5`:

<!-- input: station_choice -->
```text
5
```

<!-- output: station_choice -->
```text
Enter station number:
Station unavailable
Enter station number:
Input could not be read
```

Tekst zamiast numeru, czyli wpisane `abc`:

<!-- input: station_choice -->
```text
abc
```

<!-- output: station_choice -->
```text
Enter station number:
Input could not be read
```

**To nie jest program z punktu 5 z nowymi nazwami.** Tam dopuszczalne wartości tworzyły jeden ciągły zakres, a program tylko przyjmował albo odrzucał wartość. Tutaj:

- dostępne stanowiska należą do **dwóch oddzielnych** zakresów, więc warunek dostępności musisz zbudować samodzielnie z `&&` i `||`;
- program prowadzi dodatkowo **licznik odrzuceń**, który zmienia się tylko w jednej z trzech sytuacji;
- raport wyboru i komunikat o nieudanym odczycie mają różne znaczenie i nigdy nie pojawiają się razem.

**Zanim napiszesz program**, przygotuj dwie rzeczy:

- tabelę przebiegu dla danych `0`, `5`, `2`: próba, odczytana wartość, czy odczyt się udał, czy stanowisko jest dostępne, obie flagi i licznik odrzuceń po próbie;
- tabelę przypadków testowych: wszystkie cztery granice obu zakresów, wartości tuż obok nich, liczba ujemna, kilka odrzuceń przed wyborem, nieudany odczyt po odrzuceniu i koniec danych po kilku odrzuceniach. Przy każdym przypadku zapisz oczekiwane standardowe wyjście.

### Kryterium sukcesu

- Program buduje się jako C++20, a jego standardowe wyjście dla czterech powyższych sytuacji jest dokładnie takie jak pokazano.
- Pętla `while` kończy się z dwóch nazwanych powodów zapisanych w zmiennych `bool`. Odczyt odbywa się raz na przebieg.
- Powodzenie odczytu jest sprawdzane przez `std::cin.fail()` **przed** sprawdzeniem dostępności. Po nieudanym odczycie żadna decyzja nie opiera się na wartości numeru.
- Warunek dostępności przyjmuje dokładnie stanowiska 1–3 i 7–9.
- Licznik odrzuceń rośnie tylko po udanym odczycie niedostępnego numeru.
- Po nieudanym odczycie nie pojawia się `Selected station` ani `Rejected selections`.
- Tabela przebiegu i tabela przypadków powstały przed uruchomieniem programu.
- Umiesz wyjaśnić, dlaczego program kończy się także wtedy, gdy dane się skończą.

Gdy wynik się zgadza, możesz zapisać projekt w Gicie, jak w lekcji 1.5.

<details>
<summary>Podpowiedź 1</summary>

Zastanów się, jakie dwa zdarzenia mogą zakończyć ponawianie pytania.

</details>

<details>
<summary>Podpowiedź 2</summary>

Warunek dostępności stanowiska obejmuje dwa oddzielne zakresy. Każdy zakres wymaga dwóch porównań.

</details>

<details>
<summary>Podpowiedź 3</summary>

Licznik odrzuceń powinien się zmieniać tylko po udanym odczycie wartości, która nie spełnia wymagań.

</details>

<details>
<summary>Pełna lista przypadków kontrolnych: otwórz po przygotowaniu własnej tabeli</summary>

| Dane | Wynik | Odrzucenia | Co sprawdza |
|---|---|---|---|
| `2` | wybór 2 | 0 | dostępny numer od razu |
| `5`, `8` | wybór 8 | 1 | jedno odrzucenie |
| `5`, koniec danych | `Input could not be read` | — | koniec danych po odrzuceniu |
| `abc` | `Input could not be read` | — | tekst zamiast liczby |
| `1` | wybór 1 | 0 | dolna granica pierwszego zakresu |
| `3` | wybór 3 | 0 | górna granica pierwszego zakresu |
| `7` | wybór 7 | 0 | dolna granica drugiego zakresu |
| `9` | wybór 9 | 0 | górna granica drugiego zakresu |
| `4`, `7` | wybór 7 | 1 | początek niedostępnego obszaru |
| `6`, `9` | wybór 9 | 1 | koniec niedostępnego obszaru |
| `0`, `5`, `2` | wybór 2 | 2 | dwa odrzucenia |
| `-1`, `3` | wybór 3 | 1 | liczba ujemna |
| `4`, `abc` | `Input could not be read` | — | nieudany odczyt po odrzuceniu |
| `4`, `6`, koniec danych | `Input could not be read` | — | koniec danych po dwóch odrzuceniach |
| brak danych | `Input could not be read` | — | koniec danych przed pierwszą liczbą |

Pierwsze cztery przypadki są sprawdzone wyżej, przy treści misji.

<!-- input: station_choice -->
```text
1
```

<!-- output: station_choice -->
```text
Enter station number:
Selected station: 1
Rejected selections: 0
```

<!-- input: station_choice -->
```text
3
```

<!-- output: station_choice -->
```text
Enter station number:
Selected station: 3
Rejected selections: 0
```

<!-- input: station_choice -->
```text
7
```

<!-- output: station_choice -->
```text
Enter station number:
Selected station: 7
Rejected selections: 0
```

<!-- input: station_choice -->
```text
9
```

<!-- output: station_choice -->
```text
Enter station number:
Selected station: 9
Rejected selections: 0
```

<!-- input: station_choice -->
```text
4
7
```

<!-- output: station_choice -->
```text
Enter station number:
Station unavailable
Enter station number:
Selected station: 7
Rejected selections: 1
```

<!-- input: station_choice -->
```text
6
9
```

<!-- output: station_choice -->
```text
Enter station number:
Station unavailable
Enter station number:
Selected station: 9
Rejected selections: 1
```

<!-- input: station_choice -->
```text
0
5
2
```

<!-- output: station_choice -->
```text
Enter station number:
Station unavailable
Enter station number:
Station unavailable
Enter station number:
Selected station: 2
Rejected selections: 2
```

<!-- input: station_choice -->
```text
-1
3
```

<!-- output: station_choice -->
```text
Enter station number:
Station unavailable
Enter station number:
Selected station: 3
Rejected selections: 1
```

<!-- input: station_choice -->
```text
4
abc
```

<!-- output: station_choice -->
```text
Enter station number:
Station unavailable
Enter station number:
Input could not be read
```

<!-- input: station_choice -->
```text
4
6
```

<!-- output: station_choice -->
```text
Enter station number:
Station unavailable
Enter station number:
Station unavailable
Enter station number:
Input could not be read
```

<!-- input: station_choice -->
```text
```

<!-- output: station_choice -->
```text
Enter station number:
Input could not be read
```

</details>

Przykładowe rozwiązanie jest w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 12. Gdy coś pójdzie inaczej

| Co widzisz | Co to znaczy | Co zrobić |
|---|---|---|
| Pytanie powtarza się bez końca | Pętla nie sprawdza, czy odczyt się udał, i po nieudanym odczycie nie ma jak się zakończyć. | Przerwij program, jak w lekcji 4.1. Dodaj sprawdzenie `std::cin.fail()` i flagę, która kończy pętlę. |
| Po `abc` program wypisuje „poza zakresem” | Wartość jest sprawdzana, zanim program sprawdzi odczyt. | W łańcuchu `if`/`else if` sprawdzaj `std::cin.fail()` jako pierwsze. |
| Po nieudanym odczycie pojawia się raport wyboru | Program po pętli nie sprawdza, która flaga ją zakończyła. | Raport wypisuj tylko wtedy, gdy wartość została przyjęta. |
| Licznik odrzuceń jest o jeden za duży | Licznik rośnie także po nieudanym odczycie albo po przyjęciu wartości. | Zwiększaj go tylko w gałęzi dla poprawnie odczytanej, niedostępnej wartości. |
| Pytanie pojawia się dwa razy z rzędu bez odczytu | Pytanie albo odczyt stoi w złym miejscu, na przykład pytanie i przed pętlą, i w niej. | Jedno pytanie i jeden odczyt na przebieg, oba w ciele pętli. |
| Stanowiska 4–6 są przyjmowane albo 1–3 odrzucane | Warunek dostępności łączy porównania niewłaściwymi operatorami. | Każdy zakres to dwa porównania z `&&`. Oba zakresy łączy `\|\|`. Dopisz nawiasy. |
| Program nic nie robi i czeka | Czeka na kolejną liczbę, jak w lekcji 2.6. | Wpisz liczbę i naciśnij **Enter**. |

## 13. Wyjaśnij

Odpowiedz krótko, najlepiej na piśmie. Dopiero potem porównaj z przykładową odpowiedzią.

**1.** Dlaczego pojedynczy `if` nie wystarcza, żeby zapytać ponownie?

<details>
<summary>Przykładowa odpowiedź</summary>

Bo `if` wybiera jedną drogę i program idzie dalej. Do odczytu już nie wraca. Ponowne pytanie wymaga powrotu do tego samego fragmentu kodu, czyli pętli.

</details>

**2.** Co sprawia, że pętla pyta ponownie, i dlaczego odczyt stoi w jej ciele?

<details>
<summary>Przykładowa odpowiedź</summary>

Po odrzuconej wartości żadna flaga się nie zmienia, więc warunek `!accepted && !read_failed` nadal daje `true` i program wraca na początek ciała. Każdy przebieg to nowa próba: nowe pytanie i nowy odczyt. Gdyby odczyt stał przed pętlą, pętla sprawdzałaby w kółko tę samą wartość.

</details>

**3.** Co sprawdza `std::cin.fail()` i co oznacza w nim kropka?

<details>
<summary>Przykładowa odpowiedź</summary>

Sprawdza, czy strumień wejścia jest w stanie błędu odczytu, czyli czy odczyt się nie powiódł. Kropka odwołuje się do funkcji składowej obiektu `std::cin`, a nawiasy ją wywołują. Wynik to `bool`.

</details>

**4.** Dlaczego program nie sprawdza wartości liczby po nieudanym odczycie?

<details>
<summary>Przykładowa odpowiedź</summary>

Bo odczyt nie dostarczył żadnej nowej wartości od użytkownika. Program nie wie, czy liczba w zmiennej ma cokolwiek wspólnego z wpisanymi danymi, więc nie może na niej opierać decyzji.

</details>

**5.** Czym różni się wpisanie `0` od wpisania `abc`?

<details>
<summary>Przykładowa odpowiedź</summary>

`0` to udany odczyt poprawnej liczby `int`, która nie spełnia wymagań, więc program pyta ponownie. `abc` to nieudany odczyt liczby. Strumień jest wtedy w stanie błędu, więc program kończy pracę.

</details>

**6.** Dlaczego po `abc` program w tej lekcji nie pyta ponownie?

<details>
<summary>Przykładowa odpowiedź</summary>

Bo po nieudanym odczycie strumień jest w stanie błędu, a kolejny taki sam odczyt też by się nie udał. Nie umiemy jeszcze przywrócić strumienia do działania. Tego nauczy lekcja 4.6.

</details>

**7.** Co się stanie, gdy dane wejściowe się skończą?

<details>
<summary>Przykładowa odpowiedź</summary>

Kolejny odczyt się nie uda, `std::cin.fail()` da `true`, program ustawi `read_failed`, pętla się zakończy, a program wypisze `Input could not be read` i zakończy pracę normalnie. Nie zapyta ani razu więcej.

</details>

**8.** Dlaczego pętla ma dwie przyczyny zakończenia?

<details>
<summary>Przykładowa odpowiedź</summary>

Bo może się skończyć sukcesem, czyli przyjęciem wartości, albo niepowodzeniem, czyli nieudanym odczytem. Po pętli program musi wiedzieć, co się stało, żeby wypisać właściwy komunikat. Każdą przyczynę zapisuje osobna flaga.

</details>

**9.** Dlaczego w misji nieudany odczyt nie zwiększa licznika odrzuconych stanowisk?

<details>
<summary>Przykładowa odpowiedź</summary>

Bo licznik liczy numery, które program odczytał i odrzucił jako niedostępne. Po nieudanym odczycie nie ma żadnego numeru, więc nie ma czego odrzucać.

</details>

**10.** Czego nauczy lekcja 4.6?

<details>
<summary>Przykładowa odpowiedź</summary>

Jak przywrócić strumień do działania po nieudanym odczycie, żeby zapytać ponownie także po tekście, i jak odróżnić tekst od końca danych.

</details>

## Podsumowanie

- Żeby zapytać ponownie, program musi wrócić do odczytu. Pytanie i odczyt stoją więc w ciele pętli `while`, raz na przebieg.
- `std::cin.fail()` sprawdza, czy odczyt się nie powiódł. To wywołanie **funkcji składowej**: kropka odwołuje się do funkcji obiektu `std::cin`, a nawiasy ją wywołują. Wynik to `bool`.
- `fail()` nie mówi, dlaczego odczyt się nie udał: przyczyną może być tekst albo koniec danych. Dlatego komunikat jest neutralny.
- **Najpierw sprawdź odczyt, dopiero potem wartość.** Po nieudanym odczycie żadna decyzja nie opiera się na wartości zmiennej.
- Pętla wejścia ma dwie przyczyny zakończenia, zapisane w dwóch flagach: wartość przyjęta albo odczyt nieudany.
- Wartość odrzucona pozwala bezpiecznie zapytać ponownie. Nieudany odczyt, także koniec danych, kończy w tej lekcji pracę programu.
- Program z pętlą wejścia nie może pytać bez końca, gdy skończą się dane.

## Co dalej

Program z tej lekcji kończy pracę po każdym nieudanym odczycie, także po zwykłej literówce. W lekcji 4.6 nauczysz się przywracać strumień do działania, odrzucać błędny wpis i pytać ponownie, a przy tym odróżniać błędny wpis od końca danych. **Lekcja 4.6 jest w przygotowaniu.**

---

## Przykładowe rozwiązania

Zajrzyj tutaj **po własnej próbie**. Twoje nazwy mogą się różnić, jeśli standardowe wyjście jest takie, jak wymagane.

<details>
<summary>Punkt 6: tabela dla 0, 6 i 3</summary>

| Próba | Odczytana wartość | Odczyt udany? | Spełnia wymagania? | `accepted` po próbie | `read_failed` po próbie | Następne pytanie? |
|---|---|---|---|---|---|---|
| 1 | 0 | tak | nie: za mała | `false` | `false` | tak |
| 2 | 6 | tak | nie: za duża | `false` | `false` | tak |
| 3 | 3 | tak | tak | `true` | `false` | nie: pętla się kończy |

Były trzy próby odczytu i dwie wartości odrzucone. Liczba prób nie jest równa liczbie odrzuceń: ostatnia próba dała wartość przyjętą.

</details>

<details>
<summary>Punkt 10: pętla bez sprawdzenia odczytu</summary>

1. **Poprawna liczba, na przykład 3:** odczyt się udaje, 3 mieści się w zakresie, `accepted` staje się `true` i pętla się kończy. Program działa poprawnie.
2. **Liczba spoza zakresu, na przykład 6:** odczyt się udaje, program wypisuje komunikat i pyta ponownie. Też poprawnie.
3. **Nieudany odczyt:**

| Próba | Odczyt | Wartość `sessions` | Warunek zakresu | `accepted` | Następne pytanie? |
|---|---|---|---|---|---|
| 1 | **nieudany** (`abc` albo koniec danych) | nie można na niej polegać | zależy od przypadkowej wartości | `false`, jeśli warunek nie przejdzie | tak |
| 2 | **nieudany od razu**: strumień jest już w stanie błędu | dalej ta sama | ten sam wynik | `false` | tak |
| … | **nieudany od razu** | dalej ta sama | ten sam wynik | `false` | tak |

4. **Kolejny odczyt niczego nie zmienia:** strumień w stanie błędu nie przyjmuje nowych danych, więc każda następna próba od razu się nie udaje. Wartość w zmiennej się nie zmienia, warunek daje za każdym razem ten sam wynik, a pętla wypisuje pytanie i komunikat bez końca. Mogłaby też przyjąć wartość, której nikt nie wpisał, jeśli ta przypadkowa wartość mieści się w zakresie.
5. **Brakuje sprawdzenia `std::cin.fail()`** przed sprawdzeniem zakresu i drugiej przyczyny zakończenia pętli, czyli flagi `read_failed`. Tak działa program z punktu 5.

</details>

<details>
<summary>Punkt 11: misja, wybór stanowiska</summary>

<!-- example: station_choice -->
```cpp
#include <iostream>

int main() {
    int station{0};
    int rejected_count{0};
    bool selected{false};
    bool read_failed{false};

    while (!selected && !read_failed) {
        std::cout << "Enter station number:\n";
        std::cin >> station;

        if (std::cin.fail()) {
            read_failed = true;
        } else if ((station >= 1 && station <= 3) || (station >= 7 && station <= 9)) {
            selected = true;
        } else {
            std::cout << "Station unavailable\n";
            ++rejected_count;
        }
    }

    if (selected) {
        std::cout << "Selected station: " << station << "\n";
        std::cout << "Rejected selections: " << rejected_count << "\n";
    } else {
        std::cout << "Input could not be read\n";
    }
}
```

| Próba | Odczytana wartość | Odczyt udany? | Dostępne? | `selected` | `read_failed` | `rejected_count` |
|---|---|---|---|---|---|---|
| 1 | 0 | tak | nie | `false` | `false` | 1 |
| 2 | 5 | tak | nie | `false` | `false` | 2 |
| 3 | 2 | tak | tak | `true` | `false` | 2 |

- **Dwie flagi:** `selected` dla sukcesu i `read_failed` dla niepowodzenia. Pętla działa, dopóki żadna nie jest ustawiona.
- **Kolejność w łańcuchu:** najpierw `std::cin.fail()`, potem dostępność. Po nieudanym odczycie numer nie jest porównywany.
- **Warunek dostępności:** każdy zakres to dwa porównania połączone `&&`, a oba zakresy łączy `||`. Nawiasy pokazują grupowanie, jak w lekcji 3.4.
- **Licznik odrzuceń** rośnie tylko w gałęzi `else`, czyli po udanym odczycie niedostępnego numeru.
- **Po pętli** raport wyboru pojawia się tylko wtedy, gdy `selected` jest `true`. W przeciwnym razie pętlę zakończył nieudany odczyt.

</details>

**Poprzednia lekcja:** [Lekcja 4.4: Powtarzanie aż do osiągnięcia celu](lesson_04_repeat_until_the_goal.md) · **Następna lekcja:** w przygotowaniu · [Opis kursu](../../README.md)

# Lekcja 4.6: Błędny odczyt, odzyskiwanie strumienia i koniec danych

**Polski** · [English](lesson_06_recover_and_end_of_input.en.md) · [Opis kursu](../../README.md)

> **Moduł 4, lekcja 6** · około 90–105 minut, można ją podzielić na dwa podejścia (na przykład punkty 1–8, potem 9–13)
> **Potrzebujesz:** katalogu `cpp-workspace` i oryginalnego projektu `lesson_05_first_program`, jak dotąd. Debugger nie jest w tej lekcji potrzebny.
> **Wersja pilotażowa.** Programy z tej lekcji sprawdzamy automatycznie na Windowsie, Ubuntu i macOS, także z podanymi danymi wejściowymi. Wpisywanie danych w oknie **Run** CLiona opisujemy bez ręcznego sprawdzenia na każdym systemie.

## Zanim zaczniesz

Ta lekcja zakłada, że po lekcji 4.5:

- ponawiasz pytanie w pętli `while`, gdy odczytana liczba nie spełnia wymagań;
- sprawdzasz przez `std::cin.fail()`, czy odczyt się udał, zanim sprawdzisz wartość;
- kończysz pętlę z dwóch powodów, zapisanych w dwóch flagach;
- odczytujesz całą linijkę tekstu przez `std::getline` (lekcja 2.7).

## Sytuacja

Program z lekcji 4.5 pytał o liczbę sesji nauki od 1 do 5. Rozróżniał trzy sytuacje:

- `3`: odczyt udany, wartość dopuszczalna, program ją przyjmuje;
- `0`: odczyt udany, wartość niedopuszczalna, program pyta ponownie;
- `abc`: odczyt nieudany, program kończy pracę.

Ostatnia reakcja jest bezpieczna, ale surowa: jedna literówka kończy cały program. Nowe wymaganie brzmi: **po `abc` program ma poinformować o problemie i pozwolić wpisać liczbę ponownie.** Dla danych `abc`, `0`, `3` program powinien:

1. stwierdzić, że odczytu `abc` nie udało się zamienić na liczbę;
2. usunąć to, co przeszkadza, i zapytać ponownie;
3. odczytać `0`: to liczba, ale spoza zakresu, więc znowu zapytać;
4. odczytać `3` i przyjąć tę wartość.

Jednocześnie program nadal musi się kończyć, gdy **dane się skończą**. Po końcu danych nie ma czego naprawiać ani o co pytać.

Po tej lekcji będziesz:

- wyjaśniać, dlaczego po nieudanym odczycie samo ponowienie `std::cin >> value` nie pomaga;
- przywracać strumień do działania przez `std::cin.clear()` i odrzucać resztę błędnej linijki przez `std::getline`;
- rozpoznawać koniec danych przez `std::cin.eof()` i sprawdzać go we właściwej kolejności;
- odróżniać wartość niedopuszczalną, nieudany odczyt liczby i brak dalszych danych;
- rozumieć, dlaczego `12abc` daje liczbę 12;
- łączyć odzyskiwanie wejścia z pętlą, która gromadzi wynik.

## 1. Przygotuj projekt

W `cpp-workspace` utwórz katalog `lesson_4_6` i skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program`. Programy z punktów 7 i 9 wpisujesz w `main.cpp` tego katalogu.

## 2. Dwie przeszkody po `abc`

Po nieudanym odczycie `abc` dalsze czytanie blokują **dwie różne** rzeczy:

- **Stan błędu.** Strumień `std::cin` zapamiętuje, że odczyt się nie powiódł: `std::cin.fail()` daje `true`. Dopóki ten stan trwa, każdy kolejny odczyt od razu się nie udaje, jak w lekcji 4.5.
- **Pozostały tekst.** Znaki `abc` nie zostały odczytane jako liczba, więc **nadal czekają** w wejściu. Gdyby program spróbował odczytać liczbę jeszcze raz, napotkałby te same znaki.

Rozróżniaj przy tym dwie rzeczy:

- **wartość zmiennej**, na przykład `sessions`, to liczba zapisana w programie;
- **stan strumienia**, czyli to, co pokazują `fail()` i `eof()`, oraz znaki czekające w wejściu, opisują `std::cin`.

Naprawienie jednego nie naprawia drugiego. Potrzebne są więc dwa osobne działania.

## 3. Przywrócenie stanu: `std::cin.clear()`

<!-- fragment -->
```cpp
std::cin.clear();
```

- `clear` to kolejna funkcja składowa obiektu `std::cin`, wywoływana przez kropkę, jak `fail()` w lekcji 4.5.
- Przywraca strumieniowi zwykły stan, czyli zdejmuje znacznik nieudanego odczytu. Po `clear()` `std::cin.fail()` daje `false`, a kolejne odczyty znowu mogą się udać, **o ile są jeszcze jakieś dane**.
- **`clear()` nie usuwa żadnych znaków z wejścia.** Tekst `abc` nadal tam czeka.
- **`clear()` nie tworzy nowych danych.** Jeśli dane się skończyły, po `clear()` dalej ich nie ma.
- `clear()` nie zmienia wartości żadnej zmiennej. Zmienia tylko stan strumienia.

## 4. Odrzucenie reszty linijki: `std::getline`

Pozostały tekst usuwa znane z lekcji 2.7 `std::getline`. Odczytuje ono resztę bieżącej linijki do zmiennej pomocniczej, której potem nie używamy:

<!-- fragment -->
```cpp
std::cin.clear();

std::string discarded_line{""};
std::getline(std::cin, discarded_line);
```

- `discarded_line` dostaje resztę błędnej linijki, łącznie z jej końcem. Nie trzeba jej wypisywać ani używać. Ważne jest to, że **te znaki zostają zabrane z wejścia**.
- Następna próba odczytu zaczyna się więc od nowej linijki, a nie od tych samych błędnych znaków.
- Kolejność jest ważna: **najpierw `clear()`, potem `getline`**. Dopóki strumień jest w stanie błędu, także `getline` od razu by się nie udało.
- Programy, które używają `std::string`, potrzebują `#include <string>`.

Odrzucana jest **cała** reszta linijki. Jeśli użytkownik wpisze w jednej linijce `abc 2`, program odrzuci całe `abc 2`, a nie przyjmie `2` jako kolejnej odpowiedzi. Następna próba dotyczy dopiero następnej linijki.

Istnieją też inne sposoby odrzucania danych z wejścia. Poznasz je w dalszej części kursu. Tutaj wystarczy `std::getline`.

## 5. Koniec danych: `std::cin.eof()`

Po nieudanym odczycie trzeba wiedzieć, **dlaczego** się nie udał. Czy w wejściu był tekst, który można odrzucić, czy dane po prostu się skończyły? Odpowiada na to `std::cin.eof()` (*end of file*, koniec danych):

- daje `true`, gdy podczas dotychczasowych operacji strumień **doszedł do końca danych**;
- opisuje stan po operacjach, które już się wykonały. Nie przewiduje, czy ktoś dopiero zamierza coś wpisać;
- koniec danych to nie niedopuszczalna liczba ani błędny tekst. Nie ma czego odrzucić i nie ma na co czekać. **Po końcu danych program kończy próby**, a `clear()` niczego tu nie zmieni.

Programy z tego kursu są sprawdzane automatycznie: dane przychodzą w całości, a po ostatniej linijce się kończą. Program musi wtedy zakończyć się sam i bezpiecznie.

**Bardzo ważna kolejność: najpierw sukces, potem koniec danych.** Odczyt `std::cin >> value` może **udanie** odczytać ostatnią liczbę i jednocześnie dojść do końca danych, na przykład gdy po liczbie nie ma już nawet końca linijki. Wtedy `std::cin.eof()` daje `true`, ale `std::cin.fail()` daje `false`, a liczba jest poprawnie odczytana. Gdyby program sprawdzał najpierw `eof()`, odrzuciłby dobrą, ostatnią odpowiedź. Dlatego decyzja ma zawsze tę kolejność:

1. Jeśli odczyt się udał (`!std::cin.fail()`), program sprawdza odczytaną liczbę.
2. W przeciwnym razie, jeśli dane się skończyły (`std::cin.eof()`), program kończy próby.
3. W przeciwnym razie odczyt zatrzymał się na błędnym tekście: program przywraca strumień i odrzuca resztę linijki.

Sam wynik `eof() == true` nie oznacza więc, że ostatni odczyt nie dostarczył poprawnej wartości.

## 6. Tabela stanu strumienia

| Krok | Wartość `sessions` | `fail()` | `eof()` | Co zostaje z bieżącej linijki |
|---|---|---|---|---|
| odczyt `3` | 3 | `false` | `false` | tylko koniec linijki |
| odczyt `0` | 0: odczyt udany, ale wartość niedopuszczalna | `false` | `false` | tylko koniec linijki |
| odczyt `abc` | nie wolno na niej polegać | `true` | `false` | `abc` i koniec linijki |
| po `clear()` | bez zmian | `false` | `false` | **nadal** `abc` i koniec linijki |
| po `getline` | bez zmian | `false` | `false` | nic: linijka odrzucona |
| odczyt, gdy danych już nie ma | nie wolno na niej polegać | `true` | `true` | nic |

`clear()` zmienia tylko stan strumienia, a `getline` tylko zabiera znaki z wejścia. Żadne z nich nie zmienia wartości `sessions` ani wymagań, jakie ta wartość musi spełnić.

## 7. Kompletny program

<!-- example: sessions_recover -->
```cpp
#include <iostream>
#include <string>

int main() {
    int sessions{0};
    bool accepted{false};
    bool input_ended{false};

    while (!accepted && !input_ended) {
        std::cout << "Enter session count (1-5):\n";
        std::cin >> sessions;

        if (!std::cin.fail()) {
            if (sessions >= 1 && sessions <= 5) {
                accepted = true;
            } else {
                std::cout << "Session count out of range\n";
            }
        } else if (std::cin.eof()) {
            input_ended = true;
        } else {
            std::cin.clear();
            std::string discarded_line{""};
            std::getline(std::cin, discarded_line);

            if (std::cin.fail() || std::cin.eof()) {
                input_ended = true;
            } else {
                std::cout << "Invalid integer input, try again\n";
            }
        }
    }

    if (accepted) {
        std::cout << "Accepted sessions: " << sessions << "\n";
    } else {
        std::cout << "Input ended\n";
    }
}
```

- **Dwie flagi.** `accepted` oznacza przyjętą wartość, a `input_ended` brak dalszych danych. Pętla działa, dopóki żadna z nich nie jest ustawiona.
- **Gałąź pierwsza: odczyt udany.** Dopiero tu program sprawdza zakres. Za zakres wypisuje `Session count out of range`, a flagi się nie zmieniają, więc program pyta ponownie.
- **Gałąź druga: odczyt nieudany, bo dane się skończyły.** Program ustawia `input_ended`. Nie wywołuje `clear()` i nie pyta ponownie.
- **Gałąź trzecia: odczyt nieudany z innego powodu, czyli przez błędny tekst.** Program przywraca stan, odrzuca resztę linijki i wypisuje `Invalid integer input, try again`, po czym pętla pyta ponownie.
- **Koniec danych podczas odrzucania.** Jeśli błędna linijka była ostatnia i nie miała końca, `getline` dochodzi do końca danych i `eof()` daje `true`. Wtedy program nie obiecuje kolejnej próby: ustawia `input_ended`, a pętla nie odczytuje już nic więcej. Sprawdzenie `fail()` obejmuje rzadką sytuację, w której odrzucanie w ogóle się nie udało.
- **Komunikaty.** `Session count out of range` oznacza liczbę spoza zakresu, `Invalid integer input, try again` nieudany odczyt z możliwością kolejnej próby, `Input ended` brak dalszych danych, a `Accepted sessions: N` przyjętą wartość.

## 8. Przewidź i sprawdź

**Przewidź** dla każdego zestawu danych: ile razy padnie pytanie, jakie komunikaty się pojawią i jak program się zakończy? Zapisz odpowiedzi, a potem uruchom program.

| Zestaw | Dane, linijka po linijce |
|---|---|
| A | `abc`, `0`, `3` |
| B | `3` |
| C | `0`, `3` |
| D | `abc`, `3` |
| E | `abc`, `xyz`, `3` |
| F | `abc 2`, `4` |
| G | `0`, potem koniec danych |
| H | `abc`, potem koniec danych |
| I | brak jakiejkolwiek liczby |

<!-- input: sessions_recover -->
```text
abc
0
3
```

<details>
<summary>Standardowe wyjście dla zestawu A: abc, 0, 3</summary>

<!-- output: sessions_recover -->
```text
Enter session count (1-5):
Invalid integer input, try again
Enter session count (1-5):
Session count out of range
Enter session count (1-5):
Accepted sessions: 3
```

</details>

<!-- input: sessions_recover -->
```text
3
```

<details>
<summary>Standardowe wyjście dla zestawu B: 3</summary>

<!-- output: sessions_recover -->
```text
Enter session count (1-5):
Accepted sessions: 3
```

</details>

<!-- input: sessions_recover -->
```text
0
3
```

<details>
<summary>Standardowe wyjście dla zestawu C: 0, 3</summary>

<!-- output: sessions_recover -->
```text
Enter session count (1-5):
Session count out of range
Enter session count (1-5):
Accepted sessions: 3
```

</details>

<!-- input: sessions_recover -->
```text
abc
3
```

<details>
<summary>Standardowe wyjście dla zestawu D: abc, 3</summary>

<!-- output: sessions_recover -->
```text
Enter session count (1-5):
Invalid integer input, try again
Enter session count (1-5):
Accepted sessions: 3
```

</details>

<!-- input: sessions_recover -->
```text
abc
xyz
3
```

<details>
<summary>Standardowe wyjście dla zestawu E: abc, xyz, 3</summary>

<!-- output: sessions_recover -->
```text
Enter session count (1-5):
Invalid integer input, try again
Enter session count (1-5):
Invalid integer input, try again
Enter session count (1-5):
Accepted sessions: 3
```

</details>

<!-- input: sessions_recover -->
```text
abc 2
4
```

<details>
<summary>Standardowe wyjście dla zestawu F: abc 2, 4</summary>

<!-- output: sessions_recover -->
```text
Enter session count (1-5):
Invalid integer input, try again
Enter session count (1-5):
Accepted sessions: 4
```

Cała linijka `abc 2` została odrzucona, więc `2` nie było osobną odpowiedzią. Program przyjął dopiero `4` z następnej linijki.

</details>

<!-- input: sessions_recover -->
```text
0
```

<details>
<summary>Standardowe wyjście dla zestawu G: 0, potem koniec danych</summary>

<!-- output: sessions_recover -->
```text
Enter session count (1-5):
Session count out of range
Enter session count (1-5):
Input ended
```

</details>

<!-- input: sessions_recover -->
```text
abc
```

<details>
<summary>Standardowe wyjście dla zestawu H: abc, potem koniec danych</summary>

<!-- output: sessions_recover -->
```text
Enter session count (1-5):
Invalid integer input, try again
Enter session count (1-5):
Input ended
```

| Próba | Co się dzieje | `fail()` po odczycie | `eof()` po odczycie | Działanie programu |
|---|---|---|---|---|
| 1 | `abc` nie jest liczbą | `true` | `false` | `clear()`, `getline` odrzuca `abc`, komunikat, kolejna próba |
| 2 | nie ma już danych | `true` | `true` | `input_ended`: koniec prób |

Linijka `abc` kończyła się normalnie, więc po jej odrzuceniu program mógł zapytać jeszcze raz. Dopiero kolejna próba trafiła na koniec danych.

</details>

<!-- input: sessions_recover -->
```text
```

<details>
<summary>Standardowe wyjście dla zestawu I: brak jakiejkolwiek liczby</summary>

<!-- output: sessions_recover -->
```text
Enter session count (1-5):
Input ended
```

</details>

Każdy z tych przebiegów kończy się sam. Pętla nie trwa w nieskończoność ani po błędnym tekście, ani po końcu danych.

## 9. Eksperyment: `12abc`

Program wypisuje odczytaną liczbę, a potem resztę tej samej linijki:

<!-- example: prefix_read -->
```cpp
#include <iostream>
#include <string>

int main() {
    int number{0};
    std::string rest_of_line{""};

    std::cout << "Enter a number:\n";
    std::cin >> number;

    if (!std::cin.fail()) {
        std::cout << "Number: " << number << "\n";
        std::getline(std::cin, rest_of_line);
        std::cout << "Left in the line: [" << rest_of_line << "]\n";
    } else {
        std::cout << "Invalid integer input\n";
    }
}
```

**Przewidź**: czy dla `12abc` odczyt liczby się nie uda? A dla `12`? A dla `abc`?

<!-- input: prefix_read -->
```text
12abc
```

<details>
<summary>Standardowe wyjście dla 12abc</summary>

<!-- output: prefix_read -->
```text
Enter a number:
Number: 12
Left in the line: [abc]
```

</details>

<!-- input: prefix_read -->
```text
12
```

<details>
<summary>Standardowe wyjście dla 12</summary>

<!-- output: prefix_read -->
```text
Enter a number:
Number: 12
Left in the line: []
```

</details>

<!-- input: prefix_read -->
```text
abc
```

<details>
<summary>Standardowe wyjście dla abc</summary>

<!-- output: prefix_read -->
```text
Enter a number:
Invalid integer input
```

</details>

`std::cin >> number` odczytuje tyle cyfr, ile może, i zatrzymuje się na pierwszym znaku, który do liczby nie pasuje. Dla `12abc` odczyt się **udaje**: liczba to 12, a `abc` zostaje w wejściu. Tak samo program z punktu 7 przyjmie `3abc` jako 3:

<!-- input: sessions_recover -->
```text
3abc
```

<details>
<summary>Standardowe wyjście programu z punktu 7 dla 3abc</summary>

<!-- output: sessions_recover -->
```text
Enter session count (1-5):
Accepted sessions: 3
```

</details>

Udany odczyt początkowej liczby nie oznacza więc, że cała linijka była poprawnym zapisem liczby. **Ta lekcja uczy odzyskiwania po nieudanym odczycie, a nie pełnego sprawdzania zawartości całej linijki.** Programy z tej lekcji nie są odporne na dowolne dane.

## 10. Znajdź błąd: samo `clear()` nie wystarcza

Ten fragment **przeanalizuj na papierze, nie uruchamiaj go**. Po nieudanym odczycie program przywraca stan strumienia, ale nie odrzuca reszty linijki:

<!-- fragment -->
```cpp
while (!accepted && !input_ended) {
    std::cout << "Enter session count (1-5):\n";
    std::cin >> sessions;

    if (!std::cin.fail()) {
        if (sessions >= 1 && sessions <= 5) {
            accepted = true;
        } else {
            std::cout << "Session count out of range\n";
        }
    } else if (std::cin.eof()) {
        input_ended = true;
    } else {
        std::cin.clear();
        std::cout << "Invalid integer input, try again\n";
    }
}
```

1. Prześledź pierwszą próbę dla danych `abc`, `3`: co dzieje się ze stanem błędu?
2. Co zostaje w wejściu po `clear()`?
3. Co napotka następny odczyt? Czy kiedykolwiek dojdzie do `3`?
4. Jaki krok jest brakujący?
5. Porównaj poprawiony fragment z programem z punktu 7.

Tabela przebiegu i odpowiedzi są w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 11. Misja: kompletowanie przesyłki

Pracownik kompletuje przesyłkę. Cel to zebranie **co najmniej 10 przedmiotów**. Program pyta o wielkość kolejnej partii przedmiotów. Dopuszczalna partia ma od 1 do 4 przedmiotów.

**Wymagania:**

- Program pyta `Enter batch size (1-4):` i odczytuje liczbę całkowitą.
- Dopuszczalną partię dodaje do zebranej liczby i wypisuje postęp: `Collected: N`.
- Dla liczby spoza zakresu wypisuje `Batch size out of range` i pyta ponownie. Zebrana liczba się nie zmienia.
- Po błędnym zapisie liczby wypisuje `Invalid integer input, try again`, odzyskuje wejście i pyta ponownie. Zebrana liczba się nie zmienia.
- Po zebraniu co najmniej 10 przedmiotów kończy, bez kolejnego pytania, i wypisuje `Target reached: N items`.
- Gdy dane skończą się przed osiągnięciem celu, kończy i wypisuje `Input ended: N items collected`.
- Program nie jest odporny na dowolne dane: `2abc` zostanie przyjęte jako 2, jak w punkcie 9.

W `cpp-workspace` utwórz katalog `shipment`, skopiuj do niego `CMakeLists.txt` z oryginalnego `lesson_05_first_program`, utwórz pusty `main.cpp` i napisz program samodzielnie.

Standardowe wyjście dla czterech przykładów ma być takie. Cel osiągnięty po partiach `3`, `4`, `3`:

<!-- input: shipment -->
```text
3
4
3
```

<!-- output: shipment -->
```text
Enter batch size (1-4):
Collected: 3
Enter batch size (1-4):
Collected: 7
Enter batch size (1-4):
Collected: 10
Target reached: 10 items
```

Błędny tekst w środku, przy danych `2`, `abc`, `4`, `4`:

<!-- input: shipment -->
```text
2
abc
4
4
```

<!-- output: shipment -->
```text
Enter batch size (1-4):
Collected: 2
Enter batch size (1-4):
Invalid integer input, try again
Enter batch size (1-4):
Collected: 6
Enter batch size (1-4):
Collected: 10
Target reached: 10 items
```

Dane kończą się po partiach `2` i `3`:

<!-- input: shipment -->
```text
2
3
```

<!-- output: shipment -->
```text
Enter batch size (1-4):
Collected: 2
Enter batch size (1-4):
Collected: 5
Enter batch size (1-4):
Input ended: 5 items collected
```

Wartości spoza zakresu, przy danych `0`, `3`, `5`, `3`, `4`:

<!-- input: shipment -->
```text
0
3
5
3
4
```

<!-- output: shipment -->
```text
Enter batch size (1-4):
Batch size out of range
Enter batch size (1-4):
Collected: 3
Enter batch size (1-4):
Batch size out of range
Enter batch size (1-4):
Collected: 6
Enter batch size (1-4):
Collected: 10
Target reached: 10 items
```

**To nie jest program z punktu 7 z nowymi komunikatami.** Tam pętla czekała na **jedną** dopuszczalną wartość, która kończyła pracę. Tutaj pojedyncza poprawna partia pracy nie kończy: pętla trwa, dopóki **zebrana suma** nie osiągnie celu, jak w lekcji 4.4, a po drodze musi radzić sobie z błędnymi danymi i z końcem danych. Musisz samodzielnie zdecydować:

1. gdzie przechowywać zebraną liczbę przedmiotów i jak użyć jej w warunku pętli;
2. w których sytuacjach zebrana liczba ma się zmienić, a w których nie;
3. jak odzyskać wejście po błędnym tekście i kiedy zamiast tego zakończyć próby;
4. jak po pętli odróżnić osiągnięcie celu od wcześniejszego końca danych.

**Zanim napiszesz program**, przygotuj dwie rzeczy:

- tabelę przebiegu dla danych `2`, `abc`, `4`, `4`: próba, co odczytano, `fail()` i `eof()`, działanie programu i zebrana liczba po próbie;
- tabelę przypadków testowych: cel osiągnięty dokładnie i przekroczony, partie 0, ujemna i większa niż 4, błędny tekst raz i kilka razy, tekst i liczba spoza zakresu w jednej sekwencji, linijka z błędnym tekstem i dodatkowymi znakami, a także koniec danych przed pierwszą partią, po kilku poprawnych partiach i po kilku błędnych danych. Przy każdym przypadku zapisz oczekiwane standardowe wyjście.

### Kryterium sukcesu

- Program buduje się jako C++20, a jego standardowe wyjście dla czterech powyższych przykładów jest dokładnie takie jak pokazano.
- Pętla `while` kończy się po zebraniu co najmniej 10 przedmiotów albo po końcu danych. Nie ma pytania po osiągnięciu celu.
- Zebrana liczba rośnie tylko o poprawnie odczytane, dopuszczalne partie. Wartości spoza zakresu i błędny tekst jej nie zmieniają.
- Po nieudanym odczycie program najpierw sprawdza koniec danych. Tylko gdy dane się nie skończyły, wywołuje `std::cin.clear()` i odrzuca resztę linijki przez `std::getline`.
- Jeśli koniec danych pojawi się podczas odrzucania, program nie próbuje już czytać.
- `Target reached` pojawia się tylko po osiągnięciu celu, a `Input ended` tylko wtedy, gdy celu nie osiągnięto.
- Tabela przebiegu i tabela przypadków powstały przed uruchomieniem programu.
- Umiesz wyjaśnić, dlaczego program kończy się także po końcu danych.

Gdy wynik się zgadza, możesz zapisać projekt w Gicie, jak w lekcji 1.5.

<details>
<summary>Podpowiedź 1</summary>

Jakie dwa zdarzenia mogą zakończyć pracę: osiągnięcie celu czy brak dalszych danych?

</details>

<details>
<summary>Podpowiedź 2</summary>

W których przypadkach zgromadzona liczba przedmiotów powinna się zmienić?

</details>

<details>
<summary>Podpowiedź 3</summary>

Po nieudanym odczycie najpierw ustal, czy skończyły się dane. Dopiero przy możliwości kontynuacji usuń stan błędu i pozostały tekst.

</details>

<details>
<summary>Pełna lista przypadków kontrolnych: otwórz po przygotowaniu własnej tabeli</summary>

| Dane | Zakończenie | Zebrane | Co sprawdza |
|---|---|---|---|
| `3`, `4`, `3` | cel | 10 | cel osiągnięty dokładnie |
| `2`, `abc`, `4`, `4` | cel | 10 | błędny tekst, potem sukces |
| `2`, `3`, koniec | koniec danych | 5 | koniec danych po poprawnych partiach |
| `0`, `3`, `5`, `3`, `4` | cel | 10 | zero i za duża partia |
| `4`, `4`, `4` | cel | 12 | cel przekroczony ostatnią partią |
| `-1`, `4`, `4`, `2` | cel | 10 | partia ujemna |
| `abc`, `xyz`, `4`, `4`, `2` | cel | 10 | kilka błędnych tekstów |
| `abc`, `9`, `4`, `4`, `2` | cel | 10 | tekst i liczba spoza zakresu |
| `x 3`, `4`, `4`, `2` | cel | 10 | linijka z dodatkowymi znakami odrzucona w całości |
| brak danych | koniec danych | 0 | koniec danych przed pierwszą partią |
| `abc`, `7`, koniec | koniec danych | 0 | koniec danych po błędnych danych |

Pierwsze cztery przypadki są sprawdzone wyżej, przy treści misji.

<!-- input: shipment -->
```text
4
4
4
```

<!-- output: shipment -->
```text
Enter batch size (1-4):
Collected: 4
Enter batch size (1-4):
Collected: 8
Enter batch size (1-4):
Collected: 12
Target reached: 12 items
```

<!-- input: shipment -->
```text
-1
4
4
2
```

<!-- output: shipment -->
```text
Enter batch size (1-4):
Batch size out of range
Enter batch size (1-4):
Collected: 4
Enter batch size (1-4):
Collected: 8
Enter batch size (1-4):
Collected: 10
Target reached: 10 items
```

<!-- input: shipment -->
```text
abc
xyz
4
4
2
```

<!-- output: shipment -->
```text
Enter batch size (1-4):
Invalid integer input, try again
Enter batch size (1-4):
Invalid integer input, try again
Enter batch size (1-4):
Collected: 4
Enter batch size (1-4):
Collected: 8
Enter batch size (1-4):
Collected: 10
Target reached: 10 items
```

<!-- input: shipment -->
```text
abc
9
4
4
2
```

<!-- output: shipment -->
```text
Enter batch size (1-4):
Invalid integer input, try again
Enter batch size (1-4):
Batch size out of range
Enter batch size (1-4):
Collected: 4
Enter batch size (1-4):
Collected: 8
Enter batch size (1-4):
Collected: 10
Target reached: 10 items
```

<!-- input: shipment -->
```text
x 3
4
4
2
```

<!-- output: shipment -->
```text
Enter batch size (1-4):
Invalid integer input, try again
Enter batch size (1-4):
Collected: 4
Enter batch size (1-4):
Collected: 8
Enter batch size (1-4):
Collected: 10
Target reached: 10 items
```

<!-- input: shipment -->
```text
```

<!-- output: shipment -->
```text
Enter batch size (1-4):
Input ended: 0 items collected
```

<!-- input: shipment -->
```text
abc
7
```

<!-- output: shipment -->
```text
Enter batch size (1-4):
Invalid integer input, try again
Enter batch size (1-4):
Batch size out of range
Enter batch size (1-4):
Input ended: 0 items collected
```

</details>

Przykładowe rozwiązanie jest w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 12. Gdy coś pójdzie inaczej

| Co widzisz | Co to znaczy | Co zrobić |
|---|---|---|
| Ten sam komunikat o błędnym tekście powtarza się bez końca | Po `clear()` brakuje odrzucenia reszty linijki, więc następny odczyt trafia na te same znaki (punkt 10). | Przerwij program. Po `clear()` dodaj `std::getline` do zmiennej pomocniczej. |
| Pytanie powtarza się bez końca po końcu danych | Program wywołuje `clear()` także wtedy, gdy dane się skończyły, i próbuje dalej. | Po nieudanym odczycie najpierw sprawdź `std::cin.eof()` i wtedy zakończ próby. |
| Ostatnia poprawna liczba zostaje odrzucona | Program sprawdza `eof()` przed sprawdzeniem, czy odczyt się udał. | Najpierw `!std::cin.fail()`, dopiero w gałęzi niepowodzenia `eof()` (punkt 5). |
| `getline` nic nie odrzuca, a błąd się powtarza | `getline` stoi przed `clear()`, więc też się nie udaje. | Najpierw `clear()`, potem `getline`. |
| Po `abc 2` program przyjmuje `2` | Odrzucany jest tylko błędny wyraz, a nie cała linijka. | Odrzucaj resztę linijki przez `std::getline`. |
| `3abc` zostaje przyjęte jako 3 | Tak działa odczyt liczby przez `>>` (punkt 9). | To znane ograniczenie tej lekcji, a nie błąd w Twoim programie. |
| Suma zmienia się po błędnych danych | Dodawanie stoi poza gałęzią udanego, dopuszczalnego odczytu. | Dodawaj partię tylko po udanym odczycie wartości z zakresu. |
| Program nic nie robi i czeka | Czeka na kolejną linijkę danych, jak w lekcji 2.6. | Wpisz liczbę i naciśnij **Enter**. |

## 13. Wyjaśnij

Odpowiedz krótko, najlepiej na piśmie. Dopiero potem porównaj z przykładową odpowiedzią.

**1.** Dlaczego po `abc` samo ponowienie `std::cin >> sessions` nie pomaga?

<details>
<summary>Przykładowa odpowiedź</summary>

Bo strumień jest w stanie błędu, więc każdy kolejny odczyt od razu się nie udaje. Nawet po przywróceniu stanu w wejściu czekałyby nadal te same znaki `abc`.

</details>

**2.** Co robi `std::cin.clear()`, a czego nie robi?

<details>
<summary>Przykładowa odpowiedź</summary>

Przywraca strumieniowi zwykły stan, więc kolejne odczyty znowu mogą się udać. Nie usuwa znaków z wejścia, nie tworzy nowych danych i nie zmienia wartości zmiennych.

</details>

**3.** Po co po `clear()` wywołujemy `std::getline` i dlaczego właśnie w tej kolejności?

<details>
<summary>Przykładowa odpowiedź</summary>

`getline` zabiera z wejścia resztę błędnej linijki, żeby następny odczyt zaczął się od nowej linijki. Musi stać po `clear()`, bo dopóki strumień jest w stanie błędu, także `getline` od razu by się nie udało.

</details>

**4.** Dlaczego `eof()` sprawdzamy dopiero wtedy, gdy odczyt się nie udał?

<details>
<summary>Przykładowa odpowiedź</summary>

Bo udany odczyt ostatniej liczby też może dojść do końca danych. Wtedy `eof()` daje `true`, a liczba jest poprawna. Sprawdzenie `eof()` jako pierwsze odrzuciłoby dobrą odpowiedź.

</details>

**5.** Dlaczego po końcu danych program nie wywołuje `clear()` i nie pyta ponownie?

<details>
<summary>Przykładowa odpowiedź</summary>

Bo nie ma już czego odczytać. `clear()` nie stworzy nowych danych, więc kolejne pytania byłyby bez odpowiedzi, a pętla mogłaby trwać bez końca.

</details>

**6.** Dlaczego program sprawdza koniec danych także po odrzuceniu linijki?

<details>
<summary>Przykładowa odpowiedź</summary>

Bo błędna linijka mogła być ostatnia. Wtedy `getline` dochodzi do końca danych i nie ma sensu obiecywać kolejnej próby ani czytać dalej.

</details>

**7.** Czym różnią się `0`, `abc` i koniec danych?

<details>
<summary>Przykładowa odpowiedź</summary>

`0` to udany odczyt niedopuszczalnej liczby: program pyta ponownie. `abc` to nieudany odczyt, po którym można odzyskać wejście: `clear()`, odrzucenie linijki i ponowne pytanie. Koniec danych to nieudany odczyt, po którym nie ma czego odzyskiwać: program kończy próby.

</details>

**8.** Dlaczego `12abc` daje liczbę 12, a nie nieudany odczyt?

<details>
<summary>Przykładowa odpowiedź</summary>

Bo `>>` odczytuje tyle cyfr, ile może, i zatrzymuje się na pierwszym niepasującym znaku. Cyfry `12` tworzą poprawną liczbę, a `abc` zostaje w wejściu. Odczyt się udaje, choć cała linijka nie jest poprawnym zapisem liczby.

</details>

**9.** Dlaczego w misji pętla nie kończy się po pierwszej poprawnej partii?

<details>
<summary>Przykładowa odpowiedź</summary>

Bo celem jest zebrana suma, a nie pojedyncza poprawna odpowiedź. Warunek pętli sprawdza, czy zebrano już co najmniej 10 przedmiotów, a jedna partia ma najwyżej 4.

</details>

## Podsumowanie

- Po nieudanym odczycie są dwie przeszkody: **stan błędu** strumienia i **pozostały tekst** w wejściu. Każda wymaga osobnego działania.
- `std::cin.clear()` przywraca strumieniowi zwykły stan. Nie usuwa znaków, nie tworzy danych i nie zmienia zmiennych.
- `std::getline` do zmiennej pomocniczej odrzuca resztę błędnej linijki, w całości. Najpierw `clear()`, potem `getline`.
- `std::cin.eof()` mówi, czy strumień doszedł do końca danych. Koniec danych kończy próby: nie ma czego naprawiać.
- Kolejność decyzji: **najpierw sukces odczytu**, potem koniec danych, a dopiero na końcu odzyskiwanie. Udany odczyt ostatniej liczby może ustawić `eof()` i mimo to dać poprawną wartość.
- Jeśli podczas odrzucania linijki dane się skończą, program nie próbuje już czytać.
- `>>` odczytuje liczbę z początku linijki, więc `12abc` daje 12. Program odzyskuje wejście po nieudanym odczycie, ale nie sprawdza całych linijek.

## Co dalej

To była ostatnia lekcja Modułu 4 z nowymi umiejętnościami. W lekcji 4.7 sprawdzisz je w samodzielnym sprawdzianie. **Lekcja 4.7 jest w przygotowaniu.**

---

## Przykładowe rozwiązania

Zajrzyj tutaj **po własnej próbie**. Twoje nazwy mogą się różnić, jeśli standardowe wyjście jest takie, jak wymagane.

<details>
<summary>Punkt 10: samo clear() nie wystarcza</summary>

Dla danych `abc`, `3`:

| Próba | Co napotyka odczyt | `fail()` po odczycie | Działanie | Co zostaje w wejściu |
|---|---|---|---|---|
| 1 | `abc` | `true` | `clear()`, komunikat | **nadal** `abc` i koniec linijki, potem `3` |
| 2 | **znowu** `abc` | `true` | `clear()`, komunikat | nadal `abc` … |
| 3 | **znowu** `abc` | `true` | `clear()`, komunikat | nadal `abc` … |
| … | … | `true` | bez końca | nic się nie zmienia |

1. **Stan błędu:** po nieudanym odczycie `clear()` go zdejmuje, więc kolejny odczyt może się wykonać.
2. **W wejściu** zostaje `abc` z końcem linijki: `clear()` niczego nie usuwa.
3. **Następny odczyt** trafia na to samo `abc`, znowu się nie udaje i tak w kółko. Do `3` program nigdy nie dochodzi, a `eof()` nie daje `true`, bo dane się nie kończą. Pętla wypisuje pytanie i komunikat bez końca.
4. **Brakuje odrzucenia reszty linijki:** `std::getline(std::cin, discarded_line);` po `clear()`, a po nim sprawdzenia, czy dane się nie skończyły.
5. Tak działa program z punktu 7.

</details>

<details>
<summary>Punkt 11: misja, kompletowanie przesyłki</summary>

<!-- example: shipment -->
```cpp
#include <iostream>
#include <string>

int main() {
    const int target{10};
    int collected{0};
    int batch{0};
    bool input_ended{false};

    while (collected < target && !input_ended) {
        std::cout << "Enter batch size (1-4):\n";
        std::cin >> batch;

        if (!std::cin.fail()) {
            if (batch >= 1 && batch <= 4) {
                collected += batch;
                std::cout << "Collected: " << collected << "\n";
            } else {
                std::cout << "Batch size out of range\n";
            }
        } else if (std::cin.eof()) {
            input_ended = true;
        } else {
            std::cin.clear();
            std::string discarded_line{""};
            std::getline(std::cin, discarded_line);

            if (std::cin.fail() || std::cin.eof()) {
                input_ended = true;
            } else {
                std::cout << "Invalid integer input, try again\n";
            }
        }
    }

    if (collected >= target) {
        std::cout << "Target reached: " << collected << " items\n";
    } else {
        std::cout << "Input ended: " << collected << " items collected\n";
    }
}
```

| Próba | Co odczytano | `fail()` | `eof()` | Działanie | `collected` po próbie |
|---|---|---|---|---|---|
| 1 | 2 | `false` | `false` | partia dopuszczalna, dodana | 2 |
| 2 | `abc` | `true` | `false` | `clear()`, odrzucenie linijki, komunikat | 2 |
| 3 | 4 | `false` | `false` | partia dopuszczalna, dodana | 6 |
| 4 | 4 | `false` | `false` | partia dopuszczalna, dodana | 10 |

Po czwartej próbie `collected < target` daje `false`, więc pętla się kończy i nie zadaje kolejnego pytania.

- **Cel i postęp:** `target` to cel, a `collected` to postęp i akumulator. Warunek pętli łączy pętlę do celu z lekcji 4.4 z flagą końca danych.
- **Suma zmienia się tylko w jednym miejscu:** po udanym odczycie partii z zakresu. Wartości spoza zakresu i błędny tekst jej nie zmieniają.
- **Kolejność po nieudanym odczycie:** najpierw `eof()`, czyli koniec danych i koniec prób. Tylko w przeciwnym razie `clear()`, `getline` i ponowne sprawdzenie końca danych.
- **Po pętli** wynik rozstrzyga suma: `collected >= target` oznacza sukces. W przeciwnym razie pętlę zakończył koniec danych.
- **Zakończenie:** każda przyjęta partia to co najmniej 1 przedmiot, więc dla poprawnych partii cel zostanie osiągnięty najpóźniej po 10 przyjętych partiach. Liczba wszystkich prób nie jest z góry ograniczona, bo użytkownik może podawać kolejne błędne dane. Każde dane są jednak skończone, a koniec danych zawsze kończy pętlę.

</details>

**Poprzednia lekcja:** [Lekcja 4.5: Ponawianie pytania o poprawną wartość](lesson_05_ask_again.md) · **Następna lekcja:** w przygotowaniu · [Opis kursu](../../README.md)

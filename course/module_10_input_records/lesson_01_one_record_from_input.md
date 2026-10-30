# Lekcja 10.1: Jeden rekord z danych wejściowych

**Polski** · [English](lesson_01_one_record_from_input.en.md) · [Opis kursu](../../README.md)

> **Moduł 10, lekcja 1** · około 65–80 minut
> **Potrzebujesz:** katalogu `cpp-workspace` i oryginalnego projektu `lesson_05_first_program`, jak dotąd. Debugger nie jest w tej lekcji potrzebny.
> **Wersja pilotażowa.** Programy z tej lekcji sprawdzamy automatycznie na Windowsie, Ubuntu i macOS, także z podanymi danymi wejściowymi. Wpisywanie danych w oknie **Run** CLiona opisujemy bez ręcznego sprawdzenia na każdym systemie.

## Zanim zaczniesz

Ta lekcja zakłada, że:

- odczytujesz liczbę i jedno słowo przez `std::cin >>` (lekcje 2.6 i 2.7);
- sprawdzasz przez `std::cin.fail()`, czy odczyt się udał, i odróżniasz wartość odrzuconą od nieudanego odczytu (lekcja 4.5);
- wiesz, że po nieudanym odczycie nie wolno polegać na wartości zmiennej (lekcja 4.6);
- wybierasz jedną z kilku możliwości przez `if`, `else if` i `else` (lekcja 3.3) i łączysz warunki przez `||` (lekcja 3.4);
- definiujesz własny typ przez `struct` i tworzysz jego obiekt zapisem z `{}` (lekcja 8.1);
- znasz zasadę „najpierw sprawdź, potem zmień” z lekcji 9.2.

## Sytuacja

Dotąd wartości rekordów były wpisane w kodzie:

<!-- fragment -->
```cpp
const Parcel parcel{"BX-7", 5};
```

W tym kursie **rekord** to obiekt, który przechowuje kilka powiązanych informacji, na przykład identyfikator paczki i jej wagę. Jego typ opisujemy poznanym `struct`. „Rekord” nie jest słowem kluczowym C++. Definicja `struct Parcel` opisuje, z czego składa się każda paczka, a rekordem jest konkretny obiekt tego typu, na przykład `parcel`.

Teraz identyfikator i waga nie są znane w chwili pisania programu. Program dostaje je dopiero po uruchomieniu, ze standardowego wejścia. Dane mogą jednak być błędne: zamiast wagi pojawi się słowo, wagi zabraknie albo będzie równa zero. Z takich danych program nie powinien budować paczki.

Nowa nie jest składnia C++, tylko kolejność znanych działań:

1. odczytaj wartości do zwykłych zmiennych;
2. sprawdź, czy odczyt się udał;
3. sprawdź, czy wartości spełniają zasady;
4. dopiero wtedy utwórz kompletny rekord i korzystaj z jego pól jak w Module 8.

Po tej lekcji będziesz:

- odczytywać pola jednego rekordu przez `>>` do zainicjalizowanych zmiennych lokalnych;
- sprawdzać najpierw powodzenie odczytu, a dopiero potem zasady wartości;
- odróżniać nieudany odczyt od poprawnie odczytanej, ale niedozwolonej wartości;
- tworzyć rekord przez `{}` dopiero wtedy, gdy wszystkie jego pola są odczytane i zaakceptowane;
- przewidywać zachowanie programu przy brakujących i błędnych polach;
- dobierać dane, które ujawniają złą kolejność sprawdzeń.

## 1. Przygotuj projekt

W `cpp-workspace` utwórz katalog `lesson_10_1` i skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program`. Program z punktu 2 wpisujesz w `main.cpp` tego katalogu.

Programy z tej lekcji nie wypisują pytań. Po uruchomieniu od razu wpisz wszystkie wartości, oddzielone spacjami, i naciśnij **Enter**.

## 2. Jedna paczka z wejścia

Paczka ma identyfikator i wagę w umownych jednostkach. Identyfikator to jedno słowo ASCII, bez spacji. Waga musi być większa od zera.

<!-- example: parcel -->
```cpp
#include <iostream>
#include <string>

struct Parcel {
    std::string id;
    int weight;
};

int main() {
    std::string id{};
    int weight{0};

    std::cin >> id;
    std::cin >> weight;

    if (std::cin.fail()) {
        std::cout << "Input error\n";
    } else if (weight <= 0) {
        std::cout << "Invalid parcel\n";
    } else {
        const Parcel parcel{id, weight};

        std::cout << "Parcel: " << parcel.id << "\n";
        std::cout << "Weight: " << parcel.weight << "\n";
    }
}
```

Uruchom program i wpisz:

<!-- input: parcel -->
```text
BX-7 5
```

<!-- output: parcel -->
```text
Parcel: BX-7
Weight: 5
```

| Zapis | Co robi |
|---|---|
| `std::string id{};` i `int weight{0};` | przygotowują zmienne na odczytywane wartości, z wartościami początkowymi |
| dwa odczyty `>>` | zapisują w tych zmiennych słowo `BX-7` i liczbę 5 |
| `if (std::cin.fail())` | sprawdza, czy udały się **oba** odczyty |
| `else if (weight <= 0)` | sprawdza zasadę paczki, ale tylko po udanym odczycie |
| `const Parcel parcel{id, weight};` | tworzy rekord z odczytanych i sprawdzonych wartości |

- **Rekord powstaje dopiero w ostatniej gałęzi.** Przy błędnych danych program go w ogóle nie tworzy, więc nie ma paczki z przypadkowym identyfikatorem albo wagą.
- **Jedno `fail()` po obu odczytach wystarcza.** Gdy pierwszy odczyt się nie uda, strumień zostaje w stanie błędu i drugi też się nie udaje (lekcja 4.6). Po obu odczytach `fail()` daje więc `false` tylko wtedy, gdy udały się oba.
- **`parcel` ma `const`,** bo po utworzeniu się nie zmienia. Zmienne `id` i `weight` nie mogą mieć `const`, bo zapisuje w nich `>>` (lekcja 2.6).
- **Program wypisuje dokładnie jeden z trzech wyników:** paczkę, `Input error` albo `Invalid parcel`. Nie pyta ponownie, więc nie potrzebuje pętli.

## 3. Najpierw odczyt, potem zasady

Dwa przypadki wyglądają podobnie, ale to dwa różne problemy. **Przewidź** wynik każdego z nich i porównaj go ze zwiniętym wynikiem. Uruchomienie jest nieobowiązkowe.

**Przypadek A:** zamiast wagi słowo.

<!-- input: parcel -->
```text
BX-7 five
```

<details>
<summary>Standardowe wyjście dla przypadku A</summary>

<!-- output: parcel -->
```text
Input error
```

</details>

**Przypadek B:** waga równa zero.

<!-- input: parcel -->
```text
BX-7 0
```

<details>
<summary>Standardowe wyjście dla przypadku B</summary>

<!-- output: parcel -->
```text
Invalid parcel
```

</details>

| | A: `BX-7 five` | B: `BX-7 0` |
|---|---|---|
| Czy odczyt wagi się udał? | nie: `five` to nie liczba `int` | tak: 0 to poprawna liczba `int` |
| Co sprawdza program? | `fail()` daje `true`, więc na tym kończy | `fail()` daje `false`, więc sprawdza zasadę: 0 nie jest dodatnie |
| Wynik | `Input error` | `Invalid parcel` |

To ten sam podział co w lekcji 4.5: **nieudany odczyt** i **wartość odrzucona**. `std::cin.fail()` mówi tylko, czy udało się odczytać liczbę. O zasadach paczki nie wie nic: 0 i -3 to dla niego zwykłe, poprawnie odczytane liczby. Zasadę sprawdza dopiero warunek `weight <= 0`.

**Dlaczego ta kolejność?** Po nieudanym odczycie nie wolno polegać na wartości `weight` (lekcja 4.6), bo ta liczba nie pochodzi z danych. Najpierw trzeba więc wiedzieć, czy dane w ogóle są, a dopiero potem pytać, czy są dobre.

## 4. Brakująca wartość i koniec danych

Dane mogą się skończyć, zanim program odczyta wszystkie wartości:

<!-- input: parcel -->
```text
BX-7
```

<details>
<summary>Standardowe wyjście, gdy po BX-7 dane się kończą</summary>

<!-- output: parcel -->
```text
Input error
```

</details>

Identyfikator się odczytał, ale wagi nie ma: odczyt liczby się nie udaje, bo dane się skończyły (lekcja 4.6). To nie jest kompletny rekord, więc program go nie tworzy. Nie rozróżnia przy tym, czy zawiódł tekst zamiast liczby, czy koniec danych: w obu przypadkach wypisuje `Input error`.

**Tego przypadku nie wywołasz, wpisując dane ręcznie.** Gdy wpiszesz `BX-7` i naciśniesz **Enter**, program po prostu czeka na wagę, jak w lekcji 2.6. Koniec danych zdarza się, gdy dane przychodzą w całości, na przykład w testach automatycznych kursu. Ten przypadek przewiduj na papierze, jak w lekcji 4.5.

**`>>` to nie `getline`.** `>>` pomija białe znaki przed wartością, także puste linie. Samo **Enter** niczego więc nie kończy: program czeka dalej. W lekcji 7.4 `std::getline` traktowało pustą linię inaczej, jako udany odczyt pustego tekstu.

## 5. Odstępy i spacje w danych

`>>` pomija białe znaki przed wartością i kończy odczyt na pierwszym białym znaku po niej. Białe znaki to spacja, tabulator i koniec linii, więc wartości nie muszą stać w jednej linii. **Przewidź**, co wypisze program, gdy identyfikator i waga będą w osobnych liniach:

<!-- input: parcel -->
```text
BX-7
5
```

<details>
<summary>Standardowe wyjście dla wartości w dwóch liniach</summary>

<!-- output: parcel -->
```text
Parcel: BX-7
Weight: 5
```

</details>

Ta lekcja ma dwa świadome ograniczenia.

**Identyfikator nie może zawierać spacji.** `>>` odczytuje do `std::string` jedno słowo (lekcja 2.7). **Przewidź** wynik dla nazwy ze spacją:

<!-- input: parcel -->
```text
Big box 5
```

<details>
<summary>Standardowe wyjście dla Big box 5</summary>

<!-- output: parcel -->
```text
Input error
```

</details>

Do `id` trafia samo `Big`, a odczyt wagi trafia na `box` i się nie udaje. Tekst ze spacjami odczytasz w lekcji 10.2.

**Program nie sprawdza, co jest po ostatniej wartości.** Udany odczyt dwóch wartości nie dowodzi, że dalej nie ma już znaków:

<!-- input: parcel -->
```text
BX-7 5 kg
```

<details>
<summary>Standardowe wyjście dla BX-7 5 kg</summary>

<!-- output: parcel -->
```text
Parcel: BX-7
Weight: 5
```

</details>

Program odczytuje dokładnie dwie wartości, a `kg` zostaje w wejściu nieodczytane, jak reszta linii w lekcji 2.7. Podobnie `5kg` dałoby wagę 5, jak `12abc` w lekcji 4.5. Dane zgodne z umową zawierają dokładnie wymagane wartości, a sprawdzanie reszty linii w tej lekcji świadomie pomijamy.

| Sytuacja | Przykład | Wynik programu |
|---|---|---|
| nieudany odczyt wymaganej wartości | `BX-7 five`, `BX-7`, `Big box 5` | `Input error` |
| wartość odczytana, ale niezgodna z zasadami | `BX-7 0` | `Invalid parcel` |
| dodatkowy tekst po ostatniej wartości | `BX-7 5 kg` | poza sprawdzaniem tej lekcji: program wypisuje paczkę |

## 6. Misja: zajętość sali

Program wczytuje dane jednej sali i wypisuje, ile ma wolnych miejsc.

**Dane wejściowe:** trzy wartości oddzielone białymi znakami: kod sali, liczba wszystkich miejsc (pojemność) i liczba zajętych miejsc.

**Reguły:**

- Kod to niepusty tekst ASCII bez spacji. Program nie sprawdza jego znaków. Odczytujemy jedną salę, więc unikalność kodu nie ma znaczenia.
- Pojemność musi być większa od zera.
- Liczba zajętych miejsc musi być nieujemna i nie może przekraczać pojemności.
- Wszystkie liczby są niewielkie i mieszczą się w `int`.
- Wolne miejsca to pojemność minus liczba zajętych miejsc.

**Wymagania:**

- Program definiuje własny typ z trzema polami: kodem (`std::string`), pojemnością (`int`) i liczbą zajętych miejsc (`int`). Nazwy typu i pól wybierasz samodzielnie. Typ nie ma pola na wolne miejsca: to wartość obliczana z dwóch pozostałych pól.
- Program odczytuje trzy wartości przez `>>` do zmiennych lokalnych w `main`. Nie wypisuje pytań, nie pyta ponownie i nie używa `std::getline` ani wektora.
- Gdy odczyt się nie udał, program wypisuje dokładnie `Input error` i nie sprawdza zasad.
- Gdy odczyt się udał, ale wartości łamią zasady, program wypisuje dokładnie `Invalid room`.
- Dopiero gdy wszystko się zgadza, program tworzy rekord sali przez `{}` i wypisuje cztery linie jak w przykładzie niżej. Liczba wolnych miejsc pochodzi z pól tego rekordu.

W `cpp-workspace` utwórz katalog `room_check`, skopiuj do niego `CMakeLists.txt` z oryginalnego `lesson_05_first_program`, utwórz pusty `main.cpp` i napisz program samodzielnie.

Dla danych:

<!-- input: room -->
```text
R-12 12 8
```

standardowe wyjście ma być takie:

<!-- output: room -->
```text
Room: R-12
Capacity: 12
Occupied: 8
Available: 4
```

Odczyt trzeciej wartości się nie udaje:

<!-- input: room -->
```text
R-12 12 eight
```

<!-- output: room -->
```text
Input error
```

Odczyt się udaje, ale zajętych miejsc jest więcej niż wszystkich:

<!-- input: room -->
```text
R-12 8 9
```

<!-- output: room -->
```text
Invalid room
```

Dla jednego uruchomienia program wypisuje tylko jeden z tych trzech wyników.

**To nie jest paczka z inną nazwą.** Sala ma trzecie pole, a jedna z zasad łączy dwie liczby. Musisz samodzielnie zdecydować:

1. jak nazwać typ i pola oraz jakich typów użyć;
2. jakich zmiennych lokalnych potrzebujesz do odczytu i dlaczego muszą mieć wartości początkowe;
3. jak sprawdzić, że udały się wszystkie trzy odczyty;
4. jak oddzielić błąd odczytu od niedozwolonych wartości i w jakiej kolejności je sprawdzić;
5. jak zapisać trzy zasady wartości;
6. w którym miejscu utworzyć rekord i jak zainicjalizować jego pola;
7. jak obliczyć wolne miejsca z pól rekordu;
8. dlaczego nie wystarczy sprawdzić samych liczb, bez stanu strumienia.

**Zanim napiszesz program**, przygotuj tabelę przypadków: poprawna sala, sala pusta i pełna, pojemność 1, zerowa i ujemna pojemność, ujemna liczba zajętych miejsc, więcej zajętych miejsc niż wszystkich, słowo zamiast pierwszej albo drugiej liczby, brak ostatniej wartości. Przy każdym zapisz oczekiwany wynik: cztery linie sali, `Input error` albo `Invalid room`.

**Potem** uruchom program dla trzech danych pokazanych wyżej. Wszystkie przypadki z pełnej listy kontrolnej są sprawdzone automatycznie, więc pozostałych nie musisz uruchamiać. Przypadki, w których brakuje wartości, przeanalizuj na papierze: wpisując dane ręcznie, nie wywołasz końca danych (punkt 4).

### Kryterium sukcesu

- Program buduje się jako C++20 i dla trzech danych pokazanych wyżej wypisuje dokładnie pokazane wyniki.
- Jest jeden typ z trzema polami, bez pola na wolne miejsca.
- Zmienne do odczytu mają wartości początkowe, a rekord powstaje dopiero po sprawdzeniu odczytu i wszystkich zasad.
- `std::cin.fail()` jest sprawdzane przed zasadami wartości.
- Liczba wolnych miejsc pochodzi z pól utworzonego rekordu.
- Tabela przypadków powstała przed uruchomieniem programu.
- Umiesz wyjaśnić różnicę między `Input error` i `Invalid room`.

Gdy wynik się zgadza, możesz zapisać projekt w Gicie, jak w lekcji 1.5.

<details>
<summary>Podpowiedź 1</summary>

Zanim utworzysz rekord, zastanów się, czy udało się odczytać wszystkie jego pola.

</details>

<details>
<summary>Podpowiedź 2</summary>

Błąd odczytu i wartość, która nie spełnia zasad sali, to dwie różne sytuacje. W jakiej kolejności program powinien je sprawdzić?

</details>

<details>
<summary>Podpowiedź 3</summary>

Przygotuj zwykłe zmienne, odczytaj do nich dane, sprawdź powodzenie i ograniczenia, a dopiero potem zainicjalizuj rekord sali przez `{}`.

</details>

<details>
<summary>Pełna lista przypadków kontrolnych: otwórz po przygotowaniu własnej tabeli</summary>

Przy poprawnej sali kolumna „Wynik” podaje liczbę wolnych miejsc. Program wypisuje wtedy wszystkie cztery linie.

| | Dane | Wynik | Co sprawdza |
|---|---|---|---|
| A | `R-12 12 8` | 4 | dane z wymagań |
| B | `R-01 10 0` | 10 | sala pusta: 0 zajętych miejsc to poprawna wartość |
| C | `R-02 10 10` | 0 | sala pełna: zajęte miejsca równe pojemności |
| D | `R-03 1 0` | 1 | najmniejsza pojemność |
| E | `R-04 1 1` | 0 | jedno miejsce, zajęte |
| F | `R-05 0 0` | `Invalid room` | zerowa pojemność |
| G | `R-06 -2 0` | `Invalid room` | ujemna pojemność |
| H | `R-07 10 -1` | `Invalid room` | ujemna liczba zajętych miejsc |
| I | `R-08 8 9` | `Invalid room` | więcej zajętych miejsc niż wszystkich |
| J | `R-09 twelve 3` | `Input error` | słowo zamiast pierwszej liczby |
| K | `R-10 12 eight` | `Input error` | słowo zamiast drugiej liczby |
| L | `R-11 12` | `Input error` | brak ostatniej wartości: dane się kończą |
| M | `R-13` | `Input error` | sam kod, bez liczb |
| N | pusta linia | `Input error` | żadnej wartości: pusta linia, a po niej koniec danych |
| O | `LAB-2`, `30` i `25`, każde w osobnej linii | 5 | wartości w osobnych liniach |
| P | `Aula-3   20   5` | 15 | kilka spacji między wartościami, inny kod |
| Q | `R-14 6 2 extra` | 4 | dodatkowy tekst po trzeciej wartości: poza sprawdzaniem tej lekcji |

**Testy automatyczne i Twoje próby.** Wszystkie przypadki są sprawdzone automatycznie: rozwiązanie referencyjne jest uruchamiane dla każdego z nich, a jego pełne standardowe wyjście porównywane z oczekiwanym. Rozwiązanie i jego wyniki są w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

</details>

Przykładowe rozwiązanie jest w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 7. Znajdź błąd: waga sprawdzona przed odczytem

To zadanie wykonaj **po misji**: program poniżej ma działać tak samo jak program z punktu 2. Program możesz przepisać albo skopiować do `main.cpp`.

<details>
<summary>Program do sprawdzenia: otwórz po napisaniu własnego programu</summary>

<!-- example: parcel_order_bug -->
```cpp
#include <iostream>
#include <string>

struct Parcel {
    std::string id;
    int weight;
};

int main() {
    std::string id{};
    int weight{0};

    std::cin >> id;
    std::cin >> weight;

    if (weight <= 0) {
        std::cout << "Invalid parcel\n";
    } else if (std::cin.fail()) {
        std::cout << "Input error\n";
    } else {
        const Parcel parcel{id, weight};

        std::cout << "Parcel: " << parcel.id << "\n";
        std::cout << "Weight: " << parcel.weight << "\n";
    }
}
```

Poprawne dane:

<!-- input: parcel_order_bug -->
```text
BX-7 5
```

1. **Przewidź** wynik dla tych danych. To te same dane co w punkcie 2, więc porównaj swoją odpowiedź z wynikiem z punktu 2. Uruchomienie jest nieobowiązkowe.
2. Dobierz własne dane, dla których ten program wypisze zły wynik.
3. Dla swoich danych **przewidź**: czy odczyt wagi się uda? Którą gałąź wybierze ten program, a którą program z punktu 2?
4. Uruchom program dla swoich danych.
5. Wyjaśnij, czym różnią się tu błąd odczytu i niedozwolona waga i dlaczego program je pomylił.
6. Popraw kolejność sprawdzeń.
7. Uruchom poprawiony program dla swoich danych.
8. Czy poprawka wymagała nowej konstrukcji C++? Co właściwie się zmieniło?

</details>

Wyniki, przykładowe dane i poprawiony program są w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 8. Gdy coś pójdzie inaczej

| Co widzisz | Co to znaczy | Co zrobić |
|---|---|---|
| Program nic nie wypisuje i czeka | Nie wpisano jeszcze wszystkich wartości. `>>` czeka na kolejną, a pusta linia jej nie dostarcza (punkt 4). | Wpisz brakujące wartości i naciśnij **Enter**. |
| `Invalid room` albo `Invalid parcel` dla słowa zamiast liczby | Program sprawdza zasady przed `std::cin.fail()` (punkt 7). | Najpierw sprawdź odczyt, potem zasady. |
| Program wypisuje salę, choć jedna z liczb była słowem | Program nie sprawdza `std::cin.fail()` i korzysta z wartości, która nie pochodzi z danych. | Sprawdź `std::cin.fail()` po wszystkich odczytach, zanim użyjesz wartości. |
| Dla pojemności 0 program wypisuje salę | Warunek przepuszcza 0, na przykład `capacity < 0` zamiast `capacity <= 0`. | Pojemność musi być większa od zera, więc 0 też trzeba odrzucić. |
| `Available` jest ujemne | Brakuje zasady, że zajętych miejsc nie może być więcej niż wszystkich. | Odrzucaj dane, w których liczba zajętych miejsc przekracza pojemność. |
| Kod ze spacją, na przykład `R 12 12 8`, daje salę `R` z błędnymi liczbami | `>>` odczytuje jedno słowo: kodem staje się `R`, a liczby przesuwają się o jedną wartość. | Kod w tej lekcji nie ma spacji. Tekst ze spacjami odczytasz w lekcji 10.2. |
| Błąd kompilacji przy `>>`, którego pierwsza linia kończy się na `'const int'` | Zmienna, do której odczytujesz, ma `const` (lekcja 2.6). | Usuń `const` z tej zmiennej. `const` może mieć rekord utworzony po sprawdzeniach. |

## 9. Wyjaśnij

Odpowiedz własnymi słowami, najlepiej na piśmie. Dopiero potem porównaj z przykładowymi odpowiedziami.

1. Dlaczego program odczytuje dane do zmiennych lokalnych z wartościami początkowymi, a rekord tworzy dopiero po sprawdzeniach?
2. Czy `std::cin.fail()` sprawdza, czy pojemność jest dodatnia? Czym różni się od warunku `capacity <= 0`?
3. Czy liczbę `-1` można poprawnie odczytać do `int`? Co program sali wypisze dla `R-07 10 -1`?
4. Co się stanie, gdy zamiast liczby pojawi się słowo? A gdy zabraknie ostatniej wartości? Dlaczego w obu przypadkach nie powstaje rekord?
5. Dlaczego kod sali ze spacją wymaga innego sposobu odczytu? Czy `>>` wymaga wartości w osobnych liniach?
6. Czy trzy udane odczyty gwarantują, że po ostatniej wartości nie ma już danych?
7. Dlaczego program nie oblicza wolnych miejsc po nieudanym odczycie?
8. Czym różnią się `Input error` i `Invalid room`? Dlaczego program sprawdza je w tej kolejności?
9. Dlaczego typ sali nie ma pola na wolne miejsca?

<details>
<summary>Przykładowe odpowiedzi</summary>

1. Bo przed sprawdzeniami nie wiadomo, czy wartości są kompletne i poprawne. Zmienne lokalne mogą przechować wartości z nieudanego odczytu, ale program nic z nich nie buduje. Rekord tworzony na końcu ma zawsze wszystkie pola odczytane i zaakceptowane. Wartości początkowe są potrzebne, bo przy nieudanym odczycie zmienna może zachować swoją dotychczasową wartość. Bez wartości początkowej byłaby to wartość nieokreślona, a jej odczytanie byłoby błędem programu.
2. Nie. `fail()` mówi tylko, czy odczyt się udał, czyli czy w danych była liczba `int`. `capacity <= 0` sprawdza zasadę sali dla liczby, która już została poprawnie odczytana. Pojemność 0 to udany odczyt i jednocześnie niedozwolona wartość.
3. Tak. -1 to poprawna liczba `int`, więc `fail()` daje `false`. Łamie jednak zasadę nieujemnej liczby zajętych miejsc, więc program wypisuje `Invalid room`.
4. W obu przypadkach odczyt liczby się nie udaje: słowo nie jest liczbą, a po końcu danych nie ma czego odczytać. `fail()` daje `true` i program wypisuje `Input error`. Rekord nie powstaje, bo program nie ma kompletu wartości z danych.
5. Bo `>>` kończy odczyt tekstu na pierwszym białym znaku, więc spacja podzieliłaby kod na dwie wartości. Całą linię ze spacjami odczytuje `std::getline`, a jego połączenie z `>>` poznasz w lekcji 10.2. Osobne linie nie są potrzebne: spacja, tabulator i koniec linii tak samo oddzielają wartości.
6. Nie. Program odczytuje dokładnie trzy wartości, a to, co jest dalej, zostaje w wejściu nieodczytane. Dla `R-14 6 2 extra` program wypisze salę (przypadek Q). W tej lekcji świadomie tego nie sprawdzamy: dane zgodne z umową mają dokładnie trzy wartości.
7. Bo po nieudanym odczycie nie wolno polegać na wartościach zmiennych (lekcja 4.6). Wynik obliczony z nich wyglądałby jak prawdziwa liczba wolnych miejsc, choć nie pochodziłby z danych.
8. `Input error` znaczy, że nie udało się odczytać wszystkich wartości. `Invalid room` znaczy, że wszystkie wartości odczytały się poprawnie, ale łamią zasady sali. Najpierw sprawdzamy odczyt, bo zasady mają sens tylko dla wartości, które pochodzą z danych. W odwrotnej kolejności brak poprawnej liczby mógłby zostać uznany za niedozwoloną wartość, jak w punkcie 7.
9. Bo wolne miejsca wynikają z dwóch innych pól. Osobne pole mogłoby się z nimi nie zgadzać, a program musiałby pilnować, żeby zawsze było aktualne. Obliczenie z pól rekordu zawsze daje wynik zgodny z pojemnością i liczbą zajętych miejsc.

</details>

## Podsumowanie

- Rekord to obiekt struktury, który przechowuje kilka powiązanych informacji. Gdy jego wartości pochodzą z wejścia, program najpierw odczytuje je do zmiennych lokalnych z wartościami początkowymi.
- Kolejność jest stała: odczyt, sprawdzenie odczytu przez `std::cin.fail()`, sprawdzenie zasad, a dopiero potem utworzenie rekordu przez `{}`.
- `fail()` mówi, czy odczyt się udał, a nie, czy wartość jest dozwolona. Nieudany odczyt i niedozwolona wartość to dwa różne wyniki.
- Po nieudanym odczycie nie wolno polegać na wartościach zmiennych, dlatego zasady sprawdza się dopiero po udanym odczycie.
- `>>` oddziela wartości dowolnymi białymi znakami, także końcem linii, i odczytuje tekst tylko do pierwszej spacji. Nie sprawdza, co jest po ostatniej wartości.
- Przy błędnych danych program nie tworzy rekordu i niczego z niego nie wypisuje.

## Co dalej

W tej lekcji tekst w rekordzie był jednym słowem. W kolejnej lekcji rekord będzie zawierał tekst ze spacjami obok liczb, więc program połączy `>>` z `std::getline`. Lekcja 10.2 jest w przygotowaniu.

---

## Przykładowe rozwiązania

Zajrzyj tutaj **po własnej próbie**. Twoje nazwy mogą się różnić, jeśli standardowe wyjście jest takie, jak wymagane.

<details>
<summary>Punkt 6: misja, zajętość sali</summary>

<!-- example: room -->
```cpp
#include <iostream>
#include <string>

struct Room {
    std::string code;
    int capacity;
    int occupied;
};

int main() {
    std::string code{};
    int capacity{0};
    int occupied{0};

    std::cin >> code;
    std::cin >> capacity;
    std::cin >> occupied;

    if (std::cin.fail()) {
        std::cout << "Input error\n";
    } else if (capacity <= 0 || occupied < 0 || occupied > capacity) {
        std::cout << "Invalid room\n";
    } else {
        const Room room{code, capacity, occupied};

        std::cout << "Room: " << room.code << "\n";
        std::cout << "Capacity: " << room.capacity << "\n";
        std::cout << "Occupied: " << room.occupied << "\n";
        std::cout << "Available: " << room.capacity - room.occupied << "\n";
    }
}
```

1. **Własny typ,** bo kod, pojemność i liczba zajętych miejsc opisują jedną salę. Pola mają nazwy, a rekord można później przekazać jako całość, jak w Module 8.
2. **Najpierw zmienne lokalne,** bo `>>` potrzebuje miejsca, w którym zapisze odczytaną wartość, a rekord tworzymy raz, z kompletem wartości. Wartości początkowe sprawiają, że żadna zmienna nie ma wartości nieokreślonej, także po nieudanym odczycie.
3. **Rekord nie powstaje od razu.** Można by odczytywać prosto do pól istniejącego rekordu, ale wtedy przy błędzie istniałaby sala, której część pól pochodzi z danych, a część z wartości początkowych. Rekord tworzony na końcu jest zawsze kompletny.
4. **`>>`, a nie `getline`,** bo każda wartość to jedno słowo albo jedna liczba. `>>` pomija białe znaki przed wartością i kończy odczyt na pierwszym po niej. `std::getline` odczytuje całą linię, ze spacjami.
5. **Kod bez spacji,** bo `>>` odczytuje do `std::string` jedno słowo. Kod ze spacją podzieliłby się na dwie wartości.
6. **Co wykrywa `std::cin.fail()`:** że któraś wartość nie dała się odczytać, bo w danych było słowo zamiast liczby albo dane się skończyły.
7. **Czego `std::cin.fail()` nie wykrywa:** wartości, które odczytały się poprawnie, ale łamią zasady (0, liczby ujemne, więcej zajętych miejsc niż wszystkich), ani dodatkowego tekstu po trzeciej wartości.
8. **Zasady po sprawdzeniu odczytu,** bo po nieudanym odczycie wartości zmiennych nie pochodzą z danych. Dla `R-11 12` liczba zajętych miejsc zostaje 0, czyli wygląda na poprawną. Dlatego nie wystarczy sprawdzić samych liczb: o tym, czy odczyt się udał, mówi tylko stan strumienia.
9. **Pojemność dodatnia,** bo sala bez miejsc nie ma sensu w tej umowie, a wolne miejsca liczone z pojemności 0 nic by nie znaczyły.
10. **Zajęte miejsca nieujemne,** bo liczba zajętych miejsc nie może być mniejsza od zera.
11. **Zajęte miejsca nie większe od pojemności,** bo w sali nie może być zajętych więcej miejsc, niż ma. Bez tej zasady liczba wolnych miejsc wyszłaby ujemna.
12. **Bez pola na wolne miejsca,** bo to wartość obliczana z dwóch pól. Osobne pole mogłoby się z nimi nie zgadzać.
13. **Przy odrzuceniu nie ma obiektu sali.** Program wypisuje tylko komunikat, więc nie ma czego wypisać częściowo albo z błędnymi wartościami.
14. **Bez pętli,** bo umowa przewiduje jedną próbę odczytu. Ponawianie pytania z lekcji 4.5 i 4.6 nie jest tu potrzebne.
15. **Gdy brakuje liczby,** jak w `R-11 12`, odczyt ostatniej wartości trafia na koniec danych i się nie udaje. Program wypisuje `Input error`.
16. **Świadomie poza sprawdzaniem:** dodatkowy tekst po trzeciej wartości (przypadek Q), znaki kodu i liczby spoza zakresu `int`.

**Inne poprawne rozwiązania:** każdą zasadę można sprawdzać w osobnym `else if`, z tym samym komunikatem. Pola mogą mieć inne nazwy i inną kolejność, jeśli wartości w `{}` stoją w tej samej kolejności co pola. Liczbę wolnych miejsc można zapisać w zmiennej `const int`, obliczonej z pól rekordu.

Każdy przypadek z listy kontrolnej to osobne uruchomienie tego programu. Pierwsze trzy uruchomienia to dane z treści misji, w tym przypadek A. Dalej są przypadki od B do Q, w kolejności z listy kontrolnej.

<!-- input: room -->
```text
R-01 10 0
```

<!-- output: room -->
```text
Room: R-01
Capacity: 10
Occupied: 0
Available: 10
```

<!-- input: room -->
```text
R-02 10 10
```

<!-- output: room -->
```text
Room: R-02
Capacity: 10
Occupied: 10
Available: 0
```

<!-- input: room -->
```text
R-03 1 0
```

<!-- output: room -->
```text
Room: R-03
Capacity: 1
Occupied: 0
Available: 1
```

<!-- input: room -->
```text
R-04 1 1
```

<!-- output: room -->
```text
Room: R-04
Capacity: 1
Occupied: 1
Available: 0
```

<!-- input: room -->
```text
R-05 0 0
```

<!-- output: room -->
```text
Invalid room
```

<!-- input: room -->
```text
R-06 -2 0
```

<!-- output: room -->
```text
Invalid room
```

<!-- input: room -->
```text
R-07 10 -1
```

<!-- output: room -->
```text
Invalid room
```

<!-- input: room -->
```text
R-08 8 9
```

<!-- output: room -->
```text
Invalid room
```

<!-- input: room -->
```text
R-09 twelve 3
```

<!-- output: room -->
```text
Input error
```

<!-- input: room -->
```text
R-10 12 eight
```

<!-- output: room -->
```text
Input error
```

<!-- input: room -->
```text
R-11 12
```

<!-- output: room -->
```text
Input error
```

<!-- input: room -->
```text
R-13
```

<!-- output: room -->
```text
Input error
```

Przypadek N to pusta linia, a po niej koniec danych:

<!-- input: room -->
```text
```

<!-- output: room -->
```text
Input error
```

<!-- input: room -->
```text
LAB-2
30
25
```

<!-- output: room -->
```text
Room: LAB-2
Capacity: 30
Occupied: 25
Available: 5
```

<!-- input: room -->
```text
Aula-3   20   5
```

<!-- output: room -->
```text
Room: Aula-3
Capacity: 20
Occupied: 5
Available: 15
```

<!-- input: room -->
```text
R-14 6 2 extra
```

<!-- output: room -->
```text
Room: R-14
Capacity: 6
Occupied: 2
Available: 4
```

</details>

<details>
<summary>Punkt 7: wyniki przed poprawką i poprawiony program</summary>

Przed poprawką, dla poprawnych danych `BX-7 5`:

<!-- output: parcel_order_bug -->
```text
Parcel: BX-7
Weight: 5
```

- **Dla poprawnych danych kolejność sprawdzeń nie ma znaczenia.** Odczyt się udaje, a waga jest dodatnia, więc oba programy dochodzą do ostatniej gałęzi.
- **Dane, które ujawniają błąd:** takie, przy których odczyt wagi się nie udaje, na przykład słowo zamiast liczby. Poprawny wynik to `Input error`, a program z błędem wypisuje:

<!-- input: parcel_order_bug -->
```text
BX-7 five
```

<!-- output: parcel_order_bug -->
```text
Invalid parcel
```

Brak wagi daje ten sam zły wynik:

<!-- input: parcel_order_bug -->
```text
BX-7
```

<!-- output: parcel_order_bug -->
```text
Invalid parcel
```

- **Przyczyna:** program sprawdza `weight <= 0`, zanim sprawdzi odczyt. Po nieudanym odczycie w `weight` jest 0: przy słowie zamiast liczby zapisuje je nieudany odczyt, a przy końcu danych zostaje wartość początkowa. Ta liczba nie pochodzi z danych, ale program ocenia ją jak wagę, więc nazywa brak poprawnej liczby niedozwoloną wagą.
- **`>>` zadziałało poprawnie:** nieudany odczyt zgłosiło przez `fail()`. Błąd jest w kolejności sprawdzeń w naszym programie.
- **Dane, które błędu nie ujawniają:** poprawna waga, 0 i liczby ujemne, bo oba programy wypisują dla nich to samo. Także `BX-7 5kg`, bo `>>` odczytuje z niego liczbę 5.
- **Poprawka:** zamień kolejność sprawdzeń, najpierw `std::cin.fail()`, potem `weight <= 0`. Nie potrzeba nowej konstrukcji C++: zostają te same `if`, `else if`, `else` i te same dwa warunki, tylko w innej kolejności. Poprawiony program to program z punktu 2:

<!-- example: parcel_order_fixed -->
```cpp
#include <iostream>
#include <string>

struct Parcel {
    std::string id;
    int weight;
};

int main() {
    std::string id{};
    int weight{0};

    std::cin >> id;
    std::cin >> weight;

    if (std::cin.fail()) {
        std::cout << "Input error\n";
    } else if (weight <= 0) {
        std::cout << "Invalid parcel\n";
    } else {
        const Parcel parcel{id, weight};

        std::cout << "Parcel: " << parcel.id << "\n";
        std::cout << "Weight: " << parcel.weight << "\n";
    }
}
```

<!-- input: parcel_order_fixed -->
```text
BX-7 five
```

<!-- output: parcel_order_fixed -->
```text
Input error
```

</details>

**Poprzednia lekcja:** [Lekcja 9.5: Flota dronów dostawczych (sprawdzian Modułu 9)](../module_09_mutable_references/lesson_05_drone_fleet.md) · **Następna lekcja:** w przygotowaniu · [Opis kursu](../../README.md)

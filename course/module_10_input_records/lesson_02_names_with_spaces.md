# Lekcja 10.2: Nazwy ze spacjami: `>>` i `std::getline`

**Polski** · [English](lesson_02_names_with_spaces.en.md) · [Opis kursu](../../README.md)

> **Moduł 10, lekcja 2** · około 75–90 minut
> **Potrzebujesz:** katalogu `cpp-workspace` i oryginalnego projektu `lesson_05_first_program`, jak dotąd. Debugger nie jest w tej lekcji potrzebny.
> **Wersja pilotażowa.** Programy z tej lekcji sprawdzamy automatycznie na Windowsie, Ubuntu i macOS, także z podanymi danymi wejściowymi. Wpisywanie danych w oknie **Run** CLiona opisujemy bez ręcznego sprawdzenia na każdym systemie.

## Zanim zaczniesz

Ta lekcja zakłada, że:

- odczytujesz jedno słowo albo liczbę przez `std::cin >>`, a całą linię ze spacjami przez `std::getline`, i pamiętasz, że po `>>` w wejściu zostaje koniec linii (lekcja 2.7);
- wiesz, że po nieudanym odczycie kolejne odczyty też się nie udają, a resztę linii można odczytać przez `std::getline` do zmiennej pomocniczej (lekcja 4.6);
- odróżniasz pustą linię, czyli udany odczyt pustego tekstu, od nieudanego odczytu (lekcja 7.4);
- definiujesz własny typ przez `struct` (lekcja 8.1);
- odczytujesz dane do zmiennych lokalnych, sprawdzasz odczyt i zasady, a dopiero potem tworzysz rekord (lekcja 10.1).

## Sytuacja

W lekcji 10.1 identyfikator paczki był jednym słowem, bo `>>` odczytuje tekst tylko do pierwszej spacji. Nazwy miejsc mają jednak często kilka słów, na przykład `North Hub`. Całą linię ze spacjami odczytuje `std::getline`, a liczby nadal odczytuje `>>`.

Lekcja 2.7 radziła: najpierw `getline`, potem `>>`. To wystarcza dla jednego rekordu. Przy dwóch rekordach po liczbie pierwszego przychodzi nazwa drugiego, czyli `getline` po `>>`, a wtedy `getline` może odczytać pusty tekst. Lekcja 2.7 zapowiadała, że sposób na ten problem poznasz później. Ta lekcja go pokazuje.

Dlatego programy z tej lekcji odczytują **dokładnie dwa rekordy**, każdy do osobnych zmiennych. Jeden rekord nie ujawniłby problemu, a wiele rekordów w wektorze to temat lekcji 10.3.

Po tej lekcji będziesz:

- odczytywać pełną nazwę ze spacjami przez `std::getline`, a liczby przez `>>`;
- wyjaśniać, co zostaje w wejściu po odczycie liczby;
- dokańczać linię liczbową przez `std::getline(std::cin, rest)`, zanim odczytasz następną nazwę;
- odróżniać poprawnie odczytaną pustą nazwę od nieudanego odczytu;
- tworzyć dwa rekordy dopiero po sprawdzeniu wszystkich danych;
- dobierać dane, które ujawniają złą kolejność odczytów.

## 1. Przygotuj projekt

W `cpp-workspace` utwórz katalog `lesson_10_2` i skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program`. Program z punktu 2 wpisujesz w `main.cpp` tego katalogu.

Programy z tej lekcji nie wypisują pytań. Wpisuj dane linia po linii, jak w pokazanym bloku danych, i po każdej linii naciśnij **Enter**. Program kończy pracę sam po odczytaniu ostatniej liczby. W oknie **Run** wpisane linie mieszają się z wynikiem, jak w lekcji 7.4.

## 2. Dwie przesyłki

Program odczytuje dane dwóch przesyłek kierowanych do różnych miejsc. Każda przesyłka zajmuje dwie linie:

1. pełna nazwa miejsca docelowego, która może zawierać spacje;
2. liczba paczek.

Nazwa nie może być pusta. Liczba paczek musi być nieujemna, więc 0 jest dozwolone.

<!-- example: shipments -->
```cpp
#include <iostream>
#include <string>

struct Shipment {
    std::string destination;
    int boxes;
};

int main() {
    std::string first_destination{};
    int first_boxes{0};
    std::string rest{};
    std::string second_destination{};
    int second_boxes{0};

    std::getline(std::cin, first_destination);
    std::cin >> first_boxes;

    if (!std::cin.fail()) {
        std::getline(std::cin, rest);
        std::getline(std::cin, second_destination);
        std::cin >> second_boxes;
    }

    if (std::cin.fail()) {
        std::cout << "Input error\n";
    } else if (first_destination.empty() || first_boxes < 0 || second_destination.empty() || second_boxes < 0) {
        std::cout << "Invalid shipment\n";
    } else {
        const Shipment first{first_destination, first_boxes};
        const Shipment second{second_destination, second_boxes};

        std::cout << "Shipment 1: " << first.destination << ", boxes " << first.boxes << "\n";
        std::cout << "Shipment 2: " << second.destination << ", boxes " << second.boxes << "\n";
        std::cout << "Total boxes: " << first.boxes + second.boxes << "\n";
    }
}
```

Uruchom program i wpisz:

<!-- input: shipments -->
```text
North Hub
4
South Depot
7
```

<!-- output: shipments -->
```text
Shipment 1: North Hub, boxes 4
Shipment 2: South Depot, boxes 7
Total boxes: 11
```

| Zapis | Co robi |
|---|---|
| `std::getline(std::cin, first_destination);` | odczytuje całą pierwszą linię, ze spacją: `North Hub` |
| `std::cin >> first_boxes;` | odczytuje liczbę 4 |
| `if (!std::cin.fail())` | czyta dalej tylko wtedy, gdy pierwsza przesyłka się odczytała |
| `std::getline(std::cin, rest);` | dokańcza linię z liczbą 4 (punkt 3) |
| `std::getline(std::cin, second_destination);` | odczytuje `South Depot` |
| `std::cin >> second_boxes;` | odczytuje liczbę 7 |
| `const Shipment first{...}` i `second{...}` | tworzą dwa rekordy, dopiero po wszystkich sprawdzeniach |

- **Każda przesyłka ma własne zmienne i własny rekord,** bez wektora i bez pętli.
- **Najpierw stan strumienia, potem zasady:** `std::cin.fail()` przed `empty()` i `< 0`, jak w lekcji 10.1.
- **Suma pochodzi z pól rekordów.**
- **Jeden z trzech wyników:** raport, `Input error` albo `Invalid shipment`. Gdy druga przesyłka jest błędna, program nie wypisuje też pierwszej.

## 3. Co zostaje w wejściu po liczbie

Prześledź, co odczytuje każda operacja i co jest następne w wejściu zaraz po niej:

| Po operacji | Zmienna dostaje | Następne w wejściu |
|---|---|---|
| `std::getline(std::cin, first_destination)` | `North Hub` | `4` |
| `std::cin >> first_boxes` | 4 | **koniec linii po `4`** |
| `std::getline(std::cin, rest)` | pusty tekst | `South Depot` |
| `std::getline(std::cin, second_destination)` | `South Depot` | `7` |
| `std::cin >> second_boxes` | 7 | koniec linii po `7`, którego program już nie czyta |

`getline` zabiera z wejścia koniec linii, ale nie zapisuje go w tekście (lekcja 7.4). `>>` zatrzymuje się na pierwszym białym znaku po liczbie i **zostawia go w wejściu**. Po `4` następny jest więc koniec tej samej linii, a nie `South Depot`.

Gdyby zaraz po `>> first_boxes` program wywołał `std::getline(std::cin, second_destination)`, odczytałby tylko ten koniec linii, czyli pusty tekst. `South Depot` czekałoby dalej w wejściu. To problem z lekcji 2.7.

Dlatego między liczbą a następną nazwą stoi dodatkowy odczyt:

<!-- fragment -->
```cpp
std::cin >> first_boxes;
// Check the read.

std::getline(std::cin, rest);
// Check the read.

std::getline(std::cin, second_destination);
// Check the read.
```

`std::getline(std::cin, rest)` to konstrukcja z lekcji 4.6 w nowej roli:

- odczytuje to, co zostało z bieżącej linii, tutaj nic;
- zabiera z wejścia także koniec linii, ale nie zapisuje go w `rest`;
- pusty `rest` to **udany** odczyt: nie oznacza błędu ani końca danych;
- nie sprawdza odczytanych znaków. To nie kontrola danych, tylko przejście do następnej linii.

Każdy z tych trzech odczytów może się nie udać, ale program z punktu 2 nie potrzebuje osobnego `if` po każdym. Sprawdzenie po pierwszej liczbie decyduje, czy czytać dalej. Sprawdzenie na końcu obejmuje pozostałe odczyty: gdy jeden się nie uda, kolejne też się nie udają (lekcja 4.6).

**Po ostatniej liczbie linii nie dokańczamy,** bo program nie czyta już następnej nazwy. Dodatkowe `getline` byłoby nawet szkodliwe. Gdy dane kończą się zaraz po `7`, bez końca linii, na przykład w pliku, odczyt `7` się udaje, choć strumień doszedł do końca danych (lekcja 4.6). Kolejne `getline` nie miałoby czego odczytać i by się nie udało, więc program wypisałby `Input error` dla poprawnych danych. Testy automatyczne kursu tego przypadku nie uruchamiają, bo w nich każda linia ma swój koniec.

## 4. Pusta nazwa a brak danych

Lekcja 7.4 rozróżniała dwie sytuacje:

- **pusta linia** to udany odczyt pustego tekstu: `fail()` daje `false`, a `empty()` daje `true`;
- **brak linii** to nieudany odczyt: `fail()` daje `true`, a na zawartości zmiennej nie wolno polegać.

**Przewidź** wynik dla danych, w których druga nazwa jest pustą linią. Uruchomienie jest nieobowiązkowe.

<!-- input: shipments -->
```text
North Hub
4

7
```

<details>
<summary>Standardowe wyjście dla pustej drugiej nazwy</summary>

<!-- output: shipments -->
```text
Invalid shipment
```

</details>

Pusta linia odczytała się poprawnie, więc program sprawdza zasady i odrzuca pustą nazwę.

**Przewidź** też wynik, gdy dane kończą się zaraz po `4`. Tego przypadku nie wywołasz ręcznie: **Enter** zamiast drugiej nazwy daje pustą nazwę. Prześledź go na papierze.

<!-- input: shipments -->
```text
North Hub
4
```

<details>
<summary>Standardowe wyjście, gdy po 4 dane się kończą</summary>

<!-- output: shipments -->
```text
Input error
```

</details>

`getline(rest)` zabiera koniec linii po `4`, ale drugiej nazwy już nie ma. Kolejne `getline` nie dostarcza żadnej linii i się nie udaje, więc program wypisuje `Input error` i nie sprawdza nazw. Kolejność jest stała:

1. spróbuj odczytać dane;
2. sprawdź `std::cin.fail()`;
3. dopiero po udanym odczycie sprawdź `empty()` i zasady liczb;
4. rekordy utwórz tylko z zaakceptowanych danych.

| Sytuacja | Przykład | Wynik |
|---|---|---|
| nieudany odczyt | `four` zamiast pierwszej liczby, `seven` zamiast drugiej, brak drugiej przesyłki | `Input error` |
| udany odczyt, wartość niedozwolona | pusta pierwsza albo druga nazwa, liczba paczek `-2` | `Invalid shipment` |
| udany odczyt, wartości dozwolone | 0 paczek w pierwszej przesyłce | raport dwóch przesyłek |

<details>
<summary>Pozostałe dane z tabeli i ich wyniki</summary>

<!-- input: shipments -->
```text
North Hub
four
South Depot
7
```

<!-- output: shipments -->
```text
Input error
```

<!-- input: shipments -->
```text
North Hub
4
South Depot
seven
```

<!-- output: shipments -->
```text
Input error
```

<!-- input: shipments -->
```text

4
South Depot
7
```

<!-- output: shipments -->
```text
Invalid shipment
```

<!-- input: shipments -->
```text
North Hub
4
South Depot
-2
```

<!-- output: shipments -->
```text
Invalid shipment
```

<!-- input: shipments -->
```text
North Hub
0
South Depot
7
```

<!-- output: shipments -->
```text
Shipment 1: North Hub, boxes 0
Shipment 2: South Depot, boxes 7
Total boxes: 7
```

</details>

## 5. Czego program nie sprawdza

Dwie rzeczy świadomie pomijamy.

**Tekst po liczbie.** **Przewidź** wynik dla danych z dodatkowym słowem po pierwszej liczbie:

<!-- input: shipments -->
```text
North Hub
4 extra
South Depot
7
```

<details>
<summary>Standardowe wyjście dla 4 extra</summary>

<!-- output: shipments -->
```text
Shipment 1: North Hub, boxes 4
Shipment 2: South Depot, boxes 7
Total boxes: 11
```

</details>

`rest` dostaje ` extra`, ze spacją na początku, a program tego tekstu nie ocenia. Takie dane są poza umową, bo poprawna linia liczbowa zawiera tylko liczbę. Program nie zgłasza błędu, ale też nie potwierdza, że linia była poprawna. Tekst po ostatniej liczbie zostaje nieodczytany, jak w lekcji 10.1.

**Nazwy niepuste, ale niepoprawne.** `empty()` odrzuca tylko tekst o długości zero. Nazwa z samych spacji nie jest pusta (lekcja 7.4), więc przejdzie to sprawdzenie. W danych zgodnych z umową nazwa nie ma spacji na początku ani na końcu, a program takich spacji nie usuwa ani nie wykrywa. `empty()` mówi więc tylko, że nazwa nie jest pusta, a nie, że jest poprawna.

## 6. Misja: postęp czytania dwóch książek

Program odczytuje dane dwóch książek i wypisuje, ile stron zostało do przeczytania w obu razem.

**Dane wejściowe:** każda książka zajmuje dwie linie:

1. tytuł, który może zawierać spacje;
2. dwie liczby oddzielone spacją: liczba wszystkich stron i liczba stron już przeczytanych.

**Reguły:**

- Tytuł nie może być pusty. W danych zgodnych z umową nie ma spacji na jego początku ani końcu, a program ich nie sprawdza.
- Liczba stron musi być większa od zera.
- Liczba przeczytanych stron musi być nieujemna i nie może przekraczać liczby stron.
- Wszystkie liczby są niewielkie i mieszczą się w `int`, ich suma też.
- Tekst po liczbach jest poza umową i program go nie sprawdza.

**Wymagania:**

- Program definiuje własny typ książki z trzema polami: tytułem (`std::string`), liczbą stron (`int`) i liczbą przeczytanych stron (`int`). Nazwy typu i pól wybierasz samodzielnie.
- Odczyt jest w `main`, do zmiennych lokalnych z wartościami początkowymi: tytuły przez `std::getline`, liczby przez `>>`. Bez pytań, bez ponawiania i bez wektora.
- Gdy nie uda się odczytać wymaganych danych, także gdy dane kończą się po pierwszej książce, program wypisuje dokładnie `Input error`.
- Gdy odczyt się udał, ale któryś tytuł jest pusty albo liczby łamią zasady, program wypisuje dokładnie `Invalid books`.
- Dopiero gdy wszystko się zgadza, program tworzy dwa rekordy przez `{}` i wypisuje siedem linii jak w przykładzie niżej, z książkami w kolejności z danych. Suma nieprzeczytanych stron pochodzi z pól obu rekordów.

W `cpp-workspace` utwórz katalog `reading_progress`, skopiuj do niego `CMakeLists.txt` z oryginalnego `lesson_05_first_program`, utwórz pusty `main.cpp` i napisz program samodzielnie.

Dla danych:

<!-- input: books -->
```text
Ocean Atlas
120 50
Quiet Garden
80 80
```

standardowe wyjście ma być takie:

<!-- output: books -->
```text
Book 1: Ocean Atlas
Pages: 120
Read: 50
Book 2: Quiet Garden
Pages: 80
Read: 80
Unread total: 70
```

Tytuł drugiej książki to pusta linia. Odczyt się udaje, ale tytuł jest pusty:

<!-- input: books -->
```text
Ocean Atlas
120 50

80 80
```

<!-- output: books -->
```text
Invalid books
```

Zamiast liczby stron drugiej książki jest słowo:

<!-- input: books -->
```text
Ocean Atlas
120 50
Quiet Garden
eighty 20
```

<!-- output: books -->
```text
Input error
```

Dla jednego uruchomienia program wypisuje tylko jeden z tych trzech wyników.

**To nie są przesyłki z inną nazwą.** Linia liczbowa ma dwie liczby, a jedna z zasad łączy obie. Musisz samodzielnie zdecydować:

1. jak nazwać typ i pola oraz jakich zmiennych lokalnych potrzebujesz do odczytu;
2. które wartości odczytać przez `std::getline`, a które przez `>>`;
3. w którym miejscu dokończyć linię liczbową pierwszej książki i dlaczego nie trzeba dokańczać ostatniej;
4. kiedy sprawdzić powodzenie odczytów;
5. jak oddzielić `Input error` od `Invalid books`, także przy pustym tytule;
6. jak zapisać zasady obu książek;
7. w którym miejscu utworzyć dwa rekordy;
8. jak obliczyć sumę nieprzeczytanych stron z pól rekordów.

**Zanim napiszesz program**, przygotuj tabelę przypadków: tytuły ze spacjami i jednowyrazowe, książki przeczytane i nierozpoczęte, puste tytuły, niedozwolone liczby stron, słowo zamiast liczby, brak drugiej książki i brak ostatniej liczby. Przy każdym zapisz oczekiwany wynik.

**Potem** uruchom program dla głównych danych i dla jednego z dwóch pozostałych przykładów. Wszystkie przypadki z pełnej listy kontrolnej są sprawdzone automatycznie, więc pozostałych nie musisz uruchamiać. Przypadki, w których dane się kończą, przeanalizuj na papierze, jak w punkcie 4.

### Kryterium sukcesu

- Program buduje się jako C++20 i dla głównych danych oraz wybranego drugiego przykładu wypisuje dokładnie pokazane wyniki.
- Tytuły zachowują spacje wewnątrz.
- Linia liczbowa pierwszej książki jest dokończona przed odczytem drugiego tytułu, a po ostatniej liczbie nie ma już odczytu.
- `std::cin.fail()` jest sprawdzane przed tytułami i zasadami stron, a oba rekordy powstają dopiero po wszystkich sprawdzeniach.
- Tabela przypadków powstała przed uruchomieniem programu.
- Umiesz wyjaśnić, dlaczego pusty tytuł daje `Invalid books`, a brak tytułu `Input error`.

Gdy wynik się zgadza, możesz zapisać projekt w Gicie, jak w lekcji 1.5.

<details>
<summary>Podpowiedź 1</summary>

Skąd program wie, gdzie zaczyna się tytuł drugiej książki? Co pozostało po odczytaniu liczb pierwszej książki?

</details>

<details>
<summary>Podpowiedź 2</summary>

`>>` odczytuje liczby, ale nie musi pobrać znaku końca linii. Zanim odczytasz nowy tytuł, dokończ bieżącą linię.

</details>

<details>
<summary>Podpowiedź 3</summary>

Po sprawdzeniu odczytu liczb pierwszej książki użyj `getline` do odczytania reszty ich linii. Dopiero następnym `getline` odczytaj tytuł drugiej książki. Rekordy utwórz po kontroli całego wejścia.

</details>

<details>
<summary>Pełna lista przypadków kontrolnych: otwórz po przygotowaniu własnej tabeli</summary>

Kolejne linie danych oddziela `/`. Przy poprawnych danych kolumna „Wynik” podaje sumę nieprzeczytanych stron. Program wypisuje wtedy wszystkie siedem linii, z książkami w kolejności z danych.

| | Dane | Wynik | Co sprawdza |
|---|---|---|---|
| A | `Ocean Atlas` / `120 50` / `Quiet Garden` / `80 80` | 70 | dane z wymagań: dwa tytuły ze spacjami, pierwsza książka rozpoczęta, druga przeczytana |
| B | `Atlas` / `100 10` / `Night Train` / `50 0` | 140 | tytuł jednowyrazowy, potem tytuł ze spacją |
| C | `Deep Blue Sea` / `300 120` / `Maps` / `40 0` | 220 | tytuł ze spacjami, potem jednowyrazowy |
| D | `One Page` / `1 1` / `Long Road Home` / `90 90` | 0 | obie książki przeczytane, najmniejsza liczba stron |
| E | `First Light` / `200 0` / `Second Wind` / `150 0` | 350 | żadna książka nierozpoczęta |
| F | pusta linia / `120 50` / `Quiet Garden` / `80 80` | `Invalid books` | pusty pierwszy tytuł |
| G | `Ocean Atlas` / `120 50` / pusta linia / `80 80` | `Invalid books` | pusty drugi tytuł (dane z wymagań) |
| H | `Ocean Atlas` / `0 0` / `Quiet Garden` / `80 80` | `Invalid books` | zerowa liczba stron w pierwszej książce |
| I | `Ocean Atlas` / `120 50` / `Quiet Garden` / `0 0` | `Invalid books` | zerowa liczba stron w drugiej książce |
| J | `Ocean Atlas` / `120 50` / `Quiet Garden` / `-5 0` | `Invalid books` | ujemna liczba stron |
| K | `Ocean Atlas` / `120 -1` / `Quiet Garden` / `80 80` | `Invalid books` | ujemna liczba przeczytanych stron w pierwszej książce |
| L | `Ocean Atlas` / `120 50` / `Quiet Garden` / `80 -1` | `Invalid books` | ujemna liczba przeczytanych stron w drugiej książce |
| M | `Ocean Atlas` / `120 121` / `Quiet Garden` / `80 80` | `Invalid books` | więcej przeczytanych stron niż wszystkich w pierwszej książce |
| N | `Ocean Atlas` / `120 50` / `Quiet Garden` / `80 81` | `Invalid books` | więcej przeczytanych stron niż wszystkich w drugiej książce |
| O | `Ocean Atlas` / `many 50` / `Quiet Garden` / `80 80` | `Input error` | słowo zamiast pierwszej liczby |
| P | `Ocean Atlas` / `120 half` / `Quiet Garden` / `80 80` | `Input error` | słowo zamiast drugiej liczby |
| Q | `Ocean Atlas` / `120 50` / `Quiet Garden` / `eighty 20` | `Input error` | nieudany odczyt liczby w drugiej książce (dane z wymagań) |
| R | `Ocean Atlas` / `120 50`, potem koniec danych | `Input error` | brak drugiej książki: odczyt drugiego tytułu się nie udaje |
| S | `Ocean Atlas` / `120 50` / `Quiet Garden` / `80`, potem koniec danych | `Input error` | brak ostatniej liczby |
| T | `Ocean Atlas` / `120 50 pages` / `Quiet Garden` / `80 80` | 70 | tekst po liczbach pierwszej książki: `rest` go zabiera, ale program go nie sprawdza |
| U | `Ocean Atlas` / `120 50` / `Quiet Garden` / `80 80 done` | 70 | tekst po ostatniej liczbie: zostaje nieodczytany, poza sprawdzaniem |

**Testy automatyczne i Twoje próby.** Wszystkie przypadki są sprawdzone automatycznie: rozwiązanie referencyjne jest uruchamiane dla każdego z nich, a jego pełne standardowe wyjście porównywane z oczekiwanym. Rozwiązanie i jego wyniki są w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

</details>

Przykładowe rozwiązanie jest w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 7. Znajdź błąd: linia dokończona w złym miejscu

To zadanie wykonaj **po misji**: program poniżej ma działać tak samo jak program z punktu 2. Możesz go skopiować do `main.cpp` w katalogu `lesson_10_2`.

<details>
<summary>Program do sprawdzenia: otwórz po napisaniu własnego programu</summary>

<!-- example: shipments_order_bug -->
```cpp
#include <iostream>
#include <string>

struct Shipment {
    std::string destination;
    int boxes;
};

int main() {
    std::string first_destination{};
    int first_boxes{0};
    std::string rest{};
    std::string second_destination{};
    int second_boxes{0};

    std::getline(std::cin, first_destination);
    std::cin >> first_boxes;

    if (!std::cin.fail()) {
        std::getline(std::cin, second_destination);
        std::getline(std::cin, rest);
        std::cin >> second_boxes;
    }

    if (std::cin.fail()) {
        std::cout << "Input error\n";
    } else if (first_destination.empty() || first_boxes < 0 || second_destination.empty() || second_boxes < 0) {
        std::cout << "Invalid shipment\n";
    } else {
        const Shipment first{first_destination, first_boxes};
        const Shipment second{second_destination, second_boxes};

        std::cout << "Shipment 1: " << first.destination << ", boxes " << first.boxes << "\n";
        std::cout << "Shipment 2: " << second.destination << ", boxes " << second.boxes << "\n";
        std::cout << "Total boxes: " << first.boxes + second.boxes << "\n";
    }
}
```

Dane, w których druga nazwa jest pustą linią:

<!-- input: shipments_order_bug -->
```text
North Hub
4

7
```

1. **Przewidź** wynik tego programu dla tych danych. Program z punktu 2 wypisuje dla nich `Invalid shipment` (punkt 4).
2. Uruchom program dla tych danych i porównaj wynik z przewidywaniem.
3. Dobierz własne poprawne dane, z niepustą drugą nazwą, dla których ten program wypisze zły wynik.
4. Dla swoich danych **przewidź**, co trafi do `second_destination`, a co do `rest`.
5. Uruchom program dla swoich danych.
6. Wyjaśnij, dlaczego `getline` odczytało niewłaściwy fragment wejścia.
7. Popraw kolejność wywołań i uruchom poprawiony program dla swoich danych.
8. Dlaczego pusty `rest` w poprawionym programie nie oznacza nieudanego odczytu?

</details>

Wyniki, przykładowe dane i poprawiony program są w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 8. Gdy coś pójdzie inaczej

| Co widzisz | Co to znaczy | Co zrobić |
|---|---|---|
| `Input error` dla poprawnych danych z tytułem ze spacją | Tytuł jest odczytywany przez `>>`: do zmiennej trafia pierwsze słowo, a odczyt liczby trafia na drugie. | Odczytuj tytuł przez `std::getline`. |
| `Input error` dla poprawnych danych, choć tytuły odczytuje `getline` | Linia liczbowa pierwszej książki nie jest dokończona. Drugi tytuł jest pusty, a odczyt liczby trafia na prawdziwy tytuł. | Po liczbach pierwszej książki wywołaj `std::getline(std::cin, rest)`. |
| `Invalid books` albo `Invalid shipment` dla poprawnych danych | Linia jest dokończona dopiero po odczycie drugiego tytułu (punkt 7). | Dokończ linię przed odczytem następnego tytułu. |
| Pusty tytuł daje `Input error` | Program sprawdza pusty tytuł razem z `std::cin.fail()`, a pusta linia to udany odczyt. | Oceniaj pusty tytuł razem z zasadami stron, po sprawdzeniu odczytu. |
| Pusty tytuł daje raport | Brakuje sprawdzenia `empty()`. | Odrzucaj pusty tytuł tak jak niedozwolone liczby. |
| `Unread total` jest ujemne | Program przepuszcza więcej przeczytanych stron niż wszystkich. | Sprawdzaj tę zasadę dla obu książek. |
| Program czeka, choć wpisano wszystkie linie | Zamiast liczb wpisano pustą linię albo za mało liczb. `>>` pomija puste linie i czeka na liczbę (lekcja 10.1). | Wpisz brakujące liczby. |

## 9. Wyjaśnij

Odpowiedz własnymi słowami, najlepiej na piśmie. Dopiero potem porównaj z przykładowymi odpowiedziami.

1. Co odczyta `>>`, a co `std::getline` z linii `Ocean Atlas`? Dlaczego tytuł odczytujemy przez `getline`, a liczby przez `>>`?
2. Co zostaje w wejściu zaraz po odczycie `120 50` przez dwa `>>`? Co dostałoby `getline` wywołane w tym miejscu?
3. Do czego służy `rest`? Czy pusty `rest` oznacza błąd odczytu albo koniec danych?
4. Czym różni się pusty tytuł drugiej książki od braku drugiej książki? Jaki wynik daje każdy z tych przypadków?
5. Dlaczego program sprawdza `std::cin.fail()`, zanim sprawdzi `empty()`?
6. Czym różnią się `Input error` i `Invalid books`? Podaj po jednym przykładzie danych dla każdego wyniku.
7. Co program zrobi z tekstem `pages` w linii `120 50 pages`? Czy to znaczy, że ta linia jest poprawna?
8. Dlaczego program nie dokańcza linii po ostatniej liczbie drugiej książki?
9. Dwie książki są w dwóch osobnych rekordach. Co byłoby trudne, gdyby książek było dziesięć albo gdyby ich liczba nie była znana z góry?

<details>
<summary>Przykładowe odpowiedzi</summary>

1. `>>` odczyta samo `Ocean`, bo kończy odczyt tekstu na pierwszej spacji, a `Atlas` zostanie w wejściu. `std::getline` odczyta całą linię, `Ocean Atlas`, ze spacją w środku. Tytuł może mieć spacje, więc odczytuje go `getline`. Każda liczba jest jedną wartością, więc odczytuje ją `>>`: pomija białe znaki przed liczbą i kończy odczyt na pierwszym po niej.
2. Koniec tej linii, bo `>>` zatrzymuje się przed nim i zostawia go w wejściu. `getline` wywołane w tym miejscu odczytałoby tylko ten koniec linii i dostałoby pusty tekst, a następny tytuł czekałby dalej.
3. `rest` przyjmuje resztę linii liczbowej, a `getline` zabiera przy tym jej koniec. Dzięki temu następne `getline` zaczyna od nowej linii. Pusty `rest` to udany odczyt: w linii po liczbach nie było już innych znaków. O błędzie albo końcu danych mówi `std::cin.fail()`, a nie zawartość `rest`.
4. Pusty tytuł to pusta linia: odczyt się udaje, a tekst jest pusty. Program przechodzi do zasad i wypisuje `Invalid books`. Gdy drugiej książki nie ma, `getline` nie dostarcza żadnej linii i się nie udaje. Program wypisuje wtedy `Input error`.
5. Bo po nieudanym odczycie nie wolno polegać na zawartości zmiennej (lekcje 4.6 i 7.4). Pusty tytuł ma znaczenie tylko wtedy, gdy naprawdę został odczytany. W odwrotnej kolejności brak danych mógłby zostać uznany za pusty tytuł.
6. `Input error` znaczy, że nie udało się odczytać wymaganych danych, na przykład `eighty 20` zamiast liczb albo dane kończą się po pierwszej książce. `Invalid books` znaczy, że wszystko się odczytało, ale wartości łamią zasady, na przykład pusty tytuł albo `80 81`.
7. `>>` odczyta 120 i 50, a `getline(rest)` zabierze ` pages` razem z końcem linii. Program tego tekstu nie sprawdza, więc wypisze raport (przypadek T). Nie znaczy to, że linia jest poprawna: dane z dodatkowym tekstem są poza umową, a program po prostu ich nie ocenia.
8. Bo po ostatniej liczbie program nie odczytuje już żadnego tytułu. Dodatkowe `getline` byłoby niepotrzebne. Gdyby dane kończyły się zaraz po ostatniej liczbie, bez końca linii, takie `getline` by się nie udało i zamieniło poprawne dane w `Input error`.
9. Każda książka potrzebuje tu własnych zmiennych, własnych odczytów i własnego rekordu. Przy dziesięciu książkach kod byłby długi i powtarzalny, a przy nieznanej liczbie książek nie dałoby się go tak napisać. Rekordy trzeba będzie dodawać do wektora, co jest tematem lekcji 10.3.

</details>

## Podsumowanie

- Nazwę ze spacjami odczytuje `std::getline`, a liczby `>>`.
- Po odczycie liczby przez `>>` w wejściu zostaje koniec linii. `getline` wywołane zaraz potem odczytałoby pusty tekst.
- `std::getline(std::cin, rest)` dokańcza linię liczbową przed odczytem następnej nazwy. Pusty `rest` to udany odczyt, a zawartości `rest` program nie sprawdza.
- Po ostatniej liczbie linii nie dokańczamy, bo dodatkowy odczyt mógłby zamienić poprawne dane w błąd.
- Pusta nazwa to udany odczyt i niedozwolona wartość, a brak nazwy to nieudany odczyt. Dlatego najpierw `std::cin.fail()`, potem `empty()`.
- Rekordy powstają dopiero po sprawdzeniu wszystkich danych, a wynik pochodzi z ich pól.

## Co dalej

W tej lekcji program odczytywał dokładnie dwa rekordy, każdy do osobnych zmiennych. W kolejnej lekcji rekordy odczytane z wejścia trafią do wektora przez `push_back`. Lekcja 10.3 jest w przygotowaniu.

---

## Przykładowe rozwiązania

Zajrzyj tutaj **po własnej próbie**. Twoje nazwy mogą się różnić, jeśli standardowe wyjście jest takie, jak wymagane.

<details>
<summary>Punkt 6: misja, postęp czytania dwóch książek</summary>

<!-- example: books -->
```cpp
#include <iostream>
#include <string>

struct Book {
    std::string title;
    int pages;
    int pages_read;
};

int main() {
    std::string first_title{};
    int first_pages{0};
    int first_pages_read{0};
    std::string rest{};
    std::string second_title{};
    int second_pages{0};
    int second_pages_read{0};

    std::getline(std::cin, first_title);
    std::cin >> first_pages;
    std::cin >> first_pages_read;

    if (!std::cin.fail()) {
        std::getline(std::cin, rest);
        std::getline(std::cin, second_title);
        std::cin >> second_pages;
        std::cin >> second_pages_read;
    }

    if (std::cin.fail()) {
        std::cout << "Input error\n";
    } else if (first_title.empty() || first_pages <= 0 || first_pages_read < 0 || first_pages_read > first_pages) {
        std::cout << "Invalid books\n";
    } else if (second_title.empty() || second_pages <= 0 || second_pages_read < 0 || second_pages_read > second_pages) {
        std::cout << "Invalid books\n";
    } else {
        const Book first{first_title, first_pages, first_pages_read};
        const Book second{second_title, second_pages, second_pages_read};
        const int unread_total{(first.pages - first.pages_read) + (second.pages - second.pages_read)};

        std::cout << "Book 1: " << first.title << "\n";
        std::cout << "Pages: " << first.pages << "\n";
        std::cout << "Read: " << first.pages_read << "\n";
        std::cout << "Book 2: " << second.title << "\n";
        std::cout << "Pages: " << second.pages << "\n";
        std::cout << "Read: " << second.pages_read << "\n";
        std::cout << "Unread total: " << unread_total << "\n";
    }
}
```

1. **Tytuł przez `getline`,** bo może zawierać spacje, a `>>` odczytałby tylko jego pierwsze słowo.
2. **Liczby przez `>>`,** bo każda jest jedną wartością, a `>>` pomija spację między nimi.
3. **Dokończenie pierwszej linii liczbowej,** bo po `>>` zostaje w wejściu koniec tej linii. Bez `getline(rest)` drugi tytuł byłby pusty, a odczyt liczby trafiłby na prawdziwy tytuł.
4. **Bez dokańczania po ostatniej liczbie,** bo program nie odczytuje już następnego tytułu.
5. **Sprawdzanie `getline`:** odczyt tytułu też może się nie udać, gdy danych już nie ma. Wtedy na zawartości zmiennej z tytułem nie wolno polegać. Sprawdzenie na końcu obejmuje więc także oba odczyty przez `getline` po pierwszej książce.
6. **Pusty tytuł to nie błąd odczytu.** Pusta linia odczytuje się poprawnie (lekcja 7.4), więc program ocenia ją razem z zasadami stron i wypisuje `Invalid books`.
7. **`fail()` nie zna zasad książki:** 0 stron albo 81 przeczytanych z 80 to poprawnie odczytane liczby. Zasady sprawdzają osobne warunki.
8. **Tekst po liczbach jest poza sprawdzaniem.** `getline(rest)` zabiera resztę pierwszej linii liczbowej, ale program jej nie ocenia (przypadek T). Tekst po ostatniej liczbie zostaje w wejściu nieodczytany (przypadek U). Takie dane są poza umową.
9. **Wartości początkowe zmiennych,** bo po nieudanym odczycie zmienna może zachować swoją dotychczasową wartość. Bez wartości początkowej byłaby to wartość nieokreślona.
10. **Rekordy na końcu,** bo dopiero wtedy wiadomo, że obie książki są kompletne i poprawne. Przy błędzie w drugiej książce nie powstaje też pierwszy rekord, więc nic nie jest wypisane częściowo.
11. **Bez wektora,** bo książek jest dokładnie dwie, a każda ma własne zmienne i własny rekord. Wektor rekordów to temat lekcji 10.3.
12. **Bez funkcji odczytującej rekord,** bo dwa odczyty mieszczą się czytelnie w `main`, a umowa takiej funkcji nie wymaga.
13. **Ostatnia liczba przy końcu danych.** Gdy dane kończą się zaraz po ostatniej liczbie, bez końca linii, jej odczyt i tak się udaje (lekcja 4.6). Program nie wykonuje po nim kolejnego odczytu, więc nie zamienia poprawnych danych w `Input error`. Testy automatyczne kursu tego przypadku nie uruchamiają.
14. **Przygotowanie do lekcji 10.3.** Schemat jednego rekordu jest stały: nazwa przez `getline`, liczby przez `>>` i dokończenie linii przed następną nazwą. Przy wielu rekordach ten sam schemat powtórzy się dla każdego z nich, a gotowe rekordy trafią do wektora.

**Inne poprawne rozwiązania:** zasady obu książek mogą stać w jednym warunku albo każda w osobnym `else if`, z tym samym komunikatem. Sprawdzenie po pierwszej książce można też pominąć i zostawić tylko to na końcu: wyniki będą te same, bo po nieudanym odczycie kolejne też się nie udają (lekcja 4.6). Sprawdzenie po pierwszej książce pokazuje jednak wprost, że linię dokańczamy dopiero po udanym odczycie liczb. Pola mogą mieć inne nazwy, a sumę można obliczyć bezpośrednio w instrukcji wypisania.

Każdy przypadek z listy kontrolnej to osobne uruchomienie tego programu. Przypadki A, G i Q to dane z treści misji. Pozostałe są poniżej, w kolejności z listy kontrolnej.

<!-- input: books -->
```text
Atlas
100 10
Night Train
50 0
```

<!-- output: books -->
```text
Book 1: Atlas
Pages: 100
Read: 10
Book 2: Night Train
Pages: 50
Read: 0
Unread total: 140
```

<!-- input: books -->
```text
Deep Blue Sea
300 120
Maps
40 0
```

<!-- output: books -->
```text
Book 1: Deep Blue Sea
Pages: 300
Read: 120
Book 2: Maps
Pages: 40
Read: 0
Unread total: 220
```

<!-- input: books -->
```text
One Page
1 1
Long Road Home
90 90
```

<!-- output: books -->
```text
Book 1: One Page
Pages: 1
Read: 1
Book 2: Long Road Home
Pages: 90
Read: 90
Unread total: 0
```

<!-- input: books -->
```text
First Light
200 0
Second Wind
150 0
```

<!-- output: books -->
```text
Book 1: First Light
Pages: 200
Read: 0
Book 2: Second Wind
Pages: 150
Read: 0
Unread total: 350
```

<!-- input: books -->
```text

120 50
Quiet Garden
80 80
```

<!-- output: books -->
```text
Invalid books
```

<!-- input: books -->
```text
Ocean Atlas
0 0
Quiet Garden
80 80
```

<!-- output: books -->
```text
Invalid books
```

<!-- input: books -->
```text
Ocean Atlas
120 50
Quiet Garden
0 0
```

<!-- output: books -->
```text
Invalid books
```

<!-- input: books -->
```text
Ocean Atlas
120 50
Quiet Garden
-5 0
```

<!-- output: books -->
```text
Invalid books
```

<!-- input: books -->
```text
Ocean Atlas
120 -1
Quiet Garden
80 80
```

<!-- output: books -->
```text
Invalid books
```

<!-- input: books -->
```text
Ocean Atlas
120 50
Quiet Garden
80 -1
```

<!-- output: books -->
```text
Invalid books
```

<!-- input: books -->
```text
Ocean Atlas
120 121
Quiet Garden
80 80
```

<!-- output: books -->
```text
Invalid books
```

<!-- input: books -->
```text
Ocean Atlas
120 50
Quiet Garden
80 81
```

<!-- output: books -->
```text
Invalid books
```

<!-- input: books -->
```text
Ocean Atlas
many 50
Quiet Garden
80 80
```

<!-- output: books -->
```text
Input error
```

<!-- input: books -->
```text
Ocean Atlas
120 half
Quiet Garden
80 80
```

<!-- output: books -->
```text
Input error
```

<!-- input: books -->
```text
Ocean Atlas
120 50
```

<!-- output: books -->
```text
Input error
```

<!-- input: books -->
```text
Ocean Atlas
120 50
Quiet Garden
80
```

<!-- output: books -->
```text
Input error
```

<!-- input: books -->
```text
Ocean Atlas
120 50 pages
Quiet Garden
80 80
```

<!-- output: books -->
```text
Book 1: Ocean Atlas
Pages: 120
Read: 50
Book 2: Quiet Garden
Pages: 80
Read: 80
Unread total: 70
```

<!-- input: books -->
```text
Ocean Atlas
120 50
Quiet Garden
80 80 done
```

<!-- output: books -->
```text
Book 1: Ocean Atlas
Pages: 120
Read: 50
Book 2: Quiet Garden
Pages: 80
Read: 80
Unread total: 70
```

</details>

<details>
<summary>Punkt 7: wyniki przed poprawką i poprawiony program</summary>

Przed poprawką, dla danych z pustą drugą nazwą:

<!-- output: shipments_order_bug -->
```text
Invalid shipment
```

- **Ten przypadek maskuje błąd.** Oba programy wypisują `Invalid shipment`, ale z innego powodu. W programie z punktu 2 `second_destination` dostaje pustą linię z danych. W programie z błędem dostaje koniec linii po `4`, czyli pusty tekst, a pusta linia z danych trafia do `rest`. Wynik jest ten sam, więc te dane błędu nie ujawniają.
- **Dane, które ujawniają błąd:** dowolne poprawne dane z niepustą drugą nazwą, na przykład dane z punktu 2. Poprawny wynik to raport dwóch przesyłek, a program z błędem wypisuje:

<!-- input: shipments_order_bug -->
```text
North Hub
4
South Depot
7
```

<!-- output: shipments_order_bug -->
```text
Invalid shipment
```

- **Co trafia do zmiennych:** `second_destination` dostaje pusty tekst, czyli resztę linii po `4`. `rest` dostaje `South Depot`, a `>>` odczytuje 7. Wszystkie odczyty się udały, więc program sprawdza zasady i odrzuca pustą nazwę.
- **Przyczyna:** `getline` czyta od miejsca, w którym skończył poprzedni odczyt. Po `>> first_boxes` tym miejscem jest koniec linii z liczbą 4. Pierwsze `getline` po liczbie zawsze odczyta resztę tej linii, niezależnie od tego, do jakiej zmiennej zapisuje tekst. Program z błędem zapisuje ją w `second_destination`.
- **Poprawka:** zamień kolejność dwóch wywołań: najpierw `getline` do `rest`, potem `getline` do `second_destination`. Poprawiony program to program z punktu 2:

<!-- example: shipments_order_fixed -->
```cpp
#include <iostream>
#include <string>

struct Shipment {
    std::string destination;
    int boxes;
};

int main() {
    std::string first_destination{};
    int first_boxes{0};
    std::string rest{};
    std::string second_destination{};
    int second_boxes{0};

    std::getline(std::cin, first_destination);
    std::cin >> first_boxes;

    if (!std::cin.fail()) {
        std::getline(std::cin, rest);
        std::getline(std::cin, second_destination);
        std::cin >> second_boxes;
    }

    if (std::cin.fail()) {
        std::cout << "Input error\n";
    } else if (first_destination.empty() || first_boxes < 0 || second_destination.empty() || second_boxes < 0) {
        std::cout << "Invalid shipment\n";
    } else {
        const Shipment first{first_destination, first_boxes};
        const Shipment second{second_destination, second_boxes};

        std::cout << "Shipment 1: " << first.destination << ", boxes " << first.boxes << "\n";
        std::cout << "Shipment 2: " << second.destination << ", boxes " << second.boxes << "\n";
        std::cout << "Total boxes: " << first.boxes + second.boxes << "\n";
    }
}
```

<!-- input: shipments_order_fixed -->
```text
North Hub
4
South Depot
7
```

<!-- output: shipments_order_fixed -->
```text
Shipment 1: North Hub, boxes 4
Shipment 2: South Depot, boxes 7
Total boxes: 11
```

- **Pusty `rest` w poprawionym programie:** `rest` jest pusty, bo po `4` nie było innych znaków. Odczyt się udał, a `getline` zabrało koniec linii. O nieudanym odczycie mówi `std::cin.fail()`, a nie pusty tekst.

</details>

**Poprzednia lekcja:** [Lekcja 10.1: Jeden rekord z danych wejściowych](lesson_01_one_record_from_input.md) · **Następna lekcja:** w przygotowaniu · [Opis kursu](../../README.md)

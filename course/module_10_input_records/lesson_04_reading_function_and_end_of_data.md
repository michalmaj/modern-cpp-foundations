# Lekcja 10.4: Funkcja odczytująca rekord i zakończenie danych

**Polski** · [English](lesson_04_reading_function_and_end_of_data.en.md) · [Opis kursu](../../README.md)

> **Moduł 10, lekcja 4** · około 90–110 minut, można ją podzielić na dwa podejścia
> **Potrzebujesz:** katalogu `cpp-workspace` i oryginalnego projektu `lesson_05_first_program`, jak dotąd. Debugger nie jest w tej lekcji potrzebny.
> **Wersja pilotażowa.** Programy z tej lekcji sprawdzamy automatycznie na Windowsie, Ubuntu i macOS, także z podanymi danymi wejściowymi. Wpisywanie danych w oknie **Run** CLiona opisujemy bez ręcznego sprawdzenia na każdym systemie.

## Zanim zaczniesz

Ta lekcja zakłada, że:

- pamiętasz, że odczyt może się udać i jednocześnie dojść do końca danych, a po nieudanym odczycie kolejne też się nie udają, dopóki strumień nie zostanie przywrócony przez `clear()` (lekcja 4.6);
- odróżniasz pustą linię od nieudanego odczytu i kończysz pętlę `while`, gdy odczyt się nie uda albo linia jest pusta (lekcja 7.4);
- przekazujesz do funkcji istniejący rekord przez `T&`, a funkcja `bool` najpierw sprawdza warunki i przy odmowie niczego w nim nie zmienia (lekcje 9.1 i 9.2);
- odczytujesz nazwę przez `std::getline`, liczby przez `>>` i dokańczasz linię liczbową przez `std::getline(std::cin, rest)` (lekcja 10.2);
- dodajesz do wektora przez `push_back` tylko kompletne, sprawdzone rekordy, a przy pierwszym błędzie kończysz `main` przez `return 0;`, bez częściowego raportu (lekcja 10.3).

## Sytuacja

W lekcji 10.3 pierwsza linia danych zapowiadała liczbę przesyłek, a cały odczyt był w `main`. Często jednak nikt nie liczy rekordów z góry: dane po prostu się kończą. Program czyta wtedy kolejne rekordy, aż w miejscu następnej nazwy trafi na pustą linię albo na koniec danych. Rozróżnia przy tym trzy sytuacje:

1. **poprawny rekord:** niepusta nazwa i poprawne liczby, więc rekord trafia do wektora;
2. **zakończenie danych:** pusta linia albo koniec danych w miejscu nazwy, więc program wypisuje raport;
3. **błąd rekordu:** nazwa już jest, ale liczb nie da się odczytać albo łamią zasady, więc program wypisuje tylko komunikat.

Odczyt liczb jednego rekordu trafi do osobnej funkcji, która dostanie przez referencje strumień wejścia i rekord do wypełnienia. Główna zasada tej lekcji: **funkcja zmienia rekord wynikowy dopiero wtedy, gdy wszystkie jego liczby są odczytane i spełniają zasady.**

Po tej lekcji będziesz:

- przekazywać `std::cin` do funkcji przez parametr `std::istream&`;
- pisać funkcję `bool`, która wypełnia istniejący rekord przez `T&`, a przy odmowie zostawia go bez zmian;
- czytać rekordy do pustej linii albo do końca danych i odróżniać zakończenie danych od niekompletnego rekordu;
- odróżniać po odmowie nieudany odczyt od niedozwolonej wartości;
- dobierać dane, które ujawniają zbyt wczesne przypisanie wyniku.

## 1. Przygotuj projekt

W `cpp-workspace` utwórz katalog `lesson_10_4` i skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program`. Program z punktu 2 wpisujesz w `main.cpp` tego katalogu.

Programy z tej lekcji nie wypisują pytań. Wpisuj dane linia po linii, jak w lekcji 10.3, a po ostatnim rekordzie naciśnij **Enter** jeszcze raz: pusta linia kończy dane. Końca danych nie musisz wywoływać samodzielnie.

## 2. Lista przesyłek bez zapowiedzianej liczby

Każda przesyłka zajmuje dwie linie, jak w lekcji 10.3: pełną nazwę miejsca docelowego i liczbę paczek, która nie może być ujemna. Liczby przesyłek nikt nie zapowiada. W danych zgodnych z umową jest ich najwyżej 5.

<!-- example: shipment_reader -->
```cpp
#include <iostream>
#include <string>
#include <vector>

struct Shipment {
    std::string destination;
    int boxes;
};

bool read_shipment_values(std::istream& input, const std::string& destination, Shipment& result) {
    int boxes{0};
    input >> boxes;

    if (input.fail()) {
        return false;
    }

    if (boxes < 0) {
        return false;
    }

    result = Shipment{destination, boxes};
    return true;
}

int main() {
    std::vector<Shipment> shipments{};
    std::string destination{};
    std::getline(std::cin, destination);

    while (!std::cin.fail() && !destination.empty()) {
        Shipment shipment{"", 0};
        const bool accepted{read_shipment_values(std::cin, destination, shipment)};

        if (!accepted) {
            if (std::cin.fail()) {
                std::cout << "Input error\n";
            } else {
                std::cout << "Invalid shipments\n";
            }

            return 0;
        }

        shipments.push_back(shipment);

        std::string rest{};
        std::getline(std::cin, rest);

        if (!std::cin.fail()) {
            std::getline(std::cin, destination);
        }
    }

    int total_boxes{0};
    std::cout << "Shipments: " << shipments.size() << "\n";

    for (const Shipment& shipment : shipments) {
        std::cout << shipment.destination << ": " << shipment.boxes << "\n";
        total_boxes += shipment.boxes;
    }

    std::cout << "Total boxes: " << total_boxes << "\n";
}
```

Uruchom program, wpisz dane, a na końcu pustą linię:

<!-- input: shipment_reader -->
```text
North Hub
4
South Depot
7

```

<!-- output: shipment_reader -->
```text
Shipments: 2
North Hub: 4
South Depot: 7
Total boxes: 11
```

| Zapis | Co robi |
|---|---|
| `bool read_shipment_values(...)` | odczytuje i sprawdza liczbę paczek jednej przesyłki, a przy sukcesie wypełnia rekord wynikowy (punkt 3) |
| `result = Shipment{destination, boxes};` | nadaje rekordowi wynikowemu nowe wartości obu pól |
| `std::getline(std::cin, destination);` przed pętlą | odczytuje pierwszą nazwę |
| `while (!std::cin.fail() && !destination.empty())` | powtarza przebiegi, dopóki odczyt nazwy się udał i nazwa nie jest pusta (punkt 5) |
| `Shipment shipment{"", 0};` | przygotowuje rekord, który funkcja ma wypełnić |
| `if (!accepted)` | po odmowie wybiera komunikat i kończy `main` (punkt 6) |
| `std::getline(std::cin, rest);` | po przyjętym rekordzie dokańcza jego linię liczbową |

- **`main` czyta nazwy i decyduje o zakończeniu danych.** Funkcja dostaje tylko poprawnie odczytaną, niepustą nazwę.
- **Funkcja czyta i sprawdza liczbę** jednego rekordu, a o powodzeniu informuje wynikiem `bool`. Niczego nie wypisuje.
- **Pusta linia nie jest już błędem rekordu.** W lekcji 10.3 pusta nazwa dawała `Invalid shipments`, bo program czekał na zapowiedziany rekord. Tutaj pusta linia w miejscu nazwy oznacza zakończenie danych.

## 3. Funkcja wypełnia istniejący rekord

Nagłówek funkcji z punktu 2:

<!-- fragment -->
```cpp
bool read_shipment_values(std::istream& input, const std::string& destination, Shipment& result)
```

- **`std::istream& input`:** `std::cin` to istniejący obiekt typu `std::istream`, czyli strumień wejścia, dostępny po `#include <iostream>`. Parametr z `&` to inna nazwa przekazanego obiektu (lekcja 9.1), więc `input >> boxes` czyta z tego samego `std::cin`, od miejsca, w którym skończył `main`. Funkcja nie otwiera nowego wejścia. `const` nie ma, bo odczyt zmienia strumień: zabiera z niego znaki i może zmienić jego stan.
- **`const std::string& destination`:** nazwę odczytał już `main`, a funkcja tylko jej używa, więc dostaje ją przez `const&`, jak tekst w lekcji 7.3.
- **`Shipment& result`:** funkcja wypełnia obiekt przygotowany przez `main`, zamiast tworzyć i zwracać nowy rekord przez wartość, jak w lekcji 8.5. Tamta umowa jest dobra, gdy wynik jest jeden. Tutaj są dwa: czy odczyt się udał i kompletny rekord. O powodzeniu mówi `bool`, a rekord trafia do obiektu wywołującego.

**Tak samo działa `std::getline`.** Lekcja 5.2 zapowiadała, że funkcje biblioteczne nie zawsze otrzymują dane tak jak parametr `int`. `std::getline(std::cin, line)` dostaje strumień i tekst przez referencje bez `const`: czyta ze strumienia i zmienia `line`. Nasza funkcja ma ten sam kształt.

Funkcja wykonuje kroki w tej kolejności:

1. przygotuj zmienną lokalną `boxes` z wartością początkową;
2. odczytaj liczbę przez `>>`;
3. sprawdź `input.fail()`;
4. sprawdź zasady;
5. przypisz kompletny rekord do `result`;
6. zwróć `true`.

Każda odmowa to `return false;` przed krokiem 5, więc **po `false` rekord `result` jest bez zmian** i nie wolno go uznać za nowo odczytany. To zasada „wszystko albo nic” z lekcji 9.2: żadnych zmian pól w trakcie sprawdzeń i żadnego odtwarzania. Program z punktu 2 po `false` i tak kończy pracę, ale inny wywołujący może dalej korzystać ze swojego rekordu, więc umowa obowiązuje zawsze (punkt 8).

**Przypisanie całego rekordu.** `Shipment{destination, boxes}` to wartość całego rekordu: nazwa typu i klamry, jak przy tworzeniu rekordu, ale bez nazwy obiektu. `result = ...;` przypisuje ją istniejącemu obiektowi, więc oba pola dostają nowe wartości naraz, jak zmienna w `second = first;` z lekcji 2.2. O takim przypisaniu wspominała lekcja 8.2. Nie powstaje drugi rekord wynikowy ani element wektora: `result` to wciąż `shipment` z `main`, a element doda dopiero `push_back`.

## 4. Kto rozpoznaje zakończenie danych

| Sytuacja | Co jest w danych w miejscu rekordu | Kto ją rozpoznaje | Co dalej |
|---|---|---|---|
| poprawny rekord | niepusta nazwa, a po niej poprawna liczba | `main` czyta nazwę, a funkcja liczbę i zwraca `true` | `push_back` i następna nazwa |
| zakończenie danych | pusta linia albo koniec danych | `main`, zaraz po odczycie nazwy | raport |
| błąd rekordu | niepusta nazwa, a po niej słowo, niedozwolona liczba albo koniec danych | funkcja, która zwraca `false` | komunikat i koniec programu |

**Dlaczego nazwę czyta `main`?** Bo to przy nazwie rozstrzyga się, czy dane się skończyły. Gdyby funkcja czytała także nazwę, jej wynik musiałby wyrazić trzy sytuacje z tabeli, a `bool` ma tylko dwie wartości. Gdy nazwę czyta `main`, funkcja jest wywoływana dopiero wtedy, gdy rekord się zaczął. Jej `true` znaczy wtedy „kompletny, poprawny rekord jest w `result`”, a `false` znaczy „nowego rekordu nie ma”.

**Niekompletny rekord to nie zakończenie danych.** Gdy dane kończą się zaraz po niepustej nazwie, rekord już się zaczął, ale brakuje jego liczby. Odczyt w funkcji się nie udaje, a program wypisuje `Input error`, a nie raport.

## 5. Pętla w `main` i ostatnia liczba

Warunek pętli łączy dwa sprawdzenia z lekcji 7.4, w tej samej kolejności: czy odczyt nazwy się udał i czy nazwa nie jest pusta. Dzięki krótkiemu obliczaniu (lekcja 3.4) `empty()` jest sprawdzane tylko po udanym odczycie. Pierwszą nazwę `main` odczytuje przed pętlą, a każdą następną na końcu przebiegu.

Prześledź główne dane:

| Przebieg | `destination` | Funkcja | `getline(rest)` dokańcza | Następna nazwa |
|---|---|---|---|---|
| 1 | `North Hub` | odczytuje 4, zwraca `true` | linię z `4` | `South Depot` |
| 2 | `South Depot` | odczytuje 7, zwraca `true` | linię z `7` | pusta linia, koniec pętli |

**Po przyjętym rekordzie program dokańcza jego linię liczbową,** bo może po niej nastąpić kolejna nazwa. W lekcji 10.3 po ostatnim rekordzie nie było już odczytu, bo program znał liczbę rekordów. Tutaj dowiaduje się, że rekord był ostatni, dopiero przy próbie odczytu następnej nazwy.

**Ostatnia liczba na samym końcu danych.** Gdy dane kończą się zaraz po `7`, bez końca linii, `>>` poprawnie odczytuje 7, choć strumień doszedł już do końca danych (lekcja 4.6), a funkcja zwraca `true`. Nie udaje się dopiero `getline(rest)`. To nie jest błąd ostatniego rekordu: jego liczba jest odczytana i sprawdzona, a rekord jest w wektorze. Dlatego `main` odczytuje następną nazwę tylko po udanym dokończeniu linii, a pętlę kończy `fail()` w warunku. Gdyby po nieudanym `getline(rest)` program wypisywał `Input error`, odrzuciłby poprawne dane.

| Gdzie kończą się dane | Co się nie udaje | Wynik |
|---|---|---|
| zaraz po nazwie, przed liczbą | `>>` w funkcji | `Input error` |
| zaraz po ostatniej liczbie, bez końca linii | `getline(rest)` | raport |
| po końcu linii z ostatnią liczbą | odczyt następnej nazwy | raport |

Testy automatyczne kursu sprawdzają pierwszy i ostatni wiersz tej tabeli. Środkowego nie uruchamiają, bo w nich każda linia ma swój koniec.

<details>
<summary>Dane z tabeli i ich wyniki</summary>

Dane kończą się zaraz po nazwie drugiej przesyłki:

<!-- input: shipment_reader -->
```text
North Hub
4
South Depot
```

<!-- output: shipment_reader -->
```text
Input error
```

Dane kończą się po końcu linii z `7`, bez pustej linii:

<!-- input: shipment_reader -->
```text
North Hub
4
South Depot
7
```

<!-- output: shipment_reader -->
```text
Shipments: 2
North Hub: 4
South Depot: 7
Total boxes: 11
```

</details>

## 6. Odmowa: nieudany odczyt czy niedozwolona wartość

Funkcja zwraca `false` w dwóch sytuacjach: gdy odczyt liczby się nie udał i gdy odczytana liczba jest ujemna. Dlatego po odmowie `main` sprawdza stan strumienia: po nieudanym odczycie `std::cin.fail()` daje `true` i program wypisuje `Input error`, a w przeciwnym razie `Invalid shipments`.

To działa, bo funkcja nie wywołuje `clear()`, więc stan po nieudanym odczycie zostaje do sprawdzenia w `main` (lekcja 4.6). `false` mówi, że nowego rekordu nie ma, a `fail()` mówi, czy zawiódł odczyt: to dwie osobne informacje. Ta konwencja dotyczy tej konkretnej funkcji, a nie każdego `bool`.

**Przewidź** wyniki dla trzech zestawów danych. Uruchomienia są nieobowiązkowe.

Druga przesyłka ma `-2` paczki:

<!-- input: shipment_reader -->
```text
North Hub
4
South Depot
-2
```

<details>
<summary>Standardowe wyjście, gdy druga przesyłka ma -2 paczki</summary>

<!-- output: shipment_reader -->
```text
Invalid shipments
```

</details>

Zamiast liczby paczek drugiej przesyłki jest słowo:

<!-- input: shipment_reader -->
```text
North Hub
4
South Depot
seven
```

<details>
<summary>Standardowe wyjście, gdy zamiast liczby jest słowo</summary>

<!-- output: shipment_reader -->
```text
Input error
```

</details>

Dane zaczynają się od pustej linii:

<!-- input: shipment_reader -->
```text

```

<details>
<summary>Standardowe wyjście dla pustej linii</summary>

<!-- output: shipment_reader -->
```text
Shipments: 0
Total boxes: 0
```

</details>

- **Błąd w drugiej przesyłce:** pierwsza jest już w wektorze, ale program wypisuje tylko komunikat i kończy pracę, jak w lekcji 10.3.
- **Pusta linia na początku:** pętla nie wykonuje się ani razu. Pusty wektor to poprawny wynik, bez zastępczego rekordu. Ten sam raport daje wejście bez żadnego znaku, ale tego przypadku testy automatyczne nie uruchamiają.

| Sytuacja | Przykład | Wynik |
|---|---|---|
| nieudany odczyt liczby | `seven` zamiast liczby paczek, koniec danych po nazwie | `Input error` |
| udany odczyt, wartość niedozwolona | `-2` paczki | `Invalid shipments` |
| zakończenie danych | pusta linia albo koniec danych w miejscu nazwy, także przed pierwszą przesyłką | raport |

<details>
<summary>Pozostałe dane i ich wyniki</summary>

Jedna przesyłka, a po niej koniec danych:

<!-- input: shipment_reader -->
```text
East Gate
3
```

<!-- output: shipment_reader -->
```text
Shipments: 1
East Gate: 3
Total boxes: 3
```

Pięć przesyłek, a po nich koniec danych:

<!-- input: shipment_reader -->
```text
Central Hub
2
North Hub
4
River Port
0
South Depot
7
West End Depot
1
```

<!-- output: shipment_reader -->
```text
Shipments: 5
Central Hub: 2
North Hub: 4
River Port: 0
South Depot: 7
West End Depot: 1
Total boxes: 14
```

Pusta linia po pierwszej przesyłce kończy dane, nawet gdy po niej są jeszcze linie. Program ich nie odczytuje:

<!-- input: shipment_reader -->
```text
North Hub
4

South Depot
7
```

<!-- output: shipment_reader -->
```text
Shipments: 1
North Hub: 4
Total boxes: 4
```

</details>

## 7. Misja: wyniki drużyn

Program odczytuje wyniki kolejnych drużyn turnieju, aż dane się skończą, i wypisuje wszystkie drużyny oraz sumę zwycięstw.

**Dane wejściowe:** każda drużyna zajmuje dwie linie:

1. nazwa drużyny, która może zawierać spacje;
2. dwie liczby oddzielone spacją: liczba rozegranych spotkań i liczba wygranych spotkań.

Liczby drużyn nikt nie zapowiada. Po ostatniej drużynie jest pusta linia albo dane się kończą.

**Reguły:**

- Nazwa drużyny nie jest pusta, bo pusta linia kończy dane. W danych zgodnych z umową nie ma spacji na jej początku ani końcu. Dwie drużyny mogą mieć tę samą nazwę.
- Liczba rozegranych spotkań nie może być ujemna, a liczba wygranych nie może być ujemna ani większa od liczby rozegranych. Dozwolone jest 0 rozegranych i 0 wygranych.
- Drużyn jest najwyżej 5, a liczby są niewielkie i mieszczą się w `int`, ich suma też. Tekst po liczbach jest poza umową i program go nie sprawdza.

**Wymagania:**

- Program definiuje własny typ drużyny z trzema polami: nazwą (`std::string`), liczbą rozegranych (`int`) i liczbą wygranych (`int`).
- Liczby jednej drużyny odczytuje i sprawdza osobna funkcja. Dostaje strumień przez `std::istream&`, nazwę przez `const std::string&` i istniejący rekord wynikowy przez referencję bez `const`. Liczby odczytuje do zmiennych lokalnych, a rekord przypisuje dopiero po sprawdzeniu odczytu i zasad. Zwraca `true` albo `false`, a przy `false` rekord wynikowy zostaje bez zmian. Niczego nie wypisuje.
- `main` odczytuje nazwy, rozpoznaje zakończenie danych i dodaje rekord do początkowo pustego wektora przez `push_back` tylko po `true`. Odczyt jest bez pytań.
- Gdy nie uda się odczytać wymaganej liczby, program wypisuje dokładnie `Input error`, a gdy liczby łamią zasady, dokładnie `Invalid teams`. W obu przypadkach kończy pracę bez żadnej części raportu.
- Po zakończeniu danych program wypisuje liczbę drużyn z `size()`, każdą drużynę w kolejności z danych i sumę zwycięstw, jak w przykładzie niżej, wszystko z elementów wektora.

W `cpp-workspace` utwórz katalog `team_results`, skopiuj do niego `CMakeLists.txt` z oryginalnego `lesson_05_first_program`, utwórz pusty `main.cpp` i napisz program samodzielnie.

Dla danych zakończonych pustą linią:

<!-- input: teams -->
```text
Maple Owls
6 4
River Foxes
3 3

```

standardowe wyjście ma być takie:

<!-- output: teams -->
```text
Teams: 2
Maple Owls: played 6, won 4
River Foxes: played 3, won 3
Wins total: 7
```

Te same dane bez pustej linii, zakończone końcem danych, dają ten sam wynik:

<!-- input: teams -->
```text
Maple Owls
6 4
River Foxes
3 3
```

<!-- output: teams -->
```text
Teams: 2
Maple Owls: played 6, won 4
River Foxes: played 3, won 3
Wins total: 7
```

Zamiast liczby wygranych drugiej drużyny jest słowo. Pierwsza mogła już trafić do wektora, ale raportu nie ma:

<!-- input: teams -->
```text
Maple Owls
6 4
River Foxes
3 won
```

<!-- output: teams -->
```text
Input error
```

Druga drużyna ma więcej wygranych niż rozegranych:

<!-- input: teams -->
```text
Maple Owls
6 4
River Foxes
3 4
```

<!-- output: teams -->
```text
Invalid teams
```

Dane zaczynają się od pustej linii:

<!-- input: teams -->
```text

```

<!-- output: teams -->
```text
Teams: 0
Wins total: 0
```

Gdy po niepustej nazwie zabraknie którejś liczby, wynik to `Input error`, a nie zakończenie danych.

**To nie są przesyłki z inną nazwą.** Linia liczbowa ma dwie liczby, a jedna z zasad łączy obie. Musisz samodzielnie zdecydować:

1. jak nazwać typ, jego pola, wektor, funkcję i jej parametry;
2. w jakiej kolejności funkcja odczytuje liczby, sprawdza odczyt i zasady i w którym miejscu przypisuje rekord wynikowy;
3. gdzie `main` odczytuje kolejne nazwy, po czym poznaje zakończenie danych i kiedy dokańcza linię liczbową;
4. w którym miejscu wywołać `push_back` i jak po odmowie odróżnić `Input error` od `Invalid teams`;
5. jak wypisać drużyny i obliczyć sumę zwycięstw z elementów wektora;
6. jakie dane ujawniłyby, że funkcja zmienia rekord wynikowy przed sprawdzeniem zasad.

**Zanim napiszesz program**, przygotuj tabelę przypadków z oczekiwanymi wynikami: pusta linia na początku, jedna, dwie i pięć drużyn, oba sposoby zakończenia, powtórzona nazwa, drużyna bez spotkań, same wygrane i same porażki, ujemne liczby, więcej wygranych niż rozegranych, słowo zamiast każdej z liczb, brak liczb po nazwie, brak ostatniej liczby i błąd w drużynie po poprawnej.

**Potem** uruchom program dla głównych danych i dla jednego z dwóch błędów w drugiej drużynie. Pozostałe przypadki z pełnej listy kontrolnej są sprawdzone automatycznie, a te, w których dane kończą się bez pustej linii, przeanalizuj na papierze.

### Kryterium sukcesu

- Program buduje się jako C++20 i dla głównych danych oraz wybranego błędu w drugiej drużynie wypisuje dokładnie pokazane wyniki.
- Funkcja dostaje strumień, nazwę i rekord wynikowy przez referencje i przypisuje rekord dopiero po sprawdzeniu odczytu i zasad.
- `main` kończy odczyt po pustej linii i po końcu danych w miejscu nazwy, a przy niekompletnej drużynie wypisuje `Input error`.
- `push_back` wykonuje się tylko po `true`, a przy błędzie nie ma żadnej części raportu.
- Liczba drużyn pochodzi z `size()`, a linie i suma z elementów wektora, odczytywanych przez `const` referencję.
- Tabela przypadków powstała przed uruchomieniem programu.
- Umiesz wyjaśnić, dlaczego oba sposoby zakończenia danych dają ten sam wynik.

Gdy wynik się zgadza, możesz zapisać projekt w Gicie, jak w lekcji 1.5.

<details>
<summary>Podpowiedź 1</summary>

Które zadanie należy do `main`, a które do funkcji odczytującej liczby? Kto rozpoznaje koniec całego wejścia?

</details>

<details>
<summary>Podpowiedź 2</summary>

Funkcja powinna najpierw odczytać liczby do zmiennych lokalnych. Co stanie się z rekordem wynikowym, jeśli odczyt się nie uda?

</details>

<details>
<summary>Podpowiedź 3</summary>

Dopiero po poprawnym odczycie i sprawdzeniu liczb przypisz kompletny rekord do parametru `T&`. W `main` dodaj go przez `push_back` tylko wtedy, gdy funkcja zwróci sukces.

</details>

<details>
<summary>Pełna lista przypadków kontrolnych: otwórz po przygotowaniu własnej tabeli</summary>

Kolejne linie danych oddziela `/`. Przy poprawnych danych kolumna „Wynik” podaje liczbę drużyn i sumę zwycięstw. Program wypisuje wtedy wszystkie drużyny w kolejności z danych.

| | Dane | Wynik | Co sprawdza |
|---|---|---|---|
| A | `Maple Owls` / `6 4` / `River Foxes` / `3 3` / pusta linia | 2 drużyny, suma 7 | dane z wymagań: nazwy ze spacjami, koniec przez pustą linię |
| B | `Maple Owls` / `6 4` / `River Foxes` / `3 3`, potem koniec danych | 2 drużyny, suma 7 | koniec danych po kompletnej drużynie (dane z wymagań) |
| C | `Maple Owls` / `6 4` / `River Foxes` / `3 won` | `Input error` | słowo zamiast drugiej liczby, po poprawnej drużynie (dane z wymagań) |
| D | `Maple Owls` / `6 4` / `River Foxes` / `3 4` | `Invalid teams` | więcej wygranych niż rozegranych, po poprawnej drużynie (dane z wymagań) |
| E | pusta linia | 0 drużyn, suma 0 | pusty wektor (dane z wymagań) |
| F | `Lake Herons` / `5 2`, potem koniec danych | 1 drużyna, suma 2 | jedna drużyna |
| G | `Maple Owls` / `6 4` / `River Foxes` / `3 3` / `Hill Bears` / `0 0` / `Maple Owls` / `2 0` / `Sea Gulls` / `4 1` / pusta linia | 5 drużyn, suma 8 | największa liczba drużyn, ta sama nazwa dwa razy, drużyna bez spotkań, same wygrane i same porażki |
| H | `Maple Owls` / `-1 0` | `Invalid teams` | ujemna liczba rozegranych |
| I | `Maple Owls` / `6 -1` | `Invalid teams` | ujemna liczba wygranych |
| J | `Maple Owls` / `4 5` | `Invalid teams` | więcej wygranych niż rozegranych w pierwszej drużynie |
| K | `Maple Owls` / `six 4` | `Input error` | słowo zamiast pierwszej liczby |
| L | `Maple Owls`, potem koniec danych | `Input error` | brak liczb po niepustej nazwie |
| M | `Maple Owls` / `6`, potem koniec danych | `Input error` | brak ostatniej liczby |
| N | `Maple Owls` / `6 4` / `River Foxes`, potem koniec danych | `Input error` | koniec danych po nazwie drugiej drużyny: niekompletny rekord to nie zakończenie danych |

**Testy automatyczne i Twoje próby.** Wszystkie przypadki są sprawdzone automatycznie: rozwiązanie referencyjne jest uruchamiane dla każdego z nich, a jego pełne standardowe wyjście porównywane z oczekiwanym. Rozwiązanie i jego wyniki są w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

</details>

Przykładowe rozwiązanie jest w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 8. Znajdź błąd: wynik przypisany zbyt wcześnie

To zadanie wykonaj **po misji**. Program poniżej sprawdza funkcję `read_shipment_values` dla jednej przesyłki. Przygotowuje rekord `result` z wartościami `Old Place` i 9, odczytuje nazwę, wywołuje funkcję, a potem wypisuje jej wynik i stan `result`. Funkcja ma działać tak samo jak w punkcie 2. Program możesz skopiować do `main.cpp` w katalogu `lesson_10_4`. Wpisz nazwę, a w następnej linii liczbę.

<details>
<summary>Program do sprawdzenia: otwórz po napisaniu własnego programu</summary>

<!-- example: shipment_values_early_bug -->
```cpp
#include <iostream>
#include <string>

struct Shipment {
    std::string destination;
    int boxes;
};

bool read_shipment_values(std::istream& input, const std::string& destination, Shipment& result) {
    int boxes{0};
    input >> boxes;

    if (input.fail()) {
        return false;
    }

    result = Shipment{destination, boxes};

    if (boxes < 0) {
        return false;
    }

    return true;
}

int main() {
    Shipment result{"Old Place", 9};
    std::string destination{};
    std::getline(std::cin, destination);

    const bool accepted{read_shipment_values(std::cin, destination, result)};

    if (accepted) {
        std::cout << "Returned: true\n";
    } else {
        std::cout << "Returned: false\n";
    }

    std::cout << "Result: " << result.destination << ", " << result.boxes << "\n";
}
```

Dane z dodatnią liczbą paczek:

<!-- input: shipment_values_early_bug -->
```text
North Hub
4
```

1. **Przewidź**, co ten program wypisze dla tych danych i co wypisałby z funkcją z punktu 2.
2. Uruchom program dla tych danych i porównaj wynik z przewidywaniem.
3. Dobierz własne dane, dla których funkcja z tego programu złamie swoją umowę.
4. Dla swoich danych **przewidź**, co funkcja zwróci i jakie wartości będzie miał potem `result`.
5. Uruchom program dla swoich danych.
6. Wskaż linię, w której funkcja zmienia `result` zbyt wcześnie. Dlaczego `return false;` po tej linii nie przywraca `Old Place` i 9?
7. Przenieś przypisanie za oba sprawdzenia i uruchom poprawiony program dla swoich danych.
8. Czy słowo zamiast liczby paczek ujawnia ten błąd? Dlaczego w programie z punktu 2 ten błąd nie zmieniłby żadnego wyniku?

</details>

Wyniki, przykładowe dane i poprawiony program są w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 9. Gdy coś pójdzie inaczej

| Co widzisz | Co to znaczy | Co zrobić |
|---|---|---|
| Raport ma tylko pierwszy rekord, choć wpisano kilka | Po przyjętym rekordzie brakuje `getline(rest)`. Odczyt następnej nazwy dostaje pustą resztę linii liczbowej, a pusta nazwa kończy dane. | Po `push_back` dokończ linię przez `std::getline(std::cin, rest)`, a dopiero potem odczytaj następną nazwę. |
| Raport ma puste nazwy i zera | Parametr rekordu wynikowego nie ma `&`, więc funkcja wypełnia własną kopię, a obiekt w `main` zostaje taki, jak go przygotowano (lekcja 9.1). | Przekaż rekord wynikowy przez referencję bez `const`. |
| `Invalid teams` zamiast `Input error` dla słowa w miejscu liczby | Po `false` program zawsze wypisuje ten sam komunikat, zamiast sprawdzić stan strumienia. | Po `false` sprawdź `std::cin.fail()`: `true` oznacza `Input error`. |
| Program czeka, choć wpisano wszystkie rekordy | Program czeka na następną nazwę, bo dane kończy dopiero pusta linia. Jeśli czeka zaraz po nazwie, `>>` pomija puste linie i czeka na liczbę (lekcja 10.1). | Po ostatnim rekordzie naciśnij **Enter** na pustej linii. Po nazwie wpisz jej liczby. |
| Kompilator zgłasza `call to deleted constructor of 'std::istream'` | Parametr strumienia nie ma `&`. Strumienia nie da się przekazać przez wartość, a funkcja ma pracować na istniejącym `std::cin`. | Zapisz parametr jako `std::istream&`. |
| Kompilator zgłasza `invalid operands to binary expression ('const std::istream' ...` przy `>>` | Parametr strumienia ma `const`, a odczyt zmienia strumień. | Usuń `const` z parametru strumienia. |
| Funkcja zwraca `false`, a rekord wynikowy ma nowe wartości | Funkcja przypisuje rekord przed sprawdzeniem zasad (punkt 8). | Przypisz rekord dopiero po wszystkich sprawdzeniach. |

## 10. Wyjaśnij

Odpowiedz własnymi słowami, najlepiej na piśmie. Dopiero potem porównaj z przykładowymi odpowiedziami.

1. Co dostaje funkcja przez parametr `std::istream& input`, gdy `main` przekazuje `std::cin`? Czy funkcja otwiera nowe wejście?
2. Dlaczego rekord wynikowy trafia do funkcji przez referencję bez `const`, zamiast być zwracany przez wartość, jak w lekcji 8.5?
3. Co oznacza `true`, a co `false` funkcji `read_shipment_values`? Jaki jest stan `result` po `false`?
4. Dlaczego funkcja odczytuje liczbę do zmiennej lokalnej i przypisuje cały rekord dopiero na końcu?
5. Dlaczego nazwę odczytuje i zakończenie danych rozpoznaje `main`, a nie funkcja?
6. Co program robi, gdy pierwsza linia jest pusta? Dlaczego to nie jest błąd?
7. Dane kończą się zaraz po nazwie drugiej przesyłki. Dlaczego wynik to `Input error`, a nie raport z jedną przesyłką?
8. Dane kończą się zaraz po ostatniej liczbie, bez końca linii. Dlaczego `getline(rest)` się nie udaje i dlaczego mimo to program wypisuje raport?
9. Funkcja zwróciła `false`. Skąd `main` wie, czy wypisać `Input error`, czy `Invalid shipments`?
10. Pierwsza drużyna jest poprawna, a druga ma `3 4`. Co jest w wektorze, a co wypisuje program? Dlaczego `push_back` stoi w `main`, a nie w funkcji?

<details>
<summary>Przykładowe odpowiedzi</summary>

1. Dostaje inną nazwę istniejącego obiektu `std::cin`, czyli strumienia wejścia typu `std::istream`. Nie otwiera nowego wejścia: `input >> boxes` czyta dalej te same dane, od miejsca, w którym skończył `main`.
2. Bo funkcja ma do przekazania dwie rzeczy: czy odczyt się udał i kompletny rekord. `bool` mówi o powodzeniu, a rekord trafia do obiektu, który przygotował wywołujący. Zwracanie nowego rekordu przez wartość (lekcja 8.5) jest dobre, gdy wynik jest jeden.
3. `true`: liczba została odczytana i sprawdzona, a `result` zawiera kompletny, poprawny rekord. `false`: nowego rekordu nie ma, a `result` jest dokładnie taki jak przed wywołaniem.
4. Bo w trakcie odczytu nie wiadomo jeszcze, czy rekord będzie poprawny. Gdyby funkcja zmieniała `result` przed sprawdzeniami, po odmowie zostałby w nim niedozwolony rekord, a `return false;` tego nie cofa.
5. Bo to przy nazwie rozstrzyga się, czy dane się skończyły. Gdyby funkcja czytała też nazwę, jej `bool` musiałby wyrazić trzy sytuacje: rekord, zakończenie danych i błąd. Gdy zakończenie rozpoznaje `main`, `true` i `false` mają po jednym znaczeniu.
6. Odczyt nazwy się udaje, ale nazwa jest pusta, więc pętla nie wykonuje się ani razu, a program wypisuje raport z zerem przesyłek. Pusta linia w miejscu nazwy to umówione zakończenie danych, a pusty wektor to poprawny wynik.
7. Bo rekord już się zaczął: nazwa jest niepusta, ale brakuje jego liczby. Odczyt w funkcji się nie udaje, więc to niekompletny rekord, a nie zakończenie danych. Raport z jedną przesyłką sugerowałby, że dane były kompletne.
8. `>>` odczytało 7 i doszło do końca danych, więc `getline(rest)` nie ma już czego odczytać. Liczba ostatniego rekordu jest jednak odczytana i sprawdzona, a rekord jest w wektorze. Nieudane `getline(rest)` oznacza tylko, że nie ma następnej nazwy, więc pętla kończy się normalnie.
9. Sprawdza `std::cin.fail()`. Funkcja nie przywraca strumienia przez `clear()`, więc po nieudanym odczycie `fail()` nadal daje `true`, a po odczytanej, ale niedozwolonej liczbie daje `false`.
10. W wektorze jest pierwsza drużyna, bo została dodana, zanim program odczytał drugą. Program wypisuje tylko `Invalid teams`, bez raportu. `push_back` stoi w `main`, bo `main` buduje wektor i decyduje o jego zawartości, a funkcja tylko przygotowuje jeden rekord.

</details>

## Podsumowanie

- Gdy liczba rekordów nie jest zapowiedziana, program czyta je do pustej linii albo do końca danych w miejscu nazwy. Pusty wektor to poprawny wynik.
- `main` czyta nazwy, rozpoznaje zakończenie danych, dodaje rekordy przez `push_back` i wypisuje raport.
- Funkcja dostaje strumień przez `std::istream&`, nazwę przez `const std::string&` i rekord wynikowy przez `T&`. Przypisuje cały rekord dopiero po sprawdzeniu odczytu i zasad, więc po `false` rekord jest bez zmian.
- Po odmowie `std::cin.fail()` odróżnia nieudany odczyt od niedozwolonej wartości.
- Koniec danych po niepustej nazwie to `Input error`, a koniec danych zaraz po ostatniej poprawnej liczbie nie jest błędem.
- Po przyjętym rekordzie program dokańcza jego linię liczbową i tylko wtedy odczytuje następną nazwę.

## Co dalej

W lekcji 10.5, sprawdzianie Modułu 10, samodzielnie połączysz to, czego nauczył Cię ten moduł. Lekcja 10.5 jest w przygotowaniu.

---

## Przykładowe rozwiązania

Zajrzyj tutaj **po własnej próbie**. Twoje nazwy mogą się różnić, jeśli standardowe wyjście jest takie, jak wymagane.

<details>
<summary>Punkt 7: misja, wyniki drużyn</summary>

<!-- example: teams -->
```cpp
#include <iostream>
#include <string>
#include <vector>

struct Team {
    std::string name;
    int played;
    int won;
};

bool read_team_values(std::istream& input, const std::string& name, Team& result) {
    int played{0};
    int won{0};
    input >> played;
    input >> won;

    if (input.fail()) {
        return false;
    }

    if (played < 0 || won < 0 || won > played) {
        return false;
    }

    result = Team{name, played, won};
    return true;
}

int main() {
    std::vector<Team> teams{};
    std::string name{};
    std::getline(std::cin, name);

    while (!std::cin.fail() && !name.empty()) {
        Team team{"", 0, 0};
        const bool accepted{read_team_values(std::cin, name, team)};

        if (!accepted) {
            if (std::cin.fail()) {
                std::cout << "Input error\n";
            } else {
                std::cout << "Invalid teams\n";
            }

            return 0;
        }

        teams.push_back(team);

        std::string rest{};
        std::getline(std::cin, rest);

        if (!std::cin.fail()) {
            std::getline(std::cin, name);
        }
    }

    int wins_total{0};
    std::cout << "Teams: " << teams.size() << "\n";

    for (const Team& team : teams) {
        std::cout << team.name << ": played " << team.played << ", won " << team.won << "\n";
        wins_total += team.won;
    }

    std::cout << "Wins total: " << wins_total << "\n";
}
```

1. **`main` czyta nazwę,** bo to przy nazwie rozstrzyga się, czy dane się skończyły. Funkcja dostaje już odczytaną nazwę.
2. **`main` rozpoznaje zakończenie danych:** pustą linię i nieudany odczyt nazwy. Funkcja jest wywoływana dopiero wtedy, gdy rekord się zaczął.
3. **`std::istream&`,** bo funkcja ma czytać z istniejącego strumienia `std::cin`, od miejsca, w którym skończył `main`. Bez `const`, bo odczyt zmienia strumień.
4. **`Team&` jako parametr wynikowy,** bo funkcja ma dwa wyniki: `bool` mówi o powodzeniu, a rekord trafia do obiektu wywołującego.
5. **Rekord wynikowy bez zmian przy `false`:** każda odmowa to `return false;` przed przypisaniem, więc wywołujący dostaje swój rekord w niezmienionym stanie (lekcja 9.2).
6. **Zmienne lokalne `played` i `won`,** bo w trakcie odczytu nie wiadomo jeszcze, czy powstanie poprawny rekord. Pola `result` czekają na koniec sprawdzeń.
7. **Odczyt przed wartościami:** po nieudanym odczycie na zawartości zmiennej nie wolno polegać (lekcja 4.6), więc zasady mają sens tylko dla naprawdę odczytanych liczb.
8. **Przypisanie po wszystkich sprawdzeniach,** jednym `result = Team{name, played, won};`, więc rekord zmienia się naraz i tylko wtedy, gdy jest kompletny i poprawny.
9. **`push_back` w `main`,** bo to `main` buduje wektor, a funkcja odpowiada za jeden rekord. `main` dodaje rekord tylko po `true`.
10. **Liczba rekordów nie jest potrzebna,** bo pętla powtarza przebiegi, dopóki w miejscu nazwy jest niepusta, poprawnie odczytana linia.
11. **Pusta linia kończy odczyt,** bo to udany odczyt tekstu o długości zero (lekcja 7.4), a w umowie danych nazwa drużyny nie jest pusta.
12. **Koniec danych przed następną nazwą kończy odczyt,** bo wszystkie wcześniejsze rekordy są kompletne, a nowy się nie zaczął.
13. **Koniec danych wewnątrz rekordu to błąd:** po niepustej nazwie rekord się zaczął, więc brak liczby to nieudany odczyt i `Input error`.
14. **Ostatnia liczba może skończyć się na końcu danych:** `>>` odczytuje ją poprawnie, choć strumień doszedł do końca (lekcja 4.6). Nie udaje się dopiero `getline(rest)`.
15. **Ostatni rekord zostaje przyjęty,** bo jego liczby są odczytane i sprawdzone. Nieudane `getline(rest)` oznacza tylko, że nie ma już następnej nazwy, więc `main` jej nie odczytuje i kończy pętlę.
16. **`false` i `fail()` to dwie informacje:** `false` mówi, że nowego rekordu nie ma, a `std::cin.fail()` po `false` mówi, czy przyczyną był nieudany odczyt. Działa to, bo funkcja nie wywołuje `clear()`.
17. **Wcześniejsze drużyny mogą zostać w wektorze** po błędzie w późniejszej. Program ich nie usuwa, bo zaraz kończy pracę.
18. **Mimo to bez częściowego raportu,** bo wynik dotyczy wszystkich danych. Raport z części drużyn wyglądałby jak kompletny.
19. **Bez nowego typu wyniku,** bo `main` sam rozpoznaje zakończenie danych. Funkcji wystarczą dwie wartości `bool`, a przyczynę odmowy podaje stan strumienia.
20. **Bez pełnego sprawdzania linii,** bo umowa danych mówi, gdzie stoją nazwy i liczby. `getline(rest)` dokańcza linię liczbową, ale tekstu po liczbach nie sprawdza (lekcja 10.2).

**Inne poprawne rozwiązania:** zamiast `return 0;` można użyć flagi `bool`, jak w lekcji 7.4. Pętla może też zaczynać każdy przebieg od odczytu nazwy, jak w lekcji 7.4: gdy `getline(rest)` się nie uda, następny odczyt nazwy też się nie uda (lekcja 4.6), więc pętla skończy się tak samo. Funkcja może przypisać pola `result` po kolei zamiast całego rekordu, jeśli robi to dopiero po wszystkich sprawdzeniach. Wynik funkcji można też sprawdzić bezpośrednio w warunku `if`, bez zmiennej `accepted`.

Każdy przypadek z listy kontrolnej to osobne uruchomienie tego programu. Przypadki A–E to dane z treści misji. Pozostałe są poniżej, w kolejności z listy kontrolnej.

<!-- input: teams -->
```text
Lake Herons
5 2
```

<!-- output: teams -->
```text
Teams: 1
Lake Herons: played 5, won 2
Wins total: 2
```

<!-- input: teams -->
```text
Maple Owls
6 4
River Foxes
3 3
Hill Bears
0 0
Maple Owls
2 0
Sea Gulls
4 1

```

<!-- output: teams -->
```text
Teams: 5
Maple Owls: played 6, won 4
River Foxes: played 3, won 3
Hill Bears: played 0, won 0
Maple Owls: played 2, won 0
Sea Gulls: played 4, won 1
Wins total: 8
```

<!-- input: teams -->
```text
Maple Owls
-1 0
```

<!-- output: teams -->
```text
Invalid teams
```

<!-- input: teams -->
```text
Maple Owls
6 -1
```

<!-- output: teams -->
```text
Invalid teams
```

<!-- input: teams -->
```text
Maple Owls
4 5
```

<!-- output: teams -->
```text
Invalid teams
```

<!-- input: teams -->
```text
Maple Owls
six 4
```

<!-- output: teams -->
```text
Input error
```

<!-- input: teams -->
```text
Maple Owls
```

<!-- output: teams -->
```text
Input error
```

<!-- input: teams -->
```text
Maple Owls
6
```

<!-- output: teams -->
```text
Input error
```

<!-- input: teams -->
```text
Maple Owls
6 4
River Foxes
```

<!-- output: teams -->
```text
Input error
```

**Program kontrolny** sprawdza umowę funkcji przy odmowie, której w raporcie misji nie widać, bo po `false` program kończy pracę. Typ i funkcja są takie same jak wyżej. `main` przygotowuje rekord `Old Team` z liczbami 1 i 0, odczytuje jedną nazwę, wywołuje funkcję i wypisuje jej wynik oraz stan rekordu. To narzędzie, a nie dodatkowe zadanie: uruchamianie go jest nieobowiązkowe. Możesz w nim podmienić typ i funkcję na własne, jeśli zmienisz też nazwy w `main`.

<!-- example: team_values_check -->
```cpp
#include <iostream>
#include <string>

struct Team {
    std::string name;
    int played;
    int won;
};

bool read_team_values(std::istream& input, const std::string& name, Team& result) {
    int played{0};
    int won{0};
    input >> played;
    input >> won;

    if (input.fail()) {
        return false;
    }

    if (played < 0 || won < 0 || won > played) {
        return false;
    }

    result = Team{name, played, won};
    return true;
}

int main() {
    Team result{"Old Team", 1, 0};
    std::string name{};
    std::getline(std::cin, name);

    const bool accepted{read_team_values(std::cin, name, result)};

    if (accepted) {
        std::cout << "Returned: true\n";
    } else {
        std::cout << "Returned: false\n";
    }

    std::cout << "Result: " << result.name << ", played " << result.played << ", won " << result.won << "\n";
}
```

Poprawne liczby, także zera, zmieniają rekord:

<!-- input: team_values_check -->
```text
River Foxes
3 3
```

<!-- output: team_values_check -->
```text
Returned: true
Result: River Foxes, played 3, won 3
```

<!-- input: team_values_check -->
```text
River Foxes
0 0
```

<!-- output: team_values_check -->
```text
Returned: true
Result: River Foxes, played 0, won 0
```

Po odmowie rekord zostaje bez zmian. Dla `3 won` pierwsza liczba została odczytana, a mimo to rekord się nie zmienia:

<!-- input: team_values_check -->
```text
River Foxes
3 won
```

<!-- output: team_values_check -->
```text
Returned: false
Result: Old Team, played 1, won 0
```

<!-- input: team_values_check -->
```text
River Foxes
3 4
```

<!-- output: team_values_check -->
```text
Returned: false
Result: Old Team, played 1, won 0
```

<!-- input: team_values_check -->
```text
River Foxes
-1 0
```

<!-- output: team_values_check -->
```text
Returned: false
Result: Old Team, played 1, won 0
```

<!-- input: team_values_check -->
```text
River Foxes
```

<!-- output: team_values_check -->
```text
Returned: false
Result: Old Team, played 1, won 0
```

</details>

<details>
<summary>Punkt 8: wyniki przed poprawką i poprawiony program</summary>

Przed poprawką, dla danych z dodatnią liczbą paczek:

<!-- output: shipment_values_early_bug -->
```text
Returned: true
Result: North Hub, 4
```

- **Ten przypadek maskuje błąd.** Funkcja z punktu 2 wypisałaby to samo: liczba jest odczytana i dozwolona, więc obie wersje przypisują ten sam rekord i zwracają `true`.
- **Dane, które ujawniają błąd:** dowolna ujemna liczba paczek, na przykład `-2`. Odczyt się udaje, a zasady powinny ją odrzucić. Poprawny wynik to `Returned: false` i `Result: Old Place, 9`, a program z błędem wypisuje:

<!-- input: shipment_values_early_bug -->
```text
North Hub
-2
```

<!-- output: shipment_values_early_bug -->
```text
Returned: false
Result: North Hub, -2
```

- **Gdzie jest błąd:** `result = Shipment{destination, boxes};` stoi między sprawdzeniem odczytu a sprawdzeniem zasad. Dla `-2` przypisanie wykonuje się, zanim funkcja wie, że liczba jest niedozwolona.
- **Dlaczego `return false;` nie przywraca `Old Place` i 9:** `return` kończy wywołanie, ale nie cofa wcześniejszych zmian (lekcja 9.2). Dawnych wartości nikt nie zapamiętał, a `result` to inna nazwa obiektu z `main`, więc zmiana już w nim jest. Funkcja zwraca `false`, a rekord zawiera niedozwoloną przesyłkę.
- **Słowo zamiast liczby nie ujawnia błędu:** funkcja sprawdza odczyt przed przypisaniem, więc dla `seven` zwraca `false` i niczego nie zmienia. Błąd ujawnia tylko liczba, którą udaje się odczytać, ale która łamie zasady:

<!-- input: shipment_values_early_bug -->
```text
North Hub
seven
```

<!-- output: shipment_values_early_bug -->
```text
Returned: false
Result: Old Place, 9
```

- **W programie z punktu 2 ten błąd nie zmieniłby żadnego wyniku:** po `false` program wypisuje komunikat i kończy pracę, więc zmienionego rekordu nikt nie odczyta. Funkcja łamałaby jednak swoją umowę, a program, który po odmowie dalej korzysta z rekordu, dostałby niedozwolone dane.
- **Poprawka:** przenieś przypisanie za oba sprawdzenia. Poprawiona funkcja to funkcja z punktu 2:

<!-- example: shipment_values_early_fixed -->
```cpp
#include <iostream>
#include <string>

struct Shipment {
    std::string destination;
    int boxes;
};

bool read_shipment_values(std::istream& input, const std::string& destination, Shipment& result) {
    int boxes{0};
    input >> boxes;

    if (input.fail()) {
        return false;
    }

    if (boxes < 0) {
        return false;
    }

    result = Shipment{destination, boxes};
    return true;
}

int main() {
    Shipment result{"Old Place", 9};
    std::string destination{};
    std::getline(std::cin, destination);

    const bool accepted{read_shipment_values(std::cin, destination, result)};

    if (accepted) {
        std::cout << "Returned: true\n";
    } else {
        std::cout << "Returned: false\n";
    }

    std::cout << "Result: " << result.destination << ", " << result.boxes << "\n";
}
```

<!-- input: shipment_values_early_fixed -->
```text
North Hub
-2
```

<!-- output: shipment_values_early_fixed -->
```text
Returned: false
Result: Old Place, 9
```

Dla danych z dodatnią liczbą paczek i dla słowa poprawiony program wypisuje to samo co program z błędem:

<!-- input: shipment_values_early_fixed -->
```text
North Hub
4
```

<!-- output: shipment_values_early_fixed -->
```text
Returned: true
Result: North Hub, 4
```

<!-- input: shipment_values_early_fixed -->
```text
North Hub
seven
```

<!-- output: shipment_values_early_fixed -->
```text
Returned: false
Result: Old Place, 9
```

</details>

**Poprzednia lekcja:** [Lekcja 10.3: Budowanie wektora rekordów z danych wejściowych](lesson_03_building_a_vector_of_records.md) · **Następna lekcja:** w przygotowaniu · [Opis kursu](../../README.md)

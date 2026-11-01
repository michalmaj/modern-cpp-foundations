# Lekcja 10.3: Budowanie wektora rekordów z danych wejściowych

**Polski** · [English](lesson_03_building_a_vector_of_records.en.md) · [Opis kursu](../../README.md)

> **Moduł 10, lekcja 3** · około 80–100 minut, można ją podzielić na dwa podejścia
> **Potrzebujesz:** katalogu `cpp-workspace` i oryginalnego projektu `lesson_05_first_program`, jak dotąd. Debugger nie jest w tej lekcji potrzebny.
> **Wersja pilotażowa.** Programy z tej lekcji sprawdzamy automatycznie na Windowsie, Ubuntu i macOS, także z podanymi danymi wejściowymi. Wpisywanie danych w oknie **Run** CLiona opisujemy bez ręcznego sprawdzenia na każdym systemie.

## Zanim zaczniesz

Ta lekcja zakłada, że:

- dodajesz elementy do pustego wektora przez `push_back`, tylko po udanym odczycie, i wiesz, że `size()` rośnie o 1 przy każdym dodaniu (lekcja 6.2);
- przeglądasz wektor rekordów pętlą `for (const Product& product : products)` (lekcja 8.4) i zmieniasz jego elementy pętlą `for (Product& product : products)` (lekcja 9.3);
- wiesz, że kopia rekordu jest od niego niezależna (lekcja 8.2);
- wiesz, że wykonany `return` kończy całe wywołanie funkcji, także w pętli (lekcje 5.4 i 9.4), a `return 0;` kończy `main` (lekcja 1.3);
- odczytujesz pola do zmiennych lokalnych, sprawdzasz odczyt i zasady, a dopiero potem tworzysz rekord (lekcja 10.1);
- odczytujesz nazwę przez `std::getline`, liczby przez `>>` i dokańczasz linię liczbową przez `std::getline(std::cin, rest)` (lekcja 10.2).

## Sytuacja

W lekcji 10.2 program odczytywał dokładnie dwie przesyłki, każdą do osobnych zmiennych. Pięć przesyłek wymagałoby pięciu kompletów zmiennych, a gdy liczbę przesyłek podają dopiero dane, takiego programu nie da się napisać.

Teraz pierwsza linia danych mówi, ile rekordów nastąpi. Program odczytuje tę liczbę, potem w pętli odczytuje i sprawdza kolejne rekordy, a każdy zaakceptowany dodaje do wektora przez `push_back`. Wszystkie te elementy już znasz. Nowe jest ich połączenie w jednym programie: odczyt z wejścia, własny typ i kolekcja.

Główna zasada tej lekcji: **najpierw powstaje poprawny, kompletny rekord, a dopiero potem trafia do wektora.**

Po tej lekcji będziesz:

- odczytywać liczbę rekordów, sprawdzać jej zakres i odczytywać w pętli dokładnie tyle rekordów, ile zapowiadają dane;
- dokańczać poprzednią linię liczbową na początku każdego przebiegu;
- dodawać przez `push_back` tylko kompletne, sprawdzone rekordy;
- kończyć odczyt przy pierwszym błędzie, bez częściowego raportu;
- odróżniać dodanie nowego elementu od zmiany istniejącego;
- dobierać dane, które ujawniają zbyt wczesne dodanie rekordu.

## 1. Przygotuj projekt

W `cpp-workspace` utwórz katalog `lesson_10_3` i skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program`. Program z punktu 2 wpisujesz w `main.cpp` tego katalogu.

Programy z tej lekcji nie wypisują pytań. Wpisuj dane linia po linii, jak w lekcji 10.2. Program kończy pracę sam po odczytaniu zapowiedzianej liczby rekordów.

## 2. Lista przesyłek

Program odczytuje listę przesyłek. Pierwsza linia podaje liczbę przesyłek, od 0 do 5. Potem każda przesyłka zajmuje dwie linie, jak w lekcji 10.2: pełną nazwę miejsca docelowego i liczbę paczek. Nazwa nie może być pusta, a liczba paczek musi być nieujemna.

<!-- example: shipment_list -->
```cpp
#include <iostream>
#include <string>
#include <vector>

struct Shipment {
    std::string destination;
    int boxes;
};

int main() {
    std::vector<Shipment> shipments{};
    int count{0};
    std::cin >> count;

    if (std::cin.fail()) {
        std::cout << "Input error\n";
        return 0;
    }

    if (count < 0 || count > 5) {
        std::cout << "Invalid shipments\n";
        return 0;
    }

    for (int index{0}; index < count; ++index) {
        std::string rest{};
        std::getline(std::cin, rest);

        std::string destination{};
        int boxes{0};
        std::getline(std::cin, destination);
        std::cin >> boxes;

        if (std::cin.fail()) {
            std::cout << "Input error\n";
            return 0;
        }

        if (destination.empty() || boxes < 0) {
            std::cout << "Invalid shipments\n";
            return 0;
        }

        const Shipment shipment{destination, boxes};
        shipments.push_back(shipment);
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

Uruchom program i wpisz:

<!-- input: shipment_list -->
```text
2
North Hub
4
South Depot
7
```

<!-- output: shipment_list -->
```text
Shipments: 2
North Hub: 4
South Depot: 7
Total boxes: 11
```

| Zapis | Co robi |
|---|---|
| `std::vector<Shipment> shipments{};` | tworzy pusty wektor przesyłek, bez `const`, bo program będzie do niego dodawać |
| `std::cin >> count;` | odczytuje liczbę przesyłek |
| `return 0;` | od razu kończy `main`, po wypisaniu komunikatu (punkt 3) |
| `for (int index{0}; index < count; ++index)` | wykonuje jeden przebieg na każdą zapowiedzianą przesyłkę |
| `std::getline(std::cin, rest);` | dokańcza poprzednią linię liczbową (punkt 4) |
| `const Shipment shipment{destination, boxes};` | tworzy kompletny rekord z odczytanych i sprawdzonych danych |
| `shipments.push_back(shipment);` | dodaje ten rekord na koniec wektora |
| `shipments.size()` | podaje, ile rekordów naprawdę jest w wektorze |

- **Każdy przebieg ma własne zmienne lokalne** `rest`, `destination` i `boxes`, z wartościami początkowymi, jak zmienna `measurement` w lekcji 6.2.
- **Raport powstaje z wektora:** liczba przesyłek pochodzi z `size()`, a linie i suma z pól jego elementów.

## 3. Liczba rekordów na początku

Liczbę przesyłek program sprawdza jak każdą odczytaną wartość: najpierw `std::cin.fail()`, potem zasady. `two` daje `Input error`, a `-1` albo `6` to poprawnie odczytane, ale niedozwolone wartości, więc dają `Invalid shipments`. W obu przypadkach program nie odczytuje żadnej przesyłki.

Każde sprawdzenie, które wykrywa błąd, wypisuje komunikat i wykonuje `return 0;`. `main` też jest funkcją, a wykonany `return` kończy całe jej wywołanie (lekcja 5.4), więc dalsze linie `main` się nie wykonują. Kod zakończenia 0 mówi tylko, że program zakończył się normalnie, a o wyniku mówi komunikat.

`count` i licznik pętli mają typ `int`, bo zakres jest mały i sprawdzony przed pętlą. `count` to jednak tylko **zapowiedź** z danych, a `shipments.size()` to liczba rekordów, które naprawdę trafiły do wektora. Przy poprawnych danych są równe, ale raport opisuje wektor, więc korzysta z `size()`.

## 4. Pętla i dokańczanie poprzedniej linii

Każdy przebieg zaczyna od dokończenia poprzedniej linii, a dopiero potem odczytuje nazwę i liczbę:

<!-- fragment -->
```cpp
for (int index{0}; index < count; ++index) {
    std::string rest{};
    std::getline(std::cin, rest);

    // Check the read.
    // Read the name and the fields of the current record.
    // Check the record, create it and add it.
}
```

Prześledź główne dane:

| Przebieg | `getline(rest)` dokańcza | `destination` | `boxes` | `size()` po przebiegu |
|---|---|---|---|---|
| 1 | linię z liczbą przesyłek `2` | `North Hub` | 4 | 1 |
| 2 | linię z liczbą paczek `4` | `South Depot` | 7 | 2 |

- **W pierwszym przebiegu** poprzednia linia to linia z liczbą przesyłek: po `>> count` w wejściu został jej koniec (lekcja 10.2).
- **W każdym następnym** to linia liczbowa poprzedniej przesyłki.
- **Po ostatniej przesyłce** nie ma już przebiegu, więc linia z `7` zostaje niedokończona, jak ostatnia linia w lekcji 10.2. Dodatkowe `getline` po pętli zamieniłoby w `Input error` poprawne dane, które kończą się zaraz po `7`, bez końca linii. Testy automatyczne kursu tego przypadku nie uruchamiają, bo w nich każda linia ma swój koniec.

Dokańczanie na początku przebiegu obejmuje więc linię z liczbą rekordów i nigdy nie wykonuje się po ostatniej liczbie. `rest` nadal niczego nie sprawdza (lekcja 10.2).

W programie z punktu 2 odczyt `getline(rest)` jest sprawdzany przez ten sam `if` co odczyty nazwy i liczby, po wszystkich odczytach przebiegu: gdy jeden odczyt się nie uda, kolejne też się nie udają (lekcja 4.6).

## 5. Najpierw kompletny rekord, potem `push_back`

Każdy przebieg wykonuje te same kroki, w tej kolejności:

1. odczytaj pola do zmiennych lokalnych;
2. sprawdź `std::cin.fail()`;
3. sprawdź zasady wartości;
4. utwórz kompletny rekord przez `{}`;
5. dodaj go przez `push_back`;
6. przejdź do następnego przebiegu.

<!-- fragment -->
```cpp
const Shipment shipment{destination, boxes};
shipments.push_back(shipment);
```

- `shipment` to kompletny rekord: oba pola mają odczytane i sprawdzone wartości.
- `push_back` działa jak w lekcji 6.2, tylko dodaje rekord: na koniec `shipments` trafia **nowy element** z tymi samymi wartościami pól. Liczba elementów rośnie o jeden, a kolejność elementów to kolejność z danych.
- **Wektor przechowuje własny element.** To kopia rekordu `shipment`, niezależna od niego jak kopia z lekcji 8.2, a nie druga nazwa tego samego obiektu. Na końcu przebiegu lokalny `shipment` znika, a element w wektorze zostaje. Późniejsza zmiana `destination` albo `boxes` niczego w wektorze nie zmienia.
- **`push_back` niczego nie sprawdza.** Pusta nazwa albo `-2` paczki to dla wektora zwykłe wartości pól. O tym, co trafi do wektora, decyduje program: wywołuje `push_back` dopiero po wszystkich sprawdzeniach.

## 6. Pusta lista i błąd w późniejszym rekordzie

**Przewidź** wynik dla danych z samym `0`. Uruchomienie jest nieobowiązkowe.

<!-- input: shipment_list -->
```text
0
```

<details>
<summary>Standardowe wyjście dla 0 przesyłek</summary>

<!-- output: shipment_list -->
```text
Shipments: 0
Total boxes: 0
```

</details>

Pętla nie wykonuje się ani razu, więc program nie odczytuje żadnej nazwy ani liczby i nie wywołuje `getline(rest)`. Pusty wektor to poprawny wynik: raport podaje 0 przesyłek i sumę 0, bez zastępczego rekordu. Ten sam wynik daje `0` bez końca linii, ale tego przypadku testy automatyczne nie uruchamiają.

**Przewidź** też wynik, gdy pierwsza przesyłka jest poprawna, a druga ma `-2` paczki:

<!-- input: shipment_list -->
```text
2
North Hub
4
South Depot
-2
```

<details>
<summary>Standardowe wyjście, gdy druga przesyłka ma -2 paczki</summary>

<!-- output: shipment_list -->
```text
Invalid shipments
```

</details>

Gdy program odczytuje drugą przesyłkę, pierwsza jest już w wektorze. Program jej nie usuwa, ale też jej nie pokazuje: wypisuje tylko `Invalid shipments` i kończy pracę. Wynik to albo pełny raport wszystkich zapowiedzianych przesyłek, albo jeden komunikat, nigdy część wektora.

| Sytuacja | Przykład | Wynik |
|---|---|---|
| nieudany odczyt | `two` zamiast liczby przesyłek, `seven` zamiast liczby paczek drugiej przesyłki, zapowiedziane 3 przesyłki, a w danych tylko 2 | `Input error` |
| udany odczyt, wartość niedozwolona | liczba przesyłek `-1` albo `6`, pusta nazwa drugiej przesyłki, `-2` paczki | `Invalid shipments` |
| udany odczyt, wartości dozwolone | 0, 1 albo 5 przesyłek | raport |

<details>
<summary>Pozostałe dane z tabeli i ich wyniki</summary>

<!-- input: shipment_list -->
```text
two
```

<!-- output: shipment_list -->
```text
Input error
```

<!-- input: shipment_list -->
```text
2
North Hub
4
South Depot
seven
```

<!-- output: shipment_list -->
```text
Input error
```

<!-- input: shipment_list -->
```text
3
North Hub
4
South Depot
7
```

<!-- output: shipment_list -->
```text
Input error
```

<!-- input: shipment_list -->
```text
-1
```

<!-- output: shipment_list -->
```text
Invalid shipments
```

<!-- input: shipment_list -->
```text
6
```

<!-- output: shipment_list -->
```text
Invalid shipments
```

<!-- input: shipment_list -->
```text
2
North Hub
4

7
```

<!-- output: shipment_list -->
```text
Invalid shipments
```

<!-- input: shipment_list -->
```text
1
East Gate
3
```

<!-- output: shipment_list -->
```text
Shipments: 1
East Gate: 3
Total boxes: 3
```

<!-- input: shipment_list -->
```text
5
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

<!-- output: shipment_list -->
```text
Shipments: 5
Central Hub: 2
North Hub: 4
River Port: 0
South Depot: 7
West End Depot: 1
Total boxes: 14
```

</details>

## 7. Dodawanie a zmiana

| Operacja | Znaczenie |
|---|---|
| `shipments.push_back(shipment)` | dodaje nowy element na koniec, a `size()` rośnie o 1 (lekcja 6.2) |
| `for (Shipment& shipment : shipments)` i zmiana pola | zmienia istniejące elementy, a `size()` się nie zmienia (lekcja 9.3) |
| `for (const Shipment& shipment : shipments)` | tylko odczytuje istniejące elementy (lekcja 8.4) |

`push_back` nigdy nie aktualizuje istniejącego elementu: każde wywołanie dodaje nowy. Raport w punkcie 2 tylko odczytuje elementy, więc jego pętla używa `const Shipment&`. W tej lekcji programy nie zmieniają elementów po odczycie.

## 8. Misja: zlecenia w pracowni

Pracownia przyjmuje kilka zleceń. Program odczytuje ich listę, sprawdza każde zlecenie i wypisuje wszystkie zlecenia oraz sumę pracy, która została.

**Dane wejściowe:** pierwsza linia podaje liczbę zleceń. Potem każde zlecenie zajmuje dwie linie:

1. nazwa klienta, która może zawierać spacje;
2. dwie liczby oddzielone spacją: zaplanowane jednostki pracy i ukończone jednostki pracy.

**Reguły:**

- Zleceń jest od 0 do 5.
- Nazwa klienta nie może być pusta. W danych zgodnych z umową nie ma spacji na jej początku ani końcu, a program ich nie sprawdza. Ten sam klient może mieć kilka zleceń.
- Zaplanowanych jednostek musi być więcej niż zero.
- Liczba ukończonych jednostek musi być nieujemna i nie może przekraczać liczby zaplanowanych.
- Wszystkie liczby są niewielkie i mieszczą się w `int`, ich suma też.
- Tekst po liczbach jest poza umową i program go nie sprawdza.

**Wymagania:**

- Program definiuje własny typ zlecenia z trzema polami: nazwą klienta (`std::string`), liczbą zaplanowanych jednostek (`int`) i liczbą ukończonych jednostek (`int`). Nazwy typu, pól i wektora wybierasz samodzielnie.
- Zlecenia trafiają do początkowo pustego wektora przez `push_back`, dopiero po sprawdzeniu odczytu i zasad. Odczyt jest w `main`, bez pytań.
- Gdy nie uda się odczytać wymaganych danych, program wypisuje dokładnie `Input error`.
- Gdy odczyt się udał, ale liczba zleceń albo wartości któregoś zlecenia łamią zasady, program wypisuje dokładnie `Invalid orders`.
- Przy pierwszym błędzie program wypisuje komunikat i kończy pracę, bez żadnej części raportu.
- Gdy wszystko się zgadza, program wypisuje liczbę zleceń z `size()`, każde zlecenie w kolejności z danych i sumę pozostałych jednostek, jak w przykładzie niżej. Wszystkie te informacje pochodzą z elementów wektora.

W `cpp-workspace` utwórz katalog `workshop_orders`, skopiuj do niego `CMakeLists.txt` z oryginalnego `lesson_05_first_program`, utwórz pusty `main.cpp` i napisz program samodzielnie.

Dla danych:

<!-- input: orders -->
```text
3
North Library
12 5
City Archive
8 8
Green Workshop
6 0
```

standardowe wyjście ma być takie:

<!-- output: orders -->
```text
Orders: 3
North Library: planned 12, completed 5, remaining 7
City Archive: planned 8, completed 8, remaining 0
Green Workshop: planned 6, completed 0, remaining 6
Remaining total: 13
```

Gdy zleceń jest zero:

<!-- input: orders -->
```text
0
```

<!-- output: orders -->
```text
Orders: 0
Remaining total: 0
```

Drugie zlecenie ma więcej ukończonych jednostek niż zaplanowanych. Pierwsze mogło już trafić do wektora, ale raportu nie ma:

<!-- input: orders -->
```text
2
North Library
12 5
City Archive
8 9
```

<!-- output: orders -->
```text
Invalid orders
```

Zamiast liczby ukończonych jednostek drugiego zlecenia jest słowo:

<!-- input: orders -->
```text
2
North Library
12 5
City Archive
8 done
```

<!-- output: orders -->
```text
Input error
```

Liczba zleceń jest ujemna:

<!-- input: orders -->
```text
-1
```

<!-- output: orders -->
```text
Invalid orders
```

Słowo zamiast liczby zleceń, na przykład `three`, daje `Input error`.

**To nie są przesyłki z inną nazwą.** Linia liczbowa ma dwie liczby, a jedna z zasad łączy obie. Musisz samodzielnie zdecydować:

1. jak nazwać typ, jego pola i wektor oraz jakich zmiennych lokalnych potrzebujesz do odczytu jednego zlecenia;
2. jak zapisać licznik i warunek pętli;
3. w którym miejscu dokończyć poprzednią linię liczbową;
4. w jakiej kolejności sprawdzić odczyt i zasady oraz jak zakończyć program przy błędzie;
5. w którym miejscu utworzyć rekord i wywołać `push_back`;
6. jak wypisać zlecenia pętlą z `const` referencją;
7. jak obliczyć sumę pozostałych jednostek z pól elementów wektora.

**Zanim napiszesz program**, przygotuj tabelę przypadków: zero, jedno, dwa i pięć zleceń, nazwy ze spacjami, zlecenia ukończone i nierozpoczęte, niedozwolona liczba zleceń, pusta nazwa, niedozwolone jednostki, słowo zamiast liczby, błąd w zleceniu po poprawnym, brak zapowiedzianego zlecenia i brak ostatniej liczby. Przy każdym zapisz oczekiwany wynik.

**Potem** uruchom program dla głównych danych i dla jednego z dwóch przypadków: zera zleceń albo błędu w drugim zleceniu. Wszystkie przypadki z pełnej listy kontrolnej są sprawdzone automatycznie, więc pozostałych nie musisz uruchamiać. Przypadki, w których dane się kończą, przeanalizuj na papierze.

### Kryterium sukcesu

- Program buduje się jako C++20 i dla głównych danych oraz wybranego drugiego przypadku wypisuje dokładnie pokazane wyniki, z nazwami klientów razem ze spacjami.
- Poprzednia linia liczbowa jest dokończona na początku przebiegu, a po ostatniej liczbie nie ma już odczytu.
- `std::cin.fail()` jest sprawdzane przed zasadami, rekord powstaje i trafia do wektora dopiero po obu sprawdzeniach, a przy błędzie nie ma żadnej części raportu.
- Liczba zleceń pochodzi z `size()`, a linie i suma z elementów wektora, odczytywanych przez `const` referencję.
- Tabela przypadków powstała przed uruchomieniem programu.
- Umiesz wyjaśnić, dlaczego po błędzie w drugim zleceniu pierwsze może być w wektorze, a mimo to program go nie wypisuje.

Gdy wynik się zgadza, możesz zapisać projekt w Gicie, jak w lekcji 1.5.

<details>
<summary>Podpowiedź 1</summary>

Jak utworzyć początkowo pustą kolekcję zleceń? Co ma się wydarzyć po pomyślnym odczytaniu pojedynczego zlecenia?

</details>

<details>
<summary>Podpowiedź 2</summary>

Każdy przebieg pętli powinien przygotować lokalne dane jednego zlecenia, sprawdzić je, a dopiero potem dodać kompletny rekord do wektora.

</details>

<details>
<summary>Podpowiedź 3</summary>

Na początku przebiegu dokończ poprzednią linię liczbową. Odczytaj nazwę i obie liczby. Po poprawnym odczycie i sprawdzeniu wartości utwórz rekord, dodaj go przez `push_back`, a po wczytaniu wszystkich zleceń przejdź po wektorze i oblicz wynik.

</details>

<details>
<summary>Pełna lista przypadków kontrolnych: otwórz po przygotowaniu własnej tabeli</summary>

Kolejne linie danych oddziela `/`. Przy poprawnych danych kolumna „Wynik” podaje liczbę zleceń i sumę pozostałych jednostek. Program wypisuje wtedy wszystkie zlecenia w kolejności z danych.

| | Dane | Wynik | Co sprawdza |
|---|---|---|---|
| A | `3` / `North Library` / `12 5` / `City Archive` / `8 8` / `Green Workshop` / `6 0` | 3 zlecenia, suma 13 | dane z wymagań: nazwy ze spacjami, zlecenie ukończone i nierozpoczęte |
| B | `0` | 0 zleceń, suma 0 | pusty wektor (dane z wymagań) |
| C | `1` / `Harbor Office` / `10 3` | 1 zlecenie, suma 7 | jedno zlecenie |
| D | `2` / `Park School` / `9 4` / `City Archive` / `8 2` | 2 zlecenia, suma 11 | dwa zlecenia, inna kolejność nazw |
| E | `5` / `Art Room` / `4 1` / `Book Club` / `6 6` / `Art Room` / `3 0` / `Main Office` / `10 9` / `Tool Shed` / `2 1` | 5 zleceń, suma 8 | największa liczba zleceń, ten sam klient dwa razy |
| F | `-1` | `Invalid orders` | ujemna liczba zleceń (dane z wymagań) |
| G | `6` | `Invalid orders` | liczba zleceń większa od 5: program nie odczytuje żadnego zlecenia |
| H | `three` | `Input error` | słowo zamiast liczby zleceń |
| I | `2` / pusta linia / `12 5` / `City Archive` / `8 8` | `Invalid orders` | pusta nazwa pierwszego zlecenia |
| J | `2` / `North Library` / `12 5` / pusta linia / `8 8` | `Invalid orders` | pusta nazwa późniejszego zlecenia |
| K | `2` / `North Library` / `12 5` / `City Archive` / `0 0` | `Invalid orders` | zero zaplanowanych jednostek |
| L | `1` / `North Library` / `-4 0` | `Invalid orders` | ujemna liczba zaplanowanych jednostek |
| M | `1` / `North Library` / `12 -1` | `Invalid orders` | ujemna liczba ukończonych jednostek |
| N | `2` / `North Library` / `12 5` / `City Archive` / `8 9` | `Invalid orders` | więcej ukończonych niż zaplanowanych, po poprawnym zleceniu (dane z wymagań) |
| O | `2` / `North Library` / `12 5` / `City Archive` / `8 done` | `Input error` | słowo zamiast drugiej liczby, po poprawnym zleceniu (dane z wymagań) |
| P | `2` / `North Library` / `twelve 5` / `City Archive` / `8 8` | `Input error` | słowo zamiast pierwszej liczby |
| Q | `2` / `North Library` / `12 5`, potem koniec danych | `Input error` | brak zapowiedzianego zlecenia: odczyt jego nazwy się nie udaje |
| R | `2` / `North Library` / `12 5` / `City Archive` / `8`, potem koniec danych | `Input error` | brak ostatniej liczby |

**Testy automatyczne i Twoje próby.** Wszystkie przypadki są sprawdzone automatycznie: rozwiązanie referencyjne jest uruchamiane dla każdego z nich, a jego pełne standardowe wyjście porównywane z oczekiwanym. Rozwiązanie i jego wyniki są w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

</details>

Przykładowe rozwiązanie jest w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 9. Znajdź błąd: rekord dodany zbyt wcześnie

To zadanie wykonaj **po misji**: program poniżej ma działać tak samo jak program z punktu 2. Możesz go skopiować do `main.cpp` w katalogu `lesson_10_3`.

<details>
<summary>Program do sprawdzenia: otwórz po napisaniu własnego programu</summary>

<!-- example: shipment_list_early_bug -->
```cpp
#include <iostream>
#include <string>
#include <vector>

struct Shipment {
    std::string destination;
    int boxes;
};

int main() {
    std::vector<Shipment> shipments{};
    int count{0};
    std::cin >> count;

    if (std::cin.fail()) {
        std::cout << "Input error\n";
        return 0;
    }

    if (count < 0 || count > 5) {
        std::cout << "Invalid shipments\n";
        return 0;
    }

    for (int index{0}; index < count; ++index) {
        std::string rest{};
        std::getline(std::cin, rest);

        std::string destination{};
        int boxes{0};
        std::getline(std::cin, destination);

        const Shipment shipment{destination, boxes};
        shipments.push_back(shipment);

        std::cin >> boxes;

        if (std::cin.fail()) {
            std::cout << "Input error\n";
            return 0;
        }

        if (destination.empty() || boxes < 0) {
            std::cout << "Invalid shipments\n";
            return 0;
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

Dane, w których każda przesyłka ma 0 paczek:

<!-- input: shipment_list_early_bug -->
```text
2
North Hub
0
South Depot
0
```

1. **Przewidź** wynik tego programu i programu z punktu 2 dla tych danych.
2. Uruchom program dla tych danych i porównaj wynik z przewidywaniem.
3. Dobierz własne poprawne dane, dla których ten program wypisze zły wynik.
4. Dla swoich danych **przewidź**, kiedy każdy rekord powstaje i trafia do wektora, jaką liczbę paczek ma wtedy jego pole i jaką liczbę odczyta później `>>`.
5. Uruchom program dla swoich danych.
6. Wyjaśnij, dlaczego poprawnie odczytana liczba paczek nie trafiła do elementu wektora. Czy późniejsza zmiana zmiennej `boxes` zmienia ten element?
7. Przenieś utworzenie rekordu i `push_back` za oba sprawdzenia i uruchom poprawiony program dla swoich danych. Dlaczego `push_back` ma stać dopiero po sprawdzeniu wszystkich pól?
8. Program z błędem dodaje rekord, zanim sprawdzi odczyt. Co byłoby w wektorze, gdyby zamiast liczby paczek wpisać słowo? Dlaczego tego nie widać w wyniku?

</details>

Wyniki, przykładowe dane i poprawiony program są w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 10. Gdy coś pójdzie inaczej

| Co widzisz | Co to znaczy | Co zrobić |
|---|---|---|
| `Input error` dla poprawnych danych | Linia z liczbą rekordów nie jest dokończona, bo `getline(rest)` brakuje albo stoi dopiero na końcu przebiegu. Pierwsza nazwa jest pusta, a odczyt liczby trafia na prawdziwą nazwę. | Wywołaj `std::getline(std::cin, rest)` na początku każdego przebiegu. |
| Raport ma zera zamiast odczytanych liczb | Rekord powstaje i trafia do wektora, zanim program odczyta liczby (punkt 9). | Twórz rekord i wywołuj `push_back` po odczycie i obu sprawdzeniach. |
| Po `Input error` albo `Invalid orders` program wypisuje jeszcze raport | Po komunikacie brakuje `return 0;`, więc pętla i raport wykonują się dalej. | Po komunikacie błędu zakończ `main` przez `return 0;`. |
| Raport zawiera zlecenie z liczbą 0, choć w danych było słowo | Brakuje sprawdzenia `std::cin.fail()` przed `push_back`. Na zawartości zmiennej po nieudanym odczycie nie wolno polegać (lekcja 4.6). | Sprawdzaj odczyt przed zasadami i przed dodaniem rekordu. |
| `Remaining total` jest mniejsze, niż powinno, albo któraś pozostała liczba jest ujemna | Program przepuszcza więcej ukończonych jednostek niż zaplanowanych. | Sprawdzaj tę zasadę dla każdego zlecenia. |
| Program czeka, choć wpisano wszystkie linie | Zapowiedziana liczba rekordów jest większa od liczby wpisanych albo brakuje liczby. `>>` pomija puste linie i czeka na liczbę (lekcja 10.1). | Wpisz brakujące dane albo popraw liczbę w pierwszej linii. |
| Kompilator zgłasza `no matching member function for call to 'push_back'` | Wektor ma `const`, więc nie można do niego niczego dodać (lekcja 6.2). | Usuń `const` z definicji wektora, który ma przyjmować rekordy. |

## 11. Wyjaśnij

Odpowiedz własnymi słowami, najlepiej na piśmie. Dopiero potem porównaj z przykładowymi odpowiedziami.

1. Dlaczego wektor przesyłek na początku jest pusty i nie ma `const`?
2. Co robi `shipments.push_back(shipment)`? Gdzie trafia nowy element i jak zmienia się `size()`?
3. Dlaczego rekord powstaje i trafia do wektora dopiero po sprawdzeniu odczytu i zasad? Czy `push_back` sprawdziłoby jego poprawność?
4. Gdyby po `push_back` program zmienił zmienną `boxes`, czy zmieniłby się element wektora? Dlaczego?
5. Dlaczego `getline(rest)` stoi na początku przebiegu, a nie po pętli? Co dokańcza w pierwszym przebiegu, a co w drugim?
6. Co program robi dla danych `0`? Dlaczego to poprawny wynik, a nie błąd?
7. Pierwsze zlecenie jest poprawne, a drugie ma `8 9`. Co jest wtedy w wektorze, a co wypisuje program? Dlaczego nie wypisuje pierwszego zlecenia?
8. Czym różni się zapowiedziana liczba zleceń od `size()` wektora? Dlaczego raport korzysta z `size()`?
9. Czym różni się `push_back` od zmiany pola elementu w pętli z referencją bez `const`? Dlaczego pętla raportu używa `const` referencji?

<details>
<summary>Przykładowe odpowiedzi</summary>

1. Zanim program cokolwiek odczyta, nie ma jeszcze żadnej przesyłki, więc wektor powstaje pusty przez `{}`. Nie ma `const`, bo program będzie do niego dodawać elementy (lekcja 6.2).
2. Dodaje na koniec wektora nowy element z wartościami pól rekordu `shipment`. Wcześniejsze elementy zostają na swoich miejscach, a `size()` rośnie o 1. Kolejność elementów to więc kolejność wywołań `push_back`.
3. Bo do wektora mają trafić tylko kompletne i poprawne rekordy. `push_back` niczego nie sprawdza: dodałoby także rekord z pustą nazwą albo z niedozwoloną liczbą. O tym, co trafi do wektora, decyduje program, który wywołuje `push_back` dopiero po obu sprawdzeniach.
4. Nie. Wektor przechowuje własny element, kopię rekordu z chwili wywołania `push_back` (lekcja 8.2). Element nie jest drugą nazwą zmiennej `boxes` ani lokalnego rekordu, więc późniejsza zmiana `boxes` go nie dotyczy. Na tym polega błąd z punktu 9.
5. Bo przed każdą nazwą trzeba dokończyć linię poprzedniej liczby. W pierwszym przebiegu jest to linia z liczbą rekordów, a w drugim linia liczbowa pierwszego rekordu. Po pętli żadna nazwa już nie następuje, więc program linii nie dokańcza. Gdyby dane kończyły się zaraz po ostatniej liczbie, bez końca linii, dodatkowe `getline` by się nie udało i zamieniło poprawne dane w `Input error`.
6. Odczytuje liczbę 0, sprawdza, że jest w zakresie, i nie wykonuje pętli ani razu. Wektor zostaje pusty, a raport podaje 0 zleceń i sumę 0. Zero zleceń to dozwolona sytuacja, a nie brak danych: liczba została poprawnie odczytana.
7. W wektorze jest pierwsze zlecenie, bo zostało dodane, zanim program odczytał drugie. Drugie nie zostało dodane. Program wypisuje tylko `Invalid orders` i kończy pracę, bo wynik ma dotyczyć całej listy: częściowy raport wyglądałby jak kompletny.
8. Zapowiedziana liczba to wartość odczytana z danych, a `size()` mówi, ile rekordów naprawdę jest w wektorze. Przy poprawnych danych są równe. Raport opisuje zawartość wektora, więc liczbę zleceń bierze z `size()`.
9. `push_back` dodaje nowy element i zwiększa `size()`. Pętla z referencją bez `const`, na przykład `for (Shipment& shipment : shipments)`, zmienia pola elementów, które już są w wektorze, a ich liczba się nie zmienia (lekcja 9.3). Raport tylko odczytuje elementy, więc `const` referencja wystarcza i zapewnia, że raport niczego nie zmieni.

</details>

## Podsumowanie

- Pierwsza linia danych zapowiada liczbę rekordów. Program sprawdza jej odczyt i zakres przed pętlą, a zero rekordów to poprawna, pusta lista.
- Każdy przebieg zaczyna od dokończenia poprzedniej linii, więc po ostatniej liczbie nie ma już odczytu.
- Każdy przebieg odczytuje pola do zmiennych lokalnych, sprawdza `std::cin.fail()`, potem zasady, a dopiero potem tworzy kompletny rekord i dodaje go przez `push_back`.
- `push_back` niczego nie sprawdza: dodaje na koniec własny element wektora i zwiększa `size()`.
- Przy pierwszym błędzie program wypisuje tylko komunikat i kończy pracę, bez częściowego raportu.
- Raport pochodzi z wektora: liczba rekordów z `size()`, a reszta z pól elementów odczytywanych przez `const` referencję.

## Co dalej

W tej lekcji liczba rekordów była znana z pierwszej linii danych, a cały odczyt był w `main`. W kolejnej lekcji odczyt jednego rekordu trafi do osobnej funkcji, a program będzie czytać rekordy do końca danych. Przejdź do lekcji [10.4: Funkcja odczytująca rekord i zakończenie danych](lesson_04_reading_function_and_end_of_data.md).

---

## Przykładowe rozwiązania

Zajrzyj tutaj **po własnej próbie**. Twoje nazwy mogą się różnić, jeśli standardowe wyjście jest takie, jak wymagane.

<details>
<summary>Punkt 8: misja, zlecenia w pracowni</summary>

<!-- example: orders -->
```cpp
#include <iostream>
#include <string>
#include <vector>

struct Order {
    std::string client;
    int planned_units;
    int completed_units;
};

int main() {
    std::vector<Order> orders{};
    int count{0};
    std::cin >> count;

    if (std::cin.fail()) {
        std::cout << "Input error\n";
        return 0;
    }

    if (count < 0 || count > 5) {
        std::cout << "Invalid orders\n";
        return 0;
    }

    for (int index{0}; index < count; ++index) {
        std::string rest{};
        std::getline(std::cin, rest);

        std::string client{};
        int planned_units{0};
        int completed_units{0};
        std::getline(std::cin, client);
        std::cin >> planned_units;
        std::cin >> completed_units;

        if (std::cin.fail()) {
            std::cout << "Input error\n";
            return 0;
        }

        if (client.empty() || planned_units <= 0 || completed_units < 0 || completed_units > planned_units) {
            std::cout << "Invalid orders\n";
            return 0;
        }

        const Order order{client, planned_units, completed_units};
        orders.push_back(order);
    }

    int remaining_total{0};
    std::cout << "Orders: " << orders.size() << "\n";

    for (const Order& order : orders) {
        const int remaining{order.planned_units - order.completed_units};
        std::cout << order.client << ": planned " << order.planned_units << ", completed " << order.completed_units << ", remaining " << remaining << "\n";
        remaining_total += remaining;
    }

    std::cout << "Remaining total: " << remaining_total << "\n";
}
```

1. **Pusty wektor na początku,** bo przed odczytem nie ma jeszcze żadnego zlecenia. Elementy dochodzą dopiero w pętli.
2. **Najpierw liczba zleceń,** bo od niej zależy, ile przebiegów wykona pętla.
3. **Sprawdzenie jej zakresu** przed pętlą, bo `-1` albo `6` to poprawnie odczytane, ale niedozwolone wartości. Program nie odczytuje wtedy żadnego zlecenia.
4. **Dla zera zleceń** warunek `index < count` od razu jest fałszywy, więc pętla się nie wykonuje, a wektor zostaje pusty.
5. **Dokańczanie na początku przebiegu,** bo przed każdą nazwą stoi niedokończona linia: w pierwszym przebiegu linia z liczbą zleceń, w kolejnych linia liczbowa poprzedniego zlecenia.
6. **Bez dokańczania po pętli,** bo program nie czyta już następnej nazwy. Dodatkowe `getline` mogłoby zamienić poprawne dane w `Input error`, gdy kończą się bez końca linii.
7. **Wartości początkowe zmiennych lokalnych,** bo po nieudanym odczycie zmienna może zachować dotychczasową wartość. Każdy przebieg zaczyna od własnych, nowych zmiennych.
8. **Odczyt przed wartościami,** bo na zawartości zmiennych po nieudanym odczycie nie wolno polegać. Zasady mają sens tylko dla naprawdę odczytanych liczb.
9. **Niedozwolone zlecenie nie trafia do wektora,** bo `return 0;` kończy `main`, zanim program dojdzie do `push_back`.
10. **`push_back` po utworzeniu kompletnego rekordu,** bo do wektora mają trafiać tylko zlecenia, których wszystkie pola są odczytane i sprawdzone.
11. **Wektor przechowuje własny element:** kopię rekordu `order`, niezależną od niego. Lokalny rekord znika na końcu przebiegu, a element zostaje.
12. **`size()` to liczba dodanych rekordów,** bo każde wywołanie `push_back` zwiększa ją o 1, a nic innego jej nie zmienia.
13. **Wcześniejsze poprawne zlecenia mogą zostać w wektorze** po błędzie w późniejszym. Program ich nie usuwa, bo zaraz kończy pracę.
14. **Mimo to bez częściowego raportu,** bo wynik dotyczy całej listy. Raport z części zleceń wyglądałby jak kompletny, choć dane były błędne.
15. **Wypisywanie przez `const Order&`,** bo pętla tylko odczytuje elementy i nie kopiuje ich przy każdym przebiegu (lekcja 8.4).
16. **Bez modyfikowalnej referencji,** bo raport niczego nie zmienia. `const` zapewnia, że kompilator nie pozwoli na przypadkową zmianę.
17. **Dodawanie a zmiana:** `push_back` dodaje nowy element i zwiększa `size()`, a zmiana przez `Order&` dotyczyłaby istniejących elementów (lekcja 9.3). Misja nie zmienia zleceń po odczycie.
18. **Bez funkcji odczytującej rekord,** bo odczyt jednego zlecenia mieści się czytelnie w pętli w `main`, a umowa takiej funkcji nie wymaga.
19. **Co zostaje na lekcję 10.4:** funkcja, która odczytuje jeden rekord, i odczyt rekordów aż do końca danych, gdy ich liczba nie jest zapowiedziana.

**Inne poprawne rozwiązania:** zamiast `return 0;` można użyć flagi `bool`, jak w lekcjach 4.5 i 7.4. Wtedy pętla działa, dopóki flaga jest prawdziwa i są jeszcze zapowiedziane rekordy, a po pętli program wybiera komunikat albo raport. Zasady mogą stać w kilku osobnych warunkach z tym samym komunikatem. Sumę można obliczyć w osobnej pętli po wektorze, a pozostałe jednostki bezpośrednio w instrukcji wypisania.

Każdy przypadek z listy kontrolnej to osobne uruchomienie tego programu. Przypadki A, B, F, N i O to dane z treści misji. Pozostałe są poniżej, w kolejności z listy kontrolnej.

<!-- input: orders -->
```text
1
Harbor Office
10 3
```

<!-- output: orders -->
```text
Orders: 1
Harbor Office: planned 10, completed 3, remaining 7
Remaining total: 7
```

<!-- input: orders -->
```text
2
Park School
9 4
City Archive
8 2
```

<!-- output: orders -->
```text
Orders: 2
Park School: planned 9, completed 4, remaining 5
City Archive: planned 8, completed 2, remaining 6
Remaining total: 11
```

<!-- input: orders -->
```text
5
Art Room
4 1
Book Club
6 6
Art Room
3 0
Main Office
10 9
Tool Shed
2 1
```

<!-- output: orders -->
```text
Orders: 5
Art Room: planned 4, completed 1, remaining 3
Book Club: planned 6, completed 6, remaining 0
Art Room: planned 3, completed 0, remaining 3
Main Office: planned 10, completed 9, remaining 1
Tool Shed: planned 2, completed 1, remaining 1
Remaining total: 8
```

<!-- input: orders -->
```text
6
```

<!-- output: orders -->
```text
Invalid orders
```

<!-- input: orders -->
```text
three
```

<!-- output: orders -->
```text
Input error
```

<!-- input: orders -->
```text
2

12 5
City Archive
8 8
```

<!-- output: orders -->
```text
Invalid orders
```

<!-- input: orders -->
```text
2
North Library
12 5

8 8
```

<!-- output: orders -->
```text
Invalid orders
```

<!-- input: orders -->
```text
2
North Library
12 5
City Archive
0 0
```

<!-- output: orders -->
```text
Invalid orders
```

<!-- input: orders -->
```text
1
North Library
-4 0
```

<!-- output: orders -->
```text
Invalid orders
```

<!-- input: orders -->
```text
1
North Library
12 -1
```

<!-- output: orders -->
```text
Invalid orders
```

<!-- input: orders -->
```text
2
North Library
twelve 5
City Archive
8 8
```

<!-- output: orders -->
```text
Input error
```

<!-- input: orders -->
```text
2
North Library
12 5
```

<!-- output: orders -->
```text
Input error
```

<!-- input: orders -->
```text
2
North Library
12 5
City Archive
8
```

<!-- output: orders -->
```text
Input error
```

</details>

<details>
<summary>Punkt 9: wyniki przed poprawką i poprawiony program</summary>

Przed poprawką, dla danych z zerową liczbą paczek:

<!-- output: shipment_list_early_bug -->
```text
Shipments: 2
North Hub: 0
South Depot: 0
Total boxes: 0
```

- **Ten przypadek maskuje błąd.** Program z punktu 2 wypisuje dla tych danych to samo. Program z błędem tworzy każdy rekord z liczbą paczek 0, czyli z wartością początkową zmiennej `boxes`, a w danych też jest 0. Rekord w wektorze przypadkiem zgadza się z danymi.
- **Dane, które ujawniają błąd:** dowolne poprawne dane, w których co najmniej jedna przesyłka ma dodatnią liczbę paczek, na przykład dane z punktu 2. Poprawny wynik to raport z liczbami 4 i 7 oraz sumą 11, a program z błędem wypisuje:

<!-- input: shipment_list_early_bug -->
```text
2
North Hub
4
South Depot
7
```

<!-- output: shipment_list_early_bug -->
```text
Shipments: 2
North Hub: 0
South Depot: 0
Total boxes: 0
```

- **Kiedy powstaje rekord:** zaraz po odczycie nazwy, gdy `boxes` ma jeszcze wartość początkową 0. `push_back` dodaje do wektora element z liczbą paczek 0.
- **Dlaczego liczba nie trafia do wektora:** `>>` odczytuje 4 i zapisuje je w zmiennej `boxes`, a oba sprawdzenia przechodzą. Element wektora jest jednak własną kopią rekordu z chwili `push_back`, a nie drugą nazwą zmiennej `boxes`. Zmiana `boxes` go nie dotyczy, więc raport pokazuje 0.
- **Słowo zamiast liczby paczek:** w wektorze byłby już rekord, którego liczba paczek nigdy nie została odczytana. Wynik i tak brzmi `Input error`, bo program kończy pracę bez raportu, więc w tym programie tego nie widać. Gdyby program wypisywał po błędzie przesyłki z wektora, pokazałby liczbę paczek, której nie było w danych.
- **Poprawka:** przenieś utworzenie rekordu i `push_back` za oba sprawdzenia. Wtedy do wektora trafia tylko rekord, którego wszystkie pola są odczytane i sprawdzone. Poprawiony program to program z punktu 2:

<!-- example: shipment_list_early_fixed -->
```cpp
#include <iostream>
#include <string>
#include <vector>

struct Shipment {
    std::string destination;
    int boxes;
};

int main() {
    std::vector<Shipment> shipments{};
    int count{0};
    std::cin >> count;

    if (std::cin.fail()) {
        std::cout << "Input error\n";
        return 0;
    }

    if (count < 0 || count > 5) {
        std::cout << "Invalid shipments\n";
        return 0;
    }

    for (int index{0}; index < count; ++index) {
        std::string rest{};
        std::getline(std::cin, rest);

        std::string destination{};
        int boxes{0};
        std::getline(std::cin, destination);
        std::cin >> boxes;

        if (std::cin.fail()) {
            std::cout << "Input error\n";
            return 0;
        }

        if (destination.empty() || boxes < 0) {
            std::cout << "Invalid shipments\n";
            return 0;
        }

        const Shipment shipment{destination, boxes};
        shipments.push_back(shipment);
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

<!-- input: shipment_list_early_fixed -->
```text
2
North Hub
4
South Depot
7
```

<!-- output: shipment_list_early_fixed -->
```text
Shipments: 2
North Hub: 4
South Depot: 7
Total boxes: 11
```

Dla danych z zerową liczbą paczek poprawiony program wypisuje to samo co program z błędem:

<!-- input: shipment_list_early_fixed -->
```text
2
North Hub
0
South Depot
0
```

<!-- output: shipment_list_early_fixed -->
```text
Shipments: 2
North Hub: 0
South Depot: 0
Total boxes: 0
```

</details>

**Poprzednia lekcja:** [Lekcja 10.2: Nazwy ze spacjami: `>>` i `std::getline`](lesson_02_names_with_spaces.md) · **Następna lekcja:** [Lekcja 10.4: Funkcja odczytująca rekord i zakończenie danych](lesson_04_reading_function_and_end_of_data.md) · [Opis kursu](../../README.md)

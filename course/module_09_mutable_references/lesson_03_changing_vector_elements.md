# Lekcja 9.3: Modyfikowanie elementów wektora przez referencję

**Polski** · [English](lesson_03_changing_vector_elements.en.md) · [Opis kursu](../../README.md)

> **Moduł 9, lekcja 3** · około 75–90 minut
> **Potrzebujesz:** katalogu `cpp-workspace` i oryginalnego projektu `lesson_05_first_program`, jak dotąd. Debugger nie jest w tej lekcji potrzebny.
> **Wersja pilotażowa.** Programy z tej lekcji sprawdzamy automatycznie na Windowsie, Ubuntu i macOS. Żaden z nich nie pyta o dane: wszystkie wartości są zapisane w kodzie. Dane z wejścia odczytuje tylko program kontrolny w części z rozwiązaniami.

## Zanim zaczniesz

Ta lekcja zakłada, że:

- przeglądasz wektor pętlą zakresową (lekcja 6.1) i przekazujesz go do funkcji przez `const&` (lekcja 6.4);
- przeglądasz wektor rekordów pętlą `for (const Product& product : products)` i liczysz rekordy w zmiennej `std::size_t` (lekcja 8.4);
- piszesz funkcję z parametrem `Product&`, która zmienia przekazany rekord (lekcja 9.1);
- znasz funkcję `issue_units` z lekcji 9.2: wydaje towar tylko po spełnieniu warunków, a przy odmowie zostawia rekord bez zmian i zwraca `false`.

## Sytuacja

Funkcja `issue_units` z lekcji 9.2 zmienia jeden produkt. Magazyn przechowuje jednak wiele produktów w jednym wektorze i chce wydać po 4 sztuki z **każdego** z nich. Pętla `const Product&` z lekcji 8.4 może elementy tylko czytać. Funkcja z lekcji 6.5 tworzyła nowy wektor, a tu mają się zmienić rekordy, które już są w wektorze.

Potrzebne są dwie rzeczy: pętla, której zmienna pozwala zmienić prawdziwy element wektora, i funkcja, której wywołujący pozwala zmienić cały istniejący wektor.

Po tej lekcji będziesz:

- przeglądać elementy wektora pętlą `for (Product& product : products)` i zmieniać je przez zmienną pętli;
- pisać funkcję z parametrem `std::vector<Product>&`, która zmienia elementy istniejącego wektora;
- odróżniać zmienne pętli `const Product&`, `Product&` i `Product`;
- dzielić pracę między funkcję dla jednego rekordu i funkcję dla całej kolekcji;
- liczyć tylko rekordy, które naprawdę się zmieniły;
- dobierać dane, które ujawniają, że pętla zmienia kopie elementów.

## 1. Przygotuj projekt

W `cpp-workspace` utwórz katalog `lesson_9_3` i skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program`. Program z punktu 3 wpisujesz w `main.cpp` tego katalogu.

## 2. Pętla, która zmienia elementy

Wektor `products` przechowuje trzy produkty: `Tea` (3 sztuki), `Rice` (8) i `Pens` (10). Z każdego chcemy spróbować wydać po 4 sztuki. Nie szukamy produktu o konkretnej nazwie: przechodzimy po wszystkich rekordach i na każdym wykonujemy tę samą kontrolowaną operację.

<!-- fragment -->
```cpp
for (Product& product : products) {
    issue_units(product, 4);
}
```

| Część | Znaczenie |
|---|---|
| `Product& product` | zmienna pętli: w każdym przebiegu inna nazwa kolejnego elementu wektora, z możliwością zmiany |
| `products` | wektor istniejących rekordów |
| `issue_units(product, 4)` | funkcja z lekcji 9.2 dostaje bieżący element przez `Product&` |

- **`product` odnosi się kolejno do prawdziwych elementów:** w pierwszym przebiegu do `Tea`, w drugim do `Rice`, w trzecim do `Pens`.
- **`&` pozwala zmienić pole elementu.** Zmiana przez `product` zmienia rekord w wektorze, a nie kopię.
- **`issue_units` nadal odpowiada za warunki jednej operacji.** Odrzucone wydanie zostawia ten jeden rekord bez zmian.
- **Każdy element jest przetwarzany niezależnie.** Odmowa dla jednego produktu nie zatrzymuje pętli i nie zmienia pozostałych.
- **Pętla nie dodaje, nie usuwa ani nie przestawia elementów.** Wektor ma po niej tyle samo elementów, w tej samej kolejności. Zmieniają się tylko pola.

## 3. Funkcja dla całego wektora

Pracę nad całą kolekcją przenosimy do funkcji. Dostaje ona wektor przez `std::vector<Product>&`.

<!-- example: issue_each -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>
#include <vector>

struct Product {
    std::string name;
    int stock;
    int minimum;
    int unit_price;
};

bool issue_units(Product& product, int amount) {
    if (amount <= 0 || amount > product.stock) {
        return false;
    }

    product.stock -= amount;
    return true;
}

std::size_t issue_from_each(std::vector<Product>& products, int amount) {
    std::size_t accepted{0};

    for (Product& product : products) {
        if (issue_units(product, amount)) {
            ++accepted;
        }
    }

    return accepted;
}

int main() {
    std::vector<Product> products{
        {"Tea", 3, 8, 6},
        {"Rice", 8, 8, 4},
        {"Pens", 10, 7, 2}
    };

    const std::size_t accepted{issue_from_each(products, 4)};

    std::cout << "Accepted: " << accepted << "\n";

    for (const Product& product : products) {
        std::cout << product.name << ": " << product.stock << "\n";
    }
}
```

**Przewidź** wszystkie cztery linijki, a potem uruchom program.

<details>
<summary>Standardowe wyjście i przebieg pętli</summary>

<!-- output: issue_each -->
```text
Accepted: 2
Tea: 3
Rice: 4
Pens: 6
```

| Przebieg | `product` odnosi się do | `stock` przed | `issue_units(product, 4)` | `stock` po | `accepted` |
|---|---|---:|---|---:|---:|
| 1 | `Tea` | 3 | `false`: za mało sztuk | 3 | 0 |
| 2 | `Rice` | 8 | `true` | 4 | 1 |
| 3 | `Pens` | 10 | `true` | 6 | 2 |

</details>

- **`std::vector<Product>& products`:** funkcja dostaje istniejący wektor z `main`, a nie jego kopię, i może zmieniać jego elementy. To umowa z lekcji 9.1, tylko dla całej kolekcji.
- **Pętla `Product&`** odwiedza prawdziwe elementy tego wektora.
- **Podział pracy:** `issue_units` rozstrzyga o jednym produkcie, a `issue_from_each` organizuje pracę nad kolekcją. Reguły wydania nie ma w drugiej funkcji.
- **Licznik rośnie tylko po przyjętym wydaniu.** Odmowa niczego nie zmienia, więc nie jest liczona jako zmiana. Wynik to liczba rekordów, dlatego ma typ `std::size_t`, jak w lekcji 8.4.
- **Wywołanie w samym warunku:** wynik `issue_units` służy tylko do licznika, więc wywołanie stoi w `if`. Wykonuje się raz w każdym przebiegu.
- **Funkcja niczego nie wypisuje** i nie zmienia nazw ani liczby rekordów. Raport w `main` tylko czyta elementy, więc używa pętli `const Product&`.
- **`products` w `main` nie ma `const`,** bo jego elementy mają się zmienić.

**`&` jest potrzebne na dwóch poziomach.** Parametr `std::vector<Product>&` daje dostęp do wektora z `main`, a zmienna pętli `Product&` do jego elementów. Gdyby zabrakło któregokolwiek, zmiana trafiłaby do kopii: do osobnego wektora funkcji albo do osobnego obiektu w pętli.

## 4. Trzy sposoby przekazania wektora

| Parametr | Znaczenie |
|---|---|
| `std::vector<Product> products` | funkcja dostaje osobny wektor przekazany przez wartość |
| `const std::vector<Product>& products` | funkcja odczytuje istniejący wektor |
| `std::vector<Product>& products` | funkcja może zmieniać istniejący wektor |

Przekazanie przez wartość to poprawny C++: funkcja może zmieniać swój wektor, ale wektor wywołującego zostaje taki sam. `&` nie jest też zawsze lepszy. Wybór wynika z zadania funkcji: odczyt, zmiana istniejącej kolekcji albo praca na własnej kopii.

Tak samo jest ze zmienną pętli:

<!-- fragment -->
```cpp
for (const Product& product : products)   // 1
for (Product& product : products)         // 2
for (Product product : products)          // 3
```

| | Zmienna pętli | Zmiana pola przez zmienną pętli |
|---|---|---|
| 1 | inna nazwa elementu, tylko do odczytu | nie zbuduje się |
| 2 | inna nazwa elementu, z możliwością zmiany | zmienia element wektora |
| 3 | osobny obiekt z kopią wartości elementu | zmienia tylko ten obiekt, a element zostaje bez zmian |

Zapis 3 to poprawny C++, ale do zmiany elementów się nie nadaje.

## 5. Wektor `const` i pusty wektor

**Przewidź na papierze** dwie sytuacje dla funkcji `issue_from_each` z punktu 3:

<!-- fragment -->
```cpp
const std::vector<Product> fixed_products{
    {"Tea", 3, 8, 6}
};
std::vector<Product> no_products{};

const std::size_t first{issue_from_each(fixed_products, 4)};    // 1
const std::size_t second{issue_from_each(no_products, 4)};      // 2
```

1. Czy wywołanie 1 się zbuduje? Dlaczego?
2. Ile przebiegów wykona pętla w wywołaniu 2, co się zmieni i jaki będzie wynik?

<details>
<summary>Odpowiedzi</summary>

1. **Nie.** Kompilator zgłasza `no matching function for call to 'issue_from_each'` z uwagą, że pierwszy argument straciłby `const`. `const` przy wektorze obiecuje, że kolekcja się nie zmieni, a parametr `std::vector<Product>&` prosi o prawo do zmiany. Odrzucenie jest prawidłowe, jak przy pojedynczym rekordzie w lekcji 9.1. Nie usuwaj `const` tylko po to, żeby uciszyć kompilator: jeśli stan magazynu ma zostać taki sam, ta funkcja nie jest dla niego. Funkcja z parametrem `const std::vector<Product>&` przyjęłaby ten wektor, bo obiecuje tylko odczyt.
2. **Zero przebiegów.** Pętla nie odczytuje żadnego elementu, nic się nie zmienia, a funkcja zwraca początkową wartość licznika, czyli 0. Pusty wektor to poprawne dane: nie potrzeba osobnego warunku, a odczyt `no_products[0]` byłby błędem, bo takiego elementu nie ma.

</details>

## 6. Misja: rozliczenie rowerów miejskich

Wypożyczalnia przechowuje rowery miejskie w jednym wektorze. Każdy rower ma identyfikator, łączną liczbę przejazdów zapisanych w historii i liczbę dzisiejszych przejazdów, które czekają na rozliczenie. Po zakończeniu dnia oczekujące przejazdy trzeba przenieść do historii. Nie tworzymy nowej floty: **zmieniamy istniejące rekordy**.

**Dane:**

| Rower | Łączna liczba przejazdów | Oczekujące przejazdy |
|---|---:|---:|
| B-01 | 12 | 3 |
| B-02 | 7 | 0 |
| B-03 | 20 | 2 |
| B-04 | 0 | 1 |

**Reguły:**

- Liczby są nieujemne i niewielkie. Dane spełniają te założenia, więc program ich nie sprawdza.
- **Rozliczenie jednego roweru:** jeśli liczba oczekujących przejazdów jest dodatnia, zostaje dodana do łącznej liczby przejazdów, a liczba oczekujących spada do 0. Rekord został zmieniony. Jeśli oczekujących przejazdów jest 0, żadne pole się nie zmienia.
- Identyfikator nigdy się nie zmienia. Tych samych przejazdów nie wolno doliczyć drugi raz przy kolejnym rozliczeniu.
- **Rozliczenie floty** rozlicza każdy rower i podaje, ile rekordów naprawdę się zmieniło.

**Wymagania:**

- Program definiuje własny typ z trzema polami: identyfikatorem (`std::string`), łączną liczbą przejazdów (`int`) i liczbą oczekujących przejazdów (`int`). Nazwy typu i pól wybierasz samodzielnie.
- W `main` jest jeden wektor tych rekordów, zainicjalizowany w kodzie w kolejności z tabeli. Bez osobnych zmiennych na każdy rower i bez `push_back`.
- **Funkcja dla jednego roweru** dostaje jeden istniejący rekord, rozlicza go według reguł i zwraca odpowiedź, czy go zmieniła.
- **Funkcja dla floty** dostaje istniejący wektor, odwiedza wszystkie jego rekordy, dla każdego wywołuje funkcję dla jednego roweru i zwraca liczbę zmienionych rekordów. Nie powtarza reguły rozliczenia i nie zmienia liczby ani kolejności elementów.
- Żadna z tych funkcji niczego nie wypisuje ani nie odczytuje z wejścia. Ich nazwy i parametry wybierasz samodzielnie.
- `main` wypisuje liczbę rowerów (z `size()`) i stan przed rozliczeniem, potem **dwa razy rozlicza tę samą flotę**, wypisuje oba wyniki i stan po obu rozliczeniach, dokładnie jak w przykładzie niżej.
- Program nie odczytuje niczego z wejścia.

W `cpp-workspace` utwórz katalog `city_bikes`, skopiuj do niego `CMakeLists.txt` z oryginalnego `lesson_05_first_program`, utwórz pusty `main.cpp` i napisz program samodzielnie.

Dla danych z tabeli standardowe wyjście ma być takie:

<!-- output: city_bikes -->
```text
Bikes: 4
Before:
B-01: total 12, pending 3
B-02: total 7, pending 0
B-03: total 20, pending 2
B-04: total 0, pending 1
Updated: 3
Updated again: 0
After:
B-01: total 15, pending 0
B-02: total 7, pending 0
B-03: total 22, pending 0
B-04: total 1, pending 0
```

Pierwsze rozliczenie zmienia trzy rekordy, bo `B-02` nie ma oczekujących przejazdów. Drugie, na **tym samym wektorze**, nie zmienia żadnego: pierwsze wyzerowało już wszystkie oczekujące przejazdy.

Dla pustej floty program ma wypisać:

<!-- output: city_bikes_empty -->
```text
Bikes: 0
Before:
Updated: 0
Updated again: 0
After:
```

**To nie jest wydawanie towaru z innymi nazwami.** Musisz samodzielnie zdecydować:

1. jak nazwać typ, jego pola i obie funkcje;
2. jakie typy wyników mają obie funkcje;
3. jak przekazać jeden rekord, a jak cały wektor;
4. jaka zmienna pętli pozwala zmienić element wektora, a jaka wystarcza do wypisania;
5. kiedy rower wymaga rozliczenia;
6. w jakiej kolejności zmienić oba pola;
7. jak liczyć tylko rekordy, które naprawdę się zmieniły;
8. dlaczego drugie rozliczenie nie może niczego doliczyć;
9. co program robi dla pustej floty.

**Zanim napiszesz program**, przygotuj tabelę przypadków: dane z wymagań, pusta flota, jeden rower bez oczekujących przejazdów, jeden rower z oczekującymi, wszystkie rowery bez oczekujących, wszystkie z oczekującymi, dwa rowery z tymi samymi liczbami i flota z wymagań w odwrotnej kolejności. Przy każdym zapisz oba wyniki rozliczenia i stan po nim.

Sprawdź też tabelę rachunkiem: suma łącznych przejazdów po rozliczeniu musi być równa sumie łącznych przejazdów przed nim i wszystkich oczekujących. Dla danych z wymagań: 39 + 6 = 45. Ta zależność kontroluje rozumowanie, ale nie zastępuje sprawdzenia każdego rekordu.

**Potem** uruchom program dla danych z wymagań i dla pustej floty. Zmieniaj przy tym tylko inicjalizację wektora. Wszystkie przypadki z pełnej listy kontrolnej są sprawdzone automatycznie.

### Kryterium sukcesu

- Program buduje się jako C++20 i dla obu uruchomień wypisuje dokładnie linijki pokazane wyżej.
- Funkcja dla jednego roweru zmienia rekord tylko wtedy, gdy są oczekujące przejazdy. Funkcja dla floty wywołuje ją dla każdego elementu i liczy tylko rzeczywiste zmiany.
- Typy wyników pasują do odpowiedzi: tak albo nie dla jednego roweru, liczba rekordów dla floty.
- Obie funkcje zmieniają istniejące dane z `main`, a nie ich kopie. Niczego nie wypisują ani nie odczytują.
- Oba rozliczenia dotyczą tego samego wektora, a drugie zwraca 0.
- Tabela przypadków powstała przed uruchomieniem programu.
- Umiesz wyjaśnić, dlaczego `&` stoi zarówno w parametrze wektora, jak i w zmiennej pętli.

Gdy wynik się zgadza, możesz zapisać projekt w Gicie, jak w lekcji 1.5.

<details>
<summary>Podpowiedź 1</summary>

Czy funkcja ma przygotować nową flotę, czy zmienić rowery już przechowywane w istniejącym wektorze?

</details>

<details>
<summary>Podpowiedź 2</summary>

Jedna funkcja może rozliczyć pojedynczy rower. Druga może przejść po całej flocie i wywołać ją dla każdego elementu. Jakich referencji potrzebujesz?

</details>

<details>
<summary>Podpowiedź 3</summary>

Po poprawnym rozliczeniu przejazdy oczekujące mają zostać dodane do historii i wyzerowane. Drugi przebieg na tym samym wektorze nie może rozliczyć ich ponownie.

</details>

<details>
<summary>Pełna lista przypadków kontrolnych: otwórz po przygotowaniu własnej tabeli</summary>

Każdy rower jest zapisany jako identyfikator, łączna liczba przejazdów i liczba oczekujących.

| | Flota | Wyniki | Po rozliczeniu | Suma łącznych przejazdów | Co sprawdza |
|---|---|---|---|---|---|
| A | B-01 12 3, B-02 7 0, B-03 20 2, B-04 0 1 | 3, potem 0 | B-01 15 0, B-02 7 0, B-03 22 0, B-04 1 0 | 39 + 6 = 45 | dane z wymagań: rekordy mieszane, zerowa łączna liczba przy B-04 |
| B | pusta | 0, potem 0 | pusta | 0 + 0 = 0 | pusta flota |
| C | C-01 5 0 | 0, potem 0 | C-01 5 0 | 5 + 0 = 5 | jeden rower bez oczekujących przejazdów |
| D | D-01 4 6 | 1, potem 0 | D-01 10 0 | 4 + 6 = 10 | jeden rower z oczekującymi przejazdami |
| E | E-01 3 0, E-02 0 0, E-03 9 0 | 0, potem 0 | bez zmian | 12 + 0 = 12 | żaden rower nie wymaga rozliczenia |
| F | F-01 1 2, F-02 5 5, F-03 0 4 | 3, potem 0 | F-01 3 0, F-02 10 0, F-03 4 0 | 6 + 11 = 17 | wszystkie rowery wymagają rozliczenia |
| G | G-01 6 2, G-02 6 2 | 2, potem 0 | G-01 8 0, G-02 8 0 | 12 + 4 = 16 | dwa rowery z tymi samymi liczbami |
| H | B-04 0 1, B-03 20 2, B-02 7 0, B-01 12 3 | 3, potem 0 | B-04 1 0, B-03 22 0, B-02 7 0, B-01 15 0 | 39 + 6 = 45 | odwrotna kolejność, zachowana w wydruku |
| I | I-01 2 0, I-02 3 0, I-03 1 7 | 1, potem 0 | I-03 8 0, reszta bez zmian | 6 + 7 = 13 | do rozliczenia tylko ostatni rower |
| J | J-01 4 5, J-02 6 0, J-03 8 0 | 1, potem 0 | J-01 9 0, reszta bez zmian | 18 + 5 = 23 | do rozliczenia tylko pierwszy rower |

We wszystkich przypadkach identyfikatory, liczba rowerów i ich kolejność po rozliczeniu są takie same jak przed nim.

**Testy automatyczne i Twoje próby.** Wszystkie przypadki są sprawdzone automatycznie przez program kontrolny. Ma on ten sam typ i te same funkcje co rozwiązanie referencyjne, ale flotę odczytuje z wejścia. To tylko narzędzie do sprawdzania, a nie część misji: w misji dane są wpisane w kodzie. Program kontrolny i jego wyniki są w części [Przykładowe rozwiązania](#przykładowe-rozwiązania), bo zawierają rozwiązanie.

</details>

Przykładowe rozwiązanie jest w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 7. Znajdź błąd: zmienia się kopia elementu

To zadanie wykonaj **po misji**: program poniżej ma rozliczyć flotę, tak jak Twój program. Program możesz przepisać albo skopiować do `main.cpp`.

<details>
<summary>Program do sprawdzenia: otwórz po napisaniu własnego programu</summary>

<!-- example: fleet_copy_bug -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>
#include <vector>

struct Bike {
    std::string id;
    int total_rides;
    int pending_rides;
};

bool settle_bike(Bike& bike) {
    if (bike.pending_rides <= 0) {
        return false;
    }

    bike.total_rides += bike.pending_rides;
    bike.pending_rides = 0;
    return true;
}

std::size_t settle_fleet(std::vector<Bike>& bikes) {
    std::size_t updated{0};

    for (Bike bike : bikes) {
        if (settle_bike(bike)) {
            ++updated;
        }
    }

    return updated;
}

int main() {
    std::vector<Bike> bikes{
        {"B-01", 12, 0},
        {"B-02", 7, 0},
        {"B-03", 20, 0}
    };

    std::cout << "Bikes: " << bikes.size() << "\n";
    std::cout << "Before:\n";

    for (const Bike& bike : bikes) {
        std::cout << bike.id << ": total " << bike.total_rides << ", pending " << bike.pending_rides << "\n";
    }

    const std::size_t updated{settle_fleet(bikes)};
    const std::size_t updated_again{settle_fleet(bikes)};

    std::cout << "Updated: " << updated << "\n";
    std::cout << "Updated again: " << updated_again << "\n";
    std::cout << "After:\n";

    for (const Bike& bike : bikes) {
        std::cout << bike.id << ": total " << bike.total_rides << ", pending " << bike.pending_rides << "\n";
    }
}
```

1. **Przewidź** wynik dla danych z programu: żaden rower nie ma oczekujących przejazdów.
2. Uruchom program. Czy wynik wygląda poprawnie?
3. Zmień dane tak, żeby co najmniej jeden rower miał dodatnią liczbę oczekujących przejazdów. Zapisz poprawny wynik dla swoich danych.
4. **Przewidź**, co ten program wypisze w linijkach `Updated` i `Updated again`.
5. **Przewidź** stan rowerów w części `After`.
6. Uruchom program.
7. Wskaż miejsce, w którym powstają kopie.
8. Wyjaśnij, dlaczego funkcja dla jednego roweru działa poprawnie, a funkcja dla floty nie spełnia swojej umowy.
9. Popraw pętlę.
10. Uruchom poprawiony program dla swoich danych.

</details>

Wyniki, przykładowe dane i poprawiony program są w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 8. Gdy coś pójdzie inaczej

| Co widzisz | Co to znaczy | Co zrobić |
|---|---|---|
| `Updated` jest większe od 0, ale `After` pokazuje stary stan | Pętla w funkcji dla floty kopiuje elementy, a funkcja dla jednego roweru zmienia kopie (punkt 7). | Zmienna pętli w funkcji zmieniającej elementy potrzebuje `&`. |
| Zmiany widać w funkcji, ale nie w `main` | Funkcja dostaje wektor przez wartość i zmienia własną kopię. | Przekaż wektor przez `&`. |
| `Updated again` jest większe od 0, a łączne liczby rosną drugi raz | Funkcja dla jednego roweru nie zeruje oczekujących przejazdów. | Po dodaniu ustaw liczbę oczekujących przejazdów na 0. |
| Liczba oczekujących spada do 0, ale łączna liczba się nie zmienia | Funkcja zeruje oczekujące przejazdy przed dodaniem ich do historii. | Najpierw dodaj, potem wyzeruj. |
| `Updated` jest równe liczbie wszystkich rowerów | Licznik rośnie w każdym przebiegu, a nie tylko po zmianie. | Zwiększaj licznik tylko wtedy, gdy funkcja dla jednego roweru zgłosi zmianę. |
| Rower bez oczekujących przejazdów jest liczony jako zmieniony | Funkcja dla jednego roweru zgłasza zmianę, choć niczego nie zmieniła. | Gdy nie ma czego rozliczać, zostaw rekord i zwróć `false`. |
| `binding reference of type ... drops 'const' qualifier` | Pętla `&` przegląda wektor `const` albo parametr `const&`. | Funkcja, która zmienia elementy, potrzebuje parametru `&` bez `const`. |
| `no matching function for call to ...` z uwagą `would lose const qualifier` | Wektor `const` trafia do funkcji z parametrem `&` (punkt 5). | Zdecyduj, czy flota ma się zmieniać. Jeśli tak, usuń `const` z wektora. |

## 9. Wyjaśnij

Odpowiedz własnymi słowami, najlepiej na piśmie. Dopiero potem porównaj z przykładowymi odpowiedziami.

1. Czym różnią się parametry `std::vector<Product> products`, `const std::vector<Product>& products` i `std::vector<Product>& products`? Od czego zależy wybór?
2. Czym różnią się zmienne pętli `const Product& product`, `Product& product` i `Product product`?
3. Dlaczego funkcja zmieniająca elementy potrzebuje `&` w dwóch miejscach? Co się stanie, jeśli zabraknie jednego z nich?
4. Dlaczego funkcja dla floty wywołuje funkcję dla jednego roweru, zamiast powtarzać jej warunek i zmiany?
5. Dlaczego licznik rośnie tylko wtedy, gdy funkcja dla jednego rekordu zgłosi zmianę? Co policzyłby licznik zwiększany w każdym przebiegu?
6. Czy pętla `for (Product& product : products)` może zmienić liczbę albo kolejność elementów wektora?
7. Co robi funkcja dla floty, gdy wektor jest pusty? Dlaczego nie potrzebuje osobnego warunku?
8. Dlaczego drugie rozliczenie tej samej floty zwraca 0? Co by oznaczało, gdyby zwróciło 3?
9. W wersji z błędem licznik pokazuje zmianę, choć wektor się nie zmienił. Jak to możliwe? Dlaczego flota bez oczekujących przejazdów nie ujawnia błędu?
10. Kiedy lepiej zmienić istniejący wektor, a kiedy zwrócić nowy, jak `keep_negative` w lekcji 6.5?

<details>
<summary>Przykładowe odpowiedzi</summary>

1. Przez wartość funkcja dostaje osobny wektor: może go zmieniać, ale wektor wywołującego zostaje taki sam. Przez `const&` tylko odczytuje istniejący wektor. Przez `&` może zmieniać istniejący wektor i jego elementy. Wybór zależy od zadania funkcji: odczyt, zmiana kolekcji wywołującego albo praca na własnej kopii.
2. `const Product&` to inna nazwa elementu, tylko do odczytu. `Product&` to inna nazwa elementu, przez którą można go zmienić. `Product` to osobny obiekt z kopią wartości elementu: jego zmiana nie dotyczy wektora.
3. Bo zmiana musi dotrzeć do elementów wektora z `main`. Parametr `&` daje dostęp do tego wektora, a zmienna pętli `&` do jego elementów. Bez `&` w parametrze funkcja zmieniłaby elementy własnej kopii wektora. Bez `&` w zmiennej pętli zmieniłaby kopie elementów.
4. Bo reguła rozliczenia jednego roweru powinna być w jednym miejscu. Funkcja dla floty organizuje tylko pracę nad kolekcją. Gdyby reguła się zmieniła, wystarczy poprawić jedną funkcję.
5. Bo wynik ma mówić, ile rekordów naprawdę się zmieniło. Rower bez oczekujących przejazdów zostaje bez zmian, więc nie jest liczony. Licznik zwiększany w każdym przebiegu policzyłby po prostu wszystkie rowery, czyli to samo co `size()`.
6. Nie. Pętla odwiedza istniejące elementy po kolei i może zmieniać ich pola, ale nie dodaje, nie usuwa ani nie przestawia elementów.
7. Pętla wykonuje zero przebiegów, nic się nie zmienia, a funkcja zwraca początkową wartość licznika, czyli 0. Pusty wektor to poprawne dane, a funkcja nie odczytuje żadnego elementu.
8. Bo pierwsze rozliczenie zmieniło elementy tego samego wektora i wyzerowało oczekujące przejazdy. Wynik 3 oznaczałby, że przejazdy zostały doliczone drugi raz albo że pierwsze rozliczenie zmieniało kopie.
9. Funkcja dla jednego roweru naprawdę zmienia obiekt, który dostaje, i zgłasza zmianę, ale dostaje kopię elementu. Licznik rośnie, a element w wektorze zostaje stary. Gdy żaden rower nie ma oczekujących przejazdów, obie wersje niczego nie zmieniają i zwracają 0, więc wyglądają tak samo.
10. Zmiana istniejącego wektora pasuje, gdy kolekcja przedstawia bieżący stan, a poprzedni nie jest potrzebny, jak flota po rozliczeniu. Nowy wektor pasuje, gdy oryginał ma zostać bez zmian albo wynik to inna kolekcja, na przykład wybrane elementy, jak w lekcji 6.5. To dwie różne umowy, a nie lepsza i gorsza wersja.

</details>

## Podsumowanie

- Pętla `for (Product& product : products)` daje w każdym przebiegu dostęp do prawdziwego elementu wektora, z możliwością zmiany.
- Funkcja z parametrem `std::vector<Product>&` może zmieniać elementy istniejącego wektora wywołującego. Do samego odczytu wystarcza `const std::vector<Product>&`.
- Zmiana musi przejść przez `&` na obu poziomach: wektora i elementu. Zmienna pętli bez `&` jest kopią, a jej zmiana nie dotyczy wektora.
- Funkcja dla jednego rekordu zawiera regułę, a funkcja dla kolekcji wywołuje ją dla każdego elementu i liczy rzeczywiste zmiany.
- Pętla nie zmienia liczby ani kolejności elementów. Dla pustego wektora wykonuje zero przebiegów.

## Co dalej

W tej lekcji funkcja przeglądała wszystkie rekordy i zmieniała te, które wymagały zmiany. W kolejnej lekcji funkcja znajdzie w wektorze jeden rekord po wartości pola i zmieni tylko jego. Jest w przygotowaniu.

---

## Przykładowe rozwiązania

Zajrzyj tutaj **po własnej próbie**. Twoje nazwy mogą się różnić, jeśli standardowe wyjście jest takie, jak wymagane.

<details>
<summary>Punkt 6: misja, rozliczenie rowerów miejskich</summary>

<!-- example: city_bikes -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>
#include <vector>

struct Bike {
    std::string id;
    int total_rides;
    int pending_rides;
};

bool settle_bike(Bike& bike) {
    if (bike.pending_rides <= 0) {
        return false;
    }

    bike.total_rides += bike.pending_rides;
    bike.pending_rides = 0;
    return true;
}

std::size_t settle_fleet(std::vector<Bike>& bikes) {
    std::size_t updated{0};

    for (Bike& bike : bikes) {
        if (settle_bike(bike)) {
            ++updated;
        }
    }

    return updated;
}

int main() {
    std::vector<Bike> bikes{
        {"B-01", 12, 3},
        {"B-02", 7, 0},
        {"B-03", 20, 2},
        {"B-04", 0, 1}
    };

    std::cout << "Bikes: " << bikes.size() << "\n";
    std::cout << "Before:\n";

    for (const Bike& bike : bikes) {
        std::cout << bike.id << ": total " << bike.total_rides << ", pending " << bike.pending_rides << "\n";
    }

    const std::size_t updated{settle_fleet(bikes)};
    const std::size_t updated_again{settle_fleet(bikes)};

    std::cout << "Updated: " << updated << "\n";
    std::cout << "Updated again: " << updated_again << "\n";
    std::cout << "After:\n";

    for (const Bike& bike : bikes) {
        std::cout << bike.id << ": total " << bike.total_rides << ", pending " << bike.pending_rides << "\n";
    }
}
```

1. **Wektor bez `const`,** bo rozliczenie ma zmienić jego elementy.
2. **Parametr wektora z `&`,** bo funkcja ma zmienić flotę z `main`, a nie własną kopię.
3. **Zmienna pętli z `&`,** bo funkcja dla jednego roweru ma dostać prawdziwy element wektora, a nie kopię.
4. **Oba poziomy są potrzebne:** bez pierwszego zmieniłaby się kopia wektora, bez drugiego kopie elementów. W obu przypadkach flota w `main` zostałaby stara.
5. **`bool` dla jednego roweru,** bo odpowiedź brzmi „zmieniony” albo „bez zmian”, a funkcja dla floty potrzebuje jej do licznika.
6. **Liczba dla floty, w typie `std::size_t`,** bo wynikiem jest liczba rekordów, jak w lekcji 8.4.
7. **Bez liczenia rowerów bez zmian,** bo wynik ma mówić, ile rekordów naprawdę się zmieniło.
8. **Kopia elementu nie wystarcza,** bo zmiana kopii znika po przebiegu pętli, a element w wektorze zostaje stary (punkt 7).
9. **Identyfikator się nie zmienia,** bo funkcja dla jednego roweru go nie dotyka.
10. **Tylko dodatnia liczba oczekujących przejazdów,** bo przy zerze nie ma czego rozliczać, a rekord ma zostać bez zmian. Kolejność zmian ma znaczenie: najpierw dodanie do historii, potem wyzerowanie.
11. **Drugie rozliczenie zwraca 0,** bo pierwsze zmieniło elementy tego samego wektora i wyzerowało wszystkie oczekujące przejazdy.
12. **Pusty wektor działa** bez osobnego warunku: pętle wykonują zero przebiegów, a funkcja zwraca początkową wartość licznika, czyli 0.
13. **Różne referencje do odczytu i do zmiany:** wypisywanie tylko czyta, więc używa `const Bike&`, a rozliczenie zmienia, więc używa `Bike&`. Każda pętla dostaje tylko te uprawnienia, których potrzebuje.
14. **Bez wyszukiwania po identyfikatorze,** bo rozliczenie dotyczy każdego roweru, a nie jednego wybranego.
15. **Inaczej niż w lekcji 6.5:** `keep_negative` zostawiała oryginał bez zmian i zwracała nowy wektor z wybranymi elementami. Tutaj flota ma pokazywać bieżący stan, więc zmieniamy jej istniejące elementy. Gdyby trzeba było zachować stan sprzed rozliczenia, lepsza byłaby kopia wektora albo funkcja zwracająca nowy.

**Inne poprawne rozwiązania:**

- warunek `bike.pending_rides == 0` zamiast `<= 0`, bo dane są nieujemne;
- wynik funkcji dla jednego roweru zapisany w zmiennej `const bool` przed `if`, jak w lekcji 9.2;
- oba wyniki rozliczenia wypisane od razu po każdym wywołaniu, jeśli kolejność linijek zostaje taka sama.

**Pusta flota:** ten sam program z `std::vector<Bike> bikes{};` w miejscu wektora z czterema rowerami.

<!-- example: city_bikes_empty -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>
#include <vector>

struct Bike {
    std::string id;
    int total_rides;
    int pending_rides;
};

bool settle_bike(Bike& bike) {
    if (bike.pending_rides <= 0) {
        return false;
    }

    bike.total_rides += bike.pending_rides;
    bike.pending_rides = 0;
    return true;
}

std::size_t settle_fleet(std::vector<Bike>& bikes) {
    std::size_t updated{0};

    for (Bike& bike : bikes) {
        if (settle_bike(bike)) {
            ++updated;
        }
    }

    return updated;
}

int main() {
    std::vector<Bike> bikes{};

    std::cout << "Bikes: " << bikes.size() << "\n";
    std::cout << "Before:\n";

    for (const Bike& bike : bikes) {
        std::cout << bike.id << ": total " << bike.total_rides << ", pending " << bike.pending_rides << "\n";
    }

    const std::size_t updated{settle_fleet(bikes)};
    const std::size_t updated_again{settle_fleet(bikes)};

    std::cout << "Updated: " << updated << "\n";
    std::cout << "Updated again: " << updated_again << "\n";
    std::cout << "After:\n";

    for (const Bike& bike : bikes) {
        std::cout << bike.id << ": total " << bike.total_rides << ", pending " << bike.pending_rides << "\n";
    }
}
```

**Program kontrolny** sprawdza wszystkie przypadki z listy kontrolnej. Typ i obie funkcje są takie same jak wyżej, a raport od wypisania liczby rowerów też, poza wcięciem. Różnica jest jedna: wektor nie jest zapisany w kodzie, tylko powstaje z wejścia. Program odczytuje liczbę rowerów, a potem każdy rower: identyfikator i dwie liczby. Każdy odczytany rower trafia na koniec wektora przez `push_back`, jak w programach kontrolnych lekcji 8.4–8.6. Misja nie potrzebuje ani wejścia, ani `push_back`.

<!-- example: city_bikes_check -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>
#include <vector>

struct Bike {
    std::string id;
    int total_rides;
    int pending_rides;
};

bool settle_bike(Bike& bike) {
    if (bike.pending_rides <= 0) {
        return false;
    }

    bike.total_rides += bike.pending_rides;
    bike.pending_rides = 0;
    return true;
}

std::size_t settle_fleet(std::vector<Bike>& bikes) {
    std::size_t updated{0};

    for (Bike& bike : bikes) {
        if (settle_bike(bike)) {
            ++updated;
        }
    }

    return updated;
}

int main() {
    std::vector<Bike> bikes{};
    int count{0};

    std::cin >> count;

    for (int number{1}; number <= count; ++number) {
        std::string id{};
        int total_rides{0};
        int pending_rides{0};

        std::cin >> id;
        std::cin >> total_rides;
        std::cin >> pending_rides;

        const Bike bike{id, total_rides, pending_rides};
        bikes.push_back(bike);
    }

    if (std::cin.fail()) {
        std::cout << "Input could not be read\n";
    } else {
        std::cout << "Bikes: " << bikes.size() << "\n";
        std::cout << "Before:\n";

        for (const Bike& bike : bikes) {
            std::cout << bike.id << ": total " << bike.total_rides << ", pending " << bike.pending_rides << "\n";
        }

        const std::size_t updated{settle_fleet(bikes)};
        const std::size_t updated_again{settle_fleet(bikes)};

        std::cout << "Updated: " << updated << "\n";
        std::cout << "Updated again: " << updated_again << "\n";
        std::cout << "After:\n";

        for (const Bike& bike : bikes) {
            std::cout << bike.id << ": total " << bike.total_rides << ", pending " << bike.pending_rides << "\n";
        }
    }
}
```

Każdy przypadek zaczyna się od liczby rowerów. Potem każdy rower zajmuje jedną linijkę: identyfikator, łączna liczba przejazdów i liczba oczekujących. Przypadki stoją w kolejności z listy kontrolnej, od A do J.

<!-- input: city_bikes_check -->
```text
4
B-01 12 3
B-02 7 0
B-03 20 2
B-04 0 1
```

<!-- output: city_bikes_check -->
```text
Bikes: 4
Before:
B-01: total 12, pending 3
B-02: total 7, pending 0
B-03: total 20, pending 2
B-04: total 0, pending 1
Updated: 3
Updated again: 0
After:
B-01: total 15, pending 0
B-02: total 7, pending 0
B-03: total 22, pending 0
B-04: total 1, pending 0
```

<!-- input: city_bikes_check -->
```text
0
```

<!-- output: city_bikes_check -->
```text
Bikes: 0
Before:
Updated: 0
Updated again: 0
After:
```

<!-- input: city_bikes_check -->
```text
1
C-01 5 0
```

<!-- output: city_bikes_check -->
```text
Bikes: 1
Before:
C-01: total 5, pending 0
Updated: 0
Updated again: 0
After:
C-01: total 5, pending 0
```

<!-- input: city_bikes_check -->
```text
1
D-01 4 6
```

<!-- output: city_bikes_check -->
```text
Bikes: 1
Before:
D-01: total 4, pending 6
Updated: 1
Updated again: 0
After:
D-01: total 10, pending 0
```

<!-- input: city_bikes_check -->
```text
3
E-01 3 0
E-02 0 0
E-03 9 0
```

<!-- output: city_bikes_check -->
```text
Bikes: 3
Before:
E-01: total 3, pending 0
E-02: total 0, pending 0
E-03: total 9, pending 0
Updated: 0
Updated again: 0
After:
E-01: total 3, pending 0
E-02: total 0, pending 0
E-03: total 9, pending 0
```

<!-- input: city_bikes_check -->
```text
3
F-01 1 2
F-02 5 5
F-03 0 4
```

<!-- output: city_bikes_check -->
```text
Bikes: 3
Before:
F-01: total 1, pending 2
F-02: total 5, pending 5
F-03: total 0, pending 4
Updated: 3
Updated again: 0
After:
F-01: total 3, pending 0
F-02: total 10, pending 0
F-03: total 4, pending 0
```

<!-- input: city_bikes_check -->
```text
2
G-01 6 2
G-02 6 2
```

<!-- output: city_bikes_check -->
```text
Bikes: 2
Before:
G-01: total 6, pending 2
G-02: total 6, pending 2
Updated: 2
Updated again: 0
After:
G-01: total 8, pending 0
G-02: total 8, pending 0
```

<!-- input: city_bikes_check -->
```text
4
B-04 0 1
B-03 20 2
B-02 7 0
B-01 12 3
```

<!-- output: city_bikes_check -->
```text
Bikes: 4
Before:
B-04: total 0, pending 1
B-03: total 20, pending 2
B-02: total 7, pending 0
B-01: total 12, pending 3
Updated: 3
Updated again: 0
After:
B-04: total 1, pending 0
B-03: total 22, pending 0
B-02: total 7, pending 0
B-01: total 15, pending 0
```

<!-- input: city_bikes_check -->
```text
3
I-01 2 0
I-02 3 0
I-03 1 7
```

<!-- output: city_bikes_check -->
```text
Bikes: 3
Before:
I-01: total 2, pending 0
I-02: total 3, pending 0
I-03: total 1, pending 7
Updated: 1
Updated again: 0
After:
I-01: total 2, pending 0
I-02: total 3, pending 0
I-03: total 8, pending 0
```

<!-- input: city_bikes_check -->
```text
3
J-01 4 5
J-02 6 0
J-03 8 0
```

<!-- output: city_bikes_check -->
```text
Bikes: 3
Before:
J-01: total 4, pending 5
J-02: total 6, pending 0
J-03: total 8, pending 0
Updated: 1
Updated again: 0
After:
J-01: total 9, pending 0
J-02: total 6, pending 0
J-03: total 8, pending 0
```

</details>

<details>
<summary>Punkt 7: wyniki przed poprawką i poprawiony program</summary>

Przed poprawką, dla floty bez oczekujących przejazdów:

<!-- output: fleet_copy_bug -->
```text
Bikes: 3
Before:
B-01: total 12, pending 0
B-02: total 7, pending 0
B-03: total 20, pending 0
Updated: 0
Updated again: 0
After:
B-01: total 12, pending 0
B-02: total 7, pending 0
B-03: total 20, pending 0
```

- **Dla takiej floty wynik jest poprawny,** bo żaden rower nie wymaga rozliczenia. Poprawna wersja też zwraca 0 i niczego nie zmienia.
- **Dane, które ujawniają błąd:** każda flota z co najmniej jednym rowerem z dodatnią liczbą oczekujących przejazdów. Na przykład `B-01` z 3 oczekującymi przejazdami. Poprawny wynik to `Updated: 1`, `Updated again: 0` i `B-01: total 15, pending 0`. Program z błędem wypisuje:

<!-- example: fleet_copy_revealed -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>
#include <vector>

struct Bike {
    std::string id;
    int total_rides;
    int pending_rides;
};

bool settle_bike(Bike& bike) {
    if (bike.pending_rides <= 0) {
        return false;
    }

    bike.total_rides += bike.pending_rides;
    bike.pending_rides = 0;
    return true;
}

std::size_t settle_fleet(std::vector<Bike>& bikes) {
    std::size_t updated{0};

    for (Bike bike : bikes) {
        if (settle_bike(bike)) {
            ++updated;
        }
    }

    return updated;
}

int main() {
    std::vector<Bike> bikes{
        {"B-01", 12, 3},
        {"B-02", 7, 0},
        {"B-03", 20, 0}
    };

    std::cout << "Bikes: " << bikes.size() << "\n";
    std::cout << "Before:\n";

    for (const Bike& bike : bikes) {
        std::cout << bike.id << ": total " << bike.total_rides << ", pending " << bike.pending_rides << "\n";
    }

    const std::size_t updated{settle_fleet(bikes)};
    const std::size_t updated_again{settle_fleet(bikes)};

    std::cout << "Updated: " << updated << "\n";
    std::cout << "Updated again: " << updated_again << "\n";
    std::cout << "After:\n";

    for (const Bike& bike : bikes) {
        std::cout << bike.id << ": total " << bike.total_rides << ", pending " << bike.pending_rides << "\n";
    }
}
```

<!-- output: fleet_copy_revealed -->
```text
Bikes: 3
Before:
B-01: total 12, pending 3
B-02: total 7, pending 0
B-03: total 20, pending 0
Updated: 1
Updated again: 1
After:
B-01: total 12, pending 3
B-02: total 7, pending 0
B-03: total 20, pending 0
```

| Chwila | `bike` w pętli (kopia) | `B-01` w wektorze |
|---|---|---|
| przed pierwszym rozliczeniem | nie istnieje | total 12, pending 3 |
| pierwszy przebieg, po `settle_bike(bike)` | total 15, pending 0; licznik 1 | total 12, pending 3 |
| po pierwszym rozliczeniu | nie istnieje | total 12, pending 3 |
| drugie rozliczenie | ta sama sytuacja: nowa kopia, licznik znowu 1 | total 12, pending 3 |

- **Gdzie powstają kopie:** w pętli `for (Bike bike : bikes)`. W każdym przebiegu `bike` to nowy obiekt z wartościami bieżącego elementu.
- **Funkcja dla jednego roweru działa poprawnie:** zmienia obiekt, który dostaje, i zgłasza zmianę. Dostaje jednak kopię, więc licznik rośnie, a element w wektorze zostaje stary. Funkcja dla floty łamie swoją umowę: zgłasza zmienione rekordy, których w danych nie ma.
- **Licznik nie dowodzi skutku.** Program raportuje wykonaną operację, choć przechowywane dane się nie zmieniły. Dopiero `After` i drugie rozliczenie pokazują problem.
- **Poprawka:** zmienna pętli `Bike& bike`. Kompilator nie zgłasza błędu w wersji z kopią, bo to poprawny C++: zmiana kopii jest dozwolona, tylko nie pasuje do zadania funkcji.

<!-- example: fleet_copy_fixed -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>
#include <vector>

struct Bike {
    std::string id;
    int total_rides;
    int pending_rides;
};

bool settle_bike(Bike& bike) {
    if (bike.pending_rides <= 0) {
        return false;
    }

    bike.total_rides += bike.pending_rides;
    bike.pending_rides = 0;
    return true;
}

std::size_t settle_fleet(std::vector<Bike>& bikes) {
    std::size_t updated{0};

    for (Bike& bike : bikes) {
        if (settle_bike(bike)) {
            ++updated;
        }
    }

    return updated;
}

int main() {
    std::vector<Bike> bikes{
        {"B-01", 12, 3},
        {"B-02", 7, 0},
        {"B-03", 20, 0}
    };

    std::cout << "Bikes: " << bikes.size() << "\n";
    std::cout << "Before:\n";

    for (const Bike& bike : bikes) {
        std::cout << bike.id << ": total " << bike.total_rides << ", pending " << bike.pending_rides << "\n";
    }

    const std::size_t updated{settle_fleet(bikes)};
    const std::size_t updated_again{settle_fleet(bikes)};

    std::cout << "Updated: " << updated << "\n";
    std::cout << "Updated again: " << updated_again << "\n";
    std::cout << "After:\n";

    for (const Bike& bike : bikes) {
        std::cout << bike.id << ": total " << bike.total_rides << ", pending " << bike.pending_rides << "\n";
    }
}
```

<!-- output: fleet_copy_fixed -->
```text
Bikes: 3
Before:
B-01: total 12, pending 3
B-02: total 7, pending 0
B-03: total 20, pending 0
Updated: 1
Updated again: 0
After:
B-01: total 15, pending 0
B-02: total 7, pending 0
B-03: total 20, pending 0
```

Dla floty bez oczekujących przejazdów poprawiony program wypisuje to samo co przed poprawką. Dlatego taka flota nie wystarczy, żeby sprawdzić, czy pętla zmienia elementy wektora.

</details>

**Poprzednia lekcja:** [Lekcja 9.2: Zmiana tylko po spełnieniu warunków](lesson_02_a_change_only_when_allowed.md) · **Następna lekcja:** w przygotowaniu · [Opis kursu](../../README.md)

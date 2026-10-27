# Lekcja 8.4: Wiele rekordów w `std::vector`

**Polski** · [English](lesson_04_many_records_in_a_vector.en.md) · [Opis kursu](../../README.md)

> **Moduł 8, lekcja 4** · około 65–80 minut
> **Potrzebujesz:** katalogu `cpp-workspace` i oryginalnego projektu `lesson_05_first_program`, jak dotąd. Debugger nie jest w tej lekcji potrzebny.
> **Wersja pilotażowa.** Programy z tej lekcji sprawdzamy automatycznie na Windowsie, Ubuntu i macOS. Żaden z nich nie pyta o dane: wszystkie wartości są zapisane w kodzie. Dane z wejścia odczytuje tylko program kontrolny w części z rozwiązaniami.

## Zanim zaczniesz

Ta lekcja zakłada, że:

- przechowujesz liczby w `std::vector<int>`, przeglądasz je pętlą zakresową i sprawdzasz `size()` oraz `empty()` (lekcje 6.1 i 6.2);
- wiesz, że liczby elementów mają typ `std::size_t`, który nie przyjmuje wartości ujemnych (lekcja 6.3);
- przekazujesz wektor do funkcji przez `const std::vector<int>&` (lekcja 6.4);
- definiujesz strukturę, tworzysz jej obiekty z wartościami wszystkich pól w `{}` (lekcja 8.1) i kopię rekordu zapisem `Product copy{original};` (lekcja 8.2);
- piszesz funkcje, które dostają rekord przez `const Product&` i zwracają `int` albo `bool` (lekcja 8.3).

## Sytuacja

W lekcji 8.3 funkcja `stock_value` obliczała wartość zapasu jednego produktu i działała dla każdego produktu, który dostała. Co zrobić, jeżeli magazyn ma kilkanaście produktów, a potrzebna jest łączna wartość zapasu? Osobna zmienna i osobne wywołanie dla każdego produktu to dużo powtórzeń, a każdy nowy produkt to kolejne linijki kodu.

Ten problem znasz z Modułu 6: wiele liczb trzymał tam jeden `std::vector<int>`. Ten sam `std::vector` może przechowywać elementy naszego własnego typu. Wtedy **każdy element to cały rekord** z kilkoma powiązanymi danymi. To nie jest nowy rodzaj kolekcji: zmienia się tylko typ elementów.

Po tej lekcji będziesz:

- tworzyć wektor rekordów i inicjalizować go zagnieżdżonymi klamrami;
- przeglądać rekordy pętlą `for (const Product& product : products)` i odczytywać ich pola;
- wyjaśniać, dlaczego zmienna pętli nie kopiuje kolejnych rekordów;
- pisać funkcję, która dostaje cały wektor rekordów i korzysta z funkcji dla jednego rekordu;
- poprawnie obsługiwać pusty wektor i wektor z jednym rekordem;
- dobierać dane, które ujawniają niezgodność między oceną rekordów a podsumowaniem.

## 1. Przygotuj projekt

W `cpp-workspace` utwórz katalog `lesson_8_4` i skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program`. Programy z punktów 2 i 5 wpisujesz w `main.cpp` tego katalogu. Typ `Product` pochodzi z lekcji 8.1 i 8.3.

## 2. Wektor rekordów

<!-- example: product_names -->
```cpp
#include <iostream>
#include <string>
#include <vector>

struct Product {
    std::string name;
    int stock;
    int minimum;
    int unit_price;
};

int main() {
    const std::vector<Product> products{
        {"Tea", 3, 8, 6},
        {"Rice", 8, 8, 4},
        {"Pens", 10, 7, 2}
    };

    for (const Product& product : products) {
        std::cout << product.name << "\n";
    }
}
```

Wpisz program i **przewidź**, co wypisze. Uruchamiać go nie musisz: w punkcie 5 rozbudujesz go i wtedy uruchomisz.

<details>
<summary>Standardowe wyjście</summary>

<!-- output: product_names -->
```text
Tea
Rice
Pens
```

</details>

| Zapis | Znaczenie |
|---|---|
| `std::vector<Product>` | wektor, którego elementy mają typ `Product`, jak elementy `std::vector<int>` miały typ `int` |
| zewnętrzna para klamer | obejmuje wszystkie elementy wektora, jak `{3, 7, 5, 9}` w lekcji 6.1 |
| `{"Tea", 3, 8, 6}` | wewnętrzna para klamer: jeden rekord, z wartościami w kolejności pól, jak w lekcji 8.1 |
| przecinki między wewnętrznymi parami | oddzielają kolejne rekordy |

- **Każdy rekord ma wartości wszystkich czterech pól,** jak każdy obiekt w lekcjach 8.1–8.3.
- **`products.size()` to liczba rekordów,** tutaj 3, a `products.empty()` daje `false`. Rekord liczy się jako jeden element, choć ma cztery pola.
- **`const`,** bo program nie zmienia ani wektora, ani rekordów w nim.
- **Jeden obiekt `Product` opisuje jeden produkt, a `products` to kolekcja produktów.** Nazwy dobieramy jak w lekcji 6.1: wektor w liczbie mnogiej, element w pojedynczej.

## 3. Pętla po rekordach

Pętlę `for (const Product& product : products)` czytaj: „dla każdego produktu z `products`”.

| Część | Znaczenie |
|---|---|
| `const Product& product` | zmienna pętli: w każdym przebiegu odnosi się do kolejnego elementu wektora |
| `:` i `products` | jak w lekcji 6.1: wektor, którego elementy pętla przegląda |
| `product.name` | pole `name` bieżącego elementu |

- W pierwszym przebiegu `product` odnosi się do rekordu `Tea`, w drugim do `Rice`, a w trzecim do `Pens`. Kolejność przebiegów to kolejność rekordów w wektorze.
- **`&`:** zmienna pętli to inna nazwa istniejącego elementu, a nie jego kopia. To ten sam model co parametr `const Product&` w lekcji 8.3.
- **`const`:** przez `product` elementu nie zmienisz.

## 4. Dlaczego `const Product&`?

| Zapis | Co się dzieje |
|---|---|
| `int stock_value(const Product& product)` | parametr odnosi się do obiektu z miejsca wywołania (lekcja 8.3) |
| `for (const Product& product : products)` | zmienna pętli odnosi się kolejno do elementów wektora |
| `Product copy{original};` | powstaje nowy obiekt z kopią wartości wszystkich pól (lekcja 8.2) |

W dwóch pierwszych wierszach model jest ten sam: `const Product&` daje dostęp do istniejącego rekordu, tylko do odczytu i bez kopii. Nowy obiekt powstaje tylko w trzecim.

W lekcji 6.4 zmienna pętli `const int temperature` kopiowała jedną liczbę, a taka kopia jest tania. Rekord to kilka pól, w tym tekst. **Pętla `for (const Product product : products)`, bez `&`, też jest poprawnym C++,** ale jej zmienna jest w każdym przebiegu osobną kopią elementu, razem z tekstem z pola `std::string`. Przy samym odczycie ta kopia nie jest potrzebna, dlatego wybieramy `const Product&`. W Twoim projekcie taka pętla zbuduje się bez komunikatu, choć kompilator z włączonymi dodatkowymi ostrzeżeniami może o tej kopii przypomnieć.

## 5. Funkcja dla całego wektora

Rozbuduj program z punktu 2: dopisz przed `main` dwie funkcje i zmień `main` tak jak niżej. Funkcja `stock_value` jest taka sama jak w lekcji 8.3.

<!-- example: stock_total -->
```cpp
#include <iostream>
#include <string>
#include <vector>

struct Product {
    std::string name;
    int stock;
    int minimum;
    int unit_price;
};

int stock_value(const Product& product) {
    return product.stock * product.unit_price;
}

int total_stock_value(const std::vector<Product>& products) {
    int total{0};

    for (const Product& product : products) {
        total += stock_value(product);
    }

    return total;
}

int main() {
    const std::vector<Product> products{
        {"Tea", 3, 8, 6},
        {"Rice", 8, 8, 4},
        {"Pens", 10, 7, 2}
    };

    std::cout << "Products: " << products.size() << "\n";
    std::cout << "Total stock value: " << total_stock_value(products) << "\n";
}
```

**Przewidź** obie linijki, a potem uruchom program.

<details>
<summary>Standardowe wyjście</summary>

<!-- output: stock_total -->
```text
Products: 3
Total stock value: 70
```

</details>

- **`total_stock_value` dostaje cały wektor** przez `const std::vector<Product>&`, jak `count_cold_days` w lekcji 6.4. Tylko elementami są teraz rekordy.
- **`total`** to akumulator z lekcji 4.2: zaczyna od 0, a pętla dodaje do niego kolejne wartości.
- **Pętla bierze rekordy przez `const Product&` i dla każdego wywołuje `stock_value`:** 18, 32 i 20. Wzór `stock * unit_price` stoi w programie tylko raz.
- **Funkcja zwraca jedną liczbę** i niczego nie wypisuje. `main` wypisuje liczbę rekordów prosto z `size()` i wynik funkcji.

| Funkcja | Dostaje | Zwraca |
|---|---|---|
| `stock_value` | jeden rekord: `const Product&` | wartość zapasu jednego produktu |
| `total_stock_value` | cały wektor: `const std::vector<Product>&` | sumę wartości zapasu wszystkich produktów |

**Jedna funkcja zna regułę dla jednego elementu, a druga organizuje analizę całej kolekcji.** Gdyby wartość zapasu liczyło się inaczej, zmienisz tylko `stock_value`, a `total_stock_value` od razu skorzysta z nowej reguły.

## 6. Pusty wektor i jeden rekord

<!-- fragment -->
```cpp
const std::vector<Product> no_products{};
const std::vector<Product> one_product{
    {"Tea", 3, 8, 6}
};
```

**Przewidź**, ile przebiegów wykona pętla w `total_stock_value` dla każdego z tych wektorów i jaki wynik zwróci funkcja.

<details>
<summary>Program, który sprawdza oba przypadki</summary>

<!-- example: stock_total_small -->
```cpp
#include <iostream>
#include <string>
#include <vector>

struct Product {
    std::string name;
    int stock;
    int minimum;
    int unit_price;
};

int stock_value(const Product& product) {
    return product.stock * product.unit_price;
}

int total_stock_value(const std::vector<Product>& products) {
    int total{0};

    for (const Product& product : products) {
        total += stock_value(product);
    }

    return total;
}

int main() {
    const std::vector<Product> no_products{};
    const std::vector<Product> one_product{
        {"Tea", 3, 8, 6}
    };

    if (no_products.empty()) {
        std::cout << "No products\n";
    }

    std::cout << "Total stock value: " << total_stock_value(no_products) << "\n";
    std::cout << "Products: " << one_product.size() << "\n";
    std::cout << "Total stock value: " << total_stock_value(one_product) << "\n";
}
```

<!-- output: stock_total_small -->
```text
No products
Total stock value: 0
Products: 1
Total stock value: 18
```

</details>

- **Pusty wektor to poprawne dane, a nie błąd.** Pętla wykona zero przebiegów, więc funkcja zwróci początkową wartość akumulatora, czyli 0, jak `count_cold_days` dla pustego wektora w lekcji 6.4. Nie potrzeba specjalnego warunku ani kodu błędu. Z pustego wektora nie odczytujemy żadnego elementu.
- **W wektorze z jednym rekordem** nadal są dwie pary klamer: zewnętrzna dla wektora i wewnętrzna dla rekordu. Pętla wykona jeden przebieg.

## 7. Misja: które wydania są gotowe?

Zespół przygotowuje kilka wydań programu. To uproszczony model, bez prawdziwych narzędzi i systemów. Program sprawdza, które wydania są gotowe.

**Dane:**

| Nazwa | Kontrole zakończone | Kontrole wymagane | Blokada |
|---|---:|---:|---|
| `Core` | 5 | 5 | nie |
| `Mobile` | 4 | 5 | nie |
| `Docs` | 3 | 3 | tak |
| `Tools` | 2 | 2 | nie |
| `API` | 1 | 2 | tak |

**Reguły:**

- Liczba wymaganych kontroli wynosi od 1 do 20. Liczba zakończonych kontroli jest nieujemna i nie przekracza liczby wymaganych. Program nie sprawdza tych założeń: dane są wpisane w kodzie.
- Wydanie jest **gotowe**, gdy jednocześnie wszystkie wymagane kontrole są zakończone **i** wydanie nie jest zablokowane.
- Wydanie z zakończonymi kontrolami, ale zablokowane, nie jest gotowe. Wydanie bez blokady, ale z niezakończonymi kontrolami, też nie. Nazwa nie wpływa na ocenę.

**Wymagania:**

- Program definiuje własny typ z czterema polami: nazwą wydania (tekst), liczbą zakończonych kontroli i liczbą wymaganych kontroli (liczby całkowite) oraz informacją o blokadzie (tak albo nie). Nazwy typu i pól oraz ich typy w C++ wybierasz samodzielnie.
- Wszystkie wydania są elementami jednego wektora `const`, zainicjalizowanego w kodzie w kolejności z tabeli. Bez osobnych zmiennych na każde wydanie i bez `push_back`.
- Program ma dwie własne funkcje. Pierwsza dostaje jedno wydanie przez `const&` i ustala, czy jest gotowe. Druga dostaje cały wektor przez `const&`, przegląda wydania przez `const&`, korzysta z pierwszej funkcji i zwraca liczbę gotowych wydań. Żadna nie zmienia danych, niczego nie wypisuje ani nie odczytuje z wejścia. Nazwy funkcji i parametrów oraz typy wyników wybierasz samodzielnie.
- `main` tworzy wektor, odczytuje liczbę wydań przez `size()`, wypisuje status każdego wydania na podstawie pierwszej funkcji, wywołuje drugą funkcję, oblicza liczbę niegotowych wydań jako różnicę i wypisuje podsumowanie.
- Program wypisuje najpierw `Releases: N`, potem po jednej linijce `NAZWA: ready` albo `NAZWA: not ready` dla każdego wydania, w kolejności z wektora, a na końcu `Ready: N` i `Not ready: N`. Nie wypisuje nic więcej, także wartości pól.

W `cpp-workspace` utwórz katalog `release_review`, skopiuj do niego `CMakeLists.txt` z oryginalnego `lesson_05_first_program`, utwórz pusty `main.cpp` i napisz program samodzielnie.

Dla danych powyżej standardowe wyjście ma być takie:

<!-- output: release_review -->
```text
Releases: 5
Core: ready
Mobile: not ready
Docs: not ready
Tools: ready
API: not ready
Ready: 2
Not ready: 3
```

Gotowe są `Core` i `Tools`. `Mobile` nie ma wszystkich kontroli, `Docs` jest zablokowane, a `API` ma obie przeszkody.

**To nie jest program o produktach z innymi nazwami.** Musisz samodzielnie zdecydować:

1. jak nazwać typ, jego pola i obie funkcje oraz jakie typy mają pola i wyniki funkcji;
2. które klamry należą do wektora, a które do rekordu;
3. jak połączyć dwa warunki gotowości w funkcji dla jednego wydania;
4. jak funkcja dla całego wektora skorzysta z funkcji dla jednego wydania;
5. co program wypisze dla pustego wektora;
6. jak wypisać status każdego wydania w kolejności z wektora;
7. jak obliczyć liczbę niegotowych wydań, nie powtarzając reguły gotowości.

**Zanim napiszesz program**, przygotuj tabelę przypadków: pusty wektor, jedno gotowe wydanie, jedno zablokowane, jedno z niezakończonymi kontrolami, same gotowe, same niegotowe i dwa wydania z tymi samymi liczbami kontroli, ale różną blokadą. Przy każdym zapisz statusy wydań oraz `Ready` i `Not ready`.

**Potem** uruchom program dla danych z wymagań i dla pustego wektora. Zmieniaj przy tym tylko zawartość klamer wektora. Wszystkie przypadki z pełnej listy kontrolnej są sprawdzone automatycznie.

### Kryterium sukcesu

- Program buduje się jako C++20 i dla danych z wymagań wypisuje dokładnie osiem linijek pokazanych wyżej.
- Jest jeden typ z czterema polami i jeden wektor `const` z pięcioma rekordami, zainicjalizowany w kodzie.
- Obie funkcje dostają dane przez `const&`, niczego nie wypisują ani nie zmieniają, a reguła gotowości stoi w jednym miejscu: funkcja dla wektora i `main` korzystają z funkcji dla jednego wydania.
- Dla pustego wektora program wypisuje `Releases: 0`, `Ready: 0` i `Not ready: 0`, bez linijek z nazwami.
- Statusy stoją w kolejności z wektora, a każde wydanie pojawia się dokładnie raz.
- Tabela przypadków powstała przed uruchomieniem programu.
- Umiesz wskazać, które klamry należą do wektora, a które do rekordu.

Gdy wynik się zgadza, możesz zapisać projekt w Gicie, jak w lekcji 1.5.

<details>
<summary>Podpowiedź 1</summary>

Jak przechowywać kilka wydań, z których każde ma własną nazwę, liczby kontroli i informację o blokadzie?

</details>

<details>
<summary>Podpowiedź 2</summary>

Jedna funkcja może ocenić pojedynczy rekord. Druga może przejrzeć cały wektor i policzyć, ile rekordów spełnia tę samą regułę.

</details>

<details>
<summary>Podpowiedź 3</summary>

Nie duplikuj warunku gotowości w kilku miejscach. W pętli po wektorze korzystaj z funkcji dla pojedynczego rekordu i pamiętaj o pustej kolekcji.

</details>

<details>
<summary>Pełna lista przypadków kontrolnych: otwórz po przygotowaniu własnej tabeli</summary>

Zapis `3/5` oznacza 3 zakończone z 5 wymaganych kontroli.

| | Wydania | Gotowe | Ready | Not ready | Co sprawdza |
|---|---|---|---:|---:|---|
| A | dane z wymagań | `Core`, `Tools` | 2 | 3 | dane z wymagań |
| B | brak wydań | brak, bez linijek z nazwami | 0 | 0 | pusty wektor |
| C | `Solo` 3/3 | `Solo` | 1 | 0 | jedno gotowe wydanie |
| D | `Beta` 2/3 | brak | 0 | 1 | jedno wydanie z niezakończonymi kontrolami |
| E | `Lock` 3/3 z blokadą | brak | 0 | 1 | jedno zablokowane wydanie |
| F | `Alpha` 1/1, `Beta` 4/4, `Gamma` 20/20 | wszystkie | 3 | 0 | same gotowe; 1 i 20 wymaganych kontroli |
| G | `Alpha` 0/1, `Beta` 2/2 z blokadą, `Gamma` 1/3 z blokadą | brak | 0 | 3 | same niegotowe; zero zakończonych kontroli; obie przeszkody naraz |
| H | `Left` 2/2, `Right` 2/2 z blokadą | `Left` | 1 | 1 | te same liczby kontroli, różna blokada |
| I | dane z wymagań w odwrotnej kolejności | `Tools`, `Core` | 2 | 3 | kolejność raportu |
| J | `Web` 3/3, `Site` 3/3 | `Web`, `Site` | 2 | 0 | te same liczby, różne nazwy |

**Testy automatyczne i Twoje próby.** Wszystkie przypadki są sprawdzone automatycznie przez program kontrolny. Ma on ten sam typ, te same funkcje i ten sam raport co rozwiązanie referencyjne, ale wydania odczytuje z wejścia. To tylko narzędzie do sprawdzania, a nie część misji: w misji wektor jest zapisany w kodzie. Program kontrolny i jego wyniki są w części [Przykładowe rozwiązania](#przykładowe-rozwiązania), bo zawierają rozwiązanie.

</details>

Przykładowe rozwiązanie jest w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 8. Znajdź błąd: niepełny warunek w podsumowaniu

To zadanie wykonaj **po misji**: program poniżej zawiera funkcje podobne do Twoich. Program możesz przepisać albo skopiować do `main.cpp`.

<details>
<summary>Program do sprawdzenia: otwórz po napisaniu własnego programu</summary>

<!-- example: ready_count_bug -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>
#include <vector>

struct Release {
    std::string name;
    int completed_checks;
    int required_checks;
    bool blocked;
};

bool is_ready(const Release& release) {
    return release.completed_checks == release.required_checks && !release.blocked;
}

std::size_t count_ready(const std::vector<Release>& releases) {
    std::size_t ready{0};

    for (const Release& release : releases) {
        if (!release.blocked) {
            ++ready;
        }
    }

    return ready;
}

int main() {
    const std::vector<Release> releases{
        {"Web", 4, 4, false},
        {"Desktop", 2, 3, true}
    };

    for (const Release& release : releases) {
        if (is_ready(release)) {
            std::cout << release.name << ": ready\n";
        } else {
            std::cout << release.name << ": not ready\n";
        }
    }

    std::cout << "Ready: " << count_ready(releases) << "\n";
}
```

1. **Przewidź** standardowe wyjście dla danych z programu.
2. Uruchom program. Czy liczba `Ready` zgadza się ze statusami?
3. Dopisz do wektora jedno wydanie tak, żeby błąd stał się widoczny. Najpierw zapisz poprawny raport dla swoich danych, a potem uruchom program.
4. Porównaj status każdego wydania z liczbą `Ready`.
5. Znajdź różnicę między regułą, według której program ocenia jedno wydanie, a regułą, według której liczy gotowe.
6. Wyjaśnij, dlaczego liczenie musi korzystać z tej samej reguły co statusy.
7. Popraw funkcję liczącą, nie zmieniając danych w wektorze.
8. Uruchom poprawiony program dla swojego wektora: sprawdzasz w nim naraz oba przypadki, pierwotne dane i dopisane wydanie.
9. Przewidź, co obie wersje funkcji liczącej zwrócą dla pustego wektora.

</details>

Wyniki, przykładowe dane i poprawiony program są w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 9. Kopia czy referencja?

<!-- fragment -->
```cpp
int stock_value(const Product& product)    // 1
for (const Product& product : products)    // 2
const Product copy{tea};                   // 3
```

1. W którym zapisie powstaje nowy obiekt z własnymi wartościami pól?
2. W których zapisach program tylko odczytuje istniejący obiekt? Jaki to obiekt?
3. Dlaczego pętla po rekordach nie musi tworzyć kopii każdego elementu?
4. Czy przez `const Product&` można zmienić pole elementu?

<details>
<summary>Odpowiedzi</summary>

1. Tylko w zapisie 3. `copy` to nowy obiekt z kopią wartości wszystkich pól `tea`, niezależny od oryginału (lekcja 8.2).
2. W zapisach 1 i 2. Parametr `product` to inna nazwa obiektu podanego w wywołaniu, a zmienna pętli `product` to inna nazwa kolejnego elementu wektora.
3. Bo tylko odczytuje pola. Element już istnieje w wektorze, a referencja daje do niego dostęp na czas jednego przebiegu. Kopia przydałaby się tylko wtedy, gdyby trzeba było zachować stary stan, jak w lekcji 8.2.
4. Nie. `const` pozwala tylko czytać: linijka `product.stock = 0;` w takiej pętli się nie zbuduje. Zmienianie elementów wektora rekordów to osobny temat, którego w tej lekcji nie wprowadzamy.

</details>

## 10. Gdy coś pójdzie inaczej

| Co widzisz | Co to znaczy | Co zrobić |
|---|---|---|
| `no matching constructor for initialization of 'const std::vector<...>'` | Wartości rekordu stoją w klamrach wektora bez własnych klamer, na przykład `{"Tea", 3, 8, 6}` zamiast `{{"Tea", 3, 8, 6}}`. | Każdy rekord ujmij we własną parę klamer wewnątrz klamer wektora. |
| Pole liczbowe ma wartość 0, a pole `bool` wartość `false`, choć ich nie podano | W wewnętrznych klamrach jest mniej wartości niż pól. Program się buduje, a brakujące pola dostają 0, `false` albo pusty tekst. | Podaj wartość każdego pola w każdym rekordzie. |
| `cannot assign to variable ... with const-qualified type` w pętli albo w funkcji | Kod zmienia pole przez `const&`. | Funkcje i pętle w tej lekcji tylko czytają rekordy. |
| `non-constant-expression cannot be narrowed` przy liczbie rekordów | Wynik `size()` albo różnicę z nim zapisujesz przez `{}` w zmiennej `int` (lekcja 6.3). | Liczby rekordów przechowuj w `std::size_t`. |
| `Not ready` to ogromna liczba | Odejmowanie stoi w odwrotnej kolejności: od liczby gotowych odejmujesz liczbę wszystkich. Wynik `std::size_t` nie może być ujemny (lekcja 6.3). | Od liczby wszystkich wydań odejmij liczbę gotowych. |
| `Ready` nie zgadza się ze statusami w raporcie | Funkcja licząca sprawdza inny warunek niż funkcja dla jednego wydania (punkt 8). | W pętli liczącej korzystaj z funkcji dla jednego wydania. |
| Zablokowane wydanie ma status `ready` | Warunek pomija blokadę albo łączy warunki przez `\|\|`. | Wydanie jest gotowe tylko wtedy, gdy oba warunki są spełnione naraz. |
| Program działa, choć zmienna pętli nie ma `&` | Pętla kopiuje każdy rekord. To poprawny C++, ale przy samym odczycie kopia jest zbędna (punkt 4). | Do odczytu rekordów użyj zmiennej pętli z `const&`. |

## 11. Wyjaśnij

Odpowiedz własnymi słowami, najlepiej na piśmie. Dopiero potem porównaj z przykładowymi odpowiedziami.

1. Co oznacza `std::vector<Product>`? Czy każdy element przechowuje cały rekord?
2. Do czego należą zewnętrzne, a do czego wewnętrzne klamry w inicjalizacji wektora rekordów?
3. Co zwraca `products.size()`? Co daje `empty()` dla pustego wektora?
4. Co robi pętla zakresowa dla pustego wektora i co wtedy zwraca funkcja sumująca albo licząca?
5. Dlaczego funkcja może dostać cały wektor przez `const std::vector<Product>&`?
6. Kiedy funkcja powinna analizować jeden rekord, a kiedy całą kolekcję?
7. Dlaczego warunek gotowości powinien stać w jednej funkcji?
8. Czy poprawny licznik zbiorczy dowodzi, że każdy rekord został dobrze oceniony?
9. Kiedy przyda się pętla po indeksach zamiast pętli zakresowej?

<details>
<summary>Przykładowe odpowiedzi</summary>

1. To wektor, którego elementy mają typ `Product`. Tak: każdy element to cały rekord, ze wszystkimi polami.
2. Zewnętrzne klamry obejmują wszystkie elementy wektora. Każda wewnętrzna para to jeden rekord, z wartościami pól w kolejności z definicji struktury.
3. Liczbę elementów, czyli rekordów, jako `std::size_t`. Dla pustego wektora `empty()` daje `true`, a `size()` daje 0.
4. Nie wykonuje ani jednego przebiegu. Funkcja zwraca wtedy początkową wartość akumulatora albo licznika, czyli 0.
5. Bo tylko czyta rekordy. Dzięki `&` funkcja odczytuje istniejący wektor bez kopiowania go, a `const` nie pozwala go zmienić przez parametr, jak w lekcji 6.4.
6. Jeden rekord, gdy pytanie dotyczy jednego obiektu, na przykład „czy to wydanie jest gotowe?”. Całą kolekcję, gdy odpowiedź zależy od wielu rekordów, na przykład „ile wydań jest gotowych?”.
7. Bo wtedy statusy i licznik korzystają z tej samej reguły i nie mogą się rozjechać. Zmianę reguły robisz w jednym miejscu.
8. Nie. Licznik może się zgadzać przypadkiem, jak w przypadku maskującym z punktu 8. Dwa błędy mogą się też znieść: jedno gotowe wydanie policzone jako niegotowe i jedno niegotowe jako gotowe dają poprawną sumę. Dlatego sprawdzamy także statusy pojedynczych rekordów.
9. Gdy liczy się pozycja rekordu, na przykład przy numerowaniu linijek raportu albo porównywaniu sąsiednich rekordów (lekcja 6.3). Do samego przeglądania kolejnych rekordów wystarczy pętla zakresowa.

</details>

## Podsumowanie

- `std::vector<Product>` to znany wektor, którego elementami są rekordy, inicjalizowany zagnieżdżonymi klamrami: zewnętrznymi dla wektora, wewnętrznymi dla każdego rekordu.
- `size()` podaje liczbę rekordów, a `empty()` mówi, czy wektor jest pusty.
- `for (const Product& product : products)` przegląda rekordy w kolejności z wektora, bez kopiowania ich i bez zmieniania.
- Funkcja dla jednego rekordu zna regułę, a funkcja dla całego wektora (`const std::vector<Product>&`) korzysta z niej w pętli.
- Pusty wektor to poprawne dane: pętla nie wykona przebiegu, a suma albo licznik wynosi 0.
- Poprawny wynik zbiorczy nie dowodzi, że każdy rekord oceniono dobrze: sprawdzaj też wyniki pojedynczych rekordów.

## Co dalej

W tej lekcji funkcje analizowały kolekcję rekordów i zwracały jedną liczbę. Kolejna lekcja Modułu 8 jest w przygotowaniu.

---

## Przykładowe rozwiązania

Zajrzyj tutaj **po własnej próbie**. Twoje nazwy mogą się różnić, jeśli standardowe wyjście jest takie, jak wymagane.

<details>
<summary>Punkt 7: misja, gotowość wydań</summary>

<!-- example: release_review -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>
#include <vector>

struct Release {
    std::string name;
    int completed_checks;
    int required_checks;
    bool blocked;
};

bool is_ready(const Release& release) {
    return release.completed_checks == release.required_checks && !release.blocked;
}

std::size_t count_ready(const std::vector<Release>& releases) {
    std::size_t ready{0};

    for (const Release& release : releases) {
        if (is_ready(release)) {
            ++ready;
        }
    }

    return ready;
}

int main() {
    const std::vector<Release> releases{
        {"Core", 5, 5, false},
        {"Mobile", 4, 5, false},
        {"Docs", 3, 3, true},
        {"Tools", 2, 2, false},
        {"API", 1, 2, true}
    };

    const std::size_t total{releases.size()};
    const std::size_t ready{count_ready(releases)};

    std::cout << "Releases: " << total << "\n";

    for (const Release& release : releases) {
        if (is_ready(release)) {
            std::cout << release.name << ": ready\n";
        } else {
            std::cout << release.name << ": not ready\n";
        }
    }

    std::cout << "Ready: " << ready << "\n";
    std::cout << "Not ready: " << total - ready << "\n";
}
```

1. **Wektor rekordów,** bo każde wydanie to kilka danych, które muszą zostać razem, a wydań jest wiele. Jeden wektor zastępuje pięć osobnych zmiennych, a nowe wydanie to tylko nowa linijka w klamrach.
2. **Zagnieżdżone klamry:** zewnętrzne obejmują elementy wektora, a każda wewnętrzna para to jeden rekord: nazwa, dwie liczby kontroli i blokada, w kolejności pól.
3. **`const&` w pętli,** bo pętla tylko czyta rekordy. `const` pilnuje, żeby żadnego nie zmieniła.
4. **`release.name`** to pole `name` rekordu, do którego w bieżącym przebiegu odnosi się zmienna pętli.
5. **Bez kopii:** rekord zawiera tekst, a do odczytu nazwy i liczb kopia w każdym przebiegu jest zbędna.
6. **`bool` dla jednego wydania,** bo `is_ready` odpowiada na pytanie tak albo nie. Tekst `ready` albo `not ready` wybiera `main`.
7. **`std::size_t` dla kolekcji,** bo `count_ready` zwraca liczbę rekordów, a liczby elementów mają w kursie typ `std::size_t`, jak wynik `size()`. Dzięki temu `total - ready` nie miesza typów.
8. **`count_ready` wywołuje `is_ready`,** więc reguła gotowości stoi w programie raz. Statusy i licznik nie mogą się rozjechać.
9. **Pusty wektor daje zero:** pętla w `count_ready` nie wykona przebiegu, więc licznik zostaje 0. Pętla w `main` też nie wypisze żadnej nazwy.
10. **Niegotowe to różnica,** bo każde wydanie jest albo gotowe, albo nie. Gotowych nie może być więcej niż wszystkich, więc ta różnica jest zawsze poprawna. Odwrotne odejmowanie dałoby ogromną liczbę, jak `0 - 1` w lekcji 6.3.
11. **Dane się nie zmieniają:** wektor jest `const`, a funkcje i pętle dostają rekordy przez `const&`, więc kompilator nie pozwoliłby ich zmienić.
12. **Bez `push_back` i wejścia,** bo wszystkie wydania są znane z góry, więc wystarcza wektor zainicjalizowany w kodzie.
13. **Bez indeksów,** bo do przeglądania rekordów w kolejności nie jest potrzebna pozycja (lekcja 6.3).
14. **Ten sam model działa dla innych rekordów:** funkcja dla jednego elementu z parametrem `const Typ&` i funkcja dla kolekcji z parametrem `const std::vector<Typ>&`, która w pętli z `const Typ&` korzysta z pierwszej.

**Dwa przejścia po wektorze:** `main` przegląda wydania, żeby wypisać statusy, a `count_ready` przegląda je jeszcze raz, żeby policzyć gotowe. Przy kilku rekordach to bez znaczenia, a dzięki temu funkcja licząca niczego nie wypisuje, a `main` nie powtarza reguły gotowości.

**Inne poprawne rozwiązania:** przy danych zgodnych z regułami warunek `release.completed_checks >= release.required_checks` daje ten sam wynik co `==`. `main` może zapisać liczbę niegotowych w osobnej zmiennej `std::size_t`. Pola mogą mieć inne nazwy i inną kolejność, jeśli wartości w klamrach stoją w tej samej kolejności co pola.

**Program kontrolny** sprawdza wszystkie przypadki z listy kontrolnej. Struktura i obie funkcje są takie same jak wyżej, a raport od obliczenia liczby wydań też, poza wcięciem. Różnica jest jedna: wektor nie jest zapisany w kodzie, tylko powstaje z wejścia. Program odczytuje liczbę wydań, a potem każde wydanie: nazwę, dwie liczby kontroli oraz `yes` albo `no` dla blokady, zamienione na `bool` porównaniem, jak w lekcji 3.4. Każde odczytane wydanie trafia na koniec wektora przez `push_back`, jak liczby w lekcji 6.2. Misja nie potrzebuje ani wejścia, ani `push_back`.

<!-- example: release_review_check -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>
#include <vector>

struct Release {
    std::string name;
    int completed_checks;
    int required_checks;
    bool blocked;
};

bool is_ready(const Release& release) {
    return release.completed_checks == release.required_checks && !release.blocked;
}

std::size_t count_ready(const std::vector<Release>& releases) {
    std::size_t ready{0};

    for (const Release& release : releases) {
        if (is_ready(release)) {
            ++ready;
        }
    }

    return ready;
}

int main() {
    std::vector<Release> releases{};
    int count{0};

    std::cin >> count;

    for (int number{1}; number <= count; ++number) {
        std::string name{};
        int completed_checks{0};
        int required_checks{0};
        std::string blocked_answer{};

        std::cin >> name;
        std::cin >> completed_checks;
        std::cin >> required_checks;
        std::cin >> blocked_answer;

        const Release release{name, completed_checks, required_checks, blocked_answer == "yes"};
        releases.push_back(release);
    }

    if (std::cin.fail()) {
        std::cout << "Input could not be read\n";
    } else {
        const std::size_t total{releases.size()};
        const std::size_t ready{count_ready(releases)};

        std::cout << "Releases: " << total << "\n";

        for (const Release& release : releases) {
            if (is_ready(release)) {
                std::cout << release.name << ": ready\n";
            } else {
                std::cout << release.name << ": not ready\n";
            }
        }

        std::cout << "Ready: " << ready << "\n";
        std::cout << "Not ready: " << total - ready << "\n";
    }
}
```

Każdy przypadek zaczyna się od liczby wydań. Potem każde wydanie zajmuje jedną linijkę: nazwa, liczba zakończonych kontroli, liczba wymaganych kontroli oraz `yes` albo `no` dla blokady. Przypadki stoją w kolejności z listy kontrolnej, od A do J.

<!-- input: release_review_check -->
```text
5
Core 5 5 no
Mobile 4 5 no
Docs 3 3 yes
Tools 2 2 no
API 1 2 yes
```

<!-- output: release_review_check -->
```text
Releases: 5
Core: ready
Mobile: not ready
Docs: not ready
Tools: ready
API: not ready
Ready: 2
Not ready: 3
```

<!-- input: release_review_check -->
```text
0
```

<!-- output: release_review_check -->
```text
Releases: 0
Ready: 0
Not ready: 0
```

<!-- input: release_review_check -->
```text
1
Solo 3 3 no
```

<!-- output: release_review_check -->
```text
Releases: 1
Solo: ready
Ready: 1
Not ready: 0
```

<!-- input: release_review_check -->
```text
1
Beta 2 3 no
```

<!-- output: release_review_check -->
```text
Releases: 1
Beta: not ready
Ready: 0
Not ready: 1
```

<!-- input: release_review_check -->
```text
1
Lock 3 3 yes
```

<!-- output: release_review_check -->
```text
Releases: 1
Lock: not ready
Ready: 0
Not ready: 1
```

<!-- input: release_review_check -->
```text
3
Alpha 1 1 no
Beta 4 4 no
Gamma 20 20 no
```

<!-- output: release_review_check -->
```text
Releases: 3
Alpha: ready
Beta: ready
Gamma: ready
Ready: 3
Not ready: 0
```

<!-- input: release_review_check -->
```text
3
Alpha 0 1 no
Beta 2 2 yes
Gamma 1 3 yes
```

<!-- output: release_review_check -->
```text
Releases: 3
Alpha: not ready
Beta: not ready
Gamma: not ready
Ready: 0
Not ready: 3
```

<!-- input: release_review_check -->
```text
2
Left 2 2 no
Right 2 2 yes
```

<!-- output: release_review_check -->
```text
Releases: 2
Left: ready
Right: not ready
Ready: 1
Not ready: 1
```

<!-- input: release_review_check -->
```text
5
API 1 2 yes
Tools 2 2 no
Docs 3 3 yes
Mobile 4 5 no
Core 5 5 no
```

<!-- output: release_review_check -->
```text
Releases: 5
API: not ready
Tools: ready
Docs: not ready
Mobile: not ready
Core: ready
Ready: 2
Not ready: 3
```

<!-- input: release_review_check -->
```text
2
Web 3 3 no
Site 3 3 no
```

<!-- output: release_review_check -->
```text
Releases: 2
Web: ready
Site: ready
Ready: 2
Not ready: 0
```

</details>

<details>
<summary>Punkt 8: wyniki przed poprawką i poprawiony program</summary>

Przed poprawką, dla danych z programu:

<!-- output: ready_count_bug -->
```text
Web: ready
Desktop: not ready
Ready: 1
```

- **Wynik wygląda poprawnie.** `Web` jest gotowe, a `Desktop` zablokowane. Funkcja licząca sprawdza tylko blokadę, więc liczy `Web` i pomija `Desktop`, czyli przypadkiem daje poprawne 1.
- **Dane, które ujawniają błąd:** wydanie bez blokady, ale z niezakończonymi kontrolami. Na przykład `{"Mobile", 4, 5, false}` z misji. Poprawny raport to `Mobile: not ready` i `Ready: 1`. Program z błędem wypisuje:

<!-- example: ready_count_revealed -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>
#include <vector>

struct Release {
    std::string name;
    int completed_checks;
    int required_checks;
    bool blocked;
};

bool is_ready(const Release& release) {
    return release.completed_checks == release.required_checks && !release.blocked;
}

std::size_t count_ready(const std::vector<Release>& releases) {
    std::size_t ready{0};

    for (const Release& release : releases) {
        if (!release.blocked) {
            ++ready;
        }
    }

    return ready;
}

int main() {
    const std::vector<Release> releases{
        {"Web", 4, 4, false},
        {"Desktop", 2, 3, true},
        {"Mobile", 4, 5, false}
    };

    for (const Release& release : releases) {
        if (is_ready(release)) {
            std::cout << release.name << ": ready\n";
        } else {
            std::cout << release.name << ": not ready\n";
        }
    }

    std::cout << "Ready: " << count_ready(releases) << "\n";
}
```

<!-- output: ready_count_revealed -->
```text
Web: ready
Desktop: not ready
Mobile: not ready
Ready: 2
```

| Wydanie | Status z `is_ready` | Czy `count_ready` je liczy? |
|---|---|---|
| `Web` 4/4 | gotowe | tak |
| `Desktop` 2/3 z blokadą | niegotowe | nie |
| `Mobile` 4/5 | niegotowe | **tak** |

- **Przyczyna:** `is_ready` sprawdza oba warunki, a `count_ready` tylko blokadę. Dwie funkcje stosują dwie różne reguły gotowości, więc statusy mówią o jednym gotowym wydaniu, a licznik o dwóch.
- **Poprawka:** w pętli liczącej skorzystaj z `is_ready`: `if (is_ready(release))`. Danych w wektorze nie zmieniamy.

<!-- example: ready_count_fixed -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>
#include <vector>

struct Release {
    std::string name;
    int completed_checks;
    int required_checks;
    bool blocked;
};

bool is_ready(const Release& release) {
    return release.completed_checks == release.required_checks && !release.blocked;
}

std::size_t count_ready(const std::vector<Release>& releases) {
    std::size_t ready{0};

    for (const Release& release : releases) {
        if (is_ready(release)) {
            ++ready;
        }
    }

    return ready;
}

int main() {
    const std::vector<Release> releases{
        {"Web", 4, 4, false},
        {"Desktop", 2, 3, true},
        {"Mobile", 4, 5, false}
    };

    for (const Release& release : releases) {
        if (is_ready(release)) {
            std::cout << release.name << ": ready\n";
        } else {
            std::cout << release.name << ": not ready\n";
        }
    }

    std::cout << "Ready: " << count_ready(releases) << "\n";
}
```

<!-- output: ready_count_fixed -->
```text
Web: ready
Desktop: not ready
Mobile: not ready
Ready: 1
```

Dla pierwotnych dwóch wydań poprawiony program wypisuje to samo co przed poprawką, bo `Web` i `Desktop` obie reguły oceniają tak samo. Dla pustego wektora obie wersje zwracają 0, bo pętla nie wykona przebiegu. Ani przypadek maskujący, ani pusty wektor nie ujawniają więc błędu: potrzebne jest wydanie, które dwie reguły oceniają różnie.

</details>

**Poprzednia lekcja:** [Lekcja 8.3: Funkcje, które analizują rekord](lesson_03_functions_that_analyse_a_record.md) · **Następna lekcja:** w przygotowaniu · [Opis kursu](../../README.md)

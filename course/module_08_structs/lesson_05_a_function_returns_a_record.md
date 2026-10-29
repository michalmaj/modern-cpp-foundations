# Lekcja 8.5: Funkcja zwraca rekord z kilkoma wynikami

**Polski** · [English](lesson_05_a_function_returns_a_record.en.md) · [Opis kursu](../../README.md)

> **Moduł 8, lekcja 5** · około 75–90 minut
> **Potrzebujesz:** katalogu `cpp-workspace` i oryginalnego projektu `lesson_05_first_program`, jak dotąd. Debugger nie jest w tej lekcji potrzebny.
> **Wersja pilotażowa.** Programy z tej lekcji sprawdzamy automatycznie na Windowsie, Ubuntu i macOS. Żaden z nich nie pyta o dane: wszystkie wartości są zapisane w kodzie. Dane z wejścia odczytuje tylko program kontrolny w części z rozwiązaniami.

## Zanim zaczniesz

Ta lekcja zakłada, że:

- piszesz funkcje z typem wyniku i `return` (lekcja 5.3), a funkcja potrafi zwrócić nowy wektor albo nowy tekst przez wartość (lekcje 6.5 i 7.3);
- definiujesz strukturę, inicjalizujesz wszystkie jej pola w `{}` i zmieniasz pola obiektu bez `const` (lekcje 8.1 i 8.2);
- piszesz funkcje, które dostają rekord przez `const Product&` (lekcja 8.3);
- przeglądasz wektor rekordów pętlą `for (const Product& product : products)`, piszesz funkcję dla całego wektora, a liczby rekordów zapisujesz jako `std::size_t` (lekcja 8.4).

## Sytuacja

W lekcji 8.3 o jeden produkt pytały dwie funkcje: `stock_value` zwracała wartość zapasu jako `int`, a `needs_restock` odpowiadała wartością `bool`, czy trzeba uzupełnić zapas. To dobry projekt: każda funkcja odpowiada na jedno pytanie.

Czasem jednak kilka wyników należy do **jednej analizy** i wygodniej oddać je razem. Funkcja zwraca jedną wartość, ale ta wartość może być rekordem naszego własnego typu, z kilkoma polami. Wtedy jedna funkcja oddaje cały komplet odpowiedzi, a `main` odczytuje z niego pola.

Po tej lekcji będziesz:

- projektować własny typ wyniku i odróżniać go od typu danych wejściowych;
- pisać funkcję, która tworzy lokalny wynik, zmienia jego pola i zwraca go przez wartość;
- odbierać zwrócony rekord w `main` i odczytywać jego pola;
- łączyć w jednym wyniku sumę, licznik i odpowiedź tak albo nie;
- zachowywać w pętli informację o tym, co wydarzyło się we wszystkich dotychczas przejrzanych rekordach;
- dobierać dane, które ujawniają, że taka informacja ginie.

## 1. Przygotuj projekt

W `cpp-workspace` utwórz katalog `lesson_8_5` i skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program`. Program z punktu 3 wpisujesz w `main.cpp` tego katalogu. Typ `Product` pochodzi z poprzednich lekcji Modułu 8.

## 2. Typ wyniku

Wynik analizy jednego produktu ma dwie części: wartość zapasu i odpowiedź, czy trzeba go uzupełnić. Można je zebrać w osobnej strukturze:

<!-- fragment -->
```cpp
struct ProductReport {
    int stock_value;
    bool needs_restock;
};
```

| Typ | Co opisuje |
|---|---|
| `Product` | dane jednego produktu: nazwę, stan, minimum i cenę |
| `ProductReport` | wynik analizy jednego produktu: wartość zapasu i decyzję o uzupełnieniu |

- **To dwa różne typy,** każdy z własnymi polami. `Product` to dane, a `ProductReport` to odpowiedzi na pytania o te dane.
- **Pola wyniku nie muszą powtarzać pól wejścia.** W `ProductReport` nie ma nazwy, stanu ani ceny, tylko to, co analiza oblicza.
- **Osobne funkcje z lekcji 8.3 nadal są poprawne.** Struktura wyniku przydaje się wtedy, gdy kilka wyników powstaje w jednej analizie i wygodnie przekazać je razem.

## 3. Funkcja zwraca rekord

<!-- example: product_report -->
```cpp
#include <iostream>
#include <string>

struct Product {
    std::string name;
    int stock;
    int minimum;
    int unit_price;
};

struct ProductReport {
    int stock_value;
    bool needs_restock;
};

ProductReport inspect_product(const Product& product) {
    ProductReport result{0, false};

    result.stock_value = product.stock * product.unit_price;
    result.needs_restock = product.stock < product.minimum;

    return result;
}

int main() {
    const Product tea{"Tea", 3, 8, 6};
    const ProductReport report{inspect_product(tea)};

    std::cout << "Product: " << tea.name << "\n";
    std::cout << "Stock value: " << report.stock_value << "\n";

    if (report.needs_restock) {
        std::cout << "Restock needed: yes\n";
    } else {
        std::cout << "Restock needed: no\n";
    }
}
```

Wpisz program i **przewidź** wynik. Liczby znasz już z lekcji 8.3, więc uruchomienie jest nieobowiązkowe.

<details>
<summary>Standardowe wyjście</summary>

<!-- output: product_report -->
```text
Product: Tea
Stock value: 18
Restock needed: yes
```

</details>

| Krok w `inspect_product` | Co się dzieje |
|---|---|
| `ProductReport result{0, false};` | powstaje lokalny wynik z wartościami początkowymi wszystkich pól |
| `result.stock_value = ...;` | funkcja zapisuje w polu wartość zapasu: `3 * 6`, czyli 18 |
| `result.needs_restock = ...;` | funkcja zapisuje w drugim polu odpowiedź: `3 < 8`, czyli `true` |
| `return result;` | funkcja oddaje cały rekord: oba pola naraz |

- **Typ wyniku funkcji to `ProductReport`.** `return 18;` zwraca jedną liczbę, a `return result;` cały obiekt z kilkoma polami, bo taki typ wyniku ma funkcja.
- **`main` odbiera cały rekord** w jednej zmiennej, `report`, i odczytuje z niej pola przez kropkę: `report.stock_value` i `report.needs_restock`. Tekst `yes` albo `no` wybiera `if`, jak dotąd.
- **Funkcja niczego nie wypisuje.** Nazwę produktu `main` bierze z `tea`, bo wynik jej nie powtarza.

## 4. Wejście i wynik

| Miejsce | Zapis | Rola |
|---|---|---|
| parametr | `const Product& product` | wejście: istniejący produkt, tylko do odczytu |
| zmienna lokalna | `ProductReport result{0, false};` | wynik w budowie: funkcja zmienia jego pola, więc nie ma `const` |
| typ wyniku funkcji | `ProductReport` | to, co funkcja oddaje |
| odbiór w `main` | `const ProductReport report{inspect_product(tea)};` | gotowy wynik, którego `main` już nie zmienia |

`const` przy parametrze dotyczy tylko produktu. Nie zabrania tworzenia ani zmieniania lokalnego wyniku: to osobny obiekt, który należy do funkcji.

## 5. Zwracanie przez wartość

Ten sam model znasz z lekcji 6.5 i 7.3, gdzie funkcja zwracała nowy wektor albo nowy tekst. Teraz zwraca obiekt naszego typu:

1. funkcja tworzy lokalny wynik;
2. przygotowuje wartości jego pól;
3. zwraca wynik przez wartość;
4. kod wywołujący odbiera go we własnej zmiennej.

Zmienna `result` kończy się razem z funkcją, ale jej wartość trafia do `main` jako wynik. **To nie jest referencja do zmiennej funkcji:** `main` ma własny rekord. Współczesny C++ zwraca takie obiekty wydajnie, a jak dokładnie to robi, poznasz później. W tej lekcji wystarczy model.

**Przewidź:** wynik odebrano tym razem bez `const`, a potem zmieniono jego pole.

<!-- fragment -->
```cpp
const Product tea{"Tea", 3, 8, 6};
ProductReport report{inspect_product(tea)};

report.stock_value = 0;
```

Ile wynosi teraz `report.stock_value`, a ile `tea.stock`? Czy `inspect_product` mogła zmienić `tea`?

<details>
<summary>Odpowiedź</summary>

`report.stock_value` wynosi 0, a `tea.stock` nadal 3. `report` to osobny obiekt, więc zmiana jego pola nie dotyczy produktu, jak kopia w lekcji 8.2. Funkcja też nie mogła zmienić `tea`: dostała produkt przez `const&`, a pracowała na swoim lokalnym wyniku.

</details>

## 6. Misja: jedna analiza, trzy wyniki

Program przegląda odczyty liczników zużycia energii w uproszczonym systemie, bez prawdziwych urządzeń i jednostek. Liczby są umowne. Jedna analiza całej listy liczników ma dać trzy wyniki.

**Dane:**

| Licznik | Zużycie | Próg | Zweryfikowany? |
|---|---:|---:|---|
| `Kitchen` | 8 | 6 | tak |
| `Office` | 3 | 5 | tak |
| `Hall` | 7 | 7 | nie |
| `Lab` | 10 | 8 | nie |

**Reguły:**

- Zużycie jest nieujemne, a próg dodatni. Liczby są małe, a program nie sprawdza danych.
- **Łączne zużycie** to suma zużycia wszystkich liczników, także niezweryfikowanych.
- **Licznik przekracza próg,** gdy zużycie jest **większe** od progu. Zużycie równe progowi nie jest przekroczeniem. Weryfikacja nie ma tu znaczenia.
- **Niezweryfikowany odczyt istnieje,** gdy co najmniej jeden licznik ma niezweryfikowany odczyt, w dowolnym miejscu listy. Nie musi to być ostatni licznik ani licznik powyżej progu.

To trzy różne rodzaje informacji: suma, licznik i odpowiedź tak albo nie.

**Wymagania:**

- Program definiuje dwa własne typy. Typ licznika ma cztery pola: nazwę (tekst), zużycie i próg (liczby całkowite) oraz informację o weryfikacji (tak albo nie). Typ wyniku ma trzy pola: łączne zużycie (`int`), liczbę liczników powyżej progu (`std::size_t`) i informację, czy istnieje niezweryfikowany odczyt (`bool`). Nazwy typów i pól oraz kolejność pól wybierasz samodzielnie.
- Wszystkie liczniki są elementami jednego wektora `const`, zainicjalizowanego w kodzie w kolejności z tabeli. Bez osobnych zmiennych na każdy licznik i bez `push_back`.
- Program ma własną funkcję analizującą. Dostaje ona cały wektor przez `const&`, tworzy lokalny wynik z wartościami początkowymi wszystkich pól, przegląda liczniki przez `const&`, aktualizuje trzy pola wyniku i zwraca cały wynik. Nie zmienia danych, niczego nie wypisuje ani nie odczytuje z wejścia. Nazwę funkcji i parametru wybierasz samodzielnie. Inne funkcje nie są potrzebne.
- `main` tworzy wektor, wywołuje funkcję raz i odbiera wynik do jednej zmiennej. Liczbę liczników bierze z `size()`, a pozostałe linijki raportu z pól wyniku. Niczego nie liczy drugi raz.
- Program wypisuje dokładnie cztery linijki, jak w przykładzie niżej: `Meters`, `Total usage`, `Above limit` i `Has unverified`, ta ostatnia ze słowem `yes` albo `no`. Nie wypisuje nazw liczników ani innych komunikatów.

W `cpp-workspace` utwórz katalog `meter_summary`, skopiuj do niego `CMakeLists.txt` z oryginalnego `lesson_05_first_program`, utwórz pusty `main.cpp` i napisz program samodzielnie.

Dla danych powyżej standardowe wyjście ma być takie:

<!-- output: meter_summary -->
```text
Meters: 4
Total usage: 28
Above limit: 2
Has unverified: yes
```

Łączne zużycie to 8 + 3 + 7 + 10, czyli 28. Próg przekraczają `Kitchen` i `Lab`, a `Hall` ma zużycie równe progowi. `Hall` i `Lab` nie mają zweryfikowanych odczytów.

**To nie jest program o produktach z innymi nazwami.** Musisz samodzielnie zdecydować:

1. jak nazwać oba typy i ich pola;
2. jakie wartości początkowe ma wynik i dlaczego właśnie takie;
3. jak w pętli zmieniać sumę, a jak licznik przekroczeń;
4. jak sprawić, żeby informacja o niezweryfikowanym odczycie nie zginęła przy kolejnych licznikach;
5. jak zwrócić wynik i jak odczytać jego pola w `main`;
6. co program wypisze dla pustego wektora;
7. czy kolejność liczników może zmienić wynik.

**Zanim napiszesz program**, przygotuj tabelę przypadków: pusty wektor, jeden licznik poniżej progu, równo z progiem i powyżej, wszystkie odczyty zweryfikowane, jeden niezweryfikowany odczyt na początku, w środku i na końcu listy oraz kilka niezweryfikowanych. Przy każdym zapisz wszystkie trzy wyniki.

**Potem** uruchom program dla danych z wymagań i dla pustego wektora. Zmieniaj przy tym tylko zawartość klamer wektora. Wszystkie przypadki z pełnej listy kontrolnej są sprawdzone automatycznie.

### Kryterium sukcesu

- Program buduje się jako C++20 i dla danych z wymagań wypisuje dokładnie cztery linijki pokazane wyżej.
- Są dwa typy: licznika z czterema polami i wyniku z trzema polami typów `int`, `std::size_t` i `bool`, oraz jeden wektor `const` z czterema rekordami, zainicjalizowany w kodzie.
- Funkcja analizująca dostaje wektor przez `const&`, buduje lokalny wynik z wartościami początkowymi wszystkich pól i zwraca cały rekord. Niczego nie wypisuje ani nie zmienia.
- `main` wywołuje funkcję raz i nie powtarza jej obliczeń.
- Zużycie równe progowi nie jest przekroczeniem, a raz wykryty niezweryfikowany odczyt zostaje w wyniku, niezależnie od miejsca na liście.
- Dla pustego wektora program wypisuje `Meters: 0`, `Total usage: 0`, `Above limit: 0` i `Has unverified: no`.
- Tabela przypadków powstała przed uruchomieniem programu.
- Umiesz wyjaśnić, czym typ wyniku różni się od typu licznika.

Gdy wynik się zgadza, możesz zapisać projekt w Gicie, jak w lekcji 1.5.

<details>
<summary>Podpowiedź 1</summary>

Jedna analiza ma zwrócić trzy powiązane wyniki. Jakiego własnego typu można użyć do przechowania ich razem?

</details>

<details>
<summary>Podpowiedź 2</summary>

Utwórz lokalny rekord wynikowy z wartościami początkowymi. Podczas pętli aktualizuj odpowiednie pola, a na końcu zwróć cały rekord.

</details>

<details>
<summary>Podpowiedź 3</summary>

Suma rośnie o zużycie, licznik rośnie tylko po przekroczeniu progu, a informacja o niezweryfikowanym odczycie powinna pozostać prawdziwa, jeżeli choć jeden taki odczyt już wystąpił.

</details>

<details>
<summary>Pełna lista przypadków kontrolnych: otwórz po przygotowaniu własnej tabeli</summary>

Zapis `8/6` oznacza zużycie 8 przy progu 6. Gwiazdka oznacza niezweryfikowany odczyt.

| | Liczniki | Meters | Total usage | Above limit | Has unverified | Co sprawdza |
|---|---|---:|---:|---:|---|---|
| A | dane z wymagań | 4 | 28 | 2 | yes | dane z wymagań |
| B | brak liczników | 0 | 0 | 0 | no | pusty wektor |
| C | `Solo` 3/5 | 1 | 3 | 0 | no | jeden zweryfikowany licznik poniżej progu |
| D | `Peak` 9/5 | 1 | 9 | 1 | no | jeden zweryfikowany licznik powyżej progu |
| E | `Draft` 2/5* | 1 | 2 | 0 | yes | jeden niezweryfikowany licznik poniżej progu |
| F | `Edge` 7/7 | 1 | 7 | 0 | no | zużycie równe progowi |
| G | `Alpha` 0/4, `Beta` 2/5, `Gamma` 4/6 | 3 | 6 | 0 | no | wszystkie poniżej progów i zweryfikowane; zero zużycia |
| H | `Alpha` 6/5*, `Beta` 9/8, `Gamma` 4/1* | 3 | 19 | 3 | yes | wszystkie powyżej progów; kilka niezweryfikowanych |
| I | `Barn` 2/5*, `Loft` 3/5, `Yard` 4/5 | 3 | 9 | 0 | yes | niezweryfikowany odczyt na początku |
| J | `Loft` 3/5, `Yard` 4/5, `Barn` 2/5* | 3 | 9 | 0 | yes | niezweryfikowany odczyt na końcu |
| K | `Loft` 3/5, `Barn` 2/5*, `Yard` 4/5 | 3 | 9 | 0 | yes | niezweryfikowany odczyt w środku |
| L | `North` 6/4, `South` 6/4, `West` 6/4 | 3 | 18 | 3 | no | takie same liczby w kilku rekordach |
| M | dane z wymagań w odwrotnej kolejności | 4 | 28 | 2 | yes | inna kolejność, ten sam wynik |

**Testy automatyczne i Twoje próby.** Wszystkie przypadki są sprawdzone automatycznie przez program kontrolny. Ma on te same typy, tę samą funkcję i ten sam raport co rozwiązanie referencyjne, ale liczniki odczytuje z wejścia. To tylko narzędzie do sprawdzania, a nie część misji: w misji wektor jest zapisany w kodzie. Program kontrolny i jego wyniki są w części [Przykładowe rozwiązania](#przykładowe-rozwiązania), bo zawierają rozwiązanie.

</details>

Przykładowe rozwiązanie jest w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 7. Znajdź błąd: flaga zapomina wcześniejszy odczyt

To zadanie wykonaj **po misji**: program poniżej zawiera funkcję podobną do Twojej. Program możesz przepisać albo skopiować do `main.cpp`.

<details>
<summary>Program do sprawdzenia: otwórz po napisaniu własnego programu</summary>

<!-- example: unverified_flag_bug -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>
#include <vector>

struct Meter {
    std::string name;
    int usage;
    int limit;
    bool verified;
};

struct MeterSummary {
    int total_usage;
    std::size_t above_limit;
    bool has_unverified;
};

MeterSummary summarise_meters(const std::vector<Meter>& meters) {
    MeterSummary result{0, 0, false};

    for (const Meter& meter : meters) {
        result.total_usage += meter.usage;

        if (meter.usage > meter.limit) {
            ++result.above_limit;
        }

        result.has_unverified = !meter.verified;
    }

    return result;
}

int main() {
    const std::vector<Meter> meters{
        {"Garage", 4, 6, true},
        {"Attic", 9, 5, true},
        {"Porch", 2, 3, false}
    };

    const MeterSummary summary{summarise_meters(meters)};

    std::cout << "Meters: " << meters.size() << "\n";
    std::cout << "Total usage: " << summary.total_usage << "\n";
    std::cout << "Above limit: " << summary.above_limit << "\n";

    if (summary.has_unverified) {
        std::cout << "Has unverified: yes\n";
    } else {
        std::cout << "Has unverified: no\n";
    }
}
```

1. **Przewidź** standardowe wyjście dla danych z programu.
2. Uruchom program. Czy wszystkie trzy wyniki są poprawne?
3. Zmień dane w wektorze tak, żeby błąd stał się widoczny. Najpierw zapisz poprawne wyniki dla swoich danych, a potem uruchom program.
4. Prześledź wartość pola `has_unverified` po każdym przebiegu pętli.
5. Wyjaśnij, dlaczego informacja raz wykryta nie może zostać zapomniana przez późniejszy licznik.
6. Popraw funkcję tak, żeby suma i licznik przekroczeń działały jak dotąd.
7. Uruchom poprawiony program dla swojego wektora.
8. Przewidź, co poprawiony program wypisze dla pustego wektora.
9. Przewidź wynik dla wektora, w którym wszystkie odczyty są zweryfikowane.

</details>

Wyniki, przykładowe dane i poprawiony program są w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 8. Gdy coś pójdzie inaczej

| Co widzisz | Co to znaczy | Co zrobić |
|---|---|---|
| Ostrzeżenie `non-void function does not return a value` | Funkcja nie zwraca wyniku: brakuje `return`. Wynik takiego wywołania nie jest określony (lekcja 5.3). | Na końcu funkcji zwróć cały rekord: `return result;`. |
| `no viable conversion from 'ProductReport' to ...` | Wynik funkcji, cały rekord, trafia do zmiennej innego typu, na przykład `int`. | Odbierz cały rekord, a liczbę odczytaj z jego pola, na przykład `report.stock_value`. |
| `invalid operands to binary expression` przy `std::cout << report` | `std::cout` nie wypisze całego rekordu naraz. | Wypisuj kolejne pola, na przykład `report.stock_value`. |
| `cannot assign to variable ... with const-qualified type` | Funkcja zmienia rekord wejściowy przez `const&` albo `main` zmienia wynik odebrany jako `const`. | Zmieniaj tylko lokalny wynik w funkcji. Dane wejściowe tylko czytaj. |
| Wyniki są przypadkowymi liczbami | Lokalny wynik powstał bez wartości początkowych, na przykład `ProductReport result;`. Odczyt takich pól to niezdefiniowane zachowanie, a kompilator nie musi o tym ostrzec. | Podaj w `{}` wartości początkowe wszystkich pól wyniku. |
| `Has unverified` zależy tylko od ostatniego licznika | Pole jest nadpisywane w każdym przebiegu pętli (punkt 7). | Ustaw je na `true`, gdy trafisz na niezweryfikowany odczyt, i już go nie cofaj. |
| `Above limit` liczy też zużycie równe progowi | Warunek używa `>=` zamiast `>`. | Przekroczenie to zużycie **większe** od progu. |
| `Total usage` jest za małe | Dodawanie zużycia stoi wewnątrz warunku, więc część liczników, na przykład niezweryfikowane, nie trafia do sumy. | Dodawaj zużycie każdego licznika, poza warunkami. |

## 9. Wyjaśnij

Odpowiedz własnymi słowami, najlepiej na piśmie. Dopiero potem porównaj z przykładowymi odpowiedziami.

1. Dlaczego jedna analiza może mieć kilka wyników? Kiedy warto zebrać je w jednym rekordzie, a kiedy wystarczą osobne funkcje?
2. Co opisuje struktura wejściowa, a co wynikowa? Czy wynik musi powtarzać pola wejścia?
3. Czy funkcja może zwracać własny typ? Co oznacza wtedy `return result;`?
4. Dlaczego lokalny wynik nie ma `const`, choć parametr ma?
5. Czy funkcja zwraca referencję do swojego lokalnego obiektu? Co się dzieje z `result` po zakończeniu funkcji?
6. Dlaczego pola wyniku mogą mieć różne typy? Podaj przykład z misji.
7. Jakie wartości ma wynik dla pustego wektora i skąd się biorą?
8. Jak zachować w pętli informację tak albo nie, która dotyczy wszystkich dotychczas przejrzanych rekordów, a nie tylko bieżącego?
9. Dlaczego funkcja zwraca wynik, zamiast go wypisywać?

<details>
<summary>Przykładowe odpowiedzi</summary>

1. Bo jedno przejrzenie danych może odpowiedzieć na kilka pytań naraz, na przykład o sumę, liczbę przekroczeń i brak weryfikacji. Rekord przydaje się, gdy te odpowiedzi należą do jednej analizy i są potrzebne razem. Osobne funkcje wystarczą, gdy pytania są niezależne, jak w lekcji 8.3.
2. Struktura wejściowa opisuje dane, na przykład jeden licznik. Wynikowa opisuje odpowiedzi analizy. Wynik nie musi powtarzać pól wejścia: zawiera tylko to, co analiza oblicza.
3. Tak. Typ wyniku funkcji to wtedy nazwa struktury, a `return result;` oddaje cały obiekt, ze wszystkimi polami.
4. Bo funkcja zmienia pola wyniku podczas obliczeń. `const` przy parametrze dotyczy tylko danych wejściowych, a lokalny wynik to osobny obiekt funkcji.
5. Nie. Wynik jest zwracany przez wartość: `result` kończy się razem z funkcją, a kod wywołujący dostaje własny rekord, jak wektor w lekcji 6.5.
6. Bo każde pole odpowiada na inne pytanie i ma typ pasujący do odpowiedzi: suma zużycia to `int`, liczba liczników to `std::size_t`, a odpowiedź tak albo nie to `bool`.
7. Wartości początkowe: zero, zero i `false`. Pętla nie wykonuje przebiegu, więc funkcja zwraca wynik taki, jaki utworzyła na początku. To poprawny rekord, bez specjalnego kodu.
8. Zacząć od `false` i ustawiać `true`, gdy pojawi się szukany przypadek, ale nigdy nie przepisywać do pola odpowiedzi dotyczącej tylko bieżącego rekordu. Raz ustawione `true` zostaje do końca pętli.
9. Bo wtedy funkcja tylko liczy, a `main` decyduje, co i jak wypisać. Ten sam wynik można wypisać inaczej, sprawdzić albo przekazać dalej.

</details>

## Podsumowanie

- Gdy kilka wyników należy do jednej analizy, możesz zdefiniować typ wyniku i zwrócić jego obiekt.
- Typ wejściowy opisuje dane, a typ wyniku odpowiedzi. To różne struktury z różnymi polami.
- Funkcja tworzy lokalny wynik z wartościami początkowymi, zmienia jego pola i zwraca go przez wartość: `return result;`.
- `main` odbiera cały rekord i odczytuje jego pola, a dane wejściowe się nie zmieniają.
- Suma rośnie o każdą wartość, licznik tylko przy spełnionym warunku, a flaga, raz ustawiona na `true`, już się nie zmienia.
- Pusty wektor daje poprawny wynik: wartości początkowe.

## Co dalej

W tej lekcji jedna funkcja zwróciła kilka wyników naraz. W sprawdzianie Modułu 8 wykorzystasz umiejętności z całego modułu: własne typy danych, wektor rekordów i funkcje, które analizują rekordy i zwracają wyniki: [Lekcja 8.6: Wyniki biegu (sprawdzian Modułu 8)](lesson_06_race_results.md).

---

## Przykładowe rozwiązania

Zajrzyj tutaj **po własnej próbie**. Twoje nazwy mogą się różnić, jeśli standardowe wyjście jest takie, jak wymagane.

<details>
<summary>Punkt 6: misja, raport liczników</summary>

<!-- example: meter_summary -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>
#include <vector>

struct Meter {
    std::string name;
    int usage;
    int limit;
    bool verified;
};

struct MeterSummary {
    int total_usage;
    std::size_t above_limit;
    bool has_unverified;
};

MeterSummary summarise_meters(const std::vector<Meter>& meters) {
    MeterSummary result{0, 0, false};

    for (const Meter& meter : meters) {
        result.total_usage += meter.usage;

        if (meter.usage > meter.limit) {
            ++result.above_limit;
        }

        if (!meter.verified) {
            result.has_unverified = true;
        }
    }

    return result;
}

int main() {
    const std::vector<Meter> meters{
        {"Kitchen", 8, 6, true},
        {"Office", 3, 5, true},
        {"Hall", 7, 7, false},
        {"Lab", 10, 8, false}
    };

    const MeterSummary summary{summarise_meters(meters)};

    std::cout << "Meters: " << meters.size() << "\n";
    std::cout << "Total usage: " << summary.total_usage << "\n";
    std::cout << "Above limit: " << summary.above_limit << "\n";

    if (summary.has_unverified) {
        std::cout << "Has unverified: yes\n";
    } else {
        std::cout << "Has unverified: no\n";
    }
}
```

1. **Dwa własne typy,** bo opisują różne rzeczy: `Meter` to dane jednego licznika, a `MeterSummary` to odpowiedzi analizy całej listy.
2. **Inne pola:** wynik nie ma nazwy ani progu. Ma sumę, liczbę i odpowiedź tak albo nie, czyli rzeczy, których nie przechowuje żaden licznik.
3. **Rekord zamiast jednej liczby,** bo jedna analiza daje trzy odpowiedzi. Funkcja zwracająca `int` oddałaby tylko jedną, a trzy osobne funkcje przeglądałyby wektor trzy razy i rozdzielały jedną analizę.
4. **Zero, zero i `false` na początku,** bo tak wygląda wynik, zanim program przejrzy jakikolwiek licznik: pusta suma, żadnych przekroczeń, żadnego niezweryfikowanego odczytu.
5. **Suma:** `result.total_usage += meter.usage;` dla każdego licznika, bez warunku, więc liczą się także niezweryfikowane.
6. **Licznik:** `++result.above_limit;` tylko wtedy, gdy `meter.usage > meter.limit`.
7. **Równość nie jest przekroczeniem,** bo reguła mówi o zużyciu większym od progu. `Hall` ma 7 przy progu 7, więc się nie liczy.
8. **Flaga nie wraca do `false`:** program ustawia ją na `true` wewnątrz `if (!meter.verified)`, a poza wartością początkową nigdzie nie zapisuje `false`. Późniejszy zweryfikowany licznik nie zmienia już tej informacji.
9. **Pusty wektor daje poprawny rekord:** pętla nie wykona przebiegu, więc funkcja zwróci wartości początkowe.
10. **Przez wartość,** bo `main` ma dostać własny, gotowy wynik, jak nowy wektor w lekcji 6.5. Lokalny `result` kończy się z funkcją, więc referencja do niego nie miałaby sensu.
11. **Wejście się nie zmienia:** wektor jest `const`, a funkcja dostaje go i przegląda przez `const&`. Funkcja zmienia tylko swój lokalny wynik.
12. **Wypisywanie w `main`,** bo funkcja ma tylko liczyć. Ten sam wynik `main` może wypisać inaczej albo wykorzystać dalej.

**Kolejność liczników nie zmienia wyniku:** suma i liczba przekroczeń nie zależą od kolejności, a flaga odpowiada na pytanie, czy niezweryfikowany odczyt wystąpił gdziekolwiek. Przypadki I, J, K i M to sprawdzają.

**Inne poprawne rozwiązania:** zamiast `if` można napisać `result.has_unverified = result.has_unverified || !meter.verified;`, co daje to samo. Typy i pola mogą mieć inne nazwy i inną kolejność, jeśli wartości w klamrach stoją w tej samej kolejności co pola.

**Program kontrolny** sprawdza wszystkie przypadki z listy kontrolnej. Typy i funkcja są takie same jak wyżej, a raport od odebrania wyniku też, poza wcięciem. Różnica jest jedna: wektor nie jest zapisany w kodzie, tylko powstaje z wejścia. Program odczytuje liczbę liczników, a potem każdy licznik: nazwę, zużycie, próg oraz `yes` albo `no` dla weryfikacji, zamienione na `bool` porównaniem, jak w lekcji 3.4. Każdy odczytany licznik trafia na koniec wektora przez `push_back`, jak w programie kontrolnym lekcji 8.4. Misja nie potrzebuje ani wejścia, ani `push_back`.

<!-- example: meter_summary_check -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>
#include <vector>

struct Meter {
    std::string name;
    int usage;
    int limit;
    bool verified;
};

struct MeterSummary {
    int total_usage;
    std::size_t above_limit;
    bool has_unverified;
};

MeterSummary summarise_meters(const std::vector<Meter>& meters) {
    MeterSummary result{0, 0, false};

    for (const Meter& meter : meters) {
        result.total_usage += meter.usage;

        if (meter.usage > meter.limit) {
            ++result.above_limit;
        }

        if (!meter.verified) {
            result.has_unverified = true;
        }
    }

    return result;
}

int main() {
    std::vector<Meter> meters{};
    int count{0};

    std::cin >> count;

    for (int number{1}; number <= count; ++number) {
        std::string name{};
        int usage{0};
        int limit{0};
        std::string verified_answer{};

        std::cin >> name;
        std::cin >> usage;
        std::cin >> limit;
        std::cin >> verified_answer;

        const Meter meter{name, usage, limit, verified_answer == "yes"};
        meters.push_back(meter);
    }

    if (std::cin.fail()) {
        std::cout << "Input could not be read\n";
    } else {
        const MeterSummary summary{summarise_meters(meters)};

        std::cout << "Meters: " << meters.size() << "\n";
        std::cout << "Total usage: " << summary.total_usage << "\n";
        std::cout << "Above limit: " << summary.above_limit << "\n";

        if (summary.has_unverified) {
            std::cout << "Has unverified: yes\n";
        } else {
            std::cout << "Has unverified: no\n";
        }
    }
}
```

Każdy przypadek zaczyna się od liczby liczników. Potem każdy licznik zajmuje jedną linijkę: nazwa, zużycie, próg oraz `yes` albo `no` dla weryfikacji. Przypadki stoją w kolejności z listy kontrolnej, od A do M.

<!-- input: meter_summary_check -->
```text
4
Kitchen 8 6 yes
Office 3 5 yes
Hall 7 7 no
Lab 10 8 no
```

<!-- output: meter_summary_check -->
```text
Meters: 4
Total usage: 28
Above limit: 2
Has unverified: yes
```

<!-- input: meter_summary_check -->
```text
0
```

<!-- output: meter_summary_check -->
```text
Meters: 0
Total usage: 0
Above limit: 0
Has unverified: no
```

<!-- input: meter_summary_check -->
```text
1
Solo 3 5 yes
```

<!-- output: meter_summary_check -->
```text
Meters: 1
Total usage: 3
Above limit: 0
Has unverified: no
```

<!-- input: meter_summary_check -->
```text
1
Peak 9 5 yes
```

<!-- output: meter_summary_check -->
```text
Meters: 1
Total usage: 9
Above limit: 1
Has unverified: no
```

<!-- input: meter_summary_check -->
```text
1
Draft 2 5 no
```

<!-- output: meter_summary_check -->
```text
Meters: 1
Total usage: 2
Above limit: 0
Has unverified: yes
```

<!-- input: meter_summary_check -->
```text
1
Edge 7 7 yes
```

<!-- output: meter_summary_check -->
```text
Meters: 1
Total usage: 7
Above limit: 0
Has unverified: no
```

<!-- input: meter_summary_check -->
```text
3
Alpha 0 4 yes
Beta 2 5 yes
Gamma 4 6 yes
```

<!-- output: meter_summary_check -->
```text
Meters: 3
Total usage: 6
Above limit: 0
Has unverified: no
```

<!-- input: meter_summary_check -->
```text
3
Alpha 6 5 no
Beta 9 8 yes
Gamma 4 1 no
```

<!-- output: meter_summary_check -->
```text
Meters: 3
Total usage: 19
Above limit: 3
Has unverified: yes
```

<!-- input: meter_summary_check -->
```text
3
Barn 2 5 no
Loft 3 5 yes
Yard 4 5 yes
```

<!-- output: meter_summary_check -->
```text
Meters: 3
Total usage: 9
Above limit: 0
Has unverified: yes
```

<!-- input: meter_summary_check -->
```text
3
Loft 3 5 yes
Yard 4 5 yes
Barn 2 5 no
```

<!-- output: meter_summary_check -->
```text
Meters: 3
Total usage: 9
Above limit: 0
Has unverified: yes
```

<!-- input: meter_summary_check -->
```text
3
Loft 3 5 yes
Barn 2 5 no
Yard 4 5 yes
```

<!-- output: meter_summary_check -->
```text
Meters: 3
Total usage: 9
Above limit: 0
Has unverified: yes
```

<!-- input: meter_summary_check -->
```text
3
North 6 4 yes
South 6 4 yes
West 6 4 yes
```

<!-- output: meter_summary_check -->
```text
Meters: 3
Total usage: 18
Above limit: 3
Has unverified: no
```

<!-- input: meter_summary_check -->
```text
4
Lab 10 8 no
Hall 7 7 no
Office 3 5 yes
Kitchen 8 6 yes
```

<!-- output: meter_summary_check -->
```text
Meters: 4
Total usage: 28
Above limit: 2
Has unverified: yes
```

</details>

<details>
<summary>Punkt 7: wyniki przed poprawką i poprawiony program</summary>

Przed poprawką, dla danych z programu:

<!-- output: unverified_flag_bug -->
```text
Meters: 3
Total usage: 15
Above limit: 1
Has unverified: yes
```

- **Wszystkie trzy wyniki wyglądają poprawnie.** Suma 4 + 9 + 2 to 15, próg przekracza tylko `Attic`, a `Porch` ma niezweryfikowany odczyt. Ale `Porch` stoi na końcu listy, a funkcja przepisuje do flagi odpowiedź o bieżącym liczniku. Końcowa flaga opisuje więc tylko ostatni licznik, a tutaj przypadkiem jest to poprawna odpowiedź.
- **Dane, które ujawniają błąd:** niezweryfikowany odczyt, po którym stoi jeszcze licznik zweryfikowany. Na przykład dopisanie na końcu `{"Shed", 1, 4, true}`. Poprawne wyniki to 4, 16, 1 i `yes`. Program z błędem wypisuje:

<!-- example: unverified_flag_revealed -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>
#include <vector>

struct Meter {
    std::string name;
    int usage;
    int limit;
    bool verified;
};

struct MeterSummary {
    int total_usage;
    std::size_t above_limit;
    bool has_unverified;
};

MeterSummary summarise_meters(const std::vector<Meter>& meters) {
    MeterSummary result{0, 0, false};

    for (const Meter& meter : meters) {
        result.total_usage += meter.usage;

        if (meter.usage > meter.limit) {
            ++result.above_limit;
        }

        result.has_unverified = !meter.verified;
    }

    return result;
}

int main() {
    const std::vector<Meter> meters{
        {"Garage", 4, 6, true},
        {"Attic", 9, 5, true},
        {"Porch", 2, 3, false},
        {"Shed", 1, 4, true}
    };

    const MeterSummary summary{summarise_meters(meters)};

    std::cout << "Meters: " << meters.size() << "\n";
    std::cout << "Total usage: " << summary.total_usage << "\n";
    std::cout << "Above limit: " << summary.above_limit << "\n";

    if (summary.has_unverified) {
        std::cout << "Has unverified: yes\n";
    } else {
        std::cout << "Has unverified: no\n";
    }
}
```

<!-- output: unverified_flag_revealed -->
```text
Meters: 4
Total usage: 16
Above limit: 1
Has unverified: no
```

| Po przebiegu dla | `has_unverified` z błędem | `has_unverified` poprawnie |
|---|---|---|
| `Garage`, zweryfikowany | `false` | `false` |
| `Attic`, zweryfikowany | `false` | `false` |
| `Porch`, niezweryfikowany | `true` | `true` |
| `Shed`, zweryfikowany | **`false`** | `true` |

- **Przyczyna:** linijka `result.has_unverified = !meter.verified;` w każdym przebiegu zastępuje flagę odpowiedzią o bieżącym liczniku. Pole ma jednak opisywać całą dotychczas przejrzaną listę: raz wykryty niezweryfikowany odczyt nie przestaje istnieć tylko dlatego, że następny licznik jest zweryfikowany. Suma i licznik przekroczeń działają poprawnie, więc same nie ujawnią błędu.
- **Poprawka:** ustawiaj flagę tylko wtedy, gdy trafisz na niezweryfikowany odczyt, i nigdy jej nie cofaj.

<!-- example: unverified_flag_fixed -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>
#include <vector>

struct Meter {
    std::string name;
    int usage;
    int limit;
    bool verified;
};

struct MeterSummary {
    int total_usage;
    std::size_t above_limit;
    bool has_unverified;
};

MeterSummary summarise_meters(const std::vector<Meter>& meters) {
    MeterSummary result{0, 0, false};

    for (const Meter& meter : meters) {
        result.total_usage += meter.usage;

        if (meter.usage > meter.limit) {
            ++result.above_limit;
        }

        if (!meter.verified) {
            result.has_unverified = true;
        }
    }

    return result;
}

int main() {
    const std::vector<Meter> meters{
        {"Garage", 4, 6, true},
        {"Attic", 9, 5, true},
        {"Porch", 2, 3, false},
        {"Shed", 1, 4, true}
    };

    const MeterSummary summary{summarise_meters(meters)};

    std::cout << "Meters: " << meters.size() << "\n";
    std::cout << "Total usage: " << summary.total_usage << "\n";
    std::cout << "Above limit: " << summary.above_limit << "\n";

    if (summary.has_unverified) {
        std::cout << "Has unverified: yes\n";
    } else {
        std::cout << "Has unverified: no\n";
    }
}
```

<!-- output: unverified_flag_fixed -->
```text
Meters: 4
Total usage: 16
Above limit: 1
Has unverified: yes
```

Dla pustego wektora poprawiony program wypisze to samo co program kontrolny w przypadku B: pętla nie wykona przebiegu, więc zostają wartości początkowe. Gdy wszystkie odczyty są zweryfikowane, obie wersje zwracają `false`, bo flaga nigdy nie dostaje `true`. Ani pusty wektor, ani taki wektor, ani lista z niezweryfikowanym odczytem na końcu nie ujawniają więc błędu: potrzebny jest niezweryfikowany odczyt, po którym stoi jeszcze zweryfikowany. Dane z misji też kończą się niezweryfikowanym odczytem (`Lab`), więc ten sam błąd w Twoim programie przeszedłby dla nich niezauważony. Ujawniają go przypadki I, K i M z listy kontrolnej.

</details>

**Poprzednia lekcja:** [Lekcja 8.4: Wiele rekordów w `std::vector`](lesson_04_many_records_in_a_vector.md) · **Następna lekcja:** [Lekcja 8.6: Wyniki biegu (sprawdzian Modułu 8)](lesson_06_race_results.md) · [Opis kursu](../../README.md)

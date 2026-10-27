# Lekcja 8.3: Funkcje, które analizują rekord

**Polski** · [English](lesson_03_functions_that_analyse_a_record.en.md) · [Opis kursu](../../README.md)

> **Moduł 8, lekcja 3** · około 65–80 minut
> **Potrzebujesz:** katalogu `cpp-workspace` i oryginalnego projektu `lesson_05_first_program`, jak dotąd. Debugger nie jest w tej lekcji potrzebny.
> **Wersja pilotażowa.** Programy z tej lekcji sprawdzamy automatycznie na Windowsie, Ubuntu i macOS. Żaden z nich nie pyta o dane: wszystkie wartości są zapisane w kodzie. Dane z wejścia odczytuje tylko program kontrolny w części z rozwiązaniami.

## Zanim zaczniesz

Ta lekcja zakłada, że:

- definiujesz strukturę, tworzysz jej obiekty w `{}` i odczytujesz pola przez `.` (lekcja 8.1), a kopię rekordu tworzysz zapisem `Book before{current};` (lekcja 8.2);
- piszesz funkcje, które zwracają wynik `int` albo `bool`, a wypisywanie zostawiasz w `main` (lekcje 5.3 i 5.5);
- wiesz, że funkcja może wywołać inną funkcję, której definicja stoi wyżej w pliku (lekcje 5.5 i 5.6);
- znasz parametr `const&`, przez który funkcja czyta istniejący wektor albo tekst bez kopiowania go (lekcje 6.4 i 7.3).

## Sytuacja

W misji z lekcji 8.1 wartość zapasu powstawała w `main`, z pól jednego obiektu: `product.stock * product.unit_price`. Co zrobić, jeżeli tę wartość trzeba obliczyć dla kilku produktów albo użyć jej w innym programie? Takie obliczenie to dobry kandydat na funkcję (lekcja 5.5).

Funkcja mogłaby dostać pola osobno, jako dwa parametry `int`, ale wtedy każde wywołanie musi wybrać właściwe pola w dobrej kolejności, a dwa argumenty `int` łatwo zamienić (lekcje 5.2 i 8.1). Prościej przekazać funkcji **cały istniejący rekord do odczytu**. Parametr ma wtedy typ `Product`, czyli typ zdefiniowany przez nas.

Po tej lekcji będziesz:

- pisać funkcje z parametrem własnego typu, przekazanym przez `const&`, i odczytywać pola przez nazwę parametru;
- wywoływać jedną funkcję dla różnych obiektów;
- dobierać typ wyniku do pytania: liczba to `int`, a odpowiedź tak albo nie to `bool`;
- odróżniać parametr przez wartość od parametru `const&` i od kopii z lekcji 8.2;
- projektować dwie współpracujące funkcje, które tylko czytają rekord;
- dobierać dane, które ujawniają pomylone pola w obliczeniu.

## 1. Przygotuj projekt

W `cpp-workspace` utwórz katalog `lesson_8_3` i skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program`. Programy z punktów 2 i 4 wpisujesz w `main.cpp` tego katalogu. Typ `Product` pochodzi z misji lekcji 8.1.

## 2. Funkcja, która dostaje rekord

<!-- example: stock_values -->
```cpp
#include <iostream>
#include <string>

struct Product {
    std::string name;
    int stock;
    int minimum;
    int unit_price;
};

int stock_value(const Product& product) {
    return product.stock * product.unit_price;
}

int main() {
    const Product tea{"Tea", 3, 8, 6};
    const Product rice{"Rice", 8, 8, 4};

    const int tea_value{stock_value(tea)};
    const int rice_value{stock_value(rice)};

    std::cout << tea.name << " stock value: " << tea_value << "\n";
    std::cout << rice.name << " stock value: " << rice_value << "\n";
}
```

**Przewidź** obie linijki, a potem uruchom program.

<details>
<summary>Standardowe wyjście</summary>

<!-- output: stock_values -->
```text
Tea stock value: 18
Rice stock value: 32
```

</details>

- **`Product` to nasz typ,** tutaj w roli typu parametru. Definicja struktury stoi przed funkcją, bo funkcja korzysta z typu `Product` już w swoim nagłówku.
- **`product` to nazwa parametru.** W pierwszym wywołaniu oznacza obiekt `tea`, a w drugim `rice`. Funkcja nie zna nazw obiektów z `main`, tak jak `count_cold_days` z lekcji 6.4 nie znała nazw wektorów. Wielka litera odróżnia typ `Product` od parametru `product`.
- **`product.stock` i `product.unit_price`** odczytują dwa pola przekazanego rekordu. Wynik zależy od dwóch pól jednego obiektu.
- **Funkcja zwraca `int`:** wartość zapasu. Niczego nie wypisuje i nie zmienia rekordu: wypisuje `main`.
- **Wzór stoi w kodzie raz,** a działa dla obu produktów: `3 * 6` daje 18, a `8 * 4` daje 32.

## 3. Co znaczy `const Product&`

| Część | Znaczenie |
|---|---|
| `Product` | typ parametru: nasz własny typ |
| `&` | parametr odnosi się do istniejącego obiektu z miejsca wywołania, a nie jest jego kopią |
| `const` | przez ten parametr funkcja może rekord tylko odczytywać |
| `product` | nazwa parametru, przez którą funkcja odczytuje pola: `product.stock` |

To ten sam zapis co `const std::vector<int>&` w lekcji 6.4 i `const std::string&` w lekcji 7.3, tylko z naszym typem. Model się nie zmienia: **funkcja dostaje możliwość odczytania istniejącego rekordu, bez tworzenia jego kopii.** W czasie wywołania `stock_value(tea)` nazwa `product` to inna nazwa obiektu `tea`.

- **Przez `const&` nie zmienisz pola.** Linijka `product.stock = 0;` w tej funkcji by się nie zbudowała, podobnie jak zmiana pola obiektu `const` w lekcji 8.2.
- **`const` dotyczy dostępu przez parametr.** Obiekt w `main` nie staje się przez to stały. `tea` i `rice` mają `const`, bo `main` ich nie zmienia, ale to osobna decyzja, jak przy wektorze w lekcji 6.4.

## 4. Druga funkcja: odpowiedź tak albo nie

O ten sam produkt można zadać drugie pytanie: **czy stan jest mniejszy od wymaganego minimum?** Dopisz pod `stock_value` drugą funkcję i zmień `main` tak jak niżej:

<!-- example: restock_check -->
```cpp
#include <iostream>
#include <string>

struct Product {
    std::string name;
    int stock;
    int minimum;
    int unit_price;
};

int stock_value(const Product& product) {
    return product.stock * product.unit_price;
}

bool needs_restock(const Product& product) {
    return product.stock < product.minimum;
}

int main() {
    const Product tea{"Tea", 3, 8, 6};

    const int value{stock_value(tea)};
    const bool restock{needs_restock(tea)};

    std::cout << "Product: " << tea.name << "\n";
    std::cout << "Stock value: " << value << "\n";

    if (restock) {
        std::cout << "Restock needed: yes\n";
    } else {
        std::cout << "Restock needed: no\n";
    }
}
```

**Przewidź** wszystkie trzy linijki, a potem uruchom program.

<details>
<summary>Standardowe wyjście</summary>

<!-- output: restock_check -->
```text
Product: Tea
Stock value: 18
Restock needed: yes
```

</details>

- **Parametr jest taki sam** jak w `stock_value`: `const Product&`.
- **Funkcja odczytuje inne pola:** `stock` i `minimum`, a nie cenę.
- **Wynik ma inny typ:** `bool`, bo funkcja odpowiada na pytanie tak albo nie, jak `is_even` w lekcji 5.3.
- **Funkcja nadal niczego nie wypisuje.** Tekst `yes` albo `no` wybiera `main` przez `if`.

| Funkcja | Pytanie | Odczytywane pola | Wynik |
|---|---|---|---|
| `stock_value` | jaka jest wartość zapasu? | `stock`, `unit_price` | `int` |
| `needs_restock` | czy stan jest poniżej minimum? | `stock`, `minimum` | `bool` |

Tak przebiega program:

| Etap | Co się dzieje |
|---|---|
| `main` tworzy rekord | `tea`: `Tea`, 3, 8, 6 |
| `stock_value(tea)` | `product` odnosi się do `tea`; funkcja oblicza `3 * 6` i zwraca 18 |
| `needs_restock(tea)` | `product` znowu odnosi się do `tea`; `3 < 8` daje `true` |
| `main` wypisuje raport | nazwę z `tea.name`, liczbę 18 i, przez `if`, `yes` |
| po obu wywołaniach | `tea` ma nadal te same pola: `Tea`, 3, 8, 6 |

Do funkcji trafia cały rekord, a do `main` wraca jedna prosta wartość. Funkcja nie tworzy nowego rekordu ani kopii, tylko liczy z pól istniejącego obiektu. `main` korzysta z wyników i nie powtarza wzorów.

## 5. Przez wartość, kopia i `const&`

| Zapis | Co się dzieje |
|---|---|
| `Product copy{original};` | powstaje niezależny obiekt z wartościami pól oryginału (lekcja 8.2) |
| `int stock_value(Product product)` | parametr przez wartość: przy każdym wywołaniu powstaje osobny obiekt parametru z wartościami pól argumentu |
| `int stock_value(const Product& product)` | parametr `const&`: funkcja odczytuje istniejący obiekt przez referencję, bez kopii |

- **Przekazanie rekordu przez wartość to poprawny C++.** Funkcja z parametrem `Product product` też by się zbudowała i zwróciła ten sam wynik. Parametr byłby wtedy kopią argumentu, jak `before` w lekcji 8.2, także z własną kopią tekstu z pola `std::string`.
- **`const&` pozwala uniknąć tej kopii** przy zwykłym odczycie. Dlatego rekord, który funkcja tylko czyta, przekazujemy przez `const&`, jak wektor i tekst, a pojedyncze liczby nadal przez wartość (lekcja 6.4).
- **Nie znaczy to, że przekazywanie przez wartość jest zawsze złe.** Wybieramy `const&`, bo funkcje z tej lekcji tylko czytają rekordy.
- **Parametr `const&` to nie kopia z lekcji 8.2.** Kopia jest osobnym obiektem z własnymi wartościami, a parametr `const&` to inna nazwa obiektu z miejsca wywołania.

## 6. Misja: kontrola wypożyczenia sprzętu

Wypożyczalnia sprzętu sprawdza jedno wypożyczenie urządzenia. Program odpowiada na pytanie: **czy trzeba skontaktować się z osobą, która wypożyczyła sprzęt?**

**Dane:** urządzenie `Camera`, używane 9 dni, dozwolone 7 dni, jeszcze niezwrócone.

**Reguły:**

- Liczby dni są całkowite i nieujemne.
- **Liczba dni opóźnienia:** gdy liczba dni korzystania przekracza dozwoloną liczbę dni, to ich różnica, a w przeciwnym razie 0. Opóźnienie nigdy nie jest ujemne.
- **Kontakt jest potrzebny** tylko wtedy, gdy wypożyczenie jest opóźnione **i** urządzenie nie zostało jeszcze zwrócone.

Liczba dni opóźnienia opisuje przebieg wypożyczenia, a potrzeba kontaktu bieżącą decyzję. To celowo dwa różne pytania: urządzenie oddane po terminie ma dodatnią liczbę dni opóźnienia, ale kontakt nie jest już potrzebny.

**Wymagania:**

- Program definiuje własny typ z czterema polami: nazwą urządzenia, liczbą dni korzystania, dozwoloną liczbą dni i informacją, czy urządzenie zwrócono. Nazwę typu, nazwy pól, ich typy i kolejność wybierasz samodzielnie.
- Program ma dwie własne funkcje, które analizują rekord: pierwsza oblicza liczbę dni opóźnienia, a druga ustala, czy potrzebny jest kontakt. Każda dostaje cały rekord przez `const&`, zwraca jeden wynik, nie zmienia rekordu, niczego nie wypisuje ani nie odczytuje z wejścia. Nazwy funkcji i parametrów oraz typy wyników wybierasz samodzielnie.
- Druga funkcja może korzystać z pierwszej, ale nie musi.
- `main` tworzy jeden obiekt `const` z danymi wypożyczenia, wywołuje obie funkcje, odbiera ich wyniki i wypisuje raport. Sam nie oblicza liczby dni opóźnienia, nie decyduje o kontakcie i nie odczytuje niczego z wejścia.
- Program wypisuje dokładnie sześć linijek, jak w przykładzie niżej: `Item`, `Days used`, `Allowed days`, `Returned`, `Overdue days` i `Contact needed`. Linijki `Returned` i `Contact needed` kończą się słowem `yes` albo `no`.

W `cpp-workspace` utwórz katalog `equipment_loan`, skopiuj do niego `CMakeLists.txt` z oryginalnego `lesson_05_first_program`, utwórz pusty `main.cpp` i napisz program samodzielnie.

Dla danych powyżej standardowe wyjście ma być takie:

<!-- output: equipment_loan -->
```text
Item: Camera
Days used: 9
Allowed days: 7
Returned: no
Overdue days: 2
Contact needed: yes
```

Kamera była używana o 2 dni dłużej, niż pozwala wypożyczenie, i nadal nie wróciła, więc trzeba się skontaktować.

**To nie jest program o produktach z innymi nazwami.** Musisz samodzielnie zdecydować:

1. jak nazwać typ, jego pola i obie funkcje;
2. jaki typ ma każde pole i jaki typ wyniku ma każda funkcja;
3. których pól potrzebuje każda funkcja;
4. jak sprawić, żeby liczba dni opóźnienia nigdy nie była ujemna;
5. jak druga funkcja połączy opóźnienie z informacją o zwrocie i czy skorzysta z pierwszej funkcji;
6. w jakiej kolejności zdefiniować funkcje;
7. co robi `main`, a czego robić nie powinien.

**Zanim napiszesz program**, przygotuj tabelę przypadków: brak opóźnienia, limit osiągnięty dokładnie, przekroczony limit przy urządzeniu niezwróconym i zwróconym, zwrot w terminie, zero dozwolonych dni i zero dni korzystania. Przy każdym zapisz `Overdue days` i `Contact needed`.

**Potem** uruchom program dla danych z wymagań i dla dwóch innych przypadków z tabeli, na przykład dla limitu osiągniętego dokładnie i dla urządzenia zwróconego po terminie. Zmieniaj przy tym tylko wartości w klamrach obiektu. Wszystkie przypadki z pełnej listy kontrolnej są sprawdzone automatycznie.

### Kryterium sukcesu

- Program buduje się jako C++20 i dla danych z wymagań wypisuje dokładnie sześć linijek pokazanych wyżej.
- Jest jeden typ z czterema polami i jeden obiekt `const` tego typu.
- Obie funkcje dostają rekord przez `const&`, niczego nie wypisują i nie zmieniają rekordu.
- Pierwsza funkcja zwraca liczbę dni, nigdy ujemną. Druga zwraca odpowiedź tak albo nie, a tekst `yes` albo `no` wybiera `main`.
- Liczba dni równa limitowi nie jest opóźnieniem, a zwrócone urządzenie nigdy nie wymaga kontaktu.
- `main` nie powtarza obliczeń funkcji.
- Tabela przypadków powstała przed uruchomieniem programu.
- Umiesz powiedzieć, za co odpowiada każda funkcja, a za co `main`.

Gdy wynik się zgadza, możesz zapisać projekt w Gicie, jak w lekcji 1.5.

<details>
<summary>Podpowiedź 1</summary>

Które informacje opisują jedno wypożyczenie? Czy obie funkcje mogą otrzymać ten sam rekord?

</details>

<details>
<summary>Podpowiedź 2</summary>

Pierwsza funkcja oblicza liczbę dni, druga odpowiada tak albo nie. Jakie pola są potrzebne w każdej z nich?

</details>

<details>
<summary>Podpowiedź 3</summary>

Liczba dni opóźnienia nie może być ujemna. Kontakt ma sens tylko wtedy, gdy wypożyczenie jest po terminie i sprzęt nadal nie został zwrócony.

</details>

<details>
<summary>Pełna lista przypadków kontrolnych: otwórz po przygotowaniu własnej tabeli</summary>

| | Urządzenie | Dni | Limit | Zwrócone | Opóźnienie | Kontakt | Co sprawdza |
|---|---|---:|---:|---|---:|---|---|
| A | `Camera` | 9 | 7 | no | 2 | yes | dane z wymagań: limit przekroczony, sprzęt niezwrócony |
| B | `Tripod` | 5 | 7 | no | 0 | no | przed terminem |
| C | `Cable` | 7 | 7 | no | 0 | no | limit osiągnięty dokładnie |
| D | `Mixer` | 10 | 7 | yes | 3 | no | zwrot po terminie: opóźnienie bez kontaktu |
| E | `Lens` | 10 | 7 | no | 3 | yes | te same dni co D, ale bez zwrotu |
| F | `Light` | 0 | 0 | no | 0 | no | zero dni i zero dozwolonych dni |
| G | `Microphone` | 1 | 0 | no | 1 | yes | zero dozwolonych dni |
| H | `Screen` | 8 | 8 | yes | 0 | no | zwrot dokładnie w terminie |
| I | `Battery` | 5 | 3 | yes | 2 | no | zwrot po terminie przy innym limicie |
| J | `Charger` | 0 | 5 | no | 0 | no | zero dni korzystania |

**Testy automatyczne i Twoje próby.** Wszystkie przypadki są sprawdzone automatycznie przez program kontrolny. Ma on ten sam typ, te same funkcje i ten sam raport co rozwiązanie referencyjne, ale dane wypożyczenia odczytuje z wejścia, po jednej wartości w linijce. To tylko narzędzie do sprawdzania, a nie część misji: w misji dane są wpisane w kodzie. Program kontrolny i jego wyniki są w części [Przykładowe rozwiązania](#przykładowe-rozwiązania), bo zawierają rozwiązanie.

</details>

Przykładowe rozwiązanie jest w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 7. Znajdź błąd: zamienione pola w odejmowaniu

To zadanie wykonaj **po misji**: program poniżej zawiera funkcje podobne do Twoich. Ktoś sprawdza w nim wypożyczenie statywu. Program możesz przepisać albo skopiować do `main.cpp`.

<details>
<summary>Program do sprawdzenia: otwórz po napisaniu własnego programu</summary>

<!-- example: loan_overdue_bug -->
```cpp
#include <iostream>
#include <string>

struct Loan {
    std::string item;
    int days_used;
    int allowed_days;
    bool returned;
};

int overdue_days(const Loan& loan) {
    if (loan.days_used > loan.allowed_days) {
        return loan.allowed_days - loan.days_used;
    }

    return 0;
}

bool needs_contact(const Loan& loan) {
    return overdue_days(loan) > 0 && !loan.returned;
}

int main() {
    const Loan loan{"Tripod", 5, 7, false};

    std::cout << "Item: " << loan.item << "\n";
    std::cout << "Overdue days: " << overdue_days(loan) << "\n";

    if (needs_contact(loan)) {
        std::cout << "Contact needed: yes\n";
    } else {
        std::cout << "Contact needed: no\n";
    }
}
```

1. **Przewidź** standardowe wyjście dla danych z programu: statyw używany 5 dni przy dozwolonych 7, niezwrócony. Potem uruchom program. Czy wynik wygląda poprawnie?
2. Która linijka `overdue_days` zwraca wynik dla tych danych? Których linijek tej funkcji program wtedy w ogóle nie wykonuje?
3. Zmień wartości w `{}` tak, żeby błąd stał się widoczny. Najpierw zapisz poprawny wynik dla swoich danych, a potem uruchom program.
4. Prześledź przepływ danych dla swoich danych: które pola trafiają do odejmowania, jaką liczbę zwraca `overdue_days` i co z tą liczbą robi `needs_contact`.
5. Wskaż linijkę z błędem. Dlaczego kompilator jej nie zgłosił?
6. Popraw funkcję.
7. Uruchom poprawiony program dla swoich danych.

</details>

Wyniki, przykładowe dane i poprawiony program są w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 8. Gdy coś pójdzie inaczej

| Co widzisz | Co to znaczy | Co zrobić |
|---|---|---|
| `cannot assign to variable 'product' with const-qualified type 'const Product &'` | Funkcja zmienia pole przez parametr `const&`. | Funkcja analizująca tylko czyta rekord: oblicz wynik i go zwróć. |
| `unknown type name` z nazwą Twojego typu, w nagłówku funkcji | Funkcja stoi w pliku przed definicją struktury. | Umieść definicję struktury przed funkcjami, które z niej korzystają. |
| `use of undeclared identifier` w funkcji | Funkcja używa nazwy, której tu nie zna: samego pola (`stock`), obiektu z `main` (`tea`) albo funkcji zdefiniowanej niżej. | Pola odczytuj przez parametr: `product.stock`, a nie według podpowiedzi z `Product::`. Wywoływaną funkcję zdefiniuj wyżej. |
| Ostrzeżenie `address of function ... will always evaluate to 'true'`, a program zawsze wypisuje `yes` | W warunku stoi sama nazwa funkcji, bez wywołania. | Wywołaj funkcję z argumentem, na przykład `needs_restock(tea)`. |
| Program działa, choć parametr nie ma `const&` | Parametr przez wartość to poprawny C++, ale funkcja dostaje kopię rekordu (punkt 5). | W misji przekaż rekord przez `const&`: funkcja go tylko czyta. |
| `Overdue days` jest ujemne | Pola stoją w odejmowaniu w odwrotnej kolejności (punkt 7). | Od liczby dni korzystania odejmij dozwoloną liczbę dni. |
| Opóźnienie wychodzi także dla liczby dni równej limitowi | Warunek używa `>=` zamiast `>`. | Opóźnienie jest tylko wtedy, gdy liczba dni **przekracza** limit. |
| `Contact needed: yes` dla zwróconego urządzenia | Druga funkcja sprawdza tylko opóźnienie. | Kontakt wymaga też, żeby urządzenie nie zostało zwrócone. |

## 9. Wyjaśnij

Odpowiedz własnymi słowami, najlepiej na piśmie. Dopiero potem porównaj z przykładowymi odpowiedziami.

1. Co oznacza parametr `const Product& product`? Co jest w nim typem, a co nazwą?
2. Czy `stock_value(tea)` dostaje kopię całego rekordu? Czym jej parametr różni się od `const Product snapshot{tea};`?
3. Jak funkcja odczytuje pole przekazanego rekordu? Dlaczego nie pisze `tea.stock`?
4. Czy funkcja może zmienić pole przez parametr `const&`? Czy obiekt w `main` staje się przez to stały?
5. Czy przekazanie rekordu przez wartość jest błędem? Dlaczego w tej lekcji wybieramy `const&`?
6. Kiedy wynik funkcji powinien mieć typ `int`, a kiedy `bool`? Podaj przykłady z tej lekcji.
7. Dlaczego obliczenia stoją w funkcjach, a wypisywanie w `main`?
8. Czy funkcja, która wywołuje inną funkcję, wymaga nowego mechanizmu C++? Co musi być spełnione?
9. Dlaczego dwa pola `int` łatwo pomylić w obliczeniu i dlaczego kompilator tego nie zauważy?
10. Jakie dane pozwalają odróżnić poprawny wzór na liczbę dni opóźnienia od wzoru z zamienionymi polami, a jakie na to nie pozwalają?

<details>
<summary>Przykładowe odpowiedzi</summary>

1. Funkcja dostaje dostęp do istniejącego obiektu typu `Product`, tylko do odczytu i bez kopii. `Product` to nasz własny typ, `&` oznacza referencję, `const` zakaz zmian przez parametr, a `product` to nazwa parametru.
2. Nie. Parametr `product` odnosi się do `tea`: na czas wywołania to inna nazwa tego samego obiektu. `const Product snapshot{tea};` tworzy nowy, osobny obiekt z kopią wartości wszystkich pól.
3. Przez nazwę parametru i kropkę: `product.stock`. Funkcja nie zna nazw obiektów z `main` i ma działać dla każdego produktu, który dostanie.
4. Nie: przez `const&` pole można tylko odczytać, a próba przypisania się nie zbuduje. Obiekt w `main` nie staje się przez to stały, bo `const` w parametrze dotyczy tylko dostępu przez ten parametr.
5. Nie, to poprawny C++. Parametr przez wartość jest jednak kopią całego rekordu, także tekstu z pola `std::string`. Funkcje z tej lekcji tylko czytają rekordy, więc kopia nie jest potrzebna.
6. `int`, gdy odpowiedzią jest liczba: wartość zapasu, liczba dni opóźnienia. `bool`, gdy odpowiedzią jest tak albo nie: czy uzupełnić zapas, czy potrzebny jest kontakt.
7. Bo funkcja z jednym zadaniem działa dla różnych rekordów, wzór stoi w jednym miejscu i da się go sprawdzić osobno. `main` tworzy dane, wywołuje funkcje i decyduje, co wypisać (lekcja 5.5).
8. Nie. Wywołuje się ją tak samo jak z `main`: nazwą, z argumentem w nawiasach. W miejscu wywołania kompilator musi już znać wywoływaną funkcję, więc jej definicja (albo deklaracja z lekcji 5.6) stoi wyżej w pliku.
9. Bo kompilator sprawdza typy, a nie znaczenie pól. `loan.allowed_days - loan.days_used` i `loan.days_used - loan.allowed_days` to dwa poprawne wyrażenia typu `int`. Tak samo w lekcji 8.1 zamienione wartości dwóch pól `int` budowały się bez błędu.
10. Pozwalają dane, dla których wzór naprawdę się wykonuje: liczba dni korzystania większa od limitu. Wtedy poprawny wzór daje liczbę dodatnią, a zamieniony ujemną. Dane bez opóźnienia, także z liczbą dni równą limitowi, kończą się na `return 0;` i w obu wersjach dają ten sam wynik.

</details>

## Podsumowanie

- Funkcja może dostać cały rekord. Parametr `const Product& product` daje jej dostęp do istniejącego obiektu, tylko do odczytu i bez kopii.
- Pola odczytujesz przez nazwę parametru, `product.stock`, a jedną funkcję wywołujesz dla różnych obiektów.
- Typ wyniku wynika z pytania: liczba to `int`, a odpowiedź tak albo nie to `bool`.
- Przekazanie rekordu przez wartość też jest poprawne, ale tworzy jego kopię. Do zwykłego odczytu wybieramy `const&`.
- Funkcje analizujące rekord liczą, a `main` tworzy dane, wywołuje funkcje i wypisuje raport.
- Wzór sprawdzasz danymi, dla których naprawdę się wykonuje.

## Co dalej

W tej lekcji każda funkcja analizowała jeden rekord. Kolejna lekcja Modułu 8 jest w przygotowaniu.

---

## Przykładowe rozwiązania

Zajrzyj tutaj **po własnej próbie**. Twoje nazwy mogą się różnić, jeśli standardowe wyjście jest takie, jak wymagane.

<details>
<summary>Punkt 6: misja, kontrola wypożyczenia</summary>

<!-- example: equipment_loan -->
```cpp
#include <iostream>
#include <string>

struct Loan {
    std::string item;
    int days_used;
    int allowed_days;
    bool returned;
};

int overdue_days(const Loan& loan) {
    if (loan.days_used > loan.allowed_days) {
        return loan.days_used - loan.allowed_days;
    }

    return 0;
}

bool needs_contact(const Loan& loan) {
    return overdue_days(loan) > 0 && !loan.returned;
}

int main() {
    const Loan loan{"Camera", 9, 7, false};

    const int overdue{overdue_days(loan)};
    const bool contact{needs_contact(loan)};

    std::cout << "Item: " << loan.item << "\n";
    std::cout << "Days used: " << loan.days_used << "\n";
    std::cout << "Allowed days: " << loan.allowed_days << "\n";

    if (loan.returned) {
        std::cout << "Returned: yes\n";
    } else {
        std::cout << "Returned: no\n";
    }

    std::cout << "Overdue days: " << overdue << "\n";

    if (contact) {
        std::cout << "Contact needed: yes\n";
    } else {
        std::cout << "Contact needed: no\n";
    }
}
```

1. **Własny typ,** bo cztery dane opisują jedno wypożyczenie: nazwa, liczba dni, limit i zwrot należą do jednego rekordu.
2. **Cały rekord w funkcji,** bo każda funkcja potrzebuje kilku pól tego samego wypożyczenia. Jeden parametr zamiast kilku pól nie pozwala pomylić kolejności argumentów.
3. **`const&`,** bo funkcje tylko czytają rekord.
4. **Bez kopii:** w czasie wywołania parametr `loan` odnosi się do obiektu z `main`, który też nazywa się `loan`. Łączy je wywołanie, a nie nazwa. Kopia z lekcji 8.2 nie jest potrzebna: nikt nie zmienia rekordu ani nie musi pamiętać jego starego stanu.
5. **`int`,** bo `overdue_days` odpowiada na pytanie „ile dni?”.
6. **`bool`,** bo `needs_contact` odpowiada na pytanie „czy?”. Tekst `yes` albo `no` wybiera `main`.
7. **Pola a wyniki:** liczba dni opóźnienia zależy od `days_used` i `allowed_days`, a potrzeba kontaktu od opóźnienia i od `returned`. Nazwa urządzenia nie wpływa na żaden wynik: trafia tylko do raportu.
8. **Opóźnienie nie jest ujemne:** odejmowanie wykonuje się tylko wtedy, gdy liczba dni przekracza limit, więc różnica jest dodatnia. W pozostałych przypadkach funkcja zwraca 0. Dla 0 dni i limitu 0 wartości są równe, a 0 nie przekracza 0, więc opóźnienie wynosi 0. Bez opóźnienia kontakt nie jest potrzebny.
9. **Zwrócony sprzęt:** `needs_contact` wymaga opóźnienia **i** braku zwrotu (`&&` i `!` z lekcji 3.4). Zwrot po terminie zostawia dodatnie opóźnienie, na przykład 3 dni dla `Mixer`, ale kontakt nie jest już potrzebny.
10. **Wypisywanie w `main`:** funkcje tylko liczą. `main` tworzy rekord, wywołuje funkcje, zapisuje ich wyniki i wypisuje raport, bez powtarzania obliczeń.
11. **Rekord się nie zmienia:** obiekt jest `const`, a funkcje dostają `const&`, więc kompilator nie pozwoliłby zmienić pola. Raport wypisuje pola już po obu wywołaniach i pokazuje te same wartości, które stoją w `{}`.
12. **Bez nowego rekordu:** funkcja zwracająca liczbę oblicza ją z pól istniejącego rekordu i zwraca samą liczbę. Nie tworzy obiektu `Loan` ani kopii.

**Kolejność definicji:** `needs_contact` wywołuje `overdue_days`, więc `overdue_days` stoi w pliku wyżej, jak funkcje pomocnicze w lekcji 5.5. Osobne deklaracje z lekcji 5.6 nie są potrzebne.

**Inne poprawne rozwiązania:** druga funkcja może sprawdzić warunki samodzielnie, `return loan.days_used > loan.allowed_days && !loan.returned;`, bo opóźnienie jest dodatnie dokładnie wtedy, gdy liczba dni przekracza limit. Wywołanie pierwszej funkcji ma tę zaletę, że reguła opóźnienia stoi w jednym miejscu. Pierwsza funkcja może mieć `if` i `else`. Pola mogą mieć inne nazwy i inną kolejność, jeśli wartości w `{}` stoją w tej samej kolejności co pola.

**Program kontrolny** sprawdza wszystkie przypadki z listy kontrolnej. Struktura i obie funkcje są takie same jak wyżej, a `main` od utworzenia obiektu też, poza wcięciem. Różnica jest jedna: dane wypożyczenia są odczytywane z wejścia do zwykłych zmiennych, a obiekt `loan` powstaje z ich wartości. Nazwy urządzeń mają jedno słowo, więc wszystko odczytuje `>>`. Informację o zwrocie program odczytuje jako tekst `yes` albo `no` i zamienia na `bool` porównaniem, jak w lekcji 3.4.

<!-- example: equipment_loan_check -->
```cpp
#include <iostream>
#include <string>

struct Loan {
    std::string item;
    int days_used;
    int allowed_days;
    bool returned;
};

int overdue_days(const Loan& loan) {
    if (loan.days_used > loan.allowed_days) {
        return loan.days_used - loan.allowed_days;
    }

    return 0;
}

bool needs_contact(const Loan& loan) {
    return overdue_days(loan) > 0 && !loan.returned;
}

int main() {
    std::string item{};
    int days_used{0};
    int allowed_days{0};
    std::string returned_answer{};

    std::cin >> item;
    std::cin >> days_used;
    std::cin >> allowed_days;
    std::cin >> returned_answer;

    if (std::cin.fail()) {
        std::cout << "Input could not be read\n";
    } else {
        const Loan loan{item, days_used, allowed_days, returned_answer == "yes"};

        const int overdue{overdue_days(loan)};
        const bool contact{needs_contact(loan)};

        std::cout << "Item: " << loan.item << "\n";
        std::cout << "Days used: " << loan.days_used << "\n";
        std::cout << "Allowed days: " << loan.allowed_days << "\n";

        if (loan.returned) {
            std::cout << "Returned: yes\n";
        } else {
            std::cout << "Returned: no\n";
        }

        std::cout << "Overdue days: " << overdue << "\n";

        if (contact) {
            std::cout << "Contact needed: yes\n";
        } else {
            std::cout << "Contact needed: no\n";
        }
    }
}
```

Każdy przypadek to cztery linijki wejścia: nazwa urządzenia, liczba dni korzystania, dozwolona liczba dni oraz `yes` albo `no` dla zwrotu, w kolejności z listy kontrolnej, od A do J.

<!-- input: equipment_loan_check -->
```text
Camera
9
7
no
```

<!-- output: equipment_loan_check -->
```text
Item: Camera
Days used: 9
Allowed days: 7
Returned: no
Overdue days: 2
Contact needed: yes
```

<!-- input: equipment_loan_check -->
```text
Tripod
5
7
no
```

<!-- output: equipment_loan_check -->
```text
Item: Tripod
Days used: 5
Allowed days: 7
Returned: no
Overdue days: 0
Contact needed: no
```

<!-- input: equipment_loan_check -->
```text
Cable
7
7
no
```

<!-- output: equipment_loan_check -->
```text
Item: Cable
Days used: 7
Allowed days: 7
Returned: no
Overdue days: 0
Contact needed: no
```

<!-- input: equipment_loan_check -->
```text
Mixer
10
7
yes
```

<!-- output: equipment_loan_check -->
```text
Item: Mixer
Days used: 10
Allowed days: 7
Returned: yes
Overdue days: 3
Contact needed: no
```

<!-- input: equipment_loan_check -->
```text
Lens
10
7
no
```

<!-- output: equipment_loan_check -->
```text
Item: Lens
Days used: 10
Allowed days: 7
Returned: no
Overdue days: 3
Contact needed: yes
```

<!-- input: equipment_loan_check -->
```text
Light
0
0
no
```

<!-- output: equipment_loan_check -->
```text
Item: Light
Days used: 0
Allowed days: 0
Returned: no
Overdue days: 0
Contact needed: no
```

<!-- input: equipment_loan_check -->
```text
Microphone
1
0
no
```

<!-- output: equipment_loan_check -->
```text
Item: Microphone
Days used: 1
Allowed days: 0
Returned: no
Overdue days: 1
Contact needed: yes
```

<!-- input: equipment_loan_check -->
```text
Screen
8
8
yes
```

<!-- output: equipment_loan_check -->
```text
Item: Screen
Days used: 8
Allowed days: 8
Returned: yes
Overdue days: 0
Contact needed: no
```

<!-- input: equipment_loan_check -->
```text
Battery
5
3
yes
```

<!-- output: equipment_loan_check -->
```text
Item: Battery
Days used: 5
Allowed days: 3
Returned: yes
Overdue days: 2
Contact needed: no
```

<!-- input: equipment_loan_check -->
```text
Charger
0
5
no
```

<!-- output: equipment_loan_check -->
```text
Item: Charger
Days used: 0
Allowed days: 5
Returned: no
Overdue days: 0
Contact needed: no
```

</details>

<details>
<summary>Punkt 7: wyniki przed poprawką i poprawiony program</summary>

Przed poprawką, dla statywu używanego 5 dni przy dozwolonych 7:

<!-- output: loan_overdue_bug -->
```text
Item: Tripod
Overdue days: 0
Contact needed: no
```

- **Wynik wygląda poprawnie.** 5 nie przekracza 7, więc warunek w `overdue_days` jest fałszywy i funkcja zwraca 0 z ostatniej linijki. Odejmowanie w ogóle się nie wykonuje, więc błąd w nim nie ma wpływu na wynik. Poprawna funkcja zwróciłaby to samo.
- **Dane, które ujawniają błąd:** każde, w których liczba dni korzystania przekracza limit. Na przykład dane z misji: `Camera`, 9 dni przy dozwolonych 7, niezwrócona. Poprawny wynik to 2 dni opóźnienia i potrzebny kontakt. Program z błędem wypisuje:

<!-- example: loan_overdue_revealed -->
```cpp
#include <iostream>
#include <string>

struct Loan {
    std::string item;
    int days_used;
    int allowed_days;
    bool returned;
};

int overdue_days(const Loan& loan) {
    if (loan.days_used > loan.allowed_days) {
        return loan.allowed_days - loan.days_used;
    }

    return 0;
}

bool needs_contact(const Loan& loan) {
    return overdue_days(loan) > 0 && !loan.returned;
}

int main() {
    const Loan loan{"Camera", 9, 7, false};

    std::cout << "Item: " << loan.item << "\n";
    std::cout << "Overdue days: " << overdue_days(loan) << "\n";

    if (needs_contact(loan)) {
        std::cout << "Contact needed: yes\n";
    } else {
        std::cout << "Contact needed: no\n";
    }
}
```

<!-- output: loan_overdue_revealed -->
```text
Item: Camera
Overdue days: -2
Contact needed: no
```

| Krok | Wartość |
|---|---|
| `loan.days_used > loan.allowed_days` | `9 > 7` daje `true` |
| `loan.allowed_days - loan.days_used` | `7 - 9` daje -2 |
| `overdue_days(loan)` | zwraca -2 |
| `overdue_days(loan) > 0` w `needs_contact` | `-2 > 0` daje `false` |
| `needs_contact(loan)` | zwraca `false`, choć sprzęt nie wrócił |

- **Przyczyna:** warunek poprawnie rozpoznaje przekroczony limit, ale wzór odejmuje pola w odwrotnej kolejności: od limitu odejmuje liczbę dni korzystania. Oba pola mają typ `int`, więc kompilator przyjmuje oba wyrażenia, jak zamienione wartości w lekcji 8.1.
- **Jeden błędny wzór psuje dwie linijki.** `needs_contact` korzysta z wyniku `overdue_days`, więc ujemne opóźnienie sprawia, że kontakt znika. Dla urządzenia już zwróconego błędna byłaby tylko linijka `Overdue days`.
- **Poprawka:** od liczby dni korzystania odejmij dozwoloną liczbę dni: `return loan.days_used - loan.allowed_days;`.

<!-- example: loan_overdue_fixed -->
```cpp
#include <iostream>
#include <string>

struct Loan {
    std::string item;
    int days_used;
    int allowed_days;
    bool returned;
};

int overdue_days(const Loan& loan) {
    if (loan.days_used > loan.allowed_days) {
        return loan.days_used - loan.allowed_days;
    }

    return 0;
}

bool needs_contact(const Loan& loan) {
    return overdue_days(loan) > 0 && !loan.returned;
}

int main() {
    const Loan loan{"Camera", 9, 7, false};

    std::cout << "Item: " << loan.item << "\n";
    std::cout << "Overdue days: " << overdue_days(loan) << "\n";

    if (needs_contact(loan)) {
        std::cout << "Contact needed: yes\n";
    } else {
        std::cout << "Contact needed: no\n";
    }
}
```

<!-- output: loan_overdue_fixed -->
```text
Item: Camera
Overdue days: 2
Contact needed: yes
```

Dla danych statywu poprawiony program wypisuje to samo co przed poprawką, bo dla nich funkcja nadal kończy się na `return 0;`. Dlatego dane bez opóźnienia nie wystarczą, żeby sprawdzić wzór: trzeba danych, dla których wzór naprawdę się wykonuje.

</details>

**Poprzednia lekcja:** [Lekcja 8.2: Zmiana pól i niezależna kopia rekordu](lesson_02_changing_fields_and_copies.md) · **Następna lekcja:** w przygotowaniu · [Opis kursu](../../README.md)

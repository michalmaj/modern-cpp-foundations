# Lekcja 9.2: Zmiana tylko po spełnieniu warunków

**Polski** · [English](lesson_02_a_change_only_when_allowed.en.md) · [Opis kursu](../../README.md)

> **Moduł 9, lekcja 2** · około 75–90 minut
> **Potrzebujesz:** katalogu `cpp-workspace` i oryginalnego projektu `lesson_05_first_program`, jak dotąd. Debugger nie jest w tej lekcji potrzebny.
> **Wersja pilotażowa.** Programy z tej lekcji sprawdzamy automatycznie na Windowsie, Ubuntu i macOS. Żaden z nich nie pyta o dane: wszystkie wartości są zapisane w kodzie. Dane z wejścia odczytuje tylko program kontrolny w części z rozwiązaniami.

## Zanim zaczniesz

Ta lekcja zakłada, że:

- piszesz funkcję z parametrem `Product&`, która zmienia przekazany rekord (lekcja 9.1);
- piszesz funkcje zwracające `bool` (lekcja 5.3) i klauzule ochronne z wcześniejszym `return` (lekcja 5.4);
- łączysz warunki operatorem `||` i wiesz, że jego prawa strona nie jest obliczana, gdy lewa już rozstrzyga wynik (lekcja 3.4);
- znasz zasadę „w całości albo wcale” z rezerwacji w lekcji 8.2, gdzie `main` sprawdzał wolne miejsca przed zmianą pola.

## Sytuacja

Magazyn wydaje towar. Produkt `Tea` ma 8 sztuk. Wydanie 3 sztuk jest możliwe, ale wydanie 6 z pozostałych 5 już nie: stan nie może spaść poniżej zera. Funkcja z lekcji 9.1 zmieniała rekord zawsze. Tutaj zmiana jest dozwolona tylko po spełnieniu warunków, a wywołujący musi się dowiedzieć, czy operacja została przyjęta.

W lekcji 8.2 warunek sprawdzał `main`. Gdyby towar był wydawany w kilku miejscach programu, reguła stałaby w każdym z nich, a jedno pominięte sprawdzenie zepsułoby rekord. Teraz reguła należy do funkcji, która zmienia rekord: funkcja najpierw sprawdza warunki, zmienia rekord tylko wtedy, gdy wolno, i zwraca `bool` z informacją, czy operację przyjęła.

Po tej lekcji będziesz:

- pisać funkcję z parametrem `&`, która zmienia rekord tylko po spełnieniu warunków i zwraca `bool`;
- odróżniać wynik funkcji (`true` albo `false`) od jej skutku (zmienionego rekordu);
- chronić rekord klauzulą ochronną: najpierw wszystkie sprawdzenia, potem wszystkie zmiany;
- zostawiać cały rekord bez zmian, gdy operacja zostaje odrzucona;
- przewidywać wynik i stan rekordu po serii przyjętych i odrzuconych operacji;
- dobierać dane, które ujawniają zmianę wykonaną przed sprawdzeniem.

## 1. Przygotuj projekt

W `cpp-workspace` utwórz katalog `lesson_9_2` i skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program`. Program z punktu 2 wpisujesz w `main.cpp` tego katalogu. Typ `Product` znasz z lekcji 9.1.

## 2. Wydanie towaru

<!-- example: issue -->
```cpp
#include <iostream>
#include <string>

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

int main() {
    Product tea{"Tea", 8, 8, 6};

    std::cout << "Product: " << tea.name << "\n";
    std::cout << "Before: " << tea.stock << "\n";

    const bool first_accepted{issue_units(tea, 3)};

    if (first_accepted) {
        std::cout << "Issue 3: accepted\n";
    } else {
        std::cout << "Issue 3: refused\n";
    }

    std::cout << "After first: " << tea.stock << "\n";

    const bool second_accepted{issue_units(tea, 6)};

    if (second_accepted) {
        std::cout << "Issue 6: accepted\n";
    } else {
        std::cout << "Issue 6: refused\n";
    }

    std::cout << "After second: " << tea.stock << "\n";
}
```

**Przewidź** wszystkie sześć linijek, a potem uruchom program. Szczególnie: czy drugie wydanie zostanie przyjęte?

<details>
<summary>Standardowe wyjście</summary>

<!-- output: issue -->
```text
Product: Tea
Before: 8
Issue 3: accepted
After first: 5
Issue 6: refused
After second: 5
```

</details>

- **`Product& product`** pozwala zmienić istniejący produkt (lekcja 9.1). **`int amount`** funkcja tylko odczytuje, więc dostaje go przez wartość.
- **Warunek odmowy** łączy przez `||` dwa przypadki: ilość równą 0 albo mniejszą i ilość większą niż stan. Gdy zachodzi którykolwiek, funkcja zwraca `false`, a stan się nie zmienia.
- **Dopiero po sprawdzeniu** funkcja odejmuje ilość. Wiadomo już wtedy, że `amount` nie przekracza `product.stock`, więc stan nie spadnie poniżej zera. **`return true;`** oznacza, że operacja została przyjęta i wykonana.
- **Drugie wywołanie widzi stan po pierwszym:** zostało 5 sztuk, więc 6 to za dużo.
- **`main` zapisuje wynik każdego wywołania w zmiennej `bool`.** Funkcja wykonuje się raz, przy inicjalizacji zmiennej: zmienia rekord albo nie i zwraca wynik. `if` sprawdza potem tylko zapisany wynik.
- **Funkcja niczego nie wypisuje.** O odmowie informuje wynikiem, a raport należy do `main`.

## 3. Wynik i skutek

Funkcja `issue_units` ma **skutek**, czyli zmieniony rekord, i **wynik**, czyli `true` albo `false` przekazane do miejsca wywołania. To dwie niezależne cechy.

| Funkcja | Skutek |
|---|---|
| `void receive_delivery(Product& product, int delivered)` | zmienia rekord, nie zwraca wartości |
| `bool issue_units(Product& product, int amount)` | może zmienić rekord i informuje o powodzeniu |
| funkcja z parametrem `const Product&` i wynikiem `Product` | tworzy nową wartość, nie zmienia oryginału przez parametr |

- **`void` nie jest obowiązkowy dla funkcji, która zmienia rekord.** Dostawa z lekcji 9.1 była przyjmowana zawsze, więc nie było czego zgłaszać. Wydanie może zostać odrzucone.
- **`bool` to typ wyniku, a nie nowy sposób przekazania obiektu.** Obiekt nadal trafia do funkcji przez `&`.
- **Nowa wartość zamiast zmiany istniejącej nadal bywa dobrym projektem,** na przykład gdy oryginał ma zostać bez zmian (lekcja 8.5).

**Umowa w tej lekcji:** `true` oznacza, że operacja została przyjęta i wykonana. `false` oznacza odmowę, po której **wszystkie pola rekordu są bez zmian**. To umowa naszych funkcji, a nie znaczenie każdego `bool` w C++: `is_even` z lekcji 5.3 też zwraca `bool`, ale tylko odpowiada na pytanie.

Przyjmujemy tylko dodatnie ilości, więc `true` zawsze oznacza rzeczywistą zmianę, a ilość 0 zostaje odrzucona. W lekcji 8.2 zero nowych rezerwacji przyjmowało się jako aktualizację bez zmiany. To też poprawna umowa, tylko inna.

## 4. Klauzula ochronna chroni rekord

<!-- fragment -->
```cpp
if (amount <= 0 || amount > product.stock) {
    return false;
}
```

To znana z lekcji 5.4 klauzula ochronna. Gdy warunek jest spełniony, funkcja się kończy, `product.stock -= amount;` się nie wykonuje, a obiekt wywołującego zostaje bez zmian. To nie jest nowa konstrukcja C++. Nowe jest jej zadanie: klauzula chroni stan obiektu przekazanego przez `&`.

**Przewidź na papierze.** Produkt ma teraz 5 sztuk, jak po programie z punktu 2. Program wywołuje kolejno `issue_units(tea, 0)`, `issue_units(tea, 5)` i `issue_units(tea, 1)`. Dla każdego wywołania zapisz: ile wynosi `tea.stock` przed nim, jaką wartość mają oba warunki, który `return` się wykona, jaki jest wynik i ile wynosi `tea.stock` po wywołaniu.

<details>
<summary>Odpowiedź i program, który ją sprawdza</summary>

| Wywołanie | `tea.stock` przed | `amount <= 0` | `amount > product.stock` | Który `return` | Wynik | `tea.stock` po |
|---|---:|---|---|---|---|---:|
| `issue_units(tea, 0)` | 5 | `true` | **nie jest sprawdzany** | `return false;` | `false` | 5 |
| `issue_units(tea, 5)` | 5 | `false` | `false` | `return true;` | `true` | 0 |
| `issue_units(tea, 1)` | 0 | `false` | `true` | `return false;` | `false` | 0 |

- **0 sztuk:** lewa strona `||` jest prawdziwa, więc prawa nie jest obliczana (lekcja 3.4). Odmowa.
- **5 sztuk z 5:** wydanie całego stanu jest dozwolone, bo 5 nie jest większe od 5. Stan spada do 0.
- **1 sztuka z 0:** za mało towaru. Odmowa nie zmienia stanu, który już wynosi 0.

Ten program wykonuje te trzy wywołania. Uruchomienie go jest nieobowiązkowe.

<!-- example: issue_boundaries -->
```cpp
#include <iostream>
#include <string>

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

int main() {
    Product tea{"Tea", 5, 8, 6};

    std::cout << "Before: " << tea.stock << "\n";

    const bool zero_accepted{issue_units(tea, 0)};

    if (zero_accepted) {
        std::cout << "Issue 0: accepted\n";
    } else {
        std::cout << "Issue 0: refused\n";
    }

    std::cout << "After: " << tea.stock << "\n";

    const bool all_accepted{issue_units(tea, 5)};

    if (all_accepted) {
        std::cout << "Issue 5: accepted\n";
    } else {
        std::cout << "Issue 5: refused\n";
    }

    std::cout << "After: " << tea.stock << "\n";

    const bool one_accepted{issue_units(tea, 1)};

    if (one_accepted) {
        std::cout << "Issue 1: accepted\n";
    } else {
        std::cout << "Issue 1: refused\n";
    }

    std::cout << "After: " << tea.stock << "\n";
}
```

<!-- output: issue_boundaries -->
```text
Before: 5
Issue 0: refused
After: 5
Issue 5: accepted
After: 0
Issue 1: refused
After: 0
```

</details>

## 5. Wszystko albo nic

**Najpierw sprawdzamy wszystkie warunki, a dopiero potem zmieniamy stan.**

Gdy operacja zmienia dwa pola, łatwo o błędny układ:

1. Zmień pierwsze pole.
2. Sprawdź warunek.
3. Jeśli warunek nie jest spełniony, zwróć `false`.

Taka funkcja zgłasza odmowę, ale zostawia rekord **częściowo zmieniony**: jedno pole już jest inne. Wywołujący dostaje `false` i zakłada, że nic się nie zmieniło.

Poprawny układ:

1. Sprawdź wszystkie wymagania.
2. Jeśli któreś nie jest spełnione, zakończ funkcję bez żadnej zmiany.
3. Jeśli wszystkie są spełnione, wykonaj wszystkie zaplanowane zmiany.
4. Zwróć `true`.

To zasada **„wszystko albo nic”**: operacja zmienia wszystkie pola, które ma zmienić, albo żadnego. W lekcji 8.2 pilnował jej `main`, a teraz funkcja, więc chronione jest każde wywołanie.

## 6. Misja: karta miejska

Program przechowuje jeden rekord karty miejskiej: nazwę, liczbę dostępnych kredytów i liczbę opłaconych przejazdów. Kredyty to umowne punkty, a nie pieniądze. Przy każdej próbie opłacenia przejazdu program decyduje, czy ją przyjąć.

**Dane:** karta `City Pass` z 20 kredytami i 2 przejazdami. Potem trzy próby opłaty, w tej kolejności: 7, 15 i 13 kredytów.

**Reguły:**

- Na początku saldo i liczba przejazdów są nieujemne. Cena przejazdu to liczba całkowita.
- Opłata jest **przyjmowana** tylko wtedy, gdy cena jest większa od zera i saldo wystarcza na całą cenę, także dokładnie. Przyjęta opłata zmniejsza saldo dokładnie o cenę i zwiększa liczbę przejazdów o 1.
- W każdej innej sytuacji opłata jest **odrzucana**. Cena 0 i cena ujemna to niepoprawne żądania. Odrzucona opłata nie zmienia żadnego pola: program nie pobiera części opłaty, a saldo nigdy nie jest ujemne.
- Nazwa karty nigdy się nie zmienia.

**Wymagania:**

- Program definiuje własny typ z trzema polami: nazwą (`std::string`), saldem kredytów (`int`) i liczbą przejazdów (`int`). Nazwy typu i pól wybierasz samodzielnie.
- W `main` jest **jeden** obiekt tego typu. Program nie tworzy nowych kart dla kolejnych prób.
- Program ma jedną własną funkcję, która próbuje opłacić jeden przejazd: dostaje istniejący rekord i cenę (`int`) i zwraca `bool`, `true` przy przyjętej opłacie, a `false` przy odrzuconej. Niczego nie wypisuje ani nie odczytuje z wejścia. Nazwy funkcji i parametrów wybierasz samodzielnie.
- `main` wywołuje tę funkcję **trzy razy dla tego samego obiektu**: dla 7, 15 i 13. Po każdym wywołaniu wypisuje wynik próby, wybrany instrukcją `if` na podstawie wyniku funkcji, i bieżący stan karty.
- Program wypisuje dokładnie osiem linijek, jak w przykładzie niżej. Słowa `credits` i `rides` mają zawsze tę samą formę, niezależnie od liczby.
- Program nie odczytuje niczego z wejścia.

W `cpp-workspace` utwórz katalog `city_pass`, skopiuj do niego `CMakeLists.txt` z oryginalnego `lesson_05_first_program`, utwórz pusty `main.cpp` i napisz program samodzielnie.

Dla danych powyżej standardowe wyjście ma być takie:

<!-- output: city_pass -->
```text
Card: City Pass
Before: 20 credits, 2 rides
Fare 7: accepted
After first: 13 credits, 3 rides
Fare 15: refused
After second: 13 credits, 3 rides
Fare 13: accepted
After third: 0 credits, 4 rides
```

Druga próba jest odrzucona, bo po pierwszej zostało tylko 13 kredytów. Trzecia wykorzystuje całe pozostałe saldo.

**To nie jest wydawanie towaru z innymi nazwami:** przyjęta opłata zmienia dwa pola. Musisz samodzielnie zdecydować:

1. jak nazwać typ, jego pola i funkcję;
2. dlaczego obiekt w `main` nie ma `const`, a parametr rekordu ma `&`;
3. jak przekazać cenę;
4. dlaczego funkcja zwraca `bool`, a nie `void`;
5. jakie warunki powodują odmowę i jak je zapisać;
6. dlaczego te warunki trzeba sprawdzić przed jakąkolwiek zmianą;
7. które dwa pola zmienia przyjęta opłata, a którego funkcja nie dotyka;
8. jak sprawić, żeby odmowa zostawiła rekord dokładnie taki, jaki był;
9. jak `main` odbiera wynik każdej próby;
10. dlaczego każda kolejna próba działa na saldzie zostawionym przez poprzednią.

**Zanim napiszesz program**, przygotuj tabelę przypadków: dane z wymagań, cena 1, cena równa saldu, cena o 1 większa od salda, cena 0, cena ujemna, puste saldo, dwie przyjęte opłaty z rzędu, odmowa, a po niej przyjęta opłata. Przy każdej próbie zapisz wynik, saldo i liczbę przejazdów.

**Potem** uruchom program dla danych z wymagań i dla jednego wariantu z dwiema odmowami na początku, na przykład: saldo 10, 0 przejazdów, ceny 0, 11 i 10. Zmieniaj przy tym tylko dane. Wszystkie przypadki z pełnej listy kontrolnej są sprawdzone automatycznie.

### Kryterium sukcesu

- Program buduje się jako C++20 i dla danych z wymagań wypisuje dokładnie osiem linijek pokazanych wyżej.
- Funkcja dostaje rekord przez `&`, a cenę przez wartość, zwraca `bool` i niczego nie wypisuje ani nie odczytuje.
- Wszystkie sprawdzenia stoją przed zmianami. Przy odmowie żadne pole się nie zmienia, a przy przyjętej opłacie zmieniają się dokładnie dwa.
- Wszystkie trzy wywołania dotyczą tego samego obiektu, a `main` wybiera `accepted` albo `refused` na podstawie wyniku funkcji.
- Tabela przypadków powstała przed uruchomieniem programu.
- Umiesz wyjaśnić, dlaczego warunki są sprawdzane przed zmianą pól.

Gdy wynik się zgadza, możesz zapisać projekt w Gicie, jak w lekcji 1.5.

<details>
<summary>Podpowiedź 1</summary>

Czy opłata ma zostać przyjęta w każdej sytuacji? Co powinno stać się z rekordem, gdy nie wystarcza kredytów?

</details>

<details>
<summary>Podpowiedź 2</summary>

Funkcja ma odpowiedzieć `true` albo `false`. Najpierw rozstrzygnij, czy operacja jest dozwolona, a dopiero potem zmień stan karty.

</details>

<details>
<summary>Podpowiedź 3</summary>

Przy zaakceptowanej opłacie zmień saldo i liczbę przejazdów. Przy odmowie zakończ funkcję bez zmiany któregokolwiek pola. Kolejne wywołanie korzysta ze stanu pozostawionego przez poprzednie.

</details>

<details>
<summary>Pełna lista przypadków kontrolnych: otwórz po przygotowaniu własnej tabeli</summary>

Kolumna „Po każdej próbie” podaje wynik, a po nim saldo i liczbę przejazdów.

| | Nazwa | Na początku | Ceny | Po każdej próbie | Co sprawdza |
|---|---|---|---|---|---|
| A | `City Pass` | 20 kredytów, 2 przejazdy | 7, 15, 13 | `accepted` 13/3, `refused` 13/3, `accepted` 0/4 | dane z wymagań: przyjęcie, odmowa, wykorzystanie całego salda |
| B | `Student` | 10 kredytów, 0 przejazdów | 1 | `accepted` 9/1 | najniższa dodatnia cena |
| C | `Weekend` | 10 kredytów, 0 przejazdów | 10 | `accepted` 0/1 | cena równa saldu |
| D | `Night` | 10 kredytów, 0 przejazdów | 11 | `refused` 10/0 | cena o 1 większa od salda |
| E | `Day Card` | 10 kredytów, 2 przejazdy | 0, -3 | `refused` 10/2, `refused` 10/2 | cena 0 i cena ujemna, dwie odmowy z rzędu |
| F | `Empty` | 0 kredytów, 4 przejazdy | 1, 0 | `refused` 0/4, `refused` 0/4 | puste saldo |
| G | `Commuter` | 12 kredytów, 1 przejazd | 4, 5 | `accepted` 8/2, `accepted` 3/3 | dwie przyjęte opłaty z rzędu |
| H | `City Pass` | 10 kredytów, 0 przejazdów | 0, 11, 10 | `refused` 10/0, `refused` 10/0, `accepted` 0/1 | odmowy nie psują późniejszej przyjętej opłaty |

We wszystkich przypadkach nazwa karty po próbach jest taka sama jak na początku. Samo poprawne saldo nie dowodzi, że program działa: przy każdej próbie sprawdź też wynik i liczbę przejazdów.

**Testy automatyczne i Twoje próby.** Wszystkie przypadki są sprawdzone automatycznie przez program kontrolny. Ma on ten sam typ i tę samą funkcję co rozwiązanie referencyjne, ale stan początkowy i ceny odczytuje z wejścia, a po każdej próbie wypisuje wynik i stan. To tylko narzędzie do sprawdzania, a nie część misji: w misji dane są wpisane w kodzie, a próby są dokładnie trzy. Program kontrolny i jego wyniki są w części [Przykładowe rozwiązania](#przykładowe-rozwiązania), bo zawierają rozwiązanie.

</details>

Przykładowe rozwiązanie jest w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 7. Znajdź błąd: zmiana przed odmową

To zadanie wykonaj **po misji**: program poniżej ma pobrać jedną opłatę z karty, tak jak Twój program. Program możesz przepisać albo skopiować do `main.cpp`.

<details>
<summary>Program do sprawdzenia: otwórz po napisaniu własnego programu</summary>

<!-- example: fare_order_bug -->
```cpp
#include <iostream>
#include <string>

struct TravelCard {
    std::string name;
    int credits;
    int rides;
};

bool pay_fare(TravelCard& card, int fare) {
    ++card.rides;

    if (fare <= 0 || fare > card.credits) {
        return false;
    }

    card.credits -= fare;
    return true;
}

int main() {
    TravelCard card{"City Pass", 20, 2};
    const int fare{7};

    std::cout << "Card: " << card.name << "\n";
    std::cout << "Before: " << card.credits << " credits, " << card.rides << " rides\n";

    const bool paid{pay_fare(card, fare)};

    if (paid) {
        std::cout << "Fare " << fare << ": accepted\n";
    } else {
        std::cout << "Fare " << fare << ": refused\n";
    }

    std::cout << "After: " << card.credits << " credits, " << card.rides << " rides\n";
}
```

1. **Przewidź** wynik i stan karty dla danych z programu, czyli ceny 7.
2. Uruchom program. Czy wynik wygląda poprawnie?
3. Zmień `fare` na cenę, którą funkcja powinna odrzucić. Zapisz poprawny wynik dla swojej wartości: wynik próby, saldo i liczbę przejazdów.
4. Dla swojej wartości prześledź linijka po linijce oba pola rekordu w funkcji. Potem uruchom program.
5. Wskaż pole, które zmieniło się za wcześnie.
6. Wyjaśnij, dlaczego zwrócenie `false` nie wystarcza, żeby odmowa była poprawna.
7. Popraw kolejność sprawdzeń i zmian.
8. Uruchom poprawiony program dla swojej wartości. Przewidź, co wypisze dla ceny 7, i wyjaśnij, dlaczego poprawka nie zmienia wyniku przyjętej opłaty.
9. Uzasadnij na tym przykładzie zasadę „wszystko albo nic”.

</details>

Wyniki, przykładowa wartość i poprawiony program są w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 8. Gdy coś pójdzie inaczej

| Co widzisz | Co to znaczy | Co zrobić |
|---|---|---|
| Odrzucona opłata zwiększa liczbę przejazdów | Funkcja zmienia pole przed sprawdzeniem warunków (punkt 7). | Najpierw sprawdź wszystkie warunki, potem zmień oba pola. |
| Saldo jest ujemne | Funkcja nie porównuje ceny z saldem albo robi to po odjęciu ceny. | Porównaj cenę z saldem przed jakąkolwiek zmianą. |
| Cena równa saldu jest odrzucana | Warunek odmowy używa `>=` zamiast `>`. | Saldo równe cenie wystarcza. Odmawiaj tylko wtedy, gdy cena jest większa od salda. |
| Cena 0 albo ujemna jest przyjęta | Funkcja nie sprawdza, czy cena jest większa od zera. | Dodaj ten warunek do klauzuli ochronnej. |
| `accepted` albo `refused` nie zgadza się ze stanem karty | `main` nie korzysta z wyniku funkcji albo ma zamienione gałęzie `if`. | Zapisz wynik wywołania w zmiennej `bool` i wybierz tekst na jego podstawie. |
| Jedna próba zmienia saldo dwa razy | Funkcja jest wywołana dwa razy: raz osobno i raz w warunku `if`. Każde wywołanie to osobna próba opłaty. | Wywołaj funkcję raz, zapisz wynik i sprawdzaj zapisaną wartość. |
| Kolejna próba liczy się od salda początkowego | Wywołanie dotyczy kopii albo funkcja dostaje kartę przez wartość (lekcja 9.1). | Wywołuj funkcję dla tego samego obiektu, przekazanego przez `&`. |
| Ostrzeżenie `non-void function does not return a value in all control paths` | Po przyjętej opłacie funkcja dochodzi do końca bez `return true;`. Takie wywołanie ma niezdefiniowane zachowanie (lekcja 5.4). | Dopisz `return true;` po zmianach pól. |

## 9. Wyjaśnij

Odpowiedz własnymi słowami, najlepiej na piśmie. Dopiero potem porównaj z przykładowymi odpowiedziami.

1. Dlaczego funkcja, która zmienia rekord, może zwracać `bool`? Co jest jej wynikiem, a co skutkiem?
2. Co w tej lekcji oznacza `true`, a co `false`? Czy każda funkcja C++ zwracająca `bool` ma takie znaczenie?
3. Co musi zrobić funkcja, żeby `false` oznaczało odmowę bez żadnej zmiany?
4. Dlaczego w misji cena 0 jest odrzucana? Czym to się różni od zera nowych rezerwacji w lekcji 8.2?
5. Dlaczego saldo trzeba sprawdzić przed jego zmniejszeniem?
6. Co oznacza „wszystko albo nic” dla operacji, która zmienia dwa pola?
7. Funkcja zwiększa licznik przejazdów przed sprawdzeniem opłaty, ale przy odmowie i tak zwraca `false`. Dlaczego to błąd?
8. Dlaczego druga próba w misji widzi saldo po pierwszej, a trzecia może się udać mimo wcześniejszej odmowy?
9. Dlaczego funkcja niczego nie wypisuje, a `main` zapisuje jej wynik w zmiennej?
10. Czym różnią się funkcja, która tylko odczytuje rekord, funkcja, która go zmienia, i funkcja, która zwraca nową wartość? Kiedy w misji nowa wartość byłaby lepsza?

<details>
<summary>Przykładowe odpowiedzi</summary>

1. Bo zmiana obiektu i zwracanie wartości to dwie niezależne cechy funkcji. Skutkiem jest zmieniony rekord, który `main` widzi po wywołaniu. Wynikiem jest `true` albo `false`: informacja, czy operacja została przyjęta.
2. `true`: operacja przyjęta i wykonana zgodnie z umową. `false`: operacja odrzucona, a wszystkie pola rekordu bez zmian. To umowa naszych funkcji, a nie reguła C++. Inne funkcje zwracające `bool` mogą tylko odpowiadać na pytanie, jak `is_even` z lekcji 5.3.
3. Musi sprawdzić wszystkie warunki, zanim zmieni którekolwiek pole, i przy odmowie zakończyć się `return false;`. Wtedy żadna zmiana nie zdąży się wykonać.
4. Bo umowa misji mówi, że przejazd za 0 kredytów to niepoprawne żądanie: przyjęcie go doliczyłoby przejazd bez opłaty. W lekcji 8.2 zero rezerwacji było przyjmowane jako aktualizacja bez zmiany. To inna umowa, też poprawna. W misji `true` zawsze oznacza rzeczywistą zmianę.
5. Bo tylko przed zmianą wiadomo, czy saldo wystarczy na całą cenę. Po odjęciu byłoby za późno: saldo mogłoby już być ujemne, a karta w niepoprawnym stanie.
6. Że przyjęta opłata zmienia oba pola, saldo i liczbę przejazdów, a odrzucona żadnego. Nigdy nie zmienia tylko jednego.
7. Bo odmowa zostawia wtedy rekord częściowo zmieniony: liczba przejazdów rośnie, choć opłaty nie pobrano. `false` poprawnie zgłasza odmowę, ale wywołujący zakłada, że nic się nie zmieniło, a stan karty jest już inny.
8. Bo wszystkie wywołania dostają ten sam obiekt przez `&`. Po pierwszej opłacie saldo wynosi 13, więc 15 to za dużo. Odmowa niczego nie zmieniła, więc trzecia próba widzi nadal 13, a 13 nie jest większe od 13.
9. Funkcja odpowiada za regułę i zmianę, a raport należy do `main`. Dzięki temu tę samą funkcję można wywołać w programie z innym raportem, jak w programie kontrolnym. Zmienna zapamiętuje wynik jedynego wywołania: gdyby `main` wywołał funkcję jeszcze raz, żeby sprawdzić wynik, wykonałby drugą próbę opłaty.
10. Funkcja tylko odczytująca dostaje `const&` i niczego nie zmienia. Funkcja zmieniająca dostaje `&` i zmienia istniejący rekord. Funkcja zwracająca nową wartość dostaje `const&` i zostawia oryginał bez zmian. W misji nowa wartość byłaby lepsza na przykład w podglądzie: gdyby program miał pokazać stan karty po opłacie, zanim ją naprawdę pobierze.

</details>

## Podsumowanie

- Funkcja z parametrem `&` może zmienić rekord tylko po spełnieniu warunków i zwrócić `bool`. Wynik mówi, czy operacja została przyjęta, a skutkiem jest zmieniony rekord.
- W tej lekcji `true` oznacza operację przyjętą i wykonaną, a `false` odmowę, po której wszystkie pola są bez zmian. To umowa naszych funkcji, a nie znaczenie każdego `bool`.
- Wszystko albo nic: klauzula ochronna z `return false;` stoi przed wszystkimi zmianami. Zmiana przed sprawdzeniem może zostawić rekord częściowo zmieniony mimo `false`.
- `main` zapisuje wynik każdego wywołania i na jego podstawie wypisuje raport. Kolejne wywołania na tym samym obiekcie zaczynają od stanu zostawionego przez poprzednie, także po odmowie.

## Co dalej

W tej lekcji funkcja zmieniała jeden rekord. W kolejnej lekcji zmienisz przez referencję wiele rekordów zapisanych w wektorze: [Lekcja 9.3: Modyfikowanie elementów wektora przez referencję](lesson_03_changing_vector_elements.md).

---

## Przykładowe rozwiązania

Zajrzyj tutaj **po własnej próbie**. Twoje nazwy mogą się różnić, jeśli standardowe wyjście jest takie, jak wymagane.

<details>
<summary>Punkt 6: misja, karta miejska</summary>

<!-- example: city_pass -->
```cpp
#include <iostream>
#include <string>

struct TravelCard {
    std::string name;
    int credits;
    int rides;
};

bool pay_fare(TravelCard& card, int fare) {
    if (fare <= 0 || fare > card.credits) {
        return false;
    }

    card.credits -= fare;
    ++card.rides;
    return true;
}

int main() {
    TravelCard card{"City Pass", 20, 2};
    const int first_fare{7};
    const int second_fare{15};
    const int third_fare{13};

    std::cout << "Card: " << card.name << "\n";
    std::cout << "Before: " << card.credits << " credits, " << card.rides << " rides\n";

    const bool first_paid{pay_fare(card, first_fare)};

    if (first_paid) {
        std::cout << "Fare " << first_fare << ": accepted\n";
    } else {
        std::cout << "Fare " << first_fare << ": refused\n";
    }

    std::cout << "After first: " << card.credits << " credits, " << card.rides << " rides\n";

    const bool second_paid{pay_fare(card, second_fare)};

    if (second_paid) {
        std::cout << "Fare " << second_fare << ": accepted\n";
    } else {
        std::cout << "Fare " << second_fare << ": refused\n";
    }

    std::cout << "After second: " << card.credits << " credits, " << card.rides << " rides\n";

    const bool third_paid{pay_fare(card, third_fare)};

    if (third_paid) {
        std::cout << "Fare " << third_fare << ": accepted\n";
    } else {
        std::cout << "Fare " << third_fare << ": refused\n";
    }

    std::cout << "After third: " << card.credits << " credits, " << card.rides << " rides\n";
}
```

1. **Rekord przez `&`,** bo funkcja ma zmienić istniejącą kartę, a nie własną kopię.
2. **`bool`, a nie `void`,** bo opłata może zostać odrzucona, a `main` musi to wiedzieć, żeby wypisać `accepted` albo `refused`.
3. **`false`** oznacza: opłata odrzucona, żadne pole się nie zmieniło.
4. **`true`** oznacza: opłata przyjęta, saldo mniejsze dokładnie o cenę, jeden przejazd więcej.
5. **Cena dodatnia,** bo cena 0 doliczyłaby przejazd bez opłaty, a cena ujemna zwiększyłaby saldo. Obie to niepoprawne żądania.
6. **Saldo przed pobraniem,** bo tylko wtedy wiadomo, czy wystarczy na całą cenę. Po odjęciu saldo mogłoby już być ujemne.
7. **Kolejność:** najpierw klauzula ochronna, potem obie zmiany, na końcu `return true;`. Kolejność dwóch zmian po sprawdzeniu nie ma znaczenia.
8. **Przy odmowie oba pola bez zmian,** bo `return false;` kończy funkcję, zanim wykona się którakolwiek zmiana.
9. **Liczby przejazdów nie można zwiększyć przed sprawdzeniem,** bo odmowa zostawiłaby rekord częściowo zmieniony, jak w diagnostyce z punktu 7.
10. **Druga próba widzi saldo po pierwszej,** bo obie dotyczą tego samego obiektu `card`. 15 jest większe od 13, więc odmowa.
11. **Trzecia próba może się udać,** bo odmowa niczego nie zmieniła: saldo nadal wynosi 13, a 13 nie jest większe od 13.
12. **Bez nowego obiektu przy każdej próbie,** bo karta to jedna rzecz, której stan zmienia się w czasie. Nowa karta z wartościami początkowymi zgubiłaby wcześniejsze opłaty.
13. **Funkcja niczego nie wypisuje,** bo odpowiada tylko za regułę i zmianę. Raport należy do `main`, więc ta sama funkcja działa w programie z innym raportem, jak w programie kontrolnym niżej.
14. **Kiedy nowa wartość byłaby lepsza:** gdyby program miał pokazać podgląd, czyli stan karty po opłacie, bez pobierania jej z karty, albo porównać stan przed i po. Wtedy pasowałaby funkcja z `const&`, która zwraca nowy rekord, jak w lekcji 8.5, albo kopia zrobiona przed zmianą, jak w lekcji 8.2.

**Inne poprawne rozwiązania:**

- `card.rides += 1;` zamiast `++card.rides;`;
- zmiany obu pól w odwrotnej kolejności, nadal po klauzuli ochronnej;
- dwie osobne klauzule ochronne, jedna dla ceny równej 0 albo mniejszej i jedna dla za małego salda: obie przed zmianami;
- ceny wpisane bezpośrednio w wywołaniach i w tekstach. Wtedy jednak każdą cenę trzeba zmieniać w dwóch miejscach;
- wywołanie w samym warunku, `if (pay_fare(card, first_fare))`: funkcja też wykonuje się raz, ale zmiana karty jest wtedy ukryta w warunku. Zmienna z wynikiem pokazuje ją wyraźniej.

**Program kontrolny** sprawdza wszystkie przypadki z listy kontrolnej. Typ i funkcja są takie same jak wyżej. Różnica jest w `main`: program odczytuje nazwę, stan początkowy i ceny z wejścia, wywołuje funkcję dla każdej ceny na tym samym obiekcie, po każdej próbie wypisuje wynik i stan, a na końcu nazwę. Wejście odczytuje tak samo jak program kontrolny lekcji 9.1: nazwę przez `std::getline`, liczby przez `>>`, a ceny najpierw do wektora `int`, żeby sprawdzić odczyt, zanim cokolwiek się zmieni. Misja nie potrzebuje ani wejścia, ani wektora.

<!-- example: city_pass_check -->
```cpp
#include <iostream>
#include <string>
#include <vector>

struct TravelCard {
    std::string name;
    int credits;
    int rides;
};

bool pay_fare(TravelCard& card, int fare) {
    if (fare <= 0 || fare > card.credits) {
        return false;
    }

    card.credits -= fare;
    ++card.rides;
    return true;
}

int main() {
    std::string name{};
    int credits{0};
    int rides{0};
    int count{0};
    std::vector<int> fares{};

    std::getline(std::cin, name);
    std::cin >> credits;
    std::cin >> rides;
    std::cin >> count;

    for (int number{1}; number <= count; ++number) {
        int fare{0};
        std::cin >> fare;
        fares.push_back(fare);
    }

    if (std::cin.fail()) {
        std::cout << "Input could not be read\n";
    } else {
        TravelCard card{name, credits, rides};

        std::cout << "Before: " << card.credits << " credits, " << card.rides << " rides\n";

        for (const int fare : fares) {
            const bool paid{pay_fare(card, fare)};

            if (paid) {
                std::cout << "Fare " << fare << ": accepted\n";
            } else {
                std::cout << "Fare " << fare << ": refused\n";
            }

            std::cout << "After: " << card.credits << " credits, " << card.rides << " rides\n";
        }

        std::cout << "Card: " << card.name << "\n";
    }
}
```

Każdy przypadek to nazwa karty w pierwszej linijce, potem saldo, liczba przejazdów, liczba prób i ceny, w kolejności z listy kontrolnej, od A do H.

<!-- input: city_pass_check -->
```text
City Pass
20
2
3
7
15
13
```

<!-- output: city_pass_check -->
```text
Before: 20 credits, 2 rides
Fare 7: accepted
After: 13 credits, 3 rides
Fare 15: refused
After: 13 credits, 3 rides
Fare 13: accepted
After: 0 credits, 4 rides
Card: City Pass
```

<!-- input: city_pass_check -->
```text
Student
10
0
1
1
```

<!-- output: city_pass_check -->
```text
Before: 10 credits, 0 rides
Fare 1: accepted
After: 9 credits, 1 rides
Card: Student
```

<!-- input: city_pass_check -->
```text
Weekend
10
0
1
10
```

<!-- output: city_pass_check -->
```text
Before: 10 credits, 0 rides
Fare 10: accepted
After: 0 credits, 1 rides
Card: Weekend
```

<!-- input: city_pass_check -->
```text
Night
10
0
1
11
```

<!-- output: city_pass_check -->
```text
Before: 10 credits, 0 rides
Fare 11: refused
After: 10 credits, 0 rides
Card: Night
```

<!-- input: city_pass_check -->
```text
Day Card
10
2
2
0
-3
```

<!-- output: city_pass_check -->
```text
Before: 10 credits, 2 rides
Fare 0: refused
After: 10 credits, 2 rides
Fare -3: refused
After: 10 credits, 2 rides
Card: Day Card
```

<!-- input: city_pass_check -->
```text
Empty
0
4
2
1
0
```

<!-- output: city_pass_check -->
```text
Before: 0 credits, 4 rides
Fare 1: refused
After: 0 credits, 4 rides
Fare 0: refused
After: 0 credits, 4 rides
Card: Empty
```

<!-- input: city_pass_check -->
```text
Commuter
12
1
2
4
5
```

<!-- output: city_pass_check -->
```text
Before: 12 credits, 1 rides
Fare 4: accepted
After: 8 credits, 2 rides
Fare 5: accepted
After: 3 credits, 3 rides
Card: Commuter
```

<!-- input: city_pass_check -->
```text
City Pass
10
0
3
0
11
10
```

<!-- output: city_pass_check -->
```text
Before: 10 credits, 0 rides
Fare 0: refused
After: 10 credits, 0 rides
Fare 11: refused
After: 10 credits, 0 rides
Fare 10: accepted
After: 0 credits, 1 rides
Card: City Pass
```

</details>

<details>
<summary>Punkt 7: wyniki przed poprawką i poprawiony program</summary>

Przed poprawką, dla ceny 7:

<!-- output: fare_order_bug -->
```text
Card: City Pass
Before: 20 credits, 2 rides
Fare 7: accepted
After: 13 credits, 3 rides
```

- **Dla przyjętej opłaty wynik jest poprawny,** bo obie zmiany i tak się wykonują: liczba przejazdów rośnie o 1, a saldo spada o 7. Różni się tylko ich kolejność, a tej raport nie pokazuje.
- **Dane, które ujawniają błąd:** każda cena, którą funkcja powinna odrzucić. Na przykład 25, więcej niż saldo. Poprawny wynik to `refused` i stan bez zmian: 20 kredytów, 2 przejazdy. Program z błędem wypisuje:

<!-- example: fare_order_revealed -->
```cpp
#include <iostream>
#include <string>

struct TravelCard {
    std::string name;
    int credits;
    int rides;
};

bool pay_fare(TravelCard& card, int fare) {
    ++card.rides;

    if (fare <= 0 || fare > card.credits) {
        return false;
    }

    card.credits -= fare;
    return true;
}

int main() {
    TravelCard card{"City Pass", 20, 2};
    const int fare{25};

    std::cout << "Card: " << card.name << "\n";
    std::cout << "Before: " << card.credits << " credits, " << card.rides << " rides\n";

    const bool paid{pay_fare(card, fare)};

    if (paid) {
        std::cout << "Fare " << fare << ": accepted\n";
    } else {
        std::cout << "Fare " << fare << ": refused\n";
    }

    std::cout << "After: " << card.credits << " credits, " << card.rides << " rides\n";
}
```

<!-- output: fare_order_revealed -->
```text
Card: City Pass
Before: 20 credits, 2 rides
Fare 25: refused
After: 20 credits, 3 rides
```

| Chwila | `card.credits` | `card.rides` |
|---|---:|---:|
| przed wywołaniem | 20 | 2 |
| po `++card.rides;` | 20 | **3** |
| warunek: 25 jest większe od 20, `return false;` | 20 | 3 |
| po powrocie do `main` | 20 | 3 |

- **Pole zmienione za wcześnie:** liczba przejazdów. Funkcja zwiększa ją, zanim wie, czy opłata jest dozwolona.
- **Dlaczego `false` nie wystarcza:** wynik poprawnie zgłasza odmowę, ale rekord jest już częściowo zmieniony. Wywołujący zakłada, że po `false` nic się nie zmieniło, a karta ma przejazd, za który nikt nie zapłacił. Tak samo działa każda inna odmowa, na przykład cena 0 albo ujemna.
- **Poprawka:** przenieś `++card.rides;` za klauzulę ochronną, obok `card.credits -= fare;`. Wtedy wszystkie sprawdzenia stoją przed wszystkimi zmianami.

<!-- example: fare_order_fixed -->
```cpp
#include <iostream>
#include <string>

struct TravelCard {
    std::string name;
    int credits;
    int rides;
};

bool pay_fare(TravelCard& card, int fare) {
    if (fare <= 0 || fare > card.credits) {
        return false;
    }

    card.credits -= fare;
    ++card.rides;
    return true;
}

int main() {
    TravelCard card{"City Pass", 20, 2};
    const int fare{25};

    std::cout << "Card: " << card.name << "\n";
    std::cout << "Before: " << card.credits << " credits, " << card.rides << " rides\n";

    const bool paid{pay_fare(card, fare)};

    if (paid) {
        std::cout << "Fare " << fare << ": accepted\n";
    } else {
        std::cout << "Fare " << fare << ": refused\n";
    }

    std::cout << "After: " << card.credits << " credits, " << card.rides << " rides\n";
}
```

<!-- output: fare_order_fixed -->
```text
Card: City Pass
Before: 20 credits, 2 rides
Fare 25: refused
After: 20 credits, 2 rides
```

Dla ceny 7 poprawiony program wypisuje to samo co przed poprawką: `Fare 7: accepted` i `After: 13 credits, 3 rides`. Przy przyjętej opłacie obie wersje wykonują te same dwie zmiany, więc taki przypadek nie odróżnia ich od siebie. Dlatego do sprawdzenia kolejności potrzebna jest odmowa.

**Wszystko albo nic:** przyjęta opłata zmienia oba pola, odrzucona żadnego. Wersja z błędem przy odmowie zmieniała jedno pole z dwóch, a to stan, którego umowa nie dopuszcza.

</details>

**Poprzednia lekcja:** [Lekcja 9.1: Funkcja zmienia istniejący rekord](lesson_01_a_function_changes_a_record.md) · **Następna lekcja:** [Lekcja 9.3: Modyfikowanie elementów wektora przez referencję](lesson_03_changing_vector_elements.md) · [Opis kursu](../../README.md)

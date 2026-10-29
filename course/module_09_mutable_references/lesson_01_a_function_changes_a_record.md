# Lekcja 9.1: Funkcja zmienia istniejący rekord

**Polski** · [English](lesson_01_a_function_changes_a_record.en.md) · [Opis kursu](../../README.md)

> **Moduł 9, lekcja 1** · około 65–80 minut
> **Potrzebujesz:** katalogu `cpp-workspace` i oryginalnego projektu `lesson_05_first_program`, jak dotąd. Debugger nie jest w tej lekcji potrzebny.
> **Wersja pilotażowa.** Programy z tej lekcji sprawdzamy automatycznie na Windowsie, Ubuntu i macOS. Żaden z nich nie pyta o dane: wszystkie wartości są zapisane w kodzie. Dane z wejścia odczytuje tylko program kontrolny w części z rozwiązaniami.

## Zanim zaczniesz

Ta lekcja zakłada, że:

- wiesz, że parametr przekazany przez wartość to własna wartość funkcji, a jego zmiana nie zmienia zmiennej z miejsca wywołania (lekcja 5.2);
- wiesz, że funkcja `void` nie przekazuje wyniku, ale może mieć skutek, na przykład wypisać tekst (lekcja 5.1);
- znasz parametr `const&`, przez który funkcja odczytuje istniejący obiekt bez kopiowania go (lekcje 6.4 i 8.3);
- zmieniasz pola obiektu bez `const` i tworzysz kopię rekordu zapisem `Product copy{original};` (lekcja 8.2).

## Sytuacja

Magazyn przechowuje produkt `Tea` ze stanem 3 sztuk. Przychodzi dostawa 4 sztuk. Stan **tego samego produktu** ma wzrosnąć do 7. Nie chodzi o nowy produkt ani o osobny rekord z „drugą wersją” herbaty, tylko o zmianę pola `stock` w rekordzie, który już istnieje.

Co już umiesz?

- W lekcji 8.2 pola zmieniały się bezpośrednio w `main`: `tea.stock += 4;`. To działa, ale reguła dostawy stoi wtedy w każdym miejscu, które ją wykonuje.
- W lekcjach 8.3 i 8.4 funkcje dostawały rekord przez `const&`. Mogły go czytać, ale nie zmieniać.
- W lekcji 8.5 funkcja tworzyła nowy rekord z wynikiem i go zwracała. To dobry projekt, gdy potrzebny jest osobny wynik. Tutaj jednak wynikiem ma być **zmieniony stan istniejącego produktu**.

Potrzebna jest funkcja, której wywołujący **pozwala zmienić istniejący obiekt**. W tej lekcji poznasz parametr, który zapisuje taką umowę w nagłówku funkcji.

Po tej lekcji będziesz:

- odróżniać parametr przez wartość, przez `const&` i przez `&`;
- pisać funkcję `void` z parametrem `Product&`, która zmienia pole przekazanego rekordu;
- wyjaśniać, który obiekt zmienia funkcja i dlaczego zmiana zostaje po powrocie do `main`;
- przewidywać stan rekordu przed wywołaniem i po kolejnych wywołaniach;
- wyjaśniać, dlaczego obiekt `const` nie może trafić do funkcji z parametrem `&`;
- wybierać `const&`, gdy funkcja tylko czyta, a `&`, gdy jej zadaniem jest zmiana;
- dobierać dane, które ujawniają, że funkcja zmienia kopię zamiast oryginału.

## 1. Przygotuj projekt

W `cpp-workspace` utwórz katalog `lesson_9_1` i skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program`. Program z punktu 2 wpisujesz w `main.cpp` tego katalogu. Typ `Product` pochodzi z Modułu 8.

## 2. Parametr `Product&`

<!-- example: delivery -->
```cpp
#include <iostream>
#include <string>

struct Product {
    std::string name;
    int stock;
    int minimum;
    int unit_price;
};

void receive_delivery(Product& product, int delivered) {
    product.stock += delivered;
}

int main() {
    Product tea{"Tea", 3, 8, 6};

    std::cout << "Product: " << tea.name << "\n";
    std::cout << "Before: " << tea.stock << "\n";

    receive_delivery(tea, 4);

    std::cout << "After: " << tea.stock << "\n";
}
```

**Przewidź** wszystkie trzy linijki, a potem uruchom program. Szczególnie: ile wynosi `tea.stock` po wywołaniu?

<details>
<summary>Standardowe wyjście</summary>

<!-- output: delivery -->
```text
Product: Tea
Before: 3
After: 7
```

</details>

| Część | Znaczenie |
|---|---|
| `Product` | typ parametru: nasz rekord |
| `&` | parametr odnosi się do istniejącego obiektu z miejsca wywołania, a nie jest jego kopią |
| brak `const` | przez ten parametr funkcja może zmieniać pola tego obiektu |
| `product` | nazwa, przez którą funkcja odczytuje i zmienia pola: `product.stock` |

- **`tea` nie ma `const`,** bo dostawa ma zmienić jego stan.
- **W czasie wywołania `receive_delivery(tea, 4)` nazwa `product` to inna nazwa obiektu `tea`.** Funkcja nie dostaje kopii, tylko dostęp do tego samego rekordu.
- **`product.stock += delivered;` zmienia prawdziwe pole `tea`,** dlatego po powrocie `main` odczytuje już 7.
- **Pozostałe pola się nie zmieniają.** Funkcja zmienia tylko `stock`: `name`, `minimum` i `unit_price` mają te same wartości co przed wywołaniem.
- **Wynik `void`,** bo funkcja nie oddaje osobnej wartości. Jej skutkiem jest zmieniony stan obiektu, który `main` widzi po wywołaniu. W kolejnej lekcji funkcja zmieniająca rekord zwróci też wynik: jedno nie wyklucza drugiego.
- **Liczba sztuk przez wartość:** `int delivered` funkcja tylko odczytuje, więc wystarczy jej własna wartość, jak w lekcji 5.2.

Zapis `Product& product` nie znaczy „usuwamy `const`”. To **umowa**: wywołujący pozwala funkcji zmienić obiekt, który jej przekazuje. Dlatego nagłówek mówi czytelnikowi programu, że `tea` po wywołaniu może wyglądać inaczej.

## 3. Przebieg wywołania

| Krok | Co się dzieje | `tea.stock` |
|---|---|---:|
| 1 | `main` tworzy `tea` | 3 |
| 2 | zaczyna się `receive_delivery(tea, 4)`: `product` odnosi się do `tea`, `delivered` dostaje 4 | 3 |
| 3 | funkcja odczytuje `product.stock`, czyli pole `tea` | 3 |
| 4 | `product.stock += delivered;` zmienia to pole | 7 |
| 5 | funkcja się kończy, a nazwa `product` przestaje istnieć | 7 |
| 6 | `main` odczytuje `tea.stock` | 7 |

Nazwa `product` istnieje tylko w czasie wywołania, ale zmieniała pole obiektu `tea`, który istniał wcześniej i istnieje dalej. Dlatego zmiana zostaje. Parametr przez wartość z lekcji 5.2 działał inaczej: funkcja zmieniała swoją własną wartość, a po powrocie zmienna z `main` miała starą wartość.

## 4. Trzy sposoby przekazania rekordu

| Parametr | Co otrzymuje funkcja? | Czy zmiana pola przez parametr dotyczy oryginału? |
|---|---|---|
| `Product product` | osobny obiekt parametru, przekazany przez wartość | nie |
| `const Product& product` | dostęp do istniejącego obiektu do odczytu | nie można zmieniać przez ten parametr |
| `Product& product` | dostęp do istniejącego obiektu, z możliwością modyfikacji | tak |

- **Przekazanie przez wartość to poprawny C++.** Funkcja może zmieniać swój obiekt parametru, ale ta zmiana nie dotyczy oryginału.
- **`const&` ogranicza tylko ten dostęp.** Funkcja nie zmieni obiektu przez parametr, ale sam oryginał może się zmieniać gdzie indziej, na przykład w `main`, jeśli nie jest `const` (lekcja 8.3).
- **`&` daje uprawnienie, a nie obowiązek.** Funkcja z parametrem `Product&` może zmienić rekord, ale co naprawdę zrobi, decyduje jej kod. Dla 0 dostarczonych sztuk `receive_delivery` nic nie zmienia.

**Kiedy który?** Gdy funkcja tylko czyta rekord, wybieraj `const&`, jak w Module 8: nagłówek obiecuje wtedy, że niczego nie zmieni, a kompilator tego pilnuje. Gdy zadaniem funkcji jest zmiana istniejącego obiektu, wybierz `&`. Gdy potrzebny jest osobny wynik, a oryginał ma zostać bez zmian, funkcja może dostać `const&` i zwrócić nowy rekord, jak w lekcji 8.5. To trzy różne umowy, a nie lepsza i gorsza wersja tego samego.

## 5. Obiekt `const` nie trafi do `Product&`

Ten program różni się od programu z punktu 2 jednym słowem: `tea` ma `const`. **Przewidź**, czy się zbuduje. Możesz to sprawdzić, ale nie musisz.

<!-- broken: delivery_const_tea at=21:5 errors=1 error=^no matching function for call to 'receive_delivery' -->
```cpp
#include <iostream>
#include <string>

struct Product {
    std::string name;
    int stock;
    int minimum;
    int unit_price;
};

void receive_delivery(Product& product, int delivered) {
    product.stock += delivered;
}

int main() {
    const Product tea{"Tea", 3, 8, 6};

    std::cout << "Product: " << tea.name << "\n";
    std::cout << "Before: " << tea.stock << "\n";

    receive_delivery(tea, 4);

    std::cout << "After: " << tea.stock << "\n";
}
```

<details>
<summary>Co zgłasza kompilator i dlaczego</summary>

Program się nie zbuduje. Kompilator zgłasza w linijce 21 `no matching function for call to 'receive_delivery'` i dodaje uwagę, że pierwszy argument, `const Product`, straciłby `const`.

- **Odrzucenie jest prawidłowe.** `const` przy `tea` obiecuje, że ten obiekt się nie zmieni. Funkcja z parametrem `Product&` prosi o prawo do zmiany. Gdyby kompilator ją wywołał, złamałby pierwszą obietnicę.
- **Nie usuwaj `const` tylko po to, żeby uciszyć kompilator.** Jeśli obiekt naprawdę ma pozostać niezmieniony, ta funkcja nie jest dla niego.
- **Jeśli operacja rzeczywiście ma zmienić stan, obiekt powinien być świadomie modyfikowalny,** jak `tea` w punkcie 2. Wtedy usunięcie `const` jest decyzją o tym obiekcie, a nie sposobem na komunikat.

Funkcja z parametrem `const Product&` przyjęłaby `const` obiekt bez problemu: obiecuje tylko odczyt.

</details>

## 6. Misja: dziennik nauki

Program przechowuje jeden rekord z dotychczasowym postępem nauki: temat, łączną liczbę minut i liczbę zapisanych sesji. Po każdej nowej sesji ten sam rekord ma się zaktualizować.

**Dane:** temat `C++`, łącznie 90 minut w 2 sesjach. Potem dwie nowe sesje: 35 minut i 20 minut.

**Reguły:**

- Temat to niepusty tekst ASCII. Łączna liczba minut i liczba sesji to nieujemne liczby całkowite.
- Nowa sesja trwa od 1 do 120 minut. Dane spełniają te założenia, więc program ich nie sprawdza.
- **Zapisanie sesji** dodaje jej czas do łącznej liczby minut i zwiększa liczbę sesji o 1. Temat się nie zmienia.

**Wymagania:**

- Program definiuje własny typ z trzema polami: tematem (`std::string`), łączną liczbą minut (`int`) i liczbą sesji (`int`). Nazwy typu i pól wybierasz samodzielnie.
- W `main` jest **jeden** obiekt tego typu. Program nie tworzy nowych obiektów dla kolejnych stanów.
- Program ma jedną własną funkcję, która zapisuje jedną sesję: dostaje istniejący rekord i długość sesji, zmienia rekord i zwraca `void`. Niczego nie wypisuje ani nie odczytuje z wejścia. Nazwę funkcji i parametrów wybierasz samodzielnie.
- `main` wywołuje tę funkcję **dwa razy dla tego samego obiektu**: najpierw dla 35 minut, potem dla 20.
- Program wypisuje dokładnie cztery linijki, jak w przykładzie niżej: `Topic`, `Before` przed pierwszym wywołaniem, `After first` po pierwszym i `After second` po drugim. Liczby pochodzą z pól rekordu odczytanych w tej chwili. Słowa `minutes` i `sessions` stoją zawsze w tej samej formie, także przy liczbie 1.
- Program nie odczytuje niczego z wejścia.

W `cpp-workspace` utwórz katalog `study_log`, skopiuj do niego `CMakeLists.txt` z oryginalnego `lesson_05_first_program`, utwórz pusty `main.cpp` i napisz program samodzielnie.

Dla danych powyżej standardowe wyjście ma być takie:

<!-- output: study_log -->
```text
Topic: C++
Before: 90 minutes, 2 sessions
After first: 125 minutes, 3 sessions
After second: 145 minutes, 4 sessions
```

Pierwsza sesja daje 90 + 35, czyli 125 minut, i trzecią sesję. Druga dodaje 20 minut do **już zmienionego** stanu: 145 minut i czwarta sesja.

**To nie jest program o produktach z innymi nazwami.** Musisz samodzielnie zdecydować:

1. jak nazwać typ, jego pola i funkcję;
2. dlaczego obiekt w `main` nie ma `const`;
3. jaki parametr dostaje rekord: przez wartość, przez `const&` czy przez `&`, i dlaczego;
4. jak przekazać długość sesji;
5. dlaczego funkcja zwraca `void`;
6. które dwa pola zmienia funkcja, a którego nie dotyka;
7. jak wywołać funkcję drugi raz tak, żeby zmiana objęła także wynik pierwszej sesji;
8. w którym miejscu `main` wypisać każdą linijkę, żeby pokazywała stan z właściwej chwili.

**Zanim napiszesz program**, przygotuj tabelę przypadków: dane z wymagań, początkowe zera i jedna sesja, początkowe zera i dwie sesje, dwie sesje tej samej długości, sesje po 1 i po 120 minut. Przy każdym zapisz wszystkie linijki raportu.

**Potem** uruchom program dla danych z wymagań i dla jednego innego przypadku z tabeli, na przykład początkowych zer. Zmieniaj przy tym tylko wartości w klamrach i długości sesji. Wszystkie przypadki z pełnej listy kontrolnej są sprawdzone automatycznie.

### Kryterium sukcesu

- Program buduje się jako C++20 i dla danych z wymagań wypisuje dokładnie cztery linijki pokazane wyżej.
- Jest jeden typ z trzema polami i jeden modyfikowalny obiekt tego typu.
- Funkcja dostaje rekord przez `&`, a długość sesji przez wartość, zwraca `void`, zmienia dwa pola i nie zmienia tematu. Niczego nie wypisuje ani nie odczytuje.
- Oba wywołania dotyczą tego samego obiektu, a drugie uwzględnia wynik pierwszego.
- Tabela przypadków powstała przed uruchomieniem programu.
- Umiesz wyjaśnić, dlaczego parametr nie ma `const` i dlaczego nie jest przekazany przez wartość.

Gdy wynik się zgadza, możesz zapisać projekt w Gicie, jak w lekcji 1.5.

<details>
<summary>Podpowiedź 1</summary>

Czy nowa sesja ma zmienić istniejący dziennik, czy utworzyć osobny wynik? Który sposób przekazania rekordu odpowiada tej odpowiedzialności?

</details>

<details>
<summary>Podpowiedź 2</summary>

Funkcja ma zmienić dwa pola jednego istniejącego obiektu. Zastanów się, czym różni się parametr `T` od `T&`.

</details>

<details>
<summary>Podpowiedź 3</summary>

Po zapisaniu sesji zwiększ łączną liczbę minut i liczbę sesji. Wywołaj funkcję ponownie na tym samym rekordzie, żeby druga aktualizacja uwzględniała pierwszą.

</details>

<details>
<summary>Pełna lista przypadków kontrolnych: otwórz po przygotowaniu własnej tabeli</summary>

Kolumna „Po sesjach” podaje stan po każdej kolejnej sesji: minuty i liczbę sesji.

| | Temat | Na początku | Sesje | Po sesjach | Co sprawdza |
|---|---|---|---|---|---|
| A | `C++` | 90 min, 2 sesje | 35, 20 | 125/3, 145/4 | dane z wymagań |
| B | `Rust` | 0 min, 0 sesji | 45 | 45/1 | początkowe zera i jedna sesja |
| C | `Python` | 0 min, 0 sesji | 30, 30 | 30/1, 60/2 | początkowe zera i dwie sesje tej samej długości |
| D | `SQL` | 60 min, 1 sesja | 15 | 75/2 | niezerowy stan i jedna sesja |
| E | `Git` | 10 min, 1 sesja | 5, 25 | 15/2, 40/3 | dwie sesje różnej długości |
| F | `Math` | 0 min, 0 sesji | 1, 120 | 1/1, 121/2 | najkrótsza i najdłuższa sesja |
| G | `Modern C++` | 100 min, 4 sesje | 20, 20, 20 | 120/5, 140/6, 160/7 | trzy sesje: każda dodaje się do poprzednich; temat ze spacją |
| H | `Art` | 15 min, 1 sesja | brak | brak zmian | żadnej nowej sesji |

We wszystkich przypadkach temat po sesjach jest taki sam jak na początku.

**Testy automatyczne i Twoje próby.** Wszystkie przypadki są sprawdzone automatycznie przez program kontrolny. Ma on ten sam typ i tę samą funkcję co rozwiązanie referencyjne, ale stan początkowy i długości sesji odczytuje z wejścia, a po każdej sesji wypisuje stan. To tylko narzędzie do sprawdzania, a nie część misji: w misji dane są wpisane w kodzie, a sesje są dokładnie dwie. Program kontrolny i jego wyniki są w części [Przykładowe rozwiązania](#przykładowe-rozwiązania), bo zawierają rozwiązanie.

</details>

Przykładowe rozwiązanie jest w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 7. Znajdź błąd: zmienia się kopia

To zadanie wykonaj **po misji**: program poniżej ma przyjąć dostawę, tak jak program z punktu 2. Program możesz przepisać albo skopiować do `main.cpp`.

<details>
<summary>Program do sprawdzenia: otwórz po napisaniu własnego programu</summary>

<!-- example: delivery_copy_bug -->
```cpp
#include <iostream>
#include <string>

struct Product {
    std::string name;
    int stock;
    int minimum;
    int unit_price;
};

void receive_delivery(Product product, int delivered) {
    product.stock += delivered;
}

int main() {
    Product tea{"Tea", 3, 8, 6};
    const int delivered{0};

    std::cout << "Product: " << tea.name << "\n";
    std::cout << "Before: " << tea.stock << "\n";

    receive_delivery(tea, delivered);

    std::cout << "After: " << tea.stock << "\n";
}
```

1. Wskaż parametr, który jest przekazywany przez wartość.
2. **Przewidź**, czy `product.stock += delivered;` zmienia pole obiektu parametru.
3. **Przewidź**, czy ta zmiana dotyczy `tea.stock` w `main`.
4. Uruchom program dla danych z programu, czyli dostawy 0 sztuk. Czy wynik wygląda poprawnie?
5. Zmień wartość `delivered` tak, żeby błąd stał się widoczny. Najpierw zapisz poprawny wynik dla swojej wartości, a potem uruchom program.
6. Wyjaśnij, dlaczego zmiana obiektu parametru nie wystarcza.
7. Popraw parametr.
8. Uruchom poprawiony program dla swojej wartości. Przewidź, co wypisze dla 0.
9. Czy parametr `const Product& product` też by tu wystarczył? Dlaczego?

</details>

Wyniki, przykładowa wartość i poprawiony program są w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 8. Gdy coś pójdzie inaczej

| Co widzisz | Co to znaczy | Co zrobić |
|---|---|---|
| `After` pokazuje starą wartość, choć funkcja zwiększa pole | Funkcja dostaje rekord przez wartość i zmienia własny obiekt parametru (punkt 7). | Jeśli funkcja ma zmienić oryginał, przekaż go przez `&`. |
| `no matching function for call to ...` z uwagą `would lose const qualifier` | Do funkcji z parametrem `&` trafia obiekt `const` (punkt 5). | Zdecyduj, czy obiekt ma się zmieniać. Jeśli tak, usuń `const` z obiektu. Jeśli nie, nie wywołuj dla niego funkcji zmieniającej. |
| `cannot assign to variable ... with const-qualified type` w funkcji | Parametr ma `const&`, a funkcja próbuje zmienić pole. | Funkcja, która ma zmieniać rekord, potrzebuje parametru `&` bez `const`. |
| Po drugim wywołaniu widać tylko ostatnią sesję | Funkcja przypisuje długość sesji (`=`) zamiast ją dodawać (`+=`). | Dodawaj czas nowej sesji do dotychczasowej sumy. |
| Liczba sesji się nie zmienia | Funkcja aktualizuje tylko minuty. | Zapisanie sesji zmienia dwa pola: minuty i liczbę sesji. |
| Druga linijka `After` pokazuje stan bez pierwszej sesji | Drugie wywołanie dotyczy innego obiektu, na przykład kopii utworzonej wcześniej. | Wywołuj funkcję dwa razy dla tego samego obiektu. |
| `Before` pokazuje już zmienione wartości | `Before` wypisuje się po wywołaniu. | Wypisz stan początkowy przed pierwszym wywołaniem. |

## 9. Wyjaśnij

Odpowiedz własnymi słowami, najlepiej na piśmie. Dopiero potem porównaj z przykładowymi odpowiedziami.

1. Czym różnią się parametry `Product product`, `const Product& product` i `Product& product`?
2. Co oznacza `Product& product` dla wywołującego? Dlaczego to nie jest tylko „parametr bez `const`”?
3. Dlaczego po wywołaniu `receive_delivery(tea, 4)` w `main` widać nową wartość `tea.stock`, choć nazwa `product` już nie istnieje?
4. Czym różni się kopia rekordu z lekcji 8.2 od parametru `Product&`?
5. Dlaczego funkcja `receive_delivery` zwraca `void`? Skąd `main` wie, co się zmieniło?
6. Funkcja zmienia `stock`. Co dzieje się z pozostałymi polami? Dlaczego to ważne w misji?
7. Dlaczego drugie wywołanie w misji uwzględnia pierwszą sesję?
8. Dlaczego obiekt `const` nie może zostać przekazany do funkcji z parametrem `&`? Kiedy usunięcie `const` jest dobrą decyzją, a kiedy nie?
9. Dlaczego dostawa 0 sztuk nie wystarczy, żeby sprawdzić, czy funkcja zmienia oryginał?
10. Kiedy lepiej napisać funkcję, która zwraca nowy rekord, zamiast zmieniać istniejący? Dlaczego nie każda funkcja powinna dostawać `&`?

<details>
<summary>Przykładowe odpowiedzi</summary>

1. Przez wartość funkcja dostaje osobny obiekt parametru, więc jego zmiany nie dotyczą oryginału. Przez `const&` dostaje dostęp do istniejącego obiektu tylko do odczytu. Przez `&` dostaje dostęp do istniejącego obiektu i może zmieniać jego pola.
2. Że wywołujący pozwala funkcji zmienić przekazany obiekt i po wywołaniu musi się liczyć ze zmienionym stanem. To umowa zapisana w nagłówku: funkcja z `const&` obiecuje tylko odczyt, a funkcja z `&` może zmieniać.
3. Bo `product` był tylko inną nazwą obiektu `tea`. Funkcja zmieniała pole `tea`, a nie własną kopię. Gdy nazwa `product` znika, obiekt `tea` istnieje dalej, już ze zmienionym polem.
4. Kopia to nowy, niezależny obiekt z wartościami oryginału: jej zmiany nie dotyczą oryginału. Parametr `Product&` to nie nowy obiekt, tylko inna nazwa istniejącego, więc każda zmiana przez niego dotyczy oryginału.
5. Bo nie oddaje osobnej wartości: jej skutkiem jest zmieniony stan rekordu. `main` widzi ten skutek, odczytując pola obiektu po wywołaniu.
6. Zostają takie, jak były: funkcja zmienia tylko pola, które wymienia jej kod. W misji temat ma zostać ten sam, a zmieniają się tylko minuty i liczba sesji.
7. Bo oba wywołania dostają ten sam obiekt przez `&`. Pierwsze zmienia jego pola, a drugie zaczyna od już zmienionego stanu.
8. Bo `const` obiecuje, że obiekt się nie zmieni, a parametr `&` daje prawo do zmiany. Kompilator nie pozwala złamać tej obietnicy. Usunięcie `const` jest dobre, gdy obiekt rzeczywiście ma się zmieniać. Nie jest dobre, gdy chodzi tylko o uciszenie kompilatora.
9. Bo dodanie 0 niczego nie zmienia: funkcja zmieniająca kopię i funkcja zmieniająca oryginał dają ten sam wynik. Różnicę widać dopiero przy dodatniej dostawie.
10. Gdy potrzebny jest osobny wynik, a oryginał ma zostać bez zmian, na przykład gdy trzeba pokazać stan przed zmianą i po niej albo gdy wynik jest innym rodzajem danych, jak raport z lekcji 8.5. Funkcja, która tylko czyta, powinna dostać `const&`: wtedy nagłówek obiecuje, że niczego nie zmieni, a kompilator tego pilnuje.

</details>

## Podsumowanie

- Parametr `Product& product` daje funkcji dostęp do istniejącego obiektu z możliwością zmiany. W czasie wywołania `product` to inna nazwa przekazanego obiektu.
- Zmiana pola przez taki parametr zmienia oryginał i zostaje po powrocie z funkcji. Pola, których funkcja nie zmienia, zostają bez zmian.
- `&` to umowa: wywołujący pozwala funkcji zmienić obiekt. Obiekt `const` nie może trafić do takiej funkcji.
- Przez wartość funkcja dostaje osobny obiekt, a przez `const&` tylko odczyt. Wybór zależy od zadania funkcji.
- Funkcja `void` może mieć skutek: zmieniony stan rekordu, który wywołujący odczyta po wywołaniu.
- Kolejne wywołania na tym samym obiekcie zaczynają od stanu po poprzednich.

## Co dalej

W tej lekcji funkcja zmieniała rekord zawsze, bez żadnych warunków. W kolejnej lekcji funkcja najpierw sprawdzi, czy zmiana jest dozwolona, w razie odmowy zostawi rekord bez zmian i zwróci informację o powodzeniu. Jest w przygotowaniu.

---

## Przykładowe rozwiązania

Zajrzyj tutaj **po własnej próbie**. Twoje nazwy mogą się różnić, jeśli standardowe wyjście jest takie, jak wymagane.

<details>
<summary>Punkt 6: misja, dziennik nauki</summary>

<!-- example: study_log -->
```cpp
#include <iostream>
#include <string>

struct StudyLog {
    std::string topic;
    int total_minutes;
    int sessions;
};

void record_session(StudyLog& progress, int minutes) {
    progress.total_minutes += minutes;
    ++progress.sessions;
}

int main() {
    StudyLog progress{"C++", 90, 2};

    std::cout << "Topic: " << progress.topic << "\n";
    std::cout << "Before: " << progress.total_minutes << " minutes, " << progress.sessions << " sessions\n";

    record_session(progress, 35);
    std::cout << "After first: " << progress.total_minutes << " minutes, " << progress.sessions << " sessions\n";

    record_session(progress, 20);
    std::cout << "After second: " << progress.total_minutes << " minutes, " << progress.sessions << " sessions\n";
}
```

1. **Rekord bez `const`,** bo każda sesja ma zmienić jego stan.
2. **Parametr z `&`,** bo funkcja ma zmienić istniejący dziennik, a nie własną kopię.
3. **Bez `const` w parametrze,** bo `const&` pozwalałby tylko czytać, a funkcja zmienia dwa pola.
4. **`void`,** bo funkcja nie oddaje osobnej wartości. Jej skutkiem jest zmieniony rekord, który `main` odczytuje po wywołaniu.
5. **Długość sesji przez wartość,** bo funkcja tylko ją odczytuje. To zwykła liczba, jak w lekcji 5.2.
6. **Dwa pola,** bo jedna sesja to jednocześnie dodatkowe minuty i jedna sesja więcej. Zmiana tylko jednego z nich dałaby niespójny dziennik.
7. **Temat bez zmian,** bo funkcja go nie dotyka. Zmieniają się tylko pola wymienione w jej kodzie.
8. **Drugie wywołanie widzi pierwsze,** bo oba dotyczą tego samego obiektu `progress`. Druga sesja dodaje 20 minut do 125, a nie do 90.
9. **Parametr przez wartość** zmieniałby obiekt parametru: wszystkie linijki raportu pokazywałyby 90 minut i 2 sesje, jak w diagnostyce z punktu 7.
10. **Bez nowego rekordu,** bo dziennik ma pokazywać bieżący postęp, a poprzednich stanów program nie musi przechowywać. Każda linijka raportu powstaje w chwili, w której stan jest aktualny.
11. **Kiedy nowy rekord byłby lepszy:** gdyby program musiał porównać stan przed sesją i po niej albo zachować oryginał bez zmian. Wtedy funkcja mogłaby dostać `const&` i zwrócić nowy rekord, jak w lekcji 8.5, albo `main` mógłby zrobić kopię przed zmianą, jak w lekcji 8.2.

**Inne poprawne rozwiązania:** zamiast `++progress.sessions;` można napisać `progress.sessions += 1;`. Pola mogą mieć inne nazwy i inną kolejność, jeśli wartości w `{}` stoją w tej samej kolejności co pola. Długości sesji mogą stać w zmiennych `const int` w `main`.

**Program kontrolny** sprawdza wszystkie przypadki z listy kontrolnej. Typ i funkcja są takie same jak wyżej. Różnica jest w `main`: program odczytuje temat, stan początkowy i długości sesji z wejścia, wywołuje funkcję dla każdej sesji na tym samym obiekcie i po każdej wypisuje stan, a na końcu temat. Temat odczytuje `std::getline`, bo może zawierać spację, a liczby `>>`, dopiero po nim, jak w programie kontrolnym lekcji 8.2. Długości sesji trafiają najpierw do wektora `int` przez `push_back` (lekcja 6.2), żeby program mógł sprawdzić odczyt, zanim cokolwiek zmieni. Misja nie potrzebuje ani wejścia, ani wektora.

<!-- example: study_log_check -->
```cpp
#include <iostream>
#include <string>
#include <vector>

struct StudyLog {
    std::string topic;
    int total_minutes;
    int sessions;
};

void record_session(StudyLog& progress, int minutes) {
    progress.total_minutes += minutes;
    ++progress.sessions;
}

int main() {
    std::string topic{};
    int total_minutes{0};
    int sessions{0};
    int count{0};
    std::vector<int> lengths{};

    std::getline(std::cin, topic);
    std::cin >> total_minutes;
    std::cin >> sessions;
    std::cin >> count;

    for (int number{1}; number <= count; ++number) {
        int minutes{0};
        std::cin >> minutes;
        lengths.push_back(minutes);
    }

    if (std::cin.fail()) {
        std::cout << "Input could not be read\n";
    } else {
        StudyLog progress{topic, total_minutes, sessions};

        std::cout << "Before: " << progress.total_minutes << " minutes, " << progress.sessions << " sessions\n";

        int number{0};

        for (const int minutes : lengths) {
            record_session(progress, minutes);
            ++number;
            std::cout << "After session " << number << ": " << progress.total_minutes << " minutes, " << progress.sessions << " sessions\n";
        }

        std::cout << "Topic: " << progress.topic << "\n";
    }
}
```

Każdy przypadek to temat w pierwszej linijce, potem łączna liczba minut, liczba sesji, liczba nowych sesji i ich długości, w kolejności z listy kontrolnej, od A do H.

<!-- input: study_log_check -->
```text
C++
90
2
2
35
20
```

<!-- output: study_log_check -->
```text
Before: 90 minutes, 2 sessions
After session 1: 125 minutes, 3 sessions
After session 2: 145 minutes, 4 sessions
Topic: C++
```

<!-- input: study_log_check -->
```text
Rust
0
0
1
45
```

<!-- output: study_log_check -->
```text
Before: 0 minutes, 0 sessions
After session 1: 45 minutes, 1 sessions
Topic: Rust
```

<!-- input: study_log_check -->
```text
Python
0
0
2
30
30
```

<!-- output: study_log_check -->
```text
Before: 0 minutes, 0 sessions
After session 1: 30 minutes, 1 sessions
After session 2: 60 minutes, 2 sessions
Topic: Python
```

<!-- input: study_log_check -->
```text
SQL
60
1
1
15
```

<!-- output: study_log_check -->
```text
Before: 60 minutes, 1 sessions
After session 1: 75 minutes, 2 sessions
Topic: SQL
```

<!-- input: study_log_check -->
```text
Git
10
1
2
5
25
```

<!-- output: study_log_check -->
```text
Before: 10 minutes, 1 sessions
After session 1: 15 minutes, 2 sessions
After session 2: 40 minutes, 3 sessions
Topic: Git
```

<!-- input: study_log_check -->
```text
Math
0
0
2
1
120
```

<!-- output: study_log_check -->
```text
Before: 0 minutes, 0 sessions
After session 1: 1 minutes, 1 sessions
After session 2: 121 minutes, 2 sessions
Topic: Math
```

<!-- input: study_log_check -->
```text
Modern C++
100
4
3
20
20
20
```

<!-- output: study_log_check -->
```text
Before: 100 minutes, 4 sessions
After session 1: 120 minutes, 5 sessions
After session 2: 140 minutes, 6 sessions
After session 3: 160 minutes, 7 sessions
Topic: Modern C++
```

<!-- input: study_log_check -->
```text
Art
15
1
0
```

<!-- output: study_log_check -->
```text
Before: 15 minutes, 1 sessions
Topic: Art
```

</details>

<details>
<summary>Punkt 7: wyniki przed poprawką i poprawiony program</summary>

Przed poprawką, dla dostawy 0 sztuk:

<!-- output: delivery_copy_bug -->
```text
Product: Tea
Before: 3
After: 3
```

- **Parametr przez wartość:** `Product product`. Przy wywołaniu powstaje osobny obiekt parametru z wartościami pól `tea`.
- **Dla 0 wynik wygląda poprawnie,** bo dostawa 0 sztuk niczego nie zmienia: poprawna funkcja też zostawiłaby 3.
- **Dane, które ujawniają błąd:** każda dodatnia dostawa. Na przykład 4: wewnątrz funkcji `product.stock` wynosi na końcu 7, ale `tea.stock` po powrocie nadal wynosi 3. Poprawny wynik to `After: 7`. Program z błędem wypisuje:

<!-- example: delivery_copy_revealed -->
```cpp
#include <iostream>
#include <string>

struct Product {
    std::string name;
    int stock;
    int minimum;
    int unit_price;
};

void receive_delivery(Product product, int delivered) {
    product.stock += delivered;
}

int main() {
    Product tea{"Tea", 3, 8, 6};
    const int delivered{4};

    std::cout << "Product: " << tea.name << "\n";
    std::cout << "Before: " << tea.stock << "\n";

    receive_delivery(tea, delivered);

    std::cout << "After: " << tea.stock << "\n";
}
```

<!-- output: delivery_copy_revealed -->
```text
Product: Tea
Before: 3
After: 3
```

| Chwila | `product.stock` w funkcji | `tea.stock` w `main` |
|---|---:|---:|
| przed wywołaniem | nie istnieje | 3 |
| na początku funkcji | 3 | 3 |
| po `+=` | 7 | 3 |
| po powrocie | nie istnieje | 3 |

- **Przyczyna:** funkcja zmienia własny obiekt parametru, a nie `tea`. Przekazanie przez wartość jest poprawnym C++, ale nie pasuje do zadania funkcji: dostawa ma zmienić istniejący produkt. Kompilator nie zgłasza błędu, bo zmiana obiektu parametru jest dozwolona.
- **Poprawka:** parametr `Product& product`. Funkcja dostaje wtedy dostęp do `tea`, a nie kopię.

<!-- example: delivery_copy_fixed -->
```cpp
#include <iostream>
#include <string>

struct Product {
    std::string name;
    int stock;
    int minimum;
    int unit_price;
};

void receive_delivery(Product& product, int delivered) {
    product.stock += delivered;
}

int main() {
    Product tea{"Tea", 3, 8, 6};
    const int delivered{4};

    std::cout << "Product: " << tea.name << "\n";
    std::cout << "Before: " << tea.stock << "\n";

    receive_delivery(tea, delivered);

    std::cout << "After: " << tea.stock << "\n";
}
```

<!-- output: delivery_copy_fixed -->
```text
Product: Tea
Before: 3
After: 7
```

Dla 0 poprawiony program wypisuje to samo co przed poprawką: `After: 3`. Dlatego dostawa 0 sztuk nie wystarczy, żeby sprawdzić, który obiekt zmienia funkcja.

**Parametr `const Product& product` by tu nie wystarczył.** Funkcja dostałaby dostęp do `tea`, ale tylko do odczytu, więc linijka `product.stock += delivered;` by się nie zbudowała: kompilator zgłosiłby `cannot assign to variable 'product' with const-qualified type 'const Product &'`, jak w lekcji 8.3. `const&` pasuje do funkcji, które tylko czytają. Funkcja przyjmująca dostawę ma zmieniać, więc potrzebuje `&`.

</details>

**Poprzednia lekcja:** [Lekcja 8.6: Wyniki biegu (sprawdzian Modułu 8)](../module_08_structs/lesson_06_race_results.md) · **Następna lekcja:** w przygotowaniu · [Opis kursu](../../README.md)

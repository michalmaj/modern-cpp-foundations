# Lekcja 9.4: Znajdź rekord i zmień właściwy obiekt

**Polski** · [English](lesson_04_find_a_record_and_change_it.en.md) · [Opis kursu](../../README.md)

> **Moduł 9, lekcja 4** · około 80–95 minut
> **Potrzebujesz:** katalogu `cpp-workspace` i oryginalnego projektu `lesson_05_first_program`, jak dotąd. Debugger nie jest w tej lekcji potrzebny.
> **Wersja pilotażowa.** Programy z tej lekcji sprawdzamy automatycznie na Windowsie, Ubuntu i macOS. Żaden z nich nie pyta o dane: wszystkie wartości są zapisane w kodzie. Dane z wejścia odczytuje tylko program kontrolny w części z rozwiązaniami.

## Zanim zaczniesz

Ta lekcja zakłada, że:

- wiesz, że wykonany `return` kończy całe wywołanie funkcji, także wtedy, gdy stoi w pętli (lekcje 5.4 i 5.7);
- przekazujesz tekst do funkcji przez `const std::string&` (lekcja 7.3) i porównujesz teksty przez `==` (lekcja 3.4);
- znasz funkcję `issue_units` z lekcji 9.2: wydaje towar tylko po spełnieniu warunków i zwraca `bool`;
- zmieniasz elementy wektora w funkcji z parametrem `std::vector<Product>&` i pętlą `for (Product& product : products)` (lekcja 9.3).

## Sytuacja

W lekcji 9.3 funkcja `issue_from_each` próbowała wydać towar z **każdego** produktu. Teraz magazyn dostaje inne żądanie: **wydaj 4 sztuki produktu o nazwie `Pens`**. Z pozostałych produktów niczego nie wolno wydawać.

Funkcja musi dostać istniejący wektor i nazwę produktu, znaleźć właściwy rekord, wywołać dla niego `issue_units` i zwrócić wynik. Jeśli produktu o takiej nazwie nie ma, nic się nie zmienia.

Po tej lekcji będziesz:

- szukać rekordu w wektorze po wartości jednego pola tekstowego;
- kończyć funkcję instrukcją `return` w pętli po znalezieniu rekordu, a `return false;` stawiać za pętlą;
- zmieniać tylko znaleziony rekord, korzystając z funkcji dla jednego rekordu;
- odróżniać znalezienie rekordu od powodzenia operacji;
- dobierać dane, które ujawniają zbyt wczesny `return`.

## 1. Przygotuj projekt

W `cpp-workspace` utwórz katalog `lesson_9_4` i skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program`. Program z punktu 2 wpisujesz w `main.cpp` tego katalogu.

## 2. Wyszukiwanie produktu po nazwie

<!-- example: issue_by_name -->
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

bool issue_units(Product& product, int amount) {
    if (amount <= 0 || amount > product.stock) {
        return false;
    }

    product.stock -= amount;
    return true;
}

bool issue_named(std::vector<Product>& products, const std::string& name, int amount) {
    for (Product& product : products) {
        if (product.name == name) {
            return issue_units(product, amount);
        }
    }

    return false;
}

int main() {
    std::vector<Product> products{
        {"Tea", 3, 8, 6},
        {"Rice", 8, 8, 4},
        {"Pens", 10, 7, 2}
    };

    std::cout << "Products: " << products.size() << "\n";

    const bool pens_issued{issue_named(products, "Pens", 4)};

    if (pens_issued) {
        std::cout << "Issue Pens: accepted\n";
    } else {
        std::cout << "Issue Pens: refused\n";
    }

    const bool tea_issued{issue_named(products, "Tea", 4)};

    if (tea_issued) {
        std::cout << "Issue Tea: accepted\n";
    } else {
        std::cout << "Issue Tea: refused\n";
    }

    const bool water_issued{issue_named(products, "Water", 1)};

    if (water_issued) {
        std::cout << "Issue Water: accepted\n";
    } else {
        std::cout << "Issue Water: refused\n";
    }

    for (const Product& product : products) {
        std::cout << product.name << ": " << product.stock << "\n";
    }
}
```

**Przewidź** wszystkie siedem linijek, a potem uruchom program.

<details>
<summary>Standardowe wyjście</summary>

<!-- output: issue_by_name -->
```text
Products: 3
Issue Pens: accepted
Issue Tea: refused
Issue Water: refused
Tea: 3
Rice: 8
Pens: 6
```

</details>

- **`std::vector<Product>& products`** to istniejący wektor z `main`, który funkcja może zmienić. **`const std::string& name`** to szukana nazwa, udostępniona do odczytu bez kopiowania, jak w lekcji 7.3. W wywołaniu stoi literał, na przykład `"Pens"`: na czas wywołania powstaje z niego `std::string` (lekcja 7.1), do którego odnosi się `name`. **`int amount`** to zwykła liczba.
- **`product`** odnosi się kolejno do prawdziwych elementów wektora, jak w lekcji 9.3.
- **`product.name == name`** sprawdza, czy bieżący rekord ma szukaną nazwę. Jeśli nie, pętla przechodzi do następnego elementu.
- **Przy dopasowaniu** `issue_units` próbuje wykonać operację na tym jednym rekordzie, a `return issue_units(product, amount);` zwraca jej wynik i **kończy całą funkcję** `issue_named`. Dalszych elementów funkcja już nie przegląda.
- **`return false;` za pętlą** wykonuje się tylko wtedy, gdy pętla przejrzała wszystkie rekordy i żaden nie pasował.

Co się stało z każdym produktem?

- **`Pens`** jest trzecim elementem: funkcja przechodzi obok `Tea` i `Rice`, znajduje `Pens` i wydaje 4 sztuki.
- **`Tea`** zostaje znaleziony od razu, ale `issue_units` odmawia, bo są tylko 3 sztuki. Stan się nie zmienia.
- **`Water`** nie występuje w wektorze: pętla przegląda wszystkie trzy rekordy, a funkcja zwraca `false`.
- **`Rice`** nie bierze udziału w żadnej operacji. Wektor nadal ma trzy produkty w tej samej kolejności.

Dwie odmowy mają różne przyczyny, a wynik jest ten sam: `false`.

## 3. `return` w pętli i za pętlą

| Sytuacja | Co się dzieje |
|---|---|
| bieżący rekord nie pasuje | pętla przechodzi do następnego rekordu |
| bieżący rekord pasuje, operacja przyjęta | funkcja kończy się z `true` |
| bieżący rekord pasuje, operacja odrzucona | funkcja kończy się z `false` |
| żaden rekord nie pasuje | pętla się kończy, a potem funkcja zwraca `false` |

`return` nie kończy jednego przebiegu pętli, tylko **całe wywołanie funkcji**, jak w zgłoszeniu C z lekcji 5.7. Tutaj to zamierzone: po znalezieniu rekordu zadanie jest wykonane. Dlatego ważne jest, **gdzie** stoi `return false;`. Porównaj:

<!-- fragment -->
```cpp
for (Product& product : products) {
    if (product.name == name) {
        return issue_units(product, amount);
    }
}

return false;
```

<!-- fragment -->
```cpp
for (Product& product : products) {
    if (product.name == name) {
        return issue_units(product, amount);
    }

    return false;
}
```

W pierwszej wersji `false` oznacza: przejrzano wszystkie rekordy i żaden nie pasował. W drugiej `return false;` stoi w ciele pętli, więc funkcja kończy się już po pierwszym rekordzie, który nie pasuje, i nie sprawdza dalszych.

## 4. Znaleziono czy się udało?

Funkcja `issue_named` ma taką umowę:

- **`true`:** znaleziono rekord i wykonano żądaną operację;
- **`false`:** operacja się nie odbyła, a **cała kolekcja jest bez zmian**.

`false` ma dwie możliwe przyczyny: nie ma rekordu o takiej nazwie albo rekord jest, ale funkcja dla jednego rekordu odmówiła. Wynik `bool` mówi tylko, **czy operacja się odbyła**. Sam `false` nie dowodzi, że rekordu nie ma, a `bool` nie odpowiada na pytanie, czy nazwa istnieje.

Gdyby program musiał podać przyczynę odmowy, potrzebny byłby wynik, który przekazuje więcej informacji. W tej lekcji nie jest to potrzebne: wywołujący chce wiedzieć tylko, czy operacja się odbyła.

**Unikalne nazwy.** Funkcja kończy się na **pierwszym** pasującym rekordzie. W naszych danych każda nazwa występuje najwyżej raz, więc pasujący rekord może być tylko jeden. To założenie danych: programy z tej lekcji nie sprawdzają, czy nazwy się powtarzają.

## 5. Pusty wektor i odmowa po znalezieniu

**Przewidź na papierze** dla funkcji `issue_named` z punktu 2:

1. Co się stanie dla `std::vector<Product> no_products{};` i wywołania `issue_named(no_products, "Tea", 1)`?
2. Nazwa pasuje do rekordu, ale `issue_units` odmawia, jak dla `Tea` w punkcie 2. Co zwraca `issue_named`? Czy szuka dalej?

<details>
<summary>Odpowiedzi</summary>

1. **Zero przebiegów.** Pętla nie odczytuje żadnego elementu, a funkcja dochodzi do `return false;` za pętlą. Nic się nie zmienia. To poprawny wynik: nie potrzeba osobnego warunku, a odczyt `no_products[0]` byłby błędem, bo takiego elementu nie ma.
2. **Zwraca `false` i nie szuka dalej.** Wyszukiwanie znajduje właściwy rekord, `issue_units` zwraca `false`, a `return issue_units(product, amount);` przekazuje ten wynik dalej. Żaden rekord się nie zmienia. Szukanie innego rekordu nie miałoby sensu, bo nazwy są unikalne.

</details>

## 6. Misja: wydanie sprzętu po kodzie

Szkolna wypożyczalnia przechowuje egzemplarze sprzętu w jednym wektorze. Każdy egzemplarz ma unikalny kod, informację, czy jest dostępny, i liczbę wcześniejszych wypożyczeń. Program dostaje żądania wydania konkretnych egzemplarzy, wskazanych kodem. Najważniejsze jest, żeby zmienił się **dokładnie właściwy rekord**.

**Dane:**

| Kod | Dostępny? | Wcześniejsze wypożyczenia |
|---|---|---:|
| CAM-01 | yes | 2 |
| MIC-02 | no | 4 |
| TAB-03 | yes | 0 |
| LAP-04 | yes | 1 |

Żądania, w tej kolejności: `TAB-03`, `MIC-02`, `BAD-99`, ponownie `TAB-03` i `CAM-01`.

**Reguły:**

- Kody są niepuste, unikalne i składają się z prostego tekstu ASCII. Liczby wypożyczeń są nieujemne. Dane spełniają te założenia, więc program ich nie sprawdza.
- **Wydanie egzemplarza:** jeśli egzemplarz jest dostępny, staje się niedostępny, a jego liczba wypożyczeń rośnie o 1. Jeśli jest niedostępny, żadne pole się nie zmienia.
- **Żądanie wydania po kodzie:** jeśli w wektorze jest egzemplarz o tym kodzie, program próbuje go wydać. Jeśli takiego kodu nie ma, nic się nie zmienia. Inne egzemplarze nigdy się nie zmieniają.
- Kod egzemplarza nigdy się nie zmienia, a wektor ma zawsze te same elementy w tej samej kolejności.

**Wymagania:**

- Program definiuje własny typ z trzema polami: kodem (`std::string`), dostępnością (`bool`) i liczbą wypożyczeń (`int`). Nazwy typu i pól wybierasz samodzielnie.
- W `main` jest jeden wektor tych rekordów, zainicjalizowany w kodzie w kolejności z tabeli. Bez osobnych zmiennych na każdy egzemplarz i bez `push_back`.
- **Funkcja dla jednego egzemplarza** dostaje istniejący rekord, wydaje go według reguł i zwraca `bool`: `true`, gdy go wydała, `false`, gdy egzemplarz był niedostępny.
- **Funkcja dla kolekcji** dostaje istniejący wektor i szukany kod, znajduje egzemplarz o tym kodzie, wywołuje dla niego funkcję dla jednego egzemplarza i zwraca jej wynik. Gdy kodu nie ma, zwraca `false`. Nie powtarza reguły wydania.
- Żadna z tych funkcji niczego nie wypisuje ani nie odczytuje z wejścia. Ich nazwy i parametry wybierasz samodzielnie.
- `main` wypisuje liczbę egzemplarzy (z `size()`) i stan przed żądaniami, potem wykonuje każde żądanie **dokładnie raz, na tym samym wektorze**, wypisuje jego wynik (`accepted` dla `true`, `refused` dla `false`), a na końcu stan po wszystkich żądaniach, dokładnie jak w przykładzie niżej.
- Program nie odczytuje niczego z wejścia.

W `cpp-workspace` utwórz katalog `school_loans`, skopiuj do niego `CMakeLists.txt` z oryginalnego `lesson_05_first_program`, utwórz pusty `main.cpp` i napisz program samodzielnie.

Dla danych z tabeli standardowe wyjście ma być takie:

<!-- output: school_loans -->
```text
Equipment: 4
Before:
CAM-01: available yes, loans 2
MIC-02: available no, loans 4
TAB-03: available yes, loans 0
LAP-04: available yes, loans 1
Borrow TAB-03: accepted
Borrow MIC-02: refused
Borrow BAD-99: refused
Borrow TAB-03 again: refused
Borrow CAM-01: accepted
After:
CAM-01: available no, loans 3
MIC-02: available no, loans 4
TAB-03: available no, loans 1
LAP-04: available yes, loans 1
```

Zmieniają się tylko `TAB-03` i `CAM-01`. Drugie żądanie `TAB-03` zostaje odrzucone, bo pierwsze wydanie zmieniło jego stan. `LAP-04` zostaje bez zmian, choć jest dostępny: nikt go nie zażądał.

**Wariant z pustym wektorem:** ten sam typ i te same funkcje, pusty wektor i jedno żądanie `CAM-01`. `main` wypisuje wtedy tylko liczbę egzemplarzy i wynik żądania:

<!-- output: school_loans_empty -->
```text
Equipment: 0
Borrow CAM-01: refused
```

**To nie jest wydawanie towaru z innymi nazwami.** Musisz samodzielnie zdecydować:

1. jak nazwać typ, jego pola i obie funkcje;
2. jakie umowy mają obie funkcje: co dostają i co znaczy ich wynik;
3. dlaczego rekord i wektor są przekazywane przez `&`, a kod przez `const std::string&`;
4. które pole jest kluczem wyszukiwania i jak je porównać;
5. kiedy zakończyć funkcję w pętli, a co zwrócić po przejrzeniu wszystkich rekordów;
6. które dwa pola zmienia udane wydanie, a którego pola funkcja nie dotyka;
7. dlaczego drugie żądanie `TAB-03` zostaje odrzucone;
8. jak sprawić, żeby inne rekordy się nie zmieniały;
9. jak wypisać dostępność jako `yes` albo `no`.

**Zanim napiszesz program**, przygotuj tabelę przypadków: dane z wymagań, pusty wektor, jeden dostępny egzemplarz, jeden niedostępny, kod, którego nie ma, kod pierwszego, środkowego i ostatniego egzemplarza, to samo żądanie dwa razy, odmowa, a po niej udane wydanie innego egzemplarza. Przy każdym zapisz wyniki oraz rekordy, które powinny się zmienić, z ich nowym stanem. Pozostałe rekordy mają zostać bez zmian, a raport `After` pokazuje je wszystkie: poprawny wynik `bool` nie dowodzi, że zmienił się właściwy rekord.

**Potem** uruchom program dla danych z wymagań i dla wariantu z pustym wektorem. Wszystkie przypadki z pełnej listy kontrolnej są sprawdzone automatycznie.

### Kryterium sukcesu

- Program buduje się jako C++20 i dla obu uruchomień wypisuje dokładnie linijki pokazane wyżej.
- Funkcja dla jednego egzemplarza sprawdza dostępność przed zmianą i przy odmowie niczego nie zmienia.
- Funkcja dla kolekcji przegląda istniejące rekordy, porównuje kody przez `==`, kończy się po znalezieniu kodu i zwraca `false` dopiero po przejrzeniu wszystkich rekordów. Reguły wydania nie powtarza.
- Obie funkcje zmieniają istniejące dane z `main`, a nie ich kopie. Niczego nie wypisują ani nie odczytują.
- Wszystkie żądania dotyczą tego samego wektora, a zmieniają się tylko wydane egzemplarze.
- Tabela przypadków powstała przed uruchomieniem programu.
- Umiesz wyjaśnić, dlaczego `return false;` stoi za pętlą, a nie w niej.

Gdy wynik się zgadza, możesz zapisać projekt w Gicie, jak w lekcji 1.5.

<details>
<summary>Podpowiedź 1</summary>

Która funkcja powinna znać regułę wypożyczenia jednego egzemplarza, a która odpowiadać za odnalezienie właściwego egzemplarza w wektorze?

</details>

<details>
<summary>Podpowiedź 2</summary>

Przeglądaj istniejące rekordy przez modyfikowalną referencję. Porównaj kod aktualnego elementu z poszukiwanym kodem.

</details>

<details>
<summary>Podpowiedź 3</summary>

Po znalezieniu rekordu zwróć wynik funkcji wykonującej operację. Jeśli kodu nie ma w żadnym rekordzie, zwróć `false` dopiero po zakończeniu całej pętli.

</details>

<details>
<summary>Pełna lista przypadków kontrolnych: otwórz po przygotowaniu własnej tabeli</summary>

Każdy egzemplarz jest zapisany jako kod, dostępność i liczba wypożyczeń.

| | Egzemplarze | Żądania | Wyniki | Zmienione rekordy | Co sprawdza |
|---|---|---|---|---|---|
| A | CAM-01 yes 2, MIC-02 no 4, TAB-03 yes 0, LAP-04 yes 1 | TAB-03, MIC-02, BAD-99, TAB-03, CAM-01 | accepted, refused, refused, refused, accepted | TAB-03 no 1, CAM-01 no 3 | dane z wymagań |
| B | brak | CAM-01 | refused | brak | pusty wektor |
| C | CAM-01 yes 0 | CAM-01 | accepted | CAM-01 no 1 | jeden dostępny egzemplarz |
| D | CAM-01 no 3 | CAM-01 | refused | brak | jeden niedostępny egzemplarz |
| E | CAM-01 yes 2, MIC-02 yes 0, TAB-03 yes 5 | XYZ-00 | refused | brak | kod, którego nie ma, w niepustym wektorze |
| F | jak w E | CAM-01 | accepted | CAM-01 no 3 | dopasowanie na pierwszej pozycji |
| G | jak w E | MIC-02 | accepted | MIC-02 no 1 | dopasowanie w środku |
| H | jak w E | TAB-03 | accepted | TAB-03 no 6 | dopasowanie na ostatniej pozycji |
| I | LAP-04 yes 1, PRO-05 yes 3 | LAP-04, LAP-04 | accepted, refused | LAP-04 no 2 | udane wydanie, potem to samo żądanie |
| J | MIC-02 no 4, TAB-03 yes 0 | MIC-02, TAB-03 | refused, accepted | TAB-03 no 1 | odmowa, potem udane wydanie innego egzemplarza |
| K | CAM-01 yes 0, MIC-02 yes 1, TAB-03 yes 2 | TAB-03, CAM-01, MIC-02 | accepted, accepted, accepted | wszystkie trzy | kilka udanych wydań różnych egzemplarzy |

We wszystkich przypadkach rekordy spoza kolumny „Zmienione rekordy” są po żądaniach takie same jak przed nimi, a kody, liczba egzemplarzy i ich kolejność się nie zmieniają.

**Testy automatyczne i Twoje próby.** Wszystkie przypadki są sprawdzone automatycznie przez program kontrolny. Ma on ten sam typ i te same funkcje co rozwiązanie referencyjne, ale egzemplarze i żądania odczytuje z wejścia. To tylko narzędzie do sprawdzania, a nie część misji: w misji dane są wpisane w kodzie. Program kontrolny i jego wyniki są w części [Przykładowe rozwiązania](#przykładowe-rozwiązania), bo zawierają rozwiązanie.

</details>

Przykładowe rozwiązanie jest w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 7. Znajdź błąd: wyszukiwanie kończy się za wcześnie

To zadanie wykonaj **po misji**: program poniżej ma wydać egzemplarz o podanym kodzie, tak jak Twój program.

<details>
<summary>Program do sprawdzenia: otwórz dopiero po samodzielnym zadaniu</summary>

<!-- example: borrow_early_bug -->
```cpp
#include <iostream>
#include <string>
#include <vector>

struct Equipment {
    std::string code;
    bool available;
    int loans;
};

bool borrow_item(Equipment& item) {
    if (!item.available) {
        return false;
    }

    item.available = false;
    ++item.loans;
    return true;
}

bool borrow_by_code(std::vector<Equipment>& items, const std::string& code) {
    for (Equipment& item : items) {
        if (item.code == code) {
            return borrow_item(item);
        }

        return false;
    }

    return false;
}

void print_items(const std::vector<Equipment>& items) {
    for (const Equipment& item : items) {
        std::cout << item.code << ": available ";

        if (item.available) {
            std::cout << "yes";
        } else {
            std::cout << "no";
        }

        std::cout << ", loans " << item.loans << "\n";
    }
}

int main() {
    std::vector<Equipment> items{
        {"CAM-01", true, 2},
        {"MIC-02", false, 4},
        {"TAB-03", true, 0}
    };
    const std::string code{"CAM-01"};

    std::cout << "Before:\n";
    print_items(items);

    const bool borrowed{borrow_by_code(items, code)};

    if (borrowed) {
        std::cout << "Borrow " << code << ": accepted\n";
    } else {
        std::cout << "Borrow " << code << ": refused\n";
    }

    std::cout << "After:\n";
    print_items(items);
}
```

Raport wypisuje funkcja `print_items`, która tylko odczytuje wektor, żeby program był krótszy. Błąd nie jest w niej.

1. **Przewidź** wynik dla danych z programu: szukany kod należy do pierwszego egzemplarza. Potem uruchom program. Czy wynik wygląda poprawnie?
2. Zmień `code` tak, żeby błąd stał się widoczny. Zapisz poprawny wynik i stan wszystkich rekordów dla swojej wartości.
3. **Przewidź**, ile przebiegów pętli wykona ten program dla Twojej wartości, jaki będzie wynik i stan wszystkich rekordów. Potem uruchom program.
4. Wskaż `return`, który wykonuje się za wcześnie.
5. Wyjaśnij, dlaczego to, że bieżący rekord nie pasuje, nie oznacza, że nie pasuje żaden.
6. Popraw funkcję i uruchom ją ponownie dla swojej wartości.
7. **Przewidź** wynik obu wersji dla pustego wektora. Dlaczego pusty wektor nie ujawnia błędu?

</details>

Wyniki, przykładowa wartość i poprawiony program są w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 8. Gdy coś pójdzie inaczej

| Co widzisz | Co to znaczy | Co zrobić |
|---|---|---|
| Działa tylko kod pierwszego egzemplarza, a dalsze są odrzucane | `return false;` stoi w pętli i kończy funkcję po pierwszym niepasującym rekordzie (punkt 7). | Przenieś `return false;` za pętlę. |
| Jedno żądanie wydaje kilka egzemplarzy | Funkcja wywołuje operację dla każdego elementu albo nie kończy się po dopasowaniu. | Wywołuj operację tylko dla rekordu, którego kod pasuje, i od razu zwróć jej wynik. |
| Wynik to `accepted`, ale `After` pokazuje stary stan | Zmienna pętli albo parametr wektora nie ma `&`, więc zmienia się kopia (lekcja 9.3). | Funkcja zmieniająca elementy potrzebuje `&` w parametrze i w zmiennej pętli. |
| Drugie żądanie `TAB-03` jest przyjęte | Funkcja dla jednego egzemplarza nie sprawdza dostępności albo nie ustawia jej na `false`. | Sprawdź dostępność przed zmianą, a po wydaniu oznacz egzemplarz jako niedostępny. |
| Odrzucone żądanie zwiększa liczbę wypożyczeń | Funkcja zmienia pole przed sprawdzeniem dostępności (lekcja 9.2). | Najpierw sprawdź, potem zmień oba pola. |
| Ostrzeżenie `non-void function does not return a value in all control paths` | Brakuje `return false;` za pętlą. Gdy kodu nie ma, wywołanie dochodzi do końca funkcji bez `return`, a to niezdefiniowane zachowanie (lekcja 5.4). | Dopisz `return false;` za pętlą. |
| Błąd `no viable conversion from ... to 'bool'` w warunku | Warunek ma `=` (przypisanie) zamiast `==` (porównanie). | Porównuj kody przez `==`. |
| Dostępność wypisuje się jako `1` albo `0` | Program wypisuje wartość `bool` bezpośrednio (lekcja 3.2). | Wybierz tekst `yes` albo `no` instrukcją `if`. |

## 9. Wyjaśnij

Odpowiedz własnymi słowami, najlepiej na piśmie. Dopiero potem porównaj z przykładowymi odpowiedziami.

1. Dlaczego wyszukujemy po jednym określonym polu i dlaczego to pole musi być unikalne?
2. Dlaczego kody porównujemy przez `==`, a kod przekazujemy przez `const std::string&`?
3. Dlaczego funkcja dostaje wektor przez `&` i dlaczego zmienna pętli też ma `&`?
4. Co robi `return` wykonany wewnątrz pętli?
5. Dlaczego `return false;` nie może się wykonać po pierwszym niepasującym rekordzie?
6. Co oznacza `false`, jeśli rekord znaleziono, a co, jeśli nie znaleziono żadnego? Czy po samym `false` wiadomo, który z tych przypadków zaszedł?
7. Dlaczego regułę dostępności zna tylko funkcja dla jednego egzemplarza?
8. Dlaczego drugie żądanie `TAB-03` zostaje odrzucone?
9. Czy poprawne wyniki `accepted` i `refused` dowodzą, że wszystkie rekordy są w poprawnym stanie?
10. Czym ta lekcja różni się od lekcji 9.3?

<details>
<summary>Przykładowe odpowiedzi</summary>

1. Bo żądanie wskazuje jeden konkretny rekord, a pole kodu go identyfikuje. Gdyby dwa rekordy miały ten sam kod, funkcja zmieniłaby tylko pierwszy z nich, a żądanie byłoby niejednoznaczne. Dlatego w danych kody są unikalne.
2. `==` sprawdza, czy dwa teksty są takie same, jak w lekcji 3.4. Kod jest tylko czytany, więc wystarcza `const std::string&`: funkcja dostaje tekst do odczytu, bez kopiowania i bez prawa do zmiany.
3. Bo zmiana musi dotyczyć egzemplarza w wektorze z `main`. Parametr `&` daje dostęp do tego wektora, a zmienna pętli `&` do jego elementów, jak w lekcji 9.3. Bez któregokolwiek z nich zmieniałaby się kopia.
4. Kończy całe wywołanie funkcji i przekazuje wynik, a nie tylko jeden przebieg pętli. Dalsze elementy nie są już przeglądane.
5. Bo niepasujący bieżący rekord mówi tylko tyle, że szukany jest gdzie indziej albo go nie ma. Dopiero po przejrzeniu wszystkich rekordów wiadomo, że kodu nie ma.
6. Gdy rekord znaleziono, `false` znaczy, że funkcja dla jednego egzemplarza odmówiła. Gdy nie znaleziono, `false` znaczy, że nie było czego wydać. W obu przypadkach nic się nie zmieniło. Po samym `false` nie wiadomo, który przypadek zaszedł: wynik mówi tylko, czy operacja się odbyła.
7. Bo reguła powinna być w jednym miejscu. Funkcja dla kolekcji tylko znajduje właściwy rekord i przekazuje go dalej. Gdyby reguła się zmieniła, wystarczy poprawić jedną funkcję.
8. Bo wszystkie żądania dotyczą tego samego wektora. Pierwsze wydanie zmieniło `TAB-03` na niedostępny, więc przy drugim funkcja dla jednego egzemplarza odmawia.
9. Nie. Wyniki mogą się zgadzać, a zmienić się może zły rekord albo kopia. Dlatego przypadki kontrolne sprawdzają stan wszystkich rekordów po żądaniach.
10. W lekcji 9.3 funkcja przeglądała wszystkie rekordy i zmieniała każdy, który wymagał zmiany. Tutaj szuka jednego rekordu, zmienia tylko jego i kończy się po znalezieniu.

</details>

## Podsumowanie

- Funkcja wyszukująca przegląda istniejący wektor przez `&`, porównuje pole klucza z szukanym tekstem przez `==` i zmienia tylko znaleziony rekord, korzystając z funkcji dla jednego rekordu.
- `return` w pętli kończy całe wywołanie funkcji. Po znalezieniu rekordu to zamierzone, a `return false;` stoi za pętlą, bo „nie znaleziono” wiadomo dopiero po przejrzeniu wszystkich rekordów.
- `false` oznacza, że operacja się nie odbyła i kolekcja jest bez zmian. Może wynikać z braku rekordu albo z odmowy, a sam wynik tych przyczyn nie rozróżnia.
- Dla pustego wektora pętla nie wykonuje żadnego przebiegu, a funkcja zwraca `false`.
- Poprawny wynik `bool` nie dowodzi poprawnego stanu: trzeba sprawdzić wszystkie rekordy.

## Co dalej

Kolejna lekcja to sprawdzian Modułu 9. Wykorzystasz w nim umiejętności z całego modułu: kontrolowaną zmianę jednego rekordu, zmianę elementów wektora i wyszukiwanie rekordu do zmiany: [Lekcja 9.5: Flota dronów dostawczych (sprawdzian Modułu 9)](lesson_05_drone_fleet.md).

---

## Przykładowe rozwiązania

Zajrzyj tutaj **po własnej próbie**. Twoje nazwy mogą się różnić, jeśli standardowe wyjście jest takie, jak wymagane.

<details>
<summary>Punkt 6: misja, wydanie sprzętu po kodzie</summary>

<!-- example: school_loans -->
```cpp
#include <iostream>
#include <string>
#include <vector>

struct Equipment {
    std::string code;
    bool available;
    int loans;
};

bool borrow_item(Equipment& item) {
    if (!item.available) {
        return false;
    }

    item.available = false;
    ++item.loans;
    return true;
}

bool borrow_by_code(std::vector<Equipment>& items, const std::string& code) {
    for (Equipment& item : items) {
        if (item.code == code) {
            return borrow_item(item);
        }
    }

    return false;
}

int main() {
    std::vector<Equipment> items{
        {"CAM-01", true, 2},
        {"MIC-02", false, 4},
        {"TAB-03", true, 0},
        {"LAP-04", true, 1}
    };

    std::cout << "Equipment: " << items.size() << "\n";
    std::cout << "Before:\n";

    for (const Equipment& item : items) {
        std::cout << item.code << ": available ";

        if (item.available) {
            std::cout << "yes";
        } else {
            std::cout << "no";
        }

        std::cout << ", loans " << item.loans << "\n";
    }

    const bool tab_borrowed{borrow_by_code(items, "TAB-03")};

    if (tab_borrowed) {
        std::cout << "Borrow TAB-03: accepted\n";
    } else {
        std::cout << "Borrow TAB-03: refused\n";
    }

    const bool mic_borrowed{borrow_by_code(items, "MIC-02")};

    if (mic_borrowed) {
        std::cout << "Borrow MIC-02: accepted\n";
    } else {
        std::cout << "Borrow MIC-02: refused\n";
    }

    const bool bad_borrowed{borrow_by_code(items, "BAD-99")};

    if (bad_borrowed) {
        std::cout << "Borrow BAD-99: accepted\n";
    } else {
        std::cout << "Borrow BAD-99: refused\n";
    }

    const bool tab_borrowed_again{borrow_by_code(items, "TAB-03")};

    if (tab_borrowed_again) {
        std::cout << "Borrow TAB-03 again: accepted\n";
    } else {
        std::cout << "Borrow TAB-03 again: refused\n";
    }

    const bool cam_borrowed{borrow_by_code(items, "CAM-01")};

    if (cam_borrowed) {
        std::cout << "Borrow CAM-01: accepted\n";
    } else {
        std::cout << "Borrow CAM-01: refused\n";
    }

    std::cout << "After:\n";

    for (const Equipment& item : items) {
        std::cout << item.code << ": available ";

        if (item.available) {
            std::cout << "yes";
        } else {
            std::cout << "no";
        }

        std::cout << ", loans " << item.loans << "\n";
    }
}
```

1. **Wektor bez `const`,** bo żądania mają zmieniać jego elementy.
2. **Parametr wektora z `&`,** bo funkcja ma zmienić egzemplarz w wektorze z `main`, a nie w kopii.
3. **Zmienna pętli z `&`,** bo funkcja dla jednego egzemplarza ma dostać prawdziwy element, a nie jego kopię.
4. **Kod przez `const std::string&`,** bo funkcja tylko go odczytuje i porównuje. Nie potrzebuje kopii ani prawa do zmiany.
5. **`==`,** bo sprawdzamy, czy kod bieżącego rekordu jest dokładnie taki jak szukany.
6. **Regułę dostępności zna `borrow_item`,** bo to reguła jednego egzemplarza: sprawdza dostępność przed zmianą, a potem zmienia dwa pola.
7. **`borrow_by_code` jej nie powtarza:** tylko znajduje rekord i przekazuje go do `borrow_item`. Reguła jest w jednym miejscu.
8. **Dopasowanie kończy przeglądanie,** bo kody są unikalne, więc dalsze rekordy nie mogą pasować, a zadanie jest już wykonane.
9. **`return` w pętli kończy całą funkcję,** a nie jeden przebieg. Dlatego `return borrow_item(item);` od razu przekazuje wynik do `main`.
10. **`return false;` stoi za pętlą,** bo dopiero po przejrzeniu wszystkich rekordów wiadomo, że kodu nie ma.
11. **Niedostępny egzemplarz się nie zmienia,** bo `borrow_item` kończy się `return false;` przed zmianami, jak w lekcji 9.2.
12. **Brak kodu niczego nie zmienia,** bo bez dopasowania `borrow_item` nie jest wywoływana dla żadnego rekordu.
13. **Drugie żądanie `TAB-03` zostaje odrzucone,** bo pierwsze zmieniło ten sam rekord w tym samym wektorze na niedostępny.
14. **Pozostałe egzemplarze zachowują stan,** bo operacja dotyczy tylko rekordu, którego kod pasuje.
15. **Bez rozróżniania dwóch powodów odmowy,** bo raport potrzebuje tylko informacji, czy wydanie się odbyło. Gdyby program miał podać przyczynę, potrzebny byłby wynik, który przekazuje więcej informacji.
16. **Bez wskaźnika, iteratora i indeksu,** bo zmienna pętli `&` daje dostęp do znalezionego elementu, a `return` przekazuje wynik od razu.
17. **Liczba elementów się nie zmienia:** funkcje zmieniają tylko pola istniejących rekordów, niczego nie dodają ani nie usuwają.
18. **Inaczej niż w lekcji 9.3:** tam funkcja zmieniała każdy rekord, który wymagał zmiany, i liczyła zmiany. Tutaj szuka jednego rekordu, zmienia tylko jego i kończy się po znalezieniu.

**Inne poprawne rozwiązania:**

- warunek `if (item.available == false)` zamiast `if (!item.available)`;
- `item.loans += 1;` zamiast `++item.loans;`;
- własna funkcja, która wypisuje stan wszystkich egzemplarzy, wywołana dla `Before` i dla `After`, jeśli dostaje wektor przez `const&`;
- kod żądania zapisany w zmiennej `const std::string` i użyty w wywołaniu i w tekście.

To nie jedyne poprawne rozwiązanie: Twoje może mieć inne nazwy i inny układ `main`, jeśli spełnia wymagania.

**Wariant z pustym wektorem:**

<!-- example: school_loans_empty -->
```cpp
#include <iostream>
#include <string>
#include <vector>

struct Equipment {
    std::string code;
    bool available;
    int loans;
};

bool borrow_item(Equipment& item) {
    if (!item.available) {
        return false;
    }

    item.available = false;
    ++item.loans;
    return true;
}

bool borrow_by_code(std::vector<Equipment>& items, const std::string& code) {
    for (Equipment& item : items) {
        if (item.code == code) {
            return borrow_item(item);
        }
    }

    return false;
}

int main() {
    std::vector<Equipment> items{};

    std::cout << "Equipment: " << items.size() << "\n";

    const bool cam_borrowed{borrow_by_code(items, "CAM-01")};

    if (cam_borrowed) {
        std::cout << "Borrow CAM-01: accepted\n";
    } else {
        std::cout << "Borrow CAM-01: refused\n";
    }
}
```

**Program kontrolny** sprawdza wszystkie przypadki z listy kontrolnej. Typ i obie funkcje są takie same jak wyżej. Różnica jest w `main`: program odczytuje liczbę egzemplarzy, potem każdy egzemplarz (kod, `yes` albo `no` dla dostępności, liczbę wypożyczeń), a potem liczbę żądań. Każdy egzemplarz trafia na koniec wektora przez `push_back`, jak w programach kontrolnych lekcji 8.4–9.3. Kody żądań program odczytuje po jednym, dopiero w pętli żądań, i od razu wykonuje każde żądanie. Wypisuje `Before`, wynik każdego żądania i `After`, jak misja, ale bez słowa `again`. Misja nie potrzebuje ani wejścia, ani `push_back`.

<!-- example: school_loans_check -->
```cpp
#include <iostream>
#include <string>
#include <vector>

struct Equipment {
    std::string code;
    bool available;
    int loans;
};

bool borrow_item(Equipment& item) {
    if (!item.available) {
        return false;
    }

    item.available = false;
    ++item.loans;
    return true;
}

bool borrow_by_code(std::vector<Equipment>& items, const std::string& code) {
    for (Equipment& item : items) {
        if (item.code == code) {
            return borrow_item(item);
        }
    }

    return false;
}

int main() {
    std::vector<Equipment> items{};
    int count{0};

    std::cin >> count;

    for (int number{1}; number <= count; ++number) {
        std::string code{};
        std::string available_answer{};
        int loans{0};

        std::cin >> code;
        std::cin >> available_answer;
        std::cin >> loans;

        const Equipment item{code, available_answer == "yes", loans};
        items.push_back(item);
    }

    int request_count{0};
    std::cin >> request_count;

    if (std::cin.fail()) {
        std::cout << "Input could not be read\n";
    } else {
        std::cout << "Equipment: " << items.size() << "\n";
        std::cout << "Before:\n";

        for (const Equipment& item : items) {
            std::cout << item.code << ": available ";

            if (item.available) {
                std::cout << "yes";
            } else {
                std::cout << "no";
            }

            std::cout << ", loans " << item.loans << "\n";
        }

        for (int number{1}; number <= request_count; ++number) {
            std::string code{};
            std::cin >> code;

            const bool borrowed{borrow_by_code(items, code)};

            if (borrowed) {
                std::cout << "Borrow " << code << ": accepted\n";
            } else {
                std::cout << "Borrow " << code << ": refused\n";
            }
        }

        std::cout << "After:\n";

        for (const Equipment& item : items) {
            std::cout << item.code << ": available ";

            if (item.available) {
                std::cout << "yes";
            } else {
                std::cout << "no";
            }

            std::cout << ", loans " << item.loans << "\n";
        }
    }
}
```

Każdy przypadek zaczyna się od liczby egzemplarzy. Potem każdy egzemplarz zajmuje jedną linijkę: kod, dostępność i liczba wypożyczeń. Dalej stoi liczba żądań i kody żądań, po jednym w linijce. Przypadki stoją w kolejności z listy kontrolnej, od A do K.

<!-- input: school_loans_check -->
```text
4
CAM-01 yes 2
MIC-02 no 4
TAB-03 yes 0
LAP-04 yes 1
5
TAB-03
MIC-02
BAD-99
TAB-03
CAM-01
```

<!-- output: school_loans_check -->
```text
Equipment: 4
Before:
CAM-01: available yes, loans 2
MIC-02: available no, loans 4
TAB-03: available yes, loans 0
LAP-04: available yes, loans 1
Borrow TAB-03: accepted
Borrow MIC-02: refused
Borrow BAD-99: refused
Borrow TAB-03: refused
Borrow CAM-01: accepted
After:
CAM-01: available no, loans 3
MIC-02: available no, loans 4
TAB-03: available no, loans 1
LAP-04: available yes, loans 1
```

<!-- input: school_loans_check -->
```text
0
1
CAM-01
```

<!-- output: school_loans_check -->
```text
Equipment: 0
Before:
Borrow CAM-01: refused
After:
```

<!-- input: school_loans_check -->
```text
1
CAM-01 yes 0
1
CAM-01
```

<!-- output: school_loans_check -->
```text
Equipment: 1
Before:
CAM-01: available yes, loans 0
Borrow CAM-01: accepted
After:
CAM-01: available no, loans 1
```

<!-- input: school_loans_check -->
```text
1
CAM-01 no 3
1
CAM-01
```

<!-- output: school_loans_check -->
```text
Equipment: 1
Before:
CAM-01: available no, loans 3
Borrow CAM-01: refused
After:
CAM-01: available no, loans 3
```

<!-- input: school_loans_check -->
```text
3
CAM-01 yes 2
MIC-02 yes 0
TAB-03 yes 5
1
XYZ-00
```

<!-- output: school_loans_check -->
```text
Equipment: 3
Before:
CAM-01: available yes, loans 2
MIC-02: available yes, loans 0
TAB-03: available yes, loans 5
Borrow XYZ-00: refused
After:
CAM-01: available yes, loans 2
MIC-02: available yes, loans 0
TAB-03: available yes, loans 5
```

<!-- input: school_loans_check -->
```text
3
CAM-01 yes 2
MIC-02 yes 0
TAB-03 yes 5
1
CAM-01
```

<!-- output: school_loans_check -->
```text
Equipment: 3
Before:
CAM-01: available yes, loans 2
MIC-02: available yes, loans 0
TAB-03: available yes, loans 5
Borrow CAM-01: accepted
After:
CAM-01: available no, loans 3
MIC-02: available yes, loans 0
TAB-03: available yes, loans 5
```

<!-- input: school_loans_check -->
```text
3
CAM-01 yes 2
MIC-02 yes 0
TAB-03 yes 5
1
MIC-02
```

<!-- output: school_loans_check -->
```text
Equipment: 3
Before:
CAM-01: available yes, loans 2
MIC-02: available yes, loans 0
TAB-03: available yes, loans 5
Borrow MIC-02: accepted
After:
CAM-01: available yes, loans 2
MIC-02: available no, loans 1
TAB-03: available yes, loans 5
```

<!-- input: school_loans_check -->
```text
3
CAM-01 yes 2
MIC-02 yes 0
TAB-03 yes 5
1
TAB-03
```

<!-- output: school_loans_check -->
```text
Equipment: 3
Before:
CAM-01: available yes, loans 2
MIC-02: available yes, loans 0
TAB-03: available yes, loans 5
Borrow TAB-03: accepted
After:
CAM-01: available yes, loans 2
MIC-02: available yes, loans 0
TAB-03: available no, loans 6
```

<!-- input: school_loans_check -->
```text
2
LAP-04 yes 1
PRO-05 yes 3
2
LAP-04
LAP-04
```

<!-- output: school_loans_check -->
```text
Equipment: 2
Before:
LAP-04: available yes, loans 1
PRO-05: available yes, loans 3
Borrow LAP-04: accepted
Borrow LAP-04: refused
After:
LAP-04: available no, loans 2
PRO-05: available yes, loans 3
```

<!-- input: school_loans_check -->
```text
2
MIC-02 no 4
TAB-03 yes 0
2
MIC-02
TAB-03
```

<!-- output: school_loans_check -->
```text
Equipment: 2
Before:
MIC-02: available no, loans 4
TAB-03: available yes, loans 0
Borrow MIC-02: refused
Borrow TAB-03: accepted
After:
MIC-02: available no, loans 4
TAB-03: available no, loans 1
```

<!-- input: school_loans_check -->
```text
3
CAM-01 yes 0
MIC-02 yes 1
TAB-03 yes 2
3
TAB-03
CAM-01
MIC-02
```

<!-- output: school_loans_check -->
```text
Equipment: 3
Before:
CAM-01: available yes, loans 0
MIC-02: available yes, loans 1
TAB-03: available yes, loans 2
Borrow TAB-03: accepted
Borrow CAM-01: accepted
Borrow MIC-02: accepted
After:
CAM-01: available no, loans 1
MIC-02: available no, loans 2
TAB-03: available no, loans 3
```

</details>

<details>
<summary>Punkt 7: wyniki przed poprawką i poprawiony program</summary>

Przed poprawką, dla kodu pierwszego egzemplarza:

<!-- output: borrow_early_bug -->
```text
Before:
CAM-01: available yes, loans 2
MIC-02: available no, loans 4
TAB-03: available yes, loans 0
Borrow CAM-01: accepted
After:
CAM-01: available no, loans 3
MIC-02: available no, loans 4
TAB-03: available yes, loans 0
```

- **Dla pierwszego egzemplarza wynik jest poprawny,** bo dopasowanie następuje w pierwszym przebiegu, zanim błędny `return false;` zdąży się wykonać.
- **Dane, które ujawniają błąd:** kod egzemplarza, który nie jest pierwszy. Na przykład `TAB-03`, trzeci i dostępny. Poprawny wynik to `accepted` i `TAB-03: available no, loans 1`. Program z błędem wypisuje:

<!-- example: borrow_early_revealed -->
```cpp
#include <iostream>
#include <string>
#include <vector>

struct Equipment {
    std::string code;
    bool available;
    int loans;
};

bool borrow_item(Equipment& item) {
    if (!item.available) {
        return false;
    }

    item.available = false;
    ++item.loans;
    return true;
}

bool borrow_by_code(std::vector<Equipment>& items, const std::string& code) {
    for (Equipment& item : items) {
        if (item.code == code) {
            return borrow_item(item);
        }

        return false;
    }

    return false;
}

void print_items(const std::vector<Equipment>& items) {
    for (const Equipment& item : items) {
        std::cout << item.code << ": available ";

        if (item.available) {
            std::cout << "yes";
        } else {
            std::cout << "no";
        }

        std::cout << ", loans " << item.loans << "\n";
    }
}

int main() {
    std::vector<Equipment> items{
        {"CAM-01", true, 2},
        {"MIC-02", false, 4},
        {"TAB-03", true, 0}
    };
    const std::string code{"TAB-03"};

    std::cout << "Before:\n";
    print_items(items);

    const bool borrowed{borrow_by_code(items, code)};

    if (borrowed) {
        std::cout << "Borrow " << code << ": accepted\n";
    } else {
        std::cout << "Borrow " << code << ": refused\n";
    }

    std::cout << "After:\n";
    print_items(items);
}
```

<!-- output: borrow_early_revealed -->
```text
Before:
CAM-01: available yes, loans 2
MIC-02: available no, loans 4
TAB-03: available yes, loans 0
Borrow TAB-03: refused
After:
CAM-01: available yes, loans 2
MIC-02: available no, loans 4
TAB-03: available yes, loans 0
```

| Przebieg | `item` | `item.code == code` | Co się wykonuje |
|---|---|---|---|
| 1 | `CAM-01` | `false` | `return false;` w pętli: funkcja się kończy |
| 2 | `MIC-02` | nie jest sprawdzane | — |
| 3 | `TAB-03` | nie jest sprawdzane | — |

- **Pętla wykonuje jeden przebieg.** `return false;` stoi w ciele pętli, za `if`, więc wykonuje się w pierwszym przebiegu, w którym kod nie pasuje. Funkcja kończy się, zanim dotrze do `TAB-03`.
- **Niepasujący bieżący rekord nie oznacza, że nie pasuje żaden.** Ten `return false;` ogłasza „nie znaleziono” po sprawdzeniu jednego rekordu z trzech. Istniejący, dostępny egzemplarz nie zostaje ani znaleziony, ani wydany, a raport mówi `refused`.
- **Poprawka:** przenieś `return false;` za pętlę. Wtedy wykonuje się tylko po przejrzeniu wszystkich rekordów.
- **Porównanie z lekcją 5.7:** w zgłoszeniu C `return total;` też stał w ciele pętli bez warunku i kończył funkcję po pierwszym przebiegu. Tam maskowały go 0 i 1 runda, tu dopasowanie na pierwszej pozycji i pusty wektor. Nowe jest to, że w tej pętli jest też `return` zamierzony, po dopasowaniu, a błąd ma skutek w danych: właściwy rekord istnieje, ale się nie zmienia.

<!-- example: borrow_early_fixed -->
```cpp
#include <iostream>
#include <string>
#include <vector>

struct Equipment {
    std::string code;
    bool available;
    int loans;
};

bool borrow_item(Equipment& item) {
    if (!item.available) {
        return false;
    }

    item.available = false;
    ++item.loans;
    return true;
}

bool borrow_by_code(std::vector<Equipment>& items, const std::string& code) {
    for (Equipment& item : items) {
        if (item.code == code) {
            return borrow_item(item);
        }
    }

    return false;
}

void print_items(const std::vector<Equipment>& items) {
    for (const Equipment& item : items) {
        std::cout << item.code << ": available ";

        if (item.available) {
            std::cout << "yes";
        } else {
            std::cout << "no";
        }

        std::cout << ", loans " << item.loans << "\n";
    }
}

int main() {
    std::vector<Equipment> items{
        {"CAM-01", true, 2},
        {"MIC-02", false, 4},
        {"TAB-03", true, 0}
    };
    const std::string code{"TAB-03"};

    std::cout << "Before:\n";
    print_items(items);

    const bool borrowed{borrow_by_code(items, code)};

    if (borrowed) {
        std::cout << "Borrow " << code << ": accepted\n";
    } else {
        std::cout << "Borrow " << code << ": refused\n";
    }

    std::cout << "After:\n";
    print_items(items);
}
```

<!-- output: borrow_early_fixed -->
```text
Before:
CAM-01: available yes, loans 2
MIC-02: available no, loans 4
TAB-03: available yes, loans 0
Borrow TAB-03: accepted
After:
CAM-01: available yes, loans 2
MIC-02: available no, loans 4
TAB-03: available no, loans 1
```

**Pusty wektor:** obie wersje zwracają `false`. Pętla nie wykonuje żadnego przebiegu, więc błędny `return false;` w jej ciele nigdy się nie wykonuje, a obie funkcje dochodzą do `return false;` za pętlą. Dlatego pusty wektor błędu nie ujawnia.

</details>

**Poprzednia lekcja:** [Lekcja 9.3: Modyfikowanie elementów wektora przez referencję](lesson_03_changing_vector_elements.md) · **Następna lekcja:** [Lekcja 9.5: Flota dronów dostawczych (sprawdzian Modułu 9)](lesson_05_drone_fleet.md) · [Opis kursu](../../README.md)

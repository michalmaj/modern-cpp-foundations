# Lekcja 8.2: Zmiana pól i niezależna kopia rekordu

**Polski** · [English](lesson_02_changing_fields_and_copies.en.md) · [Opis kursu](../../README.md)

> **Moduł 8, lekcja 2** · około 65–80 minut
> **Potrzebujesz:** katalogu `cpp-workspace` i oryginalnego projektu `lesson_05_first_program`, jak dotąd. Debugger nie jest w tej lekcji potrzebny.
> **Wersja pilotażowa.** Programy z tej lekcji sprawdzamy automatycznie na Windowsie, Ubuntu i macOS. Żaden z nich nie pyta o dane: wszystkie wartości są zapisane w kodzie. Dane z wejścia odczytuje tylko program kontrolny w części z rozwiązaniami.

## Zanim zaczniesz

Ta lekcja zakłada, że:

- definiujesz strukturę, tworzysz jej obiekty z wartościami w `{}` i odczytujesz pola przez `.` (lekcja 8.1);
- odróżniasz inicjalizację od przypisania i wiesz, że przypisanie wartości jednej zmiennej do drugiej nie łączy tych zmiennych (lekcja 2.2);
- skracasz aktualizację przez `+=` (lekcja 4.2);
- znasz parametr `const&`, który pozwala czytać istniejący obiekt bez kopiowania go (lekcje 6.4 i 7.3).

## Sytuacja

W lekcji 8.1 każdy obiekt dostawał wartości raz, przy utworzeniu, i potem się nie zmieniał. Prawdziwe dane się jednak zmieniają. Książka w katalogu dostaje nowe wydanie z dodatkowymi stronami, a po lekturze trafia do przeczytanych. Na wydarzenie zapisują się kolejne osoby.

Ta lekcja odpowiada na dwa pytania:

1. **Jak zmienić dane istniejącego obiektu?**
2. **Jak zachować jego poprzedni stan**, żeby późniejsze zmiany nie zmieniły zapamiętanych wartości?

Po tej lekcji będziesz:

- zmieniać pola obiektu, który nie jest `const`, i świadomie decydować, który obiekt może się zmieniać;
- tworzyć kopię istniejącego rekordu zapisem `Book before{current};`;
- wyjaśniać, dlaczego kopia jest niezależna od oryginału, także jej pola `std::string`;
- odróżniać kopię od referencji `const&` do istniejącego obiektu;
- porównywać stan zapamiętany przed zmianą ze stanem bieżącym;
- dobierać dane, które ujawniają zmianę niewłaściwego obiektu.

## 1. Przygotuj projekt

W `cpp-workspace` utwórz katalog `lesson_8_2` i skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program`. Programy z punktów 2 i 4 wpisujesz w `main.cpp` tego katalogu. W tej lekcji korzystamy z typu `Book` z lekcji 8.1, bez zmian.

## 2. Zmiana pól

Katalog trzeba zaktualizować: książka `Guide` ma nowe wydanie, liczące 120 stron, i została przeczytana.

<!-- example: book_update -->
```cpp
#include <iostream>
#include <string>

struct Book {
    std::string title;
    int pages;
    bool finished;
};

int main() {
    Book book{"Guide", 100, false};

    std::cout << "Before pages: " << book.pages << "\n";

    if (book.finished) {
        std::cout << "Before finished: yes\n";
    } else {
        std::cout << "Before finished: no\n";
    }

    book.pages = 120;
    book.finished = true;

    std::cout << "After pages: " << book.pages << "\n";

    if (book.finished) {
        std::cout << "After finished: yes\n";
    } else {
        std::cout << "After finished: no\n";
    }
}
```

**Przewidź** wszystkie cztery linijki, a potem uruchom program.

<details>
<summary>Standardowe wyjście</summary>

<!-- output: book_update -->
```text
Before pages: 100
Before finished: no
After pages: 120
After finished: yes
```

</details>

- **`Book book{...}` nie ma `const`,** bo pola tego obiektu mają się zmieniać.
- **`book.pages = 120;` to przypisanie,** jak `count = 5;` w lekcji 2.2. Po lewej stronie stoi pole konkretnego obiektu, więc nowa wartość trafia do tego pola.
- **Zmiana jednego pola nie zmienia pozostałych.** Po pierwszym przypisaniu `title` i `finished` mają te same wartości co wcześniej. `book.finished = true;` zmienia już inne pole.
- **Definicja typu `Book` się nie zmienia.** Każda książka nadal ma te same trzy pola. Zmieniła się tylko wartość pola jednego obiektu.

Tak samo zmienisz pole tekstowe, na przykład `book.title = "Guide 2";`. Na polu liczbowym działa też `+=` z lekcji 4.2: `book.pages += 20;` zwiększyłoby liczbę stron ze 100 do 120.

Linijki `Before` program wypisał, zanim zmienił pola. Po przypisaniach stare wartości już w obiekcie nie istnieją: `book.pages` to teraz 120.

## 3. Obiekt `const` a zmiana pól

W lekcji 8.1 obiekty miały `const`:

<!-- fragment -->
```cpp
const Book book{"Guide", 100, false};

book.pages = 120;
```

Ten fragment się nie zbuduje. Clang zgłasza `cannot assign to variable 'book' with const-qualified type 'const Book'`, podobnie jak przy stałej `int` w lekcji 2.2. Problem nie dotyczy typu pola: `pages` to zwykłe pole `int`. Program próbuje je zmienić przez obiekt `const`, a taki obiekt służy tylko do odczytu.

**Poprawka to świadoma decyzja:** usuń `const` tylko wtedy, gdy obiekt naprawdę ma się zmieniać. **Obiekt, który nie powinien się później zmieniać, nadal oznaczamy `const`.** Wtedy kompilator przypilnuje, żeby żadna linijka nie zmieniła go przez pomyłkę.

## 4. Kopia rekordu

Program z punktu 2 zgubił stare wartości. Jak je zachować, żeby po aktualizacji porównać stan przed i po?

<!-- example: book_snapshot -->
```cpp
#include <iostream>
#include <string>

struct Book {
    std::string title;
    int pages;
    bool finished;
};

int main() {
    Book current{"Guide", 100, false};
    const Book before{current};

    current.pages = 120;
    current.finished = true;

    std::cout << "Before: " << before.title << ", " << before.pages << " pages\n";
    std::cout << "Current: " << current.title << ", " << current.pages << " pages\n";

    if (before.finished) {
        std::cout << "Before finished: yes\n";
    } else {
        std::cout << "Before finished: no\n";
    }

    if (current.finished) {
        std::cout << "Current finished: yes\n";
    } else {
        std::cout << "Current finished: no\n";
    }
}
```

**Przewidź:** ile stron ma `before` po zmianie `current.pages`?

<details>
<summary>Standardowe wyjście</summary>

<!-- output: book_snapshot -->
```text
Before: Guide, 100 pages
Current: Guide, 120 pages
Before finished: no
Current finished: yes
```

</details>

1. **`current` jest obiektem modyfikowalnym:** jego pola się zmieniają.
2. **`const Book before{current};` tworzy nowy obiekt** typu `Book`, z wartościami wszystkich pól `current` z tej chwili. To nie jest nowy typ: `Book` to nadal ten sam typ, a `before` to kolejny obiekt.
3. **Kopiowany jest cały rekord,** nie tylko `pages`: tytuł, liczba stron i `finished`.
4. **`before` ma `const`,** bo ma zachować poprzedni stan. Nikt nie powinien go zmieniać.
5. **Późniejsze zmiany `current` nie zmieniają `before`.** To dwa osobne obiekty. Na początku mają te same wartości pól, bo `before` powstał z `current`, ale potem każdy przechowuje własne.
6. **Pole `std::string` też należy do kopii.** Gdyby program po utworzeniu kopii zmienił `current.title`, `before.title` nadal zawierałoby `Guide`.

| Moment | `current` | `before` |
|---|---|---|
| po `const Book before{current};` | `Guide`, 100, `false` | `Guide`, 100, `false` |
| po `current.pages = 120;` | `Guide`, 120, `false` | `Guide`, 100, `false` |
| po `current.finished = true;` | `Guide`, 120, `true` | `Guide`, 100, `false` |

To ten sam mechanizm co w lekcji 2.2, gdzie `second` dostało kopię wartości `first`: zmienne nie zostały połączone, a późniejsza zmiana `first` nie zmieniła `second`. Kopia rekordu robi to samo, tylko dla wszystkich pól naraz.

**Ważna jest kolejność:** kopię tworzysz **przed** zmianą. Kopia utworzona po aktualizacji zapamiętałaby już nowe wartości.

`Book before{current};` tworzy nowy obiekt z wartością innego obiektu, czyli jest inicjalizacją, jak `int count{3};`. C++ pozwala też przypisać cały rekord do obiektu, który już istnieje, ale w tej lekcji z tego nie korzystamy.

## 5. Kopia, zmiana i referencja

| Zapis | Znaczenie |
|---|---|
| `Book first{...};` i `Book second{...};` | dwa obiekty utworzone osobno, każdy z własnymi wartościami (lekcja 8.1) |
| `current.pages = 120;` | ten sam obiekt dostaje nową wartość pola |
| `Book copy{original};` | powstaje nowy obiekt z wartościami pól oryginału |
| `const Book snapshot{original};` | powstaje niezależna kopia, której później nie zmieniamy |
| `const Book& view{original};` | powstaje referencja do istniejącego obiektu, umożliwiająca odczyt |

Ostatni wiersz to tylko przypomnienie idei `const&` z lekcji 6.4, tym razem bez funkcji: `view` to inna nazwa tego samego obiektu `original`. Właśnie dlatego **referencja nie zapamiętuje starego stanu**: gdy `original` się zmieni, przez `view` odczytasz już nowe wartości. Do zachowania stanu sprzed zmiany potrzebna jest kopia. W tej lekcji z referencji nie korzystamy.

## 6. Misja: przed i po nowych rezerwacjach

Program przechowuje informacje o wydarzeniu: jego nazwę, maksymalną liczbę miejsc i liczbę osób już zapisanych. Na wydarzenie zgłaszają się nowe osoby. Program sprawdza, czy można przyjąć wszystkie nowe rezerwacje, i porównuje stan przed zmianą i po niej.

**Dane:** wydarzenie `C++ Workshop`, 12 miejsc, 7 osób już zapisanych, 3 nowe rezerwacje.

**Reguły:**

- Wszystkie liczby są całkowite i nieujemne. Na początku liczba zapisanych osób nie przekracza liczby miejsc.
- Nowe rezerwacje przyjmujemy **w całości albo wcale**. Gdy wolnych miejsc wystarczy dla wszystkich nowych osób, także dokładnie, rezerwacje są przyjmowane. Gdy brakuje choćby jednego miejsca, liczba zapisanych się nie zmienia.
- Zero nowych rezerwacji to aktualizacja bez zmiany: zgłoszenie jest przyjęte, a liczba zapisanych zostaje taka sama.

**Wymagania:**

- Program definiuje własny typ z trzema polami: nazwą wydarzenia (`std::string`), liczbą miejsc (`int`) i liczbą zapisanych osób (`int`). Nazwy typu i pól wybierasz samodzielnie.
- Liczba nowych rezerwacji to zwykła zmienna `int` w `main`, a nie pole: nie opisuje trwałego stanu wydarzenia.
- W `main` jest jeden modyfikowalny obiekt wydarzenia i jego kopia sprzed zmiany, oznaczona `const`. Program nie tworzy innych obiektów, które powielają ten sam stan.
- Gdy rezerwacje są przyjęte, program zmienia pole liczby zapisanych w bieżącym obiekcie.
- Program wypisuje dokładnie siedem linijek:
  - `Event`: nazwa wydarzenia;
  - `Capacity`: liczba miejsc;
  - `Before`: liczba zapisanych z kopii sprzed zmiany;
  - `Requested`: liczba nowych rezerwacji;
  - `Accepted`: `yes` albo `no`;
  - `After`: liczba zapisanych z bieżącego obiektu;
  - `Seats left`: liczba miejsc minus bieżąca liczba zapisanych.
- Program nie odczytuje niczego z wejścia i nie potrzebuje własnych funkcji.

W `cpp-workspace` utwórz katalog `event_bookings`, skopiuj do niego `CMakeLists.txt` z oryginalnego `lesson_05_first_program`, utwórz pusty `main.cpp` i napisz program samodzielnie.

Dla danych powyżej standardowe wyjście ma być takie:

<!-- output: event_bookings -->
```text
Event: C++ Workshop
Capacity: 12
Before: 7
Requested: 3
Accepted: yes
After: 10
Seats left: 2
```

Wolnych miejsc jest 5, więc 3 nowe osoby się mieszczą: zapisanych jest teraz 10, a wolne zostają 2.

**To nie jest program z punktu 4 z innymi nazwami.** Musisz samodzielnie zdecydować:

1. jak nazwać typ i jego pola;
2. który obiekt ma się zmieniać, a który ma być `const`;
3. w którym miejscu programu utworzyć kopię;
4. jak sprawdzić, czy wolnych miejsc wystarczy dla wszystkich nowych osób;
5. które pole zmienić, w którym obiekcie i kiedy;
6. z którego obiektu pochodzi każda linijka raportu;
7. jak sprawić, żeby liczba wolnych miejsc nigdy nie była ujemna.

**Zanim napiszesz program**, przygotuj tabelę przypadków: mniej nowych osób niż wolnych miejsc, dokładnie tyle samo, o jedną więcej, pełne wydarzenie, wydarzenie bez zapisanych osób, zero nowych rezerwacji i zero miejsc. Przy każdym zapisz `Accepted`, `After` i `Seats left`.

**Potem** uruchom program dla danych z wymagań i dla dwóch innych przypadków z tabeli, na przykład dla odrzuconej prośby i dla zera nowych rezerwacji. Zmieniaj przy tym tylko wartości w klamrach i liczbę nowych rezerwacji. Wszystkie przypadki z pełnej listy kontrolnej są sprawdzone automatycznie.

### Kryterium sukcesu

- Program buduje się jako C++20 i dla danych z wymagań wypisuje dokładnie siedem linijek pokazanych wyżej.
- Jest jeden typ z trzema polami, jeden modyfikowalny obiekt i jego kopia `const`, utworzona przed zmianą.
- `Before` pochodzi z kopii, a `After` i `Seats left` z bieżącego obiektu.
- Odrzucona prośba nie zmienia liczby zapisanych, a liczba zapisanych nigdy nie przekracza liczby miejsc.
- Zero nowych rezerwacji daje `Accepted: yes` i niezmienioną liczbę zapisanych.
- Tabela przypadków powstała przed uruchomieniem programu.
- Umiesz wskazać, z którego obiektu pochodzi każda linijka raportu.

Gdy wynik się zgadza, możesz zapisać projekt w Gicie, jak w lekcji 1.5.

<details>
<summary>Podpowiedź 1</summary>

Jak zachować liczbę zarejestrowanych osób sprzed zmiany, jeżeli bieżący rekord ma później przechowywać nową liczbę?

</details>

<details>
<summary>Podpowiedź 2</summary>

Utwórz niezależny rekord na podstawie bieżącego, zanim zaczniesz go zmieniać. Który z tych obiektów powinien pozostać `const`?

</details>

<details>
<summary>Podpowiedź 3</summary>

Przyjmij nowe zgłoszenia tylko wtedy, gdy liczba wolnych miejsc jest wystarczająca. Zmieniaj pole bieżącego obiektu, a poprzedni stan odczytuj z zachowanej kopii.

</details>

<details>
<summary>Pełna lista przypadków kontrolnych: otwórz po przygotowaniu własnej tabeli</summary>

| | Wydarzenie | Miejsca | Przed | Nowe | Przyjęte | Po | Wolne | Co sprawdza |
|---|---|---:|---:|---:|---|---:|---:|---|
| A | `C++ Workshop` | 12 | 7 | 3 | yes | 10 | 2 | dane z wymagań: mniej osób niż wolnych miejsc |
| B | `Talk` | 12 | 7 | 5 | yes | 12 | 0 | dokładnie wszystkie wolne miejsca |
| C | `Talk` | 12 | 7 | 6 | no | 7 | 5 | o jedną osobę za dużo: rekord bez zmian |
| D | `Full` | 5 | 5 | 1 | no | 5 | 0 | pełne wydarzenie |
| E | `Empty` | 10 | 0 | 4 | yes | 4 | 6 | nikt jeszcze nie jest zapisany |
| F | `No change` | 10 | 4 | 0 | yes | 4 | 6 | zero nowych rezerwacji |
| G | `No capacity` | 0 | 0 | 1 | no | 0 | 0 | zero miejsc |
| H | `One seat` | 1 | 0 | 1 | yes | 1 | 0 | jedno miejsce, wypełnione |

**Testy automatyczne i Twoje próby.** Wszystkie przypadki są sprawdzone automatycznie przez program kontrolny. Ma on tę samą strukturę i tę samą logikę co rozwiązanie referencyjne, ale nazwę wydarzenia i trzy liczby odczytuje z wejścia, po jednej wartości w linijce. To tylko narzędzie do sprawdzania, a nie część misji: w misji dane są wpisane w kodzie. Program kontrolny i jego wyniki są w części [Przykładowe rozwiązania](#przykładowe-rozwiązania), bo zawierają rozwiązanie.

</details>

Przykładowe rozwiązanie jest w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 7. Znajdź błąd: zmieniona niewłaściwa kopia

To zadanie wykonaj **po misji**: program poniżej zawiera typ podobny do Twojego. Ktoś przyjmuje w nim zgłoszenia na spotkanie i uważa, że `copied` to inna nazwa tego samego wydarzenia. Program możesz przepisać albo skopiować do `main.cpp`.

<details>
<summary>Program do sprawdzenia: otwórz po napisaniu własnego programu</summary>

<!-- example: event_copy_bug -->
```cpp
#include <iostream>
#include <string>

struct Event {
    std::string name;
    int capacity;
    int registered;
};

int main() {
    Event current{"Meeting", 10, 4};
    Event copied{current};
    const int requested{0};

    if (requested <= current.capacity - current.registered) {
        copied.registered += requested;
    }

    std::cout << "Event: " << current.name << "\n";
    std::cout << "Requested: " << requested << "\n";
    std::cout << "Registered: " << current.registered << "\n";
    std::cout << "Seats left: " << current.capacity - current.registered << "\n";
}
```

1. Wskaż oba obiekty typu `Event`.
2. Który z nich powstał jako kopia?
3. **Przewidź**, które pole którego obiektu naprawdę się zmienia.
4. **Przewidź** standardowe wyjście dla `requested` równego 0, a potem uruchom program. Czy wynik wygląda poprawnie?
5. Zmień wartość `requested` tak, żeby błąd stał się widoczny. Najpierw zapisz poprawny wynik dla swojej wartości, a potem uruchom program.
6. Wyjaśnij przyczynę błędu.
7. Popraw aktualizację: zmień właściwe pole właściwego obiektu.
8. Uruchom poprawiony program dla swojej wartości i dla 0.

</details>

Wyniki, przykładowa wartość i poprawiony program są w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 8. Gdy coś pójdzie inaczej

| Co widzisz | Co to znaczy | Co zrobić |
|---|---|---|
| `cannot assign to variable ... with const-qualified type` przy zmianie pola | Pole jest zmieniane przez obiekt `const` (punkt 3). | Usuń `const` tylko z obiektu, który ma się zmieniać. Kopii sprzed zmiany nie zmieniaj. |
| `Before` pokazuje już nową wartość | Kopia powstała dopiero po zmianie. | Utwórz kopię przed zmianą. |
| `After` pokazuje starą wartość | Program zmienił kopię zamiast bieżącego obiektu (punkt 7). | Zmieniaj pole bieżącego obiektu. |
| `Before` i `After` są zawsze równe, także po przyjęciu rezerwacji | Obie linijki odczytują ten sam obiekt albo zmiana nie trafiła do bieżącego obiektu. | Sprawdź, z którego obiektu pochodzi każda linijka raportu. |
| Liczba zapisanych przekracza liczbę miejsc albo `Seats left` jest ujemne | Program dodaje nowe osoby bez sprawdzenia wolnych miejsc. | Najpierw porównaj nowe rezerwacje z liczbą wolnych miejsc, potem zmieniaj pole. |
| Odrzucona prośba zmienia liczbę zapisanych | Zmiana pola stoi poza warunkiem. | Zmieniaj pole tylko w gałęzi, w której rezerwacje są przyjęte. |
| Zero nowych rezerwacji daje `Accepted: no` | Warunek wymaga więcej niż zera nowych osób albo używa `<` zamiast `<=`. | Zero mieści się zawsze: wystarczy, że nowych osób nie jest więcej niż wolnych miejsc. |

## 9. Wyjaśnij

Odpowiedz własnymi słowami, najlepiej na piśmie. Dopiero potem porównaj z przykładowymi odpowiedziami.

1. Dlaczego w lekcji 8.1 obiekty mogły mieć `const`, a w tej lekcji bieżący obiekt go nie ma?
2. Co oznacza `current.registered = 10;`? Czy zmienia definicję struktury?
3. Co oznacza `Book copy{original};`? Czy powstaje nowy obiekt?
4. Czy późniejsza zmiana `original` zmienia `copy`? Czy dotyczy to także pola `std::string`?
5. Dlaczego `const Book before{current};` dobrze zachowuje niezmieniany stan, a rekord, którego pola aktualizujesz, nie powinien być `const`?
6. Czym różni się kopia od referencji `const&` do istniejącego obiektu? Dlaczego referencja nie zapamięta starego stanu?
7. Dlaczego kopię tworzymy przed zmianą, a nie po niej?
8. Dlaczego w misji nie wolno aktualizować kopii zamiast bieżącego rekordu?
9. Dlaczego sprawdzenie wolnych miejsc musi nastąpić przed przyjęciem zgłoszeń?

<details>
<summary>Przykładowe odpowiedzi</summary>

1. Bo w lekcji 8.1 żaden obiekt się nie zmieniał. Tutaj pola bieżącego obiektu mają dostać nowe wartości, a przez obiekt `const` nie da się ich zmienić.
2. To przypisanie nowej wartości do pola `registered` obiektu `current`. Definicja struktury się nie zmienia: typ ma nadal te same pola, a zmienia się tylko wartość jednego pola jednego obiektu.
3. Tworzy nowy obiekt `copy` z wartościami wszystkich pól obiektu `original` z tej chwili. Tak, to drugi, osobny obiekt tego samego typu.
4. Nie. Kopia ma własne wartości pól, także własny tekst w polu `std::string`. Zmiana oryginału nie przenosi się na kopię.
5. Bo kopia ma zachować stan sprzed zmiany, więc nic nie powinno jej zmieniać, a `const` pozwala kompilatorowi tego przypilnować. Bieżący rekord ma dostawać nowe wartości, więc `const` by na to nie pozwoliło.
6. Kopia to osobny obiekt z własnymi wartościami. Referencja to inna nazwa istniejącego obiektu: odczytuje jego aktualne wartości, więc po zmianie oryginału pokazuje już nowe.
7. Bo kopia zapamiętuje wartości z chwili, w której powstaje. Kopia utworzona po zmianie zawierałaby już nowe wartości.
8. Bo zmiana kopii nie zmienia bieżącego rekordu: to dwa niezależne obiekty. Raport `After` i liczba wolnych miejsc pochodzą z bieżącego obiektu, więc nie pokazałyby przyjętych rezerwacji, a kopia przestałaby pokazywać stan sprzed zmiany.
9. Bo rezerwacje przyjmujemy w całości albo wcale. Gdyby program najpierw zmienił pole, a dopiero potem sprawdził miejsca, odrzucona prośba zdążyłaby zmienić rekord albo przekroczyć liczbę miejsc.

</details>

## Podsumowanie

- Obiekt bez `const` może zmieniać pola: `book.pages = 120;` przypisuje nową wartość polu tego obiektu. Na polu liczbowym działa też `+=`.
- Zmiana pola nie zmienia definicji typu ani pozostałych pól.
- Obiekt, który nie powinien się zmieniać, nadal oznaczamy `const`, a kompilator pilnuje, żeby nic go nie zmieniło.
- `Book before{current};` tworzy nowy obiekt z wartościami wszystkich pól `current`, także pól `std::string`. Kopia i oryginał są niezależne.
- Kopię sprzed zmiany tworzymy przed aktualizacją i oznaczamy `const`.
- Referencja `const&` nie zapamiętuje starego stanu: pokazuje aktualne wartości oryginału.

## Co dalej

W tej lekcji wszystkie działania na rekordach stały w `main`. W kolejnej lekcji rekord trafi do funkcji, która go odczyta i obliczy wynik z jego pól: [Lekcja 8.3: Funkcje, które analizują rekord](lesson_03_functions_that_analyse_a_record.md).

---

## Przykładowe rozwiązania

Zajrzyj tutaj **po własnej próbie**. Twoje nazwy mogą się różnić, jeśli standardowe wyjście jest takie, jak wymagane.

<details>
<summary>Punkt 6: misja, rezerwacje na wydarzenie</summary>

<!-- example: event_bookings -->
```cpp
#include <iostream>
#include <string>

struct Event {
    std::string name;
    int capacity;
    int registered;
};

int main() {
    Event current{"C++ Workshop", 12, 7};
    const Event before{current};
    const int requested{3};

    const int free_seats{current.capacity - current.registered};
    const bool accepted{requested <= free_seats};

    if (accepted) {
        current.registered += requested;
    }

    std::cout << "Event: " << current.name << "\n";
    std::cout << "Capacity: " << current.capacity << "\n";
    std::cout << "Before: " << before.registered << "\n";
    std::cout << "Requested: " << requested << "\n";

    if (accepted) {
        std::cout << "Accepted: yes\n";
    } else {
        std::cout << "Accepted: no\n";
    }

    std::cout << "After: " << current.registered << "\n";
    std::cout << "Seats left: " << current.capacity - current.registered << "\n";
}
```

1. **`current` nie ma `const`,** bo po przyjęciu rezerwacji jego pole `registered` dostaje nową wartość.
2. **Kopię tworzymy przed zmianą,** bo zapamiętuje wartości z chwili, w której powstaje.
3. **Kopia może być `const`,** bo nic nie ma jej zmieniać. Kompilator pilnuje, żeby nikt jej nie zmienił przez pomyłkę.
4. **`before.registered` zachowuje 7,** bo `before` to osobny obiekt: zmiana `current.registered` go nie dotyczy.
5. **`current.registered` przechowuje 10,** bo po przyjęciu rezerwacji program zmienia właśnie to pole bieżącego obiektu.
6. **Odmowa nie zmienia rekordu:** `+=` stoi tylko w gałęzi, w której `accepted` daje `true`.
7. **Zero nowych rezerwacji** spełnia warunek `0 <= free_seats`, więc `Accepted: yes`, a dodanie 0 nie zmienia liczby zapisanych.
8. **Modyfikowalna referencja nie jest potrzebna:** wszystkie zmiany dzieją się w `main`, na obiekcie `current`.
9. **Funkcje nie są potrzebne:** program sprawdza jeden warunek i zmienia jedno pole. Przekazywanie rekordów do funkcji to temat kolejnej lekcji.
10. **Stary stan to jeden obiekt, a nie kilka zmiennych.** Kopia zachowuje wszystkie pola naraz, więc nie trzeba pamiętać, które wartości przepisać do osobnych zmiennych.
11. **Kopia to nie druga nazwa obiektu `current`:** ma własne wartości pól. Dlatego po aktualizacji `before` i `current` się różnią.
12. **Inne poprawne warunki:** `current.registered + requested <= current.capacity` daje ten sam wynik. Można też zmienić pole i wypisać `Accepted: yes` w jednej gałęzi `if`, a `Accepted: no` w gałęzi `else`. Ważne, żeby pole zmieniało się tylko po sprawdzeniu miejsc, i tylko w bieżącym obiekcie.

`Seats left` nigdy nie jest ujemne: na początku liczba zapisanych nie przekracza liczby miejsc, a nowe osoby dochodzą tylko wtedy, gdy się mieszczą.

**Program kontrolny** sprawdza wszystkie przypadki z listy kontrolnej. Struktura i logika od obliczenia wolnych miejsc są takie same jak wyżej, poza wcięciem. Różnica jest jedna: nazwa wydarzenia i trzy liczby są odczytywane z wejścia do zwykłych zmiennych, a obiekt `current` powstaje z ich wartości. Nazwę odczytuje `std::getline`, bo może zawierać spację, a liczby `>>`, dopiero po niej.

<!-- example: event_bookings_check -->
```cpp
#include <iostream>
#include <string>

struct Event {
    std::string name;
    int capacity;
    int registered;
};

int main() {
    std::string name{};
    int capacity{0};
    int registered{0};
    int requested{0};

    std::getline(std::cin, name);
    std::cin >> capacity;
    std::cin >> registered;
    std::cin >> requested;

    if (std::cin.fail()) {
        std::cout << "Input could not be read\n";
    } else {
        Event current{name, capacity, registered};
        const Event before{current};

        const int free_seats{current.capacity - current.registered};
        const bool accepted{requested <= free_seats};

        if (accepted) {
            current.registered += requested;
        }

        std::cout << "Event: " << current.name << "\n";
        std::cout << "Capacity: " << current.capacity << "\n";
        std::cout << "Before: " << before.registered << "\n";
        std::cout << "Requested: " << requested << "\n";

        if (accepted) {
            std::cout << "Accepted: yes\n";
        } else {
            std::cout << "Accepted: no\n";
        }

        std::cout << "After: " << current.registered << "\n";
        std::cout << "Seats left: " << current.capacity - current.registered << "\n";
    }
}
```

Każdy przypadek to cztery linijki wejścia: nazwa wydarzenia, liczba miejsc, liczba zapisanych i liczba nowych rezerwacji, w kolejności z listy kontrolnej, od A do H.

<!-- input: event_bookings_check -->
```text
C++ Workshop
12
7
3
```

<!-- output: event_bookings_check -->
```text
Event: C++ Workshop
Capacity: 12
Before: 7
Requested: 3
Accepted: yes
After: 10
Seats left: 2
```

<!-- input: event_bookings_check -->
```text
Talk
12
7
5
```

<!-- output: event_bookings_check -->
```text
Event: Talk
Capacity: 12
Before: 7
Requested: 5
Accepted: yes
After: 12
Seats left: 0
```

<!-- input: event_bookings_check -->
```text
Talk
12
7
6
```

<!-- output: event_bookings_check -->
```text
Event: Talk
Capacity: 12
Before: 7
Requested: 6
Accepted: no
After: 7
Seats left: 5
```

<!-- input: event_bookings_check -->
```text
Full
5
5
1
```

<!-- output: event_bookings_check -->
```text
Event: Full
Capacity: 5
Before: 5
Requested: 1
Accepted: no
After: 5
Seats left: 0
```

<!-- input: event_bookings_check -->
```text
Empty
10
0
4
```

<!-- output: event_bookings_check -->
```text
Event: Empty
Capacity: 10
Before: 0
Requested: 4
Accepted: yes
After: 4
Seats left: 6
```

<!-- input: event_bookings_check -->
```text
No change
10
4
0
```

<!-- output: event_bookings_check -->
```text
Event: No change
Capacity: 10
Before: 4
Requested: 0
Accepted: yes
After: 4
Seats left: 6
```

<!-- input: event_bookings_check -->
```text
No capacity
0
0
1
```

<!-- output: event_bookings_check -->
```text
Event: No capacity
Capacity: 0
Before: 0
Requested: 1
Accepted: no
After: 0
Seats left: 0
```

<!-- input: event_bookings_check -->
```text
One seat
1
0
1
```

<!-- output: event_bookings_check -->
```text
Event: One seat
Capacity: 1
Before: 0
Requested: 1
Accepted: yes
After: 1
Seats left: 0
```

</details>

<details>
<summary>Punkt 7: wyniki przed poprawką i poprawiony program</summary>

Przed poprawką, dla `requested` równego 0:

<!-- output: event_copy_bug -->
```text
Event: Meeting
Requested: 0
Registered: 4
Seats left: 6
```

- **Dwa obiekty:** `current` i `copied`. `copied` powstał jako kopia `current`.
- **Zmienia się `copied.registered`,** a nie `current.registered`. To dwa niezależne obiekty, więc `current` nic o tej zmianie „nie wie”.
- **Dla 0 wynik wygląda poprawnie,** bo dodanie zera niczego nie zmienia: poprawny program wypisałby to samo.
- **Dane, które ujawniają błąd:** każda dodatnia liczba nowych zgłoszeń, która mieści się w wolnych miejscach. Na przykład 3: poprawny wynik to 7 zapisanych i 3 wolne miejsca. Program z błędem wypisuje:

<!-- example: event_copy_revealed -->
```cpp
#include <iostream>
#include <string>

struct Event {
    std::string name;
    int capacity;
    int registered;
};

int main() {
    Event current{"Meeting", 10, 4};
    Event copied{current};
    const int requested{3};

    if (requested <= current.capacity - current.registered) {
        copied.registered += requested;
    }

    std::cout << "Event: " << current.name << "\n";
    std::cout << "Requested: " << requested << "\n";
    std::cout << "Registered: " << current.registered << "\n";
    std::cout << "Seats left: " << current.capacity - current.registered << "\n";
}
```

<!-- output: event_copy_revealed -->
```text
Event: Meeting
Requested: 3
Registered: 4
Seats left: 6
```

| Obiekt | `registered` przed `+=` | `registered` po `+=` |
|---|---:|---:|
| `current` | 4 | 4 |
| `copied` | 4 | **7** |

- **Przyczyna:** program zakłada, że `copied` to inna nazwa tego samego wydarzenia. Ale `Event copied{current};` tworzy nowy, niezależny obiekt. Rezerwacje trafiły do kopii, a raport czyta `current`, który się nie zmienił.
- **Poprawka:** zmieniaj pole bieżącego obiektu: `current.registered += requested;`. Kopia nie jest wtedy do niczego potrzebna, bo ten program nie wypisuje stanu sprzed zmiany, więc znika.

<!-- example: event_copy_fixed -->
```cpp
#include <iostream>
#include <string>

struct Event {
    std::string name;
    int capacity;
    int registered;
};

int main() {
    Event current{"Meeting", 10, 4};
    const int requested{3};

    if (requested <= current.capacity - current.registered) {
        current.registered += requested;
    }

    std::cout << "Event: " << current.name << "\n";
    std::cout << "Requested: " << requested << "\n";
    std::cout << "Registered: " << current.registered << "\n";
    std::cout << "Seats left: " << current.capacity - current.registered << "\n";
}
```

<!-- output: event_copy_fixed -->
```text
Event: Meeting
Requested: 3
Registered: 7
Seats left: 3
```

Dla 0 poprawiony program wypisuje to samo co przed poprawką, bo dodanie zera niczego nie zmienia. Dlatego sam przypadek z zerem nie wystarczy, żeby sprawdzić, który obiekt się zmienia.

Gdyby kopia była potrzebna do zapamiętania stanu sprzed zmiany, jak `before` w misji, powinna być `const`. Wtedy linijka `copied.registered += requested;` w ogóle by się nie zbudowała, a kompilator wskazałby pomyłkę od razu.

</details>

**Poprzednia lekcja:** [Lekcja 8.1: Pierwsza struktura: kilka danych opisujących jeden obiekt](lesson_01_first_struct.md) · **Następna lekcja:** [Lekcja 8.3: Funkcje, które analizują rekord](lesson_03_functions_that_analyse_a_record.md) · [Opis kursu](../../README.md)

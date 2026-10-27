# Lekcja 8.1: Pierwsza struktura: kilka danych opisujących jeden obiekt

**Polski** · [English](lesson_01_first_struct.en.md) · [Opis kursu](../../README.md)

> **Moduł 8, lekcja 1** · około 60–75 minut
> **Potrzebujesz:** katalogu `cpp-workspace` i oryginalnego projektu `lesson_05_first_program`, jak dotąd. Debugger nie jest w tej lekcji potrzebny.
> **Wersja pilotażowa.** Programy z tej lekcji sprawdzamy automatycznie na Windowsie, Ubuntu i macOS. Żaden z nich nie pyta o dane: wszystkie wartości są zapisane w kodzie. Dane z wejścia odczytuje tylko program kontrolny w części z rozwiązaniami.

## Zanim zaczniesz

Ta lekcja zakłada, że:

- deklarujesz zmienne typów `int`, `bool` i `std::string`, inicjalizujesz je przez `{}` i oznaczasz `const`, gdy się nie zmieniają (lekcje 2.1, 2.2, 2.7 i 3.2);
- obliczasz wyniki z kilku wartości i podejmujesz decyzje przez `if` i `else` (Moduły 2 i 3);
- wiesz, że kropka po nazwie obiektu odwołuje się do czegoś, co do niego należy, jak w `std::cin.fail()` (lekcja 4.5) albo `text.size()` (lekcja 7.1).

## Sytuacja

Program przechowuje informacje o książce:

<!-- fragment -->
```cpp
const std::string title{"C++ Basics"};
const int pages{180};
const bool finished{false};
```

To trzy różne informacje: tytuł, liczba stron i to, czy książka jest już przeczytana. Wszystkie opisują jedną książkę, ale w kodzie nic tego nie mówi: to trzy osobne zmienne.

- Skąd wiadomo, że te wartości należą do tej samej książki? Tylko z nazw i z tego, że stoją obok siebie.
- Co się stanie, gdy pojawi się druga książka? Potrzebne będą trzy kolejne zmienne, na przykład `second_title`, `second_pages` i `second_finished`.
- Jak nie pomylić tytułu jednej książki z liczbą stron drugiej? Trzeba pilnować każdej nazwy.
- Czy taki zestaw danych da się nazwać jednym typem, tak jak `int` albo `std::string`?

To poprawny C++, a w małym programie trzy zmienne wystarczą. Kłopot rośnie razem z liczbą obiektów: każda nowa książka to kolejne trzy nazwy, które łączy tylko Twoja uwaga. W tej lekcji zdefiniujesz **własny typ**, który zbiera dane jednej książki w jednym miejscu.

Po tej lekcji będziesz:

- wyjaśniać, jaki problem rozwiązuje `struct`;
- definiować prostą strukturę z polami różnych typów;
- odróżniać definicję typu od utworzenia obiektu;
- tworzyć obiekt i podawać wartości jego pól w `{}`, w kolejności pól;
- odczytywać pola przez operator `.` i używać ich w obliczeniach i warunkach;
- tworzyć kilka obiektów jednego typu, każdy z własnymi wartościami pól;
- rozpoznawać błąd pomylonych wartości pól.

## 1. Przygotuj projekt

W `cpp-workspace` utwórz katalog `lesson_8_1` i skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program`. Programy z punktów 3, 5, 7 i 8 wpisujesz w `main.cpp` tego katalogu.

## 2. Własny typ: `struct`

<!-- fragment -->
```cpp
struct Book {
    std::string title;
    int pages;
    bool finished;
};
```

| Zapis | Znaczenie |
|---|---|
| `struct` | Słowo kluczowe, które zaczyna definicję własnego typu. |
| `Book` | Nazwa nowego typu. Odtąd `Book` jest typem, tak jak `int` albo `std::string`. |
| `{ }` | Klamry obejmują definicję typu. |
| `std::string title;` | **Pole**: nazwana część każdej książki. Pole ma typ i nazwę, jak deklaracja zmiennej. |
| `int pages;`, `bool finished;` | Dwa kolejne pola, innych typów. |
| `;` po `}` | Kończy definicję całego typu. Jest potrzebny niezależnie od średników po polach. |

- **Definicja typu nie tworzy jeszcze żadnej książki.** Opisuje tylko, z czego składa się każda książka: z tytułu, liczby stron i informacji o przeczytaniu. Przypomina formularz z rubrykami, którego nikt jeszcze nie wypełnił. Dlatego pola nie mają tu wartości: dostanie je każda książka osobno.
- **Gdzie stoi definicja:** poza `main` i przed miejscem, w którym korzystasz z typu, jak definicja funkcji w lekcji 5.1. Definicja typu nie jest zmienną i nie przechowuje żadnych wartości, więc zasada „bez zmiennych zadeklarowanych poza funkcjami” jej nie dotyczy.
- **Nazwy:** nazwę własnego typu zapisujemy w kursie od wielkiej litery (`Book`), a nazwy pól, jak nazwy zmiennych, w `snake_case` (`title`, `unit_price`). Dzięki temu typ `Book` łatwo odróżnić od obiektu `book`.

C++ ma też słowo `class`, którym również definiuje się własne typy. W tej części kursu korzystamy tylko ze `struct`.

## 3. Pierwszy obiekt

<!-- example: first_book -->
```cpp
#include <iostream>
#include <string>

struct Book {
    std::string title;
    int pages;
    bool finished;
};

int main() {
    const Book book{"C++ Basics", 180, false};

    std::cout << "Title: " << book.title << "\n";
    std::cout << "Pages: " << book.pages << "\n";

    if (book.finished) {
        std::cout << "Finished: yes\n";
    } else {
        std::cout << "Finished: no\n";
    }
}
```

**Przewidź** wszystkie trzy linijki wyniku, a potem uruchom program.

<details>
<summary>Standardowe wyjście</summary>

<!-- output: first_book -->
```text
Title: C++ Basics
Pages: 180
Finished: no
```

</details>

Linijka `const Book book{"C++ Basics", 180, false};` **tworzy obiekt**, czyli jedną konkretną książkę:

- `Book` to typ, a `book` to nazwa obiektu, tak jak w `const int pages{180};` typem jest `int`, a nazwą `pages`;
- wartości w `{}` trafiają do kolejnych pól, **w tej samej kolejności, w jakiej pola stoją w definicji typu**:

| Pole | Typ | Wartość |
|---|---|---|
| `title` | `std::string` | `"C++ Basics"` |
| `pages` | `int` | `180` |
| `finished` | `bool` | `false` |

- `const`, bo program nie zmienia tej książki, jak każdej innej zmiennej, której nie zmieniamy (lekcja 2.2).
- W tej lekcji zawsze podajemy wartości **wszystkich** pól, po jednej na pole. Kompilator sprawdza ich typy: tekst nie trafi do pola `int`. Nie odróżni jednak dwóch wartości tego samego typu, gdy zamienisz ich kolejność (punkt 8).

## 4. Operator kropki

`book.title` czytaj „pole `title` obiektu `book`”. Kropkę znasz z `std::cin.fail()` i `text.size()`: tam po kropce stała funkcja należąca do obiektu, a tutaj stoi pole, czyli wartość zapisana w obiekcie.

| Wyrażenie | Typ | Wartość |
|---|---|---|
| `book.title` | `std::string` | `C++ Basics` |
| `book.pages` | `int` | `180` |
| `book.finished` | `bool` | `false` |

Pola obiektu używasz tak jak zwykłej zmiennej jego typu: `book.pages` możesz wypisać, dodać do innej liczby albo porównać, a `book.finished` postawić w warunku `if`. Dlatego program z punktu 3 wypisuje `yes` albo `no` przez `if`, zamiast wypisywać wartość `bool` jako `1` albo `0`.

## 5. Dwa obiekty tego samego typu

<!-- example: two_books -->
```cpp
#include <iostream>
#include <string>

struct Book {
    std::string title;
    int pages;
    bool finished;
};

int main() {
    const Book first{"C++ Basics", 180, false};
    const Book second{"Algorithms", 240, true};

    std::cout << first.title << ": " << first.pages << " pages\n";
    std::cout << second.title << ": " << second.pages << " pages\n";

    int pages_to_read{0};

    if (!first.finished) {
        pages_to_read += first.pages;
    }

    if (!second.finished) {
        pages_to_read += second.pages;
    }

    std::cout << "Pages to read: " << pages_to_read << "\n";
}
```

**Przewidź** wynik. Ile stron zostało do przeczytania?

<details>
<summary>Standardowe wyjście</summary>

<!-- output: two_books -->
```text
C++ Basics: 180 pages
Algorithms: 240 pages
Pages to read: 180
```

</details>

- **Oba obiekty mają typ `Book`**, więc mają te same pola: `title`, `pages` i `finished`.
- **Wartości pól są różne:** każdy obiekt przechowuje własne. `second` nie jest kopią `first`, tylko drugą, osobno utworzoną książką.
- **Nazwa przed kropką wybiera obiekt.** `first.pages` to liczba stron pierwszej książki, a `second.pages` drugiej.
- Do sumy trafiają tylko strony książki, której własne pole `finished` daje `false` (`!` z lekcji 3.4, `+=` z lekcji 4.2). Każdy warunek sprawdza pole tego samego obiektu, z którego program bierze strony.

**Zmień:** w klamrach obiektu `second` zamień `true` na `false` i przewidź nowy wynik, zanim uruchomisz program. Zmieniasz dane tylko drugiej książki: pierwsza zostaje taka sama.

## 6. Typ, obiekt i pole

| Zapis | Co to jest | Przykład |
|---|---|---|
| `Book` | własny typ | `struct Book { ... };` |
| `first`, `second` | obiekty typu `Book`: konkretne książki | `const Book first{"C++ Basics", 180, false};` |
| `pages` | nazwa pola zadeklarowanego w typie | `int pages;` |
| `first.pages` | pole konkretnego obiektu | `180` |

Samo `pages`, bez obiektu, nic nie znaczy: każda książka ma własne `pages`, więc zawsze trzeba wskazać, której książki dotyczy. Konkretny obiekt danego typu bywa też nazywany **instancją** tego typu. W tym kursie mówimy po prostu „obiekt”.

## 7. Znajdź błąd: brakujący średnik

Ten program różni się od programu z punktu 3 jednym znakiem. **Przewidź**, czy się zbuduje, a potem spróbuj go zbudować i przeczytaj pierwszy komunikat kompilatora. Znajdź brakujący znak i popraw program.

<!-- broken: first_book_no_semicolon at=8:2 errors=1 error=^expected ';' after struct -->
```cpp
#include <iostream>
#include <string>

struct Book {
    std::string title;
    int pages;
    bool finished;
}

int main() {
    const Book book{"C++ Basics", 180, false};

    std::cout << "Title: " << book.title << "\n";
    std::cout << "Pages: " << book.pages << "\n";

    if (book.finished) {
        std::cout << "Finished: yes\n";
    } else {
        std::cout << "Finished: no\n";
    }
}
```

<details>
<summary>Co zgłasza kompilator i dlaczego</summary>

Program się nie zbuduje. Kompilator zgłasza w linijce 8 `expected ';' after struct`: po zamykającej klamrze definicji `Book` brakuje średnika.

- Średniki **po polach** kończą deklaracje kolejnych pól, jak deklaracje zmiennych.
- Średnik **po `}`** kończy definicję całego typu. Bez niego kompilator nie wie, że definicja się skończyła.

**Poprawka:** dopisz `;` po `}`. Poprawiony program to program z punktu 3.

</details>

## 8. Znajdź błąd: zamienione wartości

To zadanie wykonaj **przed misją**. Program opisuje salę: jej nazwę, liczbę miejsc i liczbę zapisanych osób. Liczby wyznaczono wcześniej w dwóch zmiennych, a obiekt sali utworzono z ich wartości. Program możesz przepisać albo skopiować do `main.cpp`.

<!-- example: room_order_bug -->
```cpp
#include <iostream>
#include <string>

struct Room {
    std::string name;
    int seats;
    int people;
};

int main() {
    const int available_seats{30};
    const int registered_people{30};

    const Room room{"Lab", registered_people, available_seats};

    std::cout << "Room: " << room.name << "\n";
    std::cout << "Seats: " << room.seats << "\n";
    std::cout << "People: " << room.people << "\n";

    if (room.people >= room.seats) {
        std::cout << "Full: yes\n";
    } else {
        std::cout << "Full: no\n";
    }
}
```

1. Wypisz pola struktury `Room` w kolejności z definicji.
2. Przypisz każdą wartość z `{"Lab", registered_people, available_seats}` do pola, które ją dostaje.
3. **Przewidź** standardowe wyjście, a potem uruchom program. Czy wynik wygląda poprawnie?
4. Dlaczego kompilator nie zgłasza żadnego błędu?
5. Zmień wartości `available_seats` i `registered_people` tak, żeby pomyłka stała się widoczna w wyniku. Najpierw zapisz, jaki wynik byłby poprawny dla Twoich danych, a potem uruchom program.
6. Popraw kolejność wartości przy tworzeniu obiektu.
7. Uruchom poprawiony program dla swoich danych i dla 30 i 30.

Wyniki, przykładowe dane i poprawiony program są w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 9. Misja: karta produktu w magazynie

Program przygotowuje kartę jednego produktu w magazynie. Produkt ma:

- nazwę;
- liczbę sztuk w magazynie, czyli stan;
- minimalną wymaganą liczbę sztuk;
- cenę jednej sztuki.

**Dane produktu:** nazwa `Tea`, stan 3 sztuki, minimum 8 sztuk, cena jednej sztuki 6. Wszystkie liczby są małe, nieujemne i całkowite.

**Wymagania:**

- Program definiuje **własną strukturę**, której jeden obiekt przechowuje wszystkie cztery dane produktu. Nazwę typu, nazwy pól i ich typy wybierasz samodzielnie.
- Tworzy jeden obiekt tej struktury, z wartościami w `{}`, i wszystkie liczby raportu oblicza z pól tego obiektu. Nie przepisuje danych produktu do osobnych zmiennych.
- Wypisuje dokładnie sześć linijek: `Product: NAZWA`, `Stock: N`, `Minimum: N`, `Unit price: N`, `Stock value: N` i `To add: N`.
- **Wartość zapasu** to stan razy cena jednej sztuki.
- **Liczba sztuk do dodania:** gdy stan jest mniejszy od minimum, to różnica między minimum a stanem, a w przeciwnym razie 0. Program nigdy nie wypisuje liczby ujemnej.
- Program nie odczytuje niczego z wejścia i nie potrzebuje własnych funkcji.

W `cpp-workspace` utwórz katalog `product_card`, skopiuj do niego `CMakeLists.txt` z oryginalnego `lesson_05_first_program`, utwórz pusty `main.cpp` i napisz program samodzielnie.

Dla danych powyżej standardowe wyjście ma być takie:

<!-- output: product_card -->
```text
Product: Tea
Stock: 3
Minimum: 8
Unit price: 6
Stock value: 18
To add: 5
```

Stan 3 razy cena 6 daje wartość zapasu 18. Do minimum 8 brakuje 5 sztuk.

**To nie jest program o książkach z innymi nazwami.** Musisz samodzielnie zdecydować:

1. jak nazwać typ i jego cztery pola;
2. jaki typ ma każde pole;
3. w jakiej kolejności zapisać pola i jak podać wartości obiektu w tej samej kolejności;
4. których pól potrzebujesz do wartości zapasu, a których do sprawdzenia minimum;
5. jak sprawić, żeby liczba sztuk do dodania nigdy nie była ujemna;
6. jak zbudować cały raport z jednego obiektu.

**Zanim napiszesz program**, przygotuj tabelę przypadków: stan mniejszy od minimum, równy minimum i większy od minimum, zerowy stan i zerowa cena. Przy każdym zapisz oczekiwaną wartość zapasu i liczbę sztuk do dodania.

**Potem** uruchom program dla danych z wymagań i dla dwóch innych przypadków z tabeli, na przykład stanu równego minimum i zerowego stanu. Zmieniaj przy tym tylko wartości w klamrach obiektu. Wszystkie przypadki z pełnej listy kontrolnej są sprawdzone automatycznie.

### Kryterium sukcesu

- Program buduje się jako C++20 i dla danych z wymagań wypisuje dokładnie sześć linijek pokazanych wyżej.
- Jest jedna struktura z czterema polami i jeden obiekt tej struktury, utworzony z wartościami w `{}`.
- Wszystkie linijki raportu korzystają z pól tego obiektu, a w `main` nie ma osobnych zmiennych powtarzających dane produktu.
- Liczba sztuk do dodania nigdy nie jest ujemna, a gdy stan jest równy minimum albo większy, wynosi 0.
- Tabela przypadków powstała przed uruchomieniem programu.
- Umiesz wyjaśnić, w jakiej kolejności Twoje wartości w `{}` trafiają do pól.

Gdy wynik się zgadza, możesz zapisać projekt w Gicie, jak w lekcji 1.5.

<details>
<summary>Podpowiedź 1</summary>

Które cztery informacje opisują jeden produkt? Czy można zamknąć je w jednym własnym typie?

</details>

<details>
<summary>Podpowiedź 2</summary>

Zdefiniuj pola struktury, utwórz obiekt i korzystaj z jego pól przez operator kropki.

</details>

<details>
<summary>Podpowiedź 3</summary>

Wartość zapasu zależy od stanu i ceny. Liczba sztuk do dodania zależy od stanu i minimum, ale nie może być ujemna.

</details>

<details>
<summary>Pełna lista przypadków kontrolnych: otwórz po przygotowaniu własnej tabeli</summary>

| | Produkt | Stan | Minimum | Cena | Wartość zapasu | Do dodania | Co sprawdza |
|---|---|---:|---:|---:|---:|---:|---|
| A | `Tea` | 3 | 8 | 6 | 18 | 5 | dane z wymagań: stan mniejszy od minimum |
| B | `Rice` | 8 | 8 | 4 | 32 | 0 | stan równy minimum |
| C | `Pens` | 10 | 7 | 2 | 20 | 0 | stan większy od minimum: bez liczby ujemnej |
| D | `Box` | 0 | 5 | 3 | 0 | 5 | zerowy stan |
| E | `Glue` | 1 | 1 | 0 | 0 | 0 | zerowa cena i stan równy minimum |
| F | `Paper` | 2 | 5 | 1 | 2 | 3 | cena 1: wartość równa stanowi |

**Testy automatyczne i Twoje próby.** Wszystkie przypadki są sprawdzone automatycznie przez program kontrolny. Ma on tę samą strukturę i ten sam raport co rozwiązanie referencyjne, ale dane produktu odczytuje z wejścia, po jednej wartości w linijce. To tylko narzędzie do sprawdzania, a nie część misji: w misji dane są wpisane w kodzie. Program kontrolny i jego wyniki są w części [Przykładowe rozwiązania](#przykładowe-rozwiązania), bo zawierają rozwiązanie.

</details>

Przykładowe rozwiązanie jest w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 10. Gdy coś pójdzie inaczej

| Co widzisz | Co to znaczy | Co zrobić |
|---|---|---|
| `expected ';' after struct` | Po zamykającej klamrze definicji brakuje średnika (punkt 7). | Dopisz `;` po `}`. |
| `excess elements in struct initializer` | W `{}` jest więcej wartości niż pól. | Podaj jedną wartość dla każdego pola. |
| Komunikat z `no viable conversion` albo `cannot initialize a member subobject` przy tworzeniu obiektu | Wartość ma inny typ niż pole, do którego trafia, na przykład liczba stoi na miejscu tekstu. | Ustaw wartości w kolejności pól z definicji. |
| `use of undeclared identifier` z nazwą pola, na przykład `title` | Pole jest użyte bez obiektu. | Wskaż obiekt: `book.title`. |
| `'Book' does not refer to a value` | Przed kropką stoi nazwa typu, a nie obiektu. | Przed kropką wpisz nazwę obiektu, na przykład `book`. |
| Program się buduje, ale wartości dwóch pól liczbowych są zamienione | Wartości w `{}` stoją w innej kolejności niż pola (punkt 8). | Porównaj kolejność wartości z kolejnością pól w definicji. |
| Pole liczbowe ma wartość 0, a pole `bool` wartość `false`, choć ich nie podano | W `{}` jest mniej wartości niż pól. Pola bez wartości dostają 0, `false` albo pusty tekst. | Podaj wartość każdego pola. |
| Program wypisuje `1` albo `0` zamiast `yes` albo `no` | Pole `bool` jest wypisane bezpośrednio. | Wybierz tekst przez `if`, jak w punkcie 3. |

## 11. Wyjaśnij

Odpowiedz własnymi słowami, najlepiej na piśmie. Dopiero potem porównaj z przykładowymi odpowiedziami.

1. Jaki problem rozwiązuje `struct`?
2. Czy definicja `struct Book` tworzy już jakąś książkę?
3. Czym różnią się `Book`, `book` i `book.pages`?
4. Dlaczego po zamykającej klamrze struktury potrzebny jest średnik, skoro średniki stoją już po polach?
5. Jak wartości w `{}` trafiają do pól obiektu?
6. Co robi operator `.` i jakiego typu jest `book.finished`?
7. Czy dwa obiekty typu `Book` mogą mieć różne wartości pól? Skąd program wie, której książki dotyczy `first.pages`?
8. Dlaczego kompilator nie wykrył zamienionych wartości w programie o sali z punktu 8?
9. Dlaczego obiekt produktu w misji może być `const`?
10. Czy struktura z tej lekcji potrzebuje konstruktorów albo metod?

<details>
<summary>Przykładowe odpowiedzi</summary>

1. Łączy kilka informacji, które opisują jeden obiekt, na przykład tytuł, liczbę stron i stan przeczytania jednej książki. Zamiast osobnych zmiennych, które łączy tylko podobieństwo nazw, program ma jeden obiekt z nazwanymi polami.
2. Nie. Definicja opisuje tylko, z jakich pól składa się każda książka. Książka powstaje dopiero wtedy, gdy tworzysz obiekt, na przykład `const Book book{"C++ Basics", 180, false};`.
3. `Book` to typ, `book` to konkretny obiekt tego typu, a `book.pages` to pole `pages` tego obiektu, czyli liczba stron tej książki.
4. Średniki po polach kończą deklaracje pól, a średnik po `}` kończy definicję całego typu. To dwa różne miejsca, więc potrzebne są oba.
5. Po kolei: pierwsza wartość trafia do pierwszego pola z definicji, druga do drugiego i tak dalej. Dlatego kolejność wartości musi odpowiadać kolejności pól.
6. Wybiera pole konkretnego obiektu. `book.finished` ma typ pola z definicji, czyli `bool`.
7. Tak. Każdy obiekt przechowuje własne wartości pól. Nazwa przed kropką wskazuje obiekt: `first.pages` to strony pierwszej książki, a `second.pages` drugiej.
8. Bo oba pola, `seats` i `people`, mają typ `int`, a obie zmienne też są typu `int`. Kompilator sprawdza typy, a nie znaczenie wartości, więc liczba osób może trafić do pola miejsc bez błędu. To błąd logiczny, nie błąd kompilacji.
9. Bo program tylko odczytuje dane produktu i z nich liczy. Żadne pole obiektu się nie zmienia.
10. Nie. Obiekt tworzymy, podając w `{}` wartości wszystkich pól, a pola odczytujemy przez kropkę. Konstruktory i metody nie są tu potrzebne.

</details>

## Podsumowanie

- **`struct`** definiuje własny typ: nazwaną grupę pól, z których każde ma typ i nazwę. Po zamykającej klamrze definicji stoi średnik.
- Definicja typu nie tworzy obiektu. Obiekt tworzysz jak zmienną: typ, nazwa i wartości w `{}`, na przykład `const Book book{"C++ Basics", 180, false};`.
- Wartości w `{}` trafiają do pól w kolejności ich deklaracji. Kompilator pilnuje typów, ale nie odróżni zamienionych wartości tego samego typu.
- Operator `.` wybiera pole konkretnego obiektu: `book.pages` to liczba stron książki `book`. Pola używasz jak zwykłej zmiennej jego typu, w obliczeniach i warunkach.
- Kilka obiektów jednego typu ma te same pola, ale każdy przechowuje własne wartości.
- Struktura łączy dane, które należą do jednego obiektu, a nie tylko skraca kod.

## Co dalej

W tej lekcji każdy obiekt dostawał wartości raz, przy utworzeniu, i potem się nie zmieniał. W kolejnej części Modułu 8 zobaczysz, jak obiekt może się zmieniać i czym jest jego kopia. Jest w przygotowaniu.

---

## Przykładowe rozwiązania

Zajrzyj tutaj **po własnej próbie**. Twoje nazwy mogą się różnić, jeśli standardowe wyjście jest takie, jak wymagane.

<details>
<summary>Punkt 9: misja, karta produktu</summary>

<!-- example: product_card -->
```cpp
#include <iostream>
#include <string>

struct Product {
    std::string name;
    int stock;
    int minimum;
    int unit_price;
};

int main() {
    const Product product{"Tea", 3, 8, 6};

    int to_add{0};

    if (product.stock < product.minimum) {
        to_add = product.minimum - product.stock;
    }

    std::cout << "Product: " << product.name << "\n";
    std::cout << "Stock: " << product.stock << "\n";
    std::cout << "Minimum: " << product.minimum << "\n";
    std::cout << "Unit price: " << product.unit_price << "\n";
    std::cout << "Stock value: " << product.stock * product.unit_price << "\n";
    std::cout << "To add: " << to_add << "\n";
}
```

1. **Nowy typ**, bo cztery dane opisują jeden produkt. Struktura `Product` zapisuje ten związek w kodzie: każdy produkt ma nazwę, stan, minimum i cenę.
2. **Pola i obiekt:** `name`, `stock`, `minimum` i `unit_price` to pola zadeklarowane w typie `Product`. `product` to obiekt, czyli konkretny produkt z wartościami tych pól.
3. **Kolejność:** `{"Tea", 3, 8, 6}` podaje wartości w kolejności pól z definicji: nazwa, stan, minimum, cena.
4. **Zamiana bez błędu:** stan, minimum i cena mają typ `int`. Gdyby w `{}` zamienić miejscami 3 i 8, program zbudowałby się bez błędu, ale stan wynosiłby 8, a minimum 3. Kompilator sprawdza typy, a nie znaczenie liczb.
5. **Kropka** wybiera pole tego jednego obiektu: `product.stock` to stan, a `product.minimum` minimum.
6. **Jeden obiekt:** wszystkie linijki raportu biorą dane z `product`, więc nie da się wziąć stanu jednego produktu, a ceny innego. `to_add` to wynik obliczenia, a nie kopia danych produktu.
7. **`const`:** program tylko odczytuje pola produktu, więc obiekt może być stały, jak każda zmienna, której nie zmieniamy.
8. **Drugi produkt** to drugi obiekt tego samego typu z własnymi wartościami, na przykład `const Product rice{"Rice", 8, 8, 4};`. Pola `rice.stock` i `product.stock` są od siebie niezależne.

**Liczba sztuk do dodania** startuje od 0 i zmienia się tylko wtedy, gdy stan jest mniejszy od minimum. Dlatego dla stanu równego minimum albo większego wynik to 0, a różnica nigdy nie jest ujemna. Ten sam warunek można też zapisać jako `if` i `else`, z osobną linijką `To add` w każdej gałęzi. Pola mogą mieć inne nazwy i inną kolejność, jeśli wartości w `{}` stoją w tej samej kolejności co pola.

**Program kontrolny** sprawdza wszystkie przypadki z listy kontrolnej. Struktura i raport są takie same jak wyżej, poza wcięciem. Różnica jest jedna: dane produktu są odczytywane z wejścia do czterech zwykłych zmiennych, a obiekt powstaje z ich wartości.

<!-- example: product_card_check -->
```cpp
#include <iostream>
#include <string>

struct Product {
    std::string name;
    int stock;
    int minimum;
    int unit_price;
};

int main() {
    std::string name{};
    int stock{0};
    int minimum{0};
    int unit_price{0};

    std::cin >> name;
    std::cin >> stock;
    std::cin >> minimum;
    std::cin >> unit_price;

    if (std::cin.fail()) {
        std::cout << "Input could not be read\n";
    } else {
        const Product product{name, stock, minimum, unit_price};

        int to_add{0};

        if (product.stock < product.minimum) {
            to_add = product.minimum - product.stock;
        }

        std::cout << "Product: " << product.name << "\n";
        std::cout << "Stock: " << product.stock << "\n";
        std::cout << "Minimum: " << product.minimum << "\n";
        std::cout << "Unit price: " << product.unit_price << "\n";
        std::cout << "Stock value: " << product.stock * product.unit_price << "\n";
        std::cout << "To add: " << to_add << "\n";
    }
}
```

Każdy przypadek to cztery linijki wejścia: nazwa, stan, minimum i cena, w kolejności z listy kontrolnej, od A do F.

<!-- input: product_card_check -->
```text
Tea
3
8
6
```

<!-- output: product_card_check -->
```text
Product: Tea
Stock: 3
Minimum: 8
Unit price: 6
Stock value: 18
To add: 5
```

<!-- input: product_card_check -->
```text
Rice
8
8
4
```

<!-- output: product_card_check -->
```text
Product: Rice
Stock: 8
Minimum: 8
Unit price: 4
Stock value: 32
To add: 0
```

<!-- input: product_card_check -->
```text
Pens
10
7
2
```

<!-- output: product_card_check -->
```text
Product: Pens
Stock: 10
Minimum: 7
Unit price: 2
Stock value: 20
To add: 0
```

<!-- input: product_card_check -->
```text
Box
0
5
3
```

<!-- output: product_card_check -->
```text
Product: Box
Stock: 0
Minimum: 5
Unit price: 3
Stock value: 0
To add: 5
```

<!-- input: product_card_check -->
```text
Glue
1
1
0
```

<!-- output: product_card_check -->
```text
Product: Glue
Stock: 1
Minimum: 1
Unit price: 0
Stock value: 0
To add: 0
```

<!-- input: product_card_check -->
```text
Paper
2
5
1
```

<!-- output: product_card_check -->
```text
Product: Paper
Stock: 2
Minimum: 5
Unit price: 1
Stock value: 2
To add: 3
```

</details>

<details>
<summary>Punkt 8: wyniki przed poprawką i poprawiony program</summary>

Przed poprawką, dla 30 miejsc i 30 osób:

<!-- output: room_order_bug -->
```text
Room: Lab
Seats: 30
People: 30
Full: yes
```

| Pole z definicji | Wartość w `{}` | Co pole dostaje |
|---|---|---|
| `name` | `"Lab"` | nazwę sali |
| `seats` | `registered_people` | liczbę **osób**, a nie miejsc |
| `people` | `available_seats` | liczbę **miejsc**, a nie osób |

- **Wynik wygląda poprawnie,** bo obie liczby wynoszą 30: zamiana jednakowych wartości niczego nie zmienia.
- **Kompilator nie zgłasza błędu,** bo oba pola i obie zmienne mają typ `int`. Typy się zgadzają, a znaczenia wartości kompilator nie zna.
- **Dane, które ujawniają błąd:** dowolne dwie różne liczby. Na przykład 30 miejsc i 24 osoby, czyli `available_seats{30}` i `registered_people{24}`. Poprawny wynik to 30 miejsc, 24 osoby i `Full: no`. Program z błędem wypisuje:

<!-- example: room_order_revealed -->
```cpp
#include <iostream>
#include <string>

struct Room {
    std::string name;
    int seats;
    int people;
};

int main() {
    const int available_seats{30};
    const int registered_people{24};

    const Room room{"Lab", registered_people, available_seats};

    std::cout << "Room: " << room.name << "\n";
    std::cout << "Seats: " << room.seats << "\n";
    std::cout << "People: " << room.people << "\n";

    if (room.people >= room.seats) {
        std::cout << "Full: yes\n";
    } else {
        std::cout << "Full: no\n";
    }
}
```

<!-- output: room_order_revealed -->
```text
Room: Lab
Seats: 24
People: 30
Full: yes
```

Liczby miejsc i osób są zamienione, a do tego zmienia się decyzja: sala z sześcioma wolnymi miejscami wygląda na pełną.

**Poprawka:** wartości w `{}` w kolejności pól: najpierw liczba miejsc, potem liczba osób.

<!-- example: room_order_fixed -->
```cpp
#include <iostream>
#include <string>

struct Room {
    std::string name;
    int seats;
    int people;
};

int main() {
    const int available_seats{30};
    const int registered_people{24};

    const Room room{"Lab", available_seats, registered_people};

    std::cout << "Room: " << room.name << "\n";
    std::cout << "Seats: " << room.seats << "\n";
    std::cout << "People: " << room.people << "\n";

    if (room.people >= room.seats) {
        std::cout << "Full: yes\n";
    } else {
        std::cout << "Full: no\n";
    }
}
```

<!-- output: room_order_fixed -->
```text
Room: Lab
Seats: 30
People: 24
Full: no
```

Dla 30 i 30 poprawiony program wypisuje to samo co przed poprawką: przy jednakowych wartościach obie kolejności dają ten sam wynik. Dlatego dane z dwiema takimi samymi liczbami nie wystarczą, żeby sprawdzić kolejność pól.

</details>

**Poprzednia lekcja:** [Lekcja 7.5: Kontrola kodów paczek (sprawdzian Modułu 7)](../module_07_text/lesson_05_parcel_code_check.md) · **Następna lekcja:** w przygotowaniu · [Opis kursu](../../README.md)

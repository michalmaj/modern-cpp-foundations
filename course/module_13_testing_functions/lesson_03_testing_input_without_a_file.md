# Lekcja 13.3: Testowanie odczytu bez pliku

**Polski** · [English](lesson_03_testing_input_without_a_file.en.md) · [Opis kursu](../../README.md)

> **Moduł 13, lekcja 3** · około 85–105 minut, można ją podzielić na dwa podejścia
> **Potrzebujesz:** katalogu `cpp-workspace` i oryginalnego projektu `lesson_05_first_program`, jak dotąd. Przyda się też rozwiązanie misji z lekcji 12.3 z funkcją `read_chores`.
> **Wersja pilotażowa.** Programy z tej lekcji sprawdzamy automatycznie na Windowsie, Ubuntu i macOS, razem z ich kodem zakończenia. Nie potrzebują plików danych, pola **Working directory** ani wpisywania danych.

## Zanim zaczniesz

Ta lekcja zakłada, że:

- piszesz program testowy z lekcji 13.1 i 13.2: wynik oczekiwany z kontraktu, `PASS` albo `FAIL`, licznik niepowodzeń, kod zakończenia 0 albo 1, funkcje `check_bool` i `bool_text`;
- znasz funkcję `read_shipment_values` z lekcji 10.4: odczytuje liczbę paczek ze strumienia `std::istream&` i wypełnia rekord wynikowy tylko po sukcesie, a w lekcji 12.2 ta sama funkcja czytała z pliku;
- znasz funkcję `read_chores` z misji lekcji 12.3 i tabelę z punktu 2 tamtej lekcji, w której `\n` oznaczał znak końca linii w pliku;
- pamiętasz z lekcji 4.6, że po nieudanym odczycie `fail()` daje `true`, a `clear()` nie tworzy nowych danych;
- przechowujesz rozmiar wektora w typie `std::size_t` i nie mieszasz go z `int` (lekcja 6.3);
- zapisujesz cudzysłów wewnątrz tekstu jako `\"` (lekcja 1.6).

## Sytuacja

Funkcja `read_shipment_values` była dotąd sprawdzana na dwa sposoby: z danymi wpisywanymi z klawiatury (lekcja 10.4) i z plikiem `shipments.txt` (lekcja 12.2). Oba są dobre, gdy program jest używany. Przy testowaniu mają jednak koszt: dane trzeba za każdym razem wpisać albo przygotować plik, który musi leżeć w katalogu roboczym, łatwo przypadkowo sprawdzić inną zawartość pliku niż ta, o którą chodziło, a kilkanaście wariantów danych to kilkanaście plików albo kilkanaście wpisywań.

Program testowy z lekcji 13.1 sam porównuje wyniki. Brakuje mu tylko źródła danych, które nie wymaga ani klawiatury, ani pliku. **Tym źródłem będzie tekst zapisany w samym programie testowym.**

Po tej lekcji będziesz:

- tworzyć strumień wejścia z tekstu przez `std::istringstream` i przekazywać go funkcji z parametrem `std::istream&`;
- testować funkcję odczytu bez pliku i bez wpisywania danych;
- sprawdzać w jednym przypadku kilka skutków jednego wywołania: wynik `bool`, rekord wynikowy i stan strumienia;
- sprawdzać zawartość i kolejność wektora, rodzaj błędu i numer fizycznej linii;
- dawać każdemu niezależnemu przypadkowi nowy strumień i własne zmienne wynikowe.

## 1. Trzy źródła danych, jedna funkcja

| Źródło | Obiekt | Skąd pochodzą znaki |
|---|---|---|
| klawiatura, czyli standardowe wejście | `std::cin` | ze standardowego wejścia programu |
| plik tekstowy | `std::ifstream` | z otwartego pliku |
| tekst w pamięci | `std::istringstream` | z tekstu podanego przy tworzeniu strumienia |

We wszystkich trzech przypadkach funkcja może przyjmować ten sam parametr `std::istream&`. Funkcja z takim parametrem nie wie, skąd pochodzą znaki (lekcja 12.2), więc **tę samą, niezmienioną funkcję można przetestować tekstem zapisanym w kodzie.**

`std::istringstream` nie zastępuje `std::ifstream` w programie, który ma czytać plik. Program dziennika zadań z lekcji 12.3 nadal czyta `chores.txt`. Tekst w pamięci to trzecie źródło danych, szczególnie wygodne w testach: dane są w kodzie testu, obok wyniku oczekiwanego.

## 2. Strumień z tekstu: `std::istringstream`

<!-- example: memory_stream -->
```cpp
#include <iostream>
#include <sstream>

int main() {
    std::istringstream input{"4\n"};
    int boxes{0};
    input >> boxes;

    if (input.fail()) {
        std::cout << "Input error\n";
        return 0;
    }

    std::cout << "Boxes: " << boxes << "\n";
}
```

Program wypisuje:

<!-- output: memory_stream -->
```text
Boxes: 4
```

| Zapis | Co robi |
|---|---|
| `#include <sstream>` | udostępnia `std::istringstream` |
| `std::istringstream input{"4\n"};` | tworzy strumień wejścia, którego danymi są znaki `4` i znak końca linii |
| `input >> boxes;` | odczytuje liczbę, tak jak z `std::cin` |
| `input.fail()` | mówi, czy odczyt się nie udał, tak jak w lekcji 4.5 |

- **Nazwa:** *i* od *input* (wejście), *string* (tekst), *stream* (strumień), czyli strumień wejścia z tekstu.
- **Nie powstaje żaden plik.** Nie ma pliku danych, nie trzeba ustawiać **Working directory**, a program nie czeka na klawiaturę.
- **Tekst w cudzysłowie to dokładnie dane.** `\n` to ten sam znak końca linii, który w tabeli z lekcji 12.3 oznaczał koniec linii pliku. `""` to pusty plik, `"\n"` to jedna pusta linia, a `"Clean tables\ndone"` to dwie linie bez znaku końca linii po ostatniej. Część takich danych trudno wpisać z klawiatury, a w edytorze łatwo je zmienić niechcący, na przykład dopisując znak końca linii.
- **Odczytane znaki znikają ze strumienia,** tak jak przy `std::cin`. Po `input >> boxes` zostaje w nim tylko znak końca linii. Strumień nie wraca sam do początku tekstu (punkt 9).

W `cpp-workspace` utwórz katalog `lesson_13_3`, skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program` i otwórz go w CLionie. Ten krótki program możesz uruchomić od razu w `main.cpp`. To uruchomienie jest nieobowiązkowe. Kolejne programy z tej lekcji wpisujesz w ten sam `main.cpp`, a `CMakeLists.txt` zostawiasz bez zmian.

**Dlaczego taki strumień można przekazać funkcji z `std::istream&`?** Biblioteka standardowa określa `std::istringstream`, tak samo jak `std::ifstream` z lekcji 12.2, jako szczególny rodzaj `std::istream`. Ma wszystko, czego funkcja potrzebuje od strumienia wejścia: `>>`, `fail()` i współpracę ze `std::getline`. Parametr `input` staje się wtedy inną nazwą strumienia z tekstem:

<!-- fragment -->
```cpp
std::istringstream input{"4\n"};
Shipment shipment{"Old Destination", 1};
const bool accepted{read_shipment_values(input, "North Hub", shipment)};
```

**W tej lekcji wystarczy jeden sposób użycia:** utworzyć strumień z gotowym tekstem i z niego czytać. Biblioteka ma też strumienie, do których się pisze, i sposoby na powrót do początku strumienia, ale testy z tej lekcji ich nie potrzebują. Obowiązuje prostsza zasada: **każdy niezależny przypadek testowy dostaje nowy `std::istringstream`.**

## 3. Kontrakt `read_shipment_values`

Funkcja jest taka sama jak w lekcjach 10.4 i 12.2, co do znaku:

<!-- fragment -->
```cpp
bool read_shipment_values(std::istream& input, const std::string& destination, Shipment& result) {
    int boxes{0};
    input >> boxes;

    if (input.fail()) {
        return false;
    }

    if (boxes < 0) {
        return false;
    }

    result = Shipment{destination, boxes};
    return true;
}
```

**Kontrakt:**

- funkcja dostaje strumień, niepustą nazwę miejsca docelowego, odczytaną wcześniej przez wywołującego, i rekord wynikowy;
- odczytuje przez `>>` jedną liczbę paczek;
- `true`: liczba jest odczytana i nie jest ujemna, a `result` zawiera podaną nazwę i tę liczbę;
- `false`: odczyt się nie udał albo liczba jest ujemna, a `result` jest **bez zmian**;
- po `false` stan strumienia mówi, który to powód: po nieudanym odczycie `fail()` daje `true`, a po odczytanej, ale ujemnej liczbie `false`;
- kontrakt nie ogranicza liczby paczek z góry.

Funkcji nie zmieniamy po to, żeby łatwiej ją było testować. Test ma sprawdzić dokładnie tę funkcję, której używa program.

**Przypadki demonstracji.** Każdy zaczyna od rekordu `Shipment{"Old Destination", 1}`, czyli od wartości, których funkcja nie zapisałaby dla żadnych z tych danych. Po wywołaniu od razu widać, czy rekord się zmienił.

| Przypadek | Tekst strumienia | Nazwa | Wynik | Rekord po wywołaniu | `fail()` po wywołaniu |
|---|---|---|---|---|---|
| A | `"4\n"` | `North Hub` | `true` | `North Hub`, 4 | nie sprawdzamy |
| B | `"0\n"` | `North Hub` | `true` | `North Hub`, 0 | nie sprawdzamy |
| C | `"-2\n"` | `North Hub` | `false` | bez zmian: `Old Destination`, 1 | `false` |
| D | `"seven\n"` | `North Hub` | `false` | bez zmian: `Old Destination`, 1 | `true` |
| E | `""` | `North Hub` | `false` | bez zmian: `Old Destination`, 1 | `true` |
| F | `"4"` | `North Hub` | `true` | `North Hub`, 4 | nie sprawdzamy |
| G | `"1250\n"` | `West End Depot` | `true` | `West End Depot`, 1250 | nie sprawdzamy |

- **C, D i E różni stan strumienia.** W C liczba jest odczytana, ale ujemna, więc `fail()` daje `false`. W D `seven` nie jest liczbą, a w E nie ma żadnej liczby, więc `fail()` daje `true`. We wszystkich trzech rekord zostaje bez zmian.
- **F, liczba bez znaku końca linii:** `>>` doszedł do końca tekstu, ale odczyt się udał (lekcja 10.4, punkt 5), więc funkcja zwraca `true`. Brak znaku końca linii nie oznacza porażki.
- **G:** kontrakt nie ma górnego limitu, a nazwa ze spacjami trafia do rekordu w całości.

## 4. Jedno wywołanie, kilka sprawdzeń

W lekcjach 13.1 i 13.2 funkcja miała jeden wynik, więc każdy przypadek oznaczał jedno porównanie. `read_shipment_values` ma kilka skutków, które da się zaobserwować: zwraca `bool`, zmienia albo zostawia rekord i może zmienić stan strumienia. **Jedno wywołanie może wymagać sprawdzenia kilku własności.**

**Przypadek przyjęty** (A, B, F, G) potwierdza trzy rzeczy:

1. funkcja zwróciła `true`;
2. nazwa w rekordzie jest poprawna;
3. liczba paczek w rekordzie jest poprawna.

**Przypadek odmowy** (C, D, E) potwierdza cztery:

1. funkcja zwróciła `false`;
2. nazwa w rekordzie jest bez zmian;
3. liczba paczek w rekordzie jest bez zmian;
4. `fail()` odpowiada przyczynie odmowy.

Samo `true` nie wystarczy: funkcja mogłaby zwrócić `true` i zapisać złą liczbę. Samo `false` też nie: mogłaby odmówić, a mimo to zmienić rekord (punkt 8).

W przypadkach przyjętych `fail()` nie sprawdzamy: funkcja zwraca `true` tylko po udanym odczycie. `eof()` też nie: w F strumień doszedł do końca tekstu, ale kontrakt o tym milczy, a test sprawdza kontrakt.

**Jak liczymy.** Rozróżniamy dwie rzeczy:

- **przypadek** to jeden zestaw danych i jedno wywołanie funkcji;
- **sprawdzenie** to jedno porównanie jednej własności, z jednym werdyktem `PASS` albo `FAIL`.

Jeden przypadek daje więc trzy albo cztery sprawdzenia. Licznik z lekcji 13.1 liczy teraz sprawdzenia, więc nazywa się `checks`, a podsumowanie ma postać `Checks: N, failed: F`. Kod zakończenia zależy, jak dotąd, od licznika niepowodzeń.

## 5. Funkcje sprawdzające dla liczby i tekstu

`check_bool` i `bool_text` są takie jak w lekcji 13.2, tylko licznik nazywa się `checks`. Do liczb i tekstów potrzebne są dwie kolejne funkcje o tym samym kształcie:

<!-- fragment -->
```cpp
void check_int(const std::string& name, int expected, int actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << expected << ", actual " << actual << "\n";
        ++failed;
    }
}

void check_text(const std::string& name, const std::string& expected, const std::string& actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected \"" << expected << "\", actual \"" << actual << "\"\n";
        ++failed;
    }
}
```

- **`check_int`** to `check_equal` z lekcji 13.1 pod nazwą, która mówi, jaki typ porównuje.
- **`check_text`** porównuje teksty i wypisuje je w cudzysłowie, zapisanym jako `\"`. Dzięki temu widać pusty tekst (`""`) i spację na końcu.
- **Każda funkcja ma własną nazwę,** bo każda przyjmuje inny typ wartości.
- **Nazwa sprawdzenia** to litera przypadku i sprawdzana własność: `A accepted`, `C destination`, `D fail()`. Po linijce `FAIL` od razu widać, który przypadek i która własność się nie zgadza.

## 6. Testy poprawnego odczytu

Pierwszy program testowy sprawdza przypadki przyjęte: A, B, F i G.

<!-- example: shipment_tests -->
```cpp
#include <iostream>
#include <sstream>
#include <string>

struct Shipment {
    std::string destination;
    int boxes;
};

bool read_shipment_values(std::istream& input, const std::string& destination, Shipment& result) {
    int boxes{0};
    input >> boxes;

    if (input.fail()) {
        return false;
    }

    if (boxes < 0) {
        return false;
    }

    result = Shipment{destination, boxes};
    return true;
}

std::string bool_text(bool value) {
    if (value) {
        return "true";
    }

    return "false";
}

void check_bool(const std::string& name, bool expected, bool actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << bool_text(expected) << ", actual " << bool_text(actual) << "\n";
        ++failed;
    }
}

void check_int(const std::string& name, int expected, int actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << expected << ", actual " << actual << "\n";
        ++failed;
    }
}

void check_text(const std::string& name, const std::string& expected, const std::string& actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected \"" << expected << "\", actual \"" << actual << "\"\n";
        ++failed;
    }
}

int main() {
    int checks{0};
    int failed{0};

    std::istringstream input_a{"4\n"};
    Shipment shipment_a{"Old Destination", 1};
    const bool accepted_a{read_shipment_values(input_a, "North Hub", shipment_a)};
    check_bool("A accepted", true, accepted_a, checks, failed);
    check_text("A destination", "North Hub", shipment_a.destination, checks, failed);
    check_int("A boxes", 4, shipment_a.boxes, checks, failed);

    std::istringstream input_b{"0\n"};
    Shipment shipment_b{"Old Destination", 1};
    const bool accepted_b{read_shipment_values(input_b, "North Hub", shipment_b)};
    check_bool("B accepted", true, accepted_b, checks, failed);
    check_text("B destination", "North Hub", shipment_b.destination, checks, failed);
    check_int("B boxes", 0, shipment_b.boxes, checks, failed);

    std::istringstream input_f{"4"};
    Shipment shipment_f{"Old Destination", 1};
    const bool accepted_f{read_shipment_values(input_f, "North Hub", shipment_f)};
    check_bool("F accepted", true, accepted_f, checks, failed);
    check_text("F destination", "North Hub", shipment_f.destination, checks, failed);
    check_int("F boxes", 4, shipment_f.boxes, checks, failed);

    std::istringstream input_g{"1250\n"};
    Shipment shipment_g{"Old Destination", 1};
    const bool accepted_g{read_shipment_values(input_g, "West End Depot", shipment_g)};
    check_bool("G accepted", true, accepted_g, checks, failed);
    check_text("G destination", "West End Depot", shipment_g.destination, checks, failed);
    check_int("G boxes", 1250, shipment_g.boxes, checks, failed);

    std::cout << "Checks: " << checks << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

**To pierwsze obowiązkowe uruchomienie.** Zastąp zawartość `main.cpp` w `lesson_13_3` tym programem, zbuduj go i uruchom. **Przewidź** liczbę sprawdzeń i kod zakończenia.

<details>
<summary>Standardowe wyjście i kod zakończenia</summary>

<!-- output: shipment_tests -->
```text
PASS A accepted
PASS A destination
PASS A boxes
PASS B accepted
PASS B destination
PASS B boxes
PASS F accepted
PASS F destination
PASS F boxes
PASS G accepted
PASS G destination
PASS G boxes
Checks: 12, failed: 0
```

CLion pokazuje `Process finished with exit code 0`.

</details>

- **Każdy przypadek ma własne zmienne:** strumień `input_a`, rekord `shipment_a` i wynik `accepted_a`. Litera w nazwie mówi, do którego przypadku należą. Żaden przypadek nie korzysta ze zmiennych innego.
- **Funkcja jest ta sama co w lekcjach 10.4 i 12.2.** Zmienił się tylko kod wywołujący: zamiast `std::cin` albo pliku dostaje strumień z tekstem.
- **Cztery przypadki, dwanaście sprawdzeń.** Podsumowanie liczy sprawdzenia, a nie przypadki.

## 7. Testy odmowy: rekord bez zmian

**Dopisz do `main` przypadki C, D i E** z tabeli z punktu 3, między B a F. Każdy dostaje nowy strumień z własnym tekstem, rekord startowy `Old Destination`, 1 i cztery sprawdzenia z punktu 4. Rekord bez zmian oznacza, że oczekiwana nazwa to `Old Destination`, a oczekiwana liczba paczek to 1. Czwarte sprawdzenie porównuje `fail()` strumienia tego przypadku, na przykład `input_c.fail()`, z wartością z tabeli.

**To drugie obowiązkowe uruchomienie.** Uruchom program z siedmioma przypadkami. **Przewidź** podsumowanie.

<details>
<summary>Standardowe wyjście i kod zakończenia</summary>

<!-- output: shipment_all_tests -->
```text
PASS A accepted
PASS A destination
PASS A boxes
PASS B accepted
PASS B destination
PASS B boxes
PASS C accepted
PASS C destination
PASS C boxes
PASS C fail()
PASS D accepted
PASS D destination
PASS D boxes
PASS D fail()
PASS E accepted
PASS E destination
PASS E boxes
PASS E fail()
PASS F accepted
PASS F destination
PASS F boxes
PASS G accepted
PASS G destination
PASS G boxes
Checks: 24, failed: 0
```

CLion pokazuje `Process finished with exit code 0`.

</details>

<details>
<summary>Cały program z przypadkami A–G: otwórz po własnej próbie</summary>

<!-- example: shipment_all_tests -->
```cpp
#include <iostream>
#include <sstream>
#include <string>

struct Shipment {
    std::string destination;
    int boxes;
};

bool read_shipment_values(std::istream& input, const std::string& destination, Shipment& result) {
    int boxes{0};
    input >> boxes;

    if (input.fail()) {
        return false;
    }

    if (boxes < 0) {
        return false;
    }

    result = Shipment{destination, boxes};
    return true;
}

std::string bool_text(bool value) {
    if (value) {
        return "true";
    }

    return "false";
}

void check_bool(const std::string& name, bool expected, bool actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << bool_text(expected) << ", actual " << bool_text(actual) << "\n";
        ++failed;
    }
}

void check_int(const std::string& name, int expected, int actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << expected << ", actual " << actual << "\n";
        ++failed;
    }
}

void check_text(const std::string& name, const std::string& expected, const std::string& actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected \"" << expected << "\", actual \"" << actual << "\"\n";
        ++failed;
    }
}

int main() {
    int checks{0};
    int failed{0};

    std::istringstream input_a{"4\n"};
    Shipment shipment_a{"Old Destination", 1};
    const bool accepted_a{read_shipment_values(input_a, "North Hub", shipment_a)};
    check_bool("A accepted", true, accepted_a, checks, failed);
    check_text("A destination", "North Hub", shipment_a.destination, checks, failed);
    check_int("A boxes", 4, shipment_a.boxes, checks, failed);

    std::istringstream input_b{"0\n"};
    Shipment shipment_b{"Old Destination", 1};
    const bool accepted_b{read_shipment_values(input_b, "North Hub", shipment_b)};
    check_bool("B accepted", true, accepted_b, checks, failed);
    check_text("B destination", "North Hub", shipment_b.destination, checks, failed);
    check_int("B boxes", 0, shipment_b.boxes, checks, failed);

    std::istringstream input_c{"-2\n"};
    Shipment shipment_c{"Old Destination", 1};
    const bool accepted_c{read_shipment_values(input_c, "North Hub", shipment_c)};
    check_bool("C accepted", false, accepted_c, checks, failed);
    check_text("C destination", "Old Destination", shipment_c.destination, checks, failed);
    check_int("C boxes", 1, shipment_c.boxes, checks, failed);
    check_bool("C fail()", false, input_c.fail(), checks, failed);

    std::istringstream input_d{"seven\n"};
    Shipment shipment_d{"Old Destination", 1};
    const bool accepted_d{read_shipment_values(input_d, "North Hub", shipment_d)};
    check_bool("D accepted", false, accepted_d, checks, failed);
    check_text("D destination", "Old Destination", shipment_d.destination, checks, failed);
    check_int("D boxes", 1, shipment_d.boxes, checks, failed);
    check_bool("D fail()", true, input_d.fail(), checks, failed);

    std::istringstream input_e{""};
    Shipment shipment_e{"Old Destination", 1};
    const bool accepted_e{read_shipment_values(input_e, "North Hub", shipment_e)};
    check_bool("E accepted", false, accepted_e, checks, failed);
    check_text("E destination", "Old Destination", shipment_e.destination, checks, failed);
    check_int("E boxes", 1, shipment_e.boxes, checks, failed);
    check_bool("E fail()", true, input_e.fail(), checks, failed);

    std::istringstream input_f{"4"};
    Shipment shipment_f{"Old Destination", 1};
    const bool accepted_f{read_shipment_values(input_f, "North Hub", shipment_f)};
    check_bool("F accepted", true, accepted_f, checks, failed);
    check_text("F destination", "North Hub", shipment_f.destination, checks, failed);
    check_int("F boxes", 4, shipment_f.boxes, checks, failed);

    std::istringstream input_g{"1250\n"};
    Shipment shipment_g{"Old Destination", 1};
    const bool accepted_g{read_shipment_values(input_g, "West End Depot", shipment_g)};
    check_bool("G accepted", true, accepted_g, checks, failed);
    check_text("G destination", "West End Depot", shipment_g.destination, checks, failed);
    check_int("G boxes", 1250, shipment_g.boxes, checks, failed);

    std::cout << "Checks: " << checks << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

</details>

- **Odmowa sprawdzona z trzech stron:** wynik `false`, rekord bez zmian i stan strumienia. `fail()` odróżnia C, w którym liczba była, ale niedozwolona, od D i E, w których liczby nie udało się odczytać. To ta sama informacja, z której `main` w lekcji 10.4 wybierał między `Invalid shipments` a `Input error`.
- **Wszystkie sprawdzenia przeszły.** Znaczy to, że te siedem przypadków nie wykryło niezgodności z kontraktem, a nie że funkcja jest poprawna dla wszystkich danych (lekcja 13.2).

## 8. Gdy `bool` się zgadza, a rekord nie

Oto dwie wersje `read_shipment_values` z jedną usterką każda. Obie się budują i dla przypadków A, B, D, E, F i G dają poprawne wyniki:

| Wersja | Zmiana w funkcji | Skutek według kontraktu |
|---|---|---|
| brak kontroli wartości ujemnej | usunięte sprawdzenie `if (boxes < 0)` razem z jego `return false;` | ujemna liczba paczek jest przyjmowana |
| wynik przypisany zbyt wcześnie | `result = Shipment{destination, boxes};` stoi przed `if (boxes < 0)`, jak w programie z lekcji 10.4, punkt 8 | funkcja odmawia, ale zmienia rekord |

**Dla każdej wersji przewidź,** które sprawdzenia z zestawu A–G dadzą `FAIL`, z jaką wartością oczekiwaną i rzeczywistą. Szczególnie: czy sprawdzenie `C accepted` wykryje drugą wersję? Uruchomienie obu wersji jest nieobowiązkowe: wystarczy zmienić funkcję w `main.cpp`, a potem ją przywrócić.

<details>
<summary>Omówienie: dwie wersje i ich wyniki</summary>

**Brak kontroli wartości ujemnej.**

<!-- example: shipment_all_tests_negative_bug exit=1 -->
```cpp
#include <iostream>
#include <sstream>
#include <string>

struct Shipment {
    std::string destination;
    int boxes;
};

bool read_shipment_values(std::istream& input, const std::string& destination, Shipment& result) {
    int boxes{0};
    input >> boxes;

    if (input.fail()) {
        return false;
    }

    result = Shipment{destination, boxes};
    return true;
}

std::string bool_text(bool value) {
    if (value) {
        return "true";
    }

    return "false";
}

void check_bool(const std::string& name, bool expected, bool actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << bool_text(expected) << ", actual " << bool_text(actual) << "\n";
        ++failed;
    }
}

void check_int(const std::string& name, int expected, int actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << expected << ", actual " << actual << "\n";
        ++failed;
    }
}

void check_text(const std::string& name, const std::string& expected, const std::string& actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected \"" << expected << "\", actual \"" << actual << "\"\n";
        ++failed;
    }
}

int main() {
    int checks{0};
    int failed{0};

    std::istringstream input_a{"4\n"};
    Shipment shipment_a{"Old Destination", 1};
    const bool accepted_a{read_shipment_values(input_a, "North Hub", shipment_a)};
    check_bool("A accepted", true, accepted_a, checks, failed);
    check_text("A destination", "North Hub", shipment_a.destination, checks, failed);
    check_int("A boxes", 4, shipment_a.boxes, checks, failed);

    std::istringstream input_b{"0\n"};
    Shipment shipment_b{"Old Destination", 1};
    const bool accepted_b{read_shipment_values(input_b, "North Hub", shipment_b)};
    check_bool("B accepted", true, accepted_b, checks, failed);
    check_text("B destination", "North Hub", shipment_b.destination, checks, failed);
    check_int("B boxes", 0, shipment_b.boxes, checks, failed);

    std::istringstream input_c{"-2\n"};
    Shipment shipment_c{"Old Destination", 1};
    const bool accepted_c{read_shipment_values(input_c, "North Hub", shipment_c)};
    check_bool("C accepted", false, accepted_c, checks, failed);
    check_text("C destination", "Old Destination", shipment_c.destination, checks, failed);
    check_int("C boxes", 1, shipment_c.boxes, checks, failed);
    check_bool("C fail()", false, input_c.fail(), checks, failed);

    std::istringstream input_d{"seven\n"};
    Shipment shipment_d{"Old Destination", 1};
    const bool accepted_d{read_shipment_values(input_d, "North Hub", shipment_d)};
    check_bool("D accepted", false, accepted_d, checks, failed);
    check_text("D destination", "Old Destination", shipment_d.destination, checks, failed);
    check_int("D boxes", 1, shipment_d.boxes, checks, failed);
    check_bool("D fail()", true, input_d.fail(), checks, failed);

    std::istringstream input_e{""};
    Shipment shipment_e{"Old Destination", 1};
    const bool accepted_e{read_shipment_values(input_e, "North Hub", shipment_e)};
    check_bool("E accepted", false, accepted_e, checks, failed);
    check_text("E destination", "Old Destination", shipment_e.destination, checks, failed);
    check_int("E boxes", 1, shipment_e.boxes, checks, failed);
    check_bool("E fail()", true, input_e.fail(), checks, failed);

    std::istringstream input_f{"4"};
    Shipment shipment_f{"Old Destination", 1};
    const bool accepted_f{read_shipment_values(input_f, "North Hub", shipment_f)};
    check_bool("F accepted", true, accepted_f, checks, failed);
    check_text("F destination", "North Hub", shipment_f.destination, checks, failed);
    check_int("F boxes", 4, shipment_f.boxes, checks, failed);

    std::istringstream input_g{"1250\n"};
    Shipment shipment_g{"Old Destination", 1};
    const bool accepted_g{read_shipment_values(input_g, "West End Depot", shipment_g)};
    check_bool("G accepted", true, accepted_g, checks, failed);
    check_text("G destination", "West End Depot", shipment_g.destination, checks, failed);
    check_int("G boxes", 1250, shipment_g.boxes, checks, failed);

    std::cout << "Checks: " << checks << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

<!-- output: shipment_all_tests_negative_bug -->
```text
PASS A accepted
PASS A destination
PASS A boxes
PASS B accepted
PASS B destination
PASS B boxes
FAIL C accepted: expected false, actual true
FAIL C destination: expected "Old Destination", actual "North Hub"
FAIL C boxes: expected 1, actual -2
PASS C fail()
PASS D accepted
PASS D destination
PASS D boxes
PASS D fail()
PASS E accepted
PASS E destination
PASS E boxes
PASS E fail()
PASS F accepted
PASS F destination
PASS F boxes
PASS G accepted
PASS G destination
PASS G boxes
Checks: 24, failed: 3
```

Kod zakończenia: 1.

**Wynik przypisany zbyt wcześnie.**

<!-- example: shipment_all_tests_early_bug exit=1 -->
```cpp
#include <iostream>
#include <sstream>
#include <string>

struct Shipment {
    std::string destination;
    int boxes;
};

bool read_shipment_values(std::istream& input, const std::string& destination, Shipment& result) {
    int boxes{0};
    input >> boxes;

    if (input.fail()) {
        return false;
    }

    result = Shipment{destination, boxes};

    if (boxes < 0) {
        return false;
    }

    return true;
}

std::string bool_text(bool value) {
    if (value) {
        return "true";
    }

    return "false";
}

void check_bool(const std::string& name, bool expected, bool actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << bool_text(expected) << ", actual " << bool_text(actual) << "\n";
        ++failed;
    }
}

void check_int(const std::string& name, int expected, int actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << expected << ", actual " << actual << "\n";
        ++failed;
    }
}

void check_text(const std::string& name, const std::string& expected, const std::string& actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected \"" << expected << "\", actual \"" << actual << "\"\n";
        ++failed;
    }
}

int main() {
    int checks{0};
    int failed{0};

    std::istringstream input_a{"4\n"};
    Shipment shipment_a{"Old Destination", 1};
    const bool accepted_a{read_shipment_values(input_a, "North Hub", shipment_a)};
    check_bool("A accepted", true, accepted_a, checks, failed);
    check_text("A destination", "North Hub", shipment_a.destination, checks, failed);
    check_int("A boxes", 4, shipment_a.boxes, checks, failed);

    std::istringstream input_b{"0\n"};
    Shipment shipment_b{"Old Destination", 1};
    const bool accepted_b{read_shipment_values(input_b, "North Hub", shipment_b)};
    check_bool("B accepted", true, accepted_b, checks, failed);
    check_text("B destination", "North Hub", shipment_b.destination, checks, failed);
    check_int("B boxes", 0, shipment_b.boxes, checks, failed);

    std::istringstream input_c{"-2\n"};
    Shipment shipment_c{"Old Destination", 1};
    const bool accepted_c{read_shipment_values(input_c, "North Hub", shipment_c)};
    check_bool("C accepted", false, accepted_c, checks, failed);
    check_text("C destination", "Old Destination", shipment_c.destination, checks, failed);
    check_int("C boxes", 1, shipment_c.boxes, checks, failed);
    check_bool("C fail()", false, input_c.fail(), checks, failed);

    std::istringstream input_d{"seven\n"};
    Shipment shipment_d{"Old Destination", 1};
    const bool accepted_d{read_shipment_values(input_d, "North Hub", shipment_d)};
    check_bool("D accepted", false, accepted_d, checks, failed);
    check_text("D destination", "Old Destination", shipment_d.destination, checks, failed);
    check_int("D boxes", 1, shipment_d.boxes, checks, failed);
    check_bool("D fail()", true, input_d.fail(), checks, failed);

    std::istringstream input_e{""};
    Shipment shipment_e{"Old Destination", 1};
    const bool accepted_e{read_shipment_values(input_e, "North Hub", shipment_e)};
    check_bool("E accepted", false, accepted_e, checks, failed);
    check_text("E destination", "Old Destination", shipment_e.destination, checks, failed);
    check_int("E boxes", 1, shipment_e.boxes, checks, failed);
    check_bool("E fail()", true, input_e.fail(), checks, failed);

    std::istringstream input_f{"4"};
    Shipment shipment_f{"Old Destination", 1};
    const bool accepted_f{read_shipment_values(input_f, "North Hub", shipment_f)};
    check_bool("F accepted", true, accepted_f, checks, failed);
    check_text("F destination", "North Hub", shipment_f.destination, checks, failed);
    check_int("F boxes", 4, shipment_f.boxes, checks, failed);

    std::istringstream input_g{"1250\n"};
    Shipment shipment_g{"Old Destination", 1};
    const bool accepted_g{read_shipment_values(input_g, "West End Depot", shipment_g)};
    check_bool("G accepted", true, accepted_g, checks, failed);
    check_text("G destination", "West End Depot", shipment_g.destination, checks, failed);
    check_int("G boxes", 1250, shipment_g.boxes, checks, failed);

    std::cout << "Checks: " << checks << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

<!-- output: shipment_all_tests_early_bug -->
```text
PASS A accepted
PASS A destination
PASS A boxes
PASS B accepted
PASS B destination
PASS B boxes
PASS C accepted
FAIL C destination: expected "Old Destination", actual "North Hub"
FAIL C boxes: expected 1, actual -2
PASS C fail()
PASS D accepted
PASS D destination
PASS D boxes
PASS D fail()
PASS E accepted
PASS E destination
PASS E boxes
PASS E fail()
PASS F accepted
PASS F destination
PASS F boxes
PASS G accepted
PASS G destination
PASS G boxes
Checks: 24, failed: 2
```

Kod zakończenia: 1.

| Usterka | Przypadek | Sprawdzenia z `FAIL` | Oczekiwany | Rzeczywisty | Niepowodzenia |
|---|---|---|---|---|---|
| brak kontroli wartości ujemnej | C | `C accepted` | `false` | `true` | 3 |
| | | `C destination` | `"Old Destination"` | `"North Hub"` | |
| | | `C boxes` | 1 | -2 | |
| wynik przypisany zbyt wcześnie | C | `C destination` | `"Old Destination"` | `"North Hub"` | 2 |
| | | `C boxes` | 1 | -2 | |

- **Obie usterki wykrywa C,** jedyny przypadek z odczytaną, ale niedozwoloną liczbą. D i E przechodzą dla obu wersji: przy nieudanym odczycie obie funkcje zwracają `false`, zanim dojdą do rekordu.
- **W drugiej wersji `C accepted` daje `PASS`.** Funkcja zwraca poprawny `bool`, a mimo to łamie kontrakt, bo zmienia rekord. **Testowanie samej wartości zwracanej nie zawsze wystarcza.** Gdyby zestaw sprawdzał tylko `accepted`, ta wersja przeszłaby wszystkie sprawdzenia, a program testowy zakończyłby się kodem 0.
- **Ten sam błąd, inny sposób wykrycia.** W lekcji 10.4 tę usterkę ujawniało wypisanie stanu `result` i porównanie go z przewidywaniem. Teraz wykrywa ją program testowy, za każdym razem, bez wpisywania danych i bez czytania wydruku.
- Każdy program kończy się kodem 1, bo licznik niepowodzeń jest większy od zera.

</details>

## 9. Diagnostyka: jeden strumień dla dwóch testów

**Sytuacja.** Ktoś chce sprawdzić, że funkcja zapisuje w rekordzie tę nazwę, którą dostała. Przygotował dwa niezależne testy z tą samą liczbą 4 i różnymi nazwami. Uznał, że skoro oba potrzebują tego samego tekstu, wystarczy jeden strumień. Funkcja `read_shipment_values` jest tu **poprawna**.

<!-- example: shipment_shared_stream exit=1 -->
```cpp
#include <iostream>
#include <sstream>
#include <string>

struct Shipment {
    std::string destination;
    int boxes;
};

bool read_shipment_values(std::istream& input, const std::string& destination, Shipment& result) {
    int boxes{0};
    input >> boxes;

    if (input.fail()) {
        return false;
    }

    if (boxes < 0) {
        return false;
    }

    result = Shipment{destination, boxes};
    return true;
}

std::string bool_text(bool value) {
    if (value) {
        return "true";
    }

    return "false";
}

void check_bool(const std::string& name, bool expected, bool actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << bool_text(expected) << ", actual " << bool_text(actual) << "\n";
        ++failed;
    }
}

void check_int(const std::string& name, int expected, int actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << expected << ", actual " << actual << "\n";
        ++failed;
    }
}

void check_text(const std::string& name, const std::string& expected, const std::string& actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected \"" << expected << "\", actual \"" << actual << "\"\n";
        ++failed;
    }
}

int main() {
    int checks{0};
    int failed{0};
    std::istringstream input{"4"};

    Shipment north{"Old Destination", 1};
    const bool north_accepted{read_shipment_values(input, "North Hub", north)};
    check_bool("North Hub accepted", true, north_accepted, checks, failed);
    check_text("North Hub destination", "North Hub", north.destination, checks, failed);
    check_int("North Hub boxes", 4, north.boxes, checks, failed);

    Shipment south{"Old Destination", 1};
    const bool south_accepted{read_shipment_values(input, "South Depot", south)};
    check_bool("South Depot accepted", true, south_accepted, checks, failed);
    check_text("South Depot destination", "South Depot", south.destination, checks, failed);
    check_int("South Depot boxes", 4, south.boxes, checks, failed);

    std::cout << "Checks: " << checks << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

**To trzecie obowiązkowe uruchomienie: jedna czynność diagnostyczna.** Typ `Shipment`, funkcja `read_shipment_values` i funkcje sprawdzające są takie same jak w punkcie 7, więc w `main.cpp` wystarczy zastąpić `main`.

1. **Przewidź** wynik pierwszego wywołania, dla `North Hub`.
2. **Przewidź** wynik drugiego wywołania, dla `South Depot`.
3. Uruchom program. Ustal, w którym miejscu tekstu `4` skończył się pierwszy odczyt i co zostało w strumieniu dla drugiego.
4. Wyjaśnij, dlaczego tekst `4` nie pojawia się w strumieniu ponownie.
5. Wskaż błąd w organizacji testów: w funkcji czy w programie testowym?
6. Zaproponuj najmniejszą poprawkę.
7. Wprowadź ją i uruchom program ponownie.
8. Wyjaśnij, dlaczego każdy niezależny test powinien zaczynać od własnego strumienia.

<details>
<summary>Standardowe wyjście i kod zakończenia</summary>

<!-- output: shipment_shared_stream -->
```text
PASS North Hub accepted
PASS North Hub destination
PASS North Hub boxes
FAIL South Depot accepted: expected true, actual false
FAIL South Depot destination: expected "South Depot", actual "Old Destination"
FAIL South Depot boxes: expected 4, actual 1
Checks: 6, failed: 3
```

CLion pokazuje `Process finished with exit code 1`.

</details>

<details>
<summary>Wyjaśnienie i poprawka</summary>

| Chwila | Co zostało w strumieniu | Wynik odczytu |
|---|---|---|
| przed pierwszym wywołaniem | `4` | |
| po pierwszym wywołaniu | nic: `>>` odczytał `4` i doszedł do końca tekstu | liczba 4, `fail()` daje `false` |
| po drugim wywołaniu | nic | nieudany odczyt, `fail()` daje `true` |

- **Pierwszy test jest poprawny:** `true`, `North Hub`, 4.
- **Drugi test dostaje strumień, w którym nie ma już danych.** `>>` nie znajduje liczby, więc funkcja zwraca `false` i zostawia rekord bez zmian. Dokładnie tak mówi jej kontrakt, więc **funkcja jest poprawna, a błąd jest w programie testowym.**
- **Odczytane znaki nie wracają.** Strumień pamięta, dokąd doszedł, tak jak `std::cin` pamięta, które dane już odczytano. Drugie wywołanie nie dostaje nowej kopii tekstu. Z tekstem `"4\n"` wynik byłby taki sam: drugi odczyt pominąłby znak końca linii i też nie znalazłby liczby.
- **`clear()` by nie pomogło.** Zdjęłoby znacznik nieudanego odczytu, ale nie tworzy nowych danych (lekcja 4.6). Po `clear()` strumień nadal byłby pusty.
- **Najmniejsza poprawka:** osobny strumień dla każdego testu, każdy z tym samym tekstem. Funkcji nie zmieniasz.

<!-- example: shipment_separate_streams -->
```cpp
#include <iostream>
#include <sstream>
#include <string>

struct Shipment {
    std::string destination;
    int boxes;
};

bool read_shipment_values(std::istream& input, const std::string& destination, Shipment& result) {
    int boxes{0};
    input >> boxes;

    if (input.fail()) {
        return false;
    }

    if (boxes < 0) {
        return false;
    }

    result = Shipment{destination, boxes};
    return true;
}

std::string bool_text(bool value) {
    if (value) {
        return "true";
    }

    return "false";
}

void check_bool(const std::string& name, bool expected, bool actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << bool_text(expected) << ", actual " << bool_text(actual) << "\n";
        ++failed;
    }
}

void check_int(const std::string& name, int expected, int actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << expected << ", actual " << actual << "\n";
        ++failed;
    }
}

void check_text(const std::string& name, const std::string& expected, const std::string& actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected \"" << expected << "\", actual \"" << actual << "\"\n";
        ++failed;
    }
}

int main() {
    int checks{0};
    int failed{0};

    std::istringstream north_input{"4"};
    Shipment north{"Old Destination", 1};
    const bool north_accepted{read_shipment_values(north_input, "North Hub", north)};
    check_bool("North Hub accepted", true, north_accepted, checks, failed);
    check_text("North Hub destination", "North Hub", north.destination, checks, failed);
    check_int("North Hub boxes", 4, north.boxes, checks, failed);

    std::istringstream south_input{"4"};
    Shipment south{"Old Destination", 1};
    const bool south_accepted{read_shipment_values(south_input, "South Depot", south)};
    check_bool("South Depot accepted", true, south_accepted, checks, failed);
    check_text("South Depot destination", "South Depot", south.destination, checks, failed);
    check_int("South Depot boxes", 4, south.boxes, checks, failed);

    std::cout << "Checks: " << checks << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

<!-- output: shipment_separate_streams -->
```text
PASS North Hub accepted
PASS North Hub destination
PASS North Hub boxes
PASS South Depot accepted
PASS South Depot destination
PASS South Depot boxes
Checks: 6, failed: 0
```

Kod zakończenia: 0. Ta sama, niezmieniona funkcja przechodzi oba testy.

**Ponowne użycie strumienia nie jest błędem samo w sobie.** Pętla w `main` z lekcji 10.4 czytała z jednego `std::cin` wszystkie przesyłki po kolei i tak miało być: każdy odczyt miał zacząć tam, gdzie skończył poprzedni. Gdyby test miał sprawdzić odczyt dwóch kolejnych przesyłek z jednego źródła, jeden strumień z obiema liczbami byłby właściwy. **Błędem jest założenie, że dwa niezależne przypadki automatycznie zaczynają od tych samych danych.**

</details>

**Zasada z tej diagnostyki:** przypadki testowe mają być od siebie niezależne. Wynik jednego nie może zależeć od tego, co zrobił poprzedni. Dlatego każdy przypadek dostaje nowy strumień i własne zmienne wynikowe.

## 10. Misja: testy dziennika zadań

Program dziennika zadań z misji lekcji 12.3 czyta plik `chores.txt` funkcją `read_chores`. Teraz zadanie jest inne: **przetestować tę funkcję bez pliku**, tekstami w `std::istringstream`.

**Kontrakt funkcji z lekcji 12.3**, bez żadnej zmiany:

- nagłówek: `bool read_chores(std::istream& input, std::vector<Chore>& chores, std::string& error, int& error_line)`, a `Chore` ma pola tekstowe `name` i `status`;
- każdy rekord zajmuje dwie fizyczne linie: nazwę zadania i status `done` albo `pending`, z rozróżnieniem wielkości liter i bez dodatkowych spacji;
- dane kończy wyłącznie koniec danych w miejscu, w którym zaczynałby się kolejny rekord, a ostatnia linia może nie mieć znaku końca linii;
- każda pusta linia jest błędem `"empty"`, niepusty status inny niż `done` i `pending` to błąd `"invalid"`, a brak linii statusu po nazwie to `"incomplete"`;
- przy sukcesie funkcja zwraca `true`, a wektor zawiera rekordy w kolejności z danych;
- przy pierwszym błędzie funkcja zwraca `false`, a w `error` i `error_line` zapisuje rodzaj błędu i numer fizycznej linii, liczony od 1; przy `"incomplete"` to numer linii nazwy.

**Czego kontrakt nie obiecuje.** Po `false` wektor może zawierać rekordy odczytane przed błędem: program z lekcji 12.3 po prostu nie wypisuje wtedy raportu. Po `true` funkcja nie musi zmieniać `error` ani `error_line`. Testy sprawdzają to, co kontrakt obiecuje, a nie przypadkowe szczegóły implementacji.

W `cpp-workspace` utwórz katalog `chore_log_tests`, skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program` i otwórz go w CLionie. `CMakeLists.txt` zostaw bez zmian. Z [rozwiązania misji lekcji 12.3](../module_12_text_files/lesson_03_end_of_data_and_errors.md#przykładowe-rozwiązania) skopiuj do `main.cpp` typ `Chore` i funkcję `read_chores`, bez zmian, ale bez jej `main` i bez `#include <fstream>`. Funkcji nie musisz pisać z pamięci: oceniane są testy.

**Przypadki.** Każdy tekst to dokładnie dane, które przekazujesz konstruktorowi `std::istringstream`:

| Przypadek | Tekst strumienia |
|---|---|
| A | `""` |
| B | `"Clean tables\ndone\nSort books\npending\n"` |
| C | `"Clean tables\ndone"` |
| D | `"\n"` |
| E | `"Clean tables\n\n"` |
| F | `"Clean tables\nlater\n"` |
| G | `"Clean tables\n"` |
| H | `"Clean tables\ndone\n\n"` |
| I | `"Clean tables\ndone\nSort books\nlater\n"` |
| J | `"Clean tables\ndone\nSort books"` |
| K | `"Clean tables\ndone\nClean tables\npending"` |
| L | `"Clean tables\ndone \n"` |
| M | `"Clean tables\nlater"` |

Musisz samodzielnie zdecydować:

1. jak utworzyć strumień z każdym z tych tekstów i przekazać go do `read_chores`;
2. jak przygotować wektor wynikowy oraz zmienne `error` i `error_line` dla każdego przypadku;
3. które własności sprawdzić przy sukcesie, a które przy błędzie;
4. jak sprawdzić rozmiar wektora, skoro `size()` zwraca `std::size_t`;
5. jak porównać kolejne rekordy, pole po polu, i jak nie odczytać elementu, którego w wektorze nie ma;
6. jak porównać rodzaj błędu i numer linii;
7. które przypadki sprawdzają koniec danych, które pustą linię, które błędny status, a które brak końcowego znaku końca linii;
8. jak pokazać, że żaden przypadek nie korzysta z wyniku poprzedniego.

**Kolejność pracy:**

1. **Ustal wyniki oczekiwane, zanim napiszesz kod.** Dla każdego przypadku zapisz na kartce: sukces czy błąd; przy sukcesie liczbę rekordów i każdy rekord; przy błędzie rodzaj i numer linii. Wyniki mają wynikać z kontraktu, a nie z uruchomienia funkcji.
2. Napisz program testowy: funkcje sprawdzające, dla każdego przypadku osobny strumień, wektor, `error` i `error_line`, potem sprawdzenia, podsumowanie i kod zakończenia 1 po niepowodzeniu.
3. **To czwarte obowiązkowe uruchomienie:** uruchom program z poprawną funkcją. Wszystkie sprawdzenia powinny dać `PASS`, a kod zakończenia powinien wynosić 0. Jeśli któreś daje `FAIL`, najpierw ustal z kontraktu, czy błędny jest wynik oczekiwany, czy sprawdzenie (lekcja 13.2, punkt 9).
4. **Celowa usterka.** Wprowadź do `read_chores` starą regułę zakończenia z lekcji 12.3, punkt 7: warunek pętli `while (!input.fail() && !name.empty())` i bez sprawdzenia `if (name.empty())` na początku pętli. **Przewidź**, które sprawdzenia dadzą `FAIL`.
5. **To piąte obowiązkowe uruchomienie:** uruchom ten sam program testowy z funkcją z usterką. Zapisz, które przypadki ją wykryły i jaki był kod zakończenia. Jeśli żadne sprawdzenie nie dało `FAIL`, dopisz przypadek, który odróżni obie wersje. Potem przywróć poprawną funkcję i uruchom testy jeszcze raz.
6. **Uzasadnij wybór.** Dla przypadków C, D, H i J napisz jednym zdaniem, jaką pomyłkę w funkcji każdy z nich mógłby wykryć.

<details>
<summary>Wyniki oczekiwane: otwórz po przygotowaniu własnych</summary>

| Przypadek | Wynik | Rekordy albo błąd | Co sprawdza |
|---|---|---|---|
| A | `true` | 0 rekordów | pusty tekst, czyli koniec danych od razu |
| B | `true` | `Clean tables`, `done`; `Sort books`, `pending` | dwa rekordy w kolejności, nazwy ze spacjami |
| C | `true` | `Clean tables`, `done` | ostatni status bez znaku końca linii |
| D | `false` | `"empty"`, linia 1 | jedna pusta linia, czyli coś innego niż pusty tekst |
| E | `false` | `"empty"`, linia 2 | pusta linia w miejscu statusu |
| F | `false` | `"invalid"`, linia 2 | nieprawidłowy status pierwszego rekordu |
| G | `false` | `"incomplete"`, linia 1 | brak linii statusu, numer linii nazwy |
| H | `false` | `"empty"`, linia 3 | pusta linia po ostatnim kompletnym rekordzie |
| I | `false` | `"invalid"`, linia 4 | pierwszy błąd po poprawnym rekordzie, numer linii, a nie rekordu |
| J | `false` | `"incomplete"`, linia 3 | sama nazwa bez znaku końca linii po poprawnym rekordzie |
| K | `true` | `Clean tables`, `done`; `Clean tables`, `pending` | powtórzona nazwa, kolejność statusów |
| L | `false` | `"invalid"`, linia 2 | spacja po statusie |
| M | `false` | `"invalid"`, linia 2 | nieprawidłowy status bez znaku końca linii |

</details>

### Kryterium sukcesu

- Program buduje się jako C++20, a `CMakeLists.txt` jest taki jak w lekcji 0.5.
- `read_chores` jest taka jak w rozwiązaniu lekcji 12.3, a wszystkie dane testowe są w tekstach przekazanych `std::istringstream`. Program nie otwiera żadnego pliku i nie czyta `std::cin`.
- Wyniki oczekiwane wynikają z kontraktu i powstały przed uruchomieniem.
- Każdy przypadek ma własny strumień, wektor, `error` i `error_line`.
- Przy sukcesie program sprawdza wynik, rozmiar wektora i każdy rekord, pole po polu, w kolejności. Elementy sprawdza tylko wtedy, gdy rozmiar się zgadza.
- Przy błędzie program sprawdza wynik, rodzaj błędu i numer fizycznej linii.
- Każde sprawdzenie ma nazwę i wypisuje `PASS` albo `FAIL` z wartością oczekiwaną i rzeczywistą, a na końcu program wypisuje podsumowanie.
- Z poprawną funkcją wszystkie sprawdzenia przechodzą i kod zakończenia wynosi 0. Ze starą regułą zakończenia co najmniej jedno daje `FAIL` i kod zakończenia wynosi 1.
- Umiesz wyjaśnić, dlaczego A i D to różne przypadki i dlaczego G daje linię 1, a J linię 3.

Gdy wynik się zgadza, możesz zapisać projekt w Gicie, jak w lekcji 1.5: `main.cpp` i `CMakeLists.txt`, bez katalogu budowania.

<details>
<summary>Podpowiedź 1: źródło danych</summary>

Funkcja oczekuje `std::istream&`. Który obiekt z tej lekcji jest strumieniem wejścia, a znaki bierze z tekstu w kodzie? Każdy tekst z tabeli przepisz do kodu dokładnie, razem z `\n` albo bez niego na końcu: to różnica między przypadkami, a nie szczegół zapisu.

</details>

<details>
<summary>Podpowiedź 2: wynik funkcji</summary>

Po wywołaniu `read_chores` masz cztery rzeczy do obejrzenia: wynik `bool`, wektor, `error` i `error_line`. Przy sukcesie liczą się wynik i wektor, przy błędzie wynik, `error` i `error_line`. Rozmiar wektora ma typ `std::size_t`, więc do jego porównania przyda się funkcja sprawdzająca z parametrami tego typu (lekcja 6.3). Rekord sprawdź pole po polu, przez indeks, ale dopiero po upewnieniu się, że rozmiar się zgadza.

</details>

<details>
<summary>Podpowiedź 3: niezależność przypadków</summary>

Co zawierałby wektor w przypadku C, gdyby był tym samym wektorem co w przypadku B? Co odczytałby przypadek C ze strumienia przypadku B? Co zostałoby w `error`, gdyby przypadek sukcesu dostał zmienną po przypadku błędu? Każdy przypadek potrzebuje nowego strumienia i własnych zmiennych wynikowych.

</details>

Przykładowe rozwiązanie jest w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 11. Gdy coś pójdzie inaczej

| Co widzisz | Co to znaczy | Co zrobić |
|---|---|---|
| Kompilator zgłasza błąd przy `std::istringstream`, na przykład `implicit instantiation of undefined template 'std::basic_istringstream<char>'` | Brakuje `#include <sstream>`. Standard nie gwarantuje, że `<iostream>` go dołącza. | Dołącz `<sstream>` zawsze, gdy używasz `std::istringstream`. |
| Pierwszy przypadek przechodzi, a następny, z poprawnymi danymi, daje `actual false` | Kolejny przypadek czyta ze strumienia poprzedniego, w którym nie ma już danych (punkt 9). | Utwórz nowy `std::istringstream` dla każdego przypadku. |
| `size` daje więcej rekordów, niż jest w tekście | Przypadek dostał wektor po poprzednim przypadku, a funkcja dopisuje do niego rekordy przez `push_back`. | Przygotuj dla każdego przypadku nowy, pusty wektor. |
| Program kończy się nagle albo wypisuje przypadkowe wartości przy sprawdzaniu rekordów | Sprawdzenie odczytuje element, którego w wektorze nie ma: niezdefiniowane zachowanie (lekcja 6.3). | Sprawdzaj elementy tylko wtedy, gdy rozmiar wektora się zgadza. |
| `FAIL ... error_line` dla błędu w drugim rekordzie, choć funkcja jest poprawna | Wynik oczekiwany podaje numer rekordu albo nie liczy linii statusu. | Policz fizyczne linie od 1, jak w tabelach z lekcji 12.3, punkt 4. |
| `FAIL ... expected "empty", actual ""` | Funkcja zwróciła `true` i nie zapisała rodzaju błędu, a zmienna została taka, jak ją przygotowano. Sprawdzenie wyniku `complete` w tym samym przypadku też daje `FAIL`. | Ustal z kontraktu, czy ten tekst jest błędem. Jeśli jest, usterka jest w funkcji. |

## 12. Wyjaśnij

Odpowiedz własnymi słowami, najlepiej na piśmie. Dopiero potem porównaj z przykładowymi odpowiedziami.

1. Dlaczego można przekazać `std::istringstream` funkcji z parametrem `std::istream&`?
2. Czym różni się `std::istringstream` od `std::ifstream`?
3. Dlaczego test funkcji odczytu nie potrzebuje fizycznego pliku?
4. Dlaczego każdy niezależny przypadek powinien dostać nowy strumień?
5. Co może się stać, gdy drugi test użyje strumienia, z którego pierwszy już odczytał dane?
6. Dlaczego sprawdzenie samego wyniku `bool` może nie wystarczyć?
7. Jak sprawdzić, że rekord pozostał bez zmian po odmowie?
8. Jak sprawdzić rodzaj błędu i numer linii?
9. Dlaczego pusty strumień i strumień z jednym znakiem końca linii to różne przypadki?
10. Jak test może wykryć błąd, który nie zmienia wartości zwracanej, ale zmienia dane wynikowe?

<details>
<summary>Przykładowe odpowiedzi</summary>

1. Bo biblioteka standardowa określa `std::istringstream` jako szczególny rodzaj `std::istream`, tak jak `std::ifstream`. Ma `>>`, `fail()` i współpracuje ze `std::getline`, czyli ma wszystko, czego funkcja potrzebuje od strumienia wejścia. Parametr `std::istream&` staje się inną nazwą strumienia z tekstem.
2. `std::ifstream` czyta znaki z otwartego pliku na dysku, a `std::istringstream` z tekstu podanego przy jego tworzeniu. Do czytania pliku w programie nadal służy `std::ifstream`. Strumień z tekstu jest wygodny przede wszystkim w testach.
3. Bo funkcja czyta ze strumienia, który dostanie, i nie wie, skąd pochodzą znaki. Tekst w `std::istringstream` daje jej dokładnie te same bajty co plik, bez katalogu roboczego, bez przygotowywania pliku i bez wpisywania danych.
4. Bo strumień pamięta, dokąd doszedł odczyt, i odczytane znaki do niego nie wracają. Nowy strumień daje każdemu przypadkowi jego dane od początku, niezależnie od tego, co zrobiły inne przypadki.
5. Drugi test zacznie czytać tam, gdzie skończył pierwszy. Jeśli tekst się skończył, odczyt się nie uda, a test da `FAIL`, choć funkcja jest poprawna. Błąd jest wtedy w programie testowym, nie w funkcji.
6. Bo funkcja może mieć kilka skutków: wynik `bool`, rekord albo wektor i dane o błędzie. Może zwrócić poprawny `bool`, a jednocześnie zapisać złe dane albo zmienić rekord, który miał zostać bez zmian.
7. Przygotować rekord z wartościami, których funkcja nie zapisałaby dla tych danych, na przykład `Old Destination` i 1, a po odmowie porównać każde pole z tymi wartościami.
8. Przygotować dla przypadku osobne zmienne `error` i `error_line`, a po wywołaniu porównać `error` z oczekiwanym rodzajem, na przykład `"empty"`, przez `check_text`, a `error_line` z numerem fizycznej linii przez `check_int`.
9. Pusty strumień nie ma ani jednej linii: pierwszy odczyt się nie udaje, więc dane się kończą i wynik to sukces bez rekordów. Strumień `"\n"` ma jedną, pustą linię: odczyt się udaje, a pusta nazwa jest błędem `"empty"` w linii 1.
10. Sprawdzając, oprócz wartości zwracanej, także rekord, wektor albo dane o błędzie. Na przykład wersję, która odmawia, ale zmienia rekord, wykrywają sprawdzenia pól rekordu, choć sprawdzenie wyniku `bool` daje `PASS`.

</details>

## Podsumowanie

- `std::istringstream` z `<sstream>` to strumień wejścia z tekstu podanego przy jego tworzeniu. Funkcja z parametrem `std::istream&` czyta z niego tak samo jak ze `std::cin` i z pliku.
- Tekst w strumieniu to dokładnie dane: `""` to pusty plik, `"\n"` jedna pusta linia, a tekst bez `\n` na końcu to ostatnia linia bez znaku końca linii.
- Funkcji odczytu nie trzeba zmieniać, żeby ją przetestować. Zmienia się tylko kod wywołujący.
- Jedno wywołanie może mieć kilka skutków. Test sprawdza każdy, który obiecuje kontrakt: wynik, rekord albo wektor, dane o błędzie i, jeśli kontrakt o nim mówi, stan strumienia.
- Przypadek to jeden zestaw danych i jedno wywołanie, a sprawdzenie to jedno porównanie. Podsumowanie liczy sprawdzenia.
- Każdy niezależny przypadek dostaje nowy strumień i własne zmienne wynikowe, bo odczytane znaki nie wracają do strumienia. Jeden strumień jest właściwy wtedy, gdy program ma czytać kolejne dane z jednego źródła.

## Co dalej

Programy testowe z tej lekcji zawierają kopię testowanej funkcji. Gdyby ktoś zmienił funkcję w programie dziennika zadań, kopia w programie testowym zostałaby stara. W [lekcji 13.4: Testy obok programu](lesson_04_tests_next_to_the_program.md) zbudujesz program i jego testy w jednym projekcie, z jednego pliku z testowaną funkcją.

---

## Przykładowe rozwiązania

Zajrzyj tutaj **po własnej próbie**. To jedno z poprawnych rozwiązań. Twoje nazwy, kolejność przypadków i liczba sprawdzeń mogą być inne, jeśli każdy przypadek ma własny strumień i zmienne wynikowe, a sprawdzenia obejmują wszystko, co obiecuje kontrakt.

<details>
<summary>Punkt 10: misja, testy dziennika zadań</summary>

**`main.cpp`** z funkcją z lekcji 12.3 i przypadkami A–M:

<!-- example: chore_tests -->
```cpp
#include <cstddef>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

struct Chore {
    std::string name;
    std::string status;
};

bool read_chores(std::istream& input, std::vector<Chore>& chores, std::string& error, int& error_line) {
    int line_number{0};
    std::string name{};
    std::getline(input, name);

    while (!input.fail()) {
        ++line_number;

        if (name.empty()) {
            error = "empty";
            error_line = line_number;
            return false;
        }

        std::string status{};
        std::getline(input, status);

        if (input.fail()) {
            error = "incomplete";
            error_line = line_number;
            return false;
        }

        ++line_number;

        if (status.empty()) {
            error = "empty";
            error_line = line_number;
            return false;
        }

        if (status != "done" && status != "pending") {
            error = "invalid";
            error_line = line_number;
            return false;
        }

        chores.push_back(Chore{name, status});
        std::getline(input, name);
    }

    return true;
}

std::string bool_text(bool value) {
    if (value) {
        return "true";
    }

    return "false";
}

void check_bool(const std::string& name, bool expected, bool actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << bool_text(expected) << ", actual " << bool_text(actual) << "\n";
        ++failed;
    }
}

void check_int(const std::string& name, int expected, int actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << expected << ", actual " << actual << "\n";
        ++failed;
    }
}

void check_size(const std::string& name, std::size_t expected, std::size_t actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << expected << ", actual " << actual << "\n";
        ++failed;
    }
}

void check_text(const std::string& name, const std::string& expected, const std::string& actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected \"" << expected << "\", actual \"" << actual << "\"\n";
        ++failed;
    }
}

int main() {
    int checks{0};
    int failed{0};

    std::istringstream input_a{""};
    std::vector<Chore> chores_a{};
    std::string error_a{};
    int error_line_a{0};
    const bool complete_a{read_chores(input_a, chores_a, error_a, error_line_a)};
    check_bool("A complete", true, complete_a, checks, failed);
    check_size("A size", 0, chores_a.size(), checks, failed);

    std::istringstream input_b{"Clean tables\ndone\nSort books\npending\n"};
    std::vector<Chore> chores_b{};
    std::string error_b{};
    int error_line_b{0};
    const bool complete_b{read_chores(input_b, chores_b, error_b, error_line_b)};
    check_bool("B complete", true, complete_b, checks, failed);
    check_size("B size", 2, chores_b.size(), checks, failed);

    if (chores_b.size() == 2) {
        check_text("B chores[0].name", "Clean tables", chores_b[0].name, checks, failed);
        check_text("B chores[0].status", "done", chores_b[0].status, checks, failed);
        check_text("B chores[1].name", "Sort books", chores_b[1].name, checks, failed);
        check_text("B chores[1].status", "pending", chores_b[1].status, checks, failed);
    }

    std::istringstream input_c{"Clean tables\ndone"};
    std::vector<Chore> chores_c{};
    std::string error_c{};
    int error_line_c{0};
    const bool complete_c{read_chores(input_c, chores_c, error_c, error_line_c)};
    check_bool("C complete", true, complete_c, checks, failed);
    check_size("C size", 1, chores_c.size(), checks, failed);

    if (chores_c.size() == 1) {
        check_text("C chores[0].name", "Clean tables", chores_c[0].name, checks, failed);
        check_text("C chores[0].status", "done", chores_c[0].status, checks, failed);
    }

    std::istringstream input_d{"\n"};
    std::vector<Chore> chores_d{};
    std::string error_d{};
    int error_line_d{0};
    const bool complete_d{read_chores(input_d, chores_d, error_d, error_line_d)};
    check_bool("D complete", false, complete_d, checks, failed);
    check_text("D error", "empty", error_d, checks, failed);
    check_int("D error_line", 1, error_line_d, checks, failed);

    std::istringstream input_e{"Clean tables\n\n"};
    std::vector<Chore> chores_e{};
    std::string error_e{};
    int error_line_e{0};
    const bool complete_e{read_chores(input_e, chores_e, error_e, error_line_e)};
    check_bool("E complete", false, complete_e, checks, failed);
    check_text("E error", "empty", error_e, checks, failed);
    check_int("E error_line", 2, error_line_e, checks, failed);

    std::istringstream input_f{"Clean tables\nlater\n"};
    std::vector<Chore> chores_f{};
    std::string error_f{};
    int error_line_f{0};
    const bool complete_f{read_chores(input_f, chores_f, error_f, error_line_f)};
    check_bool("F complete", false, complete_f, checks, failed);
    check_text("F error", "invalid", error_f, checks, failed);
    check_int("F error_line", 2, error_line_f, checks, failed);

    std::istringstream input_g{"Clean tables\n"};
    std::vector<Chore> chores_g{};
    std::string error_g{};
    int error_line_g{0};
    const bool complete_g{read_chores(input_g, chores_g, error_g, error_line_g)};
    check_bool("G complete", false, complete_g, checks, failed);
    check_text("G error", "incomplete", error_g, checks, failed);
    check_int("G error_line", 1, error_line_g, checks, failed);

    std::istringstream input_h{"Clean tables\ndone\n\n"};
    std::vector<Chore> chores_h{};
    std::string error_h{};
    int error_line_h{0};
    const bool complete_h{read_chores(input_h, chores_h, error_h, error_line_h)};
    check_bool("H complete", false, complete_h, checks, failed);
    check_text("H error", "empty", error_h, checks, failed);
    check_int("H error_line", 3, error_line_h, checks, failed);

    std::istringstream input_i{"Clean tables\ndone\nSort books\nlater\n"};
    std::vector<Chore> chores_i{};
    std::string error_i{};
    int error_line_i{0};
    const bool complete_i{read_chores(input_i, chores_i, error_i, error_line_i)};
    check_bool("I complete", false, complete_i, checks, failed);
    check_text("I error", "invalid", error_i, checks, failed);
    check_int("I error_line", 4, error_line_i, checks, failed);

    std::istringstream input_j{"Clean tables\ndone\nSort books"};
    std::vector<Chore> chores_j{};
    std::string error_j{};
    int error_line_j{0};
    const bool complete_j{read_chores(input_j, chores_j, error_j, error_line_j)};
    check_bool("J complete", false, complete_j, checks, failed);
    check_text("J error", "incomplete", error_j, checks, failed);
    check_int("J error_line", 3, error_line_j, checks, failed);

    std::istringstream input_k{"Clean tables\ndone\nClean tables\npending"};
    std::vector<Chore> chores_k{};
    std::string error_k{};
    int error_line_k{0};
    const bool complete_k{read_chores(input_k, chores_k, error_k, error_line_k)};
    check_bool("K complete", true, complete_k, checks, failed);
    check_size("K size", 2, chores_k.size(), checks, failed);

    if (chores_k.size() == 2) {
        check_text("K chores[0].name", "Clean tables", chores_k[0].name, checks, failed);
        check_text("K chores[0].status", "done", chores_k[0].status, checks, failed);
        check_text("K chores[1].name", "Clean tables", chores_k[1].name, checks, failed);
        check_text("K chores[1].status", "pending", chores_k[1].status, checks, failed);
    }

    std::istringstream input_l{"Clean tables\ndone \n"};
    std::vector<Chore> chores_l{};
    std::string error_l{};
    int error_line_l{0};
    const bool complete_l{read_chores(input_l, chores_l, error_l, error_line_l)};
    check_bool("L complete", false, complete_l, checks, failed);
    check_text("L error", "invalid", error_l, checks, failed);
    check_int("L error_line", 2, error_line_l, checks, failed);

    std::istringstream input_m{"Clean tables\nlater"};
    std::vector<Chore> chores_m{};
    std::string error_m{};
    int error_line_m{0};
    const bool complete_m{read_chores(input_m, chores_m, error_m, error_line_m)};
    check_bool("M complete", false, complete_m, checks, failed);
    check_text("M error", "invalid", error_m, checks, failed);
    check_int("M error_line", 2, error_line_m, checks, failed);

    std::cout << "Checks: " << checks << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

<!-- output: chore_tests -->
```text
PASS A complete
PASS A size
PASS B complete
PASS B size
PASS B chores[0].name
PASS B chores[0].status
PASS B chores[1].name
PASS B chores[1].status
PASS C complete
PASS C size
PASS C chores[0].name
PASS C chores[0].status
PASS D complete
PASS D error
PASS D error_line
PASS E complete
PASS E error
PASS E error_line
PASS F complete
PASS F error
PASS F error_line
PASS G complete
PASS G error
PASS G error_line
PASS H complete
PASS H error
PASS H error_line
PASS I complete
PASS I error
PASS I error_line
PASS J complete
PASS J error
PASS J error_line
PASS K complete
PASS K size
PASS K chores[0].name
PASS K chores[0].status
PASS K chores[1].name
PASS K chores[1].status
PASS L complete
PASS L error
PASS L error_line
PASS M complete
PASS M error
PASS M error_line
Checks: 45, failed: 0
```

Kod zakończenia: 0.

- **`check_size`** ma parametry typu `std::size_t`, więc rozmiar wektora porównuje się bez mieszania z `int`. Wymaga `#include <cstddef>`.
- **Elementy tylko po zgodnym rozmiarze.** `if (chores_b.size() == 2)` chroni przed odczytem elementu, którego nie ma, gdyby wersja z błędem zwróciła mniej rekordów. Wtedy `FAIL` da już sprawdzenie rozmiaru.
- **Kolejność:** `chores[0]` i `chores[1]` sprawdzane osobno. W K oba rekordy mają tę samą nazwę, więc kolejność widać po statusach.
- **Po błędzie** wektora program nie sprawdza: kontrakt nie obiecuje, co w nim zostanie. W H jest w nim już `Clean tables`. Brak częściowego raportu w programie dziennika wynika z `false`, a to sprawdza `complete`.
- **Inne poprawne rozwiązania:** inny podział na funkcje sprawdzające, na przykład jedna funkcja sprawdzająca cały rekord, albo inne nazwy sprawdzeń. Ważne, żeby każdy przypadek miał własne dane, a każda niezgodność dawała `FAIL` z wartością oczekiwaną i rzeczywistą.

**Stara reguła zakończenia** (piąte obowiązkowe uruchomienie):

<!-- example: chore_tests_old_rule exit=1 -->
```cpp
#include <cstddef>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

struct Chore {
    std::string name;
    std::string status;
};

bool read_chores(std::istream& input, std::vector<Chore>& chores, std::string& error, int& error_line) {
    int line_number{0};
    std::string name{};
    std::getline(input, name);

    while (!input.fail() && !name.empty()) {
        ++line_number;

        std::string status{};
        std::getline(input, status);

        if (input.fail()) {
            error = "incomplete";
            error_line = line_number;
            return false;
        }

        ++line_number;

        if (status.empty()) {
            error = "empty";
            error_line = line_number;
            return false;
        }

        if (status != "done" && status != "pending") {
            error = "invalid";
            error_line = line_number;
            return false;
        }

        chores.push_back(Chore{name, status});
        std::getline(input, name);
    }

    return true;
}

std::string bool_text(bool value) {
    if (value) {
        return "true";
    }

    return "false";
}

void check_bool(const std::string& name, bool expected, bool actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << bool_text(expected) << ", actual " << bool_text(actual) << "\n";
        ++failed;
    }
}

void check_int(const std::string& name, int expected, int actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << expected << ", actual " << actual << "\n";
        ++failed;
    }
}

void check_size(const std::string& name, std::size_t expected, std::size_t actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << expected << ", actual " << actual << "\n";
        ++failed;
    }
}

void check_text(const std::string& name, const std::string& expected, const std::string& actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected \"" << expected << "\", actual \"" << actual << "\"\n";
        ++failed;
    }
}

int main() {
    int checks{0};
    int failed{0};

    std::istringstream input_a{""};
    std::vector<Chore> chores_a{};
    std::string error_a{};
    int error_line_a{0};
    const bool complete_a{read_chores(input_a, chores_a, error_a, error_line_a)};
    check_bool("A complete", true, complete_a, checks, failed);
    check_size("A size", 0, chores_a.size(), checks, failed);

    std::istringstream input_b{"Clean tables\ndone\nSort books\npending\n"};
    std::vector<Chore> chores_b{};
    std::string error_b{};
    int error_line_b{0};
    const bool complete_b{read_chores(input_b, chores_b, error_b, error_line_b)};
    check_bool("B complete", true, complete_b, checks, failed);
    check_size("B size", 2, chores_b.size(), checks, failed);

    if (chores_b.size() == 2) {
        check_text("B chores[0].name", "Clean tables", chores_b[0].name, checks, failed);
        check_text("B chores[0].status", "done", chores_b[0].status, checks, failed);
        check_text("B chores[1].name", "Sort books", chores_b[1].name, checks, failed);
        check_text("B chores[1].status", "pending", chores_b[1].status, checks, failed);
    }

    std::istringstream input_c{"Clean tables\ndone"};
    std::vector<Chore> chores_c{};
    std::string error_c{};
    int error_line_c{0};
    const bool complete_c{read_chores(input_c, chores_c, error_c, error_line_c)};
    check_bool("C complete", true, complete_c, checks, failed);
    check_size("C size", 1, chores_c.size(), checks, failed);

    if (chores_c.size() == 1) {
        check_text("C chores[0].name", "Clean tables", chores_c[0].name, checks, failed);
        check_text("C chores[0].status", "done", chores_c[0].status, checks, failed);
    }

    std::istringstream input_d{"\n"};
    std::vector<Chore> chores_d{};
    std::string error_d{};
    int error_line_d{0};
    const bool complete_d{read_chores(input_d, chores_d, error_d, error_line_d)};
    check_bool("D complete", false, complete_d, checks, failed);
    check_text("D error", "empty", error_d, checks, failed);
    check_int("D error_line", 1, error_line_d, checks, failed);

    std::istringstream input_e{"Clean tables\n\n"};
    std::vector<Chore> chores_e{};
    std::string error_e{};
    int error_line_e{0};
    const bool complete_e{read_chores(input_e, chores_e, error_e, error_line_e)};
    check_bool("E complete", false, complete_e, checks, failed);
    check_text("E error", "empty", error_e, checks, failed);
    check_int("E error_line", 2, error_line_e, checks, failed);

    std::istringstream input_f{"Clean tables\nlater\n"};
    std::vector<Chore> chores_f{};
    std::string error_f{};
    int error_line_f{0};
    const bool complete_f{read_chores(input_f, chores_f, error_f, error_line_f)};
    check_bool("F complete", false, complete_f, checks, failed);
    check_text("F error", "invalid", error_f, checks, failed);
    check_int("F error_line", 2, error_line_f, checks, failed);

    std::istringstream input_g{"Clean tables\n"};
    std::vector<Chore> chores_g{};
    std::string error_g{};
    int error_line_g{0};
    const bool complete_g{read_chores(input_g, chores_g, error_g, error_line_g)};
    check_bool("G complete", false, complete_g, checks, failed);
    check_text("G error", "incomplete", error_g, checks, failed);
    check_int("G error_line", 1, error_line_g, checks, failed);

    std::istringstream input_h{"Clean tables\ndone\n\n"};
    std::vector<Chore> chores_h{};
    std::string error_h{};
    int error_line_h{0};
    const bool complete_h{read_chores(input_h, chores_h, error_h, error_line_h)};
    check_bool("H complete", false, complete_h, checks, failed);
    check_text("H error", "empty", error_h, checks, failed);
    check_int("H error_line", 3, error_line_h, checks, failed);

    std::istringstream input_i{"Clean tables\ndone\nSort books\nlater\n"};
    std::vector<Chore> chores_i{};
    std::string error_i{};
    int error_line_i{0};
    const bool complete_i{read_chores(input_i, chores_i, error_i, error_line_i)};
    check_bool("I complete", false, complete_i, checks, failed);
    check_text("I error", "invalid", error_i, checks, failed);
    check_int("I error_line", 4, error_line_i, checks, failed);

    std::istringstream input_j{"Clean tables\ndone\nSort books"};
    std::vector<Chore> chores_j{};
    std::string error_j{};
    int error_line_j{0};
    const bool complete_j{read_chores(input_j, chores_j, error_j, error_line_j)};
    check_bool("J complete", false, complete_j, checks, failed);
    check_text("J error", "incomplete", error_j, checks, failed);
    check_int("J error_line", 3, error_line_j, checks, failed);

    std::istringstream input_k{"Clean tables\ndone\nClean tables\npending"};
    std::vector<Chore> chores_k{};
    std::string error_k{};
    int error_line_k{0};
    const bool complete_k{read_chores(input_k, chores_k, error_k, error_line_k)};
    check_bool("K complete", true, complete_k, checks, failed);
    check_size("K size", 2, chores_k.size(), checks, failed);

    if (chores_k.size() == 2) {
        check_text("K chores[0].name", "Clean tables", chores_k[0].name, checks, failed);
        check_text("K chores[0].status", "done", chores_k[0].status, checks, failed);
        check_text("K chores[1].name", "Clean tables", chores_k[1].name, checks, failed);
        check_text("K chores[1].status", "pending", chores_k[1].status, checks, failed);
    }

    std::istringstream input_l{"Clean tables\ndone \n"};
    std::vector<Chore> chores_l{};
    std::string error_l{};
    int error_line_l{0};
    const bool complete_l{read_chores(input_l, chores_l, error_l, error_line_l)};
    check_bool("L complete", false, complete_l, checks, failed);
    check_text("L error", "invalid", error_l, checks, failed);
    check_int("L error_line", 2, error_line_l, checks, failed);

    std::istringstream input_m{"Clean tables\nlater"};
    std::vector<Chore> chores_m{};
    std::string error_m{};
    int error_line_m{0};
    const bool complete_m{read_chores(input_m, chores_m, error_m, error_line_m)};
    check_bool("M complete", false, complete_m, checks, failed);
    check_text("M error", "invalid", error_m, checks, failed);
    check_int("M error_line", 2, error_line_m, checks, failed);

    std::cout << "Checks: " << checks << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

<!-- output: chore_tests_old_rule -->
```text
PASS A complete
PASS A size
PASS B complete
PASS B size
PASS B chores[0].name
PASS B chores[0].status
PASS B chores[1].name
PASS B chores[1].status
PASS C complete
PASS C size
PASS C chores[0].name
PASS C chores[0].status
FAIL D complete: expected false, actual true
FAIL D error: expected "empty", actual ""
FAIL D error_line: expected 1, actual 0
PASS E complete
PASS E error
PASS E error_line
PASS F complete
PASS F error
PASS F error_line
PASS G complete
PASS G error
PASS G error_line
FAIL H complete: expected false, actual true
FAIL H error: expected "empty", actual ""
FAIL H error_line: expected 3, actual 0
PASS I complete
PASS I error
PASS I error_line
PASS J complete
PASS J error
PASS J error_line
PASS K complete
PASS K size
PASS K chores[0].name
PASS K chores[0].status
PASS K chores[1].name
PASS K chores[1].status
PASS L complete
PASS L error
PASS L error_line
PASS M complete
PASS M error
PASS M error_line
Checks: 45, failed: 6
```

Kod zakończenia: 1.

**Licznik zwiększony przed sprawdzeniem odczytu statusu:** `++line_number;` stoi zaraz po `std::getline(input, status);`, przed `if (input.fail())`. To pomyłka, przed którą przestrzegała lekcja 12.3, punkt 4.

<!-- example: chore_tests_counter_bug exit=1 -->
```cpp
#include <cstddef>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

struct Chore {
    std::string name;
    std::string status;
};

bool read_chores(std::istream& input, std::vector<Chore>& chores, std::string& error, int& error_line) {
    int line_number{0};
    std::string name{};
    std::getline(input, name);

    while (!input.fail()) {
        ++line_number;

        if (name.empty()) {
            error = "empty";
            error_line = line_number;
            return false;
        }

        std::string status{};
        std::getline(input, status);
        ++line_number;

        if (input.fail()) {
            error = "incomplete";
            error_line = line_number;
            return false;
        }

        if (status.empty()) {
            error = "empty";
            error_line = line_number;
            return false;
        }

        if (status != "done" && status != "pending") {
            error = "invalid";
            error_line = line_number;
            return false;
        }

        chores.push_back(Chore{name, status});
        std::getline(input, name);
    }

    return true;
}

std::string bool_text(bool value) {
    if (value) {
        return "true";
    }

    return "false";
}

void check_bool(const std::string& name, bool expected, bool actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << bool_text(expected) << ", actual " << bool_text(actual) << "\n";
        ++failed;
    }
}

void check_int(const std::string& name, int expected, int actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << expected << ", actual " << actual << "\n";
        ++failed;
    }
}

void check_size(const std::string& name, std::size_t expected, std::size_t actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << expected << ", actual " << actual << "\n";
        ++failed;
    }
}

void check_text(const std::string& name, const std::string& expected, const std::string& actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected \"" << expected << "\", actual \"" << actual << "\"\n";
        ++failed;
    }
}

int main() {
    int checks{0};
    int failed{0};

    std::istringstream input_a{""};
    std::vector<Chore> chores_a{};
    std::string error_a{};
    int error_line_a{0};
    const bool complete_a{read_chores(input_a, chores_a, error_a, error_line_a)};
    check_bool("A complete", true, complete_a, checks, failed);
    check_size("A size", 0, chores_a.size(), checks, failed);

    std::istringstream input_b{"Clean tables\ndone\nSort books\npending\n"};
    std::vector<Chore> chores_b{};
    std::string error_b{};
    int error_line_b{0};
    const bool complete_b{read_chores(input_b, chores_b, error_b, error_line_b)};
    check_bool("B complete", true, complete_b, checks, failed);
    check_size("B size", 2, chores_b.size(), checks, failed);

    if (chores_b.size() == 2) {
        check_text("B chores[0].name", "Clean tables", chores_b[0].name, checks, failed);
        check_text("B chores[0].status", "done", chores_b[0].status, checks, failed);
        check_text("B chores[1].name", "Sort books", chores_b[1].name, checks, failed);
        check_text("B chores[1].status", "pending", chores_b[1].status, checks, failed);
    }

    std::istringstream input_c{"Clean tables\ndone"};
    std::vector<Chore> chores_c{};
    std::string error_c{};
    int error_line_c{0};
    const bool complete_c{read_chores(input_c, chores_c, error_c, error_line_c)};
    check_bool("C complete", true, complete_c, checks, failed);
    check_size("C size", 1, chores_c.size(), checks, failed);

    if (chores_c.size() == 1) {
        check_text("C chores[0].name", "Clean tables", chores_c[0].name, checks, failed);
        check_text("C chores[0].status", "done", chores_c[0].status, checks, failed);
    }

    std::istringstream input_d{"\n"};
    std::vector<Chore> chores_d{};
    std::string error_d{};
    int error_line_d{0};
    const bool complete_d{read_chores(input_d, chores_d, error_d, error_line_d)};
    check_bool("D complete", false, complete_d, checks, failed);
    check_text("D error", "empty", error_d, checks, failed);
    check_int("D error_line", 1, error_line_d, checks, failed);

    std::istringstream input_e{"Clean tables\n\n"};
    std::vector<Chore> chores_e{};
    std::string error_e{};
    int error_line_e{0};
    const bool complete_e{read_chores(input_e, chores_e, error_e, error_line_e)};
    check_bool("E complete", false, complete_e, checks, failed);
    check_text("E error", "empty", error_e, checks, failed);
    check_int("E error_line", 2, error_line_e, checks, failed);

    std::istringstream input_f{"Clean tables\nlater\n"};
    std::vector<Chore> chores_f{};
    std::string error_f{};
    int error_line_f{0};
    const bool complete_f{read_chores(input_f, chores_f, error_f, error_line_f)};
    check_bool("F complete", false, complete_f, checks, failed);
    check_text("F error", "invalid", error_f, checks, failed);
    check_int("F error_line", 2, error_line_f, checks, failed);

    std::istringstream input_g{"Clean tables\n"};
    std::vector<Chore> chores_g{};
    std::string error_g{};
    int error_line_g{0};
    const bool complete_g{read_chores(input_g, chores_g, error_g, error_line_g)};
    check_bool("G complete", false, complete_g, checks, failed);
    check_text("G error", "incomplete", error_g, checks, failed);
    check_int("G error_line", 1, error_line_g, checks, failed);

    std::istringstream input_h{"Clean tables\ndone\n\n"};
    std::vector<Chore> chores_h{};
    std::string error_h{};
    int error_line_h{0};
    const bool complete_h{read_chores(input_h, chores_h, error_h, error_line_h)};
    check_bool("H complete", false, complete_h, checks, failed);
    check_text("H error", "empty", error_h, checks, failed);
    check_int("H error_line", 3, error_line_h, checks, failed);

    std::istringstream input_i{"Clean tables\ndone\nSort books\nlater\n"};
    std::vector<Chore> chores_i{};
    std::string error_i{};
    int error_line_i{0};
    const bool complete_i{read_chores(input_i, chores_i, error_i, error_line_i)};
    check_bool("I complete", false, complete_i, checks, failed);
    check_text("I error", "invalid", error_i, checks, failed);
    check_int("I error_line", 4, error_line_i, checks, failed);

    std::istringstream input_j{"Clean tables\ndone\nSort books"};
    std::vector<Chore> chores_j{};
    std::string error_j{};
    int error_line_j{0};
    const bool complete_j{read_chores(input_j, chores_j, error_j, error_line_j)};
    check_bool("J complete", false, complete_j, checks, failed);
    check_text("J error", "incomplete", error_j, checks, failed);
    check_int("J error_line", 3, error_line_j, checks, failed);

    std::istringstream input_k{"Clean tables\ndone\nClean tables\npending"};
    std::vector<Chore> chores_k{};
    std::string error_k{};
    int error_line_k{0};
    const bool complete_k{read_chores(input_k, chores_k, error_k, error_line_k)};
    check_bool("K complete", true, complete_k, checks, failed);
    check_size("K size", 2, chores_k.size(), checks, failed);

    if (chores_k.size() == 2) {
        check_text("K chores[0].name", "Clean tables", chores_k[0].name, checks, failed);
        check_text("K chores[0].status", "done", chores_k[0].status, checks, failed);
        check_text("K chores[1].name", "Clean tables", chores_k[1].name, checks, failed);
        check_text("K chores[1].status", "pending", chores_k[1].status, checks, failed);
    }

    std::istringstream input_l{"Clean tables\ndone \n"};
    std::vector<Chore> chores_l{};
    std::string error_l{};
    int error_line_l{0};
    const bool complete_l{read_chores(input_l, chores_l, error_l, error_line_l)};
    check_bool("L complete", false, complete_l, checks, failed);
    check_text("L error", "invalid", error_l, checks, failed);
    check_int("L error_line", 2, error_line_l, checks, failed);

    std::istringstream input_m{"Clean tables\nlater"};
    std::vector<Chore> chores_m{};
    std::string error_m{};
    int error_line_m{0};
    const bool complete_m{read_chores(input_m, chores_m, error_m, error_line_m)};
    check_bool("M complete", false, complete_m, checks, failed);
    check_text("M error", "invalid", error_m, checks, failed);
    check_int("M error_line", 2, error_line_m, checks, failed);

    std::cout << "Checks: " << checks << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

<!-- output: chore_tests_counter_bug -->
```text
PASS A complete
PASS A size
PASS B complete
PASS B size
PASS B chores[0].name
PASS B chores[0].status
PASS B chores[1].name
PASS B chores[1].status
PASS C complete
PASS C size
PASS C chores[0].name
PASS C chores[0].status
PASS D complete
PASS D error
PASS D error_line
PASS E complete
PASS E error
PASS E error_line
PASS F complete
PASS F error
PASS F error_line
PASS G complete
PASS G error
FAIL G error_line: expected 1, actual 2
PASS H complete
PASS H error
PASS H error_line
PASS I complete
PASS I error
PASS I error_line
PASS J complete
PASS J error
FAIL J error_line: expected 3, actual 4
PASS K complete
PASS K size
PASS K chores[0].name
PASS K chores[0].status
PASS K chores[1].name
PASS K chores[1].status
PASS L complete
PASS L error
PASS L error_line
PASS M complete
PASS M error
PASS M error_line
Checks: 45, failed: 2
```

Kod zakończenia: 1.

| Usterka | Przypadki ujawniające | Sprawdzenia z `FAIL` | Niepowodzenia | Kod |
|---|---|---|---|---|
| stara reguła zakończenia | D, H | `complete`, `error`, `error_line` w obu | 6 | 1 |
| licznik przed sprawdzeniem odczytu statusu | G, J | tylko `error_line` w obu | 2 | 1 |

- **Stara reguła** zmienia wynik tylko wtedy, gdy pusta linia stoi w miejscu nazwy: D na początku danych, H po kompletnym rekordzie. E ma pustą linię w miejscu statusu, a tę funkcja nadal wykrywa.
- **Licznik** zmienia wynik tylko przy niekompletnym rekordzie, bo tylko wtedy odczyt statusu się nie udaje. W G i J `complete` i `error` dają `PASS`: tylko sprawdzenie numeru linii odróżnia tę wersję od poprawnej. Test, który nie sprawdza `error_line`, nie wykryłby tej usterki.
- **A i D:** pusty tekst to poprawny koniec danych, a jedna pusta linia to błąd. Gdyby zestaw miał tylko A, stara reguła by przeszła.
- Każdy program z usterką kończy się kodem 1, bo licznik niepowodzeń jest większy od zera, a z poprawną funkcją ten sam zestaw daje kod 0.

**Przykładowe uzasadnienia z kroku 6:**

- **C** wykryłby funkcję, która po odczycie statusu sprawdza `eof()` zamiast `fail()`: ostatni status bez znaku końca linii uznałaby za brakujący.
- **D** wykrywa starą regułę zakończenia: pusta linia w miejscu pierwszej nazwy kończyłaby dane bez błędu.
- **H** wykrywa tę samą regułę po kompletnym rekordzie, czyli sytuację z lekcji 12.3, w której część danych znikała bez komunikatu.
- **J** wykrywa licznik zwiększony po nieudanym odczycie: numer wskazywałby linię 4, której w danych nie ma.

</details>

**Poprzednia lekcja:** [Lekcja 13.2: Przypadki, które wykrywają błędy](lesson_02_test_cases_that_catch_bugs.md) · **Następna lekcja:** [Lekcja 13.4: Testy obok programu](lesson_04_tests_next_to_the_program.md) · [Opis kursu](../../README.md)

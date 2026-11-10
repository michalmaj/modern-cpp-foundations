# Lekcja 14.1: Stan z nazwą zamiast tekstu

**Polski** · [English](lesson_01_named_state_instead_of_text.en.md) · [Opis kursu](../../README.md)

> **Moduł 14, lekcja 1** · około 75–90 minut, można ją podzielić na dwa podejścia (punkty 1–8, potem misja)
> **Potrzebujesz:** katalogu `cpp-workspace` i oryginalnego projektu `lesson_05_first_program`, jak dotąd. Debugger nie jest w tej lekcji potrzebny.
> **Wersja pilotażowa.** Programy z tej lekcji sprawdzamy automatycznie na Windowsie, Ubuntu i macOS, razem z ich kodem zakończenia. Programy, które nie mają się zbudować, sprawdzamy razem z miejscem pierwszego błędu.

## Zanim zaczniesz

Ta lekcja zakłada, że:

- porównujesz wartości przez `==` i `!=`, także teksty (lekcje 3.2 i 3.4);
- piszesz funkcje `bool`, także takie, które od razu zwracają wynik porównania, na przykład `return count >= 1 && count <= 24;` (lekcje 5.3–5.5);
- definiujesz własny typ przez `struct` i używasz go w funkcjach (lekcje 8.1 i 8.3);
- piszesz funkcję `bool`, która zmienia parametr wynikowy `T&` dopiero po sprawdzeniu, a przy odmowie zostawia go bez zmian (lekcje 9.2 i 10.4);
- piszesz jednoplikowe programy testowe z funkcjami `check_bool` i `check_text`, które kończą się kodem 1, gdy któreś sprawdzenie się nie uda (lekcje 13.1–13.3).

## Sytuacja

Sklep internetowy śledzi zamówienia. Każde jest w jednym z trzech stanów: przyjęte, w przygotowaniu albo wysłane. Dotąd taki stan zapisywaliśmy jako tekst, tak jak pole `status` w seansach kina z lekcji 12.4: `"received"`, `"preparing"`, `"sent"`.

Tekst ma jedną wadę: **każdy napis jest poprawnym tekstem**. Jeśli w jednym miejscu programu ktoś napisze `"preparingg"` zamiast `"preparing"`, kompilator nie ma czego zgłosić. Program się zbuduje, uruchomi i będzie działał źle. W tej lekcji odpowiesz na pytanie: **czy da się zapisać stan tak, żeby dozwolone były tylko trzy nazwy, a literówkę w nazwie wykrywał kompilator?**

Po tej lekcji będziesz:

- rozpoznawać problem stanów zapisanych jako dowolne napisy;
- definiować typ wyliczeniowy `enum class` z zamkniętym zestawem nazwanych stanów;
- tworzyć zmienne tego typu, porównywać stany przez `==` i `!=`, przekazywać je do funkcji i zwracać z funkcji;
- zamieniać stan na tekst do wypisania i rozpoznawać stan z tekstu w dwóch osobnych funkcjach;
- odmawiać rozpoznania nieznanej nazwy bez zmiany wyniku;
- odróżniać literówkę w nazwie stanu, którą wykrywa kompilator, od błędu, który wykrywają dopiero testy.

## 1. Stan zapisany jako tekst

Magazyn pakuje zamówienia, które są w przygotowaniu. Ten program sprawdza stan zamówienia i decyduje, czy trzeba je spakować:

<!-- example: order_text -->
```cpp
#include <iostream>
#include <string>

bool needs_packing(const std::string& status) {
    return status == "preparingg";
}

int main() {
    std::string status{"preparing"};

    if (needs_packing(status)) {
        std::cout << "Pack the order\n";
    } else {
        std::cout << "Nothing to pack\n";
    }
}
```

**Przewidź**, co wypisze. Zamówienie jest w przygotowaniu, więc powinno zostać spakowane. Program wypisuje jednak:

<!-- output: order_text -->
```text
Nothing to pack
```

W funkcji `needs_packing` jest literówka: `"preparingg"`, z dwiema literami `g`. Kompilator jej nie zgłasza i ma rację, bo `"preparingg"` to zupełnie poprawny tekst. Porównanie dwóch różnych tekstów daje po prostu `false`. Błąd zobaczy dopiero ktoś, kto uruchomi program i zauważy zły wynik, albo test, który sprawdzi `needs_packing` dla zamówienia w przygotowaniu.

Ten program nie jest obowiązkowy do uruchomienia: sprawdzamy go automatycznie, a jego wynik widzisz powyżej.

**Gdzie jest problem:** typ `std::string` przyjmuje każdy napis. Program zna tylko trzy stany zamówienia, ale typ zmiennej `status` o tym nie wie. Umowa „dozwolone są tylko trzy napisy” istnieje wyłącznie w głowach osób, które piszą kod.

## 2. Typ wyliczeniowy: `enum class`

C++ pozwala zdefiniować typ, który ma **zamknięty zestaw nazwanych wartości**:

<!-- fragment -->
```cpp
enum class OrderStatus {
    received,
    preparing,
    sent
};
```

- `enum class` to dwa słowa kluczowe, które razem rozpoczynają definicję **typu wyliczeniowego** (*enumeration type*). Taki typ wylicza wszystkie swoje dozwolone wartości.
- `OrderStatus` to **nazwa typu**. Piszemy ją tak jak nazwy struktur z Modułu 8, wielką literą na początku każdego słowa.
- `received`, `preparing` i `sent` to **nazwy wartości** tego typu, czyli **wartości wyliczenia** (*enumerators*). Oddzielają je przecinki. Innych wartości ten typ nie ma.
- Po klamrze zamykającej stoi średnik, jak po definicji `struct`.
- Definicja stoi nad funkcjami, które z tego typu korzystają, tak jak definicja struktury.

**To nie są napisy.** `received` nie ma cudzysłowów, bo nie jest tekstem. To nazwa wartości, tak jak `count` jest nazwą zmiennej. Każdy stan zamówienia jest teraz **wartością typu `OrderStatus`**, a nie umownym słowem.

C++ ma też starszą postać tej konstrukcji, samo `enum`, bez `class`. W tym kursie używamy `enum class`, bo nazwę jego wartości zawsze piszemy razem z nazwą typu. Dzięki temu dwa różne typy mogą mieć wartość o tej samej nazwie, a kompilator nie pozwoli pomylić stanu jednego typu ze stanem drugiego.

## 3. Zmienna z nazwanym stanem

Zmienną typu `OrderStatus` tworzysz tak jak każdą inną:

<!-- fragment -->
```cpp
OrderStatus status{OrderStatus::preparing};
```

- `OrderStatus` przed nazwą zmiennej to jej typ, jak `int` albo `std::string`.
- `OrderStatus::preparing` wskazuje **konkretną wartość**: wartość `preparing` z typu `OrderStatus`. Znak `::` znasz z `std::cout`: tam oznacza nazwę `cout` z biblioteki standardowej `std`, tu nazwę `preparing` z typu `OrderStatus`.
- Sama nazwa `preparing`, bez `OrderStatus::`, nie zadziała. Wartości `enum class` zawsze podajesz razem z typem.

Stan zmienia się zwykłym przypisaniem:

<!-- fragment -->
```cpp
status = OrderStatus::sent;
```

Do zmiennej typu `OrderStatus` można przypisać tylko wartość typu `OrderStatus`. Napis `"sent"` to tekst, a nie stan zamówienia, więc `status = "sent";` się nie zbuduje.

**Nazwy typu i wartości sprawdza kompilator.** Jeśli napiszesz `OrderStatus::sendt`, kompilator nie znajdzie takiej wartości w typie `OrderStatus` i zgłosi błąd, zanim program w ogóle powstanie. Właśnie tego brakowało w punkcie 1.

## 4. Porównywanie stanów

Pytanie „czy zamówienie zostało już wysłane?” to funkcja `bool`:

<!-- fragment -->
```cpp
bool was_sent(OrderStatus status) {
    return status == OrderStatus::sent;
}
```

- Parametr typu `OrderStatus` przekazujesz przez wartość, jak `int`: to mała wartość, a funkcja jej nie zmienia.
- `==` porównuje dwa stany: daje `true`, gdy to ta sama wartość wyliczenia. `!=` daje `true`, gdy wartości są różne.
- Funkcja zwraca wynik porównania od razu, jak funkcje z lekcji 5.5.

Pełny program:

<!-- example: order_states -->
```cpp
#include <iostream>

enum class OrderStatus {
    received,
    preparing,
    sent
};

bool was_sent(OrderStatus status) {
    return status == OrderStatus::sent;
}

int main() {
    OrderStatus status{OrderStatus::received};

    if (status != OrderStatus::sent) {
        std::cout << "Order not sent yet\n";
    }

    status = OrderStatus::sent;

    if (was_sent(status)) {
        std::cout << "Order sent\n";
    }
}
```

**To pierwsze obowiązkowe uruchomienie.** W `cpp-workspace` utwórz katalog `lesson_14_1`, skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program` i otwórz go w CLionie. Zastąp zawartość `main.cpp` tym programem, zbuduj go i uruchom. `CMakeLists.txt` zostaw bez zmian. Kolejne programy z tej lekcji wpisujesz w ten sam `main.cpp`.

<details>
<summary>Standardowe wyjście</summary>

<!-- output: order_states -->
```text
Order not sent yet
Order sent
```

</details>

**Jedna nazwa na jeden stan.** Gdy stan był tekstem, wysłane zamówienie mogło być w jednym miejscu programu `"sent"`, w innym `"shipped"`, a w jeszcze innym `"dispatched"`. Każdy z tych napisów jest poprawny, a porównania między nimi dają `false`. Teraz wysłane zamówienie to zawsze `OrderStatus::sent`, bo innej nazwy dla tego stanu typ nie ma.

`enum class` nie rozwiązuje jednak wszystkiego. Funkcja, która przez pomyłkę porównuje stan z `OrderStatus::received` zamiast z `OrderStatus::sent`, zbuduje się bez żadnego ostrzeżenia. Obie nazwy istnieją, więc kompilator nie ma czego zgłosić. Taki błąd wykrywa dopiero test.

## 5. Stan to nie tekst: zamiana na napis

Program ma wypisać stan zamówienia. Najprostszy pomysł, wypisanie zmiennej przez `std::cout`, nie działa:

<!-- broken: order_print at=11:15 error=^invalid operands to binary expression -->
```cpp
#include <iostream>

enum class OrderStatus {
    received,
    preparing,
    sent
};

int main() {
    OrderStatus status{OrderStatus::preparing};
    std::cout << status << "\n";
}
```

Ten program się nie zbuduje. Nie musisz go budować: jak program z punktu 1, sprawdzamy go automatycznie, a jego wynik znasz z opisu. Kompilator zgłasza błąd w linijce 11, przy `<<`. Jego komunikat zaczyna się od `invalid operands to binary expression`: nie ma działania `<<`, które wypisuje wartość typu `OrderStatus`. Pod tym komunikatem kompilator może wypisać długą listę uwag `note:` o innych typach, które da się wypisać. Wystarczy przeczytać pierwszą linijkę błędu.

To nie przeoczenie. **Stan jest wartością typu, a tekst jest jego reprezentacją.** Jak ma wyglądać ten tekst, decyduje program: może to być `sent`, `Wysłane` albo `SENT`. Dlatego zamianę stanu na tekst zapisujesz jawnie, w osobnej funkcji:

<!-- fragment -->
```cpp
std::string status_text(OrderStatus status) {
    if (status == OrderStatus::received) {
        return "received";
    }

    if (status == OrderStatus::preparing) {
        return "preparing";
    }

    if (status == OrderStatus::sent) {
        return "sent";
    }

    return "unknown";
}
```

| Stan | Tekst zwracany przez `status_text` |
|---|---|
| `OrderStatus::received` | `"received"` |
| `OrderStatus::preparing` | `"preparing"` |
| `OrderStatus::sent` | `"sent"` |

- Każdy stan ma własny warunek i własny `return`, jak funkcje z kilkoma `return` z lekcji 5.4.
- **Ostatnia linijka, `return "unknown";`, to zachowanie zapasowe.** Dla trzech zdefiniowanych stanów się nie wykona, bo każdy z nich kończy funkcję wcześniej. Jest jednak potrzebna. Funkcja, która obiecuje wynik, musi go zwrócić na każdej drodze (lekcja 5.4), a kompilator nie uznaje trzech osobnych warunków za komplet. Bez tej linijki zgłosi, że funkcja nie zwraca wartości we wszystkich ścieżkach.
- **Co by się stało, gdyby ktoś dopisał do typu czwarty stan**, a tej funkcji nie uzupełnił? Dla nowego stanu funkcja zwróci `unknown`. Typ nie chroni więc przed każdym przeoczeniem. Test, który sprawdza tekst każdego stanu, takie przeoczenie wykryje.

Teraz wypisanie stanu wygląda tak: `std::cout << status_text(status) << "\n";`.

## 6. Tekst na stan: funkcja rozpoznająca

Czasem trzeba pójść w drugą stronę: dostajesz tekst, na przykład z pliku albo od użytkownika, i chcesz wiedzieć, który to stan. **`enum class` nie zamienia tekstu na stan samodzielnie.** Tę zamianę też piszesz jako funkcję, a funkcja decyduje, które napisy uznaje za nazwy stanów:

<!-- fragment -->
```cpp
bool parse_status(const std::string& text, OrderStatus& result) {
    if (text == "received") {
        result = OrderStatus::received;
        return true;
    }

    if (text == "preparing") {
        result = OrderStatus::preparing;
        return true;
    }

    if (text == "sent") {
        result = OrderStatus::sent;
        return true;
    }

    return false;
}
```

**Kontrakt `parse_status`:**

| Tekst | Wynik funkcji | `result` po wywołaniu |
|---|---|---|
| `"received"` | `true` | `OrderStatus::received` |
| `"preparing"` | `true` | `OrderStatus::preparing` |
| `"sent"` | `true` | `OrderStatus::sent` |
| każdy inny, na przykład `"preparring"`, `""` albo `"Sent"` | `false` | **bez zmian** |

- To **rozpoznawanie stanu z tekstu** (*parsing a state from text*). Interfejs znasz z lekcji 10.4: `bool` mówi, czy się udało, a wynik trafia do parametru wynikowego `OrderStatus& result`.
- **Nieznana nazwa stanu nie zmienia wyniku.** Funkcja przypisuje `result` dopiero wtedy, gdy rozpozna nazwę. Każda odmowa to `return false;` bez przypisania, więc wywołujący dostaje swój stan w niezmienionej postaci. To ta sama zasada „wszystko albo nic” co w lekcjach 9.2 i 10.4.
- **Wielkość liter ma znaczenie.** `"Sent"` to inny tekst niż `"sent"`, więc funkcja go odrzuca. Tak mówi kontrakt.
- Tekst może pochodzić z dowolnego miejsca programu. W tej lekcji podajesz go wprost w kodzie, żeby sprawdzić samą zamianę.

## 7. Program testowy dla stanu zamówienia

Trzy funkcje z punktów 4–6 sprawdzisz programem testowym, jak w Module 13. `check_bool` i `check_text` znasz z lekcji 13.2 i 13.3. Nowa jest tylko `check_status`, która porównuje dwa stany:

<!-- fragment -->
```cpp
void check_status(const std::string& name, OrderStatus expected, OrderStatus actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << status_text(expected) << ", actual " << status_text(actual) << "\n";
        ++failed;
    }
}
```

Stany porównuje przez `==`. Do wypisania linijki `FAIL` potrzebuje jednak tekstu, więc korzysta z `status_text`. To ta sama zasada co w punkcie 5: stan to wartość, a do wypisania zamieniasz go na tekst.

**Przypadki dla `parse_status`**, wyniki oczekiwane z kontraktu z punktu 6:

| Przypadek | Tekst | `result` przed wywołaniem | Wynik oczekiwany | `result` po wywołaniu | Dlaczego ten przypadek |
|---|---|---|---|---|---|
| A | `"received"` | `sent` | `true` | `received` | znana nazwa |
| B | `"preparing"` | `received` | `true` | `preparing` | znana nazwa |
| C | `"sent"` | `received` | `true` | `sent` | znana nazwa |
| D | `"preparring"` | `preparing` | `false` | `preparing`, bez zmian | literówka w nazwie |
| E | `""` | `received` | `false` | `received`, bez zmian | pusty tekst |

**Dlaczego `result` zaczyna od innego stanu niż oczekiwany?** W przypadku A wynik oczekiwany to `received`, więc `result` zaczyna od `sent`. Gdyby zaczynał od `received`, test przeszedłby także dla błędnej funkcji, która w ogóle nie przypisuje wyniku. W przypadkach D i E jest odwrotnie: sprawdzasz, że stan sprzed wywołania został.

Każdy przypadek ma własną zmienną wynikową, jak każdy przypadek w lekcji 13.3 miał własny strumień i rekord. Funkcje `was_sent` i `status_text` sprawdzasz dla każdego z trzech stanów.

**To drugie obowiązkowe uruchomienie.** Zastąp zawartość `main.cpp` pełnym programem testowym poniżej. Funkcje sprawdzające możesz skopiować z lekcji 13.2 i 13.3, a funkcje stanu z punktów 4–6. **Przewidź**, ile będzie sprawdzeń, zanim uruchomisz program.

<details>
<summary>Pełny program testowy</summary>

<!-- example: order_status_tests -->
```cpp
#include <iostream>
#include <string>

enum class OrderStatus {
    received,
    preparing,
    sent
};

bool was_sent(OrderStatus status) {
    return status == OrderStatus::sent;
}

std::string status_text(OrderStatus status) {
    if (status == OrderStatus::received) {
        return "received";
    }

    if (status == OrderStatus::preparing) {
        return "preparing";
    }

    if (status == OrderStatus::sent) {
        return "sent";
    }

    return "unknown";
}

bool parse_status(const std::string& text, OrderStatus& result) {
    if (text == "received") {
        result = OrderStatus::received;
        return true;
    }

    if (text == "preparing") {
        result = OrderStatus::preparing;
        return true;
    }

    if (text == "sent") {
        result = OrderStatus::sent;
        return true;
    }

    return false;
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

void check_text(const std::string& name, const std::string& expected, const std::string& actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected \"" << expected << "\", actual \"" << actual << "\"\n";
        ++failed;
    }
}

void check_status(const std::string& name, OrderStatus expected, OrderStatus actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << status_text(expected) << ", actual " << status_text(actual) << "\n";
        ++failed;
    }
}

int main() {
    int checks{0};
    int failed{0};

    check_bool("was_sent(received)", false, was_sent(OrderStatus::received), checks, failed);
    check_bool("was_sent(preparing)", false, was_sent(OrderStatus::preparing), checks, failed);
    check_bool("was_sent(sent)", true, was_sent(OrderStatus::sent), checks, failed);

    check_text("status_text(received)", "received", status_text(OrderStatus::received), checks, failed);
    check_text("status_text(preparing)", "preparing", status_text(OrderStatus::preparing), checks, failed);
    check_text("status_text(sent)", "sent", status_text(OrderStatus::sent), checks, failed);

    OrderStatus result_a{OrderStatus::sent};
    const bool accepted_a{parse_status("received", result_a)};
    check_bool("A accepted", true, accepted_a, checks, failed);
    check_status("A result", OrderStatus::received, result_a, checks, failed);

    OrderStatus result_b{OrderStatus::received};
    const bool accepted_b{parse_status("preparing", result_b)};
    check_bool("B accepted", true, accepted_b, checks, failed);
    check_status("B result", OrderStatus::preparing, result_b, checks, failed);

    OrderStatus result_c{OrderStatus::received};
    const bool accepted_c{parse_status("sent", result_c)};
    check_bool("C accepted", true, accepted_c, checks, failed);
    check_status("C result", OrderStatus::sent, result_c, checks, failed);

    OrderStatus result_d{OrderStatus::preparing};
    const bool accepted_d{parse_status("preparring", result_d)};
    check_bool("D accepted", false, accepted_d, checks, failed);
    check_status("D result", OrderStatus::preparing, result_d, checks, failed);

    OrderStatus result_e{OrderStatus::received};
    const bool accepted_e{parse_status("", result_e)};
    check_bool("E accepted", false, accepted_e, checks, failed);
    check_status("E result", OrderStatus::received, result_e, checks, failed);

    std::cout << "Checks: " << checks << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

</details>

<details>
<summary>Standardowe wyjście</summary>

<!-- output: order_status_tests -->
```text
PASS was_sent(received)
PASS was_sent(preparing)
PASS was_sent(sent)
PASS status_text(received)
PASS status_text(preparing)
PASS status_text(sent)
PASS A accepted
PASS A result
PASS B accepted
PASS B result
PASS C accepted
PASS C result
PASS D accepted
PASS D result
PASS E accepted
PASS E result
Checks: 16, failed: 0
```

Pod wynikiem CLion dopisuje `Process finished with exit code 0`.

</details>

- **16 sprawdzeń:** po trzy dla `was_sent` i `status_text`, po dwa dla każdego z pięciu przypadków `parse_status`.
- **Wyniki oczekiwane pochodzą z kontraktu**, a nie z drugiego wywołania sprawdzanej funkcji. Nawet przy `status_text` tekst oczekiwany to gotowy napis z tabeli w punkcie 5.
- `PASS D accepted` znaczy: sprawdzenie wyniku przypadku D się zgadza. Wynik oczekiwany to `false`, a funkcja zwróciła `false`.

## 8. Diagnostyka: literówka w nazwie stanu

Wróć do magazynu z punktu 1. Ten sam program, ze stanem zamiast tekstu i z tą samą pomyłką, podwojoną literą:

<!-- broken: order_packing_typo at=10:35 errors=1 error=^no member named 'preparring' in 'OrderStatus' -->
```cpp
#include <iostream>

enum class OrderStatus {
    received,
    preparing,
    sent
};

bool needs_packing(OrderStatus status) {
    return status == OrderStatus::preparring;
}

int main() {
    OrderStatus status{OrderStatus::preparing};

    if (needs_packing(status)) {
        std::cout << "Pack the order\n";
    } else {
        std::cout << "Nothing to pack\n";
    }
}
```

**To trzecie obowiązkowe uruchomienie.** Wykonaj kroki po kolei:

1. **Przewidź**, zanim cokolwiek zbudujesz: czy ten program się zbuduje? Jeśli tak, co wypisze? Jeśli nie, w której linijce kompilator zgłosi błąd?
2. Wpisz program do `main.cpp` i zbuduj go.
3. Znajdź pierwszy błąd: plik, linijkę i nazwę, której dotyczy.
4. Porównaj z punktem 1: tam ta sama pomyłka zbudowała się bez słowa.
5. Popraw nazwę i zbuduj program jeszcze raz.
6. Uruchom poprawioną wersję i sprawdź, co wypisze.

<details>
<summary>Co się dzieje i jak to naprawić: otwórz po wykonaniu kroków 1–6</summary>

**Etap:** kompilacja. Program się nie buduje, więc nie ma czego uruchomić. Kompilator zgłasza jeden błąd w linijce 10, przy nazwie `preparring`. Na systemach, na których sprawdzamy kurs, komunikat zaczyna się od `no member named 'preparring' in 'OrderStatus'`: w typie `OrderStatus` nie ma wartości o tej nazwie. Clang często dopisuje też podpowiedź w rodzaju `did you mean 'preparing'?`. Dokładne brzmienie komunikatu może zależeć od wersji kompilatora, ale zawsze wskazuje tę samą linijkę i tę samą nazwę.

**Różnica z punktem 1:**
- `"preparingg"` to napis. Każdy napis jest poprawną wartością typu `std::string`, więc kompilator nie ma czego zgłosić. Błąd wychodzi dopiero przy działaniu programu albo w teście.
- `OrderStatus::preparring` to nazwa wartości, a typ `OrderStatus` ma tylko trzy nazwy. Nieznana nazwa nie tworzy po cichu czwartego stanu: program w ogóle nie powstaje.

**Poprawka:** `OrderStatus::preparing` w linijce 10. Poprawiony program:

<!-- example: order_packing -->
```cpp
#include <iostream>

enum class OrderStatus {
    received,
    preparing,
    sent
};

bool needs_packing(OrderStatus status) {
    return status == OrderStatus::preparing;
}

int main() {
    OrderStatus status{OrderStatus::preparing};

    if (needs_packing(status)) {
        std::cout << "Pack the order\n";
    } else {
        std::cout << "Nothing to pack\n";
    }
}
```

<!-- output: order_packing -->
```text
Pack the order
```

**Czego kompilator nie wykryje:** gdyby w linijce 10 stało `OrderStatus::sent`, program zbudowałby się bez ostrzeżeń i wypisał `Nothing to pack`. To poprawna nazwa, tylko nie ta. Taki błąd wykrywa test, który sprawdza `needs_packing` dla zamówienia w przygotowaniu.

</details>

## 9. Misja: status zgłoszenia usterki

Dział techniczny prowadzi zgłoszenia usterek. Zgłoszenie jest otwarte, w trakcie sprawdzania albo zamknięte. Zapisz ten stan jako typ wyliczeniowy i przygotuj dla niego funkcje oraz program testowy.

**Typ:**

<!-- fragment -->
```cpp
enum class ReportStatus {
    opened,
    investigating,
    closed
};
```

**Kontrakt funkcji:**

- `bool needs_work(ReportStatus status)`: `true`, gdy zgłoszenie wymaga jeszcze pracy, czyli nie jest zamknięte. Dla `closed` zwraca `false`.
- `std::string report_status_text(ReportStatus status)`: tekst stanu, zgodny z tabelą poniżej.
- `bool parse_report_status(const std::string& text, ReportStatus& result)`: rozpoznaje stan z tekstu według tej samej tabeli. Dla nieznanego tekstu zwraca `false` i nie zmienia `result`. Wielkie i małe litery się rozróżnia.

| Tekst | Stan |
|---|---|
| `"opened"` | `ReportStatus::opened` |
| `"investigating"` | `ReportStatus::investigating` |
| `"closed"` | `ReportStatus::closed` |
| `"unknown"` | odmowa |
| `"Closed"` | odmowa |

W `cpp-workspace` utwórz katalog `report_status`, skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program` i otwórz go w CLionie. Całość napisz w jednym pliku `main.cpp`. `CMakeLists.txt` zostaw bez zmian.

**Kolejność pracy:**

1. **Najpierw tabela przypadków.** Zanim napiszesz kod, przygotuj tabelę przypadków dla `parse_report_status`, jak w punkcie 7: tekst, stan `result` przed wywołaniem, wynik oczekiwany, stan po wywołaniu i powód. Muszą się w niej znaleźć trzy znane nazwy, `"unknown"`, `"Closed"` i **co najmniej jeden własny błędny tekst**, inny niż w tej lekcji. Przy każdym przypadku odmowy zapisz, jaki stan ma zostać w `result` i dlaczego.
2. Zdefiniuj `ReportStatus` i napisz trzy funkcje.
3. Napisz program testowy: funkcję sprawdzającą dla stanów `ReportStatus`, sprawdzenia `needs_work` i `report_status_text` dla każdego z trzech stanów oraz dwa sprawdzenia, wyniku i stanu, dla każdego przypadku z tabeli. Na końcu podsumowanie i kod zakończenia jak w punkcie 7.
4. **To czwarte obowiązkowe uruchomienie:** uruchom program testowy z poprawnymi funkcjami. Wszystkie sprawdzenia powinny wypisać `PASS`, a kod zakończenia powinien wynosić 0.
5. **Celowy błąd.** W `report_status_text` zmień jedną literę w jednym ze zwracanych tekstów, na przykład zgub literę w `"investigating"`. **To piąte obowiązkowe uruchomienie:** zbuduj program i uruchom testy. Zapisz, czy kompilator coś zgłosił, który test się nie udał i jaki jest kod zakończenia. Potem przywróć poprawny tekst.

Nie musisz uruchamiać innych wersji. Jeśli chcesz, sprawdź jeszcze, co się stanie po literówce w nazwie wartości, na przykład `ReportStatus::closd`, i porównaj z krokiem 5.

### Kryterium sukcesu

- [ ] Program buduje się jako C++20, a `CMakeLists.txt` jest taki jak w lekcji 0.5.
- [ ] `ReportStatus` jest typem `enum class` z trzema wartościami z kontraktu; stany nie są nigdzie zapisane jako napisy.
- [ ] `needs_work` korzysta z porównania stanów i zwraca wyniki zgodne z kontraktem.
- [ ] `report_status_text` zwraca dla każdego stanu tekst z tabeli i ma jawne zachowanie zapasowe na końcu.
- [ ] `parse_report_status` rozpoznaje trzy znane nazwy, odrzuca każdy inny tekst i przy odmowie nie zmienia `result`.
- [ ] Tabela przypadków zawiera `"unknown"`, `"Closed"` i co najmniej jeden własny błędny tekst z powodem.
- [ ] W przypadkach znanych nazw `result` zaczyna od innego stanu niż oczekiwany; w przypadkach odmowy test sprawdza, że stan sprzed wywołania został.
- [ ] Wyniki oczekiwane w testach pochodzą z kontraktu, a nie z wywołań sprawdzanych funkcji.
- [ ] Z poprawnymi funkcjami wszystkie sprawdzenia przechodzą, a kod zakończenia wynosi 0.
- [ ] Z celową literówką w tekście program się buduje, test tekstu tego stanu wypisuje `FAIL`, a kod zakończenia wynosi 1.
- [ ] Umiesz powiedzieć, którą pomyłkę wykrywa kompilator, a którą tylko testy, i dlaczego.

Gdy wynik się zgadza, możesz zapisać projekt w Gicie, jak w lekcji 1.5: `main.cpp` i `CMakeLists.txt`, bez katalogu budowania.

<details>
<summary>Podpowiedź 1: definicja stanu</summary>

Zestaw stanów jest zamknięty: zgłoszenie może być tylko w jednym z trzech stanów z kontraktu. Które słowa kluczowe rozpoczynają definicję takiego typu, gdzie wpisujesz nazwy jego wartości i czym je rozdzielasz? Gdzie w pliku musi stać ta definicja, żeby funkcje mogły z niej korzystać? Porównaj z punktem 2.

</details>

<details>
<summary>Podpowiedź 2: reprezentacja tekstowa</summary>

Masz dwie zamiany w przeciwnych kierunkach. Jedna dostaje stan i zawsze zwraca jakiś tekst, także w zachowaniu zapasowym. Druga dostaje tekst i nie zawsze potrafi zwrócić stan, dlatego mówi o powodzeniu przez `bool`, a stan zwraca przez parametr wynikowy. W której z nich teksty z tabeli są wynikiem, a w której są tym, z czym porównujesz dane wejściowe?

</details>

<details>
<summary>Podpowiedź 3: nieznany tekst</summary>

Kiedy funkcja rozpoznająca może przypisać coś do `result`? Dopiero wtedy, gdy wie, który to stan. Co więc zostaje w `result`, jeśli żaden warunek nie pasuje, a funkcja dochodzi do ostatniej linijki? Jak w teście odróżnisz funkcję, która niczego nie zmienia, od takiej, która przez przypadek przypisuje ten sam stan, który już tam był?

</details>

## 10. Gdy coś pójdzie inaczej

| Co widzisz | Co to znaczy | Co zrobić |
|---|---|---|
| Błąd z `no member named '…' in 'ReportStatus'` | Nazwa wartości po `ReportStatus::` nie istnieje w tym typie, na przykład przez literówkę. | Porównaj nazwę z definicją typu. Popraw nazwę w kodzie, a nie w definicji. |
| Błąd z `use of undeclared identifier 'opened'` | Nazwa wartości bez nazwy typu przed nią. | Pisz `ReportStatus::opened`. |
| Błąd z `invalid operands to binary expression` przy `<<` | Program próbuje wypisać stan wprost przez `std::cout` (punkt 5). | Wypisz tekst stanu: `report_status_text(status)`. |
| Błąd przy inicjalizacji albo przypisaniu napisu, na przykład z `cannot initialize a variable of type 'ReportStatus'` | Do zmiennej stanu trafia tekst, na przykład `"opened"`. | Stan to wartość typu: `ReportStatus::opened`. Tekst zamieniaj funkcją rozpoznającą. |
| Ostrzeżenie albo błąd, że funkcja nie zwraca wartości we wszystkich ścieżkach | Funkcji zamiany na tekst brakuje zachowania zapasowego na końcu (punkt 5). | Dodaj końcowy `return` z tekstem zapasowym. |
| Test znanej nazwy przechodzi, choć funkcja rozpoznająca niczego nie przypisuje | `result` zaczyna od stanu, który jest wynikiem oczekiwanym (punkt 7). | Zacznij od innego stanu niż oczekiwany. |
| Linijka `FAIL` pokazuje ten sam tekst po `expected` i po `actual` | Funkcja sprawdzająca wypisuje stany przez `report_status_text`, a ta zwraca ten sam tekst dla dwóch różnych stanów. | Sprawdź testy `report_status_text`: jeden z nich wskaże błędny tekst. |

## 11. Wyjaśnij

Odpowiedz własnymi słowami, najlepiej na piśmie. Dopiero potem porównaj z przykładowymi odpowiedziami.

1. Czym różni się zmienna typu `OrderStatus` od zmiennej typu `std::string`, która przechowuje słowo `"sent"`?
2. Co oznacza, że typ wyliczeniowy ma zamknięty zestaw wartości?
3. Co oznacza zapis `OrderStatus::sent`? Co oznacza w nim każda część?
4. Kiedy `status == OrderStatus::sent` daje `true`, a kiedy `status != OrderStatus::sent` daje `true`?
5. Dlaczego literówka w `OrderStatus::preparring` zatrzymuje kompilację, a literówka w `"preparingg"` nie?
6. Dlaczego programu nie da się zbudować z `std::cout << status`, i jak wypisać stan?
7. Po co `status_text` kończy się `return "unknown";`, skoro każdy z trzech stanów ma własny warunek?
8. Jak sprawdzić w teście, że funkcja rozpoznająca odrzuca nieznany tekst?
9. Dlaczego po nieudanym rozpoznaniu funkcja nie może zmienić parametru wynikowego?
10. Skoro kompilator sprawdza nazwy stanów, to po co testy funkcji, które używają `enum class`?

<details>
<summary>Przykładowe odpowiedzi</summary>

1. Zmienna typu `OrderStatus` może mieć tylko jedną z trzech wartości zdefiniowanych w typie, a kompilator to sprawdza. Zmienna typu `std::string` może przechowywać dowolny napis, także z literówką, i kompilator nie ma jak tego sprawdzić.
2. Wszystkie dozwolone wartości są wymienione w definicji typu. Innych nie ma i nie da się ich dopisać w innym miejscu programu przez samo użycie nowej nazwy.
3. Wartość `sent` z typu `OrderStatus`. `OrderStatus` to nazwa typu, `::` oznacza „nazwa z wnętrza”, jak w `std::cout`, a `sent` to nazwa wartości.
4. `==` daje `true`, gdy `status` ma wartość `OrderStatus::sent`. `!=` daje `true`, gdy `status` ma którąkolwiek inną wartość, czyli `received` albo `preparing`.
5. `preparring` musi być nazwą wartości typu `OrderStatus`, a typ ma tylko trzy nazwy, więc kompilator zgłasza błąd. `"preparingg"` to napis, a każdy napis jest poprawną wartością `std::string`: porównanie jest legalne i po prostu daje `false`.
6. Nie ma działania `<<`, które wypisuje wartość typu `OrderStatus`. Stan to wartość, a nie tekst. Tekst daje dopiero funkcja zamiany, na przykład `std::cout << status_text(status)`.
7. Funkcja zwracająca wynik musi go zwrócić na każdej drodze, a kompilator nie uznaje trzech osobnych warunków za komplet. Ta linijka jest też zachowaniem zapasowym: gdyby do typu dopisano nowy stan bez uzupełnienia funkcji, zwróci `unknown`, a test to pokaże.
8. Wywołać ją z nieznanym tekstem i sprawdzić dwie rzeczy: że zwraca `false` i że `result` ma ten sam stan co przed wywołaniem.
9. Bo wywołujący dostałby stan, którego tekst wcale nie oznaczał. Kontrakt mówi: przy `false` wynik jest bez zmian, więc wywołujący może dalej polegać na swoim poprzednim stanie. To zasada „wszystko albo nic” z lekcji 9.2 i 10.4.
10. Bo kompilator sprawdza tylko, czy nazwa istnieje. Nie sprawdza, czy program używa właściwej nazwy, czy funkcja zwraca właściwy tekst ani czy rozpoznaje właściwe napisy. Porównanie z `OrderStatus::received` zamiast z `OrderStatus::sent` albo literówka w tekście zwracanym przez `status_text` budują się bez ostrzeżeń. Wykrywa je dopiero test.

</details>

## Podsumowanie

- Stan zapisany jako tekst przyjmuje każdy napis, także z literówką. Kompilator nie ma czego zgłosić, a błąd wychodzi dopiero przy działaniu programu albo w teście.
- `enum class` definiuje **typ wyliczeniowy** z zamkniętym zestawem nazwanych wartości. Stan jest wartością tego typu, a nie umownym napisem.
- Konkretną wartość wskazujesz zapisem `Typ::wartość`, na przykład `OrderStatus::sent`. Nazwy typu i wartości sprawdza kompilator: nieznana nazwa to błąd kompilacji.
- Stany porównujesz przez `==` i `!=`, przekazujesz do funkcji i zwracasz z funkcji jak inne małe wartości.
- **Stan jest wartością typu, a tekst jest jego reprezentacją.** Zamianę stanu na tekst i rozpoznawanie stanu z tekstu piszesz jako dwie jawne funkcje.
- Funkcja rozpoznająca zwraca `bool` i przy nieznanym tekście nie zmienia parametru wynikowego.
- Kompilator wykrywa nieznane nazwy. Pomyłki z poprawnymi nazwami i błędy w tekstach wykrywają dopiero testy.

## Co dalej

Funkcja `status_text` sprawdza stany po kolei osobnymi warunkami, a o nowym stanie, którego nie uzupełniono, dowiadujesz się dopiero z testu. W [lekcji 14.2: Każdy stan obsłużony: `switch`](lesson_02_handling_every_state_with_switch.md) poznasz konstrukcję, która obsługuje różne wartości takiego typu w jednym miejscu.

---

## Przykładowe rozwiązania

Zajrzyj tutaj **po własnej próbie**. Twoje nazwy przypadków, własne błędne teksty i kolejność sprawdzeń mogą się różnić, jeśli spełniają kontrakt i listę kontrolną.

<details>
<summary>Punkt 9: misja, status zgłoszenia usterki</summary>

**Tabela przypadków dla `parse_report_status`:**

| Przypadek | Tekst | `result` przed wywołaniem | Wynik oczekiwany | `result` po wywołaniu | Dlaczego ten przypadek |
|---|---|---|---|---|---|
| A | `"opened"` | `closed` | `true` | `opened` | znana nazwa |
| B | `"investigating"` | `opened` | `true` | `investigating` | znana nazwa |
| C | `"closed"` | `opened` | `true` | `closed` | znana nazwa |
| D | `"unknown"` | `investigating` | `false` | `investigating`, bez zmian | nieznane słowo |
| E | `"Closed"` | `opened` | `false` | `opened`, bez zmian | wielka litera: kontrakt rozróżnia wielkość liter |
| F | `"open"` | `investigating` | `false` | `investigating`, bez zmian | własny przypadek: początek znanej nazwy to jeszcze nie nazwa |

Inne dobre własne przypadki: `""`, `" closed"` ze spacją na początku, `"closed "` ze spacją na końcu, `"CLOSED"`. Każdy z nich ma być odrzucony, bo nie jest dokładnie jedną z trzech nazw.

**`main.cpp`:**

<!-- example: report_status_tests -->
```cpp
#include <iostream>
#include <string>

enum class ReportStatus {
    opened,
    investigating,
    closed
};

bool needs_work(ReportStatus status) {
    return status != ReportStatus::closed;
}

std::string report_status_text(ReportStatus status) {
    if (status == ReportStatus::opened) {
        return "opened";
    }

    if (status == ReportStatus::investigating) {
        return "investigating";
    }

    if (status == ReportStatus::closed) {
        return "closed";
    }

    return "unknown";
}

bool parse_report_status(const std::string& text, ReportStatus& result) {
    if (text == "opened") {
        result = ReportStatus::opened;
        return true;
    }

    if (text == "investigating") {
        result = ReportStatus::investigating;
        return true;
    }

    if (text == "closed") {
        result = ReportStatus::closed;
        return true;
    }

    return false;
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

void check_text(const std::string& name, const std::string& expected, const std::string& actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected \"" << expected << "\", actual \"" << actual << "\"\n";
        ++failed;
    }
}

void check_report_status(const std::string& name, ReportStatus expected, ReportStatus actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << report_status_text(expected) << ", actual " << report_status_text(actual) << "\n";
        ++failed;
    }
}

int main() {
    int checks{0};
    int failed{0};

    check_bool("needs_work(opened)", true, needs_work(ReportStatus::opened), checks, failed);
    check_bool("needs_work(investigating)", true, needs_work(ReportStatus::investigating), checks, failed);
    check_bool("needs_work(closed)", false, needs_work(ReportStatus::closed), checks, failed);

    check_text("report_status_text(opened)", "opened", report_status_text(ReportStatus::opened), checks, failed);
    check_text("report_status_text(investigating)", "investigating", report_status_text(ReportStatus::investigating), checks, failed);
    check_text("report_status_text(closed)", "closed", report_status_text(ReportStatus::closed), checks, failed);

    ReportStatus result_a{ReportStatus::closed};
    const bool accepted_a{parse_report_status("opened", result_a)};
    check_bool("A accepted", true, accepted_a, checks, failed);
    check_report_status("A result", ReportStatus::opened, result_a, checks, failed);

    ReportStatus result_b{ReportStatus::opened};
    const bool accepted_b{parse_report_status("investigating", result_b)};
    check_bool("B accepted", true, accepted_b, checks, failed);
    check_report_status("B result", ReportStatus::investigating, result_b, checks, failed);

    ReportStatus result_c{ReportStatus::opened};
    const bool accepted_c{parse_report_status("closed", result_c)};
    check_bool("C accepted", true, accepted_c, checks, failed);
    check_report_status("C result", ReportStatus::closed, result_c, checks, failed);

    ReportStatus result_d{ReportStatus::investigating};
    const bool accepted_d{parse_report_status("unknown", result_d)};
    check_bool("D accepted", false, accepted_d, checks, failed);
    check_report_status("D result", ReportStatus::investigating, result_d, checks, failed);

    ReportStatus result_e{ReportStatus::opened};
    const bool accepted_e{parse_report_status("Closed", result_e)};
    check_bool("E accepted", false, accepted_e, checks, failed);
    check_report_status("E result", ReportStatus::opened, result_e, checks, failed);

    ReportStatus result_f{ReportStatus::investigating};
    const bool accepted_f{parse_report_status("open", result_f)};
    check_bool("F accepted", false, accepted_f, checks, failed);
    check_report_status("F result", ReportStatus::investigating, result_f, checks, failed);

    std::cout << "Checks: " << checks << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

<!-- output: report_status_tests -->
```text
PASS needs_work(opened)
PASS needs_work(investigating)
PASS needs_work(closed)
PASS report_status_text(opened)
PASS report_status_text(investigating)
PASS report_status_text(closed)
PASS A accepted
PASS A result
PASS B accepted
PASS B result
PASS C accepted
PASS C result
PASS D accepted
PASS D result
PASS E accepted
PASS E result
PASS F accepted
PASS F result
Checks: 18, failed: 0
```

Kod zakończenia: 0.

- **`needs_work`:** jeden warunek, `!=`, bo zgłoszenie wymaga pracy w każdym stanie oprócz zamkniętego. Poprawne jest też `status == ReportStatus::opened || status == ReportStatus::investigating`.
- **`report_status_text`:** ta sama budowa co `status_text` w punkcie 5, z zachowaniem zapasowym na końcu.
- **`parse_report_status`:** przypisuje `result` tylko po rozpoznaniu nazwy. `"Closed"` i `"open"` nie są dokładnie żadną z trzech nazw, więc funkcja dochodzi do `return false;` i niczego nie zmienia.
- **Funkcja sprawdzająca:** porównuje stany przez `==`, a do linijki `FAIL` zamienia je na tekst. Twoja może się nazywać inaczej, na przykład `check_status`.

**Celowy błąd:** w `report_status_text` tekst `"investigatng"`, bez litery `i` przed `n`. Zmienia się tylko ta jedna linijka, a program testowy zostaje bez zmian:

<!-- example: report_status_tests_typo exit=1 -->
```cpp
#include <iostream>
#include <string>

enum class ReportStatus {
    opened,
    investigating,
    closed
};

bool needs_work(ReportStatus status) {
    return status != ReportStatus::closed;
}

std::string report_status_text(ReportStatus status) {
    if (status == ReportStatus::opened) {
        return "opened";
    }

    if (status == ReportStatus::investigating) {
        return "investigatng";
    }

    if (status == ReportStatus::closed) {
        return "closed";
    }

    return "unknown";
}

bool parse_report_status(const std::string& text, ReportStatus& result) {
    if (text == "opened") {
        result = ReportStatus::opened;
        return true;
    }

    if (text == "investigating") {
        result = ReportStatus::investigating;
        return true;
    }

    if (text == "closed") {
        result = ReportStatus::closed;
        return true;
    }

    return false;
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

void check_text(const std::string& name, const std::string& expected, const std::string& actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected \"" << expected << "\", actual \"" << actual << "\"\n";
        ++failed;
    }
}

void check_report_status(const std::string& name, ReportStatus expected, ReportStatus actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << report_status_text(expected) << ", actual " << report_status_text(actual) << "\n";
        ++failed;
    }
}

int main() {
    int checks{0};
    int failed{0};

    check_bool("needs_work(opened)", true, needs_work(ReportStatus::opened), checks, failed);
    check_bool("needs_work(investigating)", true, needs_work(ReportStatus::investigating), checks, failed);
    check_bool("needs_work(closed)", false, needs_work(ReportStatus::closed), checks, failed);

    check_text("report_status_text(opened)", "opened", report_status_text(ReportStatus::opened), checks, failed);
    check_text("report_status_text(investigating)", "investigating", report_status_text(ReportStatus::investigating), checks, failed);
    check_text("report_status_text(closed)", "closed", report_status_text(ReportStatus::closed), checks, failed);

    ReportStatus result_a{ReportStatus::closed};
    const bool accepted_a{parse_report_status("opened", result_a)};
    check_bool("A accepted", true, accepted_a, checks, failed);
    check_report_status("A result", ReportStatus::opened, result_a, checks, failed);

    ReportStatus result_b{ReportStatus::opened};
    const bool accepted_b{parse_report_status("investigating", result_b)};
    check_bool("B accepted", true, accepted_b, checks, failed);
    check_report_status("B result", ReportStatus::investigating, result_b, checks, failed);

    ReportStatus result_c{ReportStatus::opened};
    const bool accepted_c{parse_report_status("closed", result_c)};
    check_bool("C accepted", true, accepted_c, checks, failed);
    check_report_status("C result", ReportStatus::closed, result_c, checks, failed);

    ReportStatus result_d{ReportStatus::investigating};
    const bool accepted_d{parse_report_status("unknown", result_d)};
    check_bool("D accepted", false, accepted_d, checks, failed);
    check_report_status("D result", ReportStatus::investigating, result_d, checks, failed);

    ReportStatus result_e{ReportStatus::opened};
    const bool accepted_e{parse_report_status("Closed", result_e)};
    check_bool("E accepted", false, accepted_e, checks, failed);
    check_report_status("E result", ReportStatus::opened, result_e, checks, failed);

    ReportStatus result_f{ReportStatus::investigating};
    const bool accepted_f{parse_report_status("open", result_f)};
    check_bool("F accepted", false, accepted_f, checks, failed);
    check_report_status("F result", ReportStatus::investigating, result_f, checks, failed);

    std::cout << "Checks: " << checks << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

<!-- output: report_status_tests_typo -->
```text
PASS needs_work(opened)
PASS needs_work(investigating)
PASS needs_work(closed)
PASS report_status_text(opened)
FAIL report_status_text(investigating): expected "investigating", actual "investigatng"
PASS report_status_text(closed)
PASS A accepted
PASS A result
PASS B accepted
PASS B result
PASS C accepted
PASS C result
PASS D accepted
PASS D result
PASS E accepted
PASS E result
PASS F accepted
PASS F result
Checks: 18, failed: 1
```

Kod zakończenia: 1.

- **Kompilator:** nie zgłasza niczego. `"investigatng"` to poprawny napis, tak samo jak `"preparingg"` w punkcie 1.
- **Testy:** nie udaje się tylko sprawdzenie tekstu stanu `investigating`. Rozpoznawanie tekstu ma własne napisy, więc przypadki A–F przechodzą.
- **Wniosek:** typ wyliczeniowy chroni nazwy stanów, ale nie teksty, które z nich robisz. Tekst każdego stanu musi mieć własny test.

**Samoocena.** Porównaj swoją pracę z listą kontrolną w punkcie 9. Szczególnie sprawdź:
- czy żaden stan nie jest w programie zapisany jako napis, poza tekstami w dwóch funkcjach zamiany;
- czy Twój własny błędny tekst ma zapisany powód i czy test sprawdza wtedy także stan `result`;
- czy w przypadkach znanych nazw `result` zaczyna od innego stanu niż oczekiwany;
- czy umiesz wskazać jedną pomyłkę, którą zgłasza kompilator, i jedną, którą wykrywa tylko test.

Jeśli w jednym z tych punktów odpowiedź brzmi „nie”, wróć do odpowiedniego punktu lekcji, zanim przejdziesz dalej.

</details>

**Poprzednia lekcja:** [Lekcja 13.5: Rezerwacje na warsztaty (sprawdzian Modułu 13)](../module_13_testing_functions/lesson_05_workshop_reservations.md) · **Następna lekcja:** [Lekcja 14.2: Każdy stan obsłużony: `switch`](lesson_02_handling_every_state_with_switch.md) · [Opis kursu](../../README.md)

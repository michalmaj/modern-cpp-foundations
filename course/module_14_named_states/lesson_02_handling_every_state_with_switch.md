# Lekcja 14.2: Każdy stan obsłużony: `switch`

**Polski** · [English](lesson_02_handling_every_state_with_switch.en.md) · [Opis kursu](../../README.md)

> **Moduł 14, lekcja 2** · około 80–100 minut, można ją podzielić na dwa podejścia (punkty 1–7, potem misja)
> **Potrzebujesz:** katalogu `cpp-workspace` i oryginalnego projektu `lesson_05_first_program`, jak dotąd. Debugger nie jest w tej lekcji potrzebny.
> **Wersja pilotażowa.** Programy z tej lekcji sprawdzamy automatycznie na Windowsie, Ubuntu i macOS, razem z ich kodem zakończenia. Program, który nie ma się zbudować, sprawdzamy razem z miejscem pierwszego błędu. Ostrzeżeń kompilatora nie sprawdzamy automatycznie.

## Zanim zaczniesz

Ta lekcja zakłada, że:

- definiujesz typ `enum class`, porównujesz jego wartości i piszesz funkcję `status_text`, która zamienia stan na tekst (lekcja 14.1);
- piszesz ciągi warunków `if` (lekcje 3.1–3.3) i funkcje z kilkoma `return`, z których pierwszy wykonany kończy funkcję (lekcje 5.3–5.4);
- piszesz jednoplikowe programy testowe z funkcją `check_text`, które kończą się kodem 1, gdy któreś sprawdzenie się nie uda (lekcje 13.1–13.3);
- dobierasz przypadki testowe tak, żeby odróżniały poprawną funkcję od wersji z błędem (lekcja 13.2).

## Sytuacja

Wracamy do sklepu internetowego z lekcji 14.1. Funkcja `status_text` ma dla każdego z trzech stanów zamówienia osobny warunek `if`. Działa, ale żeby mieć pewność, że obsługuje każdy stan, trzeba przeczytać każdy warunek po kolei. Magazyn potrzebuje też drugiej funkcji: dla każdego stanu innego następnego działania.

W tej lekcji odpowiesz na pytanie: **jak zapisać „dla każdego stanu zrób coś innego” w jednym miejscu, i czego ta konstrukcja nie sprawdzi za Ciebie?**

Po tej lekcji będziesz:

- rozpoznawać ciąg `if`, który porównuje jedną wartość z kolejnymi stanami, jako kandydata do `switch`;
- pisać instrukcję `switch` z etykietą `case` dla każdej wartości typu `enum class`;
- kończyć obsługę stanu przez `return`, gdy funkcja ma od razu zwrócić wynik, albo przez `break`, gdy po `switch` funkcja ma jeszcze coś zrobić;
- rozpoznawać przejście do następnej etykiety, gdy brakuje `break`, i wykrywać je testem;
- świadomie decydować, czy `switch` potrzebuje etykiety `default`;
- odróżniać błąd kompilacji, ostrzeżenie kompilatora i błąd w działaniu, który wykrywa dopiero test.

## 1. Ten sam wybór w jednym miejscu: `switch`

W lekcji 14.1 funkcja `status_text` zamieniała stan zamówienia na tekst trzema warunkami `if`:

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

Przyjrzyj się tym warunkom. Każdy porównuje **tę samą zmienną**, `status`, z inną wartością **tego samego typu**, `OrderStatus`. Żeby mieć pewność, że funkcja obsługuje każdy stan, trzeba przeczytać wszystkie trzy warunki i sprawdzić, czy w każdym stoi `status`, czy żaden stan się nie powtarza i czy żadnego nie brakuje.

Na taką sytuację, jedną wartość z kilkoma znanymi, nazwanymi możliwościami, C++ ma osobną konstrukcję: **instrukcję `switch`** (*switch statement*). Ta sama funkcja wygląda z nią tak:

<!-- fragment -->
```cpp
std::string status_text(OrderStatus status) {
    switch (status) {
        case OrderStatus::received:
            return "received";
        case OrderStatus::preparing:
            return "preparing";
        case OrderStatus::sent:
            return "sent";
    }

    return "unknown";
}
```

- `switch (status)` rozpoczyna instrukcję `switch`. W nawiasach stoi wartość, według której program wybiera, co zrobić. Tu to zmienna `status`. Program oblicza ją raz, na początku.
- Klamry po nawiasach obejmują całe wnętrze `switch`.
- `case OrderStatus::received:` to **etykieta `case`** (*case label*). Nazywa jedną wartość i oznacza miejsce, od którego program zaczyna, gdy `status` ma właśnie tę wartość. Po słowie `case` stoi nazwa wartości razem z nazwą typu, jak w lekcji 14.1, a na końcu etykiety **dwukropek**, nie średnik.
- Pod etykietą stoją instrukcje dla tej wartości. Tu to jedna instrukcja, `return "received";`. Jak w lekcji 5.4, `return` od razu kończy całą funkcję i przekazuje jej wynik.
- Każdy z trzech stanów ma własną etykietę. Etykiety piszemy o jedno wcięcie głębiej niż `switch`, a instrukcje pod nimi o jeszcze jedno, żeby było widać, co należy do której etykiety.
- **Za `switch` stoi `return "unknown";`**, to samo zachowanie zapasowe co w lekcji 14.1. Każdy z trzech stanów ma swoją etykietę i kończy funkcję wcześniej. Funkcja ma jednak także drogę, na której żadna etykieta nie pasuje: wtedy program pomija całe wnętrze `switch` i dochodzi do tej linijki. Funkcja, która obiecuje wynik, musi go zwrócić na każdej drodze (lekcja 5.4), także na tej.

**Kontrakt się nie zmienia.** Zmieniła się budowa funkcji, a nie jej wyniki:

| Stan | Tekst zwracany przez `status_text` |
|---|---|
| `OrderStatus::received` | `"received"` |
| `OrderStatus::preparing` | `"preparing"` |
| `OrderStatus::sent` | `"sent"` |

**Kiedy `switch`, a kiedy `if`?** `switch` jest czytelny, gdy wybierasz według jednej wartości, która ma kilka znanych możliwości, i dla każdej robisz coś innego: etykiety tworzą listę obsłużonych stanów. Przy ciągu `if` zostajesz, gdy warunki są różne, na przykład zakres `count >= 1 && count <= 24`, albo gdy porównujesz teksty. Wartość w nawiasach `switch` musi być liczbą całkowitą, na przykład `int`, albo wartością typu wyliczeniowego. Tekstu `std::string` w `switch` nie użyjesz, dlatego `parse_status` z lekcji 14.1 zostaje przy `if`.

Pełny program:

<!-- example: order_switch -->
```cpp
#include <iostream>
#include <string>

enum class OrderStatus {
    received,
    preparing,
    sent
};

std::string status_text(OrderStatus status) {
    switch (status) {
        case OrderStatus::received:
            return "received";
        case OrderStatus::preparing:
            return "preparing";
        case OrderStatus::sent:
            return "sent";
    }

    return "unknown";
}

int main() {
    OrderStatus status{OrderStatus::received};
    std::cout << "Order: " << status_text(status) << "\n";

    status = OrderStatus::sent;
    std::cout << "Order: " << status_text(status) << "\n";
}
```

**To pierwsze obowiązkowe uruchomienie.** W `cpp-workspace` utwórz katalog `lesson_14_2`, skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program` i otwórz go w CLionie. Zastąp zawartość `main.cpp` tym programem. **Przewidź**, co wypisze, a potem zbuduj go i uruchom. `CMakeLists.txt` zostaw bez zmian. Kolejne programy z tej lekcji wpisujesz w ten sam `main.cpp`.

<details>
<summary>Standardowe wyjście</summary>

<!-- output: order_switch -->
```text
Order: received
Order: sent
```

</details>

## 2. Jak działa `switch`

Program wykonuje `switch` w kilku krokach:

| Krok | Co robi program |
|---|---|
| 1 | Oblicza wartość w nawiasach `switch`. |
| 2 | Szuka etykiety `case` z tą wartością. |
| 3 | Przechodzi do znalezionej etykiety i od niej zaczyna wykonywać instrukcje. |
| 4 | Wykonuje kolejne instrukcje w dół, aż coś zakończy wykonywanie albo aż dojdzie do klamry zamykającej `switch`. |
| 5 | Gdy żadna etykieta `case` nie pasuje, przechodzi do etykiety `default`, jeśli `switch` ją ma (punkt 6). Jeśli nie ma, pomija całe wnętrze `switch`. |

Dla `status_text(OrderStatus::preparing)` program oblicza `status`, znajduje etykietę `case OrderStatus::preparing:`, wykonuje `return "preparing";` i funkcja się kończy. Instrukcja spod etykiety `received` się nie wykonuje, bo program zaczął niżej.

**Etykieta to nie `if`.** W ciągu `if` każdy warunek ma własny blok w klamrach. Program sprawdza warunki po kolei i wykonuje blok tego, który jest spełniony. W `switch` program wybiera tylko **miejsce, od którego zaczyna**. Etykieta `case` nie ma własnych klamer i niczego nie zamyka: to znacznik miejsca w kodzie. Kiedy wykonywanie już się zaczęło, program nie sprawdza kolejnych etykiet. Jeśli dojdzie do następnej etykiety, przechodzi przez nią i wykonuje instrukcje, które stoją pod nią.

W `status_text` nie ma z tym kłopotu, bo pod każdą etykietą stoi `return`, który kończy całą funkcję, zanim program dojdzie do następnej etykiety. W punkcie 3 zobaczysz funkcję, w której etykiety trzeba zakończyć inaczej.

**Najważniejsza zasada tej lekcji:** `switch` wybiera miejsce rozpoczęcia. Etykieta `case` sama nie kończy obsługi stanu. Koniec zapisujesz jawnie, na przykład przez `return` albo `break`.

## 3. `return` kończy funkcję, `break` kończy `switch`

Magazyn potrzebuje drugiej funkcji: co trzeba zrobić z zamówieniem w danym stanie.

**Kontrakt `next_step`:**

| Stan | Następne działanie |
|---|---|
| `OrderStatus::received` | `"Confirm order"` |
| `OrderStatus::preparing` | `"Pack order"` |
| `OrderStatus::sent` | `"Track delivery"` |

Tę funkcję zapiszemy inaczej niż `status_text`. Etykiety nie zwracają wyniku same, tylko przypisują tekst do zmiennej, a funkcja zwraca go raz, za `switch`:

<!-- fragment -->
```cpp
std::string next_step(OrderStatus status) {
    std::string action{"unknown"};

    switch (status) {
        case OrderStatus::received:
            action = "Confirm order";
            break;
        case OrderStatus::preparing:
            action = "Pack order";
            break;
        case OrderStatus::sent:
            action = "Track delivery";
            break;
    }

    return action;
}
```

- `std::string action{"unknown"};` tworzy zmienną na wynik. Zaczyna od tekstu zapasowego, jak `status_text`: gdyby żadna etykieta nie pasowała, `switch` nie zmieni `action`, a funkcja zwróci `"unknown"`.
- Pod każdą etykietą stoją dwie instrukcje: przypisanie tekstu i `break;`.
- **`break;` kończy `switch`.** Program wychodzi z jego wnętrza i przechodzi do pierwszej instrukcji za klamrą zamykającą `switch`. Tu jest nią `return action;`.
- **`break` nie kończy funkcji.** Kończy tylko `switch`. Funkcję kończy dopiero `return action;`.
- W tej lekcji `break` stoi zawsze wewnątrz `switch` i kończy właśnie `switch`.

**Co dzieje się z `action` po `break`?** Nic: zmienna zachowuje tekst, który przypisała etykieta. Dla `OrderStatus::preparing` program przypisuje `"Pack order"`, `break` kończy `switch`, a `return action;` zwraca `"Pack order"`. `break` niczego nie kasuje i nie zatrzymuje programu. Zmienia tylko miejsce, w którym program działa dalej.

| | `return` | `break` |
|---|---|---|
| Co kończy | całą funkcję | tylko `switch` |
| Gdzie program działa dalej | w miejscu, które wywołało funkcję, z jej wynikiem | w pierwszej instrukcji za `switch`, w tej samej funkcji |
| Kiedy go używasz | gdy wynik jest znany od razu, pod etykietą | gdy po `switch` funkcja ma jeszcze coś zrobić, na przykład zwrócić zebrany wynik |

**Po `return` nie potrzeba `break`.** W `status_text` żadna etykieta nie ma `break` i tak ma być: `return` kończy całą funkcję, więc instrukcja pod nim nigdy by się nie wykonała. Zamiast zasady „po każdej etykiecie `break`” zadawaj sobie pytanie: **czym kończy się ta etykieta i gdzie program działa dalej?**

Pełny program z obiema funkcjami:

<!-- example: order_next_step -->
```cpp
#include <iostream>
#include <string>

enum class OrderStatus {
    received,
    preparing,
    sent
};

std::string status_text(OrderStatus status) {
    switch (status) {
        case OrderStatus::received:
            return "received";
        case OrderStatus::preparing:
            return "preparing";
        case OrderStatus::sent:
            return "sent";
    }

    return "unknown";
}

std::string next_step(OrderStatus status) {
    std::string action{"unknown"};

    switch (status) {
        case OrderStatus::received:
            action = "Confirm order";
            break;
        case OrderStatus::preparing:
            action = "Pack order";
            break;
        case OrderStatus::sent:
            action = "Track delivery";
            break;
    }

    return action;
}

int main() {
    OrderStatus status{OrderStatus::received};
    std::cout << status_text(status) << ": " << next_step(status) << "\n";

    status = OrderStatus::preparing;
    std::cout << status_text(status) << ": " << next_step(status) << "\n";

    status = OrderStatus::sent;
    std::cout << status_text(status) << ": " << next_step(status) << "\n";
}
```

**To drugie obowiązkowe uruchomienie.** Zastąp zawartość `main.cpp` tym programem. **Przewidź** wszystkie trzy linijki wyniku, a potem zbuduj program i uruchom go.

<details>
<summary>Standardowe wyjście</summary>

<!-- output: order_next_step -->
```text
received: Confirm order
preparing: Pack order
sent: Track delivery
```

</details>

## 4. Program testowy: każdy stan, obie funkcje

Każda etykieta to osobna droga przez funkcję. Pomyłka pod jedną etykietą psuje wynik tylko dla jednego stanu, dlatego sprawdzasz obie funkcje **dla każdego stanu**. Wyniki oczekiwane pochodzą z kontraktów z punktów 1 i 3:

| Stan | `status_text` | `next_step` |
|---|---|---|
| `received` | `"received"` | `"Confirm order"` |
| `preparing` | `"preparing"` | `"Pack order"` |
| `sent` | `"sent"` | `"Track delivery"` |

Obie funkcje zwracają tekst, więc wystarczy `check_text` z lekcji 13.3. Sprawdzeń jest sześć, po jednym na każdą komórkę tabeli z wynikiem.

**To trzecie obowiązkowe uruchomienie. Ma trzy etapy:** teraz uruchomisz testy poprawnych funkcji, w punkcie 5 te same testy po usunięciu jednego `break`, a na koniec znowu po naprawie. Zastąp zawartość `main.cpp` programem poniżej. Funkcję `check_text` możesz skopiować z lekcji 13.3, a funkcje stanu z punktów 1 i 3. **Przewidź** ostatnią linijkę wyniku, zanim uruchomisz program.

<details>
<summary>Pełny program testowy</summary>

<!-- example: order_switch_tests -->
```cpp
#include <iostream>
#include <string>

enum class OrderStatus {
    received,
    preparing,
    sent
};

std::string status_text(OrderStatus status) {
    switch (status) {
        case OrderStatus::received:
            return "received";
        case OrderStatus::preparing:
            return "preparing";
        case OrderStatus::sent:
            return "sent";
    }

    return "unknown";
}

std::string next_step(OrderStatus status) {
    std::string action{"unknown"};

    switch (status) {
        case OrderStatus::received:
            action = "Confirm order";
            break;
        case OrderStatus::preparing:
            action = "Pack order";
            break;
        case OrderStatus::sent:
            action = "Track delivery";
            break;
    }

    return action;
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

    check_text("status_text(received)", "received", status_text(OrderStatus::received), checks, failed);
    check_text("status_text(preparing)", "preparing", status_text(OrderStatus::preparing), checks, failed);
    check_text("status_text(sent)", "sent", status_text(OrderStatus::sent), checks, failed);

    check_text("next_step(received)", "Confirm order", next_step(OrderStatus::received), checks, failed);
    check_text("next_step(preparing)", "Pack order", next_step(OrderStatus::preparing), checks, failed);
    check_text("next_step(sent)", "Track delivery", next_step(OrderStatus::sent), checks, failed);

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

<!-- output: order_switch_tests -->
```text
PASS status_text(received)
PASS status_text(preparing)
PASS status_text(sent)
PASS next_step(received)
PASS next_step(preparing)
PASS next_step(sent)
Checks: 6, failed: 0
```

Pod wynikiem CLion dopisuje `Process finished with exit code 0`.

</details>

- **6 sprawdzeń:** po trzy dla `status_text` i `next_step`, po jednym dla każdego stanu.
- **Wyniki oczekiwane to gotowe napisy z tabel**, a nie wyniki drugiego wywołania sprawdzanej funkcji (lekcja 13.1).

## 5. Diagnostyka: brakujący `break`

Ktoś poprawia `next_step` i przez nieuwagę usuwa jedną linijkę: `break;` pod `action = "Confirm order";`. Funkcja wygląda teraz tak:

<!-- fragment -->
```cpp
std::string next_step(OrderStatus status) {
    std::string action{"unknown"};

    switch (status) {
        case OrderStatus::received:
            action = "Confirm order";
        case OrderStatus::preparing:
            action = "Pack order";
            break;
        case OrderStatus::sent:
            action = "Track delivery";
            break;
    }

    return action;
}
```

Nadal ma trzy etykiety i trzy przypisania, a każda linijka z osobna wygląda poprawnie.

**Etapy 2 i 3 trzeciego obowiązkowego uruchomienia.** Wykonaj kroki po kolei:

1. **Przewidź**, zanim cokolwiek zmienisz: czy program się zbuduje? Jeśli tak, które z sześciu sprawdzeń się nie uda i co jego linijka `FAIL` wypisze po `actual`?
2. W programie testowym z punktu 4 usuń linijkę `break;` pod `action = "Confirm order";`. Nic więcej nie zmieniaj, ani testów, ani wyników oczekiwanych.
3. Zbuduj program. Sprawdź, czy kompilator coś zgłosił.
4. Uruchom testy. Zapisz linijkę `FAIL`, podsumowanie i kod zakończenia.
5. Przywróć `break;` i uruchom te same testy jeszcze raz.

<details>
<summary>Co się dzieje i jak to naprawić: otwórz po wykonaniu kroków 1–5</summary>

**Etap:** działanie programu. Program się buduje: każda linijka jest poprawnym C++. Clang przy ustawieniach z lekcji 0.5 nie zgłasza ani błędu, ani ostrzeżenia. Ten program sprawdzamy automatycznie także z dodatkowymi ostrzeżeniami, traktowanymi jak błędy, i również buduje się bez słowa. Niektóre kompilatory potrafią ostrzec przed przejściem do następnej etykiety, ale tylko przy odpowiednich ustawieniach. Nie polegaj na tym: brak ostrzeżenia nie znaczy, że funkcja jest poprawna.

**Co się dzieje dla `OrderStatus::received`:**

| Krok | Co robi program | `action` po tym kroku |
|---|---|---|
| 1 | Tworzy `action` z tekstem zapasowym. | `"unknown"` |
| 2 | `switch` przechodzi do etykiety `case OrderStatus::received:`. | `"unknown"` |
| 3 | Wykonuje `action = "Confirm order";`. | `"Confirm order"` |
| 4 | Nie ma `break`, więc idzie dalej w dół i przechodzi przez etykietę `case OrderStatus::preparing:`. | `"Confirm order"` |
| 5 | Wykonuje `action = "Pack order";`. Nowy tekst zastępuje poprzedni. | `"Pack order"` |
| 6 | `break;` kończy `switch`. | `"Pack order"` |
| 7 | `return action;` zwraca wynik. | zwraca `"Pack order"` |

To **przejście do następnej etykiety** (*fallthrough*): bez `break` wykonywanie nie kończy się na instrukcjach jednej etykiety, tylko płynie dalej, do instrukcji pod kolejną. Dokładnie tak, jak opisuje punkt 2.

**Mapa skutków:**

| Wywołanie | Wynik oczekiwany | Wynik rzeczywisty | Test |
|---|---|---|---|
| `next_step(OrderStatus::received)` | `"Confirm order"` | `"Pack order"` | `FAIL` |
| `next_step(OrderStatus::preparing)` | `"Pack order"` | `"Pack order"` | `PASS` |
| `next_step(OrderStatus::sent)` | `"Track delivery"` | `"Track delivery"` | `PASS` |
| `status_text` dla trzech stanów | jak w tabeli z punktu 4 | bez zmian | `PASS` |

Dla `preparing` i `sent` program zaczyna niżej, od ich własnych etykiet, i dochodzi do ich własnych `break`. Brakujący `break` stoi wyżej, więc tych stanów nie dotyczy. Dlatego błąd widać tylko w jednym teście. Zestaw, który sprawdzałby `next_step` tylko dla `preparing` i `sent`, przeszedłby w całości (lekcja 13.2).

Program testowy z usuniętym `break`, bez innych zmian:

<!-- example: order_switch_tests_fallthrough exit=1 -->
```cpp
#include <iostream>
#include <string>

enum class OrderStatus {
    received,
    preparing,
    sent
};

std::string status_text(OrderStatus status) {
    switch (status) {
        case OrderStatus::received:
            return "received";
        case OrderStatus::preparing:
            return "preparing";
        case OrderStatus::sent:
            return "sent";
    }

    return "unknown";
}

std::string next_step(OrderStatus status) {
    std::string action{"unknown"};

    switch (status) {
        case OrderStatus::received:
            action = "Confirm order";
        case OrderStatus::preparing:
            action = "Pack order";
            break;
        case OrderStatus::sent:
            action = "Track delivery";
            break;
    }

    return action;
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

    check_text("status_text(received)", "received", status_text(OrderStatus::received), checks, failed);
    check_text("status_text(preparing)", "preparing", status_text(OrderStatus::preparing), checks, failed);
    check_text("status_text(sent)", "sent", status_text(OrderStatus::sent), checks, failed);

    check_text("next_step(received)", "Confirm order", next_step(OrderStatus::received), checks, failed);
    check_text("next_step(preparing)", "Pack order", next_step(OrderStatus::preparing), checks, failed);
    check_text("next_step(sent)", "Track delivery", next_step(OrderStatus::sent), checks, failed);

    std::cout << "Checks: " << checks << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

<!-- output: order_switch_tests_fallthrough -->
```text
PASS status_text(received)
PASS status_text(preparing)
PASS status_text(sent)
FAIL next_step(received): expected "Confirm order", actual "Pack order"
PASS next_step(preparing)
PASS next_step(sent)
Checks: 6, failed: 1
```

Kod zakończenia: 1.

**Poprawka:** przywróć `break;` pod `action = "Confirm order";`. Program jest znów taki jak w punkcie 4. Te same testy, z tymi samymi wynikami oczekiwanymi, wypisują sześć razy `PASS` i `Checks: 6, failed: 0`, a program kończy się kodem 0.

</details>

## 6. Etykieta `default` i nowy stan

Sklep wprowadza czwarty stan: zamówienie anulowane. Ktoś dopisuje do typu wartość `cancelled`, ale zapomina uzupełnić `status_text`:

<!-- fragment -->
```cpp
enum class OrderStatus {
    received,
    preparing,
    sent,
    cancelled
};

std::string status_text(OrderStatus status) {
    switch (status) {
        case OrderStatus::received:
            return "received";
        case OrderStatus::preparing:
            return "preparing";
        case OrderStatus::sent:
            return "sent";
    }

    return "unknown";
}
```

Taki program się zbuduje. `cancelled` nie ma etykiety, więc dla anulowanego zamówienia program pominie wnętrze `switch` i funkcja zwróci `"unknown"`. Clang przy ustawieniach z lekcji 0.5 wypisuje jednak podczas budowania **ostrzeżenie kompilatora** (*compiler warning*) przy linijce `switch (status) {`:

```text
warning: enumeration value 'cancelled' not handled in switch [-Wswitch]
```

Kompilator zna wszystkie wartości typu `OrderStatus` i widzi, że jedna z nich nie ma w tym `switch` etykiety. W nawiasie kwadratowym podaje nazwę tego ostrzeżenia, `-Wswitch`. Dlatego `switch` to dobre miejsce na obsługę wszystkich stanów: po dodaniu nowej wartości kompilator może wskazać `switch`, który trzeba uzupełnić.

Pamiętaj jednak:

- to **ostrzeżenie**, a nie błąd: program się buduje i działa, tylko dla `cancelled` zwraca tekst zapasowy;
- czy takie ostrzeżenie się pojawi i jak brzmi, zależy od kompilatora i jego ustawień;
- przy ustawieniu, które traktuje ostrzeżenia jak błędy, budowanie się zatrzyma, a komunikat zacznie się od `error:` zamiast `warning:`;
- **brak ostrzeżenia nie dowodzi, że każdy stan jest dobrze obsłużony.** Kompilator sprawdza tylko, czy każda wartość ma etykietę, a nie, czy etykieta robi to, co trzeba.

Tego ostrzeżenia nie sprawdzamy automatycznie, dlatego ten kod jest tylko do przeczytania.

**Etykieta `default`.** `switch` może mieć jedną etykietę specjalną, `default:` (*default label*). Program zaczyna od niej, gdy żadna etykieta `case` nie pasuje:

<!-- example: order_default -->
```cpp
#include <iostream>
#include <string>

enum class OrderStatus {
    received,
    preparing,
    sent,
    cancelled
};

std::string status_text(OrderStatus status) {
    switch (status) {
        case OrderStatus::received:
            return "received";
        case OrderStatus::preparing:
            return "preparing";
        case OrderStatus::sent:
            return "sent";
        default:
            return "unknown";
    }
}

int main() {
    std::cout << status_text(OrderStatus::sent) << "\n";
    std::cout << status_text(OrderStatus::cancelled) << "\n";
}
```

<!-- output: order_default -->
```text
sent
unknown
```

- `default:` stoi zwykle na końcu `switch`. Obsługuje **każdą wartość, która nie ma własnej etykiety `case`**.
- `default` jest **opcjonalny**. Wcześniejsze funkcje tej lekcji go nie mają i działają poprawnie.
- Tu zachowanie zapasowe przeszło do wnętrza `switch`. Każda droga przez `switch`, także przez `default`, kończy się `return`, więc za `switch` nie ma już końcowego `return`.
- **Kompilator milczy.** `cancelled` nie ma własnej etykiety, ale trafia do `default`, więc z punktu widzenia kompilatora każda wartość jest obsłużona. Ostrzeżenie o nieobsłużonej wartości się nie pojawia, a program buduje się i dla anulowanego zamówienia zwraca `unknown`.

Tego programu nie musisz uruchamiać: sprawdzamy go automatycznie, a jego wynik widzisz powyżej.

**`default` nie zastępuje etykiet.** Nie wie, czym jest `cancelled`. Robi to samo dla każdej wartości bez własnej etykiety, także dla takiej, którą ktoś doda za rok.

| | Bez `default` | Z `default` |
|---|---|---|
| Nowy stan bez etykiety | program pomija `switch` i dochodzi do zachowania zapasowego za nim | program przechodzi do `default` |
| Ostrzeżenie o nieobsłużonej wartości | może się pojawić | nie pojawia się |
| Co wykryje przeoczenie | ostrzeżenie, jeśli się pojawi, i test nowego stanu | tylko test nowego stanu |

**Zasada tej lekcji:** dla typu `enum class`, którego wszystkie wartości znasz, pisz etykietę `case` dla każdej wartości. `default` dodawaj z rozmysłem: wtedy, gdy dla każdej wartości bez własnej etykiety, także przyszłej, to samo zachowanie jest naprawdę poprawne. Nie dodawaj go tylko po to, żeby kompilator przestał ostrzegać. Z `default` i bez niego przeoczony stan niezawodnie wykrywa tylko test, dlatego po dodaniu wartości do typu dopisujesz też jej testy.

## 7. Błąd, ostrzeżenie, test: kto co wykrywa

Jeszcze jedna pomyłka przy kopiowaniu etykiet. Druga etykieta miała dotyczyć `preparing`, ale została w niej nazwa `received`:

<!-- broken: order_duplicate_case at=14:14 errors=1 error=^duplicate case value 'received' -->
```cpp
#include <iostream>
#include <string>

enum class OrderStatus {
    received,
    preparing,
    sent
};

std::string status_text(OrderStatus status) {
    switch (status) {
        case OrderStatus::received:
            return "received";
        case OrderStatus::received:
            return "preparing";
        case OrderStatus::sent:
            return "sent";
    }

    return "unknown";
}

int main() {
    std::cout << status_text(OrderStatus::preparing) << "\n";
}
```

Ten program się nie zbuduje. Nie musisz go budować: jak program z punktu 6, sprawdzamy go automatycznie. Kompilator zgłasza jeden błąd w linijce 14, przy drugiej etykiecie. Jego komunikat zaczyna się od `duplicate case value 'received'`: wartość `received` ma już etykietę. Clang dopisuje też uwagę `note: previous case defined here`, która wskazuje pierwszą etykietę, w linijce 12. Każda wartość może mieć w jednym `switch` tylko jedną etykietę, bo inaczej program nie wiedziałby, od której zacząć.

W tej lekcji widzisz cztery różne sytuacje. To nie są cztery nazwy tego samego problemu:

| Co się dzieje | Przykład z tej lekcji | Czy program powstaje | Kto to wykrywa |
|---|---|---|---|
| **Błąd kompilacji:** kod łamie regułę języka C++ | dwie etykiety `case OrderStatus::received:` (ten punkt) | nie | kompilator, zawsze |
| **Ostrzeżenie kompilatora:** kod jest poprawnym C++, ale kompilator uznaje go za podejrzany | `cancelled` bez etykiety i bez `default` (punkt 6) | tak | kompilator, jeśli to ostrzeżenie jest włączone |
| **Ostrzeżenie traktowane jak błąd** | to samo, przy ustawieniu, które zamienia ostrzeżenia w błędy | nie | kompilator, tylko przy takim ustawieniu |
| **Błąd w działaniu:** program się buduje, ale daje zły wynik | brakujący `break` w `next_step` (punkt 5) | tak, bez słowa | test |

Kompilator sprawdza reguły języka i, jeśli potrafi, ostrzega przed podejrzanym kodem. Nie zna jednak Twojego kontraktu: nie wie, że dla `received` następnym działaniem jest `"Confirm order"`. To sprawdza tylko test.

## 8. Misja: miejsca parkingowe

Parking pod biurowcem pokazuje na tablicy stan każdego miejsca i krótką instrukcję dla kierowcy. Miejsce jest wolne, zarezerwowane, zajęte albo wyłączone z użytku. Zapisz ten stan jako typ wyliczeniowy `ParkingSpace` i obsłuż go dwiema funkcjami ze `switch`.

**Kontrakt:**

| Stan | `space_text` | `parking_instruction` |
|---|---|---|
| `ParkingSpace::available` | `"available"` | `"Park here"` |
| `ParkingSpace::reserved` | `"reserved"` | `"Reservation required"` |
| `ParkingSpace::occupied` | `"occupied"` | `"Space occupied"` |
| `ParkingSpace::closed` | `"closed"` | `"Do not enter"` |

**Funkcje:**

- `std::string space_text(ParkingSpace state)`: tekst stanu z tabeli. Zapisz ją przez `switch`, w którym każda etykieta od razu zwraca wynik przez `return`. Za `switch` dodaj zachowanie zapasowe, `"unknown"`.
- `std::string parking_instruction(ParkingSpace state)`: instrukcja dla kierowcy z tabeli. Zapisz ją przez `switch`, w którym każda etykieta przypisuje tekst do zmiennej i kończy `switch` przez `break`. Zmienna zaczyna od tekstu zapasowego, `"unknown"`, a funkcja ma jeden `return`, za `switch`.

**Zasady:**

- W obu funkcjach każda z czterech wartości ma własną etykietę `case`. Zapisz etykiety w kolejności z tabeli.
- Nie dodawaj `default`.
- Nie rozwiązuj misji ciągiem `if`. Funkcję sprawdzającą i `main` możesz zorganizować po swojemu.

W `cpp-workspace` utwórz katalog `parking_space`, skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program` i otwórz go w CLionie. Całość napisz w jednym pliku `main.cpp`. `CMakeLists.txt` zostaw bez zmian.

**Kolejność pracy:**

1. **Najpierw plan testów.** Zanim napiszesz kod, przygotuj tabelę sprawdzeń: nazwę sprawdzenia, wywołanie i wynik oczekiwany z kontraktu, dla obu funkcji i każdej z czterech wartości. Dopisz pod nią przewidywanie: które sprawdzenie się nie uda, gdy w `parking_instruction` zabraknie `break` pod etykietą `reserved`, i jaki tekst pojawi się wtedy po `actual`.
2. Zdefiniuj `ParkingSpace` i napisz obie funkcje.
3. Napisz program testowy: `check_text` z lekcji 13.3, sprawdzenia z Twojej tabeli, a na końcu podsumowanie i kod zakończenia jak w punkcie 4.
4. **To czwarte obowiązkowe uruchomienie:** uruchom program testowy z poprawnymi funkcjami. Wszystkie sprawdzenia powinny wypisać `PASS`, a kod zakończenia powinien wynosić 0.
5. **Celowa usterka.** W `parking_instruction` usuń `break` pod etykietą `ParkingSpace::reserved`. Testów i wyników oczekiwanych nie zmieniaj. **To piąte obowiązkowe uruchomienie:** zbuduj program i uruchom testy. Zapisz, czy kompilator coś zgłosił, które sprawdzenie się nie udało, co wypisało po `actual` i jaki jest kod zakończenia. Porównaj to z przewidywaniem z kroku 1. Potem przywróć `break` i uruchom te same testy jeszcze raz.

Nie musisz uruchamiać innych wersji. Jeśli chcesz, sprawdź jeszcze, co się stanie, gdy w `parking_instruction` usuniesz całą etykietę `closed` razem z jej instrukcjami: co zgłosi kompilator i który test się nie uda.

### Kryterium sukcesu

- [ ] Program buduje się jako C++20, a `CMakeLists.txt` jest taki jak w lekcji 0.5.
- [ ] `ParkingSpace` jest typem `enum class` z czterema wartościami z kontraktu.
- [ ] `space_text` używa `switch`: każda etykieta kończy funkcję przez `return`, a za `switch` stoi zachowanie zapasowe.
- [ ] `parking_instruction` używa `switch`: każda etykieta przypisuje tekst i kończy `switch` przez `break`, a funkcja ma jeden `return`, za `switch`.
- [ ] Obie funkcje mają etykietę `case` dla każdej z czterech wartości, żadna wartość się nie powtarza, a teksty zgadzają się z tabelą co do litery.
- [ ] Żadna etykieta nie przechodzi przypadkiem do następnej.
- [ ] Żadna z funkcji nie ma `default`, a umiesz powiedzieć, co zmieniłby `default` dla nowego, piątego stanu.
- [ ] Program testowy sprawdza obie funkcje dla każdej z czterech wartości, a wyniki oczekiwane pochodzą z tabeli, nie z wywołań sprawdzanych funkcji.
- [ ] Z poprawnymi funkcjami wszystkie sprawdzenia przechodzą, a kod zakończenia wynosi 0.
- [ ] Po usunięciu `break` pod `reserved` program się buduje, `FAIL` wypisuje tylko sprawdzenie `parking_instruction` dla `reserved`, a kod zakończenia wynosi 1. Wynik zgadza się z Twoim przewidywaniem albo umiesz wyjaśnić różnicę.
- [ ] Po przywróceniu `break` te same testy, bez zmian, znów przechodzą z kodem 0.
- [ ] Umiesz powiedzieć, dlaczego samo zbudowanie programu nie dowodzi, że każdy stan jest dobrze obsłużony.

Gdy wynik się zgadza, możesz zapisać projekt w Gicie, jak w lekcji 1.5: `main.cpp` i `CMakeLists.txt`, bez katalogu budowania.

<details>
<summary>Podpowiedź 1: wartości</summary>

Ile wartości ma `ParkingSpace` i skąd wiesz, że to wszystkie? Każda z nich potrzebuje własnej etykiety w każdej z dwóch funkcji i własnego tekstu z tabeli. Jak sprawdzisz, że żadnej nie brakuje i żadna się nie powtarza? Porównaj liczbę etykiet `case` w każdej funkcji z liczbą wierszy tabeli.

</details>

<details>
<summary>Podpowiedź 2: sterowanie</summary>

W `space_text` wynik dla danego stanu jest znany od razu, pod etykietą. W `parking_instruction` funkcja zwraca wynik dopiero za `switch`. Która instrukcja kończy całą funkcję, a która tylko `switch`? Gdzie program działa dalej po każdej z nich? Porównaj z tabelą w punkcie 3.

</details>

<details>
<summary>Podpowiedź 3: diagnostyka</summary>

Załóż, że pod etykietą `reserved` program przypisał już tekst, ale nie trafia na `break`. Jaka instrukcja stoi niżej, pod następną etykietą? Co stanie się z tekstem, który jest już w zmiennej, i co funkcja w końcu zwróci? Które z Twoich sprawdzeń to zauważy, a które przejdą bez zmian?

</details>

## 9. Gdy coś pójdzie inaczej

| Co widzisz | Co to znaczy | Co zrobić |
|---|---|---|
| Błąd z `expected ':' after 'case'` | Etykieta kończy się średnikiem zamiast dwukropka. | Zakończ etykietę dwukropkiem: `case ParkingSpace::reserved:`. |
| Błąd z `use of undeclared identifier 'reserved'` | Po `case` stoi nazwa wartości bez nazwy typu. | Pisz `case ParkingSpace::reserved:`. |
| Błąd z `duplicate case value` | Dwie etykiety mają tę samą wartość, na przykład po skopiowaniu (punkt 7). | Popraw drugą z nich na wartość, której brakuje. |
| Błąd z `value of type 'OrderStatus' is not implicitly convertible to 'ParkingSpace'` | Etykieta ma wartość innego typu niż wartość w nawiasach `switch`, na przykład po skopiowaniu z punktu 1. | Użyj wartości typu `ParkingSpace`. |
| Błąd z `statement requires expression of integer type` przy `switch` | W nawiasach `switch` stoi tekst `std::string`. | `switch` działa z liczbami całkowitymi i typami wyliczeniowymi. Teksty porównuj w ciągu `if`, jak w `parse_status` z lekcji 14.1. |
| Ostrzeżenie z `enumeration value '…' not handled in switch` | Jedna z wartości nie ma w tym `switch` etykiety `case` (punkt 6). | Dopisz etykietę dla tej wartości, a w testach sprawdź jej wynik. |
| `FAIL` jednego stanu, a po `actual` tekst kolejnej etykiety | Pod etykietą tego stanu brakuje `break`, więc wykonywanie przechodzi do następnej (punkt 5). | Dodaj `break;` po przypisaniu. |
| `FAIL` jednego stanu, a po `actual` stoi `unknown` | Ta wartość nie ma etykiety `case`, więc funkcja zwraca tekst zapasowy. | Dopisz etykietę z właściwym tekstem. |

## 10. Wyjaśnij

Odpowiedz własnymi słowami, najlepiej na piśmie. Dopiero potem porównaj z przykładowymi odpowiedziami.

1. Kiedy `switch` jest czytelniejszy niż kilka warunków `if`, a kiedy zostajesz przy `if`?
2. Co stoi w nawiasach `switch`, a co oznacza etykieta `case OrderStatus::sent:`?
3. Czy etykieta `case` kończy wykonywanie instrukcji spod poprzedniej etykiety?
4. Co robi `break`, a co `return`? Gdzie program działa dalej po każdym z nich?
5. Co dzieje się z wartością `action` w `next_step` po wykonaniu `break`?
6. Czy po `return` pod etykietą potrzebny jest `break`?
7. Dlaczego po usunięciu `break` pod `"Confirm order"` zmienia się wynik tylko dla `received`?
8. Do czego służy `default` i dlaczego może ukryć nowy stan, którego nikt nie dopisał do `switch`?
9. Czy brak ostrzeżenia kompilatora dowodzi, że `switch` dobrze obsługuje każdy stan?
10. Czym różni się błąd z dwiema etykietami `received` od błędu z brakującym `break`?
11. Dlaczego testujesz funkcję dla każdej wartości `enum class`, a nie tylko dla jednej czy dwóch?

<details>
<summary>Przykładowe odpowiedzi</summary>

1. Gdy wybierasz według jednej wartości z kilkoma znanymi możliwościami, na przykład stanu `enum class`, i dla każdej robisz coś innego: etykiety tworzą listę obsłużonych stanów. Przy `if` zostajesz, gdy warunki są różne, na przykład zakresy albo porównania kilku zmiennych, i gdy porównujesz teksty, bo `switch` nie działa z `std::string`.
2. Wartość, według której program wybiera, na przykład zmienna `status`. Etykieta oznacza miejsce, od którego program zaczyna, gdy ta wartość to `OrderStatus::sent`.
3. Nie. Etykieta oznacza tylko miejsce rozpoczęcia. Jeśli wykonywanie dojdzie do następnej etykiety, program przechodzi przez nią i wykonuje instrukcje, które stoją pod nią.
4. `break` kończy `switch`: program działa dalej od pierwszej instrukcji za `switch`, w tej samej funkcji. `return` kończy całą funkcję: program wraca do miejsca wywołania z wynikiem funkcji.
5. Zachowuje tekst przypisany pod etykietą. `break` tylko przenosi wykonywanie za `switch`, do `return action;`, który zwraca ten tekst.
6. Nie. `return` kończy całą funkcję, więc `break` pod nim nigdy by się nie wykonał.
7. Dla `received` wykonywanie przechodzi do etykiety `preparing` i przypisuje `"Pack order"`, który zastępuje `"Confirm order"`. Dla `preparing` i `sent` program zaczyna od ich własnych etykiet, niżej, i dochodzi do ich własnych `break`.
8. `default` to miejsce rozpoczęcia dla każdej wartości bez własnej etykiety `case`. Nowy stan trafia do `default` i dostaje jego zachowanie, na przykład tekst zapasowy. Kompilator uznaje go za obsłużony, więc nie ostrzega, a program buduje się i działa dalej.
9. Nie. Ostrzeżenie może być wyłączone albo kompilator może go wcale nie mieć, a `default` je wycisza. Nawet gdy każda wartość ma etykietę, etykieta może zwracać zły tekst albo nie mieć `break`. Brakujący `break` z punktu 5 buduje się bez ostrzeżeń.
10. Dwie etykiety z tą samą wartością łamią regułę języka, więc program się nie buduje, a kompilator zawsze to zgłasza. Brakujący `break` to poprawny C++: program się buduje i działa, tylko daje zły wynik, który wykrywa dopiero test.
11. Bo każda etykieta to osobna droga przez funkcję, a błąd pod jedną etykietą zmienia wynik tylko dla jednego stanu. Zestaw, który pomija ten stan, przejdzie mimo błędu, jak sprawdzenia `preparing` i `sent` w punkcie 5.

</details>

## Podsumowanie

- `switch` wybiera według jednej wartości, na przykład stanu `enum class`. Każda etykieta `case` nazywa jedną wartość i oznacza miejsce, od którego program zaczyna.
- **Etykieta sama niczego nie kończy.** Po wejściu do etykiety program wykonuje kolejne instrukcje w dół, także pod następnymi etykietami, aż coś zakończy wykonywanie.
- `return` kończy całą funkcję i nie potrzebuje `break`. `break` kończy tylko `switch`, a program działa dalej od instrukcji za nim.
- Brakujący `break` daje **przejście do następnej etykiety**: program się buduje, a wynik jednego stanu jest zły. Wykrywa to test tego stanu.
- `default` obsługuje każdą wartość bez własnej etykiety, także nową. Jest opcjonalny, a jego obecność może wyciszyć ostrzeżenie o nieobsłużonej wartości. Dodajesz go z rozmysłem, nie z przyzwyczajenia.
- Błąd kompilacji, ostrzeżenie, ostrzeżenie traktowane jak błąd i błąd w działaniu to cztery różne rzeczy. Ostrzeżenia pomagają, ale nie zastępują testów.
- Każdą wartość typu wyliczeniowego testujesz w każdej funkcji, która ją obsługuje.

## Co dalej

Funkcje z tej lekcji dostają stan i zamieniają go na tekst. W [lekcji 14.3: Funkcja mówi, dlaczego odmówiła](lesson_03_function_explains_refusal.md) typ wyliczeniowy stanie się wynikiem funkcji: funkcja, która odmawia, powie nazwanym wynikiem, dlaczego odmówiła.

---

## Przykładowe rozwiązania

Zajrzyj tutaj **po własnej próbie**. Twoje nazwy sprawdzeń, nazwy zmiennych i kolejność sprawdzeń mogą się różnić, jeśli spełniają kontrakt i listę kontrolną.

<details>
<summary>Punkt 8: misja, miejsca parkingowe</summary>

**Plan testów:**

| Sprawdzenie | Wywołanie | Wynik oczekiwany |
|---|---|---|
| `space_text(available)` | `space_text(ParkingSpace::available)` | `"available"` |
| `space_text(reserved)` | `space_text(ParkingSpace::reserved)` | `"reserved"` |
| `space_text(occupied)` | `space_text(ParkingSpace::occupied)` | `"occupied"` |
| `space_text(closed)` | `space_text(ParkingSpace::closed)` | `"closed"` |
| `parking_instruction(available)` | `parking_instruction(ParkingSpace::available)` | `"Park here"` |
| `parking_instruction(reserved)` | `parking_instruction(ParkingSpace::reserved)` | `"Reservation required"` |
| `parking_instruction(occupied)` | `parking_instruction(ParkingSpace::occupied)` | `"Space occupied"` |
| `parking_instruction(closed)` | `parking_instruction(ParkingSpace::closed)` | `"Do not enter"` |

**Przewidywanie:** bez `break` pod `reserved` wykonywanie przejdzie do etykiety `occupied`, a ta przypisze `"Space occupied"`. Nie uda się tylko `parking_instruction(reserved)`, z `"Space occupied"` po `actual`. Pozostałe siedem sprawdzeń przejdzie, a kod zakończenia wyniesie 1.

**`main.cpp`:**

<!-- example: parking_space_tests -->
```cpp
#include <iostream>
#include <string>

enum class ParkingSpace {
    available,
    reserved,
    occupied,
    closed
};

std::string space_text(ParkingSpace state) {
    switch (state) {
        case ParkingSpace::available:
            return "available";
        case ParkingSpace::reserved:
            return "reserved";
        case ParkingSpace::occupied:
            return "occupied";
        case ParkingSpace::closed:
            return "closed";
    }

    return "unknown";
}

std::string parking_instruction(ParkingSpace state) {
    std::string instruction{"unknown"};

    switch (state) {
        case ParkingSpace::available:
            instruction = "Park here";
            break;
        case ParkingSpace::reserved:
            instruction = "Reservation required";
            break;
        case ParkingSpace::occupied:
            instruction = "Space occupied";
            break;
        case ParkingSpace::closed:
            instruction = "Do not enter";
            break;
    }

    return instruction;
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

    check_text("space_text(available)", "available", space_text(ParkingSpace::available), checks, failed);
    check_text("space_text(reserved)", "reserved", space_text(ParkingSpace::reserved), checks, failed);
    check_text("space_text(occupied)", "occupied", space_text(ParkingSpace::occupied), checks, failed);
    check_text("space_text(closed)", "closed", space_text(ParkingSpace::closed), checks, failed);

    check_text("parking_instruction(available)", "Park here", parking_instruction(ParkingSpace::available), checks, failed);
    check_text("parking_instruction(reserved)", "Reservation required", parking_instruction(ParkingSpace::reserved), checks, failed);
    check_text("parking_instruction(occupied)", "Space occupied", parking_instruction(ParkingSpace::occupied), checks, failed);
    check_text("parking_instruction(closed)", "Do not enter", parking_instruction(ParkingSpace::closed), checks, failed);

    std::cout << "Checks: " << checks << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

<!-- output: parking_space_tests -->
```text
PASS space_text(available)
PASS space_text(reserved)
PASS space_text(occupied)
PASS space_text(closed)
PASS parking_instruction(available)
PASS parking_instruction(reserved)
PASS parking_instruction(occupied)
PASS parking_instruction(closed)
Checks: 8, failed: 0
```

Kod zakończenia: 0.

- **`space_text`:** cztery etykiety, każda kończy funkcję przez `return`, więc żadna nie potrzebuje `break`. Za `switch` stoi zachowanie zapasowe.
- **`parking_instruction`:** cztery etykiety, każda przypisuje tekst i kończy `switch` przez `break`. Jedyny `return` stoi za `switch` i zwraca to, co przypisała etykieta.
- **Ostatni `break`, pod `closed`:** za nim jest już tylko klamra zamykająca `switch`, więc bez niego wynik byłby taki sam. Warto go jednak pisać: gdyby ktoś dopisał pod `closed` kolejną etykietę, brak tego `break` stałby się błędem.
- **Bez `default`:** każda z czterech wartości ma etykietę. Gdyby ktoś dodał do typu piąty stan, Clang mógłby ostrzec przy obu `switch`. Z `default` ostrzeżenia by nie było, a nowy stan dostałby po cichu zachowanie z `default`. W obu wersjach przeoczenie niezawodnie wykrywa tylko test nowego stanu.

**Celowa usterka:** w `parking_instruction` nie ma `break` pod `instruction = "Reservation required";`. Zmienia się tylko to jedno miejsce, a program testowy zostaje bez zmian:

<!-- example: parking_space_tests_fallthrough exit=1 -->
```cpp
#include <iostream>
#include <string>

enum class ParkingSpace {
    available,
    reserved,
    occupied,
    closed
};

std::string space_text(ParkingSpace state) {
    switch (state) {
        case ParkingSpace::available:
            return "available";
        case ParkingSpace::reserved:
            return "reserved";
        case ParkingSpace::occupied:
            return "occupied";
        case ParkingSpace::closed:
            return "closed";
    }

    return "unknown";
}

std::string parking_instruction(ParkingSpace state) {
    std::string instruction{"unknown"};

    switch (state) {
        case ParkingSpace::available:
            instruction = "Park here";
            break;
        case ParkingSpace::reserved:
            instruction = "Reservation required";
        case ParkingSpace::occupied:
            instruction = "Space occupied";
            break;
        case ParkingSpace::closed:
            instruction = "Do not enter";
            break;
    }

    return instruction;
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

    check_text("space_text(available)", "available", space_text(ParkingSpace::available), checks, failed);
    check_text("space_text(reserved)", "reserved", space_text(ParkingSpace::reserved), checks, failed);
    check_text("space_text(occupied)", "occupied", space_text(ParkingSpace::occupied), checks, failed);
    check_text("space_text(closed)", "closed", space_text(ParkingSpace::closed), checks, failed);

    check_text("parking_instruction(available)", "Park here", parking_instruction(ParkingSpace::available), checks, failed);
    check_text("parking_instruction(reserved)", "Reservation required", parking_instruction(ParkingSpace::reserved), checks, failed);
    check_text("parking_instruction(occupied)", "Space occupied", parking_instruction(ParkingSpace::occupied), checks, failed);
    check_text("parking_instruction(closed)", "Do not enter", parking_instruction(ParkingSpace::closed), checks, failed);

    std::cout << "Checks: " << checks << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

<!-- output: parking_space_tests_fallthrough -->
```text
PASS space_text(available)
PASS space_text(reserved)
PASS space_text(occupied)
PASS space_text(closed)
PASS parking_instruction(available)
FAIL parking_instruction(reserved): expected "Reservation required", actual "Space occupied"
PASS parking_instruction(occupied)
PASS parking_instruction(closed)
Checks: 8, failed: 1
```

Kod zakończenia: 1.

- **Kompilator:** nie zgłasza niczego. Program jest poprawnym C++.
- **Przebieg dla `reserved`:** etykieta `reserved` przypisuje `"Reservation required"`, ale nie ma `break`, więc wykonywanie przechodzi do etykiety `occupied` i przypisuje `"Space occupied"`. Dopiero `break` pod `occupied` kończy `switch`.
- **Testy:** nie udaje się tylko `parking_instruction(reserved)`. `occupied` zaczyna od własnej etykiety, a w `space_text` nic się nie zmieniło.
- **Jeśli Twoje etykiety stoją w innej kolejności,** po `actual` pojawi się tekst etykiety, która u Ciebie stoi pod `reserved`. Gdyby `reserved` była ostatnia, usunięcie jej `break` niczego by nie zmieniło: za nią nie ma już żadnej instrukcji.

**Po naprawie:** po przywróceniu `break` program jest znów taki jak pierwsza wersja. Te same osiem sprawdzeń wypisuje `PASS` i `Checks: 8, failed: 0`, a kod zakończenia wynosi 0.

**Samoocena.** Porównaj swoją pracę z listą kontrolną w punkcie 8. Szczególnie sprawdź:
- czy umiesz wyjaśnić, dlaczego etykiety w `space_text` nie potrzebują `break`, a w `parking_instruction` potrzebuje go każda;
- czy obie funkcje mają po cztery etykiety i żadna wartość się nie powtarza;
- czy wyniki oczekiwane w testach to napisy z kontraktu;
- czy Twoje przewidywanie z kroku 1 zgadzało się z wynikiem kroku 5, a jeśli nie, czy umiesz wyjaśnić różnicę;
- czy umiesz powiedzieć, co zmieniłby `default` w każdej z dwóch funkcji.

Jeśli w jednym z tych punktów odpowiedź brzmi „nie”, wróć do odpowiedniego punktu lekcji, zanim przejdziesz dalej.

</details>

**Poprzednia lekcja:** [Lekcja 14.1: Stan z nazwą zamiast tekstu](lesson_01_named_state_instead_of_text.md) · **Następna lekcja:** [Lekcja 14.3: Funkcja mówi, dlaczego odmówiła](lesson_03_function_explains_refusal.md) · [Opis kursu](../../README.md)

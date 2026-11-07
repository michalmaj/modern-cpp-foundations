# Lekcja 13.2: Przypadki, które wykrywają błędy

**Polski** · [English](lesson_02_test_cases_that_catch_bugs.en.md) · [Opis kursu](../../README.md)

> **Moduł 13, lekcja 2** · około 90–110 minut, można ją podzielić na dwa podejścia
> **Potrzebujesz:** katalogu `cpp-workspace` i oryginalnego projektu `lesson_05_first_program`, jak dotąd. Przyda się też Twój program testowy z misji lekcji 13.1.
> **Wersja pilotażowa.** Programy z tej lekcji sprawdzamy automatycznie na Windowsie, Ubuntu i macOS, razem z ich kodem zakończenia.

## Zanim zaczniesz

Ta lekcja zakłada, że:

- piszesz program testowy z lekcji 13.1: wynik oczekiwany z kontraktu, `PASS` albo `FAIL`, liczniki testów i niepowodzeń, kod zakończenia 0 albo 1;
- wiesz, że `std::cout` wypisuje wartość `bool` jako `1` albo `0` (lekcja 3.2);
- łączysz warunki operatorami `&&`, `||` i `!` (lekcja 3.4);
- definiujesz `struct`, tworzysz rekord w nawiasach klamrowych i przekazujesz go funkcji przez `const&` (lekcje 8.1 i 8.3);
- sprawdzasz granicę zakresu z obu stron (od Modułu 3).

## Sytuacja

Biblioteka decyduje, czy czytelnik może wypożyczyć kolejną książkę. Decyzję podejmuje funkcja, która zwraca tylko „tak” albo „nie”. Ktoś ją napisał, ktoś inny przygotował trzy testy i wszystkie przechodzą. Czy to znaczy, że funkcja jest dobra?

Lekcja 13.1 pokazała, **jak sprawdzić jeden wynik**. Ta lekcja pokazuje, **które wyniki warto sprawdzić**.

Po tej lekcji będziesz:

- odróżniać cztery różne rzeczy: działający program testowy, poprawne wyniki oczekiwane, dobrze dobrane przypadki i poprawną funkcję;
- dobierać przypadki typowe, graniczne i niepoprawnych danych na podstawie kontraktu;
- sprawdzać każdy warunek osobnym przypadkiem;
- oceniać zestaw testów po tym, czy odróżnia poprawną funkcję od wersji z błędem;
- rozpoznawać, że błąd jest w samym teście, a nie w funkcji.

## 1. Trzy razy PASS: i co z tego?

W misji z lekcji 13.1 błąd w `print_cost` wykrywał tylko test dla 4 stron. Gdyby tego testu zabrakło, wszystkie pozostałe by przeszły, a program testowy zakończyłby się kodem 0. **Zielony wynik wszystkich uruchomionych testów nie dowodzi, że funkcja jest poprawna.** Mówi tylko, że wybrane przypadki nie ujawniły niezgodności.

Te cztery własności nie są tym samym:

| Własność | Pytanie, które ją sprawdza |
|---|---|
| program testowy działa poprawnie | czy każda niezgodność daje `FAIL` i kod zakończenia 1? (lekcja 13.1) |
| wyniki oczekiwane są poprawne | czy każda wartość w teście wynika z kontraktu? |
| przypadki są dobrze dobrane | czy dla wersji funkcji z błędem któryś test dałby `FAIL`? |
| funkcja jest poprawna | czy zwraca to, co mówi kontrakt, dla wszystkich dopuszczalnych danych? |

Program testowy może działać bez zarzutu, a mimo to sprawdzać za mało. Tej lekcji chodzi o trzecią własność: o dobór przypadków.

## 2. Kontrakt: czy czytelnik może wypożyczyć kolejną książkę

Prośba o wypożyczenie to rekord z trzema polami:

<!-- fragment -->
```cpp
struct LoanRequest {
    int borrowed_books;
    int days_overdue;
    bool blocked;
};
```

**Kontrakt funkcji `bool can_borrow(const LoanRequest& request)`:**

- `borrowed_books`: liczba aktualnie wypożyczonych książek, dopuszczalnie od 0 do 5;
- `days_overdue`: liczba dni zaległości ze zwrotem, dopuszczalnie od 0 do 30;
- `blocked`: czy konto jest zablokowane, `true` albo `false`;
- kolejne wypożyczenie jest możliwe **wtedy i tylko wtedy**, gdy jednocześnie: `borrowed_books < 5`, `days_overdue == 0` i konto nie jest zablokowane;
- dla wartości spoza dopuszczalnych zakresów funkcja zwraca `false`.

Funkcja zwraca tylko `bool`. Nie mówi, **dlaczego** odmówiła.

Poprawna funkcja najpierw odrzuca niedopuszczalne dane, a potem sprawdza trzy warunki naraz:

<!-- fragment -->
```cpp
bool can_borrow(const LoanRequest& request) {
    if (request.borrowed_books < 0 || request.borrowed_books > 5) {
        return false;
    }

    if (request.days_overdue < 0 || request.days_overdue > 30) {
        return false;
    }

    return request.borrowed_books < 5 && request.days_overdue == 0 && !request.blocked;
}
```

## 3. Sprawdzanie wyniku `bool`

Funkcja sprawdzająca z lekcji 13.1 porównywała liczby. Tutaj wynik jest typu `bool`, więc potrzebna jest jej odmiana z dwiema zmianami:

<!-- fragment -->
```cpp
std::string bool_text(bool value) {
    if (value) {
        return "true";
    }

    return "false";
}

void check_bool(const std::string& name, bool expected, bool actual, int& tests, int& failed) {
    ++tests;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << bool_text(expected) << ", actual " << bool_text(actual) << "\n";
        ++failed;
    }
}
```

- **Typy parametrów:** `expected` i `actual` są typu `bool`. Reszta działa jak `check_equal`: ten sam licznik testów, ten sam licznik niepowodzeń, ten sam format.
- **`bool_text`:** `std::cout` wypisałby `bool` jako `1` albo `0`. Linijka `FAIL D {5, 0, false}: expected false, actual true` czyta się łatwiej niż `expected 0, actual 1`, a słowa `true` i `false` są dokładnie tymi, które piszesz w kodzie.
- **Nazwa testu** to litera przypadku i dane rekordu w kolejności pól: `{książki, dni zaległości, blokada}`. Po linijce `FAIL` od razu widać, dla jakich danych funkcja się pomyliła.

## 4. Słaby zestaw: A, B i J

Pierwszy zestaw testów wygląda rozsądnie: dwa razy „tak”, raz zdecydowanie „nie”.

| Przypadek | `borrowed_books` | `days_overdue` | `blocked` | Wynik oczekiwany | Skąd |
|---|---:|---:|---|---|---|
| A | 0 | 0 | `false` | `true` | wszystkie warunki spełnione |
| B | 2 | 0 | `false` | `true` | wszystkie warunki spełnione |
| J | 5 | 2 | `true` | `false` | limit osiągnięty, zaległość i blokada |

Ten program sprawdza tym zestawem **wersję funkcji, która ma jedną usterkę**. Kod programu testowego jest poprawny.

<!-- example: loan_weak_tests_bug -->
```cpp
#include <iostream>
#include <string>

struct LoanRequest {
    int borrowed_books;
    int days_overdue;
    bool blocked;
};

bool can_borrow(const LoanRequest& request) {
    if (request.borrowed_books < 0 || request.borrowed_books > 5) {
        return false;
    }

    if (request.days_overdue < 0 || request.days_overdue > 30) {
        return false;
    }

    return request.borrowed_books < 5 && request.days_overdue == 0;
}

std::string bool_text(bool value) {
    if (value) {
        return "true";
    }

    return "false";
}

void check_bool(const std::string& name, bool expected, bool actual, int& tests, int& failed) {
    ++tests;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << bool_text(expected) << ", actual " << bool_text(actual) << "\n";
        ++failed;
    }
}

int main() {
    int tests{0};
    int failed{0};

    check_bool("A {0, 0, false}", true, can_borrow(LoanRequest{0, 0, false}), tests, failed);
    check_bool("B {2, 0, false}", true, can_borrow(LoanRequest{2, 0, false}), tests, failed);
    check_bool("J {5, 2, true}", false, can_borrow(LoanRequest{5, 2, true}), tests, failed);

    std::cout << "Tests: " << tests << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

**To pierwsze obowiązkowe uruchomienie.** W `cpp-workspace` utwórz katalog `lesson_13_2`, skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program` i otwórz go w CLionie. Zastąp zawartość `main.cpp` tym programem, zbuduj go i uruchom. Kolejne programy z tej lekcji wpisujesz w ten sam `main.cpp`. **Przewidź** wynik i kod zakończenia.

<details>
<summary>Standardowe wyjście i kod zakończenia</summary>

<!-- output: loan_weak_tests_bug -->
```text
PASS A {0, 0, false}
PASS B {2, 0, false}
PASS J {5, 2, true}
Tests: 3, failed: 0
```

CLion pokazuje `Process finished with exit code 0`.

</details>

**Wszystkie testy przeszły, a funkcja ma błąd.** Porównaj ostatnią linijkę `can_borrow` z poprawną funkcją z punktu 2: brakuje `&& !request.blocked`. Ta wersja **w ogóle nie sprawdza blokady**: zablokowany czytelnik bez zaległości dostałby książkę.

- **Kod 0 oznacza sukces wykonanego zestawu testów, a nie dowód poprawności funkcji.** Program powiedział prawdę: żaden z trzech testów nie wykrył niezgodności.
- **To nie jest wadliwy program testowy** w znaczeniu z lekcji 13.1. Tam program wypisywał `FAIL`, ale kończył się kodem 0. Tutaj mechanizm działa poprawnie: gdyby któryś test się nie udał, byłoby `FAIL` i kod 1. Zawiódł **dobór przypadków**.
- **Dlaczego J nie pomaga:** J narusza trzy warunki naraz. Odrzuca go już limit pięciu książek, więc wynik jest `false` także wtedy, gdy funkcja w ogóle nie patrzy na blokadę. Przypadek „bardzo niepoprawny” sprawdza tylko, czy funkcja odrzuca **któryś** z powodów, a nie czy sprawdza **każdy** z nich.

## 5. Przypadek, który odróżni dwie wersje

Potrzebny jest przypadek, dla którego **poprawna funkcja i ta wersja z błędem zwrócą różne wyniki**. Zanim otworzysz zwinięty blok, zaproponuj taki przypadek: trzy wartości pól i wynik oczekiwany z kontraktu.

<details>
<summary>Jeden z dobrych przypadków</summary>

**F {2, 0, true}:** dwie książki, bez zaległości, konto zablokowane. Według kontraktu wynik to `false`. Wersja z błędem nie patrzy na blokadę i zwraca `true`. Wyniki się różnią, więc test dla F wykryje tę usterkę.

Każdy przypadek, w którym **blokada jest jedynym powodem odmowy**, zadziała tak samo, na przykład `{0, 0, true}`.

</details>

Reguła z tego przykładu: **żeby sprawdzić jeden warunek, naruszaj tylko ten warunek, a wszystkie pozostałe zostaw spełnione.** Wtedy wynik zależy wyłącznie od niego. Test, który daje `FAIL` dla wersji z błędem, to **test ujawniający usterkę** (*bug-revealing test*).

## 6. Przypadki typowe, graniczne i niepoprawnych danych

Mocniejszy zestaw powstaje z kontraktu, punkt po punkcie. Każdy przypadek ma powód, który da się wskazać w kontrakcie:

| Przypadek | `borrowed_books` | `days_overdue` | `blocked` | Wynik oczekiwany | Rodzaj i powód |
|---|---:|---:|---|---|---|
| A | 0 | 0 | `false` | `true` | typowy; najmniejsza liczba książek |
| B | 2 | 0 | `false` | `true` | typowy |
| C | 4 | 0 | `false` | `true` | graniczny: ostatnia liczba książek, przy której wolno wypożyczyć |
| D | 5 | 0 | `false` | `false` | graniczny: limit osiągnięty, jedyny powód odmowy |
| E | 2 | 1 | `false` | `false` | graniczny: najmniejsza zaległość, jedyny powód odmowy |
| F | 2 | 0 | `true` | `false` | blokada jako jedyny powód odmowy |
| G | -1 | 0 | `false` | `false` | niepoprawne dane: ujemna liczba książek |
| H | 6 | 0 | `false` | `false` | niepoprawne dane: liczba książek ponad zakres |
| I | 2 | -1 | `false` | `false` | niepoprawne dane: ujemna zaległość |
| J | 5 | 2 | `true` | `false` | kilka powodów odmowy naraz |
| K | 2 | 30 | `false` | `false` | największa dopuszczalna zaległość |
| L | 2 | 31 | `false` | `false` | niepoprawne dane: zaległość ponad zakres |

- **Przypadek typowy** (*typical case*): zwykłe dane, dla których odpowiedź jest oczywista. Potrzebny, ale sam niewiele sprawdza.
- **Przypadek graniczny** (*boundary case*): dane dokładnie przy granicy z kontraktu, po obu jej stronach. C i D sprawdzają granicę między 4 a 5 książkami, a B i E granicę między brakiem zaległości a jednym dniem. Tu najłatwiej pomylić `<` z `<=` albo `==` z `<=`.
- **Przypadek niepoprawnych danych** (*invalid input*): wartości spoza dopuszczalnego zakresu. Kontrakt mówi, co wtedy zrobić, więc to też są przypadki z jednoznacznym wynikiem oczekiwanym.
- **Zestaw przypadków testowych** (*test suite*) to wszystkie przypadki sprawdzane razem przez jeden program testowy.

**K i L** pokazują granicę dopuszczalnych danych: 30 dni to jeszcze poprawne dane, 31 już nie. Oba dają jednak `false`, każdy z innego powodu: K z powodu zaległości, L z powodu niepoprawnych danych. Funkcja zwraca tylko `bool`, więc test widzi wynik, a nie powód. Ta granica nie zmienia wyniku tej funkcji. **Przypadek graniczny jest najcenniejszy tam, gdzie po obu stronach granicy wynik powinien być różny**, jak przy C i D.

## 7. Mocniejszy zestaw testów

Ten sam program testowy, z wszystkimi dwunastoma przypadkami, sprawdza tę samą wersję funkcji z błędem:

<!-- example: loan_strong_tests_bug exit=1 -->
```cpp
#include <iostream>
#include <string>

struct LoanRequest {
    int borrowed_books;
    int days_overdue;
    bool blocked;
};

bool can_borrow(const LoanRequest& request) {
    if (request.borrowed_books < 0 || request.borrowed_books > 5) {
        return false;
    }

    if (request.days_overdue < 0 || request.days_overdue > 30) {
        return false;
    }

    return request.borrowed_books < 5 && request.days_overdue == 0;
}

std::string bool_text(bool value) {
    if (value) {
        return "true";
    }

    return "false";
}

void check_bool(const std::string& name, bool expected, bool actual, int& tests, int& failed) {
    ++tests;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << bool_text(expected) << ", actual " << bool_text(actual) << "\n";
        ++failed;
    }
}

int main() {
    int tests{0};
    int failed{0};

    check_bool("A {0, 0, false}", true, can_borrow(LoanRequest{0, 0, false}), tests, failed);
    check_bool("B {2, 0, false}", true, can_borrow(LoanRequest{2, 0, false}), tests, failed);
    check_bool("C {4, 0, false}", true, can_borrow(LoanRequest{4, 0, false}), tests, failed);
    check_bool("D {5, 0, false}", false, can_borrow(LoanRequest{5, 0, false}), tests, failed);
    check_bool("E {2, 1, false}", false, can_borrow(LoanRequest{2, 1, false}), tests, failed);
    check_bool("F {2, 0, true}", false, can_borrow(LoanRequest{2, 0, true}), tests, failed);
    check_bool("G {-1, 0, false}", false, can_borrow(LoanRequest{-1, 0, false}), tests, failed);
    check_bool("H {6, 0, false}", false, can_borrow(LoanRequest{6, 0, false}), tests, failed);
    check_bool("I {2, -1, false}", false, can_borrow(LoanRequest{2, -1, false}), tests, failed);
    check_bool("J {5, 2, true}", false, can_borrow(LoanRequest{5, 2, true}), tests, failed);
    check_bool("K {2, 30, false}", false, can_borrow(LoanRequest{2, 30, false}), tests, failed);
    check_bool("L {2, 31, false}", false, can_borrow(LoanRequest{2, 31, false}), tests, failed);

    std::cout << "Tests: " << tests << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

**To drugie obowiązkowe uruchomienie.** W `main.cpp` zastąp `main` tym z dwunastoma testami, a funkcję zostaw z błędem. Uruchom program. **Przewidź**, które testy się nie udadzą. Potem przywróć w `can_borrow` warunek `&& !request.blocked` i uruchom program jeszcze raz.

<details>
<summary>Standardowe wyjście i kod zakończenia dla wersji z błędem</summary>

<!-- output: loan_strong_tests_bug -->
```text
PASS A {0, 0, false}
PASS B {2, 0, false}
PASS C {4, 0, false}
PASS D {5, 0, false}
PASS E {2, 1, false}
FAIL F {2, 0, true}: expected false, actual true
PASS G {-1, 0, false}
PASS H {6, 0, false}
PASS I {2, -1, false}
PASS J {5, 2, true}
PASS K {2, 30, false}
PASS L {2, 31, false}
Tests: 12, failed: 1
```

CLion pokazuje `Process finished with exit code 1`.

</details>

Ten sam błąd, inny zestaw, inny werdykt. Usterkę wykrył **jeden** przypadek: F, jedyny, w którym o odmowie decyduje sama blokada. J, który też ma blokadę, nadal przechodzi.

<details>
<summary>Program i wynik po przywróceniu poprawnej funkcji</summary>

<!-- example: loan_strong_tests -->
```cpp
#include <iostream>
#include <string>

struct LoanRequest {
    int borrowed_books;
    int days_overdue;
    bool blocked;
};

bool can_borrow(const LoanRequest& request) {
    if (request.borrowed_books < 0 || request.borrowed_books > 5) {
        return false;
    }

    if (request.days_overdue < 0 || request.days_overdue > 30) {
        return false;
    }

    return request.borrowed_books < 5 && request.days_overdue == 0 && !request.blocked;
}

std::string bool_text(bool value) {
    if (value) {
        return "true";
    }

    return "false";
}

void check_bool(const std::string& name, bool expected, bool actual, int& tests, int& failed) {
    ++tests;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << bool_text(expected) << ", actual " << bool_text(actual) << "\n";
        ++failed;
    }
}

int main() {
    int tests{0};
    int failed{0};

    check_bool("A {0, 0, false}", true, can_borrow(LoanRequest{0, 0, false}), tests, failed);
    check_bool("B {2, 0, false}", true, can_borrow(LoanRequest{2, 0, false}), tests, failed);
    check_bool("C {4, 0, false}", true, can_borrow(LoanRequest{4, 0, false}), tests, failed);
    check_bool("D {5, 0, false}", false, can_borrow(LoanRequest{5, 0, false}), tests, failed);
    check_bool("E {2, 1, false}", false, can_borrow(LoanRequest{2, 1, false}), tests, failed);
    check_bool("F {2, 0, true}", false, can_borrow(LoanRequest{2, 0, true}), tests, failed);
    check_bool("G {-1, 0, false}", false, can_borrow(LoanRequest{-1, 0, false}), tests, failed);
    check_bool("H {6, 0, false}", false, can_borrow(LoanRequest{6, 0, false}), tests, failed);
    check_bool("I {2, -1, false}", false, can_borrow(LoanRequest{2, -1, false}), tests, failed);
    check_bool("J {5, 2, true}", false, can_borrow(LoanRequest{5, 2, true}), tests, failed);
    check_bool("K {2, 30, false}", false, can_borrow(LoanRequest{2, 30, false}), tests, failed);
    check_bool("L {2, 31, false}", false, can_borrow(LoanRequest{2, 31, false}), tests, failed);

    std::cout << "Tests: " << tests << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

<!-- output: loan_strong_tests -->
```text
PASS A {0, 0, false}
PASS B {2, 0, false}
PASS C {4, 0, false}
PASS D {5, 0, false}
PASS E {2, 1, false}
PASS F {2, 0, true}
PASS G {-1, 0, false}
PASS H {6, 0, false}
PASS I {2, -1, false}
PASS J {5, 2, true}
PASS K {2, 30, false}
PASS L {2, 31, false}
Tests: 12, failed: 0
```

Kod zakończenia: 0.

</details>

**Jak to nazwać uczciwie.** Po poprawce wszystkie testy przechodzą. To nie znaczy „funkcja jest udowodniona jako poprawna”. Znaczy: **przygotowany zestaw testów nie wykrył niezgodności w sprawdzanej wersji funkcji.** Im lepiej dobrane przypadki, tym więcej to zdanie jest warte.

**Więcej testów to nie zawsze lepsze testy.** Gdyby dopisać jeszcze `{1, 0, false}` i `{3, 0, false}`, zestaw byłby dłuższy, ale nie mocniejszy: oba przypadki sprawdzają to samo co B, wszystkie warunki spełnione. Mocniejszy zestaw (*stronger test suite*) to taki, który **odróżnia więcej wersji z błędem**, a nie taki, który ma więcej linijek. Zestaw z punktu 4 był słabym zestawem (*weak test suite*): nie odróżniał poprawnej funkcji od funkcji bez sprawdzania blokady.

## 8. Inne usterki i przypadki, które je wykrywają

Oto trzy kolejne wersje `can_borrow`. Każda różni się od poprawnej funkcji **jednym** miejscem, buduje się bez błędów i dla przypadków A i B daje poprawne wyniki:

| Wersja | Zmiana w funkcji | Skutek według kontraktu |
|---|---|---|
| zła granica limitu | `borrowed_books <= 5` zamiast `borrowed_books < 5` w ostatniej linijce | czytelnik z pięcioma książkami dostaje szóstą |
| zła granica zaległości | `days_overdue <= 1` zamiast `days_overdue == 0` w ostatniej linijce | jeden dzień zaległości nie przeszkadza |
| brak sprawdzenia ujemnej liczby | pierwszy warunek to tylko `request.borrowed_books > 5` | ujemna liczba książek przechodzi jak poprawna |

**Dla każdej wersji wybierz z tabeli A–L przypadek, który ją wykryje**, i przewidź jego linijkę `FAIL`. Zastanów się też, dlaczego słaby zestaw A, B i J przechodzi dla każdej z nich. Dopiero potem otwórz omówienie.

<details>
<summary>Omówienie: trzy wersje i ich wyniki</summary>

**Zła granica limitu.** Wykrywa ją D: pięć książek, bez zaległości i blokady.

<!-- example: loan_strong_tests_limit_bug exit=1 -->
```cpp
#include <iostream>
#include <string>

struct LoanRequest {
    int borrowed_books;
    int days_overdue;
    bool blocked;
};

bool can_borrow(const LoanRequest& request) {
    if (request.borrowed_books < 0 || request.borrowed_books > 5) {
        return false;
    }

    if (request.days_overdue < 0 || request.days_overdue > 30) {
        return false;
    }

    return request.borrowed_books <= 5 && request.days_overdue == 0 && !request.blocked;
}

std::string bool_text(bool value) {
    if (value) {
        return "true";
    }

    return "false";
}

void check_bool(const std::string& name, bool expected, bool actual, int& tests, int& failed) {
    ++tests;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << bool_text(expected) << ", actual " << bool_text(actual) << "\n";
        ++failed;
    }
}

int main() {
    int tests{0};
    int failed{0};

    check_bool("A {0, 0, false}", true, can_borrow(LoanRequest{0, 0, false}), tests, failed);
    check_bool("B {2, 0, false}", true, can_borrow(LoanRequest{2, 0, false}), tests, failed);
    check_bool("C {4, 0, false}", true, can_borrow(LoanRequest{4, 0, false}), tests, failed);
    check_bool("D {5, 0, false}", false, can_borrow(LoanRequest{5, 0, false}), tests, failed);
    check_bool("E {2, 1, false}", false, can_borrow(LoanRequest{2, 1, false}), tests, failed);
    check_bool("F {2, 0, true}", false, can_borrow(LoanRequest{2, 0, true}), tests, failed);
    check_bool("G {-1, 0, false}", false, can_borrow(LoanRequest{-1, 0, false}), tests, failed);
    check_bool("H {6, 0, false}", false, can_borrow(LoanRequest{6, 0, false}), tests, failed);
    check_bool("I {2, -1, false}", false, can_borrow(LoanRequest{2, -1, false}), tests, failed);
    check_bool("J {5, 2, true}", false, can_borrow(LoanRequest{5, 2, true}), tests, failed);
    check_bool("K {2, 30, false}", false, can_borrow(LoanRequest{2, 30, false}), tests, failed);
    check_bool("L {2, 31, false}", false, can_borrow(LoanRequest{2, 31, false}), tests, failed);

    std::cout << "Tests: " << tests << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

<!-- output: loan_strong_tests_limit_bug -->
```text
PASS A {0, 0, false}
PASS B {2, 0, false}
PASS C {4, 0, false}
FAIL D {5, 0, false}: expected false, actual true
PASS E {2, 1, false}
PASS F {2, 0, true}
PASS G {-1, 0, false}
PASS H {6, 0, false}
PASS I {2, -1, false}
PASS J {5, 2, true}
PASS K {2, 30, false}
PASS L {2, 31, false}
Tests: 12, failed: 1
```

Kod zakończenia: 1.

**Zła granica zaległości.** Wykrywa ją E: dwie książki, jeden dzień zaległości, bez blokady.

<!-- example: loan_strong_tests_overdue_bug exit=1 -->
```cpp
#include <iostream>
#include <string>

struct LoanRequest {
    int borrowed_books;
    int days_overdue;
    bool blocked;
};

bool can_borrow(const LoanRequest& request) {
    if (request.borrowed_books < 0 || request.borrowed_books > 5) {
        return false;
    }

    if (request.days_overdue < 0 || request.days_overdue > 30) {
        return false;
    }

    return request.borrowed_books < 5 && request.days_overdue <= 1 && !request.blocked;
}

std::string bool_text(bool value) {
    if (value) {
        return "true";
    }

    return "false";
}

void check_bool(const std::string& name, bool expected, bool actual, int& tests, int& failed) {
    ++tests;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << bool_text(expected) << ", actual " << bool_text(actual) << "\n";
        ++failed;
    }
}

int main() {
    int tests{0};
    int failed{0};

    check_bool("A {0, 0, false}", true, can_borrow(LoanRequest{0, 0, false}), tests, failed);
    check_bool("B {2, 0, false}", true, can_borrow(LoanRequest{2, 0, false}), tests, failed);
    check_bool("C {4, 0, false}", true, can_borrow(LoanRequest{4, 0, false}), tests, failed);
    check_bool("D {5, 0, false}", false, can_borrow(LoanRequest{5, 0, false}), tests, failed);
    check_bool("E {2, 1, false}", false, can_borrow(LoanRequest{2, 1, false}), tests, failed);
    check_bool("F {2, 0, true}", false, can_borrow(LoanRequest{2, 0, true}), tests, failed);
    check_bool("G {-1, 0, false}", false, can_borrow(LoanRequest{-1, 0, false}), tests, failed);
    check_bool("H {6, 0, false}", false, can_borrow(LoanRequest{6, 0, false}), tests, failed);
    check_bool("I {2, -1, false}", false, can_borrow(LoanRequest{2, -1, false}), tests, failed);
    check_bool("J {5, 2, true}", false, can_borrow(LoanRequest{5, 2, true}), tests, failed);
    check_bool("K {2, 30, false}", false, can_borrow(LoanRequest{2, 30, false}), tests, failed);
    check_bool("L {2, 31, false}", false, can_borrow(LoanRequest{2, 31, false}), tests, failed);

    std::cout << "Tests: " << tests << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

<!-- output: loan_strong_tests_overdue_bug -->
```text
PASS A {0, 0, false}
PASS B {2, 0, false}
PASS C {4, 0, false}
PASS D {5, 0, false}
FAIL E {2, 1, false}: expected false, actual true
PASS F {2, 0, true}
PASS G {-1, 0, false}
PASS H {6, 0, false}
PASS I {2, -1, false}
PASS J {5, 2, true}
PASS K {2, 30, false}
PASS L {2, 31, false}
Tests: 12, failed: 1
```

Kod zakończenia: 1.

**Brak sprawdzenia ujemnej liczby.** Wykrywa ją G: minus jedna książka, bez zaległości i blokady.

<!-- example: loan_strong_tests_negative_bug exit=1 -->
```cpp
#include <iostream>
#include <string>

struct LoanRequest {
    int borrowed_books;
    int days_overdue;
    bool blocked;
};

bool can_borrow(const LoanRequest& request) {
    if (request.borrowed_books > 5) {
        return false;
    }

    if (request.days_overdue < 0 || request.days_overdue > 30) {
        return false;
    }

    return request.borrowed_books < 5 && request.days_overdue == 0 && !request.blocked;
}

std::string bool_text(bool value) {
    if (value) {
        return "true";
    }

    return "false";
}

void check_bool(const std::string& name, bool expected, bool actual, int& tests, int& failed) {
    ++tests;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << bool_text(expected) << ", actual " << bool_text(actual) << "\n";
        ++failed;
    }
}

int main() {
    int tests{0};
    int failed{0};

    check_bool("A {0, 0, false}", true, can_borrow(LoanRequest{0, 0, false}), tests, failed);
    check_bool("B {2, 0, false}", true, can_borrow(LoanRequest{2, 0, false}), tests, failed);
    check_bool("C {4, 0, false}", true, can_borrow(LoanRequest{4, 0, false}), tests, failed);
    check_bool("D {5, 0, false}", false, can_borrow(LoanRequest{5, 0, false}), tests, failed);
    check_bool("E {2, 1, false}", false, can_borrow(LoanRequest{2, 1, false}), tests, failed);
    check_bool("F {2, 0, true}", false, can_borrow(LoanRequest{2, 0, true}), tests, failed);
    check_bool("G {-1, 0, false}", false, can_borrow(LoanRequest{-1, 0, false}), tests, failed);
    check_bool("H {6, 0, false}", false, can_borrow(LoanRequest{6, 0, false}), tests, failed);
    check_bool("I {2, -1, false}", false, can_borrow(LoanRequest{2, -1, false}), tests, failed);
    check_bool("J {5, 2, true}", false, can_borrow(LoanRequest{5, 2, true}), tests, failed);
    check_bool("K {2, 30, false}", false, can_borrow(LoanRequest{2, 30, false}), tests, failed);
    check_bool("L {2, 31, false}", false, can_borrow(LoanRequest{2, 31, false}), tests, failed);

    std::cout << "Tests: " << tests << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

<!-- output: loan_strong_tests_negative_bug -->
```text
PASS A {0, 0, false}
PASS B {2, 0, false}
PASS C {4, 0, false}
PASS D {5, 0, false}
PASS E {2, 1, false}
PASS F {2, 0, true}
FAIL G {-1, 0, false}: expected false, actual true
PASS H {6, 0, false}
PASS I {2, -1, false}
PASS J {5, 2, true}
PASS K {2, 30, false}
PASS L {2, 31, false}
Tests: 12, failed: 1
```

Kod zakończenia: 1.

**Mapa usterek.** Linijki A, B i J w każdym z czterech wyników to dokładnie słaby zestaw z punktu 4, więc widać, że dla każdej wersji z błędem przeszedłby bez `FAIL`.

| Usterka | Co działa nadal poprawnie | Słaby zestaw A, B, J | Przypadek ujawniający | Oczekiwany | Rzeczywisty | Dlaczego J jej nie wykrywa |
|---|---|---|---|---|---|---|
| pominięta blokada (punkt 4) | limit, zaległość, zakresy | PASS | F | `false` | `true` | J odrzucają już limit i zaległość |
| zła granica limitu | 0–4 książki, zaległość, blokada, zakresy | PASS | D | `false` | `true` | J odrzucają już zaległość i blokada |
| zła granica zaległości | 0 i 2–30 dni, limit, blokada, zakresy | PASS | E | `false` | `true` | J odrzucają już limit i blokada |
| brak sprawdzenia ujemnej liczby | 0–6 książek, zaległość, blokada | PASS | G | `false` | `true` | J nie ma ujemnej liczby książek |

- Każdą usterkę wykrywa przypadek, w którym **jedyny powód odmowy** to dokładnie ten zepsuty warunek.
- H i I nie wykrywają żadnej z tych wersji: 6 książek i -1 dnia zaległości odrzuca nie tylko sprawdzenie zakresu, ale też ostatnia linijka funkcji. Zostają w zestawie, bo sprawdzają zapis kontraktu o niepoprawnych danych niezależnie od tego, jak funkcja jest napisana. Gdyby ktoś przepisał ją bez osobnego sprawdzania zakresów, z warunkiem `borrowed_books != 5` zamiast `< 5`, H dałby `FAIL`.
- **To nie jest formalna metoda testowania**, tylko sposób sprawdzenia, czy przypadki potrafią coś wykryć: wprowadzasz celowo jedną usterkę i patrzysz, czy któryś test da `FAIL`. Zestaw, który wykrywa te cztery usterki, nie wykryje każdego możliwego błędu.

</details>

## 9. Diagnostyka: FAIL przy poprawnej funkcji

**Sytuacja.** Ktoś dopisał test dla czytelnika z pięcioma książkami. Funkcja `can_borrow` jest tu **poprawna**, taka jak w punkcie 2.

<!-- example: loan_wrong_expected exit=1 -->
```cpp
#include <iostream>
#include <string>

struct LoanRequest {
    int borrowed_books;
    int days_overdue;
    bool blocked;
};

bool can_borrow(const LoanRequest& request) {
    if (request.borrowed_books < 0 || request.borrowed_books > 5) {
        return false;
    }

    if (request.days_overdue < 0 || request.days_overdue > 30) {
        return false;
    }

    return request.borrowed_books < 5 && request.days_overdue == 0 && !request.blocked;
}

std::string bool_text(bool value) {
    if (value) {
        return "true";
    }

    return "false";
}

void check_bool(const std::string& name, bool expected, bool actual, int& tests, int& failed) {
    ++tests;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << bool_text(expected) << ", actual " << bool_text(actual) << "\n";
        ++failed;
    }
}

int main() {
    int tests{0};
    int failed{0};

    check_bool("C {4, 0, false}", true, can_borrow(LoanRequest{4, 0, false}), tests, failed);
    check_bool("D {5, 0, false}", true, can_borrow(LoanRequest{5, 0, false}), tests, failed);

    std::cout << "Tests: " << tests << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

**To trzecie obowiązkowe uruchomienie: jedna czynność diagnostyczna.**

1. Przeczytaj kontrakt z punktu 2.
2. Samodzielnie ustal z kontraktu wynik oczekiwany dla D.
3. Uruchom program i sprawdź, czy funkcja rzeczywiście narusza kontrakt.
4. Rozstrzygnij, gdzie jest błąd: w funkcji czy w teście.
5. Popraw to, co jest błędne.
6. Uruchom program ponownie.
7. Wyjaśnij, dlaczego nie wolno zmienić poprawnej funkcji tylko po to, żeby dostać `PASS`.

<details>
<summary>Standardowe wyjście i kod zakończenia</summary>

<!-- output: loan_wrong_expected -->
```text
PASS C {4, 0, false}
FAIL D {5, 0, false}: expected true, actual false
Tests: 2, failed: 1
```

CLion pokazuje `Process finished with exit code 1`.

</details>

<details>
<summary>Wyjaśnienie i poprawka</summary>

- **Wynik z kontraktu:** wypożyczenie jest możliwe tylko przy `borrowed_books < 5`. Pięć książek to osiągnięty limit, więc dla D wynik oczekiwany to `false`.
- **Funkcja zwraca `false`**, czyli dokładnie to, co mówi kontrakt. Funkcja jest poprawna. **Błędny jest wynik oczekiwany w teście** (*incorrect expected result*): ktoś zapisał `true`.
- **Poprawka:** w teście D zmień `true` na `false`. Funkcji nie zmieniasz.

<!-- example: loan_wrong_expected_fixed -->
```cpp
#include <iostream>
#include <string>

struct LoanRequest {
    int borrowed_books;
    int days_overdue;
    bool blocked;
};

bool can_borrow(const LoanRequest& request) {
    if (request.borrowed_books < 0 || request.borrowed_books > 5) {
        return false;
    }

    if (request.days_overdue < 0 || request.days_overdue > 30) {
        return false;
    }

    return request.borrowed_books < 5 && request.days_overdue == 0 && !request.blocked;
}

std::string bool_text(bool value) {
    if (value) {
        return "true";
    }

    return "false";
}

void check_bool(const std::string& name, bool expected, bool actual, int& tests, int& failed) {
    ++tests;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << bool_text(expected) << ", actual " << bool_text(actual) << "\n";
        ++failed;
    }
}

int main() {
    int tests{0};
    int failed{0};

    check_bool("C {4, 0, false}", true, can_borrow(LoanRequest{4, 0, false}), tests, failed);
    check_bool("D {5, 0, false}", false, can_borrow(LoanRequest{5, 0, false}), tests, failed);

    std::cout << "Tests: " << tests << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

<!-- output: loan_wrong_expected_fixed -->
```text
PASS C {4, 0, false}
PASS D {5, 0, false}
Tests: 2, failed: 0
```

Kod zakończenia: 0. Ta sama, niezmieniona funkcja przechodzi poprawiony test.

- **Dlaczego nie zmieniać funkcji:** gdyby zmienić `< 5` na `<= 5`, test by przeszedł, ale funkcja dawałaby szóstą książkę, czyli łamałaby kontrakt. Taka „poprawka” wprowadziłaby do funkcji dokładnie usterkę z punktu 8.

</details>

**Najważniejsza zasada tej diagnostyki: `FAIL` wskazuje niezgodność, ale sam nie rozstrzyga, czy błąd jest w funkcji, czy w teście.** Rozstrzyga kontrakt. Przy każdym `FAIL` najpierw ustal z kontraktu poprawny wynik, a dopiero potem zdecyduj, co poprawić.

## 10. Misja: rezerwacja sali

Szkolna sala jest dostępna od 8 do 20. Funkcja sprawdza, czy można przyjąć rezerwację na wskazane godziny.

**Kontrakt funkcji `bool is_valid_slot(int start_hour, int end_hour)`:**

- godziny to liczby całkowite: początek i koniec rezerwacji;
- przedział jest poprawny **wtedy i tylko wtedy**, gdy jednocześnie: zaczyna się nie wcześniej niż o 8, kończy się nie później niż o 20, początek jest wcześniejszy niż koniec (`start_hour < end_hour`) i trwa najwyżej trzy godziny;
- długość przedziału to `end_hour - start_hour`;
- nie ma dat, minut ani kalendarza.

Na przykład: 8–9 to poprawny przedział, 8–12 jest za długi, a 20–20 nie ma żadnej długości.

W `cpp-workspace` utwórz katalog `room_booking`, skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program` i otwórz go w CLionie. Funkcję i program testowy napisz samodzielnie w `main.cpp`. Możesz zaadaptować swój program testowy z lekcji 13.1 albo funkcję `check_bool` z tej lekcji. `CMakeLists.txt` zostaw bez zmian.

**Kolejność pracy:**

1. **Przeanalizuj kontrakt.** Wypisz jego warunki i wszystkie granice: które wartości są tuż po jednej i po drugiej stronie każdej z nich?
2. **Zaplanuj przypadki, zanim napiszesz kod.** Przygotuj tabelę z kolumnami: przypadek, `start_hour`, `end_hour`, wynik oczekiwany, rodzaj (typowy, graniczny, niepoprawne dane) i powód z kontraktu. Zadbaj, żeby każdy warunek był co najmniej raz **jedynym** powodem odrzucenia.
3. Napisz `is_valid_slot`.
4. Napisz program testowy: sprawdzanie wyniku `bool`, nazwa każdego testu, `PASS` albo `FAIL` z wynikiem oczekiwanym i rzeczywistym, podsumowanie i kod zakończenia 1 po niepowodzeniu.
5. **To czwarte obowiązkowe uruchomienie:** uruchom program z poprawną funkcją. Wszystkie testy powinny przejść, a kod zakończenia powinien wynosić 0.
6. **Celowy błąd.** Spraw, żeby funkcja odrzucała przedział trwający dokładnie trzy godziny, a poza tym działała tak samo.
7. **To piąte obowiązkowe uruchomienie:** uruchom ten sam program testowy z błędną funkcją. Zapisz, który test wykrył usterkę i jaki był kod zakończenia. Jeśli żaden test nie dał `FAIL`, dopisz przypadek, który odróżni obie wersje, i uruchom testy ponownie. Potem przywróć poprawną funkcję i uruchom testy jeszcze raz.
8. **Uzasadnij wybór.** Dla trzech przypadków, które uważasz za najważniejsze, napisz jednym zdaniem, jaką pomyłkę w funkcji każdy z nich by wykrył.

<details>
<summary>Wyniki oczekiwane: otwórz po przygotowaniu własnej tabeli</summary>

| Przypadek | `start_hour` | `end_hour` | Wynik oczekiwany | Rodzaj i powód |
|---|---:|---:|---|---|
| A | 8 | 9 | `true` | typowy; początek dokładnie o 8 |
| B | 8 | 11 | `true` | graniczny: dokładnie trzy godziny |
| C | 8 | 12 | `false` | graniczny: cztery godziny, za długo |
| D | 7 | 10 | `false` | graniczny: początek przed 8 |
| E | 19 | 20 | `true` | graniczny: koniec dokładnie o 20 |
| F | 20 | 20 | `false` | zerowa długość |
| G | 18 | 21 | `false` | graniczny: koniec po 20 |
| H | 10 | 9 | `false` | niepoprawne dane: koniec przed początkiem |
| I | 17 | 20 | `true` | graniczny: trzy godziny i koniec o 20 |
| J | 8 | 8 | `false` | zerowa długość na początku dnia |

</details>

### Kryterium sukcesu

- Program buduje się jako C++20, a `CMakeLists.txt` jest taki jak w lekcji 0.5.
- Tabela przypadków powstała przed kodem, a wyniki oczekiwane wynikają z kontraktu.
- W zestawie są przypadki typowe, graniczne po obu stronach granic i przypadki niepoprawnych danych, a każdy warunek kontraktu jest co najmniej raz jedynym powodem odrzucenia.
- Każdy test ma nazwę i wypisuje `PASS` albo `FAIL` z wynikiem oczekiwanym i rzeczywistym, a na końcu program wypisuje podsumowanie.
- Z poprawną funkcją wszystkie testy przechodzą, a kod zakończenia wynosi 0.
- Z celowym błędem co najmniej jeden test daje `FAIL`, a kod zakończenia wynosi 1.
- Po przywróceniu poprawnej funkcji wszystkie testy znowu przechodzą.
- Umiesz wskazać przypadek, który odróżnia poprawną funkcję od wersji z błędem, i uzasadnić trzy najważniejsze przypadki.

Gdy wynik się zgadza, możesz zapisać projekt w Gicie, jak w lekcji 1.5: `main.cpp` i `CMakeLists.txt`, bez katalogu budowania.

<details>
<summary>Podpowiedź 1: wynik ze specyfikacji</summary>

Dla każdego przypadku sprawdź warunki kontraktu po kolei, na kartce: czy początek nie jest wcześniejszy niż 8? Czy koniec nie jest późniejszy niż 20? Czy początek jest przed końcem? Ile wynosi `end_hour - start_hour`? Wynik oczekiwany zapisz, zanim uruchomisz cokolwiek.

</details>

<details>
<summary>Podpowiedź 2: granice</summary>

Każda liczba w kontrakcie, 8, 20 i 3, jest granicą. Sprawdź wartość dokładnie na granicy i tuż po obu jej stronach: na przykład przedział trwający 3 i 4 godziny albo kończący się o 20 i o 21. Granicą jest też relacja `start_hour < end_hour`: co się dzieje, gdy obie godziny są równe?

</details>

<details>
<summary>Podpowiedź 3: wykrywanie usterki</summary>

Wybierz przypadek, dla którego poprawna funkcja i wersja z celowym błędem powinny zwrócić **różne** wyniki. Jeśli błąd dotyczy przedziałów trwających dokładnie trzy godziny, który z Twoich przypadków ma dokładnie taką długość, a jednocześnie spełnia wszystkie pozostałe warunki?

</details>

## 11. Gdy coś pójdzie inaczej

| Co widzisz | Co to znaczy | Co zrobić |
|---|---|---|
| Wszystkie testy przechodzą, choć funkcja ma celowy błąd | Żaden przypadek nie odróżnia obu wersji: nie ma testu dokładnie na zepsutej granicy albo przypadki naruszają kilka warunków naraz. | Dodaj przypadek, w którym zepsuty warunek jest jedynym powodem wyniku, i uruchom testy ponownie. |
| `FAIL` dla funkcji, która wydaje się poprawna | Błąd może być w wyniku oczekiwanym (punkt 9). | Ustal wynik z kontraktu jeszcze raz. Poprawiaj tę stronę, która nie zgadza się z kontraktem, a nie tę, którą łatwiej zmienić. |
| `expected 1, actual 0` zamiast `true` i `false` | Wartość `bool` trafiła do `std::cout` bezpośrednio (lekcja 3.2). | Wypisz ją przez funkcję, która zamienia `bool` na tekst, jak `bool_text`. |
| Przypadek z blokadą daje nieoczekiwany wynik | Wartości w nawiasach klamrowych są w innej kolejności niż pola rekordu. | Podawaj je w kolejności pól: liczba książek, dni zaległości, blokada. |
| Zestaw ma dużo testów, ale nie wykrywa celowego błędu | Wiele przypadków sprawdza tę samą sytuację, na przykład same typowe dane. | Oceń każdy przypadek po tym, jaką pomyłkę mógłby wykryć, a nie po liczbie testów. |

## 12. Wyjaśnij

Odpowiedz własnymi słowami, najlepiej na piśmie. Dopiero potem porównaj z przykładowymi odpowiedziami.

1. Dlaczego to, że wszystkie testy dają `PASS`, nie dowodzi poprawności funkcji?
2. Czym różni się słaby zestaw testów od mocniejszego?
3. Dlaczego same przypadki typowe nie wystarczają?
4. Dlaczego warto sprawdzać granice, i to po obu stronach?
5. Dlaczego warto sprawdzać każdy warunek osobno?
6. Dlaczego jeden przypadek, który narusza trzy warunki naraz, może nie wystarczyć?
7. Skąd pochodzą wyniki oczekiwane?
8. Czy `FAIL` zawsze oznacza błąd w sprawdzanej funkcji?
9. Jak ustalić, czy błędna jest funkcja, czy wynik oczekiwany?
10. Jak sprawdzić, czy nowy test rzeczywiście potrafi wykryć konkretną usterkę?

<details>
<summary>Przykładowe odpowiedzi</summary>

1. Bo testy sprawdzają tylko wybrane przypadki. `PASS` znaczy, że dla nich funkcja zgadza się z kontraktem. Dla przypadków, których nikt nie sprawdził, funkcja może się mylić, jak wersja bez blokady dla A, B i J.
2. Słaby zestaw przechodzi także dla wersji funkcji z błędem. Mocniejszy odróżnia więcej takich wersji od poprawnej funkcji. O sile zestawu decyduje dobór przypadków, a nie ich liczba.
3. Bo w typowym przypadku wszystkie warunki są spełnione naraz i zwykle daleko od granic. Takie dane nie pokażą pomyłki w pojedynczym warunku ani na granicy.
4. Bo na granicy najłatwiej o pomyłkę, na przykład `<=` zamiast `<`. Wartość po jednej stronie sprawdza, że granica jest we właściwym miejscu, a wartość po drugiej, że wynik naprawdę się zmienia.
5. Bo wtedy wynik zależy tylko od jednego warunku. Jeśli funkcja go pominie albo sprawdzi źle, test da `FAIL`.
6. Bo funkcja odrzuci taki przypadek, gdy sprawdza którykolwiek z trzech warunków. Test nie pokaże, że któryś z pozostałych jest pominięty albo zepsuty.
7. Z kontraktu funkcji. Ustala się je przed uruchomieniem testu i nigdy z tego, co funkcja aktualnie zwraca.
8. Nie. `FAIL` wskazuje tylko niezgodność między wynikiem rzeczywistym a oczekiwanym. Błąd może być w funkcji albo w samym teście, na przykład w źle ustalonym wyniku oczekiwanym.
9. Ustalić wynik z kontraktu jeszcze raz. Jeśli kontrakt zgadza się z funkcją, błędny jest test. Jeśli zgadza się z wynikiem oczekiwanym, błędna jest funkcja.
10. Wprowadzić celowo usterkę, której test ma dotyczyć, uruchomić test i sprawdzić, czy daje `FAIL`. Potem przywrócić poprawną funkcję i sprawdzić, że test znowu przechodzi.

</details>

## Podsumowanie

- Gdy wszystkie testy przechodzą, przygotowany zestaw nie wykrył niezgodności. Nie dowodzi to poprawności funkcji.
- Działający program testowy, poprawne wyniki oczekiwane, dobrze dobrane przypadki i poprawna funkcja to cztery różne rzeczy.
- **Przypadki typowe** są potrzebne, ale niewiele sprawdzają. **Przypadki graniczne** sprawdzają obie strony każdej granicy z kontraktu. **Przypadki niepoprawnych danych** sprawdzają wartości spoza zakresu.
- Żeby sprawdzić jeden warunek, naruszaj tylko ten warunek. Przypadek, który narusza wiele warunków naraz, nie zastąpi sprawdzenia każdego z nich osobno.
- Siłę zestawu ocenia się po tym, czy odróżnia poprawną funkcję od wersji z błędem, a nie po liczbie testów.
- Przypadek graniczny jest najcenniejszy tam, gdzie po obu stronach granicy wynik powinien być różny.
- `FAIL` wskazuje niezgodność. Czy błąd jest w funkcji, czy w teście, rozstrzyga kontrakt.

## Co dalej

Dotąd sprawdzane funkcje dostawały gotowe wartości. W następnej lekcji Modułu 13 przetestujesz funkcję, która odczytuje dane ze strumienia. Ta lekcja jest w przygotowaniu.

---

## Przykładowe rozwiązania

Zajrzyj tutaj **po własnej próbie**. To jedno z poprawnych rozwiązań. Twoje nazwy, kolejność testów i liczba przypadków mogą być inne, jeśli zestaw sprawdza każdą granicę i każdy warunek, a program testowy porównuje wynik oczekiwany z rzeczywistym, wypisuje werdykt, liczy niepowodzenia i ustala kod zakończenia.

<details>
<summary>Punkt 10: misja, rezerwacja sali</summary>

**`main.cpp`** z poprawną funkcją i testami przypadków A–J:

<!-- example: slot_tests -->
```cpp
#include <iostream>
#include <string>

bool is_valid_slot(int start_hour, int end_hour) {
    if (start_hour < 8 || end_hour > 20) {
        return false;
    }

    if (start_hour >= end_hour) {
        return false;
    }

    return end_hour - start_hour <= 3;
}

std::string bool_text(bool value) {
    if (value) {
        return "true";
    }

    return "false";
}

void check_bool(const std::string& name, bool expected, bool actual, int& tests, int& failed) {
    ++tests;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << bool_text(expected) << ", actual " << bool_text(actual) << "\n";
        ++failed;
    }
}

int main() {
    int tests{0};
    int failed{0};

    check_bool("A 8-9", true, is_valid_slot(8, 9), tests, failed);
    check_bool("B 8-11", true, is_valid_slot(8, 11), tests, failed);
    check_bool("C 8-12", false, is_valid_slot(8, 12), tests, failed);
    check_bool("D 7-10", false, is_valid_slot(7, 10), tests, failed);
    check_bool("E 19-20", true, is_valid_slot(19, 20), tests, failed);
    check_bool("F 20-20", false, is_valid_slot(20, 20), tests, failed);
    check_bool("G 18-21", false, is_valid_slot(18, 21), tests, failed);
    check_bool("H 10-9", false, is_valid_slot(10, 9), tests, failed);
    check_bool("I 17-20", true, is_valid_slot(17, 20), tests, failed);
    check_bool("J 8-8", false, is_valid_slot(8, 8), tests, failed);

    std::cout << "Tests: " << tests << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

<!-- output: slot_tests -->
```text
PASS A 8-9
PASS B 8-11
PASS C 8-12
PASS D 7-10
PASS E 19-20
PASS F 20-20
PASS G 18-21
PASS H 10-9
PASS I 17-20
PASS J 8-8
Tests: 10, failed: 0
```

Kod zakończenia: 0. Przygotowany zestaw nie wykrył niezgodności w tej wersji funkcji.

- **Funkcja:** najpierw godziny otwarcia sali, potem kolejność początku i końca, na końcu długość. `start_hour >= end_hour` odrzuca jednocześnie zerową długość (F, J) i koniec przed początkiem (H).
- **Dlaczego te przypadki:** B i C sprawdzają granicę długości (3 i 4 godziny), A i D granicę początku (8 i 7), E i G granicę końca (20 i 21), F i J zerową długość, H odwrotną kolejność, a I łączy największą dozwoloną długość z końcem dokładnie o 20.

**Celowy błąd z misji: odrzucanie dokładnie trzech godzin**, `end_hour - start_hour < 3` zamiast `<= 3`:

<!-- example: slot_tests_three_hours_bug exit=1 -->
```cpp
#include <iostream>
#include <string>

bool is_valid_slot(int start_hour, int end_hour) {
    if (start_hour < 8 || end_hour > 20) {
        return false;
    }

    if (start_hour >= end_hour) {
        return false;
    }

    return end_hour - start_hour < 3;
}

std::string bool_text(bool value) {
    if (value) {
        return "true";
    }

    return "false";
}

void check_bool(const std::string& name, bool expected, bool actual, int& tests, int& failed) {
    ++tests;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << bool_text(expected) << ", actual " << bool_text(actual) << "\n";
        ++failed;
    }
}

int main() {
    int tests{0};
    int failed{0};

    check_bool("A 8-9", true, is_valid_slot(8, 9), tests, failed);
    check_bool("B 8-11", true, is_valid_slot(8, 11), tests, failed);
    check_bool("C 8-12", false, is_valid_slot(8, 12), tests, failed);
    check_bool("D 7-10", false, is_valid_slot(7, 10), tests, failed);
    check_bool("E 19-20", true, is_valid_slot(19, 20), tests, failed);
    check_bool("F 20-20", false, is_valid_slot(20, 20), tests, failed);
    check_bool("G 18-21", false, is_valid_slot(18, 21), tests, failed);
    check_bool("H 10-9", false, is_valid_slot(10, 9), tests, failed);
    check_bool("I 17-20", true, is_valid_slot(17, 20), tests, failed);
    check_bool("J 8-8", false, is_valid_slot(8, 8), tests, failed);

    std::cout << "Tests: " << tests << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

<!-- output: slot_tests_three_hours_bug -->
```text
PASS A 8-9
FAIL B 8-11: expected true, actual false
PASS C 8-12
PASS D 7-10
PASS E 19-20
PASS F 20-20
PASS G 18-21
PASS H 10-9
FAIL I 17-20: expected true, actual false
PASS J 8-8
Tests: 10, failed: 2
```

Kod zakończenia: 1. Po przywróceniu `<= 3` program znowu daje wynik pierwszego programu i kod 0.

**Dwie inne wersje z błędem**, każda z jedną zmianą. Sprawdź, czy Twój zestaw wykryłby także je.

**Dopuszczanie zerowej długości**, `start_hour > end_hour` zamiast `>=`:

<!-- example: slot_tests_zero_length_bug exit=1 -->
```cpp
#include <iostream>
#include <string>

bool is_valid_slot(int start_hour, int end_hour) {
    if (start_hour < 8 || end_hour > 20) {
        return false;
    }

    if (start_hour > end_hour) {
        return false;
    }

    return end_hour - start_hour <= 3;
}

std::string bool_text(bool value) {
    if (value) {
        return "true";
    }

    return "false";
}

void check_bool(const std::string& name, bool expected, bool actual, int& tests, int& failed) {
    ++tests;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << bool_text(expected) << ", actual " << bool_text(actual) << "\n";
        ++failed;
    }
}

int main() {
    int tests{0};
    int failed{0};

    check_bool("A 8-9", true, is_valid_slot(8, 9), tests, failed);
    check_bool("B 8-11", true, is_valid_slot(8, 11), tests, failed);
    check_bool("C 8-12", false, is_valid_slot(8, 12), tests, failed);
    check_bool("D 7-10", false, is_valid_slot(7, 10), tests, failed);
    check_bool("E 19-20", true, is_valid_slot(19, 20), tests, failed);
    check_bool("F 20-20", false, is_valid_slot(20, 20), tests, failed);
    check_bool("G 18-21", false, is_valid_slot(18, 21), tests, failed);
    check_bool("H 10-9", false, is_valid_slot(10, 9), tests, failed);
    check_bool("I 17-20", true, is_valid_slot(17, 20), tests, failed);
    check_bool("J 8-8", false, is_valid_slot(8, 8), tests, failed);

    std::cout << "Tests: " << tests << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

<!-- output: slot_tests_zero_length_bug -->
```text
PASS A 8-9
PASS B 8-11
PASS C 8-12
PASS D 7-10
PASS E 19-20
FAIL F 20-20: expected false, actual true
PASS G 18-21
PASS H 10-9
PASS I 17-20
FAIL J 8-8: expected false, actual true
Tests: 10, failed: 2
```

Kod zakończenia: 1.

**Zła górna granica godzin**, `end_hour >= 20` zamiast `end_hour > 20`:

<!-- example: slot_tests_end_hour_bug exit=1 -->
```cpp
#include <iostream>
#include <string>

bool is_valid_slot(int start_hour, int end_hour) {
    if (start_hour < 8 || end_hour >= 20) {
        return false;
    }

    if (start_hour >= end_hour) {
        return false;
    }

    return end_hour - start_hour <= 3;
}

std::string bool_text(bool value) {
    if (value) {
        return "true";
    }

    return "false";
}

void check_bool(const std::string& name, bool expected, bool actual, int& tests, int& failed) {
    ++tests;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << bool_text(expected) << ", actual " << bool_text(actual) << "\n";
        ++failed;
    }
}

int main() {
    int tests{0};
    int failed{0};

    check_bool("A 8-9", true, is_valid_slot(8, 9), tests, failed);
    check_bool("B 8-11", true, is_valid_slot(8, 11), tests, failed);
    check_bool("C 8-12", false, is_valid_slot(8, 12), tests, failed);
    check_bool("D 7-10", false, is_valid_slot(7, 10), tests, failed);
    check_bool("E 19-20", true, is_valid_slot(19, 20), tests, failed);
    check_bool("F 20-20", false, is_valid_slot(20, 20), tests, failed);
    check_bool("G 18-21", false, is_valid_slot(18, 21), tests, failed);
    check_bool("H 10-9", false, is_valid_slot(10, 9), tests, failed);
    check_bool("I 17-20", true, is_valid_slot(17, 20), tests, failed);
    check_bool("J 8-8", false, is_valid_slot(8, 8), tests, failed);

    std::cout << "Tests: " << tests << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

<!-- output: slot_tests_end_hour_bug -->
```text
PASS A 8-9
PASS B 8-11
PASS C 8-12
PASS D 7-10
FAIL E 19-20: expected true, actual false
PASS F 20-20
PASS G 18-21
PASS H 10-9
FAIL I 17-20: expected true, actual false
PASS J 8-8
Tests: 10, failed: 2
```

Kod zakończenia: 1.

| Usterka | Przypadki, które ją ujawniają | Oczekiwany `FAIL` |
|---|---|---|
| odrzucanie dokładnie trzech godzin | B, I | `expected true, actual false` |
| dopuszczanie zerowej długości | F, J | `expected false, actual true` |
| zła górna granica godzin | E, I | `expected true, actual false` |

- Każdą usterkę wykrywa przypadek leżący **dokładnie na zepsutej granicy**: trzy godziny, równe godziny, koniec o 20.
- A, C, D i G przechodzą dla wszystkich trzech wersji, choć C, D i G też leżą przy granicach. Każda z tych usterek zmienia wynik tylko po jednej stronie swojej granicy, dlatego granicę sprawdza się z obu stron. Zestaw złożony tylko z A, C, D i G byłby słaby.
- Jeśli Twój zestaw nie wykrył którejś wersji, dopisz przypadek na tej granicy, z pozostałymi warunkami spełnionymi.

</details>

**Poprzednia lekcja:** [Lekcja 13.1: Program, który sam sprawdza wynik](lesson_01_self_checking_program.md) · **Następna lekcja:** w przygotowaniu · [Opis kursu](../../README.md)

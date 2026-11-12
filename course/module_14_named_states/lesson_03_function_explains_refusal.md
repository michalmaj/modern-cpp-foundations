# Lekcja 14.3: Funkcja mówi, dlaczego odmówiła

**Polski** · [English](lesson_03_function_explains_refusal.en.md) · [Opis kursu](../../README.md)

> **Moduł 14, lekcja 3** · około 90–110 minut, można ją podzielić na dwa podejścia (punkty 1–7, potem misja)
> **Potrzebujesz:** katalogu `cpp-workspace` i oryginalnego projektu `lesson_05_first_program`, jak dotąd. Debugger nie jest w tej lekcji potrzebny.
> **Wersja pilotażowa.** Programy z tej lekcji sprawdzamy automatycznie na Windowsie, Ubuntu i macOS, razem z ich kodem zakończenia. Programy, które nie mają się zbudować, sprawdzamy razem z miejscem ich pierwszego błędu. Żaden program nie pyta o dane: wszystkie wartości są zapisane w kodzie.

## Zanim zaczniesz

Ta lekcja zakłada, że:

- piszesz funkcję, która zmienia dane przekazane przez `&` tylko po spełnieniu warunków i zwraca `bool`, jak `issue_units` w lekcji 9.2;
- wiesz, że `false` z takiej funkcji nie mówi, który warunek nie był spełniony (lekcja 9.4);
- definiujesz typ `enum class`, porównujesz jego wartości przez `==` i zamieniasz je na tekst (lekcja 14.1);
- obsługujesz każdą wartość typu wyliczeniowego instrukcją `switch` i kończysz etykietę przez `return` albo `break` (lekcja 14.2);
- piszesz jednoplikowe programy testowe z funkcjami `check_int`, `check_bool` i `check_text`, które kończą się kodem 1, gdy któreś sprawdzenie się nie uda, i dobierasz przypadki, które odróżniają poprawną funkcję od wersji z błędem (lekcje 13.1–13.3).

## Sytuacja

Wracamy do magazynu z lekcji 9.2. Funkcja `issue_units` wydaje towar tylko wtedy, gdy wolno, i zwraca `true` albo `false`. Gdy wydanie się nie udaje, magazyn dostaje `false` i nie wie, co poprawić: ilość w żądaniu czy stan magazynu. W lekcji 9.4 padło zdanie: gdyby program musiał podać przyczynę odmowy, potrzebny byłby wynik, który przekazuje więcej informacji. W tej lekcji zaprojektujesz taki wynik.

Odpowiesz na pytanie: **jak funkcja ma powiedzieć, dlaczego odmówiła, i jak sprawdzić osobno to, co powiedziała, i to, co zrobiła z danymi?**

Po tej lekcji będziesz:

- rozpoznawać, kiedy `bool` nie wystarcza, bo odmowa ma kilka różnych powodów;
- projektować typ `enum class`, którego wartości nazywają wszystkie możliwe zakończenia operacji, i zwracać go z funkcji;
- obsługiwać w kodzie wywołującym każdy wynik osobno, instrukcją `switch`;
- oddzielać wynik operacji od jej skutku, czyli od zmiany danych przekazanych przez `&`, i pilnować, żeby odmowa niczego nie zmieniała;
- sprawdzać w testach osobno nazwany wynik i stan danych po wywołaniu;
- ustalać i testować pierwszeństwo odmowy, gdy kilka powodów zachodzi jednocześnie.

## 1. Co mówi `false`

Tak wyglądała funkcja z lekcji 9.2:

<!-- fragment -->
```cpp
bool issue_units(Product& product, int amount) {
    if (amount <= 0 || amount > product.stock) {
        return false;
    }

    product.stock -= amount;
    return true;
}
```

Jeden warunek odmowy łączy przez `||` dwa różne powody. Dla produktu `tea` z 7 sztukami:

| Wywołanie | Powód odmowy | Wynik |
|---|---|---|
| `issue_units(tea, 0)` | niepoprawna ilość | `false` |
| `issue_units(tea, 8)` | za mało towaru | `false` |

Wywołujący dostaje w obu przypadkach to samo. Żeby podać powód, musiałby sam jeszcze raz sprawdzić ilość:

<!-- fragment -->
```cpp
const bool accepted{issue_units(tea, amount)};

if (!accepted) {
    if (amount <= 0) {
        std::cout << "Invalid amount\n";
    } else {
        std::cout << "Not enough stock\n";
    }
}
```

To działa, ale reguła stoi teraz w dwóch miejscach: w funkcji i w `main`. Gdy ktoś zmieni ją w funkcji, na przykład zacznie odrzucać żądania mniejsze niż 2 sztuki, a zapomni o `main`, raport dla żądania 1 poda zły powód: `Not enough stock`, choć towaru jest dość. Powód odmowy powinna znać i zgłaszać sama funkcja, bo to ona sprawdza warunki.

## 2. Nazwany wynik i kontrakt

Wydanie może się zakończyć na trzy sposoby. Każdy dostaje własną nazwę, w typie wyliczeniowym z lekcji 14.1:

<!-- fragment -->
```cpp
enum class IssueResult {
    issued,
    invalid_amount,
    insufficient_stock
};
```

- `IssueResult::issued`: towar wydany;
- `IssueResult::invalid_amount`: niepoprawne żądanie, czyli ilość 0 albo ujemna;
- `IssueResult::insufficient_stock`: za mało towaru na stanie.

Każdy wynik to **nazwany wynik**: wartość tego samego typu `IssueResult`. To nie tekst, nie liczba i nie osobny mechanizm zgłaszania błędów. Wynik odmowy jest równie zwykłą wartością jak wynik sukcesu.

Nowa wersja funkcji zwraca ten typ:

<!-- fragment -->
```cpp
IssueResult issue_units(int requested, int& stock);
```

**Co się zmienia w porównaniu z lekcją 9.2:**

| | Lekcja 9.2 | Ta lekcja |
|---|---|---|
| Typ wyniku | `bool` | `IssueResult` |
| Zmieniane dane | cały rekord: `Product& product` | sam stan magazynu: `int& stock` |
| Kolejność parametrów | najpierw rekord, potem ilość | najpierw żądana ilość, potem stan |
| Warunki odmowy | jeden warunek z `||` | dwa osobne warunki, bo każdy powód ma własny wynik |

**Co zostaje bez zmian:** ilość 0 i ujemna jest odrzucana, wydanie całego stanu jest dozwolone, przy pustym stanie każde dodatnie żądanie jest odrzucane, a odmowa niczego nie zmienia. Funkcja nadal niczego nie wypisuje. Do wydania nie potrzebuje nazwy ani ceny produktu, dlatego dostaje tylko liczbę sztuk na stanie, zapisaną w zmiennej `int`.

**Wynik i skutek to dwie różne rzeczy**, jak w lekcji 9.2:

| Co | Jak trafia do wywołującego | Kiedy |
|---|---|---|
| **Wynik:** jak zakończyła się operacja | wartość `IssueResult` zwrócona przez `return` | zawsze |
| **Skutek:** mniejszy stan magazynu | zmiana zmiennej przekazanej przez `int& stock` | tylko przy `issued` |

Nazwany wynik nie zastępuje parametru `int& stock`. Funkcja nie zwraca nowego stanu zamiast wyniku: zwraca informację, jak zakończyła się operacja, a stan zmienia przez referencję, i to tylko przy sukcesie.

### Kontrakt `issue_units`

**Założenie:** na wejściu `stock` jest równy 0 albo większy. Funkcja tego nie sprawdza: to warunek, o który dba wywołujący.

- Gdy `requested <= 0`: wynik `IssueResult::invalid_amount`, `stock` bez zmian.
- Gdy `requested > stock`: wynik `IssueResult::insufficient_stock`, `stock` bez zmian.
- W pozostałych przypadkach, czyli gdy `requested > 0` i `requested <= stock`: `stock` zmniejsza się o `requested`, a wynik to `IssueResult::issued`.

**Po odmowie `stock` ma dokładnie tę samą wartość co przed wywołaniem.** Funkcja nie może najpierw zmniejszyć stanu, a potem zgłosić odmowy.

Przypadki z kontraktu, z wynikiem zapisanym bez `IssueResult::`:

| Przypadek | `requested` | `stock` przed | Wynik | `stock` po |
|---|---:|---:|---|---:|
| A | 3 | 7 | `issued` | 4 |
| B | 7 | 7 | `issued` | 0 |
| C | 0 | 7 | `invalid_amount` | 7 |
| D | -2 | 7 | `invalid_amount` | 7 |
| E | 8 | 7 | `insufficient_stock` | 7 |
| F | 1 | 0 | `insufficient_stock` | 0 |
| G | 1 | 7 | `issued` | 6 |

Każdy wiersz wynika z trzech reguł powyżej, a nie z kodu funkcji. B wydaje cały stan, a F pokazuje pusty magazyn.

## 3. Funkcja i program, który obsługuje każdy wynik

<!-- example: issue_requests -->
```cpp
#include <iostream>
#include <vector>

enum class IssueResult {
    issued,
    invalid_amount,
    insufficient_stock
};

IssueResult issue_units(int requested, int& stock) {
    if (requested <= 0) {
        return IssueResult::invalid_amount;
    }

    if (requested > stock) {
        return IssueResult::insufficient_stock;
    }

    stock -= requested;
    return IssueResult::issued;
}

int main() {
    int stock{7};
    const std::vector<int> requests{3, 0, 8, 4};

    std::cout << "Stock: " << stock << "\n";

    for (const int requested : requests) {
        const IssueResult result{issue_units(requested, stock)};

        std::cout << "Request " << requested << ": ";

        switch (result) {
            case IssueResult::issued:
                std::cout << "Units issued, " << stock << " left\n";
                break;
            case IssueResult::invalid_amount:
                std::cout << "Invalid amount, ask for at least 1\n";
                break;
            case IssueResult::insufficient_stock:
                std::cout << "Not enough stock, only " << stock << " available\n";
                break;
        }
    }

    std::cout << "Final stock: " << stock << "\n";
}
```

**To pierwsze obowiązkowe uruchomienie.** W `cpp-workspace` utwórz katalog `lesson_14_3`, skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program` i zastąp zawartość `main.cpp` programem powyżej. **Przewidź** wszystkie sześć linijek, a potem uruchom program.

<details>
<summary>Standardowe wyjście</summary>

<!-- output: issue_requests -->
```text
Stock: 7
Request 3: Units issued, 4 left
Request 0: Invalid amount, ask for at least 1
Request 8: Not enough stock, only 4 available
Request 4: Units issued, 0 left
Final stock: 0
```

</details>

- **Najpierw sprawdzenia, potem zmiana.** Każda klauzula ochronna kończy funkcję własnym wynikiem, zanim wykona się `stock -= requested;`. Do zmiany dochodzi tylko żądanie, które przeszło oba sprawdzenia, jak w lekcji 9.2.
- **Każdy powód ma własny `return`.** Warunek z `||` z lekcji 9.2 jest rozdzielony na dwa `if`, bo każdy powód odmowy ma inną wartość wyniku. Każde sprawdzenie występuje w funkcji raz.
- **`const IssueResult result{issue_units(requested, stock)};`** wywołuje funkcję raz i zapamiętuje wynik. `switch` sprawdza potem zapamiętaną wartość. Drugie wywołanie byłoby kolejną próbą wydania (lekcja 9.2).
- **`switch` w `main` robi dla każdego wyniku co innego:** po wydaniu podaje, ile zostało, przy niepoprawnym żądaniu mówi, jaka ilość jest dozwolona, a przy braku towaru podaje, ile jest dostępne. Etykiety `case` nazywają wszystkie trzy wyniki, jak w lekcji 14.2.
- **`break` kończy tu tylko `switch`.** Pętla działa dalej i bierze następne żądanie.
- **Odmowy nie zmieniają stanu:** po żądaniach 0 i 8 nadal są 4 sztuki, więc ostatnie żądanie, 4, wydaje wszystko, co zostało.

**Czy kolejność dwóch sprawdzeń ma tu znaczenie?** Przy tym kontrakcie nie. Gdy `requested <= 0`, warunek `requested > stock` jest fałszywy, bo `stock` wynosi co najmniej 0. Oba powody odmowy nigdy nie zachodzą jednocześnie, więc zamiana miejscami tych dwóch `if` nie zmieni żadnego wyniku. Wynika to z założenia, że `stock` nie jest ujemny. Nie wolno za to przenieść zmiany stanu przed sprawdzenia: odmowa zostawiłaby wtedy stan zmniejszony. W misji dwa powody odmowy mogą zajść jednocześnie i tam kolejność sprawdzeń zmienia wynik.

## 4. Wynik to wartość typu `IssueResult`

Dwa nawyki z wcześniejszych lekcji tu nie działają. Oba poniższe programy się nie zbudują. Nie musisz ich budować: sprawdzamy je automatycznie, a ich wynik znasz z opisu.

**Wynik w warunku `if`, jak `bool` w lekcji 9.2:**

<!-- broken: issue_if_bool at=25:9 errors=1 error=^value of type 'IssueResult' is not contextually convertible to 'bool' -->
```cpp
#include <iostream>

enum class IssueResult {
    issued,
    invalid_amount,
    insufficient_stock
};

IssueResult issue_units(int requested, int& stock) {
    if (requested <= 0) {
        return IssueResult::invalid_amount;
    }

    if (requested > stock) {
        return IssueResult::insufficient_stock;
    }

    stock -= requested;
    return IssueResult::issued;
}

int main() {
    int stock{7};

    if (issue_units(3, stock)) {
        std::cout << "Units issued\n";
    }
}
```

Kompilator zgłasza błąd w linijce 25: `value of type 'IssueResult' is not contextually convertible to 'bool'`. Wartości typu `enum class` nie da się użyć tam, gdzie potrzebny jest `bool`. To dobrze: nie byłoby wiadomo, czy „prawda” oznacza `issued`, czy którąś z odmów.

**Porównanie z tekstem:**

<!-- broken: issue_compare_text at=26:16 errors=1 error=^invalid operands to binary expression -->
```cpp
#include <iostream>

enum class IssueResult {
    issued,
    invalid_amount,
    insufficient_stock
};

IssueResult issue_units(int requested, int& stock) {
    if (requested <= 0) {
        return IssueResult::invalid_amount;
    }

    if (requested > stock) {
        return IssueResult::insufficient_stock;
    }

    stock -= requested;
    return IssueResult::issued;
}

int main() {
    int stock{7};
    const IssueResult result{issue_units(3, stock)};

    if (result == "issued") {
        std::cout << "Units issued\n";
    }
}
```

Błąd w linijce 26 zaczyna się od `invalid operands to binary expression`, jak przy wypisywaniu stanu w lekcji 14.1. Tym razem nie istnieje `==` dla pary: wartość typu `IssueResult` i tekst w cudzysłowie. Wynik to nie tekst `"issued"`, tylko wartość `IssueResult::issued`. Przed tym błędem Clang może wypisać jeszcze ostrzeżenie o porównaniu z tekstem w cudzysłowie. O tym, że program się nie buduje, decyduje błąd.

W obu przypadkach rozwiązanie jest to samo: zapisz wynik w zmiennej i porównaj go z wartością tego samego typu albo obsłuż wszystkie wartości instrukcją `switch`, jak w punkcie 3.

<!-- fragment -->
```cpp
const IssueResult result{issue_units(3, stock)};

if (result == IssueResult::issued) {
    std::cout << "Units issued\n";
}
```

## 5. Wynik jako tekst

W testach linijka `FAIL` musi pokazać wynik, a `std::cout` nie wypisze wartości `IssueResult` wprost (lekcja 14.1). Funkcja `issue_result_text` zamienia wynik na tekst tak samo jak `status_text` w lekcji 14.2: `switch`, w którym każda etykieta od razu zwraca tekst, i zachowanie zapasowe za `switch`.

<!-- fragment -->
```cpp
std::string issue_result_text(IssueResult result) {
    switch (result) {
        case IssueResult::issued:
            return "issued";
        case IssueResult::invalid_amount:
            return "invalid_amount";
        case IssueResult::insufficient_stock:
            return "insufficient_stock";
    }

    return "unknown";
}
```

| Wynik | Tekst |
|---|---|
| `IssueResult::issued` | `"issued"` |
| `IssueResult::invalid_amount` | `"invalid_amount"` |
| `IssueResult::insufficient_stock` | `"insufficient_stock"` |

Tekst służy tylko do wypisania. Wyniki program porównuje jako wartości `IssueResult`.

## 6. Program testowy: wynik i stan osobno

Każde wywołanie `issue_units` ma dwie własności do sprawdzenia: **nazwany wynik** i **stan po wywołaniu**. Sprawdzasz je osobno, bo funkcja może pomylić jedno, a drugie zrobić dobrze.

Potrzebne są dwie funkcje sprawdzające. `check_int` z lekcji 13.3 porównuje stan. `check_issue_result` porównuje dwie wartości `IssueResult` przez `==`, a do linijki `FAIL` zamienia je na tekst przez `issue_result_text`. Ma taką samą budowę jak `check_status` z lekcji 14.1:

<!-- fragment -->
```cpp
void check_issue_result(const std::string& name, IssueResult expected, IssueResult actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << issue_result_text(expected) << ", actual " << issue_result_text(actual) << "\n";
        ++failed;
    }
}
```

Trzy zasady tego programu:

- **Test porównuje z dokładnie tym wynikiem, który podaje kontrakt.** Sprawdzenie „wynik jest inny niż `issued`” przejdzie dla obu odmów, także wtedy, gdy funkcja poda zły powód. `IssueResult::invalid_amount` i `IssueResult::insufficient_stock` to różne wyniki, więc test sprawdza, który z nich wrócił.
- **`issue_result_text` też ma własne testy.** Porównanie w `check_issue_result` dotyczy wartości, więc PASS i FAIL są poprawne nawet wtedy, gdy tekst jest pomylony. Pomylony tekst zepsułby jednak treść linijki `FAIL`, na przykład `expected issued, actual issued`. Dlatego trzy pierwsze sprawdzenia porównują teksty z tabelą z punktu 5, przez `check_text`. Wyniki oczekiwane to napisy z tabeli, a nie wywołania tej samej funkcji.
- **Każdy przypadek ma własną zmienną stanu.** `stock_a` zaczyna od 7, `stock_f` od 0, każda tak jak w tabeli z punktu 2. Gdyby przypadki korzystały z jednej zmiennej, B zaczynałby od stanu, który zostawił A.

**Liczba sprawdzeń:** 7 przypadków po 2 sprawdzenia daje 14, do tego 3 sprawdzenia tekstu, razem 17. Przypadek to jedno wywołanie z danymi z tabeli. Sprawdzenie to jedno porównanie z jedną linijką `PASS` albo `FAIL`.

**To drugie obowiązkowe uruchomienie.** Zastąp zawartość `main.cpp` programem poniżej. Funkcje `check_int` i `check_text` możesz skopiować z lekcji 13.3, a pozostałe z punktów 3, 5 i 6. **Przewidź** ostatnią linijkę wyniku, zanim uruchomisz program.

<details>
<summary>Pełny program testowy</summary>

<!-- example: issue_tests -->
```cpp
#include <iostream>
#include <string>

enum class IssueResult {
    issued,
    invalid_amount,
    insufficient_stock
};

IssueResult issue_units(int requested, int& stock) {
    if (requested <= 0) {
        return IssueResult::invalid_amount;
    }

    if (requested > stock) {
        return IssueResult::insufficient_stock;
    }

    stock -= requested;
    return IssueResult::issued;
}

std::string issue_result_text(IssueResult result) {
    switch (result) {
        case IssueResult::issued:
            return "issued";
        case IssueResult::invalid_amount:
            return "invalid_amount";
        case IssueResult::insufficient_stock:
            return "insufficient_stock";
    }

    return "unknown";
}

void check_issue_result(const std::string& name, IssueResult expected, IssueResult actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << issue_result_text(expected) << ", actual " << issue_result_text(actual) << "\n";
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

    check_text("issue_result_text(issued)", "issued", issue_result_text(IssueResult::issued), checks, failed);
    check_text("issue_result_text(invalid_amount)", "invalid_amount", issue_result_text(IssueResult::invalid_amount), checks, failed);
    check_text("issue_result_text(insufficient_stock)", "insufficient_stock", issue_result_text(IssueResult::insufficient_stock), checks, failed);

    int stock_a{7};
    const IssueResult result_a{issue_units(3, stock_a)};
    check_issue_result("A result", IssueResult::issued, result_a, checks, failed);
    check_int("A stock", 4, stock_a, checks, failed);

    int stock_b{7};
    const IssueResult result_b{issue_units(7, stock_b)};
    check_issue_result("B result", IssueResult::issued, result_b, checks, failed);
    check_int("B stock", 0, stock_b, checks, failed);

    int stock_c{7};
    const IssueResult result_c{issue_units(0, stock_c)};
    check_issue_result("C result", IssueResult::invalid_amount, result_c, checks, failed);
    check_int("C stock", 7, stock_c, checks, failed);

    int stock_d{7};
    const IssueResult result_d{issue_units(-2, stock_d)};
    check_issue_result("D result", IssueResult::invalid_amount, result_d, checks, failed);
    check_int("D stock", 7, stock_d, checks, failed);

    int stock_e{7};
    const IssueResult result_e{issue_units(8, stock_e)};
    check_issue_result("E result", IssueResult::insufficient_stock, result_e, checks, failed);
    check_int("E stock", 7, stock_e, checks, failed);

    int stock_f{0};
    const IssueResult result_f{issue_units(1, stock_f)};
    check_issue_result("F result", IssueResult::insufficient_stock, result_f, checks, failed);
    check_int("F stock", 0, stock_f, checks, failed);

    int stock_g{7};
    const IssueResult result_g{issue_units(1, stock_g)};
    check_issue_result("G result", IssueResult::issued, result_g, checks, failed);
    check_int("G stock", 6, stock_g, checks, failed);

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

<!-- output: issue_tests -->
```text
PASS issue_result_text(issued)
PASS issue_result_text(invalid_amount)
PASS issue_result_text(insufficient_stock)
PASS A result
PASS A stock
PASS B result
PASS B stock
PASS C result
PASS C stock
PASS D result
PASS D stock
PASS E result
PASS E stock
PASS F result
PASS F stock
PASS G result
PASS G stock
Checks: 17, failed: 0
```

Kod zakończenia: 0.

</details>

## 7. Diagnostyka: zły powód odmowy

Ktoś pisze drugą klauzulę ochronną przez skopiowanie pierwszej i zapomina zmienić wynik:

<!-- fragment -->
```cpp
IssueResult issue_units(int requested, int& stock) {
    if (requested <= 0) {
        return IssueResult::invalid_amount;
    }

    if (requested > stock) {
        return IssueResult::invalid_amount;
    }

    stock -= requested;
    return IssueResult::issued;
}
```

Funkcja nadal odmawia dokładnie wtedy, kiedy trzeba, a przy odmowie nadal nie zmienia stanu. Myli się tylko w powodzie.

**To trzecie obowiązkowe uruchomienie.** Wykonaj kroki po kolei:

1. **Przewidź** na podstawie tabeli z punktu 2, zanim cokolwiek zmienisz: których przypadków dotyczy druga klauzula? Które ich sprawdzenia się nie udadzą, a które przejdą? Jak będzie brzmiała ostatnia linijka?
2. W programie testowym z punktu 6 zmień w drugiej klauzuli `return IssueResult::insufficient_stock;` na `return IssueResult::invalid_amount;`. Nic więcej nie zmieniaj, ani testów, ani wyników oczekiwanych.
3. Uruchom testy. Zapisz linijki `FAIL`, podsumowanie i kod zakończenia.
4. Przywróć `return IssueResult::insufficient_stock;` i uruchom te same testy jeszcze raz.

<details>
<summary>Co się dzieje i jak to naprawić: otwórz po wykonaniu kroków 1–4</summary>

**Mapa skutków:**

| Przypadek | Dane | Wynik oczekiwany | Wynik rzeczywisty | Sprawdzenie wyniku | Sprawdzenie stanu |
|---|---|---|---|---|---|
| E | 8 sztuk przy stanie 7 | `insufficient_stock` | `invalid_amount` | `FAIL` | `PASS` |
| F | 1 sztuka przy stanie 0 | `insufficient_stock` | `invalid_amount` | `FAIL` | `PASS` |
| A–D, G | jak w tabeli | jak w tabeli | bez zmian | `PASS` | `PASS` |
| teksty | trzy wartości | jak w tabeli z punktu 5 | bez zmian | `PASS` | — |

- **Zmieniona jest jedna linijka.** Do drugiej klauzuli dochodzą tylko dodatnie żądania i odrzuca ona tylko te większe od stanu, więc błąd dotyczy dokładnie przypadków E i F.
- **Stan jest poprawny,** bo klauzula nadal kończy funkcję przed zmianą stanu. Dlatego sprawdzenia stanu przechodzą. Nie każdy błąd psuje jednocześnie wynik i dane.
- **Przy `bool` takiej pomyłki nie dałoby się zauważyć w wyniku:** obie odmowy dawały to samo `false`. Nazwany wynik mówi, **co** się nie udało, a test sprawdza, czy mówi prawdę.

Program testowy z tą zmianą, bez innych zmian:

<!-- example: issue_tests_wrong_reason exit=1 -->
```cpp
#include <iostream>
#include <string>

enum class IssueResult {
    issued,
    invalid_amount,
    insufficient_stock
};

IssueResult issue_units(int requested, int& stock) {
    if (requested <= 0) {
        return IssueResult::invalid_amount;
    }

    if (requested > stock) {
        return IssueResult::invalid_amount;
    }

    stock -= requested;
    return IssueResult::issued;
}

std::string issue_result_text(IssueResult result) {
    switch (result) {
        case IssueResult::issued:
            return "issued";
        case IssueResult::invalid_amount:
            return "invalid_amount";
        case IssueResult::insufficient_stock:
            return "insufficient_stock";
    }

    return "unknown";
}

void check_issue_result(const std::string& name, IssueResult expected, IssueResult actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << issue_result_text(expected) << ", actual " << issue_result_text(actual) << "\n";
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

    check_text("issue_result_text(issued)", "issued", issue_result_text(IssueResult::issued), checks, failed);
    check_text("issue_result_text(invalid_amount)", "invalid_amount", issue_result_text(IssueResult::invalid_amount), checks, failed);
    check_text("issue_result_text(insufficient_stock)", "insufficient_stock", issue_result_text(IssueResult::insufficient_stock), checks, failed);

    int stock_a{7};
    const IssueResult result_a{issue_units(3, stock_a)};
    check_issue_result("A result", IssueResult::issued, result_a, checks, failed);
    check_int("A stock", 4, stock_a, checks, failed);

    int stock_b{7};
    const IssueResult result_b{issue_units(7, stock_b)};
    check_issue_result("B result", IssueResult::issued, result_b, checks, failed);
    check_int("B stock", 0, stock_b, checks, failed);

    int stock_c{7};
    const IssueResult result_c{issue_units(0, stock_c)};
    check_issue_result("C result", IssueResult::invalid_amount, result_c, checks, failed);
    check_int("C stock", 7, stock_c, checks, failed);

    int stock_d{7};
    const IssueResult result_d{issue_units(-2, stock_d)};
    check_issue_result("D result", IssueResult::invalid_amount, result_d, checks, failed);
    check_int("D stock", 7, stock_d, checks, failed);

    int stock_e{7};
    const IssueResult result_e{issue_units(8, stock_e)};
    check_issue_result("E result", IssueResult::insufficient_stock, result_e, checks, failed);
    check_int("E stock", 7, stock_e, checks, failed);

    int stock_f{0};
    const IssueResult result_f{issue_units(1, stock_f)};
    check_issue_result("F result", IssueResult::insufficient_stock, result_f, checks, failed);
    check_int("F stock", 0, stock_f, checks, failed);

    int stock_g{7};
    const IssueResult result_g{issue_units(1, stock_g)};
    check_issue_result("G result", IssueResult::issued, result_g, checks, failed);
    check_int("G stock", 6, stock_g, checks, failed);

    std::cout << "Checks: " << checks << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

<!-- output: issue_tests_wrong_reason -->
```text
PASS issue_result_text(issued)
PASS issue_result_text(invalid_amount)
PASS issue_result_text(insufficient_stock)
PASS A result
PASS A stock
PASS B result
PASS B stock
PASS C result
PASS C stock
PASS D result
PASS D stock
FAIL E result: expected insufficient_stock, actual invalid_amount
PASS E stock
FAIL F result: expected insufficient_stock, actual invalid_amount
PASS F stock
PASS G result
PASS G stock
Checks: 17, failed: 2
```

Kod zakończenia: 1. Wynika z dwóch rzeczywistych linijek `FAIL`: `main` zwraca 1, bo `failed` jest większe od 0.

**Poprawka:** przywróć `return IssueResult::insufficient_stock;`. Program jest znów taki jak w punkcie 6. Te same testy, z tymi samymi wynikami oczekiwanymi, wypisują 17 razy `PASS` i `Checks: 17, failed: 0`, a kod zakończenia wynosi 0. Wyników oczekiwanych nie zmieniasz: to funkcja ma spełnić kontrakt, a nie testy mają się dopasować do funkcji.

</details>

### Odwrotnie: dobry wynik, zły stan

Ten wariant tylko przeczytaj i przewidź jego skutek. Uruchomienie go jest nieobowiązkowe. Ktoś uznaje, że skoro towaru i tak brakuje, magazyn wyda to, co ma, i dopisuje w drugiej klauzuli jedną linijkę:

<!-- fragment -->
```cpp
if (requested > stock) {
    stock = 0;
    return IssueResult::insufficient_stock;
}
```

**Przewidź:** które sprawdzenia z punktu 6 się nie udadzą? Czy przypadek F to zauważy?

<details>
<summary>Odpowiedź i program, który ją sprawdza</summary>

- **E:** wynik jest poprawny, `insufficient_stock`, więc sprawdzenie wyniku przechodzi. Stan spada jednak z 7 do 0, więc sprawdzenie stanu daje `FAIL`.
- **F:** stan już wynosi 0, więc `stock = 0;` niczego nie zmienia i oba sprawdzenia przechodzą. Tę usterkę wykrywa tylko przypadek, w którym przed odmową coś jest na stanie.
- **Wniosek:** funkcja zgłasza odmowę, a mimo to zmienia dane, czyli łamie kontrakt. Poprawny nazwany wynik nie gwarantuje poprawnego stanu. Gdyby test sprawdzał tylko wynik, przeszedłby w całości.

<!-- example: issue_tests_changed_stock exit=1 -->
```cpp
#include <iostream>
#include <string>

enum class IssueResult {
    issued,
    invalid_amount,
    insufficient_stock
};

IssueResult issue_units(int requested, int& stock) {
    if (requested <= 0) {
        return IssueResult::invalid_amount;
    }

    if (requested > stock) {
        stock = 0;
        return IssueResult::insufficient_stock;
    }

    stock -= requested;
    return IssueResult::issued;
}

std::string issue_result_text(IssueResult result) {
    switch (result) {
        case IssueResult::issued:
            return "issued";
        case IssueResult::invalid_amount:
            return "invalid_amount";
        case IssueResult::insufficient_stock:
            return "insufficient_stock";
    }

    return "unknown";
}

void check_issue_result(const std::string& name, IssueResult expected, IssueResult actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << issue_result_text(expected) << ", actual " << issue_result_text(actual) << "\n";
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

    check_text("issue_result_text(issued)", "issued", issue_result_text(IssueResult::issued), checks, failed);
    check_text("issue_result_text(invalid_amount)", "invalid_amount", issue_result_text(IssueResult::invalid_amount), checks, failed);
    check_text("issue_result_text(insufficient_stock)", "insufficient_stock", issue_result_text(IssueResult::insufficient_stock), checks, failed);

    int stock_a{7};
    const IssueResult result_a{issue_units(3, stock_a)};
    check_issue_result("A result", IssueResult::issued, result_a, checks, failed);
    check_int("A stock", 4, stock_a, checks, failed);

    int stock_b{7};
    const IssueResult result_b{issue_units(7, stock_b)};
    check_issue_result("B result", IssueResult::issued, result_b, checks, failed);
    check_int("B stock", 0, stock_b, checks, failed);

    int stock_c{7};
    const IssueResult result_c{issue_units(0, stock_c)};
    check_issue_result("C result", IssueResult::invalid_amount, result_c, checks, failed);
    check_int("C stock", 7, stock_c, checks, failed);

    int stock_d{7};
    const IssueResult result_d{issue_units(-2, stock_d)};
    check_issue_result("D result", IssueResult::invalid_amount, result_d, checks, failed);
    check_int("D stock", 7, stock_d, checks, failed);

    int stock_e{7};
    const IssueResult result_e{issue_units(8, stock_e)};
    check_issue_result("E result", IssueResult::insufficient_stock, result_e, checks, failed);
    check_int("E stock", 7, stock_e, checks, failed);

    int stock_f{0};
    const IssueResult result_f{issue_units(1, stock_f)};
    check_issue_result("F result", IssueResult::insufficient_stock, result_f, checks, failed);
    check_int("F stock", 0, stock_f, checks, failed);

    int stock_g{7};
    const IssueResult result_g{issue_units(1, stock_g)};
    check_issue_result("G result", IssueResult::issued, result_g, checks, failed);
    check_int("G stock", 6, stock_g, checks, failed);

    std::cout << "Checks: " << checks << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

<!-- output: issue_tests_changed_stock -->
```text
PASS issue_result_text(issued)
PASS issue_result_text(invalid_amount)
PASS issue_result_text(insufficient_stock)
PASS A result
PASS A stock
PASS B result
PASS B stock
PASS C result
PASS C stock
PASS D result
PASS D stock
PASS E result
FAIL E stock: expected 7, actual 0
PASS F result
PASS F stock
PASS G result
PASS G stock
Checks: 17, failed: 1
```

Kod zakończenia: 1.

</details>

## 8. Misja: doładowanie karty

Karta na przejazdy ma saldo w umownych punktach, a nie w pieniądzach, i może być aktywna albo zablokowana. Automat doładowuje kartę, ale nie zawsze: karta musi być aktywna, kwota musi być dozwolona, a saldo nie może przekroczyć limitu. Gdy automat odmawia, pokazuje powód. Twoim zadaniem jest funkcja doładowania, która zwraca nazwany wynik, i program testowy, który sprawdza ten wynik oraz kartę po wywołaniu.

To inny problem niż wydawanie towaru. Zmieniane dane to rekord z dwoma polami, powody odmowy są trzy, a kilka z nich może zajść jednocześnie.

**Typy i sygnatura:**

<!-- fragment -->
```cpp
enum class TopUpResult {
    added,
    inactive_card,
    invalid_amount,
    limit_exceeded
};

struct Card {
    int balance;
    bool active;
};

TopUpResult top_up(Card& card, int amount);
```

**Kontrakt `top_up`:**

- **Założenie:** na wejściu `card.balance` ma wartość od 0 do 100. Funkcja tego nie sprawdza.
- Poprawna kwota doładowania to od 1 do 50.
- Saldo po doładowaniu nie może przekroczyć 100. Saldo równe dokładnie 100 jest dozwolone.
- Gdy karta jest nieaktywna, czyli `card.active` ma wartość `false`: wynik `TopUpResult::inactive_card`.
- Gdy karta jest aktywna, ale kwota jest mniejsza od 1 albo większa od 50: wynik `TopUpResult::invalid_amount`.
- Gdy karta jest aktywna i kwota poprawna, ale saldo po doładowaniu byłoby większe niż 100: wynik `TopUpResult::limit_exceeded`.
- W pozostałych przypadkach saldo rośnie o `amount`, a wynik to `TopUpResult::added`.
- **Żadna odmowa nie zmienia karty:** ani salda, ani pola `active`. Pole `active` nie zmienia się także przy sukcesie.

**Pierwszeństwo odmowy.** Gdy kilka powodów odmowy zachodzi jednocześnie, wynik to pierwszy z nich na tej liście:

1. `inactive_card`;
2. `invalid_amount`;
3. `limit_exceeded`.

Dla nieaktywnej karty i kwoty 0 wynik to więc `inactive_card`, a nie `invalid_amount`. To decyzja projektowa naszego automatu, a nie reguła wszystkich systemów płatności: inny program mógłby ustalić inną kolejność. Ważne, żeby kontrakt ją określał, a funkcja i testy jej przestrzegały. Sprawdzanie danych, zanim operacja coś zmieni, to **walidacja**, a w tej misji kolejność walidacji jest częścią kontraktu.

**Format tabeli przypadków**, z jednym przypadkiem jako przykładem:

| Przypadek | Saldo przed | Aktywna | Kwota | Wynik | Saldo po | Aktywna po |
|---|---:|---|---:|---|---:|---|
| A | 40 | `true` | 20 | `added` | 60 | `true` |

**Zasady:**

- `top_up` dostaje kartę przez `&`, a kwotę przez wartość. Sprawdza wszystkie warunki, zanim zmieni kartę, i niczego nie wypisuje.
- Każde sprawdzenie występuje w funkcji raz.
- Program testowy porównuje wynik jako wartość `TopUpResult`, a nie jako tekst. Tekst wyniku służy tylko do linijek `FAIL`. Daje go funkcja `std::string top_up_result_text(TopUpResult result)`, zapisana przez `switch` z etykietą `case` dla każdej z czterech wartości i z zachowaniem zapasowym `"unknown"`. Sprawdź ją dla każdej wartości, jak `issue_result_text` w punkcie 6. Teksty to nazwy wartości: `"added"`, `"inactive_card"`, `"invalid_amount"`, `"limit_exceeded"`.
- Każdy przypadek ma własny obiekt `Card` ze stanem początkowym z Twojej tabeli.
- Dla każdego przypadku sprawdzasz trzy rzeczy: wynik, saldo po wywołaniu i pole `active` po wywołaniu. Do wyniku napisz funkcję sprawdzającą dla `TopUpResult`, jak `check_issue_result`. `check_int`, `check_bool` i `check_text` możesz skopiować z lekcji 13.3.

W `cpp-workspace` utwórz katalog `card_top_up`, skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program` i otwórz go w CLionie. Całość napisz w jednym pliku `main.cpp`. `CMakeLists.txt` zostaw bez zmian.

**Kolejność pracy:**

1. **Najpierw tabela przypadków.** Zanim napiszesz kod, przygotuj tabelę w formacie jak wyżej. Wyniki oczekiwane wyprowadź z kontraktu. Tabela ma zawierać co najmniej:
   - typowe doładowanie;
   - doładowanie, po którym saldo wynosi dokładnie 100;
   - odmowę z powodu limitu;
   - odmowę z powodu niepoprawnej kwoty;
   - odmowę z powodu nieaktywnej karty;
   - dwa przypadki, w których dwa powody odmowy zachodzą jednocześnie: nieaktywna karta z niepoprawną kwotą oraz aktywna karta z niepoprawną kwotą, przy której saldo po doładowaniu przekroczyłoby też limit;
   - dla każdego przypadku saldo i `active` po wywołaniu.

   Pod tabelą zapisz przewidywanie: które sprawdzenia się nie udadzą i co wypiszą po `actual`, gdy funkcja zacznie odrzucać doładowanie także wtedy, gdy saldo po nim wyniosłoby dokładnie 100?
2. Zdefiniuj `TopUpResult` i `Card`, napisz `top_up` i `top_up_result_text`.
3. Napisz program testowy: funkcje sprawdzające, sprawdzenia z Twojej tabeli, a na końcu podsumowanie i kod zakończenia jak w punkcie 6.
4. **To czwarte obowiązkowe uruchomienie:** uruchom program testowy z poprawną funkcją. Wszystkie sprawdzenia powinny wypisać `PASS`, a kod zakończenia powinien wynosić 0.
5. **Celowa usterka.** W warunku limitu w `top_up` zamień `>` na `>=`, tak żeby funkcja odrzucała doładowanie także wtedy, gdy saldo po nim wyniosłoby dokładnie 100. Jeśli Twój warunek ma inną postać, wprowadź usterkę o tym samym znaczeniu. Testów i wyników oczekiwanych nie zmieniaj. **To piąte obowiązkowe uruchomienie:** uruchom testy, zapisz linijki `FAIL`, podsumowanie i kod zakończenia i porównaj je z przewidywaniem z kroku 1. Potem przywróć poprawny warunek i uruchom te same testy jeszcze raz.

Nie musisz uruchamiać innych wersji. Jeśli chcesz, sprawdź jeszcze, co się stanie, gdy w `top_up` zamienisz miejscami sprawdzenie aktywności karty i sprawdzenie kwoty: który z Twoich przypadków to zauważy? Omówienie jest w przykładowym rozwiązaniu.

### Kryterium sukcesu

- [ ] Program buduje się jako C++20, a `CMakeLists.txt` jest taki jak w lekcji 0.5.
- [ ] `TopUpResult` ma cztery wartości z kontraktu, a `Card` dwa pola: `balance` i `active`.
- [ ] `top_up` dostaje kartę przez `&` i kwotę przez wartość, zwraca `TopUpResult` i niczego nie wypisuje.
- [ ] Wszystkie sprawdzenia stoją przed zmianą salda, każde występuje raz, a ich kolejność odpowiada pierwszeństwu odmowy.
- [ ] Odmowa nie zmienia ani salda, ani `active`. Doładowanie zwiększa saldo dokładnie o kwotę i nie zmienia `active`.
- [ ] `top_up_result_text` używa `switch` z etykietą `case` dla każdej z czterech wartości, a program testowy sprawdza ją dla każdej z nich.
- [ ] Tabela przypadków powstała przed kodem, a wyniki oczekiwane wynikają z kontraktu. Tabela ma wszystkie wymagane rodzaje przypadków, w tym oba przypadki z dwoma powodami odmowy naraz: nieaktywną kartę z niepoprawną kwotą i aktywną kartę z niepoprawną kwotą, przy której przekroczony byłby też limit.
- [ ] Każdy przypadek ma własny obiekt `Card`, a program sprawdza dla niego wynik, saldo i `active`.
- [ ] Wynik program porównuje jako wartość `TopUpResult`, a nie jako tekst.
- [ ] Z poprawną funkcją wszystkie sprawdzenia przechodzą, a kod zakończenia wynosi 0.
- [ ] Z usterką granicy limitu `FAIL` wypisują tylko sprawdzenia wyniku i salda w przypadkach, w których saldo miało wynieść dokładnie 100, a kod zakończenia wynosi 1. Wynik zgadza się z Twoim przewidywaniem albo umiesz wyjaśnić różnicę.
- [ ] Po przywróceniu poprawnego warunku te same testy, bez zmian, znów przechodzą z kodem 0.
- [ ] Umiesz wyjaśnić, dlaczego kolejność walidacji jest częścią kontraktu `top_up` i które przypadki z Twojej tabeli ją sprawdzają.

Gdy wynik się zgadza, możesz zapisać projekt w Gicie, jak w lekcji 1.5: `main.cpp` i `CMakeLists.txt`, bez katalogu budowania.

<details>
<summary>Podpowiedź 1: rodzaje wyniku</summary>

Jakie wartości `TopUpResult` opisują wszystkie możliwe zakończenia operacji? Dla każdej z nich znajdź w kontrakcie regułę, która ją daje, i zapisz co najmniej jeden przypadek z tym wynikiem. Czy w Twojej tabeli każda z czterech wartości pojawia się jako wynik oczekiwany?

</details>

<details>
<summary>Podpowiedź 2: niezmienność karty</summary>

W którym momencie można bezpiecznie zmienić saldo? Które dane trzeba sprawdzić przed tą zmianą? Ile miejsca zostało na karcie do limitu 100 i jak porównać z nim kwotę? Po każdej odmowie karta ma wyglądać dokładnie tak jak przed wywołaniem.

</details>

<details>
<summary>Podpowiedź 3: pierwszeństwo odmowy</summary>

Co powinno zostać zwrócone, jeśli karta jest nieaktywna, a kwota jednocześnie niepoprawna? Które sprawdzenie musi wtedy stać w funkcji wyżej? Który przypadek z Twojej tabeli dałby inny wynik, gdyby te dwa sprawdzenia zamienić miejscami?

</details>

<details>
<summary>Pełna lista przypadków kontrolnych: otwórz po przygotowaniu własnej tabeli</summary>

We wszystkich przypadkach pole `active` po wywołaniu ma tę samą wartość co przed nim.

| Przypadek | Saldo przed | Aktywna | Kwota | Wynik | Saldo po | Co sprawdza |
|---|---:|---|---:|---|---:|---|
| A | 40 | `true` | 20 | `added` | 60 | typowe doładowanie |
| B | 80 | `true` | 20 | `added` | 100 | saldo dokładnie na limicie |
| C | 100 | `true` | 1 | `limit_exceeded` | 100 | pełna karta, najmniejsza kwota |
| D | 80 | `true` | 21 | `limit_exceeded` | 80 | limit przekroczony o 1 |
| E | 50 | `true` | 0 | `invalid_amount` | 50 | kwota o 1 za mała |
| F | 50 | `true` | -1 | `invalid_amount` | 50 | kwota ujemna |
| G | 50 | `true` | 51 | `invalid_amount` | 50 | kwota o 1 za duża |
| H | 30 | `false` | 10 | `inactive_card` | 30 | nieaktywna karta, poprawna kwota |
| I | 0 | `true` | 50 | `added` | 50 | pusta karta, największa kwota |
| J | 100 | `false` | 0 | `inactive_card` | 100 | dwa powody naraz: nieaktywna karta i niepoprawna kwota |

**Dwa powody odmowy naraz** zachodzą w dwóch przypadkach i w obu o wyniku decyduje pierwszeństwo odmowy. W J karta jest nieaktywna, a kwota niepoprawna: wynik to `inactive_card`. W G kwota 51 jest niepoprawna, a saldo po doładowaniu przekroczyłoby też limit: wynik to `invalid_amount`. W pozostałych odmowach zachodzi jeden powód, więc ich wynik nie zależy od kolejności sprawdzeń.

Twoja tabela nie musi mieć wszystkich dziesięciu przypadków. Musi mieć wszystkie rodzaje wymienione w kroku 1 misji. Program referencyjny w przykładowym rozwiązaniu sprawdza osiem z nich: wszystkie poza C i F, które należą do tych samych rodzajów co D i E.

</details>

Przykładowe rozwiązanie jest w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 9. Gdy coś pójdzie inaczej

| Co widzisz | Co to znaczy | Co zrobić |
|---|---|---|
| Błąd z `value of type 'TopUpResult' is not contextually convertible to 'bool'` | Wywołanie `top_up` stoi w warunku `if`, jak funkcja zwracająca `bool` (punkt 4). | Zapisz wynik w zmiennej i porównaj go z wartością `TopUpResult` albo obsłuż go przez `switch`. |
| Błąd z `invalid operands to binary expression` przy `==` | Wynik jest porównywany z tekstem w cudzysłowie (punkt 4). | Porównuj z wartością, na przykład `TopUpResult::added`. |
| `FAIL` wyniku z `expected inactive_card, actual invalid_amount` dla nieaktywnej karty z niepoprawną kwotą | Funkcja sprawdza kwotę przed aktywnością karty. | Ustaw sprawdzenia w kolejności pierwszeństwa odmowy. |
| `FAIL` wyniku z `expected invalid_amount, actual limit_exceeded` dla zbyt dużej kwoty | Funkcja sprawdza limit przed kwotą. | Sprawdzaj limit dopiero po kwocie, zgodnie z pierwszeństwem odmowy. |
| `FAIL` wyniku i salda tylko w przypadku, w którym saldo miało wynieść dokładnie 100 | Warunek limitu odrzuca także saldo równe 100, na przykład `>=` zamiast `>`. | Odrzucaj tylko saldo, które byłoby większe niż 100. |
| Wynik odmowy jest poprawny, ale sprawdzenie salda daje `FAIL` | Funkcja zmienia saldo przed sprawdzeniem albo w ścieżce odmowy (punkt 7). | Najpierw wszystkie sprawdzenia, potem jedna zmiana salda tuż przed `return TopUpResult::added;`. |
| Wynik zgadza się z tabelą, ale saldo w kolejnych przypadkach jest przesunięte | Kilka przypadków korzysta z jednego obiektu `Card`, więc każdy zaczyna od salda zostawionego przez poprzedni. | Utwórz osobny obiekt `Card` dla każdego przypadku. |
| `FAIL` z tym samym tekstem po `expected` i po `actual`, na przykład `expected added, actual added` | Wyniki są różne, ale `top_up_result_text` zwraca ten sam tekst dla dwóch wartości. | Popraw tekst w `top_up_result_text`. Jej własne sprawdzenia też powinny to wykryć. |
| Ostrzeżenie z `enumeration value '…' not handled in switch` | W `top_up_result_text` brakuje etykiety dla jednej z wartości (lekcja 14.2). | Dopisz etykietę z właściwym tekstem. |
| Ostrzeżenie z `non-void function does not return a value in all control paths` | Po zmianie salda brakuje `return TopUpResult::added;`. Wywołanie takiej funkcji ma niezdefiniowane zachowanie (lekcja 5.4). | Dopisz `return TopUpResult::added;` po zmianie salda. |

## 10. Wyjaśnij

Odpowiedz własnymi słowami, najlepiej na piśmie. Dopiero potem porównaj z przykładowymi odpowiedziami.

1. Czym różni się wynik `bool` od nazwanego wyniku? Kiedy `bool` przestaje wystarczać?
2. Dlaczego `enum class` lepiej opisuje kilka powodów odmowy niż tekst albo liczba?
3. Co oznacza parametr `int& stock`? Czy zwrócenie nazwanego wyniku samo zmienia dane?
4. Dlaczego po odmowie dane mają zostać dokładnie takie jak przed wywołaniem?
5. Czy poprawny nazwany wynik gwarantuje poprawny stan danych? Podaj przykład z tej lekcji.
6. Dlaczego test porównuje z dokładnym wynikiem z kontraktu i nie wystarczy sprawdzić, że wynik jest inny niż `issued`?
7. Co oznacza `FAIL` sprawdzenia salda przy jednoczesnym `PASS` sprawdzenia wyniku?
8. Dlaczego w `issue_units` zamiana miejscami dwóch sprawdzeń odmowy nie zmienia wyników, a w `top_up` zamiana sprawdzenia karty i kwoty zmienia?
9. Dlaczego kolejność walidacji jest częścią kontraktu `top_up`? Jakim przypadkiem ją sprawdzasz i dlaczego nie wystarczą przypadki z jednym powodem odmowy?
10. Dlaczego kod wywołujący obsługuje każdy wynik osobno, na przykład instrukcją `switch`?
11. Po wprowadzeniu usterki test daje `FAIL`. Czy wolno zmienić wynik oczekiwany, żeby znów było `PASS`?

<details>
<summary>Przykładowe odpowiedzi</summary>

1. `bool` ma dwie wartości, więc odpowiada tylko na pytanie, czy operacja się udała. Nazwany wynik ma tyle wartości, ile jest różnych zakończeń operacji, i każde nazywa. `bool` przestaje wystarczać, gdy wywołujący musi zareagować inaczej na różne powody odmowy, na przykład podać, czy zła była ilość, czy zabrakło towaru.
2. Bo zbiór wartości jest zamknięty i znany kompilatorowi. Literówka w nazwie wartości to błąd kompilacji (lekcja 14.1), wyniku nie da się pomylić z tekstem ani liczbą, a `switch` może obsłużyć każdą wartość osobno. Tekst `"insuficient"` z literówką albo liczba `2` nie mówią, co znaczą, i kompilator ich nie sprawdzi.
3. Że funkcja dostaje dostęp do zmiennej wywołującego, a nie jej kopię, więc może zmienić tę zmienną (lekcja 9.1). Zwrócenie wyniku niczego nie zmienia: `return` przekazuje tylko wartość `IssueResult`. Stan zmienia osobna instrukcja `stock -= requested;`, wykonywana tylko przy sukcesie.
4. Bo wynik odmowy znaczy „operacja się nie odbyła”. Wywołujący zakłada wtedy, że dane są takie jak przed wywołaniem, i na przykład podaje ilość dostępną na stanie. Gdyby odmowa zmieniła dane, ten opis i dalsze operacje byłyby błędne.
5. Nie. W wariancie z `stock = 0;` funkcja zwraca poprawne `insufficient_stock`, ale stan spada z 7 do 0. Dlatego wynik i stan sprawdzasz osobno.
6. Bo `invalid_amount` i `insufficient_stock` to różne wyniki, a kontrakt mówi, który ma wrócić. Sprawdzenie „inny niż `issued`” przechodzi dla obu odmów, więc nie wykryłoby pomyłki z punktu 7.
7. Że funkcja zakończyła się właściwym wynikiem, ale zmieniła dane niezgodnie z kontraktem: odmówiła i mimo to zmieniła saldo albo przy sukcesie zmieniła je o złą wartość. To błąd skutku, a nie wyniku.
8. W `issue_units` dwa powody odmowy nigdy nie zachodzą jednocześnie: przy `stock` równym co najmniej 0 żądanie 0 albo ujemne nie jest większe od stanu. W `top_up` karta może być nieaktywna i jednocześnie mieć niepoprawną kwotę, a wtedy o wyniku decyduje to sprawdzenie, które stoi wyżej.
9. Bo gdy zachodzi kilka powodów naraz, kontrakt musi powiedzieć, który wynik wraca, a funkcja daje go tylko przy określonej kolejności sprawdzeń. Sprawdza to przypadek z dwoma powodami naraz, na przykład nieaktywna karta i kwota 0. Przypadki z jednym powodem dają ten sam wynik przy każdej kolejności sprawdzeń, więc zamiany nie wykryją.
10. Bo każdy wynik wymaga innej reakcji: przy sukcesie program pokazuje nowy stan, przy niepoprawnej kwocie mówi, jaka jest dozwolona, a przy braku towaru podaje, ile jest dostępne. `switch` z etykietą dla każdej wartości pokazuje w jednym miejscu, że żaden wynik nie został pominięty.
11. Nie. Wynik oczekiwany pochodzi z kontraktu, a nie z działania funkcji. `FAIL` oznacza, że funkcja nie spełnia kontraktu, więc poprawiasz funkcję. Zmiana oczekiwań ukryłaby błąd, a test przestałby cokolwiek sprawdzać.

</details>

## Podsumowanie

- `bool` mówi tylko, czy operacja się udała. Gdy odmowa ma kilka powodów, a wywołujący ma zareagować na każdy inaczej, funkcja zwraca **nazwany wynik**: wartość typu `enum class`, która nazywa każde możliwe zakończenie operacji.
- **Wynik i skutek to dwie różne rzeczy.** Wynik wraca przez `return`. Skutek to zmiana danych przekazanych przez `&`, wykonywana tylko przy sukcesie. Po odmowie dane są dokładnie takie jak przed wywołaniem.
- Kod wywołujący zapisuje wynik w zmiennej i obsługuje każdą wartość osobno, na przykład instrukcją `switch`. Wyniku nie porównuje się z tekstem ani nie używa jako `bool`.
- Test sprawdza osobno nazwany wynik i stan danych po wywołaniu, a wynik porównuje z dokładną wartością z kontraktu. Funkcję zamieniającą wynik na tekst też testujesz.
- Gdy kilka powodów odmowy może zajść jednocześnie, kontrakt ustala **pierwszeństwo odmowy**, a funkcja sprawdza warunki w tej kolejności. Wykrywa to tylko przypadek, w którym zachodzą dwa powody naraz.
- Po `FAIL` poprawiasz funkcję, a nie wyniki oczekiwane, i uruchamiasz te same testy jeszcze raz.

## Co dalej

W tej lekcji funkcja, która zmienia dane, mówi nazwanym wynikiem, dlaczego odmówiła. W [lekcji 14.4: Spróbuj jeszcze raz: odczyt, który odzyskuje strumień](lesson_04_reading_that_recovers_the_stream.md) ten sam pomysł trafi do funkcji odczytu: rozróżni poprawny wpis od błędnego i po błędnym wpisie przygotuje wejście na kolejną próbę.

---

## Przykładowe rozwiązania

Zajrzyj tutaj **po własnej próbie**. Twoje nazwy sprawdzeń, nazwy zmiennych, wybór przypadków i kolejność sprawdzeń w programie testowym mogą się różnić, jeśli spełniają kontrakt i listę kontrolną.

<details>
<summary>Punkt 8: misja, doładowanie karty</summary>

**Kolejność sprawdzeń w `top_up`** wynika z pierwszeństwa odmowy: najpierw aktywność karty, potem kwota, potem limit. Zmiana salda stoi na końcu, po wszystkich sprawdzeniach. Limit funkcja sprawdza dopiero po kwocie, bo wtedy wiadomo już, że kwota jest od 1 do 50. Dlatego dla kwoty 51 przy saldzie 50 wynik to `invalid_amount`, choć saldo przekroczyłoby też limit. Warunek `amount > 100 - card.balance` porównuje kwotę z miejscem, które zostało na karcie do limitu: przy saldzie 80 zostaje 20, więc kwota 20 jeszcze się mieści, a 21 już nie.

**Przypadki:** program referencyjny sprawdza osiem przypadków z pełnej listy, A, B, D, E, G, H, I i J, po trzy sprawdzenia na przypadek, czyli 24. Do tego 4 sprawdzenia tekstu, razem 28. Przypadki C i F należą do tych samych rodzajów co D i E.

**Przewidywanie:** przy usterce `>=` zamiast `>` funkcja odrzuca doładowanie, po którym saldo wyniosłoby dokładnie 100. Wśród ośmiu przypadków dotyczy to tylko B, saldo 80 i kwota 20. `FAIL` wypiszą sprawdzenie wyniku, z `limit_exceeded` po `actual`, i sprawdzenie salda, z 80 po `actual`, bo odmowa nie zmienia salda. Pozostałe 26 sprawdzeń przejdzie, a kod zakończenia wyniesie 1.

**`main.cpp`:**

<!-- example: top_up_tests -->
```cpp
#include <iostream>
#include <string>

enum class TopUpResult {
    added,
    inactive_card,
    invalid_amount,
    limit_exceeded
};

struct Card {
    int balance;
    bool active;
};

TopUpResult top_up(Card& card, int amount) {
    if (!card.active) {
        return TopUpResult::inactive_card;
    }

    if (amount < 1 || amount > 50) {
        return TopUpResult::invalid_amount;
    }

    if (amount > 100 - card.balance) {
        return TopUpResult::limit_exceeded;
    }

    card.balance += amount;
    return TopUpResult::added;
}

std::string top_up_result_text(TopUpResult result) {
    switch (result) {
        case TopUpResult::added:
            return "added";
        case TopUpResult::inactive_card:
            return "inactive_card";
        case TopUpResult::invalid_amount:
            return "invalid_amount";
        case TopUpResult::limit_exceeded:
            return "limit_exceeded";
    }

    return "unknown";
}

std::string bool_text(bool value) {
    if (value) {
        return "true";
    }

    return "false";
}

void check_top_up_result(const std::string& name, TopUpResult expected, TopUpResult actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << top_up_result_text(expected) << ", actual " << top_up_result_text(actual) << "\n";
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

int main() {
    int checks{0};
    int failed{0};

    check_text("top_up_result_text(added)", "added", top_up_result_text(TopUpResult::added), checks, failed);
    check_text("top_up_result_text(inactive_card)", "inactive_card", top_up_result_text(TopUpResult::inactive_card), checks, failed);
    check_text("top_up_result_text(invalid_amount)", "invalid_amount", top_up_result_text(TopUpResult::invalid_amount), checks, failed);
    check_text("top_up_result_text(limit_exceeded)", "limit_exceeded", top_up_result_text(TopUpResult::limit_exceeded), checks, failed);

    Card card_a{40, true};
    const TopUpResult result_a{top_up(card_a, 20)};
    check_top_up_result("A result", TopUpResult::added, result_a, checks, failed);
    check_int("A balance", 60, card_a.balance, checks, failed);
    check_bool("A active", true, card_a.active, checks, failed);

    Card card_b{80, true};
    const TopUpResult result_b{top_up(card_b, 20)};
    check_top_up_result("B result", TopUpResult::added, result_b, checks, failed);
    check_int("B balance", 100, card_b.balance, checks, failed);
    check_bool("B active", true, card_b.active, checks, failed);

    Card card_d{80, true};
    const TopUpResult result_d{top_up(card_d, 21)};
    check_top_up_result("D result", TopUpResult::limit_exceeded, result_d, checks, failed);
    check_int("D balance", 80, card_d.balance, checks, failed);
    check_bool("D active", true, card_d.active, checks, failed);

    Card card_e{50, true};
    const TopUpResult result_e{top_up(card_e, 0)};
    check_top_up_result("E result", TopUpResult::invalid_amount, result_e, checks, failed);
    check_int("E balance", 50, card_e.balance, checks, failed);
    check_bool("E active", true, card_e.active, checks, failed);

    Card card_g{50, true};
    const TopUpResult result_g{top_up(card_g, 51)};
    check_top_up_result("G result", TopUpResult::invalid_amount, result_g, checks, failed);
    check_int("G balance", 50, card_g.balance, checks, failed);
    check_bool("G active", true, card_g.active, checks, failed);

    Card card_h{30, false};
    const TopUpResult result_h{top_up(card_h, 10)};
    check_top_up_result("H result", TopUpResult::inactive_card, result_h, checks, failed);
    check_int("H balance", 30, card_h.balance, checks, failed);
    check_bool("H active", false, card_h.active, checks, failed);

    Card card_i{0, true};
    const TopUpResult result_i{top_up(card_i, 50)};
    check_top_up_result("I result", TopUpResult::added, result_i, checks, failed);
    check_int("I balance", 50, card_i.balance, checks, failed);
    check_bool("I active", true, card_i.active, checks, failed);

    Card card_j{100, false};
    const TopUpResult result_j{top_up(card_j, 0)};
    check_top_up_result("J result", TopUpResult::inactive_card, result_j, checks, failed);
    check_int("J balance", 100, card_j.balance, checks, failed);
    check_bool("J active", false, card_j.active, checks, failed);

    std::cout << "Checks: " << checks << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

<!-- output: top_up_tests -->
```text
PASS top_up_result_text(added)
PASS top_up_result_text(inactive_card)
PASS top_up_result_text(invalid_amount)
PASS top_up_result_text(limit_exceeded)
PASS A result
PASS A balance
PASS A active
PASS B result
PASS B balance
PASS B active
PASS D result
PASS D balance
PASS D active
PASS E result
PASS E balance
PASS E active
PASS G result
PASS G balance
PASS G active
PASS H result
PASS H balance
PASS H active
PASS I result
PASS I balance
PASS I active
PASS J result
PASS J balance
PASS J active
Checks: 28, failed: 0
```

Kod zakończenia: 0.

**Usterka granicy limitu.** W warunku limitu `>` zamienione na `>=`, bez innych zmian:

<!-- example: top_up_tests_limit exit=1 -->
```cpp
#include <iostream>
#include <string>

enum class TopUpResult {
    added,
    inactive_card,
    invalid_amount,
    limit_exceeded
};

struct Card {
    int balance;
    bool active;
};

TopUpResult top_up(Card& card, int amount) {
    if (!card.active) {
        return TopUpResult::inactive_card;
    }

    if (amount < 1 || amount > 50) {
        return TopUpResult::invalid_amount;
    }

    if (amount >= 100 - card.balance) {
        return TopUpResult::limit_exceeded;
    }

    card.balance += amount;
    return TopUpResult::added;
}

std::string top_up_result_text(TopUpResult result) {
    switch (result) {
        case TopUpResult::added:
            return "added";
        case TopUpResult::inactive_card:
            return "inactive_card";
        case TopUpResult::invalid_amount:
            return "invalid_amount";
        case TopUpResult::limit_exceeded:
            return "limit_exceeded";
    }

    return "unknown";
}

std::string bool_text(bool value) {
    if (value) {
        return "true";
    }

    return "false";
}

void check_top_up_result(const std::string& name, TopUpResult expected, TopUpResult actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << top_up_result_text(expected) << ", actual " << top_up_result_text(actual) << "\n";
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

int main() {
    int checks{0};
    int failed{0};

    check_text("top_up_result_text(added)", "added", top_up_result_text(TopUpResult::added), checks, failed);
    check_text("top_up_result_text(inactive_card)", "inactive_card", top_up_result_text(TopUpResult::inactive_card), checks, failed);
    check_text("top_up_result_text(invalid_amount)", "invalid_amount", top_up_result_text(TopUpResult::invalid_amount), checks, failed);
    check_text("top_up_result_text(limit_exceeded)", "limit_exceeded", top_up_result_text(TopUpResult::limit_exceeded), checks, failed);

    Card card_a{40, true};
    const TopUpResult result_a{top_up(card_a, 20)};
    check_top_up_result("A result", TopUpResult::added, result_a, checks, failed);
    check_int("A balance", 60, card_a.balance, checks, failed);
    check_bool("A active", true, card_a.active, checks, failed);

    Card card_b{80, true};
    const TopUpResult result_b{top_up(card_b, 20)};
    check_top_up_result("B result", TopUpResult::added, result_b, checks, failed);
    check_int("B balance", 100, card_b.balance, checks, failed);
    check_bool("B active", true, card_b.active, checks, failed);

    Card card_d{80, true};
    const TopUpResult result_d{top_up(card_d, 21)};
    check_top_up_result("D result", TopUpResult::limit_exceeded, result_d, checks, failed);
    check_int("D balance", 80, card_d.balance, checks, failed);
    check_bool("D active", true, card_d.active, checks, failed);

    Card card_e{50, true};
    const TopUpResult result_e{top_up(card_e, 0)};
    check_top_up_result("E result", TopUpResult::invalid_amount, result_e, checks, failed);
    check_int("E balance", 50, card_e.balance, checks, failed);
    check_bool("E active", true, card_e.active, checks, failed);

    Card card_g{50, true};
    const TopUpResult result_g{top_up(card_g, 51)};
    check_top_up_result("G result", TopUpResult::invalid_amount, result_g, checks, failed);
    check_int("G balance", 50, card_g.balance, checks, failed);
    check_bool("G active", true, card_g.active, checks, failed);

    Card card_h{30, false};
    const TopUpResult result_h{top_up(card_h, 10)};
    check_top_up_result("H result", TopUpResult::inactive_card, result_h, checks, failed);
    check_int("H balance", 30, card_h.balance, checks, failed);
    check_bool("H active", false, card_h.active, checks, failed);

    Card card_i{0, true};
    const TopUpResult result_i{top_up(card_i, 50)};
    check_top_up_result("I result", TopUpResult::added, result_i, checks, failed);
    check_int("I balance", 50, card_i.balance, checks, failed);
    check_bool("I active", true, card_i.active, checks, failed);

    Card card_j{100, false};
    const TopUpResult result_j{top_up(card_j, 0)};
    check_top_up_result("J result", TopUpResult::inactive_card, result_j, checks, failed);
    check_int("J balance", 100, card_j.balance, checks, failed);
    check_bool("J active", false, card_j.active, checks, failed);

    std::cout << "Checks: " << checks << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

<!-- output: top_up_tests_limit -->
```text
PASS top_up_result_text(added)
PASS top_up_result_text(inactive_card)
PASS top_up_result_text(invalid_amount)
PASS top_up_result_text(limit_exceeded)
PASS A result
PASS A balance
PASS A active
FAIL B result: expected added, actual limit_exceeded
FAIL B balance: expected 100, actual 80
PASS B active
PASS D result
PASS D balance
PASS D active
PASS E result
PASS E balance
PASS E active
PASS G result
PASS G balance
PASS G active
PASS H result
PASS H balance
PASS H active
PASS I result
PASS I balance
PASS I active
PASS J result
PASS J balance
PASS J active
Checks: 28, failed: 2
```

Kod zakończenia: 1.

| Przypadek | Wynik oczekiwany | Wynik rzeczywisty | Saldo oczekiwane | Saldo rzeczywiste | Sprawdzenia `FAIL` |
|---|---|---|---:|---:|---|
| B | `added` | `limit_exceeded` | 100 | 80 | wynik i saldo |
| D | `limit_exceeded` | `limit_exceeded` | 80 | 80 | żadne |
| A, I | `added` | `added` | jak w tabeli | jak w tabeli | żadne |
| E, G, H, J | jak w tabeli | bez zmian | jak w tabeli | jak w tabeli | żadne |

- **Wykrywa ją tylko B,** jedyny przypadek, w którym saldo po doładowaniu wynosi dokładnie 100. W D saldo przekroczyłoby limit, więc odmowa jest poprawna przy obu warunkach. Bez przypadku na granicy usterka przeszłaby niezauważona (lekcja 13.2).
- **Dwa `FAIL` z jednego przypadku:** wynik jest zły, a saldo zostaje 80, bo funkcja poprawnie nie zmienia karty przy odmowie. Pole `active` jest poprawne.
- **Kod 1** wynika z dwóch rzeczywistych linijek `FAIL`.

**Po naprawie:** po przywróceniu `>` program jest znów taki jak pierwsza wersja. Te same 28 sprawdzeń wypisuje `PASS` i `Checks: 28, failed: 0`, a kod zakończenia wynosi 0. Wyniki oczekiwane się nie zmieniły.

**Dodatkowa diagnostyka: zamieniona kolejność walidacji.** Funkcja sprawdza kwotę przed aktywnością karty. Pozostała część funkcji i programu jest bez zmian:

<!-- example: top_up_tests_order exit=1 -->
```cpp
#include <iostream>
#include <string>

enum class TopUpResult {
    added,
    inactive_card,
    invalid_amount,
    limit_exceeded
};

struct Card {
    int balance;
    bool active;
};

TopUpResult top_up(Card& card, int amount) {
    if (amount < 1 || amount > 50) {
        return TopUpResult::invalid_amount;
    }

    if (!card.active) {
        return TopUpResult::inactive_card;
    }

    if (amount > 100 - card.balance) {
        return TopUpResult::limit_exceeded;
    }

    card.balance += amount;
    return TopUpResult::added;
}

std::string top_up_result_text(TopUpResult result) {
    switch (result) {
        case TopUpResult::added:
            return "added";
        case TopUpResult::inactive_card:
            return "inactive_card";
        case TopUpResult::invalid_amount:
            return "invalid_amount";
        case TopUpResult::limit_exceeded:
            return "limit_exceeded";
    }

    return "unknown";
}

std::string bool_text(bool value) {
    if (value) {
        return "true";
    }

    return "false";
}

void check_top_up_result(const std::string& name, TopUpResult expected, TopUpResult actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << top_up_result_text(expected) << ", actual " << top_up_result_text(actual) << "\n";
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

int main() {
    int checks{0};
    int failed{0};

    check_text("top_up_result_text(added)", "added", top_up_result_text(TopUpResult::added), checks, failed);
    check_text("top_up_result_text(inactive_card)", "inactive_card", top_up_result_text(TopUpResult::inactive_card), checks, failed);
    check_text("top_up_result_text(invalid_amount)", "invalid_amount", top_up_result_text(TopUpResult::invalid_amount), checks, failed);
    check_text("top_up_result_text(limit_exceeded)", "limit_exceeded", top_up_result_text(TopUpResult::limit_exceeded), checks, failed);

    Card card_a{40, true};
    const TopUpResult result_a{top_up(card_a, 20)};
    check_top_up_result("A result", TopUpResult::added, result_a, checks, failed);
    check_int("A balance", 60, card_a.balance, checks, failed);
    check_bool("A active", true, card_a.active, checks, failed);

    Card card_b{80, true};
    const TopUpResult result_b{top_up(card_b, 20)};
    check_top_up_result("B result", TopUpResult::added, result_b, checks, failed);
    check_int("B balance", 100, card_b.balance, checks, failed);
    check_bool("B active", true, card_b.active, checks, failed);

    Card card_d{80, true};
    const TopUpResult result_d{top_up(card_d, 21)};
    check_top_up_result("D result", TopUpResult::limit_exceeded, result_d, checks, failed);
    check_int("D balance", 80, card_d.balance, checks, failed);
    check_bool("D active", true, card_d.active, checks, failed);

    Card card_e{50, true};
    const TopUpResult result_e{top_up(card_e, 0)};
    check_top_up_result("E result", TopUpResult::invalid_amount, result_e, checks, failed);
    check_int("E balance", 50, card_e.balance, checks, failed);
    check_bool("E active", true, card_e.active, checks, failed);

    Card card_g{50, true};
    const TopUpResult result_g{top_up(card_g, 51)};
    check_top_up_result("G result", TopUpResult::invalid_amount, result_g, checks, failed);
    check_int("G balance", 50, card_g.balance, checks, failed);
    check_bool("G active", true, card_g.active, checks, failed);

    Card card_h{30, false};
    const TopUpResult result_h{top_up(card_h, 10)};
    check_top_up_result("H result", TopUpResult::inactive_card, result_h, checks, failed);
    check_int("H balance", 30, card_h.balance, checks, failed);
    check_bool("H active", false, card_h.active, checks, failed);

    Card card_i{0, true};
    const TopUpResult result_i{top_up(card_i, 50)};
    check_top_up_result("I result", TopUpResult::added, result_i, checks, failed);
    check_int("I balance", 50, card_i.balance, checks, failed);
    check_bool("I active", true, card_i.active, checks, failed);

    Card card_j{100, false};
    const TopUpResult result_j{top_up(card_j, 0)};
    check_top_up_result("J result", TopUpResult::inactive_card, result_j, checks, failed);
    check_int("J balance", 100, card_j.balance, checks, failed);
    check_bool("J active", false, card_j.active, checks, failed);

    std::cout << "Checks: " << checks << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

<!-- output: top_up_tests_order -->
```text
PASS top_up_result_text(added)
PASS top_up_result_text(inactive_card)
PASS top_up_result_text(invalid_amount)
PASS top_up_result_text(limit_exceeded)
PASS A result
PASS A balance
PASS A active
PASS B result
PASS B balance
PASS B active
PASS D result
PASS D balance
PASS D active
PASS E result
PASS E balance
PASS E active
PASS G result
PASS G balance
PASS G active
PASS H result
PASS H balance
PASS H active
PASS I result
PASS I balance
PASS I active
FAIL J result: expected inactive_card, actual invalid_amount
PASS J balance
PASS J active
Checks: 28, failed: 1
```

Kod zakończenia: 1.

- **Wykrywa ją tylko J:** nieaktywna karta i kwota 0. Kontrakt daje pierwszeństwo `inactive_card`, a funkcja najpierw trafia na sprawdzenie kwoty i zwraca `invalid_amount`. Saldo i `active` są poprawne, bo odmowa niczego nie zmienia.
- **Przypadki, w których karta i kwota nie są błędne jednocześnie, jej nie wykrywają.** H to nieaktywna karta z poprawną kwotą: sprawdzenie kwoty przepuszcza ją dalej, a sprawdzenie karty daje `inactive_card`, jak w kontrakcie. E i G to niepoprawne kwoty na aktywnej karcie: przy aktywnej karcie wynik `invalid_amount` jest ten sam przy obu kolejnościach. Każda reguła z osobna działa, a błąd tkwi w ich kolejności.
- **G sprawdza inną parę powodów:** kwota 51 jest niepoprawna, a saldo przekroczyłoby limit. Ten przypadek nie wykrywa zamiany sprawdzenia karty i kwoty, ale wykryłby zamianę sprawdzenia kwoty i sprawdzenia limitu: funkcja zwróciłaby wtedy `limit_exceeded`.
- **Jeśli Twój przypadek z dwoma powodami to inna para,** na przykład nieaktywna karta z pełnym saldem i kwotą 1, zamiana karty i kwoty go nie dotyczy, bo kwota 1 jest poprawna. Taki przypadek wykryje za to zamianę sprawdzenia karty i sprawdzenia limitu. Każda para powodów, które mogą zajść jednocześnie, potrzebuje własnego przypadku.

**Samoocena.** Porównaj swoją pracę z listą kontrolną w punkcie 8. Szczególnie sprawdź:
- czy Twoja tabela powstała przed kodem i ma wszystkie wymagane rodzaje przypadków, w tym saldo dokładnie 100 i dwa powody odmowy naraz;
- czy każdy przypadek ma własny obiekt `Card` i czy sprawdzasz w nim wynik, saldo i `active`;
- czy wynik porównujesz jako wartość `TopUpResult`, a tekst służy tylko do linijki `FAIL`;
- czy Twoje przewidywanie z kroku 1 zgadzało się z wynikiem kroku 5, a jeśli nie, czy umiesz wyjaśnić różnicę;
- czy umiesz wskazać przypadek, który wykryłby zamianę sprawdzenia karty i sprawdzenia kwoty.

Jeśli w jednym z tych punktów odpowiedź brzmi „nie”, wróć do odpowiedniego punktu lekcji, zanim przejdziesz dalej.

</details>

**Poprzednia lekcja:** [Lekcja 14.2: Każdy stan obsłużony: `switch`](lesson_02_handling_every_state_with_switch.md) · **Następna lekcja:** [Lekcja 14.4: Spróbuj jeszcze raz: odczyt, który odzyskuje strumień](lesson_04_reading_that_recovers_the_stream.md) · [Opis kursu](../../README.md)

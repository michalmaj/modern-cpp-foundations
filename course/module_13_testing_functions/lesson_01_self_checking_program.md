# Lekcja 13.1: Program, który sam sprawdza wynik

**Polski** · [English](lesson_01_self_checking_program.en.md) · [Opis kursu](../../README.md)

> **Moduł 13, lekcja 1** · około 80–95 minut, można ją podzielić na dwa podejścia
> **Potrzebujesz:** katalogu `cpp-workspace` i oryginalnego projektu `lesson_05_first_program`, jak dotąd. Debugger nie jest w tej lekcji potrzebny.
> **Wersja pilotażowa.** Programy z tej lekcji sprawdzamy automatycznie na Windowsie, Ubuntu i macOS, razem z ich kodem zakończenia.

## Zanim zaczniesz

Ta lekcja zakłada, że:

- wiesz, że `main` przekazuje systemowi kod zakończenia, a `0` znaczy umownie „wszystko w porządku” (lekcja 1.3);
- piszesz funkcje z parametrami i wynikiem, także funkcje z kilkoma `return` (lekcje 5.2–5.4);
- znasz wydruki testowe z lekcji 5.5: kilka wywołań funkcji z dobranymi argumentami i porównanie wyników z oczekiwaniami;
- przygotowujesz przed uruchomieniem tabelę przypadków z oczekiwanymi wynikami (od Modułu 3);
- przekazujesz tekst przez `const std::string&` (lekcja 7.3), a zmienną do zmiany przez referencję, jak `int& error_line` w lekcji 12.3 (lekcja 9.1).

## Sytuacja

Parking przy bibliotece liczy opłatę za pełne godziny postoju. Reguły zapisano w funkcji `parking_fee`. Ktoś ją kiedyś zmieni, na przykład gdy zmieni się cennik, i wtedy trzeba sprawdzić, czy nadal liczy dobrze.

Dotąd takie sprawdzenie wyglądało zawsze tak samo: uruchamiasz program, patrzysz na wypisany wynik i porównujesz go w pamięci albo na kartce z tym, co powinno wyjść. W tej lekcji odpowiesz na pytanie: **czy program może sam porównać wynik funkcji z oczekiwanym i jasno powiedzieć, że coś się nie zgadza?**

Po tej lekcji będziesz:

- odróżniać wypisanie wyniku funkcji od jego sprawdzenia;
- ustalać wynik oczekiwany ze specyfikacji, zanim uruchomisz program;
- pisać program testowy, który porównuje wynik rzeczywisty z oczekiwanym i wypisuje `PASS` albo `FAIL`;
- liczyć testy i niepowodzenia i kończyć program testowy kodem 1, gdy któryś test się nie udał;
- rozpoznawać wadliwy program testowy: taki, który nie może wykryć błędu, albo taki, który wykrywa błąd, ale nie zgłasza go kodem zakończenia.

## 1. Od ręcznego sprawdzania do testu

**Kontrakt funkcji `parking_fee`:**

- `int parking_fee(int hours)`, gdzie `hours` to liczba pełnych godzin postoju;
- dopuszczalne wartości `hours`: od 0 do 8;
- 0 godzin: opłata 0;
- pierwsza godzina kosztuje 5, każda następna 3;
- dla liczby godzin spoza zakresu 0–8 funkcja zwraca -1. Opłata nigdy nie jest ujemna, więc -1 jednoznacznie oznacza „niepoprawne dane”.

Ten program wywołuje funkcję i wypisuje jej wynik, tak jak wydruki testowe z lekcji 5.5:

<!-- example: parking_print -->
```cpp
#include <iostream>

int parking_fee(int hours) {
    if (hours < 0 || hours > 8) {
        return -1;
    }

    if (hours == 0) {
        return 0;
    }

    return 5 + 3 * (hours - 1);
}

int main() {
    std::cout << parking_fee(3) << "\n";
}
```

Program wypisuje:

<!-- output: parking_print -->
```text
11
```

**Skąd wiesz, że `11` to dobry wynik?** Program tego nie wie. Wie to osoba, która go uruchomiła: czyta kontrakt, liczy 5 + 3 + 3 = 11 i porównuje z tym, co widzi. Wydruki testowe z lekcji 5.5 działały tak samo. Były dobrym krokiem: sprawdzały jedną funkcję naraz, na dobranych argumentach. Mają jednak granice:

- **porównanie wykonuje człowiek**, przy każdym uruchomieniu od nowa;
- przy kilkunastu linijkach łatwo przeoczyć jedną złą liczbę;
- po każdej zmianie funkcji trzeba wszystkie wyniki porównać jeszcze raz;
- dla programu `11` i `14` to tylko liczby do wypisania. Nie ma w nim informacji, która z nich jest poprawna.

**Test** przenosi to porównanie do programu. Program dostaje wynik, którego oczekujesz, sam porównuje go z wynikiem funkcji i wypisuje werdykt.

## 2. Wynik oczekiwany i wynik rzeczywisty

Każdy test potrzebuje dwóch wartości:

- **wynik oczekiwany** (*expected result*): to, co funkcja powinna zwrócić według kontraktu. Ustalasz go **samodzielnie, z kontraktu, przed uruchomieniem programu**;
- **wynik rzeczywisty** (*actual result*): to, co funkcja naprawdę zwróciła po wywołaniu.

Argument funkcji razem z wynikiem oczekiwanym to **przypadek testowy** (*test case*), znany z tabel przypadków. Dla `parking_fee` wyniki oczekiwane wynikają z kontraktu tak:

| `hours` | Wynik oczekiwany | Skąd |
|---:|---:|---|
| -1 | -1 | poza zakresem 0–8 |
| 0 | 0 | brak postoju |
| 1 | 5 | pierwsza godzina |
| 2 | 8 | 5 + 3 |
| 3 | 11 | 5 + 3 + 3 |
| 8 | 26 | 5 + 7 · 3 |
| 9 | -1 | poza zakresem 0–8 |

Żadna liczba w kolumnie „Wynik oczekiwany” nie pochodzi z uruchomienia funkcji. Gdyby wynik oczekiwany wziąć z tego, co funkcja zwraca dziś, test sprawdzałby tylko, czy funkcja zwraca to, co zwraca. Do tej pułapki wrócisz w punkcie 9.

## 3. Pierwsze sprawdzenie: PASS albo FAIL

Najprostszy test to jeden warunek:

<!-- example: parking_first_check -->
```cpp
#include <iostream>

int parking_fee(int hours) {
    if (hours < 0 || hours > 8) {
        return -1;
    }

    if (hours == 0) {
        return 0;
    }

    return 5 + 3 * (hours - 1);
}

int main() {
    if (parking_fee(3) == 11) {
        std::cout << "PASS\n";
    } else {
        std::cout << "FAIL\n";
    }
}
```

<!-- output: parking_first_check -->
```text
PASS
```

Wynik oczekiwany `11` stoi teraz w kodzie, a porównanie wykonuje program. Człowiek czyta już tylko werdykt:

- **`PASS`** (*passing test*, test zakończony sukcesem): wynik rzeczywisty jest równy oczekiwanemu. Dla tego przypadku funkcja działa zgodnie z kontraktem;
- **`FAIL`** (*failing test*, test zakończony niepowodzeniem): wyniki się różnią. Błąd jest w funkcji albo w samym teście, na przykład w źle policzonym wyniku oczekiwanym. Program nie wie, który z nich. To ustalasz, wracając do kontraktu.

Ten pierwszy test ma dwie słabości. `FAIL` nie mówi, **który** przypadek się nie udał ani **jaki** wynik wyszedł. A dla siedmiu przypadków z tabeli trzeba by przepisać ten sam `if` siedem razy. Powtarzany kod to sygnał, który znasz z Modułu 5: czas na funkcję.

## 4. Funkcja sprawdzająca

Ta funkcja wykonuje jeden test:

<!-- fragment -->
```cpp
void check_equal(const std::string& name, int expected, int actual, int& tests, int& failed) {
    ++tests;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << expected << ", actual " << actual << "\n";
        ++failed;
    }
}
```

| Parametr | Po co |
|---|---|
| `const std::string& name` | nazwa testu, na przykład `parking_fee(0)`. Gdy test się nie uda, od razu widać, który |
| `int expected` | wynik oczekiwany, policzony z kontraktu |
| `int actual` | wynik rzeczywisty. W wywołaniu podajesz tu samo wywołanie funkcji, na przykład `parking_fee(0)`: najpierw wykonuje się `parking_fee`, a jej wynik staje się argumentem |
| `int& tests` | licznik wykonanych testów w `main`. Referencja, bo funkcja ma zmienić zmienną z `main`, a nie własną kopię (lekcja 9.1) |
| `int& failed` | licznik niepowodzeń w `main`, z tego samego powodu. Rośnie **tylko** przy niezgodności |

`check_equal` niczego nie zwraca (`void`), bo jej wynik to wypisany werdykt i zmienione liczniki. Linijka `FAIL` podaje oba wyniki: `expected` i `actual`. Dzięki temu widzisz od razu, co się nie zgadza, i nie musisz niczego liczyć jeszcze raz.

## 5. Kilka testów i podsumowanie

Pełny program testowy dla trzech przypadków z tabeli:

<!-- example: parking_tests -->
```cpp
#include <iostream>
#include <string>

int parking_fee(int hours) {
    if (hours < 0 || hours > 8) {
        return -1;
    }

    if (hours == 0) {
        return 0;
    }

    return 5 + 3 * (hours - 1);
}

void check_equal(const std::string& name, int expected, int actual, int& tests, int& failed) {
    ++tests;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << expected << ", actual " << actual << "\n";
        ++failed;
    }
}

int main() {
    int tests{0};
    int failed{0};

    check_equal("parking_fee(0)", 0, parking_fee(0), tests, failed);
    check_equal("parking_fee(1)", 5, parking_fee(1), tests, failed);
    check_equal("parking_fee(3)", 11, parking_fee(3), tests, failed);

    std::cout << "Tests: " << tests << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

**To pierwsze obowiązkowe uruchomienie.** W `cpp-workspace` utwórz katalog `lesson_13_1`, skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program` i otwórz go w CLionie. Zastąp zawartość `main.cpp` tym programem, zbuduj go i uruchom. `CMakeLists.txt` zostaw bez zmian. Kolejne programy z tej lekcji wpisujesz w ten sam `main.cpp`.

**Przewidź** wynik, zanim uruchomisz program.

<details>
<summary>Standardowe wyjście</summary>

<!-- output: parking_tests -->
```text
PASS parking_fee(0)
PASS parking_fee(1)
PASS parking_fee(3)
Tests: 3, failed: 0
```

Pod wynikiem CLion dopisuje `Process finished with exit code 0`.

</details>

**Jak liczone są testy:**

- `main` zaczyna od `tests{0}` i `failed{0}`;
- każde wywołanie `check_equal` to jeden test, więc każde zwiększa `tests` o 1;
- `failed` rośnie tylko wtedy, gdy wynik rzeczywisty różni się od oczekiwanego;
- po wszystkich testach program wypisuje jedno podsumowanie: `Tests: 3, failed: 0`.

Kolejność testów nie ma tu znaczenia: każdy wywołuje `parking_fee` od nowa i nie korzysta z wyników poprzednich.

## 6. Kod zakończenia programu testowego

Koniec `main` to nowa część:

<!-- fragment -->
```cpp
if (failed > 0) {
    return 1;
}

return 0;
```

Z lekcji 1.3 wiesz, że `main` przekazuje systemowi kod zakończenia: `0` znaczy umownie „wszystko w porządku”, a inna liczba „coś poszło nie tak”, a co dokładnie, ustala autor programu. **Program testowy z tej lekcji ma taki kontrakt:**

| Sytuacja | Kod zakończenia |
|---|---|
| wszystkie testy zakończyły się sukcesem | `0` |
| co najmniej jeden test zakończył się niepowodzeniem | `1` |

**Po co kod, skoro jest napis `FAIL`?** Napis czyta człowiek. Kod zakończenia odczytuje każdy, kto uruchomił program: CLion, skrypt, a także automatyczne sprawdzanie tego kursu, które uruchamia programy z lekcji. Kod zakończenia nie jest częścią standardowego wyjścia, więc żaden z nich nie musi czytać ani rozumieć tekstu. Dzięki temu **wynik testów nie zależy od tego, czy ktoś uważnie przeczytał wszystkie linijki.**

**To zmiana konwencji, ale tylko dla programów testowych.** W Modułach 10–12 program, który odrzucił błędne dane, wypisywał komunikat i kończył się kodem 0. Tak miało być: odrzucenie złych danych to poprawne działanie tamtych programów. Program testowy ma inne zadanie: sprawdza inny kod. Nieudany test znaczy, że coś nie zgadza się z kontraktem, i to właśnie trzeba zgłosić. Wcześniejszych programów nie zmieniasz.

**Gdzie zobaczyć kod zakończenia:** w ostatniej linijce okna **Run** w CLionie, `Process finished with exit code …`, jak w lekcji 1.3. Terminal sam go nie wypisuje, dlatego w tej lekcji odczytujesz kod w CLionie.

**Inne narzędzia.** C++ ma też makro `assert` (nagłówek `<cassert>`), a programiści korzystają z gotowych bibliotek do testów. Mają swoje zastosowania, ale nie są tematem tej lekcji. Tutaj piszesz sprawdzanie samodzielnie, bo chcesz zobaczyć wynik każdego testu, policzyć niepowodzenia, mieć ten sam tekst na każdym systemie i samodzielnie ustalić kod zakończenia.

## 7. Testy wykrywają błąd

Ktoś zmienił `parking_fee` i popełnił błąd: dla 0 godzin funkcja zwraca teraz 5, jakby każdy wjazd na parking kosztował tyle co pierwsza godzina. Program testowy jest **ten sam** co w punkcie 5. Zmieniły się tylko dwie linijki funkcji: warunek `hours <= 1` zamiast `hours == 0` i `return 5;` zamiast `return 0;`.

<!-- example: parking_tests_bug exit=1 -->
```cpp
#include <iostream>
#include <string>

int parking_fee(int hours) {
    if (hours < 0 || hours > 8) {
        return -1;
    }

    if (hours <= 1) {
        return 5;
    }

    return 5 + 3 * (hours - 1);
}

void check_equal(const std::string& name, int expected, int actual, int& tests, int& failed) {
    ++tests;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << expected << ", actual " << actual << "\n";
        ++failed;
    }
}

int main() {
    int tests{0};
    int failed{0};

    check_equal("parking_fee(0)", 0, parking_fee(0), tests, failed);
    check_equal("parking_fee(1)", 5, parking_fee(1), tests, failed);
    check_equal("parking_fee(3)", 11, parking_fee(3), tests, failed);

    std::cout << "Tests: " << tests << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

**To drugie obowiązkowe uruchomienie.** W `main.cpp` zmień tylko funkcję `parking_fee`, jak wyżej, zbuduj program i uruchom go. **Przewidź** wynik każdej linijki i kod zakończenia.

<details>
<summary>Standardowe wyjście i kod zakończenia</summary>

<!-- output: parking_tests_bug -->
```text
FAIL parking_fee(0): expected 0, actual 5
PASS parking_fee(1)
PASS parking_fee(3)
Tests: 3, failed: 1
```

CLion pokazuje `Process finished with exit code 1`.

</details>

**Co tu się stało:**

- program się zbudował: to nie jest błąd kompilacji ani linkowania;
- program testowy wykonał wszystkie trzy testy i działał dokładnie tak, jak powinien;
- test `parking_fee(0)` dostał 5 zamiast 0, więc wypisał `FAIL` z obiema wartościami i zwiększył `failed`;
- testy dla 1 i 3 godzin nadal przechodzą, bo błąd ich nie dotyczy;
- `failed` wynosi 1, więc `main` zwraca 1.

To jest **test wykrywający błąd**. Kod zakończenia 1 nie znaczy, że zawiódł program testowy. Znaczy, że **program testowy znalazł błąd w sprawdzanej funkcji**, czyli zrobił to, po co powstał.

Przywróć poprawną funkcję z punktu 5 i uruchom program jeszcze raz: znowu trzy razy `PASS`, `Tests: 3, failed: 0` i kod 0. **Po każdej zmianie funkcji uruchamiasz te same testy.** Nie trzeba ich pisać od nowa ani niczego liczyć w pamięci: sprawdzenie, przygotowane raz, powtarza się za jednym kliknięciem.

## 8. Diagnostyka: program testowy wykrywa błąd, ale sam zgłasza sukces

**Sytuacja.** W innym programie testowym ktoś pominął koniec `main`. Funkcja `parking_fee` ma błąd z punktu 7.

<!-- example: parking_exit_bug -->
```cpp
#include <iostream>
#include <string>

int parking_fee(int hours) {
    if (hours < 0 || hours > 8) {
        return -1;
    }

    if (hours <= 1) {
        return 5;
    }

    return 5 + 3 * (hours - 1);
}

void check_equal(const std::string& name, int expected, int actual, int& tests, int& failed) {
    ++tests;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << expected << ", actual " << actual << "\n";
        ++failed;
    }
}

int main() {
    int tests{0};
    int failed{0};

    check_equal("parking_fee(0)", 0, parking_fee(0), tests, failed);
    check_equal("parking_fee(1)", 5, parking_fee(1), tests, failed);
    check_equal("parking_fee(3)", 11, parking_fee(3), tests, failed);

    std::cout << "Tests: " << tests << ", failed: " << failed << "\n";
}
```

**To trzecie obowiązkowe uruchomienie: jedna czynność diagnostyczna.** Ten program powstaje z programu z punktu 7: usuń z końca `main` sprawdzenie `if (failed > 0)` razem z `return 0;`.

1. **Przewidź** wypisany tekst.
2. Uruchom program i sprawdź kod zakończenia w ostatniej linijce okna **Run**.
3. Wyjaśnij sprzeczność między tekstem a kodem zakończenia.
4. Wskaż błąd w `main`.
5. Zaproponuj najmniejszą poprawkę.
6. Wprowadź ją i potwierdź, że teraz nieudany test daje kod 1.

<details>
<summary>Standardowe wyjście i kod zakończenia</summary>

<!-- output: parking_exit_bug -->
```text
FAIL parking_fee(0): expected 0, actual 5
PASS parking_fee(1)
PASS parking_fee(3)
Tests: 3, failed: 1
```

CLion pokazuje `Process finished with exit code 0`.

</details>

<details>
<summary>Wyjaśnienie i poprawka</summary>

- **Sprzeczność:** człowiek czyta `FAIL` i `failed: 1`, a każdy, kto sprawdza tylko kod zakończenia, dostaje 0, czyli „wszystko w porządku”. CLion, skrypt albo automatyczne sprawdzanie uznałyby, że testy przeszły.
- **Błąd:** `main` nie sprawdza `failed` przed końcem. Gdy program dochodzi do końca `main` bez `return`, działa to jak `return 0;` (lekcja 1.3), więc kod jest zawsze 0, niezależnie od wyniku testów.
- **Najmniejsza poprawka:** dopisz przed `}` funkcji `main`:

<!-- fragment -->
```cpp
if (failed > 0) {
    return 1;
}

return 0;
```

- **Po poprawce** program jest dokładnie programem z punktu 7: wypisuje te same cztery linijki i kończy się kodem 1.

To był **wadliwy program testowy**. Wykrył błąd funkcji, ale go nie zgłosił. Funkcja `parking_fee` jest tu tak samo błędna jak w punkcie 7. Różnica jest w programie testowym.

</details>

## 9. Test, który nie może się nie udać

Drugi rodzaj wadliwego programu testowego wygląda niewinnie. Funkcja `parking_fee` ma znowu błąd z punktu 7, a test porównuje ją... z nią samą:

<!-- example: parking_self_check -->
```cpp
#include <iostream>
#include <string>

int parking_fee(int hours) {
    if (hours < 0 || hours > 8) {
        return -1;
    }

    if (hours <= 1) {
        return 5;
    }

    return 5 + 3 * (hours - 1);
}

void check_equal(const std::string& name, int expected, int actual, int& tests, int& failed) {
    ++tests;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << expected << ", actual " << actual << "\n";
        ++failed;
    }
}

int main() {
    int tests{0};
    int failed{0};

    check_equal("parking_fee(0)", parking_fee(0), parking_fee(0), tests, failed);

    std::cout << "Tests: " << tests << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

Uruchamianie tego programu jest nieobowiązkowe. **Przewidź** jego wynik, zanim otworzysz zwinięty blok.

<details>
<summary>Standardowe wyjście</summary>

<!-- output: parking_self_check -->
```text
PASS parking_fee(0)
Tests: 1, failed: 0
```

Kod zakończenia: 0.

</details>

Funkcja zwraca 5 dla 0 godzin, a test i tak przechodzi. Wynik oczekiwany nie pochodzi z kontraktu, tylko z tej samej funkcji, więc oba argumenty są zawsze równe. **Taki test nie może się nie udać, więc niczego nie sprawdza.** To również wadliwy program testowy.

Ta sama pułapka ma subtelniejszą postać: wynik oczekiwany liczony w teście tym samym wzorem co w funkcji, na przykład `5 + 3 * (hours - 1)`. Jeśli wzór jest zły, test powtórzy ten sam błąd i też przejdzie. Wynik oczekiwany liczysz z kontraktu, jak w tabeli z punktu 2, i wpisujesz w test jako gotową liczbę.

**Pięć zasad dobrego testu:**

1. Wynik oczekiwany pochodzi ze specyfikacji, a nie z działania sprawdzanej funkcji.
2. Każdy test ma nazwę, która mówi, co sprawdza.
3. Test musi mieć możliwość niepowodzenia: przy błędnej funkcji powinien wypisać `FAIL`.
4. Niepowodzenie widać w dwóch miejscach: w standardowym wyjściu i w kodzie zakończenia.
5. Po każdej zmianie funkcji uruchamiasz ponownie te same testy.

## 10. Misja: koszt wydruku

Punkt ksero liczy koszt wydruku dokumentu. Napisz funkcję i jej program testowy.

**Kontrakt funkcji `print_cost`:**

- `int print_cost(int pages)`, gdzie `pages` to liczba stron;
- dopuszczalna liczba stron: od 0 do 10;
- 0 stron kosztuje 0;
- strony od pierwszej do trzeciej kosztują po 2;
- każda kolejna strona, od czwartej, kosztuje 1;
- dla liczby stron spoza zakresu 0–10 funkcja zwraca -1.

W `cpp-workspace` utwórz katalog `print_cost`, skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program` i otwórz go w CLionie. Funkcję i program testowy napisz samodzielnie w `main.cpp`, w jednym pliku, jak w punkcie 5. `CMakeLists.txt` zostaw bez zmian.

**Kolejność pracy:**

1. **Najpierw wyniki oczekiwane.** Zanim napiszesz jakikolwiek kod, policz z kontraktu wyniki oczekiwane dla co najmniej 0, 1, 4 i 11 stron. Zapisz je w tabeli z kolumną „Skąd”, jak w punkcie 2. Możesz dodać własne przypadki, na przykład 3, 5, 10 albo -1.
2. Napisz `print_cost`.
3. Napisz program testowy: funkcję sprawdzającą, co najmniej cztery testy, dla 0, 1, 4 i 11 stron, podsumowanie i kod zakończenia według kontraktu z punktu 6.
4. **To czwarte obowiązkowe uruchomienie:** uruchom program z poprawną funkcją. Wszystkie testy powinny wypisać `PASS`, a kod zakończenia powinien wynosić 0.
5. **Celowy błąd.** Zmień w `print_cost` jedną granicę albo jedną liczbę tak, żeby wynik dla 4 stron był zły, a funkcja nadal się budowała. Jeśli nie masz pomysłu, otwórz propozycję poniżej. Pełny program z tym błędem jest w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).
6. **To piąte obowiązkowe uruchomienie:** uruchom ten sam program testowy z błędną funkcją. Zapisz, który test się nie udał, jaki był wynik oczekiwany, jaki rzeczywisty i jaki jest kod zakończenia. Potem przywróć poprawną funkcję.

<details>
<summary>Propozycja celowego błędu</summary>

Spraw, żeby czwarta strona kosztowała 2 zamiast 1, na przykład przesuwając granicę pierwszego przedziału cen o jedną stronę dalej. Wynik dla 4 stron będzie wtedy o 1 za duży.

</details>

<details>
<summary>Wyniki oczekiwane: otwórz po przygotowaniu własnej tabeli</summary>

| Strony | Wynik oczekiwany | Skąd |
|---:|---:|---|
| -1 | -1 | poza zakresem 0–10 |
| 0 | 0 | brak stron |
| 1 | 2 | jedna strona po 2 |
| 3 | 6 | 3 · 2 |
| 4 | 7 | 3 · 2 + 1 |
| 5 | 8 | 3 · 2 + 2 · 1 |
| 10 | 13 | 3 · 2 + 7 · 1 |
| 11 | -1 | poza zakresem 0–10 |

</details>

W tej misji nie musisz jeszcze wybierać przypadków według jakiejś strategii. Cztery wymagane wystarczą. Jak dobierać przypadki, żeby wykrywały istotne błędy, to temat następnej lekcji.

### Kryterium sukcesu

- Program buduje się jako C++20, a `CMakeLists.txt` jest taki jak w lekcji 0.5.
- `print_cost` zwraca wyniki zgodne z kontraktem.
- Wyniki oczekiwane policzono z kontraktu przed napisaniem testów i wpisano w testy jako liczby, bez wywoływania `print_cost` i bez kopiowania jej wzoru.
- Są co najmniej cztery testy: dla 0, 1, 4 i 11 stron, każdy z nazwą.
- Każdy test wypisuje `PASS nazwa` albo `FAIL nazwa: expected X, actual Y`, a na końcu program wypisuje `Tests: N, failed: F`.
- Z poprawną funkcją wszystkie testy przechodzą, a kod zakończenia wynosi 0.
- Z celowo błędną funkcją test dla 4 stron wypisuje `FAIL`, a kod zakończenia wynosi 1.
- Umiesz powiedzieć, który test wykrył błąd, jaki był wynik oczekiwany i rzeczywisty i dlaczego program zwrócił 1.

Gdy wynik się zgadza, możesz zapisać projekt w Gicie, jak w lekcji 1.5: `main.cpp` i `CMakeLists.txt`, bez katalogu budowania.

<details>
<summary>Podpowiedź 1: wyniki oczekiwane</summary>

Zanim napiszesz porównanie, policz każdy wynik oczekiwany na kartce, wprost z kontraktu. Ile stron kosztuje po 2, a ile po 1, gdy stron jest 4? Czy 11 stron mieści się w zakresie? Wpisz te liczby do tabeli z kolumną „Skąd”. Do testów przepisujesz potem gotowe liczby z tabeli.

</details>

<details>
<summary>Podpowiedź 2: werdykt</summary>

Jeden test potrzebuje trzech rzeczy: nazwy, wyniku oczekiwanego i wyniku rzeczywistego. Wynik rzeczywisty to wywołanie `print_cost` z argumentem z tabeli. Gdy oba wyniki są równe, test wypisuje `PASS` i nazwę. Gdy się różnią, wypisuje `FAIL`, nazwę i obie wartości, w formacie z punktu 4. Funkcja sprawdzająca z punktu 4 nie zależy od tego, którą funkcję sprawdzasz.

</details>

<details>
<summary>Podpowiedź 3: niepowodzenia i kod zakończenia</summary>

Które zmienne w `main` muszą się zmieniać w czasie testów i dlaczego funkcja sprawdzająca dostaje je przez referencję? Kod zakończenia zależy od jednej z nich. Sprawdź go dopiero po wszystkich testach, żeby każdy test się wykonał i wypisał swój werdykt.

</details>

## 11. Gdy coś pójdzie inaczej

| Co widzisz | Co to znaczy | Co zrobić |
|---|---|---|
| `FAIL` w wyniku, a CLion pokazuje `exit code 0` | `main` nie zwraca 1 po niepowodzeniu (punkt 8). | Przed końcem `main` sprawdź licznik niepowodzeń i zwróć 1, gdy jest większy od 0. |
| Jest linijka `FAIL`, a podsumowanie mówi `failed: 0` | Licznik niepowodzeń trafia do funkcji przez wartość, na przykład `int failed`. Funkcja zwiększa własną kopię, a zmienna w `main` się nie zmienia (lekcje 5.2 i 9.1). | Zmień parametr na `int& failed`. To samo sprawdź dla licznika testów. |
| Wszystkie testy przechodzą, choć celowo zepsuto funkcję | Wynik oczekiwany pochodzi z wywołania sprawdzanej funkcji albo z jej wzoru (punkt 9), albo żaden test nie dotyczy zmienionego miejsca. | Sprawdź, skąd pochodzi każdy wynik oczekiwany, i czy któryś test używa argumentu, dla którego funkcja się zmieniła. |
| `FAIL` dla funkcji, która wydaje się poprawna | Błąd może być w samym teście, na przykład w źle policzonym wyniku oczekiwanym. | Policz ten wynik jeszcze raz z kontraktu. Popraw tę stronę, która nie zgadza się z kontraktem. |
| Terminal nie pokazuje kodu zakończenia | Terminal go nie wypisuje. Kod zakończenia nie jest częścią standardowego wyjścia. | W tej lekcji odczytuj kod w ostatniej linijce okna **Run** w CLionie. |

## 12. Wyjaśnij

Odpowiedz własnymi słowami, najlepiej na piśmie. Dopiero potem porównaj z przykładowymi odpowiedziami.

1. Czym test różni się od zwykłego `std::cout`, który wypisuje wynik funkcji?
2. Skąd pochodzi wynik oczekiwany?
3. Dlaczego wyniku oczekiwanego nie wolno wyznaczać przez ponowne wywołanie sprawdzanej funkcji?
4. Co oznacza `PASS`?
5. Co oznacza `FAIL`?
6. Po co program testowy liczy niepowodzenia?
7. Co oznacza kod zakończenia 0 programu testowego?
8. Co oznacza kod zakończenia 1 w naszym programie testowym?
9. Dlaczego wypisanie `FAIL` i zakończenie programu kodem 0 nie wystarcza?
10. Dlaczego po poprawce funkcji trzeba ponownie uruchomić wszystkie testy, a nie tylko ten, który wcześniej się nie udał?

<details>
<summary>Przykładowe odpowiedzi</summary>

1. `std::cout` tylko wypisuje wynik, a o tym, czy jest dobry, decyduje osoba, która go czyta. Test zawiera wynik oczekiwany, sam porównuje go z wynikiem rzeczywistym i wypisuje werdykt.
2. Ze specyfikacji, czyli z kontraktu funkcji. Liczy się go przed uruchomieniem programu i wpisuje w test jako gotową liczbę.
3. Bo wtedy test porównuje funkcję z nią samą. Oba wyniki są zawsze równe, więc test przechodzi także dla błędnej funkcji i niczego nie sprawdza.
4. Wynik rzeczywisty jest równy oczekiwanemu: dla tego przypadku funkcja działa zgodnie z kontraktem. Nie znaczy to, że funkcja jest poprawna dla wszystkich danych.
5. Wynik rzeczywisty różni się od oczekiwanego. Błąd jest w funkcji albo w samym teście, na przykład w źle policzonym wyniku oczekiwanym. Program tego nie rozstrzyga: trzeba wrócić do kontraktu.
6. Żeby po wszystkich testach wiedzieć, czy któryś się nie udał, i na tej podstawie wybrać kod zakończenia. Licznik daje też podsumowanie, w którym jednym spojrzeniem widać liczbę niepowodzeń.
7. Wszystkie wykonane testy zakończyły się sukcesem.
8. Co najmniej jeden test zakończył się niepowodzeniem. To nie znaczy, że zawiódł program testowy: wykrył on niezgodność ze specyfikacją.
9. Bo `FAIL` czyta tylko człowiek. CLion, skrypt albo automatyczne sprawdzanie odczytują kod zakończenia i przy 0 uznają, że wszystko jest w porządku. Błąd zostałby wtedy niezauważony.
10. Bo poprawka mogła zepsuć coś, co wcześniej działało, na przykład inny przypadek tej samej funkcji. Testy są już napisane, więc ich ponowne uruchomienie nic nie kosztuje.

</details>

## Podsumowanie

- Wypisanie wyniku funkcji to nie test: o tym, czy wynik jest dobry, decyduje wtedy człowiek.
- Test porównuje **wynik rzeczywisty** z **wynikiem oczekiwanym**. Wynik oczekiwany pochodzi ze specyfikacji, nigdy z działania sprawdzanej funkcji.
- `PASS`: wyniki są równe. `FAIL`: różnią się, a linijka podaje nazwę testu i obie wartości.
- Funkcja sprawdzająca wykonuje jeden test i zmienia przez referencję liczniki testów i niepowodzeń w `main`.
- Program testowy kończy się kodem 0, gdy wszystkie testy przeszły, i kodem 1, gdy co najmniej jeden się nie udał. Kod zakończenia odczytuje każdy, kto uruchamia program, bez czytania tekstu.
- Kod 1 programu testowego to wykryta niezgodność z kontraktem, a nie błąd w działaniu programu testowego.
- Wadliwy program testowy nie może wykryć błędu (porównuje funkcję z nią samą) albo go nie zgłasza (kończy się kodem 0 mimo `FAIL`).
- Po każdej zmianie funkcji uruchamiasz te same testy ponownie.

## Co dalej

Trzy testy z punktu 5 wykryły błąd dla 0 godzin. Czy wykryłyby funkcję, która dla 9 godzin zwraca 29, albo taką, która myli się tylko dla 8 godzin? W [lekcji 13.2: Przypadki, które wykrywają błędy](lesson_02_test_cases_that_catch_bugs.md) sprawdzisz, czy wybrane przypadki potrafią wykryć istotne błędy, i nauczysz się je tak dobierać.

---

## Przykładowe rozwiązania

Zajrzyj tutaj **po własnej próbie**. Twoje nazwy mogą się różnić, jeśli każdy test ma nazwę, a standardowe wyjście i kod zakończenia są zgodne z wymaganiami.

<details>
<summary>Punkt 10: misja, koszt wydruku</summary>

**`main.cpp`**, z testami wszystkich przypadków z tabeli wyników oczekiwanych:

<!-- example: print_cost_tests -->
```cpp
#include <iostream>
#include <string>

int print_cost(int pages) {
    if (pages < 0 || pages > 10) {
        return -1;
    }

    if (pages <= 3) {
        return 2 * pages;
    }

    return 6 + (pages - 3);
}

void check_equal(const std::string& name, int expected, int actual, int& tests, int& failed) {
    ++tests;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << expected << ", actual " << actual << "\n";
        ++failed;
    }
}

int main() {
    int tests{0};
    int failed{0};

    check_equal("print_cost(-1)", -1, print_cost(-1), tests, failed);
    check_equal("print_cost(0)", 0, print_cost(0), tests, failed);
    check_equal("print_cost(1)", 2, print_cost(1), tests, failed);
    check_equal("print_cost(3)", 6, print_cost(3), tests, failed);
    check_equal("print_cost(4)", 7, print_cost(4), tests, failed);
    check_equal("print_cost(5)", 8, print_cost(5), tests, failed);
    check_equal("print_cost(10)", 13, print_cost(10), tests, failed);
    check_equal("print_cost(11)", -1, print_cost(11), tests, failed);

    std::cout << "Tests: " << tests << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

<!-- output: print_cost_tests -->
```text
PASS print_cost(-1)
PASS print_cost(0)
PASS print_cost(1)
PASS print_cost(3)
PASS print_cost(4)
PASS print_cost(5)
PASS print_cost(10)
PASS print_cost(11)
Tests: 8, failed: 0
```

Kod zakończenia: 0.

- **Funkcja:** najpierw zakres, potem strony po 2 (do trzeciej włącznie), na końcu 6 za pierwsze trzy strony i po 1 za każdą następną. 0 stron daje `2 * 0`, czyli 0, więc nie wymaga osobnego warunku.
- **Testy:** wyniki oczekiwane to liczby z tabeli, policzone z kontraktu. Żaden nie powstał przez wywołanie `print_cost`.
- **Inne poprawne rozwiązania:** inna kolejność warunków; osobny warunek dla 0 stron; wzór `pages + 3` zamiast `6 + (pages - 3)` dla stron od czwartej. Twój program może mieć tylko cztery wymagane testy: wynik zawiera wtedy cztery linijki `PASS` i `Tests: 4, failed: 0`.

**Celowy błąd:** granica pierwszego przedziału przesunięta o jedną stronę, `pages <= 4` zamiast `pages <= 3`. Czwarta strona kosztuje wtedy 2 zamiast 1. Program testowy się nie zmienia:

<!-- example: print_cost_tests_bug exit=1 -->
```cpp
#include <iostream>
#include <string>

int print_cost(int pages) {
    if (pages < 0 || pages > 10) {
        return -1;
    }

    if (pages <= 4) {
        return 2 * pages;
    }

    return 6 + (pages - 3);
}

void check_equal(const std::string& name, int expected, int actual, int& tests, int& failed) {
    ++tests;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << expected << ", actual " << actual << "\n";
        ++failed;
    }
}

int main() {
    int tests{0};
    int failed{0};

    check_equal("print_cost(-1)", -1, print_cost(-1), tests, failed);
    check_equal("print_cost(0)", 0, print_cost(0), tests, failed);
    check_equal("print_cost(1)", 2, print_cost(1), tests, failed);
    check_equal("print_cost(3)", 6, print_cost(3), tests, failed);
    check_equal("print_cost(4)", 7, print_cost(4), tests, failed);
    check_equal("print_cost(5)", 8, print_cost(5), tests, failed);
    check_equal("print_cost(10)", 13, print_cost(10), tests, failed);
    check_equal("print_cost(11)", -1, print_cost(11), tests, failed);

    std::cout << "Tests: " << tests << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

<!-- output: print_cost_tests_bug -->
```text
PASS print_cost(-1)
PASS print_cost(0)
PASS print_cost(1)
PASS print_cost(3)
FAIL print_cost(4): expected 7, actual 8
PASS print_cost(5)
PASS print_cost(10)
PASS print_cost(11)
Tests: 8, failed: 1
```

Kod zakończenia: 1. To **test wykrywający błąd**: program testowy działa poprawnie, a błąd jest w `print_cost`.

- **Który test i dlaczego:** tylko `print_cost(4)`. Dla 4 stron błędna funkcja liczy `2 * 4`, czyli 8, a kontrakt daje 3 · 2 + 1 = 7.
- **Dlaczego pozostałe przechodzą:** dla 0–3 stron obie wersje wybierają tę samą gałąź. Dla 5 i 10 stron warunek `pages <= 4` jest fałszywy, więc działa ten sam wzór co w poprawnej funkcji.
- **Kod 1:** `failed` wynosi 1, więc `main` zwraca 1.
- **Wniosek na przyszłość:** ten błąd wykrywa tylko test dla 4 stron, czyli dokładnie na granicy między dwiema cenami. Gdyby zabrakło tego testu, wszystkie pozostałe by przeszły. Jak przewidywać takie miejsca, zobaczysz w następnej lekcji.

</details>

**Poprzednia lekcja:** [Lekcja 12.4: Seanse w kinie (sprawdzian Modułu 12)](../module_12_text_files/lesson_04_cinema_screenings.md) · **Następna lekcja:** [Lekcja 13.2: Przypadki, które wykrywają błędy](lesson_02_test_cases_that_catch_bugs.md) · [Opis kursu](../../README.md)

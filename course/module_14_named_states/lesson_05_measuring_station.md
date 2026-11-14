# Lekcja 14.5: Stacja pomiarowa (sprawdzian Modułu 14)

**Polski** · [English](lesson_05_measuring_station.en.md) · [Opis kursu](../../README.md)

> **Moduł 14, lekcja 5: sprawdzian** · około 150–190 minut, w dwóch podejściach
> **Potrzebujesz:** katalogu `cpp-workspace` i oryginalnego projektu `lesson_05_first_program`. Przydadzą się projekt z lekcji 13.4 jako przypomnienie dwóch targetów i misja z lekcji 14.4.
> **Wersja pilotażowa.** Rozwiązanie referencyjne i jego programy testowe sprawdzamy automatycznie na Windowsie, Ubuntu i macOS. Program właściwy jest przy tym budowany, ale automatyczne testy kursu go nie uruchamiają: uruchamiasz go samodzielnie, ręcznie. Twojego projektu nic nie ocenia automatycznie: sprawdzasz go według listy kontrolnej. Kroki w CLionie są takie jak w lekcji 13.4: opisujemy je według dokumentacji CLion 2026.3, bez ręcznego sprawdzenia na każdym systemie.

## Jak przebiega ten sprawdzian

Ta lekcja nie wprowadza nowej składni. Sprawdzasz, czy potrafisz **samodzielnie zaprojektować i przetestować program, który przetwarza ciąg danych**: każdy wynik odczytu ma w nim własną nazwę, błędny wpis nie zatrzymuje dalszej pracy, a testy sprawdzają i nazwane wyniki, i ich skutki. Łączysz w nim lekcje 14.1–14.4 (`enum class`, `switch`, nazwane wyniki z niezmienionymi danymi po odmowie, odczyt, który odzyskuje strumień) z umiejętnościami z Modułu 13: planem przed kodem, wynikami oczekiwanymi z kontraktu, `std::istringstream` i dwoma targetami.

**Najważniejszy warunek:** Twój test musi wykazać usterkę dostarczonego kodu **przed** poprawką. Same `PASS` po poprawce nie wystarczą do zaliczenia: nie wiadomo wtedy, czy test w ogóle potrafi wykryć błąd.

Sprawdzian ma trzy części i omówienie:

- **Część A: plan.** Przypadki i wyniki oczekiwane na podstawie specyfikacji, zanim zobaczysz kod startowy.
- **Część B: projekt i testowanie.** Projekt z dwoma targetami, funkcja `collect_measurements`, program testowy, wykrycie usterki w dostarczonym kodzie, poprawka i te same testy jeszcze raz. To największa część pracy.
- **Część C: zmiana wymagań.** Nowy nazwany wynik, awaria czujnika: najpierw testy nowego kontraktu, które się nie udają, potem zmiana kodu i wszystkie testy jeszcze raz.
- **Sprawdzenie i omówienie:** podpowiedzi, pełna lista przypadków, rozwiązanie referencyjne, wyjaśnienia, odpowiedzi i samoocena. Przejdź tam dopiero po częściach A i B albo wtedy, gdy świadomie zrezygnujesz z dalszej samodzielnej próby.

Zajrzenie do podpowiedzi albo do wcześniejszych lekcji nie jest porażką. Ważne jest, żeby **uczciwie zanotować, co zrobiono samodzielnie, a co z pomocą**. Proponowany podział na dwa podejścia:

- **pierwsze, około 115 minut:** specyfikacja, część A, projekt w CLionie, `collect_measurements`, program testowy, wykrycie usterki i poprawka, czyli uruchomienia 1–3;
- **drugie, około 55 minut:** część C z uruchomieniami 4 i 5, uzasadnienie, lista kontrolna i samoocena.

Typowo zajmuje to razem około 170 minut. Przedział z nagłówka, 150–190 minut, to szacunek, a nie limit: szukanie własnych pomyłek w kodzie i w testach może potrwać dłużej.

**Możesz używać:** CLiona albo terminala, CMake'a i Ninja, jak dotąd; `CMakeLists.txt` z oryginalnego `lesson_05_first_program` i wzoru dwóch targetów z lekcji 13.4; funkcji sprawdzających z lekcji 13.1–13.3 i 14.3 (dostaniesz je w szkielecie programu testowego); `read_number` i `discard_rest_of_line` z lekcji 14.4 (dostaniesz je w kodzie startowym); swojej funkcji `count_ratings` z misji lekcji 14.4 jako punktu wyjścia dla `collect_measurements`; swoich wcześniejszych tabel przypadków. Debugger nie jest potrzebny. Wszystko, czego potrzebujesz, znasz z Modułów 1–14.

Lekcje 13.4 i 14.1–14.4 traktuj jako przypomnienie zasad, a nie jako gotowy program do przepisania. Możesz świadomie przenieść fragmenty kodu, na przykład pętlę z `count_ratings`, ale plan, przypadki, wyniki oczekiwane i sposób wykazania usterki przygotuj samodzielnie. Jeśli adaptujesz wcześniejszy kod, zanotuj w samoocenie, skąd pochodzi, co przeniesiono, co zmieniono i jakie decyzje podjęto samodzielnie.

---

## Specyfikacja: stacja pomiarowa

Stacja pogodowa zbiera pomiary temperatury i na koniec podaje raport: ile pomiarów przyjęła, ile wpisów odrzuciła i jaka była najniższa i najwyższa temperatura. W tym sprawdzianie nie ma prawdziwego czujnika: zastępuje go **symulator**, który przesyła odczyty jako tekst. W testach ten tekst podajesz przez `std::istringstream`, a w programie właściwym wpisujesz go w oknie **Run**. Program nie korzysta ze sprzętu, plików ani sieci.

### Protokół symulatora

- Każdy odczyt to jeden wiersz, który zaczyna się od liczby całkowitej: temperatury w stopniach Celsjusza.
- Symulator może dopisać po liczbie dowolny tekst, na przykład jednostkę: `19 C`.
- Czasem wysyła pusty wiersz. Pusty wiersz nie jest odczytem.
- Dane kończą się, gdy symulator przestaje wysyłać.

Tekst, od którego zaczyna się próba odczytu, aż do końca jego wiersza nazywamy, jak w lekcji 14.4, **wpisem**.

**Polityka prefiksu.** Stacja odczytuje początkowy prefiks liczbowy wpisu. Nie rozpoznaje jednostek ani komentarzy i nie sprawdza całego wiersza: resztę wiersza odrzuca. Dlatego `21 C` daje 21, a `21.5` daje 21 bez zgłoszenia błędu.

| Wpis | Co odczytuje stacja | Wynik |
|---|---|---|
| `21` | 21 | `measured` |
| `21 C` | 21; reszta wiersza zostaje odrzucona | `measured` |
| `21.5` | 21, bez zgłoszenia błędu | `measured` |
| `21 30` | 21; `30` zostaje odrzucone | `measured` |
| `abc` | brak liczby | `invalid_entry` |

To ta sama zasada co w `read_number` z lekcji 14.4. `21.5` nie jest poprawnym zapisem pomiaru całkowitego, a stacja i tak przyjmie 21: to świadoma granica tego programu, a nie ścisłe sprawdzanie wiersza.

### Dwa zakresy

| Zakres | Wartości | Co znaczy liczba spoza niego |
|---|---|---|
| **zakres liczbowy protokołu symulatora** | od −99 do 99 | to nie jest poprawna wiadomość symulatora, tylko błędny wpis: `invalid_entry` |
| **zakres pomiarów przyjmowanych przez stację** | od −50 do 50, obie granice włącznie | to poprawna wiadomość, ale stacja jej nie przyjmuje: `out_of_range` |

Zakres pomiarów leży wewnątrz zakresu protokołu. Liczba 60 jest więc poprawną wiadomością z temperaturą, której stacja nie przyjmuje, a liczba 100 nie jest poprawną wiadomością w ogóle, tak samo jak `abc`.

### Funkcja `read_measurement`

<!-- fragment -->
```cpp
enum class Reading {
    measured,
    out_of_range,
    invalid_entry,
    end_of_data
};

Reading read_measurement(std::istream& input, int& temperature);
```

**Jedno wywołanie to jedna próba odczytu**, jak w `read_number`: funkcja szuka następnego znaku, który nie jest białym znakiem, próbuje od niego odczytać liczbę, a potem zużywa resztę bieżącego wiersza. Puste wiersze i wiersze z samymi białymi znakami nie są próbami. Na przykład `"21\n\nabc\n23"` to trzy próby: 21, `abc` i 23. Czwarte wywołanie daje `end_of_data`.

| Wynik | Kiedy | `temperature` |
|---|---|---|
| `Reading::measured` | liczba leży w zakresie pomiarów stacji | dostaje tę liczbę |
| `Reading::out_of_range` | liczba leży w zakresie protokołu, ale poza zakresem stacji | bez zmian |
| `Reading::invalid_entry` | na początku wpisu nie ma liczby, liczba jest za duża dla `int` albo leży poza zakresem protokołu | bez zmian |
| `Reading::end_of_data` | nie ma kolejnego wpisu | bez zmian |

- **`temperature` zmienia się wyłącznie przy `measured`.** Przy każdym innym wyniku zachowuje wartość sprzed wywołania. Funkcja niczego nie wypisuje.
- **Koniec danych nie jest odmową** i jest trwały: gdy wywołanie dało `end_of_data`, kolejne wywołania na tym samym strumieniu też dają `end_of_data`.
- Jak w lekcji 14.4, kontrakt zakłada sprawne źródło danych: gdyby źródło przestało działać, funkcja przestaje czytać i zwraca `end_of_data` tylko jako sygnał zatrzymania, a wywołujący może to rozpoznać przez `input.bad()`.

### Funkcja `collect_measurements`

<!-- fragment -->
```cpp
struct StationReport {
    int measured;
    int out_of_range;
    int invalid_entries;
    int lowest;
    int highest;
};

StationReport collect_measurements(std::istream& input, int limit);
```

**Kontrakt:**

- **Warunek wstępny:** `limit > 0`. Funkcja tego nie sprawdza.
- Wywołuje `read_measurement`, dopóki nie przyjmie `limit` pomiarów albo dopóki nie skończą się dane.
- **Do limitu liczą się tylko przyjęte pomiary.** Odmowy, `out_of_range` i `invalid_entry`, są liczone we własnych polach i nie zużywają limitu.
- Gdy przyjmie `limit` pomiarów, kończy pracę od razu: **reszta danych zostaje w strumieniu nieprzeczytana**. Kolejne wywołanie `read_measurement` na tym samym strumieniu odczyta następny wpis.
- Gdy dane skończą się wcześniej, zwraca raport z tego, co zdążyła odczytać. Sam koniec danych nie jest liczony.
- Niczego nie wypisuje.

| Pole `StationReport` | Znaczenie |
|---|---|
| `measured` | liczba przyjętych pomiarów |
| `out_of_range` | liczba odmów z powodu zakresu stacji |
| `invalid_entries` | liczba błędnych wpisów |
| `lowest`, `highest` | najniższy i najwyższy przyjęty pomiar; mają znaczenie tylko wtedy, gdy `measured > 0` |

**Raport bez pomiarów.** Gdy funkcja nie przyjęła żadnego pomiaru, czy to przy całkowicie pustym strumieniu, czy przy wpisach, z których żaden nie został przyjęty, `measured` wynosi 0, a `lowest` i `highest` też wynoszą 0. Te zera to **wartości zastępcze, a nie pomiary**: o tym, czy raport zawiera pomiary, decyduje `measured`. Prawdziwe 0 °C jest za to zwykłym pomiarem, bo 0 leży w zakresie stacji. Raport nie zawiera sumy ani średniej.

### Program właściwy

`main.cpp` dostaniesz gotowy w części B. Program wywołuje `collect_measurements` dla `std::cin` z limitem 6, czyli zbiera sześć pomiarów, i wypisuje raport. Dla takich danych, wpisanych w kolejnych wierszach (czwarty wiersz jest pusty):

```text
21
60
abc

18
25
19 C
0
-5
7
```

wypisuje:

```text
Measurements: 6 of 6
Lowest: -5
Highest: 25
Out of range: 1
Invalid entries: 1
```

Szósty przyjęty pomiar to `-5`, więc program kończy pracę po tym wierszu: `7` zostaje nieprzeczytane i nie trafia do raportu. Gdy nie przyjęto żadnego pomiaru, program zamiast `Lowest` i `Highest` wypisuje `No measurements`. W każdym przypadku kończy się kodem 0: odrzucanie błędnych wpisów to poprawne działanie stacji.

To **uruchomienie ręczne**: automatyczne testy kursu budują program właściwy, ale go nie uruchamiają. Zgodność z tym przykładem sprawdzasz samodzielnie.

### Wymagana struktura

```text
measuring_station/
├── CMakeLists.txt
├── main.cpp
├── function_tests.cpp
├── rules.cpp
└── rules.hpp
```

- **`rules.hpp`:** wszystkie typy i deklaracje, z `#pragma once`. Dostaniesz go gotowy.
- **`rules.cpp`:** jedyne definicje czterech funkcji: `discard_rest_of_line`, `read_number` i `read_measurement` dostaniesz gotowe, a `collect_measurements` napiszesz samodzielnie.
- **`main.cpp`:** program właściwy. Dostaniesz go gotowy; dołącza `rules.hpp`.
- **`function_tests.cpp`:** program testowy. Dostaniesz szkielet z funkcjami sprawdzającymi i dwoma przypadkami jako wzorem, a pozostałe przypadki z planu dopiszesz. Dołącza `rules.hpp`, nie zawiera definicji żadnej z czterech funkcji i nie odczytuje niczego ze `std::cin`.
- **`CMakeLists.txt`:** dwa targety, `first_program` i `function_tests`, oba z `rules.cpp`, w postaci z lekcji 13.4. Nic więcej.
- **Każde wywołanie `read_measurement`** w testach sprawdza wynik i `temperature`. **Każdy scenariusz `collect_measurements`** sprawdza każde pole raportu osobno, z własną etykietą. Program testowy wypisuje `PASS` albo `FAIL` z wynikiem oczekiwanym i rzeczywistym, podsumowanie `Checks: N, failed: F` i kończy się kodem 0 albo 1, zależnie od niepowodzeń.

**Zdecyduj samodzielnie:**

1. które przypadki sprawdzisz i którą regułę rozstrzyga każdy z nich;
2. jakich wyników i jakich raportów oczekujesz;
3. od jakiej wartości zacznie `temperature`, żeby każda zmiana była widoczna;
4. jak pokażesz, że po osiągnięciu limitu reszta danych została w strumieniu;
5. jak napiszesz `collect_measurements`;
6. jak wykażesz usterkę przed poprawką i jak potwierdzisz, że poprawka niczego nie zepsuła.

Przypomnienie znajdziesz w lekcjach [13.4](../module_13_testing_functions/lesson_04_tests_next_to_the_program.md) (dwa targety, wspólny `rules.cpp`), [14.2](lesson_02_handling_every_state_with_switch.md) (`switch` z etykietą dla każdej wartości), [14.3](lesson_03_function_explains_refusal.md) (nazwany wynik, dane bez zmian po odmowie, pierwszeństwo odmowy) i [14.4](lesson_04_reading_that_recovers_the_stream.md) (`read_number`, koniec danych, testy sekwencji na jednym strumieniu).

---

# Część A: plan

Zanim zobaczysz kod startowy i zanim napiszesz jakikolwiek test, przygotuj na piśmie plan. Składa się z dwóch tabel. Lista samych nazw nie wystarczy: każdy wiersz podaje dane, oczekiwany wynik i powód wyboru.

**Przypadki bezpośrednie** wywołują `read_measurement` raz, na własnym strumieniu. `temperature` zaczyna każdy przypadek od 777: takiej wartości nie da żaden przypadek, więc każda zmiana będzie widoczna.

| Przypadek | Wpis | Wynik | `temperature` po wywołaniu | Dlaczego |
|---|---|---|---:|---|
| D1 | `"21.5"` | `measured` | 21 | polityka prefiksu: odczytany prefiks to 21 |

**Scenariusze** wywołują `collect_measurements` na własnym strumieniu. Oczekiwany raport zapisz od razu w postaci `{measured, out_of_range, invalid_entries, lowest, highest}`: w części B wkleisz go do testu jako `StationReport{…}`.

| Przypadek | Tekst strumienia | `limit` | Raport | Dodatkowo | Dlaczego |
|---|---|---:|---|---|---|
| C1 | `"21\n18\n25\n30\n"` | 3 | `{3, 0, 0, 18, 25}` | następne wywołanie `read_measurement`: `measured`, 30 | limit osiągnięty, reszta danych nieprzeczytana; same dodatnie pomiary |

Plan ma **12 przypadków bezpośrednich** (z D1) i **8 scenariuszy** (z C1). Pozostałe wiersze wyprowadź samodzielnie ze specyfikacji.

**Przypadki bezpośrednie muszą obejmować:**

- obie granice zakresu stacji, każdą z obu stron;
- obie granice zakresu protokołu, każdą z obu stron;
- wpis bez liczby na początku;
- prawdziwe 0;
- brak danych.

**Każda reguła osobno.** Wynik zależy od trzech reguł: czy na początku wpisu jest liczba, czy leży w zakresie protokołu i czy leży w zakresie stacji. Każdą z nich sprawdza para przypadków, które różnią się tylko tą regułą:

| Reguła | Liczba w środku | Liczba tuż za granicą |
|---|---:|---:|
| dolna granica zakresu stacji | −50 | −51 |
| górna granica zakresu stacji | 50 | 51 |
| górna granica zakresu protokołu | 99 | 100 |
| dolna granica zakresu protokołu | −99 | −100 |

Reguła „na początku wpisu jest liczba” potrzebuje jeszcze wpisu bez liczby, na przykład `abc`. Wyniki tych przypadków wyprowadź z tabeli wyników. Przypadek, który łamie kilka reguł naraz, nie zastępuje pary: gdyby funkcja pomijała jedną z reguł, wynik i tak mogłaby ustalić inna, a usterka pozostałaby ukryta.

**Scenariusze muszą obejmować:**

- całkowicie pusty strumień;
- wpisy, z których żaden nie zostaje przyjęty, w tym liczbę za dużą dla `int`;
- zero jako pierwszy przyjęty pomiar;
- ostatni poprawny wpis bez znaku końca wiersza;
- ostatni błędny wpis bez znaku końca wiersza;
- pusty wiersz i tekst po liczbie;
- dwa błędne wpisy z rzędu;
- odmowy każdego rodzaju, po których następuje poprawny pomiar;
- odmowy, zanim limit zostanie osiągnięty, i reszta danych nieprzeczytana po osiągnięciu limitu, sprawdzona następnym wywołaniem;
- scenariusz z samymi ujemnymi pomiarami i scenariusz z samymi dodatnimi, żeby `lowest` i `highest` nie dało się pomylić z 0;
- koniec danych, zanim limit zostanie osiągnięty.

Jeden scenariusz może obejmować kilka z tych punktów.

**Odpowiedz w planie na cztery pytania:**

1. Jakie są oba zakresy i co oznacza liczba spoza każdego z nich?
2. Co liczy limit, a czego nie liczy, i co dzieje się z danymi po jego osiągnięciu?
3. Jak wygląda raport dla pustego strumienia, a jak dla wpisów bez przyjętego pomiaru? Czym różnią się od raportu z prawdziwym 0?
4. Jak sprawdzisz, że oba programy korzystają z tej samej implementacji?

Plan jest obowiązkową częścią sprawdzianu i jest oceniany razem z programem testowym. Kod startowy otwórz dopiero wtedy, gdy plan będzie gotowy.

---

# Część B: projekt i testowanie

W `cpp-workspace` utwórz katalog `measuring_station` i skopiuj do niego `CMakeLists.txt` z oryginalnego `lesson_05_first_program`. Utwórz obok cztery pozostałe pliki z wymaganej struktury, tak jak w lekcji 13.4, i otwórz katalog w CLionie.

## Kod startowy

<details>
<summary>Kod startowy: otwórz po przygotowaniu planu z części A</summary>

**`rules.hpp`**:

<!-- fragment -->
```cpp
#pragma once

#include <istream>

enum class ReadResult {
    accepted,
    out_of_range,
    invalid_input,
    end_of_input
};

void discard_rest_of_line(std::istream& input);
ReadResult read_number(std::istream& input, int minimum, int maximum, int& result);

enum class Reading {
    measured,
    out_of_range,
    invalid_entry,
    end_of_data
};

Reading read_measurement(std::istream& input, int& temperature);

struct StationReport {
    int measured;
    int out_of_range;
    int invalid_entries;
    int lowest;
    int highest;
};

StationReport collect_measurements(std::istream& input, int limit);
```

**`rules.cpp`**:

<!-- fragment -->
```cpp
#include "rules.hpp"

#include <limits>

void discard_rest_of_line(std::istream& input) {
    input.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
}

ReadResult read_number(std::istream& input, int minimum, int maximum, int& result) {
    if (input.bad()) {
        return ReadResult::end_of_input;
    }

    input >> std::ws;

    if (input.eof()) {
        return ReadResult::end_of_input;
    }

    int value{0};
    input >> value;

    if (input.fail()) {
        if (input.bad()) {
            return ReadResult::end_of_input;
        }

        input.clear();
        discard_rest_of_line(input);
        return ReadResult::invalid_input;
    }

    discard_rest_of_line(input);

    if (value < minimum || value > maximum) {
        return ReadResult::out_of_range;
    }

    result = value;
    return ReadResult::accepted;
}

Reading read_measurement(std::istream& input, int& temperature) {
    int value{0};
    const ReadResult result{read_number(input, -99, 99, value)};

    switch (result) {
        case ReadResult::accepted:
            break;
        case ReadResult::out_of_range:
            return Reading::out_of_range;
        case ReadResult::invalid_input:
            return Reading::invalid_entry;
        case ReadResult::end_of_input:
            return Reading::end_of_data;
    }

    if (value < -50 || value > 50) {
        return Reading::out_of_range;
    }

    temperature = value;
    return Reading::measured;
}
```

`discard_rest_of_line` i `read_number` są dokładnie takie jak w lekcji 14.4. `read_measurement` odczytuje liczbę przez `read_number` z zakresem protokołu, od −99 do 99, a zakres stacji sprawdza sama. W tym pliku, pod `read_measurement`, dopiszesz `collect_measurements` według kontraktu.

**Ta implementacja kompiluje się poprawnie, ale zawiera jedną nieujawnioną usterkę logiczną.** Nie szukaj jej czytaniem kodu: znajdź ją swoim testem.

**`main.cpp`**:

<!-- fragment -->
```cpp
#include <iostream>

#include "rules.hpp"

int main() {
    const int limit{6};
    const StationReport report{collect_measurements(std::cin, limit)};

    std::cout << "Measurements: " << report.measured << " of " << limit << "\n";

    if (report.measured > 0) {
        std::cout << "Lowest: " << report.lowest << "\n";
        std::cout << "Highest: " << report.highest << "\n";
    } else {
        std::cout << "No measurements\n";
    }

    std::cout << "Out of range: " << report.out_of_range << "\n";
    std::cout << "Invalid entries: " << report.invalid_entries << "\n";
}
```

**`function_tests.cpp`**, szkielet:

<!-- fragment -->
```cpp
#include <iostream>
#include <sstream>
#include <string>

#include "rules.hpp"

std::string reading_text(Reading reading) {
    switch (reading) {
        case Reading::measured:
            return "measured";
        case Reading::out_of_range:
            return "out_of_range";
        case Reading::invalid_entry:
            return "invalid_entry";
        case Reading::end_of_data:
            return "end_of_data";
    }

    return "unknown";
}

void check_reading(const std::string& name, Reading expected, Reading actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << reading_text(expected) << ", actual " << reading_text(actual) << "\n";
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

void check_report(const std::string& name, const StationReport& expected, const StationReport& actual, int& checks, int& failed) {
    check_int(name + " measured", expected.measured, actual.measured, checks, failed);
    check_int(name + " out_of_range", expected.out_of_range, actual.out_of_range, checks, failed);
    check_int(name + " invalid_entries", expected.invalid_entries, actual.invalid_entries, checks, failed);
    check_int(name + " lowest", expected.lowest, actual.lowest, checks, failed);
    check_int(name + " highest", expected.highest, actual.highest, checks, failed);
}

int main() {
    int checks{0};
    int failed{0};

    std::istringstream input_d1{"21.5"};
    int temperature_d1{777};
    check_reading("D1 result", Reading::measured, read_measurement(input_d1, temperature_d1), checks, failed);
    check_int("D1 temperature", 21, temperature_d1, checks, failed);

    std::istringstream input_c1{"21\n18\n25\n30\n"};
    const StationReport report_c1{collect_measurements(input_c1, 3)};
    check_report("C1", StationReport{3, 0, 0, 18, 25}, report_c1, checks, failed);
    int next_c1{777};
    check_reading("C1 next result", Reading::measured, read_measurement(input_c1, next_c1), checks, failed);
    check_int("C1 next temperature", 30, next_c1, checks, failed);

    std::cout << "Checks: " << checks << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }
}
```

Szkielet ma funkcje sprawdzające i dwa przypadki z planu, D1 i C1, jako wzór:

- `reading_text` zamienia wynik na tekst do linijki `FAIL`, a `check_reading` porównuje wynik oczekiwany z rzeczywistym, jak w lekcji 14.3;
- `check_report` sprawdza każde pole raportu osobno: z `"C1"` powstają etykiety `C1 measured`, `C1 out_of_range`, `C1 invalid_entries`, `C1 lowest` i `C1 highest`;
- w C1 po `collect_measurements` następuje jeszcze jedno wywołanie `read_measurement` **na tym samym strumieniu**: sprawdza, że reszta danych została nieprzeczytana.

Pozostałe przypadki z planu dopisz przed linijką z podsumowaniem, w tej samej postaci.

**Dopóki nie napiszesz `collect_measurements`, projekt się nie zbuduje:** oba programy wywołują tę funkcję, a linker nie znajdzie jej definicji.

</details>

## Kolejność pracy

1. **Pliki.** Skopiuj kod startowy do swoich plików. W `rules.cpp`, pod `read_measurement`, napisz `collect_measurements` według kontraktu. **Nie zmieniaj `read_measurement`.**
2. **Program testowy.** Dopisz do szkieletu `function_tests.cpp` wszystkie przypadki ze swojego planu, z wynikami oczekiwanymi z planu.
3. **Dwa targety.** Zmień `CMakeLists.txt` tak, jak w lekcji 13.4. CMake szuka wszystkich plików z obu list już przy wczytywaniu projektu, dlatego pliki muszą istnieć wcześniej. Wczytaj projekt ponownie i wybierz **Build | Build Project**.
4. **To pierwsze obowiązkowe uruchomienie:** uruchom `first_program` i wpisz w oknie **Run** dane z przykładu w specyfikacji, każdy wiersz zakończony Enterem; pusty wiersz to sam Enter. Po wierszu `-5` program sam kończy pracę i wypisuje raport: na `7` już nie czeka. Porównaj raport ze specyfikacją.
5. **To drugie obowiązkowe uruchomienie:** uruchom `function_tests`. Przy dostarczonym kodzie co najmniej jedno sprawdzenie powinno dać `FAIL`, a program testowy powinien zakończyć się kodem 1. Zapisz linijki `FAIL`, z wynikami oczekiwanymi i rzeczywistymi, i kod zakończenia. To jest dowód, że Twój test wykrywa usterkę.
6. Jeśli wszystkie sprawdzenia dały `PASS`, Twój zestaw nie wykrywa usterki. Najpierw sprawdź, czy Twoja `collect_measurements` przechodzi swoje scenariusze. Potem wróć do planu i do tabeli par: czy każda reguła ma przypadek, który rozstrzyga ją samodzielnie? Uzupełnij plan i testy i uruchom je jeszcze raz. Nie zmieniaj jeszcze `read_measurement`.
7. **Znajdź przyczynę.** Na podstawie linijek `FAIL` i kontraktu wskaż w `read_measurement` miejsce, które działa inaczej, niż mówi specyfikacja. Zapisz, czy błąd jest w funkcji, czy w wyniku oczekiwanym, i skąd to wiesz.
8. **Popraw tylko przyczynę w `read_measurement`.** Nie zmieniaj danych testowych, wyników oczekiwanych, `main.cpp`, `CMakeLists.txt` ani `collect_measurements`.
9. **To trzecie obowiązkowe uruchomienie:** wybierz **Build Project** i uruchom `function_tests` jeszcze raz. Wszystkie sprawdzenia powinny dać `PASS`, a kod zakończenia powinien wynosić 0. Samo ponowne zbudowanie bez uruchomienia testów nie potwierdza poprawki.

Linijki `FAIL` z Twojej własnej `collect_measurements` poprawiasz w `collect_measurements`, jeszcze przed krokiem 5, jeśli wynik oczekiwany zgadza się z kontraktem. Takie dodatkowe uruchomienia nie liczą się do pięciu obowiązkowych.

---

# Część C: zmiana wymagań

Wykonaj tę część **po części B**, najlepiej w drugim podejściu.

**Nowe wymaganie.** Symulator zgłasza teraz awarię czujnika liczbą **−99**. To **kod awarii**, zarezerwowany w protokole: nie jest temperaturą. Stacja ma go rozpoznawać jako nowy nazwany wynik.

| Liczba | Znaczenie | Wynik |
|---|---|---|
| −99 | kod awarii czujnika | `Reading::sensor_fault` |

- `Reading` dostaje wartość `sensor_fault`, przed `end_of_data`, a `StationReport` dostaje pole `sensor_faults`, jako ostatnie:

<!-- fragment -->
```cpp
enum class Reading {
    measured,
    out_of_range,
    invalid_entry,
    sensor_fault,
    end_of_data
};

struct StationReport {
    int measured;
    int out_of_range;
    int invalid_entries;
    int lowest;
    int highest;
    int sensor_faults;
};
```

- `read_measurement` dla −99 zwraca `sensor_fault`. `temperature` się nie zmienia.
- `collect_measurements` liczy awarie w `sensor_faults`. Awaria nie jest pomiarem: nie zwiększa `measured`, nie zmienia `lowest` ani `highest` i nie zużywa limitu.
- Program właściwy wypisuje na końcu raportu linijkę `Sensor faults: ` z liczbą awarii.
- `ReadResult`, `read_number` i oba zakresy zostają bez zmian. −100 nadal jest błędnym wpisem, a −98 nadal odmową z powodu zakresu stacji.

**Pierwszeństwo.** −99 leży też poza zakresem stacji, więc do tej liczby pasują dwie reguły. Kontrakt ustala, która decyduje, jak pierwszeństwo odmowy w lekcji 14.3: **kod awarii sprawdzasz przed zakresem stacji.**

**Kolejność pracy:**

1. **Mapa zmian.** Zanim zmienisz kod, zapisz, w których miejscach projektu pojawia się `Reading` albo `StationReport` i co się w każdym z nich zmieni. Zapisz też, które dawne oczekiwania zmienia nowa reguła i dlaczego tylko te.
2. **Typy.** W `rules.hpp` dodaj `sensor_fault` i `sensor_faults`.
3. **Etykiety.** W `switch` w `collect_measurements` dodaj etykietę `sensor_fault`, która zwiększa `sensor_faults`, a w `reading_text` etykietę, która zwraca `"sensor_fault"`. Pole `sensor_faults` zaczyna od 0, jak pozostałe.
4. **Testy nowego kontraktu.**
   - `check_report` ma sprawdzać także `sensor_faults`, z etykietą jak pozostałe pola.
   - **Każdy** oczekiwany `StationReport{…}` uzupełnij o jawną szóstą wartość, także w dawnych scenariuszach, w których wynosi 0.
   - Nowa reguła zmienia oczekiwania tylko tam, gdzie pojawia się wpis `-99`. Jeśli Twój plan ma go tylko w jednym przypadku bezpośrednim, to jedyne dawne oczekiwanie, które zmieniasz. Zapisz powód każdej takiej zmiany.
   - Dodaj przypadek bezpośredni z wpisem `-98`, sąsiadem kodu awarii, którego nowa reguła nie dotyczy.
   - Dodaj scenariusz, w którym awaria stoi między pomiarami, a limit zostaje osiągnięty: sprawdź raport i następne wywołanie na tym samym strumieniu.
   - Dodaj scenariusz z samymi awariami.
5. **To czwarte obowiązkowe uruchomienie:** zbuduj projekt i uruchom `function_tests`. `read_measurement` jeszcze nie rozpoznaje −99, więc sprawdzenia, które opisują awarię, powinny dać `FAIL`, a kod zakończenia powinien wynosić 1. Zapisz linijki `FAIL`. Ten `FAIL` jest oczekiwany: testy opisują już nowy kontrakt, a funkcja jeszcze nie.
6. **Zmiana funkcji.** W `read_measurement` dodaj sprawdzenie kodu awarii, przed sprawdzeniem zakresu stacji. W `main.cpp` dopisz linijkę `Sensor faults`.
7. **To piąte obowiązkowe uruchomienie:** uruchom `function_tests`. Wszystkie sprawdzenia, dawne i nowe, powinny dać `PASS`, a kod zakończenia powinien wynosić 0. Jeśli chcesz, uruchom też `first_program` z danymi, w których jest `-99`.

**Jawna szósta wartość jest obowiązkowa.** Kompilator jej nie wymusi: z ustawieniami projektu z lekcji 0.5 zapis `StationReport{3, 0, 0, 18, 25}` dla struktury z sześcioma polami kompiluje się bez ostrzeżenia, a brakujące pole dostaje po cichu 0. Test wyglądałby na kompletny, choć o awariach nie mówiłby nic. Ostrzeżenie `-Wswitch` z lekcji 14.2 może wskazać `switch` bez etykiety `sensor_fault`, ale o poprawności decydują testy, a nie ostrzeżenia.

## Gdy coś pójdzie inaczej

| Co widzisz | Co to znaczy | Co zrobić |
|---|---|---|
| Błąd linkera z `collect_measurements`, na przykład `undefined reference` albo `undefined symbol` | Funkcja jest zadeklarowana w `rules.hpp`, ale nie ma jeszcze jej definicji w `rules.cpp`. | Napisz `collect_measurements` w `rules.cpp`, pod `read_measurement`. |
| Program testowy się nie kończy | Pętla w `collect_measurements` nie dostaje `end_of_data`: koniec danych nie kończy pętli albo odzyskiwanie strumienia jest zepsute i każda próba trafia na ten sam tekst. | Zatrzymaj program przyciskiem **Stop**. Sprawdź, co Twoja pętla robi przy `end_of_data`, i porównaj `read_number` z lekcją 14.4. |
| Na dostarczonym kodzie wszystkie sprawdzenia dają `PASS` | Któraś reguła nie ma przypadku, który rozstrzyga ją samodzielnie. | Wróć do tabeli par z części A i do podpowiedzi 3. |
| `lowest` wynosi 0, choć wszystkie pomiary są dodatnie | `lowest` i `highest` zaczynają od 0, zamiast od pierwszego przyjętego pomiaru. | Pierwszy przyjęty pomiar ustawia oba pola. |
| Po zerze jako pierwszym pomiarze `lowest` albo `highest` jest złe | 0 w `lowest` jest traktowane jako „jeszcze nic nie przyjęto”. | O tym, czy coś przyjęto, decyduje `measured`, a nie wartość w `lowest`. |
| Scenariusz z odmowami przed limitem daje za mało pomiarów | Limit liczy wszystkie próby, a nie przyjęte pomiary. | Do limitu liczą się tylko `measured`. |
| W części C awaria jest liczona w `out_of_range` | Sprawdzenie zakresu stacji stoi przed sprawdzeniem kodu awarii. | Ustaw sprawdzenia w kolejności pierwszeństwa. |
| W części C stary scenariusz przechodzi, choć nie sprawdza awarii | Oczekiwany `StationReport{…}` ma pięć wartości, a szóste pole dostało po cichu 0. | Dopisz jawną szóstą wartość w każdym oczekiwanym raporcie. |
| `21.5` jest przyjęte jako 21 | Tak działa polityka prefiksu. | To zamierzone. |
| Ostrzeżenie z `enumeration value 'sensor_fault' not handled in switch` | W `switch` brakuje etykiety dla nowej wartości (lekcja 14.2). | Dopisz etykietę i sprawdź jej skutek w testach. |

## Uzasadnienie

Odpowiedz własnymi słowami, odnosząc się do swojego projektu:

1. Dlaczego wyniki oczekiwane wynikają z kontraktu, a nie z działania programu?
2. Dlaczego para 99 i 100 rozstrzyga regułę zakresu protokołu? Czy wystarczyłby przypadek `abc`?
3. Co pokazała Twoja linijka `FAIL` przed poprawką, a czego nie rozstrzyga?
4. Dlaczego zero w pustym raporcie nie jest pomiarem i jak to sprawdzają Twoje testy?
5. Dlaczego limit liczy tylko przyjęte pomiary i który przypadek to sprawdza?
6. Dlaczego po poprawce w części B nie zmieniasz żadnego oczekiwania, a w części C jedno zmieniasz?
7. Dlaczego kod awarii sprawdzasz przed zakresem stacji? Który przypadek to wykrywa?
8. Dlaczego oba targety korzystają z `rules.cpp` i dlaczego po każdej zmianie uruchamiasz wszystkie testy?

---

## Lista kontrolna przed oddaniem

Sprawdzian jest zaliczony, gdy spełniasz **wszystkie** punkty tej listy. Twoje nazwy przypadków, zmiennych i sprawdzeń oraz kolejność przypadków mogą być inne niż w rozwiązaniu referencyjnym, jeśli spełniają specyfikację. Poprawny raport programu właściwego, samo zbudowanie projektu ani same `PASS` po poprawce nie wystarczą.

- [ ] 1. Plan z części A powstał przed otwarciem kodu startowego: 12 przypadków bezpośrednich (wpis, wynik, `temperature` po wywołaniu) i 8 scenariuszy (tekst, `limit`, raport w postaci `{…}`), każdy z uzasadnieniem.
- [ ] 2. Wszystkie wartości oczekiwane wynikają z kontraktu; żadna nie pochodzi z uruchomienia programu.
- [ ] 3. Każda reguła ma parę, która rozstrzyga ją samodzielnie: −50 i −51, 50 i 51, 99 i 100, −99 i −100, a do tego wpis bez liczby, na przykład `abc`.
- [ ] 4. Projekt ma pięć plików i dziesięciolinijkowy `CMakeLists.txt` z `first_program` i `function_tests`; `rules.cpp` stoi na obu listach.
- [ ] 5. Cztery funkcje są zdefiniowane tylko w `rules.cpp`; `main.cpp` i `function_tests.cpp` dołączają `rules.hpp`.
- [ ] 6. Każdy przypadek ma własny `std::istringstream`; dodatkowe wywołanie po osiągnięciu limitu korzysta z tego samego strumienia co scenariusz.
- [ ] 7. Każde wywołanie `read_measurement` sprawdza wynik i `temperature`, a `temperature` zaczyna od wartości, której nie daje żaden przypadek.
- [ ] 8. Każdy scenariusz sprawdza `check_report`: osobne sprawdzenie i osobna etykieta dla każdego pola raportu.
- [ ] 9. Przypadki obejmują `21.5`, prawdziwe 0, brak danych, całkowicie pusty strumień, wpisy bez przyjętego pomiaru, zero jako pierwszy pomiar, ostatni poprawny i ostatni błędny wpis bez znaku końca wiersza, pusty wiersz, tekst po liczbie, odmowy przed osiągnięciem limitu i limit osiągnięty z resztą danych nieprzeczytaną, a do tego pozostałe rodzaje z części A: każdy punkt list „Przypadki bezpośrednie muszą obejmować” i „Scenariusze muszą obejmować”.
- [ ] 10. `collect_measurements` liczy do limitu tylko przyjęte pomiary, ustawia `lowest` i `highest` od pierwszego przyjętego pomiaru, a przy odmowie zmienia tylko odpowiedni licznik.
- [ ] 11. `first_program` został uruchomiony ręcznie z danymi z przykładu w specyfikacji i wypisał raport ze specyfikacji.
- [ ] 12. Na dostarczonym kodzie `function_tests` dał `FAIL` i zakończył się kodem 1. Zapisane są linijki `FAIL`, kod zakończenia i przyczyna w `read_measurement`.
- [ ] 13. Poprawka zmieniła tylko przyczynę w `read_measurement`; te same testy z tymi samymi oczekiwaniami dały same `PASS` i kod 0.
- [ ] 14. Część C: `sensor_fault`, `sensor_faults` i etykiety w `collect_measurements` i w `reading_text` są dodane; każdy oczekiwany `StationReport{…}` ma jawną szóstą wartość; `check_report` sprawdza `sensor_faults`; są nowe przypadki: `-98`, awaria wśród pomiarów z osiągniętym limitem i same awarie.
- [ ] 15. Część C: przed sprawdzeniem kodu awarii uruchomienie 4 dało `FAIL` i kod 1. Ze sprawdzeniem ustawionym przed zakresem stacji uruchomienie 5 dało same `PASS` i kod 0. Zmienione dawne oczekiwania dotyczą tylko wpisu `-99`, a powód zmiany jest zapisany.
- [ ] 16. Osiem pytań z uzasadnienia ma odpowiedzi, które odnoszą się do Twojego projektu, a samoocena jest wypełniona, z zapisanym adaptowanym kodem.

Gdy skończysz, możesz zapisać projekt `measuring_station` w Gicie, jak w lekcji 1.5: pięć plików, bez katalogu budowania.

## Kryteria oceny

Rubryka służy do samooceny albo do oceny przez prowadzącego. Kurs nie ma skali ocen ani progu punktowego: punkty pokazują, które obszary są opanowane, a które wymagają powtórki. O zaliczeniu decyduje lista kontrolna powyżej, a nie liczba punktów.

| Obszar | Punkty | Pełne punkty, gdy |
|---|---:|---|
| Plan i kontrakt (część A) | 10 | punkty 1 i 2 listy kontrolnej; odpowiedzi na pytania planu są poprawne |
| Dobór przypadków i wyniki oczekiwane | 15 | punkty 3 i 9; każda granica jest sprawdzona z obu stron |
| Nazwane wyniki, odzyskiwanie i koniec danych | 15 | wynik każdego wywołania jest sprawdzony; ostatni poprawny i ostatni błędny wpis bez znaku końca wiersza są obsłużone poprawnie; pusty wiersz nie jest próbą; `end_of_data` kończy pętlę i nie jest liczony |
| Raport, limit i dane bez zmian | 15 | punkt 10; oba przypadki raportu bez pomiarów i prawdziwe 0 są sprawdzone; reszta danych po limicie jest sprawdzona; `temperature` bez zmian po każdej odmowie i awarii jest sprawdzona |
| Dwa targety i jedna implementacja | 10 | punkty 4, 5 i 11 |
| Usterka: `FAIL`, przyczyna, poprawka, te same testy | 15 | punkty 12 i 13 |
| Część C: zmiana kontraktu i regresja | 15 | punkty 14 i 15 |
| Uzasadnienie i samoocena | 5 | punkt 16 |
| **Razem** | **100** | |

Pełnych punktów w danym obszarze nie daje:

- **nazwane wyniki:** zgubiona ostatnia wartość bez znaku końca wiersza albo koniec danych liczony jako odmowa;
- **dwa targety:** funkcja skopiowana poza `rules.cpp`, nawet gdy oba targety są zdefiniowane;
- **raport:** zmiana `temperature` albo raportu po odmowie, której nic nie wykrywa;
- **usterka:** brak `FAIL` przed poprawką, `FAIL` przy kodzie zakończenia 0 albo oczekiwanie zmienione w części B;
- **część C:** oczekiwanie zmienione poza przypadkami z `-99` i nowym polem albo rozwiązanie oparte na ostrzeżeniu kompilatora zamiast na testach.

**Inne nazwy** zmiennych, przypadków, sprawdzeń i funkcji pomocniczych nie odbierają punktów. Nazwy targetów, plików, typów i funkcji z kontraktu są jednak stałe: wynikają ze specyfikacji.

**Co sprawdza automat, a co nie.** Testy kursu sprawdzają, że rozwiązanie referencyjne się buduje, w każdym wariancie z obu targetów, i że jego programy testowe dają pokazane wyniki i kody zakończenia. Program właściwy jest budowany, ale nie uruchamiany: jego raport ze specyfikacji sprawdzasz ręcznie. **Twojego projektu, planu, testów i uzasadnienia nie sprawdza żaden automat:** ocenia je człowiek, czytając plan i kod oraz porównując Twoje uruchomienia z listą kontrolną.

---

# Sprawdzenie i omówienie

Przejdź tutaj **dopiero po częściach A i B** albo wtedy, gdy świadomie zrezygnujesz z dalszej samodzielnej próby. Dalej jest kod rozwiązania.

## Podpowiedzi

<details>
<summary>Podpowiedź 1: tabela wyników</summary>

Która reguła daje który z czterech wyników? Które dwie liczby leżą poza zakresem stacji, a różnią się tylko tym, czy mieszczą się w zakresie protokołu? Która para pokazuje każdą granicę z obu stron? Wynik każdego przypadku zapisz, zanim uruchomisz cokolwiek.

</details>

<details>
<summary>Podpowiedź 2: raport i limit</summary>

Które wywołanie ustawia `lowest` i `highest` po raz pierwszy? Co liczy się do limitu, a co nie? Jak pokażesz, że dane po osiągnięciu limitu nadal są w strumieniu: które wywołanie i na którym strumieniu to sprawdzi?

</details>

<details>
<summary>Podpowiedź 3: gdy na dostarczonym kodzie wszystko przechodzi</summary>

Czy któraś reguła ze specyfikacji nie jest rozstrzygana samodzielnie przez żaden Twój przypadek? Porównaj swoje przypadki z tabelą par z części A: przy każdej parze zapisz, jaki wynik daje każda z dwóch liczb i dlaczego. Najpierw uzupełnij plan, potem testy.

</details>

<details>
<summary>Podpowiedź 4: kolejność w części C</summary>

Najpierw wartość, pole i etykiety, potem testy: powinny się nie udać. Dopiero potem sprawdzenie w `read_measurement`. Które sprawdzenie musi stać pierwsze dla −99? Które dawne oczekiwania zmienia nowa reguła i dlaczego tylko te?

</details>

## Pełna lista przypadków kontrolnych

<details>
<summary>Przypadki D1–D13 i C1–C10, wyniki z kontraktu</summary>

**Przypadki bezpośrednie.** Każdy ma własny strumień, a `temperature` zaczyna od 777. D13 i zmieniony wynik D8 należą do części C.

| Przypadek | Wpis | Wynik | `temperature` po wywołaniu | Co rozstrzyga |
|---|---|---|---:|---|
| D1 | `"21.5"` | `measured` | 21 | polityka prefiksu, zwykły pomiar |
| D2 | `"-50"` | `measured` | −50 | dolna granica stacji, w środku |
| D3 | `"-51"` | `out_of_range` | 777 | dolna granica stacji, tuż za nią |
| D4 | `"50"` | `measured` | 50 | górna granica stacji, w środku |
| D5 | `"51"` | `out_of_range` | 777 | górna granica stacji, tuż za nią |
| D6 | `"99"` | `out_of_range` | 777 | górna granica protokołu, w środku |
| D7 | `"100"` | `invalid_entry` | 777 | górna granica protokołu, tuż za nią |
| D8 | `"-99"` | `out_of_range`, w części C `sensor_fault` | 777 | dolna granica protokołu, w środku; w części C kod awarii |
| D9 | `"-100"` | `invalid_entry` | 777 | dolna granica protokołu, tuż za nią |
| D10 | `"abc"` | `invalid_entry` | 777 | brak liczby na początku wpisu |
| D11 | `"0"` | `measured` | 0 | prawdziwe 0 jest pomiarem |
| D12 | `""` | `end_of_data` | 777 | brak danych; `temperature` bez zmian także na końcu |
| D13 | `"-98"` | `out_of_range` | 777 | część C: sąsiad kodu awarii bez zmian |

**Scenariusze.** Raport ma postać `{measured, out_of_range, invalid_entries, lowest, highest}`, a w części C na końcu jeszcze `sensor_faults`: w C1–C8 wynosi 0. C9 i C10 należą do części C.

| Przypadek | Tekst strumienia | `limit` | Raport | Dodatkowo | Co sprawdza |
|---|---|---:|---|---|---|
| C1 | `"21\n18\n25\n30\n"` | 3 | `{3, 0, 0, 18, 25}` | następne wywołanie: `measured`, 30 | limit osiągnięty, reszta nieprzeczytana; same dodatnie pomiary |
| C2 | `"21\n\n60\nabc\n19 C\n"` | 5 | `{2, 1, 1, 19, 21}` | | pusty wiersz nie jest próbą; odmowa każdego rodzaju i poprawny pomiar po nich; tekst po liczbie; koniec danych przed limitem |
| C3 | `"abc\nxyz\n-5"` | 4 | `{1, 0, 2, -5, -5}` | | dwa błędne wpisy z rzędu; ostatni poprawny wpis bez znaku końca wiersza; jeden pomiar to i najniższy, i najwyższy |
| C4 | `""` | 3 | `{0, 0, 0, 0, 0}` | | całkowicie pusty strumień |
| C5 | `"15\nerr"` | 4 | `{1, 0, 1, 15, 15}` | | ostatni błędny wpis bez znaku końca wiersza |
| C6 | `"60\n70\n-3\n-12\n8\n"` | 2 | `{2, 2, 0, -12, -3}` | następne wywołanie: `measured`, 8 | odmowy nie zużywają limitu; reszta nieprzeczytana; same ujemne pomiary |
| C7 | `"0\n5"` | 3 | `{2, 0, 0, 0, 5}` | | zero jako pierwszy pomiar; koniec danych przed limitem |
| C8 | `"60\nabc\n99999999999"` | 3 | `{0, 1, 2, 0, 0}` | | wpisy bez przyjętego pomiaru; liczba za duża dla `int`; wartości zastępcze |
| C9 | `"21\n-99\n22\n23\n"` | 2 | `{2, 0, 0, 21, 22, 1}` | następne wywołanie: `measured`, 23 | część C: awaria nie zużywa limitu i nie zmienia `lowest` ani `highest` |
| C10 | `"-99\n-99"` | 1 | `{0, 0, 0, 0, 0, 2}` | | część C: same awarie, brak pomiaru, wartości zastępcze |

Twój plan nie musi mieć dokładnie tych przypadków. Musi mieć wszystkie rodzaje wymienione w części A i pary z tabeli par.

</details>

## Rozwiązanie referencyjne

<details>
<summary>Plan i projekt rozwiązania referencyjnego, przed poprawką</summary>

To jedno z poprawnych rozwiązań, a nie jedyna dopuszczalna postać.

**Odpowiedzi na pytania planu, w skrócie:**

1. Zakres protokołu to −99…99: liczba spoza niego to `invalid_entry`, tak samo jak wpis bez liczby. Zakres stacji to −50…50: liczba z zakresu protokołu, ale spoza zakresu stacji, to `out_of_range`.
2. Limit liczy tylko przyjęte pomiary. Po jego osiągnięciu funkcja kończy pracę, a reszta danych zostaje w strumieniu: C1 i C6 sprawdzają to następnym wywołaniem.
3. Oba mają `measured == 0` i wartości zastępcze `lowest == 0`, `highest == 0`: C4 dla pustego strumienia, C8 dla wpisów bez przyjętego pomiaru. Raport z prawdziwym 0, jak w C7, ma `measured > 0`, więc jego `lowest` jest pomiarem.
4. Cztery funkcje są zdefiniowane tylko w `rules.cpp`, a ten plik stoi na listach obu targetów. Usterka w `read_measurement` zmienia wynik testów, a ta sama funkcja daje programowi właściwemu raport.

**`collect_measurements`:** pętla działa, dopóki `measured` jest mniejsze od `limit` i dane się nie skończyły. Każdy wynik obsługuje osobna etykieta `case`, zakończona przez `break`, jak w `count_ratings` z lekcji 14.4. Pierwszy przyjęty pomiar ustawia `lowest` i `highest`, a każdy następny porównuje się z nimi. `end_of_data` ustawia flagę `input_ended` i niczego nie liczy.

**`main.cpp`**:

<!-- example: station_given target=function_tests exit=1 -->
```cpp
#include <iostream>

#include "rules.hpp"

int main() {
    const int limit{6};
    const StationReport report{collect_measurements(std::cin, limit)};

    std::cout << "Measurements: " << report.measured << " of " << limit << "\n";

    if (report.measured > 0) {
        std::cout << "Lowest: " << report.lowest << "\n";
        std::cout << "Highest: " << report.highest << "\n";
    } else {
        std::cout << "No measurements\n";
    }

    std::cout << "Out of range: " << report.out_of_range << "\n";
    std::cout << "Invalid entries: " << report.invalid_entries << "\n";
}
```

**`rules.hpp`**:

<!-- file: station_given rules.hpp -->
```cpp
#pragma once

#include <istream>

enum class ReadResult {
    accepted,
    out_of_range,
    invalid_input,
    end_of_input
};

void discard_rest_of_line(std::istream& input);
ReadResult read_number(std::istream& input, int minimum, int maximum, int& result);

enum class Reading {
    measured,
    out_of_range,
    invalid_entry,
    end_of_data
};

Reading read_measurement(std::istream& input, int& temperature);

struct StationReport {
    int measured;
    int out_of_range;
    int invalid_entries;
    int lowest;
    int highest;
};

StationReport collect_measurements(std::istream& input, int limit);
```

**`rules.cpp`**, dostarczony kod i `collect_measurements`:

<!-- file: station_given rules.cpp -->
```cpp
#include "rules.hpp"

#include <limits>

void discard_rest_of_line(std::istream& input) {
    input.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
}

ReadResult read_number(std::istream& input, int minimum, int maximum, int& result) {
    if (input.bad()) {
        return ReadResult::end_of_input;
    }

    input >> std::ws;

    if (input.eof()) {
        return ReadResult::end_of_input;
    }

    int value{0};
    input >> value;

    if (input.fail()) {
        if (input.bad()) {
            return ReadResult::end_of_input;
        }

        input.clear();
        discard_rest_of_line(input);
        return ReadResult::invalid_input;
    }

    discard_rest_of_line(input);

    if (value < minimum || value > maximum) {
        return ReadResult::out_of_range;
    }

    result = value;
    return ReadResult::accepted;
}

Reading read_measurement(std::istream& input, int& temperature) {
    int value{0};
    const ReadResult result{read_number(input, -99, 99, value)};

    switch (result) {
        case ReadResult::accepted:
            break;
        case ReadResult::out_of_range:
            return Reading::out_of_range;
        case ReadResult::invalid_input:
            return Reading::invalid_entry;
        case ReadResult::end_of_input:
            return Reading::end_of_data;
    }

    if (value < -50 || value > 50) {
        return Reading::out_of_range;
    }

    temperature = value;
    return Reading::measured;
}

StationReport collect_measurements(std::istream& input, int limit) {
    StationReport report{0, 0, 0, 0, 0};
    int temperature{0};
    bool input_ended{false};

    while (report.measured < limit && !input_ended) {
        const Reading reading{read_measurement(input, temperature)};

        switch (reading) {
            case Reading::measured:
                if (report.measured == 0) {
                    report.lowest = temperature;
                    report.highest = temperature;
                } else if (temperature < report.lowest) {
                    report.lowest = temperature;
                } else if (temperature > report.highest) {
                    report.highest = temperature;
                }

                ++report.measured;
                break;
            case Reading::out_of_range:
                ++report.out_of_range;
                break;
            case Reading::invalid_entry:
                ++report.invalid_entries;
                break;
            case Reading::end_of_data:
                input_ended = true;
                break;
        }
    }

    return report;
}
```

**`function_tests.cpp`**, przypadki D1–D12 i C1–C8:

<!-- file: station_given function_tests.cpp -->
```cpp
#include <iostream>
#include <sstream>
#include <string>

#include "rules.hpp"

std::string reading_text(Reading reading) {
    switch (reading) {
        case Reading::measured:
            return "measured";
        case Reading::out_of_range:
            return "out_of_range";
        case Reading::invalid_entry:
            return "invalid_entry";
        case Reading::end_of_data:
            return "end_of_data";
    }

    return "unknown";
}

void check_reading(const std::string& name, Reading expected, Reading actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << reading_text(expected) << ", actual " << reading_text(actual) << "\n";
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

void check_report(const std::string& name, const StationReport& expected, const StationReport& actual, int& checks, int& failed) {
    check_int(name + " measured", expected.measured, actual.measured, checks, failed);
    check_int(name + " out_of_range", expected.out_of_range, actual.out_of_range, checks, failed);
    check_int(name + " invalid_entries", expected.invalid_entries, actual.invalid_entries, checks, failed);
    check_int(name + " lowest", expected.lowest, actual.lowest, checks, failed);
    check_int(name + " highest", expected.highest, actual.highest, checks, failed);
}

int main() {
    int checks{0};
    int failed{0};

    std::istringstream input_d1{"21.5"};
    int temperature_d1{777};
    check_reading("D1 result", Reading::measured, read_measurement(input_d1, temperature_d1), checks, failed);
    check_int("D1 temperature", 21, temperature_d1, checks, failed);

    std::istringstream input_d2{"-50"};
    int temperature_d2{777};
    check_reading("D2 result", Reading::measured, read_measurement(input_d2, temperature_d2), checks, failed);
    check_int("D2 temperature", -50, temperature_d2, checks, failed);

    std::istringstream input_d3{"-51"};
    int temperature_d3{777};
    check_reading("D3 result", Reading::out_of_range, read_measurement(input_d3, temperature_d3), checks, failed);
    check_int("D3 temperature", 777, temperature_d3, checks, failed);

    std::istringstream input_d4{"50"};
    int temperature_d4{777};
    check_reading("D4 result", Reading::measured, read_measurement(input_d4, temperature_d4), checks, failed);
    check_int("D4 temperature", 50, temperature_d4, checks, failed);

    std::istringstream input_d5{"51"};
    int temperature_d5{777};
    check_reading("D5 result", Reading::out_of_range, read_measurement(input_d5, temperature_d5), checks, failed);
    check_int("D5 temperature", 777, temperature_d5, checks, failed);

    std::istringstream input_d6{"99"};
    int temperature_d6{777};
    check_reading("D6 result", Reading::out_of_range, read_measurement(input_d6, temperature_d6), checks, failed);
    check_int("D6 temperature", 777, temperature_d6, checks, failed);

    std::istringstream input_d7{"100"};
    int temperature_d7{777};
    check_reading("D7 result", Reading::invalid_entry, read_measurement(input_d7, temperature_d7), checks, failed);
    check_int("D7 temperature", 777, temperature_d7, checks, failed);

    std::istringstream input_d8{"-99"};
    int temperature_d8{777};
    check_reading("D8 result", Reading::out_of_range, read_measurement(input_d8, temperature_d8), checks, failed);
    check_int("D8 temperature", 777, temperature_d8, checks, failed);

    std::istringstream input_d9{"-100"};
    int temperature_d9{777};
    check_reading("D9 result", Reading::invalid_entry, read_measurement(input_d9, temperature_d9), checks, failed);
    check_int("D9 temperature", 777, temperature_d9, checks, failed);

    std::istringstream input_d10{"abc"};
    int temperature_d10{777};
    check_reading("D10 result", Reading::invalid_entry, read_measurement(input_d10, temperature_d10), checks, failed);
    check_int("D10 temperature", 777, temperature_d10, checks, failed);

    std::istringstream input_d11{"0"};
    int temperature_d11{777};
    check_reading("D11 result", Reading::measured, read_measurement(input_d11, temperature_d11), checks, failed);
    check_int("D11 temperature", 0, temperature_d11, checks, failed);

    std::istringstream input_d12{""};
    int temperature_d12{777};
    check_reading("D12 result", Reading::end_of_data, read_measurement(input_d12, temperature_d12), checks, failed);
    check_int("D12 temperature", 777, temperature_d12, checks, failed);

    std::istringstream input_c1{"21\n18\n25\n30\n"};
    const StationReport report_c1{collect_measurements(input_c1, 3)};
    check_report("C1", StationReport{3, 0, 0, 18, 25}, report_c1, checks, failed);
    int next_c1{777};
    check_reading("C1 next result", Reading::measured, read_measurement(input_c1, next_c1), checks, failed);
    check_int("C1 next temperature", 30, next_c1, checks, failed);

    std::istringstream input_c2{"21\n\n60\nabc\n19 C\n"};
    const StationReport report_c2{collect_measurements(input_c2, 5)};
    check_report("C2", StationReport{2, 1, 1, 19, 21}, report_c2, checks, failed);

    std::istringstream input_c3{"abc\nxyz\n-5"};
    const StationReport report_c3{collect_measurements(input_c3, 4)};
    check_report("C3", StationReport{1, 0, 2, -5, -5}, report_c3, checks, failed);

    std::istringstream input_c4{""};
    const StationReport report_c4{collect_measurements(input_c4, 3)};
    check_report("C4", StationReport{0, 0, 0, 0, 0}, report_c4, checks, failed);

    std::istringstream input_c5{"15\nerr"};
    const StationReport report_c5{collect_measurements(input_c5, 4)};
    check_report("C5", StationReport{1, 0, 1, 15, 15}, report_c5, checks, failed);

    std::istringstream input_c6{"60\n70\n-3\n-12\n8\n"};
    const StationReport report_c6{collect_measurements(input_c6, 2)};
    check_report("C6", StationReport{2, 2, 0, -12, -3}, report_c6, checks, failed);
    int next_c6{777};
    check_reading("C6 next result", Reading::measured, read_measurement(input_c6, next_c6), checks, failed);
    check_int("C6 next temperature", 8, next_c6, checks, failed);

    std::istringstream input_c7{"0\n5"};
    const StationReport report_c7{collect_measurements(input_c7, 3)};
    check_report("C7", StationReport{2, 0, 0, 0, 5}, report_c7, checks, failed);

    std::istringstream input_c8{"60\nabc\n99999999999"};
    const StationReport report_c8{collect_measurements(input_c8, 3)};
    check_report("C8", StationReport{0, 1, 2, 0, 0}, report_c8, checks, failed);

    std::cout << "Checks: " << checks << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }
}
```

**`CMakeLists.txt`**:

<!-- cmake: station_given -->
```cmake
cmake_minimum_required(VERSION 3.28)
project(first_program LANGUAGES CXX)

add_executable(first_program main.cpp rules.cpp)
target_compile_features(first_program PRIVATE cxx_std_20)
set_target_properties(first_program PROPERTIES CXX_EXTENSIONS OFF)

add_executable(function_tests function_tests.cpp rules.cpp)
target_compile_features(function_tests PRIVATE cxx_std_20)
set_target_properties(function_tests PROPERTIES CXX_EXTENSIONS OFF)
```

**Przed poprawką**, z dostarczonym kodem, `function_tests` wypisuje:

<!-- output: station_given -->
```text
PASS D1 result
PASS D1 temperature
PASS D2 result
PASS D2 temperature
PASS D3 result
PASS D3 temperature
PASS D4 result
PASS D4 temperature
PASS D5 result
PASS D5 temperature
PASS D6 result
PASS D6 temperature
FAIL D7 result: expected invalid_entry, actual out_of_range
PASS D7 temperature
PASS D8 result
PASS D8 temperature
FAIL D9 result: expected invalid_entry, actual out_of_range
PASS D9 temperature
PASS D10 result
PASS D10 temperature
PASS D11 result
PASS D11 temperature
PASS D12 result
PASS D12 temperature
PASS C1 measured
PASS C1 out_of_range
PASS C1 invalid_entries
PASS C1 lowest
PASS C1 highest
PASS C1 next result
PASS C1 next temperature
PASS C2 measured
PASS C2 out_of_range
PASS C2 invalid_entries
PASS C2 lowest
PASS C2 highest
PASS C3 measured
PASS C3 out_of_range
PASS C3 invalid_entries
PASS C3 lowest
PASS C3 highest
PASS C4 measured
PASS C4 out_of_range
PASS C4 invalid_entries
PASS C4 lowest
PASS C4 highest
PASS C5 measured
PASS C5 out_of_range
PASS C5 invalid_entries
PASS C5 lowest
PASS C5 highest
PASS C6 measured
PASS C6 out_of_range
PASS C6 invalid_entries
PASS C6 lowest
PASS C6 highest
PASS C6 next result
PASS C6 next temperature
PASS C7 measured
PASS C7 out_of_range
PASS C7 invalid_entries
PASS C7 lowest
PASS C7 highest
PASS C8 measured
PASS C8 out_of_range
PASS C8 invalid_entries
PASS C8 lowest
PASS C8 highest
Checks: 68, failed: 2
```

Kod zakończenia: 1. To **test wykrywający błąd**: program testowy działa poprawnie, a kod 1 wynika z dwóch nieudanych sprawdzeń.

- **Które przypadki:** D7 (`100`) i D9 (`-100`), czyli liczby tuż za granicami zakresu protokołu. Obie nie są poprawnymi wiadomościami symulatora, więc kontrakt wymaga `invalid_entry`, a funkcja zwraca `out_of_range`. `temperature` zostaje 777, więc sprawdzenia `temperature` przechodzą.
- **Przyczyna:** w `read_measurement`, w `switch` po wyniku `read_number`, etykieta `ReadResult::out_of_range` zwraca `Reading::out_of_range`. `read_number` odmawia tu z powodu zakresu **protokołu**, więc według kontraktu to błędny wpis. Błąd jest w funkcji, bo wyniki oczekiwane zgadzają się z tabelą wyników.
- **Dlaczego pozostałe przechodzą:** liczby z zakresu protokołu, także D6 (`99`) i D8 (`-99`), przechodzą przez `read_number` i dostają właściwy wynik ze sprawdzenia zakresu stacji. Wpis bez liczby daje `invalid_input`, czyli `invalid_entry`, niezależnie od usterki. Dlatego zestaw, który sprawdza błędny wpis tylko przez `abc`, tej usterki nie wykryje: potrzebna jest para 99 i 100.
- **Program właściwy** z danymi z przykładu też działa poprawnie: nie ma w nich liczby spoza zakresu protokołu.

**Poprawka:** w `rules.cpp` jedna zmiana. W etykiecie `case ReadResult::out_of_range:` ma być `return Reading::invalid_entry;`. Program testowy, wyniki oczekiwane, `main.cpp` i `CMakeLists.txt` się nie zmieniają.

</details>

<details>
<summary>Wszystkie pliki projektu po poprawce</summary>

Różnią się od poprzednich tylko jedną linijką w `rules.cpp`.

**`main.cpp`**:

<!-- example: station_fixed target=function_tests -->
```cpp
#include <iostream>

#include "rules.hpp"

int main() {
    const int limit{6};
    const StationReport report{collect_measurements(std::cin, limit)};

    std::cout << "Measurements: " << report.measured << " of " << limit << "\n";

    if (report.measured > 0) {
        std::cout << "Lowest: " << report.lowest << "\n";
        std::cout << "Highest: " << report.highest << "\n";
    } else {
        std::cout << "No measurements\n";
    }

    std::cout << "Out of range: " << report.out_of_range << "\n";
    std::cout << "Invalid entries: " << report.invalid_entries << "\n";
}
```

**`rules.hpp`**:

<!-- file: station_fixed rules.hpp -->
```cpp
#pragma once

#include <istream>

enum class ReadResult {
    accepted,
    out_of_range,
    invalid_input,
    end_of_input
};

void discard_rest_of_line(std::istream& input);
ReadResult read_number(std::istream& input, int minimum, int maximum, int& result);

enum class Reading {
    measured,
    out_of_range,
    invalid_entry,
    end_of_data
};

Reading read_measurement(std::istream& input, int& temperature);

struct StationReport {
    int measured;
    int out_of_range;
    int invalid_entries;
    int lowest;
    int highest;
};

StationReport collect_measurements(std::istream& input, int limit);
```

**`rules.cpp`**:

<!-- file: station_fixed rules.cpp -->
```cpp
#include "rules.hpp"

#include <limits>

void discard_rest_of_line(std::istream& input) {
    input.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
}

ReadResult read_number(std::istream& input, int minimum, int maximum, int& result) {
    if (input.bad()) {
        return ReadResult::end_of_input;
    }

    input >> std::ws;

    if (input.eof()) {
        return ReadResult::end_of_input;
    }

    int value{0};
    input >> value;

    if (input.fail()) {
        if (input.bad()) {
            return ReadResult::end_of_input;
        }

        input.clear();
        discard_rest_of_line(input);
        return ReadResult::invalid_input;
    }

    discard_rest_of_line(input);

    if (value < minimum || value > maximum) {
        return ReadResult::out_of_range;
    }

    result = value;
    return ReadResult::accepted;
}

Reading read_measurement(std::istream& input, int& temperature) {
    int value{0};
    const ReadResult result{read_number(input, -99, 99, value)};

    switch (result) {
        case ReadResult::accepted:
            break;
        case ReadResult::out_of_range:
            return Reading::invalid_entry;
        case ReadResult::invalid_input:
            return Reading::invalid_entry;
        case ReadResult::end_of_input:
            return Reading::end_of_data;
    }

    if (value < -50 || value > 50) {
        return Reading::out_of_range;
    }

    temperature = value;
    return Reading::measured;
}

StationReport collect_measurements(std::istream& input, int limit) {
    StationReport report{0, 0, 0, 0, 0};
    int temperature{0};
    bool input_ended{false};

    while (report.measured < limit && !input_ended) {
        const Reading reading{read_measurement(input, temperature)};

        switch (reading) {
            case Reading::measured:
                if (report.measured == 0) {
                    report.lowest = temperature;
                    report.highest = temperature;
                } else if (temperature < report.lowest) {
                    report.lowest = temperature;
                } else if (temperature > report.highest) {
                    report.highest = temperature;
                }

                ++report.measured;
                break;
            case Reading::out_of_range:
                ++report.out_of_range;
                break;
            case Reading::invalid_entry:
                ++report.invalid_entries;
                break;
            case Reading::end_of_data:
                input_ended = true;
                break;
        }
    }

    return report;
}
```

**`function_tests.cpp`**, bez zmian:

<!-- file: station_fixed function_tests.cpp -->
```cpp
#include <iostream>
#include <sstream>
#include <string>

#include "rules.hpp"

std::string reading_text(Reading reading) {
    switch (reading) {
        case Reading::measured:
            return "measured";
        case Reading::out_of_range:
            return "out_of_range";
        case Reading::invalid_entry:
            return "invalid_entry";
        case Reading::end_of_data:
            return "end_of_data";
    }

    return "unknown";
}

void check_reading(const std::string& name, Reading expected, Reading actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << reading_text(expected) << ", actual " << reading_text(actual) << "\n";
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

void check_report(const std::string& name, const StationReport& expected, const StationReport& actual, int& checks, int& failed) {
    check_int(name + " measured", expected.measured, actual.measured, checks, failed);
    check_int(name + " out_of_range", expected.out_of_range, actual.out_of_range, checks, failed);
    check_int(name + " invalid_entries", expected.invalid_entries, actual.invalid_entries, checks, failed);
    check_int(name + " lowest", expected.lowest, actual.lowest, checks, failed);
    check_int(name + " highest", expected.highest, actual.highest, checks, failed);
}

int main() {
    int checks{0};
    int failed{0};

    std::istringstream input_d1{"21.5"};
    int temperature_d1{777};
    check_reading("D1 result", Reading::measured, read_measurement(input_d1, temperature_d1), checks, failed);
    check_int("D1 temperature", 21, temperature_d1, checks, failed);

    std::istringstream input_d2{"-50"};
    int temperature_d2{777};
    check_reading("D2 result", Reading::measured, read_measurement(input_d2, temperature_d2), checks, failed);
    check_int("D2 temperature", -50, temperature_d2, checks, failed);

    std::istringstream input_d3{"-51"};
    int temperature_d3{777};
    check_reading("D3 result", Reading::out_of_range, read_measurement(input_d3, temperature_d3), checks, failed);
    check_int("D3 temperature", 777, temperature_d3, checks, failed);

    std::istringstream input_d4{"50"};
    int temperature_d4{777};
    check_reading("D4 result", Reading::measured, read_measurement(input_d4, temperature_d4), checks, failed);
    check_int("D4 temperature", 50, temperature_d4, checks, failed);

    std::istringstream input_d5{"51"};
    int temperature_d5{777};
    check_reading("D5 result", Reading::out_of_range, read_measurement(input_d5, temperature_d5), checks, failed);
    check_int("D5 temperature", 777, temperature_d5, checks, failed);

    std::istringstream input_d6{"99"};
    int temperature_d6{777};
    check_reading("D6 result", Reading::out_of_range, read_measurement(input_d6, temperature_d6), checks, failed);
    check_int("D6 temperature", 777, temperature_d6, checks, failed);

    std::istringstream input_d7{"100"};
    int temperature_d7{777};
    check_reading("D7 result", Reading::invalid_entry, read_measurement(input_d7, temperature_d7), checks, failed);
    check_int("D7 temperature", 777, temperature_d7, checks, failed);

    std::istringstream input_d8{"-99"};
    int temperature_d8{777};
    check_reading("D8 result", Reading::out_of_range, read_measurement(input_d8, temperature_d8), checks, failed);
    check_int("D8 temperature", 777, temperature_d8, checks, failed);

    std::istringstream input_d9{"-100"};
    int temperature_d9{777};
    check_reading("D9 result", Reading::invalid_entry, read_measurement(input_d9, temperature_d9), checks, failed);
    check_int("D9 temperature", 777, temperature_d9, checks, failed);

    std::istringstream input_d10{"abc"};
    int temperature_d10{777};
    check_reading("D10 result", Reading::invalid_entry, read_measurement(input_d10, temperature_d10), checks, failed);
    check_int("D10 temperature", 777, temperature_d10, checks, failed);

    std::istringstream input_d11{"0"};
    int temperature_d11{777};
    check_reading("D11 result", Reading::measured, read_measurement(input_d11, temperature_d11), checks, failed);
    check_int("D11 temperature", 0, temperature_d11, checks, failed);

    std::istringstream input_d12{""};
    int temperature_d12{777};
    check_reading("D12 result", Reading::end_of_data, read_measurement(input_d12, temperature_d12), checks, failed);
    check_int("D12 temperature", 777, temperature_d12, checks, failed);

    std::istringstream input_c1{"21\n18\n25\n30\n"};
    const StationReport report_c1{collect_measurements(input_c1, 3)};
    check_report("C1", StationReport{3, 0, 0, 18, 25}, report_c1, checks, failed);
    int next_c1{777};
    check_reading("C1 next result", Reading::measured, read_measurement(input_c1, next_c1), checks, failed);
    check_int("C1 next temperature", 30, next_c1, checks, failed);

    std::istringstream input_c2{"21\n\n60\nabc\n19 C\n"};
    const StationReport report_c2{collect_measurements(input_c2, 5)};
    check_report("C2", StationReport{2, 1, 1, 19, 21}, report_c2, checks, failed);

    std::istringstream input_c3{"abc\nxyz\n-5"};
    const StationReport report_c3{collect_measurements(input_c3, 4)};
    check_report("C3", StationReport{1, 0, 2, -5, -5}, report_c3, checks, failed);

    std::istringstream input_c4{""};
    const StationReport report_c4{collect_measurements(input_c4, 3)};
    check_report("C4", StationReport{0, 0, 0, 0, 0}, report_c4, checks, failed);

    std::istringstream input_c5{"15\nerr"};
    const StationReport report_c5{collect_measurements(input_c5, 4)};
    check_report("C5", StationReport{1, 0, 1, 15, 15}, report_c5, checks, failed);

    std::istringstream input_c6{"60\n70\n-3\n-12\n8\n"};
    const StationReport report_c6{collect_measurements(input_c6, 2)};
    check_report("C6", StationReport{2, 2, 0, -12, -3}, report_c6, checks, failed);
    int next_c6{777};
    check_reading("C6 next result", Reading::measured, read_measurement(input_c6, next_c6), checks, failed);
    check_int("C6 next temperature", 8, next_c6, checks, failed);

    std::istringstream input_c7{"0\n5"};
    const StationReport report_c7{collect_measurements(input_c7, 3)};
    check_report("C7", StationReport{2, 0, 0, 0, 5}, report_c7, checks, failed);

    std::istringstream input_c8{"60\nabc\n99999999999"};
    const StationReport report_c8{collect_measurements(input_c8, 3)};
    check_report("C8", StationReport{0, 1, 2, 0, 0}, report_c8, checks, failed);

    std::cout << "Checks: " << checks << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }
}
```

**`CMakeLists.txt`**:

<!-- cmake: station_fixed -->
```cmake
cmake_minimum_required(VERSION 3.28)
project(first_program LANGUAGES CXX)

add_executable(first_program main.cpp rules.cpp)
target_compile_features(first_program PRIVATE cxx_std_20)
set_target_properties(first_program PROPERTIES CXX_EXTENSIONS OFF)

add_executable(function_tests function_tests.cpp rules.cpp)
target_compile_features(function_tests PRIVATE cxx_std_20)
set_target_properties(function_tests PROPERTIES CXX_EXTENSIONS OFF)
```

**Po poprawce** te same testy wypisują:

<!-- output: station_fixed -->
```text
PASS D1 result
PASS D1 temperature
PASS D2 result
PASS D2 temperature
PASS D3 result
PASS D3 temperature
PASS D4 result
PASS D4 temperature
PASS D5 result
PASS D5 temperature
PASS D6 result
PASS D6 temperature
PASS D7 result
PASS D7 temperature
PASS D8 result
PASS D8 temperature
PASS D9 result
PASS D9 temperature
PASS D10 result
PASS D10 temperature
PASS D11 result
PASS D11 temperature
PASS D12 result
PASS D12 temperature
PASS C1 measured
PASS C1 out_of_range
PASS C1 invalid_entries
PASS C1 lowest
PASS C1 highest
PASS C1 next result
PASS C1 next temperature
PASS C2 measured
PASS C2 out_of_range
PASS C2 invalid_entries
PASS C2 lowest
PASS C2 highest
PASS C3 measured
PASS C3 out_of_range
PASS C3 invalid_entries
PASS C3 lowest
PASS C3 highest
PASS C4 measured
PASS C4 out_of_range
PASS C4 invalid_entries
PASS C4 lowest
PASS C4 highest
PASS C5 measured
PASS C5 out_of_range
PASS C5 invalid_entries
PASS C5 lowest
PASS C5 highest
PASS C6 measured
PASS C6 out_of_range
PASS C6 invalid_entries
PASS C6 lowest
PASS C6 highest
PASS C6 next result
PASS C6 next temperature
PASS C7 measured
PASS C7 out_of_range
PASS C7 invalid_entries
PASS C7 lowest
PASS C7 highest
PASS C8 measured
PASS C8 out_of_range
PASS C8 invalid_entries
PASS C8 lowest
PASS C8 highest
Checks: 68, failed: 0
```

Kod zakończenia: 0. Wszystkie 68 sprawdzeń przechodzą: 12 przypadków bezpośrednich po 2 sprawdzenia, 8 scenariuszy po 5 i 2 dodatkowe wywołania po 2. Program właściwy z danymi z przykładu wypisuje raport ze specyfikacji.

</details>

<details>
<summary>Część C: mapa zmian i testy przed zmianą funkcji</summary>

**Mapa zmian:**

| Miejsce | Zmiana |
|---|---|
| `rules.hpp` | `sensor_fault` w `Reading`, `sensor_faults` w `StationReport` |
| `read_measurement` | sprawdzenie kodu awarii przed zakresem stacji |
| `collect_measurements` | raport startowy z sześcioma zerami, etykieta `sensor_fault` |
| `main.cpp` | linijka `Sensor faults` |
| `reading_text` | etykieta `sensor_fault` |
| `check_report` | sprawdzenie `sensor_faults` |
| oczekiwane raporty C1–C8 | jawna szósta wartość: 0 |
| D8 | `sensor_fault` zamiast `out_of_range`: jedyne zmienione dawne oczekiwanie, bo tylko D8 ma wpis `-99` |
| nowe przypadki | D13, C9, C10 |

`ReadResult`, `read_number` i `discard_rest_of_line` się nie zmieniają.

**Etykieta w `collect_measurements`:**

<!-- fragment -->
```cpp
            case Reading::sensor_fault:
                ++report.sensor_faults;
                break;
```

**Pliki po krokach 2–4,** bez sprawdzenia kodu awarii. `main.cpp` jest jeszcze taki jak w części B:

<!-- example: station_sensor_first target=function_tests exit=1 -->
```cpp
#include <iostream>

#include "rules.hpp"

int main() {
    const int limit{6};
    const StationReport report{collect_measurements(std::cin, limit)};

    std::cout << "Measurements: " << report.measured << " of " << limit << "\n";

    if (report.measured > 0) {
        std::cout << "Lowest: " << report.lowest << "\n";
        std::cout << "Highest: " << report.highest << "\n";
    } else {
        std::cout << "No measurements\n";
    }

    std::cout << "Out of range: " << report.out_of_range << "\n";
    std::cout << "Invalid entries: " << report.invalid_entries << "\n";
}
```

**`rules.hpp`**:

<!-- file: station_sensor_first rules.hpp -->
```cpp
#pragma once

#include <istream>

enum class ReadResult {
    accepted,
    out_of_range,
    invalid_input,
    end_of_input
};

void discard_rest_of_line(std::istream& input);
ReadResult read_number(std::istream& input, int minimum, int maximum, int& result);

enum class Reading {
    measured,
    out_of_range,
    invalid_entry,
    sensor_fault,
    end_of_data
};

Reading read_measurement(std::istream& input, int& temperature);

struct StationReport {
    int measured;
    int out_of_range;
    int invalid_entries;
    int lowest;
    int highest;
    int sensor_faults;
};

StationReport collect_measurements(std::istream& input, int limit);
```

**`rules.cpp`**:

<!-- file: station_sensor_first rules.cpp -->
```cpp
#include "rules.hpp"

#include <limits>

void discard_rest_of_line(std::istream& input) {
    input.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
}

ReadResult read_number(std::istream& input, int minimum, int maximum, int& result) {
    if (input.bad()) {
        return ReadResult::end_of_input;
    }

    input >> std::ws;

    if (input.eof()) {
        return ReadResult::end_of_input;
    }

    int value{0};
    input >> value;

    if (input.fail()) {
        if (input.bad()) {
            return ReadResult::end_of_input;
        }

        input.clear();
        discard_rest_of_line(input);
        return ReadResult::invalid_input;
    }

    discard_rest_of_line(input);

    if (value < minimum || value > maximum) {
        return ReadResult::out_of_range;
    }

    result = value;
    return ReadResult::accepted;
}

Reading read_measurement(std::istream& input, int& temperature) {
    int value{0};
    const ReadResult result{read_number(input, -99, 99, value)};

    switch (result) {
        case ReadResult::accepted:
            break;
        case ReadResult::out_of_range:
            return Reading::invalid_entry;
        case ReadResult::invalid_input:
            return Reading::invalid_entry;
        case ReadResult::end_of_input:
            return Reading::end_of_data;
    }

    if (value < -50 || value > 50) {
        return Reading::out_of_range;
    }

    temperature = value;
    return Reading::measured;
}

StationReport collect_measurements(std::istream& input, int limit) {
    StationReport report{0, 0, 0, 0, 0, 0};
    int temperature{0};
    bool input_ended{false};

    while (report.measured < limit && !input_ended) {
        const Reading reading{read_measurement(input, temperature)};

        switch (reading) {
            case Reading::measured:
                if (report.measured == 0) {
                    report.lowest = temperature;
                    report.highest = temperature;
                } else if (temperature < report.lowest) {
                    report.lowest = temperature;
                } else if (temperature > report.highest) {
                    report.highest = temperature;
                }

                ++report.measured;
                break;
            case Reading::out_of_range:
                ++report.out_of_range;
                break;
            case Reading::invalid_entry:
                ++report.invalid_entries;
                break;
            case Reading::sensor_fault:
                ++report.sensor_faults;
                break;
            case Reading::end_of_data:
                input_ended = true;
                break;
        }
    }

    return report;
}
```

**`function_tests.cpp`**, przypadki D1–D13 i C1–C10:

<!-- file: station_sensor_first function_tests.cpp -->
```cpp
#include <iostream>
#include <sstream>
#include <string>

#include "rules.hpp"

std::string reading_text(Reading reading) {
    switch (reading) {
        case Reading::measured:
            return "measured";
        case Reading::out_of_range:
            return "out_of_range";
        case Reading::invalid_entry:
            return "invalid_entry";
        case Reading::sensor_fault:
            return "sensor_fault";
        case Reading::end_of_data:
            return "end_of_data";
    }

    return "unknown";
}

void check_reading(const std::string& name, Reading expected, Reading actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << reading_text(expected) << ", actual " << reading_text(actual) << "\n";
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

void check_report(const std::string& name, const StationReport& expected, const StationReport& actual, int& checks, int& failed) {
    check_int(name + " measured", expected.measured, actual.measured, checks, failed);
    check_int(name + " out_of_range", expected.out_of_range, actual.out_of_range, checks, failed);
    check_int(name + " invalid_entries", expected.invalid_entries, actual.invalid_entries, checks, failed);
    check_int(name + " lowest", expected.lowest, actual.lowest, checks, failed);
    check_int(name + " highest", expected.highest, actual.highest, checks, failed);
    check_int(name + " sensor_faults", expected.sensor_faults, actual.sensor_faults, checks, failed);
}

int main() {
    int checks{0};
    int failed{0};

    std::istringstream input_d1{"21.5"};
    int temperature_d1{777};
    check_reading("D1 result", Reading::measured, read_measurement(input_d1, temperature_d1), checks, failed);
    check_int("D1 temperature", 21, temperature_d1, checks, failed);

    std::istringstream input_d2{"-50"};
    int temperature_d2{777};
    check_reading("D2 result", Reading::measured, read_measurement(input_d2, temperature_d2), checks, failed);
    check_int("D2 temperature", -50, temperature_d2, checks, failed);

    std::istringstream input_d3{"-51"};
    int temperature_d3{777};
    check_reading("D3 result", Reading::out_of_range, read_measurement(input_d3, temperature_d3), checks, failed);
    check_int("D3 temperature", 777, temperature_d3, checks, failed);

    std::istringstream input_d4{"50"};
    int temperature_d4{777};
    check_reading("D4 result", Reading::measured, read_measurement(input_d4, temperature_d4), checks, failed);
    check_int("D4 temperature", 50, temperature_d4, checks, failed);

    std::istringstream input_d5{"51"};
    int temperature_d5{777};
    check_reading("D5 result", Reading::out_of_range, read_measurement(input_d5, temperature_d5), checks, failed);
    check_int("D5 temperature", 777, temperature_d5, checks, failed);

    std::istringstream input_d6{"99"};
    int temperature_d6{777};
    check_reading("D6 result", Reading::out_of_range, read_measurement(input_d6, temperature_d6), checks, failed);
    check_int("D6 temperature", 777, temperature_d6, checks, failed);

    std::istringstream input_d7{"100"};
    int temperature_d7{777};
    check_reading("D7 result", Reading::invalid_entry, read_measurement(input_d7, temperature_d7), checks, failed);
    check_int("D7 temperature", 777, temperature_d7, checks, failed);

    std::istringstream input_d8{"-99"};
    int temperature_d8{777};
    check_reading("D8 result", Reading::sensor_fault, read_measurement(input_d8, temperature_d8), checks, failed);
    check_int("D8 temperature", 777, temperature_d8, checks, failed);

    std::istringstream input_d9{"-100"};
    int temperature_d9{777};
    check_reading("D9 result", Reading::invalid_entry, read_measurement(input_d9, temperature_d9), checks, failed);
    check_int("D9 temperature", 777, temperature_d9, checks, failed);

    std::istringstream input_d10{"abc"};
    int temperature_d10{777};
    check_reading("D10 result", Reading::invalid_entry, read_measurement(input_d10, temperature_d10), checks, failed);
    check_int("D10 temperature", 777, temperature_d10, checks, failed);

    std::istringstream input_d11{"0"};
    int temperature_d11{777};
    check_reading("D11 result", Reading::measured, read_measurement(input_d11, temperature_d11), checks, failed);
    check_int("D11 temperature", 0, temperature_d11, checks, failed);

    std::istringstream input_d12{""};
    int temperature_d12{777};
    check_reading("D12 result", Reading::end_of_data, read_measurement(input_d12, temperature_d12), checks, failed);
    check_int("D12 temperature", 777, temperature_d12, checks, failed);

    std::istringstream input_d13{"-98"};
    int temperature_d13{777};
    check_reading("D13 result", Reading::out_of_range, read_measurement(input_d13, temperature_d13), checks, failed);
    check_int("D13 temperature", 777, temperature_d13, checks, failed);

    std::istringstream input_c1{"21\n18\n25\n30\n"};
    const StationReport report_c1{collect_measurements(input_c1, 3)};
    check_report("C1", StationReport{3, 0, 0, 18, 25, 0}, report_c1, checks, failed);
    int next_c1{777};
    check_reading("C1 next result", Reading::measured, read_measurement(input_c1, next_c1), checks, failed);
    check_int("C1 next temperature", 30, next_c1, checks, failed);

    std::istringstream input_c2{"21\n\n60\nabc\n19 C\n"};
    const StationReport report_c2{collect_measurements(input_c2, 5)};
    check_report("C2", StationReport{2, 1, 1, 19, 21, 0}, report_c2, checks, failed);

    std::istringstream input_c3{"abc\nxyz\n-5"};
    const StationReport report_c3{collect_measurements(input_c3, 4)};
    check_report("C3", StationReport{1, 0, 2, -5, -5, 0}, report_c3, checks, failed);

    std::istringstream input_c4{""};
    const StationReport report_c4{collect_measurements(input_c4, 3)};
    check_report("C4", StationReport{0, 0, 0, 0, 0, 0}, report_c4, checks, failed);

    std::istringstream input_c5{"15\nerr"};
    const StationReport report_c5{collect_measurements(input_c5, 4)};
    check_report("C5", StationReport{1, 0, 1, 15, 15, 0}, report_c5, checks, failed);

    std::istringstream input_c6{"60\n70\n-3\n-12\n8\n"};
    const StationReport report_c6{collect_measurements(input_c6, 2)};
    check_report("C6", StationReport{2, 2, 0, -12, -3, 0}, report_c6, checks, failed);
    int next_c6{777};
    check_reading("C6 next result", Reading::measured, read_measurement(input_c6, next_c6), checks, failed);
    check_int("C6 next temperature", 8, next_c6, checks, failed);

    std::istringstream input_c7{"0\n5"};
    const StationReport report_c7{collect_measurements(input_c7, 3)};
    check_report("C7", StationReport{2, 0, 0, 0, 5, 0}, report_c7, checks, failed);

    std::istringstream input_c8{"60\nabc\n99999999999"};
    const StationReport report_c8{collect_measurements(input_c8, 3)};
    check_report("C8", StationReport{0, 1, 2, 0, 0, 0}, report_c8, checks, failed);

    std::istringstream input_c9{"21\n-99\n22\n23\n"};
    const StationReport report_c9{collect_measurements(input_c9, 2)};
    check_report("C9", StationReport{2, 0, 0, 21, 22, 1}, report_c9, checks, failed);
    int next_c9{777};
    check_reading("C9 next result", Reading::measured, read_measurement(input_c9, next_c9), checks, failed);
    check_int("C9 next temperature", 23, next_c9, checks, failed);

    std::istringstream input_c10{"-99\n-99"};
    const StationReport report_c10{collect_measurements(input_c10, 1)};
    check_report("C10", StationReport{0, 0, 0, 0, 0, 2}, report_c10, checks, failed);

    std::cout << "Checks: " << checks << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }
}
```

**`CMakeLists.txt`**:

<!-- cmake: station_sensor_first -->
```cmake
cmake_minimum_required(VERSION 3.28)
project(first_program LANGUAGES CXX)

add_executable(first_program main.cpp rules.cpp)
target_compile_features(first_program PRIVATE cxx_std_20)
set_target_properties(first_program PROPERTIES CXX_EXTENSIONS OFF)

add_executable(function_tests function_tests.cpp rules.cpp)
target_compile_features(function_tests PRIVATE cxx_std_20)
set_target_properties(function_tests PROPERTIES CXX_EXTENSIONS OFF)
```

**Czwarte uruchomienie**, przed zmianą `read_measurement`:

<!-- output: station_sensor_first -->
```text
PASS D1 result
PASS D1 temperature
PASS D2 result
PASS D2 temperature
PASS D3 result
PASS D3 temperature
PASS D4 result
PASS D4 temperature
PASS D5 result
PASS D5 temperature
PASS D6 result
PASS D6 temperature
PASS D7 result
PASS D7 temperature
FAIL D8 result: expected sensor_fault, actual out_of_range
PASS D8 temperature
PASS D9 result
PASS D9 temperature
PASS D10 result
PASS D10 temperature
PASS D11 result
PASS D11 temperature
PASS D12 result
PASS D12 temperature
PASS D13 result
PASS D13 temperature
PASS C1 measured
PASS C1 out_of_range
PASS C1 invalid_entries
PASS C1 lowest
PASS C1 highest
PASS C1 sensor_faults
PASS C1 next result
PASS C1 next temperature
PASS C2 measured
PASS C2 out_of_range
PASS C2 invalid_entries
PASS C2 lowest
PASS C2 highest
PASS C2 sensor_faults
PASS C3 measured
PASS C3 out_of_range
PASS C3 invalid_entries
PASS C3 lowest
PASS C3 highest
PASS C3 sensor_faults
PASS C4 measured
PASS C4 out_of_range
PASS C4 invalid_entries
PASS C4 lowest
PASS C4 highest
PASS C4 sensor_faults
PASS C5 measured
PASS C5 out_of_range
PASS C5 invalid_entries
PASS C5 lowest
PASS C5 highest
PASS C5 sensor_faults
PASS C6 measured
PASS C6 out_of_range
PASS C6 invalid_entries
PASS C6 lowest
PASS C6 highest
PASS C6 sensor_faults
PASS C6 next result
PASS C6 next temperature
PASS C7 measured
PASS C7 out_of_range
PASS C7 invalid_entries
PASS C7 lowest
PASS C7 highest
PASS C7 sensor_faults
PASS C8 measured
PASS C8 out_of_range
PASS C8 invalid_entries
PASS C8 lowest
PASS C8 highest
PASS C8 sensor_faults
PASS C9 measured
FAIL C9 out_of_range: expected 0, actual 1
PASS C9 invalid_entries
PASS C9 lowest
PASS C9 highest
FAIL C9 sensor_faults: expected 1, actual 0
PASS C9 next result
PASS C9 next temperature
PASS C10 measured
FAIL C10 out_of_range: expected 0, actual 2
PASS C10 invalid_entries
PASS C10 lowest
PASS C10 highest
FAIL C10 sensor_faults: expected 2, actual 0
Checks: 92, failed: 5
```

Kod zakończenia: 1. Pięć sprawdzeń opisuje awarię, której funkcja jeszcze nie rozpoznaje:

- **D8 result:** −99 przechodzi przez `read_number`, a potem sprawdzenie zakresu stacji daje `out_of_range`.
- **C9 i C10:** każda awaria jest liczona w `out_of_range`, a `sensor_faults` zostaje 0.
- **Co przechodzi:** dawne przypadki z jawną szóstą wartością 0, D13 i sprawdzenia `temperature`: po −99 nadal wynosi 777. W C9 limit też działa: awaria, liczona tu jako odmowa, nie zużywa go, więc `measured`, `lowest`, `highest` i następne wywołanie się zgadzają.

</details>

<details>
<summary>Część C ukończona</summary>

W `read_measurement` sprawdzenie kodu awarii stoi przed sprawdzeniem zakresu stacji:

<!-- fragment -->
```cpp
    if (value == -99) {
        return Reading::sensor_fault;
    }

    if (value < -50 || value > 50) {
        return Reading::out_of_range;
    }
```

Gdyby stało po nim, −99 dawałoby nadal `out_of_range`: wykryłyby to D8, C9 i C10.

**`main.cpp`**, z linijką `Sensor faults`:

<!-- example: station_sensor target=function_tests -->
```cpp
#include <iostream>

#include "rules.hpp"

int main() {
    const int limit{6};
    const StationReport report{collect_measurements(std::cin, limit)};

    std::cout << "Measurements: " << report.measured << " of " << limit << "\n";

    if (report.measured > 0) {
        std::cout << "Lowest: " << report.lowest << "\n";
        std::cout << "Highest: " << report.highest << "\n";
    } else {
        std::cout << "No measurements\n";
    }

    std::cout << "Out of range: " << report.out_of_range << "\n";
    std::cout << "Invalid entries: " << report.invalid_entries << "\n";
    std::cout << "Sensor faults: " << report.sensor_faults << "\n";
}
```

**`rules.hpp`**:

<!-- file: station_sensor rules.hpp -->
```cpp
#pragma once

#include <istream>

enum class ReadResult {
    accepted,
    out_of_range,
    invalid_input,
    end_of_input
};

void discard_rest_of_line(std::istream& input);
ReadResult read_number(std::istream& input, int minimum, int maximum, int& result);

enum class Reading {
    measured,
    out_of_range,
    invalid_entry,
    sensor_fault,
    end_of_data
};

Reading read_measurement(std::istream& input, int& temperature);

struct StationReport {
    int measured;
    int out_of_range;
    int invalid_entries;
    int lowest;
    int highest;
    int sensor_faults;
};

StationReport collect_measurements(std::istream& input, int limit);
```

**`rules.cpp`**:

<!-- file: station_sensor rules.cpp -->
```cpp
#include "rules.hpp"

#include <limits>

void discard_rest_of_line(std::istream& input) {
    input.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
}

ReadResult read_number(std::istream& input, int minimum, int maximum, int& result) {
    if (input.bad()) {
        return ReadResult::end_of_input;
    }

    input >> std::ws;

    if (input.eof()) {
        return ReadResult::end_of_input;
    }

    int value{0};
    input >> value;

    if (input.fail()) {
        if (input.bad()) {
            return ReadResult::end_of_input;
        }

        input.clear();
        discard_rest_of_line(input);
        return ReadResult::invalid_input;
    }

    discard_rest_of_line(input);

    if (value < minimum || value > maximum) {
        return ReadResult::out_of_range;
    }

    result = value;
    return ReadResult::accepted;
}

Reading read_measurement(std::istream& input, int& temperature) {
    int value{0};
    const ReadResult result{read_number(input, -99, 99, value)};

    switch (result) {
        case ReadResult::accepted:
            break;
        case ReadResult::out_of_range:
            return Reading::invalid_entry;
        case ReadResult::invalid_input:
            return Reading::invalid_entry;
        case ReadResult::end_of_input:
            return Reading::end_of_data;
    }

    if (value == -99) {
        return Reading::sensor_fault;
    }

    if (value < -50 || value > 50) {
        return Reading::out_of_range;
    }

    temperature = value;
    return Reading::measured;
}

StationReport collect_measurements(std::istream& input, int limit) {
    StationReport report{0, 0, 0, 0, 0, 0};
    int temperature{0};
    bool input_ended{false};

    while (report.measured < limit && !input_ended) {
        const Reading reading{read_measurement(input, temperature)};

        switch (reading) {
            case Reading::measured:
                if (report.measured == 0) {
                    report.lowest = temperature;
                    report.highest = temperature;
                } else if (temperature < report.lowest) {
                    report.lowest = temperature;
                } else if (temperature > report.highest) {
                    report.highest = temperature;
                }

                ++report.measured;
                break;
            case Reading::out_of_range:
                ++report.out_of_range;
                break;
            case Reading::invalid_entry:
                ++report.invalid_entries;
                break;
            case Reading::sensor_fault:
                ++report.sensor_faults;
                break;
            case Reading::end_of_data:
                input_ended = true;
                break;
        }
    }

    return report;
}
```

**`function_tests.cpp`**, bez zmian od czwartego uruchomienia:

<!-- file: station_sensor function_tests.cpp -->
```cpp
#include <iostream>
#include <sstream>
#include <string>

#include "rules.hpp"

std::string reading_text(Reading reading) {
    switch (reading) {
        case Reading::measured:
            return "measured";
        case Reading::out_of_range:
            return "out_of_range";
        case Reading::invalid_entry:
            return "invalid_entry";
        case Reading::sensor_fault:
            return "sensor_fault";
        case Reading::end_of_data:
            return "end_of_data";
    }

    return "unknown";
}

void check_reading(const std::string& name, Reading expected, Reading actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << reading_text(expected) << ", actual " << reading_text(actual) << "\n";
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

void check_report(const std::string& name, const StationReport& expected, const StationReport& actual, int& checks, int& failed) {
    check_int(name + " measured", expected.measured, actual.measured, checks, failed);
    check_int(name + " out_of_range", expected.out_of_range, actual.out_of_range, checks, failed);
    check_int(name + " invalid_entries", expected.invalid_entries, actual.invalid_entries, checks, failed);
    check_int(name + " lowest", expected.lowest, actual.lowest, checks, failed);
    check_int(name + " highest", expected.highest, actual.highest, checks, failed);
    check_int(name + " sensor_faults", expected.sensor_faults, actual.sensor_faults, checks, failed);
}

int main() {
    int checks{0};
    int failed{0};

    std::istringstream input_d1{"21.5"};
    int temperature_d1{777};
    check_reading("D1 result", Reading::measured, read_measurement(input_d1, temperature_d1), checks, failed);
    check_int("D1 temperature", 21, temperature_d1, checks, failed);

    std::istringstream input_d2{"-50"};
    int temperature_d2{777};
    check_reading("D2 result", Reading::measured, read_measurement(input_d2, temperature_d2), checks, failed);
    check_int("D2 temperature", -50, temperature_d2, checks, failed);

    std::istringstream input_d3{"-51"};
    int temperature_d3{777};
    check_reading("D3 result", Reading::out_of_range, read_measurement(input_d3, temperature_d3), checks, failed);
    check_int("D3 temperature", 777, temperature_d3, checks, failed);

    std::istringstream input_d4{"50"};
    int temperature_d4{777};
    check_reading("D4 result", Reading::measured, read_measurement(input_d4, temperature_d4), checks, failed);
    check_int("D4 temperature", 50, temperature_d4, checks, failed);

    std::istringstream input_d5{"51"};
    int temperature_d5{777};
    check_reading("D5 result", Reading::out_of_range, read_measurement(input_d5, temperature_d5), checks, failed);
    check_int("D5 temperature", 777, temperature_d5, checks, failed);

    std::istringstream input_d6{"99"};
    int temperature_d6{777};
    check_reading("D6 result", Reading::out_of_range, read_measurement(input_d6, temperature_d6), checks, failed);
    check_int("D6 temperature", 777, temperature_d6, checks, failed);

    std::istringstream input_d7{"100"};
    int temperature_d7{777};
    check_reading("D7 result", Reading::invalid_entry, read_measurement(input_d7, temperature_d7), checks, failed);
    check_int("D7 temperature", 777, temperature_d7, checks, failed);

    std::istringstream input_d8{"-99"};
    int temperature_d8{777};
    check_reading("D8 result", Reading::sensor_fault, read_measurement(input_d8, temperature_d8), checks, failed);
    check_int("D8 temperature", 777, temperature_d8, checks, failed);

    std::istringstream input_d9{"-100"};
    int temperature_d9{777};
    check_reading("D9 result", Reading::invalid_entry, read_measurement(input_d9, temperature_d9), checks, failed);
    check_int("D9 temperature", 777, temperature_d9, checks, failed);

    std::istringstream input_d10{"abc"};
    int temperature_d10{777};
    check_reading("D10 result", Reading::invalid_entry, read_measurement(input_d10, temperature_d10), checks, failed);
    check_int("D10 temperature", 777, temperature_d10, checks, failed);

    std::istringstream input_d11{"0"};
    int temperature_d11{777};
    check_reading("D11 result", Reading::measured, read_measurement(input_d11, temperature_d11), checks, failed);
    check_int("D11 temperature", 0, temperature_d11, checks, failed);

    std::istringstream input_d12{""};
    int temperature_d12{777};
    check_reading("D12 result", Reading::end_of_data, read_measurement(input_d12, temperature_d12), checks, failed);
    check_int("D12 temperature", 777, temperature_d12, checks, failed);

    std::istringstream input_d13{"-98"};
    int temperature_d13{777};
    check_reading("D13 result", Reading::out_of_range, read_measurement(input_d13, temperature_d13), checks, failed);
    check_int("D13 temperature", 777, temperature_d13, checks, failed);

    std::istringstream input_c1{"21\n18\n25\n30\n"};
    const StationReport report_c1{collect_measurements(input_c1, 3)};
    check_report("C1", StationReport{3, 0, 0, 18, 25, 0}, report_c1, checks, failed);
    int next_c1{777};
    check_reading("C1 next result", Reading::measured, read_measurement(input_c1, next_c1), checks, failed);
    check_int("C1 next temperature", 30, next_c1, checks, failed);

    std::istringstream input_c2{"21\n\n60\nabc\n19 C\n"};
    const StationReport report_c2{collect_measurements(input_c2, 5)};
    check_report("C2", StationReport{2, 1, 1, 19, 21, 0}, report_c2, checks, failed);

    std::istringstream input_c3{"abc\nxyz\n-5"};
    const StationReport report_c3{collect_measurements(input_c3, 4)};
    check_report("C3", StationReport{1, 0, 2, -5, -5, 0}, report_c3, checks, failed);

    std::istringstream input_c4{""};
    const StationReport report_c4{collect_measurements(input_c4, 3)};
    check_report("C4", StationReport{0, 0, 0, 0, 0, 0}, report_c4, checks, failed);

    std::istringstream input_c5{"15\nerr"};
    const StationReport report_c5{collect_measurements(input_c5, 4)};
    check_report("C5", StationReport{1, 0, 1, 15, 15, 0}, report_c5, checks, failed);

    std::istringstream input_c6{"60\n70\n-3\n-12\n8\n"};
    const StationReport report_c6{collect_measurements(input_c6, 2)};
    check_report("C6", StationReport{2, 2, 0, -12, -3, 0}, report_c6, checks, failed);
    int next_c6{777};
    check_reading("C6 next result", Reading::measured, read_measurement(input_c6, next_c6), checks, failed);
    check_int("C6 next temperature", 8, next_c6, checks, failed);

    std::istringstream input_c7{"0\n5"};
    const StationReport report_c7{collect_measurements(input_c7, 3)};
    check_report("C7", StationReport{2, 0, 0, 0, 5, 0}, report_c7, checks, failed);

    std::istringstream input_c8{"60\nabc\n99999999999"};
    const StationReport report_c8{collect_measurements(input_c8, 3)};
    check_report("C8", StationReport{0, 1, 2, 0, 0, 0}, report_c8, checks, failed);

    std::istringstream input_c9{"21\n-99\n22\n23\n"};
    const StationReport report_c9{collect_measurements(input_c9, 2)};
    check_report("C9", StationReport{2, 0, 0, 21, 22, 1}, report_c9, checks, failed);
    int next_c9{777};
    check_reading("C9 next result", Reading::measured, read_measurement(input_c9, next_c9), checks, failed);
    check_int("C9 next temperature", 23, next_c9, checks, failed);

    std::istringstream input_c10{"-99\n-99"};
    const StationReport report_c10{collect_measurements(input_c10, 1)};
    check_report("C10", StationReport{0, 0, 0, 0, 0, 2}, report_c10, checks, failed);

    std::cout << "Checks: " << checks << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }
}
```

**`CMakeLists.txt`**:

<!-- cmake: station_sensor -->
```cmake
cmake_minimum_required(VERSION 3.28)
project(first_program LANGUAGES CXX)

add_executable(first_program main.cpp rules.cpp)
target_compile_features(first_program PRIVATE cxx_std_20)
set_target_properties(first_program PROPERTIES CXX_EXTENSIONS OFF)

add_executable(function_tests function_tests.cpp rules.cpp)
target_compile_features(function_tests PRIVATE cxx_std_20)
set_target_properties(function_tests PROPERTIES CXX_EXTENSIONS OFF)
```

**Piąte uruchomienie:**

<!-- output: station_sensor -->
```text
PASS D1 result
PASS D1 temperature
PASS D2 result
PASS D2 temperature
PASS D3 result
PASS D3 temperature
PASS D4 result
PASS D4 temperature
PASS D5 result
PASS D5 temperature
PASS D6 result
PASS D6 temperature
PASS D7 result
PASS D7 temperature
PASS D8 result
PASS D8 temperature
PASS D9 result
PASS D9 temperature
PASS D10 result
PASS D10 temperature
PASS D11 result
PASS D11 temperature
PASS D12 result
PASS D12 temperature
PASS D13 result
PASS D13 temperature
PASS C1 measured
PASS C1 out_of_range
PASS C1 invalid_entries
PASS C1 lowest
PASS C1 highest
PASS C1 sensor_faults
PASS C1 next result
PASS C1 next temperature
PASS C2 measured
PASS C2 out_of_range
PASS C2 invalid_entries
PASS C2 lowest
PASS C2 highest
PASS C2 sensor_faults
PASS C3 measured
PASS C3 out_of_range
PASS C3 invalid_entries
PASS C3 lowest
PASS C3 highest
PASS C3 sensor_faults
PASS C4 measured
PASS C4 out_of_range
PASS C4 invalid_entries
PASS C4 lowest
PASS C4 highest
PASS C4 sensor_faults
PASS C5 measured
PASS C5 out_of_range
PASS C5 invalid_entries
PASS C5 lowest
PASS C5 highest
PASS C5 sensor_faults
PASS C6 measured
PASS C6 out_of_range
PASS C6 invalid_entries
PASS C6 lowest
PASS C6 highest
PASS C6 sensor_faults
PASS C6 next result
PASS C6 next temperature
PASS C7 measured
PASS C7 out_of_range
PASS C7 invalid_entries
PASS C7 lowest
PASS C7 highest
PASS C7 sensor_faults
PASS C8 measured
PASS C8 out_of_range
PASS C8 invalid_entries
PASS C8 lowest
PASS C8 highest
PASS C8 sensor_faults
PASS C9 measured
PASS C9 out_of_range
PASS C9 invalid_entries
PASS C9 lowest
PASS C9 highest
PASS C9 sensor_faults
PASS C9 next result
PASS C9 next temperature
PASS C10 measured
PASS C10 out_of_range
PASS C10 invalid_entries
PASS C10 lowest
PASS C10 highest
PASS C10 sensor_faults
Checks: 92, failed: 0
```

Kod zakończenia: 0. Wszystkie 92 sprawdzenia przechodzą: 13 przypadków bezpośrednich po 2 sprawdzenia, 10 scenariuszy po 6 i 3 dodatkowe wywołania po 2. Program właściwy z danymi z przykładu wypisuje ten sam raport co w części B i na końcu `Sensor faults: 0`.

</details>

## Odpowiedzi do pytań z uzasadnienia

<details>
<summary>Przykładowe odpowiedzi, dla rozwiązania referencyjnego</summary>

1. Bo kontrakt mówi, co program ma robić. Wynik wzięty z działania programu powtórzyłby jego błąd: dla `100` zapisałoby się `out_of_range` i usterka przeszłaby niezauważona (lekcja 13.1).
2. Bo obie liczby leżą poza zakresem stacji, a różnią się tylko tym, czy mieszczą się w zakresie protokołu. Różnica wyniku między nimi może więc pochodzić tylko z tej reguły. `abc` nie wystarczy: daje `invalid_entry` inną drogą, przez nieudany odczyt, i przechodzi także z usterką.
3. `FAIL D7 result: expected invalid_entry, actual out_of_range` pokazuje, że dla `100` wynik rzeczywisty różni się od oczekiwanego. Sam nie rozstrzyga, czy błąd jest w funkcji, czy w oczekiwaniu: to ustala się, wracając do tabeli wyników (lekcja 13.2).
4. Bo przy `measured == 0` żaden pomiar nie został przyjęty, a `lowest` i `highest` mają tylko wartości zastępcze. C4 i C8 sprawdzają raport bez pomiarów, a C7 i D11 sprawdzają, że prawdziwe 0 jest pomiarem.
5. Bo kontrakt mówi o liczbie pomiarów, a nie prób: stacja ma zebrać sześć temperatur, nawet gdy po drodze trafią się błędne wpisy. C6 to sprawdza: przy limicie 2 dwie odmowy przed pomiarami nie mogą zakończyć zbierania.
6. W części B kontrakt się nie zmienił, więc oczekiwania z kontraktu nadal są poprawne: zmieniasz funkcję, nie test. W części C zmienił się kontrakt dla −99, więc oczekiwanie D8 musiało się zmienić. Wszystkie inne dawne oczekiwania zostają, bo nowa reguła ich nie dotyczy.
7. Bo −99 pasuje do dwóch reguł, a kontrakt ustala pierwszeństwo kodu awarii. Sprawdzenie zakresu stacji przed kodem awarii dałoby `out_of_range`. Wykrywają to D8, C9 i C10.
8. Bo testy mają sprawdzać ten sam kod, z którego korzysta program właściwy: poprawka w `rules.cpp` trafia do obu (lekcja 13.4). Wszystkie testy uruchamiasz po każdej zmianie, bo zmiana w jednym miejscu może zepsuć coś, co wcześniej działało: to sprawdzenie regresji.

</details>

## Samoocena

Przy każdej kompetencji zaznacz jedną odpowiedź:

| Kompetencja | Samodzielnie | Z podpowiedzią | Po zajrzeniu do rozwiązania | Do powtórki |
|---|---|---|---|---|
| Plan przypadków przed kodem | | | | |
| Wyniki oczekiwane z kontraktu | | | | |
| Pary, które rozstrzygają każdą regułę | | | | |
| Dwa targety i wspólny `rules.cpp` | | | | |
| `std::istringstream` i sekwencje na jednym strumieniu | | | | |
| `collect_measurements` i limit | | | | |
| Raport bez pomiarów i prawdziwe 0 | | | | |
| Wykrycie usterki przed poprawką | | | | |
| Poprawka i te same testy | | | | |
| Zmiana kontraktu i regresja | | | | |

Jeśli adaptujesz wcześniejszy kod, zapisz pod tabelą, z którego programu korzystano, co z niego przeniesiono, co zmieniono i jakie decyzje projektowe podjęto samodzielnie: przypadki, wyniki oczekiwane, wartość startowa `temperature` i sposób wykazania usterki.

Jeśli w kolumnie „Do powtórki” jest coś zaznaczone, wróć do odpowiedniej lekcji:

| Temat | Lekcja |
|---|---|
| `enum class`, nazwane stany | [14.1](lesson_01_named_state_instead_of_text.md) |
| `switch`, etykieta dla każdej wartości, `-Wswitch` | [14.2](lesson_02_handling_every_state_with_switch.md) |
| nazwany wynik, dane bez zmian po odmowie, pierwszeństwo odmowy | [14.3](lesson_03_function_explains_refusal.md) |
| `read_number`, odzyskiwanie strumienia, koniec danych, testy sekwencji | [14.4](lesson_04_reading_that_recovers_the_stream.md) |
| dwa targety, wspólny `rules.cpp`, regresja | [13.4](../module_13_testing_functions/lesson_04_tests_next_to_the_program.md) |
| przypadki, które odróżniają usterkę, plan przed kodem | [13.5](../module_13_testing_functions/lesson_05_workshop_reservations.md) |

---

## Podsumowanie Modułu 14

Po pięciu lekcjach potrafisz:

- nazywać stany i wyniki funkcji typem `enum class`, którego wartości sprawdza kompilator, zamiast tekstu albo liczb;
- obsługiwać każdy stan w jednym miejscu instrukcją `switch`, z etykietą dla każdej wartości;
- pisać funkcję, która nazwanym wynikiem mówi, dlaczego odmówiła, i po odmowie zostawia dane bez zmian;
- ustalać pierwszeństwo, gdy do jednej sytuacji pasuje kilka reguł, i sprawdzać je przypadkiem, w którym zachodzą obie;
- odczytywać dane tak, żeby błędny wpis nie blokował dalszej pracy, a koniec danych był rozpoznany przed odczytem;
- testować sekwencje wpisów na jednym strumieniu i wprowadzać zmianę kontraktu tak, że testy najpierw się nie udają, a potem wszystkie przechodzą.

## Co dalej

To koniec Modułu 14 i wszystkich jego zaplanowanych lekcji. Kolejne moduły kursu są planowane.

**Poprzednia lekcja:** [Lekcja 14.4: Spróbuj jeszcze raz: odczyt, który odzyskuje strumień](lesson_04_reading_that_recovers_the_stream.md) · [Opis kursu](../../README.md)

# Lekcja 8.6: Wyniki biegu (sprawdzian Modułu 8)

**Polski** · [English](lesson_06_race_results.en.md) · [Opis kursu](../../README.md)

> **Moduł 8, lekcja 6: sprawdzian** · około 100–115 minut, w dwóch podejściach
> **Potrzebujesz:** katalogu `cpp-workspace` i oryginalnego projektu `lesson_05_first_program`.
> **Wersja pilotażowa.** Rozwiązania referencyjne z tej lekcji sprawdzamy automatycznie na Windowsie, Ubuntu i macOS. Twojej pracy nic nie ocenia automatycznie: sprawdzasz ją samodzielnie, według kryteriów. Twój program nie pyta o dane: wszystkie wartości są zapisane w kodzie. Dane z wejścia odczytuje tylko program kontrolny z części B.

## Jak przebiega ten sprawdzian

Ta lekcja nie wprowadza niczego nowego. Sprawdzasz, czy potrafisz samodzielnie zaprojektować **własne typy danych i funkcje, które analizują kolekcję rekordów**: liczą rekordy spełniające warunki, wybierają najlepszy rekord i zwracają podsumowanie w osobnej strukturze. Do tego analizujesz dwa krótkie problemy z kodem i wyjaśniasz swoje decyzje.

Lekcja ma dwie części:

- **Część A: sprawdzian.** Wymagania, przykłady, zadania, pytania i kryteria. Bez podpowiedzi i bez kodu rozwiązań. Wszystko, czego potrzebujesz, znasz z Modułów 1–8.
- **Część B: sprawdzenie i omówienie.** Podpowiedzi, pełna lista przypadków kontrolnych, rozwiązanie referencyjne, poprawki, odpowiedzi i samoocena. Przejdź do niej po wykonaniu części A albo wtedy, gdy świadomie zrezygnujesz z dalszej samodzielnej próby.

Zajrzenie do części B, do wcześniejszych lekcji albo do notatek nie jest porażką. Ważne jest, żeby **uczciwie zanotować, co zrobiono samodzielnie, a co z pomocą**. Proponowany podział na dwa podejścia:

- **pierwsze:** analiza wymagań, projekt obu typów i obu funkcji, ich napisanie i raport dla danych z wymagań;
- **drugie:** przypadki graniczne, zadanie 2, porównanie z rozwiązaniem, zadanie 3 i samoocena.

**Możesz używać:** CLiona albo terminala, CMake i Ninja, jak dotąd; `CMakeLists.txt` skopiowanego z oryginalnego `lesson_05_first_program`; tabel przypadków i przebiegu oraz tymczasowych wydruków testowych. Debugger nie jest potrzebny.

---

# Część A: sprawdzian

## Zadanie 1: Wyniki biegu

Biuro zawodów przygotowuje raport z biegu: kto ma kwalifikację do kolejnego etapu, ile osób ukończyło bieg i kto ma najlepszy czas. Wyniki uczestników są zapisane w programie.

**Przygotowanie:** w `cpp-workspace` utwórz katalog `race_results`, skopiuj do niego `CMakeLists.txt` z oryginalnego `lesson_05_first_program`, utwórz **pusty** `main.cpp` i napisz cały program samodzielnie.

### Dane uczestników

Każdego uczestnika opisują trzy informacje: nazwa, czas biegu w sekundach i to, czy bieg został ukończony.

- Nazwa to niepusty tekst ASCII bez spacji. Nazwy uczestników w jednym wektorze są różne.
- Czas jest liczbą całkowitą. Osoba, która ukończyła bieg, ma czas od 1 do 3600 sekund.
- Osoba, która nie ukończyła biegu, ma zapisany czas 0. **To nie jest wynik sportowy:** taki czas nie może być najlepszy ani dać kwalifikacji.
- Program nie sprawdza tych założeń, nie odczytuje niczego z wejścia i nie przelicza sekund na minuty.

Dane z wymagań, w tej kolejności:

| Uczestnik | Czas w sekundach | Bieg ukończony? |
|---|---:|---|
| `Ada` | 540 | tak |
| `Bruno` | 620 | tak |
| `Cora` | 510 | tak |
| `Daniel` | 0 | nie |
| `Ewa` | 510 | tak |
| `Filip` | 600 | tak |

**Limit kwalifikacji** to największy dopuszczalny czas zakwalifikowanej osoby. W danych z wymagań wynosi 600 sekund.

### Trzy różne pojęcia

- **Ukończony bieg:** osoba ma w rekordzie informację, że ukończyła bieg. To jeszcze nie oznacza kwalifikacji.
- **Kwalifikacja:** osoba ukończyła bieg **i** ma czas mniejszy od limitu albo mu równy. Przy limicie 600 czas 600 daje kwalifikację, a 601 już nie. Osoba, która nie ukończyła biegu, nie kwalifikuje się nigdy, także z zapisanym czasem 0.
- **Najlepszy wynik:** najkrótszy czas **spośród wszystkich osób, które ukończyły bieg**, także tych bez kwalifikacji. Przy remisie wygrywa osoba, która stoi **wcześniej** w wektorze. Gdy żadna osoba nie ukończyła biegu, najlepszego wyniku nie ma.

### Raport

Program wypisuje kolejno:

- `Runners: N`: liczbę uczestników w wektorze;
- `Qualified runners:`: zawsze, także wtedy, gdy nie ma żadnej kwalifikacji;
- pod nią nazwy zakwalifikowanych osób, każdą w osobnej linijce, w kolejności z wektora, bez czasów;
- `Finishers: N`: liczbę osób, które ukończyły bieg;
- `Qualified: N`: liczbę zakwalifikowanych osób;
- `Best finisher:` z nazwą osoby z najlepszym wynikiem i jej czasem, na przykład `Best finisher: Cora (510 s)`, albo `Best finisher: none`, gdy najlepszego wyniku nie ma.

Program nie wypisuje żadnych innych komunikatów ani pustych linii.

### Typy i funkcje

- Program definiuje **dwa własne typy**: uczestnika, z trzema polami, i podsumowania biegu. Podsumowanie przechowuje pięć informacji o jednym wyniku analizy: liczbę osób, które ukończyły bieg (`std::size_t`), liczbę zakwalifikowanych osób (`std::size_t`), informację, czy znaleziono najlepszy wynik (`bool`), nazwę osoby z najlepszym wynikiem (`std::string`) i jej czas (`int`). Nazwy typów i pól wybierasz samodzielnie.
- Wszystkie pola podsumowania mają jawne wartości początkowe. Gdy najlepszego wyniku nie ma, nazwa i czas zachowują neutralne wartości początkowe, a o tym, czy wynik istnieje, decyduje pole `bool`. Program nie wypisuje wtedy nazwy ani czasu. Nie zaczynaj szukania od „bardzo dużej” liczby, na przykład 999999.
- **Funkcja dla jednego uczestnika** dostaje uczestnika przez `const&` i limit jako `int` przez wartość. Odpowiada, czy ten uczestnik ma kwalifikację: zwraca `true` albo `false`.
- **Funkcja dla całego biegu** dostaje wektor uczestników przez `const&` i limit przez wartość. Tworzy lokalne podsumowanie, liczy osoby, które ukończyły bieg, liczy zakwalifikowane osoby **przy pomocy funkcji dla jednego uczestnika**, wybiera najlepszy wynik wśród osób, które ukończyły bieg, i zwraca podsumowanie przez wartość.
- Żadna funkcja nie zmienia danych, niczego nie wypisuje ani nie odczytuje z wejścia. Nazwy funkcji i ich nagłówki zapisujesz samodzielnie. Trzecia funkcja nie jest potrzebna, ale możesz ją dodać, jeśli ma sensowne zadanie.
- **`main`** przechowuje limit w zmiennej `int`, a uczestników w jednym wektorze `const`, zainicjalizowanym w kodzie w kolejności z tabeli. Bez osobnych zmiennych na każdego uczestnika i bez `push_back`. `main` wywołuje funkcję dla całego biegu raz, liczbę uczestników bierze z `size()`, nazwy zakwalifikowanych osób wypisuje w pętli, korzystając z funkcji dla jednego uczestnika, a resztę raportu z pól podsumowania. Nie powtarza warunku kwalifikacji ani szukania najlepszego wyniku. Program nie używa zmiennych zadeklarowanych poza funkcjami.

### Przykłady

**Przykład A:** dane z wymagań, limit 600.

<!-- output: race_results -->
```text
Runners: 6
Qualified runners:
Ada
Cora
Ewa
Filip
Finishers: 5
Qualified: 4
Best finisher: Cora (510 s)
```

`Bruno` przekracza limit, choć bieg jest ukończony. `Daniel` nie ma ukończonego biegu. `Filip` ma czas równy limitowi, więc się kwalifikuje. `Cora` i `Ewa` mają ten sam najkrótszy czas, a `Cora` stoi wcześniej.

Przykłady B–D sprawdza automatycznie program kontrolny z części B, który odczytuje uczestników z wejścia: najpierw ich liczbę, potem każdego w osobnej linijce. Te dane stoją w zwiniętych blokach. W Twoim programie te same dane stoją w klamrach wektora. We wszystkich przykładach limit wynosi 600.

**Przykład B:** pusty wektor.

<details>
<summary>Dane dla programu kontrolnego</summary>

<!-- input: race_results_check -->
```text
0
```

</details>

<!-- output: race_results_check -->
```text
Runners: 0
Qualified runners:
Finishers: 0
Qualified: 0
Best finisher: none
```

**Przykład C:** dwa rekordy bez ukończonego biegu, `Dana` i `Erik`, oba z czasem 0.

<details>
<summary>Dane dla programu kontrolnego</summary>

<!-- input: race_results_check -->
```text
2
Dana 0 no
Erik 0 no
```

</details>

<!-- output: race_results_check -->
```text
Runners: 2
Qualified runners:
Finishers: 0
Qualified: 0
Best finisher: none
```

To inny przypadek niż pusty wektor: rekordy istnieją, ale żaden bieg nie jest ukończony, a czas 0 nie jest wynikiem.

**Przykład D:** `Slow` z ukończonym biegiem i czasem 700 sekund oraz `NoFinish` bez ukończonego biegu.

<details>
<summary>Dane dla programu kontrolnego</summary>

<!-- input: race_results_check -->
```text
2
Slow 700 yes
NoFinish 0 no
```

</details>

<!-- output: race_results_check -->
```text
Runners: 2
Qualified runners:
Finishers: 1
Qualified: 0
Best finisher: Slow (700 s)
```

`Slow` nie ma kwalifikacji, a mimo to ma najlepszy wynik spośród osób, które ukończyły bieg: istnienie najlepszego wyniku nie zależy od limitu.

### Jak pracować

1. **Zaprojektuj oba typy i obie funkcje, zanim zaczniesz pisać `main`.** Przy każdej funkcji zapisz jednym zdaniem jej zadanie, parametry i typ wyniku.
2. **Przygotuj tabelę przypadków:** pusty wektor; same rekordy bez ukończonego biegu; jedna osoba z kwalifikacją, jedna z ukończonym biegiem bez kwalifikacji i jedna bez ukończonego biegu; czas równy limitowi, o sekundę krótszy i o sekundę dłuższy; najlepszy wynik na początku, w środku i na końcu wektora; pierwszy rekord bez ukończonego biegu; remis i ten sam remis w odwrotnej kolejności; kilka ukończonych biegów bez żadnej kwalifikacji. Przy każdym zapisz cały oczekiwany raport.
3. Jeśli chcesz, sprawdź funkcję dla jednego uczestnika osobno, wydrukami testowymi z lekcji 5.5: czasy 599, 600 i 601 oraz rekord bez ukończonego biegu z czasem 0. Potem usuń wydruki testowe.
4. **Uruchom cały program** dla danych z wymagań (przykład A) i dla danych z przykładu D. Zmieniaj przy tym tylko zawartość klamer wektora, a na koniec przywróć dane z wymagań. Przypadki B i C przeanalizuj na papierze: prześledź, co zwróci Twoja funkcja, gdy pętla nie wykona żadnego przebiegu albo nie trafi na ukończony bieg. Wszystkie przypadki z pełnej listy kontrolnej są sprawdzone automatycznie.

Gdy wynik się zgadza, możesz zapisać projekt w Gicie, jak w lekcji 1.5. Przed commitem sprawdź `git status`: do historii trafiają tylko `main.cpp` i `CMakeLists.txt`.

## Zadanie 2: Diagnostyka

Wykonaj to zadanie **po zadaniu 1**: oba problemy dotyczą funkcji podobnych do Twoich.

<details>
<summary>Diagnostyka A: najlepszy czas zaczyna się od zera</summary>

W `cpp-workspace` utwórz katalog `diagnosis_8`, skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program` i umieść w `main.cpp` program poniżej: możesz go przepisać albo skopiować. Wymagania są takie same jak w zadaniu 1.

<!-- example: best_time_bug -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>
#include <vector>

struct Runner {
    std::string name;
    int time_seconds;
    bool finished;
};

struct RaceSummary {
    std::size_t finishers;
    std::size_t qualified;
    bool has_best;
    std::string best_name;
    int best_time;
};

bool is_qualified(const Runner& runner, int limit) {
    return runner.finished && runner.time_seconds <= limit;
}

RaceSummary summarise_race(const std::vector<Runner>& runners, int limit) {
    RaceSummary summary{0, 0, false, "", 0};

    for (const Runner& runner : runners) {
        if (runner.finished) {
            ++summary.finishers;

            if (runner.time_seconds < summary.best_time) {
                summary.has_best = true;
                summary.best_name = runner.name;
                summary.best_time = runner.time_seconds;
            }
        }

        if (is_qualified(runner, limit)) {
            ++summary.qualified;
        }
    }

    return summary;
}

int main() {
    const int limit{600};
    const std::vector<Runner> runners{
        {"Gil", 0, false},
        {"Hana", 0, false}
    };

    const RaceSummary summary{summarise_race(runners, limit)};

    std::cout << "Runners: " << runners.size() << "\n";
    std::cout << "Qualified runners:\n";

    for (const Runner& runner : runners) {
        if (is_qualified(runner, limit)) {
            std::cout << runner.name << "\n";
        }
    }

    std::cout << "Finishers: " << summary.finishers << "\n";
    std::cout << "Qualified: " << summary.qualified << "\n";

    if (summary.has_best) {
        std::cout << "Best finisher: " << summary.best_name << " (" << summary.best_time << " s)\n";
    } else {
        std::cout << "Best finisher: none\n";
    }
}
```

1. **Przewidź** standardowe wyjście dla danych z programu.
2. Uruchom program. Czy wynik zgadza się z wymaganiami?
3. Zmień dane w wektorze tak, żeby błąd stał się widoczny. Najpierw zapisz poprawny raport dla swoich danych, a potem uruchom program.
4. Prześledź wartości pól `best_time` i `has_best` po każdym przebiegu pętli.
5. Wyjaśnij, dlaczego 0 nie nadaje się na „dotychczas najlepszy” czas.
6. Co program musi wiedzieć, zanim porówna czas z dotychczas najlepszym?
7. Popraw funkcję, nie zmieniając danych.
8. Uruchom poprawiony program dla swojego wektora.
9. Przewidź wynik poprawionego programu dla remisu, dla pustego wektora i dla danych z przykładu D, a potem porównaj go z częścią B.

</details>

<details>
<summary>Diagnostyka B: zmiana rekordu przez <code>const&amp;</code></summary>

Ten fragment **tylko analizujesz na papierze**: nie uruchamiaj go. Ta wersja funkcji kwalifikującej miała sprawić, żeby osoba bez ukończonego biegu nigdy nie mieściła się w limicie. Dopisano do niej zmianę czasu:

<!-- fragment -->
```cpp
bool is_qualified(const Runner& runner, int limit) {
    if (!runner.finished) {
        runner.time_seconds = limit + 1;
    }

    return runner.time_seconds <= limit;
}
```

1. Czy program z taką funkcją powinien się zbudować?
2. Dlaczego nie?
3. Czy problemem jest typ pola `time_seconds`?
4. Co oznacza `const&` dla dostępu przez parametr?
5. Czy funkcja kwalifikująca w ogóle potrzebuje zmieniać rekord?
6. Jak usunąć błąd, nie usuwając `const`?

</details>

Wyniki, poprawki i odpowiedzi są w części B, w sekcji [Diagnostyka: wyniki i poprawki](#diagnostyka-wyniki-i-poprawki).

## Zadanie 3: Wyjaśnij swój projekt

Odpowiedz krótko, na piśmie, odwołując się do własnego programu z zadania 1:

1. Dlaczego uczestnik i podsumowanie są dwoma różnymi typami? Dlaczego limit nie jest polem uczestnika?
2. Dlaczego funkcja dla jednego uczestnika zwraca `bool`, a funkcja dla całego biegu strukturę?
3. Dlaczego najlepszy wynik wymaga osobnej informacji, czy cokolwiek znaleziono? Dlaczego osoba bez ukończonego biegu, z czasem 0, nie wygrywa?
4. Dlaczego przy remisie zostaje osoba stojąca wcześniej? Co w Twoim raporcie może zmienić zamiana kolejności uczestników, a co nie?
5. Czy zero kwalifikacji oznacza, że żadna osoba nie ukończyła biegu? Wskaż przypadek ze swojej tabeli.
6. Dlaczego żadna z Twoich funkcji nie zmienia rekordów?
7. Czy to, że liczba zakwalifikowanych osób nie przekracza liczby osób, które ukończyły bieg, dowodzi, że program działa poprawnie?

## Kryteria sukcesu

Sprawdzian jest zaliczony, gdy spełniasz **wszystkie** kryteria. Możesz przy tym korzystać z części B, jeśli uczciwie zaznaczysz to w samoocenie.

- `race_results/main.cpp` napisano od pustego pliku, w poprawnym C++20. Program buduje się bez błędów.
- Są dwa własne typy: uczestnika z trzema polami i podsumowania z pięcioma polami wymaganych typów. Wszystkie pola mają jawne wartości początkowe.
- Funkcja dla jednego uczestnika dostaje go przez `const&`, a limit przez wartość, i zwraca `bool`. Funkcja dla całego biegu dostaje wektor przez `const&`, a limit przez wartość, korzysta z funkcji dla jednego uczestnika i zwraca podsumowanie przez wartość. Żadna nie zmienia danych, niczego nie wypisuje ani nie odczytuje.
- Limit jest zmienną `int` w `main`, a uczestnicy stoją w jednym wektorze `const`, w kolejności z tabeli.
- Standardowe wyjście dla przykładów A i D zgadza się z wymaganiami. Przypadki B i C zgadzają się z Twoją analizą na papierze i z pełną listą kontrolną.
- Osoba bez ukończonego biegu nie kwalifikuje się i nie wygrywa. Czas równy limitowi daje kwalifikację. Przy remisie wygrywa osoba stojąca wcześniej. Najlepszy wynik istnieje także przy zerze kwalifikacji, jeśli jest choć jeden ukończony bieg.
- Szukanie najlepszego wyniku zaczyna się od informacji „nic jeszcze nie znaleziono”, a nie od wymyślonej liczby. Program nie odczytuje elementów, których nie ma, na przykład pierwszego elementu pustego wektora.
- Warunek kwalifikacji stoi w programie w jednym miejscu.
- Błąd z diagnostyki A poprawiono i sprawdzono, a fragment z diagnostyki B przeanalizowano bez uruchamiania.
- Umiesz wyjaśnić każdą linijkę swojego programu i odpowiedzieć na pytania z zadania 3.

Nazwy typów, pól, funkcji i zmiennych oraz podział programu mogą być inne niż w rozwiązaniu referencyjnym, jeśli są czytelne i spełniają wymagania. Poprawny wynik to warunek konieczny, ale **nie dowód zrozumienia**. Dlatego zadania 2 i 3 są częścią sprawdzianu.

---

# Część B: sprawdzenie i omówienie

Przejdź tutaj po wykonaniu części A albo wtedy, gdy świadomie zrezygnujesz z dalszej samodzielnej próby.

## Jak sprawdzić swoją pracę

- **Standardowe wyjście:** porównaj linijki programu z oczekiwanymi, znak po znaku, także nazwy pod `Qualified runners:` i ich kolejność.
- **Przypadki graniczne:** pusty wektor i wektor bez ukończonych biegów sprawdź tabelą przebiegu i porównaj z pełną listą kontrolną. Każdy przypadek jest tam sprawdzony automatycznie.
- **Funkcje:** czy każda ma zadanie, które da się opisać jednym zdaniem? Czy warunek kwalifikacji albo szukanie najlepszego wyniku stoi też w `main`?
- **Logika wyników:** zależności opisane przy rozwiązaniu referencyjnym pomagają wyłapać błąd, ale nie zastępują przypadków z oczekiwanymi raportami.

## Podpowiedzi

<details>
<summary>Podpowiedź 1</summary>

Jakie informacje opisują jednego uczestnika, a jakie dotyczą całego biegu? Czy powinny należeć do tego samego typu?

</details>

<details>
<summary>Podpowiedź 2</summary>

Funkcja dla jednego uczestnika odpowiada na pytanie o kwalifikację. Funkcja dla całej kolekcji może policzyć ukończone biegi i kwalifikacje oraz zachować informacje o najlepszym ukończonym wyniku.

</details>

<details>
<summary>Podpowiedź 3</summary>

Nie zakładaj, że istnieje pierwszy ukończony bieg. Przy szukaniu najlepszego czasu potrzebujesz rozpoznać pierwszego poprawnego kandydata. Późniejszy kandydat zastępuje go tylko wtedy, gdy ma ściśle krótszy czas.

</details>

## Pełna lista przypadków kontrolnych

<details>
<summary>Otwórz po przygotowaniu własnej tabeli</summary>

Przykłady A–D są w części A. We wszystkich przypadkach limit wynosi 600, a „nie” oznacza bieg nieukończony, z czasem 0.

| | Uczestnicy (czas w sekundach) | Zakwalifikowane osoby | Finishers | Qualified | Best finisher | Co sprawdza |
|---|---|---|---:|---:|---|---|
| A | dane z wymagań | `Ada`, `Cora`, `Ewa`, `Filip` | 5 | 4 | `Cora (510 s)` | remis, czas równy limitowi, czas 0 nie wygrywa |
| B | brak | brak | 0 | 0 | `none` | pusty wektor |
| C | `Dana` nie, `Erik` nie | brak | 0 | 0 | `none` | rekordy bez ukończonych biegów |
| D | `Slow` 700, `NoFinish` nie | brak | 1 | 0 | `Slow (700 s)` | najlepszy wynik bez kwalifikacji |
| E | `Solo` 450 | `Solo` | 1 | 1 | `Solo (450 s)` | jedna osoba z kwalifikacją |
| F | `Late` 601 | brak | 1 | 0 | `Late (601 s)` | jedna osoba, sekunda ponad limit |
| G | `Quit` nie | brak | 0 | 0 | `none` | jeden rekord bez ukończonego biegu |
| H | `Edge` 600, `Under` 599, `Over` 601 | `Edge`, `Under` | 3 | 2 | `Under (599 s)` | limit i sekunda obok niego; najlepszy w środku |
| I | `Fast` 300, `Mid` 400, `Last` 500 | `Fast`, `Mid`, `Last` | 3 | 3 | `Fast (300 s)` | najlepszy na początku; kilka kwalifikacji |
| J | `Out` nie, `Mid` 400, `Fast` 300 | `Mid`, `Fast` | 2 | 2 | `Fast (300 s)` | pierwszy rekord bez ukończonego biegu; najlepszy na końcu |
| K | `Ewa` 510, `Cora` 510 | `Ewa`, `Cora` | 2 | 2 | `Ewa (510 s)` | remis w odwrotnej kolejności |
| L | `Slow` 700, `Slower` 900, `Late` 601 | brak | 3 | 0 | `Late (601 s)` | kilka ukończonych biegów, zero kwalifikacji |

**Testy automatyczne i Twoje próby.** Wszystkie przypadki są sprawdzone automatycznie przez program kontrolny. Ma on te same typy, te same funkcje i ten sam raport co rozwiązanie referencyjne, ale uczestników odczytuje z wejścia. To tylko narzędzie do sprawdzania, a nie część misji: w misji wektor jest zapisany w kodzie. Program kontrolny i jego wyniki są przy [rozwiązaniu referencyjnym](#rozwiązanie-referencyjne), bo zawierają rozwiązanie.

</details>

## Rozwiązanie referencyjne

Porównaj je ze swoim programem po zakończeniu części A. Nazwy, kolejność pól i drobne decyzje mogą być inne, jeśli raport jest taki sam dla wszystkich przypadków z listy kontrolnej.

<details>
<summary>Zadanie 1: wyniki biegu</summary>

<!-- example: race_results -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>
#include <vector>

struct Runner {
    std::string name;
    int time_seconds;
    bool finished;
};

struct RaceSummary {
    std::size_t finishers;
    std::size_t qualified;
    bool has_best;
    std::string best_name;
    int best_time;
};

bool is_qualified(const Runner& runner, int limit) {
    return runner.finished && runner.time_seconds <= limit;
}

RaceSummary summarise_race(const std::vector<Runner>& runners, int limit) {
    RaceSummary summary{0, 0, false, "", 0};

    for (const Runner& runner : runners) {
        if (runner.finished) {
            ++summary.finishers;

            if (!summary.has_best || runner.time_seconds < summary.best_time) {
                summary.has_best = true;
                summary.best_name = runner.name;
                summary.best_time = runner.time_seconds;
            }
        }

        if (is_qualified(runner, limit)) {
            ++summary.qualified;
        }
    }

    return summary;
}

int main() {
    const int limit{600};
    const std::vector<Runner> runners{
        {"Ada", 540, true},
        {"Bruno", 620, true},
        {"Cora", 510, true},
        {"Daniel", 0, false},
        {"Ewa", 510, true},
        {"Filip", 600, true}
    };

    const RaceSummary summary{summarise_race(runners, limit)};

    std::cout << "Runners: " << runners.size() << "\n";
    std::cout << "Qualified runners:\n";

    for (const Runner& runner : runners) {
        if (is_qualified(runner, limit)) {
            std::cout << runner.name << "\n";
        }
    }

    std::cout << "Finishers: " << summary.finishers << "\n";
    std::cout << "Qualified: " << summary.qualified << "\n";

    if (summary.has_best) {
        std::cout << "Best finisher: " << summary.best_name << " (" << summary.best_time << " s)\n";
    } else {
        std::cout << "Best finisher: none\n";
    }
}
```

1. **Dwa typy danych,** bo opisują różne rzeczy: `Runner` to jeden uczestnik, a `RaceSummary` to wynik analizy całego biegu.
2. **Limit jako osobny argument,** bo to wspólna zasada biegu, a nie cecha uczestnika. Jako pole powtarzałby się w każdym rekordzie i mógłby się różnić między rekordami.
3. **Rekord przez `const&`,** bo funkcje tylko go czytają: bez kopii i bez możliwości zmiany.
4. **`is_qualified` zwraca `bool`,** bo odpowiada na pytanie tak albo nie.
5. **`summarise_race` zwraca strukturę,** bo jedna analiza daje pięć powiązanych informacji.
6. **Bez ukończonego biegu nie ma kwalifikacji:** warunek zaczyna się od `runner.finished`, więc czas 0 nie ma znaczenia.
7. **Czas 0 nie jest wynikiem,** tylko zapisem nieukończonego biegu. Gdyby wchodził do porównań, wygrałby z każdym prawdziwym czasem.
8. **Najlepszego szukamy tylko wśród ukończonych biegów,** bo tylko one mają prawdziwy czas. Całe szukanie stoi wewnątrz `if (runner.finished)`.
9. **Najpierw trzeba wiedzieć, czy kandydat już istnieje,** bo wektor może być pusty albo nie mieć żadnego ukończonego biegu. Nie ma też „pierwszego elementu”, który można by przyjąć z góry.
10. **Pierwszy ukończony bieg:** dopóki `has_best` ma wartość `false`, warunek `!summary.has_best` jest prawdziwy, więc pierwszy ukończony bieg zostaje kandydatem bez porównywania. Dzięki krótkiemu obliczaniu z lekcji 3.4 porównanie z wartością początkową 0 nie jest wtedy w ogóle obliczane.
11. **Późniejsze porównania:** gdy kandydat już jest, nowy bieg zastępuje go tylko przy `runner.time_seconds < summary.best_time`. Nazwa i czas zmieniają się zawsze razem.
12. **Remis nie zastępuje wcześniejszego kandydata,** bo porównanie jest ścisłe: równy czas nie jest krótszy. Tak samo w lekcji 6.3 zostawał pierwszy największy spadek.
13. **Pusty wektor:** pętla nie wykona przebiegu, więc zostają wartości początkowe: zera i `has_best` równe `false`. Program wypisuje `none` i nie odczytuje żadnego elementu.
14. **Brak ukończonych biegów:** pętla przechodzi przez rekordy, ale nigdy nie wchodzi do `if (runner.finished)`, więc `has_best` zostaje `false`.
15. **Najlepszy wynik przy zerze kwalifikacji:** szukanie najlepszego nie zależy od limitu, więc w przykładzie D `Slow` wygrywa, choć nie ma kwalifikacji.
16. **`summarise_race` korzysta z `is_qualified`,** więc warunek kwalifikacji stoi w programie raz. `main` też go nie powtarza.
17. **Drugie przejście w `main`:** podsumowanie nie przechowuje listy nazw, więc `main` przegląda wektor jeszcze raz i wypisuje zakwalifikowane osoby w kolejności z wektora. Decyzję podejmuje `is_qualified`, a `main` tylko wypisuje.
18. **Bez referencji modyfikowalnych,** bo nic nie zmienia uczestników: wynik powstaje w lokalnym podsumowaniu.
19. **Bez `std::vector<std::string>`,** bo nazwy zakwalifikowanych osób da się wypisać od razu, w drugim przejściu po uczestnikach.
20. **Ten sam model pasuje do innych danych:** typ rekordu, funkcja z decyzją dla jednego rekordu, funkcja dla kolekcji zwracająca podsumowanie z flagą „znaleziono” i wybór najlepszego rekordu ścisłym porównaniem.

**Zależności między wynikami** to dodatkowa kontrola logiki, a nie zamiennik przypadków z oczekiwanymi raportami:

- **A.** Zakwalifikowanych osób nie może być więcej niż osób, które ukończyły bieg.
- **B.** Osób, które ukończyły bieg, nie może być więcej niż uczestników.
- **C.** Osoba bez ukończonego biegu nie może mieć najlepszego wyniku.
- **D.** Jeśli jest choć jedna kwalifikacja, najlepszy wynik też mieści się w limicie: nie jest dłuższy od czasu zakwalifikowanej osoby.
- **E.** Jeśli nie ma ukończonych biegów, nie ma też najlepszego wyniku.
- **F.** Jeśli nie ma kwalifikacji, najlepszy wynik nadal może istnieć.

**Inne poprawne rozwiązania:** zamiast `!summary.has_best || ...` można osobno obsłużyć pierwszy ukończony bieg w `if` i `else`. Kolejność pól i nazwy mogą być inne. Kwalifikację można też liczyć wewnątrz `if (runner.finished)`, jeśli nadal służy do tego `is_qualified`.

**Program kontrolny** sprawdza wszystkie przypadki z listy kontrolnej. Typy i funkcje są takie same jak wyżej, a raport od odebrania wyniku też, poza wcięciem. Różnica jest jedna: wektor nie jest zapisany w kodzie, tylko powstaje z wejścia. Program odczytuje liczbę uczestników, a potem każdego uczestnika: nazwę, czas oraz `yes` albo `no` dla ukończenia biegu, zamienione na `bool` porównaniem, jak w lekcji 3.4. Każdy odczytany uczestnik trafia na koniec wektora przez `push_back`, jak w programach kontrolnych lekcji 8.4 i 8.5. Misja nie potrzebuje ani wejścia, ani `push_back`.

<!-- example: race_results_check -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>
#include <vector>

struct Runner {
    std::string name;
    int time_seconds;
    bool finished;
};

struct RaceSummary {
    std::size_t finishers;
    std::size_t qualified;
    bool has_best;
    std::string best_name;
    int best_time;
};

bool is_qualified(const Runner& runner, int limit) {
    return runner.finished && runner.time_seconds <= limit;
}

RaceSummary summarise_race(const std::vector<Runner>& runners, int limit) {
    RaceSummary summary{0, 0, false, "", 0};

    for (const Runner& runner : runners) {
        if (runner.finished) {
            ++summary.finishers;

            if (!summary.has_best || runner.time_seconds < summary.best_time) {
                summary.has_best = true;
                summary.best_name = runner.name;
                summary.best_time = runner.time_seconds;
            }
        }

        if (is_qualified(runner, limit)) {
            ++summary.qualified;
        }
    }

    return summary;
}

int main() {
    const int limit{600};
    std::vector<Runner> runners{};
    int count{0};

    std::cin >> count;

    for (int number{1}; number <= count; ++number) {
        std::string name{};
        int time_seconds{0};
        std::string finished_answer{};

        std::cin >> name;
        std::cin >> time_seconds;
        std::cin >> finished_answer;

        const Runner runner{name, time_seconds, finished_answer == "yes"};
        runners.push_back(runner);
    }

    if (std::cin.fail()) {
        std::cout << "Input could not be read\n";
    } else {
        const RaceSummary summary{summarise_race(runners, limit)};

        std::cout << "Runners: " << runners.size() << "\n";
        std::cout << "Qualified runners:\n";

        for (const Runner& runner : runners) {
            if (is_qualified(runner, limit)) {
                std::cout << runner.name << "\n";
            }
        }

        std::cout << "Finishers: " << summary.finishers << "\n";
        std::cout << "Qualified: " << summary.qualified << "\n";

        if (summary.has_best) {
            std::cout << "Best finisher: " << summary.best_name << " (" << summary.best_time << " s)\n";
        } else {
            std::cout << "Best finisher: none\n";
        }
    }
}
```

Każdy przypadek zaczyna się od liczby uczestników. Potem każdy uczestnik zajmuje jedną linijkę: nazwa, czas oraz `yes` albo `no` dla ukończenia biegu. Przypadki B–D są przy przykładach w części A. Pozostałe stoją niżej, w kolejności z listy kontrolnej: najpierw A, potem od E do L.

<!-- input: race_results_check -->
```text
6
Ada 540 yes
Bruno 620 yes
Cora 510 yes
Daniel 0 no
Ewa 510 yes
Filip 600 yes
```

<!-- output: race_results_check -->
```text
Runners: 6
Qualified runners:
Ada
Cora
Ewa
Filip
Finishers: 5
Qualified: 4
Best finisher: Cora (510 s)
```

<!-- input: race_results_check -->
```text
1
Solo 450 yes
```

<!-- output: race_results_check -->
```text
Runners: 1
Qualified runners:
Solo
Finishers: 1
Qualified: 1
Best finisher: Solo (450 s)
```

<!-- input: race_results_check -->
```text
1
Late 601 yes
```

<!-- output: race_results_check -->
```text
Runners: 1
Qualified runners:
Finishers: 1
Qualified: 0
Best finisher: Late (601 s)
```

<!-- input: race_results_check -->
```text
1
Quit 0 no
```

<!-- output: race_results_check -->
```text
Runners: 1
Qualified runners:
Finishers: 0
Qualified: 0
Best finisher: none
```

<!-- input: race_results_check -->
```text
3
Edge 600 yes
Under 599 yes
Over 601 yes
```

<!-- output: race_results_check -->
```text
Runners: 3
Qualified runners:
Edge
Under
Finishers: 3
Qualified: 2
Best finisher: Under (599 s)
```

<!-- input: race_results_check -->
```text
3
Fast 300 yes
Mid 400 yes
Last 500 yes
```

<!-- output: race_results_check -->
```text
Runners: 3
Qualified runners:
Fast
Mid
Last
Finishers: 3
Qualified: 3
Best finisher: Fast (300 s)
```

<!-- input: race_results_check -->
```text
3
Out 0 no
Mid 400 yes
Fast 300 yes
```

<!-- output: race_results_check -->
```text
Runners: 3
Qualified runners:
Mid
Fast
Finishers: 2
Qualified: 2
Best finisher: Fast (300 s)
```

<!-- input: race_results_check -->
```text
2
Ewa 510 yes
Cora 510 yes
```

<!-- output: race_results_check -->
```text
Runners: 2
Qualified runners:
Ewa
Cora
Finishers: 2
Qualified: 2
Best finisher: Ewa (510 s)
```

<!-- input: race_results_check -->
```text
3
Slow 700 yes
Slower 900 yes
Late 601 yes
```

<!-- output: race_results_check -->
```text
Runners: 3
Qualified runners:
Finishers: 3
Qualified: 0
Best finisher: Late (601 s)
```

</details>

## Diagnostyka: wyniki i poprawki

<details>
<summary>Diagnostyka A: najlepszy czas zaczyna się od zera</summary>

Przed poprawką, dla danych z programu:

<!-- output: best_time_bug -->
```text
Runners: 2
Qualified runners:
Finishers: 0
Qualified: 0
Best finisher: none
```

- **Wynik wygląda poprawnie,** bo żaden bieg nie jest ukończony: do porównania czasów w ogóle nie dochodzi. Poprawny program wypisałby to samo. Tak samo zachowuje się pusty wektor.
- **Dane, które ujawniają błąd:** każde z co najmniej jednym ukończonym biegiem. Na przykład dopisanie `{"Ivo", 580, true}`. Poprawny raport to `Ivo` na liście, 1, 1 i `Best finisher: Ivo (580 s)`. Program z błędem wypisuje:

<!-- example: best_time_revealed -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>
#include <vector>

struct Runner {
    std::string name;
    int time_seconds;
    bool finished;
};

struct RaceSummary {
    std::size_t finishers;
    std::size_t qualified;
    bool has_best;
    std::string best_name;
    int best_time;
};

bool is_qualified(const Runner& runner, int limit) {
    return runner.finished && runner.time_seconds <= limit;
}

RaceSummary summarise_race(const std::vector<Runner>& runners, int limit) {
    RaceSummary summary{0, 0, false, "", 0};

    for (const Runner& runner : runners) {
        if (runner.finished) {
            ++summary.finishers;

            if (runner.time_seconds < summary.best_time) {
                summary.has_best = true;
                summary.best_name = runner.name;
                summary.best_time = runner.time_seconds;
            }
        }

        if (is_qualified(runner, limit)) {
            ++summary.qualified;
        }
    }

    return summary;
}

int main() {
    const int limit{600};
    const std::vector<Runner> runners{
        {"Gil", 0, false},
        {"Hana", 0, false},
        {"Ivo", 580, true}
    };

    const RaceSummary summary{summarise_race(runners, limit)};

    std::cout << "Runners: " << runners.size() << "\n";
    std::cout << "Qualified runners:\n";

    for (const Runner& runner : runners) {
        if (is_qualified(runner, limit)) {
            std::cout << runner.name << "\n";
        }
    }

    std::cout << "Finishers: " << summary.finishers << "\n";
    std::cout << "Qualified: " << summary.qualified << "\n";

    if (summary.has_best) {
        std::cout << "Best finisher: " << summary.best_name << " (" << summary.best_time << " s)\n";
    } else {
        std::cout << "Best finisher: none\n";
    }
}
```

<!-- output: best_time_revealed -->
```text
Runners: 3
Qualified runners:
Ivo
Finishers: 1
Qualified: 1
Best finisher: none
```

| Po przebiegu dla | Porównanie w programie z błędem | `best_time` | `has_best` |
|---|---|---:|---|
| `Gil`, bieg nieukończony | brak | 0 | `false` |
| `Hana`, bieg nieukończony | brak | 0 | `false` |
| `Ivo`, 580 | `580 < 0` daje `false` | 0 | `false` |

- **Przyczyna:** wartość początkowa 0 udaje dotychczas najlepszy czas, choć żadnego czasu jeszcze nie było. Każdy prawdziwy czas jest dodatni, więc nigdy nie jest mniejszy od 0, a pierwszy kandydat nigdy się nie pojawia. Raport sam sobie przeczy: `Finishers: 1`, a najlepszego wyniku brak (zależność E). W lekcji 6.1 największy opad mógł zaczynać od 0, bo opady były nieujemne, a pusty wektor był poza zakresem misji. Przy szukaniu najkrótszego czasu ten sam start zawodzi.
- **Co program musi wiedzieć:** czy ma już jakiegokolwiek kandydata. Tę informację przechowuje `has_best`, ale program z błędem nie używa jej przy porównaniu.
- **Poprawka:** pierwszy ukończony bieg zostaje kandydatem bez porównania, a dopiero następne porównujemy z nim: `if (!summary.has_best || runner.time_seconds < summary.best_time)`.

<!-- example: best_time_fixed -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>
#include <vector>

struct Runner {
    std::string name;
    int time_seconds;
    bool finished;
};

struct RaceSummary {
    std::size_t finishers;
    std::size_t qualified;
    bool has_best;
    std::string best_name;
    int best_time;
};

bool is_qualified(const Runner& runner, int limit) {
    return runner.finished && runner.time_seconds <= limit;
}

RaceSummary summarise_race(const std::vector<Runner>& runners, int limit) {
    RaceSummary summary{0, 0, false, "", 0};

    for (const Runner& runner : runners) {
        if (runner.finished) {
            ++summary.finishers;

            if (!summary.has_best || runner.time_seconds < summary.best_time) {
                summary.has_best = true;
                summary.best_name = runner.name;
                summary.best_time = runner.time_seconds;
            }
        }

        if (is_qualified(runner, limit)) {
            ++summary.qualified;
        }
    }

    return summary;
}

int main() {
    const int limit{600};
    const std::vector<Runner> runners{
        {"Gil", 0, false},
        {"Hana", 0, false},
        {"Ivo", 580, true}
    };

    const RaceSummary summary{summarise_race(runners, limit)};

    std::cout << "Runners: " << runners.size() << "\n";
    std::cout << "Qualified runners:\n";

    for (const Runner& runner : runners) {
        if (is_qualified(runner, limit)) {
            std::cout << runner.name << "\n";
        }
    }

    std::cout << "Finishers: " << summary.finishers << "\n";
    std::cout << "Qualified: " << summary.qualified << "\n";

    if (summary.has_best) {
        std::cout << "Best finisher: " << summary.best_name << " (" << summary.best_time << " s)\n";
    } else {
        std::cout << "Best finisher: none\n";
    }
}
```

<!-- output: best_time_fixed -->
```text
Runners: 3
Qualified runners:
Ivo
Finishers: 1
Qualified: 1
Best finisher: Ivo (580 s)
```

Poprawiona funkcja jest taka sama jak w rozwiązaniu referencyjnym, więc pozostałe sprawdzenia z kroku 9 pokrywa program kontrolny z tą samą funkcją. Remis daje osobę stojącą wcześniej (przypadki A i K), pusty wektor daje `none` (przypadek B), a dla przykładu D wynik to `Slow (700 s)`. Dla danych bez ukończonego biegu poprawiony program wypisuje to samo co przed poprawką.

</details>

<details>
<summary>Diagnostyka B: zmiana rekordu przez <code>const&amp;</code></summary>

1. Nie. Clang zgłasza `cannot assign to variable 'runner' with const-qualified type 'const Runner &'`.
2. Bo funkcja dostaje uczestnika przez `const&`, a przypisanie próbuje zmienić jego pole.
3. Nie. `time_seconds` to zwykłe pole `int`. Problemem jest dostęp przez parametr `const`, jak w lekcjach 8.3 i 8.4.
4. Że funkcja ma dostęp do istniejącego uczestnika tylko do odczytu, bez kopii. Przez ten parametr nie zmieni żadnego pola.
5. Nie. Funkcja odpowiada na pytanie, a nie poprawia dane. Zmiana czasu zniszczyłaby też informację, którą raport czyta później.
6. Zapisz regułę jako warunek, bez zmiany rekordu: `return runner.finished && runner.time_seconds <= limit;`. Osoba bez ukończonego biegu odpada już na pierwszej części warunku.

</details>

## Odpowiedzi do zadania 3

<details>
<summary>Przykładowe odpowiedzi</summary>

1. Bo uczestnik to dane jednej osoby, a podsumowanie to wynik analizy całego biegu: mają inne pola i inne zadania. Limit to wspólna zasada kwalifikacji, a nie cecha osoby, więc należy do wywołania funkcji, a nie do rekordu.
2. Bo kwalifikacja to pytanie tak albo nie o jedną osobę. Analiza całego biegu daje kilka powiązanych informacji naraz, więc zwraca je w jednym rekordzie.
3. Bo wektor może być pusty albo nie mieć żadnego ukończonego biegu, a wtedy najlepszego wyniku nie ma, choć pola nazwy i czasu mają jakieś wartości początkowe. Czas 0 oznacza nieukończony bieg, więc w ogóle nie bierze udziału w szukaniu najlepszego.
4. Bo przy ścisłym porównaniu równy czas nie zastępuje kandydata, którego program już zapamiętał. Zamiana kolejności nie zmienia liczb ani najlepszego czasu, ale przy remisie może zmienić nazwę osoby z najlepszym wynikiem, a także kolejność nazw na liście zakwalifikowanych.
5. Nie. W przykładzie D `Slow` przekracza limit, choć bieg jest ukończony. Zero kwalifikacji przy co najmniej jednym ukończonym biegu oznacza, że najlepszy wynik istnieje, tylko nie mieści się w limicie.
6. Bo obie tylko odpowiadają na pytania o dane. Dostają rekordy przez `const&`, a wynik budują w lokalnym podsumowaniu, więc dane wejściowe zostają takie, jak w kodzie.
7. Nie. To tylko zgodność między dwiema liczbami. Program z diagnostyki A spełnia ją, a mimo to podaje zły najlepszy wynik. Poprawność sprawdzają dopiero przypadki z oczekiwanymi raportami.

</details>

## Samoocena

Przy każdym kryterium zaznacz jedną odpowiedź:

| Kryterium | Samodzielnie | Z podpowiedzią | Po zajrzeniu do rozwiązania | Do powtórki |
|---|---|---|---|---|
| Projekt typu uczestnika | | | | |
| Projekt typu podsumowania i wartości początkowe | | | | |
| Wektor uczestników zainicjalizowany w kodzie | | | | |
| Funkcja kwalifikująca: `const&` i limit przez wartość | | | | |
| Funkcja dla całego biegu zwracająca podsumowanie | | | | |
| Ukończenie, kwalifikacja i najlepszy wynik jako trzy różne pojęcia | | | | |
| Wybór najlepszego wyniku z flagą „znaleziono” | | | | |
| Remis i kolejność uczestników | | | | |
| Pusty wektor i brak ukończonych biegów | | | | |
| Lista zakwalifikowanych osób w kolejności | | | | |
| Tabela przypadków | | | | |
| Diagnostyka A (najlepszy czas od zera) | | | | |
| Diagnostyka B (zmiana rekordu przez `const&`) | | | | |
| Wyjaśnienia z zadania 3 | | | | |

Jeśli w kolumnie „Do powtórki” jest coś zaznaczone, wróć do odpowiedniej lekcji:

| Temat | Lekcja |
|---|---|
| definicja struktury, pola i inicjalizacja | [8.1](lesson_01_first_struct.md) |
| zmiana pól i niezależne kopie | [8.2](lesson_02_changing_fields_and_copies.md) |
| funkcje, które dostają rekord przez `const&` | [8.3](lesson_03_functions_that_analyse_a_record.md) |
| wektor rekordów i funkcja dla całej kolekcji | [8.4](lesson_04_many_records_in_a_vector.md) |
| funkcja zwracająca rekord z kilkoma wynikami | [8.5](lesson_05_a_function_returns_a_record.md) |
| szukanie największej wartości i remis | [6.1](../module_06_collections/lesson_01_the_first_vector.md), [6.3](../module_06_collections/lesson_03_positions_and_neighbours.md) |
| wektor jako parametr `const&` i dodatkowy parametr przez wartość | [6.4](../module_06_collections/lesson_04_a_vector_as_a_parameter.md) |
| krótkie obliczanie `&&` i `\|\|` | [3.4](../module_03_decisions_and_conditions/lesson_04_combining_conditions.md) |

Potem spróbuj zadania jeszcze raz, na przykład dla zawodów, w których wygrywa najdłuższy skok, a osoba bez ważnej próby ma zapisane 0.

---

## Podsumowanie Modułu 8

Po sześciu lekcjach potrafisz:

- definiować własne typy danych, `struct`, z polami różnych typów i inicjalizować wszystkie pola w `{}`;
- odczytywać i zmieniać pola obiektu oraz tworzyć niezależne kopie rekordów;
- pisać funkcje, które dostają rekord albo wektor rekordów przez `const&` i zwracają liczbę, odpowiedź `bool` albo cały rekord z kilkoma wynikami;
- przechowywać wiele rekordów w `std::vector` i przeglądać je pętlą zakresową przez `const&`, bez kopiowania i bez zmieniania;
- oddzielać dane wejściowe od wyniku analizy, a obliczenia od wypisywania;
- wybierać najlepszy rekord z kolekcji, także wtedy, gdy kandydata może nie być albo gdy występuje remis.

Struktury mają jeszcze wiele możliwości, które poznasz w dalszych modułach.

## Co dalej

W Module 9, „Kontrolowana zmiana danych: referencje modyfikowalne”, funkcje zaczną świadomie zmieniać istniejące rekordy. Zacznij od pierwszej lekcji: [Lekcja 9.1: Funkcja zmienia istniejący rekord](../module_09_mutable_references/lesson_01_a_function_changes_a_record.md).

**Poprzednia lekcja:** [Lekcja 8.5: Funkcja zwraca rekord z kilkoma wynikami](lesson_05_a_function_returns_a_record.md) · **Następna lekcja:** [Lekcja 9.1: Funkcja zmienia istniejący rekord](../module_09_mutable_references/lesson_01_a_function_changes_a_record.md) · [Opis kursu](../../README.md)

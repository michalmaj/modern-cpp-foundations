# Lekcja 6.2: Dodawanie danych do wektora: `push_back()` i `empty()`

**Polski** · [English](lesson_02_adding_to_a_vector.en.md) · [Opis kursu](../../README.md)

> **Moduł 6, lekcja 2** · około 75–90 minut, można ją podzielić na dwa podejścia
> **Potrzebujesz:** katalogu `cpp-workspace` i oryginalnego projektu `lesson_05_first_program`, jak dotąd. Debugger nie jest w tej lekcji potrzebny.
> **Wersja pilotażowa.** Programy z tej lekcji sprawdzamy automatycznie na Windowsie, Ubuntu i macOS, także z podanymi danymi wejściowymi. Wpisywanie danych w oknie **Run** CLiona opisujemy bez ręcznego sprawdzenia na każdym systemie.

## Zanim zaczniesz

Ta lekcja zakłada, że po lekcji 6.1 i wcześniejszych modułach:

- tworzysz `std::vector<int>` z wartościami początkowymi i przeglądasz go pętlą zakresową `for`;
- odczytujesz liczbę elementów przez `size()` i przechodzisz po wektorze drugi raz, gdy potrzebujesz wyniku pierwszego przejścia;
- sprawdzasz przez `std::cin.fail()`, czy odczyt się udał, i wiesz, że po nieudanym odczycie kolejne odczyty też się nie udają (lekcje 4.5 i 4.6);
- odczytujesz ustaloną liczbę wartości w pętli z licznikiem, jak w lekcjach 4.7 i 5.7;
- pamiętasz, że dzielenie dwóch liczb całkowitych daje liczbę całkowitą (lekcje 2.4 i 2.5).

## Sytuacja

W lekcji 6.1 wszystkie elementy wektora były znane, zanim program się uruchomił:

<!-- fragment -->
```cpp
const std::vector<int> measurements{3, 7, 5, 9};
```

Co, jeśli pomiary poda użytkownik dopiero podczas działania programu? Nie będziesz zmieniać kodu źródłowego po każdym nowym pomiarze. Potrzebujesz wektora, który na początku jest pusty i **przyjmuje kolejne elementy w trakcie działania programu**.

Po tej lekcji będziesz:

- tworzyć pusty wektor, do którego można dodawać elementy, i wyjaśniać, dlaczego nie ma on `const`;
- dodawać elementy na koniec wektora przez `push_back()` i przewidywać ich kolejność;
- sprawdzać przez `empty()`, czy wektor ma jakiekolwiek elementy;
- zapisywać w wektorze wartości odczytane z wejścia, tylko po udanym odczycie;
- odróżniać liczbę prób odczytu od liczby zapisanych elementów;
- liczyć średnią zapisanych wartości bez dzielenia całkowitego i tylko wtedy, gdy są jakieś dane;
- samodzielnie projektować program, który zapisuje tylko dane spełniające wymagania.

## 1. Przygotuj projekt

W `cpp-workspace` utwórz katalog `lesson_6_2` i skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program`. Programy z punktów 2–7 wpisujesz w `main.cpp` tego katalogu.

## 2. Pusty wektor, który będzie się zmieniał

<!-- fragment -->
```cpp
std::vector<int> measurements{};
```

- Typ elementów nadal jest `int`.
- Puste `{}` tworzą wektor bez elementów: `size()` daje 0.
- **Nie ma `const`**, bo ten wektor będzie się zmieniał: program dopisze do niego elementy.

To nie jest nowa ogólna zasada. Wektor, którego program nie zmienia, nadal oznaczasz `const`, jak w lekcji 6.1. `const` pomija się tylko tam, gdzie zmiana jest częścią zadania.

## 3. Dodawanie na koniec: `push_back()`

<!-- example: push_three -->
```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<int> measurements{};
    std::cout << "Stored: " << measurements.size() << "\n";

    measurements.push_back(3);
    std::cout << "Stored: " << measurements.size() << "\n";

    measurements.push_back(7);
    measurements.push_back(5);
    std::cout << "Stored: " << measurements.size() << "\n";

    for (const int measurement : measurements) {
        std::cout << measurement << "\n";
    }
}
```

**Przewidź** wszystkie linijki standardowego wyjścia, także kolejność elementów na końcu. Potem uruchom program.

<details>
<summary>Standardowe wyjście</summary>

<!-- output: push_three -->
```text
Stored: 0
Stored: 1
Stored: 3
3
7
5
```

</details>

`measurements.push_back(3)` to wywołanie funkcji składowej wektora, jak `size()`. W nawiasach stoi wartość, którą program **dodaje na koniec** wektora. Zawartość wektora zmienia się tak:

| Moment | Zawartość | `size()` |
|---|---|---|
| po utworzeniu | `{}` | 0 |
| po `push_back(3)` | `{3}` | 1 |
| po `push_back(7)` | `{3, 7}` | 2 |
| po `push_back(5)` | `{3, 7, 5}` | 3 |

- **`push_back` to nie przypisanie.** `x = 5;` zastępuje poprzednią wartość zmiennej. `push_back(5)` **dopisuje** nowy element, a wcześniejsze elementy zostają.
- **Nowy element trafia zawsze na koniec**, więc kolejność elementów to kolejność wywołań `push_back`.
- **Wektor nie musi znać końcowej liczby elementów**, gdy go tworzysz. `size()` rośnie o 1 przy każdym `push_back`.
- **Pętla zakresowa jest taka sama jak w 6.1.** Zmieniło się tylko to, skąd wzięły się elementy.

**Przewidź**, czy ten program się zbuduje:

<!-- broken: push_to_const at=7:18 errors=1 error=^no matching member function for call to 'push_back'$ -->
```cpp
#include <iostream>
#include <vector>

int main() {
    const std::vector<int> measurements{};

    measurements.push_back(3);

    std::cout << "Measurements stored: " << measurements.size() << "\n";
}
```

<details>
<summary>Co zgłasza kompilator i dlaczego</summary>

Program się nie zbuduje. Kompilator zgłasza w linijce 7 `no matching member function for call to 'push_back'`, a w kolejnych linijkach `note:` dodaje, że wektor jest `const` (`'this' argument has type 'const std::vector<int>'`). Wektor `const` nie może się zmieniać, więc nie można do niego niczego dopisać. Poprawka: usuń `const` z definicji wektora, który ma przyjmować elementy.

</details>

## 4. Czy wektor jest pusty? `empty()`

<!-- example: empty_check -->
```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<int> measurements{};

    if (measurements.empty()) {
        std::cout << "No measurements yet\n";
    }

    measurements.push_back(4);

    if (measurements.empty()) {
        std::cout << "No measurements yet\n";
    } else {
        std::cout << "Measurements stored: " << measurements.size() << "\n";
    }
}
```

**Przewidź**, które gałęzie się wykonają, i uruchom program.

<details>
<summary>Standardowe wyjście</summary>

<!-- output: empty_check -->
```text
No measurements yet
Measurements stored: 1
```

</details>

- `empty()` odpowiada na pytanie „czy wektor nie ma żadnego elementu?”. Daje `bool`: `true` albo `false`, więc pasuje wprost do warunku `if`.
- Po udanym `push_back` wcześniej pusty wektor przestaje być pusty.
- **`empty()` niczego nie usuwa.** Tylko sprawdza. To pytanie o stan wektora, a nie polecenie.
- `measurements.empty()` sprawdza to samo co `measurements.size() == 0`, ale wprost mówi, o co pytasz. Dlatego przy pytaniu „czy są dane?” używamy `empty()`.

## 5. Próby a zapisane elementy

Program odczytuje kolejno cztery liczby: `4`, `25`, `8` i `12`. Wymaganie mówi, że dopuszczalne są tylko wartości od 0 do 20. Wypełnij tabelę, zanim otworzysz odpowiedź:

| Próba | Odczytana liczba | W zakresie 0–20? | Co robi program | Zawartość wektora po próbie | `size()` |
|---|---|---|---|---|---|
| 1 | 4 | | | | |
| 2 | 25 | | | | |
| 3 | 8 | | | | |
| 4 | 12 | | | | |

<details>
<summary>Wypełniona tabela</summary>

| Próba | Odczytana liczba | W zakresie 0–20? | Co robi program | Zawartość wektora po próbie | `size()` |
|---|---|---|---|---|---|
| 1 | 4 | tak | dodaje 4 | `{4}` | 1 |
| 2 | 25 | nie | pomija | `{4}` | 1 |
| 3 | 8 | tak | dodaje 8 | `{4, 8}` | 2 |
| 4 | 12 | tak | dodaje 12 | `{4, 8, 12}` | 3 |

Były **cztery próby**, ale wektor ma **trzy elementy**, w kolejności 4, 8, 12. `size()` daje 3, a nie 4.

</details>

**Wektor nie zna reguł Twojego zadania.** `push_back(25)` dodałoby 25 bez żadnego sprawdzenia, bo dla wektora to zwykła liczba `int`. O tym, czy wartość trafi do kolekcji, decyduje **program**: wywołuje `push_back` tylko dla wartości, które spełniają wymagania. Liczba prób i liczba zapisanych elementów to więc dwie różne informacje.

## 6. Dane z wejścia trafiają do wektora

Ten program odczytuje trzy pomiary i zapisuje je w wektorze:

<!-- example: read_measurements -->
```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<int> measurements{};

    std::cout << "Enter 3 measurements:\n";

    for (int number{1}; number <= 3; ++number) {
        int measurement{0};
        std::cin >> measurement;

        if (!std::cin.fail()) {
            measurements.push_back(measurement);
        }
    }

    if (std::cin.fail()) {
        std::cout << "Input could not be read\n";
    } else {
        std::cout << "Measurements stored: " << measurements.size() << "\n";

        for (const int measurement : measurements) {
            std::cout << measurement << "\n";
        }
    }
}
```

Uruchom program i wpisz `3`, `7` i `5`, każdą liczbę w osobnej linijce:

<!-- input: read_measurements -->
```text
3
7
5
```

<!-- output: read_measurements -->
```text
Enter 3 measurements:
Measurements stored: 3
3
7
5
```

- `push_back` stoi **po** sprawdzeniu odczytu. Do wektora trafia tylko wartość, którą naprawdę udało się odczytać.
- Wektor jest wypisywany dopiero **po** pętli odczytu. Najpierw program zbiera wszystkie elementy, potem je przegląda.
- Jeśli jeden odczyt się nie uda, kolejne też się nie udają (lekcja 4.5). Pętla i tak kończy się po trzech przebiegach, a `std::cin.fail()` po pętli nadal daje `true`.

**Przewidź**, co wypisze program, gdy wpiszesz `3`, a potem `abc`. Potem sprawdź.

<!-- input: read_measurements -->
```text
3
abc
```

<details>
<summary>Standardowe wyjście</summary>

<!-- output: read_measurements -->
```text
Enter 3 measurements:
Input could not be read
```

Pierwszy pomiar trafił do wektora, ale drugi odczyt się nie udał, więc program nie wypisuje niepełnej listy.

</details>

## 7. Średnia zapisanych wartości

Średnią liczysz z sumy i liczby elementów. Najpierw jednak sprawdzasz, czy są jakieś elementy:

<!-- example: average_distance -->
```cpp
#include <iostream>
#include <vector>

int main() {
    const std::vector<int> distances{6, 9, 4, 8};

    if (distances.empty()) {
        std::cout << "No distances\n";
    } else {
        double total{0.0};

        for (const int distance : distances) {
            total += distance;
        }

        const double average{total / distances.size()};
        std::cout << "Average distance: " << average << " km\n";
    }
}
```

**Przewidź** średnią i uruchom program.

<details>
<summary>Standardowe wyjście</summary>

<!-- output: average_distance -->
```text
Average distance: 6.75 km
```

</details>

- Ten wektor się nie zmienia, więc ma `const`.
- **Suma jest typu `double`.** Elementy są `int`, ale `total += distance;` dodaje je do zmiennej `double`. Wtedy `total / distances.size()` to dzielenie z częścią ułamkową: 27 / 4 daje 6.75. Gdyby `total` był typu `int`, byłoby to dzielenie liczb całkowitych, jak w lekcji 2.4, i program wypisałby 6.
- **`empty()` stoi przed obliczeniem.** Dla tych danych gałąź `No distances` się nie wykona, ale program jest gotowy także na pusty wektor.

**Twoja kolej: przeanalizuj, nie uruchamiaj.** Ktoś usunął sprawdzenie `empty()`, a wektor nie ma żadnego elementu:

<!-- fragment -->
```cpp
const std::vector<int> distances{};
double total{0.0};

for (const int distance : distances) {
    total += distance;
}

const double average{total / distances.size()};
```

Czy wolno tak obliczyć średnią? Ile wynosi `total`, a ile `distances.size()`?

<details>
<summary>Odpowiedź</summary>

Nie. Pętla nie wykona się ani razu, więc `total` to 0, a `distances.size()` to 0. Średnia pustego zbioru w tym modelu nie istnieje: nie ma żadnej wartości, z której można by ją policzyć. Program wykonałby dzielenie przez zero, a żaden jego wynik nie byłby sensowną średnią. Dlatego takiego programu nie uruchamiamy, tylko piszemy go tak, żeby do tego nie doszło.

**Zanim wykonasz obliczenie, które wymaga danych, sprawdź, czy te dane naprawdę są.** Tutaj służy do tego `empty()`.

</details>

## 8. Misja: czasy oczekiwania

Program zbiera czasy oczekiwania z kilku zgłoszeń, w pełnych minutach. Nie każda poprawnie odczytana liczba jest dopuszczalnym czasem. Program zapisuje w wektorze tylko dopuszczalne czasy, a potem analizuje zapisane dane.

**Wymagania:**

- Program pyta `Enter report count (0-6):` i odczytuje liczbę zgłoszeń, liczbę całkowitą.
- Jeśli odczyt się nie uda, wypisuje `Input could not be read` i kończy pracę. Jeśli liczba jest spoza zakresu od 0 do 6, wypisuje `Invalid report count` i kończy pracę.
- Dla każdego zgłoszenia, od 1 do podanej liczby, pyta `Enter waiting time N (0-20):`, gdzie `N` to numer zgłoszenia, i odczytuje czas, liczbę całkowitą.
- Czas od 0 do 20 włącznie jest dopuszczalny i trafia do wektora `std::vector<int>`. Czas spoza tego zakresu program pomija: wypisuje `Waiting time N skipped` i **nie** zapisuje go. Pominięty czas zużywa swoje zgłoszenie: program nie pyta o niego ponownie.
- Jeśli odczyt czasu się nie uda, na przykład po tekście albo gdy dane skończą się wcześniej, program wypisuje `Input could not be read` i kończy pracę: bez pytań o kolejne zgłoszenia i bez podsumowania. Wcześniej wypisane linijki zostają.
- Po odczytaniu wszystkich zgłoszeń program wypisuje `Stored waiting times: N`, gdzie `N` to liczba zapisanych czasów.
- Jeśli nie zapisano żadnego czasu, wypisuje jeszcze tylko `No valid waiting times`. Nie liczy średniej.
- W przeciwnym razie wypisuje `Average waiting time: X`, czyli średnią zapisanych czasów, i `Times above average: N`, czyli liczbę zapisanych czasów **ściśle większych** od średniej.
- Elementy wektora przeglądasz pętlą zakresową. Wystarczą konstrukcje z tej lekcji i z poprzednich.

W `cpp-workspace` utwórz katalog `waiting_times`, skopiuj do niego `CMakeLists.txt` z oryginalnego `lesson_05_first_program`, utwórz pusty `main.cpp` i napisz program samodzielnie.

**Przykład A:** cztery zgłoszenia, czasy 4, 25, 8 i 12.

<!-- input: waiting_times -->
```text
4
4
25
8
12
```

<!-- output: waiting_times -->
```text
Enter report count (0-6):
Enter waiting time 1 (0-20):
Enter waiting time 2 (0-20):
Waiting time 2 skipped
Enter waiting time 3 (0-20):
Enter waiting time 4 (0-20):
Stored waiting times: 3
Average waiting time: 8
Times above average: 1
```

Wektor zawiera 4, 8 i 12. Średnia to 8, a ściśle większe od niej jest tylko 12.

**Przykład B:** zero zgłoszeń.

<!-- input: waiting_times -->
```text
0
```

<!-- output: waiting_times -->
```text
Enter report count (0-6):
Stored waiting times: 0
No valid waiting times
```

**Przykład C:** dwa zgłoszenia, czasy 5 i 6. **Przewidź** całe standardowe wyjście, zanim napiszesz program.

<!-- input: waiting_times -->
```text
2
5
6
```

<details>
<summary>Standardowe wyjście dla przykładu C</summary>

<!-- output: waiting_times -->
```text
Enter report count (0-6):
Enter waiting time 1 (0-20):
Enter waiting time 2 (0-20):
Stored waiting times: 2
Average waiting time: 5.5
Times above average: 1
```

Program, który wypisze tu średnią 5, liczy ją dzieleniem całkowitym.

</details>

**To nie jest program z punktu 6 z innymi napisami.** Tam program zapisywał każdą odczytaną liczbę, a po błędzie i tak kończył pętlę. Musisz samodzielnie zdecydować:

1. jak zbudować pętlę, która odczytuje zaplanowaną liczbę zgłoszeń i kończy się od razu po nieudanym odczycie;
2. jak odróżnić nieudany odczyt od poprawnie odczytanej, ale niedopuszczalnej liczby;
3. pod jakim warunkiem i w którym miejscu wywołać `push_back`;
4. co program wypisuje, gdy nie zapisał żadnego czasu;
5. jak policzyć średnią bez dzielenia całkowitego;
6. jak policzyć czasy większe od średniej i dlaczego czas równy średniej się nie liczy;
7. jak sprawić, żeby po nieudanym odczycie nie pojawiło się żadne podsumowanie.

**Zanim napiszesz program**, przygotuj tabelę przypadków testowych: zero zgłoszeń, jeden czas 0, jeden czas 20, średnią z częścią ułamkową, same zera, czas równy średniej, czasy pominięte przed poprawnym, między poprawnymi i po nich, same pominięte czasy, liczby zgłoszeń -1 i 7, tekst zamiast liczby zgłoszeń i zamiast czasu oraz dane, które kończą się po liczbie zgłoszeń albo po kilku czasach. Przy każdym przypadku zapisz oczekiwane standardowe wyjście.

Przypadki z danymi, które kończą się wcześniej, przeanalizuj na papierze, zamiast je uruchamiać, i porównaj z pełną listą kontrolną.

### Kryterium sukcesu

- Program buduje się jako C++20, a jego standardowe wyjście dla przykładów A, B i C jest dokładnie takie jak powyżej.
- Dla każdego przypadku z tabeli, który da się wpisać, standardowe wyjście zgadza się z wymaganiami. Przypadki z danymi, które kończą się wcześniej, zgadzają się z tabelą przebiegu.
- Wektor zawiera tylko dopuszczalne czasy, w kolejności zgłoszeń. Pominięty czas nigdy do niego nie trafia.
- Program nie liczy średniej, gdy wektor jest pusty, i nie liczy jej dzieleniem całkowitym.
- Po nieudanym odczycie program nie pyta o kolejne zgłoszenia i nie wypisuje podsumowania.
- Tabela przypadków powstała przed uruchomieniem programu.
- Umiesz wskazać w swoim programie miejsce, w którym decyduje się, czy czas trafi do wektora.

Gdy wynik się zgadza, możesz zapisać projekt w Gicie, jak w lekcji 1.5.

<details>
<summary>Podpowiedź 1</summary>

Czy liczba odczytanych zgłoszeń musi być równa liczbie elementów zapisanych w wektorze?

</details>

<details>
<summary>Podpowiedź 2</summary>

Zastanów się, w którym miejscu wywołać `push_back()`, aby niedopuszczalna liczba nigdy nie trafiła do kolekcji.

</details>

<details>
<summary>Podpowiedź 3</summary>

Po zakończeniu odczytu sprawdź `empty()`. Dopiero potem oblicz średnią i ponownie przejrzyj zapisane wartości, aby policzyć te większe od średniej.

</details>

<details>
<summary>Pełna lista przypadków kontrolnych: otwórz po przygotowaniu własnej tabeli</summary>

Przykłady A, B i C są sprawdzone wyżej. „Pominięte” to numery zgłoszeń z komunikatem `Waiting time N skipped`.

| Dane | Pominięte | Wynik | Co sprawdza |
|---|---|---|---|
| `4`, `4`, `25`, `8`, `12` | 2 | zapisane 3, średnia 8, powyżej 1 | przykład A: pominięty czas między poprawnymi |
| `0` | — | zapisane 0, `No valid waiting times` | przykład B: zero zgłoszeń |
| `2`, `5`, `6` | — | zapisane 2, średnia 5.5, powyżej 1 | przykład C: średnia z częścią ułamkową |
| `1`, `0` | — | zapisane 1, średnia 0, powyżej 0 | dolna granica czasu |
| `1`, `20` | — | zapisane 1, średnia 20, powyżej 0 | górna granica czasu |
| `3`, `0`, `0`, `0` | — | zapisane 3, średnia 0, powyżej 0 | same zera |
| `3`, `4`, `8`, `12` | — | zapisane 3, średnia 8, powyżej 1 | czas równy średniej się nie liczy |
| `2`, `0`, `20` | — | zapisane 2, średnia 10, powyżej 1 | obie granice naraz |
| `6`, sześć razy `20` | — | zapisane 6, średnia 20, powyżej 0 | największa liczba zgłoszeń, wszystkie równe średniej |
| `3`, `-1`, `21`, `3` | 1, 2 | zapisane 1, średnia 3, powyżej 0 | czasy tuż poza zakresem przed poprawnym |
| `3`, `6`, `9`, `-5` | 3 | zapisane 2, średnia 7.5, powyżej 1 | pominięty czas po poprawnych |
| `2`, `-1`, `21` | 1, 2 | zapisane 0, `No valid waiting times` | wszystkie czasy pominięte: pusty wektor |
| `-1` | — | `Invalid report count` | liczba zgłoszeń tuż pod zakresem |
| `7` | — | `Invalid report count` | liczba zgłoszeń tuż nad zakresem |
| `abc` | — | `Input could not be read` | tekst zamiast liczby zgłoszeń |
| brak danych | — | `Input could not be read` | dane kończą się od razu |
| `2`, `abc` | — | pytanie o czas 1, potem `Input could not be read` | tekst zamiast pierwszego czasu |
| `3`, `4`, `abc` | — | pytania o czasy 1 i 2, potem `Input could not be read` | tekst zamiast drugiego czasu |
| `3`, koniec danych | — | pytanie o czas 1, potem `Input could not be read` | dane kończą się po liczbie zgłoszeń |
| `3`, `4`, koniec danych | — | pytania o czasy 1 i 2, potem `Input could not be read` | dane kończą się po jednym czasie |
| `4`, `4`, `25`, koniec danych | 2 | pytania o czasy 1–3, potem `Input could not be read` | dane kończą się po pominiętym czasie |

<!-- input: waiting_times -->
```text
1
0
```

<!-- output: waiting_times -->
```text
Enter report count (0-6):
Enter waiting time 1 (0-20):
Stored waiting times: 1
Average waiting time: 0
Times above average: 0
```

<!-- input: waiting_times -->
```text
1
20
```

<!-- output: waiting_times -->
```text
Enter report count (0-6):
Enter waiting time 1 (0-20):
Stored waiting times: 1
Average waiting time: 20
Times above average: 0
```

<!-- input: waiting_times -->
```text
3
0
0
0
```

<!-- output: waiting_times -->
```text
Enter report count (0-6):
Enter waiting time 1 (0-20):
Enter waiting time 2 (0-20):
Enter waiting time 3 (0-20):
Stored waiting times: 3
Average waiting time: 0
Times above average: 0
```

<!-- input: waiting_times -->
```text
3
4
8
12
```

<!-- output: waiting_times -->
```text
Enter report count (0-6):
Enter waiting time 1 (0-20):
Enter waiting time 2 (0-20):
Enter waiting time 3 (0-20):
Stored waiting times: 3
Average waiting time: 8
Times above average: 1
```

<!-- input: waiting_times -->
```text
2
0
20
```

<!-- output: waiting_times -->
```text
Enter report count (0-6):
Enter waiting time 1 (0-20):
Enter waiting time 2 (0-20):
Stored waiting times: 2
Average waiting time: 10
Times above average: 1
```

<!-- input: waiting_times -->
```text
6
20
20
20
20
20
20
```

<!-- output: waiting_times -->
```text
Enter report count (0-6):
Enter waiting time 1 (0-20):
Enter waiting time 2 (0-20):
Enter waiting time 3 (0-20):
Enter waiting time 4 (0-20):
Enter waiting time 5 (0-20):
Enter waiting time 6 (0-20):
Stored waiting times: 6
Average waiting time: 20
Times above average: 0
```

<!-- input: waiting_times -->
```text
3
-1
21
3
```

<!-- output: waiting_times -->
```text
Enter report count (0-6):
Enter waiting time 1 (0-20):
Waiting time 1 skipped
Enter waiting time 2 (0-20):
Waiting time 2 skipped
Enter waiting time 3 (0-20):
Stored waiting times: 1
Average waiting time: 3
Times above average: 0
```

<!-- input: waiting_times -->
```text
3
6
9
-5
```

<!-- output: waiting_times -->
```text
Enter report count (0-6):
Enter waiting time 1 (0-20):
Enter waiting time 2 (0-20):
Enter waiting time 3 (0-20):
Waiting time 3 skipped
Stored waiting times: 2
Average waiting time: 7.5
Times above average: 1
```

<!-- input: waiting_times -->
```text
2
-1
21
```

<!-- output: waiting_times -->
```text
Enter report count (0-6):
Enter waiting time 1 (0-20):
Waiting time 1 skipped
Enter waiting time 2 (0-20):
Waiting time 2 skipped
Stored waiting times: 0
No valid waiting times
```

<!-- input: waiting_times -->
```text
-1
```

<!-- output: waiting_times -->
```text
Enter report count (0-6):
Invalid report count
```

<!-- input: waiting_times -->
```text
7
```

<!-- output: waiting_times -->
```text
Enter report count (0-6):
Invalid report count
```

<!-- input: waiting_times -->
```text
abc
```

<!-- output: waiting_times -->
```text
Enter report count (0-6):
Input could not be read
```

<!-- input: waiting_times -->
```text
```

<!-- output: waiting_times -->
```text
Enter report count (0-6):
Input could not be read
```

<!-- input: waiting_times -->
```text
2
abc
```

<!-- output: waiting_times -->
```text
Enter report count (0-6):
Enter waiting time 1 (0-20):
Input could not be read
```

<!-- input: waiting_times -->
```text
3
4
abc
```

<!-- output: waiting_times -->
```text
Enter report count (0-6):
Enter waiting time 1 (0-20):
Enter waiting time 2 (0-20):
Input could not be read
```

<!-- input: waiting_times -->
```text
3
```

<!-- output: waiting_times -->
```text
Enter report count (0-6):
Enter waiting time 1 (0-20):
Input could not be read
```

<!-- input: waiting_times -->
```text
3
4
```

<!-- output: waiting_times -->
```text
Enter report count (0-6):
Enter waiting time 1 (0-20):
Enter waiting time 2 (0-20):
Input could not be read
```

<!-- input: waiting_times -->
```text
4
4
25
```

<!-- output: waiting_times -->
```text
Enter report count (0-6):
Enter waiting time 1 (0-20):
Enter waiting time 2 (0-20):
Waiting time 2 skipped
Enter waiting time 3 (0-20):
Input could not be read
```

</details>

Przykładowe rozwiązanie jest w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 9. Znajdź błąd: pominięta wartość trafia do wektora

To zadanie wykonaj **po misji**: program poniżej pokazuje, gdzie stoi `push_back` przy wybieraniu danych, więc mógłby podpowiedzieć rozwiązanie. Program odczytuje trzy wyniki od 0 do 10 i pomija wyniki spoza zakresu. Zakładamy, że wpisujesz liczby całkowite.

<details>
<summary>Program do sprawdzenia: otwórz po napisaniu własnego programu</summary>

<!-- example: scores_bug -->
```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<int> scores{};

    std::cout << "Enter 3 scores (0-10):\n";

    for (int number{1}; number <= 3; ++number) {
        int score{0};
        std::cin >> score;

        if (score < 0 || score > 10) {
            std::cout << "Score " << number << " skipped\n";
        }

        scores.push_back(score);
    }

    std::cout << "Stored scores: " << scores.size() << "\n";

    for (const int score : scores) {
        std::cout << score << "\n";
    }
}
```

1. **Przewidź**, ile wyników zostanie zapisanych dla danych `7`, `4`, `9`, a ile dla `7`, `15`, `9`.
2. Uruchom program z danymi `7`, `4`, `9`, czyli z samymi poprawnymi wynikami.
3. Uruchom go z danymi `7`, `15`, `9`.
4. Porównaj oba wyniki z wymaganiem. Dlaczego pierwszy przypadek nie ujawnia błędu?
5. Znajdź miejsce, w którym wynik jest dodawany do wektora.
6. Popraw strukturę warunku tak, żeby pominięty wynik nie trafiał do wektora.
7. Sprawdź ponownie oba przypadki.

</details>

Wyniki programu przed poprawką i poprawiony program są w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 10. Gdy coś pójdzie inaczej

| Co widzisz | Co to znaczy | Co zrobić |
|---|---|---|
| `no matching member function for call to 'push_back'` | Wektor jest `const`, więc nie można do niego dopisywać elementów (punkt 3). | Usuń `const` z definicji wektora, który ma przyjmować elementy. |
| `size()` jest większe niż liczba dopuszczalnych wartości | `push_back` wykonuje się także dla pominiętych wartości (punkt 9). | Sprawdź, czy `push_back` stoi tylko w gałęzi dla dopuszczalnej wartości. |
| Średnia to liczba całkowita, na przykład 5 zamiast 5.5 | Suma jest typu `int`, więc dzielenie jest całkowite. | Sumuj w zmiennej `double` (punkt 7). |
| Liczba czasów powyżej średniej jest za duża, gdy któryś czas jest równy średniej | Porównanie `>=` zamiast `>`. | Sprawdź przypadek `3`, `4`, `8`, `12`: wynik to 1. |
| Po zerze zgłoszeń albo po samych pominiętych czasach pojawia się średnia | Brakuje sprawdzenia `empty()` przed obliczeniem. | Sprawdź `empty()`, zanim policzysz średnią (punkt 7). |
| Po tekście program pyta o kolejne czasy | Pętla nie kończy się po nieudanym odczycie. | Zakończ odczyt od razu, jak w pętlach z flagą z lekcji 4.5 i 5.7. |
| Po nieudanym odczycie pojawia się `Stored waiting times` | Podsumowanie nie zależy od tego, czy odczyt się udał. | Wypisuj podsumowanie tylko wtedy, gdy wszystkie odczyty się udały. |
| Program nic nie robi i czeka | Czeka na liczbę, jak w lekcji 2.6. | Wpisz liczbę i naciśnij **Enter**. |

## 11. Wyjaśnij

Odpowiedz własnymi słowami, najlepiej na piśmie. Dopiero potem porównaj z przykładowymi odpowiedziami.

1. Dlaczego wektor w misji nie jest `const`, a wektory w lekcji 6.1 były?
2. Co robi `push_back()` i gdzie trafia nowy element?
3. Czy wektor musi znać końcową liczbę elementów, gdy go tworzysz?
4. Co podaje `size()`, a co `empty()`? Czy `empty()` usuwa elementy?
5. Czy `push_back()` sam sprawdza, czy wartość jest dopuszczalna?
6. Dlaczego liczba zgłoszeń może być inna niż `size()` i co dzieje się z czasem spoza zakresu?
7. Czym różni się czas niedopuszczalny od nieudanego odczytu?
8. Dlaczego nie liczymy średniej pustego wektora?
9. Dlaczego suma typu `double` chroni przed dzieleniem całkowitym?
10. Czy czasy 0 i 20 mogą zostać zapisane?
11. Czy czas równy średniej liczymy jako większy od średniej?
12. Dlaczego po obliczeniu średniej przeglądamy wektor drugi raz i czy dane nadal w nim są?

<details>
<summary>Przykładowe odpowiedzi</summary>

1. Bo program dodaje do niego elementy, czyli go zmienia. Wektory z lekcji 6.1 miały wszystkie elementy od początku i się nie zmieniały, więc miały `const`. Do wektora `const` nie da się niczego dopisać.
2. Dodaje podaną wartość jako nowy element na końcu wektora. Wcześniejsze elementy zostają, a `size()` rośnie o 1.
3. Nie. Wektor może zacząć pusty i rosnąć przy każdym `push_back`.
4. `size()` podaje liczbę elementów, a `empty()` daje `true`, gdy wektor nie ma żadnego elementu, i `false` w przeciwnym razie. `empty()` tylko sprawdza, niczego nie usuwa.
5. Nie. Dla wektora każda liczba `int` jest tak samo dobra. O tym, czy wartość trafi do wektora, decyduje program: wywołuje `push_back` tylko dla dopuszczalnych wartości.
6. Bo czas spoza zakresu zużywa swoje zgłoszenie, ale nie trafia do wektora. Program wypisuje informację o pominięciu i przechodzi do kolejnego zgłoszenia.
7. Czas niedopuszczalny to liczba odczytana poprawnie, ale spoza zakresu: program go pomija i pracuje dalej. Nieudany odczyt to brak liczby, na przykład po tekście albo po końcu danych: program nie ma czego sprawdzać i kończy pracę bez podsumowania.
8. Bo nie ma żadnej wartości, z której można by ją policzyć. Suma i liczba elementów są wtedy równe 0, a takie dzielenie nie daje sensownej średniej.
9. Bo dzielenie wartości `double` przez liczbę elementów daje wynik z częścią ułamkową. Gdyby suma była `int`, dzielenie byłoby całkowite: dla 5 i 6 wyszłoby 5 zamiast 5.5.
10. Tak. Zakres od 0 do 20 jest włącznie, więc oba końce są dopuszczalne.
11. Nie. Wymaganie mówi o czasach ściśle większych od średniej, więc w warunku stoi `>`. Przypadek `4`, `8`, `12` to sprawdza: 8 jest równe średniej i się nie liczy.
12. Bo średnia jest znana dopiero po zsumowaniu wszystkich czasów, a dopiero wtedy można porównać z nią każdy czas. Pętla zakresowa tylko odczytuje elementy, więc po pierwszym przejściu wektor ma te same czasy w tej samej kolejności.

</details>

## Podsumowanie

- `std::vector<int> values{};` tworzy pusty wektor. Bez `const`, bo program będzie do niego dopisywać elementy. Wektor, który się nie zmienia, nadal ma `const`.
- `values.push_back(value);` dodaje element na koniec. Kolejność elementów to kolejność wywołań, a `size()` rośnie o 1 przy każdym wywołaniu.
- `values.empty()` daje `true`, gdy wektor nie ma elementów. Niczego nie usuwa.
- `push_back` niczego nie sprawdza. To program decyduje, czy wartość trafi do wektora, więc liczba prób odczytu może być większa niż `size()`.
- Do wektora dodawaj wartość dopiero po udanym odczycie. Najpierw zbierz elementy, potem je przeglądaj.
- Przed średnią sprawdź `empty()`. Sumuj w `double`, żeby uniknąć dzielenia całkowitego.
- Liczenie wartości większych od średniej wymaga drugiego przejścia, bo średnia jest znana dopiero po pierwszym.

## Co dalej

W tej lekcji wektor przeglądała pętla zakresowa, zawsze od pierwszego do ostatniego elementu. W kolejnej lekcji poznasz pozycje elementów: odczytasz pierwszy, ostatni albo wybrany element i porównasz sąsiednie wartości: [Lekcja 6.3: Pozycje elementów i sąsiednie wartości w `std::vector`](lesson_03_positions_and_neighbours.md).

---

## Przykładowe rozwiązania

Zajrzyj tutaj **po własnej próbie**. Twoje nazwy mogą się różnić, jeśli standardowe wyjście jest takie, jak wymagane.

<details>
<summary>Punkt 8: misja, czasy oczekiwania</summary>

<!-- example: waiting_times -->
```cpp
#include <iostream>
#include <vector>

int main() {
    int report_count{0};

    std::cout << "Enter report count (0-6):\n";
    std::cin >> report_count;

    if (std::cin.fail()) {
        std::cout << "Input could not be read\n";
    } else if (report_count < 0 || report_count > 6) {
        std::cout << "Invalid report count\n";
    } else {
        std::vector<int> waiting_times{};
        bool input_failed{false};

        for (int report_number{1}; report_number <= report_count && !input_failed; ++report_number) {
            int waiting_time{0};

            std::cout << "Enter waiting time " << report_number << " (0-20):\n";
            std::cin >> waiting_time;

            if (std::cin.fail()) {
                input_failed = true;
            } else if (waiting_time >= 0 && waiting_time <= 20) {
                waiting_times.push_back(waiting_time);
            } else {
                std::cout << "Waiting time " << report_number << " skipped\n";
            }
        }

        if (input_failed) {
            std::cout << "Input could not be read\n";
        } else {
            std::cout << "Stored waiting times: " << waiting_times.size() << "\n";

            if (waiting_times.empty()) {
                std::cout << "No valid waiting times\n";
            } else {
                double total{0.0};

                for (const int waiting_time : waiting_times) {
                    total += waiting_time;
                }

                const double average{total / waiting_times.size()};
                int above_average{0};

                for (const int waiting_time : waiting_times) {
                    if (waiting_time > average) {
                        ++above_average;
                    }
                }

                std::cout << "Average waiting time: " << average << "\n";
                std::cout << "Times above average: " << above_average << "\n";
            }
        }
    }
}
```

- **Trzy wyniki odczytu**, trzy gałęzie: nieudany odczyt ustawia flagę, dopuszczalny czas trafia do wektora, a niedopuszczalny jest pomijany z komunikatem. `push_back` stoi tylko w jednej z nich.
- **Pętla** wykonuje się najwyżej `report_count` razy, także gdy któryś czas zostanie pominięty: każdy przebieg zużywa jedno zgłoszenie. Kończy się wcześniej tylko wtedy, gdy odczyt się nie uda, bo warunek sprawdza też `!input_failed`. Dla zera zgłoszeń nie wykonuje się ani razu.
- **`size()`** to liczba zapisanych czasów, nie liczba zgłoszeń. Dla przykładu A zgłoszeń jest 4, a `size()` daje 3.
- **Pusty wektor** po zerze zgłoszeń albo po samych pominiętych czasach kończy się komunikatem `No valid waiting times`, bez obliczania średniej.
- **Pierwsze przejście** sumuje czasy w `double`, więc średnia może mieć część ułamkową. **Drugie** porównuje każdy czas z gotową średnią. Warunek `waiting_time > average` porównuje `int` z `double`: czas zostaje na chwilę potraktowany jako `double`, a jego wartość się nie zmienia.
- **Nieudany odczyt:** wcześniejsze pytania i komunikaty zostają, a zamiast podsumowania program wypisuje `Input could not be read`.
- Ten sam program da się napisać z pętlą `while`, jak w lekcji 5.7. Ważne, żeby pętla kończyła się po nieudanym odczycie, a `push_back` stał tylko w gałęzi dla dopuszczalnego czasu.

</details>

<details>
<summary>Punkt 9: wyniki przed poprawką i poprawiony program</summary>

Przed poprawką, dla danych `7`, `4`, `9`:

<!-- input: scores_bug -->
```text
7
4
9
```

<!-- output: scores_bug -->
```text
Enter 3 scores (0-10):
Stored scores: 3
7
4
9
```

Dla danych `7`, `15`, `9`:

<!-- input: scores_bug -->
```text
7
15
9
```

<!-- output: scores_bug -->
```text
Enter 3 scores (0-10):
Score 2 skipped
Stored scores: 3
7
15
9
```

- Dla samych poprawnych wyników program działa zgodnie z wymaganiem, bo każdy wynik i tak powinien trafić do wektora. Błąd ujawnia dopiero wynik spoza zakresu.
- Dla `15` program wypisuje `Score 2 skipped`, a mimo to zapisuje 15: `size()` daje 3 zamiast 2, a 15 jest na liście.
- **Przyczyna:** `push_back` stoi **za** blokiem `if`, więc wykonuje się w każdym przebiegu, niezależnie od warunku. Komunikat o pominięciu niczego nie pomija.
- **Poprawka:** dodawanie przenieś do gałęzi `else`. Wtedy wykonuje się albo komunikat, albo `push_back`, nigdy oba.

<!-- example: scores_fixed -->
```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<int> scores{};

    std::cout << "Enter 3 scores (0-10):\n";

    for (int number{1}; number <= 3; ++number) {
        int score{0};
        std::cin >> score;

        if (score < 0 || score > 10) {
            std::cout << "Score " << number << " skipped\n";
        } else {
            scores.push_back(score);
        }
    }

    std::cout << "Stored scores: " << scores.size() << "\n";

    for (const int score : scores) {
        std::cout << score << "\n";
    }
}
```

<!-- input: scores_fixed -->
```text
7
4
9
```

<!-- output: scores_fixed -->
```text
Enter 3 scores (0-10):
Stored scores: 3
7
4
9
```

<!-- input: scores_fixed -->
```text
7
15
9
```

<!-- output: scores_fixed -->
```text
Enter 3 scores (0-10):
Score 2 skipped
Stored scores: 2
7
9
```

</details>

**Poprzednia lekcja:** [Lekcja 6.1: Pierwszy `std::vector` i pętla zakresowa `for`](lesson_01_the_first_vector.md) · **Następna lekcja:** [Lekcja 6.3: Pozycje elementów i sąsiednie wartości w `std::vector`](lesson_03_positions_and_neighbours.md) · [Opis kursu](../../README.md)

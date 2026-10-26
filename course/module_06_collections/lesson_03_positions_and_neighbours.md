# Lekcja 6.3: Pozycje elementów i sąsiednie wartości w `std::vector`

**Polski** · [English](lesson_03_positions_and_neighbours.en.md) · [Opis kursu](../../README.md)

> **Moduł 6, lekcja 3** · około 70–85 minut
> **Potrzebujesz:** katalogu `cpp-workspace` i oryginalnego projektu `lesson_05_first_program`, jak dotąd. Debugger nie jest w tej lekcji potrzebny.
> **Wersja pilotażowa.** Programy z tej lekcji sprawdzamy automatycznie na Windowsie, Ubuntu i macOS, także z podanymi danymi wejściowymi. Wpisywanie danych w oknie **Run** CLiona opisujemy bez ręcznego sprawdzenia na każdym systemie.

## Zanim zaczniesz

Ta lekcja zakłada, że po lekcjach 6.1 i 6.2:

- przeglądasz wektor pętlą zakresową i odczytujesz liczbę elementów przez `size()`;
- sprawdzasz przez `empty()`, czy wektor ma jakiekolwiek elementy;
- piszesz pętlę `for` z licznikiem: wartość początkowa, warunek i aktualizacja (lekcja 4.3);
- wiesz, że inicjalizacja przez `{}` nie pozwala na konwersję zawężającą (lekcja 2.5).

## Sytuacja

Ten wektor przechowuje cztery odczyty z czujnika:

<!-- fragment -->
```cpp
const std::vector<int> readings{10, 14, 11, 19};
```

Pętlą zakresową wypiszesz wszystkie cztery wartości. Spróbuj jednak odpowiedzieć tylko z jej pomocą:

- Który odczyt jest drugi?
- O ile drugi odczyt jest większy od pierwszego?
- Czy trzeci odczyt jest niższy od drugiego?
- Jak porównać **każdy** odczyt z poprzednim?

Pętla zakresowa daje w każdym przebiegu jedną wartość i nie mówi, na której pozycji ona stoi ani co było przed nią. Do takich pytań potrzebujesz **pozycji elementu** w wektorze. Gdy pozycja nie jest potrzebna, pętla zakresowa nadal jest dobrym wyborem.

Po tej lekcji będziesz:

- odczytywać element o wybranej pozycji przez `values[index]`, z indeksami od 0;
- wskazywać poprawne indeksy wektora i wyjaśniać, dlaczego indeks równy `size()` nie jest pozycją elementu;
- odczytywać pierwszy i ostatni element niepustego wektora;
- przechowywać rozmiary i indeksy w typie `std::size_t`;
- przechodzić po pozycjach pętlą `for` i zamieniać indeks na numer widoczny dla użytkownika;
- bezpiecznie porównywać każdy element z poprzednim, także dla pustego i jednoelementowego wektora;
- samodzielnie znajdować największy spadek między kolejnymi pomiarami.

## 1. Przygotuj projekt

W `cpp-workspace` utwórz katalog `lesson_6_3` i skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program`. Programy z punktów 2–7 wpisujesz w `main.cpp` tego katalogu.

## 2. Element o wybranej pozycji: `[]`

<!-- example: readings_by_index -->
```cpp
#include <iostream>
#include <vector>

int main() {
    const std::vector<int> readings{10, 14, 11, 19};

    std::cout << readings[0] << "\n";
    std::cout << readings[1] << "\n";
    std::cout << readings[2] << "\n";
    std::cout << readings[3] << "\n";
}
```

<!-- output: readings_by_index -->
```text
10
14
11
19
```

`readings[1]` czytaj: „element wektora `readings` o indeksie 1”. Liczba w nawiasach kwadratowych to **indeks**, czyli pozycja elementu. **Indeksy zaczynają się od 0**:

| Numer elementu dla człowieka | Indeks w C++ | Wartość |
|---|---|---|
| 1 | 0 | 10 |
| 2 | 1 | 14 |
| 3 | 2 | 11 |
| 4 | 3 | 19 |

Wektor ma cztery elementy, więc ma indeksy 0, 1, 2 i 3. Indeksu 4 nie ma: pod nim nie stoi żaden element. Ogólnie: wektor z `N` elementami ma indeksy od 0 do `N - 1`.

Indeks mówi tylko, **gdzie** stoi element. Wartość elementu to coś innego: pod indeksem 2 stoi wartość 11.

## 3. Poza zakresem

**`readings[index]` nie sprawdza, czy indeks jest poprawny.** Kompilator i program przyjmują, że to Ty pilnujesz zakresu.

<!-- fragment -->
```cpp
const std::vector<int> readings{10, 14, 11, 19};
std::cout << readings[4] << "\n";  // wrong: index 4 does not exist
```

Ten fragment się zbuduje. Ale odczyt elementu, którego nie ma, to w C++ **niezdefiniowane zachowanie**: standard języka nie mówi, co się wtedy stanie. Program może wypisać przypadkową liczbę, zakończyć się błędem albo pozornie działać poprawnie, a na innym komputerze zachować się inaczej. Nie ma tu gwarantowanego błędu kompilacji ani komunikatu. Dlatego takich programów nie uruchamiamy, tylko piszemy kod tak, żeby **każdy indeks był w zakresie od 0 do `size() - 1`**.

## 4. Pierwszy i ostatni element

<!-- example: first_and_last -->
```cpp
#include <iostream>
#include <vector>

int main() {
    const std::vector<int> readings{10, 14, 11, 19};

    if (readings.empty()) {
        std::cout << "No readings\n";
    } else {
        std::cout << "First reading: " << readings[0] << "\n";
        std::cout << "Last reading: " << readings[readings.size() - 1] << "\n";
    }
}
```

**Przewidź** obie linijki wyniku i uruchom program.

<details>
<summary>Standardowe wyjście</summary>

<!-- output: first_and_last -->
```text
First reading: 10
Last reading: 19
```

</details>

- Pierwszy element ma indeks 0, a ostatni `size() - 1`: tutaj 4 − 1, czyli 3.
- **Najpierw `empty()`.** Pusty wektor nie ma pierwszego ani ostatniego elementu. Co więcej, `size()` jest wtedy 0, a wynik `size()` to liczba bez znaku, która nie może być ujemna: `0 - 1` nie daje tu −1, tylko ogromną liczbę dodatnią. **Nie odejmujemy 1 od rozmiaru pustego wektora, żeby wyznaczyć indeks.**
- Wektor ma też funkcje `front()` i `back()`, które dają pierwszy i ostatni element. W tym kursie na razie z nich nie korzystamy.

## 5. Typ indeksu: `std::size_t`

W lekcji 6.1 wynik `size()` tylko wypisywaliśmy. Spróbuj zapisać go w zmiennej `int`:

<!-- broken: count_as_int at=6:21 errors=1 error=^non-constant-expression cannot be narrowed from type .+ to 'int' in initializer list -->
```cpp
#include <iostream>
#include <vector>

int main() {
    const std::vector<int> readings{10, 14, 11, 19};
    const int count{readings.size()};

    std::cout << "Readings: " << count << "\n";
}
```

**Przewidź**, czy program się zbuduje. Potem spróbuj go zbudować.

<details>
<summary>Co zgłasza kompilator i dlaczego</summary>

Program się nie zbuduje. Kompilator zgłasza w linijce 6 `non-constant-expression cannot be narrowed from type ... to 'int' in initializer list`. W miejscu kropek stoi nazwa typu, który podaje `size()`. Ta nazwa zależy od systemu, na przykład `'size_type' (aka 'unsigned long')`. To ta sama ochrona co w lekcji 2.5: `{}` nie pozwala na konwersję zawężającą. Typ `int` przyjmuje liczby ujemne, ale nie mieści wszystkich możliwych rozmiarów, więc taka zmiana typu mogłaby zmienić wartość.

</details>

**Poprawka:** rozmiary i indeksy przechowuj w typie **`std::size_t`**:

<!-- fragment -->
```cpp
const std::size_t count{readings.size()};
```

- `std::size_t` to typ całkowity **bez znaku**: przechowuje tylko liczby nieujemne.
- Jest przeznaczony do rozmiarów i indeksów, więc pasuje do wyniku `size()`. Ile dokładnie liczb mieści, zależy od systemu.
- Udostępnia go nagłówek `<cstddef>`. Dołączaj go zawsze, gdy piszesz `std::size_t`, jak `<vector>` przy wektorze.
- **Nie mieszaj `std::size_t` z `int`.** Porównanie zmiennej `int` z `size()` przy flagach kursu też zatrzymuje budowanie: kompilator zgłasza `comparison of integers of different signs`.

## 6. Pętla po pozycjach

Program wypisuje odczyty jako kolejne dni:

<!-- example: days_listed -->
```cpp
#include <cstddef>
#include <iostream>
#include <vector>

int main() {
    const std::vector<int> readings{10, 14, 11, 19};
    const std::size_t count{readings.size()};

    std::cout << "Readings: " << count << "\n";

    for (std::size_t index{0}; index < readings.size(); ++index) {
        std::cout << "Day " << index + 1 << ": " << readings[index] << "\n";
    }
}
```

**Przewidź** wszystkie linijki wyniku i uruchom program.

<details>
<summary>Standardowe wyjście</summary>

<!-- output: days_listed -->
```text
Readings: 4
Day 1: 10
Day 2: 14
Day 3: 11
Day 4: 19
```

</details>

To pętla `for` z lekcji 4.3, z licznikiem, który jest indeksem:

1. `std::size_t index{0}`: indeks zaczyna od 0, czyli od pierwszego elementu.
2. `index < readings.size()`: pętla trwa, dopóki indeks wskazuje istniejący element.
3. `readings[index]`: odczyt elementu o bieżącym indeksie.
4. `++index`: przejście do następnej pozycji.
5. Gdy `index` osiągnie 4, czyli `size()`, warunek daje `false` i pętla kończy się **bez** odczytu `readings[4]`.

**Indeks to nie numer dnia.** W kodzie pierwszy element ma indeks 0, a użytkownik widzi „Day 1”. Program **oblicza** numer dnia: `index + 1`. Samego indeksowania nie zmieniamy: wektor zawsze zaczyna się od indeksu 0, a numer od 1 to tylko sposób pokazania wyniku człowiekowi.

Pętla zakresowa podaje kolejne wartości. Pętla po indeksach podaje także **pozycję** każdej wartości. Gdy pozycja nie jest potrzebna, wybierz pętlę zakresową.

## 7. Sąsiednie elementy

Zmiana między dwoma kolejnymi odczytami to bieżący odczyt minus poprzedni: `readings[index] - readings[index - 1]`.

<!-- example: changes -->
```cpp
#include <cstddef>
#include <iostream>
#include <vector>

int main() {
    const std::vector<int> readings{10, 14, 11, 19};

    for (std::size_t index{1}; index < readings.size(); ++index) {
        const int change{readings[index] - readings[index - 1]};
        std::cout << change << "\n";
    }
}
```

**Przewidź**, ile liczb wypisze program i jakie. Potem go uruchom.

<details>
<summary>Standardowe wyjście</summary>

<!-- output: changes -->
```text
4
-3
8
```

</details>

| Indeks bieżącego | Poprzednia wartość | Bieżąca wartość | Zmiana |
|---|---|---|---|
| 1 | 10 | 14 | +4 |
| 2 | 14 | 11 | −3 |
| 3 | 11 | 19 | +8 |

- **Pętla zaczyna od indeksu 1**, bo element o indeksie 0 nie ma poprzednika. Dla każdego indeksu od 1 wzwyż poprzedni element, `index - 1`, istnieje.
- **Warunek `index < readings.size()`** pilnuje, żeby bieżący element też istniał.
- Cztery elementy dają **trzy** pary sąsiadów: każda para to element razem z poprzednim, a pierwszy element poprzednika nie ma.

**Twoja kolej.** Ile przebiegów wykona ta pętla dla wektora pustego `{}`, dla `{5}` i dla `{5, 8}`?

<details>
<summary>Odpowiedź</summary>

- `{}`: zero. `index` zaczyna od 1, a `1 < 0` daje `false`.
- `{5}`: zero. `1 < 1` daje `false`. Jeden element nie tworzy pary.
- `{5, 8}`: jeden przebieg, dla indeksu 1: zmiana 8 − 5 = 3.

Ta sama pętla jest bezpieczna dla każdego rozmiaru, bez osobnego sprawdzania. Porównaj z dwoma błędnymi pomysłami:

<!-- fragment -->
```cpp
// wrong: for index 0, index - 1 is not the index of any element
for (std::size_t index{0}; index < readings.size(); ++index) {
    const int change{readings[index] - readings[index - 1]};
}

// wrong: for an empty vector, readings.size() - 1 is not -1
for (std::size_t index{0}; index < readings.size() - 1; ++index) {
    const int change{readings[index + 1] - readings[index]};
}
```

W pierwszym `index - 1` dla indeksu 0 nie wskazuje żadnego elementu. W drugim, dla pustego wektora, `readings.size() - 1` to ogromna liczba, więc pętla próbuje czytać elementy, których nie ma. Oba to niezdefiniowane zachowanie, więc ich nie uruchamiamy.

</details>

## 8. Misja: największe ochłodzenie

Program przechowuje temperatury z kolejnych dni, w pełnych stopniach Celsjusza, i szuka największego spadku temperatury między dwoma kolejnymi dniami. Dane są wpisane w kodzie:

<!-- fragment -->
```cpp
const std::vector<int> temperatures{8, 5, 7, 1, 0, 3};
```

**Spadek** to sytuacja, w której temperatura wcześniejszego dnia jest wyższa niż następnego. Dla pary 8 i 5 spadek wynosi 3. Dla pary 5 i 8 ochłodzenia nie ma. Dla dwóch równych temperatur zmiana wynosi 0, a to nie jest spadek.

**Wymagania:**

- Program przechowuje temperatury w `const std::vector<int>` z wartościami początkowymi. Nie odczytuje niczego z wejścia.
- Pierwsza linijka to zawsze `Days recorded: N`, gdzie `N` to liczba dni.
- Dla mniej niż dwóch dni program wypisuje `Not enough days`.
- Dla co najmniej dwóch dni, jeśli temperatura ani razu nie spadła, wypisuje `No temperature drop`.
- W przeciwnym razie wypisuje `Largest drop: N`, czyli największy spadek, i `From day X to day Y`, czyli numery dni, między którymi nastąpił. Dni numerujemy od 1.
- Jeśli ten sam największy spadek wystąpił kilka razy, program wskazuje **pierwsze** takie wystąpienie.
- Program działa poprawnie po zmianie samych wartości w nawiasach klamrowych, także dla pustego wektora i jednego dnia. Nie odczytuje elementów poza zakresem.

W `cpp-workspace` utwórz katalog `largest_drop`, skopiuj do niego `CMakeLists.txt` z oryginalnego `lesson_05_first_program`, utwórz pusty `main.cpp` i napisz program samodzielnie.

**Przykład A:** dane z wymagań.

<!-- output: largest_drop -->
```text
Days recorded: 6
Largest drop: 6
From day 3 to day 4
```

**Przykład B:** `{2, 5, 8}`.

```text
Days recorded: 3
No temperature drop
```

**Przykład C:** `{3}`.

```text
Days recorded: 1
Not enough days
```

Przykłady B i C, jak wszystkie przypadki kontrolne, są sprawdzone automatycznie w pełnej liście kontrolnej poniżej.

**To nie jest program z punktu 7 z innymi danymi.** Tam program tylko wypisywał zmiany. Musisz samodzielnie zdecydować:

1. gdzie przechowywać największy spadek i od jakiej wartości zaczyna;
2. jak rozpoznać, że bieżąca zmiana jest spadkiem, i jak obliczyć jego wielkość;
3. co jeszcze trzeba zapamiętać, żeby wypisać numery dni;
4. kiedy zastąpić zapamiętany wynik nowym, także przy remisie;
5. jak zamienić pozycje w wektorze na numery dni;
6. jak rozpoznać, że spadku nie było;
7. jak obsłużyć pusty wektor i jeden dzień, nie sięgając po nieistniejące elementy.

**Zanim napiszesz program**, przygotuj tabelę przypadków testowych: pusty wektor, jeden dzień, dwa dni ze spadkiem, same wzrosty, same równe temperatury, temperatury ujemne, największy spadek na początku i na końcu, dwa równe największe spadki oraz równe temperatury przed spadkiem. Przy każdym przypadku zapisz oczekiwane standardowe wyjście.

**Potem pracuj w tej kolejności:**

1. Napisz program i uruchom go dla danych z wymagań.
2. Zmieniaj kolejno wartości w nawiasach klamrowych na przypadki z tabeli. Przed każdym uruchomieniem przewidź wynik.
3. Przy każdej niezgodności sprawdź, czy błąd jest w programie, czy w tabeli.

### Kryterium sukcesu

- Program buduje się jako C++20, a dla danych z wymagań wypisuje dokładnie trzy linijki przykładu A.
- Dla każdego przypadku z tabeli wynik zgadza się z wymaganiami, po zmianie samych wartości w nawiasach klamrowych.
- Przy remisie program wskazuje pierwsze wystąpienie największego spadku.
- Żaden indeks w programie nie wychodzi poza zakres, także dla pustego wektora i jednego dnia.
- Indeksy są typu `std::size_t`, a numery dni wypisywane użytkownikowi zaczynają się od 1.
- Tabela przypadków powstała przed uruchomieniem programu.
- Umiesz wyjaśnić, od którego indeksu zaczyna się Twoja pętla i dlaczego.

Gdy wynik się zgadza, możesz zapisać projekt w Gicie, jak w lekcji 1.5.

<details>
<summary>Podpowiedź 1</summary>

Aby znaleźć zmianę temperatury, które dwa kolejne elementy trzeba porównać?

</details>

<details>
<summary>Podpowiedź 2</summary>

Zastanów się, od którego indeksu możesz bezpiecznie korzystać z bieżącego i poprzedniego elementu.

</details>

<details>
<summary>Podpowiedź 3</summary>

Podczas przeglądania par zapamiętuj najlepszy dotąd dodatni spadek i jego pozycję. Przy remisie wymaganie mówi, aby zachować pierwsze wystąpienie.

</details>

<details>
<summary>Pełna lista przypadków kontrolnych: otwórz po przygotowaniu własnej tabeli</summary>

| Temperatury | Standardowe wyjście po `Days recorded: N` | Co sprawdza |
|---|---|---|
| `{}` | `Not enough days` | pusty wektor |
| `{3}` | `Not enough days` | przykład C: jeden dzień |
| `{8, 5}` | spadek 3, dni 1–2 | najmniejsza para |
| `{2, 5, 8}` | `No temperature drop` | przykład B: same wzrosty |
| `{4, 4, 4}` | `No temperature drop` | zmiana 0 to nie spadek |
| `{8, 5, 7, 1, 0, 3}` | spadek 6, dni 3–4 | przykład A |
| `{9, 5, 1}` | spadek 4, dni 1–2 | remis: pierwsze wystąpienie, na początku |
| `{7, 1, 7, 1}` | spadek 6, dni 1–2 | remis rozdzielony wzrostem |
| `{-2, -7, -9, -4}` | spadek 5, dni 1–2 | temperatury ujemne |
| `{6, 6, 3, 3}` | spadek 3, dni 2–3 | równe temperatury przed spadkiem i po nim |
| `{1, -20, 40, 0}` | spadek 40, dni 3–4 | dwa spadki, większy na końcu |

W ostatnim przypadku spadek między dniami 1 i 2 wynosi 21, a między dniami 3 i 4 wynosi 40. Program wybiera większy.

**Jak sprawdzono te wyniki.** Program misji ma dane w kodzie, więc każdy zestaw wymagałby osobnego programu. Dlatego wszystkie przypadki sprawdza jeden program kontrolny: ten sam algorytm co rozwiązanie referencyjne, ale temperatury odczytuje z wejścia, najpierw ich liczbę, a potem kolejne wartości. Nie wypisuje pytań, więc jego standardowe wyjście jest takie samo jak wynik misji dla tych danych. Ten program i jego wyniki są w części [Przykładowe rozwiązania](#przykładowe-rozwiązania). Otwórz je dopiero po napisaniu własnego programu, bo zawierają rozwiązanie.

</details>

Przykładowe rozwiązanie jest w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 9. Znajdź błąd: który remis?

To zadanie wykonaj **po misji**: program poniżej zawiera cały algorytm szukania największego spadku. Odczytuje temperatury z wejścia, tak jak program kontrolny: najpierw liczbę dni, potem kolejne temperatury. Zgodnie z wymaganiem przy remisie powinien wskazać pierwsze wystąpienie.

<details>
<summary>Program do sprawdzenia: otwórz po napisaniu własnego programu</summary>

<!-- example: drop_tie_bug -->
```cpp
#include <cstddef>
#include <iostream>
#include <vector>

int main() {
    std::vector<int> temperatures{};
    int day_count{0};
    std::cin >> day_count;

    for (int day{1}; day <= day_count; ++day) {
        int temperature{0};
        std::cin >> temperature;
        temperatures.push_back(temperature);
    }

    if (std::cin.fail()) {
        std::cout << "Input could not be read\n";
    } else {
        std::cout << "Days recorded: " << temperatures.size() << "\n";

        if (temperatures.size() < 2) {
            std::cout << "Not enough days\n";
        } else {
            int largest_drop{0};
            std::size_t drop_index{0};

            for (std::size_t index{1}; index < temperatures.size(); ++index) {
                const int drop{temperatures[index - 1] - temperatures[index]};

                if (drop >= largest_drop) {
                    largest_drop = drop;
                    drop_index = index;
                }
            }

            if (largest_drop == 0) {
                std::cout << "No temperature drop\n";
            } else {
                std::cout << "Largest drop: " << largest_drop << "\n";
                std::cout << "From day " << drop_index << " to day " << drop_index + 1 << "\n";
            }
        }
    }
}
```

1. **Przewidź** wynik dla danych A, `6`, `8`, `5`, `7`, `1`, `0`, `3`, z jednym największym spadkiem.
2. Uruchom program z tymi danymi i sprawdź, że wynik wygląda poprawnie.
3. Przeanalizuj dane `4`, `7`, `1`, `7`, `1`, z dwoma równymi największymi spadkami. Który spadek powinien wskazać program?
4. Uruchom program z tymi danymi. Którą parę dni wskazuje?
5. Znajdź warunek, który decyduje o zapisaniu nowego wyniku.
6. Popraw program.
7. Sprawdź ponownie oba przypadki.

</details>

Wyniki programu przed poprawką i poprawiony program są w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 10. Gdy coś pójdzie inaczej

| Co widzisz | Co to znaczy | Co zrobić |
|---|---|---|
| `cannot be narrowed from type ... to 'int'` | Wynik `size()` trafia do zmiennej `int` z `{}` (punkt 5). | Użyj `std::size_t`. |
| `comparison of integers of different signs` | Indeks `int` jest porównywany z `size()`. | Zadeklaruj indeks jako `std::size_t`. |
| Błąd kompilacji przy `std::size_t` | Brakuje `#include <cstddef>` albo w nazwie jest literówka. Na niektórych systemach program zbuduje się i bez `<cstddef>`, ale na innych nie. | Dopisz `#include <cstddef>`. |
| Numery dni są o jeden za małe, na przykład `From day 2 to day 3` zamiast `From day 3 to day 4` | Program wypisuje indeksy zamiast numerów dni. | Numer dnia to indeks + 1. Sprawdź, który indeks zapamiętujesz: bieżący czy poprzedni. |
| Spadek wychodzi ujemny albo w miejscu wzrostu | Odejmowanie w odwrotnej kolejności. | Spadek to temperatura wcześniejszego dnia minus temperatura następnego. |
| Przy remisie program wskazuje ostatnie wystąpienie | Warunek zapisuje nowy wynik także wtedy, gdy jest równy zapamiętanemu (punkt 9). | Zapisuj tylko wynik ściśle większy. |
| Program wypisuje dziwne liczby albo kończy się nieoczekiwanie | Prawdopodobnie odczyt poza zakresem: indeks równy `size()` albo `index - 1` dla indeksu 0. | Sprawdź warunek i wartość początkową pętli. Pętla po sąsiadach zaczyna od indeksu 1. |

## 11. Wyjaśnij

Odpowiedz własnymi słowami, najlepiej na piśmie. Dopiero potem porównaj z przykładowymi odpowiedziami.

1. Po co są indeksy, skoro pętla zakresowa przegląda wszystkie elementy?
2. Jaki indeks ma pierwszy element, a jaki ostatni element wektora z 5 elementami?
3. Czy `values[5]` jest poprawne dla wektora z 5 elementami? Co się stanie?
4. Dlaczego przed odczytem `values[values.size() - 1]` sprawdzamy `empty()`?
5. Czym jest `std::size_t` i dlaczego go używamy?
6. Dlaczego `const int count{values.size()};` się nie buduje?
7. Dlaczego w programie z dniami wypisujemy `index + 1`?
8. Dlaczego pętla po sąsiadach zaczyna od indeksu 1?
9. Ile par sąsiadów ma wektor z 4 elementami? A z jednym i z zerem elementów?
10. Kiedy wybrać pętlę zakresową, a kiedy pętlę po indeksach?
11. Dlaczego w misji przy remisie warunek ma `>`, a nie `>=`?

<details>
<summary>Przykładowe odpowiedzi</summary>

1. Bo niektóre zadania wymagają pozycji elementu: odczytu konkretnego elementu albo porównania go z poprzednim. Pętla zakresowa daje wartości, ale nie ich pozycje.
2. Pierwszy ma indeks 0, ostatni 4, czyli `size() - 1`.
3. Nie. Poprawne indeksy to 0–4. `values[5]` to odczyt poza zakresem, czyli niezdefiniowane zachowanie: nie wiadomo, co się stanie, i nie wolno na tym polegać. `[]` niczego nie sprawdza.
4. Bo pusty wektor nie ma ostatniego elementu, a `size() - 1` dla rozmiaru 0 nie daje −1, tylko ogromną liczbę dodatnią, bo wynik `size()` nie ma znaku.
5. To typ całkowity bez znaku, przeznaczony do rozmiarów i indeksów. Pasuje do wyniku `size()`, więc nie ma konwersji zawężającej ani porównań liczb ze znakiem i bez znaku.
6. Bo `{}` nie pozwala na konwersję zawężającą: typ, który podaje `size()`, nie zawsze zmieści się w `int` bez zmiany wartości.
7. Bo użytkownik liczy dni od 1, a indeksy zaczynają się od 0. Pozycja w wektorze i numer pokazywany człowiekowi to dwie różne rzeczy.
8. Bo porównujemy element z poprzednim, a element o indeksie 0 poprzednika nie ma. Dla każdego indeksu od 1 poprzednik istnieje.
9. Trzy pary. Jeden element i zero elementów nie tworzą żadnej pary, a pętla od indeksu 1 nie wykonuje wtedy żadnego przebiegu.
10. Pętlę zakresową, gdy potrzebujesz tylko kolejnych wartości. Pętlę po indeksach, gdy potrzebujesz też pozycji: numeru elementu albo sąsiedniego elementu.
11. Bo przy remisie wynik ma wskazywać pierwsze wystąpienie. Z `>` drugi, równy spadek nie zastępuje zapamiętanego. Z `>=` zastąpiłby go, więc program wskazałby ostatnie wystąpienie.

</details>

## Podsumowanie

- `values[index]` odczytuje element o podanym **indeksie**. Indeksy zaczynają się od 0, więc wektor z `N` elementami ma indeksy od 0 do `N - 1`.
- `[]` nie sprawdza zakresu. Odczyt poza zakresem to niezdefiniowane zachowanie, więc pilnujesz, żeby każdy indeks był poprawny.
- Pierwszy element to `values[0]`, ostatni `values[values.size() - 1]`, oba tylko dla niepustego wektora.
- Rozmiary i indeksy przechowujesz w `std::size_t` z `<cstddef>`. Nie zapisujesz `size()` w `int` i nie porównujesz z nim zmiennych `int`.
- Pętla po indeksach: `for (std::size_t index{0}; index < values.size(); ++index)`. Kończy się, gdy indeks osiągnie `size()`, bez odczytu nieistniejącego elementu.
- Numer pokazywany użytkownikowi to `index + 1`. Indeksowanie wektora się nie zmienia.
- Pary sąsiadów przeglądasz od indeksu 1: `values[index]` i `values[index - 1]`. Ta pętla jest bezpieczna także dla pustego i jednoelementowego wektora.
- Gdy pozycja nie jest potrzebna, pętla zakresowa nadal jest dobrym wyborem.

## Co dalej

Do tej pory cały program z wektorem mieścił się w `main`. W kolejnej lekcji przekażesz wektor do własnej funkcji, która go tylko odczytuje. Lekcja jest w przygotowaniu.

---

## Przykładowe rozwiązania

Zajrzyj tutaj **po własnej próbie**. Twoje nazwy mogą się różnić, jeśli standardowe wyjście jest takie, jak wymagane.

<details>
<summary>Punkt 8: misja, największe ochłodzenie</summary>

<!-- example: largest_drop -->
```cpp
#include <cstddef>
#include <iostream>
#include <vector>

int main() {
    const std::vector<int> temperatures{8, 5, 7, 1, 0, 3};

    std::cout << "Days recorded: " << temperatures.size() << "\n";

    if (temperatures.size() < 2) {
        std::cout << "Not enough days\n";
    } else {
        int largest_drop{0};
        std::size_t drop_index{0};

        for (std::size_t index{1}; index < temperatures.size(); ++index) {
            const int drop{temperatures[index - 1] - temperatures[index]};

            if (drop > largest_drop) {
                largest_drop = drop;
                drop_index = index;
            }
        }

        if (largest_drop == 0) {
            std::cout << "No temperature drop\n";
        } else {
            std::cout << "Largest drop: " << largest_drop << "\n";
            std::cout << "From day " << drop_index << " to day " << drop_index + 1 << "\n";
        }
    }
}
```

1. **Pętla zaczyna od indeksu 1**, bo każda para to bieżący dzień i poprzedni, a pierwszy dzień poprzedniego nie ma.
2. **Poprzedni element jest dostępny**, bo dla `index` od 1 wzwyż `index - 1` to istniejący indeks, a warunek `index < temperatures.size()` pilnuje bieżącego.
3. **Spadek** to temperatura wcześniejszego dnia minus następnego: `temperatures[index - 1] - temperatures[index]`. Jest dodatni tylko wtedy, gdy temperatura spadła. Wzrost daje liczbę ujemną, a równe temperatury 0.
4. **Najlepsza para:** `largest_drop` pamięta największy dotąd spadek, a `drop_index` indeks dnia **po** spadku. Wartość początkowa 0 oznacza „jeszcze żadnego spadku”: tylko dodatni spadek może ją zastąpić. Dlatego `largest_drop == 0` po pętli znaczy, że spadku nie było.
5. **Remis:** warunek `drop > largest_drop` zastępuje wynik tylko spadkiem ściśle większym. Równy spadek później nic nie zmienia, więc zostaje pierwsze wystąpienie.
6. **Numery dni:** para o indeksach `drop_index - 1` i `drop_index` to dni o numerach `drop_index` i `drop_index + 1`, bo numer dnia to indeks + 1.
7. **Pusty i jednoelementowy wektor** nie mają żadnej pary, więc program wypisuje `Not enough days` i w ogóle nie zaczyna porównań. Sama pętla też by się wtedy nie wykonała, ale bez tego sprawdzenia program wypisałby `No temperature drop`, jakby porównał jakieś dni.

To czytelne rozwiązanie, ale nie jedyne. Można na przykład zapamiętywać indeks dnia przed spadkiem zamiast po nim, jeśli numery dni są potem przeliczone poprawnie.

**Program kontrolny** sprawdza wszystkie przypadki z listy kontrolnej. Część po odczycie danych jest taka sama jak w rozwiązaniu wyżej, poza wcięciem. Różni się tylko źródłem danych: wektor nie ma `const`, bo program dodaje do niego odczytane temperatury przez `push_back`, jak w lekcji 6.2.

<!-- example: largest_drop_check -->
```cpp
#include <cstddef>
#include <iostream>
#include <vector>

int main() {
    std::vector<int> temperatures{};
    int day_count{0};
    std::cin >> day_count;

    for (int day{1}; day <= day_count; ++day) {
        int temperature{0};
        std::cin >> temperature;
        temperatures.push_back(temperature);
    }

    if (std::cin.fail()) {
        std::cout << "Input could not be read\n";
    } else {
        std::cout << "Days recorded: " << temperatures.size() << "\n";

        if (temperatures.size() < 2) {
            std::cout << "Not enough days\n";
        } else {
            int largest_drop{0};
            std::size_t drop_index{0};

            for (std::size_t index{1}; index < temperatures.size(); ++index) {
                const int drop{temperatures[index - 1] - temperatures[index]};

                if (drop > largest_drop) {
                    largest_drop = drop;
                    drop_index = index;
                }
            }

            if (largest_drop == 0) {
                std::cout << "No temperature drop\n";
            } else {
                std::cout << "Largest drop: " << largest_drop << "\n";
                std::cout << "From day " << drop_index << " to day " << drop_index + 1 << "\n";
            }
        }
    }
}
```

Dane wejściowe to liczba dni, a po niej temperatury. Kolejność przypadków jest taka jak w liście kontrolnej.

<!-- input: largest_drop_check -->
```text
0
```

<!-- output: largest_drop_check -->
```text
Days recorded: 0
Not enough days
```

<!-- input: largest_drop_check -->
```text
1
3
```

<!-- output: largest_drop_check -->
```text
Days recorded: 1
Not enough days
```

<!-- input: largest_drop_check -->
```text
2
8
5
```

<!-- output: largest_drop_check -->
```text
Days recorded: 2
Largest drop: 3
From day 1 to day 2
```

<!-- input: largest_drop_check -->
```text
3
2
5
8
```

<!-- output: largest_drop_check -->
```text
Days recorded: 3
No temperature drop
```

<!-- input: largest_drop_check -->
```text
3
4
4
4
```

<!-- output: largest_drop_check -->
```text
Days recorded: 3
No temperature drop
```

<!-- input: largest_drop_check -->
```text
6
8
5
7
1
0
3
```

<!-- output: largest_drop_check -->
```text
Days recorded: 6
Largest drop: 6
From day 3 to day 4
```

<!-- input: largest_drop_check -->
```text
3
9
5
1
```

<!-- output: largest_drop_check -->
```text
Days recorded: 3
Largest drop: 4
From day 1 to day 2
```

<!-- input: largest_drop_check -->
```text
4
7
1
7
1
```

<!-- output: largest_drop_check -->
```text
Days recorded: 4
Largest drop: 6
From day 1 to day 2
```

<!-- input: largest_drop_check -->
```text
4
-2
-7
-9
-4
```

<!-- output: largest_drop_check -->
```text
Days recorded: 4
Largest drop: 5
From day 1 to day 2
```

<!-- input: largest_drop_check -->
```text
4
6
6
3
3
```

<!-- output: largest_drop_check -->
```text
Days recorded: 4
Largest drop: 3
From day 2 to day 3
```

<!-- input: largest_drop_check -->
```text
4
1
-20
40
0
```

<!-- output: largest_drop_check -->
```text
Days recorded: 4
Largest drop: 40
From day 3 to day 4
```

</details>

<details>
<summary>Punkt 9: wyniki przed poprawką i poprawiony program</summary>

Przed poprawką, dla danych A:

<!-- input: drop_tie_bug -->
```text
6
8
5
7
1
0
3
```

<!-- output: drop_tie_bug -->
```text
Days recorded: 6
Largest drop: 6
From day 3 to day 4
```

Dla danych `4`, `7`, `1`, `7`, `1`:

<!-- input: drop_tie_bug -->
```text
4
7
1
7
1
```

<!-- output: drop_tie_bug -->
```text
Days recorded: 4
Largest drop: 6
From day 3 to day 4
```

- Dla danych A wynik jest poprawny, bo największy spadek występuje tylko raz.
- Dla `7`, `1`, `7`, `1` spadek 6 występuje dwa razy: między dniami 1 i 2 oraz 3 i 4. Wymaganie mówi o pierwszym wystąpieniu, a program wskazuje dni 3–4.
- **Przyczyna:** warunek `drop >= largest_drop` zapisuje nowy wynik także wtedy, gdy spadek jest **równy** zapamiętanemu. Drugi spadek 6 zastępuje więc pierwszy.
- **Poprawka:** zmień `>=` na `>`. Wtedy wynik zastępuje tylko spadek ściśle większy.

Poprawiony program to program kontrolny z punktu 8: różni się od programu z błędem tylko tym jednym znakiem. Dla obu powyższych zestawów danych daje wyniki z listy kontrolnej: dla A dni 3–4, a dla `7`, `1`, `7`, `1` dni 1–2.

</details>

**Poprzednia lekcja:** [Lekcja 6.2: Dodawanie danych do wektora: `push_back()` i `empty()`](lesson_02_adding_to_a_vector.md) · **Następna lekcja:** w przygotowaniu · [Opis kursu](../../README.md)

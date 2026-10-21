# Lekcja 2.5: Liczby z częścią ułamkową: `double` i `auto`

**Polski** · [English](lesson_05_numbers_with_a_fractional_part.en.md) · [Opis kursu](../../README.md)

> **Moduł 2, lekcja 5** · około 75 minut
> **Potrzebujesz:** katalogu `cpp-workspace` i oryginalnego projektu `lesson_05_first_program`, jak dotąd. Debugger nie jest w tej lekcji potrzebny.
> **Wersja pilotażowa.** Przykłady z tej lekcji sprawdzamy automatycznie na Windowsie, Ubuntu i macOS.

## Zanim zaczniesz

Ta lekcja zakłada, że po lekcji 2.4:

- wiesz, że `7 / 2` daje w C++ `3`, bo oba operandy są całkowite i `/` wykonuje dzielenie całkowite;
- przewidujesz grupowanie działań, dopisując niewidoczne nawiasy;
- tworzysz stałe `const int` z wartością początkową w `{}`.

## Sytuacja

W lekcji 2.4 dzielenie liczb całkowitych zawsze dawało liczbę całkowitą. Ale wiele wielkości ma część ułamkową: odległość 7,5 km, czas 2,5 godziny, średnia z kilku pomiarów. Dziś poznasz typ `double`, który przechowuje takie liczby, i zobaczysz, że **typ wartości biorących udział w obliczeniu decyduje o tym, jakie to obliczenie jest i jaki da wynik**. Na koniec poznasz `auto`: sposób, w jaki kompilator sam ustala typ zmiennej na podstawie jej wartości początkowej.

Po tej lekcji będziesz:

- odróżniać liczby całkowite od liczb z częścią ułamkową i zapisywać literały typu `double`, na przykład `7.0` i `2.5`;
- tworzyć zmienne i stałe typu `double`;
- wyjaśniać różnicę między `7 / 2` a `7.0 / 2`;
- wiedzieć, że typ zmiennej wynikowej nie naprawia wcześniejszego dzielenia całkowitego;
- przewidywać wyniki prostych działań łączących `int` i `double`;
- wiedzieć, że `double` przechowuje wartości przybliżone;
- wyjaśniać, na jakiej podstawie `auto` ustala typ i że ten typ się potem nie zmienia;
- samodzielnie dobierać typy w programie z obliczeniami.

## 1. Przygotuj projekt

W `cpp-workspace` utwórz katalog `lesson_2_5` i skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program`. Programy z punktów 2–11 wpisujesz w `main.cpp` tego katalogu.

## 2. Dwie wersje tego samego dzielenia

Zastąp zawartość `main.cpp` tym programem:

<!-- example: two_divisions -->
```cpp
#include <iostream>

int main() {
    std::cout << (7 / 2) << "\n";
    std::cout << (7.0 / 2) << "\n";
}
```

**Przewidź** oba wyniki. Zapisz je, a potem uruchom program.

<details>
<summary>Wynik programu</summary>

<!-- output: two_divisions -->
```text
3
3.5
```

</details>

Pierwsza linijka to znane z lekcji 2.4 dzielenie całkowite. Druga różni się tylko zapisem jednej liczby, a daje inny wynik:

- `7` i `2` to **literały całkowite**: liczby typu `int`, zapisane wprost w kodzie;
- `7.0` to **literał typu `double`**: liczba z częścią ułamkową, nawet jeśli ta część jest zerem;
- gdy oba operandy `/` są całkowite, wykonuje się dzielenie całkowite i wynik jest całkowity;
- gdy jeden z operandów jest typu `double`, drugi zostaje do tego obliczenia przekształcony w `double`. Wykonuje się wtedy **dzielenie zmiennoprzecinkowe**, którego wynik może mieć część ułamkową.

Ta zasada dotyczy prostych działań z tej lekcji: `+`, `-`, `*` i `/`, w których biorą udział liczby `int` i `double`. Nie jest to pełna lista zasad łączenia typów w C++. Operator `%` z lekcji 2.4 działa tylko dla liczb całkowitych, więc z `double` go nie używamy.

## 3. Typ `double`

Typ `double` przechowuje liczby z częścią ułamkową. Tak zapiszesz kilka zwykłych pomiarów:

<!-- example: double_values -->
```cpp
#include <iostream>

int main() {
    const double distance_km{7.5};
    const double walk_time_h{2.5};
    const double shelf_length_m{0.75};
    const double measured_length_m{3.0};

    std::cout << "Distance: " << distance_km << " km\n";
    std::cout << "Walk time: " << walk_time_h << " h\n";
    std::cout << "Shelf length: " << shelf_length_m << " m\n";
    std::cout << "Measured length: " << measured_length_m << " m\n";
}
```

**Przewidź**, co wypisze ostatnia linijka, a potem uruchom program.

<details>
<summary>Wynik programu</summary>

<!-- output: double_values -->
```text
Distance: 7.5 km
Walk time: 2.5 h
Shelf length: 0.75 m
Measured length: 3 m
```

</details>

- W kodzie część ułamkową zawsze oddziela się **kropką**, nie przecinkiem: `7.5`, a nie `7,5`. Tak samo w polskiej wersji kursu.
- `measured_length_m` jest typu `double` i ma wartość `3.0`, ale `std::cout` wypisuje ją jako `3`. **Z tego, jak liczba wygląda na ekranie, nie zawsze rozpoznasz jej typ.** Typ odczytuje się z kodu.
- Typ `double` nadaje się do wielkości mierzonych: odległości, czasu, długości, średnich. Nie używamy go w tej lekcji do pieniędzy, bo dokładne kwoty wymagają osobnego podejścia.
- W C++ są też inne typy liczbowe. Na razie poznajesz dwa: `int` dla liczb całkowitych i `double` dla liczb z częścią ułamkową.

## 4. Typ zmiennej nie zmienia przeszłości

Co się stanie, gdy wynik dzielenia całkowitego trafi do zmiennej typu `double`?

<!-- example: type_too_late -->
```cpp
#include <iostream>

int main() {
    const double first{7 / 2};
    const double second{7.0 / 2};

    std::cout << "first: " << first << "\n";
    std::cout << "second: " << second << "\n";
}
```

**Przewidź** obie wartości, a potem uruchom program.

<details>
<summary>Wynik programu</summary>

<!-- output: type_too_late -->
```text
first: 3
second: 3.5
```

</details>

- `first` jest typu `double`, ale przechowuje **3**. Dlaczego? Najpierw obliczana jest wartość początkowa `7 / 2`. Oba operandy są całkowite, więc to dzielenie całkowite i wynik to 3. Dopiero ta gotowa wartość trafia do `first`.
- `second` przechowuje **3.5**, bo w `7.0 / 2` jeden operand jest typu `double`.
- **Rodzaj dzielenia zależy od operandów**, a nie od typu zmiennej, do której trafi wynik. Zmienna typu `double` nie każe wykonać obliczenia jeszcze raz: dostaje wartość, która już powstała.
- `first` wypisuje się jako `3`, a nie `3.0`. Jak w punkcie 3: wygląd na ekranie nie mówi, jakiego typu jest wartość.

### Sprawdź: połowa

Ten program miał zapisać połowę:

<!-- example: half_bug -->
```cpp
#include <iostream>

int main() {
    const double half{1 / 2};
    std::cout << "half: " << half << "\n";
}
```

1. **Przewidź**, co wypisze ten program.
2. Wyjaśnij, skąd ten wynik.
3. Popraw program tak, żeby wypisał `half: 0.5`. Nie zmieniaj typu `half`.

<details>
<summary>Wynik, wyjaśnienie i poprawka: przeczytaj po własnej próbie</summary>

<!-- output: half_bug -->
```text
half: 0
```

`1 / 2` to dzielenie całkowite: 2 nie mieści się w 1 ani razu, więc wynik to 0. To, że `half` jest typu `double`, niczego nie zmienia. Wystarczy, żeby jeden operand był typu `double`:

<!-- example: half_fixed -->
```cpp
#include <iostream>

int main() {
    const double half{1.0 / 2};
    std::cout << "half: " << half << "\n";
}
```

<!-- output: half_fixed -->
```text
half: 0.5
```

</details>

## 5. Mieszanie `int` i `double`

Ktoś skacze w dal trzy razy i chce poznać średnią długość skoku. Długości to pomiary, więc są typu `double`. Liczba skoków to liczba całkowita, więc jest typu `int`:

<!-- example: average_jump -->
```cpp
#include <iostream>

int main() {
    const double first_jump_m{1.5};
    const double second_jump_m{2.5};
    const double third_jump_m{3.5};
    const int jumps{3};

    const double average_jump_m{(first_jump_m + second_jump_m + third_jump_m) / jumps};

    std::cout << "Average jump: " << average_jump_m << " m\n";
}
```

<!-- output: average_jump -->
```text
Average jump: 2.5 m
```

Suma w nawiasie to `double` (7.5). Dzielona jest przez `jumps`, które jest typu `int`. Jeden operand jest typu `double`, więc to dzielenie zmiennoprzecinkowe, a wynik to 2.5. Nawias jest potrzebny z powodów z lekcji 2.4: bez niego przez `jumps` dzieliłby się tylko trzeci skok.

**Zasada dla prostych działań z tej lekcji:** jeśli w `+`, `-`, `*` albo `/` jeden operand jest typu `int`, a drugi typu `double`, obliczenie wykonuje się na `double` i wynik jest typu `double`. W dłuższym wyrażeniu ta zasada dotyczy **każdego działania osobno**, w kolejności grupowania z lekcji 2.4.

### Przewidź samodzielnie: siedem wyrażeń

Przepisz tabelę. Dla każdego wyrażenia **przewidź** wynik i zaznacz, czy po drodze jest dzielenie całkowite. Najpierw dopisz niewidoczne nawiasy.

| | Wyrażenie | Czy jest dzielenie całkowite? | Przewidywanie | Wynik programu |
|---|---|---|---|---|
| a | `7 / 2` | | | |
| b | `7 / 2.0` | | | |
| c | `1.5 + 2` | | | |
| d | `2.5 * 2` | | | |
| e | `10 - 0.25` | | | |
| f | `1 / 2 * 4.0` | | | |
| g | `1.0 / 2 * 4` | | | |

Dopiero gdy tabela jest wypełniona, uruchom program:

<!-- example: mixed_predictions -->
```cpp
#include <iostream>

int main() {
    std::cout << "a: " << (7 / 2) << "\n";
    std::cout << "b: " << (7 / 2.0) << "\n";
    std::cout << "c: " << (1.5 + 2) << "\n";
    std::cout << "d: " << (2.5 * 2) << "\n";
    std::cout << "e: " << (10 - 0.25) << "\n";
    std::cout << "f: " << (1 / 2 * 4.0) << "\n";
    std::cout << "g: " << (1.0 / 2 * 4) << "\n";
}
```

<details>
<summary>Wynik programu</summary>

<!-- output: mixed_predictions -->
```text
a: 3
b: 3.5
c: 3.5
d: 5
e: 9.75
f: 0
g: 2
```

</details>

Wypełniona tabela z wyjaśnieniem jest w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

**Nie dopisuj `.0` wszędzie.** Liczba skoków, uczniów czy okrążeń jest całkowita i powinna pozostać `int`. Obliczenie zmiennoprzecinkowe jest potrzebne wtedy, gdy wielkość może mieć część ułamkową albo gdy wynik ma ją mieć, na przykład średnia. Wtedy przynajmniej jeden operand dzielenia musi być typu `double`. Najlepiej, gdy jest nim ta wartość, która naturalnie ma część ułamkową, jak długość albo czas.

## 6. `double` jest przybliżeniem

`double` nie jest matematyczną liczbą o dowolnej dokładności. Komputer zapisuje go w postaci dwójkowej, a **nie każdą liczbę dziesiętną da się tak zapisać dokładnie**. Na przykład 0.1 jest w `double` przechowywane jako wartość bardzo bliska 0.1, ale nie dokładnie 0.1. Dlatego wyniki niektórych obliczeń są przybliżone.

Zwykle tego nie widać: `std::cout` domyślnie wypisuje `double` w skróconej postaci, z najwyżej sześcioma cyframi znaczącymi. Pamiętaj jednak, że wypisana liczba nie zawsze jest dokładnie tą, którą przechowuje program.

W tym kursie przykłady korzystają na razie z wartości takich jak `0.5`, `0.25`, `1.5`, `2.5`, `3.75`, które `double` zapisuje dokładnie. Ich wyniki są przewidywalne i takie same na każdym systemie. Jak pracować z przybliżeniami w poważniejszych obliczeniach, poznasz później.

## 7. Nawiasy klamrowe pilnują wartości

Wartość początkową zapisujesz w `{}`, tak jak dotąd: `int count{3};`, `double average{2.5};`. Ten zapis ma jeszcze jedną zaletę. Co się stanie, gdy w zmiennej `int` spróbujesz zapisać liczbę z częścią ułamkową? **Przewidź**, a potem zbuduj:

<!-- broken: narrowing at=4 errors=1 error=^type 'double' cannot be narrowed to 'int' in initializer list -->
```cpp
#include <iostream>

int main() {
    const int ticket_count{2.5};
    std::cout << ticket_count << "\n";
}
```

Program się nie zbuduje. Kompilator zgłasza w linijce 4 `type 'double' cannot be narrowed to 'int' in initializer list`, czyli: typu `double` nie można zawęzić do `int` w nawiasach klamrowych. W tej samej linijce wypisuje też ostrzeżenie `implicit conversion from 'double' to 'int' changes value from 2.5 to 2`: po takiej zmianie 2.5 stałoby się 2. Liczba 2.5 nie zmieści się w `int` bez utraty części ułamkowej. Taką zmianę typu, która mogłaby zmienić wartość, nazywa się **konwersją zawężającą**. Inicjalizacja przez `{}` na nią nie pozwala: zamiast po cichu zapisać w `ticket_count` liczbę 2, kompilator zatrzymuje budowanie. Linijkę `note:` z radą o jawnej zmianie typu (*explicit cast*) na razie pomiń: tutaj właściwą poprawką jest dobranie typu.

Przywróć poprawny kod. Liczba biletów jest całkowita, więc wpisz na przykład `{2}`. Gdyby wartość naprawdę miała mieć część ułamkową, zmienna musiałaby być typu `double`.

Nie każda zmiana typu jest błędem. Liczbę całkowitą można zapisać w `double` bez straty, więc to się buduje i działa:

<!-- example: whole_number_in_double -->
```cpp
#include <iostream>

int main() {
    const double distance_km{7};
    std::cout << "Distance: " << distance_km << " km\n";
}
```

<!-- output: whole_number_in_double -->
```text
Distance: 7 km
```

## 8. `auto`: typ z wartości początkowej

Do tej pory przy każdej zmiennej pisano typ: `int` albo `double`. Zamiast typu można napisać `auto`. Wtedy **kompilator sam ustala typ na podstawie wartości początkowej**:

<!-- example: auto_types -->
```cpp
#include <iostream>

int main() {
    auto ticket_count{3};
    auto distance_km{7.5};
    auto first{7 / 2};
    auto second{7.0 / 2};

    std::cout << "ticket_count: " << ticket_count << "\n";
    std::cout << "distance_km: " << distance_km << "\n";
    std::cout << "first: " << first << "\n";
    std::cout << "second: " << second << "\n";
}
```

**Przewidź** typ i wartość każdej zmiennej, a potem uruchom program.

<details>
<summary>Wynik programu</summary>

<!-- output: auto_types -->
```text
ticket_count: 3
distance_km: 7.5
first: 3
second: 3.5
```

</details>

| Deklaracja | Wartość początkowa | Typ ustalony przez kompilator | Wartość |
|---|---|---|---|
| `auto ticket_count{3};` | literał całkowity | `int` | 3 |
| `auto distance_km{7.5};` | literał z kropką | `double` | 7.5 |
| `auto first{7 / 2};` | dzielenie dwóch `int` | `int` | 3 |
| `auto second{7.0 / 2};` | dzielenie `double` przez `int` | `double` | 3.5 |

- `auto` **nie oznacza** „dowolny typ”. Każda z tych zmiennych ma jeden, konkretny typ, który kompilator ustalił z wartości początkowej, jeszcze przed uruchomieniem programu.
- Ten typ się **nie zmienia** w trakcie działania programu. `ticket_count` jest typu `int` od deklaracji do końca, tak jakby napisano `int ticket_count{3};`.
- `auto` **nie wykonuje** dodatkowego obliczenia i niczego nie naprawia. `first` dostaje wynik dzielenia całkowitego, czyli 3, a jego typ to `int`, bo taki jest wynik `7 / 2`.
- Te wartości się nie zmieniają, więc zgodnie z zasadą z lekcji 2.2 mogłyby mieć też `const`, na przykład `const auto ticket_count{3};`. Tutaj go pominięto, żeby skupić się na `auto`.

Typ zmiennej z `auto` ustalasz tak, jak robi to kompilator: patrzysz na wartość początkową i stosujesz zasady z punktów 2–5.

## 9. `auto` czy jawny typ?

`auto` nie zastępuje typów wszędzie. Porównaj:

<!-- example: auto_or_explicit -->
```cpp
#include <iostream>

int main() {
    const double daily_distance_km{7.5};
    const int days{3};

    const auto total_distance_km{daily_distance_km * days};

    std::cout << "Total distance: " << total_distance_km << " km\n";
}
```

<!-- output: auto_or_explicit -->
```text
Total distance: 22.5 km
```

- Przy **danych** `daily_distance_km` i `days` jawny typ mówi czytelnikowi, czym jest wartość: odległość z częścią ułamkową i liczba całkowita. Gdyby było tu `auto`, typ też by się ustalił, ale zależałby od tego, czy ktoś napisał `7.5`, czy `7`.
- Przy **wyniku** `total_distance_km` typ jasno wynika z obliczenia: `double` razy `int` daje `double`. `auto` niczego tu nie ukrywa.

Program z samymi jawnymi typami jest tak samo dobry. `auto` to wygoda, nie obowiązek. Jeśli nie masz pewności, jaki typ ustali kompilator, napisz typ jawnie.

## 10. Napraw obliczenie

Wstążka ma 10 m długości i trzeba ją pociąć na 4 równe kawałki. **Wymaganie:** program ma wypisać długość jednego kawałka.

**Krok 1. Przewidź poprawny wynik** na podstawie opisu.

**Krok 2. Uruchom program** i porównaj wynik z przewidywaniem:

<!-- example: ribbon_bug -->
```cpp
#include <iostream>

int main() {
    const int ribbon_length_m{10};
    const int pieces{4};

    const double piece_length_m{ribbon_length_m / pieces};

    std::cout << "Piece length: " << piece_length_m << " m\n";
}
```

<details>
<summary>Wynik programu</summary>

<!-- output: ribbon_bug -->
```text
Piece length: 2 m
```

</details>

**Krok 3. Znajdź przyczynę.** Wynik `piece_length_m` jest już typu `double`, więc zmiana typu wyniku nic tu nie da. Sprawdź operandy dzielenia: jakiego są typu i jakie dzielenie wykonują?

**Krok 4. Popraw program**, zmieniając typ tej wartości, która z natury może mieć część ułamkową. Liczba kawałków ma zostać liczbą całkowitą.

**Krok 5. Sprawdź wynik.** Po poprawce program ma wypisać:

<!-- output: ribbon_fixed -->
```text
Piece length: 2.5 m
```

<details>
<summary>Wyjaśnienie i poprawiony program: przeczytaj po własnej próbie</summary>

Oba operandy, `ribbon_length_m` i `pieces`, są typu `int`, więc `ribbon_length_m / pieces` to dzielenie całkowite: 10 / 4 daje 2. Typ `double` zmiennej `piece_length_m` nie zmienia obliczenia, które już się wykonało (punkt 4).

Długość wstążki to pomiar, który mógłby wynosić na przykład 10.5 m, więc pasuje do niej typ `double`. Liczba kawałków jest całkowita i zostaje `int`:

<!-- example: ribbon_fixed -->
```cpp
#include <iostream>

int main() {
    const double ribbon_length_m{10.0};
    const int pieces{4};

    const double piece_length_m{ribbon_length_m / pieces};

    std::cout << "Piece length: " << piece_length_m << " m\n";
}
```

Teraz jeden operand jest typu `double`, więc to dzielenie zmiennoprzecinkowe: 10.0 / 4 daje 2.5.

</details>

## 11. Dobierz typ

Dla każdej wielkości wybierz `int` albo `double` i krótko uzasadnij wybór. Zastanów się: czy ta wielkość może mieć część ułamkową?

| Wielkość | Typ | Dlaczego |
|---|---|---|
| liczba uczniów w klasie | | |
| wzrost w metrach, na przykład 1.62 | | |
| liczba stron w książce | | |
| czas biegu zmierzony stoperem, na przykład 12.4 s | | |
| średnia z kilku ocen | | |
| liczba okrążeń bieżni | | |

Przykładowe odpowiedzi są w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 12. Misja: średni czas okrążenia

Na treningu biegowym 5 okrążeń bieżni zajęło łącznie 37.5 sekundy, według stopera. Program ma obliczyć średni czas jednego okrążenia.

W `cpp-workspace` utwórz katalog `lap_times`, skopiuj do niego `CMakeLists.txt` z oryginalnego `lesson_05_first_program`, utwórz pusty `main.cpp` i napisz program samodzielnie. Program ma wypisać dokładnie:

<!-- output: lap_times -->
```text
Laps: 5
Total time: 37.5 s
Average lap time: 7.5 s
```

### Kryterium sukcesu

- Program buduje się jako C++20 i wypisuje dokładnie powyższy wynik.
- Liczba okrążeń, łączny czas i średni czas mają własne stałe z sensownymi nazwami po angielsku.
- Każda stała ma typ dobrany do znaczenia: umiesz uzasadnić, dlaczego liczba okrążeń jest `int`, a czasy `double`. Jeśli przy którejś użyjesz `auto`, umiesz powiedzieć, jaki typ ustali kompilator.
- Średnią **oblicza program**: liczba 7.5 nie występuje w kodzie. Liczby 5 i 37.5 występują w kodzie tylko raz, w deklaracjach.
- Program używa tylko tego, co już znasz: `int`, `double`, `auto`, `const`, `{}`, działań arytmetycznych i `std::cout`.
- Umiesz wyjaśnić, dlaczego wynik ma część ułamkową, choć liczba okrążeń jest całkowita.

Gdy wynik się zgadza, możesz zapisać projekt w Gicie, jak w lekcji 1.5.

<details>
<summary>Podpowiedź 1</summary>

Która z tych wielkości może mieć część ułamkową, a która zawsze jest całkowita? Od tego zależy typ każdej stałej.

</details>

<details>
<summary>Podpowiedź 2</summary>

Średnia to łączny czas podzielony przez liczbę okrążeń. Sprawdź, jakiego typu są operandy tego dzielenia i czy wykona się dzielenie całkowite.

</details>

### Wariant: wolniejszy trening

Na następnym treningu 5 okrążeń zajęło 42.5 sekundy. **Przewidź** nową średnią, a potem zmień w programie **tylko jedną wartość początkową**. Wynik ma być taki:

<!-- output: lap_times_variant -->
```text
Laps: 5
Total time: 42.5 s
Average lap time: 8.5 s
```

Przykładowe rozwiązania są w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 13. Gdy coś pójdzie inaczej

| Co widzisz | Co to znaczy | Co zrobić |
|---|---|---|
| Wynik dzielenia nie ma części ułamkowej, choć powinien | Oba operandy są całkowite, więc wykonało się dzielenie całkowite. Typ zmiennej wynikowej tego nie zmienia. | Sprawdź operandy. Wartość, która z natury ma część ułamkową, powinna być typu `double`. |
| `std::cout` wypisuje `3`, a zmienna jest typu `double` | Wartość to 3.0. `std::cout` nie wypisuje `.0`. | Nic. Typ odczytuj z kodu, nie z ekranu. |
| Błąd ze słowami `cannot be narrowed` przy `{}` | Wartość w `{}` nie zmieściłaby się bez zmiany w typie zmiennej, na przykład 2.5 w `int`. | Sprawdź, czy zmienna ma właściwy typ. Wartość z częścią ułamkową wymaga `double`. |
| W kodzie `7,5` zamiast `7.5` | W C++ część ułamkową oddziela się kropką. Przecinek oznacza w kodzie coś innego. | Napisz `7.5`. |
| Błąd przy `%` z liczbą `double` | `%` działa tylko dla liczb całkowitych. | W tej lekcji nie używaj `%` z `double`. |
| Zmienna z `auto` ma inny typ, niż zakładano | Kompilator ustalił typ z wartości początkowej, na przykład `auto x{7 / 2};` daje `int`. | Sprawdź typ wartości początkowej. W razie wątpliwości napisz typ jawnie. |

## 14. Wyjaśnij

Odpowiedz własnymi słowami, najlepiej na piśmie. Dopiero potem porównaj z przykładową odpowiedzią.

**1.** Dlaczego `7 / 2` daje `3`, a `7.0 / 2` daje `3.5`?

<details>
<summary>Przykładowa odpowiedź</summary>

W `7 / 2` oba operandy są typu `int`, więc wykonuje się dzielenie całkowite. W `7.0 / 2` pierwszy operand jest typu `double`, więc drugi zostaje przekształcony w `double` i wykonuje się dzielenie zmiennoprzecinkowe, którego wynik ma część ułamkową.

</details>

**2.** Dlaczego `const double first{7 / 2};` przechowuje 3, choć jest typu `double`?

<details>
<summary>Przykładowa odpowiedź</summary>

Bo najpierw obliczane jest `7 / 2`, a to dzielenie całkowite, które daje 3. Dopiero ta wartość trafia do zmiennej. Typ zmiennej nie zmienia rodzaju dzielenia.

</details>

**3.** Czy z tego, że program wypisał `3`, wynika, że wartość jest typu `int`?

<details>
<summary>Przykładowa odpowiedź</summary>

Nie. Wartość `double` równa 3.0 też wypisuje się jako `3`. Typ trzeba odczytać z kodu.

</details>

**4.** Jakiego typu jest `x` w `auto x{7.0 / 2};` i skąd to wiadomo? Czy później może stać się typu `int`?

<details>
<summary>Przykładowa odpowiedź</summary>

`double`, bo wartość początkowa `7.0 / 2` jest typu `double`. Kompilator ustala typ raz, przy deklaracji. Później się on nie zmienia.

</details>

**5.** Dlaczego w misji liczba okrążeń jest typu `int`, a nie `double`?

<details>
<summary>Przykładowa odpowiedź</summary>

Bo okrążeń jest zawsze całkowita liczba. Część ułamkową mają czasy. Wystarczy, że łączny czas jest typu `double`, żeby dzielenie przez liczbę okrążeń było zmiennoprzecinkowe.

</details>

## Podsumowanie

- `double` przechowuje liczby z częścią ułamkową. Literał `double` ma kropkę: `7.5`, `7.0`.
- Rodzaj dzielenia zależy od **operandów**: dwa `int` dają dzielenie całkowite, a gdy jeden operand jest typu `double`, wykonuje się dzielenie zmiennoprzecinkowe.
- Typ zmiennej wynikowej **nie zmienia** obliczenia, które już się wykonało: `const double first{7 / 2};` przechowuje 3.
- W prostych działaniach `int` z `double` obliczenie wykonuje się na `double`. W dłuższym wyrażeniu dotyczy to każdego działania osobno.
- `double` przechowuje wartości **przybliżone**: nie każda liczba dziesiętna da się zapisać dokładnie. Wypisana liczba nie zawsze zdradza typ ani dokładną wartość.
- Inicjalizacja przez `{}` nie pozwala zapisać po cichu wartości, która by się zmieniła, na przykład 2.5 w `int`.
- `auto` ustala jeden konkretny typ z wartości początkowej, przy deklaracji. Ten typ się potem nie zmienia, a `auto` niczego nie oblicza za Ciebie.
- Jawny typ jest dobry przy danych, `auto` tam, gdzie typ jasno wynika z wartości początkowej.

## Co dalej

Twoje programy liczą już na liczbach całkowitych i ułamkowych, ale wszystkie dane są wpisane w kodzie. W lekcji 2.6 program zacznie pobierać liczby od użytkownika: [Lekcja 2.6: Program, który pyta użytkownika](lesson_06_a_program_that_asks_the_user.md).

---

## Przykładowe rozwiązania

Zajrzyj tutaj **po własnej próbie**. Twoje nazwy mogą się różnić, jeśli wynik jest taki, jak wymagany.

<details>
<summary>Punkt 5: siedem wyrażeń</summary>

| | Wyrażenie | Grupowanie | Czy jest dzielenie całkowite? | Wynik | Wyjaśnienie |
|---|---|---|---|---|---|
| a | `7 / 2` | — | tak | 3 | Dwa `int`. |
| b | `7 / 2.0` | — | nie | 3.5 | Jeden operand `double`. Nie ma znaczenia, czy jest po lewej, czy po prawej. |
| c | `1.5 + 2` | — | nie | 3.5 | `double` plus `int` daje `double`. |
| d | `2.5 * 2` | — | nie | 5 | Wynik jest typu `double` i wynosi 5.0, ale wypisuje się jako `5`. |
| e | `10 - 0.25` | — | nie | 9.75 | `int` minus `double` daje `double`. |
| f | `1 / 2 * 4.0` | `(1 / 2) * 4.0` | tak | 0 | Najpierw `1 / 2`: dwa `int`, wynik 0. Dopiero potem mnożenie przez `4.0`, czyli 0 · 4.0 = 0. `4.0` nie naprawia dzielenia, które już się wykonało. |
| g | `1.0 / 2 * 4` | `(1.0 / 2) * 4` | nie | 2 | `1.0 / 2` daje 0.5, a 0.5 · 4 daje 2.0, wypisane jako `2`. |

</details>

<details>
<summary>Punkt 11: dobierz typ</summary>

| Wielkość | Typ | Dlaczego |
|---|---|---|
| liczba uczniów w klasie | `int` | Uczniów liczy się w całości. |
| wzrost w metrach | `double` | Pomiar z częścią ułamkową. |
| liczba stron w książce | `int` | Strony liczy się w całości. |
| czas biegu zmierzony stoperem | `double` | Pomiar z częścią ułamkową. |
| średnia z kilku ocen | `double` | Średnia zwykle ma część ułamkową, nawet gdy oceny są całkowite. |
| liczba okrążeń bieżni | `int` | Okrążenia liczy się w całości. |

Przy średniej z ocen całkowitych pamiętaj o punkcie 4: sama zmienna `double` na wynik nie wystarczy. Jeden operand dzielenia też musi być typu `double`.

</details>

<details>
<summary>Punkt 12: misja, średni czas okrążenia</summary>

<!-- example: lap_times -->
```cpp
#include <iostream>

int main() {
    const int laps{5};
    const double total_time_s{37.5};

    const double average_lap_time_s{total_time_s / laps};

    std::cout << "Laps: " << laps << "\n";
    std::cout << "Total time: " << total_time_s << " s\n";
    std::cout << "Average lap time: " << average_lap_time_s << " s\n";
}
```

- `laps` jest typu `int`, bo okrążeń jest całkowita liczba. `total_time_s` jest typu `double`, bo to pomiar czasu.
- `total_time_s / laps` to `double` podzielone przez `int`, więc wykonuje się dzielenie zmiennoprzecinkowe: 37.5 / 5 daje 7.5.
- Zamiast `const double average_lap_time_s` można napisać `const auto average_lap_time_s`. Kompilator ustali typ `double`, bo taki jest wynik dzielenia.

</details>

<details>
<summary>Punkt 12: wariant</summary>

<!-- example: lap_times_variant -->
```cpp
#include <iostream>

int main() {
    const int laps{5};
    const double total_time_s{42.5};

    const double average_lap_time_s{total_time_s / laps};

    std::cout << "Laps: " << laps << "\n";
    std::cout << "Total time: " << total_time_s << " s\n";
    std::cout << "Average lap time: " << average_lap_time_s << " s\n";
}
```

Zmieniła się tylko wartość początkowa `total_time_s`. Obliczenie zostało takie samo: 42.5 / 5 daje 8.5.

</details>

**Poprzednia lekcja:** [Lekcja 2.4: Dzielenie, reszta i kolejność działań](lesson_04_division_remainder_and_order_of_operations.md) · **Następna lekcja:** [Lekcja 2.6: Program, który pyta użytkownika](lesson_06_a_program_that_asks_the_user.md) · [Opis kursu](../../README.md)

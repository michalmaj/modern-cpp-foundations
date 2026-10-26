# Lekcja 7.2: Pozycje i sąsiednie znaki w `std::string`

**Polski** · [English](lesson_02_positions_and_neighbours.en.md) · [Opis kursu](../../README.md)

> **Moduł 7, lekcja 2** · około 60–75 minut
> **Potrzebujesz:** katalogu `cpp-workspace` i oryginalnego projektu `lesson_05_first_program`, jak dotąd. Debugger nie jest w tej lekcji potrzebny.
> **Wersja pilotażowa.** Programy z tej lekcji sprawdzamy automatycznie na Windowsie, Ubuntu i macOS, także z podanymi danymi wejściowymi. Wpisywanie danych w oknie **Run** CLiona opisujemy bez ręcznego sprawdzenia na każdym systemie.

## Zanim zaczniesz

Ta lekcja zakłada, że:

- przeglądasz tekst znak po znaku pętlą zakresową i porównujesz znaki z literałami znakowymi (lekcja 7.1);
- odczytujesz elementy wektora przez indeks, używasz `std::size_t` z `<cstddef>` i porównujesz sąsiednie elementy pętlą od indeksu 1 (lekcja 6.3).

## Sytuacja

Pętla zakresowa z lekcji 7.1 odczytuje wszystkie znaki tekstu `"Book"`. Spróbuj jednak odpowiedzieć tylko z jej pomocą:

- Jaki znak stoi na drugiej pozycji?
- Czy dwa środkowe znaki są takie same?
- Na której pozycji powtarza się znak?
- Jak porównać każdy znak z poprzednim?

Do takich pytań potrzebna jest **pozycja** znaku, a nie tylko jego wartość. Tekst ma pozycje tak jak wektor w lekcji 6.3, więc wykorzystasz tu indeksy. Gdy pozycja nie jest potrzebna, pętla zakresowa nadal jest naturalnym wyborem.

Po tej lekcji będziesz:

- odczytywać znak o wybranym indeksie przez `text[index]`, z indeksami od 0, i zamieniać indeks na pozycję widoczną dla człowieka;
- odczytywać pierwszy i ostatni znak niepustego tekstu;
- przechodzić po tekście pętlą indeksową z `std::size_t`;
- bezpiecznie porównywać sąsiednie znaki, także w tekście pustym i jednoznakowym;
- liczyć wszystkie pary identycznych sąsiednich znaków, także pary nakładające się.

## 1. Przygotuj projekt

W `cpp-workspace` utwórz katalog `lesson_7_2` i skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program`. Programy z punktów 2–5 wpisujesz w `main.cpp` tego katalogu.

## 2. Znak o wybranej pozycji

<!-- example: book_by_index -->
```cpp
#include <iostream>
#include <string>

int main() {
    const std::string text{"Book"};

    std::cout << text[0] << "\n";
    std::cout << text[1] << "\n";
    std::cout << text[2] << "\n";
    std::cout << text[3] << "\n";
}
```

<!-- output: book_by_index -->
```text
B
o
o
k
```

| Pozycja dla człowieka | Indeks w C++ | Znak |
|---|---|---|
| 1 | 0 | `B` |
| 2 | 1 | `o` |
| 3 | 2 | `o` |
| 4 | 3 | `k` |

Zapis jest taki sam jak dla wektora w lekcji 6.3: `text[1]` czytaj „znak tekstu `text` o indeksie 1”. Wynik to jeden znak typu `char`. **Indeksy zaczynają się od 0**, więc `text.size()` daje 4, a czwarta pozycja ma indeks 3.

**Jeden szczegół różni tekst od wektora.** Dla `std::string` odczyt `text[text.size()]` jest dozwolony i daje specjalny znak zerowy, który **nie należy do treści tekstu**. Dla indeksu większego niż `size()` zachowanie jest niezdefiniowane, jak dla wektora. Nie musisz pamiętać tego szczegółu. Wystarczy reguła: **znak należący do tekstu ma indeks spełniający `index < text.size()`.**

## 3. Pierwszy i ostatni znak

<!-- example: first_and_last_char -->
```cpp
#include <iostream>
#include <string>

int main() {
    const std::string text{"Book"};

    if (!text.empty()) {
        std::cout << text[0] << "\n";
        std::cout << text[text.size() - 1] << "\n";
    }
}
```

**Przewidź** obie linijki i uruchom program.

<details>
<summary>Standardowe wyjście</summary>

<!-- output: first_and_last_char -->
```text
B
k
```

</details>

- Pierwszy znak ma indeks 0, a ostatni `size() - 1`, jak w lekcji 6.3.
- **Najpierw `empty()`.** Pusty tekst nie ma pierwszego ani ostatniego znaku. A `size() - 1` dla pustego tekstu nie daje −1, bo wynik `size()` jest liczbą bez znaku. Dlatego nie wyznaczamy ostatniej pozycji, zanim sprawdzimy, że tekst nie jest pusty.

## 4. Pętla po pozycjach

<!-- example: char_positions -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>

int main() {
    const std::string text{"Cat"};

    for (std::size_t index{0}; index < text.size(); ++index) {
        std::cout << "Position " << index + 1 << ": " << text[index] << "\n";
    }
}
```

**Przewidź** wszystkie linijki i uruchom program.

<details>
<summary>Standardowe wyjście</summary>

<!-- output: char_positions -->
```text
Position 1: C
Position 2: a
Position 3: t
```

</details>

To pętla z lekcji 6.3, tylko po tekście: indeks typu `std::size_t` zaczyna od 0, warunek `index < text.size()` dopuszcza tylko znaki należące do tekstu, `text[index]` odczytuje bieżący znak, a pętla kończy się, zanim indeks osiągnie `size()`. Indeks przechowujemy w `std::size_t` z tego samego powodu co w 6.3: tak jak wynik `size()`. Zapisanie `size()` w `int` z `{}` kompilator odrzuci jako konwersję zawężającą.

**Pozycja dla człowieka to `index + 1`.** Indeksowanie tekstu zawsze zaczyna się od 0. Numer od 1 to tylko sposób pokazania wyniku.

## 5. Sąsiednie znaki

Dla bieżącego indeksu `index` poprzedni znak ma indeks `index - 1`:

<!-- example: neighbour_pairs -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>

int main() {
    const std::string text{"Book"};

    for (std::size_t index{1}; index < text.size(); ++index) {
        const char previous{text[index - 1]};
        const char current{text[index]};

        std::cout << previous << current << "\n";
    }
}
```

**Przewidź**, ile linijek wypisze program i jakie.

<details>
<summary>Standardowe wyjście</summary>

<!-- output: neighbour_pairs -->
```text
Bo
oo
ok
```

</details>

| Bieżący indeks | Poprzedni znak | Bieżący znak | Takie same? |
|---|---|---|---|
| 1 | `B` | `o` | nie |
| 2 | `o` | `o` | tak |
| 3 | `o` | `k` | nie |

**Odpowiedz, zanim otworzysz odpowiedzi:**

1. Ile par sąsiednich znaków ma tekst czteroznakowy?
2. Dlaczego pętla zaczyna się od indeksu 1?
3. Co się stanie dla tekstu jednoznakowego, a co dla pustego?
4. Które pozycje dla człowieka tworzy para przy indeksie 2?
5. Czy porównanie `text[index - 1]` z `text[index]` jest bezpieczne dla indeksu 1? A dla ostatniego indeksu w pętli?

<details>
<summary>Odpowiedzi</summary>

1. Trzy. Każdy znak oprócz pierwszego tworzy parę z poprzednim.
2. Bo znak o indeksie 0 nie ma poprzednika. Od indeksu 1 poprzedni znak, `index - 1`, zawsze istnieje.
3. Dla jednego znaku `1 < 1` daje `false`, a dla pustego tekstu `1 < 0` daje `false`, więc pętla nie wykonuje żadnego przebiegu. Nie ma pary, więc nie ma czego porównywać. Ta pętla nie potrzebuje osobnego sprawdzenia `empty()`.
4. Indeksy 1 i 2, czyli pozycje 2 i 3: `index` i `index + 1`.
5. Tak. Dla indeksu 1 porównujemy indeksy 0 i 1. Ostatni przebieg ma `index` równy `size() - 1`, więc oba znaki należą do tekstu. Potem warunek `index < text.size()` daje `false` i pętla się kończy.

</details>

**Porównujemy dokładne wartości `char`.** `'A'` i `'A'` są takie same, ale `'A'` i `'a'` już nie: to różne znaki. Dwie sąsiednie spacje są takie same, tak samo dwie kropki albo dwie cyfry `'1'`. Nie ignorujemy wielkości liter i niczego z tekstu nie usuwamy.

## 6. Misja: mapa powtórzonych znaków

Program szuka w krótkim tekście ASCII wszystkich par sąsiednich, identycznych znaków i podaje ich pozycje. Tekst jest wpisany w kodzie:

<!-- fragment -->
```cpp
const std::string text{"coffee 111"};
```

**Wymagania:**

- Pierwsza linijka: `Characters: N`, czyli liczba elementów tekstu.
- Dla każdej pary sąsiednich, identycznych znaków, w kolejności od początku tekstu, program wypisuje `Pair X-Y: [C]`: `X` i `Y` to pozycje obu znaków, liczone od 1, a `C` to powtórzony znak, w nawiasach kwadratowych, żeby było widać także parę spacji.
- Ostatnia linijka: `Repeated pairs: N`, czyli liczba takich par.
- **Pary mogą się nakładać.** W `"AAA"` są dwie pary: pozycje 1–2 i 2–3. W `"AAAA"` są trzy: 1–2, 2–3 i 3–4. Znak, który należy do jednej pary, może należeć też do następnej.
- Porównujemy znaki dokładnie: `'A'` i `'a'` nie tworzą pary, a dwie spacje tworzą.
- Gdy żadnej pary nie ma, program wypisuje tylko `Characters: N` i `Repeated pairs: 0`, bez dodatkowego komunikatu.
- Program działa po zmianie samego tekstu w nawiasach klamrowych, także dla pustego i jednoznakowego tekstu, i nie odczytuje znaków spoza tekstu. Nie odczytuje niczego z wejścia i nie zmienia tekstu.

W `cpp-workspace` utwórz katalog `repeated_pairs`, skopiuj do niego `CMakeLists.txt` z oryginalnego `lesson_05_first_program`, utwórz pusty `main.cpp` i napisz program samodzielnie.

Dla tekstu powyżej standardowe wyjście ma być takie:

<!-- output: repeated_pairs -->
```text
Characters: 10
Pair 3-4: [f]
Pair 5-6: [e]
Pair 8-9: [1]
Pair 9-10: [1]
Repeated pairs: 4
```

W `coffee` powtarzają się `f` i `e`. Końcowe `111` daje dwie nakładające się pary. Spacja jest elementem tekstu, ale tutaj nie tworzy pary.

**To nie jest program z punktu 5 z innym tekstem.** Tam program tylko wypisywał pary. Musisz samodzielnie zdecydować:

1. jak rozpoznać parę identycznych znaków;
2. gdzie stoi licznik i kiedy rośnie;
3. jak z bieżącego indeksu wyznaczyć numery obu pozycji;
4. jak wypisać powtórzony znak;
5. jak sprawić, żeby nakładające się pary nie zginęły;
6. co program wypisze, gdy par nie ma, także dla pustego i jednoznakowego tekstu.

**Zanim napiszesz program**, przygotuj tabelę przypadków: pusty tekst, jeden znak, dwa różne znaki, dwa, trzy i cztery jednakowe znaki, dwie rozłączne pary, wielkie i małe litery obok siebie, dwie spacje, powtórzona kropka i powtórzona cyfra. Przy każdym zapisz oczekiwane linijki `Pair` i licznik.

**Potem:** uruchom program dla tekstu z wymagań, a następnie zmień tekst na 3–4 przypadki z tabeli, na przykład `"AAA"`, `"AABB"`, `"aAa"` i pusty tekst. Wszystkie przypadki z pełnej listy kontrolnej są sprawdzone automatycznie, więc nie musisz wpisywać ich wszystkich.

### Kryterium sukcesu

- Program buduje się jako C++20, a dla tekstu z wymagań wypisuje dokładnie sześć linijek pokazanych wyżej.
- Pary nakładające się są liczone: `"AAA"` daje dwie pary, a `"AAAA"` trzy.
- Pozycje w linijkach `Pair` są liczone od 1, a pary są wypisane w kolejności od początku tekstu.
- Wielkość liter ma znaczenie, a spacje i interpunkcja mogą tworzyć pary.
- Pusty i jednoznakowy tekst dają `Repeated pairs: 0`, a program nie odczytuje znaku spoza tekstu.
- Indeksy są typu `std::size_t`.
- Tabela przypadków powstała przed uruchomieniem programu.
- Umiesz wyjaśnić, dlaczego `"AAA"` daje dwie pary.

Gdy wynik się zgadza, możesz zapisać projekt w Gicie, jak w lekcji 1.5.

<details>
<summary>Podpowiedź 1</summary>

Jak sprawdzić, czy bieżący znak jest taki sam jak bezpośrednio poprzedni?

</details>

<details>
<summary>Podpowiedź 2</summary>

Pomyśl, od którego indeksu da się bezpiecznie porównywać sąsiadów i jak przeliczyć ich indeksy na numery pozycji od 1.

</details>

<details>
<summary>Podpowiedź 3</summary>

Zwiększaj licznik dla każdej identycznej pary. Nie pomijaj kolejnego porównania, ponieważ jeden znak może należeć do dwóch sąsiadujących par.

</details>

<details>
<summary>Pełna lista przypadków kontrolnych: otwórz po przygotowaniu własnej tabeli</summary>

| | Tekst | Linijki `Pair` | Licznik | Co sprawdza |
|---|---|---|---|---|
| A | `coffee 111` | 3-4 `[f]`, 5-6 `[e]`, 8-9 `[1]`, 9-10 `[1]` | 4 | dane z wymagań |
| B | pusty tekst | — | 0 | pusty tekst |
| C | `A` | — | 0 | jeden znak |
| D | `AB` | — | 0 | dwa różne znaki |
| E | `AA` | 1-2 `[A]` | 1 | najkrótsza para |
| F | `AAA` | 1-2 `[A]`, 2-3 `[A]` | 2 | dwie nakładające się pary |
| G | `AAAA` | 1-2, 2-3, 3-4, każda `[A]` | 3 | trzy nakładające się pary |
| H | `AABB` | 1-2 `[A]`, 3-4 `[B]` | 2 | dwie rozłączne pary |
| I | `aAa` | — | 0 | wielkość liter ma znaczenie |
| J | `aAAa` | 2-3 `[A]` | 1 | para wielkich liter w środku |
| K | dwie spacje | 1-2 `[ ]` | 1 | para spacji |
| L | `...` | 1-2 `[.]`, 2-3 `[.]` | 2 | powtórzona interpunkcja |
| M | `bookkeeper` | 2-3 `[o]`, 4-5 `[k]`, 6-7 `[e]` | 3 | trzy różne powtórzenia |
| N | `1233` | 3-4 `[3]` | 1 | powtórzona cyfra na końcu |

**Testy automatyczne i Twoje próby.** Wszystkie przypadki są sprawdzone automatycznie przez program kontrolny. Ma on ten sam raport co rozwiązanie referencyjne, ale tekst odczytuje z wejścia jako jedną linijkę, przez `std::getline` z lekcji 2.7. Pusty tekst to w nim pusta linijka, a nie brak danych. To tylko narzędzie do sprawdzania, a nie część misji. Program kontrolny i jego wyniki są w części [Przykładowe rozwiązania](#przykładowe-rozwiązania), bo zawierają rozwiązanie.

</details>

Przykładowe rozwiązanie jest w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 7. Znajdź błąd: zgubione nakładające się pary

To zadanie wykonaj **po misji**: program poniżej zawiera prawie cały algorytm misji. Odczytuje tekst z wejścia jako jedną linijkę, tak jak program kontrolny, i nie wypisuje pytania: po uruchomieniu wpisz tekst i naciśnij **Enter**. Wymaganie: pary nakładające się też się liczą.

<details>
<summary>Program do sprawdzenia: otwórz po napisaniu własnego programu</summary>

<!-- example: pairs_skip_bug -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>

int main() {
    std::string text{};
    std::getline(std::cin, text);

    if (std::cin.fail()) {
        std::cout << "Input could not be read\n";
    } else {
        int repeated_pairs{0};

        std::cout << "Characters: " << text.size() << "\n";

        for (std::size_t index{1}; index < text.size(); ++index) {
            if (text[index] == text[index - 1]) {
                std::cout << "Pair " << index << "-" << index + 1 << ": [" << text[index] << "]\n";
                ++repeated_pairs;
                ++index;
            }
        }

        std::cout << "Repeated pairs: " << repeated_pairs << "\n";
    }
}
```

1. **Przewidź** raport dla `AABB`, `AAA` i `AAAA`.
2. Uruchom program dla `AABB`. Czy raport jest poprawny?
3. Uruchom go dla `AAA`. Prześledź wartości `index` w tabeli: które porównanie się nie wykonało?
4. Uruchom go dla `AAAA`.
5. Wskaż instrukcję, która pomija porównanie.
6. Popraw program.
7. Sprawdź ponownie wszystkie trzy teksty.

</details>

Wyniki programu przed poprawką i poprawiony program są w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 8. Gdy coś pójdzie inaczej

| Co widzisz | Co to znaczy | Co zrobić |
|---|---|---|
| `comparison of integers of different signs` | Indeks typu `int` jest porównywany z `size()`. | Zadeklaruj indeks jako `std::size_t` (lekcja 6.3). |
| Pozycje w raporcie są o jeden za małe, na przykład `Pair 2-3` zamiast `Pair 3-4` | Program wypisuje indeksy zamiast pozycji. | Para przy indeksie `index` to pozycje `index` i `index + 1`. |
| `"AAA"` daje jedną parę zamiast dwóch | Program pomija porównanie po znalezieniu pary (punkt 7). | Każdy indeks od 1 do końca musi zostać porównany. |
| Para `'A'` i `'a'` jest liczona | Program porównuje znaki bez rozróżniania wielkości liter, na przykład przez zakresy liter. | Porównuj dokładnie: `text[index] == text[index - 1]`. |
| Dziwne znaki albo nieoczekiwane zakończenie programu | Prawdopodobnie odczyt spoza tekstu: indeks większy niż `size()` albo `index - 1` dla indeksu 0. | Pętla po sąsiadach zaczyna od indeksu 1 i ma warunek `index < text.size()`. |
| Linijka `Pair` dla spacji wygląda na pustą | Spacja jest niewidoczna bez nawiasów. | Wypisuj znak w nawiasach kwadratowych, jak w wymaganiach. |

## 9. Wyjaśnij

Odpowiedz własnymi słowami, najlepiej na piśmie. Dopiero potem porównaj z przykładowymi odpowiedziami.

1. Dlaczego pierwszy znak ma indeks 0 i jak z indeksu wyznaczyć pozycję dla człowieka?
2. Co oznacza `text[index]` i jakiego typu jest wynik?
3. Jaki warunek musi spełniać indeks znaku należącego do tekstu?
4. Dlaczego przed odczytem ostatniego znaku sprawdzamy `empty()`?
5. Po co indeks typu `std::size_t`?
6. Kiedy wybrać pętlę zakresową, a kiedy indeksową?
7. Dlaczego porównywanie sąsiadów zaczyna się od indeksu 1 i ile par ma tekst trzyznakowy?
8. Dlaczego `"AAA"` daje dwie identyczne pary?
9. Czy `'A'` i `'a'` tworzą parę? A dwie sąsiednie spacje?
10. Dlaczego ten program nie zawsze poprawnie analizuje tekst z polskimi literami?

<details>
<summary>Przykładowe odpowiedzi</summary>

1. Bo w C++ indeks to odległość od początku tekstu: pierwszy znak jest 0 pozycji od początku. Pozycja dla człowieka to `index + 1`.
2. Znak tekstu o podanym indeksie. Wynik jest typu `char`.
3. `index < text.size()`. Dla `std::string` odczyt `text[text.size()]` jest dozwolony, ale daje specjalny znak zerowy, który nie należy do treści tekstu.
4. Bo pusty tekst nie ma ostatniego znaku, a `size() - 1` dla rozmiaru 0 nie daje −1, tylko ogromną liczbę, bo wynik `size()` nie ma znaku.
5. Bo taki jest typ wyniku `size()`. Nie mieszamy go z `int`: porównanie `int` z `size()` przy flagach kursu zatrzymuje budowanie, a zapis `size()` w `int` z `{}` to konwersja zawężająca (lekcja 6.3).
6. Pętlę zakresową, gdy potrzebujesz tylko kolejnych znaków, jak w lekcji 7.1. Indeksową, gdy potrzebujesz pozycji albo sąsiada.
7. Bo znak o indeksie 0 nie ma poprzednika. Tekst trzyznakowy ma dwie pary: indeksy 0–1 i 1–2.
8. Bo środkowe `A` należy do dwóch par: z pierwszym i z ostatnim znakiem. Każde porównanie sąsiadów liczy się osobno.
9. `'A'` i `'a'` nie: to różne znaki. Dwie spacje tak: to dwa takie same znaki.
10. Bo w UTF-8 polska litera zajmuje kilka elementów `char`. Pozycje i porównania dotyczą elementów `char`, a nie liter widocznych dla człowieka. Dlatego dane w tej lekcji są w ASCII.

</details>

## Podsumowanie

- `text[index]` odczytuje znak tekstu o podanym indeksie. Indeksy zaczynają się od 0, a pozycja dla człowieka to `index + 1`.
- Znak należący do tekstu ma indeks spełniający `index < text.size()`.
- Pierwszy znak to `text[0]`, ostatni `text[text.size() - 1]`, oba tylko dla niepustego tekstu.
- Pętla po pozycjach: `for (std::size_t index{0}; index < text.size(); ++index)`, z `std::size_t` z `<cstddef>`.
- Pary sąsiadów przeglądasz od indeksu 1: `text[index - 1]` i `text[index]`. Ta pętla jest bezpieczna dla tekstu pustego i jednoznakowego.
- Znaki porównujesz dokładnie przez `==`: wielkość liter ma znaczenie, a spacja to zwykły znak.
- Pary mogą się nakładać: jeden znak może należeć do dwóch sąsiednich par.
- Pozycje dotyczą elementów `char`, więc analiza jest poprawna dla tekstu ASCII.

## Co dalej

W tej lekcji tekst był tylko odczytywany. W kolejnej lekcji funkcja dostanie tekst przez `const std::string&` i zbuduje z niego nowy tekst. Lekcja jest w przygotowaniu.

---

## Przykładowe rozwiązania

Zajrzyj tutaj **po własnej próbie**. Twoje nazwy mogą się różnić, jeśli standardowe wyjście jest takie, jak wymagane.

<details>
<summary>Punkt 6: misja, mapa powtórzonych znaków</summary>

<!-- example: repeated_pairs -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>

int main() {
    const std::string text{"coffee 111"};

    int repeated_pairs{0};

    std::cout << "Characters: " << text.size() << "\n";

    for (std::size_t index{1}; index < text.size(); ++index) {
        if (text[index] == text[index - 1]) {
            std::cout << "Pair " << index << "-" << index + 1 << ": [" << text[index] << "]\n";
            ++repeated_pairs;
        }
    }

    std::cout << "Repeated pairs: " << repeated_pairs << "\n";
}
```

1. **Pętla indeksowa**, bo potrzebujemy pozycji i poprzedniego znaku, czego pętla zakresowa nie daje.
2. **Start od indeksu 1**, bo każda para to znak z poprzednim, a pierwszy znak poprzednika nie ma. Dla tekstu pustego i jednoznakowego pętla nie wykonuje żadnego przebiegu.
3. **`std::size_t`**, bo tak jak w lekcji 6.3 indeks porównujemy z wynikiem `size()`.
4. **Poprzedni znak** to `text[index - 1]`. Dla każdego indeksu od 1 wzwyż ten indeks należy do tekstu.
5. **Porównanie znaków** `==` sprawdza, czy to dokładnie ten sam znak: `'A'` i `'a'` są różne.
6. **Pozycje:** para to indeksy `index - 1` i `index`, czyli pozycje `index` i `index + 1`.
7. **`"AAA"` daje dwie pary**, bo pętla porównuje indeksy 0–1, a potem 1–2. Oba porównania wychodzą „takie same”.
8. **Nie pomijamy indeksów:** po znalezieniu pary pętla przechodzi tylko do następnego indeksu, przez `++index` w nagłówku. Dzięki temu znak z poprzedniej pary bierze udział w następnym porównaniu.
9. **Spacje i interpunkcja** to zwykłe znaki, więc `==` traktuje je jak litery. Nawiasy w raporcie pokazują, że para składa się ze spacji.
10. **Ograniczenie ASCII:** pozycje i porównania dotyczą elementów `char`. Polska litera w UTF-8 to kilka takich elementów, więc pozycje nie odpowiadałyby literom widocznym dla człowieka.

Pary można też wykrywać inaczej, na przykład porównując znak z następnym w pętli o innym warunku, jeśli żadne porównanie nie sięga poza tekst i nakładające się pary są liczone.

**Program kontrolny** sprawdza wszystkie przypadki z listy kontrolnej. Raport i pętla są takie same jak wyżej, poza wcięciem. Tekst jest odczytywany z wejścia jako jedna linijka przez `std::getline`, więc nie ma `const`.

<!-- example: repeated_pairs_check -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>

int main() {
    std::string text{};
    std::getline(std::cin, text);

    if (std::cin.fail()) {
        std::cout << "Input could not be read\n";
    } else {
        int repeated_pairs{0};

        std::cout << "Characters: " << text.size() << "\n";

        for (std::size_t index{1}; index < text.size(); ++index) {
            if (text[index] == text[index - 1]) {
                std::cout << "Pair " << index << "-" << index + 1 << ": [" << text[index] << "]\n";
                ++repeated_pairs;
            }
        }

        std::cout << "Repeated pairs: " << repeated_pairs << "\n";
    }
}
```

Każdy przypadek to jedna linijka wejścia, w kolejności z listy kontrolnej, od A do N. Przypadek B to pusta linijka, a przypadek K to linijka z dwiema spacjami.

<!-- input: repeated_pairs_check -->
```text
coffee 111
```

<!-- output: repeated_pairs_check -->
```text
Characters: 10
Pair 3-4: [f]
Pair 5-6: [e]
Pair 8-9: [1]
Pair 9-10: [1]
Repeated pairs: 4
```

<!-- input: repeated_pairs_check -->
```text

```

<!-- output: repeated_pairs_check -->
```text
Characters: 0
Repeated pairs: 0
```

<!-- input: repeated_pairs_check -->
```text
A
```

<!-- output: repeated_pairs_check -->
```text
Characters: 1
Repeated pairs: 0
```

<!-- input: repeated_pairs_check -->
```text
AB
```

<!-- output: repeated_pairs_check -->
```text
Characters: 2
Repeated pairs: 0
```

<!-- input: repeated_pairs_check -->
```text
AA
```

<!-- output: repeated_pairs_check -->
```text
Characters: 2
Pair 1-2: [A]
Repeated pairs: 1
```

<!-- input: repeated_pairs_check -->
```text
AAA
```

<!-- output: repeated_pairs_check -->
```text
Characters: 3
Pair 1-2: [A]
Pair 2-3: [A]
Repeated pairs: 2
```

<!-- input: repeated_pairs_check -->
```text
AAAA
```

<!-- output: repeated_pairs_check -->
```text
Characters: 4
Pair 1-2: [A]
Pair 2-3: [A]
Pair 3-4: [A]
Repeated pairs: 3
```

<!-- input: repeated_pairs_check -->
```text
AABB
```

<!-- output: repeated_pairs_check -->
```text
Characters: 4
Pair 1-2: [A]
Pair 3-4: [B]
Repeated pairs: 2
```

<!-- input: repeated_pairs_check -->
```text
aAa
```

<!-- output: repeated_pairs_check -->
```text
Characters: 3
Repeated pairs: 0
```

<!-- input: repeated_pairs_check -->
```text
aAAa
```

<!-- output: repeated_pairs_check -->
```text
Characters: 4
Pair 2-3: [A]
Repeated pairs: 1
```

<!-- input: repeated_pairs_check -->
```text
  
```

<!-- output: repeated_pairs_check -->
```text
Characters: 2
Pair 1-2: [ ]
Repeated pairs: 1
```

<!-- input: repeated_pairs_check -->
```text
...
```

<!-- output: repeated_pairs_check -->
```text
Characters: 3
Pair 1-2: [.]
Pair 2-3: [.]
Repeated pairs: 2
```

<!-- input: repeated_pairs_check -->
```text
bookkeeper
```

<!-- output: repeated_pairs_check -->
```text
Characters: 10
Pair 2-3: [o]
Pair 4-5: [k]
Pair 6-7: [e]
Repeated pairs: 3
```

<!-- input: repeated_pairs_check -->
```text
1233
```

<!-- output: repeated_pairs_check -->
```text
Characters: 4
Pair 3-4: [3]
Repeated pairs: 1
```

</details>

<details>
<summary>Punkt 7: wyniki przed poprawką i poprawiony program</summary>

Przed poprawką, dla `AABB`:

<!-- input: pairs_skip_bug -->
```text
AABB
```

<!-- output: pairs_skip_bug -->
```text
Characters: 4
Pair 1-2: [A]
Pair 3-4: [B]
Repeated pairs: 2
```

Dla `AAA`:

<!-- input: pairs_skip_bug -->
```text
AAA
```

<!-- output: pairs_skip_bug -->
```text
Characters: 3
Pair 1-2: [A]
Repeated pairs: 1
```

Dla `AAAA`:

<!-- input: pairs_skip_bug -->
```text
AAAA
```

<!-- output: pairs_skip_bug -->
```text
Characters: 4
Pair 1-2: [A]
Pair 3-4: [A]
Repeated pairs: 2
```

| Przebieg | `index` przy porównaniu | Porównane pozycje | Para? | `index` po ciele i po `++index` z nagłówka |
|---|---|---|---|---|
| 1 | 1 | 1–2 | tak | 2, potem 3 |
| — | 3 | — | warunek `3 < 3` daje `false` | koniec |

- Dla `AABB` wynik jest poprawny: pary są rozłączne, więc pominięte porównanie, pozycje 2–3 (`A` i `B`), i tak nie byłoby parą.
- Dla `AAA` pominięte zostało porównanie pozycji 2–3, które **jest** parą: wynik 1 zamiast 2. Dla `AAAA` program znajduje pary 1–2 i 3–4, ale gubi 2–3: wynik 2 zamiast 3.
- **Przyczyna:** dodatkowe `++index;` w ciele, po znalezieniu pary. Razem z `++index` w nagłówku przesuwa indeks o dwa, więc kolejne porównanie się nie wykonuje. Program zakłada rozłączne pary, a wymaganie mówi o nakładających się.
- **Poprawka:** usuń `++index;` z ciała. Indeks zmienia tylko nagłówek pętli.

Odczytu spoza tekstu tu nie ma: po dodatkowym przesunięciu warunek `index < text.size()` nadal sprawdza indeks przed odczytem.

Poprawiony program to program kontrolny z punktu 6: różni się od programu z błędem tylko tą jedną linijką. Dla wszystkich trzech tekstów daje wyniki z listy kontrolnej: przypadki H, F i G.

</details>

**Poprzednia lekcja:** [Lekcja 7.1: Pierwsze znaki: `char` i przeglądanie `std::string`](lesson_01_first_characters.md) · **Następna lekcja:** w przygotowaniu · [Opis kursu](../../README.md)

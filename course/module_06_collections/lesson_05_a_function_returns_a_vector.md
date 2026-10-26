# Lekcja 6.5: Funkcja tworzy i zwraca nowy wektor

**Polski** · [English](lesson_05_a_function_returns_a_vector.en.md) · [Opis kursu](../../README.md)

> **Moduł 6, lekcja 5** · około 65–80 minut
> **Potrzebujesz:** katalogu `cpp-workspace` i oryginalnego projektu `lesson_05_first_program`, jak dotąd. Debugger nie jest w tej lekcji potrzebny.
> **Wersja pilotażowa.** Programy z tej lekcji sprawdzamy automatycznie na Windowsie, Ubuntu i macOS, także z podanymi danymi wejściowymi. Wpisywanie danych w oknie **Run** CLiona opisujemy bez ręcznego sprawdzenia na każdym systemie.

## Zanim zaczniesz

Ta lekcja zakłada, że po lekcjach 6.1–6.4:

- przeglądasz wektor pętlą zakresową i dodajesz elementy przez `push_back`;
- sprawdzasz `empty()` i `size()`;
- piszesz funkcje, które dostają wektor przez `const std::vector<int>&` i zwracają wynik `int` (lekcja 6.4);
- wiesz, że zmienna zadeklarowana w funkcji jest jej zmienną lokalną (lekcja 5.2), a `return` przekazuje wynik do miejsca wywołania (lekcja 5.3).

## Sytuacja

W lekcji 6.4 funkcja `int count_cold_days(const std::vector<int>& temperatures)` zwracała **liczbę** dni poniżej zera. Zmieńmy pytanie: chcesz dostać **same temperatury** poniżej zera, żeby później jeszcze raz je przejrzeć. Dla danych `{3, -2, 0, -5, 4}` wynikiem ma być `{-2, -5}`.

Sama liczba 2 tu nie wystarczy: nie da się z niej odtworzyć wartości −2 i −5. Potrzebny jest wynik, który przechowuje wiele wartości, czyli **wektor**. Funkcja zwracająca `int` nie była gorsza: odpowiadała na inne pytanie.

Po tej lekcji będziesz:

- pisać funkcje z typem wyniku `std::vector<int>`, które budują nowy wektor i zwracają go przez `return`;
- odbierać zwrócony wektor w `main` i dalej z nim pracować;
- wyjaśniać, dlaczego wektor wejściowy zostaje bez zmian, a kolejność wybranych elementów jest zachowana;
- rozpoznawać pusty wynik jako poprawny i sprawdzać go przez `empty()`;
- przekazywać zwrócony wektor do kolejnej funkcji;
- samodzielnie projektować przetwarzanie: dane wejściowe → nowa kolekcja → podsumowanie.

## 1. Przygotuj projekt

W `cpp-workspace` utwórz katalog `lesson_6_5` i skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program`. Programy z punktów 2–5 wpisujesz w `main.cpp` tego katalogu.

## 2. Funkcja, która zwraca wektor

<!-- example: negatives_selected -->
```cpp
#include <iostream>
#include <vector>

std::vector<int> keep_negative(const std::vector<int>& values) {
    std::vector<int> selected{};

    for (const int value : values) {
        if (value < 0) {
            selected.push_back(value);
        }
    }

    return selected;
}

int main() {
    const std::vector<int> temperatures{3, -2, 0, -5, 4};

    std::cout << "Original:";
    for (const int temperature : temperatures) {
        std::cout << " " << temperature;
    }
    std::cout << "\n";

    const std::vector<int> selected{keep_negative(temperatures)};

    std::cout << "Selected:";
    for (const int temperature : selected) {
        std::cout << " " << temperature;
    }
    std::cout << "\n";

    std::cout << "Original after:";
    for (const int temperature : temperatures) {
        std::cout << " " << temperature;
    }
    std::cout << "\n";
}
```

**Przewidź** wszystkie trzy linijki. Czy po wywołaniu `keep_negative` w `temperatures` zostaną tylko wartości ujemne? Potem uruchom program.

<details>
<summary>Standardowe wyjście</summary>

<!-- output: negatives_selected -->
```text
Original: 3 -2 0 -5 4
Selected: -2 -5
Original after: 3 -2 0 -5 4
```

</details>

**Funkcja:**

- **Typ wyniku to `std::vector<int>`**: funkcja zwraca cały wektor liczb `int`, a nie jedną liczbę.
- **Wejście idzie przez `const&`**, jak w lekcji 6.4: funkcja tylko odczytuje `values`.
- **`selected` to osobny, lokalny wektor**, na początku pusty. Nie ma `const`, bo funkcja dopisuje do niego elementy.
- Pętla przegląda wartości wejściowe, a `push_back` dodaje do `selected` tylko te, które spełniają warunek. Kolejność wybranych elementów jest więc taka sama jak w wejściu.
- **`return selected;`** przekazuje gotowy wektor do miejsca wywołania. To zwracanie **przez wartość**, tak jak `return` liczby w lekcji 5.3: wywołujący dostaje własny wynik. Wektor `selected` jako zmienna lokalna kończy się razem z funkcją, ale jego zawartość trafia do `main` jako wynik.

**`main`:**

- `const std::vector<int> selected{keep_negative(temperatures)};` tworzy nową zmienną i zapisuje w niej wynik wywołania. `main` nie zamierza zmieniać tej kolekcji, więc ma ona `const`. Nie jest to obowiązek: w innym programie zwrócony wektor można dalej zmieniać.
- **Oryginał jest bez zmian.** Funkcja niczego z niego nie usuwa: tylko go czyta i buduje osobną kolekcję. Trzecia linijka to potwierdza.
- Wartości wypisujemy z odstępem **przed** każdą liczbą, a etykieta, na przykład `Original:`, kończy się dwukropkiem. Dzięki temu na końcu linijki nie zostaje zbędna spacja.

Nazwa `selected` występuje w obu funkcjach, ale to dwie różne zmienne lokalne, jak w lekcji 5.2.

## 3. Przepływ danych

| Etap | Dane |
|---|---|
| argument w `main` | `temperatures`: `{3, -2, 0, -5, 4}` |
| parametr `values` | odnosi się do `temperatures`, bez kopii |
| początkowy wynik lokalny `selected` | `{}` |
| po dodaniu −2 | `{-2}` |
| po dodaniu −5 | `{-2, -5}` |
| `return selected;` | funkcja przekazuje nowy wektor |
| wynik w `main` | `selected`: `{-2, -5}` |
| oryginał | `temperatures`: nadal `{3, -2, 0, -5, 4}` |

Funkcja robi trzy różne rzeczy: **odczytuje** istniejący wektor przez referencję, **buduje** nową kolekcję i **zwraca** ją przez wartość. Nowy wektor nie jest drugą nazwą oryginału, tylko osobnym wynikiem.

Czy zwracanie całego wektora jest kosztowne? Współczesny C++ potrafi efektywnie zwracać kolekcje przez wartość. Jak dokładnie to robi, poznasz później. Na razie wystarczy model: **funkcja tworzy kolekcję wynikową i zwraca ją jako wartość, a wywołujący dostaje własny wynik.**

## 4. Pusty wynik

<!-- example: no_negatives -->
```cpp
#include <iostream>
#include <vector>

std::vector<int> keep_negative(const std::vector<int>& values) {
    std::vector<int> selected{};

    for (const int value : values) {
        if (value < 0) {
            selected.push_back(value);
        }
    }

    return selected;
}

int main() {
    const std::vector<int> temperatures{2, 4, 7};
    const std::vector<int> selected{keep_negative(temperatures)};

    std::cout << "Values checked: " << temperatures.size() << "\n";

    if (selected.empty()) {
        std::cout << "No values below zero\n";
    } else {
        std::cout << "Values below zero: " << selected.size() << "\n";
    }
}
```

**Przewidź**, którą gałąź wykona program, i uruchom go.

<details>
<summary>Standardowe wyjście</summary>

<!-- output: no_negatives -->
```text
Values checked: 3
No values below zero
```

</details>

Wejście ma trzy elementy, ale żaden nie spełnia warunku, więc funkcja nic nie dodaje do `selected` i zwraca pusty wektor. **To poprawny wynik, a nie błąd**: „nie ma takich wartości” to też odpowiedź. Wywołujący rozpoznaje ją przez `empty()`. Z pustego wyniku nie odczytuje się elementów, na przykład `selected[0]`: takiego elementu nie ma (lekcja 6.3).

## 5. Wynik trafia do kolejnej funkcji

Zwrócony wektor to zwykły `std::vector<int>`, więc możesz go przekazać do funkcji z lekcji 6.4:

<!-- example: negative_total -->
```cpp
#include <iostream>
#include <vector>

std::vector<int> keep_negative(const std::vector<int>& values) {
    std::vector<int> selected{};

    for (const int value : values) {
        if (value < 0) {
            selected.push_back(value);
        }
    }

    return selected;
}

int total_values(const std::vector<int>& values) {
    int total{0};

    for (const int value : values) {
        total += value;
    }

    return total;
}

int main() {
    const std::vector<int> temperatures{3, -2, 0, -5, 4};
    const std::vector<int> selected{keep_negative(temperatures)};

    std::cout << "Values below zero: " << selected.size() << "\n";
    std::cout << "Their total: " << total_values(selected) << "\n";
}
```

**Przewidź** obie linijki i uruchom program.

<details>
<summary>Standardowe wyjście</summary>

<!-- output: negative_total -->
```text
Values below zero: 2
Their total: -7
```

</details>

1. `main` ma oryginalny wektor `temperatures`.
2. Wywołuje funkcję wybierającą.
3. Zapisuje nowy wektor w nazwanej zmiennej `selected`.
4. Przekazuje `selected` do `total_values` przez `const&`.
5. Dostaje wynik `int`.
6. Wypisuje raport.

Każda funkcja ma jedno zadanie: jedna wybiera, druga sumuje, a `main` wypisuje. Wynik można by też przekazać od razu, bez zmiennej pośredniej, i to też jest poprawny C++. W tej lekcji zapisujemy go w nazwanej zmiennej, bo każdy etap jest wtedy widoczny i łatwo go sprawdzić.

## 6. Misja: kontrola długości elementów

W warsztacie mierzy się długości elementów, w pełnych centymetrach. Element jest **zaakceptowany**, jeśli jego długość mieści się w przedziale od 30 do 60 cm **włącznie**. Dane są wpisane w kodzie:

<!-- fragment -->
```cpp
const std::vector<int> lengths{28, 30, 45, 65, 60, 29, 30};
```

**Wymagania:**

- Oryginalny wektor jest `const std::vector<int>` w `main` i zostaje bez zmian. Program nie odczytuje niczego z wejścia.
- **Funkcja wybierająca:** przyjmuje istniejący wektor przez `const&` oraz dolną i górną granicę jako dwa parametry `int`, buduje nowy wektor z zaakceptowanymi długościami, w ich kolejności, i zwraca go jako `std::vector<int>`. Niczego nie wypisuje.
- **Funkcja sumująca:** przyjmuje wektor przez `const&` i zwraca sumę jego wartości jako `int`, także dla pustego wektora. Niczego nie wypisuje.
- Nazwy funkcji i parametrów wybierasz samodzielnie.
- `main` wywołuje funkcję wybierającą, zapisuje wynik w zmiennej, przekazuje go do funkcji sumującej i wypisuje raport:
  - `Original pieces: N`: liczba elementów oryginalnego wektora;
  - `Accepted pieces: N`: liczba zaakceptowanych elementów;
  - `Accepted lengths:` i po spacji kolejne zaakceptowane długości, rozdzielone spacjami, bez spacji na końcu linijki, albo `Accepted lengths: none`, gdy nie zaakceptowano żadnego elementu;
  - `Total accepted length: N`: suma zaakceptowanych długości, 0 dla pustego wyniku.
- Wartości są małe, więc suma bezpiecznie mieści się w `int`.

W `cpp-workspace` utwórz katalog `piece_lengths`, skopiuj do niego `CMakeLists.txt` z oryginalnego `lesson_05_first_program`, utwórz pusty `main.cpp` i napisz program samodzielnie.

Dla danych powyżej standardowe wyjście ma być takie:

<!-- output: piece_lengths -->
```text
Original pieces: 7
Accepted pieces: 4
Accepted lengths: 30 45 60 30
Total accepted length: 165
```

**To nie jest program z punktu 5 z innymi napisami.** Tam warunek był jeden i stały. Musisz samodzielnie zdecydować:

1. jakie parametry ma funkcja wybierająca i w jakiej kolejności;
2. jak zapisać warunek, żeby obie granice, 30 i 60, były akceptowane;
3. gdzie powstaje wektor wynikowy i kiedy dodawać do niego element;
4. jak odebrać wynik w `main` i przekazać go do funkcji sumującej;
5. jak wypisać listę długości bez spacji na końcu i kiedy wypisać `none`;
6. jak sprawdzić, że oryginalny wektor się nie zmienił.

**Zanim napiszesz program**, przygotuj tabelę przypadków: dane z wymagań, pusty wektor, brak pasujących długości, same pasujące, obie granice osobno i razem, wartości tuż poza granicami (29 i 61), powtórzone wartości i inna kolejność tych samych długości. Przy każdym zapisz zaakceptowane długości i sumę.

**Potem:** uruchom program dla danych z wymagań, a następnie zmień wartości w nawiasach klamrowych na dwa, trzy przypadki z tabeli, na przykład pusty wynik i obie granice. Wszystkie przypadki z pełnej listy kontrolnej są sprawdzone automatycznie, więc nie musisz wpisywać ich wszystkich.

### Kryterium sukcesu

- Program buduje się jako C++20, a dla danych z wymagań wypisuje dokładnie cztery linijki pokazane wyżej.
- Funkcja wybierająca zwraca nowy `std::vector<int>`, przyjmuje wektor przez `const&` i dwie granice `int`, a długości 30 i 60 są akceptowane.
- Zaakceptowane długości są w kolejności z oryginału, z powtórzeniami.
- Suma jest liczona przez osobną funkcję, która dostaje zwrócony wektor.
- Dla pustego wyniku program wypisuje `Accepted lengths: none` i sumę 0.
- Żadna linijka nie kończy się spacją, a oryginalny wektor się nie zmienia.
- Umiesz wyjaśnić, dlaczego parametr ma `&`, a typ wyniku nie.

Gdy wynik się zgadza, możesz zapisać projekt w Gicie, jak w lekcji 1.5.

<details>
<summary>Podpowiedź 1</summary>

Czym powinien różnić się wektor wejściowy od wynikowego po zakończeniu filtrowania?

</details>

<details>
<summary>Podpowiedź 2</summary>

Funkcja może utworzyć pusty wektor i dodawać do niego tylko długości spełniające obie granice zakresu.

</details>

<details>
<summary>Podpowiedź 3</summary>

Po otrzymaniu nowego wektora nie obliczaj sumy ponownie w `main()`. Przekaż wynik filtrowania do osobnej funkcji sumującej.

</details>

<details>
<summary>Pełna lista przypadków kontrolnych: otwórz po przygotowaniu własnej tabeli</summary>

| | Oryginalne długości | Zaakceptowane | Suma | Co sprawdza |
|---|---|---|---|---|
| A | `{28, 30, 45, 65, 60, 29, 30}` | `30 45 60 30` | 165 | dane z wymagań |
| B | `{}` | `none` | 0 | puste wejście |
| C | `{10, 29, 61}` | `none` | 0 | brak pasujących, wartości tuż poza granicami |
| D | `{30, 45, 60}` | `30 45 60` | 135 | wszystkie pasują |
| E | `{29, 30, 60, 61}` | `30 60` | 90 | obie granice i wartości tuż obok nich |
| F | `{30}` | `30` | 30 | dolna granica, jeden element |
| G | `{60}` | `60` | 60 | górna granica, jeden element |
| H | `{45}` | `45` | 45 | jeden element w środku |
| I | `{30, 30, 60, 60}` | `30 30 60 60` | 180 | powtórzenia na granicach |
| J | `{60, 30, 45, 30}` | `60 30 45 30` | 165 | kolejność zachowana |
| K | `{0, 0}` | `none` | 0 | zera |
| L | `{30, 45}` | `30 45` | 75 | bez górnej granicy (punkt 7) |
| M | `{30, 60}` | `30 60` | 90 | z górną granicą (punkt 7) |

**Testy automatyczne i Twoje próby.** Wszystkie przypadki są sprawdzone automatycznie przez program kontrolny. To te same funkcje i ten sam raport co w rozwiązaniu referencyjnym, ale długości są odczytywane z wejścia: najpierw ich liczba, potem kolejne wartości. To tylko narzędzie do sprawdzania, a nie część misji. Program kontrolny i jego wyniki są w części [Przykładowe rozwiązania](#przykładowe-rozwiązania), bo zawierają rozwiązanie.

</details>

Przykładowe rozwiązanie jest w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 7. Znajdź błąd: zgubiona granica

To zadanie wykonaj **po misji**: program poniżej zawiera funkcję wybierającą z misji. Odczytuje długości z wejścia, tak jak program kontrolny. Wymaganie: zaakceptowane są długości od 30 do 60 cm **włącznie**.

<details>
<summary>Program do sprawdzenia: otwórz po napisaniu własnego programu</summary>

<!-- example: lengths_bound_bug -->
```cpp
#include <iostream>
#include <vector>

std::vector<int> keep_in_range(const std::vector<int>& values, int lowest, int highest) {
    std::vector<int> selected{};

    for (const int value : values) {
        if (value >= lowest && value < highest) {
            selected.push_back(value);
        }
    }

    return selected;
}

int total_length(const std::vector<int>& values) {
    int total{0};

    for (const int value : values) {
        total += value;
    }

    return total;
}

int main() {
    std::vector<int> lengths{};
    int piece_count{0};
    std::cin >> piece_count;

    for (int piece{1}; piece <= piece_count; ++piece) {
        int length{0};
        std::cin >> length;
        lengths.push_back(length);
    }

    if (std::cin.fail()) {
        std::cout << "Input could not be read\n";
    } else {
        const std::vector<int> accepted{keep_in_range(lengths, 30, 60)};

        std::cout << "Original pieces: " << lengths.size() << "\n";
        std::cout << "Accepted pieces: " << accepted.size() << "\n";

        std::cout << "Accepted lengths:";
        if (accepted.empty()) {
            std::cout << " none";
        } else {
            for (const int length : accepted) {
                std::cout << " " << length;
            }
        }
        std::cout << "\n";

        std::cout << "Total accepted length: " << total_length(accepted) << "\n";
    }
}
```

1. Przeczytaj wymaganie i **przewidź** zawartość nowego wektora dla danych `{30, 45}`, czyli `2`, `30`, `45`, oraz dla `{30, 60}`, czyli `2`, `30`, `60`.
2. Uruchom program dla `{30, 45}`. Czy wynik jest poprawny?
3. Uruchom go dla `{30, 60}`.
4. Porównaj oba wyniki z wymaganiem. Dlaczego pierwszy przypadek nie ujawnia błędu?
5. Znajdź błędne porównanie.
6. Popraw warunek.
7. Sprawdź oba przypadki ponownie, a także długości 29 i 61.

</details>

Wyniki programu przed poprawką i poprawiony program są w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 8. Gdy coś pójdzie inaczej

| Co widzisz | Co to znaczy | Co zrobić |
|---|---|---|
| Długość 60 albo 30 nie jest zaakceptowana | Warunek używa `<` albo `>` zamiast `<=` albo `>=`. | Granice są włącznie. Sprawdź przypadki F, G i M. |
| Zaakceptowane są wszystkie długości | `push_back` stoi poza warunkiem, jak w lekcji 6.2. | `push_back` tylko w bloku `if`. |
| Kolejność długości w wyniku jest inna niż w oryginale | Wynik nie jest budowany w jednym przejściu po oryginale, od początku do końca. | Dodawaj elementy w kolejności pętli zakresowej. Sprawdź przypadek J. |
| Linijka z długościami kończy się spacją | Spacja jest wypisywana **po** każdej liczbie. | Wypisuj spację **przed** każdą liczbą, jak w punkcie 2. |
| Dla pustego wyniku brakuje `none` albo pojawia się samo `Accepted lengths:` | Brakuje sprawdzenia `empty()` przed wypisywaniem. | Sprawdź `empty()` na zwróconym wektorze. |
| Błąd kompilacji przy odebraniu wyniku | Typ zmiennej w `main` albo typ wyniku funkcji nie pasuje, na przykład `int` zamiast `std::vector<int>`. | Funkcja wybierająca zwraca `std::vector<int>`, więc wynik zapisujesz w `std::vector<int>`. |

## 9. Wyjaśnij

Odpowiedz własnymi słowami, najlepiej na piśmie. Dopiero potem porównaj z przykładowymi odpowiedziami.

1. Dlaczego funkcja może zwracać wektor zamiast `int`?
2. Co oznacza typ wyniku `std::vector<int>`?
3. Dlaczego parametr wejściowy ma `const&`, a typ wyniku nie ma `&`?
4. Dlaczego lokalny wektor wynikowy nie ma `const`, a wynik odebrany w `main` może go mieć?
5. Co robi `return selected;` i co dzieje się z wynikiem po zakończeniu funkcji?
6. Czy funkcja wybierająca zmienia oryginalny wektor?
7. Czy wynik może być pusty i jak to rozpoznać?
8. Dlaczego kolejność wybranych elementów zostaje zachowana?
9. Czy zwrócony wektor można przekazać do kolejnej funkcji?
10. Dlaczego funkcja wybierająca nie wypisuje elementów?
11. Dlaczego przypadek `{30, 45}` nie ujawnia błędu z punktu 7?

<details>
<summary>Przykładowe odpowiedzi</summary>

1. Bo czasem odpowiedzią jest wiele wartości, na przykład wszystkie temperatury poniżej zera. Jedna liczba nie przechowa tych wartości.
2. Że funkcja zwraca wektor liczb `int`, czyli całą kolekcję.
3. Parametr odnosi się do istniejącego wektora wywołującego i tylko go czyta, więc nie potrzebuje kopii. Wynik to nowa kolekcja, której wywołujący jeszcze nie ma, więc funkcja przekazuje ją jako wartość.
4. Funkcja dopisuje do lokalnego wektora elementy, więc musi go zmieniać. `main` dostaje gotowy wynik i, jeśli nie zamierza go zmieniać, oznacza go `const`.
5. Przekazuje nowy wektor jako wynik do miejsca wywołania. Zmienna lokalna kończy się razem z funkcją, ale wywołujący ma już własny wynik i może go używać.
6. Nie. Dostaje go przez `const&`, więc może go tylko czytać. Wybrane wartości trafiają do osobnego wektora.
7. Tak, gdy żaden element nie spełnia warunku albo wejście jest puste. To poprawny wynik, a `empty()` daje wtedy `true`.
8. Bo funkcja przegląda wejście od pierwszego do ostatniego elementu, a `push_back` dodaje każdy wybrany element na koniec wyniku.
9. Tak. To zwykły `std::vector<int>`, więc można go przekazać do funkcji przyjmującej `const std::vector<int>&`, jak funkcja sumująca.
10. Bo jej zadaniem jest wybór danych. Wypisywanie to zadanie `main`, jak w lekcjach 5.5 i 6.4. Dzięki temu funkcję można wykorzystać też tam, gdzie nic nie trzeba wypisywać.
11. Bo nie ma w nim długości 60, a tylko dla niej błędny warunek `value < highest` daje inny wynik niż poprawny.

</details>

## Podsumowanie

- Funkcja może zwrócić cały wektor: `std::vector<int> keep_negative(const std::vector<int>& values)`.
- Typowy układ: wejście przez `const&`, lokalny pusty wektor wynikowy, `push_back` dla wybranych elementów i `return` tego wektora.
- Zwracanie odbywa się **przez wartość**: wywołujący dostaje własny wynik. Typ wyniku nie ma `&`.
- Wynik odbierasz do zmiennej, na przykład `const std::vector<int> selected{keep_negative(temperatures)};`.
- Oryginał zostaje bez zmian, a wybrane elementy zachowują jego kolejność.
- Pusty wektor to poprawny wynik. Rozpoznajesz go przez `empty()`.
- Zwrócony wektor możesz przekazać do kolejnej funkcji, na przykład sumującej.

## Co dalej

Następna lekcja to sprawdzian Modułu 6, który połączy przechowywanie danych, pętle, indeksy i funkcje na wektorach. Lekcja jest w przygotowaniu.

---

## Przykładowe rozwiązania

Zajrzyj tutaj **po własnej próbie**. Twoje nazwy mogą się różnić, jeśli standardowe wyjście jest takie, jak wymagane.

<details>
<summary>Punkt 6: misja, kontrola długości elementów</summary>

<!-- example: piece_lengths -->
```cpp
#include <iostream>
#include <vector>

std::vector<int> keep_in_range(const std::vector<int>& values, int lowest, int highest) {
    std::vector<int> selected{};

    for (const int value : values) {
        if (value >= lowest && value <= highest) {
            selected.push_back(value);
        }
    }

    return selected;
}

int total_length(const std::vector<int>& values) {
    int total{0};

    for (const int value : values) {
        total += value;
    }

    return total;
}

int main() {
    const std::vector<int> lengths{28, 30, 45, 65, 60, 29, 30};

    const std::vector<int> accepted{keep_in_range(lengths, 30, 60)};

    std::cout << "Original pieces: " << lengths.size() << "\n";
    std::cout << "Accepted pieces: " << accepted.size() << "\n";

    std::cout << "Accepted lengths:";
    if (accepted.empty()) {
        std::cout << " none";
    } else {
        for (const int length : accepted) {
            std::cout << " " << length;
        }
    }
    std::cout << "\n";

    std::cout << "Total accepted length: " << total_length(accepted) << "\n";
}
```

1. **Parametr wejściowy ma `const&`**, bo funkcja tylko czyta oryginał i nie potrzebuje jego kopii.
2. **Typ wyniku nie ma `&`**: funkcja zwraca nową kolekcję przez wartość. Wywołujący dostaje własny wynik.
3. **Wektor lokalny `selected` nie ma `const`**, bo funkcja dopisuje do niego zaakceptowane długości.
4. **Można go zwrócić**, bo `return` przekazuje jego zawartość do miejsca wywołania jako wynik, tak jak liczbę w lekcji 5.3.
5. **Odebrany wynik `accepted` ma `const`**, bo `main` go już nie zmienia: tylko wypisuje i przekazuje dalej.
6. **Przepływ:** `lengths` → `keep_in_range` (czyta przez `const&`, buduje i zwraca nowy wektor) → `accepted` w `main` → `total_length` (czyta przez `const&`, zwraca `int`) → raport.
7. **Oryginał zostaje bez zmian**, bo obie funkcje dostają go albo wynik przez `const&` i tylko czytają.
8. **Pusty wynik** znaczy „żaden element nie spełnia warunku”. Program wypisuje wtedy `none`, a `total_length` zwraca 0, bo jej pętla nie wykonuje żadnego przebiegu.

Granice idą jako parametry, więc ta sama funkcja wybierze też inny przedział. To jeden z możliwych podziałów: można na przykład wypisywać długości w osobnej funkcji `void`, jeśli funkcje obliczeniowe niczego nie wypisują.

**Program kontrolny** sprawdza wszystkie przypadki z listy kontrolnej. Funkcje są te same co wyżej, a część `main` od `const std::vector<int> accepted{...}` jest taka sama, poza wcięciem. Długości są odczytywane z wejścia przez `push_back`, jak w lekcji 6.2, więc wektor `lengths` nie ma `const`.

<!-- example: piece_lengths_check -->
```cpp
#include <iostream>
#include <vector>

std::vector<int> keep_in_range(const std::vector<int>& values, int lowest, int highest) {
    std::vector<int> selected{};

    for (const int value : values) {
        if (value >= lowest && value <= highest) {
            selected.push_back(value);
        }
    }

    return selected;
}

int total_length(const std::vector<int>& values) {
    int total{0};

    for (const int value : values) {
        total += value;
    }

    return total;
}

int main() {
    std::vector<int> lengths{};
    int piece_count{0};
    std::cin >> piece_count;

    for (int piece{1}; piece <= piece_count; ++piece) {
        int length{0};
        std::cin >> length;
        lengths.push_back(length);
    }

    if (std::cin.fail()) {
        std::cout << "Input could not be read\n";
    } else {
        const std::vector<int> accepted{keep_in_range(lengths, 30, 60)};

        std::cout << "Original pieces: " << lengths.size() << "\n";
        std::cout << "Accepted pieces: " << accepted.size() << "\n";

        std::cout << "Accepted lengths:";
        if (accepted.empty()) {
            std::cout << " none";
        } else {
            for (const int length : accepted) {
                std::cout << " " << length;
            }
        }
        std::cout << "\n";

        std::cout << "Total accepted length: " << total_length(accepted) << "\n";
    }
}
```

Dane wejściowe to liczba elementów, a po niej ich długości. Przypadki są w kolejności z listy kontrolnej, od A do M.

<!-- input: piece_lengths_check -->
```text
7
28
30
45
65
60
29
30
```

<!-- output: piece_lengths_check -->
```text
Original pieces: 7
Accepted pieces: 4
Accepted lengths: 30 45 60 30
Total accepted length: 165
```

<!-- input: piece_lengths_check -->
```text
0
```

<!-- output: piece_lengths_check -->
```text
Original pieces: 0
Accepted pieces: 0
Accepted lengths: none
Total accepted length: 0
```

<!-- input: piece_lengths_check -->
```text
3
10
29
61
```

<!-- output: piece_lengths_check -->
```text
Original pieces: 3
Accepted pieces: 0
Accepted lengths: none
Total accepted length: 0
```

<!-- input: piece_lengths_check -->
```text
3
30
45
60
```

<!-- output: piece_lengths_check -->
```text
Original pieces: 3
Accepted pieces: 3
Accepted lengths: 30 45 60
Total accepted length: 135
```

<!-- input: piece_lengths_check -->
```text
4
29
30
60
61
```

<!-- output: piece_lengths_check -->
```text
Original pieces: 4
Accepted pieces: 2
Accepted lengths: 30 60
Total accepted length: 90
```

<!-- input: piece_lengths_check -->
```text
1
30
```

<!-- output: piece_lengths_check -->
```text
Original pieces: 1
Accepted pieces: 1
Accepted lengths: 30
Total accepted length: 30
```

<!-- input: piece_lengths_check -->
```text
1
60
```

<!-- output: piece_lengths_check -->
```text
Original pieces: 1
Accepted pieces: 1
Accepted lengths: 60
Total accepted length: 60
```

<!-- input: piece_lengths_check -->
```text
1
45
```

<!-- output: piece_lengths_check -->
```text
Original pieces: 1
Accepted pieces: 1
Accepted lengths: 45
Total accepted length: 45
```

<!-- input: piece_lengths_check -->
```text
4
30
30
60
60
```

<!-- output: piece_lengths_check -->
```text
Original pieces: 4
Accepted pieces: 4
Accepted lengths: 30 30 60 60
Total accepted length: 180
```

<!-- input: piece_lengths_check -->
```text
4
60
30
45
30
```

<!-- output: piece_lengths_check -->
```text
Original pieces: 4
Accepted pieces: 4
Accepted lengths: 60 30 45 30
Total accepted length: 165
```

<!-- input: piece_lengths_check -->
```text
2
0
0
```

<!-- output: piece_lengths_check -->
```text
Original pieces: 2
Accepted pieces: 0
Accepted lengths: none
Total accepted length: 0
```

<!-- input: piece_lengths_check -->
```text
2
30
45
```

<!-- output: piece_lengths_check -->
```text
Original pieces: 2
Accepted pieces: 2
Accepted lengths: 30 45
Total accepted length: 75
```

<!-- input: piece_lengths_check -->
```text
2
30
60
```

<!-- output: piece_lengths_check -->
```text
Original pieces: 2
Accepted pieces: 2
Accepted lengths: 30 60
Total accepted length: 90
```

</details>

<details>
<summary>Punkt 7: wyniki przed poprawką i poprawiony program</summary>

Przed poprawką, dla `{30, 45}`:

<!-- input: lengths_bound_bug -->
```text
2
30
45
```

<!-- output: lengths_bound_bug -->
```text
Original pieces: 2
Accepted pieces: 2
Accepted lengths: 30 45
Total accepted length: 75
```

Dla `{30, 60}`:

<!-- input: lengths_bound_bug -->
```text
2
30
60
```

<!-- output: lengths_bound_bug -->
```text
Original pieces: 2
Accepted pieces: 1
Accepted lengths: 30
Total accepted length: 30
```

- Dla `{30, 45}` wynik jest poprawny: żadna długość nie jest równa 60, więc błędny warunek nie ma na co wpłynąć.
- Dla `{30, 60}` długość 60 zostaje pominięta: zaakceptowany jest 1 element zamiast 2, a suma to 30 zamiast 90.
- **Przyczyna:** warunek `value < highest` akceptuje długości od 30 do **mniej niż** 60. Wymaganie mówi o przedziale włącznie.
- **Poprawka:** `value <= highest`. Dolna granica była poprawna: `value >= lowest`.

Poprawiony program to program kontrolny z punktu 6: różni się od programu z błędem tylko tym porównaniem. Dla obu zestawów danych daje wyniki z listy kontrolnej: przypadki L i M. Granice sprawdzają też przypadki C, E, F i G.

</details>

**Poprzednia lekcja:** [Lekcja 6.4: Wektor jako parametr funkcji: `const&`](lesson_04_a_vector_as_a_parameter.md) · **Następna lekcja:** w przygotowaniu · [Opis kursu](../../README.md)

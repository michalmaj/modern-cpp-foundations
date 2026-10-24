# Lekcja 5.3: Funkcja zwraca wynik (`return`)

**Polski** · [English](lesson_03_returning_a_result.en.md) · [Opis kursu](../../README.md)

> **Moduł 5, lekcja 3** · około 75–90 minut
> **Potrzebujesz:** katalogu `cpp-workspace` i oryginalnego projektu `lesson_05_first_program`, jak dotąd. Debugger nie jest w tej lekcji potrzebny.
> **Wersja pilotażowa.** Programy z tej lekcji sprawdzamy automatycznie na Windowsie, Ubuntu i macOS, także z podanymi danymi wejściowymi. Wpisywanie danych w oknie **Run** CLiona opisujemy bez ręcznego sprawdzenia na każdym systemie.

## Zanim zaczniesz

Ta lekcja zakłada, że po lekcji 5.2:

- definiujesz funkcje `void` z parametrami i wywołujesz je z argumentami;
- wiesz, że parametr otrzymuje wartość argumentu, a funkcja pracuje na tej własnej wartości;
- pamiętasz, że `/` dla dwóch liczb `int` daje wynik całkowity (lekcje 2.4 i 2.5);
- używasz wartości `bool` w warunkach `if` (lekcja 3.2).

## Sytuacja

Funkcje z lekcji 5.1 i 5.2 wykonywały działanie, najczęściej wypisywały tekst. To, co obliczyły, mogły tylko pokazać na ekranie. Często jednak wynik obliczenia jest potrzebny **dalej w programie**: do kolejnego obliczenia, do porównania, do raportu. W tej lekcji funkcja **przekaże wynik** do miejsca wywołania, a to miejsce zdecyduje, co z nim zrobić.

Po tej lekcji będziesz:

- wskazywać typ wyniku funkcji i instrukcję `return`;
- wyjaśniać, co dzieje się po wykonaniu `return`;
- odróżniać zwracanie wyniku od wypisywania go przez `std::cout`;
- zapisywać wynik wywołania w zmiennej i używać go w wyrażeniach;
- wyjaśniać szczególną regułę zakończenia `int main()`;
- pisać funkcje zwracające `int`, `double` i `bool`;
- rozpoznawać dzielenie całkowite w funkcji, która zwraca `double`;
- wydzielać obliczenie do funkcji i zostawiać wypisywanie w `main`.

## 1. Przygotuj projekt

W `cpp-workspace` utwórz katalog `lesson_5_3` i skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program`. Programy z punktów 2–9 wpisujesz w `main.cpp` tego katalogu.

## 2. Funkcja wypisuje, ale nie oddaje wyniku

Ta funkcja przelicza minuty na sekundy i wypisuje wynik:

<!-- example: print_seconds -->
```cpp
#include <iostream>

void print_seconds(int minutes) {
    std::cout << minutes * 60 << "\n";
}

int main() {
    print_seconds(3);
}
```

<!-- output: print_seconds -->
```text
180
```

To poprawny program. Pojawia się jednak nowe wymaganie: do liczby sekund trzeba **dodać 30 sekund przygotowania** i wypisać sumę. Ktoś próbuje tak:

<!-- broken: void_as_value at=8:46 errors=1 error=^invalid operands to binary expression \('void' and 'int'\) -->
```cpp
#include <iostream>

void print_seconds(int minutes) {
    std::cout << minutes * 60 << "\n";
}

int main() {
    const int total_seconds{print_seconds(3) + 30};
    std::cout << "Total seconds: " << total_seconds << "\n";
}
```

**Przewidź**, czy ten program się zbuduje, i wyjaśnij dlaczego. Potem spróbuj go zbudować.

<details>
<summary>Co zgłasza kompilator i dlaczego</summary>

Program się nie zbuduje. Kompilator zgłasza w linijce 8 `invalid operands to binary expression ('void' and 'int')`: po lewej stronie `+` stoi coś typu `void`, a po prawej `int`, i takich wartości nie da się dodać.

Funkcja `print_seconds` obliczyła 180 i wypisała tę liczbę, ale **niczego nie przekazała** do miejsca wywołania. Jej typ wyniku to `void`, więc wywołanie `print_seconds(3)` nie jest liczbą, którą można dodać do 30. Wypisanie tekstu na ekran to coś innego niż przekazanie wyniku dalej.

</details>

Funkcja `print_seconds` nie jest błędna. Robi to, do czego ją napisano: wypisuje. Nowe wymaganie potrzebuje jednak funkcji, która **przekaże wynik** do miejsca wywołania.

## 3. Pierwsza funkcja zwracająca wynik

Oto funkcja, która oblicza liczbę sekund i przekazuje ją dalej:

<!-- example: seconds_with_preparation -->
```cpp
#include <iostream>

int seconds_from_minutes(int minutes) {
    const int seconds{minutes * 60};
    return seconds;
}

int main() {
    const int total_seconds{seconds_from_minutes(3) + 30};

    std::cout << "Total seconds: " << total_seconds << "\n";
}
```

| Część | W kodzie | Znaczenie |
|---|---|---|
| **Typ wyniku** | `int` przed nazwą funkcji | Funkcja przekazuje do miejsca wywołania wynik typu `int`. |
| **Parametr** | `int minutes` | Dane do obliczenia, jak w lekcji 5.2. |
| **Zmienna lokalna** | `const int seconds{minutes * 60};` | Przechowuje obliczony wynik w funkcji. |
| **`return`** | `return seconds;` | Kończy wykonanie funkcji i przekazuje wartość `seconds` do miejsca wywołania. |

Wywołanie `seconds_from_minutes(3)` daje teraz **wartość typu `int`**. Można jej użyć wszędzie tam, gdzie pasuje liczba `int`, na przykład w wyrażeniu `seconds_from_minutes(3) + 30`. O tym, co zrobić z wynikiem, decyduje `main`.

**Przewidź**, co wypisze program, i uruchom go.

<details>
<summary>Standardowe wyjście</summary>

<!-- output: seconds_with_preparation -->
```text
Total seconds: 210
```

Funkcja niczego nie wypisuje. Liczbę 210 wypisuje `std::cout` w `main`, po dodaniu 30 do zwróconego wyniku 180.

</details>

## 4. Gdzie powstaje wynik, a gdzie jest wypisywany

Program z punktu 3 wykonuje się tak:

| Krok | Gdzie jest program | Co się dzieje |
|---|---|---|
| 1 | `main` | Przygotowuje argument `3` i wywołuje `seconds_from_minutes(3)`. |
| 2 | funkcja | Parametr `minutes` otrzymuje wartość 3. |
| 3 | funkcja | Funkcja oblicza `3 * 60`, czyli 180, i zapisuje w `seconds`. |
| 4 | funkcja | `return seconds;` kończy funkcję i przekazuje wynik 180. |
| 5 | `main` | Program kontynuuje obliczenie w miejscu wywołania: `180 + 30`. |
| 6 | `main` | Zapisuje 210 w zmiennej `total_seconds`. |
| 7 | `main` | Dopiero `std::cout` wypisuje `Total seconds: 210`. |

**Obliczenie w funkcji i wypisanie wyniku nie muszą odbywać się w tym samym miejscu programu.**

Wynik można zapisać w zmiennej albo użyć go od razu. W tym programie funkcja `seconds_from_minutes` jest taka sama jak w punkcie 3:

<!-- example: seconds_two_ways -->
```cpp
#include <iostream>

int seconds_from_minutes(int minutes) {
    const int seconds{minutes * 60};
    return seconds;
}

int main() {
    std::cout << "Start\n";

    const int stored_seconds{seconds_from_minutes(2)};
    std::cout << stored_seconds << "\n";

    std::cout << seconds_from_minutes(2) << "\n";
    std::cout << "End\n";
}
```

**Przewidź** wszystkie linijki. Wskaż też dla każdego wywołania, w którym miejscu kończy się funkcja, a w którym `main` pracuje dalej.

<details>
<summary>Standardowe wyjście i wyjaśnienie</summary>

<!-- output: seconds_two_ways -->
```text
Start
120
120
End
```

- **Pierwsze wywołanie:** funkcja kończy się na `return seconds;`, a `main` zapisuje wynik 120 w `stored_seconds`. Wypisuje go dopiero następna linijka.
- **Drugie wywołanie** stoi wewnątrz instrukcji `std::cout`. Funkcja kończy się na `return`, a wypisywanie robi `std::cout` w `main`. Funkcja nic nie wypisała ani razu.
- `seconds` w funkcji i `stored_seconds` w `main` to dwie różne zmienne, jak parametr i argument w lekcji 5.2.

</details>

**Co robi `return`?** Wykonanie instrukcji `return` **kończy bieżące wywołanie funkcji** i przekazuje wynik do miejsca wywołania. Gdyby w tej samej funkcji stały po `return` jakieś instrukcje, w tym wywołaniu już by się nie wykonały. W tej lekcji każda funkcja zwracająca wynik ma jeden `return`, na końcu ciała. Funkcja `void` nie przekazuje zwykłej wartości wyniku, dlatego jej wywołania nie da się dodać ani zapisać w zmiennej `int`.

## 5. Wracamy do `int main()`

W lekcji 5.1 obiecaliśmy wyjaśnić słowo `int` przed `main`. Teraz znasz już funkcje z typem wyniku, więc wszystko się układa:

- `main` też jest funkcją, a jej typ wyniku to `int`.
- `main` ma szczególną rolę: od niej zaczyna się wykonywanie programu. Jej wynik nie trafia do innej funkcji Twojego programu, tylko do tego, kto uruchomił program. To **kod zakończenia** z lekcji 1.3. W naszym kursie normalne zakończenie to 0.
- Możesz zakończyć `main` jawnie, jak w lekcji 1.3:

<!-- fragment -->
```cpp
int main() {
    std::cout << "Done\n";
    return 0;
}
```

**Szczególna reguła `main`:** gdy wykonanie `main` dochodzi do zamykającej klamry bez `return`, działa to tak, jakby wykonało się `return 0;`. Dlatego wszystkie dotychczasowe programy z `int main()` bez `return` były poprawne. Nie musisz dopisywać `return 0;` do swoich programów.

**Tej reguły nie wolno przenosić na inne funkcje.** Zwykła funkcja z typem wyniku `int` **nie dostaje** automatycznie wyniku 0, gdy wykonanie dojdzie do końca jej ciała. Ten fragment **przeanalizuj, nie uruchamiaj go**:

<!-- fragment -->
```cpp
int seconds_from_minutes(int minutes) {
    const int seconds{minutes * 60};
}
```

Funkcja obiecuje wynik `int`, ale go nie przekazuje: nie ma `return`. Kompilator zwykle tylko ostrzega, więc program może się zbudować. Taki program ma jednak **niezdefiniowane zachowanie**: wynik wywołania nie jest określony i nie można na nim polegać, nawet jeśli raz wygląda poprawnie. Każda zwykła funkcja, która ma typ wyniku inny niż `void`, musi przekazać wynik przez `return`.

## 6. Znajdź błąd: wynik wypisany dwa razy

Wymaganie: program przelicza 2 minuty na sekundy i wypisuje **dokładnie jedną** linijkę: `Seconds: 120`.

<!-- example: double_print_bug -->
```cpp
#include <iostream>

int seconds_from_minutes(int minutes) {
    const int seconds{minutes * 60};
    std::cout << seconds << "\n";
    return seconds;
}

int main() {
    const int seconds{seconds_from_minutes(2)};
    std::cout << "Seconds: " << seconds << "\n";
}
```

1. Przeczytaj wymaganie.
2. **Przewidź** standardowe wyjście.
3. Uruchom program.
4. Wskaż obie instrukcje, które wypisują liczbę.
5. Zdecyduj, za co odpowiada funkcja, a za co `main`.
6. Popraw program.
7. Uruchom go ponownie.

Wynik przed poprawką i poprawiony program są w części [Przykładowe rozwiązania](#przykładowe-rozwiązania). Zajrzyj tam po własnej próbie.

## 7. Wynik typu `double`

Wynik funkcji nie musi być typu `int`:

<!-- example: average_of_two -->
```cpp
#include <iostream>

double average_of_two(double first, double second) {
    return (first + second) / 2.0;
}

int main() {
    const double average{average_of_two(2.0, 3.0)};
    std::cout << "Average: " << average << "\n";
}
```

- Parametry mają typ `double`, a typ wyniku funkcji to też `double`.
- `return` może przekazać od razu wartość wyrażenia. Nie trzeba jej najpierw zapisywać w zmiennej.
- Zwrócony wynik trafia do zmiennej `double` w `main`. Wypisuje go `std::cout`, osobno.

**Przewidź** wynik i uruchom program.

<details>
<summary>Standardowe wyjście</summary>

<!-- output: average_of_two -->
```text
Average: 2.5
```

</details>

## 8. Znajdź błąd: średnia bez części ułamkowej

Wymaganie: funkcja oblicza średnią dwóch liczb **całkowitych** i zwraca ją jako `double`, z częścią ułamkową, jeśli jest potrzebna.

<!-- example: average_int_bug -->
```cpp
#include <iostream>

double average_of_two(int first, int second) {
    return (first + second) / 2;
}

int main() {
    std::cout << "Average of 2 and 4: " << average_of_two(2, 4) << "\n";
    std::cout << "Average of 3 and 4: " << average_of_two(3, 4) << "\n";
}
```

**Przewidź** obie linijki. Jaka jest poprawna średnia dla 2 i 4, a jaka dla 3 i 4? Który przypadek ujawni błąd? Uruchom program, znajdź przyczynę i popraw jedną zmianą.

Wynik przed poprawką i poprawka są w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 9. Funkcja odpowiada na pytanie: `bool`

Funkcja może zwrócić odpowiedź `true` albo `false`. Takiej funkcji używa się wygodnie w warunku:

<!-- example: even_check -->
```cpp
#include <iostream>

bool is_even(int number) {
    return number % 2 == 0;
}

int main() {
    for (int number{4}; number <= 7; ++number) {
        if (is_even(number)) {
            std::cout << number << " is even\n";
        } else {
            std::cout << number << " is odd\n";
        }
    }
}
```

`number % 2 == 0` to znany Ci warunek z lekcji 3.2. Funkcja zwraca jego wartość, a `if` w `main` decyduje, co wypisać. Nazwa zaczynająca się od `is_` podpowiada, że funkcja odpowiada na pytanie „tak albo nie”.

**Przewidź** cztery linijki i uruchom program.

<details>
<summary>Standardowe wyjście</summary>

<!-- output: even_check -->
```text
4 is even
5 is odd
6 is even
7 is odd
```

</details>

## 10. Misja: zmiana temperatury w stopniach Fahrenheita

Program porównuje dwie temperatury. Użytkownik podaje je w stopniach Celsjusza, a program przelicza obie na stopnie Fahrenheita i podaje, o ile zmieniła się temperatura. Wzór:

**F = C · 9 / 5 + 32**

W obliczeniach typu `double` użyj stałych `9.0`, `5.0` i `32.0`.

**Wymagania:**

- Program wypisuje `Enter two Celsius temperatures (-40 to 40):` i odczytuje dwie liczby typu `double`: pierwszą i drugą temperaturę.
- Jeśli odczyt się nie uda, wypisuje tylko `Input could not be read`.
- Jeśli odczytano obie liczby, ale choć jedna jest spoza zakresu od -40 do 40 włącznie, wypisuje tylko `Invalid temperature data`. To zakres przyjęty w tym zadaniu, a nie ograniczenie typu `double`.
- Dla poprawnych danych wypisuje trzy linijki: `First Fahrenheit: X`, `Second Fahrenheit: Y` i `Change Fahrenheit: Z`, gdzie `Z` to druga temperatura w stopniach Fahrenheita minus pierwsza. `Z` może być dodatnie, ujemne albo równe zero.
- Program nie pyta ponownie i po błędzie nie wypisuje żadnej z trzech linijek raportu.
- Przeliczenie wykonuje **Twoja własna funkcja**: przyjmuje jedną temperaturę typu `double` i zwraca temperaturę w stopniach Fahrenheita jako `double`. Funkcja niczego nie wypisuje i niczego nie odczytuje. Nazwę funkcji i parametru wybierasz samodzielnie.
- Odczyt, sprawdzenie danych, wywołania funkcji, obliczenie różnicy i raport należą do `main`.
- Nie używaj zmiennych zadeklarowanych poza funkcjami.

Do sprawdzenia odczytu wystarczy `std::cin.fail()`, jak w lekcji 5.2.

W `cpp-workspace` utwórz katalog `fahrenheit_change`, skopiuj do niego `CMakeLists.txt` z oryginalnego `lesson_05_first_program`, utwórz pusty `main.cpp` i napisz program samodzielnie.

Dla danych `0` i `10` standardowe wyjście ma być takie:

<!-- input: fahrenheit_change -->
```text
0
10
```

<!-- output: fahrenheit_change -->
```text
Enter two Celsius temperatures (-40 to 40):
First Fahrenheit: 32
Second Fahrenheit: 50
Change Fahrenheit: 18
```

**Przewidź**, zanim napiszesz program: co wypisze on dla danych `12.5` i `20`?

<!-- input: fahrenheit_change -->
```text
12.5
20
```

<details>
<summary>Standardowe wyjście dla 12.5 i 20</summary>

<!-- output: fahrenheit_change -->
```text
Enter two Celsius temperatures (-40 to 40):
First Fahrenheit: 54.5
Second Fahrenheit: 68
Change Fahrenheit: 13.5
```

</details>

**To nie jest `seconds_from_minutes` z innym wzorem.** Tam jeden wynik trafiał do jednego prostego obliczenia. Tutaj ta sama funkcja daje **dwa wyniki** dla dwóch różnych danych, a `main` używa obu jeszcze raz, przy obliczaniu różnicy. Musisz samodzielnie zdecydować:

1. jak nazwać funkcję i parametr i jak zapisać wzór w `return`;
2. gdzie przechować oba zwrócone wyniki, skoro potrzebujesz ich i w raporcie, i w różnicy;
3. w jakiej kolejności odejmować, żeby różnica była „druga minus pierwsza”;
4. jak sprawdzić dane, zanim program cokolwiek przeliczy.

**Zanim napiszesz program**, przygotuj tabelę przypadków testowych: obie granice zakresu, równe temperatury, druga temperatura niższa od pierwszej, temperatura z częścią ułamkową, wartości tuż poza zakresem, tekst zamiast pierwszej i zamiast drugiej liczby oraz dane, które kończą się po jednej liczbie. Przy każdym przypadku zapisz oczekiwane standardowe wyjście. Dobieraj temperatury tak, żeby wynik łatwo było policzyć w pamięci.

Przypadki z danymi, które kończą się wcześniej, przeanalizuj na papierze, jak w lekcjach 4.5–5.2, zamiast je uruchamiać, i porównaj ze zwiniętą listą kontrolną. Program z tej lekcji jest dla takich danych sprawdzany osobno, automatycznymi testami kursu.

### Kryterium sukcesu

- Program buduje się jako C++20, a jego standardowe wyjście dla danych `0`, `10` oraz `12.5`, `20` jest dokładnie takie jak powyżej.
- Dla każdego przypadku, który możesz wpisać, standardowe wyjście zgadza się z listą kontrolną. Przypadki z danymi, które kończą się wcześniej, sprawdzasz rozumowaniem.
- Przeliczenie wykonuje Twoja funkcja, która przyjmuje `double`, zwraca `double`, nie wypisuje i nie odczytuje niczego. Wzór występuje w kodzie tylko w niej.
- Każda temperatura w raporcie pojawia się raz. Różnica jest obliczona z wyników zwróconych przez funkcję.
- Przy nieudanym odczycie albo danych spoza zakresu nie pojawia się żadna linijka raportu.
- Program nie używa zmiennych zadeklarowanych poza funkcjami.
- Tabela przypadków powstała przed uruchomieniem programu.
- Umiesz wskazać typ wyniku i `return` w swojej funkcji oraz wyjaśnić, gdzie powstaje każdy wynik, a gdzie jest wypisywany.

Gdy wynik się zgadza, możesz zapisać projekt w Gicie, jak w lekcji 1.5.

<details>
<summary>Podpowiedź 1</summary>

Która część programu zawsze wykonuje to samo obliczenie, niezależnie od tego, czy przeliczasz pierwszą, czy drugą temperaturę?

</details>

<details>
<summary>Podpowiedź 2</summary>

W jaki sposób `main` może wykorzystać wynik funkcji również później, przy obliczaniu różnicy?

</details>

<details>
<summary>Podpowiedź 3</summary>

Rozdziel zadania: funkcja zwraca przeliczoną temperaturę, a `main` przechowuje oba wyniki, odejmuje pierwszy od drugiego i wypisuje raport.

</details>

<details>
<summary>Pełna lista przypadków kontrolnych: otwórz po przygotowaniu własnej tabeli</summary>

| Dane | Standardowe wyjście po pytaniu | Co sprawdza |
|---|---|---|
| `0`, `10` | 32, 50, zmiana 18 | przykład z treści |
| `12.5`, `20` | 54.5, 68, zmiana 13.5 | część ułamkowa |
| `-40`, `0` | -40, 32, zmiana 72 | dolna granica |
| `20`, `20` | 68, 68, zmiana 0 | równe temperatury |
| `40`, `-40` | 104, -40, zmiana -144 | górna granica, spadek |
| `25`, `0` | 77, 32, zmiana -45 | spadek temperatury |
| `-41`, `0` | `Invalid temperature data` | pierwsza tuż pod zakresem |
| `0`, `41` | `Invalid temperature data` | druga tuż nad zakresem |
| `abc`, `10` | `Input could not be read` | tekst zamiast pierwszej liczby |
| `10`, `abc` | `Input could not be read` | tekst zamiast drugiej liczby |
| `10`, koniec danych | `Input could not be read` | dane kończą się po jednej liczbie |
| brak danych | `Input could not be read` | dane kończą się od razu |

Pierwsze dwa przypadki są sprawdzone wyżej, przy treści misji.

<!-- input: fahrenheit_change -->
```text
-40
0
```

<!-- output: fahrenheit_change -->
```text
Enter two Celsius temperatures (-40 to 40):
First Fahrenheit: -40
Second Fahrenheit: 32
Change Fahrenheit: 72
```

<!-- input: fahrenheit_change -->
```text
20
20
```

<!-- output: fahrenheit_change -->
```text
Enter two Celsius temperatures (-40 to 40):
First Fahrenheit: 68
Second Fahrenheit: 68
Change Fahrenheit: 0
```

<!-- input: fahrenheit_change -->
```text
40
-40
```

<!-- output: fahrenheit_change -->
```text
Enter two Celsius temperatures (-40 to 40):
First Fahrenheit: 104
Second Fahrenheit: -40
Change Fahrenheit: -144
```

<!-- input: fahrenheit_change -->
```text
25
0
```

<!-- output: fahrenheit_change -->
```text
Enter two Celsius temperatures (-40 to 40):
First Fahrenheit: 77
Second Fahrenheit: 32
Change Fahrenheit: -45
```

<!-- input: fahrenheit_change -->
```text
-41
0
```

<!-- output: fahrenheit_change -->
```text
Enter two Celsius temperatures (-40 to 40):
Invalid temperature data
```

<!-- input: fahrenheit_change -->
```text
0
41
```

<!-- output: fahrenheit_change -->
```text
Enter two Celsius temperatures (-40 to 40):
Invalid temperature data
```

<!-- input: fahrenheit_change -->
```text
abc
10
```

<!-- output: fahrenheit_change -->
```text
Enter two Celsius temperatures (-40 to 40):
Input could not be read
```

<!-- input: fahrenheit_change -->
```text
10
abc
```

<!-- output: fahrenheit_change -->
```text
Enter two Celsius temperatures (-40 to 40):
Input could not be read
```

<!-- input: fahrenheit_change -->
```text
10
```

<!-- output: fahrenheit_change -->
```text
Enter two Celsius temperatures (-40 to 40):
Input could not be read
```

<!-- input: fahrenheit_change -->
```text
```

<!-- output: fahrenheit_change -->
```text
Enter two Celsius temperatures (-40 to 40):
Input could not be read
```

Temperatury w tych testach dobrano tak, żeby obliczenia typu `double` dawały dokładne, krótkie wyniki. Nie każde przeliczenie wypisze się tak prosto, ale te testy sprawdzają logikę programu, a nie zaokrąglenia.

</details>

Przykładowe rozwiązanie jest w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 11. Gdy coś pójdzie inaczej

| Co widzisz | Co to znaczy | Co zrobić |
|---|---|---|
| `invalid operands to binary expression ('void' and …)` albo inny błąd z `void` przy wywołaniu | Wynik funkcji `void` jest używany jak liczba (punkt 2). | Jeśli wynik jest potrzebny dalej, funkcja musi mieć typ wyniku i `return`. |
| Ostrzeżenie, że funkcja nie zwraca wartości | W funkcji z typem wyniku innym niż `void` brakuje `return`. | Dopisz `return` z wynikiem. Nie polegaj na takim programie, nawet jeśli się zbudował (punkt 5). |
| Ta sama liczba pojawia się dwa razy | Wypisuje i funkcja, i `main` (punkt 6). | Funkcja obliczeniowa tylko zwraca wynik. Wypisuje `main`. |
| Średnia nie ma części ułamkowej | Dzielenie odbywa się na liczbach `int`, zanim wynik trafi do `return` (punkt 8). | Dziel przez `2.0` albo pracuj na liczbach `double`. |
| Różnica temperatur ma zły znak | Odejmowanie stoi w odwrotnej kolejności. | Różnica to druga temperatura minus pierwsza. |
| Przeliczona temperatura jest zła | Wzór jest zapisany inaczej niż `C · 9 / 5 + 32`. | Sprawdź wzór dla 0 (wynik 32) i 100 (wynik 212). |
| Po błędnych danych pojawia się część raportu | Raport stoi przed sprawdzeniem danych albo poza gałęzią poprawnych danych. | Najpierw sprawdź odczyt i zakres, a raport wypisuj tylko dla poprawnych danych. |
| Program nic nie robi i czeka | Czeka na kolejną liczbę, jak w lekcji 2.6. | Wpisz liczbę i naciśnij **Enter**. Przypadku z końcem danych nie sprawdzaj w ten sposób: prześledź go na papierze. |

## 12. Wyjaśnij

Odpowiedz własnymi słowami, najlepiej na piśmie. Dopiero potem porównaj z przykładowymi odpowiedziami.

1. Co oznacza typ `int` przed nazwą funkcji?
2. Czym jest wartość zwracana?
3. Co wykonuje `return`?
4. Dlaczego `std::cout` nie zastępuje `return`?
5. Czy funkcja może zwrócić wynik bez wypisywania czegokolwiek?
6. Czy wynik wywołania można przypisać do zmiennej?
7. Czy można użyć wyniku funkcji w obliczeniu?
8. Dlaczego `main` ma szczególną regułę domyślnego wyniku 0?
9. Czy zwykła funkcja `int` dostaje automatycznie wynik 0 przy osiągnięciu zamykającej klamry?
10. Dlaczego typ wyniku `double` nie naprawia wcześniejszego dzielenia całkowitego?
11. Czy funkcja może zwrócić `bool`?
12. Dlaczego funkcja przeliczająca temperaturę nie musi wypisywać komunikatów?
13. Co jest odpowiedzialnością `main` w misji?
14. Dlaczego warto przetestować równe temperatury i przypadek, w którym druga jest niższa od pierwszej?

<details>
<summary>Przykładowe odpowiedzi</summary>

1. Że funkcja przekazuje do miejsca wywołania wynik typu `int`.
2. To wartość, którą funkcja przekazuje do miejsca wywołania przez `return`. Wywołanie funkcji staje się tą wartością.
3. Kończy bieżące wywołanie funkcji i przekazuje wynik do miejsca wywołania.
4. Bo `std::cout` tylko wypisuje tekst na ekran. Miejsce wywołania nie dostaje wtedy żadnej wartości, której mogłoby użyć dalej.
5. Tak. Tak działa `seconds_from_minutes`: zwraca wynik, a wypisuje go dopiero `main`, jeśli chce.
6. Tak, na przykład `const int stored_seconds{seconds_from_minutes(2)};`.
7. Tak, na przykład `seconds_from_minutes(3) + 30`.
8. Bo `main` jest szczególną funkcją, od której zaczyna się program. C++ ustala, że dojście do końca `main` bez `return` działa jak `return 0;`, czyli normalne zakończenie programu.
9. Nie. Ta reguła dotyczy tylko `main`. Zwykła funkcja z wynikiem `int` musi przekazać wynik przez `return`. Bez tego program ma niezdefiniowane zachowanie.
10. Bo dzielenie `(first + second) / 2` na liczbach `int` daje wynik całkowity, zanim `return` przekaże wartość. Zmiana na `double` przy zwracaniu nie przywraca utraconej części ułamkowej.
11. Tak, na przykład `is_even`. Zwrócone `true` albo `false` można od razu użyć w `if`.
12. Bo jej zadaniem jest obliczenie. Co zrobić z wynikiem, decyduje `main`: tu wypisuje go w raporcie i używa jeszcze do różnicy.
13. Odczyt i sprawdzenie danych, wywołanie funkcji dla obu temperatur, przechowanie wyników, obliczenie różnicy i wypisanie raportu.
14. Bo równe temperatury dają różnicę 0, a niższa druga temperatura daje różnicę ujemną. Te przypadki ujawniają zamienioną kolejność odejmowania, której nie widać, gdy temperatura rośnie i nie sprawdzisz znaku.

</details>

## Podsumowanie

- **Typ wyniku** przed nazwą funkcji, na przykład `int`, `double` albo `bool`, mówi, jaki wynik funkcja przekazuje do miejsca wywołania. `void` znaczy: żadnego zwykłego wyniku.
- **`return` wartość;** kończy wywołanie funkcji i przekazuje wynik. Wywołanie funkcji staje się tą wartością.
- Wynik wywołania można zapisać w zmiennej, użyć w wyrażeniu albo w warunku.
- **`return` to nie `std::cout`.** `return` przekazuje wynik do programu, `std::cout` wypisuje tekst na ekran. Funkcja obliczeniowa zwraca, a o wypisaniu decyduje miejsce wywołania.
- `main` ma typ wyniku `int`. Jej wynik to kod zakończenia programu. Tylko w `main` dojście do zamykającej klamry działa jak `return 0;`.
- Zwykła funkcja z typem wyniku innym niż `void` zawsze musi przekazać wynik przez `return`.
- Dzielenie dwóch liczb `int` daje wynik całkowity, nawet jeśli funkcja zwraca `double`.
- Funkcja zwracająca `bool` odpowiada na pytanie i dobrze pasuje do warunku `if`.

## Co dalej

Funkcje z tej lekcji obliczają wynik zawsze tym samym wzorem. W kolejnej lekcji funkcja podejmie decyzję i zależnie od danych przekaże różne wyniki: [Lekcja 5.4: Kilka dróg do `return`](lesson_04_several_returns.md).

---

## Przykładowe rozwiązania

Zajrzyj tutaj **po własnej próbie**. Twoje nazwy mogą się różnić, jeśli standardowe wyjście jest takie, jak wymagane.

<details>
<summary>Punkt 6: wynik przed poprawką i poprawiony program</summary>

Przed poprawką:

<!-- output: double_print_bug -->
```text
120
Seconds: 120
```

- Liczba 120 pojawia się **dwa razy**: raz wypisuje ją funkcja, raz `main`. Wymaganie mówi o jednej linijce.
- **Odpowiedzialność:** funkcja oblicza i zwraca liczbę sekund. O tym, jak pokazać wynik, decyduje `main`.
- **Poprawka:** usuń wypisywanie z funkcji.

<!-- example: double_print_fixed -->
```cpp
#include <iostream>

int seconds_from_minutes(int minutes) {
    const int seconds{minutes * 60};
    return seconds;
}

int main() {
    const int seconds{seconds_from_minutes(2)};
    std::cout << "Seconds: " << seconds << "\n";
}
```

<!-- output: double_print_fixed -->
```text
Seconds: 120
```

Funkcja, która i wypisuje, i zwraca wynik, jest poprawnym C++. W tym zadaniu jest jednak niezgodna z wymaganiem i niepotrzebnie miesza dwie odpowiedzialności: obliczenie i prezentację wyniku.

</details>

<details>
<summary>Punkt 8: wynik przed poprawką i poprawka</summary>

Przed poprawką:

<!-- output: average_int_bug -->
```text
Average of 2 and 4: 3
Average of 3 and 4: 3
```

- **Dla 2 i 4** wynik jest poprawny, bo 6 / 2 to dokładnie 3. Ten przypadek ukrywa błąd.
- **Dla 3 i 4** poprawna średnia to 3.5, a program wypisuje 3.
- **Przyczyna:** `first + second` i `2` są typu `int`, więc `7 / 2` daje 3, jak w lekcji 2.4. Dopiero ten całkowity wynik trafia do `return` i zamienia się na `double`. Typ wyniku funkcji nie zmienia wcześniejszego dzielenia.
- **Poprawka:** dziel przez `2.0`, jak w lekcji 2.5. Wtedy dzielenie odbywa się na liczbach typu `double`.

<!-- example: average_int_fixed -->
```cpp
#include <iostream>

double average_of_two(int first, int second) {
    return (first + second) / 2.0;
}

int main() {
    std::cout << "Average of 2 and 4: " << average_of_two(2, 4) << "\n";
    std::cout << "Average of 3 and 4: " << average_of_two(3, 4) << "\n";
}
```

<!-- output: average_int_fixed -->
```text
Average of 2 and 4: 3
Average of 3 and 4: 3.5
```

</details>

<details>
<summary>Punkt 10: misja, zmiana temperatury</summary>

<!-- example: fahrenheit_change -->
```cpp
#include <iostream>

double fahrenheit_from_celsius(double celsius) {
    return celsius * 9.0 / 5.0 + 32.0;
}

int main() {
    double first_celsius{0.0};
    double second_celsius{0.0};

    std::cout << "Enter two Celsius temperatures (-40 to 40):\n";
    std::cin >> first_celsius;
    std::cin >> second_celsius;

    if (std::cin.fail()) {
        std::cout << "Input could not be read\n";
    } else {
        const bool first_valid{first_celsius >= -40.0 && first_celsius <= 40.0};
        const bool second_valid{second_celsius >= -40.0 && second_celsius <= 40.0};

        if (first_valid && second_valid) {
            const double first_fahrenheit{fahrenheit_from_celsius(first_celsius)};
            const double second_fahrenheit{fahrenheit_from_celsius(second_celsius)};

            std::cout << "First Fahrenheit: " << first_fahrenheit << "\n";
            std::cout << "Second Fahrenheit: " << second_fahrenheit << "\n";
            std::cout << "Change Fahrenheit: " << second_fahrenheit - first_fahrenheit << "\n";
        } else {
            std::cout << "Invalid temperature data\n";
        }
    }
}
```

- **Funkcja** `fahrenheit_from_celsius` tylko oblicza: przyjmuje `double`, zwraca `double` jednym `return` z wzorem. Nie wypisuje i nie odczytuje niczego.
- **`main`** wywołuje funkcję dwa razy, z różnymi argumentami. Oba wyniki zapisuje w zmiennych `const double`, bo każdego używa dwa razy: w raporcie i w różnicy. Wzór nie powtarza się w `main`.
- **Różnica** to `second_fahrenheit - first_fahrenheit`, czyli druga minus pierwsza. Dla `40`, `-40` wynosi -144, dla `20`, `20` wynosi 0.
- **Kolejność działań:** `celsius * 9.0 / 5.0 + 32.0` mnoży, dzieli, a dopiero potem dodaje 32, jak we wzorze. Stałe `9.0` i `5.0` sprawiają, że całe obliczenie odbywa się na liczbach `double`.
- **Dane:** jedno sprawdzenie `std::cin.fail()` po obu odczytach wystarcza, jak w lekcji 5.2. Sprawdzenie zakresu stoi w gałęzi udanego odczytu, a raport tylko w gałęzi poprawnych danych.

</details>

**Poprzednia lekcja:** [Lekcja 5.2: Parametry, argumenty i przekazywanie przez wartość](lesson_02_parameters_and_arguments.md) · **Następna lekcja:** [Lekcja 5.4: Kilka dróg do `return`](lesson_04_several_returns.md) · [Opis kursu](../../README.md)

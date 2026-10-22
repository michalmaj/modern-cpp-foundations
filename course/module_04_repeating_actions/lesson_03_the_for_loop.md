# Lekcja 4.3: Pętla `for`: licznik, warunek i aktualizacja w jednym miejscu

**Polski** · [English](lesson_03_the_for_loop.en.md) · [Opis kursu](../../README.md)

> **Moduł 4, lekcja 3** · około 70–85 minut
> **Potrzebujesz:** katalogu `cpp-workspace` i oryginalnego projektu `lesson_05_first_program`, jak dotąd. Debugger nie jest w tej lekcji potrzebny.
> **Wersja pilotażowa.** Programy z tej lekcji sprawdzamy automatycznie na Windowsie, Ubuntu i macOS, także z podanymi danymi wejściowymi.

## Zanim zaczniesz

Ta lekcja zakłada, że po lekcjach 4.1 i 4.2:

- piszesz pętlę `while` z licznikiem i wskazujesz jej cztery części: wartość początkową, warunek, ciało i zmianę licznika;
- śledzisz pętlę w tabeli, w której ostatnie sprawdzenie warunku daje `false` i nie jest przebiegiem;
- wiesz, że pętla może wykonać się zero razy;
- gromadzisz wynik w akumulatorze i aktualizujesz go przez `+=`;
- pamiętasz z lekcji 3.2, że zmienna zadeklarowana w bloku istnieje tylko w nim.

## Sytuacja

Każda pętla z lekcji 4.1 i 4.2 miała ten sam układ: licznik z wartością początkową **przed** pętlą, warunek **na górze** i zmianę licznika **na końcu** ciała. Trzy rzeczy, które razem sterują powtarzaniem, stały w trzech różnych miejscach programu. W dłuższej pętli łatwo wtedy przeoczyć, od czego licznik zaczyna albo czy w ogóle się zmienia.

Dziś poznasz pętlę `for`, która zbiera te trzy części w jednej linijce. Nie robi niczego, czego nie potrafi `while`. Porządkuje tylko zapis pętli sterowanej licznikiem.

Po tej lekcji będziesz:

- wskazywać trzy części nagłówka `for` i wyjaśniać, kiedy wykonuje się każda z nich;
- przewidywać wartości licznika w kolejnych przebiegach, także przy zerze przebiegów;
- zwiększać licznik o jeden zapisem `++counter`;
- wyjaśniać, dlaczego licznik zadeklarowany w nagłówku `for` nie istnieje po pętli;
- znajdować w `for` błąd o jeden krok;
- łączyć `for` z akumulatorem;
- wybierać między `while` a `for` tam, gdzie oba zapisy są możliwe.

## 1. Przygotuj projekt

W `cpp-workspace` utwórz katalog `lesson_4_3` i skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program`. Programy z punktów 2–9 wpisujesz w `main.cpp` tego katalogu.

## 2. Od `while` do `for`

Ten program znasz z lekcji 4.1:

<!-- example: laps_while -->
```cpp
#include <iostream>

int main() {
    const int total_laps{3};
    int lap{1};

    while (lap <= total_laps) {
        std::cout << "Lap " << lap << "\n";
        lap = lap + 1;
    }

    std::cout << "Finished\n";
}
```

**Przypomnij sobie:** wskaż w nim wartość początkową licznika, warunek, ciało pętli i zmianę licznika. Odpowiedź jest w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

Czy wartość początkową, warunek i zmianę licznika da się zapisać bliżej siebie? Tak:

<!-- example: laps_for -->
```cpp
#include <iostream>

int main() {
    const int total_laps{3};

    for (int lap{1}; lap <= total_laps; ++lap) {
        std::cout << "Lap " << lap << "\n";
    }

    std::cout << "Finished\n";
}
```

**Przewidź**: czy oba programy wypiszą to samo? Potem uruchom oba.

<details>
<summary>Wynik obu programów</summary>

<!-- output: laps_while -->
```text
Lap 1
Lap 2
Lap 3
Finished
```

<!-- output: laps_for -->
```text
Lap 1
Lap 2
Lap 3
Finished
```

Wynik jest identyczny. Oba programy sterują powtarzaniem tak samo, tylko zapisują to inaczej.

</details>

Tym razem programy celowo nie wypisują `lap` po pętli, jak w lekcji 4.1. Dlaczego, zobaczysz w punkcie 7.

## 3. Trzy części nagłówka `for`

<!-- fragment -->
```cpp
for (int lap{1}; lap <= total_laps; ++lap)
```

| Część | W programie | Kiedy się wykonuje |
|---|---|---|
| **Inicjalizacja** | `int lap{1}` | Raz, na początku tej pętli. Tworzy licznik i nadaje mu wartość początkową. **Nie** powtarza się przy kolejnych przebiegach. |
| **Warunek** | `lap <= total_laps` | Przed każdym wykonaniem ciała. Jeśli jest fałszywy, ciało się nie wykonuje, a program idzie dalej za pętlą. |
| **Aktualizacja** | `++lap` | Po każdym wykonaniu ciała, przed kolejnym sprawdzeniem warunku. Tutaj zwiększa licznik o 1. |

- **Średniki** rozdzielają te trzy części nagłówka. To nie są średniki kończące instrukcje w ciele pętli: instrukcje ciała stoją jak zawsze w klamrach, każda z własnym średnikiem.
- **Ciało pętli** to, jak w `while`, instrukcje między `{` a `}`.
- `++lap` stoi w nagłówku **przed** ciałem, ale wykonuje się **po** nim. To najważniejsza różnica między miejscem zapisu a chwilą wykonania.

## 4. Kolejność wykonywania

Pętla `for` z licznikiem wykonuje się w tej kolejności:

1. **Inicjalizacja**, jeden raz.
2. **Sprawdzenie warunku.**
3. Jeśli warunek jest prawdziwy: **wykonanie ciała**.
4. **Aktualizacja.**
5. **Powrót do sprawdzenia warunku**, czyli do kroku 2.

Gdy sprawdzenie warunku da `false`, program przechodzi za pętlę. Tabela przebiegu dla trzech okrążeń:

| Sprawdzenie warunku | `lap` przy sprawdzeniu | `lap <= total_laps` | Ciało pętli | Aktualizacja `++lap` |
|---|---|---|---|---|
| 1 | 1 | `true` | wypisuje `Lap 1` | `lap` staje się 2 |
| 2 | 2 | `true` | wypisuje `Lap 2` | `lap` staje się 3 |
| 3 | 3 | `true` | wypisuje `Lap 3` | `lap` staje się 4 |
| 4 | 4 | `false` | **nie wykonuje się**: pętla się kończy | **nie wykonuje się** |

- Inicjalizacji nie ma w żadnym wierszu: wykonała się raz, **przed** pierwszym sprawdzeniem.
- Czwarte sprawdzenie daje `false`. To nie jest przebieg: ani ciało, ani aktualizacja już się nie wykonują.
- **Porównaj z tabelą z lekcji 4.1.** Wiersze są te same: te same wartości licznika, te same wyniki warunku, te same wypisane linijki. W `while` zmiana licznika była ostatnią instrukcją ciała, a w `for` stoi w nagłówku jako aktualizacja. Mechanizm jest ten sam, inny jest zapis.

**Twoja kolej.** Wypisz po kolei wszystkie kroki tej pętli, gdy `total_laps` wynosi 2: „inicjalizacja: `lap` = 1”, „sprawdzenie: `1 <= 2`, `true`”, „ciało: …” i tak dalej, aż do końca pętli. Ile jest sprawdzeń warunku, a ile aktualizacji? Odpowiedź jest w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 5. Zero, jeden i kilka przebiegów

Teraz liczbę okrążeń podaje użytkownik. Program przyjmuje od 0 do 5 okrążeń. Dla innych liczb wypisuje komunikat i pomija pętlę. Zakładamy, że użytkownik wpisuje liczbę całkowitą.

<!-- example: laps_for_input -->
```cpp
#include <iostream>

int main() {
    int total_laps{0};

    std::cout << "Enter number of laps (0-5):\n";
    std::cin >> total_laps;

    if (total_laps >= 0 && total_laps <= 5) {
        for (int lap{1}; lap <= total_laps; ++lap) {
            std::cout << "Lap " << lap << "\n";
        }

        std::cout << "Finished\n";
    } else {
        std::cout << "Number of laps must be from 0 to 5\n";
    }
}
```

**Przewidź.** Przepisz tabelę i wypełnij ją, zanim uruchomisz program.

| `total_laps` | Liczba przebiegów | Pierwsza wypisana liczba | Ostatnia wypisana liczba |
|---|---|---|---|
| 0 | | | |
| 1 | | | |
| 3 | | | |
| 5 | | | |
| -1 | | | |
| 6 | | | |

Potem uruchom program sześć razy, bez zmiany kodu.

<!-- input: laps_for_input -->
```text
0
```

<details>
<summary>Standardowe wyjście dla 0</summary>

<!-- output: laps_for_input -->
```text
Enter number of laps (0-5):
Finished
```

Inicjalizacja wykonała się (`lap` = 1), ale pierwsze sprawdzenie, `1 <= 0`, dało `false`. Ciało i aktualizacja nie wykonały się ani razu. Pętla `for`, tak jak `while`, może wykonać się zero razy.

</details>

<!-- input: laps_for_input -->
```text
1
```

<details>
<summary>Standardowe wyjście dla 1</summary>

<!-- output: laps_for_input -->
```text
Enter number of laps (0-5):
Lap 1
Finished
```

</details>

<!-- input: laps_for_input -->
```text
3
```

<details>
<summary>Standardowe wyjście dla 3</summary>

<!-- output: laps_for_input -->
```text
Enter number of laps (0-5):
Lap 1
Lap 2
Lap 3
Finished
```

</details>

<!-- input: laps_for_input -->
```text
5
```

<details>
<summary>Standardowe wyjście dla 5</summary>

<!-- output: laps_for_input -->
```text
Enter number of laps (0-5):
Lap 1
Lap 2
Lap 3
Lap 4
Lap 5
Finished
```

</details>

<!-- input: laps_for_input -->
```text
-1
```

<details>
<summary>Standardowe wyjście dla -1</summary>

<!-- output: laps_for_input -->
```text
Enter number of laps (0-5):
Number of laps must be from 0 to 5
```

</details>

<!-- input: laps_for_input -->
```text
6
```

<details>
<summary>Standardowe wyjście dla 6</summary>

<!-- output: laps_for_input -->
```text
Enter number of laps (0-5):
Number of laps must be from 0 to 5
```

</details>

Uzupełnioną tabelę porównaj z częścią [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 6. Zwiększenie o jeden: `++`

W nagłówku `for` licznik zmienia się zapisem `++lap`. Operator `++` zmienia wartość **istniejącej** zmiennej. Dla liczby całkowitej, takiej jak `lap`, zwiększa ją o jeden.

Te trzy zapisy mogą wykonać ten sam prosty krok licznika:

<!-- fragment -->
```cpp
lap = lap + 1;
lap += 1;
++lap;
```

- Gdy chcesz tylko zwiększyć licznik o jeden, wszystkie trzy dają ten sam efekt. W nagłówku `for` najczęściej spotkasz `++lap`.
- `++lap` stosuj jako osobny krok: jako aktualizację w nagłówku albo jako osobną instrukcję, na przykład `++laps_done;`. W tym kursie nie wstawiamy go do dłuższych wyrażeń.
- `+= 1` nadal jest poprawne, także dla liczników zdarzeń z lekcji 4.2. Wybierz zapis, który czyta się najjaśniej.
- Do akumulatora dodajesz jak dotąd odpowiednią wartość: `total += number;`, a nie `++`.

## 7. Gdzie istnieje licznik `for`?

Licznik zadeklarowany w nagłówku `for`, jak `int lap{1}`, istnieje tylko **w tej pętli**: w jej warunku, aktualizacji i ciele. Po pętli już go nie ma.

Ten program ma po pętli wypisać, ile okrążeń wykonano:

<!-- broken: lap_after_for at=8 error=. -->
```cpp
#include <iostream>

int main() {
    for (int lap{1}; lap <= 3; ++lap) {
        std::cout << "Lap " << lap << "\n";
    }

    std::cout << "Laps done: " << lap << "\n";
}
```

1. **Przewidź**, czy ten program się zbuduje.
2. Zbuduj go i przeczytaj komunikat kompilatora.
3. Wskaż deklarację zmiennej `lap`.
4. Wyjaśnij, dlaczego w linijce 8 ta zmienna nie jest dostępna.
5. Zaproponuj poprawkę.

<details>
<summary>Co zgłasza kompilator i dlaczego</summary>

Program się nie zbuduje. Kompilator zgłasza w linijce 8 `use of undeclared identifier 'lap'`: nie zna nazwy `lap`. Ten komunikat znasz z lekcji 3.2. `lap` jest zadeklarowane w nagłówku `for`, więc istnieje tylko w tej pętli. W linijce 8, za zamykającą klamrą pętli, ta deklaracja już nie obowiązuje.

</details>

**Poprawka zależy od wymagania.** Jeśli wartość licznika nie jest potrzebna po pętli, po prostu jej tam nie używaj, tak jak w programach z punktów 2 i 5. Tutaj wymaganie mówi jednak: wypisz po pętli, ile okrążeń wykonano. Taką wartość trzeba przechowywać w zmiennej zadeklarowanej **przed** pętlą, w szerszym zakresie. Pomysł na poprawkę zapisz, zanim zajrzysz do części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 8. Znajdź błąd: runda zero

Wymaganie: program wypisuje rundy ponumerowane **od 1 do podanej liczby rund włącznie**, a na końcu `Done`. Liczba rund musi wynosić od 0 do 5. Ten program buduje się i działa, ale nie spełnia wymagania:

<!-- example: rounds_bug -->
```cpp
#include <iostream>

int main() {
    int round_count{0};

    std::cout << "Enter round count (0-5):\n";
    std::cin >> round_count;

    if (round_count >= 0 && round_count <= 5) {
        for (int round{0}; round <= round_count; ++round) {
            std::cout << "Round " << round << "\n";
        }

        std::cout << "Done\n";
    } else {
        std::cout << "Round count must be from 0 to 5\n";
    }
}
```

1. Przeczytaj wymaganie i ustal, co program **powinien** wypisać dla 0, 1 i 3 rund.
2. Prześledź pętlę dla 0 i dla 1 rundy: od jakiej wartości zaczyna licznik i ile razy warunek daje `true`?
3. Uruchom program dla 0, 1 i 3.
4. Znajdź błąd.
5. Popraw program.
6. Sprawdź ponownie wszystkie trzy przypadki.

Wyniki przed poprawką i poprawiony program są w części [Przykładowe rozwiązania](#przykładowe-rozwiązania). Zajrzyj tam po własnej próbie.

## 9. `for` i akumulator

Pętla `for` może też gromadzić wynik, tak jak `while` w lekcji 4.2:

<!-- example: sum_for -->
```cpp
#include <iostream>

int main() {
    int total{0};

    for (int number{1}; number <= 3; ++number) {
        total += number;
    }

    std::cout << "Total: " << total << "\n";
}
```

**Przewidź** wynik, a potem uruchom program.

<details>
<summary>Wynik programu</summary>

<!-- output: sum_for -->
```text
Total: 6
```

</details>

W tej pętli są **dwie** aktualizacje i każda ma inną rolę:

- `++number` w nagłówku zmienia **licznik**, który steruje powtarzaniem;
- `total += number;` w ciele zmienia **akumulator**, który przechowuje sumę.

Akumulator stoi przed pętlą, bo jego wartość jest potrzebna po niej. Licznik stoi w nagłówku, bo po pętli nie jest potrzebny.

## 10. Misja: plan treningu

Program układa plan prostego ćwiczenia. Użytkownik podaje liczbę rund i liczbę powtórzeń w pierwszej rundzie. W każdej kolejnej rundzie liczba powtórzeń rośnie o 2. Program wypisuje liczbę powtórzeń w każdej rundzie, a na końcu łączną liczbę powtórzeń całego treningu.

**Wymagania:**

- Liczba rund to liczba całkowita od 0 do 5.
- Liczba powtórzeń w pierwszej rundzie to liczba całkowita od 1 do 10.
- Program pyta o obie wartości, w tej kolejności: `Enter round count:` i `Enter starting repetitions:`.
- Dla każdej rundy program wypisuje linijkę `Round K: R repetitions`, a na końcu `Total repetitions: T`.
- Dla 0 rund program nie wypisuje żadnej rundy, a łączna liczba powtórzeń wynosi 0.
- Jeśli którakolwiek wartość jest spoza zakresu, program wypisuje tylko `Invalid training data` i nie wypisuje żadnej rundy. Nie pyta ponownie o dane.
- Zakładamy, że użytkownik wpisuje liczby całkowite.

W `cpp-workspace` utwórz katalog `training_plan`, skopiuj do niego `CMakeLists.txt` z oryginalnego `lesson_05_first_program`, utwórz pusty `main.cpp` i napisz program samodzielnie.

Dla 3 rund i 4 powtórzeń w pierwszej rundzie standardowe wyjście ma być takie:

<!-- input: training_plan -->
```text
3
4
```

<!-- output: training_plan -->
```text
Enter round count:
Enter starting repetitions:
Round 1: 4 repetitions
Round 2: 6 repetitions
Round 3: 8 repetitions
Total repetitions: 18
```

**To nie jest pętla z okrążeń.** Tam był jeden licznik, który rósł o 1 i był wypisywany. Tutaj w każdej rundzie zmieniają się **trzy** wartości o różnych rolach: numer rundy, liczba powtórzeń w bieżącej rundzie i łączna liczba powtórzeń. Każda zmienia się inaczej i w innym momencie. Musisz samodzielnie zdecydować:

1. która zmienna jest licznikiem rund, od jakiej wartości zaczyna, kiedy pętla się kończy i jak licznik się zmienia;
2. gdzie przechowywać liczbę powtórzeń bieżącej rundy i kiedy zwiększać ją o 2;
3. gdzie zadeklarować akumulator łącznej liczby powtórzeń i kiedy dodawać do niego powtórzenia bieżącej rundy;
4. co program robi dla zera rund i jak uniknąć wypisania dodatkowej rundy.

**Zanim napiszesz program**, przygotuj dwie rzeczy:

- tabelę przebiegu dla 3 rund i 4 powtórzeń: numer rundy, powtórzenia wypisane w tej rundzie i suma po tej rundzie;
- tabelę przypadków testowych: zero rund, jedna runda, kilka rund, największa dopuszczalna liczba rund, oba końce zakresu powtórzeń i wartości tuż poza zakresem obu danych. Przy każdym przypadku zapisz oczekiwane standardowe wyjście.

### Kryterium sukcesu

- Program buduje się jako C++20, a jego standardowe wyjście dla 3 rund i 4 powtórzeń jest dokładnie takie jak powyżej.
- Dla każdej poprawnej pary danych program wypisuje dokładnie tyle rund, ile podano, z poprawną liczbą powtórzeń, i poprawną sumę. Dla danych spoza zakresu wypisuje tylko `Invalid training data`.
- Rundami steruje pętla `for` z klamrami, a jej licznik zmienia się przez `++`.
- Łączna liczba powtórzeń jest gromadzona w akumulatorze przez `+=`.
- Zakres obu wartości jest sprawdzany, zanim program zacznie wypisywać rundy.
- Tabela przebiegu i tabela przypadków powstały przed uruchomieniem programu.
- Umiesz wyjaśnić, dlaczego pętla się kończy i dlaczego dla zera rund suma wynosi 0.

Gdy wynik się zgadza, możesz zapisać projekt w Gicie, jak w lekcji 1.5.

<details>
<summary>Podpowiedź 1</summary>

Wypisz wartości, które zmieniają się z rundy na rundę, i przy każdej zapisz, o ile się zmienia. Które z nich steruje tym, ile razy pętla się wykona, a które tylko jest wypisywane albo sumowane?

</details>

<details>
<summary>Podpowiedź 2</summary>

W jednej rundzie dzieją się trzy rzeczy: wypisanie danych rundy, dodanie jej powtórzeń do sumy i przygotowanie liczby powtórzeń dla następnej rundy. W jakiej kolejności muszą nastąpić, żeby pierwsza runda pokazała liczbę podaną przez użytkownika?

</details>

<details>
<summary>Podpowiedź 3</summary>

Nagłówek `for` odpowiada na trzy pytania: od jakiego numeru zaczyna się pierwsza runda, dopóki co pętla ma trwać i jak przejść do numeru następnej rundy. Sprawdź swój warunek dla 1 rundy w tabeli przebiegu.

</details>

<details>
<summary>Pełna lista przypadków kontrolnych: otwórz po przygotowaniu własnej tabeli</summary>

| Rundy | Start | Wypisane powtórzenia | Suma | Co sprawdza |
|---|---|---|---|---|
| 3 | 4 | 4, 6, 8 | 18 | kilka przebiegów |
| 0 | 4 | brak rund | 0 | zero przebiegów |
| 1 | 4 | 4 | 4 | jeden przebieg |
| 5 | 1 | 1, 3, 5, 7, 9 | 25 | największa liczba rund, najmniejszy start |
| 2 | 10 | 10, 12 | 22 | największy start |
| -1 | 4 | — | — | liczba rund tuż pod zakresem |
| 6 | 4 | — | — | liczba rund tuż nad zakresem |
| 3 | 0 | — | — | start tuż pod zakresem |
| 3 | 11 | — | — | start tuż nad zakresem |

Przypadki z kreskami kończą się linijką `Invalid training data`. Przypadek 3 i 4 jest sprawdzony wyżej, przy treści misji.

<!-- input: training_plan -->
```text
0
4
```

<!-- output: training_plan -->
```text
Enter round count:
Enter starting repetitions:
Total repetitions: 0
```

<!-- input: training_plan -->
```text
1
4
```

<!-- output: training_plan -->
```text
Enter round count:
Enter starting repetitions:
Round 1: 4 repetitions
Total repetitions: 4
```

<!-- input: training_plan -->
```text
5
1
```

<!-- output: training_plan -->
```text
Enter round count:
Enter starting repetitions:
Round 1: 1 repetitions
Round 2: 3 repetitions
Round 3: 5 repetitions
Round 4: 7 repetitions
Round 5: 9 repetitions
Total repetitions: 25
```

<!-- input: training_plan -->
```text
2
10
```

<!-- output: training_plan -->
```text
Enter round count:
Enter starting repetitions:
Round 1: 10 repetitions
Round 2: 12 repetitions
Total repetitions: 22
```

<!-- input: training_plan -->
```text
-1
4
```

<!-- output: training_plan -->
```text
Enter round count:
Enter starting repetitions:
Invalid training data
```

<!-- input: training_plan -->
```text
6
4
```

<!-- output: training_plan -->
```text
Enter round count:
Enter starting repetitions:
Invalid training data
```

<!-- input: training_plan -->
```text
3
0
```

<!-- output: training_plan -->
```text
Enter round count:
Enter starting repetitions:
Invalid training data
```

<!-- input: training_plan -->
```text
3
11
```

<!-- output: training_plan -->
```text
Enter round count:
Enter starting repetitions:
Invalid training data
```

</details>

Przykładowe rozwiązanie jest w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 11. `while` czy `for`?

Obie pętle potrafią wykonać wiele tych samych zadań: każdą pętlę z tej lekcji da się zapisać przez `while`, a pętle z lekcji 4.1 i 4.2 przez `for`. Żadna nie jest zawsze lepsza.

- **`while`** czyta się naturalnie jako: „powtarzaj, **dopóki** ten warunek jest prawdziwy”.
- **`for`** jest często wygodny, gdy powtarzaniem steruje **licznik** z wartością początkową, warunkiem i aktualizacją. Wszystkie trzy widać wtedy w jednej linijce, a licznik nie istnieje dłużej, niż jest potrzebny.

Ta lekcja pokazuje podstawowy wzorzec `for` z licznikiem. W lekcji 4.4 zobaczysz pętlę, w której nie ma takiego licznika, a powtarzanie trwa, dopóki nie zostanie osiągnięty cel.

## 12. Gdy coś pójdzie inaczej

| Co widzisz | Co to znaczy | Co zrobić |
|---|---|---|
| Pojawia się runda albo okrążenie numer 0 | Licznik zaczyna od 0, a wymaganie mówi „od 1”. | Sprawdź inicjalizację w nagłówku. Wartość początkowa zależy od wymagania (punkt 8). |
| Jeden przebieg za dużo albo za mało | Warunek i wartość początkowa do siebie nie pasują, na przykład `<` zamiast `<=`. | Prześledź pętlę dla jednego przebiegu i dla największej wartości. |
| `use of undeclared identifier` dla licznika po pętli | Licznik zadeklarowany w nagłówku `for` istnieje tylko w pętli (punkt 7). | Jeśli wartość jest potrzebna po pętli, przechowuj ją w zmiennej zadeklarowanej przed pętlą. |
| Błąd kompilacji w nagłówku `for` | Brakuje średnika między częściami albo stoi przecinek zamiast średnika. | Nagłówek ma trzy części rozdzielone dwoma średnikami: inicjalizacja; warunek; aktualizacja. |
| Pierwsza runda nie pokazuje liczby podanej przez użytkownika | Liczba powtórzeń rośnie przed wypisaniem. | Ustal kolejność w ciele: najpierw dane bieżącej rundy, potem przygotowanie następnej. |
| Suma powtórzeń jest za mała albo za duża | Akumulator jest zerowany w ciele pętli, dodawany w złym momencie albo dodaje się licznik zamiast powtórzeń. | Wypełnij tabelę przebiegu: suma po każdej rundzie musi być sumą wypisanych powtórzeń. |
| Ta sama linijka pojawia się bez końca | Licznik się nie zmienia albo zmienia się w złą stronę. | Przerwij program, jak w lekcji 4.1, i sprawdź aktualizację w nagłówku. |

## 13. Wyjaśnij

Odpowiedz krótko, najlepiej na piśmie. Dopiero potem porównaj z przykładową odpowiedzią.

**1.** Ile razy wykonuje się inicjalizacja w nagłówku `for`?

<details>
<summary>Przykładowa odpowiedź</summary>

Raz, na początku pętli, przed pierwszym sprawdzeniem warunku.

</details>

**2.** Kiedy sprawdzany jest warunek, a kiedy wykonywana jest aktualizacja?

<details>
<summary>Przykładowa odpowiedź</summary>

Warunek: przed każdym wykonaniem ciała. Aktualizacja: po każdym wykonaniu ciała, tuż przed kolejnym sprawdzeniem warunku.

</details>

**3.** Czy ciało pętli `for` może wykonać się zero razy?

<details>
<summary>Przykładowa odpowiedź</summary>

Tak. Jeśli pierwsze sprawdzenie warunku da `false`, jak `1 <= 0`, ciało i aktualizacja nie wykonają się ani razu.

</details>

**4.** Co robi `++counter`?

<details>
<summary>Przykładowa odpowiedź</summary>

Zwiększa wartość istniejącej zmiennej całkowitej `counter` o jeden. Jako osobny krok daje ten sam efekt co `counter = counter + 1;` i `counter += 1;`.

</details>

**5.** Do czego służą średniki w nagłówku `for`?

<details>
<summary>Przykładowa odpowiedź</summary>

Rozdzielają trzy części nagłówka: inicjalizację, warunek i aktualizację.

</details>

**6.** Dlaczego licznik zadeklarowany w nagłówku nie jest dostępny po pętli?

<details>
<summary>Przykładowa odpowiedź</summary>

Bo istnieje tylko w tej pętli, jak zmienna zadeklarowana w bloku (lekcja 3.2). Za pętlą jego deklaracja już nie obowiązuje.

</details>

**7.** Kiedy `for` jest czytelniejszy niż `while`?

<details>
<summary>Przykładowa odpowiedź</summary>

Często wtedy, gdy powtarzaniem steruje licznik z wartością początkową, warunkiem i aktualizacją. W `for` wszystkie trzy stoją w jednej linijce. Gdy myślimy raczej „powtarzaj, dopóki coś jest prawdą”, naturalniejszy bywa `while`.

</details>

**8.** Dlaczego w misji potrzebujesz i licznika rund, i akumulatora?

<details>
<summary>Przykładowa odpowiedź</summary>

Bo pełnią różne role. Licznik rund decyduje, ile razy pętla się wykona, i daje numer rundy. Akumulator gromadzi łączną liczbę powtórzeń. Do sumy trafiają powtórzenia rundy, a nie numer rundy.

</details>

**9.** Co się stanie, jeśli w misji zwiększysz liczbę powtórzeń o 2 **przed** wypisaniem danych rundy?

<details>
<summary>Przykładowa odpowiedź</summary>

Pierwsza runda pokaże liczbę o 2 większą od podanej, każda następna też będzie przesunięta, a suma będzie za duża, jeśli dodajesz po zwiększeniu. Dla 3 rund i 4 powtórzeń program wypisałby 6, 8, 10 zamiast 4, 6, 8.

</details>

## Podsumowanie

- `for (inicjalizacja; warunek; aktualizacja) { … }` zbiera w jednej linijce trzy części sterujące pętlą z licznikiem.
- **Inicjalizacja** wykonuje się raz, na początku. **Warunek** jest sprawdzany przed każdym przebiegiem. **Aktualizacja** wykonuje się po każdym przebiegu, przed kolejnym sprawdzeniem.
- Ostatnie sprawdzenie warunku daje `false` i nie jest przebiegiem. Ciało może wykonać się zero razy.
- `++counter` zwiększa licznik całkowity o jeden. `counter += 1` i `counter = counter + 1` nadal są poprawne.
- Licznik zadeklarowany w nagłówku `for` istnieje tylko w tej pętli. Wartość potrzebną po pętli przechowuj w zmiennej zadeklarowanej przed nią.
- Wartość początkowa licznika wynika z wymagania. Błąd o jeden krok najszybciej ujawnia przypadek z zerem albo jednym przebiegiem.
- `for` i `while` potrafią wykonać te same zadania. `for` jest często wygodny, gdy powtarzaniem steruje licznik.

## Co dalej

W tej lekcji liczba przebiegów była znana, zanim pętla się zaczęła. W lekcji 4.4 program będzie powtarzał działanie, **dopóki nie osiągnie celu**, na przykład oszczędzał, aż uzbiera potrzebną kwotę, a liczby przebiegów nie poznasz z góry. **Lekcja 4.4 jest w przygotowaniu.**

---

## Przykładowe rozwiązania

Zajrzyj tutaj **po własnej próbie**. Twoje nazwy mogą się różnić, jeśli standardowe wyjście jest takie, jak wymagane.

<details>
<summary>Punkt 2: cztery części pętli while</summary>

- **Wartość początkowa:** `int lap{1};`, przed pętlą.
- **Warunek:** `lap <= total_laps`, w `while ( … )`.
- **Ciało:** instrukcje między `{` a `}`, tu wypisanie `Lap …` i zmiana licznika.
- **Zmiana licznika:** `lap = lap + 1;`, ostatnia instrukcja ciała.

W `for` wartość początkowa i zmiana licznika przenoszą się do nagłówka, obok warunku.

</details>

<details>
<summary>Punkt 4: wszystkie kroki dla dwóch okrążeń</summary>

1. Inicjalizacja: `lap` = 1.
2. Sprawdzenie: `1 <= 2`, `true`.
3. Ciało: wypisuje `Lap 1`.
4. Aktualizacja: `++lap`, `lap` = 2.
5. Sprawdzenie: `2 <= 2`, `true`.
6. Ciało: wypisuje `Lap 2`.
7. Aktualizacja: `++lap`, `lap` = 3.
8. Sprawdzenie: `3 <= 2`, `false`: pętla się kończy, program wypisuje `Finished`.

Trzy sprawdzenia warunku, dwa przebiegi ciała, dwie aktualizacje i jedna inicjalizacja.

</details>

<details>
<summary>Punkt 5: tabela przewidywań</summary>

| `total_laps` | Liczba przebiegów | Pierwsza wypisana liczba | Ostatnia wypisana liczba |
|---|---|---|---|
| 0 | 0 | — | — |
| 1 | 1 | 1 | 1 |
| 3 | 3 | 1 | 3 |
| 5 | 5 | 1 | 5 |
| -1 | 0 (pętla pominięta przez `else`) | — | — |
| 6 | 0 (pętla pominięta przez `else`) | — | — |

Dla 0 pętla jest wykonywana, ale jej ciało nie: warunek jest fałszywy od początku. Dla -1 i 6 program w ogóle nie dochodzi do pętli.

</details>

<details>
<summary>Punkt 7: poprawka dla licznika po pętli</summary>

Wymaganie mówi: wypisz po pętli, ile okrążeń wykonano. Ta wartość musi istnieć po pętli, więc stoi w zmiennej zadeklarowanej przed nią. Pętla zwiększa ją o jeden w każdym przebiegu:

<!-- example: laps_done_after_for -->
```cpp
#include <iostream>

int main() {
    int laps_done{0};

    for (int lap{1}; lap <= 3; ++lap) {
        std::cout << "Lap " << lap << "\n";
        ++laps_done;
    }

    std::cout << "Laps done: " << laps_done << "\n";
}
```

<!-- output: laps_done_after_for -->
```text
Lap 1
Lap 2
Lap 3
Laps done: 3
```

Zauważ: nawet gdyby `lap` istniało po pętli, miałoby wartość 4, a nie 3. Tak było w lekcji 4.1, gdzie program wypisywał `lap is now 4`. Liczba wykonanych okrążeń to inna wartość niż licznik po zakończeniu pętli, dlatego ma własną zmienną.

</details>

<details>
<summary>Punkt 8: wyniki przed poprawką i poprawiony program</summary>

Przed poprawką, dla 0, 1 i 3:

<!-- input: rounds_bug -->
```text
0
```

<!-- output: rounds_bug -->
```text
Enter round count (0-5):
Round 0
Done
```

<!-- input: rounds_bug -->
```text
1
```

<!-- output: rounds_bug -->
```text
Enter round count (0-5):
Round 0
Round 1
Done
```

<!-- input: rounds_bug -->
```text
3
```

<!-- output: rounds_bug -->
```text
Enter round count (0-5):
Round 0
Round 1
Round 2
Round 3
Done
```

- **Błąd widać już dla 0:** wymaganie nie dopuszcza żadnej rundy, a program wypisuje `Round 0`. Każdy przypadek ma o jeden przebieg za dużo, a numeracja zaczyna się od 0.
- **Przyczyna:** licznik zaczyna od 0, a warunek `round <= round_count` dopuszcza też ostatni numer. Od 0 do 3 włącznie są cztery numery, nie trzy.
- **Poprawka:** wymaganie mówi „od 1 do liczby rund włącznie”, więc licznik zaczyna od 1:

<!-- example: rounds_fixed -->
```cpp
#include <iostream>

int main() {
    int round_count{0};

    std::cout << "Enter round count (0-5):\n";
    std::cin >> round_count;

    if (round_count >= 0 && round_count <= 5) {
        for (int round{1}; round <= round_count; ++round) {
            std::cout << "Round " << round << "\n";
        }

        std::cout << "Done\n";
    } else {
        std::cout << "Round count must be from 0 to 5\n";
    }
}
```

<!-- input: rounds_fixed -->
```text
0
```

<!-- output: rounds_fixed -->
```text
Enter round count (0-5):
Done
```

<!-- input: rounds_fixed -->
```text
1
```

<!-- output: rounds_fixed -->
```text
Enter round count (0-5):
Round 1
Done
```

<!-- input: rounds_fixed -->
```text
3
```

<!-- output: rounds_fixed -->
```text
Enter round count (0-5):
Round 1
Round 2
Round 3
Done
```

Zmiana samego warunku na `round < round_count` dałaby właściwą **liczbę** przebiegów, ale numery od 0 do 2. To nie spełnia wymagania. Pętla zaczynająca od 0 nie jest błędna sama w sobie: poprawna wartość początkowa zależy od tego, co program ma wypisać.

</details>

<details>
<summary>Punkt 10: misja, plan treningu</summary>

<!-- example: training_plan -->
```cpp
#include <iostream>

int main() {
    int round_count{0};
    int start_repetitions{0};

    std::cout << "Enter round count:\n";
    std::cin >> round_count;
    std::cout << "Enter starting repetitions:\n";
    std::cin >> start_repetitions;

    const bool rounds_ok{round_count >= 0 && round_count <= 5};
    const bool start_ok{start_repetitions >= 1 && start_repetitions <= 10};

    if (rounds_ok && start_ok) {
        int repetitions{start_repetitions};
        int total_repetitions{0};

        for (int round{1}; round <= round_count; ++round) {
            std::cout << "Round " << round << ": " << repetitions << " repetitions\n";
            total_repetitions += repetitions;
            repetitions += 2;
        }

        std::cout << "Total repetitions: " << total_repetitions << "\n";
    } else {
        std::cout << "Invalid training data\n";
    }
}
```

| Sprawdzenie warunku | `round` | `round <= 3` | Wypisane powtórzenia | `total_repetitions` po rundzie | `repetitions` dla następnej rundy |
|---|---|---|---|---|---|
| 1 | 1 | `true` | 4 | 4 | 6 |
| 2 | 2 | `true` | 6 | 10 | 8 |
| 3 | 3 | `true` | 8 | 18 | 10 |
| 4 | 4 | `false` | — | — | — |

- **Trzy wartości, trzy role:** `round` steruje pętlą i daje numer rundy (`++round`), `repetitions` to powtórzenia bieżącej rundy (rośnie o 2), a `total_repetitions` to akumulator (`+=`).
- **Kolejność w ciele:** najpierw wypisanie i dodanie do sumy, potem `repetitions += 2;`. Dzięki temu pierwsza runda pokazuje liczbę podaną przez użytkownika, a do sumy trafiają te same liczby, które program wypisał.
- **Zero rund:** warunek `1 <= 0` jest fałszywy od razu, więc żadna runda się nie pojawia, a `total_repetitions` zostaje równe 0.
- Po ostatniej rundzie `repetitions` ma już wartość dla rundy, która się nie odbędzie (10). To nie szkodzi, bo tej wartości program nie wypisuje.

</details>

**Poprzednia lekcja:** [Lekcja 4.2: Sumowanie i akumulatory](lesson_02_sums_and_accumulators.md) · **Następna lekcja:** w przygotowaniu · [Opis kursu](../../README.md)

# Lekcja 4.7: Program powtarza działania (sprawdzian Modułu 4)

**Polski** · [English](lesson_07_the_program_repeats.en.md) · [Opis kursu](../../README.md)

> **Moduł 4, lekcja 7: sprawdzian** · około 100–120 minut, można go podzielić na dwa podejścia
> **Potrzebujesz:** katalogu `cpp-workspace` i oryginalnego projektu `lesson_05_first_program`.
> **Wersja pilotażowa.** Rozwiązania referencyjne z tej lekcji sprawdzamy automatycznie na Windowsie, Ubuntu i macOS, z podanymi danymi wejściowymi. Twojej pracy nic nie ocenia automatycznie: sprawdzasz ją samodzielnie, według kryteriów.

## Jak przebiega ten sprawdzian

Ta lekcja nie wprowadza niczego nowego. Sprawdzasz, czy potrafisz samodzielnie zaprojektować program, który wielokrotnie odczytuje dane, stopniowo buduje wynik i poprawnie kończy działanie: po zebraniu wszystkich danych, ale także wtedy, gdy dane skończą się wcześniej. Do tego poprawiasz dwa krótkie programy z błędami, analizujesz bez uruchamiania trzeci i wyjaśniasz swoje decyzje.

Lekcja ma dwie części:

- **Część A: sprawdzian.** Wymagania, dane testowe, oczekiwane wyniki, zadania, pytania i kryteria. Bez podpowiedzi i bez kodu rozwiązań. Wszystko, czego potrzebujesz, znasz z Modułów 1–4.
- **Część B: sprawdzenie i omówienie.** Podpowiedzi, pełne listy przypadków kontrolnych, przykładowe rozwiązania, wyjaśnienia i samoocena. Przejdź do niej po wykonaniu części A albo wtedy, gdy świadomie zrezygnujesz z dalszej samodzielnej próby.

Zajrzenie do części B, do wcześniejszych lekcji albo do notatek nie jest porażką. Ważne jest, żeby **uczciwie zanotować, co zrobiono samodzielnie, a co z pomocą**. Proponowany podział na dwa podejścia:

- **pierwsze:** projekt, napisanie i podstawowe testy programu z zadania 1;
- **drugie:** zadania 2 i 3, przypadki graniczne, porównanie z rozwiązaniem, pytania i samoocena.

**Możesz używać:** CLiona albo terminala, CMake i Ninja, jak dotąd; `CMakeLists.txt` skopiowanego z oryginalnego `lesson_05_first_program`; tabel przebiegu i przypadków oraz tymczasowych instrukcji `std::cout`. Debugger nie jest potrzebny. Nie musisz kończyć danych z klawiatury: programy sprawdzamy na danych, które same się kończą.

---

# Część A: sprawdzian

## Zadanie 1: Stacja pomiarowa

Prosta stacja zapisuje temperatury. Najpierw użytkownik podaje, ile pomiarów trzeba zebrać. Potem program odczytuje kolejne temperatury w stopniach Celsjusza. Po zebraniu wymaganej liczby **poprawnych** pomiarów wypisuje raport: liczbę pomiarów, średnią temperaturę i liczbę pomiarów poniżej zera.

**Przygotowanie:** w `cpp-workspace` utwórz katalog `measurement_station`, skopiuj do niego `CMakeLists.txt` z oryginalnego `lesson_05_first_program`, utwórz **pusty** `main.cpp` i napisz cały program samodzielnie.

**Liczba pomiarów:**

- Program pyta `Enter measurement count (1-24):` i odczytuje liczbę całkowitą. Dopuszczalne są wartości od 1 do 24 włącznie.
- Dla liczby spoza zakresu wypisuje `Measurement count out of range` i pyta ponownie.
- Po błędnie zapisanej liczbie wypisuje `Invalid integer input, try again`, odzyskuje wejście, jak w lekcji 4.6, i pyta ponownie.
- Jeśli dane się skończą, zanim liczba pomiarów zostanie ustalona, wypisuje tylko `Input ended` i kończy pracę.
- Do pomiarów przechodzi dopiero wtedy, gdy liczba pomiarów jest ustalona.

**Temperatury:**

- Dla każdej próby program pyta `Enter temperature:` i odczytuje liczbę z częścią ułamkową.
- W tym zadaniu dopuszczalne są temperatury od -20 do 40 stopni włącznie. To wymaganie scenariusza, a nie zakres typu `double` ani wszystkich temperatur na świecie.
- Dla temperatury spoza zakresu wypisuje `Temperature out of range` i pyta ponownie.
- Po błędnie zapisanej liczbie wypisuje `Invalid temperature input, try again`, odzyskuje wejście i pyta ponownie.
- Odrzucona temperatura i błędny wpis nie zmieniają sumy, liczby zebranych pomiarów ani liczby pomiarów poniżej zera.
- Temperatura dokładnie 0 **nie jest** temperaturą poniżej zera.

**Zakończenie:**

- Po zebraniu wszystkich wymaganych pomiarów program nie pyta już o temperaturę i wypisuje trzy linijki: `Measurements recorded: N`, `Average temperature: X` i `Below freezing: N`.
- Jeśli dane skończą się wcześniej, wypisuje tylko `Input ended: N of M measurements recorded`, czyli ile poprawnych pomiarów zebrał i ile było wymaganych. Nie liczy wtedy średniej. To świadoma reguła tego programu: raport dotyczy pełnego zestawu.
- Po końcu danych program nie próbuje czytać dalej. Kończy się normalnie.
- Średnią wypisuje domyślnie, przez `std::cout`, bez dodatkowego formatowania.

Program nie musi zapamiętywać wszystkich temperatur. Nie jest też odporny na dowolne dane: na przykład `12abc` zostanie odczytane jako 12, jak w lekcji 4.6.

**Pierwszy przykład:** liczba pomiarów 4, temperatury -2, 0, 1 i 5:

<!-- input: measurement_station -->
```text
4
-2
0
1
5
```

<!-- output: measurement_station -->
```text
Enter measurement count (1-24):
Enter temperature:
Enter temperature:
Enter temperature:
Enter temperature:
Measurements recorded: 4
Average temperature: 1
Below freezing: 1
```

**Drugi przykład:** błędny tekst i temperatura spoza zakresu, przy danych `2`, `abc`, `50`, `-2`, `4`:

<!-- input: measurement_station -->
```text
2
abc
50
-2
4
```

<!-- output: measurement_station -->
```text
Enter measurement count (1-24):
Enter temperature:
Invalid temperature input, try again
Enter temperature:
Temperature out of range
Enter temperature:
Enter temperature:
Measurements recorded: 2
Average temperature: 1
Below freezing: 1
```

**Trzeci przykład:** dane kończą się po dwóch z trzech pomiarów, przy danych `3`, `-2`, `2`:

<!-- input: measurement_station -->
```text
3
-2
2
```

<!-- output: measurement_station -->
```text
Enter measurement count (1-24):
Enter temperature:
Enter temperature:
Enter temperature:
Input ended: 2 of 3 measurements recorded
```

**Zanim napiszesz program**, przygotuj tabelę przypadków testowych. Musi sprawdzać co najmniej:

- jeden pomiar ujemny i jeden dodatni, kilka pomiarów ze średnią całkowitą i ze średnią z połówką, temperaturę dokładnie 0, -20 i 40 oraz największą liczbę pomiarów;
- liczby pomiarów 0 i 25, błędny tekst zamiast liczby pomiarów, także kilka razy;
- temperatury -21 i 41, błędny tekst zamiast temperatury oraz poprawny pomiar po odzyskaniu wejścia;
- koniec danych: przed liczbą pomiarów, po liczbie spoza zakresu, po błędnym tekście, zaraz po poprawnej liczbie pomiarów, po części temperatur, po odrzuconej temperaturze i po błędnym tekście w fazie pomiarów.

Przy każdym przypadku zapisz oczekiwane standardowe wyjście, łącznie z liczbą pytań. Dobierz temperatury tak, żeby średnią łatwo było policzyć w pamięci: liczby całkowite i połówki.

Gdy wynik się zgadza, możesz zapisać projekt w Gicie, jak w lekcji 1.5. Przed commitem sprawdź `git status`: do historii trafiają tylko `main.cpp` i `CMakeLists.txt`.

## Zadanie 2: Dwa zgłoszenia

W `cpp-workspace` utwórz katalog `diagnosis_4`, skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program`. Każdy z poniższych programów wpisz po kolei w `main.cpp` tego katalogu. Oba się budują, kończą działanie i dają złe wyniki.

**Zgłoszenie A.** Rozgrzewka składa się z kilku kroków. Program ma wypisać kroki **od 1 do podanej liczby kroków włącznie**, każdy jako `Step K of N`, a na końcu `Warm-up done`. Liczba kroków to od 0 do 5.

<!-- example: warmup_bug -->
```cpp
#include <iostream>

int main() {
    int step_count{0};

    std::cout << "Enter warm-up steps (0-5):\n";
    std::cin >> step_count;

    if (step_count >= 0 && step_count <= 5) {
        for (int step{0}; step <= step_count; ++step) {
            std::cout << "Step " << step << " of " << step_count << "\n";
        }

        std::cout << "Warm-up done\n";
    } else {
        std::cout << "Steps must be from 0 to 5\n";
    }
}
```

**Zgłoszenie B.** W małym kinie są rzędy foteli. W rzędzie numer `r` jest `10 + r` foteli: w pierwszym 11, w drugim 12 i tak dalej. Program ma wypisać łączną liczbę foteli dla podanej liczby rzędów, od 0 do 10.

<!-- example: cinema_bug -->
```cpp
#include <iostream>

int main() {
    int row_count{0};

    std::cout << "Enter number of rows (0-10):\n";
    std::cin >> row_count;

    if (row_count >= 0 && row_count <= 10) {
        int total_seats{0};

        for (int row{1}; row <= row_count; ++row) {
            total_seats = 0;
            total_seats += 10 + row;
        }

        std::cout << "Total seats: " << total_seats << "\n";
    } else {
        std::cout << "Rows must be from 0 to 10\n";
    }
}
```

**Dla każdego zgłoszenia:**

1. Przeczytaj wymaganie i zapisz poprawny wynik dla 0, 1 i 3.
2. **Przewidź**, co wypisze błędny program dla tych trzech przypadków. Pomoże Ci tabela przebiegu.
3. Uruchom program i porównaj.
4. Znajdź błąd.
5. Popraw program jedną zmianą.
6. Sprawdź ponownie zero, jeden i trzy przebiegi.

Zapisz wyniki w tabeli:

| Zgłoszenie | Przypadek, który ujawnia błąd | Rzeczywisty wynik | Przyczyna | Poprawka | Sprawdzenie |
|---|---|---|---|---|---|
| A | | | | | |
| B | | | | | |

Projektu `diagnosis_4` nie musisz zapisywać w Gicie.

## Zadanie 3: Analiza bez uruchamiania

Ten fragment ma zebrać 3 odczyty z zakresu od 0 do 100. Po nieudanym odczycie odzyskuje wejście, jak w lekcji 4.6. **Przeanalizuj go na papierze, nie uruchamiaj go:**

<!-- fragment -->
```cpp
int accepted{0};
int reading{0};

while (accepted < 3) {
    std::cout << "Enter reading:\n";
    std::cin >> reading;

    if (!std::cin.fail()) {
        if (reading >= 0 && reading <= 100) {
            ++accepted;
        } else {
            std::cout << "Reading out of range\n";
        }
    } else {
        std::cin.clear();
        std::string discarded_line{""};
        std::getline(std::cin, discarded_line);
        std::cout << "Invalid input, try again\n";
    }
}
```

Dane to tylko jedna linijka, `5`, po której dane się kończą.

1. Wypełnij tabelę stanu dla pierwszych czterech prób: odczytana wartość, `fail()`, `eof()`, działanie programu i `accepted` po próbie.
2. Dlaczego od drugiej próby strumień nie może dostarczyć następnej wartości?
3. Co oznacza wtedy `fail()` i czy `clear()` coś tu pomoże?
4. Jakiej przyczyny zakończenia brakuje tej pętli?
5. Jak ją uwzględnić, bez nowych konstrukcji?
6. Dlaczego limit czasu w automatycznych testach nie jest rozwiązaniem?

## Zadanie 4: Wyjaśnij

Odpowiedz krótko, na piśmie, odwołując się do własnego programu z zadania 1:

1. Dlaczego każda pętla musi mieć sposób na zakończenie? Wskaż, co kończy obie pętle Twojego programu.
2. Co decyduje o liczbie przebiegów podczas zbierania pomiarów?
3. Dlaczego odrzucone wartości nie zwiększają licznika pomiarów?
4. Jaką rolę pełni akumulator w Twoim programie?
5. Kiedy zwiększasz licznik temperatur poniżej zera i dlaczego 0 się do nich nie zalicza?
6. Dlaczego średnią obliczasz dopiero po zebraniu pełnego zestawu? Czy w Twoim programie może dojść do dzielenia przez zero?
7. Dlaczego po błędnym tekście potrzebne są i `clear()`, i odrzucenie reszty linijki?
8. Dlaczego program nie może ponawiać pytania bez końca po końcu danych?
9. Kiedy wygodniej zastosować `for`, a kiedy `while`? Którą pętlę wybrano w zadaniu 1, a którą w zgłoszeniu B, i dlaczego?
10. Dlaczego test z jedną iteracją nie wykrył błędu w zgłoszeniu B?
11. Dlaczego poprawny wynik dla jednego zestawu danych nie wystarcza, żeby uznać program za poprawny?

## Kryteria sukcesu

Sprawdzian jest zaliczony, gdy spełniasz **wszystkie** kryteria. Możesz przy tym korzystać z części B, jeśli uczciwie zaznaczysz to w samoocenie.

- `measurement_station/main.cpp` napisano od pustego pliku, w poprawnym C++20. Program buduje się bez błędów.
- Liczba pomiarów jest ustalana w pętli, która ponawia pytanie po wartości spoza zakresu i po błędnym tekście, a kończy się po poprawnej wartości albo po końcu danych.
- Temperatury są zbierane w pętli, która kończy się po zebraniu wymaganej liczby poprawnych pomiarów albo po końcu danych. Nie ma pytania po zebraniu ostatniego pomiaru.
- Po każdym odczycie program najpierw sprawdza, czy odczyt się udał, potem koniec danych, a dopiero na końcu odzyskuje wejście przez `std::cin.clear()` i `std::getline`. Uwzględnia też koniec danych podczas odrzucania linijki.
- Licznik pomiarów, suma i licznik pomiarów poniżej zera zmieniają się tylko po przyjęciu poprawnej temperatury. Temperatura 0 nie jest poniżej zera.
- Średnia jest obliczana tylko z pełnego zestawu, więc nie ma dzielenia przez zero.
- Standardowe wyjście dla trzech przykładów i dla wszystkich Twoich przypadków jest zgodne z wymaganiami.
- Tabela przypadków powstała przed uruchomieniem programu i sprawdza granice z zadania 1.
- Oba zgłoszenia z zadania 2 zdiagnozowano i poprawiono, a zero, jeden i trzy przebiegi sprawdzono ponownie.
- Zadanie 3 przeanalizowano bez uruchamiania i wskazano brakującą przyczynę zakończenia.
- Umiesz wyjaśnić każdą linijkę swojego programu i odpowiedzieć na pytania z zadania 4.

Nazwy zmiennych i układ programu mogą być inne niż w rozwiązaniu referencyjnym, jeśli są czytelne. Dwie kolejne pętle `while` to dobre rozwiązanie. Nie trzeba używać `for` w zadaniu 1, pętli zagnieżdżonych ani własnych funkcji. Poprawny wynik to warunek konieczny, ale **nie dowód zrozumienia**. Dlatego zadania 3 i 4 są częścią sprawdzianu.

---

# Część B: sprawdzenie i omówienie

Przejdź tutaj po wykonaniu części A albo wtedy, gdy świadomie zrezygnujesz z dalszej samodzielnej próby.

## Jak sprawdzić swoją pracę

- **Standardowe wyjście:** uruchom program dla każdego przypadku z tabeli i porównaj linijki programu z oczekiwanymi, znak po znaku, łącznie z liczbą pytań. Pomiń wpisane dane widoczne dzięki echu.
- **Ten sam program:** między uruchomieniami nie zmieniaj kodu.
- **Pełne listy przypadków kontrolnych** poniżej porównaj ze swoją tabelą. Czy Twoja tabela obejmowała te same granice i te same sytuacje końca danych?
- **Kolejność:** przejrzyj obie pętle. Czy po nieudanym odczycie najpierw sprawdzasz koniec danych? Czy suma i liczniki zmieniają się tylko w jednym miejscu?

## Podpowiedzi

Rozwijaj je po kolei i tylko wtedy, gdy ich potrzebujesz.

<details>
<summary>Zadanie 1, podpowiedź 1: jakie zmienne?</summary>

Wypisz, co program musi pamiętać: wymaganą liczbę pomiarów, liczbę już przyjętych, sumę temperatur i liczbę temperatur poniżej zera, a do tego informację, czy dane się skończyły. Która z tych wartości steruje drugą pętlą (lekcja 4.4), a która jest akumulatorem (lekcja 4.2)?

</details>

<details>
<summary>Zadanie 1, podpowiedź 2: dwie fazy</summary>

Program ma dwie fazy, jedna po drugiej: najpierw ustala liczbę pomiarów, potem zbiera temperatury. Każda faza to osobna pętla `while` z tymi samymi trzema sytuacjami po odczycie: odczyt udany, koniec danych albo błędny tekst (lekcja 4.6). Druga faza ma sens tylko wtedy, gdy pierwsza zakończyła się ustaloną liczbą.

</details>

<details>
<summary>Zadanie 1, podpowiedź 3: koniec i raport</summary>

Po drugiej pętli są trzy możliwe sytuacje: liczba pomiarów nie została ustalona, zebrano wszystkie pomiary albo dane skończyły się w trakcie. Która zmienna pozwala je odróżnić? Średnią licz tylko w jednej z nich.

</details>

<details>
<summary>Zadanie 2, zgłoszenie A</summary>

Od jakiego numeru zaczyna się pierwszy wypisany krok i ile razy warunek daje `true` dla 0 kroków? Porównaj to z lekcją 4.3.

</details>

<details>
<summary>Zadanie 2, zgłoszenie B</summary>

Prześledź sumę po każdym przebiegu dla 3 rzędów. Która linijka sprawia, że suma nie rośnie z rzędu na rząd? Porównaj to z lekcją 4.2.

</details>

<details>
<summary>Zadanie 3</summary>

Po końcu danych odczyt się nie udaje. Która gałąź się wtedy wykonuje i czy cokolwiek w niej może zakończyć pętlę? Porównaj to z flagą `input_ended` z lekcji 4.6.

</details>

## Pełna lista przypadków kontrolnych: zadanie 1

<details>
<summary>Otwórz po przygotowaniu własnej tabeli</summary>

Pierwsze trzy przypadki są sprawdzone w części A.

| Dane | Wynik | Co sprawdza |
|---|---|---|
| `4`, `-2`, `0`, `1`, `5` | 4 pomiary, średnia 1, poniżej zera 1 | średnia całkowita, temperatura 0 |
| `2`, `abc`, `50`, `-2`, `4` | 2 pomiary, średnia 1, poniżej zera 1 | błędny tekst i temperatura spoza zakresu |
| `3`, `-2`, `2`, koniec | 2 z 3 | koniec danych po części temperatur |
| `1`, `-5` | 1 pomiar, średnia -5, poniżej zera 1 | jeden pomiar ujemny |
| `1`, `7` | 1 pomiar, średnia 7, poniżej zera 0 | jeden pomiar dodatni |
| `2`, `1.5`, `2.5` | średnia 2 | temperatury z częścią ułamkową |
| `2`, `0`, `1` | średnia 0.5, poniżej zera 0 | średnia z połówką, 0 nie jest poniżej zera |
| `4`, `1`, `2`, `3`, `4` | średnia 2.5 | średnia z połówką |
| `3`, `-2`, `-1`, `0` | średnia -1, poniżej zera 2 | średnia ujemna |
| `2`, `-20`, `40` | średnia 10, poniżej zera 1 | obie granice temperatury |
| `24`, potem 12 par `-1`, `2` | 24 pomiary, średnia 0.5, poniżej zera 12 | największa liczba pomiarów |
| `0`, `2`, `3`, `5` | 2 pomiary, średnia 4 | liczba pomiarów 0 |
| `25`, `1`, `-3` | 1 pomiar, średnia -3 | liczba pomiarów 25 |
| `abc`, `1`, `6` | 1 pomiar, średnia 6 | tekst zamiast liczby pomiarów |
| `abc`, `xyz`, `0`, `1`, `2` | 1 pomiar, średnia 2 | kilka błędnych prób liczby pomiarów |
| `1`, `-21`, `3` | 1 pomiar, średnia 3 | temperatura -21 |
| `1`, `41`, `warm`, `0` | 1 pomiar, średnia 0 | temperatura 41, tekst, pomiar po odzyskaniu |
| brak danych | `Input ended` | koniec danych przed liczbą pomiarów |
| `30`, koniec | `Input ended` | koniec danych po liczbie spoza zakresu |
| `many`, koniec | `Input ended` | koniec danych po błędnym tekście |
| `2`, koniec | 0 z 2 | koniec danych zaraz po liczbie pomiarów |
| `2`, `45`, koniec | 0 z 2 | koniec danych po odrzuconej temperaturze |
| `2`, `1`, `abc`, koniec | 1 z 2 | koniec danych po błędnym tekście w fazie pomiarów |

<!-- input: measurement_station -->
```text
1
-5
```

<!-- output: measurement_station -->
```text
Enter measurement count (1-24):
Enter temperature:
Measurements recorded: 1
Average temperature: -5
Below freezing: 1
```

<!-- input: measurement_station -->
```text
1
7
```

<!-- output: measurement_station -->
```text
Enter measurement count (1-24):
Enter temperature:
Measurements recorded: 1
Average temperature: 7
Below freezing: 0
```

<!-- input: measurement_station -->
```text
2
1.5
2.5
```

<!-- output: measurement_station -->
```text
Enter measurement count (1-24):
Enter temperature:
Enter temperature:
Measurements recorded: 2
Average temperature: 2
Below freezing: 0
```

<!-- input: measurement_station -->
```text
2
0
1
```

<!-- output: measurement_station -->
```text
Enter measurement count (1-24):
Enter temperature:
Enter temperature:
Measurements recorded: 2
Average temperature: 0.5
Below freezing: 0
```

<!-- input: measurement_station -->
```text
4
1
2
3
4
```

<!-- output: measurement_station -->
```text
Enter measurement count (1-24):
Enter temperature:
Enter temperature:
Enter temperature:
Enter temperature:
Measurements recorded: 4
Average temperature: 2.5
Below freezing: 0
```

<!-- input: measurement_station -->
```text
3
-2
-1
0
```

<!-- output: measurement_station -->
```text
Enter measurement count (1-24):
Enter temperature:
Enter temperature:
Enter temperature:
Measurements recorded: 3
Average temperature: -1
Below freezing: 2
```

<!-- input: measurement_station -->
```text
2
-20
40
```

<!-- output: measurement_station -->
```text
Enter measurement count (1-24):
Enter temperature:
Enter temperature:
Measurements recorded: 2
Average temperature: 10
Below freezing: 1
```

<!-- input: measurement_station -->
```text
24
-1
2
-1
2
-1
2
-1
2
-1
2
-1
2
-1
2
-1
2
-1
2
-1
2
-1
2
-1
2
```

<!-- output: measurement_station -->
```text
Enter measurement count (1-24):
Enter temperature:
Enter temperature:
Enter temperature:
Enter temperature:
Enter temperature:
Enter temperature:
Enter temperature:
Enter temperature:
Enter temperature:
Enter temperature:
Enter temperature:
Enter temperature:
Enter temperature:
Enter temperature:
Enter temperature:
Enter temperature:
Enter temperature:
Enter temperature:
Enter temperature:
Enter temperature:
Enter temperature:
Enter temperature:
Enter temperature:
Enter temperature:
Measurements recorded: 24
Average temperature: 0.5
Below freezing: 12
```

<!-- input: measurement_station -->
```text
0
2
3
5
```

<!-- output: measurement_station -->
```text
Enter measurement count (1-24):
Measurement count out of range
Enter measurement count (1-24):
Enter temperature:
Enter temperature:
Measurements recorded: 2
Average temperature: 4
Below freezing: 0
```

<!-- input: measurement_station -->
```text
25
1
-3
```

<!-- output: measurement_station -->
```text
Enter measurement count (1-24):
Measurement count out of range
Enter measurement count (1-24):
Enter temperature:
Measurements recorded: 1
Average temperature: -3
Below freezing: 1
```

<!-- input: measurement_station -->
```text
abc
1
6
```

<!-- output: measurement_station -->
```text
Enter measurement count (1-24):
Invalid integer input, try again
Enter measurement count (1-24):
Enter temperature:
Measurements recorded: 1
Average temperature: 6
Below freezing: 0
```

<!-- input: measurement_station -->
```text
abc
xyz
0
1
2
```

<!-- output: measurement_station -->
```text
Enter measurement count (1-24):
Invalid integer input, try again
Enter measurement count (1-24):
Invalid integer input, try again
Enter measurement count (1-24):
Measurement count out of range
Enter measurement count (1-24):
Enter temperature:
Measurements recorded: 1
Average temperature: 2
Below freezing: 0
```

<!-- input: measurement_station -->
```text
1
-21
3
```

<!-- output: measurement_station -->
```text
Enter measurement count (1-24):
Enter temperature:
Temperature out of range
Enter temperature:
Measurements recorded: 1
Average temperature: 3
Below freezing: 0
```

<!-- input: measurement_station -->
```text
1
41
warm
0
```

<!-- output: measurement_station -->
```text
Enter measurement count (1-24):
Enter temperature:
Temperature out of range
Enter temperature:
Invalid temperature input, try again
Enter temperature:
Measurements recorded: 1
Average temperature: 0
Below freezing: 0
```

<!-- input: measurement_station -->
```text
```

<!-- output: measurement_station -->
```text
Enter measurement count (1-24):
Input ended
```

<!-- input: measurement_station -->
```text
30
```

<!-- output: measurement_station -->
```text
Enter measurement count (1-24):
Measurement count out of range
Enter measurement count (1-24):
Input ended
```

<!-- input: measurement_station -->
```text
many
```

<!-- output: measurement_station -->
```text
Enter measurement count (1-24):
Invalid integer input, try again
Enter measurement count (1-24):
Input ended
```

<!-- input: measurement_station -->
```text
2
```

<!-- output: measurement_station -->
```text
Enter measurement count (1-24):
Enter temperature:
Input ended: 0 of 2 measurements recorded
```

<!-- input: measurement_station -->
```text
2
45
```

<!-- output: measurement_station -->
```text
Enter measurement count (1-24):
Enter temperature:
Temperature out of range
Enter temperature:
Input ended: 0 of 2 measurements recorded
```

<!-- input: measurement_station -->
```text
2
1
abc
```

<!-- output: measurement_station -->
```text
Enter measurement count (1-24):
Enter temperature:
Enter temperature:
Invalid temperature input, try again
Enter temperature:
Input ended: 1 of 2 measurements recorded
```

</details>

## Przykładowe rozwiązania

<details>
<summary>Zadanie 1: stacja pomiarowa</summary>

<!-- example: measurement_station -->
```cpp
#include <iostream>
#include <string>

int main() {
    int required_count{0};
    bool count_accepted{false};
    bool input_ended{false};

    while (!count_accepted && !input_ended) {
        std::cout << "Enter measurement count (1-24):\n";
        std::cin >> required_count;

        if (!std::cin.fail()) {
            if (required_count >= 1 && required_count <= 24) {
                count_accepted = true;
            } else {
                std::cout << "Measurement count out of range\n";
            }
        } else if (std::cin.eof()) {
            input_ended = true;
        } else {
            std::cin.clear();
            std::string discarded_line{""};
            std::getline(std::cin, discarded_line);

            if (std::cin.fail() || std::cin.eof()) {
                input_ended = true;
            } else {
                std::cout << "Invalid integer input, try again\n";
            }
        }
    }

    int recorded{0};
    int below_freezing{0};
    double total{0.0};
    double temperature{0.0};

    while (count_accepted && recorded < required_count && !input_ended) {
        std::cout << "Enter temperature:\n";
        std::cin >> temperature;

        if (!std::cin.fail()) {
            if (temperature >= -20.0 && temperature <= 40.0) {
                ++recorded;
                total += temperature;

                if (temperature < 0.0) {
                    ++below_freezing;
                }
            } else {
                std::cout << "Temperature out of range\n";
            }
        } else if (std::cin.eof()) {
            input_ended = true;
        } else {
            std::cin.clear();
            std::string discarded_line{""};
            std::getline(std::cin, discarded_line);

            if (std::cin.fail() || std::cin.eof()) {
                input_ended = true;
            } else {
                std::cout << "Invalid temperature input, try again\n";
            }
        }
    }

    if (!count_accepted) {
        std::cout << "Input ended\n";
    } else if (recorded == required_count) {
        std::cout << "Measurements recorded: " << recorded << "\n";
        std::cout << "Average temperature: " << total / recorded << "\n";
        std::cout << "Below freezing: " << below_freezing << "\n";
    } else {
        std::cout << "Input ended: " << recorded << " of " << required_count << " measurements recorded\n";
    }
}
```

- **Dwie fazy, dwie pętle `while`.** Pierwsza kończy się po ustaleniu liczby pomiarów (`count_accepted`) albo po końcu danych (`input_ended`). Druga działa tylko po ustaleniu liczby i kończy się po zebraniu wszystkich pomiarów albo po końcu danych. Żadna pętla nie jest zagnieżdżona w drugiej.
- **Trzy wartości zmieniają się w jednym miejscu:** po przyjęciu poprawnej temperatury. `++recorded` liczy przyjęte pomiary, `total += temperature` jest akumulatorem, a `++below_freezing` wykonuje się tylko dla temperatury mniejszej od zera, więc 0 się nie liczy.
- **O liczbie przebiegów drugiej pętli decyduje postęp,** czyli liczba **przyjętych** pomiarów, a nie liczba prób. Błędne dane dodają próby, ale nie postęp. Dlatego to `while`, a nie `for`.
- **Kolejność po odczycie** jest taka sama w obu fazach: udany odczyt, potem koniec danych, potem odzyskiwanie i sprawdzenie końca danych po odrzuceniu linijki (lekcja 4.6). Fragment odzyskiwania powtarza się dwa razy. Na tym etapie kursu to w porządku.
- **Średnia** powstaje tylko wtedy, gdy `recorded == required_count`. Wymagana liczba to co najmniej 1, więc dzielenie przez zero nie jest możliwe. `total` jest typu `double`, więc `total / recorded` też daje `double`.
- **Wyniki:** dla `4`, `-2`, `0`, `1`, `5` suma wynosi 4, a średnia 4 / 4 = 1. Tylko -2 jest poniżej zera. Dla `2`, `abc`, `50`, `-2`, `4` przyjęte są tylko -2 i 4: suma 2, średnia 1. Ani `abc`, ani 50 nie są pomiarami.
- **Precyzja:** temperatury w testach to liczby całkowite i połówki, więc sumy i średnie są dokładne, a `std::cout` wypisuje je tak, jak je zapisujemy (1, 0.5, 2.5, -1). Nie każda możliwa średnia typu `double` wypisuje się tak prosto, ale te testy sprawdzają logikę programu, a nie zaokrąglenia.

</details>

<details>
<summary>Zadanie 2, zgłoszenie A: wynik przed poprawką i poprawiony program</summary>

Przed poprawką:

<!-- input: warmup_bug -->
```text
0
```

<!-- output: warmup_bug -->
```text
Enter warm-up steps (0-5):
Step 0 of 0
Warm-up done
```

<!-- input: warmup_bug -->
```text
1
```

<!-- output: warmup_bug -->
```text
Enter warm-up steps (0-5):
Step 0 of 1
Step 1 of 1
Warm-up done
```

<!-- input: warmup_bug -->
```text
3
```

<!-- output: warmup_bug -->
```text
Enter warm-up steps (0-5):
Step 0 of 3
Step 1 of 3
Step 2 of 3
Step 3 of 3
Warm-up done
```

- **Błąd widać już dla 0 kroków:** program wypisuje `Step 0 of 0`, choć nie powinien wypisać żadnego kroku. Każdy przypadek ma o jeden przebieg za dużo.
- **Przyczyna:** licznik zaczyna od 0, a warunek `<=` dopuszcza też ostatni numer.
- **Poprawka:** licznik zaczyna od 1, bo wymaganie mówi „od 1”:

<!-- example: warmup_fixed -->
```cpp
#include <iostream>

int main() {
    int step_count{0};

    std::cout << "Enter warm-up steps (0-5):\n";
    std::cin >> step_count;

    if (step_count >= 0 && step_count <= 5) {
        for (int step{1}; step <= step_count; ++step) {
            std::cout << "Step " << step << " of " << step_count << "\n";
        }

        std::cout << "Warm-up done\n";
    } else {
        std::cout << "Steps must be from 0 to 5\n";
    }
}
```

<!-- input: warmup_fixed -->
```text
0
```

<!-- output: warmup_fixed -->
```text
Enter warm-up steps (0-5):
Warm-up done
```

<!-- input: warmup_fixed -->
```text
1
```

<!-- output: warmup_fixed -->
```text
Enter warm-up steps (0-5):
Step 1 of 1
Warm-up done
```

<!-- input: warmup_fixed -->
```text
3
```

<!-- output: warmup_fixed -->
```text
Enter warm-up steps (0-5):
Step 1 of 3
Step 2 of 3
Step 3 of 3
Warm-up done
```

</details>

<details>
<summary>Zadanie 2, zgłoszenie B: wynik przed poprawką i poprawiony program</summary>

Przed poprawką:

<!-- input: cinema_bug -->
```text
0
```

<!-- output: cinema_bug -->
```text
Enter number of rows (0-10):
Total seats: 0
```

<!-- input: cinema_bug -->
```text
1
```

<!-- output: cinema_bug -->
```text
Enter number of rows (0-10):
Total seats: 11
```

<!-- input: cinema_bug -->
```text
3
```

<!-- output: cinema_bug -->
```text
Enter number of rows (0-10):
Total seats: 13
```

| Rząd | Fotele w rzędzie | `total_seats` po `total_seats = 0;` | `total_seats` po dodaniu |
|---|---|---|---|
| 1 | 11 | 0 | 11 |
| 2 | 12 | 0 | 12 |
| 3 | 13 | 0 | 13 |

- **Dla 0 i 1 rzędu wynik jest poprawny,** bo nie ma czego zgubić. Dopiero 3 rzędy ujawniają błąd: wynik to 13, czyli tylko ostatni rząd, zamiast 11 + 12 + 13 = 36.
- **Przyczyna:** `total_seats = 0;` w ciele pętli kasuje sumę w każdym przebiegu.
- **Poprawka:** usuń tę linijkę. Wartość początkową 0 suma dostaje raz, przed pętlą:

<!-- example: cinema_fixed -->
```cpp
#include <iostream>

int main() {
    int row_count{0};

    std::cout << "Enter number of rows (0-10):\n";
    std::cin >> row_count;

    if (row_count >= 0 && row_count <= 10) {
        int total_seats{0};

        for (int row{1}; row <= row_count; ++row) {
            total_seats += 10 + row;
        }

        std::cout << "Total seats: " << total_seats << "\n";
    } else {
        std::cout << "Rows must be from 0 to 10\n";
    }
}
```

<!-- input: cinema_fixed -->
```text
0
```

<!-- output: cinema_fixed -->
```text
Enter number of rows (0-10):
Total seats: 0
```

<!-- input: cinema_fixed -->
```text
1
```

<!-- output: cinema_fixed -->
```text
Enter number of rows (0-10):
Total seats: 11
```

<!-- input: cinema_fixed -->
```text
3
```

<!-- output: cinema_fixed -->
```text
Enter number of rows (0-10):
Total seats: 36
```

</details>

<details>
<summary>Zadanie 3: pętla bez wyjścia po końcu danych</summary>

| Próba | Odczytana wartość | `fail()` | `eof()` | Działanie | `accepted` |
|---|---|---|---|---|---|
| 1 | 5 | `false` | `false` | w zakresie: `++accepted` | 1 |
| 2 | brak: dane się skończyły | `true` | `true` | `clear()`, `getline` też się nie udaje, komunikat | 1 |
| 3 | brak | `true` | `true` | to samo | 1 |
| 4 | brak | `true` | `true` | to samo, i tak bez końca | 1 |

1. Tabela jest powyżej. Pętla pyta i wypisuje `Invalid input, try again` bez końca.
2. **Dane się skończyły:** po linijce `5` nie ma już niczego, co dałoby się odczytać, a nowe dane nie pojawią się same.
3. **`fail()` oznacza nieudany odczyt,** tu z powodu końca danych. `clear()` zdejmuje tylko znacznik błędu. Nie tworzy danych, więc następny odczyt znowu się nie udaje, a `getline` też niczego nie odrzuca.
4. **Brakuje końca danych jako przyczyny zakończenia.** Pętla kończy się tylko po trzech przyjętych odczytach, a tych nigdy nie będzie.
5. **Jak w lekcji 4.6:** po nieudanym odczycie najpierw sprawdzić `std::cin.eof()` i ustawić flagę, na przykład `input_ended`, a po odrzuceniu linijki sprawdzić koniec danych jeszcze raz. Warunek pętli to wtedy `accepted < 3 && !input_ended`.
6. **Limit czasu w testach tylko wykrywa,** że program się nie kończy. Poprawny program kończy się sam, na podstawie własnego warunku. Poza testami limitu czasu w ogóle nie ma, a program pytałby bez końca.

</details>

## Przykładowe odpowiedzi do zadania 4

<details>
<summary>Pokaż przykładowe odpowiedzi</summary>

1. Bez sposobu na zakończenie program pytałby albo liczył bez końca. Pierwszą pętlę kończy ustalenie liczby pomiarów albo koniec danych, a drugą zebranie wszystkich pomiarów albo koniec danych.
2. Liczba **przyjętych** pomiarów w porównaniu z wymaganą liczbą. Błędne i odrzucone dane dodają próby, ale nie zbliżają do końca.
3. Bo licznik mówi, ile jest poprawnych pomiarów do raportu i do średniej. Odrzucona wartość nie jest pomiarem.
4. Gromadzi sumę przyjętych temperatur, z której na końcu powstaje średnia.
5. Tylko po przyjęciu poprawnej temperatury mniejszej od zera. 0 nie jest mniejsze od zera, więc warunek `temperature < 0.0` daje dla niego `false`.
6. Bo raport dotyczy pełnego zestawu, a przy niepełnym program wypisuje tylko, ile pomiarów zebrał. Średnia powstaje, gdy zebrano wymaganą liczbę pomiarów, czyli co najmniej 1, więc dzielenia przez zero nie ma.
7. Bo są dwie przeszkody: `clear()` zdejmuje stan błędu, a odrzucenie linijki zabiera błędne znaki z wejścia. Bez któregokolwiek następny odczyt znowu się nie uda.
8. Bo po końcu danych nic już nie przyjdzie. Kolejne pytania pozostałyby bez odpowiedzi, a pętla trwałaby bez końca.
9. `for` jest wygodny, gdy licznik z wartością początkową, warunkiem i aktualizacją steruje powtarzaniem, jak w zgłoszeniu B, gdzie jest jeden przebieg na rząd. `while` jest naturalny, gdy powtarzanie trwa, dopóki coś jest prawdą, jak w zadaniu 1, gdzie liczba prób zależy od tego, ile danych trzeba odrzucić.
10. Bo przy jednym przebiegu zerowanie sumy nie ma czego skasować: 0 + 11 to poprawny wynik. Błąd widać dopiero przy kilku przebiegach.
11. Bo jeden zestaw sprawdza tylko jedną drogę przez program. Błędy o jeden krok, zerowanie akumulatora albo brak wyjścia po końcu danych ujawniają się dopiero przy zerze, jednym albo wielu przebiegach i przy danych, które kończą się wcześniej.

</details>

## Samoocena

Przy każdym kryterium zaznacz jedną odpowiedź:

| Kryterium | Samodzielnie | Z podpowiedzią | Po zajrzeniu do rozwiązania | Do powtórki |
|---|---|---|---|---|
| Napisanie programu od pustego `main.cpp` | | | | |
| Ponawianie pytania o liczbę pomiarów | | | | |
| Odzyskiwanie wejścia po błędnym tekście | | | | |
| Zakończenie obu faz po końcu danych | | | | |
| Liczenie wyłącznie poprawnych pomiarów | | | | |
| Suma, średnia i pomiary poniżej zera | | | | |
| Brak pytania po ostatnim pomiarze | | | | |
| Tabela przypadków z granicami i końcem danych | | | | |
| Zgłoszenie A (błąd o jeden krok w `for`) | | | | |
| Zgłoszenie B (zerowanie akumulatora) | | | | |
| Zadanie 3 (pętla bez wyjścia po końcu danych) | | | | |
| Wyjaśnienia z zadania 4 | | | | |

Jeśli w kolumnie „Do powtórki” jest coś zaznaczone, wróć do odpowiedniej lekcji:

| Temat | Lekcja |
|---|---|
| `while`, zero przebiegów, tabela przebiegu | 4.1 |
| akumulator i `+=` | 4.2 |
| `for` i `++` | 4.3 |
| pętla do osiągnięcia celu, postęp | 4.4 |
| ponawianie pytania i `std::cin.fail()` | 4.5 |
| `clear()`, `std::getline`, `eof()` | 4.6 |
| porównania, `&&` i `\|\|` | 3.1–3.4 |
| `double` i odczyt danych | 2.5–2.6 |

Potem spróbuj zadania jeszcze raz, na przykład z innym zakresem temperatur.

---

## Podsumowanie Modułu 4

Po siedmiu lekcjach potrafisz:

- powtarzać działania pętlą `while` i przewidywać jej przebieg w tabeli, także dla zera przebiegów;
- pisać pętle sterowane licznikiem, także w zwięzłej postaci `for`, z prefiksowym `++`;
- pisać pętle sterowane postępem w stronę celu i wyjaśniać, dlaczego się kończą;
- gromadzić wynik w akumulatorach przez `+=` i odróżniać liczniki przebiegów i zdarzeń od sum;
- znajdować błędy o jeden krok, zerowanie akumulatora i pętle bez postępu;
- ponawiać pytanie po wartości niespełniającej wymagań;
- odróżniać wartość niedopuszczalną od nieudanego odczytu i od końca danych;
- przywracać strumień do działania przez `clear()` i odrzucać resztę błędnej linijki przez `std::getline`;
- kończyć program bezpiecznie, gdy dane się skończą;
- testować pętle dla zera, jednego i wielu przebiegów.

Twoje programy nie sprawdzają jeszcze całych linijek tekstu i nie przechowują wielu wartości naraz. Każdy program to też jedna funkcja `main`. To przyjdzie w dalszych modułach.

## Co dalej

Kolejne moduły pozwolą organizować większe programy i pracować z bardziej złożonymi danymi. Moduł 5 jest w przygotowaniu.

**Poprzednia lekcja:** [Lekcja 4.6: Błędny odczyt, odzyskiwanie strumienia i koniec danych](lesson_06_recover_and_end_of_input.md) · **Następna lekcja:** w przygotowaniu · [Opis kursu](../../README.md)

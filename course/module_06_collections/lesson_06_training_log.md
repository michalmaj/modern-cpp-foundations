# Lekcja 6.6: Dziennik treningów (sprawdzian Modułu 6)

**Polski** · [English](lesson_06_training_log.en.md) · [Opis kursu](../../README.md)

> **Moduł 6, lekcja 6: sprawdzian** · około 95–115 minut, w dwóch podejściach
> **Potrzebujesz:** katalogu `cpp-workspace` i oryginalnego projektu `lesson_05_first_program`.
> **Wersja pilotażowa.** Rozwiązania referencyjne z tej lekcji sprawdzamy automatycznie na Windowsie, Ubuntu i macOS, z podanymi danymi wejściowymi. Twojej pracy nic nie ocenia automatycznie: sprawdzasz ją samodzielnie, według kryteriów.

## Jak przebiega ten sprawdzian

Ta lekcja nie wprowadza niczego nowego. Sprawdzasz, czy potrafisz samodzielnie zaprojektować program, który **zbiera dane do wektora, kilka razy je analizuje** i korzysta ze współpracujących funkcji, żeby przygotować raport. Do tego poprawiasz dwa krótkie programy z błędami i wyjaśniasz swoje decyzje.

Lekcja ma dwie części:

- **Część A: sprawdzian.** Wymagania, przykłady, zadania, pytania i kryteria. Bez podpowiedzi i bez kodu rozwiązań. Wszystko, czego potrzebujesz, znasz z Modułów 1–6.
- **Część B: sprawdzenie i omówienie.** Podpowiedzi, pełna lista przypadków kontrolnych, rozwiązanie referencyjne, poprawki, odpowiedzi i samoocena. Przejdź do niej po wykonaniu części A albo wtedy, gdy świadomie zrezygnujesz z dalszej samodzielnej próby.

Zajrzenie do części B, do wcześniejszych lekcji albo do notatek nie jest porażką. Ważne jest, żeby **uczciwie zanotować, co zrobiono samodzielnie, a co z pomocą**. Proponowany podział na dwa podejścia:

- **pierwsze:** zaprojektowanie funkcji, napisanie programu z zadania 1, sprawdzenie funkcji osobno i podstawowe przypadki raportu;
- **drugie:** przypadki graniczne, zadanie 2, porównanie z rozwiązaniem, zadanie 3 i samoocena.

**Możesz używać:** CLiona albo terminala, CMake i Ninja, jak dotąd; `CMakeLists.txt` skopiowanego z oryginalnego `lesson_05_first_program`; tabel przebiegu i przypadków oraz tymczasowych wydruków testowych. Debugger nie jest potrzebny. Nie musisz kończyć danych z klawiatury: przypadki, w których dane kończą się wcześniej, analizujesz na papierze.

---

# Część A: sprawdzian

## Zadanie 1: Dziennik treningów

Program analizuje czas treningu w kolejnych dniach. Użytkownik podaje liczbę dni, a potem liczbę minut treningu w każdym dniu. Program **przechowuje wszystkie pomiary** i odpowiada na trzy pytania:

- Jaki był średni czas treningu?
- Które zapisane wartości były większe od średniej?
- Ile razy wynik dnia był lepszy niż dnia poprzedniego?

**Przygotowanie:** w `cpp-workspace` utwórz katalog `training_log`, skopiuj do niego `CMakeLists.txt` z oryginalnego `lesson_05_first_program`, utwórz **pusty** `main.cpp` i napisz cały program samodzielnie.

### Dane wejściowe

- Program pyta `Enter training day count (1-7):` i odczytuje liczbę dni, liczbę całkowitą.
- Jeśli odczyt się nie uda, wypisuje `Input could not be read` i kończy pracę. Jeśli liczba jest spoza zakresu od 1 do 7, wypisuje `Invalid day count` i kończy pracę.
- Dla każdego dnia, od 1 do podanej liczby, pyta `Enter minutes for day N (0-30):` i odczytuje liczbę minut, liczbę całkowitą. Poprawne są wartości od 0 do 30 włącznie, także 0.
- Jeśli odczyt minut się nie uda, na przykład po tekście albo gdy dane skończą się wcześniej, program wypisuje `Input could not be read` i kończy pracę. Jeśli liczba minut jest spoza zakresu, wypisuje `Invalid training data` i kończy pracę.
- Po błędzie program nie pyta o kolejne dni, nie zapisuje błędnej wartości i nie wypisuje żadnej części raportu. Wcześniej wypisane pytania zostają. **Inaczej niż w lekcji 6.2:** wartość spoza zakresu nie jest pomijana, tylko kończy program.

### Raport

Dopiero po poprawnym odczytaniu wszystkich dni program wypisuje:

- `Recorded days: N`: liczbę zapisanych dni;
- `Average training minutes: X`: średnią liczbę minut, z częścią ułamkową, jeśli taka wychodzi;
- `Days above average: N`: liczbę zapisanych wartości **ściśle większych** od średniej;
- `Above-average minutes:` i po spacji te wartości, w kolejności dni, rozdzielone spacjami, z powtórzeniami, bez spacji na końcu linijki, albo `Above-average minutes: none`, gdy takich wartości nie ma;
- `Improved days: N`: liczbę dni, w których wynik był **większy** niż dnia poprzedniego. Pierwszy dzień nie ma poprzednika. Równy wynik to nie poprawa.

Program nie wypisuje żadnych innych komunikatów.

### Funkcje

Program ma co najmniej trzy własne funkcje obliczeniowe:

1. funkcję obliczającą średnią zapisanych pomiarów;
2. funkcję tworzącą **nowy wektor** wartości większych od podanego progu;
3. funkcję liczącą dni z poprawą względem poprzedniego dnia.

**Wymagania wobec funkcji:**

- Wektory dostają przez `const std::vector<int>&`. Funkcja tworząca nowy wektor zwraca go przez wartość.
- Nie odczytują wejścia, nie wypisują raportu i nie zmieniają przekazanych danych.
- Nazwy, pozostałe parametry, typy wyników i kolejność wywołań wybierasz samodzielnie. Funkcje nie muszą wywoływać siebie nawzajem: mogą współpracować przez `main`, który przekazuje wynik jednej funkcji do drugiej.
- **Funkcja średniej dostaje tylko niepusty wektor.** Średnia pustego zbioru w naszym modelu nie istnieje, więc nie wymyślaj dla niej sztucznego wyniku. Zapisz to wymaganie w komentarzu przy funkcji. Pilnuje go `main`: liczy średnią dopiero po odczytaniu od 1 do 7 poprawnych dni.

`main` odczytuje dane, sprawdza je, zapisuje poprawne wartości w wektorze, wywołuje funkcje i wypisuje raport. Algorytmów obliczeniowych nie powtarza. Nie używaj zmiennych zadeklarowanych poza funkcjami.

### Przykłady

**Przykład A:** pięć dni, 10, 14, 8, 18 i 10 minut.

<!-- input: training_log -->
```text
5
10
14
8
18
10
```

<!-- output: training_log -->
```text
Enter training day count (1-7):
Enter minutes for day 1 (0-30):
Enter minutes for day 2 (0-30):
Enter minutes for day 3 (0-30):
Enter minutes for day 4 (0-30):
Enter minutes for day 5 (0-30):
Recorded days: 5
Average training minutes: 12
Days above average: 2
Above-average minutes: 14 18
Improved days: 2
```

Suma minut to 60, więc średnia wynosi 12. Powyżej średniej są 14 i 18. Poprawa była dwa razy: z 10 na 14 i z 8 na 18.

**Przykład B:** jeden dzień, 7 minut.

<!-- input: training_log -->
```text
1
7
```

<!-- output: training_log -->
```text
Enter training day count (1-7):
Enter minutes for day 1 (0-30):
Recorded days: 1
Average training minutes: 7
Days above average: 0
Above-average minutes: none
Improved days: 0
```

Jeden dzień wystarcza do policzenia średniej. Jedyny wynik jest jej równy, więc nie jest większy od średniej. Jeden dzień nie tworzy pary, więc poprawy nie ma.

**Przykład C:** trzy dni, 5, 7 i 9 minut. **Przewidź** cały raport, zanim napiszesz program.

<!-- input: training_log -->
```text
3
5
7
9
```

<details>
<summary>Standardowe wyjście dla przykładu C</summary>

<!-- output: training_log -->
```text
Enter training day count (1-7):
Enter minutes for day 1 (0-30):
Enter minutes for day 2 (0-30):
Enter minutes for day 3 (0-30):
Recorded days: 3
Average training minutes: 7
Days above average: 1
Above-average minutes: 9
Improved days: 2
```

Średnia to 7, a wartość 7 jest jej równa, więc w nowym wektorze jest tylko 9.

</details>

### Jak pracować

1. **Zaprojektuj funkcje, zanim zaczniesz pisać `main`.** Przy każdej zapisz jednym zdaniem jej zadanie, parametry i typ wyniku.
2. **Przygotuj tabelę przypadków:** jeden dzień, siedem dni, same równe wartości, średnia z częścią ułamkową, wartość równa średniej, powtórzone wartości powyżej średniej, brak poprawy, poprawa tylko w ostatniej parze, równe sąsiednie dni, granice 0 i 30, liczby dni 0 i 8, minuty -1 i 31, tekst zamiast liczby oraz dane, które kończą się wcześniej. Przy każdym zapisz oczekiwany raport albo komunikat.
3. **Sprawdź każdą funkcję osobno** wydrukami testowymi, z wektorami wpisanymi w kodzie:
   - średnią dla jednego pomiaru, kilku równych wartości i zestawu ze średnią ułamkową, **nigdy dla pustego wektora**;
   - nowy wektor dla braku wyników, jednego i kilku wyników, wartości dokładnie równej progowi i pustego wejścia;
   - poprawy dla pustego wektora, jednego elementu, dwóch rosnących, dwóch malejących i dwóch równych wartości oraz dłuższego zestawu z poprawą dopiero na końcu.
4. **Usuń wydruki testowe** i złóż raport.
5. **Uruchom cały program** dla przykładów A, B i C oraz dla 2–3 innych przypadków z tabeli. Wszystkie przypadki z pełnej listy kontrolnej są sprawdzone automatycznie, więc nie musisz wpisywać ich wszystkich. Przypadki z danymi, które kończą się wcześniej, przeanalizuj na papierze.

Gdy wynik się zgadza, możesz zapisać projekt w Gicie, jak w lekcji 1.5. Przed commitem sprawdź `git status`: do historii trafiają tylko `main.cpp` i `CMakeLists.txt`.

## Zadanie 2: Dwa zgłoszenia

Wykonaj to zadanie **po zadaniu 1**: oba programy zawierają funkcje podobne do tych, które projektujesz. Każdy program sprawdza jedną funkcję dwoma testami wpisanymi w kodzie, tak jak wydruki testowe z zadania 1. W `cpp-workspace` utwórz katalog `diagnosis_6`, skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program` i wpisuj programy po kolei w `main.cpp`.

<details>
<summary>Zgłoszenie A: wartość równa średniej</summary>

Wymaganie: nowy wektor zawiera wartości **ściśle większe** od średniej.

<!-- example: above_average_bug -->
```cpp
#include <iostream>
#include <vector>

// values must not be empty
double average_of(const std::vector<int>& values) {
    double total{0.0};

    for (const int value : values) {
        total += value;
    }

    return total / values.size();
}

std::vector<int> values_above(const std::vector<int>& values, double threshold) {
    std::vector<int> selected{};

    for (const int value : values) {
        if (value >= threshold) {
            selected.push_back(value);
        }
    }

    return selected;
}

int main() {
    const std::vector<int> first_test{5, 7};
    const std::vector<int> second_test{5, 7, 9};

    const std::vector<int> first_result{values_above(first_test, average_of(first_test))};
    const std::vector<int> second_result{values_above(second_test, average_of(second_test))};

    std::cout << "Test {5, 7}:";
    for (const int value : first_result) {
        std::cout << " " << value;
    }
    std::cout << "\n";

    std::cout << "Test {5, 7, 9}:";
    for (const int value : second_result) {
        std::cout << " " << value;
    }
    std::cout << "\n";
}
```

1. **Przewidź**, jakie wartości powinny być w obu wynikach. Średnie to 6 i 7.
2. Uruchom program i porównaj z przewidywaniem.
3. Dlaczego pierwszy test nie ujawnia błędu?
4. Znajdź niepoprawny warunek i popraw go.
5. Uruchom oba testy ponownie.

</details>

<details>
<summary>Zgłoszenie B: pominięta para</summary>

Wymaganie: funkcja liczy dni, w których wynik był większy niż dnia poprzedniego, dla **wszystkich** par kolejnych dni.

<!-- example: improvements_bug -->
```cpp
#include <cstddef>
#include <iostream>
#include <vector>

int count_improvements(const std::vector<int>& values) {
    int improvements{0};

    for (std::size_t index{1}; index + 1 < values.size(); ++index) {
        if (values[index] > values[index - 1]) {
            ++improvements;
        }
    }

    return improvements;
}

int main() {
    const std::vector<int> first_test{10, 8, 6};
    const std::vector<int> second_test{10, 8, 12};

    std::cout << "Test {10, 8, 6}: " << count_improvements(first_test) << "\n";
    std::cout << "Test {10, 8, 12}: " << count_improvements(second_test) << "\n";
}
```

1. **Przewidź** poprawne wyniki obu testów.
2. Prześledź indeksy dla `{10, 8, 12}`: od którego indeksu zaczyna się pętla, przy jakim indeksie się kończy i które pary porównuje?
3. Uruchom program. Dlaczego pierwszy test nie ujawnia błędu?
4. Znajdź parę, której program nie porównuje, i popraw warunek pętli.
5. Sprawdź poprawioną funkcję także dla wektora pustego i jednoelementowego.

</details>

## Zadanie 3: Wyjaśnij swój projekt

Odpowiedz krótko, na piśmie, odwołując się do własnego programu z zadania 1:

1. Dlaczego program potrzebuje wektora, zamiast liczyć wszystko w trakcie odczytu?
2. Dlaczego Twoje funkcje obliczeniowe przyjmują wektor przez `const&`?
3. Dlaczego funkcja średniej wymaga niepustych danych i co w Twoim programie gwarantuje, że ten warunek jest spełniony?
4. Dlaczego funkcja wybierająca wartości tworzy nowy wektor? Czy oryginalny wektor się zmienia?
5. Dlaczego wartości równe średniej nie trafiają do wyniku?
6. Dlaczego pętla porównująca sąsiednie dni zaczyna się od indeksu 1 i jakiego typu jest jej indeks?
7. Dlaczego jeden dzień daje zero popraw?
8. Dlaczego raport pojawia się dopiero po odczytaniu wszystkich dni?
9. Dlaczego poprawność każdej funkcji osobno nie gwarantuje poprawnego raportu?

## Kryteria sukcesu

Sprawdzian jest zaliczony, gdy spełniasz **wszystkie** kryteria. Możesz przy tym korzystać z części B, jeśli uczciwie zaznaczysz to w samoocenie.

- `training_log/main.cpp` napisano od pustego pliku, w poprawnym C++20. Program buduje się bez błędów.
- Program przechowuje poprawne pomiary w `std::vector<int>`, dodając je przez `push_back`, i liczy raport dopiero po odczytaniu wszystkich dni.
- Są trzy funkcje obliczeniowe o zadaniach z wymagań. Przyjmują wektory przez `const std::vector<int>&`, niczego nie odczytują ani nie wypisują, a funkcja wybierająca wartości zwraca nowy `std::vector<int>`.
- Funkcja średniej sumuje w `double` i jest wywoływana tylko z niepustym wektorem, a jej wymaganie jest zapisane w komentarzu.
- Pętla porównująca sąsiednie dni ma indeks `std::size_t`, porównuje wszystkie pary i nie odczytuje elementów spoza zakresu.
- Standardowe wyjście dla przykładów A, B i C oraz dla przypadków, które da się wpisać, zgadza się z wymaganiami. Przypadki z danymi, które kończą się wcześniej, zgadzają się z tabelą przebiegu.
- Po błędzie wejścia, złej liczbie dni albo złej liczbie minut nie pojawia się żadna część raportu.
- Funkcje sprawdzono osobno wydrukami testowymi, a w programie końcowym takich wydruków nie ma.
- Oba zgłoszenia z zadania 2 zdiagnozowano i poprawiono, a poprawki sprawdzono.
- Umiesz wyjaśnić każdą linijkę swojego programu i odpowiedzieć na pytania z zadania 3.

Nazwy funkcji i zmiennych oraz podział programu mogą być inne niż w rozwiązaniu referencyjnym, jeśli są czytelne i spełniają wymagania. Poprawny wynik to warunek konieczny, ale **nie dowód zrozumienia**. Dlatego zadania 2 i 3 są częścią sprawdzianu.

---

# Część B: sprawdzenie i omówienie

Przejdź tutaj po wykonaniu części A albo wtedy, gdy świadomie zrezygnujesz z dalszej samodzielnej próby.

## Jak sprawdzić swoją pracę

- **Standardowe wyjście:** uruchom program dla przykładów i kilku przypadków z tabeli i porównaj linijki programu z oczekiwanymi, znak po znaku. Pomiń wpisane dane widoczne dzięki echu.
- **Koniec danych:** przypadki, w których dane się kończą, sprawdź tabelą przebiegu i porównaj z pełną listą kontrolną. Każdy z nich jest tam sprawdzony automatycznie.
- **Funkcje:** czy każda ma zadanie, które da się opisać jednym zdaniem? Czy któryś algorytm stoi też w `main`?
- **Dane:** czy wektor powstaje tylko z poprawnych wartości i czy żadna funkcja go nie zmienia?

## Podpowiedzi

<details>
<summary>Podpowiedź 1</summary>

Które obliczenia wykorzystują wszystkie zapisane dane, a które potrzebują dostępu do sąsiednich elementów?

</details>

<details>
<summary>Podpowiedź 2</summary>

Najpierw oblicz średnią z niepustego wektora. Następnie wykorzystaj ją jako próg dla funkcji tworzącej nową kolekcję.

</details>

<details>
<summary>Podpowiedź 3</summary>

Do policzenia popraw porównuj bieżący dzień z poprzednim, zaczynając od drugiego elementu. Zapamiętaj, że pierwszy dzień nie ma poprzednika.

</details>

## Pełna lista przypadków kontrolnych

<details>
<summary>Otwórz po przygotowaniu własnej tabeli</summary>

Przykłady A, B i C są sprawdzone w części A. Wszystkie przypadki poniżej są sprawdzone automatycznie, rozwiązaniem referencyjnym.

**Poprawne dzienniki:**

| Minuty | Średnia | Powyżej średniej | Poprawy | Co sprawdza |
|---|---|---|---|---|
| `10, 14, 8, 18, 10` | 12 | `14 18` | 2 | przykład A |
| `7` | 7 | `none` | 0 | przykład B: jeden dzień |
| `5, 7, 9` | 7 | `9` | 2 | przykład C: wartość równa średniej |
| `5, 6` | 5.5 | `6` | 1 | średnia z częścią ułamkową |
| `10, 10, 10, 10` | 10 | `none` | 0 | wszystkie równe: brak wyników i brak popraw |
| `18, 12, 6, 0` | 9 | `18 12` | 0 | same spadki |
| `2, 4, 6, 8, 10` | 6 | `8 10` | 4 | same poprawy |
| `0, 30, 0, 30, 0` | 12 | `30 30` | 2 | granice 0 i 30, powtórzenia w wyniku |
| `0, 5, 10, 15, 20, 25, 30` | 15 | `20 25 30` | 6 | siedem dni |
| `30, 0` | 15 | `30` | 0 | dwa dni, spadek |
| `10, 20, 0` | 10 | `20` | 1 | wartość równa średniej i poprawa w środku |
| `0, 0, 0` | 0 | `none` | 0 | same zera |
| `30, 30, 30` | 30 | `none` | 0 | same maksymalne wartości |
| `10, 8, 12` | 10 | `12` | 1 | poprawa tylko w ostatniej parze |

**Dane niepoprawne i koniec danych:**

| Dane | Wynik po pytaniach | Co sprawdza |
|---|---|---|
| `0` | `Invalid day count` | liczba dni tuż pod zakresem |
| `8` | `Invalid day count` | liczba dni tuż nad zakresem |
| `-1` | `Invalid day count` | ujemna liczba dni |
| `abc` | `Input could not be read` | tekst zamiast liczby dni |
| brak danych | `Input could not be read` | dane kończą się od razu |
| `3`, `-1` | pytanie o dzień 1, potem `Invalid training data` | minuty tuż pod zakresem |
| `3`, `31` | pytanie o dzień 1, potem `Invalid training data` | minuty tuż nad zakresem |
| `3`, `10`, `31` | pytania o dni 1 i 2, potem `Invalid training data` | zła wartość po poprawnej |
| `3`, `abc` | pytanie o dzień 1, potem `Input could not be read` | tekst zamiast pierwszej wartości |
| `3`, `10`, `abc` | pytania o dni 1 i 2, potem `Input could not be read` | tekst zamiast późniejszej wartości |
| `3`, koniec danych | pytanie o dzień 1, potem `Input could not be read` | brak pierwszego dnia |
| `3`, `10`, koniec danych | pytania o dni 1 i 2, potem `Input could not be read` | koniec danych po jednym dniu |
| `5`, `10`, `14`, `8`, koniec danych | pytania o dni 1–4, potem `Input could not be read` | koniec danych po kilku dniach |

W żadnym z tych przypadków nie pojawia się żadna linijka raportu.

<!-- input: training_log -->
```text
2
5
6
```

<!-- output: training_log -->
```text
Enter training day count (1-7):
Enter minutes for day 1 (0-30):
Enter minutes for day 2 (0-30):
Recorded days: 2
Average training minutes: 5.5
Days above average: 1
Above-average minutes: 6
Improved days: 1
```

<!-- input: training_log -->
```text
4
10
10
10
10
```

<!-- output: training_log -->
```text
Enter training day count (1-7):
Enter minutes for day 1 (0-30):
Enter minutes for day 2 (0-30):
Enter minutes for day 3 (0-30):
Enter minutes for day 4 (0-30):
Recorded days: 4
Average training minutes: 10
Days above average: 0
Above-average minutes: none
Improved days: 0
```

<!-- input: training_log -->
```text
4
18
12
6
0
```

<!-- output: training_log -->
```text
Enter training day count (1-7):
Enter minutes for day 1 (0-30):
Enter minutes for day 2 (0-30):
Enter minutes for day 3 (0-30):
Enter minutes for day 4 (0-30):
Recorded days: 4
Average training minutes: 9
Days above average: 2
Above-average minutes: 18 12
Improved days: 0
```

<!-- input: training_log -->
```text
5
2
4
6
8
10
```

<!-- output: training_log -->
```text
Enter training day count (1-7):
Enter minutes for day 1 (0-30):
Enter minutes for day 2 (0-30):
Enter minutes for day 3 (0-30):
Enter minutes for day 4 (0-30):
Enter minutes for day 5 (0-30):
Recorded days: 5
Average training minutes: 6
Days above average: 2
Above-average minutes: 8 10
Improved days: 4
```

<!-- input: training_log -->
```text
5
0
30
0
30
0
```

<!-- output: training_log -->
```text
Enter training day count (1-7):
Enter minutes for day 1 (0-30):
Enter minutes for day 2 (0-30):
Enter minutes for day 3 (0-30):
Enter minutes for day 4 (0-30):
Enter minutes for day 5 (0-30):
Recorded days: 5
Average training minutes: 12
Days above average: 2
Above-average minutes: 30 30
Improved days: 2
```

<!-- input: training_log -->
```text
7
0
5
10
15
20
25
30
```

<!-- output: training_log -->
```text
Enter training day count (1-7):
Enter minutes for day 1 (0-30):
Enter minutes for day 2 (0-30):
Enter minutes for day 3 (0-30):
Enter minutes for day 4 (0-30):
Enter minutes for day 5 (0-30):
Enter minutes for day 6 (0-30):
Enter minutes for day 7 (0-30):
Recorded days: 7
Average training minutes: 15
Days above average: 3
Above-average minutes: 20 25 30
Improved days: 6
```

<!-- input: training_log -->
```text
2
30
0
```

<!-- output: training_log -->
```text
Enter training day count (1-7):
Enter minutes for day 1 (0-30):
Enter minutes for day 2 (0-30):
Recorded days: 2
Average training minutes: 15
Days above average: 1
Above-average minutes: 30
Improved days: 0
```

<!-- input: training_log -->
```text
3
10
20
0
```

<!-- output: training_log -->
```text
Enter training day count (1-7):
Enter minutes for day 1 (0-30):
Enter minutes for day 2 (0-30):
Enter minutes for day 3 (0-30):
Recorded days: 3
Average training minutes: 10
Days above average: 1
Above-average minutes: 20
Improved days: 1
```

<!-- input: training_log -->
```text
3
0
0
0
```

<!-- output: training_log -->
```text
Enter training day count (1-7):
Enter minutes for day 1 (0-30):
Enter minutes for day 2 (0-30):
Enter minutes for day 3 (0-30):
Recorded days: 3
Average training minutes: 0
Days above average: 0
Above-average minutes: none
Improved days: 0
```

<!-- input: training_log -->
```text
3
30
30
30
```

<!-- output: training_log -->
```text
Enter training day count (1-7):
Enter minutes for day 1 (0-30):
Enter minutes for day 2 (0-30):
Enter minutes for day 3 (0-30):
Recorded days: 3
Average training minutes: 30
Days above average: 0
Above-average minutes: none
Improved days: 0
```

<!-- input: training_log -->
```text
3
10
8
12
```

<!-- output: training_log -->
```text
Enter training day count (1-7):
Enter minutes for day 1 (0-30):
Enter minutes for day 2 (0-30):
Enter minutes for day 3 (0-30):
Recorded days: 3
Average training minutes: 10
Days above average: 1
Above-average minutes: 12
Improved days: 1
```

<!-- input: training_log -->
```text
0
```

<!-- output: training_log -->
```text
Enter training day count (1-7):
Invalid day count
```

<!-- input: training_log -->
```text
8
```

<!-- output: training_log -->
```text
Enter training day count (1-7):
Invalid day count
```

<!-- input: training_log -->
```text
-1
```

<!-- output: training_log -->
```text
Enter training day count (1-7):
Invalid day count
```

<!-- input: training_log -->
```text
abc
```

<!-- output: training_log -->
```text
Enter training day count (1-7):
Input could not be read
```

<!-- input: training_log -->
```text
```

<!-- output: training_log -->
```text
Enter training day count (1-7):
Input could not be read
```

<!-- input: training_log -->
```text
3
-1
```

<!-- output: training_log -->
```text
Enter training day count (1-7):
Enter minutes for day 1 (0-30):
Invalid training data
```

<!-- input: training_log -->
```text
3
31
```

<!-- output: training_log -->
```text
Enter training day count (1-7):
Enter minutes for day 1 (0-30):
Invalid training data
```

<!-- input: training_log -->
```text
3
10
31
```

<!-- output: training_log -->
```text
Enter training day count (1-7):
Enter minutes for day 1 (0-30):
Enter minutes for day 2 (0-30):
Invalid training data
```

<!-- input: training_log -->
```text
3
abc
```

<!-- output: training_log -->
```text
Enter training day count (1-7):
Enter minutes for day 1 (0-30):
Input could not be read
```

<!-- input: training_log -->
```text
3
10
abc
```

<!-- output: training_log -->
```text
Enter training day count (1-7):
Enter minutes for day 1 (0-30):
Enter minutes for day 2 (0-30):
Input could not be read
```

<!-- input: training_log -->
```text
3
```

<!-- output: training_log -->
```text
Enter training day count (1-7):
Enter minutes for day 1 (0-30):
Input could not be read
```

<!-- input: training_log -->
```text
3
10
```

<!-- output: training_log -->
```text
Enter training day count (1-7):
Enter minutes for day 1 (0-30):
Enter minutes for day 2 (0-30):
Input could not be read
```

<!-- input: training_log -->
```text
5
10
14
8
```

<!-- output: training_log -->
```text
Enter training day count (1-7):
Enter minutes for day 1 (0-30):
Enter minutes for day 2 (0-30):
Enter minutes for day 3 (0-30):
Enter minutes for day 4 (0-30):
Input could not be read
```

</details>

## Rozwiązanie referencyjne

<details>
<summary>Zadanie 1: dziennik treningów</summary>

<!-- example: training_log -->
```cpp
#include <cstddef>
#include <iostream>
#include <vector>

// values must not be empty
double average_of(const std::vector<int>& values) {
    double total{0.0};

    for (const int value : values) {
        total += value;
    }

    return total / values.size();
}

std::vector<int> values_above(const std::vector<int>& values, double threshold) {
    std::vector<int> selected{};

    for (const int value : values) {
        if (value > threshold) {
            selected.push_back(value);
        }
    }

    return selected;
}

int count_improvements(const std::vector<int>& values) {
    int improvements{0};

    for (std::size_t index{1}; index < values.size(); ++index) {
        if (values[index] > values[index - 1]) {
            ++improvements;
        }
    }

    return improvements;
}

int main() {
    int day_count{0};

    std::cout << "Enter training day count (1-7):\n";
    std::cin >> day_count;

    if (std::cin.fail()) {
        std::cout << "Input could not be read\n";
    } else if (day_count < 1 || day_count > 7) {
        std::cout << "Invalid day count\n";
    } else {
        std::vector<int> minutes{};
        bool input_failed{false};
        bool invalid_data{false};

        for (int day{1}; day <= day_count && !input_failed && !invalid_data; ++day) {
            int day_minutes{0};

            std::cout << "Enter minutes for day " << day << " (0-30):\n";
            std::cin >> day_minutes;

            if (std::cin.fail()) {
                input_failed = true;
            } else if (day_minutes < 0 || day_minutes > 30) {
                invalid_data = true;
            } else {
                minutes.push_back(day_minutes);
            }
        }

        if (input_failed) {
            std::cout << "Input could not be read\n";
        } else if (invalid_data) {
            std::cout << "Invalid training data\n";
        } else {
            const double average{average_of(minutes)};
            const std::vector<int> above_average{values_above(minutes, average)};
            const int improved_days{count_improvements(minutes)};

            std::cout << "Recorded days: " << minutes.size() << "\n";
            std::cout << "Average training minutes: " << average << "\n";
            std::cout << "Days above average: " << above_average.size() << "\n";

            std::cout << "Above-average minutes:";
            if (above_average.empty()) {
                std::cout << " none";
            } else {
                for (const int value : above_average) {
                    std::cout << " " << value;
                }
            }
            std::cout << "\n";

            std::cout << "Improved days: " << improved_days << "\n";
        }
    }
}
```

| Funkcja | Zadanie | Parametry | Wynik |
|---|---|---|---|
| `average_of` | średnia niepustego wektora | wektor przez `const&` | `double` |
| `values_above` | nowy wektor wartości ściśle większych od progu, w ich kolejności | wektor przez `const&`, próg `double` | `std::vector<int>` |
| `count_improvements` | liczba dni lepszych niż poprzedni | wektor przez `const&` | `int` |
| `main` | odczyt, sprawdzenie danych, wywołania funkcji, raport | — | — |

**Przepływ danych dla przykładu A:**

| Krok | Co się dzieje |
|---|---|
| 1 | `main` odczytuje liczbę dni: 5. |
| 2 | Po pięciu poprawnych odczytach `minutes` to `{10, 14, 8, 18, 10}`. |
| 3 | `main` wywołuje `average_of(minutes)`: wektor ma pięć elementów, więc wymaganie jest spełnione. |
| 4 | Funkcja zwraca 12, a `main` zapisuje to w `average`. |
| 5 | `main` przekazuje `minutes` i `average` jako próg do `values_above`. |
| 6 | Funkcja zwraca nowy wektor `{14, 18}`, zapisany w `above_average`. `minutes` się nie zmienia. |
| 7 | `count_improvements(minutes)` porównuje pary dni 2–1, 3–2, 4–3 i 5–4. |
| 8 | Poprawa jest w parach 2–1 i 4–3, więc funkcja zwraca 2. |
| 9 | `main` buduje raport z `minutes.size()`, `average`, `above_average` i `improved_days`. |

**Omówienie:**

1. **Najpierw cały dziennik.** Wartości powyżej średniej da się wskazać dopiero wtedy, gdy średnia jest znana, a to wymaga wszystkich pomiarów. Dlatego program przechowuje je w wektorze i analizuje po odczycie, jak w lekcjach 6.1 i 6.2.
2. **Trzy funkcje, trzy zadania:** średnia, wybór wartości i liczenie popraw. Każda dostaje wektor przez `const&`, bo tylko go czyta.
3. **Argumenty i wyniki:** `average_of` zwraca `double`; `values_above` dostaje dodatkowo próg `double`, bo średnia może mieć część ułamkową, i zwraca `std::vector<int>`; `count_improvements` zwraca `int`.
4. **Średnia przed wyborem:** średnia jest progiem dla `values_above`, więc musi być obliczona wcześniej. `main` przekazuje wynik jednej funkcji do drugiej.
5. **Nowa kolekcja:** `values_above` buduje osobny wektor i zwraca go przez wartość, jak w lekcji 6.5. Oryginał zostaje bez zmian i nadal służy do liczenia popraw.
6. **Poprawa względem poprzedniego dnia:** pętla zaczyna od indeksu 1, bo pierwszy dzień nie ma poprzednika, a warunek `index < values.size()` obejmuje ostatnią parę. Dla pustego i jednoelementowego wektora pętla nie wykonuje żadnego przebiegu.
7. **Wymaganie średniej:** funkcja dzieli przez `values.size()`, więc wektor nie może być pusty. `main` wywołuje ją tylko po odczytaniu od 1 do 7 poprawnych dni. Gdy odczyt się nie uda, żadna funkcja obliczeniowa nie jest wywoływana.
8. **Raport po pełnym odczycie:** dwie flagi kończą pętlę przy pierwszym błędzie. Gałęzie po pętli wybierają komunikat błędu albo raport, więc niepełne dane nigdy nie trafiają do obliczeń.
9. **Bez referencji umożliwiających zmianę:** żadna funkcja nie zmienia danych wywołującego. Wektor wynikowy jest zwracany, a nie wpisywany do argumentu.

To jeden z możliwych podziałów. Poprawne są też na przykład inne nazwy, osobna funkcja `void` wypisująca listę wartości albo funkcja średniej wywoływana w funkcji wybierającej, jeśli funkcje obliczeniowe niczego nie wypisują, a wymaganie niepustego wektora jest zachowane.

</details>

## Zgłoszenia: wyniki i poprawki

<details>
<summary>Zgłoszenie A: wartość równa średniej</summary>

Przed poprawką:

<!-- output: above_average_bug -->
```text
Test {5, 7}: 7
Test {5, 7, 9}: 7 9
```

- Dla `{5, 7}` średnia to 6, a żadna wartość nie jest jej równa, więc wynik `7` jest poprawny i błąd się nie ujawnia.
- Dla `{5, 7, 9}` średnia to 7, a wynik zawiera też 7. Wymaganie mówi o wartościach **ściśle** większych.
- **Przyczyna:** warunek `value >= threshold`.
- **Poprawka:** `value > threshold`.

<!-- example: above_average_fixed -->
```cpp
#include <iostream>
#include <vector>

// values must not be empty
double average_of(const std::vector<int>& values) {
    double total{0.0};

    for (const int value : values) {
        total += value;
    }

    return total / values.size();
}

std::vector<int> values_above(const std::vector<int>& values, double threshold) {
    std::vector<int> selected{};

    for (const int value : values) {
        if (value > threshold) {
            selected.push_back(value);
        }
    }

    return selected;
}

int main() {
    const std::vector<int> first_test{5, 7};
    const std::vector<int> second_test{5, 7, 9};

    const std::vector<int> first_result{values_above(first_test, average_of(first_test))};
    const std::vector<int> second_result{values_above(second_test, average_of(second_test))};

    std::cout << "Test {5, 7}:";
    for (const int value : first_result) {
        std::cout << " " << value;
    }
    std::cout << "\n";

    std::cout << "Test {5, 7, 9}:";
    for (const int value : second_result) {
        std::cout << " " << value;
    }
    std::cout << "\n";
}
```

<!-- output: above_average_fixed -->
```text
Test {5, 7}: 7
Test {5, 7, 9}: 9
```

</details>

<details>
<summary>Zgłoszenie B: pominięta para</summary>

Przed poprawką:

<!-- output: improvements_bug -->
```text
Test {10, 8, 6}: 0
Test {10, 8, 12}: 0
```

- Dla `{10, 8, 6}` poprawy nie ma w żadnej parze, więc wynik 0 jest poprawny i błąd się nie ujawnia.
- Dla `{10, 8, 12}` poprawny wynik to 1: dzień 3 (12) jest lepszy od dnia 2 (8).
- **Ślad indeksów:** wektor ma 3 elementy. Pętla zaczyna od indeksu 1: `1 + 1 < 3` daje `true`, więc porównuje `values[1]` z `values[0]`, czyli 8 z 10. Dla indeksu 2: `2 + 1 < 3` daje `false`, więc pętla kończy się **przed** porównaniem `values[2]` z `values[1]`, czyli ostatniej pary.
- **Przyczyna:** warunek `index + 1 < values.size()` kończy pętlę o jeden przebieg za wcześnie. Odczytu poza zakresem tu nie ma: program po prostu pomija ostatnią parę.
- **Poprawka:** `index < values.size()`, jak w lekcji 6.3. Wtedy ostatni przebieg ma `index` równy `size() - 1` i porównuje ostatni element z poprzednim.

<!-- example: improvements_fixed -->
```cpp
#include <cstddef>
#include <iostream>
#include <vector>

int count_improvements(const std::vector<int>& values) {
    int improvements{0};

    for (std::size_t index{1}; index < values.size(); ++index) {
        if (values[index] > values[index - 1]) {
            ++improvements;
        }
    }

    return improvements;
}

int main() {
    const std::vector<int> first_test{10, 8, 6};
    const std::vector<int> second_test{10, 8, 12};
    const std::vector<int> one_day{7};
    const std::vector<int> no_days{};

    std::cout << "Test {10, 8, 6}: " << count_improvements(first_test) << "\n";
    std::cout << "Test {10, 8, 12}: " << count_improvements(second_test) << "\n";
    std::cout << "Test {7}: " << count_improvements(one_day) << "\n";
    std::cout << "Test {}: " << count_improvements(no_days) << "\n";
}
```

<!-- output: improvements_fixed -->
```text
Test {10, 8, 6}: 0
Test {10, 8, 12}: 1
Test {7}: 0
Test {}: 0
```

Dla wektora jednoelementowego i pustego pętla od indeksu 1 nie wykonuje żadnego przebiegu, więc funkcja zwraca 0.

</details>

## Odpowiedzi do zadania 3

<details>
<summary>Przykładowe odpowiedzi</summary>

1. Bo wartości powyżej średniej można wskazać dopiero po obliczeniu średniej, a ta wymaga wszystkich pomiarów. W trakcie odczytu średnia nie jest jeszcze znana, więc pomiary trzeba przechować i przejrzeć ponownie.
2. Bo tylko czytają pomiary: nie potrzebują ich kopii i nie mogą ich zmienić przez parametr.
3. Bo dzieli sumę przez liczbę elementów, a średnia pustego zbioru w naszym modelu nie istnieje. Gwarantuje to `main`: liczba dni musi być od 1 do 7, a funkcja jest wywoływana dopiero po odczytaniu wszystkich dni bez błędu.
4. Bo wynik to inny zbiór danych niż wejście, a funkcja nie ma zmieniać pomiarów. Oryginalny wektor zostaje bez zmian, bo funkcja dostaje go przez `const&`.
5. Bo wymaganie mówi o wartościach ściśle większych od średniej, więc warunek to `>`. Przykład C to sprawdza.
6. Bo każdy dzień porównujemy z poprzednim, a dzień o indeksie 0 poprzednika nie ma. Indeks jest typu `std::size_t`, tak jak wynik `size()`.
7. Bo jeden dzień nie tworzy żadnej pary kolejnych dni. Pętla od indeksu 1 nie wykonuje wtedy ani jednego przebiegu.
8. Bo raport opisuje cały dziennik. Gdy odczyt się nie uda albo dane są niepoprawne, dziennik jest niepełny, a funkcja średniej mogłaby dostać pusty wektor.
9. Bo raport zależy też od `main`: od kolejności wywołań, przekazanych argumentów, na przykład progu, i od sposobu wypisania wyników. Każda funkcja może działać poprawnie, a raport i tak może być błędny.

</details>

## Samoocena

Przy każdym kryterium zaznacz jedną odpowiedź:

| Kryterium | Samodzielnie | Z podpowiedzią | Po zajrzeniu do rozwiązania | Do powtórki |
|---|---|---|---|---|
| Zaprojektowanie trzech funkcji i ich zadań | | | | |
| Przechowywanie pomiarów w wektorze przez `push_back` | | | | |
| Odczyt i sprawdzanie danych, koniec danych | | | | |
| Średnia w `double` i wymaganie niepustego wektora | | | | |
| Funkcja zwracająca nowy wektor | | | | |
| Pętla po sąsiednich dniach i indeks `std::size_t` | | | | |
| Raport z `none` i bez spacji na końcu | | | | |
| Wydruki testowe funkcji | | | | |
| Tabela przypadków z granicami | | | | |
| Zgłoszenie A (wartość równa średniej) | | | | |
| Zgłoszenie B (pominięta para) | | | | |
| Wyjaśnienia z zadania 3 | | | | |

Jeśli w kolumnie „Do powtórki” jest coś zaznaczone, wróć do odpowiedniej lekcji:

| Temat | Lekcja |
|---|---|
| wektor i pętla zakresowa | [6.1](lesson_01_the_first_vector.md) |
| dodawanie elementów, pusty wektor i średnia | [6.2](lesson_02_adding_to_a_vector.md) |
| indeksy, `std::size_t` i sąsiednie elementy | [6.3](lesson_03_positions_and_neighbours.md) |
| wektor jako parametr `const&` | [6.4](lesson_04_a_vector_as_a_parameter.md) |
| funkcja zwracająca nowy wektor | [6.5](lesson_05_a_function_returns_a_vector.md) |
| podział odpowiedzialności i wydruki testowe | [5.5](../module_05_functions/lesson_05_several_functions.md) |
| deklaracja i definicja | [5.6](../module_05_functions/lesson_06_declaration_and_definition.md) |
| odczyt danych, flagi i pętle | [4.5](../module_04_repeating_actions/lesson_05_ask_again.md), [4.6](../module_04_repeating_actions/lesson_06_recover_and_end_of_input.md), [4.7](../module_04_repeating_actions/lesson_07_the_program_repeats.md) |

Potem spróbuj zadania jeszcze raz, na przykład z innym zakresem minut albo z wartościami poniżej średniej zamiast powyżej.

---

## Podsumowanie Modułu 6

Po sześciu lekcjach potrafisz:

- przechowywać wiele wartości tego samego typu w `std::vector<int>` i przeglądać je pętlą zakresową;
- dodawać elementy przez `push_back`, sprawdzać `size()` i `empty()` oraz odróżniać próby odczytu od zapisanych elementów;
- liczyć średnią bez dzielenia całkowitego i tylko wtedy, gdy są dane;
- odczytywać elementy przez indeks, przechowywać indeksy w `std::size_t` i bezpiecznie porównywać sąsiednie elementy;
- przekazywać wektor do funkcji przez `const&`, bez kopiowania i bez zmieniania go;
- zwracać z funkcji nowy wektor i dalej z nim pracować;
- projektować programy, które zbierają dane, analizują je kilka razy i budują raport z wyników współpracujących funkcji.

To podstawy pracy z kolekcjami. Wektory mają jeszcze wiele możliwości, które poznasz w dalszych modułach.

## Co dalej

W Module 7, „Tekst jako ciąg znaków: `std::string` i `char`”, przejrzysz tekst znak po znaku, tak jak elementy wektora. Zacznij od pierwszych znaków: [Lekcja 7.1: Pierwsze znaki: `char` i przeglądanie `std::string`](../module_07_text/lesson_01_first_characters.md).

**Poprzednia lekcja:** [Lekcja 6.5: Funkcja tworzy i zwraca nowy wektor](lesson_05_a_function_returns_a_vector.md) · **Następna lekcja:** [Lekcja 7.1: Pierwsze znaki: `char` i przeglądanie `std::string`](../module_07_text/lesson_01_first_characters.md) · [Opis kursu](../../README.md)

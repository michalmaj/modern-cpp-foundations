# Lekcja 3.1: Pierwsza decyzja programu (`if`)

**Polski** · [English](lesson_01_the_first_decision.en.md) · [Opis kursu](../../README.md)

> **Moduł 3, lekcja 1** · około 60 minut
> **Potrzebujesz:** katalogu `cpp-workspace` i oryginalnego projektu `lesson_05_first_program`, jak dotąd. Debugger nie jest w tej lekcji potrzebny.
> **Wersja pilotażowa.** Programy z tej lekcji sprawdzamy automatycznie na Windowsie, Ubuntu i macOS, także z podanymi danymi wejściowymi.

## Zanim zaczniesz

Ta lekcja zakłada, że po Module 2:

- odczytujesz liczby `int` i `double` przez `std::cin` i uruchamiasz ten sam program z różnymi danymi;
- odróżniasz dane wejściowe od standardowego wyjścia programu;
- przewidujesz wynik programu, zanim go uruchomisz.

## Sytuacja

Do tej pory każdy program wykonywał wszystkie swoje instrukcje, jedna po drugiej, zawsze tak samo. Prawdziwe programy często robią coś **tylko wtedy, gdy** zachodzi jakiś warunek: ostrzegają, gdy kończą się miejsca, albo doliczają opłatę, gdy bagaż jest za ciężki. Dziś program po raz pierwszy podejmie decyzję: **niektóre instrukcje wykona albo pominie, zależnie od danych**.

Po tej lekcji będziesz:

- wyjaśniać, do czego służy `if`;
- porównywać dwie wartości operatorami `<`, `<=`, `>` i `>=`;
- przewidywać, czy warunek jest spełniony, i które instrukcje się wykonają;
- rozpoznawać, które instrukcje należą do bloku `if`, a które wykonują się zawsze;
- pisać własny prosty `if`, zawsze z klamrami;
- sprawdzać program dla wartości tuż przy granicy i znajdować pomyłkę `<` zamiast `<=`.

## 1. Przygotuj projekt

W `cpp-workspace` utwórz katalog `lesson_3_1` i skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program`. Programy z punktów 2–6 wpisujesz w `main.cpp` tego katalogu.

## 2. Kończą się miejsca

Program dostaje liczbę wolnych miejsc w sali. Jeśli zostało ich **mniej niż 5**, ma wypisać dodatkowe ostrzeżenie. Na końcu zawsze wypisuje, że sprawdzanie się skończyło:

<!-- example: seats_check -->
```cpp
#include <iostream>

int main() {
    int seats_left{0};

    std::cout << "Enter seats left:\n";
    std::cin >> seats_left;

    if (seats_left < 5) {
        std::cout << "Few seats left\n";
    }

    std::cout << "Check complete\n";
}
```

Zanim uruchomisz program, **odpowiedz na piśmie**:

1. Co wypisze program, gdy wolnych miejsc jest 3?
2. A gdy jest ich 12?
3. A gdy jest ich dokładnie 5?
4. Czy `Check complete` pojawi się w każdym z tych przypadków?

Teraz uruchom program trzy razy, bez zmiany kodu, i wpisz kolejno `3`, `12` i `5`.

<!-- input: seats_check -->
```text
3
```

<details>
<summary>Standardowe wyjście dla 3</summary>

<!-- output: seats_check -->
```text
Enter seats left:
Few seats left
Check complete
```

</details>

<!-- input: seats_check -->
```text
12
```

<details>
<summary>Standardowe wyjście dla 12</summary>

<!-- output: seats_check -->
```text
Enter seats left:
Check complete
```

</details>

<!-- input: seats_check -->
```text
5
```

<details>
<summary>Standardowe wyjście dla 5</summary>

<!-- output: seats_check -->
```text
Enter seats left:
Check complete
```

</details>

**Co się stało, linijka po linijce?**

- `if` (po polsku „jeśli”) **podejmuje decyzję**: wykonać kolejne instrukcje czy je pominąć.
- W nawiasach okrągłych stoi **warunek**: `seats_left < 5`. Program sprawdza go z aktualną wartością zmiennej, czyli z tą, którą właśnie odczytał.
- `<` **porównuje** dwie wartości: czy lewa jest mniejsza od prawej. Porównanie daje odpowiedź **tak** albo **nie**.
- Klamry `{ }` wyznaczają **blok** instrukcji, które należą do `if`.
- Blok wykonuje się **tylko wtedy, gdy odpowiedź brzmi „tak”**. Dla 3 tak jest (3 jest mniejsze od 5), więc pojawia się `Few seats left`. Dla 12 i dla 5 odpowiedź brzmi „nie”, więc program **pomija** cały blok.
- `std::cout << "Check complete\n";` stoi **za** zamykającą klamrą, więc nie należy do `if`. Wykonuje się zawsze.

`if` nie zatrzymuje programu, gdy warunek nie jest spełniony. Program po prostu **przeskakuje blok** i wykonuje dalej to, co stoi po nim, od góry do dołu, jak dotąd.

**Dlaczego 5 nie wywołało ostrzeżenia?** 5 nie jest mniejsze od 5. Warunek `seats_left < 5` jest spełniony dla 4, 3, 2 i mniejszych liczb, ale nie dla 5. Wrócimy do tego w punkcie 6.

## 3. Klamry i wcięcia

Każdy `if` w tym kursie wygląda tak samo: warunek w nawiasach okrągłych, a po nim blok w klamrach.

<!-- fragment -->
```cpp
if (seats_left < 5) {
    std::cout << "Few seats left\n";
}
```

- Instrukcje wewnątrz bloku są **wcięte**, czyli przesunięte w prawo, jak instrukcje w `main`. Wcięcie pomaga zobaczyć, co należy do `if`, ale o tym decydują **klamry**, nie wcięcie.
- W C++ można też napisać `if` bez klamer, gdy w środku jest tylko jedna instrukcja. **W tym kursie zawsze stawiamy klamry**, także wokół jednej instrukcji: od razu widać, gdzie kończy się blok, a dopisanie kolejnej instrukcji do bloku nie zmieni po cichu działania programu.
- Po `if (…)` nie stawia się średnika. Blok w klamrach to część tej samej konstrukcji.

## 4. Cztery porównania

Oprócz `<` znasz już z matematyki trzy podobne porównania. W C++ zapisuje się je tak:

| Operator | Znaczenie | Przykład | Kiedy odpowiedź brzmi „tak” |
|---|---|---|---|
| `<` | mniej niż | `seats_left < 5` | wolnych miejsc jest mniej niż 5 |
| `<=` | mniej niż lub równo | `temperature_c <= 25` | temperatura nie przekracza 25 stopni |
| `>` | więcej niż | `weight_kg > 20.0` | bagaż przekracza 20 kg |
| `>=` | więcej niż lub równo | `points >= 50` | wynik osiągnął wymagane minimum 50 punktów |

- `<=` i `>=` zapisuje się dwoma znakami, bez spacji między nimi, z `=` na drugim miejscu.
- Różnica między `<` a `<=` (i między `>` a `>=`) dotyczy **tylko samej granicy**. Dla 25 warunek `temperature_c <= 25` jest spełniony, a warunek `temperature_c < 25` nie.
- Można porównywać liczby `int` i `double`, jak w przykładzie z bagażem.

**Przewidź.** Przepisz tabelę i wpisz, czy warunek jest spełniony (tak albo nie):

| Warunek | dla wartości 49 | dla 50 | dla 51 |
|---|---|---|---|
| `points >= 50` | | | |
| `points > 50` | | | |
| `points < 50` | | | |
| `points <= 50` | | | |

Odpowiedzi są w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 5. Przed blokiem, w bloku, po bloku

Ten program wypisuje coś przed `if`, coś w bloku `if` i coś po nim:

<!-- example: hot_day -->
```cpp
#include <iostream>

int main() {
    int temperature_c{0};

    std::cout << "Enter temperature:\n";
    std::cin >> temperature_c;

    std::cout << "Checking temperature\n";

    if (temperature_c > 30) {
        std::cout << "Hot day: drink water\n";
    }

    std::cout << "Have a nice day\n";
}
```

**Przewidź**, które linijki pojawią się dla temperatury `25`, a które dla `32`. Zapisz je, a potem uruchom program dwa razy.

<!-- input: hot_day -->
```text
25
```

<details>
<summary>Standardowe wyjście dla 25</summary>

<!-- output: hot_day -->
```text
Enter temperature:
Checking temperature
Have a nice day
```

</details>

<!-- input: hot_day -->
```text
32
```

<details>
<summary>Standardowe wyjście dla 32</summary>

<!-- output: hot_day -->
```text
Enter temperature:
Checking temperature
Hot day: drink water
Have a nice day
```

</details>

Linijki przed blokiem i po nim pojawiają się zawsze. Linijka z bloku pojawia się tylko wtedy, gdy warunek jest spełniony.

**Zmień.** Ostrzeżenie ma się teraz pojawiać **od 25 stopni włącznie**. Zmień warunek: zarówno operator, jak i liczbę. Potem **przewidź** wynik dla `24` i `25` i sprawdź oba przypadki. Przykładowa zmiana jest w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

Jeśli debugger działa u Ciebie od lekcji 2.3, możesz postawić breakpoint na linijce z `if` i kliknąć **Step Over**: zobaczysz, czy następną zaznaczoną linijką jest instrukcja w bloku, czy ta po nim. To dodatkowa możliwość. Wystarczy przewidzieć, uruchomić, porównać i wyjaśnić.

## 6. Znajdź błąd: dokładnie na granicy

Organizatorzy zmienili wymaganie:

> Wyświetl ostrzeżenie, jeśli zostało **5 lub mniej** wolnych miejsc.

W programie został jednak stary warunek:

<!-- example: seats_limit_bug -->
```cpp
#include <iostream>

int main() {
    int seats_left{0};

    std::cout << "Enter seats left:\n";
    std::cin >> seats_left;

    if (seats_left < 5) {
        std::cout << "Few seats left\n";
    }

    std::cout << "Check complete\n";
}
```

1. Przeczytaj wymaganie i **przewidź**, co **powinien** wypisać program dla `4`, `5` i `6`.
2. Uruchom program dla tych trzech wartości.
3. Znajdź przypadek, w którym wynik nie spełnia wymagania.
4. Popraw warunek.
5. Sprawdź ponownie **wszystkie trzy** przypadki.

Dane testowe to trzy osobne uruchomienia: `4`, `5` i `6`.

Wyniki programu przed poprawką i poprawiony program są w części [Przykładowe rozwiązania](#przykładowe-rozwiązania). Zajrzyj tam po własnej próbie.

**Dlaczego 3 i 12 by tego nie wykryły?** Dla 3 obie wersje warunku, `< 5` i `<= 5`, dają „tak”, a dla 12 obie dają „nie”. Te wartości leżą daleko od granicy, więc obie wersje zachowują się tak samo. Różnią się **tylko dla 5**. Dlatego warunek sprawdzaj zawsze także **dokładnie na granicy** i tuż obok niej: o jeden mniej i o jeden więcej.

## 7. Misja: limit wagi bagażu

Na lotnisku każdy bagaż waży się przed odprawą. Limit to 20 kg. Jeśli bagaż **przekracza** 20 kg, program wypisuje dodatkowe ostrzeżenie. Na końcu zawsze wypisuje, że kontrola się skończyła.

W `cpp-workspace` utwórz katalog `luggage_check`, skopiuj do niego `CMakeLists.txt` z oryginalnego `lesson_05_first_program`, utwórz pusty `main.cpp` i napisz program samodzielnie. Program odczytuje jedną wartość: wagę bagażu w kilogramach, liczbę z częścią ułamkową.

Dla wagi `19.5` standardowe wyjście ma być takie:

<!-- input: luggage_check -->
```text
19.5
```

<!-- output: luggage_check -->
```text
Enter luggage weight in kg:
Luggage check complete
```

Dla `20.0`:

<!-- input: luggage_check -->
```text
20.0
```

<!-- output: luggage_check -->
```text
Enter luggage weight in kg:
Luggage check complete
```

Dla `20.5`:

<!-- input: luggage_check -->
```text
20.5
```

<!-- output: luggage_check -->
```text
Enter luggage weight in kg:
Overweight: extra fee required
Luggage check complete
```

### Kryterium sukcesu

- Program buduje się jako C++20, a jego standardowe wyjście dla `19.5`, `20.0` i `20.5` jest dokładnie takie jak powyżej.
- Waga bagażu jest zmienną typu `double` z wartością początkową, a limit 20 kg jest zapisany w programie tylko raz, jako stała.
- Ostrzeżenie jest w bloku `if`, a komunikat końcowy za blokiem. `if` ma klamry.
- Ten sam program daje wszystkie trzy wyniki, bez zmiany kodu.
- Program używa tylko tego, co już znasz, oraz `if` i porównań z tej lekcji.
- Umiesz wyjaśnić, dlaczego dla dokładnie 20 kg ostrzeżenie się nie pojawia.

Gdy wynik się zgadza, możesz zapisać projekt w Gicie, jak w lekcji 1.5.

<details>
<summary>Podpowiedź 1</summary>

Wymaganie mówi „przekracza 20 kg”. Czy 20 kg przekracza 20 kg? Który z czterech operatorów odpowiada na pytanie „czy więcej niż”?

</details>

<details>
<summary>Podpowiedź 2</summary>

Kolejność jak w punkcie 2: zmienna i stała, prośba i odczyt, `if` z ostrzeżeniem w bloku, a na końcu, za klamrą, komunikat, który pojawia się zawsze.

</details>

Przykładowe rozwiązanie jest w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 8. Gdy coś pójdzie inaczej

| Co widzisz | Co to znaczy | Co zrobić |
|---|---|---|
| Ostrzeżenie pojawia się zawsze albo nigdy | Warunek nie odpowiada wymaganiu, na przykład ma odwrotny znak (`>` zamiast `<`). | Przeczytaj warunek na głos: „jeśli … jest mniejsze od …”. Sprawdź wartość, dla której odpowiedź powinna brzmieć „tak”. |
| Program działa dla wartości daleko od granicy, ale źle dokładnie na niej | Pomylono `<` z `<=` albo `>` z `>=`. | Sprawdź samą granicę i wartości tuż obok niej (punkt 6). |
| Komunikat, który miał pojawiać się zawsze, pojawia się tylko czasem | Stoi wewnątrz bloku, przed zamykającą klamrą. | Przenieś go za `}`. |
| Ostrzeżenie pojawia się, choć warunek nie jest spełniony | Ostrzeżenie stoi poza blokiem, za `}`. | Instrukcja, która ma zależeć od warunku, musi stać między `{` a `}`. |
| Błąd kompilacji przy `if` | Zwykle brakuje nawiasu okrągłego albo klamry. | Warunek w `( )`, blok w `{ }`. Każdy nawias i każda klamra ma swoją parę. |
| `=<` albo `= <` zamiast `<=` | Operator zapisuje się dwoma znakami, w kolejności `<=` (lub `>=`), bez spacji. | Popraw zapis na `<=` albo `>=`. |

## 9. Wyjaśnij

Odpowiedz własnymi słowami, najlepiej na piśmie. Dopiero potem porównaj z przykładową odpowiedzią.

**1.** Co robi program, gdy warunek w `if` nie jest spełniony?

<details>
<summary>Przykładowa odpowiedź</summary>

Pomija blok w klamrach i wykonuje dalej instrukcje, które stoją po zamykającej klamrze. Program się nie zatrzymuje.

</details>

**2.** Skąd wiadomo, które instrukcje należą do bloku `if`?

<details>
<summary>Przykładowa odpowiedź</summary>

Należą do niego instrukcje między `{` a `}` po warunku. Wcięcie pomaga je zobaczyć, ale o przynależności decydują klamry.

</details>

**3.** Czym różnią się `seats_left < 5` i `seats_left <= 5`? Dla jakich wartości dają różną odpowiedź?

<details>
<summary>Przykładowa odpowiedź</summary>

`<` znaczy „mniej niż”, a `<=` „mniej niż lub równo”. Różną odpowiedź dają tylko dla 5: `5 < 5` to „nie”, a `5 <= 5` to „tak”.

</details>

**4.** Dlaczego sprawdzenie programu tylko dla 3 i 12 nie wystarczyło, żeby znaleźć błąd z punktu 6?

<details>
<summary>Przykładowa odpowiedź</summary>

Bo dla 3 i 12 błędny i poprawny warunek dają tę samą odpowiedź. Różnią się tylko na samej granicy, dla 5. Trzeba sprawdzić granicę i wartości tuż obok niej.

</details>

**5.** Dlaczego w misji bagaż ważący dokładnie 20 kg nie wywołuje ostrzeżenia?

<details>
<summary>Przykładowa odpowiedź</summary>

Bo wymaganie mówi „przekracza 20 kg”, a 20 nie jest większe od 20. Warunek `>` daje dla 20 odpowiedź „nie”. Ostrzeżenie pojawia się dopiero dla wartości większych od 20, na przykład 20.5.

</details>

## Podsumowanie

- `if (warunek) { … }` wykonuje blok tylko wtedy, gdy warunek jest spełniony. W przeciwnym razie program pomija blok i idzie dalej. Nie zatrzymuje się.
- Instrukcje za zamykającą klamrą nie należą do `if` i wykonują się zawsze.
- Porównania `<`, `<=`, `>` i `>=` dają odpowiedź „tak” albo „nie”, z aktualnymi wartościami zmiennych.
- `<` i `<=` (tak samo `>` i `>=`) różnią się tylko na samej granicy. Dlatego sprawdzaj program dokładnie na granicy i tuż obok niej.
- W tym kursie `if` zawsze ma klamry, a instrukcje w bloku są wcięte.

## Co dalej

Twój program potrafi już wykonać coś albo to pominąć. W lekcji 3.2 nauczy się wybierać **jedną z dwóch dróg** i sprawdzać, czy wartości są równe. Poznasz też nazwę odpowiedzi „tak” albo „nie”, którą daje porównanie: [Lekcja 3.2: Dwie możliwości (`else`), równość i `bool`](lesson_02_two_ways.md).

---

## Przykładowe rozwiązania

Zajrzyj tutaj **po własnej próbie**. Twoje nazwy mogą się różnić, jeśli standardowe wyjście jest takie, jak wymagane.

<details>
<summary>Punkt 4: cztery porównania</summary>

| Warunek | dla 49 | dla 50 | dla 51 |
|---|---|---|---|
| `points >= 50` | nie | tak | tak |
| `points > 50` | nie | nie | tak |
| `points < 50` | tak | nie | nie |
| `points <= 50` | tak | tak | nie |

Na granicy, dla 50, odpowiedź zależy od tego, czy w operatorze jest `=`.

</details>

<details>
<summary>Punkt 5: ostrzeżenie od 25 stopni włącznie</summary>

<!-- example: hot_day_changed -->
```cpp
#include <iostream>

int main() {
    int temperature_c{0};

    std::cout << "Enter temperature:\n";
    std::cin >> temperature_c;

    std::cout << "Checking temperature\n";

    if (temperature_c >= 25) {
        std::cout << "Hot day: drink water\n";
    }

    std::cout << "Have a nice day\n";
}
```

<!-- input: hot_day_changed -->
```text
24
```

<!-- output: hot_day_changed -->
```text
Enter temperature:
Checking temperature
Have a nice day
```

<!-- input: hot_day_changed -->
```text
25
```

<!-- output: hot_day_changed -->
```text
Enter temperature:
Checking temperature
Hot day: drink water
Have a nice day
```

„Od 25 włącznie” to `>= 25`. Warunek `> 24` też dałby te same wyniki dla liczb całkowitych, ale `>= 25` mówi wprost to, co wymaganie.

</details>

<details>
<summary>Punkt 6: wyniki przed poprawką i poprawiony program</summary>

Przed poprawką dla `4`, `5` i `6`:

<!-- input: seats_limit_bug -->
```text
4
```

<!-- output: seats_limit_bug -->
```text
Enter seats left:
Few seats left
Check complete
```

<!-- input: seats_limit_bug -->
```text
5
```

<!-- output: seats_limit_bug -->
```text
Enter seats left:
Check complete
```

<!-- input: seats_limit_bug -->
```text
6
```

<!-- output: seats_limit_bug -->
```text
Enter seats left:
Check complete
```

Dla 5 ostrzeżenia brakuje, choć wymaganie mówi „5 lub mniej”. Warunek `seats_left < 5` nie obejmuje samej piątki. Poprawka to `<=`:

<!-- example: seats_limit_fixed -->
```cpp
#include <iostream>

int main() {
    int seats_left{0};

    std::cout << "Enter seats left:\n";
    std::cin >> seats_left;

    if (seats_left <= 5) {
        std::cout << "Few seats left\n";
    }

    std::cout << "Check complete\n";
}
```

Po poprawce dla `4`, `5` i `6`:

<!-- input: seats_limit_fixed -->
```text
4
```

<!-- output: seats_limit_fixed -->
```text
Enter seats left:
Few seats left
Check complete
```

<!-- input: seats_limit_fixed -->
```text
5
```

<!-- output: seats_limit_fixed -->
```text
Enter seats left:
Few seats left
Check complete
```

<!-- input: seats_limit_fixed -->
```text
6
```

<!-- output: seats_limit_fixed -->
```text
Enter seats left:
Check complete
```

</details>

<details>
<summary>Punkt 7: misja, limit wagi bagażu</summary>

<!-- example: luggage_check -->
```cpp
#include <iostream>

int main() {
    const double weight_limit_kg{20.0};
    double luggage_weight_kg{0.0};

    std::cout << "Enter luggage weight in kg:\n";
    std::cin >> luggage_weight_kg;

    if (luggage_weight_kg > weight_limit_kg) {
        std::cout << "Overweight: extra fee required\n";
    }

    std::cout << "Luggage check complete\n";
}
```

- Waga może mieć część ułamkową, więc jest typu `double`. Limit się nie zmienia, więc jest stałą `const double`.
- „Przekracza 20 kg” to `>`: dla 20.0 odpowiedź brzmi „nie”, dla 20.5 „tak”.
- Komunikat końcowy stoi za zamykającą klamrą, więc pojawia się zawsze.

</details>

**Poprzednia lekcja:** [Lekcja 2.8: Od danych do wyniku (sprawdzian Modułu 2)](../module_02_values_and_calculations/lesson_08_from_data_to_result.md) · **Następna lekcja:** [Lekcja 3.2: Dwie możliwości (`else`), równość i `bool`](lesson_02_two_ways.md) · [Opis kursu](../../README.md)

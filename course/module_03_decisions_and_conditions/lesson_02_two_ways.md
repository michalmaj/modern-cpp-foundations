# Lekcja 3.2: Dwie możliwości (`else`), równość i `bool`

**Polski** · [English](lesson_02_two_ways.en.md) · [Opis kursu](../../README.md)

> **Moduł 3, lekcja 2** · około 75 minut
> **Potrzebujesz:** katalogu `cpp-workspace` i oryginalnego projektu `lesson_05_first_program`, jak dotąd. Debugger nie jest w tej lekcji potrzebny.
> **Wersja pilotażowa.** Programy z tej lekcji sprawdzamy automatycznie na Windowsie, Ubuntu i macOS, także z podanymi danymi wejściowymi.

## Zanim zaczniesz

Ta lekcja zakłada, że po lekcji 3.1:

- piszesz `if` z porównaniem `<`, `<=`, `>` albo `>=` i wiesz, że blok wykonuje się tylko wtedy, gdy odpowiedź brzmi „tak”;
- sprawdzasz program dokładnie na granicy i tuż obok niej;
- znasz przypisanie (lekcja 2.2), resztę z dzielenia `%` (lekcja 2.4) i `std::string` (lekcja 2.7).

## Sytuacja

W lekcji 3.1 program mógł coś zrobić albo to pominąć. Często jednak trzeba wybrać **jedną z dwóch** możliwości: zaliczone albo niezaliczone, kod poprawny albo błędny. Dziś poznasz `else`, czyli drugą drogę. Nauczysz się też sprawdzać, czy wartości są **równe**, i poznasz nazwę odpowiedzi „tak” albo „nie”, którą daje porównanie.

Po tej lekcji będziesz:

- wybierać jedną z dwóch gałęzi przez `if` i `else` i przewidywać, która się wykona;
- sprawdzać równość operatorem `==` i nierówność operatorem `!=`, także dla tekstu;
- odróżniać przypisanie `=` od porównania `==`;
- wyjaśniać, czym są `bool`, `true` i `false`, i przechowywać wynik porównania w zmiennej `bool`;
- wiedzieć, gdzie zadeklarować zmienną, której używasz po `if`;
- pisać program z dwiema niezależnymi decyzjami i sprawdzać go dla różnych kombinacji danych.

## 1. Przygotuj projekt

W `cpp-workspace` utwórz katalog `lesson_3_2` i skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program`. Programy z punktów 2–8 wpisujesz w `main.cpp` tego katalogu.

## 2. Jedna z dwóch dróg: `else`

Zaliczenie wymaga co najmniej 50 punktów. Program ma wypisać `Passed` albo `Not passed`, a na końcu, zawsze, `Score checked`:

<!-- example: pass_check -->
```cpp
#include <iostream>

int main() {
    int score{0};

    std::cout << "Enter score:\n";
    std::cin >> score;

    if (score >= 50) {
        std::cout << "Passed\n";
    } else {
        std::cout << "Not passed\n";
    }

    std::cout << "Score checked\n";
}
```

**Przewidź**, co wypisze program dla 49, 50 i 51 punktów. Potem uruchom go trzy razy.

<!-- input: pass_check -->
```text
49
```

<details>
<summary>Standardowe wyjście dla 49</summary>

<!-- output: pass_check -->
```text
Enter score:
Not passed
Score checked
```

</details>

<!-- input: pass_check -->
```text
50
```

<details>
<summary>Standardowe wyjście dla 50</summary>

<!-- output: pass_check -->
```text
Enter score:
Passed
Score checked
```

</details>

<!-- input: pass_check -->
```text
51
```

<details>
<summary>Standardowe wyjście dla 51</summary>

<!-- output: pass_check -->
```text
Enter score:
Passed
Score checked
```

</details>

- Gdy warunek jest spełniony, program wykonuje **pierwszą gałąź**, czyli blok po `if`.
- W przeciwnym razie wykonuje **gałąź `else`** (po polsku „w przeciwnym razie”).
- Wykonuje się **dokładnie jedna** z dwóch gałęzi, nigdy obie po kolei.
- `else` **nie ma własnego warunku**. Jego blok wykonuje się wtedy, gdy warunek przy `if` nie jest spełniony.
- Po wybranej gałęzi program idzie dalej: `Score checked` pojawia się zawsze.
- Klamry wyznaczają obie gałęzie, a wcięcia pomagają je zobaczyć. `else` stoi zaraz za zamykającą klamrą pierwszej gałęzi.

**`if` czy `if`/`else`?** Samo `if` z lekcji 3.1 to działanie **opcjonalne**: zrób coś albo nie rób nic. `if`/`else` to wybór **jednej z dwóch alternatyw**: zrób to albo tamto. W tym programie oba komunikaty to dwie możliwe odpowiedzi na to samo pytanie, więc pasuje `else`.

## 3. Przypisanie `=` a porównanie `==`

Przypisanie znasz z lekcji 2.2: `count = 5;` **zmienia** wartość zmiennej. Do sprawdzenia, czy wartości są równe, służy inny operator: **`==`**, dwa znaki równości. Porównaj oba w jednym programie:

<!-- example: assign_and_compare -->
```cpp
#include <iostream>

int main() {
    int count{3};

    if (count == 5) {
        std::cout << "count is 5\n";
    } else {
        std::cout << "count is not 5\n";
    }
    std::cout << "count: " << count << "\n";

    count = 5;
    std::cout << "count: " << count << "\n";

    if (count == 5) {
        std::cout << "count is 5\n";
    } else {
        std::cout << "count is not 5\n";
    }
}
```

**Przewidź** wszystkie cztery linijki, a potem uruchom program.

<details>
<summary>Wynik programu</summary>

<!-- output: assign_and_compare -->
```text
count is not 5
count: 3
count: 5
count is 5
```

</details>

- `count == 5` **sprawdza**, czy `count` jest równe 5, i daje odpowiedź „tak” albo „nie”. Niczego nie zmienia: po pierwszym porównaniu `count` nadal ma 3.
- `count = 5;` **zapisuje** w `count` wartość 5. To polecenie, a nie pytanie.
- To dwie różne operacje, a nie dwa zapisy tego samego. Czytaj `==` jako „czy jest równe?”, a `=` jako „dostaje wartość”.

## 4. Nierówność: `!=`

**`!=`** sprawdza, czy wartości są **różne**. Daje „tak”, gdy się różnią, i „nie”, gdy są równe:

<!-- example: door_code -->
```cpp
#include <iostream>

int main() {
    const int expected_code{1234};
    int code{0};

    std::cout << "Enter door code:\n";
    std::cin >> code;

    if (code != expected_code) {
        std::cout << "Wrong code\n";
    } else {
        std::cout << "Door open\n";
    }
}
```

<!-- input: door_code -->
```text
4321
```

<!-- output: door_code -->
```text
Enter door code:
Wrong code
```

<!-- input: door_code -->
```text
1234
```

<!-- output: door_code -->
```text
Enter door code:
Door open
```

`==` i `!=` dają zawsze odwrotne odpowiedzi: gdy jedno mówi „tak”, drugie mówi „nie”. Ten sam program można napisać z `==`, zamieniając gałęzie miejscami. Wybierz zapis, który czyta się naturalniej dla danego wymagania.

## 5. Odpowiedź ma nazwę: `bool`

W lekcji 3.1 porównanie dawało odpowiedź „tak” albo „nie”. W C++ ta odpowiedź jest wartością typu **`bool`** (wartość logiczna). Typ `bool` ma tylko dwie wartości:

- **`true`**, czyli prawda, „tak”;
- **`false`**, czyli fałsz, „nie”.

Zmienną `bool` tworzy się tak samo jak inne:

<!-- fragment -->
```cpp
bool is_ready{true};
bool is_finished{false};
```

Najczęściej jednak wartość `bool` pochodzi z porównania. Program sprawdza, czy liczba jest parzysta, czyli czy reszta z dzielenia przez 2 wynosi 0:

<!-- example: even_check -->
```cpp
#include <iostream>

int main() {
    int number{0};

    std::cout << "Enter a whole number:\n";
    std::cin >> number;

    const bool is_even{number % 2 == 0};

    if (is_even) {
        std::cout << "Even\n";
    } else {
        std::cout << "Odd\n";
    }
}
```

**Przewidź** wynik dla 8, 7 i 0, a potem sprawdź.

<!-- input: even_check -->
```text
8
```

<!-- output: even_check -->
```text
Enter a whole number:
Even
```

<!-- input: even_check -->
```text
7
```

<!-- output: even_check -->
```text
Enter a whole number:
Odd
```

<!-- input: even_check -->
```text
0
```

<details>
<summary>Standardowe wyjście dla 0</summary>

<!-- output: even_check -->
```text
Enter a whole number:
Even
```

0 jest parzyste: 0 dzieli się przez 2 bez reszty, więc `0 % 2` daje 0.

</details>

- `number % 2 == 0`: najpierw `%` oblicza resztę z dzielenia przez 2 (lekcja 2.4), potem `==` sprawdza, czy ta reszta wynosi 0. Wynik jest typu `bool`.
- `is_even` **przechowuje** ten wynik: `true` dla liczby parzystej, `false` dla nieparzystej. Wartość się nie zmienia, więc jest stałą.
- `if (is_even)` korzysta z przechowanej wartości. Warunek w `if` to po prostu wartość `bool`: blok wykonuje się, gdy jest `true`.

**Przechowana wartość nie śledzi zmian.** `is_even` zawiera odpowiedź obliczoną **w chwili inicjalizacji**. Jeśli później zmienisz `number`, `is_even` sama się nie zaktualizuje. Ten program pokazuje to, a przy okazji to, jak `std::cout` wypisuje wartość `bool`:

<!-- example: stored_bool -->
```cpp
#include <iostream>

int main() {
    int number{8};
    const bool is_even{number % 2 == 0};
    std::cout << "is_even: " << is_even << "\n";

    number = 7;
    std::cout << "number: " << number << "\n";
    std::cout << "is_even: " << is_even << "\n";

    const bool is_even_now{number % 2 == 0};
    std::cout << "is_even_now: " << is_even_now << "\n";
}
```

<details>
<summary>Wynik programu</summary>

<!-- output: stored_bool -->
```text
is_even: 1
number: 7
is_even: 1
is_even_now: 0
```

</details>

- `std::cout` domyślnie wypisuje `true` jako **`1`**, a `false` jako **`0`**. To tylko sposób pokazania wartości na ekranie: zmienna dalej jest typu `bool`, nie `int`. Jak w lekcji 2.5, wygląd na ekranie nie mówi, jakiego typu jest wartość.
- Po `number = 7;` `is_even` nadal ma `true` (wypisane jako `1`), bo przechowuje odpowiedź obliczoną dla 8. Żeby poznać odpowiedź dla nowej wartości, trzeba **ponownie** obliczyć porównanie, jak w `is_even_now`.

Zamiast wypisywać `1` i `0`, programy w tym kursie zwykle wypisują własne słowa w gałęziach `if`/`else`, jak `Even` i `Odd`.

## 6. Tekst: `==` i `!=` dla `std::string`

Wartości `std::string` porównuje się tymi samymi operatorami. Porównywany jest **tekst**: czy oba napisy mają te same znaki w tej samej kolejności.

<!-- example: word_check -->
```cpp
#include <iostream>
#include <string>

int main() {
    const std::string expected_answer{"comet"};
    std::string answer{""};

    std::cout << "Enter the answer:\n";
    std::cin >> answer;

    if (answer == expected_answer) {
        std::cout << "Correct\n";
    } else {
        std::cout << "Incorrect\n";
    }
}
```

**Przewidź** wynik dla `comet`, `Comet` i `planet`. Potem sprawdź.

<!-- input: word_check -->
```text
comet
```

<!-- output: word_check -->
```text
Enter the answer:
Correct
```

<!-- input: word_check -->
```text
Comet
```

<details>
<summary>Standardowe wyjście dla Comet</summary>

<!-- output: word_check -->
```text
Enter the answer:
Incorrect
```

</details>

<!-- input: word_check -->
```text
planet
```

<!-- output: word_check -->
```text
Enter the answer:
Incorrect
```

- Porównanie **rozróżnia wielkość liter**: `Comet` i `comet` to różne napisy, więc odpowiedź jest „nie”. Program nie domyśla się, że chodziło o to samo słowo.
- `answer != expected_answer` dałoby `true` dla `Comet` i `planet`, a `false` dla `comet`.

**Sprawdź się.** Odpowiedz krótko, a potem porównaj z rozwiązaniami:

1. Kiedy `a == b` daje `true`? Kiedy `a != b` daje `true`?
2. Czy porównanie zmienia wartości `a` i `b`?
3. Co dają `==` i `!=` dla dwóch takich samych napisów, a co dla dwóch różnych?
4. Który zapis pasuje do każdego wymagania: `=`, `==` czy `!=`?

| Wymaganie | Zapis |
|---|---|
| Ustaw liczbę punktów na 0. | |
| Sprawdź, czy liczba punktów wynosi 0. | |
| Sprawdź, czy odpowiedź jest inna niż `comet`. | |
| Zmień odpowiedź na `comet`. | |
| Sprawdź, czy liczba jest nieparzysta. | |

## 7. Dwie niezależne decyzje

Program może mieć kilka konstrukcji `if`/`else`. Każda podejmuje **własną** decyzję:

<!-- example: weather_report -->
```cpp
#include <iostream>

int main() {
    int temperature_c{0};
    int wind_kmh{0};

    std::cout << "Enter temperature:\n";
    std::cin >> temperature_c;
    std::cout << "Enter wind speed in km/h:\n";
    std::cin >> wind_kmh;

    if (temperature_c >= 20) {
        std::cout << "Warm\n";
    } else {
        std::cout << "Cold\n";
    }

    if (wind_kmh > 30) {
        std::cout << "Windy\n";
    } else {
        std::cout << "Calm\n";
    }
}
```

**Przewidź** dwie ostatnie linijki dla temperatury 25 i wiatru 10, dla temperatury 15 i wiatru 40 oraz dla przypadku na granicach: temperatura 20, wiatr 30.

<!-- input: weather_report -->
```text
25
10
```

<!-- output: weather_report -->
```text
Enter temperature:
Enter wind speed in km/h:
Warm
Calm
```

<!-- input: weather_report -->
```text
15
40
```

<!-- output: weather_report -->
```text
Enter temperature:
Enter wind speed in km/h:
Cold
Windy
```

<!-- input: weather_report -->
```text
20
30
```

<details>
<summary>Standardowe wyjście dla 20 i 30</summary>

<!-- output: weather_report -->
```text
Enter temperature:
Enter wind speed in km/h:
Warm
Calm
```

20 spełnia `>= 20`, ale 30 nie spełnia `> 30`.

</details>

W każdej konstrukcji `if`/`else` wykonuje się jedna gałąź, więc program wypisuje **jedną** linijkę o temperaturze i **jedną** o wietrze. To nie znaczy, że w całym programie wykonuje się tylko jedna gałąź: każda decyzja jest osobna.

## 8. Gdzie żyje zmienna?

Program ma zapisać wynik w zmiennej `result` i wypisać go **po** `if`/`else`. Ktoś zadeklarował `result` wewnątrz gałęzi:

<!-- broken: result_in_block at=16 errors=1 error=^use of undeclared identifier 'result'$ -->
```cpp
#include <iostream>
#include <string>

int main() {
    int score{0};

    std::cout << "Enter score:\n";
    std::cin >> score;

    if (score >= 50) {
        std::string result{"Passed"};
    } else {
        std::string result{"Not passed"};
    }

    std::cout << "Result: " << result << "\n";
}
```

1. **Przewidź**, czy ten program się zbuduje.
2. Zbuduj go.
3. Znajdź przyczynę błędu.
4. Popraw program.
5. Wyjaśnij, dlaczego poprawka działa.

Program się nie zbuduje. Kompilator zgłasza w linijce 16 `use of undeclared identifier 'result'`: nie zna nazwy `result`. Ten komunikat znasz z lekcji 1.2 i 2.1, gdzie oznaczał literówkę albo brak deklaracji. Tutaj nazwa jest zapisana poprawnie i zadeklarowana nawet dwa razy, ale **w blokach** `if` i `else`. W linijce 16, po zamykającej klamrze, żadna z tych deklaracji już nie obowiązuje.

**Reguła:** zmienna zadeklarowana wewnątrz bloku `{ }` istnieje tylko w tym bloku, od miejsca deklaracji do zamykającej klamry. Poza blokiem jej nazwa jest nieznana.

**Poprawny wzorzec:** jeśli wartość ma być potrzebna **po** `if`/`else`, zadeklaruj zmienną **przed** nim, z wartością początkową, a w gałęziach tylko **przypisz** jej odpowiednią wartość:

<!-- example: result_before_if -->
```cpp
#include <iostream>
#include <string>

int main() {
    int score{0};
    std::string result{""};

    std::cout << "Enter score:\n";
    std::cin >> score;

    if (score >= 50) {
        result = "Passed";
    } else {
        result = "Not passed";
    }

    std::cout << "Result: " << result << "\n";
}
```

<!-- input: result_before_if -->
```text
49
```

<!-- output: result_before_if -->
```text
Enter score:
Result: Not passed
```

<!-- input: result_before_if -->
```text
50
```

<!-- output: result_before_if -->
```text
Enter score:
Result: Passed
```

- `result` jest zadeklarowane w `main`, przed `if`, więc istnieje do końca `main`, także po `if`/`else`.
- W gałęziach nie ma nowej deklaracji, tylko przypisanie (lekcja 2.2). `result` nie może więc być `const`: jego wartość zmienia się w gałęzi.
- Jeśli wynik wystarczy **wypisać** w gałęzi, jak w punkcie 2, dodatkowa zmienna nie jest potrzebna. Twórz ją tylko wtedy, gdy wartość jest potrzebna później.

## 9. Misja: mini quiz

Napisz program z krótkim quizem z dwoma pytaniami:

1. Użytkownik podaje jedno słowo: nazwę drogi, po której planeta krąży wokół Słońca. Poprawna odpowiedź to `orbit`.
2. Użytkownik podaje liczbę całkowitą. Program sprawdza, czy jest parzysta.

Program ocenia **każde pytanie osobno**.

W `cpp-workspace` utwórz katalog `mini_quiz`, skopiuj do niego `CMakeLists.txt` z oryginalnego `lesson_05_first_program`, utwórz pusty `main.cpp` i napisz program samodzielnie. Najpierw odczytaj słowo, potem liczbę. Oba odczyty przez `std::cin >>` wystarczą, bo słowo jest jedno.

Dla danych `orbit` i `4` standardowe wyjście ma być takie:

<!-- input: mini_quiz -->
```text
orbit
4
```

<!-- output: mini_quiz -->
```text
Name the path of a planet around the Sun:
Enter a whole number:
Answer: correct
Number: even
```

Program ma dawać poprawny wynik dla wszystkich tych zestawów, bez zmiany kodu:

| Słowo | Liczba | Oczekiwane dwie ostatnie linijki |
|---|---|---|
| `orbit` | `4` | `Answer: correct`, `Number: even` |
| `orbit` | `7` | `Answer: correct`, `Number: odd` |
| `planet` | `10` | `Answer: incorrect`, `Number: even` |
| `Orbit` | `3` | `Answer: incorrect`, `Number: odd` |
| `orbit` | `0` | `Answer: correct`, `Number: even` |

<!-- input: mini_quiz -->
```text
orbit
7
```

<!-- output: mini_quiz -->
```text
Name the path of a planet around the Sun:
Enter a whole number:
Answer: correct
Number: odd
```

<details>
<summary>Pozostałe trzy przypadki testowe: standardowe wyjście</summary>

<!-- input: mini_quiz -->
```text
planet
10
```

<!-- output: mini_quiz -->
```text
Name the path of a planet around the Sun:
Enter a whole number:
Answer: incorrect
Number: even
```

<!-- input: mini_quiz -->
```text
Orbit
3
```

<!-- output: mini_quiz -->
```text
Name the path of a planet around the Sun:
Enter a whole number:
Answer: incorrect
Number: odd
```

<!-- input: mini_quiz -->
```text
orbit
0
```

<!-- output: mini_quiz -->
```text
Name the path of a planet around the Sun:
Enter a whole number:
Answer: correct
Number: even
```

</details>

### Kryterium sukcesu

- Program buduje się jako C++20, a jego standardowe wyjście dla wszystkich pięciu zestawów jest dokładnie takie jak w tabeli i blokach powyżej.
- Odpowiedź jest typu `std::string`, liczba typu `int`, a oczekiwane słowo to stała `const std::string`.
- Słowo jest porównane przez `==`, a parzystość sprawdzona przez `%` i `==`.
- Przynajmniej jeden wynik porównania jest zapisany w zmiennej `bool`.
- Są dwie **osobne** konstrukcje `if`/`else`, każda z klamrami.
- Ten sam program daje wszystkie wyniki, bez zmiany kodu.
- Umiesz wyjaśnić, dlaczego `Orbit` jest oceniane jako niepoprawne i dlaczego 0 jest parzyste.

Gdy wynik się zgadza, możesz zapisać projekt w Gicie, jak w lekcji 1.5.

<details>
<summary>Podpowiedź 1</summary>

Dwa pytania to dwie osobne decyzje, jak w punkcie 7. Każda ma swoje `if`/`else` i wypisuje jedną z dwóch linijek.

</details>

<details>
<summary>Podpowiedź 2</summary>

Wynik porównania słowa i wynik sprawdzenia parzystości możesz zapisać w stałych `bool` z sensownymi nazwami, jak `is_even` w punkcie 5, i użyć ich jako warunków.

</details>

Przykładowe rozwiązanie jest w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 10. Gdy coś pójdzie inaczej

| Co widzisz | Co to znaczy | Co zrobić |
|---|---|---|
| Wykonały się obie gałęzie | Druga gałąź nie jest połączona z `if` przez `else`, na przykład stoi po prostu za blokiem. | Gałąź alternatywna to `else { … }` zaraz za zamykającą klamrą bloku `if`. |
| Błąd kompilacji przy `else` | `else` nie stoi zaraz po bloku `if`, albo ktoś dopisał przy nim warunek. | `else` nie ma warunku i musi następować bezpośrednio po `}` bloku `if`. |
| Zmienna ma nagle inną wartość, choć miała być tylko sprawdzona | W miejscu porównania jest przypisanie `=`. | Do sprawdzania równości służy `==`, dwa znaki. |
| Słowo wygląda na poprawne, a program mówi `incorrect` | Porównanie rozróżnia wielkość liter. | `Orbit` i `orbit` to różne napisy. Wpisz słowo dokładnie tak, jak oczekuje program. |
| Na ekranie jest `1` albo `0` zamiast słowa | Program wypisał wartość `bool`. | To domyślny sposób wypisywania `true` i `false`. Wypisuj słowa w gałęziach `if`/`else`. |
| Zmienna `bool` ma „starą” odpowiedź | Przechowuje wynik obliczony przy inicjalizacji. Nie śledzi późniejszych zmian. | Oblicz porównanie ponownie po zmianie danych. |
| `use of undeclared identifier` dla zmiennej z `if` | Zmienna jest zadeklarowana w bloku, a używana poza nim. | Zadeklaruj ją przed `if`, a w gałęziach tylko przypisuj (punkt 8). |

## 11. Wyjaśnij

Odpowiedz własnymi słowami, najlepiej na piśmie. Dopiero potem porównaj z przykładową odpowiedzią.

**1.** Czym różni się samo `if` od `if`/`else`?

<details>
<summary>Przykładowa odpowiedź</summary>

Samo `if` wykonuje blok albo nic nie robi. `if`/`else` zawsze wykonuje dokładnie jedną z dwóch gałęzi: blok `if`, gdy warunek jest spełniony, albo blok `else`, gdy nie jest.

</details>

**2.** Czym różni się `count = 5;` od `count == 5`?

<details>
<summary>Przykładowa odpowiedź</summary>

`count = 5;` zapisuje w `count` wartość 5. `count == 5` tylko sprawdza, czy `count` jest równe 5, i daje `true` albo `false`. Niczego nie zmienia.

</details>

**3.** Co przechowuje `const bool is_even{number % 2 == 0};` i czy zmieni się, gdy później zmienisz `number`?

<details>
<summary>Przykładowa odpowiedź</summary>

Przechowuje `true`, jeśli `number` było parzyste w chwili inicjalizacji, a w przeciwnym razie `false`. Nie zmieni się: to zapisana odpowiedź, a nie reguła. Po zmianie `number` trzeba ponownie obliczyć porównanie.

</details>

**4.** Program wypisał `is_even: 1`. Czy `is_even` jest typu `int`?

<details>
<summary>Przykładowa odpowiedź</summary>

Nie. `is_even` jest typu `bool`. `std::cout` domyślnie wypisuje `true` jako `1`, a `false` jako `0`. Typ odczytuje się z kodu.

</details>

**5.** Dlaczego program z punktu 8 się nie zbudował i jak to naprawiono?

<details>
<summary>Przykładowa odpowiedź</summary>

`result` było zadeklarowane wewnątrz bloków `if` i `else`, więc istniało tylko w nich. Po `if`/`else` ta nazwa była nieznana. Poprawka deklaruje `result` przed `if`, a w gałęziach tylko przypisuje mu wartość.

</details>

## Podsumowanie

- `if`/`else` wybiera **jedną z dwóch** gałęzi. `else` nie ma warunku i wykonuje się, gdy warunek przy `if` nie jest spełniony. Po wybranej gałęzi program idzie dalej.
- `==` sprawdza równość, a `!=` nierówność, także dla `std::string`. Porównanie niczego nie zmienia. `=` to przypisanie, czyli inna operacja.
- Porównanie `std::string` rozróżnia wielkość liter.
- Wynik porównania jest typu `bool`: `true` albo `false`. Można go zapisać w zmiennej i użyć jako warunku. Zapisana wartość nie śledzi późniejszych zmian danych.
- `std::cout` wypisuje `bool` domyślnie jako `1` albo `0`. Zmienna nadal jest typu `bool`.
- Zmienna zadeklarowana w bloku istnieje tylko w nim. Wartość potrzebną po `if`/`else` deklaruj przed nim i przypisuj w gałęziach.
- Kilka osobnych `if`/`else` podejmuje kilka osobnych decyzji.

## Co dalej

Twój program wybiera już jedną z dwóch dróg. Czasem jednak możliwości jest więcej: ocena może być A, B, C albo D. W lekcji 3.3 poznasz `else if` i nauczysz się sprawdzać wszystkie granice takich przedziałów. **Lekcja 3.3 jest w przygotowaniu.**

---

## Przykładowe rozwiązania

Zajrzyj tutaj **po własnej próbie**. Twoje nazwy mogą się różnić, jeśli standardowe wyjście jest takie, jak wymagane.

<details>
<summary>Punkt 6: sprawdź się</summary>

1. `a == b` daje `true`, gdy wartości są równe. `a != b` daje `true`, gdy są różne.
2. Nie. Porównanie tylko sprawdza i daje `true` albo `false`.
3. Dla dwóch takich samych napisów `==` daje `true`, a `!=` daje `false`. Dla dwóch różnych odwrotnie: `==` daje `false`, a `!=` daje `true`.
4. Zapisy:

| Wymaganie | Zapis |
|---|---|
| Ustaw liczbę punktów na 0. | `points = 0;` |
| Sprawdź, czy liczba punktów wynosi 0. | `points == 0` |
| Sprawdź, czy odpowiedź jest inna niż `comet`. | `answer != "comet"` |
| Zmień odpowiedź na `comet`. | `answer = "comet";` |
| Sprawdź, czy liczba jest nieparzysta. | `number % 2 != 0` |

</details>

<details>
<summary>Punkt 9: misja, mini quiz</summary>

<!-- example: mini_quiz -->
```cpp
#include <iostream>
#include <string>

int main() {
    const std::string expected_answer{"orbit"};
    std::string answer{""};
    int number{0};

    std::cout << "Name the path of a planet around the Sun:\n";
    std::cin >> answer;
    std::cout << "Enter a whole number:\n";
    std::cin >> number;

    const bool is_correct{answer == expected_answer};
    const bool is_even{number % 2 == 0};

    if (is_correct) {
        std::cout << "Answer: correct\n";
    } else {
        std::cout << "Answer: incorrect\n";
    }

    if (is_even) {
        std::cout << "Number: even\n";
    } else {
        std::cout << "Number: odd\n";
    }
}
```

- `answer` to tekst, więc `std::string`. `number` to liczba całkowita, więc `int`. Oczekiwane słowo się nie zmienia, więc jest stałą.
- `is_correct` i `is_even` przechowują wyniki dwóch porównań. Dane się po nich nie zmieniają, więc mogą być stałymi.
- Dwie osobne konstrukcje `if`/`else` podejmują dwie osobne decyzje. Każda wypisuje jedną linijkę.

</details>

**Poprzednia lekcja:** [Lekcja 3.1: Pierwsza decyzja programu (`if`)](lesson_01_the_first_decision.md) · **Następna lekcja:** w przygotowaniu · [Opis kursu](../../README.md)

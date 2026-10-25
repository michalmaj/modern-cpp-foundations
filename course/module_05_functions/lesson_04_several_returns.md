# Lekcja 5.4: Kilka dróg do `return`

**Polski** · [English](lesson_04_several_returns.en.md) · [Opis kursu](../../README.md)

> **Moduł 5, lekcja 4** · około 70–90 minut
> **Potrzebujesz:** katalogu `cpp-workspace` i oryginalnego projektu `lesson_05_first_program`, jak dotąd. Debugger nie jest w tej lekcji potrzebny.
> **Wersja pilotażowa.** Programy z tej lekcji sprawdzamy automatycznie na Windowsie, Ubuntu i macOS, także z podanymi danymi wejściowymi. Wpisywanie danych w oknie **Run** CLiona opisujemy bez ręcznego sprawdzenia na każdym systemie.

## Zanim zaczniesz

Ta lekcja zakłada, że po lekcji 5.3:

- piszesz funkcje z typem wyniku i jednym `return` na końcu;
- wiesz, że wykonanie `return` kończy wywołanie funkcji i przekazuje wynik;
- piszesz łańcuchy `if` i `else if` oraz łączysz warunki przez `&&` i `||` (lekcje 3.3 i 3.4);
- używasz zmiennych typu `std::string` (lekcja 2.7).

## Sytuacja

W lekcji 5.3 każda funkcja liczyła wynik zawsze tym samym wzorem. Często jednak wynik **zależy od danych**: dla jednych wartości funkcja ma zwrócić jedno, dla innych coś zupełnie innego. W tej lekcji funkcja podejmie decyzję i zakończy działanie w miejscu, które pasuje do otrzymanych danych.

Po tej lekcji będziesz:

- pisać funkcje z kilkoma instrukcjami `return`;
- przewidywać, który `return` wykona się dla danego argumentu;
- wyjaśniać, dlaczego po wykonanym `return` dalsze warunki nie są sprawdzane;
- stosować klauzulę ochronną do obsłużenia szczególnego przypadku;
- zwracać tekst typu `std::string`;
- znajdować błędy kolejności warunków i dobierać przypadki, które je ujawniają;
- rozpoznawać funkcję, w której jedna ze ścieżek nie zwraca wyniku;
- projektować funkcję klasyfikującą z regułami o ustalonym pierwszeństwie.

## 1. Przygotuj projekt

W `cpp-workspace` utwórz katalog `lesson_5_4` i skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program`. Programy z punktów 2–7 wpisujesz w `main.cpp` tego katalogu.

## 2. Wynik zależy od danych

Zawody dają od 0 do 10 punktów. Funkcja ma ograniczyć wynik do tego przedziału: wartość poniżej 0 daje 0, wartość powyżej 10 daje 10, a wartość od 0 do 10 zostaje bez zmian. Jeden wzór nie wystarczy, bo wynik zależy od tego, jaką wartość funkcja dostanie:

<!-- example: limit_points -->
```cpp
#include <iostream>

int limit_points(int points) {
    if (points < 0) {
        return 0;
    }

    if (points > 10) {
        return 10;
    }

    return points;
}

int main() {
    std::cout << "-3 -> " << limit_points(-3) << "\n";
    std::cout << "0 -> " << limit_points(0) << "\n";
    std::cout << "4 -> " << limit_points(4) << "\n";
    std::cout << "10 -> " << limit_points(10) << "\n";
    std::cout << "13 -> " << limit_points(13) << "\n";
}
```

Funkcja ma **trzy** instrukcje `return`: dwie w blokach `if` i jedną na końcu.

**Przewidź** pięć linijek, zanim uruchomisz program.

<details>
<summary>Standardowe wyjście</summary>

<!-- output: limit_points -->
```text
-3 -> 0
0 -> 0
4 -> 4
10 -> 10
13 -> 10
```

</details>

To świadome **ograniczanie** wyniku do przedziału: za mały wynik staje się 0, a za duży 10. To nie jest sposób na wszystkie błędne dane. W punkcie 5 zobaczysz inny model: funkcja rozpozna niedopuszczalną wartość i zwróci o tym komunikat.

## 3. Który `return` się wykona?

Prześledź wywołania `limit_points(-3)`, `limit_points(4)` i `limit_points(13)`. Przepisz tabelę i ją wypełnij:

| Argument | `points < 0` | `points > 10` | Który `return` się wykonał | Wynik |
|---|---|---|---|---|
| -3 | | | | |
| 4 | | | | |
| 13 | | | | |

<details>
<summary>Wypełniona tabela i wyjaśnienie</summary>

| Argument | `points < 0` | `points > 10` | Który `return` się wykonał | Wynik |
|---|---|---|---|---|
| -3 | `true` | **nie jest sprawdzany** | `return 0;` w pierwszym `if` | 0 |
| 4 | `false` | `false` | końcowe `return points;` | 4 |
| 13 | `false` | `true` | `return 10;` w drugim `if` | 10 |

- **Dla -3** pierwszy warunek jest prawdziwy, więc wykonuje się `return 0;`. Funkcja **natychmiast kończy działanie**: drugi warunek nie jest już sprawdzany, a miejsce wywołania dostaje 0.
- **Dla 4** oba warunki są fałszywe, więc program dochodzi do końcowego `return points;`.
- **Dla 13** pierwszy warunek jest fałszywy, drugi prawdziwy: wykonuje się `return 10;`.

</details>

**W funkcji może być kilka instrukcji `return`, ale w jednym wywołaniu wykonuje się tylko jedna z nich: pierwsza, do której dojdzie program.** Funkcja nie przechodzi wszystkich ścieżek, żeby potem wybrać wynik. Idzie od góry, sprawdza warunki po kolei i kończy się na pierwszym wykonanym `return`.

## 4. Klauzula ochronna

Często funkcja ma jeden **szczególny przypadek**, który trzeba obsłużyć inaczej niż resztę. Na przykład liczba minut nie może być ujemna, a dla ujemnej wartości funkcja ma zwrócić 0. Taki przypadek można sprawdzić **na początku** i od razu zakończyć funkcję:

<!-- fragment -->
```cpp
int seconds_from_minutes(int minutes) {
    if (minutes < 0) {
        return 0;
    }

    return minutes * 60;
}
```

To **klauzula ochronna** (ang. *guard clause*): wcześniejsze sprawdzenie sytuacji, która wymaga osobnego zakończenia funkcji. To nie jest nowa instrukcja C++, tylko sposób ułożenia znanych `if` i `return`. Po obsłużeniu szczególnego przypadku reszta funkcji zajmuje się już tylko zwykłymi danymi i nie musi stać w dodatkowym `else`.

Ta sama funkcja może też wyglądać tak:

<!-- fragment -->
```cpp
int seconds_from_minutes(int minutes) {
    if (minutes < 0) {
        return 0;
    } else {
        return minutes * 60;
    }
}
```

Obie wersje są poprawne i zwracają te same wyniki. `else` po `return` nie jest błędem. Klauzula ochronna to narzędzie czytelności: przydaje się zwłaszcza wtedy, gdy po obsłużeniu szczególnego przypadku zostaje dłuższa reszta funkcji.

## 5. Wynik typu `std::string`

Funkcja może zwracać tekst. Ta funkcja opisuje postęp pracy z 10 etapów:

<!-- example: progress_status -->
```cpp
#include <iostream>
#include <string>

std::string progress_status(int completed) {
    if (completed < 0 || completed > 10) {
        return "Invalid progress";
    }

    if (completed == 10) {
        return "Complete";
    }

    if (completed >= 5) {
        return "In progress";
    }

    return "Getting started";
}

int main() {
    const std::string status{progress_status(5)};
    std::cout << "5: " << status << "\n";

    std::cout << "-1: " << progress_status(-1) << "\n";
    std::cout << "0: " << progress_status(0) << "\n";
    std::cout << "4: " << progress_status(4) << "\n";
    std::cout << "9: " << progress_status(9) << "\n";
    std::cout << "10: " << progress_status(10) << "\n";
    std::cout << "11: " << progress_status(11) << "\n";
}
```

- Typ wyniku to `std::string`, znany Ci z lekcji 2.7. Funkcja potrzebuje nagłówka `<string>`.
- Pierwszy `if` to klauzula ochronna: niedopuszczalna liczba etapów od razu daje `Invalid progress`, a dalsze reguły już jej nie dotyczą.
- Każdy wykonany `return` kończy wywołanie i przekazuje jeden tekst.
- Funkcja **niczego nie wypisuje**. Zwrócony tekst można zapisać w zmiennej, jak `status`, albo od razu wypisać przez `std::cout` w `main`.

**Przewidź** siedem linijek. Dla każdej wskaż, który `return` się wykonał.

<details>
<summary>Standardowe wyjście</summary>

<!-- output: progress_status -->
```text
5: In progress
-1: Invalid progress
0: Getting started
4: Getting started
9: In progress
10: Complete
11: Invalid progress
```

</details>

**Typ wyniku obowiązuje każdy `return`.** W tym programie ktoś zostawił typ wyniku `int`, choć funkcja zwraca tekst:

<!-- broken: wrong_result_type at=6:16 errors=2 error=^cannot initialize return object of type 'int' -->
```cpp
#include <iostream>
#include <string>

int progress_status(int completed) {
    if (completed == 10) {
        return "Complete";
    }

    return "Not complete";
}

int main() {
    std::cout << progress_status(10) << "\n";
}
```

**Przewidź**, czy program się zbuduje. Potem spróbuj go zbudować.

<details>
<summary>Co zgłasza kompilator i dlaczego</summary>

Program się nie zbuduje. Kompilator zgłasza **dwa** błędy, po jednym dla każdego `return`. Pierwszy jest w linijce 6: `cannot initialize return object of type 'int' with an lvalue of type 'const char[9]'`. Funkcja obiecuje wynik `int`, a próbuje zwrócić tekst. Każdy `return` musi dawać wartość zgodną z typem wyniku funkcji. Poprawka to jedna zmiana. Znajdziesz ją w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

</details>

## 6. Znajdź błąd: kolejność warunków

Wymaganie jest takie samo jak w punkcie 5: 10 etapów to `Complete`, od 5 do 9 to `In progress`, od 0 do 4 to `Getting started`. W tej wersji ktoś zamienił kolejność dwóch reguł:

<!-- example: progress_order_bug -->
```cpp
#include <iostream>
#include <string>

std::string progress_status(int completed) {
    if (completed < 0 || completed > 10) {
        return "Invalid progress";
    }

    if (completed >= 5) {
        return "In progress";
    }

    if (completed == 10) {
        return "Complete";
    }

    return "Getting started";
}

int main() {
    std::cout << "4: " << progress_status(4) << "\n";
    std::cout << "5: " << progress_status(5) << "\n";
    std::cout << "9: " << progress_status(9) << "\n";
    std::cout << "10: " << progress_status(10) << "\n";
}
```

1. Przeczytaj wymaganie i zapisz poprawny wynik dla 4, 5, 9 i 10.
2. **Przewidź**, co wypisze **ten** program.
3. Uruchom go.
4. Znajdź pierwszy wynik niezgodny z wymaganiem.
5. Wyjaśnij, który `return` wykonał się zbyt wcześnie.
6. Popraw kolejność warunków.
7. Sprawdź ponownie wszystkie cztery przypadki.

Wynik przed poprawką i poprawiony program są w części [Przykładowe rozwiązania](#przykładowe-rozwiązania). Zajrzyj tam po własnej próbie.

## 7. Ścieżka bez `return`

Ta wersja `limit_points` z punktu 2 ma brakującą część. **Przeanalizuj ją na papierze, nie uruchamiaj jej:**

<!-- fragment -->
```cpp
int limit_points(int points) {
    if (points < 0) {
        return 0;
    }

    if (points > 10) {
        return 10;
    }
}
```

1. Wskaż wszystkie drogi, którymi może przejść wywołanie tej funkcji.
2. Znajdź argument, dla którego program nie trafi do żadnego `return`.
3. Wyjaśnij, dlaczego to nie jest poprawne rozwiązanie.
4. Zaproponuj brakujący `return`. Jaki wynik ma zwrócić zgodnie z wymaganiem?

<details>
<summary>Omówienie</summary>

- Są trzy drogi: argument poniżej 0 trafia do `return 0;`, argument powyżej 10 do `return 10;`, a argument od 0 do 10, na przykład 4, omija oba `if` i dochodzi do zamykającej klamry funkcji **bez żadnego `return`**.
- Funkcja obiecuje wynik `int`, ale dla takich argumentów go nie przekazuje. Kompilator może zgłosić ostrzeżenie, a program może się mimo to zbudować. Wywołanie, które dojdzie do końca funkcji bez `return`, ma jednak **niezdefiniowane zachowanie**: jego wynik nie jest określony i nie można na nim polegać. Szczególna reguła z lekcji 5.3 dotyczy tylko `main`. Zwykła funkcja nie dostaje automatycznie wyniku 0.
- **Brakujący `return`:** `return points;` na końcu, bo wartości od 0 do 10 mają zostać bez zmian. Końcowy `return` musi zwracać wynik zgodny z wymaganiem. Samo dopisanie dowolnego `return`, żeby kompilator przestał ostrzegać, nie wystarczy.

</details>

**Dla każdej możliwej drogi wykonania funkcja zwracająca wartość musi dostarczyć poprawny wynik.**

## 8. Misja: status kolejki

Punkt usługowy pokazuje na ekranie status kolejki. Program dostaje liczbę osób oczekujących i liczbę dostępnych stanowisk, a funkcja ustala status. To uproszczony model do ćwiczenia, a nie prawdziwy system kolejkowy.

**Dane:**

- liczba osób oczekujących: liczba całkowita od 0 do 12 włącznie;
- liczba dostępnych stanowisk: liczba całkowita od 0 do 4 włącznie.

**Reguły**, w tej kolejności pierwszeństwa:

1. Jeśli którakolwiek wartość jest spoza zakresu, status to `Invalid queue data`. Ta reguła ma pierwszeństwo przed wszystkimi pozostałymi.
2. Jeśli nikt nie czeka, status to `Queue empty`, także wtedy, gdy nie ma żadnego stanowiska.
3. Jeśli ktoś czeka, ale nie ma żadnego stanowiska, status to `No desks available`.
4. Jeśli liczba osób oczekujących jest **większa niż** trzykrotność liczby stanowisk, status to `Busy queue`. Chodzi o „większa niż”, a nie „większa lub równa”.
5. We wszystkich pozostałych poprawnych przypadkach status to `Manageable queue`.

Do tych samych danych może pasować kilka reguł. Wtedy obowiązuje ta, która stoi wyżej na liście.

**Wymagania programu:**

- Program wypisuje `Enter waiting people and available desks:` i odczytuje dwie liczby całkowite: liczbę osób, potem liczbę stanowisk.
- Jeśli nie udało się odczytać obu liczb, wypisuje tylko `Input could not be read` i nie ustala statusu. Nie pyta ponownie.
- W przeciwnym razie wypisuje jedną linijkę: `Queue status: STATUS`, gdzie `STATUS` to tekst zwrócony przez funkcję.
- Status ustala **Twoja własna funkcja**, która przyjmuje dwa parametry `int` i zwraca `std::string`. Stosuje reguły 1–5, także sprawdzenie zakresów, i ma kilka instrukcji `return`. Niczego nie wypisuje i niczego nie odczytuje. Nazwy funkcji i parametrów oraz kolejność parametrów wybierasz samodzielnie.
- `main` odpowiada za pytanie, odczyt, sprawdzenie, czy odczyt się udał, wywołanie funkcji i wypisanie raportu. Nie powtarza reguł klasyfikacji.
- Nie używaj zmiennych zadeklarowanych poza funkcjami.

W `cpp-workspace` utwórz katalog `queue_status`, skopiuj do niego `CMakeLists.txt` z oryginalnego `lesson_05_first_program`, utwórz pusty `main.cpp` i napisz program samodzielnie.

Dla danych `4` i `1` standardowe wyjście ma być takie:

<!-- input: queue_status -->
```text
4
1
```

<!-- output: queue_status -->
```text
Enter waiting people and available desks:
Queue status: Busy queue
```

**Przewidź**, zanim napiszesz program: jaki status wypisze on dla danych `0`, `0`, a jaki dla `3`, `1`?

<!-- input: queue_status -->
```text
0
0
```

<details>
<summary>Standardowe wyjście dla 0 i 0</summary>

<!-- output: queue_status -->
```text
Enter waiting people and available desks:
Queue status: Queue empty
```

Pasują tu dwie reguły: nikt nie czeka (reguła 2) i nie ma stanowisk (reguła 3). Wygrywa reguła 2, bo stoi wyżej.

</details>

<!-- input: queue_status -->
```text
3
1
```

<details>
<summary>Standardowe wyjście dla 3 i 1</summary>

<!-- output: queue_status -->
```text
Enter waiting people and available desks:
Queue status: Manageable queue
```

3 osoby to dokładnie trzykrotność jednego stanowiska, a nie więcej, więc reguła 4 nie pasuje.

</details>

**To nie jest `progress_status` z nowymi napisami.** Tam była jedna wartość i progi na jednej osi. Tutaj funkcja dostaje **dwie wartości o różnych rolach**, a reguły mogą się nakładać: niektóre dane pasują do kilku reguł naraz. Musisz samodzielnie zdecydować:

1. jak nazwać funkcję i parametry i w jakiej kolejności je przyjmować;
2. jak sprawdzić oba zakresy i jak ta reguła wpływa na pozostałe;
3. w jakiej kolejności sprawdzać pozostałe reguły, żeby zawsze wygrywała właściwa;
4. co funkcja zwraca, gdy żadna wcześniejsza reguła nie pasuje;
5. jak nie wypisać statusu po nieudanym odczycie.

**Zanim napiszesz program**, przygotuj tabelę przypadków testowych. Uwzględnij przypadki, w których pasują **dwie reguły naraz**, granicę trzykrotności (dokładnie trzykrotność i o jeden więcej), wartości tuż poza oboma zakresami, także w połączeniu z zerem osób, tekst zamiast pierwszej i zamiast drugiej liczby oraz dane, które kończą się po jednej liczbie. Przy każdym przypadku zapisz oczekiwane standardowe wyjście.

Przypadki z danymi, które kończą się wcześniej, przeanalizuj na papierze, jak w lekcjach 4.5–5.3, zamiast je uruchamiać, i porównaj ze zwiniętą listą kontrolną. Program z tej lekcji jest dla takich danych sprawdzany osobno, automatycznymi testami kursu.

### Kryterium sukcesu

- Program buduje się jako C++20, a jego standardowe wyjście dla danych `4`, `1`, dla `0`, `0` i dla `3`, `1` jest dokładnie takie jak powyżej.
- Dla każdego przypadku, który możesz wpisać, standardowe wyjście zgadza się z listą kontrolną. Przypadki z danymi, które kończą się wcześniej, sprawdzasz rozumowaniem.
- Status ustala Twoja funkcja zwracająca `std::string`, z dwoma parametrami `int` i kilkoma instrukcjami `return`. Funkcja nie wypisuje i nie odczytuje niczego, a reguły nie powtarzają się w `main`.
- Dla każdych dwóch liczb całkowitych funkcja dochodzi do jakiegoś `return`.
- Po nieudanym odczycie nie pojawia się `Queue status`.
- Program nie używa zmiennych zadeklarowanych poza funkcjami.
- Tabela przypadków powstała przed uruchomieniem programu.
- Umiesz wyjaśnić, dlaczego Twoja kolejność warunków odpowiada pierwszeństwu reguł.

Gdy wynik się zgadza, możesz zapisać projekt w Gicie, jak w lekcji 1.5.

<details>
<summary>Podpowiedź 1</summary>

Które dane należy odrzucić, zanim w ogóle zaczniemy ustalać status kolejki?

</details>

<details>
<summary>Podpowiedź 2</summary>

Sprawdź przypadek z zerem osób i zerem stanowisk. Która reguła powinna wygrać, jeśli kilka warunków może pasować?

</details>

<details>
<summary>Podpowiedź 3</summary>

Po obsłużeniu szczególnych przypadków funkcja może zwrócić wynik dla wszystkich pozostałych poprawnych danych. Każdy wykonany `return` kończy jej działanie.

</details>

<details>
<summary>Pełna lista przypadków kontrolnych: otwórz po przygotowaniu własnej tabeli</summary>

| Osoby | Stanowiska | Status | Co sprawdza |
|---|---|---|---|
| 4 | 1 | `Busy queue` | o jeden więcej niż trzykrotność |
| 0 | 0 | `Queue empty` | reguła 2 przed regułą 3 |
| 3 | 1 | `Manageable queue` | dokładnie trzykrotność |
| 0 | 4 | `Queue empty` | pusta kolejka przy stanowiskach |
| 1 | 0 | `No desks available` | brak stanowisk |
| 12 | 0 | `No desks available` | brak stanowisk przy pełnej kolejce |
| 1 | 1 | `Manageable queue` | zwykłe obciążenie |
| 2 | 2 | `Manageable queue` | zwykłe obciążenie |
| 12 | 4 | `Manageable queue` | górne granice, dokładnie trzykrotność |
| 12 | 3 | `Busy queue` | przekroczona trzykrotność |
| -1 | 2 | `Invalid queue data` | osoby tuż pod zakresem |
| 13 | 2 | `Invalid queue data` | osoby tuż nad zakresem |
| 2 | -1 | `Invalid queue data` | stanowiska tuż pod zakresem |
| 2 | 5 | `Invalid queue data` | stanowiska tuż nad zakresem |
| 0 | 5 | `Invalid queue data` | reguła 1 przed regułą 2 |
| `abc` | `2` | `Input could not be read` | tekst zamiast pierwszej liczby |
| `2` | `abc` | `Input could not be read` | tekst zamiast drugiej liczby |
| `2` | koniec danych | `Input could not be read` | dane kończą się po jednej liczbie |
| brak danych | brak danych | `Input could not be read` | dane kończą się od razu |

W wierszach z `Input could not be read` program wypisuje tylko pytanie i ten komunikat. W pozostałych wypisuje pytanie i `Queue status: …`. Pierwsze trzy przypadki są sprawdzone wyżej, przy treści misji.

<!-- input: queue_status -->
```text
0
4
```

<!-- output: queue_status -->
```text
Enter waiting people and available desks:
Queue status: Queue empty
```

<!-- input: queue_status -->
```text
1
0
```

<!-- output: queue_status -->
```text
Enter waiting people and available desks:
Queue status: No desks available
```

<!-- input: queue_status -->
```text
12
0
```

<!-- output: queue_status -->
```text
Enter waiting people and available desks:
Queue status: No desks available
```

<!-- input: queue_status -->
```text
1
1
```

<!-- output: queue_status -->
```text
Enter waiting people and available desks:
Queue status: Manageable queue
```

<!-- input: queue_status -->
```text
2
2
```

<!-- output: queue_status -->
```text
Enter waiting people and available desks:
Queue status: Manageable queue
```

<!-- input: queue_status -->
```text
12
4
```

<!-- output: queue_status -->
```text
Enter waiting people and available desks:
Queue status: Manageable queue
```

<!-- input: queue_status -->
```text
12
3
```

<!-- output: queue_status -->
```text
Enter waiting people and available desks:
Queue status: Busy queue
```

<!-- input: queue_status -->
```text
-1
2
```

<!-- output: queue_status -->
```text
Enter waiting people and available desks:
Queue status: Invalid queue data
```

<!-- input: queue_status -->
```text
13
2
```

<!-- output: queue_status -->
```text
Enter waiting people and available desks:
Queue status: Invalid queue data
```

<!-- input: queue_status -->
```text
2
-1
```

<!-- output: queue_status -->
```text
Enter waiting people and available desks:
Queue status: Invalid queue data
```

<!-- input: queue_status -->
```text
2
5
```

<!-- output: queue_status -->
```text
Enter waiting people and available desks:
Queue status: Invalid queue data
```

<!-- input: queue_status -->
```text
0
5
```

<!-- output: queue_status -->
```text
Enter waiting people and available desks:
Queue status: Invalid queue data
```

<!-- input: queue_status -->
```text
abc
2
```

<!-- output: queue_status -->
```text
Enter waiting people and available desks:
Input could not be read
```

<!-- input: queue_status -->
```text
2
abc
```

<!-- output: queue_status -->
```text
Enter waiting people and available desks:
Input could not be read
```

<!-- input: queue_status -->
```text
2
```

<!-- output: queue_status -->
```text
Enter waiting people and available desks:
Input could not be read
```

<!-- input: queue_status -->
```text
```

<!-- output: queue_status -->
```text
Enter waiting people and available desks:
Input could not be read
```

</details>

Przykładowe rozwiązanie jest w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 9. Gdy coś pójdzie inaczej

| Co widzisz | Co to znaczy | Co zrobić |
|---|---|---|
| Wynik dla jednej wartości jest „przejmowany” przez inną regułę | Ogólniejszy warunek stoi przed bardziej szczególnym, a jego `return` kończy funkcję wcześniej (punkt 6). | Ułóż warunki według pierwszeństwa. Sprawdź przypadek, do którego pasują dwie reguły. |
| Niedopuszczalne dane dostają zwykły status | Sprawdzenie zakresu stoi za inną regułą albo pomija jedną z wartości. | Sprawdzenie zakresu obu wartości zrób na początku funkcji, jako klauzulę ochronną. |
| Ostrzeżenie, że funkcja nie zwraca wartości we wszystkich ścieżkach | Jakaś droga przez funkcję nie kończy się `return` (punkt 7). | Znajdź argument, który omija wszystkie `return`, i dopisz wynik zgodny z wymaganiem. |
| `cannot initialize return object of type …` | `return` zwraca wartość innego typu niż typ wyniku funkcji (punkt 5). | Każdy `return` musi dawać wartość zgodną z typem wyniku. |
| Błąd kompilacji przy `std::string` | Brakuje nagłówka `<string>`. | Dopisz `#include <string>`. |
| Dla 3 osób i 1 stanowiska status to `Busy queue` | Warunek używa `>=` zamiast `>`. | Reguła mówi „większa niż”. Sprawdź dokładnie trzykrotność. |
| Po nieudanym odczycie pojawia się status | Funkcja jest wywoływana przed sprawdzeniem odczytu albo poza gałęzią udanego odczytu. | Wywołuj funkcję tylko wtedy, gdy oba odczyty się udały. |
| Program nic nie robi i czeka | Czeka na kolejną liczbę, jak w lekcji 2.6. | Wpisz liczbę i naciśnij **Enter**. Przypadku z końcem danych nie sprawdzaj w ten sposób: prześledź go na papierze. |

## 10. Wyjaśnij

Odpowiedz własnymi słowami, najlepiej na piśmie. Dopiero potem porównaj z przykładowymi odpowiedziami.

1. Czy funkcja może zawierać kilka instrukcji `return`?
2. Ile z nich wykonuje się podczas jednego wywołania?
3. Co dzieje się po wykonaniu `return`?
4. Dlaczego późniejszy warunek może nigdy nie zostać sprawdzony?
5. Co oznacza klauzula ochronna?
6. Czy jest ona nową konstrukcją języka C++?
7. Czy `else` po `return` jest zawsze błędne?
8. Dlaczego kolejność warunków wpływa na wynik?
9. Co się stanie, jeśli istnieje ścieżka bez zwrócenia wartości?
10. Czy zwykła funkcja zwracająca `int` automatycznie zwraca zero?
11. Czy funkcja może zwracać `std::string`?
12. Czy musi wtedy wypisywać tekst?
13. Dlaczego funkcja klasyfikująca nie musi wiedzieć, jak wczytano dane?
14. Dlaczego niepoprawne dane sprawdzamy przed innymi regułami?
15. Dlaczego potrzebujemy testów, w których pasują dwa warunki naraz?
16. Jaki wynik ma zwrócić funkcja, jeśli wszystkie szczególne warunki są fałszywe?

<details>
<summary>Przykładowe odpowiedzi</summary>

1. Tak, na przykład `limit_points` ma trzy.
2. Tylko jedna: pierwsza, do której program dojdzie w tym wywołaniu.
3. Wywołanie funkcji natychmiast się kończy, a wynik trafia do miejsca wywołania. Dalsze instrukcje funkcji nie wykonują się.
4. Bo wcześniejszy warunek był prawdziwy i jego `return` zakończył funkcję, zanim program doszedł do późniejszego warunku.
5. Wcześniejsze sprawdzenie szczególnego przypadku, na przykład niedopuszczalnych danych, z `return`, które od razu kończy funkcję. Reszta funkcji zajmuje się już tylko zwykłymi danymi.
6. Nie. To sposób ułożenia znanych `if` i `return`.
7. Nie. Obie wersje mogą być poprawne. Klauzula ochronna to wybór dla czytelności, a nie jedyny dozwolony styl.
8. Bo pierwszy prawdziwy warunek kończy funkcję swoim `return`. Jeśli ogólniejszy warunek stoi wyżej, przechwytuje dane, które powinny trafić do bardziej szczególnej reguły.
9. Dla argumentów, które przejdą tą ścieżką, wywołanie ma niezdefiniowane zachowanie. Kompilator może tylko ostrzec, a program może się zbudować, ale na jego wyniku nie można polegać.
10. Nie. Ta reguła dotyczy tylko `main` (lekcja 5.3).
11. Tak, na przykład `progress_status`. Potrzebny jest nagłówek `<string>`.
12. Nie. Zwraca tekst, a o wypisaniu decyduje miejsce wywołania.
13. Bo dostaje gotowe wartości jako argumenty. Odczyt i sprawdzenie, czy się udał, należą do `main`.
14. Bo niepoprawne dane mogłyby pasować do późniejszych reguł, na przykład 0 osób i 5 stanowisk do „pustej kolejki”. Reguła niepoprawnych danych ma pierwszeństwo, więc musi być sprawdzona najpierw.
15. Bo tylko takie testy pokazują, czy wygrywa właściwa reguła. Gdy pasuje tylko jedna reguła, zła kolejność warunków często daje poprawny wynik.
16. Wynik dla zwykłego przypadku, który pasuje do wymagań: w misji `Manageable queue`, w `limit_points` niezmienione `points`.

</details>

## Podsumowanie

- Funkcja może mieć **kilka instrukcji `return`**. W jednym wywołaniu wykonuje się tylko jedna: pierwsza, do której dojdzie program.
- **Wykonany `return` natychmiast kończy wywołanie.** Dalsze warunki i instrukcje funkcji nie są już sprawdzane ani wykonywane.
- **Klauzula ochronna** to wcześniejsze sprawdzenie szczególnego przypadku z `return` na początku funkcji. To sposób ułożenia znanych `if` i `return`, a nie nowa instrukcja. Wersja z `else` też jest poprawna.
- **Kolejność warunków ma znaczenie.** Każdy warunek może być poprawny osobno, a funkcja i tak da zły wynik, jeśli ogólniejsza reguła stoi przed bardziej szczególną.
- Testuj przypadki, w których **pasują dwie reguły naraz**, i granice, na przykład „dokładnie trzykrotność”.
- Funkcja może zwracać `std::string`. Każdy `return` musi dawać wartość zgodną z typem wyniku.
- **Każda droga przez funkcję zwracającą wartość musi kończyć się `return` z poprawnym wynikiem.** Brak `return` na jakiejś drodze to niezdefiniowane zachowanie, nawet jeśli kompilator tylko ostrzega.

## Co dalej

Twoje funkcje potrafią już przyjmować dane, podejmować decyzje i zwracać wyniki. W kolejnej lekcji zbudujesz program z kilku współpracujących funkcji, z których każda ma własne zadanie: [Lekcja 5.5: Kilka funkcji, jeden program](lesson_05_several_functions.md).

---

## Przykładowe rozwiązania

Zajrzyj tutaj **po własnej próbie**. Twoje nazwy mogą się różnić, jeśli standardowe wyjście jest takie, jak wymagane.

<details>
<summary>Punkt 5: poprawiony typ wyniku</summary>

Wystarczy zmienić typ wyniku z `int` na `std::string`. Nagłówek `<string>` już jest w programie:

<!-- example: right_result_type -->
```cpp
#include <iostream>
#include <string>

std::string progress_status(int completed) {
    if (completed == 10) {
        return "Complete";
    }

    return "Not complete";
}

int main() {
    std::cout << progress_status(10) << "\n";
}
```

<!-- output: right_result_type -->
```text
Complete
```

</details>

<details>
<summary>Punkt 6: wynik przed poprawką i poprawiony program</summary>

Przed poprawką:

<!-- output: progress_order_bug -->
```text
4: Getting started
5: In progress
9: In progress
10: In progress
```

- **Dla 4, 5 i 9** wyniki są poprawne. Te przypadki nie ujawniają błędu.
- **Dla 10** wymaganie mówi `Complete`, a program wypisuje `In progress`.
- **Przyczyna:** warunek `completed >= 5` jest prawdziwy także dla 10. Stoi wyżej, więc jego `return "In progress";` kończy funkcję, zanim program dojdzie do `completed == 10`. Ta reguła nigdy nie jest osiągana. Każdy warunek z osobna jest poprawny, ale kolejność nie.
- **Poprawka:** sprawdź `completed == 10` przed `completed >= 5`.

<!-- example: progress_order_fixed -->
```cpp
#include <iostream>
#include <string>

std::string progress_status(int completed) {
    if (completed < 0 || completed > 10) {
        return "Invalid progress";
    }

    if (completed == 10) {
        return "Complete";
    }

    if (completed >= 5) {
        return "In progress";
    }

    return "Getting started";
}

int main() {
    std::cout << "4: " << progress_status(4) << "\n";
    std::cout << "5: " << progress_status(5) << "\n";
    std::cout << "9: " << progress_status(9) << "\n";
    std::cout << "10: " << progress_status(10) << "\n";
}
```

<!-- output: progress_order_fixed -->
```text
4: Getting started
5: In progress
9: In progress
10: Complete
```

</details>

<details>
<summary>Punkt 8: misja, status kolejki</summary>

<!-- example: queue_status -->
```cpp
#include <iostream>
#include <string>

std::string queue_status(int waiting, int desks) {
    const bool waiting_valid{waiting >= 0 && waiting <= 12};
    const bool desks_valid{desks >= 0 && desks <= 4};

    if (!waiting_valid || !desks_valid) {
        return "Invalid queue data";
    }

    if (waiting == 0) {
        return "Queue empty";
    }

    if (desks == 0) {
        return "No desks available";
    }

    if (waiting > 3 * desks) {
        return "Busy queue";
    }

    return "Manageable queue";
}

int main() {
    int waiting_people{0};
    int available_desks{0};

    std::cout << "Enter waiting people and available desks:\n";
    std::cin >> waiting_people;
    std::cin >> available_desks;

    if (std::cin.fail()) {
        std::cout << "Input could not be read\n";
    } else {
        const std::string status{queue_status(waiting_people, available_desks)};
        std::cout << "Queue status: " << status << "\n";
    }
}
```

- **Kolejność warunków odpowiada pierwszeństwu reguł.** Klauzula ochronna dla niepoprawnych danych stoi pierwsza, więc 0 osób i 5 stanowisk daje `Invalid queue data`, a nie `Queue empty`. Pusta kolejka stoi przed brakiem stanowisk, więc 0 i 0 daje `Queue empty`.
- **`waiting > 3 * desks`** stoi po sprawdzeniu `desks == 0`. Dla zera stanowisk ta reguła i tak nie zostanie osiągnięta. Porównanie jest ścisłe: 3 osoby przy 1 stanowisku to jeszcze `Manageable queue`.
- **Końcowy `return`** obsługuje wszystkie pozostałe poprawne dane. Każda para liczb całkowitych dochodzi do jakiegoś `return`.
- **Funkcja** niczego nie wypisuje i nie wie, skąd pochodzą liczby. **`main`** sprawdza odczyt i tylko po udanym odczycie wywołuje funkcję i wypisuje raport.
- Ta kolejność nie jest jedynym poprawnym zapisem. Na przykład dwa osobne `if` sprawdzające zakresy na początku funkcji dają te same wyniki. Za to sprawdzenie `desks == 0` przed `waiting == 0` dałoby zły wynik dla 0 i 0. Liczy się, czy dla wszystkich danych wygrywa właściwa reguła.

</details>

**Poprzednia lekcja:** [Lekcja 5.3: Funkcja zwraca wynik (`return`)](lesson_03_returning_a_result.md) · **Następna lekcja:** [Lekcja 5.5: Kilka funkcji, jeden program](lesson_05_several_functions.md) · [Opis kursu](../../README.md)

# Lekcja 3.5: Sprawdzanie danych przed obliczeniami

**Polski** · [English](lesson_05_check_before_calculating.en.md) · [Opis kursu](../../README.md)

> **Moduł 3, lekcja 5** · około 75 minut
> **Potrzebujesz:** katalogu `cpp-workspace` i oryginalnego projektu `lesson_05_first_program`, jak dotąd. Debugger nie jest w tej lekcji potrzebny.
> **Wersja pilotażowa.** Programy z tej lekcji sprawdzamy automatycznie na Windowsie, Ubuntu i macOS, także z podanymi danymi wejściowymi.

## Zanim zaczniesz

Ta lekcja zakłada, że po lekcjach 3.1–3.4:

- piszesz `if`, `else` i `else if` z klamrami i łączysz warunki przez `&&`, `||` i `!`;
- wiesz, że `&&` nie oblicza prawej strony, gdy lewa jest fałszywa;
- wiesz, że zmienna zadeklarowana w bloku istnieje tylko w nim;
- pamiętasz z lekcji 2.4, że `/` i `%` na liczbach całkowitych dają pełne grupy i resztę, a dzielenia przez zero nie wolno wykonywać.

## Sytuacja

Do tej pory dane od użytkownika zawsze pasowały do zadania. Prawdziwi użytkownicy wpisują jednak także zero tam, gdzie program przez nie dzieli, albo liczbę ujemną tam, gdzie nie ma ona sensu. Dziś nauczysz się **sprawdzać dane, zanim program ich użyje**: najpierw sprawdzenie, potem decyzja, a dopiero na końcu obliczenie.

Po tej lekcji będziesz:

- wyjaśniać, dlaczego niektóre obliczenia wymagają wcześniejszego sprawdzenia wartości;
- sprawdzać dzielnik przed `/` i `%` i wykonywać obliczenie tylko w odpowiedniej gałęzi;
- odróżniać wartość poprawnie odczytaną od wartości, która spełnia wymagania zadania;
- łączyć kilka wymagań przez `&&` i pisać jeden poziom zagnieżdżonego `if`;
- wybierać między połączonym warunkiem a zagnieżdżeniem;
- korzystać w praktyce z krótkiego obliczania `&&`;
- wyjaśniać, czego takie sprawdzanie jeszcze nie obejmuje.

## 1. Przygotuj projekt

W `cpp-workspace` utwórz katalog `lesson_3_5` i skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program`. Programy z punktów 2–7 wpisujesz w `main.cpp` tego katalogu.

## 2. Cukierki dla dzieci

Organizator chce podzielić cukierki równo między dzieci. Użytkownik podaje liczbę cukierków i liczbę dzieci, a program oblicza, ile cukierków dostanie każde dziecko i ile zostanie. To zadanie dla `/` i `%` z lekcji 2.4.

**Co się stanie, jeśli liczba dzieci wynosi zero?** Z lekcji 2.4 wiesz, że w C++ **nie wolno** wykonywać dzielenia całkowitego przez zero ani obliczać reszty z dzielenia przez zero. Takie działanie ma **niezdefiniowane zachowanie**: język nie określa, co się wtedy stanie. Program może się zakończyć, wypisać cokolwiek albo zachować się inaczej na każdym komputerze. To, co zrobi akurat Twój komputer, nie mówi nic o tym, co jest poprawne. Dlatego takiego programu nie uruchamiamy, tylko piszemy go tak, żeby do dzielenia przez zero nigdy nie doszło.

## 3. Najpierw sprawdzenie, potem obliczenie

Program najpierw sprawdza dzielnik, a dzieli dopiero w gałęzi, w której wie, że dzielnik jest odpowiedni. W tym punkcie zakładamy, że liczba cukierków nie jest ujemna.

<!-- example: candy_share -->
```cpp
#include <iostream>

int main() {
    int candies{0};
    int children{0};

    std::cout << "Enter candies:\n";
    std::cin >> candies;
    std::cout << "Enter children:\n";
    std::cin >> children;

    if (children > 0) {
        const int candies_per_child{candies / children};
        const int remaining_candies{candies % children};

        std::cout << "Each child: " << candies_per_child << "\n";
        std::cout << "Remaining: " << remaining_candies << "\n";
    } else {
        std::cout << "Number of children must be positive\n";
    }
}
```

**Przewidź**, co wypisze program dla 17 cukierków i 5 dzieci, dla 20 cukierków i 4 dzieci oraz dla 12 cukierków i 0 dzieci. Potem sprawdź.

<!-- input: candy_share -->
```text
17
5
```

<!-- output: candy_share -->
```text
Enter candies:
Enter children:
Each child: 3
Remaining: 2
```

<!-- input: candy_share -->
```text
20
4
```

<!-- output: candy_share -->
```text
Enter candies:
Enter children:
Each child: 5
Remaining: 0
```

<!-- input: candy_share -->
```text
12
0
```

<details>
<summary>Standardowe wyjście dla 12 i 0</summary>

<!-- output: candy_share -->
```text
Enter candies:
Enter children:
Number of children must be positive
```

Program nie podzielił przez zero: gałąź z `/` i `%` została pominięta.

</details>

- Program **najpierw** sprawdza `children > 0`.
- Jeśli warunek jest spełniony, wykonuje obliczenia. Wtedy wiadomo już, że dzielnik jest dodatni.
- Jeśli nie jest spełniony, pomija dzielenie i wypisuje komunikat. `else` **nie naprawia** złej wartości: wybiera tylko inną drogę.
- Obliczeń nie trzeba wykonywać przed `if`. Stałe z wynikami są zadeklarowane **w bloku**, w którym są potrzebne, bo poza nim nie są używane. To zasięg blokowy z lekcji 3.2 w praktycznym zastosowaniu.

## 4. Więcej niż jedno wymaganie

Nowe wymaganie: liczba dzieci musi być **dodatnia**, a liczba cukierków **nie może być ujemna**. To dwa osobne pytania, `children > 0` i `candies >= 0`, i oba muszą dać „tak”. Znasz już `&&`:

<!-- example: candy_check -->
```cpp
#include <iostream>

int main() {
    int candies{0};
    int children{0};

    std::cout << "Enter candies:\n";
    std::cin >> candies;
    std::cout << "Enter children:\n";
    std::cin >> children;

    const bool valid_values{children > 0 && candies >= 0};

    if (valid_values) {
        const int candies_per_child{candies / children};
        const int remaining_candies{candies % children};

        std::cout << "Each child: " << candies_per_child << "\n";
        std::cout << "Remaining: " << remaining_candies << "\n";
    } else {
        std::cout << "Invalid values\n";
    }
}
```

**Przewidź** wynik dla tych par: 17 i 5, 0 i 5, 12 i 0, -3 i 4, 5 i -2. Potem sprawdź.

<!-- input: candy_check -->
```text
17
5
```

<!-- output: candy_check -->
```text
Enter candies:
Enter children:
Each child: 3
Remaining: 2
```

<!-- input: candy_check -->
```text
0
5
```

<details>
<summary>Standardowe wyjście dla 0 i 5</summary>

<!-- output: candy_check -->
```text
Enter candies:
Enter children:
Each child: 0
Remaining: 0
```

Zero cukierków to dopuszczalna sytuacja: każde dziecko dostaje zero, a nic nie zostaje.

</details>

<!-- input: candy_check -->
```text
12
0
```

<!-- output: candy_check -->
```text
Enter candies:
Enter children:
Invalid values
```

<!-- input: candy_check -->
```text
-3
4
```

<!-- output: candy_check -->
```text
Enter candies:
Enter children:
Invalid values
```

<!-- input: candy_check -->
```text
5
-2
```

<!-- output: candy_check -->
```text
Enter candies:
Enter children:
Invalid values
```

- Oba wymagania muszą być spełnione, więc `&&`.
- **Poprawny odczyt to jeszcze nie poprawne dane.** `-3` to zwykła liczba typu `int`: `std::cin` odczytał ją bez kłopotu. Dla naszego zadania ujemna liczba cukierków jest jednak niedopuszczalna. O tym decyduje warunek, a nie typ zmiennej.
- Warunek rozstrzyga, czy program przechodzi do obliczeń.

## 5. Dwa etapy decyzji: zagnieżdżony `if`

Komunikat `Invalid values` nie mówi, **która** wartość jest zła. Można zadać pytania po kolei: najpierw o dzieci, a dopiero gdy ta odpowiedź jest dobra, o cukierki. Wtedy jeden `if` stoi **wewnątrz** gałęzi drugiego:

<!-- example: candy_check_nested -->
```cpp
#include <iostream>

int main() {
    int candies{0};
    int children{0};

    std::cout << "Enter candies:\n";
    std::cin >> candies;
    std::cout << "Enter children:\n";
    std::cin >> children;

    if (children > 0) {
        if (candies >= 0) {
            const int candies_per_child{candies / children};
            const int remaining_candies{candies % children};

            std::cout << "Each child: " << candies_per_child << "\n";
            std::cout << "Remaining: " << remaining_candies << "\n";
        } else {
            std::cout << "Candy count cannot be negative\n";
        }
    } else {
        std::cout << "Number of children must be positive\n";
    }
}
```

**Przewidź** wynik dla 17 i 5, -3 i 4, 12 i 0 oraz -3 i 0, gdzie obie wartości są złe. Potem sprawdź.

<!-- input: candy_check_nested -->
```text
17
5
```

<!-- output: candy_check_nested -->
```text
Enter candies:
Enter children:
Each child: 3
Remaining: 2
```

<!-- input: candy_check_nested -->
```text
-3
4
```

<!-- output: candy_check_nested -->
```text
Enter candies:
Enter children:
Candy count cannot be negative
```

<!-- input: candy_check_nested -->
```text
12
0
```

<!-- output: candy_check_nested -->
```text
Enter candies:
Enter children:
Number of children must be positive
```

<!-- input: candy_check_nested -->
```text
-3
0
```

<details>
<summary>Standardowe wyjście dla -3 i 0</summary>

<!-- output: candy_check_nested -->
```text
Enter candies:
Enter children:
Number of children must be positive
```

Obie wartości są złe, ale program zgłasza tylko liczbę dzieci: pierwszy warunek nie jest spełniony, więc do wewnętrznego `if` program w ogóle nie dochodzi.

</details>

- Wewnętrzny `if` wykonuje się **tylko** po wejściu do gałęzi zewnętrznego `if`, czyli wtedy, gdy `children > 0`.
- Każde `else` należy do `if`, przy którego zamykającej klamrze stoi. Wewnętrzne `else` obsługuje ujemne cukierki, a zewnętrzne złą liczbę dzieci. Klamry i wcięcia pokazują tę strukturę.
- Dzięki temu program mówi **dokładniej**, która wartość nie spełnia wymagań.

**Który sposób wybrać?**

- **Jeden warunek z `&&`** (punkt 4) jest dobry, gdy wszystkie wymagania prowadzą do jednej wspólnej decyzji: obliczyć albo wypisać jeden komunikat.
- **Zagnieżdżony `if`** (punkt 5) przydaje się, gdy drugie pytanie ma sens dopiero po pierwszym albo gdy każdy przypadek ma dostać osobny komunikat.

Żaden z nich nie jest zawsze lepszy. Wybierz ten, który najprościej oddaje wymaganie. Nie zagnieżdżaj tylko po to, żeby kod wyglądał na bardziej zaawansowany.

## 6. Krótkie obliczanie w praktyce

Z lekcji 3.4 znasz regułę: `&&` nie oblicza prawej strony, gdy lewa jest fałszywa. Teraz ta reguła się przydaje. Program sprawdza, czy każde dziecko dostanie **co najmniej 3** cukierki. Zakładamy tu, że liczba cukierków nie jest ujemna.

<!-- example: enough_for_three -->
```cpp
#include <iostream>

int main() {
    int candies{0};
    int children{0};

    std::cout << "Enter candies:\n";
    std::cin >> candies;
    std::cout << "Enter children:\n";
    std::cin >> children;

    const bool enough_for_three{children > 0 && candies / children >= 3};

    if (enough_for_three) {
        std::cout << "At least 3 each\n";
    } else {
        std::cout << "Not 3 each\n";
    }
}
```

<!-- input: enough_for_three -->
```text
12
0
```

<!-- output: enough_for_three -->
```text
Enter candies:
Enter children:
Not 3 each
```

<!-- input: enough_for_three -->
```text
12
4
```

<!-- output: enough_for_three -->
```text
Enter candies:
Enter children:
At least 3 each
```

<!-- input: enough_for_three -->
```text
8
4
```

<!-- output: enough_for_three -->
```text
Enter candies:
Enter children:
Not 3 each
```

Krok po kroku:

1. C++ oblicza najpierw lewą stronę `&&`: `children > 0`.
2. Dla 0 dzieci lewa strona jest fałszywa, więc całe `&&` jest fałszywe, a prawa strona, `candies / children >= 3`, **nie jest obliczana**. Do dzielenia przez zero nie dochodzi.
3. Dla 4 dzieci lewa strona jest prawdziwa, więc program oblicza `candies / children` i sprawdza, czy wynik to co najmniej 3: dla 12 cukierków 3 (tak), dla 8 tylko 2 (nie).

Ten warunek nie sprawdza, czy liczba cukierków jest nieujemna. To osobne wymaganie, które trzeba by dopisać. Krótkie obliczanie dotyczy wbudowanych operatorów `&&` i `||`, które tu stosujesz.

**Podstawowym wzorcem pozostaje punkt 3:** sprawdź dane, a obliczenie wykonaj w odpowiedniej gałęzi. Krótkie obliczanie pokazuje, że kolejność w `&&` ma znaczenie, ale nie jest powodem, żeby ukrywać ryzykowne obliczenia w długich warunkach.

## 7. Zła wartość a nieudany odczyt

To dwa różne problemy:

- **Poprawny odczyt, niewłaściwa wartość.** Użytkownik wpisuje `0` jako liczbę dzieci. `std::cin` poprawnie odczytuje tę liczbę do zmiennej `int`, ale dla naszego zadania nie jest to dopuszczalny dzielnik. Taki przypadek **potrafisz już wykryć** przez `if`.
- **Nieudany odczyt.** Użytkownik zamiast liczby wpisuje tekst, na przykład `abc`. Wtedy odczyt liczby się **nie udaje**. To inny problem: samo sprawdzenie wartości zmiennej przez `if` nie mówi rzetelnie, czy odczyt się powiódł.

Programy w tej lekcji wykrywają tylko pierwszy przypadek. Sprawdzanie, czy odczyt się udał, i ponowne pytanie o dane poznasz w dalszej części kursu. Do tego czasu podawaj dane w postaci liczb. Program sprawdza, czy liczby pasują do zadania, ale **nie jest odporny** na dowolne dane wejściowe.

## 8. Znajdź błąd: granica przy zerze

Wymaganie z punktu 4: liczba dzieci musi być dodatnia, a liczba cukierków **nie może być ujemna**. Zero cukierków jest więc dopuszczalne. Ten program buduje się, nigdy nie dzieli przez zero, ale błędnie ocenia jeden przypadek graniczny:

<!-- example: candy_check_bug -->
```cpp
#include <iostream>

int main() {
    int candies{0};
    int children{0};

    std::cout << "Enter candies:\n";
    std::cin >> candies;
    std::cout << "Enter children:\n";
    std::cin >> children;

    const bool valid_values{children > 0 && candies > 0};

    if (valid_values) {
        const int candies_per_child{candies / children};
        const int remaining_candies{candies % children};

        std::cout << "Each child: " << candies_per_child << "\n";
        std::cout << "Remaining: " << remaining_candies << "\n";
    } else {
        std::cout << "Invalid values\n";
    }
}
```

1. Przeczytaj wymaganie i **przewidź**, co program **powinien** wypisać dla 0 cukierków i 5 dzieci.
2. Uruchom program dla 0 i 5, a także dla 17 i 5 oraz 12 i 0.
3. Znajdź warunek niezgodny z wymaganiem.
4. Popraw go.
5. Sprawdź przypadki graniczne: 0 i 5, -1 i 5, 12 i 0.

Wyniki przed poprawką i wyjaśnienie są w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

Zwróć uwagę: ten błąd nie dotyczy bezpieczeństwa obliczenia, bo `children > 0` nadal chroni przed dzieleniem przez zero. Dotyczy **wymagań zadania**: program odrzuca dane, które powinien przyjąć.

## 9. Misja: plan nauki

Program dzieli czas nauki na sesje. Użytkownik podaje łączną liczbę minut i liczbę sesji, a program oblicza, ile **pełnych** minut przypada na każdą sesję i ile minut zostaje.

Wymagania danych:

- łączna liczba minut nie może być ujemna; 0 minut jest dopuszczalne;
- liczba sesji musi być dodatnia.

Jeśli obie wartości spełniają wymagania, program wykonuje dzielenie i oblicza resztę. W przeciwnym razie wypisuje **tylko** `Invalid session data` i niczego nie oblicza. Zakładamy, że użytkownik wpisuje liczby. Nie trzeba pytać ponownie o dane.

W `cpp-workspace` utwórz katalog `study_plan`, skopiuj do niego `CMakeLists.txt` z oryginalnego `lesson_05_first_program`, utwórz pusty `main.cpp` i napisz program samodzielnie.

Dla 95 minut i 4 sesji standardowe wyjście ma być takie:

<!-- input: study_plan -->
```text
95
4
```

<!-- output: study_plan -->
```text
Enter total minutes:
Enter number of sessions:
Minutes per session: 23
Minutes left: 3
```

Dla 40 minut i 0 sesji:

<!-- input: study_plan -->
```text
40
0
```

<!-- output: study_plan -->
```text
Enter total minutes:
Enter number of sessions:
Invalid session data
```

**Zanim napiszesz program**, przygotuj tabelę przypadków. Wybierz wartości, które sprawdzą: poprawne dane z resztą i bez reszty, zero minut, zero sesji, ujemne minuty i ujemną liczbę sesji. Przy każdym przypadku zapisz oczekiwany wynik.

### Kryterium sukcesu

- Program buduje się jako C++20, a jego standardowe wyjście dla każdego przypadku jest zgodne z wymaganiami i z formatem powyżej.
- Obie liczby to zmienne `int` z wartościami początkowymi, odczytane przez `std::cin`.
- Wymagania są zapisane jako warunek (wystarczy jeden, połączony przez `&&`), a dzielenie i reszta są obliczane **tylko** w gałęzi, w której wymagania są spełnione.
- W żadnym przypadku program nie dzieli przez zero.
- Tabela przypadków powstała przed uruchomieniem programu.
- Umiesz wyjaśnić, dlaczego dla zera sesji obliczenie się nie wykonuje, a dla zera minut tak.

Gdy wynik się zgadza, możesz zapisać projekt w Gicie, jak w lekcji 1.5.

<details>
<summary>Podpowiedź 1</summary>

Ile jest wymagań i czy wszystkie prowadzą do jednej decyzji: obliczyć albo wypisać jeden komunikat? To wskazuje, czy wystarczy jeden warunek z `&&`, jak w punkcie 4.

</details>

<details>
<summary>Podpowiedź 2</summary>

Która liczba jest dzielnikiem i jaki warunek musi spełniać, żeby dzielenie było dozwolone? Czy zero minut przeszkadza w dzieleniu?

</details>

<details>
<summary>Pełna lista przypadków kontrolnych: otwórz po własnej próbie</summary>

| Minuty | Sesje | Wynik | Co sprawdza |
|---|---|---|---|
| 95 | 4 | 23 na sesję, 3 zostaje | poprawne dane, dzielenie z resztą |
| 60 | 3 | 20 na sesję, 0 zostaje | dzielenie bez reszty |
| 0 | 5 | 0 na sesję, 0 zostaje | zero minut jest dopuszczalne |
| 40 | 0 | `Invalid session data` | zerowy dzielnik |
| -1 | 3 | `Invalid session data` | ujemne minuty |
| 40 | -2 | `Invalid session data` | ujemna liczba sesji |

Przypadki 95 i 4 oraz 40 i 0 są sprawdzone wyżej, przy treści misji.

<!-- input: study_plan -->
```text
60
3
```

<!-- output: study_plan -->
```text
Enter total minutes:
Enter number of sessions:
Minutes per session: 20
Minutes left: 0
```

<!-- input: study_plan -->
```text
0
5
```

<!-- output: study_plan -->
```text
Enter total minutes:
Enter number of sessions:
Minutes per session: 0
Minutes left: 0
```

<!-- input: study_plan -->
```text
-1
3
```

<!-- output: study_plan -->
```text
Enter total minutes:
Enter number of sessions:
Invalid session data
```

<!-- input: study_plan -->
```text
40
-2
```

<!-- output: study_plan -->
```text
Enter total minutes:
Enter number of sessions:
Invalid session data
```

</details>

Przykładowe rozwiązanie jest w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 10. Gdy coś pójdzie inaczej

| Co widzisz | Co to znaczy | Co zrobić |
|---|---|---|
| Obliczenie stoi przed `if`, który sprawdza dzielnik | Dzielenie wykona się, zanim program sprawdzi dzielnik. | Przenieś obliczenie do gałęzi, w której dzielnik jest już sprawdzony. |
| Program odrzuca dopuszczalną wartość, na przykład 0 minut | Granica w warunku jest przesunięta: `>` zamiast `>=`. | Sprawdź każdą granicę wymagań z obu stron. |
| Program przyjmuje wartość, której nie powinien | Brakuje jednego z wymagań albo użyto `\|\|` zamiast `&&`. | Wypisz wszystkie wymagania i sprawdź, czy każde jest w warunku. |
| `else` nie pasuje do właściwego `if` | W zagnieżdżeniu brakuje klamry albo wcięcia są mylące. | Każde `else` należy do `if`, przy którego zamykającej klamrze stoi. Sprawdź pary klamer. |
| Po wpisaniu tekstu zamiast liczby wynik jest dziwny | To nieudany odczyt, a nie zła wartość. Tego program jeszcze nie obsługuje. | Wpisuj liczby. Obsługę nieudanego odczytu poznasz później. |
| `use of undeclared identifier` dla wyniku obliczenia | Wynik zadeklarowany w bloku jest używany poza nim. | Używaj go w tym samym bloku albo zadeklaruj zmienną przed `if`. |

## 11. Wyjaśnij

Odpowiedz własnymi słowami, najlepiej na piśmie. Dopiero potem porównaj z przykładową odpowiedzią.

**1.** Dlaczego program z punktu 3 dzieli dopiero w gałęzi `if (children > 0)`?

<details>
<summary>Przykładowa odpowiedź</summary>

Bo dzielenie całkowite przez zero jest niedozwolone (ma niezdefiniowane zachowanie). W tej gałęzi wiadomo już, że liczba dzieci jest dodatnia, więc dzielenie jest bezpieczne. Dla 0 dzieci program wybiera gałąź `else` i w ogóle nie dzieli.

</details>

**2.** Liczba `-3` została odczytana bez problemu. Dlaczego program ją odrzuca?

<details>
<summary>Przykładowa odpowiedź</summary>

Bo poprawny odczyt nie znaczy, że wartość spełnia wymagania zadania. `-3` to poprawna liczba typu `int`, ale ujemna liczba cukierków nie ma sensu w tym zadaniu, więc warunek ją odrzuca.

</details>

**3.** Kiedy wybrać jeden warunek z `&&`, a kiedy zagnieżdżony `if`?

<details>
<summary>Przykładowa odpowiedź</summary>

Jeden warunek, gdy wszystkie wymagania prowadzą do jednej decyzji. Zagnieżdżony `if`, gdy drugie pytanie ma sens dopiero po pierwszym albo gdy każdy przypadek ma dostać osobny komunikat.

</details>

**4.** Dlaczego `children > 0 && candies / children >= 3` nie dzieli przez zero dla 0 dzieci?

<details>
<summary>Przykładowa odpowiedź</summary>

Bo `&&` najpierw oblicza lewą stronę. Dla 0 dzieci `children > 0` jest fałszywe, więc całość jest fałszywa, a prawa strona z dzieleniem nie jest obliczana.

</details>

**5.** Czym różni się wpisanie `0` jako liczby dzieci od wpisania `abc`?

<details>
<summary>Przykładowa odpowiedź</summary>

`0` to poprawnie odczytana liczba, która nie spełnia wymagań zadania. Program wykrywa to przez `if`. `abc` to nieudany odczyt liczby. To inny problem, którego program jeszcze nie obsługuje.

</details>

## Podsumowanie

- **Najpierw sprawdzenie, potem decyzja, na końcu obliczenie.** Ryzykowne działanie, takie jak dzielenie przez wartość z wejścia, wykonuj tylko w gałęzi, w której dane są już sprawdzone.
- `else` nie naprawia złej wartości. Wybiera inną drogę, na przykład komunikat zamiast obliczenia.
- Poprawny odczyt to nie to samo co poprawne dane: liczba może być poprawnym `int`, a mimo to nie spełniać wymagań zadania.
- Kilka wymagań łączysz przez `&&`. Zagnieżdżony `if` przydaje się, gdy drugie pytanie ma sens dopiero po pierwszym albo gdy przypadki mają osobne komunikaty.
- Krótkie obliczanie `&&` sprawia, że w `children > 0 && candies / children >= 3` dzielenie nie wykona się dla 0 dzieci. Podstawowym wzorcem pozostaje jednak obliczenie w sprawdzonej gałęzi.
- Programy z tej lekcji wykrywają złe wartości, ale nie nieudany odczyt. Tego nauczysz się później.

## Co dalej

Znasz już wszystkie narzędzia Modułu 3: `if`, `else`, `else if`, porównania, `bool`, operatory logiczne i sprawdzanie danych przed obliczeniami. W lekcji 3.6 sprawdzisz je w samodzielnym zadaniu. **Lekcja 3.6 jest w przygotowaniu.**

---

## Przykładowe rozwiązania

Zajrzyj tutaj **po własnej próbie**. Twoje nazwy mogą się różnić, jeśli standardowe wyjście jest takie, jak wymagane.

<details>
<summary>Punkt 8: wyniki przed poprawką i poprawka</summary>

Przed poprawką:

<!-- input: candy_check_bug -->
```text
0
5
```

<!-- output: candy_check_bug -->
```text
Enter candies:
Enter children:
Invalid values
```

<!-- input: candy_check_bug -->
```text
17
5
```

<!-- output: candy_check_bug -->
```text
Enter candies:
Enter children:
Each child: 3
Remaining: 2
```

<!-- input: candy_check_bug -->
```text
12
0
```

<!-- output: candy_check_bug -->
```text
Enter candies:
Enter children:
Invalid values
```

Dla 0 cukierków i 5 dzieci program wypisuje `Invalid values`, choć wymaganie dopuszcza zero cukierków. Warunek `candies > 0` wyklucza samo zero. Powinien być `candies >= 0`, czyli „nie ujemna”. Poprawiony program to program z punktu 4, który dla 0 i 5 wypisuje `Each child: 0` i `Remaining: 0`, a dla -3 i 4 oraz 12 i 0 `Invalid values`.

</details>

<details>
<summary>Punkt 9: misja, plan nauki</summary>

<!-- example: study_plan -->
```cpp
#include <iostream>

int main() {
    int total_minutes{0};
    int sessions{0};

    std::cout << "Enter total minutes:\n";
    std::cin >> total_minutes;
    std::cout << "Enter number of sessions:\n";
    std::cin >> sessions;

    const bool valid_data{sessions > 0 && total_minutes >= 0};

    if (valid_data) {
        const int minutes_per_session{total_minutes / sessions};
        const int minutes_left{total_minutes % sessions};

        std::cout << "Minutes per session: " << minutes_per_session << "\n";
        std::cout << "Minutes left: " << minutes_left << "\n";
    } else {
        std::cout << "Invalid session data\n";
    }
}
```

- Dwa wymagania prowadzą do jednej decyzji, więc wystarczy jeden warunek z `&&`.
- `/` i `%` stoją w gałęzi, w której `sessions > 0`, więc dzielenie przez zero nigdy się nie wykona.
- `total_minutes >= 0` dopuszcza zero: 0 minut podzielone na sesje daje 0 na sesję i 0 reszty.

</details>

**Poprzednia lekcja:** [Lekcja 3.4: Łączenie warunków (`&&`, `||`, `!`)](lesson_04_combining_conditions.md) · **Następna lekcja:** w przygotowaniu · [Opis kursu](../../README.md)

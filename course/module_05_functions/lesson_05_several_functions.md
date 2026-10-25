# Lekcja 5.5: Kilka funkcji, jeden program

**Polski** · [English](lesson_05_several_functions.en.md) · [Opis kursu](../../README.md)

> **Moduł 5, lekcja 5** · około 80–95 minut
> **Potrzebujesz:** katalogu `cpp-workspace` i oryginalnego projektu `lesson_05_first_program`, jak dotąd. Debugger nie jest w tej lekcji potrzebny.
> **Wersja pilotażowa.** Programy z tej lekcji sprawdzamy automatycznie na Windowsie, Ubuntu i macOS, także z podanymi danymi wejściowymi. Wpisywanie danych w oknie **Run** CLiona opisujemy bez ręcznego sprawdzenia na każdym systemie.

## Zanim zaczniesz

Ta lekcja zakłada, że po lekcji 5.4:

- piszesz funkcje z parametrami, które zwracają `bool`, `int`, `double` albo `std::string`;
- wiesz, że parametr otrzymuje wartość argumentu, a wykonany `return` kończy wywołanie;
- stosujesz kilka instrukcji `return` i klauzule ochronne;
- zostawiasz odczyt i wypisywanie w `main`, a obliczenia w funkcjach.

## Sytuacja

Dotąd każdy program miał jedną własną funkcję, czasem wywoływaną kilka razy, i `main`, które z niej korzystało. Większy problem składa się jednak z kilku mniejszych zadań: trzeba coś sprawdzić, coś obliczyć i coś wybrać. W tej lekcji jeden program będzie się składał z **kilku funkcji o różnych zadaniach**, a funkcje będą korzystać z wyników **innych funkcji**. Nie chodzi o to, żeby funkcji było jak najwięcej, ale o rozsądny podział problemu.

Po tej lekcji będziesz:

- dzielić problem na kilka zadań i wskazywać zadanie każdej funkcji;
- pisać funkcję, która wywołuje inną własną funkcję i korzysta z jej wyniku;
- śledzić kolejność wywołań i powrotów między funkcjami;
- sprawdzać pojedyncze funkcje kontrolowanymi wywołaniami i wydrukami;
- odróżniać sprawdzenie jednej funkcji od sprawdzenia całego programu;
- znajdować funkcję, która ignoruje wynik funkcji pomocniczej;
- projektować program z co najmniej trzech współpracujących funkcji.

## 1. Przygotuj projekt

W `cpp-workspace` utwórz katalog `lesson_5_5` i skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program`. Programy z punktów 2–8 wpisujesz w `main.cpp` tego katalogu.

## 2. Program robi kilka rzeczy

Stacja pomiarowa z lekcji 4.7 musi odpowiedzieć na trzy pytania: czy liczba pomiarów jest dopuszczalna (od 1 do 24), czy temperatura mieści się w zakresie (od -20 do 40) i jaki opis przypisać danym. W tej wersji wszystko stoi w `main`, dla stałych danych:

<!-- example: station_all_in_main -->
```cpp
#include <iostream>
#include <string>

int main() {
    const int count{2};
    const double temperature{-3.0};

    std::string status{""};

    if (count < 1 || count > 24) {
        status = "Invalid station data";
    } else if (temperature < -20.0 || temperature > 40.0) {
        status = "Invalid station data";
    } else if (temperature < 0.0) {
        status = "Below freezing";
    } else {
        status = "Measurement ready";
    }

    std::cout << "Status: " << status << "\n";
}
```

<!-- output: station_all_in_main -->
```text
Status: Below freezing
```

To poprawny program. Zastanów się jednak:

1. Która część kodu odpowiada za liczbę pomiarów, która za temperaturę, a która wybiera opis?
2. Czy da się sprawdzić każde z tych zadań osobno, na przykład samą regułę temperatury dla -21 i -20?
3. Czy wybór opisu musi znać szczegóły zakresów, czy wystarczy mu odpowiedź „dobre” albo „złe”?

<details>
<summary>Omówienie</summary>

Wszystkie trzy zadania są wymieszane w jednym łańcuchu `if`. Żeby sprawdzić samą regułę temperatury, trzeba zmieniać dane całego programu i patrzeć na opis, który zależy też od innych reguł. Wybór opisu nie potrzebuje znać liczb 1, 24, -20 i 40: wystarczy mu wiedzieć, czy dane są dopuszczalne. To nie jest błąd C++. To kwestia czytelności, podziału odpowiedzialności i możliwości osobnego sprawdzania.

</details>

## 3. Trzy funkcje, każda z własnym zadaniem

Ten sam problem, podzielony na trzy funkcje:

<!-- example: station_functions -->
```cpp
#include <iostream>
#include <string>

bool is_valid_measurement_count(int count) {
    return count >= 1 && count <= 24;
}

bool is_valid_temperature(double temperature) {
    return temperature >= -20.0 && temperature <= 40.0;
}

std::string measurement_status(int count, double temperature) {
    if (!is_valid_measurement_count(count)) {
        return "Invalid station data";
    }

    if (!is_valid_temperature(temperature)) {
        return "Invalid station data";
    }

    if (temperature < 0.0) {
        return "Below freezing";
    }

    return "Measurement ready";
}

int main() {
    std::cout << "2, -3.0: " << measurement_status(2, -3.0) << "\n";
    std::cout << "2, 12.5: " << measurement_status(2, 12.5) << "\n";
    std::cout << "0, 12.5: " << measurement_status(0, 12.5) << "\n";
    std::cout << "2, 41.0: " << measurement_status(2, 41.0) << "\n";
}
```

| Funkcja | Zadanie | Dostaje | Zwraca |
|---|---|---|---|
| `is_valid_measurement_count` | czy liczba pomiarów jest dopuszczalna | liczbę pomiarów | `bool` |
| `is_valid_temperature` | czy temperatura jest w zakresie | temperaturę | `bool` |
| `measurement_status` | jaki opis pasuje do danych | liczbę pomiarów i temperaturę | `std::string` |
| `main` | wywołuje funkcję i wypisuje wyniki | | |

`measurement_status` **nie powtarza** warunków z zakresami. Zamiast tego wywołuje dwie małe funkcje i korzysta z ich odpowiedzi. Każda funkcja ma odrębne zadanie. To jeden z możliwych podziałów, nie jedyny poprawny.

**Przewidź** cztery linijki i uruchom program.

<details>
<summary>Standardowe wyjście</summary>

<!-- output: station_functions -->
```text
2, -3.0: Below freezing
2, 12.5: Measurement ready
0, 12.5: Invalid station data
2, 41.0: Invalid station data
```

</details>

## 4. Funkcja wywołuje funkcję

W lekcjach 5.1–5.4 schemat był zawsze ten sam: `main` wywołuje własną funkcję, a wynik wraca do `main`. Teraz droga jest dłuższa:

**`main` → `measurement_status` → funkcja sprawdzająca → wynik wraca do `measurement_status` → wynik wraca do `main`**

- `main` nie musi wywoływać każdej funkcji. Funkcje sprawdzające wywołuje `measurement_status`.
- Własna funkcja może wywołać inną własną funkcję tak samo jak `main`: nazwą, z argumentami w nawiasach.
- Wynik funkcji pomocniczej trafia do **funkcji, która ją wywołała**, tutaj do `measurement_status`, i staje się wartością w jej warunku.
- Funkcja pomocnicza nie wie, kto ostatecznie wypisze raport, i nie musi tego wiedzieć.
- Dane przechodzą między funkcjami tylko przez argumenty i zwracane wyniki, przez wartość, jak w lekcji 5.2. Funkcje nie mają wspólnych zmiennych.

Tak przebiega wywołanie `measurement_status(2, -3.0)`:

| Krok | Gdzie jest program | Co się dzieje |
|---|---|---|
| 1 | `main` | Wywołuje `measurement_status(2, -3.0)`. |
| 2 | `measurement_status` | `count` = 2, `temperature` = -3.0. Sprawdza pierwszy warunek. |
| 3 | `measurement_status` | Wywołuje `is_valid_measurement_count(2)`. |
| 4 | `is_valid_measurement_count` | Oblicza `2 >= 1 && 2 <= 24` i zwraca `true`. |
| 5 | `measurement_status` | Wraca z wynikiem `true`. `!true` to `false`, więc pierwszy `return` się nie wykonuje. |
| 6 | `measurement_status` | Sprawdza drugi warunek. |
| 7 | `measurement_status` | Wywołuje `is_valid_temperature(-3.0)`. |
| 8 | `is_valid_temperature` | Oblicza `-3.0 >= -20.0 && -3.0 <= 40.0` i zwraca `true`. |
| 9 | `measurement_status` | Wraca z wynikiem `true`. Drugi `return` się nie wykonuje. |
| 10 | `measurement_status` | Sprawdza `-3.0 < 0.0`: `true`. |
| 11 | `measurement_status` | `return "Below freezing";` kończy wywołanie. |
| 12 | `main` | Dostaje tekst `Below freezing` i wypisuje go. |

Tej tabeli nie musisz pamiętać. Każdy krok da się odczytać z kodu: wywołanie, wykonanie funkcji, powrót z wynikiem.

**Przewidź** dla wywołania `measurement_status(0, 12.5)`: które funkcje sprawdzające zostaną wywołane, a które nie?

<details>
<summary>Odpowiedź</summary>

Tylko `is_valid_measurement_count(0)`. Zwraca `false`, więc `!false` to `true` i wykonuje się pierwsze `return "Invalid station data";`. Wywołanie `measurement_status` kończy się od razu, jak w lekcji 5.4. Do drugiego warunku program w ogóle nie dochodzi, więc `is_valid_temperature` **nie zostaje wywołana**.

</details>

**Kolejność definicji.** W programie z punktu 3 najpierw stoją dwie małe funkcje pomocnicze, potem funkcja, która z nich korzysta, a na końcu `main`. Dzięki temu w każdym miejscu wywołania kompilator zna już wywoływaną funkcję, jak w lekcji 5.1. W lekcji 5.6 zobaczysz inny sposób uporządkowania funkcji w pliku.

## 5. Sprawdź jedną funkcję

Każdą małą funkcję da się sprawdzić osobno. Wystarczy przygotować kilka wywołań z dobranymi argumentami i wypisać wyniki. Ten program **sprawdza funkcje**, a nie obsługuje stacji. Funkcje są takie same jak w punkcie 3:

<!-- example: station_checks -->
```cpp
#include <iostream>
#include <string>

bool is_valid_measurement_count(int count) {
    return count >= 1 && count <= 24;
}

bool is_valid_temperature(double temperature) {
    return temperature >= -20.0 && temperature <= 40.0;
}

std::string measurement_status(int count, double temperature) {
    if (!is_valid_measurement_count(count)) {
        return "Invalid station data";
    }

    if (!is_valid_temperature(temperature)) {
        return "Invalid station data";
    }

    if (temperature < 0.0) {
        return "Below freezing";
    }

    return "Measurement ready";
}

int main() {
    std::cout << "Count 0 valid: " << is_valid_measurement_count(0) << "\n";
    std::cout << "Count 1 valid: " << is_valid_measurement_count(1) << "\n";
    std::cout << "Count 24 valid: " << is_valid_measurement_count(24) << "\n";
    std::cout << "Count 25 valid: " << is_valid_measurement_count(25) << "\n";

    std::cout << "Temperature -21.0 valid: " << is_valid_temperature(-21.0) << "\n";
    std::cout << "Temperature -20.0 valid: " << is_valid_temperature(-20.0) << "\n";
    std::cout << "Temperature 40.0 valid: " << is_valid_temperature(40.0) << "\n";
    std::cout << "Temperature 41.0 valid: " << is_valid_temperature(41.0) << "\n";

    std::cout << "Status 2, -21.0: " << measurement_status(2, -21.0) << "\n";
}
```

Wartości `bool` wypisują się jako `1` (`true`) albo `0` (`false`), jak w lekcji 3.2.

**Przewidź** każdą linijkę, zanim uruchomisz program. Zapisz oczekiwania w tabeli: argument, oczekiwany wynik.

<details>
<summary>Standardowe wyjście</summary>

<!-- output: station_checks -->
```text
Count 0 valid: 0
Count 1 valid: 1
Count 24 valid: 1
Count 25 valid: 0
Temperature -21.0 valid: 0
Temperature -20.0 valid: 1
Temperature 40.0 valid: 1
Temperature 41.0 valid: 0
Status 2, -21.0: Invalid station data
```

</details>

Tak wygląda **prosty wydruk testowy**:

1. Wybierz funkcję i argumenty, najlepiej granice i wartości tuż obok nich.
2. Zapisz oczekiwany wynik.
3. Wywołaj funkcję i wypisz wynik.
4. Porównaj.

To nie jest nowe narzędzie ani system testów. To zwykłe wywołania i `std::cout`. Wydruki testowe pomagają w czasie pracy, ale nie zostają w programie, który obsługuje użytkownika: dlatego są tu osobnym programem.

## 6. Sprawdzenie funkcji a sprawdzenie programu

Dwie ostatnie grupy linijek z punktu 5 zadają **różne pytania**:

- `is_valid_temperature(-21.0)` daje `0`: czy **reguła temperatury** jest poprawna?
- `measurement_status(2, -21.0)` daje `Invalid station data`: czy funkcja nadrzędna **poprawnie korzysta** z wyniku tej reguły?

Pierwsze pytanie sprawdza jedną funkcję. Drugie sprawdza też współpracę funkcji. **Funkcje mogą być poprawne osobno, a program może z nich korzystać źle.** Kilka wydruków testowych nie daje pełnej gwarancji poprawności, ale dobrze dobrane granice łapią wiele błędów wcześnie. Punkt 7 pokazuje taki błąd współpracy.

## 7. Znajdź błąd: zignorowany wynik

Wymaganie jest takie samo jak w punkcie 3: liczba pomiarów od 1 do 24, temperatura od -20 do 40, a dla danych spoza zakresu opis `Invalid station data`. Obie funkcje pomocnicze są poprawne. Błąd jest gdzie indziej:

<!-- example: status_ignored_bug -->
```cpp
#include <iostream>
#include <string>

bool is_valid_measurement_count(int count) {
    return count >= 1 && count <= 24;
}

bool is_valid_temperature(double temperature) {
    return temperature >= -20.0 && temperature <= 40.0;
}

std::string measurement_status(int count, double temperature) {
    if (!is_valid_measurement_count(count)) {
        return "Invalid station data";
    }

    is_valid_temperature(temperature);

    if (temperature < 0.0) {
        return "Below freezing";
    }

    return "Measurement ready";
}

int main() {
    std::cout << "2, 12.5: " << measurement_status(2, 12.5) << "\n";
    std::cout << "0, 12.5: " << measurement_status(0, 12.5) << "\n";
    std::cout << "2, -21.0: " << measurement_status(2, -21.0) << "\n";
    std::cout << "2, 41.0: " << measurement_status(2, 41.0) << "\n";
}
```

Program buduje się bez błędów i bez ostrzeżeń.

1. Przeczytaj wymaganie i zapisz poprawny opis dla czterech par danych.
2. **Przewidź**, co wypisze **ten** program.
3. Uruchom go i znajdź niezgodności.
4. Ustal, która funkcja odpowiada za regułę, której wynik się nie zgadza.
5. Znajdź miejsce, w którym jej wynik został pominięty.
6. Popraw współpracę funkcji.
7. Sprawdź ponownie wszystkie cztery przypadki.

Wynik przed poprawką i poprawka są w części [Przykładowe rozwiązania](#przykładowe-rozwiązania). Zajrzyj tam po własnej próbie.

## 8. Czy każda instrukcja potrzebuje funkcji?

Więcej funkcji nie oznacza automatycznie lepszego programu. Ta funkcja tylko przekazuje argumenty dalej i niczego nie dodaje:

<!-- fragment -->
```cpp
std::string station_status(int count, double temperature) {
    return measurement_status(count, temperature);
}
```

Program z nią nie jest czytelniejszy: przy śledzeniu trzeba przejść przez jedno wywołanie więcej, a nie ma nowej reguły do sprawdzenia. Zanim wydzielisz funkcję, zapytaj:

- Czy ma nazwane zadanie, które da się opisać jednym zdaniem?
- Czy jej wynik albo działanie jest zrozumiałe bez czytania całego programu?
- Czy da się ją sprawdzić osobno?
- Czy zapobiega powtórzeniu ważnej reguły?
- Czy podział nie utrudnia śledzenia programu?

Nie ma sztywnej liczby linijek, po której funkcja jest „za długa”. Liczy się czytelne zadanie.

## 9. Misja: koszt dostawy przesyłki

Program oblicza koszt dostarczenia przesyłki w pełnych złotych. To uproszczony model cenowy do ćwiczenia, a nie prawdziwy cennik przewoźnika.

**Dane:**

- masa przesyłki w pełnych kilogramach: liczba całkowita od 1 do 8 włącznie;
- strefa dostawy: liczba całkowita od 1 do 3 włącznie.

**Cena** to cena podstawowa zależna od masy plus dopłata zależna od strefy:

| Masa | Cena podstawowa |
|---|---|
| 1–2 kg | 5 zł |
| 3–5 kg | 8 zł |
| 6–8 kg | 12 zł |

| Strefa | Dopłata |
|---|---|
| 1 | 0 zł |
| 2 | 3 zł |
| 3 | 6 zł |

**Wymagania:**

- Program wypisuje `Enter parcel weight and delivery zone:` i odczytuje dwie liczby całkowite: masę, potem strefę.
- Jeśli odczyt się nie uda, wypisuje tylko `Input could not be read`.
- Jeśli odczytano obie liczby, ale choć jedna jest spoza zakresu, wypisuje tylko `Invalid shipping data`.
- Dla poprawnych danych wypisuje `Shipping cost: N`, gdzie `N` to koszt w pełnych złotych.
- Program nie pyta ponownie.
- Program ma **co najmniej trzy własne funkcje oprócz `main`**. **Co najmniej jedna z nich wywołuje inną własną funkcję.** Funkcje obliczające i sprawdzające niczego nie wypisują i niczego nie odczytują.
- `main` wypisuje pytanie, odczytuje dane, sprawdza odczyt, korzysta z Twojej funkcji do sprawdzenia danych, otrzymuje koszt i wypisuje raport. Reguły ceny podstawowej i dopłat nie stoją w `main`.
- Definicje funkcji pomocniczych stoją przed funkcjami, które z nich korzystają, a wszystkie przed `main`.
- Nie używaj zmiennych zadeklarowanych poza funkcjami.

W `cpp-workspace` utwórz katalog `shipping_cost`, skopiuj do niego `CMakeLists.txt` z oryginalnego `lesson_05_first_program`, utwórz pusty `main.cpp` i napisz program samodzielnie.

Dla danych `2` i `3` (5 zł ceny podstawowej i 6 zł dopłaty):

<!-- input: shipping_cost -->
```text
2
3
```

<!-- output: shipping_cost -->
```text
Enter parcel weight and delivery zone:
Shipping cost: 11
```

Dla danych `6` i `2` (12 zł ceny podstawowej i 3 zł dopłaty):

<!-- input: shipping_cost -->
```text
6
2
```

<!-- output: shipping_cost -->
```text
Enter parcel weight and delivery zone:
Shipping cost: 15
```

**To nie jest stacja pomiarowa z nowymi nazwami.** Tam dwie funkcje sprawdzały zakresy, a trzecia wybierała opis. Tutaj są **dwie osobne reguły cenowe** i wynik typu `int`, który powstaje z wyników innych funkcji. Musisz samodzielnie zdecydować:

1. które zadania wydzielić do funkcji, jakie dać im parametry i typy wyników;
2. która funkcja zna reguły ceny podstawowej, a która dopłat;
3. która funkcja korzysta z wyniku innej, żeby nie powtarzać jej reguł;
4. w jakiej kolejności zapisać definicje;
5. co zostaje w `main`.

**Najpierw sprawdź funkcje osobno.** Zanim uruchomisz cały program z danymi, przygotuj osobny program z wydrukami testowymi, jak w punkcie 5:

1. Wybierz funkcję.
2. Przygotuj argumenty: granice mas (2 i 3, 5 i 6), granice stref, wartości spoza zakresu.
3. Zapisz oczekiwany wynik.
4. Wypisz rzeczywisty wynik wywołania.
5. Porównaj.
6. Dopiero potem sprawdź program jako całość.

Program, który obsługuje użytkownika, nie zawiera wydruków testowych.

**Zanim napiszesz program**, przygotuj też tabelę przypadków dla całego programu: każda granica masy i strefy z obu stron, wartości spoza zakresu dla masy i dla strefy, tekst zamiast pierwszej i zamiast drugiej liczby oraz dane, które kończą się po jednej liczbie. Przy każdym przypadku zapisz oczekiwane standardowe wyjście.

Przypadki z danymi, które kończą się wcześniej, przeanalizuj na papierze, jak w lekcjach 4.5–5.4, zamiast je uruchamiać, i porównaj ze zwiniętą listą kontrolną. Program z tej lekcji jest dla takich danych sprawdzany osobno, automatycznymi testami kursu.

### Kryterium sukcesu

- Program buduje się jako C++20, a jego standardowe wyjście dla danych `2`, `3` i `6`, `2` jest dokładnie takie jak powyżej.
- Dla każdego przypadku, który możesz wpisać, standardowe wyjście zgadza się z listą kontrolną. Przypadki z danymi, które kończą się wcześniej, sprawdzasz rozumowaniem.
- Program ma co najmniej trzy własne funkcje oprócz `main`, a co najmniej jedna z nich wywołuje inną własną funkcję i korzysta z jej wyniku.
- Każda reguła cenowa występuje w kodzie raz, w funkcji. `main` nie zawiera progów masy ani dopłat.
- Funkcje obliczające i sprawdzające nie wypisują i nie odczytują niczego.
- Po nieudanym odczycie albo danych spoza zakresu nie pojawia się `Shipping cost`.
- Przed sprawdzeniem całego programu sprawdzono funkcje wydrukami testowymi, a w programie końcowym takich wydruków nie ma.
- Program nie używa zmiennych zadeklarowanych poza funkcjami.
- Umiesz powiedzieć o każdej funkcji: jakie ma zadanie, co dostaje, co zwraca i kto ją wywołuje.

Gdy wynik się zgadza, możesz zapisać projekt w Gicie, jak w lekcji 1.5.

<details>
<summary>Podpowiedź 1</summary>

Wskaż trzy różne zadania: sprawdzenie danych, ustalenie ceny podstawowej oraz wyznaczenie kosztu końcowego.

</details>

<details>
<summary>Podpowiedź 2</summary>

Zastanów się, która funkcja zna zasady ceny podstawowej, a która może wykorzystać jej wynik bez powtarzania tych zasad.

</details>

<details>
<summary>Podpowiedź 3</summary>

Jeśli funkcja obliczająca koszt całkowity potrzebuje ceny podstawowej, może wywołać inną własną funkcję i wykorzystać otrzymaną wartość w dalszym obliczeniu.

</details>

<details>
<summary>Pełna lista przypadków kontrolnych: otwórz po przygotowaniu własnej tabeli</summary>

| Masa | Strefa | Standardowe wyjście po pytaniu | Co sprawdza |
|---|---|---|---|
| 2 | 3 | `Shipping cost: 11` | przykład z treści |
| 6 | 2 | `Shipping cost: 15` | przykład z treści |
| 1 | 1 | `Shipping cost: 5` | dolne granice |
| 2 | 2 | `Shipping cost: 8` | koniec pierwszego przedziału masy |
| 3 | 1 | `Shipping cost: 8` | początek drugiego przedziału masy |
| 3 | 3 | `Shipping cost: 14` | drugi przedział, najwyższa dopłata |
| 4 | 2 | `Shipping cost: 11` | środek drugiego przedziału |
| 5 | 2 | `Shipping cost: 11` | koniec drugiego przedziału |
| 6 | 3 | `Shipping cost: 18` | początek trzeciego przedziału |
| 8 | 1 | `Shipping cost: 12` | górna granica masy |
| 8 | 3 | `Shipping cost: 18` | górne granice |
| 0 | 1 | `Invalid shipping data` | masa tuż pod zakresem |
| -1 | 1 | `Invalid shipping data` | masa ujemna |
| 9 | 1 | `Invalid shipping data` | masa tuż nad zakresem |
| 1 | 0 | `Invalid shipping data` | strefa tuż pod zakresem |
| 1 | 4 | `Invalid shipping data` | strefa tuż nad zakresem |
| `abc` | `1` | `Input could not be read` | tekst zamiast masy |
| `1` | `abc` | `Input could not be read` | tekst zamiast strefy |
| `1` | koniec danych | `Input could not be read` | dane kończą się po jednej liczbie |
| brak danych | brak danych | `Input could not be read` | dane kończą się od razu |

Pierwsze dwa przypadki są sprawdzone wyżej, przy treści misji.

<!-- input: shipping_cost -->
```text
1
1
```

<!-- output: shipping_cost -->
```text
Enter parcel weight and delivery zone:
Shipping cost: 5
```

<!-- input: shipping_cost -->
```text
2
2
```

<!-- output: shipping_cost -->
```text
Enter parcel weight and delivery zone:
Shipping cost: 8
```

<!-- input: shipping_cost -->
```text
3
1
```

<!-- output: shipping_cost -->
```text
Enter parcel weight and delivery zone:
Shipping cost: 8
```

<!-- input: shipping_cost -->
```text
3
3
```

<!-- output: shipping_cost -->
```text
Enter parcel weight and delivery zone:
Shipping cost: 14
```

<!-- input: shipping_cost -->
```text
4
2
```

<!-- output: shipping_cost -->
```text
Enter parcel weight and delivery zone:
Shipping cost: 11
```

<!-- input: shipping_cost -->
```text
5
2
```

<!-- output: shipping_cost -->
```text
Enter parcel weight and delivery zone:
Shipping cost: 11
```

<!-- input: shipping_cost -->
```text
6
3
```

<!-- output: shipping_cost -->
```text
Enter parcel weight and delivery zone:
Shipping cost: 18
```

<!-- input: shipping_cost -->
```text
8
1
```

<!-- output: shipping_cost -->
```text
Enter parcel weight and delivery zone:
Shipping cost: 12
```

<!-- input: shipping_cost -->
```text
8
3
```

<!-- output: shipping_cost -->
```text
Enter parcel weight and delivery zone:
Shipping cost: 18
```

<!-- input: shipping_cost -->
```text
0
1
```

<!-- output: shipping_cost -->
```text
Enter parcel weight and delivery zone:
Invalid shipping data
```

<!-- input: shipping_cost -->
```text
-1
1
```

<!-- output: shipping_cost -->
```text
Enter parcel weight and delivery zone:
Invalid shipping data
```

<!-- input: shipping_cost -->
```text
9
1
```

<!-- output: shipping_cost -->
```text
Enter parcel weight and delivery zone:
Invalid shipping data
```

<!-- input: shipping_cost -->
```text
1
0
```

<!-- output: shipping_cost -->
```text
Enter parcel weight and delivery zone:
Invalid shipping data
```

<!-- input: shipping_cost -->
```text
1
4
```

<!-- output: shipping_cost -->
```text
Enter parcel weight and delivery zone:
Invalid shipping data
```

<!-- input: shipping_cost -->
```text
abc
1
```

<!-- output: shipping_cost -->
```text
Enter parcel weight and delivery zone:
Input could not be read
```

<!-- input: shipping_cost -->
```text
1
abc
```

<!-- output: shipping_cost -->
```text
Enter parcel weight and delivery zone:
Input could not be read
```

<!-- input: shipping_cost -->
```text
1
```

<!-- output: shipping_cost -->
```text
Enter parcel weight and delivery zone:
Input could not be read
```

<!-- input: shipping_cost -->
```text
```

<!-- output: shipping_cost -->
```text
Enter parcel weight and delivery zone:
Input could not be read
```

</details>

Przykładowe rozwiązanie jest w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 10. Gdy coś pójdzie inaczej

| Co widzisz | Co to znaczy | Co zrobić |
|---|---|---|
| `use of undeclared identifier` z nazwą Twojej funkcji | Funkcja jest wywoływana w pliku przed swoją definicją, także przez inną funkcję. | Funkcje pomocnicze zapisuj przed funkcjami, które z nich korzystają. |
| Dane spoza zakresu dostają zwykły wynik | Wynik funkcji sprawdzającej jest pomijany albo funkcja nie jest wywoływana (punkt 7). | Sprawdź, czy wynik każdego wywołania jest użyty w warunku albo w obliczeniu. |
| Wydruk testowy pokazuje dobry wynik, a cały program zły | Funkcja jest poprawna, ale korzystająca z niej funkcja albo `main` używa jej źle (punkt 6). | Sprawdź także współpracę: wywołaj funkcję nadrzędną dla tych samych granic. |
| Koszt jest zły tylko na granicy, na przykład dla 2 kg albo 5 kg | Próg w funkcji ceny podstawowej używa `<` zamiast `<=` albo odwrotnie. | Sprawdź tę funkcję wydrukami dla 2, 3, 5 i 6. |
| Reguły cen powtarzają się w kilku miejscach | Zamiast wywołać funkcję, kod powtarza jej warunki. | Niech jedna funkcja zna regułę, a pozostałe korzystają z jej wyniku. |
| W wyniku programu pojawiają się wydruki testowe | Program testowy i program końcowy są wymieszane. | Wydruki testowe trzymaj w osobnym programie albo usuń je przed końcowym sprawdzeniem. |
| Po nieudanym odczycie pojawia się koszt | Funkcje są wywoływane przed sprawdzeniem odczytu. | Najpierw sprawdź `std::cin.fail()`, potem zakres, a dopiero potem licz koszt. |
| Program nic nie robi i czeka | Czeka na kolejną liczbę, jak w lekcji 2.6. | Wpisz liczbę i naciśnij **Enter**. Przypadku z końcem danych nie sprawdzaj w ten sposób: prześledź go na papierze. |

## 11. Wyjaśnij

Odpowiedz własnymi słowami, najlepiej na piśmie. Dopiero potem porównaj z przykładowymi odpowiedziami.

1. Dlaczego program może potrzebować więcej niż jednej własnej funkcji?
2. Czy własna funkcja może wywołać inną własną funkcję?
3. Co dzieje się z wynikiem funkcji pomocniczej?
4. Czy każda funkcja musi być wywoływana bezpośrednio przez `main`?
5. Dlaczego funkcja sprawdzająca zakres może zwracać `bool`?
6. Dlaczego funkcja obliczająca koszt może zwracać `int`?
7. Czy funkcja może wykorzystywać wynik innej funkcji w swoim `return`?
8. Dlaczego warto oddzielać obliczenia od wypisywania?
9. Czy poprawność każdej funkcji osobno gwarantuje poprawność całego programu?
10. Po co przygotowujemy wydruki testowe?
11. Czym wydruk testowy różni się od zwykłego raportu programu?
12. Dlaczego testowanie granic zakresów jest ważne?
13. Czy każda pojedyncza instrukcja powinna mieć własną funkcję?
14. Dlaczego nie używamy tu zmiennych zadeklarowanych poza funkcjami?
15. Dlaczego kolejność definicji ma znaczenie przy obecnym sposobie organizacji kodu?
16. Czy do stworzenia kilku współpracujących funkcji potrzebujemy już nowych sposobów przekazywania danych?

<details>
<summary>Przykładowe odpowiedzi</summary>

1. Bo większy problem składa się z kilku zadań. Każde z nich można nazwać, zapisać raz i sprawdzić osobno.
2. Tak. Wywołuje ją tak samo jak `main`: nazwą i argumentami.
3. Trafia do funkcji, która ją wywołała, i staje się tam wartością, na przykład w warunku albo w obliczeniu.
4. Nie. Funkcję może wywołać każda funkcja zdefiniowana w pliku po niej, tak jak `measurement_status` wywołuje funkcje sprawdzające.
5. Bo odpowiada na pytanie „tak albo nie”: czy wartość jest dopuszczalna.
6. Bo koszt w tym zadaniu to liczba pełnych złotych.
7. Tak, na przykład `return base_price(weight) + zone_surcharge(zone);`.
8. Bo funkcję, która tylko oblicza, można wywołać z różnych miejsc i sprawdzić osobno. O tym, co wypisać, decyduje miejsce wywołania.
9. Nie. Funkcje mogą być poprawne, a funkcja nadrzędna albo `main` może z nich korzystać źle, na przykład pominąć wynik (punkt 7).
10. Żeby sprawdzić jedną funkcję dla dobranych argumentów, zanim zacznie od niej zależeć cały program.
11. Wydruk testowy pokazuje wynik jednej funkcji dla jednego argumentu i służy osobie, która pisze program. Raport jest częścią programu dla użytkownika. Wydruków testowych nie zostawiamy w programie końcowym.
12. Bo błędy często siedzą właśnie na granicach, na przykład `<` zamiast `<=`. Wartość w środku przedziału ich nie ujawnia.
13. Nie. Funkcja ma sens, gdy ma czytelne zadanie. Funkcja, która tylko przekazuje argumenty dalej, nie poprawia programu.
14. Bo funkcje przekazują dane przez argumenty i zwracane wyniki. Dzięki temu każda zależy tylko od tego, co dostała, i da się ją sprawdzić osobno.
15. Bo kompilator czyta plik od góry i w miejscu wywołania musi już znać wywoływaną funkcję. Dlatego funkcje pomocnicze stoją przed funkcjami, które z nich korzystają.
16. Nie. Wystarczą parametry, argumenty i `return`, które znasz z lekcji 5.2–5.4.

</details>

## Podsumowanie

- Jeden program może składać się z **kilku funkcji o różnych zadaniach**. Każda powinna mieć zadanie, które da się nazwać.
- **Własna funkcja może wywołać inną własną funkcję.** Wynik funkcji pomocniczej trafia do funkcji, która ją wywołała.
- Dane przechodzą między funkcjami przez argumenty i zwracane wyniki. Wywołanie, wykonanie i powrót można prześledzić w tabeli krok po kroku.
- Funkcje pomocnicze stoją w pliku przed funkcjami, które z nich korzystają, a wszystkie przed `main`.
- **Wydruk testowy** to kilka wywołań z dobranymi argumentami i porównanie wyników z oczekiwaniami. Nie zostaje w programie dla użytkownika.
- Sprawdzenie jednej funkcji to nie to samo co sprawdzenie programu. **Funkcje mogą być poprawne osobno, a źle ze sobą współpracować**, na przykład gdy wynik funkcji pomocniczej zostanie pominięty.
- Więcej funkcji nie oznacza lepszego programu. Funkcja ma sens, gdy ma czytelne zadanie.

## Co dalej

Twoje programy składają się już z kilku funkcji, ułożonych w pliku tak, żeby każda była zapisana przed swoim wywołaniem. W kolejnej lekcji zobaczysz inny sposób uporządkowania funkcji: [Lekcja 5.6: Deklaracja, definicja i linkowanie](lesson_06_declaration_and_definition.md).

---

## Przykładowe rozwiązania

Zajrzyj tutaj **po własnej próbie**. Twoje nazwy mogą się różnić, jeśli standardowe wyjście jest takie, jak wymagane.

<details>
<summary>Punkt 7: wynik przed poprawką i poprawka</summary>

Przed poprawką:

<!-- output: status_ignored_bug -->
```text
2, 12.5: Measurement ready
0, 12.5: Invalid station data
2, -21.0: Below freezing
2, 41.0: Measurement ready
```

- **Dla 2, 12.5 i 0, 12.5** wyniki są poprawne. Te przypadki nie ujawniają błędu: pierwsza temperatura jest w zakresie, a druga para odpada już na liczbie pomiarów.
- **Dla 2, -21.0 i 2, 41.0** wymaganie mówi `Invalid station data`, a program wypisuje `Below freezing` i `Measurement ready`.
- **Przyczyna:** funkcja `is_valid_temperature` jest poprawna i jest wywoływana, ale linijka `is_valid_temperature(temperature);` **wyrzuca jej wynik**. Żadna decyzja nie korzysta z odpowiedzi `false`. Kompilator nie ostrzega, bo samo wywołanie funkcji jest poprawną instrukcją.
- **Poprawka:** użyj wyniku w warunku, jak w punkcie 3:

<!-- fragment -->
```cpp
    if (!is_valid_temperature(temperature)) {
        return "Invalid station data";
    }
```

Poprawiony program, z tymi samymi czterema przypadkami:

<!-- example: status_ignored_fixed -->
```cpp
#include <iostream>
#include <string>

bool is_valid_measurement_count(int count) {
    return count >= 1 && count <= 24;
}

bool is_valid_temperature(double temperature) {
    return temperature >= -20.0 && temperature <= 40.0;
}

std::string measurement_status(int count, double temperature) {
    if (!is_valid_measurement_count(count)) {
        return "Invalid station data";
    }

    if (!is_valid_temperature(temperature)) {
        return "Invalid station data";
    }

    if (temperature < 0.0) {
        return "Below freezing";
    }

    return "Measurement ready";
}

int main() {
    std::cout << "2, 12.5: " << measurement_status(2, 12.5) << "\n";
    std::cout << "0, 12.5: " << measurement_status(0, 12.5) << "\n";
    std::cout << "2, -21.0: " << measurement_status(2, -21.0) << "\n";
    std::cout << "2, 41.0: " << measurement_status(2, 41.0) << "\n";
}
```

<!-- output: status_ignored_fixed -->
```text
2, 12.5: Measurement ready
0, 12.5: Invalid station data
2, -21.0: Invalid station data
2, 41.0: Invalid station data
```

</details>

<details>
<summary>Punkt 9: misja, koszt dostawy</summary>

Najpierw program z wydrukami testowymi, który sprawdza funkcje osobno:

<!-- example: shipping_checks -->
```cpp
#include <iostream>

bool is_valid_shipping_data(int weight, int zone) {
    return weight >= 1 && weight <= 8 && zone >= 1 && zone <= 3;
}

int base_price(int weight) {
    if (weight <= 2) {
        return 5;
    }

    if (weight <= 5) {
        return 8;
    }

    return 12;
}

int zone_surcharge(int zone) {
    if (zone == 1) {
        return 0;
    }

    if (zone == 2) {
        return 3;
    }

    return 6;
}

int shipping_cost(int weight, int zone) {
    return base_price(weight) + zone_surcharge(zone);
}

int main() {
    std::cout << "Valid 1, 1: " << is_valid_shipping_data(1, 1) << "\n";
    std::cout << "Valid 0, 1: " << is_valid_shipping_data(0, 1) << "\n";
    std::cout << "Valid 8, 3: " << is_valid_shipping_data(8, 3) << "\n";
    std::cout << "Valid 9, 1: " << is_valid_shipping_data(9, 1) << "\n";
    std::cout << "Valid 2, 4: " << is_valid_shipping_data(2, 4) << "\n";

    std::cout << "Base price 2: " << base_price(2) << "\n";
    std::cout << "Base price 3: " << base_price(3) << "\n";
    std::cout << "Base price 5: " << base_price(5) << "\n";
    std::cout << "Base price 6: " << base_price(6) << "\n";

    std::cout << "Surcharge 1: " << zone_surcharge(1) << "\n";
    std::cout << "Surcharge 2: " << zone_surcharge(2) << "\n";
    std::cout << "Surcharge 3: " << zone_surcharge(3) << "\n";

    std::cout << "Cost 2, 3: " << shipping_cost(2, 3) << "\n";
    std::cout << "Cost 6, 2: " << shipping_cost(6, 2) << "\n";
}
```

<!-- output: shipping_checks -->
```text
Valid 1, 1: 1
Valid 0, 1: 0
Valid 8, 3: 1
Valid 9, 1: 0
Valid 2, 4: 0
Base price 2: 5
Base price 3: 8
Base price 5: 8
Base price 6: 12
Surcharge 1: 0
Surcharge 2: 3
Surcharge 3: 6
Cost 2, 3: 11
Cost 6, 2: 15
```

Potem program końcowy, z tymi samymi funkcjami i bez wydruków testowych:

<!-- example: shipping_cost -->
```cpp
#include <iostream>

bool is_valid_shipping_data(int weight, int zone) {
    return weight >= 1 && weight <= 8 && zone >= 1 && zone <= 3;
}

int base_price(int weight) {
    if (weight <= 2) {
        return 5;
    }

    if (weight <= 5) {
        return 8;
    }

    return 12;
}

int zone_surcharge(int zone) {
    if (zone == 1) {
        return 0;
    }

    if (zone == 2) {
        return 3;
    }

    return 6;
}

int shipping_cost(int weight, int zone) {
    return base_price(weight) + zone_surcharge(zone);
}

int main() {
    int weight{0};
    int zone{0};

    std::cout << "Enter parcel weight and delivery zone:\n";
    std::cin >> weight;
    std::cin >> zone;

    if (std::cin.fail()) {
        std::cout << "Input could not be read\n";
    } else if (!is_valid_shipping_data(weight, zone)) {
        std::cout << "Invalid shipping data\n";
    } else {
        std::cout << "Shipping cost: " << shipping_cost(weight, zone) << "\n";
    }
}
```

| Funkcja | Zadanie | Dostaje | Zwraca | Kto ją wywołuje |
|---|---|---|---|---|
| `is_valid_shipping_data` | czy masa i strefa są dopuszczalne | masę i strefę | `bool` | `main` |
| `base_price` | cena podstawowa według masy | masę | `int` | `shipping_cost` |
| `zone_surcharge` | dopłata według strefy | strefę | `int` | `shipping_cost` |
| `shipping_cost` | koszt całkowity | masę i strefę | `int` | `main` |

- **Współpraca:** `shipping_cost` nie zna progów masy ani dopłat. Wywołuje `base_price` i `zone_surcharge` i dodaje ich wyniki w swoim `return`. Każda reguła cenowa stoi w kodzie raz.
- **Kolejność definicji:** `base_price` i `zone_surcharge` stoją przed `shipping_cost`, która je wywołuje, a wszystkie przed `main`.
- **Założenie:** `base_price` i `zone_surcharge` liczą poprawnie tylko dla danych z zakresu. Dla 9 kg `base_price` zwróciłaby 12. Dlatego `main` wywołuje `shipping_cost` dopiero po sprawdzeniu `is_valid_shipping_data`.
- **Sprawdzanie osobno:** program z wydrukami testowymi sprawdza każdą funkcję na granicach (2 i 3, 5 i 6, wszystkie strefy, wartości spoza zakresu), a dwa ostatnie wydruki sprawdzają współpracę. Program końcowy zawiera tylko raport.
- **Nieudany odczyt:** `main` najpierw sprawdza `std::cin.fail()`. Po nieudanym odczycie, także gdy dane kończą się po jednej liczbie, żadna funkcja cenowa nie jest wywoływana.
- To jeden z poprawnych podziałów. Inny czytelny podział też jest dobry, jeśli spełnia wymagania, na przykład bez osobnej funkcji `zone_surcharge`, z dopłatą liczoną w `shipping_cost`.

</details>

**Poprzednia lekcja:** [Lekcja 5.4: Kilka dróg do `return`](lesson_04_several_returns.md) · **Następna lekcja:** [Lekcja 5.6: Deklaracja, definicja i linkowanie](lesson_06_declaration_and_definition.md) · [Opis kursu](../../README.md)

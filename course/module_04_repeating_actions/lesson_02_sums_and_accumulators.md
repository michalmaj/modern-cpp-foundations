# Lekcja 4.2: Sumowanie i akumulatory

**Polski** · [English](lesson_02_sums_and_accumulators.en.md) · [Opis kursu](../../README.md)

> **Moduł 4, lekcja 2** · około 70–85 minut
> **Potrzebujesz:** katalogu `cpp-workspace` i oryginalnego projektu `lesson_05_first_program`, jak dotąd. Debugger nie jest w tej lekcji potrzebny.
> **Wersja pilotażowa.** Programy z tej lekcji sprawdzamy automatycznie na Windowsie, Ubuntu i macOS, także z podanymi danymi wejściowymi.

## Zanim zaczniesz

Ta lekcja zakłada, że po lekcji 4.1:

- piszesz pętlę `while` z licznikiem: wartość początkowa, warunek, ciało i zmiana licznika;
- śledzisz pętlę w tabeli, w której każdy wiersz to jedno sprawdzenie warunku;
- wiesz, że pętla może wykonać się zero razy;
- sprawdzasz pętlę dla zera, jednego i kilku przebiegów.

## Sytuacja

Ile to jest 1 + 2 + 3? To łatwe: 6. Do programu też łatwo wpisać `1 + 2 + 3`. Ale gdyby użytkownik podawał, do jakiej liczby sumować, do 10, do 500 albo do 1000, takiego wyrażenia nie da się zapisać z góry.

Można jednak liczyć tak, jak liczy się w pamięci: **krok po kroku**. Najpierw masz 0. Dodajesz 1 i masz 1. Dodajesz 2 i masz 3. Dodajesz 3 i masz 6. W każdym kroku pamiętasz tylko jedną liczbę: dotychczasową sumę. Dziś pętla nauczy się w ten sposób **gromadzić wynik**.

Po tej lekcji będziesz:

- wyjaśniać, czym jest akumulator i czym różni się od licznika;
- nadawać akumulatorowi właściwą wartość początkową i aktualizować go w każdym przebiegu;
- odtwarzać wartość sumy po każdym przebiegu;
- zapisywać aktualizację krócej, przez `+=`;
- znajdować błąd zerowania sumy w pętli i wyjaśniać, dlaczego jeden przebieg go nie ujawnia;
- sumować wartości odczytywane w kolejnych przebiegach, także typu `double`.

## 1. Przygotuj projekt

W `cpp-workspace` utwórz katalog `lesson_4_2` i skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program`. Programy z punktów 2–7 wpisujesz w `main.cpp` tego katalogu.

## 2. Suma krok po kroku

<!-- example: sum_to_three -->
```cpp
#include <iostream>

int main() {
    int total{0};
    int number{1};

    while (number <= 3) {
        total = total + number;
        number = number + 1;
    }

    std::cout << "Total: " << total << "\n";
}
```

**Przewidź**, co wypisze program, a potem go uruchom.

<details>
<summary>Wynik programu</summary>

<!-- output: sum_to_three -->
```text
Total: 6
```

</details>

Pętla jest taka sama jak w lekcji 4.1: `number` to licznik, który zaczyna od 1, rośnie o 1 i kończy pętlę, gdy przekroczy 3. Nowa jest druga zmienna:

- `number` to **liczba dodawana w tym przebiegu**. Jej zmiana prowadzi pętlę do końca.
- `total` przechowuje **sumę zgromadzoną do tej chwili**.
- `total` dostaje wartość początkową 0 **przed pętlą**. Przed pierwszym dodaniem nic jeszcze nie zsumowano, a 0 niczego nie zmienia w sumie.
- `total = total + number;` bierze **dotychczasową** sumę, dodaje do niej bieżącą liczbę i zapisuje wynik z powrotem w `total` (lekcja 2.2). Każdy przebieg korzysta więc z wyniku poprzedniego.

Zmienną, która w kolejnych przebiegach gromadzi wynik, nazywa się **akumulatorem**. To nie jest nowy typ ani specjalna konstrukcja C++, tylko zwykła zmienna `int`, używana w określony sposób.

## 3. Tabela przebiegu

Tabela z lekcji 4.1 dostaje kolumny dla sumy:

| Sprawdzenie warunku | `number` | `number <= 3` | `total` przed dodaniem | Dodawana wartość | `total` po dodaniu | `number` po ciele |
|---|---|---|---|---|---|---|
| 1 | 1 | `true` | 0 | 1 | 1 | 2 |
| 2 | 2 | `true` | 1 | 2 | 3 | 3 |
| 3 | 3 | `true` | 3 | 3 | 6 | 4 |
| 4 | 4 | `false` | — | — | — | — |

- Wiersz po wierszu widać sumę **po każdym przebiegu**: 1, potem 3, potem 6. Wartość w kolumnie „przed dodaniem” to zawsze wartość „po dodaniu” z poprzedniego wiersza.
- Czwarte sprawdzenie daje `false`, bo licznik przekroczył górną granicę. To **nie jest** kolejny przebieg: ciało się nie wykonuje, a `total` zostaje równe 6.

**Twoja kolej.** Wyobraź sobie, że warunek brzmi `number <= 4`. Przepisz tabelę i wypełnij ją dla tego przypadku: ile będzie sprawdzeń warunku, jaka będzie suma po każdym przebiegu i jaki wynik wypisze program? Odpowiedź jest w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 4. Krótszy zapis: `+=`

Aktualizacja „weź starą wartość, dodaj coś i zapisz z powrotem” zdarza się tak często, że C++ ma na nią krótszy zapis. W naszych przykładach te dwie linijki robią to samo:

<!-- fragment -->
```cpp
total = total + number;
total += number;
```

Czytaj `total += number;` jako: **„zwiększ przechowywaną sumę o wartość `number`”**.

- `+=` zmienia **istniejącą** zmienną po lewej stronie. Nie tworzy nowej: `total` musi być wcześniej zadeklarowane, z wartością początkową.
- `+=` dodaje tę wartość, która stoi po prawej stronie, a nie zawsze 1.
- **Uwaga o typach.** Inicjalizacja przez `{}` odrzuca zawężenie typu: `int total{2.5};` się nie zbuduje (lekcja 2.5). `+=` takiej ochrony nie daje. Gdyby do sumy typu `int` dodać wartość `double`, część ułamkowa przepadłaby bez błędu kompilacji. Dlatego **typ akumulatora dobieraj do sumowanych wartości**: liczby całkowite sumuj w `int`, a wartości z częścią ułamkową w `double`.

## 5. Suma od 1 do N

Teraz górną granicę podaje użytkownik. Program przyjmuje N od 0 do 1000. Dla innych liczb wypisuje komunikat i w ogóle nie sumuje. Zakładamy, że użytkownik wpisuje liczbę całkowitą.

<!-- example: sum_to_n -->
```cpp
#include <iostream>

int main() {
    int limit{0};

    std::cout << "Enter N (0-1000):\n";
    std::cin >> limit;

    if (limit >= 0 && limit <= 1000) {
        int total{0};
        int number{1};

        while (number <= limit) {
            total += number;
            number = number + 1;
        }

        std::cout << "Total: " << total << "\n";
    } else {
        std::cout << "N must be from 0 to 1000\n";
    }
}
```

**Przewidź** wynik dla N równego 0, 1, 3 i 4. Zapisz odpowiedzi, a potem uruchom program cztery razy, bez zmiany kodu.

<!-- input: sum_to_n -->
```text
0
```

<details>
<summary>Standardowe wyjście dla 0</summary>

<!-- output: sum_to_n -->
```text
Enter N (0-1000):
Total: 0
```

Pierwsze sprawdzenie, `1 <= 0`, daje `false`: zero przebiegów. Suma zostaje równa wartości początkowej, czyli 0. To poprawny wynik: suma żadnych liczb to 0.

</details>

<!-- input: sum_to_n -->
```text
1
```

<details>
<summary>Standardowe wyjście dla 1</summary>

<!-- output: sum_to_n -->
```text
Enter N (0-1000):
Total: 1
```

</details>

<!-- input: sum_to_n -->
```text
3
```

<details>
<summary>Standardowe wyjście dla 3</summary>

<!-- output: sum_to_n -->
```text
Enter N (0-1000):
Total: 6
```

</details>

<!-- input: sum_to_n -->
```text
4
```

<details>
<summary>Standardowe wyjście dla 4</summary>

<!-- output: sum_to_n -->
```text
Enter N (0-1000):
Total: 10
```

</details>

**Największe N.** Dla 1000 pętla wykona 1000 przebiegów, w ułamku sekundy. Przewidź: czy wynik będzie większy, czy mniejszy niż 1 000 000? Potem sprawdź.

<!-- input: sum_to_n -->
```text
1000
```

<details>
<summary>Standardowe wyjście dla 1000</summary>

<!-- output: sum_to_n -->
```text
Enter N (0-1000):
Total: 500500
```

</details>

**Dlaczego zakres od 0 do 1000?** Dzięki niemu program działa krótko, a jego wynik da się przewidzieć i sprawdzić. Typ `int` nie mieści dowolnie dużych liczb, więc dla bardzo dużego N suma przestałaby się w nim mieścić. Największa suma z tego zakresu, 500500, mieści się bez problemu. Dla liczby spoza zakresu, na przykład 1001, program wybiera gałąź `else` i w ogóle nie dochodzi do pętli:

<!-- input: sum_to_n -->
```text
1001
```

<details>
<summary>Standardowe wyjście dla 1001</summary>

<!-- output: sum_to_n -->
```text
Enter N (0-1000):
N must be from 0 to 1000
```

</details>

Taką sumę da się też obliczyć wzorem, bez pętli. Tutaj jednak chodzi o to, jak pętla gromadzi wynik.

## 6. Trzy role zmiennych

W pętlach często spotkasz trzy role:

| Rola | Co robi | Jak się zmienia | Przykład |
|---|---|---|---|
| **licznik przebiegów** | mówi, który to przebieg, i decyduje, kiedy skończyć | w każdym przebiegu o tyle samo | `number` |
| **akumulator** | gromadzi wynik z wartości przetwarzanych w kolejnych przebiegach | o wartość z bieżącego przebiegu | `total` |
| **licznik zdarzeń** | liczy, ile razy zaszła określona sytuacja | tylko wtedy, gdy ta sytuacja zachodzi | `even_count` niżej |

Ten program sumuje liczby od 1 do 6 i przy okazji liczy, ile z nich jest parzystych:

<!-- example: sum_and_evens -->
```cpp
#include <iostream>

int main() {
    const int limit{6};
    int number{1};
    int total{0};
    int even_count{0};

    while (number <= limit) {
        total += number;

        if (number % 2 == 0) {
            even_count += 1;
        }

        number = number + 1;
    }

    std::cout << "Total: " << total << "\n";
    std::cout << "Even numbers: " << even_count << "\n";
}
```

**Przewidź** obie linijki wyniku, a potem uruchom program.

<details>
<summary>Wynik programu</summary>

<!-- output: sum_and_evens -->
```text
Total: 21
Even numbers: 3
```

`total` rośnie w **każdym** przebiegu, o bieżącą liczbę. `even_count` rośnie o 1 **tylko** w przebiegach z liczbą parzystą (2, 4 i 6), bo jego aktualizacja stoi w bloku `if`. Tu `+=` dodaje 1, bo jedno zdarzenie zwiększa licznik o jeden.

</details>

Nie każda pętla potrzebuje wszystkich trzech ról. I nie każda suma pochodzi z licznika: w następnym punkcie sumowane wartości przychodzą od użytkownika.

## 7. Sumowanie wartości z wejścia

Program pyta trzy razy o czas treningu w minutach i sumuje odpowiedzi. W każdym przebiegu:

1. odczytuje jeden czas;
2. dodaje go do sumy;
3. zmienia licznik przebiegów.

Użytkownik wpisuje kolejno 20, 35 i 15. **Przewidź**, bez pisania programu: przepisz tabelę i wypełnij ją.

| Przebieg | Odczytany czas | Suma przed dodaniem | Suma po dodaniu |
|---|---|---|---|
| 1 | | | |
| 2 | | | |
| 3 | | | |

Jaka jest suma na końcu? I czym różni się tu rola licznika od roli odczytanego czasu? Odpowiedź jest w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 8. Znajdź błąd: zgubiona suma

Wymaganie jest takie jak w punkcie 5: program wypisuje sumę liczb od 1 do N. W tej wersji ktoś dopisał jedną linijkę:

<!-- example: sum_reset_bug -->
```cpp
#include <iostream>

int main() {
    int limit{0};

    std::cout << "Enter N (0-1000):\n";
    std::cin >> limit;

    if (limit >= 0 && limit <= 1000) {
        int total{0};
        int number{1};

        while (number <= limit) {
            total = 0;
            total += number;
            number = number + 1;
        }

        std::cout << "Total: " << total << "\n";
    } else {
        std::cout << "N must be from 0 to 1000\n";
    }
}
```

1. **Przewidź**, co program **powinien** wypisać dla N równego 0, 1 i 3.
2. Przewidź, co wypisze **ten** program. Wypełnij tabelę przebiegu dla N = 3.
3. Uruchom program dla 0, 1 i 3.
4. Znajdź pierwszy przypadek, w którym wynik nie zgadza się z wymaganiem.
5. Wskaż linijkę, w której gubiona jest dotychczasowa suma.
6. Popraw program.
7. Sprawdź ponownie wszystkie trzy przypadki.

Wyniki programu przed poprawką i poprawka są w części [Przykładowe rozwiązania](#przykładowe-rozwiązania). Zajrzyj tam po własnej próbie.

## 9. Misja: łączna waga paczek

Magazyn przygotowuje paczki do wysyłki. Program pyta o liczbę paczek, a potem o wagę każdej z nich w kilogramach. Po odczytaniu wszystkich wag wypisuje ich łączną wagę.

**Wymagania:**

- Liczba paczek to liczba całkowita od 0 do 5.
- Waga paczki to liczba z częścią ułamkową, nie mniejsza od zera.
- Każdą wagę program odczytuje w osobnym przebiegu pętli, po prośbie `Enter parcel weight:`. Prośba pojawia się raz na każdą paczkę.
- Program nie musi pamiętać wszystkich wag naraz. Wystarczy, że gromadzi ich sumę.
- Dla 0 paczek program nie pyta o żadną wagę i wypisuje sumę 0.
- Dla liczby paczek spoza zakresu program wypisuje tylko `Invalid parcel count` i nie pyta o żadną wagę.
- Zakładamy, że użytkownik wpisuje liczby i że dla dopuszczalnej liczby paczek poda wszystkie wagi. Program **nie jest** odporny na inne dane, na przykład tekst zamiast liczby. To przyjdzie w dalszych lekcjach.

W `cpp-workspace` utwórz katalog `parcel_weights`, skopiuj do niego `CMakeLists.txt` z oryginalnego `lesson_05_first_program`, utwórz pusty `main.cpp` i napisz program samodzielnie.

Dla trzech paczek o wagach 1.25, 2.5 i 0.75 standardowe wyjście ma być takie:

<!-- input: parcel_weights -->
```text
3
1.25
2.5
0.75
```

<!-- output: parcel_weights -->
```text
Enter parcel count:
Enter parcel weight:
Enter parcel weight:
Enter parcel weight:
Total weight: 4.5 kg
```

Dla 0 paczek:

<!-- input: parcel_weights -->
```text
0
```

<!-- output: parcel_weights -->
```text
Enter parcel count:
Total weight: 0 kg
```

**To nie jest suma od 1 do N.** Tam sumowane były kolejne wartości licznika. Tutaj licznik mówi tylko, **ile** paczek obsłużyć, a sumowane wartości przychodzą osobno, ze standardowego wejścia, i są typu `double`. Licznik i dodawana waga to dwie różne zmienne o różnych rolach. Musisz samodzielnie zdecydować:

1. jaką wartość początkową ma akumulator i gdzie go zadeklarować;
2. jak w każdym przebiegu odczytać jedną wagę i dodać ją do sumy;
3. jak zmieniać licznik i kiedy zakończyć odczytywanie;
4. co program robi dla zera paczek.

**Zanim napiszesz program**, przygotuj dwie rzeczy:

- tabelę przebiegu dla trzech paczek z przykładu: odczytana waga, suma przed dodaniem i suma po dodaniu;
- tabelę przypadków testowych: zero paczek, jedna paczka, kilka paczek, największa dopuszczalna liczba paczek i liczby tuż poza zakresem z obu stron. Przy każdym przypadku zapisz oczekiwane standardowe wyjście, łącznie z liczbą próśb o wagę.

### Kryterium sukcesu

- Program buduje się jako C++20, a jego standardowe wyjście dla obu przykładów jest dokładnie takie jak powyżej.
- Dla każdej liczby paczek od 0 do 5 program prosi o wagę dokładnie tyle razy, ile jest paczek, i wypisuje ich sumę. Dla każdej innej liczby wypisuje tylko `Invalid parcel count`.
- Suma jest gromadzona w akumulatorze typu `double`, zadeklarowanym z wartością początkową, i aktualizowana w każdym przebiegu.
- Licznik paczek i odczytana waga to osobne zmienne.
- Pętla `while` ma klamry, a zakres liczby paczek jest sprawdzany, zanim program zacznie odczytywać wagi.
- Tabela przebiegu i tabela przypadków powstały przed uruchomieniem programu.
- Umiesz wyjaśnić, dlaczego dla zera paczek suma wynosi 0, a program nie pyta o wagę.

Gdy wynik się zgadza, możesz zapisać projekt w Gicie, jak w lekcji 1.5.

<details>
<summary>Podpowiedź 1</summary>

Zastanów się, jaka wartość oznacza brak zgromadzonej wagi.

</details>

<details>
<summary>Podpowiedź 2</summary>

Oddziel zmienną określającą numer paczki od zmiennej przechowującej sumę.

</details>

<details>
<summary>Podpowiedź 3</summary>

Każdy przebieg pętli powinien odczytać jedną wagę i zmienić łączną sumę.

</details>

<details>
<summary>Pełna lista przypadków kontrolnych: otwórz po przygotowaniu własnej tabeli</summary>

| Liczba paczek | Wagi | Prośby o wagę | Ostatnia linijka | Co sprawdza |
|---|---|---|---|---|
| 3 | 1.25, 2.5, 0.75 | 3 | `Total weight: 4.5 kg` | kilka przebiegów |
| 0 | — | 0 | `Total weight: 0 kg` | zero przebiegów |
| 1 | 1.25 | 1 | `Total weight: 1.25 kg` | jeden przebieg |
| 5 | 0.5, 1.25, 2, 0.75, 3 | 5 | `Total weight: 7.5 kg` | największa dopuszczalna liczba paczek |
| -1 | — | 0 | `Invalid parcel count` | tuż pod zakresem |
| 6 | — | 0 | `Invalid parcel count` | tuż nad zakresem |

Przypadki z trzema i zerem paczek są sprawdzone wyżej, przy treści misji. Wagi wybrano tak, żeby sumy dało się zapisać dokładnie, bez zaokrągleń.

<!-- input: parcel_weights -->
```text
1
1.25
```

<!-- output: parcel_weights -->
```text
Enter parcel count:
Enter parcel weight:
Total weight: 1.25 kg
```

<!-- input: parcel_weights -->
```text
5
0.5
1.25
2
0.75
3
```

<!-- output: parcel_weights -->
```text
Enter parcel count:
Enter parcel weight:
Enter parcel weight:
Enter parcel weight:
Enter parcel weight:
Enter parcel weight:
Total weight: 7.5 kg
```

<!-- input: parcel_weights -->
```text
-1
```

<!-- output: parcel_weights -->
```text
Enter parcel count:
Invalid parcel count
```

<!-- input: parcel_weights -->
```text
6
```

<!-- output: parcel_weights -->
```text
Enter parcel count:
Invalid parcel count
```

</details>

### Wariant dla chętnych: ciężkie paczki

Ten wariant nie jest wymagany. Program ma dodatkowo policzyć, ile paczek waży **co najmniej 2 kg**, i po linijce z łączną wagą wypisać `Heavy parcels: K`. Potrzebujesz osobnego licznika zdarzeń i `if`, jak w punkcie 6. Przewidź wynik dla pięciu paczek z listy kontrolnej, a potem sprawdź.

<details>
<summary>Przypadki wariantu: otwórz po własnej próbie</summary>

<!-- input: parcel_weights_heavy -->
```text
5
0.5
1.25
2
0.75
3
```

<!-- output: parcel_weights_heavy -->
```text
Enter parcel count:
Enter parcel weight:
Enter parcel weight:
Enter parcel weight:
Enter parcel weight:
Enter parcel weight:
Total weight: 7.5 kg
Heavy parcels: 2
```

<!-- input: parcel_weights_heavy -->
```text
3
1.25
2.5
0.75
```

<!-- output: parcel_weights_heavy -->
```text
Enter parcel count:
Enter parcel weight:
Enter parcel weight:
Enter parcel weight:
Total weight: 4.5 kg
Heavy parcels: 1
```

<!-- input: parcel_weights_heavy -->
```text
0
```

<!-- output: parcel_weights_heavy -->
```text
Enter parcel count:
Total weight: 0 kg
Heavy parcels: 0
```

Paczka o wadze dokładnie 2 kg się liczy, bo wymaganie mówi „co najmniej”.

</details>

Przykładowe rozwiązania są w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 10. Gdy coś pójdzie inaczej

| Co widzisz | Co to znaczy | Co zrobić |
|---|---|---|
| Wypisana suma to tylko ostatnia wartość | Akumulator jest zerowany w ciele pętli, więc każdy przebieg zaczyna od nowa. | Ustaw wartość początkową raz, przed pętlą (punkt 8). |
| `use of undeclared identifier` dla sumy po pętli | Akumulator jest zadeklarowany w ciele pętli, więc za pętlą już nie istnieje (lekcja 3.2). | Zadeklaruj go przed pętlą. |
| Suma jest o jedną wartość za mała albo za duża | Błąd o jeden krok w warunku albo w wartości początkowej licznika. | Sprawdź przypadki z jednym przebiegiem i z największą wartością. Wypełnij tabelę przebiegu. |
| Suma wag nie ma części ułamkowej | Akumulator albo zmienna z wagą jest typu `int`. | Wagę i sumę wag przechowuj w `double`. |
| Prośba o wagę pojawia się za dużo albo za mało razy | Odczyt stoi poza pętlą albo licznik zmienia się źle. | Odczyt i prośba o wagę muszą być w ciele pętli, raz na przebieg. |
| Dla zera paczek program czeka na dane | Program odczytuje wagę przed pętlą albo poza nią. | Dla zera paczek ciało pętli nie wykonuje się ani razu, więc żaden odczyt wagi nie może stać poza nim. |
| Program nic nie robi i czeka | Czeka na kolejną wagę: wpisano mniej wag niż paczek. | Wpisz brakujące wagi i naciśnij **Enter**. |

## 11. Wyjaśnij

Odpowiedz własnymi słowami, najlepiej na piśmie. Dopiero potem porównaj z przykładową odpowiedzią.

**1.** Czym jest akumulator i dlaczego zwykle zaczyna od 0?

<details>
<summary>Przykładowa odpowiedź</summary>

To zwykła zmienna, która w kolejnych przebiegach gromadzi wynik, tutaj sumę. Przed pierwszym przebiegiem nic jeszcze nie zsumowano, a 0 niczego nie zmienia w sumie. Dlatego dla zera przebiegów wynik to 0.

</details>

**2.** Czym różni się licznik przebiegów od akumulatora?

<details>
<summary>Przykładowa odpowiedź</summary>

Licznik mówi, który to przebieg, i decyduje, kiedy pętla się kończy. Zmienia się w każdym przebiegu o tyle samo. Akumulator gromadzi wynik i zmienia się o wartość z bieżącego przebiegu, na przykład o odczytaną wagę.

</details>

**3.** Co robi `total += number;`?

<details>
<summary>Przykładowa odpowiedź</summary>

Zwiększa wartość istniejącej zmiennej `total` o wartość `number`. W naszych przykładach robi to samo co `total = total + number;`.

</details>

**4.** Dlaczego program z punktu 8 dawał dobry wynik dla N równego 1, a zły dla 3?

<details>
<summary>Przykładowa odpowiedź</summary>

Bo zerowanie w ciele pętli kasuje sumę z poprzednich przebiegów. Przy jednym przebiegu nie ma czego skasować: 0 + 1 to poprawny wynik. Błąd widać dopiero przy kilku przebiegach, gdy wynik powinien zależeć od wcześniejszych dodań.

</details>

**5.** Czym różni się `int total{0};` przed pętlą od `total = 0;` w jej ciele?

<details>
<summary>Przykładowa odpowiedź</summary>

Wartość początkowa przed pętlą ustawia sumę raz, zanim zacznie się gromadzenie. Przypisanie w ciele pętli wykonuje się w każdym przebiegu i za każdym razem wyrzuca to, co już zgromadzono.

</details>

**6.** Dlaczego w misji sumę wag przechowujesz w `double`?

<details>
<summary>Przykładowa odpowiedź</summary>

Bo wagi mają część ułamkową. Suma typu `int` gubiłaby tę część, a `+=` nie zgłosiłby błędu tak jak inicjalizacja przez `{}`.

</details>

**7.** Dlaczego dla zera paczek program nie pyta o wagę?

<details>
<summary>Przykładowa odpowiedź</summary>

Bo odczyt wagi stoi w ciele pętli, a dla zera paczek warunek jest fałszywy już przy pierwszym sprawdzeniu. Ciało nie wykonuje się ani razu, a suma zostaje równa wartości początkowej 0.

</details>

## Podsumowanie

- **Akumulator** to zwykła zmienna, która w kolejnych przebiegach gromadzi wynik, na przykład sumę.
- Akumulator dostaje wartość początkową **przed pętlą**. Dla sumy jest to 0: wynik dla zera przebiegów.
- W każdym przebiegu akumulator zmienia się na podstawie swojej dotychczasowej wartości: `total = total + number;` albo krócej `total += number;`.
- `+=` zwiększa istniejącą zmienną o wartość z prawej strony. Nie chroni przed zawężeniem typu, więc typ akumulatora dobieraj do sumowanych wartości.
- **Licznik przebiegów** decyduje, kiedy skończyć, **akumulator** gromadzi wynik, a **licznik zdarzeń** rośnie tylko wtedy, gdy zajdzie określona sytuacja.
- Sumowane wartości nie muszą pochodzić z licznika. Mogą przychodzić ze standardowego wejścia, po jednej na przebieg.
- Zerowanie akumulatora w ciele pętli gubi wcześniejszy wynik. Taki błąd ujawnia dopiero test z kilkoma przebiegami, nie z jednym.

## Co dalej

Pętle z tej lekcji i z lekcji 4.1 mają zawsze te same części: licznik z wartością początkową, warunek i zmianę licznika na końcu ciała. W lekcji 4.3 poznasz pętlę `for`, która zbiera te trzy części w jednej linijce. **Lekcja 4.3 jest w przygotowaniu.**

---

## Przykładowe rozwiązania

Zajrzyj tutaj **po własnej próbie**. Twoje nazwy mogą się różnić, jeśli standardowe wyjście jest takie, jak wymagane.

<details>
<summary>Punkt 3: tabela przebiegu dla liczb od 1 do 4</summary>

| Sprawdzenie warunku | `number` | `number <= 4` | `total` przed dodaniem | Dodawana wartość | `total` po dodaniu | `number` po ciele |
|---|---|---|---|---|---|---|
| 1 | 1 | `true` | 0 | 1 | 1 | 2 |
| 2 | 2 | `true` | 1 | 2 | 3 | 3 |
| 3 | 3 | `true` | 3 | 3 | 6 | 4 |
| 4 | 4 | `true` | 6 | 4 | 10 | 5 |
| 5 | 5 | `false` | — | — | — | — |

Pięć sprawdzeń warunku, cztery przebiegi. Program wypisuje `Total: 10`.

</details>

<details>
<summary>Punkt 7: trzy czasy treningu</summary>

| Przebieg | Odczytany czas | Suma przed dodaniem | Suma po dodaniu |
|---|---|---|---|
| 1 | 20 | 0 | 20 |
| 2 | 35 | 20 | 55 |
| 3 | 15 | 55 | 70 |

Suma na końcu to 70 minut. Licznik mówi tylko, który to przebieg i kiedy skończyć po trzecim. Do sumy trafiają **odczytane czasy**, a nie wartości licznika.

</details>

<details>
<summary>Punkt 8: wyniki przed poprawką i poprawka</summary>

Przed poprawką, dla 0, 1 i 3:

<!-- input: sum_reset_bug -->
```text
0
```

<!-- output: sum_reset_bug -->
```text
Enter N (0-1000):
Total: 0
```

<!-- input: sum_reset_bug -->
```text
1
```

<!-- output: sum_reset_bug -->
```text
Enter N (0-1000):
Total: 1
```

<!-- input: sum_reset_bug -->
```text
3
```

<!-- output: sum_reset_bug -->
```text
Enter N (0-1000):
Total: 3
```

| Sprawdzenie warunku | `number` | `number <= 3` | `total` po `total = 0;` | `total` po dodaniu |
|---|---|---|---|---|
| 1 | 1 | `true` | 0 | 1 |
| 2 | 2 | `true` | 0 | 2 |
| 3 | 3 | `true` | 0 | 3 |
| 4 | 4 | `false` | — | — |

- **Pierwszy niezgodny przypadek** to 3: wymaganie mówi 6, a program wypisuje 3, czyli tylko ostatnią dodaną liczbę.
- **Dlaczego 0 i 1 nie wystarczyły:** dla 0 pętla się nie wykonuje, a dla jednego przebiegu zerowanie nie ma czego skasować. Oba wyniki są poprawne, choć program jest błędny.
- **Przyczyna:** `total = 0;` w ciele pętli wykonuje się w każdym przebiegu i wyrzuca sumę z poprzednich przebiegów.
- **Poprawka:** usuń tę linijkę. Wartość początkową 0 suma dostaje raz, przed pętlą, w deklaracji `int total{0};`. Poprawiony program to program z punktu 5. Jego wyniki dla 0, 1 i 3 są sprawdzone tam.

</details>

<details>
<summary>Punkt 9: misja, łączna waga paczek</summary>

<!-- example: parcel_weights -->
```cpp
#include <iostream>

int main() {
    int parcel_count{0};

    std::cout << "Enter parcel count:\n";
    std::cin >> parcel_count;

    if (parcel_count >= 0 && parcel_count <= 5) {
        double total_weight{0.0};
        int parcel{1};

        while (parcel <= parcel_count) {
            double weight{0.0};

            std::cout << "Enter parcel weight:\n";
            std::cin >> weight;
            total_weight += weight;
            parcel = parcel + 1;
        }

        std::cout << "Total weight: " << total_weight << " kg\n";
    } else {
        std::cout << "Invalid parcel count\n";
    }
}
```

| Sprawdzenie warunku | `parcel` | `parcel <= 3` | Odczytana waga | `total_weight` przed | `total_weight` po |
|---|---|---|---|---|---|
| 1 | 1 | `true` | 1.25 | 0 | 1.25 |
| 2 | 2 | `true` | 2.5 | 1.25 | 3.75 |
| 3 | 3 | `true` | 0.75 | 3.75 | 4.5 |
| 4 | 4 | `false` | — | — | — |

- **Akumulator** `total_weight` jest typu `double` i zaczyna od 0.0, przed pętlą. Dla zera paczek zostaje równy 0, a `std::cout` wypisuje go jako `0`.
- **Licznik** `parcel` mówi tylko, którą paczkę obsługuje przebieg. Do sumy trafia **odczytana waga**, a nie licznik.
- **Odczyt** stoi w ciele pętli, więc prośba o wagę pojawia się dokładnie raz na paczkę i ani razu dla zera paczek.
- `weight` jest zadeklarowane w ciele pętli, bo potrzebne jest tylko w jednym przebiegu. Możesz też zadeklarować je przed pętlą: wynik będzie taki sam.

</details>

<details>
<summary>Punkt 9: wariant, ciężkie paczki</summary>

<!-- example: parcel_weights_heavy -->
```cpp
#include <iostream>

int main() {
    int parcel_count{0};

    std::cout << "Enter parcel count:\n";
    std::cin >> parcel_count;

    if (parcel_count >= 0 && parcel_count <= 5) {
        double total_weight{0.0};
        int heavy_parcels{0};
        int parcel{1};

        while (parcel <= parcel_count) {
            double weight{0.0};

            std::cout << "Enter parcel weight:\n";
            std::cin >> weight;
            total_weight += weight;

            if (weight >= 2.0) {
                heavy_parcels += 1;
            }

            parcel = parcel + 1;
        }

        std::cout << "Total weight: " << total_weight << " kg\n";
        std::cout << "Heavy parcels: " << heavy_parcels << "\n";
    } else {
        std::cout << "Invalid parcel count\n";
    }
}
```

`heavy_parcels` to licznik zdarzeń: rośnie o 1 tylko wtedy, gdy odczytana waga to co najmniej 2 kg.

</details>

**Poprzednia lekcja:** [Lekcja 4.1: Pierwsza pętla (`while`)](lesson_01_the_first_loop.md) · **Następna lekcja:** w przygotowaniu · [Opis kursu](../../README.md)

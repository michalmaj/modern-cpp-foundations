# Lekcja 2.2: Gdy wartości się zmieniają

**Polski** · [English](lesson_02_when_values_change.en.md) · [Opis kursu](../../README.md)

> **Moduł 2, lekcja 2** · około 60 minut
> **Potrzebujesz:** katalogu `cpp-workspace` i oryginalnego projektu `lesson_05_first_program`, jak dotąd.
> **Wersja pilotażowa.** Przykłady z tej lekcji sprawdzamy automatycznie na Windowsie, Ubuntu i macOS.

## Zanim zaczniesz

Ta lekcja zakłada, że po lekcji 2.1:

- tworzysz zmienne typu `int` z wartością początkową, na przykład `int ticket_count{3};`;
- używasz ich w obliczeniach z `+`, `-` i `*`;
- wypisujesz tekst i wartości w jednej instrukcji, z kilkoma `<<`.

## Sytuacja

W lekcji 2.1 każda zmienna dostawała wartość raz, przy tworzeniu, i potem już jej nie zmieniała. Prawdziwe programy często śledzą coś, co się zmienia: liczbę wolnych miejsc, punkty w grze, stan licznika. Dziś zmienisz wartość istniejącej zmiennej, nauczysz się przewidywać wartości krok po kroku i oznaczysz te wartości, które zmieniać się **nie** powinny.

Po tej lekcji będziesz:

- odróżniać inicjalizację zmiennej od późniejszego przypisania;
- wyjaśniać, co robi `=` w instrukcji `count = count + 1;`;
- przewidywać wartości zmiennych po kolejnych instrukcjach i zapisywać je w tabeli;
- wiedzieć, że po przypisaniu jednej zmiennej `int` do drugiej obie dalej są niezależne;
- tworzyć stałe `const int` i rozumieć, dlaczego nie można ich później zmienić;
- samodzielnie pisać program, w którym wartości zmieniają się w określonej kolejności.

## 1. Przygotuj projekt

W `cpp-workspace` utwórz katalog `lesson_2_2` i skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program`. Programy z tej lekcji wpisujesz w `main.cpp` tego katalogu.

## 2. Wartość się zmienia

Zastąp zawartość `main.cpp` tym programem:

<!-- example: seats_left -->
```cpp
#include <iostream>

int main() {
    int seats_left{12};
    std::cout << "Seats left: " << seats_left << "\n";

    seats_left = seats_left - 3;
    std::cout << "Seats left: " << seats_left << "\n";
}
```

**Przewidź**, co wypiszą obie linijki z `std::cout`. Zapisz odpowiedź, a potem uruchom program.

<details>
<summary>Wynik programu</summary>

<!-- output: seats_left -->
```text
Seats left: 12
Seats left: 9
```

</details>

**Co się stało, linijka po linijce?**

1. `int seats_left{12};` to znana z lekcji 2.1 **deklaracja z inicjalizacją**. Powstaje zmienna `seats_left` z wartością początkową `12`.
2. Pierwsze `std::cout` wypisuje aktualną wartość: `12`.
3. `seats_left = seats_left - 3;` to **przypisanie**. Nie ma tu typu `int` na początku, więc nie powstaje nowa zmienna: zmienia się wartość tej, która już istnieje.
4. Drugie `std::cout` wypisuje nową wartość: `9`.

**Jak czytać `=` w przypisaniu.** W matematyce `x = x - 3` byłoby równaniem bez rozwiązania. W C++ `=` nie jest równaniem i niczego nie porównuje. To **polecenie** w dwóch krokach:

1. najpierw program **oblicza prawą stronę**: bierze aktualną wartość `seats_left` (12) i odejmuje 3, co daje 9;
2. potem **zapisuje wynik** w zmiennej po lewej stronie. Poprzednia wartość, 12, zostaje zastąpiona.

Czytaj to więc jako „`seats_left` dostaje wartość `seats_left - 3`”, a nie „`seats_left` równa się …”. Sprawdzanie, czy dwie wartości są równe, to osobny zapis, który poznasz w Module 3.

**Kolejność ma znaczenie.** Instrukcje wykonują się od góry do dołu, jak w Module 1. Pierwsze `std::cout` stoi przed przypisaniem, więc wypisuje starą wartość. Gdyby obie linijki z `std::cout` stały pod przypisaniem, obie wypisałyby `9`.

## 3. Inicjalizacja a przypisanie

| Zapis | Co robi |
|---|---|
| `int count{3};` | **Deklaracja z inicjalizacją:** tworzy nową zmienną `count` i nadaje jej wartość początkową. |
| `count = 5;` | **Przypisanie:** zmienia wartość zmiennej `count`, która już istnieje. Typu się tu nie podaje. |

Zmienną deklarujesz **raz**. Co się stanie, gdy spróbujesz „zmienić wartość” drugą deklaracją? **Przewidź**, a potem zbuduj ten program:

<!-- broken: redefinition at=5:9 errors=1 error=^redefinition of 'count'$ -->
```cpp
#include <iostream>

int main() {
    int count{3};
    int count{5};
    std::cout << count << "\n";
}
```

Kompilator zgłasza `redefinition of 'count'` (ponowna definicja `count`) w linijce 5, a w dodatkowej linijce `note:` wskazuje miejsce pierwszej deklaracji. W jednym `main` nazwa zmiennej może być zadeklarowana tylko raz. Druga deklaracja próbowałaby utworzyć drugą zmienną o tej samej nazwie, a nie zmienić pierwszą.

Popraw program: w linijce 5 usuń `int` i nawiasy klamrowe, tak żeby powstało przypisanie `count = 5;`. Zbuduj i uruchom go ponownie.

<details>
<summary>Poprawiony program i jego wynik</summary>

<!-- example: count_assignment -->
```cpp
#include <iostream>

int main() {
    int count{3};
    count = 5;
    std::cout << count << "\n";
}
```

<!-- output: count_assignment -->
```text
5
```

</details>

Tak jak w lekcji 2.1, zmienna zawsze dostaje wartość od razu przy deklaracji. Przypisanie nie zastępuje inicjalizacji: zmienia wartość, która już jest.

## 4. Przewidź: dwie niezależne zmienne

W tym programie najpierw zmienna `second` dostaje wartość zmiennej `first`, a potem `first` się zmienia.

<!-- example: two_variables -->
```cpp
#include <iostream>

int main() {
    int first{4};
    int second{0};

    second = first;
    first = 9;

    std::cout << "first: " << first << "\n";
    std::cout << "second: " << second << "\n";
}
```

**Przewidź**, zanim uruchomisz program: jaką wartość wypisze `first`, a jaką `second`? Zapisz obie.

<details>
<summary>Wynik programu</summary>

<!-- output: two_variables -->
```text
first: 9
second: 4
```

</details>

**Dlaczego `second` ma nadal `4`?** Przypisanie `second = first;` bierze **wartość**, którą `first` ma **w tej chwili** (4), i zapisuje jej kopię w `second`. Zmienne nie zostają ze sobą połączone. Gdy potem `first` dostaje 9, `second` o tym „nie wie”: dalej przechowuje swoją kopię, czyli 4. Tak zachowują się zmienne typu `int`, takie jak tutaj.

## 5. Śledź wartości krok po kroku

Oto program z kilkoma przypisaniami. Wypisuje tylko wartości końcowe:

<!-- example: trace_final -->
```cpp
#include <iostream>

int main() {
    int points{10};
    int bonus{5};

    points = points + bonus;
    bonus = bonus * 2;
    points = points - bonus;
    bonus = points + 1;

    std::cout << "points: " << points << ", bonus: " << bonus << "\n";
}
```

**Krok 1. Przewidź na papierze.** Przepisz tabelę i wypełnij ją **przed** uruchomieniem programu. W każdym wierszu wpisz wartości obu zmiennych **po** wykonaniu danej linijki.

| Linijka | `points` | `bonus` |
|---|---|---|
| `int points{10};` i `int bonus{5};` | 10 | 5 |
| `points = points + bonus;` | | |
| `bonus = bonus * 2;` | | |
| `points = points - bonus;` | | |
| `bonus = points + 1;` | | |

Pamiętaj: w każdym przypisaniu prawa strona korzysta z wartości **z poprzedniego wiersza**.

**Krok 2. Sprawdź.** Uruchom program i porównaj ostatni wiersz tabeli z wynikiem.

**Krok 3. Sprawdź każdy krok.** Dopisz w programie, pod każdym przypisaniem, instrukcję `std::cout`, która wypisze obie wartości w tej samej postaci co ostatnia linijka programu. Uruchom program i porównaj każdy wypisany wiersz z tabelą. Jeśli któryś się nie zgadza, znajdź pierwszy taki wiersz i sprawdź, z której wartości skorzystano przy obliczaniu prawej strony.

Takie śledzenie wartości to umiejętność, której programiści używają stale. W kolejnych lekcjach przyda się jeszcze nieraz.

## 6. Wartości, które się nie zmieniają: `const`

Na parkingu jest 20 miejsc. Liczba **wolnych** miejsc zmienia się przez cały dzień, ale **pojemność** parkingu się nie zmienia. Gdyby program przez pomyłkę przypisał pojemności nową wartość, wszystkie obliczenia, które z niej korzystają, byłyby błędne.

C++ pozwala oznaczyć taką wartość jako **stałą** słowem `const`:

<!-- example: parking_const -->
```cpp
#include <iostream>

int main() {
    const int parking_capacity{20};
    int available_spaces{12};

    int occupied_spaces{parking_capacity - available_spaces};

    std::cout << "Capacity: " << parking_capacity << "\n";
    std::cout << "Occupied: " << occupied_spaces << "\n";
}
```

<!-- output: parking_const -->
```text
Capacity: 20
Occupied: 8
```

- `const int parking_capacity{20};` tworzy zmienną typu `int`, której wartości **nie można zmienić** po inicjalizacji. Słowo `const` stoi przed typem.
- `available_spaces` nie ma `const`, bo jego wartość ma się zmieniać.
- Stałą można **odczytywać** i używać w obliczeniach, jak każdą zmienną: tutaj w `parking_capacity - available_spaces`.
- Stała musi dostać wartość **od razu**, przy deklaracji. Później nie da się jej nadać.

**Kiedy `const`?** Gdy wartość nie powinna się zmieniać przez cały czas działania programu. W lekcji 2.1 żadna zmienna się nie zmieniała, więc wszystkie mogłyby mieć `const`. Od teraz oznaczaj tak wartości, które mają zostać takie same. Kompilator dopilnuje, żeby nic ich przez pomyłkę nie zmieniło.

### Eksperyment: spróbuj zmienić stałą

Ktoś chce powiększyć parking i dopisuje przypisanie:

<!-- broken: const_assignment at=5 errors=1 error=^cannot assign to variable 'parking_capacity' with const-qualified type 'const int'$ -->
```cpp
#include <iostream>

int main() {
    const int parking_capacity{20};
    parking_capacity = 25;
    std::cout << "Capacity: " << parking_capacity << "\n";
}
```

1. **Przewidź:** czy ten program się zbuduje?
2. Zbuduj go.
3. Znajdź pierwszą istotną informację w wyniku budowania.
4. Wyjaśnij przyczynę własnymi słowami.
5. Przywróć poprawny kod: usuń linijkę z przypisaniem.

<details>
<summary>Wyjaśnienie: przeczytaj po własnej próbie</summary>

Program się nie zbuduje. Kompilator zgłasza w linijce 5 `cannot assign to variable 'parking_capacity' with const-qualified type 'const int'`, czyli: nie można przypisać wartości zmiennej, której typ ma `const`. W linijce `note:` wskazuje deklarację z `const`. To ochrona, którą zamówiło słowo `const`: kompilator nie pozwolił zmienić wartości, która miała zostać stała. Jeśli pojemność parkingu naprawdę ma być inna, zmień jej wartość początkową w deklaracji.

</details>

Podobnie ze stałą bez wartości początkowej. Ten program też się nie zbuduje:

<!-- broken: const_without_value at=4 errors=1 error=^default initialization of an object of const type 'const int'$ -->
```cpp
#include <iostream>

int main() {
    const int parking_capacity;
    std::cout << "Capacity: " << parking_capacity << "\n";
}
```

Kompilator zgłasza `default initialization of an object of const type 'const int'`: stała nie dostała wartości. Stała musi ją dostać przy deklaracji, bo później nie da się jej już nadać.

## 7. Misja: parking przez cały dzień

Mały parking ma 20 miejsc i rano jest pusty. W ciągu dnia:

- rano przyjeżdża 7 samochodów;
- w południe przyjeżdżają jeszcze 4;
- po południu wyjeżdża 6 samochodów.

W `cpp-workspace` utwórz katalog `parking_day`, skopiuj do niego `CMakeLists.txt` z oryginalnego `lesson_05_first_program`, utwórz pusty `main.cpp` i napisz program samodzielnie. Program ma wypisać dokładnie:

<!-- output: parking_day -->
```text
Capacity: 20
Free spaces at opening: 20
Free spaces after the morning: 13
Free spaces after noon: 9
Free spaces after the afternoon: 15
Capacity at closing: 20
```

### Kryterium sukcesu

- Program buduje się jako C++20 i wypisuje dokładnie powyższy wynik.
- Pojemność parkingu to `const int`.
- Liczba wolnych miejsc to zwykła zmienna `int`, z wartością początkową przy deklaracji, zmieniana **przypisaniem** po każdym zdarzeniu.
- Wartości 13, 9 i 15 **oblicza program**: nie występują w kodzie.
- Zdarzenia zachodzą w podanej kolejności, a wynik jest wypisywany po każdym z nich.
- Program używa tylko tego, co już znasz: `int`, `const`, `{}`, `=`, `+`, `-`, `*` i `std::cout`.
- Umiesz wyjaśnić, dlaczego pojemność ma `const`, a liczba wolnych miejsc nie.

Gdy wynik się zgadza, możesz zapisać projekt w Gicie, jak w lekcji 1.5.

<details>
<summary>Podpowiedź 1</summary>

Która wartość ma być taka sama przez cały dzień, a która się zmienia? Od tego zależy, gdzie użyjesz `const`.

</details>

<details>
<summary>Podpowiedź 2</summary>

Każde zdarzenie to jedno przypisanie do liczby wolnych miejsc, a pod nim jedno `std::cout`. Przyjazd samochodów zmniejsza liczbę wolnych miejsc, a wyjazd ją zwiększa.

</details>

### Wariant: inny poranek

Rano przyjeżdża nie 7, lecz 8 samochodów. **Przewidź** trzy nowe wartości wolnych miejsc, a potem zmień w programie **jedną liczbę**, zbuduj go i uruchom. Wynik ma być taki:

<!-- output: parking_day_variant -->
```text
Capacity: 20
Free spaces at opening: 20
Free spaces after the morning: 12
Free spaces after noon: 8
Free spaces after the afternoon: 14
Capacity at closing: 20
```

Przykładowe rozwiązania są w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 8. Gdy coś pójdzie inaczej

| Co widzisz | Co to znaczy | Co zrobić |
|---|---|---|
| `redefinition of '…'` | Ta sama nazwa została zadeklarowana drugi raz, z typem na początku. | Aby zmienić wartość istniejącej zmiennej, użyj przypisania bez typu: `count = 5;`. |
| `cannot assign to variable '…' with const-qualified type …` | Próbujesz zmienić stałą. | Jeśli wartość ma się zmieniać, usuń `const` z deklaracji. Jeśli nie, usuń przypisanie. |
| `use of undeclared identifier '…'` przy przypisaniu | Przypisanie stoi wyżej niż deklaracja albo nazwa ma literówkę. | Zmienną najpierw deklarujesz, potem jej przypisujesz. Porównaj nazwy znak po znaku. |
| Wypisana wartość jest „o krok” za stara albo za nowa | `std::cout` stoi w złym miejscu względem przypisania. | Instrukcje wykonują się od góry do dołu. Przesuń `std::cout` pod przypisanie, którego wynik ma pokazać. |
| Wartość się nie zmienia, choć jest linijka z odejmowaniem, na przykład `seats_left - 3;` | Program oblicza wynik, ale nigdzie go nie zapisuje. Kompilator może przy tym wypisać ostrzeżenie (`warning`). | Zapisz wynik przypisaniem: `seats_left = seats_left - 3;`. |
| Zmiana jednej zmiennej „nie przeniosła się” na drugą | Tak ma być: przypisanie kopiuje wartość (punkt 4). | Jeśli druga zmienna ma mieć nową wartość, przypisz ją ponownie po zmianie. |

## 9. Wyjaśnij

Odpowiedz własnymi słowami, najlepiej na piśmie. Dopiero potem porównaj z przykładową odpowiedzią.

**1.** Czym różni się `int count{3};` od `count = 5;`?

<details>
<summary>Przykładowa odpowiedź</summary>

Pierwsze tworzy nową zmienną `count` z wartością początkową 3. Drugie zmienia wartość istniejącej zmiennej na 5.

</details>

**2.** Co dokładnie robi program, wykonując `count = count + 1;`?

<details>
<summary>Przykładowa odpowiedź</summary>

Najpierw oblicza prawą stronę: bierze aktualną wartość `count` i dodaje 1. Potem zapisuje wynik w `count`, a poprzednia wartość znika. To nie jest równanie, tylko polecenie.

</details>

**3.** Dlaczego w punkcie 4 `second` ma `4`, choć `first` ma na końcu `9`?

<details>
<summary>Przykładowa odpowiedź</summary>

Bo `second = first;` skopiowało wartość, którą `first` miało w tamtej chwili, czyli 4. Późniejsza zmiana `first` nie zmienia `second`.

</details>

**4.** W misji: dlaczego pojemność ma `const`, a liczba wolnych miejsc nie?

<details>
<summary>Przykładowa odpowiedź</summary>

Pojemność parkingu jest przez cały dzień taka sama, a `const` sprawia, że kompilator nie pozwoli jej przez pomyłkę zmienić. Liczba wolnych miejsc musi się zmieniać po każdym zdarzeniu, więc nie może być stałą.

</details>

**5.** Jak sprawdzić, czy przewidywania w tabeli z punktu 5 są poprawne dla każdego kroku, a nie tylko dla wyniku końcowego?

<details>
<summary>Przykładowa odpowiedź</summary>

Dopisać pod każdym przypisaniem `std::cout`, które wypisze aktualne wartości, i porównać każdy wypisany wiersz z odpowiednim wierszem tabeli. Pierwszy niezgodny wiersz pokazuje, gdzie przewidywanie się rozjechało.

</details>

## Podsumowanie

- **Inicjalizacja** (`int count{3};`) tworzy zmienną i nadaje jej wartość początkową. **Przypisanie** (`count = 5;`) zmienia wartość zmiennej, która już istnieje.
- `=` w przypisaniu to nie równanie: najpierw obliczana jest prawa strona, potem wynik trafia do zmiennej po lewej.
- Instrukcje wykonują się po kolei. Wartość zmiennej zależy od tego, które przypisania już się wykonały.
- Przypisanie jednej zmiennej `int` do drugiej kopiuje wartość. Zmienne pozostają niezależne.
- `const` oznacza wartość, która nie może się zmienić po inicjalizacji. Stałą można odczytywać, ale nie można jej przypisać nowej wartości, a kompilator tego pilnuje.
- Tabela wartości i dodatkowe `std::cout` pomagają sprawdzić, co program robi krok po kroku.

## Co dalej

Umiesz już przewidywać i sprawdzać, jak wartości zmieniają się krok po kroku. W lekcji 2.3 zobaczysz te zmiany w działającym programie, za pomocą debuggera, i znajdziesz instrukcję, która psuje wynik: [Lekcja 2.3: Zobacz, co dzieje się w programie](lesson_03_see_what_happens_in_the_program.md).

---

## Przykładowe rozwiązania

Zajrzyj tutaj **po własnej próbie**. Twoje nazwy i postać wypisywanych linijek mogą się różnić, jeśli wynik jest taki, jak wymagany.

<details>
<summary>Punkt 5: tabela i program z wypisaniem każdego kroku</summary>

| Linijka | `points` | `bonus` |
|---|---|---|
| `int points{10};` i `int bonus{5};` | 10 | 5 |
| `points = points + bonus;` | 15 | 5 |
| `bonus = bonus * 2;` | 15 | 10 |
| `points = points - bonus;` | 5 | 10 |
| `bonus = points + 1;` | 5 | 6 |

<!-- example: trace_steps -->
```cpp
#include <iostream>

int main() {
    int points{10};
    int bonus{5};

    points = points + bonus;
    std::cout << "points: " << points << ", bonus: " << bonus << "\n";
    bonus = bonus * 2;
    std::cout << "points: " << points << ", bonus: " << bonus << "\n";
    points = points - bonus;
    std::cout << "points: " << points << ", bonus: " << bonus << "\n";
    bonus = points + 1;
    std::cout << "points: " << points << ", bonus: " << bonus << "\n";
}
```

<!-- output: trace_steps -->
```text
points: 15, bonus: 5
points: 15, bonus: 10
points: 5, bonus: 10
points: 5, bonus: 6
```

Ostatni wiersz to wynik oryginalnego programu:

<!-- output: trace_final -->
```text
points: 5, bonus: 6
```

Najczęstsza pomyłka to użycie w trzecim przypisaniu starej wartości `bonus` (5), a nie już zmienionej (10).

</details>

<details>
<summary>Punkt 7: misja, parking przez cały dzień</summary>

<!-- example: parking_day -->
```cpp
#include <iostream>

int main() {
    const int parking_capacity{20};
    int free_spaces{parking_capacity};

    std::cout << "Capacity: " << parking_capacity << "\n";
    std::cout << "Free spaces at opening: " << free_spaces << "\n";

    free_spaces = free_spaces - 7;
    std::cout << "Free spaces after the morning: " << free_spaces << "\n";

    free_spaces = free_spaces - 4;
    std::cout << "Free spaces after noon: " << free_spaces << "\n";

    free_spaces = free_spaces + 6;
    std::cout << "Free spaces after the afternoon: " << free_spaces << "\n";

    std::cout << "Capacity at closing: " << parking_capacity << "\n";
}
```

- Pojemność się nie zmienia, więc ma `const`.
- Rano parking jest pusty, dlatego `free_spaces` zaczyna od wartości pojemności, a nie od wpisanej drugi raz liczby 20.
- Każde zdarzenie to jedno przypisanie. Przyjazd odejmuje, wyjazd dodaje.

</details>

<details>
<summary>Punkt 7: wariant</summary>

<!-- example: parking_day_variant -->
```cpp
#include <iostream>

int main() {
    const int parking_capacity{20};
    int free_spaces{parking_capacity};

    std::cout << "Capacity: " << parking_capacity << "\n";
    std::cout << "Free spaces at opening: " << free_spaces << "\n";

    free_spaces = free_spaces - 8;
    std::cout << "Free spaces after the morning: " << free_spaces << "\n";

    free_spaces = free_spaces - 4;
    std::cout << "Free spaces after noon: " << free_spaces << "\n";

    free_spaces = free_spaces + 6;
    std::cout << "Free spaces after the afternoon: " << free_spaces << "\n";

    std::cout << "Capacity at closing: " << parking_capacity << "\n";
}
```

Zmieniła się tylko liczba w porannym przypisaniu. Kolejne wartości program obliczył od nowej wartości, bo każde przypisanie korzysta z poprzedniej.

</details>

**Poprzednia lekcja:** [Lekcja 2.1: Wartości, które program pamięta](lesson_01_values_the_program_remembers.md) · **Następna lekcja:** [Lekcja 2.3: Zobacz, co dzieje się w programie](lesson_03_see_what_happens_in_the_program.md) · [Opis kursu](../../README.md)

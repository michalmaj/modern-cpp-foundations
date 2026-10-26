# Lekcja 7.1: Pierwsze znaki: `char` i przeglądanie `std::string`

**Polski** · [English](lesson_01_first_characters.en.md) · [Opis kursu](../../README.md)

> **Moduł 7, lekcja 1** · około 60–75 minut
> **Potrzebujesz:** katalogu `cpp-workspace` i oryginalnego projektu `lesson_05_first_program`, jak dotąd. Debugger nie jest w tej lekcji potrzebny.
> **Wersja pilotażowa.** Programy z tej lekcji sprawdzamy automatycznie na Windowsie, Ubuntu i macOS, także z podanymi danymi wejściowymi. Wpisywanie danych w oknie **Run** CLiona opisujemy bez ręcznego sprawdzenia na każdym systemie.

## Zanim zaczniesz

Ta lekcja zakłada, że:

- przechowujesz tekst w zmiennej `std::string` i wiesz, że potrzebuje ona `#include <string>` (lekcja 2.7);
- łączysz warunki operatorami `&&` i `||` (lekcja 3.4);
- przeglądasz wektor pętlą zakresową i odczytujesz `size()` oraz `empty()` (lekcje 6.1 i 6.2);
- liczysz zdarzenia licznikiem (lekcja 4.2).

## Sytuacja

W lekcji 6.1 pętla zakresowa przeglądała kolejne elementy wektora:

<!-- fragment -->
```cpp
const std::vector<int> numbers{3, 7, 5};

for (const int number : numbers) {
    std::cout << number << "\n";
}
```

Tekst też składa się z kolejnych elementów: `"ABC"` to A, potem B, potem C. Program, który zna tylko cały tekst, nie odpowie jednak na pytania o jego wnętrze: ile jest w nim cyfr? ile liter? czy są spacje?

**Czy tekst da się przejrzeć tak jak elementy wektora?** Tak. `std::string` też pozwala przeglądać kolejne elementy, a każdy z nich to jeden **znak**, wartość nowego typu `char`. `std::string` to inny typ niż `std::vector`, ale sposób przeglądania jest podobny.

Po tej lekcji będziesz:

- zapisywać zmienne typu `char` i odróżniać `'A'` od `"A"`;
- wyjaśniać, że `std::string` przechowuje ciąg elementów `char`;
- przeglądać tekst znak po znaku pętlą zakresową, łącznie ze spacjami i interpunkcją;
- odczytywać liczbę elementów tekstu przez `size()` i sprawdzać pusty tekst przez `empty()`;
- rozpoznawać w tekście ASCII wielkie i małe litery, cyfry oraz pozostałe znaki;
- wyjaśniać, dlaczego ta analiza jest poprawna tylko dla tekstu ASCII.

## 1. Przygotuj projekt

W `cpp-workspace` utwórz katalog `lesson_7_1` i skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program`. Programy z punktów 2–7 wpisujesz w `main.cpp` tego katalogu.

## 2. Pierwszy `char`

<!-- example: first_chars -->
```cpp
#include <iostream>
#include <string>

int main() {
    const char first{'A'};
    const char second{'7'};
    const char third{'!'};
    const std::string text{"A"};

    std::cout << first << "\n";
    std::cout << second << "\n";
    std::cout << third << "\n";
    std::cout << text << " has " << text.size() << " element\n";
}
```

<!-- output: first_chars -->
```text
A
7
!
A has 1 element
```

- **`char`** to typ, który przechowuje **jeden znak**. `'A'` to litera, `'!'` to znak interpunkcyjny.
- **`'7'` to znak, a nie liczba 7.** Porównaj `const int number{7};` i `const char digit{'7'};`. Obie wartości wypiszą się jako `7`, ale służą do czegoś innego: `int` do liczenia, `char` do zapisu znaku w tekście. Do zamiany cyfry-znaku na liczbę wrócimy w dalszej części kursu.
- `std::cout` wypisuje `char` jako znak, tak samo jak tekst.

## 3. Apostrof i cudzysłów

| Zapis | Co to jest |
|---|---|
| `'A'` | **literał znakowy** w apostrofach: jeden znak, typ `char` |
| `"A"` | **literał tekstowy** w cudzysłowie: tekst, tutaj jednoznakowy |

- Literałem tekstowym `"A"` można utworzyć `std::string`, jak w `const std::string text{"A"};` wyżej. Ale sam literał `"A"` **nie jest** typu `std::string`: to stały tekst z kodu, z którego `std::string` dopiero powstaje.
- `std::string` może zawierać jeden znak, jak `text` wyżej, wiele znaków albo żadnego.
- **Apostrof: zawsze dokładnie jeden znak.** Cudzysłów: tekst dowolnej długości.

**Przewidź**, czy ten program się zbuduje:

<!-- broken: char_from_text at=5:23 errors=1 error=^cannot initialize a variable of type 'const char' with an lvalue of type 'const char\[2\]' -->
```cpp
#include <iostream>
#include <string>

int main() {
    const char symbol{"A"};

    std::cout << symbol << "\n";
}
```

<details>
<summary>Co zgłasza kompilator i dlaczego</summary>

Program się nie zbuduje. Kompilator zgłasza w linijce 5 `cannot initialize a variable of type 'const char' with an lvalue of type 'const char[2]'`: zmiennej typu `char` nie da się zainicjalizować literałem tekstowym. `"A"` to tekst, a nie pojedynczy znak. Zapis `const char[2]` znaczy, że ten literał przechowuje dwa elementy: literę A i niewidoczny znak kończący tekst. Na razie wystarczy zapamiętać, że to nie jest `char`.

**Poprawka:** gdy potrzebny jest jeden znak, użyj apostrofów: `const char symbol{'A'};`.

</details>

## 4. Pętla zakresowa po tekście

<!-- example: cat_letters -->
```cpp
#include <iostream>
#include <string>

int main() {
    const std::string text{"Cat"};

    for (const char symbol : text) {
        std::cout << symbol << "\n";
    }
}
```

**Przewidź**, ile linijek wypisze program i w jakiej kolejności. Potem go uruchom.

<details>
<summary>Standardowe wyjście</summary>

<!-- output: cat_letters -->
```text
C
a
t
```

</details>

To ta sama pętla zakresowa co w lekcji 6.1, tylko po tekście:

- `text` ma trzy elementy, więc ciało wykonuje się trzy razy;
- `symbol` dostaje kolejno wartości `'C'`, `'a'` i `'t'`, w kolejności z tekstu;
- typ zmiennej pętli to typ elementów tekstu: `char`. `const`, bo ciało tylko odczytuje znak;
- nie ma licznika ani indeksu do pilnowania.

## 5. Spacje i inne znaki

Spacja i interpunkcja to też elementy tekstu. Ten program otacza każdy element nawiasami kwadratowymi, żeby spacja była widoczna:

<!-- example: bracketed -->
```cpp
#include <iostream>
#include <string>

int main() {
    const std::string text{"A 7!"};

    std::cout << "Elements: " << text.size() << "\n";

    for (const char symbol : text) {
        std::cout << "[" << symbol << "]\n";
    }
}
```

**Przewidź** liczbę elementów i wszystkie linijki wyniku.

<details>
<summary>Standardowe wyjście</summary>

<!-- output: bracketed -->
```text
Elements: 4
[A]
[ ]
[7]
[!]
```

</details>

Tekst `"A 7!"` ma **cztery** elementy: `A`, spację, `7` i `!`. Spacja nie znika podczas przeglądania: to zwykły znak, tylko niewidoczny bez nawiasów.

`text.size()` podaje liczbę elementów tekstu, tak jak dla wektora. Nie trzeba liczyć znaków osobnym licznikiem.

## 6. Pusty tekst

<!-- example: empty_text -->
```cpp
#include <iostream>
#include <string>

int main() {
    const std::string empty_text{};

    std::cout << "Elements: " << empty_text.size() << "\n";

    if (empty_text.empty()) {
        std::cout << "The text is empty\n";
    }

    for (const char symbol : empty_text) {
        std::cout << "[" << symbol << "]\n";
    }

    std::cout << "Done\n";
}
```

**Przewidź**, ile razy wykona się ciało pętli.

<details>
<summary>Standardowe wyjście</summary>

<!-- output: empty_text -->
```text
Elements: 0
The text is empty
Done
```

</details>

Puste `{}` tworzą tekst bez elementów. `size()` daje 0, `empty()` daje `true`, a pętla zakresowa nie wykonuje ani jednego przebiegu, jak dla pustego wektora w lekcji 6.1. Pusty tekst to poprawny przypadek, który trzeba uwzględniać.

## 7. Granica: tekst ASCII

W tej lekcji analizujemy tekst **ASCII**: angielskie litery, cyfry, spację i podstawową interpunkcję. Dla takiego tekstu jeden element `char` to jeden widoczny znak. `std::string` może przechowywać też tekst z polskimi literami, ale sam ich nie rozpoznaje. W popularnym kodowaniu UTF-8 litera taka jak `ż` zajmuje **kilka** elementów `char`. Dla takiego tekstu `size()` podaje liczbę elementów `char`, a nie liczbę liter widocznych dla człowieka, pętla zakresowa odczytuje jedną literę jako kilka elementów, a porównania z tej lekcji nie rozpoznają polskich liter. To świadome ograniczenie tej lekcji, a nie błąd. Dlatego wszystkie dane w zadaniach są w ASCII.

## 8. Rozpoznawanie cyfr

Znaki można porównywać tak jak liczby: `<`, `>`, `<=`, `>=`, `==`. Cyfry od `'0'` do `'9'` następują po sobie w kolejności, więc warunek `symbol >= '0' && symbol <= '9'` jest prawdziwy dokładnie dla cyfry:

<!-- example: room_digits -->
```cpp
#include <iostream>
#include <string>

int main() {
    const std::string label{"Room 12"};
    int digits{0};

    for (const char symbol : label) {
        if (symbol >= '0' && symbol <= '9') {
            ++digits;
        }
    }

    std::cout << "Digits: " << digits << "\n";
}
```

**Przewidź** wynik i uruchom program.

<details>
<summary>Standardowe wyjście</summary>

<!-- output: room_digits -->
```text
Digits: 2
```

</details>

- Pętla przegląda siedem elementów: `R`, `o`, `o`, `m`, spację, `1` i `2`.
- Licznik rośnie tylko dla `'1'` i `'2'`.
- Porównujemy **znaki**: `'0'` i `'9'` stoją w apostrofach. Bez apostrofów `0` i `9` byłyby liczbami `int`, a to coś innego.

W tekście ASCII tak samo rozpoznasz wielką literę angielskiego alfabetu, od `'A'` do `'Z'`, i małą, od `'a'` do `'z'`: litery w każdym z tych zakresów też następują po sobie w kolejności. Wielkie i małe litery to jednak **dwa osobne zakresy**. Każdy znak, który nie jest literą ani cyfrą, to „inny” znak: spacja, myślnik, wykrzyknik i każda inna interpunkcja.

## 9. Misja: raport znaków

Program przygotowuje raport o zawartości krótkiego komunikatu. Komunikat jest wpisany w kodzie i zawiera tylko znaki ASCII:

<!-- fragment -->
```cpp
const std::string message{"Box 7 - ready!"};
```

**Wymagania:**

- Program wypisuje cztery linijki:
  - `Characters: N`: liczbę wszystkich elementów komunikatu;
  - `Letters: N`: liczbę liter angielskiego alfabetu, wielkich i małych;
  - `Digits: N`: liczbę cyfr;
  - `Other: N`: liczbę pozostałych znaków, czyli spacji, myślników, wykrzykników i innej interpunkcji.
- **Każdy element komunikatu należy do dokładnie jednej kategorii:** litera, cyfra albo inny. Suma trzech kategorii jest więc równa liczbie wszystkich elementów.
- Program używa `std::string`, pętli zakresowej ze zmienną `const char`, liczników `int` i `size()`. Nie zmienia komunikatu, nie odczytuje niczego z wejścia i nie korzysta z dodatkowych bibliotek.
- Po zmianie samego komunikatu w nawiasach klamrowych program podaje poprawny raport dla nowego tekstu ASCII, także pustego.

W `cpp-workspace` utwórz katalog `message_report`, skopiuj do niego `CMakeLists.txt` z oryginalnego `lesson_05_first_program`, utwórz pusty `main.cpp` i napisz program samodzielnie.

Dla komunikatu powyżej standardowe wyjście ma być takie:

<!-- output: message_report -->
```text
Characters: 14
Letters: 8
Digits: 1
Other: 5
```

Liter jest 8: trzy w `Box` i pięć w `ready`. Cyfra jest jedna, `7`. Innych znaków jest 5: trzy spacje, myślnik i wykrzyknik.

**To nie jest program z punktu 8 z innymi napisami.** Tam był jeden licznik i jeden warunek. Musisz samodzielnie zdecydować:

1. jak rozpoznać literę, skoro wielkie i małe litery to dwa zakresy;
2. w jakiej kolejności sprawdzać kategorie, żeby żaden znak nie zwiększył dwóch liczników;
3. jak rozpoznać „inny” znak, nie wypisując wszystkich możliwych znaków interpunkcyjnych;
4. skąd wziąć liczbę wszystkich elementów;
5. jak sprawdzić, że raport się zgadza.

**Zanim napiszesz program**, przygotuj tabelę przypadków: komunikat z wymagań, pusty tekst, same wielkie litery, same małe litery, same cyfry, same spacje i myślniki, po jednym znaku z każdej kategorii oraz znak spoza liter i cyfr, na przykład `_`. Przy każdym zapisz cztery liczby raportu.

**Potem:** uruchom program dla komunikatu z wymagań, a następnie zmień komunikat na 3–4 przypadki z tabeli, na przykład pusty tekst, `AbC`, `019` i ` -- `. Wszystkie przypadki z pełnej listy kontrolnej są sprawdzone automatycznie, więc nie musisz wpisywać ich wszystkich.

### Kryterium sukcesu

- Program buduje się jako C++20, a dla komunikatu z wymagań wypisuje dokładnie cztery linijki pokazane wyżej.
- Wielkie i małe litery są liczone jako litery, cyfry jako cyfry, a wszystko inne, także spacja, jako inne.
- Każdy element zwiększa dokładnie jeden z trzech liczników, więc ich suma jest równa liczbie wszystkich elementów.
- Dla pustego tekstu program wypisuje same zera.
- Program nie korzysta z indeksów, wejścia ani dodatkowych bibliotek.
- Tabela przypadków powstała przed uruchomieniem programu.
- Umiesz wyjaśnić, dlaczego Twój program nie policzy żadnego znaku dwa razy.

Gdy wynik się zgadza, możesz zapisać projekt w Gicie, jak w lekcji 1.5.

<details>
<summary>Podpowiedź 1</summary>

Czy potrafisz przejrzeć każdy znak komunikatu tak samo, jak wcześniej przeglądało się elementy wektora?

</details>

<details>
<summary>Podpowiedź 2</summary>

Każdy znak może należeć do jednej z trzech kategorii: litera, cyfra albo pozostałe. Jak rozpoznać każdą z nich?

</details>

<details>
<summary>Podpowiedź 3</summary>

Pamiętaj o małych i wielkich literach oraz o tym, aby każdy znak zwiększał dokładnie jeden licznik kategorii.

</details>

<details>
<summary>Pełna lista przypadków kontrolnych: otwórz po przygotowaniu własnej tabeli</summary>

| | Komunikat | Wszystkie | Litery | Cyfry | Inne | Co sprawdza |
|---|---|---|---|---|---|---|
| A | `Box 7 - ready!` | 14 | 8 | 1 | 5 | dane z wymagań |
| B | pusty tekst | 0 | 0 | 0 | 0 | pusty tekst |
| C | `ABC` | 3 | 3 | 0 | 0 | same wielkie litery |
| D | `xyz` | 3 | 3 | 0 | 0 | same małe litery |
| E | `019` | 3 | 0 | 3 | 0 | same cyfry, także `0` i `9` |
| F | ` -- ` (spacja, dwa myślniki, spacja) | 4 | 0 | 0 | 4 | spacje i interpunkcja |
| G | `A0!` | 3 | 1 | 1 | 1 | po jednym z każdej kategorii |
| H | `A1 B2` | 5 | 2 | 2 | 1 | mieszane kategorie ze spacją |
| I | `z_9` | 3 | 1 | 1 | 1 | `_` to inny znak |
| J | `AbC` | 3 | 3 | 0 | 0 | wielkie i małe litery razem (punkt 10) |

W każdym wierszu suma liter, cyfr i innych jest równa liczbie wszystkich elementów.

**Testy automatyczne i Twoje próby.** Wszystkie przypadki są sprawdzone automatycznie przez program kontrolny. Ma on ten sam raport co rozwiązanie referencyjne, ale komunikat odczytuje z wejścia jako jedną linijkę, przez `std::getline` z lekcji 2.7. Pusty tekst to w nim pusta linijka. To tylko narzędzie do sprawdzania, a nie część misji: w misji komunikat jest wpisany w kodzie. Program kontrolny i jego wyniki są w części [Przykładowe rozwiązania](#przykładowe-rozwiązania), bo zawierają rozwiązanie.

</details>

Przykładowe rozwiązanie jest w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 10. Znajdź błąd: zgubione małe litery

To zadanie wykonaj **po misji**: program poniżej zawiera cały raport. Odczytuje komunikat z wejścia jako jedną linijkę, tak jak program kontrolny, i nie wypisuje pytania: po uruchomieniu wpisz tekst i naciśnij **Enter**. Wymaganie: litery to wielkie **i małe** litery angielskiego alfabetu.

<details>
<summary>Program do sprawdzenia: otwórz po napisaniu własnego programu</summary>

<!-- example: letters_bug -->
```cpp
#include <iostream>
#include <string>

int main() {
    std::string message{};
    std::getline(std::cin, message);

    if (std::cin.fail()) {
        std::cout << "Input could not be read\n";
    } else {
        int letters{0};
        int digits{0};
        int other{0};

        for (const char symbol : message) {
            if (symbol >= 'A' && symbol <= 'Z') {
                ++letters;
            } else if (symbol >= '0' && symbol <= '9') {
                ++digits;
            } else {
                ++other;
            }
        }

        std::cout << "Characters: " << message.size() << "\n";
        std::cout << "Letters: " << letters << "\n";
        std::cout << "Digits: " << digits << "\n";
        std::cout << "Other: " << other << "\n";
    }
}
```

1. **Przewidź** raport dla `ABC` i dla `AbC`.
2. Uruchom program i wpisz `ABC`. Czy raport jest poprawny?
3. Uruchom go ponownie i wpisz `AbC`.
4. Suma liter, cyfr i innych nadal jest równa liczbie wszystkich elementów. Dlaczego ta kontrola nie wykrywa błędu?
5. Znajdź brakujący zakres znaków.
6. Popraw warunek.
7. Sprawdź oba teksty ponownie.

</details>

Wyniki programu przed poprawką i poprawiony program są w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 11. Gdy coś pójdzie inaczej

| Co widzisz | Co to znaczy | Co zrobić |
|---|---|---|
| `cannot initialize a variable of type 'const char' with ...` | Zmienna `char` dostaje literał tekstowy w cudzysłowie (punkt 3). | Pojedynczy znak zapisuj w apostrofach: `'A'`. |
| `comparison between pointer and integer` przy porównaniu znaku | Znak jest porównywany z literałem tekstowym, na przykład `symbol == "-"`. | Porównuj z literałem znakowym: `symbol == '-'`. |
| Liczba liter jest za mała | Warunek obejmuje tylko wielkie albo tylko małe litery (punkt 10). | Litera to zakres `'A'`–`'Z'` **albo** zakres `'a'`–`'z'`. |
| Suma kategorii jest większa niż liczba elementów | Jeden znak zwiększa dwa liczniki, na przykład dwa osobne `if` zamiast `else if`. | Sprawdzaj kategorie w jednym łańcuchu `if` / `else if` / `else`. |
| Cyfry nie są liczone | Warunek porównuje z liczbami `0` i `9` zamiast ze znakami `'0'` i `'9'`. | Używaj apostrofów. |
| Liczby nie zgadzają się dla tekstu z polską literą | W UTF-8 polska litera zajmuje kilka elementów `char` (punkt 7). | W tej lekcji używaj tekstu bez polskich liter. |

## 12. Wyjaśnij

Odpowiedz własnymi słowami, najlepiej na piśmie. Dopiero potem porównaj z przykładowymi odpowiedziami.

1. Co przechowuje zmienna typu `char`?
2. Czym różni się `'A'` od `"A"`? Czy literał `"A"` ma typ `std::string`?
3. Co przechowuje `std::string`?
4. Jakiego typu jest zmienna pętli zakresowej po tekście i dlaczego?
5. Czy spacja jest elementem tekstu?
6. Co podają `size()` i `empty()` dla tekstu?
7. Ile przebiegów wykonuje pętla zakresowa po pustym tekście?
8. Jak rozpoznać cyfrę ASCII i dlaczego `'0'` musi stać w apostrofach?
9. Dlaczego trzeba uwzględnić osobno małe i wielkie litery?
10. Jak sprawić, żeby żaden znak nie został policzony dwa razy?
11. Dlaczego `size()` może podać inną liczbę niż liczba liter widocznych w tekście UTF-8?

<details>
<summary>Przykładowe odpowiedzi</summary>

1. Jeden znak, na przykład literę, cyfrę, spację albo znak interpunkcyjny.
2. `'A'` to literał znakowy: jeden znak typu `char`. `"A"` to literał tekstowy. Można z niego utworzyć `std::string`, ale sam literał nie ma typu `std::string`.
3. Ciąg elementów `char`: zero, jeden albo wiele znaków.
4. `char`, bo elementy tekstu są typu `char`. Typ zmiennej pętli to typ elementów, jak `int` dla `std::vector<int>`.
5. Tak. Spacja to zwykły znak: liczy się w `size()` i pętla dostaje ją jak każdy inny element.
6. `size()` podaje liczbę elementów tekstu, a `empty()` daje `true`, gdy tekst nie ma żadnego elementu.
7. Zero. Ciało nie wykonuje się ani razu.
8. Warunkiem `symbol >= '0' && symbol <= '9'`, bo cyfry następują po sobie w kolejności. Apostrofy są potrzebne, bo porównujemy znaki: `0` bez apostrofów to liczba `int`, a nie znak `'0'`.
9. Bo w ASCII to dwa osobne zakresy znaków. Warunek tylko dla `'A'`–`'Z'` pominie wszystkie małe litery.
10. Sprawdzać kategorie w jednym łańcuchu `if` / `else if` / `else`. Wtedy dla każdego znaku wykonuje się dokładnie jedna gałąź.
11. Bo `size()` liczy elementy `char`, a w UTF-8 jedna widoczna litera, na przykład `ż`, może zajmować kilka takich elementów.

</details>

## Podsumowanie

- **`char`** przechowuje jeden znak. Literał znakowy zapisujesz w apostrofach: `'A'`, `'7'`, `'!'`.
- `"A"` w cudzysłowie to literał tekstowy, z którego można utworzyć `std::string`, ale to nie jest `char`.
- **`std::string`** przechowuje ciąg elementów `char`. Pętla zakresowa `for (const char symbol : text)` przegląda je kolejno, łącznie ze spacjami i interpunkcją.
- `size()` podaje liczbę elementów tekstu, a `empty()` sprawdza, czy tekst jest pusty. Pusty tekst daje zero przebiegów pętli.
- Znaki porównujesz z literałami znakowymi. W ASCII cyfra to `'0'`–`'9'`, wielka litera `'A'`–`'Z'`, a mała `'a'`–`'z'`.
- Łańcuch `if` / `else if` / `else` przydziela każdy znak do dokładnie jednej kategorii.
- Ta analiza jest poprawna dla tekstu ASCII. W UTF-8 jedna polska litera może zajmować kilka elementów `char`.

## Co dalej

W tej lekcji pętla przeglądała znaki po kolei. W kolejnej lekcji odczytasz znak o wybranej pozycji i porównasz sąsiednie znaki, tak jak elementy wektora w lekcji 6.3: [Lekcja 7.2: Pozycje i sąsiednie znaki w `std::string`](lesson_02_positions_and_neighbours.md).

---

## Przykładowe rozwiązania

Zajrzyj tutaj **po własnej próbie**. Twoje nazwy mogą się różnić, jeśli standardowe wyjście jest takie, jak wymagane.

<details>
<summary>Punkt 9: misja, raport znaków</summary>

<!-- example: message_report -->
```cpp
#include <iostream>
#include <string>

int main() {
    const std::string message{"Box 7 - ready!"};

    int letters{0};
    int digits{0};
    int other{0};

    for (const char symbol : message) {
        if ((symbol >= 'A' && symbol <= 'Z') || (symbol >= 'a' && symbol <= 'z')) {
            ++letters;
        } else if (symbol >= '0' && symbol <= '9') {
            ++digits;
        } else {
            ++other;
        }
    }

    std::cout << "Characters: " << message.size() << "\n";
    std::cout << "Letters: " << letters << "\n";
    std::cout << "Digits: " << digits << "\n";
    std::cout << "Other: " << other << "\n";
}
```

1. **Pętla zakresowa:** `std::string` pozwala przeglądać kolejne elementy, tak jak wektor, więc każdy znak trafia do ciała pętli dokładnie raz.
2. **Zmienna pętli to `char`**, bo elementy tekstu są typu `char`. `const`, bo ciało tylko odczytuje znak.
3. **Wielkie i małe litery** to dwa zakresy połączone `||`. Nawiasy wokół każdego zakresu pokazują, które warunki `&&` tworzą całość.
4. **Brak podwójnego liczenia:** łańcuch `if` / `else if` / `else` wykonuje dla każdego znaku dokładnie jedną gałąź. Dlatego suma trzech liczników jest zawsze równa `message.size()`.
5. **Spacja** nie jest ani literą, ani cyfrą, więc trafia do gałęzi `else`, czyli do kategorii `Other`, jak myślnik i wykrzyknik.
6. **Pusty tekst:** pętla nie wykonuje żadnego przebiegu, więc liczniki zostają przy wartościach początkowych 0, a `size()` daje 0.
7. **Ograniczenie ASCII:** zakresy `'A'`–`'Z'` i `'a'`–`'z'` obejmują tylko angielskie litery. Dla tekstu UTF-8 z polską literą każdy jej element `char` trafiłby do `Other`, a `Characters` nie byłoby liczbą widocznych liter. Program jest poprawny dla tekstu ASCII, a nie dla dowolnego tekstu Unicode.

Kategorie można też sprawdzać w innej kolejności, na przykład najpierw cyfry, jeśli łańcuch `else if` zapewnia, że każdy znak trafia do jednej kategorii.

**Program kontrolny** sprawdza wszystkie przypadki z listy kontrolnej. Pętla i raport są takie same jak wyżej, poza wcięciem. Różnica jest jedna: komunikat jest odczytywany z wejścia jako jedna linijka przez `std::getline` (lekcja 2.7), więc nie ma `const`.

<!-- example: message_report_check -->
```cpp
#include <iostream>
#include <string>

int main() {
    std::string message{};
    std::getline(std::cin, message);

    if (std::cin.fail()) {
        std::cout << "Input could not be read\n";
    } else {
        int letters{0};
        int digits{0};
        int other{0};

        for (const char symbol : message) {
            if ((symbol >= 'A' && symbol <= 'Z') || (symbol >= 'a' && symbol <= 'z')) {
                ++letters;
            } else if (symbol >= '0' && symbol <= '9') {
                ++digits;
            } else {
                ++other;
            }
        }

        std::cout << "Characters: " << message.size() << "\n";
        std::cout << "Letters: " << letters << "\n";
        std::cout << "Digits: " << digits << "\n";
        std::cout << "Other: " << other << "\n";
    }
}
```

Każdy przypadek to jedna linijka wejścia, w kolejności z listy kontrolnej, od A do J. Przypadek B to pusta linijka.

<!-- input: message_report_check -->
```text
Box 7 - ready!
```

<!-- output: message_report_check -->
```text
Characters: 14
Letters: 8
Digits: 1
Other: 5
```

<!-- input: message_report_check -->
```text

```

<!-- output: message_report_check -->
```text
Characters: 0
Letters: 0
Digits: 0
Other: 0
```

<!-- input: message_report_check -->
```text
ABC
```

<!-- output: message_report_check -->
```text
Characters: 3
Letters: 3
Digits: 0
Other: 0
```

<!-- input: message_report_check -->
```text
xyz
```

<!-- output: message_report_check -->
```text
Characters: 3
Letters: 3
Digits: 0
Other: 0
```

<!-- input: message_report_check -->
```text
019
```

<!-- output: message_report_check -->
```text
Characters: 3
Letters: 0
Digits: 3
Other: 0
```

<!-- input: message_report_check -->
```text
 -- 
```

<!-- output: message_report_check -->
```text
Characters: 4
Letters: 0
Digits: 0
Other: 4
```

<!-- input: message_report_check -->
```text
A0!
```

<!-- output: message_report_check -->
```text
Characters: 3
Letters: 1
Digits: 1
Other: 1
```

<!-- input: message_report_check -->
```text
A1 B2
```

<!-- output: message_report_check -->
```text
Characters: 5
Letters: 2
Digits: 2
Other: 1
```

<!-- input: message_report_check -->
```text
z_9
```

<!-- output: message_report_check -->
```text
Characters: 3
Letters: 1
Digits: 1
Other: 1
```

<!-- input: message_report_check -->
```text
AbC
```

<!-- output: message_report_check -->
```text
Characters: 3
Letters: 3
Digits: 0
Other: 0
```

</details>

<details>
<summary>Punkt 10: wyniki przed poprawką i poprawiony program</summary>

Przed poprawką, dla `ABC`:

<!-- input: letters_bug -->
```text
ABC
```

<!-- output: letters_bug -->
```text
Characters: 3
Letters: 3
Digits: 0
Other: 0
```

Dla `AbC`:

<!-- input: letters_bug -->
```text
AbC
```

<!-- output: letters_bug -->
```text
Characters: 3
Letters: 2
Digits: 0
Other: 1
```

- Dla `ABC` raport jest poprawny: wszystkie litery są wielkie, więc brakujący zakres nie ma znaczenia.
- Dla `AbC` mała litera `b` trafia do `Other`: liter jest 2 zamiast 3.
- **Suma nadal się zgadza** (2 + 0 + 1 = 3), bo `b` zwiększyła inny licznik, ale tylko jeden. Kontrola sumy wykrywa podwójne liczenie, ale nie wykryje znaku przypisanego do złej kategorii.
- **Przyczyna:** warunek litery obejmuje tylko zakres `'A'`–`'Z'`.
- **Poprawka:** `(symbol >= 'A' && symbol <= 'Z') || (symbol >= 'a' && symbol <= 'z')`.

Poprawiony program to program kontrolny z punktu 9: różni się od programu z błędem tylko tym warunkiem. Dla obu tekstów daje wyniki z listy kontrolnej: przypadki C i J.

</details>

**Poprzednia lekcja:** [Lekcja 6.6: Dziennik treningów (sprawdzian Modułu 6)](../module_06_collections/lesson_06_training_log.md) · **Następna lekcja:** [Lekcja 7.2: Pozycje i sąsiednie znaki w `std::string`](lesson_02_positions_and_neighbours.md) · [Opis kursu](../../README.md)

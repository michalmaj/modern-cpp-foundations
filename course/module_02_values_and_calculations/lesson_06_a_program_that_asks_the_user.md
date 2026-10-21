# Lekcja 2.6: Program, który pyta użytkownika

**Polski** · [English](lesson_06_a_program_that_asks_the_user.en.md) · [Opis kursu](../../README.md)

> **Moduł 2, lekcja 6** · około 75 minut
> **Potrzebujesz:** katalogu `cpp-workspace` i oryginalnego projektu `lesson_05_first_program`, jak dotąd, oraz terminala z lekcji 0.5 i 0.6. Debugger nie jest w tej lekcji potrzebny.
> **Wersja pilotażowa.** Programy z tej lekcji sprawdzamy automatycznie na Windowsie, Ubuntu i macOS, także z podanymi danymi wejściowymi. Wpisywanie danych w oknie **Run** CLiona opisujemy bez ręcznego sprawdzenia na każdym systemie. Jeśli w oknie **Run** nie da się wpisać danych, uruchamiaj programy w terminalu, jak w punkcie 3.

## Zanim zaczniesz

Ta lekcja zakłada, że po lekcji 2.5:

- tworzysz zmienne i stałe typu `int` i `double` z wartością początkową w `{}`;
- wiesz, że `int` razy `double` daje `double`, a dzielenie dwóch `int` jest dzieleniem całkowitym;
- uruchamiasz zbudowany program w terminalu, jak w lekcji 0.5, punkt 7.

## Sytuacja

Do tej pory wszystkie dane były wpisane w kodzie. Żeby policzyć coś dla innych liczb, trzeba było zmienić kod i zbudować program jeszcze raz. Prawdziwe programy zwykle pytają: o liczbę, o wymiar, o czas. Dziś program po raz pierwszy **pobierze dane podczas działania**. Zobaczysz, że **ten sam program, bez ponownego budowania, daje różne wyniki dla różnych danych**.

Po tej lekcji będziesz:

- odróżniać dane zapisane w kodzie od danych podawanych podczas działania programu;
- wyjaśniać, czym jest standardowe wejście i czym różni się od standardowego wyjścia;
- odczytywać liczby typu `int` i `double` za pomocą `std::cin` i `>>`;
- prosić użytkownika o dane i odróżniać to, co wypisuje program, od tego, co wpisuje użytkownik;
- używać odczytanych danych w obliczeniach i wypisywać wynik, który od nich zależy;
- uruchamiać ten sam program kilka razy z różnymi danymi;
- opisywać drogę informacji: wejście → zmienna → obliczenie → wynik.

## 1. Przygotuj projekt

W `cpp-workspace` utwórz katalog `lesson_2_6`, skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program` i otwórz ten katalog w CLionie, jak w lekcji 1.1 (**File | Open**).

## 2. Dane w kodzie i dane od użytkownika

Ten program zna swoją liczbę od początku, bo jest wpisana w kodzie:

<!-- example: count_in_code -->
```cpp
#include <iostream>

int main() {
    const int count{5};
    std::cout << "Count: " << count << "\n";
}
```

<!-- output: count_in_code -->
```text
Count: 5
```

Żeby wypisał inną liczbę, trzeba zmienić kod i zbudować program ponownie. Teraz zastąp zawartość `main.cpp` wersją, która pobiera liczbę od użytkownika:

<!-- example: count_from_input -->
```cpp
#include <iostream>

int main() {
    int count{0};
    std::cin >> count;
    std::cout << "Count: " << count << "\n";
}
```

Zbuduj go i uruchom (**Run**). Program nic nie wypisze, tylko poczeka. Kliknij w okno **Run**, wpisz `5` i naciśnij **Enter**.

Dane wejściowe:

<!-- input: count_from_input -->
```text
5
```

Program wypisze:

<!-- output: count_from_input -->
```text
Count: 5
```

## 3. Ten sam program, inne dane

To najważniejszy eksperyment tej lekcji. **Nie zmieniaj kodu.**

1. Uruchom program jeszcze raz (**Run**). Kod się nie zmienił, więc CLion nie musi niczego budować (lekcja 0.5): uruchamia ten sam plik wykonywalny.
2. Tym razem wpisz `12` i naciśnij **Enter**.

<!-- input: count_from_input -->
```text
12
```

<!-- output: count_from_input -->
```text
Count: 12
```

Między uruchomieniami **nie zmienił się** kod, plik `CMakeLists.txt` ani plik wykonywalny. Zmieniły się tylko **dane**, a razem z nimi wynik.

**Ten sam eksperyment w terminalu.** Tu widać najwyraźniej, że to jeden i ten sam plik wykonywalny, bo uruchamiasz go bezpośrednio, bez żadnego budowania. W terminalu przejdź do katalogu `lesson_2_6` i uruchom dwa razy program zbudowany przez CLion, jak w lekcji 0.5, punkt 7. Za pierwszym razem wpisz `5`, za drugim `12`:

| Windows (PowerShell) | macOS i Linux |
|---|---|
| `.\cmake-build-debug\first_program.exe` | `./cmake-build-debug/first_program` |

## 4. Co robi `std::cin >> count;`

- **`std::cin`** to **standardowe wejście** programu: strumień, z którego program może pobierać dane. Para do znanego `std::cout`, czyli **standardowego wyjścia**.
- **`>>`** odczytuje ze strumienia wartość i **zapisuje ją w zmiennej** po prawej stronie. Po `std::cin >> count;` zmienna `count` ma odczytaną wartość.
- Kierunek strzałek pokazuje drogę danych:
  - `std::cout << count` wysyła wartość **ze zmiennej do wyjścia**, na ekran;
  - `std::cin >> count` pobiera wartość **z wejścia do zmiennej**.
- Gdy uruchamiasz program w terminalu albo w CLionie, standardowe wejście to zwykle **klawiatura**: to, co wpiszesz w oknie programu. Dane mogą jednak przyjść też z innego źródła. Na przykład automatyczne testy tego kursu podają programom dane bez żadnego pisania na klawiaturze.

## 5. Program czeka na dane

Co się dzieje, gdy program dochodzi do `std::cin >> count;`? Sprawdź na tym programie:

<!-- example: waiting -->
```cpp
#include <iostream>

int main() {
    int count{0};
    std::cout << "Before reading\n";
    std::cin >> count;
    std::cout << "After reading: " << count << "\n";
}
```

Uruchom go i **jeszcze nic nie wpisuj**. Przyjrzyj się oknu programu: jest tam już `Before reading`, ale nie ma `After reading`.

Program nie zawiesił się. **Czeka na dane**: instrukcja `std::cin >> count;` jeszcze się nie zakończyła, więc kolejne instrukcje się nie wykonały. Teraz wpisz `7` i naciśnij **Enter**. **Enter** zatwierdza wpisaną wartość: dopiero wtedy program ją odczytuje i idzie dalej.

<!-- input: waiting -->
```text
7
```

<!-- output: waiting -->
```text
Before reading
After reading: 7
```

Instrukcje po odczycie korzystają już z odczytanej wartości. Jeśli debugger działa u Ciebie od lekcji 2.3, możesz to też obejrzeć krok po kroku, ale nie jest to potrzebne.

## 6. Poproś o dane i odróżnij je od wyniku

Program, który tylko czeka, nie mówi, czego chce. Dlatego przed odczytem zwykle wypisuje się prośbę:

<!-- example: prompt -->
```cpp
#include <iostream>

int main() {
    int count{0};
    std::cout << "Enter count:\n";
    std::cin >> count;
    std::cout << "Count: " << count << "\n";
}
```

`std::cout` tylko **wypisuje** prośbę. Niczego nie odczytuje i samo nie sprawia, że program pobierze dane. Odczytuje dopiero `std::cin`.

Gdy uruchomisz program i wpiszesz `5`, na ekranie zobaczysz trzy linijki:

```text
Enter count:
5
Count: 5
```

**Nie wszystkie pochodzą od programu.** Linijkę `5` widać tylko dlatego, że okno, w którym piszesz, pokazuje wpisywane znaki. To tak zwane **echo**. Program jej nie wypisał: żadne `std::cout` w kodzie nie wypisuje samego `5`. Dlatego w tym kursie rozdzielamy trzy rzeczy.

**Dane wejściowe**, czyli to, co trafia do `std::cin`:

<!-- input: prompt -->
```text
5
```

**Standardowe wyjście**, czyli tylko to, co wypisał program przez `std::cout`:

<!-- output: prompt -->
```text
Enter count:
Count: 5
```

**Zapis tego, co widać na ekranie**, jak wyżej: linijki programu i wpisana liczba między nimi.

Automatyczne testy tego kursu porównują tylko standardowe wyjście.

## 7. Wczytaj `int` i `double`

Program może odczytać kilka wartości różnych typów. Każda trafia do zmiennej, której typ pasuje do danych:

<!-- example: floors_and_height -->
```cpp
#include <iostream>

int main() {
    int floors{0};
    double floor_height_m{0.0};

    std::cout << "Enter the number of floors:\n";
    std::cin >> floors;
    std::cout << "Enter the floor height in m:\n";
    std::cin >> floor_height_m;

    std::cout << "Floors: " << floors << "\n";
    std::cout << "Floor height: " << floor_height_m << " m\n";
}
```

Uruchom program i podaj dwie wartości w osobnych linijkach: `3` i `2.75`.

<!-- input: floors_and_height -->
```text
3
2.75
```

<!-- output: floors_and_height -->
```text
Enter the number of floors:
Enter the floor height in m:
Floors: 3
Floor height: 2.75 m
```

- Liczba pięter jest całkowita, więc trafia do `int`. Wysokość piętra może mieć część ułamkową, więc trafia do `double`. **Typ zmiennej musi pasować do rodzaju danych**, które chcesz odczytać.
- Wartość z częścią ułamkową wpisuj z **kropką**: `2.75`, tak jak w kodzie.
- `>>` pomija odstępy przed wartością: spacje, tabulatory i przejścia do nowej linii. Dlatego obie wartości możesz też wpisać w jednej linijce, oddzielone spacją. Sprawdź: uruchom program jeszcze raz i wpisz `3 2.75`, a potem **Enter**. Wynik będzie ten sam:

<!-- input: floors_and_height -->
```text
3 2.75
```

<!-- output: floors_and_height -->
```text
Enter the number of floors:
Enter the floor height in m:
Floors: 3
Floor height: 2.75 m
```

## 8. Zmienne na dane

Zmienna, do której program wczytuje dane, ma wartość początkową jak każda inna: `int floors{0};`, `double floor_height_m{0.0};`.

- `0` i `0.0` to tylko **wartości początkowe**. Udany odczyt zastępuje je danymi ze standardowego wejścia.
- Taka zmienna **nie może być `const`**: odczyt zmienia jej wartość, a stałej zmienić nie można. Sprawdź, co powie kompilator, gdy spróbujesz:

<!-- broken: read_into_const at=5 errors=1 error=^(invalid operands to binary expression|use of overloaded operator '>>' is ambiguous) .*'const int'\)$ -->
```cpp
#include <iostream>

int main() {
    const int count{0};
    std::cin >> count;
    std::cout << "Count: " << count << "\n";
}
```

Program się nie zbuduje. Kompilator zgłasza błąd w linijce 5, przy `>>`, ale jego treść zależy od systemu, bo pochodzi z biblioteki standardowej:

- na Ubuntu i macOS: `invalid operands to binary expression ('istream' (aka 'basic_istream<char>') and 'const int')`;
- na Windowsie: `use of overloaded operator '>>' is ambiguous (with operand types 'istream' (aka 'basic_istream<char, char_traits<char>>') and 'const int')`.

Pod nim pojawia się wiele linijek `note:` o bibliotece standardowej, na niektórych systemach kilkadziesiąt. Nie musisz ich czytać. Jak w lekcji 1.2, liczy się pierwsza linijka z `error` w `main.cpp`. Obie wersje kończą się tak samo: `'const int'`. To jest przyczyna: `>>` nie może zapisać wartości w stałej. Przywróć poprawny kod: usuń `const`.

- **Po** odczycie możesz użyć danych do utworzenia stałej, jeśli wynik obliczenia ma się już nie zmieniać. Tak zrobisz w następnym punkcie.
- Wartość początkowa `0` **nie** zabezpiecza programu przed złymi danymi. To po prostu poprawnie zainicjalizowana zmienna (więcej w punkcie 11).

## 9. Oblicz z danymi

Magazyn pakuje przedmioty do pudełek. Program pyta o liczbę pudełek i liczbę przedmiotów w jednym pudełku, a potem liczy wszystkie przedmioty:

<!-- example: boxes_total -->
```cpp
#include <iostream>

int main() {
    int boxes{0};
    int items_per_box{0};

    std::cout << "Enter the number of boxes:\n";
    std::cin >> boxes;
    std::cout << "Enter the items per box:\n";
    std::cin >> items_per_box;

    const int total_items{boxes * items_per_box};

    std::cout << "Total items: " << total_items << "\n";
}
```

Kolejność ma znaczenie: obliczenie stoi **po** obu odczytach, więc korzysta z wpisanych liczb, a nie z wartości początkowych 0. Wynik się już nie zmienia, więc jest stałą `const int`.

Uruchom program dwa razy: z danymi `3` i `4`, a potem `5` i `6`.

<!-- input: boxes_total -->
```text
3
4
```

<!-- output: boxes_total -->
```text
Enter the number of boxes:
Enter the items per box:
Total items: 12
```

<!-- input: boxes_total -->
```text
5
6
```

<!-- output: boxes_total -->
```text
Enter the number of boxes:
Enter the items per box:
Total items: 30
```

**Przewidź**, co wypisze program dla `7` i `8`. Zapisz wynik, a potem sprawdź go, uruchamiając program trzeci raz.

<!-- input: boxes_total -->
```text
7
8
```

<details>
<summary>Wynik dla 7 i 8</summary>

<!-- output: boxes_total -->
```text
Enter the number of boxes:
Enter the items per box:
Total items: 56
```

</details>

## 10. Gdy typ wyniku nie pasuje

W lekcji 2.5 wszystkie dane były stałymi z wartościami wpisanymi w kodzie. Teraz wartości pojawiają się dopiero podczas działania programu, i to ma znaczenie dla `{}`. Ten program zapisuje liczbę miejsc w sali jako `double`:

<!-- broken: seats_as_double at=8 errors=1 error=^non-constant-expression cannot be narrowed from type 'int' to 'double' in initializer list -->
```cpp
#include <iostream>

int main() {
    int rows{0};
    int chairs_per_row{0};
    std::cin >> rows;
    std::cin >> chairs_per_row;
    const double seats{rows * chairs_per_row};
    std::cout << "Seats: " << seats << "\n";
}
```

Program się nie zbuduje. Kompilator zgłasza w linijce 8 `non-constant-expression cannot be narrowed from type 'int' to 'double' in initializer list`, czyli: wyrażenia, które nie jest stałe, nie można zawęzić z `int` do `double` w nawiasach klamrowych.

- W lekcji 2.5 `const double first{7 / 2};` budowało się, bo `7 / 2` jest **stałym wyrażeniem**: kompilator zna jego wartość już podczas budowania i widzi, że da się ją zapisać w `double` bez zmiany.
- Tutaj `rows * chairs_per_row` zależy od danych, których jeszcze nie ma. Wynik typu `int`, znany dopiero podczas działania programu, `{}` traktuje przy zamianie na `double` jako konwersję zawężającą i jej nie przyjmuje.
- Linijkę `note:` z radą o jawnej zmianie typu (*explicit cast*) na razie pomiń, jak w lekcji 2.5.

Właściwa poprawka to **typ dobrany do wyniku**. Liczba miejsc jest całkowita, a `int` razy `int` daje `int`, więc wynik powinien być typu `int`:

<!-- example: seats_as_int -->
```cpp
#include <iostream>

int main() {
    int rows{0};
    int chairs_per_row{0};
    std::cin >> rows;
    std::cin >> chairs_per_row;
    const int seats{rows * chairs_per_row};
    std::cout << "Seats: " << seats << "\n";
}
```

<!-- input: seats_as_int -->
```text
5
8
```

<!-- output: seats_as_int -->
```text
Seats: 40
```

To samo zobaczysz przy dzieleniu: `const double average{points / games};` z dwiema zmiennymi `int` odczytanymi z wejścia też się nie zbuduje, z tym samym komunikatem. Nawet bez tego błędu wynik byłby zły, bo dzielenie dwóch `int` jest dzieleniem całkowitym (lekcja 2.4). Dlatego w zadaniach dobieraj typy według znaczenia danych: `int` dla liczb całkowitych, `double` dla wielkości z częścią ułamkową. Gdy w mnożeniu bierze udział `double`, wynik też jest `double` i pasuje do zmiennej `double`.

## 11. Zakładamy poprawne dane

Twoje programy zakładają na razie, że użytkownik podaje dane zgodne z prośbą: liczbę całkowitą tam, gdzie program pyta o liczbę całkowitą, i liczbę z kropką tam, gdzie pyta o liczbę z częścią ułamkową. **Program nie potrafi jeszcze poprawnie obsłużyć** sytuacji, w której ktoś:

- wpisze tekst zamiast liczby;
- nie poda wymaganej wartości;
- poda liczbę za dużą dla typu;
- poda wartość bez sensu w danej sytuacji, na przykład ujemną liczbę pudełek;
- zapisze liczbę w innej postaci, na przykład `2,75` zamiast `2.75`.

Wynik będzie wtedy po prostu zły. Sprawdzać dane i reagować na błędy nauczysz się później, gdy poznasz instrukcje, które pozwalają programowi wybierać, co zrobić. Do tego czasu w ćwiczeniach podawaj dane zgodne z opisem. Dlatego też żaden program w tej lekcji nie dzieli przez liczbę podaną przez użytkownika: ktoś mógłby wpisać 0, a dzielenia przez zero nie wolno wykonywać (lekcja 2.4).

## 12. Misja: dystans treningu

Napisz program, który liczy łączny dystans treningu biegowego. Użytkownik podaje:

1. liczbę okrążeń (liczba całkowita);
2. długość jednego okrążenia w kilometrach (liczba z częścią ułamkową).

Program liczy **łączny dystans = liczba okrążeń × długość okrążenia** i wypisuje go.

W `cpp-workspace` utwórz katalog `training_distance`, skopiuj do niego `CMakeLists.txt` z oryginalnego `lesson_05_first_program`, utwórz pusty `main.cpp` i napisz program samodzielnie.

**Pierwsze uruchomienie:** 4 okrążenia po 1.25 km.

<!-- input: training_distance -->
```text
4
1.25
```

Standardowe wyjście ma być dokładnie takie:

<!-- output: training_distance -->
```text
Enter the number of laps:
Enter the lap length in km:
Total distance: 5 km
```

**Drugie uruchomienie tego samego programu,** bez zmiany kodu: 3 okrążenia po 2.5 km.

<!-- input: training_distance -->
```text
3
2.5
```

<!-- output: training_distance -->
```text
Enter the number of laps:
Enter the lap length in km:
Total distance: 7.5 km
```

Na ekranie zobaczysz między linijkami programu także wpisane liczby (echo, punkt 6). W pierwszym uruchomieniu łączny dystans to 5.0 km, ale `std::cout` wypisuje go jako `5` (lekcja 2.5).

### Kryterium sukcesu

- Program buduje się jako C++20, a jego standardowe wyjście dla obu zestawów danych jest dokładnie takie jak powyżej.
- **Oba wyniki daje ten sam program:** między uruchomieniami nie zmieniasz kodu i nie budujesz programu ponownie.
- Liczba okrążeń trafia do zmiennej `int`, a długość okrążenia do zmiennej `double`, obie z wartościami początkowymi i bez `const`.
- Łączny dystans jest obliczany **po** odczycie obu wartości i ma typ, który pasuje do wyniku mnożenia. Umiesz ten typ uzasadnić.
- W kodzie nie ma liczb 4, 1.25, 3, 2.5, 5 ani 7.5: dane przychodzą ze standardowego wejścia, a wynik oblicza program.
- Program używa tylko tego, co już znasz, oraz `std::cin` i `>>`.
- Umiesz wyjaśnić, dlaczego wynik się zmienił, choć kod został taki sam.

Gdy wynik się zgadza, możesz zapisać projekt w Gicie, jak w lekcji 1.5.

<details>
<summary>Podpowiedź 1</summary>

Najpierw zmienne na dane, potem dla każdej wartości prośba i odczyt, na końcu obliczenie i wynik. Program z punktu 9 ma tę samą kolejność, ale inne typy.

</details>

<details>
<summary>Podpowiedź 2</summary>

`int` razy `double` daje `double` (lekcja 2.5). Jakiego typu musi więc być łączny dystans, żeby `{}` przyjęło wynik mnożenia?

</details>

Przykładowe rozwiązanie jest w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 13. Gdy coś pójdzie inaczej

| Co widzisz | Co to znaczy | Co zrobić |
|---|---|---|
| Program nic nie wypisuje albo wypisał prośbę i „stoi” | Czeka na dane przy `std::cin`. Nie zawiesił się. | Wpisz wartość w oknie programu i naciśnij **Enter**. |
| W oknie **Run** CLiona nie da się nic wpisać | To miejsce tej instrukcji nie jest jeszcze sprawdzone na każdym systemie. | Uruchom program w terminalu, jak w punkcie 3. |
| Wynik nie zależy od wpisanych danych | Obliczenie albo wypisanie stoi **przed** odczytem i korzysta z wartości początkowej. | Odczyt musi być przed obliczeniem, które z niego korzysta. |
| Wpisana liczba pojawia się na ekranie, choć jej nie wypisujesz | To echo okna, w którym piszesz, a nie wynik programu. | Nic. To nie jest standardowe wyjście programu. |
| Błąd kompilacji przy `std::cin >>` ze zmienną `const` | Do stałej nie da się wczytać wartości. | Zmienna na dane nie może mieć `const`. |
| Błąd `non-constant-expression cannot be narrowed …` przy `{}` | Wynik działania na dwóch `int` ma trafić do `double` (punkt 10). | Dobierz typ wyniku do obliczenia, na przykład `int` dla liczby miejsc. |
| Wpisano `2,75` albo tekst i wynik jest dziwny | Takich danych program jeszcze nie obsługuje (punkt 11). | Uruchom program jeszcze raz i podaj dane zgodne z prośbą, z kropką. |

## 14. Wyjaśnij

Odpowiedz własnymi słowami, najlepiej na piśmie. Dopiero potem porównaj z przykładową odpowiedzią.

**1.** Dlaczego ten sam plik wykonywalny wypisał raz `Count: 5`, a raz `Count: 12`?

<details>
<summary>Przykładowa odpowiedź</summary>

Bo program nie ma tej liczby w kodzie. Odczytuje ją przy każdym uruchomieniu ze standardowego wejścia. Kod i plik wykonywalny się nie zmieniły, zmieniły się tylko dane, a wynik od nich zależy.

</details>

**2.** Czym różni się `std::cin >> count` od `std::cout << count`?

<details>
<summary>Przykładowa odpowiedź</summary>

`std::cin >> count` pobiera wartość ze standardowego wejścia i zapisuje ją w `count`. `std::cout << count` wysyła wartość `count` na standardowe wyjście. Strzałki pokazują kierunek danych.

</details>

**3.** Na ekranie widać `Enter count:`, `5` i `Count: 5`. Które z tych linijek wypisał program?

<details>
<summary>Przykładowa odpowiedź</summary>

`Enter count:` i `Count: 5`. Linijka `5` to wpisane dane, widoczne dzięki echu okna, w którym się pisze.

</details>

**4.** Dlaczego zmienna, do której wczytujesz dane, nie może być `const`?

<details>
<summary>Przykładowa odpowiedź</summary>

Bo odczyt zmienia jej wartość: zastępuje wartość początkową wpisaną liczbą. Stałej nie można zmienić po inicjalizacji.

</details>

**5.** Opisz drogę informacji w misji, od klawiatury do wyniku.

<details>
<summary>Przykładowa odpowiedź</summary>

Użytkownik wpisuje liczby. `std::cin >>` zapisuje je w zmiennych `int` i `double`. Program mnoży te wartości i zapisuje wynik w zmiennej `double`. `std::cout <<` wypisuje wynik na standardowe wyjście.

</details>

## Podsumowanie

- Program może pobierać dane **podczas działania**. Ten sam plik wykonywalny daje wtedy różne wyniki dla różnych danych, bez zmiany kodu i bez ponownego budowania.
- `std::cin` to **standardowe wejście**, a `std::cout` to **standardowe wyjście**. `std::cin >> x` zapisuje odczytaną wartość w `x`.
- Przy `std::cin` program **czeka na dane**. **Enter** zatwierdza wpisaną wartość.
- Prośbę wypisuje `std::cout`, a odczytuje dopiero `std::cin`. Wpisane liczby widać na ekranie dzięki echu, ale nie są one wynikiem programu.
- Typ zmiennej musi pasować do danych: `int` dla liczb całkowitych, `double` dla liczb z kropką. `>>` pomija odstępy i przejścia do nowej linii między wartościami.
- Zmienna na dane ma wartość początkową i nie jest `const`. Wynik obliczenia po odczycie może być stałą.
- Wynik działania na dwóch `int` odczytanych z wejścia nie trafi przez `{}` do `double`. Dobierz typy tak, żeby pasowały do obliczenia.
- Na razie zakładamy poprawne dane. Obsługę błędnych poznasz później.

## Co dalej

Twoje programy pytają już o liczby. W lekcji 2.7 poznasz wartości tekstowe i program zapyta o słowo. **Lekcja 2.7 jest w przygotowaniu.**

---

## Przykładowe rozwiązania

Zajrzyj tutaj **po własnej próbie**. Twoje nazwy mogą się różnić, jeśli standardowe wyjście jest takie, jak wymagane.

<details>
<summary>Punkt 12: misja, dystans treningu</summary>

<!-- example: training_distance -->
```cpp
#include <iostream>

int main() {
    int laps{0};
    double lap_length_km{0.0};

    std::cout << "Enter the number of laps:\n";
    std::cin >> laps;
    std::cout << "Enter the lap length in km:\n";
    std::cin >> lap_length_km;

    const double total_distance_km{laps * lap_length_km};

    std::cout << "Total distance: " << total_distance_km << " km\n";
}
```

- `laps` jest typu `int`, bo okrążeń jest całkowita liczba. `lap_length_km` jest typu `double`, bo długość może mieć część ułamkową. Obie zmienne odbierają dane, więc nie mają `const`.
- `laps * lap_length_km` to `int` razy `double`, więc wynik jest typu `double` i pasuje do `const double total_distance_km`. Można też napisać `const auto total_distance_km{laps * lap_length_km};`: kompilator ustali typ `double`.
- Ten sam program obsługuje oba zestawy danych: 4 · 1.25 = 5 i 3 · 2.5 = 7.5.

</details>

**Poprzednia lekcja:** [Lekcja 2.5: Liczby z częścią ułamkową: `double` i `auto`](lesson_05_numbers_with_a_fractional_part.md) · **Następna lekcja:** w przygotowaniu · [Opis kursu](../../README.md)

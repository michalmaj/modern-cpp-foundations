# Lekcja 5.2: Parametry, argumenty i przekazywanie przez wartość

**Polski** · [English](lesson_02_parameters_and_arguments.en.md) · [Opis kursu](../../README.md)

> **Moduł 5, lekcja 2** · około 70–85 minut
> **Potrzebujesz:** katalogu `cpp-workspace` i oryginalnego projektu `lesson_05_first_program`, jak dotąd. Debugger nie jest w tej lekcji potrzebny.
> **Wersja pilotażowa.** Programy z tej lekcji sprawdzamy automatycznie na Windowsie, Ubuntu i macOS, także z podanymi danymi wejściowymi. Wpisywanie danych w oknie **Run** CLiona opisujemy bez ręcznego sprawdzenia na każdym systemie.

## Zanim zaczniesz

Ta lekcja zakłada, że po lekcji 5.1:

- definiujesz funkcję `void` bez parametrów przed `main` i wywołujesz ją z `main`;
- wiesz, że ciało funkcji wykonuje się dopiero przy wywołaniu, a potem program wraca za miejsce wywołania;
- piszesz pętle `for` z licznikiem i `++` (lekcja 4.3);
- wiesz, że zmienna istnieje tylko w bloku, w którym ją zadeklarowano (lekcje 3.2 i 4.3).

## Sytuacja

Funkcja `show_workshop_rules` z lekcji 5.1 robi zawsze dokładnie to samo. To wystarczało, bo zasady warsztatu się nie zmieniały. Często jednak potrzebujesz **podobnego** zadania dla **różnych danych**: linii o różnej długości, słupka o różnej wysokości. W tej lekcji funkcja dostanie dane z miejsca wywołania.

Po tej lekcji będziesz:

- wyjaśniać, po co funkcji parametr;
- wskazywać parametr w definicji i argument w wywołaniu;
- wywoływać funkcję z literałem, ze zmienną i z wyrażeniem;
- definiować funkcję z dwoma parametrami i dobierać kolejność argumentów;
- wyjaśniać, co znaczy przekazywanie przez wartość, i przewidywać, czy zmiana parametru zmieni zmienną w `main`;
- rozpoznawać błąd zasięgu parametru i zamienione argumenty;
- pisać funkcję, której argumenty sterują wypisywaniem.

## 1. Przygotuj projekt

W `cpp-workspace` utwórz katalog `lesson_5_2` i skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program`. Programy z punktów 3–10 wpisujesz w `main.cpp` tego katalogu.

## 2. Funkcja, która potrzebuje informacji

Program ma wypisywać linie z myślników: raz trzy znaki `-`, innym razem pięć. Ze znanych Ci narzędzi wynikają dwie osobne funkcje:

<!-- fragment -->
```cpp
void print_three_dashes() {
    std::cout << "---\n";
}

void print_five_dashes() {
    std::cout << "-----\n";
}
```

A gdyby potrzebna była linia z czterech, siedmiu albo dwudziestu znaków? Każda długość to nowa funkcja, prawie identyczna z poprzednimi. Różnią się tylko **jedną informacją**: liczbą znaków.

**Zastanów się:** skąd funkcja mogłaby się dowiedzieć, jak długą linię ma wypisać?

<details>
<summary>Omówienie</summary>

Tę informację zna tylko miejsce wywołania: raz potrzeba trzech znaków, raz pięciu. Funkcja potrzebuje więc sposobu, żeby przy każdym wywołaniu **dostać** liczbę znaków od tego, kto ją wywołuje. Wtedy wystarczy jedna funkcja dla wszystkich długości.

</details>

## 3. Pierwszy parametr

Oto jedna funkcja dla linii dowolnej długości:

<!-- example: line_lengths -->
```cpp
#include <iostream>

void print_line(int length) {
    for (int position{0}; position < length; ++position) {
        std::cout << "-";
    }

    std::cout << "\n";
}

int main() {
    print_line(3);
    print_line(5);
}
```

- `print_line` to nazwa funkcji, a `void` znaczy, jak w lekcji 5.1, że funkcja nie przekazuje wyniku do miejsca wywołania.
- **`int length`** w nawiasach to **parametr**: zmienna funkcji, która przy każdym wywołaniu **otrzymuje wartość**. `int` to jej typ, a `length` to nazwa, której używasz w ciele funkcji.
- Ciało funkcji korzysta z wartości `length`: pętla `for` wypisuje tyle myślników, ile wynosi `length`, a potem kończy linię.
- **`print_line(3);`** wywołuje funkcję i przekazuje jej wartość 3. W tym wywołaniu `length` ma wartość 3. W wywołaniu `print_line(5);` ma wartość 5.

**Przewidź**, co wypisze program. Zapisz odpowiedź, a potem go uruchom.

<details>
<summary>Standardowe wyjście</summary>

<!-- output: line_lengths -->
```text
---
-----
```

Program ma **jedną** definicję funkcji. Zmieniają się tylko dane przekazywane w kolejnych wywołaniach.

</details>

## 4. Parametr i argument

Zestaw definicję z wywołaniem:

| | W kodzie | Co to jest |
|---|---|---|
| **Parametr** | `int length` w definicji `void print_line(int length)` | Nazwana zmienna funkcji. Przy każdym wywołaniu otrzymuje wartość. |
| **Argument** | `5` w wywołaniu `print_line(5);` | Wyrażenie podane przy wywołaniu. Jego wartość otrzymuje parametr. |

Argument nie musi być liczbą wpisaną wprost. Może nim być zmienna albo całe wyrażenie:

<!-- fragment -->
```cpp
const int separator_length{4};
print_line(separator_length);
print_line(separator_length + 2);
```

W pierwszym wywołaniu argumentem jest `separator_length`, więc `length` otrzymuje wartość 4. W drugim argumentem jest wyrażenie `separator_length + 2`, więc `length` otrzymuje 6. Parametr i argument to nie dwie nazwy tej samej zmiennej: parametr `length` należy do funkcji, a `separator_length` do `main`.

Wywołania z argumentami znasz już z funkcji biblioteki standardowej, na przykład `std::getline(std::cin, line)`. Teraz piszesz własną funkcję, która przyjmuje dane. Funkcje biblioteczne nie zawsze otrzymują dane tak jak nasz parametr `int`. Do tego wrócimy w dalszych modułach.

## 5. Przewidź: kilka wywołań jednej funkcji

Funkcja `print_line` jest taka sama jak w punkcie 3. Zmienia się tylko `main`:

<!-- example: line_calls -->
```cpp
#include <iostream>

void print_line(int length) {
    for (int position{0}; position < length; ++position) {
        std::cout << "-";
    }

    std::cout << "\n";
}

int main() {
    const int separator_length{4};

    std::cout << "Literal 3:\n";
    print_line(3);
    std::cout << "Variable:\n";
    print_line(separator_length);
    std::cout << "Expression:\n";
    print_line(separator_length + 2);
    std::cout << "Zero:\n";
    print_line(0);
    std::cout << "Done\n";
}
```

**Przewidź**, zanim uruchomisz program:

1. Ile razy zostanie wywołana funkcja `print_line`?
2. Ile przebiegów wykona pętla `for` w każdym wywołaniu?
3. Ile myślników będzie w każdej linii?
4. Co zostanie wypisane dla długości zero?

<details>
<summary>Standardowe wyjście i wyjaśnienie</summary>

<!-- output: line_calls -->
```text
Literal 3:
---
Variable:
----
Expression:
------
Zero:

Done
```

- Funkcja jest wywołana 4 razy, z wartościami 3, 4, 6 i 0. Pętla wykonuje 3, 4, 6 i 0 przebiegów.
- **Dla zera** pierwsze sprawdzenie warunku, `0 < 0`, daje `false`, więc pętla nie wypisuje żadnego myślnika. Instrukcja `std::cout << "\n";` stoi jednak **za** pętlą, więc wykonuje się zawsze. Dlatego między `Zero:` a `Done` widać **pustą linię**: linię bez znaków, ale z jej zakończeniem.

</details>

## 6. Przekazywanie przez wartość

W tej funkcji parametr **zmienia się** w ciele:

<!-- example: pass_by_value -->
```cpp
#include <iostream>

void count_down(int remaining) {
    while (remaining > 0) {
        std::cout << remaining << "\n";
        remaining = remaining - 1;
    }
}

int main() {
    int laps{3};

    count_down(laps);

    std::cout << "Caller value: " << laps << "\n";
}
```

**Przewidź**: co wypisze funkcja i jaką wartość `laps` wypisze `main` po powrocie z funkcji?

<details>
<summary>Standardowe wyjście</summary>

<!-- output: pass_by_value -->
```text
3
2
1
Caller value: 3
```

</details>

Co się tu dzieje:

- Wywołanie `count_down(laps)` przekazuje funkcji **wartość** zmiennej `laps`, czyli 3.
- Parametr `remaining` otrzymuje **własną** wartość 3. Jest zmienną funkcji, a nie inną nazwą zmiennej `laps`.
- W ciele funkcji `remaining` maleje do 0. To zmienia tylko `remaining`.
- Po powrocie do `main` zmienna `laps` nadal ma wartość 3.

To jest **przekazywanie przez wartość**: **funkcja pracuje na własnej wartości parametru, otrzymanej z argumentu.** Tak działają parametry, które poznajesz w tej lekcji, na przykład `int length` i `int remaining`. C++ ma też inne sposoby przekazywania danych do funkcji. Poznasz je w dalszej części kursu.

**Sprawdź.** Zmień w `main` nazwę `laps` na `remaining`, w trzech miejscach, tak żeby zmienna w `main` nazywała się tak samo jak parametr. Funkcja się nie zmienia:

<!-- example: pass_by_value_same_name -->
```cpp
#include <iostream>

void count_down(int remaining) {
    while (remaining > 0) {
        std::cout << remaining << "\n";
        remaining = remaining - 1;
    }
}

int main() {
    int remaining{3};

    count_down(remaining);

    std::cout << "Caller value: " << remaining << "\n";
}
```

**Przewidź**, czy wynik będzie inny, a potem uruchom program.

<details>
<summary>Standardowe wyjście i wyjaśnienie</summary>

<!-- output: pass_by_value_same_name -->
```text
3
2
1
Caller value: 3
```

Wynik jest taki sam. To nadal **dwie różne zmienne**: jedna należy do `main`, druga, parametr, do funkcji `count_down`. Ta sama nazwa ich nie łączy. Parametr otrzymuje tylko wartość argumentu.

</details>

## 7. Tabela zmian wartości

Tak zmieniają się wartości w programie z punktu 6, w wersji z `laps`:

| Moment | `laps` w `main` | `remaining` w `count_down` | Wypisane |
|---|---|---|---|
| przed wywołaniem | 3 | nie istnieje | |
| początek funkcji | 3 | 3 | |
| po pierwszym przebiegu | 3 | 2 | `3` |
| po drugim przebiegu | 3 | 1 | `2` |
| po trzecim przebiegu | 3 | 0 | `1` |
| sprawdzenie `remaining > 0` | 3 | 0, warunek `false` | |
| po powrocie do `main` | 3 | nie istnieje | `Caller value: 3` |

**Odpowiedz:** dlaczego zmienna `laps` nie staje się zerem?

<details>
<summary>Odpowiedź</summary>

Bo funkcja nigdy nie zmienia `laps`. Przy wywołaniu parametr `remaining` otrzymał wartość `laps`, czyli 3, i od tej chwili jest osobną zmienną funkcji. Instrukcja `remaining = remaining - 1;` zmienia tylko `remaining`. Gdy funkcja się kończy, jej parametr przestaje istnieć, a w `main` zostaje niezmienione `laps`. Funkcja `void` nie przekazuje też niczego z powrotem do `main`.

</details>

## 8. Dwa parametry

Funkcja może mieć kilka parametrów. Rozdziela się je przecinkiem:

<!-- example: pair_order -->
```cpp
#include <iostream>

void show_pair(int first, int second) {
    std::cout << "First: " << first << "\n";
    std::cout << "Second: " << second << "\n";
}

int main() {
    show_pair(2, 5);
    show_pair(5, 2);

    const int low{1};
    const int high{9};
    show_pair(high, low);
}
```

- Funkcja `show_pair` ma dwa parametry: `first` i `second`.
- Każde wywołanie podaje **dwa argumenty**, też rozdzielone przecinkiem.
- **Pierwszy argument trafia do pierwszego parametru, a drugi do drugiego.** Decyduje kolejność, nie nazwy zmiennych w `main`.

**Przewidź** wszystkie sześć linijek. Zwróć uwagę na ostatnie wywołanie: która wartość trafi do `first`?

<details>
<summary>Standardowe wyjście i wyjaśnienie</summary>

<!-- output: pair_order -->
```text
First: 2
Second: 5
First: 5
Second: 2
First: 9
Second: 1
```

W ostatnim wywołaniu pierwszym argumentem jest `high`, więc `first` otrzymuje 9, a `second` otrzymuje 1. Nazwy `low` i `high` nie mają tu znaczenia: liczy się tylko pozycja argumentu w nawiasach.

</details>

## 9. Znajdź błąd: zamienione argumenty

Wymaganie: program odczytuje dwie liczby całkowite i wypisuje **pierwszą odczytaną** jako `First`, a **drugą** jako `Second`. Zakładamy, że użytkownik wpisuje dwie liczby całkowite.

<!-- example: pair_bug -->
```cpp
#include <iostream>

void show_pair(int first, int second) {
    std::cout << "First: " << first << "\n";
    std::cout << "Second: " << second << "\n";
}

int main() {
    int first_value{0};
    int second_value{0};

    std::cout << "Enter two values:\n";
    std::cin >> first_value;
    std::cin >> second_value;

    show_pair(second_value, first_value);
}
```

Program buduje się bez błędów i bez ostrzeżeń. Sprawdź go dla dwóch przypadków:

| Przypadek | Dane |
|---|---|
| A | `3`, `3` |
| B | `2`, `5` |

1. Przeczytaj wymaganie i zapisz poprawne standardowe wyjście dla obu przypadków.
2. **Przewidź**, co wypisze **ten** program.
3. Uruchom go dla obu przypadków.
4. Znajdź przypadek, który ujawnia błąd, i miejsce błędu w kodzie.
5. Popraw program.
6. Sprawdź ponownie oba przypadki.

Wyniki przed poprawką, wyjaśnienie i poprawiony program są w części [Przykładowe rozwiązania](#przykładowe-rozwiązania). Zajrzyj tam po własnej próbie.

## 10. Gdzie istnieje parametr?

Parametr, jak zmienna zadeklarowana w bloku (lekcje 3.2 i 4.3), istnieje tylko **w swojej funkcji**. Ten program po wywołaniu funkcji próbuje wypisać `length` w `main`:

<!-- broken: param_scope at=13:32 error=^use of undeclared identifier 'length' -->
```cpp
#include <iostream>

void print_line(int length) {
    for (int position{0}; position < length; ++position) {
        std::cout << "-";
    }

    std::cout << "\n";
}

int main() {
    print_line(4);
    std::cout << "Length: " << length << "\n";
}
```

**Przewidź**, czy ten program się zbuduje. Potem spróbuj go zbudować i przeczytaj komunikat kompilatora.

<details>
<summary>Co zgłasza kompilator i dlaczego</summary>

Program się nie zbuduje. Kompilator zgłasza w linijce 13 `use of undeclared identifier 'length'`. `length` to parametr funkcji `print_line`, więc istnieje tylko w jej ciele. W `main` nie ma żadnej zmiennej o tej nazwie. Wywołanie `print_line(4)` przekazuje funkcji wartość 4, ale nie tworzy w `main` zmiennej `length`.

Kompilator dopisuje do tego komunikatu podpowiedź `did you mean '__NSConstantString_tag::length'?` i zgłasza w tej samej linijce drugi błąd. `__NSConstantString_tag` to nazwa wbudowana w kompilator, niezwiązana z Twoim programem: kompilator szukał podobnej nazwy i trafił na tę. Podpowiedzi kompilatora bywają chybione. Liczy się pierwsza część komunikatu: w `main` nazwa `length` jest nieznana.

</details>

**Poprawka:** jeśli `main` ma korzystać z tej samej wartości, przechowuje ją we **własnej** zmiennej i przekazuje jako argument. Poprawiony program jest w części [Przykładowe rozwiązania](#przykładowe-rozwiązania). Nie przenoś zmiennej poza funkcje, żeby była widoczna wszędzie: każda funkcja ma swoje zmienne, a dane przekazuje się przez argumenty.

## 11. Misja: wykres aktywności

Program rysuje tekstowy wykres aktywności z trzech dni. Użytkownik podaje, ile bloków aktywności było w każdym dniu. Program wypisuje dla każdego dnia jeden słupek ze znaków `#`.

**Wymagania:**

- Program wypisuje `Enter blocks for days 1, 2 and 3:` i odczytuje trzy liczby całkowite, kolejno dla dni 1, 2 i 3.
- Jeśli nie udało się odczytać wszystkich trzech liczb, program wypisuje tylko `Input could not be read` i nie rysuje wykresu.
- Jeśli odczytano trzy liczby, ale choć jedna jest spoza zakresu od 0 do 6, program wypisuje tylko `Invalid bar data` i nie rysuje wykresu.
- Dla poprawnych danych program wypisuje dokładnie trzy linijki, dla dni 1, 2 i 3, w formacie `Day N: [` + tyle znaków `#`, ile bloków + `]`. Dla zera bloków słupek to `[]`.
- Program nie pyta ponownie.
- Jeden słupek wypisuje **Twoja własna funkcja `void` z dwoma parametrami `int`**: numerem dnia i liczbą bloków. Nazwy parametrów i ich kolejność w definicji wybierasz samodzielnie, ale argumenty w każdym wywołaniu muszą trafić do właściwych parametrów.
- Odczyt danych, ich sprawdzenie i decyzję o wywołaniach podejmuje `main`. Funkcja odpowiada tylko za wypisanie jednego słupka.
- Nie używaj zmiennych zadeklarowanych poza funkcjami.

Do sprawdzenia, czy odczyt się udał, wystarczy `std::cin.fail()` z lekcji 4.5. Nie musisz odzyskiwać wejścia ani sprawdzać, co jeszcze stoi w linijce po liczbie.

W `cpp-workspace` utwórz katalog `activity_chart`, skopiuj do niego `CMakeLists.txt` z oryginalnego `lesson_05_first_program`, utwórz pusty `main.cpp` i napisz program samodzielnie.

Dla danych `2`, `0`, `4` standardowe wyjście ma być takie:

<!-- input: activity_chart -->
```text
2
0
4
```

<!-- output: activity_chart -->
```text
Enter blocks for days 1, 2 and 3:
Day 1: [##]
Day 2: []
Day 3: [####]
```

**To nie jest `print_line` ani `show_pair` z nowymi nazwami.** `print_line` miała jeden parametr i zawsze ten sam znak, a `show_pair` tylko wypisywała dwie wartości. Tutaj funkcja dostaje **dwie wartości o różnych rolach**: jedna jest wypisywana jako numer, druga steruje pętlą. Musi też złożyć jedną linijkę z kilku części. Musisz samodzielnie zdecydować:

1. jakie parametry ma funkcja i w jakiej kolejności;
2. jak funkcja buduje jedną linijkę, także dla zera bloków;
3. jak `main` sprawdza dane, zanim narysuje cokolwiek;
4. jakie argumenty dostaje funkcja w każdym z trzech wywołań.

**Zanim napiszesz program**, przygotuj tabelę przypadków testowych: same zera, górna granica 6, kilka różnych wartości, wartość ujemna, wartość powyżej 6, tekst zamiast liczby i dane, które kończą się po dwóch liczbach. Przy każdym przypadku zapisz oczekiwane standardowe wyjście. Dla danych `2`, `0`, `4` zapisz też, jakie argumenty dostaje funkcja w każdym wywołaniu.

Przypadek z danymi, które kończą się wcześniej, przeanalizuj na papierze, jak w lekcjach 4.5–4.7, zamiast go uruchamiać: przyjmij, że po ostatniej linijce wejście się kończy, prześledź program i porównaj odpowiedź ze zwiniętą listą kontrolną. Program z tej lekcji jest dla takich danych sprawdzany osobno, automatycznymi testami kursu.

### Kryterium sukcesu

- Program buduje się jako C++20, a jego standardowe wyjście dla danych `2`, `0`, `4` jest dokładnie takie jak powyżej.
- Dla każdego przypadku, który możesz wpisać, standardowe wyjście zgadza się z listą kontrolną. Przypadek z danymi kończącymi się po dwóch liczbach sprawdzasz rozumowaniem: prześledzony program wypisuje te same linijki co lista kontrolna.
- Słupek wypisuje Twoja funkcja `void` z dwoma parametrami `int`, zdefiniowana przed `main`. Znak `#` występuje w kodzie tylko w tej funkcji.
- Dla zera bloków słupek to `[]`.
- Przy nieudanym odczycie albo danych spoza zakresu nie pojawia się żaden słupek.
- Program nie używa zmiennych zadeklarowanych poza funkcjami.
- Tabela przypadków powstała przed uruchomieniem programu.
- Umiesz wskazać w swoim programie parametry i argumenty oraz wyjaśnić, który argument trafia do którego parametru.

Gdy wynik się zgadza, możesz zapisać projekt w Gicie, jak w lekcji 1.5.

<details>
<summary>Podpowiedź 1</summary>

Jakie dwie informacje są potrzebne funkcji, żeby wypisać jeden właściwy słupek?

</details>

<details>
<summary>Podpowiedź 2</summary>

Numer dnia i liczba znaków `#` mają różne zadania. Zastanów się, gdzie wykorzystać każdą wartość.

</details>

<details>
<summary>Podpowiedź 3</summary>

Funkcja może wypisać początek linii, następnie powtórzyć znak `#` w pętli, a na końcu zamknąć nawias.

</details>

<details>
<summary>Pełna lista przypadków kontrolnych: otwórz po przygotowaniu własnej tabeli</summary>

| Dane | Standardowe wyjście po pytaniu | Co sprawdza |
|---|---|---|
| `2`, `0`, `4` | `Day 1: [##]`, `Day 2: []`, `Day 3: [####]` | różne wartości, także zero |
| `0`, `0`, `0` | trzy razy pusty słupek `[]` | same zera |
| `6`, `6`, `6` | trzy słupki po sześć `#` | górna granica |
| `1`, `4`, `0` | `[#]`, `[####]`, `[]` | numer dnia nie jest mylony z długością |
| `5`, `1`, `3` | `[#####]`, `[#]`, `[###]` | kolejny nierówny zestaw |
| `-1`, `2`, `3` | `Invalid bar data` | wartość ujemna |
| `2`, `7`, `1` | `Invalid bar data` | wartość powyżej zakresu |
| `abc`, `1`, `2` | `Input could not be read` | tekst zamiast liczby |
| `1`, `2`, koniec danych | `Input could not be read` | dane kończą się przed trzecią liczbą |

Przypadek `2`, `0`, `4` jest sprawdzony wyżej, przy treści misji.

<!-- input: activity_chart -->
```text
0
0
0
```

<!-- output: activity_chart -->
```text
Enter blocks for days 1, 2 and 3:
Day 1: []
Day 2: []
Day 3: []
```

<!-- input: activity_chart -->
```text
6
6
6
```

<!-- output: activity_chart -->
```text
Enter blocks for days 1, 2 and 3:
Day 1: [######]
Day 2: [######]
Day 3: [######]
```

<!-- input: activity_chart -->
```text
1
4
0
```

<!-- output: activity_chart -->
```text
Enter blocks for days 1, 2 and 3:
Day 1: [#]
Day 2: [####]
Day 3: []
```

<!-- input: activity_chart -->
```text
5
1
3
```

<!-- output: activity_chart -->
```text
Enter blocks for days 1, 2 and 3:
Day 1: [#####]
Day 2: [#]
Day 3: [###]
```

<!-- input: activity_chart -->
```text
-1
2
3
```

<!-- output: activity_chart -->
```text
Enter blocks for days 1, 2 and 3:
Invalid bar data
```

<!-- input: activity_chart -->
```text
2
7
1
```

<!-- output: activity_chart -->
```text
Enter blocks for days 1, 2 and 3:
Invalid bar data
```

<!-- input: activity_chart -->
```text
abc
1
2
```

<!-- output: activity_chart -->
```text
Enter blocks for days 1, 2 and 3:
Input could not be read
```

<!-- input: activity_chart -->
```text
1
2
```

<!-- output: activity_chart -->
```text
Enter blocks for days 1, 2 and 3:
Input could not be read
```

</details>

Przykładowe rozwiązanie jest w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 12. Gdy coś pójdzie inaczej

| Co widzisz | Co to znaczy | Co zrobić |
|---|---|---|
| `use of undeclared identifier` z nazwą parametru | Parametru użyto poza jego funkcją, na przykład w `main` (punkt 10). | W `main` używaj własnej zmiennej i przekazuj ją jako argument. |
| Błąd kompilacji przy wywołaniu: kompilator nie znajduje pasującej funkcji | Liczba argumentów nie zgadza się z liczbą parametrów. | Policz parametry w definicji i argumenty w wywołaniu. |
| Słupki mają długość numeru dnia, a numery dni są dziwne | Argumenty w wywołaniu stoją w innej kolejności niż parametry w definicji. | Porównaj kolejność parametrów i argumentów, pozycja po pozycji. |
| Dla zera bloków brakuje `[]` albo linijka nie jest zakończona | Nawias zamykający lub koniec linii stoi w pętli albo jest pomijany. | Początek i koniec linijki wypisuj poza pętlą. W pętli tylko `#`. |
| Słupek ma o jeden znak `#` za dużo albo za mało | Licznik pętli zaczyna się od innej wartości, niż zakłada warunek. | Sprawdź w tabeli przebiegu słupek z 1 bloku. |
| Wykres pojawia się mimo złych danych | Funkcja jest wywoływana przed sprawdzeniem danych. | Najpierw sprawdź odczyt i zakres, wywołuj funkcję tylko dla poprawnych danych. |
| Zmienna w `main` „nie zmienia się”, choć funkcja zmienia parametr | Tak działa przekazywanie przez wartość (punkt 6). | To nie błąd. Funkcja pracuje na własnej wartości parametru. |
| Program nic nie robi i czeka | Czeka na kolejną liczbę, jak w lekcji 2.6. | Wpisz liczbę i naciśnij **Enter**. Przypadku z końcem danych nie sprawdzaj w ten sposób: prześledź go na papierze. |

## 13. Wyjaśnij

Odpowiedz własnymi słowami, najlepiej na piśmie. Dopiero potem porównaj z przykładowymi odpowiedziami.

1. Po co funkcji parametr?
2. Czym parametr różni się od argumentu?
3. Czy argument musi być literałem?
4. Co oznacza `int length` w definicji funkcji?
5. Czy funkcja może zostać wywołana kilka razy z innymi argumentami?
6. W jakiej kolejności wartości trafiają do parametrów?
7. Dlaczego zamiana dwóch argumentów typu `int` może nie powodować błędu kompilacji?
8. Co oznacza przekazywanie przez wartość?
9. Dlaczego zmiana `remaining` nie zmienia `laps`?
10. Czy parametr jest automatycznie dostępny w `main`?
11. Czy funkcja `void` może mieć parametry?
12. Dlaczego funkcja wypisująca słupek nie musi wiedzieć, skąd pochodzą dane?
13. Co powinno się stać dla słupka długości zero?
14. Dlaczego test z dwiema równymi wartościami nie wykrywa każdej zamiany argumentów?

<details>
<summary>Przykładowe odpowiedzi</summary>

1. Żeby jedna funkcja mogła wykonać podobne zadanie dla różnych danych. Dane dostaje przy każdym wywołaniu, więc nie trzeba pisać osobnej funkcji dla każdej wartości.
2. Parametr to nazwana zmienna w definicji funkcji. Argument to wyrażenie podane przy wywołaniu. Jego wartość otrzymuje parametr.
3. Nie. Argumentem może być literał, zmienna albo wyrażenie, na przykład `separator_length + 2`.
4. Że funkcja ma parametr o nazwie `length` i typie `int`. Przy każdym wywołaniu `length` otrzymuje wartość argumentu.
5. Tak. Każde wywołanie może przekazać inną wartość, a ciało funkcji wykonuje się wtedy z tą wartością.
6. Według pozycji: pierwszy argument trafia do pierwszego parametru, drugi do drugiego. Nazwy zmiennych w `main` nie mają znaczenia.
7. Bo obie wartości mają ten sam typ, więc wywołanie jest poprawnym C++. Kompilator nie wie, która liczba miała być która. To błąd logiczny, nie błąd kompilacji.
8. Że parametr otrzymuje wartość argumentu i funkcja pracuje na tej własnej wartości. Zmiana parametru nie zmienia zmiennej, którą podano jako argument.
9. Bo `remaining` jest osobną zmienną funkcji, która tylko otrzymała wartość `laps`. Zmienia się wyłącznie `remaining`.
10. Nie. Parametr istnieje tylko w swojej funkcji. W `main` jego nazwa jest nieznana.
11. Tak. `void` mówi tylko, że funkcja nie przekazuje wyniku. Parametry określają, jakie dane funkcja otrzymuje.
12. Bo dostaje gotowe wartości jako argumenty. Odczyt i sprawdzenie danych należą do `main`, a funkcja tylko wypisuje słupek dla otrzymanych wartości.
13. Powinna pojawić się linijka `Day N: []`: pętla nie wypisuje żadnego `#`, ale początek i koniec linijki są wypisywane zawsze.
14. Bo gdy obie wartości są równe, zamiana daje te same liczby na tych samych miejscach. Dopiero różne wartości pokazują, która trafiła do którego parametru.

</details>

## Podsumowanie

- **Parametr** to nazwana zmienna funkcji, zapisana w nawiasach definicji, na przykład `int length`. Przy każdym wywołaniu otrzymuje wartość.
- **Argument** to wyrażenie podane przy wywołaniu: literał, zmienna albo wyrażenie, na przykład `print_line(separator_length + 2)`.
- Jedna funkcja z parametrem może wykonywać podobne zadanie dla różnych danych.
- Przy kilku parametrach argumenty trafiają do parametrów **według pozycji**. Nazwy zmiennych w miejscu wywołania nie mają znaczenia.
- Jeśli dwa parametry mają ten sam typ, kompilator nie wykryje zamienionych argumentów. Ujawni je dopiero test z różnymi wartościami.
- **Przekazywanie przez wartość:** funkcja pracuje na własnej wartości parametru, otrzymanej z argumentu. Zmiana parametru nie zmienia zmiennej w miejscu wywołania.
- Parametr istnieje tylko w swojej funkcji. W `main` jego nazwa jest nieznana.
- Funkcja `void` może mieć parametry: `void` dotyczy tylko wyniku.

## Co dalej

Funkcje z tej lekcji dostają dane, ale niczego nie oddają: wszystko, co wyliczą, mogą tylko wypisać. W kolejnej lekcji zobaczysz, jak funkcja może przekazać wynik z powrotem do miejsca wywołania. Lekcja 5.3 jest w przygotowaniu.

---

## Przykładowe rozwiązania

Zajrzyj tutaj **po własnej próbie**. Twoje nazwy mogą się różnić, jeśli standardowe wyjście jest takie, jak wymagane.

<details>
<summary>Punkt 9: wyniki przed poprawką i poprawiony program</summary>

Przed poprawką, przypadek A, dane `3`, `3`:

<!-- input: pair_bug -->
```text
3
3
```

<!-- output: pair_bug -->
```text
Enter two values:
First: 3
Second: 3
```

Przypadek B, dane `2`, `5`:

<!-- input: pair_bug -->
```text
2
5
```

<!-- output: pair_bug -->
```text
Enter two values:
First: 5
Second: 2
```

- **Przypadek A wygląda poprawnie**, bo obie wartości są równe: zamiana daje te same liczby na tych samych miejscach.
- **Przypadek B ujawnia błąd:** pierwsza odczytana wartość, 2, powinna być `First`, a pojawia się jako `Second`.
- **Przyczyna:** wywołanie `show_pair(second_value, first_value)` podaje argumenty w odwrotnej kolejności. Definicja funkcji jest poprawna. Oba argumenty mają typ `int`, więc kompilator nie zgłasza ani błędu, ani ostrzeżenia.
- **Poprawka:** `show_pair(first_value, second_value);`.

<!-- example: pair_fixed -->
```cpp
#include <iostream>

void show_pair(int first, int second) {
    std::cout << "First: " << first << "\n";
    std::cout << "Second: " << second << "\n";
}

int main() {
    int first_value{0};
    int second_value{0};

    std::cout << "Enter two values:\n";
    std::cin >> first_value;
    std::cin >> second_value;

    show_pair(first_value, second_value);
}
```

<!-- input: pair_fixed -->
```text
3
3
```

<!-- output: pair_fixed -->
```text
Enter two values:
First: 3
Second: 3
```

<!-- input: pair_fixed -->
```text
2
5
```

<!-- output: pair_fixed -->
```text
Enter two values:
First: 2
Second: 5
```

</details>

<details>
<summary>Punkt 10: poprawiony program</summary>

`main` przechowuje wartość we własnej zmiennej, przekazuje ją jako argument i sam ją wypisuje:

<!-- example: param_scope_fixed -->
```cpp
#include <iostream>

void print_line(int length) {
    for (int position{0}; position < length; ++position) {
        std::cout << "-";
    }

    std::cout << "\n";
}

int main() {
    const int requested_length{4};

    print_line(requested_length);
    std::cout << "Length: " << requested_length << "\n";
}
```

<!-- output: param_scope_fixed -->
```text
----
Length: 4
```

</details>

<details>
<summary>Punkt 11: misja, wykres aktywności</summary>

<!-- example: activity_chart -->
```cpp
#include <iostream>

void print_bar(int day, int blocks) {
    std::cout << "Day " << day << ": [";

    for (int block{0}; block < blocks; ++block) {
        std::cout << "#";
    }

    std::cout << "]\n";
}

int main() {
    int first_day_blocks{0};
    int second_day_blocks{0};
    int third_day_blocks{0};

    std::cout << "Enter blocks for days 1, 2 and 3:\n";
    std::cin >> first_day_blocks;
    std::cin >> second_day_blocks;
    std::cin >> third_day_blocks;

    if (std::cin.fail()) {
        std::cout << "Input could not be read\n";
    } else {
        const bool first_valid{first_day_blocks >= 0 && first_day_blocks <= 6};
        const bool second_valid{second_day_blocks >= 0 && second_day_blocks <= 6};
        const bool third_valid{third_day_blocks >= 0 && third_day_blocks <= 6};

        if (first_valid && second_valid && third_valid) {
            print_bar(1, first_day_blocks);
            print_bar(2, second_day_blocks);
            print_bar(3, third_day_blocks);
        } else {
            std::cout << "Invalid bar data\n";
        }
    }
}
```

- **Funkcja `print_bar`** ma dwa parametry o różnych rolach. `day` jest tylko wypisywany, a `blocks` steruje pętlą. Początek linijki i `]` z końcem linii stoją poza pętlą, więc dla zera bloków powstaje `Day N: []`.
- **Argumenty:** w każdym wywołaniu pierwszy argument to numer dnia, a drugi to liczba bloków, w tej samej kolejności co parametry. Dla danych `2`, `0`, `4` funkcja dostaje kolejno (1, 2), (2, 0) i (3, 4).
- **`main`** odczytuje dane, sprawdza je i decyduje o wywołaniach. Funkcja nie wie, skąd pochodzą wartości.
- **Nieudany odczyt:** po nieudanym odczycie także kolejne odczyty się nie udają, więc wystarczy jedno sprawdzenie `std::cin.fail()` po trzech odczytach. Dotyczy to też danych, które kończą się po dwóch liczbach: odczyt trzeciej się nie udaje. Wartości zmiennych nie są wtedy używane.
- **Sprawdzenie zakresu** stoi w gałęzi udanego odczytu, z trzema nazwanymi warunkami jak w lekcji 3.4. Wykres powstaje tylko wtedy, gdy wszystkie trzy są spełnione.
- Parametry można też ustawić w definicji w odwrotnej kolejności, na przykład `print_bar(int blocks, int day)`. Wtedy poprawne wywołanie dla pierwszego dnia to `print_bar(first_day_blocks, 1)`. Oba układy są dobre, jeśli definicja i wywołania są zgodne.

</details>

**Poprzednia lekcja:** [Lekcja 5.1: Pierwsza własna funkcja (`void`)](lesson_01_the_first_function.md) · **Następna lekcja:** w przygotowaniu · [Opis kursu](../../README.md)

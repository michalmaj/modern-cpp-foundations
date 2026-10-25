# Lekcja 5.6: Deklaracja, definicja i linkowanie

**Polski** · [English](lesson_06_declaration_and_definition.en.md) · [Opis kursu](../../README.md)

> **Moduł 5, lekcja 6** · około 40–55 minut
> **Potrzebujesz:** katalogu `cpp-workspace` i oryginalnego projektu `lesson_05_first_program`, jak dotąd. Debugger nie jest w tej lekcji potrzebny.
> **Wersja pilotażowa.** Programy z tej lekcji sprawdzamy automatycznie na Windowsie, Ubuntu i macOS, także z podanymi danymi wejściowymi. Wpisywanie danych w oknie **Run** CLiona opisujemy bez ręcznego sprawdzenia na każdym systemie.

## Zanim zaczniesz

Ta lekcja zakłada, że:

- piszesz programy z kilkoma współpracującymi funkcjami, a funkcje pomocnicze zapisujesz przed funkcjami, które z nich korzystają (lekcja 5.5);
- wiesz, że wywołanie funkcji zapisanej pod `main` kończy się błędem `use of undeclared identifier` (lekcja 5.1);
- pamiętasz z lekcji 1.4, że budowanie programu ma dwa etapy: kompilację i linkowanie.

## Sytuacja

Do tej pory każda funkcja musiała stać w pliku przed swoim pierwszym wywołaniem. To działa, ale narzuca kolejność: najpierw funkcje pomocnicze, na końcu `main`. W tej lekcji odpowiesz na dwa pytania. **Czy funkcję można wywołać, zanim w pliku pojawi się jej definicja?** I **dlaczego program może przejść kompilację, a mimo to nie przejść linkowania?**

Po tej lekcji będziesz:

- odróżniać deklarację funkcji od jej definicji i od wywołania;
- zapisywać deklarację funkcji zakończoną średnikiem;
- umieszczać `main` przed definicjami własnych funkcji;
- sprawdzać, czy deklaracja pasuje do definicji;
- odróżniać błąd kompilacji od błędu linkowania i naprawiać oba.

## 1. Przygotuj projekt

W `cpp-workspace` utwórz katalog `lesson_5_6` i skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program`. Programy z punktów 2–7 wpisujesz w `main.cpp` tego katalogu.

## 2. Znany układ i jedna zmiana

Ten układ znasz z lekcji 5.5: definicja funkcji stoi przed `main`, więc w miejscu wywołania kompilator już ją zna.

<!-- example: score_definition_first -->
```cpp
#include <iostream>

int double_points(int points) {
    return points * 2;
}

int main() {
    std::cout << "Score: " << double_points(4) << "\n";
}
```

<!-- output: score_definition_first -->
```text
Score: 8
```

Teraz ktoś przenosi całą definicję **pod** `main`:

<!-- broken: score_undeclared at=4:31 errors=1 error=^use of undeclared identifier 'double_points' -->
```cpp
#include <iostream>

int main() {
    std::cout << "Score: " << double_points(4) << "\n";
}

int double_points(int points) {
    return points * 2;
}
```

**Przewidź**, czy ten program się zbuduje. Jeśli nie, na którym etapie: kompilacji czy linkowania? Potem spróbuj go zbudować.

<details>
<summary>Co zgłasza kompilator i dlaczego</summary>

Program się nie zbuduje. Kompilator zgłasza w linijce 4 `use of undeclared identifier 'double_points'`, tak jak w lekcji 5.1. To **błąd kompilacji**: kompilator czyta plik od góry i w miejscu wywołania nie zna jeszcze nazwy `double_points`. Definicja stoi niżej w tym samym pliku, ale to nie sprawia, że kompilator zna nazwę wcześniej. Kompilacja się nie kończy, więc do linkowania w ogóle nie dochodzi.

</details>

## 3. Deklaracja funkcji

Żeby wywołać funkcję, kompilator nie potrzebuje od razu jej ciała. Wystarczy mu wiedza, **jaka to funkcja**: jak się nazywa, co zwraca i jakie parametry przyjmuje. Taką wiedzę daje **deklaracja**:

<!-- fragment -->
```cpp
int double_points(int points);
```

| Część | Znaczenie |
|---|---|
| `int` | typ wyniku |
| `double_points` | nazwa funkcji |
| `int points` | parametr i jego typ |
| `;` | koniec deklaracji: w tym miejscu nie ma ciała funkcji |

Deklaracja mówi kompilatorowi, jaką funkcję można wywołać. Nie zawiera instrukcji, nie wykonuje żadnego obliczenia i nie zastępuje funkcji.

**Definicja** to funkcja razem z ciałem, czyli to, co znasz od lekcji 5.1:

<!-- fragment -->
```cpp
int double_points(int points) {
    return points * 2;
}
```

Definicja dostarcza instrukcje, które wykonują się przy wywołaniu. **Definicja jest jednocześnie deklaracją**: też mówi kompilatorowi, jak się nazywa funkcja, co zwraca i co przyjmuje. Dlatego programy z definicjami przed `main` działały bez osobnych deklaracji i nadal są poprawne.

## 4. Deklaracja przed `main`, definicja pod `main`

Ten program ma deklarację przed `main` i definicję po nim:

<!-- example: score_declaration_first -->
```cpp
#include <iostream>

int double_points(int points);

int main() {
    std::cout << "Score: " << double_points(4) << "\n";
}

int double_points(int points) {
    return points * 2;
}
```

Wskaż w nim: deklarację, `main`, wywołanie funkcji, definicję i instrukcję `return`. **Przewidź**, czy program się zbuduje i co wypisze.

<details>
<summary>Standardowe wyjście i wyjaśnienie</summary>

<!-- output: score_declaration_first -->
```text
Score: 8
```

Wynik jest taki sam jak w punkcie 2. W miejscu wywołania kompilator zna już funkcję dzięki deklaracji w linijce 3, więc kompilacja się udaje. Ciało funkcji stoi niżej, w definicji. Deklaracja niczego nie wykonała: przy wywołaniu program wykonuje instrukcje z definicji.

</details>

**Deklaracja i definicja muszą do siebie pasować**, bo opisują tę samą funkcję:

| Co | W deklaracji | W definicji |
|---|---|---|
| nazwa funkcji | `double_points` | `double_points` |
| typ wyniku | `int` | `int` |
| liczba parametrów | 1 | 1 |
| typy parametrów, w tej samej kolejności | `int` | `int` |

W deklaracji można pominąć nazwę parametru. To nadal deklaracja tej samej funkcji:

<!-- fragment -->
```cpp
int double_points(int);
```

W definicji nazwa jest potrzebna, bo ciało funkcji odwołuje się do wartości parametru. Nazwy w deklaracji i definicji nie muszą być takie same. Muszą się za to zgadzać typy. Gdyby typy parametrów w deklaracji i definicji się różniły, nie byłaby to już ta sama funkcja. Tego przypadku w tej lekcji nie omawiamy: trzymaj deklaracje i definicje zgodne.

## 5. Kilka deklaracji na początku pliku

Deklaracje pozwalają opisać wszystkie funkcje na początku pliku. Funkcje z lekcji 5.5 mogłyby wyglądać tak:

<!-- fragment -->
```cpp
int base_price(int weight);
int zone_surcharge(int zone);
int shipping_cost(int weight, int zone);

int main() {
    // reading, checking and the report
}

// the definitions of the three functions
```

W tym programie dwie funkcje współpracują, a definicje stoją pod `main`, w dowolnej kolejności:

<!-- example: score_two_declarations -->
```cpp
#include <iostream>

int double_points(int points);
int score_with_bonus(int points);

int main() {
    std::cout << "Score: " << score_with_bonus(4) << "\n";
}

int score_with_bonus(int points) {
    return double_points(points) + 5;
}

int double_points(int points) {
    return points * 2;
}
```

**Przewidź** wynik. Zwróć uwagę, że `score_with_bonus` wywołuje `double_points`, choć definicja `double_points` stoi w pliku niżej.

<details>
<summary>Standardowe wyjście i wyjaśnienie</summary>

<!-- output: score_two_declarations -->
```text
Score: 13
```

`score_with_bonus(4)` wywołuje `double_points(4)`, dostaje 8 i dodaje 5. W miejscu tego wywołania kompilator zna `double_points` z deklaracji na początku pliku, więc kolejność definicji nie ma znaczenia. Funkcje nadal przekazują sobie wartości przez parametry i `return`. Zmieniła się organizacja kodu, a nie to, jak działa wywołanie.

</details>

Układ z `main` na początku to **jedna z możliwych** organizacji pliku, a nie obowiązek. Definicje przed `main`, jak w lekcji 5.5, też są dobrym rozwiązaniem i nie potrzebują osobnych deklaracji.

## 6. Kompilacja a linkowanie

W lekcji 1.4 budowanie programu miało dwa etapy:

- **Kompilacja:** kompilator sprawdza kod źródłowy i tłumaczy go na plik obiektowy.
- **Linkowanie:** linker łączy plik obiektowy z kodem biblioteki i kodem startowym w program. Musi przy tym odnaleźć definicje funkcji, z których program korzysta.

Deklaracja wystarcza **kompilatorowi**: dzięki niej wie, że funkcja istnieje i jak ją wywołać. Wywoływana funkcja nadal potrzebuje jednak **definicji**, a jej szuka **linker**.

## 7. Znajdź błąd: deklaracja bez definicji

W tym programie funkcja jest zadeklarowana i wywołana, ale nigdzie nie ma jej definicji:

<!-- broken: score_missing_definition stage=link error=double_points -->
```cpp
#include <iostream>

int double_points(int points);

int main() {
    std::cout << "Score: " << double_points(4) << "\n";
}
```

**Przewidź**, czy program się zbuduje. Jeśli nie, na którym etapie i dlaczego? Potem spróbuj go zbudować i przeczytaj komunikat.

<details>
<summary>Co się dzieje i dlaczego</summary>

1. **Kompilacja się udaje.** W miejscu wywołania kompilator zna funkcję z deklaracji, więc nie ma czego zgłosić. Powstaje plik obiektowy.
2. **Linkowanie się nie udaje.** Linker szuka definicji `double_points`, bo `main` ją wywołuje, i nie znajduje jej nigdzie.
3. Budowanie kończy się niepowodzeniem i program do uruchomienia nie powstaje.

Komunikat pochodzi od linkera, nie od kompilatora, i na każdym systemie wygląda trochę inaczej. Na Ubuntu linker pisze `undefined reference to 'double_points(int)'`, na macOS `"double_points(int)", referenced from`, a na Windowsie `undefined symbol: int __cdecl double_points(int)`. Na końcu pojawia się też `linker command failed`. Nie musisz pamiętać tych komunikatów. Ważne, że wskazują nazwę funkcji, której definicji brakuje, i że błąd pojawia się **po** kompilacji.

Sama deklaracja bez definicji nie zawsze jest błędem. Tutaj problem polega na tym, że funkcja jest **wywoływana**, więc program potrzebuje jej definicji.

</details>

**Popraw program:** sprawdź, że deklaracja istnieje i że funkcja jest wywoływana, a potem dopisz definicję pasującą do deklaracji. Nie usuwaj wywołania i nie przenoś obliczenia do `main`. Zbuduj program ponownie, uruchom go i porównaj wynik z punktem 4. Poprawiony program jest w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

**Dwa błędy, dwa etapy:**

| Sytuacja | Etap, który się nie udaje | Przyczyna | Naprawa |
|---|---|---|---|
| Wywołanie bez wcześniejszej deklaracji (punkt 2) | kompilacja | kompilator nie zna funkcji w miejscu wywołania | dopisz deklarację przed wywołaniem albo przenieś definicję wyżej |
| Deklaracja i wywołanie bez definicji (punkt 7) | linkowanie | brakuje definicji wywoływanej funkcji | dopisz definicję |
| Zgodna deklaracja i definicja (punkt 4) | budowanie się udaje | funkcja jest znana i ma definicję | |

## 8. Misja: plan sali warsztatowej

Sala warsztatowa ma 10 miejsc. Dwie grupy zgłaszają liczbę uczestników, a program sprawdza, czy wszyscy się zmieszczą.

**Wymagania:**

- Program wypisuje `Enter group sizes (0-8):` i odczytuje dwie liczby całkowite: liczebność pierwszej i drugiej grupy.
- Jeśli odczyt się nie uda, wypisuje tylko `Input could not be read`.
- Jeśli którakolwiek liczba jest spoza zakresu od 0 do 8, wypisuje tylko `Invalid group size`.
- Dla poprawnych danych wypisuje `Total attendees: N` i jedną z linijek: `Room status: Fits` albo `Room status: Too many people`. Dokładnie 10 osób się mieści, 11 i więcej już nie.
- Program nie pyta ponownie.
- Program ma **co najmniej dwie własne funkcje**: jedna oblicza łączną liczbę osób i zwraca `int`, druga ustala, czy łączna liczba nie przekracza pojemności sali, i zwraca `bool`. **Druga funkcja korzysta z wyniku pierwszej.** Nazwy funkcji i parametrów wybierasz samodzielnie.
- Funkcje niczego nie wypisują i niczego nie odczytują. Komunikat statusu wybiera `main` na podstawie wyniku `bool`: w raporcie nie pojawia się `0` ani `1`.
- **Układ pliku:** najpierw `#include`, potem deklaracje obu funkcji, potem `main`, a na końcu definicje funkcji.
- Nie używaj zmiennych zadeklarowanych poza funkcjami.

W `cpp-workspace` utwórz katalog `room_plan`, skopiuj do niego `CMakeLists.txt` z oryginalnego `lesson_05_first_program`, utwórz pusty `main.cpp` i napisz program samodzielnie.

Dla danych `4` i `5`:

<!-- input: room_plan -->
```text
4
5
```

<!-- output: room_plan -->
```text
Enter group sizes (0-8):
Total attendees: 9
Room status: Fits
```

Dla danych `5` i `5`, czyli dokładnie na granicy pojemności:

<!-- input: room_plan -->
```text
5
5
```

<!-- output: room_plan -->
```text
Enter group sizes (0-8):
Total attendees: 10
Room status: Fits
```

Dla danych `6` i `5`:

<!-- input: room_plan -->
```text
6
5
```

<!-- output: room_plan -->
```text
Enter group sizes (0-8):
Total attendees: 11
Room status: Too many people
```

**To nie jest `double_points` z nowymi nazwami.** W punktach 2–7 funkcja była gotowa, a zmieniało się tylko jej miejsce w pliku. Tutaj musisz samodzielnie zdecydować:

1. jak nazwać obie funkcje, jakie mają typy wyników i parametry, w jakiej kolejności;
2. jak zapisać deklaracje zgodne z definicjami;
3. jak druga funkcja korzysta z wyniku pierwszej;
4. co zostaje w `main`: odczyt, sprawdzenie danych i wybór komunikatu.

**Zanim napiszesz program**, przygotuj tabelę przypadków testowych: same zera, jedna pusta grupa, łączna liczba 9, 10 i 11, obie grupy po 8, wartości tuż poza zakresem dla każdej grupy, tekst zamiast pierwszej i zamiast drugiej liczby oraz dane, które kończą się po jednej liczbie. Przy każdym przypadku zapisz oczekiwane standardowe wyjście.

Przypadki z danymi, które kończą się wcześniej, przeanalizuj na papierze, jak w lekcjach 4.5–5.5, zamiast je uruchamiać, i porównaj ze zwiniętą listą kontrolną. Program z tej lekcji jest dla takich danych sprawdzany osobno, automatycznymi testami kursu.

### Kryterium sukcesu

- Program buduje się jako C++20, a jego standardowe wyjście dla trzech przykładów powyżej jest dokładnie takie, jak pokazano.
- Dla każdego przypadku, który możesz wpisać, standardowe wyjście zgadza się z listą kontrolną. Przypadki z danymi, które kończą się wcześniej, sprawdzasz rozumowaniem.
- Plik ma układ: `#include`, deklaracje, `main`, definicje. Każda deklaracja pasuje do swojej definicji.
- Funkcja `bool` korzysta z wyniku funkcji `int`, a obie niczego nie wypisują i nie odczytują.
- Po nieudanym odczycie albo danych spoza zakresu nie pojawia się `Total attendees`.
- Program nie używa zmiennych zadeklarowanych poza funkcjami.
- Tabela przypadków powstała przed uruchomieniem programu.
- Umiesz wskazać w swoim programie każdą deklarację, każdą definicję i każde wywołanie.

Gdy wynik się zgadza, możesz zapisać projekt w Gicie, jak w lekcji 1.5.

<details>
<summary>Podpowiedź 1</summary>

Jakie informacje kompilator powinien znać o obu funkcjach, zanim dotrze do `main`?

</details>

<details>
<summary>Podpowiedź 2</summary>

Deklaracja podaje nazwę, typ wyniku i typy parametrów. Definicja zawiera także instrukcje wykonywane przez funkcję.

</details>

<details>
<summary>Podpowiedź 3</summary>

Zapisz najpierw deklaracje obu funkcji, następnie `main`, a dopiero poniżej ich definicje. Sprawdź, czy wywołanie jednej funkcji przez drugą korzysta z właściwych argumentów.

</details>

<details>
<summary>Pełna lista przypadków kontrolnych: otwórz po przygotowaniu własnej tabeli</summary>

| Grupa 1 | Grupa 2 | Standardowe wyjście po pytaniu | Co sprawdza |
|---|---|---|---|
| 4 | 5 | `Total attendees: 9`, `Room status: Fits` | przykład z treści |
| 5 | 5 | `Total attendees: 10`, `Room status: Fits` | dokładnie pojemność sali |
| 6 | 5 | `Total attendees: 11`, `Room status: Too many people` | o jedną osobę za dużo |
| 0 | 0 | `Total attendees: 0`, `Room status: Fits` | same zera |
| 0 | 8 | `Total attendees: 8`, `Room status: Fits` | jedna pusta grupa |
| 8 | 2 | `Total attendees: 10`, `Room status: Fits` | pojemność, górna granica grupy 1 |
| 2 | 8 | `Total attendees: 10`, `Room status: Fits` | pojemność, górna granica grupy 2 |
| 8 | 8 | `Total attendees: 16`, `Room status: Too many people` | obie grupy pełne |
| -1 | 2 | `Invalid group size` | pierwsza tuż pod zakresem |
| 2 | -1 | `Invalid group size` | druga tuż pod zakresem |
| 9 | 0 | `Invalid group size` | pierwsza tuż nad zakresem |
| 0 | 9 | `Invalid group size` | druga tuż nad zakresem |
| `abc` | `2` | `Input could not be read` | tekst zamiast pierwszej liczby |
| `2` | `abc` | `Input could not be read` | tekst zamiast drugiej liczby |
| `2` | koniec danych | `Input could not be read` | dane kończą się po jednej liczbie |
| brak danych | brak danych | `Input could not be read` | dane kończą się od razu |

Pierwsze trzy przypadki są sprawdzone wyżej, przy treści misji.

<!-- input: room_plan -->
```text
0
0
```

<!-- output: room_plan -->
```text
Enter group sizes (0-8):
Total attendees: 0
Room status: Fits
```

<!-- input: room_plan -->
```text
0
8
```

<!-- output: room_plan -->
```text
Enter group sizes (0-8):
Total attendees: 8
Room status: Fits
```

<!-- input: room_plan -->
```text
8
2
```

<!-- output: room_plan -->
```text
Enter group sizes (0-8):
Total attendees: 10
Room status: Fits
```

<!-- input: room_plan -->
```text
2
8
```

<!-- output: room_plan -->
```text
Enter group sizes (0-8):
Total attendees: 10
Room status: Fits
```

<!-- input: room_plan -->
```text
8
8
```

<!-- output: room_plan -->
```text
Enter group sizes (0-8):
Total attendees: 16
Room status: Too many people
```

<!-- input: room_plan -->
```text
-1
2
```

<!-- output: room_plan -->
```text
Enter group sizes (0-8):
Invalid group size
```

<!-- input: room_plan -->
```text
2
-1
```

<!-- output: room_plan -->
```text
Enter group sizes (0-8):
Invalid group size
```

<!-- input: room_plan -->
```text
9
0
```

<!-- output: room_plan -->
```text
Enter group sizes (0-8):
Invalid group size
```

<!-- input: room_plan -->
```text
0
9
```

<!-- output: room_plan -->
```text
Enter group sizes (0-8):
Invalid group size
```

<!-- input: room_plan -->
```text
abc
2
```

<!-- output: room_plan -->
```text
Enter group sizes (0-8):
Input could not be read
```

<!-- input: room_plan -->
```text
2
abc
```

<!-- output: room_plan -->
```text
Enter group sizes (0-8):
Input could not be read
```

<!-- input: room_plan -->
```text
2
```

<!-- output: room_plan -->
```text
Enter group sizes (0-8):
Input could not be read
```

<!-- input: room_plan -->
```text
```

<!-- output: room_plan -->
```text
Enter group sizes (0-8):
Input could not be read
```

</details>

**Po misji: dwa osobne eksperymenty.** Każdy zacznij od programu, który działa poprawnie, i po każdym przywróć go do tego stanu. Nie łącz obu zmian naraz.

- **Eksperyment A.** Usuń deklarację tej funkcji, którą wywołuje `main`. **Przewidź**, który etap budowania się nie uda. Zbuduj program, porównaj z punktem 2 i przywróć deklarację.
- **Eksperyment B.** Zostaw deklaracje, ale usuń definicję funkcji, która jest wywoływana. **Przewidź**, który etap się nie uda. Zbuduj program, porównaj z punktem 7 i przywróć definicję.

<details>
<summary>Co powinno się stać</summary>

- **Eksperyment A:** kompilacja się nie udaje. W miejscu wywołania w `main` kompilator nie zna funkcji, jak w punkcie 2. Kompilator zgłasza `use of undeclared identifier` z nazwą funkcji.
- **Eksperyment B:** kompilacja się udaje, bo deklaracja nadal istnieje, ale linkowanie się nie udaje, bo brakuje definicji wywoływanej funkcji, jak w punkcie 7. Komunikat pochodzi od linkera i zawiera nazwę funkcji.

</details>

Przykładowe rozwiązanie jest w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 9. Gdy coś pójdzie inaczej

| Co widzisz | Co to znaczy | Co zrobić |
|---|---|---|
| `use of undeclared identifier` z nazwą Twojej funkcji | W miejscu wywołania kompilator nie zna funkcji: brakuje deklaracji albo stoi ona niżej niż wywołanie. | Dopisz deklarację przed pierwszym wywołaniem, na przykład przed `main`. |
| `undefined reference`, `undefined symbol` albo `referenced from`, a na końcu `linker command failed` | Funkcja jest zadeklarowana i wywołana, ale linker nie znajduje jej definicji. | Dopisz definicję zgodną z deklaracją. Sprawdź, czy nazwa w definicji jest taka sama. |
| Błąd linkowania, choć definicja jest w pliku | Definicja nie pasuje do deklaracji, na przykład ma inną nazwę albo inne typy parametrów. | Porównaj deklarację i definicję: nazwa, typ wyniku, liczba i typy parametrów. |
| Błąd kompilacji przy deklaracji | Brakuje średnika na końcu deklaracji. | Deklaracja kończy się `;`, a definicja ciałem w klamrach. |
| W raporcie pojawia się `0` albo `1` | Wynik `bool` jest wypisywany bezpośrednio. | Niech `main` wybierze komunikat przez `if`. |
| Po nieudanym odczycie albo złych danych pojawia się raport | Funkcje są wywoływane przed sprawdzeniem danych. | Najpierw sprawdź odczyt i zakres, a dopiero potem licz i wypisuj. |
| Program nic nie robi i czeka | Czeka na kolejną liczbę, jak w lekcji 2.6. | Wpisz liczbę i naciśnij **Enter**. Przypadku z końcem danych nie sprawdzaj w ten sposób: prześledź go na papierze. |

## 10. Wyjaśnij

Odpowiedz własnymi słowami, najlepiej na piśmie. Dopiero potem porównaj z przykładowymi odpowiedziami.

1. Co to jest deklaracja funkcji?
2. Co to jest definicja?
3. Co to jest wywołanie?
4. Czym różni się deklaracja od definicji?
5. Dlaczego deklaracja kończy się średnikiem?
6. Czy deklaracja wykonuje instrukcje funkcji?
7. Czy definicja umieszczona przed `main` może zastąpić osobną deklarację?
8. Czy wolno umieścić `main` przed definicjami własnych funkcji?
9. Co musi wtedy znaleźć się wcześniej?
10. Czy nazwy parametrów w deklaracji są obowiązkowe?
11. Dlaczego typy parametrów muszą odpowiadać używanej funkcji?
12. Co się dzieje, gdy wywołamy funkcję nieznaną kompilatorowi?
13. Co się dzieje, gdy wywoływana funkcja jest zadeklarowana, ale nie ma definicji?
14. Czym różni się błąd kompilacji od błędu linkowania?
15. Czy komunikaty linkerów na różnych systemach muszą wyglądać identycznie?
16. Czy każde wywołanie własnej funkcji wymaga wcześniejszej osobnej deklaracji zakończonej średnikiem?

<details>
<summary>Przykładowe odpowiedzi</summary>

1. Informacja dla kompilatora, jaka funkcja istnieje: typ wyniku, nazwa i typy parametrów, zakończona średnikiem, bez ciała.
2. Funkcja razem z ciałem, czyli z instrukcjami, które wykonują się przy wywołaniu.
3. Miejsce, w którym program każe wykonać funkcję: nazwa, argumenty w nawiasach.
4. Deklaracja tylko opisuje funkcję. Definicja też ją opisuje, ale dodatkowo zawiera ciało z instrukcjami.
5. Bo w tym miejscu nie ma ciała funkcji. Średnik kończy opis funkcji.
6. Nie. Deklaracja niczego nie wykonuje. Wykonują się instrukcje z definicji, gdy program dojdzie do wywołania.
7. Tak. Definicja jest też deklaracją, więc definicja przed miejscem wywołania wystarcza.
8. Tak, jeśli kompilator zna funkcje w miejscach ich wywołań.
9. Deklaracje funkcji wywoływanych w `main`, na przykład na początku pliku.
10. Nie. W deklaracji wystarczą typy, na przykład `int double_points(int);`. W definicji nazwa jest potrzebna, żeby ciało mogło użyć wartości parametru.
11. Bo deklaracja i definicja muszą opisywać tę samą funkcję. Inne typy parametrów oznaczałyby inną funkcję.
12. Kompilacja się nie udaje: kompilator zgłasza `use of undeclared identifier`.
13. Kompilacja się udaje, ale linkowanie nie: linker nie znajduje definicji wywoływanej funkcji i program nie powstaje.
14. Błąd kompilacji zgłasza kompilator, gdy kod jednego pliku jest niepoprawny, na przykład gdy nie zna nazwy. Błąd linkowania zgłasza linker, gdy łączy program i nie znajduje czegoś, czego program potrzebuje, na przykład definicji funkcji.
15. Nie. Na każdym systemie linker jest inny i pisze inaczej. Ważne jest, na którym etapie pojawił się błąd i której funkcji dotyczy.
16. Nie. Wystarczy, że w miejscu wywołania kompilator zna funkcję, z deklaracji albo z wcześniejszej definicji.

</details>

## Podsumowanie

- **Deklaracja** opisuje funkcję: typ wyniku, nazwa, typy parametrów i średnik. Nie ma ciała i niczego nie wykonuje.
- **Definicja** to funkcja z ciałem. Jest też deklaracją, więc definicja przed miejscem wywołania wystarcza.
- **Wywołanie** każe wykonać funkcję. W miejscu wywołania kompilator musi znać funkcję: z deklaracji albo z wcześniejszej definicji.
- Z deklaracjami na początku pliku możesz umieścić `main` przed definicjami, w dowolnej kolejności definicji. To jedna z możliwych organizacji, a nie obowiązek.
- Deklaracja i definicja muszą do siebie pasować: nazwa, typ wyniku, liczba i typy parametrów. Nazwy parametrów w deklaracji można pominąć.
- **Brak deklaracji** w miejscu wywołania to **błąd kompilacji**. **Brak definicji** wywoływanej funkcji to **błąd linkowania**: kompilacja się udaje, ale program nie powstaje.
- Komunikaty linkerów różnią się między systemami. Ważne są etap i nazwa funkcji.

## Co dalej

Znasz już podstawy własnych funkcji: definicję i wywołanie, parametry, wynik, kilka dróg do `return`, współpracę funkcji oraz deklaracje. Kolejna lekcja jest w przygotowaniu.

---

## Przykładowe rozwiązania

Zajrzyj tutaj **po własnej próbie**. Twoje nazwy mogą się różnić, jeśli standardowe wyjście jest takie, jak wymagane.

<details>
<summary>Punkt 7: program z dopisaną definicją</summary>

Deklaracja i wywołanie zostają bez zmian. Dochodzi definicja pasująca do deklaracji:

<!-- example: score_definition_added -->
```cpp
#include <iostream>

int double_points(int points);

int main() {
    std::cout << "Score: " << double_points(4) << "\n";
}

int double_points(int points) {
    return points * 2;
}
```

<!-- output: score_definition_added -->
```text
Score: 8
```

Teraz udają się oba etapy: kompilator zna funkcję z deklaracji, a linker znajduje jej definicję.

</details>

<details>
<summary>Punkt 8: misja, plan sali</summary>

<!-- example: room_plan -->
```cpp
#include <iostream>

int total_attendees(int first_group, int second_group);
bool fits_in_room(int first_group, int second_group);

int main() {
    int first_group{0};
    int second_group{0};

    std::cout << "Enter group sizes (0-8):\n";
    std::cin >> first_group;
    std::cin >> second_group;

    if (std::cin.fail()) {
        std::cout << "Input could not be read\n";
    } else {
        const bool first_valid{first_group >= 0 && first_group <= 8};
        const bool second_valid{second_group >= 0 && second_group <= 8};

        if (first_valid && second_valid) {
            std::cout << "Total attendees: " << total_attendees(first_group, second_group) << "\n";

            if (fits_in_room(first_group, second_group)) {
                std::cout << "Room status: Fits\n";
            } else {
                std::cout << "Room status: Too many people\n";
            }
        } else {
            std::cout << "Invalid group size\n";
        }
    }
}

bool fits_in_room(int first_group, int second_group) {
    const int room_capacity{10};
    return total_attendees(first_group, second_group) <= room_capacity;
}

int total_attendees(int first_group, int second_group) {
    return first_group + second_group;
}
```

- **Układ pliku:** `#include`, dwie deklaracje, `main`, dwie definicje. Każda deklaracja ma te same typy i tę samą kolejność parametrów co definicja.
- **Kolejność definicji:** `fits_in_room` stoi przed `total_attendees`, choć ją wywołuje. Działa to, bo w miejscu wywołania kompilator zna `total_attendees` z deklaracji na początku pliku.
- **Współpraca:** `fits_in_room` nie powtarza dodawania, tylko korzysta z wyniku `total_attendees` i porównuje go z pojemnością `<= 10`. Dokładnie 10 osób się mieści.
- **`main`** sprawdza odczyt i zakres, wypisuje łączną liczbę osób i wybiera komunikat statusu na podstawie wyniku `bool`.
- **Nieudany odczyt** albo dane spoza zakresu kończą program jednym komunikatem, bez wywołania funkcji.

</details>

**Poprzednia lekcja:** [Lekcja 5.5: Kilka funkcji, jeden program](lesson_05_several_functions.md) · **Następna lekcja:** w przygotowaniu · [Opis kursu](../../README.md)

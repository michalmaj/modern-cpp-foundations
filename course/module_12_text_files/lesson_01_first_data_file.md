# Lekcja 12.1: Pierwszy plik z danymi

**Polski** · [English](lesson_01_first_data_file.en.md) · [Opis kursu](../../README.md)

> **Moduł 12, lekcja 1** · około 90–110 minut, można ją podzielić na dwa podejścia
> **Potrzebujesz:** katalogu `cpp-workspace` i oryginalnego projektu `lesson_05_first_program`, jak dotąd. Debugger nie jest w tej lekcji potrzebny.
> **Wersja pilotażowa.** Programy z tej lekcji sprawdzamy automatycznie na Windowsie, Ubuntu i macOS, z podanymi plikami danych. Kroki w CLionie (nowy plik, pole **Working directory** w konfiguracji uruchomienia) opisujemy według dokumentacji CLion 2026.3, bez ręcznego sprawdzenia na każdym systemie.

## Zanim zaczniesz

Ta lekcja zakłada, że:

- wiesz, że powłoka zawsze ma bieżący katalog, a ścieżka względna liczy się od niego (lekcje 0.1 i 0.2);
- budujesz i uruchamiasz w CLionie projekt z `main.cpp` i `CMakeLists.txt`, a program wykonywalny powstaje w katalogu budowania, zwykle `cmake-build-debug` (lekcja 0.5);
- odczytujesz liczby przez `>>`, który pomija spacje i przejścia do nowej linii (lekcja 2.6);
- sprawdzasz przez `fail()`, czy odczyt się udał, zanim sprawdzisz wartość (lekcje 4.5 i 10.3);
- odczytujesz najpierw liczbę, która zapowiada, ile wartości nastąpi, a potem w pętli dokładnie tyle wartości, i przy pierwszym błędzie kończysz `main` przez `return 0;`, bez częściowego raportu (lekcja 10.3).

## Sytuacja

Aplikacja w telefonie liczy kroki i na koniec każdego dnia zapisuje ich liczbę. Chcesz zsumować kroki z kilku dni. Programy z Modułu 10 dostawały dane z klawiatury, więc przy każdym uruchomieniu trzeba je było wpisywać od nowa w oknie **Run**. Gdy dane już gdzieś są, wygodniej trzymać je w **pliku tekstowym**: przygotowujesz go raz, a program odczytuje go sam przy każdym uruchomieniu.

W tej lekcji program sam otworzy plik `steps.txt` i odczyta z niego liczby. Odpowiesz na trzy pytania: **jak program otwiera plik? Gdzie go szuka? Co ma zrobić, gdy pliku nie da się otworzyć albo gdy brakuje w nim danych?**

Po tej lekcji będziesz:

- tworzyć prosty plik tekstowy z danymi dla programu;
- otwierać go przez `std::ifstream` i sprawdzać, czy otwarcie się udało;
- odczytywać z niego liczby znanym operatorem `>>` i sprawdzać każdy odczyt;
- ustalać katalog roboczy programu w CLionie i umieszczać w nim plik danych;
- odróżniać brak pliku, pusty plik i plik, który zapowiada zero wartości;
- naprawiać sytuację, w której poprawny program nie znajduje poprawnego pliku.

## 1. Plik z danymi i jego kontrakt

`steps.txt` to zwykły plik tekstowy, taki jak `lista.txt` z lekcji 0.1. Dane z dwóch dni wyglądają w nim tak:

<!-- run: steps -->

<!-- datafile: steps steps.txt -->
```text
2
4200
7350
```

**Kontrakt pliku**, czyli zasady, które musi spełniać, żeby program mógł z niego policzyć wynik:

- pierwsza liczba to liczba dni, od 0 do 5;
- po niej następuje dokładnie tyle liczb, ile dni: kroki z kolejnych dni, każda liczba od 0 do 20000;
- liczby są oddzielone spacjami albo przejściami do nowej linii. W przykładach każda stoi w osobnej linii, bo tak łatwiej czytać plik, ale `>>` pomija spacje i przejścia do nowej linii tak samo jak przy odczycie z klawiatury (lekcja 2.6). Granice linii nie mają więc dla programu znaczenia;
- program odczytuje tylko liczby, które zapowiada pierwsza liczba. Czy po nich w pliku coś jeszcze jest, w tej lekcji nie sprawdzamy.

Największa możliwa suma to 5 · 20000 = 100000, więc dla danych zgodnych z kontraktem wynik bezpiecznie mieści się w `int`.

Program wypisuje raport dopiero wtedy, gdy odczytał i sprawdził wszystkie wymagane liczby. Każda inna sytuacja kończy się jednym komunikatem, bez częściowego raportu:

| Sytuacja | Standardowe wyjście |
|---|---|
| pliku nie udało się otworzyć | `Cannot open steps.txt` |
| plik jest otwarty, ale wymaganej liczby nie udało się odczytać | `Input error` |
| liczba jest odczytana, ale nie mieści się w swoim zakresie, także liczba dni | `Invalid steps` |
| wszystkie wymagane liczby są odczytane i poprawne | `Days: N` i `Total steps: T` |

Po każdym z tych wyników program kończy się kodem 0, jak w Module 10. Komunikaty trafiają na standardowe wyjście.

**Plik z danymi to nie plik źródłowy.** `main.cpp` i `steps.txt` są zwykłymi plikami tekstowymi, ale mają różne role:

| | `main.cpp` | `steps.txt` |
|---|---|---|
| co zawiera | kod programu | dane, które program odczytuje |
| kto go czyta | kompilator, podczas budowania | działający program, podczas uruchomienia |
| czy jest w `add_executable` | tak | nie |
| co trzeba zrobić po jego zmianie | zbudować program ponownie | nic: wystarczy uruchomić program jeszcze raz |

## 2. Pierwszy strumień plikowy: `std::ifstream`

Ten program otwiera `steps.txt`, sprawdza dane według kontraktu i wypisuje raport:

<!-- example: steps -->
```cpp
#include <fstream>
#include <iostream>

int main() {
    std::ifstream input{"steps.txt"};

    if (input.fail()) {
        std::cout << "Cannot open steps.txt\n";
        return 0;
    }

    int days{0};
    input >> days;

    if (input.fail()) {
        std::cout << "Input error\n";
        return 0;
    }

    if (days < 0 || days > 5) {
        std::cout << "Invalid steps\n";
        return 0;
    }

    int total_steps{0};

    for (int day{0}; day < days; ++day) {
        int steps{0};
        input >> steps;

        if (input.fail()) {
            std::cout << "Input error\n";
            return 0;
        }

        if (steps < 0 || steps > 20000) {
            std::cout << "Invalid steps\n";
            return 0;
        }

        total_steps += steps;
    }

    std::cout << "Days: " << days << "\n";
    std::cout << "Total steps: " << total_steps << "\n";
}
```

Nowe są tylko trzy linijki: `#include <fstream>`, utworzenie zmiennej `input` i sprawdzenie `input.fail()` zaraz po nim. Reszta to schemat z lekcji 10.3, tyle że zamiast `std::cin` program odczytuje z `input`.

| Zapis | Co robi |
|---|---|
| `#include <fstream>` | dołącza nagłówek strumieni plikowych (*file streams*), tak jak `<iostream>` dołącza `std::cin` i `std::cout` |
| `std::ifstream input{"steps.txt"};` | tworzy zmienną `input` typu `std::ifstream` i od razu próbuje otworzyć do odczytu plik o nazwie `steps.txt`. Nie odczytuje jeszcze żadnych danych |
| `input.fail()` zaraz po utworzeniu | `true`, gdy pliku nie udało się otworzyć; ta sama funkcja składowa co `std::cin.fail()` z lekcji 4.5 |
| `input >> days;` | odczytuje liczbę z pliku tak, jak `std::cin >> days;` odczytuje ją z klawiatury |
| `input.fail()` po odczycie | `true`, gdy odczyt się nie udał, jak dotąd |

- **`std::ifstream`** to skrót od *input file stream*, strumień wejściowy z pliku. `std::cin` jest strumieniem z klawiatury, a `input` strumieniem z pliku. Odczytujesz z obu tak samo: przez `>>`, a powodzenie sprawdzasz przez `fail()`.
- **Nazwę zmiennej wybierasz samodzielnie.** `input` to zwykła nazwa zmiennej, jak `count` czy `total`.
- **Plik zamyka się sam,** gdy kończy się zmienna `input`, tu razem z `main`. Nie musisz go zamykać ręcznie.

**Kolejność sprawdzeń** jest ta sama dla każdej wymaganej liczby:

1. Czy plik się otworzył? Jeśli nie: `Cannot open steps.txt`. Bez otwartego pliku nie ma czego odczytywać.
2. Czy odczyt liczby się udał? Jeśli nie: `Input error`. Wartości, której nie udało się odczytać, program nie porównuje z zakresem.
3. Czy odczytana liczba mieści się w swoim zakresie? Jeśli nie: `Invalid steps`.
4. Dopiero potem program przechodzi do następnej liczby.

**Nieudane otwarcie to nie to samo co nieudany odczyt.** Nieudane otwarcie znaczy, że program w ogóle nie dostał pliku: nie ma go tam, gdzie program szuka, albo nie da się go otworzyć z innego powodu, na przykład gdy pod tą nazwą jest katalog. Dlatego komunikat brzmi `Cannot open`, a nie „pliku nie ma”. Nieudany odczyt znaczy, że plik jest otwarty, ale w miejscu wymaganej liczby jest coś innego albo nic.

## 3. Przygotuj projekt

Projekt z tej lekcji wygląda tak:

```text
lesson_12_1/
├── CMakeLists.txt
├── main.cpp
└── steps.txt
```

1. W `cpp-workspace` utwórz katalog `lesson_12_1` i skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program`.
2. `CMakeLists.txt` zostaw bez zmian. Wymienia tylko `main.cpp` i tak ma zostać.
3. Otwórz katalog w CLionie jak w lekcji 1.1: **File | Open**, potem **Trust Project** i profil **Debug**.
4. Zastąp zawartość `main.cpp` programem z punktu 2.
5. Utwórz plik `steps.txt` w katalogu `lesson_12_1`, obok `main.cpp` i `CMakeLists.txt`:
   - **W CLionie** (według dokumentacji CLion 2026.3): w oknie **Project** kliknij prawym przyciskiem myszy katalog `lesson_12_1` i wybierz **New | File**. Wpisz nazwę `steps.txt` i naciśnij **Enter**.
   - **W innym edytorze tekstu**, który zapisuje zwykły tekst: zapisz plik jako `steps.txt` w katalogu `lesson_12_1`.
6. Wpisz do `steps.txt` trzy liczby z punktu 1, każdą w osobnej linii, i zapisz plik. Po ostatniej liczbie możesz nacisnąć **Enter** albo nie: program odczyta dane tak samo (punkt 6, przypadek G).

**Nie dopisuj `steps.txt` do `add_executable`.** CMake opisuje, z jakich plików źródłowych zbudować program, a `steps.txt` nie jest kodem. Kompilator nigdy go nie czyta. Plik otwiera dopiero działający program, w chwili wykonania linijki ze `std::ifstream`.

Programu jeszcze nie uruchamiaj: najpierw ustal, gdzie będzie szukał pliku.

## 4. Katalog roboczy: gdzie program szuka pliku

`"steps.txt"` w programie to **ścieżka względna**: sama nazwa, bez katalogów. Z lekcji 0.1 wiesz, że ścieżka względna liczy się od bieżącego katalogu. Każdy uruchomiony program, nie tylko powłoka, ma własny bieżący katalog. Nazywa się go **katalogiem roboczym** (ang. *working directory*). To od tych słów pochodzi `pwd`: *print working directory*. Program szuka `steps.txt` właśnie w swoim katalogu roboczym.

Katalog roboczy **nie** jest automatycznie:

- katalogiem, w którym leży `main.cpp`;
- katalogiem z `CMakeLists.txt`;
- katalogiem, w którym leży program wykonywalny, na przykład `cmake-build-debug`;
- katalogiem `cpp-workspace` ani żadnym innym, który wydaje się „główny”.

Katalog roboczy to ustawienie **uruchomienia**, a nie kodu. Ten sam program wykonywalny, uruchomiony dwa razy z różnymi katalogami roboczymi, może raz znaleźć plik, a raz nie. Kod się nie zmienia.

**Katalog roboczy to też nie katalog budowania.** Katalog budowania, na przykład `cmake-build-debug`, to miejsce, w którym CMake i Ninja zapisują pliki obiektowe i program wykonywalny. Zmiana katalogu roboczego niczego nie buduje i nie przenosi programu. Zmienia tylko miejsce, od którego program liczy ścieżki względne.

**Sprawdź katalog roboczy w CLionie** (według dokumentacji CLion 2026.3, bez ręcznego sprawdzenia na każdym systemie):

1. Wybierz **Run | Edit Configurations**. Otworzy się okno **Run/Debug Configurations**.
2. Po lewej, w grupie **CMake Application**, wybierz konfigurację `first_program`.
3. Znajdź pole **Working directory** i przeczytaj jego wartość.
4. Według dokumentacji CLiona pole domyślnie wskazuje katalog projektu, tu `lesson_12_1`. Może to być pełna ścieżka kończąca się na `lesson_12_1` albo zapis `$ProjectFileDir$`, którym CLion oznacza katalog projektu. Wtedy niczego nie zmieniaj.
5. Jeśli pole jest puste albo wskazuje inny katalog, ustaw w nim katalog `lesson_12_1`, ten z `steps.txt`: kliknij ikonę katalogu na końcu pola i wskaż `lesson_12_1` albo wpisz jego pełną ścieżkę.
6. Zatwierdź **OK**. Zmiana dotyczy tylko tej konfiguracji, nie innych projektów.

Nie zakładaj, że CLion na każdym komputerze i w każdej wersji ustawia ten sam katalog. Zawsze przeczytaj pole.

**W terminalu** katalogiem roboczym programu jest bieżący katalog powłoki, z którego program uruchamiasz. Jeśli uruchamiasz program z katalogu `lesson_12_1`, poleceniem z lekcji 1.4, program szuka `steps.txt` właśnie w `lesson_12_1`. Terminal w tej lekcji jest nieobowiązkowy.

**Automatyczne sprawdzanie kursu a Twój komputer.** Gdy kurs sprawdza programy z tej lekcji automatycznie, sam tworzy plik z danymi, każdy w osobnym, pustym katalogu, i tam uruchamia program. Na Twoim komputerze nikt tego nie robi: plik musisz utworzyć samodzielnie i zadbać, żeby program uruchamiał się z katalogu, w którym ten plik leży.

## 5. Zbuduj i uruchom demonstrację

**W CLionie:** wybierz **Build | Build Project**, a potem kliknij **Run** (▶) przy konfiguracji `first_program`. Program nie czeka na dane z klawiatury: niczego nie wpisuj w oknie **Run**.

**W terminalu** (nieobowiązkowo): w katalogu `lesson_12_1` skonfiguruj i zbuduj projekt w katalogu `build-terminal`, tak jak w lekcji 11.1, punkt 5. Uruchom program z katalogu `lesson_12_1`: `.\build-terminal\first_program.exe` (macOS i Ubuntu: `./build-terminal/first_program`).

Dla pliku z punktu 1 program wypisuje:

<!-- output: steps -->
```text
Days: 2
Total steps: 11550
```

Program otworzył `steps.txt`, odczytał liczbę dni `2`, potem dwie liczby kroków i wypisał ich sumę: 4200 + 7350 = 11550.

## 6. Brak pliku, pusty plik i zero dni

Ten sam program, z tym samym `main.cpp`, daje różne wyniki dla różnych plików. **Przewidź** każdy wynik, zanim otworzysz zwinięty blok. Uruchamianie tych przypadków jest nieobowiązkowe: żeby je sprawdzić, zmieniasz tylko zawartość albo nazwę `steps.txt`, bez ponownego budowania.

**B: zero dni.** Plik zawiera jedną liczbę, `0`:

<!-- run: steps -->

<!-- datafile: steps steps.txt -->
```text
0
```

<details>
<summary>Standardowe wyjście dla B</summary>

<!-- output: steps -->
```text
Days: 0
Total steps: 0
```

To poprawny plik: mówi, że dni jest zero. Program odczytał liczbę `0`, pętla nie wykonała ani jednego przebiegu, a suma zostaje 0.

</details>

**C: brak pliku.** W katalogu roboczym nie ma pliku `steps.txt`.

<!-- run: steps -->

<details>
<summary>Standardowe wyjście dla C</summary>

<!-- output: steps -->
```text
Cannot open steps.txt
```

Otwarcie się nie udało, więc program niczego nie odczytuje. Nie wypisuje `Days: 0`, bo nie wie, ile dni zawiera plik, którego nie dostał.

</details>

**D: pusty plik.** `steps.txt` istnieje, ale nie ma w nim ani jednego znaku:

<!-- run: steps -->

<!-- datafile: steps steps.txt -->
```text
```

<details>
<summary>Standardowe wyjście dla D</summary>

<!-- output: steps -->
```text
Input error
```

Otwarcie się udało, bo plik istnieje. Nie udał się dopiero odczyt pierwszej wymaganej liczby: w pliku nie ma żadnej liczby.

</details>

**Trzy sytuacje, trzy różne wyniki:**

| Przypadek | Otwarcie | Odczyt liczby dni | Wynik |
|---|---|---|---|
| B: plik z `0` | udane | udany: `0` | raport: zero dni |
| C: brak pliku | nieudane | — | `Cannot open steps.txt` |
| D: pusty plik | udane | nieudany | `Input error` |

Pusty plik to nie to samo co plik z zerem. Plik z `0` zawiera informację: „dni było zero”. Pusty plik nie zawiera żadnej informacji, nawet tej. Gdyby program nie sprawdzał odczytu liczby dni, pusty plik dałby taki sam raport jak plik z `0`, a program przedstawiłby brak danych jako poprawny wynik.

**E: błąd w późniejszej liczbie.** Pierwsze dwie liczby są poprawne, a w miejscu trzeciej stoi słowo:

<!-- run: steps -->

<!-- datafile: steps steps.txt -->
```text
2
4200
seven
```

<details>
<summary>Standardowe wyjście dla E</summary>

<!-- output: steps -->
```text
Input error
```

`seven` nie jest liczbą, więc odczyt się nie udaje. Program zdążył już dodać 4200 do sumy, ale raportu nie wypisuje: przy pierwszym błędzie kończy pracę jednym komunikatem.

</details>

**F: niedozwolona liczba kroków.** Trzecia liczba się odczytuje, ale jest ujemna:

<!-- run: steps -->

<!-- datafile: steps steps.txt -->
```text
2
4200
-1
```

<details>
<summary>Standardowe wyjście dla F</summary>

<!-- output: steps -->
```text
Invalid steps
```

`-1` odczytuje się poprawnie, ale nie mieści się w zakresie od 0 do 20000. Tu też nie ma częściowego raportu.

</details>

**G: ostatnia liczba bez końca linii.** Plik zawiera te same liczby co w punkcie 1, ale po `7350` nie ma już znaku końca linii:

<!-- run: steps -->

<!-- datafile: steps steps.txt noeol -->
```text
2
4200
7350
```

<details>
<summary>Standardowe wyjście dla G</summary>

<!-- output: steps -->
```text
Days: 2
Total steps: 11550
```

Wynik jest taki sam jak w punkcie 5. Jak w lekcji 4.6, odczyt `>>` może się udać także wtedy, gdy zaraz po liczbie dane się kończą. O błędzie decyduje `fail()`, a nie to, czy po ostatniej liczbie był koniec linii. Takiego pliku nie musisz przygotowywać: ten przypadek sprawdzamy automatycznie.

</details>

<details>
<summary>Pozostałe przypadki kontrolne: otwórz po przewidywaniach</summary>

Wszystkie te przypadki są sprawdzane automatycznie. Wyniki wynikają z kontraktu z punktu 1.

**H: ujemna liczba dni.**

<!-- run: steps -->

<!-- datafile: steps steps.txt -->
```text
-1
```

<!-- output: steps -->
```text
Invalid steps
```

**I: sześć dni.** Program nie odczytuje żadnej liczby kroków, bo już liczba dni jest niedozwolona.

<!-- run: steps -->

<!-- datafile: steps steps.txt -->
```text
6
1000
2000
3000
4000
5000
6000
```

<!-- output: steps -->
```text
Invalid steps
```

**J: liczba kroków 20001,** o jeden za dużo.

<!-- run: steps -->

<!-- datafile: steps steps.txt -->
```text
2
4200
20001
```

<!-- output: steps -->
```text
Invalid steps
```

**K: słowo zamiast liczby dni.**

<!-- run: steps -->

<!-- datafile: steps steps.txt -->
```text
two
4200
7350
```

<!-- output: steps -->
```text
Input error
```

**L: brak ostatniej wymaganej liczby.** Plik zapowiada trzy dni, a zawiera tylko dwie liczby kroków.

<!-- run: steps -->

<!-- datafile: steps steps.txt -->
```text
3
4200
7350
```

<!-- output: steps -->
```text
Input error
```

**M: pięć dni.**

<!-- run: steps -->

<!-- datafile: steps steps.txt -->
```text
5
1000
2000
3000
4000
5000
```

<!-- output: steps -->
```text
Days: 5
Total steps: 15000
```

**N: największa możliwa suma,** pięć dni po 20000 kroków.

<!-- run: steps -->

<!-- datafile: steps steps.txt -->
```text
5
20000
20000
20000
20000
20000
```

<!-- output: steps -->
```text
Days: 5
Total steps: 100000
```

**O: obie granice zakresu kroków,** 0 i 20000.

<!-- run: steps -->

<!-- datafile: steps steps.txt -->
```text
2
0
20000
```

<!-- output: steps -->
```text
Days: 2
Total steps: 20000
```

**Czego ten program nie sprawdza.** Trzy kolejne przypadki pokazują granice odczytu przez `>>`. Program nie widzi linii pliku, tylko kolejne liczby:

**P: wszystkie liczby w jednej linii.** Raport jest taki sam jak w punkcie 5.

<!-- run: steps -->

<!-- datafile: steps steps.txt -->
```text
2 4200 7350
```

<!-- output: steps -->
```text
Days: 2
Total steps: 11550
```

**Q: puste linie między liczbami.** `>>` je pomija, więc raport znowu jest taki sam.

<!-- run: steps -->

<!-- datafile: steps steps.txt -->
```text
2

4200

7350
```

<!-- output: steps -->
```text
Days: 2
Total steps: 11550
```

**R: więcej liczb, niż zapowiada pierwsza.** Program odczytuje jedną liczbę kroków, a `7350` zostaje nieodczytane.

<!-- run: steps -->

<!-- datafile: steps steps.txt -->
```text
1
4200
7350
```

<!-- output: steps -->
```text
Days: 1
Total steps: 4200
```

</details>

## 7. Diagnostyka: program nie znajduje pliku

**Sytuacja.** Program jest poprawny, `steps.txt` istnieje i ma poprawne dane, a mimo to program wypisuje `Cannot open steps.txt`. Ten sam komunikat co w przypadku C, choć plik jest na dysku. To nie jest błąd kompilacji ani linkowania: program się buduje i uruchamia. Problem pojawia się dopiero podczas działania, przy otwieraniu pliku.

Odtwórz tę sytuację w projekcie `lesson_12_1`. Plików niczego nie zmieniaj:

1. Otwórz **Run | Edit Configurations** i konfigurację `first_program`, jak w punkcie 4.
2. W polu **Working directory** ustaw katalog `cmake-build-debug` z katalogu `lesson_12_1`, czyli ten, w którym leży program wykonywalny: kliknij ikonę katalogu na końcu pola i go wskaż. Jeśli Twój katalog budowania nazywa się trochę inaczej, wybierz ten, który masz. Zatwierdź **OK**.
3. **Przewidź**, co wypisze program. Potem kliknij **Run** (▶).

Program wypisuje `Cannot open steps.txt`. Teraz znajdź przyczynę tak, jakby nikt Ci jej nie podał:

1. Sprawdź nazwę pliku w kodzie i na dysku: `steps.txt` w obu miejscach, bez dodatkowego rozszerzenia, na przykład `steps.txt.txt`.
2. Sprawdź wielkość liter: `Steps.txt` to inna nazwa niż `steps.txt`. Na Ubuntu wielkość liter zawsze ma znaczenie, a na Windowsie i zwykle na macOS nie, dlatego taki błąd może ujawnić się dopiero na innym komputerze.
3. Sprawdź, jaki katalog roboczy ma konfiguracja: pole **Working directory**.
4. Sprawdź, czy `steps.txt` jest w tym katalogu.
5. Popraw konfigurację albo położenie pliku.
6. Uruchom ponownie ten sam program, bez zmian w `main.cpp`.

<details>
<summary>Co się dzieje i jak to naprawić: otwórz po wykonaniu kroków 1–4</summary>

- **Nazwa i wielkość liter są poprawne.** Program prosi o `steps.txt` i taki plik leży w `lesson_12_1`.
- **Katalog roboczy to `cmake-build-debug`.** Program szuka tam `steps.txt`, a pliku tam nie ma. Leży w `lesson_12_1`.
- **Naprawa:** w polu **Working directory** ustaw z powrotem katalog `lesson_12_1`, jak w punkcie 4, i uruchom program ponownie. Wypisze znowu raport z punktu 5. Nie zmieniasz `main.cpp` i nie budujesz programu od nowa: zmienia się tylko miejsce, w którym program szuka pliku.

Plik można by też skopiować do `cmake-build-debug`, ale to gorsza naprawa. Katalog budowania zawiera pliki wygenerowane przez narzędzia, a dane należą do projektu. Nie wpisuj też w programie ścieżki bezwzględnej, na przykład z nazwą swojego katalogu domowego: program działałby wtedy tylko na Twoim komputerze.

Ta sama przyczyna ma kilka postaci. Program nie znajduje pliku, gdy katalog roboczy wskazuje inne miejsce (to ćwiczenie), gdy plik zapisano w innym katalogu, na przykład w `cmake-build-debug`, i gdy plik ma inną nazwę, niż podaje program. W każdym z tych przypadków odpowiedź daje to samo pytanie: **jaki jest katalog roboczy i czy w nim leży plik o dokładnie tej nazwie?**

</details>

Zanim przejdziesz dalej, upewnij się, że **Working directory** wskazuje znowu `lesson_12_1`.

## 8. Misja: strony przeczytane podczas sesji

Po każdej sesji czytania zapisujesz, ile stron przeczytano. Program odczytuje te dane z pliku `pages.txt` i podaje liczbę sesji oraz łączną liczbę stron.

**Kontrakt pliku `pages.txt`:**

- pierwsza liczba to liczba sesji, od 0 do 5;
- po niej następuje dokładnie tyle liczb, ile sesji: strony przeczytane w kolejnych sesjach, każda liczba od 0 do 500;
- liczby są oddzielone spacjami albo przejściami do nowej linii;
- raport powstaje dopiero wtedy, gdy wszystkie wymagane liczby są odczytane i poprawne.

**Komunikaty:**

| Sytuacja | Standardowe wyjście |
|---|---|
| pliku nie udało się otworzyć | `Cannot open pages.txt` |
| plik jest otwarty, ale wymaganej liczby nie udało się odczytać | `Input error` |
| liczba jest odczytana, ale nie mieści się w swoim zakresie, także liczba sesji | `Invalid pages` |
| wszystkie wymagane liczby są odczytane i poprawne | `Sessions: N` i `Total pages: T` |

Program wypisuje tylko jeden z tych wyników i kończy się kodem 0, bez częściowego raportu i bez pytań. Największa możliwa suma to 5 · 500 = 2500.

W `cpp-workspace` utwórz katalog `reading_pages`, skopiuj do niego `CMakeLists.txt` z oryginalnego `lesson_05_first_program`, utwórz pusty `main.cpp` i plik `pages.txt`. Otwórz katalog w CLionie. Napisz program samodzielnie.

Musisz samodzielnie zdecydować:

1. jak nazwać zmienną strumienia plikowego;
2. gdzie sprawdzić, czy otwarcie się udało;
3. gdzie sprawdzić, czy odczyt liczby sesji się udał;
4. jak sprawdzić zakres liczby sesji;
5. jak odczytać kolejne liczby stron;
6. kiedy sprawdzać, czy odczyt każdej z nich się udał;
7. kiedy sprawdzać, czy mieści się w zakresie;
8. jak obliczyć sumę;
9. jak nie dopuścić do częściowego raportu;
10. jak ustawić katalog roboczy nowego projektu;
11. jak sprawdzić zachowanie programu, gdy pliku nie ma;
12. jak odróżnić pusty plik od poprawnego pliku z zerową liczbą sesji.

**Przypadki A–G.** Każdy przypadek to inna zawartość `pages.txt` albo brak pliku.

**A: trzy sesje.**

<!-- run: pages -->

<!-- datafile: pages pages.txt -->
```text
3
12
0
25
```

<!-- output: pages -->
```text
Sessions: 3
Total pages: 37
```

**B: zero sesji.**

<!-- run: pages -->

<!-- datafile: pages pages.txt -->
```text
0
```

<!-- output: pages -->
```text
Sessions: 0
Total pages: 0
```

**C: brak pliku.** W katalogu roboczym nie ma `pages.txt`.

<!-- run: pages -->

<!-- output: pages -->
```text
Cannot open pages.txt
```

**D: pusty plik.** `pages.txt` istnieje, ale jest pusty.

<!-- run: pages -->

<!-- datafile: pages pages.txt -->
```text
```

<!-- output: pages -->
```text
Input error
```

**E: niedozwolona liczba stron.**

<!-- run: pages -->

<!-- datafile: pages pages.txt -->
```text
2
15
-1
```

<!-- output: pages -->
```text
Invalid pages
```

**F: słowo zamiast liczby stron.**

<!-- run: pages -->

<!-- datafile: pages pages.txt -->
```text
2
15
seven
```

<!-- output: pages -->
```text
Input error
```

**G: niekompletne dane.** Plik zapowiada dwie sesje, a zawiera tylko jedną liczbę stron.

<!-- run: pages -->

<!-- datafile: pages pages.txt -->
```text
2
15
```

<!-- output: pages -->
```text
Input error
```

**Zanim napiszesz program**, przygotuj krótką tabelę: przypadki A–G i co najmniej jeden własny, na przykład z granicą zakresu, z oczekiwanym wynikiem ustalonym z kontraktu.

**Potem uruchom program dla A i dla D.** Między uruchomieniami zmieniasz tylko zawartość `pages.txt`, nie kod. Pozostałe przypadki prześledź na kartce, linijka po linijce swojego programu, i porównaj z wynikami podanymi wyżej. Jeśli masz czas, uruchom też C: najprościej tymczasowo zmienić nazwę pliku, na przykład na `pages_off.txt`, a potem przywrócić `pages.txt`. Wszystkie przypadki A–G są sprawdzane automatycznie w rozwiązaniu referencyjnym.

### Kryterium sukcesu

- Program buduje się jako C++20 i dla A oraz D wypisuje dokładnie pokazany wynik.
- Twoje przewidywania dla B, C, E, F i G zgadzają się z wynikami podanymi wyżej.
- Program sprawdza otwarcie pliku, zanim cokolwiek z niego odczyta.
- Każdy odczyt jest sprawdzony przez `fail()`, zanim program sprawdzi zakres tej wartości.
- Po pierwszym błędzie program wypisuje jeden komunikat i kończy pracę, bez częściowego raportu.
- `pages.txt` nie jest w `add_executable`, a `CMakeLists.txt` jest taki jak w lekcji 0.5.
- **Working directory** konfiguracji wskazuje katalog z `pages.txt`, a Ty umiesz powiedzieć, gdzie program szuka pliku i dlaczego.
- Umiesz wyjaśnić, dlaczego pusty plik daje inny wynik niż plik z `0`.

Gdy wynik się zgadza, możesz zapisać projekt w Gicie, jak w lekcji 1.5. Tym razem do commita należą trzy pliki: `main.cpp`, `CMakeLists.txt` i `pages.txt` z danymi A. Plik danych jest częścią projektu, bo bez niego program nie ma czego odczytać. Katalogu budowania nie dodawaj.

<details>
<summary>Podpowiedź 1: otwarcie pliku</summary>

Który nagłówek daje typ strumienia plikowego? Utwórz zmienną tego typu z nazwą pliku w nawiasach klamrowych, a zaraz potem, zanim odczytasz pierwszą liczbę, zapytaj ją o `fail()`. Co ma wtedy wypisać program i czy powinien działać dalej?

</details>

<details>
<summary>Podpowiedź 2: odczyt i sprawdzanie</summary>

Dla każdej wymaganej liczby kolejność jest ta sama co w punkcie 2: najpierw odczyt przez `>>`, potem `fail()`, dopiero potem zakres. Liczba sesji też jest wymaganą liczbą. Liczb stron odczytujesz tyle, ile zapowiada liczba sesji, w pętli z lekcji 10.3.

</details>

<details>
<summary>Podpowiedź 3: katalog roboczy i raport</summary>

`pages.txt` musi leżeć w katalogu roboczym konfiguracji, a nie obok programu wykonywalnego. Sprawdź pole **Working directory** nowego projektu tak samo jak w punkcie 4. Raport wypisz po pętli: do tego miejsca program dochodzi tylko wtedy, gdy żaden `return 0;` w pętli się nie wykonał.

</details>

Przykładowe rozwiązanie jest w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 9. Gdy coś pójdzie inaczej

| Co widzisz | Co to znaczy | Co zrobić |
|---|---|---|
| `Cannot open steps.txt`, choć plik istnieje | Plik nie leży w katalogu roboczym albo ma inną nazwę. | Wykonaj kroki z punktu 7: nazwa, wielkość liter, **Working directory**, położenie pliku. |
| W katalogu jest plik `steps.txt.txt` albo `steps.txt` nie ma rozszerzenia `.txt` | Edytor dopisał rozszerzenie albo plik zapisano pod inną nazwą. Windows domyślnie ukrywa znane rozszerzenia. | Sprawdź nazwę w terminalu poleceniem `ls` i zmień ją na dokładnie `steps.txt`. |
| `Input error` dla danych, które wyglądają poprawnie | Plik zapisano jako dokument, na przykład w formacie RTF, a nie jako zwykły tekst, albo w miejscu liczby jest litera, na przykład `O` zamiast `0`. | Utwórz plik w CLionie (**New \| File**) albo w edytorze, który zapisuje zwykły tekst, i wpisz dane jeszcze raz. |
| Raport z innymi liczbami, niż się spodziewasz | Program odczytuje inny plik `steps.txt` niż ten, który edytujesz, na przykład kopię w innym katalogu. | Sprawdź **Working directory** i otwórz plik właśnie z tego katalogu. |
| Program nic nie wypisuje i czeka | Uruchomiony program odczytuje z `std::cin` zamiast ze strumienia plikowego. | Sprawdź, czy wszystkie odczyty używają zmiennej strumienia plikowego, na przykład `input >> days;`. |

## 10. Wyjaśnij

Odpowiedz własnymi słowami, najlepiej na piśmie. Dopiero potem porównaj z przykładowymi odpowiedziami.

1. Do czego służy nagłówek `<fstream>` i co robi linijka `std::ifstream input{"steps.txt"};`?
2. Co oznacza nazwa `steps.txt` bez żadnego katalogu? Od którego katalogu program zaczyna jej szukać?
3. Skąd program wie, w którym katalogu szukać pliku, gdy uruchamiasz go w CLionie, a skąd, gdy uruchamiasz go z terminala?
4. Czym różni się `Cannot open steps.txt` od `Input error`? Podaj po jednej sytuacji, w której pojawia się każdy z nich.
5. Dlaczego pusty plik daje inny wynik niż plik zawierający `0`? Co by się stało, gdyby program nie sprawdzał odczytu liczby dni?
6. Program jest poprawny, plik też, a program wypisuje `Cannot open steps.txt`. Jak to możliwe? Co sprawdzisz najpierw?
7. Czy `steps.txt` należy do listy plików w `add_executable`? Co musisz zrobić po zmianie `steps.txt`, a co po zmianie `main.cpp`?
8. Czy brak znaku końca linii po ostatniej liczbie zawsze oznacza błąd odczytu?
9. Dlaczego zmiana katalogu roboczego nie jest tym samym co zmiana katalogu budowania?
10. Czego nie sprawdza program z tej lekcji? Podaj dwa pliki, dla których wypisze poprawny raport, choć nie wyglądają tak jak w punkcie 1.

<details>
<summary>Przykładowe odpowiedzi</summary>

1. `<fstream>` dołącza strumienie plikowe. Linijka tworzy zmienną `input` typu `std::ifstream`, czyli strumień wejściowy z pliku, i od razu próbuje otworzyć do odczytu plik `steps.txt`. Danych jeszcze nie odczytuje: robią to dopiero kolejne `input >> ...`.
2. To ścieżka względna: sama nazwa pliku. Program szuka go w swoim katalogu roboczym, czyli w bieżącym katalogu działającego programu.
3. W CLionie katalog roboczy ustala pole **Working directory** w konfiguracji uruchomienia. W terminalu jest nim bieżący katalog powłoki, z którego uruchamiasz program. Sam kod tego nie ustala.
4. `Cannot open steps.txt`: programowi nie udało się otworzyć pliku, na przykład pliku nie ma w katalogu roboczym. `Input error`: plik się otworzył, ale wymaganej liczby nie udało się odczytać, na przykład plik jest pusty albo w miejscu liczby stoi słowo `seven`.
5. Plik z `0` mówi, że dni było zero, więc raport `Days: 0` jest poprawny. Pusty plik nie mówi nic, więc odczyt liczby dni się nie udaje i program wypisuje `Input error`. Bez sprawdzenia odczytu `days` zostałoby 0 i program wypisałby dla pustego pliku taki sam raport jak dla pliku z `0`, czyli przedstawiłby brak danych jako wynik.
6. Program szuka pliku w swoim katalogu roboczym, a plik leży gdzie indziej albo ma trochę inną nazwę. Najpierw sprawdzam nazwę i wielkość liter, potem pole **Working directory** i to, czy plik leży właśnie w tym katalogu.
7. Nie. `add_executable` wymienia pliki źródłowe, które kompilator tłumaczy na program, a `steps.txt` to dane, które program odczytuje podczas działania. Po zmianie `steps.txt` wystarczy uruchomić program ponownie. Po zmianie `main.cpp` trzeba go zbudować ponownie, co w CLionie **Run** robi sam.
8. Nie. Jeśli ostatnia liczba jest kompletna, `>>` odczytuje ją poprawnie, także gdy zaraz po niej dane się kończą, a `fail()` daje `false`. Błąd pojawia się wtedy, gdy wymaganej liczby brakuje albo nie jest liczbą.
9. Katalog budowania to miejsce, w którym narzędzia zapisują zbudowany program. Katalog roboczy to miejsce, od którego działający program liczy ścieżki względne. Zmiana katalogu roboczego nie przenosi i nie buduje programu, a program wykonywalny może leżeć w innym katalogu niż ten, w którym szuka danych.
10. Program nie sprawdza linii pliku ani danych po wymaganych liczbach. Poprawny raport wypisze na przykład dla `2 4200 7350` w jednej linii, dla pliku z pustymi liniami między liczbami i dla pliku, w którym po wymaganych liczbach jest jeszcze jedna liczba albo słowo.

</details>

## Podsumowanie

- Dane, które program ma odczytywać przy każdym uruchomieniu, mogą leżeć w zwykłym pliku tekstowym. Plik danych nie jest plikiem źródłowym i nie trafia do `add_executable`.
- `#include <fstream>` daje strumienie plikowe. `std::ifstream input{"steps.txt"};` tworzy strumień i próbuje otworzyć plik do odczytu.
- Z pliku odczytujesz tak samo jak z klawiatury: przez `>>`. Powodzenie otwarcia i każdego odczytu sprawdzasz przez `fail()`.
- Kolejność sprawdzeń: otwarcie, odczyt wartości, jej zakres, dopiero potem następna wartość. Raport powstaje po odczytaniu wszystkich wymaganych wartości.
- Brak pliku (`Cannot open`), pusty plik (`Input error`) i plik z zerem (raport) to trzy różne sytuacje.
- Ścieżka względna liczy się od katalogu roboczego programu. W CLionie ustala go pole **Working directory**, a w terminalu bieżący katalog powłoki. Nie jest nim automatycznie katalog `main.cpp` ani katalog programu wykonywalnego.
- Gdy poprawny program nie znajduje poprawnego pliku, sprawdzasz nazwę, wielkość liter, katalog roboczy i położenie pliku, a nie kod.

## Co dalej

Program z tej lekcji odczytuje z pliku same liczby. Kolejne lekcje Modułu 12 są w przygotowaniu.

---

## Przykładowe rozwiązania

Zajrzyj tutaj **po własnej próbie**. Twoje nazwy zmiennych mogą się różnić, jeśli standardowe wyjście jest takie, jak wymagane.

<details>
<summary>Punkt 8: misja, strony przeczytane podczas sesji</summary>

**`main.cpp`**:

<!-- example: pages -->
```cpp
#include <fstream>
#include <iostream>

int main() {
    std::ifstream reading_log{"pages.txt"};

    if (reading_log.fail()) {
        std::cout << "Cannot open pages.txt\n";
        return 0;
    }

    int sessions{0};
    reading_log >> sessions;

    if (reading_log.fail()) {
        std::cout << "Input error\n";
        return 0;
    }

    if (sessions < 0 || sessions > 5) {
        std::cout << "Invalid pages\n";
        return 0;
    }

    int total_pages{0};

    for (int session{0}; session < sessions; ++session) {
        int pages{0};
        reading_log >> pages;

        if (reading_log.fail()) {
            std::cout << "Input error\n";
            return 0;
        }

        if (pages < 0 || pages > 500) {
            std::cout << "Invalid pages\n";
            return 0;
        }

        total_pages += pages;
    }

    std::cout << "Sessions: " << sessions << "\n";
    std::cout << "Total pages: " << total_pages << "\n";
}
```

**`CMakeLists.txt`**: taki jak w oryginalnym `lesson_05_first_program`, bez zmian. `pages.txt` nie jest w `add_executable`.

**`pages.txt`** z danymi A, w katalogu `reading_pages`, obok `main.cpp` i `CMakeLists.txt`:

<!-- run: pages -->

<!-- datafile: pages pages.txt -->
```text
3
12
0
25
```

<!-- output: pages -->
```text
Sessions: 3
Total pages: 37
```

- **Konfiguracja uruchomienia:** pole **Working directory** konfiguracji `first_program` wskazuje katalog `reading_pages`, ten z `pages.txt`. W terminalu program uruchamiasz z katalogu `reading_pages`.
- **Kolejność sprawdzeń:** najpierw `reading_log.fail()` zaraz po otwarciu, potem dla liczby sesji i każdej liczby stron: odczyt, `fail()`, zakres. Każdy błąd kończy `main` przez `return 0;`, więc raport po pętli wypisuje się tylko dla kompletnych, poprawnych danych.
- **Pusty plik a zero sesji:** dla pustego pliku odczyt liczby sesji się nie udaje (`Input error`). Dla pliku z `0` odczyt się udaje, pętla nie wykonuje żadnego przebiegu, a raport podaje zero sesji i zero stron.
- **Inne poprawne rozwiązania:** inna nazwa strumienia, na przykład `input` albo `pages_file`; zakresy zapisane jako stałe `const int`; pętla `while` z licznikiem zamiast `for`.

| Przypadek | Plik `pages.txt` | Standardowe wyjście |
|---|---|---|
| A | `3`, `12`, `0`, `25` | `Sessions: 3`, `Total pages: 37` |
| B | `0` | `Sessions: 0`, `Total pages: 0` |
| C | brak pliku | `Cannot open pages.txt` |
| D | pusty plik | `Input error` |
| E | `2`, `15`, `-1` | `Invalid pages` |
| F | `2`, `15`, `seven` | `Input error` |
| G | `2`, `15` | `Input error` |

Pozostałe przypadki kontrolne, sprawdzane automatycznie:

**H: jedna sesja.**

<!-- run: pages -->

<!-- datafile: pages pages.txt -->
```text
1
40
```

<!-- output: pages -->
```text
Sessions: 1
Total pages: 40
```

**I: pięć sesji.**

<!-- run: pages -->

<!-- datafile: pages pages.txt -->
```text
5
10
20
30
40
50
```

<!-- output: pages -->
```text
Sessions: 5
Total pages: 150
```

**J: 500 stron w jednej sesji,** górna granica.

<!-- run: pages -->

<!-- datafile: pages pages.txt -->
```text
1
500
```

<!-- output: pages -->
```text
Sessions: 1
Total pages: 500
```

**K: 501 stron,** o jedną za dużo.

<!-- run: pages -->

<!-- datafile: pages pages.txt -->
```text
1
501
```

<!-- output: pages -->
```text
Invalid pages
```

**L: ujemna liczba sesji.**

<!-- run: pages -->

<!-- datafile: pages pages.txt -->
```text
-2
```

<!-- output: pages -->
```text
Invalid pages
```

**M: dane A bez końca linii po ostatniej liczbie.**

<!-- run: pages -->

<!-- datafile: pages pages.txt noeol -->
```text
3
12
0
25
```

<!-- output: pages -->
```text
Sessions: 3
Total pages: 37
```

**N: największa możliwa suma,** pięć sesji po 500 stron.

<!-- run: pages -->

<!-- datafile: pages pages.txt -->
```text
5
500
500
500
500
500
```

<!-- output: pages -->
```text
Sessions: 5
Total pages: 2500
```

**O: sześć sesji.**

<!-- run: pages -->

<!-- datafile: pages pages.txt -->
```text
6
10
10
10
10
10
10
```

<!-- output: pages -->
```text
Invalid pages
```

</details>

**Poprzednia lekcja:** [Lekcja 11.5: Samodzielny program wieloplikowy (sprawdzian Modułu 11)](../module_11_multifile_programs/lesson_05_multifile_checkpoint.md) · **Następna lekcja:** w przygotowaniu · [Opis kursu](../../README.md)

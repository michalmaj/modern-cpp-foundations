# Lekcja 7.4: Przetwarzanie kolejnych linii przez `std::getline`

**Polski** · [English](lesson_04_successive_lines.en.md) · [Opis kursu](../../README.md)

> **Moduł 7, lekcja 4** · około 70–85 minut
> **Potrzebujesz:** katalogu `cpp-workspace` i oryginalnego projektu `lesson_05_first_program`, jak dotąd. Przyda się też Twój projekt `initials` z lekcji 7.3. Debugger nie jest w tej lekcji potrzebny.
> **Wersja pilotażowa.** Programy z tej lekcji sprawdzamy automatycznie na Windowsie, Ubuntu i macOS, także z podanymi danymi wejściowymi. Wpisywanie danych w oknie **Run** CLiona opisujemy bez ręcznego sprawdzenia na każdym systemie.

## Zanim zaczniesz

Ta lekcja zakłada, że:

- odczytujesz całą linię tekstu przez `std::getline` (lekcja 2.7);
- sprawdzasz przez `std::cin.fail()`, czy odczyt się udał, i kończysz pętlę `while` za pomocą flagi `bool` (lekcja 4.5);
- pamiętasz zasadę „najpierw sukces, potem koniec danych” (lekcja 4.6);
- przechowujesz rozmiary w typie `std::size_t` (lekcja 6.3);
- piszesz funkcję, która dostaje tekst przez `const std::string&` i zwraca jego inicjały jako nowy `std::string` (lekcja 7.3).

## Sytuacja

W lekcji 7.3 tekst był wpisany w kodzie, a funkcja wyznaczała jego inicjały:

<!-- fragment -->
```cpp
const std::string name{"Ada Lovelace"};
```

A co, jeśli teksty podaje użytkownik podczas działania programu i nie wiadomo z góry, ile ich będzie? Osobna zmienna i osobne wywołanie funkcji dla każdego tekstu nie wchodzą w grę. Potrzebna jest pętla, która powtarza cztery kroki:

1. odczytaj jedną linię;
2. sprawdź, czy to już koniec;
3. jeśli nie, przeanalizuj linię i wypisz wynik;
4. wróć do odczytu następnej linii.

Wcześniejszych linii nie trzeba przechowywać: wynik każdej linii jest gotowy zaraz po jej odczycie, a do podsumowania wystarczą dwa liczniki. Wszystkie potrzebne operacje już znasz. Nowe jest ich połączenie.

Po tej lekcji będziesz:

- odczytywać kolejne linie w pętli `while` sterowanej flagą `bool`;
- odróżniać pustą linię od nieudanego odczytu, także przy ostatniej linii danych;
- łączyć pętlę odczytu z funkcją tekstową i liczyć przetworzone linie i znaki.

## 1. Przygotuj projekt

W `cpp-workspace` utwórz katalog `lesson_7_4` i skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program`. Programy z punktów 2 i 4 wpisujesz w `main.cpp` tego katalogu.

Programy z tej lekcji nie wypisują pytań. Po uruchomieniu od razu wpisuj dane i każdą linię kończ klawiszem **Enter**. Pusta linia to samo naciśnięcie **Enter**, bez żadnego znaku.

## 2. Jedna linia: przypomnienie `std::getline`

Program odczytuje jedną linię i wypisuje ją w nawiasach kwadratowych razem z liczbą jej znaków:

<!-- example: one_line -->
```cpp
#include <iostream>
#include <string>

int main() {
    std::string line{};
    std::getline(std::cin, line);

    if (std::cin.fail()) {
        std::cout << "Input could not be read\n";
    } else {
        std::cout << "Line: [" << line << "]\n";
        std::cout << "Characters: " << line.size() << "\n";
    }
}
```

Uruchom program, wpisz `Ada Lovelace` i naciśnij **Enter**:

<!-- input: one_line -->
```text
Ada Lovelace
```

**Przewidź:** czy spacja zostanie w tekście? Ile znaków wypisze program?

<details>
<summary>Standardowe wyjście</summary>

<!-- output: one_line -->
```text
Line: [Ada Lovelace]
Characters: 12
```

</details>

`std::getline` odczytuje **całą linię** razem ze spacjami, a nie jedno słowo, jak `>>` (lekcja 2.7). Odczyt kończy się na **znaku końca linii**, który powstaje po naciśnięciu **Enter**. To ten sam znak, który program wypisuje przez `"\n"`. `getline` zabiera go z wejścia, ale **nie dopisuje** go do tekstu. Dlatego `Ada Lovelace` ma 12 znaków: 11 liter i jedną spację.

**Dlaczego tylko `getline`.** Po odczycie przez `>>` w wejściu zostaje znak końca linii, a `getline` wywołane zaraz potem odczytałoby go jako pustą linię (lekcja 2.7). W tej lekcji pusta linia oznacza koniec pracy, więc taki znak zakończyłby odczyt przed pierwszym tekstem. Dlatego programy z tej lekcji czytają dane wyłącznie przez `std::getline`. Jak łączyć oba rodzaje odczytu, poznasz później.

## 3. Pusta linia a nieudany odczyt

Uruchom program z punktu 2 jeszcze raz i od razu naciśnij **Enter**, nie wpisując żadnego znaku. **Przewidź:** czy odczyt się uda?

<!-- input: one_line -->
```text

```

<details>
<summary>Standardowe wyjście</summary>

<!-- output: one_line -->
```text
Line: []
Characters: 0
```

</details>

To najważniejsze rozróżnienie tej lekcji:

- **Pusta linia to udany odczyt.** W wejściu był sam znak końca linii. Tekst jest pusty: `line.size()` daje 0, a `line.empty()` daje `true`. Program nie wybrał gałęzi `fail()`.
- **Nieudany odczyt** oznacza, że `getline` nie dostarczyło żadnej linii, bo w wejściu nie było już ani znaków, ani znaku końca linii. Zwykle to koniec danych. `std::cin.fail()` daje wtedy `true`.

Odczyt może się nie udać także z rzadszych powodów, na przykład przy błędzie wejścia. `fail()` nie mówi, która przyczyna wystąpiła (lekcja 4.5), a tutaj nie musimy ich rozróżniać: każdy nieudany odczyt kończy przetwarzanie.

| Sytuacja | Co czeka w wejściu | `std::cin.fail()` | `line` po odczycie | Decyzja programu |
|---|---|---|---|---|
| zwykła linia | znaki i znak końca linii | `false` | tekst bez znaku końca linii | przetworzyć |
| pusta linia | sam znak końca linii | `false` | pusty tekst, `empty()` daje `true` | zakończyć |
| brak danych | nic | `true` | nie wolno polegać na zawartości | zakończyć |

Kolejność sprawdzeń po każdym odczycie:

1. Czy odczyt się udał? Jeśli nie, przetwarzanie się kończy.
2. Czy linia jest pusta? Jeśli tak, przetwarzanie się kończy.
3. Dopiero niepusta, poprawnie odczytana linia trafia do analizy.

To zasada z lekcji 4.5: po nieudanym odczycie żadna decyzja nie opiera się na zawartości zmiennej. Pusta linia znaczy „to już wszystko” tylko wtedy, gdy odczyt się udał. Brak danych prześledzisz na papierze w punkcie 5.

## 4. Wiele linii: pętla z flagą

Program odczytuje kolejne linie, aż trafi na pustą linię albo odczyt się nie uda, i liczy przetworzone linie oraz ich znaki:

<!-- example: line_counter -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>

int main() {
    bool reading{true};
    std::size_t line_count{0};
    std::size_t character_count{0};

    while (reading) {
        std::string line{};
        std::getline(std::cin, line);

        if (std::cin.fail()) {
            reading = false;
        } else if (line.empty()) {
            reading = false;
        } else {
            ++line_count;
            character_count += line.size();
        }
    }

    std::cout << "Lines: " << line_count << "\n";
    std::cout << "Characters: " << character_count << "\n";
}
```

Uruchom program i wpisz `Ada`, `Bob`, a potem pustą linię:

<!-- input: line_counter -->
```text
Ada
Bob

```

**Przewidź** obie liczby. Czy pusta linia na końcu zostanie policzona?

<details>
<summary>Standardowe wyjście</summary>

<!-- output: line_counter -->
```text
Lines: 2
Characters: 6
```

</details>

- **Flaga `reading`** zaczyna od `true`, a warunek pętli to sama flaga, jak wartość `bool` w warunku `if` w lekcji 3.2. Program ustawia ją na `false` po nieudanym odczycie i po pustej linii.
- **Jeden odczyt na przebieg**, a po nim jedna decyzja: zakończyć albo przetworzyć.
- **`line` powstaje w każdym przebiegu od nowa**, więc nie zostaje w niej nic z poprzedniej linii.
- **Liczniki rosną tylko w ostatniej gałęzi**, czyli dla linii, która naprawdę trafiła do analizy. Do `character_count` trafia `line.size()`: liczą się spacje, ale nie znaki końca linii. Oba liczniki mają typ `std::size_t`, jak rozmiary w lekcji 6.3.

**Dlaczego jedna flaga?** W lekcji 4.5 pętla miała dwie flagi, bo po pętli program musiał wiedzieć, co ją zakończyło. Tutaj podsumowanie jest takie samo dla obu przyczyn, więc wystarczy flaga, która mówi tylko, czy czytać dalej.

| Próba | Odczytana linia | `fail()` | `empty()` | Decyzja | `reading` po próbie | `line_count` | `character_count` |
|---|---|---|---|---|---|---|---|
| 1 | `Ada` | `false` | `false` | przetworzyć | `true` | 1 | 3 |
| 2 | `Bob` | `false` | `false` | przetworzyć | `true` | 2 | 6 |
| 3 | pusta | `false` | `true` | zakończyć | `false` | 2 | 6 |

## 5. Koniec danych i ostatnia linia

Końca danych nie musisz wywoływać samodzielnie: przyjmij, że po ostatniej podanej linii wejście się kończy, i prześledź program na papierze. **Przewidź:** jak zmieni się tabela z punktu 4, gdy zaraz po linii `Bob` dane się skończą, bez pustej linii?

<details>
<summary>Odpowiedź i standardowe wyjście</summary>

Próby 1 i 2 przebiegają tak samo. W próbie 3 `getline` nie dostarcza żadnej linii: `fail()` daje `true`, a program ustawia `reading` na `false` i nie sprawdza już `empty()`. Liczniki się nie zmieniają, więc podsumowanie jest takie samo jak po pustej linii. Ten przypadek sprawdzają automatyczne testy kursu na Windowsie, Ubuntu i macOS:

<!-- input: line_counter -->
```text
Ada
Bob
```

<!-- output: line_counter -->
```text
Lines: 2
Characters: 6
```

</details>

**Ostatnia linia bez znaku końca linii.** Dane mogą się też skończyć zaraz po ostatnim znaku linii, na przykład w pliku tekstowym. Prześledź dane: `Ada`, znak końca linii, `Bob` i nic więcej:

| Próba | Co dostarcza `getline` | `fail()` | Decyzja | `line_count` | `character_count` |
|---|---|---|---|---|---|
| 1 | `Ada` | `false` | przetworzyć | 1 | 3 |
| 2 | `Bob`, a zaraz po nim dane się kończą | `false` | przetworzyć | 2 | 6 |
| 3 | nic | `true` | zakończyć | 2 | 6 |

W próbie 2 strumień doszedł do końca danych, a mimo to odczyt **się udał**: `fail()` daje `false`, a `line` zawiera `Bob`. To sytuacja z lekcji 4.6, gdzie ostatnia liczba bez końca linii była odczytana poprawnie, choć `eof()` dawało już `true`. Program przetwarza więc `Bob` jak każdą inną linię, a pętlę kończy dopiero następna, nieudana próba. Program, który kończyłby pracę, gdy tylko `eof()` da `true`, zgubiłby `Bob`. Testy automatyczne kursu tego przypadku nie uruchamiają, bo w nich każda linia kończy się znakiem końca linii.

**Po nieudanym odczycie nie korzystaj z `line`.** Gdyby `line` powstawała przed pętlą, po próbie 3 mogłaby nadal zawierać `Bob`, a program, który nie sprawdza najpierw `fail()`, mógłby przetworzyć tę linię drugi raz. W programie z punktu 4 tak się nie stanie.

## 6. Pusta linia to nie to samo co spacje

| Tekst | `size()` | `empty()` | W tej lekcji |
|---|---|---|---|
| `""`, pusta linia | 0 | `true` | kończy odczyt |
| `" "`, jedna spacja | 1 | `false` | zwykła linia danych |
| `"   "`, trzy spacje | 3 | `false` | zwykła linia danych |

**Tylko linia o długości zero kończy odczyt.** Linia z jednej albo kilku spacji nie jest pusta: ma znaki, tylko żaden z nich nie jest literą. Program nie usuwa z niej spacji i nie traktuje jej jak pustej.

Uruchom program z punktu 4, wpisz trzy spacje i naciśnij **Enter**, a potem naciśnij **Enter** jeszcze raz:

<!-- input: line_counter -->
```text
   

```

**Przewidź** wynik.

<details>
<summary>Standardowe wyjście</summary>

<!-- output: line_counter -->
```text
Lines: 1
Characters: 3
```

</details>

Pierwsza linia nie jest pusta, więc została przetworzona i policzona, razem z trzema spacjami. Dopiero druga, naprawdę pusta linia zakończyła pętlę.

## 7. Misja: dziennik krótkich tekstów

Program dostaje kolejne linie z krótkimi tekstami, na przykład z imionami i nazwiskami. Każdą linię numeruje, wypisuje i podaje jej inicjały, a na końcu wypisuje podsumowanie.

**Jakie dane są możliwe.** Takie jak w lekcji 7.3: litery `A`–`Z` i `a`–`z` oraz zwykłe spacje, bez cyfr, tabulatorów, interpunkcji i polskich liter. Spacji może być kilka, mogą stać na początku i na końcu linii, a linia może składać się z samych spacji. Tych założeń nie musisz sprawdzać.

**Reguły:**

- Program przetwarza kolejne linie, aż odczyta pustą linię albo odczyt się nie uda. Pusta linia nie jest raportowana, a tego, co stoi po niej, program już nie odczytuje.
- Dla każdej przetworzonej linii wypisuje `Line N: [TEKST]` i `Initials N: [WYNIK]`: numer od 1, oryginalną linię ze wszystkimi spacjami i jej inicjały, jak w lekcji 7.3.
- Na końcu wypisuje `Lines processed: N` i `Characters processed: N`. Liczba znaków to suma `size()` przetworzonych linii: ze spacjami, ale bez znaków końca linii i bez inicjałów.
- Podsumowanie nie zależy od tego, co zakończyło odczyt. Program nie wypisuje pytań ani komunikatu o zakończeniu.

**Wymagania:**

- Co najmniej jedna własna funkcja dostaje tekst przez `const std::string&` i zwraca jego inicjały jako nowy `std::string`, niczego nie odczytując ani nie wypisując. Możesz ją skopiować z projektu `initials` z lekcji 7.3.
- `main` odczytuje linie przez `std::getline` w pętli `while` sterowanej flagą `bool` i odpowiada za całe wypisywanie.
- Program nie przechowuje wcześniejszych linii.

W `cpp-workspace` utwórz katalog `texts_log`, skopiuj do niego `CMakeLists.txt` z oryginalnego `lesson_05_first_program`, utwórz pusty `main.cpp` i napisz program samodzielnie.

Dla takiego wejścia:

<!-- input: texts_log -->
```text
Ada Lovelace
Mary ann SMITH

Ignored line
```

standardowe wyjście ma być takie:

<!-- output: texts_log -->
```text
Line 1: [Ada Lovelace]
Initials 1: [AL]
Line 2: [Mary ann SMITH]
Initials 2: [MaS]
Lines processed: 2
Characters processed: 26
```

`Ada Lovelace` ma 12 znaków, a `Mary ann SMITH` 14, razem 26. `Ignored line` stoi po pustej linii, więc program jej nie odczytuje. Gdy wpisujesz dane samodzielnie, program kończy się zaraz po pustej linii.

Gdy pierwsza linia jest pusta, program nie przetwarza żadnej linii. To pusta linia, a nie brak danych:

<!-- input: texts_log -->
```text

```

<!-- output: texts_log -->
```text
Lines processed: 0
Characters processed: 0
```

Linia z trzech spacji nie jest pusta, więc program ją przetwarza. Nie ma w niej wyrazów, więc jej inicjały są puste:

<!-- input: texts_log -->
```text
   

```

<!-- output: texts_log -->
```text
Line 1: [   ]
Initials 1: []
Lines processed: 1
Characters processed: 3
```

**Funkcja inicjałów nie jest tu nowym zadaniem:** powstała w lekcji 7.3. Nowe jest sterowanie odczytem i połączenie wszystkiego w jeden program. Musisz samodzielnie zdecydować:

1. gdzie utworzyć zmienną z bieżącą linią;
2. kiedy sprawdzić `std::cin.fail()`, a kiedy `line.empty()`;
3. kiedy zwiększyć licznik linii i jak numerować nim raport;
4. kiedy wywołać funkcję inicjałów;
5. jak wypisać linię, żeby spacje pozostały widoczne;
6. jak policzyć znaki przez `size()`;
7. jak oddzielić raport linii od podsumowania;
8. dlaczego funkcja inicjałów nie powinna sama wywoływać `getline`.

**Zanim napiszesz program**, przygotuj tabelę przypadków z oczekiwanym standardowym wyjściem, między innymi: pusta linia jako pierwsza, jedna linia, dane zakończone bez pustej linii, same spacje, spacje na początku i na końcu, pusta linia między dwoma tekstami i różna wielkość liter.

**Potem** uruchom program dla danych z przykładu, bez `Ignored line`, i dla 2–3 przypadków z tabeli, na przykład `Ada`, trzy spacje albo `  Ada  `, każdy zakończony pustą linią. W terminalu wpisywane linie mieszają się z raportem, bo program odpowiada zaraz po każdej linii. Przypadki zakończone końcem danych prześledź na papierze. Wszystkie przypadki z pełnej listy kontrolnej są sprawdzone automatycznie.

### Kryterium sukcesu

- Program buduje się jako C++20 i dla danych z przykładu wypisuje dokładnie sześć linii pokazanych wyżej.
- Powodzenie odczytu jest sprawdzane przed `line.empty()`, a funkcja inicjałów niczego nie odczytuje ani nie wypisuje.
- Pusta linia nie trafia ani do raportu, ani do liczników, a linia z samych spacji jest przetwarzana.
- Ostatnia linia przed końcem danych jest przetworzona dokładnie raz.
- Podsumowanie pojawia się po pętli i jest takie samo dla obu sposobów zakończenia.
- Tabela przypadków powstała przed uruchomieniem programu.
- Umiesz wyjaśnić, dlaczego program nie potrzebuje wektora wszystkich linii.

Gdy wynik się zgadza, możesz zapisać projekt w Gicie, jak w lekcji 1.5.

<details>
<summary>Podpowiedź 1</summary>

Jakie trzy decyzje trzeba podjąć po każdej próbie odczytu jednej linii: czy odczyt się powiódł, czy tekst jest pusty, czy należy go przetworzyć?

</details>

<details>
<summary>Podpowiedź 2</summary>

Licznik przetworzonych linii powinien rosnąć tylko dla linii, która rzeczywiście trafiła do analizy. Pusta linia kończąca nie jest rekordem.

</details>

<details>
<summary>Podpowiedź 3</summary>

Dla każdej niepustej linii wywołaj znaną funkcję wyznaczającą inicjały, wypisz dwa wiersze raportu i dodaj `line.size()` do łącznej liczby znaków. Podsumowanie wypisz dopiero po zakończeniu pętli.

</details>

<details>
<summary>Pełna lista przypadków kontrolnych: otwórz po przygotowaniu własnej tabeli</summary>

| | Wejście | Inicjały | Linie | Znaki | Co sprawdza |
|---|---|---|---|---|---|
| A | `Ada Lovelace`, `Mary ann SMITH`, pusta linia, `Ignored line` | `AL`, `MaS` | 2 | 26 | dane z przykładu; po pustej linii nic nie jest odczytywane |
| B | pusta linia | brak | 0 | 0 | pusta linia jako pierwsza |
| C | `Ada`, pusta linia | `A` | 1 | 3 | jedna linia |
| D | `Ada Lovelace`, `Mary ann SMITH`, koniec danych | `AL`, `MaS` | 2 | 26 | koniec danych zamiast pustej linii: ten sam raport co w A |
| E | trzy spacje, pusta linia | pusty wynik | 1 | 3 | same spacje to dane |
| F | `  Ada  `, pusta linia | `A` | 1 | 7 | spacje na początku i na końcu |
| G | `A  B   C`, pusta linia | `ABC` | 1 | 8 | kilka spacji między wyrazami |
| H | `A`, pusta linia | `A` | 1 | 1 | jedna litera |
| I | `Bo`, `Grace Hopper`, `Alan Mathison Turing`, pusta linia | `B`, `GH`, `AMT` | 3 | 34 | linie o różnych długościach |
| J | `Grace Hopper`, pusta linia, `Ada Lovelace` | `GH` | 1 | 12 | tekst po pustej linii nie jest przetwarzany |
| K | `Al`, `Bo`, `Cy`, `Di`, `Ed`, koniec danych | `A`, `B`, `C`, `D`, `E` | 5 | 10 | numeracja do 5; ostatnia linia przed końcem danych |
| L | `ada lovelace`, `ADA LOVELACE`, `ada Lovelace`, pusta linia | `al`, `AL`, `aL` | 3 | 36 | wielkość liter w inicjałach |

**Testy automatyczne i Twoje próby.** Wszystkie przypadki są sprawdzone automatycznie. Rozwiązanie referencyjne samo odczytuje dane z wejścia, więc nie potrzebuje osobnego programu kontrolnego. Przypadki A, B i E są pokazane wyżej, a pozostałe w części [Przykładowe rozwiązania](#przykładowe-rozwiązania). W przypadkach D i K dane kończą się po ostatniej podanej linii. Pusta linia w przypadku B to jeden znak końca linii, a nie brak danych. Ostatniej linii bez znaku końca linii (punkt 5) testy nie uruchamiają.

</details>

Przykładowe rozwiązanie jest w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 8. Znajdź błąd: pusta linia w liczniku

To zadanie wykonaj **po misji**: program poniżej zawiera prawie całe rozwiązanie. Poprawnie raportuje kolejne linie, ale jego podsumowanie nie zawsze się zgadza. Tak jak program z misji, nie wypisuje pytań.

<details>
<summary>Program do sprawdzenia: otwórz po napisaniu własnego programu</summary>

<!-- example: texts_log_count_bug -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>

std::string initials_of(const std::string& text) {
    std::string result{};

    for (std::size_t index{0}; index < text.size(); ++index) {
        const bool word_can_start{index == 0 || text[index - 1] == ' '};

        if (text[index] != ' ' && word_can_start) {
            result.push_back(text[index]);
        }
    }

    return result;
}

int main() {
    bool reading{true};
    std::size_t lines_processed{0};
    std::size_t characters_processed{0};

    while (reading) {
        std::string line{};
        std::getline(std::cin, line);

        if (std::cin.fail()) {
            reading = false;
        } else {
            ++lines_processed;

            if (line.empty()) {
                reading = false;
            } else {
                characters_processed += line.size();

                const std::string initials{initials_of(line)};

                std::cout << "Line " << lines_processed << ": [" << line << "]\n";
                std::cout << "Initials " << lines_processed << ": [" << initials << "]\n";
            }
        }
    }

    std::cout << "Lines processed: " << lines_processed << "\n";
    std::cout << "Characters processed: " << characters_processed << "\n";
}
```

1. **Przewidź** wynik dla dwóch zestawów: (a) `Ada Lovelace` i `Mary ann SMITH`, po których kończą się dane; (b) `Ada` i pusta linia.
2. Zestaw (a) kończy się końcem danych, więc prześledź go na papierze i porównaj z wynikiem w części Przykładowe rozwiązania. Czy podsumowanie jest poprawne?
3. Uruchom program dla zestawu (b). Ile linii podaje podsumowanie, a ile raportów `Line N` wypisał program?
4. Wskaż miejsce, w którym program zwiększa licznik. Dla których odczytów to się dzieje?
5. Popraw kolejność: licznik ma rosnąć dopiero wtedy, gdy wiadomo, że linia nie jest pusta.
6. Uruchom poprawiony program dla zestawu (b) i dla pustej linii jako pierwszej.
7. Prześledź poprawiony program dla zestawu (a), czyli dla zakończenia przez koniec danych. Czy wynik się zmienił?

</details>

Wyniki programu przed poprawką i poprawiony program są w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 9. Gdy coś pójdzie inaczej

| Co widzisz | Co to znaczy | Co zrobić |
|---|---|---|
| W podsumowaniu jest o jedną linię za dużo | Licznik rośnie, zanim program sprawdzi, czy linia jest pusta (punkt 8). | Zwiększaj licznik tylko w gałęzi, która przetwarza linię. |
| Program wypisuje `Line N: []` dla pustej linii kończącej | Linia jest przetwarzana, zanim program sprawdzi, czy jest pusta. | Najpierw sprawdź `fail()`, potem `empty()`, dopiero potem przetwarzaj. |
| Linia z samych spacji kończy odczyt | Program traktuje spacje jak pustą linię. | Odczyt kończy tylko linia, dla której `line.empty()` daje `true`. Same spacje to zwykła linia danych. |
| Program po pustej linii czeka na kolejne dane | Pusta linia nie zmienia flagi, na przykład program sprawdza coś innego niż `line.empty()`. | Po pustej linii ustaw flagę na `false`. |
| Liczba znaków jest większa o liczbę linii | Program dolicza znak końca linii, na przykład dodaje `line.size() + 1`. | `getline` nie dopisuje znaku końca linii do tekstu. Dodawaj samo `line.size()`. |
| Podsumowanie pojawia się po każdej linii | Wypisywanie podsumowania stoi wewnątrz pętli. | Podsumowanie wypisuj po pętli. |
| W raporcie brakuje spacji z początku albo z końca linii | Linia była odczytana przez `>>` albo program wypisuje coś innego niż oryginalny tekst. | Odczytuj linię przez `std::getline` i wypisuj ją bez zmian. |
| Program kończy odczyt, zanim wpiszesz pierwszy tekst | Przed `getline` stoi odczyt przez `>>`, który zostawił znak końca linii (punkt 2). | W tej lekcji czytaj dane tylko przez `std::getline`. |

## 10. Wyjaśnij

Odpowiedz własnymi słowami, najlepiej na piśmie. Dopiero potem porównaj z przykładowymi odpowiedziami.

1. Czym różni się odczyt jednej linii od odczytu kolejnych linii?
2. Czy `getline` zachowuje spacje? Czy dopisuje do tekstu znak końca linii?
3. Czy pustą linię można odczytać poprawnie? Co wtedy daje `line.empty()`?
4. Czy tekst `"   "` jest pusty?
5. Dlaczego najpierw sprawdzamy powodzenie odczytu, a dopiero potem `empty()`?
6. Czy koniec danych oznacza zawsze, że ostatnio odczytana linia jest niepoprawna?
7. Czy pusta linia kończąca zwiększa licznik przetworzonych linii?
8. Dlaczego program nie przechowuje wszystkich linii w wektorze?
9. Dlaczego funkcja wyznaczająca inicjały nie powinna sama odczytywać wejścia?

<details>
<summary>Przykładowe odpowiedzi</summary>

1. Jeden odczyt daje jeden tekst. Gdy linii jest wiele, a ich liczba nie jest znana z góry, odczyt stoi w pętli: jedna próba na przebieg, aż pusta linia albo nieudany odczyt zakończą pracę.
2. Zachowuje wszystkie spacje, także z początku i z końca linii. Znaku końca linii nie dopisuje: zabiera go z wejścia, ale ten znak tylko kończy odczyt. Dlatego nie ma go w `size()`.
3. Tak. Pusta linia to udany odczyt: `fail()` daje `false`, a odczytany tekst nie ma żadnych znaków, więc `line.empty()` daje `true`. W tej lekcji to sygnał od użytkownika, że to już wszystkie teksty.
4. Nie. Ma trzy znaki, spacje, więc `size()` daje 3, a `empty()` daje `false`. To zwykła linia danych z pustymi inicjałami.
5. Bo po nieudanym odczycie nie wolno polegać na zawartości `line`. Najpierw trzeba wiedzieć, czy linia w ogóle została odczytana. Dopiero wtedy jej treść, także to, czy jest pusta, coś znaczy.
6. Nie. Ostatnia linia może zostać odczytana poprawnie, nawet jeśli zaraz po niej kończą się dane. O jej przetworzeniu decyduje `fail()`, a pętlę kończy dopiero następna, nieudana próba.
7. Nie. To udany odczyt, ale nie rekord do analizy. Licznik rośnie tylko w gałęzi, która przetwarza linię.
8. Bo do wyniku każdej linii wystarcza ona sama, a do podsumowania dwa liczniki. Żadna późniejsza decyzja nie wymaga wcześniejszych linii. Wektor byłby potrzebny, gdyby program po odczycie musiał wrócić do wszystkich linii, na przykład wypisać je w innej kolejności.
9. Bo jej zadaniem jest tylko wyznaczyć inicjały danego tekstu. Funkcja, która nie czyta wejścia, działa dla każdego tekstu: wpisanego w kodzie, jak w lekcji 7.3, i odczytanego z wejścia, jak tutaj. O odczycie, końcu pracy i wypisywaniu decyduje `main`, jak w podziale odpowiedzialności z lekcji 5.5.

</details>

## Podsumowanie

- `std::getline` odczytuje całą linię ze spacjami. Znak końca linii kończy odczyt, ale nie trafia do tekstu.
- Pusta linia to udany odczyt z pustym tekstem. Nieudany odczyt oznacza, że linii nie ma, zwykle z powodu końca danych.
- Po każdym odczycie: najpierw `fail()`, potem `empty()`, dopiero potem przetwarzanie.
- Pętla `while` z flagą `bool` wykonuje jeden odczyt na przebieg. Ostatnią linię przed końcem danych też trzeba przetworzyć.
- Linia z samych spacji nie jest pusta.
- Liczniki rosną tylko dla przetworzonych linii, a wcześniejszych linii nie trzeba przechowywać.

## Co dalej

W kolejnej części Modułu 7 wykorzystasz umiejętności z całego modułu: analizę znaków i ich pozycji, budowanie nowego tekstu i odczyt wielu linii. Jest w przygotowaniu.

---

## Przykładowe rozwiązania

Zajrzyj tutaj **po własnej próbie**. Twoje nazwy mogą się różnić, jeśli standardowe wyjście jest takie, jak wymagane.

<details>
<summary>Punkt 7: misja, dziennik krótkich tekstów</summary>

<!-- example: texts_log -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>

std::string initials_of(const std::string& text) {
    std::string result{};

    for (std::size_t index{0}; index < text.size(); ++index) {
        const bool word_can_start{index == 0 || text[index - 1] == ' '};

        if (text[index] != ' ' && word_can_start) {
            result.push_back(text[index]);
        }
    }

    return result;
}

int main() {
    bool reading{true};
    std::size_t lines_processed{0};
    std::size_t characters_processed{0};

    while (reading) {
        std::string line{};
        std::getline(std::cin, line);

        if (std::cin.fail()) {
            reading = false;
        } else if (line.empty()) {
            reading = false;
        } else {
            ++lines_processed;
            characters_processed += line.size();

            const std::string initials{initials_of(line)};

            std::cout << "Line " << lines_processed << ": [" << line << "]\n";
            std::cout << "Initials " << lines_processed << ": [" << initials << "]\n";
        }
    }

    std::cout << "Lines processed: " << lines_processed << "\n";
    std::cout << "Characters processed: " << characters_processed << "\n";
}
```

1. **Dlaczego pętla.** Każda linia wymaga tych samych kroków: odczytu, decyzji i raportu. Pętla powtarza je dla kolejnych linii bez osobnego kodu dla każdej z nich.
2. **Liczba linii nie musi być znana z góry.** Pętla nie liczy przebiegów do żadnej granicy. Działa, dopóki flaga `reading` jest prawdziwa, a kończy ją sytuacja w danych: pusta linia albo nieudany odczyt.
3. **Najpierw odczyt, potem analiza.** `std::cin.fail()` jest sprawdzane jako pierwsze, bo po nieudanym odczycie nie wolno polegać na zawartości `line`. Dopiero po udanym odczycie program sprawdza `line.empty()`.
4. **Pusta linia kończy pracę**, bo to umówiony sygnał od użytkownika. Nie jest rekordem, więc nie trafia do raportu ani do liczników.
5. **Same spacje nie kończą pracy.** `"   "` ma trzy znaki, więc `empty()` daje `false`. Linia jest przetwarzana, a funkcja zwraca dla niej puste inicjały.
6. **Ostatnia linia może nie mieć znaku końca linii.** Gdy dane kończą się zaraz po jej ostatnim znaku, `getline` i tak ją dostarcza, a `fail()` daje `false`. Program ją przetwarza, a pętlę kończy dopiero następna, nieudana próba.
7. **Licznik po sprawdzeniach.** `++lines_processed` stoi w gałęzi dla niepustej, poprawnie odczytanej linii. Dzięki temu numer w raporcie i liczba w podsumowaniu dotyczą tylko przetworzonych linii.
8. **Funkcja dla każdej linii osobno.** Każda linia to osobny tekst z własnymi inicjałami. `initials_of` dostaje ją przez `const std::string&`, bez kopiowania, i zwraca nowy tekst, który `main` od razu wypisuje.
9. **Bez wektora.** Raport linii powstaje zaraz po jej odczycie, a podsumowanie potrzebuje tylko dwóch liczb. Żadna decyzja nie wymaga wcześniejszych linii.
10. **To samo podsumowanie.** Obie przyczyny zakończenia ustawiają tę samą flagę, a podsumowanie stoi po pętli, więc nie zależy od tego, co ją zakończyło.
11. **Tylko `getline`.** Po odczycie przez `>>` w wejściu zostałby znak końca linii. `getline` odczytałoby go jako pustą linię i program zakończyłby pracę, zanim przetworzyłby jakikolwiek tekst.
12. **Co zostawiamy na później:** rozróżnianie przyczyn nieudanego odczytu, łączenie `>>` z `getline`, sprawdzanie, czy linie spełniają założenia misji, na przykład czy nie ma w nich cyfr, i odczyt danych z plików.

**Inne poprawne układy.** Obie gałęzie, które kończą pętlę, można połączyć w jeden warunek: `if (std::cin.fail() || line.empty())`. Krótkie obliczanie z lekcji 3.4 sprawdza wtedy `line.empty()` tylko po udanym odczycie. Ważne, żeby przetwarzanie i liczniki stały wyłącznie w gałęzi dla niepustej, poprawnie odczytanej linii. W innych programach możesz też spotkać odczyt wpisany wprost w warunek pętli: `while (std::getline(std::cin, line))`. To poprawny C++, ale jego zrozumienie wymaga wiedzy o strumieniach, której jeszcze nie mamy, więc w tym kursie zostajemy przy fladze i `std::cin.fail()`.

**Wyniki pozostałych przypadków z listy kontrolnej.** Przypadki A, B i E są w treści misji. W przypadkach D i K dane kończą się po ostatniej podanej linii.

Przypadek C, `Ada` i pusta linia:

<!-- input: texts_log -->
```text
Ada

```

<!-- output: texts_log -->
```text
Line 1: [Ada]
Initials 1: [A]
Lines processed: 1
Characters processed: 3
```

Przypadek D, te same dwie linie co w A, po których kończą się dane:

<!-- input: texts_log -->
```text
Ada Lovelace
Mary ann SMITH
```

<!-- output: texts_log -->
```text
Line 1: [Ada Lovelace]
Initials 1: [AL]
Line 2: [Mary ann SMITH]
Initials 2: [MaS]
Lines processed: 2
Characters processed: 26
```

Przypadek F, `  Ada  ` z dwiema spacjami na początku i dwiema na końcu:

<!-- input: texts_log -->
```text
  Ada  

```

<!-- output: texts_log -->
```text
Line 1: [  Ada  ]
Initials 1: [A]
Lines processed: 1
Characters processed: 7
```

Przypadek G, `A  B   C`:

<!-- input: texts_log -->
```text
A  B   C

```

<!-- output: texts_log -->
```text
Line 1: [A  B   C]
Initials 1: [ABC]
Lines processed: 1
Characters processed: 8
```

Przypadek H, `A`:

<!-- input: texts_log -->
```text
A

```

<!-- output: texts_log -->
```text
Line 1: [A]
Initials 1: [A]
Lines processed: 1
Characters processed: 1
```

Przypadek I, linie o różnych długościach, 2, 12 i 20 znaków:

<!-- input: texts_log -->
```text
Bo
Grace Hopper
Alan Mathison Turing

```

<!-- output: texts_log -->
```text
Line 1: [Bo]
Initials 1: [B]
Line 2: [Grace Hopper]
Initials 2: [GH]
Line 3: [Alan Mathison Turing]
Initials 3: [AMT]
Lines processed: 3
Characters processed: 34
```

Przypadek J, pusta linia między dwoma tekstami:

<!-- input: texts_log -->
```text
Grace Hopper

Ada Lovelace
```

<!-- output: texts_log -->
```text
Line 1: [Grace Hopper]
Initials 1: [GH]
Lines processed: 1
Characters processed: 12
```

Przypadek K, pięć krótkich linii, po których kończą się dane:

<!-- input: texts_log -->
```text
Al
Bo
Cy
Di
Ed
```

<!-- output: texts_log -->
```text
Line 1: [Al]
Initials 1: [A]
Line 2: [Bo]
Initials 2: [B]
Line 3: [Cy]
Initials 3: [C]
Line 4: [Di]
Initials 4: [D]
Line 5: [Ed]
Initials 5: [E]
Lines processed: 5
Characters processed: 10
```

Przypadek L, różna wielkość liter:

<!-- input: texts_log -->
```text
ada lovelace
ADA LOVELACE
ada Lovelace

```

<!-- output: texts_log -->
```text
Line 1: [ada lovelace]
Initials 1: [al]
Line 2: [ADA LOVELACE]
Initials 2: [AL]
Line 3: [ada Lovelace]
Initials 3: [aL]
Lines processed: 3
Characters processed: 36
```

</details>

<details>
<summary>Punkt 8: wyniki przed poprawką i poprawiony program</summary>

Przed poprawką, zestaw (a): `Ada Lovelace` i `Mary ann SMITH`, po których kończą się dane:

<!-- input: texts_log_count_bug -->
```text
Ada Lovelace
Mary ann SMITH
```

<!-- output: texts_log_count_bug -->
```text
Line 1: [Ada Lovelace]
Initials 1: [AL]
Line 2: [Mary ann SMITH]
Initials 2: [MaS]
Lines processed: 2
Characters processed: 26
```

Zestaw (b): `Ada` i pusta linia:

<!-- input: texts_log_count_bug -->
```text
Ada

```

<!-- output: texts_log_count_bug -->
```text
Line 1: [Ada]
Initials 1: [A]
Lines processed: 2
Characters processed: 3
```

| Próba | Odczytana linia | `fail()` | `lines_processed` po `++` | `empty()` | Działanie |
|---|---|---|---|---|---|
| 1 | `Ada` | `false` | 1 | `false` | raport `Line 1` |
| 2 | pusta | `false` | **2** | `true` | koniec pętli |

Pusta linia jako pierwsza:

<!-- input: texts_log_count_bug -->
```text

```

<!-- output: texts_log_count_bug -->
```text
Lines processed: 1
Characters processed: 0
```

- **Przyczyna:** program zwiększa licznik po każdym udanym odczycie, zanim sprawdzi, czy linia jest pusta. Pusta linia kończąca to udany odczyt, więc też zostaje policzona, choć nie jest rekordem. Raporty `Line N` są poprawne, bo dla pustej linii program niczego nie wypisuje. Błędne jest tylko podsumowanie.
- **Dlaczego zestaw (a) nie ujawnia błędu:** dane kończą się bez pustej linii. Ostatnia próba się nie udaje, a po nieudanym odczycie licznik nie rośnie, więc podsumowanie jest poprawne.
- **Poprawka:** przenieś `++lines_processed;` do gałęzi dla niepustej linii, przed `characters_processed += line.size();`. W gałęzi `else` zostaje wtedy sam `if`, który można zapisać jako `else if`.

Poprawiony program to rozwiązanie referencyjne z punktu 7. Dla pustej linii jako pierwszej daje `Lines processed: 0` (przypadek B), dla `Ada` i pustej linii `Lines processed: 1` (przypadek C), a dla zestawu (a) ten sam raport co wcześniej (przypadek D). Odczytu spoza tekstu nie ma w żadnej wersji: funkcja inicjałów jest taka sama jak w rozwiązaniu referencyjnym.

</details>

**Poprzednia lekcja:** [Lekcja 7.3: Funkcja tworzy nowy tekst](lesson_03_a_function_creates_a_new_text.md) · **Następna lekcja:** w przygotowaniu · [Opis kursu](../../README.md)

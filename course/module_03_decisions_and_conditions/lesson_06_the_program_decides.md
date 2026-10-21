# Lekcja 3.6: Program podejmuje decyzje (sprawdzian Modułu 3)

**Polski** · [English](lesson_06_the_program_decides.en.md) · [Opis kursu](../../README.md)

> **Moduł 3, lekcja 6: sprawdzian** · około 90–100 minut, można go podzielić na dwa podejścia
> **Potrzebujesz:** katalogu `cpp-workspace` i oryginalnego projektu `lesson_05_first_program`.
> **Wersja pilotażowa.** Rozwiązania referencyjne z tej lekcji sprawdzamy automatycznie na Windowsie, Ubuntu i macOS, z podanymi danymi wejściowymi. Twojej pracy nic nie ocenia automatycznie: sprawdzasz ją samodzielnie, według kryteriów.

## Jak przebiega ten sprawdzian

Ta lekcja nie wprowadza niczego nowego. Sprawdzasz, czy potrafisz samodzielnie zaprojektować program, którego zachowanie zależy od kilku wymagań i danych wejściowych: sprawdza dane, wybiera kategorię, liczy tylko wtedy, gdy wolno, i podejmuje decyzję na podstawie kilku warunków. Do tego diagnozujesz dwa krótkie programy z błędami logicznymi i wyjaśniasz swoje decyzje.

Lekcja ma dwie części:

- **Część A: sprawdzian.** Wymagania, dane testowe, oczekiwane wyniki, pytania i kryteria. Bez podpowiedzi i bez kodu rozwiązań. Wszystko, czego potrzebujesz, znasz z Modułów 1–3.
- **Część B: sprawdzenie i omówienie.** Podpowiedzi, pełne listy przypadków kontrolnych, przykładowe rozwiązania, wyjaśnienia i samoocena. Przejdź do niej po wykonaniu części A albo wtedy, gdy świadomie zrezygnujesz z dalszej samodzielnej próby.

Zajrzenie do części B, do wcześniejszych lekcji albo do notatek nie jest porażką. Ważne jest, żeby **uczciwie zanotować, co zrobiono samodzielnie, a co z pomocą**. Sprawdzian możesz podzielić na dwa podejścia, na przykład zadanie 1 jednego dnia, a zadania 2 i 3 następnego.

**Możesz używać:** CLiona albo terminala, CMake i Ninja, jak dotąd; `CMakeLists.txt` skopiowanego z oryginalnego `lesson_05_first_program`; tabeli przypadków i tymczasowych instrukcji `std::cout`; debuggera z lekcji 2.3, jeśli działa w Twoim środowisku.

We wszystkich zadaniach zakładamy, że użytkownik wpisuje dane w poprawnej postaci: tekst tam, gdzie program pyta o tekst, i liczby tam, gdzie pyta o liczby. **Wartości** liczb mogą jednak nie spełniać wymagań zadania i to program ma sprawdzić.

---

# Część A: sprawdzian

## Zadanie 1: Pokaz naukowy

Organizatorzy przygotowują pokaz naukowy. Program pomaga im ocenić plan wydarzenia.

**Przygotowanie:** w `cpp-workspace` utwórz katalog `science_show`, skopiuj do niego `CMakeLists.txt` z oryginalnego `lesson_05_first_program`, utwórz **pusty** `main.cpp` i napisz cały program samodzielnie. Nie kopiuj programów z wcześniejszych lekcji.

**Dane wejściowe**, w tej kolejności, każda wartość w osobnej linijce:

1. nazwa wydarzenia: cała linijka tekstu, może zawierać spacje;
2. czas trwania w godzinach: liczba z częścią ułamkową;
3. liczba uczestników: liczba całkowita.

**Wymagania danych.** Dane są dopuszczalne, gdy:

- czas trwania jest większy od zera;
- liczba uczestników wynosi co najmniej 1 i nie przekracza 30.

Jeśli którekolwiek wymaganie nie jest spełnione, program po prośbach o dane wypisuje tylko `Invalid event data` i nie robi nic więcej. Nie pyta ponownie o dane.

**Dla dopuszczalnych danych** program wypisuje raport:

1. `Event: ` i nazwę wydarzenia;
2. kategorię czasu trwania:

   | Czas trwania | Kategoria |
   |---|---|
   | do 1.5 godziny włącznie | `Short` |
   | powyżej 1.5, do 3 godzin włącznie | `Standard` |
   | powyżej 3 godzin | `Extended` |

3. liczbę **pełnych** grup po 6 uczestników i liczbę uczestników, którzy zostają poza pełnymi grupami (dla 19 osób: 3 pełne grupy i 1 osoba);
4. czy potrzebna jest dodatkowa osoba do pomocy. Jest potrzebna, gdy spełniony jest **przynajmniej jeden** z warunków: czas trwania przekracza 3 godziny **lub** uczestników jest więcej niż 18. Program wypisuje wtedy `Extra helper: Yes`, a w przeciwnym razie `Extra helper: No`.

**Pierwszy przykład:**

<!-- input: science_show -->
```text
Night Sky Show
1.5
12
```

Standardowe wyjście ma być dokładnie takie:

<!-- output: science_show -->
```text
Enter event name:
Enter duration in hours:
Enter participant count:
Event: Night Sky Show
Duration category: Short
Full groups: 2
Remaining participants: 0
Extra helper: No
```

**Drugi przykład:**

<!-- input: science_show -->
```text
Robotics Demo
2.5
19
```

<!-- output: science_show -->
```text
Enter event name:
Enter duration in hours:
Enter participant count:
Event: Robotics Demo
Duration category: Standard
Full groups: 3
Remaining participants: 1
Extra helper: Yes
```

**Trzeci przykład, dane niespełniające wymagań:**

<!-- input: science_show -->
```text
Chemistry Fair
2.0
31
```

<!-- output: science_show -->
```text
Enter event name:
Enter duration in hours:
Enter participant count:
Invalid event data
```

**Przed uruchomieniem programu przygotuj tabelę przypadków testowych.** Musi sprawdzać co najmniej:

- obie granice kategorii czasu (1.5 i 3), na samej granicy i tuż nad nią;
- najmniejszą i największą dopuszczalną liczbę uczestników oraz liczby tuż poza zakresem;
- granicę 18 uczestników dla dodatkowej pomocy, na samej granicy i tuż nad nią;
- wszystkie cztery kombinacje warunków dodatkowej pomocy: żaden, tylko czas, tylko liczba uczestników, oba;
- czas równy zero i czas ujemny;
- podział na grupy z resztą i bez reszty.

Przy każdym przypadku zapisz oczekiwany wynik. Potem uruchom program dla wszystkich i porównaj.

Na ekranie zobaczysz między linijkami programu także wpisane dane: to echo, a nie standardowe wyjście (lekcja 2.6). Czas 2.0 możesz wpisać też jako `2`.

Gdy wynik się zgadza, możesz zapisać projekt w Gicie, jak w lekcji 1.5. Przed commitem sprawdź `git status`: do historii trafiają tylko `main.cpp` i `CMakeLists.txt`.

## Zadanie 2: Dwa zgłoszenia

W `cpp-workspace` utwórz katalog `diagnosis_3`, skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program`. Każdy z poniższych programów wpisz po kolei w `main.cpp` tego katalogu. Oba się budują i działają, ale dają złe wyniki.

**Zgłoszenie A.** Firma kurierska klasyfikuje paczki według wagi w kilogramach (liczba całkowita, co najmniej 1):

| Waga | Rozmiar |
|---|---|
| do 5 kg włącznie | `Small` |
| od 6 do 20 kg | `Medium` |
| powyżej 20 kg | `Large` |

<!-- example: parcel_size_bug -->
```cpp
#include <iostream>

int main() {
    int weight_kg{0};

    std::cout << "Enter parcel weight in kg:\n";
    std::cin >> weight_kg;

    if (weight_kg <= 20) {
        std::cout << "Size: Medium\n";
    } else if (weight_kg <= 5) {
        std::cout << "Size: Small\n";
    } else {
        std::cout << "Size: Large\n";
    }
}
```

**Zgłoszenie B.** Na ściankę wspinaczkową mogą wejść osoby, które mają **co najmniej 140 cm wzrostu i co najmniej 10 lat**. Oba wymagania muszą być spełnione jednocześnie.

<!-- example: climbing_bug -->
```cpp
#include <iostream>

int main() {
    int height_cm{0};
    int age{0};

    std::cout << "Enter height in cm:\n";
    std::cin >> height_cm;
    std::cout << "Enter age:\n";
    std::cin >> age;

    const bool allowed{height_cm >= 140 || age >= 10};

    if (allowed) {
        std::cout << "Climbing: allowed\n";
    } else {
        std::cout << "Climbing: not allowed\n";
    }
}
```

**Dla każdego zgłoszenia:**

1. Przeczytaj wymagania i zdecyduj, jakie wyniki są poprawne.
2. Przygotuj przypadki testowe: dla zgłoszenia A granice wszystkich rozmiarów, dla zgłoszenia B cztery kombinacje: oba wymagania spełnione, tylko pierwsze, tylko drugie, żadne.
3. **Przewidź**, co wypisze błędny program dla Twoich przypadków.
4. Uruchom program i porównaj.
5. Znajdź przyczynę: kolejność warunków albo niewłaściwy operator.
6. Popraw program jedną zmianą.
7. Sprawdź ponownie wszystkie przypadki.

Zapisz wyniki w tabeli:

| Zgłoszenie | Przypadek, który ujawnia błąd | Rzeczywisty wynik | Przyczyna | Poprawka | Sprawdzenie |
|---|---|---|---|---|---|
| A | | | | | |
| B | | | | | |

Projektu `diagnosis_3` nie musisz zapisywać w Gicie.

## Zadanie 3: Wyjaśnij

Odpowiedz krótko, na piśmie, odwołując się do własnego programu z zadania 1:

1. Dlaczego sprawdzenie wymagań danych stoi przed klasyfikacją i obliczeniami?
2. Dlaczego przy sprawdzaniu liczby uczestników używasz `&&`?
3. Dlaczego decyzja o dodatkowej pomocy korzysta z `||`? Co się stanie, gdy spełnione są oba jej warunki?
4. Dlaczego kolejność warunków w łańcuchu `else if` ma znaczenie? Pokaż to na swoim łańcuchu kategorii.
5. Jeśli `needs_extra_helper` jest zmienną typu `bool`, co oznacza `!needs_extra_helper`?
6. Dlaczego warto sprawdzać wartości dokładnie na granicach? Podaj jedną granicę z zadania 1, przy której pomyłka `<` i `<=` zmieniłaby wynik.
7. Dlaczego nie można twierdzić, że Twój program poprawnie obsługuje wpisanie `abc` zamiast liczby?

## Kryteria sukcesu

Sprawdzian jest zaliczony, gdy spełniasz **wszystkie** kryteria:

- `science_show/main.cpp` napisano od pustego pliku, w poprawnym C++20. Program buduje się bez błędów.
- Nazwa jest odczytana w całości przez `std::getline`, **przed** odczytami liczb przez `>>`. Czas trwania jest typu `double`, a liczba uczestników typu `int`, wszystkie z wartościami początkowymi.
- Wymagania danych są sprawdzane **przed** klasyfikacją i obliczeniami. Dla danych niespełniających wymagań program wypisuje tylko `Invalid event data`.
- Kategorie wybiera łańcuch `if`/`else if`/`else` w kolejności, w której każda gałąź jest osiągalna.
- Pełne grupy i pozostałych uczestników obliczają `/` i `%`. Wielkość grupy jest stałą.
- Decyzję o dodatkowej pomocy wyraża czytelny warunek z `||`. Przynajmniej jeden warunek jest zapisany w nazwanej zmiennej `bool`.
- Standardowe wyjście dla trzech przykładów i dla wszystkich Twoich przypadków jest zgodne z wymaganiami.
- Tabela przypadków powstała przed uruchomieniem programu i sprawdza granice wymienione w zadaniu 1.
- Oba zgłoszenia z zadania 2 zdiagnozowano i poprawiono, a wszystkie przypadki sprawdzono ponownie.
- Umiesz wyjaśnić każdą linijkę swojego programu i odpowiedzieć na pytania z zadania 3.

Zagnieżdżony `if` jest dozwolony, ale niewymagany. Nazwy zmiennych mogą być inne niż w rozwiązaniu referencyjnym, jeśli są czytelne. Poprawny wynik to warunek konieczny, ale **nie dowód zrozumienia**. Dlatego zadanie 3 jest częścią sprawdzianu.

---

# Część B: sprawdzenie i omówienie

Przejdź tutaj po wykonaniu części A albo wtedy, gdy świadomie zrezygnujesz z dalszej samodzielnej próby.

## Jak sprawdzić swoją pracę

- **Standardowe wyjście:** uruchom program dla każdego przypadku z tabeli i porównaj linijki programu z oczekiwanymi, znak po znaku. Pomiń wpisane dane widoczne dzięki echu.
- **Ten sam program:** między uruchomieniami nie zmieniaj kodu.
- **Pełne listy przypadków kontrolnych** poniżej porównaj ze swoją tabelą. Czy Twoja tabela obejmowała te same granice?
- **Kolejność:** przejrzyj program od góry. Czy żadne dzielenie ani klasyfikacja nie wykonuje się przed sprawdzeniem danych?

## Podpowiedzi

Każda podpowiedź dotyczy sposobu myślenia. Rozwijaj je po kolei i tylko wtedy, gdy ich potrzebujesz.

<details>
<summary>Zadanie 1, podpowiedź 1: od czego zacząć?</summary>

Od typów i odczytów: tekst ze spacjami, liczba z częścią ułamkową, liczba całkowita. Która metoda odczytu musi być pierwsza (lekcja 2.7)? Potem jedna decyzja: czy dane spełniają wymagania (lekcja 3.5)?

</details>

<details>
<summary>Zadanie 1, podpowiedź 2: kategorie i grupy</summary>

Kategorie to łańcuch z trzema gałęziami. Gdy progi pytają „do … włącznie”, zacznij od najniższego progu z `<=` (lekcja 3.3). Grupy po 6: „ile pełnych?” i „ile zostanie?” (lekcja 2.4). Wszystko to wykonuje się tylko dla dopuszczalnych danych.

</details>

<details>
<summary>Zadanie 1, podpowiedź 3: dodatkowa pomoc</summary>

Wymaganie mówi „przynajmniej jeden z warunków”. Który operator odpowiada „lub”, również wtedy, gdy oba warunki są spełnione (lekcja 3.4)? Nadaj wynikowi nazwę, na przykład `needs_extra_helper`.

</details>

<details>
<summary>Zadanie 2, zgłoszenie A</summary>

Dla wagi 3 kg który warunek jest sprawdzany jako pierwszy i czy jest spełniony? Czy do gałęzi `Small` program może kiedykolwiek dojść?

</details>

<details>
<summary>Zadanie 2, zgłoszenie B</summary>

Wymaganie mówi, że oba warunki muszą być spełnione jednocześnie. Który przypadek z czterech kombinacji ujawni, że program przyjmuje osoby spełniające tylko jeden warunek?

</details>

## Pełna lista przypadków kontrolnych: zadanie 1

<details>
<summary>Otwórz po przygotowaniu własnej tabeli</summary>

Pierwsze trzy przypadki są sprawdzone w części A.

| Nazwa | Czas | Uczestnicy | Kategoria | Grupy | Zostaje | Pomoc | Co sprawdza |
|---|---|---|---|---|---|---|---|
| Night Sky Show | 1.5 | 12 | `Short` | 2 | 0 | `No` | granica 1.5, podział bez reszty, żaden warunek pomocy |
| Robotics Demo | 2.5 | 19 | `Standard` | 3 | 1 | `Yes` | pomoc tylko z powodu uczestników (19) |
| Chemistry Fair | 2.0 | 31 | — | — | — | — | 31 uczestników: poza zakresem |
| Volcano Lab | 3.5 | 12 | `Extended` | 2 | 0 | `Yes` | pomoc tylko z powodu czasu |
| Star Party Marathon | 3.5 | 24 | `Extended` | 4 | 0 | `Yes` | oba warunki pomocy |
| Magnet Workshop | 3.0 | 18 | `Standard` | 3 | 0 | `No` | granica 3.0 i granica 18 |
| Crystal Club | 1.75 | 6 | `Standard` | 1 | 0 | `No` | tuż nad granicą 1.5 |
| Tiny Bugs Tour | 1.25 | 1 | `Short` | 0 | 1 | `No` | najmniejsza liczba uczestników, brak pełnej grupy |
| Big Science Day | 2.0 | 30 | `Standard` | 5 | 0 | `Yes` | największa liczba uczestników |
| Zero Hour Talk | 0 | 12 | — | — | — | — | czas równy zero |
| Time Machine Show | -1.5 | 10 | — | — | — | — | czas ujemny |
| Empty Room Demo | 2.0 | 0 | — | — | — | — | zero uczestników |

Przypadki z kreskami kończą się linijką `Invalid event data`.

<!-- input: science_show -->
```text
Volcano Lab
3.5
12
```

<!-- output: science_show -->
```text
Enter event name:
Enter duration in hours:
Enter participant count:
Event: Volcano Lab
Duration category: Extended
Full groups: 2
Remaining participants: 0
Extra helper: Yes
```

<!-- input: science_show -->
```text
Star Party Marathon
3.5
24
```

<!-- output: science_show -->
```text
Enter event name:
Enter duration in hours:
Enter participant count:
Event: Star Party Marathon
Duration category: Extended
Full groups: 4
Remaining participants: 0
Extra helper: Yes
```

<!-- input: science_show -->
```text
Magnet Workshop
3.0
18
```

<!-- output: science_show -->
```text
Enter event name:
Enter duration in hours:
Enter participant count:
Event: Magnet Workshop
Duration category: Standard
Full groups: 3
Remaining participants: 0
Extra helper: No
```

<!-- input: science_show -->
```text
Crystal Club
1.75
6
```

<!-- output: science_show -->
```text
Enter event name:
Enter duration in hours:
Enter participant count:
Event: Crystal Club
Duration category: Standard
Full groups: 1
Remaining participants: 0
Extra helper: No
```

<!-- input: science_show -->
```text
Tiny Bugs Tour
1.25
1
```

<!-- output: science_show -->
```text
Enter event name:
Enter duration in hours:
Enter participant count:
Event: Tiny Bugs Tour
Duration category: Short
Full groups: 0
Remaining participants: 1
Extra helper: No
```

<!-- input: science_show -->
```text
Big Science Day
2.0
30
```

<!-- output: science_show -->
```text
Enter event name:
Enter duration in hours:
Enter participant count:
Event: Big Science Day
Duration category: Standard
Full groups: 5
Remaining participants: 0
Extra helper: Yes
```

<!-- input: science_show -->
```text
Zero Hour Talk
0
12
```

<!-- output: science_show -->
```text
Enter event name:
Enter duration in hours:
Enter participant count:
Invalid event data
```

<!-- input: science_show -->
```text
Time Machine Show
-1.5
10
```

<!-- output: science_show -->
```text
Enter event name:
Enter duration in hours:
Enter participant count:
Invalid event data
```

<!-- input: science_show -->
```text
Empty Room Demo
2.0
0
```

<!-- output: science_show -->
```text
Enter event name:
Enter duration in hours:
Enter participant count:
Invalid event data
```

</details>

## Przykładowe rozwiązania

<details>
<summary>Zadanie 1: pokaz naukowy</summary>

<!-- example: science_show -->
```cpp
#include <iostream>
#include <string>

int main() {
    const int group_size{6};

    std::string event_name{""};
    double duration_hours{0.0};
    int participants{0};

    std::cout << "Enter event name:\n";
    std::getline(std::cin, event_name);
    std::cout << "Enter duration in hours:\n";
    std::cin >> duration_hours;
    std::cout << "Enter participant count:\n";
    std::cin >> participants;

    const bool valid_data{duration_hours > 0.0 && participants >= 1 && participants <= 30};

    if (valid_data) {
        std::cout << "Event: " << event_name << "\n";

        if (duration_hours <= 1.5) {
            std::cout << "Duration category: Short\n";
        } else if (duration_hours <= 3.0) {
            std::cout << "Duration category: Standard\n";
        } else {
            std::cout << "Duration category: Extended\n";
        }

        const int full_groups{participants / group_size};
        const int remaining_participants{participants % group_size};
        std::cout << "Full groups: " << full_groups << "\n";
        std::cout << "Remaining participants: " << remaining_participants << "\n";

        const bool needs_extra_helper{duration_hours > 3.0 || participants > 18};
        if (needs_extra_helper) {
            std::cout << "Extra helper: Yes\n";
        } else {
            std::cout << "Extra helper: No\n";
        }
    } else {
        std::cout << "Invalid event data\n";
    }
}
```

- **Najpierw sprawdzenie:** `valid_data` łączy trzy wymagania przez `&&`, bo wszystkie muszą być spełnione. Klasyfikacja, dzielenie i decyzja o pomocy stoją w gałęzi dla dopuszczalnych danych. Dla danych niespełniających wymagań program niczego nie liczy.
- **Kategorie:** progi „do … włącznie” idą od najniższego, z `<=`. Do `else if (duration_hours <= 3.0)` program dochodzi tylko wtedy, gdy czas przekracza 1.5, więc ta gałąź obsługuje dokładnie przedział od 1.5 (bez) do 3.0 (włącznie).
- **Grupy:** `/` daje pełne grupy, `%` uczestników poza nimi. Dzielnik jest stałą 6, więc dzielenie przez zero nie grozi.
- **Pomoc:** `||`, bo wystarczy jeden warunek, także gdy spełnione są oba. Granice 3.0 i 18 nie dają pomocy, bo wymaganie mówi „przekracza”.
- Łańcuch kategorii i decyzja o pomocy stoją wewnątrz gałęzi `if (valid_data)`, czyli o jeden poziom głębiej. To dozwolone zagnieżdżenie. Inne czytelne układy, które dają ten sam wynik, też są poprawne.

</details>

<details>
<summary>Zadanie 2, zgłoszenie A: wynik przed poprawką i poprawiony program</summary>

Przed poprawką:

<!-- input: parcel_size_bug -->
```text
3
```

<!-- output: parcel_size_bug -->
```text
Enter parcel weight in kg:
Size: Medium
```

<!-- input: parcel_size_bug -->
```text
12
```

<!-- output: parcel_size_bug -->
```text
Enter parcel weight in kg:
Size: Medium
```

<!-- input: parcel_size_bug -->
```text
25
```

<!-- output: parcel_size_bug -->
```text
Enter parcel weight in kg:
Size: Large
```

- **Przypadek, który ujawnia błąd:** każda waga do 5 kg, na przykład 3 kg daje `Medium` zamiast `Small`.
- **Przyczyna:** `weight_kg <= 20` stoi pierwsze i przechwytuje także wszystkie wagi do 5 kg, więc gałąź `Small` jest nieosiągalna. Każdy warunek osobno jest poprawny, zła jest kolejność.
- **Poprawka:** zamień kolejność dwóch pierwszych warunków:

<!-- example: parcel_size_fixed -->
```cpp
#include <iostream>

int main() {
    int weight_kg{0};

    std::cout << "Enter parcel weight in kg:\n";
    std::cin >> weight_kg;

    if (weight_kg <= 5) {
        std::cout << "Size: Small\n";
    } else if (weight_kg <= 20) {
        std::cout << "Size: Medium\n";
    } else {
        std::cout << "Size: Large\n";
    }
}
```

Granice po poprawce:

<!-- input: parcel_size_fixed -->
```text
5
```

<!-- output: parcel_size_fixed -->
```text
Enter parcel weight in kg:
Size: Small
```

<!-- input: parcel_size_fixed -->
```text
6
```

<!-- output: parcel_size_fixed -->
```text
Enter parcel weight in kg:
Size: Medium
```

<!-- input: parcel_size_fixed -->
```text
20
```

<!-- output: parcel_size_fixed -->
```text
Enter parcel weight in kg:
Size: Medium
```

<!-- input: parcel_size_fixed -->
```text
21
```

<!-- output: parcel_size_fixed -->
```text
Enter parcel weight in kg:
Size: Large
```

</details>

<details>
<summary>Zadanie 2, zgłoszenie B: wynik przed poprawką i poprawiony program</summary>

Przed poprawką, dla czterech kombinacji (wzrost, wiek):

<!-- input: climbing_bug -->
```text
150
12
```

<!-- output: climbing_bug -->
```text
Enter height in cm:
Enter age:
Climbing: allowed
```

<!-- input: climbing_bug -->
```text
150
8
```

<!-- output: climbing_bug -->
```text
Enter height in cm:
Enter age:
Climbing: allowed
```

<!-- input: climbing_bug -->
```text
130
12
```

<!-- output: climbing_bug -->
```text
Enter height in cm:
Enter age:
Climbing: allowed
```

<!-- input: climbing_bug -->
```text
130
8
```

<!-- output: climbing_bug -->
```text
Enter height in cm:
Enter age:
Climbing: not allowed
```

- **Przypadki, które ujawniają błąd:** 150 cm i 8 lat oraz 130 cm i 12 lat. Każdy spełnia tylko jedno wymaganie, a program wpuszcza.
- **Przyczyna:** `||` jest prawdziwe, gdy spełniony jest choćby jeden warunek. Wymaganie mówi „oba jednocześnie”, czyli „i”.
- **Poprawka:** `&&` zamiast `||`:

<!-- example: climbing_fixed -->
```cpp
#include <iostream>

int main() {
    int height_cm{0};
    int age{0};

    std::cout << "Enter height in cm:\n";
    std::cin >> height_cm;
    std::cout << "Enter age:\n";
    std::cin >> age;

    const bool allowed{height_cm >= 140 && age >= 10};

    if (allowed) {
        std::cout << "Climbing: allowed\n";
    } else {
        std::cout << "Climbing: not allowed\n";
    }
}
```

Po poprawce, te same cztery kombinacje:

<!-- input: climbing_fixed -->
```text
150
12
```

<!-- output: climbing_fixed -->
```text
Enter height in cm:
Enter age:
Climbing: allowed
```

<!-- input: climbing_fixed -->
```text
150
8
```

<!-- output: climbing_fixed -->
```text
Enter height in cm:
Enter age:
Climbing: not allowed
```

<!-- input: climbing_fixed -->
```text
130
12
```

<!-- output: climbing_fixed -->
```text
Enter height in cm:
Enter age:
Climbing: not allowed
```

<!-- input: climbing_fixed -->
```text
130
8
```

<!-- output: climbing_fixed -->
```text
Enter height in cm:
Enter age:
Climbing: not allowed
```

Przypadki „oba spełnione” i „żadne” dają ten sam wynik przed poprawką i po niej. Dlatego testowanie tylko ich nie wykryłoby błędu: potrzebne są przypadki, w których spełnione jest tylko jedno wymaganie.

</details>

## Przykładowe odpowiedzi do zadania 3

<details>
<summary>Pokaż przykładowe odpowiedzi</summary>

1. Bo obliczenia i klasyfikacja mają sens tylko dla dopuszczalnych danych. Gdy dane nie spełniają wymagań, program wypisuje `Invalid event data` i niczego nie liczy.
2. Bo liczba uczestników musi spełniać dwa warunki jednocześnie: co najmniej 1 **i** najwyżej 30. Przedział zapisuje się jako dwa porównania połączone przez `&&`.
3. Bo wystarczy jeden z warunków. `||` jest prawdziwe także wtedy, gdy oba warunki są spełnione, więc wtedy też jest `Extra helper: Yes`.
4. Bo program wykonuje gałąź pierwszego spełnionego warunku. Gdyby `duration_hours <= 3.0` stało przed `duration_hours <= 1.5`, czas 1.25 dostałby `Standard`, a gałąź `Short` byłaby nieosiągalna.
5. „Nie potrzeba dodatkowej pomocy”: `!needs_extra_helper` jest `true`, gdy `needs_extra_helper` jest `false`, i odwrotnie. Sama zmienna się nie zmienia.
6. Bo pomyłka `<` z `<=` (albo `>` z `>=`) zmienia wynik tylko dokładnie na granicy. Na przykład dla 18 uczestników: wymaganie „więcej niż 18” to `> 18`. Przy `>= 18` program zażądałby pomocy dla 18 osób.
7. Bo program sprawdza tylko wartości, które udało się odczytać. Wpisanie `abc` to nieudany odczyt, a tego program nie wykrywa. Obsługę takich sytuacji poznasz później.

</details>

## Samoocena

Przy każdym kryterium zaznacz jedną odpowiedź:

| Kryterium | Samodzielnie | Z podpowiedzią | Po zajrzeniu do rozwiązania | Do powtórki |
|---|---|---|---|---|
| Napisanie programu od pustego `main.cpp` | | | | |
| Odczyt nazwy przez `std::getline` i liczb przez `>>` | | | | |
| Sprawdzenie wymagań danych przed obliczeniami | | | | |
| Łańcuch kategorii w poprawnej kolejności | | | | |
| Pełne grupy i reszta przez `/` i `%` | | | | |
| Decyzja o pomocy z `\|\|` i zmienną `bool` | | | | |
| Tabela przypadków z granicami przed uruchomieniem | | | | |
| Diagnoza zgłoszenia A (kolejność `else if`) | | | | |
| Diagnoza zgłoszenia B (`&&` a `\|\|`) | | | | |
| Szukanie błędu tabelą przypadków i `std::cout` | | | | |
| Obsługa debuggera w CLionie | | | | |
| Wyjaśnienia z zadania 3 | | | | |

Wiersz o debuggerze dotyczy **narzędzia**, a wiersz o tabeli przypadków **techniki szukania błędu**. Obie umiejętności się uzupełniają, ale nie zastępują. Jeśli debugger nie działa w Twoim środowisku, zostaw jego wiersz pusty.

Jeśli w kolumnie „Do powtórki” jest coś zaznaczone, wróć do odpowiedniej lekcji:

| Temat | Lekcja |
|---|---|
| pierwszy warunek, porównania i granice | 3.1 |
| `else`, `bool`, równość i zasięg zmiennych | 3.2 |
| `else if` i kolejność warunków | 3.3 |
| `&&`, `\|\|`, `!` i krótkie obliczanie | 3.4 |
| sprawdzanie danych przed obliczeniami | 3.5 |
| `std::getline` i tekst | 2.7 |
| `double` i mieszanie typów | 2.5 |
| `/`, `%` i dzielenie całkowite | 2.4 |

Potem spróbuj zadania jeszcze raz, na przykład z innymi progami kategorii.

---

## Podsumowanie Modułu 3

Po sześciu lekcjach potrafisz:

- pisać programy, które wybierają różne działania zależnie od danych;
- zapisywać porównania i przechowywać ich wyniki w zmiennych `bool`;
- budować konstrukcje `if`, `else` i łańcuchy `else if` w poprawnej kolejności;
- łączyć warunki przez `&&` i `||` i odwracać je przez `!`;
- rozumieć krótkie obliczanie `&&` i `||`;
- planować przypadki testowe i sprawdzać wartości dokładnie na granicach;
- znajdować błędy w kolejności warunków i w doborze operatorów;
- sprawdzać dane przed obliczeniami i pomijać obliczenie, gdy wymagania nie są spełnione;
- odróżniać wartość niespełniającą wymagań od nieudanego odczytu.

Programy reagują już na złe wartości, ale nie potrafią jeszcze zapytać ponownie ani obsłużyć nieudanego odczytu. To przyjdzie razem z powtarzaniem działań.

## Co dalej: Moduł 4

Twoje programy potrafią już **wybrać** działanie. W Module 4, „Powtarzanie działań”, nauczą się wykonywać działania **wielokrotnie**. Moduł 4 jest w przygotowaniu.

**Poprzednia lekcja:** [Lekcja 3.5: Sprawdzanie danych przed obliczeniami](lesson_05_check_before_calculating.md) · **Następna lekcja:** w przygotowaniu · [Opis kursu](../../README.md)

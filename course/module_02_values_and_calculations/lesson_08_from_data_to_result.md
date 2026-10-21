# Lekcja 2.8: Od danych do wyniku (sprawdzian Modułu 2)

**Polski** · [English](lesson_08_from_data_to_result.en.md) · [Opis kursu](../../README.md)

> **Moduł 2, lekcja 8: sprawdzian** · około 90 minut, można go podzielić na dwa podejścia
> **Potrzebujesz:** katalogu `cpp-workspace` z repozytorium Gita z lekcji 1.5 i oryginalnego projektu `lesson_05_first_program`.
> **Wersja pilotażowa.** Rozwiązania referencyjne z tej lekcji sprawdzamy automatycznie na Windowsie, Ubuntu i macOS, z podanymi danymi wejściowymi. Twojej pracy nic nie ocenia automatycznie: sprawdzasz ją samodzielnie, według kryteriów.

## Jak przebiega ten sprawdzian

Ta lekcja nie wprowadza niczego nowego. Sprawdzasz, czy potrafisz samodzielnie zaprojektować program, który pobiera dane od użytkownika, przechowuje je w dobrze dobranych zmiennych, liczy i wypisuje wynik. Do tego diagnozujesz dwa krótkie zgłoszenia i wyjaśniasz własne decyzje.

Lekcja ma dwie części:

- **Część A: sprawdzian.** Wymagania, dane testowe, oczekiwane wyniki, pytania i kryteria. Bez podpowiedzi i bez kodu rozwiązań. Wszystko, czego potrzebujesz, znasz z lekcji 2.1–2.7 i z Modułu 1.
- **Część B: sprawdzenie i omówienie.** Sposób sprawdzenia, podpowiedzi, przykładowe rozwiązania, wyjaśnienia i samoocena. Przejdź do niej po wykonaniu części A albo wtedy, gdy świadomie zrezygnujesz z dalszej samodzielnej próby.

Zajrzenie do części B, do wcześniejszych lekcji albo do swoich notatek nie jest porażką. Ważne jest tylko to, żeby **uczciwie zanotować, co zrobiono samodzielnie, a co z pomocą**. Samoocena na końcu to rozróżnia. Sprawdzian możesz podzielić na dwa podejścia, na przykład zadanie 1 jednego dnia, a zadania 2 i 3 następnego.

**Możesz używać:**

- CLiona albo terminala, CMake i Ninja, jak dotąd;
- `CMakeLists.txt` skopiowanego z oryginalnego `lesson_05_first_program`;
- debuggera z lekcji 2.3, jeśli działa w Twoim środowisku, albo tabeli wartości i tymczasowych instrukcji `std::cout`;
- Gita, jeśli chcesz zapisać gotową pracę.

We wszystkich zadaniach zakładamy **poprawne dane wejściowe**, takie jak podane. Programy nie muszą sprawdzać danych ani reagować na błędne.

---

# Część A: sprawdzian

## Zadanie 1: Plan trasy

Organizatorzy przygotowują trasę spacerową. Do oznaczenia trasy używają znaczników, które pakuje się **po 6 sztuk**. Napisz program, który pomoże im zaplanować trasę.

**Przygotowanie:**

- W `cpp-workspace` utwórz nowy katalog `route_plan`.
- Skopiuj do niego `CMakeLists.txt` z oryginalnego `lesson_05_first_program`.
- Utwórz w nim **pusty** `main.cpp` i napisz cały program samodzielnie. Nie kopiuj programów z wcześniejszych lekcji.

**Dane wejściowe**, w tej kolejności, każda wartość w osobnej linijce:

1. nazwa trasy, która może zawierać spacje;
2. liczba okrążeń, liczba całkowita;
3. długość jednego okrążenia w kilometrach, liczba z częścią ułamkową;
4. liczba dostępnych znaczników, liczba całkowita.

**Program oblicza:**

- całkowity dystans: liczba okrążeń razy długość okrążenia;
- liczbę pełnych paczek po 6 znaczników, które da się przygotować z dostępnych znaczników;
- liczbę znaczników, które zostaną poza pełnymi paczkami.

**Wymagania:**

- Przed każdym odczytem program wypisuje prośbę o dane, a na końcu raport, dokładnie jak w przykładach poniżej.
- Liczba znaczników w paczce, 6, jest w programie stałą `const int`.
- Pierwsza linijka raportu, `Route: …`, jest tekstem **zbudowanym przez łączenie** wartości `std::string` i zapisanym w zmiennej, zanim program go wypisze.
- Ten sam program, bez zmiany kodu i bez ponownego budowania, daje poprawny wynik dla obu zestawów danych.

**Pierwszy zestaw danych:**

<!-- input: route_plan -->
```text
Forest Loop
4
1.25
29
```

Standardowe wyjście ma być dokładnie takie:

<!-- output: route_plan -->
```text
Enter route name:
Enter number of laps:
Enter lap length in km:
Enter number of markers:
Route: Forest Loop
Total distance: 5 km
Full marker packs: 4
Markers left: 5
```

**Drugi zestaw danych,** w drugim uruchomieniu tego samego programu:

<!-- input: route_plan -->
```text
City Evening Walk
3
2.5
30
```

<!-- output: route_plan -->
```text
Enter route name:
Enter number of laps:
Enter lap length in km:
Enter number of markers:
Route: City Evening Walk
Total distance: 7.5 km
Full marker packs: 5
Markers left: 0
```

Na ekranie zobaczysz między linijkami programu także wpisane dane: to echo, a nie standardowe wyjście (lekcja 2.6). Dystans 5.0 km program wypisuje jako `5` (lekcja 2.5).

Gdy wynik się zgadza, możesz zapisać projekt w Gicie, jak w lekcji 1.5. Przed commitem sprawdź `git status`: do historii trafiają tylko `main.cpp` i `CMakeLists.txt`, bez katalogów budowania.

## Zadanie 2: Dwa zgłoszenia

W `cpp-workspace` utwórz katalog `diagnosis_2`, skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program`. Każdy z poniższych programów wpisz po kolei w `main.cpp` tego katalogu. Oba się budują i działają, ale dają zły wynik.

**Zgłoszenie A.** Program ma wypisać pełną nazwę wydarzenia, którą poda użytkownik:

<!-- example: event_name_bug -->
```cpp
#include <iostream>
#include <string>

int main() {
    std::string event_name{""};

    std::cout << "Enter event name:\n";
    std::cin >> event_name;

    std::cout << "Event: " << event_name << "\n";
}
```

Dla tych danych:

<!-- input: event_name_fixed -->
```text
Spring Science Fair
```

standardowe wyjście ma być takie:

<!-- output: event_name_fixed -->
```text
Enter event name:
Event: Spring Science Fair
```

**Zgłoszenie B.** Program ma zamienić liczbę minut na pełne godziny i pozostałe minuty:

<!-- example: time_bug -->
```cpp
#include <iostream>

int main() {
    const int minutes_per_hour{60};
    int total_minutes{0};

    std::cout << "Enter total minutes:\n";
    std::cin >> total_minutes;

    const int hours{total_minutes % minutes_per_hour};
    const int minutes{total_minutes % minutes_per_hour};

    std::cout << "Time: " << hours << " h " << minutes << " min\n";
}
```

Dane testowe to `135` i `200`. **Przewidź** poprawny wynik dla obu, a dopiero potem porównaj go z oczekiwanym:

<!-- input: time_fixed -->
```text
135
```

<details>
<summary>Oczekiwane standardowe wyjście dla 135</summary>

<!-- output: time_fixed -->
```text
Enter total minutes:
Time: 2 h 15 min
```

</details>

<!-- input: time_fixed -->
```text
200
```

<details>
<summary>Oczekiwane standardowe wyjście dla 200</summary>

<!-- output: time_fixed -->
```text
Enter total minutes:
Time: 3 h 20 min
```

</details>

**Dla każdego zgłoszenia:**

1. Uruchom program z podanymi danymi i zapisz, co naprawdę wypisuje.
2. Porównaj to z oczekiwanym wynikiem.
3. Znajdź instrukcję, która daje zły wynik. Możesz użyć debuggera, jeśli działa u Ciebie od lekcji 2.3, albo tabeli wartości i tymczasowych instrukcji `std::cout`.
4. Wyjaśnij przyczynę jednym zdaniem.
5. Popraw program jedną zmianą.
6. Sprawdź, że po poprawce wynik jest taki jak oczekiwany. Usuń tymczasowe instrukcje `std::cout`, jeśli je dopisano.

Zapisz wyniki w tabeli:

| Zgłoszenie | Rzeczywisty wynik | Instrukcja, która daje zły wynik | Przyczyna | Poprawka | Sprawdzenie |
|---|---|---|---|---|---|
| A | | | | | |
| B | | | | | |

Projektu `diagnosis_2` nie musisz zapisywać w Gicie.

## Zadanie 3: Wyjaśnij

Odpowiedz krótko, na piśmie, odwołując się do własnego programu z zadania 1:

1. Dlaczego nazwa trasy jest przechowywana w `std::string`?
2. Dlaczego nazwę trasy odczytujesz przez `std::getline`, a nie przez `>>`? Dlaczego ten odczyt stoi przed odczytem liczb?
3. Dlaczego długość okrążenia ma typ `double`, a liczba okrążeń `int`?
4. Dlaczego do obliczenia pełnych paczek i pozostałych znaczników nadają się `/` oraz `%`?
5. Dlaczego liczba znaczników w paczce może być `const`, a liczba dostępnych znaczników nie?
6. Jaki typ miałaby zmienna zainicjalizowana przez `auto` wyrażeniem, które w Twoim programie oblicza całkowity dystans? Skąd to wiadomo?
7. Dlaczego ten sam program daje różne wyniki dla dwóch zestawów danych, bez ponownego budowania?

## Kryteria sukcesu

Sprawdzian jest zaliczony, gdy spełniasz **wszystkie** kryteria:

- `route_plan/main.cpp` napisano od pustego pliku, w poprawnym C++20. Program buduje się bez błędów.
- Typy danych wynikają z ich znaczenia: tekst w `std::string`, liczby całkowite w `int`, wielkość z częścią ułamkową w `double`. Każda zmienna ma wartość początkową.
- Nazwa trasy ze spacjami jest odczytywana w całości przez `std::getline`, **przed** odczytem liczb przez `>>`.
- Całkowity dystans jest obliczany z udziałem `double`, a pełne paczki i pozostałe znaczniki przez `/` i `%`.
- Liczba znaczników w paczce to stała `const int`. Wartości, które po obliczeniu się nie zmieniają, też mogą być stałymi.
- Pierwsza linijka raportu jest tekstem zbudowanym przez łączenie `std::string` i zapisanym w zmiennej.
- Standardowe wyjście dla **obu** zestawów danych jest dokładnie takie jak w zadaniu 1, a między uruchomieniami kod się nie zmienia.
- Oba zgłoszenia z zadania 2 zdiagnozowano i poprawiono: rzeczywisty wynik, instrukcja, przyczyna, jedna poprawka i sprawdzenie.
- Umiesz wyjaśnić każdą linijkę swojego programu i odpowiedzieć na pytania z zadania 3.

Nazwy zmiennych mogą być inne niż w przykładowym rozwiązaniu, jeśli są czytelne i mówią, co oznacza wartość. Poprawny wynik to warunek konieczny, ale **nie dowód zrozumienia**: program może działać, choć ktoś nie rozumie, dlaczego. Dlatego zadanie 3 jest częścią sprawdzianu.

---

# Część B: sprawdzenie i omówienie

Przejdź tutaj po wykonaniu części A albo wtedy, gdy świadomie zrezygnujesz z dalszej samodzielnej próby.

## Jak sprawdzić swoją pracę

- **Standardowe wyjście:** uruchom program dwa razy, raz z każdym zestawem danych. Porównaj linijki programu z oczekiwanymi znak po znaku. Pomiń wpisane przez siebie dane, które widać dzięki echu.
- **Ten sam program:** między uruchomieniami nie zmieniaj kodu. W terminalu możesz uruchomić dwa razy ten sam plik wykonywalny, jak w lekcji 2.6, punkt 3.
- **Obliczenia ręcznie:** 4 · 1.25 = 5 i 3 · 2.5 = 7.5. 29 znaczników to 4 paczki po 6 (24) i 5 reszty. 30 to 5 paczek i 0 reszty.
- **Typy i kolejność odczytów:** przejrzyj deklaracje. Przy każdej zmiennej powiedz, dlaczego ma taki typ i czy może mieć `const`.
- **Git, jeśli zapisano pracę:** `git status` nie pokazuje plików `route_plan`, a `git ls-files route_plan` pokazuje tylko `CMakeLists.txt` i `main.cpp`.

## Podpowiedzi

Każda podpowiedź dotyczy sposobu myślenia. Rozwijaj je po kolei i tylko wtedy, gdy ich potrzebujesz.

<details>
<summary>Zadanie 1, podpowiedź 1: od czego zacząć?</summary>

Od listy danych i ich typów: co jest tekstem, co liczbą całkowitą, a co liczbą z częścią ułamkową? Potem kolejność jak w lekcjach 2.6 i 2.7: zmienne na dane, dla każdej wartości prośba i odczyt, na końcu obliczenia i raport.

</details>

<details>
<summary>Zadanie 1, podpowiedź 2: odczyty</summary>

Nazwa trasy ma spacje, więc `>>` odczytałoby tylko jej pierwsze słowo. Która metoda odczytuje całą linijkę i dlaczego musi być pierwsza (lekcja 2.7, punkt 8)?

</details>

<details>
<summary>Zadanie 1, podpowiedź 3: obliczenia</summary>

Dystans: `int` razy `double` daje `double` (lekcja 2.5), więc typ wyniku musi pasować do `{}`. Paczki: „ile pełnych grup?” i „ile zostanie?” to pytania o `/` i `%` (lekcja 2.4). Tekst `Route: …` zbuduj przez `+` z literału i nazwy trasy (lekcja 2.7).

</details>

<details>
<summary>Zadanie 2, zgłoszenie A</summary>

Porównaj rzeczywisty wynik z oczekiwanym: której części nazwy brakuje? Czym kończy się odczyt przez `>>` do `std::string`?

</details>

<details>
<summary>Zadanie 2, zgłoszenie B</summary>

Przy 135 minutach liczba godzin i liczba minut są takie same. Które z dwóch obliczeń daje liczbę pełnych grup, a które resztę?

</details>

## Przykładowe rozwiązania

<details>
<summary>Zadanie 1: plan trasy</summary>

<!-- example: route_plan -->
```cpp
#include <iostream>
#include <string>

int main() {
    const int markers_per_pack{6};

    std::string route_name{""};
    int laps{0};
    double lap_length_km{0.0};
    int markers{0};

    std::cout << "Enter route name:\n";
    std::getline(std::cin, route_name);
    std::cout << "Enter number of laps:\n";
    std::cin >> laps;
    std::cout << "Enter lap length in km:\n";
    std::cin >> lap_length_km;
    std::cout << "Enter number of markers:\n";
    std::cin >> markers;

    const double total_distance_km{laps * lap_length_km};
    const int full_packs{markers / markers_per_pack};
    const int markers_left{markers % markers_per_pack};
    const std::string title{"Route: " + route_name};

    std::cout << title << "\n";
    std::cout << "Total distance: " << total_distance_km << " km\n";
    std::cout << "Full marker packs: " << full_packs << "\n";
    std::cout << "Markers left: " << markers_left << "\n";
}
```

- **Typy:** nazwa trasy to tekst ze spacjami, więc `std::string`. Okrążenia i znaczniki liczy się w całości, więc `int`. Długość okrążenia może mieć część ułamkową, więc `double`. Zmienne na dane mają wartości początkowe i nie mają `const`, bo odczyt je zmienia.
- **Odczyty:** `std::getline` stoi pierwszy, więc nazwa jest odczytana w całości, a kolejne `>>` nie mają problemu z końcem linijki.
- **Obliczenia:** `laps * lap_length_km` to `int` razy `double`, więc wynik jest `double` i pasuje do `const double`. `markers / markers_per_pack` i `markers % markers_per_pack` to dzielenie całkowite i reszta: pełne paczki i to, co zostanie. Obliczenia stoją po odczytach i się nie zmieniają, więc są stałymi.
- **Tekst:** `"Route: " + route_name` to literał plus `std::string`, więc wynik jest tekstem `std::string`, zapisanym w stałej `title`.

</details>

<details>
<summary>Zadanie 2, zgłoszenie A: wynik przed poprawką i poprawiony program</summary>

Przed poprawką, dla tych samych danych:

<!-- input: event_name_bug -->
```text
Spring Science Fair
```

<!-- output: event_name_bug -->
```text
Enter event name:
Event: Spring
```

- **Instrukcja:** `std::cin >> event_name;`.
- **Przyczyna:** `>>` odczytuje do `std::string` jedno słowo i kończy na spacji. `std::string` mieści spacje, ale ta metoda odczytu ich nie przenosi.
- **Poprawka:** odczytaj całą linijkę przez `std::getline`:

<!-- example: event_name_fixed -->
```cpp
#include <iostream>
#include <string>

int main() {
    std::string event_name{""};

    std::cout << "Enter event name:\n";
    std::getline(std::cin, event_name);

    std::cout << "Event: " << event_name << "\n";
}
```

</details>

<details>
<summary>Zadanie 2, zgłoszenie B: wynik przed poprawką i poprawiony program</summary>

Przed poprawką:

<!-- input: time_bug -->
```text
135
```

<!-- output: time_bug -->
```text
Enter total minutes:
Time: 15 h 15 min
```

<!-- input: time_bug -->
```text
200
```

<!-- output: time_bug -->
```text
Enter total minutes:
Time: 20 h 20 min
```

- **Instrukcja:** `const int hours{total_minutes % minutes_per_hour};`.
- **Przyczyna:** godziny to liczba pełnych grup po 60 minut, czyli dzielenie całkowite `/`. `%` daje resztę, a reszta to minuty, więc obie wartości wychodzą takie same. Tabela wartości albo `std::cout` po tej instrukcji pokazuje 15 zamiast oczekiwanych 2.
- **Poprawka:** w obliczeniu godzin zamień `%` na `/`:

<!-- example: time_fixed -->
```cpp
#include <iostream>

int main() {
    const int minutes_per_hour{60};
    int total_minutes{0};

    std::cout << "Enter total minutes:\n";
    std::cin >> total_minutes;

    const int hours{total_minutes / minutes_per_hour};
    const int minutes{total_minutes % minutes_per_hour};

    std::cout << "Time: " << hours << " h " << minutes << " min\n";
}
```

Sprawdzenie: 2 · 60 + 15 = 135 i 3 · 60 + 20 = 200.

</details>

## Przykładowe odpowiedzi do zadania 3

<details>
<summary>Pokaż przykładowe odpowiedzi</summary>

1. Bo nazwa trasy to tekst, który może składać się z kilku słów. `int` i `double` przechowują tylko liczby.
2. Bo `>>` odczytałoby tylko pierwsze słowo, a `std::getline` odczytuje całą linijkę ze spacjami. Stoi przed odczytami liczb, bo po `>>` w wejściu zostaje koniec linijki, a `std::getline` wywołane później mogłoby odczytać pusty tekst.
3. Bo długość okrążenia to pomiar, który może mieć część ułamkową, na przykład 1.25 km. Okrążeń jest zawsze całkowita liczba.
4. Bo `/` na dwóch liczbach całkowitych daje liczbę pełnych grup po 6, a `%` resztę, czyli znaczniki, które się do żadnej pełnej paczki nie zmieszczą.
5. Bo paczka ma zawsze 6 znaczników: ta wartość nie zmienia się w trakcie działania programu, a `const` pilnuje, żeby nic jej przez pomyłkę nie zmieniło. Liczbę dostępnych znaczników program odczytuje od użytkownika, więc musi być zwykłą zmienną.
6. `double`, bo wyrażenie to liczba okrążeń (`int`) razy długość okrążenia (`double`), a `int` razy `double` daje `double`. `auto` ustala typ z wartości początkowej.
7. Bo dane nie są zapisane w kodzie: program odczytuje je przy każdym uruchomieniu ze standardowego wejścia. Zmieniają się dane, a kod i plik wykonywalny zostają takie same.

</details>

## Samoocena

Przy każdym kryterium zaznacz jedną odpowiedź:

| Kryterium | Samodzielnie | Z podpowiedzią | Po zajrzeniu do rozwiązania | Do powtórki |
|---|---|---|---|---|
| Napisanie programu od pustego `main.cpp` | | | | |
| Dobór typów: `std::string`, `int`, `double` | | | | |
| Odczyt nazwy ze spacjami i kolejność `std::getline` przed `>>` | | | | |
| Obliczenie dystansu z `double` | | | | |
| Pełne paczki i reszta przez `/` i `%` | | | | |
| `const` dla wartości, które się nie zmieniają | | | | |
| Tekst zbudowany przez łączenie `std::string` | | | | |
| Dokładny wynik dla obu zestawów danych, bez zmiany kodu | | | | |
| Diagnoza zgłoszenia A | | | | |
| Diagnoza zgłoszenia B | | | | |
| Szukanie błędu tabelą wartości i tymczasowym `std::cout` | | | | |
| Obsługa debuggera w CLionie (breakpoint, Step Over) | | | | |
| Wyjaśnienia z zadania 3 | | | | |

Wiersz o debuggerze dotyczy **narzędzia**, a wiersz o tabeli wartości i `std::cout` **techniki szukania błędu**. Obie umiejętności się uzupełniają, ale nie zastępują. Jeśli debugger nie działa w Twoim środowisku, zostaw jego wiersz pusty i wróć do lekcji 2.3, gdy zacznie działać.

Jeśli w kolumnie „Do powtórki” jest coś zaznaczone, wróć do odpowiedniej lekcji:

| Temat | Lekcja |
|---|---|
| zmienne, wartości początkowe i obliczenia | 2.1 |
| przypisanie, `const`, tabela wartości | 2.2 |
| debugger i śledzenie wartości przez `std::cout` | 2.3 |
| `/`, `%` i kolejność działań | 2.4 |
| `double`, mieszanie `int` i `double`, `auto` | 2.5 |
| `std::cin`, standardowe wejście i echo | 2.6 |
| `std::string`, łączenie tekstu, `std::getline` | 2.7 |

Potem spróbuj zadania jeszcze raz, na przykład z innymi danymi trasy.

---

## Podsumowanie Modułu 2

Po ośmiu lekcjach potrafisz:

- przechowywać wartości w zmiennych o dobranych typach i zmieniać je przypisaniem podczas działania programu;
- oznaczać `const` wartości, które mają się nie zmieniać;
- wykonywać obliczenia i przewidywać kolejność działań;
- odróżniać dzielenie całkowite od zmiennoprzecinkowego i używać `/` oraz `%`;
- czytać i stosować `auto` w prostych deklaracjach;
- pobierać dane od użytkownika i uruchamiać ten sam program z różnymi danymi;
- przechowywać i łączyć tekst oraz odczytywać całe linijki;
- analizować przebieg programu tabelą wartości, wypisywaniem albo debuggerem i znajdować proste błędy logiczne.

O stanie materiałów: kod i obliczenia ze wszystkich lekcji Modułu 2 są sprawdzane automatycznie na trzech systemach. Instrukcja obsługi debuggera w CLionie pozostaje pilotażowa: nie została jeszcze ręcznie sprawdzona na wszystkich trzech systemach.

## Co dalej: Moduł 3

Twoje programy wykonują na razie zawsze te same instrukcje, od góry do dołu. W Module 3 zaczną **podejmować decyzje**: poznasz porównania i warunki, dzięki którym program wykona różne instrukcje w zależności od danych. Moduł 3 jest w przygotowaniu.

**Poprzednia lekcja:** [Lekcja 2.7: Tekst, który program pamięta (`std::string`)](lesson_07_text_the_program_remembers.md) · **Następna lekcja:** w przygotowaniu · [Opis kursu](../../README.md)

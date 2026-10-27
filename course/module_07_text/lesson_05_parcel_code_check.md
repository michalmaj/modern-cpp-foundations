# Lekcja 7.5: Kontrola kodów paczek (sprawdzian Modułu 7)

**Polski** · [English](lesson_05_parcel_code_check.en.md) · [Opis kursu](../../README.md)

> **Moduł 7, lekcja 5: sprawdzian** · około 95–115 minut, w dwóch podejściach
> **Potrzebujesz:** katalogu `cpp-workspace` i oryginalnego projektu `lesson_05_first_program`.
> **Wersja pilotażowa.** Rozwiązania referencyjne z tej lekcji sprawdzamy automatycznie na Windowsie, Ubuntu i macOS, z podanymi danymi wejściowymi. Twojej pracy nic nie ocenia automatycznie: sprawdzasz ją samodzielnie, według kryteriów. Wpisywanie danych w oknie **Run** CLiona opisujemy bez ręcznego sprawdzenia na każdym systemie.

## Jak przebiega ten sprawdzian

Ta lekcja nie wprowadza niczego nowego. Sprawdzasz, czy potrafisz samodzielnie zaprojektować program, który **odczytuje kolejne teksty, przekształca je i sprawdza ich format**, a potem buduje raport z wyników współpracujących funkcji. Do tego analizujesz dwa krótkie problemy z kodem i wyjaśniasz swoje decyzje.

Lekcja ma dwie części:

- **Część A: sprawdzian.** Wymagania, przykłady, zadania, pytania i kryteria. Bez podpowiedzi i bez kodu rozwiązań. Wszystko, czego potrzebujesz, znasz z Modułów 1–7.
- **Część B: sprawdzenie i omówienie.** Podpowiedzi, pełna lista przypadków kontrolnych, rozwiązanie referencyjne, poprawki, odpowiedzi i samoocena. Przejdź do niej po wykonaniu części A albo wtedy, gdy świadomie zrezygnujesz z dalszej samodzielnej próby.

Zajrzenie do części B, do wcześniejszych lekcji albo do notatek nie jest porażką. Ważne jest, żeby **uczciwie zanotować, co zrobiono samodzielnie, a co z pomocą**. Proponowany podział na dwa podejścia:

- **pierwsze:** analiza wymagań, projekt obu funkcji, ich napisanie i sprawdzenie wydrukami testowymi, połączenie z pętlą odczytu;
- **drugie:** przypadki graniczne, pełny raport, pusta linia i linia ze spacjami, zadanie 2, porównanie z rozwiązaniem, zadanie 3 i samoocena.

**Możesz używać:** CLiona albo terminala, CMake i Ninja, jak dotąd; `CMakeLists.txt` skopiowanego z oryginalnego `lesson_05_first_program`; tabel przypadków i przebiegu oraz tymczasowych wydruków testowych. Debugger nie jest potrzebny. Nie musisz kończyć danych z klawiatury: przypadki, w których dane kończą się bez pustej linii, analizujesz na papierze.

---

# Część A: sprawdzian

## Zadanie 1: Kontrola kodów paczek

Punkt odbioru paczek dostaje kolejne zgłoszenia. Każda niepusta linia zawiera jeden kod paczki, wpisany przez człowieka, czasem ze spacjami: `A B - 1 2 3 4` zamiast `AB-1234`. Program usuwa z każdego kodu spacje, sprawdza, czy to, co zostało, ma wymagany format, i przygotowuje raport. Sprawdza tylko budowę tekstu, a nie to, czy paczka naprawdę istnieje.

**Przygotowanie:** w `cpp-workspace` utwórz katalog `parcel_codes`, skopiuj do niego `CMakeLists.txt` z oryginalnego `lesson_05_first_program`, utwórz **pusty** `main.cpp` i napisz cały program samodzielnie.

### Format kodu

Po usunięciu spacji poprawny kod ma **dokładnie siedem znaków**: dwie wielkie litery, myślnik i cztery cyfry, na przykład `AB-1234`. Indeksy liczymy od 0, jak w lekcji 7.2:

| Indeks w C++ | Wymaganie |
|---|---|
| 0 | wielka litera od `A` do `Z` |
| 1 | wielka litera od `A` do `Z` |
| 2 | myślnik `-` |
| 3 | cyfra od `0` do `9` |
| 4 | cyfra od `0` do `9` |
| 5 | cyfra od `0` do `9` |
| 6 | cyfra od `0` do `9` |

- Poprawne są na przykład `AB-1234`, `AA-0000`, `ZZ-9999` i `BC-0102`. Litery mogą się powtarzać, a cyfry mogą zaczynać się od zera.
- **Wielkość liter ma znaczenie.** Program nie zamienia małych liter na wielkie, więc `Ab-1234` i `ab-1234` są niepoprawne.
- Cztery cyfry to cztery znaki, a nie liczba: sprawdzasz tylko, czy każdy z nich jest cyfrą i czy stoi na swoim miejscu.

### Dane wejściowe

- Program odczytuje kolejne linie przez `std::getline`. Nie wypisuje pytań: po uruchomieniu od razu wpisuj kody, każdy w osobnej linii.
- **Każda niepusta linia to jeden kod.** Przed sprawdzeniem formatu program usuwa z kodu **wszystkie** zwykłe spacje, nie tylko te na początku i na końcu. Linie `  AB-1234  `, `A B - 1 2 3 4` i `AA-00 00` dają kody `AB-1234`, `AB-1234` i `AA-0000`, więc wszystkie trzy są poprawne. Oryginalna linia zostaje bez zmian.
- Odczyt kończy się po **pierwszej pustej linii** albo po **nieudanym odczycie**, zwykle na końcu danych. Tego, co stoi po pustej linii, program już nie odczytuje. Ostatnią linię przed końcem danych sprawdza, nawet jeśli nie kończy jej znak końca linii (lekcja 7.4).
- **Jakie dane są możliwe.** Linie zawierają drukowalne znaki ASCII: litery, cyfry, zwykłe spacje i znaki interpunkcyjne, bez tabulatorów i polskich liter. Tych założeń nie musisz sprawdzać. Każdy znak, który nie pasuje do formatu, na przykład `_`, `!` albo mała litera, sprawia, że kod jest niepoprawny.

### Pusta linia a linia ze spacjami

To najważniejsza decyzja w tym programie:

- **Pusta linia** ma długość zero. Kończy odczyt: program nie sprawdza jej jako kodu, nie zwiększa żadnego licznika i wypisuje podsumowanie.
- **Linia z samych spacji**, na przykład z trzech, nie jest pusta. To jedno zgłoszenie: po usunięciu spacji zostaje pusty tekst, który nie ma formatu kodu. Program liczy więc niepoprawny kod i odczytuje następną linię.

O końcu odczytu decyduje zatem **oryginalna linia**, zanim program usunie z niej spacje. Pusty tekst po usunięciu spacji nie kończy odczytu.

### Raport

Dla każdego sprawdzonego kodu program od razu wypisuje jedną linijkę: `Code N: valid` albo `Code N: invalid`. `N` to numer kodu, od 1, nadawany po kolei wszystkim kodom, także niepoprawnym.

Po zakończeniu odczytu wypisuje trzy linijki:

- `Codes processed: N`: liczbę sprawdzonych kodów;
- `Valid codes: N`: liczbę kodów poprawnych;
- `Invalid codes: N`: liczbę kodów niepoprawnych.

Liczba sprawdzonych kodów jest zawsze równa sumie poprawnych i niepoprawnych. Gdy kodów nie było, wszystkie trzy liczby to 0. Program nie wypisuje żadnych innych komunikatów: ani samych kodów, ani informacji o tym, co zakończyło odczyt.

### Funkcje

Program ma co najmniej dwie własne funkcje:

1. funkcję, która z otrzymanego tekstu tworzy **nowy tekst bez spacji**, z pozostałymi znakami w tej samej kolejności, i zwraca go przez wartość; nowy tekst buduje przez `push_back`, jak w lekcji 7.3;
2. funkcję, która dla kodu **już bez spacji** odpowiada, czy ma on wymagany format: zwraca `true` albo `false`.

**Wymagania wobec funkcji:**

- Obie dostają tekst przez `const std::string&`. Niczego nie odczytują, niczego nie wypisują i nie zmieniają przekazanego tekstu.
- **Funkcja sprawdzająca format nie może odczytać znaku spoza tekstu.** Musi działać poprawnie dla każdego tekstu: pustego, jednoznakowego, za krótkiego i za długiego. Znak należący do tekstu ma indeks mniejszy niż `size()` (lekcja 7.2).
- Nazwy funkcji i ich nagłówki zapisujesz samodzielnie: typ wyniku dobierz do zadania funkcji. Możesz dodać własne funkcje pomocnicze, ale nie musisz.

`main` odczytuje linie przez `std::getline` w pętli `while` z flagą `bool`, jak w lekcji 7.4. Rozpoznaje koniec danych, numeruje kody, wywołuje obie funkcje, wypisuje wynik każdego kodu, liczy kody i wypisuje podsumowanie. Algorytmów funkcji nie powtarza. Program nie przechowuje wcześniejszych linii i nie używa zmiennych zadeklarowanych poza funkcjami. Do liczników możesz użyć `std::size_t`.

### Przykłady

**Przykład A:** sześć linii. Piąta składa się z trzech spacji, a szósta jest pusta.

<!-- input: parcel_codes -->
```text
AB-1234
A B - 1 2 3 4
Ab-1234
AB-123
   

```

<!-- output: parcel_codes -->
```text
Code 1: valid
Code 2: valid
Code 3: invalid
Code 4: invalid
Code 5: invalid
Codes processed: 5
Valid codes: 2
Invalid codes: 3
```

Kod 2 po usunięciu spacji to `AB-1234`. W kodzie 3 druga litera jest mała, kod 4 ma tylko trzy cyfry, a z linii 5 po usunięciu spacji nic nie zostaje. Pusta szósta linia kończy odczyt.

**Przykład B:** pierwsza linia jest pusta. To pusta linia, a nie brak danych.

<!-- input: parcel_codes -->
```text

```

<!-- output: parcel_codes -->
```text
Codes processed: 0
Valid codes: 0
Invalid codes: 0
```

**Przykład C:** linia z trzech spacji, a potem pusta linia.

<!-- input: parcel_codes -->
```text
   

```

<!-- output: parcel_codes -->
```text
Code 1: invalid
Codes processed: 1
Valid codes: 0
Invalid codes: 1
```

**Przykład D:** `AB-1234`, pusta linia i `ZZ-9999`. **Przewidź** raport, zanim napiszesz program.

<!-- input: parcel_codes -->
```text
AB-1234

ZZ-9999
```

<details>
<summary>Standardowe wyjście dla przykładu D</summary>

<!-- output: parcel_codes -->
```text
Code 1: valid
Codes processed: 1
Valid codes: 1
Invalid codes: 0
```

`ZZ-9999` ma poprawny format, ale stoi po pustej linii, więc program go nie odczytuje. Poprawność kodu nie ma znaczenia, gdy linia jest już poza zakresem przetwarzania.

</details>

### Jak pracować

1. **Zaprojektuj obie funkcje, zanim zaczniesz pisać `main`.** Przy każdej zapisz jednym zdaniem jej zadanie, parametr i typ wyniku.
2. **Przygotuj tabelę przypadków:** poprawne kody z `A`, `Z`, `0` i `9`; spacje na początku, na końcu i w środku; mała litera; cyfra zamiast litery; inny znak zamiast myślnika; litera wśród cyfr; za krótki i za długi kod; sam myślnik; same spacje; pusta linia jako pierwsza; kod po pustej linii; dane, które kończą się bez pustej linii. Przy każdym zapisz oczekiwany wynik.
3. **Sprawdź każdą funkcję osobno** wydrukami testowymi z lekcji 5.5, z tekstami wpisanymi w kodzie:
   - usuwanie spacji: spacje w różnych miejscach, same spacje i pusty tekst, z wynikiem w nawiasach kwadratowych, żeby było widać spacje;
   - sprawdzanie formatu: kilka poprawnych kodów, kody z błędem na różnych pozycjach, za krótkie, za długie i pusty tekst. Wartości `bool` wypisują się jako `1` albo `0`.
4. **Usuń wydruki testowe** i połącz funkcje z pętlą odczytu.
5. **Uruchom cały program** dla przykładów A, B i C oraz dla 1–2 innych przypadków z tabeli. Każdą linię kończ klawiszem **Enter**, a pustą linię wpisz samym **Enter**. Wpisywane linie mieszają się w terminalu z raportem, bo program odpowiada zaraz po każdej linii. Przypadki, w których dane kończą się bez pustej linii, przeanalizuj na papierze. Wszystkie przypadki z pełnej listy kontrolnej są sprawdzone automatycznie.

Gdy wynik się zgadza, możesz zapisać projekt w Gicie, jak w lekcji 1.5. Przed commitem sprawdź `git status`: do historii trafiają tylko `main.cpp` i `CMakeLists.txt`.

## Zadanie 2: Diagnostyka

Wykonaj to zadanie **po zadaniu 1**: oba problemy dotyczą funkcji podobnej do Twojej funkcji sprawdzającej format.

<details>
<summary>Diagnostyka A: granica zakresu liter</summary>

W `cpp-workspace` utwórz katalog `diagnosis_7`, skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program` i umieść w `main.cpp` program poniżej: możesz go przepisać albo skopiować. Program sprawdza funkcję dwoma testami wpisanymi w kodzie, tak jak Twoje wydruki testowe. Wymaganie: na indeksach 0 i 1 stoją wielkie litery od `A` do `Z`, **włącznie** z `A` i `Z`.

<!-- example: letter_range_bug -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>

bool is_valid_code(const std::string& code) {
    if (code.size() != 7) {
        return false;
    }

    const bool first_is_capital{code[0] > 'A' && code[0] <= 'Z'};
    const bool second_is_capital{code[1] >= 'A' && code[1] <= 'Z'};
    const bool has_hyphen{code[2] == '-'};
    bool all_digits{true};

    for (std::size_t index{3}; index < code.size(); ++index) {
        const bool is_digit{code[index] >= '0' && code[index] <= '9'};

        if (!is_digit) {
            all_digits = false;
        }
    }

    return first_is_capital && second_is_capital && has_hyphen && all_digits;
}

int main() {
    const std::string first_test{"BC-1234"};
    const std::string second_test{"AB-1234"};

    std::cout << "Test BC-1234: " << is_valid_code(first_test) << "\n";
    std::cout << "Test AB-1234: " << is_valid_code(second_test) << "\n";
}
```

1. **Przewidź** wynik obu testów. Oba kody są poprawne według wymagań.
2. Uruchom program. Który test daje wynik zgodny z wymaganiami, a który nie?
3. Dlaczego test `BC-1234` nie ujawnia błędu?
4. Znajdź warunek, który odrzuca `AB-1234`, i wskaż w nim błędną granicę zakresu.
5. Popraw warunek.
6. Dopisz test kodu `AA-0000` i uruchom program ponownie.
7. Dopisz test kodu `aB-1234`: mała litera na poprawionej pozycji nadal musi dawać `0`.

</details>

<details>
<summary>Diagnostyka B: indeks przed sprawdzeniem długości</summary>

Ten fragment **tylko analizujesz na papierze**: nie uruchamiaj go. To początek innej wersji funkcji sprawdzającej format:

<!-- fragment -->
```cpp
bool is_valid_code(const std::string& code) {
    const bool has_hyphen{code[2] == '-'};
    const bool last_is_digit{code[6] >= '0' && code[6] <= '9'};

    if (code.size() != 7) {
        return false;
    }

    // ...the other positions, then the result
}
```

Rozważ wywołanie tej funkcji dla tekstu `"AB-"`:

1. Ile znaków ma ten tekst?
2. Jakie indeksy mają jego znaki?
3. Dlaczego odczyt `code[6]` jest tu nieprawidłowy?
4. Czy da się przewidzieć, co zrobi program z takim odczytem?
5. Jakie sprawdzenie musi stać przed odczytem znaków na konkretnych pozycjach?
6. Dlaczego sprawdzenie długości powinno stać przed sprawdzaniem liter, myślnika i cyfr?

</details>

Wyniki, poprawki i odpowiedzi są w części B, w sekcji [Diagnostyka: wyniki i poprawki](#diagnostyka-wyniki-i-poprawki).

## Zadanie 3: Wyjaśnij swój projekt

Odpowiedz krótko, na piśmie, odwołując się do własnego programu z zadania 1:

1. Dlaczego Twój program sprawdza, czy linia jest pusta, zanim usunie z niej spacje? Dlaczego linia z samych spacji jest niepoprawnym kodem, a nie końcem danych?
2. Dlaczego kod bez spacji jest osobnym `std::string`, a oryginalna linia zostaje bez zmian?
3. Dlaczego funkcja usuwająca spacje zwraca tekst, a funkcja sprawdzająca format zwraca `bool`?
4. Dlaczego Twoja funkcja sprawdzająca format zna długość kodu, zanim odczyta jakikolwiek znak? Dla których kodów z Twojej tabeli ta kolejność ma znaczenie?
5. Dlaczego program nie musi przechowywać wszystkich kodów?
6. Czy to, że liczba sprawdzonych kodów jest równa sumie poprawnych i niepoprawnych, dowodzi, że każdy kod został oceniony poprawnie?

## Kryteria sukcesu

Sprawdzian jest zaliczony, gdy spełniasz **wszystkie** kryteria. Możesz przy tym korzystać z części B, jeśli uczciwie zaznaczysz to w samoocenie.

- `parcel_codes/main.cpp` napisano od pustego pliku, w poprawnym C++20. Program buduje się bez błędów.
- Program odczytuje linie przez `std::getline` w pętli `while` z flagą `bool`, sprawdza powodzenie odczytu przed `empty()` i kończy odczyt po pierwszej pustej linii albo po nieudanym odczycie.
- Są dwie funkcje o zadaniach z wymagań. Obie dostają tekst przez `const std::string&`, niczego nie odczytują ani nie wypisują i nie zmieniają przekazanego tekstu. Typ wyniku każdej z nich pasuje do jej zadania.
- Funkcja usuwająca spacje buduje nowy tekst przez `push_back` i usuwa wszystkie spacje, także ze środka kodu. Funkcja sprawdzająca format nie odczytuje znaku spoza tekstu, także dla pustego tekstu i kodów krótszych niż siedem znaków.
- Linia z samych spacji jest liczona jako niepoprawny kod, a o końcu odczytu decyduje oryginalna linia. Program nie przechowuje wcześniejszych linii.
- Standardowe wyjście dla przykładów A, B i C oraz dla wpisanych przypadków zgadza się z wymaganiami. Przypadki zakończone bez pustej linii zgadzają się z Twoją analizą na papierze i z pełną listą kontrolną.
- Funkcje sprawdzono osobno wydrukami testowymi, a w programie końcowym takich wydruków nie ma.
- Błąd z diagnostyki A poprawiono i sprawdzono, a fragment z diagnostyki B przeanalizowano bez uruchamiania.
- Umiesz wyjaśnić każdą linijkę swojego programu i odpowiedzieć na pytania z zadania 3.

Nazwy funkcji i zmiennych oraz podział programu mogą być inne niż w rozwiązaniu referencyjnym, jeśli są czytelne i spełniają wymagania. Poprawny wynik to warunek konieczny, ale **nie dowód zrozumienia**. Dlatego zadania 2 i 3 są częścią sprawdzianu.

---

# Część B: sprawdzenie i omówienie

Przejdź tutaj po wykonaniu części A albo wtedy, gdy świadomie zrezygnujesz z dalszej samodzielnej próby.

## Jak sprawdzić swoją pracę

- **Standardowe wyjście:** porównaj linijki programu z oczekiwanymi, znak po znaku. Pomiń linie, które wpisujesz: widać je w terminalu, ale nie są częścią standardowego wyjścia programu.
- **Koniec danych:** przypadki zakończone bez pustej linii sprawdź tabelą przebiegu i porównaj z pełną listą kontrolną. Każdy z nich jest tam sprawdzony automatycznie.
- **Funkcje:** czy każda ma zadanie, które da się opisać jednym zdaniem? Czy któryś algorytm stoi też w `main`?
- **Kolejność:** czy o końcu odczytu decyduje oryginalna linia? Czy funkcja sprawdzająca format zna długość kodu, zanim odczyta pierwszy znak?

## Podpowiedzi

<details>
<summary>Podpowiedź 1</summary>

Które zadania programu można wykonać osobnymi funkcjami? Czy usuwanie spacji i sprawdzanie formatu to ta sama odpowiedzialność?

</details>

<details>
<summary>Podpowiedź 2</summary>

Najpierw zdecyduj, czy oryginalna linia kończy odczyt. Jeśli nie, utwórz tekst bez spacji i dopiero na nim sprawdzaj format.

</details>

<details>
<summary>Podpowiedź 3</summary>

Przed odczytem znaków po indeksach sprawdź, czy kod ma dokładnie siedem znaków. Następnie zbadaj dwa miejsca na wielkie litery, jedno na myślnik i cztery na cyfry.

</details>

## Pełna lista przypadków kontrolnych

<details>
<summary>Otwórz po przygotowaniu własnej tabeli</summary>

Przykłady A–D są sprawdzone w części A. Wszystkie przypadki poniżej są sprawdzone automatycznie, rozwiązaniem referencyjnym, które samo odczytuje dane z wejścia. Każdy przypadek to osobne uruchomienie programu.

**Poprawne kody**, wszystkie w jednym wejściu, w przypadku E:

| Linia | Kod bez spacji | Co sprawdza |
|---|---|---|
| `AB-1234` | `AB-1234` | zwykły poprawny kod |
| `AA-0000` | `AA-0000` | dwa razy `A`, same zera |
| `ZZ-9999` | `ZZ-9999` | dwa razy `Z`, same dziewiątki |
| `BC-0102` | `BC-0102` | zero na początku części cyfrowej |
| `  AB-1234  ` | `AB-1234` | po dwie spacje na początku i na końcu |
| `A B - 1 2 3 4` | `AB-1234` | spacje między wszystkimi znakami |
| `AA-00 00` | `AA-0000` | spacja wśród cyfr |

**Niepoprawne kody**, wszystkie w jednym wejściu, w przypadku F:

| Linia | Dlaczego niepoprawny |
|---|---|
| `Ab-1234` | mała litera na indeksie 1 |
| `ab-1234` | dwie małe litery |
| `aB-1234` | mała litera na indeksie 0 |
| `A1-1234` | cyfra zamiast drugiej litery |
| `AB_1234` | `_` zamiast myślnika |
| `AB-123` | za krótki: 6 znaków |
| `AB-12345` | za długi: 8 znaków |
| `AB-A234` | litera na indeksie 3, pierwszym z cyfr |
| `AB-12A4` | litera wśród cyfr, na indeksie 5 |
| `AB-123A` | litera na indeksie 6, ostatnim |
| `AB-1234!` | dodatkowy znak: 8 znaków |
| `-` | jeden znak |
| trzy spacje | po usunięciu spacji zostaje pusty tekst |

**Przebieg wielu linii:**

| | Wejście | Wyniki kodów | Sprawdzone, poprawne, niepoprawne | Co sprawdza |
|---|---|---|---|---|
| A | przykład A | valid, valid, invalid, invalid, invalid | 5, 2, 3 | dane z części A |
| B | pusta linia | — | 0, 0, 0 | pusta linia jako pierwsza |
| C | trzy spacje, pusta linia | invalid | 1, 0, 1 | same spacje to kod, a nie koniec danych |
| D | `AB-1234`, pusta linia, `ZZ-9999` | valid | 1, 1, 0 | po pustej linii nic nie jest odczytywane |
| E | siedem poprawnych kodów, pusta linia | 7 razy valid | 7, 7, 0 | tabela poprawnych kodów |
| F | trzynaście niepoprawnych kodów, pusta linia | 13 razy invalid | 13, 0, 13 | tabela niepoprawnych kodów; odrzucony kod nie kończy odczytu |
| G | `AB-123`, `ZZ-9999`, `A1-1234`, `AA-00 00`, pusta linia | invalid, valid, invalid, valid | 4, 2, 2 | poprawny kod po niepoprawnym |
| H | `BC-0102`, pusta linia | valid | 1, 1, 0 | jeden poprawny kod |
| I | `AB-12345`, pusta linia | invalid | 1, 0, 1 | jeden niepoprawny kod |
| J | `AB-1234`, koniec danych | valid | 1, 1, 0 | koniec danych po jednym kodzie |
| K | `ZZ-9999`, `AB_1234`, `A B - 1 2 3 4`, koniec danych | valid, invalid, valid | 3, 2, 1 | koniec danych po kilku kodach |
| L | `AB-1234`, jedna spacja, `BC-0102`, pusta linia | valid, invalid, valid | 3, 2, 1 | linia ze spacją w środku danych nie kończy odczytu |

**Testy automatyczne i Twoje próby.** W przypadkach J i K dane kończą się po ostatniej podanej linii. Pusta linia w przypadku B to jeden znak końca linii, a nie brak danych. Ostatniej linii bez znaku końca linii testy nie uruchamiają, bo w nich każda linia kończy się znakiem końca linii.

Przypadek E, siedem poprawnych kodów:

<!-- input: parcel_codes -->
```text
AB-1234
AA-0000
ZZ-9999
BC-0102
  AB-1234  
A B - 1 2 3 4
AA-00 00

```

<!-- output: parcel_codes -->
```text
Code 1: valid
Code 2: valid
Code 3: valid
Code 4: valid
Code 5: valid
Code 6: valid
Code 7: valid
Codes processed: 7
Valid codes: 7
Invalid codes: 0
```

Przypadek F, trzynaście niepoprawnych kodów:

<!-- input: parcel_codes -->
```text
Ab-1234
ab-1234
aB-1234
A1-1234
AB_1234
AB-123
AB-12345
AB-A234
AB-12A4
AB-123A
AB-1234!
-
   

```

<!-- output: parcel_codes -->
```text
Code 1: invalid
Code 2: invalid
Code 3: invalid
Code 4: invalid
Code 5: invalid
Code 6: invalid
Code 7: invalid
Code 8: invalid
Code 9: invalid
Code 10: invalid
Code 11: invalid
Code 12: invalid
Code 13: invalid
Codes processed: 13
Valid codes: 0
Invalid codes: 13
```

Przypadek G, poprawne kody na przemian z niepoprawnymi:

<!-- input: parcel_codes -->
```text
AB-123
ZZ-9999
A1-1234
AA-00 00

```

<!-- output: parcel_codes -->
```text
Code 1: invalid
Code 2: valid
Code 3: invalid
Code 4: valid
Codes processed: 4
Valid codes: 2
Invalid codes: 2
```

Przypadek H, jeden poprawny kod:

<!-- input: parcel_codes -->
```text
BC-0102

```

<!-- output: parcel_codes -->
```text
Code 1: valid
Codes processed: 1
Valid codes: 1
Invalid codes: 0
```

Przypadek I, jeden niepoprawny kod:

<!-- input: parcel_codes -->
```text
AB-12345

```

<!-- output: parcel_codes -->
```text
Code 1: invalid
Codes processed: 1
Valid codes: 0
Invalid codes: 1
```

Przypadek J, jeden kod, po którym kończą się dane:

<!-- input: parcel_codes -->
```text
AB-1234
```

<!-- output: parcel_codes -->
```text
Code 1: valid
Codes processed: 1
Valid codes: 1
Invalid codes: 0
```

Przypadek K, trzy kody, po których kończą się dane:

<!-- input: parcel_codes -->
```text
ZZ-9999
AB_1234
A B - 1 2 3 4
```

<!-- output: parcel_codes -->
```text
Code 1: valid
Code 2: invalid
Code 3: valid
Codes processed: 3
Valid codes: 2
Invalid codes: 1
```

Przypadek L, linia z jednej spacji między dwoma kodami:

<!-- input: parcel_codes -->
```text
AB-1234
 
BC-0102

```

<!-- output: parcel_codes -->
```text
Code 1: valid
Code 2: invalid
Code 3: valid
Codes processed: 3
Valid codes: 2
Invalid codes: 1
```

</details>

## Rozwiązanie referencyjne

<details>
<summary>Zadanie 1: kontrola kodów paczek</summary>

<!-- example: parcel_codes -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>

std::string without_spaces(const std::string& text) {
    std::string result{};

    for (const char symbol : text) {
        if (symbol != ' ') {
            result.push_back(symbol);
        }
    }

    return result;
}

bool is_valid_code(const std::string& code) {
    if (code.size() != 7) {
        return false;
    }

    const bool first_is_capital{code[0] >= 'A' && code[0] <= 'Z'};
    const bool second_is_capital{code[1] >= 'A' && code[1] <= 'Z'};
    const bool has_hyphen{code[2] == '-'};
    bool all_digits{true};

    for (std::size_t index{3}; index < code.size(); ++index) {
        const bool is_digit{code[index] >= '0' && code[index] <= '9'};

        if (!is_digit) {
            all_digits = false;
        }
    }

    return first_is_capital && second_is_capital && has_hyphen && all_digits;
}

int main() {
    bool reading{true};
    std::size_t codes_processed{0};
    std::size_t valid_codes{0};
    std::size_t invalid_codes{0};

    while (reading) {
        std::string line{};
        std::getline(std::cin, line);

        if (std::cin.fail()) {
            reading = false;
        } else if (line.empty()) {
            reading = false;
        } else {
            const std::string code{without_spaces(line)};
            const bool valid{is_valid_code(code)};

            ++codes_processed;

            if (valid) {
                ++valid_codes;
                std::cout << "Code " << codes_processed << ": valid\n";
            } else {
                ++invalid_codes;
                std::cout << "Code " << codes_processed << ": invalid\n";
            }
        }
    }

    std::cout << "Codes processed: " << codes_processed << "\n";
    std::cout << "Valid codes: " << valid_codes << "\n";
    std::cout << "Invalid codes: " << invalid_codes << "\n";
}
```

| Funkcja | Zadanie | Parametr | Wynik |
|---|---|---|---|
| `without_spaces` | nowy tekst: wszystkie znaki oprócz spacji, w tej samej kolejności | tekst przez `const&` | `std::string` |
| `is_valid_code` | czy tekst ma format kodu: siedem znaków, dwie wielkie litery, myślnik i cztery cyfry | kod bez spacji przez `const&` | `bool` |
| `main` | odczyt linii, koniec odczytu, numeracja, wywołania funkcji, liczniki i cały raport | — | — |

**Przepływ danych dla kodu 2 z przykładu A:**

| Krok | Co się dzieje |
|---|---|
| 1 | `std::getline` odczytuje drugą linię, `A B - 1 2 3 4`: 13 znaków razem ze spacjami. |
| 2 | `std::cin.fail()` daje `false`: odczyt się udał. |
| 3 | `line.empty()` daje `false`: oryginalna linia nie jest pusta, więc to kod do sprawdzenia. |
| 4 | `main` przekazuje `line` do `without_spaces`. |
| 5 | Funkcja zwraca nowy tekst `AB-1234`, który `main` zapisuje w `code`. `line` się nie zmienia. |
| 6 | `main` przekazuje `code` do `is_valid_code`. `code.size()` daje 7, więc klauzula ochronna nie kończy funkcji. |
| 7 | `code[0]` to `A`, a `code[1]` to `B`: obie są wielkimi literami. |
| 8 | `code[2]` to `-`. |
| 9 | Pętla od indeksu 3 do 6 odczytuje `1`, `2`, `3` i `4`. To same cyfry, więc `all_digits` zostaje `true`. |
| 10 | Funkcja zwraca `true`, a `main` zapisuje ten wynik w `valid`. |
| 11 | `codes_processed` rośnie do 2, a `valid_codes` też do 2. |
| 12 | `main` wypisuje `Code 2: valid` i odczytuje następną linię. |

**Omówienie:**

1. **Najpierw powodzenie odczytu.** `std::cin.fail()` jest sprawdzane jako pierwsze, bo po nieudanym odczycie nie wolno polegać na zawartości `line` (lekcja 7.4).
2. **Koniec odczytu zależy od oryginalnej linii.** `line.empty()` stoi przed wywołaniem `without_spaces`. Pusta linia to umówiony sygnał końca, a ten sygnał dotyczy linii wpisanej przez użytkownika, a nie tekstu po przekształceniu.
3. **Same spacje to zgłoszenie.** Linia `"   "` ma trzy znaki, więc `empty()` daje `false` i program sprawdza ją jako kod. Gdyby o końcu decydował tekst bez spacji, ta linia zakończyłaby odczyt. Przypadki C, F i L to sprawdzają.
4. **Nowy tekst.** Kod bez spacji to inny tekst niż linia: ma inne znaki i inną długość. `without_spaces` buduje go w lokalnym `result` przez `push_back`, jak w lekcji 7.3, i zwraca przez wartość.
5. **Oryginał bez zmian.** Funkcja dostaje linię przez `const std::string&`, więc może ją tylko czytać: program, który próbowałby zmienić parametr, nie zbudowałby się. Wejście i tekst do sprawdzenia to dwa osobne obiekty: `line` i `code`.
6. **Najpierw usuwanie spacji, potem format.** Reguła formatu dotyczy kodu bez spacji. `A B - 1 2 3 4` ma 13 znaków i dopiero po usunięciu spacji ma 7 znaków zgodnych z formatem.
7. **Wynik `bool`.** Pytanie „czy kod ma wymagany format?” ma dwie odpowiedzi: tak albo nie. Funkcja tylko odpowiada, a `main` decyduje, co wypisać i który licznik zwiększyć. Dzięki temu funkcję da się sprawdzić wydrukami testowymi bez całego programu, jak w lekcji 5.5.
8. **Najpierw długość.** Klauzula ochronna `if (code.size() != 7)` z lekcji 5.4 kończy funkcję, zanim ta odczyta jakikolwiek znak. Po niej wiadomo, że istnieją wszystkie indeksy od 0 do 6. Za krótkie kody, sam myślnik i pusty tekst dostają `false` bez żadnego odczytu znaku.
9. **Pozycje.** Na indeksach 0 i 1 funkcja sprawdza zakres od `'A'` do `'Z'`, tak jak w lekcji 7.1. Na indeksie 2 porównuje znak z `'-'`. Pętla od indeksu 3 do ostatniego ustawia `all_digits` na `false` przy każdym znaku spoza zakresu od `'0'` do `'9'`. Funkcja zwraca `true` tylko wtedy, gdy wszystkie cztery warunki są spełnione.
10. **Małe litery.** Wielkie i małe litery to dwa osobne zakresy ASCII (lekcja 7.1). `'b'` nie mieści się w zakresie od `'A'` do `'Z'`, więc `Ab-1234` jest niepoprawny. Program niczego nie zamienia: sprawdza znak dokładnie taki, jaki stoi w kodzie.
11. **Trzy liczniki.** `codes_processed` rośnie dla każdego sprawdzonego kodu i daje jego numer. Razem z nim rośnie dokładnie jeden z dwóch pozostałych liczników: w gałęzi `if` albo w gałęzi `else`. Dlatego zawsze `codes_processed` jest równe `valid_codes + invalid_codes`.
12. **Pusty kod jest niepoprawny.** Po usunięciu spacji z `"   "` zostaje pusty tekst. Jego `size()` daje 0, więc klauzula ochronna zwraca `false`, zanim funkcja odczyta `code[0]`. Pusty tekst to poprawny wynik usuwania spacji (lekcja 7.3), ale nie poprawny kod.
13. **Ostatnia linia przy końcu danych.** Gdy dane kończą się zaraz po ostatnim znaku linii, bez znaku końca linii, `getline` i tak dostarcza tę linię, a `fail()` daje `false`. Program ją sprawdza, a pętlę kończy dopiero następna, nieudana próba (lekcja 7.4).
14. **Bez wektora.** Wynik każdego kodu jest gotowy zaraz po jego odczycie, a podsumowanie potrzebuje tylko trzech liczb. Żadna decyzja nie wymaga wcześniejszych linii, więc wektor tekstów nie jest potrzebny.

**Inne poprawne układy.** To jeden z możliwych podziałów. Każdą pozycję można też sprawdzić osobną klauzulą ochronną, na przykład `if (code[2] != '-') { return false; }`, a cztery cyfry czterema warunkami zamiast pętli. Długość można sprawdzić w tym samym warunku co znaki: w `code.size() == 7 && code[0] >= 'A' && ...` krótkie obliczanie z lekcji 3.4 odczytuje znaki tylko przy poprawnej długości. Wolno dodać małą funkcję pomocniczą, która dostaje jeden znak `char` i odpowiada, czy to wielka litera. W `main` licznik `codes_processed` może rosnąć na początku gałęzi przetwarzania, jak w lekcji 7.4, a oba warunki końca można połączyć w `if (std::cin.fail() || line.empty())`. Ważne, żeby o końcu odczytu decydowała oryginalna linia, a długość była znana przed pierwszym odczytem znaku.

</details>

## Diagnostyka: wyniki i poprawki

<details>
<summary>Diagnostyka A: granica zakresu liter</summary>

Przed poprawką:

<!-- output: letter_range_bug -->
```text
Test BC-1234: 1
Test AB-1234: 0
```

- Oba kody są poprawne według wymagań, więc oba testy powinny dać `1`.
- `BC-1234` nie ujawnia błędu: jego pierwsza litera to `B`, a `B` jest większe od `A`, więc błędny warunek ją przepuszcza.
- `AB-1234` ujawnia błąd: `'A' > 'A'` daje `false`, więc funkcja odrzuca poprawny kod.
- **Przyczyna:** warunek `code[0] > 'A'` wyklucza dolną granicę zakresu. Błąd dotyczy tylko litery `A` na indeksie 0: każda inna wielka litera przechodzi.
- **Poprawka:** `code[0] >= 'A' && code[0] <= 'Z'`, tak jak dla indeksu 1.

Po poprawce, z dopisanymi testami:

<!-- example: letter_range_fixed -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>

bool is_valid_code(const std::string& code) {
    if (code.size() != 7) {
        return false;
    }

    const bool first_is_capital{code[0] >= 'A' && code[0] <= 'Z'};
    const bool second_is_capital{code[1] >= 'A' && code[1] <= 'Z'};
    const bool has_hyphen{code[2] == '-'};
    bool all_digits{true};

    for (std::size_t index{3}; index < code.size(); ++index) {
        const bool is_digit{code[index] >= '0' && code[index] <= '9'};

        if (!is_digit) {
            all_digits = false;
        }
    }

    return first_is_capital && second_is_capital && has_hyphen && all_digits;
}

int main() {
    const std::string first_test{"BC-1234"};
    const std::string second_test{"AB-1234"};
    const std::string third_test{"AA-0000"};
    const std::string fourth_test{"aB-1234"};

    std::cout << "Test BC-1234: " << is_valid_code(first_test) << "\n";
    std::cout << "Test AB-1234: " << is_valid_code(second_test) << "\n";
    std::cout << "Test AA-0000: " << is_valid_code(third_test) << "\n";
    std::cout << "Test aB-1234: " << is_valid_code(fourth_test) << "\n";
}
```

<!-- output: letter_range_fixed -->
```text
Test BC-1234: 1
Test AB-1234: 1
Test AA-0000: 1
Test aB-1234: 0
```

`AA-0000` sprawdza literę `A` na obu pozycjach i cyfrę `0`. `aB-1234` sprawdza, czy poprawka nie poszła za daleko: mała litera `a` stoi w ASCII po wszystkich wielkich literach, więc górna granica `<= 'Z'` nadal ją odrzuca. Funkcja w poprawionym programie jest taka sama jak w rozwiązaniu referencyjnym. Odczytu spoza tekstu nie ma w żadnej wersji, bo długość jest sprawdzana przed pierwszym odczytem znaku.

</details>

<details>
<summary>Diagnostyka B: indeks przed sprawdzeniem długości</summary>

1. Trzy: `size()` daje 3.
2. 0, 1 i 2. Pod tymi indeksami stoją `A`, `B` i `-`.
3. Znak należący do tekstu ma indeks mniejszy niż `size()`, czyli tutaj mniejszy niż 3. Indeks 6 jest większy niż `size()`, więc takiego znaku nie ma, a w C++20 taki odczyt to niezdefiniowane zachowanie (lekcja 7.2). Odczyt `code[2]` w pierwszej linijce jest w porządku: indeks 2 należy do tekstu.
4. Nie. Standard języka nie mówi, co się wtedy stanie. Program może dać przypadkowy wynik, zakończyć się błędem albo pozornie działać poprawnie, a na innym komputerze zachować się inaczej. Fragment się zbuduje, bo kompilator nie sprawdza indeksów (lekcja 6.3). Dlatego takiego kodu nie uruchamiamy, żeby „zobaczyć, co wyjdzie”.
5. Sprawdzenie długości: `if (code.size() != 7)` z `return false;`, czyli klauzula ochronna z lekcji 5.4. Po nim wiadomo, że istnieją wszystkie indeksy od 0 do 6.
6. Bo każde sprawdzenie litery, myślnika i cyfry odczytuje znak. Program wykonuje instrukcje po kolei, więc sprawdzenie długości stojące niżej nie cofnie odczytu, który już się wykonał. Za krótkie kody są zwykłymi danymi: `AB-123`, sam myślnik albo pusty tekst z linii samych spacji. Dopiero gdy długość wynosi 7, wszystkie indeksy od 0 do 6 należą do tekstu.

Bezpieczna wersja tego początku ma klauzulę ochronną przed pierwszym odczytem znaku, tak jak rozwiązanie referencyjne:

<!-- fragment -->
```cpp
bool is_valid_code(const std::string& code) {
    if (code.size() != 7) {
        return false;
    }

    const bool has_hyphen{code[2] == '-'};
    const bool last_is_digit{code[6] >= '0' && code[6] <= '9'};

    // ...the other positions, then the result
}
```

</details>

## Odpowiedzi do zadania 3

<details>
<summary>Przykładowe odpowiedzi</summary>

1. Bo pustą linię od linii z samych spacji odróżnia tylko oryginał: pusta ma długość zero, a `"   "` ma trzy znaki. Po usunięciu spacji obie dają pusty tekst. Gdyby program sprawdzał koniec dopiero na tekście bez spacji, linia ze spacjami zakończyłaby odczyt, a kolejne kody nie zostałyby sprawdzone. Taka linia to zgłoszenie: ktoś coś w niej wpisał. Po usunięciu spacji nie zostaje w niej żaden znak, a pusty tekst nie ma siedmiu znaków, więc to niepoprawny kod.
2. Bo to inny tekst niż linia: ma inne znaki i inną długość. Funkcja buduje go od nowa i zwraca, a linia zostaje taka, jak ją wpisano, bo funkcja dostaje ją przez `const&` i może ją tylko czytać.
3. Bo pierwsza funkcja tworzy nowy tekst, więc jej wynikiem jest `std::string`. Druga odpowiada na pytanie, na które są tylko dwie odpowiedzi, tak albo nie, więc jej wynikiem jest `bool`. O tym, co wypisać i który licznik zwiększyć, decyduje `main` na podstawie tej odpowiedzi.
4. Bo znak można odczytać tylko wtedy, gdy jego indeks jest mniejszy niż `size()`, a dopiero przy długości 7 istnieją wszystkie indeksy od 0 do 6. Kolejność ma znaczenie dla kodów krótszych niż siedem znaków, na przykład `AB-123`, `-` albo pusty tekst z linii samych spacji. Dla nich indeks 6 nie należy do tekstu. Za długie kody, jak `AB-12345`, też odrzuca sprawdzenie długości, ale ich znaki od indeksu 0 do 6 istnieją.
5. Bo wynik każdego kodu jest gotowy zaraz po jego odczycie, a podsumowanie potrzebuje tylko trzech liczników. Wcześniejsze kody nie są potrzebne do żadnej późniejszej decyzji.
6. Nie. Równość mówi tylko, że każdy sprawdzony kod trafił do dokładnie jednej z dwóch grup. Funkcja z diagnostyki A zalicza `AB-1234` do niepoprawnych, a liczniki i tak się sumują. Poprawność oceny sprawdzają dopiero przypadki z oczekiwanymi wynikami.

</details>

## Samoocena

Przy każdym kryterium zaznacz jedną odpowiedź:

| Kryterium | Samodzielnie | Z podpowiedzią | Po zajrzeniu do rozwiązania | Do powtórki |
|---|---|---|---|---|
| Podział programu na dwie funkcje i `main` | | | | |
| Nowy tekst bez spacji, budowany przez `push_back` | | | | |
| Sprawdzenie długości przed odczytem znaków | | | | |
| Wielkie litery, myślnik i cyfry na właściwych pozycjach | | | | |
| Pętla odczytu: pusta linia i koniec danych | | | | |
| Linia z samych spacji jako niepoprawny kod | | | | |
| Numeracja kodów i trzy liczniki | | | | |
| Wydruki testowe funkcji | | | | |
| Tabela przypadków | | | | |
| Diagnostyka A (granica zakresu liter) | | | | |
| Diagnostyka B (indeks przed sprawdzeniem długości) | | | | |
| Wyjaśnienia z zadania 3 | | | | |

Jeśli w kolumnie „Do powtórki” jest coś zaznaczone, wróć do odpowiedniej lekcji:

| Temat | Lekcja |
|---|---|
| `char`, porównania znaków i zakresy ASCII | [7.1](lesson_01_first_characters.md) |
| indeksy, `std::size_t` i znaki należące do tekstu | [7.2](lesson_02_positions_and_neighbours.md) |
| funkcja, która dostaje `const std::string&` i tworzy nowy tekst | [7.3](lesson_03_a_function_creates_a_new_text.md) |
| kolejne linie, pusta linia i koniec danych | [7.4](lesson_04_successive_lines.md) |
| kilka instrukcji `return` i klauzula ochronna | [5.4](../module_05_functions/lesson_04_several_returns.md) |
| funkcje zwracające `bool`, podział odpowiedzialności i wydruki testowe | [5.5](../module_05_functions/lesson_05_several_functions.md) |
| krótkie obliczanie `&&` i `\|\|` | [3.4](../module_03_decisions_and_conditions/lesson_04_combining_conditions.md) |
| odczyt spoza zakresu i niezdefiniowane zachowanie | [6.3](../module_06_collections/lesson_03_positions_and_neighbours.md) |

Potem spróbuj zadania jeszcze raz, na przykład z innym formatem kodu: trzy wielkie litery, myślnik i trzy cyfry.

---

## Podsumowanie Modułu 7

Po pięciu lekcjach potrafisz:

- odróżniać znak `char` od tekstu `std::string`, a literał `'A'` od `"A"`;
- przeglądać tekst znak po znaku i rozpoznawać w tekście ASCII wielkie i małe litery, cyfry i pozostałe znaki;
- odczytywać znaki przez indeks typu `std::size_t`, tylko w granicach tekstu, i porównywać sąsiednie znaki;
- pisać funkcje, które dostają tekst przez `const std::string&` i zwracają nowy `std::string`;
- odczytywać kolejne linie przez `std::getline` i odróżniać pustą linię od nieudanego odczytu;
- projektować programy, które odczytują kolejne teksty, przekształcają je, sprawdzają ich format i budują raport z wyników współpracujących funkcji.

Wszystko to dotyczy tekstu ASCII. Tekst ma jeszcze wiele możliwości, które poznasz w dalszych modułach.

## Co dalej

W Module 8, „Własne typy danych: `struct` i rekordy”, zdefiniujesz własny typ, który łączy kilka informacji o jednym obiekcie. Zacznij od pierwszej struktury: [Lekcja 8.1: Pierwsza struktura: kilka danych opisujących jeden obiekt](../module_08_structs/lesson_01_first_struct.md).

**Poprzednia lekcja:** [Lekcja 7.4: Przetwarzanie kolejnych linii przez `std::getline`](lesson_04_successive_lines.md) · **Następna lekcja:** [Lekcja 8.1: Pierwsza struktura: kilka danych opisujących jeden obiekt](../module_08_structs/lesson_01_first_struct.md) · [Opis kursu](../../README.md)

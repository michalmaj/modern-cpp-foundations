# Lekcja 7.3: Funkcja tworzy nowy tekst

**Polski** · [English](lesson_03_a_function_creates_a_new_text.en.md) · [Opis kursu](../../README.md)

> **Moduł 7, lekcja 3** · około 60–75 minut
> **Potrzebujesz:** katalogu `cpp-workspace` i oryginalnego projektu `lesson_05_first_program`, jak dotąd. Debugger nie jest w tej lekcji potrzebny.
> **Wersja pilotażowa.** Programy z tej lekcji sprawdzamy automatycznie na Windowsie, Ubuntu i macOS, także z podanymi danymi wejściowymi. Wpisywanie danych w oknie **Run** CLiona opisujemy bez ręcznego sprawdzenia na każdym systemie.

## Zanim zaczniesz

Ta lekcja zakłada, że:

- piszesz funkcje, które dostają wektor przez `const std::vector<int>&` (lekcja 6.4), i funkcje, które budują nowy wektor przez `push_back` i zwracają go przez wartość (lekcja 6.5);
- przeglądasz tekst pętlą zakresową i porównujesz znaki (lekcja 7.1);
- odczytujesz znaki przez indeks i porównujesz znak z poprzednim (lekcja 7.2);
- pamiętasz krótkie obliczanie `&&` i `||` (lekcja 3.4).

## Sytuacja

W lekcji 6.5 funkcja dostawała wektor, wybierała z niego elementy i zwracała **nowy** wektor. Z tekstem bywa podobnie. Z napisu `"A B C"` chcesz otrzymać ten sam tekst bez spacji, czyli `"ABC"`. Samo policzenie spacji nie wystarczy: potrzebny jest nowy ciąg znaków. Zbudujesz go w osobnym `std::string`, a tekst wejściowy zostanie bez zmian.

Po tej lekcji będziesz:

- pisać funkcje, które dostają tekst przez `const std::string&` i zwracają nowy `std::string`;
- budować nowy tekst znak po znaku przez `push_back`;
- odróżniać tekst wejściowy od wynikowego i rozpoznawać pusty wynik jako poprawny;
- rozpoznawać początek wyrazu, także gdy wyrazy oddziela kilka spacji;
- samodzielnie projektować funkcję, która wyznacza inicjały.

## 1. Przygotuj projekt

W `cpp-workspace` utwórz katalog `lesson_7_3` i skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program`. Programy z punktów 2 i 3 wpisujesz w `main.cpp` tego katalogu.

## 2. Funkcja, która zwraca nowy tekst

<!-- example: spaces_removed -->
```cpp
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

int main() {
    const std::string source{"A B  C"};

    std::cout << "Original: [" << source << "]\n";

    const std::string selected{without_spaces(source)};

    std::cout << "Selected: [" << selected << "]\n";
    std::cout << "Original after: [" << source << "]\n";
}
```

**Przewidź** wszystkie trzy linijki. Czy po wywołaniu `without_spaces` w `source` nadal są spacje? Nawiasy kwadratowe pokazują, gdzie zaczyna się i kończy tekst, więc widać także spacje.

<details>
<summary>Standardowe wyjście</summary>

<!-- output: spaces_removed -->
```text
Original: [A B  C]
Selected: [ABC]
Original after: [A B  C]
```

</details>

To ten sam układ co w lekcji 6.5, tylko dla tekstu:

| Zapis | Znaczenie w tej lekcji |
|---|---|
| `const std::string& text` | istniejący tekst udostępniony funkcji do odczytu, bez kopiowania |
| `std::string result{}` | nowy, lokalny tekst, który funkcja buduje; na początku pusty |
| `result.push_back(symbol)` | dodanie jednego znaku na koniec nowego tekstu |
| `return result;` | zwrócenie gotowego tekstu przez wartość |
| `const std::string selected{...}` | odebranie wyniku, którego `main` nie zamierza zmieniać |

- **`push_back` dla tekstu** działa jak dla wektora w lekcji 6.2: dodaje jeden element na koniec, a tutaj elementem jest jeden znak `char`. Spacje nie są dodawane, a pozostałe znaki trafiają do wyniku w tej samej kolejności co w tekście wejściowym.
- **`const` dotyczy tylko parametru.** Funkcja nie może zmienić `text`, ale swój lokalny `result` zmienia, bo dopisuje do niego znaki, więc `result` nie ma `const`. Wynik odebrany w `main` ma `const`, bo `main` go już nie zmienia.
- **Oryginał jest bez zmian:** funkcja tylko odczytuje `text` i buduje osobny wynik. Trzecia linijka to potwierdza.
- **Zwracanie przez wartość** działa jak w lekcji 6.5: wywołujący dostaje własny, gotowy wynik.

Napisy da się też łączyć innymi sposobami, na przykład `+` z lekcji 2.7. W tej lekcji budujemy wynik znak po znaku, więc używamy tylko `push_back`.

## 3. Pusty wynik

<!-- example: only_spaces -->
```cpp
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

int main() {
    const std::string source{"   "};
    const std::string selected{without_spaces(source)};

    std::cout << "Original: [" << source << "]\n";
    std::cout << "Selected: [" << selected << "]\n";
    std::cout << "Selected size: " << selected.size() << "\n";

    if (selected.empty()) {
        std::cout << "The result is empty\n";
    }
}
```

**Przewidź** wynik dla tekstu złożonego z samych spacji.

<details>
<summary>Standardowe wyjście</summary>

<!-- output: only_spaces -->
```text
Original: [   ]
Selected: []
Selected size: 0
The result is empty
```

</details>

Funkcja nie znalazła żadnego znaku do zachowania, więc zwróciła pusty tekst. **To poprawny wynik, a nie błąd:** wynik istnieje, ma `size()` równe 0, a `empty()` daje `true`. Nie trzeba osobnego kodu błędu ani specjalnej wartości. Z pustego wyniku nie odczytuje się tylko znaków, na przykład `selected[0]`: takiego znaku nie ma (lekcja 7.2).

## 4. Misja: inicjały

Program otrzymuje imię i nazwisko zapisane w tekście i tworzy nowy tekst z pierwszą literą każdego wyrazu. Tekst jest wpisany w kodzie:

<!-- fragment -->
```cpp
const std::string name{"  Ada   Lovelace  "};
```

**Jakie dane są możliwe.** Tekst zawiera wyłącznie wielkie litery `A`–`Z`, małe litery `a`–`z` i zwykłe spacje. Nie ma w nim cyfr, myślników, apostrofów, przecinków, tabulatorów ani polskich liter. To świadome uproszczenie, więc nie musisz sprawdzać innych znaków.

**Reguły:**

- **Wyraz** to niepusty ciąg liter. Wyrazy oddziela jedna albo więcej spacji. Spacje mogą stać także na początku i na końcu tekstu.
- Każdy wyraz daje **dokładnie jeden** inicjał: swoją pierwszą literę.
- Spacje nigdy nie trafiają do wyniku.
- **Wielkość liter zostaje bez zmian.** Dla `"Mary ann SMITH"` wynik to `"MaS"`, a nie `"MAS"`. Program wybiera istniejące znaki i ich nie zmienia.
- Pusty tekst albo tekst z samych spacji daje pusty wynik.

**Wymagania:**

- Program ma własną funkcję, która dostaje tekst przez `const std::string&`, tworzy lokalny pusty `std::string`, dodaje do niego inicjały przez `push_back` i zwraca go przez wartość. Funkcja niczego nie odczytuje z wejścia, niczego nie wypisuje i nie zmienia tekstu wejściowego. Jej nazwę wybierasz samodzielnie.
- `main` przygotowuje tekst, wywołuje funkcję, odbiera wynik i wypisuje dwie linijki: `Name: [TEKST]` i `Initials: [WYNIK]`. Pusty wynik wypisuje jako `Initials: []`. Nie wypisuje nic więcej i nie powtarza algorytmu funkcji.
- Jeśli porównujesz znak z poprzednim, pamiętaj, że pierwszy znak tekstu poprzednika nie ma (lekcja 7.2).
- Program nie odczytuje niczego z wejścia.

W `cpp-workspace` utwórz katalog `initials`, skopiuj do niego `CMakeLists.txt` z oryginalnego `lesson_05_first_program`, utwórz pusty `main.cpp` i napisz program samodzielnie.

Dla tekstu powyżej standardowe wyjście ma być takie:

<!-- output: initials -->
```text
Name: [  Ada   Lovelace  ]
Initials: [AL]
```

**To nie jest funkcja z punktu 2 z innym warunkiem.** Tam o każdym znaku decydowało tylko to, czy jest spacją. Tutaj o znaku decyduje także jego miejsce: litera trafia do wyniku tylko wtedy, gdy **zaczyna wyraz**. Nie wystarczy usunąć spacji, zachować wszystkich liter ani brać znaku po każdej spacji, bo spacji między wyrazami może być kilka. Musisz samodzielnie zdecydować:

1. jak nazwać funkcję i zapisać jej nagłówek;
2. czy przeglądasz tekst pętlą zakresową, czy indeksową;
3. jak rozpoznać początek pierwszego wyrazu, także po spacjach na początku tekstu;
4. jak rozpoznać początek kolejnego wyrazu po kilku spacjach;
5. jak sprawić, żeby żadna spacja nie trafiła do wyniku;
6. co funkcja zwróci dla tekstu pustego i dla samych spacji.

**Zanim napiszesz program**, przygotuj tabelę przypadków: dane z wymagań, dwa wyrazy oddzielone jedną i dwiema spacjami, spacje tylko na początku i tylko na końcu, jeden wyraz, jedna litera, pusty tekst, jedna spacja, same spacje, mieszana wielkość liter i trzy wyrazy z różną liczbą spacji. Przy każdym zapisz oczekiwany wynik.

**Potem:** uruchom program dla danych z wymagań, a następnie zmień tekst na 3–4 przypadki z tabeli, na przykład `"Ada  Lovelace"`, `"Mary ann SMITH"`, `"   "` i pusty tekst. Wszystkie przypadki z pełnej listy kontrolnej są sprawdzone automatycznie, więc nie musisz wpisywać ich wszystkich.

### Kryterium sukcesu

- Program buduje się jako C++20, a dla danych z wymagań wypisuje dokładnie dwie linijki pokazane wyżej.
- Funkcja dostaje tekst przez `const std::string&`, buduje wynik przez `push_back` i zwraca go jako `std::string`. Niczego nie odczytuje ani nie wypisuje.
- Każdy wyraz daje jeden inicjał, niezależnie od liczby spacji przed nim i po nim.
- W wyniku nie ma spacji, a wielkość liter jest taka jak w tekście wejściowym.
- Pusty tekst i same spacje dają `Initials: []`.
- Program nie odczytuje znaku spoza tekstu.
- Tabela przypadków powstała przed uruchomieniem programu.
- Umiesz wyjaśnić, po czym Twoja funkcja rozpoznaje początek wyrazu.

Gdy wynik się zgadza, możesz zapisać projekt w Gicie, jak w lekcji 1.5.

<details>
<summary>Podpowiedź 1</summary>

Które znaki są potrzebne w nowym tekście, a które mają pozostać tylko w tekście wejściowym?

</details>

<details>
<summary>Podpowiedź 2</summary>

Pierwsza litera każdego wyrazu jest ważna. Jak rozpoznać początek kolejnego wyrazu, jeśli pomiędzy wyrazami jest więcej niż jedna spacja?

</details>

<details>
<summary>Podpowiedź 3</summary>

Upewnij się, że do wyniku dodajesz tylko literę, a nie spację. Możesz analizować poprzedni znak albo zapamiętywać, że oczekujesz początku nowego wyrazu.

</details>

<details>
<summary>Pełna lista przypadków kontrolnych: otwórz po przygotowaniu własnej tabeli</summary>

| | Tekst | Inicjały | Co sprawdza |
|---|---|---|---|
| A | `  Ada   Lovelace  ` | `AL` | dane z wymagań: spacje na początku, w środku i na końcu |
| B | `Ada Lovelace` | `AL` | dwa wyrazy, jedna spacja |
| C | `Ada  Lovelace` | `AL` | dwie spacje między wyrazami |
| D | `  Ada` | `A` | spacje tylko na początku |
| E | `Ada  ` | `A` | spacje tylko na końcu |
| F | `Ada` | `A` | jeden wyraz, bez spacji |
| G | `A` | `A` | jedna litera |
| H | pusty tekst | pusty | pusty tekst |
| I | jedna spacja | pusty | jedna spacja |
| J | trzy spacje | pusty | same spacje |
| K | `Mary ann SMITH` | `MaS` | wielkość liter bez zmian |
| L | `a B c` | `aBc` | małe i wielkie inicjały |
| M | `A  B   C` | `ABC` | trzy wyrazy, różna liczba spacji |
| N | `Ada Ada` | `AA` | powtórzony wyraz |
| O | `AA BB` | `AB` | tylko pierwsza litera wyrazu |

**Testy automatyczne i Twoje próby.** Wszystkie przypadki są sprawdzone automatycznie przez program kontrolny. Ma on tę samą funkcję co rozwiązanie referencyjne, ale tekst odczytuje z wejścia jako jedną linijkę, przez `std::getline` z lekcji 2.7. Spacje na początku i na końcu linijki są przy tym zachowane, a pusty tekst to pusta linijka, a nie brak danych. To tylko narzędzie do sprawdzania, a nie część misji. Program kontrolny i jego wyniki są w części [Przykładowe rozwiązania](#przykładowe-rozwiązania), bo zawierają rozwiązanie.

</details>

Przykładowe rozwiązanie jest w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 5. Znajdź błąd: spacja jako inicjał

To zadanie wykonaj **po misji**: program poniżej zawiera prawie całe rozwiązanie. Odczytuje tekst z wejścia jako jedną linijkę, tak jak program kontrolny, i nie wypisuje pytania: po uruchomieniu wpisz tekst i naciśnij **Enter**. Funkcja sprawdza, czy znak stoi na początku tekstu albo zaraz po spacji.

<details>
<summary>Program do sprawdzenia: otwórz po napisaniu własnego programu</summary>

<!-- example: initials_space_bug -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>

std::string initials_of(const std::string& text) {
    std::string result{};

    for (std::size_t index{0}; index < text.size(); ++index) {
        const bool word_can_start{index == 0 || text[index - 1] == ' '};

        if (word_can_start) {
            result.push_back(text[index]);
        }
    }

    return result;
}

int main() {
    std::string name{};
    std::getline(std::cin, name);

    if (std::cin.fail()) {
        std::cout << "Input could not be read\n";
    } else {
        const std::string initials{initials_of(name)};

        std::cout << "Name: [" << name << "]\n";
        std::cout << "Initials: [" << initials << "]\n";
    }
}
```

1. **Przewidź** wynik dla `Ada Lovelace` i dla `Ada  Lovelace`, z dwiema spacjami.
2. Uruchom program dla `Ada Lovelace`. Czy wynik jest poprawny?
3. Uruchom go dla `Ada  Lovelace`.
4. Prześledź znaki od indeksu 3 do 5: przy którym znaku do wyniku trafia spacja?
5. Wskaż sprawdzenie, którego brakuje.
6. Popraw funkcję.
7. Sprawdź ponownie oba przypadki, a także `  Ada`, trzy spacje, `Ada` i `A  B   C`.

</details>

Wyniki programu przed poprawką i poprawiony program są w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 6. Gdy coś pójdzie inaczej

| Co widzisz | Co to znaczy | Co zrobić |
|---|---|---|
| W wyniku jest spacja, na przykład `Initials: [A L]` | Program dodaje znak, który stoi po spacji, choć sam jest spacją (punkt 5). | Do wyniku dodawaj tylko znak, który nie jest spacją. |
| Wynik zaczyna się od spacji przy spacjach na początku tekstu | Pierwszy znak tekstu jest dodawany bez sprawdzenia, czy jest literą. | Pierwszy znak też musi być literą, żeby trafić do wyniku. |
| Brakuje pierwszego inicjału | Pierwszy wyraz nie jest rozpoznawany, bo przed nim nie ma spacji. | Początek tekstu też może być początkiem wyrazu. |
| Za dużo inicjałów, na przykład `AdaLovelace` zamiast `AL` | Program dodaje każdą literę, a nie tylko pierwszą w wyrazie. | Litera trafia do wyniku tylko wtedy, gdy zaczyna wyraz. |
| Błąd kompilacji przy `push_back`, w którym kompilator wspomina `const` | Program dopisuje znak do parametru `const&` albo do wyniku zadeklarowanego jako `const`. | Buduj wynik w lokalnym `std::string` bez `const`. |
| Błąd kompilacji przy `push_back` z `'const char[2]'` | Do `push_back` trafia tekst w cudzysłowie, na przykład `"A"`. | `push_back` przyjmuje jeden znak: `'A'` albo zmienną typu `char`. |
| Dziwne znaki albo nieoczekiwane zakończenie programu | Prawdopodobnie odczyt `text[index - 1]` dla indeksu 0. | Pierwszy znak nie ma poprzednika (lekcja 7.2). Sprawdź go osobno albo użyj krótkiego obliczania z lekcji 3.4. |

## 7. Wyjaśnij

Odpowiedz własnymi słowami, najlepiej na piśmie. Dopiero potem porównaj z przykładowymi odpowiedziami.

1. Co oznacza parametr `const std::string&` i dlaczego funkcja nie musi kopiować tekstu?
2. Dlaczego lokalny wynik nie ma `const`, a wynik odebrany w `main` może go mieć?
3. Co robi `push_back(char)` na tekście?
4. Czym różni się zwracanie `std::string` od zwracania `int`? Czy `return result;` zwraca referencję do zmiennej lokalnej?
5. Czy funkcja zmienia oryginalny tekst?
6. Co oznacza pusty wynik i czym różni się od nieudanego działania?
7. Dlaczego kilka spacji między wyrazami nie może dawać kilku inicjałów?
8. Dlaczego spacje na początku tekstu wymagają uwagi?
9. Jak Twój program zachowuje wielkość liter?
10. Kiedy w tej misji wygodniejsza jest pętla zakresowa, a kiedy indeksowa?
11. Dlaczego przypadek `Ada Lovelace` nie ujawnia błędu z punktu 5?

<details>
<summary>Przykładowe odpowiedzi</summary>

1. Parametr odnosi się do istniejącego tekstu wywołującego i pozwala go tylko czytać, jak `const&` dla wektora w lekcji 6.4. Funkcja, która tylko czyta tekst, nie potrzebuje jego kopii.
2. Funkcja dopisuje znaki do lokalnego wyniku, więc musi go zmieniać. `main` dostaje gotowy wynik i, jeśli go nie zmienia, oznacza go `const`.
3. Dodaje jeden znak na koniec tekstu. Wcześniejsze znaki zostają, a `size()` rośnie o 1.
4. Mechanizm jest ten sam: `return` przekazuje wynik do miejsca wywołania przez wartość. Różni się tylko typ: zamiast jednej liczby wywołujący dostaje cały nowy tekst. To nie jest referencja do zmiennej lokalnej, tylko własny wynik wywołującego, jak w lekcji 6.5.
5. Nie. Dostaje go przez `const&`, więc może go tylko czytać. Wybrane znaki trafiają do osobnego tekstu.
6. Że żaden znak nie spełnił warunku, na przykład tekst był pusty albo składał się z samych spacji. Funkcja zadziałała poprawnie, a jej wynik to tekst bez znaków: `size()` daje 0, a `empty()` daje `true`.
7. Bo każdy wyraz zaczyna się tylko raz. Spacje są separatorami, a nie wyrazami: dodatkowa spacja nie zaczyna nowego wyrazu, a inicjał to litera, nie spacja.
8. Bo przed pierwszym wyrazem może nie być żadnego znaku, a może być kilka spacji. Funkcja musi rozpoznać pierwszą literę w obu sytuacjach i nie dodać żadnej z tych spacji.
9. Dodaje do wyniku dokładnie ten znak, który stoi w tekście, bez żadnej zamiany. Wielka litera zostaje wielka, a mała mała.
10. Pętla indeksowa daje bezpośredni dostęp do poprzedniego znaku, ale wymaga ostrożności przy indeksie 0. Pętla zakresowa nie ma indeksów, więc o poprzednim znaku trzeba pamiętać w osobnej zmiennej. Obie drogi są poprawne.
11. Bo między wyrazami jest tylko jedna spacja. Po pojedynczej spacji następny znak jest już literą, więc błędny warunek nie ma okazji dodać spacji.

</details>

## Podsumowanie

- Funkcja może dostać tekst przez `const std::string&`, zbudować nowy `std::string` i zwrócić go przez wartość, tak jak wektor w lekcji 6.5.
- `push_back(char)` dodaje jeden znak na koniec nowego tekstu. Wynik buduje się w lokalnym `std::string` bez `const`.
- Tekst wejściowy zostaje bez zmian, a wybrane znaki zachowują jego kolejność.
- Pusty tekst to poprawny wynik, a nie błąd. Rozpoznajesz go przez `empty()`, a w nawiasach wygląda tak: `[]`.
- Początek wyrazu to litera, która stoi na początku tekstu albo zaraz po spacji. Kilka spacji z rzędu nie tworzy nowych wyrazów.
- Przy porównywaniu z poprzednim znakiem pamiętaj, że pierwszy znak poprzednika nie ma.

## Co dalej

W tej lekcji tekst był wpisany w kodzie. W kolejnej lekcji program odczyta z wejścia kolejne linie tekstu przez `std::getline` i przeanalizuje każdą z nich: [Lekcja 7.4: Przetwarzanie kolejnych linii przez `std::getline`](lesson_04_successive_lines.md).

---

## Przykładowe rozwiązania

Zajrzyj tutaj **po własnej próbie**. Twoje nazwy mogą się różnić, jeśli standardowe wyjście jest takie, jak wymagane.

<details>
<summary>Punkt 4: misja, inicjały</summary>

<!-- example: initials -->
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
    const std::string name{"  Ada   Lovelace  "};
    const std::string initials{initials_of(name)};

    std::cout << "Name: [" << name << "]\n";
    std::cout << "Initials: [" << initials << "]\n";
}
```

1. **Parametr ma `const&`**, bo funkcja tylko czyta tekst i nie potrzebuje jego kopii.
2. **Wynik lokalny nie ma `const`**, bo funkcja dopisuje do niego inicjały.
3. **Zwracanie `std::string` przez wartość:** `main` dostaje gotowy, własny wynik, jak wektor w lekcji 6.5.
4. **Pierwszy wyraz:** dla indeksu 0 `word_can_start` jest prawdziwe, bo początek tekstu też może zaczynać wyraz. Lewa część `index == 0` jest wtedy prawdziwa, więc `||` nie oblicza prawej części: `text[index - 1]` dla indeksu 0 nie jest odczytywane. To krótkie obliczanie z lekcji 3.4 w praktyce.
5. **Kolejne wyrazy:** dla indeksu od 1 wzwyż `word_can_start` jest prawdziwe, gdy poprzedni znak jest spacją.
6. **Kilka spacji:** znak po spacji trafia do wyniku tylko wtedy, gdy sam nie jest spacją: `text[index] != ' '`. Druga i kolejna spacja stoją po spacji, ale są spacjami, więc nie trafiają do wyniku.
7. **Spacje na początku:** pierwsza spacja stoi na początku tekstu, a następne po spacjach, ale żadna nie jest literą, więc żadna nie trafia do wyniku. Do wyniku trafia dopiero pierwsza litera po nich.
8. **Spacje na końcu:** po ostatnim wyrazie nie ma już liter, więc nic więcej nie zostaje dodane.
9. **Pusty tekst:** pętla nie wykonuje żadnego przebiegu, więc funkcja zwraca pusty `result`.
10. **Wielkość liter:** `push_back(text[index])` dodaje znak dokładnie taki, jaki stoi w tekście.
11. **Oryginał bez zmian:** funkcja dostaje `text` przez `const&` i tylko go czyta.
12. **Inne poprawne algorytmy:** można przeglądać tekst pętlą zakresową i pamiętać w zmiennej `bool`, czy poprzedni znak był spacją, jak w programie poniżej. Można też osobno sprawdzić pierwszy znak, a pętlę porównującą z poprzednim zacząć od indeksu 1. Ważne, żeby każdy wyraz dał jeden inicjał, a spacja nigdy nie trafiła do wyniku.

**Inny poprawny algorytm: pętla zakresowa i zmienna, która pamięta poprzedni znak.**

<!-- example: initials_with_flag -->
```cpp
#include <iostream>
#include <string>

std::string initials_of(const std::string& text) {
    std::string result{};
    bool after_space{true};

    for (const char symbol : text) {
        if (symbol != ' ' && after_space) {
            result.push_back(symbol);
        }

        after_space = (symbol == ' ');
    }

    return result;
}

int main() {
    const std::string name{"  Ada   Lovelace  "};
    const std::string initials{initials_of(name)};

    std::cout << "Name: [" << name << "]\n";
    std::cout << "Initials: [" << initials << "]\n";
}
```

<!-- output: initials_with_flag -->
```text
Name: [  Ada   Lovelace  ]
Initials: [AL]
```

`after_space` mówi, czy poprzedni znak był spacją. Na początku ma wartość `true`, bo pierwszy znak tekstu też może zaczynać wyraz, tak jak znak po spacji. Po każdym znaku zmienna dostaje nową wartość: `true`, gdy ten znak był spacją, i `false` w przeciwnym razie. Ta wersja nie potrzebuje indeksów, więc nie ma też ryzyka odczytu przed pierwszym znakiem.

**Program kontrolny** sprawdza wszystkie przypadki z listy kontrolnej. Funkcja jest taka sama jak w rozwiązaniu referencyjnym, a w `main` tekst jest odczytywany z wejścia jako jedna linijka przez `std::getline`, więc nie ma `const`. `std::getline` zachowuje spacje na początku i na końcu linijki.

<!-- example: initials_check -->
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
    std::string name{};
    std::getline(std::cin, name);

    if (std::cin.fail()) {
        std::cout << "Input could not be read\n";
    } else {
        const std::string initials{initials_of(name)};

        std::cout << "Name: [" << name << "]\n";
        std::cout << "Initials: [" << initials << "]\n";
    }
}
```

Każdy przypadek to jedna linijka wejścia, w kolejności z listy kontrolnej, od A do O. Przypadek H to pusta linijka, przypadek I to jedna spacja, a przypadek J to trzy spacje.

<!-- input: initials_check -->
```text
  Ada   Lovelace  
```

<!-- output: initials_check -->
```text
Name: [  Ada   Lovelace  ]
Initials: [AL]
```

<!-- input: initials_check -->
```text
Ada Lovelace
```

<!-- output: initials_check -->
```text
Name: [Ada Lovelace]
Initials: [AL]
```

<!-- input: initials_check -->
```text
Ada  Lovelace
```

<!-- output: initials_check -->
```text
Name: [Ada  Lovelace]
Initials: [AL]
```

<!-- input: initials_check -->
```text
  Ada
```

<!-- output: initials_check -->
```text
Name: [  Ada]
Initials: [A]
```

<!-- input: initials_check -->
```text
Ada  
```

<!-- output: initials_check -->
```text
Name: [Ada  ]
Initials: [A]
```

<!-- input: initials_check -->
```text
Ada
```

<!-- output: initials_check -->
```text
Name: [Ada]
Initials: [A]
```

<!-- input: initials_check -->
```text
A
```

<!-- output: initials_check -->
```text
Name: [A]
Initials: [A]
```

<!-- input: initials_check -->
```text

```

<!-- output: initials_check -->
```text
Name: []
Initials: []
```

<!-- input: initials_check -->
```text
 
```

<!-- output: initials_check -->
```text
Name: [ ]
Initials: []
```

<!-- input: initials_check -->
```text
   
```

<!-- output: initials_check -->
```text
Name: [   ]
Initials: []
```

<!-- input: initials_check -->
```text
Mary ann SMITH
```

<!-- output: initials_check -->
```text
Name: [Mary ann SMITH]
Initials: [MaS]
```

<!-- input: initials_check -->
```text
a B c
```

<!-- output: initials_check -->
```text
Name: [a B c]
Initials: [aBc]
```

<!-- input: initials_check -->
```text
A  B   C
```

<!-- output: initials_check -->
```text
Name: [A  B   C]
Initials: [ABC]
```

<!-- input: initials_check -->
```text
Ada Ada
```

<!-- output: initials_check -->
```text
Name: [Ada Ada]
Initials: [AA]
```

<!-- input: initials_check -->
```text
AA BB
```

<!-- output: initials_check -->
```text
Name: [AA BB]
Initials: [AB]
```

</details>

<details>
<summary>Punkt 5: wyniki przed poprawką i poprawiony program</summary>

Przed poprawką, dla `Ada Lovelace`:

<!-- input: initials_space_bug -->
```text
Ada Lovelace
```

<!-- output: initials_space_bug -->
```text
Name: [Ada Lovelace]
Initials: [AL]
```

Dla `Ada  Lovelace`, z dwiema spacjami:

<!-- input: initials_space_bug -->
```text
Ada  Lovelace
```

<!-- output: initials_space_bug -->
```text
Name: [Ada  Lovelace]
Initials: [A L]
```

| Indeks | Znak | Poprzedni znak | `word_can_start` | Dodany? |
|---|---|---|---|---|
| 3 | spacja | `a` | `false` | nie |
| 4 | spacja | spacja | `true` | **tak: spacja trafia do wyniku** |
| 5 | `L` | spacja | `true` | tak |

Dla pozostałych tekstów:

<!-- input: initials_space_bug -->
```text
  Ada
```

<!-- output: initials_space_bug -->
```text
Name: [  Ada]
Initials: [  A]
```

<!-- input: initials_space_bug -->
```text
   
```

<!-- output: initials_space_bug -->
```text
Name: [   ]
Initials: [   ]
```

<!-- input: initials_space_bug -->
```text
Ada
```

<!-- output: initials_space_bug -->
```text
Name: [Ada]
Initials: [A]
```

<!-- input: initials_space_bug -->
```text
A  B   C
```

<!-- output: initials_space_bug -->
```text
Name: [A  B   C]
Initials: [A B  C]
```

- Dla `Ada Lovelace` i `Ada` wynik jest poprawny: po pojedynczej spacji stoi już litera, a bez spacji nie ma czego pomylić.
- Dla dwóch spacji z rzędu, spacji na początku i samych spacji do wyniku trafiają spacje: druga spacja stoi po spacji, a funkcja nie sprawdza, czy sam znak jest literą.
- **Przyczyna:** warunek `if (word_can_start)` sprawdza tylko miejsce znaku, a nie sam znak.
- **Poprawka:** `if (text[index] != ' ' && word_can_start)`.

Odczytu spoza tekstu tu nie ma: dla indeksu 0 krótkie obliczanie `||` pomija `text[index - 1]`.

Poprawiony program to program kontrolny z punktu 4: różni się od programu z błędem tylko tym warunkiem. Dla wszystkich sześciu tekstów daje wyniki z listy kontrolnej: przypadki B, C, D, J, F i M.

</details>

**Poprzednia lekcja:** [Lekcja 7.2: Pozycje i sąsiednie znaki w `std::string`](lesson_02_positions_and_neighbours.md) · **Następna lekcja:** [Lekcja 7.4: Przetwarzanie kolejnych linii przez `std::getline`](lesson_04_successive_lines.md) · [Opis kursu](../../README.md)

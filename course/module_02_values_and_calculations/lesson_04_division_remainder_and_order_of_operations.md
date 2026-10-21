# Lekcja 2.4: Dzielenie, reszta i kolejność działań

**Polski** · [English](lesson_04_division_remainder_and_order_of_operations.en.md) · [Opis kursu](../../README.md)

> **Moduł 2, lekcja 4** · około 60–75 minut
> **Potrzebujesz:** katalogu `cpp-workspace` i oryginalnego projektu `lesson_05_first_program`, jak dotąd. Debugger nie jest w tej lekcji potrzebny.
> **Wersja pilotażowa.** Przykłady z tej lekcji sprawdzamy automatycznie na Windowsie, Ubuntu i macOS.

## Zanim zaczniesz

Ta lekcja zakłada, że po lekcjach 2.1–2.3:

- tworzysz zmienne `int` i stałe `const int` z wartością początkową w `{}`;
- liczysz z `+`, `-` i `*` i wypisujesz wyniki przez `std::cout`;
- przewidujesz wartości przed uruchomieniem programu i porównujesz je z wynikiem;
- szukasz pierwszego miejsca, w którym obliczenie daje inny wynik, niż przewidywano: debuggerem albo wypisując wartości.

## Sytuacja

W szkole 7 podzielone przez 2 to 3,5. W programie dzielenie liczb całkowitych działa według własnych, ściśle określonych zasad i daje inny wynik. Dziś poznasz te zasady, nowe działanie, które oblicza **resztę z dzielenia**, i reguły mówiące, w jakiej kolejności łączą się działania w dłuższym wyrażeniu.

Po tej lekcji będziesz:

- dzielić liczby całkowite operatorem `/` i przewidywać wynik dla liczb dodatnich;
- wyjaśniać, dlaczego `7 / 2` daje `3` i gdzie znika część ułamkowa;
- obliczać resztę z dzielenia operatorem `%` i odróżniać go od `/`;
- stosować `/` i `%` razem w praktycznym zadaniu;
- przewidywać, jak pogrupuje się wyrażenie z kilkoma działaniami, i zmieniać to nawiasami;
- znajdować błąd w obliczeniu, które się buduje, ale liczy coś innego, niż miało.

## 1. Przygotuj projekt

W `cpp-workspace` utwórz katalog `lesson_2_4` i skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program`. Programy z punktów 2–8 wpisujesz w `main.cpp` tego katalogu.

## 2. Ile wynosi 7 / 2?

W C++ dzielenie zapisuje się ukośnikiem `/`. Zastąp zawartość `main.cpp` tym programem:

<!-- example: divide_seven -->
```cpp
#include <iostream>

int main() {
    const int result{7 / 2};
    std::cout << result << "\n";
}
```

**Przewidź**, co wypisze program. Zapisz odpowiedź, a potem zbuduj go i uruchom.

<details>
<summary>Wynik programu</summary>

<!-- output: divide_seven -->
```text
3
```

</details>

Nie 3,5, tylko 3. To nie błąd programu, tylko zasada:

- liczby po obu stronach operatora to jego **operandy**. Tutaj oba operandy, `7` i `2`, są typu `int`, czyli są liczbami całkowitymi;
- gdy oba operandy są całkowite, `/` wykonuje **dzielenie całkowite**, a jego wynik też jest liczbą całkowitą;
- dla liczb dodatnich ten wynik to **pełna część** ilorazu: ile razy 2 mieści się w 7 w całości. Część ułamkowa nie zostaje zachowana;
- C++ tego wyniku **nie zaokrągla** do najbliższej liczby całkowitej. Po prostu go nie tworzy.

**Część ułamkowa znika już w samym dzieleniu, nie przy zapisie do zmiennej.** `7 / 2` od razu daje `3`. Nie powstaje po drodze 3,5, które dopiero zmienna `int` „przycina”. Sprawdź to w kolejnym programie: ostatnia linijka wypisuje wynik dzielenia bez żadnej zmiennej. Nawiasy wokół dzielenia w `std::cout` pokazują wyraźnie, co ma zostać obliczone, jak w lekcji 2.1.

<!-- example: division_cases -->
```cpp
#include <iostream>

int main() {
    std::cout << "8 / 2 = " << (8 / 2) << "\n";
    std::cout << "9 / 2 = " << (9 / 2) << "\n";
    std::cout << "10 / 3 = " << (10 / 3) << "\n";
    std::cout << "3 / 5 = " << (3 / 5) << "\n";
    std::cout << "7 / 2 = " << (7 / 2) << "\n";
}
```

**Przewidź** każdy wynik, zanim uruchomisz program.

<details>
<summary>Wynik programu</summary>

<!-- output: division_cases -->
```text
8 / 2 = 4
9 / 2 = 4
10 / 3 = 3
3 / 5 = 0
7 / 2 = 3
```

</details>

- `8 / 2` dzieli się bez reszty, więc wynik jest taki jak w matematyce: 4.
- `9 / 2` daje 4, a nie 5. Gdyby C++ zaokrąglało 4,5, mogłoby wyjść 5. Nie zaokrągla: liczy, ile razy 2 mieści się w 9 w całości.
- `10 / 3` daje 3: trzy trójki mieszczą się w 10, a 1 zostaje.
- `3 / 5` daje 0: 5 nie mieści się w 3 ani razu. To, że matematycznie wychodzi 0,6, nic tu nie zmienia.
- Ostatnia linijka nie zapisuje wyniku w żadnej zmiennej, a i tak wypisuje 3. To potwierdza, że część ułamkowa znika w samym dzieleniu.

W tym kursie dzielimy na razie tylko **liczby dodatnie**. Dla liczb ujemnych zasady też są dokładnie określone. Poznasz je później.

## 3. Reszta z dzielenia: `%`

W klasie jest 17 kredek do rozdania do pudełek po 5. Ile pudełek będzie pełnych i ile kredek zostanie? Odpowiadają na to dwa operatory:

<!-- example: groups_and_remainder -->
```cpp
#include <iostream>

int main() {
    const int full_groups{17 / 5};
    const int remaining_items{17 % 5};

    std::cout << "Full groups: " << full_groups << "\n";
    std::cout << "Remaining items: " << remaining_items << "\n";
}
```

<!-- output: groups_and_remainder -->
```text
Full groups: 3
Remaining items: 2
```

- `/` mówi, ile jest **pełnych grup**: `17 / 5` daje `3`.
- `%` mówi, ile elementów **zostaje**: `17 % 5` daje `2`. To **operator reszty z dzielenia**.
- Razem opisują wszystko: 3 pełne grupy po 5 to 15 kredek, a z pozostałymi 2 jest ich 17.

**Uwaga na znak `%`.** W C++ nie ma on nic wspólnego z procentami. `17 % 5` nie oznacza „17 procent z 5”. To zawsze reszta z dzielenia 17 przez 5.

Tak jak przy `/`, w tej lekcji obie liczby przy `%` są dodatnie.

## 4. Nigdy nie dziel przez zero

> **Ważna zasada:** w C++ **nie wolno** wykonywać dzielenia całkowitego przez zero ani obliczać reszty z dzielenia przez zero: ani `/ 0`, ani `% 0`.

Takie działanie ma w C++ **niezdefiniowane zachowanie** (*undefined behaviour*). Oznacza to, że język nie określa, co się wtedy stanie. Program może się nagle zakończyć, wypisać przypadkową wartość albo zachowywać się różnie na różnych komputerach. Kompilator czasem ostrzeże o dzieleniu przez zero widocznym w kodzie, ale nie zawsze może to zauważyć przed uruchomieniem programu.

W tej lekcji dzielnik jest zawsze **znaną liczbą dodatnią**, wpisaną w kodzie. Jak sprawdzić dzielnik, którego wartości nie znasz z góry, poznasz w Module 3.

## 5. Kolejność działań

Znasz już pięć operatorów arytmetycznych: `+`, `-`, `*`, `/` i `%`. Gdy w jednym wyrażeniu jest ich kilka, C++ musi wiedzieć, które działania łączą się ze sobą. Decydują o tym dwie zasady:

| Poziom | Operatory | Na tym samym poziomie |
|---|---|---|
| wyższy (łączą się najpierw) | `*`, `/`, `%` | od lewej do prawej |
| niższy | `+`, `-` | od lewej do prawej |

- **Priorytet:** `*`, `/` i `%` łączą się ze swoimi liczbami przed `+` i `-`.
- **Łączność:** gdy kilka operatorów stoi na tym samym poziomie, w wyrażeniach z tej lekcji grupują się od lewej do prawej.
- **Nawiasy** zmieniają grupowanie: to, co w nawiasach, tworzy jedną całość.

Najłatwiej przewidzieć wynik, dopisując w myślach **niewidoczne nawiasy**. Sprawdź to na dwóch parach wyrażeń:

<!-- example: grouping -->
```cpp
#include <iostream>

int main() {
    const int first{20 / 5 * 2};
    const int second{20 / (5 * 2)};
    const int third{10 - 8 / 2};
    const int fourth{(10 - 8) / 2};

    std::cout << "20 / 5 * 2 = " << first << "\n";
    std::cout << "20 / (5 * 2) = " << second << "\n";
    std::cout << "10 - 8 / 2 = " << third << "\n";
    std::cout << "(10 - 8) / 2 = " << fourth << "\n";
}
```

**Przewidź** wszystkie cztery wyniki, a potem uruchom program.

<details>
<summary>Wynik programu</summary>

<!-- output: grouping -->
```text
20 / 5 * 2 = 8
20 / (5 * 2) = 2
10 - 8 / 2 = 6
(10 - 8) / 2 = 1
```

</details>

| Wyrażenie | Niewidoczne nawiasy | Obliczenie | Wynik |
|---|---|---|---|
| `20 / 5 * 2` | `(20 / 5) * 2` | 4 · 2 | 8 |
| `20 / (5 * 2)` | nawias już jest | 20 / 10 | 2 |
| `10 - 8 / 2` | `10 - (8 / 2)` | 10 − 4 | 6 |
| `(10 - 8) / 2` | nawias już jest | 2 / 2 | 1 |

**Uwaga na częsty błąd.** Czasem słyszy się regułę „najpierw mnożenie, potem dzielenie”. To nieprawda, w C++ i w matematyce: `*` i `/` są na **tym samym** poziomie. W `20 / 5 * 2` pierwsze jest dzielenie, bo stoi bardziej po lewej. Mnożenie przed dzieleniem trzeba zapisać nawiasem, jak w `20 / (5 * 2)`.

**Nawiasy dla jasności.** Jeśli nie masz pewności, jak wyrażenie się pogrupuje, albo chcesz, żeby czytelnik nie musiał się zastanawiać, dopisz nawiasy, nawet gdy niczego nie zmieniają: `(20 / 5) * 2` znaczy to samo co `20 / 5 * 2`, ale czyta się je szybciej. Tak samo było z nawiasami w `std::cout` w lekcji 2.1.

Priorytet i łączność mówią tylko, **które działania łączą się ze sobą**. Nie opisują ogólnej kolejności, w jakiej C++ oblicza wszystkie części dłuższych instrukcji. W wyrażeniach z tej lekcji, zbudowanych z liczb, zmiennych i operatorów arytmetycznych, samo grupowanie wystarcza, żeby przewidzieć wynik.

## 6. Przewidź samodzielnie: sześć wyrażeń

Każde z tych wyrażeń sprawdza inną pułapkę. Przepisz tabelę i dla każdego wiersza:

1. **przewidź** wynik;
2. zapisz **grupowanie**, czyli niewidoczne nawiasy;
3. sprawdź wynik w programie poniżej;
4. jeśli wynik jest inny niż przewidywany, **wyjaśnij**, skąd ta różnica.

| | Wyrażenie | Grupowanie | Przewidywanie | Wynik programu |
|---|---|---|---|---|
| a | `17 / 4` | | | |
| b | `17 % 4` | | | |
| c | `12 / 2 * 3` | | | |
| d | `12 / (2 * 3)` | | | |
| e | `2 + 3 * 4` | | | |
| f | `(2 + 3) * 4` | | | |

Dopiero gdy tabela jest wypełniona, uruchom program:

<!-- example: predictions -->
```cpp
#include <iostream>

int main() {
    const int a{17 / 4};
    const int b{17 % 4};
    const int c{12 / 2 * 3};
    const int d{12 / (2 * 3)};
    const int e{2 + 3 * 4};
    const int f{(2 + 3) * 4};

    std::cout << "a: " << a << "\n";
    std::cout << "b: " << b << "\n";
    std::cout << "c: " << c << "\n";
    std::cout << "d: " << d << "\n";
    std::cout << "e: " << e << "\n";
    std::cout << "f: " << f << "\n";
}
```

<details>
<summary>Wynik programu</summary>

<!-- output: predictions -->
```text
a: 4
b: 1
c: 18
d: 2
e: 14
f: 20
```

</details>

Wypełniona tabela z grupowaniem i opisem każdej pułapki jest w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 7. Program, który liczy coś innego

Dwie klasy idą razem na zajęcia sportowe. W pierwszej jest 14 uczniów, w drugiej 16. Wszyscy razem dzielą się na drużyny po 5 osób. **Wymaganie:** program ma wypisać, ile drużyn powstanie.

**Krok 1. Przewidź poprawny wynik** na podstawie samego opisu. Zapisz go.

**Krok 2. Przeczytaj program** i zastanów się, co naprawdę oblicza wyrażenie w `teams`:

<!-- example: teams_bug -->
```cpp
#include <iostream>

int main() {
    const int first_class_pupils{14};
    const int second_class_pupils{16};
    const int team_size{5};

    const int teams{first_class_pupils + second_class_pupils / team_size};

    std::cout << "Teams: " << teams << "\n";
}
```

**Krok 3. Uruchom program** i porównaj wynik z przewidywaniem.

<details>
<summary>Wynik programu</summary>

<!-- output: teams_bug -->
```text
Teams: 17
```

</details>

Program się zbudował i działa, ale 17 drużyn po 5 osób to 85 osób, a uczniów jest 30.

**Krok 4. Znajdź przyczynę.** Dopisz do wyrażenia w `teams` niewidoczne nawiasy, tak jak w punkcie 5. Które działanie wykonuje się z którym? Możesz też wypisać część wyrażenia przez `std::cout` albo, jeśli debugger działa u Ciebie od lekcji 2.3, rozpisać obliczenie na kilka stałych i obejrzeć ich wartości. Nie jest to tu konieczne: wystarczy uważnie przeczytać wyrażenie.

**Krok 5. Popraw wyrażenie** tak, żeby obliczało to, czego wymaga opis.

**Krok 6. Sprawdź wynik.** Po poprawce program ma wypisać:

<!-- output: teams_fixed -->
```text
Teams: 6
```

<details>
<summary>Wyjaśnienie i poprawiony program: przeczytaj po własnej próbie</summary>

`/` łączy się przed `+`, więc wyrażenie znaczy `first_class_pupils + (second_class_pupils / team_size)`. Na drużyny dzieli się tylko druga klasa: `16 / 5` daje 3, a do tego program dodaje całą pierwszą klasę, 14 uczniów. Wychodzi 17, czyli liczba bez sensu: część to uczniowie, część to drużyny.

Zamierzone obliczenie to „najpierw dodaj wszystkich uczniów, potem podziel przez wielkość drużyny”. Dodawanie musi więc trafić do nawiasu:

<!-- example: teams_fixed -->
```cpp
#include <iostream>

int main() {
    const int first_class_pupils{14};
    const int second_class_pupils{16};
    const int team_size{5};

    const int teams{(first_class_pupils + second_class_pupils) / team_size};

    std::cout << "Teams: " << teams << "\n";
}
```

Teraz `30 / 5` daje 6.

</details>

## 8. Misja: zestawy identyfikatorów

Organizatorzy szkolnego festiwalu mają 29 identyfikatorów. Do każdego zestawu dla drużyny wkładają 6 identyfikatorów. Chcą wiedzieć, ile **pełnych** zestawów przygotują i ile identyfikatorów zostanie niewykorzystanych.

W `cpp-workspace` utwórz katalog `badge_kits`, skopiuj do niego `CMakeLists.txt` z oryginalnego `lesson_05_first_program`, utwórz pusty `main.cpp` i napisz program samodzielnie. Program ma wypisać dokładnie:

<!-- output: badge_kits -->
```text
Badges: 29
Badges per kit: 6
Full kits: 4
Badges left: 5
```

### Kryterium sukcesu

- Program buduje się jako C++20 i wypisuje dokładnie powyższy wynik.
- Liczba identyfikatorów i liczba identyfikatorów w zestawie mają własne zmienne z sensownymi nazwami po angielsku, z wartościami początkowymi.
- Wartości, które w programie się nie zmieniają, mają `const`.
- Liczbę pełnych zestawów oblicza `/`, a liczbę pozostałych identyfikatorów `%`. Liczby 4 i 5 **oblicza program**: nie występują w kodzie.
- Liczby 29 i 6 występują w kodzie **tylko raz**, w deklaracjach. Obliczenia i wypisywanie korzystają ze zmiennych. Dzięki temu w wariancie wystarczy zmienić jedną wartość.
- Program używa tylko tego, co już znasz: `int`, `const`, `{}`, `+`, `-`, `*`, `/`, `%` i `std::cout`.
- Umiesz sprawdzić wynik bez komputera: pełne zestawy razy 6, plus pozostałe identyfikatory, daje 29.

Gdy wynik się zgadza, możesz zapisać projekt w Gicie, jak w lekcji 1.5.

<details>
<summary>Podpowiedź 1</summary>

Pytanie „ile pełnych zestawów” to pytanie o liczbę pełnych grup. Pytanie „ile zostanie” to pytanie o resztę. Które operatory na nie odpowiadają?

</details>

<details>
<summary>Podpowiedź 2</summary>

Wystarczą cztery stałe: dwie z danymi i dwie z wynikami obliczeń. Każdą wypisz w osobnej linijce, w kolejności z wymaganego wyniku.

</details>

### Wariant: więcej identyfikatorów

Do organizatorów trafiły dodatkowe identyfikatory i jest ich teraz 32. **Przewidź** nowe wyniki, a potem zmień w programie **tylko jedną wartość początkową**. Wynik ma być taki:

<!-- output: badge_kits_variant -->
```text
Badges: 32
Badges per kit: 6
Full kits: 5
Badges left: 2
```

**I jeszcze jedno pytanie:** ile zostanie, jeśli identyfikatorów będzie 30? Przewidź, sprawdź w programie, a potem porównaj:

<details>
<summary>Wynik dla 30 identyfikatorów</summary>

<!-- output: badge_kits_exact -->
```text
Badges: 30
Badges per kit: 6
Full kits: 5
Badges left: 0
```

30 dzieli się przez 6 bez reszty, więc `%` daje 0. Reszta równa zero to zwykły, poprawny wynik.

</details>

Przykładowe rozwiązania są w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 9. Gdy coś pójdzie inaczej

| Co widzisz | Co to znaczy | Co zrobić |
|---|---|---|
| Oczekiwano 3,5, a program wypisuje 3 | Oba operandy są całkowite, więc `/` wykonuje dzielenie całkowite. | Tak ma być. Jeśli potrzebujesz reszty, użyj `%`. Liczby z częścią ułamkową poznasz w lekcji 2.5. |
| Wynik to liczba „pozostałych”, a miała być liczba pełnych grup (albo odwrotnie) | `/` i `%` zamieniły się miejscami. | `/` daje pełne grupy, `%` daje resztę. |
| Wynik dłuższego wyrażenia jest inny niż przewidywany | Działania pogrupowały się inaczej, niż zakładano. | Dopisz niewidoczne nawiasy według punktu 5. Zamierzone grupowanie zapisz prawdziwymi nawiasami. |
| `20 / 5 * 2` daje 8, a oczekiwano 2 | Założono, że mnożenie jest przed dzieleniem. | `*` i `/` są na tym samym poziomie i łączą się od lewej. Napisz `20 / (5 * 2)`, jeśli tak ma być. |
| W wyrażeniu jest dzielenie przez zero albo `% 0` | Niezdefiniowane zachowanie, nawet jeśli program się zbudował. | Usuń je. Dzielnik musi być liczbą dodatnią. |
| `%` miał policzyć procenty | `%` to reszta z dzielenia, nie procenty. | Procentów nie liczymy w tej lekcji. |

## 10. Wyjaśnij

Odpowiedz własnymi słowami, najlepiej na piśmie. Dopiero potem porównaj z przykładową odpowiedzią.

**1.** Dlaczego `7 / 2` daje w C++ `3`?

<details>
<summary>Przykładowa odpowiedź</summary>

Oba operandy są typu `int`, więc `/` wykonuje dzielenie całkowite. Wynik to pełna część ilorazu, czyli ile razy 2 mieści się w 7 w całości. Część ułamkowa nie zostaje zachowana i nic nie jest zaokrąglane.

</details>

**2.** Czy część ułamkowa w `const int result{7 / 2};` znika dlatego, że wynik trafia do zmiennej typu `int`?

<details>
<summary>Przykładowa odpowiedź</summary>

Nie. Znika już w samym dzieleniu: `7 / 2` od razu daje 3. Widać to w punkcie 2, gdzie `(7 / 2)` wypisane bez zmiennej też daje 3.

</details>

**3.** Czym różnią się `/` i `%`? Wyjaśnij na przykładzie 17 kredek w pudełkach po 5.

<details>
<summary>Przykładowa odpowiedź</summary>

`17 / 5` daje 3, czyli liczbę pełnych pudełek. `17 % 5` daje 2, czyli liczbę kredek, które zostaną. 3 pudełka po 5 i 2 kredki to razem 17.

</details>

**4.** Ile wynosi `20 / 5 * 2` i dlaczego nie 2?

<details>
<summary>Przykładowa odpowiedź</summary>

8. `/` i `*` są na tym samym poziomie i łączą się od lewej do prawej, więc wyrażenie znaczy `(20 / 5) * 2`, czyli 4 · 2. Wynik 2 dałoby `20 / (5 * 2)`.

</details>

**5.** Dlaczego w tej lekcji dzielnik jest zawsze znaną liczbą dodatnią?

<details>
<summary>Przykładowa odpowiedź</summary>

Bo dzielenie całkowite przez zero i reszta z dzielenia przez zero mają w C++ niezdefiniowane zachowanie. Sprawdzać dzielnik, którego nie znamy z góry, nauczymy się później. Tutaj dzielnik jest liczbą dodatnią wpisaną w kodzie.

</details>

## Podsumowanie

- Gdy oba operandy są całkowite, `/` wykonuje **dzielenie całkowite**: dla liczb dodatnich daje pełną część ilorazu, bez zaokrąglania. Część ułamkowa znika już w samym dzieleniu.
- `%` daje **resztę z dzielenia**. `/` i `%` razem odpowiadają na pytania „ile pełnych grup?” i „ile zostanie?”. `%` nie ma nic wspólnego z procentami.
- **Nie wolno** dzielić ani obliczać reszty przez zero: to niezdefiniowane zachowanie.
- `*`, `/` i `%` łączą się przed `+` i `-`. Operatory na tym samym poziomie grupują się w tych wyrażeniach od lewej do prawej. „Mnożenie przed dzieleniem” to błędna reguła.
- Nawiasy zmieniają grupowanie i pomagają czytelnikowi. Zamierzone obliczenie warto zapisać nawiasami.
- Przy dłuższym wyrażeniu najpierw dopisz niewidoczne nawiasy, potem licz.

## Co dalej

Dzielenie liczb całkowitych daje liczby całkowite. A co, jeśli potrzebujesz wyniku 3,5, na przykład średniej albo ceny za kilogram? Liczby z częścią ułamkową poznasz w lekcji 2.5. **Lekcja 2.5 jest w przygotowaniu.**

---

## Przykładowe rozwiązania

Zajrzyj tutaj **po własnej próbie**. Twoje nazwy mogą się różnić, jeśli wynik jest taki, jak wymagany.

<details>
<summary>Punkt 6: sześć wyrażeń</summary>

| | Wyrażenie | Grupowanie | Wynik | Pułapka |
|---|---|---|---|---|
| a | `17 / 4` | — | 4 | Oczekiwanie wyniku ułamkowego (4,25). Dzielenie całkowite daje pełną część: 4. |
| b | `17 % 4` | — | 1 | Mylenie `%` z `/`. 4 czwórki to 16, zostaje 1. |
| c | `12 / 2 * 3` | `(12 / 2) * 3` | 18 | Założenie, że mnożenie jest przed dzieleniem. Daje to 2 zamiast 18. |
| d | `12 / (2 * 3)` | nawias już jest | 2 | Pominięcie nawiasu. Bez niego wyszłoby 18. |
| e | `2 + 3 * 4` | `2 + (3 * 4)` | 14 | Liczenie od lewej bez priorytetów: (2 + 3) · 4 = 20. |
| f | `(2 + 3) * 4` | nawias już jest | 20 | Pominięcie nawiasu. Bez niego wyszłoby 14. |

</details>

<details>
<summary>Punkt 8: misja, zestawy identyfikatorów</summary>

<!-- example: badge_kits -->
```cpp
#include <iostream>

int main() {
    const int badges{29};
    const int badges_per_kit{6};

    const int full_kits{badges / badges_per_kit};
    const int badges_left{badges % badges_per_kit};

    std::cout << "Badges: " << badges << "\n";
    std::cout << "Badges per kit: " << badges_per_kit << "\n";
    std::cout << "Full kits: " << full_kits << "\n";
    std::cout << "Badges left: " << badges_left << "\n";
}
```

- Ani liczba identyfikatorów, ani wielkość zestawu nie zmieniają się w trakcie działania programu, więc obie mają `const`. Wyniki obliczeń też się nie zmieniają.
- Sprawdzenie: 4 · 6 + 5 = 29.

</details>

<details>
<summary>Punkt 8: wariant z 32 identyfikatorami</summary>

<!-- example: badge_kits_variant -->
```cpp
#include <iostream>

int main() {
    const int badges{32};
    const int badges_per_kit{6};

    const int full_kits{badges / badges_per_kit};
    const int badges_left{badges % badges_per_kit};

    std::cout << "Badges: " << badges << "\n";
    std::cout << "Badges per kit: " << badges_per_kit << "\n";
    std::cout << "Full kits: " << full_kits << "\n";
    std::cout << "Badges left: " << badges_left << "\n";
}
```

Zmieniła się tylko wartość początkowa `badges`. Obliczenia zostały takie same. Sprawdzenie: 5 · 6 + 2 = 32.

</details>

<details>
<summary>Punkt 8: 30 identyfikatorów</summary>

<!-- example: badge_kits_exact -->
```cpp
#include <iostream>

int main() {
    const int badges{30};
    const int badges_per_kit{6};

    const int full_kits{badges / badges_per_kit};
    const int badges_left{badges % badges_per_kit};

    std::cout << "Badges: " << badges << "\n";
    std::cout << "Badges per kit: " << badges_per_kit << "\n";
    std::cout << "Full kits: " << full_kits << "\n";
    std::cout << "Badges left: " << badges_left << "\n";
}
```

Sprawdzenie: 5 · 6 + 0 = 30.

</details>

**Poprzednia lekcja:** [Lekcja 2.3: Zobacz, co dzieje się w programie](lesson_03_see_what_happens_in_the_program.md) · **Następna lekcja:** w przygotowaniu · [Opis kursu](../../README.md)

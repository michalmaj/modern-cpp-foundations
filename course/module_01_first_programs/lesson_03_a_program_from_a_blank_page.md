# Lekcja 1.3: Program od pustej kartki

**Polski** · [English](lesson_03_a_program_from_a_blank_page.en.md) · [Opis kursu](../../README.md)

> **Moduł 1, lekcja 3** · około 75 minut
> **Potrzebujesz:** katalogu `cpp-workspace` i oryginalnego projektu `lesson_05_first_program` z [lekcji 1.1](lesson_01_first_program_inside.md) oraz sposobu pracy z [lekcji 1.2](lesson_02_when_the_compiler_complains.md).
> **Wersja pilotażowa:** kroki w CLionie opisujemy według dokumentacji CLion 2026.2. W Twojej wersji nazwy przycisków mogą się nieznacznie różnić.

## Zanim zaczniesz

Ta lekcja zakłada, że po lekcjach 1.1 i 1.2:

- rozumiesz program wypisujący tekst: `#include <iostream>`, `main`, instrukcje `std::cout << "…";`, `\n` i średnik;
- umiesz zbudować program, uruchomić go i porównać wynik z oczekiwanym;
- przy błędzie kompilacji pracujesz w pętli z lekcji 1.2: **zobacz problem → przeczytaj diagnostykę → postaw hipotezę → popraw jedną rzecz → zbuduj ponownie → sprawdź wynik**.

## Sytuacja

Do tej pory zawsze był gotowy program albo prawie gotowy kod. Dziś zaczniesz od **pustego pliku** `main.cpp` i napiszesz w nim cały program sam.

Poznasz też cztery nowe drobiazgi, bo bez nich wiele prostych programów nie da się napisać: jak wypisać cudzysłów `"`, jak wypisać ukośnik odwrotny `\`, jak dodać komentarz i co znaczy `return 0;` na końcu `main`.

Po tej lekcji będziesz:

- zaczynać od pustego `main.cpp` i samodzielnie zapisywać szkielet programu;
- pisać program, który wypisuje kilka linijek w zadanej kolejności;
- wypisywać `"` i `\` wewnątrz tekstu i odróżniać to, co jest w kodzie, od tego, co pojawia się w wyniku;
- dodawać komentarze, które pomagają czytelnikowi, i wiedzieć, że nie są instrukcjami;
- wyjaśniać, czym jest kod zakończenia programu i czym różni się od tekstu wypisanego przez program;
- wyjaśniać każdą istotną linijkę własnego programu.

## 1. Przygotuj pusty `main.cpp`

„Od pustej kartki” znaczy tu: **sam piszesz `main.cpp`**. Plik `CMakeLists.txt` bierzesz gotowy, ten sam co zawsze.

1. W `cpp-workspace` utwórz katalog `lesson_1_3`.
2. Skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego katalogu kursu `lesson_05_first_program`, tak jak w lekcjach 1.1 i 1.2.
3. Otwórz `cpp-workspace/lesson_1_3` w CLionie i sprawdź w oknie CMake, czy jest `Clang 22`.
4. Otwórz `main.cpp` w edytorze CLiona. Zaznacz cały tekst (<kbd>Ctrl</kbd> + <kbd>A</kbd>, na macOS <kbd>⌘ Cmd</kbd> + <kbd>A</kbd>) i usuń go klawiszem <kbd>Delete</kbd> albo <kbd>Backspace</kbd>.

Usuwasz **zawartość** pliku, a nie sam plik. W oknie plików nic nie usuwaj: `main.cpp` i `CMakeLists.txt` mają zostać w katalogu. Programy z lekcji 1.1 i 1.2 są w swoich katalogach i nic się z nimi nie dzieje.

Pustego pliku jeszcze nie buduj. Program bez `main` się nie zbuduje, a ten błąd zgłasza inne narzędzie niż kompilator. Wrócimy do tego w lekcji 1.4.

## 2. Przypomnij sobie szkielet programu

Nie zaglądaj do poprzednich lekcji. Odpowiedz z pamięci, najlepiej na kartce, a dopiero potem sprawdź.

**1.** Co musi stać na samej górze pliku, żeby kompilator znał `std::cout`? Czy ta linijka kończy się średnikiem?

<details>
<summary>Sprawdź</summary>

`#include <iostream>`. To dyrektywa preprocesora, a nie instrukcja, więc nie kończy się średnikiem.

</details>

**2.** Jak zaczyna się i jak kończy część programu, którą komputer wykonuje po uruchomieniu?

<details>
<summary>Sprawdź</summary>

Zaczyna się od `int main() {`, a kończy klamrą `}`. Instrukcje piszesz między nimi.

</details>

**3.** Jak wygląda instrukcja, która wypisuje jedną linijkę tekstu i przechodzi do następnej? Z jakich czterech części się składa?

<details>
<summary>Sprawdź</summary>

`std::cout << "tekst\n";` – miejsce wysyłania tekstu (`std::cout`), „wyślij do” (`<<`), napis w cudzysłowie zakończony `\n` i średnik.

</details>

## 3. Pierwszy program od pustej kartki

Kawiarnia na rogu potrzebuje programu, który wypisze tabliczkę na drzwi. **W pustym `main.cpp` napisz cały program**, który wypisze dokładnie:

<!-- output: coffee_corner -->
```text
COFFEE CORNER
Open: 8:00 - 16:00
Please come in!
```

Potrzebujesz tylko tego, co już znasz. Nie kopiuj kodu z poprzednich lekcji: napisz go z klawiatury.

Gdy skończysz: **Build | Build Project**, a potem **Run**. Porównaj wynik z oczekiwanym znak po znaku. Jeśli budowanie się nie uda, pracuj w pętli z lekcji 1.2.

<details>
<summary>Podpowiedź 1</summary>

Zacznij od szkieletu z punktu 2: trzy elementy, bez żadnej instrukcji w środku. Dopiero potem dopisuj instrukcje.

</details>

<details>
<summary>Podpowiedź 2</summary>

Napisz szkielet i jedną instrukcję, dla pierwszej linijki, i zbuduj program. Gdy działa, dopisz kolejne. Mały krok łatwiej sprawdzić.

</details>

Przykładowe rozwiązanie jest w części [Przykładowe rozwiązania](#przykładowe-rozwiązania). Zajrzyj tam dopiero po udanej próbie.

**Zatrzymaj się na chwilę.** To był Twój pierwszy program napisany w całości samodzielnie, od pierwszej do ostatniej linijki, bez gotowego wzoru.

## 4. Cudzysłów i ukośnik odwrotny w napisie

### Cudzysłów

Program ma wypisać:

<!-- output: press_one -->
```text
Press "1" to start.
```

Pierwsza próba, która się nasuwa:

<!-- broken: press_one_plain at=4:26 errors=2 error=^expected ';' after expression$ -->
```cpp
#include <iostream>

int main() {
    std::cout << "Press "1" to start.\n";
}
```

**Przewidź:** czy ten program się zbuduje? Potem sprawdź: zastąp nim zawartość `main.cpp` i zbuduj. Programem z kawiarnią się nie przejmuj, w punkcie 6 napiszesz go jeszcze raz.

Przejdź przez pętlę z lekcji 1.2. Komunikat mówi o brakującym średniku, a przecież średnik jest na końcu linijki. Spójrz na **pozycję**, którą wskazuje kompilator. Co stoi tuż przed nią?

<details>
<summary>Wyjaśnienie: przeczytaj po własnej próbie</summary>

Kompilator czyta napis od `"` do **następnego** `"`. Napis `"Press "` kończy się więc na drugim cudzysłowie. Zaraz za nim stoi `1`, a kompilator oczekiwał w tym miejscu końca instrukcji. Stąd `expected ';' after expression` na pozycji, gdzie zaczyna się `1`.

Komunikat dobrze wskazuje **miejsce**, ale jego propozycja, czyli średnik, nie jest tu rozwiązaniem. Hipoteza musi wyjaśniać przyczynę: drugi cudzysłów zakończył napis za wcześnie.

Ten sam problem daje drugi błąd tuż obok, na pozycji 27, i dwie linijki `warning:` (ostrzeżenie: kompilator zauważył coś podejrzanego, ale ostrzeżenie samo nie przerywa budowania). Wszystkie mają jedną przyczynę, jak w lekcji 1.2: popraw ją, a znikną razem.

</details>

Żeby cudzysłów był **częścią napisu**, a nie jego końcem, poprzedź go ukośnikiem odwrotnym: `\"`.

<!-- example: press_one -->
```cpp
#include <iostream>

int main() {
    std::cout << "Press \"1\" to start.\n";
}
```

W kodzie stoi `\"`, a w wyniku pojawia się sam `"`.

### Ukośnik odwrotny

**Przewidź**, co wypisze ten program, i zapisz odpowiedź. Potem go uruchom.

<!-- example: path_plain -->
```cpp
#include <iostream>

int main() {
    std::cout << "C:\new\notes.txt\n";
}
```

<details>
<summary>Wynik programu</summary>

<!-- output: path_plain -->
```text
C:
ew
otes.txt
```

</details>

Program się zbudował, ale wypisał coś innego, niż sugeruje kod. W napisie ukośnik odwrotny `\` rozpoczyna **specjalny zapis**: razem z następnym znakiem znaczy coś innego niż te dwa znaki osobno. `\n` w środku ścieżki zrobiło więc to samo co zawsze: przeszło do nowej linii. Kompilator nie zgłosił błędu, bo kod jest poprawnym C++, tylko robi coś innego, niż chcieliśmy (lekcja 1.2).

Żeby wypisać jeden ukośnik odwrotny, zapisz w napisie **dwa**: `\\`.

<!-- example: path_fixed -->
```cpp
#include <iostream>

int main() {
    std::cout << "C:\\new\\notes.txt\n";
}
```

<!-- output: path_fixed -->
```text
C:\new\notes.txt
```

### Kod a wynik

| W kodzie, wewnątrz `"…"` | W wyniku programu |
|---|---|
| `\n` | przejście do nowej linii |
| `\"` | `"` |
| `\\` | `\` |

Takich zapisów jest w C++ kilka więcej. Poznasz je, gdy będą potrzebne. Te trzy wystarczą do większości tekstów.

## 5. Komentarze

**Komentarz** to notatka dla ludzi czytających kod. Zaczyna się od `//` i trwa do końca linijki. Kompilator go pomija, więc komentarz **nie jest instrukcją** i nic nie robi, gdy program działa.

**Przewidź**, ile linijek wypisze ten program i jakie:

<!-- example: comments -->
```cpp
#include <iostream>

int main() {
    // The sign hangs on the door, so every line must stay short.
    std::cout << "COFFEE CORNER\n";
    std::cout << "Comments start with // in C++.\n";
}
```

<details>
<summary>Wynik programu</summary>

<!-- output: comments -->
```text
COFFEE CORNER
Comments start with // in C++.
```

</details>

- Pierwsza linijka w `main` to komentarz: nic nie wypisuje.
- `//` **wewnątrz cudzysłowów** nie jest komentarzem, tylko zwykłym tekstem napisu. Kompilator najpierw widzi `"` i wie, że to napis.

**Dobry komentarz** mówi to, czego nie widać w samym kodzie: dlaczego coś jest tak zrobione. Komentarz `// prints COFFEE CORNER` nad `std::cout << "COFFEE CORNER\n";` tylko powtarza kod, więc nie pomaga. W programach w tym kursie komentarzy będzie niewiele, i tylko tam, gdzie coś wymaga wyjaśnienia.

**Obserwacja:** w tym programie wstaw `//` na początku drugiej instrukcji, zbuduj go i uruchom. Ta linijka zniknie z wyniku, bo instrukcja stała się komentarzem. Tak można na chwilę **wyłączyć** fragment kodu, na przykład szukając przyczyny problemu. To coś innego niż komentarz, który coś wyjaśnia. Po obserwacji usuń `//`, żeby instrukcja znów działała.

## 6. `return 0;` i kod zakończenia

Za każdym razem, gdy program kończył działanie, CLion dopisywał pod jego wynikiem `Process finished with exit code 0`. Skąd to `0`?

- `main` to **funkcja**: nazwany fragment programu. Funkcję `main` uruchamia system, gdy startuje Twój program.
- Kończąc działanie, `main` przekazuje temu, kto uruchomił program, **jedną liczbę całkowitą**: **kod zakończenia** (ang. *exit code*). Słowo `int` przed `main` oznacza właśnie „liczba całkowita”. Typy poznasz dokładnie w Module 2.
- `0` znaczy umownie „wszystko w porządku”. Inna liczba znaczy „coś poszło nie tak”, a co dokładnie, ustala autor programu.
- Instrukcja `return 0;` kończy `main` i przekazuje kod `0`.
- **Gdy program dojdzie do końca `main` bez `return`, działa to tak samo jak `return 0;`.** Dlatego wszystkie dotychczasowe programy kończyły się kodem 0, choć nie miały `return`. W `main` możesz więc pisać `return 0;` na końcu, żeby pokazać to wprost, albo go pominąć. Obie wersje są poprawne.

**Eksperyment.** Napisz jeszcze raz, z pamięci, program z kawiarnią z punktu 3. To dobra powtórka. Dopisz w nim `return 3;` jako ostatnią instrukcję w `main`, przed `}`. Zbuduj i uruchom.

<!-- example: coffee_corner_exit_3 exit=3 -->
```cpp
#include <iostream>

int main() {
    std::cout << "COFFEE CORNER\n";
    std::cout << "Open: 8:00 - 16:00\n";
    std::cout << "Please come in!\n";
    return 3;
}
```

**Przewidź:** czy wynik programu się zmieni? A ostatnia linijka w oknie Run?

<details>
<summary>Co się stało</summary>

<!-- output: coffee_corner_exit_3 -->
```text
COFFEE CORNER
Open: 8:00 - 16:00
Please come in!
```

Program wypisał te same trzy linijki co wcześniej, a CLion pokazał `Process finished with exit code 3`. Kod zakończenia **nie jest częścią wyniku programu**: program go nie wypisuje, tylko przekazuje systemowi. Linijkę `Process finished …` dopisuje CLion.

</details>

Na koniec zmień `return 3;` na `return 0;`. Od teraz możesz kończyć `main` instrukcją `return 0;`.

## 7. Misja: bilet do kina

Kino chce wydrukować bilet z programu. W katalogu `cpp-workspace` utwórz katalog `cinema_ticket`, skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program`, otwórz go w CLionie i sprawdź `Clang 22`. Potem **usuń całą zawartość `main.cpp`**, tak jak w punkcie 1, i napisz program od pustej kartki.

Program ma wypisać dokładnie:

<!-- output: cinema_ticket -->
```text
CINEMA TICKET
Film: "The Long Night"
Row 7, seat 12
File: C:\tickets\night.txt
Enjoy the film!
```

**Możesz używać:** `#include <iostream>`, `int main() { … }`, `std::cout << "…";`, `\n`, `\"`, `\\`, komentarzy `//` i `return 0;`. Nic więcej nie jest potrzebne.

### Kryterium sukcesu

- `main.cpp` napisano od pustego pliku, bez kopiowania wcześniejszych programów.
- Program buduje się bez błędów i wypisuje **dokładnie** pięć linijek powyżej: te same znaki, cudzysłowy i ukośniki, bez dodatkowych linijek.
- CLion pokazuje `Process finished with exit code 0`.
- Program ma co najmniej jeden komentarz, który wyjaśnia coś nieoczywistego, a nie powtarza kod.
- Umiesz wyjaśnić każdą linijkę programu: co robi i dlaczego jest zapisana właśnie tak.

<details>
<summary>Podpowiedź 1</summary>

Najpierw szkielet, potem jedna linijka biletu na raz. Po każdej dopisanej instrukcji zbuduj program i porównaj wynik.

</details>

<details>
<summary>Podpowiedź 2</summary>

Przejrzyj oczekiwany wynik znak po znaku. Które znaki mają specjalne znaczenie wewnątrz napisu w C++? Ile ich jest w każdej linijce?

</details>

### Wariant: sprawdź, czy rozumiesz własny kod

Bez zaglądania do rozwiązania zmień swój program tak, żeby wypisał:

<!-- output: cinema_ticket_variant -->
```text
CINEMA TICKET
Film: "The Short Day"
File: C:\tickets\day.txt
Row 3, seat 4
Enjoy the film!
```

Zmieniły się dwie linijki i kolejność dwóch innych. Jeśli rozumiesz swój program, wystarczy kilka zmian.

Przykładowe rozwiązania misji i wariantu są w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 8. Gdy coś pójdzie inaczej

| Co widzisz | Co to znaczy | Co zrobić |
|---|---|---|
| Błąd w linijce z cudzysłowem w napisie, choć komunikat mówi o czymś innym, na przykład o średniku albo o `invalid suffix on literal` (na Windowsie ten drugi bywa ostrzeżeniem `warning`) | Cudzysłów w środku napisu zakończył go za wcześnie. | Sprawdź, czy każdy `"`, który ma się pojawić w wyniku, jest zapisany jako `\"`. |
| Program się buduje, ale w ścieżce brakuje liter, jest nowa linia albo odstęp | Pojedynczy `\` z następną literą to specjalny zapis, na przykład `\n` (nowa linia) albo `\t` (odstęp, tzw. tabulator). | Zapisz każdy ukośnik, który ma się pojawić w wyniku, jako `\\`. |
| Budowanie się nie udaje, a pliku `main.cpp` prawie nie ma albo brakuje w nim `main` | Bez `main` nie powstanie program. Ten błąd zgłasza inne narzędzie niż kompilator (lekcja 1.4). | Napisz szkielet programu z `int main() { … }`. |
| Linijka zniknęła z wyniku | Instrukcja zaczyna się od `//`, więc jest komentarzem. | Usuń `//` przed instrukcją. |
| CLion pokazuje `exit code` inny niż 0 | `main` zwraca inną liczbę, na przykład `return 3;`. | Zmień na `return 0;` albo usuń `return`. |
| Zniknął plik `main.cpp` albo `CMakeLists.txt` | Usunięto plik zamiast jego zawartości. | Skopiuj go ponownie z oryginalnego `lesson_05_first_program`. |

## 9. Wyjaśnij

Odpowiedz własnymi słowami, najlepiej na piśmie. Dopiero potem porównaj z przykładową odpowiedzią.

**1.** W kodzie stoi `"C:\\tickets\\night.txt\n"`. Ile ukośników odwrotnych pojawi się w wyniku i dlaczego?

<details>
<summary>Przykładowa odpowiedź</summary>

Dwa. Każde `\\` w napisie oznacza jeden `\` w wyniku. `\n` na końcu nie wypisuje ukośnika, tylko przechodzi do nowej linii.

</details>

**2.** Czy dopisanie komentarza może zmienić wynik programu? A wstawienie `//` przed instrukcję?

<details>
<summary>Przykładowa odpowiedź</summary>

Komentarz niczego nie zmienia, bo kompilator go pomija. Wstawienie `//` przed instrukcję zmienia wynik, bo instrukcja staje się komentarzem i przestaje być wykonywana.

</details>

**3.** Program wypisał „Everything went wrong!”, a CLion pokazał `exit code 0`. Czy to sprzeczność?

<details>
<summary>Przykładowa odpowiedź</summary>

Nie. Tekst to wynik programu, a kod zakończenia to osobna liczba przekazywana systemowi. Program może wypisać dowolny tekst i zakończyć się kodem 0, bo te dwie rzeczy są od siebie niezależne.

</details>

**4.** Dlaczego wszystkie programy z lekcji 1.1 i 1.2 kończyły się kodem 0, choć nie miały `return 0;`?

<details>
<summary>Przykładowa odpowiedź</summary>

Bo gdy program dochodzi do końca `main` bez `return`, działa to tak samo jak `return 0;`.

</details>

**5.** Wybierz z misji linijkę, która była dla Ciebie najtrudniejsza, i wyjaśnij każdy jej znak, który nie pojawia się w wyniku.

<details>
<summary>Przykładowa odpowiedź</summary>

Na przykład `std::cout << "Film: \"The Long Night\"\n";`. W wyniku nie ma: `std::cout <<` (wysłanie tekstu), cudzysłowów otwierającego i zamykającego napis, ukośników przed wewnętrznymi cudzysłowami (`\"` daje sam `"`), `\n` (przejście do nowej linii) i średnika (koniec instrukcji).

</details>

## Podsumowanie

- Program od pustej kartki zaczynasz od szkieletu: `#include <iostream>`, `int main() {`, `}`. Instrukcje dopisujesz po jednej i budujesz po każdej.
- W napisie `\` rozpoczyna specjalny zapis: `\n` to nowa linia, `\"` to cudzysłów, `\\` to jeden ukośnik odwrotny. To, co widzisz w kodzie, nie zawsze jest tym, co pojawi się w wyniku.
- Komentarz `//` to notatka dla ludzi, a nie instrukcja. Pisz go tam, gdzie coś wymaga wyjaśnienia.
- `main` przekazuje systemowi kod zakończenia: `0` znaczy „w porządku”. `return 0;` robi to wprost; koniec `main` bez `return` działa tak samo. Kod zakończenia nie jest częścią wyniku programu.

Po tej lekcji możesz powiedzieć: **„Potrafię samodzielnie napisać mały program w C++, poprawić podstawowe błędy i sprawdzić jego działanie”.**

## Co dalej

Za każdym razem klikasz **Build** i powstaje program. W lekcji 1.4 zobaczysz, co dzieje się po drodze: jak kod źródłowy staje się plikiem wykonywalnym i co opisuje `CMakeLists.txt`. **Lekcja 1.4 jest w przygotowaniu.**

---

## Przykładowe rozwiązania

Zajrzyj tutaj **po własnej próbie**. Twój kod może się różnić, na przykład komentarzami, pustymi linijkami albo tym, czy na końcu jest `return 0;`, i nadal być dobry, jeśli spełnia kryteria.

<details>
<summary>Punkt 3: tabliczka kawiarni</summary>

<!-- example: coffee_corner -->
```cpp
#include <iostream>

int main() {
    std::cout << "COFFEE CORNER\n";
    std::cout << "Open: 8:00 - 16:00\n";
    std::cout << "Please come in!\n";
}
```

Szkielet z trzech elementów, a w nim trzy instrukcje w kolejności linijek wyniku. Każdy napis kończy się `\n`.

</details>

<details>
<summary>Punkt 7: misja, bilet do kina</summary>

<!-- example: cinema_ticket -->
```cpp
#include <iostream>

int main() {
    std::cout << "CINEMA TICKET\n";
    std::cout << "Film: \"The Long Night\"\n";
    std::cout << "Row 7, seat 12\n";
    // Each \\ in the code prints one backslash.
    std::cout << "File: C:\\tickets\\night.txt\n";
    std::cout << "Enjoy the film!\n";
    return 0;
}
```

- Cudzysłowy wokół tytułu filmu są częścią tekstu, więc każdy jest zapisany jako `\"`.
- W ścieżce każdy `\` jest zapisany jako `\\`. Pojedynczy dałby `\t` (tabulator) i `\n` (nową linię) zamiast liter.
- Komentarz wyjaśnia linijkę, która mogłaby zaskoczyć czytelnika.
- `return 0;` na końcu jest opcjonalne; pokazuje wprost, że program kończy się poprawnie.

</details>

<details>
<summary>Punkt 7: wariant</summary>

<!-- example: cinema_ticket_variant -->
```cpp
#include <iostream>

int main() {
    std::cout << "CINEMA TICKET\n";
    std::cout << "Film: \"The Short Day\"\n";
    // Each \\ in the code prints one backslash.
    std::cout << "File: C:\\tickets\\day.txt\n";
    std::cout << "Row 3, seat 4\n";
    std::cout << "Enjoy the film!\n";
    return 0;
}
```

Zmieniły się teksty dwóch instrukcji, a dwie inne zamieniły się miejscami. Komentarz przesunął się razem z linijką, którą wyjaśnia.

</details>

**Poprzednia lekcja:** [Lekcja 1.2: Gdy kompilator protestuje](lesson_02_when_the_compiler_complains.md) · **Następna lekcja:** w przygotowaniu · [Opis kursu](../../README.md)

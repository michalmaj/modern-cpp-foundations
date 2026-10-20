# Lekcja 1.1: Pierwszy program od środka

**Polski** · [English](lesson_01_first_program_inside.en.md) · [Opis kursu](../../README.md)

> **Moduł 1, lekcja 1** · około 60 minut
> **Potrzebujesz:** projektu `lesson_05_first_program` z [lekcji 0.5](../module_00_tooling/lesson_05_first_program_in_clion.md) i CLiona z toolchainem `LLVM 22`, który utworzono w lekcji 0.5, punkt 4.
> **Wersja pilotażowa:** kroki w CLionie opisujemy według dokumentacji CLion 2026.2. W Twojej wersji nazwy przycisków mogą się nieznacznie różnić.

## Zanim zaczniesz

Ta lekcja zakłada, że po Module 0:

- umiesz tworzyć katalogi i kopiować pliki w oknie plików;
- umiesz otworzyć projekt w CLionie, zbudować go i uruchomić (**Run**);
- wiesz, że po zmianie kodu program trzeba zbudować ponownie, żeby zobaczyć nowy wynik.

## Sytuacja

W Module 0 program był dla Ciebie czarną skrzynką: zmieniał się w nim tylko tekst w cudzysłowie. Dziś zajrzysz do środka. Przeczytasz `main.cpp` linijka po linijce, będziesz przewidywać, co wypisze program, zmienisz go, a na końcu napiszesz pierwsze własne instrukcje w C++.

Dzisiejsza droga: **rozpoznaj → przewidź → zmień → uzupełnij → napisz → wyjaśnij**.

Po tej lekcji będziesz:

- pracować na własnej kopii projektu w katalogu `cpp-workspace`, a nie na materiałach kursu;
- wskazywać w programie `main`, czyli miejsce, od którego zaczyna się wykonywanie Twojego kodu;
- rozpoznawać instrukcje wypisujące tekst i ich części: `std::cout`, `<<`, napis w cudzysłowie i średnik;
- przewidywać, w jakiej kolejności program wypisze komunikaty;
- samodzielnie dopisywać instrukcje wypisujące tekst, budować program i sprawdzać wynik.

## 1. Przygotuj własne miejsce pracy

Katalog `lesson_05_first_program` należy do materiałów kursu. Od dziś traktuj go jak **oryginał**: nie pracujesz w nim, tylko kopiujesz z niego to, czego potrzebujesz. Pracujesz na **kopii** we własnym katalogu roboczym, `cpp-workspace`.

Dzięki temu:

- Twoja praca zostaje u Ciebie, nawet jeśli kiedyś pobierzesz materiały kursu ponownie;
- zawsze możesz wrócić do oryginalnego przykładu: wystarczy skopiować go jeszcze raz;
- każde większe zadanie może mieć własny katalog, więc nic nie nadpisuje poprzedniej pracy.

**Krok 1. Utwórz `cpp-workspace`.** Otwórz katalog domowy w oknie plików, tak jak w lekcji 0.2: w terminalu wpisz `cd ~`, a potem:

| Windows | macOS | Linux |
|---|---|---|
| `explorer .` | `open .` | `xdg-open .` |

Utwórz w nim katalog `cpp-workspace`, a w nim katalog `lesson_1_1`.

**Krok 2. Skopiuj projekt.** W drugim oknie plików otwórz katalog kursu `lesson_05_first_program` (pobrany w lekcji 0.5). Skopiuj z niego **tylko dwa pliki**: `main.cpp` i `CMakeLists.txt`.

1. Kliknij `main.cpp`, przytrzymaj <kbd>Ctrl</kbd> (na macOS <kbd>⌘ Cmd</kbd>) i kliknij `CMakeLists.txt`. Oba pliki są zaznaczone.
2. Skopiuj je: <kbd>Ctrl</kbd> + <kbd>C</kbd> (na macOS <kbd>⌘ Cmd</kbd> + <kbd>C</kbd>).
3. Przejdź do `cpp-workspace/lesson_1_1` i wklej: <kbd>Ctrl</kbd> + <kbd>V</kbd> (na macOS <kbd>⌘ Cmd</kbd> + <kbd>V</kbd>).

Używaj kopiowania i wklejania, a nie przeciągania: przeciągnięcie potrafi **przenieść** pliki zamiast je skopiować.

Nie kopiuj nic więcej. Katalogi budowania (`cmake-build-debug`, `build-terminal` i inne) to wyniki budowania tamtej kopii projektu, a ukryty katalog `.idea` to ustawienia CLiona dla tamtego miejsca. Dla nowej kopii CLion i CMake utworzą własne.

Sprawdź, czy masz taki układ:

```text
cpp-workspace
└── lesson_1_1
    ├── CMakeLists.txt
    └── main.cpp
```

**Krok 3. Otwórz kopię w CLionie.** Wybierz **File | Open** i wskaż katalog `cpp-workspace/lesson_1_1`. Jeśli CLion zapyta, czy otworzyć projekt w tym samym oknie (**This Window**), czy w nowym (**New Window**), wybierz **This Window**. Potem, jak w lekcji 0.5: **Trust Project**, a w oknie **CMake Profiles** zatwierdź profil **Debug** (**OK**).

**Krok 4. Sprawdź kompilator.** To nowy projekt, więc CLion mógł wybrać dla niego swój domyślny toolchain. W oknie **CMake** znajdź linijkę z `The CXX compiler identification is`. Musi w niej być **`Clang 22`**. Jeśli jest coś innego:

1. Otwórz ustawienia (**File | Settings**, na macOS **CLion | Settings**) i przejdź do **Build, Execution, Deployment | CMake**.
2. W profilu **Debug** w polu **Toolchain** wybierz `LLVM 22`. Toolchain z lekcji 0.5 nadal istnieje; trzeba go tylko wskazać dla tego projektu.
3. Kliknij **OK** i sprawdź okno CMake jeszcze raz.

**Krok 5. Zacznij od oryginalnego kodu.** W lekcjach 0.5 i 0.6 komunikat był zmieniany, więc Twój `main.cpp` może wyglądać inaczej. Otwórz `main.cpp` w kopii i sprawdź, czy wygląda dokładnie tak. Jeśli nie, zastąp całą jego zawartość tym kodem (skopiuj go stąd):

<!-- example: original source=../module_00_tooling/lesson_05_first_program/main.cpp -->
```cpp
#include <iostream>

int main() {
    std::cout << "Hello! My first C++20 program works.\n";
}
```

Kliknij **Run** (▶). W oknie Run pojawi się wynik programu:

<!-- output: original -->
```text
Hello! My first C++20 program works.
```

Pod nim CLion dopisze jeszcze `Process finished with exit code 0`. Ta linijka nie pochodzi z Twojego programu, tylko z CLiona, więc w tej lekcji pomijamy ją w oczekiwanych wynikach.

Wolisz budować w terminalu? Polecenia z [lekcji 0.6](../module_00_tooling/lesson_06_same_program_without_clion.md) działają tak samo w katalogu `cpp-workspace/lesson_1_1`.

## 2. Rozpoznaj: co jest w `main.cpp`

Program ma pięć linijek, w tym jedną pustą. Nie wszystkie musisz dziś rozumieć do końca.

| Linijka | Co robi | Dziś |
|---|---|---|
| `#include <iostream>` | Dołącza do programu tę część **biblioteki standardowej** C++ (gotowych narzędzi, które przychodzą razem z językiem), która wypisuje tekst. Bez niej program nie znałby `std::cout`. | Rozpoznaj. Więcej w lekcji 1.2. |
| (pusta linijka) | Nic. Jest tylko dla czytelności. | |
| `int main() {` | Początek **`main`**. Od tego miejsca zaczyna się wykonywanie Twojego kodu. Klamra `{` otwiera część, w której piszesz instrukcje. | Zapamiętaj: kod do wykonania piszesz między `{` a `}`. Znaczenie `int` poznasz później. |
| `std::cout << "Hello! My first C++20 program works.\n";` | **Instrukcja**, czyli jedno polecenie dla komputera. Ta wypisuje tekst. | Zrozum. Rozbieramy ją niżej. |
| `}` | Klamra zamykająca `main`. Gdy program tu dojdzie, kończy działanie. | Zrozum. |

Teraz najważniejsza linijka, kawałek po kawałku:

<!-- fragment -->
```cpp
std::cout << "Hello! My first C++20 program works.\n";
```

- **`std::cout`** to miejsce, do którego program wysyła tekst do wyświetlenia: okno Run w CLionie albo terminal. `std::` oznacza, że `cout` pochodzi z biblioteki standardowej. Na razie zawsze pisz je razem: `std::cout`.
- **`<<`** czytaj tutaj jako „wyślij do”: wyślij to, co stoi po prawej, do `std::cout`. Strzałki pokazują kierunek: tekst płynie w lewo, do `std::cout`.
- **`"…"`** to **napis**, czyli tekst w cudzysłowie (fachowo: *literał tekstowy*). Program wypisuje go dokładnie tak, jak go zapisano: z tymi samymi literami, spacjami i znakami. Same cudzysłowy oznaczają tylko początek i koniec napisu, nie pojawiają się w wyniku.
- **`\n`** na końcu napisu to nie dwa znaki do wypisania, tylko polecenie: „przejdź do nowej linii”. Jego działanie zobaczysz w punkcie 4.
- **`;`** (średnik) kończy instrukcję, trochę jak kropka kończy zdanie.

**Co możesz już bezpiecznie zmieniać, a czego na razie nie ruszaj?**

| Możesz zmieniać | Na razie zostaw bez zmian |
|---|---|
| tekst między cudzysłowami (bez polskich liter, o czym niżej) | `#include <iostream>` |
| liczbę instrukcji `std::cout << "…";` i ich kolejność, jeśli są między `{` a `}` | `int main() {` i zamykające `}` |
| | części każdej instrukcji: `std::cout`, `<<`, cudzysłowy i `;` |

W tym module komunikaty programów piszemy bez polskich liter. To nie jest ograniczenie C++: konsola Windowsa nie zawsze wyświetla je poprawnie bez dodatkowych ustawień, a tym zajmiemy się później.

**Sprawdź się:**

**1.** Ile instrukcji jest w `main`?

<details>
<summary>Odpowiedź</summary>

Jedna: linijka zaczynająca się od `std::cout` i zakończona średnikiem.

</details>

**2.** Które znaki z tej instrukcji widać w wyniku programu?

<details>
<summary>Odpowiedź</summary>

Tylko tekst między cudzysłowami, bez `\n`. Cudzysłowy, `std::cout`, `<<`, `\n` i `;` mówią komputerowi, co ma zrobić, ale same się nie wypisują. Zamiast `\n` w wyniku jest przejście do nowej linii.

</details>

## 3. Przewidź: dwie instrukcje

Zastąp całą zawartość `main.cpp` tym programem (skopiuj go stąd):

<!-- example: two_lines -->
```cpp
#include <iostream>

int main() {
    std::cout << "Good morning!\n";
    std::cout << "Time to write some C++.\n";
}
```

**Zanim klikniesz Run, przewidź:** ile linijek wypisze program i w jakiej kolejności? Zapisz odpowiedź, na przykład w notatkach.

Teraz kliknij **Run** i porównaj wynik ze swoim przewidywaniem.

<details>
<summary>Wynik programu</summary>

<!-- output: two_lines -->
```text
Good morning!
Time to write some C++.
```

</details>

**Co się stało?** Program wykonuje instrukcje w `main` **po kolei, od góry do dołu**. Najpierw pierwsza instrukcja wypisała swój tekst i przeszła do nowej linii (`\n`), potem druga zrobiła to samo.

## 4. Zmień: kolejność i nowa linia

### Zmiana 1: kolejność

**Cel:** program ma wypisać te same dwa komunikaty, ale w odwrotnej kolejności:

<!-- output: swapped -->
```text
Time to write some C++.
Good morning!
```

Nie zmieniaj tekstu. Zmień tylko kolejność instrukcji. W CLionie możesz wyciąć całą linijkę (<kbd>Ctrl</kbd> + <kbd>X</kbd>, na macOS <kbd>⌘ Cmd</kbd> + <kbd>X</kbd>, gdy kursor stoi w tej linijce) i wkleić ją w innym miejscu.

Kliknij **Run** i sprawdź wynik. Potem odpowiedz sobie: **dlaczego** wynik się zmienił, choć żaden tekst się nie zmienił?

### Zmiana 2: bez `\n`

W programie po zmianie 1 usuń `\n` z **pierwszej** instrukcji, tej z `Time to write some C++.`. Usuń tylko te dwa znaki, `\` i `n`; cudzysłów zamykający zostaje.

**Przewidź:** ile linijek wypisze teraz program? Gdzie zacznie się `Good morning!`? Zapisz odpowiedź, a potem kliknij **Run**.

<details>
<summary>Wynik programu</summary>

<!-- output: no_newline -->
```text
Time to write some C++.Good morning!
```

</details>

**Co się stało?** Nowa instrukcja nie zaczyna sama nowej linii. Do nowej linii przechodzi się tylko wtedy, gdy w napisie jest `\n`. Bez niego drugi tekst zaczyna się zaraz za pierwszym, nawet bez spacji.

Kod obu zmian znajdziesz w części [Przykładowe rozwiązania](#przykładowe-rozwiązania) na końcu lekcji. Zajrzyj tam po własnej próbie.

## 5. Uzupełnij: brakujący krok

Instrukcja montażu lampy ma trzy kroki, ale w programie brakuje środkowego. Zastąp całą zawartość `main.cpp` tym niekompletnym kodem:

<!-- fragment -->
```cpp
#include <iostream>

int main() {
    std::cout << "Step 1: Open the box.\n";
    _______________________________________
    std::cout << "Step 3: Plug in the lamp.\n";
}
```

**Twoje zadanie:** zastąp linijkę z podkreśleniami (`____`) **własną instrukcją**, tak żeby program wypisał dokładnie:

<!-- output: lamp_steps -->
```text
Step 1: Open the box.
Step 2: Take out the cable.
Step 3: Plug in the lamp.
```

Tę jedną instrukcję wpisz z klawiatury, nie kopiuj jej. Ten kod w obecnej postaci się nie zbuduje: podkreślenia nie są instrukcją C++. Program zbudujesz dopiero po uzupełnieniu.

**Sprawdź:** kliknij **Run** i porównaj wynik z oczekiwanym, znak po znaku, razem z kropkami i wielkością liter.

<details>
<summary>Podpowiedź 1</summary>

Która z istniejących linijek robi prawie to samo, co ma zrobić brakująca?

</details>

<details>
<summary>Podpowiedź 2</summary>

Twoja instrukcja ma ten sam kształt co linijka `Step 1`, tylko inny tekst w cudzysłowie. Na końcu napisu `\n`, na końcu instrukcji `;`.

</details>

Przykładowe rozwiązanie jest w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 6. Misja: etykieta paczki

Wysyłasz paczkę z czymś delikatnym i potrzebujesz programu, który wypisze etykietę do naklejenia.

**Przygotuj projekt.** Misja dostaje własny katalog, żeby nie nadpisać ćwiczeń z `lesson_1_1`:

1. W `cpp-workspace` utwórz katalog `parcel_label`.
2. Skopiuj do niego `main.cpp` i `CMakeLists.txt` z **oryginalnego** katalogu kursu `lesson_05_first_program`, tak jak w punkcie 1.
3. Otwórz `cpp-workspace/parcel_label` w CLionie i sprawdź w oknie CMake, czy jest `Clang 22` (punkt 1, krok 4).

Twój `cpp-workspace` wygląda teraz tak:

```text
cpp-workspace
├── lesson_1_1
│   ├── CMakeLists.txt
│   └── main.cpp
└── parcel_label
    ├── CMakeLists.txt
    └── main.cpp
```

**Zadanie.** Zmień `main.cpp` w `parcel_label` tak, żeby program wypisał dokładnie te trzy linijki:

<!-- output: parcel_label -->
```text
TO: Ola Nowak
FROM: Modern C++ Foundations
FRAGILE - HANDLE WITH CARE
```

Każdą linijkę wypisz osobną instrukcją. Kod piszesz sam: wszystko, czego potrzebujesz, już znasz.

### Kryterium sukcesu

- Program wypisuje **dokładnie** te trzy linijki, w tej kolejności: te same litery (także wielkie i małe), spacje, dwukropki i myślnik.
- Nie ma dodatkowych linijek, pustych linijek ani tekstu sklejonego w jednej linijce.
- Każda linijka wyniku pochodzi z osobnej instrukcji, a każda instrukcja kończy się średnikiem.
- Program zbudowano z katalogu `cpp-workspace/parcel_label`, a okno CMake pokazuje `Clang 22`.
- Umiesz wskazać, która instrukcja wypisuje którą linijkę.

<details>
<summary>Podpowiedź 1</summary>

Ile linijek ma wynik? Tyle instrukcji potrzebujesz. Który program z tej lekcji ma najbardziej podobny kształt?

</details>

<details>
<summary>Podpowiedź 2</summary>

Zacznij od jednej linijki: niech program wypisze tylko `TO: Ola Nowak`. Kliknij **Run** i sprawdź. Potem dopisz pod nią następną instrukcję i znowu sprawdź. Małe kroki łatwiej sprawdzić.

</details>

Przykładowe rozwiązanie jest w części [Przykładowe rozwiązania](#przykładowe-rozwiązania). Zajrzyj tam dopiero wtedy, gdy Twój program spełnia wszystkie kryteria albo gdy naprawdę utkniesz.

## 7. Gdy coś pójdzie inaczej

Gdy budowanie się nie udaje, CLion pokazuje komunikaty kompilatora w oknie **Build**. **Czytaj je od początku:** pierwszy komunikat `error:` zwykle wskazuje prawdziwą przyczynę. Dokładne czytanie takich komunikatów to temat lekcji 1.2.

| Co widzisz | Co to znaczy | Co zrobić |
|---|---|---|
| Dwa komunikaty sklejone w jednej linijce | W pierwszym napisie brakuje `\n`. | Dopisz `\n` na końcu napisu, przed cudzysłowem zamykającym. |
| Dodatkowa pusta linijka | Jeden napis ma `\n` dwa razy albo jest instrukcja, która wypisuje samo `\n`. | Każdy napis powinien kończyć się jednym `\n`. |
| Budowanie kończy się błędem (`error:`) | Kompilator nie rozumie jakiejś linijki. | Sprawdź po kolei: czy każda instrukcja kończy się `;`? Czy każdy napis ma cudzysłów na początku i na końcu? Czy instrukcje są między `{` a `}`? Czy zostały podkreślenia z punktu 5? |
| Błąd w linijce z napisem, choć wszystko wygląda dobrze | Cudzysłów może być „ozdobny” (`“` albo `”`), na przykład po skopiowaniu tekstu z dokumentu lub komunikatora. | Usuń cudzysłowy i wpisz je z klawiatury w CLionie: `"`. |
| Wynik z innego ćwiczenia | W CLionie jest otwarty inny projekt. | Sprawdź nazwę projektu u góry okna CLiona. Otwórz właściwy katalog (**File \| Open**). |
| Okno CMake pokazuje inny kompilator niż `Clang 22` | Ten projekt używa innego toolchainu. | Punkt 1, krok 4. Potem **Tools \| CMake \| Reset Cache and Reload Project**. |
| Inna wielkość liter albo brak spacji w wyniku | Program wypisuje napis dokładnie tak, jak go zapisano. | Porównaj napis w kodzie z oczekiwanym wynikiem, znak po znaku. |

## 8. Wyjaśnij

Odpowiedz własnymi słowami, najlepiej na piśmie. Dopiero potem porównaj z przykładową odpowiedzią.

**1.** Dlaczego komunikaty pojawiły się w takiej kolejności, a nie innej?

<details>
<summary>Przykładowa odpowiedź</summary>

Program wykonuje instrukcje w `main` po kolei, od góry do dołu. Komunikat z wyższej instrukcji pojawia się pierwszy. Po zamianie instrukcji miejscami zmieniła się kolejność komunikatów, choć tekst został ten sam.

</details>

**2.** Co robi każda instrukcja, którą dopisano w misji?

<details>
<summary>Przykładowa odpowiedź</summary>

Każda wysyła jeden napis do `std::cout`, czyli wypisuje go, a `\n` na końcu napisu przechodzi do nowej linii. Pierwsza wypisuje odbiorcę, druga nadawcę, trzecia ostrzeżenie.

</details>

**3.** Co trzeba zrobić po zmianie kodu, żeby zobaczyć nowy wynik?

<details>
<summary>Przykładowa odpowiedź</summary>

Zapisać plik, zbudować program ponownie i go uruchomić. Run w CLionie robi to za jednym kliknięciem: najpierw buduje, jeśli trzeba, potem uruchamia. W terminalu trzeba samodzielnie zbudować (`cmake --build …`) i uruchomić program.

</details>

**4.** Które elementy programu już rozumiesz, a które dopiero poznasz?

<details>
<summary>Przykładowa odpowiedź</summary>

Rozumiem: kod wykonuje się od `{` do `}` w `main`, od góry do dołu; `std::cout << "…";` wypisuje napis; `\n` przechodzi do nowej linii; `;` kończy instrukcję. Na razie tylko rozpoznaję: `#include <iostream>`, `int` przed `main` i `std::`. Ich znaczenie poznam w kolejnych lekcjach.

</details>

## Podsumowanie

- Pracujesz na **kopii** projektu w `cpp-workspace`. Oryginał z kursu zostaje nietknięty i zawsze możesz skopiować go jeszcze raz.
- Twój kod piszesz w **`main`**, między `{` a `}`. Program wykonuje instrukcje po kolei, od góry do dołu.
- `std::cout << "…";` to **instrukcja**, która wypisuje **napis**. Średnik ją kończy.
- Napis wypisuje się dokładnie tak, jak go zapisano. **`\n`** przechodzi do nowej linii; bez niego kolejny tekst pojawi się w tej samej linijce.
- Po zmianie kodu trzeba zbudować program ponownie; Run w CLionie robi to sam.

---

## Przykładowe rozwiązania

Zajrzyj tutaj **po własnej próbie** i po sprawdzeniu wyniku. Twoje rozwiązanie może się różnić, na przykład pustymi linijkami w kodzie, i nadal być dobre, jeśli program wypisuje dokładnie oczekiwany wynik.

<details>
<summary>Punkt 4, zmiana 1: kolejność</summary>

<!-- example: swapped -->
```cpp
#include <iostream>

int main() {
    std::cout << "Time to write some C++.\n";
    std::cout << "Good morning!\n";
}
```

Teksty się nie zmieniły, zmieniła się tylko kolejność instrukcji. Program wykonuje je od góry do dołu, więc najpierw wypisuje `Time to write some C++.`.

</details>

<details>
<summary>Punkt 4, zmiana 2: bez <code>\n</code></summary>

<!-- example: no_newline -->
```cpp
#include <iostream>

int main() {
    std::cout << "Time to write some C++.";
    std::cout << "Good morning!\n";
}
```

Pierwszy napis nie kończy się `\n`, więc program nie przechodzi do nowej linii i `Good morning!` pojawia się zaraz za kropką.

</details>

<details>
<summary>Punkt 5: brakujący krok</summary>

<!-- example: lamp_steps -->
```cpp
#include <iostream>

int main() {
    std::cout << "Step 1: Open the box.\n";
    std::cout << "Step 2: Take out the cable.\n";
    std::cout << "Step 3: Plug in the lamp.\n";
}
```

Nowa instrukcja stoi między dwiema istniejącymi, bo jej komunikat ma się pojawić między nimi.

</details>

<details>
<summary>Punkt 6: misja, etykieta paczki</summary>

<!-- example: parcel_label -->
```cpp
#include <iostream>

int main() {
    std::cout << "TO: Ola Nowak\n";
    std::cout << "FROM: Modern C++ Foundations\n";
    std::cout << "FRAGILE - HANDLE WITH CARE\n";
}
```

Trzy linijki wyniku to trzy instrukcje, w tej samej kolejności. Każdy napis kończy się `\n`, więc każda linijka etykiety zaczyna się od nowej linii.

</details>

**Poprzednia lekcja:** [Lekcja 0.6: Ten sam program bez CLiona](../module_00_tooling/lesson_06_same_program_without_clion.md) · **Następna lekcja:** w przygotowaniu · [Opis kursu](../../README.md)

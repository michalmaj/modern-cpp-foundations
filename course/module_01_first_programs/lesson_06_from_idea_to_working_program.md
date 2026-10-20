# Lekcja 1.6: Samodzielnie od pomysłu do działającego programu

**Polski** · [English](lesson_06_from_idea_to_working_program.en.md) · [Opis kursu](../../README.md)

> **Moduł 1, lekcja 6: sprawdzian** · około 90 minut
> **Potrzebujesz:** katalogu `cpp-workspace` z repozytorium Gita z [lekcji 1.5](lesson_05_save_the_history_of_your_work.md) i oryginalnego projektu `lesson_05_first_program`.
> **Wersja pilotażowa.** Rozwiązania referencyjne i polecenia z tej lekcji sprawdzamy automatycznie na Windowsie, Ubuntu i macOS. Twojej pracy nic nie ocenia automatycznie: sprawdzasz ją sam, według kryteriów.

## Jak przebiega ten sprawdzian

Ta lekcja nie wprowadza niczego nowego. Sprawdzasz, czy potrafisz samodzielnie przejść całą drogę: od wymagań, przez kod, budowanie i sprawdzenie wyniku, po zapisanie pracy w Gicie. Do tego diagnozujesz dwa problemy i wyjaśniasz, co zrobiono.

Lekcja ma dwie części:

- **Część A: sprawdzian.** Same zadania, wymagania, oczekiwane wyniki i kryteria. Bez podpowiedzi i bez kodu rozwiązań. Wszystko, czego potrzebujesz, znasz z lekcji 1.1–1.5.
- **Część B: sprawdzenie i omówienie.** Podpowiedzi, przykładowe rozwiązania, wyjaśnienia i samoocena. Przejdź do niej po wykonaniu części A albo wtedy, gdy świadomie zrezygnujesz z dalszej samodzielnej próby.

Zajrzenie do części B, do wcześniejszych lekcji albo do swoich notatek nie jest porażką. To normalna część nauki. Ważne jest tylko jedno: **zanotuj uczciwie, co zrobiono samodzielnie, a co z pomocą**. Na końcu jest samoocena, która to rozróżnia. Dzięki niej będzie wiadomo, co warto powtórzyć przed Modułem 2.

**Możesz używać:**

- terminala, CMake i Ninja (polecenia z lekcji 0.6 i 1.4);
- CLiona jako edytora i IDE;
- Gita w terminalu (lekcja 1.5);
- `CMakeLists.txt` skopiowanego z oryginalnego `lesson_05_first_program`. Nie musisz pisać CMake z pamięci.

---

# Część A: sprawdzian

## Zadanie 1: Tablica wieczoru gier

Biblioteka miejska organizuje wieczór gier planszowych i chce wyświetlać informację w terminalu przy wejściu.

**Przygotowanie:**

- W `cpp-workspace` utwórz nowy katalog `board_games_night`.
- Skopiuj do niego `CMakeLists.txt` z oryginalnego `lesson_05_first_program`.
- Utwórz w nim **pusty** `main.cpp` i napisz cały program sam.
- Nie zmieniaj wcześniejszych projektów w `cpp-workspace`.

**Wymagania:**

- Program wypisuje **dokładnie** poniższy tekst, linijka po linijce, razem z pustą linijką:

<!-- output: board_games_night -->
```text
BOARD GAMES NIGHT
=================
Where: City Library, room "Blue"
When: Friday, 18:00
Bring: your favourite game

Sign-up sheet: \\library\games\list.txt
Have fun!
```

- Program ma co najmniej jeden komentarz, który wyjaśnia coś nieoczywistego, a nie powtarza kod.
- Program kończy się poprawnie: kod zakończenia 0.
- Zbuduj program i uruchom go. Porównaj wynik z oczekiwanym znak po znaku.
- Gdy wynik się zgadza, **zapisz tę wersję w historii Gita**: tylko pliki źródłowe tego projektu. Zanim zapiszesz, sprawdź, co trafi do commita.

## Zadanie 2: Zmiana planów

Biblioteka zmieniła salę i godzinę, a do tego chce zachęcić do pożyczania gier. Zmień swój program tak, żeby wypisywał dokładnie:

<!-- output: board_games_night_changed -->
```text
BOARD GAMES NIGHT
=================
Where: City Library, room "Green"
When: Friday, 19:30
Sign-up sheet: \\library\games\list.txt

Bring: your favourite game, or "Dixit" from the shelf
Have fun!
```

- Przed zapisaniem zobacz, czym ta wersja różni się od zapisanej, i umiej to opisać.
- Zbuduj i uruchom zmieniony program i sprawdź wynik.
- Zapisz **drugi commit**.
- Potwierdź, że historia zawiera obie wersje, a projekt nie ma niezapisanych zmian.

Jeśli chcesz sprawdzić swoją samodzielność, wykonaj to zadanie bez zaglądania do rozwiązania zadania 1.

## Zadanie 3: Dwa zgłoszenia

W `cpp-workspace` utwórz katalog `diagnosis` i skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program`. Zbuduj go poleceniami z terminala, w katalogu `build-terminal`.

**Zgłoszenie 1.** Ktoś chciał wypisać `Saving to C:\games\list.txt` i napisał taki `main.cpp`:

<!-- broken: diagnosis_backslash at=4:18 error=^expected expression$ -->
```cpp
#include <iostream>

int main() {
    std::cout << "Saving to C:\";
    std::cout << "games\\list.txt\n";
}
```

**Zgłoszenie 2.** Ktoś inny zmienił nazwę programu na `board_games` i jego `CMakeLists.txt` wygląda tak (`main.cpp` jest już poprawny):

```cmake
cmake_minimum_required(VERSION 3.28)
project(first_program LANGUAGES CXX)

add_executable(board_games main.cpp)
target_compile_features(first_program PRIVATE cxx_std_20)
set_target_properties(first_program PROPERTIES CXX_EXTENSIONS OFF)
```

**Dla każdego zgłoszenia:**

1. Uruchom właściwy krok: konfigurację albo budowanie.
2. Ustal etap problemu: konfiguracja, kompilacja czy linkowanie.
3. Znajdź pierwszą istotną informację i ją zapisz.
4. Postaw hipotezę, co jest przyczyną.
5. Popraw problem jedną zmianą.
6. Sprawdź, że po zmianie wszystko działa. Program ze zgłoszenia 1 wypisuje `Saving to C:\games\list.txt`, a po zgłoszeniu 2 program nazywa się `board_games` i daje się uruchomić.

Zapisz wyniki w tabeli:

| Zgłoszenie | Etap | Pierwsza istotna informacja | Hipoteza | Poprawka | Sprawdzenie |
|---|---|---|---|---|---|
| 1 | | | | | |
| 2 | | | | | |

Projektu `diagnosis` nie musisz zapisywać w Gicie.

## Zadanie 4: Wyjaśnij

Odpowiedz krótko, na piśmie, odwołując się do tego, co zrobiono w zadaniach 1–3:

1. Jaką rolę pełni `main.cpp` w Twoim projekcie `board_games_night`?
2. Do czego służy `CMakeLists.txt`? Co by się stało, gdyby jego linijki nie pasowały do siebie (zgłoszenie 2)?
3. Co robi kompilator z Twoim `main.cpp`?
4. Czym różni się kompilacja od linkowania? Który z tych etapów zgłosiłby problem, gdyby w Twoim programie zamiast `main` było `mian`?
5. Dlaczego samo zapisanie zmienionego `main.cpp` w zadaniu 2 nie zmieniło wcześniej zbudowanego programu?
6. Dlaczego program może działać niepoprawnie, choć zbudował się bez błędów? Podaj przykład z tego sprawdzianu.
7. Nad którą linijką programu trzeba było zastanawiać się najdłużej i dlaczego?

## Kryteria sukcesu

Sprawdzian jest zaliczony, gdy spełniasz **wszystkie** kryteria:

- `board_games_night/main.cpp` napisano od pustego pliku, w poprawnym C++20.
- Program buduje się bez błędów i uruchamia, a jego wynik jest **dokładnie** taki jak w zadaniu 1, a po zmianie dokładnie taki jak w zadaniu 2.
- Program kończy się kodem 0.
- Program ma sensowny komentarz.
- Oba zgłoszenia z zadania 3 zdiagnozowano: właściwy etap, cytat z wyniku narzędzi, hipoteza, jedna poprawka i sprawdzenie.
- Historia Gita ma **dwa commity** projektu `board_games_night` z opisami, które mówią, co każda wersja wnosi. `git status` nie pokazuje niezapisanych zmian w tym projekcie.
- W historii nie ma plików wygenerowanych przez narzędzia ani ustawień CLiona: dla tego projektu zapisane są tylko `main.cpp` i `CMakeLists.txt`.
- Umiesz wyjaśnić każdą linijkę swojego programu i każde polecenie, którego użyto (zadanie 4).

Działający program, poprawny wynik i czyste `git status` to konieczne warunki, ale **nie dowód zrozumienia**. Dowodem jest to, że potrafisz wyjaśnić, dlaczego program działa i jak znaleziono przyczyny problemów. Dlatego zadanie 4 jest częścią sprawdzianu.

---

# Część B: sprawdzenie i omówienie

Przejdź tutaj po wykonaniu części A albo wtedy, gdy świadomie zrezygnujesz z dalszej samodzielnej próby.

## Jak sprawdzić swoją pracę

- **Wynik programu:** uruchom program i porównaj go z oczekiwanym znak po znaku, razem z pustą linijką, cudzysłowami i liczbą ukośników.
- **Kod zakończenia:** w CLionie jest pod wynikiem: `Process finished with exit code 0`.
- **Historia:**
  - `git log --oneline` pokazuje dwa nowe commity;
  - `git status` nie pokazuje plików `board_games_night`;
  - `git ls-files board_games_night` pokazuje tylko `CMakeLists.txt` i `main.cpp`.

## Podpowiedzi

Każda podpowiedź dotyczy sposobu myślenia. Rozwijaj je po kolei i tylko wtedy, gdy ich potrzebujesz.

<details>
<summary>Zadanie 1: od czego zacząć?</summary>

Od szkieletu programu (lekcja 1.3), potem jedna linijka wyniku na raz. Po każdej dopisanej instrukcji zbuduj i porównaj wynik.

</details>

<details>
<summary>Zadanie 1: pusta linijka i ukośniki</summary>

Pusta linijka to linijka, w której jest tylko przejście do nowej linii. Ile znaków `\` musi być w kodzie, żeby w wyniku pojawiły się dwa obok siebie?

</details>

<details>
<summary>Zadanie 3: zgłoszenie 1</summary>

Co w napisie znaczy `\` tuż przed `"`? Gdzie w takim razie kończy się pierwszy napis?

</details>

<details>
<summary>Zadanie 3: zgłoszenie 2</summary>

Który krok zgłasza błąd: konfiguracja czy budowanie? Ile razy w `CMakeLists.txt` występuje nazwa programu i czy wszędzie jest taka sama?

</details>

## Przykładowe rozwiązania

<details>
<summary>Zadanie 1: program</summary>

<!-- example: board_games_night -->
```cpp
#include <iostream>

int main() {
    std::cout << "BOARD GAMES NIGHT\n";
    std::cout << "=================\n";
    std::cout << "Where: City Library, room \"Blue\"\n";
    std::cout << "When: Friday, 18:00\n";
    std::cout << "Bring: your favourite game\n";
    std::cout << "\n";
    // In the code, \\ prints one backslash, so \\\\ prints two.
    std::cout << "Sign-up sheet: \\\\library\\games\\list.txt\n";
    std::cout << "Have fun!\n";
    return 0;
}
```

- Cudzysłowy wokół `Blue` są częścią tekstu, więc każdy jest zapisany jako `\"`.
- Ścieżka zaczyna się od dwóch ukośników, więc w kodzie są cztery (`\\\\`). Każdy następny ukośnik to w kodzie `\\`.
- Pustą linijkę wypisuje instrukcja z samym `\n`. Równie dobrze można dopisać drugie `\n` do poprzedniej linijki.
- Komentarz wyjaśnia najtrudniejszą linijkę. `return 0;` jest opcjonalne: koniec `main` bez `return` działa tak samo.

</details>

<details>
<summary>Zadanie 2: zmieniony program</summary>

<!-- example: board_games_night_changed -->
```cpp
#include <iostream>

int main() {
    std::cout << "BOARD GAMES NIGHT\n";
    std::cout << "=================\n";
    std::cout << "Where: City Library, room \"Green\"\n";
    std::cout << "When: Friday, 19:30\n";
    // In the code, \\ prints one backslash, so \\\\ prints two.
    std::cout << "Sign-up sheet: \\\\library\\games\\list.txt\n";
    std::cout << "\n";
    std::cout << "Bring: your favourite game, or \"Dixit\" from the shelf\n";
    std::cout << "Have fun!\n";
    return 0;
}
```

`git diff` przed drugim commitem pokazuje zmienione linijki z sali i godziny. Pokazuje też, że linijka `Sign-up sheet` i pusta linijka przesunęły się nad `Bring`, a linijka `Bring` ma nowy tekst. Przykładowy przebieg w Gicie, w katalogu `cpp-workspace`:

```text
git status
git add board_games_night/main.cpp board_games_night/CMakeLists.txt
git status
git commit -m "Add the board games night board"
```

a po zmianie:

```text
git diff
git add board_games_night/main.cpp
git diff --staged
git commit -m "Move the board games night to the Green room"
git log --oneline
git status
git ls-files board_games_night
```

</details>

<details>
<summary>Zadanie 3: zgłoszenie 1</summary>

- **Etap:** kompilacja. Konfiguracja się udała, a budowanie zatrzymało się na `main.cpp`.
- **Pierwsza istotna informacja:** `warning: missing terminating '"' character` w linijce 4, a zaraz potem `error: expected expression` w tym samym miejscu. Tu najwięcej mówi ostrzeżenie.
- **Hipoteza:** `\"` na końcu napisu to cudzysłów wewnątrz tekstu, a nie jego koniec (lekcja 1.3). Napis się więc nie kończy.
- **Poprawka:** ukośnik, który ma się pojawić w wyniku, zapisać jako `\\`:

<!-- example: diagnosis_backslash_fixed -->
```cpp
#include <iostream>

int main() {
    std::cout << "Saving to C:\\";
    std::cout << "games\\list.txt\n";
}
```

<!-- output: diagnosis_backslash_fixed -->
```text
Saving to C:\games\list.txt
```

</details>

<details>
<summary>Zadanie 3: zgłoszenie 2</summary>

- **Etap:** konfiguracja. Błąd pojawia się już przy `cmake -S . -B build-terminal …`, a kompilator ani linker nie ruszyły. Jeśli `build-terminal` był skonfigurowany wcześniej, ten sam błąd pokaże `cmake --build`, bo najpierw ponownie uruchomi CMake.
- **Pierwsza istotna informacja:** `CMake Error at CMakeLists.txt:5 (target_compile_features):` i `Cannot specify compile features for target "first_program" which is not built by this project.`. Drugi błąd, w linijce 6 (`set_target_properties`), ma tę samą przyczynę: jedna przyczyna, dwa komunikaty, jak w lekcji 1.2.
- **Hipoteza:** nazwę programu zmieniono tylko w `add_executable`. Dwie następne linijki nadal mówią o `first_program`, którego projekt już nie buduje (lekcja 1.4, eksperyment C).
- **Poprawka:** w obu linijkach wpisać `board_games`. Po konfiguracji i budowaniu w `build-terminal` jest program `board_games`, na Windowsie `board_games.exe`.

</details>

## Przykładowe odpowiedzi do zadania 4

<details>
<summary>Pokaż przykładowe odpowiedzi</summary>

1. `main.cpp` to kod źródłowy programu. Wykonywanie zaczyna się od `main`, a instrukcje wypisują tablicę po kolei, od góry do dołu.
2. `CMakeLists.txt` mówi narzędziom, jaki program zbudować, z jakiego pliku i w jakim standardzie. Gdy jego linijki do siebie nie pasują, konfiguracja się nie udaje i nic nie zostaje zbudowane.
3. Sprawdza, czy kod jest poprawnym C++, i tłumaczy go na plik obiektowy.
4. Kompilacja sprawdza i tłumaczy jeden plik, a linkowanie łączy plik obiektowy z kodem biblioteki i kodem startowym w program. Literówkę `mian` zgłosiłby linker, bo kompilator uznałby `mian` za poprawną nazwę funkcji.
5. Program to osobny plik, który powstaje przy budowaniu. Zmienia się dopiero po ponownym zbudowaniu.
6. Bo kompilator sprawdza poprawność C++, a nie to, czy tekst jest taki, jak chcemy. Na przykład brak `\n` albo jeden ukośnik zamiast dwóch daje poprawny program z innym wynikiem.
7. To odpowiedź osobista. Dobra odpowiedź wskazuje konkretną linijkę i mówi, czego dotyczyła wątpliwość, na przykład liczby ukośników w ścieżce.

</details>

## Samoocena

Przy każdym kryterium zaznacz jedną odpowiedź:

| Kryterium | Samodzielnie | Z podpowiedzią | Po zajrzeniu do rozwiązania | Do powtórki |
|---|---|---|---|---|
| Napisanie programu od pustego `main.cpp` | | | | |
| Dokładny wynik, w tym `\"`, `\\` i pusta linijka | | | | |
| Budowanie i uruchomienie | | | | |
| Diagnoza zgłoszenia 1 (kompilacja) | | | | |
| Diagnoza zgłoszenia 2 (konfiguracja) | | | | |
| Dwa commity bez plików wygenerowanych | | | | |
| Wyjaśnienia z zadania 4 | | | | |

Jeśli w kolumnie „Do powtórki” jest coś zaznaczone, wróć do odpowiedniej lekcji:

| Temat | Lekcja |
|---|---|
| szkielet i instrukcje | 1.1 i 1.3 |
| komunikaty kompilatora | 1.2 |
| `\"`, `\\`, komentarze | 1.3 |
| etapy budowania i `CMakeLists.txt` | 1.4 |
| Git | 1.5 |

Potem spróbuj zadania jeszcze raz, na przykład z innym tekstem tablicy.

---

## Podsumowanie Modułu 1

Po sześciu lekcjach potrafisz:

- czytać i samodzielnie pisać małe programy w C++20, zaczynając od pustego pliku;
- wypisywać tekst w zadanej kolejności, z `\n`, `\"` i `\\`, i dodawać komentarze tam, gdzie coś wymaga wyjaśnienia;
- czytać komunikaty kompilatora, stawiać hipotezy i poprawiać jedną rzecz naraz;
- odróżniać konfigurację, kompilację, linkowanie i działanie programu, i po wyniku narzędzi rozpoznawać, gdzie jest problem;
- korzystać z prostego projektu CMake i rozumieć jego linijki;
- zapisywać historię własnej pracy w Gicie, bez plików wygenerowanych przez narzędzia.

## Co dalej: Moduł 2

Twoje programy wypisują na razie zawsze ten sam tekst. W Module 2 zaczną **pamiętać i liczyć**: poznasz wartości, typy, zmienne, wyrażenia i obliczenia oraz nauczysz się wczytywać proste dane od użytkownika. **Moduł 2 jest w przygotowaniu.**

**Poprzednia lekcja:** [Lekcja 1.5: Zapisz historię swojej pracy](lesson_05_save_the_history_of_your_work.md) · **Następny moduł:** w przygotowaniu · [Opis kursu](../../README.md)

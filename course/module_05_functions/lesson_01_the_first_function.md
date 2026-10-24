# Lekcja 5.1: Pierwsza własna funkcja (`void`)

**Polski** · [English](lesson_01_the_first_function.en.md) · [Opis kursu](../../README.md)

> **Moduł 5, lekcja 1** · około 60–75 minut
> **Potrzebujesz:** katalogu `cpp-workspace` i oryginalnego projektu `lesson_05_first_program`, jak dotąd. Debugger nie jest w tej lekcji potrzebny.
> **Wersja pilotażowa.** Programy z tej lekcji sprawdzamy automatycznie na Windowsie, Ubuntu i macOS, także z podanymi danymi wejściowymi. Wpisywanie danych w oknie **Run** CLiona opisujemy bez ręcznego sprawdzenia na każdym systemie.

## Zanim zaczniesz

Ta lekcja zakłada, że po Module 4:

- piszesz programy z `if`/`else` i z pętlami `while` oraz `for`;
- sprawdzasz zakres danych, zanim program zacznie pracę;
- wiesz, że `main` to funkcja, od której zaczyna się wykonywanie programu (lekcja 1.3);
- czytasz komunikaty kompilatora i poprawiasz błędy kompilacji (lekcja 1.2).

## Sytuacja

Twoje programy robią już sporo, ale każdy jest jednym długim `main`. Gdy ten sam fragment ma się wykonać w kilku miejscach programu, trzeba go zapisać kilka razy. W tej lekcji poznasz sposób, żeby taki fragment **nazwać**, zapisać **raz** i wykonywać tam, gdzie jest potrzebny: **własną funkcję**.

Po tej lekcji będziesz:

- wyjaśniać, po co wydziela się fragment kodu do funkcji;
- wskazywać w funkcji `void`, jej nazwę, puste nawiasy i ciało;
- odróżniać definicję funkcji od jej wywołania;
- przewidywać kolejność wykonania programu z funkcją, także gdy funkcja nie jest wywołana albo jest wywołana kilka razy;
- znajdować wywołanie, którego jest za dużo;
- pisać własną funkcję `void` i decydować, gdzie ją wywołać w programie z pętlą.

## 1. Przygotuj projekt

W `cpp-workspace` utwórz katalog `lesson_5_1` i skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program`. Programy z punktów 2–9 wpisujesz w `main.cpp` tego katalogu.

## 2. Ten sam fragment w dwóch miejscach

Na zajęciach w warsztacie prowadzący dwa razy przypomina zasady bezpieczeństwa: na porannej odprawie i na popołudniowej. Ten program znasz w całości:

<!-- example: briefing_repeated -->
```cpp
#include <iostream>

int main() {
    std::cout << "Morning briefing\n";
    std::cout << "Wear safety glasses\n";
    std::cout << "Keep tools organised\n";

    std::cout << "Afternoon briefing\n";
    std::cout << "Wear safety glasses\n";
    std::cout << "Keep tools organised\n";
}
```

<!-- output: briefing_repeated -->
```text
Morning briefing
Wear safety glasses
Keep tools organised
Afternoon briefing
Wear safety glasses
Keep tools organised
```

Program działa poprawnie. Zastanów się jednak i zapisz krótkie odpowiedzi:

1. Co trzeba zmienić w kodzie, jeśli jedna zasada zostanie zaktualizowana?
2. Ile miejsc trzeba wtedy sprawdzić?
3. Co się stanie, jeśli zmienisz tylko jedną kopię?
4. Czy te dwie instrukcje mają wspólne zadanie, które dałoby się nazwać?

<details>
<summary>Omówienie</summary>

Zasady są zapisane dwa razy, więc każdą zmianę trzeba wprowadzić w dwóch miejscach. Jeśli zmienisz tylko jedną kopię, program się zbuduje i uruchomi, ale rano i po południu poda **różne** zasady. Nikt nie zauważy tego od razu, bo kompilator nie ma tu czego zgłosić: powtórzony kod to poprawny C++. To kłopot z czytelnością i z późniejszymi zmianami, a nie błąd języka.

Obie instrukcje mają jedno wspólne zadanie: **pokazać zasady warsztatu**. Takie zadanie można nazwać i zapisać w jednym miejscu.

</details>

## 3. Pierwsza własna funkcja

Oto zasady warsztatu zapisane jako funkcja:

<!-- fragment -->
```cpp
void show_workshop_rules() {
    std::cout << "Wear safety glasses\n";
    std::cout << "Keep tools organised\n";
}
```

To jest **definicja funkcji**: opis, co funkcja robi. Jej części:

| Część | W kodzie | Znaczenie |
|---|---|---|
| **Typ wyniku** | `void` | Funkcja nie przekazuje żadnego wyniku do miejsca, w którym ją wywołano. Nie znaczy to, że nic nie robi: ta funkcja wypisuje dwie linijki. |
| **Nazwa** | `show_workshop_rules` | Opisuje zadanie funkcji. Zapisujemy ją jak nazwy zmiennych: małymi literami, ze słowami połączonymi `_`. |
| **Nawiasy** | `()` | Puste: ta funkcja nie potrzebuje żadnych danych z zewnątrz. Co może się w nich znaleźć, zobaczysz w kolejnej lekcji. |
| **Ciało** | instrukcje między `{` a `}` | To, co funkcja wykonuje, gdy zostanie wywołana. |

Definicję piszesz **poza** `main`, przed nim, tak jak w następnym punkcie.

## 4. Wywołanie funkcji z `main`

Ten program wykonuje to samo co program z punktu 2:

<!-- example: briefing_function -->
```cpp
#include <iostream>

void show_workshop_rules() {
    std::cout << "Wear safety glasses\n";
    std::cout << "Keep tools organised\n";
}

int main() {
    std::cout << "Morning briefing\n";
    show_workshop_rules();

    std::cout << "Afternoon briefing\n";
    show_workshop_rules();
}
```

<!-- output: briefing_function -->
```text
Morning briefing
Wear safety glasses
Keep tools organised
Afternoon briefing
Wear safety glasses
Keep tools organised
```

Standardowe wyjście jest identyczne jak w punkcie 2. Zmienił się sposób zapisu: zasady stoją w kodzie **raz**.

- **`show_workshop_rules();`** to **wywołanie funkcji**: nazwa, puste nawiasy i średnik. Wywołanie mówi: „wykonaj teraz instrukcje tej funkcji”.
- **`main` też jest funkcją** (lekcja 1.3), ale ma szczególną rolę: od niej zaczyna się wykonywanie programu. Program nie zaczyna się od `show_workshop_rules`, choć ta funkcja stoi w pliku wyżej. Słowo `int` przed `main` znasz od początku kursu. To też szczególny element `main`, do którego wrócimy, gdy poznasz funkcje przekazujące wynik.
- Własną funkcję wywołuje się tak samo jak znane Ci już `std::getline(…)`: nazwą i nawiasami. W nawiasach `std::getline` stały dane do odczytu. Nawiasy `show_workshop_rules()` są puste.

## 5. Kolejność wykonania

Program z punktu 4 wykonuje się w takiej kolejności:

| Krok | Gdzie jest program | Co się dzieje | Na ekranie |
|---|---|---|---|
| 1 | `main` | początek programu | |
| 2 | `main` | wypisanie | `Morning briefing` |
| 3 | `main` | pierwsze wywołanie `show_workshop_rules()`: przejście do funkcji | |
| 4 | funkcja | pierwsza instrukcja ciała | `Wear safety glasses` |
| 5 | funkcja | druga instrukcja ciała | `Keep tools organised` |
| 6 | `main` | koniec ciała funkcji: powrót za miejsce wywołania | |
| 7 | `main` | wypisanie | `Afternoon briefing` |
| 8 | `main` | drugie wywołanie tej samej funkcji | |
| 9 | funkcja | obie instrukcje ciała | `Wear safety glasses`, `Keep tools organised` |
| 10 | `main` | powrót za drugie wywołanie, koniec `main`: program się kończy | |

Program nie wkleja treści funkcji do `main`. Przy wywołaniu **przechodzi** do funkcji, wykonuje jej instrukcje od góry do dołu i **wraca** do miejsca za wywołaniem.

**Przewidź.** Ile razy wykonają się instrukcje wewnątrz funkcji, jeśli wywołasz ją dwa razy? A ile linijek wypisze ten program, z trzema wywołaniami?

<!-- example: briefing_three_calls -->
```cpp
#include <iostream>

void show_workshop_rules() {
    std::cout << "Wear safety glasses\n";
    std::cout << "Keep tools organised\n";
}

int main() {
    std::cout << "Morning briefing\n";
    show_workshop_rules();

    std::cout << "Afternoon briefing\n";
    show_workshop_rules();

    std::cout << "Evening briefing\n";
    show_workshop_rules();
}
```

<details>
<summary>Odpowiedź i standardowe wyjście dla trzech wywołań</summary>

Ciało funkcji wykonuje się raz przy każdym wywołaniu. Przy dwóch wywołaniach obie instrukcje ciała wykonują się dwa razy, przy trzech trzy razy. Ten program wypisuje 9 linijek: 3 nazwy odpraw i 3 × 2 linijki zasad.

<!-- output: briefing_three_calls -->
```text
Morning briefing
Wear safety glasses
Keep tools organised
Afternoon briefing
Wear safety glasses
Keep tools organised
Evening briefing
Wear safety glasses
Keep tools organised
```

</details>

## 6. Definicja to nie wywołanie

W tym programie funkcja jest zdefiniowana, ale `main` jej nie wywołuje:

<!-- example: rules_not_called -->
```cpp
#include <iostream>

void show_workshop_rules() {
    std::cout << "Wear safety glasses\n";
    std::cout << "Keep tools organised\n";
}

int main() {
    std::cout << "Morning briefing\n";
    std::cout << "Afternoon briefing\n";
}
```

**Przewidź**, co wypisze program. Zapisz odpowiedź, a potem go uruchom.

<details>
<summary>Standardowe wyjście i wyjaśnienie</summary>

<!-- output: rules_not_called -->
```text
Morning briefing
Afternoon briefing
```

Zasady się nie pojawiły. **Samo zapisanie definicji funkcji nie wykonuje jej instrukcji.** Program zaczyna się od `main` i wykonuje tylko to, co `main` mu każe. Funkcja stoi w pliku wyżej, ale bez wywołania jej ciało się nie wykonuje.

</details>

Teraz dopisz **jedno** wywołanie, zaraz po `Morning briefing`. Przewidź wynik i uruchom program:

<!-- example: rules_called_once -->
```cpp
#include <iostream>

void show_workshop_rules() {
    std::cout << "Wear safety glasses\n";
    std::cout << "Keep tools organised\n";
}

int main() {
    std::cout << "Morning briefing\n";
    show_workshop_rules();
    std::cout << "Afternoon briefing\n";
}
```

<details>
<summary>Standardowe wyjście dla jednego wywołania</summary>

<!-- output: rules_called_once -->
```text
Morning briefing
Wear safety glasses
Keep tools organised
Afternoon briefing
```

</details>

Dopisz drugie wywołanie, zaraz po `Afternoon briefing`. Otrzymasz program z punktu 4 i jego wynik: zasady pojawią się dwa razy. **Zero wywołań, zero wykonań. Jedno wywołanie, jedno wykonanie. Dwa wywołania, dwa wykonania.**

## 7. Jedna zmiana, wszystkie wywołania

Wróć do programu z punktu 4. Prowadzący zmienia drugą zasadę na `Keep the floor clear`. Zmień **tylko jedną** linijkę, w ciele funkcji:

<!-- example: briefing_changed -->
```cpp
#include <iostream>

void show_workshop_rules() {
    std::cout << "Wear safety glasses\n";
    std::cout << "Keep the floor clear\n";
}

int main() {
    std::cout << "Morning briefing\n";
    show_workshop_rules();

    std::cout << "Afternoon briefing\n";
    show_workshop_rules();
}
```

**Przewidź**, w ilu miejscach standardowego wyjścia pojawi się nowy tekst. Potem uruchom program.

<details>
<summary>Standardowe wyjście po zmianie</summary>

<!-- output: briefing_changed -->
```text
Morning briefing
Wear safety glasses
Keep the floor clear
Afternoon briefing
Wear safety glasses
Keep the floor clear
```

Nowy tekst pojawia się w obu miejscach, choć zmieniono jedną linijkę. Oba wywołania wykonują to samo ciało funkcji.

</details>

Funkcja daje **jedno miejsce**, w którym zapisane są instrukcje wykonywane wielokrotnie. Nie znaczy to, że każda linijka albo każde powtórzenie musi trafić do osobnej funkcji. Funkcja ma sens wtedy, gdy jej instrukcje mają **wspólne, czytelne zadanie**, które da się nazwać, jak „pokaż zasady warsztatu”.

## 8. Znajdź błąd: o jedno wywołanie za dużo

Wymaganie: program wypisuje plan dnia warsztatu: `Session 1`, `Lunch`, `Session 2` i na końcu `See you tomorrow`. Zasady pojawiają się **dokładnie dwa razy: zaraz po nazwie każdej sesji**.

<!-- example: day_plan_bug -->
```cpp
#include <iostream>

void show_workshop_rules() {
    std::cout << "Wear safety glasses\n";
    std::cout << "Keep tools organised\n";
}

int main() {
    std::cout << "Session 1\n";
    show_workshop_rules();
    std::cout << "Lunch\n";
    show_workshop_rules();
    std::cout << "Session 2\n";
    show_workshop_rules();
    std::cout << "See you tomorrow\n";
}
```

1. Przeczytaj wymaganie i zapisz, jakie standardowe wyjście **powinno** się pojawić.
2. **Przewidź**, co wypisze **ten** program.
3. Uruchom go.
4. Porównaj, ile razy pojawiają się zasady, i gdzie.
5. Znajdź wywołanie, którego jest za dużo.
6. Popraw program.
7. Uruchom go ponownie i sprawdź, czy wynik zgadza się z wymaganiem.

Wynik programu przed poprawką i poprawiony program są w części [Przykładowe rozwiązania](#przykładowe-rozwiązania). Zajrzyj tam po własnej próbie.

## 9. Funkcja zapisana pod `main`

W tym programie definicja funkcji stoi **po** `main`:

<!-- broken: rules_after_main at=5:5 errors=1 error=^use of undeclared identifier 'show_workshop_rules'$ -->
```cpp
#include <iostream>

int main() {
    std::cout << "Morning briefing\n";
    show_workshop_rules();
}

void show_workshop_rules() {
    std::cout << "Wear safety glasses\n";
    std::cout << "Keep tools organised\n";
}
```

**Przewidź**, czy ten program się zbuduje. Potem spróbuj go zbudować i przeczytaj komunikat kompilatora.

<details>
<summary>Co zgłasza kompilator i dlaczego</summary>

Program się nie zbuduje. Kompilator zgłasza w linijce 5 `use of undeclared identifier 'show_workshop_rules'`: nie zna tej nazwy. Ten sam komunikat znasz z lekcji 3.2 i 4.3, gdzie dotyczył zmiennej.

Kompilator czyta plik od góry. Gdy dochodzi do wywołania w linijce 5, nie widział jeszcze żadnej funkcji o tej nazwie. Definicja stoi niżej, ale w tym miejscu kompilator jeszcze o niej nie wie.

</details>

**Poprawka:** przenieś całą definicję funkcji **przed** `main`. W tym kursie na razie stosujemy taki wzór: **funkcja musi być zapisana w pliku, zanim ją wywołasz**. Są też inne sposoby uporządkowania funkcji w pliku. Poznasz je później. Poprawiony program jest w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 10. Misja: przerwy między rundami

Program układa plan treningu z przerwami. Użytkownik podaje liczbę rund. Program wypisuje kolejne rundy, a **między** nimi przerwę.

**Wymagania:**

- Program pyta `Enter round count (0-5):` i odczytuje liczbę całkowitą. Zakładamy, że użytkownik wpisuje liczbę całkowitą.
- Dla liczby spoza zakresu od 0 do 5 program wypisuje tylko `Invalid round count` i nie zaczyna planu. Nie pyta ponownie.
- Dla poprawnej liczby wypisuje kolejne rundy, od 1 do podanej liczby włącznie, każdą jako `Round N`.
- Między dwiema kolejnymi rundami wypisuje przerwę, dokładnie te dwie linijki:

  ```text
  Break: drink water
  Break: stretch
  ```

- Przed pierwszą rundą i po ostatniej rundzie przerwy nie ma.
- Na końcu planu wypisuje `Training complete`.
- Przerwę wypisuje **Twoja własna funkcja `void` bez parametrów**, zdefiniowana przed `main`. Linijki przerwy stoją w kodzie tylko w niej. Numer rundy wypisuje kod w `main`.
- Nie używaj zmiennych zadeklarowanych poza funkcjami.

W `cpp-workspace` utwórz katalog `round_breaks`, skopiuj do niego `CMakeLists.txt` z oryginalnego `lesson_05_first_program`, utwórz pusty `main.cpp` i napisz program samodzielnie.

Dla 3 rund standardowe wyjście ma być takie:

<!-- input: round_breaks -->
```text
3
```

<!-- output: round_breaks -->
```text
Enter round count (0-5):
Round 1
Break: drink water
Break: stretch
Round 2
Break: drink water
Break: stretch
Round 3
Training complete
```

**To nie jest program z warsztatu z innymi napisami.** Tam funkcję wywoływano w dwóch stałych miejscach `main`. Tutaj liczba rund zależy od danych, a przerwa ma się pojawić tylko w niektórych miejscach powtarzania. Sama funkcja nie wie, która runda trwa. O tym, **kiedy** ją wywołać, decyduje `main`. Musisz samodzielnie zdecydować:

1. jak kontrolować liczbę rund;
2. gdzie wypisywać bieżącą rundę;
3. od czego zależy, czy po rundzie będzie przerwa;
4. gdzie umieścić wywołanie funkcji;
5. jak uniknąć przerwy po ostatniej rundzie;
6. co program robi dla zera rund.

**Zanim napiszesz program**, przygotuj tabelę przypadków testowych: zero rund, jedna runda, dwie rundy, trzy rundy, największa dopuszczalna liczba rund i wartości tuż poza zakresem z obu stron. Przy każdym przypadku zapisz oczekiwane standardowe wyjście, także dla 0 i 1, i liczbę przerw.

**Potem pracuj w tej kolejności:**

1. Zaprojektuj, w którym miejscu programu i pod jakim warunkiem stoi wywołanie funkcji.
2. Napisz program.
3. Uruchom go dla 2 i 3 rund i porównaj wyniki z tabelą.
4. Zmień na chwilę jedną linijkę przerwy w funkcji. **Przewidź**, w ilu miejscach wyniku dla 3 rund pojawi się zmiana, i sprawdź to.
5. Przywróć wymagany tekst przerwy.
6. Sprawdź pozostałe przypadki z tabeli: 0, 1, 5, -1 i 6.

### Kryterium sukcesu

- Program buduje się jako C++20, a jego standardowe wyjście dla 3 rund jest dokładnie takie jak powyżej.
- Dla każdej liczby od 0 do 5 program wypisuje odpowiednie rundy, przerwy tylko między rundami i `Training complete`. Dla każdej innej liczby wypisuje tylko pytanie i `Invalid round count`.
- Przerwę wypisuje Twoja funkcja `void` bez parametrów, zdefiniowana przed `main`. Linijki przerwy występują w kodzie tylko raz, w tej funkcji.
- Funkcja nie wypisuje numeru rundy. Program nie używa zmiennych zadeklarowanych poza funkcjami.
- Tabela przypadków powstała przed uruchomieniem programu.
- Ten sam program obsługuje wszystkie przypadki, bez zmiany kodu.
- Umiesz wskazać w swoim programie definicję funkcji i jej wywołanie oraz wyjaśnić, dlaczego po ostatniej rundzie przerwy nie ma.

Gdy wynik się zgadza, możesz zapisać projekt w Gicie, jak w lekcji 1.5.

<details>
<summary>Podpowiedź 1</summary>

Które instrukcje mają zawsze wykonywać się razem, niezależnie od numeru rundy?

</details>

<details>
<summary>Podpowiedź 2</summary>

W jaki sposób program rozpoznaje, czy po bieżącej rundzie będzie jeszcze następna?

</details>

<details>
<summary>Podpowiedź 3</summary>

Zastanów się, czy wywołanie funkcji powinno następować przed wypisaniem rundy, po każdej rundzie czy tylko po niektórych rundach.

</details>

<details>
<summary>Pełna lista przypadków kontrolnych: otwórz po przygotowaniu własnej tabeli</summary>

| Liczba rund | Standardowe wyjście po pytaniu | Przerwy | Co sprawdza |
|---|---|---|---|
| 3 | `Round 1`, przerwa, `Round 2`, przerwa, `Round 3`, `Training complete` | 2 | kilka rund |
| 0 | `Training complete` | 0 | zero rund |
| 1 | `Round 1`, `Training complete` | 0 | jedna runda: brak przerwy po ostatniej |
| 2 | `Round 1`, przerwa, `Round 2`, `Training complete` | 1 | najmniejsza liczba rund z przerwą |
| 5 | `Round 1` … `Round 5`, przerwa między każdą parą, `Training complete` | 4 | największa dopuszczalna liczba |
| -1 | `Invalid round count` | 0 | tuż pod zakresem |
| 6 | `Invalid round count` | 0 | tuż nad zakresem |

Przypadek 3 jest sprawdzony wyżej, przy treści misji.

<!-- input: round_breaks -->
```text
0
```

<!-- output: round_breaks -->
```text
Enter round count (0-5):
Training complete
```

<!-- input: round_breaks -->
```text
1
```

<!-- output: round_breaks -->
```text
Enter round count (0-5):
Round 1
Training complete
```

<!-- input: round_breaks -->
```text
2
```

<!-- output: round_breaks -->
```text
Enter round count (0-5):
Round 1
Break: drink water
Break: stretch
Round 2
Training complete
```

<!-- input: round_breaks -->
```text
5
```

<!-- output: round_breaks -->
```text
Enter round count (0-5):
Round 1
Break: drink water
Break: stretch
Round 2
Break: drink water
Break: stretch
Round 3
Break: drink water
Break: stretch
Round 4
Break: drink water
Break: stretch
Round 5
Training complete
```

<!-- input: round_breaks -->
```text
-1
```

<!-- output: round_breaks -->
```text
Enter round count (0-5):
Invalid round count
```

<!-- input: round_breaks -->
```text
6
```

<!-- output: round_breaks -->
```text
Enter round count (0-5):
Invalid round count
```

</details>

Przykładowe rozwiązanie jest w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 11. Gdy coś pójdzie inaczej

| Co widzisz | Co to znaczy | Co zrobić |
|---|---|---|
| `use of undeclared identifier` z nazwą Twojej funkcji | Wywołanie stoi w pliku przed definicją funkcji albo nazwa w wywołaniu różni się od nazwy w definicji. | Przenieś definicję przed `main`. Porównaj nazwy znak po znaku. |
| Błąd kompilacji przy definicji funkcji | Definicja stoi wewnątrz `main`, między jego klamrami. | Definicję zapisuj poza `main`, przed nim. W `main` stoi tylko wywołanie. |
| Instrukcje funkcji nie pojawiają się w wyniku | Funkcja nie jest wywołana albo w wywołaniu brakuje nawiasów: na przykład `show_break;` niczego nie wywołuje, a kompilator najwyżej wyświetli ostrzeżenie. | Wywołanie to nazwa, `()` i średnik. |
| Przerwa pojawia się po ostatniej rundzie | Wywołanie wykonuje się w każdym przebiegu pętli, bez warunku. | Zastanów się, po których rundach przerwa jest potrzebna (podpowiedź 2). |
| Przerwa pojawia się przed pierwszą rundą | Wywołanie stoi przed wypisaniem rundy i wykonuje się także w pierwszym przebiegu. | Sprawdź w tabeli przypadek z jedną rundą. |
| Te same linijki pojawiają się o jeden raz za dużo | Jest dodatkowe wywołanie funkcji (punkt 8). | Policz wywołania i porównaj z wymaganiem. |
| Program nic nie robi i czeka | Czeka na liczbę, jak w lekcji 2.6. | Wpisz liczbę i naciśnij **Enter**. |

## 12. Wyjaśnij

Odpowiedz własnymi słowami, najlepiej na piśmie. Dopiero potem porównaj z przykładowymi odpowiedziami.

1. Po co tworzymy własną funkcję?
2. Co oznacza `void`?
3. Czy funkcja `void` może wypisywać tekst?
4. Dlaczego w funkcjach z tej lekcji nawiasy są puste?
5. Czym różni się definicja funkcji od jej wywołania?
6. Czy funkcja wykona się sama, jeśli jest zdefiniowana przed `main`?
7. Co dzieje się po wykonaniu ostatniej instrukcji ciała funkcji?
8. Ile razy wykonają się instrukcje funkcji wywołanej trzy razy?
9. Dlaczego zmiana treści funkcji wpływa na wszystkie jej wywołania?
10. Dlaczego w misji funkcji nie wywołujemy po ostatniej rundzie?
11. Co stanie się w misji dla zera rund?
12. Czy każda instrukcja programu musi trafić do własnej funkcji?

<details>
<summary>Przykładowe odpowiedzi</summary>

1. Żeby nazwać fragment kodu, który ma wspólne zadanie, zapisać go raz i wykonywać tam, gdzie jest potrzebny. Zmiana tego fragmentu wymaga wtedy zmiany w jednym miejscu.
2. Że funkcja nie przekazuje żadnego wyniku do miejsca wywołania.
3. Tak. `void` mówi tylko, że funkcja nie przekazuje wyniku. Jej ciało może wykonywać dowolne znane Ci instrukcje, na przykład `std::cout`.
4. Bo te funkcje nie potrzebują żadnych danych z zewnątrz: robią zawsze to samo.
5. Definicja opisuje, co funkcja robi: typ wyniku, nazwa, nawiasy i ciało. Wywołanie, czyli nazwa z nawiasami i średnikiem, każe te instrukcje wykonać w danym miejscu programu.
6. Nie. Program zaczyna się od `main`, a ciało funkcji wykonuje się tylko wtedy, gdy program dojdzie do jej wywołania.
7. Program wraca do miejsca za wywołaniem i wykonuje dalsze instrukcje funkcji, która ją wywołała, tutaj `main`.
8. Trzy razy: raz przy każdym wywołaniu.
9. Bo każde wywołanie wykonuje to samo ciało, zapisane w jednym miejscu. Nie ma osobnych kopii, które trzeba by zmieniać.
10. Bo przerwa ma być **między** rundami. Po ostatniej rundzie nie ma już następnej, więc przerwa nie jest potrzebna. O tym, czy ją wywołać, decyduje warunek w `main`, bo sama funkcja nie wie, która runda trwa.
11. Pętla rund nie wykona się ani razu, więc nie pojawi się żadna runda ani przerwa. Program wypisze tylko pytanie i `Training complete`.
12. Nie. Funkcja ma sens, gdy jej instrukcje mają wspólne, czytelne zadanie. Wydzielanie każdej linijki do osobnej funkcji nie poprawia programu.

</details>

## Podsumowanie

- **Własna funkcja** to nazwany fragment kodu z jednym zadaniem. Zapisujesz go raz, a wykonujesz wszędzie tam, gdzie go wywołasz.
- Definicja funkcji `void` ma typ wyniku `void`, nazwę, nawiasy i ciało w klamrach: `void show_workshop_rules() { … }`.
- `void` znaczy, że funkcja nie przekazuje wyniku do miejsca wywołania. Funkcja może przy tym wypisywać tekst.
- Puste nawiasy znaczą, że funkcja nie potrzebuje danych z zewnątrz.
- **Definicja nie jest wywołaniem.** Ciało funkcji wykonuje się dopiero wtedy, gdy program dojdzie do wywołania `show_workshop_rules();`. Każde wywołanie wykonuje je raz.
- Po wykonaniu ciała program wraca za miejsce wywołania.
- `main` też jest funkcją: od niej zaczyna się wykonywanie programu.
- Na razie definicja funkcji stoi w pliku przed miejscem jej wywołania. Inaczej kompilator zgłosi `use of undeclared identifier`.
- Zmiana w ciele funkcji zmienia wynik wszystkich jej wywołań.
- O tym, kiedy wywołać funkcję, decyduje miejsce, które ją wywołuje, na przykład warunek w pętli w `main`.

## Co dalej

Funkcje z tej lekcji robią za każdym razem dokładnie to samo. W kolejnej lekcji zobaczysz, jak przekazać funkcji dane, żeby jedna funkcja mogła działać na różnych wartościach. Lekcja 5.2 jest w przygotowaniu.

---

## Przykładowe rozwiązania

Zajrzyj tutaj **po własnej próbie**. Twoje nazwy mogą się różnić, jeśli standardowe wyjście jest takie, jak wymagane.

<details>
<summary>Punkt 8: wynik przed poprawką i poprawiony program</summary>

Przed poprawką:

<!-- output: day_plan_bug -->
```text
Session 1
Wear safety glasses
Keep tools organised
Lunch
Wear safety glasses
Keep tools organised
Session 2
Wear safety glasses
Keep tools organised
See you tomorrow
```

- **Zasady pojawiają się trzy razy**, a wymaganie mówi: dwa razy, zaraz po nazwie każdej sesji.
- **Przyczyna:** wywołanie po `Lunch` jest nadmiarowe. Sama funkcja jest poprawna. Błąd leży w **miejscu wywołania**.
- **Poprawka:** usuń wywołanie, które stoi po `Lunch`.

<!-- example: day_plan_fixed -->
```cpp
#include <iostream>

void show_workshop_rules() {
    std::cout << "Wear safety glasses\n";
    std::cout << "Keep tools organised\n";
}

int main() {
    std::cout << "Session 1\n";
    show_workshop_rules();
    std::cout << "Lunch\n";
    std::cout << "Session 2\n";
    show_workshop_rules();
    std::cout << "See you tomorrow\n";
}
```

<!-- output: day_plan_fixed -->
```text
Session 1
Wear safety glasses
Keep tools organised
Lunch
Session 2
Wear safety glasses
Keep tools organised
See you tomorrow
```

</details>

<details>
<summary>Punkt 9: poprawiony program</summary>

Definicja stoi przed `main`, więc w linijce wywołania kompilator już zna funkcję:

<!-- example: rules_before_main -->
```cpp
#include <iostream>

void show_workshop_rules() {
    std::cout << "Wear safety glasses\n";
    std::cout << "Keep tools organised\n";
}

int main() {
    std::cout << "Morning briefing\n";
    show_workshop_rules();
}
```

<!-- output: rules_before_main -->
```text
Morning briefing
Wear safety glasses
Keep tools organised
```

</details>

<details>
<summary>Punkt 10: misja, przerwy między rundami</summary>

<!-- example: round_breaks -->
```cpp
#include <iostream>

void show_break() {
    std::cout << "Break: drink water\n";
    std::cout << "Break: stretch\n";
}

int main() {
    int round_count{0};

    std::cout << "Enter round count (0-5):\n";
    std::cin >> round_count;

    if (round_count >= 0 && round_count <= 5) {
        for (int round_number{1}; round_number <= round_count; ++round_number) {
            std::cout << "Round " << round_number << "\n";

            if (round_number < round_count) {
                show_break();
            }
        }

        std::cout << "Training complete\n";
    } else {
        std::cout << "Invalid round count\n";
    }
}
```

- **Definicja** funkcji `show_break` stoi przed `main`. **Wywołanie** `show_break();` stoi w pętli, w `main`.
- **Funkcja nie wie, która runda trwa.** Wypisuje zawsze te same dwie linijki. O tym, czy przerwa jest potrzebna, decyduje `main`: po rundzie `round_number` będzie następna runda tylko wtedy, gdy `round_number < round_count`.
- **Po ostatniej rundzie** warunek daje `false`, więc przerwy nie ma. Dla jednej rundy warunek `1 < 1` daje `false` już w pierwszym przebiegu.
- **Dla zera rund** warunek pętli `1 <= 0` od razu daje `false`. Nie ma żadnej rundy ani przerwy, a program wypisuje `Training complete`.
- **Inne poprawne rozwiązanie:** wywołać funkcję **przed** wypisaniem rundy, ale tylko od drugiej rundy, z warunkiem `round_number > 1`. Wynik jest taki sam.
- Zakres jest sprawdzany przez `if`/`else`, zanim program zacznie plan, tak jak w lekcji 4.1.
- Funkcja nie potrzebuje numeru rundy, bo przerwa jest zawsze taka sama. Gdyby przerwa miała pokazywać numer rundy, funkcja musiałaby go dostać. Jak przekazać funkcji dane, zobaczysz w kolejnej lekcji.

</details>

**Poprzednia lekcja:** [Lekcja 4.7: Program powtarza działania (sprawdzian Modułu 4)](../module_04_repeating_actions/lesson_07_the_program_repeats.md) · **Następna lekcja:** w przygotowaniu · [Opis kursu](../../README.md)

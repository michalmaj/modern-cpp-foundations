# Lekcja 10.5: Zapisy na warsztaty (sprawdzian Modułu 10)

**Polski** · [English](lesson_05_workshop_registrations.en.md) · [Opis kursu](../../README.md)

> **Moduł 10, lekcja 5: sprawdzian** · około 115–140 minut, w dwóch podejściach
> **Potrzebujesz:** katalogu `cpp-workspace` i oryginalnego projektu `lesson_05_first_program`.
> **Wersja pilotażowa.** Rozwiązania referencyjne z tej lekcji sprawdzamy automatycznie na Windowsie, Ubuntu i macOS, z podanymi danymi wejściowymi. Twojej pracy nic nie ocenia automatycznie: sprawdzasz ją samodzielnie, według kryteriów. Wpisywanie danych w oknie **Run** CLiona opisujemy bez ręcznego sprawdzenia na każdym systemie.

## Jak przebiega ten sprawdzian

Ta lekcja nie wprowadza niczego nowego. Sprawdzasz, czy potrafisz samodzielnie zaprojektować program, który **odczytuje z wejścia nieznaną z góry liczbę rekordów, bezpiecznie buduje z nich wektor, a potem analizuje gotową kolekcję funkcją, która dostaje ją przez `const&`**. Łączysz w nim lekcje 10.1–10.4 z wektorem z Modułu 6, funkcjami analizującymi kolekcję z Modułu 8 i referencjami z Modułu 9. Nowe jest tylko to połączenie: kolekcja zbudowana z danych wejściowych trafia do zaprojektowanej przez Ciebie funkcji analizującej.

Lekcja ma dwie części:

- **Część A: sprawdzian.** Zadanie 1: wymagania, format danych, raport, przykłady i kryteria. Bez podpowiedzi i bez kodu rozwiązań. Wszystko, czego potrzebujesz, znasz z Modułów 1–10.
- **Część B: sprawdzenie i omówienie.** Podpowiedzi, pełna lista przypadków kontrolnych, zadanie 2 (diagnostyka) i zadanie 3 (wyjaśnienia), które wykonujesz po zadaniu 1, a potem rozwiązanie referencyjne, poprawki, odpowiedzi i samoocena. Przejdź do niej dopiero po wykonaniu części A albo wtedy, gdy świadomie zrezygnujesz z dalszej samodzielnej próby.

Zajrzenie do części B, do wcześniejszych lekcji albo do notatek nie jest porażką. Ważne jest, żeby **uczciwie zanotować, co zrobiono samodzielnie, a co z pomocą**. Proponowany podział na dwa podejścia:

- **pierwsze:** analiza umowy danych, projekt typu i dwóch funkcji, pętla odczytu i raport dla danych z wymagań;
- **drugie:** błędy i przypadki graniczne, pusty import, zadania 2 i 3, porównanie z rozwiązaniem i samoocena.

**Możesz używać:** CLiona albo terminala, CMake i Ninja, jak dotąd; `CMakeLists.txt` skopiowanego z oryginalnego `lesson_05_first_program`; tabel przypadków i przebiegu oraz tymczasowych wydruków testowych. Debugger nie jest potrzebny. Nie musisz kończyć danych z klawiatury: wpisane dane kończysz pustą linią, a przypadki, w których dane kończą się bez pustej linii, analizujesz na papierze.

---

# Część A: sprawdzian

## Zadanie 1: Zapisy na warsztaty

Organizatorzy warsztatów zbierają zgłoszenia uczestników. Każda osoba zapisuje się do jednej z dwóch grup, **grupy 1, podstawowej**, albo **grupy 2, zaawansowanej**, i wybiera, na ile zajęć przyjdzie. Program odczytuje wszystkie zgłoszenia z wejścia, a potem wypisuje raport dla organizatorów. Nie modeluje limitów miejsc, płatności, dat ani terminów zajęć.

**Przygotowanie:** w `cpp-workspace` utwórz katalog `workshop_registrations`, skopiuj do niego `CMakeLists.txt` z oryginalnego `lesson_05_first_program`, utwórz **pusty** `main.cpp` i napisz cały program samodzielnie.

### Dane wejściowe

Każde zgłoszenie zajmuje dwie linie:

1. imię i nazwisko uczestnika, które może zawierać spacje;
2. dwie liczby oddzielone spacją: numer grupy i liczba zajęć.

Na przykład w tym zgłoszeniu osoba `Ala Nowak` zapisuje się do grupy 1 na dwa zajęcia:

```text
Ala Nowak
1 2
```

Liczby zgłoszeń nikt nie zapowiada. Odczyt kończy się, gdy w miejscu następnego imienia i nazwiska jest **pusta linia** albo gdy **dane się kończą**. Pusta linia nie jest zgłoszeniem.

### Reguły

- Imię i nazwisko nie jest puste, bo pusta linia kończy dane. Może zawierać spacje między słowami, ale w danych zgodnych z umową nie ma spacji na początku ani na końcu. Dwie osoby mogą mieć takie samo imię i nazwisko: to wciąż dwa zgłoszenia.
- Numer grupy wynosi dokładnie 1 albo 2.
- Liczba zajęć wynosi od 1 do 6 włącznie.
- Wszystkie dane są tekstem ASCII. Liczby są niewielkie i mieszczą się w `int`, ich suma też. W danych zgodnych z umową jest najwyżej 5 zgłoszeń.
- Program nie sprawdza tekstu po drugiej liczbie, spacji na początku i końcu imienia i nazwiska, linii złożonych z samych spacji, powtórzeń ani liczby zgłoszeń. Takie dane są poza umową.

### Błędy

- **`Input error`:** nie udało się odczytać którejś z dwóch liczb zgłoszenia. Zamiast liczby jest słowo albo dane kończą się po niepustym imieniu i nazwisku lub po pierwszej liczbie. Rozpoczęte zgłoszenie bez wymaganej liczby to błąd, a nie zakończenie danych.
- **`Invalid registrations`:** obie liczby udało się odczytać, ale numer grupy nie wynosi 1 ani 2 albo liczba zajęć jest spoza zakresu 1–6.
- Gdy nie udało się odczytać którejś liczby, wynik to `Input error`, nawet jeśli druga liczba łamie zasady.
- Przy pierwszym błędzie program wypisuje dokładnie jeden z tych komunikatów i kończy pracę: nie czyta dalszych danych i nie wypisuje żadnej części raportu. Wcześniej przyjęte zgłoszenia mogą już być w wektorze i nie trzeba ich usuwać. Program nie poprawia danych i nie przywraca strumienia.

### Typ i dwie funkcje

- Program definiuje **jeden własny typ** zgłoszenia z trzema polami: imieniem i nazwiskiem (`std::string`), numerem grupy (`int`) i liczbą zajęć (`int`). Bez dodatkowych pól: ani nazwy grupy, którą wyznacza numer, ani liczby wszystkich zgłoszeń. Nazwy typu i pól wybierasz samodzielnie.
- **Funkcja odczytująca liczby jednego zgłoszenia** dostaje strumień wejścia, z którego czyta `main`, imię i nazwisko odczytane już przez `main` oraz istniejący rekord wynikowy przygotowany przez `main`. Czyta dalej z tego samego strumienia, nie kopiuje imienia i nazwiska ani go nie zmienia, a kompletne zgłoszenie zapisuje w rekordzie wywołującego. Zwraca `true` albo `false`. Przy `false` żadne pole rekordu wynikowego się nie zmienia, nawet gdy jedną liczbę udało się już odczytać. Niczego nie wypisuje i niczego nie dodaje do wektora.
- **Funkcja licząca uczestników grupy** dostaje gotową kolekcję zgłoszeń i numer grupy. Przegląda całą kolekcję bez kopiowania jej i bez możliwości zmiany jej elementów, a zwraca liczbę zgłoszeń z tym numerem grupy. To liczba elementów, jak w lekcji 8.4. Niczego nie wypisuje, nie zmienia kolekcji i nie tworzy nowego wektora.
- Typy parametrów i sposób ich przekazania wybierasz samodzielnie, tak żeby funkcje spełniały te umowy. Obie funkcje mają różne zadania: pierwsza w kontrolowany sposób zmienia jeden obiekt, druga tylko odczytuje całą kolekcję. Trzecia funkcja nie jest potrzebna. Możesz dodać własną funkcję pomocniczą, na przykład wypisującą albo sumującą, jeśli korzysta tylko z poznanych konstrukcji i nie zmienia kolekcji.
- **`main`** odczytuje imiona i nazwiska, rozpoznaje zakończenie danych, przygotowuje rekord wynikowy, wywołuje funkcję odczytującą i dodaje zgłoszenie do początkowo pustego wektora przez `push_back` tylko po `true`. Po odmowie wybiera komunikat. Funkcja odczytująca zwraca tylko `true` albo `false`: bez nowego typu wyniku.
- Raport `main` wypisuje dopiero po zakończeniu odczytu, wyłącznie z elementów wektora. Nie wystarczy liczyć grup i zajęć w trakcie odczytu, bez przechowywania zgłoszeń. Program nie wypisuje pytań i nie używa zmiennych zadeklarowanych poza funkcjami.

### Raport

Po zakończeniu danych program wypisuje, w tej kolejności:

1. `Registrations:` i liczbę zgłoszeń z `size()`;
2. `Group 1:` i liczbę zgłoszeń do grupy 1 z funkcji liczącej;
3. `Group 2:` i liczbę zgłoszeń do grupy 2 z tej samej funkcji;
4. `Sessions total:` i sumę liczb zajęć wszystkich zgłoszeń, obliczoną z elementów wektora;
5. `Group 2 participants:`, a pod spodem imiona i nazwiska uczestników grupy 2, każde w osobnej linii, w kolejności z danych. Gdy grupa 2 nie ma żadnego zgłoszenia, zamiast nich jest jedna linia `(none)`.

Liczba zgłoszeń, liczby uczestników obu grup i suma zajęć to cztery różne informacje: na przykład suma zajęć nie jest liczbą uczestników. Program nie wypisuje innych komunikatów ani pustych linii.

### Przykłady

**Przykład A:** dane z wymagań, zakończone pustą linią.

<!-- input: workshop_registrations -->
```text
Ala Nowak
1 2
Jan Lis
2 4
Maja Kot
1 1
Olek Wrona
2 3

```

<!-- output: workshop_registrations -->
```text
Registrations: 4
Group 1: 2
Group 2: 2
Sessions total: 10
Group 2 participants:
Jan Lis
Olek Wrona
```

Grupa 1 to `Ala Nowak` i `Maja Kot`, a grupa 2 to `Jan Lis` i `Olek Wrona`. Suma zajęć to 2 + 4 + 1 + 3 = 10.

**Przykład B:** te same dane bez pustej linii, zakończone końcem danych. Wynik jest taki sam jak w przykładzie A.

<!-- input: workshop_registrations -->
```text
Ala Nowak
1 2
Jan Lis
2 4
Maja Kot
1 1
Olek Wrona
2 3
```

<!-- output: workshop_registrations -->
```text
Registrations: 4
Group 1: 2
Group 2: 2
Sessions total: 10
Group 2 participants:
Jan Lis
Olek Wrona
```

**Przykład C:** dane zaczynają się od pustej linii. Pusty wektor to poprawny wynik, a nie błąd.

<!-- input: workshop_registrations -->
```text

```

<!-- output: workshop_registrations -->
```text
Registrations: 0
Group 1: 0
Group 2: 0
Sessions total: 0
Group 2 participants:
(none)
```

**Przykład D:** zamiast liczby zajęć drugiego zgłoszenia jest słowo. Pierwsze zgłoszenie mogło już trafić do wektora, ale raportu nie ma.

<!-- input: workshop_registrations -->
```text
Ala Nowak
1 2
Jan Lis
2 four
```

<!-- output: workshop_registrations -->
```text
Input error
```

**Przykład E:** drugie zgłoszenie ma numer grupy 3.

<!-- input: workshop_registrations -->
```text
Ala Nowak
1 2
Jan Lis
3 4
```

<!-- output: workshop_registrations -->
```text
Invalid registrations
```

**Przykład F:** wszystkie zgłoszenia są do grupy 1. **Przewidź** raport, zanim napiszesz program.

<!-- input: workshop_registrations -->
```text
Ala Nowak
1 1
Maja Kot
1 3

```

<details>
<summary>Standardowe wyjście dla przykładu F</summary>

<!-- output: workshop_registrations -->
```text
Registrations: 2
Group 1: 2
Group 2: 0
Sessions total: 4
Group 2 participants:
(none)
```

Brak zgłoszeń do grupy 2 nie jest błędem: ta grupa jest po prostu pusta.

</details>

### Jak pracować

Proponowana kolejność to plan pracy, a nie dwanaście osobnych programów ani uruchomień:

1. Zapisz umowę: pola zgłoszenia, zasady i oba rodzaje błędów.
2. Zaprojektuj typ zgłoszenia.
3. Zaprojektuj funkcję odczytującą liczby jednego zgłoszenia: jej parametry, sposób ich przekazania i znaczenie wyniku.
4. Zaprojektuj funkcję liczącą uczestników grupy.
5. Utwórz pusty wektor.
6. Zorganizuj odczyt imion i nazwisk aż do zakończenia danych.
7. Dodawaj do wektora tylko kompletne zgłoszenia.
8. Obsłuż pierwszy błąd bez raportu.
9. Sprawdź pustą kolekcję.
10. Wypisz raport z całego wektora.
11. Sprawdź liczenie obu grup i sumę zajęć.
12. Sprawdź, czy imiona i nazwiska grupy 2 stoją w kolejności z danych.

**Zanim uruchomisz program**, przygotuj tabelę przypadków z oczekiwanymi wynikami: pusta linia na początku; jedno, dwa i pięć zgłoszeń; oba sposoby zakończenia; wszystkie zgłoszenia w grupie 1 i wszystkie w grupie 2; grupy w mieszanej kolejności; to samo imię i nazwisko dwa razy; grupa 0, 3 i ujemna; 0, 1, 6, 7 i ujemna liczba zajęć; słowo zamiast numeru grupy i zamiast liczby zajęć; koniec danych po imieniu i nazwisku oraz po pierwszej liczbie; błąd w zgłoszeniu po poprawnym. Przy każdym przypadku zapisz cały oczekiwany raport albo komunikat.

**Uruchom program** dla przykładu A i dla jednego z błędów w drugim zgłoszeniu, z przykładu D albo E. Każdą linię kończ klawiszem **Enter**, a po ostatnim zgłoszeniu naciśnij **Enter** jeszcze raz, na pustej linii. Pozostałe przypadki przeanalizuj na papierze. Wszystkie przypadki z pełnej listy kontrolnej są sprawdzone automatycznie.

Gdy wynik się zgadza, możesz zapisać projekt w Gicie, jak w lekcji 1.5. Przed commitem sprawdź `git status`: do historii trafiają tylko `main.cpp` i `CMakeLists.txt`.

## Kryteria sukcesu

Sprawdzian jest zaliczony, gdy spełniasz **wszystkie** kryteria. Możesz przy tym korzystać z części B, jeśli uczciwie zaznaczysz to w samoocenie.

- `workshop_registrations/main.cpp` napisano od pustego pliku, w poprawnym C++20. Program buduje się bez błędów.
- Jest jeden typ zgłoszenia z trzema polami wymaganych typów, a zgłoszenia trafiają do jednego wektora, w kolejności z danych.
- Funkcja odczytująca czyta z tego samego strumienia co `main`, dostaje imię i nazwisko bez kopiowania i bez możliwości zmiany i wypełnia rekord przygotowany przez `main`. Przy odmowie nie zmienia żadnego jego pola, także gdy jedną liczbę udało się odczytać.
- Funkcja licząca dostaje kolekcję bez kopiowania i bez możliwości zmiany, przegląda wszystkie elementy i zwraca liczbę zgłoszeń wybranej grupy.
- Żadna z dwóch funkcji niczego nie wypisuje. Zasady grupy i liczby zajęć stoją w programie w jednym miejscu.
- `main` kończy odczyt po pustej linii i po końcu danych w miejscu imienia i nazwiska, a przy rozpoczętym, niekompletnym zgłoszeniu wypisuje `Input error`. `push_back` wykonuje się tylko po `true`, a przy błędzie nie ma żadnej części raportu.
- Raport pochodzi z elementów wektora: liczba zgłoszeń z `size()`, liczby uczestników grup z funkcji liczącej, a suma zajęć oraz imiona i nazwiska z elementów.
- Dla przykładu A i wybranego błędu w drugim zgłoszeniu program wypisuje dokładnie pokazane wyniki. Pozostałe przykłady i przypadki z Twojej tabeli zgadzają się z analizą na papierze i z pełną listą kontrolną.
- Tabela przypadków powstała przed uruchomieniem programu.
- Błąd z diagnostyki A poprawiono i sprawdzono, a fragment z diagnostyki B przeanalizowano bez uruchamiania (zadanie 2 w części B).
- Umiesz wyjaśnić każdą linijkę swojego programu i odpowiedzieć na pytania z zadania 3.

Nazwy typu, pól, funkcji i zmiennych oraz podział `main` mogą być inne niż w rozwiązaniu referencyjnym, jeśli są czytelne i spełniają wymagania. Poprawny wynik to warunek konieczny, ale **nie dowód zrozumienia**. Dlatego zadania 2 i 3 są częścią sprawdzianu.

---

# Część B: sprawdzenie i omówienie

Przejdź tutaj **dopiero po wykonaniu części A** albo wtedy, gdy świadomie zrezygnujesz z dalszej samodzielnej próby. Ta część zawiera podpowiedzi, a dalej kod bardzo zbliżony do rozwiązania zadania 1.

## Jak sprawdzić swoją pracę

- **Standardowe wyjście:** porównaj linie programu z oczekiwanymi, znak po znaku, także dwukropki, spacje i kolejność imion i nazwisk. Przy poprawnych danych sprawdzaj cały raport, a nie tylko liczby.
- **Liczby raportu:** czy liczba zgłoszeń równa się sumie liczb uczestników obu grup? Czy suma zajęć zgadza się z dodawaniem w Twojej tabeli? Zgodność tych liczb nie dowodzi poprawności, ale niezgodność zawsze oznacza błąd.
- **Rekord po odmowie:** czy funkcja odczytująca zostawia rekord wynikowy bez zmian także wtedy, gdy pierwszą liczbę udało się odczytać? Raport tego nie pokaże, bo po błędzie program kończy pracę. Pomoże w tym program kontrolny przy rozwiązaniu referencyjnym.
- **Odpowiedzialności:** czy któraś z funkcji coś wypisuje? Czy zasady grupy i liczby zajęć stoją też w `main`? Czy funkcja licząca mogłaby zmienić kolekcję?

## Podpowiedzi

<details>
<summary>Podpowiedź 1</summary>

Które zadanie należy do funkcji odczytującej pojedynczy rekord, a które do funkcji analizującej gotową kolekcję? Która z nich potrzebuje modyfikowalnej referencji?

</details>

<details>
<summary>Podpowiedź 2</summary>

Odczytuj liczby do zmiennych lokalnych i zmieniaj rekord wynikowy dopiero po sprawdzeniu wszystkich zasad. Pusta linia w miejscu nazwy kończy import, ale brak liczby po nazwie jest błędem.

</details>

<details>
<summary>Podpowiedź 3</summary>

Po zbudowaniu wektora przekaż go przez `const&` do funkcji liczącej uczestników grupy. Raport liczby zgłoszeń, sumy zajęć i nazw grupy 2 powinien opierać się na elementach gotowej kolekcji.

</details>

## Pełna lista przypadków kontrolnych

<details>
<summary>Otwórz po przygotowaniu własnej tabeli</summary>

Kolejne linie danych oddziela `/`. Przy poprawnych danych kolumna „Wynik” podaje liczbę zgłoszeń, liczby uczestników grup 1 i 2, sumę zajęć oraz imiona i nazwiska z grupy 2. Program wypisuje wtedy cały raport, jak w przykładzie A.

| | Dane | Wynik | Co sprawdza |
|---|---|---|---|
| A | `Ala Nowak` / `1 2` / `Jan Lis` / `2 4` / `Maja Kot` / `1 1` / `Olek Wrona` / `2 3` / pusta linia | 4; 2 i 2; 10; `Jan Lis`, `Olek Wrona` | dane z wymagań: grupy w mieszanej kolejności, zakończenie pustą linią |
| B | to samo bez pustej linii, potem koniec danych | jak w A | koniec danych po kompletnym zgłoszeniu |
| C | pusta linia | 0; 0 i 0; 0; `(none)` | pusty import |
| D | `Ala Nowak` / `1 2` / `Jan Lis` / `2 four` | `Input error` | słowo zamiast liczby zajęć w drugim zgłoszeniu; bez częściowego raportu |
| E | `Ala Nowak` / `1 2` / `Jan Lis` / `3 4` | `Invalid registrations` | grupa 3 w drugim zgłoszeniu; bez częściowego raportu |
| F | `Ala Nowak` / `1 1` / `Maja Kot` / `1 3` / pusta linia | 2; 2 i 0; 4; `(none)` | wszystkie zgłoszenia w grupie 1; jedne zajęcia |
| G | `Ewa Maj` / `2 6`, potem koniec danych | 1; 0 i 1; 6; `Ewa Maj` | jedno zgłoszenie; wszystkie w grupie 2; sześć zajęć |
| H | `Jan Lis` / `2 4` / `Ala Nowak` / `1 2` / `Jan Lis` / `2 1` / `Anna Maria Zielinska` / `2 6` / `Piotr Nowak` / `1 5` / pusta linia | 5; 2 i 3; 18; `Jan Lis`, `Jan Lis`, `Anna Maria Zielinska` | pięć zgłoszeń; to samo imię i nazwisko dwa razy; trzy słowa w linii; grupa 1 dopiero na drugiej pozycji |
| I | `Ala Nowak` / `0 2` | `Invalid registrations` | grupa 0 |
| J | `Ala Nowak` / `-1 2` | `Invalid registrations` | ujemna grupa |
| K | `Ala Nowak` / `1 0` | `Invalid registrations` | zero zajęć |
| L | `Ala Nowak` / `2 7` | `Invalid registrations` | siedem zajęć |
| M | `Ala Nowak` / `1 -3` | `Invalid registrations` | ujemna liczba zajęć |
| N | `Ala Nowak` / `one 2` | `Input error` | słowo zamiast numeru grupy |
| O | `Ala Nowak`, potem koniec danych | `Input error` | brak liczb po niepustym imieniu i nazwisku |
| P | `Ala Nowak` / `1`, potem koniec danych | `Input error` | brak drugiej liczby |
| Q | `Ala Nowak` / `3 four` | `Input error` | nieudany odczyt ma pierwszeństwo przed niedozwoloną grupą |
| R | `Ala Nowak` / `1 2` / pusta linia / `Jan Lis` / `3 4` | 1; 1 i 0; 2; `(none)` | pusta linia kończy dane, więc dalszych linii program nie odczytuje |

**Testy automatyczne i Twoje próby.** Wszystkie przypadki są sprawdzone automatycznie: rozwiązanie referencyjne jest uruchamiane dla każdego z nich, a jego pełne standardowe wyjście porównywane z oczekiwanym. Rozwiązanie i jego wyniki są w części [Rozwiązanie referencyjne](#rozwiązanie-referencyjne).

</details>

## Zadanie 2: Diagnostyka

Wykonaj to zadanie **po zadaniu 1**, przed zajrzeniem do rozwiązania referencyjnego. Oba problemy dotyczą programów podobnych do Twojego.

<details>
<summary>Diagnostyka A: funkcja licząca kończy się za wcześnie (otwórz dopiero po zadaniu 1)</summary>

W `cpp-workspace` utwórz katalog `diagnosis_10`, skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program` i umieść w `main.cpp` program poniżej: możesz go przepisać albo skopiować. Program sprawdza tylko funkcję liczącą, więc zgłoszenia są zapisane w kodzie, a nie odczytywane z wejścia. Funkcja ma działać tak samo jak funkcja licząca z zadania 1.

<!-- example: group_count_bug -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>
#include <vector>

struct Registration {
    std::string name;
    int group;
    int sessions;
};

std::size_t count_group(const std::vector<Registration>& registrations, int group) {
    std::size_t count{0};

    for (const Registration& registration : registrations) {
        if (registration.group == group) {
            ++count;
        }

        return count;
    }

    return count;
}

int main() {
    const std::vector<Registration> registrations{
        {"Ala Nowak", 1, 2}
    };

    std::cout << "Registrations: " << registrations.size() << "\n";
    std::cout << "Group 1: " << count_group(registrations, 1) << "\n";
    std::cout << "Group 2: " << count_group(registrations, 2) << "\n";
}
```

1. **Przewidź** wynik dla danych z programu: jedno zgłoszenie do grupy 1. Potem uruchom program. Czy wynik wygląda poprawnie?
2. **Przewidź** wynik dla pustego wektora. Dlaczego pusty wektor nie ujawnia błędu?
3. Zmień zgłoszenia w wektorze tak, żeby błąd stał się widoczny. Zapisz poprawne liczby uczestników obu grup dla swoich danych.
4. **Przewidź**, ile przebiegów pętli wykona funkcja dla Twoich danych i co wypisze program. Potem uruchom program.
5. Wskaż `return`, który wykonuje się za wcześnie. Dlaczego kończy całą funkcję, a nie tylko jeden przebieg pętli?
6. Dlaczego poprawny wynik dla jednego zgłoszenia nie dowodzi, że funkcja jest poprawna?
7. W lekcji 9.4 `return` w pętli był zamierzony. Czym liczenie wszystkich pasujących zgłoszeń różni się od wyszukania jednego rekordu?
8. Popraw funkcję i uruchom program ponownie dla swoich danych.

</details>

<details>
<summary>Diagnostyka B: niekompletne zgłoszenie uznane za zakończenie danych (otwórz dopiero po zadaniu 1)</summary>

Ten fragment przeanalizuj **na papierze**, bez uruchamiania. To pętla odczytu z innej wersji programu z zadania 1. Odczytuje imię i nazwisko na początku każdego przebiegu, jak pętla z lekcji 7.4, a po pętli program wypisuje raport. Funkcja `read_registration_values` działa poprawnie: czyta obie liczby, sprawdza odczyt i zasady i przy `false` niczego nie zmienia.

<!-- fragment -->
```cpp
bool reading{true};

while (reading) {
    std::string name{};
    std::getline(std::cin, name);

    if (std::cin.fail() || name.empty()) {
        reading = false;
    } else {
        Registration registration{"", 0, 0};
        const bool accepted{read_registration_values(std::cin, name, registration)};

        if (accepted) {
            registrations.push_back(registration);

            std::string rest{};
            std::getline(std::cin, rest);
        } else {
            reading = false;
        }
    }
}
```

Dane, po których wejście się kończy:

```text
Ala Nowak
1 2
Jan Lis
2
```

1. Co wypisze program z tą pętlą dla tych danych, a jaki wynik jest poprawny?
2. Dlaczego drugie zgłoszenie już się rozpoczęło?
3. Dlaczego brak liczby zajęć to błąd odczytu, a nie zakończenie danych?
4. Dlaczego nie wolno traktować każdego `false` jak końca danych? Co ta wersja wypisałaby, gdyby drugie zgłoszenie miało `3 4`?
5. Dlaczego nie wolno wypisać raportu z jednym zgłoszeniem?
6. Jak rozdzielić decyzję o zakończeniu danych od decyzji o odmowie zgłoszenia? Co powinna zrobić gałąź `else` po `false`?

</details>

Wyniki, przykładowe dane i poprawki są w części [Diagnostyka: wyniki i poprawki](#diagnostyka-wyniki-i-poprawki).

## Zadanie 3: Wyjaśnij swój projekt

Odpowiedz krótko, na piśmie, odwołując się do własnego programu z zadania 1, zanim otworzysz rozwiązanie referencyjne:

1. Dlaczego odczyt liczb jednego zgłoszenia stoi w osobnej funkcji, a odczyt imion i nazwisk i cała pętla w `main`?
2. Jak Twoja funkcja odczytująca dostaje strumień i rekord wynikowy? Dlaczego oba parametry to referencje bez `const`?
3. Dlaczego funkcja nie może zmienić rekordu wynikowego przed sprawdzeniem wszystkich zasad, choć `main` po odmowie i tak kończy pracę?
4. Kiedy `main` wywołuje `push_back`? Co jest w wektorze po błędzie w drugim zgłoszeniu i dlaczego program nie wypisuje części raportu?
5. Jak program odróżnia pustą linię od nieudanego odczytu imienia i nazwiska, a jak rozpoczęte, niekompletne zgłoszenie od zakończenia danych?
6. Dlaczego funkcja licząca dostaje wektor przez `const&` i dlaczego jej zmienna pętli też ma `const&`?
7. Dlaczego funkcja licząca musi przejrzeć całą kolekcję, skoro wyszukiwanie z lekcji 9.4 kończyło się po znalezieniu rekordu?
8. Czym różnią się liczba zgłoszeń, liczby uczestników obu grup i suma zajęć? Która zależność między nimi zawsze zachodzi, a która tylko dla niektórych danych?
9. Dlaczego brak uczestników grupy 2 nie jest błędem? Skąd Twój program wie, że ma wypisać `(none)`?
10. Funkcja odczytująca zwróciła `true` dla każdego zgłoszenia, a funkcja licząca zwróciła liczby. Czy to dowodzi, że raport jest poprawny? Jak to sprawdzasz?

## Rozwiązanie referencyjne

Zajrzyj tutaj **po wykonaniu zadań 1–3**. Twoje nazwy i układ `main` mogą być inne, jeśli program spełnia wymagania.

<details>
<summary>Zadanie 1: zapisy na warsztaty</summary>

<!-- example: workshop_registrations -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>
#include <vector>

struct Registration {
    std::string name;
    int group;
    int sessions;
};

bool read_registration_values(std::istream& input, const std::string& name, Registration& result) {
    int group{0};
    int sessions{0};
    input >> group;
    input >> sessions;

    if (input.fail()) {
        return false;
    }

    if (group != 1 && group != 2) {
        return false;
    }

    if (sessions < 1 || sessions > 6) {
        return false;
    }

    result = Registration{name, group, sessions};
    return true;
}

std::size_t count_group(const std::vector<Registration>& registrations, int group) {
    std::size_t count{0};

    for (const Registration& registration : registrations) {
        if (registration.group == group) {
            ++count;
        }
    }

    return count;
}

int main() {
    std::vector<Registration> registrations{};
    std::string name{};
    std::getline(std::cin, name);

    while (!std::cin.fail() && !name.empty()) {
        Registration registration{"", 0, 0};
        const bool accepted{read_registration_values(std::cin, name, registration)};

        if (!accepted) {
            if (std::cin.fail()) {
                std::cout << "Input error\n";
            } else {
                std::cout << "Invalid registrations\n";
            }

            return 0;
        }

        registrations.push_back(registration);

        std::string rest{};
        std::getline(std::cin, rest);

        if (!std::cin.fail()) {
            std::getline(std::cin, name);
        }
    }

    const std::size_t basic_count{count_group(registrations, 1)};
    const std::size_t advanced_count{count_group(registrations, 2)};
    int sessions_total{0};

    for (const Registration& registration : registrations) {
        sessions_total += registration.sessions;
    }

    std::cout << "Registrations: " << registrations.size() << "\n";
    std::cout << "Group 1: " << basic_count << "\n";
    std::cout << "Group 2: " << advanced_count << "\n";
    std::cout << "Sessions total: " << sessions_total << "\n";
    std::cout << "Group 2 participants:\n";

    if (advanced_count == 0) {
        std::cout << "(none)\n";
    }

    for (const Registration& registration : registrations) {
        if (registration.group == 2) {
            std::cout << registration.name << "\n";
        }
    }
}
```

1. **Imię i nazwisko odczytuje `main`,** bo przy tej linii rozstrzyga się, czy dane się skończyły. Funkcja odczytująca jest wywoływana dopiero wtedy, gdy zgłoszenie się zaczęło.
2. **Strumień przez `std::istream&`,** bo funkcja ma czytać dalej z istniejącego `std::cin`, od miejsca, w którym skończył `main`. Bez `const`, bo odczyt zmienia strumień.
3. **Rekord wynikowy przez `Registration&`,** bo funkcja ma dwa wyniki: `bool` mówi o powodzeniu, a kompletne zgłoszenie trafia do obiektu przygotowanego przez `main`.
4. **Odczyt przed przypisaniem:** obie liczby trafiają najpierw do zmiennych lokalnych, bo w trakcie odczytu nie wiadomo jeszcze, czy powstanie poprawne zgłoszenie. Po nieudanym odczycie na wartości zmiennej nie wolno polegać (lekcja 4.6), więc zasady sprawdza się dopiero po `input.fail()`. W tym zadaniu w liczbie, której nie udało się odczytać, zostaje 0 (lekcja 10.1), a 0 łamie zasady obu pól, więc program bez tego sprawdzenia wypisałby te same wyniki. Sprawdzenie zostaje, bo umowa funkcji nie może zależeć od tego, co zostało w zmiennej: przy zasadach, które dopuszczają 0, jak w misji z lekcji 10.4, taki program przyjąłby liczbę, której nie było w danych.
5. **Przy `false` rekord jest bez zmian,** bo każde `return false;` stoi przed `result = Registration{name, group, sessions};`. To zasada „wszystko albo nic” z lekcji 9.2.
6. **Pusta linia to co innego niż nieudany odczyt:** pusta linia to udany odczyt tekstu o długości zero (lekcja 7.4), a umowa mówi, że kończy dane. Nieudany odczyt imienia i nazwiska oznacza, że danych już nie ma. Oba kończą odczyt i żadne nie tworzy zgłoszenia.
7. **Brak liczby po niepustym imieniu i nazwisku to błąd,** bo zgłoszenie już się zaczęło. Funkcja zwraca `false`, a `std::cin.fail()` daje `true`, więc wynik to `Input error`, a nie raport.
8. **`push_back` tylko po `true`,** bo do wektora mają trafiać wyłącznie kompletne, sprawdzone zgłoszenia (lekcja 10.3).
9. **Kolekcja przez `const std::vector<Registration>&`,** bo funkcja licząca ma tylko odczytać gotowy wektor z `main`: bez kopii i bez możliwości zmiany (lekcja 8.4).
10. **Element przez `const Registration&`,** bo pętla tylko porównuje pole `group`. Bez `&` każdy przebieg kopiowałby zgłoszenie, a bez `const` pętla mogłaby je zmienić.
11. **Bez kopii wektora:** przez `const&` funkcja pracuje na wektorze z `main`. Kopia nie zmieniłaby wyniku, ale niczego by nie dała, a przy dużej kolekcji kosztowałaby czas i pamięć.
12. **`std::size_t`,** bo funkcja zwraca liczbę elementów, tak jak `size()` (lekcje 6.3 i 8.4). Dlatego program dołącza `<cstddef>`.
13. **Liczba zgłoszeń z `size()`,** bo w wektorze są dokładnie przyjęte zgłoszenia. Osobny licznik w pętli odczytu powtarzałby tę informację i mógłby się z nią rozjechać.
14. **Suma zajęć to nie liczba uczestników:** dodaje pola `sessions`, a nie liczy rekordy. Dla danych z wymagań wynosi 10 przy 4 zgłoszeniach. Obie liczby byłyby równe tylko wtedy, gdyby każde zgłoszenie miało jedne zajęcia.
15. **Raport dopiero po zakończeniu odczytu,** bo każda jego linia dotyczy wszystkich danych. Przy błędzie w późniejszym zgłoszeniu program kończy pracę przez `return 0;`, zanim wypisze cokolwiek z raportu.
16. **`false` funkcji odczytującej nie oznacza końca danych:** znaczy, że rozpoczęte zgłoszenie jest błędne i nowego rekordu nie ma. Zakończenie danych `main` rozpoznaje sam, zanim wywoła funkcję, a przyczynę odmowy podaje `std::cin.fail()`.
17. **Brak grupy 2 to nie błąd:** dane zgodne z umową mogą nie mieć ani jednego zgłoszenia do grupy 2. Funkcja zwraca wtedy 0, pętla imion i nazwisk niczego nie wypisuje, a `(none)` mówi, że lista jest pusta.
18. **Wynik funkcji nie zastępuje sprawdzenia kolekcji:** `true` mówi tylko, że jedno zgłoszenie jest poprawne, a funkcja licząca może podać złą liczbę, jak w diagnostyce A. `Group 2` i lista pod `Group 2 participants:` opisują te same elementy wektora, więc muszą się zgadzać, a przypadki kontrolne porównują cały raport.

**Inne poprawne rozwiązania:**

- pętla, która odczytuje imię i nazwisko na początku każdego przebiegu, jak w lekcji 7.4, z flagą `bool`;
- flaga zamiast `return 0;`, jeśli po błędzie program nie wypisuje raportu;
- zasada grupy zapisana jako `group < 1 || group > 2` albo wszystkie zasady w jednym warunku połączonym przez `||`;
- pola rekordu wynikowego przypisane po kolei, jeśli dzieje się to dopiero po wszystkich sprawdzeniach;
- decyzja o `(none)` podjęta flagą `bool` ustawianą w pętli imion i nazwisk;
- osobna funkcja sumująca zajęcia albo wypisująca imiona i nazwiska grupy 2, która dostaje wektor przez `const&`.

To nie jedyne poprawne rozwiązanie.

Każdy przypadek z listy kontrolnej to osobne uruchomienie tego programu. Przypadki A–F to przykłady z części A. Pozostałe są poniżej, w kolejności z listy kontrolnej.

<!-- input: workshop_registrations -->
```text
Ewa Maj
2 6
```

<!-- output: workshop_registrations -->
```text
Registrations: 1
Group 1: 0
Group 2: 1
Sessions total: 6
Group 2 participants:
Ewa Maj
```

<!-- input: workshop_registrations -->
```text
Jan Lis
2 4
Ala Nowak
1 2
Jan Lis
2 1
Anna Maria Zielinska
2 6
Piotr Nowak
1 5

```

<!-- output: workshop_registrations -->
```text
Registrations: 5
Group 1: 2
Group 2: 3
Sessions total: 18
Group 2 participants:
Jan Lis
Jan Lis
Anna Maria Zielinska
```

<!-- input: workshop_registrations -->
```text
Ala Nowak
0 2
```

<!-- output: workshop_registrations -->
```text
Invalid registrations
```

<!-- input: workshop_registrations -->
```text
Ala Nowak
-1 2
```

<!-- output: workshop_registrations -->
```text
Invalid registrations
```

<!-- input: workshop_registrations -->
```text
Ala Nowak
1 0
```

<!-- output: workshop_registrations -->
```text
Invalid registrations
```

<!-- input: workshop_registrations -->
```text
Ala Nowak
2 7
```

<!-- output: workshop_registrations -->
```text
Invalid registrations
```

<!-- input: workshop_registrations -->
```text
Ala Nowak
1 -3
```

<!-- output: workshop_registrations -->
```text
Invalid registrations
```

<!-- input: workshop_registrations -->
```text
Ala Nowak
one 2
```

<!-- output: workshop_registrations -->
```text
Input error
```

<!-- input: workshop_registrations -->
```text
Ala Nowak
```

<!-- output: workshop_registrations -->
```text
Input error
```

<!-- input: workshop_registrations -->
```text
Ala Nowak
1
```

<!-- output: workshop_registrations -->
```text
Input error
```

<!-- input: workshop_registrations -->
```text
Ala Nowak
3 four
```

<!-- output: workshop_registrations -->
```text
Input error
```

<!-- input: workshop_registrations -->
```text
Ala Nowak
1 2

Jan Lis
3 4
```

<!-- output: workshop_registrations -->
```text
Registrations: 1
Group 1: 1
Group 2: 0
Sessions total: 2
Group 2 participants:
(none)
```

**Program kontrolny** sprawdza umowę funkcji odczytującej przy odmowie, której w raporcie nie widać, bo po `false` program kończy pracę. Typ i funkcja są takie same jak wyżej. `main` przygotowuje rekord `Old Name` z grupą 2 i pięcioma zajęciami, odczytuje jedno imię i nazwisko, wywołuje funkcję i wypisuje jej wynik oraz stan rekordu. To narzędzie, a nie dodatkowe zadanie: uruchamianie go jest nieobowiązkowe. Możesz w nim podmienić typ i funkcję na własne, jeśli zmienisz też nazwy w `main`.

<!-- example: registration_values_check -->
```cpp
#include <iostream>
#include <string>

struct Registration {
    std::string name;
    int group;
    int sessions;
};

bool read_registration_values(std::istream& input, const std::string& name, Registration& result) {
    int group{0};
    int sessions{0};
    input >> group;
    input >> sessions;

    if (input.fail()) {
        return false;
    }

    if (group != 1 && group != 2) {
        return false;
    }

    if (sessions < 1 || sessions > 6) {
        return false;
    }

    result = Registration{name, group, sessions};
    return true;
}

int main() {
    Registration result{"Old Name", 2, 5};
    std::string name{};
    std::getline(std::cin, name);

    const bool accepted{read_registration_values(std::cin, name, result)};

    if (accepted) {
        std::cout << "Returned: true\n";
    } else {
        std::cout << "Returned: false\n";
    }

    std::cout << "Result: " << result.name << ", group " << result.group << ", sessions " << result.sessions << "\n";
}
```

Poprawne liczby zmieniają rekord:

<!-- input: registration_values_check -->
```text
Ewa Maj
1 6
```

<!-- output: registration_values_check -->
```text
Returned: true
Result: Ewa Maj, group 1, sessions 6
```

Po odmowie rekord zostaje bez zmian: po słowie zamiast pierwszej i zamiast drugiej liczby, po braku drugiej liczby, po niedozwolonej grupie i po niedozwolonej liczbie zajęć. W trzech ostatnich przypadkach pierwsza liczba została odczytana, a mimo to rekord się nie zmienia.

<!-- input: registration_values_check -->
```text
Ewa Maj
one 2
```

<!-- output: registration_values_check -->
```text
Returned: false
Result: Old Name, group 2, sessions 5
```

<!-- input: registration_values_check -->
```text
Ewa Maj
1 four
```

<!-- output: registration_values_check -->
```text
Returned: false
Result: Old Name, group 2, sessions 5
```

<!-- input: registration_values_check -->
```text
Ewa Maj
1
```

<!-- output: registration_values_check -->
```text
Returned: false
Result: Old Name, group 2, sessions 5
```

<!-- input: registration_values_check -->
```text
Ewa Maj
3 4
```

<!-- output: registration_values_check -->
```text
Returned: false
Result: Old Name, group 2, sessions 5
```

<!-- input: registration_values_check -->
```text
Ewa Maj
1 7
```

<!-- output: registration_values_check -->
```text
Returned: false
Result: Old Name, group 2, sessions 5
```

</details>

## Diagnostyka: wyniki i poprawki

<details>
<summary>Diagnostyka A: funkcja licząca kończy się za wcześnie</summary>

Przed poprawką, dla jednego zgłoszenia do grupy 1:

<!-- output: group_count_bug -->
```text
Registrations: 1
Group 1: 1
Group 2: 0
```

- **Ten przypadek maskuje błąd.** Poprawna funkcja wypisałaby to samo. Pętla ma tylko jeden przebieg, więc `return count;` w jej ciele wykonuje się dopiero po sprawdzeniu jedynego zgłoszenia.
- **Pusty wektor też nie ujawnia błędu:** pętla nie wykonuje się ani razu, więc obie wersje dochodzą do `return count;` za pętlą i zwracają 0.
- **Dane, które ujawniają błąd:** kilka zgłoszeń, wśród których pasujące zgłoszenie stoi dalej niż na pierwszej pozycji. Na przykład `Ala Nowak` w grupie 1, `Jan Lis` w grupie 2 i `Maja Kot` w grupie 1. Poprawny wynik to `Group 1: 2` i `Group 2: 1`. Program z błędem wypisuje:

<!-- example: group_count_revealed -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>
#include <vector>

struct Registration {
    std::string name;
    int group;
    int sessions;
};

std::size_t count_group(const std::vector<Registration>& registrations, int group) {
    std::size_t count{0};

    for (const Registration& registration : registrations) {
        if (registration.group == group) {
            ++count;
        }

        return count;
    }

    return count;
}

int main() {
    const std::vector<Registration> registrations{
        {"Ala Nowak", 1, 2},
        {"Jan Lis", 2, 4},
        {"Maja Kot", 1, 1}
    };

    std::cout << "Registrations: " << registrations.size() << "\n";
    std::cout << "Group 1: " << count_group(registrations, 1) << "\n";
    std::cout << "Group 2: " << count_group(registrations, 2) << "\n";
}
```

<!-- output: group_count_revealed -->
```text
Registrations: 3
Group 1: 1
Group 2: 0
```

| Wywołanie | Przebieg 1: `Ala Nowak`, grupa 1 | Dalsze przebiegi | Wynik | Poprawny wynik |
|---|---|---|---|---|
| `count_group(registrations, 1)` | pasuje, `count` = 1, potem `return count;` | nie wykonują się | 1 | 2 |
| `count_group(registrations, 2)` | nie pasuje, `count` = 0, potem `return count;` | nie wykonują się | 0 | 1 |

- **Gdzie jest błąd:** `return count;` stoi w ciele pętli, za `if`. Wykonuje się w pierwszym przebiegu, niezależnie od tego, czy zgłoszenie pasuje.
- **`return` kończy całą funkcję,** a nie jeden przebieg pętli (lekcja 9.4). Po nim pętla nie ma już dalszych przebiegów, a funkcja zwraca wynik po sprawdzeniu tylko pierwszego elementu.
- **Poprawny wynik dla jednego zgłoszenia nic nie dowodzi,** bo przy jednym elemencie pierwszy przebieg jest zarazem ostatnim. Nawet dwa zgłoszenia `Ala Nowak` w grupie 1 i `Jan Lis` w grupie 2 dają poprawne `Group 1: 1`, a błąd widać dopiero w `Group 2: 0`. Ujawnia go tylko pasujące zgłoszenie na dalszej pozycji. Ujawniłyby go też dane z wymagań zadania 1.
- **Różnica wobec lekcji 9.4:** tam funkcja szukała jednego rekordu, więc po znalezieniu zadanie było wykonane, a `return` w pętli był zamierzony. Błędem był `return false;` w ciele pętli, po rekordzie, który nie pasował. Tutaj funkcja liczy wszystkie pasujące zgłoszenia, więc wynik jest znany dopiero po ostatnim elemencie, a w pętli nie powinno być żadnego `return`.
- **Poprawka:** usuń `return count;` z ciała pętli. Zostaje tylko `return count;` za pętlą. Kompilator nie zgłasza tu błędu ani ostrzeżenia, bo to poprawny C++, tylko niezgodny z zadaniem funkcji. Poprawiona funkcja to funkcja z rozwiązania referencyjnego:

<!-- example: group_count_fixed -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>
#include <vector>

struct Registration {
    std::string name;
    int group;
    int sessions;
};

std::size_t count_group(const std::vector<Registration>& registrations, int group) {
    std::size_t count{0};

    for (const Registration& registration : registrations) {
        if (registration.group == group) {
            ++count;
        }
    }

    return count;
}

int main() {
    const std::vector<Registration> registrations{
        {"Ala Nowak", 1, 2},
        {"Jan Lis", 2, 4},
        {"Maja Kot", 1, 1}
    };

    std::cout << "Registrations: " << registrations.size() << "\n";
    std::cout << "Group 1: " << count_group(registrations, 1) << "\n";
    std::cout << "Group 2: " << count_group(registrations, 2) << "\n";
}
```

<!-- output: group_count_fixed -->
```text
Registrations: 3
Group 1: 2
Group 2: 1
```

Teraz `Group 1` i `Group 2` dają razem 3, tyle co `Registrations`. W wersji z błędem dawały 1, choć zgłoszenia są tylko w grupach 1 i 2.

</details>

<details>
<summary>Diagnostyka B: niekompletne zgłoszenie uznane za zakończenie danych</summary>

1. **Ta wersja wypisuje raport z jednym zgłoszeniem:** `Registrations: 1`, `Group 1: 1`, `Group 2: 0`, `Sessions total: 2`, `Group 2 participants:` i `(none)`. **Poprawny wynik** to tylko `Input error`.
2. **Drugie zgłoszenie się rozpoczęło,** bo odczyt imienia i nazwiska `Jan Lis` się udał, a linia nie jest pusta. Od tej chwili program musi dostać obie liczby tego zgłoszenia.
3. **To błąd odczytu,** bo numer grupy się odczytał, ale liczby zajęć już nie: dane się skończyły. Funkcja zwraca `false`, a `std::cin.fail()` daje `true`. Zakończeniem danych byłaby pusta linia albo koniec danych w miejscu imienia i nazwiska, a nie w środku zgłoszenia.
4. **`false` mówi tylko, że nowego zgłoszenia nie ma,** a nie dlaczego. Gałąź `else` ustawia `reading` na `false` tak samo jak pusta linia, więc program myli błąd z zakończeniem. Dla `3 4` ta wersja wypisałaby ten sam raport z jednym zgłoszeniem zamiast `Invalid registrations`.
5. **Raport z jednym zgłoszeniem wyglądałby jak kompletny,** choć dane były błędne. Organizatorzy nie wiedzieliby, że jedno zgłoszenie się nie zapisało.
6. **Zakończenie danych rozpoznaje warunek `std::cin.fail() || name.empty()` przy odczycie imienia i nazwiska,** jeszcze przed wywołaniem funkcji. Po wywołaniu `false` zawsze oznacza błąd zgłoszenia. Gałąź `else` powinna więc wybrać komunikat przez `std::cin.fail()` (`Input error` albo `Invalid registrations`) i zakończyć `main` przez `return 0;`, bez raportu, jak w rozwiązaniu referencyjnym.

</details>

## Odpowiedzi do zadania 3

<details>
<summary>Przykładowe odpowiedzi</summary>

1. Bo to dwa różne zadania. Przy linii imienia i nazwiska rozstrzyga się, czy dane się skończyły, więc tę linię i pętlę obsługuje `main`. Funkcja dostaje już rozpoczęte zgłoszenie i odpowiada tylko za jego liczby, więc jej `true` i `false` mają po jednym znaczeniu.
2. Strumień przez `std::istream&`, a rekord przez `Registration&`. Funkcja ma czytać z istniejącego `std::cin`, a odczyt zmienia strumień. Ma też wypełnić obiekt przygotowany przez `main`. Z `const` nie mogłaby zrobić ani jednego, ani drugiego, a bez `&` pracowałaby na kopii albo w ogóle by się nie skompilowała.
3. Bo umowa mówi, że po `false` rekord jest bez zmian, niezależnie od tego, co zrobi wywołujący. Program kontrolny i inny wywołujący mogą dalej korzystać z rekordu. `return false;` nie cofa wcześniejszego przypisania.
4. Tylko po `true`. Po błędzie w drugim zgłoszeniu w wektorze jest pierwsze zgłoszenie, bo zostało dodane wcześniej. Program wypisuje tylko komunikat, bo raport ma dotyczyć wszystkich danych, a z częścią zgłoszeń wyglądałby jak kompletny.
5. Pusta linia to udany odczyt: `fail()` daje `false`, a `empty()` daje `true`. Nieudany odczyt imienia i nazwiska daje `fail()` równe `true`. Oba kończą dane. Niekompletne zgłoszenie ma niepustą, poprawnie odczytaną linię imienia i nazwiska, a potem brakuje liczby: wtedy `false` zwraca funkcja i to jest błąd.
6. Bo funkcja tylko odczytuje gotowy wektor: `&` usuwa kopię, a `const` gwarantuje, że go nie zmieni. Zmienna pętli z `const&` z tego samego powodu nie kopiuje zgłoszeń i nie może ich zmienić.
7. Bo liczba dopasowań jest znana dopiero po sprawdzeniu ostatniego elementu. Wyszukiwanie z lekcji 9.4 miało znaleźć jeden rekord i mogło skończyć się zaraz po nim. Funkcja licząca kończy się dopiero za pętlą.
8. Liczba zgłoszeń liczy rekordy w wektorze, liczba uczestników grupy liczy rekordy z danym numerem grupy, a suma zajęć dodaje pola `sessions`. Zawsze liczba uczestników grupy 1 i grupy 2 daje razem liczbę zgłoszeń, bo każde zgłoszenie należy do dokładnie jednej grupy. Suma zajęć równa się liczbie zgłoszeń tylko wtedy, gdy każde zgłoszenie ma jedne zajęcia.
9. Bo umowa pozwala, żeby do grupy 2 nikt się nie zapisał: to poprawne dane z pustą listą. W rozwiązaniu referencyjnym `(none)` pojawia się, gdy funkcja licząca zwróci 0 dla grupy 2. Inne poprawne rozwiązanie to flaga ustawiana w pętli imion i nazwisk.
10. Nie. `true` mówi o jednym zgłoszeniu, a funkcja licząca może się mylić, jak w diagnostyce A. Sprawdzam cały raport dla przypadków z tabeli: czy liczby grup dają razem liczbę zgłoszeń i czy lista grupy 2 ma tyle imion i nazwisk, ile podaje `Group 2`.

</details>

## Samoocena

Przy każdym kryterium zaznacz jedną odpowiedź:

| Kryterium | Samodzielnie | Z podpowiedzią | Po zajrzeniu do rozwiązania | Do powtórki |
|---|---|---|---|---|
| Projekt typu zgłoszenia | | | | |
| Funkcja odczytująca: parametry i ich przekazanie | | | | |
| Odczyt przed zasadami, rekord bez zmian po odmowie | | | | |
| Zakończenie danych: pusta linia i koniec danych | | | | |
| Niekompletne zgłoszenie i `Input error` | | | | |
| Niedozwolone wartości i `Invalid registrations` | | | | |
| `push_back` tylko po `true`, bez częściowego raportu | | | | |
| Funkcja licząca: `const&`, cała kolekcja, `std::size_t` | | | | |
| Suma zajęć z elementów wektora | | | | |
| Imiona i nazwiska grupy 2 w kolejności i `(none)` | | | | |
| Pusty import | | | | |
| Tabela przypadków przed uruchomieniem | | | | |
| Diagnostyka A (funkcja licząca kończy się za wcześnie) | | | | |
| Diagnostyka B (niekompletne zgłoszenie jako zakończenie danych) | | | | |
| Wyjaśnienia z zadania 3 | | | | |

Poprawne uruchomienie programu dla przykładów to dopiero część dowodu. Opanowanie Modułu 10 pokazują także tabela przypadków, obie diagnostyki i wyjaśnienia.

Jeśli w kolumnie „Do powtórki” jest coś zaznaczone, wróć do odpowiedniej lekcji:

| Temat | Lekcja |
|---|---|
| rekord z danych wejściowych, najpierw odczyt, potem zasady | [10.1](lesson_01_one_record_from_input.md) |
| imię i nazwisko ze spacjami, dokończenie linii liczbowej | [10.2](lesson_02_names_with_spaces.md) |
| `push_back` kompletnych rekordów, bez częściowego raportu | [10.3](lesson_03_building_a_vector_of_records.md) |
| funkcja odczytująca, `std::istream&`, zakończenie danych | [10.4](lesson_04_reading_function_and_end_of_data.md) |
| funkcja analizująca wektor rekordów, `std::size_t` | [8.4](../module_08_structs/lesson_04_many_records_in_a_vector.md) |
| wszystko albo nic, wynik `bool` | [9.2](../module_09_mutable_references/lesson_02_a_change_only_when_allowed.md) |
| `return` w pętli i za pętlą | [9.4](../module_09_mutable_references/lesson_04_find_a_record_and_change_it.md) |
| pusta linia a nieudany odczyt | [7.4](../module_07_text/lesson_04_successive_lines.md) |

Potem spróbuj zadania jeszcze raz, na przykład dla wypożyczeń w bibliotece szkolnej, w której każde wypożyczenie ma tytuł, dział 1 albo 2 i liczbę dni od 1 do 14, a raport podaje liczbę wypożyczeń w każdym dziale i tytuły z jednego z nich.

---

## Podsumowanie Modułu 10

Po pięciu lekcjach potrafisz:

- odczytywać pola rekordu do zmiennych lokalnych, sprawdzać najpierw odczyt, potem zasady, i dopiero wtedy budować rekord;
- odczytywać nazwy ze spacjami przez `std::getline`, liczby przez `>>` i dokańczać linię liczbową;
- budować wektor rekordów przez `push_back` tylko z kompletnych, sprawdzonych rekordów i przy pierwszym błędzie nie wypisywać częściowego raportu;
- czytać rekordy do pustej linii albo do końca danych i odróżniać zakończenie danych od niekompletnego rekordu;
- pisać funkcję z `std::istream&` i `T&`, która wypełnia rekord wynikowy tylko po sukcesie;
- przekazywać kolekcję zbudowaną z wejścia do funkcji analizującej przez `const&` i budować raport z jej elementów.

## Co dalej

Kolejny moduł kursu jest w przygotowaniu.

**Poprzednia lekcja:** [Lekcja 10.4: Funkcja odczytująca rekord i zakończenie danych](lesson_04_reading_function_and_end_of_data.md) · **Następna lekcja:** w przygotowaniu · [Opis kursu](../../README.md)

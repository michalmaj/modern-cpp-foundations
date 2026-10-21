# Lekcja 3.4: Łączenie warunków (`&&`, `||`, `!`)

**Polski** · [English](lesson_04_combining_conditions.en.md) · [Opis kursu](../../README.md)

> **Moduł 3, lekcja 4** · około 60–75 minut
> **Potrzebujesz:** katalogu `cpp-workspace` i oryginalnego projektu `lesson_05_first_program`, jak dotąd. Debugger nie jest w tej lekcji potrzebny.
> **Wersja pilotażowa.** Programy z tej lekcji sprawdzamy automatycznie na Windowsie, Ubuntu i macOS, także z podanymi danymi wejściowymi.

## Zanim zaczniesz

Ta lekcja zakłada, że po lekcjach 3.1–3.3:

- piszesz `if`, `else` i łańcuchy `else if`, zawsze z klamrami;
- zapisujesz wynik porównania w zmiennej `bool` i używasz jej jako warunku;
- wiesz, że zapisana wartość `bool` nie zmienia się sama, gdy później zmienią się dane;
- sprawdzasz każdą granicę z obu stron.

## Sytuacja

Do tej pory każdy warunek zadawał jedno pytanie: czy liczba jest mniejsza od 5, czy dzień to sobota. Wymagania często łączą jednak kilka pytań: „od 1 do 10”, „w sobotę **lub** w niedzielę”, „**nie** w dzień sprzątania”. Dziś poznasz trzy operatory, które łączą warunki: `&&` („i”), `||` („lub”) i `!` („nie”). Nauczysz się też przekładać wymagania zapisane słowami na czytelne warunki w kodzie.

Po tej lekcji będziesz:

- wyjaśniać znaczenie `&&`, `||` i `!` i dobierać operator do wymagania;
- sprawdzać, czy liczba należy do przedziału;
- wiedzieć, że `||` daje „tak” także wtedy, gdy spełnione są oba warunki;
- zapisywać złożone warunki czytelnie, z nazwanymi zmiennymi `bool` i nawiasami;
- rozumieć, kiedy prawa strona `&&` i `||` nie jest w ogóle obliczana;
- znajdować błąd w połączonym warunku i dobierać przypadki testowe, które go ujawnią.

## 1. Przygotuj projekt

W `cpp-workspace` utwórz katalog `lesson_3_4` i skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program`. Programy z punktów 2–7 wpisujesz w `main.cpp` tego katalogu.

## 2. Liczba w przedziale: `&&`

Program ma sprawdzić, czy liczba należy do przedziału **od 1 do 10 włącznie**. Oba potrzebne porównania już znasz: `number >= 1` i `number <= 10`. Jak zapisać warunek, który jest spełniony tylko wtedy, gdy **oba** porównania dają „tak”?

<!-- example: range_check -->
```cpp
#include <iostream>

int main() {
    int number{0};

    std::cout << "Enter a number:\n";
    std::cin >> number;

    const bool in_range{number >= 1 && number <= 10};

    if (in_range) {
        std::cout << "In range\n";
    } else {
        std::cout << "Out of range\n";
    }
}
```

- **`&&`** to logiczne **„i”**. Całe wyrażenie `number >= 1 && number <= 10` jest prawdziwe (`true`) tylko wtedy, gdy **oba** porównania są prawdziwe. Wystarczy, że jedno jest fałszywe, a całość jest fałszywa.
- `in_range` to zmienna `bool`, która przechowuje wynik całego wyrażenia. `if (in_range)` korzysta z niej jak w lekcji 3.2.
- Operator logiczny niczego nie zmienia: `number` ma po porównaniu tę samą wartość.

W C++ przedziału nie zapisuje się jak w szkole, jednym łańcuchem nierówności z liczbą pośrodku. Trzeba jawnie połączyć **dwa** porównania operatorem `&&`, tak jak wyżej.

**Przewidź**, co wypisze program dla 0, 1, 5, 10 i 11. Zapisz odpowiedzi, a potem uruchom go pięć razy.

<!-- input: range_check -->
```text
0
```

<details>
<summary>Standardowe wyjście dla 0</summary>

<!-- output: range_check -->
```text
Enter a number:
Out of range
```

</details>

<!-- input: range_check -->
```text
1
```

<details>
<summary>Standardowe wyjście dla 1</summary>

<!-- output: range_check -->
```text
Enter a number:
In range
```

</details>

<!-- input: range_check -->
```text
5
```

<details>
<summary>Standardowe wyjście dla 5</summary>

<!-- output: range_check -->
```text
Enter a number:
In range
```

</details>

<!-- input: range_check -->
```text
10
```

<details>
<summary>Standardowe wyjście dla 10</summary>

<!-- output: range_check -->
```text
Enter a number:
In range
```

</details>

<!-- input: range_check -->
```text
11
```

<details>
<summary>Standardowe wyjście dla 11</summary>

<!-- output: range_check -->
```text
Enter a number:
Out of range
```

</details>

0 i 11 to zwykłe, poprawnie odczytane liczby. Po prostu **nie spełniają warunku**: leżą poza zakresem od 1 do 10. Dla 0 fałszywe jest pierwsze porównanie, a dla 11 drugie. W obu przypadkach to wystarcza, żeby całe `&&` było fałszywe.

## 3. Wystarczy jeden warunek: `||`

Zajęcia odbywają się **w sobotę lub w niedzielę**. Dni tygodnia oznaczamy numerami: 1 to poniedziałek, …, 6 to sobota, 7 to niedziela.

<!-- example: weekend_check -->
```cpp
#include <iostream>

int main() {
    int day{0};

    std::cout << "Enter day (1-7):\n";
    std::cin >> day;

    const bool is_weekend{day == 6 || day == 7};

    if (is_weekend) {
        std::cout << "Weekend\n";
    } else {
        std::cout << "Weekday\n";
    }
}
```

**Przewidź** wynik dla dni 5, 6 i 7, a potem sprawdź.

<!-- input: weekend_check -->
```text
5
```

<!-- output: weekend_check -->
```text
Enter day (1-7):
Weekday
```

<!-- input: weekend_check -->
```text
6
```

<!-- output: weekend_check -->
```text
Enter day (1-7):
Weekend
```

<!-- input: weekend_check -->
```text
7
```

<!-- output: weekend_check -->
```text
Enter day (1-7):
Weekend
```

- **`||`** to logiczne **„lub”**. Całe wyrażenie jest prawdziwe, gdy **przynajmniej jeden** warunek jest prawdziwy, a fałszywe tylko wtedy, gdy **oba** są fałszywe.
- `||` nie wybiera „lepszego” warunku i niczego nie zmienia. Odpowiada tylko „tak” albo „nie” dla całości.

**„Lub” obejmuje też „oba naraz”.** W przykładzie z weekendem dzień nie może być jednocześnie 6 i 7, więc tego nie widać. Ten program pokazuje to wprost: wejść można z biletem **lub** będąc na liście gości.

<!-- example: entry_check -->
```cpp
#include <iostream>
#include <string>

int main() {
    std::string ticket_answer{""};
    std::string list_answer{""};

    std::cout << "Do you have a ticket? (yes/no)\n";
    std::cin >> ticket_answer;
    std::cout << "Are you on the guest list? (yes/no)\n";
    std::cin >> list_answer;

    const bool has_ticket{ticket_answer == "yes"};
    const bool on_guest_list{list_answer == "yes"};

    if (has_ticket || on_guest_list) {
        std::cout << "Come in\n";
    } else {
        std::cout << "Sorry, no entry\n";
    }
}
```

**Przewidź** wynik dla czterech kombinacji: bilet i brak na liście, brak biletu i obecność na liście, **i bilet, i lista**, ani biletu, ani listy.

<!-- input: entry_check -->
```text
yes
no
```

<!-- output: entry_check -->
```text
Do you have a ticket? (yes/no)
Are you on the guest list? (yes/no)
Come in
```

<!-- input: entry_check -->
```text
no
yes
```

<!-- output: entry_check -->
```text
Do you have a ticket? (yes/no)
Are you on the guest list? (yes/no)
Come in
```

<!-- input: entry_check -->
```text
yes
yes
```

<details>
<summary>Standardowe wyjście dla „yes” i „yes”</summary>

<!-- output: entry_check -->
```text
Do you have a ticket? (yes/no)
Are you on the guest list? (yes/no)
Come in
```

Oba warunki są prawdziwe, więc `||` daje „tak”. W C++ „lub” nie znaczy „albo jedno, albo drugie, ale nie oba”.

</details>

<!-- input: entry_check -->
```text
no
no
```

<!-- output: entry_check -->
```text
Do you have a ticket? (yes/no)
Are you on the guest list? (yes/no)
Sorry, no entry
```

**`&&` czy `||`?** Porównaj:

| Lewy warunek | Prawy warunek | `lewy && prawy` | `lewy \|\| prawy` |
|---|---|---|---|
| `true` | `true` | `true` | `true` |
| `true` | `false` | `false` | `true` |
| `false` | `true` | `false` | `true` |
| `false` | `false` | `false` | `false` |

**Wybierz operator.** Przepisz tabelę i przy każdym wymaganiu wpisz `&&` albo `||`:

| Wymaganie | Operator |
|---|---|
| Temperatura jest od 18 do 24 stopni. | |
| Dzień to wtorek albo czwartek. | |
| Osoba ma co najmniej 18 lat i bilet. | |
| Odpowiedź to `yes` albo `y`. | |
| Wynik jest od 0 do 100 punktów. | |

Odpowiedzi są w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 4. Zaprzeczenie: `!`

Czasem wymaganie mówi „jeśli **nie**”. Do zaprzeczenia wartości logicznej służy **`!`**, czyli logiczne „nie”:

<!-- example: weekday_notice -->
```cpp
#include <iostream>

int main() {
    int day{0};

    std::cout << "Enter day (1-7):\n";
    std::cin >> day;

    const bool is_weekend{day == 6 || day == 7};

    if (!is_weekend) {
        std::cout << "Not a weekend\n";
    }

    std::cout << "Day checked\n";
}
```

<!-- input: weekday_notice -->
```text
3
```

<!-- output: weekday_notice -->
```text
Enter day (1-7):
Not a weekend
Day checked
```

<!-- input: weekday_notice -->
```text
6
```

<!-- output: weekday_notice -->
```text
Enter day (1-7):
Day checked
```

- `!` odwraca wartość logiczną: `!true` daje `false`, a `!false` daje `true`.
- `!is_weekend` czyta się „nie weekend”. Wynik to **nowa** wartość logiczna, a `is_weekend` się nie zmienia.
- **`!` to nie `!=`.** `!=` z lekcji 3.2 porównuje dwie wartości („czy są różne?”). `!` stoi przed **jedną** wartością logiczną i ją odwraca.
- `if (!warunek)` stosuj tam, gdzie wymaganie naprawdę brzmi „jeśli nie …”. Unikaj podwójnych zaprzeczeń: zwykle da się je zapisać prościej.

## 5. Czytelne warunki

Basen jest otwarty, gdy temperatura wody wynosi **od 24 do 28 stopni** i **nie** jest poniedziałek, bo w poniedziałki basen jest sprzątany. To wymaganie łączy kilka pytań. Zamiast pisać je w jednym długim warunku, nadaj każdej części nazwę:

<!-- example: pool_open -->
```cpp
#include <iostream>

int main() {
    int water_temperature_c{0};
    int day{0};

    std::cout << "Enter water temperature:\n";
    std::cin >> water_temperature_c;
    std::cout << "Enter day (1-7):\n";
    std::cin >> day;

    const bool water_ok{water_temperature_c >= 24 && water_temperature_c <= 28};
    const bool is_cleaning_day{day == 1};

    if (water_ok && !is_cleaning_day) {
        std::cout << "Pool open\n";
    } else {
        std::cout << "Pool closed\n";
    }
}
```

<!-- input: pool_open -->
```text
26
3
```

<!-- output: pool_open -->
```text
Enter water temperature:
Enter day (1-7):
Pool open
```

<!-- input: pool_open -->
```text
26
1
```

<!-- output: pool_open -->
```text
Enter water temperature:
Enter day (1-7):
Pool closed
```

<!-- input: pool_open -->
```text
30
3
```

<!-- output: pool_open -->
```text
Enter water temperature:
Enter day (1-7):
Pool closed
```

- `water_ok` i `is_cleaning_day` to **nazwy części wymagania**. Warunek `water_ok && !is_cleaning_day` czyta się prawie jak zdanie: „woda w porządku i nie dzień sprzątania”.
- Każda z tych zmiennych **przechowuje wynik** obliczony w chwili inicjalizacji, jak w lekcji 3.2. Gdyby później zmieniła się temperatura albo dzień, `water_ok` i `is_cleaning_day` same się nie przeliczą.

**Nawiasy.** Gdy warunek łączy kilka grup, pokaż, co do czego należy, na jeden z dwóch sposobów: nazwanymi zmiennymi `bool`, jak wyżej, albo nawiasami, na przykład `(age >= 18 && has_ticket) || on_guest_list`. W C++ `&&` ma pierwszeństwo przed `||`, czyli łączy się najpierw, podobnie jak mnożenie przed dodawaniem w lekcji 2.4. Nie polegaj jednak na tej regule w zapisie: gdy w jednym warunku są `&&` i `||`, zawsze dopisz nawiasy, żeby grupowanie było widać od razu.

## 6. Krótkie obliczanie

`&&` i `||` obliczają warunki **od lewej** i potrafią skończyć wcześniej:

- **`&&`:** najpierw obliczany jest lewy warunek. Jeśli jest **fałszywy**, wynik całości jest już znany (`false`), więc prawy warunek **nie jest obliczany**.
- **`||`:** najpierw obliczany jest lewy warunek. Jeśli jest **prawdziwy**, wynik całości jest już znany (`true`), więc prawy warunek **nie jest obliczany**.

To **krótkie obliczanie** (*short-circuit evaluation*): obliczanie kończy się, gdy tylko wynik jest pewny. Prawa strona jest obliczana tylko wtedy, gdy jest potrzebna do ustalenia wyniku.

**Sprawdź się.** Przy każdym wierszu odpowiedz: czy prawy warunek musi zostać obliczony?

| Wyrażenie | Wartość | Czy prawy warunek jest obliczany? |
|---|---|---|
| `number >= 1 && number <= 10` | `number` to 0 | |
| `number >= 1 && number <= 10` | `number` to 5 | |
| `day == 6 \|\| day == 7` | `day` to 6 | |
| `day == 6 \|\| day == 7` | `day` to 3 | |

Odpowiedzi są w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

Z samego wyniku `true` albo `false` nie da się odczytać, czy obliczono oba warunki. Dla `day` równego 6 wyrażenie `day == 6 || day == 7` daje `true`, choć porównanie `day == 7` w ogóle się nie wykonało. W następnej lekcji ta reguła przyda się w praktyce: pozwoli bezpiecznie sprawdzić wartość, zanim program jej użyje.

## 7. Znajdź błąd: zły dzień

Wymaganie: program wypisuje `Weekend` w **sobotę lub niedzielę** (dni 6 i 7), a w pozostałe dni `Weekday`. Ten program buduje się i działa, ale nie spełnia wymagania:

<!-- example: weekend_bug -->
```cpp
#include <iostream>

int main() {
    int day{0};

    std::cout << "Enter day (1-7):\n";
    std::cin >> day;

    const bool is_weekend{day == 5 || day == 6};

    if (is_weekend) {
        std::cout << "Weekend\n";
    } else {
        std::cout << "Weekday\n";
    }
}
```

1. Przeczytaj wymaganie i **przewidź**, co program **powinien** wypisać dla dni 5, 6 i 7.
2. Zanim uruchomisz program, zastanów się: który z tych dni ujawni błąd? Czy wystarczyłoby sprawdzić tylko sobotę?
3. Uruchom program dla 5, 6 i 7.
4. Znajdź niewłaściwą część warunku.
5. Popraw program.
6. Sprawdź ponownie wszystkie trzy dni.

Wyniki przed poprawką i poprawiony program są w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 8. Misja: weekendowe warsztaty

Warsztaty są przeznaczone dla osób w wieku **od 12 do 17 lat włącznie** i odbywają się wyłącznie w **sobotę** (dzień 6) **lub w niedzielę** (dzień 7). Program pyta o wiek i numer dnia tygodnia, a potem wypisuje:

- `Entry allowed`, jeśli spełnione są **wszystkie** wymagania;
- `Entry denied` w pozostałych przypadkach.

W `cpp-workspace` utwórz katalog `weekend_workshop`, skopiuj do niego `CMakeLists.txt` z oryginalnego `lesson_05_first_program`, utwórz pusty `main.cpp` i napisz program samodzielnie. Zakładamy, że odczyt się udaje, a numer dnia jest jedną z liczb od 1 do 7.

Dla wieku 15 i dnia 6 standardowe wyjście ma być takie:

<!-- input: weekend_workshop -->
```text
15
6
```

<!-- output: weekend_workshop -->
```text
Enter age:
Enter day (1-7):
Entry allowed
```

**Zanim napiszesz program**, przygotuj tabelę przewidywań: wybierz kombinacje wieku i dnia, które sprawdzą obie granice wieku z obu stron, dzień dozwolony i niedozwolony, oba dni weekendu oraz przypadki, w których spełniony jest tylko jeden z dwóch warunków. Przy każdej kombinacji zapisz oczekiwany wynik.

### Kryterium sukcesu

- Program buduje się jako C++20 i dla każdej kombinacji wypisuje prośby i dokładnie jedną linijkę: `Entry allowed` albo `Entry denied`, zgodnie z wymaganiami.
- Wiek i dzień to zmienne `int` z wartościami początkowymi, odczytane przez `std::cin`.
- Granice wieku sprawdza `&&`, a dni weekendu `||`.
- Przynajmniej jedna część wymagania jest zapisana w nazwanej zmiennej `bool`, a decyzję podejmuje `if`/`else` z klamrami.
- Tabela przewidywań powstała przed uruchomieniem programu.
- Umiesz wyjaśnić dla każdej kombinacji, dlaczego została przyjęta albo odrzucona.

Gdy wynik się zgadza, możesz zapisać projekt w Gicie, jak w lekcji 1.5.

<details>
<summary>Podpowiedź 1</summary>

Wymaganie ma dwie części: wiek i dzień. Każdą z nich zapisz jako osobną zmienną `bool`. Która część potrzebuje „i”, a która „lub”?

</details>

<details>
<summary>Podpowiedź 2</summary>

Wejście jest dozwolone, gdy spełnione są obie części naraz. Jakim operatorem połączysz dwie zmienne `bool` w warunku `if`?

</details>

<details>
<summary>Pełna lista przypadków kontrolnych: otwórz po własnej próbie</summary>

| Wiek | Dzień | Wynik | Co sprawdza |
|---|---|---|---|
| 11 | 6 | `Entry denied` | wiek tuż pod zakresem |
| 12 | 6 | `Entry allowed` | dolna granica wieku |
| 17 | 7 | `Entry allowed` | górna granica wieku, niedziela |
| 18 | 7 | `Entry denied` | wiek tuż nad zakresem |
| 15 | 5 | `Entry denied` | dobry wiek, dzień spoza weekendu |
| 15 | 6 | `Entry allowed` | sobota |
| 15 | 7 | `Entry allowed` | niedziela |
| 12 | 5 | `Entry denied` | dobry wiek na granicy, zły dzień |

Kombinacja 15 i 6 jest sprawdzona wyżej, przy treści misji.

<!-- input: weekend_workshop -->
```text
11
6
```

<!-- output: weekend_workshop -->
```text
Enter age:
Enter day (1-7):
Entry denied
```

<!-- input: weekend_workshop -->
```text
12
6
```

<!-- output: weekend_workshop -->
```text
Enter age:
Enter day (1-7):
Entry allowed
```

<!-- input: weekend_workshop -->
```text
17
7
```

<!-- output: weekend_workshop -->
```text
Enter age:
Enter day (1-7):
Entry allowed
```

<!-- input: weekend_workshop -->
```text
18
7
```

<!-- output: weekend_workshop -->
```text
Enter age:
Enter day (1-7):
Entry denied
```

<!-- input: weekend_workshop -->
```text
15
5
```

<!-- output: weekend_workshop -->
```text
Enter age:
Enter day (1-7):
Entry denied
```

<!-- input: weekend_workshop -->
```text
15
7
```

<!-- output: weekend_workshop -->
```text
Enter age:
Enter day (1-7):
Entry allowed
```

<!-- input: weekend_workshop -->
```text
12
5
```

<!-- output: weekend_workshop -->
```text
Enter age:
Enter day (1-7):
Entry denied
```

</details>

### Wariant: podpowiedź o terminie

Gdy dzień **nie** jest dniem weekendu, program ma dodatkowo, po linijce z wynikiem, wypisać `Workshops run only at the weekend`. Dla pozostałych dni nic się nie zmienia. Dopisz to samodzielnie, korzystając z `!`, i sprawdź dni 5 i 6.

<details>
<summary>Przypadki wariantu: otwórz po własnej próbie</summary>

<!-- input: weekend_workshop_variant -->
```text
15
5
```

<!-- output: weekend_workshop_variant -->
```text
Enter age:
Enter day (1-7):
Entry denied
Workshops run only at the weekend
```

<!-- input: weekend_workshop_variant -->
```text
11
6
```

<!-- output: weekend_workshop_variant -->
```text
Enter age:
Enter day (1-7):
Entry denied
```

<!-- input: weekend_workshop_variant -->
```text
15
6
```

<!-- output: weekend_workshop_variant -->
```text
Enter age:
Enter day (1-7):
Entry allowed
```

</details>

Przykładowe rozwiązania są w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 9. Gdy coś pójdzie inaczej

| Co widzisz | Co to znaczy | Co zrobić |
|---|---|---|
| Wartości z przedziału są odrzucane albo spoza niego przyjmowane | Pomylono `&&` z `\|\|` w warunku przedziału. | Przedział to „co najmniej dolna granica **i** co najwyżej górna”: `&&`. |
| Warunek z „lub” nigdy nie jest spełniony | Zamiast `\|\|` użyto `&&`. Dzień nie może być jednocześnie 6 i 7. | Gdy wystarczy jeden warunek, użyj `\|\|`. |
| Działa dla wartości ze środka, ale źle na granicy | Granica jest przesunięta albo użyto `<` zamiast `<=`. | Sprawdź obie granice z obu stron. |
| Błąd kompilacji przy `&` albo `\|` | Operatory logiczne zapisuje się dwoma znakami. | Użyj `&&` i `\|\|`. |
| Pomylono `!` z `!=` | `!` odwraca jedną wartość logiczną, a `!=` porównuje dwie wartości. | Zaprzeczenie warunku to `!warunek`, a porównanie to `a != b`. |
| Trudno przeczytać długi warunek | W jednym wyrażeniu jest zbyt wiele części. | Nazwij części zmiennymi `bool` albo dopisz nawiasy. |

## 10. Wyjaśnij

Odpowiedz własnymi słowami, najlepiej na piśmie. Dopiero potem porównaj z przykładową odpowiedzią.

**1.** Kiedy wyrażenie z `&&` jest prawdziwe, a kiedy wyrażenie z `||`?

<details>
<summary>Przykładowa odpowiedź</summary>

`&&` jest prawdziwe, gdy oba warunki są prawdziwe. `||` jest prawdziwe, gdy prawdziwy jest przynajmniej jeden warunek, także wtedy, gdy oba.

</details>

**2.** Jak w C++ sprawdzić, czy `number` należy do przedziału od 1 do 10 włącznie?

<details>
<summary>Przykładowa odpowiedź</summary>

Dwoma porównaniami połączonymi przez `&&`: `number >= 1 && number <= 10`.

</details>

**3.** Czym różni się `!is_weekend` od `day != 6`?

<details>
<summary>Przykładowa odpowiedź</summary>

`!is_weekend` odwraca jedną wartość logiczną: daje `true`, gdy `is_weekend` jest `false`. `day != 6` porównuje dwie wartości i daje `true`, gdy `day` jest różne od 6.

</details>

**4.** Dlaczego dla `day` równego 6 w wyrażeniu `day == 6 || day == 7` porównanie `day == 7` nie jest obliczane?

<details>
<summary>Przykładowa odpowiedź</summary>

Bo lewy warunek, `day == 6`, jest prawdziwy, a `||` z jednym prawdziwym warunkiem jest już prawdziwe. Wynik jest znany, więc prawej strony nie trzeba obliczać.

</details>

**5.** Dlaczego w misji kombinacja 15 i 5 jest odrzucana, choć wiek jest odpowiedni?

<details>
<summary>Przykładowa odpowiedź</summary>

Bo wejście wymaga spełnienia obu części naraz (`&&`): wiek jest w zakresie, ale dzień 5 nie jest ani sobotą, ani niedzielą, więc druga część jest fałszywa.

</details>

## Podsumowanie

- **`&&`** („i”) jest prawdziwe, gdy oba warunki są prawdziwe. Przedział zapisujesz jako dwa porównania połączone przez `&&`, na przykład `number >= 1 && number <= 10`.
- **`||`** („lub”) jest prawdziwe, gdy prawdziwy jest przynajmniej jeden warunek, także gdy oba.
- **`!`** („nie”) odwraca jedną wartość logiczną. To nie jest `!=`.
- Złożone warunki zapisuj czytelnie: części wymagania nazywaj zmiennymi `bool`, a przy mieszaniu `&&` i `||` dopisuj nawiasy.
- **Krótkie obliczanie:** `&&` nie oblicza prawej strony, gdy lewa jest fałszywa, a `||`, gdy lewa jest prawdziwa.
- Wartość, która nie spełnia warunku, to zwykle poprawnie odczytana dana spoza zakresu. Sprawdzaj obie granice i każdą część połączonego warunku osobno.

## Co dalej

Twoje programy łączą już kilka warunków. W lekcji 3.5 użyjesz tej umiejętności, żeby **sprawdzać dane, zanim program ich użyje**, na przykład żeby nigdy nie dzielić przez zero. **Lekcja 3.5 jest w przygotowaniu.**

---

## Przykładowe rozwiązania

Zajrzyj tutaj **po własnej próbie**. Twoje nazwy mogą się różnić, jeśli standardowe wyjście jest takie, jak wymagane.

<details>
<summary>Punkt 3: wybierz operator</summary>

| Wymaganie | Operator |
|---|---|
| Temperatura jest od 18 do 24 stopni. | `&&` |
| Dzień to wtorek albo czwartek. | `\|\|` |
| Osoba ma co najmniej 18 lat i bilet. | `&&` |
| Odpowiedź to `yes` albo `y`. | `\|\|` |
| Wynik jest od 0 do 100 punktów. | `&&` |

</details>

<details>
<summary>Punkt 6: krótkie obliczanie</summary>

| Wyrażenie | Wartość | Czy prawy warunek jest obliczany? |
|---|---|---|
| `number >= 1 && number <= 10` | `number` to 0 | nie: lewy jest fałszywy, więc całość jest fałszywa |
| `number >= 1 && number <= 10` | `number` to 5 | tak: lewy jest prawdziwy, wynik zależy od prawego |
| `day == 6 \|\| day == 7` | `day` to 6 | nie: lewy jest prawdziwy, więc całość jest prawdziwa |
| `day == 6 \|\| day == 7` | `day` to 3 | tak: lewy jest fałszywy, wynik zależy od prawego |

</details>

<details>
<summary>Punkt 7: wyniki przed poprawką i poprawiony program</summary>

Przed poprawką, dla dni 5, 6 i 7:

<!-- input: weekend_bug -->
```text
5
```

<!-- output: weekend_bug -->
```text
Enter day (1-7):
Weekend
```

<!-- input: weekend_bug -->
```text
6
```

<!-- output: weekend_bug -->
```text
Enter day (1-7):
Weekend
```

<!-- input: weekend_bug -->
```text
7
```

<!-- output: weekend_bug -->
```text
Enter day (1-7):
Weekday
```

Piątek (5) jest uznany za weekend, a niedziela (7) za dzień powszedni. Sobota (6) daje poprawny wynik, więc test samej soboty nie wykryłby błędu: trzeba sprawdzić każdy z dni, o które pyta wymaganie, i dzień tuż obok. Warunek powinien sprawdzać 6 i 7: `day == 6 || day == 7`. Poprawiony program to program z punktu 3.

</details>

<details>
<summary>Punkt 8: misja, weekendowe warsztaty</summary>

<!-- example: weekend_workshop -->
```cpp
#include <iostream>

int main() {
    int age{0};
    int day{0};

    std::cout << "Enter age:\n";
    std::cin >> age;
    std::cout << "Enter day (1-7):\n";
    std::cin >> day;

    const bool age_allowed{age >= 12 && age <= 17};
    const bool is_weekend{day == 6 || day == 7};

    if (age_allowed && is_weekend) {
        std::cout << "Entry allowed\n";
    } else {
        std::cout << "Entry denied\n";
    }
}
```

- `age_allowed` to przedział wieku: oba porównania muszą być prawdziwe, więc `&&`.
- `is_weekend` to sobota lub niedziela: wystarczy jeden z dwóch warunków, więc `||`.
- Wejście wymaga obu części naraz, więc w `if` stoi `age_allowed && is_weekend`. Nazwy sprawiają, że warunek czyta się jak wymaganie.

</details>

<details>
<summary>Punkt 8: wariant z podpowiedzią o terminie</summary>

<!-- example: weekend_workshop_variant -->
```cpp
#include <iostream>

int main() {
    int age{0};
    int day{0};

    std::cout << "Enter age:\n";
    std::cin >> age;
    std::cout << "Enter day (1-7):\n";
    std::cin >> day;

    const bool age_allowed{age >= 12 && age <= 17};
    const bool is_weekend{day == 6 || day == 7};

    if (age_allowed && is_weekend) {
        std::cout << "Entry allowed\n";
    } else {
        std::cout << "Entry denied\n";
    }

    if (!is_weekend) {
        std::cout << "Workshops run only at the weekend\n";
    }
}
```

Druga decyzja jest osobna, jak w lekcji 3.2: `!is_weekend` jest prawdziwe dla każdego dnia spoza weekendu, niezależnie od wieku.

</details>

**Poprzednia lekcja:** [Lekcja 3.3: Wybór spośród wielu możliwości (`else if`)](lesson_03_many_possibilities.md) · **Następna lekcja:** w przygotowaniu · [Opis kursu](../../README.md)

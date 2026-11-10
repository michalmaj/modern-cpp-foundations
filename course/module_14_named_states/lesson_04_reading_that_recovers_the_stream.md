# Lekcja 14.4: Spróbuj jeszcze raz: odczyt, który odzyskuje strumień

**Polski** · [English](lesson_04_reading_that_recovers_the_stream.en.md) · [Opis kursu](../../README.md)

> **Moduł 14, lekcja 4** · około 95–120 minut, w dwóch podejściach: punkty 1–5 to mechanizm odczytu i odzyskiwania, punkty 6–10 to testy sekwencji i misja
> **Potrzebujesz:** katalogu `cpp-workspace` i oryginalnego projektu `lesson_05_first_program`, jak dotąd. Debugger nie jest w tej lekcji potrzebny.
> **Wersja pilotażowa.** Programy z tej lekcji sprawdzamy automatycznie na Windowsie, Ubuntu i macOS, także z podanymi danymi wejściowymi i razem z ich kodem zakończenia. Wpisywanie danych w oknie **Run** CLiona opisujemy bez ręcznego sprawdzenia na każdym systemie.

## Zanim zaczniesz

Ta lekcja zakłada, że:

- wiesz z lekcji 4.6, że po nieudanym odczycie są dwie przeszkody: stan błędu strumienia i tekst, który został w wejściu; znasz `clear()`, odrzucanie reszty linijki przez `std::getline`, `eof()` i kolejność „najpierw sukces odczytu, potem koniec danych”;
- piszesz funkcje odczytu z parametrem `std::istream&`, które czytają do zmiennych lokalnych, a wynik przypisują dopiero po sprawdzeniach (lekcja 10.4);
- tworzysz w testach strumień z tekstu przez `std::istringstream` i dajesz każdemu niezależnemu przypadkowi nowy strumień (lekcja 13.3);
- zwracasz z funkcji nazwany wynik typu `enum class`, obsługujesz każdy wynik instrukcją `switch` i sprawdzasz w testach osobno wynik i stan danych (lekcje 14.1–14.3).

## Sytuacja

Automat z biletami pyta, ile biletów ktoś chce: od 1 do 6. Ludzie się mylą. Ktoś wpisze `abc`, ktoś `9`, ktoś `3 tickets`, a ktoś naciśnie Enter, nie wpisując niczego. Program ma powiedzieć, co jest nie tak, pozwolić spróbować jeszcze raz i zakończyć się sam, gdy danych już nie ma. To nie jest prawdziwy system sprzedaży: na tym automacie ćwiczysz odczyt.

W lekcji 4.6 taki odczyt stał w pętli w `main`. Tutaj trafi do funkcji, która za każdym razem zwraca nazwany wynik i sama przygotowuje strumień na następną próbę.

Odpowiesz na pytanie: **jak napisać funkcję odczytu, która po błędnym wpisie pozwala spróbować jeszcze raz, nie gubi ostatniej liczby i nie zapętla się, gdy dane się skończą?**

Po tej lekcji będziesz:

- rozróżniać cztery wyniki odczytu: `accepted`, `out_of_range`, `invalid_input` i `end_of_input`;
- wyjaśniać, co naprawia `clear()`, a co usuwa `ignore`, i dlaczego po nieudanym odczycie potrzebne są obie operacje;
- rozpoznawać koniec danych, zanim spróbujesz odczytać następną liczbę, także gdy ostatnia liczba nie ma znaku końca wiersza;
- czytać do zmiennej lokalnej i nie zmieniać parametru wynikowego przy odmowie;
- obsługiwać wyniki instrukcją `switch` i kończyć pętlę po `end_of_input`;
- testować całe sekwencje odczytów na jednym strumieniu.

## 1. Dwie przeszkody po `abc`

Strumień zawiera trzy wiersze:

| Wiersz | Treść |
|---|---|
| 1 | `2` |
| 2 | `abc` |
| 3 | `5` |

Pierwszy odczyt liczby daje 2, a drugi trafia na `abc` i się nie udaje. Co zrobić, żeby trzeci odczyt dał 5? Program poniżej sprawdza to na trzech strumieniach z tym samym tekstem, `"2\nabc\n5\n"`. Funkcja `try_read` odczytuje jedną liczbę i wypisuje, co się stało. Strumień A po błędzie zostaje bez zmian, w strumieniu B program wywołuje tylko `clear()`, a w strumieniu C `clear()` i `ignore`.

<!-- example: recovery_steps -->
```cpp
#include <iostream>
#include <limits>
#include <sstream>
#include <string>

void try_read(std::istream& input, const std::string& label) {
    int number{0};
    input >> number;

    if (input.fail()) {
        std::cout << label << ": read failed\n";
    } else {
        std::cout << label << ": read " << number << "\n";
    }
}

int main() {
    std::istringstream input_a{"2\nabc\n5\n"};
    try_read(input_a, "A1");
    try_read(input_a, "A2");
    try_read(input_a, "A3");

    std::istringstream input_b{"2\nabc\n5\n"};
    try_read(input_b, "B1");
    try_read(input_b, "B2");
    input_b.clear();
    try_read(input_b, "B3");

    std::istringstream input_c{"2\nabc\n5\n"};
    try_read(input_c, "C1");
    try_read(input_c, "C2");
    input_c.clear();
    input_c.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
    try_read(input_c, "C3");
}
```

Ten program możesz uruchomić, ale nie musisz: wystarczy przewidzieć wynik i porównać go z wyjściem poniżej. Jeśli chcesz go uruchomić, w `cpp-workspace` utwórz katalog `lesson_14_4`, skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program` i zastąp zawartość `main.cpp` programem powyżej. Programy z punktów 1–7 to programy jednoplikowe i wszystkie mogą powstawać w tym katalogu, po kolei.

**Przewidź** wyniki A3, B3 i C3, zanim otworzysz wyjście.

<details>
<summary>Standardowe wyjście</summary>

<!-- output: recovery_steps -->
```text
A1: read 2
A2: read failed
A3: read failed
B1: read 2
B2: read failed
B3: read failed
C1: read 2
C2: read failed
C3: read 5
```

</details>

- **A3: odczyt się nie udaje,** bo strumień jest w stanie błędu. Dopóki ten stan trwa, każdy kolejny odczyt od razu się nie udaje, jak w lekcji 4.6. Do `5` program nie dochodzi.
- **B3: nadal się nie udaje.** `clear()` zdjęło znacznik błędu, ale nie usunęło żadnego znaku. Odczyt znowu trafia na to samo `abc`.
- **C3: odczyt daje 5.** `clear()` przywróciło zwykły stan, a `ignore` zabrało z wejścia `abc` razem z końcem wiersza. Następny odczyt zaczyna się od wiersza z `5`.

| Krok | Stan strumienia | Co czeka w wejściu |
|---|---|---|
| po nieudanym odczycie `abc` | błąd: `fail()` daje `true` | `abc`, koniec wiersza, potem `5` |
| po `clear()` | zwykły: `fail()` daje `false` | **nadal** `abc`, koniec wiersza, potem `5` |
| po `ignore` | zwykły | `5` i koniec wiersza |

**`clear()` naprawia stan, a `ignore` usuwa znaki.** Po nieudanym odczycie potrzebne są obie operacje, w tej kolejności.

## 2. `ignore`: odrzucenie reszty wiersza

W programie z punktu 1 odzyskanie strumienia to dwie linijki:

<!-- fragment -->
```cpp
input_c.clear();
input_c.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
```

W lekcji 4.6 resztę linijki odrzucało `std::getline` do zmiennej pomocniczej:

<!-- fragment -->
```cpp
std::cin.clear();

std::string discarded_line{""};
std::getline(std::cin, discarded_line);
```

Lekcja 4.6 zapowiadała, że istnieją też inne sposoby odrzucania danych z wejścia. `ignore` to jeden z nich: funkcja składowa strumienia, która zabiera znaki z wejścia i od razu je wyrzuca. Nie potrzebuje zmiennej, do której trafiłby tekst.

| Część | Znaczenie |
|---|---|
| `input_c.ignore(…)` | zabierz znaki ze strumienia `input_c` i wyrzuć je |
| `std::numeric_limits<std::streamsize>::max()` | największa wartość typu `std::streamsize`, którego biblioteka używa do liczenia znaków; dla `ignore` ta jedna wartość oznacza: **bez limitu liczby znaków** |
| `'\n'` | zatrzymaj się na końcu wiersza; znak końca wiersza też zostaje zabrany |

Gdy dane skończą się wcześniej niż wiersz, `ignore` zatrzymuje się na ich końcu.

Całe wyrażenie czytaj jako jedno polecenie: **odrzuć pozostałe znaki aż do końca wiersza albo do końca danych.** `std::numeric_limits` wymaga `#include <limits>`. Program może się zbudować i bez tego dołączenia, bo czasem dołączają je inne nagłówki, ale nie wolno na tym polegać.

**Najpierw `clear()`, potem `ignore`.** Na strumieniu w stanie błędu `ignore` niczego nie robi, tak jak `getline` w lekcji 4.6. W punkcie 7 zobaczysz, co się dzieje, gdy zabraknie `clear()`.

`getline` i `ignore` mają różne zastosowania. `getline` odczytuje tekst do zmiennej i przydaje się, gdy ten tekst jest potrzebny, na przykład gdy program czyta całe wiersze, jak w lekcji 12.3. `ignore` tylko wyrzuca znaki. Wcześniejsze programy kursu nie muszą niczego zmieniać: odrzucanie przez `getline` nadal w nich działa.

<details>
<summary>Dla dociekliwych: <code>ignore()</code> bez argumentów, stała liczba znaków i różnica względem <code>getline</code></summary>

| Wywołanie | Co robi | Skutek po nieudanym odczycie `abc` |
|---|---|---|
| `input.ignore()` | zabiera **jeden** znak | zostaje `bc`: kolejne próby trafiają na `b`, potem na `c`, więc z jednego wpisu robią się trzy nieudane odczyty |
| `input.ignore(1000, '\n')` | zabiera najwyżej 1000 znaków | wystarczy dla krótkich wierszy, ale z wiersza dłuższego niż 1000 znaków reszta trafi do następnej próby |
| `input.ignore(std::numeric_limits<std::streamsize>::max(), '\n')` | zabiera wszystko do końca wiersza, bez limitu | cały wiersz z `abc` znika |

**`getline` i `ignore` nie są wymienne w każdej sytuacji.** W tej lekcji zabierają te same znaki, ale `getline` zapisuje je w zmiennej typu `std::string`. Różnią się też stanem strumienia na samym końcu danych: gdy strumień jest w zwykłym stanie, ale nie ma już żadnego znaku do zabrania, `getline` zgłasza nieudany odczyt (`fail()` daje `true`), a `ignore` tylko dochodzi do końca danych (`eof()` daje `true`).

</details>

## 3. Koniec danych przed odczytem liczby

Funkcja odczytu będzie wywoływana wiele razy, aż dane się skończą. Za każdym razem musi więc najpierw ustalić, czy jest jeszcze jakiś wpis. Służą do tego dwie linijki:

<!-- fragment -->
```cpp
input >> std::ws;

if (input.eof()) {
    return ReadResult::end_of_input;
}
```

- **`input >> std::ws;`** pomija **białe znaki**: spacje, tabulatory i znaki końca wiersza. Pomija więc także puste wiersze i wiersze z samymi spacjami. Zatrzymuje się na pierwszym znaku, który nie jest białym znakiem, albo na końcu danych. Niczego poza białymi znakami nie usuwa.
- **`eof()` po `std::ws`** odpowiada na pytanie: czy za białymi znakami coś jeszcze jest? Jeśli nie, nie ma kolejnego wpisu i funkcja zwraca `end_of_input`, zanim spróbuje odczytać liczbę.

**Dlaczego nie sprawdzić `eof()` po odczycie liczby?** Lekcja 4.6 pokazała, że udany odczyt ostatniej liczby może dojść do końca danych. Gdy dane kończą się na `4` bez znaku końca wiersza, `>>` odczytuje 4, a `eof()` daje już `true`. To nie jest błąd. Po odczycie liczby `eof()` nie mówi więc, czy odczyt się udał. Funkcja pyta o koniec danych przed odczytem, a po odczycie sprawdza tylko, czy się udał.

Kolejne wywołania funkcji z tej lekcji na jednym strumieniu, z zakresem 1–6:

| Dane | Wyniki kolejnych wywołań |
|---|---|
| `""` | `end_of_input` |
| `"4"` | `accepted` (4), `end_of_input` |
| `"4\n"` | `accepted` (4), `end_of_input` |
| `"abc"` | `invalid_input`, `end_of_input` |
| `"abc\n"` | `invalid_input`, `end_of_input` |
| `"4\n5"` | `accepted` (4), `accepted` (5), `end_of_input` |

- **Ostatnie `4` bez znaku końca wiersza** jest przyjęte. Dopiero następne wywołanie nie znajduje już wpisu.
- **Ostatnie `abc` bez znaku końca wiersza** nie znika: funkcja zgłasza `invalid_input`. Odczyt liczby zatrzymuje się na `a`, więc nie dochodzi do końca danych. Dopiero odrzucenie reszty wiersza zabiera `abc` i dochodzi do końca. Następne wywołanie daje `end_of_input`.
- **Każde kolejne wywołanie po końcu danych** też daje `end_of_input`. Funkcja nie wywołuje wtedy `clear()` i nie ma czego odzyskiwać.

**Pomijanie białych znaków to nie odrzucanie reszty wiersza:**

| Operacja | Co usuwa | Kiedy |
|---|---|---|
| `input >> std::ws` | białe znaki przed wpisem, także puste wiersze | na początku każdej próby |
| odrzucenie reszty wiersza przez `ignore` | wszystkie znaki do końca bieżącego wiersza, także błędny tekst | po każdej próbie, która znalazła wpis |

**Awaria źródła danych to nie koniec danych.** Funkcja z tej lekcji zakłada sprawne źródło: tekst w pamięci, plik albo klawiaturę, z których dane da się czytać zwykłymi operacjami strumienia. `input.bad()` daje `true`, gdy zawiodło samo źródło, a nie wpis. W programach kursu to się nie zdarza. Gdyby jednak się zdarzyło, funkcja nie próbuje odzyskiwać strumienia: zwraca `end_of_input` tylko jako sygnał, że dalszy odczyt jest niemożliwy, i niczego nie zmienia. Nie oznacza to, że dane się skończyły. Program, który musi odróżnić te dwie sytuacje, po `end_of_input` sprawdza `input.bad()`.

<details>
<summary>Dla dociekliwych: dlaczego kolejność z lekcji 4.6 tu nie wystarcza</summary>

W lekcji 4.6 program sprawdzał najpierw, czy odczyt się udał, a dopiero po nieudanym odczycie `eof()`. W funkcji, która jest wywoływana aż do końca danych, to za mało.

Nieudany odczyt, który doszedł do końca danych, ustawia jednocześnie `fail()` i `eof()`, na przykład gdy ostatni wpis to sam znak `-` albo liczba za duża dla `int`, bez znaku końca wiersza. Tak samo wygląda stan strumienia, gdy danych w ogóle już nie ma. Funkcja, która rozpoznaje koniec danych po nieudanym odczycie, zgłosiłaby wtedy `end_of_input` zamiast `invalid_input` i ostatni błędny wpis by zniknął. Dla danych `"4\n-"` dałaby `accepted`, `end_of_input` zamiast `accepted`, `invalid_input`, `end_of_input`.

Dlatego koniec danych funkcja rozpoznaje przed odczytem liczby, po `std::ws`. Po odczycie stan strumienia jest potrzebny tylko do jednego pytania: czy odczyt się udał.

Jeszcze jedna drobna rzecz: gdy przyjęta liczba była ostatnim znakiem danych, odrzucenie reszty wiersza nie ma czego zabrać i ustawia `fail()`. Wynik `accepted` i odczytana wartość są już wtedy ustalone, a następne wywołanie i tak zwraca `end_of_input`.

</details>

## 4. Funkcja `read_number`

Cztery możliwe zakończenia odczytu dostają własne nazwy:

<!-- fragment -->
```cpp
enum class ReadResult {
    accepted,
    out_of_range,
    invalid_input,
    end_of_input
};
```

Funkcja dostaje strumień, dozwolony zakres i zmienną na wynik:

<!-- fragment -->
```cpp
ReadResult read_number(std::istream& input, int minimum, int maximum, int& result);
```

**Jedno wywołanie szuka następnego znaku, który nie jest białym znakiem, próbuje od tego miejsca odczytać liczbę, a potem zużywa resztę bieżącego wiersza.** Puste wiersze i wiersze z samymi białymi znakami nie są osobnymi próbami. Tekst, od którego zaczyna się próba, aż do końca jego wiersza nazywamy dalej **wpisem**.

### Kontrakt `read_number`

**Założenia:** `minimum <= maximum`, a źródło danych działa (punkt 3). Funkcja tego nie sprawdza.

| Wynik | Kiedy | `result` |
|---|---|---|
| `ReadResult::accepted` | odczyt liczby `int` się udał, a liczba jest od `minimum` do `maximum` | dostaje odczytaną liczbę |
| `ReadResult::out_of_range` | odczyt się udał, ale liczba jest mniejsza od `minimum` albo większa od `maximum` | bez zmian |
| `ReadResult::invalid_input` | odczyt liczby `int` się nie udał | bez zmian |
| `ReadResult::end_of_input` | nie ma kolejnego wpisu | bez zmian |

**`result` zmienia się wyłącznie przy `accepted`.** Przy każdym innym wyniku zachowuje wartość sprzed wywołania. Funkcja niczego nie wypisuje.

**Funkcja próbuje odczytać liczbę całkowitą na początku wpisu, a resztę wiersza odrzuca.** Nie sprawdza, czy cały wpis jest zapisem jednej liczby. Dla zakresu 1–6:

| Wpis | Wynik | Dlaczego |
|---|---|---|
| `3` | `accepted`, wartość 3 | |
| `3.5` | `accepted`, wartość 3 | `>>` odczytuje 3 i zatrzymuje się na kropce; `.5` zostaje odrzucone |
| `3 tickets` | `accepted`, wartość 3 | ` tickets` zostaje odrzucone |
| `2 5` | `accepted`, wartość 2 | `5` stoi w tym samym wierszu, więc zostaje odrzucone |
| `12abc` | `out_of_range` | odczyt daje 12, a 12 jest poza zakresem |
| `abc` | `invalid_input` | na początku wpisu nie ma liczby |

To świadoma granica tej funkcji, a nie ścisłe sprawdzanie całego wpisu: `3.5` nie jest poprawnym zapisem liczby całkowitej, a funkcja i tak przyjmie 3. Tak samo jak w lekcji 4.6, program odzyskuje wejście po nieudanym odczycie, ale nie sprawdza całych wierszy.

**Liczba za duża dla `int`.** Jeżeli zapis liczby nie mieści się w `int`, na przykład `999999999999999999999999`, odczyt się nie udaje. Funkcja zwraca wtedy `invalid_input`, a nie `out_of_range`: nie zna wartości wpisanej liczby.

**Dlaczego zmienna lokalna?** Nieudany odczyt może zapisać do zmiennej inną wartość, a w lekcji 4.6 padło: na wartości po nieudanym odczycie nie wolno polegać. Także udany odczyt liczby spoza zakresu zapisuje tę liczbę. Dlatego funkcja czyta do zmiennej `value`, a do `result` przepisuje ją dopiero po wszystkich sprawdzeniach, jak w lekcji 10.4.

### Cała funkcja

W punkcie 2 wywołanie `ignore` było zapisane wprost. W funkcji ta sama operacja jest potrzebna w dwóch miejscach, dlatego dostaje własną nazwę: `discard_rest_of_line`. W środku jest dokładnie to samo wywołanie.

<!-- fragment -->
```cpp
enum class ReadResult {
    accepted,
    out_of_range,
    invalid_input,
    end_of_input
};

void discard_rest_of_line(std::istream& input) {
    input.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
}

ReadResult read_number(std::istream& input, int minimum, int maximum, int& result) {
    if (input.bad()) {
        return ReadResult::end_of_input;
    }

    input >> std::ws;

    if (input.eof()) {
        return ReadResult::end_of_input;
    }

    int value{0};
    input >> value;

    if (input.fail()) {
        if (input.bad()) {
            return ReadResult::end_of_input;
        }

        input.clear();
        discard_rest_of_line(input);
        return ReadResult::invalid_input;
    }

    discard_rest_of_line(input);

    if (value < minimum || value > maximum) {
        return ReadResult::out_of_range;
    }

    result = value;
    return ReadResult::accepted;
}
```

| Krok | Kod | Po co |
|---|---|---|
| 1 | `if (input.bad())` na początku | źródło przestało działać: nie ma czego próbować |
| 2 | `input >> std::ws;` | pomija białe znaki i puste wiersze |
| 3 | `if (input.eof())` | nie ma kolejnego wpisu: `end_of_input` |
| 4 | `input >> value;` | odczyt do zmiennej lokalnej |
| 5 | `if (input.fail())` | odczyt się nie udał. `fail()` daje `true` także przy awarii źródła, więc najpierw `bad()`: awaria kończy odczyt bez odzyskiwania. Zwykły błędny wpis: `clear()`, odrzucenie reszty wiersza, `invalid_input` |
| 6 | `discard_rest_of_line(input);` po udanym odczycie | reszta wiersza znika, także po poprawnej liczbie |
| 7 | sprawdzenie zakresu | liczba poza zakresem: `out_of_range`, `result` bez zmian |
| 8 | `result = value;` | dopiero teraz: `accepted` |

Wynik zależy od tego, co dał odczyt i sprawdzenie zakresu. Odrzucanie reszty wiersza w kroku 6 może dojść do końca danych, ale nie zmienia już wyniku. Funkcja nie wywołuje `clear()` na początku każdej próby: czyści stan tylko wtedy, gdy właśnie rozpoznała nieudany odczyt błędnego wpisu.

## 5. Program, który pyta ponownie

`main` pyta o liczbę biletów, dopóki są dane:

<!-- fragment -->
```cpp
int main() {
    int tickets{0};
    bool input_ended{false};

    while (!input_ended) {
        std::cout << "How many tickets (1-6)?\n";
        const ReadResult result{read_number(std::cin, 1, 6, tickets)};

        switch (result) {
            case ReadResult::accepted:
                std::cout << "Tickets: " << tickets << "\n";
                break;
            case ReadResult::out_of_range:
                std::cout << "Choose from 1 to 6 tickets\n";
                break;
            case ReadResult::invalid_input:
                std::cout << "Not a whole number, try again\n";
                break;
            case ReadResult::end_of_input:
                input_ended = true;
                break;
        }
    }

    std::cout << "No more requests\n";
}
```

- **`const ReadResult result{read_number(std::cin, 1, 6, tickets)};`** wywołuje funkcję raz na pytanie i zapamiętuje wynik, jak w lekcji 14.3.
- **`switch` robi dla każdego wyniku co innego:** przy `accepted` podaje liczbę biletów, przy odmowach mówi, co poprawić, a przy `end_of_input` ustawia `input_ended`. Etykiety `case` nazywają wszystkie cztery wyniki.
- **`break` kończy tylko `switch`.** Pętlę kończy warunek `!input_ended`, jak flaga `input_ended` w lekcji 4.6.
- **Odzyskanie strumienia jest w funkcji.** `main` nie wywołuje `clear()` ani `ignore`: po każdym wywołaniu strumień jest gotowy na następną próbę.

**To pierwsze obowiązkowe uruchomienie.** W `cpp-workspace` utwórz katalog `lesson_14_4` (jeśli nie powstał w punkcie 1), skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program` i zastąp zawartość `main.cpp` pełnym programem poniżej. **Przewidź** odpowiedzi programu na cztery wpisy: `2`, `abc`, `9`, `3 tickets`. Potem uruchom program i wpisz je w oknie **Run**, każdy zakończony Enterem.

Nie musisz kończyć danych z klawiatury. Gdy skończysz, zatrzymaj program przyciskiem **Stop**. W sprawdzeniu automatycznym dane kończą się po ostatniej linijce, więc program sam wypisuje `No more requests`.

<details>
<summary>Pełny program</summary>

<!-- example: ticket_requests -->
```cpp
#include <iostream>
#include <limits>

enum class ReadResult {
    accepted,
    out_of_range,
    invalid_input,
    end_of_input
};

void discard_rest_of_line(std::istream& input) {
    input.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
}

ReadResult read_number(std::istream& input, int minimum, int maximum, int& result) {
    if (input.bad()) {
        return ReadResult::end_of_input;
    }

    input >> std::ws;

    if (input.eof()) {
        return ReadResult::end_of_input;
    }

    int value{0};
    input >> value;

    if (input.fail()) {
        if (input.bad()) {
            return ReadResult::end_of_input;
        }

        input.clear();
        discard_rest_of_line(input);
        return ReadResult::invalid_input;
    }

    discard_rest_of_line(input);

    if (value < minimum || value > maximum) {
        return ReadResult::out_of_range;
    }

    result = value;
    return ReadResult::accepted;
}

int main() {
    int tickets{0};
    bool input_ended{false};

    while (!input_ended) {
        std::cout << "How many tickets (1-6)?\n";
        const ReadResult result{read_number(std::cin, 1, 6, tickets)};

        switch (result) {
            case ReadResult::accepted:
                std::cout << "Tickets: " << tickets << "\n";
                break;
            case ReadResult::out_of_range:
                std::cout << "Choose from 1 to 6 tickets\n";
                break;
            case ReadResult::invalid_input:
                std::cout << "Not a whole number, try again\n";
                break;
            case ReadResult::end_of_input:
                input_ended = true;
                break;
        }
    }

    std::cout << "No more requests\n";
}
```

</details>

<!-- input: ticket_requests -->
```text
2
abc
9
3 tickets
```

<details>
<summary>Standardowe wyjście dla tych czterech wpisów</summary>

<!-- output: ticket_requests -->
```text
How many tickets (1-6)?
Tickets: 2
How many tickets (1-6)?
Not a whole number, try again
How many tickets (1-6)?
Choose from 1 to 6 tickets
How many tickets (1-6)?
Tickets: 3
How many tickets (1-6)?
No more requests
```

</details>

Drugie sprawdzenie zaczyna się od dwóch pustych wierszy:

<!-- input: ticket_requests -->
```text


5
```

<details>
<summary>Standardowe wyjście dla danych z pustymi wierszami</summary>

<!-- output: ticket_requests -->
```text
How many tickets (1-6)?
Tickets: 5
How many tickets (1-6)?
No more requests
```

</details>

Puste wiersze nie dają żadnego komunikatu: `std::ws` je pomija, więc nie są próbami. Wiersz z `3 tickets` daje 3 bilety, bo funkcja przyjmuje liczbę z początku wpisu.

## 6. Testy sekwencji na jednym strumieniu

W lekcji 13.3 każdy niezależny przypadek dostawał nowy `std::istringstream` i jedno wywołanie. Ta zasada zostaje: **każdy scenariusz testowy dostaje nowy strumień.** Wewnątrz scenariusza funkcja jest jednak wywoływana kilka razy **na tym samym strumieniu**, bo właśnie to robi program: czyta kolejne wpisy z jednego źródła. Lekcja 13.3 mówiła o tym wprost: jeden strumień jest właściwy, gdy program ma czytać kolejne dane z jednego źródła.

Każde wywołanie sprawdzasz dwa razy: wynik i wartość `tickets` po wywołaniu. Wynik porównuje funkcja `check_read_result`, zbudowana jak `check_issue_result` w lekcji 14.3. Tekst wyniku daje `read_result_text`, `switch` z zachowaniem zapasowym `"unknown"`, testowany jak w lekcji 14.3:

<!-- fragment -->
```cpp
void check_read_result(const std::string& name, ReadResult expected, ReadResult actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << read_result_text(expected) << ", actual " << read_result_text(actual) << "\n";
        ++failed;
    }
}
```

Początek scenariusza S1. Wywołanie `read_number` stoi wprost w argumencie, jak wywołanie testowanej funkcji w lekcji 13.1. Sprawdzenie `tickets` w następnej linijce widzi już stan po tym wywołaniu:

<!-- fragment -->
```cpp
std::istringstream input_s1{"2\nabc\n5\n"};
int tickets_s1{-1};
check_read_result("S1 call 1 result", ReadResult::accepted, read_number(input_s1, 1, 6, tickets_s1), checks, failed);
check_int("S1 call 1 tickets", 2, tickets_s1, checks, failed);
check_read_result("S1 call 2 result", ReadResult::invalid_input, read_number(input_s1, 1, 6, tickets_s1), checks, failed);
check_int("S1 call 2 tickets", 2, tickets_s1, checks, failed);
```

**Scenariusze**, zakres 1–6, `tickets` na początku każdego scenariusza równe −1. Wyniki oczekiwane wynikają z kontraktu z punktu 4:

| Scenariusz | Dane | Kolejne wywołania: wynik i `tickets` po nim | Co sprawdza |
|---|---|---|---|
| S1 | `"2\nabc\n5\n"` | `accepted` 2; `invalid_input` 2; `accepted` 5; `end_of_input` 5 | odzyskanie po błędnym wpisie |
| S2 | `"7\n3"` | `out_of_range` −1; `accepted` 3; `end_of_input` 3 | odmowa zakresu, ostatnia liczba bez znaku końca wiersza |
| S3 | `""` | `end_of_input` −1; `end_of_input` −1 | brak danych i wywołanie po końcu danych |
| S4 | `"4\n999999999999999999999999"` | `accepted` 4; `invalid_input` 4; `end_of_input` 4 | liczba za duża dla `int` jako ostatni wpis bez znaku końca wiersza |
| S5 | `"3 tickets\n5\n"` | `accepted` 3; `accepted` 5; `end_of_input` 5 | odrzucenie reszty wiersza po poprawnej liczbie |

- **Wartość początkowa −1, a nie 0.** −1 leży poza zakresem i żaden poprawny odczyt jej nie da. Każda zmiana `tickets` po odmowie będzie więc widoczna w linijce `FAIL`. Przy 0 część takich zmian by się ukryła.
- **Po odmowie `tickets` zostaje bez zmian:** w S1 po `abc` nadal 2, w S4 po za dużej liczbie nadal 4.

**Liczba sprawdzeń:** 15 wywołań po 2 sprawdzenia daje 30, do tego 4 sprawdzenia `read_result_text`, razem 34.

**To drugie obowiązkowe uruchomienie.** Zastąp zawartość `main.cpp` programem testowym poniżej. Funkcje `check_int` i `check_text` możesz skopiować z lekcji 14.3. **Przewidź** ostatnią linijkę, zanim uruchomisz program.

<details>
<summary>Pełny program testowy</summary>

<!-- example: ticket_tests -->
```cpp
#include <iostream>
#include <limits>
#include <sstream>
#include <string>

enum class ReadResult {
    accepted,
    out_of_range,
    invalid_input,
    end_of_input
};

void discard_rest_of_line(std::istream& input) {
    input.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
}

ReadResult read_number(std::istream& input, int minimum, int maximum, int& result) {
    if (input.bad()) {
        return ReadResult::end_of_input;
    }

    input >> std::ws;

    if (input.eof()) {
        return ReadResult::end_of_input;
    }

    int value{0};
    input >> value;

    if (input.fail()) {
        if (input.bad()) {
            return ReadResult::end_of_input;
        }

        input.clear();
        discard_rest_of_line(input);
        return ReadResult::invalid_input;
    }

    discard_rest_of_line(input);

    if (value < minimum || value > maximum) {
        return ReadResult::out_of_range;
    }

    result = value;
    return ReadResult::accepted;
}

std::string read_result_text(ReadResult result) {
    switch (result) {
        case ReadResult::accepted:
            return "accepted";
        case ReadResult::out_of_range:
            return "out_of_range";
        case ReadResult::invalid_input:
            return "invalid_input";
        case ReadResult::end_of_input:
            return "end_of_input";
    }

    return "unknown";
}

void check_read_result(const std::string& name, ReadResult expected, ReadResult actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << read_result_text(expected) << ", actual " << read_result_text(actual) << "\n";
        ++failed;
    }
}

void check_int(const std::string& name, int expected, int actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << expected << ", actual " << actual << "\n";
        ++failed;
    }
}

void check_text(const std::string& name, const std::string& expected, const std::string& actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected \"" << expected << "\", actual \"" << actual << "\"\n";
        ++failed;
    }
}

int main() {
    int checks{0};
    int failed{0};

    check_text("read_result_text(accepted)", "accepted", read_result_text(ReadResult::accepted), checks, failed);
    check_text("read_result_text(out_of_range)", "out_of_range", read_result_text(ReadResult::out_of_range), checks, failed);
    check_text("read_result_text(invalid_input)", "invalid_input", read_result_text(ReadResult::invalid_input), checks, failed);
    check_text("read_result_text(end_of_input)", "end_of_input", read_result_text(ReadResult::end_of_input), checks, failed);

    std::istringstream input_s1{"2\nabc\n5\n"};
    int tickets_s1{-1};
    check_read_result("S1 call 1 result", ReadResult::accepted, read_number(input_s1, 1, 6, tickets_s1), checks, failed);
    check_int("S1 call 1 tickets", 2, tickets_s1, checks, failed);
    check_read_result("S1 call 2 result", ReadResult::invalid_input, read_number(input_s1, 1, 6, tickets_s1), checks, failed);
    check_int("S1 call 2 tickets", 2, tickets_s1, checks, failed);
    check_read_result("S1 call 3 result", ReadResult::accepted, read_number(input_s1, 1, 6, tickets_s1), checks, failed);
    check_int("S1 call 3 tickets", 5, tickets_s1, checks, failed);
    check_read_result("S1 call 4 result", ReadResult::end_of_input, read_number(input_s1, 1, 6, tickets_s1), checks, failed);
    check_int("S1 call 4 tickets", 5, tickets_s1, checks, failed);

    std::istringstream input_s2{"7\n3"};
    int tickets_s2{-1};
    check_read_result("S2 call 1 result", ReadResult::out_of_range, read_number(input_s2, 1, 6, tickets_s2), checks, failed);
    check_int("S2 call 1 tickets", -1, tickets_s2, checks, failed);
    check_read_result("S2 call 2 result", ReadResult::accepted, read_number(input_s2, 1, 6, tickets_s2), checks, failed);
    check_int("S2 call 2 tickets", 3, tickets_s2, checks, failed);
    check_read_result("S2 call 3 result", ReadResult::end_of_input, read_number(input_s2, 1, 6, tickets_s2), checks, failed);
    check_int("S2 call 3 tickets", 3, tickets_s2, checks, failed);

    std::istringstream input_s3{""};
    int tickets_s3{-1};
    check_read_result("S3 call 1 result", ReadResult::end_of_input, read_number(input_s3, 1, 6, tickets_s3), checks, failed);
    check_int("S3 call 1 tickets", -1, tickets_s3, checks, failed);
    check_read_result("S3 call 2 result", ReadResult::end_of_input, read_number(input_s3, 1, 6, tickets_s3), checks, failed);
    check_int("S3 call 2 tickets", -1, tickets_s3, checks, failed);

    std::istringstream input_s4{"4\n999999999999999999999999"};
    int tickets_s4{-1};
    check_read_result("S4 call 1 result", ReadResult::accepted, read_number(input_s4, 1, 6, tickets_s4), checks, failed);
    check_int("S4 call 1 tickets", 4, tickets_s4, checks, failed);
    check_read_result("S4 call 2 result", ReadResult::invalid_input, read_number(input_s4, 1, 6, tickets_s4), checks, failed);
    check_int("S4 call 2 tickets", 4, tickets_s4, checks, failed);
    check_read_result("S4 call 3 result", ReadResult::end_of_input, read_number(input_s4, 1, 6, tickets_s4), checks, failed);
    check_int("S4 call 3 tickets", 4, tickets_s4, checks, failed);

    std::istringstream input_s5{"3 tickets\n5\n"};
    int tickets_s5{-1};
    check_read_result("S5 call 1 result", ReadResult::accepted, read_number(input_s5, 1, 6, tickets_s5), checks, failed);
    check_int("S5 call 1 tickets", 3, tickets_s5, checks, failed);
    check_read_result("S5 call 2 result", ReadResult::accepted, read_number(input_s5, 1, 6, tickets_s5), checks, failed);
    check_int("S5 call 2 tickets", 5, tickets_s5, checks, failed);
    check_read_result("S5 call 3 result", ReadResult::end_of_input, read_number(input_s5, 1, 6, tickets_s5), checks, failed);
    check_int("S5 call 3 tickets", 5, tickets_s5, checks, failed);

    std::cout << "Checks: " << checks << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }
}
```

</details>

<details>
<summary>Standardowe wyjście</summary>

<!-- output: ticket_tests -->
```text
PASS read_result_text(accepted)
PASS read_result_text(out_of_range)
PASS read_result_text(invalid_input)
PASS read_result_text(end_of_input)
PASS S1 call 1 result
PASS S1 call 1 tickets
PASS S1 call 2 result
PASS S1 call 2 tickets
PASS S1 call 3 result
PASS S1 call 3 tickets
PASS S1 call 4 result
PASS S1 call 4 tickets
PASS S2 call 1 result
PASS S2 call 1 tickets
PASS S2 call 2 result
PASS S2 call 2 tickets
PASS S2 call 3 result
PASS S2 call 3 tickets
PASS S3 call 1 result
PASS S3 call 1 tickets
PASS S3 call 2 result
PASS S3 call 2 tickets
PASS S4 call 1 result
PASS S4 call 1 tickets
PASS S4 call 2 result
PASS S4 call 2 tickets
PASS S4 call 3 result
PASS S4 call 3 tickets
PASS S5 call 1 result
PASS S5 call 1 tickets
PASS S5 call 2 result
PASS S5 call 2 tickets
PASS S5 call 3 result
PASS S5 call 3 tickets
Checks: 34, failed: 0
```

Kod zakończenia: 0.

</details>

## 7. Diagnostyka: `ignore` bez `clear()`

Ktoś uznaje, że skoro błędny tekst trzeba usunąć, wystarczy go odrzucić, i pomija `clear()`:

<!-- fragment -->
```cpp
if (input.fail()) {
    if (input.bad()) {
        return ReadResult::end_of_input;
    }

    discard_rest_of_line(input);
    return ReadResult::invalid_input;
}
```

**To trzecie obowiązkowe uruchomienie.** Wykonaj kroki po kolei:

1. **Przewidź** na podstawie tabeli scenariuszy z punktu 6: który scenariusz to zauważy? Które wywołania dadzą `FAIL` i co będzie po `actual`?
2. W programie testowym z punktu 6 usuń w `read_number` linijkę `input.clear();`. Nic więcej nie zmieniaj, ani testów, ani wyników oczekiwanych.
3. Uruchom testy. Zapisz linijki `FAIL`, podsumowanie i kod zakończenia.
4. Przywróć `input.clear();` i uruchom te same testy jeszcze raz.

**Nie uruchamiaj z tą usterką programu z punktu 5.** Po pierwszym błędnym wpisie wypisywałby `Not a whole number, try again` bez końca i trzeba by go zatrzymać przyciskiem **Stop**. Program testowy wywołuje funkcję określoną liczbę razy, więc zawsze się kończy.

<details>
<summary>Co się dzieje i jak to naprawić: otwórz po wykonaniu kroków 1–4</summary>

Program testowy z tą zmianą, bez innych zmian:

<!-- example: ticket_tests_no_clear exit=1 -->
```cpp
#include <iostream>
#include <limits>
#include <sstream>
#include <string>

enum class ReadResult {
    accepted,
    out_of_range,
    invalid_input,
    end_of_input
};

void discard_rest_of_line(std::istream& input) {
    input.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
}

ReadResult read_number(std::istream& input, int minimum, int maximum, int& result) {
    if (input.bad()) {
        return ReadResult::end_of_input;
    }

    input >> std::ws;

    if (input.eof()) {
        return ReadResult::end_of_input;
    }

    int value{0};
    input >> value;

    if (input.fail()) {
        if (input.bad()) {
            return ReadResult::end_of_input;
        }

        discard_rest_of_line(input);
        return ReadResult::invalid_input;
    }

    discard_rest_of_line(input);

    if (value < minimum || value > maximum) {
        return ReadResult::out_of_range;
    }

    result = value;
    return ReadResult::accepted;
}

std::string read_result_text(ReadResult result) {
    switch (result) {
        case ReadResult::accepted:
            return "accepted";
        case ReadResult::out_of_range:
            return "out_of_range";
        case ReadResult::invalid_input:
            return "invalid_input";
        case ReadResult::end_of_input:
            return "end_of_input";
    }

    return "unknown";
}

void check_read_result(const std::string& name, ReadResult expected, ReadResult actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << read_result_text(expected) << ", actual " << read_result_text(actual) << "\n";
        ++failed;
    }
}

void check_int(const std::string& name, int expected, int actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << expected << ", actual " << actual << "\n";
        ++failed;
    }
}

void check_text(const std::string& name, const std::string& expected, const std::string& actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected \"" << expected << "\", actual \"" << actual << "\"\n";
        ++failed;
    }
}

int main() {
    int checks{0};
    int failed{0};

    check_text("read_result_text(accepted)", "accepted", read_result_text(ReadResult::accepted), checks, failed);
    check_text("read_result_text(out_of_range)", "out_of_range", read_result_text(ReadResult::out_of_range), checks, failed);
    check_text("read_result_text(invalid_input)", "invalid_input", read_result_text(ReadResult::invalid_input), checks, failed);
    check_text("read_result_text(end_of_input)", "end_of_input", read_result_text(ReadResult::end_of_input), checks, failed);

    std::istringstream input_s1{"2\nabc\n5\n"};
    int tickets_s1{-1};
    check_read_result("S1 call 1 result", ReadResult::accepted, read_number(input_s1, 1, 6, tickets_s1), checks, failed);
    check_int("S1 call 1 tickets", 2, tickets_s1, checks, failed);
    check_read_result("S1 call 2 result", ReadResult::invalid_input, read_number(input_s1, 1, 6, tickets_s1), checks, failed);
    check_int("S1 call 2 tickets", 2, tickets_s1, checks, failed);
    check_read_result("S1 call 3 result", ReadResult::accepted, read_number(input_s1, 1, 6, tickets_s1), checks, failed);
    check_int("S1 call 3 tickets", 5, tickets_s1, checks, failed);
    check_read_result("S1 call 4 result", ReadResult::end_of_input, read_number(input_s1, 1, 6, tickets_s1), checks, failed);
    check_int("S1 call 4 tickets", 5, tickets_s1, checks, failed);

    std::istringstream input_s2{"7\n3"};
    int tickets_s2{-1};
    check_read_result("S2 call 1 result", ReadResult::out_of_range, read_number(input_s2, 1, 6, tickets_s2), checks, failed);
    check_int("S2 call 1 tickets", -1, tickets_s2, checks, failed);
    check_read_result("S2 call 2 result", ReadResult::accepted, read_number(input_s2, 1, 6, tickets_s2), checks, failed);
    check_int("S2 call 2 tickets", 3, tickets_s2, checks, failed);
    check_read_result("S2 call 3 result", ReadResult::end_of_input, read_number(input_s2, 1, 6, tickets_s2), checks, failed);
    check_int("S2 call 3 tickets", 3, tickets_s2, checks, failed);

    std::istringstream input_s3{""};
    int tickets_s3{-1};
    check_read_result("S3 call 1 result", ReadResult::end_of_input, read_number(input_s3, 1, 6, tickets_s3), checks, failed);
    check_int("S3 call 1 tickets", -1, tickets_s3, checks, failed);
    check_read_result("S3 call 2 result", ReadResult::end_of_input, read_number(input_s3, 1, 6, tickets_s3), checks, failed);
    check_int("S3 call 2 tickets", -1, tickets_s3, checks, failed);

    std::istringstream input_s4{"4\n999999999999999999999999"};
    int tickets_s4{-1};
    check_read_result("S4 call 1 result", ReadResult::accepted, read_number(input_s4, 1, 6, tickets_s4), checks, failed);
    check_int("S4 call 1 tickets", 4, tickets_s4, checks, failed);
    check_read_result("S4 call 2 result", ReadResult::invalid_input, read_number(input_s4, 1, 6, tickets_s4), checks, failed);
    check_int("S4 call 2 tickets", 4, tickets_s4, checks, failed);
    check_read_result("S4 call 3 result", ReadResult::end_of_input, read_number(input_s4, 1, 6, tickets_s4), checks, failed);
    check_int("S4 call 3 tickets", 4, tickets_s4, checks, failed);

    std::istringstream input_s5{"3 tickets\n5\n"};
    int tickets_s5{-1};
    check_read_result("S5 call 1 result", ReadResult::accepted, read_number(input_s5, 1, 6, tickets_s5), checks, failed);
    check_int("S5 call 1 tickets", 3, tickets_s5, checks, failed);
    check_read_result("S5 call 2 result", ReadResult::accepted, read_number(input_s5, 1, 6, tickets_s5), checks, failed);
    check_int("S5 call 2 tickets", 5, tickets_s5, checks, failed);
    check_read_result("S5 call 3 result", ReadResult::end_of_input, read_number(input_s5, 1, 6, tickets_s5), checks, failed);
    check_int("S5 call 3 tickets", 5, tickets_s5, checks, failed);

    std::cout << "Checks: " << checks << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }
}
```

<!-- output: ticket_tests_no_clear -->
```text
PASS read_result_text(accepted)
PASS read_result_text(out_of_range)
PASS read_result_text(invalid_input)
PASS read_result_text(end_of_input)
PASS S1 call 1 result
PASS S1 call 1 tickets
PASS S1 call 2 result
PASS S1 call 2 tickets
FAIL S1 call 3 result: expected accepted, actual invalid_input
FAIL S1 call 3 tickets: expected 5, actual 2
FAIL S1 call 4 result: expected end_of_input, actual invalid_input
FAIL S1 call 4 tickets: expected 5, actual 2
PASS S2 call 1 result
PASS S2 call 1 tickets
PASS S2 call 2 result
PASS S2 call 2 tickets
PASS S2 call 3 result
PASS S2 call 3 tickets
PASS S3 call 1 result
PASS S3 call 1 tickets
PASS S3 call 2 result
PASS S3 call 2 tickets
PASS S4 call 1 result
PASS S4 call 1 tickets
PASS S4 call 2 result
PASS S4 call 2 tickets
PASS S4 call 3 result
PASS S4 call 3 tickets
PASS S5 call 1 result
PASS S5 call 1 tickets
PASS S5 call 2 result
PASS S5 call 2 tickets
PASS S5 call 3 result
PASS S5 call 3 tickets
Checks: 34, failed: 4
```

Kod zakończenia: 1. Wynika z czterech rzeczywistych linijek `FAIL`: `main` zwraca 1, bo `failed` jest większe od 0.

| Scenariusz | Co się dzieje | Sprawdzenia `FAIL` |
|---|---|---|
| S1 | wywołanie 2 poprawnie zgłasza `invalid_input`, ale strumień zostaje w stanie błędu; `ignore` niczego nie zabiera, więc wywołania 3 i 4 znowu trafiają na ten sam błąd | wynik i `tickets` w wywołaniach 3 i 4 |
| S4 | nieudany odczyt za dużej liczby dochodzi do końca danych, więc następne wywołanie i tak znajduje koniec | żadne |
| S2, S3, S5 | nie ma w nich nieudanego odczytu | żadne |

- **`ignore` na strumieniu w stanie błędu nic nie robi.** Odczyt w wywołaniu 3 trafia na to samo `abc`. Strumień nie wychodzi z błędu, więc do `5` funkcja nigdy nie dochodzi.
- **Wynik wywołania 2 jest poprawny.** Usterkę widać dopiero w następnych wywołaniach na tym samym strumieniu. Test pojedynczego wywołania, jak w lekcji 13.3, by jej nie zauważył.
- **W programie z pętlą** każde wywołanie zwracałoby `invalid_input`, a `end_of_input` nigdy by nie przyszło.

**Poprawka:** przywróć `input.clear();` przed odrzuceniem reszty wiersza. Te same testy, z tymi samymi wynikami oczekiwanymi, wypisują 34 razy `PASS` i `Checks: 34, failed: 0`, a kod zakończenia wynosi 0.

</details>

### Nieobowiązkowo: koniec danych sprawdzony za późno

Ten wariant tylko przeczytaj i przewidź jego skutek. Ktoś przenosi sprawdzenie `eof()` za odczyt liczby:

<!-- fragment -->
```cpp
input >> std::ws;

int value{0};
input >> value;

if (input.eof()) {
    return ReadResult::end_of_input;
}
```

**Przewidź:** który scenariusz z punktu 6 straci liczbę, a który błędny wpis?

<details>
<summary>Odpowiedź i program, który ją sprawdza</summary>

- **S2:** `3` jest ostatnim znakiem danych. Odczyt daje 3 i dochodzi do końca, więc `eof()` daje `true` i funkcja zwraca `end_of_input`. Poprawna liczba ginie, a `tickets` zostaje −1. To pułapka z lekcji 4.6.
- **S4:** nieudany odczyt za dużej liczby też dochodzi do końca. Funkcja zwraca `end_of_input` zamiast `invalid_input`, więc ostatni błędny wpis znika.
- **S1, S3, S5:** bez zmian, bo w nich żaden odczyt liczby nie kończy się na samym końcu danych.

<!-- example: ticket_tests_eof_after exit=1 -->
```cpp
#include <iostream>
#include <limits>
#include <sstream>
#include <string>

enum class ReadResult {
    accepted,
    out_of_range,
    invalid_input,
    end_of_input
};

void discard_rest_of_line(std::istream& input) {
    input.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
}

ReadResult read_number(std::istream& input, int minimum, int maximum, int& result) {
    if (input.bad()) {
        return ReadResult::end_of_input;
    }

    input >> std::ws;

    int value{0};
    input >> value;

    if (input.eof()) {
        return ReadResult::end_of_input;
    }

    if (input.fail()) {
        if (input.bad()) {
            return ReadResult::end_of_input;
        }

        input.clear();
        discard_rest_of_line(input);
        return ReadResult::invalid_input;
    }

    discard_rest_of_line(input);

    if (value < minimum || value > maximum) {
        return ReadResult::out_of_range;
    }

    result = value;
    return ReadResult::accepted;
}

std::string read_result_text(ReadResult result) {
    switch (result) {
        case ReadResult::accepted:
            return "accepted";
        case ReadResult::out_of_range:
            return "out_of_range";
        case ReadResult::invalid_input:
            return "invalid_input";
        case ReadResult::end_of_input:
            return "end_of_input";
    }

    return "unknown";
}

void check_read_result(const std::string& name, ReadResult expected, ReadResult actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << read_result_text(expected) << ", actual " << read_result_text(actual) << "\n";
        ++failed;
    }
}

void check_int(const std::string& name, int expected, int actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << expected << ", actual " << actual << "\n";
        ++failed;
    }
}

void check_text(const std::string& name, const std::string& expected, const std::string& actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected \"" << expected << "\", actual \"" << actual << "\"\n";
        ++failed;
    }
}

int main() {
    int checks{0};
    int failed{0};

    check_text("read_result_text(accepted)", "accepted", read_result_text(ReadResult::accepted), checks, failed);
    check_text("read_result_text(out_of_range)", "out_of_range", read_result_text(ReadResult::out_of_range), checks, failed);
    check_text("read_result_text(invalid_input)", "invalid_input", read_result_text(ReadResult::invalid_input), checks, failed);
    check_text("read_result_text(end_of_input)", "end_of_input", read_result_text(ReadResult::end_of_input), checks, failed);

    std::istringstream input_s1{"2\nabc\n5\n"};
    int tickets_s1{-1};
    check_read_result("S1 call 1 result", ReadResult::accepted, read_number(input_s1, 1, 6, tickets_s1), checks, failed);
    check_int("S1 call 1 tickets", 2, tickets_s1, checks, failed);
    check_read_result("S1 call 2 result", ReadResult::invalid_input, read_number(input_s1, 1, 6, tickets_s1), checks, failed);
    check_int("S1 call 2 tickets", 2, tickets_s1, checks, failed);
    check_read_result("S1 call 3 result", ReadResult::accepted, read_number(input_s1, 1, 6, tickets_s1), checks, failed);
    check_int("S1 call 3 tickets", 5, tickets_s1, checks, failed);
    check_read_result("S1 call 4 result", ReadResult::end_of_input, read_number(input_s1, 1, 6, tickets_s1), checks, failed);
    check_int("S1 call 4 tickets", 5, tickets_s1, checks, failed);

    std::istringstream input_s2{"7\n3"};
    int tickets_s2{-1};
    check_read_result("S2 call 1 result", ReadResult::out_of_range, read_number(input_s2, 1, 6, tickets_s2), checks, failed);
    check_int("S2 call 1 tickets", -1, tickets_s2, checks, failed);
    check_read_result("S2 call 2 result", ReadResult::accepted, read_number(input_s2, 1, 6, tickets_s2), checks, failed);
    check_int("S2 call 2 tickets", 3, tickets_s2, checks, failed);
    check_read_result("S2 call 3 result", ReadResult::end_of_input, read_number(input_s2, 1, 6, tickets_s2), checks, failed);
    check_int("S2 call 3 tickets", 3, tickets_s2, checks, failed);

    std::istringstream input_s3{""};
    int tickets_s3{-1};
    check_read_result("S3 call 1 result", ReadResult::end_of_input, read_number(input_s3, 1, 6, tickets_s3), checks, failed);
    check_int("S3 call 1 tickets", -1, tickets_s3, checks, failed);
    check_read_result("S3 call 2 result", ReadResult::end_of_input, read_number(input_s3, 1, 6, tickets_s3), checks, failed);
    check_int("S3 call 2 tickets", -1, tickets_s3, checks, failed);

    std::istringstream input_s4{"4\n999999999999999999999999"};
    int tickets_s4{-1};
    check_read_result("S4 call 1 result", ReadResult::accepted, read_number(input_s4, 1, 6, tickets_s4), checks, failed);
    check_int("S4 call 1 tickets", 4, tickets_s4, checks, failed);
    check_read_result("S4 call 2 result", ReadResult::invalid_input, read_number(input_s4, 1, 6, tickets_s4), checks, failed);
    check_int("S4 call 2 tickets", 4, tickets_s4, checks, failed);
    check_read_result("S4 call 3 result", ReadResult::end_of_input, read_number(input_s4, 1, 6, tickets_s4), checks, failed);
    check_int("S4 call 3 tickets", 4, tickets_s4, checks, failed);

    std::istringstream input_s5{"3 tickets\n5\n"};
    int tickets_s5{-1};
    check_read_result("S5 call 1 result", ReadResult::accepted, read_number(input_s5, 1, 6, tickets_s5), checks, failed);
    check_int("S5 call 1 tickets", 3, tickets_s5, checks, failed);
    check_read_result("S5 call 2 result", ReadResult::accepted, read_number(input_s5, 1, 6, tickets_s5), checks, failed);
    check_int("S5 call 2 tickets", 5, tickets_s5, checks, failed);
    check_read_result("S5 call 3 result", ReadResult::end_of_input, read_number(input_s5, 1, 6, tickets_s5), checks, failed);
    check_int("S5 call 3 tickets", 5, tickets_s5, checks, failed);

    std::cout << "Checks: " << checks << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }
}
```

<!-- output: ticket_tests_eof_after -->
```text
PASS read_result_text(accepted)
PASS read_result_text(out_of_range)
PASS read_result_text(invalid_input)
PASS read_result_text(end_of_input)
PASS S1 call 1 result
PASS S1 call 1 tickets
PASS S1 call 2 result
PASS S1 call 2 tickets
PASS S1 call 3 result
PASS S1 call 3 tickets
PASS S1 call 4 result
PASS S1 call 4 tickets
PASS S2 call 1 result
PASS S2 call 1 tickets
FAIL S2 call 2 result: expected accepted, actual end_of_input
FAIL S2 call 2 tickets: expected 3, actual -1
PASS S2 call 3 result
FAIL S2 call 3 tickets: expected 3, actual -1
PASS S3 call 1 result
PASS S3 call 1 tickets
PASS S3 call 2 result
PASS S3 call 2 tickets
PASS S4 call 1 result
PASS S4 call 1 tickets
FAIL S4 call 2 result: expected invalid_input, actual end_of_input
PASS S4 call 2 tickets
PASS S4 call 3 result
PASS S4 call 3 tickets
PASS S5 call 1 result
PASS S5 call 1 tickets
PASS S5 call 2 result
PASS S5 call 2 tickets
PASS S5 call 3 result
PASS S5 call 3 tickets
Checks: 34, failed: 4
```

Kod zakończenia: 1.

</details>

## 8. Misja: oceny w ankiecie

Po warsztatach uczestnicy oceniają je w skali od 1 do 5. Oceny trafiają do programu jako kolejne wpisy, po jednej w wierszu. Zdarzają się pomyłki: pusty wiersz, tekst zamiast liczby, liczba spoza skali. Twoim zadaniem jest funkcja, która przejdzie przez wszystkie wpisy i policzy, co się w nich znalazło, oraz program testowy, który sprawdzi ją razem z funkcją odczytu.

`read_number` zostaje taka jak w demonstracji. Nowa jest funkcja, która wywołuje ją aż do końca danych:

<!-- fragment -->
```cpp
struct SurveyCounts {
    int accepted;
    int out_of_range;
    int invalid_input;
    int sum;
};

SurveyCounts count_ratings(std::istream& input);
```

**Kontrakt `count_ratings`:**

- wywołuje `read_number` dla zakresu 1–5, aż dostanie `end_of_input`;
- przy `accepted` zwiększa `accepted` o 1 i dodaje odczytaną ocenę do `sum`;
- przy `out_of_range` zwiększa `out_of_range` o 1;
- przy `invalid_input` zwiększa `invalid_input` o 1;
- przy `end_of_input` kończy pracę: sam koniec danych nie jest odmową i nie jest liczony;
- odmowy nie zmieniają `sum`;
- niczego nie wypisuje i zwraca liczniki.

Trzy pierwsze pola `SurveyCounts` mają te same nazwy co wyniki, które liczą, a `sum` to suma przyjętych ocen. Średniej nie liczysz.

**Zasady:**

- `ReadResult`, `discard_rest_of_line`, `read_number`, `read_result_text` i `check_read_result` skopiuj z punktu 6 bez zmian, a `check_int` z lekcji 14.3.
- Każdy scenariusz ma własny `std::istringstream`. W scenariuszu kolejne wywołania korzystają z tego samego strumienia.
- Dwa rodzaje scenariuszy. **Scenariusze odczytu** wywołują `read_number` z zakresem 1–5 i sprawdzają po każdym wywołaniu wynik i ocenę. **Scenariusze liczenia** wywołują `count_ratings` i sprawdzają wszystkie cztery pola.
- Zmienna z oceną zaczyna każdy scenariusz odczytu od wartości spoza zakresu i różnej od 0, na przykład −1.

W `cpp-workspace` utwórz katalog `survey_ratings`, skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program` i otwórz go w CLionie. Całość napisz w jednym pliku `main.cpp`. `CMakeLists.txt` zostaw bez zmian.

**Kolejność pracy:**

1. **Najpierw tabela scenariuszy.** Zanim napiszesz kod, wypisz scenariusze z danymi i wynikami oczekiwanymi wyprowadzonymi z kontraktu. Tabela ma zawierać co najmniej:
   - przyjętą ocenę;
   - odmowę z powodu zakresu, z oceną bez zmian;
   - błędny wpis, po którym następuje poprawny;
   - dwa błędne wpisy z rzędu;
   - ostatnią poprawną ocenę bez znaku końca wiersza;
   - ostatni błędny wpis bez znaku końca wiersza;
   - niezmienioną ocenę po błędnym wpisie;
   - scenariusz liczenia z mieszanymi wpisami i pustym wierszem;
   - scenariusz liczenia bez danych.

   Pod tabelą zapisz przewidywanie: które sprawdzenia się nie udadzą, gdy `read_number` zacznie czytać od razu do `result`, zamiast do zmiennej lokalnej? Czy zauważą to scenariusze liczenia?
2. Zdefiniuj `SurveyCounts` i napisz `count_ratings`.
3. Napisz program testowy: sprawdzenia z Twojej tabeli, a na końcu podsumowanie i kod zakończenia jak w punkcie 6.
4. **To czwarte obowiązkowe uruchomienie:** uruchom program testowy. Wszystkie sprawdzenia powinny wypisać `PASS`, a kod zakończenia powinien wynosić 0.
5. **Celowa usterka.** W `read_number` zamiast `int value{0};` i `input >> value;` wpisz `input >> result;`, w sprawdzeniu zakresu użyj `result` zamiast `value` i usuń linijkę `result = value;`. Testów i wyników oczekiwanych nie zmieniaj. **To piąte obowiązkowe uruchomienie:** uruchom testy, zapisz linijki `FAIL`, podsumowanie i kod zakończenia i porównaj je z przewidywaniem z kroku 1. Potem przywróć zmienną lokalną i uruchom te same testy jeszcze raz.

Jeśli chcesz, napisz jeszcze program, który czyta oceny z klawiatury przez `count_ratings(std::cin)` i wypisuje liczniki. Ten krok jest nieobowiązkowy, a przykład jest w przykładowym rozwiązaniu.

### Kryterium sukcesu

- [ ] Program buduje się jako C++20, a `CMakeLists.txt` jest taki jak w lekcji 0.5.
- [ ] `read_number` jest taka jak w punkcie 6 i jest wywoływana z zakresem 1–5.
- [ ] `SurveyCounts` ma pola `accepted`, `out_of_range`, `invalid_input` i `sum`.
- [ ] `count_ratings` dostaje strumień przez `std::istream&`, wywołuje `read_number` w pętli i obsługuje cztery wyniki instrukcją `switch` z etykietą dla każdego z nich.
- [ ] Pętla kończy się po `end_of_input`, a koniec danych nie jest liczony jako odmowa.
- [ ] Do `sum` trafiają tylko przyjęte oceny. `count_ratings` niczego nie wypisuje.
- [ ] Tabela scenariuszy powstała przed kodem, ma wszystkie wymagane rodzaje i wyniki oczekiwane z kontraktu.
- [ ] Każdy scenariusz ma własny strumień, a kolejne wywołania w scenariuszu korzystają z tego samego strumienia.
- [ ] Scenariusze odczytu sprawdzają po każdym wywołaniu wynik i ocenę. Ocena zaczyna od wartości spoza zakresu i różnej od 0.
- [ ] Scenariusze liczenia sprawdzają wszystkie cztery pola `SurveyCounts`.
- [ ] Z poprawną funkcją wszystkie sprawdzenia przechodzą, a kod zakończenia wynosi 0.
- [ ] Z celową usterką `FAIL` wypisują sprawdzenia oceny po odmowach, a kod zakończenia wynosi 1. Wynik zgadza się z Twoim przewidywaniem albo umiesz wyjaśnić różnicę.
- [ ] Po przywróceniu zmiennej lokalnej te same testy, bez zmian, znów przechodzą z kodem 0.

Gdy wynik się zgadza, możesz zapisać projekt w Gicie, jak w lekcji 1.5: `main.cpp` i `CMakeLists.txt`, bez katalogu budowania.

<details>
<summary>Podpowiedź 1: nazwane wyniki</summary>

Co `read_number` zwraca po poprawnym odczycie, co po każdej z dwóch odmów, a co wtedy, gdy danych już nie ma? Który z tych wyników zmienia który licznik, a który kończy pętlę? Czy przy którymś wyniku trzeba coś dodać do sumy?

</details>

<details>
<summary>Podpowiedź 2: odzyskiwanie</summary>

Dlaczego `clear()` bez odrzucenia reszty wiersza nie wystarcza? Co trafiłoby do następnego wywołania, gdyby po `abc` został tylko zdjęty stan błędu? Który z Twoich scenariuszy pokaże, że po błędnym wpisie następny poprawny jest naprawdę odczytany?

</details>

<details>
<summary>Podpowiedź 3: koniec danych i niezmienność</summary>

Kiedy pętla w `count_ratings` ma się skończyć i dlaczego koniec danych nie jest odmową? Jak sprawdzić, że ocena po odmowie ma tę samą wartość co przed wywołaniem? Od jakiej wartości ocena powinna zaczynać, żeby każda zmiana była widoczna? Czy same liczniki wystarczą, żeby to sprawdzić?

</details>

<details>
<summary>Pełna lista scenariuszy kontrolnych: otwórz po przygotowaniu własnej tabeli</summary>

Scenariusze odczytu, zakres 1–5, ocena na początku −1:

| Scenariusz | Dane | Kolejne wywołania: wynik i ocena po nim | Co sprawdza |
|---|---|---|---|
| R1 | `"abc\n4\n"` | `invalid_input` −1; `accepted` 4; `end_of_input` 4 | błędny wpis, potem poprawny; ocena bez zmian po błędnym wpisie |
| R2 | `"0\n6\n1"` | `out_of_range` −1; `out_of_range` −1; `accepted` 1; `end_of_input` 1 | liczby tuż za obiema granicami; najmniejsza ocena przyjęta; ostatnia poprawna ocena bez znaku końca wiersza |
| R3 | `"2\nxyz"` | `accepted` 2; `invalid_input` 2; `end_of_input` 2 | ostatni błędny wpis bez znaku końca wiersza; ocena bez zmian po wcześniejszej przyjętej |

Scenariusze liczenia:

| Scenariusz | Dane | `accepted` | `out_of_range` | `invalid_input` | `sum` | Co sprawdza |
|---|---|---:|---:|---:|---:|---|
| C1 | `"5\n\nabc\nxyz\n0\n3 stars\n4"` | 3 | 1 | 2 | 12 | wszystkie rodzaje wyników, pusty wiersz, dwa błędne wpisy z rzędu, prefiks liczbowy, ostatnia ocena bez znaku końca wiersza |
| C2 | `""` | 0 | 0 | 0 | 0 | brak danych: koniec danych nie jest odmową |

Twoja tabela nie musi mieć dokładnie tych scenariuszy. Musi mieć wszystkie rodzaje wymienione w kroku 1 misji.

</details>

Przykładowe rozwiązanie jest w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 9. Gdy coś pójdzie inaczej

| Co widzisz | Co to znaczy | Co zrobić |
|---|---|---|
| Ten sam komunikat o błędnym wpisie powtarza się bez końca | Po nieudanym odczycie brakuje `clear()` albo odrzucenia reszty wiersza, więc następna próba trafia na ten sam tekst (punkty 1 i 7). | Zatrzymaj program przyciskiem **Stop**. Po nieudanym odczycie wywołaj `clear()`, a potem odrzuć resztę wiersza. |
| Program testowy misji się nie kończy | Pętla w `count_ratings` czeka na `end_of_input`, a z tego samego powodu co wyżej każda próba daje `invalid_input`. | Zatrzymaj program i sprawdź odzyskiwanie w `read_number`. |
| Ostatnia liczba bez znaku końca wiersza daje `end_of_input` zamiast `accepted` | Funkcja sprawdza `eof()` po odczycie liczby (punkt 7, wariant nieobowiązkowy). | Sprawdzaj koniec danych przed odczytem liczby, po `input >> std::ws`. |
| Ostatni błędny wpis bez znaku końca wiersza daje `end_of_input` zamiast `invalid_input` | Funkcja rozpoznaje koniec danych po nieudanym odczycie (punkt 3). | Jak wyżej: koniec danych przed odczytem, po odczycie tylko `fail()`. |
| Po odmowie zmienna z wynikiem ma inną wartość, na przykład 0 | Odczyt idzie od razu do `result` albo przypisanie stoi przed sprawdzeniem zakresu. | Czytaj do zmiennej lokalnej i przypisuj tylko przy `accepted`. |
| `3 tickets` daje dwa wyniki: `accepted` i `invalid_input` | Po udanym odczycie brakuje odrzucenia reszty wiersza, więc ` tickets` trafia do następnej próby. | Wywołaj `discard_rest_of_line(input);` także po udanym odczycie. |
| `abc` daje trzy wyniki `invalid_input` | `ignore()` bez argumentów zabiera tylko jeden znak. | Użyj pełnej postaci z `std::numeric_limits<std::streamsize>::max()` i `'\n'`. |
| `3.5` jest przyjęte jako 3 | Tak działa ta funkcja: odczytuje liczbę z początku wpisu, a resztę wiersza odrzuca (punkt 4). | To zamierzone. Ścisłe sprawdzanie całego wpisu nie jest częścią tej lekcji. |
| Pusty wiersz nie daje żadnego komunikatu | `std::ws` pomija puste wiersze, więc nie są próbami. | To zamierzone. |
| Błąd z `use of undeclared identifier 'ws'; did you mean 'std::ws'?` | Brakuje `std::` przed `ws`. | Zapisz `input >> std::ws;`. |
| Ostrzeżenie z `enumeration value '…' not handled in switch` | W `switch` brakuje etykiety dla jednego z czterech wyników (lekcja 14.2). | Dopisz etykietę. |

## 10. Wyjaśnij

Odpowiedz własnymi słowami, najlepiej na piśmie. Dopiero potem porównaj z przykładowymi odpowiedziami.

1. Co naprawia `clear()`, a czego nie naprawia?
2. Dlaczego po nieudanym odczycie potrzebne są i `clear()`, i odrzucenie reszty wiersza? Co się dzieje, gdy zabraknie jednego z nich?
3. Co znaczy `std::numeric_limits<std::streamsize>::max()` w wywołaniu `ignore` i dlaczego nie wystarczy `ignore()` bez argumentów?
4. Czym różni się `input >> std::ws` od odrzucenia reszty wiersza?
5. Dlaczego funkcja rozpoznaje koniec danych przed odczytem liczby, a nie po nim?
6. Dane kończą się na `4` bez znaku końca wiersza. Dlaczego to nie jest błąd i co zwrócą dwa kolejne wywołania?
7. Dane kończą się na `abc` bez znaku końca wiersza. Dlaczego funkcja zgłasza `invalid_input`, a nie od razu `end_of_input`?
8. Dlaczego `12abc` daje `out_of_range`, a `3.5` daje `accepted`? Czy funkcja sprawdza cały wpis?
9. Dlaczego liczba za duża dla `int` daje `invalid_input`, a nie `out_of_range`?
10. Dlaczego funkcja czyta do zmiennej lokalnej, a scenariusz testowy zaczyna od −1, a nie od 0?
11. Dlaczego każdy scenariusz testowy ma własny strumień, a kolejne wywołania w scenariuszu korzystają z tego samego?
12. W misji odczyt prosto do `result` nie zmienił żadnego licznika. Dlaczego testy liczników tego nie wykryły i co to wykryło?

<details>
<summary>Przykładowe odpowiedzi</summary>

1. Naprawia stan strumienia: zdejmuje znacznik nieudanego odczytu, więc kolejne odczyty znowu mogą się udać. Nie usuwa żadnego znaku, nie tworzy danych i nie zmienia żadnej zmiennej. Błędny tekst nadal czeka w wejściu.
2. Bo są dwie przeszkody: stan błędu i błędny tekst. Bez `clear()` strumień zostaje w stanie błędu, a `ignore` niczego nie zabiera, więc każdy odczyt od razu się nie udaje. Bez odrzucenia reszty wiersza stan jest zwykły, ale następny odczyt trafia na ten sam tekst. W obu przypadkach program w pętli powtarzałby ten sam komunikat bez końca.
3. To największa wartość typu, którego biblioteka używa do liczenia znaków. Dla `ignore` ta wartość oznacza brak limitu, więc `ignore` zabiera znaki aż do końca wiersza albo do końca danych. `ignore()` bez argumentów zabiera jeden znak: po `abc` zostaje `bc` i kolejne próby trafiają na kolejne litery.
4. `std::ws` usuwa tylko białe znaki przed wpisem, także puste wiersze, i zatrzymuje się na pierwszym innym znaku. Odrzucenie reszty wiersza usuwa wszystkie znaki do końca bieżącego wiersza, także błędny tekst. `std::ws` stoi na początku każdej próby, a odrzucenie reszty wiersza po każdej próbie, która znalazła wpis.
5. Bo po odczycie `eof()` nie mówi, czy odczyt się udał. Udany odczyt ostatniej liczby bez znaku końca wiersza też dochodzi do końca danych, a nieudany odczyt, który doszedł do końca, wygląda tak samo jak brak danych. Przed odczytem, po `std::ws`, `eof()` odpowiada na jedno pytanie: czy jest jeszcze jakiś wpis.
6. Bo `>>` odczytuje 4 i dopiero przy tym dochodzi do końca danych. `fail()` daje `false`, więc odczyt się udał, a `eof()` tylko mówi, że dalej nic nie ma. Pierwsze wywołanie zwraca `accepted` z wartością 4, następne `end_of_input`, kolejne znowu `end_of_input`.
7. Bo `abc` to wpis, tylko błędny. Odczyt liczby zatrzymuje się na `a` i nie dochodzi do końca danych, więc funkcja odzyskuje strumień i zgłasza `invalid_input`. Dopiero odrzucenie reszty wiersza dochodzi do końca. Gdyby funkcja od razu zgłosiła koniec danych, ostatni błędny wpis by zniknął i nikt by się o nim nie dowiedział.
8. Bo funkcja odczytuje liczbę z początku wpisu i resztę wiersza odrzuca bez sprawdzania. Z `12abc` odczytuje 12, a to jest poza zakresem 1–6. Z `3.5` odczytuje 3 i odrzuca `.5`. Funkcja nie sprawdza, czy cały wpis jest zapisem jednej liczby.
9. Bo odczyt takiej liczby się nie udaje. `out_of_range` oznacza, że odczytana liczba jest znana, tylko leży poza zakresem. Liczby za dużej dla `int` funkcja w ogóle nie dostaje, więc nie może ocenić jej zakresu.
10. Bo nieudany odczyt może zapisać do zmiennej inną wartość, a odczyt liczby spoza zakresu zapisuje tę liczbę. Zmienna lokalna chroni `result`, który ma się zmienić tylko przy `accepted`. Start od −1 sprawia, że każda zmiana po odmowie jest widoczna. Przy 0 zmiana na 0 po nieudanym odczycie, na przykład w wariancie z misji, przeszłaby niezauważona.
11. Bo scenariusze są od siebie niezależne: każdy zaczyna od swoich danych, a wynik jednego nie może zależeć od tego, co zrobił poprzedni. Wewnątrz scenariusza wywołania nie są niezależne: sprawdzają, czy po każdym wpisie strumień jest gotowy na następny. Dlatego korzystają z tego samego strumienia, tak jak program czytający kolejne wpisy.
12. Bo liczniki zależą tylko od nazwanych wyników, a do sumy trafiają tylko przyjęte oceny. Wyniki były poprawne i przyjęte oceny też. Zmiana dotyczyła tylko oceny po odmowach, której `count_ratings` nie używa. Wykryły to sprawdzenia oceny w scenariuszach odczytu, które wywołują `read_number` bezpośrednio.

</details>

## Podsumowanie

- Po nieudanym odczycie są dwie przeszkody: stan błędu i błędny tekst. **`clear()` naprawia stan, a `ignore` usuwa znaki.** Potrzebne są obie operacje, najpierw `clear()`.
- `input.ignore(std::numeric_limits<std::streamsize>::max(), '\n');` odrzuca pozostałe znaki aż do końca wiersza albo do końca danych. Wymaga `#include <limits>`.
- **Koniec danych rozpoznajesz przed odczytem liczby:** `input >> std::ws;` pomija białe znaki i puste wiersze, a `eof()` mówi, czy jest jeszcze jakiś wpis. Po odczycie liczby sprawdzasz tylko, czy się udał. Ostatnia liczba bez znaku końca wiersza jest przyjęta, a ostatni błędny wpis bez niego jest zgłoszony.
- Funkcja `read_number` zwraca jeden z czterech nazwanych wyników, sama odzyskuje strumień i zmienia `result` tylko przy `accepted`. Odczytuje liczbę z początku wpisu, a resztę wiersza odrzuca bez sprawdzania. Liczba za duża dla `int` to `invalid_input`.
- Awaria źródła danych to nie koniec danych. Funkcja zakłada sprawne źródło, a przy awarii przestaje czytać, bez odzyskiwania.
- Testy sekwencji: każdy scenariusz ma nowy strumień, a w scenariuszu kolejne wywołania korzystają z tego samego. Po każdym wywołaniu sprawdzasz wynik i wartość zmiennej wynikowej, a zmienna zaczyna od wartości, której żaden poprawny odczyt nie da.

## Co dalej

To była ostatnia lekcja Modułu 14 z nowymi umiejętnościami. Planowana lekcja 14.5 to sprawdzian modułu: program stacji pomiarowej, w którym połączysz nazwane stany, `switch`, nazwane wyniki i odczyt odzyskujący strumień. Ta lekcja jest w przygotowaniu.

---

## Przykładowe rozwiązania

Zajrzyj tutaj **po własnej próbie**. Twoje nazwy sprawdzeń, nazwy zmiennych, wybór scenariuszy i ich kolejność mogą się różnić, jeśli spełniają kontrakt i listę kontrolną.

<details>
<summary>Punkt 8: misja, oceny w ankiecie</summary>

**`count_ratings`:** pętla działa, dopóki nie przyjdzie `end_of_input`. Każdy wynik obsługuje osobna etykieta `case`, zakończona przez `break`. Do sumy trafia ocena tylko w etykiecie `accepted`. `end_of_input` ustawia flagę `input_ended` i niczego nie liczy. Ocena trafia do zmiennej `rating`, którą zmienia wyłącznie `read_number`, i to tylko przy `accepted`.

**Scenariusze:** program referencyjny ma trzy scenariusze odczytu, R1–R3, z 10 wywołaniami po 2 sprawdzenia, czyli 20, i dwa scenariusze liczenia, C1 i C2, po 4 sprawdzenia, czyli 8. Razem 28.

**Przewidywanie:** przy odczycie prosto do `result` nazwane wyniki się nie zmieniają, ale ocena po odmowach tak. Po nieudanym odczycie standard C++ wymaga zapisania w zmiennej 0, a po odczycie liczby spoza zakresu zostaje w niej ta liczba. `FAIL` wypiszą sprawdzenia oceny w R1 po `abc`, w R2 po `0` i po `6` oraz w R3 po `xyz` i po końcu danych. Scenariusze liczenia przejdą.

**`main.cpp`:**

<!-- example: survey_tests -->
```cpp
#include <iostream>
#include <limits>
#include <sstream>
#include <string>

enum class ReadResult {
    accepted,
    out_of_range,
    invalid_input,
    end_of_input
};

void discard_rest_of_line(std::istream& input) {
    input.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
}

ReadResult read_number(std::istream& input, int minimum, int maximum, int& result) {
    if (input.bad()) {
        return ReadResult::end_of_input;
    }

    input >> std::ws;

    if (input.eof()) {
        return ReadResult::end_of_input;
    }

    int value{0};
    input >> value;

    if (input.fail()) {
        if (input.bad()) {
            return ReadResult::end_of_input;
        }

        input.clear();
        discard_rest_of_line(input);
        return ReadResult::invalid_input;
    }

    discard_rest_of_line(input);

    if (value < minimum || value > maximum) {
        return ReadResult::out_of_range;
    }

    result = value;
    return ReadResult::accepted;
}

std::string read_result_text(ReadResult result) {
    switch (result) {
        case ReadResult::accepted:
            return "accepted";
        case ReadResult::out_of_range:
            return "out_of_range";
        case ReadResult::invalid_input:
            return "invalid_input";
        case ReadResult::end_of_input:
            return "end_of_input";
    }

    return "unknown";
}

struct SurveyCounts {
    int accepted;
    int out_of_range;
    int invalid_input;
    int sum;
};

SurveyCounts count_ratings(std::istream& input) {
    SurveyCounts counts{0, 0, 0, 0};
    int rating{0};
    bool input_ended{false};

    while (!input_ended) {
        const ReadResult result{read_number(input, 1, 5, rating)};

        switch (result) {
            case ReadResult::accepted:
                ++counts.accepted;
                counts.sum += rating;
                break;
            case ReadResult::out_of_range:
                ++counts.out_of_range;
                break;
            case ReadResult::invalid_input:
                ++counts.invalid_input;
                break;
            case ReadResult::end_of_input:
                input_ended = true;
                break;
        }
    }

    return counts;
}

void check_read_result(const std::string& name, ReadResult expected, ReadResult actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << read_result_text(expected) << ", actual " << read_result_text(actual) << "\n";
        ++failed;
    }
}

void check_int(const std::string& name, int expected, int actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << expected << ", actual " << actual << "\n";
        ++failed;
    }
}

int main() {
    int checks{0};
    int failed{0};

    std::istringstream input_r1{"abc\n4\n"};
    int rating_r1{-1};
    check_read_result("R1 call 1 result", ReadResult::invalid_input, read_number(input_r1, 1, 5, rating_r1), checks, failed);
    check_int("R1 call 1 rating", -1, rating_r1, checks, failed);
    check_read_result("R1 call 2 result", ReadResult::accepted, read_number(input_r1, 1, 5, rating_r1), checks, failed);
    check_int("R1 call 2 rating", 4, rating_r1, checks, failed);
    check_read_result("R1 call 3 result", ReadResult::end_of_input, read_number(input_r1, 1, 5, rating_r1), checks, failed);
    check_int("R1 call 3 rating", 4, rating_r1, checks, failed);

    std::istringstream input_r2{"0\n6\n1"};
    int rating_r2{-1};
    check_read_result("R2 call 1 result", ReadResult::out_of_range, read_number(input_r2, 1, 5, rating_r2), checks, failed);
    check_int("R2 call 1 rating", -1, rating_r2, checks, failed);
    check_read_result("R2 call 2 result", ReadResult::out_of_range, read_number(input_r2, 1, 5, rating_r2), checks, failed);
    check_int("R2 call 2 rating", -1, rating_r2, checks, failed);
    check_read_result("R2 call 3 result", ReadResult::accepted, read_number(input_r2, 1, 5, rating_r2), checks, failed);
    check_int("R2 call 3 rating", 1, rating_r2, checks, failed);
    check_read_result("R2 call 4 result", ReadResult::end_of_input, read_number(input_r2, 1, 5, rating_r2), checks, failed);
    check_int("R2 call 4 rating", 1, rating_r2, checks, failed);

    std::istringstream input_r3{"2\nxyz"};
    int rating_r3{-1};
    check_read_result("R3 call 1 result", ReadResult::accepted, read_number(input_r3, 1, 5, rating_r3), checks, failed);
    check_int("R3 call 1 rating", 2, rating_r3, checks, failed);
    check_read_result("R3 call 2 result", ReadResult::invalid_input, read_number(input_r3, 1, 5, rating_r3), checks, failed);
    check_int("R3 call 2 rating", 2, rating_r3, checks, failed);
    check_read_result("R3 call 3 result", ReadResult::end_of_input, read_number(input_r3, 1, 5, rating_r3), checks, failed);
    check_int("R3 call 3 rating", 2, rating_r3, checks, failed);

    std::istringstream input_c1{"5\n\nabc\nxyz\n0\n3 stars\n4"};
    const SurveyCounts counts_c1{count_ratings(input_c1)};
    check_int("C1 accepted", 3, counts_c1.accepted, checks, failed);
    check_int("C1 out_of_range", 1, counts_c1.out_of_range, checks, failed);
    check_int("C1 invalid_input", 2, counts_c1.invalid_input, checks, failed);
    check_int("C1 sum", 12, counts_c1.sum, checks, failed);

    std::istringstream input_c2{""};
    const SurveyCounts counts_c2{count_ratings(input_c2)};
    check_int("C2 accepted", 0, counts_c2.accepted, checks, failed);
    check_int("C2 out_of_range", 0, counts_c2.out_of_range, checks, failed);
    check_int("C2 invalid_input", 0, counts_c2.invalid_input, checks, failed);
    check_int("C2 sum", 0, counts_c2.sum, checks, failed);

    std::cout << "Checks: " << checks << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }
}
```

<!-- output: survey_tests -->
```text
PASS R1 call 1 result
PASS R1 call 1 rating
PASS R1 call 2 result
PASS R1 call 2 rating
PASS R1 call 3 result
PASS R1 call 3 rating
PASS R2 call 1 result
PASS R2 call 1 rating
PASS R2 call 2 result
PASS R2 call 2 rating
PASS R2 call 3 result
PASS R2 call 3 rating
PASS R2 call 4 result
PASS R2 call 4 rating
PASS R3 call 1 result
PASS R3 call 1 rating
PASS R3 call 2 result
PASS R3 call 2 rating
PASS R3 call 3 result
PASS R3 call 3 rating
PASS C1 accepted
PASS C1 out_of_range
PASS C1 invalid_input
PASS C1 sum
PASS C2 accepted
PASS C2 out_of_range
PASS C2 invalid_input
PASS C2 sum
Checks: 28, failed: 0
```

Kod zakończenia: 0.

**Celowa usterka:** odczyt prosto do `result`, bez innych zmian:

<!-- fragment -->
```cpp
input >> result;
```

<!-- example: survey_tests_direct_read exit=1 -->
```cpp
#include <iostream>
#include <limits>
#include <sstream>
#include <string>

enum class ReadResult {
    accepted,
    out_of_range,
    invalid_input,
    end_of_input
};

void discard_rest_of_line(std::istream& input) {
    input.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
}

ReadResult read_number(std::istream& input, int minimum, int maximum, int& result) {
    if (input.bad()) {
        return ReadResult::end_of_input;
    }

    input >> std::ws;

    if (input.eof()) {
        return ReadResult::end_of_input;
    }

    input >> result;

    if (input.fail()) {
        if (input.bad()) {
            return ReadResult::end_of_input;
        }

        input.clear();
        discard_rest_of_line(input);
        return ReadResult::invalid_input;
    }

    discard_rest_of_line(input);

    if (result < minimum || result > maximum) {
        return ReadResult::out_of_range;
    }

    return ReadResult::accepted;
}

std::string read_result_text(ReadResult result) {
    switch (result) {
        case ReadResult::accepted:
            return "accepted";
        case ReadResult::out_of_range:
            return "out_of_range";
        case ReadResult::invalid_input:
            return "invalid_input";
        case ReadResult::end_of_input:
            return "end_of_input";
    }

    return "unknown";
}

struct SurveyCounts {
    int accepted;
    int out_of_range;
    int invalid_input;
    int sum;
};

SurveyCounts count_ratings(std::istream& input) {
    SurveyCounts counts{0, 0, 0, 0};
    int rating{0};
    bool input_ended{false};

    while (!input_ended) {
        const ReadResult result{read_number(input, 1, 5, rating)};

        switch (result) {
            case ReadResult::accepted:
                ++counts.accepted;
                counts.sum += rating;
                break;
            case ReadResult::out_of_range:
                ++counts.out_of_range;
                break;
            case ReadResult::invalid_input:
                ++counts.invalid_input;
                break;
            case ReadResult::end_of_input:
                input_ended = true;
                break;
        }
    }

    return counts;
}

void check_read_result(const std::string& name, ReadResult expected, ReadResult actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << read_result_text(expected) << ", actual " << read_result_text(actual) << "\n";
        ++failed;
    }
}

void check_int(const std::string& name, int expected, int actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << expected << ", actual " << actual << "\n";
        ++failed;
    }
}

int main() {
    int checks{0};
    int failed{0};

    std::istringstream input_r1{"abc\n4\n"};
    int rating_r1{-1};
    check_read_result("R1 call 1 result", ReadResult::invalid_input, read_number(input_r1, 1, 5, rating_r1), checks, failed);
    check_int("R1 call 1 rating", -1, rating_r1, checks, failed);
    check_read_result("R1 call 2 result", ReadResult::accepted, read_number(input_r1, 1, 5, rating_r1), checks, failed);
    check_int("R1 call 2 rating", 4, rating_r1, checks, failed);
    check_read_result("R1 call 3 result", ReadResult::end_of_input, read_number(input_r1, 1, 5, rating_r1), checks, failed);
    check_int("R1 call 3 rating", 4, rating_r1, checks, failed);

    std::istringstream input_r2{"0\n6\n1"};
    int rating_r2{-1};
    check_read_result("R2 call 1 result", ReadResult::out_of_range, read_number(input_r2, 1, 5, rating_r2), checks, failed);
    check_int("R2 call 1 rating", -1, rating_r2, checks, failed);
    check_read_result("R2 call 2 result", ReadResult::out_of_range, read_number(input_r2, 1, 5, rating_r2), checks, failed);
    check_int("R2 call 2 rating", -1, rating_r2, checks, failed);
    check_read_result("R2 call 3 result", ReadResult::accepted, read_number(input_r2, 1, 5, rating_r2), checks, failed);
    check_int("R2 call 3 rating", 1, rating_r2, checks, failed);
    check_read_result("R2 call 4 result", ReadResult::end_of_input, read_number(input_r2, 1, 5, rating_r2), checks, failed);
    check_int("R2 call 4 rating", 1, rating_r2, checks, failed);

    std::istringstream input_r3{"2\nxyz"};
    int rating_r3{-1};
    check_read_result("R3 call 1 result", ReadResult::accepted, read_number(input_r3, 1, 5, rating_r3), checks, failed);
    check_int("R3 call 1 rating", 2, rating_r3, checks, failed);
    check_read_result("R3 call 2 result", ReadResult::invalid_input, read_number(input_r3, 1, 5, rating_r3), checks, failed);
    check_int("R3 call 2 rating", 2, rating_r3, checks, failed);
    check_read_result("R3 call 3 result", ReadResult::end_of_input, read_number(input_r3, 1, 5, rating_r3), checks, failed);
    check_int("R3 call 3 rating", 2, rating_r3, checks, failed);

    std::istringstream input_c1{"5\n\nabc\nxyz\n0\n3 stars\n4"};
    const SurveyCounts counts_c1{count_ratings(input_c1)};
    check_int("C1 accepted", 3, counts_c1.accepted, checks, failed);
    check_int("C1 out_of_range", 1, counts_c1.out_of_range, checks, failed);
    check_int("C1 invalid_input", 2, counts_c1.invalid_input, checks, failed);
    check_int("C1 sum", 12, counts_c1.sum, checks, failed);

    std::istringstream input_c2{""};
    const SurveyCounts counts_c2{count_ratings(input_c2)};
    check_int("C2 accepted", 0, counts_c2.accepted, checks, failed);
    check_int("C2 out_of_range", 0, counts_c2.out_of_range, checks, failed);
    check_int("C2 invalid_input", 0, counts_c2.invalid_input, checks, failed);
    check_int("C2 sum", 0, counts_c2.sum, checks, failed);

    std::cout << "Checks: " << checks << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }
}
```

<!-- output: survey_tests_direct_read -->
```text
PASS R1 call 1 result
FAIL R1 call 1 rating: expected -1, actual 0
PASS R1 call 2 result
PASS R1 call 2 rating
PASS R1 call 3 result
PASS R1 call 3 rating
PASS R2 call 1 result
FAIL R2 call 1 rating: expected -1, actual 0
PASS R2 call 2 result
FAIL R2 call 2 rating: expected -1, actual 6
PASS R2 call 3 result
PASS R2 call 3 rating
PASS R2 call 4 result
PASS R2 call 4 rating
PASS R3 call 1 result
PASS R3 call 1 rating
PASS R3 call 2 result
FAIL R3 call 2 rating: expected 2, actual 0
PASS R3 call 3 result
FAIL R3 call 3 rating: expected 2, actual 0
PASS C1 accepted
PASS C1 out_of_range
PASS C1 invalid_input
PASS C1 sum
PASS C2 accepted
PASS C2 out_of_range
PASS C2 invalid_input
PASS C2 sum
Checks: 28, failed: 5
```

Kod zakończenia: 1.

| Scenariusz | Wywołanie | Wynik | Ocena oczekiwana | Ocena rzeczywista |
|---|---|---|---:|---:|
| R1 | 1: `abc` | `invalid_input`, poprawny | −1 | 0 |
| R2 | 1: `0` | `out_of_range`, poprawny | −1 | 0 |
| R2 | 2: `6` | `out_of_range`, poprawny | −1 | 6 |
| R3 | 2: `xyz` | `invalid_input`, poprawny | 2 | 0 |
| R3 | 3: koniec danych | `end_of_input`, poprawny | 2 | 0 |
| C1, C2 | wszystkie | liczniki poprawne | — | — |

- **Każdy nazwany wynik jest poprawny,** a mimo to funkcja łamie kontrakt: po odmowie zmienia `result`. To ta sama lekcja co w 14.3: poprawny wynik nie gwarantuje poprawnego stanu.
- **Scenariusze liczenia tego nie widzą.** Liczniki zależą tylko od wyników, a do sumy trafiają tylko przyjęte oceny, które są poprawne. Usterkę wykrywają sprawdzenia oceny w scenariuszach, które wywołują `read_number` bezpośrednio.
- **Ostatni `FAIL` w R3** pokazuje skutek wcześniejszego błędu: `end_of_input` niczego nie zmienia, więc 0 zostaje z poprzedniego wywołania.
- **Kod 1** wynika z pięciu rzeczywistych linijek `FAIL`.

**Po naprawie:** po przywróceniu zmiennej lokalnej program jest znów taki jak pierwsza wersja. Te same 28 sprawdzeń wypisuje `PASS` i `Checks: 28, failed: 0`, a kod zakończenia wynosi 0. Wyniki oczekiwane się nie zmieniły.

**Nieobowiązkowo: raport z klawiatury.** Ten sam `count_ratings` czyta z `std::cin`:

<!-- example: survey_report -->
```cpp
#include <iostream>
#include <limits>

enum class ReadResult {
    accepted,
    out_of_range,
    invalid_input,
    end_of_input
};

void discard_rest_of_line(std::istream& input) {
    input.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
}

ReadResult read_number(std::istream& input, int minimum, int maximum, int& result) {
    if (input.bad()) {
        return ReadResult::end_of_input;
    }

    input >> std::ws;

    if (input.eof()) {
        return ReadResult::end_of_input;
    }

    int value{0};
    input >> value;

    if (input.fail()) {
        if (input.bad()) {
            return ReadResult::end_of_input;
        }

        input.clear();
        discard_rest_of_line(input);
        return ReadResult::invalid_input;
    }

    discard_rest_of_line(input);

    if (value < minimum || value > maximum) {
        return ReadResult::out_of_range;
    }

    result = value;
    return ReadResult::accepted;
}

struct SurveyCounts {
    int accepted;
    int out_of_range;
    int invalid_input;
    int sum;
};

SurveyCounts count_ratings(std::istream& input) {
    SurveyCounts counts{0, 0, 0, 0};
    int rating{0};
    bool input_ended{false};

    while (!input_ended) {
        const ReadResult result{read_number(input, 1, 5, rating)};

        switch (result) {
            case ReadResult::accepted:
                ++counts.accepted;
                counts.sum += rating;
                break;
            case ReadResult::out_of_range:
                ++counts.out_of_range;
                break;
            case ReadResult::invalid_input:
                ++counts.invalid_input;
                break;
            case ReadResult::end_of_input:
                input_ended = true;
                break;
        }
    }

    return counts;
}

int main() {
    std::cout << "Enter ratings from 1 to 5, one per line:\n";
    const SurveyCounts counts{count_ratings(std::cin)};

    std::cout << "Ratings: " << counts.accepted << "\n";
    std::cout << "Sum: " << counts.sum << "\n";
    std::cout << "Out of range: " << counts.out_of_range << "\n";
    std::cout << "Invalid entries: " << counts.invalid_input << "\n";
}
```

<!-- input: survey_report -->
```text
5
3
abc
9

4
```

<!-- output: survey_report -->
```text
Enter ratings from 1 to 5, one per line:
Ratings: 3
Sum: 12
Out of range: 1
Invalid entries: 1
```

Pusty wiersz nie jest liczony, `abc` to błędny wpis, a `9` jest poza skalą.

**Samoocena.** Porównaj swoją pracę z listą kontrolną w punkcie 8. Szczególnie sprawdź:
- czy Twoja tabela powstała przed kodem i ma wszystkie wymagane rodzaje scenariuszy, w tym ostatnią ocenę i ostatni błędny wpis bez znaku końca wiersza;
- czy każdy scenariusz ma własny strumień, a kolejne wywołania w scenariuszu korzystają z tego samego;
- czy po każdym wywołaniu `read_number` sprawdzasz i wynik, i ocenę;
- czy koniec danych kończy pętlę i nie zwiększa żadnego licznika;
- czy Twoje przewidywanie z kroku 1 zgadzało się z wynikiem kroku 5, a jeśli nie, czy umiesz wyjaśnić różnicę.

Jeśli w jednym z tych punktów odpowiedź brzmi „nie”, wróć do odpowiedniego punktu lekcji, zanim przejdziesz dalej.

</details>

**Poprzednia lekcja:** [Lekcja 14.3: Funkcja mówi, dlaczego odmówiła](lesson_03_function_explains_refusal.md) · **Następna lekcja:** 14.5, w przygotowaniu · [Opis kursu](../../README.md)

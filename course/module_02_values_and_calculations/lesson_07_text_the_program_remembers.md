# Lekcja 2.7: Tekst, który program pamięta (`std::string`)

**Polski** · [English](lesson_07_text_the_program_remembers.en.md) · [Opis kursu](../../README.md)

> **Moduł 2, lekcja 7** · około 60–75 minut
> **Potrzebujesz:** katalogu `cpp-workspace` i oryginalnego projektu `lesson_05_first_program`, jak dotąd. Debugger nie jest w tej lekcji potrzebny.
> **Wersja pilotażowa.** Programy z tej lekcji sprawdzamy automatycznie na Windowsie, Ubuntu i macOS, także z podanymi danymi wejściowymi.

## Zanim zaczniesz

Ta lekcja zakłada, że po lekcjach 2.1–2.6:

- tworzysz zmienne i stałe z wartością początkową w `{}` i zmieniasz zmienne przypisaniem;
- odczytujesz liczby przez `std::cin >>` i uruchamiasz ten sam program z różnymi danymi;
- odróżniasz dane wejściowe od standardowego wyjścia programu (lekcja 2.6, punkt 6).

## Sytuacja

Twoje programy pamiętają i liczą już liczby. Tekst pojawiał się w nich tylko jako napis w cudzysłowie, wypisywany od razu przez `std::cout`. Dziś program zacznie **przechowywać tekst w zmiennej**: zmieniać go, łączyć z innym tekstem i odczytywać od użytkownika, także całe linijki ze spacjami.

Po tej lekcji będziesz:

- wyjaśniać, do czego służy `std::string`, i odróżniać literał tekstowy od zmiennej z tekstem;
- tworzyć zmienne i stałe typu `std::string`, wypisywać je i zmieniać przypisaniem;
- łączyć teksty operatorem `+` i odróżniać to od wypisywania kilku wartości przez `<<`;
- odczytywać jedno słowo przez `std::cin >>` i całą linijkę przez `std::getline`;
- samodzielnie pisać program, którego komunikaty zależą od wpisanego tekstu.

## 1. Przygotuj projekt

W `cpp-workspace` utwórz katalog `lesson_2_7` i skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program`. Programy z punktów 2–7 wpisujesz w `main.cpp` tego katalogu.

## 2. Tekst jako wartość

Od Modułu 1 wypisujesz tekst wprost: `std::cout << "Hello!\n";`. Teraz zapisz tekst w zmiennej:

<!-- example: text_variable -->
```cpp
#include <iostream>
#include <string>

int main() {
    std::string greeting{"Hello!"};
    std::string event_name{"Science Fair"};

    std::cout << greeting << "\n";
    std::cout << "Event: " << event_name << "\n";
}
```

<!-- output: text_variable -->
```text
Hello!
Event: Science Fair
```

- `"Hello!"` to **literał tekstowy**: tekst zapisany wprost w kodzie, w cudzysłowie, jak w Module 1.
- `std::string` to **typ z biblioteki standardowej**, który przechowuje tekst. `greeting` to zmienna tego typu, a `{"Hello!"}` daje jej wartość początkową, tak jak `{3}` zmiennej `int`.
- Literał i zmienna to dwie różne rzeczy, choć tu zawierają ten sam tekst. Literał jest stałym kawałkiem kodu. Zmienna typu `std::string` przechowuje tekst, który program może zmieniać, łączyć z innym i odczytywać od użytkownika.
- Tekst w `std::string` może zawierać spacje, jak `Science Fair`.
- `std::cout` wypisuje tekst ze zmiennej tak samo jak liczbę.
- Typ `std::string` wymaga nagłówka **`#include <string>`**. Programy, które wypisują albo czytają, potrzebują też `#include <iostream>`, jak dotąd. Czasem program się zbuduje bez `#include <string>`, bo inny nagłówek dołączy go po drodze. Nie polegaj na tym: jeśli używasz `std::string`, dopisz `#include <string>`.

`std::string` potrafi więcej niż `int` i `double`, bo tekst może mieć dowolną długość. Na razie potrzebujesz tylko tego, co w tej lekcji.

## 3. Zmień tekst

Przypisanie z lekcji 2.2 działa także dla tekstu:

<!-- example: status_change -->
```cpp
#include <iostream>
#include <string>

int main() {
    const std::string application_name{"My App"};
    std::string status{"Waiting"};

    std::cout << application_name << ": " << status << "\n";
    status = "Ready";
    std::cout << application_name << ": " << status << "\n";
}
```

**Przewidź** obie linijki wyniku, a potem uruchom program.

<details>
<summary>Wynik programu</summary>

<!-- output: status_change -->
```text
My App: Waiting
My App: Ready
```

</details>

- `status = "Ready";` zastępuje poprzedni tekst nowym, tak jak przypisanie zastępuje liczbę. Pierwsze `std::cout` stoi przed przypisaniem, więc wypisuje starą wartość.
- `application_name` ma `const`, bo nazwa programu nie powinna się zmieniać. Zasada z lekcji 2.2 obowiązuje także dla tekstu. `greeting` z punktu 2 też mógłby mieć `const`.

## 4. Połącz teksty

Operator `+` potrafi **łączyć teksty**:

<!-- example: join_text -->
```cpp
#include <iostream>
#include <string>

int main() {
    const std::string greeting{"Hello, "};
    const std::string name{"Ada"};

    const std::string message{greeting + name};

    std::cout << message << "\n";
    std::cout << greeting << name << "\n";
}
```

**Przewidź**, jaką wartość ma `message` i co wypiszą obie linijki z `std::cout`.

<details>
<summary>Wynik programu</summary>

<!-- output: join_text -->
```text
Hello, Ada
Hello, Ada
```

</details>

- `greeting + name` tworzy **nowy tekst**: `Hello, ` i zaraz za nim `Ada`. Spacja jest na końcu `greeting`, więc trafia między słowa. `+` niczego nie dodaje do siebie arytmetycznie, tylko dokleja jeden tekst do drugiego.
- **Znaczenie operatora zależy od typów operandów**, jak w lekcji 2.5: dla liczb `+` dodaje, a dla dwóch wartości `std::string` łączy.
- Wynik jest zapisany w nowej stałej `message`. Można go potem wypisać, jak każdą wartość.
- Obie linijki wyglądają na ekranie tak samo, ale program robi co innego:
  - `std::cout << message` wypisuje **jeden, wcześniej zbudowany tekst**;
  - `std::cout << greeting << name` wysyła na wyjście **dwa teksty po kolei**, jeden za drugim. Żaden nowy tekst przy tym nie powstaje.
- `<<` nie łączy więc tekstów tak jak `+`. Gdy tekst ma tylko trafić na ekran, wystarczy `<<`. Gdy chcesz go przechować albo użyć dalej, zbuduj go przez `+`.

**Literały i `+`.** W `greeting + name` oba operandy są typu `std::string`. Do `std::string` można też dokleić literał, na przykład `greeting + "!"`. Ale `"Hello, " + "Ada"` nie łączy dwóch wartości `std::string`, bo literał nie jest wartością typu `std::string`. Dlatego **w każdym `+` przynajmniej jeden operand musi być typu `std::string`**. W dłuższym wyrażeniu ta zasada dotyczy każdego `+` osobno, od lewej do prawej, jak w lekcjach 2.4 i 2.5.

## 5. Przewidź: co odczyta `std::cin >>`?

Tekst można odczytać ze standardowego wejścia tak samo jak liczbę:

<!-- example: read_one_word -->
```cpp
#include <iostream>
#include <string>

int main() {
    std::string name{""};

    std::cout << "Enter your name:\n";
    std::cin >> name;
    std::cout << "Name: " << name << "\n";
}
```

`{""}` to pusty tekst: wartość początkowa, którą odczyt zastąpi. Zmienna na dane nie jest `const`, jak w lekcji 2.6.

**Przewidź**, co wypisze program, gdy wpiszesz `Ola Nowak`. Zapisz odpowiedź, a potem uruchom program.

<!-- input: read_one_word -->
```text
Ola Nowak
```

<details>
<summary>Standardowe wyjście programu</summary>

<!-- output: read_one_word -->
```text
Enter your name:
Name: Ola
```

</details>

- `>>` odczytuje do `std::string` **jedno słowo**: pomija odstępy przed nim, a **spacja kończy odczyt**. Do `name` trafia więc `Ola`.
- Reszta, ` Nowak`, nie zniknęła. Została w standardowym wejściu, nieodczytana. Ten program po prostu już z niej nie korzysta.
- **To nie znaczy, że `std::string` nie mieści spacji.** `event_name` z punktu 2 przechowuje `Science Fair`. Ograniczenie wynika z **operacji odczytu** `>>`, a nie z typu.

## 6. Cała linijka: `std::getline`

Imię i nazwisko albo nazwa wydarzenia zwykle zawierają spacje. Do odczytania całej linijki służy `std::getline`:

<!-- example: read_full_line -->
```cpp
#include <iostream>
#include <string>

int main() {
    std::string full_name{""};

    std::cout << "Enter your full name:\n";
    std::getline(std::cin, full_name);
    std::cout << "Full name: " << full_name << "\n";
}
```

Uruchom program i wpisz `Ada Lovelace`:

<!-- input: read_full_line -->
```text
Ada Lovelace
```

<!-- output: read_full_line -->
```text
Enter your full name:
Full name: Ada Lovelace
```

Teraz uruchom go jeszcze raz i wpisz to samo co w punkcie 5, `Ola Nowak`. **Przewidź** wynik.

<!-- input: read_full_line -->
```text
Ola Nowak
```

<details>
<summary>Standardowe wyjście programu</summary>

<!-- output: read_full_line -->
```text
Enter your full name:
Full name: Ola Nowak
```

</details>

- `std::getline` to **funkcja z biblioteki standardowej**: gotowa, nazwana operacja, którą wywołujesz, podając w nawiasach, czego ma użyć. Własne funkcje poznasz później. Tutaj tylko korzystasz z gotowej.
- W nawiasach podajesz dwie rzeczy: **skąd czytać** (`std::cin`) i **dokąd zapisać** (`full_name`, zmienna typu `std::string`).
- `std::getline` czyta **do końca linijki**, czyli do miejsca, w którym naciśnięto **Enter**. Spacje są częścią odczytanego tekstu.
- Sam znak końca linijki nie trafia do `full_name`: zmienna przechowuje `Ada Lovelace`, bez niczego na końcu.

To samo wejście `Ola Nowak` dało w punkcie 5 `Ola`, a tutaj `Ola Nowak`. Różnica wynika z **metody odczytu**, nie z danych.

## 7. Ten sam program, inne imię

Program z odczytanego tekstu buduje powitanie:

<!-- example: greeting_message -->
```cpp
#include <iostream>
#include <string>

int main() {
    std::string full_name{""};

    std::cout << "Enter your full name:\n";
    std::getline(std::cin, full_name);

    const std::string message{"Hello, " + full_name + "!"};

    std::cout << message << "\n";
}
```

Uruchom go dwa razy, **bez zmiany kodu**: raz z `Ada Lovelace`, raz z `Grace Hopper`.

<!-- input: greeting_message -->
```text
Ada Lovelace
```

<!-- output: greeting_message -->
```text
Enter your full name:
Hello, Ada Lovelace!
```

<!-- input: greeting_message -->
```text
Grace Hopper
```

<!-- output: greeting_message -->
```text
Enter your full name:
Hello, Grace Hopper!
```

- `"Hello, " + full_name` to literał plus `std::string`, więc wynik jest typu `std::string`. Do niego program dokleja `"!"`. Każdy `+` ma przynajmniej jeden operand typu `std::string` (punkt 4).
- Jak w lekcji 2.6: na ekranie zobaczysz między linijkami programu także wpisane imię i nazwisko. To echo okna, w którym piszesz. Standardowe wyjście to tylko dwie linijki powyżej.

## 8. Uwaga: najpierw `getline`, potem `>>`

Po odczycie przez `std::cin >>` w standardowym wejściu zostaje koniec linijki z wciśniętego **Enter**. Gdyby zaraz potem program wywołał `std::getline`, mógłby odczytać tylko ten pusty koniec linijki i dostać pusty tekst. Jak sobie z tym radzić, poznasz później.

Na razie wystarczy jedna zasada: **jeśli program czyta tekst przez `std::getline` i liczbę przez `>>`, najpierw wywołaj `std::getline`, a dopiero potem `>>`.** Tak jest w misji.

## 9. Misja: identyfikator uczestnika

Napisz program, który przygotowuje prosty identyfikator uczestnika wydarzenia. Użytkownik podaje:

1. imię i nazwisko uczestnika, które może zawierać spacje;
2. numer miejsca, jako liczbę całkowitą.

Program wypisuje imię i nazwisko, numer miejsca i powitanie z imieniem i nazwiskiem.

W `cpp-workspace` utwórz katalog `participant_badge`, skopiuj do niego `CMakeLists.txt` z oryginalnego `lesson_05_first_program`, utwórz pusty `main.cpp` i napisz program samodzielnie.

**Pierwsze uruchomienie:**

<!-- input: participant_badge -->
```text
Ada Lovelace
12
```

Standardowe wyjście ma być dokładnie takie:

<!-- output: participant_badge -->
```text
Enter participant name:
Enter seat number:
Participant: Ada Lovelace
Seat: 12
Welcome, Ada Lovelace!
```

**Drugie uruchomienie tego samego programu,** bez zmiany kodu:

<!-- input: participant_badge -->
```text
Grace Hopper
8
```

<!-- output: participant_badge -->
```text
Enter participant name:
Enter seat number:
Participant: Grace Hopper
Seat: 8
Welcome, Grace Hopper!
```

### Kryterium sukcesu

- Program buduje się jako C++20, a jego standardowe wyjście dla obu zestawów danych jest dokładnie takie jak powyżej.
- Program ma `#include <string>` i `#include <iostream>`.
- Imię i nazwisko trafia do zmiennej `std::string` przez `std::getline`, a numer miejsca do zmiennej `int` przez `std::cin >>`, **w tej kolejności**. Obie zmienne mają wartości początkowe i nie mają `const`.
- Powitanie `Welcome, …!` jest **tekstem zbudowanym przez `+`** i zapisanym w stałej `std::string`.
- W kodzie nie ma `Ada Lovelace`, `Grace Hopper`, 12 ani 8: dane przychodzą ze standardowego wejścia.
- Program używa tylko tego, co już znasz.
- Umiesz wyjaśnić, co w programie jest tekstem, a co liczbą, i dlaczego imię czytasz przez `std::getline`, a nie przez `>>`.

Gdy wynik się zgadza, możesz zapisać projekt w Gicie, jak w lekcji 1.5.

<details>
<summary>Podpowiedź 1</summary>

Kolejność jak w lekcji 2.6: zmienne na dane, potem dla każdej wartości prośba i odczyt, na końcu tekst wynikowy i wypisanie. Która metoda odczytu zachowa spację między imieniem a nazwiskiem?

</details>

<details>
<summary>Podpowiedź 2</summary>

Powitanie to literał `"Welcome, "`, imię i nazwisko i literał `"!"`, połączone przez `+`. Numeru miejsca nie łącz przez `+`: wypisz go przez `<<`, jak każdą liczbę.

</details>

### Wariant: dłuższe imię

Uruchom ten sam program dla uczestniczki o imieniu złożonym z kilku słów. **Przewidź** wynik, zanim go zobaczysz.

<!-- input: participant_badge -->
```text
Mary Ann Evans
3
```

<details>
<summary>Standardowe wyjście programu</summary>

<!-- output: participant_badge -->
```text
Enter participant name:
Enter seat number:
Participant: Mary Ann Evans
Seat: 3
Welcome, Mary Ann Evans!
```

</details>

Program działa bez zmian w kodzie, bo `std::getline` odczytuje całą linijkę, niezależnie od liczby spacji.

Przykładowe rozwiązanie jest w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 10. Gdy coś pójdzie inaczej

| Co widzisz | Co to znaczy | Co zrobić |
|---|---|---|
| Kompilator nie zna `std::string` albo `std::getline` | Brakuje nagłówka. | Dopisz `#include <string>`. Nawet jeśli bez niego program się buduje, nie polegaj na tym. |
| Z `Ada Lovelace` program zapamiętał tylko `Ada` | Tekst odczytano przez `>>`, które czyta jedno słowo. | Do całej linijki użyj `std::getline(std::cin, …)`. |
| Słowa w połączonym tekście są sklejone, na przykład `Hello,Ada` | `+` dokleja teksty dokładnie tak, jak są. Spacja nie pojawia się sama. | Dopisz spację w jednym z tekstów, na przykład `"Hello, "`. |
| Błąd kompilacji przy `+` z dwoma tekstami w cudzysłowie | Dwa literały nie są wartościami `std::string` (punkt 4). | Przynajmniej jeden operand każdego `+` musi być typu `std::string`. Albo wypisz teksty przez `<<`. |
| `std::getline` odczytał pusty tekst, choć wpisano imię | Przed `std::getline` był odczyt przez `>>`, a po nim został koniec linijki (punkt 8). | Najpierw `std::getline`, potem `>>`. |
| Wpisany tekst jest widoczny na ekranie dwa razy albo między linijkami programu | Jedno z wystąpień to echo, a nie wynik programu (lekcja 2.6). | Nic. Standardowe wyjście to tylko to, co wypisuje `std::cout`. |
| Litery z polskimi znakami albo inne znaki spoza podstawowego alfabetu wyświetlają się dziwnie | Wyświetlanie takich znaków zależy od ustawień systemu i konsoli. | W tej lekcji używaj w danych liter bez polskich znaków, na przykład `Lukasz` zamiast `Łukasz`. Pracę z takimi znakami poznasz później. |

## 11. Wyjaśnij

Odpowiedz własnymi słowami, najlepiej na piśmie. Dopiero potem porównaj z przykładową odpowiedzią.

**1.** Czym różni się `"Hello!"` od `greeting` w `std::string greeting{"Hello!"};`?

<details>
<summary>Przykładowa odpowiedź</summary>

`"Hello!"` to literał tekstowy, czyli tekst zapisany wprost w kodzie. `greeting` to zmienna typu `std::string`, która przechowuje kopię tego tekstu jako wartość początkową. Wartość zmiennej można potem zmienić przypisaniem, połączyć z innym tekstem albo wczytać od użytkownika.

</details>

**2.** `std::cout << message` i `std::cout << greeting << name` wypisały to samo. Czym się różnią?

<details>
<summary>Przykładowa odpowiedź</summary>

`message` to jeden tekst zbudowany wcześniej przez `+` i przechowywany w zmiennej. W drugiej instrukcji `<<` wysyła na wyjście dwa osobne teksty, jeden za drugim, i żaden nowy tekst nie powstaje.

</details>

**3.** Dlaczego po wpisaniu `Ola Nowak` program z punktu 5 zapamiętał tylko `Ola`? Czy to znaczy, że `std::string` nie mieści spacji?

<details>
<summary>Przykładowa odpowiedź</summary>

Bo `>>` odczytuje do `std::string` jedno słowo i kończy na spacji. `std::string` mieści spacje: `event_name` przechowuje `Science Fair`, a `std::getline` odczytuje `Ola Nowak` w całości. Ograniczenie wynika z metody odczytu.

</details>

**4.** Co robi `std::getline(std::cin, full_name);`?

<details>
<summary>Przykładowa odpowiedź</summary>

Odczytuje ze standardowego wejścia całą linijkę, aż do końca linijki, razem ze spacjami, i zapisuje ją w `full_name`. Sam znak końca linijki nie trafia do zmiennej.

</details>

**5.** Dlaczego w misji imię i nazwisko odczytujesz przed numerem miejsca?

<details>
<summary>Przykładowa odpowiedź</summary>

Bo po odczycie liczby przez `>>` w wejściu zostaje koniec linijki, a `std::getline` wywołane potem mogłoby odczytać pusty tekst. Gdy najpierw działa `std::getline`, a potem `>>`, problem nie występuje.

</details>

## Podsumowanie

- `std::string` przechowuje tekst w zmiennej. Wymaga `#include <string>`. Literał tekstowy w cudzysłowie i zmienna `std::string` to różne rzeczy, choć mogą zawierać ten sam tekst.
- Zmienną `std::string` inicjalizujesz w `{}`, zmieniasz przypisaniem i wypisujesz przez `std::cout`. Tekst, który ma się nie zmieniać, oznaczasz `const`.
- `+` łączy teksty, gdy przynajmniej jeden operand każdego `+` jest typu `std::string`. Tworzy przy tym nowy tekst. `<<` tylko wysyła kolejne wartości na wyjście.
- `std::cin >>` odczytuje do `std::string` jedno słowo. `std::getline(std::cin, …)` odczytuje całą linijkę ze spacjami, bez znaku końca linijki.
- `std::string` mieści spacje. Ograniczenie do jednego słowa wynika z `>>`, nie z typu.
- Gdy program czyta tekst i liczbę: najpierw `std::getline`, potem `>>`.

## Co dalej

Znasz już wszystkie narzędzia Modułu 2: liczby całkowite i ułamkowe, tekst, obliczenia, stałe, dane od użytkownika i sposoby szukania błędów w wynikach. W lekcji 2.8 sprawdzisz je w samodzielnym zadaniu. **Lekcja 2.8 jest w przygotowaniu.**

---

## Przykładowe rozwiązania

Zajrzyj tutaj **po własnej próbie**. Twoje nazwy mogą się różnić, jeśli standardowe wyjście jest takie, jak wymagane.

<details>
<summary>Punkt 9: misja, identyfikator uczestnika</summary>

<!-- example: participant_badge -->
```cpp
#include <iostream>
#include <string>

int main() {
    std::string participant_name{""};
    int seat_number{0};

    std::cout << "Enter participant name:\n";
    std::getline(std::cin, participant_name);
    std::cout << "Enter seat number:\n";
    std::cin >> seat_number;

    const std::string welcome{"Welcome, " + participant_name + "!"};

    std::cout << "Participant: " << participant_name << "\n";
    std::cout << "Seat: " << seat_number << "\n";
    std::cout << welcome << "\n";
}
```

- `participant_name` jest typu `std::string`, bo to tekst, który może zawierać spacje. Dlatego odczytuje go `std::getline`. `seat_number` jest typu `int`, bo numer miejsca to liczba całkowita. Odczytuje go `>>`.
- `std::getline` stoi przed `>>`, więc nie ma problemu z pozostawionym końcem linijki.
- `welcome` to nowy tekst zbudowany przez `+`. Po zbudowaniu się nie zmienia, więc ma `const`. Numer miejsca trafia na ekran przez `<<`, bez łączenia z tekstem.

</details>

**Poprzednia lekcja:** [Lekcja 2.6: Program, który pyta użytkownika](lesson_06_a_program_that_asks_the_user.md) · **Następna lekcja:** w przygotowaniu · [Opis kursu](../../README.md)

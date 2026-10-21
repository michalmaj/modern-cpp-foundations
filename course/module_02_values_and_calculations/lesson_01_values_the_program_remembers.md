# Lekcja 2.1: Wartości, które program pamięta

**Polski** · [English](lesson_01_values_the_program_remembers.en.md) · [Opis kursu](../../README.md)

> **Moduł 2, lekcja 1** · około 60 minut
> **Potrzebujesz:** katalogu `cpp-workspace` i oryginalnego projektu `lesson_05_first_program`, jak w Module 1.
> **Wersja pilotażowa.** Przykłady z tej lekcji sprawdzamy automatycznie na Windowsie, Ubuntu i macOS.

## Zanim zaczniesz

Ta lekcja zakłada, że po Module 1:

- umiesz napisać od pustego pliku program wypisujący tekst, zbudować go i uruchomić;
- czytasz komunikaty kompilatora metodą z lekcji 1.2;
- zapisujesz swoją pracę w Gicie (lekcja 1.5).

## Sytuacja

Dotąd każdy Twój program wypisywał tekst, który ktoś przygotował wcześniej, znak po znaku. Nawet liczba `75` w wyniku była tylko dwoma znakami w napisie.

Dziś program sam **obliczy** wynik. Wartości, z których liczy, będą miały nazwy, a gdy zmienisz jedną z nich, zmieni się wszystko, co od niej zależy.

Po tej lekcji będziesz:

- odróżniać tekst zawierający cyfry od wartości liczbowej;
- wiedzieć, czym jest literał liczbowy i do czego służy typ `int`;
- tworzyć zmienne z wartością początkową, na przykład `int ticket_count{3};`;
- używać zmiennych w obliczeniach z `+`, `-` i `*` i zapisywać wynik w nowej zmiennej;
- wypisywać tekst i liczby w jednej instrukcji;
- przewidywać wynik programu, zanim go uruchomisz;
- samodzielnie pisać program, którego wynik zależy od ustalonych wartości.

## 1. Przygotuj projekt

W `cpp-workspace` utwórz katalog `lesson_2_1` i skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program`, jak w Module 1. Programy z tej lekcji wpisujesz w `main.cpp` tego katalogu. Budujesz i uruchamiasz go jak dotąd: w CLionie albo w terminalu.

## 2. Tekst a liczba

Zastąp zawartość `main.cpp` tym programem:

<!-- example: text_or_number -->
```cpp
#include <iostream>

int main() {
    std::cout << "3 + 4\n";
    std::cout << (3 + 4) << "\n";
}
```

**Przewidź**, co wypisze każda z dwóch instrukcji. Zapisz odpowiedź, a potem uruchom program.

<details>
<summary>Wynik programu</summary>

<!-- output: text_or_number -->
```text
3 + 4
7
```

</details>

**Co się stało?**

- **Pierwsza instrukcja** wypisuje **napis**, jak w Module 1. Cudzysłowy mówią: „wypisz te znaki dokładnie tak, jak są”. Cyfry w napisie to tylko znaki, tak samo jak litery.
- **W drugiej instrukcji** `3` i `4` stoją **bez cudzysłowów**. To **literały liczbowe**: liczby zapisane wprost w kodzie. Program traktuje je jak liczby, więc `3 + 4` jest **wyrażeniem**, które program **oblicza** podczas działania. Wysyła do `std::cout` wynik, czyli wartość `7`.
- **Nawiasy** wokół `3 + 4` pokazują wyraźnie, co ma zostać obliczone. Dokładne zasady kolejności działań poznasz w jednej z następnych lekcji.
- **Nowością są dwa znaki `<<` w jednej instrukcji:** `std::cout << (3 + 4) << "\n";`. Każde `<<` wysyła do `std::cout` kolejny element, od lewej do prawej: najpierw wartość `7`, potem napis `"\n"`, czyli przejście do nowej linii.

## 3. Przewidź: kilka obliczeń

Zastąp zawartość `main.cpp` tym programem. **Zanim go uruchomisz,** zapisz, co wypisze każda linijka.

<!-- example: predict -->
```cpp
#include <iostream>

int main() {
    std::cout << (10 - 3) << "\n";
    std::cout << (6 * 7) << "\n";
    std::cout << "6 * 7 = " << (6 * 7) << "\n";
    std::cout << (2 + 3 + 4) << "\n";
}
```

<details>
<summary>Wynik programu</summary>

<!-- output: predict -->
```text
7
42
6 * 7 = 42
9
```

</details>

- `-` to odejmowanie, a `*` to mnożenie. Znak `x` nie oznacza w C++ mnożenia.
- Trzecia linijka łączy oba światy: najpierw napis `"6 * 7 = "`, wypisany dokładnie tak, jak jest, a potem **obliczona** wartość `42`.

## 4. Zmienna: nazwa dla wartości

Kasa sprzedaje bilety po 25. Ten program wypisuje cenę i koszt trzech biletów:

<!-- example: repeated_numbers -->
```cpp
#include <iostream>

int main() {
    std::cout << "Price per ticket: " << 25 << "\n";
    std::cout << "Total cost: " << (3 * 25) << "\n";
}
```

<!-- output: repeated_numbers -->
```text
Price per ticket: 25
Total cost: 75
```

Działa, ale cena `25` jest wpisana w dwóch miejscach. Jeśli się zmieni, trzeba ją znaleźć i poprawić wszędzie, a o jednym miejscu łatwo zapomnieć. Do tego `3 * 25` nie mówi, co te liczby znaczą.

Rozwiązaniem jest **zmienna**: **nazwana wartość określonego typu**. Pomocna bywa analogia z podpisaną szufladką, w której leży liczba. To tylko analogia: w rzeczywistości zmienną zarządza kompilator i nie musisz wiedzieć, jak dokładnie ją przechowuje.

<!-- example: first_variables -->
```cpp
#include <iostream>

int main() {
    int ticket_count{3};
    int ticket_price{25};
    int total_cost{ticket_count * ticket_price};

    std::cout << "Tickets: " << ticket_count << "\n";
    std::cout << "Price per ticket: " << ticket_price << "\n";
    std::cout << "Total cost: " << total_cost << "\n";
}
```

<!-- output: first_variables -->
```text
Tickets: 3
Price per ticket: 25
Total cost: 75
```

Rozbierz pierwszą linijkę w `main`, `int ticket_count{3};`:

| Część | Znaczenie |
|---|---|
| `int` | **Typ**: jaki rodzaj wartości przechowuje zmienna. `int` to liczby **całkowite**, bez części ułamkowej, na przykład `3`, `25`, `-7`. Inne typy poznasz w kolejnych lekcjach. |
| `ticket_count` | **Nazwa** zmiennej. Dzięki niej używasz wartości w dalszej części programu. |
| `{3}` | **Inicjalizacja**: wartość początkowa. Zmienna dostaje ją od razu, gdy powstaje. |
| `;` | Koniec tej linijki, jak przy instrukcjach. |

Cała linijka to **deklaracja** zmiennej: mówi kompilatorowi, że od teraz istnieje zmienna o takiej nazwie, typie i wartości początkowej.

**Użycie zmiennej:**

- `ticket_count * ticket_price` w trzeciej linijce **odczytuje** wartości obu zmiennych i je mnoży. Wynik, `75`, staje się wartością początkową nowej zmiennej `total_cost`.
- `std::cout << ticket_count` wypisuje **wartość** zmiennej, czyli `3`. Sama nazwa, bez cudzysłowów, oznacza wartość. `"ticket_count"` w cudzysłowie byłoby zwykłym napisem i program wypisałby słowo `ticket_count`.
- Zmiennej używasz **po** jej deklaracji, czyli niżej w kodzie. Dlatego `total_cost` stoi pod `ticket_count` i `ticket_price`.

**Zasady dobrego kodu, od pierwszej zmiennej:**

- **Zawsze nadawaj wartość początkową.** Zmienna bez niej nie ma określonej wartości, a odczytanie jej to błąd, którego kompilator nie zawsze wykryje. W tym kursie każda zmienna dostaje wartość od razu.
- **Nazwa mówi, co znaczy wartość:** `ticket_price`, a nie `p` czy `x`.
  - Nazwy w kursie piszemy po angielsku, małymi literami, ze słowami połączonymi podkreśleniem (`snake_case`).
  - Nazwa nie może zawierać spacji ani myślnika i nie może zaczynać się od cyfry.
  - Wielkość liter ma znaczenie: `Total` i `total` to dwie różne nazwy.
- W tej lekcji każda zmienna dostaje wartość **raz**, przy tworzeniu. Jak zmienić wartość zmiennej, która już istnieje, dowiesz się w lekcji 2.2.

**Szybki eksperyment z literówką.** W ostatnim programie zmień w jednej linijce `std::cout` nazwę `ticket_count` na `ticket_cout` (bez `n`). Zbuduj go. Na przykład:

<!-- broken: name_typo at=5:33 errors=1 error=^use of undeclared identifier 'ticket_cout'; did you mean 'ticket_count'\?$ -->
```cpp
#include <iostream>

int main() {
    int ticket_count{3};
    std::cout << "Tickets: " << ticket_cout << "\n";
}
```

Komunikat znasz z lekcji 1.2: `use of undeclared identifier 'ticket_cout'; did you mean 'ticket_count'?`. Kompilator nie zna nazwy `ticket_cout` i podpowiada podobną nazwę, którą zna. Popraw literówkę i zbuduj program ponownie.

## 5. Zmień wartości

Wróć do programu z kasą biletową (ten z trzema zmiennymi). **Zmień tylko** wartość początkową `ticket_count` z `3` na `5`.

**Przewidź**, co wypisze program, zanim go zbudujesz i uruchomisz.

<details>
<summary>Wynik programu</summary>

<!-- output: first_variables_changed -->
```text
Tickets: 5
Price per ticket: 25
Total cost: 125
```

</details>

Zmieniła się jedna liczba w kodzie, a w wyniku dwie linijki, bo `total_cost` jest obliczany z `ticket_count`. Na tym polega korzyść ze zmiennych: każda wartość jest zapisana w kodzie **jeden raz**, a wszystko, co od niej zależy, korzysta z jej nazwy. Pamiętaj, że jak zawsze po zmianie kodu program trzeba **zbudować ponownie**.

## 6. Uzupełnij: powierzchnia pokoju

Pokój ma 4 metry szerokości i 5 metrów długości. W programie brakuje jednej linijki:

<!-- fragment -->
```cpp
#include <iostream>

int main() {
    int room_width{4};
    int room_length{5};
    _______________________________________

    std::cout << "Area: " << room_area << " square metres\n";
}
```

**Zadanie:** zastąp linijkę z podkreśleniami **własną deklaracją** zmiennej `room_area`, której wartość program obliczy z szerokości i długości. Program ma wypisać:

<!-- output: room_area -->
```text
Area: 20 square metres
```

Liczby `20` nie wpisuj w kodzie: niech program ją obliczy.

<details>
<summary>Podpowiedź</summary>

Spójrz, jak powstaje `total_cost` w punkcie 4: typ, nazwa, a w `{}` wyrażenie z innymi zmiennymi.

</details>

## 7. Misja: kasa biletowa

Sala koncertowa ma 50 miejsc. Bilet kosztuje 40, a sprzedano 6 biletów. Kasjer chce programu, który wypisze krótkie podsumowanie.

W `cpp-workspace` utwórz katalog `ticket_office`, skopiuj do niego `CMakeLists.txt` z oryginalnego `lesson_05_first_program`, utwórz pusty `main.cpp` i napisz program sam.

Program ma wypisać dokładnie:

<!-- output: ticket_office -->
```text
Tickets sold: 6
Price per ticket: 40
Total: 240
Seats left: 44
```

### Kryterium sukcesu

- Wynik zgadza się co do znaku.
- Liczba miejsc w sali, cena i liczba sprzedanych biletów są zapisane w zmiennych typu `int`, każda **jeden raz**, z wartością początkową w `{}`.
- `240` i `44` **oblicza program**. Te liczby nie występują w kodzie.
- Nazwy zmiennych są po angielsku, w `snake_case`, i mówią, co znaczy wartość.
- Umiesz wyjaśnić, skąd program „wie”, że zostały 44 miejsca.

Gdy wynik się zgadza, możesz zapisać projekt w Gicie, jak w lekcji 1.5.

<details>
<summary>Podpowiedź 1</summary>

Ile różnych wartości jest danych w treści zadania? Ile trzeba obliczyć? Każda z nich może mieć własną zmienną.

</details>

<details>
<summary>Podpowiedź 2</summary>

Liczba wolnych miejsc to liczba miejsc w sali **minus** liczba sprzedanych biletów.

</details>

### Wariant: więcej sprzedanych biletów

Sprzedano jeszcze 3 bilety, więc razem 9. **Przewidź** nowy wynik, a potem zmień w programie **jedną** wartość początkową, zbuduj i uruchom program. Wynik ma być taki:

<!-- output: ticket_office_variant -->
```text
Tickets sold: 9
Price per ticket: 40
Total: 360
Seats left: 41
```

Jeśli w programie musisz zmienić więcej niż jedną liczbę, wróć do kryteriów misji.

Przykładowe rozwiązania są w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 8. Gdy coś pójdzie inaczej

| Co widzisz | Co to znaczy | Co zrobić |
|---|---|---|
| Zamiast liczby pojawia się nazwa zmiennej, na przykład `Total: total_cost` | Nazwa stoi w cudzysłowie, więc jest zwykłym napisem. | Usuń cudzysłowy wokół nazwy: `<< total_cost <<`. |
| Wynik sklejony z tekstem, na przykład `Total:240` | W napisie przed wartością brakuje spacji. | Dopisz spację na końcu napisu: `"Total: "`. |
| `use of undeclared identifier '…'` | Kompilator nie zna tej nazwy: literówka, inna wielkość liter albo zmienna użyta wyżej, niż została zadeklarowana. | Porównaj nazwę z deklaracją, znak po znaku. Sprawdź, czy deklaracja stoi wyżej. Kompilator często podpowiada właściwą nazwę (`did you mean …?`). |
| Błąd kompilacji w linijce z `<<` | Brakuje `<<` między elementami albo cudzysłowu w napisie. | Każdy element (napis, wartość, `"\n"`) poprzedza własne `<<`. |
| Program po zmianie wartości wypisuje stary wynik | Program nie został zbudowany ponownie. | Zbuduj ponownie (Run w CLionie robi to sam). |

**Uwaga:** tekstu i liczby nie łączy się w C++ znakiem `+`, tak jak w niektórych innych językach. Każdy element wysyłasz do `std::cout` osobnym `<<`.

## 9. Wyjaśnij

Odpowiedz własnymi słowami, najlepiej na piśmie. Dopiero potem porównaj z przykładową odpowiedzią.

**1.** Dlaczego `std::cout << "3 + 4\n";` wypisuje `3 + 4`, a `std::cout << (3 + 4) << "\n";` wypisuje `7`?

<details>
<summary>Przykładowa odpowiedź</summary>

W cudzysłowie `3 + 4` to napis, który program wypisuje znak po znaku. Bez cudzysłowów `3` i `4` to liczby, a `3 + 4` to wyrażenie, które program oblicza. Do `std::cout` trafia jego wynik, `7`.

</details>

**2.** Co oznacza każda część zapisu `int ticket_price{25};`?

<details>
<summary>Przykładowa odpowiedź</summary>

`int` to typ: liczba całkowita. `ticket_price` to nazwa zmiennej. `{25}` to wartość początkowa. `;` kończy deklarację.

</details>

**3.** Dlaczego po zmianie `ticket_count` z `3` na `5` zmieniły się dwie linijki wyniku, choć w kodzie zmieniono jedną liczbę?

<details>
<summary>Przykładowa odpowiedź</summary>

Bo `total_cost` jest obliczany z wartości `ticket_count`. Program wypisuje `ticket_count` i obliczony z niej `total_cost`, więc obie linijki zależą od tej jednej wartości.

</details>

**4.** Czym różni się `std::cout << total_cost;` od `std::cout << "total_cost";`?

<details>
<summary>Przykładowa odpowiedź</summary>

Pierwsze wypisuje wartość zmiennej, na przykład `75`. Drugie wypisuje napis, czyli słowo `total_cost`.

</details>

**5.** W misji: skąd program „wie”, że zostały 44 miejsca?

<details>
<summary>Przykładowa odpowiedź</summary>

Nie wie tego z góry. Oblicza to z dwóch zmiennych: liczby miejsc w sali (50) minus liczby sprzedanych biletów (6). Gdy zmieni się jedna z nich, wynik też się zmieni.

</details>

## Podsumowanie

- W cudzysłowie cyfry są tylko tekstem. Bez cudzysłowów `3 + 4` to **wyrażenie**, które program **oblicza**.
- **Zmienna** to nazwana wartość określonego typu. `int` przechowuje liczby całkowite.
- Deklaracja z inicjalizacją: `int ticket_count{3};`. Każda zmienna w kursie dostaje wartość od razu.
- Zmiennych używasz w wyrażeniach z `+`, `-` i `*`, a wynik możesz zapisać w nowej zmiennej.
- Kilka `<<` w jednej instrukcji wysyła do `std::cout` kolejne elementy: napisy i wartości.
- Każda wartość zapisana raz, pod dobrą nazwą, oznacza jedną zmianę w kodzie, gdy wartość się zmienia.

## Co dalej

W tej lekcji każda zmienna dostawała wartość raz, przy tworzeniu. W [lekcji 2.2](lesson_02_when_values_change.md) wartości zaczną się zmieniać w trakcie działania programu.

---

## Przykładowe rozwiązania

Zajrzyj tutaj **po własnej próbie**. Twoje nazwy zmiennych mogą być inne i nadal dobre, jeśli mówią, co znaczy wartość.

<details>
<summary>Punkt 5: zmieniony program</summary>

<!-- example: first_variables_changed -->
```cpp
#include <iostream>

int main() {
    int ticket_count{5};
    int ticket_price{25};
    int total_cost{ticket_count * ticket_price};

    std::cout << "Tickets: " << ticket_count << "\n";
    std::cout << "Price per ticket: " << ticket_price << "\n";
    std::cout << "Total cost: " << total_cost << "\n";
}
```

</details>

<details>
<summary>Punkt 6: powierzchnia pokoju</summary>

<!-- example: room_area -->
```cpp
#include <iostream>

int main() {
    int room_width{4};
    int room_length{5};
    int room_area{room_width * room_length};

    std::cout << "Area: " << room_area << " square metres\n";
}
```

Powierzchnia to szerokość razy długość, a wynik od razu staje się wartością początkową `room_area`.

</details>

<details>
<summary>Punkt 7: misja, kasa biletowa</summary>

<!-- example: ticket_office -->
```cpp
#include <iostream>

int main() {
    int hall_seats{50};
    int ticket_price{40};
    int tickets_sold{6};
    int total{tickets_sold * ticket_price};
    int seats_left{hall_seats - tickets_sold};

    std::cout << "Tickets sold: " << tickets_sold << "\n";
    std::cout << "Price per ticket: " << ticket_price << "\n";
    std::cout << "Total: " << total << "\n";
    std::cout << "Seats left: " << seats_left << "\n";
}
```

- Dane z treści zadania to trzy zmienne: `hall_seats`, `ticket_price` i `tickets_sold`.
- Wyniki to dwie zmienne obliczane z danych: `total` i `seats_left`.
- `hall_seats` nie jest wypisywane, ale jest potrzebne do obliczenia.

</details>

<details>
<summary>Punkt 7: wariant</summary>

<!-- example: ticket_office_variant -->
```cpp
#include <iostream>

int main() {
    int hall_seats{50};
    int ticket_price{40};
    int tickets_sold{9};
    int total{tickets_sold * ticket_price};
    int seats_left{hall_seats - tickets_sold};

    std::cout << "Tickets sold: " << tickets_sold << "\n";
    std::cout << "Price per ticket: " << ticket_price << "\n";
    std::cout << "Total: " << total << "\n";
    std::cout << "Seats left: " << seats_left << "\n";
}
```

Zmieniła się tylko jedna liczba: `tickets_sold{9}`. Oba wyniki program obliczył sam.

</details>

**Poprzednia lekcja:** [Lekcja 1.6: Samodzielnie od pomysłu do działającego programu](../module_01_first_programs/lesson_06_from_idea_to_working_program.md) · **Następna lekcja:** [Lekcja 2.2: Gdy wartości się zmieniają](lesson_02_when_values_change.md) · [Opis kursu](../../README.md)

# Lekcja 5.7: Program z własnych funkcji (sprawdzian Modułu 5)

**Polski** · [English](lesson_07_a_program_of_functions.en.md) · [Opis kursu](../../README.md)

> **Moduł 5, lekcja 7: sprawdzian** · około 100–120 minut, można go podzielić na dwa podejścia
> **Potrzebujesz:** katalogu `cpp-workspace` i oryginalnego projektu `lesson_05_first_program`.
> **Wersja pilotażowa.** Rozwiązania referencyjne z tej lekcji sprawdzamy automatycznie na Windowsie, Ubuntu i macOS, z podanymi danymi wejściowymi. Twojej pracy nic nie ocenia automatycznie: sprawdzasz ją samodzielnie, według kryteriów.

## Jak przebiega ten sprawdzian

Ta lekcja nie wprowadza niczego nowego. Sprawdzasz, czy potrafisz samodzielnie zaprojektować kilka współpracujących funkcji: zdecydować, **co trzeba obliczyć**, **która funkcja powinna to robić** i **kto potrzebuje jej wyniku**. Do tego poprawiasz trzy krótkie programy z błędami, rozpoznajesz błąd kompilacji i błąd linkowania oraz wyjaśniasz swoje decyzje.

Lekcja ma dwie części:

- **Część A: sprawdzian.** Wymagania, przykłady, zadania, pytania i kryteria. Bez podpowiedzi i bez kodu rozwiązań. Wszystko, czego potrzebujesz, znasz z Modułów 1–5.
- **Część B: sprawdzenie i omówienie.** Podpowiedzi, pełna lista przypadków kontrolnych, przykładowe rozwiązania, wyjaśnienia i samoocena. Przejdź do niej po wykonaniu części A albo wtedy, gdy świadomie zrezygnujesz z dalszej samodzielnej próby.

Zajrzenie do części B, do wcześniejszych lekcji albo do notatek nie jest porażką. Ważne jest, żeby **uczciwie zanotować, co zrobiono samodzielnie, a co z pomocą**. Proponowany podział na dwa podejścia:

- **pierwsze:** zaprojektowanie funkcji i zapisanie ich zadań, napisanie programu z zadania 1, sprawdzenie funkcji osobno i podstawowe przypadki całego programu;
- **drugie:** przypadki graniczne, zadania 2 i 3, porównanie z rozwiązaniem, pytania i samoocena.

**Możesz używać:** CLiona albo terminala, CMake i Ninja, jak dotąd; `CMakeLists.txt` skopiowanego z oryginalnego `lesson_05_first_program`; tabel przebiegu i przypadków oraz tymczasowych wydruków testowych. Debugger nie jest potrzebny. Nie musisz kończyć danych z klawiatury: przypadki, w których dane kończą się wcześniej, analizujesz na papierze.

---

# Część A: sprawdzian

## Zadanie 1: Wypożyczalnia rowerów

Niewielka wypożyczalnia ma kilka rowerów. Pracownik kolejno obsługuje prośby klientów: każdy klient prosi o określoną liczbę rowerów, a program decyduje, czy prośbę można przyjąć. Po przyjęciu prośby dostępnych rowerów ubywa. Po wszystkich zaplanowanych prośbach program wypisuje podsumowanie. To uproszczony model do ćwiczenia: nie ma zwrotów, cen, czasu wypożyczenia ani danych klientów.

**Przygotowanie:** w `cpp-workspace` utwórz katalog `bike_rental`, skopiuj do niego `CMakeLists.txt` z oryginalnego `lesson_05_first_program`, utwórz **pusty** `main.cpp` i napisz cały program samodzielnie.

**Plan dnia:**

- Program wypisuje `Enter available bikes (0-6) and request count (0-5):` i odczytuje dwie liczby całkowite: liczbę dostępnych rowerów i liczbę zgłoszeń do obsłużenia.
- Dopuszczalne są od 0 do 6 rowerów i od 0 do 5 zgłoszeń, włącznie. Zero to poprawna wartość obu pól.
- Jeśli odczyt się nie uda, program wypisuje tylko `Input could not be read` i kończy pracę.
- Jeśli którakolwiek wartość jest spoza zakresu, wypisuje tylko `Invalid rental plan` i kończy pracę.

**Zgłoszenia:**

- Dla każdego zgłoszenia, po kolei, program wypisuje `Enter bikes for request N:`, gdzie `N` to numer zgłoszenia od 1, i odczytuje liczbę żądanych rowerów.
- Klient może poprosić o 1, 2 albo 3 rowery. Prośba jest **przyjęta**, jeśli mieści się w tym zakresie i wypożyczalnia ma co najmniej tyle dostępnych rowerów. W przeciwnym razie jest **odrzucona**. Nie ma częściowych wypożyczeń: przy prośbie o 3 rowery i 2 dostępnych cała prośba zostaje odrzucona.
- Poprawnie odczytana liczba spoza zakresu, na przykład 0 albo 4, to **odrzucone zgłoszenie**, a nie nieudany odczyt. Program przechodzi wtedy do następnego zgłoszenia.
- Po każdym zgłoszeniu program wypisuje `Request N: Accepted` albo `Request N: Rejected`.
- Przyjęte zgłoszenie zmniejsza liczbę dostępnych rowerów o liczbę żądanych rowerów. Odrzucone nie zmienia jej wcale. Liczba dostępnych rowerów nigdy nie jest ujemna.
- Jeśli odczyt liczby rowerów dla zgłoszenia się nie uda, na przykład po tekście albo gdy dane skończą się wcześniej, program wypisuje `Input could not be read` i kończy pracę, bez podsumowania i bez kolejnych prób odczytu. Wcześniej wypisane linijki zostają.

**Podsumowanie** wypisuje się tylko wtedy, gdy wszystkie zaplanowane zgłoszenia zostały odczytane, w tej kolejności:

- `Accepted requests: N`
- `Rejected requests: N`
- `Bikes remaining: N`

Liczba przyjętych zgłoszeń to nie liczba wypożyczonych rowerów: jedno zgłoszenie może dotyczyć kilku rowerów.

**Funkcje:**

- Program ma **co najmniej trzy sensowne własne funkcje oprócz `main`**. Co najmniej jedna zwraca `bool`, a co najmniej jedna `int`.
- **Co najmniej jedna własna funkcja wywołuje inną własną funkcję** i korzysta z jej wyniku.
- Dane przechodzą przez parametry i zwracane wartości. Funkcje obliczające i sprawdzające nie odczytują i nie wypisują niczego.
- Nazwy, parametry i podział funkcji wybierasz samodzielnie. Jako punkt wyjścia możesz wydzielić trzy odpowiedzialności:
  1. czy liczba żądanych rowerów jest dopuszczalna;
  2. czy przy obecnej liczbie dostępnych rowerów prośbę da się obsłużyć;
  3. ile rowerów zostanie rzeczywiście przydzielonych: dla przyjętej prośby tyle, ile żądano, dla odrzuconej zero.

  To propozycja, a nie lista wymaganych funkcji. Inny podział jest dobry, jeśli każda funkcja ma rzeczywiste zadanie, ważne reguły się nie powtarzają, a kod pozostaje czytelny.
- **`main`** wypisuje pytania, odczytuje dane, sprawdza odczyt i plan, obsługuje dokładnie zaplanowaną liczbę zgłoszeń, wywołuje funkcje, aktualizuje liczbę dostępnych rowerów i liczniki oraz wypisuje wyniki.
- **Układ pliku** wybierasz samodzielnie: definicje funkcji pomocniczych przed funkcjami, które z nich korzystają, a na końcu `main`, albo deklaracje na początku, potem `main`, a definicje poniżej.
- Nie używaj zmiennych zadeklarowanych poza funkcjami.

**Przykład A:** dwa zgłoszenia przyjęte, dwa odrzucone. Dane:

<!-- input: bike_rental -->
```text
5
4
2
3
1
0
```

<!-- output: bike_rental -->
```text
Enter available bikes (0-6) and request count (0-5):
Enter bikes for request 1:
Request 1: Accepted
Enter bikes for request 2:
Request 2: Accepted
Enter bikes for request 3:
Request 3: Rejected
Enter bikes for request 4:
Request 4: Rejected
Accepted requests: 2
Rejected requests: 2
Bikes remaining: 0
```

Dwa pierwsze zgłoszenia wykorzystują wszystkie 5 rowerów. Trzecie nie może być obsłużone, bo nie ma już rowerów. Czwarte prosi o 0 rowerów, więc jest niedopuszczalne.

**Przykład B:** brak zaplanowanych zgłoszeń. Program nie pyta o żadne zgłoszenie:

<!-- input: bike_rental -->
```text
0
0
```

<!-- output: bike_rental -->
```text
Enter available bikes (0-6) and request count (0-5):
Accepted requests: 0
Rejected requests: 0
Bikes remaining: 0
```

**Przykład C:** 2 rowery, 3 zgłoszenia, prośby o 3, 1 i 1 rower. **Przewidź** całe standardowe wyjście, zanim napiszesz program:

<!-- input: bike_rental -->
```text
2
3
3
1
1
```

<details>
<summary>Standardowe wyjście dla przykładu C</summary>

<!-- output: bike_rental -->
```text
Enter available bikes (0-6) and request count (0-5):
Enter bikes for request 1:
Request 1: Rejected
Enter bikes for request 2:
Request 2: Accepted
Enter bikes for request 3:
Request 3: Accepted
Accepted requests: 2
Rejected requests: 1
Bikes remaining: 0
```

Prośba o 3 rowery przy 2 dostępnych jest odrzucona i nie zmienia stanu. Dwie kolejne prośby po 1 rowerze są przyjęte, a na końcu nie zostaje żaden rower.

</details>

**Zanim napiszesz program**, zapisz na kartce:

- jakie funkcje utworzysz, co każda dostaje, co zwraca i kto ją wywołuje;
- tabelę przypadków testowych: plan bez zgłoszeń, granice planu i wartości tuż poza nimi, zgłoszenie dokładnie wykorzystujące pozostałe rowery, zgłoszenie większe niż dostępność, a po nim mniejsze, kilka przyjęć i kilka odrzuceń z rzędu, prośby o 0, -1 i 4, tekst zamiast danych planu i zamiast liczby w zgłoszeniu oraz dane, które kończą się przed pierwszym zgłoszeniem i po kilku zgłoszeniach. Przy każdym przypadku zapisz oczekiwane standardowe wyjście.

Przypadki z danymi, które kończą się wcześniej, przeanalizuj na papierze, zamiast je uruchamiać, i porównaj z pełną listą kontrolną w części B.

**Najpierw sprawdź funkcje osobno**, wydrukami testowymi jak w lekcji 5.5:

1. Wybierz jedną funkcję.
2. Ustal, jaki wynik powinna zwrócić dla konkretnych argumentów.
3. Zapisz przewidywanie.
4. Tymczasowo wypisz wynik jej wywołania.
5. Porównaj.
6. Sprawdź przypadek graniczny.
7. Powtórz dla funkcji, która korzysta z innej własnej funkcji.
8. Usuń wydruki testowe, zanim sprawdzisz docelowe standardowe wyjście.

Sprawdź co najmniej: poprawną prośbę o 1 i o 3 rowery, niedopuszczalną prośbę o 0 i o 4, wystarczającą i niewystarczającą liczbę dostępnych rowerów, sytuację, w której dostępnych rowerów jest dokładnie tyle, ile żądanych, oraz wynik funkcji, która korzysta z innej funkcji.

Gdy wynik się zgadza, możesz zapisać projekt w Gicie, jak w lekcji 1.5. Przed commitem sprawdź `git status`: do historii trafiają tylko `main.cpp` i `CMakeLists.txt`.

## Zadanie 2: Trzy zgłoszenia

W `cpp-workspace` utwórz katalog `diagnosis_5`, skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program`. Każdy z poniższych programów wpisz po kolei w `main.cpp` tego katalogu.

**Zgłoszenie A: zasięg.** Funkcja ma obliczyć, ile rowerów zostanie na stacji z 6 rowerami po wypożyczeniu 2. Program się nie buduje:

<!-- broken: bikes_scope at=4:12 errors=1 error=^use of undeclared identifier 'station_bikes' -->
```cpp
#include <iostream>

int bikes_after_rental(int rented_bikes) {
    return station_bikes - rented_bikes;
}

int main() {
    const int station_bikes{6};
    std::cout << "Bikes left: " << bikes_after_rental(2) << "\n";
}
```

1. Wskaż nazwę, której kompilator nie zna w miejscu użycia.
2. Wyjaśnij, dlaczego funkcja nie ma dostępu do zmiennej `main`.
3. Zaproponuj parametr i popraw wywołanie tak, żeby przekazywało odpowiedni argument. Nie używaj zmiennej zadeklarowanej poza funkcjami.
4. Zbuduj i uruchom poprawiony program. Wymagany wynik to `Bikes left: 4`.

**Zgłoszenie B: wypisanie i wynik.** Wymaganie: program wypisuje **dokładnie jedną** linijkę, `Wheels needed: 6`, czyli liczbę kół potrzebnych dla 3 rowerów.

<!-- example: wheels_bug -->
```cpp
#include <iostream>

int wheels_needed(int bikes) {
    const int wheels{bikes * 2};
    std::cout << wheels << "\n";
    return wheels;
}

int main() {
    const int wheels{wheels_needed(3)};
    std::cout << "Wheels needed: " << wheels << "\n";
}
```

1. **Przewidź** standardowe wyjście.
2. Uruchom program i porównaj.
3. Wskaż instrukcje, które rzeczywiście wypisują tekst.
4. Oddziel obliczenie od prezentacji wyniku.
5. Sprawdź poprawkę.

**Zgłoszenie C: `return` w pętli.** Funkcja ma obliczyć łączną liczbę kroków treningu: w każdej rundzie są 2 kroki, więc dla 3 rund wynik to 6.

<!-- example: steps_bug -->
```cpp
#include <iostream>

int total_training_steps(int rounds) {
    int total{0};

    for (int round_number{0}; round_number < rounds; ++round_number) {
        total += 2;
        return total;
    }

    return total;
}

int main() {
    std::cout << "Rounds: 0, steps: " << total_training_steps(0) << "\n";
    std::cout << "Rounds: 1, steps: " << total_training_steps(1) << "\n";
    std::cout << "Rounds: 3, steps: " << total_training_steps(3) << "\n";
}
```

1. Zapisz poprawny wynik dla 0, 1 i 3 rund.
2. **Przewidź**, co wypisze **ten** program.
3. Uruchom go i znajdź przypadek, który ujawnia błąd.
4. Wyjaśnij, co robi `return` wewnątrz pętli.
5. Popraw funkcję i sprawdź ponownie wszystkie trzy przypadki.

Zapisz wyniki w tabeli:

| Zgłoszenie | Przypadek, który ujawnia błąd | Przyczyna | Poprawka | Sprawdzenie |
|---|---|---|---|---|
| A | | | | |
| B | | | | |
| C | | | | |

Projektu `diagnosis_5` nie musisz zapisywać w Gicie.

## Zadanie 3: Kompilacja czy linkowanie?

Oba programy się nie budują, ale z różnych powodów. Możesz je wpisać w `main.cpp` katalogu `diagnosis_5` i zbudować.

**Przypadek A:**

<!-- broken: bikes_undeclared at=4:36 errors=1 error=^use of undeclared identifier 'bikes_left' -->
```cpp
#include <iostream>

int main() {
    std::cout << "Bikes left: " << bikes_left(2) << "\n";
}

int bikes_left(int rented_bikes) {
    return 6 - rented_bikes;
}
```

**Przypadek B:**

<!-- broken: bikes_no_definition stage=link error=undefined reference to .bikes_left\(int\)'|undefined symbol: int __cdecl bikes_left\(int\)|"bikes_left\(int\)", referenced from -->
```cpp
#include <iostream>

int bikes_left(int rented_bikes);

int main() {
    std::cout << "Bikes left: " << bikes_left(2) << "\n";
}
```

Dla każdego przypadku:

1. Wskaż deklarację, definicję i wywołanie, jeśli występują.
2. Wskaż etap budowania, który się nie udaje: kompilację czy linkowanie.
3. Wyjaśnij, dlaczego właśnie ten etap.
4. Zaproponuj poprawkę.

Nie musisz pamiętać dokładnych komunikatów linkerów. Ważne są etap i przyczyna.

## Zadanie 4: Wyjaśnij swój projekt

Odpowiedz krótko, na piśmie, odwołując się do własnego programu z zadania 1:

1. Dlaczego wybrano właśnie takie funkcje? Jakie zadanie ma każda z nich?
2. Która funkcja sprawdza, czy liczba żądanych rowerów jest dopuszczalna?
3. Która funkcja decyduje o przydziale rowerów?
4. Która funkcja wywołuje inną własną funkcję? Jakie wartości jej przekazuje i jaki wynik otrzymuje?
5. Dlaczego Twoje funkcje nie muszą znać zmiennych lokalnych `main`?
6. Dlaczego liczba dostępnych rowerów zmienia się właśnie w tym miejscu programu, w którym ją zmieniasz?
7. Czy funkcja może poprawnie zwracać `bool`, niczego nie wypisując? Wskaż taką funkcję w swoim programie.
8. Co by się stało, gdyby w wywołaniu zamienić dwa argumenty typu `int`, na przykład liczbę żądanych i dostępnych rowerów? Czy kompilator by to zgłosił?
9. Dlaczego test z jednym zgłoszeniem nie wystarcza?
10. Dlaczego poprawny wynik funkcji pomocniczej nie gwarantuje poprawności całego programu?
11. Dlaczego Twój program się kompiluje? Które funkcje kompilator zna w miejscach ich wywołań i skąd?
12. Dlaczego po nieudanym odczycie program nie wypisuje podsumowania?

## Kryteria sukcesu

Sprawdzian jest zaliczony, gdy spełniasz **wszystkie** kryteria. Możesz przy tym korzystać z części B, jeśli uczciwie zaznaczysz to w samoocenie.

- `bike_rental/main.cpp` napisano od pustego pliku, w poprawnym C++20. Program buduje się bez błędów.
- Program ma co najmniej trzy sensowne własne funkcje oprócz `main`, w tym co najmniej jedną zwracającą `bool` i co najmniej jedną zwracającą `int`. Co najmniej jedna własna funkcja wywołuje inną i korzysta z jej wyniku.
- Funkcje obliczające i sprawdzające nie odczytują i nie wypisują niczego. Reguły zgłoszeń nie są powielone w `main`, a żadna funkcja nie istnieje tylko po to, żeby spełnić liczbę.
- Liczba dostępnych rowerów i liczniki zmieniają się w `main`, na podstawie wyników funkcji: przyjęte zgłoszenie zmniejsza dostępność, odrzucone jej nie zmienia.
- Standardowe wyjście dla przykładów A, B i C oraz dla przypadków, które da się wpisać, zgadza się z wymaganiami. Przypadki z danymi, które kończą się wcześniej, zgadzają się z tabelą przebiegu.
- Po nieudanym odczycie albo błędnym planie nie pojawia się podsumowanie.
- Funkcje sprawdzono osobno wydrukami testowymi, a w programie końcowym takich wydruków nie ma.
- Tabela przypadków powstała przed uruchomieniem programu.
- Wszystkie trzy zgłoszenia z zadania 2 zdiagnozowano i poprawiono, a poprawki sprawdzono.
- W zadaniu 3 poprawnie wskazano etap i przyczynę obu błędów.
- Umiesz wyjaśnić każdą linijkę swojego programu i odpowiedzieć na pytania z zadania 4.

Nazwy funkcji i zmiennych oraz podział programu mogą być inne niż w rozwiązaniu referencyjnym, jeśli są czytelne i spełniają wymagania. Poprawny wynik to warunek konieczny, ale **nie dowód zrozumienia**. Dlatego zadania 2–4 są częścią sprawdzianu.

---

# Część B: sprawdzenie i omówienie

Przejdź tutaj po wykonaniu części A albo wtedy, gdy świadomie zrezygnujesz z dalszej samodzielnej próby.

## Jak sprawdzić swoją pracę

- **Standardowe wyjście:** uruchom program dla każdego przypadku z tabeli, który możesz wpisać, i porównaj linijki programu z oczekiwanymi, znak po znaku. Pomiń wpisane dane widoczne dzięki echu.
- **Koniec danych:** przypadki, w których dane się kończą, sprawdź tabelą przebiegu i porównaj z pełną listą kontrolną. Każdy z nich jest tam sprawdzony automatycznie.
- **Funkcje:** czy każda ma zadanie, które da się opisać jednym zdaniem? Czy któraś funkcja tylko przekazuje argumenty dalej? Czy jakaś reguła stoi w dwóch miejscach?
- **Stan:** czy liczba dostępnych rowerów i liczniki zmieniają się w jednym miejscu, tylko na podstawie wyniku funkcji?

## Podpowiedzi

Rozwijaj je po kolei i tylko wtedy, gdy ich potrzebujesz.

<details>
<summary>Zadanie 1, podpowiedź 1</summary>

Które decyzje związane z pojedynczym zgłoszeniem nie powinny zależeć od tego, jak program wczytuje dane?

</details>

<details>
<summary>Zadanie 1, podpowiedź 2</summary>

Oddziel sprawdzenie dopuszczalnej liczby rowerów od sprawdzenia aktualnej dostępności. Zastanów się, która funkcja może wykorzystać wynik drugiej.

</details>

<details>
<summary>Zadanie 1, podpowiedź 3</summary>

Niech funkcje zwracają informacje potrzebne do podjęcia decyzji. `main` może wykorzystać wynik, aby zaktualizować dostępne rowery i liczniki zgłoszeń.

</details>

<details>
<summary>Zadanie 2, zgłoszenie A</summary>

Gdzie zadeklarowano `station_bikes`? Jak funkcja dostawała dane od miejsca wywołania w lekcji 5.2?

</details>

<details>
<summary>Zadanie 2, zgłoszenie B</summary>

Ile instrukcji `std::cout` wykonuje się w całym programie? Porównaj to z lekcją 5.3.

</details>

<details>
<summary>Zadanie 2, zgłoszenie C</summary>

Prześledź wywołanie dla 3 rund. Ile przebiegów pętli wykona się, zanim funkcja zakończy działanie? Porównaj to z lekcją 5.4.

</details>

## Pełna lista przypadków kontrolnych: zadanie 1

<details>
<summary>Otwórz po przygotowaniu własnej tabeli</summary>

Pierwsze trzy przypadki są sprawdzone w części A. W kolumnie „Wynik” `P` to przyjęte, a `O` odrzucone zgłoszenie, w kolejności zgłoszeń.

| Dane | Wynik | Co sprawdza |
|---|---|---|
| `5`, `4`, `2`, `3`, `1`, `0` | P P O O; podsumowanie 2, 2, 0 | przykład A |
| `0`, `0` | podsumowanie 0, 0, 0 | przykład B: brak zgłoszeń |
| `2`, `3`, `3`, `1`, `1` | O P P; podsumowanie 2, 1, 0 | przykład C: prośba większa niż dostępność |
| `6`, `0` | podsumowanie 0, 0, 6 | plan bez zgłoszeń, pełna stacja |
| `0`, `1`, `1` | O; podsumowanie 0, 1, 0 | brak rowerów |
| `1`, `1`, `1` | P; podsumowanie 1, 0, 0 | jedno zgłoszenie na całą dostępność |
| `2`, `1`, `3` | O; podsumowanie 0, 1, 2 | prośba większa niż dostępność, bez częściowego wypożyczenia |
| `6`, `5`, `1`, `1`, `1`, `1`, `1` | P P P P P; podsumowanie 5, 0, 1 | największy plan, kilka przyjęć z rzędu |
| `3`, `2`, `1`, `2` | P P; podsumowanie 2, 0, 0 | zgłoszenie dokładnie wykorzystuje pozostałe rowery |
| `4`, `3`, `3`, `3`, `1` | P O P; podsumowanie 2, 1, 0 | odrzucenie, a po nim mniejsze, przyjęte zgłoszenie |
| `1`, `3`, `2`, `3`, `2` | O O O; podsumowanie 0, 3, 1 | kilka odrzuceń z rzędu |
| `4`, `3`, `0`, `-1`, `4` | O O O; podsumowanie 0, 3, 4 | prośby o 0, -1 i 4 rowery |
| `6`, `5`, `3`, `4`, `2`, `2`, `1` | P O P O P; podsumowanie 3, 2, 0 | mieszana sekwencja |
| `-1`, `2` | `Invalid rental plan` | rowery tuż pod zakresem |
| `7`, `2` | `Invalid rental plan` | rowery tuż nad zakresem |
| `3`, `-1` | `Invalid rental plan` | zgłoszenia tuż pod zakresem |
| `3`, `6` | `Invalid rental plan` | zgłoszenia tuż nad zakresem |
| `abc`, `2` | `Input could not be read` | tekst zamiast liczby rowerów |
| `3`, `abc` | `Input could not be read` | tekst zamiast liczby zgłoszeń |
| brak danych | `Input could not be read` | dane kończą się od razu |
| `3`, `2`, koniec danych | pytanie o zgłoszenie 1, potem `Input could not be read` | dane kończą się przed pierwszym zgłoszeniem |
| `3`, `2`, `1`, koniec danych | P; pytanie o zgłoszenie 2, potem `Input could not be read` | dane kończą się po jednym zgłoszeniu |
| `3`, `3`, `1`, `abc` | P; pytanie o zgłoszenie 2, potem `Input could not be read` | tekst zamiast liczby w zgłoszeniu |
| `5`, `4`, `1`, `1`, koniec danych | P P; pytanie o zgłoszenie 3, potem `Input could not be read` | dane kończą się po kilku zgłoszeniach |

<!-- input: bike_rental -->
```text
6
0
```

<!-- output: bike_rental -->
```text
Enter available bikes (0-6) and request count (0-5):
Accepted requests: 0
Rejected requests: 0
Bikes remaining: 6
```

<!-- input: bike_rental -->
```text
0
1
1
```

<!-- output: bike_rental -->
```text
Enter available bikes (0-6) and request count (0-5):
Enter bikes for request 1:
Request 1: Rejected
Accepted requests: 0
Rejected requests: 1
Bikes remaining: 0
```

<!-- input: bike_rental -->
```text
1
1
1
```

<!-- output: bike_rental -->
```text
Enter available bikes (0-6) and request count (0-5):
Enter bikes for request 1:
Request 1: Accepted
Accepted requests: 1
Rejected requests: 0
Bikes remaining: 0
```

<!-- input: bike_rental -->
```text
2
1
3
```

<!-- output: bike_rental -->
```text
Enter available bikes (0-6) and request count (0-5):
Enter bikes for request 1:
Request 1: Rejected
Accepted requests: 0
Rejected requests: 1
Bikes remaining: 2
```

<!-- input: bike_rental -->
```text
6
5
1
1
1
1
1
```

<!-- output: bike_rental -->
```text
Enter available bikes (0-6) and request count (0-5):
Enter bikes for request 1:
Request 1: Accepted
Enter bikes for request 2:
Request 2: Accepted
Enter bikes for request 3:
Request 3: Accepted
Enter bikes for request 4:
Request 4: Accepted
Enter bikes for request 5:
Request 5: Accepted
Accepted requests: 5
Rejected requests: 0
Bikes remaining: 1
```

<!-- input: bike_rental -->
```text
3
2
1
2
```

<!-- output: bike_rental -->
```text
Enter available bikes (0-6) and request count (0-5):
Enter bikes for request 1:
Request 1: Accepted
Enter bikes for request 2:
Request 2: Accepted
Accepted requests: 2
Rejected requests: 0
Bikes remaining: 0
```

<!-- input: bike_rental -->
```text
4
3
3
3
1
```

<!-- output: bike_rental -->
```text
Enter available bikes (0-6) and request count (0-5):
Enter bikes for request 1:
Request 1: Accepted
Enter bikes for request 2:
Request 2: Rejected
Enter bikes for request 3:
Request 3: Accepted
Accepted requests: 2
Rejected requests: 1
Bikes remaining: 0
```

<!-- input: bike_rental -->
```text
1
3
2
3
2
```

<!-- output: bike_rental -->
```text
Enter available bikes (0-6) and request count (0-5):
Enter bikes for request 1:
Request 1: Rejected
Enter bikes for request 2:
Request 2: Rejected
Enter bikes for request 3:
Request 3: Rejected
Accepted requests: 0
Rejected requests: 3
Bikes remaining: 1
```

<!-- input: bike_rental -->
```text
4
3
0
-1
4
```

<!-- output: bike_rental -->
```text
Enter available bikes (0-6) and request count (0-5):
Enter bikes for request 1:
Request 1: Rejected
Enter bikes for request 2:
Request 2: Rejected
Enter bikes for request 3:
Request 3: Rejected
Accepted requests: 0
Rejected requests: 3
Bikes remaining: 4
```

<!-- input: bike_rental -->
```text
6
5
3
4
2
2
1
```

<!-- output: bike_rental -->
```text
Enter available bikes (0-6) and request count (0-5):
Enter bikes for request 1:
Request 1: Accepted
Enter bikes for request 2:
Request 2: Rejected
Enter bikes for request 3:
Request 3: Accepted
Enter bikes for request 4:
Request 4: Rejected
Enter bikes for request 5:
Request 5: Accepted
Accepted requests: 3
Rejected requests: 2
Bikes remaining: 0
```

<!-- input: bike_rental -->
```text
-1
2
```

<!-- output: bike_rental -->
```text
Enter available bikes (0-6) and request count (0-5):
Invalid rental plan
```

<!-- input: bike_rental -->
```text
7
2
```

<!-- output: bike_rental -->
```text
Enter available bikes (0-6) and request count (0-5):
Invalid rental plan
```

<!-- input: bike_rental -->
```text
3
-1
```

<!-- output: bike_rental -->
```text
Enter available bikes (0-6) and request count (0-5):
Invalid rental plan
```

<!-- input: bike_rental -->
```text
3
6
```

<!-- output: bike_rental -->
```text
Enter available bikes (0-6) and request count (0-5):
Invalid rental plan
```

<!-- input: bike_rental -->
```text
abc
2
```

<!-- output: bike_rental -->
```text
Enter available bikes (0-6) and request count (0-5):
Input could not be read
```

<!-- input: bike_rental -->
```text
3
abc
```

<!-- output: bike_rental -->
```text
Enter available bikes (0-6) and request count (0-5):
Input could not be read
```

<!-- input: bike_rental -->
```text
```

<!-- output: bike_rental -->
```text
Enter available bikes (0-6) and request count (0-5):
Input could not be read
```

<!-- input: bike_rental -->
```text
3
2
```

<!-- output: bike_rental -->
```text
Enter available bikes (0-6) and request count (0-5):
Enter bikes for request 1:
Input could not be read
```

<!-- input: bike_rental -->
```text
3
2
1
```

<!-- output: bike_rental -->
```text
Enter available bikes (0-6) and request count (0-5):
Enter bikes for request 1:
Request 1: Accepted
Enter bikes for request 2:
Input could not be read
```

<!-- input: bike_rental -->
```text
3
3
1
abc
```

<!-- output: bike_rental -->
```text
Enter available bikes (0-6) and request count (0-5):
Enter bikes for request 1:
Request 1: Accepted
Enter bikes for request 2:
Input could not be read
```

<!-- input: bike_rental -->
```text
5
4
1
1
```

<!-- output: bike_rental -->
```text
Enter available bikes (0-6) and request count (0-5):
Enter bikes for request 1:
Request 1: Accepted
Enter bikes for request 2:
Request 2: Accepted
Enter bikes for request 3:
Input could not be read
```

</details>

## Przykładowe rozwiązania

Zajrzyj tutaj **po własnej próbie**.

<details>
<summary>Zadanie 1: przykładowe rozwiązanie</summary>

<!-- example: bike_rental -->
```cpp
#include <iostream>

bool is_valid_plan(int available_bikes, int request_count) {
    const bool bikes_valid{available_bikes >= 0 && available_bikes <= 6};
    const bool count_valid{request_count >= 0 && request_count <= 5};
    return bikes_valid && count_valid;
}

bool is_valid_request(int requested_bikes) {
    return requested_bikes >= 1 && requested_bikes <= 3;
}

bool can_serve(int requested_bikes, int available_bikes) {
    return is_valid_request(requested_bikes) && requested_bikes <= available_bikes;
}

int bikes_to_assign(int requested_bikes, int available_bikes) {
    if (!can_serve(requested_bikes, available_bikes)) {
        return 0;
    }

    return requested_bikes;
}

int main() {
    int available_bikes{0};
    int request_count{0};

    std::cout << "Enter available bikes (0-6) and request count (0-5):\n";
    std::cin >> available_bikes;
    std::cin >> request_count;

    if (std::cin.fail()) {
        std::cout << "Input could not be read\n";
    } else if (!is_valid_plan(available_bikes, request_count)) {
        std::cout << "Invalid rental plan\n";
    } else {
        int accepted_requests{0};
        int rejected_requests{0};
        int request_number{1};
        bool input_failed{false};

        while (request_number <= request_count && !input_failed) {
            int requested_bikes{0};

            std::cout << "Enter bikes for request " << request_number << ":\n";
            std::cin >> requested_bikes;

            if (std::cin.fail()) {
                input_failed = true;
            } else {
                const int assigned_bikes{bikes_to_assign(requested_bikes, available_bikes)};

                if (assigned_bikes > 0) {
                    available_bikes = available_bikes - assigned_bikes;
                    ++accepted_requests;
                    std::cout << "Request " << request_number << ": Accepted\n";
                } else {
                    ++rejected_requests;
                    std::cout << "Request " << request_number << ": Rejected\n";
                }

                ++request_number;
            }
        }

        if (input_failed) {
            std::cout << "Input could not be read\n";
        } else {
            std::cout << "Accepted requests: " << accepted_requests << "\n";
            std::cout << "Rejected requests: " << rejected_requests << "\n";
            std::cout << "Bikes remaining: " << available_bikes << "\n";
        }
    }
}
```

| Funkcja | Zadanie | Parametry | Wynik | Kto ją wywołuje |
|---|---|---|---|---|
| `is_valid_plan` | czy plan dnia jest dopuszczalny | rowery, liczba zgłoszeń | `bool` | `main` |
| `is_valid_request` | czy prośba jest w zakresie 1–3 | żądane rowery | `bool` | `can_serve` |
| `can_serve` | czy prośbę da się obsłużyć przy obecnej dostępności | żądane i dostępne rowery | `bool` | `bikes_to_assign` |
| `bikes_to_assign` | ile rowerów przydzielić: żądaną liczbę albo 0 | żądane i dostępne rowery | `int` | `main` |

- **Współpraca:** `bikes_to_assign` korzysta z `can_serve`, a `can_serve` z `is_valid_request`. Każda reguła stoi w kodzie raz: zakres prośby tylko w `is_valid_request`, porównanie z dostępnością tylko w `can_serve`.
- **Możliwe wyniki:** `is_valid_request` daje `true` dla 1, 2 i 3. `can_serve` daje `true` tylko wtedy, gdy prośba jest dopuszczalna i nie większa niż dostępność, także gdy jest dokładnie równa. `bikes_to_assign` daje 0 dla odrzuconej prośby albo liczbę żądanych rowerów.
- **Stan zmienia `main`.** Funkcje dostają kopie wartości, jak w lekcji 5.2, i niczego nie zmieniają poza sobą. `main` odejmuje przydzielone rowery od `available_bikes` i zwiększa jeden z liczników. Dzięki temu stan wypożyczalni zmienia się w jednym miejscu, a dostępność nie może spaść poniżej zera: `bikes_to_assign` nigdy nie zwraca więcej, niż jest dostępnych rowerów.
- **Pętla** obsługuje dokładnie `request_count` zgłoszeń i kończy się wcześniej tylko wtedy, gdy odczyt się nie uda. Flaga `input_failed` działa jak w lekcji 4.5. Dla zera zgłoszeń pętla nie wykonuje się ani razu.
- **Nieudany odczyt:** wcześniejsze wyniki zostają, a program wypisuje `Input could not be read` zamiast podsumowania.
- **Układ pliku:** to rozwiązanie zapisuje definicje funkcji pomocniczych przed funkcjami, które z nich korzystają, a `main` na końcu. Drugi układ też jest poprawny: deklaracje czterech funkcji na początku, potem `main`, a definicje poniżej, w dowolnej kolejności, jak w lekcji 5.6.
- **Inne podziały** też są poprawne, na przykład bez osobnej funkcji `can_serve` albo bez funkcji dla planu, ze sprawdzeniem planu w `main`, jeśli każda funkcja ma rzeczywiste zadanie, a reguły się nie powtarzają.

**Przepływ wywołań** dla przykładu A: zgłoszenie 1 (2 rowery przy 5 dostępnych) i zgłoszenie 3 (1 rower przy 0 dostępnych):

| Krok | Zgłoszenie 1 | Zgłoszenie 3 |
|---|---|---|
| dostępne rowery przed zgłoszeniem | 5 | 0 |
| `main` wywołuje | `bikes_to_assign(2, 5)` | `bikes_to_assign(1, 0)` |
| `bikes_to_assign` wywołuje | `can_serve(2, 5)` | `can_serve(1, 0)` |
| `can_serve` wywołuje | `is_valid_request(2)`: `true` | `is_valid_request(1)`: `true` |
| `can_serve` porównuje | `2 <= 5`: `true`, zwraca `true` | `1 <= 0`: `false`, zwraca `false` |
| `bikes_to_assign` zwraca | 2 | 0 |
| decyzja `main` | przyjęte: `Request 1: Accepted` | odrzucone: `Request 3: Rejected` |
| dostępne rowery po zgłoszeniu | 5 - 2 = 3 | bez zmian: 0 |
| liczniki | przyjęte: 1 | odrzucone: 1 |

**Wydruki testowe** dla tych funkcji, w osobnym programie, jak w lekcji 5.5:

<!-- example: rental_checks -->
```cpp
#include <iostream>

bool is_valid_plan(int available_bikes, int request_count) {
    const bool bikes_valid{available_bikes >= 0 && available_bikes <= 6};
    const bool count_valid{request_count >= 0 && request_count <= 5};
    return bikes_valid && count_valid;
}

bool is_valid_request(int requested_bikes) {
    return requested_bikes >= 1 && requested_bikes <= 3;
}

bool can_serve(int requested_bikes, int available_bikes) {
    return is_valid_request(requested_bikes) && requested_bikes <= available_bikes;
}

int bikes_to_assign(int requested_bikes, int available_bikes) {
    if (!can_serve(requested_bikes, available_bikes)) {
        return 0;
    }

    return requested_bikes;
}

int main() {
    std::cout << "Plan 0, 0 valid: " << is_valid_plan(0, 0) << "\n";
    std::cout << "Plan 7, 2 valid: " << is_valid_plan(7, 2) << "\n";

    std::cout << "Request 1 valid: " << is_valid_request(1) << "\n";
    std::cout << "Request 3 valid: " << is_valid_request(3) << "\n";
    std::cout << "Request 0 valid: " << is_valid_request(0) << "\n";
    std::cout << "Request 4 valid: " << is_valid_request(4) << "\n";

    std::cout << "Serve 2 of 2: " << can_serve(2, 2) << "\n";
    std::cout << "Serve 3 of 2: " << can_serve(3, 2) << "\n";
    std::cout << "Serve 1 of 0: " << can_serve(1, 0) << "\n";
    std::cout << "Serve 4 of 6: " << can_serve(4, 6) << "\n";

    std::cout << "Assign 3 of 5: " << bikes_to_assign(3, 5) << "\n";
    std::cout << "Assign 3 of 2: " << bikes_to_assign(3, 2) << "\n";
    std::cout << "Assign 0 of 5: " << bikes_to_assign(0, 5) << "\n";
    std::cout << "Assign 2 of 2: " << bikes_to_assign(2, 2) << "\n";
}
```

<!-- output: rental_checks -->
```text
Plan 0, 0 valid: 1
Plan 7, 2 valid: 0
Request 1 valid: 1
Request 3 valid: 1
Request 0 valid: 0
Request 4 valid: 0
Serve 2 of 2: 1
Serve 3 of 2: 0
Serve 1 of 0: 0
Serve 4 of 6: 0
Assign 3 of 5: 3
Assign 3 of 2: 0
Assign 0 of 5: 0
Assign 2 of 2: 2
```

</details>

<details>
<summary>Zadanie 2, zgłoszenie A: przyczyna i poprawka</summary>

Kompilator zgłasza w linijce 4 `use of undeclared identifier 'station_bikes'`. Zmienna `station_bikes` jest lokalna w `main`, a funkcja widzi tylko swoje parametry i własne zmienne (lekcja 5.2). Poprawka: funkcja dostaje liczbę rowerów na stacji jako parametr, a `main` przekazuje ją jako argument.

<!-- example: bikes_scope_fixed -->
```cpp
#include <iostream>

int bikes_after_rental(int station_bikes, int rented_bikes) {
    return station_bikes - rented_bikes;
}

int main() {
    const int station_bikes{6};
    std::cout << "Bikes left: " << bikes_after_rental(station_bikes, 2) << "\n";
}
```

<!-- output: bikes_scope_fixed -->
```text
Bikes left: 4
```

Parametr może się nazywać tak samo jak zmienna w `main`. To nadal dwie różne zmienne: parametr otrzymuje tylko wartość argumentu.

</details>

<details>
<summary>Zadanie 2, zgłoszenie B: wynik przed poprawką i poprawka</summary>

Przed poprawką:

<!-- output: wheels_bug -->
```text
6
Wheels needed: 6
```

Liczbę wypisuje i funkcja, i `main`, a wymaganie mówi o jednej linijce. Funkcja oblicza i zwraca wynik, a o prezentacji decyduje `main`. Poprawka usuwa wypisywanie z funkcji:

<!-- example: wheels_fixed -->
```cpp
#include <iostream>

int wheels_needed(int bikes) {
    const int wheels{bikes * 2};
    return wheels;
}

int main() {
    const int wheels{wheels_needed(3)};
    std::cout << "Wheels needed: " << wheels << "\n";
}
```

<!-- output: wheels_fixed -->
```text
Wheels needed: 6
```

Funkcja, która wypisuje i zwraca wynik, jest poprawnym C++. Tutaj jest niezgodna z wymaganiem i miesza obliczenie z prezentacją.

</details>

<details>
<summary>Zadanie 2, zgłoszenie C: wynik przed poprawką i poprawka</summary>

Przed poprawką:

<!-- output: steps_bug -->
```text
Rounds: 0, steps: 0
Rounds: 1, steps: 2
Rounds: 3, steps: 2
```

- **Dla 0 i 1 rundy** wynik jest poprawny, więc te testy błędu nie ujawniają.
- **Dla 3 rund** wynik to 2 zamiast 6.
- **Przyczyna:** `return total;` stoi **w ciele pętli**. `return` nie kończy jednego przebiegu: kończy **całe wywołanie funkcji** (lekcja 5.4). Funkcja kończy się więc po pierwszym przebiegu, z wynikiem 2. Dla 0 rund pętla się nie wykonuje, a dla 1 rundy pierwszy przebieg jest jedynym, dlatego oba przypadki wyglądają dobrze.
- **Poprawka:** usuń `return` z pętli. Wynik zwraca końcowy `return`, po wszystkich przebiegach.

<!-- example: steps_fixed -->
```cpp
#include <iostream>

int total_training_steps(int rounds) {
    int total{0};

    for (int round_number{0}; round_number < rounds; ++round_number) {
        total += 2;
    }

    return total;
}

int main() {
    std::cout << "Rounds: 0, steps: " << total_training_steps(0) << "\n";
    std::cout << "Rounds: 1, steps: " << total_training_steps(1) << "\n";
    std::cout << "Rounds: 3, steps: " << total_training_steps(3) << "\n";
}
```

<!-- output: steps_fixed -->
```text
Rounds: 0, steps: 0
Rounds: 1, steps: 2
Rounds: 3, steps: 6
```

</details>

<details>
<summary>Zadanie 3: odpowiedzi</summary>

**Przypadek A.** Nie ma osobnej deklaracji. Definicja stoi pod `main`, a wywołanie `bikes_left(2)` w `main`. **Kompilacja się nie udaje:** kompilator zgłasza w linijce 4 `use of undeclared identifier 'bikes_left'`, bo czyta plik od góry i w miejscu wywołania nie zna jeszcze tej nazwy. Poprawka: dopisz deklarację `int bikes_left(int rented_bikes);` przed `main` albo przenieś definicję nad `main`.

**Przypadek B.** Deklaracja stoi przed `main`, wywołanie w `main`, a definicji nie ma nigdzie. **Kompilacja się udaje**, bo deklaracja wystarcza kompilatorowi. **Linkowanie się nie udaje:** linker nie znajduje definicji wywoływanej funkcji, więc program nie powstaje. Komunikat zależy od systemu, ale zawiera nazwę `bikes_left(int)`, a na końcu pojawia się `linker command failed`. Poprawka: dopisz definicję zgodną z deklaracją:

<!-- example: bikes_declared -->
```cpp
#include <iostream>

int bikes_left(int rented_bikes);

int main() {
    std::cout << "Bikes left: " << bikes_left(2) << "\n";
}

int bikes_left(int rented_bikes) {
    return 6 - rented_bikes;
}
```

<!-- output: bikes_declared -->
```text
Bikes left: 4
```

</details>

## Przykładowe odpowiedzi do zadania 4

<details>
<summary>Otwórz po zapisaniu własnych odpowiedzi</summary>

Odpowiedzi dotyczą rozwiązania referencyjnego. Twoje mogą się różnić, jeśli opisują Twój program.

1. Każda funkcja odpowiada na jedno pytanie: czy plan jest dopuszczalny, czy prośba jest w zakresie, czy da się ją obsłużyć, ile rowerów przydzielić. Każdą da się nazwać jednym zdaniem i sprawdzić osobno.
2. `is_valid_request`.
3. `bikes_to_assign`, która korzysta z `can_serve`.
4. `bikes_to_assign` wywołuje `can_serve` z liczbą żądanych i dostępnych rowerów i dostaje `bool`. `can_serve` wywołuje `is_valid_request` z liczbą żądanych rowerów i też dostaje `bool`.
5. Bo dostają potrzebne wartości jako argumenty. Zmienne `main` są lokalne i funkcje nie mają do nich dostępu (lekcja 5.2, zgłoszenie A).
6. Bo `main` przechowuje stan wypożyczalni, a funkcje pracują na kopiach wartości. Zmiana w jednym miejscu, po wyniku `bikes_to_assign`, gwarantuje, że odrzucone zgłoszenie niczego nie zmienia.
7. Tak, na przykład `is_valid_request` i `can_serve`. Zwracają odpowiedź, a o tym, co wypisać, decyduje `main`.
8. Kompilator by tego nie zgłosił, bo oba argumenty są typu `int` (lekcja 5.2). Program dawałby złe decyzje, na przykład `can_serve(5, 2)` zamiast `can_serve(2, 5)`. Ujawniłby to test z różnymi wartościami.
9. Bo jedno zgłoszenie nie sprawdza zmiany dostępności między zgłoszeniami, odrzucenia po wykorzystaniu rowerów ani liczników większych niż 1.
10. Bo `main` może źle korzystać z poprawnego wyniku, na przykład zapomnieć odjąć rowery albo zwiększyć zły licznik (lekcja 5.5).
11. Definicja każdej funkcji pomocniczej stoi przed funkcją, która ją wywołuje, a wszystkie przed `main`, więc w każdym miejscu wywołania kompilator zna już funkcję. W układzie z deklaracjami tę wiedzę dałyby deklaracje na początku pliku (lekcja 5.6).
12. Bo plan nie został w pełni zrealizowany: część zgłoszeń nie została odczytana, więc liczby w podsumowaniu nie opisywałyby zaplanowanego dnia.

</details>

## Samoocena

Przy każdym kryterium zaznacz jedną odpowiedź:

| Kryterium | Samodzielnie | Z podpowiedzią | Po zajrzeniu do rozwiązania | Do powtórki |
|---|---|---|---|---|
| Zaprojektowanie funkcji i ich zadań | | | | |
| Funkcja wywołująca inną funkcję | | | | |
| Przekazywanie argumentów i odbieranie wyników | | | | |
| Funkcje bez wejścia i wyjścia | | | | |
| Aktualizacja stanu w `main` | | | | |
| Obsługa zgłoszeń w pętli i liczniki | | | | |
| Nieudany odczyt i koniec danych | | | | |
| Wydruki testowe funkcji | | | | |
| Tabela przypadków z granicami | | | | |
| Zgłoszenie A (zasięg) | | | | |
| Zgłoszenie B (wypisanie i wynik) | | | | |
| Zgłoszenie C (`return` w pętli) | | | | |
| Zadanie 3 (kompilacja i linkowanie) | | | | |
| Wyjaśnienia z zadania 4 | | | | |

Jeśli w kolumnie „Do powtórki” jest coś zaznaczone, wróć do odpowiedniej lekcji:

| Temat | Lekcja |
|---|---|
| definicja, wywołanie i `void` | 5.1 |
| parametry, argumenty, przekazywanie przez wartość i zasięg | 5.2 |
| `return`, typ wyniku i `std::cout` | 5.3 |
| kilka dróg do `return` i klauzule ochronne | 5.4 |
| współpraca funkcji i wydruki testowe | 5.5 |
| deklaracja, definicja, kompilacja i linkowanie | 5.6 |
| pętle, liczniki i koniec danych | Moduł 4 |
| warunki, `&&` i `\|\|` | Moduł 3 |

Potem spróbuj zadania jeszcze raz, na przykład z inną liczbą rowerów albo innym zakresem próśb.

---

## Podsumowanie Modułu 5

Po siedmiu lekcjach potrafisz:

- definiować i wywoływać własne funkcje, także funkcje `void`;
- przekazywać funkcjom argumenty i rozumieć przekazywanie przez wartość;
- korzystać ze zmiennych lokalnych i wiedzieć, gdzie istnieje parametr;
- zwracać wyniki przez `return` i odróżniać obliczanie od wypisywania;
- korzystać z wyników typu `int`, `double`, `bool` i `std::string`;
- pisać funkcje z kilkoma drogami do `return` i klauzulami ochronnymi;
- budować funkcje, które korzystają z innych funkcji, i dzielić program na zadania;
- sprawdzać funkcje prostymi wydrukami testowymi;
- zapisywać deklaracje i definicje oraz odróżniać błędy kompilacji od błędów linkowania.

To podstawy. Funkcje w C++ mają jeszcze wiele możliwości, które poznasz w dalszych modułach.

## Co dalej

Kolejne moduły są w przygotowaniu.

**Poprzednia lekcja:** [Lekcja 5.6: Deklaracja, definicja i linkowanie](lesson_06_declaration_and_definition.md) · **Następna lekcja:** w przygotowaniu · [Opis kursu](../../README.md)

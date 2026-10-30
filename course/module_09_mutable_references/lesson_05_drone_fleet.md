# Lekcja 9.5: Flota dronów dostawczych (sprawdzian Modułu 9)

**Polski** · [English](lesson_05_drone_fleet.en.md) · [Opis kursu](../../README.md)

> **Moduł 9, lekcja 5: sprawdzian** · około 105–125 minut, w dwóch podejściach
> **Potrzebujesz:** katalogu `cpp-workspace` i oryginalnego projektu `lesson_05_first_program`.
> **Wersja pilotażowa.** Rozwiązania referencyjne z tej lekcji sprawdzamy automatycznie na Windowsie, Ubuntu i macOS. Twojej pracy nic nie ocenia automatycznie: sprawdzasz ją samodzielnie, według kryteriów. Twój program nie pyta o dane: wszystkie wartości są zapisane w kodzie. Dane z wejścia odczytuje tylko program kontrolny z części B.

## Jak przebiega ten sprawdzian

Ta lekcja nie wprowadza niczego nowego. Sprawdzasz, czy potrafisz samodzielnie zaprojektować program, w którym **kilka funkcji świadomie zmienia istniejące rekordy**: każda operacja zachowuje ustalone warunki poprawności, a odmowa nie zostawia częściowo zmienionych danych. Nie chodzi o liczenie podsumowań ani wybieranie najlepszego rekordu, tylko o kontrolowaną zmianę stanu.

Lekcja ma dwie części:

- **Część A: sprawdzian.** Zadanie 1: wymagania, dane, raport i kryteria. Bez podpowiedzi i bez kodu rozwiązań. Wszystko, czego potrzebujesz, znasz z Modułów 1–9.
- **Część B: sprawdzenie i omówienie.** Podpowiedzi, pełna lista przypadków kontrolnych, zadanie 2 (diagnostyka) i zadanie 3 (wyjaśnienia), które wykonujesz po zadaniu 1, a potem rozwiązanie referencyjne, poprawki, odpowiedzi i samoocena. Przejdź do niej dopiero po wykonaniu części A albo wtedy, gdy świadomie zrezygnujesz z dalszej samodzielnej próby.

Zajrzenie do części B, do wcześniejszych lekcji albo do notatek nie jest porażką. Ważne jest, żeby **uczciwie zanotować, co zrobiono samodzielnie, a co z pomocą**. Proponowany podział na dwa podejścia:

- **pierwsze:** analiza reguł, projekt typu i trzech funkcji, ich napisanie i raport dla danych z wymagań;
- **drugie:** przypadki graniczne, wariant z pustym wektorem, zadania 2 i 3, porównanie z rozwiązaniem i samoocena.

**Możesz używać:** CLiona albo terminala, CMake i Ninja, jak dotąd; `CMakeLists.txt` skopiowanego z oryginalnego `lesson_05_first_program`; tabel przypadków i przebiegu oraz tymczasowych wydruków testowych. Debugger nie jest potrzebny.

---

# Część A: sprawdzian

## Zadanie 1: Flota dronów dostawczych

Program zarządza uproszczoną flotą dronów dostawczych. To nie jest symulator prawdziwych urządzeń: bateria i koszt lotu to umowne punkty, a program nie modeluje czasu, odległości, tras ani pogody. Wszystkie operacje zmieniają drony zapisane w jednej kolekcji.

**Przygotowanie:** w `cpp-workspace` utwórz katalog `drone_fleet`, skopiuj do niego `CMakeLists.txt` z oryginalnego `lesson_05_first_program`, utwórz **pusty** `main.cpp` i napisz cały program samodzielnie.

### Dane floty

| Dron | Bateria | Loty | Uziemiony |
|---|---:|---:|---|
| A-01 | 65 | 2 | nie |
| B-02 | 35 | 0 | nie |
| C-03 | 90 | 4 | tak |
| D-04 | 100 | 1 | nie |

### Reguły

- Identyfikatory są niepuste, unikalne i składają się z prostego tekstu ASCII. Bateria ma od 0 do 100 punktów, a liczba lotów jest nieujemna. Wszystkie liczby są małe. Dane spełniają te założenia, więc program ich nie sprawdza.
- **Lot** jest dozwolony tylko wtedy, gdy spełnione są **wszystkie trzy** warunki:
  1. koszt lotu jest dodatni;
  2. dron nie jest uziemiony;
  3. bateria **po** locie wynosiłaby co najmniej 20 punktów. To rezerwa: bateria równa dokładnie 20 po locie jest dozwolona, a 19 już nie.
- Koszt 0 i koszt ujemny to niepoprawne żądania.
- **Lot przyjęty:** bateria maleje o koszt, liczba lotów rośnie o 1, a pozostałe pola się nie zmieniają. **Lot odrzucony:** żadne pole się nie zmienia. Nie ma częściowego lotu.
- **Lot po identyfikatorze** dotyczy tylko drona o tym identyfikatorze. Nieznany identyfikator to odmowa, po której nic się nie zmienia. Wynik „lot się nie odbył” nie rozróżnia, czy drona nie znaleziono, czy lot odrzucono, jak w lekcji 9.4.
- **Ładowanie floty:** każdy dron z baterią poniżej 100 dostaje baterię 100. Ładowanie nie zmienia liczby lotów ani identyfikatorów. Dron, który już ma 100, nie jest liczony jako naładowany.
- **Uziemiony dron może zostać naładowany, ale ładowanie nie znosi uziemienia.** Po naładowaniu nadal nie może latać.
- Liczba dronów w wektorze i ich kolejność nigdy się nie zmieniają.

### Typ i funkcje

- Program definiuje **jeden własny typ** drona z czterema polami: identyfikatorem (`std::string`), baterią (`int`), liczbą lotów (`int`) i informacją o uziemieniu (`bool`). Bez dodatkowych pól. Nazwy typu i pól wybierasz samodzielnie.
- **Funkcja lotu jednego drona** dostaje istniejący rekord przez modyfikowalną referencję i koszt (`int`) przez wartość. Sprawdza wszystkie warunki lotu, zanim cokolwiek zmieni. Zwraca `bool`: `true`, gdy wykonała lot, `false`, gdy go odrzuciła.
- **Funkcja lotu po identyfikatorze** dostaje istniejący wektor przez modyfikowalną referencję, identyfikator przez `const std::string&` i koszt przez wartość. Znajduje drona o tym identyfikatorze, wykonuje jego lot **funkcją lotu jednego drona** i zwraca jej wynik. Gdy identyfikatora nie ma, zwraca `false`.
- **Funkcja ładowania floty** dostaje istniejący wektor przez modyfikowalną referencję, ładuje drony według reguł i zwraca liczbę dronów, których bateria naprawdę się zmieniła. To liczba elementów, jak w lekcji 8.4.
- Żadna z tych funkcji niczego nie wypisuje ani nie odczytuje z wejścia. Nazwy funkcji i parametrów oraz ich nagłówki zapisujesz samodzielnie. Czwarta funkcja nie jest potrzebna. Możesz dodać funkcję, która tylko wypisuje flotę, jeśli dostaje ją przez `const&`.
- **`main`** przechowuje drony w jednym wektorze, zainicjalizowanym w kodzie w kolejności z tabeli. Bez osobnych zmiennych dla dronów i bez `push_back`. `main` wykonuje operacje z listy niżej, każdą **dokładnie raz, na tym samym wektorze**. Wynik każdego lotu zapisuje i na jego podstawie wypisuje `accepted` albo `refused`, bez ponownego wywoływania operacji. Nie powtarza reguł lotu ani ładowania. Program nie używa zmiennych zadeklarowanych poza funkcjami.

### Operacje

Wykonaj dokładnie te operacje, w tej kolejności:

1. lot `B-02`, koszt 15;
2. lot `B-02`, koszt 1;
3. lot `C-03`, koszt 10;
4. lot `BAD-99`, koszt 10;
5. ładowanie całej floty;
6. lot `B-02`, koszt 80;
7. lot `B-02`, koszt 1.

### Raport

Dla danych z wymagań standardowe wyjście ma być takie:

<!-- output: drone_fleet -->
```text
Drones: 4
Before:
A-01: battery 65, flights 2, grounded no
B-02: battery 35, flights 0, grounded no
C-03: battery 90, flights 4, grounded yes
D-04: battery 100, flights 1, grounded no
Fly B-02 (15): accepted
Fly B-02 (1): refused
Fly C-03 (10): refused
Fly BAD-99 (10): refused
Charged: 3
Fly B-02 (80): accepted
Fly B-02 (1): refused
After:
A-01: battery 100, flights 2, grounded no
B-02: battery 20, flights 2, grounded no
C-03: battery 100, flights 4, grounded yes
D-04: battery 100, flights 1, grounded no
```

- `Drones` pochodzi z `size()`, a `Before` i `After` pokazują wszystkie drony w kolejności z wektora.
- W linijkach lotów w nawiasie stoi koszt.
- `Charged` to wynik funkcji ładowania floty.
- Program nie wypisuje żadnych innych komunikatów ani pustych linijek.

**Wariant z pustym wektorem:** te same funkcje, pusty wektor, jeden lot `A-01` z kosztem 10 i ładowanie floty. `main` wypisuje wtedy tylko:

<!-- output: drone_fleet_empty -->
```text
Drones: 0
Fly A-01 (10): refused
Charged: 0
```

### Jak pracować

1. **Zaprojektuj typ i trzy funkcje, zanim zaczniesz pisać `main`.** Przy każdej funkcji zapisz jednym zdaniem jej zadanie, parametry i typ wyniku.
2. **Przygotuj tabelę przypadków:** dane z wymagań; pusty wektor; jeden dron; koszt 0 i koszt ujemny; lot, który zostawia dokładnie 20, i taki, który zostawiłby 19; koszt większy od baterii; uziemiony dron z pełną i z niepełną baterią; nieznany identyfikator; dron na pierwszej, środkowej i ostatniej pozycji; dwa loty tego samego drona z ładowaniem pomiędzy nimi; ładowanie, gdy wszystkie baterie są pełne, i gdy żadna nie jest, dwa razy z rzędu. Przy każdej operacji zapisz wynik i stan drona, którego dotyczy. **Stan po odmowie sprawdzaj od razu po niej**, a nie tylko na końcu: późniejsze ładowanie może ukryć baterię zmienioną przez odrzucony lot.
3. **Uruchom program** dla danych z wymagań i dla wariantu z pustym wektorem. Pozostałe przypadki przeanalizuj na papierze. Wszystkie przypadki z pełnej listy kontrolnej są sprawdzone automatycznie.

Gdy wynik się zgadza, możesz zapisać projekt w Gicie, jak w lekcji 1.5. Przed commitem sprawdź `git status`: do historii trafiają tylko `main.cpp` i `CMakeLists.txt`.

## Kryteria sukcesu

Sprawdzian jest zaliczony, gdy spełniasz **wszystkie** kryteria. Możesz przy tym korzystać z części B, jeśli uczciwie zaznaczysz to w samoocenie.

- `drone_fleet/main.cpp` napisano od pustego pliku, w poprawnym C++20. Program buduje się bez błędów.
- Jest jeden typ drona z czterema polami wymaganych typów, a drony stoją w jednym wektorze, w kolejności z tabeli.
- Funkcja lotu jednego drona dostaje rekord przez `&`, a koszt przez wartość. Sprawdza wszystkie trzy warunki, zanim cokolwiek zmieni. Przy odmowie nie zmienia żadnego pola, a przy powodzeniu zmienia dokładnie baterię i liczbę lotów.
- Funkcja lotu po identyfikatorze dostaje wektor przez `&`, a identyfikator przez `const std::string&`, zmienia prawdziwy element, korzysta z funkcji lotu jednego drona i zwraca `false` dopiero po przejrzeniu wszystkich dronów.
- Funkcja ładowania floty zmienia tylko baterię, nie znosi uziemienia i liczy tylko drony, których bateria naprawdę się zmieniła.
- Żadna z trzech funkcji niczego nie wypisuje ani nie odczytuje. Reguły lotu i ładowania stoją w programie w jednym miejscu.
- Standardowe wyjście dla danych z wymagań i dla wariantu z pustym wektorem zgadza się z wymaganiami. Pozostałe przypadki zgadzają się z Twoją analizą na papierze i z pełną listą kontrolną.
- Błąd z diagnostyki A poprawiono i sprawdzono, a fragment z diagnostyki B przeanalizowano bez uruchamiania (zadanie 2 w części B).
- Umiesz wyjaśnić każdą linijkę swojego programu i odpowiedzieć na pytania z zadania 3.

Nazwy typu, pól, funkcji i zmiennych oraz podział `main` mogą być inne niż w rozwiązaniu referencyjnym, jeśli są czytelne i spełniają wymagania. Poprawny wynik to warunek konieczny, ale **nie dowód zrozumienia**. Dlatego zadania 2 i 3 są częścią sprawdzianu.

---

# Część B: sprawdzenie i omówienie

Przejdź tutaj **dopiero po wykonaniu części A** albo wtedy, gdy świadomie zrezygnujesz z dalszej samodzielnej próby. Ta część zawiera kod bardzo zbliżony do rozwiązania zadania 1.

## Jak sprawdzić swoją pracę

- **Standardowe wyjście:** porównaj linijki programu z oczekiwanymi, znak po znaku, także koszty w nawiasach i kolejność dronów.
- **Stan po odmowie:** dla każdego odrzuconego lotu sprawdź, że wszystkie cztery pola drona są takie same jak przed nim. Pełna lista kontrolna pokazuje stan floty po każdej operacji.
- **Funkcje:** czy każda ma zadanie, które da się opisać jednym zdaniem? Czy warunek rezerwy albo ładowania stoi też w `main`?
- **Wynik a skutek:** `accepted` mówi, że funkcja zgłosiła lot. Czy zmienił się prawdziwy rekord, pokazuje dopiero `After`.

## Podpowiedzi

<details>
<summary>Podpowiedź 1</summary>

Które operacje dotyczą jednego drona, a które całej floty? Która z nich musi wyszukać rekord po identyfikatorze?

</details>

<details>
<summary>Podpowiedź 2</summary>

Sprawdzaj warunki lotu przed zmianą baterii i licznika. Funkcja szukająca drona powinna korzystać z funkcji wykonującej lot.

</details>

<details>
<summary>Podpowiedź 3</summary>

Przy ładowaniu przeglądaj rzeczywiste rekordy przez referencję i licz tylko baterie, których wartość wzrosła. Przy odmowie lotu nie zmieniaj żadnego pola.

</details>

## Pełna lista przypadków kontrolnych

<details>
<summary>Otwórz po przygotowaniu własnej tabeli</summary>

Każdy dron jest zapisany jako identyfikator, bateria, liczba lotów i uziemienie.

| | Flota | Operacje | Wyniki | Co sprawdza |
|---|---|---|---|---|
| A | A-01 65 2 no, B-02 35 0 no, C-03 90 4 yes, D-04 100 1 no | lot B-02 15, B-02 1, C-03 10, BAD-99 10, ładowanie, B-02 80, B-02 1 | accepted, refused, refused, refused, 3, accepted, refused | dane z wymagań |
| B | pusta | lot A-01 10, ładowanie | refused, 0 | pusty wektor |
| C | S-01 50 0 no | lot S-01 30 | accepted | jeden dron; zostaje dokładnie 20 |
| D | S-01 50 0 no | lot S-01 31 | refused | zostałoby 19 |
| E | Z-01 80 3 no | lot Z-01 0, Z-01 -5 | refused, refused | koszt 0 i ujemny; dwie odmowy z rzędu |
| F | X-01 30 1 no | lot X-01 40 | refused | koszt większy od baterii |
| G | G-01 100 2 yes | lot G-01 10, ładowanie | refused, 0 | uziemiony dron z pełną baterią |
| H | G-02 40 5 yes, N-01 70 1 no | lot G-02 10, ładowanie, G-02 10 | refused, 2, refused | uziemiony dron z niepełną baterią: ładowanie nie znosi uziemienia |
| I | A-01 60 0 no, B-02 60 0 no | lot ZZ-99 10 | refused | nieznany identyfikator w niepustym wektorze |
| J | P-01 80 0 no, P-02 80 0 no, P-03 80 0 no | lot P-03 10, P-02 20, P-01 30 | accepted, accepted, accepted | dopasowanie na ostatniej, środkowej i pierwszej pozycji |
| K | R-01 60 0 no | lot R-01 30, R-01 20, ładowanie, R-01 20 | accepted, refused, 1, accepted | dwa loty jednego drona; odmowa, potem przyjęcie po ładowaniu |
| L | F-01 100 0 no, F-02 100 3 yes | ładowanie, ładowanie | 0, 0 | wszystkie baterie pełne |
| M | L-01 10 0 no, L-02 99 1 yes, L-03 0 2 no | ładowanie, ładowanie | 3, 0 | żadna bateria niepełna; ponowne ładowanie |

We wszystkich przypadkach identyfikatory, liczba dronów i ich kolejność się nie zmieniają. Odrzucony lot nie zmienia żadnego pola, a ładowanie zmienia tylko baterię.

**Testy automatyczne i Twoje próby.** Wszystkie przypadki są sprawdzone automatycznie przez program kontrolny. Ma on ten sam typ i te same trzy funkcje co rozwiązanie referencyjne, ale flotę i operacje odczytuje z wejścia i **po każdej operacji wypisuje stan całej floty**. To tylko narzędzie do sprawdzania, a nie część sprawdzianu. Program kontrolny i jego wyniki są przy rozwiązaniu referencyjnym.

</details>

## Zadanie 2: Diagnostyka

Wykonaj to zadanie **po zadaniu 1**, przed zajrzeniem do rozwiązania referencyjnego. Oba problemy dotyczą funkcji podobnych do Twoich.

<details>
<summary>Diagnostyka A: zmienia się kopia drona (otwórz dopiero po zadaniu 1)</summary>

W `cpp-workspace` utwórz katalog `diagnosis_9`, skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program` i umieść w `main.cpp` program poniżej: możesz go przepisać albo skopiować. Reguły są takie same jak w zadaniu 1. Flotę wypisuje funkcja `print_fleet`, która tylko odczytuje wektor. Błąd nie jest w niej.

<!-- example: fleet_copy_bug -->
```cpp
#include <iostream>
#include <string>
#include <vector>

struct Drone {
    std::string id;
    int battery;
    int flights;
    bool grounded;
};

bool fly(Drone& drone, int cost) {
    if (cost <= 0 || drone.grounded) {
        return false;
    }

    if (drone.battery - cost < 20) {
        return false;
    }

    drone.battery -= cost;
    ++drone.flights;
    return true;
}

bool fly_by_id(std::vector<Drone>& drones, const std::string& id, int cost) {
    for (Drone drone : drones) {
        if (drone.id == id) {
            return fly(drone, cost);
        }
    }

    return false;
}

void print_fleet(const std::vector<Drone>& drones) {
    for (const Drone& drone : drones) {
        std::cout << drone.id << ": battery " << drone.battery << ", flights " << drone.flights << ", grounded ";

        if (drone.grounded) {
            std::cout << "yes\n";
        } else {
            std::cout << "no\n";
        }
    }
}

int main() {
    std::vector<Drone> drones{
        {"A-01", 65, 2, false},
        {"B-02", 35, 0, false}
    };
    const std::string id{"B-02"};
    const int cost{0};

    std::cout << "Before:\n";
    print_fleet(drones);

    const bool flown{fly_by_id(drones, id, cost)};

    if (flown) {
        std::cout << "Fly " << id << " (" << cost << "): accepted\n";
    } else {
        std::cout << "Fly " << id << " (" << cost << "): refused\n";
    }

    std::cout << "After:\n";
    print_fleet(drones);
}
```

1. **Przewidź** wynik dla danych z programu: koszt 0, czyli żądanie, które powinno zostać odrzucone. Potem uruchom program. Czy wynik wygląda poprawnie?
2. Zmień dane tak, żeby błąd stał się widoczny. Zapisz poprawny wynik i stan obu dronów dla swoich danych.
3. **Przewidź**, co wypisze ten program dla Twoich danych: wynik lotu i stan obu dronów. Potem uruchom program.
4. Wskaż miejsce, w którym powstaje kopia.
5. Wyjaśnij, dlaczego funkcja lotu jednego drona działa poprawnie, a funkcja lotu po identyfikatorze nie spełnia swojej umowy.
6. Popraw program i uruchom go ponownie dla swoich danych.

</details>

<details>
<summary>Diagnostyka B: bateria zmienia się przed sprawdzeniem rezerwy (otwórz dopiero po zadaniu 1)</summary>

Ten fragment przeanalizuj **na papierze**, bez uruchamiania. To inna wersja funkcji lotu jednego drona:

<!-- fragment -->
```cpp
bool fly(Drone& drone, int cost) {
    if (cost <= 0 || drone.grounded) {
        return false;
    }

    drone.battery -= cost;

    if (drone.battery < 20) {
        return false;
    }

    ++drone.flights;
    return true;
}
```

Dron ma baterię 25, nie jest uziemiony i ma 3 loty. Żądany lot kosztuje 10.

1. Jaki jest poprawny wynik i stan drona po tym żądaniu?
2. Co zwraca ta wersja i jaki stan drona zostawia?
3. Które sprawdzenie odbywa się za późno? Dlaczego to narusza zasadę „wszystko albo nic”?
4. Dlaczego `return false;` nie cofa wcześniejszej zmiany?
5. Jak zmienić kolejność, żeby odmowa niczego nie zmieniała?

</details>

Wyniki, przykładowe dane i poprawki są w części [Diagnostyka: wyniki i poprawki](#diagnostyka-wyniki-i-poprawki).

## Zadanie 3: Wyjaśnij swój projekt

Odpowiedz krótko, na piśmie, odwołując się do własnego programu z zadania 1, zanim otworzysz rozwiązanie referencyjne:

1. Dlaczego funkcja lotu jednego drona dostaje rekord przez `&`, a obie funkcje dla floty dostają wektor przez `&`? Dlaczego zmienne pętli w tych funkcjach też mają `&`?
2. Co oznacza `false` zwrócone przez funkcję lotu po identyfikatorze? Czy po nim wiadomo, czy dron istnieje?
3. Dlaczego bateria 20 po locie jest dozwolona, a 19 nie? Wskaż te przypadki w swojej tabeli.
4. Dlaczego odrzucony lot nie może zmienić żadnego pola? Co stałoby się z kolejnymi lotami tego drona, gdyby odmowa zmieniała baterię?
5. Dlaczego ładowanie nie zmienia uziemienia ani liczby lotów, a dron z baterią 100 nie jest liczony?
6. Dlaczego wszystkie siedem operacji musi działać na tym samym wektorze? Co pokazują dwa loty `B-02` z ładowaniem pomiędzy nimi?
7. Czy wynik `accepted` dowodzi, że zmienił się właściwy rekord? Jak to sprawdzasz?
8. Dlaczego reguły lotu zna tylko jedna funkcja? Jakie zadania mają pozostałe dwie?

## Rozwiązanie referencyjne

Zajrzyj tutaj **po wykonaniu zadań 1–3**. Twoje nazwy i układ `main` mogą być inne, jeśli program spełnia wymagania.

<details>
<summary>Zadanie 1: flota dronów dostawczych</summary>

<!-- example: drone_fleet -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>
#include <vector>

struct Drone {
    std::string id;
    int battery;
    int flights;
    bool grounded;
};

bool fly(Drone& drone, int cost) {
    if (cost <= 0 || drone.grounded) {
        return false;
    }

    if (drone.battery - cost < 20) {
        return false;
    }

    drone.battery -= cost;
    ++drone.flights;
    return true;
}

bool fly_by_id(std::vector<Drone>& drones, const std::string& id, int cost) {
    for (Drone& drone : drones) {
        if (drone.id == id) {
            return fly(drone, cost);
        }
    }

    return false;
}

std::size_t charge_fleet(std::vector<Drone>& drones) {
    std::size_t charged{0};

    for (Drone& drone : drones) {
        if (drone.battery < 100) {
            drone.battery = 100;
            ++charged;
        }
    }

    return charged;
}

int main() {
    std::vector<Drone> drones{
        {"A-01", 65, 2, false},
        {"B-02", 35, 0, false},
        {"C-03", 90, 4, true},
        {"D-04", 100, 1, false}
    };

    std::cout << "Drones: " << drones.size() << "\n";
    std::cout << "Before:\n";

    for (const Drone& drone : drones) {
        std::cout << drone.id << ": battery " << drone.battery << ", flights " << drone.flights << ", grounded ";

        if (drone.grounded) {
            std::cout << "yes\n";
        } else {
            std::cout << "no\n";
        }
    }

    const bool first_flight{fly_by_id(drones, "B-02", 15)};

    if (first_flight) {
        std::cout << "Fly B-02 (15): accepted\n";
    } else {
        std::cout << "Fly B-02 (15): refused\n";
    }

    const bool second_flight{fly_by_id(drones, "B-02", 1)};

    if (second_flight) {
        std::cout << "Fly B-02 (1): accepted\n";
    } else {
        std::cout << "Fly B-02 (1): refused\n";
    }

    const bool third_flight{fly_by_id(drones, "C-03", 10)};

    if (third_flight) {
        std::cout << "Fly C-03 (10): accepted\n";
    } else {
        std::cout << "Fly C-03 (10): refused\n";
    }

    const bool fourth_flight{fly_by_id(drones, "BAD-99", 10)};

    if (fourth_flight) {
        std::cout << "Fly BAD-99 (10): accepted\n";
    } else {
        std::cout << "Fly BAD-99 (10): refused\n";
    }

    const std::size_t charged{charge_fleet(drones)};

    std::cout << "Charged: " << charged << "\n";

    const bool fifth_flight{fly_by_id(drones, "B-02", 80)};

    if (fifth_flight) {
        std::cout << "Fly B-02 (80): accepted\n";
    } else {
        std::cout << "Fly B-02 (80): refused\n";
    }

    const bool sixth_flight{fly_by_id(drones, "B-02", 1)};

    if (sixth_flight) {
        std::cout << "Fly B-02 (1): accepted\n";
    } else {
        std::cout << "Fly B-02 (1): refused\n";
    }

    std::cout << "After:\n";

    for (const Drone& drone : drones) {
        std::cout << drone.id << ": battery " << drone.battery << ", flights " << drone.flights << ", grounded ";

        if (drone.grounded) {
            std::cout << "yes\n";
        } else {
            std::cout << "no\n";
        }
    }
}
```

1. **Jeden typ wystarcza,** bo każda operacja zmienia drony, a wyniki to pojedyncza odpowiedź `bool` albo jedna liczba. Osobny typ podsumowania nie jest potrzebny.
2. **`fly` dostaje `Drone&`,** bo lot ma zmienić istniejący rekord, a nie jego kopię.
3. **`fly_by_id` dostaje `std::vector<Drone>&`** i przegląda go pętlą `Drone&`, bo znaleziony dron ma się zmienić w wektorze z `main`.
4. **Identyfikator przez `const std::string&`,** bo funkcja tylko go odczytuje i porównuje.
5. **`charge_fleet` używa pętli `Drone&`,** bo zmienia baterie prawdziwych elementów. Pętla bez `&` zmieniałaby kopie.
6. **`bool` oznacza powodzenie lotu, a nie znalezienie drona:** `false` znaczy „lot się nie odbył”, z braku drona albo z odmowy.
7. **Koszt 0 i ujemny są odrzucane,** bo lot za 0 dodałby lot bez zużycia baterii, a ujemny koszt zwiększyłby baterię. Sprawdzenie stoi na początku, więc rezerwa jest liczona tylko dla dodatniego kosztu.
8. **Uziemiony dron jest odrzucany** niezależnie od baterii: to drugi warunek tej samej klauzuli.
9. **Bateria 20 po locie jest dozwolona,** bo rezerwa to „co najmniej 20”. Warunek odmowy to `drone.battery - cost < 20`, a 20 nie jest mniejsze od 20.
10. **19 oznacza odmowę,** bo 19 jest mniejsze od 20.
11. **Przy odmowie nic się nie zmienia,** bo obie klauzule ochronne stoją przed zmianami. Planowaną baterię oblicza wyrażenie w warunku, a pole zmienia się dopiero po sprawdzeniu.
12. **Ładowanie nie zmienia `grounded`,** bo uziemienie to osobna decyzja, a nie stan baterii. C-03 po naładowaniu nadal nie może latać.
13. **Ładowanie nie zwiększa `flights`,** bo żaden lot się nie odbył.
14. **Dron z baterią 100 nie jest liczony,** bo jego bateria się nie zmienia, a wynik ma mówić o rzeczywistych zmianach.
15. **Kolejne wywołania korzystają ze stanu po poprzednich,** bo wszystkie dotyczą tego samego wektora: drugi lot `B-02` widzi baterię 20, a lot za 80 jest możliwy dopiero po ładowaniu.
16. **Nowa kolekcja nie jest potrzebna,** bo flota przedstawia bieżący stan, a stan sprzed operacji nie jest potrzebny w raporcie.
17. **`accepted` nie dowodzi zmiany oryginału:** funkcja może poprawnie zmienić kopię i zgłosić lot (diagnostyka A). Dowodem jest dopiero stan w `After`.
18. **Trzy odpowiedzialności:** `fly` zna reguły jednego lotu i chroni stan jednego drona; `fly_by_id` znajduje właściwy rekord i przekazuje go do `fly`; `charge_fleet` zmienia wszystkie rekordy, które tego potrzebują.

**Inne poprawne rozwiązania:**

- jedna klauzula ochronna z trzema warunkami połączonymi przez `||`, jeśli koszt jest sprawdzany jako pierwszy;
- warunek rezerwy zapisany jako `cost > drone.battery - 20`;
- lokalna stała, na przykład `const int reserve{20};`, w funkcji lotu;
- własna funkcja wypisująca flotę, która dostaje wektor przez `const&`, wywołana dla `Before` i `After`;
- osobna funkcja ładująca jednego drona, wywoływana przez funkcję ładowania floty.

To nie jedyne poprawne rozwiązanie.

**Wariant z pustym wektorem:**

<!-- example: drone_fleet_empty -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>
#include <vector>

struct Drone {
    std::string id;
    int battery;
    int flights;
    bool grounded;
};

bool fly(Drone& drone, int cost) {
    if (cost <= 0 || drone.grounded) {
        return false;
    }

    if (drone.battery - cost < 20) {
        return false;
    }

    drone.battery -= cost;
    ++drone.flights;
    return true;
}

bool fly_by_id(std::vector<Drone>& drones, const std::string& id, int cost) {
    for (Drone& drone : drones) {
        if (drone.id == id) {
            return fly(drone, cost);
        }
    }

    return false;
}

std::size_t charge_fleet(std::vector<Drone>& drones) {
    std::size_t charged{0};

    for (Drone& drone : drones) {
        if (drone.battery < 100) {
            drone.battery = 100;
            ++charged;
        }
    }

    return charged;
}

int main() {
    std::vector<Drone> drones{};

    std::cout << "Drones: " << drones.size() << "\n";

    const bool flown{fly_by_id(drones, "A-01", 10)};

    if (flown) {
        std::cout << "Fly A-01 (10): accepted\n";
    } else {
        std::cout << "Fly A-01 (10): refused\n";
    }

    const std::size_t charged{charge_fleet(drones)};

    std::cout << "Charged: " << charged << "\n";
}
```

Dla pustego wektora obie pętle wykonują zero przebiegów: `fly_by_id` dochodzi do `return false;` za pętlą, a `charge_fleet` zwraca 0. Żaden element nie jest odczytywany.

**Program kontrolny** sprawdza wszystkie przypadki z listy kontrolnej. Typ i trzy funkcje są takie same jak wyżej. Różnica jest w `main`: program odczytuje liczbę dronów, potem każdego drona (identyfikator, baterię, liczbę lotów i `yes` albo `no` dla uziemienia), a potem liczbę operacji. Każdy dron trafia na koniec wektora przez `push_back`, jak w programach kontrolnych lekcji 8.4–9.4. Operację, czyli `fly` z identyfikatorem i kosztem albo `charge`, odczytuje po jednej, dopiero w pętli operacji, i od razu ją wykonuje. **Po każdej operacji wypisuje stan całej floty**, żeby stan po odmowie był widoczny od razu. Do wypisywania służy funkcja `print_fleet`, która tylko odczytuje wektor.

<!-- example: drone_fleet_check -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>
#include <vector>

struct Drone {
    std::string id;
    int battery;
    int flights;
    bool grounded;
};

bool fly(Drone& drone, int cost) {
    if (cost <= 0 || drone.grounded) {
        return false;
    }

    if (drone.battery - cost < 20) {
        return false;
    }

    drone.battery -= cost;
    ++drone.flights;
    return true;
}

bool fly_by_id(std::vector<Drone>& drones, const std::string& id, int cost) {
    for (Drone& drone : drones) {
        if (drone.id == id) {
            return fly(drone, cost);
        }
    }

    return false;
}

std::size_t charge_fleet(std::vector<Drone>& drones) {
    std::size_t charged{0};

    for (Drone& drone : drones) {
        if (drone.battery < 100) {
            drone.battery = 100;
            ++charged;
        }
    }

    return charged;
}

void print_fleet(const std::vector<Drone>& drones) {
    for (const Drone& drone : drones) {
        std::cout << drone.id << ": battery " << drone.battery << ", flights " << drone.flights << ", grounded ";

        if (drone.grounded) {
            std::cout << "yes\n";
        } else {
            std::cout << "no\n";
        }
    }
}

int main() {
    std::vector<Drone> drones{};
    int count{0};

    std::cin >> count;

    for (int number{1}; number <= count; ++number) {
        std::string id{};
        int battery{0};
        int flights{0};
        std::string grounded_answer{};

        std::cin >> id;
        std::cin >> battery;
        std::cin >> flights;
        std::cin >> grounded_answer;

        const Drone drone{id, battery, flights, grounded_answer == "yes"};
        drones.push_back(drone);
    }

    int operation_count{0};
    std::cin >> operation_count;

    if (std::cin.fail()) {
        std::cout << "Input could not be read\n";
    } else {
        std::cout << "Drones: " << drones.size() << "\n";
        std::cout << "Before:\n";
        print_fleet(drones);

        for (int number{1}; number <= operation_count; ++number) {
            std::string operation{};
            std::cin >> operation;

            if (operation == "fly") {
                std::string id{};
                int cost{0};

                std::cin >> id;
                std::cin >> cost;

                const bool flown{fly_by_id(drones, id, cost)};

                if (flown) {
                    std::cout << "Fly " << id << " (" << cost << "): accepted\n";
                } else {
                    std::cout << "Fly " << id << " (" << cost << "): refused\n";
                }
            } else {
                const std::size_t charged{charge_fleet(drones)};

                std::cout << "Charged: " << charged << "\n";
            }

            print_fleet(drones);
        }
    }
}
```

Każdy przypadek zaczyna się od liczby dronów. Potem każdy dron zajmuje jedną linijkę: identyfikator, bateria, liczba lotów i uziemienie. Dalej stoi liczba operacji i operacje, po jednej w linijce. Przypadki stoją w kolejności z listy kontrolnej, od A do M.

<!-- input: drone_fleet_check -->
```text
4
A-01 65 2 no
B-02 35 0 no
C-03 90 4 yes
D-04 100 1 no
7
fly B-02 15
fly B-02 1
fly C-03 10
fly BAD-99 10
charge
fly B-02 80
fly B-02 1
```

<!-- output: drone_fleet_check -->
```text
Drones: 4
Before:
A-01: battery 65, flights 2, grounded no
B-02: battery 35, flights 0, grounded no
C-03: battery 90, flights 4, grounded yes
D-04: battery 100, flights 1, grounded no
Fly B-02 (15): accepted
A-01: battery 65, flights 2, grounded no
B-02: battery 20, flights 1, grounded no
C-03: battery 90, flights 4, grounded yes
D-04: battery 100, flights 1, grounded no
Fly B-02 (1): refused
A-01: battery 65, flights 2, grounded no
B-02: battery 20, flights 1, grounded no
C-03: battery 90, flights 4, grounded yes
D-04: battery 100, flights 1, grounded no
Fly C-03 (10): refused
A-01: battery 65, flights 2, grounded no
B-02: battery 20, flights 1, grounded no
C-03: battery 90, flights 4, grounded yes
D-04: battery 100, flights 1, grounded no
Fly BAD-99 (10): refused
A-01: battery 65, flights 2, grounded no
B-02: battery 20, flights 1, grounded no
C-03: battery 90, flights 4, grounded yes
D-04: battery 100, flights 1, grounded no
Charged: 3
A-01: battery 100, flights 2, grounded no
B-02: battery 100, flights 1, grounded no
C-03: battery 100, flights 4, grounded yes
D-04: battery 100, flights 1, grounded no
Fly B-02 (80): accepted
A-01: battery 100, flights 2, grounded no
B-02: battery 20, flights 2, grounded no
C-03: battery 100, flights 4, grounded yes
D-04: battery 100, flights 1, grounded no
Fly B-02 (1): refused
A-01: battery 100, flights 2, grounded no
B-02: battery 20, flights 2, grounded no
C-03: battery 100, flights 4, grounded yes
D-04: battery 100, flights 1, grounded no
```

<!-- input: drone_fleet_check -->
```text
0
2
fly A-01 10
charge
```

<!-- output: drone_fleet_check -->
```text
Drones: 0
Before:
Fly A-01 (10): refused
Charged: 0
```

<!-- input: drone_fleet_check -->
```text
1
S-01 50 0 no
1
fly S-01 30
```

<!-- output: drone_fleet_check -->
```text
Drones: 1
Before:
S-01: battery 50, flights 0, grounded no
Fly S-01 (30): accepted
S-01: battery 20, flights 1, grounded no
```

<!-- input: drone_fleet_check -->
```text
1
S-01 50 0 no
1
fly S-01 31
```

<!-- output: drone_fleet_check -->
```text
Drones: 1
Before:
S-01: battery 50, flights 0, grounded no
Fly S-01 (31): refused
S-01: battery 50, flights 0, grounded no
```

<!-- input: drone_fleet_check -->
```text
1
Z-01 80 3 no
2
fly Z-01 0
fly Z-01 -5
```

<!-- output: drone_fleet_check -->
```text
Drones: 1
Before:
Z-01: battery 80, flights 3, grounded no
Fly Z-01 (0): refused
Z-01: battery 80, flights 3, grounded no
Fly Z-01 (-5): refused
Z-01: battery 80, flights 3, grounded no
```

<!-- input: drone_fleet_check -->
```text
1
X-01 30 1 no
1
fly X-01 40
```

<!-- output: drone_fleet_check -->
```text
Drones: 1
Before:
X-01: battery 30, flights 1, grounded no
Fly X-01 (40): refused
X-01: battery 30, flights 1, grounded no
```

<!-- input: drone_fleet_check -->
```text
1
G-01 100 2 yes
2
fly G-01 10
charge
```

<!-- output: drone_fleet_check -->
```text
Drones: 1
Before:
G-01: battery 100, flights 2, grounded yes
Fly G-01 (10): refused
G-01: battery 100, flights 2, grounded yes
Charged: 0
G-01: battery 100, flights 2, grounded yes
```

<!-- input: drone_fleet_check -->
```text
2
G-02 40 5 yes
N-01 70 1 no
3
fly G-02 10
charge
fly G-02 10
```

<!-- output: drone_fleet_check -->
```text
Drones: 2
Before:
G-02: battery 40, flights 5, grounded yes
N-01: battery 70, flights 1, grounded no
Fly G-02 (10): refused
G-02: battery 40, flights 5, grounded yes
N-01: battery 70, flights 1, grounded no
Charged: 2
G-02: battery 100, flights 5, grounded yes
N-01: battery 100, flights 1, grounded no
Fly G-02 (10): refused
G-02: battery 100, flights 5, grounded yes
N-01: battery 100, flights 1, grounded no
```

<!-- input: drone_fleet_check -->
```text
2
A-01 60 0 no
B-02 60 0 no
1
fly ZZ-99 10
```

<!-- output: drone_fleet_check -->
```text
Drones: 2
Before:
A-01: battery 60, flights 0, grounded no
B-02: battery 60, flights 0, grounded no
Fly ZZ-99 (10): refused
A-01: battery 60, flights 0, grounded no
B-02: battery 60, flights 0, grounded no
```

<!-- input: drone_fleet_check -->
```text
3
P-01 80 0 no
P-02 80 0 no
P-03 80 0 no
3
fly P-03 10
fly P-02 20
fly P-01 30
```

<!-- output: drone_fleet_check -->
```text
Drones: 3
Before:
P-01: battery 80, flights 0, grounded no
P-02: battery 80, flights 0, grounded no
P-03: battery 80, flights 0, grounded no
Fly P-03 (10): accepted
P-01: battery 80, flights 0, grounded no
P-02: battery 80, flights 0, grounded no
P-03: battery 70, flights 1, grounded no
Fly P-02 (20): accepted
P-01: battery 80, flights 0, grounded no
P-02: battery 60, flights 1, grounded no
P-03: battery 70, flights 1, grounded no
Fly P-01 (30): accepted
P-01: battery 50, flights 1, grounded no
P-02: battery 60, flights 1, grounded no
P-03: battery 70, flights 1, grounded no
```

<!-- input: drone_fleet_check -->
```text
1
R-01 60 0 no
4
fly R-01 30
fly R-01 20
charge
fly R-01 20
```

<!-- output: drone_fleet_check -->
```text
Drones: 1
Before:
R-01: battery 60, flights 0, grounded no
Fly R-01 (30): accepted
R-01: battery 30, flights 1, grounded no
Fly R-01 (20): refused
R-01: battery 30, flights 1, grounded no
Charged: 1
R-01: battery 100, flights 1, grounded no
Fly R-01 (20): accepted
R-01: battery 80, flights 2, grounded no
```

<!-- input: drone_fleet_check -->
```text
2
F-01 100 0 no
F-02 100 3 yes
2
charge
charge
```

<!-- output: drone_fleet_check -->
```text
Drones: 2
Before:
F-01: battery 100, flights 0, grounded no
F-02: battery 100, flights 3, grounded yes
Charged: 0
F-01: battery 100, flights 0, grounded no
F-02: battery 100, flights 3, grounded yes
Charged: 0
F-01: battery 100, flights 0, grounded no
F-02: battery 100, flights 3, grounded yes
```

<!-- input: drone_fleet_check -->
```text
3
L-01 10 0 no
L-02 99 1 yes
L-03 0 2 no
2
charge
charge
```

<!-- output: drone_fleet_check -->
```text
Drones: 3
Before:
L-01: battery 10, flights 0, grounded no
L-02: battery 99, flights 1, grounded yes
L-03: battery 0, flights 2, grounded no
Charged: 3
L-01: battery 100, flights 0, grounded no
L-02: battery 100, flights 1, grounded yes
L-03: battery 100, flights 2, grounded no
Charged: 0
L-01: battery 100, flights 0, grounded no
L-02: battery 100, flights 1, grounded yes
L-03: battery 100, flights 2, grounded no
```

</details>

## Diagnostyka: wyniki i poprawki

<details>
<summary>Diagnostyka A: zmienia się kopia drona</summary>

Przed poprawką, dla kosztu 0:

<!-- output: fleet_copy_bug -->
```text
Before:
A-01: battery 65, flights 2, grounded no
B-02: battery 35, flights 0, grounded no
Fly B-02 (0): refused
After:
A-01: battery 65, flights 2, grounded no
B-02: battery 35, flights 0, grounded no
```

- **Dla kosztu 0 wynik jest poprawny,** bo funkcja lotu jednego drona odrzuca takie żądanie, zanim cokolwiek zmieni. Poprawna wersja też zwraca `false` i niczego nie zmienia.
- **Dane, które ujawniają błąd:** każdy lot, który powinien zostać przyjęty. Na przykład `B-02` z kosztem 15. Poprawny wynik to `accepted` i `B-02: battery 20, flights 1`. Program z błędem wypisuje:

<!-- example: fleet_copy_revealed -->
```cpp
#include <iostream>
#include <string>
#include <vector>

struct Drone {
    std::string id;
    int battery;
    int flights;
    bool grounded;
};

bool fly(Drone& drone, int cost) {
    if (cost <= 0 || drone.grounded) {
        return false;
    }

    if (drone.battery - cost < 20) {
        return false;
    }

    drone.battery -= cost;
    ++drone.flights;
    return true;
}

bool fly_by_id(std::vector<Drone>& drones, const std::string& id, int cost) {
    for (Drone drone : drones) {
        if (drone.id == id) {
            return fly(drone, cost);
        }
    }

    return false;
}

void print_fleet(const std::vector<Drone>& drones) {
    for (const Drone& drone : drones) {
        std::cout << drone.id << ": battery " << drone.battery << ", flights " << drone.flights << ", grounded ";

        if (drone.grounded) {
            std::cout << "yes\n";
        } else {
            std::cout << "no\n";
        }
    }
}

int main() {
    std::vector<Drone> drones{
        {"A-01", 65, 2, false},
        {"B-02", 35, 0, false}
    };
    const std::string id{"B-02"};
    const int cost{15};

    std::cout << "Before:\n";
    print_fleet(drones);

    const bool flown{fly_by_id(drones, id, cost)};

    if (flown) {
        std::cout << "Fly " << id << " (" << cost << "): accepted\n";
    } else {
        std::cout << "Fly " << id << " (" << cost << "): refused\n";
    }

    std::cout << "After:\n";
    print_fleet(drones);
}
```

<!-- output: fleet_copy_revealed -->
```text
Before:
A-01: battery 65, flights 2, grounded no
B-02: battery 35, flights 0, grounded no
Fly B-02 (15): accepted
After:
A-01: battery 65, flights 2, grounded no
B-02: battery 35, flights 0, grounded no
```

| Chwila | `drone` w pętli (kopia) | `B-02` w wektorze |
|---|---|---|
| przed wywołaniem | nie istnieje | battery 35, flights 0 |
| drugi przebieg: `drone.id == id` | kopia `B-02`: battery 35, flights 0 | battery 35, flights 0 |
| po `fly(drone, cost)` | battery 20, flights 1; wynik `true` | battery 35, flights 0 |
| po powrocie do `main` | nie istnieje | battery 35, flights 0 |

- **Gdzie powstaje kopia:** w pętli `for (Drone drone : drones)`. W każdym przebiegu `drone` to nowy obiekt z wartościami bieżącego elementu.
- **`fly` działa poprawnie:** sprawdza warunki, zmienia obiekt, który dostaje, i zgłasza lot. Dostaje jednak kopię. `fly_by_id` łamie swoją umowę: zgłasza wykonany lot, a dron w wektorze się nie zmienia.
- **Wynik nie zastępuje sprawdzenia skutku.** `accepted` jest wypisane, a stan w `After` jest stary. Gdyby raport pokazywał tylko wyniki, błąd zostałby niezauważony.
- **Poprawka:** zmienna pętli `Drone& drone`. Kompilator nie zgłasza błędu w wersji z kopią, bo to poprawny C++: zmiana kopii jest dozwolona, tylko nie pasuje do zadania funkcji.

<!-- example: fleet_copy_fixed -->
```cpp
#include <iostream>
#include <string>
#include <vector>

struct Drone {
    std::string id;
    int battery;
    int flights;
    bool grounded;
};

bool fly(Drone& drone, int cost) {
    if (cost <= 0 || drone.grounded) {
        return false;
    }

    if (drone.battery - cost < 20) {
        return false;
    }

    drone.battery -= cost;
    ++drone.flights;
    return true;
}

bool fly_by_id(std::vector<Drone>& drones, const std::string& id, int cost) {
    for (Drone& drone : drones) {
        if (drone.id == id) {
            return fly(drone, cost);
        }
    }

    return false;
}

void print_fleet(const std::vector<Drone>& drones) {
    for (const Drone& drone : drones) {
        std::cout << drone.id << ": battery " << drone.battery << ", flights " << drone.flights << ", grounded ";

        if (drone.grounded) {
            std::cout << "yes\n";
        } else {
            std::cout << "no\n";
        }
    }
}

int main() {
    std::vector<Drone> drones{
        {"A-01", 65, 2, false},
        {"B-02", 35, 0, false}
    };
    const std::string id{"B-02"};
    const int cost{15};

    std::cout << "Before:\n";
    print_fleet(drones);

    const bool flown{fly_by_id(drones, id, cost)};

    if (flown) {
        std::cout << "Fly " << id << " (" << cost << "): accepted\n";
    } else {
        std::cout << "Fly " << id << " (" << cost << "): refused\n";
    }

    std::cout << "After:\n";
    print_fleet(drones);
}
```

<!-- output: fleet_copy_fixed -->
```text
Before:
A-01: battery 65, flights 2, grounded no
B-02: battery 35, flights 0, grounded no
Fly B-02 (15): accepted
After:
A-01: battery 65, flights 2, grounded no
B-02: battery 20, flights 1, grounded no
```

Dla kosztu 0 poprawiony program wypisuje to samo co przed poprawką. Dlatego żądanie odrzucone nie wystarczy, żeby sprawdzić, czy funkcja zmienia prawdziwy element.

</details>

<details>
<summary>Diagnostyka B: bateria zmienia się przed sprawdzeniem rezerwy</summary>

1. **Poprawnie:** odmowa, bo 25 − 10 = 15, a to mniej niż rezerwa 20. Dron zostaje bez zmian: bateria 25, 3 loty.
2. **Ta wersja** zwraca `false`, ale zostawia baterię 15. Liczba lotów zostaje 3, bo `++drone.flights;` stoi za drugim sprawdzeniem. Rekord jest częściowo zmieniony.
3. **Za późno odbywa się sprawdzenie rezerwy.** Funkcja zmienia baterię, zanim wie, czy lot jest dozwolony. Odmowa powinna zostawić wszystkie pola bez zmian, a tu jedno pole już się zmieniło: to łamie zasadę „wszystko albo nic” z lekcji 9.2.
4. **`return false;` tylko kończy funkcję** i przekazuje wynik. Nie przywraca wcześniejszych wartości pól: zmiana baterii już się wykonała na prawdziwym rekordzie.
5. **Poprawka:** sprawdź rezerwę na planowanej baterii, zanim zmienisz pole, na przykład `if (drone.battery - cost < 20) { return false; }`, a obie zmiany wykonaj dopiero po wszystkich sprawdzeniach, jak w rozwiązaniu referencyjnym.

Taki błąd łatwo przeoczyć w całej sekwencji: późniejsze ładowanie ustawia baterię na 100 i ukrywa zmianę z odrzuconego lotu. Dlatego stan po odmowie sprawdza się od razu po niej.

</details>

## Odpowiedzi do zadania 3

<details>
<summary>Przykładowe odpowiedzi</summary>

1. Bo wszystkie trzy funkcje mają zmieniać istniejące dane z `main`. Rekord przez `&` daje dostęp do prawdziwego drona, wektor przez `&` do prawdziwej floty, a zmienna pętli `&` do jej prawdziwych elementów. Bez któregokolwiek z nich zmieniałaby się kopia.
2. Że lot się nie odbył i nic się nie zmieniło. Nie wiadomo, czy drona nie było, czy lot odrzucono: wynik mówi tylko o powodzeniu operacji, jak w lekcji 9.4.
3. Bo rezerwa to „co najmniej 20 po locie”, a warunek odmowy to bateria po locie mniejsza od 20. W liście kontrolnej przypadek C zostawia dokładnie 20 i jest przyjęty, a przypadek D zostawiłby 19 i jest odrzucony.
4. Bo umowa mówi, że odmowa nic nie zmienia. Gdyby odmowa zmniejszała baterię, kolejne loty tego drona widziałyby za niską baterię i mogłyby zostać odrzucone bez powodu, a raport pokazywałby stan, którego nie ma.
5. Bo ładowanie dotyczy tylko baterii: uziemienie i loty to inne informacje, a żaden lot się nie odbył. Dron z baterią 100 się nie zmienia, więc nie jest liczony: wynik ma mówić o rzeczywistych zmianach.
6. Bo każda operacja ma zaczynać od stanu po poprzednich. Drugi lot `B-02` za 1 jest odrzucony, bo zostało 20; lot za 80 jest możliwy dopiero po ładowaniu, a ostatni lot za 1 znowu natrafia na rezerwę.
7. Nie. Funkcja może zmienić kopię i zgłosić lot, jak w diagnostyce A. Sprawdzam to stanem floty w `After` i w przypadkach kontrolnych, które pokazują stan po każdej operacji.
8. Bo reguła powinna być w jednym miejscu, a jej zmiana ma wymagać poprawienia jednej funkcji. Funkcja lotu po identyfikatorze tylko znajduje drona i przekazuje go do funkcji lotu. Funkcja ładowania ma własną, inną regułę i nie potrzebuje reguł lotu.

</details>

## Samoocena

Przy każdym kryterium zaznacz jedną odpowiedź:

| Kryterium | Samodzielnie | Z podpowiedzią | Po zajrzeniu do rozwiązania | Do powtórki |
|---|---|---|---|---|
| Projekt typu drona | | | | |
| Wektor dronów zainicjalizowany w kodzie | | | | |
| Funkcja lotu: `&`, wszystkie warunki przed zmianą, dwa pola | | | | |
| Rezerwa: granica 20 i 19 | | | | |
| Koszt 0 i ujemny, uziemienie | | | | |
| Funkcja lotu po identyfikatorze i `return false;` za pętlą | | | | |
| Ładowanie: tylko bateria, liczenie rzeczywistych zmian | | | | |
| Uziemiony dron i ładowanie | | | | |
| Siedem operacji na tym samym wektorze | | | | |
| Wariant z pustym wektorem | | | | |
| Tabela przypadków i stan po odmowie | | | | |
| Diagnostyka A (zmienia się kopia drona) | | | | |
| Diagnostyka B (bateria przed sprawdzeniem rezerwy) | | | | |
| Wyjaśnienia z zadania 3 | | | | |

Jeśli w kolumnie „Do powtórki” jest coś zaznaczone, wróć do odpowiedniej lekcji:

| Temat | Lekcja |
|---|---|
| funkcja zmienia rekord przez `T&` | [9.1](lesson_01_a_function_changes_a_record.md) |
| sprawdzenie przed zmianą, wynik `bool`, wszystko albo nic | [9.2](lesson_02_a_change_only_when_allowed.md) |
| zmiana elementów wektora, dwa poziomy `&`, licznik rzeczywistych zmian | [9.3](lesson_03_changing_vector_elements.md) |
| wyszukanie rekordu, `return` w pętli i za pętlą | [9.4](lesson_04_find_a_record_and_change_it.md) |
| klauzule ochronne | [5.4](../module_05_functions/lesson_04_several_returns.md) |
| łączenie warunków i krótkie obliczanie | [3.4](../module_03_decisions_and_conditions/lesson_04_combining_conditions.md) |
| wektor rekordów i `std::size_t` | [8.4](../module_08_structs/lesson_04_many_records_in_a_vector.md) |

Potem spróbuj zadania jeszcze raz, na przykład dla wypożyczalni hulajnóg, w której jazda wymaga rezerwy baterii, a zablokowane hulajnogi można ładować, ale nie wypożyczać.

---

## Podsumowanie Modułu 9

Po pięciu lekcjach potrafisz:

- przekazywać istniejący rekord przez `T&`, gdy zadaniem funkcji jest jego zmiana, i odróżniać to od przekazania przez wartość i przez `const&`;
- pisać funkcje, które sprawdzają wszystkie warunki przed zmianą, przy odmowie niczego nie zmieniają i zwracają `bool`;
- zmieniać elementy istniejącego wektora w funkcji z parametrem `std::vector<T>&` i pętlą `T&`, licząc tylko rzeczywiste zmiany;
- znajdować rekord po unikalnym identyfikatorze i zmieniać tylko jego, z `return` w pętli i `return false;` za nią;
- odróżniać wynik funkcji od jej skutku i sprawdzać stan danych, a nie tylko komunikat;
- dobierać dane, które ujawniają zmianę kopii, częściową zmianę i zbyt wczesny `return`.

## Co dalej

To ostatnia lekcja Modułu 9. Kolejne moduły kursu są w przygotowaniu.

**Poprzednia lekcja:** [Lekcja 9.4: Znajdź rekord i zmień właściwy obiekt](lesson_04_find_a_record_and_change_it.md) · **Następna lekcja:** w przygotowaniu · [Opis kursu](../../README.md)

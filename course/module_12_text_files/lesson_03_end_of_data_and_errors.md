# Lekcja 12.3: Gdzie kończą się dane i gdzie jest błąd

**Polski** · [English](lesson_03_end_of_data_and_errors.en.md) · [Opis kursu](../../README.md)

> **Moduł 12, lekcja 3** · około 90–110 minut, można ją podzielić na dwa podejścia
> **Potrzebujesz:** katalogu `cpp-workspace` i oryginalnego projektu `lesson_05_first_program`, jak dotąd. Debugger nie jest w tej lekcji potrzebny.
> **Wersja pilotażowa.** Programy z tej lekcji sprawdzamy automatycznie na Windowsie, Ubuntu i macOS, z podanymi plikami danych. Kroki w CLionie (nowy plik, pole **Working directory**) są takie jak w lekcji 12.1: opisujemy je według dokumentacji CLion 2026.3, bez ręcznego sprawdzenia na każdym systemie.

## Zanim zaczniesz

Ta lekcja zakłada, że:

- odczytujesz linie przez `std::getline` i wiesz z lekcji 7.4, że pusta linia to udany odczyt z pustym tekstem, a nieudany odczyt oznacza, że nie było już żadnej linii;
- pamiętasz z lekcji 4.6 i 7.4, że odczyt ostatniej linii może się udać, choć strumień doszedł już do końca danych, więc o powodzeniu odczytu decyduje `fail()`;
- piszesz licznik, który zaczyna od 0 i rośnie o 1 (lekcja 4.2);
- przekazujesz do funkcji istniejący obiekt przez referencję bez `const`, żeby funkcja mogła go zmienić, także wektor (lekcje 9.1 i 9.3);
- znasz program z lekcji 12.2, jego kontrakt danych i przypadek I, w którym pusta linia między przesyłkami kończyła odczyt;
- otwierasz plik przez `std::ifstream`, sprawdzasz otwarcie przez `fail()`, tworzysz plik danych w projekcie i sprawdzasz pole **Working directory** (lekcja 12.1).

## Sytuacja

W szkolnej pracowni biologicznej ktoś codziennie zapisuje w pliku `watering.txt` stan roślin: nazwę rośliny, a w następnej linii `watered`, jeśli roślina jest podlana, albo `dry`, jeśli ziemia jest sucha. Plik jest pisany ręcznie, więc zdarzają się w nim pomyłki: przypadkowa pusta linia, literówka w statusie, brak ostatniej linii.

Program ma odczytać **cały** plik i wypisać raport. Jeśli plik zawiera błąd, nie wypisuje raportu, tylko wskazuje numer linii do poprawienia, taki sam jak numer linii w edytorze.

Po tej lekcji będziesz:

- odróżniać koniec pliku od pustej linii;
- czytać plik tak, żeby dane kończył wyłącznie koniec pliku;
- numerować fizyczne linie pliku podczas odczytu jednym licznikiem, zwiększanym po każdym udanym `std::getline`;
- zgłaszać pustą linię, nieprawidłowy status i niekompletny rekord z numerem linii, bez częściowego raportu;
- poprawnie odczytywać ostatnią linię bez znaku końca linii.

## 1. Punkt wyjścia: dane, które znikają

W lekcji 12.2, punkt 6, program z przesyłkami dostał taki plik `shipments.txt`:

```text
North Hub
4

South Depot
7
```

i wypisał:

```text
Shipments: 1
North Hub: 4
Total boxes: 4
```

Nie było żadnego komunikatu, a `South Depot` nie trafił do raportu. Odpowiedz na kartce, zanim przeczytasz dalej:

1. Czy plik się skończył, kiedy program przestał czytać?
2. Czy wszystkie dane zostały odczytane?
3. Dlaczego program nie zgłosił błędu?
4. Skąd program miałby wiedzieć, że pusta linia oznacza koniec danych, a nie pomyłkę w pliku?
5. Co powinien zrobić program, jeśli ma przetworzyć cały plik?

## 2. Pusta linia to nie koniec pliku

Odpowiedzi:

1. Nie. Za pustą linią są jeszcze dwie linie, `South Depot` i `7`. Program przestał czytać, zanim plik się skończył.
2. Nie. Ostatnia przesyłka została w pliku nieodczytana.
3. Bo tak mówił kontrakt lekcji 12.2: pusta linia w miejscu nazwy kończy dane. Odczyt pustej linii się udał, ale nazwa była pusta, więc warunek pętli `!input.fail() && !destination.empty()` zakończył pętlę. Dla programu to było zwykłe zakończenie danych.
4. Nie miałby skąd. Sama pusta linia nie mówi, czy ktoś chciał zakończyć listę, czy przypadkiem zostawił odstęp. W lekcji 12.2 rozstrzygał to kontrakt, przejęty z wpisywania z klawiatury, gdzie pustą linię wpisuje się świadomie.
5. Czytać aż do końca pliku, a pustą linię uznać za błąd danych i powiedzieć, w którym miejscu jest.

Program z lekcji 12.2 nie był błędny: dla danych zgodnych ze swoim kontraktem działał poprawnie. **W tej lekcji zmieniamy kontrakt: listę rekordów kończy wyłącznie koniec pliku, a pusta linia jest błędem danych.**

**Koniec pliku a pusta linia.** W tabeli `\n` oznacza znak końca linii, ten sam, który program wypisuje przez `"\n"`.

| Zawartość pliku | Fizyczne linie | Kolejne wywołania `std::getline` |
|---|---|---|
| nic (pusty plik) | 0 | od razu nieudany odczyt |
| `\n` | 1, pusta | pusty tekst, potem nieudany odczyt |
| `Basil` | 1 | `Basil`, potem nieudany odczyt |
| `Basil\n` | 1 | `Basil`, potem nieudany odczyt |
| `Basil\nwatered\n` | 2 | `Basil`, `watered`, potem nieudany odczyt |
| `Basil\nwatered\n\n` | 3, trzecia pusta | `Basil`, `watered`, pusty tekst, potem nieudany odczyt |

- **Znak końca linii kończy linię, a nie zaczyna nowej.** `Basil\n` ma jedną linię, tak samo jak `Basil`. Dopiero drugi znak końca linii zaraz po pierwszym tworzy nową, pustą linię.
- **Pusta linia to udany odczyt:** `fail()` daje `false`, a tekst jest pusty (lekcja 7.4). **Koniec pliku to nieudany odczyt:** `std::getline` nie znajduje już żadnej linii, a `fail()` daje `true`.
- **Ostatnia linia bez znaku końca linii też jest udanym odczytem.** W pliku `Basil\nwatered` drugie wywołanie dostarcza `watered` i dochodzi do końca pliku: `eof()` daje już `true`, ale `fail()` daje `false`. Dopiero trzecie wywołanie się nie udaje. Dlatego program nie pyta przed odczytem, czy plik się skończył. Najpierw próbuje odczytać linię, a potem sprawdza `fail()`.
- **Nieudany odczyt traktujemy jako koniec pliku.** Tak jest w zwykłym pliku tekstowym, który udało się otworzyć. Rzadkie awarie, na przykład błąd dysku, też dają nieudany odczyt, ale ich rozpoznawanie jest poza tą lekcją.

**Dlaczego bez liczb?** `>>` przed liczbą pomija białe znaki, także znaki końca linii (lekcja 2.6). Gdyby między nazwą a liczbą stała pusta linia, `>>` przeskoczyłby ją bez śladu: program nie zauważyłby pustej linii i źle policzyłby numery kolejnych linii. Żeby zobaczyć każdą linię, trzeba ją odczytać w całości przez `std::getline`. Linię z liczbą trzeba by potem zamienić na liczbę, a tego jeszcze nie umiemy. Dlatego w tej lekcji oba pola rekordu są tekstem, a program nie jest poprawioną wersją programu z przesyłkami. Zmieniamy format danych, żeby ulepszyć sposób czytania pliku i sprawdzania jego budowy.

## 3. Nowy kontrakt danych

> **Kontrakt pliku `watering.txt`.**
>
> - Każdy rekord zajmuje dokładnie dwie fizyczne linie: nazwę rośliny i jej status.
> - Nazwa nie jest pusta, może zawierać spacje i może się powtarzać. Program zachowuje ją dokładnie, ze wszystkimi znakami.
> - Status to dokładnie `watered` albo `dry`. Wielkość liter ma znaczenie, a dodatkowe spacje nie są dozwolone, więc `Watered`, `DRY` i `dry ` są nieprawidłowe.
> - **Dane kończy wyłącznie koniec pliku** w miejscu, w którym zaczynałby się kolejny rekord.
> - Każda pusta linia jest błędem: w miejscu nazwy, w miejscu statusu i na końcu pliku.
> - Ostatnia linia może nie mieć znaku końca linii.
> - Liczba rekordów nie jest ograniczona. W przykładach jest ich od 0 do 5.
>
> Pusta linia to linia bez żadnego znaku. Linia z samymi spacjami nie jest pusta (lekcja 7.4): jako nazwa jest przyjmowana, a jako status jest nieprawidłowa.

| Sytuacja | Standardowe wyjście |
|---|---|
| pliku nie udało się otworzyć | `Cannot open watering.txt` |
| pusta linia w miejscu nazwy albo statusu | `Empty line N`, gdzie N to numer pustej linii |
| status niepusty, ale inny niż `watered` i `dry` | `Invalid line N`, gdzie N to numer linii statusu |
| plik kończy się zaraz po nazwie, bez linii statusu | `Incomplete record on line N`, gdzie N to numer linii tej nazwy |
| cały plik jest poprawny | `Plants: N`, każda roślina w kolejności z pliku, na przykład `Basil: watered`, i `Watered total: T` |

- **N to zawsze numer fizycznej linii pliku**, liczony od 1, jak w edytorze. `T` to liczba roślin ze statusem `watered`.
- Program zgłasza pierwszy błąd i kończy pracę kodem 0, **bez częściowego raportu**. Raport wypisuje dopiero po odczytaniu całego pliku. Nie sortuje roślin i nie usuwa powtórzeń.
- **Niekompletny rekord wskazuje ostatnią istniejącą linię.** Linii statusu w pliku nie ma, więc program nie może podać jej numeru. Podaje numer linii nazwy, od której rekord się zaczął: to po niej trzeba dopisać status.
- **Pusta linia statusu to nie niekompletny rekord.** W pliku `Basil\n\n` druga linia istnieje, tylko jest pusta: `Empty line 2`. W pliku `Basil\n` drugiej linii nie ma: `Incomplete record on line 1`.
- **Sprawdzenia wynikają z kontraktu.** Program sprawdza dokładnie to, co kontrakt nazywa błędem, i nic więcej: nie obcina spacji z nazw i nie poprawia wielkości liter. Inny kontrakt wymagałby innych sprawdzeń.

## 4. Jeden `std::getline`, jedna fizyczna linia

**Reguła numerowania:** licznik linii zaczyna od 0 i rośnie o 1 **dokładnie po każdym udanym `std::getline`**. Nieudany odczyt nie dostarcza żadnej linii, więc licznika nie zmienia. Sam koniec pliku też nie jest linią. Po udanym odczycie licznik jest więc numerem właśnie odczytanej linii, a komunikat może go podać bez żadnych obliczeń.

Przebieg dla pliku, w którym drugi rekord ma nieprawidłowy status:

```text
Basil
watered
Mint
soaked
```

| Wywołanie `std::getline` | Odczytany tekst | `fail()` | Licznik po wywołaniu | Sprawdzenie |
|---|---|---|---|---|
| 1 (nazwa) | `Basil` | `false` | 1 | nazwa niepusta |
| 2 (status) | `watered` | `false` | 2 | status dozwolony, rekord przyjęty |
| 3 (nazwa) | `Mint` | `false` | 3 | nazwa niepusta |
| 4 (status) | `soaked` | `false` | 4 | status niedozwolony: `Invalid line 4` |

**Numer rekordu to nie numer linii.** Błąd jest w drugim rekordzie, ale w czwartej linii. `Invalid line 2` wskazywałoby linię `watered`, która jest poprawna. Komunikat o „rekordzie 2” kazałby szukać, którą z dwóch linii poprawić, a ktoś, kto poprawia plik w edytorze, widzi numery linii, nie rekordów. Dlatego program ma osobny licznik linii, a liczbę rekordów zna z rozmiaru wektora.

Przebieg dla pliku `Basil\n`, w którym brakuje statusu:

| Wywołanie `std::getline` | Odczytany tekst | `fail()` | Licznik po wywołaniu | Sprawdzenie |
|---|---|---|---|---|
| 1 (nazwa) | `Basil` | `false` | 1 | nazwa niepusta |
| 2 (status) | nic | `true` | 1 | brak statusu: `Incomplete record on line 1` |

Gdyby licznik rósł także po nieudanym odczycie, program wypisałby `Incomplete record on line 2`, czyli numer linii, której w pliku nie ma.

## 5. Program demonstracyjny

W `cpp-workspace` utwórz katalog `lesson_12_3` i skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program`. Otwórz katalog w CLionie (**File | Open**, potem **Trust Project** i profil **Debug**). Obok `main.cpp` utwórz plik `watering.txt`, tak jak `steps.txt` w lekcji 12.1, punkt 3, i sprawdź pole **Working directory**, jak w punkcie 4 tamtej lekcji. Zastąp zawartość `main.cpp` programem:

<!-- example: watering -->
```cpp
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

struct Plant {
    std::string name;
    std::string status;
};

bool read_plants(std::istream& input, std::vector<Plant>& plants, std::string& error, int& error_line) {
    int line_number{0};
    std::string name{};
    std::getline(input, name);

    while (!input.fail()) {
        ++line_number;

        if (name.empty()) {
            error = "empty";
            error_line = line_number;
            return false;
        }

        std::string status{};
        std::getline(input, status);

        if (input.fail()) {
            error = "incomplete";
            error_line = line_number;
            return false;
        }

        ++line_number;

        if (status.empty()) {
            error = "empty";
            error_line = line_number;
            return false;
        }

        if (status != "watered" && status != "dry") {
            error = "invalid";
            error_line = line_number;
            return false;
        }

        plants.push_back(Plant{name, status});
        std::getline(input, name);
    }

    return true;
}

int main() {
    std::ifstream input{"watering.txt"};

    if (input.fail()) {
        std::cout << "Cannot open watering.txt\n";
        return 0;
    }

    std::vector<Plant> plants{};
    std::string error{};
    int error_line{0};
    const bool complete{read_plants(input, plants, error, error_line)};

    if (!complete) {
        if (error == "empty") {
            std::cout << "Empty line " << error_line << "\n";
        } else if (error == "invalid") {
            std::cout << "Invalid line " << error_line << "\n";
        } else {
            std::cout << "Incomplete record on line " << error_line << "\n";
        }

        return 0;
    }

    int watered_total{0};
    std::cout << "Plants: " << plants.size() << "\n";

    for (const Plant& plant : plants) {
        std::cout << plant.name << ": " << plant.status << "\n";

        if (plant.status == "watered") {
            ++watered_total;
        }
    }

    std::cout << "Watered total: " << watered_total << "\n";
}
```

- **`read_plants` odczytuje cały plik.** Dostaje strumień przez `std::istream&`, jak funkcja z lekcji 12.2, wektor do wypełnienia i dwie zmienne na opis błędu. Zwraca `true`, gdy cały plik jest poprawny, a `false` przy pierwszym błędzie. Niczego nie wypisuje i nie zna nazwy pliku.
- **`std::string& error` i `int& error_line`** działają jak parametr `Product&` w lekcji 9.1, tylko dla tekstu i liczby: funkcja zapisuje w nich rodzaj błędu i numer linii, a `main` po powrocie odczytuje je ze swoich zmiennych. Wektor też dostaje przez referencję bez `const` (lekcja 9.3) i dopisuje do niego rekordy przez `push_back`.
- **Nazwa jest odczytywana przed pętlą i na końcu jej treści**, jak w lekcji 10.4. Pętla wykonuje się tylko po udanym odczycie nazwy, więc jej pierwsza instrukcja, `++line_number;`, liczy linię tej nazwy.
- **Warunek pętli to samo `!input.fail()`.** W lekcji 12.2 stał tam jeszcze warunek niepustej nazwy, więc pusta linia kończyła pętlę. Tutaj pętlę kończy tylko nieudany odczyt nazwy, czyli koniec pliku. Pustą nazwę sprawdza pierwszy `if` w pętli i zgłasza błąd.
- **Status:** nieudany odczyt statusu oznacza, że plik skończył się w środku rekordu. Licznik nie urósł, więc wskazuje linię nazwy. Po udanym odczycie licznik rośnie i wskazuje linię statusu. Najpierw jest sprawdzenie pustej linii, potem dozwolonego słowa, więc pusta linia nigdy nie daje `Invalid line`.
- **Rodzaj błędu to tekst: `"empty"`, `"invalid"` albo `"incomplete"`.** Funkcja tylko opisuje błąd, a pełny komunikat wybiera `main`, jak po odmowie w lekcji 12.2.
- **Bez częściowego raportu.** Przy błędzie w wektorze mogą już być wcześniejsze rośliny, ale `main` po `false` wypisuje tylko komunikat i kończy pracę. Raport powstaje dopiero po `true`. Liczba roślin to `plants.size()`, a `watered_total` rośnie dla każdego statusu `watered`.

Wpisz do `watering.txt` dane A:

<!-- run: watering -->

<!-- datafile: watering watering.txt -->
```text
Basil
watered
Mint
dry
Fern
watered
```

Zbuduj i uruchom program. To pierwsze obowiązkowe uruchomienie.

<!-- output: watering -->
```text
Plants: 3
Basil: watered
Mint: dry
Fern: watered
Watered total: 2
```

## 6. Przypadki brzegowe

Każdy przypadek to inna zawartość `watering.txt` albo brak pliku. Programu nie zmieniasz i nie budujesz od nowa.

**D: pusta linia w środku.** To plik z punktu 1, tylko w nowym formacie:

<!-- run: watering -->

<!-- datafile: watering watering.txt -->
```text
Basil
watered

Mint
dry
```

**Przewidź** wynik, a potem uruchom program. To drugie obowiązkowe uruchomienie.

<details>
<summary>Standardowe wyjście dla D</summary>

<!-- output: watering -->
```text
Empty line 3
```

Trzecie `std::getline` odczytuje pustą linię. Odczyt się udał, licznik ma wartość 3, a nazwa jest pusta, więc funkcja zgłasza błąd. Program nie wypisuje raportu z jedną rośliną: rekord `Mint` nie znika po cichu.

</details>

**G: niekompletny rekord.** Plik kończy się zaraz po pierwszej nazwie:

<!-- run: watering -->

<!-- datafile: watering watering.txt -->
```text
Basil
```

**Przewidź** wynik, a potem uruchom program. To trzecie obowiązkowe uruchomienie.

<details>
<summary>Standardowe wyjście dla G</summary>

<!-- output: watering -->
```text
Incomplete record on line 1
```

To drugi przebieg z punktu 4: odczyt statusu się nie udaje, a licznik zostaje na 1.

</details>

Pozostałe przypadki przewidź na kartce, zanim otworzysz zwinięty blok. Ich uruchamianie jest nieobowiązkowe.

**B: pusty plik.** `watering.txt` istnieje, ale nie ma w nim ani jednego znaku.

<!-- run: watering -->

<!-- datafile: watering watering.txt -->
```text
```

<details>
<summary>Standardowe wyjście dla B</summary>

<!-- output: watering -->
```text
Plants: 0
Watered total: 0
```

Pierwszy odczyt nazwy się nie udaje. To koniec pliku tam, gdzie zaczynałby się rekord, więc poprawny koniec listy, w której nie ma roślin. Pusty plik nie zawiera żadnej linii, więc nie zawiera też pustej linii.

</details>

**C: brak pliku.** W katalogu roboczym nie ma `watering.txt`.

<!-- run: watering -->

<details>
<summary>Standardowe wyjście dla C</summary>

<!-- output: watering -->
```text
Cannot open watering.txt
```

Program nie wypisuje `Plants: 0`, bo nie wie, co jest w pliku, którego nie otworzył.

</details>

**E: pusta linia statusu.** Po `Basil` są dwa znaki końca linii, czyli `Basil\n\n`.

<!-- run: watering -->

<!-- datafile: watering watering.txt -->
```text
Basil

```

<details>
<summary>Standardowe wyjście dla E</summary>

<!-- output: watering -->
```text
Empty line 2
```

Druga linia istnieje, tylko jest pusta. To nie jest niekompletny rekord, jak w G.

</details>

**F: nieprawidłowy status.**

<!-- run: watering -->

<!-- datafile: watering watering.txt -->
```text
Basil
soaked
```

<details>
<summary>Standardowe wyjście dla F</summary>

<!-- output: watering -->
```text
Invalid line 2
```

</details>

**H: ostatni status bez znaku końca linii.** Plik to dokładnie `Basil\nwatered`.

<!-- run: watering -->

<!-- datafile: watering watering.txt noeol -->
```text
Basil
watered
```

<details>
<summary>Standardowe wyjście dla H</summary>

<!-- output: watering -->
```text
Plants: 1
Basil: watered
Watered total: 1
```

`std::getline` dostarcza `watered` i dochodzi do końca pliku, ale `fail()` daje `false`, więc rekord jest kompletny. Następny odczyt nazwy się nie udaje: to poprawny koniec danych. Ten sam plik ze znakiem końca linii po `watered` daje dokładnie ten sam raport (przypadek K niżej). Plik bez znaku końca linii powstaje łatwo, gdy po ostatnim słowie nie naciśniesz **Enter**. Takiego pliku nie musisz przygotowywać.

</details>

**I: pusta linia na końcu.** Plik to `Basil\nwatered\n\n`.

<!-- run: watering -->

<!-- datafile: watering watering.txt -->
```text
Basil
watered

```

<details>
<summary>Standardowe wyjście dla I</summary>

<!-- output: watering -->
```text
Empty line 3
```

Pierwszy znak końca linii po `watered` kończy linię 2. Drugi tworzy linię 3, pustą. W lekcji 12.2 pusta linia na końcu kończyła dane (tamten przypadek C). Tutaj jest błędem, bo zmienił się kontrakt.

</details>

**J: nieprawidłowy status drugiego rekordu.** To plik z przebiegu w punkcie 4.

<!-- run: watering -->

<!-- datafile: watering watering.txt -->
```text
Basil
watered
Mint
soaked
```

<details>
<summary>Standardowe wyjście dla J</summary>

<!-- output: watering -->
```text
Invalid line 4
```

Pierwszy rekord był poprawny, ale nie trafia do raportu: przy błędzie raportu nie ma wcale.

</details>

Gdzie może się skończyć plik i co wtedy wypisuje program:

| Gdzie kończy się plik | Przypadek | Wynik |
|---|---|---|
| przed pierwszą nazwą: pusty plik | B | raport bez roślin |
| zaraz po nazwie, bez linii statusu | G | `Incomplete record on line 1` |
| zaraz po statusie, bez znaku końca linii | H | raport |
| po znaku końca linii za statusem | K | raport |
| po pustej linii za statusem | I | `Empty line 3` |

<details>
<summary>Pozostałe przypadki kontrolne: otwórz po przewidywaniach</summary>

Wszystkie te przypadki są sprawdzane automatycznie. Wyniki wynikają z kontraktu z punktu 3.

**K: dane H ze znakiem końca linii po `watered`.**

<!-- run: watering -->

<!-- datafile: watering watering.txt -->
```text
Basil
watered
```

<!-- output: watering -->
```text
Plants: 1
Basil: watered
Watered total: 1
```

**L: jedna pusta linia.** Plik zawiera tylko jeden znak końca linii.

<!-- run: watering -->

<!-- datafile: watering watering.txt -->
```text

```

<!-- output: watering -->
```text
Empty line 1
```

**M: sama nazwa, bez znaku końca linii.** Plik to dokładnie `Basil`.

<!-- run: watering -->

<!-- datafile: watering watering.txt noeol -->
```text
Basil
```

<!-- output: watering -->
```text
Incomplete record on line 1
```

**N: nieprawidłowy status bez znaku końca linii.**

<!-- run: watering -->

<!-- datafile: watering watering.txt noeol -->
```text
Basil
soaked
```

<!-- output: watering -->
```text
Invalid line 2
```

**O: spacja po statusie.** W drugiej linii jest `watered` i jedna spacja.

<!-- run: watering -->

<!-- datafile: watering watering.txt -->
```text
Basil
watered 
```

<!-- output: watering -->
```text
Invalid line 2
```

**P: ta sama nazwa dwa razy.** Każde wystąpienie to osobny rekord.

<!-- run: watering -->

<!-- datafile: watering watering.txt -->
```text
Basil
watered
Basil
dry
```

<!-- output: watering -->
```text
Plants: 2
Basil: watered
Basil: dry
Watered total: 1
```

**Q: pięć rekordów,** w tym nazwa ze spacją.

<!-- run: watering -->

<!-- datafile: watering watering.txt -->
```text
Basil
watered
Mint
dry
Fern
watered
Peace Lily
watered
Aloe
dry
```

<!-- output: watering -->
```text
Plants: 5
Basil: watered
Mint: dry
Fern: watered
Peace Lily: watered
Aloe: dry
Watered total: 3
```

**R: błąd po trzech poprawnych rekordach.** Status `Dry` jest pisany wielką literą.

<!-- run: watering -->

<!-- datafile: watering watering.txt -->
```text
Basil
watered
Mint
dry
Fern
watered
Rose
Dry
```

<!-- output: watering -->
```text
Invalid line 8
```

</details>

## 7. Diagnostyka: stara reguła na nowych danych

**Sytuacja.** Ktoś przeniósł do dziennika podlewania regułę zakończenia z lekcji 12.2: pusta linia w miejscu nazwy kończy dane. W programie z punktu 5 zmienił tylko dwa miejsca funkcji `read_plants`:

| Program z punktu 5 | Program ze starą regułą |
|---|---|
| `while (!input.fail()) {` | `while (!input.fail() && !name.empty()) {` |
| na początku pętli `if (name.empty())` z błędem `"empty"` | brak tego sprawdzenia |

<details>
<summary>Cały program ze starą regułą</summary>

<!-- example: watering_old_rule -->
```cpp
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

struct Plant {
    std::string name;
    std::string status;
};

bool read_plants(std::istream& input, std::vector<Plant>& plants, std::string& error, int& error_line) {
    int line_number{0};
    std::string name{};
    std::getline(input, name);

    while (!input.fail() && !name.empty()) {
        ++line_number;

        std::string status{};
        std::getline(input, status);

        if (input.fail()) {
            error = "incomplete";
            error_line = line_number;
            return false;
        }

        ++line_number;

        if (status.empty()) {
            error = "empty";
            error_line = line_number;
            return false;
        }

        if (status != "watered" && status != "dry") {
            error = "invalid";
            error_line = line_number;
            return false;
        }

        plants.push_back(Plant{name, status});
        std::getline(input, name);
    }

    return true;
}

int main() {
    std::ifstream input{"watering.txt"};

    if (input.fail()) {
        std::cout << "Cannot open watering.txt\n";
        return 0;
    }

    std::vector<Plant> plants{};
    std::string error{};
    int error_line{0};
    const bool complete{read_plants(input, plants, error, error_line)};

    if (!complete) {
        if (error == "empty") {
            std::cout << "Empty line " << error_line << "\n";
        } else if (error == "invalid") {
            std::cout << "Invalid line " << error_line << "\n";
        } else {
            std::cout << "Incomplete record on line " << error_line << "\n";
        }

        return 0;
    }

    int watered_total{0};
    std::cout << "Plants: " << plants.size() << "\n";

    for (const Plant& plant : plants) {
        std::cout << plant.name << ": " << plant.status << "\n";

        if (plant.status == "watered") {
            ++watered_total;
        }
    }

    std::cout << "Watered total: " << watered_total << "\n";
}
```

</details>

Programu ze starą regułą nie musisz przepisywać ani uruchamiać: jego wyniki są sprawdzane automatycznie. Odpowiedz na kartce:

1. **Przewidź**, co wypisze program ze starą regułą dla danych D z punktu 6.
2. Wskaż warunek, który kończy odczyt. Dlaczego rekord `Mint` nie zostaje odczytany?
3. Dlaczego to nie jest koniec pliku? Co daje `fail()` po odczycie pustej linii?
4. Porównaj swoją odpowiedź z wynikiem drugiego obowiązkowego uruchomienia, czyli programu z punktu 5 dla tych samych danych.
5. Skąd w `Empty line 3` bierze się liczba 3?
6. Jeśli plik miał zawierać dwie rośliny, który wynik jest bezpieczniejszy i dlaczego?
7. Odpowiedz na pytania 1 i 6 także dla danych I z punktu 6.

<details>
<summary>Co się dzieje: otwórz po odpowiedziach</summary>

Wyniki programu ze starą regułą, sprawdzane automatycznie. Dane D:

<!-- run: watering_old_rule -->

<!-- datafile: watering_old_rule watering.txt -->
```text
Basil
watered

Mint
dry
```

<!-- output: watering_old_rule -->
```text
Plants: 1
Basil: watered
Watered total: 1
```

Dane I:

<!-- run: watering_old_rule -->

<!-- datafile: watering_old_rule watering.txt -->
```text
Basil
watered

```

<!-- output: watering_old_rule -->
```text
Plants: 1
Basil: watered
Watered total: 1
```

1. Dla D program ze starą regułą wypisuje raport z jedną rośliną, bez żadnego komunikatu.
2. Trzecie `std::getline` odczytuje pustą linię. Odczyt się udał, więc `!input.fail()` daje `true`, ale `!name.empty()` daje `false` i pętla się kończy. Funkcja zwraca `true`, jakby cały plik był poprawny, a linie 4 i 5 zostają nieodczytane.
3. Bo linia 3 istnieje: `fail()` daje `false`. Koniec pliku to nieudany odczyt, a tu odczyt się udał, tylko tekst jest pusty.
4. Program z punktu 5 dla tych samych bajtów wypisuje `Empty line 3`. Jego pętlę kończy tylko nieudany odczyt, a pusta nazwa jest błędem.
5. Z licznika: `Basil` to linia 1, `watered` linia 2, a pusta linia to trzecie udane `std::getline`, więc licznik ma wartość 3.
6. Bezpieczniejszy jest `Empty line 3`. Raport z jedną rośliną wygląda na kompletny i nic nie ostrzega, że `Mint` zniknęła. Komunikat nie daje wyniku, który ktoś mógłby uznać za pełny, i mówi, którą linię poprawić. Gdy plik trzeba przetworzyć w całości, cichy brak danych jest groźniejszy niż jawny błąd.
7. Dla I stara reguła też wypisuje raport z jedną rośliną, a nowy program `Empty line 3`. Według kontraktu lekcji 12.2 raport był poprawny, bo pusta linia na końcu kończyła dane. Nowy kontrakt jest surowszy: pustej linii nie wolno zostawić nawet na końcu pliku.

Program z lekcji 12.2 nie miał błędu: działał zgodnie ze swoim kontraktem. Zmienił się kontrakt, więc musiała się zmienić reguła zakończenia, a z nią warunek pętli.

</details>

## 8. Misja: dziennik zadań

Klub szkolny zapisuje w pliku zadania do wykonania i ich stan. Program odczytuje plik `chores.txt` i wypisuje wszystkie zadania oraz liczbę wykonanych.

**Kontrakt pliku `chores.txt`:**

- każdy rekord zajmuje dokładnie dwie fizyczne linie: nazwę zadania i jego status;
- nazwa nie jest pusta, może zawierać spacje i może się powtarzać, a program zachowuje ją dokładnie;
- status to dokładnie `done` albo `pending`, z rozróżnieniem wielkości liter i bez dodatkowych spacji;
- dane kończy wyłącznie koniec pliku w miejscu, w którym zaczynałby się kolejny rekord;
- każda pusta linia jest błędem, a po nazwie musi istnieć linia ze statusem;
- ostatnia linia może nie mieć znaku końca linii.

**Komunikaty:**

| Sytuacja | Standardowe wyjście |
|---|---|
| pliku nie udało się otworzyć | `Cannot open chores.txt` |
| pusta linia | `Empty line N` |
| status niepusty, ale inny niż `done` i `pending` | `Invalid line N` |
| plik kończy się zaraz po nazwie | `Incomplete record on line N`, gdzie N to numer linii tej nazwy |
| cały plik jest poprawny | `Tasks: N`, każde zadanie w kolejności z pliku, na przykład `Clean tables: done`, i `Done total: T` |

N to numer fizycznej linii pliku, a `T` to liczba zadań ze statusem `done`. Program nie sortuje zadań i nie usuwa powtórzeń. Po błędzie wypisuje tylko jeden komunikat, bez częściowego raportu, i kończy się kodem 0.

**Wymagania:**

- Program definiuje własny typ rekordu z dwoma polami tekstowymi i zbiera rekordy w wektorze.
- Cały plik odczytuje jedna funkcja, która dostaje strumień przez `std::istream&`. Każdą linię odczytuje przez `std::getline`, bez `>>`, liczy fizyczne linie i przy pierwszym błędzie przekazuje do `main` jego rodzaj i numer linii. O tym, czy linia jest odczytana, decyduje `fail()` po odczycie. Funkcja niczego nie wypisuje, nie otwiera pliku i nie używa `std::cin`.
- `main` otwiera `chores.txt`, sprawdza otwarcie, wywołuje funkcję i wypisuje albo jeden komunikat, albo pełny raport.

W `cpp-workspace` utwórz katalog `chore_log`, skopiuj do niego `CMakeLists.txt` z oryginalnego `lesson_05_first_program`, utwórz pusty `main.cpp` i plik `chores.txt`. `CMakeLists.txt` zostaw bez zmian, a `chores.txt` nie dopisuj do `add_executable`. Otwórz katalog w CLionie i sprawdź **Working directory**, jak w lekcji 12.1, punkt 4. Jeden plik `main.cpp` wystarczy. Napisz program samodzielnie. Możesz zaglądać do programu z punktu 5.

```text
chore_log/
├── CMakeLists.txt
├── chores.txt
└── main.cpp
```

Musisz samodzielnie zdecydować:

1. jak nazwać typ rekordu, jego pola, wektor, funkcję i jej parametry;
2. jak funkcja przekaże do `main` rodzaj błędu i numer linii;
3. gdzie licznik linii zaczyna i w których miejscach rośnie;
4. po czym funkcja pozna poprawny koniec danych;
5. po czym pozna niekompletny rekord i jaki numer wtedy poda;
6. jak odróżni pustą linię od braku linii;
7. w jakiej kolejności sprawdzi pustą linię i dozwolony status;
8. jak nie dopuścić do częściowego raportu;
9. czy ostatni rekord bez znaku końca linii wymaga osobnego kodu;
10. jakimi plikami sprawdzi pusty plik, brak pliku i błąd w późniejszym rekordzie.

**Przypadki A–J.** Każdy przypadek to inna zawartość `chores.txt` albo brak pliku.

**A: trzy zadania.**

<!-- run: chores -->

<!-- datafile: chores chores.txt -->
```text
Clean tables
done
Sort books
pending
Water plants
done
```

<!-- output: chores -->
```text
Tasks: 3
Clean tables: done
Sort books: pending
Water plants: done
Done total: 2
```

**B: pusty plik.**

<!-- run: chores -->

<!-- datafile: chores chores.txt -->
```text
```

<!-- output: chores -->
```text
Tasks: 0
Done total: 0
```

**C: brak pliku.** W katalogu roboczym nie ma `chores.txt`.

<!-- run: chores -->

<!-- output: chores -->
```text
Cannot open chores.txt
```

**D: pusta pierwsza linia.** Plik zawiera tylko jeden znak końca linii.

<!-- run: chores -->

<!-- datafile: chores chores.txt -->
```text

```

<!-- output: chores -->
```text
Empty line 1
```

**E: pusty status.** Plik to `Clean tables\n\n`.

<!-- run: chores -->

<!-- datafile: chores chores.txt -->
```text
Clean tables

```

<!-- output: chores -->
```text
Empty line 2
```

**F: nieprawidłowy status drugiego zadania.**

<!-- run: chores -->

<!-- datafile: chores chores.txt -->
```text
Clean tables
done
Sort books
later
```

<!-- output: chores -->
```text
Invalid line 4
```

**G: brak statusu drugiego zadania.**

<!-- run: chores -->

<!-- datafile: chores chores.txt -->
```text
Clean tables
done
Sort books
```

<!-- output: chores -->
```text
Incomplete record on line 3
```

**H: pusta linia po poprawnym zadaniu.** Plik to `Clean tables\ndone\n\n`.

<!-- run: chores -->

<!-- datafile: chores chores.txt -->
```text
Clean tables
done

```

<!-- output: chores -->
```text
Empty line 3
```

**I: ostatni status bez znaku końca linii.** Plik to dokładnie `Clean tables\ndone`.

<!-- run: chores -->

<!-- datafile: chores chores.txt noeol -->
```text
Clean tables
done
```

<!-- output: chores -->
```text
Tasks: 1
Clean tables: done
Done total: 1
```

**J: ta sama nazwa dwa razy.**

<!-- run: chores -->

<!-- datafile: chores chores.txt -->
```text
Clean tables
done
Clean tables
pending
```

<!-- output: chores -->
```text
Tasks: 2
Clean tables: done
Clean tables: pending
Done total: 1
```

**Zanim napiszesz program**, prześledź na kartce przypadki A, D, G i H, tak jak w tabelach z punktu 4: wywołanie `std::getline`, odczytany tekst, `fail()`, licznik i sprawdzenie.

**Potem uruchom program dla A.** To czwarte obowiązkowe uruchomienie. **Następnie dla F**, zmieniając tylko zawartość `chores.txt`. To piąte obowiązkowe uruchomienie: błąd jest w późniejszej linii, więc sprawdza numerowanie. Pozostałe przypadki prześledź na kartce, linijka po linijce swojego programu. Wszystkie są sprawdzane automatycznie w rozwiązaniu referencyjnym.

### Kryterium sukcesu

- Program buduje się jako C++20 i dla A oraz F wypisuje dokładnie pokazane wyniki.
- Twoje przewidywania dla B–E i G–J zgadzają się z wynikami podanymi wyżej.
- Funkcja dostaje strumień przez `std::istream&`, czyta każdą linię przez `std::getline` i zwiększa licznik tylko po udanym odczycie.
- W funkcji nie ma `std::cin`, `std::cout`, `>>` ani otwierania pliku, a pętli nie steruje `eof()`.
- Po błędzie program nie wypisuje żadnej części raportu.
- `chores.txt` nie jest w `add_executable`, `CMakeLists.txt` jest taki jak w lekcji 0.5, a **Working directory** wskazuje katalog z `chores.txt`.
- Umiesz wyjaśnić, dlaczego G daje numer 3, a nie 4, i dlaczego H daje błąd, a I raport.

Gdy wynik się zgadza, możesz zapisać projekt w Gicie, jak w lekcji 1.5: `main.cpp`, `CMakeLists.txt` i `chores.txt` z danymi A, bez katalogu budowania.

<details>
<summary>Podpowiedź 1: koniec pliku i pusta linia</summary>

Po każdym `std::getline` są dwa różne pytania. Czy odczyt się udał, czyli czy w pliku była jeszcze linia? To mówi `fail()`. Czy odczytana linia jest pusta? To mówi `empty()`, ale tylko po udanym odczycie. Który wynik oznacza poprawny koniec danych, a który błąd, jeśli dzieje się to w miejscu nazwy? A w miejscu statusu?

</details>

<details>
<summary>Podpowiedź 2: numerowanie</summary>

Licznik mówi, ile linii udało się już odczytać. Zwiększaj go po każdym udanym `std::getline`, także po odczycie statusu, a nie raz na rekord. Po nieudanym odczycie zostaw go bez zmian: wtedy wskazuje ostatnią linię, która istnieje.

</details>

<details>
<summary>Podpowiedź 3: raport i błędy</summary>

Nieudany odczyt statusu po niepustej nazwie to niekompletny rekord. Status sprawdź w dwóch krokach: najpierw czy linia jest pusta, potem czy to `done` albo `pending`. Rekord dodaj do wektora dopiero po obu sprawdzeniach, a raport wypisuj w `main` dopiero wtedy, gdy funkcja przeczytała cały plik bez błędu.

</details>

Przykładowe rozwiązanie jest w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 9. Gdy coś pójdzie inaczej

| Co widzisz | Co to znaczy | Co zrobić |
|---|---|---|
| `Incomplete record on line 2` zamiast `line 1` | Licznik rośnie także po nieudanym odczycie, na przykład zaraz po `std::getline`, przed sprawdzeniem `fail()`. | Zwiększaj licznik dopiero wtedy, gdy wiesz, że odczyt się udał. |
| `Invalid line 2` zamiast `Invalid line 4` | Program liczy rekordy, a nie linie, albo zwiększa licznik raz na rekord. | Zwiększaj licznik po każdym udanym `std::getline`, także po odczycie statusu. |
| Pusta linia daje raport zamiast `Empty line N` | W warunku pętli zostało `!name.empty()` z lekcji 12.2 (punkt 7). | Pętlę kończy tylko nieudany odczyt nazwy. Pustą nazwę sprawdź w treści pętli. |
| Pusty status daje `Invalid line N` zamiast `Empty line N` | Sprawdzenie dozwolonego słowa stoi przed sprawdzeniem pustej linii. | Najpierw sprawdź `empty()`, potem dozwolone słowo. |
| Ostatni rekord bez znaku końca linii znika albo daje błąd | Program sprawdza `eof()` zamiast powodzenia odczytu. Po udanym odczycie ostatniej linii `eof()` może już dawać `true` (punkt 2). | O tym, czy linia jest odczytana, decyduje `fail()` po odczycie. |
| `Invalid line N`, choć status wygląda poprawnie | W linii jest znak, którego nie widać: spacja na końcu, wielka litera albo, w pliku z Windowsa odczytywanym na Linuksie lub macOS, znak `\r` przed końcem linii. | Popraw tę linię. Plik z innego systemu utwórz od nowa w CLionie i przepisz dane. |
| Przed komunikatem błędu jest część raportu | Program wypisuje rekordy w trakcie odczytu. | Najpierw odczytaj cały plik, a raport wypisz dopiero po `true`. |
| `Cannot open chores.txt`, choć plik istnieje | Plik nie leży w katalogu roboczym albo ma inną nazwę. | Wykonaj kroki z lekcji 12.1, punkt 7: nazwa, wielkość liter, **Working directory**, położenie pliku. |

## 10. Wyjaśnij

Odpowiedz własnymi słowami, najlepiej na piśmie. Dopiero potem porównaj z przykładowymi odpowiedziami.

1. Dlaczego pusta linia nie oznacza końca pliku?
2. Kiedy `std::getline` pomyślnie odczytuje pustą linię?
3. Po czym program poznaje koniec danych przed nowym rekordem?
4. Dlaczego licznik linii nie rośnie po nieudanym `std::getline`?
5. Dlaczego numer rekordu nie wystarcza do wskazania błędu?
6. Czym różni się `Empty line 2` od `Incomplete record on line 1`? Podaj plik dla każdego z tych komunikatów.
7. Dlaczego ostatni status bez znaku końca linii może być poprawny?
8. Dlaczego `>>` utrudnia śledzenie fizycznych linii?
9. Dlaczego przy błędzie nie wolno wypisać częściowego raportu?
10. Dlaczego program z tej lekcji nadal nie jest czytnikiem dowolnego pliku tekstowego?

<details>
<summary>Przykładowe odpowiedzi</summary>

1. Bo pusta linia jest w pliku: `std::getline` ją odczytuje, `fail()` daje `false`, a za nią mogą być kolejne linie. Koniec pliku to sytuacja, w której nie ma już żadnej linii, więc odczyt się nie udaje.
2. Gdy w pliku są dwa znaki końca linii z rzędu, albo plik zaczyna się od znaku końca linii. Odczyt zabiera wtedy sam znak końca linii: `fail()` daje `false`, a tekst jest pusty.
3. Po tym, że odczyt nazwy się nie udaje: `fail()` daje `true` tam, gdzie zaczynałby się kolejny rekord. Tylko to kończy dane.
4. Bo nieudany odczyt nie dostarcza żadnej linii. Licznik ma wskazywać linie, które naprawdę są w pliku. Gdyby rósł po nieudanym odczycie, niekompletny rekord wskazywałby linię, której nie ma.
5. Bo rekord zajmuje dwie linie, a osoba, która poprawia plik, widzi w edytorze numery linii. „Rekord 2” nie mówi, czy błąd jest w nazwie, czy w statusie. Numer linii wskazuje dokładnie jedno miejsce.
6. `Empty line 2`: druga linia istnieje, ale jest pusta, na przykład `Basil\n\n`. `Incomplete record on line 1`: drugiej linii nie ma, plik kończy się po nazwie, na przykład `Basil\n` albo `Basil`.
7. Bo `std::getline` odczytuje znaki aż do końca pliku i daje `fail()` równe `false`. Ustawione `eof()` oznacza tylko, że strumień doszedł do końca pliku. Nie udaje się dopiero następny odczyt, w miejscu nazwy, a to jest poprawny koniec danych.
8. Bo `>>` przed wartością pomija białe znaki, w tym znaki końca linii. Może przeskoczyć pustą linię bez śladu, a program nie wie, ile linii minął. Dlatego każdą linię odczytujemy w całości przez `std::getline`.
9. Bo częściowy raport wyglądałby jak pełny. Ktoś mógłby go użyć, nie wiedząc, że część danych nie została sprawdzona albo odczytana. Komunikat błędu mówi jasno: plik trzeba poprawić.
10. Bo zna tylko jeden format: dwie linie na rekord i dwa stałe słowa statusu. Zatrzymuje się na pierwszym błędzie i nie czyta dalej, nie obcina spacji i nie zamienia tekstu na liczby. Działa poprawnie dla danych zgodnych ze swoim kontraktem, a plik o innej budowie wymagałby innych sprawdzeń.

</details>

## Podsumowanie

- Koniec pliku to nieudany odczyt: nie ma już żadnej linii. Pusta linia to udany odczyt z pustym tekstem. W tej lekcji dane kończy wyłącznie koniec pliku, a każda pusta linia jest błędem.
- Znak końca linii kończy linię, a nie zaczyna nowej. Dopiero drugi znak końca linii z rzędu tworzy pustą linię. Ostatnia linia bez znaku końca linii jest odczytywana normalnie.
- O odczytaniu linii decyduje `fail()` po odczycie, a nie `eof()`.
- Jeden licznik, zwiększany po każdym udanym `std::getline`, daje numer fizycznej linii. Numer rekordu to coś innego.
- `Empty line N` wskazuje pustą linię, `Invalid line N` linię z niedozwolonym statusem, a `Incomplete record on line N` linię nazwy, po której plik się skończył.
- Funkcja odczytu opisuje błąd przez referencje, a `main` wybiera komunikat. Raport powstaje dopiero po odczytaniu całego pliku bez błędu.

## Co dalej

W [lekcji 12.4: Seanse w kinie (sprawdzian Modułu 12)](lesson_04_cinema_screenings.md) samodzielnie zaprojektujesz, napiszesz i sprawdzisz program, który odczytuje i kontroluje plik z danymi.

---

## Przykładowe rozwiązania

Zajrzyj tutaj **po własnej próbie**. Twoje nazwy mogą się różnić, jeśli standardowe wyjście jest takie, jak wymagane.

<details>
<summary>Punkt 8: misja, dziennik zadań</summary>

**`main.cpp`**:

<!-- example: chores -->
```cpp
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

struct Chore {
    std::string name;
    std::string status;
};

bool read_chores(std::istream& input, std::vector<Chore>& chores, std::string& error, int& error_line) {
    int line_number{0};
    std::string name{};
    std::getline(input, name);

    while (!input.fail()) {
        ++line_number;

        if (name.empty()) {
            error = "empty";
            error_line = line_number;
            return false;
        }

        std::string status{};
        std::getline(input, status);

        if (input.fail()) {
            error = "incomplete";
            error_line = line_number;
            return false;
        }

        ++line_number;

        if (status.empty()) {
            error = "empty";
            error_line = line_number;
            return false;
        }

        if (status != "done" && status != "pending") {
            error = "invalid";
            error_line = line_number;
            return false;
        }

        chores.push_back(Chore{name, status});
        std::getline(input, name);
    }

    return true;
}

int main() {
    std::ifstream chores_file{"chores.txt"};

    if (chores_file.fail()) {
        std::cout << "Cannot open chores.txt\n";
        return 0;
    }

    std::vector<Chore> chores{};
    std::string error{};
    int error_line{0};
    const bool complete{read_chores(chores_file, chores, error, error_line)};

    if (!complete) {
        if (error == "empty") {
            std::cout << "Empty line " << error_line << "\n";
        } else if (error == "invalid") {
            std::cout << "Invalid line " << error_line << "\n";
        } else {
            std::cout << "Incomplete record on line " << error_line << "\n";
        }

        return 0;
    }

    int done_total{0};
    std::cout << "Tasks: " << chores.size() << "\n";

    for (const Chore& chore : chores) {
        std::cout << chore.name << ": " << chore.status << "\n";

        if (chore.status == "done") {
            ++done_total;
        }
    }

    std::cout << "Done total: " << done_total << "\n";
}
```

**`CMakeLists.txt`**: taki jak w oryginalnym `lesson_05_first_program`, bez zmian. `chores.txt` nie jest w `add_executable`.

**`chores.txt`** z danymi A, w katalogu `chore_log`, obok `main.cpp` i `CMakeLists.txt`:

<!-- run: chores -->

<!-- datafile: chores chores.txt -->
```text
Clean tables
done
Sort books
pending
Water plants
done
```

<!-- output: chores -->
```text
Tasks: 3
Clean tables: done
Sort books: pending
Water plants: done
Done total: 2
```

- **Uruchomienie:** pole **Working directory** konfiguracji `first_program` wskazuje katalog `chore_log`, ten z `chores.txt`. W terminalu program uruchamiasz z katalogu `chore_log`.
- **Model odczytu:** `read_chores` czyta nazwę, a w pętli, która trwa, dopóki odczyt nazwy się udaje, sprawdza pustą nazwę, czyta status, sprawdza jego odczyt, pustą linię i dozwolone słowo, dodaje rekord i czyta następną nazwę. Nieudany odczyt nazwy kończy pętlę i oznacza poprawny koniec danych.
- **Zwrot błędu:** funkcja zwraca `false` i zapisuje rodzaj błędu w `error` (`"empty"`, `"invalid"` albo `"incomplete"`), a numer linii w `error_line`. `main` zamienia rodzaj na komunikat.
- **Numerowanie:** `line_number` rośnie raz po udanym odczycie nazwy, na początku pętli, i raz po udanym odczycie statusu. Po nieudanym odczycie statusu nie rośnie, więc `Incomplete record` podaje linię nazwy.
- **Brak znaku końca linii:** nie wymaga osobnego kodu. Ostatnia linia jest udanym odczytem, a pętlę kończy dopiero następny, nieudany odczyt nazwy.
- **Bez częściowego raportu:** `main` wypisuje raport tylko po `true`. Po `false` wektor może zawierać wcześniejsze zadania, ale nic z niego nie jest wypisywane.
- **Inne poprawne rozwiązania:** pętla z flagą `bool` i odczytem nazwy na początku każdego przebiegu, jak w lekcji 7.4; osobna mała funkcja, która odczytuje jedną linię i zwiększa licznik tylko po udanym odczycie, wywoływana dla nazwy i dla statusu. Ważne, żeby licznik rósł tylko po udanym odczycie, a raport powstawał dopiero na końcu.

| Przypadek | Plik `chores.txt` | Standardowe wyjście |
|---|---|---|
| A | `Clean tables`, `done`, `Sort books`, `pending`, `Water plants`, `done` | 3 zadania, `Done total: 2` |
| B | pusty plik | `Tasks: 0`, `Done total: 0` |
| C | brak pliku | `Cannot open chores.txt` |
| D | jedna pusta linia | `Empty line 1` |
| E | `Clean tables`, pusta linia | `Empty line 2` |
| F | `Clean tables`, `done`, `Sort books`, `later` | `Invalid line 4` |
| G | `Clean tables`, `done`, `Sort books` | `Incomplete record on line 3` |
| H | `Clean tables`, `done`, pusta linia | `Empty line 3` |
| I | `Clean tables`, `done` bez znaku końca linii | 1 zadanie, `Done total: 1` |
| J | `Clean tables`, `done`, `Clean tables`, `pending` | 2 zadania, `Done total: 1` |

Pozostałe przypadki kontrolne, sprawdzane automatycznie:

**K: jedno zadanie,** ze statusem `pending`.

<!-- run: chores -->

<!-- datafile: chores chores.txt -->
```text
Water plants
pending
```

<!-- output: chores -->
```text
Tasks: 1
Water plants: pending
Done total: 0
```

**L: pięć zadań,** wszystkie wykonane.

<!-- run: chores -->

<!-- datafile: chores chores.txt -->
```text
Clean tables
done
Sort books
done
Water plants
done
Fold laundry
done
Empty bins
done
```

<!-- output: chores -->
```text
Tasks: 5
Clean tables: done
Sort books: done
Water plants: done
Fold laundry: done
Empty bins: done
Done total: 5
```

**M: `Done` wielką literą.**

<!-- run: chores -->

<!-- datafile: chores chores.txt -->
```text
Clean tables
Done
```

<!-- output: chores -->
```text
Invalid line 2
```

**N: spacja po `done`.**

<!-- run: chores -->

<!-- datafile: chores chores.txt -->
```text
Clean tables
done 
```

<!-- output: chores -->
```text
Invalid line 2
```

**O: niekompletny pierwszy rekord.**

<!-- run: chores -->

<!-- datafile: chores chores.txt -->
```text
Clean tables
```

<!-- output: chores -->
```text
Incomplete record on line 1
```

**P: brak statusu po trzech poprawnych zadaniach.**

<!-- run: chores -->

<!-- datafile: chores chores.txt -->
```text
Clean tables
done
Sort books
pending
Water plants
done
Fold laundry
```

<!-- output: chores -->
```text
Incomplete record on line 7
```

**Q: pusta linia między zadaniami.** Za nią są jeszcze dane, ale wynik jest taki sam jak w H.

<!-- run: chores -->

<!-- datafile: chores chores.txt -->
```text
Clean tables
done

Sort books
pending
```

<!-- output: chores -->
```text
Empty line 3
```

**R: nieprawidłowy status bez znaku końca linii.**

<!-- run: chores -->

<!-- datafile: chores chores.txt noeol -->
```text
Clean tables
later
```

<!-- output: chores -->
```text
Invalid line 2
```

</details>

**Poprzednia lekcja:** [Lekcja 12.2: Rekordy z pliku: ta sama funkcja odczytu](lesson_02_records_from_a_file.md) · **Następna lekcja:** [Lekcja 12.4: Seanse w kinie (sprawdzian Modułu 12)](lesson_04_cinema_screenings.md) · [Opis kursu](../../README.md)

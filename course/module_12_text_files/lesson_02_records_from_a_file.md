# Lekcja 12.2: Rekordy z pliku: ta sama funkcja odczytu

**Polski** · [English](lesson_02_records_from_a_file.en.md) · [Opis kursu](../../README.md)

> **Moduł 12, lekcja 2** · około 90–110 minut, można ją podzielić na dwa podejścia
> **Potrzebujesz:** katalogu `cpp-workspace` i oryginalnego projektu `lesson_05_first_program`, jak dotąd. Debugger nie jest w tej lekcji potrzebny.
> **Wersja pilotażowa.** Programy z tej lekcji sprawdzamy automatycznie na Windowsie, Ubuntu i macOS, z podanymi plikami danych i danymi wejściowymi. Kroki w CLionie (nowy plik, pole **Working directory**) są takie jak w lekcji 12.1: opisujemy je według dokumentacji CLion 2026.3, bez ręcznego sprawdzenia na każdym systemie.

## Zanim zaczniesz

Ta lekcja zakłada, że:

- znasz program z lekcji 10.4: funkcja `read_shipment_values` dostaje strumień przez `std::istream&`, nazwę przez `const std::string&` i rekord wynikowy przez `Shipment&`, a `main` odczytuje nazwy, rozpoznaje zakończenie danych i po odmowie odróżnia `Input error` od `Invalid shipments` przez `fail()`;
- pamiętasz, że parametr z `&` to inna nazwa obiektu przekazanego przy wywołaniu, a parametr bez `&` to jego kopia (lekcja 9.1);
- odczytujesz nazwę przez `std::getline`, liczbę przez `>>` i dokańczasz linię liczbową przez `std::getline` (lekcja 10.2);
- otwierasz plik przez `std::ifstream`, sprawdzasz otwarcie przez `fail()`, tworzysz plik danych w projekcie i sprawdzasz pole **Working directory** (lekcja 12.1).

## Sytuacja

W lekcji 10.4 program odczytywał listę przesyłek z klawiatury, więc przy każdym uruchomieniu trzeba ją było wpisywać od nowa. Teraz ta sama lista leży w pliku `shipments.txt`. Program ma ją odczytać i wypisać taki sam raport jak wtedy.

Czy potrzebna jest nowa funkcja odczytu, na przykład `read_shipment_from_file`? Nie. Funkcja `read_shipment_values` z lekcji 10.4 nigdzie nie wymienia `std::cin`: czyta z parametru `input`, czyli ze strumienia, który dostanie przy wywołaniu. **Zmienisz tylko kod wywołujący: to `main` zdecyduje, skąd pochodzą dane.** Funkcja zostanie bez zmian, co do znaku.

Po tej lekcji będziesz:

- przekazywać tej samej funkcji z parametrem `std::istream&` raz `std::cin`, a raz otwarty `std::ifstream`;
- dzielić odpowiedzialność: kod wywołujący wybiera i otwiera źródło danych, a funkcja czyta z tego strumienia, który dostanie;
- sprawdzać, że oba źródła dają ten sam wynik dla tych samych danych;
- podawać kontrakt danych programu i wskazywać jego granice, na przykład pustą linię w środku pliku;
- rozpoznawać błąd kompilacji, który pojawia się, gdy strumień jest przekazany przez wartość.

## 1. Co funkcja wie o strumieniu

Nagłówek funkcji z lekcji 10.4:

<!-- fragment -->
```cpp
bool read_shipment_values(std::istream& input, const std::string& destination, Shipment& result)
```

W treści tej funkcji nie ma `std::cin`, nazwy pliku ani `std::cout`. Funkcja wie tylko tyle:

- dostaje strumień wejścia, z którego czyta przez `>>` i którego stan sprawdza przez `fail()`;
- dostaje gotową, niepustą nazwę i rekord do wypełnienia;
- ma odczytać jedną liczbę, sprawdzić ją i przy sukcesie wypełnić rekord.

Nie wie natomiast, czy dane pochodzą z klawiatury, czy z pliku, jak ten plik się nazywa ani kto go otworzył. Nie musi tego wiedzieć: odczyt liczby wygląda tak samo w obu przypadkach.

**Przypomnienie: `std::istream&`.** `std::istream` to typ strumienia wejścia (*input stream*), a `std::cin` jest obiektem tego typu (lekcja 10.4). `&` oznacza, że parametr `input` to inna nazwa obiektu przekazanego przy wywołaniu: funkcja nie dostaje kopii, tylko pracuje na strumieniu wywołującego. `input >> boxes` zabiera znaki z tego samego strumienia, więc po powrocie z funkcji `main` czyta dalej od miejsca, w którym funkcja skończyła. `const` nie ma, bo odczyt zmienia strumień: przesuwa miejsce odczytu i może zmienić jego stan.

**Dlaczego można przekazać plik?** `std::ifstream` z lekcji 12.1 to strumień wejścia z pliku. Biblioteka standardowa określa go jako szczególny rodzaj `std::istream`, więc ma wszystko, czego funkcja potrzebuje od strumienia wejścia: `>>`, `fail()` i współpracę ze `std::getline`. Dlatego otwarty `std::ifstream` możesz przekazać wszędzie tam, gdzie funkcja oczekuje `std::istream&`. Parametr `input` staje się wtedy inną nazwą strumienia plikowego.

`std::cin` i strumień plikowy to nadal dwa różne obiekty z różnymi źródłami danych: jeden czyta z klawiatury, drugi z pliku. Wspólny jest sposób korzystania z nich, a ten wystarcza funkcji. Jak biblioteka to urządza od środka, w tym kursie nie jest potrzebne.

## 2. Punkt wyjścia: wersja z klawiaturą

W `cpp-workspace` utwórz katalog `lesson_12_2` i skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program`. Otwórz katalog w CLionie (**File | Open**, potem **Trust Project** i profil **Debug**) i zastąp zawartość `main.cpp` programem z lekcji 10.4, punkt 2. Ten sam program jest w zwiniętym bloku poniżej.

<details>
<summary>Program z lekcji 10.4: wersja z klawiaturą</summary>

<!-- example: shipments_keyboard -->
```cpp
#include <iostream>
#include <string>
#include <vector>

struct Shipment {
    std::string destination;
    int boxes;
};

bool read_shipment_values(std::istream& input, const std::string& destination, Shipment& result) {
    int boxes{0};
    input >> boxes;

    if (input.fail()) {
        return false;
    }

    if (boxes < 0) {
        return false;
    }

    result = Shipment{destination, boxes};
    return true;
}

int main() {
    std::vector<Shipment> shipments{};
    std::string destination{};
    std::getline(std::cin, destination);

    while (!std::cin.fail() && !destination.empty()) {
        Shipment shipment{"", 0};
        const bool accepted{read_shipment_values(std::cin, destination, shipment)};

        if (!accepted) {
            if (std::cin.fail()) {
                std::cout << "Input error\n";
            } else {
                std::cout << "Invalid shipments\n";
            }

            return 0;
        }

        shipments.push_back(shipment);

        std::string rest{};
        std::getline(std::cin, rest);

        if (!std::cin.fail()) {
            std::getline(std::cin, destination);
        }
    }

    int total_boxes{0};
    std::cout << "Shipments: " << shipments.size() << "\n";

    for (const Shipment& shipment : shipments) {
        std::cout << shipment.destination << ": " << shipment.boxes << "\n";
        total_boxes += shipment.boxes;
    }

    std::cout << "Total boxes: " << total_boxes << "\n";
}
```

</details>

Zbuduj i uruchom program. W oknie **Run** wpisz dane, a na końcu naciśnij **Enter** na pustej linii, jak w lekcji 10.4:

<!-- input: shipments_keyboard -->
```text
North Hub
4
South Depot
7

```

<!-- output: shipments_keyboard -->
```text
Shipments: 2
North Hub: 4
South Depot: 7
Total boxes: 11
```

To pierwsze obowiązkowe uruchomienie. Zapamiętaj ten raport: za chwilę te same dane trafią do programu z pliku.

## 3. Te same rekordy z pliku

Zmień `main` tak, żeby czytał z pliku `shipments.txt`. Typu `Shipment` i funkcji `read_shipment_values` nie zmieniaj. Cały program po zmianach:

<!-- example: shipments_file -->
```cpp
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

struct Shipment {
    std::string destination;
    int boxes;
};

bool read_shipment_values(std::istream& input, const std::string& destination, Shipment& result) {
    int boxes{0};
    input >> boxes;

    if (input.fail()) {
        return false;
    }

    if (boxes < 0) {
        return false;
    }

    result = Shipment{destination, boxes};
    return true;
}

int main() {
    std::ifstream input{"shipments.txt"};

    if (input.fail()) {
        std::cout << "Cannot open shipments.txt\n";
        return 0;
    }

    std::vector<Shipment> shipments{};
    std::string destination{};
    std::getline(input, destination);

    while (!input.fail() && !destination.empty()) {
        Shipment shipment{"", 0};
        const bool accepted{read_shipment_values(input, destination, shipment)};

        if (!accepted) {
            if (input.fail()) {
                std::cout << "Input error\n";
            } else {
                std::cout << "Invalid shipments\n";
            }

            return 0;
        }

        shipments.push_back(shipment);

        std::string rest{};
        std::getline(input, rest);

        if (!input.fail()) {
            std::getline(input, destination);
        }
    }

    int total_boxes{0};
    std::cout << "Shipments: " << shipments.size() << "\n";

    for (const Shipment& shipment : shipments) {
        std::cout << shipment.destination << ": " << shipment.boxes << "\n";
        total_boxes += shipment.boxes;
    }

    std::cout << "Total boxes: " << total_boxes << "\n";
}
```

Co się zmieniło w porównaniu z wersją z klawiaturą:

| Wersja z klawiaturą | Wersja z plikiem |
|---|---|
| brak | `#include <fstream>` |
| brak | `std::ifstream input{"shipments.txt"};` i zaraz po nim sprawdzenie `input.fail()` z komunikatem `Cannot open shipments.txt` |
| `std::getline(std::cin, destination);` (dwa razy) | `std::getline(input, destination);` |
| `std::cin.fail()` (trzy razy) | `input.fail()` |
| `read_shipment_values(std::cin, destination, shipment)` | `read_shipment_values(input, destination, shipment)` |
| `std::getline(std::cin, rest);` | `std::getline(input, rest);` |

- **Typ i funkcja są te same, co do znaku.** Zmienił się tylko argument wywołania: zamiast `std::cin` funkcja dostaje `input`.
- **W `main` nie zostało żadne `std::cin`.** Każdy odczyt i każde sprawdzenie `fail()` dotyczy tego samego strumienia `input`. Gdyby choć jedno `std::getline` zostało przy `std::cin`, program czytałby część danych z pliku, a część z klawiatury (punkt 9).
- **Ta sama nazwa `input` w `main` i w funkcji to przypadek.** Parametr byłby inną nazwą przekazanego strumienia także wtedy, gdyby zmienna w `main` nazywała się na przykład `shipments_file`. Liczy się to, co przekazujesz przy wywołaniu.

| Element | Standardowe wejście | Plik |
|---|---|---|
| źródło danych | `std::cin` | otwarty `std::ifstream` |
| kto przygotowuje strumień | jest gotowy od startu programu | `main` otwiera plik i sprawdza otwarcie |
| typ parametru funkcji | `std::istream&` | `std::istream&` |
| algorytm odczytu rekordu | ten sam | ten sam |
| funkcja wypełniająca rekord | ta sama | ta sama |
| raport | ten sam | ten sam |

**Plik z danymi.** W katalogu `lesson_12_2`, obok `main.cpp` i `CMakeLists.txt`, utwórz plik `shipments.txt`, tak jak `steps.txt` w lekcji 12.1, punkt 3. Wpisz do niego te same dane co w punkcie 2, ale bez pustej linii na końcu:

<!-- run: shipments_file -->

<!-- datafile: shipments_file shipments.txt -->
```text
North Hub
4
South Depot
7
```

Potem:

1. Sprawdź pole **Working directory** konfiguracji `first_program`, jak w lekcji 12.1, punkt 4. Ma wskazywać katalog `lesson_12_2`, ten z `shipments.txt`.
2. Zbuduj i uruchom program. Niczego nie wpisuj w oknie **Run**: program nie czeka na klawiaturę.

<!-- output: shipments_file -->
```text
Shipments: 2
North Hub: 4
South Depot: 7
Total boxes: 11
```

To drugie obowiązkowe uruchomienie. Raport jest dokładnie taki sam jak z klawiatury.

**Te same dane, ten sam wynik.** Z klawiatury dane kończyła pusta linia, a w pliku kończy je koniec pliku. Według lekcji 10.4 obie sytuacje oznaczają zakończenie danych, więc raport jest ten sam. Jak sprawdzić, że funkcja działa według tej samej umowy dla obu źródeł? Podać obu wersjom programu te same dane i porównać standardowe wyjście. Testy automatyczne kursu robią to dla kilku zestawów danych (punkt 6).

## 4. Kto za co odpowiada

| Kod wywołujący (`main`) | Funkcja `read_shipment_values` |
|---|---|
| wybiera źródło danych: `std::cin` albo plik | dostaje istniejący strumień |
| otwiera plik, jeśli dane są w pliku, i sprawdza otwarcie | nie zna nazwy pliku i niczego nie otwiera |
| odczytuje nazwę i decyduje, czy dane się skończyły | odczytuje liczbę i sprawdza, czy jest dozwolona |
| wywołuje funkcję i po odmowie wybiera komunikat | wypełnia rekord dopiero po sukcesie, a przy odmowie zostawia go bez zmian |
| buduje wektor przez `push_back` | o wyniku informuje przez `bool` |
| wypisuje raport albo komunikat | niczego nie wypisuje |

- **Dlaczego funkcja nie otwiera pliku?** Gdyby w jej treści stało `std::ifstream input{"shipments.txt"};`, umiałaby czytać tylko z tego jednego pliku, a każde wywołanie otwierałoby go od nowa i zaczynało od pierwszej linii. Funkcja, która dostaje strumień, czyta z każdego źródła, zawsze od miejsca, w którym skończył wywołujący.
- **Dlaczego funkcja niczego nie wypisuje?** Gdyby sama wypisywała `Input error`, każdy program, który jej używa, musiałby przyjąć ten komunikat. Funkcja tylko mówi, czy się udało, a `main` zna całą sytuację i decyduje, co wypisać.
- **Bez kopii funkcji.** Nie potrzebujesz osobnych `read_shipment_from_file` i `read_shipment_from_keyboard`. Dwie kopie tego samego algorytmu trzeba by poprawiać w dwóch miejscach, a różnice między nimi łatwo przeoczyć.
- **Jeden plik źródłowy wystarczy.** Funkcję można by przenieść do osobnej pary plików `.hpp` i `.cpp`, jak części programu w lekcji 11.4, i działałaby tak samo. To, że przyjmuje różne strumienie, wynika z typu parametru, a nie z pliku, w którym leży.

## 5. Kontrakt danych tej lekcji

> **Kontrakt danych tej lekcji.** Program korzysta z formatu z lekcji 10.4. W poprawnych danych:
>
> - każda przesyłka zajmuje dwie linie: nazwę miejsca docelowego i liczbę paczek;
> - nazwa nie jest pusta, może zawierać spacje i może się powtarzać, a liczba paczek nie jest ujemna;
> - przesyłek jest najwyżej 5;
> - dane kończy koniec pliku albo pusta linia w miejscu kolejnej nazwy;
> - między przesyłkami nie ma pustych linii;
> - tekstu po liczbie w jej linii program nie sprawdza.
>
> Program działa poprawnie **dla tak określonych danych**. Nie sprawdza każdego błędu, który może się zdarzyć w pliku tekstowym.

| Sytuacja | Standardowe wyjście |
|---|---|
| pliku nie udało się otworzyć | `Cannot open shipments.txt` |
| po niepustej nazwie liczby nie udało się odczytać, także gdy plik kończy się zaraz po nazwie | `Input error` |
| liczba jest odczytana, ale ujemna | `Invalid shipments` |
| dane się zakończyły | `Shipments: N`, przesyłki w kolejności z pliku i `Total boxes: T` |

Komunikaty błędów są takie jak w lekcji 10.4, nowy jest tylko `Cannot open shipments.txt`. Po komunikacie nie ma częściowego raportu, a program kończy się kodem 0.

**Przewidź** wynik każdego przypadku, zanim otworzysz zwinięty blok. Uruchamianie ich jest nieobowiązkowe: zmieniasz tylko zawartość albo nazwę `shipments.txt`, bez ponownego budowania.

**B: pusty plik.** `shipments.txt` istnieje, ale nie ma w nim ani jednego znaku.

<!-- run: shipments_file -->

<!-- datafile: shipments_file shipments.txt -->
```text
```

<details>
<summary>Standardowe wyjście dla B</summary>

<!-- output: shipments_file -->
```text
Shipments: 0
Total boxes: 0
```

Otwarcie się udaje. Pierwszy odczyt nazwy trafia na koniec pliku, więc pętla nie wykonuje się ani razu. To poprawne zakończenie danych: lista bez przesyłek. W lekcji 12.1 pusty plik dawał `Input error`, bo kontrakt wymagał liczby dni. Tutaj kontrakt nie wymaga żadnego rekordu. **O tym, co znaczy pusty plik, decyduje kontrakt.**

</details>

**C: pusta linia na końcu.** Po jednej przesyłce jest pusta linia.

<!-- run: shipments_file -->

<!-- datafile: shipments_file shipments.txt -->
```text
North Hub
4

```

<details>
<summary>Standardowe wyjście dla C</summary>

<!-- output: shipments_file -->
```text
Shipments: 1
North Hub: 4
Total boxes: 4
```

Pusta linia w miejscu kolejnej nazwy kończy dane, tak jak pusta linia wpisana w oknie **Run**.

</details>

**D: brak pliku.** W katalogu roboczym nie ma `shipments.txt`.

<!-- run: shipments_file -->

<details>
<summary>Standardowe wyjście dla D</summary>

<!-- output: shipments_file -->
```text
Cannot open shipments.txt
```

Otwarcie się nie udaje, więc program niczego nie odczytuje. Nie wypisuje `Shipments: 0`, bo nie wie, co jest w pliku, którego nie dostał.

</details>

**E: niedozwolona liczba paczek** w drugiej przesyłce.

<!-- run: shipments_file -->

<!-- datafile: shipments_file shipments.txt -->
```text
North Hub
4
South Depot
-2
```

<details>
<summary>Standardowe wyjście dla E</summary>

<!-- output: shipments_file -->
```text
Invalid shipments
```

`-2` odczytuje się poprawnie, ale jest ujemne. Funkcja zwraca `false`, a `input.fail()` daje `false`, więc `main` wybiera `Invalid shipments`. Pierwsza przesyłka jest już w wektorze, ale raportu nie ma.

</details>

**F: słowo zamiast liczby** w drugiej przesyłce.

<!-- run: shipments_file -->

<!-- datafile: shipments_file shipments.txt -->
```text
North Hub
4
South Depot
seven
```

<details>
<summary>Standardowe wyjście dla F</summary>

<!-- output: shipments_file -->
```text
Input error
```

Odczyt `seven` przez `>>` się nie udaje, więc po `false` funkcji `input.fail()` daje `true`.

</details>

**G: brak liczby po nazwie.** Plik kończy się zaraz po nazwie drugiej przesyłki.

<!-- run: shipments_file -->

<!-- datafile: shipments_file shipments.txt -->
```text
North Hub
4
South Depot
```

<details>
<summary>Standardowe wyjście dla G</summary>

<!-- output: shipments_file -->
```text
Input error
```

Niepusta nazwa rozpoczyna rekord, więc koniec pliku zaraz po niej to niekompletny rekord, a nie zakończenie danych (lekcja 10.4, punkt 4). Ostatnia nazwa nie trafia do raportu jako przesyłka.

</details>

**H: ostatnia liczba bez końca linii.** Dane z punktu 3, ale po `7` nie ma już znaku końca linii.

<!-- run: shipments_file -->

<!-- datafile: shipments_file shipments.txt noeol -->
```text
North Hub
4
South Depot
7
```

<details>
<summary>Standardowe wyjście dla H</summary>

<!-- output: shipments_file -->
```text
Shipments: 2
North Hub: 4
South Depot: 7
Total boxes: 11
```

`>>` odczytuje 7 i dochodzi do końca pliku, a funkcja zwraca `true`. Nie udaje się dopiero `std::getline(input, rest)`, więc `main` nie odczytuje następnej nazwy, a pętla kończy się na `fail()` w warunku. W lekcji 10.4 ten przypadek był tylko w tabeli, bo z klawiatury testy automatyczne nie umiały go podać. Plik bez końca linii po ostatnim wierszu powstaje łatwo, na przykład gdy po ostatniej liczbie nie naciśniesz **Enter**. Takiego pliku nie musisz przygotowywać.

</details>

Gdzie mogą się skończyć dane i co wtedy wypisuje program:

| Gdzie kończą się dane | Przypadek | Wynik |
|---|---|---|
| przed pierwszą nazwą: pusty plik | B | raport bez przesyłek |
| na pustej linii w miejscu nazwy | C | raport |
| zaraz po nazwie, przed liczbą | G | `Input error` |
| zaraz po ostatniej liczbie, bez końca linii | H | raport |
| po końcu linii z ostatnią liczbą | A | raport |

## 6. Granica kontraktu: pusta linia w środku

**I: pusta linia między przesyłkami.** Ktoś zapisał w pliku dwie przesyłki, ale między nimi zostawił pustą linię:

<!-- run: shipments_file -->

<!-- datafile: shipments_file shipments.txt -->
```text
North Hub
4

South Depot
7
```

**Przewidź**, ile przesyłek pokaże raport.

<details>
<summary>Standardowe wyjście dla I</summary>

<!-- output: shipments_file -->
```text
Shipments: 1
North Hub: 4
Total boxes: 4
```

</details>

Program zatrzymuje odczyt na pustej linii, bo tak każe kontrakt: pusta linia w miejscu nazwy kończy dane. `South Depot` i `7` zostają w pliku nieodczytane, a raport nic o nich nie mówi. **To nie jest odczyt obu przesyłek.** Program nie ma tu błędu: dla danych zgodnych z kontraktem działa poprawnie, a ten plik łamie kontrakt, bo między przesyłkami nie wolno zostawiać pustej linii. Jeśli jednak plik miał zawierać dwie przesyłki, raport jest niekompletny, a nic tego nie sygnalizuje.

**Dlaczego w pliku to większy problem niż przy klawiaturze?** Przy wpisywaniu w oknie **Run** pusta linia to świadoma decyzja: naciskasz **Enter**, bo lista się skończyła. W pliku nikt nie wpisuje osobnej linii „koniec”, bo plik kończy się sam. Pusta linia w środku pliku łatwo pojawia się przypadkiem, na przykład przy dopisywaniu albo kopiowaniu danych, a program po cichu pomija wszystko, co jest za nią.

**Pytanie na później.** Co powinien zrobić program, jeżeli pusta linia pojawi się między dwiema przesyłkami, a chcemy odczytać wszystkie rekordy albo przynajmniej dowiedzieć się, że z plikiem jest coś nie tak? Zapisz swoją odpowiedź. Wrócisz do tego pytania w kolejnej lekcji Modułu 12.

<details>
<summary>Pozostałe przypadki kontrolne: otwórz po przewidywaniach</summary>

Wszystkie te przypadki są sprawdzane automatycznie. Wyniki wynikają z kontraktu z punktu 5.

**J: jedna przesyłka.**

<!-- run: shipments_file -->

<!-- datafile: shipments_file shipments.txt -->
```text
East Gate
3
```

<!-- output: shipments_file -->
```text
Shipments: 1
East Gate: 3
Total boxes: 3
```

**K: pięć przesyłek,** największa liczba w kontrakcie, w tym przesyłka z zerem paczek.

<!-- run: shipments_file -->

<!-- datafile: shipments_file shipments.txt -->
```text
Central Hub
2
North Hub
4
River Port
0
South Depot
7
West End Depot
1
```

<!-- output: shipments_file -->
```text
Shipments: 5
Central Hub: 2
North Hub: 4
River Port: 0
South Depot: 7
West End Depot: 1
Total boxes: 14
```

**L: ta sama nazwa dwa razy.** Każde wystąpienie to osobna przesyłka.

<!-- run: shipments_file -->

<!-- datafile: shipments_file shipments.txt -->
```text
North Hub
4
North Hub
0
```

<!-- output: shipments_file -->
```text
Shipments: 2
North Hub: 4
North Hub: 0
Total boxes: 4
```

**M: słowo zamiast liczby w pierwszej przesyłce.**

<!-- run: shipments_file -->

<!-- datafile: shipments_file shipments.txt -->
```text
North Hub
four
```

<!-- output: shipments_file -->
```text
Input error
```

**N: pusta linia na samym początku.** Plik ma jedną linię i jest ona pusta, więc dane kończą się, zanim zacznie się pierwsza przesyłka. Raport jest taki sam jak dla pustego pliku.

<!-- run: shipments_file -->

<!-- datafile: shipments_file shipments.txt -->
```text

```

<!-- output: shipments_file -->
```text
Shipments: 0
Total boxes: 0
```

</details>

<details>
<summary>Te same dane w wersji z klawiaturą: otwórz po przewidywaniach</summary>

Wersja z punktu 2 to program z lekcji 10.4. Testy automatyczne tamtej lekcji sprawdzają go z klawiatury dla dokładnie tych samych znaków co przypadki A, E, F, G, I, J, K i N tej lekcji, z tymi samymi wynikami. Tak musi być, bo funkcja i pętla są w obu wersjach takie same. Tutaj sprawdzamy jeszcze dane A bez pustej linii na końcu, czyli dokładnie te znaki, które wersja z punktu 3 znajduje w pliku:

<!-- input: shipments_keyboard -->
```text
North Hub
4
South Depot
7
```

<!-- output: shipments_keyboard -->
```text
Shipments: 2
North Hub: 4
South Depot: 7
Total boxes: 11
```

Tylko brak pliku (D) nie ma odpowiednika z klawiatury: przy `std::cin` nie ma czego otwierać.

</details>

## 7. Diagnostyka: strumień przekazany przez wartość

**Sytuacja.** Ktoś uznał, że `&` w nagłówku `read_shipment_values` jest zbędny, bo „funkcja przecież tylko czyta”. Usunął go i zapisał parametr jako `std::istream input`. Sprawdź, co na to kompilator.

1. W `main.cpp` projektu `lesson_12_2` zmień w nagłówku funkcji `std::istream& input` na `std::istream input`. Niczego więcej nie zmieniaj.
2. **Przewidź:** czy program się zbuduje? Jeśli nie, czy będzie to błąd kompilacji, czy linkowania? Którą linijkę wskaże kompilator?
3. Zbuduj projekt (**Build | Build Project**). To trzecie obowiązkowe uruchomienie: tym razem uruchamiasz budowanie, a nie program.
4. W oknie **Build** znajdź pierwszy błąd: plik, linijkę i treść komunikatu.
5. Ustal, która linijka zawiera błąd, a która go powoduje.
6. Przywróć `&`, czyli `std::istream& input`. Zbuduj i uruchom program. To czwarte obowiązkowe uruchomienie: program znowu wypisuje raport z punktu 3.

<details>
<summary>Program z błędem: taki, jaki powstaje po kroku 1</summary>

<!-- broken: shipments_by_value at=41:50 errors=1 error=^call to deleted constructor of 'std::istream' -->
```cpp
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

struct Shipment {
    std::string destination;
    int boxes;
};

bool read_shipment_values(std::istream input, const std::string& destination, Shipment& result) {
    int boxes{0};
    input >> boxes;

    if (input.fail()) {
        return false;
    }

    if (boxes < 0) {
        return false;
    }

    result = Shipment{destination, boxes};
    return true;
}

int main() {
    std::ifstream input{"shipments.txt"};

    if (input.fail()) {
        std::cout << "Cannot open shipments.txt\n";
        return 0;
    }

    std::vector<Shipment> shipments{};
    std::string destination{};
    std::getline(input, destination);

    while (!input.fail() && !destination.empty()) {
        Shipment shipment{"", 0};
        const bool accepted{read_shipment_values(input, destination, shipment)};

        if (!accepted) {
            if (input.fail()) {
                std::cout << "Input error\n";
            } else {
                std::cout << "Invalid shipments\n";
            }

            return 0;
        }

        shipments.push_back(shipment);

        std::string rest{};
        std::getline(input, rest);

        if (!input.fail()) {
            std::getline(input, destination);
        }
    }

    int total_boxes{0};
    std::cout << "Shipments: " << shipments.size() << "\n";

    for (const Shipment& shipment : shipments) {
        std::cout << shipment.destination << ": " << shipment.boxes << "\n";
        total_boxes += shipment.boxes;
    }

    std::cout << "Total boxes: " << total_boxes << "\n";
}
```

</details>

<details>
<summary>Co się dzieje i jak to naprawić: otwórz po kroku 5</summary>

1. **To błąd kompilacji.** Kompilacja `main.cpp` się nie udaje, więc do linkowania nie dochodzi. W wyniku budowania wygląda to mniej więcej tak (ścieżki skrócone, notatki z wnętrza biblioteki standardowej pominięte):

   ```text
   main.cpp:41:50: error: call to deleted constructor of 'std::istream' (aka 'basic_istream<char>')
   main.cpp:11:40: note: passing argument to parameter 'input' here
   ```

   Na Windowsie, Ubuntu i macOS ścieżki i notatka z wnętrza biblioteki wyglądają inaczej. Błąd wskazuje to samo miejsce i zaczyna się tak samo, a na Windowsie inny jest tylko dopisek w nawiasie: `(aka 'basic_istream<char, char_traits<char>>')`.
2. **Błąd wskazuje wywołanie, a przyczyna jest w nagłówku.** Linijka 41 to wywołanie `read_shipment_values(input, destination, shipment)` w `main`, a kolumna 50 to argument `input`. Notatka `note:` wskazuje parametr `input` w linijce 11: tam brakuje `&`.
3. **Co mówi komunikat.** Parametr bez `&` to nowy obiekt, tworzony przy wywołaniu jako kopia argumentu (lekcja 9.1). *Constructor* (konstruktor) to w C++ operacja, która tworzy nowy obiekt danego typu, a *deleted* (usunięty) znaczy, że biblioteka standardowa celowo jej zabroniła. Komunikat mówi więc: żeby wywołać tę funkcję, trzeba by utworzyć nowy `std::istream` jako kopię `input`, a strumienia wejścia nie wolno kopiować.
4. **Dlaczego strumienia się nie kopiuje.** Strumień to nie zwykła wartość, jak liczba: jest związany z jednym źródłem danych i pamięta, dokąd już doczytał. Funkcja ma czytać z tego samego strumienia co `main`, od miejsca, w którym `main` skończył, i zostawić go tam, gdzie sama skończyła. Do tego potrzebna jest referencja.
5. **Poprawka:** przywróć `&`. Program buduje się i wypisuje ten sam raport co w punkcie 3. Dodanie `const` nie jest poprawką: odczyt zmienia strumień, więc z parametrem `const std::istream&` kompilator odrzuci `input >> boxes` (punkt 9).
6. **Z `std::cin` jest tak samo.** W wersji z klawiaturą, z parametrem bez `&`, kompilator zgłasza ten sam błąd przy argumencie `std::cin`: nie wolno kopiować żadnego strumienia wejścia.

</details>

## 8. Misja: wypożyczenia w bibliotece szkolnej

Biblioteka szkolna zapisuje w pliku, ile egzemplarzy każdego tytułu jest wypożyczonych. Program odczytuje plik `loans.txt` i wypisuje wszystkie wpisy oraz łączną liczbę wypożyczonych egzemplarzy.

**Kontrakt pliku `loans.txt`:**

- każdy wpis zajmuje dwie linie: tytuł książki, a w następnej linii liczbę wypożyczonych egzemplarzy tego tytułu;
- tytuł może zawierać spacje i nie jest pusty, bo pusta linia kończy dane;
- ten sam tytuł może wystąpić kilka razy, a każde wystąpienie to osobny wpis;
- liczba egzemplarzy to liczba całkowita od 0 do 12;
- wpisów jest najwyżej 5, więc suma wynosi najwyżej 5 · 12 = 60;
- dane kończy koniec pliku albo pusta linia w miejscu kolejnego tytułu, a między wpisami nie ma pustych linii;
- tekstu po liczbie w jej linii program nie sprawdza.

**Komunikaty:**

| Sytuacja | Standardowe wyjście |
|---|---|
| pliku nie udało się otworzyć | `Cannot open loans.txt` |
| po niepustym tytule liczby nie udało się odczytać | `Input error` |
| liczba jest odczytana, ale spoza zakresu od 0 do 12 | `Invalid loans` |
| dane się zakończyły | `Loans: N`, każdy wpis w kolejności z pliku, na przykład `Science Atlas: 2` i `Total copies: T` |

Program nie sortuje wpisów i nie usuwa powtórzeń. Raport wypisuje dopiero po przetworzeniu wszystkich wpisów, a po błędzie tylko jeden komunikat, bez częściowego raportu. Nie zadaje pytań i kończy się kodem 0.

**Wymagania:**

- Program definiuje własny typ wpisu z dwoma polami: tytułem (`std::string`) i liczbą egzemplarzy (`int`), i zbiera wpisy w początkowo pustym wektorze.
- Liczbę jednego wpisu odczytuje i sprawdza osobna funkcja. Dostaje strumień przez `std::istream&`, tytuł przez `const std::string&` i istniejący rekord wynikowy przez referencję bez `const`. Liczbę odczytuje do zmiennej lokalnej, a rekord przypisuje dopiero po sprawdzeniu odczytu i zakresu. Zwraca `true` albo `false`, a przy `false` rekord wynikowy zostaje bez zmian. Niczego nie wypisuje, nie otwiera pliku i nie używa `std::cin`.
- `main` otwiera `loans.txt` i sprawdza otwarcie, odczytuje tytuły, rozpoznaje zakończenie danych, wywołuje funkcję, dodaje rekord przez `push_back` tylko po `true` i po odmowie odróżnia `Input error` od `Invalid loans`.

W `cpp-workspace` utwórz katalog `library_loans`, skopiuj do niego `CMakeLists.txt` z oryginalnego `lesson_05_first_program`, utwórz pusty `main.cpp` i plik `loans.txt`. `CMakeLists.txt` zostaw bez zmian, a `loans.txt` nie dopisuj do `add_executable`: plik odczytuje działający program, kompilator go nie czyta. Otwórz katalog w CLionie i sprawdź **Working directory**, jak w lekcji 12.1, punkt 4. Jeden plik `main.cpp` wystarczy. Napisz program samodzielnie.

```text
library_loans/
├── CMakeLists.txt
├── loans.txt
└── main.cpp
```

Musisz samodzielnie zdecydować:

1. jak nazwać typ, jego pola, wektor, funkcję, jej parametry i zmienną strumienia plikowego;
2. w jakiej kolejności funkcja odczytuje liczbę, sprawdza odczyt i zakres i w którym miejscu przypisuje rekord wynikowy;
3. gdzie `main` otwiera plik i sprawdza otwarcie;
4. gdzie `main` odczytuje kolejne tytuły i po czym poznaje zakończenie danych;
5. kiedy dokańczać linię liczbową;
6. jak po odmowie odróżnić `Input error` od `Invalid loans`;
7. jak nie dopuścić do częściowego raportu;
8. jak obliczyć sumę z elementów wektora;
9. jakie dane ujawniłyby, że funkcja zmienia rekord wynikowy przed sprawdzeniem zakresu.

**Przypadki A–J.** Każdy przypadek to inna zawartość `loans.txt` albo brak pliku.

**A: dwa wpisy.**

<!-- run: loans -->

<!-- datafile: loans loans.txt -->
```text
Science Atlas
2
History Notes
3
```

<!-- output: loans -->
```text
Loans: 2
Science Atlas: 2
History Notes: 3
Total copies: 5
```

**B: pusty plik.**

<!-- run: loans -->

<!-- datafile: loans loans.txt -->
```text
```

<!-- output: loans -->
```text
Loans: 0
Total copies: 0
```

**C: brak pliku.** W katalogu roboczym nie ma `loans.txt`.

<!-- run: loans -->

<!-- output: loans -->
```text
Cannot open loans.txt
```

**D: słowo zamiast liczby** w drugim wpisie.

<!-- run: loans -->

<!-- datafile: loans loans.txt -->
```text
Science Atlas
2
History Notes
seven
```

<!-- output: loans -->
```text
Input error
```

**E: niedozwolona liczba** w drugim wpisie.

<!-- run: loans -->

<!-- datafile: loans loans.txt -->
```text
Science Atlas
2
History Notes
-1
```

<!-- output: loans -->
```text
Invalid loans
```

**F: przerwany wpis.** Plik kończy się zaraz po drugim tytule.

<!-- run: loans -->

<!-- datafile: loans loans.txt -->
```text
Science Atlas
2
History Notes
```

<!-- output: loans -->
```text
Input error
```

**G: pusta linia kończy dane.**

<!-- run: loans -->

<!-- datafile: loans loans.txt -->
```text
Science Atlas
2

```

<!-- output: loans -->
```text
Loans: 1
Science Atlas: 2
Total copies: 2
```

**H: pusta linia przed następnym wpisem.** Granica kontraktu, jak w punkcie 6: drugi wpis nie trafia do raportu.

<!-- run: loans -->

<!-- datafile: loans loans.txt -->
```text
Science Atlas
2

History Notes
3
```

<!-- output: loans -->
```text
Loans: 1
Science Atlas: 2
Total copies: 2
```

**I: dane A bez końca linii po ostatniej liczbie.**

<!-- run: loans -->

<!-- datafile: loans loans.txt noeol -->
```text
Science Atlas
2
History Notes
3
```

<!-- output: loans -->
```text
Loans: 2
Science Atlas: 2
History Notes: 3
Total copies: 5
```

**J: ten sam tytuł dwa razy.**

<!-- run: loans -->

<!-- datafile: loans loans.txt -->
```text
Science Atlas
2
Science Atlas
4
```

<!-- output: loans -->
```text
Loans: 2
Science Atlas: 2
Science Atlas: 4
Total copies: 6
```

**Zanim napiszesz program**, przygotuj tabelę: przypadki A–J i co najmniej dwa własne, na przykład z granicami zakresu, z oczekiwanym wynikiem ustalonym z kontraktu.

**Potem uruchom program dla A.** To piąte obowiązkowe uruchomienie. Pozostałe przypadki prześledź na kartce, linijka po linijce swojego programu, i porównaj z wynikami podanymi wyżej. Jeśli masz czas, uruchom też B albo H: zmieniasz tylko zawartość `loans.txt`, nie kod. Wszystkie przypadki są sprawdzane automatycznie w rozwiązaniu referencyjnym.

### Kryterium sukcesu

- Program buduje się jako C++20 i dla A wypisuje dokładnie pokazany wynik.
- Twoje przewidywania dla B–J zgadzają się z wynikami podanymi wyżej.
- Funkcja dostaje strumień przez `std::istream&`, tytuł przez `const std::string&` i rekord wynikowy przez referencję, a przypisuje rekord dopiero po sprawdzeniu odczytu i zakresu.
- W funkcji nie ma `std::cin`, `std::cout` ani otwierania pliku.
- `main` sprawdza otwarcie, zanim cokolwiek odczyta, dodaje rekord tylko po `true` i przy błędzie nie wypisuje żadnej części raportu.
- `loans.txt` nie jest w `add_executable`, `CMakeLists.txt` jest taki jak w lekcji 0.5, a **Working directory** wskazuje katalog z `loans.txt`.
- Umiesz wyjaśnić, dlaczego dla H raport ma tylko jeden wpis i dlaczego to granica kontraktu, a nie błąd programu.

Gdy wynik się zgadza, możesz zapisać projekt w Gicie, jak w lekcji 1.5: `main.cpp`, `CMakeLists.txt` i `loans.txt` z danymi A, bez katalogu budowania.

<details>
<summary>Podpowiedź 1: wspólny parametr</summary>

Funkcja z punktu 1 nie wie, skąd pochodzą dane, i dlatego pasuje do każdego źródła. Jaki typ parametru pozwoli Twojej funkcji czytać z otwartego pliku, a w razie potrzeby także ze `std::cin`? Kto w Twoim programie powinien znać nazwę `loans.txt`?

</details>

<details>
<summary>Podpowiedź 2: rekord i odmowa</summary>

Najpierw odczytaj liczbę do zmiennej lokalnej i sprawdź `fail()`, potem zakres od 0 do 12. Rekord wynikowy przypisz dopiero na końcu, jednym przypisaniem całego rekordu, jak `result = Shipment{destination, boxes};` w lekcji 10.4. Każda odmowa to `return false;` przed tym przypisaniem.

</details>

<details>
<summary>Podpowiedź 3: koniec danych i plik</summary>

Rozróżnij cztery sytuacje: plik, którego nie udało się otworzyć (sprawdź zaraz po utworzeniu strumienia); koniec pliku albo pusta linia w miejscu tytułu (koniec danych, raport); koniec pliku po niepustym tytule (`Input error`); poprawny wpis (`push_back`, dokończenie linii liczbowej i następny tytuł). Odczyt tytułu i warunek pętli są takie jak w `main` z punktu 3.

</details>

Przykładowe rozwiązanie jest w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 9. Gdy coś pójdzie inaczej

| Co widzisz | Co to znaczy | Co zrobić |
|---|---|---|
| Program nic nie wypisuje i czeka | W `main` zostało `std::cin`, na przykład w `std::getline(std::cin, destination)`, więc program czeka na klawiaturę. | Zamień każde `std::cin` w `main` na zmienną strumienia plikowego. |
| Kompilator zgłasza `call to deleted constructor of 'std::istream'` | Parametr strumienia nie ma `&`, więc wywołanie próbuje skopiować strumień (punkt 7). | Zapisz parametr jako `std::istream&`. |
| Kompilator zgłasza przy `>>` `invalid operands to binary expression`, a w komunikacie jest `const std::istream` | Parametr strumienia ma `const`, a odczyt zmienia strumień. | Usuń `const` z parametru strumienia. |
| `Cannot open shipments.txt`, choć plik istnieje | Plik nie leży w katalogu roboczym albo ma inną nazwę. | Wykonaj kroki z lekcji 12.1, punkt 7: nazwa, wielkość liter, **Working directory**, położenie pliku. |
| Raport ma mniej przesyłek, niż jest w pliku, i nie ma żadnego komunikatu | W środku pliku jest pusta linia, która kończy dane (punkt 6). | Usuń pustą linię: plik łamie kontrakt tej lekcji. |
| `Input error`, choć dane wyglądają poprawnie | W miejscu liczby jest litera, na przykład `O` zamiast `0`, albo brakuje linii z liczbą po ostatniej nazwie. | Sprawdź plik linia po linii: po każdej nazwie musi stać linia z liczbą. |

## 10. Wyjaśnij

Odpowiedz własnymi słowami, najlepiej na piśmie. Dopiero potem porównaj z przykładowymi odpowiedziami.

1. Dlaczego `read_shipment_values` przyjmuje `std::istream&`, zamiast czytać bezpośrednio ze `std::cin`?
2. Co zmienia się w programie przy przejściu z klawiatury na plik, a co zostaje bez zmian? Jak sprawdzisz, że obie wersje działają według tej samej umowy?
3. Dlaczego otwarty `std::ifstream` można przekazać do funkcji, która oczekuje `std::istream&`? Czy `std::cin` i strumień plikowy to ten sam obiekt?
4. Co się dzieje, gdy parametr strumienia nie ma `&`? Gdzie kompilator wskazuje błąd, a gdzie jest jego przyczyna?
5. Dlaczego parametr strumienia nie ma `const`?
6. Dlaczego plik otwiera `main`, a nie funkcja odczytu? Co by się stało, gdyby funkcja przy każdym wywołaniu otwierała `shipments.txt`?
7. Funkcja zwróciła `false`, choć odczyt liczby z pliku się udał. Kiedy tak się dzieje, co jest wtedy w rekordzie wynikowym i kto wybiera komunikat?
8. Jeden plik kończy się zaraz po nazwie drugiej przesyłki, a drugi zaraz po jej liczbie, bez końca linii. Dlaczego wyniki są różne?
9. Co wypisze program, gdy między dwiema przesyłkami w pliku jest pusta linia? Czy to błąd programu?
10. Dlaczego program z tej lekcji nie jest jeszcze ogólnym czytnikiem plików tekstowych? Podaj dwie rzeczy, których nie sprawdza.

<details>
<summary>Przykładowe odpowiedzi</summary>

1. Bo wtedy funkcja nie zależy od źródła danych. Czyta z tego strumienia, który dostanie: ze `std::cin` albo z otwartego pliku. Funkcja na sztywno związana ze `std::cin` musiałaby mieć drugą kopię do czytania z pliku.
2. Zmienia się tylko `main`: dochodzi `#include <fstream>`, otwarcie pliku z jego sprawdzeniem, a każde `std::cin` zastępuje zmienna strumienia plikowego. Typ, funkcja, pętla i raport zostają te same. Sprawdzam to, podając obu wersjom te same dane i porównując standardowe wyjście.
3. Bo `std::ifstream` to rodzaj strumienia wejścia: ma `>>`, `fail()` i współpracuje ze `std::getline`, czyli ma wszystko, czego funkcja potrzebuje od `std::istream`. To nie jest ten sam obiekt: `std::cin` czyta z klawiatury, a strumień plikowy z pliku. Wspólny jest tylko sposób korzystania z nich.
4. Parametr bez `&` to kopia argumentu, a strumienia wejścia nie wolno kopiować. Kompilator zgłasza `call to deleted constructor of 'std::istream'` przy wywołaniu funkcji w `main`, przy argumencie. Przyczyna jest w nagłówku funkcji, gdzie brakuje `&`; wskazuje go notatka `note:`.
5. Bo odczyt zmienia strumień: zabiera z niego znaki i może zmienić jego stan. Z `const` kompilator nie pozwoliłby na `input >> boxes`.
6. Bo to `main` wie, skąd mają pochodzić dane, i to on ma sprawdzić, czy plik się otworzył. Funkcja otwierająca `shipments.txt` przy każdym wywołaniu czytałaby zawsze od pierwszej linii pliku i nie działałaby ze `std::cin` ani z innym plikiem.
7. Gdy liczba się odczytała, ale jest niedozwolona, na przykład `-2` paczki albo `13` egzemplarzy. Rekord wynikowy jest wtedy taki jak przed wywołaniem, bo funkcja przypisuje go dopiero po wszystkich sprawdzeniach. Komunikat wybiera `main`: po `false` sprawdza `fail()` strumienia i wypisuje `Input error` albo `Invalid ...`.
8. W pierwszym pliku rekord się zaczął, ale brakuje jego liczby, więc odczyt w funkcji się nie udaje: `Input error`. W drugim liczba jest kompletna: `>>` ją odczytuje, a nie udaje się dopiero dokończenie linii, co oznacza tylko, że nie ma już następnej nazwy. Program wypisuje raport.
9. Raport tylko z przesyłkami sprzed pustej linii, bez żadnego komunikatu. To nie jest błąd programu, tylko granica jego kontraktu: pusta linia w miejscu nazwy kończy dane, a między przesyłkami nie wolno jej zostawiać. Jeśli plik miał zawierać więcej przesyłek, raport jest jednak niekompletny.
10. Bo działa poprawnie tylko dla danych zgodnych z kontraktem tej lekcji. Nie odróżnia pustej linii w środku pliku od zakończenia danych, nie sprawdza tekstu po liczbie w jej linii i przy błędzie nie mówi, w którym miejscu pliku on jest.

</details>

## Podsumowanie

- Funkcja z parametrem `std::istream&` czyta z każdego strumienia wejścia: ze `std::cin` i z otwartego `std::ifstream`. Żeby przejść z klawiatury na plik, zmieniasz tylko kod wywołujący.
- `main` wybiera źródło, otwiera plik i sprawdza otwarcie, odczytuje nazwy, rozpoznaje zakończenie danych, buduje wektor i wypisuje wynik. Funkcja odczytuje i sprawdza wartości jednego rekordu, niczego nie otwiera i niczego nie wypisuje.
- Strumień przekazujesz przez referencję bez `const`. Strumienia nie wolno kopiować (`call to deleted constructor of 'std::istream'`), a odczyt go zmienia.
- Te same dane dają ten sam wynik z klawiatury i z pliku. W pliku dane kończy zwykle koniec pliku, także wtedy, gdy po ostatniej liczbie nie ma końca linii.
- Kontrakt określa, dla jakich danych program działa poprawnie. Od niego zależy też, co znaczy pusty plik: tutaj to lista bez przesyłek.
- Pusta linia w środku pliku po cichu kończy odczyt. To granica kontraktu przejętego z klawiatury, a nie odczytanie wszystkich rekordów.

## Co dalej

Program z tej lekcji ufa formatowi pliku: pusta linia kończy odczyt, a przy błędzie nie wiadomo, w którym miejscu pliku on jest. Kolejna lekcja Modułu 12 zajmie się dokładniejszym rozpoznawaniem, gdzie kończą się dane w pliku i gdzie jest błąd. Jest w przygotowaniu.

---

## Przykładowe rozwiązania

Zajrzyj tutaj **po własnej próbie**. Twoje nazwy mogą się różnić, jeśli standardowe wyjście jest takie, jak wymagane.

<details>
<summary>Punkt 8: misja, wypożyczenia w bibliotece szkolnej</summary>

**`main.cpp`**:

<!-- example: loans -->
```cpp
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

struct Loan {
    std::string title;
    int copies;
};

bool read_loan_values(std::istream& input, const std::string& title, Loan& result) {
    int copies{0};
    input >> copies;

    if (input.fail()) {
        return false;
    }

    if (copies < 0 || copies > 12) {
        return false;
    }

    result = Loan{title, copies};
    return true;
}

int main() {
    std::ifstream loans_file{"loans.txt"};

    if (loans_file.fail()) {
        std::cout << "Cannot open loans.txt\n";
        return 0;
    }

    std::vector<Loan> loans{};
    std::string title{};
    std::getline(loans_file, title);

    while (!loans_file.fail() && !title.empty()) {
        Loan loan{"", 0};
        const bool accepted{read_loan_values(loans_file, title, loan)};

        if (!accepted) {
            if (loans_file.fail()) {
                std::cout << "Input error\n";
            } else {
                std::cout << "Invalid loans\n";
            }

            return 0;
        }

        loans.push_back(loan);

        std::string rest{};
        std::getline(loans_file, rest);

        if (!loans_file.fail()) {
            std::getline(loans_file, title);
        }
    }

    int total_copies{0};
    std::cout << "Loans: " << loans.size() << "\n";

    for (const Loan& loan : loans) {
        std::cout << loan.title << ": " << loan.copies << "\n";
        total_copies += loan.copies;
    }

    std::cout << "Total copies: " << total_copies << "\n";
}
```

**`CMakeLists.txt`**: taki jak w oryginalnym `lesson_05_first_program`, bez zmian. `loans.txt` nie jest w `add_executable`.

**`loans.txt`** z danymi A, w katalogu `library_loans`, obok `main.cpp` i `CMakeLists.txt`:

<!-- run: loans -->

<!-- datafile: loans loans.txt -->
```text
Science Atlas
2
History Notes
3
```

<!-- output: loans -->
```text
Loans: 2
Science Atlas: 2
History Notes: 3
Total copies: 5
```

- **Uruchomienie:** pole **Working directory** konfiguracji `first_program` wskazuje katalog `library_loans`, ten z `loans.txt`. W terminalu program uruchamiasz z katalogu `library_loans`.
- **Funkcja odczytu:** `read_loan_values` dostaje strumień przez `std::istream&`, jak po poprawce z punktu 7, tytuł przez `const std::string&` i rekord przez `Loan&`. Odczytuje liczbę do zmiennej lokalnej `copies`, sprawdza `fail()`, potem zakres od 0 do 12, i dopiero wtedy przypisuje cały rekord. Niczego nie wypisuje i nie wie, że czyta z pliku.
- **`main`:** otwiera `loans.txt` i sprawdza otwarcie, a potem robi to samo co `main` z punktu 3: odczytuje tytuły, kończy pętlę na końcu pliku albo pustej linii, po odmowie wybiera komunikat przez `loans_file.fail()`, dokańcza linię liczbową i dopiero wtedy odczytuje następny tytuł.
- **Zmienna strumienia** nazywa się tu `loans_file`, a parametr funkcji `input`. Nazwy mogą być różne, bo parametr i tak jest inną nazwą przekazanego strumienia.
- **Inne poprawne rozwiązania:** zakres zapisany jako stałe `const int`, warunek zakresu rozbity na dwa `if`, flaga `bool` zamiast `return 0;` w pętli, jak w lekcji 7.4.

| Przypadek | Plik `loans.txt` | Standardowe wyjście |
|---|---|---|
| A | `Science Atlas`, `2`, `History Notes`, `3` | 2 wpisy, `Total copies: 5` |
| B | pusty plik | `Loans: 0`, `Total copies: 0` |
| C | brak pliku | `Cannot open loans.txt` |
| D | `Science Atlas`, `2`, `History Notes`, `seven` | `Input error` |
| E | `Science Atlas`, `2`, `History Notes`, `-1` | `Invalid loans` |
| F | `Science Atlas`, `2`, `History Notes` | `Input error` |
| G | `Science Atlas`, `2`, pusta linia | 1 wpis, `Total copies: 2` |
| H | `Science Atlas`, `2`, pusta linia, `History Notes`, `3` | 1 wpis, `Total copies: 2` |
| I | dane A bez końca linii po `3` | 2 wpisy, `Total copies: 5` |
| J | `Science Atlas`, `2`, `Science Atlas`, `4` | 2 wpisy, `Total copies: 6` |

Pozostałe przypadki kontrolne, sprawdzane automatycznie:

**K: jeden wpis.**

<!-- run: loans -->

<!-- datafile: loans loans.txt -->
```text
Poetry for Kids
1
```

<!-- output: loans -->
```text
Loans: 1
Poetry for Kids: 1
Total copies: 1
```

**L: obie granice zakresu,** 0 i 12.

<!-- run: loans -->

<!-- datafile: loans loans.txt -->
```text
Science Atlas
0
History Notes
12
```

<!-- output: loans -->
```text
Loans: 2
Science Atlas: 0
History Notes: 12
Total copies: 12
```

**M: 13 egzemplarzy,** o jeden za dużo.

<!-- run: loans -->

<!-- datafile: loans loans.txt -->
```text
Science Atlas
2
History Notes
13
```

<!-- output: loans -->
```text
Invalid loans
```

**N: największa możliwa suma,** pięć wpisów po 12 egzemplarzy.

<!-- run: loans -->

<!-- datafile: loans loans.txt -->
```text
Science Atlas
12
History Notes
12
Poetry for Kids
12
Space Facts
12
Animal Stories
12
```

<!-- output: loans -->
```text
Loans: 5
Science Atlas: 12
History Notes: 12
Poetry for Kids: 12
Space Facts: 12
Animal Stories: 12
Total copies: 60
```

**O: słowo zamiast liczby w pierwszym wpisie.**

<!-- run: loans -->

<!-- datafile: loans loans.txt -->
```text
Science Atlas
two
```

<!-- output: loans -->
```text
Input error
```

**P: sam tytuł, bez końca linii.** Plik kończy się zaraz po pierwszym tytule.

<!-- run: loans -->

<!-- datafile: loans loans.txt noeol -->
```text
Science Atlas
```

<!-- output: loans -->
```text
Input error
```

**Program kontrolny** sprawdza umowę funkcji przy odmowie, której w raporcie nie widać, bo po `false` program kończy pracę. Typ i funkcja są takie same jak wyżej, ale `main` czyta ze `std::cin`: ta sama funkcja działa bez zmian z klawiaturą. `main` przygotowuje rekord `Old Title` z liczbą 1, odczytuje jeden tytuł, wywołuje funkcję i wypisuje jej wynik oraz stan rekordu. Uruchamianie go jest nieobowiązkowe. Możesz w nim podmienić typ i funkcję na własne, jeśli zmienisz też nazwy w `main`.

<!-- example: loan_values_check -->
```cpp
#include <iostream>
#include <string>

struct Loan {
    std::string title;
    int copies;
};

bool read_loan_values(std::istream& input, const std::string& title, Loan& result) {
    int copies{0};
    input >> copies;

    if (input.fail()) {
        return false;
    }

    if (copies < 0 || copies > 12) {
        return false;
    }

    result = Loan{title, copies};
    return true;
}

int main() {
    Loan result{"Old Title", 1};
    std::string title{};
    std::getline(std::cin, title);

    const bool accepted{read_loan_values(std::cin, title, result)};

    if (accepted) {
        std::cout << "Returned: true\n";
    } else {
        std::cout << "Returned: false\n";
    }

    std::cout << "Result: " << result.title << ", " << result.copies << "\n";
}
```

Poprawna liczba zmienia rekord:

<!-- input: loan_values_check -->
```text
History Notes
3
```

<!-- output: loan_values_check -->
```text
Returned: true
Result: History Notes, 3
```

Po odmowie rekord zostaje bez zmian, także wtedy, gdy liczba się odczytała, ale jest spoza zakresu:

<!-- input: loan_values_check -->
```text
History Notes
seven
```

<!-- output: loan_values_check -->
```text
Returned: false
Result: Old Title, 1
```

<!-- input: loan_values_check -->
```text
History Notes
13
```

<!-- output: loan_values_check -->
```text
Returned: false
Result: Old Title, 1
```

<!-- input: loan_values_check -->
```text
History Notes
```

<!-- output: loan_values_check -->
```text
Returned: false
Result: Old Title, 1
```

</details>

**Poprzednia lekcja:** [Lekcja 12.1: Pierwszy plik z danymi](lesson_01_first_data_file.md) · **Następna lekcja:** w przygotowaniu · [Opis kursu](../../README.md)

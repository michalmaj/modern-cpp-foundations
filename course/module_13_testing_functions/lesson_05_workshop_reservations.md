# Lekcja 13.5: Rezerwacje na warsztaty (sprawdzian Modułu 13)

**Polski** · [English](lesson_05_workshop_reservations.en.md) · [Opis kursu](../../README.md)

> **Moduł 13, lekcja 5: sprawdzian** · około 110–135 minut, w dwóch podejściach
> **Potrzebujesz:** katalogu `cpp-workspace` i oryginalnego projektu `lesson_05_first_program`. Przyda się projekt z lekcji 13.4 jako przypomnienie dwóch targetów.
> **Wersja pilotażowa.** Rozwiązanie referencyjne i programy z diagnostyki sprawdzamy automatycznie na Windowsie, Ubuntu i macOS. Twojego projektu nic nie ocenia automatycznie: sprawdzasz go samodzielnie, według listy kontrolnej. Kroki w CLionie są takie jak w lekcji 13.4: opisujemy je według dokumentacji CLion 2026.3, bez ręcznego sprawdzenia na każdym systemie.

## Jak przebiega ten sprawdzian

Ta lekcja nie wprowadza niczego nowego. Sprawdzasz, czy potrafisz **samodzielnie zaplanować i napisać program testowy dla funkcji, której używa prawdziwy program**: dobrać przypadki na podstawie specyfikacji, sprawdzić wynik i parametr wyjściowy, wykryć błąd we wspólnej implementacji, naprawić go i uruchomić te same testy jeszcze raz. Łączysz w nim lekcje 13.1–13.4.

**Najważniejszy warunek:** Twój test musi wykazać niezgodność **przed** poprawką funkcji. Same `PASS` dla poprawionej funkcji nie wystarczą do zaliczenia: nie wiadomo wtedy, czy test w ogóle potrafi wykryć błąd.

Sprawdzian ma trzy części i omówienie:

- **Część A: plan.** Specyfikacja, przypadki i wyniki oczekiwane, zanim zobaczysz kod funkcji.
- **Część B: projekt i testowanie.** Projekt z dwoma targetami, program testowy, uruchomienie na dostarczonej funkcji, wykrycie błędu, poprawka i ponowne testy. To największa część pracy.
- **Część C: diagnostyka i uzasadnienie.** Zestaw testów, który przepuszcza naruszenie kontraktu, i pytania o Twoje decyzje. Wykonaj ją po części B.
- **Sprawdzenie i omówienie:** podpowiedzi, pełna lista przypadków, projekt do diagnostyki, rozwiązanie referencyjne, wyjaśnienia, odpowiedzi i samoocena. Przejdź tam dopiero po częściach A i B albo wtedy, gdy świadomie zrezygnujesz z dalszej samodzielnej próby.

Zajrzenie do podpowiedzi albo do wcześniejszych lekcji nie jest porażką. Ważne jest, żeby **uczciwie zanotować, co zrobiono samodzielnie, a co z pomocą**. Proponowany podział na dwa podejścia:

- **pierwsze:** specyfikacja, część A, projekt w CLionie, program właściwy, pierwsza wersja programu testowego i wykrycie usterki;
- **drugie:** uzupełnienie zestawu, poprawka, ponowne testy, część C, lista kontrolna i samoocena.

**Możesz używać:** CLiona albo terminala, CMake'a i Ninja, jak dotąd; `CMakeLists.txt` z oryginalnego `lesson_05_first_program` i wzoru dwóch targetów z lekcji 13.4; funkcji sprawdzających z lekcji 13.1–13.3; sposobu tworzenia `std::istringstream` z lekcji 13.3; zasad podziału na pliki z Modułu 11; swoich wcześniejszych tabel przypadków. Debugger nie jest potrzebny. Wszystko, czego potrzebujesz, znasz z Modułów 1–13.

Lekcje 13.1–13.4 traktuj jako przypomnienie zasad, a nie jako gotowy program do przepisania. Możesz świadomie przenieść fragmenty kodu, na przykład funkcje sprawdzające z lekcji 13.3 albo `CMakeLists.txt` z lekcji 13.4, ale plan, przypadki, wyniki oczekiwane i sposób wykazania błędu przygotuj samodzielnie. Jeśli adaptujesz wcześniejszy kod, zanotuj w samoocenie, skąd pochodzi, co przeniesiono, co zmieniono i jakie decyzje podjęto samodzielnie.

---

## Specyfikacja: rezerwacje na warsztaty

Organizator warsztatów zapisuje dla sali dwie liczby: jej **pojemność**, czyli liczbę wszystkich miejsc, i liczbę **zarezerwowanych** miejsc. Program odczytuje obie liczby i wypisuje, ile miejsc zostało wolnych. Nie modeluje uczestników, cen, dat, godzin, wielu sal ani kont.

Celem sprawdzianu nie jest samo wyliczenie wolnych miejsc. **Oceniasz umiejętność przetestowania funkcji, która przyjmuje dane.** Tę funkcję dostaniesz gotową w części B.

### Funkcja `read_workshop`

<!-- fragment -->
```cpp
struct Workshop {
    int capacity;
    int reserved;
};

bool read_workshop(std::istream& input, Workshop& result);
```

**Kontrakt:**

- Funkcja próbuje odczytać ze strumienia `input` dwie liczby typu `int`, operatorem `>>`: najpierw `capacity`, potem `reserved`. Liczby rozdzielają zwykłe białe znaki, na przykład spacja albo znak końca linii.
- **Reguły poprawności:** `1 <= capacity <= 30` oraz `0 <= reserved <= capacity`. Sala może więc mieć jedno miejsce albo trzydzieści, może nie mieć żadnej rezerwacji i może być zajęta w całości. Liczba rezerwacji nie może przekroczyć pojemności, a wartości ujemne są niepoprawne.
- **Sukces:** gdy obie liczby udało się odczytać i spełniają reguły, funkcja zapisuje je w `result` i zwraca `true`.
- **Odmowa:** gdy nie udało się odczytać obu liczb albo dane łamią reguły, funkcja zwraca `false` i **nie zmienia żadnego pola `result`**. Ta gwarancja jest częścią kontraktu.
- Ostatnia liczba nie musi mieć po sobie znaku końca linii: `"12 8"` i `"12 8\n"` są tak samo poprawne.
- Funkcja odczytuje dwie liczby, a nie cały dokument. Kontrakt nie mówi nic o znakach po drugiej liczbie ani o stanie strumienia po odmowie. Nie ma numerów linii ani osobnego parametru z opisem błędu.

### Program właściwy

`main` programu właściwego wywołuje `read_workshop` dla `std::cin`. Dla poprawnych danych wypisuje pojemność, liczbę rezerwacji i liczbę wolnych miejsc. Dla wejścia `12 8` wypisuje:

```text
Capacity: 12
Reserved: 8
Available: 4
```

Dla niepoprawnych danych wypisuje dokładnie `Invalid workshop data`. W obu sytuacjach kończy się kodem 0, jak programy z Modułów 10–12: odrzucenie złych danych to poprawne działanie tego programu.

### Wymagana struktura

```text
workshop_reservations/
├── CMakeLists.txt
├── main.cpp
├── function_tests.cpp
├── rules.cpp
└── rules.hpp
```

- **`rules.hpp`:** typ `Workshop` i deklaracja `read_workshop`, z `#pragma once`.
- **`rules.cpp`:** jedyna definicja `read_workshop`; dołącza `rules.hpp`.
- **`main.cpp`:** `main` programu właściwego; dołącza `rules.hpp` i nie zawiera kopii funkcji odczytu.
- **`function_tests.cpp`:** `main` programu testowego; dołącza `rules.hpp` i nie zawiera definicji `read_workshop`. Każdy przypadek ma **własny** `std::istringstream`, własny rekord i własne oczekiwania. Każde wywołanie sprawdza **wynik `bool`, pole `capacity` i pole `reserved`**: przy odmowie sprawdzenia pól potwierdzają, że rekord się nie zmienił. Program wypisuje `PASS` albo `FAIL` z wynikiem oczekiwanym i rzeczywistym, podsumowanie `Checks: N, failed: F` i kończy się kodem 0 albo 1, zależnie od niepowodzeń.
- **`CMakeLists.txt`:** dwa targety, `first_program` i `function_tests`, oba z `rules.cpp`, w postaci z lekcji 13.4: plik z lekcji 0.5, pusta linijka i te same trzy linijki dla `function_tests`. Nic więcej.
- Jedno sprawdzenie jednej własności to jedno sprawdzenie w podsumowaniu, jak w lekcji 13.3: jeden przypadek daje więc trzy sprawdzenia.
- Program testowy nie odczytuje niczego ze `std::cin` i nie potrzebuje żadnego pliku ani katalogu roboczego.

**Zdecyduj samodzielnie:**

1. które przypadki sprawdzisz i dlaczego;
2. jakich wyników oczekujesz w każdym z nich;
3. od jakiego rekordu zacznie każdy przypadek, żeby zmiana albo jej brak były widoczne;
4. jak nazwiesz sprawdzenia, żeby linijka `FAIL` mówiła, który przypadek i które pole zawiodło;
5. jakich funkcji sprawdzających użyjesz;
6. jak wykażesz, że Twój test wykrywa usterkę, zanim ją naprawisz;
7. jak potwierdzisz, że poprawka niczego nie zepsuła.

Przypomnienie znajdziesz w lekcjach [13.1](lesson_01_self_checking_program.md) (wynik oczekiwany, `PASS` i `FAIL`, kod zakończenia), [13.2](lesson_02_test_cases_that_catch_bugs.md) (dobór przypadków), [13.3](lesson_03_testing_input_without_a_file.md) (`std::istringstream`, rekord po odmowie) i [13.4](lesson_04_tests_next_to_the_program.md) (dwa targety, wspólny `rules.cpp`).

---

# Część A: plan

Zanim zobaczysz kod funkcji i zanim napiszesz jakikolwiek test, przygotuj na piśmie plan. Najważniejsza jego część to **tabela przypadków**. Lista samych nazw nie wystarczy: każdy wiersz podaje tekst strumienia, oczekiwany wynik `bool`, oczekiwany stan rekordu po wywołaniu i powód wyboru. Dwa wiersze jako wzór:

| Przypadek | Tekst strumienia | Wynik `bool` | Rekord po wywołaniu, start `{9, 4}` | Dlaczego |
|---|---|---|---|---|
| A | `"12 8"` | `true` | `{12, 8}` | zwykły poprawny przypadek |
| J | `"ten 3"` | `false` | `{9, 4}`, bez zmian | nieudany odczyt: tekst zamiast liczby |

Pozostałe wiersze wyprowadź samodzielnie ze specyfikacji. Zestaw musi obejmować co najmniej te kategorie:

- zwykły poprawny przypadek;
- dolną granicę pojemności;
- salę zajętą w całości;
- wartość poniżej dozwolonego zakresu;
- wartość powyżej dozwolonego zakresu;
- więcej rezerwacji niż miejsc;
- nieudany odczyt;
- niezmieniony rekord po każdej odmowie.

**Każda reguła osobno.** Reguły poprawności ze specyfikacji to cztery reguły liczbowe: `capacity >= 1`, `capacity <= 30`, `reserved >= 0` i `reserved <= capacity`. Dla każdej z nich zaplanuj co najmniej jeden przypadek odmowy, w którym obie liczby dają się odczytać, ta reguła jest naruszona, a pozostałe trzy są spełnione. Dzięki temu sprawdzisz każdą kontrolę osobno, jak w lekcji 13.2. Przypadek, który narusza kilka reguł naraz, nie zastępuje tych sprawdzeń: gdyby funkcja pomijała jedną z nich, odmowę i tak mogłaby spowodować inna reguła, a błąd pozostałby ukryty. Nieudany odczyt to osobna kategoria: nie ma w nim dwóch odczytanych liczb, więc ta zasada go nie dotyczy.

Nie musisz mieć wielu przypadków. Liczy się to, czy każdy z nich może wykryć inną pomyłkę.

**Odpowiedz w planie na dziesięć pytań:**

1. Jakie są poprawne zakresy obu pól?
2. Czy sala może mieć zero miejsc?
3. Czy może mieć zero rezerwacji?
4. Czy wszystkie miejsca mogą być zajęte?
5. Który przypadek sprawdza górną granicę pojemności?
6. Który przypadek sprawdza zbyt dużą liczbę rezerwacji?
7. Co powinno się stać, gdy brakuje drugiej liczby?
8. Co powinno się stać, gdy zamiast liczby stoi tekst?
9. Co powinno się stać z `result` po `false`?
10. Jak sprawdzisz, że testowana funkcja jest rzeczywiście wspólna dla obu programów?

**Odpowiedz też krótko:**

1. Dlaczego wyniki oczekiwane zapisujesz przed uruchomieniem testów, a nie po?
2. Dlaczego rekord startowy ma inne wartości niż rekordy oczekiwane przy sukcesie?
3. Dlaczego każdy przypadek dostaje własny strumień?
4. Dlaczego warto sprawdzić każdą granicę z obu stron?

Plan jest obowiązkową częścią sprawdzianu i jest oceniany razem z programem testowym. Nie poprawiaj niczego w funkcji, zanim plan nie będzie gotowy.

---

# Część B: projekt i testowanie

## Kod startowy

W `cpp-workspace` utwórz katalog `workshop_reservations` i skopiuj do niego `CMakeLists.txt` z oryginalnego `lesson_05_first_program`. Utwórz obok pliki z wymaganej struktury, tak jak w lekcji 13.4. Te dwa dostajesz gotowe:

**`rules.hpp`**:

<!-- file: workshop_m1 rules.hpp -->
```cpp
#pragma once

#include <istream>

struct Workshop {
    int capacity;
    int reserved;
};

bool read_workshop(std::istream& input, Workshop& result);
```

`<istream>` deklaruje `std::istream`: nagłówek jest samowystarczalny, jak w lekcji 11.3.

**`rules.cpp`**:

<!-- file: workshop_m1 rules.cpp -->
```cpp
#include "rules.hpp"

bool read_workshop(std::istream& input, Workshop& result) {
    int capacity{0};
    int reserved{0};
    input >> capacity;
    input >> reserved;

    if (input.fail()) {
        return false;
    }

    if (capacity < 1 || capacity > 30) {
        return false;
    }

    if (reserved < 0 || reserved >= capacity) {
        return false;
    }

    result = Workshop{capacity, reserved};
    return true;
}
```

**Ta implementacja kompiluje się poprawnie, ale zawiera jedną nieujawnioną usterkę logiczną.** Nie szukaj jej czytaniem kodu: znajdź ją swoim testem. `main.cpp`, `function_tests.cpp` i oba targety w `CMakeLists.txt` napiszesz samodzielnie.

## Kolejność pracy

1. **Program właściwy.** Napisz `main.cpp` według specyfikacji programu właściwego.
2. **Program testowy.** Napisz `function_tests.cpp` według swojego planu z części A. **Nie zmieniaj `rules.cpp`.**
3. **Dwa targety.** Zmień `CMakeLists.txt` tak, jak w lekcji 13.4. CMake szuka wszystkich plików z obu list już przy wczytywaniu projektu, dlatego `function_tests.cpp` musi istnieć wcześniej. Wczytaj projekt ponownie i wybierz **Build | Build Project**.
4. **To pierwsze obowiązkowe uruchomienie:** uruchom `first_program`, wpisz w oknie **Run** `12 8` i naciśnij **Enter**. Program powinien wypisać trzy linijki ze specyfikacji i zakończyć się kodem 0.
5. **To drugie obowiązkowe uruchomienie:** uruchom `function_tests`. Przy dostarczonej funkcji co najmniej jedno sprawdzenie powinno dać `FAIL`, a program testowy powinien zakończyć się kodem 1. Zapisz, które przypadki i które sprawdzenia się nie udały, z wynikami oczekiwanymi i rzeczywistymi, i jaki był kod zakończenia. To jest dowód, że Twój test wykrywa usterkę.
6. Jeśli wszystkie sprawdzenia dały `PASS`, Twój zestaw nie wykrywa usterki tej funkcji. Wróć do planu i do listy kategorii, uzupełnij przypadki i uruchom testy jeszcze raz. Nie zmieniaj jeszcze `rules.cpp`.
7. **Znajdź przyczynę.** Na podstawie linijek `FAIL` i kontraktu wskaż w `rules.cpp` warunek, który działa inaczej, niż mówi specyfikacja. Zapisz, czy błąd jest w funkcji, czy w wyniku oczekiwanym, i skąd to wiesz.
8. **Popraw tylko `rules.cpp`.** Nie zmieniaj danych testowych, wyników oczekiwanych, `main.cpp`, `function_tests.cpp` ani `CMakeLists.txt`.
9. **To trzecie obowiązkowe uruchomienie:** wybierz **Build Project** i uruchom `function_tests` jeszcze raz. Wszystkie sprawdzenia powinny dać `PASS`, a kod zakończenia powinien wynosić 0. Samo ponowne zbudowanie bez uruchomienia testów nie potwierdza poprawki.

---

# Część C: diagnostyka i uzasadnienie

Wykonaj tę część **po części B**.

## Diagnostyka: test przechodzi, choć funkcja łamie kontrakt

Ktoś inny też poprawił usterkę z części B, ale przy okazji przestawił jedną linię: jego `read_workshop` zapisuje odczytane liczby do `result` zaraz po udanym odczycie, a zakresy sprawdza dopiero potem. Dla niepoprawnych liczb nadal zwraca `false`.

Ta osoba sprawdziła swoją funkcję programem testowym z dwoma przypadkami: A, w którym sprawdza wynik i oba pola, oraz H, czyli `"10 11"` z rekordem startowym `{9, 4}`, w którym sprawdza **tylko** wynik `bool`. Wszystkie sprawdzenia przeszły, a program testowy zakończył się kodem 0.

**Przygotowanie:** w `cpp-workspace` utwórz katalog `workshop_diagnostics` i skopiuj do niego pięć plików z `workshop_reservations`, bez katalogu budowania. W kopii zastąp `rules.cpp` i `function_tests.cpp` plikami z części [Projekt do diagnostyki](#projekt-do-diagnostyki) w omówieniu. Pozostałe pliki zostają Twoje. Otwórz nowy katalog w CLionie, jak nowy projekt.

1. **Przewidź:** co dla przypadku H zwraca ta funkcja i jakie pola ma po wywołaniu rekord? Dlaczego sprawdzenie `accepted == false` tego nie widzi?
2. Wypisz wymagania kontraktu, których ten program testowy nie sprawdza.
3. Zaprojektuj brakujące sprawdzenia dla przypadku H: jakie wartości są oczekiwane i skąd je bierzesz?
4. **To czwarte obowiązkowe uruchomienie:** wybierz **Build Project** i uruchom `function_tests` bez zmian: zapisz wynik i kod zakończenia. Potem dopisz swoje sprawdzenia dla H, uruchom program jeszcze raz i zapisz linijki `FAIL` i kod zakończenia.
5. Wyjaśnij, czy błąd jest w funkcji, czy w wynikach oczekiwanych.
6. Zaproponuj najmniejszą poprawkę funkcji i wprowadź ją w `rules.cpp` kopii.
7. **To piąte obowiązkowe uruchomienie:** uruchom swój wzmocniony program testowy. Potem skopiuj do `workshop_diagnostics` swój `function_tests.cpp` z części B i uruchom go: wszystkie sprawdzenia powinny dać `PASS`, z kodem 0.
8. Wyjaśnij, dlaczego po tej poprawce trzeba uruchomić jeszcze raz także wszystkie wcześniejsze testy, a nie tylko te dla przypadku H.

## Uzasadnienie

Odpowiedz własnymi słowami, odnosząc się do swojego programu testowego:

1. Dlaczego wynik oczekiwany musi wynikać ze specyfikacji?
2. Dlaczego same przypadki typowe nie wystarczają?
3. Dlaczego sala zajęta w całości jest ważnym przypadkiem?
4. Co mówi `FAIL`, a czego nie rozstrzyga?
5. Dlaczego sprawdzasz także pola rekordu, a nie tylko wynik `bool`?
6. Dlaczego `std::istringstream` jest wygodny w testach?
7. Dlaczego każdy przypadek ma własny strumień?
8. Dlaczego oba targety korzystają z `rules.cpp`?
9. Dlaczego kod 1 programu testowego może być oczekiwanym wynikiem?
10. Co powinno się stać po poprawieniu wykrytej usterki?

---

## Lista kontrolna przed oddaniem

Sprawdzian jest zaliczony, gdy spełniasz **wszystkie** punkty tej listy. Twoje nazwy, funkcje pomocnicze i liczba przypadków mogą być inne niż w rozwiązaniu referencyjnym, jeśli spełniają specyfikację. Poprawny wynik programu właściwego dla `12 8`, samo zbudowanie projektu ani same `PASS` po poprawce nie wystarczą.

- [ ] Plan przypadków z części A powstał przed poprawianiem funkcji i zawiera dane, wynik `bool`, stan rekordu i uzasadnienie.
- [ ] Wyniki oczekiwane wynikają ze specyfikacji, a nie z działania funkcji.
- [ ] Projekt ma dwa targety CMake, `first_program` i `function_tests`, w postaci z lekcji 13.4.
- [ ] Oba targety korzystają z tej samej implementacji: `rules.cpp` stoi na obu listach, a `rules.hpp` dołączają `main.cpp` i `function_tests.cpp`.
- [ ] Definicja `read_workshop` jest tylko w `rules.cpp`, bez kopii w programie testowym.
- [ ] Program testowy podaje dane przez `std::istringstream`.
- [ ] Każdy niezależny przypadek ma własny strumień i własny rekord.
- [ ] Testy sprawdzają wynik `bool` każdego wywołania.
- [ ] Testy sprawdzają oba pola `Workshop`, także po odmowie.
- [ ] Zestaw obejmuje poprawne granice, nieudany odczyt oraz, dla każdej z czterech reguł liczbowych, przypadek odmowy, w którym naruszona jest tylko ta reguła.
- [ ] Usterka dostarczonej funkcji została wykryta testem przed poprawką `rules.cpp`.
- [ ] Program testowy po `FAIL` rzeczywiście zakończył się kodem 1.
- [ ] Po poprawce te same testy, z tymi samymi wynikami oczekiwanymi, przechodzą z kodem 0.
- [ ] Diagnostyka z części C jest wykonana, pytania z uzasadnienia mają odpowiedzi, a samoocena jest wypełniona.

Gdy skończysz, możesz zapisać projekt `workshop_reservations` w Gicie, jak w lekcji 1.5: pięć plików, bez katalogu budowania.

## Kryteria oceny

Rubryka służy do samooceny albo do oceny przez prowadzącego. Kurs nie ma skali ocen ani progu punktowego: punkty pokazują, które obszary są opanowane, a które wymagają powtórki. O zaliczeniu decyduje lista kontrolna powyżej, a nie liczba punktów.

| Obszar | Punkty | Pełne punkty, gdy |
|---|---:|---|
| Plan i uzasadnienie przypadków | 10 | plan powstał przed poprawką, ma dla każdego przypadku dane, wynik `bool`, stan rekordu i powód, a odpowiedzi na pytania z części A są poprawne |
| Organizacja projektu i dwa targety | 20 | pięć plików ma role ze specyfikacji, `CMakeLists.txt` ma dwa targety w postaci z lekcji 13.4, `rules.cpp` stoi na obu listach, definicja `read_workshop` jest tylko w nim, a program właściwy dla `12 8` daje wynik ze specyfikacji |
| Dobór przypadków i wyniki oczekiwane | 20 | zestaw obejmuje wszystkie wymagane kategorie, a dla każdej z czterech reguł liczbowych przypadek odmowy, w którym naruszona jest tylko ta reguła; każdy przypadek ma powód, a wszystkie wyniki oczekiwane zgadzają się ze specyfikacją |
| Testy ze `std::istringstream` i kontrola całego wyniku | 20 | każdy przypadek ma własny strumień i rekord, każde wywołanie sprawdza wynik i oba pola, a przy odmowie sprawdzenia pól potwierdzają niezmieniony rekord |
| Wykrycie usterki, poprawka i ponowne testy | 20 | `FAIL` i kod 1 pojawiły się przed poprawką, przyczyna jest wskazana w `rules.cpp`, poprawka zmienia tylko ten plik, a te same testy przechodzą potem z kodem 0 |
| Diagnostyka, uzasadnienia i samoocena | 10 | słaby test jest wyjaśniony i wzmocniony, poprawka sprawdzona pełnym zestawem, odpowiedzi odnoszą się do Twojego projektu, a samoocena uczciwie opisuje adaptowany kod |
| **Razem** | **100** | |

- **Błędne wyniki oczekiwane** odbierają pełne punkty za dobór przypadków, nawet gdy przypadków jest dużo.
- **`FAIL` przy kodzie zakończenia 0** nie daje pełnych punktów za wykrycie usterki: każdy, kto czyta tylko kod zakończenia, uzna testy za udane.
- **Kopia `read_workshop` w `function_tests.cpp`** nie daje pełnych punktów za organizację projektu, nawet gdy oba targety są zdefiniowane.
- **Inne nazwy** zmiennych, sprawdzeń i funkcji pomocniczych nie odbierają punktów. Nazwy targetów i plików z `main` są jednak stałe: wynikają ze specyfikacji projektu.

**Co sprawdza automat, a co nie.** Testy kursu sprawdzają, że rozwiązanie referencyjne i programy z diagnostyki się budują, że programy testowe dają pokazane wyniki i kody zakończenia oraz że program właściwy wypisuje to, co w specyfikacji. **Twojego projektu, planu, testów i uzasadnienia nie sprawdza żaden automat:** ocenia je człowiek, czytając plan i kod oraz porównując Twoje uruchomienia z listą kontrolną.

---

# Sprawdzenie i omówienie

Przejdź tutaj **dopiero po częściach A i B** albo wtedy, gdy świadomie zrezygnujesz z dalszej samodzielnej próby. Dalej jest kod rozwiązania.

## Podpowiedzi

<details>
<summary>Podpowiedź 1: plan przypadków</summary>

Każda liczba w regułach jest granicą: 1 i 30 dla pojemności, 0 i `capacity` dla rezerwacji. Dla każdej z nich wybierz wartość dokładnie na granicy i tuż za nią. Zapytaj też: czy sala, w której zarezerwowano wszystkie miejsca, jest poprawna według specyfikacji? Wynik zapisz, zanim uruchomisz cokolwiek.

</details>

<details>
<summary>Podpowiedź 2: testowanie funkcji</summary>

Funkcja daje trzy rzeczy do sprawdzenia: wynik `bool` i dwa pola rekordu. Każdy przypadek potrzebuje własnego `std::istringstream` z własnym tekstem i własnego rekordu startowego. Jeśli rekord startowy ma wartości, których żaden poprawny odczyt by nie dał, każda zmiana pola przy odmowie będzie widoczna w linijce `FAIL`.

</details>

<details>
<summary>Podpowiedź 3: wspólna implementacja i regresja</summary>

Gdzie jest jedyna definicja funkcji, której używają oba programy? Tam wprowadzasz poprawkę, a program testowy i wyniki oczekiwane zostają bez zmian, bo kontrakt się nie zmienił. Po poprawce zbuduj oba programy, **Build Project**, i uruchom te same testy jeszcze raz.

</details>

## Pełna lista przypadków kontrolnych

<details>
<summary>Przypadki A–N, wyniki ze specyfikacji</summary>

Każdy przypadek zaczyna od rekordu `{9, 4}`: takich wartości nie daje żaden przypadek z poprawnymi danymi, więc każda zmiana rekordu przy odmowie jest widoczna. Rozwiązanie referencyjne sprawdza przypadki A–J. K–N to dodatkowe przypadki z tej samej specyfikacji.

| Przypadek | Tekst strumienia | Wynik `bool` | Rekord po wywołaniu | Dlaczego |
|---|---|---|---|---|
| A | `"12 8"` | `true` | `{12, 8}` | zwykły poprawny przypadek |
| B | `"1 0"` | `true` | `{1, 0}` | dolna granica pojemności i zero rezerwacji |
| C | `"10 10"` | `true` | `{10, 10}` | sala zajęta w całości |
| D | `"30 30"` | `true` | `{30, 30}` | górna granica pojemności, zajęta w całości |
| E | `"0 0"` | `false` | `{9, 4}`, bez zmian | pojemność poniżej zakresu |
| F | `"31 0"` | `false` | `{9, 4}`, bez zmian | pojemność powyżej zakresu |
| G | `"10 -1"` | `false` | `{9, 4}`, bez zmian | rezerwacje poniżej zakresu |
| H | `"10 11"` | `false` | `{9, 4}`, bez zmian | więcej rezerwacji niż miejsc |
| I | `"10"` | `false` | `{9, 4}`, bez zmian | brak drugiej liczby |
| J | `"ten 3"` | `false` | `{9, 4}`, bez zmian | tekst zamiast liczby |
| K | `""` | `false` | `{9, 4}`, bez zmian | pusty tekst |
| L | `"30 0"` | `true` | `{30, 0}` | górna granica pojemności, zero rezerwacji |
| M | `"12 8\n"` | `true` | `{12, 8}` | znak końca linii po ostatniej liczbie |
| N | `"10 10\n"` | `true` | `{10, 10}` | sala zajęta w całości, ze znakiem końca linii |

</details>

## Projekt do diagnostyki

<details>
<summary>Pliki do części C: otwórz po części B</summary>

**`rules.cpp`** z przestawioną linią:

<!-- file: workshop_weak rules.cpp -->
```cpp
#include "rules.hpp"

bool read_workshop(std::istream& input, Workshop& result) {
    int capacity{0};
    int reserved{0};
    input >> capacity;
    input >> reserved;

    if (input.fail()) {
        return false;
    }

    result = Workshop{capacity, reserved};

    if (capacity < 1 || capacity > 30) {
        return false;
    }

    if (reserved < 0 || reserved > capacity) {
        return false;
    }

    return true;
}
```

**`function_tests.cpp`**, słaby program testowy:

<!-- file: workshop_weak function_tests.cpp -->
```cpp
#include <iostream>
#include <sstream>
#include <string>

#include "rules.hpp"

std::string bool_text(bool value) {
    if (value) {
        return "true";
    }

    return "false";
}

void check_bool(const std::string& name, bool expected, bool actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << bool_text(expected) << ", actual " << bool_text(actual) << "\n";
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

    std::istringstream input_a{"12 8"};
    Workshop workshop_a{9, 4};
    const bool accepted_a{read_workshop(input_a, workshop_a)};
    check_bool("A accepted", true, accepted_a, checks, failed);
    check_int("A capacity", 12, workshop_a.capacity, checks, failed);
    check_int("A reserved", 8, workshop_a.reserved, checks, failed);

    std::istringstream input_h{"10 11"};
    Workshop workshop_h{9, 4};
    const bool accepted_h{read_workshop(input_h, workshop_h)};
    check_bool("H accepted", false, accepted_h, checks, failed);

    std::cout << "Checks: " << checks << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

<details>
<summary>Pozostałe pliki tego projektu, takie jak w rozwiązaniu referencyjnym</summary>

**`main.cpp`**:

<!-- example: workshop_weak target=function_tests -->
```cpp
#include <iostream>

#include "rules.hpp"

int main() {
    Workshop workshop{0, 0};

    if (!read_workshop(std::cin, workshop)) {
        std::cout << "Invalid workshop data\n";
        return 0;
    }

    std::cout << "Capacity: " << workshop.capacity << "\n";
    std::cout << "Reserved: " << workshop.reserved << "\n";
    std::cout << "Available: " << workshop.capacity - workshop.reserved << "\n";
}
```

**`rules.hpp`**:

<!-- file: workshop_weak rules.hpp -->
```cpp
#pragma once

#include <istream>

struct Workshop {
    int capacity;
    int reserved;
};

bool read_workshop(std::istream& input, Workshop& result);
```

**`CMakeLists.txt`**:

<!-- cmake: workshop_weak -->
```cmake
cmake_minimum_required(VERSION 3.28)
project(first_program LANGUAGES CXX)

add_executable(first_program main.cpp rules.cpp)
target_compile_features(first_program PRIVATE cxx_std_20)
set_target_properties(first_program PROPERTIES CXX_EXTENSIONS OFF)

add_executable(function_tests function_tests.cpp rules.cpp)
target_compile_features(function_tests PRIVATE cxx_std_20)
set_target_properties(function_tests PROPERTIES CXX_EXTENSIONS OFF)
```

</details>

</details>

## Rozwiązanie referencyjne

<details>
<summary>Plan i projekt rozwiązania referencyjnego</summary>

To jedno z poprawnych rozwiązań, a nie jedyna dopuszczalna postać.

**Plan, w skrócie:**

1. `capacity` od 1 do 30, `reserved` od 0 do `capacity`.
2. Nie: pojemność 0 jest poniżej zakresu (E).
3. Tak: zero rezerwacji jest poprawne (B, L).
4. Tak: `reserved` może być równe `capacity` (C, D).
5. D (`30 30`) i L (`30 0`) z jednej strony, F (`31 0`) z drugiej.
6. H (`10 11`): o jedną rezerwację za dużo.
7. I (`"10"`): odczyt drugiej liczby się nie udaje, więc `false` i rekord bez zmian.
8. J (`"ten 3"`): odczyt pierwszej liczby się nie udaje, więc `false` i rekord bez zmian.
9. Nic: wszystkie pola mają wartości sprzed wywołania.
10. Definicja jest tylko w `rules.cpp`, a ten plik stoi na listach obu targetów. Celowa usterka w `rules.cpp` zmienia wyniki testów, a ta sama funkcja daje programowi właściwemu wynik ze specyfikacji.

Krótkie odpowiedzi: wynik oczekiwany zapisany po uruchomieniu powtórzyłby działanie funkcji, także błędne; rekord startowy `{9, 4}` odróżnia „funkcja zapisała pola” od „pola zostały takie jak były”; osobny strumień sprawia, że żaden przypadek nie zaczyna od danych zużytych przez poprzedni (lekcja 13.3); granica sprawdzona tylko z jednej strony nie pokaże, czy przesunięto ją o jeden.

**`main.cpp`**:

<!-- example: workshop_m1 target=function_tests exit=1 -->
```cpp
#include <iostream>

#include "rules.hpp"

int main() {
    Workshop workshop{0, 0};

    if (!read_workshop(std::cin, workshop)) {
        std::cout << "Invalid workshop data\n";
        return 0;
    }

    std::cout << "Capacity: " << workshop.capacity << "\n";
    std::cout << "Reserved: " << workshop.reserved << "\n";
    std::cout << "Available: " << workshop.capacity - workshop.reserved << "\n";
}
```

**`function_tests.cpp`**, przypadki A–J:

<!-- file: workshop_m1 function_tests.cpp -->
```cpp
#include <iostream>
#include <sstream>
#include <string>

#include "rules.hpp"

std::string bool_text(bool value) {
    if (value) {
        return "true";
    }

    return "false";
}

void check_bool(const std::string& name, bool expected, bool actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << bool_text(expected) << ", actual " << bool_text(actual) << "\n";
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

    std::istringstream input_a{"12 8"};
    Workshop workshop_a{9, 4};
    const bool accepted_a{read_workshop(input_a, workshop_a)};
    check_bool("A accepted", true, accepted_a, checks, failed);
    check_int("A capacity", 12, workshop_a.capacity, checks, failed);
    check_int("A reserved", 8, workshop_a.reserved, checks, failed);

    std::istringstream input_b{"1 0"};
    Workshop workshop_b{9, 4};
    const bool accepted_b{read_workshop(input_b, workshop_b)};
    check_bool("B accepted", true, accepted_b, checks, failed);
    check_int("B capacity", 1, workshop_b.capacity, checks, failed);
    check_int("B reserved", 0, workshop_b.reserved, checks, failed);

    std::istringstream input_c{"10 10"};
    Workshop workshop_c{9, 4};
    const bool accepted_c{read_workshop(input_c, workshop_c)};
    check_bool("C accepted", true, accepted_c, checks, failed);
    check_int("C capacity", 10, workshop_c.capacity, checks, failed);
    check_int("C reserved", 10, workshop_c.reserved, checks, failed);

    std::istringstream input_d{"30 30"};
    Workshop workshop_d{9, 4};
    const bool accepted_d{read_workshop(input_d, workshop_d)};
    check_bool("D accepted", true, accepted_d, checks, failed);
    check_int("D capacity", 30, workshop_d.capacity, checks, failed);
    check_int("D reserved", 30, workshop_d.reserved, checks, failed);

    std::istringstream input_e{"0 0"};
    Workshop workshop_e{9, 4};
    const bool accepted_e{read_workshop(input_e, workshop_e)};
    check_bool("E accepted", false, accepted_e, checks, failed);
    check_int("E capacity", 9, workshop_e.capacity, checks, failed);
    check_int("E reserved", 4, workshop_e.reserved, checks, failed);

    std::istringstream input_f{"31 0"};
    Workshop workshop_f{9, 4};
    const bool accepted_f{read_workshop(input_f, workshop_f)};
    check_bool("F accepted", false, accepted_f, checks, failed);
    check_int("F capacity", 9, workshop_f.capacity, checks, failed);
    check_int("F reserved", 4, workshop_f.reserved, checks, failed);

    std::istringstream input_g{"10 -1"};
    Workshop workshop_g{9, 4};
    const bool accepted_g{read_workshop(input_g, workshop_g)};
    check_bool("G accepted", false, accepted_g, checks, failed);
    check_int("G capacity", 9, workshop_g.capacity, checks, failed);
    check_int("G reserved", 4, workshop_g.reserved, checks, failed);

    std::istringstream input_h{"10 11"};
    Workshop workshop_h{9, 4};
    const bool accepted_h{read_workshop(input_h, workshop_h)};
    check_bool("H accepted", false, accepted_h, checks, failed);
    check_int("H capacity", 9, workshop_h.capacity, checks, failed);
    check_int("H reserved", 4, workshop_h.reserved, checks, failed);

    std::istringstream input_i{"10"};
    Workshop workshop_i{9, 4};
    const bool accepted_i{read_workshop(input_i, workshop_i)};
    check_bool("I accepted", false, accepted_i, checks, failed);
    check_int("I capacity", 9, workshop_i.capacity, checks, failed);
    check_int("I reserved", 4, workshop_i.reserved, checks, failed);

    std::istringstream input_j{"ten 3"};
    Workshop workshop_j{9, 4};
    const bool accepted_j{read_workshop(input_j, workshop_j)};
    check_bool("J accepted", false, accepted_j, checks, failed);
    check_int("J capacity", 9, workshop_j.capacity, checks, failed);
    check_int("J reserved", 4, workshop_j.reserved, checks, failed);

    std::cout << "Checks: " << checks << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

**`CMakeLists.txt`**:

<!-- cmake: workshop_m1 -->
```cmake
cmake_minimum_required(VERSION 3.28)
project(first_program LANGUAGES CXX)

add_executable(first_program main.cpp rules.cpp)
target_compile_features(first_program PRIVATE cxx_std_20)
set_target_properties(first_program PROPERTIES CXX_EXTENSIONS OFF)

add_executable(function_tests function_tests.cpp rules.cpp)
target_compile_features(function_tests PRIVATE cxx_std_20)
set_target_properties(function_tests PROPERTIES CXX_EXTENSIONS OFF)
```

`rules.hpp` i `rules.cpp` to kod startowy z części B.

**Przed poprawką**, z dostarczoną funkcją, `function_tests` wypisuje:

<!-- output: workshop_m1 -->
```text
PASS A accepted
PASS A capacity
PASS A reserved
PASS B accepted
PASS B capacity
PASS B reserved
FAIL C accepted: expected true, actual false
FAIL C capacity: expected 10, actual 9
FAIL C reserved: expected 10, actual 4
FAIL D accepted: expected true, actual false
FAIL D capacity: expected 30, actual 9
FAIL D reserved: expected 30, actual 4
PASS E accepted
PASS E capacity
PASS E reserved
PASS F accepted
PASS F capacity
PASS F reserved
PASS G accepted
PASS G capacity
PASS G reserved
PASS H accepted
PASS H capacity
PASS H reserved
PASS I accepted
PASS I capacity
PASS I reserved
PASS J accepted
PASS J capacity
PASS J reserved
Checks: 30, failed: 6
```

Kod zakończenia: 1. To **test wykrywający błąd**: program testowy działa poprawnie, a kod 1 wynika z sześciu nieudanych sprawdzeń.

- **Które przypadki:** C i D, oba z salą zajętą w całości. Funkcja zwraca `false`, więc rekord zostaje `{9, 4}`: nie zgadza się wynik i oba pola, czyli trzy sprawdzenia w każdym przypadku.
- **Przyczyna:** warunek `reserved >= capacity` odrzuca także `reserved == capacity`, a kontrakt na to pozwala. Błąd jest w funkcji, bo wyniki oczekiwane zgadzają się ze specyfikacją.
- **Dlaczego pozostałe przechodzą:** w A, B i przy odmowach E–J obie wersje warunku dają ten sam wynik. Program właściwy dla `12 8` też działa poprawnie: usterka nie dotyczy typowych danych.

**Poprawka:** w `rules.cpp` jedna zmiana, `reserved > capacity` zamiast `reserved >= capacity`. Program testowy, wyniki oczekiwane, `main.cpp` i `CMakeLists.txt` się nie zmieniają.

**Po poprawce** te same testy wypisują:

<!-- output: workshop_fixed -->
```text
PASS A accepted
PASS A capacity
PASS A reserved
PASS B accepted
PASS B capacity
PASS B reserved
PASS C accepted
PASS C capacity
PASS C reserved
PASS D accepted
PASS D capacity
PASS D reserved
PASS E accepted
PASS E capacity
PASS E reserved
PASS F accepted
PASS F capacity
PASS F reserved
PASS G accepted
PASS G capacity
PASS G reserved
PASS H accepted
PASS H capacity
PASS H reserved
PASS I accepted
PASS I capacity
PASS I reserved
PASS J accepted
PASS J capacity
PASS J reserved
Checks: 30, failed: 0
```

Kod zakończenia: 0. Przygotowany zestaw nie wykrył już żadnej niezgodności. Nie dowodzi to poprawności funkcji dla wszystkich danych.

<details>
<summary>Wszystkie pliki projektu po poprawce</summary>

Te same pliki co przed poprawką, poza jednym warunkiem w `rules.cpp`.

**`main.cpp`**:

<!-- example: workshop_fixed target=function_tests -->
```cpp
#include <iostream>

#include "rules.hpp"

int main() {
    Workshop workshop{0, 0};

    if (!read_workshop(std::cin, workshop)) {
        std::cout << "Invalid workshop data\n";
        return 0;
    }

    std::cout << "Capacity: " << workshop.capacity << "\n";
    std::cout << "Reserved: " << workshop.reserved << "\n";
    std::cout << "Available: " << workshop.capacity - workshop.reserved << "\n";
}
```

**`rules.hpp`**:

<!-- file: workshop_fixed rules.hpp -->
```cpp
#pragma once

#include <istream>

struct Workshop {
    int capacity;
    int reserved;
};

bool read_workshop(std::istream& input, Workshop& result);
```

**`rules.cpp`**, po poprawce:

<!-- file: workshop_fixed rules.cpp -->
```cpp
#include "rules.hpp"

bool read_workshop(std::istream& input, Workshop& result) {
    int capacity{0};
    int reserved{0};
    input >> capacity;
    input >> reserved;

    if (input.fail()) {
        return false;
    }

    if (capacity < 1 || capacity > 30) {
        return false;
    }

    if (reserved < 0 || reserved > capacity) {
        return false;
    }

    result = Workshop{capacity, reserved};
    return true;
}
```

**`function_tests.cpp`**, bez zmian:

<!-- file: workshop_fixed function_tests.cpp -->
```cpp
#include <iostream>
#include <sstream>
#include <string>

#include "rules.hpp"

std::string bool_text(bool value) {
    if (value) {
        return "true";
    }

    return "false";
}

void check_bool(const std::string& name, bool expected, bool actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << bool_text(expected) << ", actual " << bool_text(actual) << "\n";
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

    std::istringstream input_a{"12 8"};
    Workshop workshop_a{9, 4};
    const bool accepted_a{read_workshop(input_a, workshop_a)};
    check_bool("A accepted", true, accepted_a, checks, failed);
    check_int("A capacity", 12, workshop_a.capacity, checks, failed);
    check_int("A reserved", 8, workshop_a.reserved, checks, failed);

    std::istringstream input_b{"1 0"};
    Workshop workshop_b{9, 4};
    const bool accepted_b{read_workshop(input_b, workshop_b)};
    check_bool("B accepted", true, accepted_b, checks, failed);
    check_int("B capacity", 1, workshop_b.capacity, checks, failed);
    check_int("B reserved", 0, workshop_b.reserved, checks, failed);

    std::istringstream input_c{"10 10"};
    Workshop workshop_c{9, 4};
    const bool accepted_c{read_workshop(input_c, workshop_c)};
    check_bool("C accepted", true, accepted_c, checks, failed);
    check_int("C capacity", 10, workshop_c.capacity, checks, failed);
    check_int("C reserved", 10, workshop_c.reserved, checks, failed);

    std::istringstream input_d{"30 30"};
    Workshop workshop_d{9, 4};
    const bool accepted_d{read_workshop(input_d, workshop_d)};
    check_bool("D accepted", true, accepted_d, checks, failed);
    check_int("D capacity", 30, workshop_d.capacity, checks, failed);
    check_int("D reserved", 30, workshop_d.reserved, checks, failed);

    std::istringstream input_e{"0 0"};
    Workshop workshop_e{9, 4};
    const bool accepted_e{read_workshop(input_e, workshop_e)};
    check_bool("E accepted", false, accepted_e, checks, failed);
    check_int("E capacity", 9, workshop_e.capacity, checks, failed);
    check_int("E reserved", 4, workshop_e.reserved, checks, failed);

    std::istringstream input_f{"31 0"};
    Workshop workshop_f{9, 4};
    const bool accepted_f{read_workshop(input_f, workshop_f)};
    check_bool("F accepted", false, accepted_f, checks, failed);
    check_int("F capacity", 9, workshop_f.capacity, checks, failed);
    check_int("F reserved", 4, workshop_f.reserved, checks, failed);

    std::istringstream input_g{"10 -1"};
    Workshop workshop_g{9, 4};
    const bool accepted_g{read_workshop(input_g, workshop_g)};
    check_bool("G accepted", false, accepted_g, checks, failed);
    check_int("G capacity", 9, workshop_g.capacity, checks, failed);
    check_int("G reserved", 4, workshop_g.reserved, checks, failed);

    std::istringstream input_h{"10 11"};
    Workshop workshop_h{9, 4};
    const bool accepted_h{read_workshop(input_h, workshop_h)};
    check_bool("H accepted", false, accepted_h, checks, failed);
    check_int("H capacity", 9, workshop_h.capacity, checks, failed);
    check_int("H reserved", 4, workshop_h.reserved, checks, failed);

    std::istringstream input_i{"10"};
    Workshop workshop_i{9, 4};
    const bool accepted_i{read_workshop(input_i, workshop_i)};
    check_bool("I accepted", false, accepted_i, checks, failed);
    check_int("I capacity", 9, workshop_i.capacity, checks, failed);
    check_int("I reserved", 4, workshop_i.reserved, checks, failed);

    std::istringstream input_j{"ten 3"};
    Workshop workshop_j{9, 4};
    const bool accepted_j{read_workshop(input_j, workshop_j)};
    check_bool("J accepted", false, accepted_j, checks, failed);
    check_int("J capacity", 9, workshop_j.capacity, checks, failed);
    check_int("J reserved", 4, workshop_j.reserved, checks, failed);

    std::cout << "Checks: " << checks << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

**`CMakeLists.txt`**:

<!-- cmake: workshop_fixed -->
```cmake
cmake_minimum_required(VERSION 3.28)
project(first_program LANGUAGES CXX)

add_executable(first_program main.cpp rules.cpp)
target_compile_features(first_program PRIVATE cxx_std_20)
set_target_properties(first_program PROPERTIES CXX_EXTENSIONS OFF)

add_executable(function_tests function_tests.cpp rules.cpp)
target_compile_features(function_tests PRIVATE cxx_std_20)
set_target_properties(function_tests PROPERTIES CXX_EXTENSIONS OFF)
```

</details>

**Program właściwy, sprawdzony osobno.** W projekcie z dwoma targetami testy kursu uruchamiają tylko `function_tests`. Dlatego wyniki programu właściwego sprawdzamy osobno: te same `main.cpp`, `rules.hpp` i poprawiony `rules.cpp`, zbudowane jako jeden program i uruchomione z danymi z klawiatury. Tekst z klawiatury zawsze kończy się tu znakiem końca linii, a ostatnie dane to jedna pusta linia.

<details>
<summary>Program właściwy dla sześciu danych wejściowych</summary>

**`main.cpp`**:

<!-- example: workshop_program -->
```cpp
#include <iostream>

#include "rules.hpp"

int main() {
    Workshop workshop{0, 0};

    if (!read_workshop(std::cin, workshop)) {
        std::cout << "Invalid workshop data\n";
        return 0;
    }

    std::cout << "Capacity: " << workshop.capacity << "\n";
    std::cout << "Reserved: " << workshop.reserved << "\n";
    std::cout << "Available: " << workshop.capacity - workshop.reserved << "\n";
}
```

**`rules.hpp`**:

<!-- file: workshop_program rules.hpp -->
```cpp
#pragma once

#include <istream>

struct Workshop {
    int capacity;
    int reserved;
};

bool read_workshop(std::istream& input, Workshop& result);
```

**`rules.cpp`**:

<!-- file: workshop_program rules.cpp -->
```cpp
#include "rules.hpp"

bool read_workshop(std::istream& input, Workshop& result) {
    int capacity{0};
    int reserved{0};
    input >> capacity;
    input >> reserved;

    if (input.fail()) {
        return false;
    }

    if (capacity < 1 || capacity > 30) {
        return false;
    }

    if (reserved < 0 || reserved > capacity) {
        return false;
    }

    result = Workshop{capacity, reserved};
    return true;
}
```

**`CMakeLists.txt`**, jeden program:

<!-- cmake: workshop_program -->
```cmake
cmake_minimum_required(VERSION 3.28)
project(first_program LANGUAGES CXX)

add_executable(first_program main.cpp rules.cpp)
target_compile_features(first_program PRIVATE cxx_std_20)
set_target_properties(first_program PROPERTIES CXX_EXTENSIONS OFF)
```

<!-- input: workshop_program -->
```text
12 8
```

<!-- output: workshop_program -->
```text
Capacity: 12
Reserved: 8
Available: 4
```

<!-- input: workshop_program -->
```text
10 10
```

<!-- output: workshop_program -->
```text
Capacity: 10
Reserved: 10
Available: 0
```

<!-- input: workshop_program -->
```text
30 0
```

<!-- output: workshop_program -->
```text
Capacity: 30
Reserved: 0
Available: 30
```

<!-- input: workshop_program -->
```text
10 11
```

<!-- output: workshop_program -->
```text
Invalid workshop data
```

<!-- input: workshop_program -->
```text
ten 3
```

<!-- output: workshop_program -->
```text
Invalid workshop data
```

<!-- input: workshop_program -->
```text

```

<!-- output: workshop_program -->
```text
Invalid workshop data
```

</details>

</details>

## Diagnostyka: wyjaśnienie i poprawka

<details>
<summary>Otwórz po wykonaniu diagnostyki</summary>

**Słaby program testowy** z przestawioną linią wypisuje:

<!-- output: workshop_weak -->
```text
PASS A accepted
PASS A capacity
PASS A reserved
PASS H accepted
Checks: 4, failed: 0
```

Kod zakończenia: 0, choć funkcja łamie kontrakt.

1. **Dla H** funkcja odczytuje 10 i 11, zapisuje je do `result` i dopiero potem odrzuca dane, bo 11 > 10. Zwraca `false`, jak trzeba, ale rekord ma już pola `{10, 11}` zamiast `{9, 4}`. Sprawdzenie `accepted == false` widzi tylko wynik, a nie rekord.
2. **Niesprawdzone wymagania:** przy odmowie oba pola mają zostać bez zmian. Sprawdzić trzeba `capacity` i `reserved`.
3. **Brakujące sprawdzenia:** dla H oczekiwane są wartości startowe, 9 i 4, bo kontrakt mówi, że przy odmowie rekord się nie zmienia.
4. **Wzmocniony program testowy** to słaby program z dwoma dodatkowymi sprawdzeniami dla H. Z tą samą funkcją wypisuje:

<!-- output: workshop_strong -->
```text
PASS A accepted
PASS A capacity
PASS A reserved
PASS H accepted
FAIL H capacity: expected 9, actual 10
FAIL H reserved: expected 4, actual 11
Checks: 6, failed: 2
```

   Kod zakończenia: 1. Dwa nowe sprawdzenia wykryły zmianę rekordu.
5. **Błąd jest w funkcji:** wartości oczekiwane 9 i 4 wynikają wprost z kontraktu.
6. **Poprawka:** linia `result = Workshop{capacity, reserved};` wraca na koniec funkcji, po wszystkich sprawdzeniach, tuż przed `return true;`. Funkcja jest wtedy taka jak poprawiony `rules.cpp` z rozwiązania referencyjnego. Wzmocnione sprawdzenia przypadków A i H są dokładnie sprawdzeniami A i H z rozwiązania referencyjnego, więc z poprawioną funkcją przechodzą, jak cały zestaw A–J.
7. **Po poprawce** Twój pełny zestaw z części B przechodzi z kodem 0.
8. **Dlaczego wszystkie testy:** przestawienie linii mogło zepsuć coś, co wcześniej działało. Gdyby zapis rekordu wypadł z funkcji, poprawne przypadki A–D dałyby `FAIL` przy polach. Testy H tego nie pokażą.

**Wniosek:** test, który sprawdza tylko wynik `bool`, przepuszcza funkcję, która przy odmowie zmienia rekord. Pełny zestaw z rozwiązania referencyjnego, który przy każdej odmowie sprawdza oba pola, wykrywa tę usterkę w przypadkach E, F, G i H, bo w każdym z nich obie liczby dało się odczytać.

<details>
<summary>Wzmocniony program testowy, sprawdzony automatycznie</summary>

**`main.cpp`**:

<!-- example: workshop_strong target=function_tests exit=1 -->
```cpp
#include <iostream>

#include "rules.hpp"

int main() {
    Workshop workshop{0, 0};

    if (!read_workshop(std::cin, workshop)) {
        std::cout << "Invalid workshop data\n";
        return 0;
    }

    std::cout << "Capacity: " << workshop.capacity << "\n";
    std::cout << "Reserved: " << workshop.reserved << "\n";
    std::cout << "Available: " << workshop.capacity - workshop.reserved << "\n";
}
```

**`rules.hpp`**:

<!-- file: workshop_strong rules.hpp -->
```cpp
#pragma once

#include <istream>

struct Workshop {
    int capacity;
    int reserved;
};

bool read_workshop(std::istream& input, Workshop& result);
```

**`rules.cpp`**, z przestawioną linią:

<!-- file: workshop_strong rules.cpp -->
```cpp
#include "rules.hpp"

bool read_workshop(std::istream& input, Workshop& result) {
    int capacity{0};
    int reserved{0};
    input >> capacity;
    input >> reserved;

    if (input.fail()) {
        return false;
    }

    result = Workshop{capacity, reserved};

    if (capacity < 1 || capacity > 30) {
        return false;
    }

    if (reserved < 0 || reserved > capacity) {
        return false;
    }

    return true;
}
```

**`function_tests.cpp`**:

<!-- file: workshop_strong function_tests.cpp -->
```cpp
#include <iostream>
#include <sstream>
#include <string>

#include "rules.hpp"

std::string bool_text(bool value) {
    if (value) {
        return "true";
    }

    return "false";
}

void check_bool(const std::string& name, bool expected, bool actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << bool_text(expected) << ", actual " << bool_text(actual) << "\n";
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

    std::istringstream input_a{"12 8"};
    Workshop workshop_a{9, 4};
    const bool accepted_a{read_workshop(input_a, workshop_a)};
    check_bool("A accepted", true, accepted_a, checks, failed);
    check_int("A capacity", 12, workshop_a.capacity, checks, failed);
    check_int("A reserved", 8, workshop_a.reserved, checks, failed);

    std::istringstream input_h{"10 11"};
    Workshop workshop_h{9, 4};
    const bool accepted_h{read_workshop(input_h, workshop_h)};
    check_bool("H accepted", false, accepted_h, checks, failed);
    check_int("H capacity", 9, workshop_h.capacity, checks, failed);
    check_int("H reserved", 4, workshop_h.reserved, checks, failed);

    std::cout << "Checks: " << checks << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

**`CMakeLists.txt`**:

<!-- cmake: workshop_strong -->
```cmake
cmake_minimum_required(VERSION 3.28)
project(first_program LANGUAGES CXX)

add_executable(first_program main.cpp rules.cpp)
target_compile_features(first_program PRIVATE cxx_std_20)
set_target_properties(first_program PROPERTIES CXX_EXTENSIONS OFF)

add_executable(function_tests function_tests.cpp rules.cpp)
target_compile_features(function_tests PRIVATE cxx_std_20)
set_target_properties(function_tests PROPERTIES CXX_EXTENSIONS OFF)
```

</details>

**Różne usterki, różne przypadki.** Zestaw A–J z rozwiązania referencyjnego wykrywa każdą z tych wersji funkcji innymi przypadkami:

| Usterka | Co robi funkcja | Przypadki z `FAIL` | Sprawdzenia z `FAIL` |
|---|---|---|---|
| M1, dostarczona w części B | odrzuca salę zajętą w całości: `reserved >= capacity` | C, D | po trzy: wynik i oba pola |
| M2, z części C | zapisuje rekord przed sprawdzeniem zakresów | E, F, G, H | po dwa: oba pola, wynik jest poprawny |
| M3 | nie sprawdza górnej granicy pojemności | F | trzy |
| M4 | nie sprawdza, czy rezerwacji nie jest więcej niż miejsc | H | trzy |

Przy M2 przypadki I i J przechodzą: odczyt się nie udaje, zanim funkcja dojdzie do zapisu rekordu. Usterki M3 i M4 nie są częścią obowiązkowej pracy. Sprawdź w swojej tabeli, które z Twoich przypadków by je wykryły.

</details>

## Odpowiedzi do pytań z części C

<details>
<summary>Przykładowe odpowiedzi, dla rozwiązania referencyjnego</summary>

1. Bo specyfikacja mówi, co funkcja ma robić. Wynik wzięty z działania funkcji powtórzyłby jej błąd, a test przeszedłby także dla błędnej funkcji (lekcja 13.1).
2. Bo w typowym przypadku wszystkie reguły są spełnione naraz i daleko od granic. Usterka M1 przepuszcza `12 8` i wszystkie zwykłe sale, a myli się tylko na granicy.
3. Bo to granica reguły `reserved <= capacity`: jedyny przypadek, w którym `<` i `<=` dają różny wynik. Bez niego nikt nie zauważy, że pełna sala jest odrzucana.
4. `FAIL` mówi, że wynik rzeczywisty różni się od oczekiwanego. Nie rozstrzyga, czy błąd jest w funkcji, czy w wyniku oczekiwanym: to ustala się, wracając do specyfikacji (lekcja 13.2).
5. Bo kontrakt obejmuje też rekord: przy sukcesie oba pola mają odczytane wartości, a przy odmowie zostają bez zmian. Usterka M2 daje poprawny wynik `bool` i zły rekord.
6. Bo podaje funkcji tekst zapisany w programie: każdy przypadek ma swoje dane, nie trzeba niczego wpisywać ani przygotowywać pliku, a wynik jest za każdym razem taki sam.
7. Bo strumień zapamiętuje, co już odczytano. Przypadek, który czytałby ze strumienia poprzedniego, zaczynałby od innych danych niż te z tabeli (lekcja 13.3).
8. Bo testy mają sprawdzać tę samą funkcję, której używa program właściwy. Poprawka w `rules.cpp` trafia wtedy do obu programów, a test kopii sprawdzałby tylko kopię (lekcja 13.4).
9. Bo program testowy zwraca 1, gdy wykrył niezgodność. Przed poprawką funkcji to jest dokładnie ten wynik, którego oczekujesz: dowód, że test wykrywa usterkę.
10. Trzeba zbudować oba programy i uruchomić te same testy, bez zmiany wyników oczekiwanych: wszystkie powinny dać `PASS`, z kodem 0. Nie dowodzi to poprawności dla wszystkich danych, tylko brak niezgodności w sprawdzonych przypadkach.

</details>

## Samoocena

Przy każdej kompetencji zaznacz jedną odpowiedź:

| Kompetencja | Samodzielnie | Z podpowiedzią | Po zajrzeniu do rozwiązania | Do powtórki |
|---|---|---|---|---|
| Plan przypadków przed kodem | | | | |
| Wyniki oczekiwane ze specyfikacji | | | | |
| Dwa targety i wspólny `rules.cpp` | | | | |
| `std::istringstream` i osobny strumień dla przypadku | | | | |
| Sprawdzanie wyniku `bool` i obu pól | | | | |
| Niezmieniony rekord po odmowie | | | | |
| Dobór przypadków granicznych i błędnych | | | | |
| Wykrycie usterki przed poprawką | | | | |
| Poprawka i ponowne testy | | | | |
| Diagnostyka słabego testu | | | | |

Jeśli adaptujesz wcześniejszy kod, zapisz pod tabelą, z którego programu korzystano, co z niego przeniesiono, co zmieniono i jakie decyzje projektowe podjęto samodzielnie: przypadki, wyniki oczekiwane, rekord startowy i sposób wykazania błędu.

Jeśli w kolumnie „Do powtórki” jest coś zaznaczone, wróć do odpowiedniej lekcji:

| Temat | Lekcja |
|---|---|
| wynik oczekiwany i rzeczywisty, `PASS` i `FAIL`, kod zakończenia | [13.1](lesson_01_self_checking_program.md) |
| przypadki typowe, graniczne i błędne, przypadek odróżniający usterkę | [13.2](lesson_02_test_cases_that_catch_bugs.md) |
| `std::istringstream`, osobny strumień, rekord po odmowie | [13.3](lesson_03_testing_input_without_a_file.md) |
| dwa targety, wspólny `rules.cpp`, regresja | [13.4](lesson_04_tests_next_to_the_program.md) |
| nagłówek i plik `.cpp`, `#pragma once` | [11.2](../module_11_multifile_programs/lesson_02_own_header_file.md) |

---

## Podsumowanie Modułu 13

Po pięciu lekcjach potrafisz:

- pisać program testowy, który porównuje wynik rzeczywisty z oczekiwanym, wypisuje `PASS` albo `FAIL`, liczy niepowodzenia i kończy się kodem 1, gdy coś się nie zgadza;
- ustalać wyniki oczekiwane ze specyfikacji, nigdy z działania sprawdzanej funkcji;
- dobierać przypadki typowe, graniczne i błędne tak, żeby odróżniały poprawną funkcję od wersji z usterką;
- testować funkcję odczytu bez pliku i bez klawiatury, przez `std::istringstream`, sprawdzając wynik i rekord;
- budować program i jego testy w jednym projekcie, z jednej definicji funkcji, w dwóch targetach CMake;
- wykazywać usterkę testem przed poprawką i potwierdzać poprawkę tymi samymi testami.

## Co dalej

To koniec Modułu 13 i wszystkich jego zaplanowanych lekcji. W Module 14, „Nazwane stany i wyniki funkcji”, stany i wyniki funkcji dostaną własne nazwy, które sprawdza kompilator. Zacznij od pierwszej lekcji: [Lekcja 14.1: Stan z nazwą zamiast tekstu](../module_14_named_states/lesson_01_named_state_instead_of_text.md).

**Poprzednia lekcja:** [Lekcja 13.4: Testy obok programu](lesson_04_tests_next_to_the_program.md) · **Następna lekcja:** [Lekcja 14.1: Stan z nazwą zamiast tekstu](../module_14_named_states/lesson_01_named_state_instead_of_text.md) · [Opis kursu](../../README.md)

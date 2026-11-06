# Lekcja 12.4: Seanse w kinie (sprawdzian Modułu 12)

**Polski** · [English](lesson_04_cinema_screenings.en.md) · [Opis kursu](../../README.md)

> **Moduł 12, lekcja 4: sprawdzian** · około 100–120 minut, w dwóch podejściach
> **Potrzebujesz:** katalogu `cpp-workspace` i oryginalnego projektu `lesson_05_first_program`.
> **Wersja pilotażowa.** Rozwiązanie referencyjne i program z diagnostyki sprawdzamy automatycznie na Windowsie, Ubuntu i macOS, z podanymi plikami danych. Twojego projektu nic nie ocenia automatycznie: sprawdzasz go samodzielnie, według listy kontrolnej. Kroki w CLionie (nowy plik, pole **Working directory**) są takie jak w lekcjach 12.1–12.3: opisujemy je według dokumentacji CLion 2026.3, bez ręcznego sprawdzenia na każdym systemie.

## Jak przebiega ten sprawdzian

Ta lekcja nie wprowadza niczego nowego. Sprawdzasz, czy potrafisz **samodzielnie zaprojektować, napisać i sprawdzić program, który odczytuje plik tekstowy**, kontroluje jego rekordy, wskazuje numer błędnej linii i tworzy raport dopiero po poprawnym przetworzeniu całego pliku. Łączysz w nim lekcje 12.1–12.3.

Sprawdzian ma trzy części i omówienie:

- **Część A: plan.** Krótki plan danych, odczytu i odpowiedzialności, zanim napiszesz kod.
- **Część B: implementacja i testy.** Program według specyfikacji, sprawdzony przypadkami kontrolnymi. To największa część pracy.
- **Część C: diagnostyka i uzasadnienie.** Błąd w numerowaniu linii i pytania o Twoje decyzje. Wykonaj ją po części B.
- **Sprawdzenie i omówienie:** podpowiedzi, pełna lista przypadków, rozwiązanie referencyjne, wyjaśnienie diagnostyki, odpowiedzi i samoocena. Przejdź tam dopiero po częściach A i B albo wtedy, gdy świadomie zrezygnujesz z dalszej samodzielnej próby.

Zajrzenie do podpowiedzi albo do wcześniejszych lekcji nie jest porażką. Ważne jest, żeby **uczciwie zanotować, co zrobiono samodzielnie, a co z pomocą**. Proponowany podział na dwa podejścia:

- **pierwsze:** specyfikacja, część A, projekt w CLionie, typ rekordu, funkcja odczytu i przypadek A;
- **drugie:** pełna kontrola danych, numery linii, raport, przypadki kontrolne, część C i samoocena.

**Możesz używać:** CLiona albo terminala, CMake i Ninja, jak dotąd; `CMakeLists.txt` skopiowanego z oryginalnego `lesson_05_first_program`; lekcji 12.1–12.3 jako przypomnienia; tabel przypadków. Debugger nie jest potrzebny. Wszystko, czego potrzebujesz, znasz z Modułów 1–12.

---

## Specyfikacja: seanse w kinie

Małe kino zapisuje w pliku repertuar dnia: tytuł filmu i stan seansu. Program odczytuje ten plik i wypisuje wszystkie seanse oraz to, ile z nich ma wolne miejsca, ile jest wyprzedanych, a ile odwołanych. Nie modeluje godzin, sal, cen ani biletów.

**Przygotowanie:** w `cpp-workspace` utwórz katalog `cinema_screenings` i skopiuj do niego `CMakeLists.txt` z oryginalnego `lesson_05_first_program`. Obok utwórz `main.cpp` i plik danych `screenings.txt`, tak jak w lekcji 12.1, punkt 3. `CMakeLists.txt` zostaw bez zmian: `screenings.txt` to dane, które odczytuje działający program, a nie plik do skompilowania, więc nie dopisuj go do `add_executable`. Otwórz katalog w CLionie i sprawdź pole **Working directory** konfiguracji `first_program`, jak w lekcji 12.1, punkt 4. Sam fakt, że plik leży obok `main.cpp`, nie wystarcza: program szuka go w swoim katalogu roboczym.

```text
cinema_screenings/
├── CMakeLists.txt
├── main.cpp
└── screenings.txt
```

### Plik `screenings.txt`

Plik zawiera zero lub więcej rekordów. Każdy rekord zajmuje dokładnie dwie fizyczne linie:

1. tytuł filmu;
2. status seansu: `available` (są wolne miejsca), `full` (seans wyprzedany) albo `cancelled` (seans odwołany).

**Zasady:**

- Tytuł nie jest pustą linią, może zawierać spacje i może się powtarzać: każde wystąpienie to osobny seans. Program zachowuje tytuł dokładnie, ze wszystkimi znakami, także ze spacjami na początku i na końcu. Linia z samymi spacjami nie jest pusta, więc jest poprawnym tytułem.
- Status ma dokładnie jedną z trzech postaci. Wielkość liter ma znaczenie i nie ma dodatkowych spacji: `Available`, `FULL`, `Canceled` i `available ` ze spacją na końcu są nieprawidłowe.
- Liczba seansów nie jest ograniczona. Pusty plik, czyli plik bez żadnego znaku, jest poprawny i oznacza zero seansów.
- Dane są tekstem ASCII, a linie kończy znak `\n`.

### Koniec danych i błędy

- **Dane kończy wyłącznie koniec pliku** w miejscu, w którym zaczynałby się kolejny rekord. Pusta linia nie jest znakiem końca.
- Ostatnia linia może nie mieć znaku końca linii: to nie jest błąd. Znak końca linii po ostatnim statusie nie tworzy dodatkowej, pustej linii. Tworzy ją dopiero drugi znak końca linii z rzędu.
- Linie są numerowane od 1, jak w edytorze. N w komunikatach to zawsze numer fizycznej linii pliku.

| Sytuacja | Standardowe wyjście |
|---|---|
| pliku nie udało się otworzyć | `Cannot open screenings.txt` |
| pusta linia: przed pierwszym rekordem, w miejscu tytułu albo statusu, między rekordami albo na końcu pliku | `Empty line N`, gdzie N to numer tej pustej linii |
| status niepusty, ale inny niż `available`, `full` i `cancelled` | `Invalid line N`, gdzie N to numer linii statusu |
| plik kończy się zaraz po tytule, bez linii statusu | `Incomplete record on line N`, gdzie N to numer linii tego tytułu |

- Program sprawdza rekordy po kolei, od początku pliku, i zgłasza **pierwszy** błąd. Przy każdej linii najpierw sprawdza, czy udało się ją odczytać, potem czy jest pusta, a dopiero na końcu, czy status jest dozwolony. Pusty status to więc `Empty line N`, a nie `Invalid line N`.
- Po błędzie program wypisuje tylko ten jeden komunikat, bez żadnej części raportu, i kończy pracę kodem 0. Nie wypisuje niczego na `std::cerr`.

### Raport

Gdy cały plik jest poprawny, program wypisuje:

```text
Screenings: N
TITLE: STATUS
Available total: A
Full total: F
Cancelled total: C
```

- Linia `TITLE: STATUS` powtarza się dla każdego seansu, w kolejności z pliku: tytuł, dwukropek, spacja i status, na przykład `Morning Birds: available`.
- `N` to liczba wszystkich seansów, a `A`, `F` i `C` to liczby seansów ze statusem `available`, `full` i `cancelled`. Każdy seans liczy się w dokładnie jednym z trzech podsumowań, więc razem dają `N`.
- Program nie sortuje seansów, nie usuwa powtórzeń i nie dopisuje numerów. Raport wypisuje dopiero po sprawdzeniu całego pliku. Przykład raportu jest w przypadku A w części B.

### Wymagana struktura

- **Typ rekordu** (`struct`) z tytułem i statusem oraz **wektor** rekordów w kolejności z pliku.
- **Funkcja odczytu**, która dostaje strumień przez `std::istream&` i odczytuje z niego cały plik: każdą linię przez `std::getline`, z licznikiem fizycznych linii. Rozpoznaje koniec danych i błędy, a kodowi wywołującemu przekazuje rodzaj pierwszego błędu i numer jego linii. Nie otwiera pliku, nie używa `std::cin` i niczego nie wypisuje. Tę samą funkcję dałoby się wywołać ze `std::cin` zamiast otwartego pliku, bez zmian w jej treści, choć Twój program czyta tylko `screenings.txt`.
- **`main`** otwiera `screenings.txt`, sprawdza otwarcie, wywołuje funkcję odczytu i wypisuje albo jeden komunikat, albo pełny raport. Raport z trzema podsumowaniami powstaje dopiero wtedy, gdy funkcja odczytu przeczyta cały plik bez błędu.
- Pól rekordu nie odczytujesz przez `>>`, a pętli nie sterujesz przez `eof()`. O tym, czy linia jest odczytana, decyduje `fail()` po odczycie.
- Wystarczy jeden plik `main.cpp`. Możesz podzielić program na kilka plików, jak w Module 11, ale nie jest to wymagane i nie daje dodatkowych punktów.

**Zdecyduj samodzielnie:**

1. jak nazwać typ rekordu, jego pola i wektor;
2. jakie funkcje będzie miał program i jak je nazwać;
3. jakie parametry ma funkcja odczytu i co zwraca;
4. jak funkcja odczytu przekaże rodzaj błędu i numer linii;
5. gdzie zaczyna się licznik linii i kiedy rośnie;
6. po czym program pozna poprawny koniec danych, a po czym niekompletny rekord;
7. jak sprawdzi, czy status jest dozwolony;
8. gdzie i jak policzy trzy podsumowania;
9. jak nie dopuści do częściowego raportu;
10. jakimi plikami danych sprawdzi swój program.

Przypomnienie znajdziesz w lekcjach [12.1](lesson_01_first_data_file.md) (plik danych, katalog roboczy, nieudane otwarcie), [12.2](lesson_02_records_from_a_file.md) (funkcja odczytu z `std::istream&`) i [12.3](lesson_03_end_of_data_and_errors.md) (koniec pliku, puste linie, numery linii).

---

# Część A: plan

Zanim napiszesz kod, przygotuj na piśmie krótki plan. Kilka zdań albo tabela wystarczą. Plan odpowiada na dziesięć pytań:

1. Jak wygląda w programie jeden seans?
2. W czym program przechowuje listę seansów?
3. Gdzie program otwiera `screenings.txt`?
4. Która funkcja odczytuje rekordy?
5. Jak ta funkcja dostaje strumień?
6. Jak program odróżnia poprawny koniec danych od błędu?
7. Jak program numeruje linie?
8. Jak funkcja odczytu przekazuje rodzaj błędu i numer linii?
9. Gdzie program liczy trzy podsumowania?
10. Kiedy program wypisuje raport?

Odpowiedz też krótko:

1. Dlaczego funkcja odczytu przyjmuje `std::istream&`?
2. Dlaczego otwarcie `std::ifstream` nie powinno być ukryte wewnątrz funkcji odczytu, której można używać z różnymi strumieniami?
3. Czym różni się koniec pliku od pustej linii?
4. Dlaczego licznik linii rośnie dopiero po udanym `std::getline`?
5. Dlaczego raport powstaje dopiero po sprawdzeniu całego pliku?

Plan jest obowiązkową częścią sprawdzianu i jest oceniany razem z programem.

---

# Część B: implementacja i testy

Napisz program według specyfikacji i swojego planu. **Przed uruchomieniem** przygotuj tabelę przypadków: zawartość pliku i przewidywany wynik. Wyniki poniżej wynikają wprost ze specyfikacji. Każdy przypadek to inna zawartość `screenings.txt` albo brak pliku. Programu nie budujesz od nowa.

**A: trzy poprawne seanse.**

<!-- run: screenings -->

<!-- datafile: screenings screenings.txt -->
```text
Morning Birds
available
Northern Lights
full
Evening Stories
cancelled
```

<!-- output: screenings -->
```text
Screenings: 3
Morning Birds: available
Northern Lights: full
Evening Stories: cancelled
Available total: 1
Full total: 1
Cancelled total: 1
```

**B: pusty plik.** Plik istnieje, ale nie ma w nim ani jednego znaku.

<!-- run: screenings -->

<!-- datafile: screenings screenings.txt -->
```text
```

<!-- output: screenings -->
```text
Screenings: 0
Available total: 0
Full total: 0
Cancelled total: 0
```

**C: brak pliku.** W katalogu roboczym nie ma `screenings.txt`.

<!-- run: screenings -->

<!-- output: screenings -->
```text
Cannot open screenings.txt
```

**D: jedna pusta linia.** Plik zawiera tylko jeden znak końca linii.

<!-- run: screenings -->

<!-- datafile: screenings screenings.txt -->
```text

```

<!-- output: screenings -->
```text
Empty line 1
```

**E: pusty status.** Plik to `Morning Birds\n\n`.

<!-- run: screenings -->

<!-- datafile: screenings screenings.txt -->
```text
Morning Birds

```

<!-- output: screenings -->
```text
Empty line 2
```

**F: brak statusu.** Plik to `Morning Birds\n`, więc istnieje tylko linia tytułu.

<!-- run: screenings -->

<!-- datafile: screenings screenings.txt -->
```text
Morning Birds
```

<!-- output: screenings -->
```text
Incomplete record on line 1
```

**H: ostatni status bez znaku końca linii.** Plik to dokładnie `Morning Birds\navailable`. Takiego pliku nie musisz przygotowywać: testy kursu sprawdzają go automatycznie.

<!-- run: screenings -->

<!-- datafile: screenings screenings.txt noeol -->
```text
Morning Birds
available
```

<!-- output: screenings -->
```text
Screenings: 1
Morning Birds: available
Available total: 1
Full total: 0
Cancelled total: 0
```

**M: nieprawidłowy status drugiego seansu.** Pierwszy seans był poprawny, ale nie ma częściowego raportu.

<!-- run: screenings -->

<!-- datafile: screenings screenings.txt -->
```text
Morning Birds
available
Evening Stories
unknown
```

<!-- output: screenings -->
```text
Invalid line 4
```

Pozostałe przypadki, G i I–T, są w pełnej liście w części „Sprawdzenie i omówienie”. Wynikają z tej samej specyfikacji: nie ma w nich żadnej nowej reguły.

**Uruchom obowiązkowo**, zmieniając tylko zawartość albo nazwę `screenings.txt`:

1. A;
2. C: zmień nazwę pliku, na przykład na `screenings_old.txt`, uruchom program i przywróć nazwę;
3. D albo E;
4. M;
5. F, a potem wykonaj część C.

Pozostałe przypadki przewidź w swojej tabeli i porównaj z pełną listą. Wszystkie są sprawdzone automatycznie dla rozwiązania referencyjnego.

---

# Część C: diagnostyka i uzasadnienie

Wykonaj tę część **po części B**.

## Diagnostyka: numer linii, której nie ma

Ktoś napisał program, który powinien wskazywać linię niekompletnego rekordu. Przy odczycie statusu licznik linii rośnie jednak zaraz po `std::getline`, zanim program sprawdzi, czy odczyt się udał:

<!-- fragment -->
```cpp
std::getline(input, status);
++line_number;

if (input.fail()) {
    error = "incomplete";
    error_line = line_number;
    return false;
}
```

Tytuł został już poprawnie odczytany i ma numer 1, a plik to `Morning Birds\n`, jak w przypadku F.

1. Przewidź, jaki numer wypisze ten program dla F.
2. Wyjaśnij, dlaczego ten numer jest niepoprawny.
3. Wskaż linię kodu, która powoduje problem.
4. Zaproponuj najmniejszą poprawkę.
5. Sprawdź, że Twój program dla F wypisuje `Incomplete record on line 1`. To piąte obowiązkowe uruchomienie z części B. Jeśli chcesz, wprowadź ten sam błąd do swojego programu, uruchom go dla F i przywróć poprawną kolejność.
6. Wyjaśnij, dlaczego brakujący status nie powinien zwiększać licznika fizycznych linii.
7. Dla których przypadków z części B ten błąd zmieni wynik, a dla których nie? Co z tego wynika dla testowania?

## Uzasadnienie

Odpowiedz własnymi słowami, odnosząc się do swojego programu:

1. Dlaczego Twoja funkcja odczytu przyjmuje `std::istream&`, a nie `std::ifstream` przez wartość?
2. Dlaczego pusty plik jest poprawny?
3. Dlaczego pusta linia nie kończy danych?
4. Kiedy Twój program zwiększa licznik linii?
5. Dlaczego przy niekompletnym rekordzie program wskazuje linię tytułu?
6. Dlaczego trzy podsumowania razem dają liczbę seansów?
7. Dlaczego po błędzie nie ma częściowego raportu i co w Twoim programie to zapewnia?
8. Jaką rolę pełni katalog roboczy programu?
9. Jak można by użyć tej samej funkcji odczytu dla danych ze `std::cin`?

---

## Lista kontrolna przed oddaniem

Sprawdzian jest zaliczony, gdy spełniasz **wszystkie** punkty tej listy. Twój podział na funkcje i pliki może być inny niż w rozwiązaniu referencyjnym, jeśli spełnia specyfikację. Poprawny wynik dla samego przypadku A nie wystarcza.

- [ ] Plan z części A powstał przed kodem i zgadza się z programem.
- [ ] Program otwiera `screenings.txt`, sprawdza otwarcie i przy nieudanym otwarciu wypisuje `Cannot open screenings.txt`.
- [ ] Rekordy odczytuje funkcja, która dostaje strumień przez `std::istream&`, nie otwiera pliku, nie używa `std::cin` i niczego nie wypisuje.
- [ ] Obie linie rekordu są odczytywane przez `std::getline`, bez `>>`.
- [ ] Program odróżnia koniec pliku od pustej linii: pusty plik daje raport bez seansów, a każda pusta linia daje `Empty line N`.
- [ ] Licznik rośnie tylko po udanym `std::getline`, a numery w komunikatach są numerami fizycznych linii.
- [ ] Program rozpoznaje pustą linię, niedozwolony status i niekompletny rekord, w kolejności sprawdzeń ze specyfikacji.
- [ ] Program zgłasza tylko pierwszy błąd i po nim nie wypisuje żadnej części raportu.
- [ ] Raport zachowuje wszystkie seanse, ich kolejność i powtórzone tytuły, z tytułami bez zmian.
- [ ] Trzy podsumowania są poprawne i razem dają liczbę seansów.
- [ ] Raport i komunikaty zgadzają się ze specyfikacją co do znaku.
- [ ] Obowiązkowe uruchomienia (A, C, D albo E, M i F) dają pokazane wyniki, a przewidywania pozostałych przypadków zgadzają się z pełną listą.
- [ ] Część C jest wykonana: błąd licznika jest wyjaśniony, a poprawka wskazana i sprawdzona dla F.
- [ ] Umiesz wyjaśnić swoje decyzje: odpowiedzi z uzasadnienia odnoszą się do Twojego programu.

Gdy skończysz, możesz zapisać projekt w Gicie, jak w lekcji 1.5: `main.cpp`, `CMakeLists.txt` i `screenings.txt` z danymi A, bez katalogu budowania. Zwykły plik danych należy do projektu i może być śledzony razem z kodem.

## Kryteria oceny

Rubryka służy do samooceny albo do oceny przez prowadzącego. Kurs nie ma skali ocen ani progu punktowego: punkty pokazują, które obszary są opanowane, a które wymagają powtórki. O zaliczeniu decyduje lista kontrolna powyżej, a nie liczba punktów.

| Obszar | Punkty | Pełne punkty, gdy |
|---|---:|---|
| Plan i podział odpowiedzialności | 10 | plan powstał przed kodem, odpowiada na dziesięć pytań i pięć krótkich pytań, a program jest z nim zgodny |
| Przygotowanie projektu i obsługa pliku | 15 | `CMakeLists.txt` jest kanoniczny i nie wymienia pliku danych, **Working directory** wskazuje katalog z `screenings.txt`, `main` sprawdza otwarcie przed odczytem, a brak pliku daje dokładny komunikat |
| Funkcja odczytu przyjmująca `std::istream&` | 15 | cały odczyt stoi w funkcji z parametrem `std::istream&`, która nie otwiera pliku, nie używa `std::cin` i niczego nie wypisuje, a odpowiedź o użyciu jej ze `std::cin` jest poprawna |
| EOF, puste linie i numerowanie | 20 | koniec danych rozpoznaje nieudany odczyt tytułu, każda pusta linia daje `Empty line N`, licznik rośnie tylko po udanym `std::getline`, a numery są poprawne także dla F, G i O |
| Walidacja, błędy i brak częściowego raportu | 15 | trzy rodzaje błędów są rozpoznawane w kolejności ze specyfikacji, komunikaty są dokładne, program zgłasza tylko pierwszy błąd, a po nim nie wypisuje żadnej części raportu |
| Rekordy i raport z trzema podsumowaniami | 10 | seanse są w kolejności z pliku, z powtórzeniami i niezmienionymi tytułami, a trzy podsumowania są poprawne i razem dają liczbę seansów |
| Testy, diagnostyka i uzasadnienie | 15 | tabela przypadków powstała przed uruchomieniem, obowiązkowe uruchomienia dają pokazane wyniki, błąd licznika z części C jest wyjaśniony i poprawiony, a odpowiedzi odnoszą się do projektu |
| **Razem** | **100** | |

- **Poprawny wynik nie daje automatycznie wszystkich punktów:** plan, funkcję odczytu i strukturę ocenia się, czytając program.
- **Odczyt bez funkcji z `std::istream&`**, na przykład cały w `main` albo w funkcji, która sama otwiera plik, nie dostaje punktów za funkcję odczytu, nawet przy dobrym wyniku.
- **Częściowy raport po błędzie** narusza specyfikację: oznacza brak punktów za walidację i błędy.
- **Dobry wynik dla A przy złych numerach dla F, G albo O** nie daje pełnych punktów za numerowanie.
- **Inne nazwy** i inny, uzasadniony podział na funkcje nie odbierają punktów. Podział na kilka plików nie daje dodatkowych punktów, a jeden `main.cpp` ich nie odbiera.

**Co sprawdza automat, a co nie.** Testy kursu sprawdzają, że rozwiązanie referencyjne i program z diagnostyki się budują i dają pokazane wyniki. Twoje uruchomienia przypadków kontrolnych sprawdzają zachowanie Twojego programu dla tych danych. **Twojego kodu, planu i uzasadnienia nie sprawdza żaden automat:** ocenia je człowiek, czytając plan i program.

---

# Sprawdzenie i omówienie

Przejdź tutaj **dopiero po częściach A i B** albo wtedy, gdy świadomie zrezygnujesz z dalszej samodzielnej próby. Dalej jest kod rozwiązania.

## Podpowiedzi

<details>
<summary>Podpowiedź 1: dane i funkcje</summary>

Które działania zależą od zawartości pliku, a które tylko od gotowej listy seansów? Odczyt i kontrola dotyczą każdej linii pliku po kolei. Raport i podsumowania potrzebują już tylko listy poprawnych seansów. Co z tego powinna wiedzieć funkcja odczytu, a co `main`?

</details>

<details>
<summary>Podpowiedź 2: koniec pliku i błędy</summary>

Rozróżnij cztery sytuacje: nieudany odczyt tytułu; udany odczyt pustej linii; nieudany odczyt statusu po tytule; udany odczyt niepustego statusu, który nie jest dozwolony. Która z nich jest jedynym poprawnym końcem listy, a która oznacza niekompletny rekord?

</details>

<details>
<summary>Podpowiedź 3: numerowanie i raport</summary>

Licznik linii mówi, ile linii udało się już odczytać: rośnie po każdym udanym `std::getline`, także po statusie, a po nieudanym nie rośnie. Rodzaj błędu i numer linii funkcja odczytu może zapisać w zmiennych przekazanych przez referencję, jak w lekcji 12.3. Podsumowania i raport policz dopiero wtedy, gdy funkcja zakończy się sukcesem.

</details>

## Pełna lista przypadków kontrolnych

<details>
<summary>Przypadki G i I–T, sprawdzone automatycznie dla rozwiązania referencyjnego</summary>

**G: brak statusu, bez znaku końca linii.** Plik to dokładnie `Morning Birds`.

<!-- run: screenings -->

<!-- datafile: screenings screenings.txt noeol -->
```text
Morning Birds
```

<!-- output: screenings -->
```text
Incomplete record on line 1
```

**I: pusta linia na końcu.** Plik to `Morning Birds\navailable\n\n`: drugi znak końca linii tworzy linię 3, pustą.

<!-- run: screenings -->

<!-- datafile: screenings screenings.txt -->
```text
Morning Birds
available

```

<!-- output: screenings -->
```text
Empty line 3
```

**J: nieznany status.**

<!-- run: screenings -->

<!-- datafile: screenings screenings.txt -->
```text
Morning Birds
postponed
```

<!-- output: screenings -->
```text
Invalid line 2
```

**K: wielka litera w statusie.**

<!-- run: screenings -->

<!-- datafile: screenings screenings.txt -->
```text
Morning Birds
Available
```

<!-- output: screenings -->
```text
Invalid line 2
```

**L: spacja po statusie.** W drugiej linii jest `full` i jedna spacja.

<!-- run: screenings -->

<!-- datafile: screenings screenings.txt -->
```text
Morning Birds
full 
```

<!-- output: screenings -->
```text
Invalid line 2
```

**N: pusta linia między seansami.** Za nią są jeszcze dane, ale odczyt nie kończy się na pierwszym seansie.

<!-- run: screenings -->

<!-- datafile: screenings screenings.txt -->
```text
Morning Birds
available

Evening Stories
full
```

<!-- output: screenings -->
```text
Empty line 3
```

**O: niekompletny drugi rekord.**

<!-- run: screenings -->

<!-- datafile: screenings screenings.txt -->
```text
Morning Birds
available
Evening Stories
```

<!-- output: screenings -->
```text
Incomplete record on line 3
```

**P: ten sam tytuł dwa razy.** Każde wystąpienie to osobny seans.

<!-- run: screenings -->

<!-- datafile: screenings screenings.txt -->
```text
Morning Birds
available
Morning Birds
full
```

<!-- output: screenings -->
```text
Screenings: 2
Morning Birds: available
Morning Birds: full
Available total: 1
Full total: 1
Cancelled total: 0
```

**Q: pięć seansów,** dwa `available`, dwa `full` i jeden `cancelled`.

<!-- run: screenings -->

<!-- datafile: screenings screenings.txt -->
```text
Morning Birds
available
Northern Lights
full
Evening Stories
cancelled
Harbour Lights
available
Silent River
full
```

<!-- output: screenings -->
```text
Screenings: 5
Morning Birds: available
Northern Lights: full
Evening Stories: cancelled
Harbour Lights: available
Silent River: full
Available total: 2
Full total: 2
Cancelled total: 1
```

**R: tytuł ze spacjami.**

<!-- run: screenings -->

<!-- datafile: screenings screenings.txt -->
```text
The Last Morning Show
cancelled
```

<!-- output: screenings -->
```text
Screenings: 1
The Last Morning Show: cancelled
Available total: 0
Full total: 0
Cancelled total: 1
```

**S: tytuł z samych spacji.** Pierwsza linia zawiera trzy spacje. To nie jest pusta linia, więc raport zachowuje te spacje przed dwukropkiem.

<!-- run: screenings -->

<!-- datafile: screenings screenings.txt -->
```text
   
available
```

<!-- output: screenings -->
```text
Screenings: 1
   : available
Available total: 1
Full total: 0
Cancelled total: 0
```

**T: kilka błędów w jednym pliku.** Pierwszy jest nieprawidłowy status w linii 2. Dalej są jeszcze pusta linia i status `Full`, ale program zgłasza tylko pierwszy błąd.

<!-- run: screenings -->

<!-- datafile: screenings screenings.txt -->
```text
Morning Birds
postponed

Evening Stories
Full
```

<!-- output: screenings -->
```text
Invalid line 2
```

| Przypadek | Plik `screenings.txt` | Standardowe wyjście |
|---|---|---|
| A | trzy seanse, po jednym z każdym statusem | 3 seanse, podsumowania 1, 1 i 1 |
| B | pusty plik | `Screenings: 0` i trzy zera |
| C | brak pliku | `Cannot open screenings.txt` |
| D | jedna pusta linia | `Empty line 1` |
| E | `Morning Birds`, pusta linia | `Empty line 2` |
| F | `Morning Birds` ze znakiem końca linii | `Incomplete record on line 1` |
| G | `Morning Birds` bez znaku końca linii | `Incomplete record on line 1` |
| H | `Morning Birds`, `available` bez znaku końca linii | 1 seans, podsumowania 1, 0 i 0 |
| I | `Morning Birds`, `available`, pusta linia | `Empty line 3` |
| J | `Morning Birds`, `postponed` | `Invalid line 2` |
| K | `Morning Birds`, `Available` | `Invalid line 2` |
| L | `Morning Birds`, `full` ze spacją | `Invalid line 2` |
| M | drugi seans ze statusem `unknown` | `Invalid line 4` |
| N | pusta linia między seansami | `Empty line 3` |
| O | drugi tytuł bez statusu | `Incomplete record on line 3` |
| P | ten sam tytuł z dwoma statusami | 2 seanse, podsumowania 1, 1 i 0 |
| Q | pięć seansów | 5 seansów, podsumowania 2, 2 i 1 |
| R | `The Last Morning Show`, `cancelled` | 1 seans, podsumowania 0, 0 i 1 |
| S | trzy spacje, `available` | 1 seans o tytule z trzech spacji |
| T | `postponed` w linii 2, dalej kolejne błędy | `Invalid line 2` |

</details>

## Rozwiązanie referencyjne

<details>
<summary>Plan i program rozwiązania referencyjnego</summary>

To jedno z poprawnych rozwiązań, a nie jedyna dopuszczalna struktura.

| Część programu | Odpowiedzialność | Dane wejściowe | Wynik |
|---|---|---|---|
| `struct Screening` | jeden seans | — | tytuł i status jako `std::string` |
| `is_allowed_status` | sprawdzenie statusu | tekst statusu | `true` albo `false` |
| `read_screenings` | odczyt i kontrola całego pliku | strumień przez `std::istream&` i pusty wektor | `true` i wypełniony wektor albo `false` z rodzajem błędu i numerem linii |
| `print_report` | raport i trzy podsumowania | wektor seansów przez `const&` | linie raportu na standardowym wyjściu |
| `main` | otwarcie pliku, wywołanie odczytu, komunikat albo raport | `screenings.txt` | standardowe wyjście |

**`main.cpp`**:

<!-- example: screenings -->
```cpp
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

struct Screening {
    std::string title;
    std::string status;
};

bool is_allowed_status(const std::string& status) {
    return status == "available" || status == "full" || status == "cancelled";
}

bool read_screenings(std::istream& input, std::vector<Screening>& screenings, std::string& error, int& error_line) {
    int line_number{0};
    std::string title{};
    std::getline(input, title);

    while (!input.fail()) {
        ++line_number;

        if (title.empty()) {
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

        if (!is_allowed_status(status)) {
            error = "invalid";
            error_line = line_number;
            return false;
        }

        screenings.push_back(Screening{title, status});
        std::getline(input, title);
    }

    return true;
}

void print_report(const std::vector<Screening>& screenings) {
    int available_total{0};
    int full_total{0};
    int cancelled_total{0};
    std::cout << "Screenings: " << screenings.size() << "\n";

    for (const Screening& screening : screenings) {
        std::cout << screening.title << ": " << screening.status << "\n";

        if (screening.status == "available") {
            ++available_total;
        } else if (screening.status == "full") {
            ++full_total;
        } else {
            ++cancelled_total;
        }
    }

    std::cout << "Available total: " << available_total << "\n";
    std::cout << "Full total: " << full_total << "\n";
    std::cout << "Cancelled total: " << cancelled_total << "\n";
}

int main() {
    std::ifstream screenings_file{"screenings.txt"};

    if (screenings_file.fail()) {
        std::cout << "Cannot open screenings.txt\n";
        return 0;
    }

    std::vector<Screening> screenings{};
    std::string error{};
    int error_line{0};
    const bool complete{read_screenings(screenings_file, screenings, error, error_line)};

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

    print_report(screenings);
}
```

**`CMakeLists.txt`**: taki jak w oryginalnym `lesson_05_first_program`, bez zmian. `screenings.txt` nie jest w `add_executable`.

**`screenings.txt`** z danymi A, w katalogu `cinema_screenings`, obok `main.cpp` i `CMakeLists.txt`:

<!-- run: screenings -->

<!-- datafile: screenings screenings.txt -->
```text
Morning Birds
available
Northern Lights
full
Evening Stories
cancelled
```

<!-- output: screenings -->
```text
Screenings: 3
Morning Birds: available
Northern Lights: full
Evening Stories: cancelled
Available total: 1
Full total: 1
Cancelled total: 1
```

- **Uruchomienie:** pole **Working directory** konfiguracji `first_program` wskazuje katalog `cinema_screenings`, ten z `screenings.txt`. W terminalu program uruchamiasz z katalogu `cinema_screenings`.
- **Funkcja odczytu:** `read_screenings` dostaje strumień przez `std::istream&`, a wektor, rodzaj błędu i numer linii przez referencje bez `const`. Nie otwiera pliku i niczego nie wypisuje. Ze `std::cin` wywołanie wyglądałoby tak: `read_screenings(std::cin, screenings, error, error_line)`, bez zmian w funkcji.
- **Kolejność sprawdzeń:** najpierw `fail()` po każdym `std::getline`, potem `empty()`, a dla statusu na końcu `is_allowed_status`. Pusty status daje więc `Empty line N`, a nie `Invalid line N`.
- **Numerowanie:** `line_number` rośnie raz po udanym odczycie tytułu, na początku pętli, i raz po udanym odczycie statusu. Po nieudanym odczycie statusu nie rośnie, więc `Incomplete record` podaje linię tytułu.
- **Koniec pliku i brak znaku końca linii:** pętlę kończy tylko nieudany odczyt tytułu. Ostatnia linia bez znaku końca linii jest zwykłym, udanym odczytem i nie wymaga osobnego kodu.
- **Podsumowania:** `print_report` przechodzi po wektorze raz. Każdy seans zwiększa dokładnie jeden licznik: `if`, `else if` i `else`. Gałąź `else` obejmuje `cancelled`, bo do wektora trafiają tylko seanse z dozwolonym statusem.
- **Bez częściowego raportu:** `main` wywołuje `print_report` tylko po `true`. Po `false` wektor może zawierać wcześniejsze seanse, ale nic z niego nie jest wypisywane.
- **Inne poprawne rozwiązania:** inne nazwy; sprawdzenie statusu wprost w warunku zamiast osobnej funkcji; podsumowania liczone w osobnej funkcji albo w `main`; pętla z flagą `bool`, jak w lekcji 7.4; typ i deklaracje we własnym nagłówku, a funkcje w osobnych plikach `.cpp`, jak w Module 11. Ważne, żeby licznik rósł tylko po udanym odczycie, a raport powstawał dopiero na końcu.

</details>

## Diagnostyka: wyjaśnienie i poprawka

<details>
<summary>Otwórz po wykonaniu diagnostyki</summary>

Cały program z błędem to rozwiązanie referencyjne z jedną przestawioną linią: `++line_number;` stoi zaraz po odczycie statusu. Jego wyniki są sprawdzane automatycznie.

<!-- example: screenings_counter_bug -->
```cpp
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

struct Screening {
    std::string title;
    std::string status;
};

bool is_allowed_status(const std::string& status) {
    return status == "available" || status == "full" || status == "cancelled";
}

bool read_screenings(std::istream& input, std::vector<Screening>& screenings, std::string& error, int& error_line) {
    int line_number{0};
    std::string title{};
    std::getline(input, title);

    while (!input.fail()) {
        ++line_number;

        if (title.empty()) {
            error = "empty";
            error_line = line_number;
            return false;
        }

        std::string status{};
        std::getline(input, status);
        ++line_number;

        if (input.fail()) {
            error = "incomplete";
            error_line = line_number;
            return false;
        }

        if (status.empty()) {
            error = "empty";
            error_line = line_number;
            return false;
        }

        if (!is_allowed_status(status)) {
            error = "invalid";
            error_line = line_number;
            return false;
        }

        screenings.push_back(Screening{title, status});
        std::getline(input, title);
    }

    return true;
}

void print_report(const std::vector<Screening>& screenings) {
    int available_total{0};
    int full_total{0};
    int cancelled_total{0};
    std::cout << "Screenings: " << screenings.size() << "\n";

    for (const Screening& screening : screenings) {
        std::cout << screening.title << ": " << screening.status << "\n";

        if (screening.status == "available") {
            ++available_total;
        } else if (screening.status == "full") {
            ++full_total;
        } else {
            ++cancelled_total;
        }
    }

    std::cout << "Available total: " << available_total << "\n";
    std::cout << "Full total: " << full_total << "\n";
    std::cout << "Cancelled total: " << cancelled_total << "\n";
}

int main() {
    std::ifstream screenings_file{"screenings.txt"};

    if (screenings_file.fail()) {
        std::cout << "Cannot open screenings.txt\n";
        return 0;
    }

    std::vector<Screening> screenings{};
    std::string error{};
    int error_line{0};
    const bool complete{read_screenings(screenings_file, screenings, error, error_line)};

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

    print_report(screenings);
}
```

Dla F:

<!-- run: screenings_counter_bug -->

<!-- datafile: screenings_counter_bug screenings.txt -->
```text
Morning Birds
```

<!-- output: screenings_counter_bug -->
```text
Incomplete record on line 2
```

Dla G, czyli tego samego tytułu bez znaku końca linii:

<!-- run: screenings_counter_bug -->

<!-- datafile: screenings_counter_bug screenings.txt noeol -->
```text
Morning Birds
```

<!-- output: screenings_counter_bug -->
```text
Incomplete record on line 2
```

Dla O, gdzie brakuje statusu drugiego seansu:

<!-- run: screenings_counter_bug -->

<!-- datafile: screenings_counter_bug screenings.txt -->
```text
Morning Birds
available
Evening Stories
```

<!-- output: screenings_counter_bug -->
```text
Incomplete record on line 4
```

Dla A, czyli poprawnego pliku:

<!-- run: screenings_counter_bug -->

<!-- datafile: screenings_counter_bug screenings.txt -->
```text
Morning Birds
available
Northern Lights
full
Evening Stories
cancelled
```

<!-- output: screenings_counter_bug -->
```text
Screenings: 3
Morning Birds: available
Northern Lights: full
Evening Stories: cancelled
Available total: 1
Full total: 1
Cancelled total: 1
```

1. **Program wypisuje `Incomplete record on line 2`.** Odczyt statusu się nie udaje, ale licznik już urósł z 1 do 2.
2. **Ten numer jest niepoprawny,** bo plik ma tylko jedną linię. Linii 2 nie ma, więc nie można jej poprawić. Rekord zaczął się w linii 1 i to po niej trzeba dopisać status.
3. **Problem powoduje `++line_number;` zaraz po `std::getline(input, status);`,** przed sprawdzeniem `input.fail()`.
4. **Najmniejsza poprawka:** przenieś `++line_number;` za blok `if (input.fail())`:

<!-- fragment -->
```cpp
std::getline(input, status);

if (input.fail()) {
    error = "incomplete";
    error_line = line_number;
    return false;
}

++line_number;
```

5. **Po poprawce** program dla F wypisuje `Incomplete record on line 1`, jak rozwiązanie referencyjne w części B.
6. **Licznik liczy linie, które istnieją w pliku.** Nieudany odczyt nie dostarcza żadnej linii, więc nie ma czego liczyć. Licznik zwiększony mimo to wskazuje linię, której nie ma.
7. **Błąd zmienia wynik tylko przy niekompletnym rekordzie:** w części B dla F, a w pełnej liście także dla G (`line 2`) i O (`line 4`, choć plik ma trzy linie). Po udanym odczycie statusu licznik rośnie raz w obu wersjach, więc dla A, M i pozostałych przypadków wynik jest taki sam. Dlatego sam przypadek A nie wykrywa tego błędu: testy muszą obejmować także przypadki błędne, a wśród nich każdy rodzaj błędu.

</details>

## Odpowiedzi do pytań z części C

<details>
<summary>Przykładowe odpowiedzi, dla rozwiązania referencyjnego</summary>

1. Bo funkcja ma czytać z każdego strumienia wejścia: z otwartego pliku i ze `std::cin`. `std::ifstream` przez wartość wiązałby ją z plikiem, a strumienia i tak nie wolno kopiować (lekcja 12.2). Referencja pozwala czytać z tego samego strumienia, który przygotował `main`.
2. Bo specyfikacja dopuszcza zero rekordów. Pierwszy odczyt tytułu się nie udaje w miejscu, w którym zaczynałby się rekord, a to jest poprawny koniec danych. Pusty plik nie zawiera żadnej linii, więc nie zawiera też pustej linii.
3. Bo pusta linia jest w pliku: `std::getline` ją odczytuje, `fail()` daje `false`, a za nią mogą być kolejne seanse. Dane kończy tylko nieudany odczyt tytułu. Gdyby pusta linia kończyła dane, seanse za nią zniknęłyby bez komunikatu.
4. Po każdym udanym `std::getline`: raz po tytule i raz po statusie. Nigdy po nieudanym odczycie.
5. Bo linii statusu w pliku nie ma, a rekord zaczął się w linii tytułu. To ostatnia istniejąca linia i to po niej trzeba dopisać status.
6. Bo do wektora trafiają tylko seanse z jednym z trzech dozwolonych statusów, a każdy seans zwiększa dokładnie jeden licznik: `if`, `else if` i `else`.
7. Bo częściowy raport wyglądałby jak pełny, choć część pliku jest błędna albo nieprzeczytana. `main` wywołuje `print_report` dopiero wtedy, gdy `read_screenings` zwróci `true`.
8. Program otwiera `screenings.txt` przez ścieżkę względną, więc szuka pliku w swoim katalogu roboczym, a nie obok `main.cpp`. W CLionie katalog roboczy ustawia pole **Working directory**, a w terminalu jest nim katalog, z którego uruchamiasz program (lekcja 12.1).
9. Wywołując ją ze `std::cin` zamiast otwartego pliku: `read_screenings(std::cin, screenings, error, error_line)`. Funkcja się nie zmienia, bo zna tylko `std::istream&`. Zmienia się tylko argument w `main`, a reguły odczytu zostają te same.

</details>

## Samoocena

Przy każdej kompetencji zaznacz jedną odpowiedź:

| Kompetencja | Samodzielnie | Z podpowiedzią | Po zajrzeniu do rozwiązania | Do powtórki |
|---|---|---|---|---|
| Plan danych, odczytu i odpowiedzialności | | | | |
| Plik danych, katalog roboczy i nieudane otwarcie | | | | |
| Funkcja odczytu z `std::istream&` | | | | |
| Koniec pliku a pusta linia | | | | |
| Numery fizycznych linii | | | | |
| Pusta linia, niedozwolony status, niekompletny rekord | | | | |
| Pierwszy błąd bez częściowego raportu | | | | |
| Raport z trzema podsumowaniami | | | | |
| Przypadki normalne, graniczne i błędne | | | | |
| Diagnostyka licznika linii | | | | |

Jeśli w kolumnie „Do powtórki” jest coś zaznaczone, wróć do odpowiedniej lekcji:

| Temat | Lekcja |
|---|---|
| plik danych, `std::ifstream`, katalog roboczy, nieudane otwarcie | [12.1](lesson_01_first_data_file.md) |
| funkcja odczytu z `std::istream&`, kto otwiera plik, strumień przez referencję | [12.2](lesson_02_records_from_a_file.md) |
| koniec pliku, puste linie, numery linii, trzy rodzaje błędów | [12.3](lesson_03_end_of_data_and_errors.md) |
| rekordy w wektorze, raport po odczycie | [10.3](../module_10_input_records/lesson_03_building_a_vector_of_records.md) |

---

## Podsumowanie Modułu 12

Po czterech lekcjach potrafisz:

- otwierać plik tekstowy przez `std::ifstream`, sprawdzać otwarcie i rozumieć, gdzie program szuka pliku podanego ścieżką względną;
- odróżniać nieudane otwarcie od nieudanego odczytu, a pusty plik od brakującego;
- pisać funkcję odczytu z parametrem `std::istream&`, która działa z plikiem i ze `std::cin`;
- kończyć dane wyłącznie na końcu pliku i odróżniać go od pustej linii, także przy ostatniej linii bez znaku końca linii;
- numerować fizyczne linie i wskazywać pustą linię, niedozwoloną wartość i niekompletny rekord;
- wypisywać raport dopiero po sprawdzeniu całego pliku, bez częściowego raportu po błędzie.

## Co dalej

To koniec Modułu 12 i wszystkich jego zaplanowanych lekcji. Kolejne moduły kursu są w przygotowaniu.

**Poprzednia lekcja:** [Lekcja 12.3: Gdzie kończą się dane i gdzie jest błąd](lesson_03_end_of_data_and_errors.md) · **Następna lekcja:** w przygotowaniu · [Opis kursu](../../README.md)

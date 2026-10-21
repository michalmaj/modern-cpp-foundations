# Lekcja 2.3: Zobacz, co dzieje się w programie

**Polski** · [English](lesson_03_see_what_happens_in_the_program.en.md) · [Opis kursu](../../README.md)

> **Moduł 2, lekcja 3** · około 60 minut
> **Potrzebujesz:** katalogu `cpp-workspace`, oryginalnego projektu `lesson_05_first_program` i CLiona z toolchainem `LLVM 22` z lekcji 0.5.
> **Wersja pilotażowa.** Programy z tej lekcji sprawdzamy automatycznie na Windowsie, Ubuntu i macOS. Kroki obsługi debuggera przygotowaliśmy według dokumentacji CLiona 2026.2, ale nie sprawdziliśmy ich jeszcze ręcznie we wszystkich konfiguracjach. Jeśli debugger nie działa w Twoim środowisku, prześledzisz wartości metodą z `std::cout` z punktu 8 i też ukończysz tę lekcję.

## Zanim zaczniesz

Ta lekcja zakłada, że po lekcji 2.2:

- rozumiesz, że przypisanie `total = total + 4;` najpierw oblicza prawą stronę, a potem zastępuje starą wartość zmiennej;
- umiesz wypełnić tabelę wartości zmiennych po kolejnych instrukcjach;
- umiesz dopisać `std::cout`, żeby sprawdzić wartość po każdym kroku;
- otwierasz projekt w CLionie i budujesz go w profilu **Debug**, jak w lekcji 0.5.

## Sytuacja

Program, który się buduje i uruchamia, nie musi działać poprawnie. Czasem kompilator niczego nie zgłasza, a wynik i tak jest zły. Wiesz wtedy, **że** coś jest nie tak, ale nie wiesz, **gdzie**. Dziś poznasz **debugger**: narzędzie, które zatrzymuje program w wybranym miejscu i pokazuje wartości zmiennych, a potem pozwala wykonywać go instrukcja po instrukcji. Twoje przewidywanie porównasz z tym, co program naprawdę robi.

Po tej lekcji będziesz:

- wyjaśniać, do czego służy debugger i czym jest breakpoint;
- odróżniać zwykłe uruchomienie (**Run**) od uruchomienia pod debuggerem (**Debug**);
- rozumieć, dlaczego do debugowania potrzebna jest konfiguracja Debug;
- zatrzymywać program przed wybraną instrukcją i odczytywać wartości zmiennych;
- wykonywać program krok po kroku przyciskiem **Step Over** i obserwować zmiany wartości;
- znajdować pierwszą instrukcję, po której stan programu różni się od przewidywania;
- poprawiać błąd logiczny i sprawdzać wynik;
- szukać takiego błędu także bez debuggera, wypisując wartości.

## 1. Przygotuj projekt

W `cpp-workspace` utwórz katalog `lesson_2_3` i skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program`.

Tym razem będziesz korzystać z debuggera, więc otwórz ten katalog w CLionie, jak w lekcji 1.1: **File | Open**, wskaż `cpp-workspace/lesson_2_3`, wybierz **This Window**, potem **Trust Project**, a w oknie **CMake Profiles** zatwierdź profil **Debug** (**OK**).

## 2. Najpierw przewidywanie: paragon

Kasa w małym sklepie liczy paragon. Klient kupuje chleb za 4 zł, mleko za 6 zł i ser za 7 zł, a na koniec oddaje kupon rabatowy na 2 zł. Ktoś napisał do tego program. Zastąp zawartość `main.cpp` tym kodem, ale **jeszcze go nie uruchamiaj**:

<!-- example: receipt_bug -->
```cpp
#include <iostream>

int main() {
    const int bread_price{4};
    const int milk_price{6};
    const int cheese_price{7};
    const int coupon{2};
    int total{0};

    total = total + bread_price;
    total = total + milk_price;
    total = cheese_price;
    total = total - coupon;

    std::cout << "To pay: " << total << "\n";
}
```

Przeczytaj kod. Przepisz tabelę i wpisz w niej, ile **powinno** wynosić `total` po każdej instrukcji, żeby paragon był policzony poprawnie:

| Instrukcja | Oczekiwane `total` po wykonaniu |
|---|---|
| `int total{0};` | 0 |
| `total = total + bread_price;` | |
| `total = total + milk_price;` | |
| `total = cheese_price;` | |
| `total = total - coupon;` | |

Jeśli już teraz coś wydaje Ci się podejrzane, zanotuj to. Za chwilę to sprawdzisz.

Teraz zbuduj i uruchom program (**Run**). Porównaj wynik z ostatnim wierszem tabeli.

<details>
<summary>Wynik programu</summary>

<!-- output: receipt_bug -->
```text
To pay: 5
```

</details>

Program się zbudował, kompilator nic nie zgłosił, a wynik i tak nie zgadza się z paragonem. To **błąd logiczny**: program robi coś innego, niż miał robić. Sam wynik końcowy mówi tylko, **że** coś jest źle. Każda z czterech instrukcji mogła zawinić.

**W którym momencie wartość `total` stała się nieprawidłowa?**

Odpowiedź znajdziesz za pomocą debuggera.

## 3. Debugger, breakpoint i konfiguracja Debug

**Debugger** to narzędzie, które uruchamia Twój program pod kontrolą. Może go zatrzymać, pokazać aktualne wartości zmiennych, a potem wykonywać dalej, po jednej instrukcji.

- **Run** uruchamia program zwyczajnie: wykonuje się od początku do końca, bez zatrzymywania.
- **Debug** uruchamia program pod debuggerem. Program zatrzyma się w miejscach, które wskażesz.
- **Breakpoint** (punkt przerwania) to znacznik przy instrukcji, który mówi: „zatrzymaj się, **zanim** wykonasz tę instrukcję”.

**Dlaczego konfiguracja Debug?** W lekcji 0.5 budujesz program w profilu CMake **Debug**. W tej konfiguracji kompilator dołącza do programu dodatkowe **informacje dla debuggera**: która część skompilowanego programu odpowiada której linijce kodu i gdzie są zmienne. Bez nich debugger nie wie, gdzie jest Twoja instrukcja. Konfiguracja **Release** jest przygotowana do szybkiego działania: kompilator może w niej przestawiać i łączyć instrukcje i domyślnie nie dołącza tych informacji. Do szukania błędów używaj więc zawsze profilu Debug.

## 4. Sprawdź ustawienia przed pierwszą sesją

**1. Właściwy projekt.** U góry okna CLiona sprawdź, że otwarty jest projekt z katalogu `lesson_2_3`, a w edytorze plik `main.cpp` z paragonem.

**2. Profil CMake Debug.** Otwórz okno **CMake** i sprawdź dwie rzeczy, jak w lekcji 0.5, punkt 5: kompilator to `Clang 22` (lub nowszy), a polecenie na samej górze zawiera `-DCMAKE_BUILD_TYPE=Debug`.

**3. Profil debugowania.** Uwaga na dwie podobne nazwy:

- **profil CMake Debug** (z lekcji 0.5) mówi, **jak zbudować** program;
- **profil debugowania** (*Debug Profile*) mówi, **którym debuggerem** go śledzić.

W głównym pasku narzędzi, obok wyboru programu do uruchomienia, jest przełącznik z napisem `Debug | <nazwa profilu>`. Pokazuje profil debugowania, którego CLion użyje w następnej sesji. Wszystkie profile znajdziesz w ustawieniach (na Windowsie i Ubuntu **File | Settings**, na macOS **CLion | Settings**): **Build, Execution, Deployment | Debugger | Debug Profiles**.

### Ubuntu

CLion sam przygotowuje domyślny profil z wbudowanym debuggerem **GDB**. Niczego nie zmieniaj.

### macOS

CLion sam przygotowuje domyślny profil z wbudowanym debuggerem **LLDB**. Niczego nie zmieniaj.

### Windows

Na Windowsie `clang++` zapisuje informacje dla debuggera w formacie Microsoftu (w pliku `.pdb`). CLion ma do nich wbudowany debugger oparty na **LLDB**, przygotowany dla toolchainu Visual Studio. Potrzebujesz więc profilu typu **LLDB**, a nie GDB. Najpewniej będzie utworzyć taki profil samodzielnie i nadać mu własną nazwę. Wtedy wiesz, jakiego jest typu:

1. W ustawieniach otwórz **Build, Execution, Deployment | Debugger | Debug Profiles**.
2. W części **General-purpose debuggers** kliknij kafelek **LLDB**. CLion doda do listy nowy profil tego typu.
3. W polu **Name** wpisz na przykład `LLDB Visual Studio`. Pole **Executable** jest dla LLDB na Windowsie niedostępne: CLion używa swojego wbudowanego LLDB.
4. Zaznacz **Available for all projects**, żeby ten profil był dostępny także w kolejnych projektach.
5. Kliknij **OK**.
6. W przełączniku w pasku narzędzi wybierz `Debug | LLDB Visual Studio`.

W ustawieniach toolchainu (**Toolchains**) jest też starsze pole **Debugger**. W CLionie 2026.2 to ustawienie jest przestarzałe: o tym, którego debuggera użyje sesja, decyduje profil debugowania. Nie zmieniaj go.

**Jeśli w lekcji 0.5 użyto toolchainu System zamiast Visual Studio,** nie mamy potwierdzenia, że debugger będzie w tej konfiguracji działał. Spróbuj kroków z punktu 5. Jeśli program się nie zatrzyma, nie zmieniaj toolchainu, tylko przejdź do punktu 8.

## 5. Pierwsza sesja z debuggerem

**Krok 1. Postaw breakpoint.** Znajdź w edytorze instrukcję `total = total + bread_price;`. Kliknij w lewy margines edytora (pasek z numerami linijek) na jej wysokości. Pojawi się tam znacznik breakpointu. Ponowne kliknięcie usuwa go.

Stawiaj breakpoint zawsze przy linijce z instrukcją, nie przy pustej linijce ani przy `}`. Tutaj wybrana instrukcja stoi pod wszystkimi deklaracjami, więc każda zmienna ma już wartość początkową.

**Krok 2. Uruchom pod debuggerem.** Kliknij przycisk **Debug** w górnym pasku narzędzi albo wybierz z menu **Run | Debug '…'** (w cudzysłowie jest nazwa programu). Nie klikaj **Run**: przy zwykłym uruchomieniu program się nie zatrzyma. CLion zbuduje program, jeśli trzeba, uruchomi go pod debuggerem i zatrzyma przy breakpoincie. Sesję obsługujesz w oknie **Debug** na dole ekranu. Jeśli go nie widać, otwórz je przez **View | Tool Windows | Debug**.

**Krok 3. Zrozum niebieską linię.** To najważniejsza rzecz w tej lekcji.

> Linijka z breakpointem jest teraz wyróżniona na niebiesko. To **aktualny punkt wykonania**: instrukcja, która wykona się **jako następna**. Program zatrzymał się **przed** nią. **Ta instrukcja jeszcze się nie wykonała.**

**Krok 4. Odczytaj wartość.** W oknie **Debug** otwórz zakładkę **Variables** i znajdź w niej `total`. Najpierw przewidź: jaką wartość ma teraz `total`? Dopiero potem spójrz.

<details>
<summary>Co powinno być widać i dlaczego</summary>

`total` ma wartość **0**, choć niebieska instrukcja dodaje cenę chleba. Nic się nie zepsuło: ta instrukcja jeszcze się nie wykonała. Wykonało się tylko to, co stoi nad nią, a tam `total` dostało wartość początkową 0.

</details>

W zakładce **Variables** mogą być też inne zmienne, na przykład ceny. Dziś obserwujesz tylko `total`. CLion może pokazywać wartości zmiennych także w samym edytorze, obok kodu.

**Krok 5. Wykonaj jedną instrukcję.** Na pasku narzędzi okna **Debug** znajdź przycisk **Step Over** (nazwa przycisku pojawi się po najechaniu na niego kursorem). Kliknij go **raz**. Niebieska instrukcja się wykona, a niebieska linia przejdzie do następnej instrukcji. Sprawdź `total` w zakładce **Variables**: teraz widzisz wartość **po** wykonaniu instrukcji.

**Krok 6. Krok po kroku, aż do pierwszej różnicy.** Przepisz tę tabelę. W kolumnie „oczekiwane” wpisz wartości z tabeli z punktu 2. Przed każdym kliknięciem **Step Over** zapisz, ile `total` ma **teraz**, a po kliknięciu zapisz nową wartość.

| Instrukcja na niebiesko (jeszcze niewykonana) | `total` teraz | Oczekiwane `total` po wykonaniu | `total` po **Step Over** |
|---|---|---|---|
| `total = total + bread_price;` | | | |
| `total = total + milk_price;` | | | |
| `total = cheese_price;` | | | |
| `total = total - coupon;` | | | |

Wartość „po” z jednego wiersza to wartość „teraz” w następnym. Szukasz **pierwszego** wiersza, w którym ostatnia kolumna różni się od oczekiwanej. Instrukcja z tego wiersza jako pierwsza dała zły wynik.

**Krok 7. Zakończ sesję.** Gdy niebieska linia dojdzie do instrukcji ze `std::cout`, przestań klikać **Step Over**. Kliknij **Resume Program** (przycisk na pasku narzędzi okna **Debug** albo menu **Run | Debugging Actions | Resume Program**). Program wykona resztę instrukcji bez zatrzymywania, bo nie ma już dalszych breakpointów, i się zakończy. Jeśli chcesz przerwać sesję wcześniej, kliknij **Stop** na pasku narzędzi okna **Debug**.

Nie klikaj **Step Over** za ostatnią instrukcją programu. Debugger mógłby wtedy przejść do kodu, który uruchamia i kończy programy i nie pochodzi z Twojego pliku. Jeśli zobaczysz nieznany plik albo kod, którego nie piszesz, kliknij **Stop**.

Wypełniona tabela i wyjaśnienie są w części [Przykładowe rozwiązania](#przykładowe-rozwiązania). Zajrzyj tam po własnej próbie.

## 6. Popraw i sprawdź

Gdy wiesz już, która instrukcja zawiniła, popraw ją. Przypomnij sobie z lekcji 2.2, że przypisanie **zastępuje** starą wartość zmiennej. Co ta instrukcja miała zrobić z dotychczasową sumą?

Po poprawce uruchom program zwyczajnie (**Run**). Wynik ma być taki:

<!-- output: receipt_fixed -->
```text
To pay: 15
```

<details>
<summary>Poprawiony program</summary>

<!-- example: receipt_fixed -->
```cpp
#include <iostream>

int main() {
    const int bread_price{4};
    const int milk_price{6};
    const int cheese_price{7};
    const int coupon{2};
    int total{0};

    total = total + bread_price;
    total = total + milk_price;
    total = total + cheese_price;
    total = total - coupon;

    std::cout << "To pay: " << total << "\n";
}
```

</details>

Jeśli chcesz, uruchom poprawiony program jeszcze raz pod debuggerem z tym samym breakpointem. Po trzecim **Step Over** `total` ma teraz 17, tak jak w tabeli z punktu 2.

## 7. Co dał debugger

Wynik `To pay: 5` mówił tylko, że coś jest źle. Debugger pozwolił zatrzymać program przed podejrzanymi instrukcjami, zobaczyć wartość **przed** i **po** każdej z nich i porównać ją z przewidywaniem. Pierwsza różnica wskazała konkretną instrukcję. Nie trzeba było przy tym zmieniać kodu.

Debugger nie naprawia programu: pokazuje, co program robi. Decyzja, co poprawić, należy do Ciebie.

## 8. Gdy debugger nie działa: śledzenie z `std::cout`

Ta metoda przyda się, jeśli w Twoim środowisku:

- program uruchomiony przez **Debug** nie zatrzymuje się przy breakpoincie;
- CLion oznacza breakpoint jako nieprawidłowy (*invalid*);
- zakładka **Variables** jest pusta;
- nie da się wybrać właściwego profilu debugowania.

Znasz ją z lekcji 2.2, punkt 5. Wykonaj ją na programie z paragonem, w wersji **z błędem**:

1. Przygotuj tabelę oczekiwanych wartości z punktu 2.
2. Pod każdym przypisaniem do `total` dopisz instrukcję, która wypisze aktualną wartość, na przykład:

<!-- fragment -->
```cpp
std::cout << "total: " << total << "\n";
```

3. Zbuduj i uruchom program (**Run**).
4. Porównaj każdy wypisany wiersz `total: …` z odpowiednim wierszem tabeli.
5. Znajdź pierwszy wiersz, który się nie zgadza. Przypisanie tuż nad dopisanym `std::cout`, który go wypisał, jako pierwsze dało zły wynik.
6. Usuń tymczasowe instrukcje `std::cout`, które dopisano.
7. Popraw błędną instrukcję.
8. Uruchom program jeszcze raz i sprawdź, czy wypisuje `To pay: 15`.

<details>
<summary>Program z dopisanym wypisywaniem i jego wynik</summary>

<!-- example: receipt_trace -->
```cpp
#include <iostream>

int main() {
    const int bread_price{4};
    const int milk_price{6};
    const int cheese_price{7};
    const int coupon{2};
    int total{0};

    total = total + bread_price;
    std::cout << "total: " << total << "\n";
    total = total + milk_price;
    std::cout << "total: " << total << "\n";
    total = cheese_price;
    std::cout << "total: " << total << "\n";
    total = total - coupon;
    std::cout << "total: " << total << "\n";

    std::cout << "To pay: " << total << "\n";
}
```

<!-- output: receipt_trace -->
```text
total: 4
total: 10
total: 7
total: 5
To pay: 5
```

Trzeci wiersz to 7, a oczekiwane było 17. Zły wynik dało więc trzecie przypisanie, `total = cheese_price;`.

</details>

**Czym ta metoda różni się od debuggera?** Wypisywanie wartości pozwala prześledzić, jak zmieniają się wartości, ale **nie jest pełnym odpowiednikiem** debuggera:

- **wymaga zmiany kodu**, który badasz: łatwo przy tym zrobić nowy błąd, a dopisane linijki trzeba potem usunąć;
- **pokazuje tylko to, co wybierzesz** do wypisania, a debugger pokazuje wartości wszystkich zmiennych w miejscu zatrzymania;
- **nie zatrzymuje programu**: nie możesz się zatrzymać, przyjrzeć i zdecydować, co sprawdzić dalej;
- **nie uczy obsługi debuggera**, z którego będziesz korzystać w kolejnych lekcjach.

Jeśli korzystasz z tej metody, bo debugger w Twoim środowisku nie działa, możesz spokojnie przejść dalej w Module 2. Obsługę debuggera uzupełnisz później, gdy zacznie działać.

## 9. Misja: szkolna biblioteka

W klasowej bibliotece na półce stoi 20 książek, a wypożyczonych nie ma żadnej. W ciągu dnia:

- rano uczniowie wypożyczają 6 książek;
- w południe oddają 4 książki;
- po południu wypożyczają jeszcze 3.

Program ma wypisać, ile książek jest na koniec dnia na półce, a ile jest wypożyczonych. Ktoś go napisał, ale wynik jest zły.

W `cpp-workspace` utwórz katalog `school_library`, skopiuj do niego `CMakeLists.txt` i `main.cpp` z oryginalnego `lesson_05_first_program`, a zawartość `main.cpp` zastąp tym programem. Otwórz katalog w CLionie.

<!-- example: library_bug -->
```cpp
#include <iostream>

int main() {
    const int morning_loans{6};
    const int returns{4};
    const int afternoon_loans{3};
    int on_shelf{20};
    int borrowed{0};

    on_shelf = on_shelf - morning_loans;
    borrowed = borrowed + morning_loans;
    on_shelf = on_shelf + returns;
    borrowed = borrowed + returns;
    on_shelf = on_shelf - afternoon_loans;
    borrowed = borrowed + afternoon_loans;

    std::cout << "On the shelf: " << on_shelf << "\n";
    std::cout << "Borrowed: " << borrowed << "\n";
}
```

Tym razem decyzje należą do Ciebie:

1. Na podstawie opisu dnia **przewidź** i zapisz w tabeli, ile powinny wynosić `on_shelf` i `borrowed` po każdej instrukcji.
2. Uruchom program (**Run**) i porównaj wynik z ostatnim wierszem tabeli.
3. Wybierz, gdzie zatrzymać program, i znajdź pierwszą instrukcję, po której wartość różni się od przewidywania: debuggerem albo metodą z `std::cout`.
4. Popraw błąd i sprawdź wynik.

<details>
<summary>Wynik programu z błędem</summary>

<!-- output: library_bug -->
```text
On the shelf: 15
Borrowed: 13
```

</details>

### Kryterium sukcesu

- Tabela przewidywanych wartości obu zmiennych po każdej instrukcji jest wypełniona **przed** szukaniem błędu.
- Wiesz, która instrukcja jako pierwsza dała zły wynik, i jaką wartość miała zmienna tuż po niej.
- Poprawka zmienia tylko tę jedną instrukcję.
- Po poprawce program buduje się jako C++20 i wypisuje wynik zgodny z opisem dnia. Sprawdź go dopiero po własnym przewidywaniu:

<details>
<summary>Oczekiwany wynik po poprawce</summary>

<!-- output: library_fixed -->
```text
On the shelf: 15
Borrowed: 5
```

</details>

- Umiesz wyjaśnić, dlaczego ta instrukcja dawała zły wynik.

Gdy wynik się zgadza, możesz zapisać projekt w Gicie, jak w lekcji 1.5.

<details>
<summary>Podpowiedź 1</summary>

Która zmienna ma na końcu złą wartość? Breakpoint możesz postawić przy pierwszej instrukcji, która ją zmienia, albo po prostu przy pierwszym przypisaniu.

</details>

<details>
<summary>Podpowiedź 2</summary>

Książek na półce i wypożyczonych jest razem zawsze 20. Po każdej instrukcji, która dotyczy jednego zdarzenia, możesz to sprawdzić.

</details>

### Samoocena

Zaznacz, co pasuje do Twojej pracy:

- Błąd udało mi się znaleźć za pomocą **debuggera**.
- Błąd udało mi się znaleźć, **wypisując wartości** przez `std::cout`.
- Do znalezienia błędu potrzebne były **podpowiedzi** albo **przykładowe rozwiązanie**.

Każda z tych dróg jest w porządku. Jeśli debugger nie był dostępny, obsługa debuggera zostaje Ci do uzupełnienia później. Jeśli potrzebne było rozwiązanie, wróć do misji za kilka dni i spróbuj jeszcze raz.

## 10. Gdy coś pójdzie inaczej

| Co widzisz | Co to znaczy | Co zrobić |
|---|---|---|
| Program wykonuje się do końca i się nie zatrzymuje | Uruchomiono **Run** zamiast **Debug** albo nie ma breakpointu. | Postaw breakpoint przy instrukcji i uruchom przez **Debug**. |
| CLion oznacza breakpoint jako nieprawidłowy (*invalid*) albo program uruchomiony przez **Debug** się nie zatrzymuje | Debugger nie umie dopasować breakpointu do programu: linijka nie zawiera instrukcji, program nie jest zbudowany w profilu Debug albo, na Windowsie, aktywny profil debugowania nie jest typu LLDB. | Przenieś breakpoint na instrukcję. Sprawdź punkt 4. Jeśli to nie pomoże, użyj metody z punktu 8. |
| Przy pierwszym zatrzymaniu `total` ma 0, a nie 4 | Tak ma być: niebieska instrukcja jeszcze się nie wykonała. | Kliknij **Step Over** i sprawdź wartość ponownie. |
| Na Windowsie przełącznik pokazuje profil typu GDB | Do formatu, w którym `clang++` zapisuje na Windowsie informacje dla debuggera, CLion przewiduje wbudowany LLDB. | Wybierz profil LLDB utworzony w punkcie 4. |
| Po **Step Over** otwiera się nieznany plik albo kod, którego nie piszesz | Debugger przeszedł za ostatnią instrukcję Twojego programu. | Kliknij **Stop**. Następnym razem zakończ sesję przez **Resume Program**, gdy niebieska linia dojdzie do `std::cout`. |
| Debugger pokazuje kod z innego ćwiczenia | W CLionie jest otwarty inny projekt. | Otwórz właściwy katalog (**File \| Open**). |
| Po poprawce wynik jest nadal zły | Poprawiono inną instrukcję niż ta, która zawiniła, albo pojawiła się nowa pomyłka. | Wróć do tabeli i jeszcze raz znajdź pierwszą różnicę. |

## 11. Wyjaśnij

Odpowiedz własnymi słowami, najlepiej na piśmie. Dopiero potem porównaj z przykładową odpowiedzią.

**1.** Czym różni się uruchomienie przez **Run** od uruchomienia przez **Debug**?

<details>
<summary>Przykładowa odpowiedź</summary>

**Run** wykonuje program od początku do końca bez zatrzymywania. **Debug** uruchamia go pod debuggerem, który zatrzymuje program przy breakpointach i pozwala oglądać wartości zmiennych oraz wykonywać instrukcje po kolei.

</details>

**2.** Co oznacza niebieska linia w edytorze podczas sesji debugowania? Czy ta instrukcja już się wykonała?

<details>
<summary>Przykładowa odpowiedź</summary>

To aktualny punkt wykonania: instrukcja, która wykona się jako następna. Jeszcze się nie wykonała. Jej efekt widać dopiero po **Step Over**.

</details>

**3.** Dlaczego przy pierwszym zatrzymaniu `total` miało 0, choć breakpoint stał przy instrukcji dodającej cenę chleba?

<details>
<summary>Przykładowa odpowiedź</summary>

Bo program zatrzymuje się **przed** instrukcją z breakpointem. W tej chwili wykonała się tylko inicjalizacja `int total{0};`.

</details>

**4.** Dlaczego sam wynik `To pay: 5` nie wystarczył, żeby wskazać błędną instrukcję?

<details>
<summary>Przykładowa odpowiedź</summary>

Wynik końcowy pokazuje tylko skutek wszystkich instrukcji razem. Każda z nich mogła zawinić. Dopiero porównanie wartości po każdej instrukcji z przewidywaniem wskazało pierwszą, która dała zły wynik.

</details>

**5.** Podaj dwie różnice między szukaniem błędu debuggerem a wypisywaniem wartości przez `std::cout`.

<details>
<summary>Przykładowa odpowiedź</summary>

Na przykład: wypisywanie wymaga zmiany kodu, a debugger nie. Wypisywanie pokazuje tylko wybrane wartości, a debugger wszystkie zmienne w miejscu zatrzymania. Debugger pozwala zatrzymać program, a wypisywanie nie.

</details>

## Podsumowanie

- **Błąd logiczny** to sytuacja, w której program się buduje i działa, ale robi coś innego, niż miał. Kompilator go nie zgłosi.
- **Debugger** uruchamia program pod kontrolą: zatrzymuje go, pokazuje wartości zmiennych i pozwala wykonywać instrukcje po kolei.
- **Breakpoint** zatrzymuje program **przed** wykonaniem wskazanej instrukcji.
- Do debugowania potrzebny jest program zbudowany w konfiguracji **Debug**. Profil debugowania wybiera, którym debuggerem CLion go śledzi.
- **Niebieska linia** to instrukcja, która wykona się jako następna. Jej efekt widać po **Step Over**.
- Szukasz **pierwszej** instrukcji, po której wartość różni się od przewidywania. To tam jest błąd.
- Wypisywanie wartości przez `std::cout` też pozwala znaleźć taką instrukcję, ale wymaga zmiany kodu i nie zastępuje debuggera.

## Co dalej

Umiesz już porównać przewidywanie z tym, co program naprawdę robi, i znaleźć pierwszą złą instrukcję. W lekcji 2.4 poznasz dzielenie liczb całkowitych, resztę z dzielenia i zasady kolejności działań: [Lekcja 2.4: Dzielenie, reszta i kolejność działań](lesson_04_division_remainder_and_order_of_operations.md).

---

## Przykładowe rozwiązania

Zajrzyj tutaj **po własnej próbie**.

<details>
<summary>Punkty 2 i 5: tabele dla paragonu</summary>

Oczekiwane wartości (punkt 2):

| Instrukcja | Oczekiwane `total` po wykonaniu |
|---|---|
| `int total{0};` | 0 |
| `total = total + bread_price;` | 4 |
| `total = total + milk_price;` | 10 |
| `total = cheese_price;` | 17 |
| `total = total - coupon;` | 15 |

Sesja z debuggerem (punkt 5):

| Instrukcja na niebiesko (jeszcze niewykonana) | `total` teraz | Oczekiwane `total` po wykonaniu | `total` po **Step Over** |
|---|---|---|---|
| `total = total + bread_price;` | 0 | 4 | 4 |
| `total = total + milk_price;` | 4 | 10 | 10 |
| `total = cheese_price;` | 10 | 17 | **7** |
| `total = total - coupon;` | 7 | 15 | 5 |

Pierwsza różnica jest w trzecim wierszu: po `total = cheese_price;` `total` ma 7 zamiast 17. To przypisanie **zastępuje** dotychczasową sumę (10) samą ceną sera (7), zamiast ją do niej dodać. Ostatnia instrukcja jest poprawna: odejmuje kupon, ale od złej sumy, dlatego wynik końcowy to 5. Poprawna instrukcja to `total = total + cheese_price;`.

</details>

<details>
<summary>Punkt 9: misja, szkolna biblioteka</summary>

| Instrukcja | `on_shelf` | `borrowed` |
|---|---|---|
| `int on_shelf{20};` i `int borrowed{0};` | 20 | 0 |
| `on_shelf = on_shelf - morning_loans;` | 14 | 0 |
| `borrowed = borrowed + morning_loans;` | 14 | 6 |
| `on_shelf = on_shelf + returns;` | 18 | 6 |
| `borrowed = borrowed + returns;` | 18 | oczekiwane 2, program daje **10** |
| `on_shelf = on_shelf - afternoon_loans;` | 15 | oczekiwane 2, program daje 10 |
| `borrowed = borrowed + afternoon_loans;` | 15 | oczekiwane 5, program daje 13 |

Pierwsza różnica pojawia się po `borrowed = borrowed + returns;`: `borrowed` ma 10 zamiast 2. Oddane książki wracają na półkę, więc liczba wypożyczonych musi się **zmniejszyć**, a program ją zwiększa. Na półce i u czytelników jest wtedy razem 28 książek, a nie 20. Poprawiony program:

<!-- example: library_fixed -->
```cpp
#include <iostream>

int main() {
    const int morning_loans{6};
    const int returns{4};
    const int afternoon_loans{3};
    int on_shelf{20};
    int borrowed{0};

    on_shelf = on_shelf - morning_loans;
    borrowed = borrowed + morning_loans;
    on_shelf = on_shelf + returns;
    borrowed = borrowed - returns;
    on_shelf = on_shelf - afternoon_loans;
    borrowed = borrowed + afternoon_loans;

    std::cout << "On the shelf: " << on_shelf << "\n";
    std::cout << "Borrowed: " << borrowed << "\n";
}
```

Jego wynik to ten z kryterium sukcesu: `On the shelf: 15` i `Borrowed: 5`.

</details>

**Poprzednia lekcja:** [Lekcja 2.2: Gdy wartości się zmieniają](lesson_02_when_values_change.md) · **Następna lekcja:** [Lekcja 2.4: Dzielenie, reszta i kolejność działań](lesson_04_division_remainder_and_order_of_operations.md) · [Opis kursu](../../README.md)

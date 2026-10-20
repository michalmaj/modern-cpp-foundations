# Lekcja 1.2: Gdy kompilator protestuje

**Polski** · [English](lesson_02_when_the_compiler_complains.en.md) · [Opis kursu](../../README.md)

> **Moduł 1, lekcja 2** · około 60–75 minut
> **Potrzebujesz:** katalogu `cpp-workspace` i oryginalnego projektu `lesson_05_first_program` z [lekcji 1.1](lesson_01_first_program_inside.md).
> **Wersja pilotażowa:** kroki w CLionie opisujemy według dokumentacji CLion 2026.2. W Twojej wersji nazwy przycisków mogą się nieznacznie różnić.

## Zanim zaczniesz

Ta lekcja zakłada, że po lekcji 1.1:

- umiesz skopiować projekt do `cpp-workspace`, otworzyć go w CLionie i sprawdzić, czy jest `Clang 22`;
- rozumiesz instrukcję `std::cout << "…";`: co robią `std::cout`, `<<`, napis w cudzysłowie, `\n` i średnik.

## Sytuacja

Każdy programista codziennie widzi błędy kompilacji. To nie porażka, tylko normalna część pracy. Kompilator nie zgaduje, co miało być w kodzie: gdy czegoś nie rozumie, przerywa budowanie i pisze, **gdzie** i **co** mu nie pasuje.

Dziś celowo popsujesz działający program na trzy sposoby i nauczysz się czytać te komunikaty. Nie chodzi o zapamiętanie trzech poprawek. Chodzi o **sposób pracy**, który zadziała też przy komunikatach, których jeszcze nie znasz:

**zobacz problem → przeczytaj diagnostykę → postaw hipotezę → popraw jedną rzecz → zbuduj ponownie → sprawdź wynik**

*Diagnostyka* to komunikaty, które kompilator wypisuje o problemach w kodzie. *Hipoteza* to Twoje przypuszczenie, co jest przyczyną, zanim je sprawdzisz.

Po tej lekcji będziesz:

- rozpoznawać, że budowanie się nie udało, i odróżniać komunikaty kompilatora od wyniku działającego programu;
- odczytywać z komunikatu nazwę pliku, numer linijki i pozycję w linijce;
- znajdować pierwszą istotną informację wśród wielu linijek wyniku budowania;
- stawiać hipotezę o przyczynie, poprawiać jedną rzecz i sprawdzać efekt;
- wyjaśniać, dlaczego jeden błąd może dać kilka komunikatów;
- wyjaśniać rolę `;`, `#include <iostream>` i `std::` w Twoich programach.

## 1. Przygotuj kopię do eksperymentów

Programy i misja z lekcji 1.1 zostają nietknięte. Do psucia potrzebujesz osobnej kopii:

1. W `cpp-workspace` utwórz katalog `lesson_1_2`.
2. Skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego katalogu kursu `lesson_05_first_program`, tak jak w lekcji 1.1.
3. Otwórz `cpp-workspace/lesson_1_2` w CLionie i sprawdź w oknie CMake, czy jest `Clang 22`.
4. Zastąp całą zawartość `main.cpp` znanym programem z lekcji 1.1:

<!-- example: start -->
```cpp
#include <iostream>

int main() {
    std::cout << "Good morning!\n";
    std::cout << "Time to write some C++.\n";
}
```

5. Zbuduj go poleceniem **Build | Build Project**, a potem kliknij **Run**. Wynik:

<!-- output: start -->
```text
Good morning!
Time to write some C++.
```

W tej lekcji zawsze najpierw **budujesz** (**Build | Build Project**), a **Run** klikasz dopiero wtedy, gdy budowanie się udało. Dzięki temu widzisz osobno, czy problem jest z budowaniem, czy z tym, co wypisuje program.

**Ważne:** kod, który za chwilę zepsujesz, jest częścią ćwiczenia, a nie wzorem do zachowania. Po każdym eksperymencie przywracasz poprawny program.

## 2. Dwa różne problemy

Zanim cokolwiek zepsujesz, odróżnij dwie sytuacje:

| | Program się nie buduje | Program się buduje, ale wypisuje coś innego, niż chcesz |
|---|---|---|
| Co widzisz | W oknie **Build** komunikaty ze słowem `error`. Nowy program nie powstaje. | Budowanie się udaje, a w oknie **Run** jest inny tekst niż oczekiwany. |
| Kto zauważa problem | Kompilator. | Ty, gdy porównasz wynik z oczekiwanym. |
| Przykład | Brakujący średnik. | Literówka w napisie, na przykład `"Good mornign!\n"`, albo brakujące `\n`. |

Kompilator sprawdza, czy kod jest poprawnie zapisanym C++: czy instrukcje mają właściwą formę i czy zna użyte nazwy. **Nie sprawdza, czy program robi to, co chcesz.** Napis z literówką to dla niego zwykły, poprawny napis. Dlatego udane budowanie nie oznacza jeszcze, że program jest dobry: wynik zawsze trzeba sprawdzić.

## 3. Eksperyment A: brakujący średnik (krok po kroku)

**Zmiana.** W linijce 4 usuń średnik na końcu. Twój `main.cpp` wygląda teraz tak:

<!-- broken: no_semicolon at=4:35 errors=1 error=^expected ';' after expression$ -->
```cpp
#include <iostream>

int main() {
    std::cout << "Good morning!\n"
    std::cout << "Time to write some C++.\n";
}
```

**Przewidź:** czy ten program się zbuduje? Zapisz odpowiedź.

CLion może już teraz podkreślić coś na czerwono w edytorze. To CLion analizuje kod na bieżąco, w trakcie pisania. Rozstrzyga jednak dopiero budowanie, więc zbuduj program: **Build | Build Project**.

### Krok 1. Zobacz problem

W oknie **Build** pojawi się wynik budowania, mniej więcej taki:

```text
[3/4] Building CXX object CMakeFiles/first_program.dir/main.cpp.o
FAILED: CMakeFiles/first_program.dir/main.cpp.o
/opt/homebrew/opt/llvm@22/bin/clang++ … -c /Users/ola/cpp-workspace/lesson_1_2/main.cpp
/Users/ola/cpp-workspace/lesson_1_2/main.cpp:4:35: error: expected ';' after expression
    4 |     std::cout << "Good morning!\n"
      |                                   ^
      |                                   ;
1 error generated.
ninja: build stopped: subcommand failed.
```

Szczegóły będą u Ciebie trochę inne: ścieżki, nazwa kompilatora, na Windowsie `main.cpp.obj` zamiast `main.cpp.o`, czasem `FAILED: [code=1]`. To nie ma znaczenia.

Po czym poznać, że budowanie się nie udało? Są słowa `FAILED` i `error`, na końcu `1 error generated.` (wygenerowano 1 błąd) i `build stopped` (budowanie przerwane). Nowy plik wykonywalny nie powstał.

### Krok 2. Przeczytaj diagnostykę

Czytaj od góry i szukaj **pierwszej informacji, która wskazuje miejsce w Twoim kodzie**:

- `[3/4] Building CXX object …`: zwykły krok budowania, jak w lekcji 0.5;
- `FAILED: …`: który krok się nie udał. Tu kompilacja `main.cpp`;
- długa linijka z `clang++`: polecenie, którym uruchomiono kompilator. Możesz ją pominąć;
- **`…/main.cpp:4:35: error: expected ';' after expression`**: to jest ta informacja.

Rozłóż ją na części:

| Część | Znaczenie |
|---|---|
| `…/main.cpp` | Plik, w którym jest problem. |
| `4` | Numer linijki. CLion pokazuje numery linijek po lewej stronie edytora. |
| `35` | Pozycja w linijce (kolumna): 35. znak od lewej, licząc spacje. |
| `error` | Rodzaj komunikatu: błąd, przez który programu nie da się zbudować. |
| `expected ';' after expression` | Opis: „oczekiwano `;` po wyrażeniu”. Wyrażenie to tutaj `std::cout << "Good morning!\n"`. |

Pod spodem kompilator pokazuje tę linijkę kodu. Znak `^` wskazuje pozycję 35, zaraz za cudzysłowem zamykającym, a w linijce niżej kompilator podpowiada, czego tam brakuje: `;`.

### Krok 3. Postaw hipotezę

Na przykład: „W linijce 4 po napisie brakuje średnika, więc kompilator nie wie, gdzie kończy się pierwsza instrukcja”.

Dlaczego to ważne? **Składnia** języka to reguły zapisu kodu, a w C++ instrukcja `std::cout << …` kończy się średnikiem. Przejście do nowej linijki nic dla kompilatora nie znaczy. Bez średnika czyta dalej i dokleja `std::cout` z linijki 5 do pierwszej instrukcji, a to już nie ma sensu.

**Czy wskazane miejsce to zawsze przyczyna?** Tutaj tak: kompilator wskazał dokładnie miejsce, w którym czegoś brakuje. Dlatego pod `^` nie ma żadnego złego znaku, jest puste miejsce. Kompilator zauważa jednak problem dopiero wtedy, gdy coś przestaje pasować, a to bywa później niż sam błąd. Traktuj więc wskazane miejsce jako **początek poszukiwań**: sprawdź je i to, co stoi przed nim. W eksperymencie B zobaczysz, że przyczyna może być w zupełnie innej linijce.

### Krok 4. Popraw jedną rzecz

Dopisz średnik na końcu linijki 4. Nic więcej nie zmieniaj.

### Krok 5. Zbuduj ponownie

**Build | Build Project.** Tym razem w oknie Build nie ma `error`, a ostatni krok to `Linking CXX executable first_program` (na Windowsie `first_program.exe`).

### Krok 6. Sprawdź wynik

Kliknij **Run**. Program wypisuje dwie linijki, tak jak w punkcie 1. Hipoteza się potwierdziła.

## 4. Eksperyment B: kompilator nie zna nazwy

Tym razem więcej pracy wykonasz sam.

**Zmiana.** Zacznij od poprawnego programu. Usuń dwie pierwsze linijki: `#include <iostream>` i pustą linijkę pod nią. Twój `main.cpp`:

<!-- broken: no_include at=2:5 errors=2 error=^use of undeclared identifier 'std'$ -->
```cpp
int main() {
    std::cout << "Good morning!\n";
    std::cout << "Time to write some C++.\n";
}
```

**Przewidź:** czy program się zbuduje? Zbuduj go (**Build | Build Project**).

**Przeczytaj diagnostykę sam.** Znajdź w oknie Build linijki z `main.cpp` i `error` i odpowiedz:

1. Ile jest komunikatów `error`?
2. Których linijek i pozycji dotyczą?
3. Co mówią? Słowo *identifier* znaczy tu „nazwa”, a *undeclared*: „niezadeklarowana”, czyli taka, której kompilator nie zna.

<details>
<summary>Sprawdź odpowiedzi</summary>

```text
…/main.cpp:2:5: error: use of undeclared identifier 'std'
…/main.cpp:3:5: error: use of undeclared identifier 'std'
2 errors generated.
```

1. Dwa.
2. Linijka 2, pozycja 5, i linijka 3, pozycja 5: w obu miejscach zaczyna się `std`.
3. „Użyto nazwy `std`, której kompilator nie zna”.

</details>

**Postaw hipotezę, zanim poprawisz.** Komunikaty wskazują linijki 2 i 3, ale w nich nic nie zmieniano. Co się zmieniło? Zapisz swoją hipotezę.

**Wyjaśnienie.** Kompilator czyta plik od góry i musi znać każdą użytą nazwę. `std::cout` nie jest wbudowane w język: to część **biblioteki standardowej**, a kompilator dowiaduje się o niej dopiero z linijki `#include <iostream>`.

- Linijki zaczynające się od `#` to **dyrektywy preprocesora**: polecenia dla narzędzi budowania, wykonywane jeszcze przed właściwą kompilacją. **Nie są instrukcjami programu.** Nie wykonują się, gdy program działa, nie stoją w `main` i nie kończą się średnikiem.
- `#include <iostream>` znaczy: „wstaw w tym miejscu **deklaracje** z części biblioteki standardowej o nazwie `iostream`”. Deklaracja to informacja dla kompilatora, że coś o danej nazwie istnieje i jak tego używać. Jedną z tych deklaracji jest `std::cout`.
- Bez tej linijki kompilator nie zna ani `std`, ani `std::cout`.

To przykład z eksperymentu A: **przyczyna jest w innym miejscu niż wskazane linijki**. Kompilator pokazuje, gdzie użyto nieznanej nazwy, a brakuje czegoś na samej górze pliku.

**Jeden błąd, kilka komunikatów.** Jedna brakująca linijka dała dwa komunikaty, po jednym w każdym miejscu, gdzie użyto `std`. Gdyby program miał dziesięć takich instrukcji, komunikatów byłoby dziesięć, a błąd nadal jeden. Dlatego nie poprawiaj każdego komunikatu osobno: szukaj **wspólnej przyczyny**.

**Popraw jedną rzecz:** przywróć `#include <iostream>` i pustą linijkę na górze pliku. Zbuduj ponownie. Oba komunikaty znikną naraz, choć zmieniono tylko jedno miejsce. Kliknij **Run** i sprawdź wynik.

## 5. Eksperyment C: `cout` zamiast `std::cout`

Tym razem dostajesz tylko zadanie. Przejdź przez schemat samodzielnie.

**Zmiana.** Zacznij od poprawnego programu. W linijce 5 usuń `std::`, tak żeby zostało samo `cout`:

<!-- broken: no_std at=5:5 errors=1 error=^use of undeclared identifier 'cout'; did you mean 'std::cout'\?$ -->
```cpp
#include <iostream>

int main() {
    std::cout << "Good morning!\n";
    cout << "Time to write some C++.\n";
}
```

**Zadanie:**

1. Przewidź, czy program się zbuduje.
2. Zbuduj go i znajdź pierwszą istotną informację: plik, linijkę, pozycję i opis.
3. Zapisz hipotezę: co jest nie tak i **dlaczego**. „Trzeba dopisać `std::`” to jeszcze nie odpowiedź na pytanie „dlaczego”.
4. Popraw jedną rzecz, zbuduj ponownie i sprawdź wynik.

<details>
<summary>Podpowiedź (dotyczy sposobu pracy)</summary>

Komunikat ma dwie części oddzielone średnikiem. Druga to propozycja kompilatora. Pod komunikatem jest jeszcze linijka `note:`, czyli dodatkowa informacja. Do jakiego pliku prowadzi? Czy to Twój plik?

</details>

<details>
<summary>Wyjaśnienie: przeczytaj po własnej próbie</summary>

```text
…/main.cpp:5:5: error: use of undeclared identifier 'cout'; did you mean 'std::cout'?
    5 |     cout << "Time to write some C++.\n";
      |     ^~~~
      |     std::cout
…/iostream:…: note: 'std::cout' declared here
1 error generated.
```

- **Co mówi komunikat:** „użyto nazwy `cout`, której kompilator nie zna; czy chodziło o `std::cout`?”.
- **Linijka `note:`** prowadzi do pliku `iostream` biblioteki standardowej, tam gdzie zadeklarowano `std::cout`. Ścieżka i numer linijki zależą od systemu, bo każdy ma inną bibliotekę standardową. To nie Twój plik i niczego w nim nie zmieniasz.
- **Dlaczego:** nazwy z biblioteki standardowej należą do grupy nazw o nazwie `std` (fachowo: *przestrzeni nazw*, ang. *namespace*; poznasz je dokładniej później). `std::cout` to pełna nazwa: „`cout` z grupy `std`”. Samo `cout` to dla kompilatora **inna nazwa**, szukana poza tą grupą. Nikt jej nie zadeklarował, więc kompilator jej nie zna. `#include <iostream>` jest na miejscu, więc kompilator zna `std::cout` i dlatego może ją podpowiedzieć.
- **Poprawka:** przywróć `std::` w linijce 5.
- **Propozycja kompilatora** była tu trafna, ale traktuj ją jak hipotezę do sprawdzenia, a nie polecenie. Zrozum, dlaczego ma sens, zanim ją przyjmiesz.

W internecie możesz spotkać linijkę `using namespace std;`, dzięki której pisze się samo `cout`. W tym kursie jej nie używamy: pełna nazwa `std::cout` od razu mówi, skąd pochodzi.

</details>

## 6. Misja: lista zakupów

Ktoś napisał program, który ma wypisywać listę zakupów, ale programu nie da się zbudować, a może nie tylko to. Napraw go.

**Przygotuj projekt:**

1. Utwórz `cpp-workspace/shopping_list` i skopiuj do niego `main.cpp` i `CMakeLists.txt` z oryginalnego `lesson_05_first_program`.
2. Otwórz go w CLionie i sprawdź, czy jest `Clang 22`.
3. Zastąp zawartość `main.cpp` tym kodem (skopiuj go stąd):

<!-- broken: shopping_list_start at=2:5 errors=4 error=^use of undeclared identifier 'std'$ -->
```cpp
int main() {
    std::cout << "SHOPPING LIST\n";
    std::cout << "- bread\n"
    cout << "- milk\n";
    std::cout << "- apples";
    std::cout << "TOTAL: 3 items\n";
}
```

**Cel:** program buduje się bez błędów i wypisuje dokładnie:

<!-- output: shopping_list -->
```text
SHOPPING LIST
- bread
- milk
- apples
TOTAL: 3 items
```

**Sposób pracy:**

1. Zbuduj program.
2. Przeczytaj komunikaty.
3. Wybierz jeden problem.
4. Zapisz przypuszczenie, co jest jego przyczyną.
5. Wprowadź jedną poprawkę.
6. Zbuduj ponownie.
7. Powtarzaj, aż program się zbuduje **i** wypisze oczekiwany wynik.

**Dziennik diagnostyczny.** Każdą poprawkę zapisuj jako jeden wiersz, na przykład w notatkach:

| # | Objaw: co widzę | Przypuszczenie: dlaczego | Poprawka: jedna zmiana | Rezultat: co widzę po zbudowaniu |
|---|---|---|---|---|
| 1 | | | | |

### Kryterium sukcesu

- Program buduje się bez żadnego `error`.
- Program wypisuje **dokładnie** pięć oczekiwanych linijek.
- Każdy wiersz dziennika opisuje jedną poprawkę, a po każdej poprawce program był budowany ponownie.
- Dziennik pokazuje, które problemy zgłosił kompilator, a który znaleziono dopiero po porównaniu wyniku z oczekiwanym.
- Umiesz wyjaśnić każdą poprawkę własnymi słowami.

<details>
<summary>Podpowiedź 1</summary>

Ile różnych przyczyn mogą mieć komunikaty z pierwszego budowania? Czy kilka komunikatów może mieć jedną przyczynę?

</details>

<details>
<summary>Podpowiedź 2</summary>

Po każdej poprawce czytaj komunikaty od nowa: mogą pojawić się nowe, a numery linijek mogą się przesunąć. Gdy program wreszcie się zbuduje, nie kończ: porównaj wynik z oczekiwanym, znak po znaku.

</details>

Przykładowe rozwiązanie, razem z przykładowym dziennikiem, jest w części [Przykładowe rozwiązania](#przykładowe-rozwiązania).

## 7. Gdy coś pójdzie inaczej

| Co widzisz | Co to znaczy | Co zrobić |
|---|---|---|
| Bardzo dużo komunikatów | Kilka z nich może mieć jedną przyczynę. | Zacznij od pierwszego komunikatu, który wskazuje `main.cpp`. Popraw jedną rzecz i zbuduj ponownie: często znika kilka komunikatów naraz. |
| Po poprawce pojawiły się nowe komunikaty | Kompilator doszedł dalej i zauważył coś, czego wcześniej nie sprawdził. Albo poprawka wprowadziła nowy problem. | Przeczytaj komunikaty od nowa. Jeśli poprawka niczego nie wyjaśniła, cofnij ją (<kbd>Ctrl</kbd> + <kbd>Z</kbd>, na macOS <kbd>⌘ Cmd</kbd> + <kbd>Z</kbd>) i postaw nową hipotezę. |
| Inny tekst komunikatu niż w lekcji | Treść komunikatów zależy od wersji kompilatora i systemu. | Szukaj tych samych informacji: pliku, linijki, pozycji i sensu opisu. |
| Numer linijki nie pasuje do tego, co widzisz w edytorze | Kod zmienił się od ostatniego budowania, na przykład dopisano linijkę na górze. | Zbuduj ponownie i czytaj nowe komunikaty. |
| Budowanie się udało, ale wynik jest inny niż oczekiwany | To nie jest problem dla kompilatora: kod jest poprawnym C++, ale robi coś innego, niż chcesz. | Porównaj wynik z oczekiwanym znak po znaku i znajdź instrukcję, która wypisuje różniący się fragment. |
| W terminalu program wypisuje stary wynik | Ostatnie budowanie się nie udało, więc został poprzedni plik wykonywalny (lekcja 0.5). | Sprawdź wynik budowania i popraw błędy. Uruchamiaj program dopiero po udanym budowaniu. |

## 8. Wyjaśnij

Odpowiedz własnymi słowami, najlepiej na piśmie. Dopiero potem porównaj z przykładową odpowiedzią.

**1.** Czym różni się program, który się nie buduje, od programu, który się buduje, ale wypisuje zły tekst? Kto zauważa każdy z tych problemów?

<details>
<summary>Przykładowa odpowiedź</summary>

Gdy program się nie buduje, kompilator zgłasza `error` i nowy program nie powstaje. Kod nie jest poprawnym C++. Gdy program się buduje, ale wypisuje zły tekst, kod jest poprawnym C++, tylko robi coś innego, niż chcieliśmy. Kompilator tego nie zauważy; widać to dopiero po porównaniu wyniku z oczekiwanym.

</details>

**2.** Co oznaczają liczby w `main.cpp:4:35`?

<details>
<summary>Przykładowa odpowiedź</summary>

Linijkę 4 i pozycję 35 w tej linijce, czyli miejsce, w którym kompilator zauważył problem.

</details>

**3.** Dlaczego w eksperymencie B jeden brakujący `#include` dał dwa komunikaty? Ile poprawek było potrzebnych?

<details>
<summary>Przykładowa odpowiedź</summary>

Kompilator zgłosił problem w każdym miejscu, gdzie użyto nieznanej nazwy `std`, czyli w dwóch instrukcjach. Przyczyna była jedna, więc wystarczyła jedna poprawka: przywrócenie `#include <iostream>`.

</details>

**4.** Czym `#include <iostream>` różni się od instrukcji `std::cout << "…";`?

<details>
<summary>Przykładowa odpowiedź</summary>

`#include <iostream>` to dyrektywa preprocesora, wykonywana przed kompilacją: udostępnia kompilatorowi deklaracje z biblioteki standardowej, między innymi `std::cout`. Nie wykonuje się, gdy program działa. `std::cout << "…";` to instrukcja w `main`, wykonywana, gdy program działa: wypisuje tekst.

</details>

**5.** Dlaczego warto poprawiać jedną rzecz naraz i budować po każdej zmianie?

<details>
<summary>Przykładowa odpowiedź</summary>

Bo wtedy wiadomo, co dała każda zmiana: czy hipoteza była trafna i czy poprawka czegoś nie zepsuła. Jedna przyczyna może dać kilka komunikatów, a po poprawce mogą pojawić się nowe. Po wielu zmianach naraz trudno powiedzieć, która co zrobiła.

</details>

## Podsumowanie

- Błędy kompilacji to normalna część programowania. Komunikat mówi, **gdzie** (plik, linijka, pozycja) i **co** kompilatorowi nie pasuje.
- Czytaj wynik budowania od góry i szukaj pierwszej informacji, która wskazuje miejsce w Twoim kodzie. Wskazane miejsce to początek poszukiwań: przyczyna może być wcześniej, nawet w innej linijce.
- Jeden błąd może dać kilka komunikatów, a inne błędy mogą być niewidoczne, dopóki nie poprawisz pierwszego.
- Pracuj w pętli: **zobacz problem → przeczytaj diagnostykę → postaw hipotezę → popraw jedną rzecz → zbuduj ponownie → sprawdź wynik**.
- `;` kończy instrukcję. `#include <iostream>` udostępnia kompilatorowi deklaracje, między innymi `std::cout`. `std::` wskazuje, że to nazwa z biblioteki standardowej.
- Udane budowanie nie oznacza poprawnego programu: kompilator nie sprawdza, czy program robi to, co chcesz. Wynik zawsze trzeba sprawdzić.

---

## Przykładowe rozwiązania

Zajrzyj tutaj **po własnej próbie**. Twoja kolejność poprawek może być inna i nadal dobra, jeśli każdą poprawkę uzasadniono, a program wypisuje dokładnie oczekiwany wynik.

<details>
<summary>Misja: przykładowy dziennik diagnostyczny</summary>

| # | Objaw: co widzę | Przypuszczenie: dlaczego | Poprawka: jedna zmiana | Rezultat: co widzę po zbudowaniu |
|---|---|---|---|---|
| 1 | 4 błędy `use of undeclared identifier 'std'` w linijkach 2, 3, 5 i 6. | Wszystkie dotyczą nieznanej nazwy `std`. Brakuje `#include <iostream>`: jedna przyczyna, cztery komunikaty. | Dopisuję `#include <iostream>` i pustą linijkę na górze. | Nowe komunikaty: `expected ';' after expression` w linijce 5 i `use of undeclared identifier 'cout'` w linijce 6. Wcześniej ich nie było. Numery linijek przesunęły się o 2. |
| 2 | `5:29: error: expected ';' after expression` | Po napisie `"- bread\n"` brakuje średnika. | Dopisuję `;` na końcu linijki 5. | Zostaje jeden błąd: `cout` w linijce 6. |
| 3 | `6:5: error: use of undeclared identifier 'cout'; did you mean 'std::cout'?` | Brakuje `std::`, więc `cout` to nazwa, której nikt nie zadeklarował. | Dopisuję `std::` przed `cout`. | Budowanie się udaje. Run: `- applesTOTAL: 3 items` w jednej linijce. |
| 4 | Wynik inny niż oczekiwany: dwie linijki sklejone. Kompilator nic nie zgłosił. | Napis `"- apples"` nie kończy się `\n`. | Dopisuję `\n` w tym napisie. | Wynik zgadza się z oczekiwanym. |

**Dlaczego po poprawce 1 pojawiły się nowe błędy?** Kompilator, który nie rozumie początku instrukcji, często pomija jej resztę aż do najbliższego średnika. W pierwotnym kodzie brakowało średnika w linijce 3, więc ta instrukcja ciągnęła się do końca linijki 4. Błąd z `cout` był w niej ukryty. Liczba komunikatów nie musi więc równać się liczbie błędów, w żadną stronę.

</details>

<details>
<summary>Misja: kod po kolejnych poprawkach</summary>

Po poprawce 1:

<!-- broken: shopping_list_after_include at=5:29 errors=2 error=^expected ';' after expression$ -->
```cpp
#include <iostream>

int main() {
    std::cout << "SHOPPING LIST\n";
    std::cout << "- bread\n"
    cout << "- milk\n";
    std::cout << "- apples";
    std::cout << "TOTAL: 3 items\n";
}
```

Po poprawce 2:

<!-- broken: shopping_list_after_semicolon at=6:5 errors=1 error=^use of undeclared identifier 'cout'; did you mean 'std::cout'\?$ -->
```cpp
#include <iostream>

int main() {
    std::cout << "SHOPPING LIST\n";
    std::cout << "- bread\n";
    cout << "- milk\n";
    std::cout << "- apples";
    std::cout << "TOTAL: 3 items\n";
}
```

Po poprawce 3 program się buduje, ale wypisuje:

<!-- example: shopping_list_builds -->
```cpp
#include <iostream>

int main() {
    std::cout << "SHOPPING LIST\n";
    std::cout << "- bread\n";
    std::cout << "- milk\n";
    std::cout << "- apples";
    std::cout << "TOTAL: 3 items\n";
}
```

<!-- output: shopping_list_builds -->
```text
SHOPPING LIST
- bread
- milk
- applesTOTAL: 3 items
```

Po poprawce 4, czyli rozwiązanie:

<!-- example: shopping_list -->
```cpp
#include <iostream>

int main() {
    std::cout << "SHOPPING LIST\n";
    std::cout << "- bread\n";
    std::cout << "- milk\n";
    std::cout << "- apples\n";
    std::cout << "TOTAL: 3 items\n";
}
```

</details>

**Poprzednia lekcja:** [Lekcja 1.1: Pierwszy program od środka](lesson_01_first_program_inside.md) · **Następna lekcja:** w przygotowaniu · [Opis kursu](../../README.md)

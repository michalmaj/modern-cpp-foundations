# Modern C++ Foundations

**Polski** · [English](README.en.md)

Kurs programowania od zera, w języku C++. Nie musisz wcześniej programować. Wystarczy, że umiesz korzystać z komputera tak jak na co dzień.

> **Stan kursu: w przygotowaniu.** Moduł 0 jest funkcjonalnie kompletny (sześć lekcji, wersja pilotażowa). Dostępne są też wszystkie lekcje Modułu 1 (sześć lekcji, wersja pilotażowa). Dostępne są też wszystkie lekcje Modułu 2 (osiem lekcji, wersja pilotażowa). Dostępne są też wszystkie lekcje Modułu 3 (sześć lekcji, wersja pilotażowa). Moduł 4 jest rozwijany: dostępna jest jego pierwsza lekcja. Szczegóły znajdziesz w sekcji [Stan kursu](#stan-kursu).

## Ścieżka nauki C++

Modern C++ Foundations to pierwszy z trzech kursów, które razem tworzą ścieżkę nauki C++:

| Część | Kurs | Czego dotyczy | Repozytorium | Stan |
|---|---|---|---|---|
| **A: jesteś tutaj** | **Modern C++ Foundations** | Podstawy programowania i współczesnego C++ | [modern-cpp-foundations](https://github.com/michalmaj/modern-cpp-foundations) | W przygotowaniu |
| B | Advanced Modern C++ | C++ dla zaawansowanych: jak język działa „od środka”, szablony, zarządzanie pamięcią, programy wykonujące wiele zadań jednocześnie, wydajność | `advanced-modern-cpp` (jeszcze nie utworzone) | Planowany |
| C | C++ Vision & AI Systems | C++ w praktyce: przetwarzanie obrazu, sztuczna inteligencja i systemy, w których liczy się wydajność | `cpp-vision-ai-systems` (jeszcze nie utworzone) | Planowany |

Kolejność A → B → C jest zalecana, ale nie obowiązkowa. Jeśli masz już podobną wiedzę, możesz zacząć od kursu B lub C.

## Dla kogo jest ten kurs

Dla każdego, kto chce nauczyć się programowania od podstaw i robić to porządnie. Kurs uczy jednocześnie dwóch rzeczy: **jak myśleć jak programista** i **jak pisać programy w C++**.

C++ to jeden z najważniejszych języków programowania. Pisze się w nim między innymi gry, przeglądarki internetowe, części systemów operacyjnych, oprogramowanie samochodów i narzędzia naukowe.

To kurs ogólny. Nie musisz interesować się żadną konkretną dziedziną: to, czego się nauczysz, przyda się w każdym rodzaju programowania w C++.

## Nie musisz umieć programować

Kurs zaczyna się jeszcze przed pierwszym programem. Nie zakładamy, że wiesz:

- czym jest terminal, czyli okno, w którym wydaje się komputerowi polecenia tekstowe;
- jak tekst, który piszesz, staje się programem, który można uruchomić;
- czym są kompilator, Git czy środowisko programistyczne.

Każde nowe pojęcie wyjaśniamy, zanim zaczniemy go używać. Nie wymagamy też znajomości innego języka programowania.

Od pierwszej lekcji uczymy współczesnego C++. Nie zaczynamy od przestarzałych nawyków, których potem trzeba się oduczać. Starsze sposoby pisania pokazujemy tylko jako tło historyczne, gdy pomagają coś zrozumieć.

## Czego się nauczysz

Po ukończeniu kursu będziesz umieć:

- samodzielnie pisać, uruchamiać i poprawiać programy w C++, od pierwszego `Hello, World!` po małe i średnie aplikacje;
- rozwiązywać nowe problemy krok po kroku: zrozumieć zadanie, zaprojektować rozwiązanie, sprawdzić je i wyjaśnić, dlaczego działa;
- czytać komunikaty o błędach i spokojnie szukać ich przyczyny;
- przechowywać i przetwarzać dane: liczby, teksty, listy i własne typy danych;
- dzielić program na mniejsze, czytelne części: funkcje, pliki, biblioteki i klasy;
- rozumieć, jak program korzysta z pamięci, i pisać kod, który bezpiecznie nią zarządza;
- wyjaśnić, co dzieje się od napisania kodu do uruchomienia programu;
- sprawdzać, czy program działa poprawnie: pisać testy, korzystać z debuggera (narzędzia do śledzenia programu krok po kroku) i reagować na ostrzeżenia;
- korzystać z terminala oraz z Gita i GitHuba, czyli narzędzi do zapisywania historii zmian w kodzie i dzielenia się nim, tak jak robią to zawodowi programiści.

## Jak wygląda nauka

Większość pracy to **krótkie, niezależne zadania**. Każde ma własną krótką historię, która wyjaśnia, po co piszesz dany program, oraz jasny sposób sprawdzenia, czy rozwiązanie działa. Zadania nie składają się w jedną wielką aplikację: jeśli utkniesz na jednym, nie zablokuje to kolejnych. Od czasu do czasu pojawi się większy, samodzielny projekt, który łączy kilka umiejętności.

W każdym temacie powtarza się ten sam rytm:

**zrozum → wypróbuj → zastosuj → sprawdź → wyjaśnij**

Na początku prowadzimy krok po kroku. Z czasem coraz więcej decyzji należy do Ciebie, aż do samodzielnego projektowania rozwiązań.

## Na czym będziesz pracować

**Systemy operacyjne:** Windows, Linux i macOS. Wszystkie trzy są oficjalnie wspierane. Nie potrzebujesz specjalnego sprzętu: wystarczy zwykły komputer z jednym z tych systemów i dostęp do internetu, żeby zainstalować narzędzia.

**Narzędzia:**

| Narzędzie | Do czego służy |
|---|---|
| **CLion** | Środowisko programistyczne (IDE): program, w którym piszesz, uruchamiasz i sprawdzasz swój kod. |
| **LLVM/Clang 22 lub nowszy** | Zestaw narzędzi z kompilatorem `clang++`, który tłumaczy kod C++ na program, jaki komputer może uruchomić. |
| **C++20** | Wersja języka C++, której uczymy. |
| **CMake** | Opisuje, z jakich plików składa się projekt i jak z nich zbudować program. |
| **Ninja** | Szybko wykonuje kroki budowania przygotowane przez CMake. |
| **CTest** | Uruchamia testy, które sprawdzają, czy program działa poprawnie. |

Nie musisz teraz rozumieć tych nazw ani niczego instalować. Każde narzędzie wyjaśnimy w kursie, a zainstalujesz je w [lekcji 0.4](course/module_00_tooling/lesson_04_installing_the_tools.md). To wersja pilotażowa: część kroków instalacji nie została jeszcze sprawdzona na każdym systemie.

CLion jest wygodny, ale nie jest konieczny: każdy projekt z kursu da się zbudować i uruchomić także z terminala.

Na Windowsie kompilator korzysta dodatkowo z narzędzi Microsoftu (Visual Studio Build Tools z Windows SDK). Lekcja 0.4 pokazuje, jak je zainstalować.

## Stan kursu

Kurs jest **w przygotowaniu**. Uczciwie o tym, co już jest, a czego jeszcze nie ma:

| Element | Stan |
|---|---|
| Opis kursu (ten plik) | Gotowy |
| Moduł 0, lekcja 1: [Pliki, katalogi i pierwsze spotkanie z terminalem](course/module_00_tooling/lesson_01_files_and_terminal.md) | Dostępna (wersja pilotażowa) |
| Moduł 0, lekcja 2: [Poruszanie się między katalogami](course/module_00_tooling/lesson_02_moving_between_folders.md) | Dostępna (wersja pilotażowa) |
| Moduł 0, lekcja 3: [Co się dzieje, gdy wpisujesz polecenie?](course/module_00_tooling/lesson_03_commands_and_programs.md) | Dostępna (wersja pilotażowa) |
| Moduł 0, lekcja 4: [Przygotuj warsztat: instalacja narzędzi](course/module_00_tooling/lesson_04_installing_the_tools.md) | Dostępna (wersja pilotażowa; instrukcje instalacji nie zostały jeszcze sprawdzone na każdym systemie) |
| Moduł 0, lekcja 5: [Twój pierwszy działający program w CLionie](course/module_00_tooling/lesson_05_first_program_in_clion.md) | Dostępna (wersja pilotażowa; kroki w CLionie nie zostały jeszcze sprawdzone na każdym systemie) |
| Moduł 0, lekcja 6: [Ten sam program bez CLiona](course/module_00_tooling/lesson_06_same_program_without_clion.md) | Dostępna (wersja pilotażowa) |
| Moduł 1, lekcja 1: [Pierwszy program od środka](course/module_01_first_programs/lesson_01_first_program_inside.md) | Dostępna (wersja pilotażowa; kroki w CLionie nie zostały jeszcze sprawdzone na każdym systemie) |
| Moduł 1, lekcja 2: [Gdy kompilator protestuje](course/module_01_first_programs/lesson_02_when_the_compiler_complains.md) | Dostępna (wersja pilotażowa; kroki w CLionie nie zostały jeszcze sprawdzone na każdym systemie) |
| Moduł 1, lekcja 3: [Program od pustej kartki](course/module_01_first_programs/lesson_03_a_program_from_a_blank_page.md) | Dostępna (wersja pilotażowa; kroki w CLionie nie zostały jeszcze sprawdzone na każdym systemie) |
| Moduł 1, lekcja 4: [Od kodu źródłowego do programu wykonywalnego](course/module_01_first_programs/lesson_04_from_source_code_to_an_executable.md) | Dostępna (wersja pilotażowa) |
| Moduł 1, lekcja 5: [Zapisz historię swojej pracy](course/module_01_first_programs/lesson_05_save_the_history_of_your_work.md) | Dostępna (wersja pilotażowa) |
| Moduł 1, lekcja 6: [Samodzielnie od pomysłu do działającego programu](course/module_01_first_programs/lesson_06_from_idea_to_working_program.md) (sprawdzian Modułu 1) | Dostępna (wersja pilotażowa) |
| Moduł 2, lekcja 1: [Wartości, które program pamięta](course/module_02_values_and_calculations/lesson_01_values_the_program_remembers.md) | Dostępna (wersja pilotażowa) |
| Moduł 2, lekcja 2: [Gdy wartości się zmieniają](course/module_02_values_and_calculations/lesson_02_when_values_change.md) | Dostępna (wersja pilotażowa) |
| Moduł 2, lekcja 3: [Zobacz, co dzieje się w programie](course/module_02_values_and_calculations/lesson_03_see_what_happens_in_the_program.md) | Dostępna (wersja pilotażowa; kroki debuggera w CLionie nie zostały jeszcze sprawdzone na każdym systemie) |
| Moduł 2, lekcja 4: [Dzielenie, reszta i kolejność działań](course/module_02_values_and_calculations/lesson_04_division_remainder_and_order_of_operations.md) | Dostępna (wersja pilotażowa) |
| Moduł 2, lekcja 5: [Liczby z częścią ułamkową: `double` i `auto`](course/module_02_values_and_calculations/lesson_05_numbers_with_a_fractional_part.md) | Dostępna (wersja pilotażowa) |
| Moduł 2, lekcja 6: [Program, który pyta użytkownika](course/module_02_values_and_calculations/lesson_06_a_program_that_asks_the_user.md) | Dostępna (wersja pilotażowa) |
| Moduł 2, lekcja 7: [Tekst, który program pamięta (`std::string`)](course/module_02_values_and_calculations/lesson_07_text_the_program_remembers.md) | Dostępna (wersja pilotażowa) |
| Moduł 2, lekcja 8: [Od danych do wyniku](course/module_02_values_and_calculations/lesson_08_from_data_to_result.md) (sprawdzian Modułu 2) | Dostępna (wersja pilotażowa) |
| Moduł 3, lekcja 1: [Pierwsza decyzja programu (`if`)](course/module_03_decisions_and_conditions/lesson_01_the_first_decision.md) | Dostępna (wersja pilotażowa) |
| Moduł 3, lekcja 2: [Dwie możliwości (`else`), równość i `bool`](course/module_03_decisions_and_conditions/lesson_02_two_ways.md) | Dostępna (wersja pilotażowa) |
| Moduł 3, lekcja 3: [Wybór spośród wielu możliwości (`else if`)](course/module_03_decisions_and_conditions/lesson_03_many_possibilities.md) | Dostępna (wersja pilotażowa) |
| Moduł 3, lekcja 4: [Łączenie warunków (`&&`, `\|\|`, `!`)](course/module_03_decisions_and_conditions/lesson_04_combining_conditions.md) | Dostępna (wersja pilotażowa) |
| Moduł 3, lekcja 5: [Sprawdzanie danych przed obliczeniami](course/module_03_decisions_and_conditions/lesson_05_check_before_calculating.md) | Dostępna (wersja pilotażowa) |
| Moduł 3, lekcja 6: [Program podejmuje decyzje (sprawdzian Modułu 3)](course/module_03_decisions_and_conditions/lesson_06_the_program_decides.md) | Dostępna (wersja pilotażowa) |
| Moduł 4, lekcja 1: [Pierwsza pętla (`while`)](course/module_04_repeating_actions/lesson_01_the_first_loop.md) | Dostępna (wersja pilotażowa) |
| Moduł 4: pozostałe lekcje (powtarzanie działań) | W przygotowaniu |
| Kolejne moduły | Planowane |
| Plan całego kursu | Jeszcze nieopublikowany |
| Kursy B i C | Planowane, repozytoria jeszcze nie istnieją |

## Jak zacząć

Przechodź lekcje po kolei, zaczynając od pierwszej:

1. **[Lekcja 0.1: Pliki, katalogi i pierwsze spotkanie z terminalem](course/module_00_tooling/lesson_01_files_and_terminal.md)**
2. **[Lekcja 0.2: Poruszanie się między katalogami](course/module_00_tooling/lesson_02_moving_between_folders.md)**
3. **[Lekcja 0.3: Co się dzieje, gdy wpisujesz polecenie?](course/module_00_tooling/lesson_03_commands_and_programs.md)**
4. **[Lekcja 0.4: Przygotuj warsztat: instalacja narzędzi](course/module_00_tooling/lesson_04_installing_the_tools.md)**
5. **[Lekcja 0.5: Twój pierwszy działający program w CLionie](course/module_00_tooling/lesson_05_first_program_in_clion.md)**
6. **[Lekcja 0.6: Ten sam program bez CLiona](course/module_00_tooling/lesson_06_same_program_without_clion.md)**
7. **[Lekcja 1.1: Pierwszy program od środka](course/module_01_first_programs/lesson_01_first_program_inside.md)**
8. **[Lekcja 1.2: Gdy kompilator protestuje](course/module_01_first_programs/lesson_02_when_the_compiler_complains.md)**
9. **[Lekcja 1.3: Program od pustej kartki](course/module_01_first_programs/lesson_03_a_program_from_a_blank_page.md)**
10. **[Lekcja 1.4: Od kodu źródłowego do programu wykonywalnego](course/module_01_first_programs/lesson_04_from_source_code_to_an_executable.md)**
11. **[Lekcja 1.5: Zapisz historię swojej pracy](course/module_01_first_programs/lesson_05_save_the_history_of_your_work.md)**
12. **[Lekcja 1.6: Samodzielnie od pomysłu do działającego programu](course/module_01_first_programs/lesson_06_from_idea_to_working_program.md)**
13. **[Lekcja 2.1: Wartości, które program pamięta](course/module_02_values_and_calculations/lesson_01_values_the_program_remembers.md)**
14. **[Lekcja 2.2: Gdy wartości się zmieniają](course/module_02_values_and_calculations/lesson_02_when_values_change.md)**
15. **[Lekcja 2.3: Zobacz, co dzieje się w programie](course/module_02_values_and_calculations/lesson_03_see_what_happens_in_the_program.md)**
16. **[Lekcja 2.4: Dzielenie, reszta i kolejność działań](course/module_02_values_and_calculations/lesson_04_division_remainder_and_order_of_operations.md)**
17. **[Lekcja 2.5: Liczby z częścią ułamkową: `double` i `auto`](course/module_02_values_and_calculations/lesson_05_numbers_with_a_fractional_part.md)**
18. **[Lekcja 2.6: Program, który pyta użytkownika](course/module_02_values_and_calculations/lesson_06_a_program_that_asks_the_user.md)**
19. **[Lekcja 2.7: Tekst, który program pamięta (`std::string`)](course/module_02_values_and_calculations/lesson_07_text_the_program_remembers.md)**
20. **[Lekcja 2.8: Od danych do wyniku (sprawdzian Modułu 2)](course/module_02_values_and_calculations/lesson_08_from_data_to_result.md)**
21. **[Lekcja 3.1: Pierwsza decyzja programu (`if`)](course/module_03_decisions_and_conditions/lesson_01_the_first_decision.md)**
22. **[Lekcja 3.2: Dwie możliwości (`else`), równość i `bool`](course/module_03_decisions_and_conditions/lesson_02_two_ways.md)**
23. **[Lekcja 3.3: Wybór spośród wielu możliwości (`else if`)](course/module_03_decisions_and_conditions/lesson_03_many_possibilities.md)**
24. **[Lekcja 3.4: Łączenie warunków (`&&`, `||`, `!`)](course/module_03_decisions_and_conditions/lesson_04_combining_conditions.md)**
25. **[Lekcja 3.5: Sprawdzanie danych przed obliczeniami](course/module_03_decisions_and_conditions/lesson_05_check_before_calculating.md)**
26. **[Lekcja 3.6: Program podejmuje decyzje (sprawdzian Modułu 3)](course/module_03_decisions_and_conditions/lesson_06_the_program_decides.md)**
27. **[Lekcja 4.1: Pierwsza pętla (`while`)](course/module_04_repeating_actions/lesson_01_the_first_loop.md)**

Do lekcji 0.1–0.3 potrzebujesz tylko komputera z Windows, macOS albo Linuksem. W lekcji 0.4 zainstalujesz narzędzia kursu.

W Module 1 (lekcje 1.1–1.6) zaczniesz czytać i pisać własny kod w C++20. W Module 2 (lekcje 2.1–2.8) programy zaczną pamiętać wartości, liczyć, pobierać dane od użytkownika i przechowywać tekst. Kończy go sprawdzian w lekcji 2.8. W Module 3 (lekcje 3.1–3.6) programy zaczną podejmować decyzje. Kończy go sprawdzian w lekcji 3.6. W Module 4, który zaczyna lekcja 4.1, programy zaczną powtarzać działania. Kolejne lekcje Modułu 4 są w przygotowaniu.

## Co dalej po tym kursie

Naturalnym kolejnym krokiem będzie **Advanced Modern C++ (B)**, który pogłębia to, czego nauczysz się tutaj. Jeśli zainteresuje Cię przetwarzanie obrazu i sztuczna inteligencja, później możesz przejść do **C++ Vision & AI Systems (C)**. Ten kurs będzie oficjalnie wspierał tylko system Ubuntu 24.04 LTS.

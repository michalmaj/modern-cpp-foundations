# Modern C++ Foundations

**Polski** · [English](README.en.md)

Kurs programowania od zera, w języku C++. Nie musisz wcześniej programować. Wystarczy, że umiesz korzystać z komputera tak jak na co dzień.

> **Stan kursu: w przygotowaniu.** Dostępne są trzy pierwsze lekcje, kolejne są w przygotowaniu. Szczegóły znajdziesz w sekcji [Stan kursu](#stan-kursu).

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

Nie musisz teraz rozumieć tych nazw ani niczego instalować. Każde narzędzie wyjaśnimy w kursie. Instrukcje instalacji dla każdego systemu opublikujemy dopiero wtedy, gdy zostaną sprawdzone.

CLion jest wygodny, ale nie jest konieczny: każdy projekt z kursu da się zbudować i uruchomić także z terminala.

Na Windowsie kompilator korzysta dodatkowo z narzędzi Microsoftu (Visual Studio Build Tools i Windows SDK). Dokładną listę potrzebnych składników podamy w instrukcji instalacji.

## Stan kursu

Kurs jest **w przygotowaniu**. Uczciwie o tym, co już jest, a czego jeszcze nie ma:

| Element | Stan |
|---|---|
| Opis kursu (ten plik) | Gotowy |
| Moduł 0, lekcja 1: [Pliki, katalogi i pierwsze spotkanie z terminalem](course/module_00_tooling/lesson_01_files_and_terminal.md) | Dostępna (wersja pilotażowa) |
| Moduł 0, lekcja 2: [Poruszanie się między katalogami](course/module_00_tooling/lesson_02_moving_between_folders.md) | Dostępna (wersja pilotażowa) |
| Moduł 0, lekcja 3: [Co się dzieje, gdy wpisujesz polecenie?](course/module_00_tooling/lesson_03_commands_and_programs.md) | Dostępna (wersja pilotażowa) |
| Pozostałe lekcje Modułu 0: przygotowanie komputera i pierwsze kroki | W przygotowaniu |
| Kolejne moduły | Planowane |
| Plan całego kursu | Jeszcze nieopublikowany |
| Kursy B i C | Planowane, repozytoria jeszcze nie istnieją |

## Jak zacząć

Przechodź lekcje po kolei, zaczynając od pierwszej:

1. **[Lekcja 0.1: Pliki, katalogi i pierwsze spotkanie z terminalem](course/module_00_tooling/lesson_01_files_and_terminal.md)**
2. **[Lekcja 0.2: Poruszanie się między katalogami](course/module_00_tooling/lesson_02_moving_between_folders.md)**
3. **[Lekcja 0.3: Co się dzieje, gdy wpisujesz polecenie?](course/module_00_tooling/lesson_03_commands_and_programs.md)**

Potrzebujesz tylko komputera z Windows, macOS albo Linuksem. Nie musisz niczego instalować.

Kolejne lekcje Modułu 0 są w przygotowaniu. Zainstalujesz w nich narzędzia i sprawdzisz, czy wszystko działa, uruchamiając swój pierwszy program.

## Co dalej po tym kursie

Naturalnym kolejnym krokiem będzie **Advanced Modern C++ (B)**, który pogłębia to, czego nauczysz się tutaj. Jeśli zainteresuje Cię przetwarzanie obrazu i sztuczna inteligencja, później możesz przejść do **C++ Vision & AI Systems (C)**. Ten kurs będzie oficjalnie wspierał tylko system Ubuntu 24.04 LTS.

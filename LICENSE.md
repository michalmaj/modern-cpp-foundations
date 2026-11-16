# Licencje / Licences

[Polski](#polski) · [English](#english)

## Polski

Kurs Modern C++ Foundations ma dwie licencje: jedną dla tekstu i jedną dla kodu. Ten plik wyjaśnia, której licencji podlega każdy rodzaj materiału. Nie jest osobną, trzecią licencją: warunki korzystania określają pełne teksty obu licencji.

### Dwie licencje

| Licencja | Identyfikator SPDX | Pełny tekst | Strona licencji |
|---|---|---|---|
| Creative Commons Attribution 4.0 International (CC BY 4.0) | `CC-BY-4.0` | [LICENSES/CC-BY-4.0.txt](LICENSES/CC-BY-4.0.txt) | [creativecommons.org/licenses/by/4.0](https://creativecommons.org/licenses/by/4.0/) |
| Licencja MIT (MIT License) | `MIT` | [LICENSES/MIT.txt](LICENSES/MIT.txt) | [opensource.org/license/mit](https://opensource.org/license/mit) |

Obie licencje pozwalają kopiować, udostępniać i zmieniać materiały oraz wykorzystywać je w dowolnym celu, także komercyjnie. Wymagają za to podania autora i zachowania informacji o licencji (szczegóły niżej).

### Co obejmuje każda licencja

| Materiał | Licencja |
|---|---|
| Tekst lekcji po polsku i po angielsku: objaśnienia, polecenia ćwiczeń, pytania, podpowiedzi, opisy rozwiązań, tabele i podsumowania | CC BY 4.0 |
| Pozostała dokumentacja w plikach Markdown (`.md`), np. README i ten plik | CC BY 4.0 |
| Kod C++: pliki `.cpp` i `.hpp` oraz bloki kodu w lekcjach, razem z komentarzami w kodzie, przykładowymi rozwiązaniami i przykładami z celowymi błędami | MIT |
| Kod CMake: pliki `CMakeLists.txt` i bloki kodu CMake w lekcjach | MIT |
| Polecenia terminala w lekcjach | MIT |
| Dane do przykładów w lekcjach: dane wejściowe, pliki z danymi i oczekiwane wyniki programów z kursu | MIT, jako część przykładu |
| Wszystkie pozostałe pliki repozytorium poza plikami Markdown: testy, program sprawdzający przykłady z lekcji, skrypty, workflowy GitHub Actions i formularze zgłoszeń | MIT |
| Komunikaty kompilatora, linkera i innych narzędzi pokazane w lekcjach oraz teksty licencji w katalogu `LICENSES/` | żadna z nich (zobacz niżej) |

### Tekst i kod w jednym pliku lekcji

Lekcje są plikami Markdown (`.md`), w których tekst przeplata się z kodem. Dlatego o licencji decyduje rodzaj treści, a nie plik:

| Fragment lekcji | Licencja |
|---|---|
| akapit, który wyjaśnia działanie funkcji | CC BY 4.0 |
| blok kodu z tą funkcją w C++ | MIT |
| polecenie ćwiczenia | CC BY 4.0 |
| przykładowe rozwiązanie w C++ | MIT |
| blok kodu CMake | MIT |
| tabela, która wyjaśnia działanie programu | CC BY 4.0 |
| schemat katalogów albo inny blok, który tylko coś objaśnia | CC BY 4.0 |

Kod wpleciony w zdanie, np. `std::cout << total;`, też jest na licencji MIT, a samo zdanie na CC BY 4.0. Bloki kodu w lekcjach nie mają nagłówków licencyjnych, żeby nie przeszkadzały w nauce: obowiązuje je podział opisany w tym pliku.

### Przykłady

- **Nauka.** Czytasz lekcje, drukujesz je, przepisujesz przykłady i zmieniasz je, żeby sprawdzić, co się stanie.
- **Udostępnianie.** Wysyłasz lekcję osobom z grupy albo rozdajesz jej wydruki na zajęciach. Podaj autora, źródło i licencję.
- **Przeróbka.** Tłumaczysz lekcję, skracasz ją albo przygotowujesz na jej podstawie własne materiały do zajęć i publikujesz swoją wersję. Podaj autora, źródło i licencję oraz zaznacz, co zmieniono.
- **Własny projekt.** Program z lekcji staje się początkiem Twojego projektu, także komercyjnego. Zachowaj informację o prawach autorskich i tekst licencji MIT.

Licencje nie zmieniają zasad Twojej szkoły ani uczelni. Jeśli oddajesz pracę na zaliczenie, stosuj ich zasady korzystania z cudzych materiałów.

### Jak podać autora i licencję

**Tekst (CC BY 4.0).** Gdy udostępniasz tekst kursu albo jego przeróbkę, podaj:

- tytuł i autora: „Modern C++ Foundations”, Michał Maj;
- źródło: https://github.com/michalmaj/modern-cpp-foundations;
- licencję razem z odnośnikiem: CC BY 4.0, https://creativecommons.org/licenses/by/4.0/;
- informację, czy tekst zmieniono.

Przykład:

> Na podstawie lekcji 3.2 kursu „Modern C++ Foundations”, Michał Maj, https://github.com/michalmaj/modern-cpp-foundations, licencja CC BY 4.0, https://creativecommons.org/licenses/by/4.0/. Tekst przetłumaczono i skrócono.

Nie sugeruj, że autor kursu popiera Ciebie albo Twoją wersję.

**Kod (MIT).** Gdy kopiujesz kod z kursu albo jego istotną część, dołącz informację o prawach autorskich `Copyright (c) 2026 Michał Maj` i tekst licencji MIT, np. kopię pliku [LICENSES/MIT.txt](LICENSES/MIT.txt).

### Materiały innych twórców i znaki towarowe

- **Komunikaty narzędzi.** Lekcje pokazują komunikaty kompilatora, linkera, CMake'a, narzędzia Ninja, Gita i terminala. Tworzą je te narzędzia, więc licencje kursu ich nie obejmują.
- **Narzędzia i biblioteki.** Kurs uczy korzystania z narzędzi i bibliotek innych twórców, np. z biblioteki standardowej C++, LLVM/Clang, CMake'a, narzędzia Ninja, CLiona, Gita i GitHuba. Repozytorium nie zawiera ich kodu, a licencje kursu ich nie obejmują. Każde z nich ma własne warunki korzystania.
- **Znaki towarowe.** Nazwy produktów i firm mogą być znakami towarowymi ich właścicieli. Kurs używa ich tylko po to, żeby wskazać produkt. Nie oznacza to współpracy z ich właścicielami ani poparcia z ich strony.
- **Teksty licencji.** Pliki w katalogu `LICENSES/` zawierają standardowe teksty licencji. Licencje kursu ich nie obejmują.

### Bez gwarancji

Kurs i kod udostępniamy bez żadnych gwarancji. Szczegóły są w pełnych tekstach obu licencji.

### Autor

Autor kursu i właściciel praw autorskich: Michał Maj (https://github.com/michalmaj).

## English

The Modern C++ Foundations course has two licences: one for the text and one for the code. This file explains which licence covers each kind of material. It isn't a separate, third licence: the full texts of the two licences set the terms of use.

### Two licences

| Licence | SPDX identifier | Full text | Licence page |
|---|---|---|---|
| Creative Commons Attribution 4.0 International (CC BY 4.0) | `CC-BY-4.0` | [LICENSES/CC-BY-4.0.txt](LICENSES/CC-BY-4.0.txt) | [creativecommons.org/licenses/by/4.0](https://creativecommons.org/licenses/by/4.0/) |
| MIT License | `MIT` | [LICENSES/MIT.txt](LICENSES/MIT.txt) | [opensource.org/license/mit](https://opensource.org/license/mit) |

Both licences let you copy, share and change the materials and use them for any purpose, commercial use included. In return, they require you to credit the author and keep the licence information (details below).

### What each licence covers

| Material | Licence |
|---|---|
| Lesson text in Polish and English: explanations, exercise instructions, questions, hints, solution descriptions, tables and summaries | CC BY 4.0 |
| Other documentation in Markdown files (`.md`), e.g. the READMEs and this file | CC BY 4.0 |
| C++ code: `.cpp` and `.hpp` files and the code blocks in the lessons, including comments in the code, example solutions and examples with deliberate errors | MIT |
| CMake code: `CMakeLists.txt` files and the CMake code blocks in the lessons | MIT |
| Terminal commands in the lessons | MIT |
| Data for the examples in the lessons: input data, data files and the expected output of the course's programs | MIT, as part of the example |
| All other files in the repository apart from Markdown files: tests, the program that checks the lesson examples, scripts, GitHub Actions workflows and issue forms | MIT |
| Messages from the compiler, the linker and other tools shown in the lessons, and the licence texts in the `LICENSES/` folder | neither (see below) |

### Text and code in one lesson file

The lessons are Markdown files (`.md`) in which text and code alternate. So the licence depends on the kind of content, not on the file:

| Part of a lesson | Licence |
|---|---|
| a paragraph that explains how a function works | CC BY 4.0 |
| a code block with that function in C++ | MIT |
| exercise instructions | CC BY 4.0 |
| an example solution in C++ | MIT |
| a CMake code block | MIT |
| a table that explains how a program works | CC BY 4.0 |
| a folder diagram or another block that only explains something | CC BY 4.0 |

Code inside a sentence, e.g. `std::cout << total;`, is also under the MIT License, and the sentence itself is under CC BY 4.0. The code blocks in the lessons have no licence headers, so that they don't get in the way of learning: the split described in this file applies to them.

### Examples

- **Learning.** You read the lessons, print them, type out the examples and change them to see what happens.
- **Sharing.** You send a lesson to people in your group or hand out printed copies at a workshop. Give the author, the source and the licence.
- **Adapting.** You translate a lesson, shorten it or base your own teaching materials on it, and publish your version. Give the author, the source and the licence, and say what was changed.
- **Your own project.** A program from a lesson becomes the start of your own project, a commercial one included. Keep the copyright notice and the text of the MIT License.

The licences don't change the rules of your school or university. If you hand in work for a grade, follow their rules on using other people's materials.

### How to credit the author and the licence

**Text (CC BY 4.0).** When you share the course text or your adaptation of it, give:

- the title and the author: “Modern C++ Foundations”, Michał Maj;
- the source: https://github.com/michalmaj/modern-cpp-foundations;
- the licence with a link: CC BY 4.0, https://creativecommons.org/licenses/by/4.0/;
- whether the text was changed.

Example:

> Based on lesson 3.2 of “Modern C++ Foundations”, Michał Maj, https://github.com/michalmaj/modern-cpp-foundations, licensed under CC BY 4.0, https://creativecommons.org/licenses/by/4.0/. The text was translated and shortened.

Don't suggest that the author of the course endorses you or your version.

**Code (MIT).** When you copy code from the course, or a substantial part of it, include the copyright notice `Copyright (c) 2026 Michał Maj` and the text of the MIT License, e.g. a copy of [LICENSES/MIT.txt](LICENSES/MIT.txt).

### Other people's materials and trademarks

- **Tool messages.** The lessons show messages from the compiler, the linker, CMake, Ninja, Git and the terminal. These tools produce them, so the course's licences don't cover them.
- **Tools and libraries.** The course teaches you to use tools and libraries made by others, e.g. the C++ standard library, LLVM/Clang, CMake, Ninja, CLion, Git and GitHub. The repository doesn't contain their code, and the course's licences don't cover them. Each of them has its own terms of use.
- **Trademarks.** Product and company names may be trademarks of their owners. The course uses them only to identify the product. This doesn't mean any cooperation with their owners or endorsement by them.
- **Licence texts.** The files in the `LICENSES/` folder contain the standard licence texts. The course's licences don't cover them.

### No warranty

We provide the course and the code without any warranty. The details are in the full texts of both licences.

### Author

Author of the course and copyright holder: Michał Maj (https://github.com/michalmaj).

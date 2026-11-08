# Toolchain checks

`cpp20_smoke/` is a tiny C++20 project that checks whether the official course toolchain can compile, link, run and test a program. The toolchain is upstream LLVM/Clang 22 or newer, used through `clang++`, together with CMake, Ninja and CTest.

This is a check for course maintainers. It is **not** an installation guide for learners.

## Three levels of verification

These are different things. A green run of this check proves only the first.

1. **The toolchain works on a CI runner.** `.github/workflows/toolchains.yml` runs this project on GitHub-hosted Windows, Ubuntu 24.04 and macOS runners. Those runners come with many tools preinstalled, for example full Visual Studio on Windows.
2. **A clean installation works on a learner's computer.** This needs a fresh machine or virtual machine and the exact steps a learner will follow. It is not covered here.
3. **CLion is set up correctly.** This includes toolchain selection, Debug/Release profiles and the debugger. It is a separate, manual check.

## What the project checks

- **Configuration fails** unless the compiler is upstream Clang 22 or newer, with the `clang++` (GNU-style) driver, and on Windows targets the MSVC ABI. AppleClang, GCC, MSVC `cl`, `clang-cl` and MinGW are rejected, so a green run can't come from a silent fallback.
- **It builds** a static library, a program and a test program. This uses the compiler, the archiver and the linker. It uses C++20: concepts, ranges, `std::span`, `std::format`, `operator<=>` and designated initializers.
- **CTest runs two real tests:**
  - `smoke_test` checks the library's results and fails with a message for each wrong one;
  - `program_output` checks the program's output, including whether assertions are compiled in. That proves whether Debug or Release was actually built.
- **The program prints** the compiler version, the C++ standard library it was built against, and `__cplusplus`.

The same workflow also builds the learner project of lesson 0.5 (`course/module_00_tooling/lesson_05_first_program`) in Debug, runs it, and checks the behaviour the lesson describes: after editing `main.cpp` without building, the existing executable still prints the old message; after building it prints the new one; a second build without changes does no work. It works on a copy in `build/`, so the tracked lesson files are never changed.

`lesson_06.ps1` (Windows PowerShell 5.1 and PowerShell 7) and `lesson_06.sh` (bash on Ubuntu, zsh on macOS) run the **exact terminal commands of lesson 0.6** on a temporary copy of that project: CMake configure, build and run; a direct `clang++` compile; and the edit-and-rebuild experiment with three executables. They can be run locally from the repository root, for example `zsh tests/toolchains/lesson_06.sh` or `powershell -NoProfile -ExecutionPolicy Bypass -File tests\toolchains\lesson_06.ps1`.

`lesson_examples.py` checks the **C++ code published in the lessons**: it builds and runs the marked code blocks and compares their output. How lessons mark their code, and what exactly is checked, is described in [Lesson examples](#lesson-examples-lesson_examplespy) below.

`lesson_14.ps1` (Windows PowerShell 5.1 and PowerShell 7) and `lesson_14.sh` (bash on Ubuntu, zsh on macOS) run the **terminal commands of lesson 1.4** on a temporary copy of the lesson 0.5 project: compiling with `clang++ -c` and linking by hand, the `mian` link error, renaming the program in `CMakeLists.txt` and the CMake error for a missing source file. They check files and key messages, never Ninja's step counters such as `[3/4]`.

`lesson_16.ps1` and `lesson_16.sh` check the CMake part of the lesson 1.6 diagnosis task: a `CMakeLists.txt` in which the program was renamed in `add_executable` only must fail at configuration (two `CMake Error` messages, for lines 5 and 6), and the corrected file must build a program called `board_games`. The C++ programs of lesson 1.6 are checked by `lesson_examples.py`.

## Running it locally

From the repository root, with the official toolchain installed. Use the full path to upstream `clang++`, so that CMake can't pick another compiler:

| System | `CXX_COMPILER` used in CI |
|---|---|
| Windows (PowerShell) | `C:\Program Files\LLVM\bin\clang++.exe` (LLVM from Chocolatey) |
| Ubuntu 24.04 | `/usr/bin/clang++-22` (apt.llvm.org) |
| macOS | `$(brew --prefix llvm@22)/bin/clang++` (Homebrew), **not** `/usr/bin/clang++`, which is AppleClang |

Then, for each configuration (`Debug` and `Release`):

```sh
cmake -S tests/toolchains/cpp20_smoke -B build/toolchain-smoke/Debug -G Ninja -DCMAKE_BUILD_TYPE=Debug -DCMAKE_CXX_COMPILER=<CXX_COMPILER>
cmake --build build/toolchain-smoke/Debug
ctest --test-dir build/toolchain-smoke/Debug --output-on-failure
```

`build/` is ignored by Git. The workflow file shows exactly how CI installs the tools and identifies the environment. That is a CI recipe, not a verified procedure for a clean computer.

## Lesson examples: `lesson_examples.py`

`lesson_examples.py` checks the C++ code blocks in the lessons under `course/` (from Module 1 on; a Module 0 lesson is skipped unless it contains markers). This section is for course authors and maintainers: how to mark code in a lesson, and what the check does with it. The script's docstring and its `--self-test` cases are the detailed reference.

### Markers

Code blocks are marked with an HTML comment, which GitHub doesn't show. The marker is a line of its own, **not indented**, directly above the block it describes (blank lines in between are allowed, other text is not):

| Marker | Block | Meaning |
|---|---|---|
| `<!-- example: NAME -->` | ` ```cpp ` | A complete program. It is built and run. |
| `<!-- example: NAME exit=N -->` | ` ```cpp ` | The same, but every run must end with exit code N instead of 0. |
| `<!-- example: NAME source=PATH -->` | ` ```cpp ` | The same, and the code must equal the file PATH (relative to the lesson). Lessons 1.1 and 1.4 use it for the lesson 0.5 `main.cpp`. With both attributes: `source=` first, then `exit=`. |
| `<!-- example: NAME target=function_tests -->` | ` ```cpp ` | The `main.cpp` of a program in several files with a second target, the test program `function_tests`: both are built, and only `function_tests` is run (see [Programs with a test target](#programs-with-a-test-target)). With `exit=N`: `target=` first. Never with `source=`. |
| `<!-- output: NAME -->` | ` ```text ` | The exact expected standard output of one run of NAME. |
| `<!-- input: NAME -->` | ` ```text ` | The standard input of one run of NAME (see [Runs](#runs-standard-input-and-expected-output)). |
| `<!-- broken: NAME at=LINE[:COLUMN] [errors=N] error=REGEX -->` | ` ```cpp ` | A program that must **fail to compile**, with its first error in `main.cpp` at LINE (and COLUMN) and a message matching REGEX; with `errors=N`, `main.cpp` must get exactly N errors. |
| `<!-- broken: NAME in=PATH at=LINE[:COLUMN] [errors=N] error=REGEX -->` | ` ```cpp ` | Only for a program in several files: it must **fail to compile**, with the first error located in its file PATH, a `.cpp` source or a `.hpp` header (see [Compile errors in several files](#compile-errors-in-several-files)). Without `in=`, PATH is `main.cpp`. |
| `<!-- broken: NAME stage=link error=REGEX -->` | ` ```cpp ` | A program that must **compile and then fail to link**, with REGEX matching the build output. |
| `<!-- fragment -->` | ` ```cpp ` | Deliberately incomplete code: never built or run. |
| `<!-- file: NAME PATH -->` | ` ```cpp ` | One more file of program NAME, a `.cpp` source or a `.hpp` header, saved as PATH (see [Programs in several files](#programs-in-several-files)). |
| `<!-- cmake: NAME -->` | ` ```cmake ` | The `CMakeLists.txt` of program NAME, for a program in several files. |
| `<!-- run: NAME -->` | none | A line of its own, **with no code block**: the next run of example NAME, for a program that reads a data file (see [Programs that read a data file](#programs-that-read-a-data-file)). |
| `<!-- datafile: NAME PATH -->` | ` ```text ` | The file PATH that this run of NAME finds in its working directory. |
| `<!-- datafile: NAME PATH noeol -->` | ` ```text ` | The same, without a line end after the last line. |

- **NAME** uses lowercase letters, digits and `_`. Within one lesson, every `example` and `broken` program has its own name; a buggy program and its fixed version get different names. `file` and `cmake` blocks use the NAME of the program they belong to.
- **Attributes** are exactly the ones above, in that order. Anything else makes the marker unreadable and is reported. There is no `warning=` attribute.
- **Every ` ```cpp ` block must have a marker**; an unmarked one is reported. ` ```text ` blocks without a marker are ordinary text.
- **Every `example` needs at least one `output` block.** Every `input` and `output` block needs an `example` of the same name in the same lesson.

Which marker to use:
- a complete program the learner runs, with its exact output: `example` with `output` (and `input`);
- a line, a header or a sketch to read, or code that must not run, such as an endless loop: `fragment`;
- a compile error the learner should see: `broken` with `at=`, and in a program in several files `in=` for a file other than `main.cpp`;
- a link error: `broken` with `stage=link`;
- a program in several files: its `example` or `broken` block for `main.cpp`, a `file` block for each other file, and one `cmake` block;
- a program in several files and a test program built from the same sources: `example` with `target=function_tests`, a `file` block `function_tests.cpp`, and the `CMakeLists.txt` with two targets;
- a program that reads a data file: its `example` block and, for each run, a `run` marker with the run's `datafile`, `input` and `output` blocks.

### Building

Each `example` and each `broken` program is built as `main.cpp` of the lesson 0.5 project (its `CMakeLists.txt`), with CMake, Ninja and the given compiler, in Debug. This happens in a copy under `build/lesson-examples/<lesson>/<name>`; the lessons are never modified. A program in several files brings its own files and `CMakeLists.txt` ([Programs in several files](#programs-in-several-files)); everything else below applies to it too.

- **Examples** are built with `-Wall -Wextra -pedantic-errors -Werror`, so any warning fails the build.
- **Broken programs** are built with the project's own flags only, exactly as a learner builds them, because some messages are warnings on one system and errors on another.
- **Configuring must succeed and report Clang 22 or newer.** Otherwise the result is reported as an environment problem (`configure failed`), never as the expected compile error.

### Broken programs

- **Compile stage (`at=`):**
  - the build must fail with compiler errors in `main.cpp`;
  - the first of them must be at LINE (and COLUMN, if given);
  - REGEX, a Python regular expression, must be found in the message after `error: `;
  - `errors=N` also fixes the number of errors in `main.cpp`.

  In a program in several files, the error may be located in another of its files, named by `in=` ([Compile errors in several files](#compile-errors-in-several-files)).
- **Link stage (`stage=link`):**
  - `main.cpp` must compile without errors (its object file exists);
  - the build must then fail in the linker (`linker command failed`, no executable);
  - REGEX must match the build output.

  Linker messages differ per platform, so REGEX lists the minimal alternatives (GNU `ld`, Apple `ld`, `lld-link`).

  This is for one-file programs; a program in several files has stricter rules ([Programs in several files](#programs-in-several-files)).

The whole build output of every broken program is printed, so the messages on the three systems can be compared. Before pinning a message, check it on all three systems and pin its stable part. For example, lesson 4.3 pins `at=8 errors=1 error=^use of undeclared identifier 'lap'$` after a first run with a permissive `error=.` on the lesson's branch.

### Programs in several files

A program may consist of `main.cpp`, more `.cpp` files and `.hpp` headers, built from its own `CMakeLists.txt`. Its blocks are tied together by NAME, so they may stand anywhere in the lesson, before or after the program's own block:

- the `example` or `broken` block is always `main.cpp`;
- each other file has a `file` block: `<!-- file: NAME PATH -->` above a ` ```cpp ` block, for a source and for a header alike;
- exactly one `cmake` block: `<!-- cmake: NAME -->` above a ` ```cmake ` block.

A program without `file` and `cmake` blocks is a one-file program and is checked exactly as before. A program with any of them needs its own block, at least one `file` block and exactly one `cmake` block.

````markdown
<!-- example: twice -->
```cpp
#include <iostream>

#include "tools.hpp"

int main() {
    int value{0};

    std::cin >> value;
    std::cout << "Twice: " << twice(value) << "\n";
}
```

<!-- file: twice tools.hpp -->
```cpp
#pragma once

int twice(int value);
```

<!-- file: twice tools.cpp -->
```cpp
#include "tools.hpp"

int twice(int value) {
    return value * 2;
}
```

<!-- cmake: twice -->
```cmake
cmake_minimum_required(VERSION 3.28)
project(first_program LANGUAGES CXX)

add_executable(first_program main.cpp tools.cpp)
target_compile_features(first_program PRIVATE cxx_std_20)
set_target_properties(first_program PROPERTIES CXX_EXTENSIONS OFF)
```

<!-- input: twice -->
```text
4
```

<!-- output: twice -->
```text
Twice: 8
```
````

More `input`/`output` pairs give more runs of the same program, as for any example. The markers are invisible on GitHub, so tell the learner the name of each file in the text above its block.

**Before anything is built**, the lesson is checked against these rules. A program that breaks one is reported and not built.

- **File names:**
  - lowercase letters, digits and `_`, starting with a letter, ending in `.cpp` or `.hpp`, at most 24 characters;
  - no folders, `..` or separators;
  - not `main.cpp`;
  - not a name Windows reserves for a device (`con`, `prn`, `aux`, `nul`, `com1`–`com9`, `lpt1`–`lpt9`, with any extension);
  - each name once per program.
- **Every block needs its program:** a `file` or `cmake` block whose NAME has no `example` or `broken` block is reported. So are `file` blocks without a `cmake` block, a `cmake` block without `file` blocks, and a second `cmake` block.
- **`CMakeLists.txt`** must be the lesson 0.5 file, line for line, except the sources of `add_executable(first_program ...)`:
  - one line, the sources separated by single spaces, in any order;
  - `main.cpp` included;
  - only `.cpp` files of the program, with exactly their names, each once; headers are not listed;
  - no other change or command, except the one fixed form with a second target ([Programs with a test target](#programs-with-a-test-target)).

  An `example`, and a `broken` program with a compile error, list all of their `.cpp` files, so a source left out can't hide where an error is. Only a `broken` program with `stage=link` may leave some out: that is how a source missing from the build is shown. A source that isn't a file of the program is reported before CMake runs: CMake would stop at configuration, which a lesson can't use as an expected result.
- **Preprocessor directives** in `main.cpp` and the `file` blocks:
  - comments (`//` and `/* ... */`) are skipped, so a commented-out `#include` is not checked;
  - every other `#include` is either `#include <...>` or `#include "name.hpp"` naming a header of the program **with the same case**. A different case would work on Windows and macOS but not on Linux, so it is reported on every system, in examples and broken programs alike;
  - a header that no file includes is allowed;
  - `#if`, `#ifdef`, `#ifndef` and the other conditional directives are not allowed, because the check doesn't interpret them; headers use `#pragma once`.

**Building:**
- the files are written next to `main.cpp` in `build/lesson-examples/<lesson>/<name>/src`, with the program's `CMakeLists.txt` instead of the lesson 0.5 one;
- configuring is the same as for every program (Debug, Ninja, the compiler, Clang 22 or newer, the same flags);
- building uses one job at a time (`cmake --build DIR -j 1`), so the steps run, and a failed build stops, in the same order on every system.

An example that fails to build is reported with its first failed step, for example `build failed: tools.cpp failed to compile` or `build failed: the program failed to link`.

**Broken programs in several files with `stage=link`** pass only if:
1. configuring succeeded;
2. the build failed;
3. no earlier step failed: no dependency scanning, no compiling, nothing else;
4. the only failed step is the link of `first_program` (`first_program.exe` on Windows), found in Ninja's `FAILED:` lines;
5. every source in `add_executable` has its object file;
6. that step's output contains `linker command failed`;
7. no program was created;
8. REGEX matches that step's output.

A source that fails to compile, or a missing header found at the dependency scan, is reported as the reason the build stopped before linking, never as the expected link error. `in=` is not allowed with `stage=link`: a link error has no file and line to point to.

#### Compile errors in several files

A `broken` program in several files may instead be expected to **fail to compile**:

```text
<!-- broken: NAME in=PATH at=LINE[:COLUMN] [errors=N] error=REGEX -->
```

- **The attributes** come in exactly this order; `in=` is optional, and `at=` is required.
- **`in=PATH`** names the file in which the compiler locates the error:
  - `main.cpp` (the default, so a marker without `in=` means `main.cpp`, as before) or the PATH of one of the program's own `file` blocks, a `.cpp` source or a `.hpp` header;
  - written exactly as that file's name, with the same case;
  - never a folder, another extension, a file of another program or a file the lesson doesn't show.

  A one-file program can't use `in=`: all of its errors are in `main.cpp`.
- **`at=LINE[:COLUMN]`** is the line (and column) of the first error **in that file**, not of the `#include` line that brought a header in.
- **`errors=N`** counts the errors located in PATH in the checked compile step (below). Errors in other files of the same step aren't counted, and nothing is added up over several sources.
- **`error=REGEX`**, a Python regular expression, must be found in the first error's message after `error: `.

Such a program lists **all** of its `.cpp` files in `add_executable`. Building stops at the first failed step (one job at a time), and that step is the one checked. The program passes only if:
1. configuring succeeded and reported Clang 22 or newer;
2. the build failed;
3. the first failed step **compiles one of its sources**. A failed dependency scan (for example a missing `#include <...>` header) or a failed link is reported as such, never taken for the expected compile error;
4. the first compiler error in that step's own output (`file:line:column: error: ...`) is located in PATH, at LINE (and COLUMN), and its message matches REGEX. Notes, `fatal error` lines and the `In file included from main.cpp:4:` lines before an error in a header are not errors;
5. with `errors=N`, exactly N errors of that step are located in PATH.

**A `.cpp` file or a header.** An error in a `.cpp` file, for example `tools.cpp` with a missing `;`, is reported by the step that compiles `tools.cpp`: `in=tools.cpp`. A header isn't compiled by itself. Its errors are reported by a source that includes it, located in the header itself: `record.hpp:1:8: error: redefinition of 'Record'` when `main.cpp` includes `record.hpp` twice without `#pragma once`, so `in=record.hpp at=1:8`. When several sources include a broken header, whichever of them is compiled first fails, with the same location, so the expectation doesn't depend on the order of the sources.

**What is not checked.** Building stops at the first failed step, so a source compiled later isn't compiled at all: an error in it is not seen. Lessons keep one deliberate mistake per broken program, and show the corrected program as an `example`, which builds all of its sources.

**Not supported** (reported, not built):
- a missing header as the expected error: a local `#include "x.hpp"` must name a file of the program, in every program;
- `stage=scan` and `stage=configure`: a dependency scan or a CMake configuration can't be an expected result;
- folders in file names;
- files shared between programs;
- any other `CMakeLists.txt`.

### Programs with a test target

A program in several files may have a **second target**, `function_tests`: a test program built in the same project from the **same sources** as the program. The program proper (`first_program`, built from `main.cpp`) and the tests (`function_tests`, built from `function_tests.cpp`) both compile the shared `.cpp` files, so a change in them is seen by the next run of the tests. There is no library, no CTest and no test framework: the test program is an ordinary program that prints its results and ends with an exit code.

**The marker.** The program's own block is still its `main.cpp`, the program proper. `target=function_tests` says that the `output` block is the output of the test program:

```text
<!-- example: NAME target=function_tests -->
<!-- example: NAME target=function_tests exit=1 -->
```

- `target=` comes before `exit=` and is never combined with `source=`.
- `function_tests` is the only value; `target=tests` or `target=first_program` is reported.
- It is only for an `example` in several files, and only with the `CMakeLists.txt` below. The two go together: that `CMakeLists.txt` without `target=function_tests`, or `target=function_tests` with the one-target `CMakeLists.txt`, is reported.

**The files:**

| File | Block | Built into |
|---|---|---|
| `main.cpp` | the `example` block | `first_program` only |
| `function_tests.cpp` | a `file` block, required | `function_tests` only |
| every other `.cpp` file, for example `rules.cpp` | `file` blocks | both targets |
| `.hpp` headers, for example `rules.hpp` | `file` blocks | included, never listed |

**`CMakeLists.txt`** has exactly ten lines: the lesson 0.5 file with the sources of `first_program`, an empty line, and the same three lines for `function_tests`.

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

- Only the sources of the two `add_executable` lines may differ. Every other line is compared exactly, so both targets use C++20 without extensions, and nothing else is allowed: no `add_library`, `target_link_libraries`, `add_subdirectory`, `enable_testing`, CTest or third target.
- **The two lists of sources:**
  - `first_program` lists `main.cpp` and never `function_tests.cpp`;
  - `function_tests` lists `function_tests.cpp` and never `main.cpp` (each has its own `main` function);
  - every other `.cpp` file of the program is listed by **both** targets, so the shared sources are the same set in both lists, and there is at least one;
  - each list follows the rules of [Programs in several files](#programs-in-several-files): one line, single spaces, each source once, no headers, only files of the program, with exactly their names.
- **A shared header:** `main.cpp` includes a header of the program (`#include "rules.hpp"`), and `function_tests.cpp` includes at least one of the same headers itself. An `#include` in a comment doesn't count, and neither does a name written with another case (which is reported anyway).

**Building and running:**
- The whole project is built, as every program in several files (`cmake --build DIR -j 1`, no `--target`): both targets, in the same order on every system.
- A failed step of **either** target fails the example, although only the tests are run, so a broken program proper can't hide behind passing tests. The message names the step and its target, and nothing is run:
  - `build failed: main.cpp (target first_program) failed to compile`
  - `build failed: rules.cpp (target function_tests) failed to compile`
  - `build failed: first_program failed to link`
  - `build failed: function_tests failed to link`
- After a successful build both programs must exist (`first_program` and `function_tests`, with `.exe` on Windows).
- Only `function_tests` is run, **once**, with an empty standard input, in the checker's working directory. `first_program` is built but not run: running it is the learner's step in the lesson. A lesson that shows the program proper's output shows it as another program, in the usual way.
- That run is judged as every run ([Exit codes and stderr](#exit-codes-and-stderr), [Timeout](#timeout), [Output limit](#output-limit)): the exit code (0, or `exit=N`), an empty stderr, and stdout equal to its **one** `output` block. The log calls it `example NAME (target function_tests)`, and the lesson's summary counts these programs: `1 of these programs with two targets (both built, function_tests run)`.

**Exit codes.** By the course convention, a test program ends with 0 when every check passed and with 1 when it found a mismatch. A lesson that shows the tests catching a bug marks that program `exit=1`, with its `FAIL` lines as the expected output: exit code 1 is then the expected result, not a CI failure. Marked without `exit=1`, the same program fails the check.

Example: a complete program with a test target.

````markdown
<!-- example: parking_tests target=function_tests -->
```cpp
#include <iostream>

#include "rules.hpp"

int main() {
    int hours{0};

    std::cin >> hours;
    std::cout << "Fee: " << parking_fee(hours) << "\n";
}
```

<!-- file: parking_tests rules.hpp -->
```cpp
#pragma once

int parking_fee(int hours);
```

<!-- file: parking_tests rules.cpp -->
```cpp
#include "rules.hpp"

int parking_fee(int hours) {
    if (hours < 0 || hours > 8) {
        return -1;
    }

    if (hours == 0) {
        return 0;
    }

    return 5 + 3 * (hours - 1);
}
```

<!-- file: parking_tests function_tests.cpp -->
```cpp
#include <iostream>
#include <string>

#include "rules.hpp"

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

    check_int("parking_fee(0)", 0, parking_fee(0), checks, failed);
    check_int("parking_fee(1)", 5, parking_fee(1), checks, failed);
    check_int("parking_fee(2)", 8, parking_fee(2), checks, failed);
    check_int("parking_fee(9)", -1, parking_fee(9), checks, failed);

    std::cout << "Checks: " << checks << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

<!-- cmake: parking_tests -->
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

<!-- output: parking_tests -->
```text
PASS parking_fee(0)
PASS parking_fee(1)
PASS parking_fee(2)
PASS parking_fee(9)
Checks: 4, failed: 0
```
````

With a bug in `rules.cpp`, the same tests fail. That is another program, with all of its blocks repeated under its own name (blocks aren't shared between programs):

| `rules.cpp` returns | `function_tests` prints | Exit code | Marker |
|---|---|---|---|
| `5 + 3 * (hours - 1)` | four `PASS` lines, then `Checks: 4, failed: 0` | 0 | `target=function_tests` |
| `5 + 2 * (hours - 1)` | `FAIL parking_fee(2): expected 8, actual 7` among the `PASS` lines, then `Checks: 4, failed: 1` | 1 | `target=function_tests exit=1` |

**Before anything is built**, mistakes are reported with the rule they break, and the program is not built:

| Mistake | Message (shortened) |
|---|---|
| `target=tests` | `unknown target tests (an example can name only target=function_tests)` |
| `exit=1 target=function_tests` | `cannot read the example marker (expected target=function_tests [exit=N], in this order)` |
| `source=` and `target=` | `target= can't be combined with source= …` |
| `target=function_tests` in a one-file program | `target=function_tests is only for a program in several files with two targets` |
| `target=function_tests` with the one-target `CMakeLists.txt` | `target=function_tests needs the CMakeLists.txt with two targets …` |
| the `CMakeLists.txt` with two targets, without `target=` | `a CMakeLists.txt with two targets needs target=function_tests on the example` |
| `cxx_std_17`, a missing line, no empty line, `enable_testing()`, a third `add_executable` | `the cmake block differs from the CMakeLists.txt with two targets …` |
| no `function_tests.cpp` file block | `target=function_tests needs a file block function_tests.cpp, …` |
| `main.cpp` in `function_tests` | `function_tests must not list main.cpp (it has its own main function)` |
| `function_tests.cpp` in `first_program` | `first_program must not list function_tests.cpp (it has its own main function)` |
| `rules.cpp` in `first_program` only | `rules.cpp is listed by first_program but not by function_tests (the tests build from the same sources as the program)` |
| no shared `.cpp` file | `first_program and function_tests share no .cpp file, …` |
| a `.cpp` file in neither list | `helper.cpp is in neither add_executable …` |
| a header, a source twice, another case or a missing file in a list | `add_executable(function_tests ...) lists the header rules.hpp: …`, and the other messages of one list |
| `function_tests.cpp` without a header that `main.cpp` includes | `function_tests.cpp includes none of the headers of the program that main.cpp includes (rules.hpp), so the two targets share no interface` |
| an `input` block, a `run` marker or a data file | `an example with target=function_tests runs once, with an empty standard input: …` |
| a second `output` block | `an example with target=function_tests has exactly one output block, not 2` |
| a `broken` program with two targets, or `target=` on a `broken` marker | `a broken program has one target …`, `cannot read the broken marker (target= is only for an example: …)` |

**What the check guarantees, and what it doesn't:**
1. **The structure, before building:** the marker, the exact `CMakeLists.txt`, the two lists of sources (each program's own `main` file in its own target only, the same shared `.cpp` files in both) and a shared header. This is read from the text, without interpreting CMake or C++.
2. **Both targets build:** the whole project is built, so both programs compile and link from the same shared sources. A failure of either fails the example.
3. **The behaviour of each example:** the test program's exact output and exit code are compared with the lesson. That is what a given example shows: for example, a faulty shared source marked `exit=1` with its `FAIL` lines shows, by running, that these tests detect it.
4. **What it doesn't decide:** which function each check calls. A shared header and shared sources show a common interface and a common implementation in the build, **not** that every check uses the program's function: tests that call a copy under another name, or check nothing useful, would still pass. Telling that apart needs an analysis of the C++ code, which the check doesn't do; it stays a review task. A copy with the same name as a shared function fails to link, and a `static` copy fails to compile in a file that includes the function's header, but those are results of the compiler and the linker, not rules of the check.

**Not supported** (reported, not built): `input` blocks, `run` markers and data files in such an example; running `first_program` in it; a `broken` program with two targets; any other target name; a third target; a library, CTest or a test framework. The mistake "the tests added to the program's own target" is an ordinary one-target `broken` program with `stage=link`: with `add_executable(first_program main.cpp rules.cpp function_tests.cpp)`, the link fails with two `main` functions.

**Compatibility:** a marker without `target=` means what it meant before, and a `CMakeLists.txt` without an `add_executable(function_tests ...)` line is checked by the one-target rules, with the same messages. In a program with one target, `function_tests.cpp` is an ordinary file name.

### Runs, standard input and expected output

An example is **built once**, and the same executable is used for all of its runs:

- **Without `input` blocks:** one run with an empty standard input (no data at all).
- **With `input` blocks:** one run per `input` block, in the order of the lesson.
  - The `output` blocks that follow an `input` block, up to the next `input` block of the same name, are the expected output of that run.
  - An `output` block before the first `input` block, and an `input` block with no `output` block after it, are reported.
  - **Pairing is by order only,** never by content.

  The example's own code block may stand anywhere in the lesson, for example after its runs, in a collapsed solution.

If a run has several `output` blocks, **each of them** must equal the output. So don't repeat an output block "for the reader" after another run, unless it is identical.

**Standard input:**
- The text of an `input` block, which always ends with a line end, is written to the program through a pipe. The pipe is then closed, so after the last line the program sees the **end of its input**: a further `std::cin >>` that needs data fails.
- An empty `input` block gives one empty line.
- Nothing is typed, so nothing is echoed: standard output is the program's output alone, without the input that a terminal or CLion would show.
- **Each run is a new process** with its own standard input; runs share nothing but the executable.

**Standard output:**
- The output is decoded (ASCII) and Windows line ends (`\r\n`) become `\n`. It must then **equal the `output` block exactly**, including its final line end.
- A program whose output doesn't end with `\n` can't match, because every block ends with one.

Example: one program, two independent runs.

````markdown
<!-- example: double_it -->
```cpp
#include <iostream>

int main() {
    int number{0};

    std::cout << "Enter a number:\n";
    std::cin >> number;
    std::cout << "Double: " << number * 2 << "\n";
}
```

<!-- input: double_it -->
```text
4
```

<!-- output: double_it -->
```text
Enter a number:
Double: 8
```

<!-- input: double_it -->
```text
-3
```

<!-- output: double_it -->
```text
Enter a number:
Double: -6
```
````

In a lesson, the outputs are usually inside `<details>` blocks, so that a prediction comes first. That changes nothing for the check: markers inside `<details>` work the same.

### Programs that read a data file

A program that opens a file with a relative name, such as `std::ifstream input{"steps.txt"};`, looks for it in its **working directory**. Such an example declares **each of its runs** with a `run` marker, and the checker gives each run a new folder of its own, holding only that run's data file.

````markdown
<!-- example: steps -->
```cpp
...the program, which opens steps.txt...
```

<!-- run: steps -->

<!-- datafile: steps steps.txt -->
```text
4200
7350
```

<!-- output: steps -->
```text
Total steps: 11550
```

<!-- run: steps -->

<!-- output: steps -->
```text
Cannot open steps.txt
```
````

**Runs:**
- `<!-- run: NAME -->` is a line of its own, with **no code block** after it, and starts the next run of example NAME. Runs are numbered from 1, in the order of their markers, and the log names them `example steps (run 2 of 2)`.
- The `input`, `datafile` and `output` blocks of NAME after a `run` marker, up to NAME's next `run` marker, belong to that run. Blocks of other programs may stand in between: each block belongs to the program it names. The `example` block itself may stand anywhere, before the runs or after them.
- **Each run has:**
  - at most one `input` block: without it, the run gets an **empty standard input** (the end of input at once, never the checker's own);
  - at most one `datafile` block: without it, the run's folder is **empty**, so the program finds no file;
  - **exactly one** `output` block.
- **A run with neither** `input` nor `datafile` is a valid run: it tests what the program does when its file is missing.
- **An example with `run` markers has all of its `input` and `output` blocks in its runs.** One before its first `run` marker is reported, because the old and the new way of grouping runs never mix in one example.
- `run` and `datafile` are only for an `example`: a `broken` program is never run.
- **An example without `run` markers is checked exactly as before** ([Runs](#runs-standard-input-and-expected-output)): in the checker's own working directory, and without data files. A `datafile` block in such an example is reported.

**The data file:**
- **PATH** is the file's name in the working directory:
  - lowercase letters, digits and `_`, starting with a letter, ending in `.txt`, at most 24 characters (the rule of [file blocks](#programs-in-several-files), with `.txt`);
  - no folders, `/`, `\`, `..` or spaces;
  - not a name that Windows reserves (`con.txt`, `nul.txt`, `com1.txt`…).

  Before writing, the checker also makes sure that the file lands inside the run's folder.
- **Its bytes are the block's lines, each followed by one line end (LF):** no BOM, no CR, no change to spaces or tabs.
  - An **empty block** is an empty file (zero bytes);
  - a block of **one empty line** is a file of one line end;
  - a block ending with an empty line is a file whose last line is empty.
- **`noeol`** leaves out the final line end only (`Alpha` instead of `Alpha\n`). It isn't allowed on an empty block (nothing to leave out) or after an empty last line (those bytes have their own form: the block without that line and without `noeol`). It is only for data files: `input` and `output` blocks don't take it.
- **The data are ASCII,** like every marked block: printable characters, spaces and tabs. Other control characters are reported, and so are, in a lesson with data files, characters such as `\v` that would split one line of the block into two.

**The working directory:**
- Each run gets a new, empty folder, `build/lesson-examples/<lesson>/<NAME>/run_<N>`, as its working directory. Only that run's data file is written there, and nothing of other runs or of the build.
- The program is started by its absolute path.
- **After the run the folder is removed,** whatever the result: a pass, a wrong output, an exit code, stderr, a timeout, the output limit, or a program that couldn't be started. A folder still locked on Windows is retried a few times; if it can't be removed, that is reported as a problem.
- Exit codes, stderr, the timeout and the output limit are checked as for every run.

**Before anything is built,** these are reported, and the example isn't built or run:
- a `run` or `datafile` marker that can't be read: other attributes, `noeol` twice, or another order;
- a `run` or `datafile` of a program that isn't an `example` of the lesson;
- a `datafile` without a `run`;
- an `input` or `output` block before the first `run` of its example;
- a second `input`, `datafile` or `output` block in one run, or a run without an `output` block;
- a bad PATH;
- `noeol` where it isn't allowed;
- control characters;
- a fence other than ` ```text `;
- a `run` marker directly followed by a code block (mark the block, or put text between them).

### Exit codes and stderr

- **Exit code:**
  - every run must exit with 0, or with the example's `exit=N`;
  - `exit=N` applies to **every run** of that example; there is no exit code per run;
  - another code is reported as `exit code X, expected N`.
- **stderr** must be **empty** in every run; anything on it is reported as `printed to stderr: …`. Standard output and standard error are captured and checked separately.
- **A course convention, not a checker rule:** programs that reject a value print a message on **stdout** and end normally, with exit code 0. They never exit with an error code on their own.
- **Output mismatch:** a run that ends in time but prints something else is reported as `output '…', expected '…'`. Several problems of one run are reported together.
- **Mismatch vs `broken`:** a mismatch means that an `example` failed. A `broken` program is one that is *meant* not to build. If it builds, that is reported too.

### Timeout

- **Per run:** each run may take at most `--timeout` seconds; the default is **10**, and the CI workflow uses the default.
- **When exceeded:** the program is stopped and the run is reported as `did not finish within 10 s`. Checking then continues with the next run.
- **What it is for:** the timeout detects programs that don't end. It never replaces a program's own ending condition: a correct example ends by itself, well within the limit.
- **What it isn't:** it isn't a guarantee that any program is safe to run.

### Output limit

Each run may print **at most 65,536 bytes (64 KiB) to stdout**, and separately **at most 65,536 bytes to stderr**:
- Exactly 65,536 bytes is allowed; 65,537 on a stream fails the run.
- The bytes are counted **as the program writes them**, before decoding and before `\r\n` becomes `\n`.
- The limit is applied **while the program runs**: each stream is read as it is written, and the checker keeps at most one byte more than the limit. As soon as a stream goes over, the program is **stopped**, and the run is reported as `stdout exceeded the 65536-byte limit, so the program was stopped` (or `stderr …`).
- It isn't a truncation of finished output.

Three different failures:

| Failure | Meaning |
|---|---|
| **Output limit exceeded** | The program printed more than 64 KiB on one stream; it was stopped at once. |
| **Execution timeout** | The program didn't end within `--timeout` seconds; it was stopped then. |
| **Output mismatch** | The program ended in time, within the limit, but its stdout differs from the expected output (or it printed to stderr, or ended with another exit code). |

Failure messages and the log of passing runs show at most **1,000 characters** of a program's output, followed by `… more characters, not shown`. This way a large output never ends up in full in the CI log.

### Polish and English lessons

- For every `X.md` there must be an `X.en.md`.
- **The marked blocks of the two files must be the same list:** the same markers (kind, name, attributes) with byte-identical code, input and expected output, in the same order. Fragments, broken programs, `file` and `cmake` blocks are included, and so are `run` markers and `datafile` blocks.
  - So both lessons have the same runs in the same order, with the same file names, `noeol` and data, **byte for byte**: an empty data file and a file of one line end are different.
- **Marked blocks must be ASCII,** so code, input and output contain no Polish characters.
- **Nothing else is compared:** prose, headings, tables and unmarked blocks aren't checked. The check says nothing about whether the two lessons explain the same things equally well; that remains a review task.

### Self-test and CI

- **What it does:** `--self-test` runs the same check on small fixture lessons in a temporary folder, and verifies the **verdicts**: correct fixtures must pass, and deliberately wrong ones must be reported for the right reason.
- **The wrong fixtures include:**
  - a wrong output or exit code;
  - a broken program that compiles;
  - a different first error, line or number of errors;
  - a PL/EN difference;
  - an unmarked block;
  - a broken environment;
  - wrongly paired `input`/`output` blocks;
  - a program that never ends;
  - since PR #35, the output limit: exactly 65,536 and 65,537 bytes on each stream (written without line ends, so the byte counts are the same on Windows), programs that flood stdout or stderr, writing to both streams in turns, and short failure messages.
- **Programs in several files** have two kinds of fixtures:
  - **checked before anything is built:** markers, missing and repeated blocks, file names, `CMakeLists.txt`, `#include` lines (also one commented out), conditional directives, and the refusal of what isn't supported. Each of these must be reported with nothing built;
  - **really built with CMake and Ninja on every system:** a program with two `.cpp` files and a header and two runs, a wrong output and an exit code, a one-file example next to it built as before, a link error from a source left out of `add_executable`, a compile error, a scan error and a build that succeeds where a link error was expected, a different linker message, an example that fails to compile or to link, a PL/EN difference, and a broken environment.
- **Compile errors in several files (`in=`)** have both kinds too:
  - **checked before anything is built:** `in=` with `stage=link`, without `at=` or in another order, a PATH that isn't a file of the program (another program's file, a folder, another extension, another case), `in=` in a one-file program, a source left out of `add_executable`, and a missing header, still refused;
  - **really built:** an error in a second `.cpp` file; an error in a header included by two sources; `Record` defined twice in one translation unit, located in `record.hpp`, and the same header with `#pragma once`, which builds and runs; a header that uses a type without including its header; and the wrong expectations: another file (also the `#include` line in `main.cpp` just before an error in the header), another line, column, message or number of errors, a build that succeeds, a scan error, a link error, a broken environment and a PL/EN difference in `in=`.

  Static checks can't show that building works: only the second kind can.
- **Parts (`--shard`)** have their own fixtures, mostly lessons with only a fragment, so that nothing is built:
  - invalid values;
  - parts that are disjoint and cover every lesson (1–5 lessons, 1–3 parts);
  - an odd number of lessons;
  - the unchanged summary without `--shard`;
  - a problem found before building, reported by a part that doesn't build that lesson;
  - a program in several files built whole by its own part;
  - a part without lessons;
  - a failing program that fails only its own part;
  - an example with `run` markers, run whole by its own part with the same verdicts as without `--shard`.
- **Programs that read a data file:**
  - the exact bytes each run's program reads: a line end, `noeol`, an empty file, one empty line, an empty last line, spaces and a tab, and no file;
  - a new folder per run with only its own file (a file, then none, then the same name with other content) in a program in several files, with no run folder left afterwards;
  - an empty standard input without an `input` block, and a run with both an input and a data file;
  - two programs whose blocks alternate;
  - a PL/EN difference of one byte (an empty file against one line end);
  - bad names (uppercase, `../`, a Windows device name, another extension, no extension, too long, a space);
  - misused markers and attributes, and problems in the structure of runs, each reported with nothing built;
  - lines that look like markers but aren't, next to ordinary HTML comments, which stay text;
  - control characters;
  - failing runs (output, exit code, stderr, timeout, output limit) with no folder left;
  - an example without `run` markers, which keeps its runs and the checker's working directory;
  - and, run directly: a folder left from before, a name that would leave the folder, and a program that can't be started.
- **Programs with a test target** have both kinds:
  - **checked before anything is built:** bad `target=` markers (another value, a one-file program, another order, with `source=`), a marker and a `CMakeLists.txt` that don't go together, a `CMakeLists.txt` that differs from the form with two targets, wrong lists of sources (each `main` file in the wrong target, a shared source missing from one list, no shared source, a `.cpp` file in neither), the rules of one list applied to the second, `main.cpp` and `function_tests.cpp` without a header in common (also through an `#include` in a comment or written with another case), `input` and `run` blocks and a second `output` block, and a `broken` program with two targets or `target=`;
  - **really built:** a correct program, with both programs and both object files of the shared `rules.cpp` checked; a bug in `rules.cpp` caught by the tests with `exit=1`, and the same bug failing an example that expects every check to pass; a one-file example and a one-target program built as before next to it; a compile error in `main.cpp` and a link error of `first_program`, which fail the example although only the tests are run; a compile error in `function_tests.cpp`; a copy of the tested function in the tests, which fails to link although it would hide the bug; and `function_tests.cpp` added to `first_program` as a one-target `broken` program with `stage=link` (two `main` functions).
- **Size:** the self-test has 145 cases in the current repository; the number grows with the checker and isn't a requirement.
- **Workflow:** `.github/workflows/toolchains.yml` runs both modes on Windows (MSVC ABI), Ubuntu 24.04 and macOS. Locally, from the repository root, with the official compiler:

```sh
python3 tests/toolchains/lesson_examples.py --cxx /usr/bin/clang++-22 [--make-program /usr/bin/ninja]
python3 tests/toolchains/lesson_examples.py --self-test --cxx /usr/bin/clang++-22
```

### Parts of the course (`--shard K/N`)

Building and running every example takes most of the Windows job's time, so on Windows that work is split between two jobs. `--shard K/N` (1 ≤ K ≤ N, for example `--shard 1/2`) does it without listing any lesson:

- **Every lesson is still read and checked before building,** in every part: the English version, unmarked blocks, PL/EN, markers, names, inputs and outputs, and the files and `CMakeLists.txt` of programs in several files. A problem in any lesson fails every part.
- **Only the building and running is split, by whole lessons.** The checked lessons, in sorted order and numbered from 0, go to part (number % N) + 1: in two parts, the 1st, 3rd, 5th… lesson to part 1 and the 2nd, 4th… to part 2. All programs of a lesson, with all their runs and files, are built by the same part. A new lesson needs no configuration, and the parts don't depend on the system or on timing.
- **The log says which part builds each lesson** (`part 2 of 2: built and run by that part, not by this one (1 of 2)`), prints the size of every part, and ends with its own summary, which never claims the whole course: `PASSED: part 1 of 2: 70 lesson file(s) read, 64 lesson(s) checked before building, 32 of them built and run in this part (197 example(s), 11 broken program(s), 566 run(s)), 0 problem(s)`.
- **A part without lessons fails** (use fewer parts).
- **Without `--shard`, nothing changes:** every lesson is built, and the log, including its last line, is as before. Ubuntu and macOS run the whole course in one job.

The workflow's two Windows jobs run `--shard 1/2` (with the self-test and the other checks) and `--shard 2/2`, and the workflow fails if either fails. Each job installs the same LLVM; nothing is shared between them.

### What the check doesn't verify

It checks the reference programs and the published data. It does **not** check:
- whether learners understand a lesson, or how long the exercises take;
- the CLion debugger, or typing input into CLion's Run window;
- whether a program is correct for inputs that aren't published, or robust against arbitrary input (for example text where a number is expected);
- compiler warnings as an expected result: examples must have none, and a `broken` program can only expect errors;
- one exit code per run (only per example), or a run whose input doesn't end with a line end;
- in a program that reads a data file: more than one data file per run, folders, files the program writes, a file that exists but can't be opened, data files with CRLF line ends or non-ASCII text;
- processes started by an example: lesson programs start none, and the check doesn't manage them;
- the CMake configure and build output, which isn't limited like a program's output;
- in a program in several files: a missing header, a dependency-scan error or a CMake error at configuration as the expected result, an error in a source compiled after the one that failed, folders, or a `CMakeLists.txt` other than the lesson 0.5 one with its sources (see [Programs in several files](#programs-in-several-files));
- in a program with a test target: which function each check calls, the output of `first_program`, or how CLion shows and runs the two targets (see [Programs with a test target](#programs-with-a-test-target)).

Two authoring traps:
- **Markers and code fences must start at the beginning of the line.** An indented block, for example inside a list item, isn't recognised: an indented ` ```cpp ` block is neither checked nor reported as unmarked.
  - A line that **looks like** a marker (the name of a kind, or its plural, then a colon, however spaced or indented, or `fragment`) must be one exactly, or it is reported: `<!--run: steps-->`, `  <!-- run: steps -->`, `<!-- datafiles: … -->`, `<!-- output : … -->`.
  - Other HTML comments, such as `<!-- TODO: … -->` or `<!-- run the program twice -->`, are ordinary text.
  - A marker without its colon (`<!-- datafile steps steps.txt -->`) isn't recognised as one.
- **A case named in prose or in a table is only checked if it has its own `input`/`output` pair.**

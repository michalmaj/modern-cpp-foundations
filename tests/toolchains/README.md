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
| `<!-- output: NAME -->` | ` ```text ` | The exact expected standard output of one run of NAME. |
| `<!-- input: NAME -->` | ` ```text ` | The standard input of one run of NAME (see [Runs](#runs-standard-input-and-expected-output)). |
| `<!-- broken: NAME at=LINE[:COLUMN] [errors=N] error=REGEX -->` | ` ```cpp ` | A program that must **fail to compile**, with its first error in `main.cpp` at LINE (and COLUMN) and a message matching REGEX; with `errors=N`, `main.cpp` must get exactly N errors. |
| `<!-- broken: NAME stage=link error=REGEX -->` | ` ```cpp ` | A program that must **compile and then fail to link**, with REGEX matching the build output. |
| `<!-- fragment -->` | ` ```cpp ` | Deliberately incomplete code: never built or run. |

- **NAME** uses lowercase letters, digits and `_`. Within one lesson, every `example` and `broken` program has its own name; a buggy program and its fixed version get different names.
- **Attributes** are exactly the ones above, in that order. Anything else makes the marker unreadable and is reported. There is no `warning=` attribute.
- **Every ` ```cpp ` block must have a marker**; an unmarked one is reported. ` ```text ` blocks without a marker are ordinary text.
- **Every `example` needs at least one `output` block.** Every `input` and `output` block needs an `example` of the same name in the same lesson.

Which marker to use:
- a complete program the learner runs, with its exact output: `example` with `output` (and `input`);
- a line, a header or a sketch to read, or code that must not run, such as an endless loop: `fragment`;
- a compile error the learner should see: `broken` with `at=`;
- a link error: `broken` with `stage=link`.

### Building

Each `example` and each `broken` program is built as `main.cpp` of the lesson 0.5 project (its `CMakeLists.txt`), with CMake, Ninja and the given compiler, in Debug. This happens in a copy under `build/lesson-examples/<lesson>/<name>`; the lessons are never modified.

- **Examples** are built with `-Wall -Wextra -pedantic-errors -Werror`, so any warning fails the build.
- **Broken programs** are built with the project's own flags only, exactly as a learner builds them, because some messages are warnings on one system and errors on another.
- **Configuring must succeed and report Clang 22 or newer.** Otherwise the result is reported as an environment problem (`configure failed`), never as the expected compile error.

### Broken programs

- **Compile stage (`at=`):**
  - the build must fail with compiler errors in `main.cpp`;
  - the first of them must be at LINE (and COLUMN, if given);
  - REGEX, a Python regular expression, must be found in the message after `error: `;
  - `errors=N` also fixes the number of errors in `main.cpp`.
- **Link stage (`stage=link`):**
  - `main.cpp` must compile without errors (its object file exists);
  - the build must then fail in the linker (`linker command failed`, no executable);
  - REGEX must match the build output.

  Linker messages differ per platform, so REGEX lists the minimal alternatives (GNU `ld`, Apple `ld`, `lld-link`).

The whole build output of every broken program is printed, so the messages on the three systems can be compared. Before pinning a message, check it on all three systems and pin its stable part. For example, lesson 4.3 pins `at=8 errors=1 error=^use of undeclared identifier 'lap'$` after a first run with a permissive `error=.` on the lesson's branch.

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
- **The marked blocks of the two files must be the same list:** the same markers (kind, name, attributes) with byte-identical code, input and expected output, in the same order. Fragments and broken programs are included.
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
- **Size:** the self-test has 36 cases in the current repository; the number grows with the checker and isn't a requirement.
- **Workflow:** `.github/workflows/toolchains.yml` runs both modes on Windows (MSVC ABI), Ubuntu 24.04 and macOS. Locally, from the repository root, with the official compiler:

```sh
python3 tests/toolchains/lesson_examples.py --cxx /usr/bin/clang++-22 [--make-program /usr/bin/ninja]
python3 tests/toolchains/lesson_examples.py --self-test --cxx /usr/bin/clang++-22
```

### What the check doesn't verify

It checks the reference programs and the published data. It does **not** check:
- whether learners understand a lesson, or how long the exercises take;
- the CLion debugger, or typing input into CLion's Run window;
- whether a program is correct for inputs that aren't published, or robust against arbitrary input (for example text where a number is expected);
- compiler warnings as an expected result: examples must have none, and a `broken` program can only expect errors;
- one exit code per run (only per example), or a run whose input doesn't end with a line end;
- processes started by an example: lesson programs start none, and the check doesn't manage them;
- the CMake configure and build output, which isn't limited like a program's output.

Two authoring traps:
- **Markers and code fences must start at the beginning of the line.** An indented block, for example inside a list item, isn't recognised: an indented ` ```cpp ` block is neither checked nor reported as unmarked.
- **A case named in prose or in a table is only checked if it has its own `input`/`output` pair.**

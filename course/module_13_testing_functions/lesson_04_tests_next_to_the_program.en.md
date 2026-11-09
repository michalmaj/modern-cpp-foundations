# Lesson 13.4: Tests next to the program

[Polski](lesson_04_tests_next_to_the_program.md) · **English** · [Course overview](../../README.en.md)

> **Module 13, lesson 4** · about 90–110 minutes, can be split into two sessions
> **You need:** your `cpp-workspace` folder and the original `lesson_05_first_program` project, as before. Your solution of the lesson 13.2 mission, with the function `is_valid_slot`, will be useful too.
> **Pilot version.** The projects in this lesson are checked automatically on Windows, Ubuntu and macOS: in each of them both programs are built and the test program is run, together with its exit code. The steps in CLion (new files, reloading the CMake project, choosing the program in the toolbar, **Build Project**) are described according to the CLion 2026.3 documentation, without a manual check on every system.

## Before you start

This lesson assumes that:

- you write a test program as in lessons 13.1–13.3: the expected result from the contract, a check function such as `check_int` or `check_bool`, counters of checks and failures, the summary `Checks: N, failed: F` and exit code 0 or 1;
- you build a program from several files: declarations in a `.hpp` header with `#pragma once`, definitions in a `.cpp` file that includes this header, and every `.cpp` file listed in `add_executable` (lessons 11.1–11.4);
- you tell a compile error from a link error, and you know that two definitions of the same function in two `.cpp` files are reported by the linker (lesson 11.4);
- after changing `CMakeLists.txt`, you reload the CMake project in CLion (lesson 11.1);
- you know that CLion runs a program according to a run configuration, such as `first_program` (lesson 12.1).

## The situation

The parking machine at the library calculates the fee with the function `parking_fee` from lesson 13.1. Its tests were written then in a separate program, in which the function was written once more, next to the tests. That was enough to start with. Now the machine's program and the tests are to live side by side for a long time, and the price list will change one day. In this lesson you will answer the question: **how do you organise a project so that the tests check exactly the function the program uses?**

After this lesson you will:

- split the application program and the test program into two files, each with its own `main` function;
- put the declaration of the tested function into a shared header, and its only definition into one `.cpp` file;
- describe in `CMakeLists.txt` two programs that use the same `.cpp` file;
- build both programs and run each of them separately in CLion;
- recognise a regression: a change in the shared file breaks something that worked before, and the tests detect it;
- tell a link error with two `main` functions in one program from a `FAIL` in the tests.

## 1. Two copies of one function

Start from the organisation you know. There are two separate projects, each with one `main.cpp` file:

```text
the machine's project               the tests' project, as in lesson 13.1
  main.cpp                            main.cpp
    parking_fee   <- copy 1             parking_fee   <- copy 2
    main: prints the fee                check_int and main: PASS or FAIL
```

The tests check copy 2, while the machine calculates with copy 1. As long as both copies are identical, the test results also say something about the machine. But nobody keeps an eye on that:

| What happened | The machine's program | The test program |
|---|---|---|
| Someone changed `parking_fee` in the machine and made a mistake | calculates wrongly | still `PASS`: it checks the old copy |
| Someone fixed a bug in the test program only | still calculates wrongly | `PASS` |
| Someone changed the price list in the machine, but not in the tests | uses the new price list | checks the old price list |

In each of these cases the tests pass or fail because of the **copy**, not because of the function the machine uses. **Tests of a copy check the copy.**

The solution: one definition of the function, used by both programs. The program and its tests then become one project.

**Not every small program needs its own test program from the start.** An exercise with one function and one run can do without it. This organisation pays off when:

- the program grows, and so does the number of functions;
- a function is used in several places of the program;
- the tests are meant to stay, not just for one check;
- the implementation of the function will change;
- after every change you want to run the same checks.

## 2. The plan: one function, two programs

**The key idea of this lesson: the program and the tests have separate `main` functions, but they use the same functions.**

The project has five files:

| File | Role | Contains | Doesn't contain |
|---|---|---|---|
| `rules.hpp` | the shared header | the declaration of `parking_fee` | a definition |
| `rules.cpp` | **the shared implementation** | the only definition of `parking_fee` | a `main` function |
| `main.cpp` | **the application program** | the machine's `main`: a call of the function and the printed fee | a definition of `parking_fee`, tests |
| `function_tests.cpp` | **the test program** | `check_int` and a `main` with the tests | a definition of `parking_fee` |
| `CMakeLists.txt` | the build plan | two programs and their files | |

```text
                      rules.hpp (declaration)
                     /                      \
             main.cpp                        function_tests.cpp
          + rules.cpp                      + rules.cpp
                |                                  |
       the application program              the test program
```

- Each program has **exactly one** `main` function, where its execution starts. That is why `main.cpp` and `function_tests.cpp` belong to two different programs.
- Both programs are built from **the same** `rules.cpp` file. There is no second copy of the function, so there is nothing to keep in step.
- The application program knows nothing about the tests. The test program knows nothing about what the machine prints. Only `rules.hpp` and `rules.cpp` connect them.

## 3. Prepare the files of the project

In `cpp-workspace`, create a folder `lesson_13_4` and copy `main.cpp` and `CMakeLists.txt` from the original `lesson_05_first_program` into it. Open it in CLion as in lesson 11.1: **File | Open**, then **Trust Project** and the **Debug** profile.

Create three new files next to `main.cpp`, as in Module 11:

- `rules.hpp`: **New | C/C++ Header File**, the type `.hpp`, and replace the content of CLion's template with the text below (lesson 11.2);
- `rules.cpp` and `function_tests.cpp`: **New | C/C++ Source File**, the type `.cpp`, without the option **Create an associated header** (lesson 11.1).

If CLion offers to add a file to a target (**Add to targets**), you don't need to use it: you will write both lists of files in section 4 and compare them with the ones shown there.

**`rules.hpp`**, the declaration:

<!-- file: parking_project rules.hpp -->
```cpp
#pragma once

int parking_fee(int hours);
```

**`rules.cpp`**, the only definition. It is the function from lesson 13.1, unchanged. The file includes its own header, as in lesson 11.2:

<!-- file: parking_project rules.cpp -->
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

**`main.cpp`**, the application program. Replace the content of the copied file with it:

<!-- example: parking_project target=function_tests -->
```cpp
#include <iostream>

#include "rules.hpp"

int main() {
    const int hours{2};

    std::cout << "Parking hours: " << hours << "\n";
    std::cout << "Fee: " << parking_fee(hours) << "\n";
}
```

The program reads no data: the number of hours is a constant, so that the result depends on the function only. A real machine would read it, like the programs of Module 10.

**`function_tests.cpp`**, the test program:

<!-- file: parking_project function_tests.cpp -->
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
    check_int("parking_fee(3)", 11, parking_fee(3), checks, failed);
    check_int("parking_fee(8)", 26, parking_fee(8), checks, failed);
    check_int("parking_fee(9)", -1, parking_fee(9), checks, failed);

    std::cout << "Checks: " << checks << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

- `check_int` and the check counter `checks` are as in lesson 13.3. Here each case is one check.
- **This file has no definition of `parking_fee`.** Every call `parking_fee(...)` goes to the function in `rules.cpp`, the same one that `main.cpp` uses.
- The expected results are numbers from the contract of lesson 13.1, not calls of the function and not a copy of its formula (lesson 13.1, section 9):

| Case | `hours` | Expected result | Why |
|---|---:|---:|---|
| A | 0 | 0 | no parking |
| B | 1 | 5 | the first hour |
| C | 2 | 8 | 5 + 3 |
| D | 3 | 11 | 5 + 3 + 3 |
| E | 8 | 26 | 5 + 7 · 3 |
| F | 9 | -1 | outside the range 0–8 |

Don't build the program yet: first both programs have to be described in `CMakeLists.txt`.

## 4. Two targets in `CMakeLists.txt`

Since lesson 0.5, `CMakeLists.txt` has described one program: the line `add_executable(first_program main.cpp)`. In Module 11 more `.cpp` files appeared on that list, after `main.cpp`. Here you change the file in two steps:

1. **The application program**, as in Module 11: you build `first_program` from `main.cpp` and `rules.cpp`.
2. **The test program, the new part:** below it, an empty line and three lines for a second program, `function_tests`.

The whole file:

<!-- cmake: parking_project -->
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

- A **target** is something CMake builds, here: a program. Its name is the first word in `add_executable`. Since lesson 0.5 you have known one target, `first_program`. Now the project has two: `first_program` and `function_tests`.
- **The name of a target doesn't have to be the name of a file.** `first_program` is built from `main.cpp` and `rules.cpp`. The file with the test program's `main` has the same name as its target here, so that they are easy to match, but CMake doesn't require it.
- **Each target has its own list of files**, and on it exactly one file with a `main` function: `first_program` has `main.cpp`, and `function_tests` has `function_tests.cpp`.
- **`rules.cpp` is on both lists.** It is one file in the project folder, with no copying. CMake compiles it separately for each program, so there will be two object files from the same source. A change in `rules.cpp` reaches both programs as soon as you rebuild them.
- **`rules.hpp` is on no list**, like every header (lesson 11.2). It is included by `main.cpp`, `function_tests.cpp` and `rules.cpp`.
- **You repeat the two property lines for `function_tests`.** The settings belong to a target, so without them the test program could be compiled under another C++ standard than the application program.
- The other lines of the lesson 0.5 file stay unchanged. In this course, all source files of a target stand on one `add_executable` line, and an empty line separates the two lists.

`function_tests.cpp` **doesn't go** on the list of `first_program`, and `main.cpp` doesn't go on the list of `function_tests`. What happens when someone mixes them up, you will see in section 8.

## 5. Build and run both programs

**This is the first required run.**

**In CLion** (according to the CLion 2026.3 documentation, without a manual check on every system):

1. After changing `CMakeLists.txt`, reload the project: click the notice about the change, or choose **Tools | CMake | Reload CMake Project**.
2. In the toolbar, in the choice of program to run, CLion shows the run configurations. After the reload there should be two: `first_program` and `function_tests`. If `function_tests` is missing, check the line `add_executable(function_tests ...)` and reload the project again.
3. Choose **Build | Build Project**. This command builds every program of the project, here both. In the **Build** window you'll find lines roughly like these:

   ```text
   Building CXX object CMakeFiles/first_program.dir/main.cpp.o
   Building CXX object CMakeFiles/first_program.dir/rules.cpp.o
   Building CXX object CMakeFiles/function_tests.dir/function_tests.cpp.o
   Building CXX object CMakeFiles/function_tests.dir/rules.cpp.o
   Linking CXX executable first_program
   Linking CXX executable function_tests
   ```

   There are four compilations, **two** of them of `rules.cpp`, one for each program, and two links. The order of the lines may differ. On Windows the object files end in `.obj`, and the programs in `.exe`.
4. Choose `first_program` and click **Run** (▶). **Predict** the result before you see it.
5. Choose `function_tests` and click **Run**. **Predict** the result of each line and the exit code.

<details>
<summary>Standard output of both programs</summary>

`first_program`, the application program:

```text
Parking hours: 2
Fee: 8
```

`function_tests`, the test program:

<!-- output: parking_project -->
```text
PASS parking_fee(0)
PASS parking_fee(1)
PASS parking_fee(2)
PASS parking_fee(3)
PASS parking_fee(8)
PASS parking_fee(9)
Checks: 6, failed: 0
```

Both programs end with exit code 0: `Process finished with exit code 0`.

</details>

**How do you know which program ran?** From the choice in the toolbar, from the name of the configuration that CLion shows in the **Run** window, and from the content: the application program prints the fee, and the test program prints `PASS` or `FAIL` lines and a summary.

**Build and Run are two different actions:**

- **Build | Build Project** builds every program of the project and runs nothing.
- **Run** runs **one** program, the one chosen in the toolbar. Before running it, CLion builds that program if something in it has changed. It doesn't have to build the other program as well.
- Other build commands, for example the one with the name of the chosen configuration in the **Build** menu, build only the chosen program.

That is why you start with **Build Project** after every change. If you only clicked **Run** with `function_tests` chosen, a mistake in `main.cpp` could go unnoticed until `first_program` is chosen.

**In the terminal** (optional): configure the project in a folder `build-terminal` as in lesson 11.1, section 5. The command `cmake --build build-terminal` builds both programs, because it names no target. Then run each of them: `./build-terminal/first_program` and `./build-terminal/function_tests` (Windows: `.\build-terminal\first_program.exe` and `.\build-terminal\function_tests.exe`). Read the exit code in CLion, as in lesson 13.1: the terminal doesn't print it.

**What is checked automatically.** The course's automatic check builds both programs from these five files, runs the test program and compares its output and exit code with the lesson. The output of the application program is shown as an example of a run in CLion: it isn't checked automatically.

## 6. A change in the shared file

**This is the second required run.**

Someone was updating the price list and made a mistake: each further hour now costs 2 instead of 3. In `rules.cpp`, change only the last line of the function:

<!-- fragment -->
```cpp
    return 5 + 2 * (hours - 1);
```

Change nothing else: not `rules.hpp`, not `main.cpp`, not `function_tests.cpp`, not `CMakeLists.txt`, and not the expected results.

1. **Predict:** which checks will give `FAIL`, with what actual result, what will the test program's exit code be, and what will the application program print?
2. Choose **Build | Build Project**.
3. Run `function_tests`, and then `first_program`.

<details>
<summary>Standard output of both programs and the exit code</summary>

`function_tests`:

<!-- output: parking_project_bug -->
```text
PASS parking_fee(0)
PASS parking_fee(1)
FAIL parking_fee(2): expected 8, actual 7
FAIL parking_fee(3): expected 11, actual 9
FAIL parking_fee(8): expected 26, actual 19
PASS parking_fee(9)
Checks: 6, failed: 3
```

CLion shows `Process finished with exit code 1`.

`first_program`:

```text
Parking hours: 2
Fee: 7
```

</details>

<details>
<summary>All files of the project with the bug</summary>

The same files as in sections 3 and 4, except the last line of `parking_fee`. You don't have to retype them: you change one line in your `rules.cpp`.

**`main.cpp`**:

<!-- example: parking_project_bug target=function_tests exit=1 -->
```cpp
#include <iostream>

#include "rules.hpp"

int main() {
    const int hours{2};

    std::cout << "Parking hours: " << hours << "\n";
    std::cout << "Fee: " << parking_fee(hours) << "\n";
}
```

**`rules.hpp`**:

<!-- file: parking_project_bug rules.hpp -->
```cpp
#pragma once

int parking_fee(int hours);
```

**`rules.cpp`**, with the bug:

<!-- file: parking_project_bug rules.cpp -->
```cpp
#include "rules.hpp"

int parking_fee(int hours) {
    if (hours < 0 || hours > 8) {
        return -1;
    }

    if (hours == 0) {
        return 0;
    }

    return 5 + 2 * (hours - 1);
}
```

**`function_tests.cpp`**:

<!-- file: parking_project_bug function_tests.cpp -->
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
    check_int("parking_fee(3)", 11, parking_fee(3), checks, failed);
    check_int("parking_fee(8)", 26, parking_fee(8), checks, failed);
    check_int("parking_fee(9)", -1, parking_fee(9), checks, failed);

    std::cout << "Checks: " << checks << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

**`CMakeLists.txt`**:

<!-- cmake: parking_project_bug -->
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

**What happened here:**

- Both programs were built: this is neither a compile error nor a link error.
- Three checks failed: for 2, 3 and 8 hours. The changed formula only counts the further hours, and for 1 hour it still gives 5 + 2 · 0 = 5. For 0 and 9 hours the function returns earlier, at the first conditions.
- Each `FAIL` line gives the expected result from the contract and the actual result of the changed function. `failed` is 3, so the test program returns 1. Exit code 1 means here that **the tests detected a bug in the function**, not that the test program failed.
- **The application program changed too:** it prints `Fee: 7` instead of `Fee: 8`. Both programs use the same `rules.cpp`, so one change reached both. With the two copies of section 1, the tests wouldn't have noticed it.

This situation has a name: a **regression**, a change in the code that accidentally breaks behaviour that worked before. The kept tests detected it right after the rebuild, before anyone paid for parking according to the wrong price list.

**Fix the function.** Restore the line `return 5 + 3 * (hours - 1);` in `rules.cpp`, choose **Build Project** and run `function_tests` again: six times `PASS` again, `Checks: 6, failed: 0` and exit code 0. The files are again as in section 3, so both programs print the same as in section 5, and `first_program` prints `Fee: 8` again.

**We don't fix the test to match a faulty function. We fix the function to meet the contract.** The expected results come from the contract, and the contract hasn't changed, so the tests don't change either. If the price list itself changed, the new expected results would have to be calculated from the new contract, not read from what the function returns.

Six times `PASS` means that the function agrees with the contract in the six checked cases. It doesn't prove that it is correct for all data (lesson 13.2).

## 7. Do the tests really check `rules.cpp`?

Two targets, `rules.cpp` on both lists, a shared header and two built programs are **necessary conditions**. By themselves they don't guarantee that every check in `function_tests.cpp` calls the function from `rules.cpp`. Each of these projects builds without errors, and its tests don't check the right function:

- `function_tests.cpp` contains a formula copied by hand, for example in the check function;
- the tests call a second function under another name, for example `parking_fee_copy`, defined in the tests' file;
- the expected results are computed by calling the same function, so the tests repeat its bug (lesson 13.1, section 9);
- the check function prints `PASS` without comparing the results.

A copy with **the same** name as the function in `rules.cpp` doesn't build: the linker reports two definitions, as in lesson 11.4. A copy under another name passes without any message.

**A practical check:** the deliberate bug in `rules.cpp` in section 6 gave `FAIL`. That is evidence that **these particular tests** call the function from `rules.cpp`. It isn't evidence for every test you write later: after adding a new check, it is worth breaking the function deliberately again and seeing that check report `FAIL` (lesson 13.2).

## 8. Find the bug: two programs built as one

**This is the third required run: one diagnostic task.**

Someone wanted the tests in the same project, but instead of a second target, added `function_tests.cpp` to the list of `first_program`. Recreate this project: in `cpp-workspace`, create a folder `parking_one_target`, copy the four `.cpp` and `.hpp` files of `lesson_13_4` into it, with the correct `rules.cpp`, and save this `CMakeLists.txt` in it:

<!-- cmake: parking_one_target -->
```cmake
cmake_minimum_required(VERSION 3.28)
project(first_program LANGUAGES CXX)

add_executable(first_program main.cpp rules.cpp function_tests.cpp)
target_compile_features(first_program PRIVATE cxx_std_20)
set_target_properties(first_program PROPERTIES CXX_EXTENSIONS OFF)
```

<details>
<summary>The other files, unchanged from section 3</summary>

**`main.cpp`**:

<!-- broken: parking_one_target stage=link error=multiple definition of .main'|duplicate symbol: main\b|duplicate symbol '_main' in: -->
```cpp
#include <iostream>

#include "rules.hpp"

int main() {
    const int hours{2};

    std::cout << "Parking hours: " << hours << "\n";
    std::cout << "Fee: " << parking_fee(hours) << "\n";
}
```

**`rules.hpp`**:

<!-- file: parking_one_target rules.hpp -->
```cpp
#pragma once

int parking_fee(int hours);
```

**`rules.cpp`**:

<!-- file: parking_one_target rules.cpp -->
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

**`function_tests.cpp`**:

<!-- file: parking_one_target function_tests.cpp -->
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
    check_int("parking_fee(3)", 11, parking_fee(3), checks, failed);
    check_int("parking_fee(8)", 26, parking_fee(8), checks, failed);
    check_int("parking_fee(9)", -1, parking_fee(9), checks, failed);

    std::cout << "Checks: " << checks << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

</details>

**Before you build**, answer in writing:

1. **Predict:** at which stage will the build fail: CMake configuration, compilation or linking?
2. Is each of the three `.cpp` files correct C++ on its own?
3. How many `main` functions will the linker get for the program `first_program`?
4. Will this be a `FAIL` in the tests?

**Then:**

5. Open the project in CLion and choose **Build | Build Project**. In the terminal, configure it as a new project in lesson 11.1, section 5.
6. Read the build output: how many files were compiled, and which function does the linker name?
7. Fix `CMakeLists.txt`: each file with a `main` in its own target, which is the file of section 4. Reload the project.
8. Choose **Build Project** and confirm that both programs were created. Run `function_tests`: six times `PASS` and exit code 0.

<details>
<summary>What happens and why: open after building the faulty project</summary>

1. **Configuration and compilation succeed.** CMake doesn't know which file contains `main`: the list is correct for it, because all the files exist and each is on it once. Each of the three `.cpp` files is correct code, so the compiler compiles all three: there are three `Building CXX object` lines.
2. **Linking fails.** The linker combines three object files into one program and gets two definitions of `main`: from `main.cpp` and from `function_tests.cpp`. The message names `main`: on Ubuntu `multiple definition of`, on macOS `duplicate symbol '_main'`, on Windows `duplicate symbol: main`, and at the end `linker command failed`. The exact text depends on the system, so look for the function's name and the words about a repeated definition.
3. **Two `main` functions can be in one project, but not in one program.** A program has one starting point. Each `main` needs its own target.
4. **This is not a `FAIL`.** The test program wasn't created at all, so nothing ran. A `FAIL` appears when the test program was built, ran and found a mismatch with the contract. Here the mistake is in the list of files, not in the tests or in the function.
5. **The fix is a separate target**, not removing one of the `main` functions. Back with the file of section 4, the project builds two programs, and `function_tests` gives the same result as in section 5.
6. **Two different ways of detecting this mistake.** On your computer it is reported by the linker, because CMake and CLion don't look into the content of the files. For projects with two targets, the course's automatic check also refuses, before building, a list that contains the `main` file of the other program. That is the checker's own check of the structure, not something CMake does.

</details>

## 9. Mission: room booking in two programs

The school's reception has a program that checks a room booking with the function `is_valid_slot` from the lesson 13.2 mission. You already have tests of this function in your program from lesson 13.2, together with a copy of it. Move the function and the tests into one project with two programs.

**The contract of `bool is_valid_slot(int start_hour, int end_hour)`**, unchanged from lesson 13.2:

- a slot is valid **if and only if**, at the same time: it starts no earlier than 8, ends no later than 20, the start is earlier than the end (`start_hour < end_hour`), and it lasts at most three hours;
- the length of a slot is `end_hour - start_hour`;
- there are no dates, minutes or calendar.

In `cpp-workspace`, create a folder `lesson_13_4_mission` with five files:

```text
lesson_13_4_mission/
├── CMakeLists.txt
├── main.cpp
├── function_tests.cpp
├── rules.cpp
└── rules.hpp
```

**Requirements:**

- `rules.hpp` declares `is_valid_slot`;
- `rules.cpp` contains the **only** definition of `is_valid_slot`;
- `main.cpp` includes `rules.hpp`, calls `is_valid_slot` for the slot 8–11 and prints `Slot 8-11: valid` or `Slot 8-11: invalid`, depending on the result. It reads no data and contains no tests;
- `function_tests.cpp` includes `rules.hpp`, checks `bool` results, prints `PASS` or `FAIL` with the expected and the actual result, counts checks and failures, prints the summary `Checks: N, failed: F` and ends with exit code 0 or 1;
- `CMakeLists.txt` describes exactly two programs, `first_program` and `function_tests`, both with `rules.cpp`, and doesn't combine two `main` functions in one program.

**The order of work:**

1. **The plan first.** For each of the five files, write in one sentence what goes into it, as in the table of section 2.
2. **The table of cases.** Prepare a table with the expected results from the contract. You can take your table from lesson 13.2. Make sure it covers the limits of the start (8 and 7), the end (20 and 21) and the length (3 and 4 hours), and a zero length.
3. Write `rules.hpp` and `rules.cpp`. You can move the function from your lesson 13.2 solution: after the move, it is only in `rules.cpp`.
4. Write `main.cpp` and `function_tests.cpp`. You know the functions `bool_text` and `check_bool` from lessons 13.2 and 13.3.
5. Write `CMakeLists.txt` with two targets.
6. **This is the fourth required run:** choose **Build Project**, run `first_program`, and then `function_tests`. The application program should print `Slot 8-11: valid`, all tests should pass, and the tests' exit code should be 0.
7. **A deliberate bug.** Change **only** `rules.cpp` so that the function refuses a slot that lasts exactly three hours, and otherwise works the same. Predict which checks will give `FAIL` and what the application program will print.
8. **This is the fifth required run:** choose **Build Project** and run both programs. Write down which checks failed, what the tests' exit code was and what the application program printed. Then restore the correct function, build the project and run the tests again: all of them should pass, with exit code 0.
9. **Explain** in two or three sentences what the `FAIL` after the deliberate bug showed, and what it didn't show.

<details>
<summary>The cases: open after preparing your own table</summary>

Eight cases from the table of lesson 13.2, with new letters: the slot 17–20 was case I there.

| Case | `start_hour` | `end_hour` | Expected result | Why |
|---|---:|---:|---|---|
| A | 8 | 9 | `true` | starts exactly at 8 |
| B | 8 | 11 | `true` | exactly three hours |
| C | 8 | 12 | `false` | four hours, too long |
| D | 7 | 10 | `false` | starts before 8 |
| E | 19 | 20 | `true` | ends exactly at 20 |
| F | 20 | 20 | `false` | zero length |
| G | 18 | 21 | `false` | ends after 20 |
| H | 17 | 20 | `true` | three hours, ending exactly at 20 |

</details>

### Success criteria

- The project has two targets, `first_program` and `function_tests`, each with its own file with a `main`.
- `rules.cpp` is on both lists, and `rules.hpp` is included by `main.cpp` and `function_tests.cpp`.
- Both programs build, and the application program prints `Slot 8-11: valid`.
- With the correct function all tests give `PASS`, and the tests' exit code is 0.
- `function_tests.cpp` has no definition of `is_valid_slot`, no copy of its conditions and no expected results computed by calling it.
- After the deliberate change in `rules.cpp`, the tests of slots that last exactly three hours give `FAIL`, the exit code is 1, and the application program prints `Slot 8-11: invalid`.
- After the function is restored, all tests give `PASS` again, with no expected result changed.
- You can show which file holds the only definition of the function, and explain why one change in it changed the result of both programs.

When the result matches, you can save the project in Git, as in lesson 1.5: the five files, without the build folder.

<details>
<summary>Hint 1: the roles of the files</summary>

Where should the declaration of the function go, where its definition, and where each of the two `main` functions? Which file has to include the header so that the compiler knows `is_valid_slot`? Compare your plan with the table of section 2: the function changes, not the roles of the files.

</details>

<details>
<summary>Hint 2: two targets</summary>

Which files should be in `add_executable(first_program ...)`, and which in `add_executable(function_tests ...)`? Each list must have exactly one file with a `main`. Which file must be on both lists, so that both programs use the same function?

</details>

<details>
<summary>Hint 3: the regression</summary>

Why do you have to rebuild the project and run the tests again after changing `rules.cpp`, and why don't you change any expected result while doing it? Where do the expected results come from, and has the contract changed?

</details>

## 10. When something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| There is no configuration `function_tests` in the toolbar | The CMake project wasn't reloaded, or the line `add_executable(function_tests ...)` has a mistake. | Check that line and choose **Tools \| CMake \| Reload CMake Project**. |
| `multiple definition of` or `duplicate symbol` with the name `main` | The file with one program's `main` is on the list of the other program (section 8). | Each file with a `main` only on the list of its own target. |
| `multiple definition of` or `duplicate symbol` with the name of the tested function | The tests' file contains a copy of the function with the same name (section 7). | Remove the copy. The function belongs only in `rules.cpp`. |
| `undefined reference`, `undefined symbol` or `referenced from` with the name of the tested function when one program is linked | That program's list lacks `rules.cpp`, or the definition has another name or other parameters than the declaration (lessons 11.1 and 11.2). | Add `rules.cpp` to both lists. Compare the definition with the header. |
| `use of undeclared identifier` with the name of the tested function | The file calls the function, but doesn't include `rules.hpp`. | Add `#include "rules.hpp"`. |
| The **Run** window shows a fee or `Slot ...` instead of `PASS` lines | The application program ran. | Choose `function_tests` in the toolbar and run it again. |
| After a change in `rules.cpp` the result didn't change | The program that ran wasn't rebuilt, or the tests check a copy of the function (section 7). | Choose **Build Project** and run the tests again. Check that the tests' file has no copy. |
| The tests give `FAIL`, and CLion shows `exit code 1` | The tests detected a mismatch with the contract. The program was built. | Compare the expected result with the contract. Fix the function or, if the expected result is wrong, the test. |

## 11. Explain

Answer in your own words, preferably in writing. Only then compare with the example answers.

1. What does a target mean in CMake?
2. Why can one project have two `main` functions?
3. Why can't they end up in one executable program?
4. Which files are shared by both targets, and how?
5. Why don't we copy the implementation of the function into the test program?
6. What happens to both programs after a change in `rules.cpp`?
7. Why do you have to rebuild the project after changing the implementation?
8. How is building a target different from running it?
9. Why doesn't exit code 1 of the test program mean a compile error?
10. What does the deliberate bug in `rules.cpp` confirm, and what doesn't it confirm?

<details>
<summary>Example answers</summary>

1. Something CMake builds, in this lesson an executable program. The name of the target is the first word in `add_executable`, followed by the list of its source files.
2. Because a project can build several programs. Each program has its own `main` function, in another file and in another target.
3. Because a program has one starting point. The linker, which combines the object files of one program, would get two definitions of `main` and report an error.
4. `rules.cpp` is on the lists of both targets and is compiled separately for each program. `rules.hpp` is on no list: it is included by `main.cpp`, `function_tests.cpp` and `rules.cpp`.
5. Because the tests would then check the copy, not the function the program uses. A change in the program wouldn't reach the tests, and a change in the tests wouldn't reach the program.
6. After the rebuild, both programs use the changed function: the application program prints another result, and the tests compare this new result with the expected results.
7. Because the programs are made from the files when they are built. Until you rebuild them, you run programs built from the old version of `rules.cpp`.
8. Building makes a program from the files, and running executes a finished program. **Build Project** builds both programs and runs nothing. **Run** runs one chosen program.
9. Because a program that didn't compile isn't created at all, so it can't run or return any code. Exit code 1 was returned by a test program that was built, performed all its checks and found a mismatch with the contract.
10. It confirms that these particular tests call the function from `rules.cpp` and detect this change. It doesn't confirm that the function is correct for all data, or that every future test will check the right function.

</details>

## Summary

- Tests of a copy of a function check the copy. For the tests to check the program's function, both programs must use one definition.
- **The program and the tests have separate `main` functions, but they use the same functions:** the declaration in a shared header, the only definition in a shared `.cpp` file.
- A **target** is something CMake builds. One `CMakeLists.txt` can describe two programs: `first_program` from `main.cpp` and `function_tests` from `function_tests.cpp`, both with `rules.cpp`.
- **Build Project** builds both programs. **Run** runs one, chosen in the toolbar.
- A change in the shared file reaches both programs after a rebuild. A **regression** is detected by the kept tests, run again without changing the expected results.
- You fix the function to meet the contract, not the test to match the function.
- Two `main` functions in one program are a link error, not a `FAIL`: the test program isn't created at all.
- Shared files don't guarantee that every check calls the right function. A deliberate bug that gives `FAIL` shows it for particular tests.

## What's next

You can now check the results of functions, choose cases, test reading without a file and keep the tests next to the program that uses the same functions. You will combine all of this in the Module 13 test: [Lesson 13.5: Workshop reservations (the Module 13 test)](lesson_05_workshop_reservations.en.md).

---

## Example solutions

Look here **after your own attempt**. Your case names and the order of the checks may differ, as long as every limit of the contract is checked and the files have the roles of section 2.

<details>
<summary>Section 9: the mission, room booking in two programs</summary>

**`rules.hpp`**:

<!-- file: slot_project rules.hpp -->
```cpp
#pragma once

bool is_valid_slot(int start_hour, int end_hour);
```

**`rules.cpp`**, the only definition, moved from the lesson 13.2 solution unchanged:

<!-- file: slot_project rules.cpp -->
```cpp
#include "rules.hpp"

bool is_valid_slot(int start_hour, int end_hour) {
    if (start_hour < 8 || end_hour > 20) {
        return false;
    }

    if (start_hour >= end_hour) {
        return false;
    }

    return end_hour - start_hour <= 3;
}
```

**`main.cpp`**, the application program:

<!-- example: slot_project target=function_tests -->
```cpp
#include <iostream>

#include "rules.hpp"

int main() {
    const int start_hour{8};
    const int end_hour{11};

    std::cout << "Slot " << start_hour << "-" << end_hour << ": ";

    if (is_valid_slot(start_hour, end_hour)) {
        std::cout << "valid\n";
    } else {
        std::cout << "invalid\n";
    }
}
```

**`function_tests.cpp`**, the test program:

<!-- file: slot_project function_tests.cpp -->
```cpp
#include <iostream>
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

int main() {
    int checks{0};
    int failed{0};

    check_bool("A 8-9", true, is_valid_slot(8, 9), checks, failed);
    check_bool("B 8-11", true, is_valid_slot(8, 11), checks, failed);
    check_bool("C 8-12", false, is_valid_slot(8, 12), checks, failed);
    check_bool("D 7-10", false, is_valid_slot(7, 10), checks, failed);
    check_bool("E 19-20", true, is_valid_slot(19, 20), checks, failed);
    check_bool("F 20-20", false, is_valid_slot(20, 20), checks, failed);
    check_bool("G 18-21", false, is_valid_slot(18, 21), checks, failed);
    check_bool("H 17-20", true, is_valid_slot(17, 20), checks, failed);

    std::cout << "Checks: " << checks << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

**`CMakeLists.txt`**:

<!-- cmake: slot_project -->
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

`first_program` prints:

```text
Slot 8-11: valid
```

`function_tests` prints:

<!-- output: slot_project -->
```text
PASS A 8-9
PASS B 8-11
PASS C 8-12
PASS D 7-10
PASS E 19-20
PASS F 20-20
PASS G 18-21
PASS H 17-20
Checks: 8, failed: 0
```

The tests' exit code: 0.

- **Sharing:** `is_valid_slot` is defined only in `rules.cpp`, and this file is on the lists of both targets. `main.cpp` and `function_tests.cpp` know the function from `rules.hpp`.
- **The tests:** the expected results are the values of the table of cases, written as `true` and `false`. None of them comes from calling `is_valid_slot`, and the tests' file has none of its conditions.
- **The application program** chooses its text by the function's result, so it doesn't repeat any condition of the contract itself.

**The deliberate bug:** `end_hour - start_hour < 3` instead of `<= 3`, only in `rules.cpp`. The test program and the expected results don't change.

`function_tests` prints:

<!-- output: slot_project_bug -->
```text
PASS A 8-9
FAIL B 8-11: expected true, actual false
PASS C 8-12
PASS D 7-10
PASS E 19-20
PASS F 20-20
PASS G 18-21
FAIL H 17-20: expected true, actual false
Checks: 8, failed: 2
```

The tests' exit code: 1. `first_program` prints:

```text
Slot 8-11: invalid
```

- **Which checks:** B and H, the two slots that last exactly three hours. For them `3 < 3` is false, so the function returns `false` instead of `true`.
- **Why the others pass:** A and E are shorter than three hours, C is too long in both versions, and D, F and G are refused by the earlier conditions, before the function checks the length.
- **The application program** shows the same bug, because the slot 8–11 lasts exactly three hours.
- **After the fix**, `rules.cpp` is again as above, so both programs print the same as in the first version, and the tests end with exit code 0.
- **What it shows:** these eight checks call the function from `rules.cpp`, and two of them detect this change. It doesn't show that the function is correct for all hours.

<details>
<summary>All files of the version with the bug</summary>

The same files as above, except the last line of `is_valid_slot`.

**`main.cpp`**:

<!-- example: slot_project_bug target=function_tests exit=1 -->
```cpp
#include <iostream>

#include "rules.hpp"

int main() {
    const int start_hour{8};
    const int end_hour{11};

    std::cout << "Slot " << start_hour << "-" << end_hour << ": ";

    if (is_valid_slot(start_hour, end_hour)) {
        std::cout << "valid\n";
    } else {
        std::cout << "invalid\n";
    }
}
```

**`rules.hpp`**:

<!-- file: slot_project_bug rules.hpp -->
```cpp
#pragma once

bool is_valid_slot(int start_hour, int end_hour);
```

**`rules.cpp`**, with the bug:

<!-- file: slot_project_bug rules.cpp -->
```cpp
#include "rules.hpp"

bool is_valid_slot(int start_hour, int end_hour) {
    if (start_hour < 8 || end_hour > 20) {
        return false;
    }

    if (start_hour >= end_hour) {
        return false;
    }

    return end_hour - start_hour < 3;
}
```

**`function_tests.cpp`**:

<!-- file: slot_project_bug function_tests.cpp -->
```cpp
#include <iostream>
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

int main() {
    int checks{0};
    int failed{0};

    check_bool("A 8-9", true, is_valid_slot(8, 9), checks, failed);
    check_bool("B 8-11", true, is_valid_slot(8, 11), checks, failed);
    check_bool("C 8-12", false, is_valid_slot(8, 12), checks, failed);
    check_bool("D 7-10", false, is_valid_slot(7, 10), checks, failed);
    check_bool("E 19-20", true, is_valid_slot(19, 20), checks, failed);
    check_bool("F 20-20", false, is_valid_slot(20, 20), checks, failed);
    check_bool("G 18-21", false, is_valid_slot(18, 21), checks, failed);
    check_bool("H 17-20", true, is_valid_slot(17, 20), checks, failed);

    std::cout << "Checks: " << checks << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

**`CMakeLists.txt`**:

<!-- cmake: slot_project_bug -->
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

**Previous lesson:** [Lesson 13.3: Testing a reading function without a file](lesson_03_testing_input_without_a_file.en.md) · **Next lesson:** [Lesson 13.5: Workshop reservations (the Module 13 test)](lesson_05_workshop_reservations.en.md) · [Course overview](../../README.en.md)

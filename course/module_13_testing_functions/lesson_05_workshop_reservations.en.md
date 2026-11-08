# Lesson 13.5: Workshop reservations (the Module 13 test)

[Polski](lesson_05_workshop_reservations.md) · **English** · [Course overview](../../README.en.md)

> **Module 13, lesson 5: the test** · about 110–135 minutes, in two sessions
> **You need:** your `cpp-workspace` folder and the original `lesson_05_first_program` project. The project of lesson 13.4 will be useful as a reminder of the two targets.
> **Pilot version.** The reference solution and the diagnostic's programs are checked automatically on Windows, Ubuntu and macOS. Nothing grades your project automatically: you check it yourself, against the checklist. The steps in CLion are the same as in lesson 13.4: they are described according to the CLion 2026.3 documentation, without a manual check on every system.

## How this test works

This lesson introduces nothing new. You check whether you can **plan and write, on your own, a test program for a function that a real program uses**: choose cases from the specification, check the result and the output parameter, detect a bug in the shared implementation, fix it and run the same tests again. It combines lessons 13.1–13.4.

**The most important condition:** your test must show a mismatch **before** the function is fixed. `PASS` lines for the fixed function alone aren't enough to pass the test: they don't show that the test can detect a bug at all.

The test has three parts and a review:

- **Part A: the plan.** The specification, the cases and the expected results, before you see the function's code.
- **Part B: the project and the testing.** A project with two targets, the test program, a run on the supplied function, detecting the bug, the fix and the tests again. This is the largest part of the work.
- **Part C: diagnostic and justification.** A test set that lets a contract violation through, and questions about your decisions. Do it after Part B.
- **Checking and review:** hints, the full list of cases, the diagnostic's project, the reference solution, explanations, answers and a self-assessment. Go there only after Parts A and B, or when you consciously give up further work on your own.

Looking at a hint or at an earlier lesson isn't a failure. What matters is to **note honestly what was done independently and what with help**. A suggested split into two sessions:

- **first:** the specification, Part A, the project in CLion, the application program, the first version of the test program and detecting the bug;
- **second:** completing the test set, the fix, the tests again, Part C, the checklist and the self-assessment.

**You may use:** CLion or the terminal, CMake and Ninja, as before; `CMakeLists.txt` from the original `lesson_05_first_program` and the pattern of two targets from lesson 13.4; the check functions of lessons 13.1–13.3; the way of creating `std::istringstream` from lesson 13.3; the rules of splitting into files from Module 11; your earlier case tables. You won't need the debugger. You know everything you need from Modules 1–13.

Treat lessons 13.1–13.4 as reminders of the rules, not as a finished program to copy. You may carry over parts of code consciously, for example the check functions of lesson 13.3 or the `CMakeLists.txt` of lesson 13.4, but prepare the plan, the cases, the expected results and the way of showing the bug on your own. If you adapt earlier code, note in the self-assessment where it comes from, what was carried over, what was changed and which decisions were made on your own.

---

## Specification: workshop reservations

A workshop organiser records two numbers for a room: its **capacity**, the number of all seats, and the number of **reserved** seats. The program reads both numbers and prints how many seats are still free. It doesn't model participants, prices, dates, hours, several rooms or accounts.

The aim of the test isn't the number of free seats itself. **You are assessed on testing a function that takes in data.** You get that function ready-made in Part B.

### The function `read_workshop`

<!-- fragment -->
```cpp
struct Workshop {
    int capacity;
    int reserved;
};

bool read_workshop(std::istream& input, Workshop& result);
```

**The contract:**

- The function tries to read two `int` numbers from the stream `input` with the operator `>>`: first `capacity`, then `reserved`. The numbers are separated by ordinary whitespace, for example a space or a line end.
- **Validity rules:** `1 <= capacity <= 30` and `0 <= reserved <= capacity`. So a room can have one seat or thirty, can have no reservation at all, and can be fully booked. The number of reservations can't exceed the capacity, and negative values aren't valid.
- **Success:** when both numbers were read and meet the rules, the function stores them in `result` and returns `true`.
- **Refusal:** when both numbers couldn't be read, or the data break the rules, the function returns `false` and **changes no field of `result`**. This guarantee is part of the contract.
- The last number doesn't need a line end after it: `"12 8"` and `"12 8\n"` are equally valid.
- The function reads two numbers, not a whole document. The contract says nothing about characters after the second number or about the stream's state after a refusal. There are no line numbers and no separate parameter describing an error.

### The application program

The `main` of the application program calls `read_workshop` for `std::cin`. For valid data it prints the capacity, the number of reservations and the number of free seats. For the input `12 8` it prints:

```text
Capacity: 12
Reserved: 8
Available: 4
```

For invalid data it prints exactly `Invalid workshop data`. In both situations it ends with exit code 0, like the programs of Modules 10–12: refusing bad data is correct behaviour for this program.

### The required structure

```text
workshop_reservations/
├── CMakeLists.txt
├── main.cpp
├── function_tests.cpp
├── rules.cpp
└── rules.hpp
```

- **`rules.hpp`:** the type `Workshop` and the declaration of `read_workshop`, with `#pragma once`.
- **`rules.cpp`:** the only definition of `read_workshop`; it includes `rules.hpp`.
- **`main.cpp`:** the `main` of the application program; it includes `rules.hpp` and contains no copy of the reading function.
- **`function_tests.cpp`:** the `main` of the test program; it includes `rules.hpp` and contains no definition of `read_workshop`. Each case has **its own** `std::istringstream`, its own record and its own expectations. Each call checks **the `bool` result, the field `capacity` and the field `reserved`**: after a refusal, the checks of the fields confirm that the record didn't change. The program prints `PASS` or `FAIL` with the expected and the actual result, the summary `Checks: N, failed: F`, and ends with exit code 0 or 1, depending on the failures.
- **`CMakeLists.txt`:** two targets, `first_program` and `function_tests`, both with `rules.cpp`, in the form of lesson 13.4: the lesson 0.5 file, an empty line and the same three lines for `function_tests`. Nothing else.
- One check of one property is one check in the summary, as in lesson 13.3: one case therefore gives three checks.
- The test program reads nothing from `std::cin` and needs no file and no working directory.

**Decide on your own:**

1. which cases you check, and why;
2. which results you expect in each of them;
3. which record each case starts from, so that a change, or the lack of one, is visible;
4. how you name the checks, so that a `FAIL` line says which case and which field failed;
5. which check functions you use;
6. how you show that your test detects the bug before you fix it;
7. how you confirm that the fix broke nothing.

You'll find reminders in lessons [13.1](lesson_01_self_checking_program.en.md) (the expected result, `PASS` and `FAIL`, the exit code), [13.2](lesson_02_test_cases_that_catch_bugs.en.md) (choosing cases), [13.3](lesson_03_testing_input_without_a_file.en.md) (`std::istringstream`, the record after a refusal) and [13.4](lesson_04_tests_next_to_the_program.en.md) (two targets, the shared `rules.cpp`).

---

# Part A: the plan

Before you see the function's code and before you write any test, prepare a plan in writing. Its most important part is the **table of cases**. A list of names alone isn't enough: each row gives the stream's text, the expected `bool` result, the expected state of the record after the call, and the reason for the choice. Two rows as a model:

| Case | Stream text | `bool` result | Record after the call, start `{9, 4}` | Why |
|---|---|---|---|---|
| A | `"12 8"` | `true` | `{12, 8}` | an ordinary valid case |
| J | `"ten 3"` | `false` | `{9, 4}`, unchanged | a failed read: text instead of a number |

Derive the other rows from the specification on your own. The set must cover at least these categories:

- an ordinary valid case;
- the lower limit of the capacity;
- a fully booked room;
- a value below the allowed range;
- a value above the allowed range;
- more reservations than seats;
- a failed read;
- an unchanged record after every refusal.

You don't need many cases. What counts is whether each of them can detect a different mistake.

**Answer ten questions in the plan:**

1. What are the valid ranges of both fields?
2. Can a room have zero seats?
3. Can it have zero reservations?
4. Can all seats be taken?
5. Which case checks the upper limit of the capacity?
6. Which case checks too many reservations?
7. What should happen when the second number is missing?
8. What should happen when there is text instead of a number?
9. What should happen to `result` after `false`?
10. How will you check that the tested function is really shared by both programs?

**Answer briefly, too:**

1. Why do you write the expected results down before running the tests, not after?
2. Why does the start record have other values than the records expected after a success?
3. Why does each case get its own stream?
4. Why is it worth checking each limit from both sides?

The plan is a required part of the test and is assessed together with the test program. Don't fix anything in the function before the plan is ready.

---

# Part B: the project and the testing

## The starter code

In `cpp-workspace`, create a folder `workshop_reservations` and copy `CMakeLists.txt` from the original `lesson_05_first_program` into it. Create the files of the required structure next to it, as in lesson 13.4. These two you get ready-made:

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

`<istream>` declares `std::istream`: the header is self-contained, as in lesson 11.3.

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

**This implementation compiles correctly, but it contains one undisclosed logic bug.** Don't look for it by reading the code: find it with your test. You write `main.cpp`, `function_tests.cpp` and both targets in `CMakeLists.txt` on your own.

## The order of work

1. **The application program.** Write `main.cpp` according to the specification of the application program.
2. **The test program.** Write `function_tests.cpp` according to your plan from Part A. **Don't change `rules.cpp`.**
3. **Two targets.** Change `CMakeLists.txt` as in lesson 13.4. CMake looks for all the files of both lists already when the project is loaded, so `function_tests.cpp` has to exist first. Reload the project and choose **Build | Build Project**.
4. **This is the first required run:** run `first_program`, type `12 8` in the **Run** window and press **Enter**. The program should print the three lines of the specification and end with exit code 0.
5. **This is the second required run:** run `function_tests`. With the supplied function, at least one check should give `FAIL`, and the test program should end with exit code 1. Write down which cases and which checks failed, with the expected and the actual results, and what the exit code was. This is the evidence that your test detects the bug.
6. If all checks gave `PASS`, your test set doesn't detect this function's bug. Go back to your plan and to the list of categories, add cases and run the tests again. Don't change `rules.cpp` yet.
7. **Find the cause.** From the `FAIL` lines and the contract, point to the condition in `rules.cpp` that works differently than the specification says. Write down whether the mistake is in the function or in the expected result, and how you know.
8. **Fix only `rules.cpp`.** Don't change the test data, the expected results, `main.cpp`, `function_tests.cpp` or `CMakeLists.txt`.
9. **This is the third required run:** choose **Build Project** and run `function_tests` again. All checks should give `PASS`, and the exit code should be 0. Rebuilding alone, without running the tests, doesn't confirm the fix.

---

# Part C: diagnostic and justification

Do this part **after Part B**.

## Diagnostic: the test passes, although the function breaks the contract

Someone else fixed the bug of Part B too, but moved one line at the same time: their `read_workshop` stores the numbers in `result` right after a successful read, and only then checks the ranges. For invalid numbers it still returns `false`.

This person checked the function with a test program of two cases: A, in which it checks the result and both fields, and H, that is `"10 11"` with the start record `{9, 4}`, in which it checks **only** the `bool` result. All checks passed, and the test program ended with exit code 0.

**Preparation:** in `cpp-workspace`, create a folder `workshop_diagnostics` and copy the five files of `workshop_reservations` into it, without the build folder. In the copy, replace `rules.cpp` and `function_tests.cpp` with the files of the section [Project for the diagnostic](#project-for-the-diagnostic) in the review. The other files stay yours. Open the new folder in CLion, as a new project.

1. **Predict:** what does this function return for case H, and what fields does the record have after the call? Why doesn't the check `accepted == false` see it?
2. List the requirements of the contract that this test program doesn't check.
3. Design the missing checks for case H: which values are expected, and where do you take them from?
4. **This is the fourth required run:** choose **Build Project** and run `function_tests` unchanged: write down the result and the exit code. Then add your checks for H, run the program again, and write down the `FAIL` lines and the exit code.
5. Explain whether the mistake is in the function or in the expected results.
6. Propose the smallest fix of the function, and make it in the copy's `rules.cpp`.
7. **This is the fifth required run:** run your strengthened test program. Then copy your `function_tests.cpp` from Part B into `workshop_diagnostics` and run it: all checks should give `PASS`, with exit code 0.
8. Explain why, after this fix, all the earlier tests have to be run again too, not only the ones for case H.

## Justification

Answer in your own words, referring to your test program:

1. Why must the expected result follow from the specification?
2. Why aren't typical cases alone enough?
3. Why is a fully booked room an important case?
4. What does `FAIL` say, and what doesn't it decide?
5. Why do you also check the fields of the record, not only the `bool` result?
6. Why is `std::istringstream` convenient in tests?
7. Why does each case have its own stream?
8. Why do both targets use `rules.cpp`?
9. Why can exit code 1 of the test program be an expected result?
10. What should happen after the detected bug is fixed?

---

## Checklist before you hand in

The test is passed when you meet **all** the items of this list. Your names, helper functions and number of cases may differ from the reference solution, as long as they meet the specification. A correct result of the application program for `12 8`, building the project alone, or `PASS` lines after the fix alone aren't enough.

- [ ] The plan of cases from Part A was made before the function was fixed, and contains the data, the `bool` result, the state of the record and a reason.
- [ ] The expected results follow from the specification, not from what the function does.
- [ ] The project has two CMake targets, `first_program` and `function_tests`, in the form of lesson 13.4.
- [ ] Both targets use the same implementation: `rules.cpp` is on both lists, and `rules.hpp` is included by `main.cpp` and `function_tests.cpp`.
- [ ] The definition of `read_workshop` is only in `rules.cpp`, with no copy in the test program.
- [ ] The test program supplies the data through `std::istringstream`.
- [ ] Each independent case has its own stream and its own record.
- [ ] The tests check the `bool` result of each call.
- [ ] The tests check both fields of `Workshop`, also after a refusal.
- [ ] The set covers the valid limits, values out of range, too many reservations and a failed read.
- [ ] The supplied function's bug was detected by a test before `rules.cpp` was fixed.
- [ ] After `FAIL`, the test program really ended with exit code 1.
- [ ] After the fix, the same tests, with the same expected results, pass with exit code 0.
- [ ] The diagnostic of Part C is done, the justification questions are answered, and the self-assessment is filled in.

When you are done, you can save the project `workshop_reservations` in Git, as in lesson 1.5: the five files, without the build folder.

## Assessment criteria

The rubric is for self-assessment or for assessment by a teacher. The course has no grading scale and no points threshold: the points show which areas are mastered and which need revision. The checklist above decides whether the test is passed, not the number of points.

| Area | Points | Full points when |
|---|---:|---|
| The plan and the reasons for the cases | 10 | the plan was made before the fix, gives the data, the `bool` result, the state of the record and a reason for every case, and the answers to the questions of Part A are correct |
| The project's organisation and two targets | 20 | the five files have the roles of the specification, `CMakeLists.txt` has two targets in the form of lesson 13.4, `rules.cpp` is on both lists, `read_workshop` is defined only in it, and the application program gives the specified result for `12 8` |
| The choice of cases and the expected results | 20 | the set covers all required categories, each case has a reason, and all expected results agree with the specification |
| Tests with `std::istringstream` and a check of the whole result | 20 | each case has its own stream and record, each call checks the result and both fields, and after a refusal the field checks confirm the unchanged record |
| Detecting the bug, the fix and the tests again | 20 | `FAIL` and exit code 1 appeared before the fix, the cause is pointed out in `rules.cpp`, the fix changes only that file, and the same tests then pass with exit code 0 |
| Diagnostic, justification and self-assessment | 10 | the weak test is explained and strengthened, the fix is checked with the full set, the answers refer to your project, and the self-assessment describes adapted code honestly |
| **Total** | **100** | |

- **Wrong expected results** take away full points for the choice of cases, even when there are many cases.
- **`FAIL` with exit code 0** doesn't give full points for detecting the bug: anyone who reads only the exit code will take the tests as passed.
- **A copy of `read_workshop` in `function_tests.cpp`** doesn't give full points for the project's organisation, even when both targets are defined.
- **Other names** of variables, checks and helper functions take away no points. The names of the targets and of the files with `main` are fixed, though: they come from the project's specification.

**What is checked automatically, and what isn't.** The course's tests check that the reference solution and the diagnostic's programs build, that the test programs give the shown results and exit codes, and that the application program prints what the specification says. **No automatic check looks at your project, your plan, your tests or your justification:** a person assesses them by reading the plan and the code and comparing your runs with the checklist.

---

# Checking and review

Go here **only after Parts A and B**, or when you consciously give up further work on your own. The solution's code follows.

## Hints

<details>
<summary>Hint 1: the plan of cases</summary>

Every number in the rules is a limit: 1 and 30 for the capacity, 0 and `capacity` for the reservations. For each of them, choose a value exactly at the limit and just beyond it. Ask yourself too: is a room in which all seats are reserved valid according to the specification? Write the result down before you run anything.

</details>

<details>
<summary>Hint 2: testing the function</summary>

The function gives three things to check: the `bool` result and the two fields of the record. Each case needs its own `std::istringstream` with its own text, and its own start record. If the start record has values that no valid read would give, every change of a field after a refusal shows up in a `FAIL` line.

</details>

<details>
<summary>Hint 3: the shared implementation and the regression</summary>

Where is the only definition of the function that both programs use? That is where the fix goes, while the test program and the expected results stay unchanged, because the contract hasn't changed. After the fix, build both programs, **Build Project**, and run the same tests again.

</details>

## The full list of control cases

<details>
<summary>Cases A–N, results from the specification</summary>

Each case starts from the record `{9, 4}`: no case with valid data gives these values, so every change of the record after a refusal is visible. The reference solution checks cases A–J. K–N are additional cases from the same specification.

| Case | Stream text | `bool` result | Record after the call | Why |
|---|---|---|---|---|
| A | `"12 8"` | `true` | `{12, 8}` | an ordinary valid case |
| B | `"1 0"` | `true` | `{1, 0}` | the lower limit of the capacity and zero reservations |
| C | `"10 10"` | `true` | `{10, 10}` | a fully booked room |
| D | `"30 30"` | `true` | `{30, 30}` | the upper limit of the capacity, fully booked |
| E | `"0 0"` | `false` | `{9, 4}`, unchanged | capacity below the range |
| F | `"31 0"` | `false` | `{9, 4}`, unchanged | capacity above the range |
| G | `"10 -1"` | `false` | `{9, 4}`, unchanged | reservations below the range |
| H | `"10 11"` | `false` | `{9, 4}`, unchanged | more reservations than seats |
| I | `"10"` | `false` | `{9, 4}`, unchanged | the second number is missing |
| J | `"ten 3"` | `false` | `{9, 4}`, unchanged | text instead of a number |
| K | `""` | `false` | `{9, 4}`, unchanged | an empty text |
| L | `"30 0"` | `true` | `{30, 0}` | the upper limit of the capacity, zero reservations |
| M | `"12 8\n"` | `true` | `{12, 8}` | a line end after the last number |
| N | `"10 10\n"` | `true` | `{10, 10}` | a fully booked room, with a line end |

</details>

## Project for the diagnostic

<details>
<summary>The files for Part C: open after Part B</summary>

**`rules.cpp`** with the moved line:

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

**`function_tests.cpp`**, the weak test program:

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
<summary>The other files of this project, as in the reference solution</summary>

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

## The reference solution

<details>
<summary>The plan and the project of the reference solution</summary>

This is one of the correct solutions, not the only acceptable form.

**The plan, in short:**

1. `capacity` from 1 to 30, `reserved` from 0 to `capacity`.
2. No: a capacity of 0 is below the range (E).
3. Yes: zero reservations are valid (B, L).
4. Yes: `reserved` may equal `capacity` (C, D).
5. D (`30 30`) and L (`30 0`) on one side, F (`31 0`) on the other.
6. H (`10 11`): one reservation too many.
7. I (`"10"`): reading the second number fails, so `false` and the record unchanged.
8. J (`"ten 3"`): reading the first number fails, so `false` and the record unchanged.
9. Nothing: all fields keep the values they had before the call.
10. The definition is only in `rules.cpp`, and this file is on the lists of both targets. A deliberate bug in `rules.cpp` changes the test results, and the same function gives the application program the specified result.

Short answers: an expected result written after the run would repeat what the function does, its mistakes too; the start record `{9, 4}` tells "the function stored the fields" from "the fields stayed as they were"; a separate stream means that no case starts from data used up by the previous one (lesson 13.3); a limit checked from one side only won't show whether it was moved by one.

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

**`function_tests.cpp`**, cases A–J:

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

`rules.hpp` and `rules.cpp` are the starter code of Part B.

**Before the fix**, with the supplied function, `function_tests` prints:

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

Exit code: 1. This is **a test that detects a bug**: the test program works correctly, and exit code 1 comes from six failed checks.

- **Which cases:** C and D, both with a fully booked room. The function returns `false`, so the record stays `{9, 4}`: the result and both fields disagree, three checks in each case.
- **The cause:** the condition `reserved >= capacity` also refuses `reserved == capacity`, which the contract allows. The mistake is in the function, because the expected results agree with the specification.
- **Why the others pass:** in A, B and the refusals E–J, both versions of the condition give the same result. The application program works correctly for `12 8` too: the bug doesn't affect typical data.

**The fix:** one change in `rules.cpp`, `reserved > capacity` instead of `reserved >= capacity`. The test program, the expected results, `main.cpp` and `CMakeLists.txt` don't change.

**After the fix**, the same tests print:

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

Exit code: 0. The prepared set no longer detects any mismatch. That doesn't prove the function correct for all data.

<details>
<summary>All files of the project after the fix</summary>

The same files as before the fix, except one condition in `rules.cpp`.

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

**`rules.cpp`**, after the fix:

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

**`function_tests.cpp`**, unchanged:

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

**The application program, checked separately.** In a project with two targets, the course's tests run only `function_tests`. That is why the results of the application program are checked separately: the same `main.cpp`, `rules.hpp` and fixed `rules.cpp`, built as one program and run with keyboard data. Here the keyboard text always ends with a line end, and the last data are one empty line.

<details>
<summary>The application program for six inputs</summary>

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

**`CMakeLists.txt`**, one program:

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

## Diagnostic: explanation and fix

<details>
<summary>Open after doing the diagnostic</summary>

**The weak test program** with the moved line prints:

<!-- output: workshop_weak -->
```text
PASS A accepted
PASS A capacity
PASS A reserved
PASS H accepted
Checks: 4, failed: 0
```

Exit code: 0, although the function breaks the contract.

1. **For H** the function reads 10 and 11, stores them in `result`, and only then refuses the data, because 11 > 10. It returns `false`, as it should, but the record already has the fields `{10, 11}` instead of `{9, 4}`. The check `accepted == false` sees only the result, not the record.
2. **The requirements not checked:** after a refusal both fields must stay unchanged. `capacity` and `reserved` have to be checked.
3. **The missing checks:** for H the start values, 9 and 4, are expected, because the contract says the record doesn't change after a refusal.
4. **The strengthened test program** is the weak program with two more checks for H. With the same function it prints:

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

   Exit code: 1. The two new checks detected the change of the record.
5. **The mistake is in the function:** the expected values 9 and 4 follow directly from the contract.
6. **The fix:** the line `result = Workshop{capacity, reserved};` goes back to the end of the function, after all the checks, just before `return true;`. The function is then the same as the fixed `rules.cpp` of the reference solution. The strengthened checks of cases A and H are exactly the checks of A and H in the reference solution, so with the fixed function they pass, like the whole set A–J.
7. **After the fix**, your full set from Part B passes with exit code 0.
8. **Why all the tests:** moving the line could have broken something that worked before. If storing the record had dropped out of the function, the valid cases A–D would give `FAIL` for the fields. The tests of H won't show that.

**Conclusion:** a test that checks only the `bool` result lets through a function that changes the record after a refusal. The full set of the reference solution, which checks both fields after every refusal, detects this bug in cases E, F, G and H, because in each of them both numbers could be read.

<details>
<summary>The strengthened test program, checked automatically</summary>

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

**`rules.cpp`**, with the moved line:

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

**Different bugs, different cases.** The set A–J of the reference solution detects each of these versions of the function with other cases:

| Bug | What the function does | Cases with `FAIL` | Checks with `FAIL` |
|---|---|---|---|
| M1, supplied in Part B | refuses a fully booked room: `reserved >= capacity` | C, D | three each: the result and both fields |
| M2, from Part C | stores the record before checking the ranges | E, F, G, H | two each: both fields, the result is right |
| M3 | doesn't check the upper limit of the capacity | F | three |
| M4 | doesn't check that there are no more reservations than seats | H | three |

With M2, cases I and J pass: the read fails before the function gets to storing the record. Bugs M3 and M4 aren't part of the required work. Check in your table which of your cases would detect them.

</details>

## Answers to the questions of Part C

<details>
<summary>Example answers, for the reference solution</summary>

1. Because the specification says what the function has to do. A result taken from what the function does would repeat its mistake, and the test would pass for a faulty function too (lesson 13.1).
2. Because in a typical case all rules are met at once, far from the limits. Bug M1 lets `12 8` and all ordinary rooms through, and is wrong only at the limit.
3. Because it is the limit of the rule `reserved <= capacity`: the only case in which `<` and `<=` give different results. Without it, nobody notices that a full room is refused.
4. `FAIL` says that the actual result differs from the expected one. It doesn't decide whether the mistake is in the function or in the expected result: that is settled by going back to the specification (lesson 13.2).
5. Because the contract covers the record too: after a success both fields have the read values, and after a refusal they stay unchanged. Bug M2 gives a correct `bool` result and a wrong record.
6. Because it gives the function a text written in the program: each case has its own data, nothing has to be typed and no file has to be prepared, and the result is the same every time.
7. Because a stream remembers what has already been read. A case that read from the previous case's stream would start from other data than the ones in the table (lesson 13.3).
8. Because the tests are to check the same function that the application program uses. A fix in `rules.cpp` then reaches both programs, while a test of a copy would check only the copy (lesson 13.4).
9. Because the test program returns 1 when it detects a mismatch. Before the function is fixed, that is exactly the result you expect: the evidence that the test detects the bug.
10. Both programs have to be built and the same tests run, without changing the expected results: all of them should give `PASS`, with exit code 0. That doesn't prove correctness for all data, only that the checked cases show no mismatch.

</details>

## Self-assessment

For each competence, mark one answer:

| Competence | On my own | With a hint | After looking at the solution | To revise |
|---|---|---|---|---|
| A plan of cases before the code | | | | |
| Expected results from the specification | | | | |
| Two targets and the shared `rules.cpp` | | | | |
| `std::istringstream` and a separate stream per case | | | | |
| Checking the `bool` result and both fields | | | | |
| An unchanged record after a refusal | | | | |
| Choosing limit and error cases | | | | |
| Detecting the bug before the fix | | | | |
| The fix and the tests again | | | | |
| The diagnostic of the weak test | | | | |

If you adapt earlier code, write below the table which program was used, what was carried over from it, what was changed, and which design decisions were made on your own: the cases, the expected results, the start record and the way of showing the bug.

If anything is marked in the "To revise" column, go back to the matching lesson:

| Topic | Lesson |
|---|---|
| the expected and the actual result, `PASS` and `FAIL`, the exit code | [13.1](lesson_01_self_checking_program.en.md) |
| typical, limit and error cases, a case that tells a bug apart | [13.2](lesson_02_test_cases_that_catch_bugs.en.md) |
| `std::istringstream`, a separate stream, the record after a refusal | [13.3](lesson_03_testing_input_without_a_file.en.md) |
| two targets, the shared `rules.cpp`, regression | [13.4](lesson_04_tests_next_to_the_program.en.md) |
| a header and a `.cpp` file, `#pragma once` | [11.2](../module_11_multifile_programs/lesson_02_own_header_file.en.md) |

---

## Module 13 summary

After five lessons you can:

- write a test program that compares the actual result with the expected one, prints `PASS` or `FAIL`, counts failures and ends with exit code 1 when something disagrees;
- set the expected results from the specification, never from what the tested function does;
- choose typical, limit and error cases so that they tell a correct function from a version with a bug;
- test a reading function without a file and without the keyboard, through `std::istringstream`, checking the result and the record;
- build a program and its tests in one project, from one definition of the function, in two CMake targets;
- show a bug with a test before fixing it, and confirm the fix with the same tests.

## What's next

This is the end of Module 13 and all of its planned lessons. The next module of the course is in preparation.

**Previous lesson:** [Lesson 13.4: Tests next to the program](lesson_04_tests_next_to_the_program.en.md) · **Next lesson:** in preparation · [Course overview](../../README.en.md)

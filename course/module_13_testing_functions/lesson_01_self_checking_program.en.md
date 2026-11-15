# Lesson 13.1: A program that checks the result itself

[Polski](lesson_01_self_checking_program.md) · **English** · [Course overview](../../README.en.md)

> **Module 13, lesson 1** · about 80–95 minutes, can be split into two sessions
> **You need:** your `cpp-workspace` folder and the original `lesson_05_first_program` project, as before. You won't need the debugger in this lesson.
> **Pilot version.** The programs in this lesson are checked automatically on Windows, Ubuntu and macOS, together with their exit codes.

## Before you start

This lesson assumes that you:

- know that `main` passes an exit code to the system, and that `0` conventionally means "everything is fine" (lesson 1.3);
- write functions with parameters and a result, including functions with several `return` statements (lessons 5.2–5.4);
- know the test printouts of lesson 5.5: a few calls of a function with chosen arguments, and a comparison of the results with what you expected;
- prepare a table of cases with expected results before you run a program (since Module 3);
- pass text with `const std::string&` (lesson 7.3), and a variable to be changed by reference, like `int& error_line` in lesson 12.3 (lesson 9.1).

## The situation

The car park next to the library charges for full hours of parking. The rules are written in a function, `parking_fee`. Someday someone will change it, for example when the prices change, and then you'll have to check that it still calculates correctly.

So far such a check has always looked the same: you run the program, look at the printed result, and compare it, in your head or on paper, with what should come out. In this lesson you'll answer the question: **can a program compare a function's result with the expected one by itself, and say clearly that something doesn't match?**

After this lesson you will:

- tell printing a function's result apart from checking it;
- work out the expected result from the specification before you run the program;
- write a test program that compares the actual result with the expected one and prints `PASS` or `FAIL`;
- count the tests and the failures, and end a test program with exit code 1 when any test failed;
- recognise a faulty test program: one that can't detect a bug, or one that detects a bug but doesn't report it through the exit code.

## 1. From checking by hand to a test

**The contract of the function `parking_fee`:**

- `int parking_fee(int hours)`, where `hours` is the number of full hours of parking;
- the allowed values of `hours`: from 0 to 8;
- 0 hours: the fee is 0;
- the first hour costs 5, and each further hour 3;
- for a number of hours outside 0–8 the function returns -1. A fee is never negative, so -1 unambiguously means "invalid data".

This program calls the function and prints its result, just like the test printouts of lesson 5.5:

<!-- example: parking_print -->
```cpp
#include <iostream>

int parking_fee(int hours) {
    if (hours < 0 || hours > 8) {
        return -1;
    }

    if (hours == 0) {
        return 0;
    }

    return 5 + 3 * (hours - 1);
}

int main() {
    std::cout << parking_fee(3) << "\n";
}
```

The program prints:

<!-- output: parking_print -->
```text
11
```

**How do you know that `11` is the right result?** The program doesn't know. The person who ran it knows: they read the contract, work out 5 + 3 + 3 = 11, and compare it with what they see. The test printouts of lesson 5.5 worked the same way. They were a good step: they checked one function at a time, on chosen arguments. But they have limits:

- **a person does the comparison**, from scratch on every run;
- among a dozen lines it's easy to miss one wrong number;
- after every change to the function, all results have to be compared again;
- to the program, `11` and `14` are just numbers to print. Nothing in it says which of them is correct.

A **test** moves that comparison into the program. The program gets the result you expect, compares it with the function's result by itself, and prints a verdict.

## 2. The expected result and the actual result

Every test needs two values:

- the **expected result**: what the function should return according to the contract. You work it out **on your own, from the contract, before you run the program**;
- the **actual result**: what the function really returned when it was called.

An argument of the function together with its expected result is a **test case**, familiar from the case tables. For `parking_fee`, the expected results follow from the contract like this:

| `hours` | Expected result | Where it comes from |
|---:|---:|---|
| -1 | -1 | outside 0–8 |
| 0 | 0 | no parking |
| 1 | 5 | the first hour |
| 2 | 8 | 5 + 3 |
| 3 | 11 | 5 + 3 + 3 |
| 8 | 26 | 5 + 7 · 3 |
| 9 | -1 | outside 0–8 |

No number in the column "Expected result" comes from running the function. If the expected result were taken from what the function returns today, the test would only check that the function returns what it returns. You'll come back to this trap in section 9.

## 3. The first check: PASS or FAIL

The simplest test is one condition:

<!-- example: parking_first_check -->
```cpp
#include <iostream>

int parking_fee(int hours) {
    if (hours < 0 || hours > 8) {
        return -1;
    }

    if (hours == 0) {
        return 0;
    }

    return 5 + 3 * (hours - 1);
}

int main() {
    if (parking_fee(3) == 11) {
        std::cout << "PASS\n";
    } else {
        std::cout << "FAIL\n";
    }
}
```

<!-- output: parking_first_check -->
```text
PASS
```

The expected result `11` is now in the code, and the program does the comparison. A person only reads the verdict:

- **`PASS`** (a *passing test*): the actual result equals the expected one. For this case the function works according to the contract;
- **`FAIL`** (a *failing test*): the results differ. The bug is in the function or in the test itself, for example in a wrongly worked-out expected result. The program doesn't know which. You find out by going back to the contract.

This first test has two weaknesses. `FAIL` doesn't say **which** case failed, or **what** result came out. And for the seven cases of the table you'd have to write the same `if` seven times. Repeated code is a signal you know from Module 5: it's time for a function.

## 4. A checking function

This function performs one test:

<!-- fragment -->
```cpp
void check_equal(const std::string& name, int expected, int actual, int& tests, int& failed) {
    ++tests;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << expected << ", actual " << actual << "\n";
        ++failed;
    }
}
```

| Parameter | What for |
|---|---|
| `const std::string& name` | the test's name, for example `parking_fee(0)`. When the test fails, you see at once which one it was |
| `int expected` | the expected result, worked out from the contract |
| `int actual` | the actual result. In the call you pass the call of the function itself here, for example `parking_fee(0)`: `parking_fee` runs first, and its result becomes the argument |
| `int& tests` | the counter of tests run, in `main`. A reference, because the function must change the variable in `main`, not its own copy (lesson 9.1) |
| `int& failed` | the counter of failures, in `main`, for the same reason. It grows **only** when the results don't match |

`check_equal` returns nothing (`void`), because its result is the printed verdict and the changed counters. The `FAIL` line gives both results: `expected` and `actual`. So you see at once what doesn't match, and you don't have to work anything out again.

## 5. Several tests and a summary

A complete test program for three cases of the table:

<!-- example: parking_tests -->
```cpp
#include <iostream>
#include <string>

int parking_fee(int hours) {
    if (hours < 0 || hours > 8) {
        return -1;
    }

    if (hours == 0) {
        return 0;
    }

    return 5 + 3 * (hours - 1);
}

void check_equal(const std::string& name, int expected, int actual, int& tests, int& failed) {
    ++tests;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << expected << ", actual " << actual << "\n";
        ++failed;
    }
}

int main() {
    int tests{0};
    int failed{0};

    check_equal("parking_fee(0)", 0, parking_fee(0), tests, failed);
    check_equal("parking_fee(1)", 5, parking_fee(1), tests, failed);
    check_equal("parking_fee(3)", 11, parking_fee(3), tests, failed);

    std::cout << "Tests: " << tests << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

**This is the first required run.** In `cpp-workspace`, create a folder `lesson_13_1`, copy `main.cpp` and `CMakeLists.txt` from the original `lesson_05_first_program` into it, and open it in CLion. Replace the contents of `main.cpp` with this program, build it and run it. Leave `CMakeLists.txt` unchanged. You type the next programs of this lesson into the same `main.cpp`.

**Predict** the result before you run the program.

<details>
<summary>Standard output</summary>

<!-- output: parking_tests -->
```text
PASS parking_fee(0)
PASS parking_fee(1)
PASS parking_fee(3)
Tests: 3, failed: 0
```

Under the output, CLion adds `Process finished with exit code 0`.

</details>

**How the tests are counted:**

- `main` starts with `tests{0}` and `failed{0}`;
- each call of `check_equal` is one test, so each one increases `tests` by 1;
- `failed` grows only when the actual result differs from the expected one;
- after all the tests, the program prints one summary: `Tests: 3, failed: 0`.

The order of the tests doesn't matter here: each one calls `parking_fee` anew and doesn't use the results of the earlier ones.

## 6. The exit code of a test program

The end of `main` is the new part:

<!-- fragment -->
```cpp
if (failed > 0) {
    return 1;
}

return 0;
```

You know from lesson 1.3 that `main` passes an exit code to the system: `0` conventionally means "everything is fine", and another number "something went wrong", where what exactly is decided by the program's author. **The test program of this lesson has this contract:**

| Situation | Exit code |
|---|---|
| all tests passed | `0` |
| at least one test failed | `1` |

**Why a code, when there's the word `FAIL`?** A person reads the word. The exit code is read by whatever started the program: CLion, a script, and also this course's automatic checking, which runs the programs of the lessons. The exit code isn't part of the standard output, so none of them has to read or understand any text. That way **the result of the tests doesn't depend on whether someone read every line carefully.**

**This changes a convention, but only for test programs.** In Modules 10–12, a program that rejected invalid data printed a message and ended with exit code 0. That was right: rejecting bad data is correct behaviour for those programs. A test program has a different job: it checks other code. A failed test means that something doesn't match the contract, and that is exactly what has to be reported. You don't change the earlier programs.

**Where to see the exit code:** in the last line of CLion's **Run** window, `Process finished with exit code …`, as in lesson 1.3. The terminal doesn't print it by itself, so in this lesson you read the code in CLion.

**Other tools.** C++ also has the `assert` macro (the header `<cassert>`), and programmers use ready-made testing libraries. They have their uses, but they aren't the topic of this lesson. Here you write the checking yourself, because you want to see the result of every test, count the failures, get the same text on every system and decide the exit code yourself.

## 7. The tests detect a bug

Someone changed `parking_fee` and made a mistake: for 0 hours the function now returns 5, as if every entry to the car park cost as much as the first hour. The test program is **the same** as in section 5. Only two lines of the function changed: the condition `hours <= 1` instead of `hours == 0`, and `return 5;` instead of `return 0;`.

<!-- example: parking_tests_bug exit=1 -->
```cpp
#include <iostream>
#include <string>

int parking_fee(int hours) {
    if (hours < 0 || hours > 8) {
        return -1;
    }

    if (hours <= 1) {
        return 5;
    }

    return 5 + 3 * (hours - 1);
}

void check_equal(const std::string& name, int expected, int actual, int& tests, int& failed) {
    ++tests;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << expected << ", actual " << actual << "\n";
        ++failed;
    }
}

int main() {
    int tests{0};
    int failed{0};

    check_equal("parking_fee(0)", 0, parking_fee(0), tests, failed);
    check_equal("parking_fee(1)", 5, parking_fee(1), tests, failed);
    check_equal("parking_fee(3)", 11, parking_fee(3), tests, failed);

    std::cout << "Tests: " << tests << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

**This is the second required run.** In `main.cpp`, change only the function `parking_fee`, as above, then build the program and run it. **Predict** every line of the result and the exit code.

<details>
<summary>Standard output and exit code</summary>

<!-- output: parking_tests_bug -->
```text
FAIL parking_fee(0): expected 0, actual 5
PASS parking_fee(1)
PASS parking_fee(3)
Tests: 3, failed: 1
```

CLion shows `Process finished with exit code 1`.

</details>

**What happened here:**

- the program built: this isn't a compile error or a link error;
- the test program ran all three tests and worked exactly as it should;
- the test `parking_fee(0)` got 5 instead of 0, so it printed `FAIL` with both values and increased `failed`;
- the tests for 1 and 3 hours still pass, because the bug doesn't affect them;
- `failed` is 1, so `main` returns 1.

This is **a test detecting a bug**. Exit code 1 doesn't mean that the test program failed. It means that **the test program found a bug in the function it checks**, which is exactly what it was written for.

Restore the correct function of section 5 and run the program again: three times `PASS` again, `Tests: 3, failed: 0` and code 0. **After every change to the function you run the same tests.** You don't have to write them again or work anything out in your head: a check prepared once repeats with one click.

## 8. Diagnostic: the test program detects a bug, but reports success

**The situation.** In another test program, someone left out the end of `main`. The function `parking_fee` has the bug of section 7.

<!-- example: parking_exit_bug -->
```cpp
#include <iostream>
#include <string>

int parking_fee(int hours) {
    if (hours < 0 || hours > 8) {
        return -1;
    }

    if (hours <= 1) {
        return 5;
    }

    return 5 + 3 * (hours - 1);
}

void check_equal(const std::string& name, int expected, int actual, int& tests, int& failed) {
    ++tests;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << expected << ", actual " << actual << "\n";
        ++failed;
    }
}

int main() {
    int tests{0};
    int failed{0};

    check_equal("parking_fee(0)", 0, parking_fee(0), tests, failed);
    check_equal("parking_fee(1)", 5, parking_fee(1), tests, failed);
    check_equal("parking_fee(3)", 11, parking_fee(3), tests, failed);

    std::cout << "Tests: " << tests << ", failed: " << failed << "\n";
}
```

**This is the third required run: one diagnostic task.** You get this program from the program of section 7: remove the check `if (failed > 0)` together with `return 0;` from the end of `main`.

1. **Predict** the printed text.
2. Run the program and check the exit code in the last line of the **Run** window.
3. Explain the contradiction between the text and the exit code.
4. Point to the mistake in `main`.
5. Suggest the smallest fix.
6. Make it, and confirm that a failed test now gives code 1.

<details>
<summary>Standard output and exit code</summary>

<!-- output: parking_exit_bug -->
```text
FAIL parking_fee(0): expected 0, actual 5
PASS parking_fee(1)
PASS parking_fee(3)
Tests: 3, failed: 1
```

CLion shows `Process finished with exit code 0`.

</details>

<details>
<summary>Explanation and fix</summary>

- **The contradiction:** a person reads `FAIL` and `failed: 1`, while whatever checks only the exit code gets 0, that is, "everything is fine". CLion, a script or the automatic checking would conclude that the tests passed.
- **The mistake:** `main` doesn't check `failed` before its end. When a program reaches the end of `main` without a `return`, that works like `return 0;` (lesson 1.3), so the code is always 0, whatever the result of the tests.
- **The smallest fix:** before the closing `}` of `main`, add:

<!-- fragment -->
```cpp
if (failed > 0) {
    return 1;
}

return 0;
```

- **After the fix** the program is exactly the program of section 7: it prints the same four lines and ends with code 1.

This was **a faulty test program**. It detected the function's bug but didn't report it. The function `parking_fee` is exactly as buggy here as in section 7. The difference is in the test program.

</details>

## 9. A test that can't fail

The second kind of faulty test program looks harmless. The function `parking_fee` again has the bug of section 7, and the test compares it... with itself:

<!-- example: parking_self_check -->
```cpp
#include <iostream>
#include <string>

int parking_fee(int hours) {
    if (hours < 0 || hours > 8) {
        return -1;
    }

    if (hours <= 1) {
        return 5;
    }

    return 5 + 3 * (hours - 1);
}

void check_equal(const std::string& name, int expected, int actual, int& tests, int& failed) {
    ++tests;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << expected << ", actual " << actual << "\n";
        ++failed;
    }
}

int main() {
    int tests{0};
    int failed{0};

    check_equal("parking_fee(0)", parking_fee(0), parking_fee(0), tests, failed);

    std::cout << "Tests: " << tests << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

Running this program is optional. **Predict** its result before you open the collapsed block.

<details>
<summary>Standard output</summary>

<!-- output: parking_self_check -->
```text
PASS parking_fee(0)
Tests: 1, failed: 0
```

Exit code: 0.

</details>

The function returns 5 for 0 hours, and the test passes anyway. The expected result doesn't come from the contract but from the same function, so both arguments are always equal. **A test like this can't fail, so it checks nothing.** This is a faulty test program too.

The same trap has a subtler form: the expected result calculated in the test with the same formula as in the function, for example `5 + 3 * (hours - 1)`. If the formula is wrong, the test repeats the same mistake and passes too. You work out the expected result from the contract, as in the table of section 2, and write it into the test as a ready number.

**Five rules of a good test:**

1. The expected result comes from the specification, not from what the checked function does.
2. Every test has a name that says what it checks.
3. A test must be able to fail: with a buggy function it should print `FAIL`.
4. A failure shows in two places: in the standard output and in the exit code.
5. After every change to the function, you run the same tests again.

## 10. Mission: the cost of printing

A copy shop calculates the cost of printing a document. Write the function and its test program.

**The contract of the function `print_cost`:**

- `int print_cost(int pages)`, where `pages` is the number of pages;
- the allowed number of pages: from 0 to 10;
- 0 pages cost 0;
- pages one to three cost 2 each;
- each further page, from the fourth on, costs 1;
- for a number of pages outside 0–10 the function returns -1.

In `cpp-workspace`, create a folder `print_cost`, copy `main.cpp` and `CMakeLists.txt` from the original `lesson_05_first_program` into it, and open it in CLion. Write the function and the test program on your own in `main.cpp`, in one file, as in section 5. Leave `CMakeLists.txt` unchanged.

**The order of work:**

1. **The expected results first.** Before you write any code, work out from the contract the expected results for at least 0, 1, 4 and 11 pages. Write them in a table with a column "Where it comes from", as in section 2. You may add your own cases, for example 3, 5, 10 or -1.
2. Write `print_cost`.
3. Write the test program: a checking function, at least four tests, for 0, 1, 4 and 11 pages, a summary and an exit code according to the contract of section 6.
4. **This is the fourth required run:** run the program with the correct function. Every test should print `PASS`, and the exit code should be 0.
5. **A deliberate bug.** Change one boundary or one number in `print_cost` so that the result for 4 pages is wrong, while the function still builds. If you have no idea, open the suggestion below. The complete program with this bug is in the section [Example solutions](#example-solutions).
6. **This is the fifth required run:** run the same test program with the buggy function. Write down which test failed, what the expected result was, what the actual one was, and what the exit code is. Then restore the correct function.

<details>
<summary>A suggested deliberate bug</summary>

Make the fourth page cost 2 instead of 1, for example by moving the boundary of the first price range one page further. The result for 4 pages is then 1 too big.

</details>

<details>
<summary>Expected results: open after preparing your own table</summary>

| Pages | Expected result | Where it comes from |
|---:|---:|---|
| -1 | -1 | outside 0–10 |
| 0 | 0 | no pages |
| 1 | 2 | one page at 2 |
| 3 | 6 | 3 · 2 |
| 4 | 7 | 3 · 2 + 1 |
| 5 | 8 | 3 · 2 + 2 · 1 |
| 10 | 13 | 3 · 2 + 7 · 1 |
| 11 | -1 | outside 0–10 |

</details>

In this mission you don't have to choose the cases by any strategy yet. The four required ones are enough. How to choose cases so that they detect important bugs is the topic of the next lesson.

### Success criteria

- The program builds as C++20, and `CMakeLists.txt` is as in lesson 0.5.
- `print_cost` returns results that match the contract.
- The expected results were worked out from the contract before the tests were written, and written into the tests as numbers, without calling `print_cost` and without copying its formula.
- There are at least four tests: for 0, 1, 4 and 11 pages, each with a name.
- Every test prints `PASS name` or `FAIL name: expected X, actual Y`, and at the end the program prints `Tests: N, failed: F`.
- With the correct function, every test passes and the exit code is 0.
- With the deliberately buggy function, the test for 4 pages prints `FAIL`, and the exit code is 1.
- You can say which test detected the bug, what the expected and actual results were, and why the program returned 1.

When the result matches, you can save the project in Git, as in lesson 1.5: `main.cpp` and `CMakeLists.txt`, without the build folder.

<details>
<summary>Hint 1: the expected results</summary>

Before you write a comparison, work out every expected result on paper, straight from the contract. How many pages cost 2 and how many cost 1 when there are 4 pages? Is 11 pages within the range? Write these numbers in the table with the column "Where it comes from". You then copy the ready numbers from the table into the tests.

</details>

<details>
<summary>Hint 2: the verdict</summary>

One test needs three things: a name, the expected result and the actual result. The actual result is a call of `print_cost` with an argument from the table. When both results are equal, the test prints `PASS` and the name. When they differ, it prints `FAIL`, the name and both values, in the format of section 4. The checking function of section 4 doesn't depend on which function you check.

</details>

<details>
<summary>Hint 3: failures and the exit code</summary>

Which variables in `main` must change while the tests run, and why does the checking function get them by reference? The exit code depends on one of them. Check it only after all the tests, so that every test runs and prints its verdict.

</details>

## 11. When something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `FAIL` in the output, but CLion shows `exit code 0` | `main` doesn't return 1 after a failure (section 8). | Before the end of `main`, check the failure counter and return 1 when it's greater than 0. |
| There's a `FAIL` line, but the summary says `failed: 0` | The failure counter is passed to the function by value, for example `int failed`. The function increases its own copy, and the variable in `main` doesn't change (lessons 5.2 and 9.1). | Change the parameter to `int& failed`. Check the same for the test counter. |
| Every test passes, although the function was broken on purpose | The expected result comes from a call of the checked function or from its formula (section 9), or no test concerns the changed place. | Check where every expected result comes from, and whether some test uses an argument for which the function changed. |
| `FAIL` for a function that seems correct | The mistake may be in the test itself, for example in a wrongly worked-out expected result. | Work out that result from the contract again. Fix whichever side doesn't match the contract. |
| The terminal doesn't show the exit code | The terminal doesn't print it. The exit code isn't part of the standard output. | In this lesson, read the code in the last line of CLion's **Run** window. |

## 12. Explain

Answer in your own words, preferably in writing. Only then compare with the example answers.

1. How is a test different from an ordinary `std::cout` that prints a function's result?
2. Where does the expected result come from?
3. Why must the expected result never be obtained by calling the checked function again?
4. What does `PASS` mean?
5. What does `FAIL` mean?
6. Why does a test program count the failures?
7. What does exit code 0 of a test program mean?
8. What does exit code 1 mean in our test program?
9. Why isn't it enough to print `FAIL` and end the program with code 0?
10. Why must you run all the tests again after fixing a function, not just the one that failed before?

<details>
<summary>Example answers</summary>

1. `std::cout` only prints the result, and whether it's right is decided by the person who reads it. A test contains the expected result, compares it with the actual result by itself, and prints a verdict.
2. From the specification, that is, from the function's contract. It's worked out before the program runs and written into the test as a ready number.
3. Because then the test compares the function with itself. Both results are always equal, so the test passes even for a buggy function and checks nothing.
4. The actual result equals the expected one: for this case the function works according to the contract. It doesn't mean that the function is correct for all data.
5. The actual result differs from the expected one. The bug is in the function or in the test itself, for example in a wrongly worked-out expected result. The program doesn't decide which: you have to go back to the contract.
6. So that after all the tests it knows whether any of them failed, and can choose the exit code from that. The counter also gives a summary that shows the number of failures at a glance.
7. Every test that ran passed.
8. At least one test failed. That doesn't mean that the test program failed: it detected a mismatch with the specification.
9. Because only a person reads `FAIL`. CLion, a script or the automatic checking read the exit code, and with 0 they conclude that everything is fine. The bug would then go unnoticed.
10. Because the fix may have broken something that worked before, for example another case of the same function. The tests are already written, so running them again costs nothing.

</details>

## Summary

- Printing a function's result isn't a test: then a person decides whether the result is right.
- A test compares the **actual result** with the **expected result**. The expected result comes from the specification, never from what the checked function does.
- `PASS`: the results are equal. `FAIL`: they differ, and the line gives the test's name and both values.
- A checking function performs one test and changes, by reference, the counters of tests and failures in `main`.
- A test program ends with code 0 when every test passed, and with code 1 when at least one failed. The exit code is read by whatever runs the program, without reading any text.
- Code 1 of a test program is a detected mismatch with the contract, not a fault in how the test program runs.
- A faulty test program can't detect a bug (it compares the function with itself) or doesn't report it (it ends with code 0 despite a `FAIL`).
- After every change to the function, you run the same tests again.

## What's next

The three tests of section 5 detected the bug for 0 hours. Would they detect a function that returns 29 for 9 hours, or one that is wrong only for 8 hours? In [lesson 13.2: Test cases that catch bugs](lesson_02_test_cases_that_catch_bugs.en.md) you'll check whether the chosen cases can detect important bugs, and learn how to choose them.

---

## Example solutions

Look here **after your own attempt**. Your names may differ, as long as every test has a name, and the standard output and the exit code match the requirements.

<details>
<summary>Section 10: the mission, the cost of printing</summary>

**`main.cpp`**, with tests of every case in the table of expected results:

<!-- example: print_cost_tests -->
```cpp
#include <iostream>
#include <string>

int print_cost(int pages) {
    if (pages < 0 || pages > 10) {
        return -1;
    }

    if (pages <= 3) {
        return 2 * pages;
    }

    return 6 + (pages - 3);
}

void check_equal(const std::string& name, int expected, int actual, int& tests, int& failed) {
    ++tests;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << expected << ", actual " << actual << "\n";
        ++failed;
    }
}

int main() {
    int tests{0};
    int failed{0};

    check_equal("print_cost(-1)", -1, print_cost(-1), tests, failed);
    check_equal("print_cost(0)", 0, print_cost(0), tests, failed);
    check_equal("print_cost(1)", 2, print_cost(1), tests, failed);
    check_equal("print_cost(3)", 6, print_cost(3), tests, failed);
    check_equal("print_cost(4)", 7, print_cost(4), tests, failed);
    check_equal("print_cost(5)", 8, print_cost(5), tests, failed);
    check_equal("print_cost(10)", 13, print_cost(10), tests, failed);
    check_equal("print_cost(11)", -1, print_cost(11), tests, failed);

    std::cout << "Tests: " << tests << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

<!-- output: print_cost_tests -->
```text
PASS print_cost(-1)
PASS print_cost(0)
PASS print_cost(1)
PASS print_cost(3)
PASS print_cost(4)
PASS print_cost(5)
PASS print_cost(10)
PASS print_cost(11)
Tests: 8, failed: 0
```

Exit code: 0.

- **The function:** first the range, then the pages at 2 (up to and including the third), and finally 6 for the first three pages plus 1 for each further page. 0 pages give `2 * 0`, that is 0, so they need no separate condition.
- **The tests:** the expected results are the numbers of the table, worked out from the contract. None of them came from calling `print_cost`.
- **Other correct solutions:** a different order of the conditions; a separate condition for 0 pages; the formula `pages + 3` instead of `6 + (pages - 3)` for pages from the fourth on. Your program may have only the four required tests: then the output has four `PASS` lines and `Tests: 4, failed: 0`.

**The deliberate bug:** the boundary of the first range moved by one page, `pages <= 4` instead of `pages <= 3`. The fourth page then costs 2 instead of 1. The test program doesn't change:

<!-- example: print_cost_tests_bug exit=1 -->
```cpp
#include <iostream>
#include <string>

int print_cost(int pages) {
    if (pages < 0 || pages > 10) {
        return -1;
    }

    if (pages <= 4) {
        return 2 * pages;
    }

    return 6 + (pages - 3);
}

void check_equal(const std::string& name, int expected, int actual, int& tests, int& failed) {
    ++tests;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << expected << ", actual " << actual << "\n";
        ++failed;
    }
}

int main() {
    int tests{0};
    int failed{0};

    check_equal("print_cost(-1)", -1, print_cost(-1), tests, failed);
    check_equal("print_cost(0)", 0, print_cost(0), tests, failed);
    check_equal("print_cost(1)", 2, print_cost(1), tests, failed);
    check_equal("print_cost(3)", 6, print_cost(3), tests, failed);
    check_equal("print_cost(4)", 7, print_cost(4), tests, failed);
    check_equal("print_cost(5)", 8, print_cost(5), tests, failed);
    check_equal("print_cost(10)", 13, print_cost(10), tests, failed);
    check_equal("print_cost(11)", -1, print_cost(11), tests, failed);

    std::cout << "Tests: " << tests << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

<!-- output: print_cost_tests_bug -->
```text
PASS print_cost(-1)
PASS print_cost(0)
PASS print_cost(1)
PASS print_cost(3)
FAIL print_cost(4): expected 7, actual 8
PASS print_cost(5)
PASS print_cost(10)
PASS print_cost(11)
Tests: 8, failed: 1
```

Exit code: 1. This is **a test detecting a bug**: the test program works correctly, and the bug is in `print_cost`.

- **Which test, and why:** only `print_cost(4)`. For 4 pages the buggy function calculates `2 * 4`, that is 8, while the contract gives 3 · 2 + 1 = 7.
- **Why the others pass:** for 0–3 pages both versions take the same branch. For 5 and 10 pages the condition `pages <= 4` is false, so the same formula runs as in the correct function.
- **Code 1:** `failed` is 1, so `main` returns 1.
- **A lesson for later:** only the test for 4 pages detects this bug, that is, exactly at the boundary between the two prices. Without that test, all the others would pass. You'll see how to foresee such places in the next lesson.

</details>

**Previous lesson:** [Lesson 12.4: Cinema screenings (the Module 12 test)](../module_12_text_files/lesson_04_cinema_screenings.en.md) · **Next lesson:** [Lesson 13.2: Test cases that catch bugs](lesson_02_test_cases_that_catch_bugs.en.md) · [Course overview](../../README.en.md)

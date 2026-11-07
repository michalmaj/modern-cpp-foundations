# Lesson 13.2: Test cases that catch bugs

[Polski](lesson_02_test_cases_that_catch_bugs.md) · **English** · [Course overview](../../README.en.md)

> **Module 13, lesson 2** · about 90–110 minutes, can be split into two sessions
> **You need:** your `cpp-workspace` folder and the original `lesson_05_first_program` project, as before. Your test program from the mission of lesson 13.1 will be useful too.
> **Pilot version.** The programs in this lesson are checked automatically on Windows, Ubuntu and macOS, together with their exit codes.

## Before you start

This lesson assumes that you:

- write the test program of lesson 13.1: the expected result from the contract, `PASS` or `FAIL`, counters of tests and failures, exit code 0 or 1;
- know that `std::cout` prints a `bool` value as `1` or `0` (lesson 3.2);
- combine conditions with the operators `&&`, `||` and `!` (lesson 3.4);
- define a `struct`, create a record in braces and pass it to a function by `const&` (lessons 8.1 and 8.3);
- check a range boundary from both sides (since Module 3).

## The situation

A library decides whether a reader may borrow another book. The decision is made by a function that returns only "yes" or "no". Someone wrote it, someone else prepared three tests, and they all pass. Does that mean the function is good?

Lesson 13.1 showed **how to check one result**. This lesson shows **which results are worth checking**.

After this lesson you will:

- tell apart four different things: a working test program, correct expected results, well-chosen cases and a correct function;
- choose typical cases, boundary cases and cases of invalid input from the contract;
- check every condition with a case of its own;
- judge a test suite by whether it tells the correct function apart from a version with a bug;
- recognise that the mistake is in the test itself, not in the function.

## 1. Three times PASS: so what?

In the mission of lesson 13.1, the bug in `print_cost` was detected only by the test for 4 pages. Without that test, all the others would have passed, and the test program would have ended with code 0. **A green result of every test that ran doesn't prove that the function is correct.** It only says that the chosen cases didn't reveal a mismatch.

These four properties aren't the same:

| Property | The question that checks it |
|---|---|
| the test program works correctly | does every mismatch give `FAIL` and exit code 1? (lesson 13.1) |
| the expected results are correct | does every value in the test follow from the contract? |
| the cases are well chosen | would some test give `FAIL` for a version of the function with a bug? |
| the function is correct | does it return what the contract says, for all allowed data? |

A test program can work flawlessly and still check too little. This lesson is about the third property: the choice of cases.

## 2. The contract: may the reader borrow another book

A loan request is a record with three fields:

<!-- fragment -->
```cpp
struct LoanRequest {
    int borrowed_books;
    int days_overdue;
    bool blocked;
};
```

**The contract of the function `bool can_borrow(const LoanRequest& request)`:**

- `borrowed_books`: the number of books currently borrowed, allowed from 0 to 5;
- `days_overdue`: the number of days a return is overdue, allowed from 0 to 30;
- `blocked`: whether the account is blocked, `true` or `false`;
- another loan is possible **if and only if** all of these hold at once: `borrowed_books < 5`, `days_overdue == 0`, and the account isn't blocked;
- for values outside the allowed ranges, the function returns `false`.

The function returns only a `bool`. It doesn't say **why** it refused.

The correct function first rejects data that aren't allowed, and then checks the three conditions at once:

<!-- fragment -->
```cpp
bool can_borrow(const LoanRequest& request) {
    if (request.borrowed_books < 0 || request.borrowed_books > 5) {
        return false;
    }

    if (request.days_overdue < 0 || request.days_overdue > 30) {
        return false;
    }

    return request.borrowed_books < 5 && request.days_overdue == 0 && !request.blocked;
}
```

## 3. Checking a `bool` result

The checking function of lesson 13.1 compared numbers. Here the result is a `bool`, so you need a variant of it with two changes:

<!-- fragment -->
```cpp
std::string bool_text(bool value) {
    if (value) {
        return "true";
    }

    return "false";
}

void check_bool(const std::string& name, bool expected, bool actual, int& tests, int& failed) {
    ++tests;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << bool_text(expected) << ", actual " << bool_text(actual) << "\n";
        ++failed;
    }
}
```

- **The parameter types:** `expected` and `actual` are `bool`. The rest works like `check_equal`: the same test counter, the same failure counter, the same format.
- **`bool_text`:** `std::cout` would print a `bool` as `1` or `0`. The line `FAIL D {5, 0, false}: expected false, actual true` reads more easily than `expected 0, actual 1`, and the words `true` and `false` are exactly the ones you write in the code.
- **The test's name** is the case's letter and the record's data in the order of the fields: `{books, days overdue, blocked}`. A `FAIL` line shows at once for which data the function was wrong.

## 4. A weak suite: A, B and J

The first test suite looks sensible: "yes" twice, and a clear "no" once.

| Case | `borrowed_books` | `days_overdue` | `blocked` | Expected result | Where it comes from |
|---|---:|---:|---|---|---|
| A | 0 | 0 | `false` | `true` | every condition holds |
| B | 2 | 0 | `false` | `true` | every condition holds |
| J | 5 | 2 | `true` | `false` | the limit reached, overdue and blocked |

This program checks, with this suite, **a version of the function that has one bug**. The code of the test program is correct.

<!-- example: loan_weak_tests_bug -->
```cpp
#include <iostream>
#include <string>

struct LoanRequest {
    int borrowed_books;
    int days_overdue;
    bool blocked;
};

bool can_borrow(const LoanRequest& request) {
    if (request.borrowed_books < 0 || request.borrowed_books > 5) {
        return false;
    }

    if (request.days_overdue < 0 || request.days_overdue > 30) {
        return false;
    }

    return request.borrowed_books < 5 && request.days_overdue == 0;
}

std::string bool_text(bool value) {
    if (value) {
        return "true";
    }

    return "false";
}

void check_bool(const std::string& name, bool expected, bool actual, int& tests, int& failed) {
    ++tests;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << bool_text(expected) << ", actual " << bool_text(actual) << "\n";
        ++failed;
    }
}

int main() {
    int tests{0};
    int failed{0};

    check_bool("A {0, 0, false}", true, can_borrow(LoanRequest{0, 0, false}), tests, failed);
    check_bool("B {2, 0, false}", true, can_borrow(LoanRequest{2, 0, false}), tests, failed);
    check_bool("J {5, 2, true}", false, can_borrow(LoanRequest{5, 2, true}), tests, failed);

    std::cout << "Tests: " << tests << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

**This is the first required run.** In `cpp-workspace`, create a folder `lesson_13_2`, copy `main.cpp` and `CMakeLists.txt` from the original `lesson_05_first_program` into it, and open it in CLion. Replace the contents of `main.cpp` with this program, build it and run it. You type the next programs of this lesson into the same `main.cpp`. **Predict** the result and the exit code.

<details>
<summary>Standard output and exit code</summary>

<!-- output: loan_weak_tests_bug -->
```text
PASS A {0, 0, false}
PASS B {2, 0, false}
PASS J {5, 2, true}
Tests: 3, failed: 0
```

CLion shows `Process finished with exit code 0`.

</details>

**Every test passed, and the function has a bug.** Compare the last line of `can_borrow` with the correct function of section 2: `&& !request.blocked` is missing. This version **doesn't check the block at all**: a blocked reader with nothing overdue would get a book.

- **Code 0 means that the suite that ran succeeded, not that the function is proven correct.** The program told the truth: none of the three tests detected a mismatch.
- **This isn't a faulty test program** in the sense of lesson 13.1. There the program printed `FAIL` but ended with code 0. Here the mechanism works correctly: if a test failed, there would be `FAIL` and code 1. What let you down is **the choice of cases**.
- **Why J doesn't help:** J breaks three conditions at once. The limit of five books already rejects it, so the result is `false` even when the function doesn't look at the block at all. A "very wrong" case only checks that the function rejects **some** of the reasons, not that it checks **each** of them.

## 5. A case that tells the two versions apart

You need a case for which **the correct function and this version with a bug return different results**. Before you open the collapsed block, suggest such a case: three field values and the expected result from the contract.

<details>
<summary>One of the good cases</summary>

**F {2, 0, true}:** two books, nothing overdue, the account blocked. According to the contract, the result is `false`. The version with the bug doesn't look at the block and returns `true`. The results differ, so the test for F detects this bug.

Any case in which **the block is the only reason for refusing** works the same way, for example `{0, 0, true}`.

</details>

The rule from this example: **to check one condition, break only that condition, and leave all the others satisfied.** Then the result depends on it alone. A test that gives `FAIL` for a version with a bug is a **bug-revealing test**.

## 6. Typical cases, boundary cases and invalid input

A stronger suite comes from the contract, point by point. Every case has a reason you can point to in the contract:

| Case | `borrowed_books` | `days_overdue` | `blocked` | Expected result | Kind and reason |
|---|---:|---:|---|---|---|
| A | 0 | 0 | `false` | `true` | typical; the smallest number of books |
| B | 2 | 0 | `false` | `true` | typical |
| C | 4 | 0 | `false` | `true` | boundary: the last number of books that still allows a loan |
| D | 5 | 0 | `false` | `false` | boundary: the limit reached, the only reason for refusing |
| E | 2 | 1 | `false` | `false` | boundary: the smallest overdue, the only reason for refusing |
| F | 2 | 0 | `true` | `false` | the block as the only reason for refusing |
| G | -1 | 0 | `false` | `false` | invalid input: a negative number of books |
| H | 6 | 0 | `false` | `false` | invalid input: a number of books above the range |
| I | 2 | -1 | `false` | `false` | invalid input: a negative overdue |
| J | 5 | 2 | `true` | `false` | several reasons for refusing at once |
| K | 2 | 30 | `false` | `false` | the largest allowed overdue |
| L | 2 | 31 | `false` | `false` | invalid input: an overdue above the range |

- A **typical case**: ordinary data, for which the answer is obvious. Needed, but on its own it checks little.
- A **boundary case**: data exactly at a boundary from the contract, on both of its sides. C and D check the boundary between 4 and 5 books, and B and E the boundary between nothing overdue and one day. This is where `<` and `<=`, or `==` and `<=`, are easiest to confuse.
- A case of **invalid input**: values outside the allowed range. The contract says what to do then, so these are cases with an unambiguous expected result too.
- A **test suite** is all the cases checked together by one test program.

**K and L** show the boundary of the allowed data: 30 days are still valid data, 31 aren't. Both give `false`, though, each for a different reason: K because of the overdue, L because of invalid input. The function returns only a `bool`, so a test sees the result, not the reason. This boundary doesn't change the result of this function. **A boundary case is most valuable where the result should differ on the two sides of the boundary**, as with C and D.

## 7. A stronger test suite

The same test program, with all twelve cases, checks the same version of the function with the bug:

<!-- example: loan_strong_tests_bug exit=1 -->
```cpp
#include <iostream>
#include <string>

struct LoanRequest {
    int borrowed_books;
    int days_overdue;
    bool blocked;
};

bool can_borrow(const LoanRequest& request) {
    if (request.borrowed_books < 0 || request.borrowed_books > 5) {
        return false;
    }

    if (request.days_overdue < 0 || request.days_overdue > 30) {
        return false;
    }

    return request.borrowed_books < 5 && request.days_overdue == 0;
}

std::string bool_text(bool value) {
    if (value) {
        return "true";
    }

    return "false";
}

void check_bool(const std::string& name, bool expected, bool actual, int& tests, int& failed) {
    ++tests;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << bool_text(expected) << ", actual " << bool_text(actual) << "\n";
        ++failed;
    }
}

int main() {
    int tests{0};
    int failed{0};

    check_bool("A {0, 0, false}", true, can_borrow(LoanRequest{0, 0, false}), tests, failed);
    check_bool("B {2, 0, false}", true, can_borrow(LoanRequest{2, 0, false}), tests, failed);
    check_bool("C {4, 0, false}", true, can_borrow(LoanRequest{4, 0, false}), tests, failed);
    check_bool("D {5, 0, false}", false, can_borrow(LoanRequest{5, 0, false}), tests, failed);
    check_bool("E {2, 1, false}", false, can_borrow(LoanRequest{2, 1, false}), tests, failed);
    check_bool("F {2, 0, true}", false, can_borrow(LoanRequest{2, 0, true}), tests, failed);
    check_bool("G {-1, 0, false}", false, can_borrow(LoanRequest{-1, 0, false}), tests, failed);
    check_bool("H {6, 0, false}", false, can_borrow(LoanRequest{6, 0, false}), tests, failed);
    check_bool("I {2, -1, false}", false, can_borrow(LoanRequest{2, -1, false}), tests, failed);
    check_bool("J {5, 2, true}", false, can_borrow(LoanRequest{5, 2, true}), tests, failed);
    check_bool("K {2, 30, false}", false, can_borrow(LoanRequest{2, 30, false}), tests, failed);
    check_bool("L {2, 31, false}", false, can_borrow(LoanRequest{2, 31, false}), tests, failed);

    std::cout << "Tests: " << tests << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

**This is the second required run.** In `main.cpp`, replace `main` with the one with twelve tests, and leave the function with its bug. Run the program. **Predict** which tests will fail. Then restore the condition `&& !request.blocked` in `can_borrow` and run the program again.

<details>
<summary>Standard output and exit code for the version with the bug</summary>

<!-- output: loan_strong_tests_bug -->
```text
PASS A {0, 0, false}
PASS B {2, 0, false}
PASS C {4, 0, false}
PASS D {5, 0, false}
PASS E {2, 1, false}
FAIL F {2, 0, true}: expected false, actual true
PASS G {-1, 0, false}
PASS H {6, 0, false}
PASS I {2, -1, false}
PASS J {5, 2, true}
PASS K {2, 30, false}
PASS L {2, 31, false}
Tests: 12, failed: 1
```

CLion shows `Process finished with exit code 1`.

</details>

The same bug, a different suite, a different verdict. **One** case detected the bug: F, the only one in which the block alone decides the refusal. J, which also has the block, still passes.

<details>
<summary>The program and its result after restoring the correct function</summary>

<!-- example: loan_strong_tests -->
```cpp
#include <iostream>
#include <string>

struct LoanRequest {
    int borrowed_books;
    int days_overdue;
    bool blocked;
};

bool can_borrow(const LoanRequest& request) {
    if (request.borrowed_books < 0 || request.borrowed_books > 5) {
        return false;
    }

    if (request.days_overdue < 0 || request.days_overdue > 30) {
        return false;
    }

    return request.borrowed_books < 5 && request.days_overdue == 0 && !request.blocked;
}

std::string bool_text(bool value) {
    if (value) {
        return "true";
    }

    return "false";
}

void check_bool(const std::string& name, bool expected, bool actual, int& tests, int& failed) {
    ++tests;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << bool_text(expected) << ", actual " << bool_text(actual) << "\n";
        ++failed;
    }
}

int main() {
    int tests{0};
    int failed{0};

    check_bool("A {0, 0, false}", true, can_borrow(LoanRequest{0, 0, false}), tests, failed);
    check_bool("B {2, 0, false}", true, can_borrow(LoanRequest{2, 0, false}), tests, failed);
    check_bool("C {4, 0, false}", true, can_borrow(LoanRequest{4, 0, false}), tests, failed);
    check_bool("D {5, 0, false}", false, can_borrow(LoanRequest{5, 0, false}), tests, failed);
    check_bool("E {2, 1, false}", false, can_borrow(LoanRequest{2, 1, false}), tests, failed);
    check_bool("F {2, 0, true}", false, can_borrow(LoanRequest{2, 0, true}), tests, failed);
    check_bool("G {-1, 0, false}", false, can_borrow(LoanRequest{-1, 0, false}), tests, failed);
    check_bool("H {6, 0, false}", false, can_borrow(LoanRequest{6, 0, false}), tests, failed);
    check_bool("I {2, -1, false}", false, can_borrow(LoanRequest{2, -1, false}), tests, failed);
    check_bool("J {5, 2, true}", false, can_borrow(LoanRequest{5, 2, true}), tests, failed);
    check_bool("K {2, 30, false}", false, can_borrow(LoanRequest{2, 30, false}), tests, failed);
    check_bool("L {2, 31, false}", false, can_borrow(LoanRequest{2, 31, false}), tests, failed);

    std::cout << "Tests: " << tests << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

<!-- output: loan_strong_tests -->
```text
PASS A {0, 0, false}
PASS B {2, 0, false}
PASS C {4, 0, false}
PASS D {5, 0, false}
PASS E {2, 1, false}
PASS F {2, 0, true}
PASS G {-1, 0, false}
PASS H {6, 0, false}
PASS I {2, -1, false}
PASS J {5, 2, true}
PASS K {2, 30, false}
PASS L {2, 31, false}
Tests: 12, failed: 0
```

Exit code: 0.

</details>

**How to say it honestly.** After the fix, every test passes. That doesn't mean "the function is proven correct". It means: **the prepared test suite didn't detect a mismatch in the checked version of the function.** The better the cases are chosen, the more that sentence is worth.

**More tests aren't always better tests.** If you added `{1, 0, false}` and `{3, 0, false}`, the suite would be longer but not stronger: both cases check the same as B, with every condition satisfied. A **stronger test suite** is one that **tells more versions with a bug apart** from the correct function, not one with more lines. The suite of section 4 was a **weak test suite**: it didn't tell the correct function apart from a function that doesn't check the block.

## 8. Other bugs, and the cases that detect them

Here are three more versions of `can_borrow`. Each differs from the correct function in **one** place, builds without errors, and gives the correct results for cases A and B:

| Version | The change in the function | The effect, by the contract |
|---|---|---|
| a wrong limit boundary | `borrowed_books <= 5` instead of `borrowed_books < 5` in the last line | a reader with five books gets a sixth |
| a wrong overdue boundary | `days_overdue <= 1` instead of `days_overdue == 0` in the last line | one day overdue doesn't matter |
| no check of a negative number | the first condition is only `request.borrowed_books > 5` | a negative number of books passes as valid |

**For each version, choose from the table A–L a case that detects it**, and predict its `FAIL` line. Think also about why the weak suite A, B and J passes for each of them. Only then open the review.

<details>
<summary>Review: three versions and their results</summary>

**A wrong limit boundary.** D detects it: five books, nothing overdue, not blocked.

<!-- example: loan_strong_tests_limit_bug exit=1 -->
```cpp
#include <iostream>
#include <string>

struct LoanRequest {
    int borrowed_books;
    int days_overdue;
    bool blocked;
};

bool can_borrow(const LoanRequest& request) {
    if (request.borrowed_books < 0 || request.borrowed_books > 5) {
        return false;
    }

    if (request.days_overdue < 0 || request.days_overdue > 30) {
        return false;
    }

    return request.borrowed_books <= 5 && request.days_overdue == 0 && !request.blocked;
}

std::string bool_text(bool value) {
    if (value) {
        return "true";
    }

    return "false";
}

void check_bool(const std::string& name, bool expected, bool actual, int& tests, int& failed) {
    ++tests;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << bool_text(expected) << ", actual " << bool_text(actual) << "\n";
        ++failed;
    }
}

int main() {
    int tests{0};
    int failed{0};

    check_bool("A {0, 0, false}", true, can_borrow(LoanRequest{0, 0, false}), tests, failed);
    check_bool("B {2, 0, false}", true, can_borrow(LoanRequest{2, 0, false}), tests, failed);
    check_bool("C {4, 0, false}", true, can_borrow(LoanRequest{4, 0, false}), tests, failed);
    check_bool("D {5, 0, false}", false, can_borrow(LoanRequest{5, 0, false}), tests, failed);
    check_bool("E {2, 1, false}", false, can_borrow(LoanRequest{2, 1, false}), tests, failed);
    check_bool("F {2, 0, true}", false, can_borrow(LoanRequest{2, 0, true}), tests, failed);
    check_bool("G {-1, 0, false}", false, can_borrow(LoanRequest{-1, 0, false}), tests, failed);
    check_bool("H {6, 0, false}", false, can_borrow(LoanRequest{6, 0, false}), tests, failed);
    check_bool("I {2, -1, false}", false, can_borrow(LoanRequest{2, -1, false}), tests, failed);
    check_bool("J {5, 2, true}", false, can_borrow(LoanRequest{5, 2, true}), tests, failed);
    check_bool("K {2, 30, false}", false, can_borrow(LoanRequest{2, 30, false}), tests, failed);
    check_bool("L {2, 31, false}", false, can_borrow(LoanRequest{2, 31, false}), tests, failed);

    std::cout << "Tests: " << tests << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

<!-- output: loan_strong_tests_limit_bug -->
```text
PASS A {0, 0, false}
PASS B {2, 0, false}
PASS C {4, 0, false}
FAIL D {5, 0, false}: expected false, actual true
PASS E {2, 1, false}
PASS F {2, 0, true}
PASS G {-1, 0, false}
PASS H {6, 0, false}
PASS I {2, -1, false}
PASS J {5, 2, true}
PASS K {2, 30, false}
PASS L {2, 31, false}
Tests: 12, failed: 1
```

Exit code: 1.

**A wrong overdue boundary.** E detects it: two books, one day overdue, not blocked.

<!-- example: loan_strong_tests_overdue_bug exit=1 -->
```cpp
#include <iostream>
#include <string>

struct LoanRequest {
    int borrowed_books;
    int days_overdue;
    bool blocked;
};

bool can_borrow(const LoanRequest& request) {
    if (request.borrowed_books < 0 || request.borrowed_books > 5) {
        return false;
    }

    if (request.days_overdue < 0 || request.days_overdue > 30) {
        return false;
    }

    return request.borrowed_books < 5 && request.days_overdue <= 1 && !request.blocked;
}

std::string bool_text(bool value) {
    if (value) {
        return "true";
    }

    return "false";
}

void check_bool(const std::string& name, bool expected, bool actual, int& tests, int& failed) {
    ++tests;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << bool_text(expected) << ", actual " << bool_text(actual) << "\n";
        ++failed;
    }
}

int main() {
    int tests{0};
    int failed{0};

    check_bool("A {0, 0, false}", true, can_borrow(LoanRequest{0, 0, false}), tests, failed);
    check_bool("B {2, 0, false}", true, can_borrow(LoanRequest{2, 0, false}), tests, failed);
    check_bool("C {4, 0, false}", true, can_borrow(LoanRequest{4, 0, false}), tests, failed);
    check_bool("D {5, 0, false}", false, can_borrow(LoanRequest{5, 0, false}), tests, failed);
    check_bool("E {2, 1, false}", false, can_borrow(LoanRequest{2, 1, false}), tests, failed);
    check_bool("F {2, 0, true}", false, can_borrow(LoanRequest{2, 0, true}), tests, failed);
    check_bool("G {-1, 0, false}", false, can_borrow(LoanRequest{-1, 0, false}), tests, failed);
    check_bool("H {6, 0, false}", false, can_borrow(LoanRequest{6, 0, false}), tests, failed);
    check_bool("I {2, -1, false}", false, can_borrow(LoanRequest{2, -1, false}), tests, failed);
    check_bool("J {5, 2, true}", false, can_borrow(LoanRequest{5, 2, true}), tests, failed);
    check_bool("K {2, 30, false}", false, can_borrow(LoanRequest{2, 30, false}), tests, failed);
    check_bool("L {2, 31, false}", false, can_borrow(LoanRequest{2, 31, false}), tests, failed);

    std::cout << "Tests: " << tests << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

<!-- output: loan_strong_tests_overdue_bug -->
```text
PASS A {0, 0, false}
PASS B {2, 0, false}
PASS C {4, 0, false}
PASS D {5, 0, false}
FAIL E {2, 1, false}: expected false, actual true
PASS F {2, 0, true}
PASS G {-1, 0, false}
PASS H {6, 0, false}
PASS I {2, -1, false}
PASS J {5, 2, true}
PASS K {2, 30, false}
PASS L {2, 31, false}
Tests: 12, failed: 1
```

Exit code: 1.

**No check of a negative number.** G detects it: minus one book, nothing overdue, not blocked.

<!-- example: loan_strong_tests_negative_bug exit=1 -->
```cpp
#include <iostream>
#include <string>

struct LoanRequest {
    int borrowed_books;
    int days_overdue;
    bool blocked;
};

bool can_borrow(const LoanRequest& request) {
    if (request.borrowed_books > 5) {
        return false;
    }

    if (request.days_overdue < 0 || request.days_overdue > 30) {
        return false;
    }

    return request.borrowed_books < 5 && request.days_overdue == 0 && !request.blocked;
}

std::string bool_text(bool value) {
    if (value) {
        return "true";
    }

    return "false";
}

void check_bool(const std::string& name, bool expected, bool actual, int& tests, int& failed) {
    ++tests;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << bool_text(expected) << ", actual " << bool_text(actual) << "\n";
        ++failed;
    }
}

int main() {
    int tests{0};
    int failed{0};

    check_bool("A {0, 0, false}", true, can_borrow(LoanRequest{0, 0, false}), tests, failed);
    check_bool("B {2, 0, false}", true, can_borrow(LoanRequest{2, 0, false}), tests, failed);
    check_bool("C {4, 0, false}", true, can_borrow(LoanRequest{4, 0, false}), tests, failed);
    check_bool("D {5, 0, false}", false, can_borrow(LoanRequest{5, 0, false}), tests, failed);
    check_bool("E {2, 1, false}", false, can_borrow(LoanRequest{2, 1, false}), tests, failed);
    check_bool("F {2, 0, true}", false, can_borrow(LoanRequest{2, 0, true}), tests, failed);
    check_bool("G {-1, 0, false}", false, can_borrow(LoanRequest{-1, 0, false}), tests, failed);
    check_bool("H {6, 0, false}", false, can_borrow(LoanRequest{6, 0, false}), tests, failed);
    check_bool("I {2, -1, false}", false, can_borrow(LoanRequest{2, -1, false}), tests, failed);
    check_bool("J {5, 2, true}", false, can_borrow(LoanRequest{5, 2, true}), tests, failed);
    check_bool("K {2, 30, false}", false, can_borrow(LoanRequest{2, 30, false}), tests, failed);
    check_bool("L {2, 31, false}", false, can_borrow(LoanRequest{2, 31, false}), tests, failed);

    std::cout << "Tests: " << tests << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

<!-- output: loan_strong_tests_negative_bug -->
```text
PASS A {0, 0, false}
PASS B {2, 0, false}
PASS C {4, 0, false}
PASS D {5, 0, false}
PASS E {2, 1, false}
PASS F {2, 0, true}
FAIL G {-1, 0, false}: expected false, actual true
PASS H {6, 0, false}
PASS I {2, -1, false}
PASS J {5, 2, true}
PASS K {2, 30, false}
PASS L {2, 31, false}
Tests: 12, failed: 1
```

Exit code: 1.

**The map of bugs.** The lines A, B and J in each of the four results are exactly the weak suite of section 4, so you can see that it would pass without a `FAIL` for every version with a bug.

| Bug | What still works correctly | The weak suite A, B, J | The bug-revealing case | Expected | Actual | Why J doesn't detect it |
|---|---|---|---|---|---|---|
| the block left out (section 4) | the limit, the overdue, the ranges | PASS | F | `false` | `true` | the limit and the overdue already reject J |
| a wrong limit boundary | 0–4 books, the overdue, the block, the ranges | PASS | D | `false` | `true` | the overdue and the block already reject J |
| a wrong overdue boundary | 0 and 2–30 days, the limit, the block, the ranges | PASS | E | `false` | `true` | the limit and the block already reject J |
| no check of a negative number | 0–6 books, the overdue, the block | PASS | G | `false` | `true` | J has no negative number of books |

- Each bug is detected by a case in which **the only reason for refusing** is exactly the broken condition.
- H and I detect none of these versions: 6 books and -1 day overdue are rejected not only by the range check but also by the last line of the function. They stay in the suite because they check what the contract says about invalid input, whatever way the function is written. If someone rewrote it without separate range checks, with the condition `borrowed_books != 5` instead of `< 5`, H would give `FAIL`.
- **This isn't a formal testing method**, only a way of checking whether the cases can detect anything: you plant one bug on purpose and watch whether some test gives `FAIL`. A suite that detects these four bugs won't detect every possible mistake.

</details>

## 9. Diagnostic: FAIL with a correct function

**The situation.** Someone added a test for a reader with five books. The function `can_borrow` is **correct** here, as in section 2.

<!-- example: loan_wrong_expected exit=1 -->
```cpp
#include <iostream>
#include <string>

struct LoanRequest {
    int borrowed_books;
    int days_overdue;
    bool blocked;
};

bool can_borrow(const LoanRequest& request) {
    if (request.borrowed_books < 0 || request.borrowed_books > 5) {
        return false;
    }

    if (request.days_overdue < 0 || request.days_overdue > 30) {
        return false;
    }

    return request.borrowed_books < 5 && request.days_overdue == 0 && !request.blocked;
}

std::string bool_text(bool value) {
    if (value) {
        return "true";
    }

    return "false";
}

void check_bool(const std::string& name, bool expected, bool actual, int& tests, int& failed) {
    ++tests;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << bool_text(expected) << ", actual " << bool_text(actual) << "\n";
        ++failed;
    }
}

int main() {
    int tests{0};
    int failed{0};

    check_bool("C {4, 0, false}", true, can_borrow(LoanRequest{4, 0, false}), tests, failed);
    check_bool("D {5, 0, false}", true, can_borrow(LoanRequest{5, 0, false}), tests, failed);

    std::cout << "Tests: " << tests << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

**This is the third required run: one diagnostic task.**

1. Read the contract of section 2.
2. Work out the expected result for D from the contract on your own.
3. Run the program and check whether the function really breaks the contract.
4. Decide where the mistake is: in the function or in the test.
5. Fix what is wrong.
6. Run the program again.
7. Explain why you must not change a correct function just to get `PASS`.

<details>
<summary>Standard output and exit code</summary>

<!-- output: loan_wrong_expected -->
```text
PASS C {4, 0, false}
FAIL D {5, 0, false}: expected true, actual false
Tests: 2, failed: 1
```

CLion shows `Process finished with exit code 1`.

</details>

<details>
<summary>Explanation and fix</summary>

- **The result from the contract:** a loan is possible only with `borrowed_books < 5`. Five books is the limit reached, so the expected result for D is `false`.
- **The function returns `false`**, exactly what the contract says. The function is correct. What's wrong is **the expected result in the test**, an **incorrect expected result**: someone wrote `true`.
- **The fix:** in test D, change `true` to `false`. You don't change the function.

<!-- example: loan_wrong_expected_fixed -->
```cpp
#include <iostream>
#include <string>

struct LoanRequest {
    int borrowed_books;
    int days_overdue;
    bool blocked;
};

bool can_borrow(const LoanRequest& request) {
    if (request.borrowed_books < 0 || request.borrowed_books > 5) {
        return false;
    }

    if (request.days_overdue < 0 || request.days_overdue > 30) {
        return false;
    }

    return request.borrowed_books < 5 && request.days_overdue == 0 && !request.blocked;
}

std::string bool_text(bool value) {
    if (value) {
        return "true";
    }

    return "false";
}

void check_bool(const std::string& name, bool expected, bool actual, int& tests, int& failed) {
    ++tests;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << bool_text(expected) << ", actual " << bool_text(actual) << "\n";
        ++failed;
    }
}

int main() {
    int tests{0};
    int failed{0};

    check_bool("C {4, 0, false}", true, can_borrow(LoanRequest{4, 0, false}), tests, failed);
    check_bool("D {5, 0, false}", false, can_borrow(LoanRequest{5, 0, false}), tests, failed);

    std::cout << "Tests: " << tests << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

<!-- output: loan_wrong_expected_fixed -->
```text
PASS C {4, 0, false}
PASS D {5, 0, false}
Tests: 2, failed: 0
```

Exit code: 0. The same, unchanged function passes the corrected test.

- **Why not change the function:** if you changed `< 5` to `<= 5`, the test would pass, but the function would give out a sixth book, that is, break the contract. Such a "fix" would put exactly the bug of section 8 into the function.

</details>

**The most important rule of this diagnostic: `FAIL` points to a mismatch, but doesn't decide by itself whether the mistake is in the function or in the test.** The contract decides. At every `FAIL`, first work out the correct result from the contract, and only then decide what to fix.

## 10. Mission: booking a room

A school room is available from 8 to 20. A function checks whether a booking for the given hours can be accepted.

**The contract of the function `bool is_valid_slot(int start_hour, int end_hour)`:**

- the hours are whole numbers: the start and the end of the booking;
- a slot is valid **if and only if** all of these hold at once: it starts no earlier than 8, it ends no later than 20, the start is earlier than the end (`start_hour < end_hour`), and it lasts at most three hours;
- the length of the slot is `end_hour - start_hour`;
- there are no dates, minutes or calendar.

For example: 8–9 is a valid slot, 8–12 is too long, and 20–20 has no length at all.

In `cpp-workspace`, create a folder `room_booking`, copy `main.cpp` and `CMakeLists.txt` from the original `lesson_05_first_program` into it, and open it in CLion. Write the function and the test program on your own in `main.cpp`. You may adapt your test program of lesson 13.1 or the function `check_bool` of this lesson. Leave `CMakeLists.txt` unchanged.

**The order of work:**

1. **Analyse the contract.** List its conditions and all its boundaries: which values lie just on one side and just on the other side of each of them?
2. **Plan the cases before you write code.** Prepare a table with the columns: case, `start_hour`, `end_hour`, expected result, kind (typical, boundary, invalid input) and the reason from the contract. Make sure that every condition is, at least once, the **only** reason for rejecting.
3. Write `is_valid_slot`.
4. Write the test program: a check of a `bool` result, a name for every test, `PASS` or `FAIL` with the expected and actual results, a summary, and exit code 1 after a failure.
5. **This is the fourth required run:** run the program with the correct function. Every test should pass, and the exit code should be 0.
6. **A deliberate bug.** Make the function reject a slot that lasts exactly three hours, and work the same otherwise.
7. **This is the fifth required run:** run the same test program with the buggy function. Write down which test detected the bug and what the exit code was. If no test gave `FAIL`, add a case that tells the two versions apart, and run the tests again. Then restore the correct function and run the tests once more.
8. **Justify your choice.** For the three cases you consider most important, write in one sentence which mistake in the function each of them would detect.

<details>
<summary>Expected results: open after preparing your own table</summary>

| Case | `start_hour` | `end_hour` | Expected result | Kind and reason |
|---|---:|---:|---|---|
| A | 8 | 9 | `true` | typical; starts exactly at 8 |
| B | 8 | 11 | `true` | boundary: exactly three hours |
| C | 8 | 12 | `false` | boundary: four hours, too long |
| D | 7 | 10 | `false` | boundary: starts before 8 |
| E | 19 | 20 | `true` | boundary: ends exactly at 20 |
| F | 20 | 20 | `false` | zero length |
| G | 18 | 21 | `false` | boundary: ends after 20 |
| H | 10 | 9 | `false` | invalid input: the end before the start |
| I | 17 | 20 | `true` | boundary: three hours and ends at 20 |
| J | 8 | 8 | `false` | zero length at the start of the day |

</details>

### Success criteria

- The program builds as C++20, and `CMakeLists.txt` is as in lesson 0.5.
- The table of cases was made before the code, and the expected results follow from the contract.
- The suite has typical cases, boundary cases on both sides of the boundaries and cases of invalid input, and every condition of the contract is, at least once, the only reason for rejecting.
- Every test has a name and prints `PASS` or `FAIL` with the expected and actual results, and at the end the program prints a summary.
- With the correct function every test passes, and the exit code is 0.
- With the deliberate bug at least one test gives `FAIL`, and the exit code is 1.
- After the correct function is restored, every test passes again.
- You can point to the case that tells the correct function apart from the version with the bug, and justify the three most important cases.

When the result matches, you can save the project in Git, as in lesson 1.5: `main.cpp` and `CMakeLists.txt`, without the build folder.

<details>
<summary>Hint 1: the result from the specification</summary>

For every case, go through the conditions of the contract one by one, on paper: is the start no earlier than 8? Is the end no later than 20? Is the start before the end? What is `end_hour - start_hour`? Write down the expected result before you run anything.

</details>

<details>
<summary>Hint 2: the boundaries</summary>

Every number in the contract, 8, 20 and 3, is a boundary. Check a value exactly at the boundary and just on both sides of it: for example a slot that lasts 3 and 4 hours, or one that ends at 20 and at 21. The relation `start_hour < end_hour` is a boundary too: what happens when both hours are equal?

</details>

<details>
<summary>Hint 3: detecting the bug</summary>

Choose a case for which the correct function and the version with the deliberate bug should return **different** results. If the bug concerns slots that last exactly three hours, which of your cases has exactly that length while satisfying all the other conditions?

</details>

## 11. When something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| Every test passes, although the function has a deliberate bug | No case tells the two versions apart: there's no test exactly at the broken boundary, or the cases break several conditions at once. | Add a case in which the broken condition is the only reason for the result, and run the tests again. |
| `FAIL` for a function that seems correct | The mistake may be in the expected result (section 9). | Work out the result from the contract again. Fix the side that doesn't match the contract, not the side that's easier to change. |
| `expected 1, actual 0` instead of `true` and `false` | The `bool` value went to `std::cout` directly (lesson 3.2). | Print it through a function that turns a `bool` into text, like `bool_text`. |
| A case with the block gives an unexpected result | The values in the braces are in a different order from the record's fields. | Give them in the order of the fields: the number of books, the days overdue, the block. |
| The suite has many tests but doesn't detect the deliberate bug | Many cases check the same situation, for example only typical data. | Judge every case by which mistake it could detect, not by the number of tests. |

## 12. Explain

Answer in your own words, preferably in writing. Only then compare with the example answers.

1. Why doesn't it prove that a function is correct when every test gives `PASS`?
2. How is a weak test suite different from a stronger one?
3. Why aren't typical cases enough on their own?
4. Why is it worth checking boundaries, and on both sides?
5. Why is it worth checking every condition separately?
6. Why may one case that breaks three conditions at once not be enough?
7. Where do expected results come from?
8. Does `FAIL` always mean a bug in the checked function?
9. How do you find out whether the function or the expected result is wrong?
10. How do you check whether a new test can really detect a particular bug?

<details>
<summary>Example answers</summary>

1. Because tests check only the chosen cases. `PASS` means that for them the function matches the contract. For cases nobody checked, the function may be wrong, like the version without the block for A, B and J.
2. A weak suite passes for versions of the function with a bug as well. A stronger one tells more such versions apart from the correct function. The strength of a suite is decided by the choice of cases, not their number.
3. Because in a typical case all the conditions hold at once, usually far from the boundaries. Such data won't show a mistake in a single condition or at a boundary.
4. Because a mistake is most likely at a boundary, for example `<=` instead of `<`. A value on one side checks that the boundary is in the right place, and a value on the other side that the result really changes.
5. Because then the result depends on one condition only. If the function leaves it out or checks it wrongly, the test gives `FAIL`.
6. Because the function rejects such a case if it checks any one of the three conditions. The test won't show that one of the others is left out or broken.
7. From the function's contract. They're worked out before the test runs, and never from what the function currently returns.
8. No. `FAIL` only points to a mismatch between the actual and the expected result. The mistake may be in the function or in the test itself, for example in a wrongly worked-out expected result.
9. Work out the result from the contract again. If the contract agrees with the function, the test is wrong. If it agrees with the expected result, the function is wrong.
10. Plant on purpose the bug the test is meant for, run the test and check that it gives `FAIL`. Then restore the correct function and check that the test passes again.

</details>

## Summary

- When every test passes, the prepared suite didn't detect a mismatch. That doesn't prove the function correct.
- A working test program, correct expected results, well-chosen cases and a correct function are four different things.
- **Typical cases** are needed but check little. **Boundary cases** check both sides of every boundary from the contract. Cases of **invalid input** check values outside the range.
- To check one condition, break only that condition. A case that breaks many conditions at once doesn't replace checking each of them separately.
- A suite's strength is judged by whether it tells the correct function apart from versions with a bug, not by the number of tests.
- A boundary case is most valuable where the result should differ on the two sides of the boundary.
- `FAIL` points to a mismatch. Whether the mistake is in the function or in the test is decided by the contract.

## What's next

So far the checked functions got ready values. In the next lesson of Module 13 you'll test a function that reads data from a stream. That lesson is in preparation.

---

## Example solutions

Look here **after your own attempt**. This is one of the correct solutions. Your names, the order of the tests and the number of cases may differ, as long as the suite checks every boundary and every condition, and the test program compares the expected result with the actual one, prints a verdict, counts the failures and sets the exit code.

<details>
<summary>Section 10: the mission, booking a room</summary>

**`main.cpp`** with the correct function and tests of cases A–J:

<!-- example: slot_tests -->
```cpp
#include <iostream>
#include <string>

bool is_valid_slot(int start_hour, int end_hour) {
    if (start_hour < 8 || end_hour > 20) {
        return false;
    }

    if (start_hour >= end_hour) {
        return false;
    }

    return end_hour - start_hour <= 3;
}

std::string bool_text(bool value) {
    if (value) {
        return "true";
    }

    return "false";
}

void check_bool(const std::string& name, bool expected, bool actual, int& tests, int& failed) {
    ++tests;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << bool_text(expected) << ", actual " << bool_text(actual) << "\n";
        ++failed;
    }
}

int main() {
    int tests{0};
    int failed{0};

    check_bool("A 8-9", true, is_valid_slot(8, 9), tests, failed);
    check_bool("B 8-11", true, is_valid_slot(8, 11), tests, failed);
    check_bool("C 8-12", false, is_valid_slot(8, 12), tests, failed);
    check_bool("D 7-10", false, is_valid_slot(7, 10), tests, failed);
    check_bool("E 19-20", true, is_valid_slot(19, 20), tests, failed);
    check_bool("F 20-20", false, is_valid_slot(20, 20), tests, failed);
    check_bool("G 18-21", false, is_valid_slot(18, 21), tests, failed);
    check_bool("H 10-9", false, is_valid_slot(10, 9), tests, failed);
    check_bool("I 17-20", true, is_valid_slot(17, 20), tests, failed);
    check_bool("J 8-8", false, is_valid_slot(8, 8), tests, failed);

    std::cout << "Tests: " << tests << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

<!-- output: slot_tests -->
```text
PASS A 8-9
PASS B 8-11
PASS C 8-12
PASS D 7-10
PASS E 19-20
PASS F 20-20
PASS G 18-21
PASS H 10-9
PASS I 17-20
PASS J 8-8
Tests: 10, failed: 0
```

Exit code: 0. The prepared suite didn't detect a mismatch in this version of the function.

- **The function:** first the room's opening hours, then the order of the start and the end, finally the length. `start_hour >= end_hour` rejects both a zero length (F, J) and an end before the start (H).
- **Why these cases:** B and C check the boundary of the length (3 and 4 hours), A and D the boundary of the start (8 and 7), E and G the boundary of the end (20 and 21), F and J a zero length, H the reversed order, and I combines the largest allowed length with an end exactly at 20.

**The deliberate bug of the mission: rejecting exactly three hours**, `end_hour - start_hour < 3` instead of `<= 3`:

<!-- example: slot_tests_three_hours_bug exit=1 -->
```cpp
#include <iostream>
#include <string>

bool is_valid_slot(int start_hour, int end_hour) {
    if (start_hour < 8 || end_hour > 20) {
        return false;
    }

    if (start_hour >= end_hour) {
        return false;
    }

    return end_hour - start_hour < 3;
}

std::string bool_text(bool value) {
    if (value) {
        return "true";
    }

    return "false";
}

void check_bool(const std::string& name, bool expected, bool actual, int& tests, int& failed) {
    ++tests;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << bool_text(expected) << ", actual " << bool_text(actual) << "\n";
        ++failed;
    }
}

int main() {
    int tests{0};
    int failed{0};

    check_bool("A 8-9", true, is_valid_slot(8, 9), tests, failed);
    check_bool("B 8-11", true, is_valid_slot(8, 11), tests, failed);
    check_bool("C 8-12", false, is_valid_slot(8, 12), tests, failed);
    check_bool("D 7-10", false, is_valid_slot(7, 10), tests, failed);
    check_bool("E 19-20", true, is_valid_slot(19, 20), tests, failed);
    check_bool("F 20-20", false, is_valid_slot(20, 20), tests, failed);
    check_bool("G 18-21", false, is_valid_slot(18, 21), tests, failed);
    check_bool("H 10-9", false, is_valid_slot(10, 9), tests, failed);
    check_bool("I 17-20", true, is_valid_slot(17, 20), tests, failed);
    check_bool("J 8-8", false, is_valid_slot(8, 8), tests, failed);

    std::cout << "Tests: " << tests << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

<!-- output: slot_tests_three_hours_bug -->
```text
PASS A 8-9
FAIL B 8-11: expected true, actual false
PASS C 8-12
PASS D 7-10
PASS E 19-20
PASS F 20-20
PASS G 18-21
PASS H 10-9
FAIL I 17-20: expected true, actual false
PASS J 8-8
Tests: 10, failed: 2
```

Exit code: 1. After `<= 3` is restored, the program gives the result of the first program again, and code 0.

**Two other versions with a bug**, each with one change. Check whether your suite would detect them too.

**Allowing a zero length**, `start_hour > end_hour` instead of `>=`:

<!-- example: slot_tests_zero_length_bug exit=1 -->
```cpp
#include <iostream>
#include <string>

bool is_valid_slot(int start_hour, int end_hour) {
    if (start_hour < 8 || end_hour > 20) {
        return false;
    }

    if (start_hour > end_hour) {
        return false;
    }

    return end_hour - start_hour <= 3;
}

std::string bool_text(bool value) {
    if (value) {
        return "true";
    }

    return "false";
}

void check_bool(const std::string& name, bool expected, bool actual, int& tests, int& failed) {
    ++tests;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << bool_text(expected) << ", actual " << bool_text(actual) << "\n";
        ++failed;
    }
}

int main() {
    int tests{0};
    int failed{0};

    check_bool("A 8-9", true, is_valid_slot(8, 9), tests, failed);
    check_bool("B 8-11", true, is_valid_slot(8, 11), tests, failed);
    check_bool("C 8-12", false, is_valid_slot(8, 12), tests, failed);
    check_bool("D 7-10", false, is_valid_slot(7, 10), tests, failed);
    check_bool("E 19-20", true, is_valid_slot(19, 20), tests, failed);
    check_bool("F 20-20", false, is_valid_slot(20, 20), tests, failed);
    check_bool("G 18-21", false, is_valid_slot(18, 21), tests, failed);
    check_bool("H 10-9", false, is_valid_slot(10, 9), tests, failed);
    check_bool("I 17-20", true, is_valid_slot(17, 20), tests, failed);
    check_bool("J 8-8", false, is_valid_slot(8, 8), tests, failed);

    std::cout << "Tests: " << tests << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

<!-- output: slot_tests_zero_length_bug -->
```text
PASS A 8-9
PASS B 8-11
PASS C 8-12
PASS D 7-10
PASS E 19-20
FAIL F 20-20: expected false, actual true
PASS G 18-21
PASS H 10-9
PASS I 17-20
FAIL J 8-8: expected false, actual true
Tests: 10, failed: 2
```

Exit code: 1.

**A wrong upper boundary of the hours**, `end_hour >= 20` instead of `end_hour > 20`:

<!-- example: slot_tests_end_hour_bug exit=1 -->
```cpp
#include <iostream>
#include <string>

bool is_valid_slot(int start_hour, int end_hour) {
    if (start_hour < 8 || end_hour >= 20) {
        return false;
    }

    if (start_hour >= end_hour) {
        return false;
    }

    return end_hour - start_hour <= 3;
}

std::string bool_text(bool value) {
    if (value) {
        return "true";
    }

    return "false";
}

void check_bool(const std::string& name, bool expected, bool actual, int& tests, int& failed) {
    ++tests;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << bool_text(expected) << ", actual " << bool_text(actual) << "\n";
        ++failed;
    }
}

int main() {
    int tests{0};
    int failed{0};

    check_bool("A 8-9", true, is_valid_slot(8, 9), tests, failed);
    check_bool("B 8-11", true, is_valid_slot(8, 11), tests, failed);
    check_bool("C 8-12", false, is_valid_slot(8, 12), tests, failed);
    check_bool("D 7-10", false, is_valid_slot(7, 10), tests, failed);
    check_bool("E 19-20", true, is_valid_slot(19, 20), tests, failed);
    check_bool("F 20-20", false, is_valid_slot(20, 20), tests, failed);
    check_bool("G 18-21", false, is_valid_slot(18, 21), tests, failed);
    check_bool("H 10-9", false, is_valid_slot(10, 9), tests, failed);
    check_bool("I 17-20", true, is_valid_slot(17, 20), tests, failed);
    check_bool("J 8-8", false, is_valid_slot(8, 8), tests, failed);

    std::cout << "Tests: " << tests << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

<!-- output: slot_tests_end_hour_bug -->
```text
PASS A 8-9
PASS B 8-11
PASS C 8-12
PASS D 7-10
FAIL E 19-20: expected true, actual false
PASS F 20-20
PASS G 18-21
PASS H 10-9
FAIL I 17-20: expected true, actual false
PASS J 8-8
Tests: 10, failed: 2
```

Exit code: 1.

| Bug | The cases that reveal it | The expected `FAIL` |
|---|---|---|
| rejecting exactly three hours | B, I | `expected true, actual false` |
| allowing a zero length | F, J | `expected false, actual true` |
| a wrong upper boundary of the hours | E, I | `expected true, actual false` |

- Each bug is detected by a case lying **exactly at the broken boundary**: three hours, equal hours, an end at 20.
- A, C, D and G pass for all three versions, although C, D and G lie at boundaries too. Each of these bugs changes the result on only one side of its boundary, which is why a boundary is checked from both sides. A suite of only A, C, D and G would be weak.
- If your suite didn't detect one of the versions, add a case at that boundary, with the other conditions satisfied.

</details>

**Previous lesson:** [Lesson 13.1: A program that checks the result itself](lesson_01_self_checking_program.en.md) · **Next lesson:** in preparation · [Course overview](../../README.en.md)

# Lesson 3.5: Checking data before calculating

[Polski](lesson_05_check_before_calculating.md) · **English** · [Course overview](../../README.en.md)

> **Module 3, lesson 5** · about 75 minutes
> **You need:** the `cpp-workspace` folder and the original `lesson_05_first_program` project, as before. You don't need the debugger in this lesson.
> **Pilot version.** The programs in this lesson are checked automatically on Windows, Ubuntu and macOS, including with the given input data.

## Before you start

This lesson assumes that after lessons 3.1–3.4:

- you write `if`, `else` and `else if` with braces, and combine conditions with `&&`, `||` and `!`;
- you know that `&&` doesn't evaluate its right side when the left is false;
- you know that a variable declared in a block exists only in that block;
- you remember from lesson 2.4 that `/` and `%` on whole numbers give full groups and the remainder, and that division by zero must never be performed.

## The situation

So far, the data from the user has always fitted the task. Real users, though, type zero where the program divides by it, or a negative number where it makes no sense. Today you'll learn to **check data before the program uses it**: first the check, then the decision, and only at the end the calculation.

After this lesson you will:

- explain why some calculations need the values to be checked first;
- check a divisor before `/` and `%`, and perform the calculation only in the appropriate branch;
- tell a correctly read value apart from a value that meets the task's requirements;
- combine several requirements with `&&`, and write one level of nested `if`;
- choose between a combined condition and nesting;
- use the short-circuit evaluation of `&&` in practice;
- explain what such checking doesn't cover yet.

## 1. Prepare the project

In `cpp-workspace`, create a folder `lesson_3_5` and copy `main.cpp` and `CMakeLists.txt` into it from the original `lesson_05_first_program`. You type the programs from sections 2–7 into that folder's `main.cpp`.

## 2. Candies for children

An organiser wants to share candies equally among children. The user gives the number of candies and the number of children, and the program calculates how many candies each child gets and how many are left over. That's a task for `/` and `%` from lesson 2.4.

**What happens if the number of children is zero?** From lesson 2.4 you know that in C++ you **must not** perform integer division by zero or calculate the remainder of a division by zero. Such an operation has **undefined behaviour**: the language doesn't specify what happens. The program might stop, print anything, or behave differently on every computer. What your own computer happens to do says nothing about what is correct. That's why we don't run such a program; we write it so that a division by zero can never happen.

## 3. First the check, then the calculation

The program checks the divisor first, and divides only in the branch in which it knows the divisor is suitable. In this section we assume that the number of candies isn't negative.

<!-- example: candy_share -->
```cpp
#include <iostream>

int main() {
    int candies{0};
    int children{0};

    std::cout << "Enter candies:\n";
    std::cin >> candies;
    std::cout << "Enter children:\n";
    std::cin >> children;

    if (children > 0) {
        const int candies_per_child{candies / children};
        const int remaining_candies{candies % children};

        std::cout << "Each child: " << candies_per_child << "\n";
        std::cout << "Remaining: " << remaining_candies << "\n";
    } else {
        std::cout << "Number of children must be positive\n";
    }
}
```

**Predict** what the program prints for 17 candies and 5 children, for 20 candies and 4 children, and for 12 candies and 0 children. Then check.

<!-- input: candy_share -->
```text
17
5
```

<!-- output: candy_share -->
```text
Enter candies:
Enter children:
Each child: 3
Remaining: 2
```

<!-- input: candy_share -->
```text
20
4
```

<!-- output: candy_share -->
```text
Enter candies:
Enter children:
Each child: 5
Remaining: 0
```

<!-- input: candy_share -->
```text
12
0
```

<details>
<summary>The standard output for 12 and 0</summary>

<!-- output: candy_share -->
```text
Enter candies:
Enter children:
Number of children must be positive
```

The program didn't divide by zero: the branch with `/` and `%` was skipped.

</details>

- The program **first** checks `children > 0`.
- If the condition is satisfied, it performs the calculations. By then it's known that the divisor is positive.
- If it isn't satisfied, it skips the division and prints a message. `else` **doesn't fix** a bad value: it only chooses another way.
- The calculations don't need to happen before the `if`. The result constants are declared **in the block** where they're needed, because they aren't used outside it. That's the block scope from lesson 3.2, put to practical use.

## 4. More than one requirement

A new requirement: the number of children must be **positive**, and the number of candies **can't be negative**. These are two separate questions, `children > 0` and `candies >= 0`, and both must answer "yes". You already know `&&`:

<!-- example: candy_check -->
```cpp
#include <iostream>

int main() {
    int candies{0};
    int children{0};

    std::cout << "Enter candies:\n";
    std::cin >> candies;
    std::cout << "Enter children:\n";
    std::cin >> children;

    const bool valid_values{children > 0 && candies >= 0};

    if (valid_values) {
        const int candies_per_child{candies / children};
        const int remaining_candies{candies % children};

        std::cout << "Each child: " << candies_per_child << "\n";
        std::cout << "Remaining: " << remaining_candies << "\n";
    } else {
        std::cout << "Invalid values\n";
    }
}
```

**Predict** the result for these pairs: 17 and 5, 0 and 5, 12 and 0, -3 and 4, 5 and -2. Then check.

<!-- input: candy_check -->
```text
17
5
```

<!-- output: candy_check -->
```text
Enter candies:
Enter children:
Each child: 3
Remaining: 2
```

<!-- input: candy_check -->
```text
0
5
```

<details>
<summary>The standard output for 0 and 5</summary>

<!-- output: candy_check -->
```text
Enter candies:
Enter children:
Each child: 0
Remaining: 0
```

Zero candies is an acceptable situation: each child gets zero, and nothing is left over.

</details>

<!-- input: candy_check -->
```text
12
0
```

<!-- output: candy_check -->
```text
Enter candies:
Enter children:
Invalid values
```

<!-- input: candy_check -->
```text
-3
4
```

<!-- output: candy_check -->
```text
Enter candies:
Enter children:
Invalid values
```

<!-- input: candy_check -->
```text
5
-2
```

<!-- output: candy_check -->
```text
Enter candies:
Enter children:
Invalid values
```

- Both requirements must be met, so `&&`.
- **A correct read isn't yet correct data.** `-3` is an ordinary `int` number: `std::cin` read it without trouble. For our task, though, a negative number of candies is unacceptable. The condition decides that, not the variable's type.
- The condition decides whether the program goes on to the calculations.

## 5. Two stages of decision: a nested `if`

The message `Invalid values` doesn't say **which** value is wrong. You can ask the questions in turn: first about the children, and only when that answer is good, about the candies. Then one `if` stands **inside** a branch of the other:

<!-- example: candy_check_nested -->
```cpp
#include <iostream>

int main() {
    int candies{0};
    int children{0};

    std::cout << "Enter candies:\n";
    std::cin >> candies;
    std::cout << "Enter children:\n";
    std::cin >> children;

    if (children > 0) {
        if (candies >= 0) {
            const int candies_per_child{candies / children};
            const int remaining_candies{candies % children};

            std::cout << "Each child: " << candies_per_child << "\n";
            std::cout << "Remaining: " << remaining_candies << "\n";
        } else {
            std::cout << "Candy count cannot be negative\n";
        }
    } else {
        std::cout << "Number of children must be positive\n";
    }
}
```

**Predict** the result for 17 and 5, -3 and 4, 12 and 0, and -3 and 0, where both values are wrong. Then check.

<!-- input: candy_check_nested -->
```text
17
5
```

<!-- output: candy_check_nested -->
```text
Enter candies:
Enter children:
Each child: 3
Remaining: 2
```

<!-- input: candy_check_nested -->
```text
-3
4
```

<!-- output: candy_check_nested -->
```text
Enter candies:
Enter children:
Candy count cannot be negative
```

<!-- input: candy_check_nested -->
```text
12
0
```

<!-- output: candy_check_nested -->
```text
Enter candies:
Enter children:
Number of children must be positive
```

<!-- input: candy_check_nested -->
```text
-3
0
```

<details>
<summary>The standard output for -3 and 0</summary>

<!-- output: candy_check_nested -->
```text
Enter candies:
Enter children:
Number of children must be positive
```

Both values are wrong, but the program reports only the number of children: the first condition isn't satisfied, so the program never reaches the inner `if`.

</details>

- The inner `if` runs **only** after entering the branch of the outer `if`, that is, when `children > 0`.
- Each `else` belongs to the `if` whose closing brace it follows. The inner `else` handles negative candies, and the outer one a wrong number of children. The braces and indentation show this structure.
- This way the program says **more precisely** which value doesn't meet the requirements.

**Which way to choose?**

- **One condition with `&&`** (section 4) is good when all the requirements lead to one common decision: calculate, or print one message.
- **A nested `if`** (section 5) is useful when the second question only makes sense after the first, or when each case should get its own message.

Neither is always better. Choose the one that expresses the requirement most simply. Don't nest just to make code look more advanced.

## 6. Short-circuit evaluation in practice

From lesson 3.4 you know the rule: `&&` doesn't evaluate its right side when the left is false. Now the rule becomes useful. The program checks whether each child gets **at least 3** candies. Here we assume that the number of candies isn't negative.

<!-- example: enough_for_three -->
```cpp
#include <iostream>

int main() {
    int candies{0};
    int children{0};

    std::cout << "Enter candies:\n";
    std::cin >> candies;
    std::cout << "Enter children:\n";
    std::cin >> children;

    const bool enough_for_three{children > 0 && candies / children >= 3};

    if (enough_for_three) {
        std::cout << "At least 3 each\n";
    } else {
        std::cout << "Not 3 each\n";
    }
}
```

<!-- input: enough_for_three -->
```text
12
0
```

<!-- output: enough_for_three -->
```text
Enter candies:
Enter children:
Not 3 each
```

<!-- input: enough_for_three -->
```text
12
4
```

<!-- output: enough_for_three -->
```text
Enter candies:
Enter children:
At least 3 each
```

<!-- input: enough_for_three -->
```text
8
4
```

<!-- output: enough_for_three -->
```text
Enter candies:
Enter children:
Not 3 each
```

Step by step:

1. C++ evaluates the left side of `&&` first: `children > 0`.
2. For 0 children the left side is false, so the whole `&&` is false, and the right side, `candies / children >= 3`, **isn't evaluated**. No division by zero takes place.
3. For 4 children the left side is true, so the program calculates `candies / children` and checks whether the result is at least 3: for 12 candies it's 3 (yes), for 8 only 2 (no).

This condition doesn't check that the number of candies is non-negative. That's a separate requirement, which would have to be added. Short-circuit evaluation applies to the built-in `&&` and `||` operators you're using here.

**The main pattern is still section 3:** check the data, and perform the calculation in the appropriate branch. Short-circuit evaluation shows that the order inside `&&` matters, but it's no reason to hide risky calculations in long conditions.

## 7. A wrong value vs a failed read

These are two different problems:

- **A correct read, an unsuitable value.** The user types `0` as the number of children. `std::cin` correctly reads this number into an `int` variable, but for our task it isn't an acceptable divisor. You **can already detect** this case with an `if`.
- **A failed read.** The user types text instead of a number, for example `abc`. Then reading the number **fails**. That's a different problem: checking the variable's value with an `if` doesn't reliably tell you whether the read succeeded.

The programs in this lesson detect only the first case. You'll learn to check whether a read succeeded, and to ask for the data again, later in the course. Until then, give the data as numbers. The program checks whether the numbers suit the task, but it **isn't robust** against any input whatsoever.

## 8. Find the bug: the limit at zero

The requirement from section 4: the number of children must be positive, and the number of candies **can't be negative**. So zero candies is acceptable. This program builds, never divides by zero, but judges one boundary case wrongly:

<!-- example: candy_check_bug -->
```cpp
#include <iostream>

int main() {
    int candies{0};
    int children{0};

    std::cout << "Enter candies:\n";
    std::cin >> candies;
    std::cout << "Enter children:\n";
    std::cin >> children;

    const bool valid_values{children > 0 && candies > 0};

    if (valid_values) {
        const int candies_per_child{candies / children};
        const int remaining_candies{candies % children};

        std::cout << "Each child: " << candies_per_child << "\n";
        std::cout << "Remaining: " << remaining_candies << "\n";
    } else {
        std::cout << "Invalid values\n";
    }
}
```

1. Read the requirement and **predict** what the program **should** print for 0 candies and 5 children.
2. Run the program for 0 and 5, and also for 17 and 5, and 12 and 0.
3. Find the condition that doesn't match the requirement.
4. Fix it.
5. Check the boundary cases: 0 and 5, -1 and 5, 12 and 0.

The output before the fix, and an explanation, are in [Example solutions](#example-solutions).

Note: this bug isn't about the calculation's safety, because `children > 0` still protects against division by zero. It's about the **task's requirements**: the program rejects data it should accept.

## 9. Mission: a study plan

The program divides study time into sessions. The user gives the total number of minutes and the number of sessions, and the program calculates how many **full** minutes each session gets and how many minutes are left over.

The data requirements:

- the total number of minutes can't be negative; 0 minutes is acceptable;
- the number of sessions must be positive.

If both values meet the requirements, the program performs the division and calculates the remainder. Otherwise it prints **only** `Invalid session data` and calculates nothing. We assume the user types numbers. There's no need to ask for the data again.

In `cpp-workspace`, create a folder `study_plan`, copy `CMakeLists.txt` into it from the original `lesson_05_first_program`, create an empty `main.cpp`, and write the program on your own.

For 95 minutes and 4 sessions, the standard output must be:

<!-- input: study_plan -->
```text
95
4
```

<!-- output: study_plan -->
```text
Enter total minutes:
Enter number of sessions:
Minutes per session: 23
Minutes left: 3
```

For 40 minutes and 0 sessions:

<!-- input: study_plan -->
```text
40
0
```

<!-- output: study_plan -->
```text
Enter total minutes:
Enter number of sessions:
Invalid session data
```

**Before you write the program**, prepare a table of cases. Choose values that check: correct data with and without a remainder, zero minutes, zero sessions, negative minutes and a negative number of sessions. For each case, write the expected result.

### Success criteria

- The program builds as C++20, and its standard output for each case matches the requirements and the format above.
- Both numbers are `int` variables with starting values, read with `std::cin`.
- The requirements are written as a condition (one, combined with `&&`, is enough), and the division and remainder are calculated **only** in the branch where the requirements are met.
- In no case does the program divide by zero.
- The table of cases was prepared before running the program.
- You can explain why the calculation doesn't run for zero sessions, but does for zero minutes.

Once the output matches, you can save the project in Git, as in lesson 1.5.

<details>
<summary>Hint 1</summary>

How many requirements are there, and do they all lead to one decision: calculate, or print one message? That tells you whether one condition with `&&` is enough, as in section 4.

</details>

<details>
<summary>Hint 2</summary>

Which number is the divisor, and what condition must it meet for the division to be allowed? Does zero minutes get in the way of dividing?

</details>

<details>
<summary>The full list of control cases: open after your own attempt</summary>

| Minutes | Sessions | Result | What it checks |
|---|---|---|---|
| 95 | 4 | 23 per session, 3 left | correct data, a division with a remainder |
| 60 | 3 | 20 per session, 0 left | a division without a remainder |
| 0 | 5 | 0 per session, 0 left | zero minutes is acceptable |
| 40 | 0 | `Invalid session data` | a zero divisor |
| -1 | 3 | `Invalid session data` | negative minutes |
| 40 | -2 | `Invalid session data` | a negative number of sessions |

The cases 95 and 4, and 40 and 0, are checked above, with the mission text.

<!-- input: study_plan -->
```text
60
3
```

<!-- output: study_plan -->
```text
Enter total minutes:
Enter number of sessions:
Minutes per session: 20
Minutes left: 0
```

<!-- input: study_plan -->
```text
0
5
```

<!-- output: study_plan -->
```text
Enter total minutes:
Enter number of sessions:
Minutes per session: 0
Minutes left: 0
```

<!-- input: study_plan -->
```text
-1
3
```

<!-- output: study_plan -->
```text
Enter total minutes:
Enter number of sessions:
Invalid session data
```

<!-- input: study_plan -->
```text
40
-2
```

<!-- output: study_plan -->
```text
Enter total minutes:
Enter number of sessions:
Invalid session data
```

</details>

An example solution is in [Example solutions](#example-solutions).

## 10. When something goes differently

| What you see | What it means | What to do |
|---|---|---|
| The calculation comes before the `if` that checks the divisor | The division runs before the program checks the divisor. | Move the calculation into the branch where the divisor has already been checked. |
| The program rejects an acceptable value, for example 0 minutes | A limit in the condition is shifted: `>` instead of `>=`. | Check every limit of the requirements from both sides. |
| The program accepts a value it shouldn't | One of the requirements is missing, or `\|\|` was used instead of `&&`. | List all the requirements and check that each one is in the condition. |
| An `else` doesn't match the right `if` | A brace is missing in the nesting, or the indentation is misleading. | Each `else` belongs to the `if` whose closing brace it follows. Check the pairs of braces. |
| After typing text instead of a number, the result is strange | That's a failed read, not a wrong value. The program doesn't handle it yet. | Type numbers. You'll learn to handle failed reads later. |
| `use of undeclared identifier` for a calculation's result | A result declared in a block is used outside it. | Use it in the same block, or declare the variable before the `if`. |

## 11. Explain

Answer in your own words, preferably in writing. Only then compare with the example answer.

**1.** Why does the program in section 3 divide only in the branch `if (children > 0)`?

<details>
<summary>Example answer</summary>

Because integer division by zero isn't allowed (it has undefined behaviour). In that branch it's already known that the number of children is positive, so the division is safe. For 0 children the program chooses the `else` branch and doesn't divide at all.

</details>

**2.** The number `-3` was read without any problem. Why does the program reject it?

<details>
<summary>Example answer</summary>

Because a correct read doesn't mean the value meets the task's requirements. `-3` is a correct `int` number, but a negative number of candies makes no sense in this task, so the condition rejects it.

</details>

**3.** When do you choose one condition with `&&`, and when a nested `if`?

<details>
<summary>Example answer</summary>

One condition when all the requirements lead to one decision. A nested `if` when the second question only makes sense after the first, or when each case should get its own message.

</details>

**4.** Why doesn't `children > 0 && candies / children >= 3` divide by zero for 0 children?

<details>
<summary>Example answer</summary>

Because `&&` evaluates the left side first. For 0 children, `children > 0` is false, so the whole thing is false, and the right side with the division isn't evaluated.

</details>

**5.** How does typing `0` as the number of children differ from typing `abc`?

<details>
<summary>Example answer</summary>

`0` is a correctly read number that doesn't meet the task's requirements. The program detects it with an `if`. `abc` is a failed read of a number. That's a different problem, which the program doesn't handle yet.

</details>

## Summary

- **First the check, then the decision, and at the end the calculation.** Perform a risky operation, such as dividing by a value from input, only in a branch where the data has already been checked.
- `else` doesn't fix a bad value. It chooses another way, for example a message instead of a calculation.
- A correct read isn't the same as correct data: a number can be a correct `int` and still not meet the task's requirements.
- You combine several requirements with `&&`. A nested `if` is useful when the second question only makes sense after the first, or when the cases have separate messages.
- Short-circuit evaluation of `&&` means that in `children > 0 && candies / children >= 3`, the division doesn't run for 0 children. The main pattern is still calculating in the checked branch.
- The programs in this lesson detect wrong values, but not failed reads. You'll learn that later.

## What's next

You now know all the tools of Module 3: `if`, `else`, `else if`, comparisons, `bool`, logical operators, and checking data before calculating. In lesson 3.6 you'll test them in an independent task. **Lesson 3.6 is in preparation.**

---

## Example solutions

Look here **after your own attempt**. Your names may differ, as long as the standard output is as required.

<details>
<summary>Section 8: the output before the fix, and the fix</summary>

Before the fix:

<!-- input: candy_check_bug -->
```text
0
5
```

<!-- output: candy_check_bug -->
```text
Enter candies:
Enter children:
Invalid values
```

<!-- input: candy_check_bug -->
```text
17
5
```

<!-- output: candy_check_bug -->
```text
Enter candies:
Enter children:
Each child: 3
Remaining: 2
```

<!-- input: candy_check_bug -->
```text
12
0
```

<!-- output: candy_check_bug -->
```text
Enter candies:
Enter children:
Invalid values
```

For 0 candies and 5 children the program prints `Invalid values`, although the requirement allows zero candies. The condition `candies > 0` excludes zero itself. It should be `candies >= 0`, that is, "not negative". The fixed program is the program from section 4, which prints `Each child: 0` and `Remaining: 0` for 0 and 5, and `Invalid values` for -3 and 4 and for 12 and 0.

</details>

<details>
<summary>Section 9: mission, a study plan</summary>

<!-- example: study_plan -->
```cpp
#include <iostream>

int main() {
    int total_minutes{0};
    int sessions{0};

    std::cout << "Enter total minutes:\n";
    std::cin >> total_minutes;
    std::cout << "Enter number of sessions:\n";
    std::cin >> sessions;

    const bool valid_data{sessions > 0 && total_minutes >= 0};

    if (valid_data) {
        const int minutes_per_session{total_minutes / sessions};
        const int minutes_left{total_minutes % sessions};

        std::cout << "Minutes per session: " << minutes_per_session << "\n";
        std::cout << "Minutes left: " << minutes_left << "\n";
    } else {
        std::cout << "Invalid session data\n";
    }
}
```

- Two requirements lead to one decision, so one condition with `&&` is enough.
- `/` and `%` stand in the branch where `sessions > 0`, so a division by zero never runs.
- `total_minutes >= 0` allows zero: 0 minutes divided into sessions gives 0 per session and 0 left over.

</details>

**Previous lesson:** [Lesson 3.4: Combining conditions (`&&`, `||`, `!`)](lesson_04_combining_conditions.en.md) · **Next lesson:** in preparation · [Course overview](../../README.en.md)

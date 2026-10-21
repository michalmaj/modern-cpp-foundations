# Lesson 3.3: Choosing among many possibilities (`else if`)

[Polski](lesson_03_many_possibilities.md) · **English** · [Course overview](../../README.en.md)

> **Module 3, lesson 3** · about 75 minutes
> **You need:** the `cpp-workspace` folder and the original `lesson_05_first_program` project, as before. You don't need the debugger in this lesson.
> **Pilot version.** The programs in this lesson are checked automatically on Windows, Ubuntu and macOS, including with the given input data.

## Before you start

This lesson assumes that after lessons 3.1 and 3.2:

- you write `if` and `if`/`else` with braces and the comparisons `<`, `<=`, `>`, `>=`, `==`, `!=`;
- you know that exactly one of the two branches runs in an `if`/`else`;
- you check a program exactly at a limit and right next to it;
- you know that a variable declared in a block exists only in that block.

## The situation

In lesson 3.2, a program chose one of two ways: `Passed` or `Not passed`. Often, though, there are more possibilities: a result can be weak, fair, good or excellent, and a ticket can be reduced, regular or for seniors. Today you'll meet `else if`, a way to choose **one of several** ways. You'll also learn to **plan test cases** for every limit before you run the program.

After this lesson you will:

- recognise when `if`/`else` is no longer enough;
- choose one of several branches with a chain of `if`, `else if` and `else`;
- explain that the conditions are checked in order, and that the branch of the first satisfied condition runs;
- find bugs caused by the order of the conditions;
- know when a chain needs a final `else`;
- tell separate `if`s apart from one chain;
- prepare a table of boundary cases before writing a program.

## 1. Prepare the project

In `cpp-workspace`, create a folder `lesson_3_3` and copy `main.cpp` and `CMakeLists.txt` into it from the original `lesson_05_first_program`. You type the programs from sections 2–7 into that folder's `main.cpp`.

## 2. More than two results

The program gets a number of points from 0 to 100 and must assign one of four levels:

| Points | Result |
|---|---|
| 0–49 | `Needs work` |
| 50–74 | `Pass` |
| 75–89 | `Good` |
| 90–100 | `Excellent` |

One `if`/`else` gives only two ways, and here there are four. You need a **chain** of conditions:

<!-- example: score_level -->
```cpp
#include <iostream>

int main() {
    int score{0};

    std::cout << "Enter score (0-100):\n";
    std::cin >> score;

    if (score >= 90) {
        std::cout << "Excellent\n";
    } else if (score >= 75) {
        std::cout << "Good\n";
    } else if (score >= 50) {
        std::cout << "Pass\n";
    } else {
        std::cout << "Needs work\n";
    }

    std::cout << "Score checked\n";
}
```

**Predict** what the program prints for 49, 75 and 90. Write down your answers, then run the program three times.

<!-- input: score_level -->
```text
49
```

<details>
<summary>The standard output for 49</summary>

<!-- output: score_level -->
```text
Enter score (0-100):
Needs work
Score checked
```

</details>

<!-- input: score_level -->
```text
75
```

<details>
<summary>The standard output for 75</summary>

<!-- output: score_level -->
```text
Enter score (0-100):
Good
Score checked
```

</details>

<!-- input: score_level -->
```text
90
```

<details>
<summary>The standard output for 90</summary>

<!-- output: score_level -->
```text
Enter score (0-100):
Excellent
Score checked
```

</details>

## 3. How the chain works

The chain starts with `if`, then come further `else if`s (each is the word `else` followed by a new `if` with a condition), and at the end an `else`. The program goes through it **from the top**:

1. It checks the first condition, `score >= 90`.
2. If it isn't satisfied, it checks the next one, `score >= 75`, and so on.
3. When a condition is satisfied, it executes **that condition's** branch.
4. It **skips** the remaining branches of this chain: it doesn't check their conditions any more.
5. If no condition is satisfied, it executes the branch of the final `else`.
6. After the chain the program carries on: `Score checked` always appears.

**Predict the result for 95.** 95 satisfies `score >= 90`, but also `score >= 75` and `score >= 50`. What does the program print? Check.

<!-- input: score_level -->
```text
95
```

<details>
<summary>The standard output for 95, and an explanation</summary>

<!-- output: score_level -->
```text
Enter score (0-100):
Excellent
Score checked
```

Only `Excellent`. The program doesn't evaluate all the conditions and then pick the best one. It goes **in the order written in the code**: the first condition, `score >= 90`, is satisfied, so the first branch runs, and the rest of the chain is skipped. That 95 also satisfies the later conditions no longer matters.

</details>

That's why the thresholds in this chain go **from the highest**: the program reaches `else if (score >= 75)` only when `score >= 90` wasn't satisfied. So that branch handles exactly the results from 75 to 89.

## 4. Plan the test cases

The program was checked for 49, 75, 90 and 95. Is that enough? **Before you look further:**

1. Write down the values worth checking. Think about each limit between the levels: the limit itself, and the value right next to it, on the other side.
2. Next to each value, write the result you predict.
3. Run the program for your values and compare.

Some questions to help: what does the program print for 50? For 74? For 89? Why is the result for 100 still `Excellent`? Can the program print more than one level at once?

<details>
<summary>The full list of control cases: open after your own attempt</summary>

Each of the three limits (50, 75, 90) is checked from both sides, plus both ends of the range, 0 and 100:

| Points | Result | Why this value |
|---|---|---|
| 0 | `Needs work` | the lower end of the range |
| 49 | `Needs work` | right below the limit 50 |
| 50 | `Pass` | the limit 50 |
| 74 | `Pass` | right below the limit 75 |
| 75 | `Good` | the limit 75 |
| 89 | `Good` | right below the limit 90 |
| 90 | `Excellent` | the limit 90 |
| 100 | `Excellent` | the upper end of the range |

<!-- input: score_level -->
```text
0
```

<!-- output: score_level -->
```text
Enter score (0-100):
Needs work
Score checked
```

<!-- input: score_level -->
```text
50
```

<!-- output: score_level -->
```text
Enter score (0-100):
Pass
Score checked
```

<!-- input: score_level -->
```text
74
```

<!-- output: score_level -->
```text
Enter score (0-100):
Pass
Score checked
```

<!-- input: score_level -->
```text
89
```

<!-- output: score_level -->
```text
Enter score (0-100):
Good
Score checked
```

<!-- input: score_level -->
```text
100
```

<!-- output: score_level -->
```text
Enter score (0-100):
Excellent
Score checked
```

The values 49, 75 and 90 were already checked in section 2. For each value the program prints **exactly one** level, because at most one branch of a chain runs. For 100 the result is `Excellent`, because 100 satisfies `score >= 90`.

</details>

## 5. Find the bug: the wrong order

This program has the same requirements as the program in section 2. It compiles without errors, but someone put the conditions in a different order:

<!-- example: score_order_bug -->
```cpp
#include <iostream>

int main() {
    int score{0};

    std::cout << "Enter score (0-100):\n";
    std::cin >> score;

    if (score >= 50) {
        std::cout << "Pass\n";
    } else if (score >= 75) {
        std::cout << "Good\n";
    } else if (score >= 90) {
        std::cout << "Excellent\n";
    } else {
        std::cout << "Needs work\n";
    }

    std::cout << "Score checked\n";
}
```

1. Read the requirements in the table in section 2.
2. **Predict** what the program **should** print for 30, 60, 80 and 90.
3. Read the conditions in the order in which the program checks them. What happens for 80?
4. Run the program for these four values.
5. Find the first value for which the chosen branch doesn't match the requirements.
6. Fix the program.
7. Check all the limits from section 4 again.

The program's output before the fix, and two correct versions, are in [Example solutions](#example-solutions).

Each of these conditions is correct on its own: `score >= 75` really does mean "at least 75". The bug is in the **order**. When the condition `score >= 50` comes first, it catches every result from 50 upwards, so the program never reaches the `Good` and `Excellent` branches. So fixing a single operator isn't always enough: sometimes you have to rearrange the conditions.

## 6. The final `else` and a missing case

This chain has no final `else`:

<!-- example: score_no_else -->
```cpp
#include <iostream>

int main() {
    int score{0};

    std::cout << "Enter score (0-100):\n";
    std::cin >> score;

    if (score >= 90) {
        std::cout << "Excellent\n";
    } else if (score >= 75) {
        std::cout << "Good\n";
    } else if (score >= 50) {
        std::cout << "Pass\n";
    }

    std::cout << "Score checked\n";
}
```

**Predict** what the program prints for 80, and what for 30.

<!-- input: score_no_else -->
```text
80
```

<!-- output: score_no_else -->
```text
Enter score (0-100):
Good
Score checked
```

<!-- input: score_no_else -->
```text
30
```

<details>
<summary>The standard output for 30</summary>

<!-- output: score_no_else -->
```text
Enter score (0-100):
Score checked
```

</details>

For 30 no condition is satisfied, and there is no final `else`, so **no branch** of the chain runs. The program printed no level.

Must every chain end with an `else`? **It depends on the requirements.** The warning about seats running out in lesson 3.1 was deliberately optional: sometimes nothing needs doing. Here, though, the requirement says that **every** result from 0 to 100 gets a level. Then a final `else` is natural: it handles everything the earlier branches didn't.

## 7. Separate `if`s are not a chain

In lesson 3.2 a program had two independent decisions. Compare this program with the chain from section 2:

<!-- example: separate_ifs -->
```cpp
#include <iostream>

int main() {
    int score{0};

    std::cout << "Enter score (0-100):\n";
    std::cin >> score;

    if (score >= 50) {
        std::cout << "At least 50\n";
    }
    if (score >= 75) {
        std::cout << "At least 75\n";
    }
    if (score >= 90) {
        std::cout << "At least 90\n";
    }
}
```

**Predict** how many lines this program prints for 95, and how many for 60. How many levels did the chain from section 2 print for 95?

<!-- input: separate_ifs -->
```text
95
```

<details>
<summary>The standard output for 95</summary>

<!-- output: separate_ifs -->
```text
Enter score (0-100):
At least 50
At least 75
At least 90
```

</details>

<!-- input: separate_ifs -->
```text
60
```

<details>
<summary>The standard output for 60</summary>

<!-- output: separate_ifs -->
```text
Enter score (0-100):
At least 50
```

</details>

There's no `else` here, so these are three **separate** decisions: each `if` checks its condition independently of the others, and for 95 all three blocks run. In one `if`/`else if`/`else` chain, **at most one** branch runs. When the categories exclude each other and there must be one result, you need a chain.

**Variable scope.** The programs in this lesson print the result straight away in a branch, and that's enough. If the name of the level were needed **after** the chain, the pattern from lesson 3.2 applies: declare a `std::string` variable before the chain, and only assign it a value in the branches.

## 8. Mission: the ticket category

A museum sets the ticket category by the visitor's age:

| Age | Category |
|---|---|
| 0–6 | `Free` |
| 7–17 | `Youth` |
| 18–64 | `Regular` |
| 65 and over | `Senior` |

In `cpp-workspace`, create a folder `ticket_category`, copy `CMakeLists.txt` into it from the original `lesson_05_first_program`, create an empty `main.cpp`, and write the program on your own. The program reads one whole number, the age, and prints exactly one category. We assume the read succeeds and the age makes sense: a non-negative number.

For the age 30, the standard output must be:

<!-- input: ticket_category -->
```text
30
```

<!-- output: ticket_category -->
```text
Enter age:
Category: Regular
```

**Before you write the program**, prepare a table of test cases: choose values that check every limit from both sides, and next to each write the expected category. Then write the program and check it for all your values.

### Success criteria

- The program builds as C++20, and for every age it prints the request and exactly one line `Category: …`, according to the table.
- The age is an `int` variable with a starting value, read with `std::cin`.
- A chain of `if`, `else if` and `else` chooses the category, with braces around every branch.
- The conditions are in an order that makes every branch reachable. You can explain why that order is correct.
- The table of cases was prepared before running the program, and it checks every limit from both sides.
- The same program handles all cases, without changing the code.

Once the output matches, you can save the project in Git, as in lesson 1.5.

<details>
<summary>Hint 1</summary>

How many limits are there between the categories? At each one, check the limit itself and the age one year younger.

</details>

<details>
<summary>Hint 2</summary>

Order the conditions as in section 2: from the highest threshold to the lowest, each with `>=`. The final `else` handles the youngest category. You can store the thresholds as `const int` constants with names that say from which age a category starts.

</details>

<details>
<summary>The full list of control cases: open after your own attempt</summary>

| Age | Category | Limit |
|---|---|---|
| 6 | `Free` | right below 7 |
| 7 | `Youth` | 7 |
| 17 | `Youth` | right below 18 |
| 18 | `Regular` | 18 |
| 64 | `Regular` | right below 65 |
| 65 | `Senior` | 65 |

<!-- input: ticket_category -->
```text
6
```

<!-- output: ticket_category -->
```text
Enter age:
Category: Free
```

<!-- input: ticket_category -->
```text
7
```

<!-- output: ticket_category -->
```text
Enter age:
Category: Youth
```

<!-- input: ticket_category -->
```text
17
```

<!-- output: ticket_category -->
```text
Enter age:
Category: Youth
```

<!-- input: ticket_category -->
```text
18
```

<!-- output: ticket_category -->
```text
Enter age:
Category: Regular
```

<!-- input: ticket_category -->
```text
64
```

<!-- output: ticket_category -->
```text
Enter age:
Category: Regular
```

<!-- input: ticket_category -->
```text
65
```

<!-- output: ticket_category -->
```text
Enter age:
Category: Senior
```

</details>

### Variant: Senior from 60

The museum changes the rule: the `Senior` category starts at 60. Change **one threshold** in the program, propose the new boundary values, predict the results, and check that the program still assigns exactly one category.

<details>
<summary>The new boundary cases: open after your own attempt</summary>

<!-- input: ticket_category_variant -->
```text
59
```

<!-- output: ticket_category_variant -->
```text
Enter age:
Category: Regular
```

<!-- input: ticket_category_variant -->
```text
60
```

<!-- output: ticket_category_variant -->
```text
Enter age:
Category: Senior
```

The other limits (7 and 18) didn't change, so their cases give the same results as before.

</details>

Example solutions are in [Example solutions](#example-solutions).

## 9. When something goes differently

| What you see | What it means | What to do |
|---|---|---|
| The higher categories never appear | An earlier condition catches all those values, for example `>= 50` comes before `>= 75`. | Order the thresholds from highest to lowest, or change the conditions so that every branch is reachable. |
| No category appears for some values | The chain has no final `else`, and no condition is satisfied. | If every value must get a category, add a final `else`. |
| Two or more categories appear | These are separate `if`s, not one chain. | Join them into a chain: `else if` instead of another separate `if`. |
| A wrong result exactly at a limit | `>` was confused with `>=`, or a threshold is off by one. | Check every limit from both sides, using your table of cases. |
| A compile error at `else if` | A brace is missing before `else`, or the parentheses around the condition. | Each branch ends with `}`, followed by `else if (…) {`. |

## 10. Explain

Answer in your own words, preferably in writing. Only then compare with the example answer.

**1.** In what order does the program check the conditions of a chain, and when does it stop checking them?

<details>
<summary>Example answer</summary>

From the top, in the order written in the code. When it reaches the first satisfied condition, it executes that branch, and it doesn't check the remaining conditions of this chain.

</details>

**2.** Why does the program from section 2 print only `Excellent` for 95 points, although 95 also satisfies `score >= 75`?

<details>
<summary>Example answer</summary>

Because the first condition, `score >= 90`, is satisfied, so the first branch runs and the rest of the chain is skipped. The program doesn't check the later conditions any more.

</details>

**3.** What was wrong with the program in section 5, given that each condition on its own was correct?

<details>
<summary>Example answer</summary>

The order. `score >= 50` came first and caught every result from 50 upwards, so the `Good` and `Excellent` branches were unreachable.

</details>

**4.** When should a chain end with an `else`?

<details>
<summary>Example answer</summary>

When the requirements say that every value must get one of the results. Then `else` handles everything the earlier branches didn't. When the action is optional, `else` isn't needed.

</details>

**5.** How do three separate `if`s differ from an `if`/`else if`/`else` chain?

<details>
<summary>Example answer</summary>

Separate `if`s are separate decisions: several blocks can run. In a chain, at most one branch runs.

</details>

## Summary

- A chain of `if`, `else if`, …, `else` chooses **one of several** branches. `else if` is `else` followed by another `if`, not a separate keyword.
- The conditions are checked **in order**. The branch of the **first** satisfied condition runs, and the rest of the chain is skipped.
- Order matters: with thresholds using `>=`, order them from the highest, or some branches become unreachable.
- The final `else` handles everything the earlier branches didn't. It's needed when every value must get a result.
- Separate `if`s make separate decisions and can run several blocks. In a chain, at most one branch runs.
- Before running a program, prepare a table of cases: check every limit from both sides, and the ends of the range.

## What's next

Your programs now choose one of many ways, and a well-ordered chain was enough for every category. Sometimes, though, you need to check **two conditions at once**, for example whether a value lies in the range from 1 to 10. In lesson 3.4 you'll learn to combine conditions. **Lesson 3.4 is in preparation.**

---

## Example solutions

Look here **after your own attempt**. Your names may differ, as long as the standard output is as required.

<details>
<summary>Section 5: the output before the fix, and the fixed programs</summary>

Before the fix, for 30, 60, 80 and 90:

<!-- input: score_order_bug -->
```text
30
```

<!-- output: score_order_bug -->
```text
Enter score (0-100):
Needs work
Score checked
```

<!-- input: score_order_bug -->
```text
60
```

<!-- output: score_order_bug -->
```text
Enter score (0-100):
Pass
Score checked
```

<!-- input: score_order_bug -->
```text
80
```

<!-- output: score_order_bug -->
```text
Enter score (0-100):
Pass
Score checked
```

<!-- input: score_order_bug -->
```text
90
```

<!-- output: score_order_bug -->
```text
Enter score (0-100):
Pass
Score checked
```

The first value that doesn't match is 80: the requirement says `Good`, and the program prints `Pass`. For 90, too, it prints `Pass` instead of `Excellent`.

**Fix 1: thresholds from the highest.** This is the program from section 2: `>= 90`, then `>= 75`, then `>= 50`, and finally `else`. The full list in section 4 checks its limits.

**Fix 2: thresholds from the lowest, with `<`.** The order can also be the other way round, if the conditions ask "below":

<!-- example: score_ascending -->
```cpp
#include <iostream>

int main() {
    int score{0};

    std::cout << "Enter score (0-100):\n";
    std::cin >> score;

    if (score < 50) {
        std::cout << "Needs work\n";
    } else if (score < 75) {
        std::cout << "Pass\n";
    } else if (score < 90) {
        std::cout << "Good\n";
    } else {
        std::cout << "Excellent\n";
    }

    std::cout << "Score checked\n";
}
```

<!-- input: score_ascending -->
```text
49
```

<!-- output: score_ascending -->
```text
Enter score (0-100):
Needs work
Score checked
```

<!-- input: score_ascending -->
```text
50
```

<!-- output: score_ascending -->
```text
Enter score (0-100):
Pass
Score checked
```

<!-- input: score_ascending -->
```text
74
```

<!-- output: score_ascending -->
```text
Enter score (0-100):
Pass
Score checked
```

<!-- input: score_ascending -->
```text
75
```

<!-- output: score_ascending -->
```text
Enter score (0-100):
Good
Score checked
```

<!-- input: score_ascending -->
```text
89
```

<!-- output: score_ascending -->
```text
Enter score (0-100):
Good
Score checked
```

<!-- input: score_ascending -->
```text
90
```

<!-- output: score_ascending -->
```text
Enter score (0-100):
Excellent
Score checked
```

Both versions are correct. What matters is whether, in the written order, each branch handles exactly its range.

</details>

<details>
<summary>Section 8: mission, the ticket category</summary>

<!-- example: ticket_category -->
```cpp
#include <iostream>

int main() {
    const int youth_from_age{7};
    const int regular_from_age{18};
    const int senior_from_age{65};
    int age{0};

    std::cout << "Enter age:\n";
    std::cin >> age;

    if (age >= senior_from_age) {
        std::cout << "Category: Senior\n";
    } else if (age >= regular_from_age) {
        std::cout << "Category: Regular\n";
    } else if (age >= youth_from_age) {
        std::cout << "Category: Youth\n";
    } else {
        std::cout << "Category: Free\n";
    }
}
```

- The thresholds go from the highest, so the program reaches each branch only when the higher thresholds weren't satisfied. So the `Regular` branch handles exactly the ages from 18 to 64.
- The final `else` handles the youngest category: every age gets exactly one category.
- The threshold constants say from which age a category starts, and each threshold is written only once.

</details>

<details>
<summary>Section 8: the variant, Senior from 60</summary>

<!-- example: ticket_category_variant -->
```cpp
#include <iostream>

int main() {
    const int youth_from_age{7};
    const int regular_from_age{18};
    const int senior_from_age{60};
    int age{0};

    std::cout << "Enter age:\n";
    std::cin >> age;

    if (age >= senior_from_age) {
        std::cout << "Category: Senior\n";
    } else if (age >= regular_from_age) {
        std::cout << "Category: Regular\n";
    } else if (age >= youth_from_age) {
        std::cout << "Category: Youth\n";
    } else {
        std::cout << "Category: Free\n";
    }
}
```

Only the threshold `senior_from_age` changed. The new limit is 60, so you check 59 and 60.

</details>

**Previous lesson:** [Lesson 3.2: Two possibilities (`else`), equality and `bool`](lesson_02_two_ways.en.md) · **Next lesson:** in preparation · [Course overview](../../README.en.md)

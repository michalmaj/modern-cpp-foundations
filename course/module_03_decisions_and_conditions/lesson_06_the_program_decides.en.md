# Lesson 3.6: The program makes decisions (the Module 3 test)

[Polski](lesson_06_the_program_decides.md) · **English** · [Course overview](../../README.en.md)

> **Module 3, lesson 6: the test** · about 90–100 minutes, can be split into two sessions
> **You need:** the `cpp-workspace` folder and the original `lesson_05_first_program` project.
> **Pilot version.** The reference solutions in this lesson are checked automatically on Windows, Ubuntu and macOS, with the given input data. Nothing grades your work automatically: you check it yourself, against the criteria.

## How this test works

This lesson introduces nothing new. You check whether you can design a program on your own whose behaviour depends on several requirements and on input data: it checks the data, chooses a category, calculates only when it's allowed to, and makes a decision based on several conditions. You also diagnose two short programs with logic errors and explain your decisions.

The lesson has two parts:

- **Part A: the test.** Requirements, test data, expected results, questions and criteria. No hints and no solution code. Everything you need, you know from Modules 1–3.
- **Part B: checking and discussion.** Hints, full lists of control cases, example solutions, explanations and a self-assessment. Go there after finishing part A, or when you knowingly decide to stop trying on your own.

Looking at part B, at earlier lessons or at your notes is not a failure. What matters is **honestly noting what was done on your own and what was done with help**. You can split the test into two sessions, for example task 1 on one day and tasks 2 and 3 on the next.

**You can use:** CLion or the terminal, CMake and Ninja, as before; the `CMakeLists.txt` copied from the original `lesson_05_first_program`; a table of cases and temporary `std::cout` statements; the debugger from lesson 2.3, if it works in your environment.

In all tasks we assume that the user types data in the correct form: text where the program asks for text, and numbers where it asks for numbers. The **values** of the numbers, however, may not meet the task's requirements, and checking them is the program's job.

---

# Part A: the test

## Task 1: A science show

The organisers are preparing a science show. The program helps them assess the event plan.

**Setup:** in `cpp-workspace`, create a `science_show` folder, copy `CMakeLists.txt` into it from the original `lesson_05_first_program`, create an **empty** `main.cpp` and write the whole program on your own. Don't copy programs from earlier lessons.

**Input data**, in this order, each value on its own line:

1. the event name: a whole line of text, which may contain spaces;
2. the duration in hours: a number with a fractional part;
3. the participant count: a whole number.

**Data requirements.** The data is acceptable when:

- the duration is greater than zero;
- the participant count is at least 1 and doesn't exceed 30.

If any requirement isn't met, the program prints only `Invalid event data` after the prompts and does nothing more. It doesn't ask for the data again.

**For acceptable data** the program prints a report:

1. `Event: ` and the event name;
2. the duration category:

   | Duration | Category |
   |---|---|
   | up to 1.5 hours inclusive | `Short` |
   | over 1.5, up to 3 hours inclusive | `Standard` |
   | over 3 hours | `Extended` |

3. the number of **full** groups of 6 participants and the number of participants left outside the full groups (for 19 people: 3 full groups and 1 person);
4. whether an extra helper is needed. One is needed when **at least one** of these conditions holds: the duration exceeds 3 hours **or** there are more than 18 participants. The program then prints `Extra helper: Yes`, and otherwise `Extra helper: No`.

**The first example:**

<!-- input: science_show -->
```text
Night Sky Show
1.5
12
```

Standard output must be exactly:

<!-- output: science_show -->
```text
Enter event name:
Enter duration in hours:
Enter participant count:
Event: Night Sky Show
Duration category: Short
Full groups: 2
Remaining participants: 0
Extra helper: No
```

**The second example:**

<!-- input: science_show -->
```text
Robotics Demo
2.5
19
```

<!-- output: science_show -->
```text
Enter event name:
Enter duration in hours:
Enter participant count:
Event: Robotics Demo
Duration category: Standard
Full groups: 3
Remaining participants: 1
Extra helper: Yes
```

**The third example, data that doesn't meet the requirements:**

<!-- input: science_show -->
```text
Chemistry Fair
2.0
31
```

<!-- output: science_show -->
```text
Enter event name:
Enter duration in hours:
Enter participant count:
Invalid event data
```

**Before you run the program, prepare a table of test cases.** It must check at least:

- both duration category boundaries (1.5 and 3), exactly on the boundary and just above it;
- the smallest and the largest acceptable participant count, and the counts just outside the range;
- the 18-participant boundary for the extra helper, exactly on it and just above it;
- all four combinations of the extra helper conditions: neither, only the duration, only the participant count, both;
- a duration of zero and a negative duration;
- a division into groups with a remainder and without one.

Write down the expected result for each case. Then run the program for all of them and compare.

On the screen you'll also see the typed data between the program's lines: that's the echo, not standard output (lesson 2.6). You can also type the duration 2.0 as `2`.

When the result matches, you can save the project in Git, as in lesson 1.5. Before committing, check `git status`: only `main.cpp` and `CMakeLists.txt` go into the history.

## Task 2: Two bug reports

In `cpp-workspace`, create a `diagnosis_3` folder and copy `main.cpp` and `CMakeLists.txt` into it from the original `lesson_05_first_program`. Type each of the programs below in turn into that folder's `main.cpp`. Both build and run, but they give wrong results.

**Report A.** A courier company classifies parcels by weight in kilograms (a whole number, at least 1):

| Weight | Size |
|---|---|
| up to 5 kg inclusive | `Small` |
| from 6 to 20 kg | `Medium` |
| over 20 kg | `Large` |

<!-- example: parcel_size_bug -->
```cpp
#include <iostream>

int main() {
    int weight_kg{0};

    std::cout << "Enter parcel weight in kg:\n";
    std::cin >> weight_kg;

    if (weight_kg <= 20) {
        std::cout << "Size: Medium\n";
    } else if (weight_kg <= 5) {
        std::cout << "Size: Small\n";
    } else {
        std::cout << "Size: Large\n";
    }
}
```

**Report B.** The climbing wall is open to people who are **at least 140 cm tall and at least 10 years old**. Both requirements must hold at the same time.

<!-- example: climbing_bug -->
```cpp
#include <iostream>

int main() {
    int height_cm{0};
    int age{0};

    std::cout << "Enter height in cm:\n";
    std::cin >> height_cm;
    std::cout << "Enter age:\n";
    std::cin >> age;

    const bool allowed{height_cm >= 140 || age >= 10};

    if (allowed) {
        std::cout << "Climbing: allowed\n";
    } else {
        std::cout << "Climbing: not allowed\n";
    }
}
```

**For each report:**

1. Read the requirements and decide which results are correct.
2. Prepare test cases: for report A, the boundaries of all the sizes; for report B, four combinations: both requirements met, only the first, only the second, neither.
3. **Predict** what the buggy program prints for your cases.
4. Run the program and compare.
5. Find the cause: the order of the conditions or the wrong operator.
6. Fix the program with one change.
7. Check all the cases again.

Record the results in a table:

| Report | Case that reveals the bug | Actual result | Cause | Fix | Check |
|---|---|---|---|---|---|
| A | | | | | |
| B | | | | | |

You don't need to save the `diagnosis_3` project in Git.

## Task 3: Explain

Answer briefly, in writing, referring to your own program from task 1:

1. Why does the data requirements check come before the classification and the calculations?
2. Why do you use `&&` when checking the participant count?
3. Why does the extra helper decision use `||`? What happens when both of its conditions hold?
4. Why does the order of conditions in an `else if` chain matter? Show it with your category chain.
5. If `needs_extra_helper` is a `bool` variable, what does `!needs_extra_helper` mean?
6. Why is it worth checking values exactly at the boundaries? Give one boundary from task 1 where confusing `<` and `<=` would change the result.
7. Why can't you claim that your program correctly handles typing `abc` instead of a number?

## Success criteria

You pass the test when you meet **all** the criteria:

- `science_show/main.cpp` was written from an empty file, in valid C++20. The program builds without errors.
- The name is read in full with `std::getline`, **before** the numbers are read with `>>`. The duration is a `double` and the participant count an `int`, all with initial values.
- The data requirements are checked **before** the classification and the calculations. For data that doesn't meet the requirements, the program prints only `Invalid event data`.
- The categories are chosen by an `if`/`else if`/`else` chain in an order in which every branch is reachable.
- The full groups and the remaining participants are calculated with `/` and `%`. The group size is a constant.
- The extra helper decision is expressed by a readable condition with `||`. At least one condition is stored in a named `bool` variable.
- Standard output for the three examples and for all your cases matches the requirements.
- The table of cases was made before running the program and checks the boundaries listed in task 1.
- Both reports from task 2 were diagnosed and fixed, and all the cases were checked again.
- You can explain every line of your program and answer the questions from task 3.

A nested `if` is allowed, but not required. Variable names can differ from the reference solution, as long as they're readable. A correct result is a necessary condition, but **not proof of understanding**. That's why task 3 is part of the test.

---

# Part B: checking and discussion

Come here after finishing part A, or when you knowingly decide to stop trying on your own.

## How to check your work

- **Standard output:** run the program for every case in your table and compare the program's lines with the expected ones, character by character. Skip the typed data that the echo shows.
- **The same program:** don't change the code between runs.
- **Compare the full lists of control cases** below with your table. Did your table cover the same boundaries?
- **Order:** read the program from the top. Does any division or classification run before the data check?

## Hints

Each hint is about a way of thinking. Open them in order, and only when you need them.

<details>
<summary>Task 1, hint 1: where to start?</summary>

With the types and the reads: text with spaces, a number with a fractional part, a whole number. Which reading method has to come first (lesson 2.7)? Then one decision: does the data meet the requirements (lesson 3.5)?

</details>

<details>
<summary>Task 1, hint 2: categories and groups</summary>

The categories are a chain with three branches. When the thresholds say "up to … inclusive", start with the lowest threshold using `<=` (lesson 3.3). Groups of 6: "how many full ones?" and "how many are left?" (lesson 2.4). All of this runs only for acceptable data.

</details>

<details>
<summary>Task 1, hint 3: the extra helper</summary>

The requirement says "at least one of the conditions". Which operator means "or", including when both conditions hold (lesson 3.4)? Give the result a name, for example `needs_extra_helper`.

</details>

<details>
<summary>Task 2, report A</summary>

For a weight of 3 kg, which condition is checked first, and does it hold? Can the program ever reach the `Small` branch?

</details>

<details>
<summary>Task 2, report B</summary>

The requirement says both conditions must hold at the same time. Which of the four combinations will reveal that the program accepts people who meet only one condition?

</details>

## The full list of control cases: task 1

<details>
<summary>Open after preparing your own table</summary>

The first three cases are checked in part A.

| Name | Duration | Participants | Category | Groups | Left | Helper | What it checks |
|---|---|---|---|---|---|---|---|
| Night Sky Show | 1.5 | 12 | `Short` | 2 | 0 | `No` | the 1.5 boundary, a division without a remainder, no helper condition |
| Robotics Demo | 2.5 | 19 | `Standard` | 3 | 1 | `Yes` | helper only because of the participants (19) |
| Chemistry Fair | 2.0 | 31 | — | — | — | — | 31 participants: out of range |
| Volcano Lab | 3.5 | 12 | `Extended` | 2 | 0 | `Yes` | helper only because of the duration |
| Star Party Marathon | 3.5 | 24 | `Extended` | 4 | 0 | `Yes` | both helper conditions |
| Magnet Workshop | 3.0 | 18 | `Standard` | 3 | 0 | `No` | the 3.0 boundary and the 18 boundary |
| Crystal Club | 1.75 | 6 | `Standard` | 1 | 0 | `No` | just above the 1.5 boundary |
| Tiny Bugs Tour | 1.25 | 1 | `Short` | 0 | 1 | `No` | the smallest participant count, no full group |
| Big Science Day | 2.0 | 30 | `Standard` | 5 | 0 | `Yes` | the largest participant count |
| Zero Hour Talk | 0 | 12 | — | — | — | — | a duration of zero |
| Time Machine Show | -1.5 | 10 | — | — | — | — | a negative duration |
| Empty Room Demo | 2.0 | 0 | — | — | — | — | zero participants |

The cases with dashes end with the line `Invalid event data`.

<!-- input: science_show -->
```text
Volcano Lab
3.5
12
```

<!-- output: science_show -->
```text
Enter event name:
Enter duration in hours:
Enter participant count:
Event: Volcano Lab
Duration category: Extended
Full groups: 2
Remaining participants: 0
Extra helper: Yes
```

<!-- input: science_show -->
```text
Star Party Marathon
3.5
24
```

<!-- output: science_show -->
```text
Enter event name:
Enter duration in hours:
Enter participant count:
Event: Star Party Marathon
Duration category: Extended
Full groups: 4
Remaining participants: 0
Extra helper: Yes
```

<!-- input: science_show -->
```text
Magnet Workshop
3.0
18
```

<!-- output: science_show -->
```text
Enter event name:
Enter duration in hours:
Enter participant count:
Event: Magnet Workshop
Duration category: Standard
Full groups: 3
Remaining participants: 0
Extra helper: No
```

<!-- input: science_show -->
```text
Crystal Club
1.75
6
```

<!-- output: science_show -->
```text
Enter event name:
Enter duration in hours:
Enter participant count:
Event: Crystal Club
Duration category: Standard
Full groups: 1
Remaining participants: 0
Extra helper: No
```

<!-- input: science_show -->
```text
Tiny Bugs Tour
1.25
1
```

<!-- output: science_show -->
```text
Enter event name:
Enter duration in hours:
Enter participant count:
Event: Tiny Bugs Tour
Duration category: Short
Full groups: 0
Remaining participants: 1
Extra helper: No
```

<!-- input: science_show -->
```text
Big Science Day
2.0
30
```

<!-- output: science_show -->
```text
Enter event name:
Enter duration in hours:
Enter participant count:
Event: Big Science Day
Duration category: Standard
Full groups: 5
Remaining participants: 0
Extra helper: Yes
```

<!-- input: science_show -->
```text
Zero Hour Talk
0
12
```

<!-- output: science_show -->
```text
Enter event name:
Enter duration in hours:
Enter participant count:
Invalid event data
```

<!-- input: science_show -->
```text
Time Machine Show
-1.5
10
```

<!-- output: science_show -->
```text
Enter event name:
Enter duration in hours:
Enter participant count:
Invalid event data
```

<!-- input: science_show -->
```text
Empty Room Demo
2.0
0
```

<!-- output: science_show -->
```text
Enter event name:
Enter duration in hours:
Enter participant count:
Invalid event data
```

</details>

## Example solutions

<details>
<summary>Task 1: the science show</summary>

<!-- example: science_show -->
```cpp
#include <iostream>
#include <string>

int main() {
    const int group_size{6};

    std::string event_name{""};
    double duration_hours{0.0};
    int participants{0};

    std::cout << "Enter event name:\n";
    std::getline(std::cin, event_name);
    std::cout << "Enter duration in hours:\n";
    std::cin >> duration_hours;
    std::cout << "Enter participant count:\n";
    std::cin >> participants;

    const bool valid_data{duration_hours > 0.0 && participants >= 1 && participants <= 30};

    if (valid_data) {
        std::cout << "Event: " << event_name << "\n";

        if (duration_hours <= 1.5) {
            std::cout << "Duration category: Short\n";
        } else if (duration_hours <= 3.0) {
            std::cout << "Duration category: Standard\n";
        } else {
            std::cout << "Duration category: Extended\n";
        }

        const int full_groups{participants / group_size};
        const int remaining_participants{participants % group_size};
        std::cout << "Full groups: " << full_groups << "\n";
        std::cout << "Remaining participants: " << remaining_participants << "\n";

        const bool needs_extra_helper{duration_hours > 3.0 || participants > 18};
        if (needs_extra_helper) {
            std::cout << "Extra helper: Yes\n";
        } else {
            std::cout << "Extra helper: No\n";
        }
    } else {
        std::cout << "Invalid event data\n";
    }
}
```

- **The check first:** `valid_data` combines three requirements with `&&`, because all of them must hold. The classification, the division and the helper decision are in the branch for acceptable data. For data that doesn't meet the requirements, the program calculates nothing.
- **The categories:** the "up to … inclusive" thresholds go from the lowest, with `<=`. The program reaches `else if (duration_hours <= 3.0)` only when the duration exceeds 1.5, so that branch handles exactly the range from 1.5 (exclusive) to 3.0 (inclusive).
- **The groups:** `/` gives the full groups, `%` the participants outside them. The divisor is the constant 6, so there's no risk of dividing by zero.
- **The helper:** `||`, because one condition is enough, also when both hold. The boundaries 3.0 and 18 don't give a helper, because the requirement says "exceeds".
- The category chain and the helper decision are inside the `if (valid_data)` branch, one level deeper. That's allowed nesting. Other readable layouts that give the same result are correct too.

</details>

<details>
<summary>Task 2, report A: the result before the fix, and the fixed program</summary>

Before the fix:

<!-- input: parcel_size_bug -->
```text
3
```

<!-- output: parcel_size_bug -->
```text
Enter parcel weight in kg:
Size: Medium
```

<!-- input: parcel_size_bug -->
```text
12
```

<!-- output: parcel_size_bug -->
```text
Enter parcel weight in kg:
Size: Medium
```

<!-- input: parcel_size_bug -->
```text
25
```

<!-- output: parcel_size_bug -->
```text
Enter parcel weight in kg:
Size: Large
```

- **The case that reveals the bug:** any weight up to 5 kg; for example, 3 kg gives `Medium` instead of `Small`.
- **The cause:** `weight_kg <= 20` comes first and also catches every weight up to 5 kg, so the `Small` branch is unreachable. Each condition on its own is correct; the order is wrong.
- **The fix:** swap the first two conditions:

<!-- example: parcel_size_fixed -->
```cpp
#include <iostream>

int main() {
    int weight_kg{0};

    std::cout << "Enter parcel weight in kg:\n";
    std::cin >> weight_kg;

    if (weight_kg <= 5) {
        std::cout << "Size: Small\n";
    } else if (weight_kg <= 20) {
        std::cout << "Size: Medium\n";
    } else {
        std::cout << "Size: Large\n";
    }
}
```

The boundaries after the fix:

<!-- input: parcel_size_fixed -->
```text
5
```

<!-- output: parcel_size_fixed -->
```text
Enter parcel weight in kg:
Size: Small
```

<!-- input: parcel_size_fixed -->
```text
6
```

<!-- output: parcel_size_fixed -->
```text
Enter parcel weight in kg:
Size: Medium
```

<!-- input: parcel_size_fixed -->
```text
20
```

<!-- output: parcel_size_fixed -->
```text
Enter parcel weight in kg:
Size: Medium
```

<!-- input: parcel_size_fixed -->
```text
21
```

<!-- output: parcel_size_fixed -->
```text
Enter parcel weight in kg:
Size: Large
```

</details>

<details>
<summary>Task 2, report B: the result before the fix, and the fixed program</summary>

Before the fix, for the four combinations (height, age):

<!-- input: climbing_bug -->
```text
150
12
```

<!-- output: climbing_bug -->
```text
Enter height in cm:
Enter age:
Climbing: allowed
```

<!-- input: climbing_bug -->
```text
150
8
```

<!-- output: climbing_bug -->
```text
Enter height in cm:
Enter age:
Climbing: allowed
```

<!-- input: climbing_bug -->
```text
130
12
```

<!-- output: climbing_bug -->
```text
Enter height in cm:
Enter age:
Climbing: allowed
```

<!-- input: climbing_bug -->
```text
130
8
```

<!-- output: climbing_bug -->
```text
Enter height in cm:
Enter age:
Climbing: not allowed
```

- **The cases that reveal the bug:** 150 cm and 8 years, and 130 cm and 12 years. Each meets only one requirement, and the program lets them in.
- **The cause:** `||` is true when even one condition holds. The requirement says "both at the same time", that is, "and".
- **The fix:** `&&` instead of `||`:

<!-- example: climbing_fixed -->
```cpp
#include <iostream>

int main() {
    int height_cm{0};
    int age{0};

    std::cout << "Enter height in cm:\n";
    std::cin >> height_cm;
    std::cout << "Enter age:\n";
    std::cin >> age;

    const bool allowed{height_cm >= 140 && age >= 10};

    if (allowed) {
        std::cout << "Climbing: allowed\n";
    } else {
        std::cout << "Climbing: not allowed\n";
    }
}
```

After the fix, the same four combinations:

<!-- input: climbing_fixed -->
```text
150
12
```

<!-- output: climbing_fixed -->
```text
Enter height in cm:
Enter age:
Climbing: allowed
```

<!-- input: climbing_fixed -->
```text
150
8
```

<!-- output: climbing_fixed -->
```text
Enter height in cm:
Enter age:
Climbing: not allowed
```

<!-- input: climbing_fixed -->
```text
130
12
```

<!-- output: climbing_fixed -->
```text
Enter height in cm:
Enter age:
Climbing: not allowed
```

<!-- input: climbing_fixed -->
```text
130
8
```

<!-- output: climbing_fixed -->
```text
Enter height in cm:
Enter age:
Climbing: not allowed
```

The "both met" and "neither" cases give the same result before and after the fix. That's why testing only those wouldn't reveal the bug: you need cases in which only one requirement holds.

</details>

## Example answers to task 3

<details>
<summary>Show the example answers</summary>

1. Because the calculations and the classification only make sense for acceptable data. When the data doesn't meet the requirements, the program prints `Invalid event data` and calculates nothing.
2. Because the participant count must meet two conditions at the same time: at least 1 **and** at most 30. A range is written as two comparisons joined by `&&`.
3. Because one of the conditions is enough. `||` is also true when both conditions hold, so in that case it's `Extra helper: Yes` too.
4. Because the program runs the branch of the first condition that holds. If `duration_hours <= 3.0` came before `duration_hours <= 1.5`, a duration of 1.25 would get `Standard`, and the `Short` branch would be unreachable.
5. "No extra helper is needed": `!needs_extra_helper` is `true` when `needs_extra_helper` is `false`, and the other way round. The variable itself doesn't change.
6. Because confusing `<` with `<=` (or `>` with `>=`) changes the result only exactly at the boundary. For example, for 18 participants: the requirement "more than 18" is `> 18`. With `>= 18`, the program would ask for a helper for 18 people.
7. Because the program only checks values that were read successfully. Typing `abc` is a failed read, and the program doesn't detect that. You'll learn to handle such situations later.

</details>

## Self-assessment

For each criterion, mark one answer:

| Criterion | On my own | With a hint | After looking at the solution | To revise |
|---|---|---|---|---|
| Writing the program from an empty `main.cpp` | | | | |
| Reading the name with `std::getline` and the numbers with `>>` | | | | |
| Checking the data requirements before the calculations | | | | |
| The category chain in the correct order | | | | |
| Full groups and the remainder with `/` and `%` | | | | |
| The helper decision with `\|\|` and a `bool` variable | | | | |
| A table of cases with boundaries before running | | | | |
| Diagnosing report A (`else if` order) | | | | |
| Diagnosing report B (`&&` versus `\|\|`) | | | | |
| Finding bugs with a table of cases and `std::cout` | | | | |
| Using the debugger in CLion | | | | |
| The explanations from task 3 | | | | |

The debugger row is about a **tool**, and the table of cases row is about a **bug-finding technique**. The two skills complement each other, but don't replace each other. If the debugger doesn't work in your environment, leave its row empty.

If anything is marked in the "To revise" column, go back to the matching lesson:

| Topic | Lesson |
|---|---|
| the first condition, comparisons and boundaries | 3.1 |
| `else`, `bool`, equality and variable scope | 3.2 |
| `else if` and the order of conditions | 3.3 |
| `&&`, `\|\|`, `!` and short-circuit evaluation | 3.4 |
| checking data before calculating | 3.5 |
| `std::getline` and text | 2.7 |
| `double` and mixing types | 2.5 |
| `/`, `%` and integer division | 2.4 |

Then try the task again, for example with different category thresholds.

---

## Module 3 summary

After six lessons, you can:

- write programs that choose different actions depending on the data;
- write comparisons and store their results in `bool` variables;
- build `if` and `else` statements and `else if` chains in the correct order;
- combine conditions with `&&` and `||`, and invert them with `!`;
- understand the short-circuit evaluation of `&&` and `||`;
- plan test cases and check values exactly at the boundaries;
- find bugs in the order of conditions and in the choice of operators;
- check data before calculating, and skip a calculation when the requirements aren't met;
- tell a value that doesn't meet the requirements apart from a failed read.

Your programs already react to wrong values, but they can't yet ask again or handle a failed read. That will come together with repeating actions.

## What's next: Module 4

Your programs can already **choose** an action. In Module 4, "Repeating actions", they'll learn to perform actions **many times**. Start with the first loop: [Lesson 4.1: The first loop (`while`)](../module_04_repeating_actions/lesson_01_the_first_loop.en.md).

**Previous lesson:** [Lesson 3.5: Checking data before calculating](lesson_05_check_before_calculating.en.md) · **Next lesson:** [Lesson 4.1: The first loop (`while`)](../module_04_repeating_actions/lesson_01_the_first_loop.en.md) · [Course overview](../../README.en.md)

# Lesson 4.4: Repeating until the goal is reached

[Polski](lesson_04_repeat_until_the_goal.md) · **English** · [Course overview](../../README.en.md)

> **Module 4, lesson 4** · about 70–85 minutes
> **You need:** the `cpp-workspace` folder and the original `lesson_05_first_program` project, as before. You don't need the debugger in this lesson.
> **Pilot version.** The programs in this lesson are checked automatically on Windows, Ubuntu and macOS, including with the given input data.

## Before you start

This lesson assumes that after lessons 4.1–4.3:

- you write `while` and `for` loops and trace them in a table in which the last condition check gives `false` and isn't an iteration;
- you know that a loop can run zero times;
- you build up a result in an accumulator with `+=` and increase a counter with `++`;
- you check data with `if` before the program starts calculating (lesson 3.5).

## The situation

In lessons 4.1–4.3 a counter decided the number of repetitions: "print 3 laps", "add up the numbers to N", "plan 5 rounds". Often, though, we think differently: **"repeat until you reach the goal"**. Put money aside until you've collected the amount you need. Read until you've read the planned number of pages.

The program then doesn't need a planned number of repetitions. After every iteration it checks **how far it is from the goal**, and decides from that whether to keep going. That's what the `while` you already know is for. Today its condition will depend on a changing state, not on a counter.

After this lesson you'll be able to:

- tell a counter-controlled loop from a loop controlled by reaching a goal;
- point out the state that the loop's condition depends on, and write the condition "repeat while the goal isn't reached";
- explain why the loop ends, and check the data before the loop starts;
- tell reaching the goal exactly from passing it, and find a bug of one iteration too many;
- recognise, without running it, a loop that makes no progress;
- write a loop in which the step changes from one iteration to the next.

## 1. Prepare the project

In `cpp-workspace`, create a `lesson_4_4` folder and copy `main.cpp` and `CMakeLists.txt` into it from the original `lesson_05_first_program`. You type the programs from sections 2–9 into that folder's `main.cpp`.

## 2. Saving towards a goal

Someone wants to collect a certain amount, paying in the same number of whole zloty each time. The program knows the goal and the amount of one payment. It repeats the payments **while the sum collected is less than the goal**. The goal can be 0 to 500 zl, and a payment 25 to 100 zl. We assume the user types whole numbers.

<!-- example: savings -->
```cpp
#include <iostream>

int main() {
    int goal{0};
    int payment{0};

    std::cout << "Enter goal in zl (0-500):\n";
    std::cin >> goal;
    std::cout << "Enter payment in zl (25-100):\n";
    std::cin >> payment;

    const bool goal_ok{goal >= 0 && goal <= 500};
    const bool payment_ok{payment >= 25 && payment <= 100};

    if (goal_ok && payment_ok) {
        int saved{0};
        int payment_count{0};

        while (saved < goal) {
            saved += payment;
            ++payment_count;
            std::cout << "Payment " << payment_count << ": saved " << saved << " zl\n";
        }

        std::cout << "Payments: " << payment_count << "\n";
        std::cout << "Saved: " << saved << " zl\n";
    } else {
        std::cout << "Invalid savings data\n";
    }
}
```

- `goal` is the **goal**: the amount we want to collect. It doesn't change in the loop.
- `payment` is the **step**: how much the sum grows in one iteration.
- `saved` is the **progress**: how much has been collected so far. It's the accumulator from lesson 4.2.
- `payment_count` counts the payments made.
- The condition `saved < goal` depends on **the sum collected**, not on the payment counter. The counter only records how many payments there were. It doesn't decide when to stop.
- After every payment, `saved` grows. When the sum reaches or passes the goal, the condition gives `false` and the loop ends.

In this example, the number of payments could be calculated in advance. That isn't the point, though. The program decides **on its own** whether to repeat, based on the current progress, and never writes down a planned number of iterations.

**Predict**, for a goal of 100 zl and payments of 30 zl: how many payments will there be, how will the sum grow, will the last payment hit the goal exactly, and what will the final amount be? Write your answers down, then run the program.

<!-- input: savings -->
```text
100
30
```

<details>
<summary>Standard output for 100 and 30</summary>

<!-- output: savings -->
```text
Enter goal in zl (0-500):
Enter payment in zl (25-100):
Payment 1: saved 30 zl
Payment 2: saved 60 zl
Payment 3: saved 90 zl
Payment 4: saved 120 zl
Payments: 4
Saved: 120 zl
```

</details>

## 3. The progress table

The table for a goal of 100 zl and payments of 30 zl:

| Condition check | `saved` at the check | `saved < goal` | Payment in the body | `saved` after the payment | `payment_count` after the payment |
|---|---|---|---|---|---|
| 1 | 0 | `true` | 30 | 30 | 1 |
| 2 | 30 | `true` | 30 | 60 | 2 |
| 3 | 60 | `true` | 30 | 90 | 3 |
| 4 | 90 | `true` | 30 | 120 | 4 |
| 5 | 120 | `false` | **none**: the loop ends | — | — |

- The condition was checked **5 times**, and there were **4** payments. The fifth check gives `false` and isn't an iteration.
- At 90 zl, 10 zl are still missing, so the program makes another **full** payment. The sum passes the goal by 20 zl. That's fine: we always pay in the same amount, and the program doesn't calculate a partial payment. It's an exercise in repeating until a condition is met, not a banking system.

## 4. Goal, progress and step

| Idea | What it is | In the example |
|---|---|---|
| **goal** | the state we want to reach | `goal` |
| **progress** | the value that changes in successive iterations and is compared with the goal | `saved` |
| **step** | how much the progress changes in one iteration | `payment` |

These aren't new C++ types, just names that help you understand the loop. In this example the step is **constant**: every payment is the same. In the mission at the end of the lesson, the step will change. In both cases the loop ends once the goal is reached.

## 5. Hitting the goal exactly

Now the goal is 100 zl and the payment is 25 zl. **Predict**: how many payments will there be, and what will the sum be? After the payment that makes exactly 100 zl, is one more needed?

<!-- input: savings -->
```text
100
25
```

<details>
<summary>Standard output for 100 and 25, and explanation</summary>

<!-- output: savings -->
```text
Enter goal in zl (0-500):
Enter payment in zl (25-100):
Payment 1: saved 25 zl
Payment 2: saved 50 zl
Payment 3: saved 75 zl
Payment 4: saved 100 zl
Payments: 4
Saved: 100 zl
```

After the fourth payment the sum is exactly 100 zl. The fifth check, `100 < 100`, gives `false`, so the loop ends. **A goal that has been reached needs no extra payment.**

</details>

The condition `saved < goal` asks: **is anything still missing?** When the sum equals the goal, nothing is missing, and the program stops paying in. A condition that also gave `true` for an equal sum would lead to a payment that nobody needs. You'll find such a bug in section 9.

## 6. Zero, one and many iterations

**Predict.** Copy the table and fill it in before you run the program.

| Goal | Payment | Number of payments | Final sum |
|---|---|---|---|
| 0 | 25 | | |
| 25 | 25 | | |
| 500 | 25 | | |

Then run the program three times.

<!-- input: savings -->
```text
0
25
```

<details>
<summary>Standard output for 0 and 25</summary>

<!-- output: savings -->
```text
Enter goal in zl (0-500):
Enter payment in zl (25-100):
Payments: 0
Saved: 0 zl
```

`saved` starts at 0, and the condition `0 < 0` is false already at the first check. Nothing needs to be paid in: a goal of 0 zl is reached from the start. The loop body doesn't run even once, `payment_count` stays 0, and the summary after the loop is printed anyway. That's correct behaviour, not bad data: a goal of 0 is within the accepted range.

</details>

<!-- input: savings -->
```text
25
25
```

<details>
<summary>Standard output for 25 and 25</summary>

<!-- output: savings -->
```text
Enter goal in zl (0-500):
Enter payment in zl (25-100):
Payment 1: saved 25 zl
Payments: 1
Saved: 25 zl
```

</details>

<!-- input: savings -->
```text
500
25
```

<details>
<summary>Standard output for 500 and 25</summary>

<!-- output: savings -->
```text
Enter goal in zl (0-500):
Enter payment in zl (25-100):
Payment 1: saved 25 zl
Payment 2: saved 50 zl
Payment 3: saved 75 zl
Payment 4: saved 100 zl
Payment 5: saved 125 zl
Payment 6: saved 150 zl
Payment 7: saved 175 zl
Payment 8: saved 200 zl
Payment 9: saved 225 zl
Payment 10: saved 250 zl
Payment 11: saved 275 zl
Payment 12: saved 300 zl
Payment 13: saved 325 zl
Payment 14: saved 350 zl
Payment 15: saved 375 zl
Payment 16: saved 400 zl
Payment 17: saved 425 zl
Payment 18: saved 450 zl
Payment 19: saved 475 zl
Payment 20: saved 500 zl
Payments: 20
Saved: 500 zl
```

The largest goal and the smallest payment give the most iterations: 20.

</details>

## 7. Checking the data before the loop

The program checks both ranges **before** it enters the loop. For data outside the range, it prints only `Invalid savings data` and ends normally, without any payment.

**Predict** what the program will print for a payment of 0 zl and a goal of 100 zl, then check this and the other cases.

<!-- input: savings -->
```text
100
0
```

<details>
<summary>Standard output for 100 and 0, and for the other data outside the range</summary>

<!-- output: savings -->
```text
Enter goal in zl (0-500):
Enter payment in zl (25-100):
Invalid savings data
```

A payment of 24 zl (just below the range) and of 101 zl (just above it) end the same way, as do goals of -1 zl and 501 zl:

<!-- input: savings -->
```text
100
24
```

<!-- output: savings -->
```text
Enter goal in zl (0-500):
Enter payment in zl (25-100):
Invalid savings data
```

<!-- input: savings -->
```text
100
101
```

<!-- output: savings -->
```text
Enter goal in zl (0-500):
Enter payment in zl (25-100):
Invalid savings data
```

<!-- input: savings -->
```text
-1
50
```

<!-- output: savings -->
```text
Enter goal in zl (0-500):
Enter payment in zl (25-100):
Invalid savings data
```

<!-- input: savings -->
```text
501
50
```

<!-- output: savings -->
```text
Enter goal in zl (0-500):
Enter payment in zl (25-100):
Invalid savings data
```

</details>

**Why before the loop?** The check protects the loop itself:

- a payment of 0 zl doesn't change the sum, so for a positive goal `saved < goal` would give `true` forever;
- a negative payment moves the sum **away** from a positive goal;
- in both cases the ending condition would never become false.

Checking inside the loop would be too late: the bad payment would already have been made. In this lesson, bad data ends the program with a message. You'll learn to ask for the data again in the next lesson.

## 8. What guarantees the ending?

For acceptable data the loop always ends, **because the sum grows by at least 25 zl in every iteration, and the goal is at most 500 zl**. After 20 payments the sum is at least 500 zl, so the condition `saved < goal` must become false by then at the latest. There's no need for a formal proof, but you should be able to answer four questions:

1. Does every iteration bring the program closer to the goal?
2. Can the goal stay out of reach all the time?
3. What has to change for the condition to become false?
4. Why do we need limits on the data?

Example answers are in [Example solutions](#example-solutions).

The range 0 to 500 zl isn't a limit of the `int` type, but **a requirement of this task**. Thanks to it, the loop has at most 20 iterations, so the output is short and easy to check.

## 9. Find the bug: one payment too many

The requirement is the same as in section 2: the program pays in **while the sum is less than the goal**. In this version, someone changed the loop's condition:

<!-- example: savings_bug -->
```cpp
#include <iostream>

int main() {
    int goal{0};
    int payment{0};

    std::cout << "Enter goal in zl (0-500):\n";
    std::cin >> goal;
    std::cout << "Enter payment in zl (25-100):\n";
    std::cin >> payment;

    const bool goal_ok{goal >= 0 && goal <= 500};
    const bool payment_ok{payment >= 25 && payment <= 100};

    if (goal_ok && payment_ok) {
        int saved{0};
        int payment_count{0};

        while (saved <= goal) {
            saved += payment;
            ++payment_count;
            std::cout << "Payment " << payment_count << ": saved " << saved << " zl\n";
        }

        std::cout << "Payments: " << payment_count << "\n";
        std::cout << "Saved: " << saved << " zl\n";
    } else {
        std::cout << "Invalid savings data\n";
    }
}
```

1. Read the requirement and write down how many payments, and what sum, the program **should** give for three pairs: goal 0 and payment 25, goal 100 and payment 25, goal 100 and payment 30.
2. Predict what **this** program will print. A trace table for goal 0 will help.
3. Run the program for these three pairs.
4. Find the first case where the result doesn't match the requirement.
5. Fix the condition.
6. Check all three cases again.

The results before the fix, and the fix, are in [Example solutions](#example-solutions). Look there after your own attempt.

## 10. A loop that makes no progress

**Analyse this fragment on paper; don't run it.** Someone mixed up the variables, and the body increases the goal instead of the sum:

<!-- fragment -->
```cpp
int saved{0};
int payment_count{0};

while (saved < goal) {
    goal += payment;
    ++payment_count;
    std::cout << "Payment " << payment_count << ": saved " << saved << " zl\n";
}
```

For a goal of 100 zl and payments of 30 zl:

| Condition check | `saved` | `goal` | `saved < goal` | After the body: `goal` | After the body: `payment_count` |
|---|---|---|---|---|---|
| 1 | 0 | 100 | `true` | 130 | 1 |
| 2 | 0 | 130 | `true` | 160 | 2 |
| 3 | 0 | 160 | `true` | 190 | 3 |
| … | 0 | … | `true` | keeps growing | keeps growing |

Something does change in this loop, in every iteration: `goal` grows, and `payment_count` grows. But the condition compares `saved` with `goal`, and `saved` stands still while the goal runs away. The answer "no" never comes, and the program would keep printing lines forever.

**It isn't enough that something changes in the loop. What changes must be the thing that actually leads to the end of the repetition:** here, the progress `saved`, towards the goal.

If such a loop ever starts by mistake, stop the program as in lesson 4.1: <kbd>Ctrl</kbd> + <kbd>C</kbd> in the terminal, or the **Stop** button in CLion.

## 11. Mission: a reading goal

The program simulates a reading plan. The user gives the goal, i.e. the total number of pages to read, and the number of pages for the first day. In this simplified simulation, each following day you read **twice as many** pages as the day before. The program simulates day after day until the total number of pages read reaches or passes the goal. It's a simple model for practice, not advice on how to read.

**Requirements:**

- The goal is a whole number from 0 to 100 pages.
- The number of pages for the first day is a whole number from 1 to 10.
- The program asks for both values, in this order: `Enter page goal (0-100):` and `Enter pages for day 1 (1-10):`.
- For each day the program prints a line `Day D: read P, total T`: the day number, the pages read that day, and the total number of pages read.
- After the last day it prints `Days: D` and `Total pages: T`.
- For a goal of 0 the program simulates no day.
- If either value is outside its range, the program prints only `Invalid reading data`. It doesn't ask for the data again.
- We assume the user types whole numbers.

In `cpp-workspace`, create a `reading_goal` folder, copy `CMakeLists.txt` into it from the original `lesson_05_first_program`, create an empty `main.cpp` and write the program on your own.

For a goal of 20 pages and 3 pages on the first day, standard output must be:

<!-- input: reading_goal -->
```text
20
3
```

<!-- output: reading_goal -->
```text
Enter page goal (0-100):
Enter pages for day 1 (1-10):
Day 1: read 3, total 3
Day 2: read 6, total 9
Day 3: read 12, total 21
Days: 3
Total pages: 21
```

**This isn't the savings program with new names.** There the step was constant: every payment was the same. Here **the step changes after every iteration**: the number of pages on a given day is twice the previous day's. The number of days follows from the progress made. You have to decide on your own:

1. which variable holds the total progress, and which the number of pages for the current day;
2. what start value the day counter has, and what the `while` condition checks;
3. in what order, within one iteration, to add the day's pages to the sum, print the day's line, and double the number of pages for the next day;
4. how to avoid an extra day after the goal is reached, and what the program does for a goal of 0.

Doubling needs only the multiplication you know (lesson 2.4). No new operator is needed.

**Before you write the program**, prepare two things:

- a trace table for a goal of 20 and 3 pages: the day number, the pages that day, the sum after that day, and the pages for the next day;
- a table of test cases: goal 0, a goal reached after one day, a goal reached exactly, a goal passed, the largest goal with the smallest start, and the values just outside the range of both inputs. Write down the expected standard output for each case.

### Success criteria

- The program builds as C++20, and its standard output for a goal of 20 and 3 pages is exactly as above.
- For every acceptable pair of values, the program prints the right days and stops after the first day on which the sum reached or passed the goal. For data outside the range it prints only `Invalid reading data`.
- The repetition is controlled by a `while` loop whose condition compares the progress with the goal.
- The total number of pages is built up in an accumulator, and the number of pages per day doubles after each day.
- The range of both values is checked before the program starts simulating days.
- The trace table and the table of cases were made before running the program.
- You can explain why the loop ends, and why for a goal of 0 there is no day.

When the result matches, you can save the project in Git, as in lesson 1.5.

<details>
<summary>Hint 1</summary>

Work out the three ideas from section 4 for this mission: what is the goal, what is the progress, and what is the step? Which of them change from day to day, and how?

</details>

<details>
<summary>Hint 2</summary>

The day's line should show **that** day's pages and the sum **after** that day. So what has to happen before printing, and what only after it, so that the next day gets twice the pages?

</details>

<details>
<summary>Hint 3</summary>

The `while` condition answers the question: is the total read still less than the goal? Check it in a trace table for a goal of 3 and 1 page: after how many days should it give `false`?

</details>

<details>
<summary>The full list of control cases: open after preparing your own table</summary>

| Goal | First day | Pages on successive days | Days | Total pages | What it checks |
|---|---|---|---|---|---|
| 20 | 3 | 3, 6, 12 | 3 | 21 | the goal passed on the last day |
| 0 | 3 | — | 0 | 0 | zero iterations |
| 1 | 1 | 1 | 1 | 1 | one day, the goal reached exactly |
| 3 | 1 | 1, 2 | 2 | 3 | the goal reached exactly after two days |
| 10 | 2 | 2, 4, 8 | 3 | 14 | the goal passed |
| 10 | 10 | 10 | 1 | 10 | one day, the goal reached exactly |
| 100 | 1 | 1, 2, 4, 8, 16, 32, 64 | 7 | 127 | the largest goal and the smallest start: the most days |
| -1 | 3 | — | — | — | the goal just below the range |
| 101 | 3 | — | — | — | the goal just above the range |
| 20 | 0 | — | — | — | the first day just below the range |
| 20 | 11 | — | — | — | the first day just above the range |

The cases with a dash in the "Days" column end with the line `Invalid reading data`. The case with a goal of 20 and 3 pages is checked above, in the mission's description.

<!-- input: reading_goal -->
```text
0
3
```

<!-- output: reading_goal -->
```text
Enter page goal (0-100):
Enter pages for day 1 (1-10):
Days: 0
Total pages: 0
```

<!-- input: reading_goal -->
```text
1
1
```

<!-- output: reading_goal -->
```text
Enter page goal (0-100):
Enter pages for day 1 (1-10):
Day 1: read 1, total 1
Days: 1
Total pages: 1
```

<!-- input: reading_goal -->
```text
3
1
```

<!-- output: reading_goal -->
```text
Enter page goal (0-100):
Enter pages for day 1 (1-10):
Day 1: read 1, total 1
Day 2: read 2, total 3
Days: 2
Total pages: 3
```

<!-- input: reading_goal -->
```text
10
2
```

<!-- output: reading_goal -->
```text
Enter page goal (0-100):
Enter pages for day 1 (1-10):
Day 1: read 2, total 2
Day 2: read 4, total 6
Day 3: read 8, total 14
Days: 3
Total pages: 14
```

<!-- input: reading_goal -->
```text
10
10
```

<!-- output: reading_goal -->
```text
Enter page goal (0-100):
Enter pages for day 1 (1-10):
Day 1: read 10, total 10
Days: 1
Total pages: 10
```

<!-- input: reading_goal -->
```text
100
1
```

<!-- output: reading_goal -->
```text
Enter page goal (0-100):
Enter pages for day 1 (1-10):
Day 1: read 1, total 1
Day 2: read 2, total 3
Day 3: read 4, total 7
Day 4: read 8, total 15
Day 5: read 16, total 31
Day 6: read 32, total 63
Day 7: read 64, total 127
Days: 7
Total pages: 127
```

<!-- input: reading_goal -->
```text
-1
3
```

<!-- output: reading_goal -->
```text
Enter page goal (0-100):
Enter pages for day 1 (1-10):
Invalid reading data
```

<!-- input: reading_goal -->
```text
101
3
```

<!-- output: reading_goal -->
```text
Enter page goal (0-100):
Enter pages for day 1 (1-10):
Invalid reading data
```

<!-- input: reading_goal -->
```text
20
0
```

<!-- output: reading_goal -->
```text
Enter page goal (0-100):
Enter pages for day 1 (1-10):
Invalid reading data
```

<!-- input: reading_goal -->
```text
20
11
```

<!-- output: reading_goal -->
```text
Enter page goal (0-100):
Enter pages for day 1 (1-10):
Invalid reading data
```

</details>

An example solution is in [Example solutions](#example-solutions).

## 12. When something goes differently

| What you see | What it means | What to do |
|---|---|---|
| After the goal is reached, there's one more iteration | The condition also gives `true` when the progress equals the goal, for example `<=` instead of `<`. | Check the case in which the goal is reached exactly (section 9). |
| For a goal of 0, one iteration appears | The same bug: the condition doesn't rule out equality. | Put the start values into the condition and check that it gives `false`. |
| The same line, or growing numbers, appear forever | The loop makes no progress: the wrong variable changes, or the step is zero. | Stop the program. In a trace table, check whether the variable in the condition moves towards the goal (section 10). |
| The first day shows twice the number of pages | The step is doubled before printing and adding to the sum. | Fix the order in the body: first the current day, then preparing the next one. |
| The sum is too small or too large | The wrong value goes into the sum, or the accumulator is reset in the body. | Check in a trace table that the sum after each day is the sum of the pages printed so far. |
| For bad data the program starts iterating | The range check is after the loop, or inside it. | Check the data with `if` before the program enters the loop. |

## 13. Explain

Answer briefly, preferably in writing. Only then compare with the example answer.

**1.** How does a counter-controlled loop differ from a loop controlled by reaching a goal?

<details>
<summary>Example answer</summary>

In a counter loop, the condition asks whether the counter has reached the planned number of repetitions. In a goal loop, the condition asks whether the progress, for example the sum collected, has already reached the goal. The number of iterations then follows from how fast the progress grows.

</details>

**2.** Which variable does the condition in the savings program depend on, and why not `payment_count`?

<details>
<summary>Example answer</summary>

On `saved`, the sum collected. The goal is about an amount, not about a number of payments. `payment_count` only records how many payments there were.

</details>

**3.** Why is there no payment for a goal of 0, and why is that correct?

<details>
<summary>Example answer</summary>

Because `saved` starts at 0, and the condition `0 < 0` is false straight away. A goal of 0 zl is reached before anything is paid in, so no payment is needed.

</details>

**4.** How does reaching the goal exactly differ from passing it? How many iterations are needed in each case?

<details>
<summary>Example answer</summary>

When the goal is reached exactly, the last iteration gives a sum equal to the goal, for example 4 payments of 25 zl make 100 zl. When it's passed, the last iteration gives more than the goal, for example 4 payments of 30 zl make 120 zl. In both cases the loop ends right after the iteration that made the sum at least equal to the goal. An extra iteration is never needed.

</details>

**5.** Why didn't the case 100 zl and 30 zl reveal the bug in section 9?

<details>
<summary>Example answer</summary>

Because the sum never equals the goal: after 90 zl it jumps straight to 120 zl. `<` and `<=` differ only when the progress is exactly equal to the goal. Such a case is revealed by goal 0 and goal 100 with payments of 25 zl.

</details>

**6.** Why might the program in section 10 never end, although something changes in every iteration?

<details>
<summary>Example answer</summary>

Because the goal changes, not the progress. `saved` stays 0 while `goal` grows, so `saved < goal` always gives `true`. Updating some variable doesn't guarantee the end. The progress has to move towards the goal.

</details>

**7.** Why does the reading mission end after at most 7 days?

<details>
<summary>Example answer</summary>

Because on the first day you read at least 1 page, and on each following day twice as many. Even with the smallest start, the sum after 7 days is 1 + 2 + 4 + 8 + 16 + 32 + 64 = 127, which is more than the largest goal, 100 pages. A larger start ends the loop even sooner.

</details>

## Summary

- A loop can keep going **while the goal isn't reached**. The condition then compares a changing progress with the goal, and the number of iterations follows from the progress.
- The **goal** is the state we want to reach, the **progress** is the value that changes in successive iterations, and the **step** is the change of the progress in one iteration. The step can be constant, or change from one iteration to the next.
- The condition `progress < goal` asks whether anything is still missing. A goal that has been reached needs no extra iteration. A goal reached from the start means zero iterations.
- The last iteration can hit the goal exactly or pass it. Both cases must be checked, because only the exact hit reveals the `<=` bug.
- A loop ends only if every iteration brings the progress closer to the goal. Check data that would prevent that, such as a payment of 0 zl, **before** the loop.
- It isn't enough that something changes in the loop. What changes must be the thing the condition depends on, and towards the goal.

## What's next

So far, bad data ended the program with a message. In lesson 4.5, the loop will repeat a question **until the user gives an acceptable value**: the goal will then be a valid answer: [Lesson 4.5: Asking again for a valid value](lesson_05_ask_again.en.md).

---

## Example solutions

Look here **after your own attempt**. Your names may differ, as long as the standard output is as required.

<details>
<summary>Section 6: the prediction table</summary>

| Goal | Payment | Number of payments | Final sum |
|---|---|---|---|
| 0 | 25 | 0 | 0 |
| 25 | 25 | 1 | 25 |
| 500 | 25 | 20 | 500 |

</details>

<details>
<summary>Section 8: four questions about the ending</summary>

1. Yes. Every payment is at least 25 zl, so the sum grows in every iteration.
2. No. The goal doesn't change and is at most 500 zl, while the sum keeps growing, so it eventually catches up.
3. The sum `saved` must reach or pass the goal. Then `saved < goal` gives `false`.
4. Without them, a payment of 0 zl or a negative one wouldn't bring the sum closer to the goal, and the loop might never end. The goal's upper limit also keeps the number of iterations at 20 or fewer.

</details>

<details>
<summary>Section 9: the results before the fix, and the fix</summary>

Before the fix:

<!-- input: savings_bug -->
```text
0
25
```

<!-- output: savings_bug -->
```text
Enter goal in zl (0-500):
Enter payment in zl (25-100):
Payment 1: saved 25 zl
Payments: 1
Saved: 25 zl
```

<!-- input: savings_bug -->
```text
100
25
```

<!-- output: savings_bug -->
```text
Enter goal in zl (0-500):
Enter payment in zl (25-100):
Payment 1: saved 25 zl
Payment 2: saved 50 zl
Payment 3: saved 75 zl
Payment 4: saved 100 zl
Payment 5: saved 125 zl
Payments: 5
Saved: 125 zl
```

<!-- input: savings_bug -->
```text
100
30
```

<!-- output: savings_bug -->
```text
Enter goal in zl (0-500):
Enter payment in zl (25-100):
Payment 1: saved 30 zl
Payment 2: saved 60 zl
Payment 3: saved 90 zl
Payment 4: saved 120 zl
Payments: 4
Saved: 120 zl
```

- **The first mismatching case** is goal 0: the requirement needs no payment, but the program makes one, because `0 <= 0` gives `true`.
- **Goal 100 with payments of 25 zl:** after four payments the sum is exactly 100 zl, and `100 <= 100` gives `true`. The program makes a fifth, unnecessary payment.
- **Goal 100 with payments of 30 zl** gives the same result as the correct program, because the sum jumps from 90 zl straight to 120 zl and never equals the goal. **Not every set of data reveals the bug:** this one is revealed only by cases in which the progress hits the goal exactly.
- **The fix:** `while (saved < goal)`. The fixed program is the one from section 2. Its results for these three pairs are checked in sections 2, 5 and 6.

</details>

<details>
<summary>Section 11: the mission, a reading goal</summary>

<!-- example: reading_goal -->
```cpp
#include <iostream>

int main() {
    int page_goal{0};
    int first_day_pages{0};

    std::cout << "Enter page goal (0-100):\n";
    std::cin >> page_goal;
    std::cout << "Enter pages for day 1 (1-10):\n";
    std::cin >> first_day_pages;

    const bool goal_ok{page_goal >= 0 && page_goal <= 100};
    const bool pages_ok{first_day_pages >= 1 && first_day_pages <= 10};

    if (goal_ok && pages_ok) {
        int total_pages{0};
        int pages_today{first_day_pages};
        int day{0};

        while (total_pages < page_goal) {
            ++day;
            total_pages += pages_today;
            std::cout << "Day " << day << ": read " << pages_today << ", total " << total_pages << "\n";
            pages_today = pages_today * 2;
        }

        std::cout << "Days: " << day << "\n";
        std::cout << "Total pages: " << total_pages << "\n";
    } else {
        std::cout << "Invalid reading data\n";
    }
}
```

| Condition check | `total_pages` at the check | `total_pages < 20` | Day | Pages that day | `total_pages` after the day | Pages for the next day |
|---|---|---|---|---|---|---|
| 1 | 0 | `true` | 1 | 3 | 3 | 6 |
| 2 | 3 | `true` | 2 | 6 | 9 | 12 |
| 3 | 9 | `true` | 3 | 12 | 21 | 24 |
| 4 | 21 | `false` | — | — | — | — |

- **Goal, progress and step:** `page_goal` doesn't change. `total_pages` is the progress and the accumulator. `pages_today` is the step, which doubles after every day.
- **The order in the body:** the day number, adding the day's pages to the sum, printing the line, and only at the end doubling the pages for the next day. That way the first day shows the number the user gave.
- **The day counter** starts at 0 and grows at the start of every iteration, so after the loop it equals the number of days. For a goal of 0 it stays 0.
- **The ending and safety:** the step is at least 1 page and grows every day, so the sum grows in every iteration, and for a goal of at most 100 pages the loop ends after 7 days at the latest. For all acceptable data, the largest number of pages on one day is 96 (goal 100, start 6: 6, 12, 24, 48, 96), and the largest sum is 189 (goal 100, start 3), so all the values fit in an `int` with a huge margin.
- After the last day, `pages_today` already holds the value for a day that won't happen. That does no harm, because the program doesn't print it.

</details>

**Previous lesson:** [Lesson 4.3: The `for` loop: counter, condition and update in one place](lesson_03_the_for_loop.en.md) · **Next lesson:** [Lesson 4.5: Asking again for a valid value](lesson_05_ask_again.en.md) · [Course overview](../../README.en.md)

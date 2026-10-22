# Lesson 4.3: The `for` loop: counter, condition and update in one place

[Polski](lesson_03_the_for_loop.md) · **English** · [Course overview](../../README.en.md)

> **Module 4, lesson 3** · about 70–85 minutes
> **You need:** the `cpp-workspace` folder and the original `lesson_05_first_program` project, as before. You don't need the debugger in this lesson.
> **Pilot version.** The programs in this lesson are checked automatically on Windows, Ubuntu and macOS, including with the given input data.

## Before you start

This lesson assumes that after lessons 4.1 and 4.2:

- you write a `while` loop with a counter and can point out its four parts: start value, condition, body and the counter's change;
- you trace a loop in a table in which the last condition check gives `false` and isn't an iteration;
- you know that a loop can run zero times;
- you build up a result in an accumulator and update it with `+=`;
- you remember from lesson 3.2 that a variable declared in a block exists only in that block.

## The situation

Every loop in lessons 4.1 and 4.2 had the same layout: a counter with its start value **before** the loop, the condition **at the top**, and the counter's change **at the end** of the body. Three things that together control the repetition stood in three different places in the program. In a longer loop it's easy to miss where the counter starts, or whether it changes at all.

Today you'll meet the `for` loop, which gathers these three parts into one line. It does nothing that `while` can't do. It just tidies up how a counter-controlled loop is written.

After this lesson you'll be able to:

- point out the three parts of a `for` header and explain when each of them runs;
- predict the counter's values in successive iterations, including with zero iterations;
- increase a counter by one with `++counter`;
- explain why a counter declared in a `for` header doesn't exist after the loop;
- find an off-by-one error in a `for`;
- combine `for` with an accumulator;
- choose between `while` and `for` where both are possible.

## 1. Prepare the project

In `cpp-workspace`, create a `lesson_4_3` folder and copy `main.cpp` and `CMakeLists.txt` into it from the original `lesson_05_first_program`. You type the programs from sections 2–9 into that folder's `main.cpp`.

## 2. From `while` to `for`

You know this program from lesson 4.1:

<!-- example: laps_while -->
```cpp
#include <iostream>

int main() {
    const int total_laps{3};
    int lap{1};

    while (lap <= total_laps) {
        std::cout << "Lap " << lap << "\n";
        lap = lap + 1;
    }

    std::cout << "Finished\n";
}
```

**Recall:** point out the counter's start value, the condition, the loop body and the counter's change. The answer is in [Example solutions](#example-solutions).

Can the start value, the condition and the counter's change be written closer together? Yes:

<!-- example: laps_for -->
```cpp
#include <iostream>

int main() {
    const int total_laps{3};

    for (int lap{1}; lap <= total_laps; ++lap) {
        std::cout << "Lap " << lap << "\n";
    }

    std::cout << "Finished\n";
}
```

**Predict**: will both programs print the same thing? Then run both.

<details>
<summary>The output of both programs</summary>

<!-- output: laps_while -->
```text
Lap 1
Lap 2
Lap 3
Finished
```

<!-- output: laps_for -->
```text
Lap 1
Lap 2
Lap 3
Finished
```

The output is identical. Both programs control the repetition the same way; they just write it differently.

</details>

This time the programs deliberately don't print `lap` after the loop, as lesson 4.1 did. You'll see why in section 7.

## 3. The three parts of a `for` header

<!-- fragment -->
```cpp
for (int lap{1}; lap <= total_laps; ++lap)
```

| Part | In the program | When it runs |
|---|---|---|
| **Initialisation** | `int lap{1}` | Once, at the start of this loop. It creates the counter and gives it its start value. It is **not** repeated in later iterations. |
| **Condition** | `lap <= total_laps` | Before every run of the body. If it's false, the body doesn't run, and the program carries on after the loop. |
| **Update** | `++lap` | After every run of the body, before the next condition check. Here it increases the counter by 1. |

- **The semicolons** separate these three parts of the header. They aren't the semicolons that end the statements in the loop body: the body's statements stand in braces as always, each with its own semicolon.
- **The loop body** is, as in `while`, the statements between `{` and `}`.
- `++lap` stands in the header **before** the body, but runs **after** it. That's the most important difference between where it's written and when it runs.

## 4. The order of execution

A `for` loop with a counter runs in this order:

1. **Initialisation**, once.
2. **The condition check.**
3. If the condition is true: **the body runs**.
4. **The update.**
5. **Back to the condition check**, i.e. to step 2.

When a condition check gives `false`, the program goes on past the loop. The trace table for three laps:

| Condition check | `lap` at the check | `lap <= total_laps` | Loop body | Update `++lap` |
|---|---|---|---|---|
| 1 | 1 | `true` | prints `Lap 1` | `lap` becomes 2 |
| 2 | 2 | `true` | prints `Lap 2` | `lap` becomes 3 |
| 3 | 3 | `true` | prints `Lap 3` | `lap` becomes 4 |
| 4 | 4 | `false` | **doesn't run**: the loop ends | **doesn't run** |

- The initialisation isn't in any row: it ran once, **before** the first check.
- The fourth check gives `false`. It isn't an iteration: neither the body nor the update runs any more.
- **Compare with the table from lesson 4.1.** The rows are the same: the same counter values, the same condition results, the same printed lines. In `while`, the counter's change was the body's last statement; in `for`, it stands in the header as the update. The mechanism is the same; the way it's written is different.

**Your turn.** Write down, in order, every step of this loop when `total_laps` is 2: "initialisation: `lap` = 1", "check: `1 <= 2`, `true`", "body: …" and so on, to the end of the loop. How many condition checks are there, and how many updates? The answer is in [Example solutions](#example-solutions).

## 5. Zero, one and several iterations

Now the user gives the number of laps. The program accepts 0 to 5 laps. For other numbers it prints a message and skips the loop. We assume the user types a whole number.

<!-- example: laps_for_input -->
```cpp
#include <iostream>

int main() {
    int total_laps{0};

    std::cout << "Enter number of laps (0-5):\n";
    std::cin >> total_laps;

    if (total_laps >= 0 && total_laps <= 5) {
        for (int lap{1}; lap <= total_laps; ++lap) {
            std::cout << "Lap " << lap << "\n";
        }

        std::cout << "Finished\n";
    } else {
        std::cout << "Number of laps must be from 0 to 5\n";
    }
}
```

**Predict.** Copy the table and fill it in before you run the program.

| `total_laps` | Number of iterations | First number printed | Last number printed |
|---|---|---|---|
| 0 | | | |
| 1 | | | |
| 3 | | | |
| 5 | | | |
| -1 | | | |
| 6 | | | |

Then run the program six times, without changing the code.

<!-- input: laps_for_input -->
```text
0
```

<details>
<summary>Standard output for 0</summary>

<!-- output: laps_for_input -->
```text
Enter number of laps (0-5):
Finished
```

The initialisation ran (`lap` = 1), but the first check, `1 <= 0`, gave `false`. The body and the update didn't run even once. A `for` loop, like `while`, can run zero times.

</details>

<!-- input: laps_for_input -->
```text
1
```

<details>
<summary>Standard output for 1</summary>

<!-- output: laps_for_input -->
```text
Enter number of laps (0-5):
Lap 1
Finished
```

</details>

<!-- input: laps_for_input -->
```text
3
```

<details>
<summary>Standard output for 3</summary>

<!-- output: laps_for_input -->
```text
Enter number of laps (0-5):
Lap 1
Lap 2
Lap 3
Finished
```

</details>

<!-- input: laps_for_input -->
```text
5
```

<details>
<summary>Standard output for 5</summary>

<!-- output: laps_for_input -->
```text
Enter number of laps (0-5):
Lap 1
Lap 2
Lap 3
Lap 4
Lap 5
Finished
```

</details>

<!-- input: laps_for_input -->
```text
-1
```

<details>
<summary>Standard output for -1</summary>

<!-- output: laps_for_input -->
```text
Enter number of laps (0-5):
Number of laps must be from 0 to 5
```

</details>

<!-- input: laps_for_input -->
```text
6
```

<details>
<summary>Standard output for 6</summary>

<!-- output: laps_for_input -->
```text
Enter number of laps (0-5):
Number of laps must be from 0 to 5
```

</details>

Compare your completed table with [Example solutions](#example-solutions).

## 6. Increasing by one: `++`

In the `for` header, the counter changes with `++lap`. The `++` operator changes the value of an **existing** variable. For a whole number such as `lap`, it increases it by one.

These three forms can do the same simple counter step:

<!-- fragment -->
```cpp
lap = lap + 1;
lap += 1;
++lap;
```

- When you only want to increase the counter by one, all three have the same effect. In a `for` header you'll most often see `++lap`.
- Use `++lap` as a step of its own: as the update in the header, or as a separate statement, for example `++laps_done;`. In this course we don't put it inside longer expressions.
- `+= 1` is still correct, also for the event counters from lesson 4.2. Choose the form that reads most clearly.
- To an accumulator you add the right value, as before: `total += number;`, not `++`.

## 7. Where does a `for` counter exist?

A counter declared in a `for` header, such as `int lap{1}`, exists only **in that loop**: in its condition, its update and its body. After the loop it's gone.

This program should print, after the loop, how many laps were done:

<!-- broken: lap_after_for at=8 errors=1 error=^use of undeclared identifier 'lap'$ -->
```cpp
#include <iostream>

int main() {
    for (int lap{1}; lap <= 3; ++lap) {
        std::cout << "Lap " << lap << "\n";
    }

    std::cout << "Laps done: " << lap << "\n";
}
```

1. **Predict** whether this program will build.
2. Build it and read the compiler's message.
3. Point to the declaration of the variable `lap`.
4. Explain why that variable isn't available on line 8.
5. Suggest a fix.

<details>
<summary>What the compiler reports, and why</summary>

The program doesn't build. On line 8 the compiler reports `use of undeclared identifier 'lap'`: it doesn't know the name `lap`. You know this message from lesson 3.2. `lap` is declared in the `for` header, so it exists only in that loop. On line 8, after the loop's closing brace, that declaration no longer applies.

</details>

**The fix depends on the requirement.** If the counter's value isn't needed after the loop, simply don't use it there, as in the programs in sections 2 and 5. Here, though, the requirement says: after the loop, print how many laps were done. Such a value has to be kept in a variable declared **before** the loop, in a wider scope. Write down your idea for the fix before you look at [Example solutions](#example-solutions).

## 8. Find the bug: round zero

The requirement: the program prints rounds numbered **from 1 to the given number of rounds inclusive**, and finally `Done`. The number of rounds must be from 0 to 5. This program builds and runs, but doesn't meet the requirement:

<!-- example: rounds_bug -->
```cpp
#include <iostream>

int main() {
    int round_count{0};

    std::cout << "Enter round count (0-5):\n";
    std::cin >> round_count;

    if (round_count >= 0 && round_count <= 5) {
        for (int round{0}; round <= round_count; ++round) {
            std::cout << "Round " << round << "\n";
        }

        std::cout << "Done\n";
    } else {
        std::cout << "Round count must be from 0 to 5\n";
    }
}
```

1. Read the requirement and work out what the program **should** print for 0, 1 and 3 rounds.
2. Trace the loop for 0 rounds and for 1 round: which value does the counter start from, and how many times does the condition give `true`?
3. Run the program for 0, 1 and 3.
4. Find the bug.
5. Fix the program.
6. Check all three cases again.

The results before the fix, and the fixed program, are in [Example solutions](#example-solutions). Look there after your own attempt.

## 9. `for` and an accumulator

A `for` loop can also build up a result, just like `while` in lesson 4.2:

<!-- example: sum_for -->
```cpp
#include <iostream>

int main() {
    int total{0};

    for (int number{1}; number <= 3; ++number) {
        total += number;
    }

    std::cout << "Total: " << total << "\n";
}
```

**Predict** the result, then run the program.

<details>
<summary>The program's output</summary>

<!-- output: sum_for -->
```text
Total: 6
```

</details>

This loop has **two** updates, and each has a different role:

- `++number` in the header changes the **counter**, which controls the repetition;
- `total += number;` in the body changes the **accumulator**, which holds the sum.

The accumulator is declared before the loop, because its value is needed after it. The counter is in the header, because it isn't needed after the loop.

## 10. Mission: a training plan

The program draws up a plan for a simple exercise. The user gives the number of rounds and the number of repetitions in the first round. In each following round, the number of repetitions goes up by 2. The program prints the number of repetitions in each round, and finally the total number of repetitions in the whole training.

**Requirements:**

- The number of rounds is a whole number from 0 to 5.
- The number of repetitions in the first round is a whole number from 1 to 10.
- The program asks for both values, in this order: `Enter round count:` and `Enter starting repetitions:`.
- For each round the program prints a line `Round K: R repetitions`, and at the end `Total repetitions: T`.
- For 0 rounds the program prints no round, and the total number of repetitions is 0.
- If either value is outside its range, the program prints only `Invalid training data` and prints no round. It doesn't ask for the data again.
- We assume the user types whole numbers.

In `cpp-workspace`, create a `training_plan` folder, copy `CMakeLists.txt` into it from the original `lesson_05_first_program`, create an empty `main.cpp` and write the program on your own.

For 3 rounds and 4 repetitions in the first round, standard output must be:

<!-- input: training_plan -->
```text
3
4
```

<!-- output: training_plan -->
```text
Enter round count:
Enter starting repetitions:
Round 1: 4 repetitions
Round 2: 6 repetitions
Round 3: 8 repetitions
Total repetitions: 18
```

**This isn't the laps loop.** There was one counter, which grew by 1 and was printed. Here **three** values with different roles change in every round: the round number, the number of repetitions in the current round, and the total number of repetitions. Each changes differently and at a different moment. You have to decide on your own:

1. which variable is the round counter, which value it starts from, when the loop ends and how the counter changes;
2. where to keep the current round's repetitions, and when to increase them by 2;
3. where to declare the accumulator for the total repetitions, and when to add the current round's repetitions to it;
4. what the program does for zero rounds, and how to avoid printing an extra round.

**Before you write the program**, prepare two things:

- a trace table for 3 rounds and 4 repetitions: the round number, the repetitions printed in that round, and the sum after that round;
- a table of test cases: zero rounds, one round, several rounds, the largest acceptable number of rounds, both ends of the repetitions range, and the values just outside the range of both inputs. Write down the expected standard output for each case.

### Success criteria

- The program builds as C++20, and its standard output for 3 rounds and 4 repetitions is exactly as above.
- For every acceptable pair of values, the program prints exactly as many rounds as given, with the right number of repetitions, and the right sum. For data outside the range it prints only `Invalid training data`.
- The rounds are controlled by a `for` loop with braces, and its counter changes with `++`.
- The total number of repetitions is built up in an accumulator with `+=`.
- The range of both values is checked before the program starts printing rounds.
- The trace table and the table of cases were made before running the program.
- You can explain why the loop ends, and why for zero rounds the sum is 0.

When the result matches, you can save the project in Git, as in lesson 1.5.

<details>
<summary>Hint 1</summary>

List the values that change from round to round, and next to each write down by how much it changes. Which of them controls how many times the loop runs, and which are only printed or added up?

</details>

<details>
<summary>Hint 2</summary>

Three things happen in one round: printing the round's data, adding its repetitions to the sum, and preparing the number of repetitions for the next round. In what order must they happen, so that the first round shows the number the user gave?

</details>

<details>
<summary>Hint 3</summary>

The `for` header answers three questions: which number the first round starts from, while what the loop should keep going, and how to move to the next round's number. Check your condition for 1 round in a trace table.

</details>

<details>
<summary>The full list of control cases: open after preparing your own table</summary>

| Rounds | Start | Repetitions printed | Sum | What it checks |
|---|---|---|---|---|
| 3 | 4 | 4, 6, 8 | 18 | several iterations |
| 0 | 4 | no rounds | 0 | zero iterations |
| 1 | 4 | 4 | 4 | one iteration |
| 5 | 1 | 1, 3, 5, 7, 9 | 25 | the most rounds, the smallest start |
| 2 | 10 | 10, 12 | 22 | the largest start |
| -1 | 4 | — | — | the number of rounds just below the range |
| 6 | 4 | — | — | the number of rounds just above the range |
| 3 | 0 | — | — | the start just below the range |
| 3 | 11 | — | — | the start just above the range |

The cases with dashes end with the line `Invalid training data`. The case 3 and 4 is checked above, in the mission's description.

<!-- input: training_plan -->
```text
0
4
```

<!-- output: training_plan -->
```text
Enter round count:
Enter starting repetitions:
Total repetitions: 0
```

<!-- input: training_plan -->
```text
1
4
```

<!-- output: training_plan -->
```text
Enter round count:
Enter starting repetitions:
Round 1: 4 repetitions
Total repetitions: 4
```

<!-- input: training_plan -->
```text
5
1
```

<!-- output: training_plan -->
```text
Enter round count:
Enter starting repetitions:
Round 1: 1 repetitions
Round 2: 3 repetitions
Round 3: 5 repetitions
Round 4: 7 repetitions
Round 5: 9 repetitions
Total repetitions: 25
```

<!-- input: training_plan -->
```text
2
10
```

<!-- output: training_plan -->
```text
Enter round count:
Enter starting repetitions:
Round 1: 10 repetitions
Round 2: 12 repetitions
Total repetitions: 22
```

<!-- input: training_plan -->
```text
-1
4
```

<!-- output: training_plan -->
```text
Enter round count:
Enter starting repetitions:
Invalid training data
```

<!-- input: training_plan -->
```text
6
4
```

<!-- output: training_plan -->
```text
Enter round count:
Enter starting repetitions:
Invalid training data
```

<!-- input: training_plan -->
```text
3
0
```

<!-- output: training_plan -->
```text
Enter round count:
Enter starting repetitions:
Invalid training data
```

<!-- input: training_plan -->
```text
3
11
```

<!-- output: training_plan -->
```text
Enter round count:
Enter starting repetitions:
Invalid training data
```

</details>

An example solution is in [Example solutions](#example-solutions).

## 11. `while` or `for`?

Both loops can do many of the same tasks: every loop in this lesson can be written with `while`, and the loops in lessons 4.1 and 4.2 with `for`. Neither is always better.

- **`while`** reads naturally as: "repeat **while** this condition is true".
- **`for`** is often convenient when a **counter** with a start value, a condition and an update controls the repetition. All three are then visible in one line, and the counter doesn't exist for longer than it's needed.

This lesson shows the basic `for` pattern with a counter. In lesson 4.4 you'll see a loop without such a counter, which keeps repeating until a goal is reached.

## 12. When something goes differently

| What you see | What it means | What to do |
|---|---|---|
| Round or lap number 0 appears | The counter starts at 0, but the requirement says "from 1". | Check the initialisation in the header. The start value follows from the requirement (section 8). |
| One iteration too many or too few | The condition and the start value don't fit together, for example `<` instead of `<=`. | Trace the loop for one iteration and for the largest value. |
| `use of undeclared identifier` for the counter after the loop | A counter declared in a `for` header exists only in the loop (section 7). | If the value is needed after the loop, keep it in a variable declared before the loop. |
| A compile error in the `for` header | A semicolon between the parts is missing, or there's a comma instead of a semicolon. | The header has three parts separated by two semicolons: initialisation; condition; update. |
| The first round doesn't show the number the user gave | The number of repetitions is increased before printing. | Fix the order in the body: first the current round's data, then preparing the next one. |
| The total repetitions are too small or too large | The accumulator is reset in the loop body, added at the wrong moment, or the counter is added instead of the repetitions. | Fill in a trace table: the sum after each round must be the sum of the repetitions printed. |
| The same line appears forever | The counter doesn't change, or changes in the wrong direction. | Stop the program, as in lesson 4.1, and check the update in the header. |

## 13. Explain

Answer briefly, preferably in writing. Only then compare with the example answer.

**1.** How many times does the initialisation in a `for` header run?

<details>
<summary>Example answer</summary>

Once, at the start of the loop, before the first condition check.

</details>

**2.** When is the condition checked, and when does the update run?

<details>
<summary>Example answer</summary>

The condition: before every run of the body. The update: after every run of the body, just before the next condition check.

</details>

**3.** Can the body of a `for` loop run zero times?

<details>
<summary>Example answer</summary>

Yes. If the first condition check gives `false`, like `1 <= 0`, neither the body nor the update runs even once.

</details>

**4.** What does `++counter` do?

<details>
<summary>Example answer</summary>

It increases the value of the existing whole-number variable `counter` by one. As a step of its own, it has the same effect as `counter = counter + 1;` and `counter += 1;`.

</details>

**5.** What are the semicolons in a `for` header for?

<details>
<summary>Example answer</summary>

They separate the header's three parts: the initialisation, the condition and the update.

</details>

**6.** Why isn't a counter declared in the header available after the loop?

<details>
<summary>Example answer</summary>

Because it exists only in that loop, like a variable declared in a block (lesson 3.2). After the loop, its declaration no longer applies.

</details>

**7.** When is `for` more readable than `while`?

<details>
<summary>Example answer</summary>

Often when a counter with a start value, a condition and an update controls the repetition. In `for` all three stand in one line. When we think rather "repeat while something is true", `while` is often more natural.

</details>

**8.** Why does the mission need both a round counter and an accumulator?

<details>
<summary>Example answer</summary>

Because they have different roles. The round counter decides how many times the loop runs, and gives the round number. The accumulator builds up the total number of repetitions. What goes into the sum is a round's repetitions, not the round number.

</details>

**9.** What happens if, in the mission, you increase the number of repetitions by 2 **before** printing the round's data?

<details>
<summary>Example answer</summary>

The first round shows a number 2 greater than the one given, every following round is shifted too, and the sum is too large if you add after increasing. For 3 rounds and 4 repetitions the program would print 6, 8, 10 instead of 4, 6, 8.

</details>

## Summary

- `for (initialisation; condition; update) { … }` gathers into one line the three parts that control a counting loop.
- The **initialisation** runs once, at the start. The **condition** is checked before every iteration. The **update** runs after every iteration, before the next check.
- The last condition check gives `false` and isn't an iteration. The body can run zero times.
- `++counter` increases a whole-number counter by one. `counter += 1` and `counter = counter + 1` are still correct.
- A counter declared in a `for` header exists only in that loop. Keep a value that's needed after the loop in a variable declared before it.
- The counter's start value follows from the requirement. An off-by-one error is revealed fastest by the case with zero or one iteration.
- `for` and `while` can do the same tasks. `for` is often convenient when a counter controls the repetition.

## What's next

In this lesson the number of iterations was known before the loop started. In lesson 4.4 the program will repeat an action **until it reaches a goal**, for example saving until it has the amount it needs, and you won't know the number of iterations in advance. **Lesson 4.4 is in preparation.**

---

## Example solutions

Look here **after your own attempt**. Your names may differ, as long as the standard output is as required.

<details>
<summary>Section 2: the four parts of the while loop</summary>

- **Start value:** `int lap{1};`, before the loop.
- **Condition:** `lap <= total_laps`, in `while ( … )`.
- **Body:** the statements between `{` and `}`, here printing `Lap …` and the counter's change.
- **Counter's change:** `lap = lap + 1;`, the body's last statement.

In `for`, the start value and the counter's change move into the header, next to the condition.

</details>

<details>
<summary>Section 4: every step for two laps</summary>

1. Initialisation: `lap` = 1.
2. Check: `1 <= 2`, `true`.
3. Body: prints `Lap 1`.
4. Update: `++lap`, `lap` = 2.
5. Check: `2 <= 2`, `true`.
6. Body: prints `Lap 2`.
7. Update: `++lap`, `lap` = 3.
8. Check: `3 <= 2`, `false`: the loop ends, and the program prints `Finished`.

Three condition checks, two runs of the body, two updates and one initialisation.

</details>

<details>
<summary>Section 5: the prediction table</summary>

| `total_laps` | Number of iterations | First number printed | Last number printed |
|---|---|---|---|
| 0 | 0 | — | — |
| 1 | 1 | 1 | 1 |
| 3 | 3 | 1 | 3 |
| 5 | 5 | 1 | 5 |
| -1 | 0 (loop skipped by `else`) | — | — |
| 6 | 0 (loop skipped by `else`) | — | — |

For 0 the loop is reached, but its body doesn't run: the condition is false from the start. For -1 and 6 the program never reaches the loop.

</details>

<details>
<summary>Section 7: the fix for the counter after the loop</summary>

The requirement says: after the loop, print how many laps were done. That value must exist after the loop, so it lives in a variable declared before it. The loop increases it by one in every iteration:

<!-- example: laps_done_after_for -->
```cpp
#include <iostream>

int main() {
    int laps_done{0};

    for (int lap{1}; lap <= 3; ++lap) {
        std::cout << "Lap " << lap << "\n";
        ++laps_done;
    }

    std::cout << "Laps done: " << laps_done << "\n";
}
```

<!-- output: laps_done_after_for -->
```text
Lap 1
Lap 2
Lap 3
Laps done: 3
```

Notice: even if `lap` existed after the loop, its value would be 4, not 3. That's how it was in lesson 4.1, where the program printed `lap is now 4`. The number of laps done is a different value from the counter after the loop ends, so it gets its own variable.

</details>

<details>
<summary>Section 8: the results before the fix, and the fixed program</summary>

Before the fix, for 0, 1 and 3:

<!-- input: rounds_bug -->
```text
0
```

<!-- output: rounds_bug -->
```text
Enter round count (0-5):
Round 0
Done
```

<!-- input: rounds_bug -->
```text
1
```

<!-- output: rounds_bug -->
```text
Enter round count (0-5):
Round 0
Round 1
Done
```

<!-- input: rounds_bug -->
```text
3
```

<!-- output: rounds_bug -->
```text
Enter round count (0-5):
Round 0
Round 1
Round 2
Round 3
Done
```

- **The bug shows already for 0:** the requirement allows no round, but the program prints `Round 0`. Every case has one iteration too many, and the numbering starts at 0.
- **The cause:** the counter starts at 0, and the condition `round <= round_count` also allows the last number. From 0 to 3 inclusive there are four numbers, not three.
- **The fix:** the requirement says "from 1 to the number of rounds inclusive", so the counter starts at 1:

<!-- example: rounds_fixed -->
```cpp
#include <iostream>

int main() {
    int round_count{0};

    std::cout << "Enter round count (0-5):\n";
    std::cin >> round_count;

    if (round_count >= 0 && round_count <= 5) {
        for (int round{1}; round <= round_count; ++round) {
            std::cout << "Round " << round << "\n";
        }

        std::cout << "Done\n";
    } else {
        std::cout << "Round count must be from 0 to 5\n";
    }
}
```

<!-- input: rounds_fixed -->
```text
0
```

<!-- output: rounds_fixed -->
```text
Enter round count (0-5):
Done
```

<!-- input: rounds_fixed -->
```text
1
```

<!-- output: rounds_fixed -->
```text
Enter round count (0-5):
Round 1
Done
```

<!-- input: rounds_fixed -->
```text
3
```

<!-- output: rounds_fixed -->
```text
Enter round count (0-5):
Round 1
Round 2
Round 3
Done
```

Changing only the condition to `round < round_count` would give the right **number** of iterations, but the numbers 0 to 2. That doesn't meet the requirement. A loop starting at 0 isn't wrong in itself: the right start value depends on what the program has to print.

</details>

<details>
<summary>Section 10: the mission, a training plan</summary>

<!-- example: training_plan -->
```cpp
#include <iostream>

int main() {
    int round_count{0};
    int start_repetitions{0};

    std::cout << "Enter round count:\n";
    std::cin >> round_count;
    std::cout << "Enter starting repetitions:\n";
    std::cin >> start_repetitions;

    const bool rounds_ok{round_count >= 0 && round_count <= 5};
    const bool start_ok{start_repetitions >= 1 && start_repetitions <= 10};

    if (rounds_ok && start_ok) {
        int repetitions{start_repetitions};
        int total_repetitions{0};

        for (int round{1}; round <= round_count; ++round) {
            std::cout << "Round " << round << ": " << repetitions << " repetitions\n";
            total_repetitions += repetitions;
            repetitions += 2;
        }

        std::cout << "Total repetitions: " << total_repetitions << "\n";
    } else {
        std::cout << "Invalid training data\n";
    }
}
```

| Condition check | `round` | `round <= 3` | Repetitions printed | `total_repetitions` after the round | `repetitions` for the next round |
|---|---|---|---|---|---|
| 1 | 1 | `true` | 4 | 4 | 6 |
| 2 | 2 | `true` | 6 | 10 | 8 |
| 3 | 3 | `true` | 8 | 18 | 10 |
| 4 | 4 | `false` | — | — | — |

- **Three values, three roles:** `round` controls the loop and gives the round number (`++round`), `repetitions` is the current round's repetitions (grows by 2), and `total_repetitions` is the accumulator (`+=`).
- **The order in the body:** first printing and adding to the sum, then `repetitions += 2;`. That way the first round shows the number the user gave, and the sum gets the same numbers that were printed.
- **Zero rounds:** the condition `1 <= 0` is false straight away, so no round appears, and `total_repetitions` stays 0.
- After the last round, `repetitions` already holds the value for a round that won't happen (10). That does no harm, because the program doesn't print it.

</details>

**Previous lesson:** [Lesson 4.2: Sums and accumulators](lesson_02_sums_and_accumulators.en.md) · **Next lesson:** in preparation · [Course overview](../../README.en.md)

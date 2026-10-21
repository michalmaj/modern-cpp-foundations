# Lesson 4.1: The first loop (`while`)

[Polski](lesson_01_the_first_loop.md) · **English** · [Course overview](../../README.en.md)

> **Module 4, lesson 1** · about 60–75 minutes
> **You need:** the `cpp-workspace` folder and the original `lesson_05_first_program` project, as before. You don't need the debugger in this lesson.
> **Pilot version.** The programs in this lesson are checked automatically on Windows, Ubuntu and macOS, including with the given input data. Stopping a program in CLion is described without a manual check on every system.

## Before you start

This lesson assumes that after Module 3:

- you write `if` and `if`/`else` with braces, and combine conditions with `&&`;
- you know that `if` checks its condition with the variable's **current** value;
- you change a variable's value by assignment, including from its old value, for example `count = count + 1;` (lesson 2.2);
- you check a program for values at a boundary and right next to it.

## The situation

A training organiser wants a program to print the numbers of the laps, one after another. For three laps, three statements are enough:

<!-- fragment -->
```cpp
std::cout << "Lap 1\n";
std::cout << "Lap 2\n";
std::cout << "Lap 3\n";
```

But what if there were 10 laps? Or 100? Or what if the user gave the number, and the program didn't know it when the code was written? Copying the same statement stops making sense. You need a way for the program to **go back to the same piece of code** and run it again, and to **know when to stop**. Today you'll meet the first loop: `while`.

After this lesson you'll be able to:

- explain why a program needs repetition;
- point out, in a `while` loop, the counter's start value, the condition, the loop body and the counter's change;
- explain when the program checks the condition and why the loop ends;
- trace a loop in a table and predict the number of repetitions, including zero;
- find an off-by-one error and choose the cases that reveal it;
- recognise a loop that makes no progress, without running it;
- stop a program that runs too long;
- write your own loop with a counter.

## 1. Prepare the project

In `cpp-workspace`, create a `lesson_4_1` folder and copy `main.cpp` and `CMakeLists.txt` into it from the original `lesson_05_first_program`. You type the programs from sections 2–6 into that folder's `main.cpp`.

## 2. The first loop: three laps

<!-- example: laps_three -->
```cpp
#include <iostream>

int main() {
    const int total_laps{3};
    int lap{1};

    while (lap <= total_laps) {
        std::cout << "Lap " << lap << "\n";
        lap = lap + 1;
    }

    std::cout << "Finished, lap is now " << lap << "\n";
}
```

Before you run the program, **answer in writing**:

1. Which lap numbers will the program print?
2. How many times will the block in braces after `while` run?
3. What value will `lap` have after the loop ends?
4. Why does the last line say exactly what it says?

Now run the program.

<details>
<summary>The program's output</summary>

<!-- output: laps_three -->
```text
Lap 1
Lap 2
Lap 3
Finished, lap is now 4
```

The last line says `4`, not `3`. Sections 3 and 4 explain why.

</details>

## 3. The four parts of the loop

`while` repeats the block in braces **while** the condition holds. This loop has four parts:

| Part | In the program | Role |
|---|---|---|
| **Start value** | `int lap{1};` | Before the loop: the counter starts from this value. This line runs **once**. |
| **Condition** | `while (lap <= total_laps)` | Before every run of the block, the program checks whether the condition holds. "Yes": it runs the block. "No": the loop ends. |
| **Loop body** | the statements between `{` and `}` | What is repeated: here, printing the lap number. |
| **Change of state** | `lap = lap + 1;` | The body's last statement: the counter gets a new value, 1 greater than the old one. |

The number of repetitions isn't written anywhere directly. It **follows** from these parts: the counter starts at 1, grows by 1 after each run of the body, and the condition stops holding once the counter goes past 3.

**`while` and `if`.** You know `if` from lesson 3.1: it checks a condition and, if the answer is "yes", runs the block, and then the program carries on. `while` checks its condition the same way, but **after running the block, it goes back to the condition** and checks it again, with the new value of `lap`. Only when the answer is "no" does the program skip the block and run the statements after the loop.

- The condition is checked **before every** run of the body, with the counter's current value.
- After running the body, the program doesn't go straight past the loop. **It goes back to the condition.**
- `while` **changes nothing by itself**. The counter grows only because the body contains the statement `lap = lap + 1;`.

One run of the loop body is called an **iteration**.

## 4. The trace table

A trace table shows best how a loop runs. Each row is **one check of the condition**:

| Condition check | `lap` at the check | `lap <= total_laps` | Loop body | `lap` after the body |
|---|---|---|---|---|
| 1 | 1 | `true` | prints `Lap 1`, then `lap = lap + 1;` | 2 |
| 2 | 2 | `true` | prints `Lap 2`, then `lap = lap + 1;` | 3 |
| 3 | 3 | `true` | prints `Lap 3`, then `lap = lap + 1;` | 4 |
| 4 | 4 | `false` | **doesn't run**: the loop ends | — |

- The condition was checked **4 times**, and the body ran **3 times**. The last check isn't an iteration: its `false` result ends the loop.
- After the third iteration, `lap` is 4. The loop ends precisely because 4 doesn't meet the condition `lap <= 3`. That value stays in the variable, so the last line says `lap is now 4`.

**Your turn.** Imagine the program says `const int total_laps{2};`. Copy the table and fill it in for this case: how many condition checks, how many iterations, and what will the program's last line be? The answer is in [Example solutions](#example-solutions).

## 5. The number of laps from input

Now the user gives the number of laps. To keep the examples short, the program accepts only 0 to 5 laps. For other numbers it prints a message and doesn't start the loop at all. We assume the user types a whole number.

<!-- example: laps_input -->
```cpp
#include <iostream>

int main() {
    int total_laps{0};

    std::cout << "Enter number of laps (0-5):\n";
    std::cin >> total_laps;

    if (total_laps >= 0 && total_laps <= 5) {
        int lap{1};

        while (lap <= total_laps) {
            std::cout << "Lap " << lap << "\n";
            lap = lap + 1;
        }

        std::cout << "Finished\n";
    } else {
        std::cout << "Number of laps must be from 0 to 5\n";
    }
}
```

- The `if` from lesson 3.5 checks the data before the program starts repeating. The loop is in the branch for acceptable data.
- `total_laps` is the number of laps **requested**. It's read once and doesn't change in the loop.
- `lap` is the counter, which **changes** in every iteration.
- The number of iterations **performed** follows from both of these values.

**Predict.** Copy the table and fill it in for three runs: 0, 1 and 3.

| `total_laps` | Laps printed | Number of iterations | `lap` after the loop |
|---|---|---|---|
| 0 | | | |
| 1 | | | |
| 3 | | | |

Then run the program three times, without changing the code.

<!-- input: laps_input -->
```text
0
```

<details>
<summary>Standard output for 0</summary>

<!-- output: laps_input -->
```text
Enter number of laps (0-5):
Finished
```

</details>

<!-- input: laps_input -->
```text
1
```

<details>
<summary>Standard output for 1</summary>

<!-- output: laps_input -->
```text
Enter number of laps (0-5):
Lap 1
Finished
```

</details>

<!-- input: laps_input -->
```text
3
```

<details>
<summary>Standard output for 3</summary>

<!-- output: laps_input -->
```text
Enter number of laps (0-5):
Lap 1
Lap 2
Lap 3
Finished
```

</details>

Compare your completed table with [Example solutions](#example-solutions).

**Zero iterations.** For 0 laps, the first condition check, `1 <= 0`, gives `false`. The loop body doesn't run **even once**, and the program goes straight to `Finished`. That's not a bug: for zero laps, that's exactly what should happen. A `while` loop can run zero times, because it checks its condition **before** the first iteration.

**And for 9?** Predict what the program prints for a number outside the range, and whether the loop runs. Then check.

<!-- input: laps_input -->
```text
9
```

<details>
<summary>Standard output for 9, and explanation</summary>

<!-- output: laps_input -->
```text
Enter number of laps (0-5):
Number of laps must be from 0 to 5
```

The loop doesn't run, but for a different reason than for 0: the program never reaches it, because it takes the `else` branch.

</details>

## 6. Where is the counter's change?

In this program, the counter's change comes **before** printing, not after it. Everything else is the same:

<!-- example: laps_update_first -->
```cpp
#include <iostream>

int main() {
    const int total_laps{3};
    int lap{1};

    while (lap <= total_laps) {
        lap = lap + 1;
        std::cout << "Lap " << lap << "\n";
    }

    std::cout << "Finished, lap is now " << lap << "\n";
}
```

**Predict** which lap numbers will appear on the screen now. Look especially at the third iteration: what value does `lap` have just before printing? Write your answer down, then run the program.

<details>
<summary>The program's output and explanation</summary>

<!-- output: laps_update_first -->
```text
Lap 2
Lap 3
Lap 4
Finished, lap is now 4
```

In the third iteration, `lap = lap + 1;` changes 3 to 4. The value 4 no longer meets the condition `lap <= 3`, and yet the program prints `Lap 4`. **The program doesn't leave the loop body halfway** when the condition stops holding. It runs the body to the end, and checks the condition only afterwards, when it goes back to the top. Then 4 gives `false` and the loop ends.

Both versions run the body three times, but only the first prints laps 1 to 3. The order of statements in the body matters: with the counter's change at the end of the body, the whole iteration still works with the "old" value.

</details>

## 7. Find the bug: off by one

The requirement: the program prints the laps **from 1 to `total_laps` inclusive**. In this version, someone changed the loop's condition:

<!-- example: laps_bug -->
```cpp
#include <iostream>

int main() {
    int total_laps{0};

    std::cout << "Enter number of laps (0-5):\n";
    std::cin >> total_laps;

    if (total_laps >= 0 && total_laps <= 5) {
        int lap{1};

        while (lap < total_laps) {
            std::cout << "Lap " << lap << "\n";
            lap = lap + 1;
        }

        std::cout << "Finished\n";
    } else {
        std::cout << "Number of laps must be from 0 to 5\n";
    }
}
```

1. Read the requirement and **predict** what the program **should** print for 0, 1 and 3 laps.
2. Predict what **this** program will print. A trace table for 1 lap will help.
3. Run the program for 0, 1 and 3.
4. Find the first case where the result doesn't match the requirement.
5. Fix the program.
6. Check all three cases again.

The program's results before the fix, and the fix, are in [Example solutions](#example-solutions). Look there after your own attempt.

## 8. A loop that makes no progress

The condition `lap <= total_laps` depends on `lap`. What if there is no statement in the body that changes `lap`? **Analyse this fragment on paper; don't run it**:

<!-- fragment -->
```cpp
const int total_laps{3};
int lap{1};

while (lap <= total_laps) {
    std::cout << "Lap " << lap << "\n";
}
```

| Condition check | `lap` at the check | `lap <= total_laps` | Loop body | `lap` after the body |
|---|---|---|---|---|
| 1 | 1 | `true` | prints `Lap 1` | 1 |
| 2 | 1 | `true` | prints `Lap 1` | 1 |
| 3 | 1 | `true` | prints `Lap 1` | 1 |
| … | 1 | `true` | prints `Lap 1` | 1 |

Every check sees the same value of `lap`, so it gives the same result: `true`. Nothing in the body brings the program closer to the answer "no", so the loop **has no way to end**. The program would print `Lap 1` forever. A loop like this is called an **infinite loop**.

So for every loop, ask: **what changes in the body, and does that change lead to the condition stopping to hold at some point?** In this lesson the answer is the counter's change. In later lessons you'll see loops that end for other reasons, because their condition depends on other changing values.

## 9. How do you stop a program that runs too long?

If you start a loop that doesn't end by mistake, stop the program:

- **in the terminal** (PowerShell, macOS and Linux): press <kbd>Ctrl</kbd> + <kbd>C</kbd>;
- **in CLion:** click the **Stop** button (the red square) in the **Run** window or on the top toolbar.

The program stops, and you can fix the code and build it again. You don't break anything: you only stop your own program.

A program may also be **waiting for data**, as in lesson 2.6, and then nothing happens either. So ask: did the program ask for data that hasn't been typed yet? If so, it's waiting. If the data was typed and the same lines keep piling up on the screen, the loop doesn't end.

## 10. Mission: a countdown

Before an event starts, the program counts down out loud. The user gives the countdown length `N`: a whole number from 0 to 5. The program prints `N`, then `N - 1`, and so on down to `1`, each number on its own line, and finally `Liftoff!`. For 0 it prints no number, only `Liftoff!`.

If the number is outside the range 0 to 5, the program prints only `Countdown length must be from 0 to 5` and doesn't start the countdown. We assume the user types a whole number.

In `cpp-workspace`, create a `countdown` folder, copy `CMakeLists.txt` into it from the original `lesson_05_first_program`, create an empty `main.cpp` and write the program on your own.

For 3, standard output must be:

<!-- input: countdown -->
```text
3
```

<!-- output: countdown -->
```text
Enter countdown length:
3
2
1
Liftoff!
```

For 0:

<!-- input: countdown -->
```text
0
```

<!-- output: countdown -->
```text
Enter countdown length:
Liftoff!
```

**This isn't the laps loop.** The lap counter started at 1, grew, and ended after going past the upper limit. The countdown counter starts from the value the user gives, **gets smaller**, and ends at the lower limit. You have to decide on your own:

1. which value the counter starts from;
2. which condition means "keep counting";
3. how the counter changes in each iteration;
4. where `Liftoff!` goes, so that it appears exactly once.

**Before you write the program**, prepare two things:

- a trace table for `N` = 3, with every condition check, including the last one;
- a table of test cases: zero iterations, one iteration, several iterations, the largest acceptable length, and the values just outside the range on both sides. Write down the expected standard output for each case.

### Success criteria

- The program builds as C++20, and its standard output for 3 and 0 is exactly as above.
- For every length from 0 to 5 the program prints the right numbers and `Liftoff!`, and for any other number only `Countdown length must be from 0 to 5`.
- The countdown is done by a `while` loop with braces. The counter changes by an explicit assignment, in the loop body.
- The range is checked with `if`/`else` before the program starts counting down.
- The trace table and the table of cases were made before running the program.
- The same program handles all cases, without changing the code.
- You can explain why the loop ends, and why for 0 the body doesn't run even once.

When the result matches, you can save the project in Git, as in lesson 1.5.

<details>
<summary>Hint 1</summary>

The loop's condition depends on the counter. If the counter doesn't change, the condition gives the same answer every time (section 8). Which statement in the body changes the counter?

</details>

<details>
<summary>Hint 2</summary>

Work out two boundary values: which number does the program print first, and which last? The first suggests the counter's start value. The last suggests when the condition must still give "yes".

</details>

<details>
<summary>Hint 3</summary>

The laps grew, but the countdown gets smaller. How do you write the counter's new value as 1 **less** than the old one? Check in a trace table for `N` = 1 that the loop prints exactly one number.

</details>

<details>
<summary>The full list of control cases: open after preparing your own table</summary>

| `N` | Standard output after the prompt | What it checks |
|---|---|---|
| 3 | `3`, `2`, `1`, `Liftoff!` | several iterations |
| 0 | `Liftoff!` | zero iterations |
| 1 | `1`, `Liftoff!` | one iteration |
| 5 | `5`, `4`, `3`, `2`, `1`, `Liftoff!` | the largest acceptable length |
| -1 | `Countdown length must be from 0 to 5` | just below the range |
| 6 | `Countdown length must be from 0 to 5` | just above the range |

Cases 3 and 0 are checked above, in the mission's description.

<!-- input: countdown -->
```text
1
```

<!-- output: countdown -->
```text
Enter countdown length:
1
Liftoff!
```

<!-- input: countdown -->
```text
5
```

<!-- output: countdown -->
```text
Enter countdown length:
5
4
3
2
1
Liftoff!
```

<!-- input: countdown -->
```text
-1
```

<!-- output: countdown -->
```text
Enter countdown length:
Countdown length must be from 0 to 5
```

<!-- input: countdown -->
```text
6
```

<!-- output: countdown -->
```text
Enter countdown length:
Countdown length must be from 0 to 5
```

</details>

An example solution is in [Example solutions](#example-solutions).

## 11. When something goes differently

| What you see | What it means | What to do |
|---|---|---|
| The same line appears forever | The counter doesn't change, or changes in the wrong direction, so the condition always gives "yes". | Stop the program (section 9). Fill in a trace table for two or three checks, and find the statement that should bring the counter closer to the end. |
| The last number is missing, or there's one too many | An off-by-one error: a wrong start value, or `<` instead of `<=` (or the other way round). | Check the case with one iteration and the largest value. Fill in a trace table. |
| The loop doesn't run even once, although it should | The condition is false already at the first check. | Put the counter's start value into the condition and check whether the answer is "yes". |
| The printed values are shifted by one | The counter's change comes before the statement that prints it. | Decide which value the iteration should show: before the change or after it (section 6). |
| The final message appears several times | It's in the loop body, before the closing brace. | Move it after the loop's `}`. |
| The program does nothing and waits | It's waiting for data, as in lesson 2.6. | Type a number and press **Enter**. |
| A compile error at `while` | Usually a parenthesis or a brace is missing. | The condition in `( )`, the body in `{ }`. Every parenthesis and every brace has its pair. |

## 12. Explain

Answer in your own words, preferably in writing. Only then compare with the example answer.

**1.** When exactly does `while` check its condition?

<details>
<summary>Example answer</summary>

Before every iteration: the first time before the body runs for the first time, and then every time the program goes back to the top of the loop after running the body.

</details>

**2.** Why can `while` run zero times?

<details>
<summary>Example answer</summary>

Because the condition is checked before the first iteration. If it gives `false` straight away, like `1 <= 0` for zero laps, the body is skipped and the program carries on after the loop.

</details>

**3.** Why is `lap` 4 after the loop ends in section 2?

<details>
<summary>Example answer</summary>

Because in the third iteration `lap = lap + 1;` changes 3 to 4. At the fourth check, 4 doesn't meet `lap <= 3`, so the loop ends, and the value 4 stays in the variable.

</details>

**4.** Does changing the counter to a value that doesn't meet the condition stop the current iteration at once?

<details>
<summary>Example answer</summary>

No. The program runs the body to the end, and checks the condition only when it goes back to the top of the loop. That's why `Lap 4` appeared in section 6.

</details>

**5.** What happens if the counter doesn't change?

<details>
<summary>Example answer</summary>

Every check of the condition sees the same value and gives the same result. If that was `true`, the loop has no way to end, and the program repeats the body forever.

</details>

**6.** What's the difference between `lap < total_laps` and `lap <= total_laps`? Which case in section 7 doesn't reveal it?

<details>
<summary>Example answer</summary>

`lap < total_laps` gives `false` already when `lap` equals `total_laps`, so it skips the last lap: for 3 it prints only two. `<=` also allows equality. For 0, neither version prints anything, so that case doesn't reveal the bug. 1 and 3 reveal it.

</details>

**7.** Why does the counter in the countdown mission get smaller instead of bigger?

<details>
<summary>Example answer</summary>

Because the countdown prints smaller and smaller numbers and ends at the lower limit. Making the counter smaller brings it closer to the value at which the condition stops holding. Making it bigger would move it away from that value, and the loop would never end.

</details>

**8.** What makes the program carry on after the loop ends?

<details>
<summary>Example answer</summary>

When the condition gives `false`, the program skips the body and runs the statements after the loop's closing brace, from top to bottom, as before. The loop doesn't end the program; it only ends the repetition.

</details>

## Summary

- `while (condition) { … }` repeats the loop body while the condition holds.
- The condition is checked **before every** iteration. After running the body, the program goes back to the condition. When the answer is "no", it carries on after the loop.
- A counting loop has four parts: the start value before the loop, the condition, the body, and the counter's change in the body. `while` changes nothing by itself.
- The number of iterations follows from the start value, the condition and the change. The condition is always checked one more time than the body runs: the last check gives `false`.
- A loop can run zero times, when the condition is false from the start.
- The program doesn't leave the body halfway. The condition is checked only after the whole body has run.
- If nothing in the body brings the condition closer to the answer "no", the loop doesn't end. You stop the program with <kbd>Ctrl</kbd> + <kbd>C</kbd> in the terminal, or with the **Stop** button in CLion.
- Test a loop for zero iterations, one, several and the largest acceptable value. An off-by-one error is often revealed by only one of these cases.

## What's next

Your loop already counts iterations. In lesson 4.2 it will learn to **add** another value to a result in each iteration, for example to total the training minutes from several days. **Lesson 4.2 is in preparation.**

---

## Example solutions

Look here **after your own attempt**. Your names may differ, as long as the standard output is as required.

<details>
<summary>Section 4: the trace table for two laps</summary>

| Condition check | `lap` at the check | `lap <= total_laps` | Loop body | `lap` after the body |
|---|---|---|---|---|
| 1 | 1 | `true` | prints `Lap 1`, then `lap = lap + 1;` | 2 |
| 2 | 2 | `true` | prints `Lap 2`, then `lap = lap + 1;` | 3 |
| 3 | 3 | `false` | doesn't run: the loop ends | — |

Three condition checks, two iterations. The program's last line is `Finished, lap is now 3`.

</details>

<details>
<summary>Section 5: zero, one and three iterations</summary>

| `total_laps` | Laps printed | Number of iterations | `lap` after the loop |
|---|---|---|---|
| 0 | none | 0 | 1 |
| 1 | `Lap 1` | 1 | 2 |
| 3 | `Lap 1`, `Lap 2`, `Lap 3` | 3 | 4 |

`lap` after the loop is always 1 greater than the number of laps, because the loop ends at the first value that goes past `total_laps`. The program doesn't print this value. You can see it by temporarily adding a `std::cout` after the loop.

</details>

<details>
<summary>Section 7: the results before the fix, and the fix</summary>

Before the fix, for 0, 1 and 3:

<!-- input: laps_bug -->
```text
0
```

<!-- output: laps_bug -->
```text
Enter number of laps (0-5):
Finished
```

<!-- input: laps_bug -->
```text
1
```

<!-- output: laps_bug -->
```text
Enter number of laps (0-5):
Finished
```

<!-- input: laps_bug -->
```text
3
```

<!-- output: laps_bug -->
```text
Enter number of laps (0-5):
Lap 1
Lap 2
Finished
```

- **The first mismatching case** is 1: the requirement says `Lap 1`, and the program prints no lap. For 3, `Lap 3` is missing.
- **Why 0 wasn't enough:** for zero, both versions of the condition give `false` at the first check (`1 < 0` and `1 <= 0`), so both correctly print nothing. One test wasn't enough.
- **The cause:** `lap < total_laps` is false when `lap` **equals** `total_laps`, so the last lap is skipped. The requirement says "inclusive".
- **The fix:** `while (lap <= total_laps)`. The fixed program is the one from section 5. Its results for 0, 1 and 3 are checked there.

</details>

<details>
<summary>Section 10: the mission, a countdown</summary>

<!-- example: countdown -->
```cpp
#include <iostream>

int main() {
    int length{0};

    std::cout << "Enter countdown length:\n";
    std::cin >> length;

    if (length >= 0 && length <= 5) {
        int count{length};

        while (count >= 1) {
            std::cout << count << "\n";
            count = count - 1;
        }

        std::cout << "Liftoff!\n";
    } else {
        std::cout << "Countdown length must be from 0 to 5\n";
    }
}
```

| Condition check | `count` at the check | `count >= 1` | Loop body | `count` after the body |
|---|---|---|---|---|
| 1 | 3 | `true` | prints `3`, then `count = count - 1;` | 2 |
| 2 | 2 | `true` | prints `2`, then `count = count - 1;` | 1 |
| 3 | 1 | `true` | prints `1`, then `count = count - 1;` | 0 |
| 4 | 0 | `false` | doesn't run: the loop ends | — |

- **Start value:** the first number printed is `N`, so the counter starts from the length that was read.
- **Condition:** the last number printed is 1, so the loop goes on while the counter is at least 1. The condition `count > 0` works the same for whole numbers.
- **Change:** `count = count - 1;` makes the counter smaller and brings it closer to 0, at which the condition gives `false`.
- **`Liftoff!`** is after the loop, so it appears exactly once, including for 0, when the body doesn't run even once.
- Instead of a separate `count` counter, you can make `length` itself smaller. A separate variable keeps the length that was read unchanged, in case it's needed later.

</details>

**Previous lesson:** [Lesson 3.6: The program makes decisions (the Module 3 test)](../module_03_decisions_and_conditions/lesson_06_the_program_decides.en.md) · **Next lesson:** in preparation · [Course overview](../../README.en.md)

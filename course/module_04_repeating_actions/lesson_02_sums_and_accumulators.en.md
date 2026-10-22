# Lesson 4.2: Sums and accumulators

[Polski](lesson_02_sums_and_accumulators.md) · **English** · [Course overview](../../README.en.md)

> **Module 4, lesson 2** · about 70–85 minutes
> **You need:** the `cpp-workspace` folder and the original `lesson_05_first_program` project, as before. You don't need the debugger in this lesson.
> **Pilot version.** The programs in this lesson are checked automatically on Windows, Ubuntu and macOS, including with the given input data.

## Before you start

This lesson assumes that after lesson 4.1:

- you write a `while` loop with a counter: start value, condition, body and the counter's change;
- you trace a loop in a table in which each row is one condition check;
- you know that a loop can run zero times;
- you check a loop for zero, one and several iterations.

## The situation

What is 1 + 2 + 3? That's easy: 6. It's also easy to type `1 + 2 + 3` into a program. But if the user said how far to add, to 10, to 500 or to 1000, you couldn't write that expression in advance.

You can, however, add up the way you do in your head: **step by step**. First you have 0. You add 1 and have 1. You add 2 and have 3. You add 3 and have 6. At each step you remember just one number: the sum so far. Today the loop learns to **build up a result** this way.

After this lesson you'll be able to:

- explain what an accumulator is and how it differs from a counter;
- give an accumulator the right start value and update it in every iteration;
- work out the value of the sum after every iteration;
- write the update more briefly, with `+=`;
- find a bug that resets the sum inside the loop, and explain why one iteration doesn't reveal it;
- add up values read in successive iterations, including `double` values.

## 1. Prepare the project

In `cpp-workspace`, create a `lesson_4_2` folder and copy `main.cpp` and `CMakeLists.txt` into it from the original `lesson_05_first_program`. You type the programs from sections 2–7 into that folder's `main.cpp`.

## 2. A sum, step by step

<!-- example: sum_to_three -->
```cpp
#include <iostream>

int main() {
    int total{0};
    int number{1};

    while (number <= 3) {
        total = total + number;
        number = number + 1;
    }

    std::cout << "Total: " << total << "\n";
}
```

**Predict** what the program will print, then run it.

<details>
<summary>The program's output</summary>

<!-- output: sum_to_three -->
```text
Total: 6
```

</details>

The loop is the same as in lesson 4.1: `number` is a counter that starts at 1, grows by 1, and ends the loop when it goes past 3. What's new is the second variable:

- `number` is **the number added in this iteration**. Its change brings the loop to its end.
- `total` holds **the sum collected so far**.
- `total` gets the start value 0 **before the loop**. Before the first addition nothing has been added up yet, and 0 changes nothing in a sum.
- `total = total + number;` takes the sum **so far**, adds the current number to it, and stores the result back in `total` (lesson 2.2). So every iteration uses the result of the previous one.

A variable that builds up a result over successive iterations is called an **accumulator**. It isn't a new type or a special C++ construct, just an ordinary `int` variable used in a particular way.

## 3. The trace table

The table from lesson 4.1 gets columns for the sum:

| Condition check | `number` | `number <= 3` | `total` before adding | Value added | `total` after adding | `number` after the body |
|---|---|---|---|---|---|---|
| 1 | 1 | `true` | 0 | 1 | 1 | 2 |
| 2 | 2 | `true` | 1 | 2 | 3 | 3 |
| 3 | 3 | `true` | 3 | 3 | 6 | 4 |
| 4 | 4 | `false` | — | — | — | — |

- Row by row, you can see the sum **after each iteration**: 1, then 3, then 6. The value in the "before adding" column is always the "after adding" value from the row above.
- The fourth check gives `false`, because the counter went past the upper limit. It is **not** another iteration: the body doesn't run, and `total` stays 6.

**Your turn.** Imagine the condition says `number <= 4`. Copy the table and fill it in for this case: how many condition checks will there be, what will the sum be after each iteration, and what will the program print? The answer is in [Example solutions](#example-solutions).

## 4. A shorter form: `+=`

An update that says "take the old value, add something and store it back" is so common that C++ has a shorter form for it. In our examples these two lines do the same thing:

<!-- fragment -->
```cpp
total = total + number;
total += number;
```

Read `total += number;` as: **"increase the stored sum by the value of `number`"**.

- `+=` changes the **existing** variable on its left. It doesn't create a new one: `total` must be declared earlier, with a start value.
- `+=` adds whatever value is on its right, not always 1.
- **A note on types.** Initialisation with `{}` rejects narrowing: `int total{2.5};` doesn't build (lesson 2.5). `+=` gives no such protection. If you added a `double` value to an `int` sum, the fractional part would be lost without a compile error. So **choose the accumulator's type to match the values you add**: add whole numbers in an `int`, and values with a fractional part in a `double`.

## 5. The sum from 1 to N

Now the user gives the upper limit. The program accepts N from 0 to 1000. For other numbers it prints a message and doesn't add anything up. We assume the user types a whole number.

<!-- example: sum_to_n -->
```cpp
#include <iostream>

int main() {
    int limit{0};

    std::cout << "Enter N (0-1000):\n";
    std::cin >> limit;

    if (limit >= 0 && limit <= 1000) {
        int total{0};
        int number{1};

        while (number <= limit) {
            total += number;
            number = number + 1;
        }

        std::cout << "Total: " << total << "\n";
    } else {
        std::cout << "N must be from 0 to 1000\n";
    }
}
```

**Predict** the result for N equal to 0, 1, 3 and 4. Write your answers down, then run the program four times, without changing the code.

<!-- input: sum_to_n -->
```text
0
```

<details>
<summary>Standard output for 0</summary>

<!-- output: sum_to_n -->
```text
Enter N (0-1000):
Total: 0
```

The first check, `1 <= 0`, gives `false`: zero iterations. The sum stays equal to its start value, 0. That's the right result: the sum of no numbers is 0.

</details>

<!-- input: sum_to_n -->
```text
1
```

<details>
<summary>Standard output for 1</summary>

<!-- output: sum_to_n -->
```text
Enter N (0-1000):
Total: 1
```

</details>

<!-- input: sum_to_n -->
```text
3
```

<details>
<summary>Standard output for 3</summary>

<!-- output: sum_to_n -->
```text
Enter N (0-1000):
Total: 6
```

</details>

<!-- input: sum_to_n -->
```text
4
```

<details>
<summary>Standard output for 4</summary>

<!-- output: sum_to_n -->
```text
Enter N (0-1000):
Total: 10
```

</details>

**The largest N.** For 1000 the loop runs 1000 iterations, in a fraction of a second. Predict: will the result be larger or smaller than 1,000,000? Then check.

<!-- input: sum_to_n -->
```text
1000
```

<details>
<summary>Standard output for 1000</summary>

<!-- output: sum_to_n -->
```text
Enter N (0-1000):
Total: 500500
```

</details>

**Why the range 0 to 1000?** It keeps the program quick, and its result easy to predict and check. An `int` can't hold arbitrarily large numbers, so for a very large N the sum would no longer fit in it. The largest sum in this range, 500500, fits easily. For a number outside the range, for example 1001, the program takes the `else` branch and never reaches the loop:

<!-- input: sum_to_n -->
```text
1001
```

<details>
<summary>Standard output for 1001</summary>

<!-- output: sum_to_n -->
```text
Enter N (0-1000):
N must be from 0 to 1000
```

</details>

This sum can also be calculated with a formula, without a loop. Here, though, the point is how a loop builds up a result.

## 6. Three roles of variables

In loops you'll often meet three roles:

| Role | What it does | How it changes | Example |
|---|---|---|---|
| **iteration counter** | says which iteration this is, and decides when to stop | by the same amount in every iteration | `number` |
| **accumulator** | builds up a result from the values processed in successive iterations | by the value from the current iteration | `total` |
| **event counter** | counts how many times a particular situation happened | only when that situation happens | `even_count` below |

This program adds up the numbers from 1 to 6 and also counts how many of them are even:

<!-- example: sum_and_evens -->
```cpp
#include <iostream>

int main() {
    const int limit{6};
    int number{1};
    int total{0};
    int even_count{0};

    while (number <= limit) {
        total += number;

        if (number % 2 == 0) {
            even_count += 1;
        }

        number = number + 1;
    }

    std::cout << "Total: " << total << "\n";
    std::cout << "Even numbers: " << even_count << "\n";
}
```

**Predict** both lines of output, then run the program.

<details>
<summary>The program's output</summary>

<!-- output: sum_and_evens -->
```text
Total: 21
Even numbers: 3
```

`total` grows in **every** iteration, by the current number. `even_count` grows by 1 **only** in the iterations with an even number (2, 4 and 6), because its update is in the `if` block. Here `+=` adds 1, because one event increases the counter by one.

</details>

Not every loop needs all three roles. And not every sum comes from the counter: in the next section the values being added come from the user.

## 7. Adding up values from input

A program asks three times for a training time in minutes and adds up the answers. In each iteration it:

1. reads one time;
2. adds it to the sum;
3. changes the iteration counter.

The user types 20, 35 and 15, in that order. **Predict**, without writing the program: copy the table and fill it in.

| Iteration | Time read | Sum before adding | Sum after adding |
|---|---|---|---|
| 1 | | | |
| 2 | | | |
| 3 | | | |

What is the sum at the end? And how does the counter's role differ here from the role of the time that was read? The answer is in [Example solutions](#example-solutions).

## 8. Find the bug: the lost sum

The requirement is the same as in section 5: the program prints the sum of the numbers from 1 to N. In this version, someone added one line:

<!-- example: sum_reset_bug -->
```cpp
#include <iostream>

int main() {
    int limit{0};

    std::cout << "Enter N (0-1000):\n";
    std::cin >> limit;

    if (limit >= 0 && limit <= 1000) {
        int total{0};
        int number{1};

        while (number <= limit) {
            total = 0;
            total += number;
            number = number + 1;
        }

        std::cout << "Total: " << total << "\n";
    } else {
        std::cout << "N must be from 0 to 1000\n";
    }
}
```

1. **Predict** what the program **should** print for N equal to 0, 1 and 3.
2. Predict what **this** program will print. Fill in a trace table for N = 3.
3. Run the program for 0, 1 and 3.
4. Find the first case where the result doesn't match the requirement.
5. Point to the line where the sum so far gets lost.
6. Fix the program.
7. Check all three cases again.

The program's results before the fix, and the fix, are in [Example solutions](#example-solutions). Look there after your own attempt.

## 9. Mission: the total weight of parcels

A warehouse is preparing parcels for shipping. The program asks for the number of parcels, then for the weight of each one in kilograms. After reading all the weights, it prints their total weight.

**Requirements:**

- The number of parcels is a whole number from 0 to 5.
- A parcel's weight is a number with a fractional part, not less than zero.
- The program reads each weight in a separate iteration of the loop, after the prompt `Enter parcel weight:`. The prompt appears once for each parcel.
- The program doesn't need to remember all the weights at once. It's enough to build up their sum.
- For 0 parcels the program asks for no weight and prints a sum of 0.
- For a number of parcels outside the range, the program prints only `Invalid parcel count` and asks for no weight.
- We assume the user types numbers and, for an acceptable number of parcels, gives all the weights. The program is **not** robust against other data, for example text instead of a number. That comes in later lessons.

In `cpp-workspace`, create a `parcel_weights` folder, copy `CMakeLists.txt` into it from the original `lesson_05_first_program`, create an empty `main.cpp` and write the program on your own.

For three parcels weighing 1.25, 2.5 and 0.75, standard output must be:

<!-- input: parcel_weights -->
```text
3
1.25
2.5
0.75
```

<!-- output: parcel_weights -->
```text
Enter parcel count:
Enter parcel weight:
Enter parcel weight:
Enter parcel weight:
Total weight: 4.5 kg
```

For 0 parcels:

<!-- input: parcel_weights -->
```text
0
```

<!-- output: parcel_weights -->
```text
Enter parcel count:
Total weight: 0 kg
```

**This isn't the sum from 1 to N.** There, the values added were the counter's successive values. Here the counter only says **how many** parcels to handle, and the values added come separately, from standard input, and are `double`s. The counter and the weight being added are two different variables with different roles. You have to decide on your own:

1. what start value the accumulator has, and where to declare it;
2. how to read one weight in each iteration and add it to the sum;
3. how to change the counter, and when to stop reading;
4. what the program does for zero parcels.

**Before you write the program**, prepare two things:

- a trace table for the three parcels in the example: the weight read, the sum before adding and the sum after adding;
- a table of test cases: zero parcels, one parcel, several parcels, the largest acceptable number of parcels, and the numbers just outside the range on both sides. Write down the expected standard output for each case, including the number of weight prompts.

### Success criteria

- The program builds as C++20, and its standard output for both examples is exactly as above.
- For every number of parcels from 0 to 5, the program asks for a weight exactly as many times as there are parcels, and prints their sum. For any other number it prints only `Invalid parcel count`.
- The sum is built up in an accumulator of type `double`, declared with a start value and updated in every iteration.
- The parcel counter and the weight read are separate variables.
- The `while` loop has braces, and the range of the number of parcels is checked before the program starts reading weights.
- The trace table and the table of cases were made before running the program.
- You can explain why for zero parcels the sum is 0 and the program doesn't ask for a weight.

When the result matches, you can save the project in Git, as in lesson 1.5.

<details>
<summary>Hint 1</summary>

Think about which value means that no weight has been collected yet.

</details>

<details>
<summary>Hint 2</summary>

Keep the variable that says which parcel this is separate from the variable that holds the sum.

</details>

<details>
<summary>Hint 3</summary>

Each iteration of the loop should read one weight and change the total sum.

</details>

<details>
<summary>The full list of control cases: open after preparing your own table</summary>

| Number of parcels | Weights | Weight prompts | Last line | What it checks |
|---|---|---|---|---|
| 3 | 1.25, 2.5, 0.75 | 3 | `Total weight: 4.5 kg` | several iterations |
| 0 | — | 0 | `Total weight: 0 kg` | zero iterations |
| 1 | 1.25 | 1 | `Total weight: 1.25 kg` | one iteration |
| 5 | 0.5, 1.25, 2, 0.75, 3 | 5 | `Total weight: 7.5 kg` | the largest acceptable number of parcels |
| -1 | — | 0 | `Invalid parcel count` | just below the range |
| 6 | — | 0 | `Invalid parcel count` | just above the range |

The cases with three and zero parcels are checked above, in the mission's description. The weights were chosen so that the sums can be written exactly, without rounding.

<!-- input: parcel_weights -->
```text
1
1.25
```

<!-- output: parcel_weights -->
```text
Enter parcel count:
Enter parcel weight:
Total weight: 1.25 kg
```

<!-- input: parcel_weights -->
```text
5
0.5
1.25
2
0.75
3
```

<!-- output: parcel_weights -->
```text
Enter parcel count:
Enter parcel weight:
Enter parcel weight:
Enter parcel weight:
Enter parcel weight:
Enter parcel weight:
Total weight: 7.5 kg
```

<!-- input: parcel_weights -->
```text
-1
```

<!-- output: parcel_weights -->
```text
Enter parcel count:
Invalid parcel count
```

<!-- input: parcel_weights -->
```text
6
```

<!-- output: parcel_weights -->
```text
Enter parcel count:
Invalid parcel count
```

</details>

### Optional variant: heavy parcels

This variant isn't required. The program should also count how many parcels weigh **at least 2 kg**, and after the total weight line print `Heavy parcels: K`. You need a separate event counter and an `if`, as in section 6. Predict the result for the five parcels from the control list, then check.

<details>
<summary>The variant's cases: open after your own attempt</summary>

<!-- input: parcel_weights_heavy -->
```text
5
0.5
1.25
2
0.75
3
```

<!-- output: parcel_weights_heavy -->
```text
Enter parcel count:
Enter parcel weight:
Enter parcel weight:
Enter parcel weight:
Enter parcel weight:
Enter parcel weight:
Total weight: 7.5 kg
Heavy parcels: 2
```

<!-- input: parcel_weights_heavy -->
```text
3
1.25
2.5
0.75
```

<!-- output: parcel_weights_heavy -->
```text
Enter parcel count:
Enter parcel weight:
Enter parcel weight:
Enter parcel weight:
Total weight: 4.5 kg
Heavy parcels: 1
```

<!-- input: parcel_weights_heavy -->
```text
0
```

<!-- output: parcel_weights_heavy -->
```text
Enter parcel count:
Total weight: 0 kg
Heavy parcels: 0
```

A parcel weighing exactly 2 kg counts, because the requirement says "at least".

</details>

Example solutions are in [Example solutions](#example-solutions).

## 10. When something goes differently

| What you see | What it means | What to do |
|---|---|---|
| The printed sum is only the last value | The accumulator is reset in the loop body, so every iteration starts afresh. | Set the start value once, before the loop (section 8). |
| `use of undeclared identifier` for the sum after the loop | The accumulator is declared in the loop body, so it no longer exists after the loop (lesson 3.2). | Declare it before the loop. |
| The sum is one value too small or too large | An off-by-one error in the condition or in the counter's start value. | Check the cases with one iteration and with the largest value. Fill in a trace table. |
| The sum of the weights has no fractional part | The accumulator or the weight variable is an `int`. | Keep the weight and the sum of weights in `double`s. |
| The weight prompt appears too many or too few times | The read is outside the loop, or the counter changes wrongly. | The read and the weight prompt must be in the loop body, once per iteration. |
| For zero parcels the program waits for data | The program reads a weight before the loop or outside it. | For zero parcels the loop body doesn't run even once, so no weight read may be outside it. |
| The program does nothing and waits | It's waiting for another weight: fewer weights were typed than there are parcels. | Type the missing weights and press **Enter**. |

## 11. Explain

Answer in your own words, preferably in writing. Only then compare with the example answer.

**1.** What is an accumulator, and why does it usually start at 0?

<details>
<summary>Example answer</summary>

It's an ordinary variable that builds up a result over successive iterations, here a sum. Before the first iteration nothing has been added up yet, and 0 changes nothing in a sum. That's why the result for zero iterations is 0.

</details>

**2.** How does an iteration counter differ from an accumulator?

<details>
<summary>Example answer</summary>

The counter says which iteration this is, and decides when the loop ends. It changes by the same amount in every iteration. The accumulator builds up a result, and changes by the value from the current iteration, for example by the weight that was read.

</details>

**3.** What does `total += number;` do?

<details>
<summary>Example answer</summary>

It increases the value of the existing variable `total` by the value of `number`. In our examples it does the same as `total = total + number;`.

</details>

**4.** Why did the program in section 8 give the right result for N equal to 1, but the wrong one for 3?

<details>
<summary>Example answer</summary>

Because the reset in the loop body wipes out the sum from the previous iterations. With one iteration there's nothing to wipe out: 0 + 1 is the right result. The bug shows only with several iterations, when the result should depend on earlier additions.

</details>

**5.** What's the difference between `int total{0};` before the loop and `total = 0;` in its body?

<details>
<summary>Example answer</summary>

The start value before the loop sets the sum once, before collecting begins. The assignment in the loop body runs in every iteration, and each time throws away what has been collected.

</details>

**6.** Why do you keep the sum of the weights in a `double` in the mission?

<details>
<summary>Example answer</summary>

Because the weights have a fractional part. An `int` sum would lose that part, and `+=` wouldn't report an error the way initialisation with `{}` does.

</details>

**7.** Why doesn't the program ask for a weight when there are zero parcels?

<details>
<summary>Example answer</summary>

Because the weight read is in the loop body, and for zero parcels the condition is false already at the first check. The body doesn't run even once, and the sum stays equal to its start value, 0.

</details>

## Summary

- An **accumulator** is an ordinary variable that builds up a result over successive iterations, for example a sum.
- An accumulator gets its start value **before the loop**. For a sum it's 0: the result for zero iterations.
- In each iteration the accumulator changes based on its value so far: `total = total + number;`, or more briefly `total += number;`.
- `+=` increases an existing variable by the value on the right. It doesn't protect against narrowing, so choose the accumulator's type to match the values you add.
- The **iteration counter** decides when to stop, the **accumulator** builds up the result, and an **event counter** grows only when a particular situation happens.
- The values added don't have to come from the counter. They can come from standard input, one per iteration.
- Resetting the accumulator in the loop body loses the earlier result. Only a test with several iterations reveals such a bug, not a test with one.

## What's next

The loops in this lesson and in lesson 4.1 always have the same parts: a counter with a start value, a condition, and the counter's change at the end of the body. In lesson 4.3 you'll meet the `for` loop, which gathers these three parts into one line. **Lesson 4.3 is in preparation.**

---

## Example solutions

Look here **after your own attempt**. Your names may differ, as long as the standard output is as required.

<details>
<summary>Section 3: the trace table for the numbers from 1 to 4</summary>

| Condition check | `number` | `number <= 4` | `total` before adding | Value added | `total` after adding | `number` after the body |
|---|---|---|---|---|---|---|
| 1 | 1 | `true` | 0 | 1 | 1 | 2 |
| 2 | 2 | `true` | 1 | 2 | 3 | 3 |
| 3 | 3 | `true` | 3 | 3 | 6 | 4 |
| 4 | 4 | `true` | 6 | 4 | 10 | 5 |
| 5 | 5 | `false` | — | — | — | — |

Five condition checks, four iterations. The program prints `Total: 10`.

</details>

<details>
<summary>Section 7: three training times</summary>

| Iteration | Time read | Sum before adding | Sum after adding |
|---|---|---|---|
| 1 | 20 | 0 | 20 |
| 2 | 35 | 20 | 55 |
| 3 | 15 | 55 | 70 |

The sum at the end is 70 minutes. The counter only says which iteration this is, and when to stop after the third. What goes into the sum is **the times that were read**, not the counter's values.

</details>

<details>
<summary>Section 8: the results before the fix, and the fix</summary>

Before the fix, for 0, 1 and 3:

<!-- input: sum_reset_bug -->
```text
0
```

<!-- output: sum_reset_bug -->
```text
Enter N (0-1000):
Total: 0
```

<!-- input: sum_reset_bug -->
```text
1
```

<!-- output: sum_reset_bug -->
```text
Enter N (0-1000):
Total: 1
```

<!-- input: sum_reset_bug -->
```text
3
```

<!-- output: sum_reset_bug -->
```text
Enter N (0-1000):
Total: 3
```

| Condition check | `number` | `number <= 3` | `total` after `total = 0;` | `total` after adding |
|---|---|---|---|---|
| 1 | 1 | `true` | 0 | 1 |
| 2 | 2 | `true` | 0 | 2 |
| 3 | 3 | `true` | 0 | 3 |
| 4 | 4 | `false` | — | — |

- **The first mismatching case** is 3: the requirement says 6, and the program prints 3, i.e. only the last number added.
- **Why 0 and 1 weren't enough:** for 0 the loop doesn't run, and for one iteration the reset has nothing to wipe out. Both results are right, even though the program is wrong.
- **The cause:** `total = 0;` in the loop body runs in every iteration and throws away the sum from the previous iterations.
- **The fix:** remove that line. The sum gets its start value 0 once, before the loop, in the declaration `int total{0};`. The fixed program is the one from section 5. Its results for 0, 1 and 3 are checked there.

</details>

<details>
<summary>Section 9: the mission, the total weight of parcels</summary>

<!-- example: parcel_weights -->
```cpp
#include <iostream>

int main() {
    int parcel_count{0};

    std::cout << "Enter parcel count:\n";
    std::cin >> parcel_count;

    if (parcel_count >= 0 && parcel_count <= 5) {
        double total_weight{0.0};
        int parcel{1};

        while (parcel <= parcel_count) {
            double weight{0.0};

            std::cout << "Enter parcel weight:\n";
            std::cin >> weight;
            total_weight += weight;
            parcel = parcel + 1;
        }

        std::cout << "Total weight: " << total_weight << " kg\n";
    } else {
        std::cout << "Invalid parcel count\n";
    }
}
```

| Condition check | `parcel` | `parcel <= 3` | Weight read | `total_weight` before | `total_weight` after |
|---|---|---|---|---|---|
| 1 | 1 | `true` | 1.25 | 0 | 1.25 |
| 2 | 2 | `true` | 2.5 | 1.25 | 3.75 |
| 3 | 3 | `true` | 0.75 | 3.75 | 4.5 |
| 4 | 4 | `false` | — | — | — |

- **The accumulator** `total_weight` is a `double` and starts at 0.0, before the loop. For zero parcels it stays 0, and `std::cout` prints it as `0`.
- **The counter** `parcel` only says which parcel the iteration handles. What goes into the sum is **the weight that was read**, not the counter.
- **The read** is in the loop body, so the weight prompt appears exactly once per parcel, and not at all for zero parcels.
- `weight` is declared in the loop body, because it's needed only within one iteration. You can also declare it before the loop: the result is the same.

</details>

<details>
<summary>Section 9: the variant, heavy parcels</summary>

<!-- example: parcel_weights_heavy -->
```cpp
#include <iostream>

int main() {
    int parcel_count{0};

    std::cout << "Enter parcel count:\n";
    std::cin >> parcel_count;

    if (parcel_count >= 0 && parcel_count <= 5) {
        double total_weight{0.0};
        int heavy_parcels{0};
        int parcel{1};

        while (parcel <= parcel_count) {
            double weight{0.0};

            std::cout << "Enter parcel weight:\n";
            std::cin >> weight;
            total_weight += weight;

            if (weight >= 2.0) {
                heavy_parcels += 1;
            }

            parcel = parcel + 1;
        }

        std::cout << "Total weight: " << total_weight << " kg\n";
        std::cout << "Heavy parcels: " << heavy_parcels << "\n";
    } else {
        std::cout << "Invalid parcel count\n";
    }
}
```

`heavy_parcels` is an event counter: it grows by 1 only when the weight that was read is at least 2 kg.

</details>

**Previous lesson:** [Lesson 4.1: The first loop (`while`)](lesson_01_the_first_loop.en.md) · **Next lesson:** in preparation · [Course overview](../../README.en.md)

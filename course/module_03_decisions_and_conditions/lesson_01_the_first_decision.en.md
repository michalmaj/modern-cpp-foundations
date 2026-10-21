# Lesson 3.1: The program's first decision (`if`)

[Polski](lesson_01_the_first_decision.md) · **English** · [Course overview](../../README.en.md)

> **Module 3, lesson 1** · about 60 minutes
> **You need:** the `cpp-workspace` folder and the original `lesson_05_first_program` project, as before. You don't need the debugger in this lesson.
> **Pilot version.** The programs in this lesson are checked automatically on Windows, Ubuntu and macOS, including with the given input data.

## Before you start

This lesson assumes that after Module 2:

- you read `int` and `double` numbers with `std::cin`, and run the same program with different data;
- you tell input data apart from the program's standard output;
- you predict a program's output before you run it.

## The situation

So far, every program has executed all of its statements, one after another, always in the same way. Real programs often do something **only when** a condition holds: they warn when seats are running out, or add a fee when a bag is too heavy. Today, for the first time, a program will make a decision: **it will execute some statements or skip them, depending on the data**.

After this lesson you will:

- explain what `if` is for;
- compare two values with the operators `<`, `<=`, `>` and `>=`;
- predict whether a condition is satisfied, and which statements will run;
- recognise which statements belong to an `if` block and which always run;
- write your own simple `if`, always with braces;
- check a program with values right at a limit, and find a `<` that should be `<=`.

## 1. Prepare the project

In `cpp-workspace`, create a folder `lesson_3_1` and copy `main.cpp` and `CMakeLists.txt` into it from the original `lesson_05_first_program`. You type the programs from sections 2–6 into that folder's `main.cpp`.

## 2. Seats are running out

The program gets the number of free seats in a room. If **fewer than 5** are left, it must print an extra warning. At the end it always prints that the check is finished:

<!-- example: seats_check -->
```cpp
#include <iostream>

int main() {
    int seats_left{0};

    std::cout << "Enter seats left:\n";
    std::cin >> seats_left;

    if (seats_left < 5) {
        std::cout << "Few seats left\n";
    }

    std::cout << "Check complete\n";
}
```

Before you run the program, **answer in writing**:

1. What does the program print when 3 seats are free?
2. And when 12 are free?
3. And when exactly 5 are free?
4. Does `Check complete` appear in each of these cases?

Now run the program three times, without changing the code, and type `3`, `12` and `5` in turn.

<!-- input: seats_check -->
```text
3
```

<details>
<summary>The standard output for 3</summary>

<!-- output: seats_check -->
```text
Enter seats left:
Few seats left
Check complete
```

</details>

<!-- input: seats_check -->
```text
12
```

<details>
<summary>The standard output for 12</summary>

<!-- output: seats_check -->
```text
Enter seats left:
Check complete
```

</details>

<!-- input: seats_check -->
```text
5
```

<details>
<summary>The standard output for 5</summary>

<!-- output: seats_check -->
```text
Enter seats left:
Check complete
```

</details>

**What happened, line by line?**

- `if` **makes a decision**: whether to execute the following statements or skip them.
- The parentheses hold a **condition**: `seats_left < 5`. The program checks it with the current value of the variable, the one it has just read.
- `<` **compares** two values: is the left one smaller than the right one? A comparison gives the answer **yes** or **no**.
- The braces `{ }` mark the **block** of statements that belong to the `if`.
- The block runs **only when the answer is "yes"**. For 3 it is (3 is smaller than 5), so `Few seats left` appears. For 12 and for 5 the answer is "no", so the program **skips** the whole block.
- `std::cout << "Check complete\n";` comes **after** the closing brace, so it doesn't belong to the `if`. It always runs.

`if` doesn't stop the program when the condition isn't satisfied. The program simply **jumps over the block** and carries on with what comes after it, top to bottom, as before.

**Why didn't 5 trigger the warning?** 5 isn't smaller than 5. The condition `seats_left < 5` is satisfied for 4, 3, 2 and smaller numbers, but not for 5. We'll come back to this in section 6.

## 3. Braces and indentation

Every `if` in this course looks the same: a condition in parentheses, followed by a block in braces.

<!-- fragment -->
```cpp
if (seats_left < 5) {
    std::cout << "Few seats left\n";
}
```

- The statements inside the block are **indented**, that is, shifted to the right, like the statements in `main`. Indentation helps you see what belongs to the `if`, but the **braces** decide it, not the indentation.
- In C++ you can also write an `if` without braces when there is only one statement inside. **In this course we always use braces**, even around a single statement: you can see at once where the block ends, and adding another statement to the block won't silently change how the program works.
- There is no semicolon after `if (…)`. The block in braces is part of the same construct.

## 4. Four comparisons

Besides `<`, you already know three similar comparisons from maths. In C++ you write them like this:

| Operator | Meaning | Example | When the answer is "yes" |
|---|---|---|---|
| `<` | less than | `seats_left < 5` | fewer than 5 seats are free |
| `<=` | less than or equal to | `temperature_c <= 25` | the temperature doesn't exceed 25 degrees |
| `>` | greater than | `weight_kg > 20.0` | the bag exceeds 20 kg |
| `>=` | greater than or equal to | `points >= 50` | the score has reached the required minimum of 50 points |

- `<=` and `>=` are written with two characters, without a space between them, with `=` second.
- The difference between `<` and `<=` (and between `>` and `>=`) concerns **only the limit itself**. For 25, the condition `temperature_c <= 25` is satisfied, while `temperature_c < 25` isn't.
- You can compare `int` and `double` numbers, as in the luggage example.

**Predict.** Copy the table and write whether each condition is satisfied (yes or no):

| Condition | for the value 49 | for 50 | for 51 |
|---|---|---|---|
| `points >= 50` | | | |
| `points > 50` | | | |
| `points < 50` | | | |
| `points <= 50` | | | |

The answers are in [Example solutions](#example-solutions).

## 5. Before the block, in the block, after the block

This program prints something before the `if`, something in the `if` block, and something after it:

<!-- example: hot_day -->
```cpp
#include <iostream>

int main() {
    int temperature_c{0};

    std::cout << "Enter temperature:\n";
    std::cin >> temperature_c;

    std::cout << "Checking temperature\n";

    if (temperature_c > 30) {
        std::cout << "Hot day: drink water\n";
    }

    std::cout << "Have a nice day\n";
}
```

**Predict** which lines appear for a temperature of `25` and which for `32`. Write them down, then run the program twice.

<!-- input: hot_day -->
```text
25
```

<details>
<summary>The standard output for 25</summary>

<!-- output: hot_day -->
```text
Enter temperature:
Checking temperature
Have a nice day
```

</details>

<!-- input: hot_day -->
```text
32
```

<details>
<summary>The standard output for 32</summary>

<!-- output: hot_day -->
```text
Enter temperature:
Checking temperature
Hot day: drink water
Have a nice day
```

</details>

The lines before and after the block always appear. The line in the block appears only when the condition is satisfied.

**Change it.** The warning should now appear **from 25 degrees inclusive**. Change the condition: both the operator and the number. Then **predict** the result for `24` and `25`, and check both cases. An example change is in [Example solutions](#example-solutions).

If the debugger has worked for you since lesson 2.3, you can set a breakpoint on the line with `if` and click **Step Over**: you'll see whether the next highlighted line is the statement in the block or the one after it. That's an extra option. Predicting, running, comparing and explaining is enough.

## 6. Find the bug: exactly at the limit

The organisers changed the requirement:

> Show a warning if **5 or fewer** seats are free.

But the program still has the old condition:

<!-- example: seats_limit_bug -->
```cpp
#include <iostream>

int main() {
    int seats_left{0};

    std::cout << "Enter seats left:\n";
    std::cin >> seats_left;

    if (seats_left < 5) {
        std::cout << "Few seats left\n";
    }

    std::cout << "Check complete\n";
}
```

1. Read the requirement and **predict** what the program **should** print for `4`, `5` and `6`.
2. Run the program for these three values.
3. Find the case in which the output doesn't meet the requirement.
4. Fix the condition.
5. Check **all three** cases again.

The test data is three separate runs: `4`, `5` and `6`.

The program's output before the fix, and the fixed program, are in [Example solutions](#example-solutions). Look there after your own attempt.

**Why wouldn't 3 and 12 have found it?** For 3 both versions of the condition, `< 5` and `<= 5`, answer "yes", and for 12 both answer "no". These values lie far from the limit, so both versions behave the same. They differ **only for 5**. That's why you should always check a condition **exactly at the limit** too, and right next to it: one less and one more.

## 7. Mission: the luggage weight limit

At the airport, every bag is weighed before check-in. The limit is 20 kg. If a bag **exceeds** 20 kg, the program prints an extra warning. At the end it always prints that the check is finished.

In `cpp-workspace`, create a folder `luggage_check`, copy `CMakeLists.txt` into it from the original `lesson_05_first_program`, create an empty `main.cpp`, and write the program on your own. The program reads one value: the bag's weight in kilograms, a number with a fractional part.

For the weight `19.5`, the standard output must be:

<!-- input: luggage_check -->
```text
19.5
```

<!-- output: luggage_check -->
```text
Enter luggage weight in kg:
Luggage check complete
```

For `20.0`:

<!-- input: luggage_check -->
```text
20.0
```

<!-- output: luggage_check -->
```text
Enter luggage weight in kg:
Luggage check complete
```

For `20.5`:

<!-- input: luggage_check -->
```text
20.5
```

<!-- output: luggage_check -->
```text
Enter luggage weight in kg:
Overweight: extra fee required
Luggage check complete
```

### Success criteria

- The program builds as C++20, and its standard output for `19.5`, `20.0` and `20.5` is exactly as above.
- The bag's weight is a `double` variable with a starting value, and the 20 kg limit appears in the program only once, as a constant.
- The warning is in the `if` block, and the final message is after the block. The `if` has braces.
- The same program gives all three results, without changing the code.
- The program uses only what you already know, plus `if` and the comparisons from this lesson.
- You can explain why a bag of exactly 20 kg doesn't trigger the warning.

Once the output matches, you can save the project in Git, as in lesson 1.5.

<details>
<summary>Hint 1</summary>

The requirement says "exceeds 20 kg". Does 20 kg exceed 20 kg? Which of the four operators answers the question "is it more than"?

</details>

<details>
<summary>Hint 2</summary>

The order is as in section 2: the variable and the constant, the request and the read, the `if` with the warning in its block, and finally, after the brace, the message that always appears.

</details>

An example solution is in [Example solutions](#example-solutions).

## 8. When something goes differently

| What you see | What it means | What to do |
|---|---|---|
| The warning always appears, or never | The condition doesn't match the requirement, for example it has the opposite sign (`>` instead of `<`). | Read the condition aloud: "if … is less than …". Check a value for which the answer should be "yes". |
| The program works for values far from the limit, but goes wrong exactly at it | `<` was confused with `<=`, or `>` with `>=`. | Check the limit itself and the values right next to it (section 6). |
| A message that should always appear appears only sometimes | It is inside the block, before the closing brace. | Move it after `}`. |
| The warning appears although the condition isn't satisfied | The warning is outside the block, after `}`. | A statement that should depend on the condition must stand between `{` and `}`. |
| A compile error at `if` | Usually a parenthesis or a brace is missing. | The condition goes in `( )`, the block in `{ }`. Every parenthesis and every brace has its pair. |
| `=<` or `= <` instead of `<=` | The operator is written with two characters, in the order `<=` (or `>=`), without a space. | Fix it to `<=` or `>=`. |

## 9. Explain

Answer in your own words, preferably in writing. Only then compare with the example answer.

**1.** What does the program do when the condition in an `if` isn't satisfied?

<details>
<summary>Example answer</summary>

It skips the block in braces and carries on with the statements after the closing brace. The program doesn't stop.

</details>

**2.** How do you know which statements belong to an `if` block?

<details>
<summary>Example answer</summary>

The statements between `{` and `}` after the condition belong to it. Indentation helps you see them, but the braces decide what belongs.

</details>

**3.** How do `seats_left < 5` and `seats_left <= 5` differ? For which values do they give different answers?

<details>
<summary>Example answer</summary>

`<` means "less than", and `<=` "less than or equal to". They give different answers only for 5: `5 < 5` is "no", and `5 <= 5` is "yes".

</details>

**4.** Why wasn't checking the program only for 3 and 12 enough to find the bug in section 6?

<details>
<summary>Example answer</summary>

Because for 3 and 12 the wrong and the correct condition give the same answer. They differ only at the limit itself, for 5. You have to check the limit and the values right next to it.

</details>

**5.** Why doesn't a bag of exactly 20 kg trigger the warning in the mission?

<details>
<summary>Example answer</summary>

Because the requirement says "exceeds 20 kg", and 20 isn't greater than 20. The condition `>` answers "no" for 20. The warning appears only for values greater than 20, for example 20.5.

</details>

## Summary

- `if (condition) { … }` runs the block only when the condition is satisfied. Otherwise the program skips the block and carries on. It doesn't stop.
- Statements after the closing brace don't belong to the `if` and always run.
- The comparisons `<`, `<=`, `>` and `>=` give the answer "yes" or "no", using the current values of the variables.
- `<` and `<=` (and likewise `>` and `>=`) differ only at the limit itself. That's why you check a program exactly at the limit and right next to it.
- In this course an `if` always has braces, and the statements in the block are indented.

## What's next

Your program can now do something or skip it. In lesson 3.2 it will learn to choose **one of two ways**, and to check whether values are equal. You'll also learn the name of the "yes" or "no" answer that a comparison gives: [Lesson 3.2: Two possibilities (`else`), equality and `bool`](lesson_02_two_ways.en.md).

---

## Example solutions

Look here **after your own attempt**. Your names may differ, as long as the standard output is as required.

<details>
<summary>Section 4: four comparisons</summary>

| Condition | for 49 | for 50 | for 51 |
|---|---|---|---|
| `points >= 50` | no | yes | yes |
| `points > 50` | no | no | yes |
| `points < 50` | yes | no | no |
| `points <= 50` | yes | yes | no |

At the limit, for 50, the answer depends on whether the operator contains `=`.

</details>

<details>
<summary>Section 5: the warning from 25 degrees inclusive</summary>

<!-- example: hot_day_changed -->
```cpp
#include <iostream>

int main() {
    int temperature_c{0};

    std::cout << "Enter temperature:\n";
    std::cin >> temperature_c;

    std::cout << "Checking temperature\n";

    if (temperature_c >= 25) {
        std::cout << "Hot day: drink water\n";
    }

    std::cout << "Have a nice day\n";
}
```

<!-- input: hot_day_changed -->
```text
24
```

<!-- output: hot_day_changed -->
```text
Enter temperature:
Checking temperature
Have a nice day
```

<!-- input: hot_day_changed -->
```text
25
```

<!-- output: hot_day_changed -->
```text
Enter temperature:
Checking temperature
Hot day: drink water
Have a nice day
```

"From 25 inclusive" is `>= 25`. The condition `> 24` would give the same results for whole numbers, but `>= 25` says exactly what the requirement says.

</details>

<details>
<summary>Section 6: the output before the fix, and the fixed program</summary>

Before the fix, for `4`, `5` and `6`:

<!-- input: seats_limit_bug -->
```text
4
```

<!-- output: seats_limit_bug -->
```text
Enter seats left:
Few seats left
Check complete
```

<!-- input: seats_limit_bug -->
```text
5
```

<!-- output: seats_limit_bug -->
```text
Enter seats left:
Check complete
```

<!-- input: seats_limit_bug -->
```text
6
```

<!-- output: seats_limit_bug -->
```text
Enter seats left:
Check complete
```

For 5 the warning is missing, although the requirement says "5 or fewer". The condition `seats_left < 5` doesn't include 5 itself. The fix is `<=`:

<!-- example: seats_limit_fixed -->
```cpp
#include <iostream>

int main() {
    int seats_left{0};

    std::cout << "Enter seats left:\n";
    std::cin >> seats_left;

    if (seats_left <= 5) {
        std::cout << "Few seats left\n";
    }

    std::cout << "Check complete\n";
}
```

After the fix, for `4`, `5` and `6`:

<!-- input: seats_limit_fixed -->
```text
4
```

<!-- output: seats_limit_fixed -->
```text
Enter seats left:
Few seats left
Check complete
```

<!-- input: seats_limit_fixed -->
```text
5
```

<!-- output: seats_limit_fixed -->
```text
Enter seats left:
Few seats left
Check complete
```

<!-- input: seats_limit_fixed -->
```text
6
```

<!-- output: seats_limit_fixed -->
```text
Enter seats left:
Check complete
```

</details>

<details>
<summary>Section 7: mission, the luggage weight limit</summary>

<!-- example: luggage_check -->
```cpp
#include <iostream>

int main() {
    const double weight_limit_kg{20.0};
    double luggage_weight_kg{0.0};

    std::cout << "Enter luggage weight in kg:\n";
    std::cin >> luggage_weight_kg;

    if (luggage_weight_kg > weight_limit_kg) {
        std::cout << "Overweight: extra fee required\n";
    }

    std::cout << "Luggage check complete\n";
}
```

- The weight can have a fractional part, so it is a `double`. The limit doesn't change, so it is a `const double` constant.
- "Exceeds 20 kg" is `>`: for 20.0 the answer is "no", for 20.5 "yes".
- The final message comes after the closing brace, so it always appears.

</details>

**Previous lesson:** [Lesson 2.8: From data to result (the Module 2 test)](../module_02_values_and_calculations/lesson_08_from_data_to_result.en.md) · **Next lesson:** [Lesson 3.2: Two possibilities (`else`), equality and `bool`](lesson_02_two_ways.en.md) · [Course overview](../../README.en.md)

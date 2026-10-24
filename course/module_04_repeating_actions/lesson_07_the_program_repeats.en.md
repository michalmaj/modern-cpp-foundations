# Lesson 4.7: The program repeats actions (the Module 4 test)

[Polski](lesson_07_the_program_repeats.md) · **English** · [Course overview](../../README.en.md)

> **Module 4, lesson 7: the test** · about 100–120 minutes, can be split into two sessions
> **You need:** the `cpp-workspace` folder and the original `lesson_05_first_program` project.
> **Pilot version.** The reference solutions in this lesson are checked automatically on Windows, Ubuntu and macOS, with the given input data. Nothing grades your work automatically: you check it yourself, against the criteria.

## How this test works

This lesson introduces nothing new. You check whether you can design a program on your own that reads data repeatedly, builds up a result step by step, and ends correctly: after collecting all the data, but also when the data runs out early. You also fix two short programs with bugs, analyse a third one without running it, and explain your decisions.

The lesson has two parts:

- **Part A: the test.** Requirements, test data, expected results, tasks, questions and criteria. No hints and no solution code. Everything you need, you know from Modules 1–4.
- **Part B: checking and discussion.** Hints, full lists of control cases, example solutions, explanations and a self-assessment. Go there after finishing part A, or when you knowingly decide to stop trying on your own.

Looking at part B, at earlier lessons or at your notes is not a failure. What matters is **honestly noting what was done on your own and what was done with help**. A suggested split into two sessions:

- **first:** designing, writing and basic testing of the program in task 1;
- **second:** tasks 2 and 3, boundary cases, comparing with the solution, the questions and the self-assessment.

**You can use:** CLion or the terminal, CMake and Ninja, as before; the `CMakeLists.txt` copied from the original `lesson_05_first_program`; trace tables, tables of cases, and temporary `std::cout` statements. You don't need the debugger. You don't have to end the data from the keyboard: the programs are checked on data that ends by itself.

---

# Part A: the test

## Task 1: A measurement station

A simple station records temperatures. First the user gives how many measurements need to be collected. Then the program reads successive temperatures in degrees Celsius. After collecting the required number of **valid** measurements, it prints a report: the number of measurements, the average temperature, and the number of measurements below zero.

**Setup:** in `cpp-workspace`, create a `measurement_station` folder, copy `CMakeLists.txt` into it from the original `lesson_05_first_program`, create an **empty** `main.cpp` and write the whole program on your own.

**The number of measurements:**

- The program asks `Enter measurement count (1-24):` and reads a whole number. Values from 1 to 24 inclusive are acceptable.
- For a number outside the range, it prints `Measurement count out of range` and asks again.
- After a badly written number, it prints `Invalid integer input, try again`, recovers the input as in lesson 4.6, and asks again.
- If the data runs out before the number of measurements is settled, it prints only `Input ended` and ends.
- It moves on to the measurements only once the number of measurements is settled.

**Temperatures:**

- For each attempt the program asks `Enter temperature:` and reads a number with a fractional part.
- In this task, temperatures from -20 to 40 degrees inclusive are acceptable. That's a requirement of the scenario, not the range of the `double` type or of all temperatures in the world.
- For a temperature outside the range, it prints `Temperature out of range` and asks again.
- After a badly written number, it prints `Invalid temperature input, try again`, recovers the input and asks again.
- A rejected temperature and a bad entry don't change the sum, the number of measurements collected, or the number of measurements below zero.
- A temperature of exactly 0 **isn't** a temperature below zero.

**The ending:**

- After collecting all the required measurements, the program doesn't ask for another temperature, and prints three lines: `Measurements recorded: N`, `Average temperature: X` and `Below freezing: N`.
- If the data runs out earlier, it prints only `Input ended: N of M measurements recorded`, i.e. how many valid measurements it collected and how many were required. It doesn't compute the average then. That's a deliberate rule of this program: the report is about a complete set.
- After the end of the data, the program doesn't try to read further. It ends normally.
- It prints the average the default way, with `std::cout`, without extra formatting.

The program doesn't need to remember all the temperatures. Nor does it check whole lines: it recovers the input after a failed read, as in lesson 4.6, but it doesn't verify that the whole entry is a correctly written number. In lesson 4.6, reading `12abc` into an `int` variable gave the number 12. The temperature, however, is a `double`, and you shouldn't assume the same result for it: an entry such as `12abc` isn't necessarily read as 12. The standard libraries on different systems may treat it differently.

**The first example:** a count of 4 measurements, temperatures -2, 0, 1 and 5:

<!-- input: measurement_station -->
```text
4
-2
0
1
5
```

<!-- output: measurement_station -->
```text
Enter measurement count (1-24):
Enter temperature:
Enter temperature:
Enter temperature:
Enter temperature:
Measurements recorded: 4
Average temperature: 1
Below freezing: 1
```

**The second example:** bad text and a temperature outside the range, with the data `2`, `abc`, `50`, `-2`, `4`:

<!-- input: measurement_station -->
```text
2
abc
50
-2
4
```

<!-- output: measurement_station -->
```text
Enter measurement count (1-24):
Enter temperature:
Invalid temperature input, try again
Enter temperature:
Temperature out of range
Enter temperature:
Enter temperature:
Measurements recorded: 2
Average temperature: 1
Below freezing: 1
```

**The third example:** the data runs out after two of three measurements, with the data `3`, `-2`, `2`:

<!-- input: measurement_station -->
```text
3
-2
2
```

<!-- output: measurement_station -->
```text
Enter measurement count (1-24):
Enter temperature:
Enter temperature:
Enter temperature:
Input ended: 2 of 3 measurements recorded
```

**Before you write the program**, prepare a table of test cases. It must check at least:

- one negative and one positive measurement, several measurements with a whole-number average and with a half in the average, a temperature of exactly 0, -20 and 40, and the largest number of measurements;
- measurement counts of 0 and 25, and bad text instead of the count, also several times;
- temperatures of -21 and 41, bad text instead of a temperature, and a valid measurement after recovering the input;
- the end of the data: before the count, after an out-of-range count, after bad text, right after a valid count, after some of the temperatures, after a rejected temperature, and after bad text in the measurement phase.

Write down the expected standard output for each case, including the number of questions. Choose temperatures whose average is easy to work out in your head: whole numbers and halves.

You don't have to run the cases with the end of the data, including the third example, because ending the data from the keyboard isn't required. Write down in a trace table what the program does after each attempt, and compare it with the full list of control cases in part B.

When the result matches, you can save the project in Git, as in lesson 1.5. Before committing, check `git status`: only `main.cpp` and `CMakeLists.txt` go into the history.

## Task 2: Two bug reports

In `cpp-workspace`, create a `diagnosis_4` folder and copy `main.cpp` and `CMakeLists.txt` into it from the original `lesson_05_first_program`. Type each of the programs below in turn into that folder's `main.cpp`. Both build, end, and give wrong results.

**Report A.** A warm-up consists of several steps. The program should print the steps **from 1 to the given number of steps inclusive**, each as `Step K of N`, and finally `Warm-up done`. The number of steps is 0 to 5.

<!-- example: warmup_bug -->
```cpp
#include <iostream>

int main() {
    int step_count{0};

    std::cout << "Enter warm-up steps (0-5):\n";
    std::cin >> step_count;

    if (step_count >= 0 && step_count <= 5) {
        for (int step{0}; step <= step_count; ++step) {
            std::cout << "Step " << step << " of " << step_count << "\n";
        }

        std::cout << "Warm-up done\n";
    } else {
        std::cout << "Steps must be from 0 to 5\n";
    }
}
```

**Report B.** A small cinema has rows of seats. Row number `r` has `10 + r` seats: the first 11, the second 12, and so on. The program should print the total number of seats for the given number of rows, from 0 to 10.

<!-- example: cinema_bug -->
```cpp
#include <iostream>

int main() {
    int row_count{0};

    std::cout << "Enter number of rows (0-10):\n";
    std::cin >> row_count;

    if (row_count >= 0 && row_count <= 10) {
        int total_seats{0};

        for (int row{1}; row <= row_count; ++row) {
            total_seats = 0;
            total_seats += 10 + row;
        }

        std::cout << "Total seats: " << total_seats << "\n";
    } else {
        std::cout << "Rows must be from 0 to 10\n";
    }
}
```

**For each report:**

1. Read the requirement and write down the correct result for 0, 1 and 3.
2. **Predict** what the buggy program will print for these three cases. A trace table will help.
3. Run the program and compare.
4. Find the bug.
5. Fix the program with one change.
6. Check zero, one and three iterations again.

Record the results in a table:

| Report | Case that reveals the bug | Actual result | Cause | Fix | Check |
|---|---|---|---|---|---|
| A | | | | | |
| B | | | | | |

You don't need to save the `diagnosis_4` project in Git.

## Task 3: Analysis without running

This fragment should collect 3 readings in the range 0 to 100. After a failed read it recovers the input, as in lesson 4.6. **Analyse it on paper; don't run it:**

<!-- fragment -->
```cpp
int accepted{0};
int reading{0};

while (accepted < 3) {
    std::cout << "Enter reading:\n";
    std::cin >> reading;

    if (!std::cin.fail()) {
        if (reading >= 0 && reading <= 100) {
            ++accepted;
        } else {
            std::cout << "Reading out of range\n";
        }
    } else {
        std::cin.clear();
        std::string discarded_line{""};
        std::getline(std::cin, discarded_line);
        std::cout << "Invalid input, try again\n";
    }
}
```

The data is a single line, `5`, after which the data ends.

1. Fill in a state table for the first four attempts: the value read, `fail()`, `eof()`, what the program does, and `accepted` after the attempt.
2. Why can't the stream deliver another value from the second attempt on?
3. What does `fail()` mean then, and will `clear()` help here at all?
4. Which reason to end is this loop missing?
5. How can it be taken into account, without new constructs?
6. Why isn't the time limit in the automatic tests a solution?

## Task 4: Explain

Answer briefly, in writing, referring to your own program from task 1:

1. Why must every loop have a way to end? Point out what ends both loops in your program.
2. What decides the number of iterations while collecting the measurements?
3. Why don't rejected values increase the measurement counter?
4. What role does the accumulator play in your program?
5. When do you increase the counter of temperatures below zero, and why doesn't 0 count among them?
6. Why do you compute the average only after collecting a complete set? Can a division by zero happen in your program?
7. Why are both `clear()` and discarding the rest of the line needed after bad text?
8. Why mustn't the program ask again forever after the end of the data?
9. When is `for` more convenient, and when `while`? Which loop was chosen in task 1, and which in report B, and why?
10. Why didn't a test with one iteration reveal the bug in report B?
11. Why isn't a correct result for one set of data enough to consider a program correct?

## Success criteria

You pass the test when you meet **all** the criteria. You may use part B along the way, as long as you note it honestly in the self-assessment.

- `measurement_station/main.cpp` was written from an empty file, in valid C++20. The program builds without errors.
- The number of measurements is settled in a loop that asks again after a value outside the range and after bad text, and ends after a valid value or after the end of the data.
- The temperatures are collected in a loop that ends after collecting the required number of valid measurements, or after the end of the data. There's no question after the last measurement has been collected.
- After each read, the program first checks whether the read succeeded, then the end of the data, and only last recovers the input with `std::cin.clear()` and `std::getline`. It also takes into account the end of the data while discarding a line.
- The measurement counter, the sum and the counter of measurements below zero change only after a valid temperature is accepted. A temperature of 0 isn't below zero.
- The average is computed only from a complete set, so there's no division by zero.
- Standard output for the cases that can be typed matches the requirements, and the cases with the end of the data, including the third example, agree with the trace table.
- The table of cases was made before running the program and checks the boundaries from task 1.
- Both reports from task 2 were diagnosed and fixed, and zero, one and three iterations were checked again.
- Task 3 was analysed without running, and the missing reason to end was identified.
- You can explain every line of your program and answer the questions from task 4.

Variable names and the program's layout can differ from the reference solution, as long as they're readable. Two successive `while` loops are a good solution. There's no need to use `for` in task 1, nested loops, or functions of your own. A correct result is a necessary condition, but **not proof of understanding**. That's why tasks 3 and 4 are part of the test.

---

# Part B: checking and discussion

Come here after finishing part A, or when you knowingly decide to stop trying on your own.

## How to check your work

- **Standard output:** run the program for every case in your table and compare the program's lines with the expected ones, character by character, including the number of questions. Skip the typed data that the echo shows.
- **The same program:** don't change the code between runs.
- **The end of the data:** check the cases in which the data runs out with a trace table, and compare them with the full list of control cases. Each of them is checked automatically there.
- **Compare the full lists of control cases** below with your table. Did your table cover the same boundaries and the same end-of-data situations?
- **Order:** look through both loops. After a failed read, do you check for the end of the data first? Do the sum and the counters change in only one place?

## Hints

Open them in order, and only when you need them.

<details>
<summary>Task 1, hint 1: which variables?</summary>

List what the program has to remember: the required number of measurements, the number already accepted, the sum of the temperatures, and the number of temperatures below zero, plus whether the data has run out. Which of these values controls the second loop (lesson 4.4), and which is an accumulator (lesson 4.2)?

</details>

<details>
<summary>Task 1, hint 2: two phases</summary>

The program has two phases, one after the other: first it settles the number of measurements, then it collects the temperatures. Each phase is a separate `while` loop with the same three situations after a read: the read succeeded, the end of the data, or bad text (lesson 4.6). The second phase makes sense only if the first ended with a settled number.

</details>

<details>
<summary>Task 1, hint 3: the ending and the report</summary>

After the second loop there are three possible situations: the number of measurements wasn't settled, all the measurements were collected, or the data ran out along the way. Which variable lets you tell them apart? Compute the average in only one of them.

</details>

<details>
<summary>Task 2, report A</summary>

Which number does the first printed step start from, and how many times does the condition give `true` for 0 steps? Compare with lesson 4.3.

</details>

<details>
<summary>Task 2, report B</summary>

Trace the sum after each iteration for 3 rows. Which line keeps the sum from growing from row to row? Compare with lesson 4.2.

</details>

<details>
<summary>Task 3</summary>

After the end of the data, the read fails. Which branch runs then, and can anything in it end the loop? Compare with the `input_ended` flag in lesson 4.6.

</details>

## The full list of control cases: task 1

<details>
<summary>Open after preparing your own table</summary>

The first three cases are checked in part A.

| Data | Result | What it checks |
|---|---|---|
| `4`, `-2`, `0`, `1`, `5` | 4 measurements, average 1, below zero 1 | a whole-number average, a temperature of 0 |
| `2`, `abc`, `50`, `-2`, `4` | 2 measurements, average 1, below zero 1 | bad text and a temperature outside the range |
| `3`, `-2`, `2`, end | 2 of 3 | the end of the data after some of the temperatures |
| `1`, `-5` | 1 measurement, average -5, below zero 1 | one negative measurement |
| `1`, `7` | 1 measurement, average 7, below zero 0 | one positive measurement |
| `2`, `1.5`, `2.5` | average 2 | temperatures with a fractional part |
| `2`, `0`, `1` | average 0.5, below zero 0 | an average with a half, 0 isn't below zero |
| `4`, `1`, `2`, `3`, `4` | average 2.5 | an average with a half |
| `3`, `-2`, `-1`, `0` | average -1, below zero 2 | a negative average |
| `2`, `-20`, `40` | average 10, below zero 1 | both temperature boundaries |
| `24`, then 12 pairs `-1`, `2` | 24 measurements, average 0.5, below zero 12 | the largest number of measurements |
| `0`, `2`, `3`, `5` | 2 measurements, average 4 | a count of 0 |
| `25`, `1`, `-3` | 1 measurement, average -3 | a count of 25 |
| `abc`, `1`, `6` | 1 measurement, average 6 | text instead of the count |
| `abc`, `xyz`, `0`, `1`, `2` | 1 measurement, average 2 | several bad attempts at the count |
| `1`, `-21`, `3` | 1 measurement, average 3 | a temperature of -21 |
| `1`, `41`, `warm`, `0` | 1 measurement, average 0 | a temperature of 41, text, a measurement after recovery |
| no data | `Input ended` | the end of the data before the count |
| `30`, end | `Input ended` | the end of the data after an out-of-range count |
| `many`, end | `Input ended` | the end of the data after bad text |
| `2`, end | 0 of 2 | the end of the data right after the count |
| `2`, `45`, end | 0 of 2 | the end of the data after a rejected temperature |
| `2`, `1`, `abc`, end | 1 of 2 | the end of the data after bad text in the measurement phase |

<!-- input: measurement_station -->
```text
1
-5
```

<!-- output: measurement_station -->
```text
Enter measurement count (1-24):
Enter temperature:
Measurements recorded: 1
Average temperature: -5
Below freezing: 1
```

<!-- input: measurement_station -->
```text
1
7
```

<!-- output: measurement_station -->
```text
Enter measurement count (1-24):
Enter temperature:
Measurements recorded: 1
Average temperature: 7
Below freezing: 0
```

<!-- input: measurement_station -->
```text
2
1.5
2.5
```

<!-- output: measurement_station -->
```text
Enter measurement count (1-24):
Enter temperature:
Enter temperature:
Measurements recorded: 2
Average temperature: 2
Below freezing: 0
```

<!-- input: measurement_station -->
```text
2
0
1
```

<!-- output: measurement_station -->
```text
Enter measurement count (1-24):
Enter temperature:
Enter temperature:
Measurements recorded: 2
Average temperature: 0.5
Below freezing: 0
```

<!-- input: measurement_station -->
```text
4
1
2
3
4
```

<!-- output: measurement_station -->
```text
Enter measurement count (1-24):
Enter temperature:
Enter temperature:
Enter temperature:
Enter temperature:
Measurements recorded: 4
Average temperature: 2.5
Below freezing: 0
```

<!-- input: measurement_station -->
```text
3
-2
-1
0
```

<!-- output: measurement_station -->
```text
Enter measurement count (1-24):
Enter temperature:
Enter temperature:
Enter temperature:
Measurements recorded: 3
Average temperature: -1
Below freezing: 2
```

<!-- input: measurement_station -->
```text
2
-20
40
```

<!-- output: measurement_station -->
```text
Enter measurement count (1-24):
Enter temperature:
Enter temperature:
Measurements recorded: 2
Average temperature: 10
Below freezing: 1
```

<!-- input: measurement_station -->
```text
24
-1
2
-1
2
-1
2
-1
2
-1
2
-1
2
-1
2
-1
2
-1
2
-1
2
-1
2
-1
2
```

<!-- output: measurement_station -->
```text
Enter measurement count (1-24):
Enter temperature:
Enter temperature:
Enter temperature:
Enter temperature:
Enter temperature:
Enter temperature:
Enter temperature:
Enter temperature:
Enter temperature:
Enter temperature:
Enter temperature:
Enter temperature:
Enter temperature:
Enter temperature:
Enter temperature:
Enter temperature:
Enter temperature:
Enter temperature:
Enter temperature:
Enter temperature:
Enter temperature:
Enter temperature:
Enter temperature:
Enter temperature:
Measurements recorded: 24
Average temperature: 0.5
Below freezing: 12
```

<!-- input: measurement_station -->
```text
0
2
3
5
```

<!-- output: measurement_station -->
```text
Enter measurement count (1-24):
Measurement count out of range
Enter measurement count (1-24):
Enter temperature:
Enter temperature:
Measurements recorded: 2
Average temperature: 4
Below freezing: 0
```

<!-- input: measurement_station -->
```text
25
1
-3
```

<!-- output: measurement_station -->
```text
Enter measurement count (1-24):
Measurement count out of range
Enter measurement count (1-24):
Enter temperature:
Measurements recorded: 1
Average temperature: -3
Below freezing: 1
```

<!-- input: measurement_station -->
```text
abc
1
6
```

<!-- output: measurement_station -->
```text
Enter measurement count (1-24):
Invalid integer input, try again
Enter measurement count (1-24):
Enter temperature:
Measurements recorded: 1
Average temperature: 6
Below freezing: 0
```

<!-- input: measurement_station -->
```text
abc
xyz
0
1
2
```

<!-- output: measurement_station -->
```text
Enter measurement count (1-24):
Invalid integer input, try again
Enter measurement count (1-24):
Invalid integer input, try again
Enter measurement count (1-24):
Measurement count out of range
Enter measurement count (1-24):
Enter temperature:
Measurements recorded: 1
Average temperature: 2
Below freezing: 0
```

<!-- input: measurement_station -->
```text
1
-21
3
```

<!-- output: measurement_station -->
```text
Enter measurement count (1-24):
Enter temperature:
Temperature out of range
Enter temperature:
Measurements recorded: 1
Average temperature: 3
Below freezing: 0
```

<!-- input: measurement_station -->
```text
1
41
warm
0
```

<!-- output: measurement_station -->
```text
Enter measurement count (1-24):
Enter temperature:
Temperature out of range
Enter temperature:
Invalid temperature input, try again
Enter temperature:
Measurements recorded: 1
Average temperature: 0
Below freezing: 0
```

<!-- input: measurement_station -->
```text
```

<!-- output: measurement_station -->
```text
Enter measurement count (1-24):
Input ended
```

<!-- input: measurement_station -->
```text
30
```

<!-- output: measurement_station -->
```text
Enter measurement count (1-24):
Measurement count out of range
Enter measurement count (1-24):
Input ended
```

<!-- input: measurement_station -->
```text
many
```

<!-- output: measurement_station -->
```text
Enter measurement count (1-24):
Invalid integer input, try again
Enter measurement count (1-24):
Input ended
```

<!-- input: measurement_station -->
```text
2
```

<!-- output: measurement_station -->
```text
Enter measurement count (1-24):
Enter temperature:
Input ended: 0 of 2 measurements recorded
```

<!-- input: measurement_station -->
```text
2
45
```

<!-- output: measurement_station -->
```text
Enter measurement count (1-24):
Enter temperature:
Temperature out of range
Enter temperature:
Input ended: 0 of 2 measurements recorded
```

<!-- input: measurement_station -->
```text
2
1
abc
```

<!-- output: measurement_station -->
```text
Enter measurement count (1-24):
Enter temperature:
Enter temperature:
Invalid temperature input, try again
Enter temperature:
Input ended: 1 of 2 measurements recorded
```

</details>

## Example solutions

<details>
<summary>Task 1: the measurement station</summary>

<!-- example: measurement_station -->
```cpp
#include <iostream>
#include <string>

int main() {
    int required_count{0};
    bool count_accepted{false};
    bool input_ended{false};

    while (!count_accepted && !input_ended) {
        std::cout << "Enter measurement count (1-24):\n";
        std::cin >> required_count;

        if (!std::cin.fail()) {
            if (required_count >= 1 && required_count <= 24) {
                count_accepted = true;
            } else {
                std::cout << "Measurement count out of range\n";
            }
        } else if (std::cin.eof()) {
            input_ended = true;
        } else {
            std::cin.clear();
            std::string discarded_line{""};
            std::getline(std::cin, discarded_line);

            if (std::cin.fail() || std::cin.eof()) {
                input_ended = true;
            } else {
                std::cout << "Invalid integer input, try again\n";
            }
        }
    }

    int recorded{0};
    int below_freezing{0};
    double total{0.0};
    double temperature{0.0};

    while (count_accepted && recorded < required_count && !input_ended) {
        std::cout << "Enter temperature:\n";
        std::cin >> temperature;

        if (!std::cin.fail()) {
            if (temperature >= -20.0 && temperature <= 40.0) {
                ++recorded;
                total += temperature;

                if (temperature < 0.0) {
                    ++below_freezing;
                }
            } else {
                std::cout << "Temperature out of range\n";
            }
        } else if (std::cin.eof()) {
            input_ended = true;
        } else {
            std::cin.clear();
            std::string discarded_line{""};
            std::getline(std::cin, discarded_line);

            if (std::cin.fail() || std::cin.eof()) {
                input_ended = true;
            } else {
                std::cout << "Invalid temperature input, try again\n";
            }
        }
    }

    if (!count_accepted) {
        std::cout << "Input ended\n";
    } else if (recorded == required_count) {
        std::cout << "Measurements recorded: " << recorded << "\n";
        std::cout << "Average temperature: " << total / recorded << "\n";
        std::cout << "Below freezing: " << below_freezing << "\n";
    } else {
        std::cout << "Input ended: " << recorded << " of " << required_count << " measurements recorded\n";
    }
}
```

- **Two phases, two `while` loops.** The first ends once the number of measurements is settled (`count_accepted`) or after the end of the data (`input_ended`). The second runs only once the number is settled, and ends after collecting all the measurements or after the end of the data. Neither loop is nested in the other.
- **Three values change in one place:** after a valid temperature is accepted. `++recorded` counts the accepted measurements, `total += temperature` is the accumulator, and `++below_freezing` runs only for a temperature less than zero, so 0 doesn't count.
- **The number of iterations of the second loop is decided by the progress,** i.e. the number of **accepted** measurements, not the number of attempts. Bad data adds attempts, but not progress. That's why it's a `while`, not a `for`.
- **The order after a read** is the same in both phases: a successful read, then the end of the data, then recovery and a check for the end of the data after discarding the line (lesson 4.6). The recovery fragment appears twice. At this stage of the course that's fine.
- **The average** is computed only when `recorded == required_count`. The required number is at least 1, so a division by zero is impossible. `total` is a `double`, so `total / recorded` also gives a `double`.
- **The results:** for `4`, `-2`, `0`, `1`, `5` the sum is 4, and the average 4 / 4 = 1. Only -2 is below zero. For `2`, `abc`, `50`, `-2`, `4` only -2 and 4 are accepted: a sum of 2, an average of 1. Neither `abc` nor 50 is a measurement.
- **Precision:** the temperatures in the tests are whole numbers and halves, so the sums and averages are exact, and `std::cout` prints them the way we write them (1, 0.5, 2.5, -1). Not every possible `double` average prints so simply, but these tests check the program's logic, not rounding.

</details>

<details>
<summary>Task 2, report A: the result before the fix, and the fixed program</summary>

Before the fix:

<!-- input: warmup_bug -->
```text
0
```

<!-- output: warmup_bug -->
```text
Enter warm-up steps (0-5):
Step 0 of 0
Warm-up done
```

<!-- input: warmup_bug -->
```text
1
```

<!-- output: warmup_bug -->
```text
Enter warm-up steps (0-5):
Step 0 of 1
Step 1 of 1
Warm-up done
```

<!-- input: warmup_bug -->
```text
3
```

<!-- output: warmup_bug -->
```text
Enter warm-up steps (0-5):
Step 0 of 3
Step 1 of 3
Step 2 of 3
Step 3 of 3
Warm-up done
```

- **The bug shows already for 0 steps:** the program prints `Step 0 of 0`, although it shouldn't print any step. Every case has one iteration too many.
- **The cause:** the counter starts at 0, and the condition `<=` also allows the last number.
- **The fix:** the counter starts at 1, because the requirement says "from 1":

<!-- example: warmup_fixed -->
```cpp
#include <iostream>

int main() {
    int step_count{0};

    std::cout << "Enter warm-up steps (0-5):\n";
    std::cin >> step_count;

    if (step_count >= 0 && step_count <= 5) {
        for (int step{1}; step <= step_count; ++step) {
            std::cout << "Step " << step << " of " << step_count << "\n";
        }

        std::cout << "Warm-up done\n";
    } else {
        std::cout << "Steps must be from 0 to 5\n";
    }
}
```

<!-- input: warmup_fixed -->
```text
0
```

<!-- output: warmup_fixed -->
```text
Enter warm-up steps (0-5):
Warm-up done
```

<!-- input: warmup_fixed -->
```text
1
```

<!-- output: warmup_fixed -->
```text
Enter warm-up steps (0-5):
Step 1 of 1
Warm-up done
```

<!-- input: warmup_fixed -->
```text
3
```

<!-- output: warmup_fixed -->
```text
Enter warm-up steps (0-5):
Step 1 of 3
Step 2 of 3
Step 3 of 3
Warm-up done
```

</details>

<details>
<summary>Task 2, report B: the result before the fix, and the fixed program</summary>

Before the fix:

<!-- input: cinema_bug -->
```text
0
```

<!-- output: cinema_bug -->
```text
Enter number of rows (0-10):
Total seats: 0
```

<!-- input: cinema_bug -->
```text
1
```

<!-- output: cinema_bug -->
```text
Enter number of rows (0-10):
Total seats: 11
```

<!-- input: cinema_bug -->
```text
3
```

<!-- output: cinema_bug -->
```text
Enter number of rows (0-10):
Total seats: 13
```

| Row | Seats in the row | `total_seats` after `total_seats = 0;` | `total_seats` after adding |
|---|---|---|---|
| 1 | 11 | 0 | 11 |
| 2 | 12 | 0 | 12 |
| 3 | 13 | 0 | 13 |

- **For 0 and 1 rows the result is right,** because there's nothing to lose. Only 3 rows reveal the bug: the result is 13, i.e. only the last row, instead of 11 + 12 + 13 = 36.
- **The cause:** `total_seats = 0;` in the loop body wipes out the sum in every iteration.
- **The fix:** remove that line. The sum gets its start value 0 once, before the loop:

<!-- example: cinema_fixed -->
```cpp
#include <iostream>

int main() {
    int row_count{0};

    std::cout << "Enter number of rows (0-10):\n";
    std::cin >> row_count;

    if (row_count >= 0 && row_count <= 10) {
        int total_seats{0};

        for (int row{1}; row <= row_count; ++row) {
            total_seats += 10 + row;
        }

        std::cout << "Total seats: " << total_seats << "\n";
    } else {
        std::cout << "Rows must be from 0 to 10\n";
    }
}
```

<!-- input: cinema_fixed -->
```text
0
```

<!-- output: cinema_fixed -->
```text
Enter number of rows (0-10):
Total seats: 0
```

<!-- input: cinema_fixed -->
```text
1
```

<!-- output: cinema_fixed -->
```text
Enter number of rows (0-10):
Total seats: 11
```

<!-- input: cinema_fixed -->
```text
3
```

<!-- output: cinema_fixed -->
```text
Enter number of rows (0-10):
Total seats: 36
```

</details>

<details>
<summary>Task 3: a loop with no way out after the end of the data</summary>

| Attempt | Value read | `fail()` | `eof()` | What the program does | `accepted` |
|---|---|---|---|---|---|
| 1 | 5 | `false` | `false` | in range: `++accepted` | 1 |
| 2 | none: the data has run out | `true` | `true` | `clear()`, `getline` fails too, message | 1 |
| 3 | none | `true` | `true` | the same | 1 |
| 4 | none | `true` | `true` | the same, and so on forever | 1 |

1. The table is above. The loop asks and prints `Invalid input, try again` forever.
2. **The data has run out:** after the line `5` there's nothing left that could be read, and new data won't appear by itself.
3. **`fail()` means a failed read,** here because of the end of the data. `clear()` only removes the error mark. It doesn't create data, so the next read fails again, and `getline` doesn't discard anything either.
4. **The end of the data is missing as a reason to end.** The loop ends only after three accepted readings, and those will never come.
5. **As in lesson 4.6:** after a failed read, first check `std::cin.eof()` and set a flag, for example `input_ended`, and after discarding the line check for the end of the data once more. The loop's condition is then `accepted < 3 && !input_ended`.
6. **The time limit in the tests only detects** that a program doesn't end. A correct program ends by itself, based on its own condition. Outside the tests there's no time limit at all, and the program would keep asking forever.

</details>

## Example answers to task 4

<details>
<summary>Show the example answers</summary>

1. Without a way to end, the program would keep asking or calculating forever. The first loop is ended by settling the number of measurements or by the end of the data, and the second by collecting all the measurements or by the end of the data.
2. The number of **accepted** measurements compared with the required number. Bad and rejected data add attempts, but don't bring the end closer.
3. Because the counter says how many valid measurements there are for the report and the average. A rejected value isn't a measurement.
4. It builds up the sum of the accepted temperatures, from which the average is computed at the end.
5. Only after accepting a valid temperature less than zero. 0 isn't less than zero, so the condition `temperature < 0.0` gives `false` for it.
6. Because the report is about a complete set; for an incomplete one the program only prints how many measurements it collected. The average is computed when the required number of measurements has been collected, i.e. at least 1, so there's no division by zero.
7. Because there are two obstacles: `clear()` removes the error state, and discarding the line takes the bad characters out of the input. Without either of them, the next read fails again.
8. Because after the end of the data nothing more will come. Further questions would get no answer, and the loop would go on forever.
9. `for` is convenient when a counter with a start value, a condition and an update controls the repetition, as in report B, with one iteration per row. `while` is natural when the repetition goes on while something is true, as in task 1, where the number of attempts depends on how much data has to be rejected.
10. Because with one iteration, resetting the sum has nothing to wipe out: 0 + 11 is the right result. The bug shows only with several iterations.
11. Because one set of data checks only one path through the program. Off-by-one errors, resetting an accumulator, or a missing way out after the end of the data show up only with zero, one or many iterations, and with data that runs out early.

</details>

## Self-assessment

For each criterion, mark one answer:

| Criterion | On my own | With a hint | After looking at the solution | To revise |
|---|---|---|---|---|
| Writing the program from an empty `main.cpp` | | | | |
| Asking again for the number of measurements | | | | |
| Recovering the input after bad text | | | | |
| Ending both phases after the end of the data | | | | |
| Counting only valid measurements | | | | |
| The sum, the average and the measurements below zero | | | | |
| No question after the last measurement | | | | |
| A table of cases with boundaries and the end of the data | | | | |
| Report A (an off-by-one in `for`) | | | | |
| Report B (resetting an accumulator) | | | | |
| Task 3 (a loop with no way out after the end of the data) | | | | |
| The explanations from task 4 | | | | |

If anything is marked in the "To revise" column, go back to the matching lesson:

| Topic | Lesson |
|---|---|
| `while`, zero iterations, the trace table | 4.1 |
| the accumulator and `+=` | 4.2 |
| `for` and `++` | 4.3 |
| a loop until a goal is reached, progress | 4.4 |
| asking again and `std::cin.fail()` | 4.5 |
| `clear()`, `std::getline`, `eof()` | 4.6 |
| comparisons, `&&` and `\|\|` | 3.1–3.4 |
| `double` and reading data | 2.5–2.6 |

Then try the task again, for example with a different temperature range.

---

## Module 4 summary

After seven lessons, you can:

- repeat actions with a `while` loop and predict how it runs in a table, including zero iterations;
- write counter-controlled loops, also in the compact `for` form, with prefix `++`;
- write loops controlled by progress towards a goal, and explain why they end;
- build up results in accumulators with `+=`, and tell iteration and event counters from sums;
- find off-by-one errors, accumulator resets, and loops without progress;
- ask again after a value that doesn't meet the requirements;
- tell an unacceptable value from a failed read and from the end of the data;
- bring the stream back into working order with `clear()`, and discard the rest of a bad line with `std::getline`;
- end a program safely when the data runs out;
- test loops for zero, one and many iterations.

Your programs don't yet check whole lines of text, and don't store many values at once. Each program is also a single `main` function. Those things come in later modules.

## What's next

The next modules will let you organise larger programs and work with more complex data. Module 5 is in preparation.

**Previous lesson:** [Lesson 4.6: A failed read, recovering the stream and the end of the data](lesson_06_recover_and_end_of_input.en.md) · **Next lesson:** in preparation · [Course overview](../../README.en.md)

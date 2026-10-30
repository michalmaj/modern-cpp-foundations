# Lesson 6.2: Adding data to a vector: `push_back()` and `empty()`

[Polski](lesson_02_adding_to_a_vector.md) · **English** · [Course overview](../../README.en.md)

> **Module 6, lesson 2** · about 75–90 minutes, can be split into two sessions
> **You need:** your `cpp-workspace` folder and the original `lesson_05_first_program` project, as before. You won't need the debugger in this lesson.
> **Pilot version.** The programs in this lesson are checked automatically on Windows, Ubuntu and macOS, including with the given input data. Typing input in CLion's **Run** window is described without a manual check on every system.

## Before you start

This lesson assumes that after lesson 6.1 and the earlier modules you:

- create a `std::vector<int>` with initial values and go through it with a range-based `for` loop;
- get the number of elements with `size()` and go through a vector a second time when you need the result of the first pass;
- check with `std::cin.fail()` whether a read succeeded, and know that after a failed read the following reads fail too (lessons 4.5 and 4.6);
- read a fixed number of values in a loop with a counter, as in lessons 4.7 and 5.7;
- remember that dividing two whole numbers gives a whole number (lessons 2.4 and 2.5).

## The situation

In lesson 6.1, every element of the vector was known before the program started:

<!-- fragment -->
```cpp
const std::vector<int> measurements{3, 7, 5, 9};
```

What if the user gives the measurements only while the program is running? You won't change the source code after every new measurement. You need a vector that starts empty and **takes new elements while the program runs**.

After this lesson you will:

- create an empty vector that elements can be added to, and explain why it has no `const`;
- add elements at the end of a vector with `push_back()` and predict their order;
- check with `empty()` whether a vector has any elements;
- store values read from the input in a vector, only after a successful read;
- tell the number of read attempts from the number of stored elements;
- compute the average of the stored values without integer division, and only when there's data;
- design on your own a program that stores only the data that meets the requirements.

## 1. Prepare the project

In `cpp-workspace`, create a folder `lesson_6_2` and copy `main.cpp` and `CMakeLists.txt` from the original `lesson_05_first_program` into it. You type the programs from sections 2–7 into `main.cpp` in this folder.

## 2. An empty vector that will change

<!-- fragment -->
```cpp
std::vector<int> measurements{};
```

- The element type is still `int`.
- Empty `{}` create a vector with no elements: `size()` gives 0.
- **There's no `const`**, because this vector will change: the program will add elements to it.

This isn't a new general rule. A vector the program doesn't change still gets `const`, as in lesson 6.1. You leave `const` out only where the change is part of the task.

## 3. Adding at the end: `push_back()`

<!-- example: push_three -->
```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<int> measurements{};
    std::cout << "Stored: " << measurements.size() << "\n";

    measurements.push_back(3);
    std::cout << "Stored: " << measurements.size() << "\n";

    measurements.push_back(7);
    measurements.push_back(5);
    std::cout << "Stored: " << measurements.size() << "\n";

    for (const int measurement : measurements) {
        std::cout << measurement << "\n";
    }
}
```

**Predict** every line of standard output, including the order of the elements at the end. Then run the program.

<details>
<summary>Standard output</summary>

<!-- output: push_three -->
```text
Stored: 0
Stored: 1
Stored: 3
3
7
5
```

</details>

`measurements.push_back(3)` is a call to a member function of the vector, like `size()`. The parentheses hold the value the program **adds at the end** of the vector. The vector's contents change like this:

| Moment | Contents | `size()` |
|---|---|---|
| after creation | `{}` | 0 |
| after `push_back(3)` | `{3}` | 1 |
| after `push_back(7)` | `{3, 7}` | 2 |
| after `push_back(5)` | `{3, 7, 5}` | 3 |

- **`push_back` isn't an assignment.** `x = 5;` replaces the variable's previous value. `push_back(5)` **adds** a new element, and the earlier elements stay.
- **A new element always goes at the end**, so the order of the elements is the order of the `push_back` calls.
- **The vector doesn't need to know the final number of elements** when you create it. `size()` grows by 1 with every `push_back`.
- **The range-based loop is the same as in 6.1.** Only where the elements came from has changed.

**Predict** whether this program builds:

<!-- broken: push_to_const at=7:18 errors=1 error=^no matching member function for call to 'push_back'$ -->
```cpp
#include <iostream>
#include <vector>

int main() {
    const std::vector<int> measurements{};

    measurements.push_back(3);

    std::cout << "Measurements stored: " << measurements.size() << "\n";
}
```

<details>
<summary>What the compiler reports, and why</summary>

The program won't build. On line 7, the compiler reports `no matching member function for call to 'push_back'`, and in the following `note:` lines it adds that the vector is `const` (`'this' argument has type 'const std::vector<int>'`). A `const` vector can't change, so nothing can be added to it. The fix: remove `const` from the definition of a vector that should take elements.

</details>

## 4. Is the vector empty? `empty()`

<!-- example: empty_check -->
```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<int> measurements{};

    if (measurements.empty()) {
        std::cout << "No measurements yet\n";
    }

    measurements.push_back(4);

    if (measurements.empty()) {
        std::cout << "No measurements yet\n";
    } else {
        std::cout << "Measurements stored: " << measurements.size() << "\n";
    }
}
```

**Predict** which branches run, and run the program.

<details>
<summary>Standard output</summary>

<!-- output: empty_check -->
```text
No measurements yet
Measurements stored: 1
```

</details>

- `empty()` answers the question "does the vector have no elements at all?". It gives a `bool`, `true` or `false`, so it fits straight into an `if` condition.
- After a successful `push_back`, a vector that was empty is no longer empty.
- **`empty()` doesn't remove anything.** It only checks. It's a question about the vector's state, not a command.
- `measurements.empty()` checks the same thing as `measurements.size() == 0`, but says directly what you're asking. That's why, when the question is "is there any data?", we use `empty()`.

## 5. Attempts and stored elements

A program reads four numbers in turn: `4`, `25`, `8` and `12`. The requirement says that only values from 0 to 20 are allowed. Fill in the table before you open the answer:

| Attempt | Number read | In the range 0–20? | What the program does | Vector contents after the attempt | `size()` |
|---|---|---|---|---|---|
| 1 | 4 | | | | |
| 2 | 25 | | | | |
| 3 | 8 | | | | |
| 4 | 12 | | | | |

<details>
<summary>The filled-in table</summary>

| Attempt | Number read | In the range 0–20? | What the program does | Vector contents after the attempt | `size()` |
|---|---|---|---|---|---|
| 1 | 4 | yes | adds 4 | `{4}` | 1 |
| 2 | 25 | no | skips it | `{4}` | 1 |
| 3 | 8 | yes | adds 8 | `{4, 8}` | 2 |
| 4 | 12 | yes | adds 12 | `{4, 8, 12}` | 3 |

There were **four attempts**, but the vector has **three elements**, in the order 4, 8, 12. `size()` gives 3, not 4.

</details>

**The vector doesn't know your task's rules.** `push_back(25)` would add 25 without any check, because for the vector it's an ordinary `int`. Whether a value goes into the collection is decided by **the program**: it calls `push_back` only for values that meet the requirements. So the number of attempts and the number of stored elements are two different pieces of information.

## 6. Data from the input goes into the vector

This program reads three measurements and stores them in a vector:

<!-- example: read_measurements -->
```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<int> measurements{};

    std::cout << "Enter 3 measurements:\n";

    for (int number{1}; number <= 3; ++number) {
        int measurement{0};
        std::cin >> measurement;

        if (!std::cin.fail()) {
            measurements.push_back(measurement);
        }
    }

    if (std::cin.fail()) {
        std::cout << "Input could not be read\n";
    } else {
        std::cout << "Measurements stored: " << measurements.size() << "\n";

        for (const int measurement : measurements) {
            std::cout << measurement << "\n";
        }
    }
}
```

Run the program and type `3`, `7` and `5`, each number on its own line:

<!-- input: read_measurements -->
```text
3
7
5
```

<!-- output: read_measurements -->
```text
Enter 3 measurements:
Measurements stored: 3
3
7
5
```

- `push_back` stands **after** the read is checked. Only a value that was really read goes into the vector.
- The vector is printed only **after** the reading loop. First the program collects all the elements, then it goes through them.
- If one read fails, the following ones fail too (lesson 4.5). The loop still ends after three passes, and `std::cin.fail()` after the loop still gives `true`.

**Predict** what the program prints when you type `3` and then `abc`. Then check.

<!-- input: read_measurements -->
```text
3
abc
```

<details>
<summary>Standard output</summary>

<!-- output: read_measurements -->
```text
Enter 3 measurements:
Input could not be read
```

The first measurement went into the vector, but the second read failed, so the program doesn't print an incomplete list.

</details>

## 7. The average of the stored values

You compute an average from the sum and the number of elements. But first you check whether there are any elements:

<!-- example: average_distance -->
```cpp
#include <iostream>
#include <vector>

int main() {
    const std::vector<int> distances{6, 9, 4, 8};

    if (distances.empty()) {
        std::cout << "No distances\n";
    } else {
        double total{0.0};

        for (const int distance : distances) {
            total += distance;
        }

        const double average{total / distances.size()};
        std::cout << "Average distance: " << average << " km\n";
    }
}
```

**Predict** the average and run the program.

<details>
<summary>Standard output</summary>

<!-- output: average_distance -->
```text
Average distance: 6.75 km
```

</details>

- This vector doesn't change, so it has `const`.
- **The sum is a `double`.** The elements are `int`s, but `total += distance;` adds them to a `double` variable. Then `total / distances.size()` is a division with a fractional part: 27 / 4 gives 6.75. If `total` were an `int`, it would be a division of whole numbers, as in lesson 2.4, and the program would print 6.
- **`empty()` comes before the calculation.** For this data the `No distances` branch doesn't run, but the program is also ready for an empty vector.

**Your turn: analyse it, don't run it.** Someone removed the `empty()` check, and the vector has no elements:

<!-- fragment -->
```cpp
const std::vector<int> distances{};
double total{0.0};

for (const int distance : distances) {
    total += distance;
}

const double average{total / distances.size()};
```

Can the average be computed like this? What is `total`, and what is `distances.size()`?

<details>
<summary>Answer</summary>

No. The loop doesn't run even once, so `total` is 0, and `distances.size()` is 0. In this model the average of an empty set doesn't exist: there's no value to compute it from. The program would divide by zero, and none of its results would be a meaningful average. That's why we don't run such a program; we write it so that this can't happen.

**Before you do a calculation that needs data, check that the data really exists.** Here, `empty()` does that.

</details>

## 8. Mission: waiting times

The program collects waiting times from several reports, in whole minutes. Not every number read correctly is an allowed waiting time. The program stores only the allowed times in a vector, and then analyses the stored data.

**Requirements:**

- The program asks `Enter report count (0-6):` and reads the number of reports, a whole number.
- If the read fails, it prints `Input could not be read` and ends. If the number is outside the range 0 to 6, it prints `Invalid report count` and ends.
- For each report, from 1 to the given number, it asks `Enter waiting time N (0-20):`, where `N` is the report number, and reads the time, a whole number.
- A time from 0 to 20 inclusive is allowed and goes into a `std::vector<int>`. A time outside that range is skipped: the program prints `Waiting time N skipped` and does **not** store it. A skipped time uses up its report: the program doesn't ask for it again.
- If reading a time fails, for example after text or when the data ends early, the program prints `Input could not be read` and ends: no questions about further reports and no summary. Lines printed earlier stay.
- After reading all the reports, the program prints `Stored waiting times: N`, where `N` is the number of stored times.
- If no time was stored, it then prints only `No valid waiting times`. It doesn't compute an average.
- Otherwise it prints `Average waiting time: X`, the average of the stored times, and `Times above average: N`, the number of stored times **strictly greater** than the average.
- You go through the vector's elements with a range-based loop. The constructs from this lesson and the earlier ones are enough.

In `cpp-workspace`, create a folder `waiting_times`, copy `CMakeLists.txt` from the original `lesson_05_first_program` into it, create an empty `main.cpp` and write the program on your own.

**Example A:** four reports, times 4, 25, 8 and 12.

<!-- input: waiting_times -->
```text
4
4
25
8
12
```

<!-- output: waiting_times -->
```text
Enter report count (0-6):
Enter waiting time 1 (0-20):
Enter waiting time 2 (0-20):
Waiting time 2 skipped
Enter waiting time 3 (0-20):
Enter waiting time 4 (0-20):
Stored waiting times: 3
Average waiting time: 8
Times above average: 1
```

The vector holds 4, 8 and 12. The average is 8, and only 12 is strictly greater than it.

**Example B:** zero reports.

<!-- input: waiting_times -->
```text
0
```

<!-- output: waiting_times -->
```text
Enter report count (0-6):
Stored waiting times: 0
No valid waiting times
```

**Example C:** two reports, times 5 and 6. **Predict** the whole standard output before you write the program.

<!-- input: waiting_times -->
```text
2
5
6
```

<details>
<summary>Standard output for example C</summary>

<!-- output: waiting_times -->
```text
Enter report count (0-6):
Enter waiting time 1 (0-20):
Enter waiting time 2 (0-20):
Stored waiting times: 2
Average waiting time: 5.5
Times above average: 1
```

A program that prints an average of 5 here computes it with integer division.

</details>

**This isn't the program from section 6 with different messages.** That program stored every number it read, and after an error it still finished its loop. You have to decide on your own:

1. how to build a loop that reads the planned number of reports and ends straight away after a failed read;
2. how to tell a failed read from a number that was read correctly but isn't allowed;
3. under what condition, and where, to call `push_back`;
4. what the program prints when it stored no time;
5. how to compute the average without integer division;
6. how to count the times above the average, and why a time equal to the average doesn't count;
7. how to make sure that no summary appears after a failed read.

**Before you write the program**, prepare a table of test cases: zero reports, one time of 0, one time of 20, an average with a fractional part, all zeros, a time equal to the average, times skipped before a valid one, between valid ones and after them, only skipped times, report counts of -1 and 7, text instead of the report count and instead of a time, and data that ends after the report count or after a few times. For each case, write down the expected standard output.

Run the program for examples A, B and C and for 4–6 cases of your choice from the table. Analyse the cases where the data ends early on paper, instead of running them, and compare them with the full list of check cases. All the cases of the full check list are checked automatically.

### Success criteria

- The program builds as C++20, and its standard output for examples A, B and C is exactly as above.
- For 4–6 cases of your choice from the table that can be typed, the standard output matches the requirements. The cases where the data ends early match your trace table.
- The vector holds only allowed times, in the order of the reports. A skipped time never goes into it.
- The program doesn't compute an average when the vector is empty, and doesn't compute it with integer division.
- After a failed read, the program doesn't ask about further reports and doesn't print a summary.
- The table of cases was made before the program was run.
- You can point to the place in your program where it's decided whether a time goes into the vector.

When the result matches, you can save the project in Git, as in lesson 1.5.

<details>
<summary>Hint 1</summary>

Does the number of reports read have to equal the number of elements stored in the vector?

</details>

<details>
<summary>Hint 2</summary>

Think about where to call `push_back()` so that a value that isn't allowed never gets into the collection.

</details>

<details>
<summary>Hint 3</summary>

After reading has finished, check `empty()`. Only then compute the average and go through the stored values again to count those greater than the average.

</details>

<details>
<summary>The full list of check cases: open it after preparing your own table</summary>

Examples A, B and C are checked above. "Skipped" lists the report numbers with the message `Waiting time N skipped`.

| Data | Skipped | Result | What it checks |
|---|---|---|---|
| `4`, `4`, `25`, `8`, `12` | 2 | stored 3, average 8, above 1 | example A: a skipped time between valid ones |
| `0` | — | stored 0, `No valid waiting times` | example B: zero reports |
| `2`, `5`, `6` | — | stored 2, average 5.5, above 1 | example C: an average with a fractional part |
| `1`, `0` | — | stored 1, average 0, above 0 | the lower bound of a time |
| `1`, `20` | — | stored 1, average 20, above 0 | the upper bound of a time |
| `3`, `0`, `0`, `0` | — | stored 3, average 0, above 0 | all zeros |
| `3`, `4`, `8`, `12` | — | stored 3, average 8, above 1 | a time equal to the average doesn't count |
| `2`, `0`, `20` | — | stored 2, average 10, above 1 | both bounds at once |
| `6`, `20` six times | — | stored 6, average 20, above 0 | the largest report count, all equal to the average |
| `3`, `-1`, `21`, `3` | 1, 2 | stored 1, average 3, above 0 | times just outside the range before a valid one |
| `3`, `6`, `9`, `-5` | 3 | stored 2, average 7.5, above 1 | a skipped time after valid ones |
| `2`, `-1`, `21` | 1, 2 | stored 0, `No valid waiting times` | every time skipped: an empty vector |
| `-1` | — | `Invalid report count` | a report count just below the range |
| `7` | — | `Invalid report count` | a report count just above the range |
| `abc` | — | `Input could not be read` | text instead of the report count |
| no data | — | `Input could not be read` | the data ends straight away |
| `2`, `abc` | — | the question for time 1, then `Input could not be read` | text instead of the first time |
| `3`, `4`, `abc` | — | the questions for times 1 and 2, then `Input could not be read` | text instead of the second time |
| `3`, end of data | — | the question for time 1, then `Input could not be read` | the data ends after the report count |
| `3`, `4`, end of data | — | the questions for times 1 and 2, then `Input could not be read` | the data ends after one time |
| `4`, `4`, `25`, end of data | 2 | the questions for times 1–3, then `Input could not be read` | the data ends after a skipped time |

<!-- input: waiting_times -->
```text
1
0
```

<!-- output: waiting_times -->
```text
Enter report count (0-6):
Enter waiting time 1 (0-20):
Stored waiting times: 1
Average waiting time: 0
Times above average: 0
```

<!-- input: waiting_times -->
```text
1
20
```

<!-- output: waiting_times -->
```text
Enter report count (0-6):
Enter waiting time 1 (0-20):
Stored waiting times: 1
Average waiting time: 20
Times above average: 0
```

<!-- input: waiting_times -->
```text
3
0
0
0
```

<!-- output: waiting_times -->
```text
Enter report count (0-6):
Enter waiting time 1 (0-20):
Enter waiting time 2 (0-20):
Enter waiting time 3 (0-20):
Stored waiting times: 3
Average waiting time: 0
Times above average: 0
```

<!-- input: waiting_times -->
```text
3
4
8
12
```

<!-- output: waiting_times -->
```text
Enter report count (0-6):
Enter waiting time 1 (0-20):
Enter waiting time 2 (0-20):
Enter waiting time 3 (0-20):
Stored waiting times: 3
Average waiting time: 8
Times above average: 1
```

<!-- input: waiting_times -->
```text
2
0
20
```

<!-- output: waiting_times -->
```text
Enter report count (0-6):
Enter waiting time 1 (0-20):
Enter waiting time 2 (0-20):
Stored waiting times: 2
Average waiting time: 10
Times above average: 1
```

<!-- input: waiting_times -->
```text
6
20
20
20
20
20
20
```

<!-- output: waiting_times -->
```text
Enter report count (0-6):
Enter waiting time 1 (0-20):
Enter waiting time 2 (0-20):
Enter waiting time 3 (0-20):
Enter waiting time 4 (0-20):
Enter waiting time 5 (0-20):
Enter waiting time 6 (0-20):
Stored waiting times: 6
Average waiting time: 20
Times above average: 0
```

<!-- input: waiting_times -->
```text
3
-1
21
3
```

<!-- output: waiting_times -->
```text
Enter report count (0-6):
Enter waiting time 1 (0-20):
Waiting time 1 skipped
Enter waiting time 2 (0-20):
Waiting time 2 skipped
Enter waiting time 3 (0-20):
Stored waiting times: 1
Average waiting time: 3
Times above average: 0
```

<!-- input: waiting_times -->
```text
3
6
9
-5
```

<!-- output: waiting_times -->
```text
Enter report count (0-6):
Enter waiting time 1 (0-20):
Enter waiting time 2 (0-20):
Enter waiting time 3 (0-20):
Waiting time 3 skipped
Stored waiting times: 2
Average waiting time: 7.5
Times above average: 1
```

<!-- input: waiting_times -->
```text
2
-1
21
```

<!-- output: waiting_times -->
```text
Enter report count (0-6):
Enter waiting time 1 (0-20):
Waiting time 1 skipped
Enter waiting time 2 (0-20):
Waiting time 2 skipped
Stored waiting times: 0
No valid waiting times
```

<!-- input: waiting_times -->
```text
-1
```

<!-- output: waiting_times -->
```text
Enter report count (0-6):
Invalid report count
```

<!-- input: waiting_times -->
```text
7
```

<!-- output: waiting_times -->
```text
Enter report count (0-6):
Invalid report count
```

<!-- input: waiting_times -->
```text
abc
```

<!-- output: waiting_times -->
```text
Enter report count (0-6):
Input could not be read
```

<!-- input: waiting_times -->
```text
```

<!-- output: waiting_times -->
```text
Enter report count (0-6):
Input could not be read
```

<!-- input: waiting_times -->
```text
2
abc
```

<!-- output: waiting_times -->
```text
Enter report count (0-6):
Enter waiting time 1 (0-20):
Input could not be read
```

<!-- input: waiting_times -->
```text
3
4
abc
```

<!-- output: waiting_times -->
```text
Enter report count (0-6):
Enter waiting time 1 (0-20):
Enter waiting time 2 (0-20):
Input could not be read
```

<!-- input: waiting_times -->
```text
3
```

<!-- output: waiting_times -->
```text
Enter report count (0-6):
Enter waiting time 1 (0-20):
Input could not be read
```

<!-- input: waiting_times -->
```text
3
4
```

<!-- output: waiting_times -->
```text
Enter report count (0-6):
Enter waiting time 1 (0-20):
Enter waiting time 2 (0-20):
Input could not be read
```

<!-- input: waiting_times -->
```text
4
4
25
```

<!-- output: waiting_times -->
```text
Enter report count (0-6):
Enter waiting time 1 (0-20):
Enter waiting time 2 (0-20):
Waiting time 2 skipped
Enter waiting time 3 (0-20):
Input could not be read
```

</details>

An example solution is in [Example solutions](#example-solutions).

## 9. Find the bug: a skipped value gets into the vector

Do this task **after the mission**: the program below shows where `push_back` goes when choosing data, so it could give away the solution. The program reads three scores from 0 to 10 and skips the scores outside that range. We assume you type whole numbers.

<details>
<summary>The program to check: open it after writing your own program</summary>

<!-- example: scores_bug -->
```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<int> scores{};

    std::cout << "Enter 3 scores (0-10):\n";

    for (int number{1}; number <= 3; ++number) {
        int score{0};
        std::cin >> score;

        if (score < 0 || score > 10) {
            std::cout << "Score " << number << " skipped\n";
        }

        scores.push_back(score);
    }

    std::cout << "Stored scores: " << scores.size() << "\n";

    for (const int score : scores) {
        std::cout << score << "\n";
    }
}
```

1. **Predict** how many scores are stored for the data `7`, `4`, `9`, and how many for `7`, `15`, `9`.
2. Run the program with the data `7`, `4`, `9`, only valid scores.
3. Run it with the data `7`, `15`, `9`.
4. Compare both results with the requirement. Why doesn't the first case reveal the bug?
5. Find the place where a score is added to the vector.
6. Fix the structure of the condition so that a skipped score doesn't go into the vector.
7. Check both cases again.

</details>

The program's output before the fix, and the fixed program, are in [Example solutions](#example-solutions).

## 10. When something goes differently

| What you see | What it means | What to do |
|---|---|---|
| `no matching member function for call to 'push_back'` | The vector is `const`, so no elements can be added to it (section 3). | Remove `const` from the definition of a vector that should take elements. |
| `size()` is larger than the number of allowed values | `push_back` also runs for skipped values (section 9). | Check that `push_back` stands only in the branch for an allowed value. |
| The average is a whole number, for example 5 instead of 5.5 | The sum is an `int`, so the division is integer division. | Sum into a `double` variable (section 7). |
| The number of times above the average is too large when some time equals the average | `>=` instead of `>`. | Check the case `3`, `4`, `8`, `12`: the result is 1. |
| An average appears after zero reports or after only skipped times | The `empty()` check before the calculation is missing. | Check `empty()` before you compute the average (section 7). |
| After text, the program asks for more times | The loop doesn't end after a failed read. | End the reading straight away, as in the loops with a flag in lessons 4.5 and 5.7. |
| `Stored waiting times` appears after a failed read | The summary doesn't depend on whether the reads succeeded. | Print the summary only when every read succeeded. |
| The program does nothing and waits | It's waiting for a number, as in lesson 2.6. | Type a number and press **Enter**. |

## 11. Explain

Answer in your own words, preferably in writing. Only then compare with the example answers.

1. Why isn't the vector in the mission `const`, when the vectors in lesson 6.1 were?
2. What does `push_back()` do, and where does the new element go?
3. Does a vector need to know its final number of elements when you create it?
4. What does `size()` give, and what does `empty()` give? Does `empty()` remove elements?
5. Does `push_back()` check by itself whether a value is allowed?
6. Why can the number of reports differ from `size()`, and what happens to a time outside the range?
7. How does a time that isn't allowed differ from a failed read?
8. Why don't we compute the average of an empty vector?
9. Why does a `double` sum protect against integer division?
10. Can the times 0 and 20 be stored?
11. Do we count a time equal to the average as greater than the average?
12. Why do we go through the vector a second time after computing the average, and is the data still in it?

<details>
<summary>Example answers</summary>

1. Because the program adds elements to it, so it changes it. The vectors in lesson 6.1 had all their elements from the start and didn't change, so they had `const`. Nothing can be added to a `const` vector.
2. It adds the given value as a new element at the end of the vector. The earlier elements stay, and `size()` grows by 1.
3. No. A vector can start empty and grow with every `push_back`.
4. `size()` gives the number of elements, and `empty()` gives `true` when the vector has no elements and `false` otherwise. `empty()` only checks; it doesn't remove anything.
5. No. For the vector, every `int` is equally good. Whether a value goes into the vector is decided by the program: it calls `push_back` only for allowed values.
6. Because a time outside the range uses up its report but doesn't go into the vector. The program prints that it was skipped and moves on to the next report.
7. A time that isn't allowed is a number read correctly but outside the range: the program skips it and carries on. A failed read means there's no number at all, for example after text or at the end of the data: the program has nothing to check and ends without a summary.
8. Because there's no value to compute it from. The sum and the number of elements are both 0 then, and such a division doesn't give a meaningful average.
9. Because dividing a `double` value by the number of elements gives a result with a fractional part. If the sum were an `int`, the division would be integer division: for 5 and 6 you'd get 5 instead of 5.5.
10. Yes. The range from 0 to 20 is inclusive, so both ends are allowed.
11. No. The requirement is about times strictly greater than the average, so the condition uses `>`. The case `4`, `8`, `12` checks this: 8 equals the average and doesn't count.
12. Because the average is known only after all the times have been summed, and only then can each time be compared with it. The range-based loop only reads the elements, so after the first pass the vector has the same times in the same order.

</details>

## Summary

- `std::vector<int> values{};` creates an empty vector. No `const`, because the program will add elements to it. A vector that doesn't change still has `const`.
- `values.push_back(value);` adds an element at the end. The order of the elements is the order of the calls, and `size()` grows by 1 with each call.
- `values.empty()` gives `true` when the vector has no elements. It doesn't remove anything.
- `push_back` doesn't check anything. The program decides whether a value goes into the vector, so the number of read attempts can be larger than `size()`.
- Add a value to the vector only after a successful read. First collect the elements, then go through them.
- Check `empty()` before an average. Sum into a `double` to avoid integer division.
- Counting the values greater than the average needs a second pass, because the average is known only after the first.

## What's next

In this lesson, a range-based loop went through the vector, always from the first element to the last. In the next lesson you'll meet the positions of elements: you'll read the first, the last or a chosen element, and compare neighbouring values: [Lesson 6.3: Element positions and neighbouring values in a `std::vector`](lesson_03_positions_and_neighbours.en.md).

---

## Example solutions

Look here **after your own attempt**. Your names may differ, as long as the standard output is as required.

<details>
<summary>Section 8: the mission, waiting times</summary>

<!-- example: waiting_times -->
```cpp
#include <iostream>
#include <vector>

int main() {
    int report_count{0};

    std::cout << "Enter report count (0-6):\n";
    std::cin >> report_count;

    if (std::cin.fail()) {
        std::cout << "Input could not be read\n";
    } else if (report_count < 0 || report_count > 6) {
        std::cout << "Invalid report count\n";
    } else {
        std::vector<int> waiting_times{};
        bool input_failed{false};

        for (int report_number{1}; report_number <= report_count && !input_failed; ++report_number) {
            int waiting_time{0};

            std::cout << "Enter waiting time " << report_number << " (0-20):\n";
            std::cin >> waiting_time;

            if (std::cin.fail()) {
                input_failed = true;
            } else if (waiting_time >= 0 && waiting_time <= 20) {
                waiting_times.push_back(waiting_time);
            } else {
                std::cout << "Waiting time " << report_number << " skipped\n";
            }
        }

        if (input_failed) {
            std::cout << "Input could not be read\n";
        } else {
            std::cout << "Stored waiting times: " << waiting_times.size() << "\n";

            if (waiting_times.empty()) {
                std::cout << "No valid waiting times\n";
            } else {
                double total{0.0};

                for (const int waiting_time : waiting_times) {
                    total += waiting_time;
                }

                const double average{total / waiting_times.size()};
                int above_average{0};

                for (const int waiting_time : waiting_times) {
                    if (waiting_time > average) {
                        ++above_average;
                    }
                }

                std::cout << "Average waiting time: " << average << "\n";
                std::cout << "Times above average: " << above_average << "\n";
            }
        }
    }
}
```

- **Three outcomes of a read**, three branches: a failed read sets the flag, an allowed time goes into the vector, and a time that isn't allowed is skipped with a message. `push_back` stands in only one of them.
- **The loop** runs at most `report_count` times, also when some time is skipped: each pass uses up one report. It ends early only when a read fails, because its condition also checks `!input_failed`. For zero reports it doesn't run at all.
- **`size()`** is the number of stored times, not the number of reports. For example A there are 4 reports, and `size()` gives 3.
- **An empty vector**, after zero reports or after only skipped times, ends with the message `No valid waiting times`, without computing an average.
- **The first pass** sums the times in a `double`, so the average can have a fractional part. **The second** compares each time with the finished average. The condition `waiting_time > average` compares an `int` with a `double`: the time is treated as a `double` for a moment, and its value doesn't change.
- **A failed read:** the earlier questions and messages stay, and instead of a summary the program prints `Input could not be read`.
- The same program can be written with a `while` loop, as in lesson 5.7. What matters is that the loop ends after a failed read, and that `push_back` stands only in the branch for an allowed time.

</details>

<details>
<summary>Section 9: the output before the fix, and the fixed program</summary>

Before the fix, for the data `7`, `4`, `9`:

<!-- input: scores_bug -->
```text
7
4
9
```

<!-- output: scores_bug -->
```text
Enter 3 scores (0-10):
Stored scores: 3
7
4
9
```

For the data `7`, `15`, `9`:

<!-- input: scores_bug -->
```text
7
15
9
```

<!-- output: scores_bug -->
```text
Enter 3 scores (0-10):
Score 2 skipped
Stored scores: 3
7
15
9
```

- With only valid scores the program behaves as required, because every score should go into the vector anyway. Only a score outside the range reveals the bug.
- For `15`, the program prints `Score 2 skipped` and still stores 15: `size()` gives 3 instead of 2, and 15 is in the list.
- **The cause:** `push_back` stands **after** the `if` block, so it runs in every pass, whatever the condition. The "skipped" message doesn't skip anything.
- **The fix:** move the adding into an `else` branch. Then either the message or `push_back` runs, never both.

<!-- example: scores_fixed -->
```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<int> scores{};

    std::cout << "Enter 3 scores (0-10):\n";

    for (int number{1}; number <= 3; ++number) {
        int score{0};
        std::cin >> score;

        if (score < 0 || score > 10) {
            std::cout << "Score " << number << " skipped\n";
        } else {
            scores.push_back(score);
        }
    }

    std::cout << "Stored scores: " << scores.size() << "\n";

    for (const int score : scores) {
        std::cout << score << "\n";
    }
}
```

<!-- input: scores_fixed -->
```text
7
4
9
```

<!-- output: scores_fixed -->
```text
Enter 3 scores (0-10):
Stored scores: 3
7
4
9
```

<!-- input: scores_fixed -->
```text
7
15
9
```

<!-- output: scores_fixed -->
```text
Enter 3 scores (0-10):
Score 2 skipped
Stored scores: 2
7
9
```

</details>

**Previous lesson:** [Lesson 6.1: Your first `std::vector` and the range-based `for` loop](lesson_01_the_first_vector.en.md) · **Next lesson:** [Lesson 6.3: Element positions and neighbouring values in a `std::vector`](lesson_03_positions_and_neighbours.en.md) · [Course overview](../../README.en.md)

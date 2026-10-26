# Lesson 6.6: A training log (the Module 6 test)

[Polski](lesson_06_training_log.md) · **English** · [Course overview](../../README.en.md)

> **Module 6, lesson 6: the test** · about 95–115 minutes, in two sessions
> **You need:** your `cpp-workspace` folder and the original `lesson_05_first_program` project.
> **Pilot version.** The reference solutions in this lesson are checked automatically on Windows, Ubuntu and macOS, with the given input data. Nothing grades your own work automatically: you check it yourself, against the criteria.

## How this test works

This lesson introduces nothing new. You check whether you can design on your own a program that **collects data into a vector, analyses it several times** and uses cooperating functions to prepare a report. You also fix two short programs with bugs and explain your decisions.

The lesson has two parts:

- **Part A: the test.** Requirements, examples, tasks, questions and criteria. No hints and no solution code. Everything you need is from Modules 1–6.
- **Part B: checking and discussion.** Hints, the full list of check cases, the reference solution, fixes, answers and self-assessment. Go there after doing Part A, or when you consciously decide to stop trying on your own.

Looking at Part B, at earlier lessons or at your notes isn't a failure. What matters is that you **honestly note what you did on your own and what with help**. A suggested split into two sessions:

- **first:** designing the functions, writing the program for task 1, checking the functions on their own, and the basic report cases;
- **second:** the boundary cases, task 2, comparing with the solution, task 3 and the self-assessment.

**You may use:** CLion or the terminal, CMake and Ninja, as before; a `CMakeLists.txt` copied from the original `lesson_05_first_program`; trace and case tables, and temporary test printouts. You won't need the debugger. You don't need to end the data from the keyboard: you analyse the cases where the data ends early on paper.

---

# Part A: the test

## Task 1: A training log

The program analyses training time on successive days. The user gives the number of days, then the number of training minutes on each day. The program **stores every measurement** and answers three questions:

- What was the average training time?
- Which stored values were greater than the average?
- How many times was a day's result better than the previous day's?

**Preparation:** in `cpp-workspace`, create a folder `training_log`, copy `CMakeLists.txt` from the original `lesson_05_first_program` into it, create an **empty** `main.cpp` and write the whole program on your own.

### Input data

- The program asks `Enter training day count (1-7):` and reads the number of days, a whole number.
- If the read fails, it prints `Input could not be read` and ends. If the number is outside the range 1 to 7, it prints `Invalid day count` and ends.
- For each day, from 1 to the given number, it asks `Enter minutes for day N (0-30):` and reads the number of minutes, a whole number. Values from 0 to 30 inclusive are valid, 0 included.
- If reading the minutes fails, for example after text or when the data ends early, the program prints `Input could not be read` and ends. If the number of minutes is outside the range, it prints `Invalid training data` and ends.
- After an error, the program doesn't ask about further days, doesn't store the wrong value and prints no part of the report. Questions printed earlier stay. **Unlike lesson 6.2:** a value outside the range isn't skipped; it ends the program.

### The report

Only after reading every day correctly does the program print:

- `Recorded days: N`: the number of recorded days;
- `Average training minutes: X`: the average number of minutes, with a fractional part if there is one;
- `Days above average: N`: the number of stored values **strictly greater** than the average;
- `Above-average minutes:` followed, after a space, by those values, in the order of the days, separated by spaces, with repetitions and with no space at the end of the line, or `Above-average minutes: none` when there are no such values;
- `Improved days: N`: the number of days whose result was **greater** than the previous day's. The first day has no previous day. An equal result isn't an improvement.

The program prints no other messages.

### The functions

The program has at least three of your own calculating functions:

1. a function computing the average of the stored measurements;
2. a function creating a **new vector** of the values greater than a given threshold;
3. a function counting the days that improved on the previous day.

**Requirements for the functions:**

- They get vectors through `const std::vector<int>&`. The function creating a new vector returns it by value.
- They don't read the input, don't print the report and don't change the data passed to them.
- You choose the names, the other parameters, the result types and the order of the calls yourself. The functions don't have to call each other: they can cooperate through `main`, which passes the result of one function to another.
- **The average function gets only a non-empty vector.** The average of an empty set doesn't exist in our model, so don't invent an artificial result for it. Write this requirement in a comment next to the function. `main` makes sure of it: it computes the average only after reading from 1 to 7 valid days.

`main` reads the data, checks it, stores the valid values in a vector, calls the functions and prints the report. It doesn't repeat the calculating algorithms. Don't use variables declared outside functions.

### Examples

**Example A:** five days, 10, 14, 8, 18 and 10 minutes.

<!-- input: training_log -->
```text
5
10
14
8
18
10
```

<!-- output: training_log -->
```text
Enter training day count (1-7):
Enter minutes for day 1 (0-30):
Enter minutes for day 2 (0-30):
Enter minutes for day 3 (0-30):
Enter minutes for day 4 (0-30):
Enter minutes for day 5 (0-30):
Recorded days: 5
Average training minutes: 12
Days above average: 2
Above-average minutes: 14 18
Improved days: 2
```

The total is 60 minutes, so the average is 12. Above the average are 14 and 18. There were two improvements: from 10 to 14 and from 8 to 18.

**Example B:** one day, 7 minutes.

<!-- input: training_log -->
```text
1
7
```

<!-- output: training_log -->
```text
Enter training day count (1-7):
Enter minutes for day 1 (0-30):
Recorded days: 1
Average training minutes: 7
Days above average: 0
Above-average minutes: none
Improved days: 0
```

One day is enough to compute the average. The only result equals it, so it isn't greater than the average. One day makes no pair, so there's no improvement.

**Example C:** three days, 5, 7 and 9 minutes. **Predict** the whole report before you write the program.

<!-- input: training_log -->
```text
3
5
7
9
```

<details>
<summary>Standard output for example C</summary>

<!-- output: training_log -->
```text
Enter training day count (1-7):
Enter minutes for day 1 (0-30):
Enter minutes for day 2 (0-30):
Enter minutes for day 3 (0-30):
Recorded days: 3
Average training minutes: 7
Days above average: 1
Above-average minutes: 9
Improved days: 2
```

The average is 7, and the value 7 equals it, so the new vector holds only 9.

</details>

### How to work

1. **Design the functions before you start writing `main`.** For each, write in one sentence its task, its parameters and its result type.
2. **Prepare a table of cases:** one day, seven days, all equal values, an average with a fractional part, a value equal to the average, repeated values above the average, no improvement, an improvement only in the last pair, equal neighbouring days, the bounds 0 and 30, day counts of 0 and 8, minutes of -1 and 31, text instead of a number, and data that ends early. For each, write down the expected report or message.
3. **Check each function on its own** with test printouts, using vectors written in the code:
   - the average for one measurement, several equal values and a set with a fractional average, **never for an empty vector**;
   - the new vector for no results, one result and several results, a value exactly equal to the threshold, and an empty input;
   - the improvements for an empty vector, one element, two rising values, two falling values, two equal values, and a longer set with an improvement only at the end.
4. **Remove the test printouts** and put the report together.
5. **Run the whole program** for examples A, B and C and for 2–3 other cases from your table. Every case in the full list of check cases is checked automatically, so you don't need to type them all. Analyse the cases where the data ends early on paper.

When the result matches, you can save the project in Git, as in lesson 1.5. Before you commit, check `git status`: only `main.cpp` and `CMakeLists.txt` go into the history.

## Task 2: Two bug reports

Do this task **after task 1**: both programs contain functions similar to the ones you're designing. Each program checks one function with two tests written in the code, like the test printouts in task 1. In `cpp-workspace`, create a folder `diagnosis_6`, copy `main.cpp` and `CMakeLists.txt` from the original `lesson_05_first_program` into it, and type the programs into `main.cpp` one after the other.

<details>
<summary>Report A: a value equal to the average</summary>

The requirement: the new vector holds the values **strictly greater** than the average.

<!-- example: above_average_bug -->
```cpp
#include <iostream>
#include <vector>

// values must not be empty
double average_of(const std::vector<int>& values) {
    double total{0.0};

    for (const int value : values) {
        total += value;
    }

    return total / values.size();
}

std::vector<int> values_above(const std::vector<int>& values, double threshold) {
    std::vector<int> selected{};

    for (const int value : values) {
        if (value >= threshold) {
            selected.push_back(value);
        }
    }

    return selected;
}

int main() {
    const std::vector<int> first_test{5, 7};
    const std::vector<int> second_test{5, 7, 9};

    const std::vector<int> first_result{values_above(first_test, average_of(first_test))};
    const std::vector<int> second_result{values_above(second_test, average_of(second_test))};

    std::cout << "Test {5, 7}:";
    for (const int value : first_result) {
        std::cout << " " << value;
    }
    std::cout << "\n";

    std::cout << "Test {5, 7, 9}:";
    for (const int value : second_result) {
        std::cout << " " << value;
    }
    std::cout << "\n";
}
```

1. **Predict** which values should be in both results. The averages are 6 and 7.
2. Run the program and compare with your prediction.
3. Why doesn't the first test reveal the bug?
4. Find the wrong condition and fix it.
5. Run both tests again.

</details>

<details>
<summary>Report B: a skipped pair</summary>

The requirement: the function counts the days whose result was greater than the previous day's, for **every** pair of consecutive days.

<!-- example: improvements_bug -->
```cpp
#include <cstddef>
#include <iostream>
#include <vector>

int count_improvements(const std::vector<int>& values) {
    int improvements{0};

    for (std::size_t index{1}; index + 1 < values.size(); ++index) {
        if (values[index] > values[index - 1]) {
            ++improvements;
        }
    }

    return improvements;
}

int main() {
    const std::vector<int> first_test{10, 8, 6};
    const std::vector<int> second_test{10, 8, 12};

    std::cout << "Test {10, 8, 6}: " << count_improvements(first_test) << "\n";
    std::cout << "Test {10, 8, 12}: " << count_improvements(second_test) << "\n";
}
```

1. **Predict** the correct results of both tests.
2. Trace the indices for `{10, 8, 12}`: which index does the loop start at, at which index does it end, and which pairs does it compare?
3. Run the program. Why doesn't the first test reveal the bug?
4. Find the pair the program doesn't compare, and fix the loop's condition.
5. Check the fixed function also for an empty and a one-element vector.

</details>

## Task 3: Explain your design

Answer briefly, in writing, referring to your own program from task 1:

1. Why does the program need a vector, instead of computing everything while reading?
2. Why do your calculating functions take the vector through `const&`?
3. Why does the average function need non-empty data, and what in your program guarantees that this holds?
4. Why does the function choosing values create a new vector? Does the original vector change?
5. Why don't values equal to the average go into the result?
6. Why does the loop comparing neighbouring days start at index 1, and what type is its index?
7. Why does one day give zero improvements?
8. Why does the report appear only after every day has been read?
9. Why doesn't each function being correct on its own guarantee a correct report?

## Success criteria

You pass the test when you meet **all** the criteria. You may use Part B while doing so, as long as you note it honestly in the self-assessment.

- `training_log/main.cpp` was written from an empty file, in valid C++20. The program builds without errors.
- The program stores the valid measurements in a `std::vector<int>`, adding them with `push_back`, and computes the report only after reading every day.
- There are three calculating functions with the tasks from the requirements. They take vectors through `const std::vector<int>&`, read and print nothing, and the function choosing values returns a new `std::vector<int>`.
- The average function sums in a `double` and is called only with a non-empty vector, and its requirement is written in a comment.
- The loop comparing neighbouring days has a `std::size_t` index, compares every pair and reads no element out of range.
- The standard output for examples A, B and C and for the cases that can be typed matches the requirements. The cases where the data ends early match your trace table.
- After an input error, a wrong day count or a wrong number of minutes, no part of the report appears.
- The functions were checked on their own with test printouts, and the final program contains no such printouts.
- Both bug reports in task 2 were diagnosed and fixed, and the fixes were checked.
- You can explain every line of your program and answer the questions in task 3.

The names of the functions and variables, and the split of the program, may differ from the reference solution, as long as they're readable and meet the requirements. A correct result is a necessary condition, but **not proof of understanding**. That's why tasks 2 and 3 are part of the test.

---

# Part B: checking and discussion

Come here after doing Part A, or when you consciously decide to stop trying on your own.

## How to check your work

- **Standard output:** run the program for the examples and a few cases from your table, and compare the program's lines with the expected ones, character by character. Ignore the typed data visible because of the echo.
- **End of the data:** check the cases where the data ends with a trace table, and compare them with the full list of check cases. Each of them is checked automatically there.
- **Functions:** does each have a task you can describe in one sentence? Does some algorithm also appear in `main`?
- **Data:** is the vector built only from valid values, and does no function change it?

## Hints

<details>
<summary>Hint 1</summary>

Which calculations use all the stored data, and which need access to neighbouring elements?

</details>

<details>
<summary>Hint 2</summary>

First compute the average of a non-empty vector. Then use it as the threshold for the function that creates a new collection.

</details>

<details>
<summary>Hint 3</summary>

To count the improvements, compare the current day with the previous one, starting from the second element. Remember that the first day has no previous day.

</details>

## The full list of check cases

<details>
<summary>Open it after preparing your own table</summary>

Examples A, B and C are checked in Part A. Every case below is checked automatically, with the reference solution.

**Valid logs:**

| Minutes | Average | Above the average | Improvements | What it checks |
|---|---|---|---|---|
| `10, 14, 8, 18, 10` | 12 | `14 18` | 2 | example A |
| `7` | 7 | `none` | 0 | example B: one day |
| `5, 7, 9` | 7 | `9` | 2 | example C: a value equal to the average |
| `5, 6` | 5.5 | `6` | 1 | an average with a fractional part |
| `10, 10, 10, 10` | 10 | `none` | 0 | all equal: no results and no improvements |
| `18, 12, 6, 0` | 9 | `18 12` | 0 | only falls |
| `2, 4, 6, 8, 10` | 6 | `8 10` | 4 | only improvements |
| `0, 30, 0, 30, 0` | 12 | `30 30` | 2 | the bounds 0 and 30, repetitions in the result |
| `0, 5, 10, 15, 20, 25, 30` | 15 | `20 25 30` | 6 | seven days |
| `30, 0` | 15 | `30` | 0 | two days, a fall |
| `10, 20, 0` | 10 | `20` | 1 | a value equal to the average and an improvement in the middle |
| `0, 0, 0` | 0 | `none` | 0 | all zeros |
| `30, 30, 30` | 30 | `none` | 0 | all at the maximum |
| `10, 8, 12` | 10 | `12` | 1 | an improvement only in the last pair |

**Invalid data and the end of the data:**

| Data | Result after the questions | What it checks |
|---|---|---|
| `0` | `Invalid day count` | a day count just below the range |
| `8` | `Invalid day count` | a day count just above the range |
| `-1` | `Invalid day count` | a negative day count |
| `abc` | `Input could not be read` | text instead of the day count |
| no data | `Input could not be read` | the data ends straight away |
| `3`, `-1` | the question for day 1, then `Invalid training data` | minutes just below the range |
| `3`, `31` | the question for day 1, then `Invalid training data` | minutes just above the range |
| `3`, `10`, `31` | the questions for days 1 and 2, then `Invalid training data` | a wrong value after a valid one |
| `3`, `abc` | the question for day 1, then `Input could not be read` | text instead of the first value |
| `3`, `10`, `abc` | the questions for days 1 and 2, then `Input could not be read` | text instead of a later value |
| `3`, end of data | the question for day 1, then `Input could not be read` | no first day |
| `3`, `10`, end of data | the questions for days 1 and 2, then `Input could not be read` | the data ends after one day |
| `5`, `10`, `14`, `8`, end of data | the questions for days 1–4, then `Input could not be read` | the data ends after several days |

In none of these cases does any line of the report appear.

<!-- input: training_log -->
```text
2
5
6
```

<!-- output: training_log -->
```text
Enter training day count (1-7):
Enter minutes for day 1 (0-30):
Enter minutes for day 2 (0-30):
Recorded days: 2
Average training minutes: 5.5
Days above average: 1
Above-average minutes: 6
Improved days: 1
```

<!-- input: training_log -->
```text
4
10
10
10
10
```

<!-- output: training_log -->
```text
Enter training day count (1-7):
Enter minutes for day 1 (0-30):
Enter minutes for day 2 (0-30):
Enter minutes for day 3 (0-30):
Enter minutes for day 4 (0-30):
Recorded days: 4
Average training minutes: 10
Days above average: 0
Above-average minutes: none
Improved days: 0
```

<!-- input: training_log -->
```text
4
18
12
6
0
```

<!-- output: training_log -->
```text
Enter training day count (1-7):
Enter minutes for day 1 (0-30):
Enter minutes for day 2 (0-30):
Enter minutes for day 3 (0-30):
Enter minutes for day 4 (0-30):
Recorded days: 4
Average training minutes: 9
Days above average: 2
Above-average minutes: 18 12
Improved days: 0
```

<!-- input: training_log -->
```text
5
2
4
6
8
10
```

<!-- output: training_log -->
```text
Enter training day count (1-7):
Enter minutes for day 1 (0-30):
Enter minutes for day 2 (0-30):
Enter minutes for day 3 (0-30):
Enter minutes for day 4 (0-30):
Enter minutes for day 5 (0-30):
Recorded days: 5
Average training minutes: 6
Days above average: 2
Above-average minutes: 8 10
Improved days: 4
```

<!-- input: training_log -->
```text
5
0
30
0
30
0
```

<!-- output: training_log -->
```text
Enter training day count (1-7):
Enter minutes for day 1 (0-30):
Enter minutes for day 2 (0-30):
Enter minutes for day 3 (0-30):
Enter minutes for day 4 (0-30):
Enter minutes for day 5 (0-30):
Recorded days: 5
Average training minutes: 12
Days above average: 2
Above-average minutes: 30 30
Improved days: 2
```

<!-- input: training_log -->
```text
7
0
5
10
15
20
25
30
```

<!-- output: training_log -->
```text
Enter training day count (1-7):
Enter minutes for day 1 (0-30):
Enter minutes for day 2 (0-30):
Enter minutes for day 3 (0-30):
Enter minutes for day 4 (0-30):
Enter minutes for day 5 (0-30):
Enter minutes for day 6 (0-30):
Enter minutes for day 7 (0-30):
Recorded days: 7
Average training minutes: 15
Days above average: 3
Above-average minutes: 20 25 30
Improved days: 6
```

<!-- input: training_log -->
```text
2
30
0
```

<!-- output: training_log -->
```text
Enter training day count (1-7):
Enter minutes for day 1 (0-30):
Enter minutes for day 2 (0-30):
Recorded days: 2
Average training minutes: 15
Days above average: 1
Above-average minutes: 30
Improved days: 0
```

<!-- input: training_log -->
```text
3
10
20
0
```

<!-- output: training_log -->
```text
Enter training day count (1-7):
Enter minutes for day 1 (0-30):
Enter minutes for day 2 (0-30):
Enter minutes for day 3 (0-30):
Recorded days: 3
Average training minutes: 10
Days above average: 1
Above-average minutes: 20
Improved days: 1
```

<!-- input: training_log -->
```text
3
0
0
0
```

<!-- output: training_log -->
```text
Enter training day count (1-7):
Enter minutes for day 1 (0-30):
Enter minutes for day 2 (0-30):
Enter minutes for day 3 (0-30):
Recorded days: 3
Average training minutes: 0
Days above average: 0
Above-average minutes: none
Improved days: 0
```

<!-- input: training_log -->
```text
3
30
30
30
```

<!-- output: training_log -->
```text
Enter training day count (1-7):
Enter minutes for day 1 (0-30):
Enter minutes for day 2 (0-30):
Enter minutes for day 3 (0-30):
Recorded days: 3
Average training minutes: 30
Days above average: 0
Above-average minutes: none
Improved days: 0
```

<!-- input: training_log -->
```text
3
10
8
12
```

<!-- output: training_log -->
```text
Enter training day count (1-7):
Enter minutes for day 1 (0-30):
Enter minutes for day 2 (0-30):
Enter minutes for day 3 (0-30):
Recorded days: 3
Average training minutes: 10
Days above average: 1
Above-average minutes: 12
Improved days: 1
```

<!-- input: training_log -->
```text
0
```

<!-- output: training_log -->
```text
Enter training day count (1-7):
Invalid day count
```

<!-- input: training_log -->
```text
8
```

<!-- output: training_log -->
```text
Enter training day count (1-7):
Invalid day count
```

<!-- input: training_log -->
```text
-1
```

<!-- output: training_log -->
```text
Enter training day count (1-7):
Invalid day count
```

<!-- input: training_log -->
```text
abc
```

<!-- output: training_log -->
```text
Enter training day count (1-7):
Input could not be read
```

<!-- input: training_log -->
```text
```

<!-- output: training_log -->
```text
Enter training day count (1-7):
Input could not be read
```

<!-- input: training_log -->
```text
3
-1
```

<!-- output: training_log -->
```text
Enter training day count (1-7):
Enter minutes for day 1 (0-30):
Invalid training data
```

<!-- input: training_log -->
```text
3
31
```

<!-- output: training_log -->
```text
Enter training day count (1-7):
Enter minutes for day 1 (0-30):
Invalid training data
```

<!-- input: training_log -->
```text
3
10
31
```

<!-- output: training_log -->
```text
Enter training day count (1-7):
Enter minutes for day 1 (0-30):
Enter minutes for day 2 (0-30):
Invalid training data
```

<!-- input: training_log -->
```text
3
abc
```

<!-- output: training_log -->
```text
Enter training day count (1-7):
Enter minutes for day 1 (0-30):
Input could not be read
```

<!-- input: training_log -->
```text
3
10
abc
```

<!-- output: training_log -->
```text
Enter training day count (1-7):
Enter minutes for day 1 (0-30):
Enter minutes for day 2 (0-30):
Input could not be read
```

<!-- input: training_log -->
```text
3
```

<!-- output: training_log -->
```text
Enter training day count (1-7):
Enter minutes for day 1 (0-30):
Input could not be read
```

<!-- input: training_log -->
```text
3
10
```

<!-- output: training_log -->
```text
Enter training day count (1-7):
Enter minutes for day 1 (0-30):
Enter minutes for day 2 (0-30):
Input could not be read
```

<!-- input: training_log -->
```text
5
10
14
8
```

<!-- output: training_log -->
```text
Enter training day count (1-7):
Enter minutes for day 1 (0-30):
Enter minutes for day 2 (0-30):
Enter minutes for day 3 (0-30):
Enter minutes for day 4 (0-30):
Input could not be read
```

</details>

## The reference solution

<details>
<summary>Task 1: the training log</summary>

<!-- example: training_log -->
```cpp
#include <cstddef>
#include <iostream>
#include <vector>

// values must not be empty
double average_of(const std::vector<int>& values) {
    double total{0.0};

    for (const int value : values) {
        total += value;
    }

    return total / values.size();
}

std::vector<int> values_above(const std::vector<int>& values, double threshold) {
    std::vector<int> selected{};

    for (const int value : values) {
        if (value > threshold) {
            selected.push_back(value);
        }
    }

    return selected;
}

int count_improvements(const std::vector<int>& values) {
    int improvements{0};

    for (std::size_t index{1}; index < values.size(); ++index) {
        if (values[index] > values[index - 1]) {
            ++improvements;
        }
    }

    return improvements;
}

int main() {
    int day_count{0};

    std::cout << "Enter training day count (1-7):\n";
    std::cin >> day_count;

    if (std::cin.fail()) {
        std::cout << "Input could not be read\n";
    } else if (day_count < 1 || day_count > 7) {
        std::cout << "Invalid day count\n";
    } else {
        std::vector<int> minutes{};
        bool input_failed{false};
        bool invalid_data{false};

        for (int day{1}; day <= day_count && !input_failed && !invalid_data; ++day) {
            int day_minutes{0};

            std::cout << "Enter minutes for day " << day << " (0-30):\n";
            std::cin >> day_minutes;

            if (std::cin.fail()) {
                input_failed = true;
            } else if (day_minutes < 0 || day_minutes > 30) {
                invalid_data = true;
            } else {
                minutes.push_back(day_minutes);
            }
        }

        if (input_failed) {
            std::cout << "Input could not be read\n";
        } else if (invalid_data) {
            std::cout << "Invalid training data\n";
        } else {
            const double average{average_of(minutes)};
            const std::vector<int> above_average{values_above(minutes, average)};
            const int improved_days{count_improvements(minutes)};

            std::cout << "Recorded days: " << minutes.size() << "\n";
            std::cout << "Average training minutes: " << average << "\n";
            std::cout << "Days above average: " << above_average.size() << "\n";

            std::cout << "Above-average minutes:";
            if (above_average.empty()) {
                std::cout << " none";
            } else {
                for (const int value : above_average) {
                    std::cout << " " << value;
                }
            }
            std::cout << "\n";

            std::cout << "Improved days: " << improved_days << "\n";
        }
    }
}
```

| Function | Task | Parameters | Result |
|---|---|---|---|
| `average_of` | the average of a non-empty vector | the vector through `const&` | `double` |
| `values_above` | a new vector of the values strictly greater than the threshold, in their order | the vector through `const&`, a `double` threshold | `std::vector<int>` |
| `count_improvements` | the number of days better than the previous one | the vector through `const&` | `int` |
| `main` | reading, checking the data, calling the functions, the report | — | — |

**The flow of the data for example A:**

| Step | What happens |
|---|---|
| 1 | `main` reads the number of days: 5. |
| 2 | After five valid reads, `minutes` is `{10, 14, 8, 18, 10}`. |
| 3 | `main` calls `average_of(minutes)`: the vector has five elements, so the requirement holds. |
| 4 | The function returns 12, and `main` stores it in `average`. |
| 5 | `main` passes `minutes`, and `average` as the threshold, to `values_above`. |
| 6 | The function returns the new vector `{14, 18}`, stored in `above_average`. `minutes` doesn't change. |
| 7 | `count_improvements(minutes)` compares the pairs of days 2–1, 3–2, 4–3 and 5–4. |
| 8 | There's an improvement in the pairs 2–1 and 4–3, so the function returns 2. |
| 9 | `main` builds the report from `minutes.size()`, `average`, `above_average` and `improved_days`. |

**Discussion:**

1. **The whole log first.** The values above the average can be pointed out only once the average is known, and that needs every measurement. That's why the program stores them in a vector and analyses them after reading, as in lessons 6.1 and 6.2.
2. **Three functions, three tasks:** the average, choosing values, and counting improvements. Each gets the vector through `const&`, because it only reads it.
3. **Arguments and results:** `average_of` returns a `double`; `values_above` also gets a `double` threshold, because the average can have a fractional part, and returns a `std::vector<int>`; `count_improvements` returns an `int`.
4. **The average before choosing:** the average is the threshold for `values_above`, so it has to be computed first. `main` passes the result of one function to the other.
5. **A new collection:** `values_above` builds a separate vector and returns it by value, as in lesson 6.5. The original stays unchanged and is still used to count improvements.
6. **An improvement on the previous day:** the loop starts at index 1, because the first day has no previous day, and the condition `index < values.size()` includes the last pair. For an empty and a one-element vector the loop makes no passes.
7. **The average's requirement:** the function divides by `values.size()`, so the vector mustn't be empty. `main` calls it only after reading from 1 to 7 valid days. When the reading fails, no calculating function is called.
8. **The report after a full read:** two flags end the loop at the first error. The branches after the loop choose the error message or the report, so incomplete data never reaches the calculations.
9. **No references that allow changes:** no function changes the caller's data. The result vector is returned, not written into an argument.

This is one possible split. Other designs are also correct, for example different names, a separate `void` function printing the list of values, or the average function called inside the choosing function, as long as the calculating functions print nothing and the non-empty requirement of the average is kept.

</details>

## The bug reports: results and fixes

<details>
<summary>Report A: a value equal to the average</summary>

Before the fix:

<!-- output: above_average_bug -->
```text
Test {5, 7}: 7
Test {5, 7, 9}: 7 9
```

- For `{5, 7}` the average is 6, and no value equals it, so the result `7` is correct and the bug doesn't show.
- For `{5, 7, 9}` the average is 7, and the result also contains 7. The requirement is about values **strictly** greater.
- **The cause:** the condition `value >= threshold`.
- **The fix:** `value > threshold`.

<!-- example: above_average_fixed -->
```cpp
#include <iostream>
#include <vector>

// values must not be empty
double average_of(const std::vector<int>& values) {
    double total{0.0};

    for (const int value : values) {
        total += value;
    }

    return total / values.size();
}

std::vector<int> values_above(const std::vector<int>& values, double threshold) {
    std::vector<int> selected{};

    for (const int value : values) {
        if (value > threshold) {
            selected.push_back(value);
        }
    }

    return selected;
}

int main() {
    const std::vector<int> first_test{5, 7};
    const std::vector<int> second_test{5, 7, 9};

    const std::vector<int> first_result{values_above(first_test, average_of(first_test))};
    const std::vector<int> second_result{values_above(second_test, average_of(second_test))};

    std::cout << "Test {5, 7}:";
    for (const int value : first_result) {
        std::cout << " " << value;
    }
    std::cout << "\n";

    std::cout << "Test {5, 7, 9}:";
    for (const int value : second_result) {
        std::cout << " " << value;
    }
    std::cout << "\n";
}
```

<!-- output: above_average_fixed -->
```text
Test {5, 7}: 7
Test {5, 7, 9}: 9
```

</details>

<details>
<summary>Report B: a skipped pair</summary>

Before the fix:

<!-- output: improvements_bug -->
```text
Test {10, 8, 6}: 0
Test {10, 8, 12}: 0
```

- For `{10, 8, 6}` there's no improvement in any pair, so the result 0 is correct and the bug doesn't show.
- For `{10, 8, 12}` the correct result is 1: day 3 (12) is better than day 2 (8).
- **Tracing the indices:** the vector has 3 elements. The loop starts at index 1: `1 + 1 < 3` gives `true`, so it compares `values[1]` with `values[0]`, 8 with 10. For index 2: `2 + 1 < 3` gives `false`, so the loop ends **before** comparing `values[2]` with `values[1]`, the last pair.
- **The cause:** the condition `index + 1 < values.size()` ends the loop one pass too early. There's no read out of range here: the program simply skips the last pair.
- **The fix:** `index < values.size()`, as in lesson 6.3. Then the last pass has `index` equal to `size() - 1` and compares the last element with the previous one.

<!-- example: improvements_fixed -->
```cpp
#include <cstddef>
#include <iostream>
#include <vector>

int count_improvements(const std::vector<int>& values) {
    int improvements{0};

    for (std::size_t index{1}; index < values.size(); ++index) {
        if (values[index] > values[index - 1]) {
            ++improvements;
        }
    }

    return improvements;
}

int main() {
    const std::vector<int> first_test{10, 8, 6};
    const std::vector<int> second_test{10, 8, 12};
    const std::vector<int> one_day{7};
    const std::vector<int> no_days{};

    std::cout << "Test {10, 8, 6}: " << count_improvements(first_test) << "\n";
    std::cout << "Test {10, 8, 12}: " << count_improvements(second_test) << "\n";
    std::cout << "Test {7}: " << count_improvements(one_day) << "\n";
    std::cout << "Test {}: " << count_improvements(no_days) << "\n";
}
```

<!-- output: improvements_fixed -->
```text
Test {10, 8, 6}: 0
Test {10, 8, 12}: 1
Test {7}: 0
Test {}: 0
```

For a one-element and an empty vector, the loop from index 1 makes no passes, so the function returns 0.

</details>

## Answers to task 3

<details>
<summary>Example answers</summary>

1. Because the values above the average can be pointed out only after the average has been computed, and that needs every measurement. While reading, the average isn't known yet, so the measurements have to be stored and gone through again.
2. Because they only read the measurements: they don't need a copy and can't change them through the parameter.
3. Because it divides the sum by the number of elements, and the average of an empty set doesn't exist in our model. `main` guarantees it: the day count has to be from 1 to 7, and the function is called only after every day has been read without an error.
4. Because the result is a different set of data from the input, and the function mustn't change the measurements. The original vector stays unchanged, because the function gets it through `const&`.
5. Because the requirement is about values strictly greater than the average, so the condition is `>`. Example C checks this.
6. Because we compare each day with the previous one, and the day at index 0 has no previous day. The index is of type `std::size_t`, like the result of `size()`.
7. Because one day makes no pair of consecutive days. The loop from index 1 then makes no passes at all.
8. Because the report describes the whole log. When the reading fails or the data is invalid, the log is incomplete, and the average function could get an empty vector.
9. Because the report also depends on `main`: on the order of the calls, on the arguments passed, for example the threshold, and on how the results are printed. Each function can work correctly and the report can still be wrong.

</details>

## Self-assessment

For each criterion, mark one answer:

| Criterion | On my own | With a hint | After looking at the solution | To revise |
|---|---|---|---|---|
| Designing the three functions and their tasks | | | | |
| Storing the measurements in a vector with `push_back` | | | | |
| Reading and checking the data, the end of the data | | | | |
| The average in a `double` and the non-empty requirement | | | | |
| The function returning a new vector | | | | |
| The loop over neighbouring days and the `std::size_t` index | | | | |
| The report with `none` and no space at the end | | | | |
| Test printouts of the functions | | | | |
| A table of cases with the bounds | | | | |
| Report A (a value equal to the average) | | | | |
| Report B (a skipped pair) | | | | |
| The explanations in task 3 | | | | |

If anything is marked in the "To revise" column, go back to the relevant lesson:

| Topic | Lesson |
|---|---|
| a vector and the range-based loop | [6.1](lesson_01_the_first_vector.en.md) |
| adding elements, an empty vector and the average | [6.2](lesson_02_adding_to_a_vector.en.md) |
| indices, `std::size_t` and neighbouring elements | [6.3](lesson_03_positions_and_neighbours.en.md) |
| a vector as a `const&` parameter | [6.4](lesson_04_a_vector_as_a_parameter.en.md) |
| a function returning a new vector | [6.5](lesson_05_a_function_returns_a_vector.en.md) |
| splitting responsibilities and test printouts | [5.5](../module_05_functions/lesson_05_several_functions.en.md) |
| declaration and definition | [5.6](../module_05_functions/lesson_06_declaration_and_definition.en.md) |
| reading data, flags and loops | [4.5](../module_04_repeating_actions/lesson_05_ask_again.en.md), [4.6](../module_04_repeating_actions/lesson_06_recover_and_end_of_input.en.md), [4.7](../module_04_repeating_actions/lesson_07_the_program_repeats.en.md) |

Then try the task again, for example with a different range of minutes, or with the values below the average instead of above.

---

## Module 6 summary

After six lessons, you can:

- store many values of the same type in a `std::vector<int>` and go through them with a range-based loop;
- add elements with `push_back`, check `size()` and `empty()`, and tell read attempts from stored elements;
- compute an average without integer division, and only when there's data;
- read elements through an index, keep indices in `std::size_t` and safely compare neighbouring elements;
- pass a vector to a function through `const&`, without copying or changing it;
- return a new vector from a function and keep working with it;
- design programs that collect data, analyse it several times and build a report from the results of cooperating functions.

These are the basics of working with collections. Vectors have many more possibilities, which you'll meet in later modules.

## What's next

In Module 7, "Text as a sequence of characters: `std::string` and `char`", you'll go through a text character by character, like the elements of a vector. Start with the first characters: [Lesson 7.1: First characters: `char` and going through a `std::string`](../module_07_text/lesson_01_first_characters.en.md).

**Previous lesson:** [Lesson 6.5: A function creates and returns a new vector](lesson_05_a_function_returns_a_vector.en.md) · **Next lesson:** [Lesson 7.1: First characters: `char` and going through a `std::string`](../module_07_text/lesson_01_first_characters.en.md) · [Course overview](../../README.en.md)

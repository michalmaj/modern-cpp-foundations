# Lesson 6.4: A vector as a function parameter: `const&`

[Polski](lesson_04_a_vector_as_a_parameter.md) · **English** · [Course overview](../../README.en.md)

> **Module 6, lesson 4** · about 70–85 minutes
> **You need:** your `cpp-workspace` folder and the original `lesson_05_first_program` project, as before. You won't need the debugger in this lesson.
> **Pilot version.** The programs in this lesson are checked automatically on Windows, Ubuntu and macOS, including with the given input data. Typing input in CLion's **Run** window is described without a manual check on every system.

## Before you start

This lesson assumes that after Module 5 and lessons 6.1–6.3 you:

- define your own functions with parameters and a result, before `main` (lessons 5.1–5.3);
- know that an `int` parameter gets its own copy of the argument's value (lesson 5.2);
- split a program into calculating functions and a `main` that prints the results, and check functions with test printouts (lesson 5.5);
- go through a vector with a range-based loop, add elements with `push_back` and check `empty()` (lessons 6.1–6.3).

## The situation

Functions and vectors have been separate topics so far: functions got single numbers, and `main` processed the vectors. Two stations recorded temperatures:

<!-- fragment -->
```cpp
const std::vector<int> north_temperatures{3, -2, 0, -5};
const std::vector<int> south_temperatures{7, 4, 2};
```

For each station you want to count the days with a temperature below zero. You know the loop that counts them. But you don't want to write it twice. In lesson 5.5, such a piece of code went into a function: **a calculation with a clear task that has to work for different data is a good candidate for a function.** But how do you pass a function **all** the readings from a chosen vector? A separate `int` parameter for each reading is out of the question: the vectors have different lengths.

After this lesson you will:

- write functions with a `const std::vector<int>&` parameter and explain the roles of `const` and `&`;
- explain why such a function doesn't create a copy of the whole vector;
- call the same function for different vectors and use its result in `main`;
- combine, in one function, a vector parameter with an `int` parameter passed by value;
- design a sensible result of a function for an empty vector;
- check functions on vectors, empty ones included, and detect a mixed-up argument in a call.

## 1. Prepare the project

In `cpp-workspace`, create a folder `lesson_6_4` and copy `main.cpp` and `CMakeLists.txt` from the original `lesson_05_first_program` into it. You type the programs from sections 2–6 into `main.cpp` in this folder.

## 2. Your first function that gets a vector

<!-- example: cold_days -->
```cpp
#include <iostream>
#include <vector>

int count_cold_days(const std::vector<int>& temperatures) {
    int cold_days{0};

    for (const int temperature : temperatures) {
        if (temperature < 0) {
            ++cold_days;
        }
    }

    return cold_days;
}

int main() {
    const std::vector<int> north_temperatures{3, -2, 0, -5};
    const std::vector<int> south_temperatures{7, 4, 2};

    std::cout << "North cold days: " << count_cold_days(north_temperatures) << "\n";
    std::cout << "South cold days: " << count_cold_days(south_temperatures) << "\n";
}
```

**Predict** both lines of output and run the program.

<details>
<summary>Standard output</summary>

<!-- output: cold_days -->
```text
North cold days: 2
South cold days: 0
```

</details>

- `temperatures` is the **name of the parameter**. There's no vector with that name in `main`: the function doesn't need to know the names of the vectors in `main`. Any `std::vector<int>` can be the argument.
- The function reads the values of the vector it got, counts the days below zero and **returns** an `int` result, like the functions in lesson 5.3.
- **`main` prints**, and the function only counts, as in lesson 5.5.
- The loop appears in the code once, and works for both stations.

## 3. What `const std::vector<int>&` means

| Part | Meaning |
|---|---|
| `std::vector<int>` | The type: a vector of `int`s. |
| `&` | The parameter is a **reference**: it refers to an existing vector from the place of the call, rather than being a separate copy of it. |
| `const` | Through this parameter, the function can only **read** the vector; it can't change it. |
| `temperatures` | The name of the parameter, which the function uses in its body. |

A simple model: **the function gets the ability to read an existing vector, without creating a copy of it.** The word "reference" means here that, during the call, `temperatures` is another name for the same vector that `main` passed.

**Compare with lesson 5.2.** There, `void count_down(int remaining)` got its own copy of a number, and changing `remaining` didn't change the variable in `main`. A copy of one `int` costs nothing, so single numbers are still passed by value. A vector can have very many elements, and a function that only reads it doesn't need a copy. That's why a vector for reading is passed by `const&`. Passing a vector by value is also correct C++. We use the `const&` pattern when the function should **only read** the collection.

**Don't mix up two notations.** `const std::vector<int>& temperatures` in the function's header is a reference to the **whole vector**. `for (const int temperature : temperatures)` in the body is the range-based loop from lesson 6.1: in each pass it copies one `int`. Copying a single number isn't copying the whole collection.

**`const` is about access through the parameter.** A function with a `const&` parameter can't change the vector **through that parameter**. That doesn't mean the vector becomes unchangeable for ever: if the vector in `main` has no `const`, `main` can still change it:

<!-- example: cold_days_later -->
```cpp
#include <iostream>
#include <vector>

int count_cold_days(const std::vector<int>& temperatures) {
    int cold_days{0};

    for (const int temperature : temperatures) {
        if (temperature < 0) {
            ++cold_days;
        }
    }

    return cold_days;
}

int main() {
    std::vector<int> readings{};
    std::cout << "Cold days: " << count_cold_days(readings) << "\n";

    readings.push_back(-1);
    readings.push_back(4);
    std::cout << "Cold days: " << count_cold_days(readings) << "\n";
}
```

**Predict** both lines, including the first call with an empty vector. Then run the program.

<details>
<summary>Standard output</summary>

<!-- output: cold_days_later -->
```text
Cold days: 0
Cold days: 1
```

</details>

- The first call gets an **empty** vector. The function has no special condition for that, and still returns 0: the counter starts at 0, the range-based loop makes no passes, and `return` returns 0.
- `main` adds two elements. The second call reads the same, now changed, vector and returns 1.

## 4. The flow of a call

For `count_cold_days(north_temperatures)` from section 2:

| Step | What happens |
|---|---|
| 1 | `main` has the vector `north_temperatures` with four values: 3, −2, 0, −5. |
| 2 | `main` calls `count_cold_days(north_temperatures)`. |
| 3 | The parameter `temperatures` refers to `north_temperatures`. The vector isn't copied. |
| 4 | The loop reads 3, −2, 0 and −5 in turn. |
| 5 | The counter grows twice: for −2 and for −5. 0 isn't below zero. |
| 6 | The function returns 2. |
| 7 | `main` prints the result it got. |

**Predict:** what changes in this table for `count_cold_days(south_temperatures)`?

<details>
<summary>Answer</summary>

The parameter `temperatures` now refers to `south_temperatures`. The loop reads 7, 4 and 2, only three values, and the counter never grows. The function returns 0. The function's code is the same; only the vector the parameter refers to has changed.

</details>

**Not every calculation has a natural result for an empty vector.** The number of days below zero in an empty set is simply 0, and so is the sum. But the average and the largest value of an empty set don't exist (lessons 6.1 and 6.2), so a function computing them needs a separate design decision. In this lesson we choose calculations for which an empty vector has an unambiguous result.

## 5. `const&` doesn't let you change the vector

Someone added a line to the function that adds a reading:

<!-- broken: push_through_const_ref at=5:18 errors=1 error=^no matching member function for call to 'push_back'$ -->
```cpp
#include <iostream>
#include <vector>

int count_cold_days(const std::vector<int>& temperatures) {
    temperatures.push_back(10);

    int cold_days{0};

    for (const int temperature : temperatures) {
        if (temperature < 0) {
            ++cold_days;
        }
    }

    return cold_days;
}

int main() {
    const std::vector<int> north_temperatures{3, -2, 0, -5};

    std::cout << "North cold days: " << count_cold_days(north_temperatures) << "\n";
}
```

**Predict** whether the program builds.

<details>
<summary>What the compiler reports, and why</summary>

The program won't build. On line 5, the compiler reports `no matching member function for call to 'push_back'`, the same message as in lesson 6.2. In the `note:` lines it adds that `temperatures` has the type `const std::vector<int>`. It's the `const` in the parameter's type that limits this: through `temperatures` the vector can only be read.

**The fix:** remove the line with `push_back`. The task of this function is to read and count, not to change the data. You get the program from section 2.

</details>

## 6. A vector and an extra number

A function can have several parameters of different kinds. For example, counting the days below a chosen threshold could have this header:

<!-- fragment -->
```cpp
int count_below(const std::vector<int>& values, int threshold)
```

The vector for reading goes by `const&`, and the threshold, a small number, by value, as in lesson 5.2. A call gives both arguments in the order of the parameters: `count_below(north_temperatures, 0)`. We don't pass an `int` by reference: a copy of it costs nothing.

## 7. Mission: two weeks of reading

The program compares the reading in two weeks. Each week is a separate vector with the number of pages read on successive days. A week can have from 0 to 6 recorded days, and every value is in the range 0–30. The data is written in the code:

<!-- fragment -->
```cpp
const std::vector<int> week_a{12, 0, 8, 15, 9};
const std::vector<int> week_b{5, 18, 11, 16};
```

**Requirements:**

- Both vectors are defined in `main` as `const std::vector<int>`. The program doesn't read anything from the input.
- For each week, the program prints the total number of pages and the number of days on which **at least** 10 pages were read. Exactly 10 pages meets the goal. A day with 0 pages is an ordinary day of data.
- Then it compares the **total numbers of pages** and prints in which week more was read, or a tie. The number of goal days doesn't decide the result.
- The program has at least two of your own calculating functions:
  - a function that returns the sum of the values of the vector it gets, as an `int`;
  - a function that returns the number of elements reaching a threshold, as an `int`, with the threshold passed as an extra `int` parameter.
- Both functions get the vector through `const std::vector<int>&`, are defined before `main` and print nothing. You choose the names of the functions and parameters yourself.
- The functions compute the sums and the counters, not `main`. `main` prepares the data, calls the functions, compares the results and prints the report.
- Both vectors may be empty: the program works correctly then too.

The standard output has exactly these lines, in this order: `Week A pages: N`, `Week A goal days: N`, `Week B pages: N`, `Week B goal days: N`, and at the end one of three: `More pages: Week A`, `More pages: Week B` or `More pages: Tie`.

In `cpp-workspace`, create a folder `reading_weeks`, copy `CMakeLists.txt` from the original `lesson_05_first_program` into it, create an empty `main.cpp` and write the program on your own.

For the data above, the standard output must be:

<!-- output: reading_weeks -->
```text
Week A pages: 44
Week A goal days: 2
Week B pages: 50
Week B goal days: 3
More pages: Week B
```

The values are small: a week has at most 6 days of at most 30 pages, so the sums and counters fit safely in an `int`.

**This isn't the stations program with different messages.** There, there was one ready-made function. You have to decide on your own:

1. what task each of the two functions has, and what to call them;
2. what parameters the functions have, and in what order;
3. what values the sum and the counter start from;
4. how to make a value equal to the threshold count;
5. how to call both functions for both weeks;
6. how `main` chooses the winner and recognises a tie;
7. what the program prints for empty weeks.

**First check each function on its own**, as in lesson 5.5, before you put the whole report together:

1. Prepare a few small `const` vectors in `main`: for the summing function an empty one, a one-element one and one with several elements; for the threshold function an empty one, one with values below the threshold, one with a value of exactly 10, and one with values above.
2. For each, write down the expected result.
3. Call the function and temporarily print the result.
4. Compare with the expected result.
5. Remove the test printouts from the final program.

**Then check the whole program.** Run it for the data from the requirements, and then change the values in the braces to two or three cases from the full list of check cases, for example a tie of the sums and two empty weeks. The other cases in the list are checked automatically, so you don't need to type them all.

### Success criteria

- The program builds as C++20 and, for the data from the requirements, prints exactly the five lines shown above.
- Both functions take the vector through `const std::vector<int>&`, return an `int` and print nothing. The threshold is an `int` parameter.
- Each function is called for both weeks. The calculations aren't repeated in `main`.
- The result of the comparison depends on the sum of pages, also when the numbers of goal days differ.
- The program works for empty weeks and for a value equal to the threshold.
- The test printouts of the functions were made before the report was put together, and were removed from the final program.
- You can explain why the vector goes by `const&` and the threshold by value.

When the result matches, you can save the project in Git, as in lesson 1.5.

<details>
<summary>Hint 1</summary>

Which calculations do you do both for week A and for week B? Can each of them become one function?

</details>

<details>
<summary>Hint 2</summary>

A function doesn't need to know whether it got the data of week A or week B. It only needs a vector, and sometimes an extra value that sets the threshold.

</details>

<details>
<summary>Hint 3</summary>

Design separately a function that sums the pages and a function that counts the days meeting the goal. Call both for both weeks, and leave the comparison of the totals to `main()`.

</details>

<details>
<summary>The full list of check cases: open it after preparing your own tests</summary>

| | Week A | Week B | Pages A, goal days A | Pages B, goal days B | Last line | What it checks |
|---|---|---|---|---|---|---|
| A | `{12, 0, 8, 15, 9}` | `{5, 18, 11, 16}` | 44, 2 | 50, 3 | `More pages: Week B` | the data from the requirements |
| B | `{20, 10}` | `{5, 0}` | 30, 2 | 5, 0 | `More pages: Week A` | A wins |
| C | `{20, 0}` | `{10, 10}` | 20, 1 | 20, 2 | `More pages: Tie` | a tie of the sums with different goal days |
| D | `{}` | `{}` | 0, 0 | 0, 0 | `More pages: Tie` | both weeks empty |
| E | `{}` | `{10}` | 0, 0 | 10, 1 | `More pages: Week B` | one week empty |
| F | `{9}` | `{10}` | 9, 0 | 10, 1 | `More pages: Week B` | exactly at the threshold |
| G | `{9, 9}` | `{8}` | 18, 0 | 8, 0 | `More pages: Week A` | every value below the threshold |
| H | `{10, 10, 10}` | `{30}` | 30, 3 | 30, 1 | `More pages: Tie` | a tie of the sums with a different spread |
| I | `{12, 0, 8, 15, 9}` | `{12, 0, 8, 15, 9}` | 44, 2 | 44, 2 | `More pages: Tie` | two identical weeks (section 8) |

**Automatic tests and your own runs.** Every case in the table is checked automatically by a check program. It's the same report and the same functions as the reference solution, but it reads both weeks from the input: the number of days and the pages of week A, then of week B. The check program and its results are in [Example solutions](#example-solutions), because they contain the solution. By hand, it's enough to check a few cases, as described above.

</details>

An example solution is in [Example solutions](#example-solutions).

## 8. Find the bug: the wrong week

Do this task **after the mission**: the program below contains both of the mission's functions. The functions work correctly, and the program builds without errors. It reads both weeks from the input, like the check program.

<details>
<summary>The program to check: open it after writing your own program</summary>

<!-- example: weeks_argument_bug -->
```cpp
#include <iostream>
#include <vector>

int total_pages(const std::vector<int>& pages) {
    int total{0};

    for (const int day_pages : pages) {
        total += day_pages;
    }

    return total;
}

int count_goal_days(const std::vector<int>& pages, int goal) {
    int goal_days{0};

    for (const int day_pages : pages) {
        if (day_pages >= goal) {
            ++goal_days;
        }
    }

    return goal_days;
}

int main() {
    std::vector<int> week_a{};
    std::vector<int> week_b{};
    int day_count{0};

    std::cin >> day_count;

    for (int day{1}; day <= day_count; ++day) {
        int day_pages{0};
        std::cin >> day_pages;
        week_a.push_back(day_pages);
    }

    std::cin >> day_count;

    for (int day{1}; day <= day_count; ++day) {
        int day_pages{0};
        std::cin >> day_pages;
        week_b.push_back(day_pages);
    }

    if (std::cin.fail()) {
        std::cout << "Input could not be read\n";
    } else {
        const int daily_goal{10};
        const int pages_a{total_pages(week_a)};
        const int pages_b{total_pages(week_a)};

        std::cout << "Week A pages: " << pages_a << "\n";
        std::cout << "Week A goal days: " << count_goal_days(week_a, daily_goal) << "\n";
        std::cout << "Week B pages: " << pages_b << "\n";
        std::cout << "Week B goal days: " << count_goal_days(week_b, daily_goal) << "\n";

        if (pages_a > pages_b) {
            std::cout << "More pages: Week A\n";
        } else if (pages_b > pages_a) {
            std::cout << "More pages: Week B\n";
        } else {
            std::cout << "More pages: Tie\n";
        }
    }
}
```

The program prints no questions: type the numbers in order, each on its own line.

1. Read the mission's requirement and **predict** the report for two identical weeks `{12, 0, 8, 15, 9}`, the data `5`, `12`, `0`, `8`, `15`, `9`, `5`, `12`, `0`, `8`, `15`, `9`.
2. Run the program with that data. Is the report correct?
3. Run it with the data of example A: `5`, `12`, `0`, `8`, `15`, `9`, `4`, `5`, `18`, `11`, `16`.
4. Compare both reports with the requirement. Why doesn't the first test reveal the bug?
5. Find the call with the wrong argument.
6. Fix it.
7. Compare the results for both data sets again.

</details>

The program's output before the fix, and the fixed program, are in [Example solutions](#example-solutions).

## 9. When something goes differently

| What you see | What it means | What to do |
|---|---|---|
| `no matching member function for call to 'push_back'` in a function | The function tries to change the vector through a `const&` parameter (section 5). | A reading function doesn't change the vector. Remove the change, or move it to `main`. |
| `no matching function for call to ...` at a call | The number or order of the arguments doesn't match the parameters. | Compare the call with the function's header: first the vector, then the threshold, if that's how the parameters are written. |
| A day with exactly 10 pages doesn't count | The condition uses `>` instead of `>=`. | Check case F: for `{10}` the result is 1. |
| With equal sums, the program names a week | The winner is chosen by the number of goal days, or the tie branch is missing. | Check cases C and H: the result is `Tie`. |
| Both weeks have the same results, although the data differs | A function is called twice with the same vector (section 8). | Check the arguments of every call. |
| A sum or counter is too large on a later call | The accumulator isn't a local variable of the function. | The sum and the counter should be declared in the function's body, before the loop. |

## 10. Explain

Answer in your own words, preferably in writing. Only then compare with the example answers.

1. Why can a function need a whole vector as a parameter?
2. What does `const std::vector<int>&` mean?
3. How does it differ from an `int` parameter passed by value?
4. Does a function with such a parameter create a copy of the whole vector?
5. Can the same function be called for two different vectors? Does it need to know their names in `main`?
6. Can you call `push_back()` through a `const&` parameter?
7. Does a vector in `main` need `const` to be passed to such a function?
8. Can a function with a vector parameter return an ordinary `int` result?
9. What do the mission's functions return for an empty vector, and why?
10. Why do we pass the threshold as an ordinary `int`?
11. Why can a test with two identical vectors hide a mixed-up argument?

<details>
<summary>Example answers</summary>

1. Because its task concerns every value of the collection, for example computing the sum, and the number of values differs from vector to vector. A separate parameter for each value wouldn't be possible.
2. The parameter is a reference to a vector of `int`s: it refers to the vector from the place of the call, without copying it, and `const` means that through this parameter the vector can only be read.
3. An `int` parameter gets its own copy of the argument's value. A `const std::vector<int>&` parameter gets no copy; it refers to the existing vector and lets the function read it.
4. No. The function reads the vector the caller passed.
5. Yes. Each time, the parameter refers to the vector given in the call. The function knows only the name of its own parameter.
6. No. The `const` in the parameter's type forbids changes through this parameter, so the compiler reports an error.
7. No. A vector without `const` can be passed too. The function still can't change it through its parameter, but `main` can still change it.
8. Yes. The result type doesn't depend on the parameter types: a function can take a vector and return an `int`.
9. 0. The sum and the counter start at 0, the range-based loop makes no passes for an empty vector, so the functions return the initial value. For a sum and a number of days that's an unambiguous, sensible result.
10. Because it's one small number whose copy costs nothing, and the function doesn't change it. A reference gives no benefit here.
11. Because with identical vectors, a call with the wrong vector gives the same result as with the right one. Only different data reveals the bug.

</details>

## Summary

- A function that has to analyse a whole vector gets it as a parameter: `int count_cold_days(const std::vector<int>& temperatures)`.
- `&` means the parameter is a **reference**: it refers to the vector from the place of the call, without copying it. `const` means that through this parameter the vector can only be read.
- You call the same function for different vectors. The function doesn't know their names in `main`.
- Single numbers, like a threshold, are still passed by value.
- `const&` limits only the access through the parameter. A vector without `const` in `main` can still be changed in `main`.
- The function returns a result, and `main` prints and compares it.
- For an empty vector, a sum and a counter have the natural result 0. An average and a maximum need a separate decision.
- You check functions on their own, empty vectors included, and different data in the tests reveals mixed-up arguments.

## What's next

The functions in this lesson returned single numbers. In the next lesson a function will return a new vector, for example one built from chosen elements of another vector: [Lesson 6.5: A function creates and returns a new vector](lesson_05_a_function_returns_a_vector.en.md).

---

## Example solutions

Look here **after your own attempt**. Your names may differ, as long as the standard output is as required.

<details>
<summary>Section 7: the mission, two weeks of reading</summary>

<!-- example: reading_weeks -->
```cpp
#include <iostream>
#include <vector>

int total_pages(const std::vector<int>& pages) {
    int total{0};

    for (const int day_pages : pages) {
        total += day_pages;
    }

    return total;
}

int count_goal_days(const std::vector<int>& pages, int goal) {
    int goal_days{0};

    for (const int day_pages : pages) {
        if (day_pages >= goal) {
            ++goal_days;
        }
    }

    return goal_days;
}

int main() {
    const std::vector<int> week_a{12, 0, 8, 15, 9};
    const std::vector<int> week_b{5, 18, 11, 16};

    const int daily_goal{10};
    const int pages_a{total_pages(week_a)};
    const int pages_b{total_pages(week_b)};

    std::cout << "Week A pages: " << pages_a << "\n";
    std::cout << "Week A goal days: " << count_goal_days(week_a, daily_goal) << "\n";
    std::cout << "Week B pages: " << pages_b << "\n";
    std::cout << "Week B goal days: " << count_goal_days(week_b, daily_goal) << "\n";

    if (pages_a > pages_b) {
        std::cout << "More pages: Week A\n";
    } else if (pages_b > pages_a) {
        std::cout << "More pages: Week B\n";
    } else {
        std::cout << "More pages: Tie\n";
    }
}
```

1. **Both functions take `const&`**, because they only read a week: they don't need a copy of it and mustn't change it.
2. **The threshold `goal` goes by value**: it's one `int`, and the function doesn't change it.
3. **The functions work for both weeks**, because they don't depend on the names in `main`. The parameter `pages` refers each time to the vector of the call: once to `week_a`, once to `week_b`.
4. **One implementation is enough:** the summing loop and the counting loop each appear in the code once. Changing a rule, for example the threshold condition `>=`, needs a change in one place.
5. **An empty vector:** `total` and `goal_days` start at 0, and the loop makes no passes, so both functions return 0. For a sum and a number of days that's the right result.
6. **Choosing the week belongs to `main`**, because it's a decision about the report that needs the results of both weeks. The calculating functions know about only one vector at a time.
7. `main` keeps the sums in `pages_a` and `pages_b`, because it needs them twice: to print and to compare. It prints the numbers of goal days straight away.

This is one possible split. It's also correct, for example, to keep all four results in variables, or to use a different order of the threshold function's parameters, as long as its calls match.

**The check program** checks every case in the list of check cases. The functions are the same as above, and the part of `main` from `const int daily_goal{10};` on is the same, apart from the indentation. Only the source of the data differs: both weeks are read from the input with `push_back`, as in lesson 6.2, so the vectors have no `const`. The program prints no questions, so its standard output is the same as the mission's result.

<!-- example: reading_weeks_check -->
```cpp
#include <iostream>
#include <vector>

int total_pages(const std::vector<int>& pages) {
    int total{0};

    for (const int day_pages : pages) {
        total += day_pages;
    }

    return total;
}

int count_goal_days(const std::vector<int>& pages, int goal) {
    int goal_days{0};

    for (const int day_pages : pages) {
        if (day_pages >= goal) {
            ++goal_days;
        }
    }

    return goal_days;
}

int main() {
    std::vector<int> week_a{};
    std::vector<int> week_b{};
    int day_count{0};

    std::cin >> day_count;

    for (int day{1}; day <= day_count; ++day) {
        int day_pages{0};
        std::cin >> day_pages;
        week_a.push_back(day_pages);
    }

    std::cin >> day_count;

    for (int day{1}; day <= day_count; ++day) {
        int day_pages{0};
        std::cin >> day_pages;
        week_b.push_back(day_pages);
    }

    if (std::cin.fail()) {
        std::cout << "Input could not be read\n";
    } else {
        const int daily_goal{10};
        const int pages_a{total_pages(week_a)};
        const int pages_b{total_pages(week_b)};

        std::cout << "Week A pages: " << pages_a << "\n";
        std::cout << "Week A goal days: " << count_goal_days(week_a, daily_goal) << "\n";
        std::cout << "Week B pages: " << pages_b << "\n";
        std::cout << "Week B goal days: " << count_goal_days(week_b, daily_goal) << "\n";

        if (pages_a > pages_b) {
            std::cout << "More pages: Week A\n";
        } else if (pages_b > pages_a) {
            std::cout << "More pages: Week B\n";
        } else {
            std::cout << "More pages: Tie\n";
        }
    }
}
```

The input data is the number of days and the pages of week A, then the number of days and the pages of week B. The cases come in the order of the list of check cases, from A to I.

<!-- input: reading_weeks_check -->
```text
5
12
0
8
15
9
4
5
18
11
16
```

<!-- output: reading_weeks_check -->
```text
Week A pages: 44
Week A goal days: 2
Week B pages: 50
Week B goal days: 3
More pages: Week B
```

<!-- input: reading_weeks_check -->
```text
2
20
10
2
5
0
```

<!-- output: reading_weeks_check -->
```text
Week A pages: 30
Week A goal days: 2
Week B pages: 5
Week B goal days: 0
More pages: Week A
```

<!-- input: reading_weeks_check -->
```text
2
20
0
2
10
10
```

<!-- output: reading_weeks_check -->
```text
Week A pages: 20
Week A goal days: 1
Week B pages: 20
Week B goal days: 2
More pages: Tie
```

<!-- input: reading_weeks_check -->
```text
0
0
```

<!-- output: reading_weeks_check -->
```text
Week A pages: 0
Week A goal days: 0
Week B pages: 0
Week B goal days: 0
More pages: Tie
```

<!-- input: reading_weeks_check -->
```text
0
1
10
```

<!-- output: reading_weeks_check -->
```text
Week A pages: 0
Week A goal days: 0
Week B pages: 10
Week B goal days: 1
More pages: Week B
```

<!-- input: reading_weeks_check -->
```text
1
9
1
10
```

<!-- output: reading_weeks_check -->
```text
Week A pages: 9
Week A goal days: 0
Week B pages: 10
Week B goal days: 1
More pages: Week B
```

<!-- input: reading_weeks_check -->
```text
2
9
9
1
8
```

<!-- output: reading_weeks_check -->
```text
Week A pages: 18
Week A goal days: 0
Week B pages: 8
Week B goal days: 0
More pages: Week A
```

<!-- input: reading_weeks_check -->
```text
3
10
10
10
1
30
```

<!-- output: reading_weeks_check -->
```text
Week A pages: 30
Week A goal days: 3
Week B pages: 30
Week B goal days: 1
More pages: Tie
```

<!-- input: reading_weeks_check -->
```text
5
12
0
8
15
9
5
12
0
8
15
9
```

<!-- output: reading_weeks_check -->
```text
Week A pages: 44
Week A goal days: 2
Week B pages: 44
Week B goal days: 2
More pages: Tie
```

</details>

<details>
<summary>Section 8: the output before the fix, and the fixed program</summary>

Before the fix, for two identical weeks:

<!-- input: weeks_argument_bug -->
```text
5
12
0
8
15
9
5
12
0
8
15
9
```

<!-- output: weeks_argument_bug -->
```text
Week A pages: 44
Week A goal days: 2
Week B pages: 44
Week B goal days: 2
More pages: Tie
```

For the data of example A:

<!-- input: weeks_argument_bug -->
```text
5
12
0
8
15
9
4
5
18
11
16
```

<!-- output: weeks_argument_bug -->
```text
Week A pages: 44
Week A goal days: 2
Week B pages: 44
Week B goal days: 3
More pages: Tie
```

- For identical weeks the report is correct: week B's sum is computed from week A, but both weeks have the same data, so the result comes out the same.
- For example A, week B has 50 pages, but the program prints 44 and declares a tie. The number of goal days for B, 3, is correct, because that call gets the right vector.
- **The cause:** `const int pages_b{total_pages(week_a)};`. The argument is `week_a`, but it should be `week_b`. The compiler won't detect this: both vectors have the same type, so the call is valid C++. It's a logic error.
- **The fix:** `const int pages_b{total_pages(week_b)};`.

The fixed program is the check program from section 7: it differs from the buggy program only in that argument. For both data sets it gives the results from the list of check cases: case I (identical weeks) and case A (`More pages: Week B`).

</details>

**Previous lesson:** [Lesson 6.3: Element positions and neighbouring values in a `std::vector`](lesson_03_positions_and_neighbours.en.md) · **Next lesson:** [Lesson 6.5: A function creates and returns a new vector](lesson_05_a_function_returns_a_vector.en.md) · [Course overview](../../README.en.md)

# Lesson 6.1: Your first `std::vector` and the range-based `for` loop

[Polski](lesson_01_the_first_vector.md) · **English** · [Course overview](../../README.en.md)

> **Module 6, lesson 1** · about 60–75 minutes
> **You need:** your `cpp-workspace` folder and the original `lesson_05_first_program` project, as before. You won't need the debugger in this lesson.
> **Pilot version.** The programs in this lesson are checked automatically on Windows, Ubuntu and macOS. None of them asks for data: all the values are written in the code.

## Before you start

This lesson assumes that after Modules 4 and 5 you:

- collect a result in an accumulator and count events with a counter (lesson 4.2);
- write a `for` loop with a counter and trace it in a trace table (lesson 4.3);
- know that initialisation with `{}` doesn't allow a narrowing conversion (lesson 2.5);
- call a member function with a dot, like `std::cin.fail()` (lesson 4.5).

You won't need your own functions from Module 5 in this lesson: every program fits in `main`.

## The situation

The measurement station from lesson 4.7 read one temperature after another and updated the sum and the counters straight away. After the loop it knew the sum and the number of measurements, but **it no longer knew the measurements themselves**. Each read overwrote the previous value.

What if, after computing the summary, you want to go back to the earlier values? For example, to point out the temperatures above the average, or to check how many times the highest one occurred. The sum and the count alone can't tell you that: a sum of 15 from three measurements could be 3, 7 and 5, but also 5, 5 and 5.

In this lesson you'll meet **`std::vector`**: a variable that stores many values of the same type in a fixed order, and a loop that goes through them one by one.

After this lesson you will:

- explain why a separate variable for each value stops being enough;
- define a `std::vector<int>` with initial values and point out the type of its elements;
- get the number of elements with `size()`;
- write a range-based `for` loop and explain where the loop variable gets its value from;
- compute a sum and count events over the elements of a vector;
- go through the same vector several times, when the second pass needs the result of the first;
- predict how many times a loop runs for one, several and zero elements;
- design simple processing of a set of data on your own.

## 1. Prepare the project

In `cpp-workspace`, create a folder `lesson_6_1` and copy `main.cpp` and `CMakeLists.txt` from the original `lesson_05_first_program` into it. You type the programs from sections 3–9 into `main.cpp` in this folder.

## 2. A separate variable for each value

If the station had to remember three measurements, it could store each one in a separate variable:

<!-- fragment -->
```cpp
const int first{3};
const int second{7};
const int third{5};
```

That's correct code. But every new measurement means a new name and a new term in the sum `first + second + third`. With 24 measurements there would be 24 names. A loop won't help here: there's no way for successive passes to reach `first`, then `second`, then `third`. You need **one** variable for **all** the measurements.

## 3. Your first vector

<!-- example: measurements_stored -->
```cpp
#include <iostream>
#include <vector>

int main() {
    const std::vector<int> measurements{3, 7, 5, 9};

    std::cout << "Measurements stored: " << measurements.size() << "\n";
}
```

<!-- output: measurements_stored -->
```text
Measurements stored: 4
```

| In the code | Meaning |
|---|---|
| `#include <vector>` | Makes `std::vector` available, just as `<iostream>` makes `std::cout` available. |
| `std::vector<int>` | The variable's type: a **vector**, an ordered collection of values. The angle brackets `< >` hold the type of the elements: every element of this vector is an `int`. |
| `measurements` | The variable's name. One name for the whole collection. |
| `{3, 7, 5, 9}` | The initial values, the **elements** of the vector. The vector keeps their order: the first is 3, the last is 9. |
| `const` | This program doesn't change the vector, so, as with other variables, we mark it `const` (lesson 2.2). |
| `measurements.size()` | The number of elements in the vector, here 4. `size()` is a member function of the vector, called with a dot, like `std::cin.fail()` in lesson 4.5. |

All the elements of one vector have the same type, in this lesson `int`. Write `#include <vector>` in every program with a vector: on some systems the program builds without it, but on others it doesn't.

**Print the number of elements directly**, as here. `size()` gives it in a separate type meant for sizes, not as an `int`. If you store that result in an `int` variable with `{}`, the compiler rejects it as a narrowing conversion, as in lesson 2.5. You'll meet the right type in one of the next lessons.

## 4. The range-based `for` loop

This program prints all the measurements, each on its own line:

<!-- example: measurements_listed -->
```cpp
#include <iostream>
#include <vector>

int main() {
    const std::vector<int> measurements{3, 7, 5, 9};

    for (const int measurement : measurements) {
        std::cout << measurement << "\n";
    }
}
```

**Predict** what the program prints and in what order. Then run it.

<details>
<summary>Standard output</summary>

<!-- output: measurements_listed -->
```text
3
7
5
9
```

</details>

This is a **range-based `for` loop**. Read its header as "for each `measurement` in `measurements`".

| Part | Meaning |
|---|---|
| `for` | The same word as in lesson 4.3: repetition. |
| `const int measurement` | **The loop variable.** In each pass it gets the value of the next element. Its type is the type of the vector's elements: `int`. `const`, because the body only reads it. |
| `:` | The colon separates the loop variable from the collection the loop goes through. |
| `measurements` | The vector whose elements you go through. |
| the body in `{ }` | Runs once for each element. |

In the loop from lesson 4.3 you had to write the counter's initial value, the condition and the update. Here there's none of those parts. The loop takes the elements in order by itself and ends after the last one, so there's no counter to increase and no condition to get wrong by one.

Choose names that read well: the vector in the plural (`measurements`), the loop variable in the singular (`measurement`).

## 5. The loop step by step

| Pass | Value of `measurement` | On the screen |
|---|---|---|
| 1 | 3, the first element | `3` |
| 2 | 7 | `7` |
| 3 | 5 | `5` |
| 4 | 9, the last element | `9` |
| — | there's no next element: the loop ends | |

Answer before you open the answers:

1. How many times does the loop body run?
2. Which value comes first?
3. Which comes last?
4. Is the order the same as in the braces?
5. Do you need `++` in the body to move on to the next element?
6. What changes if you add a fifth element to the braces? And how many times does the body run for the vector `{6}`?

<details>
<summary>Answers</summary>

1. Four times: once for each of the four elements.
2. 3, the first element in the braces.
3. 9, the last element.
4. Yes. The range-based loop goes through the elements in the order they're stored in, and the vector stores them in the order of the initialisation.
5. No. The loop moves on to the next element by itself. There's no counter in this loop to increase.
6. The body runs five times, and the new element is printed last. The loop itself doesn't need to change: you'll check that in the next section. For the vector `{6}` the body runs once.

</details>

## 6. More data, the same loop

Add the measurement 4 at the end of the braces and add a line with the number of elements:

<!-- example: measurements_five -->
```cpp
#include <iostream>
#include <vector>

int main() {
    const std::vector<int> measurements{3, 7, 5, 9, 4};

    std::cout << "Measurements stored: " << measurements.size() << "\n";

    for (const int measurement : measurements) {
        std::cout << measurement << "\n";
    }
}
```

**Predict** every line of standard output and run the program.

<details>
<summary>Standard output</summary>

<!-- output: measurements_five -->
```text
Measurements stored: 5
3
7
5
9
4
```

</details>

Only the line with the data changed. The loop is the same and goes through as many elements as the vector has. With the separate variables from section 2, a new measurement would mean a new name and a new line with `std::cout`.

## 7. A sum and a counter over the data in a vector

The vector stores the data, and you process it as before. A hiking route is made of stages, each with a length in kilometres. The program computes the length of the whole route and the number of long stages, those of at least 12 km:

<!-- example: route_summary -->
```cpp
#include <iostream>
#include <vector>

int main() {
    const std::vector<int> stages{12, 8, 15, 10};

    int total{0};
    int long_stages{0};

    for (const int stage : stages) {
        total += stage;

        if (stage >= 12) {
            ++long_stages;
        }
    }

    std::cout << "Total distance: " << total << " km\n";
    std::cout << "Long stages: " << long_stages << "\n";
}
```

**Predict** both lines of output and run the program.

<details>
<summary>Standard output</summary>

<!-- output: route_summary -->
```text
Total distance: 45 km
Long stages: 2
```

</details>

`total` is an accumulator and `long_stages` an event counter, both declared **before** the loop, as in lesson 4.2. Only the source of the values is new: the vector's elements instead of a counter or the input.

## 8. A second pass over the same data

Now the program should also print, after each stage, how many kilometres are left to the end of the route. The first such line needs the length of the **whole** route, and that's known only after looking at every stage. So the program goes through the vector a second time:

<!-- example: route_plan -->
```cpp
#include <iostream>
#include <vector>

int main() {
    const std::vector<int> stages{12, 8, 15, 10};

    int total{0};
    int long_stages{0};

    for (const int stage : stages) {
        total += stage;

        if (stage >= 12) {
            ++long_stages;
        }
    }

    std::cout << "Total distance: " << total << " km\n";
    std::cout << "Long stages: " << long_stages << "\n";

    int remaining{total};

    for (const int stage : stages) {
        remaining -= stage;
        std::cout << "Left after stage: " << remaining << " km\n";
    }
}
```

**Predict** the four `Left after stage` lines and run the program.

<details>
<summary>Standard output</summary>

<!-- output: route_plan -->
```text
Total distance: 45 km
Long stages: 2
Left after stage: 33 km
Left after stage: 25 km
Left after stage: 10 km
Left after stage: 0 km
```

</details>

- **The first pass** computes the length of the route. **The second** starts from it and subtracts the stages one by one. The last line is 0 km, which confirms that both passes covered the same stages.
- **The data doesn't disappear after the first loop.** The range-based loop only reads the elements, so afterwards the vector has the same stages in the same order. In lesson 4.7, each value was available in one pass only.
- The second pass is needed because **it uses the result of the first**. When one pass is enough, as for the average in lesson 4.7, storing all the values isn't necessary.

## 9. An empty vector

A vector can have no elements at all. Then the braces are empty:

<!-- example: measurements_empty -->
```cpp
#include <iostream>
#include <vector>

int main() {
    const std::vector<int> measurements{};

    std::cout << "Measurements stored: " << measurements.size() << "\n";

    for (const int measurement : measurements) {
        std::cout << measurement << "\n";
    }

    std::cout << "End of list\n";
}
```

**Predict** how many times the loop body runs and what the program prints.

<details>
<summary>Standard output and explanation</summary>

<!-- output: measurements_empty -->
```text
Measurements stored: 0
End of list
```

The body didn't run even once: there's no element, so the loop ends straight away. That's correct and safe behaviour, like a loop with zero passes in lesson 4.1.

</details>

Not every result makes sense for an empty collection. The length of a route with no stages is 0 km. But a route with no stages has no longest stage. You'll learn how to check whether a vector is empty in the next lesson.

## 10. Mission: rainy days

The program analyses the rainfall on successive days. Each day's rainfall is a small, non-negative whole number of millimetres. The values are written in the code:

<!-- fragment -->
```cpp
const std::vector<int> rainfall{0, 5, 2, 5, 1, 0};
```

**Requirements:**

- The program stores the rainfall in a `std::vector<int>` with initial values, as above. It doesn't read anything from the input.
- It prints three lines: the total rainfall (`Total rainfall: N`), the highest rainfall recorded on one day (`Highest daily rainfall: N`) and the number of days on which that highest rainfall occurred (`Days at highest rainfall: N`).
- We assume that the vector has at least one element and that all the values are non-negative. You don't handle an empty vector: a total of 0 would make sense, but there would be no highest rainfall, and a program that prints 0 then gives a value that isn't in the data.
- After changing only the values in the braces, the program gives correct results for the new data, with no other change to the code.
- You go through the elements with a range-based `for` loop. The constructs from this lesson and the previous modules are enough.

In `cpp-workspace`, create a folder `rainy_days`, copy `CMakeLists.txt` from the original `lesson_05_first_program` into it, create an empty `main.cpp` and write the program on your own.

For the data above, the standard output must be:

<!-- output: rainfall_report -->
```text
Total rainfall: 13
Highest daily rainfall: 5
Days at highest rainfall: 2
```

**This isn't the route program with different messages.** There, the program was ready. Here, nobody tells you how many passes you need or what each one computes. You have to decide on your own:

1. how to find the highest value while going through the days;
2. which variables hold the results and what values they start from;
3. at which point of the program you know the final highest rainfall;
4. whether one pass over the vector is enough, or whether you need another;
5. how to count all the days with the highest rainfall, also when there are several.

**Before you write the program**, prepare a table of test cases. Each case is different values in the braces. Include: the data from the requirements, one day, every day with the same rainfall, all zeros, the highest rainfall only on the first day, and the highest rainfall only on the last day. For each case, write down the three numbers the program should print.

**Then work in this order:**

1. Write the program and run it for the data from the requirements.
2. Compare the result with the expected standard output.
3. Change the values in the braces to each of the other cases in your table in turn. Predict the result before each run.
4. For each mismatch, check whether the mistake is in the program or in the table.

### Success criteria

- The program builds as C++20 and, for the data from the requirements, prints exactly the three lines shown above.
- For every case in the table it gives the correct total, highest rainfall and number of days with the highest rainfall, after changing only the values in the braces.
- All the days with the highest rainfall are counted, also when there are several or when every day has the same rainfall.
- The program doesn't read data from the input and uses nothing beyond this lesson and the previous modules.
- The table of cases was made before the program was run.
- You can explain at which point your program knows the final highest rainfall.

When the result matches, you can save the project in Git, as in lesson 1.5.

<details>
<summary>Hint 1</summary>

What information about the rainfall can you compute during the first look at all the days?

</details>

<details>
<summary>Hint 2</summary>

To count the days with the highest rainfall, you first need to know what the highest value was.

</details>

<details>
<summary>Hint 3</summary>

Once you've found the highest rainfall, you can look through the same stored values again and count the elements equal to the maximum.

</details>

<details>
<summary>The full list of check cases: open it after preparing your own table</summary>

| Case | Values in the braces | Total | Highest rainfall | Days at highest rainfall | What it checks |
|---|---|---|---|---|---|
| A | `0, 5, 2, 5, 1, 0` | 13 | 5 | 2 | the data from the requirements: the highest rainfall twice |
| B | `3, 3, 3` | 9 | 3 | 3 | every day with the same rainfall |
| C | `7` | 7 | 7 | 1 | one day |
| D | `0, 0, 0` | 0 | 0 | 3 | no rain: the highest rainfall is 0 |
| E | `8, 2, 1, 3` | 14 | 8 | 1 | the highest rainfall only on the first day |
| F | `1, 2, 3, 9` | 15 | 9 | 1 | the highest rainfall only on the last day |

For each case, the standard output has the same three lines as for A, with the numbers from the table. Case A is checked above, with the mission's requirements.

</details>

An example solution is in [Example solutions](#example-solutions).

## 11. Find the bug: too many days with the highest rainfall

Do this task **after the mission**. Someone else solved the same mission but wanted to go through the vector only once. Their program is below, in a collapsed part, so that it doesn't give away the mission's solution.

<details>
<summary>The program to check: open it after writing your own program</summary>

<!-- example: rainfall_bug -->
```cpp
#include <iostream>
#include <vector>

int main() {
    const std::vector<int> rainfall{0, 5, 2, 5, 1, 0};

    int total{0};
    int highest{0};
    int days_at_highest{0};

    for (const int amount : rainfall) {
        total += amount;

        if (amount > highest) {
            highest = amount;
        }

        if (amount == highest) {
            ++days_at_highest;
        }
    }

    std::cout << "Total rainfall: " << total << "\n";
    std::cout << "Highest daily rainfall: " << highest << "\n";
    std::cout << "Days at highest rainfall: " << days_at_highest << "\n";
}
```

1. Write down what standard output **should** appear for this data (case A).
2. **Predict** what **this** program prints. Use a trace table with the columns: `amount`, `highest` after the first `if`, `days_at_highest` after the second `if`.
3. Run the program.
4. Compare the result with the requirement.
5. Find the day that was counted when it shouldn't have been, and explain why the program counted it.
6. Fix the program.
7. Check the fixed program for case A, with the repeated highest rainfall. Then cases C and E. Why did the buggy program give the correct result for them?

</details>

The output before the fix, and the fixed versions, are in [Example solutions](#example-solutions).

## 12. When something goes differently

| What you see | What it means | What to do |
|---|---|---|
| A compile error at `std::vector` | `#include <vector>` is missing, or the name has a typo. | Add `#include <vector>` at the top of the file. |
| Several errors in the loop header, for example `expected ';' in 'for' statement specifier` | There's a semicolon instead of the colon: `for (const int x ; values)`. | A `:` goes between the loop variable and the vector. |
| `cannot assign to variable ... with const-qualified type 'const int'` | The loop body tries to change the loop variable, which is `const`. | In this lesson the loop variable is for reading only. Store a result in a separate variable, declared before the loop. |
| `cannot be narrowed` at `size()` | The result of `size()` goes into an `int` variable with `{}`. | Print `size()` directly (section 3). |
| The sum or the counter shows only the last element | The accumulator or the counter is declared in the loop body and starts again in every pass. | Declare it before the loop, as in lesson 4.2. |
| Too many days with the highest rainfall | The days are counted before the program knows the final highest rainfall (section 11). | Trace the program in a table for cases A and F. |
| The program prints nothing and waits | That shouldn't happen: the programs in this lesson don't read any input. | Check whether a `std::cin` from another program was left in the code. |

## 13. Explain

Answer in your own words, preferably in writing. Only then compare with the example answers.

1. What is a `std::vector<int>`?
2. Why do we include `<vector>`?
3. What does the `int` inside `std::vector<int>` mean?
4. What are the values in the braces of a vector definition for?
5. Do the elements of a vector have a definite order?
6. How does a range-based loop differ from a `for` loop with a counter?
7. What does the colon in a range-based loop mean?
8. Where does the loop variable get its value from?
9. Do you have to move on to the next element by hand in a range-based loop?
10. What does `const int` do for the loop variable?
11. How many passes does a range-based loop make over an empty vector?
12. Can you go through the same vector several times?
13. Why is a vector useful when you later want to go back to earlier data?
14. What does `size()` give?
15. Why don't we store the result of `size()` in an `int` variable?
16. Why can counting the days with the highest rainfall in the mission need a second pass?

<details>
<summary>Example answers</summary>

1. A variable that stores an ordered collection of `int` values, the vector's elements.
2. Because that's where `std::vector` is. Without it the program may not build, even if it happens to build on one system.
3. The type of the elements: every element of this vector is an `int`.
4. They're the initial values: the elements the vector has from the moment it's created, in the given order. Empty braces `{}` give a vector with no elements.
5. Yes. The vector stores the elements in the order of the initialisation, and the range-based loop goes through them in that order.
6. In a loop with a counter you have to write the initial value, the condition and the update. A range-based loop has no counter: it takes each element of the collection in turn and ends after the last one.
7. It separates the loop variable from the collection the loop goes through. The header reads "for each `measurement` in `measurements`".
8. In each pass it gets the value of the next element of the vector, from the first to the last.
9. No. The loop moves on to the next element by itself, so there's no `++` and no condition to write.
10. The body can read the variable but can't change it. The compiler reports an error if the body tries. The loop variable is a separate value anyway: changing it wouldn't change the vector's element.
11. Zero. The body doesn't run even once, and the program goes on past the loop.
12. Yes. The range-based loop only reads the elements, so afterwards the vector has the same elements in the same order and can be gone through again.
13. Because it stores all the values. A program that only updates a sum and counters, as in lesson 4.7, can't go back to an earlier value.
14. The number of elements in the vector.
15. Because `size()` gives its result in a separate type meant for sizes, and initialisation with `{}` doesn't allow turning it into an `int` (a narrowing conversion, lesson 2.5). For now we print `size()` directly.
16. Because a day can be counted as a day with the highest rainfall only once the final highest rainfall is known. During the first pass, that value can still change. The second pass compares each day with the final value. It's not the only possible way, but it's the simplest to check.

</details>

## Summary

- **`std::vector<int>`** stores many `int` values in one variable, in a fixed order. It needs `#include <vector>`.
- You write the initial values in braces: `const std::vector<int> measurements{3, 7, 5, 9};`. Empty `{}` give a vector with no elements.
- `measurements.size()` gives the number of elements. For now, print it directly, without storing it in an `int`.
- **The range-based loop** `for (const int measurement : measurements)` runs its body once for each element, from the first to the last. There's no counter, condition or update to write.
- For an empty vector, a range-based loop makes no passes at all.
- The familiar accumulators, counters and conditions work on a vector's elements.
- After the loop ends, the data is still in the vector. A second pass makes sense when it needs the result of the first, for example a sum or the highest value.
- Not every result makes sense for an empty collection. A sum does; the highest value doesn't.

## What's next

In this lesson, all the elements were written in the code before the program started. In the next lesson, the vector will take new elements while the program runs, and the program will check whether it got any at all: [Lesson 6.2: Adding data to a vector: `push_back()` and `empty()`](lesson_02_adding_to_a_vector.en.md).

---

## Example solutions

Look here **after your own attempt**. Your names may differ, as long as the standard output is as required.

<details>
<summary>Section 10: the mission, rainy days</summary>

<!-- example: rainfall_report -->
```cpp
#include <iostream>
#include <vector>

int main() {
    const std::vector<int> rainfall{0, 5, 2, 5, 1, 0};

    int total{0};
    int highest{0};

    for (const int amount : rainfall) {
        total += amount;

        if (amount > highest) {
            highest = amount;
        }
    }

    int days_at_highest{0};

    for (const int amount : rainfall) {
        if (amount == highest) {
            ++days_at_highest;
        }
    }

    std::cout << "Total rainfall: " << total << "\n";
    std::cout << "Highest daily rainfall: " << highest << "\n";
    std::cout << "Days at highest rainfall: " << days_at_highest << "\n";
}
```

- **The vector stores every day**, so the rainfall is still available after the first loop. Without it, the program couldn't check any day a second time.
- **The first pass** computes the total and looks for the highest rainfall. `highest` remembers the highest value among the days seen so far. When the current day has more rain, that rainfall becomes the new value of `highest`.
- **The initial value 0** is safe only because of the mission's assumptions: all the rainfall values are non-negative, and there's at least one day. For the data `0, 0, 0`, the highest rainfall really is 0, because that rainfall is in the data. For an empty vector the program would also print 0, but no such day would be in the data. That's why an empty vector is outside the mission's scope.
- **The second pass** counts the days equal to the highest rainfall. After the first loop, `highest` already has its final value, so every day is compared with the right number.
- **A repeated highest rainfall** is the most important case: in data A it occurs twice, and in data B and D every day is equal. If a program always counted just one such day, cases C, E and F wouldn't reveal that mistake.
- **Changing the number of elements** changes only the number of passes of both loops. The loop code stays the same.
- Two passes are a readable strategy, but not the only one. A correct one-pass solution is with section 11.

</details>

<details>
<summary>Section 11: the output before the fix and the fixed versions</summary>

Before the fix:

<!-- output: rainfall_bug -->
```text
Total rainfall: 13
Highest daily rainfall: 5
Days at highest rainfall: 3
```

| Day | `amount` | `highest` after the first `if` | `days_at_highest` after the second `if` |
|---|---|---|---|
| 1 | 0 | 0 | 1 |
| 2 | 5 | 5 | 2 |
| 3 | 2 | 5 | 2 |
| 4 | 5 | 5 | 3 |
| 5 | 1 | 5 | 3 |
| 6 | 0 | 5 | 3 |

- The total and the highest rainfall are correct. The number of days is wrong: 3 instead of 2.
- **The cause:** the counter is updated in the wrong place, in the same loop in which the program is still looking for the highest rainfall. On the first day, the highest rainfall "so far" is 0, so that day gets counted. Then the highest rainfall rises to 5, but the counter doesn't forget the day it counted earlier.
- **Why C and E gave the right result:** in both cases the highest rainfall is on the first day, so the highest "so far" is final from the start. The same holds for B and D, where every day is equal. The bug shows up in data where a day with less rain comes before the highest rainfall: for A the program prints 3 instead of 2, and for F (`1, 2, 3, 9`) 4 instead of 1, because every day is the highest rainfall for a moment.

**The fix with two passes:** move the second `if`, with the counter, into a separate loop after the first. You get the mission's solution shown above.

**The fix with one pass:** when a new highest rainfall appears, the earlier counting no longer matters, so the counter starts again from zero:

<!-- example: rainfall_one_pass -->
```cpp
#include <iostream>
#include <vector>

int main() {
    const std::vector<int> rainfall{0, 5, 2, 5, 1, 0};

    int total{0};
    int highest{0};
    int days_at_highest{0};

    for (const int amount : rainfall) {
        total += amount;

        if (amount > highest) {
            highest = amount;
            days_at_highest = 0;
        }

        if (amount == highest) {
            ++days_at_highest;
        }
    }

    std::cout << "Total rainfall: " << total << "\n";
    std::cout << "Highest daily rainfall: " << highest << "\n";
    std::cout << "Days at highest rainfall: " << days_at_highest << "\n";
}
```

<!-- output: rainfall_one_pass -->
```text
Total rainfall: 13
Highest daily rainfall: 5
Days at highest rainfall: 2
```

After the counter is reset, the second `if` counts the current day straight away, because its rainfall equals the new `highest`. This version is shorter, but harder to check in your head. Both are correct for all the check cases.

</details>

**Previous lesson:** [Lesson 5.7: A program built from your own functions (the Module 5 test)](../module_05_functions/lesson_07_a_program_of_functions.en.md) · **Next lesson:** [Lesson 6.2: Adding data to a vector: `push_back()` and `empty()`](lesson_02_adding_to_a_vector.en.md) · [Course overview](../../README.en.md)

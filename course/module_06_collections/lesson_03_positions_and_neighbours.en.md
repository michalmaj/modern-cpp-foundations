# Lesson 6.3: Element positions and neighbouring values in a `std::vector`

[Polski](lesson_03_positions_and_neighbours.md) · **English** · [Course overview](../../README.en.md)

> **Module 6, lesson 3** · about 70–85 minutes
> **You need:** your `cpp-workspace` folder and the original `lesson_05_first_program` project, as before. You won't need the debugger in this lesson.
> **Pilot version.** The programs in this lesson are checked automatically on Windows, Ubuntu and macOS, including with the given input data. Typing input in CLion's **Run** window is described without a manual check on every system.

## Before you start

This lesson assumes that after lessons 6.1 and 6.2 you:

- go through a vector with a range-based loop and get the number of elements with `size()`;
- check with `empty()` whether a vector has any elements;
- write a `for` loop with a counter: initial value, condition and update (lesson 4.3);
- know that initialisation with `{}` doesn't allow a narrowing conversion (lesson 2.5).

## The situation

This vector stores four readings from a sensor:

<!-- fragment -->
```cpp
const std::vector<int> readings{10, 14, 11, 19};
```

A range-based loop prints all four values. But try to answer these questions with it alone:

- Which reading is the second one?
- By how much is the second reading greater than the first?
- Is the third reading lower than the second?
- How do you compare **each** reading with the one before it?

A range-based loop gives you one value per pass, and doesn't tell you which position it's at or what came before it. For questions like these you need the **position of an element** in the vector. When the position isn't needed, a range-based loop is still a good choice.

After this lesson you will:

- read the element at a chosen position with `values[index]`, with indices from 0;
- point out the valid indices of a vector and explain why an index equal to `size()` isn't the position of an element;
- read the first and last element of a non-empty vector;
- store sizes and indices in the type `std::size_t`;
- go through positions with a `for` loop and turn an index into a number shown to the user;
- safely compare each element with the previous one, also for an empty and a one-element vector;
- find on your own the largest drop between consecutive measurements.

## 1. Prepare the project

In `cpp-workspace`, create a folder `lesson_6_3` and copy `main.cpp` and `CMakeLists.txt` from the original `lesson_05_first_program` into it. You type the programs from sections 2–7 into `main.cpp` in this folder.

## 2. The element at a chosen position: `[]`

<!-- example: readings_by_index -->
```cpp
#include <iostream>
#include <vector>

int main() {
    const std::vector<int> readings{10, 14, 11, 19};

    std::cout << readings[0] << "\n";
    std::cout << readings[1] << "\n";
    std::cout << readings[2] << "\n";
    std::cout << readings[3] << "\n";
}
```

<!-- output: readings_by_index -->
```text
10
14
11
19
```

Read `readings[1]` as "the element of `readings` at index 1". The number in the square brackets is the **index**, the element's position. **Indices start at 0**:

| Element number for a person | Index in C++ | Value |
|---|---|---|
| 1 | 0 | 10 |
| 2 | 1 | 14 |
| 3 | 2 | 11 |
| 4 | 3 | 19 |

The vector has four elements, so it has the indices 0, 1, 2 and 3. There's no index 4: no element stands there. In general, a vector with `N` elements has the indices from 0 to `N - 1`.

An index only says **where** an element is. The element's value is something else: at index 2 stands the value 11.

## 3. Out of range

**`readings[index]` doesn't check whether the index is valid.** The compiler and the program assume that you keep the index in range.

<!-- fragment -->
```cpp
const std::vector<int> readings{10, 14, 11, 19};
std::cout << readings[4] << "\n";  // wrong: index 4 does not exist
```

This fragment builds. But reading an element that doesn't exist is **undefined behaviour** in C++: the language standard doesn't say what happens then. The program may print a random number, end with an error, or seem to work correctly, and behave differently on another computer. There's no guaranteed compile error or message here. That's why we don't run such programs; we write the code so that **every index is in the range from 0 to `size() - 1`**.

## 4. The first and last element

<!-- example: first_and_last -->
```cpp
#include <iostream>
#include <vector>

int main() {
    const std::vector<int> readings{10, 14, 11, 19};

    if (readings.empty()) {
        std::cout << "No readings\n";
    } else {
        std::cout << "First reading: " << readings[0] << "\n";
        std::cout << "Last reading: " << readings[readings.size() - 1] << "\n";
    }
}
```

**Predict** both lines of output and run the program.

<details>
<summary>Standard output</summary>

<!-- output: first_and_last -->
```text
First reading: 10
Last reading: 19
```

</details>

- The first element has the index 0, and the last one `size() - 1`: here 4 − 1, which is 3.
- **`empty()` first.** An empty vector has no first or last element. What's more, `size()` is then 0, and the result of `size()` is an unsigned number, which can't be negative: `0 - 1` doesn't give −1 here, but a huge positive number. **We don't subtract 1 from the size of an empty vector to get an index.**
- A vector also has the functions `front()` and `back()`, which give the first and last element. In this course we don't use them for now.

## 5. The index type: `std::size_t`

In lesson 6.1 we only printed the result of `size()`. Try storing it in an `int` variable:

<!-- broken: count_as_int at=6:21 errors=1 error=^non-constant-expression cannot be narrowed from type .+ to 'int' in initializer list -->
```cpp
#include <iostream>
#include <vector>

int main() {
    const std::vector<int> readings{10, 14, 11, 19};
    const int count{readings.size()};

    std::cout << "Readings: " << count << "\n";
}
```

**Predict** whether the program builds. Then try to build it.

<details>
<summary>What the compiler reports, and why</summary>

The program won't build. On line 6, the compiler reports `non-constant-expression cannot be narrowed from type ... to 'int' in initializer list`. In place of the dots stands the name of the type `size()` gives. That name depends on the system, for example `'size_type' (aka 'unsigned long')`. It's the same protection as in lesson 2.5: `{}` doesn't allow a narrowing conversion. The type `int` holds negative numbers but can't hold every possible size, so such a change of type could change the value.

</details>

**The fix:** store sizes and indices in the type **`std::size_t`**:

<!-- fragment -->
```cpp
const std::size_t count{readings.size()};
```

- `std::size_t` is an **unsigned** whole-number type: it holds only non-negative numbers.
- It's meant for sizes and indices, so it matches the result of `size()`. Exactly how many numbers it holds depends on the system.
- The header `<cstddef>` makes it available. Always include it when you write `std::size_t`, as you include `<vector>` for a vector.
- **Don't mix `std::size_t` with `int`.** Comparing an `int` variable with `size()` also stops the build with the course flags: the compiler reports `comparison of integers of different signs`.

## 6. A loop over positions

The program prints the readings as successive days:

<!-- example: days_listed -->
```cpp
#include <cstddef>
#include <iostream>
#include <vector>

int main() {
    const std::vector<int> readings{10, 14, 11, 19};
    const std::size_t count{readings.size()};

    std::cout << "Readings: " << count << "\n";

    for (std::size_t index{0}; index < readings.size(); ++index) {
        std::cout << "Day " << index + 1 << ": " << readings[index] << "\n";
    }
}
```

**Predict** every line of output and run the program.

<details>
<summary>Standard output</summary>

<!-- output: days_listed -->
```text
Readings: 4
Day 1: 10
Day 2: 14
Day 3: 11
Day 4: 19
```

</details>

This is the `for` loop from lesson 4.3, with a counter that is an index:

1. `std::size_t index{0}`: the index starts at 0, the first element.
2. `index < readings.size()`: the loop goes on while the index points at an existing element.
3. `readings[index]`: reading the element at the current index.
4. `++index`: moving on to the next position.
5. When `index` reaches 4, which is `size()`, the condition gives `false` and the loop ends **without** reading `readings[4]`.

**An index isn't a day number.** In the code the first element has the index 0, and the user sees "Day 1". The program **computes** the day number: `index + 1`. The indexing itself doesn't change: a vector always starts at index 0, and numbering from 1 is only a way to show the result to a person.

A range-based loop gives the successive values. A loop over indices also gives the **position** of each value. When the position isn't needed, choose a range-based loop.

## 7. Neighbouring elements

The change between two consecutive readings is the current reading minus the previous one: `readings[index] - readings[index - 1]`.

<!-- example: changes -->
```cpp
#include <cstddef>
#include <iostream>
#include <vector>

int main() {
    const std::vector<int> readings{10, 14, 11, 19};

    for (std::size_t index{1}; index < readings.size(); ++index) {
        const int change{readings[index] - readings[index - 1]};
        std::cout << change << "\n";
    }
}
```

**Predict** how many numbers the program prints, and which. Then run it.

<details>
<summary>Standard output</summary>

<!-- output: changes -->
```text
4
-3
8
```

</details>

| Index of the current | Previous value | Current value | Change |
|---|---|---|---|
| 1 | 10 | 14 | +4 |
| 2 | 14 | 11 | −3 |
| 3 | 11 | 19 | +8 |

- **The loop starts at index 1**, because the element at index 0 has no predecessor. For every index from 1 upwards, the previous element, `index - 1`, exists.
- **The condition `index < readings.size()`** makes sure the current element exists too.
- Four elements give **three** pairs of neighbours: each pair is an element together with the previous one, and the first element has no predecessor.

**Your turn.** How many passes does this loop make for the empty vector `{}`, for `{5}` and for `{5, 8}`?

<details>
<summary>Answer</summary>

- `{}`: zero. `index` starts at 1, and `1 < 0` gives `false`.
- `{5}`: zero. `1 < 1` gives `false`. One element doesn't make a pair.
- `{5, 8}`: one pass, for index 1: the change 8 − 5 = 3.

The same loop is safe for every size, with no separate check. Compare it with two wrong ideas:

<!-- fragment -->
```cpp
// wrong: for index 0, index - 1 is not the index of any element
for (std::size_t index{0}; index < readings.size(); ++index) {
    const int change{readings[index] - readings[index - 1]};
}

// wrong: for an empty vector, readings.size() - 1 is not -1
for (std::size_t index{0}; index < readings.size() - 1; ++index) {
    const int change{readings[index + 1] - readings[index]};
}
```

In the first, `index - 1` for index 0 doesn't point at any element. In the second, for an empty vector, `readings.size() - 1` is a huge number, so the loop tries to read elements that don't exist. Both are undefined behaviour, so we don't run them.

</details>

## 8. Mission: the largest cold snap

The program stores temperatures from successive days, in whole degrees Celsius, and looks for the largest temperature drop between two consecutive days. The data is written in the code:

<!-- fragment -->
```cpp
const std::vector<int> temperatures{8, 5, 7, 1, 0, 3};
```

A **drop** is when the earlier day's temperature is higher than the next day's. For the pair 8 and 5, the drop is 3. For the pair 5 and 8, there's no cooling. For two equal temperatures the change is 0, and that isn't a drop.

**Requirements:**

- The program stores the temperatures in a `const std::vector<int>` with initial values. It doesn't read anything from the input.
- The first line is always `Days recorded: N`, where `N` is the number of days.
- For fewer than two days, the program prints `Not enough days`.
- For at least two days, if the temperature never dropped, it prints `No temperature drop`.
- Otherwise it prints `Largest drop: N`, the largest drop, and `From day X to day Y`, the numbers of the days between which it happened. Days are numbered from 1.
- If the same largest drop happened several times, the program points to the **first** such occurrence.
- The program works correctly after changing only the values in the braces, also for an empty vector and for one day. It doesn't read elements out of range.

In `cpp-workspace`, create a folder `largest_drop`, copy `CMakeLists.txt` from the original `lesson_05_first_program` into it, create an empty `main.cpp` and write the program on your own.

**Example A:** the data from the requirements.

<!-- output: largest_drop -->
```text
Days recorded: 6
Largest drop: 6
From day 3 to day 4
```

**Example B:** `{2, 5, 8}`.

```text
Days recorded: 3
No temperature drop
```

**Example C:** `{3}`.

```text
Days recorded: 1
Not enough days
```

Examples B and C, like all the check cases, are checked automatically in the full list of check cases below.

**This isn't the program from section 7 with different data.** That program only printed the changes. You have to decide on your own:

1. where to store the largest drop and what value it starts from;
2. how to recognise that the current change is a drop, and how to compute its size;
3. what else you need to remember to print the day numbers;
4. when to replace the remembered result with a new one, also when there's a tie;
5. how to turn positions in the vector into day numbers;
6. how to recognise that there was no drop;
7. how to handle an empty vector and one day without reaching for elements that don't exist.

**Before you write the program**, prepare a table of test cases: an empty vector, one day, two days with a drop, only rises, only equal temperatures, negative temperatures, the largest drop at the start and at the end, two equal largest drops, and equal temperatures before a drop. For each case, write down the expected standard output.

**Then work in this order:**

1. Write the program and run it for the data from the requirements.
2. Change the values in the braces to each case in your table in turn. Predict the result before each run.
3. For each mismatch, check whether the mistake is in the program or in the table.

### Success criteria

- The program builds as C++20 and, for the data from the requirements, prints exactly the three lines of example A.
- For every case in the table the result matches the requirements, after changing only the values in the braces.
- With a tie, the program points to the first occurrence of the largest drop.
- No index in the program goes out of range, also for an empty vector and for one day.
- The indices are of type `std::size_t`, and the day numbers shown to the user start at 1.
- The table of cases was made before the program was run.
- You can explain which index your loop starts at, and why.

When the result matches, you can save the project in Git, as in lesson 1.5.

<details>
<summary>Hint 1</summary>

To find a change in temperature, which two consecutive elements do you need to compare?

</details>

<details>
<summary>Hint 2</summary>

Think about which index you can start from to use the current and the previous element safely.

</details>

<details>
<summary>Hint 3</summary>

While going through the pairs, remember the best positive drop so far and its position. For a tie, the requirement says to keep the first occurrence.

</details>

<details>
<summary>The full list of check cases: open it after preparing your own table</summary>

| Temperatures | Standard output after `Days recorded: N` | What it checks |
|---|---|---|
| `{}` | `Not enough days` | an empty vector |
| `{3}` | `Not enough days` | example C: one day |
| `{8, 5}` | a drop of 3, days 1–2 | the smallest pair |
| `{2, 5, 8}` | `No temperature drop` | example B: only rises |
| `{4, 4, 4}` | `No temperature drop` | a change of 0 isn't a drop |
| `{8, 5, 7, 1, 0, 3}` | a drop of 6, days 3–4 | example A |
| `{9, 5, 1}` | a drop of 4, days 1–2 | a tie: the first occurrence, at the start |
| `{7, 1, 7, 1}` | a drop of 6, days 1–2 | a tie separated by a rise |
| `{-2, -7, -9, -4}` | a drop of 5, days 1–2 | negative temperatures |
| `{6, 6, 3, 3}` | a drop of 3, days 2–3 | equal temperatures before and after the drop |
| `{1, -20, 40, 0}` | a drop of 40, days 3–4 | two drops, the larger at the end |

In the last case, the drop between days 1 and 2 is 21, and between days 3 and 4 it's 40. The program chooses the larger one.

**How these results were checked.** The mission program has its data in the code, so each data set would need a separate program. That's why one check program checks every case: the same algorithm as the reference solution, but it reads the temperatures from the input, first how many there are and then the values. It prints no questions, so its standard output is the same as the mission's result for that data. That program and its results are in [Example solutions](#example-solutions). Open them only after writing your own program, because they contain the solution.

</details>

An example solution is in [Example solutions](#example-solutions).

## 9. Find the bug: which tie?

Do this task **after the mission**: the program below contains the whole algorithm for finding the largest drop. It reads the temperatures from the input, like the check program: first the number of days, then the temperatures one by one. According to the requirement, with a tie it should point to the first occurrence.

<details>
<summary>The program to check: open it after writing your own program</summary>

<!-- example: drop_tie_bug -->
```cpp
#include <cstddef>
#include <iostream>
#include <vector>

int main() {
    std::vector<int> temperatures{};
    int day_count{0};
    std::cin >> day_count;

    for (int day{1}; day <= day_count; ++day) {
        int temperature{0};
        std::cin >> temperature;
        temperatures.push_back(temperature);
    }

    if (std::cin.fail()) {
        std::cout << "Input could not be read\n";
    } else {
        std::cout << "Days recorded: " << temperatures.size() << "\n";

        if (temperatures.size() < 2) {
            std::cout << "Not enough days\n";
        } else {
            int largest_drop{0};
            std::size_t drop_index{0};

            for (std::size_t index{1}; index < temperatures.size(); ++index) {
                const int drop{temperatures[index - 1] - temperatures[index]};

                if (drop >= largest_drop) {
                    largest_drop = drop;
                    drop_index = index;
                }
            }

            if (largest_drop == 0) {
                std::cout << "No temperature drop\n";
            } else {
                std::cout << "Largest drop: " << largest_drop << "\n";
                std::cout << "From day " << drop_index << " to day " << drop_index + 1 << "\n";
            }
        }
    }
}
```

1. **Predict** the result for data A, `6`, `8`, `5`, `7`, `1`, `0`, `3`, with a single largest drop.
2. Run the program with that data and check that the result looks correct.
3. Analyse the data `4`, `7`, `1`, `7`, `1`, with two equal largest drops. Which drop should the program point to?
4. Run the program with that data. Which pair of days does it point to?
5. Find the condition that decides whether a new result is stored.
6. Fix the program.
7. Check both cases again.

</details>

The program's output before the fix, and the fixed program, are in [Example solutions](#example-solutions).

## 10. When something goes differently

| What you see | What it means | What to do |
|---|---|---|
| `cannot be narrowed from type ... to 'int'` | The result of `size()` goes into an `int` variable with `{}` (section 5). | Use `std::size_t`. |
| `comparison of integers of different signs` | An `int` index is compared with `size()`. | Declare the index as `std::size_t`. |
| A compile error at `std::size_t` | `#include <cstddef>` is missing, or the name has a typo. On some systems the program builds without `<cstddef>` too, but on others it doesn't. | Add `#include <cstddef>`. |
| The day numbers are one too small, for example `From day 2 to day 3` instead of `From day 3 to day 4` | The program prints indices instead of day numbers. | A day number is the index + 1. Check which index you remember: the current one or the previous one. |
| The drop comes out negative, or appears where there was a rise | The subtraction is the wrong way round. | A drop is the earlier day's temperature minus the next day's. |
| With a tie, the program points to the last occurrence | The condition stores a new result also when it equals the remembered one (section 9). | Store only a result that is strictly greater. |
| The program prints strange numbers or ends unexpectedly | Probably a read out of range: an index equal to `size()`, or `index - 1` for index 0. | Check the loop's condition and initial value. A loop over neighbours starts at index 1. |

## 11. Explain

Answer in your own words, preferably in writing. Only then compare with the example answers.

1. What are indices for, when a range-based loop goes through every element?
2. What index does the first element have, and what index the last element of a vector with 5 elements?
3. Is `values[5]` correct for a vector with 5 elements? What happens?
4. Why do we check `empty()` before reading `values[values.size() - 1]`?
5. What is `std::size_t`, and why do we use it?
6. Why doesn't `const int count{values.size()};` build?
7. Why does the program with days print `index + 1`?
8. Why does the loop over neighbours start at index 1?
9. How many pairs of neighbours does a vector with 4 elements have? And with one element, and with zero?
10. When do you choose a range-based loop, and when a loop over indices?
11. Why does the condition in the mission use `>` and not `>=` for a tie?

<details>
<summary>Example answers</summary>

1. Because some tasks need the position of an element: reading a particular element, or comparing it with the previous one. A range-based loop gives the values, but not their positions.
2. The first has the index 0, the last 4, which is `size() - 1`.
3. No. The valid indices are 0–4. `values[5]` is a read out of range, which is undefined behaviour: there's no knowing what happens, and you mustn't rely on it. `[]` checks nothing.
4. Because an empty vector has no last element, and `size() - 1` for a size of 0 doesn't give −1, but a huge positive number, because the result of `size()` is unsigned.
5. It's an unsigned whole-number type, meant for sizes and indices. It matches the result of `size()`, so there's no narrowing conversion and no comparison of signed with unsigned numbers.
6. Because `{}` doesn't allow a narrowing conversion: the type `size()` gives doesn't always fit into an `int` without changing the value.
7. Because the user counts days from 1, and indices start at 0. The position in the vector and the number shown to a person are two different things.
8. Because we compare an element with the previous one, and the element at index 0 has no predecessor. For every index from 1 upwards, a predecessor exists.
9. Three pairs. One element and zero elements make no pair, and a loop from index 1 makes no passes then.
10. A range-based loop when you need only the successive values. A loop over indices when you also need positions: the element's number or a neighbouring element.
11. Because with a tie the result should point to the first occurrence. With `>`, a second, equal drop doesn't replace the remembered one. With `>=` it would replace it, so the program would point to the last occurrence.

</details>

## Summary

- `values[index]` reads the element at the given **index**. Indices start at 0, so a vector with `N` elements has the indices from 0 to `N - 1`.
- `[]` doesn't check the range. A read out of range is undefined behaviour, so you make sure every index is valid.
- The first element is `values[0]`, the last `values[values.size() - 1]`, both only for a non-empty vector.
- You store sizes and indices in `std::size_t` from `<cstddef>`. You don't store `size()` in an `int`, and you don't compare `int` variables with it.
- A loop over indices: `for (std::size_t index{0}; index < values.size(); ++index)`. It ends when the index reaches `size()`, without reading an element that doesn't exist.
- The number shown to the user is `index + 1`. The vector's indexing doesn't change.
- You go through pairs of neighbours from index 1: `values[index]` and `values[index - 1]`. That loop is safe also for an empty and a one-element vector.
- When the position isn't needed, a range-based loop is still a good choice.

## What's next

So far, a whole program with a vector fitted in `main`. In the next lesson you'll pass a vector to your own function, which only reads it: [Lesson 6.4: A vector as a function parameter: `const&`](lesson_04_a_vector_as_a_parameter.en.md).

---

## Example solutions

Look here **after your own attempt**. Your names may differ, as long as the standard output is as required.

<details>
<summary>Section 8: the mission, the largest cold snap</summary>

<!-- example: largest_drop -->
```cpp
#include <cstddef>
#include <iostream>
#include <vector>

int main() {
    const std::vector<int> temperatures{8, 5, 7, 1, 0, 3};

    std::cout << "Days recorded: " << temperatures.size() << "\n";

    if (temperatures.size() < 2) {
        std::cout << "Not enough days\n";
    } else {
        int largest_drop{0};
        std::size_t drop_index{0};

        for (std::size_t index{1}; index < temperatures.size(); ++index) {
            const int drop{temperatures[index - 1] - temperatures[index]};

            if (drop > largest_drop) {
                largest_drop = drop;
                drop_index = index;
            }
        }

        if (largest_drop == 0) {
            std::cout << "No temperature drop\n";
        } else {
            std::cout << "Largest drop: " << largest_drop << "\n";
            std::cout << "From day " << drop_index << " to day " << drop_index + 1 << "\n";
        }
    }
}
```

1. **The loop starts at index 1**, because each pair is the current day and the previous one, and the first day has no previous day.
2. **The previous element is available**, because for `index` from 1 upwards `index - 1` is an existing index, and the condition `index < temperatures.size()` takes care of the current one.
3. **A drop** is the earlier day's temperature minus the next day's: `temperatures[index - 1] - temperatures[index]`. It's positive only when the temperature fell. A rise gives a negative number, and equal temperatures give 0.
4. **The best pair:** `largest_drop` remembers the largest drop so far, and `drop_index` the index of the day **after** the drop. The initial value 0 means "no drop yet": only a positive drop can replace it. That's why `largest_drop == 0` after the loop means there was no drop.
5. **A tie:** the condition `drop > largest_drop` replaces the result only with a strictly greater drop. An equal drop later changes nothing, so the first occurrence stays.
6. **Day numbers:** the pair with the indices `drop_index - 1` and `drop_index` is the days numbered `drop_index` and `drop_index + 1`, because a day number is the index + 1.
7. **An empty and a one-element vector** have no pair, so the program prints `Not enough days` and doesn't start comparing at all. The loop itself wouldn't run then either, but without that check the program would print `No temperature drop`, as if it had compared some days.

It's a readable solution, but not the only one. For example, you can remember the index of the day before the drop instead of after it, as long as the day numbers are worked out correctly afterwards.

**The check program** checks every case in the list of check cases. The part after reading the data is the same as in the solution above, apart from the indentation. It differs only in where the data comes from: the vector has no `const`, because the program adds the temperatures it reads with `push_back`, as in lesson 6.2.

<!-- example: largest_drop_check -->
```cpp
#include <cstddef>
#include <iostream>
#include <vector>

int main() {
    std::vector<int> temperatures{};
    int day_count{0};
    std::cin >> day_count;

    for (int day{1}; day <= day_count; ++day) {
        int temperature{0};
        std::cin >> temperature;
        temperatures.push_back(temperature);
    }

    if (std::cin.fail()) {
        std::cout << "Input could not be read\n";
    } else {
        std::cout << "Days recorded: " << temperatures.size() << "\n";

        if (temperatures.size() < 2) {
            std::cout << "Not enough days\n";
        } else {
            int largest_drop{0};
            std::size_t drop_index{0};

            for (std::size_t index{1}; index < temperatures.size(); ++index) {
                const int drop{temperatures[index - 1] - temperatures[index]};

                if (drop > largest_drop) {
                    largest_drop = drop;
                    drop_index = index;
                }
            }

            if (largest_drop == 0) {
                std::cout << "No temperature drop\n";
            } else {
                std::cout << "Largest drop: " << largest_drop << "\n";
                std::cout << "From day " << drop_index << " to day " << drop_index + 1 << "\n";
            }
        }
    }
}
```

The input data is the number of days, followed by the temperatures. The cases come in the same order as in the list of check cases.

<!-- input: largest_drop_check -->
```text
0
```

<!-- output: largest_drop_check -->
```text
Days recorded: 0
Not enough days
```

<!-- input: largest_drop_check -->
```text
1
3
```

<!-- output: largest_drop_check -->
```text
Days recorded: 1
Not enough days
```

<!-- input: largest_drop_check -->
```text
2
8
5
```

<!-- output: largest_drop_check -->
```text
Days recorded: 2
Largest drop: 3
From day 1 to day 2
```

<!-- input: largest_drop_check -->
```text
3
2
5
8
```

<!-- output: largest_drop_check -->
```text
Days recorded: 3
No temperature drop
```

<!-- input: largest_drop_check -->
```text
3
4
4
4
```

<!-- output: largest_drop_check -->
```text
Days recorded: 3
No temperature drop
```

<!-- input: largest_drop_check -->
```text
6
8
5
7
1
0
3
```

<!-- output: largest_drop_check -->
```text
Days recorded: 6
Largest drop: 6
From day 3 to day 4
```

<!-- input: largest_drop_check -->
```text
3
9
5
1
```

<!-- output: largest_drop_check -->
```text
Days recorded: 3
Largest drop: 4
From day 1 to day 2
```

<!-- input: largest_drop_check -->
```text
4
7
1
7
1
```

<!-- output: largest_drop_check -->
```text
Days recorded: 4
Largest drop: 6
From day 1 to day 2
```

<!-- input: largest_drop_check -->
```text
4
-2
-7
-9
-4
```

<!-- output: largest_drop_check -->
```text
Days recorded: 4
Largest drop: 5
From day 1 to day 2
```

<!-- input: largest_drop_check -->
```text
4
6
6
3
3
```

<!-- output: largest_drop_check -->
```text
Days recorded: 4
Largest drop: 3
From day 2 to day 3
```

<!-- input: largest_drop_check -->
```text
4
1
-20
40
0
```

<!-- output: largest_drop_check -->
```text
Days recorded: 4
Largest drop: 40
From day 3 to day 4
```

</details>

<details>
<summary>Section 9: the output before the fix, and the fixed program</summary>

Before the fix, for data A:

<!-- input: drop_tie_bug -->
```text
6
8
5
7
1
0
3
```

<!-- output: drop_tie_bug -->
```text
Days recorded: 6
Largest drop: 6
From day 3 to day 4
```

For the data `4`, `7`, `1`, `7`, `1`:

<!-- input: drop_tie_bug -->
```text
4
7
1
7
1
```

<!-- output: drop_tie_bug -->
```text
Days recorded: 4
Largest drop: 6
From day 3 to day 4
```

- For data A the result is correct, because the largest drop occurs only once.
- For `7`, `1`, `7`, `1` the drop of 6 occurs twice: between days 1 and 2, and between days 3 and 4. The requirement asks for the first occurrence, but the program points to days 3–4.
- **The cause:** the condition `drop >= largest_drop` stores a new result also when the drop is **equal** to the remembered one. So the second drop of 6 replaces the first.
- **The fix:** change `>=` to `>`. Then only a strictly greater drop replaces the result.

The fixed program is the check program from section 8: it differs from the buggy program only in that one character. For both data sets above it gives the results from the list of check cases: days 3–4 for A, and days 1–2 for `7`, `1`, `7`, `1`.

</details>

**Previous lesson:** [Lesson 6.2: Adding data to a vector: `push_back()` and `empty()`](lesson_02_adding_to_a_vector.en.md) · **Next lesson:** [Lesson 6.4: A vector as a function parameter: `const&`](lesson_04_a_vector_as_a_parameter.en.md) · [Course overview](../../README.en.md)

# Lesson 6.5: A function creates and returns a new vector

[Polski](lesson_05_a_function_returns_a_vector.md) · **English** · [Course overview](../../README.en.md)

> **Module 6, lesson 5** · about 65–80 minutes
> **You need:** your `cpp-workspace` folder and the original `lesson_05_first_program` project, as before. You won't need the debugger in this lesson.
> **Pilot version.** The programs in this lesson are checked automatically on Windows, Ubuntu and macOS, including with the given input data. Typing input in CLion's **Run** window is described without a manual check on every system.

## Before you start

This lesson assumes that after lessons 6.1–6.4 you:

- go through a vector with a range-based loop and add elements with `push_back`;
- check `empty()` and `size()`;
- write functions that get a vector through `const std::vector<int>&` and return an `int` result (lesson 6.4);
- know that a variable declared in a function is its local variable (lesson 5.2), and that `return` passes a result to the place of the call (lesson 5.3).

## The situation

In lesson 6.4, the function `int count_cold_days(const std::vector<int>& temperatures)` returned the **number** of days below zero. Let's change the question: you want to get **the temperatures themselves** that are below zero, so that you can go through them again later. For the data `{3, -2, 0, -5, 4}` the result should be `{-2, -5}`.

The number 2 alone isn't enough here: you can't recover the values −2 and −5 from it. You need a result that stores many values, a **vector**. The function returning an `int` wasn't worse: it answered a different question.

After this lesson you will:

- write functions with the result type `std::vector<int>` that build a new vector and return it with `return`;
- receive a returned vector in `main` and keep working with it;
- explain why the input vector stays unchanged, and why the order of the chosen elements is kept;
- recognise an empty result as correct and check it with `empty()`;
- pass a returned vector to another function;
- design processing on your own: input data → a new collection → a summary.

## 1. Prepare the project

In `cpp-workspace`, create a folder `lesson_6_5` and copy `main.cpp` and `CMakeLists.txt` from the original `lesson_05_first_program` into it. You type the programs from sections 2–5 into `main.cpp` in this folder.

## 2. A function that returns a vector

<!-- example: negatives_selected -->
```cpp
#include <iostream>
#include <vector>

std::vector<int> keep_negative(const std::vector<int>& values) {
    std::vector<int> selected{};

    for (const int value : values) {
        if (value < 0) {
            selected.push_back(value);
        }
    }

    return selected;
}

int main() {
    const std::vector<int> temperatures{3, -2, 0, -5, 4};

    std::cout << "Original:";
    for (const int temperature : temperatures) {
        std::cout << " " << temperature;
    }
    std::cout << "\n";

    const std::vector<int> selected{keep_negative(temperatures)};

    std::cout << "Selected:";
    for (const int temperature : selected) {
        std::cout << " " << temperature;
    }
    std::cout << "\n";

    std::cout << "Original after:";
    for (const int temperature : temperatures) {
        std::cout << " " << temperature;
    }
    std::cout << "\n";
}
```

**Predict** all three lines. After the call to `keep_negative`, will only the negative values remain in `temperatures`? Then run the program.

<details>
<summary>Standard output</summary>

<!-- output: negatives_selected -->
```text
Original: 3 -2 0 -5 4
Selected: -2 -5
Original after: 3 -2 0 -5 4
```

</details>

**The function:**

- **The result type is `std::vector<int>`**: the function returns a whole vector of `int`s, not one number.
- **The input goes by `const&`**, as in lesson 6.4: the function only reads `values`.
- **`selected` is a separate, local vector**, empty at first. It has no `const`, because the function adds elements to it.
- The loop goes through the input values, and `push_back` adds to `selected` only those that meet the condition. So the order of the chosen elements is the same as in the input.
- **`return selected;`** passes the finished vector to the place of the call. It's returning **by value**, like the `return` of a number in lesson 5.3: the caller gets its own result. The vector `selected`, as a local variable, ends together with the function, but its contents reach `main` as the result.

**`main`:**

- `const std::vector<int> selected{keep_negative(temperatures)};` creates a new variable and stores the result of the call in it. `main` doesn't intend to change this collection, so it has `const`. That isn't a rule: in another program, a returned vector can be changed further.
- **The original is unchanged.** The function removes nothing from it: it only reads it and builds a separate collection. The third line confirms that.
- The values are printed with a space **before** each number, and the label, for example `Original:`, ends with a colon. That way no extra space is left at the end of the line.

The name `selected` appears in both functions, but they're two different local variables, as in lesson 5.2.

## 3. The flow of the data

| Stage | Data |
|---|---|
| the argument in `main` | `temperatures`: `{3, -2, 0, -5, 4}` |
| the parameter `values` | refers to `temperatures`, without a copy |
| the initial local result `selected` | `{}` |
| after adding −2 | `{-2}` |
| after adding −5 | `{-2, -5}` |
| `return selected;` | the function passes the new vector |
| the result in `main` | `selected`: `{-2, -5}` |
| the original | `temperatures`: still `{3, -2, 0, -5, 4}` |

The function does three different things: it **reads** an existing vector through a reference, **builds** a new collection, and **returns** it by value. The new vector isn't a second name for the original, but a separate result.

Is returning a whole vector expensive? Modern C++ can return collections by value efficiently. You'll learn later exactly how it does that. For now this model is enough: **the function creates a result collection and returns it as a value, and the caller gets its own result.**

## 4. An empty result

<!-- example: no_negatives -->
```cpp
#include <iostream>
#include <vector>

std::vector<int> keep_negative(const std::vector<int>& values) {
    std::vector<int> selected{};

    for (const int value : values) {
        if (value < 0) {
            selected.push_back(value);
        }
    }

    return selected;
}

int main() {
    const std::vector<int> temperatures{2, 4, 7};
    const std::vector<int> selected{keep_negative(temperatures)};

    std::cout << "Values checked: " << temperatures.size() << "\n";

    if (selected.empty()) {
        std::cout << "No values below zero\n";
    } else {
        std::cout << "Values below zero: " << selected.size() << "\n";
    }
}
```

**Predict** which branch the program runs, and run it.

<details>
<summary>Standard output</summary>

<!-- output: no_negatives -->
```text
Values checked: 3
No values below zero
```

</details>

The input has three elements, but none meets the condition, so the function adds nothing to `selected` and returns an empty vector. **That's a correct result, not an error**: "there are no such values" is an answer too. The caller recognises it with `empty()`. You don't read elements from an empty result, for example `selected[0]`: there's no such element (lesson 6.3).

## 5. The result goes to another function

A returned vector is an ordinary `std::vector<int>`, so you can pass it to a function from lesson 6.4:

<!-- example: negative_total -->
```cpp
#include <iostream>
#include <vector>

std::vector<int> keep_negative(const std::vector<int>& values) {
    std::vector<int> selected{};

    for (const int value : values) {
        if (value < 0) {
            selected.push_back(value);
        }
    }

    return selected;
}

int total_values(const std::vector<int>& values) {
    int total{0};

    for (const int value : values) {
        total += value;
    }

    return total;
}

int main() {
    const std::vector<int> temperatures{3, -2, 0, -5, 4};
    const std::vector<int> selected{keep_negative(temperatures)};

    std::cout << "Values below zero: " << selected.size() << "\n";
    std::cout << "Their total: " << total_values(selected) << "\n";
}
```

**Predict** both lines and run the program.

<details>
<summary>Standard output</summary>

<!-- output: negative_total -->
```text
Values below zero: 2
Their total: -7
```

</details>

1. `main` has the original vector `temperatures`.
2. It calls the selecting function.
3. It stores the new vector in the named variable `selected`.
4. It passes `selected` to `total_values` through `const&`.
5. It gets an `int` result.
6. It prints the report.

Each function has one task: one selects, the other sums, and `main` prints. The result could also be passed on straight away, without the intermediate variable, and that's valid C++ too. In this lesson we store it in a named variable, because then every stage is visible and easy to check.

## 6. Mission: checking the lengths of pieces

In a workshop, the lengths of pieces are measured in whole centimetres. A piece is **accepted** if its length is in the range from 30 to 60 cm **inclusive**. The data is written in the code:

<!-- fragment -->
```cpp
const std::vector<int> lengths{28, 30, 45, 65, 60, 29, 30};
```

**Requirements:**

- The original vector is a `const std::vector<int>` in `main`, and stays unchanged. The program doesn't read anything from the input.
- **The selecting function:** takes the existing vector through `const&`, plus the lower and upper bound as two `int` parameters, builds a new vector with the accepted lengths, in their order, and returns it as a `std::vector<int>`. It prints nothing.
- **The summing function:** takes a vector through `const&` and returns the sum of its values as an `int`, also for an empty vector. It prints nothing.
- You choose the names of the functions and parameters yourself.
- `main` calls the selecting function, stores the result in a variable, passes it to the summing function and prints the report:
  - `Original pieces: N`: the number of elements of the original vector;
  - `Accepted pieces: N`: the number of accepted elements;
  - `Accepted lengths:` followed, after a space, by the accepted lengths separated by spaces, with no space at the end of the line, or `Accepted lengths: none` when no piece was accepted;
  - `Total accepted length: N`: the sum of the accepted lengths, 0 for an empty result.
- The values are small, so the sum fits safely in an `int`.

In `cpp-workspace`, create a folder `piece_lengths`, copy `CMakeLists.txt` from the original `lesson_05_first_program` into it, create an empty `main.cpp` and write the program on your own.

For the data above, the standard output must be:

<!-- output: piece_lengths -->
```text
Original pieces: 7
Accepted pieces: 4
Accepted lengths: 30 45 60 30
Total accepted length: 165
```

**This isn't the program from section 5 with different messages.** There, the condition was a single fixed one. You have to decide on your own:

1. what parameters the selecting function has, and in what order;
2. how to write the condition so that both bounds, 30 and 60, are accepted;
3. where the result vector is created and when to add an element to it;
4. how to receive the result in `main` and pass it to the summing function;
5. how to print the list of lengths with no space at the end, and when to print `none`;
6. how to check that the original vector didn't change.

**Before you write the program**, prepare a table of cases: the data from the requirements, an empty vector, no matching lengths, all matching, both bounds separately and together, values just outside the bounds (29 and 61), repeated values, and the same lengths in a different order. For each, write down the accepted lengths and the sum.

**Then:** run the program for the data from the requirements, and then change the values in the braces to two or three cases from your table, for example an empty result and both bounds. Every case in the full list of check cases is checked automatically, so you don't need to type them all.

### Success criteria

- The program builds as C++20 and, for the data from the requirements, prints exactly the four lines shown above.
- The selecting function returns a new `std::vector<int>`, takes the vector through `const&` and two `int` bounds, and the lengths 30 and 60 are accepted.
- The accepted lengths come in the order of the original, with repetitions.
- The sum is computed by a separate function that gets the returned vector.
- For an empty result the program prints `Accepted lengths: none` and a sum of 0.
- No line ends with a space, and the original vector doesn't change.
- You can explain why the parameter has `&` and the result type doesn't.

When the result matches, you can save the project in Git, as in lesson 1.5.

<details>
<summary>Hint 1</summary>

How should the input vector differ from the result vector once the filtering is done?

</details>

<details>
<summary>Hint 2</summary>

The function can create an empty vector and add to it only the lengths that meet both bounds of the range.

</details>

<details>
<summary>Hint 3</summary>

After you get the new vector, don't compute the sum again in `main()`. Pass the result of the filtering to a separate summing function.

</details>

<details>
<summary>The full list of check cases: open it after preparing your own table</summary>

| | Original lengths | Accepted | Sum | What it checks |
|---|---|---|---|---|
| A | `{28, 30, 45, 65, 60, 29, 30}` | `30 45 60 30` | 165 | the data from the requirements |
| B | `{}` | `none` | 0 | an empty input |
| C | `{10, 29, 61}` | `none` | 0 | nothing matches, values just outside the bounds |
| D | `{30, 45, 60}` | `30 45 60` | 135 | everything matches |
| E | `{29, 30, 60, 61}` | `30 60` | 90 | both bounds and the values next to them |
| F | `{30}` | `30` | 30 | the lower bound, one element |
| G | `{60}` | `60` | 60 | the upper bound, one element |
| H | `{45}` | `45` | 45 | one element in the middle |
| I | `{30, 30, 60, 60}` | `30 30 60 60` | 180 | repetitions at the bounds |
| J | `{60, 30, 45, 30}` | `60 30 45 30` | 165 | the order is kept |
| K | `{0, 0}` | `none` | 0 | zeros |
| L | `{30, 45}` | `30 45` | 75 | without the upper bound (section 7) |
| M | `{30, 60}` | `30 60` | 90 | with the upper bound (section 7) |

**Automatic tests and your own runs.** Every case is checked automatically by a check program. It has the same functions and the same report as the reference solution, but it reads the lengths from the input: first how many there are, then the values. It's only a checking tool, not part of the mission. The check program and its results are in [Example solutions](#example-solutions), because they contain the solution.

</details>

An example solution is in [Example solutions](#example-solutions).

## 7. Find the bug: the lost bound

Do this task **after the mission**: the program below contains the mission's selecting function. It reads the lengths from the input, like the check program. The requirement: lengths from 30 to 60 cm **inclusive** are accepted.

<details>
<summary>The program to check: open it after writing your own program</summary>

<!-- example: lengths_bound_bug -->
```cpp
#include <iostream>
#include <vector>

std::vector<int> keep_in_range(const std::vector<int>& values, int lowest, int highest) {
    std::vector<int> selected{};

    for (const int value : values) {
        if (value >= lowest && value < highest) {
            selected.push_back(value);
        }
    }

    return selected;
}

int total_length(const std::vector<int>& values) {
    int total{0};

    for (const int value : values) {
        total += value;
    }

    return total;
}

int main() {
    std::vector<int> lengths{};
    int piece_count{0};
    std::cin >> piece_count;

    for (int piece{1}; piece <= piece_count; ++piece) {
        int length{0};
        std::cin >> length;
        lengths.push_back(length);
    }

    if (std::cin.fail()) {
        std::cout << "Input could not be read\n";
    } else {
        const std::vector<int> accepted{keep_in_range(lengths, 30, 60)};

        std::cout << "Original pieces: " << lengths.size() << "\n";
        std::cout << "Accepted pieces: " << accepted.size() << "\n";

        std::cout << "Accepted lengths:";
        if (accepted.empty()) {
            std::cout << " none";
        } else {
            for (const int length : accepted) {
                std::cout << " " << length;
            }
        }
        std::cout << "\n";

        std::cout << "Total accepted length: " << total_length(accepted) << "\n";
    }
}
```

1. Read the requirement and **predict** the contents of the new vector for the data `{30, 45}`, which is `2`, `30`, `45`, and for `{30, 60}`, which is `2`, `30`, `60`.
2. Run the program for `{30, 45}`. Is the result correct?
3. Run it for `{30, 60}`.
4. Compare both results with the requirement. Why doesn't the first case reveal the bug?
5. Find the wrong comparison.
6. Fix the condition.
7. Check both cases again, and also the lengths 29 and 61.

</details>

The program's output before the fix, and the fixed program, are in [Example solutions](#example-solutions).

## 8. When something goes differently

| What you see | What it means | What to do |
|---|---|---|
| A length of 60 or 30 isn't accepted | The condition uses `<` or `>` instead of `<=` or `>=`. | The bounds are inclusive. Check cases F, G and M. |
| Every length is accepted | `push_back` stands outside the condition, as in lesson 6.2. | `push_back` only inside the `if` block. |
| The order of the lengths in the result differs from the original | The result isn't built in one pass over the original, from start to end. | Add the elements in the order of the range-based loop. Check case J. |
| The line with the lengths ends with a space | A space is printed **after** each number. | Print the space **before** each number, as in section 2. |
| For an empty result, `none` is missing, or only `Accepted lengths:` appears | The `empty()` check before printing is missing. | Check `empty()` on the returned vector. |
| A compile error when receiving the result | The type of the variable in `main` or the function's result type doesn't match, for example `int` instead of `std::vector<int>`. | The selecting function returns a `std::vector<int>`, so you store the result in a `std::vector<int>`. |

## 9. Explain

Answer in your own words, preferably in writing. Only then compare with the example answers.

1. Why can a function return a vector instead of an `int`?
2. What does the result type `std::vector<int>` mean?
3. Why does the input parameter have `const&`, while the result type has no `&`?
4. Why does the local result vector have no `const`, while the result received in `main` can have it?
5. What does `return selected;` do, and what happens to the result after the function ends?
6. Does the selecting function change the original vector?
7. Can the result be empty, and how do you recognise that?
8. Why is the order of the chosen elements kept?
9. Can a returned vector be passed to another function?
10. Why doesn't the selecting function print the elements?
11. Why doesn't the case `{30, 45}` reveal the bug in section 7?

<details>
<summary>Example answers</summary>

1. Because sometimes the answer is many values, for example all the temperatures below zero. One number can't store those values.
2. That the function returns a vector of `int`s, a whole collection.
3. The parameter refers to the caller's existing vector and only reads it, so it needs no copy. The result is a new collection the caller doesn't have yet, so the function passes it as a value.
4. The function adds elements to the local vector, so it has to change it. `main` gets a finished result and, if it doesn't intend to change it, marks it `const`.
5. It passes the new vector as the result to the place of the call. The local variable ends together with the function, but the caller already has its own result and can use it.
6. No. It gets it through `const&`, so it can only read it. The chosen values go into a separate vector.
7. Yes, when no element meets the condition or the input is empty. It's a correct result, and `empty()` gives `true` then.
8. Because the function goes through the input from the first element to the last, and `push_back` adds each chosen element at the end of the result.
9. Yes. It's an ordinary `std::vector<int>`, so it can be passed to a function taking `const std::vector<int>&`, like the summing function.
10. Because its task is choosing data. Printing is `main`'s task, as in lessons 5.5 and 6.4. That way the function can also be used where nothing needs printing.
11. Because it contains no length of 60, and only for that length does the wrong condition `value < highest` give a different result from the correct one.

</details>

## Summary

- A function can return a whole vector: `std::vector<int> keep_negative(const std::vector<int>& values)`.
- The typical layout: the input through `const&`, a local empty result vector, `push_back` for the chosen elements, and `return` of that vector.
- Returning happens **by value**: the caller gets its own result. The result type has no `&`.
- You receive the result in a variable, for example `const std::vector<int> selected{keep_negative(temperatures)};`.
- The original stays unchanged, and the chosen elements keep its order.
- An empty vector is a correct result. You recognise it with `empty()`.
- You can pass a returned vector on to another function, for example a summing one.

## What's next

The next lesson is the Module 6 test, which brings together storing data, loops, indices and functions on vectors: [Lesson 6.6: A training log (the Module 6 test)](lesson_06_training_log.en.md).

---

## Example solutions

Look here **after your own attempt**. Your names may differ, as long as the standard output is as required.

<details>
<summary>Section 6: the mission, checking the lengths of pieces</summary>

<!-- example: piece_lengths -->
```cpp
#include <iostream>
#include <vector>

std::vector<int> keep_in_range(const std::vector<int>& values, int lowest, int highest) {
    std::vector<int> selected{};

    for (const int value : values) {
        if (value >= lowest && value <= highest) {
            selected.push_back(value);
        }
    }

    return selected;
}

int total_length(const std::vector<int>& values) {
    int total{0};

    for (const int value : values) {
        total += value;
    }

    return total;
}

int main() {
    const std::vector<int> lengths{28, 30, 45, 65, 60, 29, 30};

    const std::vector<int> accepted{keep_in_range(lengths, 30, 60)};

    std::cout << "Original pieces: " << lengths.size() << "\n";
    std::cout << "Accepted pieces: " << accepted.size() << "\n";

    std::cout << "Accepted lengths:";
    if (accepted.empty()) {
        std::cout << " none";
    } else {
        for (const int length : accepted) {
            std::cout << " " << length;
        }
    }
    std::cout << "\n";

    std::cout << "Total accepted length: " << total_length(accepted) << "\n";
}
```

1. **The input parameter has `const&`**, because the function only reads the original and needs no copy of it.
2. **The result type has no `&`**: the function returns a new collection by value. The caller gets its own result.
3. **The local vector `selected` has no `const`**, because the function adds the accepted lengths to it.
4. **It can be returned**, because `return` passes its contents to the place of the call as the result, like a number in lesson 5.3.
5. **The received result `accepted` has `const`**, because `main` doesn't change it any more: it only prints it and passes it on.
6. **The flow:** `lengths` → `keep_in_range` (reads through `const&`, builds and returns a new vector) → `accepted` in `main` → `total_length` (reads through `const&`, returns an `int`) → the report.
7. **The original stays unchanged**, because both functions get it, or the result, through `const&` and only read.
8. **An empty result** means "no element meets the condition". The program then prints `none`, and `total_length` returns 0, because its loop makes no passes.

The bounds are parameters, so the same function will also select a different range. This is one possible split: for example, you can print the lengths in a separate `void` function, as long as the calculating functions print nothing.

**The check program** checks every case in the list of check cases. The functions are the same as above, and the part of `main` from `const std::vector<int> accepted{...}` on is the same, apart from the indentation. The lengths are read from the input with `push_back`, as in lesson 6.2, so the vector `lengths` has no `const`.

<!-- example: piece_lengths_check -->
```cpp
#include <iostream>
#include <vector>

std::vector<int> keep_in_range(const std::vector<int>& values, int lowest, int highest) {
    std::vector<int> selected{};

    for (const int value : values) {
        if (value >= lowest && value <= highest) {
            selected.push_back(value);
        }
    }

    return selected;
}

int total_length(const std::vector<int>& values) {
    int total{0};

    for (const int value : values) {
        total += value;
    }

    return total;
}

int main() {
    std::vector<int> lengths{};
    int piece_count{0};
    std::cin >> piece_count;

    for (int piece{1}; piece <= piece_count; ++piece) {
        int length{0};
        std::cin >> length;
        lengths.push_back(length);
    }

    if (std::cin.fail()) {
        std::cout << "Input could not be read\n";
    } else {
        const std::vector<int> accepted{keep_in_range(lengths, 30, 60)};

        std::cout << "Original pieces: " << lengths.size() << "\n";
        std::cout << "Accepted pieces: " << accepted.size() << "\n";

        std::cout << "Accepted lengths:";
        if (accepted.empty()) {
            std::cout << " none";
        } else {
            for (const int length : accepted) {
                std::cout << " " << length;
            }
        }
        std::cout << "\n";

        std::cout << "Total accepted length: " << total_length(accepted) << "\n";
    }
}
```

The input data is the number of pieces, followed by their lengths. The cases come in the order of the list of check cases, from A to M.

<!-- input: piece_lengths_check -->
```text
7
28
30
45
65
60
29
30
```

<!-- output: piece_lengths_check -->
```text
Original pieces: 7
Accepted pieces: 4
Accepted lengths: 30 45 60 30
Total accepted length: 165
```

<!-- input: piece_lengths_check -->
```text
0
```

<!-- output: piece_lengths_check -->
```text
Original pieces: 0
Accepted pieces: 0
Accepted lengths: none
Total accepted length: 0
```

<!-- input: piece_lengths_check -->
```text
3
10
29
61
```

<!-- output: piece_lengths_check -->
```text
Original pieces: 3
Accepted pieces: 0
Accepted lengths: none
Total accepted length: 0
```

<!-- input: piece_lengths_check -->
```text
3
30
45
60
```

<!-- output: piece_lengths_check -->
```text
Original pieces: 3
Accepted pieces: 3
Accepted lengths: 30 45 60
Total accepted length: 135
```

<!-- input: piece_lengths_check -->
```text
4
29
30
60
61
```

<!-- output: piece_lengths_check -->
```text
Original pieces: 4
Accepted pieces: 2
Accepted lengths: 30 60
Total accepted length: 90
```

<!-- input: piece_lengths_check -->
```text
1
30
```

<!-- output: piece_lengths_check -->
```text
Original pieces: 1
Accepted pieces: 1
Accepted lengths: 30
Total accepted length: 30
```

<!-- input: piece_lengths_check -->
```text
1
60
```

<!-- output: piece_lengths_check -->
```text
Original pieces: 1
Accepted pieces: 1
Accepted lengths: 60
Total accepted length: 60
```

<!-- input: piece_lengths_check -->
```text
1
45
```

<!-- output: piece_lengths_check -->
```text
Original pieces: 1
Accepted pieces: 1
Accepted lengths: 45
Total accepted length: 45
```

<!-- input: piece_lengths_check -->
```text
4
30
30
60
60
```

<!-- output: piece_lengths_check -->
```text
Original pieces: 4
Accepted pieces: 4
Accepted lengths: 30 30 60 60
Total accepted length: 180
```

<!-- input: piece_lengths_check -->
```text
4
60
30
45
30
```

<!-- output: piece_lengths_check -->
```text
Original pieces: 4
Accepted pieces: 4
Accepted lengths: 60 30 45 30
Total accepted length: 165
```

<!-- input: piece_lengths_check -->
```text
2
0
0
```

<!-- output: piece_lengths_check -->
```text
Original pieces: 2
Accepted pieces: 0
Accepted lengths: none
Total accepted length: 0
```

<!-- input: piece_lengths_check -->
```text
2
30
45
```

<!-- output: piece_lengths_check -->
```text
Original pieces: 2
Accepted pieces: 2
Accepted lengths: 30 45
Total accepted length: 75
```

<!-- input: piece_lengths_check -->
```text
2
30
60
```

<!-- output: piece_lengths_check -->
```text
Original pieces: 2
Accepted pieces: 2
Accepted lengths: 30 60
Total accepted length: 90
```

</details>

<details>
<summary>Section 7: the output before the fix, and the fixed program</summary>

Before the fix, for `{30, 45}`:

<!-- input: lengths_bound_bug -->
```text
2
30
45
```

<!-- output: lengths_bound_bug -->
```text
Original pieces: 2
Accepted pieces: 2
Accepted lengths: 30 45
Total accepted length: 75
```

For `{30, 60}`:

<!-- input: lengths_bound_bug -->
```text
2
30
60
```

<!-- output: lengths_bound_bug -->
```text
Original pieces: 2
Accepted pieces: 1
Accepted lengths: 30
Total accepted length: 30
```

- For `{30, 45}` the result is correct: no length equals 60, so the wrong condition has nothing to affect.
- For `{30, 60}` the length 60 is left out: 1 piece is accepted instead of 2, and the sum is 30 instead of 90.
- **The cause:** the condition `value < highest` accepts lengths from 30 to **less than** 60. The requirement is about an inclusive range.
- **The fix:** `value <= highest`. The lower bound was correct: `value >= lowest`.

The fixed program is the check program from section 6: it differs from the buggy program only in that comparison. For both data sets it gives the results from the list of check cases: cases L and M. Cases C, E, F and G also check the bounds.

</details>

**Previous lesson:** [Lesson 6.4: A vector as a function parameter: `const&`](lesson_04_a_vector_as_a_parameter.en.md) · **Next lesson:** [Lesson 6.6: A training log (the Module 6 test)](lesson_06_training_log.en.md) · [Course overview](../../README.en.md)

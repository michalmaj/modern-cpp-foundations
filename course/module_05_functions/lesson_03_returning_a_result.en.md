# Lesson 5.3: A function returns a result (`return`)

[Polski](lesson_03_returning_a_result.md) · **English** · [Course overview](../../README.en.md)

> **Module 5, lesson 3** · about 75–90 minutes
> **You need:** the `cpp-workspace` folder and the original `lesson_05_first_program` project, as before. You don't need the debugger in this lesson.
> **Pilot version.** The programs in this lesson are checked automatically on Windows, Ubuntu and macOS, including with the given input data. Typing input into CLion's **Run** window is described without a manual check on every system.

## Before you start

This lesson assumes that after lesson 5.2 you:

- define `void` functions with parameters and call them with arguments;
- know that a parameter receives the argument's value, and that the function works on that value of its own;
- remember that `/` on two `int` numbers gives a whole-number result (lessons 2.4 and 2.5);
- use `bool` values in `if` conditions (lesson 3.2).

## The situation

The functions in lessons 5.1 and 5.2 carried out an action, usually printing text. Whatever they worked out, they could only show on the screen. Often, though, the result of a calculation is needed **further on in the program**: for another calculation, a comparison, a report. In this lesson a function will **pass its result back** to the place of the call, and that place decides what to do with it.

After this lesson you will:

- point out a function's result type and its `return` statement;
- explain what happens after `return` runs;
- tell returning a result from printing it with `std::cout`;
- store a call's result in a variable and use it in expressions;
- explain the special ending rule of `int main()`;
- write functions that return `int`, `double` and `bool`;
- recognise integer division in a function that returns `double`;
- move a calculation into a function and keep the printing in `main`.

## 1. Prepare the project

In `cpp-workspace`, create a `lesson_5_3` folder and copy `main.cpp` and `CMakeLists.txt` into it from the original `lesson_05_first_program`. You type the programs from sections 2–9 into that folder's `main.cpp`.

## 2. A function prints, but gives no result back

This function converts minutes to seconds and prints the result:

<!-- example: print_seconds -->
```cpp
#include <iostream>

void print_seconds(int minutes) {
    std::cout << minutes * 60 << "\n";
}

int main() {
    print_seconds(3);
}
```

<!-- output: print_seconds -->
```text
180
```

This is a correct program. But a new requirement comes up: **add 30 seconds of preparation** to the number of seconds and print the sum. Someone tries this:

<!-- broken: void_as_value at=8:46 errors=1 error=^invalid operands to binary expression \('void' and 'int'\) -->
```cpp
#include <iostream>

void print_seconds(int minutes) {
    std::cout << minutes * 60 << "\n";
}

int main() {
    const int total_seconds{print_seconds(3) + 30};
    std::cout << "Total seconds: " << total_seconds << "\n";
}
```

**Predict** whether this program will build, and explain why. Then try to build it.

<details>
<summary>What the compiler reports, and why</summary>

The program won't build. The compiler reports `invalid operands to binary expression ('void' and 'int')` on line 8: on the left of `+` stands something of type `void`, on the right an `int`, and such values can't be added.

The function `print_seconds` worked out 180 and printed that number, but it **passed nothing back** to the place of the call. Its result type is `void`, so the call `print_seconds(3)` isn't a number that can be added to 30. Printing text on the screen is something different from passing a result on.

</details>

The function `print_seconds` isn't wrong. It does what it was written for: it prints. But the new requirement needs a function that **passes its result back** to the place of the call.

## 3. The first function that returns a result

Here is a function that works out the number of seconds and passes it on:

<!-- example: seconds_with_preparation -->
```cpp
#include <iostream>

int seconds_from_minutes(int minutes) {
    const int seconds{minutes * 60};
    return seconds;
}

int main() {
    const int total_seconds{seconds_from_minutes(3) + 30};

    std::cout << "Total seconds: " << total_seconds << "\n";
}
```

| Part | In the code | Meaning |
|---|---|---|
| **Result type** | `int` before the function's name | The function passes a result of type `int` back to the place of the call. |
| **Parameter** | `int minutes` | The data for the calculation, as in lesson 5.2. |
| **Local variable** | `const int seconds{minutes * 60};` | Holds the calculated result in the function. |
| **`return`** | `return seconds;` | Ends the function's run and passes the value of `seconds` back to the place of the call. |

The call `seconds_from_minutes(3)` now gives **a value of type `int`**. It can be used wherever an `int` number fits, for example in the expression `seconds_from_minutes(3) + 30`. `main` decides what to do with the result.

**Predict** what the program will print, and run it.

<details>
<summary>Standard output</summary>

<!-- output: seconds_with_preparation -->
```text
Total seconds: 210
```

The function prints nothing. The number 210 is printed by `std::cout` in `main`, after adding 30 to the returned result 180.

</details>

## 4. Where the result is made, and where it's printed

The program in section 3 runs like this:

| Step | Where the program is | What happens |
|---|---|---|
| 1 | `main` | Prepares the argument `3` and calls `seconds_from_minutes(3)`. |
| 2 | function | The parameter `minutes` receives the value 3. |
| 3 | function | The function works out `3 * 60`, that is 180, and stores it in `seconds`. |
| 4 | function | `return seconds;` ends the function and passes the result 180 back. |
| 5 | `main` | The program continues the calculation at the place of the call: `180 + 30`. |
| 6 | `main` | It stores 210 in the variable `total_seconds`. |
| 7 | `main` | Only then does `std::cout` print `Total seconds: 210`. |

**The calculation in the function and the printing of the result don't have to happen in the same place in the program.**

You can store the result in a variable, or use it straight away. In this program the function `seconds_from_minutes` is the same as in section 3:

<!-- example: seconds_two_ways -->
```cpp
#include <iostream>

int seconds_from_minutes(int minutes) {
    const int seconds{minutes * 60};
    return seconds;
}

int main() {
    std::cout << "Start\n";

    const int stored_seconds{seconds_from_minutes(2)};
    std::cout << stored_seconds << "\n";

    std::cout << seconds_from_minutes(2) << "\n";
    std::cout << "End\n";
}
```

**Predict** every line. For each call, also point out where the function ends and where `main` carries on.

<details>
<summary>Standard output and explanation</summary>

<!-- output: seconds_two_ways -->
```text
Start
120
120
End
```

- **The first call:** the function ends at `return seconds;`, and `main` stores the result 120 in `stored_seconds`. Only the next line prints it.
- **The second call** stands inside a `std::cout` statement. The function ends at `return`, and the printing is done by `std::cout` in `main`. The function didn't print anything, either time.
- `seconds` in the function and `stored_seconds` in `main` are two different variables, like the parameter and the argument in lesson 5.2.

</details>

**What does `return` do?** Running a `return` statement **ends the current call of the function** and passes the result back to the place of the call. If any statements stood after the `return` in the same function, they wouldn't run in that call any more. In this lesson, every function that returns a result has one `return`, at the end of its body. A `void` function passes back no ordinary result value, which is why its call can't be added or stored in an `int` variable.

## 5. Back to `int main()`

In lesson 5.1 we promised to explain the word `int` before `main`. Now that you know functions with a result type, it all fits together:

- `main` is a function too, and its result type is `int`.
- `main` has a special role: the program starts running from it. Its result doesn't go to another function of your program, but to whoever started the program. That's the **exit code** from lesson 1.3. In this course, a normal ending is 0.
- You can end `main` explicitly, as in lesson 1.3:

<!-- fragment -->
```cpp
int main() {
    std::cout << "Done\n";
    return 0;
}
```

**The special rule for `main`:** when `main` reaches its closing brace without a `return`, it works as if `return 0;` had run. That's why all the programs so far with `int main()` and no `return` were correct. You don't need to add `return 0;` to your programs.

**This rule must not be carried over to other functions.** An ordinary function with the result type `int` **doesn't get** the result 0 automatically when it reaches the end of its body. **Analyse this fragment; don't run it**:

<!-- fragment -->
```cpp
int seconds_from_minutes(int minutes) {
    const int seconds{minutes * 60};
}
```

The function promises an `int` result but doesn't pass one back: there's no `return`. The compiler usually only warns, so the program may build. But such a program has **undefined behaviour**: the result of the call isn't determined and can't be relied on, even if it looks right once. Every ordinary function whose result type isn't `void` must pass a result back with `return`.

## 6. Find the bug: the result printed twice

The requirement: the program converts 2 minutes to seconds and prints **exactly one** line: `Seconds: 120`.

<!-- example: double_print_bug -->
```cpp
#include <iostream>

int seconds_from_minutes(int minutes) {
    const int seconds{minutes * 60};
    std::cout << seconds << "\n";
    return seconds;
}

int main() {
    const int seconds{seconds_from_minutes(2)};
    std::cout << "Seconds: " << seconds << "\n";
}
```

1. Read the requirement.
2. **Predict** the standard output.
3. Run the program.
4. Point out both statements that print the number.
5. Decide what the function is responsible for, and what `main` is responsible for.
6. Fix the program.
7. Run it again.

The output before the fix, and the fixed program, are in [Example solutions](#example-solutions). Look there after your own attempt.

## 7. A result of type `double`

A function's result doesn't have to be an `int`:

<!-- example: average_of_two -->
```cpp
#include <iostream>

double average_of_two(double first, double second) {
    return (first + second) / 2.0;
}

int main() {
    const double average{average_of_two(2.0, 3.0)};
    std::cout << "Average: " << average << "\n";
}
```

- The parameters have the type `double`, and the function's result type is `double` too.
- `return` can pass back the value of an expression directly. It doesn't have to be stored in a variable first.
- The returned result goes into a `double` variable in `main`. `std::cout` prints it, separately.

**Predict** the result and run the program.

<details>
<summary>Standard output</summary>

<!-- output: average_of_two -->
```text
Average: 2.5
```

</details>

## 8. Find the bug: an average without its fractional part

The requirement: the function works out the average of two **whole** numbers and returns it as a `double`, with a fractional part if needed.

<!-- example: average_int_bug -->
```cpp
#include <iostream>

double average_of_two(int first, int second) {
    return (first + second) / 2;
}

int main() {
    std::cout << "Average of 2 and 4: " << average_of_two(2, 4) << "\n";
    std::cout << "Average of 3 and 4: " << average_of_two(3, 4) << "\n";
}
```

**Predict** both lines. What is the correct average of 2 and 4, and of 3 and 4? Which case will reveal the bug? Run the program, find the cause, and fix it with one change.

The output before the fix, and the fix, are in [Example solutions](#example-solutions).

## 9. A function answers a question: `bool`

A function can return the answer `true` or `false`. Such a function fits neatly into a condition:

<!-- example: even_check -->
```cpp
#include <iostream>

bool is_even(int number) {
    return number % 2 == 0;
}

int main() {
    for (int number{4}; number <= 7; ++number) {
        if (is_even(number)) {
            std::cout << number << " is even\n";
        } else {
            std::cout << number << " is odd\n";
        }
    }
}
```

`number % 2 == 0` is a condition you know from lesson 3.2. The function returns its value, and the `if` in `main` decides what to print. A name starting with `is_` hints that the function answers a yes-or-no question.

**Predict** the four lines and run the program.

<details>
<summary>Standard output</summary>

<!-- output: even_check -->
```text
4 is even
5 is odd
6 is even
7 is odd
```

</details>

## 10. Mission: a temperature change in degrees Fahrenheit

The program compares two temperatures. The user gives them in degrees Celsius, and the program converts both to degrees Fahrenheit and reports how much the temperature changed. The formula:

**F = C · 9 / 5 + 32**

In `double` calculations, use the constants `9.0`, `5.0` and `32.0`.

**Requirements:**

- The program prints `Enter two Celsius temperatures (-40 to 40):` and reads two `double` numbers: the first and the second temperature.
- If the read fails, it prints only `Input could not be read`.
- If both numbers were read but at least one is outside the range -40 to 40 inclusive, it prints only `Invalid temperature data`. That's the range set for this task, not a limit of the `double` type.
- For valid data it prints three lines: `First Fahrenheit: X`, `Second Fahrenheit: Y` and `Change Fahrenheit: Z`, where `Z` is the second temperature in degrees Fahrenheit minus the first. `Z` can be positive, negative or zero.
- The program doesn't ask again, and after an error it prints none of the three report lines.
- The conversion is done by **your own function**: it takes one temperature of type `double` and returns the temperature in degrees Fahrenheit as a `double`. The function prints nothing and reads nothing. You choose the names of the function and its parameter.
- Reading, checking the data, calling the function, working out the difference and the report belong to `main`.
- Don't use variables declared outside functions.

To check the read, `std::cin.fail()` is enough, as in lesson 5.2.

In `cpp-workspace`, create a `fahrenheit_change` folder, copy `CMakeLists.txt` into it from the original `lesson_05_first_program`, create an empty `main.cpp` and write the program on your own.

For the data `0` and `10` the standard output must be as follows:

<!-- input: fahrenheit_change -->
```text
0
10
```

<!-- output: fahrenheit_change -->
```text
Enter two Celsius temperatures (-40 to 40):
First Fahrenheit: 32
Second Fahrenheit: 50
Change Fahrenheit: 18
```

**Predict**, before you write the program: what will it print for the data `12.5` and `20`?

<!-- input: fahrenheit_change -->
```text
12.5
20
```

<details>
<summary>Standard output for 12.5 and 20</summary>

<!-- output: fahrenheit_change -->
```text
Enter two Celsius temperatures (-40 to 40):
First Fahrenheit: 54.5
Second Fahrenheit: 68
Change Fahrenheit: 13.5
```

</details>

**This isn't `seconds_from_minutes` with a different formula.** There, one result went into one simple calculation. Here the same function gives **two results** for two different inputs, and `main` uses both again, to work out the difference. You have to decide on your own:

1. how to name the function and its parameter, and how to write the formula in `return`;
2. where to keep both returned results, since you need them both in the report and in the difference;
3. in what order to subtract, so that the difference is "second minus first";
4. how to check the data before the program converts anything.

**Before you write the program**, prepare a table of test cases: both ends of the range, equal temperatures, a second temperature lower than the first, a temperature with a fractional part, values just outside the range, text instead of the first and instead of the second number, and data that ends after one number. For each case, write down the expected standard output. Choose temperatures whose results are easy to work out in your head.

Analyse the cases where the data ends early on paper, as in lessons 4.5–5.2, instead of running them, and compare with the collapsed list of check cases. This lesson's program is checked separately for such data, by the course's automatic tests.

### Success criteria

- The program builds as C++20, and its standard output for the data `0`, `10` and `12.5`, `20` is exactly as shown above.
- For every case you can type, the standard output matches the list of check cases. You check the cases where the data ends early by reasoning.
- The conversion is done by your function, which takes a `double`, returns a `double`, and neither prints nor reads anything. The formula appears in the code only in it.
- Each temperature appears in the report once. The difference is worked out from the results returned by the function.
- After a failed read or out-of-range data, no report line appears.
- The program doesn't use variables declared outside functions.
- The table of cases was made before running the program.
- You can point out the result type and the `return` in your function, and explain where each result is made and where it's printed.

When the result matches, you can save the project in Git, as in lesson 1.5.

<details>
<summary>Hint 1</summary>

Which part of the program always does the same calculation, whether you're converting the first or the second temperature?

</details>

<details>
<summary>Hint 2</summary>

How can `main` also use the function's result later, when working out the difference?

</details>

<details>
<summary>Hint 3</summary>

Split the jobs: the function returns the converted temperature, and `main` keeps both results, subtracts the first from the second, and prints the report.

</details>

<details>
<summary>The full list of check cases: open it after preparing your own table</summary>

| Data | Standard output after the question | What it checks |
|---|---|---|
| `0`, `10` | 32, 50, change 18 | the example in the text |
| `12.5`, `20` | 54.5, 68, change 13.5 | a fractional part |
| `-40`, `0` | -40, 32, change 72 | the lower limit |
| `20`, `20` | 68, 68, change 0 | equal temperatures |
| `40`, `-40` | 104, -40, change -144 | the upper limit, a drop |
| `25`, `0` | 77, 32, change -45 | the temperature drops |
| `-41`, `0` | `Invalid temperature data` | the first just below the range |
| `0`, `41` | `Invalid temperature data` | the second just above the range |
| `abc`, `10` | `Input could not be read` | text instead of the first number |
| `10`, `abc` | `Input could not be read` | text instead of the second number |
| `10`, then the end of the data | `Input could not be read` | the data ends after one number |
| no data | `Input could not be read` | the data ends at once |

The first two cases are checked above, with the mission's text.

<!-- input: fahrenheit_change -->
```text
-40
0
```

<!-- output: fahrenheit_change -->
```text
Enter two Celsius temperatures (-40 to 40):
First Fahrenheit: -40
Second Fahrenheit: 32
Change Fahrenheit: 72
```

<!-- input: fahrenheit_change -->
```text
20
20
```

<!-- output: fahrenheit_change -->
```text
Enter two Celsius temperatures (-40 to 40):
First Fahrenheit: 68
Second Fahrenheit: 68
Change Fahrenheit: 0
```

<!-- input: fahrenheit_change -->
```text
40
-40
```

<!-- output: fahrenheit_change -->
```text
Enter two Celsius temperatures (-40 to 40):
First Fahrenheit: 104
Second Fahrenheit: -40
Change Fahrenheit: -144
```

<!-- input: fahrenheit_change -->
```text
25
0
```

<!-- output: fahrenheit_change -->
```text
Enter two Celsius temperatures (-40 to 40):
First Fahrenheit: 77
Second Fahrenheit: 32
Change Fahrenheit: -45
```

<!-- input: fahrenheit_change -->
```text
-41
0
```

<!-- output: fahrenheit_change -->
```text
Enter two Celsius temperatures (-40 to 40):
Invalid temperature data
```

<!-- input: fahrenheit_change -->
```text
0
41
```

<!-- output: fahrenheit_change -->
```text
Enter two Celsius temperatures (-40 to 40):
Invalid temperature data
```

<!-- input: fahrenheit_change -->
```text
abc
10
```

<!-- output: fahrenheit_change -->
```text
Enter two Celsius temperatures (-40 to 40):
Input could not be read
```

<!-- input: fahrenheit_change -->
```text
10
abc
```

<!-- output: fahrenheit_change -->
```text
Enter two Celsius temperatures (-40 to 40):
Input could not be read
```

<!-- input: fahrenheit_change -->
```text
10
```

<!-- output: fahrenheit_change -->
```text
Enter two Celsius temperatures (-40 to 40):
Input could not be read
```

<!-- input: fahrenheit_change -->
```text
```

<!-- output: fahrenheit_change -->
```text
Enter two Celsius temperatures (-40 to 40):
Input could not be read
```

The temperatures in these tests were chosen so that the `double` calculations give exact, short results. Not every conversion prints this simply, but these tests check the program's logic, not rounding.

</details>

An example solution is in [Example solutions](#example-solutions).

## 11. When something goes differently

| What you see | What it means | What to do |
|---|---|---|
| `invalid operands to binary expression ('void' and …)`, or another error with `void` at a call | A `void` function's result is being used like a number (section 2). | If the result is needed later, the function must have a result type and a `return`. |
| A warning that a function doesn't return a value | A function whose result type isn't `void` is missing its `return`. | Add a `return` with the result. Don't rely on such a program, even if it built (section 5). |
| The same number appears twice | Both the function and `main` print it (section 6). | A calculating function only returns the result. `main` prints it. |
| The average has no fractional part | The division happens on `int` numbers before the result reaches `return` (section 8). | Divide by `2.0`, or work with `double` numbers. |
| The temperature change has the wrong sign | The subtraction is in the reverse order. | The change is the second temperature minus the first. |
| A converted temperature is wrong | The formula is written differently from `C · 9 / 5 + 32`. | Check the formula for 0 (result 32) and 100 (result 212). |
| Part of the report appears after bad data | The report stands before the data check, or outside the branch for valid data. | First check the read and the range, and print the report only for valid data. |
| The program does nothing and waits | It's waiting for another number, as in lesson 2.6. | Type a number and press **Enter**. Don't check a case where the data runs out this way: trace it on paper. |

## 12. Explain

Answer in your own words, preferably in writing. Only then compare with the example answers.

1. What does the type `int` before a function's name mean?
2. What is a returned value?
3. What does `return` do?
4. Why doesn't `std::cout` replace `return`?
5. Can a function return a result without printing anything?
6. Can a call's result be assigned to a variable?
7. Can a function's result be used in a calculation?
8. Why does `main` have a special rule of a default result of 0?
9. Does an ordinary `int` function automatically get the result 0 when it reaches its closing brace?
10. Why doesn't the result type `double` fix an earlier integer division?
11. Can a function return a `bool`?
12. Why doesn't the temperature-converting function need to print any messages?
13. What is `main` responsible for in the mission?
14. Why is it worth testing equal temperatures and a case where the second is lower than the first?

<details>
<summary>Example answers</summary>

1. That the function passes a result of type `int` back to the place of the call.
2. It's the value that the function passes back to the place of the call with `return`. The function call becomes that value.
3. It ends the current call of the function and passes the result back to the place of the call.
4. Because `std::cout` only prints text on the screen. The place of the call then gets no value it could use further.
5. Yes. That's how `seconds_from_minutes` works: it returns the result, and only `main` prints it, if it wants to.
6. Yes, for example `const int stored_seconds{seconds_from_minutes(2)};`.
7. Yes, for example `seconds_from_minutes(3) + 30`.
8. Because `main` is a special function where the program starts. C++ says that reaching the end of `main` without `return` works like `return 0;`, that is, a normal end of the program.
9. No. That rule applies only to `main`. An ordinary function with an `int` result must pass the result back with `return`. Without it, the program has undefined behaviour.
10. Because the division `(first + second) / 2` on `int` numbers gives a whole-number result before `return` passes the value back. Turning it into a `double` when it's returned doesn't bring back the lost fractional part.
11. Yes, for example `is_even`. The returned `true` or `false` can be used straight away in an `if`.
12. Because its job is the calculation. `main` decides what to do with the result: here it prints it in the report and also uses it for the difference.
13. Reading and checking the data, calling the function for both temperatures, keeping the results, working out the difference, and printing the report.
14. Because equal temperatures give a change of 0, and a lower second temperature gives a negative change. These cases reveal a reversed subtraction, which you don't see when the temperature rises and you don't check the sign.

</details>

## Summary

- The **result type** before a function's name, for example `int`, `double` or `bool`, says what result the function passes back to the place of the call. `void` means: no ordinary result.
- **`return` value;** ends the function's call and passes the result back. The function call becomes that value.
- A call's result can be stored in a variable, used in an expression or used in a condition.
- **`return` isn't `std::cout`.** `return` passes a result back to the program, and `std::cout` prints text on the screen. A calculating function returns; the place of the call decides about printing.
- `main` has the result type `int`. Its result is the program's exit code. Only in `main` does reaching the closing brace work like `return 0;`.
- An ordinary function whose result type isn't `void` must always pass a result back with `return`.
- Dividing two `int` numbers gives a whole-number result, even if the function returns a `double`.
- A function that returns `bool` answers a question and fits well into an `if` condition.

## What's next

The functions in this lesson always work out their result with the same formula. In the next lesson a function will make a decision and pass back different results depending on the data: [Lesson 5.4: Several ways to `return`](lesson_04_several_returns.en.md).

---

## Example solutions

Look here **after your own attempt**. Your names may differ, as long as the standard output is as required.

<details>
<summary>Section 6: the output before the fix, and the fixed program</summary>

Before the fix:

<!-- output: double_print_bug -->
```text
120
Seconds: 120
```

- The number 120 appears **twice**: once printed by the function, once by `main`. The requirement says one line.
- **Responsibilities:** the function works out and returns the number of seconds. `main` decides how to show the result.
- **The fix:** remove the printing from the function.

<!-- example: double_print_fixed -->
```cpp
#include <iostream>

int seconds_from_minutes(int minutes) {
    const int seconds{minutes * 60};
    return seconds;
}

int main() {
    const int seconds{seconds_from_minutes(2)};
    std::cout << "Seconds: " << seconds << "\n";
}
```

<!-- output: double_print_fixed -->
```text
Seconds: 120
```

A function that both prints and returns its result is valid C++. In this task, though, it doesn't meet the requirement, and it needlessly mixes two responsibilities: the calculation and the presentation of the result.

</details>

<details>
<summary>Section 8: the output before the fix, and the fix</summary>

Before the fix:

<!-- output: average_int_bug -->
```text
Average of 2 and 4: 3
Average of 3 and 4: 3
```

- **For 2 and 4** the result is correct, because 6 / 2 is exactly 3. This case hides the bug.
- **For 3 and 4** the correct average is 3.5, but the program prints 3.
- **The cause:** `first + second` and `2` are `int`s, so `7 / 2` gives 3, as in lesson 2.4. Only that whole-number result reaches `return` and becomes a `double`. The function's result type doesn't change the earlier division.
- **The fix:** divide by `2.0`, as in lesson 2.5. Then the division happens on `double` numbers.

<!-- example: average_int_fixed -->
```cpp
#include <iostream>

double average_of_two(int first, int second) {
    return (first + second) / 2.0;
}

int main() {
    std::cout << "Average of 2 and 4: " << average_of_two(2, 4) << "\n";
    std::cout << "Average of 3 and 4: " << average_of_two(3, 4) << "\n";
}
```

<!-- output: average_int_fixed -->
```text
Average of 2 and 4: 3
Average of 3 and 4: 3.5
```

</details>

<details>
<summary>Section 10: the mission, a temperature change</summary>

<!-- example: fahrenheit_change -->
```cpp
#include <iostream>

double fahrenheit_from_celsius(double celsius) {
    return celsius * 9.0 / 5.0 + 32.0;
}

int main() {
    double first_celsius{0.0};
    double second_celsius{0.0};

    std::cout << "Enter two Celsius temperatures (-40 to 40):\n";
    std::cin >> first_celsius;
    std::cin >> second_celsius;

    if (std::cin.fail()) {
        std::cout << "Input could not be read\n";
    } else {
        const bool first_valid{first_celsius >= -40.0 && first_celsius <= 40.0};
        const bool second_valid{second_celsius >= -40.0 && second_celsius <= 40.0};

        if (first_valid && second_valid) {
            const double first_fahrenheit{fahrenheit_from_celsius(first_celsius)};
            const double second_fahrenheit{fahrenheit_from_celsius(second_celsius)};

            std::cout << "First Fahrenheit: " << first_fahrenheit << "\n";
            std::cout << "Second Fahrenheit: " << second_fahrenheit << "\n";
            std::cout << "Change Fahrenheit: " << second_fahrenheit - first_fahrenheit << "\n";
        } else {
            std::cout << "Invalid temperature data\n";
        }
    }
}
```

- **The function** `fahrenheit_from_celsius` only calculates: it takes a `double` and returns a `double` with one `return` holding the formula. It neither prints nor reads anything.
- **`main`** calls the function twice, with different arguments. It stores both results in `const double` variables, because it uses each one twice: in the report and in the difference. The formula isn't repeated in `main`.
- **The difference** is `second_fahrenheit - first_fahrenheit`, that is, second minus first. For `40`, `-40` it's -144; for `20`, `20` it's 0.
- **The order of operations:** `celsius * 9.0 / 5.0 + 32.0` multiplies, divides, and only then adds 32, as in the formula. The constants `9.0` and `5.0` make the whole calculation happen on `double` numbers.
- **The data:** one `std::cin.fail()` check after both reads is enough, as in lesson 5.2. The range check stands in the branch for a successful read, and the report only in the branch for valid data.

</details>

**Previous lesson:** [Lesson 5.2: Parameters, arguments and passing by value](lesson_02_parameters_and_arguments.en.md) · **Next lesson:** [Lesson 5.4: Several ways to `return`](lesson_04_several_returns.en.md) · [Course overview](../../README.en.md)

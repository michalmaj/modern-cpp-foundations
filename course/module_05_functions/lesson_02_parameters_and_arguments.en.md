# Lesson 5.2: Parameters, arguments and passing by value

[Polski](lesson_02_parameters_and_arguments.md) · **English** · [Course overview](../../README.en.md)

> **Module 5, lesson 2** · about 70–85 minutes
> **You need:** the `cpp-workspace` folder and the original `lesson_05_first_program` project, as before. You don't need the debugger in this lesson.
> **Pilot version.** The programs in this lesson are checked automatically on Windows, Ubuntu and macOS, including with the given input data. Typing input into CLion's **Run** window is described without a manual check on every system.

## Before you start

This lesson assumes that after lesson 5.1 you:

- define a `void` function with no parameters before `main` and call it from `main`;
- know that a function's body runs only when it's called, and that the program then comes back to just after the call;
- write `for` loops with a counter and `++` (lesson 4.3);
- know that a variable exists only in the block where it was declared (lessons 3.2 and 4.3).

## The situation

The `show_workshop_rules` function from lesson 5.1 always does exactly the same thing. That was enough, because the workshop rules didn't change. Often, though, you need a **similar** job for **different data**: lines of different lengths, bars of different heights. In this lesson a function gets data from the place where it's called.

After this lesson you will:

- explain why a function needs a parameter;
- point out a parameter in a definition and an argument in a call;
- call a function with a literal, a variable and an expression;
- define a function with two parameters and choose the order of the arguments;
- explain what passing by value means, and predict whether changing a parameter changes a variable in `main`;
- recognise a parameter scope error and swapped arguments;
- write a function whose arguments control what it prints.

## 1. Prepare the project

In `cpp-workspace`, create a `lesson_5_2` folder and copy `main.cpp` and `CMakeLists.txt` into it from the original `lesson_05_first_program`. You type the programs from sections 3–10 into that folder's `main.cpp`.

## 2. A function that needs information

The program has to print lines of dashes: three `-` characters one time, five another time. With the tools you know, that gives two separate functions:

<!-- fragment -->
```cpp
void print_three_dashes() {
    std::cout << "---\n";
}

void print_five_dashes() {
    std::cout << "-----\n";
}
```

And what if you needed a line of four, seven or twenty characters? Every length means a new function, almost identical to the others. They differ in only **one piece of information**: the number of characters.

**Think about it:** where could the function find out how long a line to print?

<details>
<summary>Discussion</summary>

Only the place of the call knows that: one time it needs three characters, another time five. So the function needs a way to **receive** the number of characters from whoever calls it, at every call. Then one function is enough for every length.

</details>

## 3. The first parameter

Here is one function for a line of any length:

<!-- example: line_lengths -->
```cpp
#include <iostream>

void print_line(int length) {
    for (int position{0}; position < length; ++position) {
        std::cout << "-";
    }

    std::cout << "\n";
}

int main() {
    print_line(3);
    print_line(5);
}
```

- `print_line` is the function's name, and `void` means, as in lesson 5.1, that the function doesn't pass a result back to the place of the call.
- **`int length`** in the parentheses is a **parameter**: a variable of the function that **receives a value** at every call. `int` is its type, and `length` is the name you use in the function's body.
- The function's body uses the value of `length`: the `for` loop prints as many dashes as `length` says, then ends the line.
- **`print_line(3);`** calls the function and passes it the value 3. In this call `length` has the value 3. In the call `print_line(5);` it has the value 5.

**Predict** what the program will print. Write your answer down, then run it.

<details>
<summary>Standard output</summary>

<!-- output: line_lengths -->
```text
---
-----
```

The program has **one** function definition. Only the data passed in each call changes.

</details>

## 4. Parameter and argument

Put the definition next to the call:

| | In the code | What it is |
|---|---|---|
| **Parameter** | `int length` in the definition `void print_line(int length)` | A named variable of the function. It receives a value at every call. |
| **Argument** | `5` in the call `print_line(5);` | An expression given at the call. The parameter receives its value. |

An argument doesn't have to be a number typed in directly. It can be a variable, or a whole expression:

<!-- fragment -->
```cpp
const int separator_length{4};
print_line(separator_length);
print_line(separator_length + 2);
```

In the first call the argument is `separator_length`, so `length` receives the value 4. In the second the argument is the expression `separator_length + 2`, so `length` receives 6. A parameter and an argument aren't two names for the same variable: the parameter `length` belongs to the function, and `separator_length` belongs to `main`.

You already know calls with arguments from standard library functions, for example `std::getline(std::cin, line)`. Now you're writing your own function that takes data. Library functions don't always receive their data the way our `int` parameter does. We'll come back to that in later modules.

## 5. Predict: several calls of one function

The `print_line` function is the same as in section 3. Only `main` changes:

<!-- example: line_calls -->
```cpp
#include <iostream>

void print_line(int length) {
    for (int position{0}; position < length; ++position) {
        std::cout << "-";
    }

    std::cout << "\n";
}

int main() {
    const int separator_length{4};

    std::cout << "Literal 3:\n";
    print_line(3);
    std::cout << "Variable:\n";
    print_line(separator_length);
    std::cout << "Expression:\n";
    print_line(separator_length + 2);
    std::cout << "Zero:\n";
    print_line(0);
    std::cout << "Done\n";
}
```

**Predict**, before you run the program:

1. How many times will `print_line` be called?
2. How many iterations will the `for` loop do in each call?
3. How many dashes will each line have?
4. What will be printed for a length of zero?

<details>
<summary>Standard output and explanation</summary>

<!-- output: line_calls -->
```text
Literal 3:
---
Variable:
----
Expression:
------
Zero:

Done
```

- The function is called 4 times, with the values 3, 4, 6 and 0. The loop does 3, 4, 6 and 0 iterations.
- **For zero**, the first check of the condition, `0 < 0`, gives `false`, so the loop prints no dash. But the statement `std::cout << "\n";` stands **after** the loop, so it always runs. That's why there's an **empty line** between `Zero:` and `Done`: a line with no characters, but with its line ending.

</details>

## 6. Passing by value

In this function the parameter **changes** in the body:

<!-- example: pass_by_value -->
```cpp
#include <iostream>

void count_down(int remaining) {
    while (remaining > 0) {
        std::cout << remaining << "\n";
        remaining = remaining - 1;
    }
}

int main() {
    int laps{3};

    count_down(laps);

    std::cout << "Caller value: " << laps << "\n";
}
```

**Predict**: what will the function print, and what value of `laps` will `main` print after coming back from the function?

<details>
<summary>Standard output</summary>

<!-- output: pass_by_value -->
```text
3
2
1
Caller value: 3
```

</details>

What happens here:

- The call `count_down(laps)` passes the **value** of the variable `laps`, that is 3, to the function.
- The parameter `remaining` receives **its own** value 3. It's a variable of the function, not another name for the variable `laps`.
- In the function's body `remaining` goes down to 0. That changes only `remaining`.
- After coming back to `main`, the variable `laps` still has the value 3.

This is **passing by value**: **the function works on its own value of the parameter, received from the argument.** That's how the parameters you meet in this lesson work, for example `int length` and `int remaining`. C++ also has other ways of passing data to a function. You'll meet them later in the course.

**Check.** In `main`, rename `laps` to `remaining`, in three places, so that the variable in `main` has the same name as the parameter. The function doesn't change:

<!-- example: pass_by_value_same_name -->
```cpp
#include <iostream>

void count_down(int remaining) {
    while (remaining > 0) {
        std::cout << remaining << "\n";
        remaining = remaining - 1;
    }
}

int main() {
    int remaining{3};

    count_down(remaining);

    std::cout << "Caller value: " << remaining << "\n";
}
```

**Predict** whether the result will be different, then run the program.

<details>
<summary>Standard output and explanation</summary>

<!-- output: pass_by_value_same_name -->
```text
3
2
1
Caller value: 3
```

The result is the same. These are still **two different variables**: one belongs to `main`, the other, the parameter, to the function `count_down`. Having the same name doesn't connect them. The parameter only receives the argument's value.

</details>

## 7. A table of changing values

This is how the values change in the program from section 6, in the version with `laps`:

| Moment | `laps` in `main` | `remaining` in `count_down` | Printed |
|---|---|---|---|
| before the call | 3 | doesn't exist | |
| the function starts | 3 | 3 | |
| after the first iteration | 3 | 2 | `3` |
| after the second iteration | 3 | 1 | `2` |
| after the third iteration | 3 | 0 | `1` |
| checking `remaining > 0` | 3 | 0, the condition is `false` | |
| back in `main` | 3 | doesn't exist | `Caller value: 3` |

**Answer:** why doesn't the variable `laps` become zero?

<details>
<summary>Answer</summary>

Because the function never changes `laps`. At the call, the parameter `remaining` received the value of `laps`, that is 3, and from then on it's a separate variable of the function. The statement `remaining = remaining - 1;` changes only `remaining`. When the function ends, its parameter stops existing, and `laps` is left unchanged in `main`. A `void` function also doesn't pass anything back to `main`.

</details>

## 8. Two parameters

A function can have several parameters. They're separated by commas:

<!-- example: pair_order -->
```cpp
#include <iostream>

void show_pair(int first, int second) {
    std::cout << "First: " << first << "\n";
    std::cout << "Second: " << second << "\n";
}

int main() {
    show_pair(2, 5);
    show_pair(5, 2);

    const int low{1};
    const int high{9};
    show_pair(high, low);
}
```

- The function `show_pair` has two parameters: `first` and `second`.
- Every call gives **two arguments**, also separated by a comma.
- **The first argument goes to the first parameter, and the second to the second.** The order decides, not the names of the variables in `main`.

**Predict** all six lines. Pay attention to the last call: which value will go to `first`?

<details>
<summary>Standard output and explanation</summary>

<!-- output: pair_order -->
```text
First: 2
Second: 5
First: 5
Second: 2
First: 9
Second: 1
```

In the last call the first argument is `high`, so `first` receives 9 and `second` receives 1. The names `low` and `high` don't matter here: only the argument's position in the parentheses counts.

</details>

## 9. Find the bug: swapped arguments

The requirement: the program reads two whole numbers and prints **the first one read** as `First` and **the second** as `Second`. We assume the user types two whole numbers.

<!-- example: pair_bug -->
```cpp
#include <iostream>

void show_pair(int first, int second) {
    std::cout << "First: " << first << "\n";
    std::cout << "Second: " << second << "\n";
}

int main() {
    int first_value{0};
    int second_value{0};

    std::cout << "Enter two values:\n";
    std::cin >> first_value;
    std::cin >> second_value;

    show_pair(second_value, first_value);
}
```

The program builds with no errors and no warnings. Check it for two cases:

| Case | Data |
|---|---|
| A | `3`, `3` |
| B | `2`, `5` |

1. Read the requirement and write down the correct standard output for both cases.
2. **Predict** what **this** program will print.
3. Run it for both cases.
4. Find the case that reveals the bug, and where the bug is in the code.
5. Fix the program.
6. Check both cases again.

The results before the fix, the explanation and the fixed program are in [Example solutions](#example-solutions). Look there after your own attempt.

## 10. Where does a parameter exist?

A parameter, like a variable declared in a block (lessons 3.2 and 4.3), exists only **in its function**. After calling the function, this program tries to print `length` in `main`:

<!-- broken: param_scope at=13:32 error=^use of undeclared identifier 'length' -->
```cpp
#include <iostream>

void print_line(int length) {
    for (int position{0}; position < length; ++position) {
        std::cout << "-";
    }

    std::cout << "\n";
}

int main() {
    print_line(4);
    std::cout << "Length: " << length << "\n";
}
```

**Predict** whether this program will build. Then try to build it and read the compiler's message.

<details>
<summary>What the compiler reports, and why</summary>

The program won't build. The compiler reports `use of undeclared identifier 'length'` on line 13. `length` is a parameter of the function `print_line`, so it exists only in that function's body. There's no variable with that name in `main`. The call `print_line(4)` passes the value 4 to the function, but it doesn't create a variable `length` in `main`.

The compiler adds the hint `did you mean '__NSConstantString_tag::length'?` to this message, and reports a second error on the same line. `__NSConstantString_tag` is a name built into the compiler, unrelated to your program: the compiler looked for a similar name and came across this one. Compiler hints can miss the point. The first part of the message is what counts: in `main` the name `length` is unknown.

</details>

**The fix:** if `main` needs the same value, it keeps it in a variable of **its own** and passes it as the argument. The fixed program is in [Example solutions](#example-solutions). Don't move the variable outside the functions so that it's visible everywhere: each function has its own variables, and data is passed through arguments.

## 11. Mission: an activity chart

The program draws a text chart of activity over three days. The user gives how many blocks of activity there were on each day. The program prints one bar of `#` characters for each day.

**Requirements:**

- The program prints `Enter blocks for days 1, 2 and 3:` and reads three whole numbers, for days 1, 2 and 3 in that order.
- If not all three numbers could be read, the program prints only `Input could not be read` and doesn't draw the chart.
- If three numbers were read but at least one is outside the range 0 to 6, the program prints only `Invalid bar data` and doesn't draw the chart.
- For valid data the program prints exactly three lines, for days 1, 2 and 3, in the format `Day N: [` + as many `#` characters as there are blocks + `]`. For zero blocks the bar is `[]`.
- The program doesn't ask again.
- One bar is printed by **your own `void` function with two `int` parameters**: the day number and the number of blocks. You choose the parameters' names and their order in the definition yourself, but in every call the arguments must go to the right parameters.
- `main` reads the data, checks it and decides on the calls. The function is responsible only for printing one bar.
- Don't use variables declared outside functions.

To check whether the read succeeded, the `std::cin.fail()` from lesson 4.5 is enough. You don't need to recover the input or check what else is on the line after the number.

In `cpp-workspace`, create an `activity_chart` folder, copy `CMakeLists.txt` into it from the original `lesson_05_first_program`, create an empty `main.cpp` and write the program on your own.

For the data `2`, `0`, `4` the standard output must be as follows:

<!-- input: activity_chart -->
```text
2
0
4
```

<!-- output: activity_chart -->
```text
Enter blocks for days 1, 2 and 3:
Day 1: [##]
Day 2: []
Day 3: [####]
```

**This isn't `print_line` or `show_pair` with new names.** `print_line` had one parameter and always the same character, and `show_pair` only printed two values. Here the function gets **two values with different roles**: one is printed as a number, the other controls a loop. It also has to put one line together from several parts. You have to decide on your own:

1. what parameters the function has, and in what order;
2. how the function builds one line, also for zero blocks;
3. how `main` checks the data before drawing anything;
4. what arguments the function gets in each of the three calls.

**Before you write the program**, prepare a table of test cases: all zeros, the upper limit 6, a few different values, a negative value, a value above 6, text instead of a number, and data that ends after two numbers. For each case, write down the expected standard output. For the data `2`, `0`, `4`, also write down what arguments the function gets in each call.

Analyse the case where the data ends early on paper, as in lessons 4.5–4.7, instead of running it: assume the input ends after its last line, trace the program, and compare your answer with the collapsed list of check cases. This lesson's program is checked separately for such data, by the course's automatic tests.

### Success criteria

- The program builds as C++20, and its standard output for the data `2`, `0`, `4` is exactly as shown above.
- For every case you can type, the standard output matches the list of check cases. You check the case with data ending after two numbers by reasoning: traced, the program prints the same lines as the list of check cases.
- The bar is printed by your `void` function with two `int` parameters, defined before `main`. The `#` character appears in the code only in that function.
- For zero blocks the bar is `[]`.
- After a failed read or out-of-range data, no bar appears.
- The program doesn't use variables declared outside functions.
- The table of cases was made before running the program.
- You can point out the parameters and the arguments in your program, and explain which argument goes to which parameter.

When the result matches, you can save the project in Git, as in lesson 1.5.

<details>
<summary>Hint 1</summary>

What two pieces of information does the function need to print one correct bar?

</details>

<details>
<summary>Hint 2</summary>

The day number and the number of `#` characters have different jobs. Think about where to use each value.

</details>

<details>
<summary>Hint 3</summary>

The function can print the start of the line, then repeat the `#` character in a loop, and finally close the bracket.

</details>

<details>
<summary>The full list of check cases: open it after preparing your own table</summary>

| Data | Standard output after the question | What it checks |
|---|---|---|
| `2`, `0`, `4` | `Day 1: [##]`, `Day 2: []`, `Day 3: [####]` | different values, including zero |
| `0`, `0`, `0` | an empty bar `[]` three times | all zeros |
| `6`, `6`, `6` | three bars of six `#` | the upper limit |
| `1`, `4`, `0` | `[#]`, `[####]`, `[]` | the day number isn't confused with the length |
| `5`, `1`, `3` | `[#####]`, `[#]`, `[###]` | another uneven set |
| `-1`, `2`, `3` | `Invalid bar data` | a negative value |
| `2`, `7`, `1` | `Invalid bar data` | a value above the range |
| `abc`, `1`, `2` | `Input could not be read` | text instead of a number |
| `1`, `2`, then the end of the data | `Input could not be read` | the data ends before the third number |

The case `2`, `0`, `4` is checked above, with the mission's text.

<!-- input: activity_chart -->
```text
0
0
0
```

<!-- output: activity_chart -->
```text
Enter blocks for days 1, 2 and 3:
Day 1: []
Day 2: []
Day 3: []
```

<!-- input: activity_chart -->
```text
6
6
6
```

<!-- output: activity_chart -->
```text
Enter blocks for days 1, 2 and 3:
Day 1: [######]
Day 2: [######]
Day 3: [######]
```

<!-- input: activity_chart -->
```text
1
4
0
```

<!-- output: activity_chart -->
```text
Enter blocks for days 1, 2 and 3:
Day 1: [#]
Day 2: [####]
Day 3: []
```

<!-- input: activity_chart -->
```text
5
1
3
```

<!-- output: activity_chart -->
```text
Enter blocks for days 1, 2 and 3:
Day 1: [#####]
Day 2: [#]
Day 3: [###]
```

<!-- input: activity_chart -->
```text
-1
2
3
```

<!-- output: activity_chart -->
```text
Enter blocks for days 1, 2 and 3:
Invalid bar data
```

<!-- input: activity_chart -->
```text
2
7
1
```

<!-- output: activity_chart -->
```text
Enter blocks for days 1, 2 and 3:
Invalid bar data
```

<!-- input: activity_chart -->
```text
abc
1
2
```

<!-- output: activity_chart -->
```text
Enter blocks for days 1, 2 and 3:
Input could not be read
```

<!-- input: activity_chart -->
```text
1
2
```

<!-- output: activity_chart -->
```text
Enter blocks for days 1, 2 and 3:
Input could not be read
```

</details>

An example solution is in [Example solutions](#example-solutions).

## 12. When something goes differently

| What you see | What it means | What to do |
|---|---|---|
| `use of undeclared identifier` with a parameter's name | The parameter was used outside its function, for example in `main` (section 10). | In `main`, use a variable of its own and pass it as the argument. |
| A compile error at a call: the compiler finds no matching function | The number of arguments doesn't match the number of parameters. | Count the parameters in the definition and the arguments in the call. |
| The bars are as long as the day numbers, and the day numbers look odd | The arguments in the call are in a different order from the parameters in the definition. | Compare the order of parameters and arguments, position by position. |
| For zero blocks `[]` is missing, or the line isn't ended | The closing bracket or the line ending is inside the loop, or skipped. | Print the start and the end of the line outside the loop. Only `#` goes in the loop. |
| A bar has one `#` too many or too few | The loop counter starts from a different value than the condition assumes. | Check a bar of 1 block in a trace table. |
| The chart appears despite bad data | The function is called before the data is checked. | First check the read and the range; call the function only for valid data. |
| A variable in `main` "doesn't change", although the function changes its parameter | That's how passing by value works (section 6). | It's not a bug. The function works on its own value of the parameter. |
| The program does nothing and waits | It's waiting for another number, as in lesson 2.6. | Type a number and press **Enter**. Don't check a case where the data runs out this way: trace it on paper. |

## 13. Explain

Answer in your own words, preferably in writing. Only then compare with the example answers.

1. Why does a function need a parameter?
2. How does a parameter differ from an argument?
3. Does an argument have to be a literal?
4. What does `int length` mean in a function's definition?
5. Can a function be called several times with different arguments?
6. In what order do the values go to the parameters?
7. Why might swapping two `int` arguments cause no compile error?
8. What does passing by value mean?
9. Why doesn't changing `remaining` change `laps`?
10. Is a parameter automatically available in `main`?
11. Can a `void` function have parameters?
12. Why doesn't the bar-printing function need to know where the data came from?
13. What should happen for a bar of length zero?
14. Why doesn't a test with two equal values reveal every swap of arguments?

<details>
<summary>Example answers</summary>

1. So that one function can do a similar job for different data. It gets the data at every call, so you don't need a separate function for every value.
2. A parameter is a named variable in the function's definition. An argument is an expression given at the call. The parameter receives its value.
3. No. An argument can be a literal, a variable or an expression, for example `separator_length + 2`.
4. That the function has a parameter named `length` of type `int`. At every call, `length` receives the argument's value.
5. Yes. Each call can pass a different value, and the function's body then runs with that value.
6. By position: the first argument goes to the first parameter, the second to the second. The names of the variables in `main` don't matter.
7. Because both values have the same type, so the call is valid C++. The compiler doesn't know which number was meant to be which. It's a logic error, not a compile error.
8. That the parameter receives the argument's value and the function works on that value of its own. Changing the parameter doesn't change the variable given as the argument.
9. Because `remaining` is a separate variable of the function, which only received the value of `laps`. Only `remaining` changes.
10. No. A parameter exists only in its function. In `main` its name is unknown.
11. Yes. `void` only says that the function doesn't pass back a result. The parameters say what data the function receives.
12. Because it gets ready values as arguments. Reading and checking the data belong to `main`, and the function only prints a bar for the values it received.
13. The line `Day N: []` should appear: the loop prints no `#`, but the start and the end of the line are always printed.
14. Because when both values are equal, swapping them puts the same numbers in the same places. Only different values show which one went to which parameter.

</details>

## Summary

- A **parameter** is a named variable of a function, written in the definition's parentheses, for example `int length`. It receives a value at every call.
- An **argument** is an expression given at the call: a literal, a variable or an expression, for example `print_line(separator_length + 2)`.
- One function with a parameter can do a similar job for different data.
- With several parameters, the arguments go to the parameters **by position**. The names of the variables at the place of the call don't matter.
- If two parameters have the same type, the compiler won't detect swapped arguments. Only a test with different values reveals them.
- **Passing by value:** the function works on its own value of the parameter, received from the argument. Changing the parameter doesn't change the variable at the place of the call.
- A parameter exists only in its function. In `main` its name is unknown.
- A `void` function can have parameters: `void` is only about the result.

## What's next

The functions in this lesson receive data, but give nothing back: anything they work out, they can only print. In the next lesson you'll see how a function can pass a result back to the place of the call: [Lesson 5.3: A function returns a result (`return`)](lesson_03_returning_a_result.en.md).

---

## Example solutions

Look here **after your own attempt**. Your names may differ, as long as the standard output is as required.

<details>
<summary>Section 9: the results before the fix, and the fixed program</summary>

Before the fix, case A, data `3`, `3`:

<!-- input: pair_bug -->
```text
3
3
```

<!-- output: pair_bug -->
```text
Enter two values:
First: 3
Second: 3
```

Case B, data `2`, `5`:

<!-- input: pair_bug -->
```text
2
5
```

<!-- output: pair_bug -->
```text
Enter two values:
First: 5
Second: 2
```

- **Case A looks correct**, because both values are equal: swapping them puts the same numbers in the same places.
- **Case B reveals the bug:** the first value read, 2, should be `First`, but it appears as `Second`.
- **The cause:** the call `show_pair(second_value, first_value)` gives the arguments in the reverse order. The function's definition is correct. Both arguments are `int`s, so the compiler reports neither an error nor a warning.
- **The fix:** `show_pair(first_value, second_value);`.

<!-- example: pair_fixed -->
```cpp
#include <iostream>

void show_pair(int first, int second) {
    std::cout << "First: " << first << "\n";
    std::cout << "Second: " << second << "\n";
}

int main() {
    int first_value{0};
    int second_value{0};

    std::cout << "Enter two values:\n";
    std::cin >> first_value;
    std::cin >> second_value;

    show_pair(first_value, second_value);
}
```

<!-- input: pair_fixed -->
```text
3
3
```

<!-- output: pair_fixed -->
```text
Enter two values:
First: 3
Second: 3
```

<!-- input: pair_fixed -->
```text
2
5
```

<!-- output: pair_fixed -->
```text
Enter two values:
First: 2
Second: 5
```

</details>

<details>
<summary>Section 10: the fixed program</summary>

`main` keeps the value in a variable of its own, passes it as the argument, and prints it itself:

<!-- example: param_scope_fixed -->
```cpp
#include <iostream>

void print_line(int length) {
    for (int position{0}; position < length; ++position) {
        std::cout << "-";
    }

    std::cout << "\n";
}

int main() {
    const int requested_length{4};

    print_line(requested_length);
    std::cout << "Length: " << requested_length << "\n";
}
```

<!-- output: param_scope_fixed -->
```text
----
Length: 4
```

</details>

<details>
<summary>Section 11: the mission, an activity chart</summary>

<!-- example: activity_chart -->
```cpp
#include <iostream>

void print_bar(int day, int blocks) {
    std::cout << "Day " << day << ": [";

    for (int block{0}; block < blocks; ++block) {
        std::cout << "#";
    }

    std::cout << "]\n";
}

int main() {
    int first_day_blocks{0};
    int second_day_blocks{0};
    int third_day_blocks{0};

    std::cout << "Enter blocks for days 1, 2 and 3:\n";
    std::cin >> first_day_blocks;
    std::cin >> second_day_blocks;
    std::cin >> third_day_blocks;

    if (std::cin.fail()) {
        std::cout << "Input could not be read\n";
    } else {
        const bool first_valid{first_day_blocks >= 0 && first_day_blocks <= 6};
        const bool second_valid{second_day_blocks >= 0 && second_day_blocks <= 6};
        const bool third_valid{third_day_blocks >= 0 && third_day_blocks <= 6};

        if (first_valid && second_valid && third_valid) {
            print_bar(1, first_day_blocks);
            print_bar(2, second_day_blocks);
            print_bar(3, third_day_blocks);
        } else {
            std::cout << "Invalid bar data\n";
        }
    }
}
```

- **The function `print_bar`** has two parameters with different roles. `day` is only printed, and `blocks` controls the loop. The start of the line, and the `]` with the line ending, stand outside the loop, so zero blocks give `Day N: []`.
- **The arguments:** in every call the first argument is the day number and the second is the number of blocks, in the same order as the parameters. For the data `2`, `0`, `4` the function gets (1, 2), (2, 0) and (3, 4) in turn.
- **`main`** reads the data, checks it and decides on the calls. The function doesn't know where the values came from.
- **A failed read:** after a failed read, the following reads fail too, so one `std::cin.fail()` check after the three reads is enough. That also covers data that ends after two numbers: reading the third one fails. The variables' values aren't used then.
- **The range check** stands in the branch for a successful read, with three named conditions as in lesson 3.4. The chart is drawn only when all three hold.
- You can also put the parameters in the definition in the reverse order, for example `print_bar(int blocks, int day)`. Then the correct call for the first day is `print_bar(first_day_blocks, 1)`. Both arrangements are fine, as long as the definition and the calls agree.

</details>

**Previous lesson:** [Lesson 5.1: Your first function (`void`)](lesson_01_the_first_function.en.md) · **Next lesson:** [Lesson 5.3: A function returns a result (`return`)](lesson_03_returning_a_result.en.md) · [Course overview](../../README.en.md)

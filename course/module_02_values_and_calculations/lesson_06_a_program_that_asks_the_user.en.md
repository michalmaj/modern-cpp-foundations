# Lesson 2.6: A program that asks the user

[Polski](lesson_06_a_program_that_asks_the_user.md) · **English** · [Course overview](../../README.en.md)

> **Module 2, lesson 6** · about 75 minutes
> **You need:** the `cpp-workspace` folder and the original `lesson_05_first_program` project, as before, and the terminal from lessons 0.5 and 0.6. You don't need the debugger in this lesson.
> **Pilot version.** The programs in this lesson are checked automatically on Windows, Ubuntu and macOS, including with the given input data. Typing input into CLion's **Run** window is described without a manual check on every system. If you can't type input into the **Run** window, run the programs in the terminal, as in section 3.

## Before you start

This lesson assumes that after lesson 2.5:

- you create `int` and `double` variables and constants with a starting value in `{}`;
- you know that `int` times `double` gives `double`, and that dividing two `int`s is an integer division;
- you run a built program in the terminal, as in lesson 0.5, section 7.

## The situation

So far, all the data has been written in the code. To calculate something for other numbers, you had to change the code and build the program again. Real programs usually ask: for a number, a size, a time. Today, for the first time, a program will **take data while it runs**. You'll see that **the same program, without being built again, gives different results for different data**.

After this lesson you will:

- tell data written in the code apart from data given while the program runs;
- explain what standard input is, and how it differs from standard output;
- read `int` and `double` numbers with `std::cin` and `>>`;
- ask the user for data, and tell what the program prints apart from what the user types;
- use the data you read in calculations, and print a result that depends on it;
- run the same program several times with different data;
- describe the path of information: input → variable → calculation → result.

## 1. Prepare the project

In `cpp-workspace`, create a folder `lesson_2_6`, copy `main.cpp` and `CMakeLists.txt` into it from the original `lesson_05_first_program`, and open this folder in CLion, as in lesson 1.1 (**File | Open**).

## 2. Data in the code and data from the user

This program knows its number from the start, because it is written in the code:

<!-- example: count_in_code -->
```cpp
#include <iostream>

int main() {
    const int count{5};
    std::cout << "Count: " << count << "\n";
}
```

<!-- output: count_in_code -->
```text
Count: 5
```

To make it print a different number, you have to change the code and build the program again. Now replace the contents of `main.cpp` with a version that takes the number from the user:

<!-- example: count_from_input -->
```cpp
#include <iostream>

int main() {
    int count{0};
    std::cin >> count;
    std::cout << "Count: " << count << "\n";
}
```

Build it and run it (**Run**). The program prints nothing and just waits. Click in the **Run** window, type `5` and press **Enter**.

Input data:

<!-- input: count_from_input -->
```text
5
```

The program prints:

<!-- output: count_from_input -->
```text
Count: 5
```

## 3. The same program, different data

This is the most important experiment of this lesson. **Don't change the code.**

1. Run the program again (**Run**). The code hasn't changed, so CLion doesn't need to build anything (lesson 0.5): it runs the same executable.
2. This time type `12` and press **Enter**.

<!-- input: count_from_input -->
```text
12
```

<!-- output: count_from_input -->
```text
Count: 12
```

Between the runs, the code, the `CMakeLists.txt` file and the executable **did not change**. Only the **data** changed, and the result changed with it.

**The same experiment in the terminal.** Here it's clearest that this is one and the same executable, because you run it directly, without any building. In the terminal, go to the `lesson_2_6` folder and run the program built by CLion twice, as in lesson 0.5, section 7. Type `5` the first time and `12` the second:

| Windows (PowerShell) | macOS and Linux |
|---|---|
| `.\cmake-build-debug\first_program.exe` | `./cmake-build-debug/first_program` |

## 4. What `std::cin >> count;` does

- **`std::cin`** is the program's **standard input**: a stream the program can take data from. It's the partner of the familiar `std::cout`, the **standard output**.
- **`>>`** reads a value from the stream and **stores it in the variable** on its right. After `std::cin >> count;`, the variable `count` has the value that was read.
- The direction of the arrows shows the path of the data:
  - `std::cout << count` sends a value **from the variable to the output**, to the screen;
  - `std::cin >> count` takes a value **from the input into the variable**.
- When you run a program in the terminal or in CLion, standard input is usually the **keyboard**: what you type into the program's window. But the data can also come from another source. For example, this course's automatic tests give programs their data without anyone typing on a keyboard.

## 5. The program waits for data

What happens when the program reaches `std::cin >> count;`? Check it with this program:

<!-- example: waiting -->
```cpp
#include <iostream>

int main() {
    int count{0};
    std::cout << "Before reading\n";
    std::cin >> count;
    std::cout << "After reading: " << count << "\n";
}
```

Run it and **don't type anything yet**. Look at the program's window: `Before reading` is already there, but `After reading` isn't.

The program hasn't frozen. **It's waiting for data**: the statement `std::cin >> count;` hasn't finished yet, so the statements after it haven't run. Now type `7` and press **Enter**. **Enter** confirms the value you typed: only then does the program read it and carry on.

<!-- input: waiting -->
```text
7
```

<!-- output: waiting -->
```text
Before reading
After reading: 7
```

The statements after the reading already use the value that was read. If the debugger has worked for you since lesson 2.3, you can also watch this step by step, but you don't need to.

## 6. Ask for the data, and tell it apart from the result

A program that just waits doesn't say what it wants. That's why it usually prints a request before reading:

<!-- example: prompt -->
```cpp
#include <iostream>

int main() {
    int count{0};
    std::cout << "Enter count:\n";
    std::cin >> count;
    std::cout << "Count: " << count << "\n";
}
```

`std::cout` only **prints** the request. It reads nothing, and printing it doesn't by itself make the program take any data. Only `std::cin` reads.

When you run the program and type `5`, you'll see three lines on the screen:

```text
Enter count:
5
Count: 5
```

**Not all of them come from the program.** You see the line `5` only because the window you type into shows the characters you type. This is called **echo**. The program didn't print it: no `std::cout` in the code prints `5` on its own. That's why this course keeps three things apart.

**Input data**, that is, what goes into `std::cin`:

<!-- input: prompt -->
```text
5
```

**Standard output**, that is, only what the program printed with `std::cout`:

<!-- output: prompt -->
```text
Enter count:
Count: 5
```

**A record of what you see on the screen**, as above: the program's lines with the typed number between them.

This course's automatic tests compare only the standard output.

## 7. Read an `int` and a `double`

A program can read several values of different types. Each goes into a variable whose type fits the data:

<!-- example: floors_and_height -->
```cpp
#include <iostream>

int main() {
    int floors{0};
    double floor_height_m{0.0};

    std::cout << "Enter the number of floors:\n";
    std::cin >> floors;
    std::cout << "Enter the floor height in m:\n";
    std::cin >> floor_height_m;

    std::cout << "Floors: " << floors << "\n";
    std::cout << "Floor height: " << floor_height_m << " m\n";
}
```

Run the program and give two values on separate lines: `3` and `2.75`.

<!-- input: floors_and_height -->
```text
3
2.75
```

<!-- output: floors_and_height -->
```text
Enter the number of floors:
Enter the floor height in m:
Floors: 3
Floor height: 2.75 m
```

- The number of floors is a whole number, so it goes into an `int`. A floor height can have a fractional part, so it goes into a `double`. **The variable's type must fit the kind of data** you want to read.
- Type a value with a fractional part with a **dot**: `2.75`, just as in the code.
- `>>` skips the spacing before a value: spaces, tabs and line breaks. That's why you can also type both values on one line, separated by a space. Check it: run the program again and type `3 2.75`, then **Enter**. The result is the same:

<!-- input: floors_and_height -->
```text
3 2.75
```

<!-- output: floors_and_height -->
```text
Enter the number of floors:
Enter the floor height in m:
Floors: 3
Floor height: 2.75 m
```

## 8. Variables for data

A variable the program reads data into has a starting value like any other: `int floors{0};`, `double floor_height_m{0.0};`.

- `0` and `0.0` are only **starting values**. A successful read replaces them with the data from standard input.
- Such a variable **can't be `const`**: reading changes its value, and a constant can't be changed. Check what the compiler says if you try:

<!-- broken: read_into_const at=5 errors=1 error=^(invalid operands to binary expression|use of overloaded operator '>>' is ambiguous) .*'const int'\)$ -->
```cpp
#include <iostream>

int main() {
    const int count{0};
    std::cin >> count;
    std::cout << "Count: " << count << "\n";
}
```

The program won't build. The compiler reports an error on line 5, at `>>`, but its wording depends on the system, because it comes from the standard library:

- on Ubuntu and macOS: `invalid operands to binary expression ('istream' (aka 'basic_istream<char>') and 'const int')`;
- on Windows: `use of overloaded operator '>>' is ambiguous (with operand types 'istream' (aka 'basic_istream<char, char_traits<char>>') and 'const int')`.

Below it come many `note:` lines about the standard library, several dozen on some systems. You don't need to read them. As in lesson 1.2, what counts is the first line with `error` in `main.cpp`. Both versions end the same way: `'const int'`. That's the cause: `>>` can't store a value in a constant. Restore correct code: remove `const`.

- **After** reading, you can use the data to create a constant, if the result of a calculation shouldn't change any more. You'll do that in the next section.
- The starting value `0` does **not** protect the program against bad data. It's simply a correctly initialised variable (more in section 11).

## 9. Calculate with the data

A warehouse packs items into boxes. The program asks for the number of boxes and the number of items in one box, then counts all the items:

<!-- example: boxes_total -->
```cpp
#include <iostream>

int main() {
    int boxes{0};
    int items_per_box{0};

    std::cout << "Enter the number of boxes:\n";
    std::cin >> boxes;
    std::cout << "Enter the items per box:\n";
    std::cin >> items_per_box;

    const int total_items{boxes * items_per_box};

    std::cout << "Total items: " << total_items << "\n";
}
```

The order matters: the calculation comes **after** both reads, so it uses the numbers that were typed, not the starting values 0. The result doesn't change any more, so it is a `const int` constant.

Run the program twice: with the data `3` and `4`, then `5` and `6`.

<!-- input: boxes_total -->
```text
3
4
```

<!-- output: boxes_total -->
```text
Enter the number of boxes:
Enter the items per box:
Total items: 12
```

<!-- input: boxes_total -->
```text
5
6
```

<!-- output: boxes_total -->
```text
Enter the number of boxes:
Enter the items per box:
Total items: 30
```

**Predict** what the program prints for `7` and `8`. Write the result down, then check it by running the program a third time.

<!-- input: boxes_total -->
```text
7
8
```

<details>
<summary>The output for 7 and 8</summary>

<!-- output: boxes_total -->
```text
Enter the number of boxes:
Enter the items per box:
Total items: 56
```

</details>

## 10. When the result's type doesn't fit

In lesson 2.5, all the data were constants with values written in the code. Now the values appear only while the program runs, and that matters for `{}`. This program stores the number of seats in a room as a `double`:

<!-- broken: seats_as_double at=8 errors=1 error=^non-constant-expression cannot be narrowed from type 'int' to 'double' in initializer list -->
```cpp
#include <iostream>

int main() {
    int rows{0};
    int chairs_per_row{0};
    std::cin >> rows;
    std::cin >> chairs_per_row;
    const double seats{rows * chairs_per_row};
    std::cout << "Seats: " << seats << "\n";
}
```

The program won't build. On line 8, the compiler reports `non-constant-expression cannot be narrowed from type 'int' to 'double' in initializer list`.

- In lesson 2.5, `const double first{7 / 2};` built, because `7 / 2` is a **constant expression**: the compiler knows its value while building, and sees that it can be stored in a `double` without changing.
- Here, `rows * chairs_per_row` depends on data that doesn't exist yet. An `int` result known only while the program runs is treated by `{}` as a narrowing conversion when it is changed to `double`, and is not accepted.
- Skip the `note:` line suggesting an explicit cast for now, as in lesson 2.5.

The right fix is **a type that fits the result**. The number of seats is a whole number, and `int` times `int` gives `int`, so the result should be of type `int`:

<!-- example: seats_as_int -->
```cpp
#include <iostream>

int main() {
    int rows{0};
    int chairs_per_row{0};
    std::cin >> rows;
    std::cin >> chairs_per_row;
    const int seats{rows * chairs_per_row};
    std::cout << "Seats: " << seats << "\n";
}
```

<!-- input: seats_as_int -->
```text
5
8
```

<!-- output: seats_as_int -->
```text
Seats: 40
```

You'll see the same with division: `const double average{points / games};` with two `int` variables read from input won't build either, with the same message. Even without that error the result would be wrong, because dividing two `int`s is an integer division (lesson 2.4). So in the exercises, choose types by the meaning of the data: `int` for whole numbers, `double` for quantities with a fractional part. When a `double` takes part in a multiplication, the result is a `double` too, and fits a `double` variable.

## 11. We assume correct data

For now, your programs assume that the user gives data that matches the request: a whole number where the program asks for a whole number, and a number with a dot where it asks for a number with a fractional part. **The program can't yet handle correctly** a situation in which someone:

- types text instead of a number;
- doesn't give a required value;
- gives a number too large for the type;
- gives a value that makes no sense in the situation, such as a negative number of boxes;
- writes a number in another form, such as `2,75` instead of `2.75`.

The result will then simply be wrong. You'll learn to check data and react to errors later, once you know the statements that let a program choose what to do. Until then, give data that matches the description in the exercises. That's also why no program in this lesson divides by a number given by the user: someone could type 0, and dividing by zero must never be done (lesson 2.4).

## 12. Mission: the training distance

Write a program that calculates the total distance of a running session. The user gives:

1. the number of laps (a whole number);
2. the length of one lap in kilometres (a number with a fractional part).

The program calculates **total distance = number of laps × lap length** and prints it.

In `cpp-workspace`, create a folder `training_distance`, copy `CMakeLists.txt` into it from the original `lesson_05_first_program`, create an empty `main.cpp`, and write the program on your own.

**The first run:** 4 laps of 1.25 km.

<!-- input: training_distance -->
```text
4
1.25
```

The standard output must be exactly:

<!-- output: training_distance -->
```text
Enter the number of laps:
Enter the lap length in km:
Total distance: 5 km
```

**A second run of the same program,** without changing the code: 3 laps of 2.5 km.

<!-- input: training_distance -->
```text
3
2.5
```

<!-- output: training_distance -->
```text
Enter the number of laps:
Enter the lap length in km:
Total distance: 7.5 km
```

On the screen you'll also see the numbers you typed between the program's lines (echo, section 6). In the first run the total distance is 5.0 km, but `std::cout` prints it as `5` (lesson 2.5).

### Success criteria

- The program builds as C++20, and its standard output for both sets of data is exactly as above.
- **The same program gives both results:** between the runs you don't change the code and don't build the program again.
- The number of laps goes into an `int` variable and the lap length into a `double` variable, both with starting values and without `const`.
- The total distance is calculated **after** both values are read, and has a type that fits the result of the multiplication. You can justify that type.
- The code contains none of the numbers 4, 1.25, 3, 2.5, 5 or 7.5: the data comes from standard input, and the program calculates the result.
- The program uses only what you already know, plus `std::cin` and `>>`.
- You can explain why the result changed even though the code stayed the same.

Once the output matches, you can save the project in Git, as in lesson 1.5.

<details>
<summary>Hint 1</summary>

First the variables for the data, then a request and a read for each value, and finally the calculation and the result. The program in section 9 has the same order, but different types.

</details>

<details>
<summary>Hint 2</summary>

`int` times `double` gives `double` (lesson 2.5). So what type must the total distance be, for `{}` to accept the result of the multiplication?

</details>

An example solution is in [Example solutions](#example-solutions).

## 13. When something goes differently

| What you see | What it means | What to do |
|---|---|---|
| The program prints nothing, or printed the request and "stands still" | It's waiting for data at `std::cin`. It hasn't frozen. | Type a value into the program's window and press **Enter**. |
| You can't type anything into CLion's **Run** window | This part of the instructions hasn't been checked on every system yet. | Run the program in the terminal, as in section 3. |
| The result doesn't depend on the data you type | The calculation or the output comes **before** the read, and uses the starting value. | The read must come before the calculation that uses it. |
| The number you typed appears on the screen, although you don't print it | That's the echo of the window you type into, not the program's output. | Nothing. It isn't the program's standard output. |
| A compile error at `std::cin >>` with a `const` variable | You can't read a value into a constant. | A variable for data can't be `const`. |
| The error `non-constant-expression cannot be narrowed …` at `{}` | The result of an operation on two `int`s is going into a `double` (section 10). | Choose the result's type to fit the calculation, for example `int` for a number of seats. |
| You typed `2,75` or text, and the result is strange | The program doesn't handle such data yet (section 11). | Run the program again and give data that matches the request, with a dot. |

## 14. Explain

Answer in your own words, preferably in writing. Only then compare with the example answer.

**1.** Why did the same executable print `Count: 5` once and `Count: 12` another time?

<details>
<summary>Example answer</summary>

Because the program doesn't have that number in its code. It reads it from standard input every time it runs. The code and the executable didn't change; only the data changed, and the result depends on it.

</details>

**2.** How is `std::cin >> count` different from `std::cout << count`?

<details>
<summary>Example answer</summary>

`std::cin >> count` takes a value from standard input and stores it in `count`. `std::cout << count` sends the value of `count` to standard output. The arrows show the direction of the data.

</details>

**3.** The screen shows `Enter count:`, `5` and `Count: 5`. Which of these lines did the program print?

<details>
<summary>Example answer</summary>

`Enter count:` and `Count: 5`. The line `5` is the typed data, visible thanks to the echo of the window you type into.

</details>

**4.** Why can't the variable you read data into be `const`?

<details>
<summary>Example answer</summary>

Because reading changes its value: it replaces the starting value with the typed number. A constant can't be changed after initialisation.

</details>

**5.** Describe the path of information in the mission, from the keyboard to the result.

<details>
<summary>Example answer</summary>

The user types the numbers. `std::cin >>` stores them in the `int` and `double` variables. The program multiplies these values and stores the result in a `double` variable. `std::cout <<` prints the result to standard output.

</details>

## Summary

- A program can take data **while it runs**. The same executable then gives different results for different data, without changing the code and without building it again.
- `std::cin` is **standard input**, and `std::cout` is **standard output**. `std::cin >> x` stores the value it reads in `x`.
- At `std::cin`, the program **waits for data**. **Enter** confirms the value you typed.
- `std::cout` prints the request, and only `std::cin` reads. You see the typed numbers on the screen thanks to echo, but they aren't the program's output.
- The variable's type must fit the data: `int` for whole numbers, `double` for numbers with a dot. `>>` skips spaces and line breaks between values.
- A variable for data has a starting value and isn't `const`. The result of a calculation after the read can be a constant.
- The result of an operation on two `int`s read from input won't go into a `double` through `{}`. Choose types that fit the calculation.
- For now we assume correct data. You'll learn to handle bad data later.

## What's next

Your programs now ask for numbers. In lesson 2.7 you'll meet text values, and a program will ask for a word. **Lesson 2.7 is in preparation.**

---

## Example solutions

Look here **after your own attempt**. Your names may differ, as long as the standard output is as required.

<details>
<summary>Section 12: mission, the training distance</summary>

<!-- example: training_distance -->
```cpp
#include <iostream>

int main() {
    int laps{0};
    double lap_length_km{0.0};

    std::cout << "Enter the number of laps:\n";
    std::cin >> laps;
    std::cout << "Enter the lap length in km:\n";
    std::cin >> lap_length_km;

    const double total_distance_km{laps * lap_length_km};

    std::cout << "Total distance: " << total_distance_km << " km\n";
}
```

- `laps` is of type `int`, because there is always a whole number of laps. `lap_length_km` is of type `double`, because a length can have a fractional part. Both variables receive data, so neither is `const`.
- `laps * lap_length_km` is an `int` times a `double`, so the result is of type `double` and fits `const double total_distance_km`. You could also write `const auto total_distance_km{laps * lap_length_km};`: the compiler works out the type `double`.
- The same program handles both sets of data: 4 · 1.25 = 5 and 3 · 2.5 = 7.5.

</details>

**Previous lesson:** [Lesson 2.5: Numbers with a fractional part: `double` and `auto`](lesson_05_numbers_with_a_fractional_part.en.md) · **Next lesson:** in preparation · [Course overview](../../README.en.md)

# Lesson 2.1: Values the program remembers

[Polski](lesson_01_values_the_program_remembers.md) · **English** · [Course overview](../../README.en.md)

> **Module 2, lesson 1** · about 60 minutes
> **You need:** the `cpp-workspace` folder and the original `lesson_05_first_program` project, as in Module 1.
> **Pilot version.** The examples in this lesson are checked automatically on Windows, Ubuntu and macOS.

## Before you start

This lesson assumes that after Module 1:

- you can write a program that prints text, starting from an empty file, then build and run it;
- you read compiler messages with the method from lesson 1.2;
- you save your work in Git (lesson 1.5).

## The situation

So far, every program of yours printed text that someone had prepared in advance, character by character. Even the number `75` in the output was just two characters in a text.

Today the program will **calculate** the result itself. The values it calculates from will have names, and when you change one of them, everything that depends on it changes too.

After this lesson you will:

- tell text that contains digits apart from a numeric value;
- know what a numeric literal is and what the type `int` is for;
- create variables with a starting value, for example `int ticket_count{3};`;
- use variables in calculations with `+`, `-` and `*`, and store the result in a new variable;
- print text and numbers in one statement;
- predict a program's output before you run it;
- write a program on your own whose output depends on given values.

## 1. Prepare the project

In `cpp-workspace`, create a folder `lesson_2_1` and copy `main.cpp` and `CMakeLists.txt` into it from the original `lesson_05_first_program`, as in Module 1. You type the programs of this lesson into that folder's `main.cpp`. You build and run it as before: in CLion or in the terminal.

## 2. Text vs. number

Replace the content of `main.cpp` with this program:

<!-- example: text_or_number -->
```cpp
#include <iostream>

int main() {
    std::cout << "3 + 4\n";
    std::cout << (3 + 4) << "\n";
}
```

**Predict** what each of the two statements prints. Write your answer down, then run the program.

<details>
<summary>The program's output</summary>

<!-- output: text_or_number -->
```text
3 + 4
7
```

</details>

**What happened?**

- **The first statement** prints **text**, as in Module 1. The quotes say: "print these characters exactly as they are". Digits inside text are just characters, like letters.
- **In the second statement,** `3` and `4` stand **without quotes**. They are **numeric literals**: numbers written directly in the code. The program treats them as numbers, so `3 + 4` is an **expression** that the program **calculates** while it runs. It sends the result to `std::cout`: the value `7`.
- **The parentheses** around `3 + 4` show clearly what is to be calculated. You'll learn the exact rules of the order of operations in a later lesson.
- **What's new is the two `<<` in one statement:** `std::cout << (3 + 4) << "\n";`. Each `<<` sends the next item to `std::cout`, from left to right: first the value `7`, then the text `"\n"`, which moves to a new line.

## 3. Predict: a few calculations

Replace the content of `main.cpp` with this program. **Before you run it,** write down what each line will print.

<!-- example: predict -->
```cpp
#include <iostream>

int main() {
    std::cout << (10 - 3) << "\n";
    std::cout << (6 * 7) << "\n";
    std::cout << "6 * 7 = " << (6 * 7) << "\n";
    std::cout << (2 + 3 + 4) << "\n";
}
```

<details>
<summary>The program's output</summary>

<!-- output: predict -->
```text
7
42
6 * 7 = 42
9
```

</details>

- `-` is subtraction and `*` is multiplication. The letter `x` doesn't mean multiplication in C++.
- The third line combines both worlds: first the text `"6 * 7 = "`, printed exactly as it is, and then the **calculated** value `42`.

## 4. A variable: a name for a value

A box office sells tickets at 25. This program prints the price and the cost of three tickets:

<!-- example: repeated_numbers -->
```cpp
#include <iostream>

int main() {
    std::cout << "Price per ticket: " << 25 << "\n";
    std::cout << "Total cost: " << (3 * 25) << "\n";
}
```

<!-- output: repeated_numbers -->
```text
Price per ticket: 25
Total cost: 75
```

It works, but the price `25` is typed in two places. If it changes, you have to find and fix it everywhere, and it's easy to forget one place. Also, `3 * 25` doesn't say what these numbers mean.

The solution is a **variable**: **a named value of a given type**. An analogy that can help is a labelled drawer holding a number. It's only an analogy: in reality the compiler manages the variable, and you don't need to know exactly how it stores it.

<!-- example: first_variables -->
```cpp
#include <iostream>

int main() {
    int ticket_count{3};
    int ticket_price{25};
    int total_cost{ticket_count * ticket_price};

    std::cout << "Tickets: " << ticket_count << "\n";
    std::cout << "Price per ticket: " << ticket_price << "\n";
    std::cout << "Total cost: " << total_cost << "\n";
}
```

<!-- output: first_variables -->
```text
Tickets: 3
Price per ticket: 25
Total cost: 75
```

Take apart the first line in `main`, `int ticket_count{3};`:

| Part | Meaning |
|---|---|
| `int` | The **type**: what kind of value the variable holds. `int` means **whole** numbers, with no fractional part, for example `3`, `25`, `-7`. You'll meet other types in later lessons. |
| `ticket_count` | The **name** of the variable. With it, you use the value later in the program. |
| `{3}` | **Initialisation**: the starting value. The variable gets it right when it is created. |
| `;` | The end of this line, as with statements. |

The whole line is a **declaration** of the variable: it tells the compiler that from now on there is a variable with this name, type and starting value.

**Using a variable:**

- `ticket_count * ticket_price` in the third line **reads** the values of both variables and multiplies them. The result, `75`, becomes the starting value of the new variable `total_cost`.
- `std::cout << ticket_count` prints the variable's **value**, `3`. The name alone, without quotes, means the value. `"ticket_count"` in quotes would be ordinary text, and the program would print the word `ticket_count`.
- You use a variable **after** its declaration, that is, lower in the code. That's why `total_cost` stands below `ticket_count` and `ticket_price`.

**Good habits, from the very first variable:**

- **Always give a starting value.** A variable without one has no defined value, and reading it is an error that the compiler doesn't always detect. In this course, every variable gets its value right away.
- **The name says what the value means:** `ticket_price`, not `p` or `x`.
  - In this course, names are in English, in lower case, with words joined by underscores (`snake_case`).
  - A name can't contain a space or a hyphen, and can't start with a digit.
  - Letter case matters: `Total` and `total` are two different names.
- In this lesson, every variable gets its value **once**, when it is created. How to change the value of a variable that already exists is the topic of lesson 2.2.

**A quick experiment with a typo.** In the last program, change `ticket_count` in one of the `std::cout` lines to `ticket_cout` (without the `n`). Build it. For example:

<!-- broken: name_typo at=5:33 errors=1 error=^use of undeclared identifier 'ticket_cout'; did you mean 'ticket_count'\?$ -->
```cpp
#include <iostream>

int main() {
    int ticket_count{3};
    std::cout << "Tickets: " << ticket_cout << "\n";
}
```

You know the message from lesson 1.2: `use of undeclared identifier 'ticket_cout'; did you mean 'ticket_count'?`. The compiler doesn't know the name `ticket_cout`, and suggests a similar name that it does know. Fix the typo and build the program again.

## 5. Change the values

Go back to the box office program (the one with three variables). **Change only** the starting value of `ticket_count`, from `3` to `5`.

**Predict** what the program will print before you build and run it.

<details>
<summary>The program's output</summary>

<!-- output: first_variables_changed -->
```text
Tickets: 5
Price per ticket: 25
Total cost: 125
```

</details>

One number changed in the code, and two lines changed in the output, because `total_cost` is calculated from `ticket_count`. That's the benefit of variables: each value is written in the code **once**, and everything that depends on it uses its name. Remember that, as always after a code change, the program has to be **built again**.

## 6. Fill in: the area of a room

A room is 4 metres wide and 5 metres long. One line is missing from the program:

<!-- fragment -->
```cpp
#include <iostream>

int main() {
    int room_width{4};
    int room_length{5};
    _______________________________________

    std::cout << "Area: " << room_area << " square metres\n";
}
```

**Your task:** replace the line of underscores with **your own declaration** of a variable `room_area`, whose value the program calculates from the width and the length. The program must print:

<!-- output: room_area -->
```text
Area: 20 square metres
```

Don't type the number `20` in the code: let the program calculate it.

<details>
<summary>Hint</summary>

Look at how `total_cost` is created in section 4: the type, the name, and in `{}` an expression with other variables.

</details>

## 7. Mission: the box office

A concert hall has 50 seats. A ticket costs 40, and 6 tickets have been sold. The cashier wants a program that prints a short summary.

In `cpp-workspace`, create a folder `ticket_office`, copy `CMakeLists.txt` into it from the original `lesson_05_first_program`, create an empty `main.cpp`, and write the program yourself.

The program must print exactly:

<!-- output: ticket_office -->
```text
Tickets sold: 6
Price per ticket: 40
Total: 240
Seats left: 44
```

### Success criteria

- The output matches character by character.
- The number of seats in the hall, the price and the number of tickets sold are stored in `int` variables, each **once**, with a starting value in `{}`.
- **The program calculates** `240` and `44`. These numbers don't appear in the code.
- Variable names are in English, in `snake_case`, and say what the value means.
- You can explain how the program "knows" that 44 seats are left.

Once the output matches, you can save the project in Git, as in lesson 1.5.

<details>
<summary>Hint 1</summary>

How many different values does the task give you? How many must be calculated? Each of them can have its own variable.

</details>

<details>
<summary>Hint 2</summary>

The number of seats left is the number of seats in the hall **minus** the number of tickets sold.

</details>

### Variant: more tickets sold

3 more tickets have been sold, so 9 in total. **Predict** the new output, then change **one** starting value in the program, build it and run it. The output must be:

<!-- output: ticket_office_variant -->
```text
Tickets sold: 9
Price per ticket: 40
Total: 360
Seats left: 41
```

If you have to change more than one number in the program, go back to the mission's criteria.

Example solutions are in [Example solutions](#example-solutions).

## 8. When something goes differently

| What you see | What it means | What to do |
|---|---|---|
| The name of a variable appears instead of a number, for example `Total: total_cost` | The name is in quotes, so it's ordinary text. | Remove the quotes around the name: `<< total_cost <<`. |
| The output is glued to the text, for example `Total:240` | The text before the value is missing a space. | Add a space at the end of the text: `"Total: "`. |
| `use of undeclared identifier '…'` | The compiler doesn't know this name: a typo, different letter case, or a variable used above its declaration. | Compare the name with the declaration, character by character. Check that the declaration is above. The compiler often suggests the right name (`did you mean …?`). |
| A compile error on a line with `<<` | A `<<` is missing between items, or a quote is missing in a text. | Every item (text, value, `"\n"`) gets its own `<<` before it. |
| After changing a value, the program prints the old result | The program wasn't built again. | Build again (Run in CLion does it for you). |

**Note:** in C++ you don't join text and a number with `+`, as you might in some other languages. You send each item to `std::cout` with its own `<<`.

## 9. Explain

Answer in your own words, preferably in writing. Only then compare with the example answer.

**1.** Why does `std::cout << "3 + 4\n";` print `3 + 4`, while `std::cout << (3 + 4) << "\n";` prints `7`?

<details>
<summary>Example answer</summary>

In quotes, `3 + 4` is text that the program prints character by character. Without quotes, `3` and `4` are numbers, and `3 + 4` is an expression that the program calculates. Its result, `7`, goes to `std::cout`.

</details>

**2.** What does each part of `int ticket_price{25};` mean?

<details>
<summary>Example answer</summary>

`int` is the type: a whole number. `ticket_price` is the name of the variable. `{25}` is the starting value. `;` ends the declaration.

</details>

**3.** Why did two lines of the output change after `ticket_count` went from `3` to `5`, although one number changed in the code?

<details>
<summary>Example answer</summary>

Because `total_cost` is calculated from the value of `ticket_count`. The program prints `ticket_count` and the `total_cost` calculated from it, so both lines depend on that one value.

</details>

**4.** How does `std::cout << total_cost;` differ from `std::cout << "total_cost";`?

<details>
<summary>Example answer</summary>

The first prints the variable's value, for example `75`. The second prints text: the word `total_cost`.

</details>

**5.** In the mission: how does the program "know" that 44 seats are left?

<details>
<summary>Example answer</summary>

It doesn't know in advance. It calculates it from two variables: the number of seats in the hall (50) minus the number of tickets sold (6). When either of them changes, the result changes too.

</details>

## Summary

- In quotes, digits are just text. Without quotes, `3 + 4` is an **expression** that the program **calculates**.
- A **variable** is a named value of a given type. `int` holds whole numbers.
- A declaration with initialisation: `int ticket_count{3};`. Every variable in the course gets its value right away.
- You use variables in expressions with `+`, `-` and `*`, and you can store the result in a new variable.
- Several `<<` in one statement send items to `std::cout` one after another: texts and values.
- Each value written once, under a good name, means one change in the code when the value changes.

## What's next

In this lesson, every variable got its value once, when it was created. In [lesson 2.2](lesson_02_when_values_change.en.md), values will start to change while the program runs.

---

## Example solutions

Look here **after your own attempt**. Your variable names may differ and still be good, as long as they say what the value means.

<details>
<summary>Section 5: the changed program</summary>

<!-- example: first_variables_changed -->
```cpp
#include <iostream>

int main() {
    int ticket_count{5};
    int ticket_price{25};
    int total_cost{ticket_count * ticket_price};

    std::cout << "Tickets: " << ticket_count << "\n";
    std::cout << "Price per ticket: " << ticket_price << "\n";
    std::cout << "Total cost: " << total_cost << "\n";
}
```

</details>

<details>
<summary>Section 6: the area of a room</summary>

<!-- example: room_area -->
```cpp
#include <iostream>

int main() {
    int room_width{4};
    int room_length{5};
    int room_area{room_width * room_length};

    std::cout << "Area: " << room_area << " square metres\n";
}
```

The area is the width times the length, and the result becomes the starting value of `room_area` right away.

</details>

<details>
<summary>Section 7: the mission, the box office</summary>

<!-- example: ticket_office -->
```cpp
#include <iostream>

int main() {
    int hall_seats{50};
    int ticket_price{40};
    int tickets_sold{6};
    int total{tickets_sold * ticket_price};
    int seats_left{hall_seats - tickets_sold};

    std::cout << "Tickets sold: " << tickets_sold << "\n";
    std::cout << "Price per ticket: " << ticket_price << "\n";
    std::cout << "Total: " << total << "\n";
    std::cout << "Seats left: " << seats_left << "\n";
}
```

- The data from the task are three variables: `hall_seats`, `ticket_price` and `tickets_sold`.
- The results are two variables calculated from the data: `total` and `seats_left`.
- `hall_seats` isn't printed, but it's needed for the calculation.

</details>

<details>
<summary>Section 7: the variant</summary>

<!-- example: ticket_office_variant -->
```cpp
#include <iostream>

int main() {
    int hall_seats{50};
    int ticket_price{40};
    int tickets_sold{9};
    int total{tickets_sold * ticket_price};
    int seats_left{hall_seats - tickets_sold};

    std::cout << "Tickets sold: " << tickets_sold << "\n";
    std::cout << "Price per ticket: " << ticket_price << "\n";
    std::cout << "Total: " << total << "\n";
    std::cout << "Seats left: " << seats_left << "\n";
}
```

Only one number changed: `tickets_sold{9}`. The program calculated both results itself.

</details>

**Previous lesson:** [Lesson 1.6: From an idea to a working program, on your own](../module_01_first_programs/lesson_06_from_idea_to_working_program.en.md) · **Next lesson:** [Lesson 2.2: When values change](lesson_02_when_values_change.en.md) · [Course overview](../../README.en.md)

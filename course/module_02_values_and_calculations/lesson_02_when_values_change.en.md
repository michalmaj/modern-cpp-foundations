# Lesson 2.2: When values change

[Polski](lesson_02_when_values_change.md) · **English** · [Course overview](../../README.en.md)

> **Module 2, lesson 2** · about 60 minutes
> **You need:** the `cpp-workspace` folder and the original `lesson_05_first_program` project, as before.
> **Pilot version.** The examples in this lesson are checked automatically on Windows, Ubuntu and macOS.

## Before you start

This lesson assumes that after lesson 2.1:

- you create `int` variables with a starting value, for example `int ticket_count{3};`;
- you use them in calculations with `+`, `-` and `*`;
- you print text and values in one statement, with several `<<`.

## The situation

In lesson 2.1, every variable got its value once, when it was created, and never changed it afterwards. Real programs often keep track of something that changes: the number of free seats, points in a game, the state of a counter. Today you'll change the value of an existing variable, learn to predict values step by step, and mark the values that should **not** change.

After this lesson you will:

- tell the initialisation of a variable apart from a later assignment;
- explain what `=` does in the statement `count = count + 1;`;
- predict the values of variables after a sequence of statements, and write them in a table;
- know that after assigning one `int` variable to another, both stay independent;
- create `const int` constants, and understand why they can't be changed later;
- write a program on your own in which values change in a given order.

## 1. Prepare the project

In `cpp-workspace`, create a folder `lesson_2_2` and copy `main.cpp` and `CMakeLists.txt` into it from the original `lesson_05_first_program`. You type the programs of this lesson into that folder's `main.cpp`.

## 2. A value changes

Replace the content of `main.cpp` with this program:

<!-- example: seats_left -->
```cpp
#include <iostream>

int main() {
    int seats_left{12};
    std::cout << "Seats left: " << seats_left << "\n";

    seats_left = seats_left - 3;
    std::cout << "Seats left: " << seats_left << "\n";
}
```

**Predict** what both `std::cout` lines will print. Write your answer down, then run the program.

<details>
<summary>The program's output</summary>

<!-- output: seats_left -->
```text
Seats left: 12
Seats left: 9
```

</details>

**What happened, line by line?**

1. `int seats_left{12};` is the **declaration with initialisation** you know from lesson 2.1. It creates the variable `seats_left` with the starting value `12`.
2. The first `std::cout` prints the current value: `12`.
3. `seats_left = seats_left - 3;` is an **assignment**. There's no type `int` at the start, so no new variable is created: the value of the existing one changes.
4. The second `std::cout` prints the new value: `9`.

**How to read `=` in an assignment.** In maths, `x = x - 3` would be an equation with no solution. In C++, `=` isn't an equation and compares nothing. It's an **instruction** in two steps:

1. first the program **calculates the right-hand side**: it takes the current value of `seats_left` (12) and subtracts 3, which gives 9;
2. then it **stores the result** in the variable on the left. The previous value, 12, is replaced.

So read it as "`seats_left` gets the value `seats_left - 3`", not "`seats_left` equals …". Checking whether two values are equal is a separate notation that you'll meet in Module 3.

**Order matters.** Statements run from top to bottom, as in Module 1. The first `std::cout` stands before the assignment, so it prints the old value. If both `std::cout` lines stood below the assignment, both would print `9`.

## 3. Initialisation vs. assignment

| Code | What it does |
|---|---|
| `int count{3};` | **Declaration with initialisation:** creates a new variable `count` and gives it a starting value. |
| `count = 5;` | **Assignment:** changes the value of the variable `count`, which already exists. No type is written here. |

You declare a variable **once**. What happens if you try to "change the value" with a second declaration? **Predict**, then build this program:

<!-- broken: redefinition at=5:9 errors=1 error=^redefinition of 'count'$ -->
```cpp
#include <iostream>

int main() {
    int count{3};
    int count{5};
    std::cout << count << "\n";
}
```

The compiler reports `redefinition of 'count'` in line 5, and an extra `note:` line points to where it was first declared. In one `main`, a variable's name can be declared only once. The second declaration would try to create a second variable with the same name, not change the first one.

Fix the program: in line 5, delete `int` and the braces, so that it becomes the assignment `count = 5;`. Build and run it again.

<details>
<summary>The fixed program and its output</summary>

<!-- example: count_assignment -->
```cpp
#include <iostream>

int main() {
    int count{3};
    count = 5;
    std::cout << count << "\n";
}
```

<!-- output: count_assignment -->
```text
5
```

</details>

As in lesson 2.1, a variable always gets its value right at its declaration. An assignment doesn't replace initialisation: it changes a value that is already there.

## 4. Predict: two independent variables

In this program, the variable `second` first gets the value of the variable `first`, and then `first` changes.

<!-- example: two_variables -->
```cpp
#include <iostream>

int main() {
    int first{4};
    int second{0};

    second = first;
    first = 9;

    std::cout << "first: " << first << "\n";
    std::cout << "second: " << second << "\n";
}
```

**Predict** before you run the program: what value will `first` print, and what will `second` print? Write both down.

<details>
<summary>The program's output</summary>

<!-- output: two_variables -->
```text
first: 9
second: 4
```

</details>

**Why does `second` still have `4`?** The assignment `second = first;` takes the **value** that `first` has **at that moment** (4), and stores a copy of it in `second`. The variables are not linked. When `first` then gets 9, `second` doesn't "know" about it: it still holds its copy, 4. This is how `int` variables like these behave.

## 5. Trace the values step by step

Here's a program with several assignments. It prints only the final values:

<!-- example: trace_final -->
```cpp
#include <iostream>

int main() {
    int points{10};
    int bonus{5};

    points = points + bonus;
    bonus = bonus * 2;
    points = points - bonus;
    bonus = points + 1;

    std::cout << "points: " << points << ", bonus: " << bonus << "\n";
}
```

**Step 1. Predict on paper.** Copy the table and fill it in **before** you run the program. In each row, write the values of both variables **after** that line has run.

| Line | `points` | `bonus` |
|---|---|---|
| `int points{10};` and `int bonus{5};` | 10 | 5 |
| `points = points + bonus;` | | |
| `bonus = bonus * 2;` | | |
| `points = points - bonus;` | | |
| `bonus = points + 1;` | | |

Remember: in each assignment, the right-hand side uses the values **from the previous row**.

**Step 2. Check.** Run the program, and compare the last row of the table with the output.

**Step 3. Check every step.** In the program, below each assignment, add a `std::cout` statement that prints both values in the same form as the program's last line. Run the program, and compare each printed line with the table. If one doesn't match, find the first such line, and check which value was used to calculate the right-hand side.

Tracing values like this is a skill programmers use all the time. It will be useful in later lessons more than once.

## 6. Values that don't change: `const`

A car park has 20 spaces. The number of **free** spaces changes all day, but the car park's **capacity** doesn't. If the program assigned a new value to the capacity by mistake, every calculation that uses it would be wrong.

C++ lets you mark such a value as a **constant** with the word `const`:

<!-- example: parking_const -->
```cpp
#include <iostream>

int main() {
    const int parking_capacity{20};
    int available_spaces{12};

    int occupied_spaces{parking_capacity - available_spaces};

    std::cout << "Capacity: " << parking_capacity << "\n";
    std::cout << "Occupied: " << occupied_spaces << "\n";
}
```

<!-- output: parking_const -->
```text
Capacity: 20
Occupied: 8
```

- `const int parking_capacity{20};` creates an `int` variable whose value **can't be changed** after initialisation. The word `const` stands before the type.
- `available_spaces` has no `const`, because its value is meant to change.
- You can **read** a constant and use it in calculations, like any variable: here in `parking_capacity - available_spaces`.
- A constant must get its value **right away**, at the declaration. It can't be given one later.

**When `const`?** When a value shouldn't change while the program runs. In lesson 2.1 no variable changed, so all of them could have had `const`. From now on, mark the values that must stay the same this way. The compiler will make sure nothing changes them by mistake.

### Experiment: try to change a constant

Someone wants to make the car park bigger, and adds an assignment:

<!-- broken: const_assignment at=5 errors=1 error=^cannot assign to variable 'parking_capacity' with const-qualified type 'const int'$ -->
```cpp
#include <iostream>

int main() {
    const int parking_capacity{20};
    parking_capacity = 25;
    std::cout << "Capacity: " << parking_capacity << "\n";
}
```

1. **Predict:** will this program build?
2. Build it.
3. Find the first relevant piece of information in the build output.
4. Explain the cause in your own words.
5. Restore the correct code: delete the line with the assignment.

<details>
<summary>Explanation: read it after your own attempt</summary>

The program doesn't build. In line 5, the compiler reports `cannot assign to variable 'parking_capacity' with const-qualified type 'const int'`: you can't assign a value to a variable whose type has `const`. A `note:` line points to the declaration with `const`. This is the protection that the word `const` asked for: the compiler didn't allow a value that was meant to stay constant to change. If the car park's capacity really should be different, change its starting value in the declaration.

</details>

The same goes for a constant without a starting value. This program doesn't build either:

<!-- broken: const_without_value at=4 errors=1 error=^default initialization of an object of const type 'const int'$ -->
```cpp
#include <iostream>

int main() {
    const int parking_capacity;
    std::cout << "Capacity: " << parking_capacity << "\n";
}
```

The compiler reports `default initialization of an object of const type 'const int'`: the constant got no value. A constant must get it at the declaration, because it can't be given one later.

## 7. Mission: a car park through the day

A small car park has 20 spaces and is empty in the morning. During the day:

- in the morning, 7 cars arrive;
- at noon, 4 more arrive;
- in the afternoon, 6 cars leave.

In `cpp-workspace`, create a folder `parking_day`, copy `CMakeLists.txt` into it from the original `lesson_05_first_program`, create an empty `main.cpp`, and write the program yourself. The program must print exactly:

<!-- output: parking_day -->
```text
Capacity: 20
Free spaces at opening: 20
Free spaces after the morning: 13
Free spaces after noon: 9
Free spaces after the afternoon: 15
Capacity at closing: 20
```

### Success criteria

- The program builds as C++20 and prints exactly the output above.
- The car park's capacity is a `const int`.
- The number of free spaces is an ordinary `int` variable, with a starting value at its declaration, changed by **assignment** after each event.
- **The program calculates** the values 13, 9 and 15: they don't appear in the code.
- The events happen in the given order, and the output is printed after each of them.
- The program uses only what you already know: `int`, `const`, `{}`, `=`, `+`, `-`, `*` and `std::cout`.
- You can explain why the capacity has `const` and the number of free spaces doesn't.

Once the output matches, you can save the project in Git, as in lesson 1.5.

<details>
<summary>Hint 1</summary>

Which value must stay the same all day, and which one changes? That decides where you use `const`.

</details>

<details>
<summary>Hint 2</summary>

Each event is one assignment to the number of free spaces, followed by one `std::cout`. Cars arriving decrease the number of free spaces, and cars leaving increase it.

</details>

### Variant: a different morning

In the morning, 8 cars arrive instead of 7. **Predict** the three new values of free spaces, then change **one number** in the program, build it and run it. The output must be:

<!-- output: parking_day_variant -->
```text
Capacity: 20
Free spaces at opening: 20
Free spaces after the morning: 12
Free spaces after noon: 8
Free spaces after the afternoon: 14
Capacity at closing: 20
```

Example solutions are in [Example solutions](#example-solutions).

## 8. When something goes differently

| What you see | What it means | What to do |
|---|---|---|
| `redefinition of '…'` | The same name was declared a second time, with a type at the start. | To change the value of an existing variable, use an assignment without a type: `count = 5;`. |
| `cannot assign to variable '…' with const-qualified type …` | You're trying to change a constant. | If the value is meant to change, remove `const` from the declaration. If not, remove the assignment. |
| `use of undeclared identifier '…'` on an assignment | The assignment stands above the declaration, or the name has a typo. | Declare the variable first, then assign to it. Compare the names character by character. |
| A printed value is "one step" too old or too new | `std::cout` is in the wrong place relative to the assignment. | Statements run from top to bottom. Move `std::cout` below the assignment whose result it should show. |
| A value doesn't change, although there's a line with a subtraction, for example `seats_left - 3;` | The program calculates the result but doesn't store it anywhere. The compiler may print a warning (`warning`) about it. | Store the result with an assignment: `seats_left = seats_left - 3;`. |
| Changing one variable didn't "carry over" to another | That's expected: assignment copies the value (section 4). | If the second variable should get the new value, assign it again after the change. |

## 9. Explain

Answer in your own words, preferably in writing. Only then compare with the example answer.

**1.** How does `int count{3};` differ from `count = 5;`?

<details>
<summary>Example answer</summary>

The first creates a new variable `count` with the starting value 3. The second changes the value of the existing variable to 5.

</details>

**2.** What exactly does the program do when it runs `count = count + 1;`?

<details>
<summary>Example answer</summary>

First it calculates the right-hand side: it takes the current value of `count` and adds 1. Then it stores the result in `count`, and the previous value is gone. It's not an equation, it's an instruction.

</details>

**3.** Why does `second` have `4` in section 4, although `first` ends up with `9`?

<details>
<summary>Example answer</summary>

Because `second = first;` copied the value that `first` had at that moment, which was 4. Changing `first` later doesn't change `second`.

</details>

**4.** In the mission: why does the capacity have `const`, and the number of free spaces doesn't?

<details>
<summary>Example answer</summary>

The car park's capacity is the same all day, and `const` means the compiler won't let it be changed by mistake. The number of free spaces has to change after every event, so it can't be a constant.

</details>

**5.** How can you check that the predictions in the section 5 table are right for every step, not just for the final result?

<details>
<summary>Example answer</summary>

Add a `std::cout` below each assignment that prints the current values, and compare each printed line with the matching row of the table. The first line that doesn't match shows where the prediction went wrong.

</details>

## Summary

- **Initialisation** (`int count{3};`) creates a variable and gives it a starting value. **Assignment** (`count = 5;`) changes the value of a variable that already exists.
- `=` in an assignment isn't an equation: first the right-hand side is calculated, then the result goes into the variable on the left.
- Statements run in order. A variable's value depends on which assignments have already run.
- Assigning one `int` variable to another copies the value. The variables stay independent.
- `const` marks a value that can't change after initialisation. You can read a constant, but you can't assign it a new value, and the compiler makes sure of it.
- A table of values and extra `std::cout` lines help you check what the program does step by step.

## What's next

You can now predict and check how values change step by step. **Lesson 2.3 is in preparation.**

---

## Example solutions

Look here **after your own attempt**. Your names and the form of the printed lines may differ, as long as the output is as required.

<details>
<summary>Section 5: the table, and the program that prints every step</summary>

| Line | `points` | `bonus` |
|---|---|---|
| `int points{10};` and `int bonus{5};` | 10 | 5 |
| `points = points + bonus;` | 15 | 5 |
| `bonus = bonus * 2;` | 15 | 10 |
| `points = points - bonus;` | 5 | 10 |
| `bonus = points + 1;` | 5 | 6 |

<!-- example: trace_steps -->
```cpp
#include <iostream>

int main() {
    int points{10};
    int bonus{5};

    points = points + bonus;
    std::cout << "points: " << points << ", bonus: " << bonus << "\n";
    bonus = bonus * 2;
    std::cout << "points: " << points << ", bonus: " << bonus << "\n";
    points = points - bonus;
    std::cout << "points: " << points << ", bonus: " << bonus << "\n";
    bonus = points + 1;
    std::cout << "points: " << points << ", bonus: " << bonus << "\n";
}
```

<!-- output: trace_steps -->
```text
points: 15, bonus: 5
points: 15, bonus: 10
points: 5, bonus: 10
points: 5, bonus: 6
```

The last line is the output of the original program:

<!-- output: trace_final -->
```text
points: 5, bonus: 6
```

The most common mistake is using the old value of `bonus` (5) in the third assignment, instead of the already changed one (10).

</details>

<details>
<summary>Section 7: the mission, a car park through the day</summary>

<!-- example: parking_day -->
```cpp
#include <iostream>

int main() {
    const int parking_capacity{20};
    int free_spaces{parking_capacity};

    std::cout << "Capacity: " << parking_capacity << "\n";
    std::cout << "Free spaces at opening: " << free_spaces << "\n";

    free_spaces = free_spaces - 7;
    std::cout << "Free spaces after the morning: " << free_spaces << "\n";

    free_spaces = free_spaces - 4;
    std::cout << "Free spaces after noon: " << free_spaces << "\n";

    free_spaces = free_spaces + 6;
    std::cout << "Free spaces after the afternoon: " << free_spaces << "\n";

    std::cout << "Capacity at closing: " << parking_capacity << "\n";
}
```

- The capacity doesn't change, so it has `const`.
- The car park is empty in the morning, so `free_spaces` starts from the capacity's value, rather than from the number 20 typed a second time.
- Each event is one assignment. Arriving subtracts, leaving adds.

</details>

<details>
<summary>Section 7: the variant</summary>

<!-- example: parking_day_variant -->
```cpp
#include <iostream>

int main() {
    const int parking_capacity{20};
    int free_spaces{parking_capacity};

    std::cout << "Capacity: " << parking_capacity << "\n";
    std::cout << "Free spaces at opening: " << free_spaces << "\n";

    free_spaces = free_spaces - 8;
    std::cout << "Free spaces after the morning: " << free_spaces << "\n";

    free_spaces = free_spaces - 4;
    std::cout << "Free spaces after noon: " << free_spaces << "\n";

    free_spaces = free_spaces + 6;
    std::cout << "Free spaces after the afternoon: " << free_spaces << "\n";

    std::cout << "Capacity at closing: " << parking_capacity << "\n";
}
```

Only the number in the morning assignment changed. The program calculated the next values from the new value, because each assignment uses the previous one.

</details>

**Previous lesson:** [Lesson 2.1: Values the program remembers](lesson_01_values_the_program_remembers.en.md) · **Next lesson:** in preparation · [Course overview](../../README.en.md)

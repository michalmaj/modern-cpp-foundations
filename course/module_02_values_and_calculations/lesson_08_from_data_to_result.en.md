# Lesson 2.8: From data to result (the Module 2 test)

[Polski](lesson_08_from_data_to_result.md) · **English** · [Course overview](../../README.en.md)

> **Module 2, lesson 8: the test** · about 90 minutes, which you can split into two sessions
> **You need:** the `cpp-workspace` folder with the Git repository from lesson 1.5, and the original `lesson_05_first_program` project.
> **Pilot version.** The reference solutions in this lesson are checked automatically on Windows, Ubuntu and macOS, with the given input data. Nothing grades your work automatically: you check it yourself, against the criteria.

## How this test works

This lesson introduces nothing new. You check whether you can, on your own, design a program that takes data from the user, stores it in well-chosen variables, calculates, and prints a result. On top of that, you diagnose two short reports and explain your own decisions.

The lesson has two parts:

- **Part A: the test.** Requirements, test data, expected results, questions and criteria. No hints and no solution code. Everything you need, you know from lessons 2.1–2.7 and from Module 1.
- **Part B: checking and discussion.** How to check, hints, example solutions, explanations and a self-assessment. Go there after finishing part A, or when you knowingly decide to stop trying on your own.

Looking at part B, at earlier lessons or at your notes isn't a failure. What matters is to **note honestly what was done on your own and what with help**. The self-assessment at the end makes that distinction. You can split the test into two sessions, for example task 1 on one day and tasks 2 and 3 on the next.

**You may use:**

- CLion, or the terminal, CMake and Ninja, as before;
- the `CMakeLists.txt` copied from the original `lesson_05_first_program`;
- the debugger from lesson 2.3, if it works in your environment, or a table of values and temporary `std::cout` statements;
- Git, if you want to save the finished work.

In all tasks we assume **correct input data**, like the data given. The programs don't need to check the data or react to bad data.

---

# Part A: the test

## Task 1: A route plan

The organisers are preparing a walking route. To mark the route they use markers, which are packed **6 to a pack**. Write a program that helps them plan the route.

**Preparation:**

- In `cpp-workspace`, create a new folder `route_plan`.
- Copy `CMakeLists.txt` into it from the original `lesson_05_first_program`.
- Create an **empty** `main.cpp` in it and write the whole program on your own. Don't copy programs from earlier lessons.

**Input data**, in this order, each value on its own line:

1. the name of the route, which can contain spaces;
2. the number of laps, a whole number;
3. the length of one lap in kilometres, a number with a fractional part;
4. the number of available markers, a whole number.

**The program calculates:**

- the total distance: the number of laps times the lap length;
- the number of full packs of 6 markers that can be made from the available markers;
- the number of markers left over outside the full packs.

**Requirements:**

- Before each read, the program prints a request for the data, and at the end a report, exactly as in the examples below.
- The number of markers in a pack, 6, is a `const int` constant in the program.
- The first line of the report, `Route: …`, is text **built by joining** `std::string` values and stored in a variable before the program prints it.
- The same program, without changing the code and without building it again, gives the correct result for both sets of data.

**The first set of data:**

<!-- input: route_plan -->
```text
Forest Loop
4
1.25
29
```

The standard output must be exactly:

<!-- output: route_plan -->
```text
Enter route name:
Enter number of laps:
Enter lap length in km:
Enter number of markers:
Route: Forest Loop
Total distance: 5 km
Full marker packs: 4
Markers left: 5
```

**The second set of data,** in a second run of the same program:

<!-- input: route_plan -->
```text
City Evening Walk
3
2.5
30
```

<!-- output: route_plan -->
```text
Enter route name:
Enter number of laps:
Enter lap length in km:
Enter number of markers:
Route: City Evening Walk
Total distance: 7.5 km
Full marker packs: 5
Markers left: 0
```

On the screen you'll also see the data you typed between the program's lines: that's echo, not standard output (lesson 2.6). The program prints the distance 5.0 km as `5` (lesson 2.5).

Once the output matches, you can save the project in Git, as in lesson 1.5. Before committing, check `git status`: only `main.cpp` and `CMakeLists.txt` go into the history, with no build folders.

## Task 2: Two reports

In `cpp-workspace`, create a folder `diagnosis_2` and copy `main.cpp` and `CMakeLists.txt` into it from the original `lesson_05_first_program`. Type each of the programs below in turn into that folder's `main.cpp`. Both build and run, but give a wrong result.

**Report A.** The program should print the full name of an event given by the user:

<!-- example: event_name_bug -->
```cpp
#include <iostream>
#include <string>

int main() {
    std::string event_name{""};

    std::cout << "Enter event name:\n";
    std::cin >> event_name;

    std::cout << "Event: " << event_name << "\n";
}
```

For this data:

<!-- input: event_name_fixed -->
```text
Spring Science Fair
```

the standard output should be:

<!-- output: event_name_fixed -->
```text
Enter event name:
Event: Spring Science Fair
```

**Report B.** The program should convert a number of minutes into full hours and remaining minutes:

<!-- example: time_bug -->
```cpp
#include <iostream>

int main() {
    const int minutes_per_hour{60};
    int total_minutes{0};

    std::cout << "Enter total minutes:\n";
    std::cin >> total_minutes;

    const int hours{total_minutes % minutes_per_hour};
    const int minutes{total_minutes % minutes_per_hour};

    std::cout << "Time: " << hours << " h " << minutes << " min\n";
}
```

The test data is `135` and `200`. **Predict** the correct result for both, and only then compare it with the expected one:

<!-- input: time_fixed -->
```text
135
```

<details>
<summary>The expected standard output for 135</summary>

<!-- output: time_fixed -->
```text
Enter total minutes:
Time: 2 h 15 min
```

</details>

<!-- input: time_fixed -->
```text
200
```

<details>
<summary>The expected standard output for 200</summary>

<!-- output: time_fixed -->
```text
Enter total minutes:
Time: 3 h 20 min
```

</details>

**For each report:**

1. Run the program with the given data and write down what it really prints.
2. Compare it with the expected result.
3. Find the statement that gives the wrong result. You can use the debugger, if it has worked for you since lesson 2.3, or a table of values and temporary `std::cout` statements.
4. Explain the cause in one sentence.
5. Fix the program with one change.
6. Check that after the fix the result is as expected. Remove any temporary `std::cout` statements you added.

Write the results in a table:

| Report | Actual result | The statement that gives the wrong result | Cause | Fix | Check |
|---|---|---|---|---|---|
| A | | | | | |
| B | | | | | |

You don't need to save the `diagnosis_2` project in Git.

## Task 3: Explain

Answer briefly, in writing, referring to your own program from task 1:

1. Why is the route name stored in a `std::string`?
2. Why do you read the route name with `std::getline` and not with `>>`? Why does that read come before the reads of the numbers?
3. Why is the lap length of type `double`, and the number of laps `int`?
4. Why are `/` and `%` suitable for calculating the full packs and the markers left over?
5. Why can the number of markers in a pack be `const`, while the number of available markers can't?
6. What type would a variable have if it were initialised with `auto` from the expression that calculates the total distance in your program? How do you know?
7. Why does the same program give different results for the two sets of data, without being built again?

## Success criteria

The test is passed when you meet **all** the criteria:

- `route_plan/main.cpp` was written from an empty file, in correct C++20. The program builds without errors.
- The data types follow from their meaning: text in a `std::string`, whole numbers in an `int`, a quantity with a fractional part in a `double`. Every variable has a starting value.
- The route name with spaces is read in full with `std::getline`, **before** the numbers are read with `>>`.
- The total distance is calculated with a `double` taking part, and the full packs and the markers left over with `/` and `%`.
- The number of markers in a pack is a `const int` constant. Values that don't change after they are calculated can be constants too.
- The first line of the report is text built by joining `std::string` values and stored in a variable.
- The standard output for **both** sets of data is exactly as in task 1, and the code doesn't change between the runs.
- Both reports in task 2 were diagnosed and fixed: the actual result, the statement, the cause, one fix and a check.
- You can explain every line of your program and answer the questions in task 3.

Variable names may differ from those in the example solution, as long as they are readable and say what the value means. A correct result is a necessary condition, but **not proof of understanding**: a program can work even though someone doesn't understand why. That's why task 3 is part of the test.

---

# Part B: checking and discussion

Go here after finishing part A, or when you knowingly decide to stop trying on your own.

## How to check your work

- **Standard output:** run the program twice, once with each set of data. Compare the program's lines with the expected ones character by character. Ignore the data you typed, which you see thanks to echo.
- **The same program:** don't change the code between the runs. In the terminal you can run the same executable twice, as in lesson 2.6, section 3.
- **The calculations by hand:** 4 · 1.25 = 5 and 3 · 2.5 = 7.5. 29 markers make 4 packs of 6 (24) with 5 left over. 30 make 5 packs with 0 left over.
- **The types and the order of reads:** go through the declarations. For each variable, say why it has that type and whether it can be `const`.
- **Git, if you saved the work:** `git status` shows no `route_plan` files, and `git ls-files route_plan` shows only `CMakeLists.txt` and `main.cpp`.

## Hints

Each hint is about the way of thinking. Open them in order, and only when you need them.

<details>
<summary>Task 1, hint 1: where to start?</summary>

With a list of the data and their types: what is text, what is a whole number, and what is a number with a fractional part? Then the order from lessons 2.6 and 2.7: the variables for the data, a request and a read for each value, and finally the calculations and the report.

</details>

<details>
<summary>Task 1, hint 2: the reads</summary>

The route name has spaces, so `>>` would read only its first word. Which method reads a whole line, and why must it come first (lesson 2.7, section 8)?

</details>

<details>
<summary>Task 1, hint 3: the calculations</summary>

The distance: `int` times `double` gives `double` (lesson 2.5), so the result's type must fit `{}`. The packs: "how many full groups?" and "how many are left?" are questions for `/` and `%` (lesson 2.4). Build the text `Route: …` with `+` from a literal and the route name (lesson 2.7).

</details>

<details>
<summary>Task 2, report A</summary>

Compare the actual result with the expected one: which part of the name is missing? What ends a read with `>>` into a `std::string`?

</details>

<details>
<summary>Task 2, report B</summary>

For 135 minutes, the number of hours and the number of minutes are the same. Which of the two calculations gives the number of full groups, and which the remainder?

</details>

## Example solutions

<details>
<summary>Task 1: the route plan</summary>

<!-- example: route_plan -->
```cpp
#include <iostream>
#include <string>

int main() {
    const int markers_per_pack{6};

    std::string route_name{""};
    int laps{0};
    double lap_length_km{0.0};
    int markers{0};

    std::cout << "Enter route name:\n";
    std::getline(std::cin, route_name);
    std::cout << "Enter number of laps:\n";
    std::cin >> laps;
    std::cout << "Enter lap length in km:\n";
    std::cin >> lap_length_km;
    std::cout << "Enter number of markers:\n";
    std::cin >> markers;

    const double total_distance_km{laps * lap_length_km};
    const int full_packs{markers / markers_per_pack};
    const int markers_left{markers % markers_per_pack};
    const std::string title{"Route: " + route_name};

    std::cout << title << "\n";
    std::cout << "Total distance: " << total_distance_km << " km\n";
    std::cout << "Full marker packs: " << full_packs << "\n";
    std::cout << "Markers left: " << markers_left << "\n";
}
```

- **Types:** the route name is text with spaces, so `std::string`. Laps and markers are counted whole, so `int`. A lap length can have a fractional part, so `double`. The variables for the data have starting values and aren't `const`, because reading changes them.
- **Reads:** `std::getline` comes first, so the name is read in full, and the `>>` reads after it have no problem with a line ending.
- **Calculations:** `laps * lap_length_km` is an `int` times a `double`, so the result is a `double` and fits `const double`. `markers / markers_per_pack` and `markers % markers_per_pack` are integer division and the remainder: the full packs and what is left over. The calculations come after the reads and don't change, so they are constants.
- **Text:** `"Route: " + route_name` is a literal plus a `std::string`, so the result is `std::string` text, stored in the constant `title`.

</details>

<details>
<summary>Task 2, report A: the result before the fix, and the fixed program</summary>

Before the fix, for the same data:

<!-- input: event_name_bug -->
```text
Spring Science Fair
```

<!-- output: event_name_bug -->
```text
Enter event name:
Event: Spring
```

- **The statement:** `std::cin >> event_name;`.
- **The cause:** `>>` reads one word into a `std::string` and stops at a space. A `std::string` can hold spaces, but this read method doesn't bring them in.
- **The fix:** read the whole line with `std::getline`:

<!-- example: event_name_fixed -->
```cpp
#include <iostream>
#include <string>

int main() {
    std::string event_name{""};

    std::cout << "Enter event name:\n";
    std::getline(std::cin, event_name);

    std::cout << "Event: " << event_name << "\n";
}
```

</details>

<details>
<summary>Task 2, report B: the result before the fix, and the fixed program</summary>

Before the fix:

<!-- input: time_bug -->
```text
135
```

<!-- output: time_bug -->
```text
Enter total minutes:
Time: 15 h 15 min
```

<!-- input: time_bug -->
```text
200
```

<!-- output: time_bug -->
```text
Enter total minutes:
Time: 20 h 20 min
```

- **The statement:** `const int hours{total_minutes % minutes_per_hour};`.
- **The cause:** the hours are the number of full groups of 60 minutes, which is integer division, `/`. `%` gives the remainder, and the remainder is the minutes, so both values come out the same. A table of values, or a `std::cout` after this statement, shows 15 instead of the expected 2.
- **The fix:** in the calculation of the hours, replace `%` with `/`:

<!-- example: time_fixed -->
```cpp
#include <iostream>

int main() {
    const int minutes_per_hour{60};
    int total_minutes{0};

    std::cout << "Enter total minutes:\n";
    std::cin >> total_minutes;

    const int hours{total_minutes / minutes_per_hour};
    const int minutes{total_minutes % minutes_per_hour};

    std::cout << "Time: " << hours << " h " << minutes << " min\n";
}
```

The check: 2 · 60 + 15 = 135 and 3 · 60 + 20 = 200.

</details>

## Example answers to task 3

<details>
<summary>Show the example answers</summary>

1. Because the route name is text that can consist of several words. `int` and `double` store only numbers.
2. Because `>>` would read only the first word, while `std::getline` reads the whole line with its spaces. It comes before the reads of the numbers because after `>>` a line ending stays in the input, and a `std::getline` called afterwards could read an empty text.
3. Because the lap length is a measurement that can have a fractional part, for example 1.25 km. There is always a whole number of laps.
4. Because `/` on two whole numbers gives the number of full groups of 6, and `%` gives the remainder: the markers that don't fit into any full pack.
5. Because a pack always has 6 markers: that value doesn't change while the program runs, and `const` makes sure nothing changes it by mistake. The program reads the number of available markers from the user, so it has to be an ordinary variable.
6. `double`, because the expression is the number of laps (`int`) times the lap length (`double`), and `int` times `double` gives `double`. `auto` works out the type from the starting value.
7. Because the data isn't written in the code: the program reads it from standard input every time it runs. The data changes, while the code and the executable stay the same.

</details>

## Self-assessment

For each criterion, mark one answer:

| Criterion | On my own | With a hint | After looking at the solution | To revise |
|---|---|---|---|---|
| Writing the program from an empty `main.cpp` | | | | |
| Choosing the types: `std::string`, `int`, `double` | | | | |
| Reading a name with spaces, and the order `std::getline` before `>>` | | | | |
| Calculating the distance with `double` | | | | |
| Full packs and the remainder with `/` and `%` | | | | |
| `const` for values that don't change | | | | |
| Text built by joining `std::string` values | | | | |
| The exact output for both sets of data, without changing the code | | | | |
| Diagnosing report A | | | | |
| Diagnosing report B | | | | |
| Finding an error with a table of values and a temporary `std::cout` | | | | |
| Using the debugger in CLion (breakpoint, Step Over) | | | | |
| The explanations in task 3 | | | | |

The debugger row is about the **tool**, and the row about the table of values and `std::cout` is about the **technique of finding an error**. The two skills complement each other, but neither replaces the other. If the debugger doesn't work in your environment, leave its row empty and come back to lesson 2.3 once it works.

If something is marked in the "To revise" column, go back to the matching lesson:

| Topic | Lesson |
|---|---|
| variables, starting values and calculations | 2.1 |
| assignment, `const`, the table of values | 2.2 |
| the debugger, and tracing values with `std::cout` | 2.3 |
| `/`, `%` and the order of operations | 2.4 |
| `double`, mixing `int` and `double`, `auto` | 2.5 |
| `std::cin`, standard input and echo | 2.6 |
| `std::string`, joining text, `std::getline` | 2.7 |

Then try the task again, for example with different route data.

---

## Module 2 summary

After eight lessons you can:

- store values in variables of well-chosen types, and change them by assignment while the program runs;
- mark as `const` the values that shouldn't change;
- calculate, and predict the order of operations;
- tell integer division apart from floating-point division, and use `/` and `%`;
- read and use `auto` in simple declarations;
- take data from the user, and run the same program with different data;
- store and join text, and read whole lines;
- analyse how a program runs with a table of values, by printing, or with the debugger, and find simple logic errors.

About the state of the materials: the code and calculations in all Module 2 lessons are checked automatically on three systems. The instructions for using the debugger in CLion remain a pilot: they haven't yet been checked by hand on all three systems.

## What's next: Module 3

So far your programs always execute the same statements, from top to bottom. In Module 3 they'll start **making decisions**: you'll learn comparisons and conditions, which let a program execute different statements depending on the data. Start with [lesson 3.1: The program's first decision (`if`)](../module_03_decisions_and_conditions/lesson_01_the_first_decision.en.md). Module 3 is in development: the further lessons are in preparation.

**Previous lesson:** [Lesson 2.7: Text the program remembers (`std::string`)](lesson_07_text_the_program_remembers.en.md) · **Next lesson:** [Lesson 3.1: The program's first decision (`if`)](../module_03_decisions_and_conditions/lesson_01_the_first_decision.en.md) · [Course overview](../../README.en.md)

# Lesson 5.6: Declaration, definition and linking

[Polski](lesson_06_declaration_and_definition.md) · **English** · [Course overview](../../README.en.md)

> **Module 5, lesson 6** · about 40–55 minutes
> **You need:** the `cpp-workspace` folder and the original `lesson_05_first_program` project, as before. You don't need the debugger in this lesson.
> **Pilot version.** The programs in this lesson are checked automatically on Windows, Ubuntu and macOS, including with the given input data. Typing input into CLion's **Run** window is described without a manual check on every system.

## Before you start

This lesson assumes that you:

- write programs with several cooperating functions, and write helper functions before the functions that use them (lesson 5.5);
- know that calling a function written below `main` ends with the error `use of undeclared identifier` (lesson 5.1);
- remember from lesson 1.4 that building a program has two stages: compiling and linking.

## The situation

So far, every function had to stand in the file before its first call. That works, but it imposes an order: helper functions first, `main` at the end. In this lesson you'll answer two questions. **Can a function be called before its definition appears in the file?** And **why can a program pass compiling and still fail to link?**

After this lesson you will:

- tell a function's declaration from its definition and from a call;
- write a function declaration ending with a semicolon;
- put `main` before the definitions of your own functions;
- check that a declaration matches its definition;
- tell a compile error from a link error, and fix both.

## 1. Prepare the project

In `cpp-workspace`, create a `lesson_5_6` folder and copy `main.cpp` and `CMakeLists.txt` into it from the original `lesson_05_first_program`. You type the programs from sections 2–7 into that folder's `main.cpp`.

## 2. A familiar layout, and one change

You know this layout from lesson 5.5: the function's definition stands before `main`, so the compiler already knows it at the place of the call.

<!-- example: score_definition_first -->
```cpp
#include <iostream>

int double_points(int points) {
    return points * 2;
}

int main() {
    std::cout << "Score: " << double_points(4) << "\n";
}
```

<!-- output: score_definition_first -->
```text
Score: 8
```

Now someone moves the whole definition **below** `main`:

<!-- broken: score_undeclared at=4:31 errors=1 error=^use of undeclared identifier 'double_points' -->
```cpp
#include <iostream>

int main() {
    std::cout << "Score: " << double_points(4) << "\n";
}

int double_points(int points) {
    return points * 2;
}
```

**Predict** whether this program will build. If not, at which stage: compiling or linking? Then try to build it.

<details>
<summary>What the compiler reports, and why</summary>

The program won't build. The compiler reports `use of undeclared identifier 'double_points'` on line 4, as in lesson 5.1. This is a **compile error**: the compiler reads the file from the top, and at the place of the call it doesn't know the name `double_points` yet. The definition stands further down in the same file, but that doesn't make the compiler know the name earlier. Compiling doesn't finish, so linking never starts.

</details>

## 3. A function declaration

To call a function, the compiler doesn't need its body straight away. It's enough for it to know **what kind of function it is**: its name, what it returns and what parameters it takes. A **declaration** gives it that knowledge:

<!-- fragment -->
```cpp
int double_points(int points);
```

| Part | Meaning |
|---|---|
| `int` | the result type |
| `double_points` | the function's name |
| `int points` | a parameter and its type |
| `;` | the end of the declaration: there's no function body here |

A declaration tells the compiler which function can be called. It contains no statements, does no calculation and doesn't replace the function.

A **definition** is a function together with its body, that is, what you've known since lesson 5.1:

<!-- fragment -->
```cpp
int double_points(int points) {
    return points * 2;
}
```

A definition provides the statements that run when the function is called. **A definition is also a declaration**: it too tells the compiler the function's name, what it returns and what it takes. That's why programs with the definitions before `main` worked without separate declarations, and they're still correct.

## 4. The declaration before `main`, the definition below `main`

This program has a declaration before `main` and the definition after it:

<!-- example: score_declaration_first -->
```cpp
#include <iostream>

int double_points(int points);

int main() {
    std::cout << "Score: " << double_points(4) << "\n";
}

int double_points(int points) {
    return points * 2;
}
```

Point out in it: the declaration, `main`, the function call, the definition and the `return` statement. **Predict** whether the program will build, and what it will print.

<details>
<summary>Standard output and explanation</summary>

<!-- output: score_declaration_first -->
```text
Score: 8
```

The result is the same as in section 2. At the place of the call the compiler already knows the function, thanks to the declaration on line 3, so compiling succeeds. The function's body stands further down, in the definition. The declaration ran nothing: at the call, the program runs the statements from the definition.

</details>

**A declaration and a definition must match**, because they describe the same function:

| What | In the declaration | In the definition |
|---|---|---|
| the function's name | `double_points` | `double_points` |
| the result type | `int` | `int` |
| the number of parameters | 1 | 1 |
| the parameter types, in the same order | `int` | `int` |

In a declaration, a parameter's name can be left out. It's still a declaration of the same function:

<!-- fragment -->
```cpp
int double_points(int);
```

In the definition the name is needed, because the function's body refers to the parameter's value. The names in the declaration and the definition don't have to be the same. The types, though, must match. If the parameter types in the declaration and the definition differed, it would no longer be the same function. We don't cover that case in this lesson: keep declarations and definitions matching.

## 5. Several declarations at the start of the file

Declarations let you describe all the functions at the start of the file. The functions from lesson 5.5 could look like this:

<!-- fragment -->
```cpp
int base_price(int weight);
int zone_surcharge(int zone);
int shipping_cost(int weight, int zone);

int main() {
    // reading, checking and the report
}

// the definitions of the three functions
```

In this program two functions cooperate, and the definitions stand below `main`, in any order:

<!-- example: score_two_declarations -->
```cpp
#include <iostream>

int double_points(int points);
int score_with_bonus(int points);

int main() {
    std::cout << "Score: " << score_with_bonus(4) << "\n";
}

int score_with_bonus(int points) {
    return double_points(points) + 5;
}

int double_points(int points) {
    return points * 2;
}
```

**Predict** the result. Notice that `score_with_bonus` calls `double_points`, although `double_points`'s definition stands further down in the file.

<details>
<summary>Standard output and explanation</summary>

<!-- output: score_two_declarations -->
```text
Score: 13
```

`score_with_bonus(4)` calls `double_points(4)`, gets 8 and adds 5. At the place of that call the compiler knows `double_points` from the declaration at the start of the file, so the order of the definitions doesn't matter. The functions still pass values to each other through parameters and `return`. The organisation of the code changed, not how a call works.

</details>

A layout with `main` at the start is **one possible** way to organise a file, not a requirement. Definitions before `main`, as in lesson 5.5, are a good solution too and need no separate declarations.

## 6. Compiling vs linking

In lesson 1.4, building a program had two stages:

- **Compiling:** the compiler checks the source code and translates it into an object file.
- **Linking:** the linker joins the object file with library code and startup code into a program. On the way, it has to find the definitions of the functions the program uses.

A declaration is enough for **the compiler**: thanks to it, the compiler knows the function exists and how to call it. But the called function still needs a **definition**, and **the linker** looks for it.

## 7. Find the bug: a declaration with no definition

In this program the function is declared and called, but there's no definition anywhere:

<!-- broken: score_missing_definition stage=link error=double_points -->
```cpp
#include <iostream>

int double_points(int points);

int main() {
    std::cout << "Score: " << double_points(4) << "\n";
}
```

**Predict** whether the program will build. If not, at which stage, and why? Then try to build it and read the message.

<details>
<summary>What happens, and why</summary>

1. **Compiling succeeds.** At the place of the call the compiler knows the function from the declaration, so there's nothing to report. An object file is created.
2. **Linking fails.** The linker looks for the definition of `double_points`, because `main` calls it, and doesn't find it anywhere.
3. The build ends in failure, and no program to run is created.

The message comes from the linker, not the compiler, and it looks a little different on each system. On Ubuntu the linker writes `undefined reference to 'double_points(int)'`, on macOS `"double_points(int)", referenced from`, and on Windows `undefined symbol: int __cdecl double_points(int)`. At the end there's also `linker command failed`. You don't need to remember these messages. What matters is that they name the function whose definition is missing, and that the error appears **after** compiling.

A declaration without a definition isn't always an error. Here the problem is that the function is **called**, so the program needs its definition.

</details>

**Fix the program:** check that the declaration exists and that the function is called, then add a definition that matches the declaration. Don't remove the call, and don't move the calculation into `main`. Build the program again, run it, and compare the result with section 4. The fixed program is in [Example solutions](#example-solutions).

**Two errors, two stages:**

| Situation | The stage that fails | The cause | The fix |
|---|---|---|---|
| A call with no earlier declaration (section 2) | compiling | the compiler doesn't know the function at the place of the call | add a declaration before the call, or move the definition up |
| A declaration and a call with no definition (section 7) | linking | the called function's definition is missing | add the definition |
| A matching declaration and definition (section 4) | the build succeeds | the function is known and has a definition | |

## 8. Mission: the workshop room plan

The workshop room has 10 places. Two groups report their numbers of participants, and the program checks whether everyone fits.

**Requirements:**

- The program prints `Enter group sizes (0-8):` and reads two whole numbers: the size of the first and of the second group.
- If the read fails, it prints only `Input could not be read`.
- If either number is outside the range 0 to 8, it prints only `Invalid group size`.
- For valid data it prints `Total attendees: N` and one of the lines `Room status: Fits` or `Room status: Too many people`. Exactly 10 people fit; 11 and more don't.
- The program doesn't ask again.
- The program has **at least two own functions**: one works out the total number of people and returns an `int`, the other decides whether the total doesn't exceed the room's capacity and returns a `bool`. **The second function uses the first one's result.** You choose the names of the functions and their parameters.
- The functions print nothing and read nothing. `main` chooses the status message based on the `bool` result: neither `0` nor `1` appears in the report.
- **The file layout:** first `#include`, then the declarations of both functions, then `main`, and finally the definitions of the functions.
- Don't use variables declared outside functions.

In `cpp-workspace`, create a `room_plan` folder, copy `CMakeLists.txt` into it from the original `lesson_05_first_program`, create an empty `main.cpp` and write the program on your own.

For the data `4` and `5`:

<!-- input: room_plan -->
```text
4
5
```

<!-- output: room_plan -->
```text
Enter group sizes (0-8):
Total attendees: 9
Room status: Fits
```

For the data `5` and `5`, exactly at the room's capacity:

<!-- input: room_plan -->
```text
5
5
```

<!-- output: room_plan -->
```text
Enter group sizes (0-8):
Total attendees: 10
Room status: Fits
```

For the data `6` and `5`:

<!-- input: room_plan -->
```text
6
5
```

<!-- output: room_plan -->
```text
Enter group sizes (0-8):
Total attendees: 11
Room status: Too many people
```

**This isn't `double_points` with new names.** In sections 2–7 the function was ready, and only its place in the file changed. Here you have to decide on your own:

1. how to name both functions, what result types and parameters they have, and in what order;
2. how to write declarations that match the definitions;
3. how the second function uses the first one's result;
4. what stays in `main`: reading, checking the data and choosing the message.

**Before you write the program**, prepare a table of test cases: all zeros, one empty group, totals of 9, 10 and 11, both groups at 8, values just outside the range for each group, text instead of the first and instead of the second number, and data that ends after one number. For each case, write down the expected standard output.

Analyse the cases where the data ends early on paper, as in lessons 4.5–5.5, instead of running them, and compare with the collapsed list of check cases. This lesson's program is checked separately for such data, by the course's automatic tests.

### Success criteria

- The program builds as C++20, and its standard output for the three examples above is exactly as shown.
- For every case you can type, the standard output matches the list of check cases. You check the cases where the data ends early by reasoning.
- The file's layout is: `#include`, declarations, `main`, definitions. Every declaration matches its definition.
- The `bool` function uses the `int` function's result, and neither prints or reads anything.
- After a failed read or out-of-range data, `Total attendees` doesn't appear.
- The program doesn't use variables declared outside functions.
- The table of cases was made before running the program.
- You can point out every declaration, every definition and every call in your program.

When the result matches, you can save the project in Git, as in lesson 1.5.

<details>
<summary>Hint 1</summary>

What should the compiler know about both functions before it reaches `main`?

</details>

<details>
<summary>Hint 2</summary>

A declaration gives the name, the result type and the parameter types. A definition also contains the statements the function runs.

</details>

<details>
<summary>Hint 3</summary>

Write the declarations of both functions first, then `main`, and only below that their definitions. Check that the call of one function by the other passes the right arguments.

</details>

<details>
<summary>The full list of check cases: open it after preparing your own table</summary>

| Group 1 | Group 2 | Standard output after the question | What it checks |
|---|---|---|---|
| 4 | 5 | `Total attendees: 9`, `Room status: Fits` | the example in the text |
| 5 | 5 | `Total attendees: 10`, `Room status: Fits` | exactly the room's capacity |
| 6 | 5 | `Total attendees: 11`, `Room status: Too many people` | one person too many |
| 0 | 0 | `Total attendees: 0`, `Room status: Fits` | all zeros |
| 0 | 8 | `Total attendees: 8`, `Room status: Fits` | one empty group |
| 8 | 2 | `Total attendees: 10`, `Room status: Fits` | capacity, the upper limit of group 1 |
| 2 | 8 | `Total attendees: 10`, `Room status: Fits` | capacity, the upper limit of group 2 |
| 8 | 8 | `Total attendees: 16`, `Room status: Too many people` | both groups full |
| -1 | 2 | `Invalid group size` | the first just below the range |
| 2 | -1 | `Invalid group size` | the second just below the range |
| 9 | 0 | `Invalid group size` | the first just above the range |
| 0 | 9 | `Invalid group size` | the second just above the range |
| `abc` | `2` | `Input could not be read` | text instead of the first number |
| `2` | `abc` | `Input could not be read` | text instead of the second number |
| `2` | the end of the data | `Input could not be read` | the data ends after one number |
| no data | no data | `Input could not be read` | the data ends at once |

The first three cases are checked above, with the mission's text.

<!-- input: room_plan -->
```text
0
0
```

<!-- output: room_plan -->
```text
Enter group sizes (0-8):
Total attendees: 0
Room status: Fits
```

<!-- input: room_plan -->
```text
0
8
```

<!-- output: room_plan -->
```text
Enter group sizes (0-8):
Total attendees: 8
Room status: Fits
```

<!-- input: room_plan -->
```text
8
2
```

<!-- output: room_plan -->
```text
Enter group sizes (0-8):
Total attendees: 10
Room status: Fits
```

<!-- input: room_plan -->
```text
2
8
```

<!-- output: room_plan -->
```text
Enter group sizes (0-8):
Total attendees: 10
Room status: Fits
```

<!-- input: room_plan -->
```text
8
8
```

<!-- output: room_plan -->
```text
Enter group sizes (0-8):
Total attendees: 16
Room status: Too many people
```

<!-- input: room_plan -->
```text
-1
2
```

<!-- output: room_plan -->
```text
Enter group sizes (0-8):
Invalid group size
```

<!-- input: room_plan -->
```text
2
-1
```

<!-- output: room_plan -->
```text
Enter group sizes (0-8):
Invalid group size
```

<!-- input: room_plan -->
```text
9
0
```

<!-- output: room_plan -->
```text
Enter group sizes (0-8):
Invalid group size
```

<!-- input: room_plan -->
```text
0
9
```

<!-- output: room_plan -->
```text
Enter group sizes (0-8):
Invalid group size
```

<!-- input: room_plan -->
```text
abc
2
```

<!-- output: room_plan -->
```text
Enter group sizes (0-8):
Input could not be read
```

<!-- input: room_plan -->
```text
2
abc
```

<!-- output: room_plan -->
```text
Enter group sizes (0-8):
Input could not be read
```

<!-- input: room_plan -->
```text
2
```

<!-- output: room_plan -->
```text
Enter group sizes (0-8):
Input could not be read
```

<!-- input: room_plan -->
```text
```

<!-- output: room_plan -->
```text
Enter group sizes (0-8):
Input could not be read
```

</details>

**After the mission: two separate experiments.** Start each one from a program that works correctly, and restore it to that state after each one. Don't combine both changes at once.

- **Experiment A.** Remove the declaration of the function that `main` calls. **Predict** which stage of the build will fail. Build the program, compare with section 2, and restore the declaration.
- **Experiment B.** Keep the declarations, but remove the definition of a function that is called. **Predict** which stage will fail. Build the program, compare with section 7, and restore the definition.

<details>
<summary>What should happen</summary>

- **Experiment A:** compiling fails. At the place of the call in `main`, the compiler doesn't know the function, as in section 2. The compiler reports `use of undeclared identifier` with the function's name.
- **Experiment B:** compiling succeeds, because the declaration still exists, but linking fails, because the called function's definition is missing, as in section 7. The message comes from the linker and contains the function's name.

</details>

An example solution is in [Example solutions](#example-solutions).

## 9. When something goes differently

| What you see | What it means | What to do |
|---|---|---|
| `use of undeclared identifier` with your function's name | At the place of the call the compiler doesn't know the function: the declaration is missing, or it stands below the call. | Add a declaration before the first call, for example before `main`. |
| `undefined reference`, `undefined symbol` or `referenced from`, and `linker command failed` at the end | The function is declared and called, but the linker can't find its definition. | Add a definition that matches the declaration. Check that the name in the definition is the same. |
| A link error, although the definition is in the file | The definition doesn't match the declaration, for example it has a different name or different parameter types. | Compare the declaration and the definition: the name, the result type, the number and types of parameters. |
| A compile error at a declaration | The semicolon at the end of the declaration is missing. | A declaration ends with `;`, and a definition with a body in braces. |
| `0` or `1` appears in the report | The `bool` result is printed directly. | Let `main` choose the message with an `if`. |
| A report appears after a failed read or bad data | The functions are called before the data is checked. | First check the read and the range, and only then calculate and print. |
| The program does nothing and waits | It's waiting for another number, as in lesson 2.6. | Type a number and press **Enter**. Don't check a case where the data runs out this way: trace it on paper. |

## 10. Explain

Answer in your own words, preferably in writing. Only then compare with the example answers.

1. What is a function declaration?
2. What is a definition?
3. What is a call?
4. How does a declaration differ from a definition?
5. Why does a declaration end with a semicolon?
6. Does a declaration run the function's statements?
7. Can a definition placed before `main` replace a separate declaration?
8. Is it allowed to put `main` before the definitions of your own functions?
9. What must then come earlier?
10. Are parameter names required in a declaration?
11. Why must the parameter types match the function being used?
12. What happens when we call a function the compiler doesn't know?
13. What happens when a called function is declared but has no definition?
14. How does a compile error differ from a link error?
15. Do linker messages on different systems have to look the same?
16. Does every call of an own function need an earlier separate declaration ending with a semicolon?

<details>
<summary>Example answers</summary>

1. Information for the compiler about which function exists: the result type, the name and the parameter types, ending with a semicolon, with no body.
2. A function together with its body, that is, with the statements that run when it's called.
3. The place where the program tells a function to run: its name, with arguments in parentheses.
4. A declaration only describes the function. A definition describes it too, but also contains the body with its statements.
5. Because there's no function body at that point. The semicolon ends the function's description.
6. No. A declaration runs nothing. The statements from the definition run when the program reaches the call.
7. Yes. A definition is also a declaration, so a definition before the place of the call is enough.
8. Yes, as long as the compiler knows the functions at the places where they're called.
9. The declarations of the functions called in `main`, for example at the start of the file.
10. No. In a declaration the types are enough, for example `int double_points(int);`. In the definition the name is needed, so that the body can use the parameter's value.
11. Because the declaration and the definition must describe the same function. Different parameter types would mean a different function.
12. Compiling fails: the compiler reports `use of undeclared identifier`.
13. Compiling succeeds, but linking doesn't: the linker can't find the called function's definition, and the program isn't created.
14. A compile error is reported by the compiler when the code of one file is incorrect, for example when it doesn't know a name. A link error is reported by the linker when it joins the program and can't find something the program needs, for example a function's definition.
15. No. Each system has a different linker, and each one words it differently. What matters is the stage at which the error appeared and which function it's about.
16. No. It's enough that the compiler knows the function at the place of the call, from a declaration or from an earlier definition.

</details>

## Summary

- A **declaration** describes a function: the result type, the name, the parameter types and a semicolon. It has no body and runs nothing.
- A **definition** is a function with a body. It's also a declaration, so a definition before the place of the call is enough.
- A **call** tells a function to run. At the place of the call the compiler must know the function: from a declaration or from an earlier definition.
- With declarations at the start of the file, you can put `main` before the definitions, with the definitions in any order. It's one possible way to organise a file, not a requirement.
- A declaration and a definition must match: the name, the result type, the number and types of parameters. Parameter names can be left out in a declaration.
- **A missing declaration** at the place of a call is a **compile error**. **A missing definition** of a called function is a **link error**: compiling succeeds, but no program is created.
- Linker messages differ between systems. What matters is the stage and the function's name.

## What's next

You now know the basics of your own functions: definitions and calls, parameters, results, several ways to `return`, functions working together, and declarations. The next lesson is in preparation.

---

## Example solutions

Look here **after your own attempt**. Your names may differ, as long as the standard output is as required.

<details>
<summary>Section 7: the program with the definition added</summary>

The declaration and the call stay unchanged. A definition that matches the declaration is added:

<!-- example: score_definition_added -->
```cpp
#include <iostream>

int double_points(int points);

int main() {
    std::cout << "Score: " << double_points(4) << "\n";
}

int double_points(int points) {
    return points * 2;
}
```

<!-- output: score_definition_added -->
```text
Score: 8
```

Now both stages succeed: the compiler knows the function from the declaration, and the linker finds its definition.

</details>

<details>
<summary>Section 8: the mission, the room plan</summary>

<!-- example: room_plan -->
```cpp
#include <iostream>

int total_attendees(int first_group, int second_group);
bool fits_in_room(int first_group, int second_group);

int main() {
    int first_group{0};
    int second_group{0};

    std::cout << "Enter group sizes (0-8):\n";
    std::cin >> first_group;
    std::cin >> second_group;

    if (std::cin.fail()) {
        std::cout << "Input could not be read\n";
    } else {
        const bool first_valid{first_group >= 0 && first_group <= 8};
        const bool second_valid{second_group >= 0 && second_group <= 8};

        if (first_valid && second_valid) {
            std::cout << "Total attendees: " << total_attendees(first_group, second_group) << "\n";

            if (fits_in_room(first_group, second_group)) {
                std::cout << "Room status: Fits\n";
            } else {
                std::cout << "Room status: Too many people\n";
            }
        } else {
            std::cout << "Invalid group size\n";
        }
    }
}

bool fits_in_room(int first_group, int second_group) {
    const int room_capacity{10};
    return total_attendees(first_group, second_group) <= room_capacity;
}

int total_attendees(int first_group, int second_group) {
    return first_group + second_group;
}
```

- **The file layout:** `#include`, two declarations, `main`, two definitions. Each declaration has the same types and the same order of parameters as its definition.
- **The order of the definitions:** `fits_in_room` stands before `total_attendees`, although it calls it. This works because at the place of the call the compiler knows `total_attendees` from the declaration at the start of the file.
- **Cooperation:** `fits_in_room` doesn't repeat the addition; it uses the result of `total_attendees` and compares it with the capacity, `<= 10`. Exactly 10 people fit.
- **`main`** checks the read and the range, prints the total number of people, and chooses the status message based on the `bool` result.
- **A failed read** or out-of-range data ends the program with one message, without calling the functions.

</details>

**Previous lesson:** [Lesson 5.5: Several functions, one program](lesson_05_several_functions.en.md) · **Next lesson:** in preparation · [Course overview](../../README.en.md)

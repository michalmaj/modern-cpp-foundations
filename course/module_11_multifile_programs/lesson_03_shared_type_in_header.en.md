# Lesson 11.3: A shared type in a header

[Polski](lesson_03_shared_type_in_header.md) · **English** · [Course overview](../../README.en.md)

> **Module 11, lesson 3** · about 85–105 minutes; you can split it into two sessions: sections 1–6 and sections 7–11
> **You need:** your `cpp-workspace` folder with the `lesson_11_2` and `ticket_cost_header` projects from [lesson 11.2](lesson_02_own_header_file.en.md). You won't need the debugger in this lesson.
> **Pilot version.** The programs in this lesson, built from several files, are checked automatically on Windows, Ubuntu and macOS, with the given input data, together with the compile errors of sections 8 and 9. The steps in CLion are described according to the CLion 2026.2 documentation, without a manual check on every system.

## Before you start

This lesson assumes that you:

- define your own type with `struct`, create a record with values in `{}` and use its fields with the dot operator (lessons 8.1 and 8.2);
- pass a record that a function only reads by `const&` (lesson 8.3);
- build a program from two `.cpp` files and your own header with `#pragma once` (lessons 11.1 and 11.2).

## The situation

In lesson 11.2, the function `calculate_points` got two separate numbers. But the number of tasks and the bonus together describe one result, and in Module 8 we combined such data in a record. Only in Module 8 the type, the functions and `main` stood in one file. Now `main.cpp` creates the record and a function in `points.cpp` reads its fields, so **both files must know the same type**. In this lesson you'll put its definition in the shared header.

After this lesson you will:

- put the definition of your own type in a header, together with the declaration of a function that uses it;
- create a record in `main.cpp` and pass it by `const&` to a function from another `.cpp` file;
- explain what `#pragma once` protects against when a header contains a type's definition;
- recognise the error of a type defined again, and a header that doesn't include the type it needs.

## 1. Prepare the project

In `cpp-workspace`, create a folder `lesson_11_3` and copy four files into it from `lesson_11_2`: `main.cpp`, `points.hpp`, `points.cpp` and `CMakeLists.txt`. Don't copy the build folders. Open the folder in CLion, or go to it in the terminal, as in lesson 11.1, section 1. In sections 2 and 3 you'll change the three code files. `CMakeLists.txt` stays unchanged.

## 2. A type in the header

Add the definition of the type `TaskResult` to `points.hpp`, and change the function's declaration so that it takes a record:

**`points.hpp`**:

<!-- file: points points.hpp -->
```cpp
#pragma once

struct TaskResult {
    int solved;
    int bonus;
};

int calculate_points(const TaskResult& result);
```

- **`TaskResult` is the name of a type,** defined like the types of Module 8. Every record of this type has two fields: the number of solved tasks and the bonus. The definition itself creates no record.
- **The type's definition stands before the function's declaration,** because the function uses the type in its parameter, as in lesson 8.3.
- **`const TaskResult& result`:** the function reads an existing record, without a copy and without a way to change its fields (lesson 8.3).
- **The header now contains a type's definition and a function's declaration.** Together they are the information shared by both `.cpp` files: what the record looks like, and how to call the function.

Why does the header contain the type's full **definition**, not just a declaration as for the function? A file that creates a record or reads its fields must know which fields the record consists of. A call to a function from another file is joined by the linker (lesson 11.1), but no linker adds a type's fields: the compiler needs them in every `.cpp` file that uses them. That's why a type's definition may stand in a header included by several `.cpp` files. **An ordinary function's definition still stays in the `.cpp` file** (lesson 11.2, section 2).

**A self-contained header** itself includes the headers that its declarations and type definitions need, instead of counting on a `.cpp` file to have included them earlier. `points.hpp` uses only `int`, so it needs no standard header. If it used `std::string` or `std::vector`, it would itself include `<string>` or `<vector>`. The same goes for your own headers (section 9).

## 3. `main.cpp` and `points.cpp` use the type

`main.cpp` creates a record, puts the numbers it reads into its fields and passes it to the function:

**`main.cpp`**:

<!-- example: points -->
```cpp
#include <iostream>

#include "points.hpp"

int main() {
    TaskResult result{0, 0};

    std::cin >> result.solved;
    std::cin >> result.bonus;

    std::cout << "Points: " << calculate_points(result) << "\n";
}
```

| Code | What it does |
|---|---|
| `#include "points.hpp"` | gives `main.cpp` the definition of `TaskResult` and the declaration of `calculate_points` |
| `TaskResult result{0, 0};` | creates a record with initial values for both fields, like `int solved{0};` in lesson 11.2 |
| `std::cin >> result.solved;` | stores the number it reads in the `solved` field of this record |
| `calculate_points(result)` | passes the whole record to the function, instead of two numbers |

- **`result` has no `const`,** because `>>` stores values in its fields. A field of an object without `const` can be the target of `>>`, like a variable, just as it changed with `=` in lesson 8.2.
- **In Module 10, a record was created only after the data was checked.** This program, like the programs of lessons 11.1 and 11.2, doesn't check the data, so reading straight into the fields is enough.

The function's definition in `points.cpp` gets the new parameter. The calculation doesn't change:

**`points.cpp`**:

<!-- file: points points.cpp -->
```cpp
#include "points.hpp"

int calculate_points(const TaskResult& result) {
    const int points_per_task{3};
    return result.solved * points_per_task + result.bonus;
}
```

- **`points.cpp` includes `points.hpp` too,** because to read `result.solved` it must know the fields of `TaskResult`. The function's declaration and definition stand together in one translation unit again.
- **`points.cpp` has no second definition of `TaskResult`.** The type is defined only in the header.
- **What's shared is the type's definition, not one object.** The record `result` is created in `main` and exists only there. `points.cpp` has no record of its own: through `const&`, the function reads the one it got in the call. If another file created its own `TaskResult` record, that would be a separate object, like `first` and `second` in lesson 8.1.

| | Module 8 | This lesson |
|---|---|---|
| the type's definition | in `main.cpp`, above the functions | in `points.hpp` |
| the function with a `const&` parameter | in the same file as `main` | in `points.cpp` |
| creating the record | in `main` | in `main`, in `main.cpp` |
| which files know the type | one file | every file that includes the header |

The structure itself works as in Module 8: the header changes only where it is defined.

## 4. One definition of the type, not two copies

You could define the type separately in `main.cpp` and in `points.cpp`, copying the same lines. Then you'd have to make sure by hand that both copies always stay the same. Imagine that the record gets a third field, and someone adds it to only one copy. Each `.cpp` file is compiled separately, so the compiler of `main.cpp` doesn't see the copy in `points.cpp`, and isn't required to notice the difference. Such a project is easy to break.

A shared header removes this problem: **the type is defined in one place,** both `.cpp` files include that header, and each of them gets exactly the same definition. Changing the type means changing one file.

## 5. `#pragma once` with a type's definition

In lesson 11.2, the header contained only a function's declaration. A matching declaration may be repeated, so `#pragma once` wasn't needed there for compiling. **A type's definition is different:** within one translation unit, `struct TaskResult` may be defined only once.

```text
main.cpp:    #include "points.hpp"   ──►  TaskResult once  ┐  two separate translation units:
points.cpp:  #include "points.hpp"   ──►  TaskResult once  ┘  correct

main.cpp:    #include "points.hpp"   ──►  without #pragma once TaskResult twice
             #include "points.hpp"        in one translation unit: an error
```

- **Two `.cpp` files that each include `points.hpp` aren't a repeated definition.** Each `.cpp` file is prepared and compiled separately, so each gets the type once.
- **The same header twice in one `.cpp` file** means two definitions in one translation unit. That can happen by accident, for example through a copied `#include` line, or through a header that itself includes `points.hpp` (section 9).
- **`#pragma once` makes the second inclusion be skipped,** so the definition reaches the translation unit once. It has nothing to do with including the header in different `.cpp` files, and it doesn't replace linking.

You'll see what this error looks like in section 8.

## 6. Build and run

`CMakeLists.txt` doesn't change:

<!-- cmake: points -->
```cmake
cmake_minimum_required(VERSION 3.28)
project(first_program LANGUAGES CXX)

add_executable(first_program main.cpp points.cpp)
target_compile_features(first_program PRIVATE cxx_std_20)
set_target_properties(first_program PROPERTIES CXX_EXTENSIONS OFF)
```

A header, also one with a type's definition, is compiled as part of the `.cpp` files that include it, and no separate object file is created from it. That's why, in this course's project, `add_executable` still lists only `.cpp` files. It's a rule of our simple project, not a CMake rule (lesson 11.2, section 5).

Build and run the program as in lesson 11.1, section 5. For the data:

<!-- input: points -->
```text
4 2
```

the program prints:

<!-- output: points -->
```text
Points: 14
```

**Predict** the results for `0 5` and `3 0`. Running them is optional.

<!-- input: points -->
```text
0 5
```

<details>
<summary>Standard output for 0 5</summary>

<!-- output: points -->
```text
Points: 5
```

</details>

<!-- input: points -->
```text
3 0
```

<details>
<summary>Standard output for 3 0</summary>

<!-- output: points -->
```text
Points: 9
```

</details>

The results `14` and `5` are the same as in lessons 11.1 and 11.2. **A record instead of two arguments, and the type in a header, change how the data is organised and what the function looks like, not the rule of the calculation.** Nor does the program run faster.

## 7. Mission: a ticket order as a record

Design the data of the ticket program as a record. In `cpp-workspace`, create a folder `ticket_order` and copy four files into it from the `ticket_cost_header` project of lesson 11.2: `main.cpp`, the header, the second `.cpp` file and `CMakeLists.txt`. Leave the original unchanged: you'll use it to compare the results. If you don't have that project, recreate it from [the mission solution in lesson 11.2](lesson_02_own_header_file.en.md#example-solutions).

**Requirements:**

- A regular ticket costs 12 units, a reduced one 7. The program reads two numbers: the number of regular tickets and of reduced ones.
- **Both numbers go into the fields of one record** of your own type, defined **only** in the header, with `#pragma once` on the first line.
- The function gets this record by `const&` and returns the total cost. Its declaration stands in the header, and its definition in the second `.cpp` file.
- **Both `.cpp` files include the header.** No `.cpp` file defines the type a second time.
- `main` creates the record, reads the data into its fields, calls the function and prints `Total cost: N`.
- `add_executable` lists two `.cpp` files, and the rest of `CMakeLists.txt` doesn't change.
- You can keep the file names from lesson 11.2. Name the type with a capital letter, and the fields and the function in `snake_case`, as so far in the course.
- The data is non-negative and small. Don't add checks of the data or new kinds of tickets.

The results must be the same as in lesson 11.2. **Data A:**

<!-- input: tickets -->
```text
2 3
```

<!-- output: tickets -->
```text
Total cost: 45
```

**Data B:**

<!-- input: tickets -->
```text
0 4
```

<!-- output: tickets -->
```text
Total cost: 28
```

**Data C:**

<!-- input: tickets -->
```text
0 0
```

<!-- output: tickets -->
```text
Total cost: 0
```

**Predict D:** `3 0`, only regular tickets.

<!-- input: tickets -->
```text
3 0
```

<details>
<summary>Standard output for data D</summary>

<!-- output: tickets -->
```text
Total cost: 36
```

</details>

**Decide yourself:**

1. what to call your own type;
2. which fields it has, and of which types;
3. where to define the type;
4. what to call the header;
5. what to call the function;
6. how to write its declaration with `const&`;
7. how to write its definition;
8. where the `#include` lines with the header's name stand;
9. how to create the record in `main` and fill its fields;
10. how to compare the results with the project from lesson 11.2.

**Then** build the program and run it for data A and one boundary case: B or C. Compare the results with those of the `ticket_cost_header` project for the same data. Predict the other cases. All of them are checked automatically in the reference solution.

### Success criterion

- The program builds as C++20 and, for data A and for B or C, prints exactly the result shown, the same as the project from lesson 11.2.
- The header starts with `#pragma once` and contains the type's definition and the function's declaration with a `const&` parameter.
- The type is defined only in the header: neither `main.cpp` nor the second `.cpp` file contains a copy of it.
- Both `.cpp` files include the header, and the second `.cpp` file contains the only definition of the function, matching the declaration.
- `main` creates the record, puts the data into its fields and passes it to the function.
- `add_executable` lists two `.cpp` files, without the header.

Correct results don't prove that the files are well organised: a copy of the type or of the declaration in the wrong file would sometimes build too. That's why you check the files against the list above. Your names may differ from those of the reference solution.

<details>
<summary>Hint 1</summary>

Who needs to know the type's definition? `main.cpp` creates the record and puts the data into its fields, and the second `.cpp` file reads those fields in the function.

</details>

<details>
<summary>Hint 2</summary>

In which file is it best to define this type, so as not to duplicate code? Both `.cpp` files already include that file.

</details>

<details>
<summary>Hint 3</summary>

What should both `.cpp` files include, and what does a function's declaration with `const&` look like? Think of `calculate_points` in section 2: the result type, the function's name, and in the parentheses `const`, the type's name, `&` and the parameter's name.

</details>

The example solution is in [Example solutions](#example-solutions).

## 8. Find the bug: a type defined twice

Do this task **after the mission**. Someone removed the line `#pragma once` from `points.hpp`, thinking it unnecessary, and in `main.cpp` copied the line `#include "points.hpp"` by accident. Recreate this project: in `cpp-workspace`, create a folder `points_twice_check`, copy the four files from `lesson_11_3` into it and make both changes. `points.cpp` and `CMakeLists.txt` stay as in sections 3 and 6.

**`points.hpp`** in this project, without `#pragma once`:

<!-- file: points_twice_check points.hpp -->
```cpp
struct TaskResult {
    int solved;
    int bonus;
};

int calculate_points(const TaskResult& result);
```

**`main.cpp`** in this project:

<!-- broken: points_twice_check in=points.hpp at=1:8 errors=1 error=^redefinition of 'TaskResult'$ -->
```cpp
#include <iostream>

#include "points.hpp"
#include "points.hpp"

int main() {
    TaskResult result{0, 0};

    std::cin >> result.solved;
    std::cin >> result.bonus;

    std::cout << "Points: " << calculate_points(result) << "\n";
}
```

<details>
<summary>The other files, unchanged from sections 3 and 6</summary>

**`points.cpp`**:

<!-- file: points_twice_check points.cpp -->
```cpp
#include "points.hpp"

int calculate_points(const TaskResult& result) {
    const int points_per_task{3};
    return result.solved * points_per_task + result.bonus;
}
```

**`CMakeLists.txt`**:

<!-- cmake: points_twice_check -->
```cmake
cmake_minimum_required(VERSION 3.28)
project(first_program LANGUAGES CXX)

add_executable(first_program main.cpp points.cpp)
target_compile_features(first_program PRIVATE cxx_std_20)
set_target_properties(first_program PROPERTIES CXX_EXTENSIONS OFF)
```

</details>

**Before you build**, answer in writing:

1. **Predict:** at which stage will the build fail, compiling or linking?
2. Do the two definitions of `TaskResult` come from two different `.cpp` files?
3. How many times does the content of `points.hpp` reach the translation unit of `main.cpp`?
4. Which definition appears twice in it?

**Then:**

5. Build the project. Configure it as a new project in lesson 11.1, section 5.
6. Read the build output, in the **Build** window or in the terminal. Which `.cpp` file was being compiled, and in which file and on which line is the error?
7. Add `#pragma once` on the first line of `points.hpp`. Leave **both** `#include` lines in `main.cpp` for now.
8. Build the project again and run it for `4 2`.
9. Remove the repeated line `#include "points.hpp"` from `main.cpp`: it isn't needed, and it makes the code harder to read.
10. Explain why, in lesson 11.2, a repeated declaration of the function didn't give such an error.

<details>
<summary>What happens and why: open after building the broken project</summary>

1. **It's a compile error, not a link error.** Compiling `main.cpp` fails, so linking never starts. Changing `CMakeLists.txt` won't fix anything here: both `.cpp` files are in `add_executable`, and the error is in the content of one of them.
2. **The message points to the header,** although `main.cpp` is being compiled. In the build output it looks roughly like this (paths shortened):

   ```text
   In file included from main.cpp:4:
   points.hpp:1:8: error: redefinition of 'TaskResult'
   main.cpp:3:10: note: 'points.hpp' included multiple times, additional include site here
   main.cpp:4:10: note: 'points.hpp' included multiple times, additional include site here
   points.hpp:1:8: note: unguarded header; consider using #ifdef guards or #pragma once
   ```

   The first line says **where the header came from**: line 4 of `main.cpp`. The second says **where the error is**: in `points.hpp`, on line 1, in column 8, at the name `TaskResult`. The lines with `note:` are hints: they show both `#include` lines and suggest protecting the header. They also mention include guards with `#ifdef`, and in this course we use `#pragma once`. On Windows and on other systems the paths look different, and the text of the error is the same.
3. **Both definitions come from the same header, in one translation unit.** The two `#include` lines put the content of `points.hpp` into `main.cpp` twice, so the compiler sees `struct TaskResult` twice in one file. `points.cpp` includes the header once and is correct by itself.
4. **The function's declaration also stands in the header twice, but here it does no harm:** a matching declaration may be repeated. Two definitions of a type in one translation unit may not. That's why there was no error in lesson 11.2.
5. **After you add `#pragma once`,** the second inclusion is skipped, so the program builds even with two `#include` lines. It prints `Points: 14`, as in section 6: `#pragma once` doesn't change how the function works. Still, don't keep the repeated line in the code, because it only makes the code harder to read.

</details>

The fixed project is in [Example solutions](#example-solutions).

## 9. On paper: a header that doesn't include its type

This task is **optional** and needs no running. The calculator project grows, and the type gets a separate header, `task_result.hpp`, because other headers will use it too in the future. `points.hpp` now contains only the function's declaration:

**`task_result.hpp`**:

<!-- file: points_order_check task_result.hpp -->
```cpp
#pragma once

struct TaskResult {
    int solved;
    int bonus;
};
```

**`points.hpp`**:

<!-- file: points_order_check points.hpp -->
```cpp
#pragma once

int calculate_points(const TaskResult& result);
```

`main.cpp` includes `"task_result.hpp"` first, then `"points.hpp"`. `points.cpp` includes only `"points.hpp"`. `add_executable` lists both `.cpp` files.

**Answer:** which `.cpp` file will compile, which won't, and in which file will the compiler report the error? How do you fix it without adding new `#include` lines to the `.cpp` files?

<details>
<summary>Answer</summary>

- **`main.cpp` compiles, but only by chance.** It includes `task_result.hpp` before `points.hpp`, so when the compiler reaches the function's declaration, it already knows `TaskResult`.
- **`points.cpp` doesn't compile.** It includes only `points.hpp`, in which `TaskResult` is unknown. The error is in the header: `points.hpp:3:28: error: unknown type name 'TaskResult'`, and right after it the same error in the function's definition in `points.cpp`.
- **The fix:** `points.hpp` itself includes the header with the type it uses: `#include "task_result.hpp"` below `#pragma once`. Then every file that includes `points.hpp` gets `TaskResult` too, whatever the order of its own `#include` lines.
- **Adding more `#include` lines to the `.cpp` files isn't a fix,** because `points.hpp` would still depend on what someone included before it.
- **`main.cpp` now gets `task_result.hpp` twice:** directly and through `points.hpp`. Thanks to `#pragma once` in `task_result.hpp`, the type reaches this translation unit once. It's the same protection as in section 8.

This rule is called a **self-contained header**: a header itself includes the headers it needs for its own declarations.

</details>

<details>
<summary>The full broken project, checked automatically (optional)</summary>

**`main.cpp`**:

<!-- broken: points_order_check in=points.hpp at=3:28 errors=1 error=^unknown type name 'TaskResult'$ -->
```cpp
#include <iostream>

#include "task_result.hpp"
#include "points.hpp"

int main() {
    TaskResult result{0, 0};

    std::cin >> result.solved;
    std::cin >> result.bonus;

    std::cout << "Points: " << calculate_points(result) << "\n";
}
```

**`points.cpp`**:

<!-- file: points_order_check points.cpp -->
```cpp
#include "points.hpp"

int calculate_points(const TaskResult& result) {
    const int points_per_task{3};
    return result.solved * points_per_task + result.bonus;
}
```

**`CMakeLists.txt`**:

<!-- cmake: points_order_check -->
```cmake
cmake_minimum_required(VERSION 3.28)
project(first_program LANGUAGES CXX)

add_executable(first_program main.cpp points.cpp)
target_compile_features(first_program PRIVATE cxx_std_20)
set_target_properties(first_program PROPERTIES CXX_EXTENSIONS OFF)
```

</details>

The fixed project is in [Example solutions](#example-solutions).

## 10. When something goes differently

| What you see | What it means | What to do |
|---|---|---|
| `redefinition of 'TaskResult'` pointing to the header | A header without `#pragma once` reached one `.cpp` file twice (section 8). | Add `#pragma once` on the first line of the header, and remove repeated `#include` lines. |
| `redefinition of 'TaskResult'`, although the header has `#pragma once` | One of the `.cpp` files still has a hand-written second definition of the type. | Remove the copy. Only the header defines the type. |
| `unknown type name 'TaskResult'` in a `.cpp` file | The file doesn't include the header with the type, or includes it below the place where it uses the type. | Add `#include "points.hpp"` at the start of the file. |
| `unknown type name 'TaskResult'` in a header | The header uses a type from another header that it doesn't include itself (section 9). | Add the missing `#include` to that header. |
| `no member named 'solve' in 'TaskResult'` | A field's name differs from the one in the type's definition. | Compare the name with the definition in the header. |
| `no matching function for call to 'calculate_points'` | `main` calls the function the old way, with two numbers, while the declaration takes a record. | Pass the record to the function: `calculate_points(result)`. |
| A link error naming `calculate_points`, although both `.cpp` files are in `add_executable` | The definition in `points.cpp` has other parameters than the declaration, for example still two numbers. | Change the definition's parameter to `const TaskResult& result`, as in the header. |

## 11. Explain

Answer in your own words, preferably in writing. Only then compare with the example answers.

1. What is now in `points.hpp`, and what in `points.cpp`? Does `points.hpp` go into `add_executable`?
2. Why does the definition of `TaskResult` stand in the header, and not in one of the `.cpp` files?
3. Why don't we copy the type's definition into both `.cpp` files?
4. What is `TaskResult`, and what is `result`? Does `points.cpp` have access to some shared, global record?
5. What does the parameter `const TaskResult& result` give?
6. Why do both `.cpp` files include `points.hpp`?
7. What does `#pragma once` do, and why does it matter more with a type's definition than in lesson 11.2?
8. Is it a repeated definition that `main.cpp` and `points.cpp` both include `points.hpp`? And two identical `#include` lines in one `.cpp` file?
9. Is `redefinition of 'TaskResult'` a compile error or a link error? How does it differ from the error in lesson 11.2, section 8?
10. What does it mean that a header is self-contained?

<details>
<summary>Example answers</summary>

1. `points.hpp` has `#pragma once`, the definition of the type `TaskResult` and the declaration of `calculate_points`. `points.cpp` has `#include "points.hpp"` and the function's definition. `add_executable` lists only `main.cpp` and `points.cpp`: the header is compiled as part of them.
2. Because two files need it: `main.cpp` creates the record and puts the data into its fields, and `points.cpp` reads those fields. Each of them must know the type's fields, and the header gives them the same definition.
3. Because two copies would have to be kept the same by hand. The `.cpp` files are compiled separately, so the compiler isn't required to notice that the copies have drifted apart. One definition in the header is one place to change.
4. `TaskResult` is a type, and `result` is an object of this type, one record. There is no shared record: only the type's definition is shared. `points.cpp` reads the record from `main` only through the function's parameter.
5. The function reads an existing record, without creating a copy, and can't change its fields.
6. `main.cpp` needs the type's definition and the function's declaration to create the record and call the function. `points.cpp` needs the type's definition to read the fields, and by including the header it has the function's declaration and definition in one translation unit.
7. It makes the header be processed at most once within one translation unit. In lesson 11.2 the header contained only a function's declaration, which may be repeated. A type's definition may not be repeated within one translation unit, so without `#pragma once` a second inclusion gives an error.
8. No: each `.cpp` file is a separate translation unit, and each gets the type once. Two `#include` lines in one `.cpp` file put the definition into the same translation unit twice. Without `#pragma once`, that's a `redefinition` error.
9. A compile error: compiling `main.cpp` fails, so linking doesn't start. In lesson 11.2, section 8, everything compiled, and the linker didn't find the function's definition.
10. The header itself includes the headers it needs for its declarations, for example `points.hpp` includes `task_result.hpp`. Then it works in every file that includes it, whatever the order of the `#include` lines.

</details>

## Summary

- The definition of your own type that several `.cpp` files use goes into a shared header. Every file that creates a record or reads its fields includes that header.
- What's shared is the type's definition, not an object: a record exists where it was created, and a function from another file gets it through a `const&` parameter.
- We define the type in one place, not in copies in every `.cpp` file. An ordinary function's definition still stays in the `.cpp` file.
- Within one translation unit, a type may be defined only once. `#pragma once` protects against processing a header again in the same `.cpp` file. Including a header in different `.cpp` files is correct.
- `redefinition` is a compile error, and the message points to a place in the header. The line `In file included from` says where the header came from.
- A header should itself include the headers it needs, instead of depending on the order of the `#include` lines in the `.cpp` files. Such a header is called self-contained.
- Changing how the files and the function's interface are organised doesn't change the program's results.

## What's next

The program in this lesson has one type and one function. The larger programs of Modules 8–10 had several functions that read data, analysed it and printed results. In [lesson 11.4: Splitting a program by responsibility](lesson_04_splitting_responsibilities.en.md), such a program goes into several files, each with its own role.

---

## Example solutions

Look here **after your own attempt**. Your names may differ, as long as the standard output is as required.

<details>
<summary>Section 7: mission, a ticket order as a record</summary>

**`tickets.hpp`**:

<!-- file: tickets tickets.hpp -->
```cpp
#pragma once

struct TicketOrder {
    int regular_tickets;
    int reduced_tickets;
};

int total_cost(const TicketOrder& order);
```

**`tickets.cpp`**:

<!-- file: tickets tickets.cpp -->
```cpp
#include "tickets.hpp"

int total_cost(const TicketOrder& order) {
    const int regular_price{12};
    const int reduced_price{7};
    return order.regular_tickets * regular_price + order.reduced_tickets * reduced_price;
}
```

**`main.cpp`**:

<!-- example: tickets -->
```cpp
#include <iostream>

#include "tickets.hpp"

int main() {
    TicketOrder order{0, 0};

    std::cin >> order.regular_tickets;
    std::cin >> order.reduced_tickets;

    std::cout << "Total cost: " << total_cost(order) << "\n";
}
```

**`CMakeLists.txt`**, the same as in lesson 11.2:

<!-- cmake: tickets -->
```cmake
cmake_minimum_required(VERSION 3.28)
project(first_program LANGUAGES CXX)

add_executable(first_program main.cpp tickets.cpp)
target_compile_features(first_program PRIVATE cxx_std_20)
set_target_properties(first_program PROPERTIES CXX_EXTENSIONS OFF)
```

The results for data A–D: 45, 28, 0 and 36, the same as in lesson 11.2.

This is one of the correct solutions:

1. **`TicketOrder` is defined in `tickets.hpp`,** because both `.cpp` files use it: `main.cpp` creates the record, and `tickets.cpp` reads its fields.
2. **The fields `regular_tickets` and `reduced_tickets`** have the type `int`, as the function's parameters had before. The type's name starts with a capital letter, and the fields are in `snake_case`.
3. **The declaration `int total_cost(const TicketOrder& order);`** stands below the type's definition, because it uses the type.
4. **The function's definition stays in `tickets.cpp`** and reads the fields through `order.`, without changing the record.
5. **Both `.cpp` files include `tickets.hpp`.** Neither contains a copy of `TicketOrder`.
6. **`TicketOrder order{0, 0};`** creates a record with initial values, and the two `>>` reads put the data into its fields. `order` has no `const`, because `>>` stores values in its fields.
7. **`total_cost(order)`** passes the whole record. The function gets it by `const&`, so without a copy.
8. **`#pragma once`** protects the type's definition against being repeated within one translation unit.
9. **`add_executable` lists two `.cpp` files,** without the header.
10. **The results didn't change,** because the prices and the formula are the same. Only the organisation of the data changed.

Other correct solutions: other names of the type, the fields, the function and the files, for example `struct Order` in `prices.hpp`, if you keep the files from lesson 11.2.

</details>

<details>
<summary>Section 8: the fixed project</summary>

`points.hpp` starts with `#pragma once` again. `main.cpp` still has both `#include` lines, as at the first check of the fix in step 8. Then remove the repeated line.

**`points.hpp`**:

<!-- file: points_twice_fixed points.hpp -->
```cpp
#pragma once

struct TaskResult {
    int solved;
    int bonus;
};

int calculate_points(const TaskResult& result);
```

**`main.cpp`**, with both `#include` lines, as in step 8:

<!-- example: points_twice_fixed -->
```cpp
#include <iostream>

#include "points.hpp"
#include "points.hpp"

int main() {
    TaskResult result{0, 0};

    std::cin >> result.solved;
    std::cin >> result.bonus;

    std::cout << "Points: " << calculate_points(result) << "\n";
}
```

**`points.cpp`**, unchanged:

<!-- file: points_twice_fixed points.cpp -->
```cpp
#include "points.hpp"

int calculate_points(const TaskResult& result) {
    const int points_per_task{3};
    return result.solved * points_per_task + result.bonus;
}
```

**`CMakeLists.txt`**, unchanged:

<!-- cmake: points_twice_fixed -->
```cmake
cmake_minimum_required(VERSION 3.28)
project(first_program LANGUAGES CXX)

add_executable(first_program main.cpp points.cpp)
target_compile_features(first_program PRIVATE cxx_std_20)
set_target_properties(first_program PROPERTIES CXX_EXTENSIONS OFF)
```

For the same data as in section 6:

<!-- input: points_twice_fixed -->
```text
4 2
```

<!-- output: points_twice_fixed -->
```text
Points: 14
```

</details>

<details>
<summary>Section 9: a self-contained header</summary>

Only `points.hpp` changes: it includes `task_result.hpp` itself. `main.cpp` and `points.cpp` stay as in the broken project.

**`points.hpp`**:

<!-- file: points_order_fixed points.hpp -->
```cpp
#pragma once

#include "task_result.hpp"

int calculate_points(const TaskResult& result);
```

**`task_result.hpp`**, unchanged:

<!-- file: points_order_fixed task_result.hpp -->
```cpp
#pragma once

struct TaskResult {
    int solved;
    int bonus;
};
```

**`main.cpp`**, unchanged:

<!-- example: points_order_fixed -->
```cpp
#include <iostream>

#include "task_result.hpp"
#include "points.hpp"

int main() {
    TaskResult result{0, 0};

    std::cin >> result.solved;
    std::cin >> result.bonus;

    std::cout << "Points: " << calculate_points(result) << "\n";
}
```

**`points.cpp`**, unchanged:

<!-- file: points_order_fixed points.cpp -->
```cpp
#include "points.hpp"

int calculate_points(const TaskResult& result) {
    const int points_per_task{3};
    return result.solved * points_per_task + result.bonus;
}
```

**`CMakeLists.txt`**, unchanged:

<!-- cmake: points_order_fixed -->
```cmake
cmake_minimum_required(VERSION 3.28)
project(first_program LANGUAGES CXX)

add_executable(first_program main.cpp points.cpp)
target_compile_features(first_program PRIVATE cxx_std_20)
set_target_properties(first_program PROPERTIES CXX_EXTENSIONS OFF)
```

<!-- input: points_order_fixed -->
```text
4 2
```

<!-- output: points_order_fixed -->
```text
Points: 14
```

`main.cpp` gets `task_result.hpp` twice, directly and through `points.hpp`, and thanks to `#pragma once` the type reaches this translation unit once. `main.cpp` may keep its own `#include "task_result.hpp"`, because it uses `TaskResult` itself.

</details>

**Previous lesson:** [Lesson 11.2: Your own header file](lesson_02_own_header_file.en.md) · **Next lesson:** [Lesson 11.4: Splitting a program by responsibility](lesson_04_splitting_responsibilities.en.md) · [Course overview](../../README.en.md)

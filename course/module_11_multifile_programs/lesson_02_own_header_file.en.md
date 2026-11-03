# Lesson 11.2: Your own header file

[Polski](lesson_02_own_header_file.md) · **English** · [Course overview](../../README.en.md)

> **Module 11, lesson 2** · about 80–100 minutes; you can split it into two sessions: sections 1–6 and sections 7–10
> **You need:** your `cpp-workspace` folder with the `lesson_11_1` and `ticket_cost` projects from [lesson 11.1](lesson_01_second_source_file.en.md). You won't need the debugger in this lesson.
> **Pilot version.** The programs in this lesson, built from several files, are checked automatically on Windows, Ubuntu and macOS, with the given input data. The steps in CLion (a new header file, typing input in the **Run** window) are described according to the CLion 2026.2 documentation, without a manual check on every system.

## Before you start

This lesson assumes that you:

- build a program from two `.cpp` files: the function's declaration stands in `main.cpp`, the definition in a second file, and `add_executable` lists both files (lesson 11.1);
- know that the preprocessor handles lines starting with `#`, and that `#include <iostream>` inserts declarations from the standard library (lesson 1.4);
- check that a declaration matches its definition (lessons 5.6 and 11.1).

## The situation

In lesson 11.1, `main.cpp` had its own copy of the declaration of `calculate_points`. If a third `.cpp` file also calls the function, it needs another copy. When the function gets a new parameter, every copy must be fixed, and the compiler won't compare them with each other. In this lesson you'll write the declaration **once**, in your own **header file** `.hpp`, and include it in every file that needs it.

After this lesson you will:

- create your own header file with a function's declaration and `#pragma once`;
- include it with `#include "points.hpp"` in the file that calls the function and in the file with its definition;
- explain why the definition stays in the `.cpp` file, and why `add_executable` still lists only `.cpp` files;
- recognise a link error when the header contains a declaration, but there's no matching definition anywhere.

## 1. Prepare the project

In `cpp-workspace`, create a folder `lesson_11_2` and copy three files into it from `lesson_11_1`: `main.cpp`, `points.cpp` and `CMakeLists.txt`. Don't copy the build folders, as in lesson 1.1. It's the same points calculator as in lesson 11.1, so you can focus on the declaration. Open the folder in CLion, or go to it in the terminal, as in lesson 11.1, section 1.

## 2. The header file `points.hpp`

A **header file** is a file with declarations that other files include with `#include`. In this course it has the extension `.hpp`. You'll also meet `.h`, common in older code and in the C language.

In the `lesson_11_2` folder, next to `main.cpp`, create a file `points.hpp`:

- **In CLion** (according to the CLion 2026.2 documentation): in the **Project** window, right-click the project folder and choose **New | C/C++ Header File**. Type the name `points`, and in the type field choose `.hpp` if CLion offers another extension. Don't add the file to the `first_program` target (section 5). By default, a new CLion header already contains the lines `#ifndef`, `#define` and `#endif`. Replace the file's whole content with the text below.
- **In another text editor:** save the file as `points.hpp` in the same folder as `main.cpp`.

Then **cut** the declaration of `calculate_points` out of `main.cpp` and paste it into `points.hpp`, below the line `#pragma once`:

**`points.hpp`**:

<!-- file: points points.hpp -->
```cpp
#pragma once

int calculate_points(int solved, int bonus);
```

- The header contains the **declaration**, ending with a semicolon, without the function's body.
- **The definition stays in `points.cpp`.** Two `.cpp` files will include the header, so a definition written in the header would get into the program twice, and the linker would report that the function is defined more than once.

## 3. `#pragma once`

`#pragma once` stands on the first line of your own header. It tells the preprocessor: if this header has already been included in this translation unit (lesson 11.1, section 6), don't process it a second time. That can happen when a file includes the same header indirectly, through other headers.

- **It works within one `.cpp` file,** not across the whole program. `main.cpp` and `points.cpp` are compiled separately, and each of them gets the declaration from the header.
- **It doesn't replace the definition, and doesn't change linking.**
- **It isn't what makes this program compile.** The header contains only a function's declaration, and a matching declaration may be repeated. `#pragma once` is a habit whose meaning becomes clearer when a header contains the definition of your own type.

`#pragma once` isn't part of the ISO C++20 standard, but Clang and other popular compilers support it. In other people's code and in CLion's template for a new header, you'll see three lines instead, `#ifndef`, `#define` and `#endif`, called include guards. They serve the same purpose. In this course you don't write them.

## 4. `#include "points.hpp"` in both `.cpp` files

In place of the removed declaration, `main.cpp` gets `#include "points.hpp"`:

**`main.cpp`**:

<!-- example: points -->
```cpp
#include <iostream>

#include "points.hpp"

int main() {
    int solved{0};
    int bonus{0};

    std::cin >> solved;
    std::cin >> bonus;

    std::cout << "Points: " << calculate_points(solved, bonus) << "\n";
}
```

`points.cpp` includes the same header at its start. The definition doesn't change:

**`points.cpp`**:

<!-- file: points points.cpp -->
```cpp
#include "points.hpp"

int calculate_points(int solved, int bonus) {
    const int points_per_task{3};
    return solved * points_per_task + bonus;
}
```

**What `#include` does.** When the preprocessor prepares a file for compiling (lesson 1.4), `#include "points.hpp"` puts the header's content at that place. So the compiler sees the declaration in `main.cpp` as if it were typed there. `#include` doesn't run anything, and doesn't compile or link `points.cpp`: CMake, Ninja and the linker still do that.

| Code | What it includes | Where the file is |
|---|---|---|
| `#include <iostream>` | a header of the standard library | in the standard library's folders, which the compiler knows |
| `#include "points.hpp"` | your own header from the project | in the same folder as the file that includes it |

**Why both files.** `main.cpp` needs the declaration to compile the call. `points.cpp` includes it so that the declaration and the definition stand together in one translation unit. The declaration exists in one place: after a change to the function you fix the header and the definition, and every file that includes the header gets the new version.

**You still have to check that they match.** The header in `points.cpp` doesn't guarantee that the function defined below it is the declared one. A function with another name or other parameter types is simply another function to C++: the compiler won't report it. So compare the name, the result type and the parameter types, as in lesson 11.1. You'll see such a mistake in section 8.

## 5. `CMakeLists.txt` unchanged

`CMakeLists.txt` stays as in lesson 11.1:

<!-- cmake: points -->
```cmake
cmake_minimum_required(VERSION 3.28)
project(first_program LANGUAGES CXX)

add_executable(first_program main.cpp points.cpp)
target_compile_features(first_program PRIVATE cxx_std_20)
set_target_properties(first_program PROPERTIES CXX_EXTENSIONS OFF)
```

- **A header isn't compiled or linked separately.** Its content is compiled as part of every `.cpp` file that includes it. No separate object file is created from it.
- **In this course's project, `add_executable` lists only `.cpp` files.** CMake lets you add headers to a target too, for example so that a development environment shows them with the project. This course doesn't do that: it's a rule of our simple project, not a CMake rule. If CLion added `points.hpp` to `add_executable`, remove that name.

## 6. Build and run

Build and run the program as in lesson 11.1, section 5. `CMakeLists.txt` hasn't changed. If you configure the new folder `lesson_11_2` in CLion or in the terminal, configuring is the same as there.

The build output still has **two** `Building CXX object` lines, for `main.cpp` and `points.cpp`, and one `Linking` line. There's no separate line for `points.hpp`:

```text
points.hpp ──#include──► main.cpp    ──►  compiling  ──►  main.cpp.o    ──┐
           ──#include──► points.cpp  ──►  compiling  ──►  points.cpp.o  ──┴──►  linking  ──►  first_program
```

For the data:

<!-- input: points -->
```text
4 2
```

the program prints:

<!-- output: points -->
```text
Points: 14
```

**Predict** the result for `0 5`. Running it is optional.

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

These are exactly the same results as in lesson 11.1. **Adding a header changes how the code is organised, not the result of the calculation.** Nor does the program run faster: the benefit is keeping the declaration in one place.

## 7. Mission: tickets with a header

Turn your `ticket_cost` project from lesson 11.1 into a project with its own header. In `cpp-workspace`, create a folder `ticket_cost_header` and copy `main.cpp`, the second `.cpp` file and `CMakeLists.txt` from `ticket_cost` into it. Leave the original unchanged: you'll use it to compare the results. If you don't have that project, recreate it from [the mission solution in lesson 11.1](lesson_01_second_source_file.en.md#example-solutions).

**Requirements:**

- The calculation doesn't change: a regular ticket costs 12 units, a reduced one 7, the function returns the total cost, and `main` reads both numbers and prints `Total cost: N`.
- The function's declaration stands **only** in the header, with `#pragma once` on the first line.
- The definition stays in the second `.cpp` file. The header contains no definition.
- **Both `.cpp` files include the same header** with `#include "..."`.
- `add_executable` still lists two `.cpp` files, without the header. The program has one `main`.
- You can keep the function and file names from lesson 11.1. The header's name consists of lowercase English letters, digits and `_`, and ends in `.hpp`. The example solution uses `tickets.hpp`.
- Don't add new rules or checks of the data.

The results must be the same as in lesson 11.1. **Data A:**

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

**Predict D:** `3 0`, regular tickets only.

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

1. what to call the header;
2. what to write in it;
3. where `#pragma once` stands;
4. where the function's declaration stands;
5. what stays in `main.cpp`;
6. what stays in the second `.cpp` file;
7. where both `#include` lines with the header's name stand;
8. whether to keep the old declaration in `main.cpp`;
9. which files `CMakeLists.txt` lists;
10. how to show that the change of organisation didn't change the results.

**Then** build the program and run it for data A and one boundary case: B or C. Compare the results with those of the `ticket_cost` project for the same data. Predict the other cases. All of them are checked automatically in the reference solution.

### Success criterion

- The program builds as C++20 and, for data A and for B or C, prints exactly the result shown, the same as the project from lesson 11.1.
- The header starts with `#pragma once` and contains the function's declaration, with no definition.
- `main.cpp` has no hand-written declaration: it has an `#include` of the header.
- The second `.cpp` file includes the same header and contains the only definition of the function, matching the declaration.
- `add_executable` lists two `.cpp` files, without the header.
- No file includes a `.cpp` file.

A program that builds and prints the right results doesn't yet prove that the files are organised correctly: a redundant copy of the declaration in `main.cpp` would build too. That's why you check the files against the list above. When everything matches, you can save the project in Git. Four files belong in the commit now, the header included.

<details>
<summary>Hint 1</summary>

In which file should the function's declaration live now? One remains, and every file that needs it uses the same one.

</details>

<details>
<summary>Hint 2</summary>

What should `main.cpp` and the second `.cpp` file include so that they use one declaration? Both need the same `#include` line, with the header's name in quotes.

</details>

<details>
<summary>Hint 3</summary>

What should stay in `add_executable`, and what should be in the header? The list of files to build doesn't change, and the header contains only `#pragma once` and the declaration.

</details>

The example solution is in [Example solutions](#example-solutions).

## 8. Find the bug: a declaration isn't a definition

Do this task **after the mission**. Someone was editing the points calculator and lost one letter in the definition in `points.cpp`: `calculate_point` instead of `calculate_points`. Recreate this project: in `cpp-workspace`, create a folder `points_name_check`, copy the four files from `lesson_11_2` into it, and in `points.cpp` remove the final `s` from the function's name in the definition.

**`points.cpp`** in this project:

<!-- file: points_name_check points.cpp -->
```cpp
#include "points.hpp"

int calculate_point(int solved, int bonus) {
    const int points_per_task{3};
    return solved * points_per_task + bonus;
}
```

<details>
<summary>The other files, unchanged from sections 4 and 5</summary>

**`main.cpp`**:

<!-- broken: points_name_check stage=link error=undefined reference to .calculate_points\(int, int\)'|undefined symbol: int __cdecl calculate_points\(int, int\)|"calculate_points\(int, int\)", referenced from -->
```cpp
#include <iostream>

#include "points.hpp"

int main() {
    int solved{0};
    int bonus{0};

    std::cin >> solved;
    std::cin >> bonus;

    std::cout << "Points: " << calculate_points(solved, bonus) << "\n";
}
```

**`points.hpp`**:

<!-- file: points_name_check points.hpp -->
```cpp
#pragma once

int calculate_points(int solved, int bonus);
```

**`CMakeLists.txt`**:

<!-- cmake: points_name_check -->
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
2. What does `points.hpp` declare?
3. Compare the function's name in the call in `main`, in the header and in the definition.
4. Are both `.cpp` files in `add_executable`?

**Then:**

5. Build the project. Configure it as a new project in lesson 11.1, section 5.
6. Read the build output: which files compiled, and what does the linker report?
7. Fix the name in the definition to `calculate_points`.
8. Build the project again.
9. Run it and type `4 2`.
10. Explain why the header alone didn't provide the definition.

<details>
<summary>What happens, and why: open it after building the broken project</summary>

1. **Both files compile:** there are two `Building CXX object` lines. `main.cpp` knows `calculate_points` from the header. `points.cpp` includes that header and defines the function `calculate_point`, which to the compiler is simply another function.
2. **Linking fails.** `main` calls `calculate_points`, and no object file has its definition. The message is the same as in lesson 11.1: on Ubuntu ``undefined reference to `calculate_points(int, int)'``, on macOS `"calculate_points(int, int)", referenced from`, on Windows `undefined symbol: int __cdecl calculate_points(int, int)`, and `linker command failed` at the end.
3. **The header contains only a declaration.** It says that the function exists and how to call it, but it doesn't define it. Some `.cpp` file in `add_executable` must provide the definition.

**A different problem from lesson 11.1, the same message.** There, the definition was correct, but its file wasn't built. Here, the file is built, but it defines another function. So a link error doesn't always mean a `.cpp` file left out: first check `add_executable`, then compare the names and types in the header and in the definition.

After the name is fixed, the program prints `Points: 14`, as in section 6.

</details>

**On paper, without running anything.** What happens if `main.cpp` and `points.cpp` include `points.hpp`, but `main.cpp` still has a hand-written, identical declaration of `calculate_points`?

<details>
<summary>Answer</summary>

The program still compiles and works: a matching declaration of an ordinary function may be repeated. But that copy is redundant. When the function changes and someone fixes only the header, the copy in `main.cpp` will stop matching. That's why we keep the declaration in one place, in the header.

</details>

The fixed project is in [Example solutions](#example-solutions).

## 9. When something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `'points.hpp' file not found` | The header isn't next to the file that includes it, or it has another name, for example `points.h` or `points.hpp.txt`. | Check the name with `ls` and compare it with the `#include` line. |
| `file not found with <angled> include; use "quotes" instead` | Your own header is included in angle brackets. | Include your own headers in quotes: `#include "points.hpp"`. |
| the warning `non-portable path to file`, or `file not found` for a name with a capital letter | The case in `#include` differs from the file's name, for example `Points.hpp`. On Windows and macOS the file is found, with a warning; on Linux it isn't. | Type the name exactly as it is on disk. |
| `use of undeclared identifier` with the function's name in `main.cpp` | `main.cpp` doesn't include the header, or includes it below the call. | Add `#include "points.hpp"` at the start of `main.cpp`. |
| `undefined reference`, `undefined symbol` or `referenced from`, although both `.cpp` files are in `add_executable` | The definition has another name or other parameter types than the declaration in the header (section 8). | Compare the definition with the declaration in the header. |
| The linker reports that the function is defined more than once, for example `duplicate symbol` or `multiple definition` | The definition got into the header, which two `.cpp` files include. | Keep the declaration with a semicolon in the header, and the definition in the `.cpp` file. |
| `add_executable` has `points.hpp`, or the header has the lines `#ifndef`, `#define` and `#endif` | That's how CLion prepared the file (section 2). | Remove the header's name from `add_executable`, and replace the header's content with the text from section 2. |

## 10. Explain

Answer in your own words, preferably in writing. Only then compare with the example answers.

1. What is in `points.hpp`, and what in `points.cpp`?
2. Why does `main.cpp` include `points.hpp`? And why does `points.cpp` include it too?
3. What does `#include "points.hpp"` do, and what doesn't it do? How does it differ from `#include <iostream>`?
4. What does `#pragma once` do, and what doesn't it do?
5. Is a header compiled or linked separately?
6. Why doesn't `points.hpp` stand in `add_executable` in this course's project? Would CMake allow it?
7. Does a header alone provide a function's definition?
8. Does a link error always mean a `.cpp` file left out of `add_executable`?
9. The program in lesson 10.5 had its own type, used by two functions and `main`. If you split it into files, what would every file that uses that type need to know about it?

<details>
<summary>Example answers</summary>

1. `points.hpp` has `#pragma once` and the declaration of `calculate_points`. `points.cpp` has `#include "points.hpp"` and the function's definition, that is, its body with the calculation.
2. `main.cpp` needs the declaration to compile the call. `points.cpp` includes the same header so that the declaration and the definition stand in one translation unit, and the declaration exists in one place only. That doesn't guarantee that the definition matches, though: a function with another name or other parameter types would simply be another function.
3. It puts the header's content at the place of that line, before the file is compiled. It doesn't run code, and doesn't compile or link `points.cpp`. Quotes mean your own header from the project folder, and angle brackets a header of the standard library.
4. It makes the header processed at most once in one translation unit, even if it's included several times. It doesn't limit including to one file in the whole program, doesn't provide a definition, and doesn't change linking.
5. No. Its content is compiled as part of every `.cpp` file that includes it. There's no separate object file.
6. Because in this course `add_executable` lists the files that are compiled, and a header isn't one of them. CMake would allow adding the header, for example for the convenience of a development environment. Leaving it out is a rule of our simple project, not a CMake rule.
7. No. It contains the declaration, and a `.cpp` file in `add_executable` must provide the definition. In section 8 the header was included, and still the definition was missing.
8. No. In lesson 11.1 the file was left out, and in section 8 the file was built but defined a function with another name. The same message can have different causes.
9. Every such file needs the type's definition, that is, which fields it consists of, not only a declaration. Such a definition can also go into a shared header. Then `#pragma once` matters more.

</details>

## Summary

- A header file `.hpp` contains declarations that other files include with `#include "..."`. A function's declaration then exists in one place.
- `#include` inserts the header's content into the file before compiling. It doesn't compile or link other files.
- The header is included by the file that calls the function and by the file with its definition. The name, the result type and the parameter types still need comparing.
- The definition stays in the `.cpp` file. A header doesn't provide a definition.
- `#pragma once` prevents a header from being processed again in one translation unit. It isn't part of the standard, but popular compilers support it.
- A header isn't compiled or linked separately. In this course's project, `add_executable` lists only `.cpp` files.
- The same linker message can mean a `.cpp` file left out, or a definition that doesn't match the declaration.

## What's next

The header in this lesson contains only a function's declaration. The programs of Modules 8–10 also had their own types, used by several functions. In the next lesson of Module 11, the definition of such a type will go into a shared header. That lesson is in preparation.

---

## Example solutions

Look here **after your own attempt**. Your names may differ, as long as the standard output is as required.

<details>
<summary>Section 7: the mission, tickets with a header</summary>

**`tickets.hpp`**:

<!-- file: tickets tickets.hpp -->
```cpp
#pragma once

int total_cost(int regular_tickets, int reduced_tickets);
```

**`tickets.cpp`**:

<!-- file: tickets tickets.cpp -->
```cpp
#include "tickets.hpp"

int total_cost(int regular_tickets, int reduced_tickets) {
    const int regular_price{12};
    const int reduced_price{7};
    return regular_tickets * regular_price + reduced_tickets * reduced_price;
}
```

**`main.cpp`**:

<!-- example: tickets -->
```cpp
#include <iostream>

#include "tickets.hpp"

int main() {
    int regular_tickets{0};
    int reduced_tickets{0};

    std::cin >> regular_tickets;
    std::cin >> reduced_tickets;

    std::cout << "Total cost: " << total_cost(regular_tickets, reduced_tickets) << "\n";
}
```

**`CMakeLists.txt`**, the same as in lesson 11.1:

<!-- cmake: tickets -->
```cmake
cmake_minimum_required(VERSION 3.28)
project(first_program LANGUAGES CXX)

add_executable(first_program main.cpp tickets.cpp)
target_compile_features(first_program PRIVATE cxx_std_20)
set_target_properties(first_program PROPERTIES CXX_EXTENSIONS OFF)
```

The results for data A–D: 45, 28, 0 and 36, the same as in lesson 11.1.

1. **The declaration is in the header,** because two files need it, and it must exist in one place.
2. **The definition stays in `tickets.cpp`,** because two `.cpp` files include the header. A definition in the header would get into the program twice.
3. **Both `.cpp` files include the header:** `main.cpp` to compile the call, and `tickets.cpp` so that the declaration and the definition stand together.
4. **`main.cpp` has no second, hand-written declaration.** It would build, but after a change to the function it could stop matching the header.
5. **`#pragma once`** makes the header processed at most once in one translation unit.
6. **It doesn't block including in different `.cpp` files:** `main.cpp` and `tickets.cpp` are compiled separately, and each gets the declaration.
7. **`add_executable` lists two `.cpp` files,** because only they are compiled. The header is compiled as part of them.
8. **A `.cpp` file isn't included in another `.cpp`:** the definition would get into the program twice, and the linker joins `.cpp` files.
9. **Linking is still needed:** the call in `main.cpp.o` must be joined with the definition in `tickets.cpp.o`.
10. **The results haven't changed,** because the calculation and `main` are the same. Only the place of the declaration has changed.

Other correct solutions: the names from your project in lesson 11.1, for example `prices.hpp` next to `prices.cpp`, or a declaration without parameter names, `int total_cost(int, int);`.

</details>

<details>
<summary>Section 8: the fixed project</summary>

Compared with the broken project, one line of `points.cpp` changes: the definition is called `calculate_points` again.

**`points.cpp`**:

<!-- file: points_name_fixed points.cpp -->
```cpp
#include "points.hpp"

int calculate_points(int solved, int bonus) {
    const int points_per_task{3};
    return solved * points_per_task + bonus;
}
```

**`main.cpp`**, unchanged:

<!-- example: points_name_fixed -->
```cpp
#include <iostream>

#include "points.hpp"

int main() {
    int solved{0};
    int bonus{0};

    std::cin >> solved;
    std::cin >> bonus;

    std::cout << "Points: " << calculate_points(solved, bonus) << "\n";
}
```

**`points.hpp`**, unchanged:

<!-- file: points_name_fixed points.hpp -->
```cpp
#pragma once

int calculate_points(int solved, int bonus);
```

**`CMakeLists.txt`**, unchanged:

<!-- cmake: points_name_fixed -->
```cmake
cmake_minimum_required(VERSION 3.28)
project(first_program LANGUAGES CXX)

add_executable(first_program main.cpp points.cpp)
target_compile_features(first_program PRIVATE cxx_std_20)
set_target_properties(first_program PROPERTIES CXX_EXTENSIONS OFF)
```

For the same data as in section 6:

<!-- input: points_name_fixed -->
```text
4 2
```

<!-- output: points_name_fixed -->
```text
Points: 14
```

</details>

**Previous lesson:** [Lesson 11.1: A second source file](lesson_01_second_source_file.en.md) · **Next lesson:** in preparation · [Course overview](../../README.en.md)

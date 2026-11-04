# Lesson 11.4: Splitting a program by responsibility

[Polski](lesson_04_splitting_responsibilities.md) · **English** · [Course overview](../../README.en.md)

> **Module 11, lesson 4** · about 100–120 minutes; you can split it into two sessions: sections 1–7 and sections 8–11
> **You need:** your `cpp-workspace` folder with the `workshop_orders` project from [lesson 10.3](../module_10_input_records/lesson_03_building_a_vector_of_records.en.md). You won't need the debugger in this lesson.
> **Pilot version.** The programs in this lesson, built from several files, are checked automatically on Windows, Ubuntu and macOS, with the data of lesson 10.3, together with the link error of section 9. The steps in CLion are the same as in lessons 11.1–11.3, and haven't been checked by hand on every system.

## Before you start

This lesson assumes that you:

- read a list of records with an announced count, check the reading before the rules, and at the first error end the program without a report (lesson 10.3);
- pass a vector of records and its elements by `const&` (lessons 8.3 and 8.4);
- build a program from several `.cpp` files and your own header with a shared type (lessons 11.1–11.3).

## The situation

The shipment-list program of lesson 10.3 does everything in one `main`: it reads the data, checks it, builds the vector, adds up the boxes and prints the report. At 60 lines that's still manageable, but to change how the report looks you have to read through all the reading code, and to check the sum you have to look for it among the output statements. In this lesson you'll split this program into files **by responsibility**: reading and control, calculations, and the report, with a shared header.

After this lesson you will:

- plan how to split a program into files according to what each part is responsible for;
- put the shared type and the declarations of functions that other files need in a shared header;
- keep calculating a result apart from printing the report, and call functions defined in different `.cpp` files;
- recognise the link error when the same function is defined in two files.

## 1. Prepare the project

In `cpp-workspace`, create a folder `lesson_11_4`, copy `CMakeLists.txt` into it from the original `lesson_05_first_program`, and create in it a `main.cpp` with the shipment-list program of [lesson 10.3, section 2](../module_10_input_records/lesson_03_building_a_vector_of_records.en.md#2-a-list-of-shipments). If your `main.cpp` in `lesson_10_3` already contains another program, copy the code from that section. In this lesson you don't change how it works; you only spread it over four files, all in the folder `lesson_11_4`:

1. **In sections 3–5**, create three new files next to `main.cpp`: `shipments.hpp`, `shipments_analysis.cpp` and `shipments_report.cpp`, as in lessons 11.1 and 11.2, and type the code shown into them.
2. **In section 6**, change `main.cpp`: the type, the sum and the report are in the new files by then, so reading and control stay in `main.cpp`.
3. **In section 7**, add both new `.cpp` files to `add_executable`, next to `main.cpp`: all three belong to the same program, `first_program`. Only then build and run the program.

## 2. A plan first

Before you create the files, decide who is responsible for what:

| Responsibility | Data needed | File | Function or operation | Result |
|---|---|---|---|---|
| reading, checking the data, building the list and controlling the program | standard input | `main.cpp` | `main` | a vector of valid shipments, or the message `Input error` or `Invalid shipments` |
| the shared type and the declarations | — | `shipments.hpp` | `struct Shipment`, the declarations of two functions | an agreement that the other files use |
| calculations | the vector of shipments | `shipments_analysis.cpp` | `total_boxes` | the number of boxes, an `int` |
| the report | the vector of shipments | `shipments_report.cpp` | `print_shipments` | the report's lines on standard output |

How the data and the calls flow:

```text
main  ──reads valid records──►  std::vector<Shipment>
main  ──const std::vector<Shipment>&──►  print_shipments   (shipments_report.cpp)
print_shipments  ──the same vector──►  total_boxes   (shipments_analysis.cpp)
total_boxes  ──returns the sum──►  print_shipments  ──►  the report on standard output
```

Why these boundaries:

- **Reading and control stay in `main`,** because `main` decides whether the data is valid and whether a report is printed at all.
- **The calculation stands apart,** because it doesn't depend on how the result is printed. Changing how the report looks then doesn't need a change to the sum.
- **The report stands apart,** because it prints ready data and doesn't need to know how it was read.
- **The type and the declarations are shared,** so nobody copies them (lessons 11.2 and 11.3).

It becomes easier to find the code responsible for a given problem, and the calculations don't mix with the output. Splitting into files doesn't change how the program works, nor does it make it faster. This is one sensible split, not the only architecture for every program. What this split does **not** mean:

- **Not every function gets its own file.** Several related functions may stand in one `.cpp` file, as you'll see in the mission.
- **The header declares what other files need,** not everything in the whole program. A helper function used only in one `.cpp` file doesn't have to go into the shared header.
- **A file includes the headers it needs itself,** not every header of the project.
- **The order of the files in `add_executable` doesn't set the order of execution.** The program always starts with `main`, and functions run when something calls them.

## 3. The shared header: an agreement between the files

**`shipments.hpp`**:

<!-- file: shipments shipments.hpp -->
```cpp
#pragma once

#include <string>
#include <vector>

struct Shipment {
    std::string destination;
    int boxes;
};

int total_boxes(const std::vector<Shipment>& shipments);
void print_shipments(const std::vector<Shipment>& shipments);
```

- **The header is an agreement.** It says what a shipment looks like and which functions can be called, not how they work. The implementation stands in the `.cpp` files, and `main.cpp` joins everything into the program's flow.
- **`Shipment` is the same type as in lesson 10.3,** moved into the header like `TaskResult` in lesson 11.3.
- **Two declarations,** because other files use these functions: `main.cpp` calls `print_shipments`, and `shipments_report.cpp` calls `total_boxes`.
- **`void`,** because `print_shipments` returns nothing; it only prints (lesson 5.1).
- **The header is self-contained:** it includes `<string>` and `<vector>` itself, because its declarations need them (lesson 11.3, section 9). It contains no definitions of ordinary functions (lesson 11.2).

## 4. Calculations: `shipments_analysis.cpp`

<!-- file: shipments shipments_analysis.cpp -->
```cpp
#include "shipments.hpp"

int total_boxes(const std::vector<Shipment>& shipments) {
    int total{0};

    for (const Shipment& shipment : shipments) {
        total += shipment.boxes;
    }

    return total;
}
```

- **It gets the vector by `const&` and goes through the elements by `const Shipment&`,** without copies and without changes (lesson 8.4).
- **It reads and prints nothing:** it only returns the result.
- **It includes only `shipments.hpp`,** because that gives it the type and the declaration it defines. It doesn't use standard input or output.

## 5. The report: `shipments_report.cpp`

<!-- file: shipments shipments_report.cpp -->
```cpp
#include <iostream>

#include "shipments.hpp"

void print_shipments(const std::vector<Shipment>& shipments) {
    std::cout << "Shipments: " << shipments.size() << "\n";

    for (const Shipment& shipment : shipments) {
        std::cout << shipment.destination << ": " << shipment.boxes << "\n";
    }

    std::cout << "Total boxes: " << total_boxes(shipments) << "\n";
}
```

- **It prints the report in the same format as in lesson 10.3:** the number of shipments, each shipment in the vector's order, and the total.
- **It doesn't calculate the total itself.** It calls `total_boxes`, which is defined in another file. The compiler knows it from the declaration in `shipments.hpp`, and the linker joins the call to the definition, like `main` and `calculate_points` in lesson 11.1. **Functions from different files work together without including `.cpp` files.**
- **It includes `<iostream>`,** because it prints itself, and `shipments.hpp`, because it uses the type and both declarations.

## 6. Reading and control: `main.cpp`

**`main.cpp`**:

<!-- example: shipments -->
```cpp
#include <iostream>
#include <string>
#include <vector>

#include "shipments.hpp"

int main() {
    std::vector<Shipment> shipments{};
    int count{0};
    std::cin >> count;

    if (std::cin.fail()) {
        std::cout << "Input error\n";
        return 0;
    }

    if (count < 0 || count > 5) {
        std::cout << "Invalid shipments\n";
        return 0;
    }

    for (int index{0}; index < count; ++index) {
        std::string rest{};
        std::getline(std::cin, rest);

        std::string destination{};
        int boxes{0};
        std::getline(std::cin, destination);
        std::cin >> boxes;

        if (std::cin.fail()) {
            std::cout << "Input error\n";
            return 0;
        }

        if (destination.empty() || boxes < 0) {
            std::cout << "Invalid shipments\n";
            return 0;
        }

        const Shipment shipment{destination, boxes};
        shipments.push_back(shipment);
    }

    print_shipments(shipments);
}
```

- **Reading and checking are as in lesson 10.3:** the number of shipments, finishing the line, `std::cin.fail()` before the rules, a record only after both checks (lesson 10.3, sections 3–6). Only the ending changed.
- **Instead of adding up and printing, there is one call:** `print_shipments(shipments);`. The report is printed only after every shipment has been read successfully.
- **`Input error` and `Invalid shipments` stay in `main`,** because they are the reaction to an error in reading and in controlling the program, not part of the report. On an error, `return 0;` ends the program before the call is reached.
- **`main.cpp` keeps its `#include` lines from lesson 10.3,** because it reads text with `std::getline` and builds the vector itself, and it adds `shipments.hpp`.

## 7. Build and compare the results

Change the `add_executable` line so that it lists three `.cpp` files, on one line, without the header. If CLion added the files, compare it with the one below:

<!-- cmake: shipments -->
```cmake
cmake_minimum_required(VERSION 3.28)
project(first_program LANGUAGES CXX)

add_executable(first_program main.cpp shipments_analysis.cpp shipments_report.cpp)
target_compile_features(first_program PRIVATE cxx_std_20)
set_target_properties(first_program PROPERTIES CXX_EXTENSIONS OFF)
```

Build and run the program as in lesson 11.1, section 5. The build output has three `Building CXX object` lines and one `Linking` line. For data A, the same as in lesson 10.3:

<!-- input: shipments -->
```text
2
North Hub
4
South Depot
7
```

<!-- output: shipments -->
```text
Shipments: 2
North Hub: 4
South Depot: 7
Total boxes: 11
```

**Predict**, then compare the results for data B (an empty list), C (an error in a later record) and D (a word instead of a number). Running them is optional.

<!-- input: shipments -->
```text
0
```

<details>
<summary>Standard output for data B</summary>

<!-- output: shipments -->
```text
Shipments: 0
Total boxes: 0
```

</details>

<!-- input: shipments -->
```text
2
North Hub
4
South Depot
-2
```

<details>
<summary>Standard output for data C</summary>

<!-- output: shipments -->
```text
Invalid shipments
```

</details>

<!-- input: shipments -->
```text
2
North Hub
4
South Depot
seven
```

<details>
<summary>Standard output for data D</summary>

<!-- output: shipments -->
```text
Input error
```

</details>

**The results are exactly as in lesson 10.3,** for the same data. But a correct report for data A doesn't prove that all the rules of lesson 10.3 still work. That's why the program is checked automatically with all 11 cases of that lesson:

<details>
<summary>The other cases of lesson 10.3, checked automatically</summary>

A word instead of the number of shipments:

<!-- input: shipments -->
```text
two
```

<!-- output: shipments -->
```text
Input error
```

3 shipments announced, but only 2 in the data:

<!-- input: shipments -->
```text
3
North Hub
4
South Depot
7
```

<!-- output: shipments -->
```text
Input error
```

A number of shipments outside 0–5:

<!-- input: shipments -->
```text
-1
```

<!-- output: shipments -->
```text
Invalid shipments
```

<!-- input: shipments -->
```text
6
```

<!-- output: shipments -->
```text
Invalid shipments
```

An empty name of a later shipment:

<!-- input: shipments -->
```text
2
North Hub
4

7
```

<!-- output: shipments -->
```text
Invalid shipments
```

One shipment:

<!-- input: shipments -->
```text
1
East Gate
3
```

<!-- output: shipments -->
```text
Shipments: 1
East Gate: 3
Total boxes: 3
```

Five shipments:

<!-- input: shipments -->
```text
5
Central Hub
2
North Hub
4
River Port
0
South Depot
7
West End Depot
1
```

<!-- output: shipments -->
```text
Shipments: 5
Central Hub: 2
North Hub: 4
River Port: 0
South Depot: 7
West End Depot: 1
Total boxes: 14
```

</details>

Data that ends right after the last number, without a line end, gives the same results. The automated tests don't run that case, as in lesson 10.3.

## 8. Mission: workshop orders, in several files

Split your `workshop_orders` program from [the mission of lesson 10.3](../module_10_input_records/lesson_03_building_a_vector_of_records.en.md#8-mission-workshop-orders) by responsibility. In `cpp-workspace`, create a folder `workshop_orders_split` and copy `CMakeLists.txt` into it from `lesson_11_4`. Leave the original unchanged: you'll use it to compare the results. If you don't have that project, recreate it from [the solution of lesson 10.3](../module_10_input_records/lesson_03_building_a_vector_of_records.en.md#example-solutions).

**The agreement doesn't change:** 0 to 5 orders, a non-empty client name with spaces, planned units greater than zero, completed units non-negative and not more than planned. The reading is checked before the rules. A failed read gives `Input error`, a forbidden value `Invalid orders`, and after an error there's no part of the report. The details of reading, spaces, finishing lines and the end of the data are as in lesson 10.3, section 8.

**Requirements:**

1. **A plan first.** Before you create the files, write down a table as in section 2: responsibility, data, file, function, result.
2. **`main.cpp`** reads and checks the data, creates the records, builds the vector, prints the error messages, and calls the report only after success.
3. **A shared header** defines the order type and declares the functions that other files need, with `#pragma once`. It is self-contained.
4. **An analysis file** contains two functions: the remaining units of one order, and the sum of the remaining units of the whole list. It neither reads nor prints.
5. **A report file** prints the number of orders, each order and the total, and takes both values from the analysis functions. The formula for the remaining units stands in one place.
6. **The collection and the elements that are only read** are passed by `const&`.
7. **`add_executable`** lists all three `.cpp` files on one line, without the header.
8. File names consist of lowercase English letters, digits and `_`, and end in `.cpp` or `.hpp`. The example solution uses `orders.hpp`, `orders_analysis.cpp` and `orders_report.cpp`.

The results must be exactly as in lesson 10.3. **Data A:**

<!-- input: orders -->
```text
3
North Library
12 5
City Archive
8 8
Green Workshop
6 0
```

<!-- output: orders -->
```text
Orders: 3
North Library: planned 12, completed 5, remaining 7
City Archive: planned 8, completed 8, remaining 0
Green Workshop: planned 6, completed 0, remaining 6
Remaining total: 13
```

**Data B:**

<!-- input: orders -->
```text
0
```

<!-- output: orders -->
```text
Orders: 0
Remaining total: 0
```

**Data C**, a forbidden value in the second order:

<!-- input: orders -->
```text
2
North Library
12 5
City Archive
8 9
```

<!-- output: orders -->
```text
Invalid orders
```

**Predict D**, a word instead of a number in the second order, and **E**: zero planned units, then a word instead of the second number.

<!-- input: orders -->
```text
2
North Library
12 5
City Archive
8 done
```

<details>
<summary>Standard output for data D</summary>

<!-- output: orders -->
```text
Input error
```

</details>

<!-- input: orders -->
```text
2
North Library
12 5
City Archive
0 done
```

<details>
<summary>Standard output for data E</summary>

<!-- output: orders -->
```text
Input error
```

</details>

E protects the order of lesson 10.3: a failed read takes precedence over checking the values.

**Decide yourself:**

1. what to call the files;
2. what to call the type and its fields;
3. what to call the functions;
4. which functions to declare in the header;
5. which functions to define in the analysis file;
6. which function prepares the report;
7. how the data passes between the functions;
8. which `#include` lines each file needs;
9. which sources to list in `add_executable`;
10. how to compare the results with the one-file version from lesson 10.3.

**Then** build the program and run it for data A and one of the cases B or C. Compare the results with those of the `workshop_orders` project for the same data. Predict the other cases. All 19 cases of lesson 10.3 are checked automatically in the reference solution.

### Success criterion

- The program builds as C++20 and, for data A and for B or C, prints exactly the result shown, the same as the project from lesson 10.3.
- The plan was made before the files, and each file has one role, described in it.
- The type is defined only in the shared header, and the header contains only the type's definition and declarations, with `#pragma once` and the `#include` lines it needs.
- `main.cpp` doesn't calculate remaining units and doesn't print the report's details. The report file doesn't repeat the formula from the analysis file.
- Each function is defined exactly once, in its own `.cpp` file.
- `add_executable` lists three `.cpp` files.

Correct results prove the behaviour, not the organisation: a program with all its code in `main` would print them too. Where the calculations and the report stand, you check against the list above.

<details>
<summary>Hint 1</summary>

How do you separate the part that reads the data from the part that calculates the result? How can you tell where, in the program of lesson 10.3, the reading ends and the report begins?

</details>

<details>
<summary>Hint 2</summary>

Which data and declarations must be shared by several files? Think about who creates the records, who reads them, and who calls whose functions.

</details>

<details>
<summary>Hint 3</summary>

How do you organise the analysis file and the report file so that the formula for the remaining units stands in one place? A function for one order can serve both the sum and the report's lines.

</details>

The example solution is in [Example solutions](#example-solutions).

## 9. Find the bug: the same function in two files

Do this task **after the mission**. Someone was moving the sum into `shipments_analysis.cpp`, but forgot to delete the old version of the function from the report file. Recreate this project: in `cpp-workspace`, create a folder `shipments_twice_check`, copy the five files from `lesson_11_4` into it, and in `shipments_report.cpp` add a second definition of `total_boxes`, the same as in the analysis file:

**`shipments_report.cpp`** in this project:

<!-- file: shipments_twice_check shipments_report.cpp -->
```cpp
#include <iostream>

#include "shipments.hpp"

int total_boxes(const std::vector<Shipment>& shipments) {
    int total{0};

    for (const Shipment& shipment : shipments) {
        total += shipment.boxes;
    }

    return total;
}

void print_shipments(const std::vector<Shipment>& shipments) {
    std::cout << "Shipments: " << shipments.size() << "\n";

    for (const Shipment& shipment : shipments) {
        std::cout << shipment.destination << ": " << shipment.boxes << "\n";
    }

    std::cout << "Total boxes: " << total_boxes(shipments) << "\n";
}
```

<details>
<summary>The other files, unchanged from sections 3–7</summary>

**`main.cpp`**:

<!-- broken: shipments_twice_check stage=link error=multiple definition of .total_boxes\(|duplicate symbol: int __cdecl total_boxes\(|duplicate symbol 'total_boxes\( -->
```cpp
#include <iostream>
#include <string>
#include <vector>

#include "shipments.hpp"

int main() {
    std::vector<Shipment> shipments{};
    int count{0};
    std::cin >> count;

    if (std::cin.fail()) {
        std::cout << "Input error\n";
        return 0;
    }

    if (count < 0 || count > 5) {
        std::cout << "Invalid shipments\n";
        return 0;
    }

    for (int index{0}; index < count; ++index) {
        std::string rest{};
        std::getline(std::cin, rest);

        std::string destination{};
        int boxes{0};
        std::getline(std::cin, destination);
        std::cin >> boxes;

        if (std::cin.fail()) {
            std::cout << "Input error\n";
            return 0;
        }

        if (destination.empty() || boxes < 0) {
            std::cout << "Invalid shipments\n";
            return 0;
        }

        const Shipment shipment{destination, boxes};
        shipments.push_back(shipment);
    }

    print_shipments(shipments);
}
```

**`shipments.hpp`**:

<!-- file: shipments_twice_check shipments.hpp -->
```cpp
#pragma once

#include <string>
#include <vector>

struct Shipment {
    std::string destination;
    int boxes;
};

int total_boxes(const std::vector<Shipment>& shipments);
void print_shipments(const std::vector<Shipment>& shipments);
```

**`shipments_analysis.cpp`**:

<!-- file: shipments_twice_check shipments_analysis.cpp -->
```cpp
#include "shipments.hpp"

int total_boxes(const std::vector<Shipment>& shipments) {
    int total{0};

    for (const Shipment& shipment : shipments) {
        total += shipment.boxes;
    }

    return total;
}
```

**`CMakeLists.txt`**:

<!-- cmake: shipments_twice_check -->
```cmake
cmake_minimum_required(VERSION 3.28)
project(first_program LANGUAGES CXX)

add_executable(first_program main.cpp shipments_analysis.cpp shipments_report.cpp)
target_compile_features(first_program PRIVATE cxx_std_20)
set_target_properties(first_program PROPERTIES CXX_EXTENSIONS OFF)
```

</details>

**Before you build**, answer in writing:

1. **Predict:** at which stage will the build fail, compiling or linking?
2. Is each of the three `.cpp` files, on its own, correct C++ code?
3. How many definitions of `total_boxes` will the linker get?
4. Can `#pragma once` in `shipments.hpp` help here?

**Then:**

5. Build the project. Configure it as a new project in lesson 11.1, section 5.
6. Read the build output: how many files compiled, and what does the linker report?
7. Remove the second definition of `total_boxes` from `shipments_report.cpp`. Keep the definition in `shipments_analysis.cpp`, because the calculations belong in that file.
8. Build the project again and run it for data A of section 7.
9. Explain why removing `shipments_analysis.cpp` from `add_executable` wouldn't be a fix.

<details>
<summary>What happens and why: open after building the broken project</summary>

1. **All three files compile:** there are three `Building CXX object` lines. Each file on its own is correct: `shipments_report.cpp` defines two functions, and `shipments_analysis.cpp` one.
2. **Linking fails,** because the linker gets two definitions of the same ordinary function, from two object files, and doesn't know which one to use. The message names `total_boxes`: on Ubuntu `multiple definition of`, on macOS `duplicate symbol`, on Windows `duplicate symbol:`, and at the end `linker command failed`.
3. **`#pragma once` doesn't help here.** It works within one translation unit (lesson 11.3), and these two definitions stand in two different `.cpp` files, which are compiled separately.
4. **A different error from the earlier ones:**
   - in lesson 11.1 a definition was missing, because its file wasn't built;
   - in lesson 11.2 the definition had another name;
   - in lesson 11.3 a type was defined twice in one translation unit, which the compiler reported;
   - here there are too many definitions of a function, in two units, which the linker reports.
5. **The fix is one definition in the right file.** Removing `shipments_analysis.cpp` from `add_executable` would remove the error, but leave the calculations in the report file, which breaks the split. After the copy is removed, the files are the same as in sections 3–7, and for data A the program prints the same report.

</details>

## 10. When something goes differently

| What you see | What it means | What to do |
|---|---|---|
| `multiple definition of` or `duplicate symbol` with a function's name | The same function is defined in two `.cpp` files (section 9), or a file includes a `.cpp` file. | Keep one definition, in the file responsible for it. Don't include `.cpp` files. |
| `undefined reference`, `undefined symbol` or `referenced from` with `total_boxes` or `print_shipments` | The file with the definition isn't in `add_executable`, or the definition has another name or other parameters than the declaration (lessons 11.1 and 11.2). | Check `add_executable`, and compare the definition with the header. |
| `use of undeclared identifier 'Shipment'` or `unknown type name 'Shipment'` | The file doesn't include `shipments.hpp`. | Add `#include "shipments.hpp"`. |
| `no member named 'cout' in namespace 'std'` in the report file | The file prints, but doesn't include `<iostream>`. | Add `#include <iostream>` to that file. |
| The report differs from lesson 10.3, for example the total stands before the shipments | A different order of statements in the report function. | Compare the order of the lines with the report of lesson 10.3. |
| With invalid data, part of a report appears | The report is called before the reading ends, or despite an error. | Call the report function only after the loop, when all records are valid. |

## 11. Explain

Answer in your own words, preferably in writing. Only then compare with the example answers.

1. What is `main.cpp` responsible for, and what are the other `.cpp` files responsible for?
2. Why does calculating the total stand in a different file from printing the report?
3. Why is `Shipment` defined in the header?
4. Why does the header declare exactly `total_boxes` and `print_shipments`?
5. Which `#include` lines does `shipments_report.cpp` have, and why exactly those?
6. How does `print_shipments` call `total_boxes`, when that function is defined in another file?
7. Why must all three `.cpp` files be in `add_executable`? Does their order set the order in which the program runs?
8. How do you show that the split didn't change how the program works? What doesn't a comparison of standard output alone prove?
9. Why is the same function defined in two `.cpp` files a link error, not a compile error? Could `#pragma once` remove it?
10. Should every function have its own file and a declaration in the shared header?

<details>
<summary>Example answers</summary>

1. `main.cpp` reads and checks the data, builds the vector, prints the error messages and decides whether a report is printed. `shipments_analysis.cpp` calculates the number of boxes, and `shipments_report.cpp` prints the report.
2. Because the calculation doesn't depend on how the report looks. You can change the output format without changing the sum, and check the sum without reading output statements.
3. Because all three `.cpp` files use it: `main.cpp` creates the records, and the others read their fields. A definition in one header isn't copied.
4. Because other files use these functions: `main.cpp` calls `print_shipments`, and `shipments_report.cpp` calls `total_boxes`. The header declares what other files need.
5. `<iostream>`, because the file prints itself, and `shipments.hpp`, because it uses `Shipment` and both declarations. `<string>` and `<vector>` come from the self-contained header, whose declarations need them.
6. The compiler knows `total_boxes` from the declaration in `shipments.hpp`, so it compiles the call. The linker joins it to the definition in `shipments_analysis.cpp`. No file includes a `.cpp` file.
7. Because each of them contains a definition the program needs, and the linker joins only the files in `add_executable`. Their order in the list doesn't matter for how the program runs: it starts with `main`, and functions run when something calls them.
8. Run the program for the same data as in lesson 10.3, invalid data included, and compare the full output. The comparison doesn't prove that the code is split well: a program with all its code in `main` would give the same results. You check the organisation by reading the files.
9. Because each `.cpp` file on its own is correct, and the compiler compiles them separately. Only the linker sees two definitions of the same function. `#pragma once` works within one translation unit, so it won't remove definitions from two different files.
10. No. Related functions may stand in one file, like the two functions in the analysis file of the mission. The header declares only what other files need.

</details>

## Summary

- A larger program is split into files by responsibility: reading and control in `main.cpp`, calculations in one `.cpp` file, the report in another.
- The shared header is an agreement: it defines the shared type and declares the functions that other files need. The `.cpp` files contain the implementation.
- Functions from different `.cpp` files work together through the header's declarations, and the linker joins them. A `.cpp` file isn't included in another.
- Each file includes the headers it needs itself. All `.cpp` files stand in `add_executable`, but their order doesn't set the order of execution.
- Splitting into files doesn't change how the program behaves: you compare the results on the same data, invalid data included.
- The same ordinary function defined in two `.cpp` files is a link error. The fix is one definition in the right file, not `#pragma once`, and not removing files from `add_executable`.
- Not every function needs its own file or a place in the shared header.

## What's next

In lessons 11.1–11.4 the program went from one file to several `.cpp` files with a shared header, each with its own role. In [lesson 11.5: Building a multi-file program (the Module 11 test)](lesson_05_multifile_checkpoint.en.md), you'll design such a program on your own, from the plan to the diagnostics.

---

## Example solutions

Look here **after your own attempt**. Your names may differ, as long as the standard output is as required.

<details>
<summary>Section 8: mission, workshop orders in several files</summary>

**The plan:**

| Responsibility | Data needed | File | Function or operation | Result |
|---|---|---|---|---|
| reading, checking, building the list and control | standard input | `main.cpp` | `main` | a vector of valid orders, or the message `Input error` or `Invalid orders` |
| the shared type and the declarations | — | `orders.hpp` | `struct Order`, the declarations of three functions | an agreement for the other files |
| calculations | one order or the vector of orders | `orders_analysis.cpp` | `remaining_units`, `remaining_total` | remaining units, `int` numbers |
| the report | the vector of orders | `orders_report.cpp` | `print_orders` | the report's lines |

**`orders.hpp`**:

<!-- file: orders orders.hpp -->
```cpp
#pragma once

#include <string>
#include <vector>

struct Order {
    std::string client;
    int planned_units;
    int completed_units;
};

int remaining_units(const Order& order);
int remaining_total(const std::vector<Order>& orders);
void print_orders(const std::vector<Order>& orders);
```

**`orders_analysis.cpp`**:

<!-- file: orders orders_analysis.cpp -->
```cpp
#include "orders.hpp"

int remaining_units(const Order& order) {
    return order.planned_units - order.completed_units;
}

int remaining_total(const std::vector<Order>& orders) {
    int total{0};

    for (const Order& order : orders) {
        total += remaining_units(order);
    }

    return total;
}
```

**`orders_report.cpp`**:

<!-- file: orders orders_report.cpp -->
```cpp
#include <iostream>

#include "orders.hpp"

void print_orders(const std::vector<Order>& orders) {
    std::cout << "Orders: " << orders.size() << "\n";

    for (const Order& order : orders) {
        std::cout << order.client << ": planned " << order.planned_units << ", completed " << order.completed_units
                  << ", remaining " << remaining_units(order) << "\n";
    }

    std::cout << "Remaining total: " << remaining_total(orders) << "\n";
}
```

**`main.cpp`**:

<!-- example: orders -->
```cpp
#include <iostream>
#include <string>
#include <vector>

#include "orders.hpp"

int main() {
    std::vector<Order> orders{};
    int count{0};
    std::cin >> count;

    if (std::cin.fail()) {
        std::cout << "Input error\n";
        return 0;
    }

    if (count < 0 || count > 5) {
        std::cout << "Invalid orders\n";
        return 0;
    }

    for (int index{0}; index < count; ++index) {
        std::string rest{};
        std::getline(std::cin, rest);

        std::string client{};
        int planned_units{0};
        int completed_units{0};
        std::getline(std::cin, client);
        std::cin >> planned_units;
        std::cin >> completed_units;

        if (std::cin.fail()) {
            std::cout << "Input error\n";
            return 0;
        }

        if (client.empty() || planned_units <= 0 || completed_units < 0 || completed_units > planned_units) {
            std::cout << "Invalid orders\n";
            return 0;
        }

        const Order order{client, planned_units, completed_units};
        orders.push_back(order);
    }

    print_orders(orders);
}
```

**`CMakeLists.txt`**:

<!-- cmake: orders -->
```cmake
cmake_minimum_required(VERSION 3.28)
project(first_program LANGUAGES CXX)

add_executable(first_program main.cpp orders_analysis.cpp orders_report.cpp)
target_compile_features(first_program PRIVATE cxx_std_20)
set_target_properties(first_program PROPERTIES CXX_EXTENSIONS OFF)
```

This is one of the correct solutions:

1. **`Order` is defined in `orders.hpp`,** because all three `.cpp` files use it. It's the same type as in lesson 10.3.
2. **The header declares three functions,** because each is used by another file: `main.cpp` calls `print_orders`, and `orders_report.cpp` calls `remaining_units` and `remaining_total`.
3. **`remaining_units` and `remaining_total` stand in one file,** because both belong to the calculations. Not every function needs its own file.
4. **The formula `planned_units - completed_units` stands once,** in `remaining_units`. Both the total and the report's line use it.
5. **The vector and the elements are passed by `const&`,** because the functions only read them.
6. **`orders_analysis.cpp` reads and prints nothing,** and `orders_report.cpp` calculates nothing itself.
7. **`main.cpp` has the reading and checking of lesson 10.3 unchanged,** and instead of adding up and printing, one call `print_orders(orders);` after the loop.
8. **The error messages stay in `main`,** and on an error `return 0;` ends the program before the report. There is no partial report.
9. **`add_executable` lists three `.cpp` files,** on one line, without the header.
10. **The results are as in lesson 10.3** for all 19 cases, because the reading, the rules and the report's format didn't change.

Other correct solutions: other names of the files, the type and the functions; a single analysis function with the loop, if only it calculates remaining units and the report takes them from it; declarations without parameter names.

</details>

<details>
<summary>Section 8: the full list of test cases of lesson 10.3</summary>

The same cases as in the table of lesson 10.3, section 8, with the same results. All of them are checked automatically for the solution above.

A negative number of orders:

<!-- input: orders -->
```text
-1
```

<!-- output: orders -->
```text
Invalid orders
```

One, two and five orders, the same client twice included:

<!-- input: orders -->
```text
1
Harbor Office
10 3
```

<!-- output: orders -->
```text
Orders: 1
Harbor Office: planned 10, completed 3, remaining 7
Remaining total: 7
```

<!-- input: orders -->
```text
2
Park School
9 4
City Archive
8 2
```

<!-- output: orders -->
```text
Orders: 2
Park School: planned 9, completed 4, remaining 5
City Archive: planned 8, completed 2, remaining 6
Remaining total: 11
```

<!-- input: orders -->
```text
5
Art Room
4 1
Book Club
6 6
Art Room
3 0
Main Office
10 9
Tool Shed
2 1
```

<!-- output: orders -->
```text
Orders: 5
Art Room: planned 4, completed 1, remaining 3
Book Club: planned 6, completed 6, remaining 0
Art Room: planned 3, completed 0, remaining 3
Main Office: planned 10, completed 9, remaining 1
Tool Shed: planned 2, completed 1, remaining 1
Remaining total: 8
```

A number of orders greater than 5, and a word instead of the number of orders:

<!-- input: orders -->
```text
6
```

<!-- output: orders -->
```text
Invalid orders
```

<!-- input: orders -->
```text
three
```

<!-- output: orders -->
```text
Input error
```

An empty name of the first and of a later order:

<!-- input: orders -->
```text
2

12 5
City Archive
8 8
```

<!-- output: orders -->
```text
Invalid orders
```

<!-- input: orders -->
```text
2
North Library
12 5

8 8
```

<!-- output: orders -->
```text
Invalid orders
```

Zero planned units, negative planned units and negative completed units:

<!-- input: orders -->
```text
2
North Library
12 5
City Archive
0 0
```

<!-- output: orders -->
```text
Invalid orders
```

<!-- input: orders -->
```text
1
North Library
-4 0
```

<!-- output: orders -->
```text
Invalid orders
```

<!-- input: orders -->
```text
1
North Library
12 -1
```

<!-- output: orders -->
```text
Invalid orders
```

A word instead of the first number, a missing announced order, and a missing last number:

<!-- input: orders -->
```text
2
North Library
twelve 5
City Archive
8 8
```

<!-- output: orders -->
```text
Input error
```

<!-- input: orders -->
```text
2
North Library
12 5
```

<!-- output: orders -->
```text
Input error
```

<!-- input: orders -->
```text
2
North Library
12 5
City Archive
8
```

<!-- output: orders -->
```text
Input error
```

</details>

<details>
<summary>Section 9: the fixed project</summary>

After the second definition of `total_boxes` is removed from `shipments_report.cpp`, all five files are the same as in sections 3–7. The summing function is defined once, in `shipments_analysis.cpp`, and the report file calls it. The program builds and, for data A, prints the same report as in section 7. This project, with all 11 cases, is checked automatically.

</details>

**Previous lesson:** [Lesson 11.3: A shared type in a header](lesson_03_shared_type_in_header.en.md) · **Next lesson:** [Lesson 11.5: Building a multi-file program (the Module 11 test)](lesson_05_multifile_checkpoint.en.md) · [Course overview](../../README.en.md)

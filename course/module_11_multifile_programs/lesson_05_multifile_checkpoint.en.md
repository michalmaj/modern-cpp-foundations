# Lesson 11.5: Checkpoint — Building a Multi-File Program

[Polski](lesson_05_multifile_checkpoint.md) · **English** · [Course overview](../../README.en.md)

> **Module 11, lesson 5: the checkpoint** · about 100–120 minutes, in two sessions
> **You need:** your `cpp-workspace` folder and the original `lesson_05_first_program` project.
> **Pilot version.** The reference solution and the diagnostic project are checked automatically on Windows, Ubuntu and macOS, with the given input data. Nothing grades your own project automatically: you check it yourself, against the criteria. The steps in CLion are the same as in lessons 11.1–11.4, and haven't been checked by hand on every system.

## How this checkpoint works

This lesson introduces nothing new. You check whether you can **design, build and check a small program in several files on your own**, with no ready split and no ready functions. In it you combine lessons 11.1–11.4 with reading a list of records from lesson 10.3.

The checkpoint has three parts and a discussion:

- **Part A: the design.** A plan of how to split the program into files, before you write code.
- **Part B: implementation and testing.** The program according to the specification, checked with the check cases. This is the largest part of the work.
- **Part C: diagnostics and justification.** A link error in a ready project, and questions about your decisions. Do it after Part B.
- **Checking and discussion:** hints, the full list of cases, the diagnostic project, the reference solution, answers and a self-assessment. Go there only after Parts A and B, or when you consciously give up further attempts on your own.

Looking at the hints or at earlier lessons isn't a failure. What matters is **to note honestly what was done on your own and what with help**. A suggested split into two sessions:

- **first:** the specification, Part A and the shared header;
- **second:** the `.cpp` files, `CMakeLists.txt`, the check cases and Part C.

**You may use:** CLion or the terminal, CMake and Ninja, as before; a `CMakeLists.txt` copied from the original `lesson_05_first_program`; lessons 10.3 and 11.1–11.4 as reminders; case tables. You won't need the debugger. Everything you need, you know from Modules 1–11.

---

## The specification: free seats in workshop rooms

An organiser runs several workshop rooms. For each one, they know its name, how many seats it has in total and how many of them are already taken. The program reads the list of rooms and prints how many free seats each room has, and how many there are in total. It doesn't model dates, bookings or participants.

**Preparation:** in `cpp-workspace`, create a folder `workshop_rooms` and copy `CMakeLists.txt` into it from the original `lesson_05_first_program`. You'll create the other files on your own.

### Input data

The first line gives the number of rooms. Then each room takes two lines:

1. the room's name, which may contain spaces;
2. two integers separated by a space: the capacity, which is the total number of seats, and the number of occupied seats.

### Rules

- There are 0 to 5 rooms.
- A room's name must not be empty. Data that follows the agreement has no spaces at its start or end, and the program neither checks nor removes them. Names may repeat: each room is a separate record.
- The capacity is from 1 to 100.
- The number of occupied seats is from 0 to the room's capacity.
- All data is ASCII text. Text after the second number is outside the agreement, and the program doesn't check it.

### Errors

- When the required data can't be read, the program prints exactly `Input error`.
- When the reading succeeded, but the number of rooms or the values of some room break the rules, the program prints exactly `Invalid rooms`.
- At the first error, the program prints the message and ends, with no part of the report.
- **Reading first, then the rules,** as in lesson 10.3: the program checks whether reading **both** numbers of the current room succeeded, and only then their values. After a failed read, it doesn't try to read any further.

### The report

For valid data, the program prints the number of rooms, one line per room, in the order of the data, and the total number of free seats:

```text
Rooms: NUMBER_OF_ROOMS
NAME: capacity CAPACITY, occupied OCCUPIED, free FREE
Free seats total: TOTAL
```

A room's free seats are its capacity minus its occupied seats, and the total is the sum of the free seats of all rooms. **The calculation of free seats stands in one place in the program.** The program doesn't sort the rooms or remove repeats.

### The required structure

- **`main.cpp`** reads and checks the data, builds the collection of rooms, prints the error messages, and starts the report only after every room has been read successfully.
- **At least one shared header,** self-contained, with `#pragma once`: the room type, and the declarations of the functions that other files need.
- **A separate `.cpp` file with the calculations:** the free seats of one room, and their sum for all rooms. It doesn't read, print or change records.
- **A separate `.cpp` file with the report:** it prints the report and uses the calculation functions.
- **`CMakeLists.txt`** from lesson 0.5, in which `add_executable(first_program ...)` lists all the `.cpp` files needed.

Don't include `.cpp` files with `#include`, and don't copy function definitions between files. A program whose code all stands in `main.cpp` doesn't meet the requirements, even if it prints the right results.

**Decide yourself:**

1. what to call the calculation file, the report file and the header;
2. what to call the room type;
3. what to call its fields;
4. what to call the functions;
5. which parameters the functions have;
6. which types they return;
7. which declarations other files need;
8. how to split the calculations and the report;
9. which standard headers each file includes;
10. which files to list in `add_executable`;
11. how to pass the collection of rooms;
12. how to check that the solution is correct.

You'll find reminders in lessons [11.1](lesson_01_second_source_file.en.md) (a second file and `add_executable`), [11.2](lesson_02_own_header_file.en.md) (a header), [11.3](lesson_03_shared_type_in_header.en.md) (a type in a header) and [11.4](lesson_04_splitting_responsibilities.en.md) (splitting by responsibility), and reading a list of records in [lesson 10.3](../module_10_input_records/lesson_03_building_a_vector_of_records.en.md).

---

# Part A: the design

Before you write code, prepare in writing a table for all the files of your project:

| File | Responsibility | Input data | Result |
|---|---|---|---|
| | | | |

Also answer briefly:

1. What must be shared by several files?
2. Which functions can stay a detail of one `.cpp` file?
3. In which file does the program start running?
4. Which files does CMake compile?
5. How does the result of the calculations reach the report?

The plan is a required part of the checkpoint, and it is assessed together with the program.

---

# Part B: implementation and testing

Write the program according to the specification and your plan. **Before running it,** prepare a case table: the data and the predicted result. The results below follow directly from the agreement.

**A**, three rooms: names with spaces, a partly occupied room, a full one and an empty one:

<!-- input: rooms -->
```text
3
North Hall
12 7
South Lab
8 8
Quiet Room
6 0
```

<!-- output: rooms -->
```text
Rooms: 3
North Hall: capacity 12, occupied 7, free 5
South Lab: capacity 8, occupied 8, free 0
Quiet Room: capacity 6, occupied 0, free 6
Free seats total: 11
```

**B**, no rooms:

<!-- input: rooms -->
```text
0
```

<!-- output: rooms -->
```text
Rooms: 0
Free seats total: 0
```

**C**, the second room has more occupied seats than its capacity. The first room was valid, but there's no partial report:

<!-- input: rooms -->
```text
2
North Hall
12 7
South Lab
8 9
```

<!-- output: rooms -->
```text
Invalid rooms
```

**D**, a word instead of the number of occupied seats in the second room:

<!-- input: rooms -->
```text
2
North Hall
12 7
South Lab
8 done
```

<!-- output: rooms -->
```text
Input error
```

**E**, capacity 0 in the second room, then a word instead of the second number. A failed read takes precedence over checking the values, so this isn't `Invalid rooms`:

<!-- input: rooms -->
```text
2
North Hall
12 7
South Lab
0 done
```

<!-- output: rooms -->
```text
Input error
```

**F**, an empty room name:

<!-- input: rooms -->
```text
1

12 7
```

<!-- output: rooms -->
```text
Invalid rooms
```

**G**, capacity 0:

<!-- input: rooms -->
```text
1
North Hall
0 0
```

<!-- output: rooms -->
```text
Invalid rooms
```

**H**, more than 5 rooms:

<!-- input: rooms -->
```text
6
```

<!-- output: rooms -->
```text
Invalid rooms
```

**I**, a word instead of the number of rooms:

<!-- input: rooms -->
```text
three
```

<!-- output: rooms -->
```text
Input error
```

**J**, two rooms with the same name: both stay in the report:

<!-- input: rooms -->
```text
2
East Wing
10 3
East Wing
5 0
```

<!-- output: rooms -->
```text
Rooms: 2
East Wing: capacity 10, occupied 3, free 7
East Wing: capacity 5, occupied 0, free 5
Free seats total: 12
```

**Run these, they're required:** A, B, and one of the cases C or D. Predict the others in your table, and compare them with the full list of cases in "Checking and discussion". All of them are checked automatically for the reference solution. Data that ends right after the last number, without a line end, gives the same result. The automated tests don't run that case, as in lesson 10.3.

---

# Part C: diagnostics and justification

Do this part **after Part B**.

## Diagnostics: a missing definition

The `rooms_link_check` project is in [Checking and discussion](#the-diagnostic-project). Its file names are fixed: `main.cpp`, `rooms.hpp`, `rooms_analysis.cpp`, `rooms_report.cpp` and `CMakeLists.txt`. It contains code very close to the reference solution, so open it only now. Recreate it in a folder `rooms_link_check`, build it and:

1. find out at which stage the build fails;
2. explain what the message about a missing definition means;
3. check the declarations in the header and the definitions in the `.cpp` files;
4. check the list of files in `add_executable`;
5. fix the project, build it again and run it for data A;
6. explain why `#include "rooms_analysis.cpp"` isn't the right fix.

**Finally, in writing:** how does this problem differ from the situation in which the same function is defined in two `.cpp` files?

## Justification

Answer in your own words, referring to your project:

1. What is the shared header in your project for, and what stands in it?
2. How does a function's declaration differ from its definition? Where does each one stand?
3. Why does no file include a `.cpp` file?
4. Must every one of your functions be declared in the shared header?
5. Why must the `.cpp` files be listed in `add_executable`?
6. How can you tell whether an error comes from compiling or from linking?
7. Why do the calculations stand in a different file from the report?
8. What does passing the collection of rooms by `const&` give?
9. What don't the check cases tell you about the program's structure? How do you check that a change of the split didn't change how it works?

---

## Checklist before you hand it in

- [ ] The plan of Part A was made before the code, and it matches the program.
- [ ] The room type is defined once, in a shared header with `#pragma once`, which itself includes the standard headers it needs.
- [ ] The header contains the type's definition and declarations, with no function definitions.
- [ ] The calculations and the report stand in two separate `.cpp` files, and each function is defined exactly once.
- [ ] One function calculates free seats, and the total and the report use it.
- [ ] The calculation file reads and prints nothing.
- [ ] The collection and the elements that are only read are passed by `const&`.
- [ ] `main.cpp` checks reading both numbers before the rules, and on an error ends with no part of the report.
- [ ] `add_executable` lists all the `.cpp` files, without the header, and no file includes a `.cpp` file.
- [ ] For A, B and C or D, the result matches character by character, and the other cases in your table match the full list.
- [ ] Part C is done.

## Assessment criteria

The rubric is for self-assessment, or for assessment by a teacher. The course has no grading scale and no points threshold: the points show which areas are mastered and which need revision.

| Area | Points | Full points when |
|---|---:|---|
| The plan of responsibilities | 15 | the table was made before the code, each file has its role, data and result described, and the answers to the five questions match the program |
| The shared header, the type and the declarations | 15 | the type is defined once, the header has `#pragma once`, is self-contained, and declares the functions that other files need, without their definitions |
| The implementation files and CMake | 15 | calculations and report in separate `.cpp` files, each function defined once, no file includes a `.cpp` file, and `add_executable` lists all the `.cpp` files |
| Reading and checking the data | 20 | reading both numbers is checked before the rules, all the rules are checked, the messages are exact, and after an error there's no part of the report |
| Calculations, the report and passing data | 15 | one function calculates free seats, the total uses it, the report takes both values from the calculations, and the collection and elements are passed by `const&` |
| Correct results and testing | 10 | A, B and C or D give the exact result, and the case table was made before running and matches the full list |
| Diagnostics and justification | 10 | the link error is recognised and fixed through `add_executable`, and the answers of Part C are correct and refer to the project |
| **Total** | **100** | |

- **A correct result doesn't automatically give all the points:** the plan, header and file areas are assessed by reading the project.
- **A program in one file** doesn't meet the structure requirements: it gets no points for the header, or for the implementation files and CMake, even with a correct result.
- **A wrong `add_executable`**, for example without the calculation file, or with an included `.cpp` file, means no points for the implementation files and CMake.
- **A partial report after an error** breaks the agreement: it means no points for reading and checking the data in that area.
- **Other names** of the type, fields, functions and files don't cost points. A different, justified split, for example two headers, is assessed by the same competences, not by matching the reference solution.

**What is checked automatically, and what isn't.** The course's tests check that the reference solution builds and gives the results shown. Your runs of the check cases check how your program behaves for that data. **The quality of the split, independence and justification are checked by no automaton:** a person assesses them by reading the plan and the files.

---

# Checking and discussion

Come here **only after Parts A and B**, or when you consciously give up further attempts on your own. Further on there is code very close to the solution.

## Hints

<details>
<summary>Hint 1: the structure</summary>

Which actions of the program depend on the input data, which only calculate, and which only print? Give each of these groups one file.

</details>

<details>
<summary>Hint 2: the interface</summary>

Which type and which functions are used in more than one file? They belong in the shared header. Remember which standard headers the declarations themselves need.

</details>

<details>
<summary>Hint 3: the flow and CMake</summary>

`main` passes the finished collection to the report, and the report asks the calculations for the free seats of one room and for the total. The linker joins these calls only to definitions from the files listed in `add_executable`.

</details>

## The full list of check cases

<details>
<summary>Cases K–T, checked automatically for the reference solution</summary>

**K**, one room with the largest capacity:

<!-- input: rooms -->
```text
1
Main Hall
100 99
```

<!-- output: rooms -->
```text
Rooms: 1
Main Hall: capacity 100, occupied 99, free 1
Free seats total: 1
```

**L**, five rooms, one with capacity 1 included:

<!-- input: rooms -->
```text
5
Room One
10 2
Room Two
20 20
Room Three
1 0
Room Four
100 50
Room Five
7 3
```

<!-- output: rooms -->
```text
Rooms: 5
Room One: capacity 10, occupied 2, free 8
Room Two: capacity 20, occupied 20, free 0
Room Three: capacity 1, occupied 0, free 1
Room Four: capacity 100, occupied 50, free 50
Room Five: capacity 7, occupied 3, free 4
Free seats total: 63
```

**M**, a negative number of rooms:

<!-- input: rooms -->
```text
-1
```

<!-- output: rooms -->
```text
Invalid rooms
```

**N**, a negative capacity:

<!-- input: rooms -->
```text
1
North Hall
-5 0
```

<!-- output: rooms -->
```text
Invalid rooms
```

**O**, capacity 101:

<!-- input: rooms -->
```text
1
North Hall
101 0
```

<!-- output: rooms -->
```text
Invalid rooms
```

**P**, a negative number of occupied seats:

<!-- input: rooms -->
```text
1
North Hall
12 -1
```

<!-- output: rooms -->
```text
Invalid rooms
```

**Q**, 2 rooms announced, but the data ends where the second name should be. This isn't an empty name, as in F, but a failed read:

<!-- input: rooms -->
```text
2
North Hall
12 7
```

<!-- output: rooms -->
```text
Input error
```

**R**, both numbers of the room missing:

<!-- input: rooms -->
```text
1
North Hall
```

<!-- output: rooms -->
```text
Input error
```

**S**, the second number of the room missing:

<!-- input: rooms -->
```text
1
North Hall
12
```

<!-- output: rooms -->
```text
Input error
```

**T**, a word instead of the capacity:

<!-- input: rooms -->
```text
1
North Hall
twelve 7
```

<!-- output: rooms -->
```text
Input error
```

</details>

## The diagnostic project

<details>
<summary>The rooms_link_check project: open after Part B</summary>

**`CMakeLists.txt`**:

<!-- cmake: rooms_link_check -->
```cmake
cmake_minimum_required(VERSION 3.28)
project(first_program LANGUAGES CXX)

add_executable(first_program main.cpp rooms_report.cpp)
target_compile_features(first_program PRIVATE cxx_std_20)
set_target_properties(first_program PROPERTIES CXX_EXTENSIONS OFF)
```

**`main.cpp`**:

<!-- broken: rooms_link_check stage=link error=undefined reference to .free_seats\(Room const&\)'|undefined symbol: int __cdecl free_seats\(struct Room const &\)|"free_seats\(Room const&\)", referenced from -->
```cpp
#include <iostream>
#include <string>
#include <vector>

#include "rooms.hpp"

int main() {
    std::vector<Room> rooms{};
    int count{0};
    std::cin >> count;

    if (std::cin.fail()) {
        std::cout << "Input error\n";
        return 0;
    }

    if (count < 0 || count > 5) {
        std::cout << "Invalid rooms\n";
        return 0;
    }

    for (int index{0}; index < count; ++index) {
        std::string rest{};
        std::getline(std::cin, rest);

        std::string name{};
        int capacity{0};
        int occupied{0};
        std::getline(std::cin, name);
        std::cin >> capacity;
        std::cin >> occupied;

        if (std::cin.fail()) {
            std::cout << "Input error\n";
            return 0;
        }

        if (name.empty() || capacity < 1 || capacity > 100 || occupied < 0 || occupied > capacity) {
            std::cout << "Invalid rooms\n";
            return 0;
        }

        const Room room{name, capacity, occupied};
        rooms.push_back(room);
    }

    print_rooms(rooms);
}
```

**`rooms.hpp`**:

<!-- file: rooms_link_check rooms.hpp -->
```cpp
#pragma once

#include <string>
#include <vector>

struct Room {
    std::string name;
    int capacity;
    int occupied;
};

int free_seats(const Room& room);
int free_seats_total(const std::vector<Room>& rooms);
void print_rooms(const std::vector<Room>& rooms);
```

**`rooms_analysis.cpp`**:

<!-- file: rooms_link_check rooms_analysis.cpp -->
```cpp
#include "rooms.hpp"

int free_seats(const Room& room) {
    return room.capacity - room.occupied;
}

int free_seats_total(const std::vector<Room>& rooms) {
    int total{0};

    for (const Room& room : rooms) {
        total += free_seats(room);
    }

    return total;
}
```

**`rooms_report.cpp`**:

<!-- file: rooms_link_check rooms_report.cpp -->
```cpp
#include <iostream>

#include "rooms.hpp"

void print_rooms(const std::vector<Room>& rooms) {
    std::cout << "Rooms: " << rooms.size() << "\n";

    for (const Room& room : rooms) {
        std::cout << room.name << ": capacity " << room.capacity << ", occupied " << room.occupied
                  << ", free " << free_seats(room) << "\n";
    }

    std::cout << "Free seats total: " << free_seats_total(rooms) << "\n";
}
```

</details>

## The reference solution

<details>
<summary>The plan and the five files of the reference solution</summary>

This is one of the correct solutions, not the only acceptable structure.

| File | Responsibility | Input data | Result |
|---|---|---|---|
| `main.cpp` | reading, checking the data, building the collection and control | standard input | a vector of valid rooms, or the message `Input error` or `Invalid rooms` |
| `rooms.hpp` | the shared type and the declarations | — | `struct Room` and the declarations of three functions |
| `rooms_analysis.cpp` | calculations | one room or the vector of rooms | a room's free seats and their total, `int` numbers |
| `rooms_report.cpp` | the report | the vector of rooms | the report's lines on standard output |

**`rooms.hpp`**:

<!-- file: rooms rooms.hpp -->
```cpp
#pragma once

#include <string>
#include <vector>

struct Room {
    std::string name;
    int capacity;
    int occupied;
};

int free_seats(const Room& room);
int free_seats_total(const std::vector<Room>& rooms);
void print_rooms(const std::vector<Room>& rooms);
```

**`rooms_analysis.cpp`**:

<!-- file: rooms rooms_analysis.cpp -->
```cpp
#include "rooms.hpp"

int free_seats(const Room& room) {
    return room.capacity - room.occupied;
}

int free_seats_total(const std::vector<Room>& rooms) {
    int total{0};

    for (const Room& room : rooms) {
        total += free_seats(room);
    }

    return total;
}
```

**`rooms_report.cpp`**:

<!-- file: rooms rooms_report.cpp -->
```cpp
#include <iostream>

#include "rooms.hpp"

void print_rooms(const std::vector<Room>& rooms) {
    std::cout << "Rooms: " << rooms.size() << "\n";

    for (const Room& room : rooms) {
        std::cout << room.name << ": capacity " << room.capacity << ", occupied " << room.occupied
                  << ", free " << free_seats(room) << "\n";
    }

    std::cout << "Free seats total: " << free_seats_total(rooms) << "\n";
}
```

**`main.cpp`**:

<!-- example: rooms -->
```cpp
#include <iostream>
#include <string>
#include <vector>

#include "rooms.hpp"

int main() {
    std::vector<Room> rooms{};
    int count{0};
    std::cin >> count;

    if (std::cin.fail()) {
        std::cout << "Input error\n";
        return 0;
    }

    if (count < 0 || count > 5) {
        std::cout << "Invalid rooms\n";
        return 0;
    }

    for (int index{0}; index < count; ++index) {
        std::string rest{};
        std::getline(std::cin, rest);

        std::string name{};
        int capacity{0};
        int occupied{0};
        std::getline(std::cin, name);
        std::cin >> capacity;
        std::cin >> occupied;

        if (std::cin.fail()) {
            std::cout << "Input error\n";
            return 0;
        }

        if (name.empty() || capacity < 1 || capacity > 100 || occupied < 0 || occupied > capacity) {
            std::cout << "Invalid rooms\n";
            return 0;
        }

        const Room room{name, capacity, occupied};
        rooms.push_back(room);
    }

    print_rooms(rooms);
}
```

**`CMakeLists.txt`**:

<!-- cmake: rooms -->
```cmake
cmake_minimum_required(VERSION 3.28)
project(first_program LANGUAGES CXX)

add_executable(first_program main.cpp rooms_analysis.cpp rooms_report.cpp)
target_compile_features(first_program PRIVATE cxx_std_20)
set_target_properties(first_program PROPERTIES CXX_EXTENSIONS OFF)
```

1. **`Room` is defined in `rooms.hpp`,** because all three `.cpp` files use it. The header itself includes `<string>` and `<vector>`, which its declarations need.
2. **The header declares three functions,** because each is used by another file: `main.cpp` calls `print_rooms`, and `rooms_report.cpp` calls `free_seats` and `free_seats_total`.
3. **The formula `room.capacity - room.occupied` stands once,** in `free_seats`. Both the total and the report's line use it.
4. **`free_seats_total` adds up the results of `free_seats`,** instead of repeating the formula.
5. **The collection and the elements are passed by `const&`,** because the functions only read them.
6. **`rooms_analysis.cpp` reads and prints nothing,** and `rooms_report.cpp` calculates nothing itself.
7. **`main.cpp` finishes the number line before each name** with `std::getline` into the variable `rest`, as in lesson 10.3. So an empty name stays an empty text, instead of being skipped.
8. **Reading both numbers is checked with one `std::cin.fail()` before the rules,** so for E the result is `Input error`. On an error, `return 0;` ends the program before `print_rooms` is called, so there's no partial report.
9. **A record is created and added to the vector only after both checks,** and the report describes the vector: the number of rooms comes from `size()`.
10. **`add_executable` lists three `.cpp` files,** on one line, without the header.

Other correct solutions: other names; the calculations and the report in files with other names; one header for the type and a second for the declarations, if the second includes the first itself; a single analysis function, if the formula still stands in one place.

</details>

## Diagnostics: explanation and fix

<details>
<summary>Open after doing the diagnostics</summary>

1. **Two files compile:** `main.cpp` and `rooms_report.cpp`, because only they are in `add_executable`. Both are correct: they know `free_seats` and `free_seats_total` from the declarations in `rooms.hpp`.
2. **Linking fails,** because `rooms_report.cpp` calls these functions, and their definitions stand in `rooms_analysis.cpp`, which nobody compiles. The message names the missing functions: on Ubuntu `undefined reference to`, on macOS `referenced from`, on Windows `undefined symbol:`, and at the end `linker command failed`. There's no program.
3. **The declarations and the definitions are correct** and match each other. The problem is only in the list of files.
4. **The fix:** add `rooms_analysis.cpp` to `add_executable`, that is, `add_executable(first_program main.cpp rooms_analysis.cpp rooms_report.cpp)`, and in CLion reload the CMake project (lesson 11.1). After building, the program prints the report of Part B for data A, because the files are the same as in the reference solution.
5. **`#include "rooms_analysis.cpp"` isn't a fix.** It would put the definitions into the file that includes it: in this project the error would disappear, but when someone later adds `rooms_analysis.cpp` to `add_executable`, the same functions will be defined twice. The linker joins `.cpp` files, not `#include` (lesson 11.2).

**The answer to the question of Part C.** Here a definition is missing: the call has nothing to be joined to, the linker reports `undefined reference` or `undefined symbol`, and the fix is adding the file to `add_executable`. When the same function is defined in two `.cpp` files, there are too many definitions: the linker reports `multiple definition` or `duplicate symbol`, and the fix is removing one definition (lesson 11.4). In both cases each file compiles on its own, and the linker reports the error.

</details>

## Answers to the questions of Part C

<details>
<summary>Example answers, for the reference solution</summary>

1. So that the room type and the functions' declarations exist in one place. The header defines `Room` and declares the functions that other files use.
2. A declaration gives the name, the result type and the parameters, with a semicolon: it stands in the header. A definition also contains the function's body: it stands in one `.cpp` file.
3. Because an included `.cpp` file would put definitions into another translation unit, and the linker joins `.cpp` files. It would risk a double definition.
4. No. The header declares the functions that other files need. A helper function used only in one `.cpp` file doesn't have to go there.
5. Because CMake compiles and links only the files in this list. A file outside the list doesn't get into the program, so its definitions are missing when linking.
6. A compile error points to a file and a line in the code, and appears at `Building CXX object`. A link error appears only at `Linking`, names a function, and ends with `linker command failed`.
7. Because the calculation doesn't depend on how the report looks. You can change the output format without changing the calculations, and check the calculations without reading the output code.
8. The function reads the existing collection without copying it and without a way to change it.
9. The cases check the behaviour, not the split: a program in one file would give the same results. You check the structure by reading the files. You check the behaviour after a change of the split by running the same cases, invalid ones included, and comparing the full results.

</details>

## Self-assessment

For each competence, mark one answer:

| Competence | On my own | With a hint | After looking at the solution | To revise |
|---|---|---|---|---|
| A plan of the files' responsibilities | | | | |
| Declarations and definitions in the right files | | | | |
| A shared type in a header | | | | |
| The `#include` lines each file needs | | | | |
| Passing data between functions and files | | | | |
| Calculations apart from the report | | | | |
| `add_executable` with all the `.cpp` files | | | | |
| The input and output agreement, with no partial report | | | | |
| Compile errors and link errors | | | | |
| Normal, boundary and invalid cases | | | | |

If something is marked in the "To revise" column, go back to the relevant lesson:

| Topic | Lesson |
|---|---|
| a second source file, `add_executable`, a missing file when linking | [11.1](lesson_01_second_source_file.en.md) |
| your own header, `#include "..."`, a declaration versus a definition | [11.2](lesson_02_own_header_file.en.md) |
| a type in a header, `#pragma once`, a self-contained header | [11.3](lesson_03_shared_type_in_header.en.md) |
| splitting by responsibility, a double definition | [11.4](lesson_04_splitting_responsibilities.en.md) |
| reading a list of records, reading first, then the rules | [10.3](../module_10_input_records/lesson_03_building_a_vector_of_records.en.md) |

---

## Module 11 summary

After five lessons you can:

- build a program from several `.cpp` files and list them in `add_executable`;
- keep functions' declarations and shared types in your own self-contained header with `#pragma once`;
- split a program by responsibility: reading and control, calculations, and the report;
- call functions defined in other files through the header's declarations, without including `.cpp` files;
- tell compile errors from link errors: a missing definition and a double definition;
- check that a change in how the files are organised didn't change how the program works.

## What's next

This is the end of Module 11. The next module of the course is in preparation.

**Previous lesson:** [Lesson 11.4: Splitting a program by responsibility](lesson_04_splitting_responsibilities.en.md) · **Next lesson:** in preparation · [Course overview](../../README.en.md)

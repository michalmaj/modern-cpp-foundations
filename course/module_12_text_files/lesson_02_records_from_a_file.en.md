# Lesson 12.2: Records from a file: the same reading function

[Polski](lesson_02_records_from_a_file.md) · **English** · [Course overview](../../README.en.md)

> **Module 12, lesson 2** · about 90–110 minutes, can be split into two sessions
> **You need:** your `cpp-workspace` folder and the original `lesson_05_first_program` project, as before. You won't need the debugger in this lesson.
> **Pilot version.** The programs in this lesson are checked automatically on Windows, Ubuntu and macOS, with the given data files and input data. The steps in CLion (a new file, the **Working directory** field) are the same as in lesson 12.1: they are described according to the CLion 2026.3 documentation, without a manual check on every system.

## Before you start

This lesson assumes that you:

- know the program of lesson 10.4: the function `read_shipment_values` gets the stream through `std::istream&`, the name through `const std::string&` and the result record through `Shipment&`, while `main` reads the names, recognises the ending of the data and, after a refusal, tells `Input error` from `Invalid shipments` with `fail()`;
- remember that a parameter with `&` is another name for the object passed in the call, and that a parameter without `&` is its copy (lesson 9.1);
- read a name with `std::getline`, a number with `>>`, and finish the number line with `std::getline` (lesson 10.2);
- open a file with `std::ifstream`, check opening with `fail()`, create a data file in a project and check the **Working directory** field (lesson 12.1).

## The situation

In lesson 10.4 the program read the list of shipments from the keyboard, so on every run it had to be typed again. Now the same list is in a file, `shipments.txt`. The program should read it and print the same report as then.

Is a new reading function needed, for example `read_shipment_from_file`? No. The function `read_shipment_values` of lesson 10.4 never mentions `std::cin`: it reads from its parameter `input`, that is, from the stream it's given in the call. **You'll change only the calling code: `main` decides where the data come from.** The function stays unchanged, character for character.

After this lesson you will:

- pass the same function with a `std::istream&` parameter `std::cin` once, and an open `std::ifstream` another time;
- split the responsibility: the calling code chooses and opens the data source, and the function reads from whatever stream it's given;
- check that both sources give the same result for the same data;
- state a program's data contract and point out its limits, for example an empty line in the middle of a file;
- recognise the compile error that appears when a stream is passed by value.

## 1. What the function knows about the stream

The function's header from lesson 10.4:

<!-- fragment -->
```cpp
bool read_shipment_values(std::istream& input, const std::string& destination, Shipment& result)
```

The body of this function has no `std::cin`, no file name and no `std::cout`. The function knows only this:

- it gets an input stream, reads from it with `>>` and checks its state with `fail()`;
- it gets a ready, non-empty name and a record to fill;
- it has to read one number, check it and, on success, fill the record.

It doesn't know whether the data come from the keyboard or from a file, what that file is called, or who opened it. It doesn't need to: reading a number looks the same in both cases.

**A reminder: `std::istream&`.** `std::istream` is the type of an input stream, and `std::cin` is an object of that type (lesson 10.4). `&` means that the parameter `input` is another name for the object passed in the call: the function gets no copy, it works on the caller's stream. `input >> boxes` takes characters from that same stream, so after the function returns, `main` reads on from where the function stopped. There's no `const`, because reading changes the stream: it moves the reading position and may change its state.

**Why can a file be passed?** `std::ifstream` from lesson 12.1 is an input stream from a file. The standard library defines it as a particular kind of `std::istream`, so it has everything the function needs from an input stream: `>>`, `fail()` and working with `std::getline`. That's why you can pass an open `std::ifstream` wherever a function expects `std::istream&`. The parameter `input` then becomes another name for the file stream.

`std::cin` and the file stream are still two different objects with different data sources: one reads from the keyboard, the other from a file. What they share is the way they're used, and that's enough for the function. How the library arranges this inside isn't needed in this course.

## 2. The starting point: the keyboard version

In `cpp-workspace`, create a folder `lesson_12_2` and copy `main.cpp` and `CMakeLists.txt` from the original `lesson_05_first_program` into it. Open the folder in CLion (**File | Open**, then **Trust Project** and the **Debug** profile) and replace the contents of `main.cpp` with the program of lesson 10.4, section 2. The same program is in the collapsed block below.

<details>
<summary>The program of lesson 10.4: the keyboard version</summary>

<!-- example: shipments_keyboard -->
```cpp
#include <iostream>
#include <string>
#include <vector>

struct Shipment {
    std::string destination;
    int boxes;
};

bool read_shipment_values(std::istream& input, const std::string& destination, Shipment& result) {
    int boxes{0};
    input >> boxes;

    if (input.fail()) {
        return false;
    }

    if (boxes < 0) {
        return false;
    }

    result = Shipment{destination, boxes};
    return true;
}

int main() {
    std::vector<Shipment> shipments{};
    std::string destination{};
    std::getline(std::cin, destination);

    while (!std::cin.fail() && !destination.empty()) {
        Shipment shipment{"", 0};
        const bool accepted{read_shipment_values(std::cin, destination, shipment)};

        if (!accepted) {
            if (std::cin.fail()) {
                std::cout << "Input error\n";
            } else {
                std::cout << "Invalid shipments\n";
            }

            return 0;
        }

        shipments.push_back(shipment);

        std::string rest{};
        std::getline(std::cin, rest);

        if (!std::cin.fail()) {
            std::getline(std::cin, destination);
        }
    }

    int total_boxes{0};
    std::cout << "Shipments: " << shipments.size() << "\n";

    for (const Shipment& shipment : shipments) {
        std::cout << shipment.destination << ": " << shipment.boxes << "\n";
        total_boxes += shipment.boxes;
    }

    std::cout << "Total boxes: " << total_boxes << "\n";
}
```

</details>

Build and run the program. In the **Run** window, type the data, and at the end press **Enter** on an empty line, as in lesson 10.4:

<!-- input: shipments_keyboard -->
```text
North Hub
4
South Depot
7

```

<!-- output: shipments_keyboard -->
```text
Shipments: 2
North Hub: 4
South Depot: 7
Total boxes: 11
```

This is the first required run. Remember this report: in a moment the same data will reach the program from a file.

## 3. The same records from a file

Change `main` so that it reads from the file `shipments.txt`. Don't change the type `Shipment` or the function `read_shipment_values`. The whole program after the changes:

<!-- example: shipments_file -->
```cpp
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

struct Shipment {
    std::string destination;
    int boxes;
};

bool read_shipment_values(std::istream& input, const std::string& destination, Shipment& result) {
    int boxes{0};
    input >> boxes;

    if (input.fail()) {
        return false;
    }

    if (boxes < 0) {
        return false;
    }

    result = Shipment{destination, boxes};
    return true;
}

int main() {
    std::ifstream input{"shipments.txt"};

    if (input.fail()) {
        std::cout << "Cannot open shipments.txt\n";
        return 0;
    }

    std::vector<Shipment> shipments{};
    std::string destination{};
    std::getline(input, destination);

    while (!input.fail() && !destination.empty()) {
        Shipment shipment{"", 0};
        const bool accepted{read_shipment_values(input, destination, shipment)};

        if (!accepted) {
            if (input.fail()) {
                std::cout << "Input error\n";
            } else {
                std::cout << "Invalid shipments\n";
            }

            return 0;
        }

        shipments.push_back(shipment);

        std::string rest{};
        std::getline(input, rest);

        if (!input.fail()) {
            std::getline(input, destination);
        }
    }

    int total_boxes{0};
    std::cout << "Shipments: " << shipments.size() << "\n";

    for (const Shipment& shipment : shipments) {
        std::cout << shipment.destination << ": " << shipment.boxes << "\n";
        total_boxes += shipment.boxes;
    }

    std::cout << "Total boxes: " << total_boxes << "\n";
}
```

What changed compared with the keyboard version:

| The keyboard version | The file version |
|---|---|
| nothing | `#include <fstream>` |
| nothing | `std::ifstream input{"shipments.txt"};` and right after it a check of `input.fail()` with the message `Cannot open shipments.txt` |
| `std::getline(std::cin, destination);` (twice) | `std::getline(input, destination);` |
| `std::cin.fail()` (three times) | `input.fail()` |
| `read_shipment_values(std::cin, destination, shipment)` | `read_shipment_values(input, destination, shipment)` |
| `std::getline(std::cin, rest);` | `std::getline(input, rest);` |

- **The type and the function are the same, character for character.** Only the argument of the call changed: instead of `std::cin`, the function gets `input`.
- **In `main` no `std::cin` is left.** Every read and every check of `fail()` is about the same stream, `input`. If even one `std::getline` stayed with `std::cin`, the program would read part of the data from the file and part from the keyboard (section 9).
- **The same name `input` in `main` and in the function is a coincidence.** The parameter would be another name for the passed stream even if the variable in `main` were called, for example, `shipments_file`. What counts is what you pass in the call.

| Element | Standard input | File |
|---|---|---|
| data source | `std::cin` | an open `std::ifstream` |
| who prepares the stream | it's ready from the program's start | `main` opens the file and checks the opening |
| the function's parameter type | `std::istream&` | `std::istream&` |
| the algorithm reading a record | the same | the same |
| the function filling the record | the same | the same |
| the report | the same | the same |

**The data file.** In the folder `lesson_12_2`, next to `main.cpp` and `CMakeLists.txt`, create a file `shipments.txt`, as you created `steps.txt` in lesson 12.1, section 3. Type into it the same data as in section 2, but without the empty line at the end:

<!-- run: shipments_file -->

<!-- datafile: shipments_file shipments.txt -->
```text
North Hub
4
South Depot
7
```

Then:

1. Check the **Working directory** field of the `first_program` configuration, as in lesson 12.1, section 4. It must point at the folder `lesson_12_2`, the one with `shipments.txt`.
2. Build and run the program. Don't type anything in the **Run** window: the program doesn't wait for the keyboard.

<!-- output: shipments_file -->
```text
Shipments: 2
North Hub: 4
South Depot: 7
Total boxes: 11
```

This is the second required run. The report is exactly the same as from the keyboard.

**The same data, the same result.** From the keyboard the data were ended by an empty line, and in the file they're ended by the end of the file. According to lesson 10.4 both situations mean the ending of the data, so the report is the same. How do you check that the function works by the same agreement for both sources? Give both versions of the program the same data and compare their standard output. The course's automatic tests do it for several data sets (section 6).

## 4. Who is responsible for what

| The calling code (`main`) | The function `read_shipment_values` |
|---|---|
| chooses the data source: `std::cin` or a file | gets an existing stream |
| opens the file, if the data are in a file, and checks the opening | doesn't know the file name and opens nothing |
| reads the name and decides whether the data have ended | reads the number and checks that it's allowed |
| calls the function and, after a refusal, chooses the message | fills the record only on success, and leaves it unchanged on a refusal |
| builds the vector with `push_back` | reports its result through `bool` |
| prints the report or a message | prints nothing |

- **Why doesn't the function open the file?** If its body had `std::ifstream input{"shipments.txt"};`, it could read only from that one file, and every call would open it again and start from the first line. A function that is given a stream reads from any source, always from where the caller stopped.
- **Why doesn't the function print anything?** If it printed `Input error` itself, every program using it would have to accept that message. The function only says whether it succeeded, and `main`, which knows the whole situation, decides what to print.
- **No copies of the function.** You don't need separate `read_shipment_from_file` and `read_shipment_from_keyboard`. Two copies of the same algorithm would have to be fixed in two places, and differences between them are easy to miss.
- **One source file is enough.** The function could move to its own pair of `.hpp` and `.cpp` files, like the parts of the program in lesson 11.4, and it would work the same. That it accepts different streams comes from the parameter's type, not from the file it's in.

## 5. This lesson's data contract

> **This lesson's data contract.** The program uses the format of lesson 10.4. In valid data:
>
> - each shipment takes two lines: the destination's name and the number of boxes;
> - the name isn't empty, may contain spaces and may repeat, and the number of boxes isn't negative;
> - there are at most 5 shipments;
> - the data are ended by the end of the file or by an empty line where the next name would be;
> - there are no empty lines between shipments;
> - the program doesn't check text after the number on its line.
>
> The program works correctly **for data defined this way**. It doesn't check every error that can happen in a text file.

| Situation | Standard output |
|---|---|
| the file couldn't be opened | `Cannot open shipments.txt` |
| after a non-empty name the number couldn't be read, also when the file ends right after the name | `Input error` |
| the number has been read, but it's negative | `Invalid shipments` |
| the data have ended | `Shipments: N`, the shipments in the order of the file, and `Total boxes: T` |

The error messages are the same as in lesson 10.4; only `Cannot open shipments.txt` is new. After a message there's no partial report, and the program ends with exit code 0.

**Predict** the result of each case before you open the collapsed block. Running them is optional: you only change the contents or the name of `shipments.txt`, with no rebuilding.

**B: an empty file.** `shipments.txt` exists, but has not a single character in it.

<!-- run: shipments_file -->

<!-- datafile: shipments_file shipments.txt -->
```text
```

<details>
<summary>Standard output for B</summary>

<!-- output: shipments_file -->
```text
Shipments: 0
Total boxes: 0
```

Opening works. The first read of a name meets the end of the file, so the loop doesn't run even once. That's a correct ending of the data: a list without shipments. In lesson 12.1 an empty file gave `Input error`, because the contract required a number of days. Here the contract requires no record at all. **What an empty file means is decided by the contract.**

</details>

**C: an empty line at the end.** One shipment is followed by an empty line.

<!-- run: shipments_file -->

<!-- datafile: shipments_file shipments.txt -->
```text
North Hub
4

```

<details>
<summary>Standard output for C</summary>

<!-- output: shipments_file -->
```text
Shipments: 1
North Hub: 4
Total boxes: 4
```

An empty line where the next name would be ends the data, just like an empty line typed in the **Run** window.

</details>

**D: a missing file.** There's no `shipments.txt` in the working directory.

<!-- run: shipments_file -->

<details>
<summary>Standard output for D</summary>

<!-- output: shipments_file -->
```text
Cannot open shipments.txt
```

Opening fails, so the program reads nothing. It doesn't print `Shipments: 0`, because it doesn't know what's in a file it didn't get.

</details>

**E: a number of boxes not allowed** in the second shipment.

<!-- run: shipments_file -->

<!-- datafile: shipments_file shipments.txt -->
```text
North Hub
4
South Depot
-2
```

<details>
<summary>Standard output for E</summary>

<!-- output: shipments_file -->
```text
Invalid shipments
```

`-2` is read correctly, but it's negative. The function returns `false`, and `input.fail()` gives `false`, so `main` chooses `Invalid shipments`. The first shipment is already in the vector, but there's no report.

</details>

**F: a word instead of a number** in the second shipment.

<!-- run: shipments_file -->

<!-- datafile: shipments_file shipments.txt -->
```text
North Hub
4
South Depot
seven
```

<details>
<summary>Standard output for F</summary>

<!-- output: shipments_file -->
```text
Input error
```

Reading `seven` with `>>` fails, so after the function's `false`, `input.fail()` gives `true`.

</details>

**G: no number after a name.** The file ends right after the name of the second shipment.

<!-- run: shipments_file -->

<!-- datafile: shipments_file shipments.txt -->
```text
North Hub
4
South Depot
```

<details>
<summary>Standard output for G</summary>

<!-- output: shipments_file -->
```text
Input error
```

A non-empty name starts a record, so the end of the file right after it is an incomplete record, not the ending of the data (lesson 10.4, section 4). The last name doesn't get into the report as a shipment.

</details>

**H: the last number with no line end.** The data of section 3, but after `7` there's no line end any more.

<!-- run: shipments_file -->

<!-- datafile: shipments_file shipments.txt noeol -->
```text
North Hub
4
South Depot
7
```

<details>
<summary>Standard output for H</summary>

<!-- output: shipments_file -->
```text
Shipments: 2
North Hub: 4
South Depot: 7
Total boxes: 11
```

`>>` reads 7 and reaches the end of the file, and the function returns `true`. Only `std::getline(input, rest)` fails, so `main` doesn't read the next name, and the loop ends on `fail()` in its condition. In lesson 10.4 this case was only in a table, because the automatic tests couldn't give it from the keyboard. A file without a line end after its last line is easy to make, for example when you don't press **Enter** after the last number. You don't have to prepare such a file.

</details>

Where the data can end, and what the program prints then:

| Where the data end | Case | Result |
|---|---|---|
| before the first name: an empty file | B | a report without shipments |
| at an empty line where a name would be | C | the report |
| right after a name, before its number | G | `Input error` |
| right after the last number, with no line end | H | the report |
| after the line end of the last number | A | the report |

## 6. The contract's limit: an empty line in the middle

**I: an empty line between shipments.** Someone wrote two shipments in the file, but left an empty line between them:

<!-- run: shipments_file -->

<!-- datafile: shipments_file shipments.txt -->
```text
North Hub
4

South Depot
7
```

**Predict** how many shipments the report will show.

<details>
<summary>Standard output for I</summary>

<!-- output: shipments_file -->
```text
Shipments: 1
North Hub: 4
Total boxes: 4
```

</details>

The program stops reading at the empty line, because the contract says so: an empty line where a name would be ends the data. `South Depot` and `7` stay unread in the file, and the report says nothing about them. **This is not a reading of both shipments.** The program has no bug here: it works correctly for data that follow the contract, and this file breaks the contract, because no empty line may be left between shipments. If the file was meant to hold two shipments, though, the report is incomplete, and nothing signals it.

**Why is this a bigger problem in a file than at the keyboard?** When typing in the **Run** window, an empty line is a deliberate decision: you press **Enter** because the list has ended. In a file nobody types a separate "end" line, because the file ends by itself. An empty line in the middle of a file easily appears by accident, for example when adding or copying data, and the program silently skips everything after it.

**A question for later.** What should the program do if an empty line appears between two shipments, and we want to read all the records, or at least learn that something is wrong with the file? Write down your answer. You'll come back to this question in the next lesson of Module 12.

<details>
<summary>The other control cases: open after your predictions</summary>

All these cases are checked automatically. Their results follow from the contract of section 5.

**J: one shipment.**

<!-- run: shipments_file -->

<!-- datafile: shipments_file shipments.txt -->
```text
East Gate
3
```

<!-- output: shipments_file -->
```text
Shipments: 1
East Gate: 3
Total boxes: 3
```

**K: five shipments,** the largest number in the contract, including a shipment with zero boxes.

<!-- run: shipments_file -->

<!-- datafile: shipments_file shipments.txt -->
```text
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

<!-- output: shipments_file -->
```text
Shipments: 5
Central Hub: 2
North Hub: 4
River Port: 0
South Depot: 7
West End Depot: 1
Total boxes: 14
```

**L: the same name twice.** Each occurrence is a separate shipment.

<!-- run: shipments_file -->

<!-- datafile: shipments_file shipments.txt -->
```text
North Hub
4
North Hub
0
```

<!-- output: shipments_file -->
```text
Shipments: 2
North Hub: 4
North Hub: 0
Total boxes: 4
```

**M: a word instead of the number in the first shipment.**

<!-- run: shipments_file -->

<!-- datafile: shipments_file shipments.txt -->
```text
North Hub
four
```

<!-- output: shipments_file -->
```text
Input error
```

**N: an empty line at the very start.** The file has one line, and it's empty, so the data end before the first shipment starts. The report is the same as for an empty file.

<!-- run: shipments_file -->

<!-- datafile: shipments_file shipments.txt -->
```text

```

<!-- output: shipments_file -->
```text
Shipments: 0
Total boxes: 0
```

</details>

<details>
<summary>The same data in the keyboard version: open after your predictions</summary>

The version of section 2 is the program of lesson 10.4. That lesson's automatic tests check it from the keyboard for exactly the same characters as the cases A, E, F, G, I, J, K and N of this lesson, with the same results. It must be so, because the function and the loop are the same in both versions. Here we also check the data A without the empty line at the end, that is, exactly the characters that the version of section 3 finds in the file:

<!-- input: shipments_keyboard -->
```text
North Hub
4
South Depot
7
```

<!-- output: shipments_keyboard -->
```text
Shipments: 2
North Hub: 4
South Depot: 7
Total boxes: 11
```

Only the missing file (D) has no keyboard counterpart: with `std::cin` there's nothing to open.

</details>

## 7. Diagnostic: a stream passed by value

**The situation.** Someone decided that the `&` in the header of `read_shipment_values` is unnecessary, because "the function only reads anyway". They removed it and wrote the parameter as `std::istream input`. Check what the compiler says.

1. In `main.cpp` of the project `lesson_12_2`, change `std::istream& input` in the function's header to `std::istream input`. Don't change anything else.
2. **Predict:** will the program build? If not, will it be a compile error or a link error? Which line will the compiler point to?
3. Build the project (**Build | Build Project**). This is the third required run: this time you run the build, not the program.
4. In the **Build** window, find the first error: the file, the line and the message.
5. Work out which line contains the error and which line causes it.
6. Restore the `&`, that is, `std::istream& input`. Build and run the program. This is the fourth required run: the program prints the report of section 3 again.

<details>
<summary>The program with the bug: as it is after step 1</summary>

<!-- broken: shipments_by_value at=41:50 errors=1 error=^call to deleted constructor of 'std::istream' -->
```cpp
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

struct Shipment {
    std::string destination;
    int boxes;
};

bool read_shipment_values(std::istream input, const std::string& destination, Shipment& result) {
    int boxes{0};
    input >> boxes;

    if (input.fail()) {
        return false;
    }

    if (boxes < 0) {
        return false;
    }

    result = Shipment{destination, boxes};
    return true;
}

int main() {
    std::ifstream input{"shipments.txt"};

    if (input.fail()) {
        std::cout << "Cannot open shipments.txt\n";
        return 0;
    }

    std::vector<Shipment> shipments{};
    std::string destination{};
    std::getline(input, destination);

    while (!input.fail() && !destination.empty()) {
        Shipment shipment{"", 0};
        const bool accepted{read_shipment_values(input, destination, shipment)};

        if (!accepted) {
            if (input.fail()) {
                std::cout << "Input error\n";
            } else {
                std::cout << "Invalid shipments\n";
            }

            return 0;
        }

        shipments.push_back(shipment);

        std::string rest{};
        std::getline(input, rest);

        if (!input.fail()) {
            std::getline(input, destination);
        }
    }

    int total_boxes{0};
    std::cout << "Shipments: " << shipments.size() << "\n";

    for (const Shipment& shipment : shipments) {
        std::cout << shipment.destination << ": " << shipment.boxes << "\n";
        total_boxes += shipment.boxes;
    }

    std::cout << "Total boxes: " << total_boxes << "\n";
}
```

</details>

<details>
<summary>What happens and how to fix it: open after step 5</summary>

1. **It's a compile error.** Compiling `main.cpp` fails, so linking never happens. In the build output it looks roughly like this (paths shortened, notes from inside the standard library left out):

   ```text
   main.cpp:41:50: error: call to deleted constructor of 'std::istream' (aka 'basic_istream<char>')
   main.cpp:11:40: note: passing argument to parameter 'input' here
   ```

   On Windows, Ubuntu and macOS the paths and the note from inside the library look different. The error points to the same place and starts the same way; on Windows only the part in brackets differs: `(aka 'basic_istream<char, char_traits<char>>')`.
2. **The error points to the call, and its cause is in the header.** Line 41 is the call `read_shipment_values(input, destination, shipment)` in `main`, and column 50 is the argument `input`. The `note:` points to the parameter `input` on line 11: that's where the `&` is missing.
3. **What the message says.** A parameter without `&` is a new object, created in the call as a copy of the argument (lesson 9.1). A *constructor* is the operation in C++ that creates a new object of a type, and *deleted* means that the standard library has deliberately forbidden it. So the message says: to call this function, a new `std::istream` would have to be created as a copy of `input`, and an input stream may not be copied.
4. **Why a stream isn't copied.** A stream isn't an ordinary value like a number: it's tied to one data source and remembers how far it has read. The function must read from the same stream as `main`, from where `main` stopped, and leave it where it stopped itself. That needs a reference.
5. **The fix:** restore the `&`. The program builds and prints the same report as in section 3. Adding `const` isn't a fix: reading changes the stream, so with a `const std::istream&` parameter the compiler rejects `input >> boxes` (section 9).
6. **It's the same with `std::cin`.** In the keyboard version, with the parameter without `&`, the compiler reports the same error at the argument `std::cin`: no input stream may be copied.

</details>

## 8. Mission: school library loans

A school library records in a file how many copies of each title are on loan. The program reads the file `loans.txt` and prints all the entries and the total number of copies on loan.

**The contract of `loans.txt`:**

- each entry takes two lines: the book's title, and on the next line the number of copies of that title on loan;
- the title may contain spaces and isn't empty, because an empty line ends the data;
- the same title may appear several times, and each occurrence is a separate entry;
- the number of copies is a whole number from 0 to 12;
- there are at most 5 entries, so the total is at most 5 · 12 = 60;
- the data are ended by the end of the file or by an empty line where the next title would be, and there are no empty lines between entries;
- the program doesn't check text after the number on its line.

**The messages:**

| Situation | Standard output |
|---|---|
| the file couldn't be opened | `Cannot open loans.txt` |
| after a non-empty title the number couldn't be read | `Input error` |
| the number has been read, but it's outside the range from 0 to 12 | `Invalid loans` |
| the data have ended | `Loans: N`, each entry in the order of the file, for example `Science Atlas: 2`, and `Total copies: T` |

The program doesn't sort the entries and doesn't remove repeats. It prints the report only after processing all the entries, and after an error only one message, with no partial report. It asks no questions and ends with exit code 0.

**Requirements:**

- The program defines its own entry type with two fields: the title (`std::string`) and the number of copies (`int`), and collects the entries in an initially empty vector.
- A separate function reads and checks the number of one entry. It gets the stream through `std::istream&`, the title through `const std::string&` and an existing result record through a reference without `const`. It reads the number into a local variable, and assigns the record only after checking the read and the range. It returns `true` or `false`, and on `false` the result record stays unchanged. It prints nothing, opens no file and doesn't use `std::cin`.
- `main` opens `loans.txt` and checks the opening, reads the titles, recognises the ending of the data, calls the function, adds a record with `push_back` only after `true`, and after a refusal tells `Input error` from `Invalid loans`.

In `cpp-workspace`, create a folder `library_loans`, copy `CMakeLists.txt` from the original `lesson_05_first_program` into it, and create an empty `main.cpp` and a file `loans.txt`. Leave `CMakeLists.txt` unchanged, and don't add `loans.txt` to `add_executable`: the file is read by the running program, the compiler doesn't read it. Open the folder in CLion and check **Working directory**, as in lesson 12.1, section 4. One `main.cpp` file is enough. Write the program on your own.

```text
library_loans/
├── CMakeLists.txt
├── loans.txt
└── main.cpp
```

You have to decide on your own:

1. what to call the type, its fields, the vector, the function, its parameters and the file stream variable;
2. in what order the function reads the number and checks the read and the range, and where it assigns the result record;
3. where `main` opens the file and checks the opening;
4. where `main` reads the next titles, and how it recognises the ending of the data;
5. when to finish the number line;
6. how to tell `Input error` from `Invalid loans` after a refusal;
7. how to prevent a partial report;
8. how to compute the total from the vector's elements;
9. what data would reveal that the function changes the result record before checking the range.

**Cases A–J.** Each case is different contents of `loans.txt`, or no file.

**A: two entries.**

<!-- run: loans -->

<!-- datafile: loans loans.txt -->
```text
Science Atlas
2
History Notes
3
```

<!-- output: loans -->
```text
Loans: 2
Science Atlas: 2
History Notes: 3
Total copies: 5
```

**B: an empty file.**

<!-- run: loans -->

<!-- datafile: loans loans.txt -->
```text
```

<!-- output: loans -->
```text
Loans: 0
Total copies: 0
```

**C: a missing file.** There's no `loans.txt` in the working directory.

<!-- run: loans -->

<!-- output: loans -->
```text
Cannot open loans.txt
```

**D: a word instead of the number** in the second entry.

<!-- run: loans -->

<!-- datafile: loans loans.txt -->
```text
Science Atlas
2
History Notes
seven
```

<!-- output: loans -->
```text
Input error
```

**E: a number not allowed** in the second entry.

<!-- run: loans -->

<!-- datafile: loans loans.txt -->
```text
Science Atlas
2
History Notes
-1
```

<!-- output: loans -->
```text
Invalid loans
```

**F: an interrupted entry.** The file ends right after the second title.

<!-- run: loans -->

<!-- datafile: loans loans.txt -->
```text
Science Atlas
2
History Notes
```

<!-- output: loans -->
```text
Input error
```

**G: an empty line ends the data.**

<!-- run: loans -->

<!-- datafile: loans loans.txt -->
```text
Science Atlas
2

```

<!-- output: loans -->
```text
Loans: 1
Science Atlas: 2
Total copies: 2
```

**H: an empty line before the next entry.** The contract's limit, as in section 6: the second entry doesn't get into the report.

<!-- run: loans -->

<!-- datafile: loans loans.txt -->
```text
Science Atlas
2

History Notes
3
```

<!-- output: loans -->
```text
Loans: 1
Science Atlas: 2
Total copies: 2
```

**I: the data A with no line end after the last number.**

<!-- run: loans -->

<!-- datafile: loans loans.txt noeol -->
```text
Science Atlas
2
History Notes
3
```

<!-- output: loans -->
```text
Loans: 2
Science Atlas: 2
History Notes: 3
Total copies: 5
```

**J: the same title twice.**

<!-- run: loans -->

<!-- datafile: loans loans.txt -->
```text
Science Atlas
2
Science Atlas
4
```

<!-- output: loans -->
```text
Loans: 2
Science Atlas: 2
Science Atlas: 4
Total copies: 6
```

**Before you write the program**, prepare a table: the cases A–J and at least two of your own, for example with the limits of the range, with the expected result worked out from the contract.

**Then run the program for A.** This is the fifth required run. Trace the other cases on paper, line by line through your program, and compare them with the results given above. If you have time, also run B or H: you only change the contents of `loans.txt`, not the code. All the cases are checked automatically in the reference solution.

### Success criteria

- The program builds as C++20 and prints exactly the result shown for A.
- Your predictions for B–J agree with the results given above.
- The function gets the stream through `std::istream&`, the title through `const std::string&` and the result record through a reference, and assigns the record only after checking the read and the range.
- The function has no `std::cin`, no `std::cout` and doesn't open a file.
- `main` checks the opening before reading anything, adds a record only after `true`, and on an error prints no part of the report.
- `loans.txt` isn't in `add_executable`, `CMakeLists.txt` is the same as in lesson 0.5, and **Working directory** points at the folder with `loans.txt`.
- You can explain why for H the report has only one entry, and why that's a limit of the contract, not a bug of the program.

When the result matches, you can save the project in Git, as in lesson 1.5: `main.cpp`, `CMakeLists.txt` and `loans.txt` with the data A, without the build folder.

<details>
<summary>Hint 1: the shared parameter</summary>

The function of section 1 doesn't know where the data come from, and that's why it fits any source. What parameter type lets your function read from an open file, and, if needed, from `std::cin` too? Who in your program should know the name `loans.txt`?

</details>

<details>
<summary>Hint 2: the record and the refusal</summary>

First read the number into a local variable and check `fail()`, then the range from 0 to 12. Assign the result record only at the end, with one assignment of the whole record, like `result = Shipment{destination, boxes};` in lesson 10.4. Each refusal is a `return false;` before that assignment.

</details>

<details>
<summary>Hint 3: the end of the data and the file</summary>

Tell four situations apart: a file that couldn't be opened (check right after creating the stream); the end of the file or an empty line where a title would be (the ending of the data, the report); the end of the file after a non-empty title (`Input error`); a valid entry (`push_back`, finishing the number line, and the next title). Reading the title and the loop's condition are the same as in `main` of section 3.

</details>

An example solution is in [Example solutions](#example-solutions).

## 9. When something goes differently

| What you see | What it means | What to do |
|---|---|---|
| The program prints nothing and waits | In `main` a `std::cin` is left, for example in `std::getline(std::cin, destination)`, so the program waits for the keyboard. | Replace every `std::cin` in `main` with the file stream variable. |
| The compiler reports `call to deleted constructor of 'std::istream'` | The stream parameter has no `&`, so the call tries to copy the stream (section 7). | Write the parameter as `std::istream&`. |
| At `>>` the compiler reports `invalid operands to binary expression`, and the message contains `const std::istream` | The stream parameter has `const`, and reading changes the stream. | Remove `const` from the stream parameter. |
| `Cannot open shipments.txt`, although the file exists | The file isn't in the working directory, or has another name. | Follow the steps of lesson 12.1, section 7: the name, the case of letters, **Working directory**, where the file is. |
| The report has fewer shipments than the file, and there's no message | There's an empty line in the middle of the file, which ends the data (section 6). | Remove the empty line: the file breaks this lesson's contract. |
| `Input error`, although the data look correct | Where a number should be, there's a letter, for example `O` instead of `0`, or the line with the number after the last name is missing. | Check the file line by line: every name must be followed by a line with a number. |

## 10. Explain

Answer in your own words, preferably in writing. Only then compare with the example answers.

1. Why does `read_shipment_values` take `std::istream&` instead of reading directly from `std::cin`?
2. What changes in the program when you move from the keyboard to a file, and what stays unchanged? How do you check that both versions work by the same agreement?
3. Why can an open `std::ifstream` be passed to a function that expects `std::istream&`? Are `std::cin` and the file stream the same object?
4. What happens when the stream parameter has no `&`? Where does the compiler point to the error, and where is its cause?
5. Why doesn't the stream parameter have `const`?
6. Why does `main` open the file, and not the reading function? What would happen if the function opened `shipments.txt` on every call?
7. The function returned `false`, although reading the number from the file succeeded. When does that happen, what's in the result record then, and who chooses the message?
8. One file ends right after the name of the second shipment, and another right after its number, with no line end. Why are the results different?
9. What does the program print when there's an empty line between two shipments in the file? Is that a bug of the program?
10. Why isn't the program of this lesson a general reader of text files yet? Give two things it doesn't check.

<details>
<summary>Example answers</summary>

1. Because then the function doesn't depend on the data source. It reads from whatever stream it's given: from `std::cin` or from an open file. A function tied to `std::cin` would need a second copy to read from a file.
2. Only `main` changes: `#include <fstream>` and opening the file with its check are added, and the file stream variable replaces every `std::cin`. The type, the function, the loop and the report stay the same. I check it by giving both versions the same data and comparing their standard output.
3. Because `std::ifstream` is a kind of input stream: it has `>>`, `fail()` and works with `std::getline`, so it has everything the function needs from `std::istream`. It isn't the same object: `std::cin` reads from the keyboard, and the file stream from a file. Only the way they're used is shared.
4. A parameter without `&` is a copy of the argument, and an input stream may not be copied. The compiler reports `call to deleted constructor of 'std::istream'` at the function call in `main`, at the argument. The cause is in the function's header, where the `&` is missing; the `note:` points to it.
5. Because reading changes the stream: it takes characters from it and may change its state. With `const` the compiler wouldn't allow `input >> boxes`.
6. Because `main` knows where the data should come from, and it must also check whether the file opened. A function opening `shipments.txt` on every call would always read from the file's first line, and wouldn't work with `std::cin` or with another file.
7. When the number has been read but isn't allowed, for example `-2` boxes or `13` copies. The result record is then the same as before the call, because the function assigns it only after all the checks. `main` chooses the message: after `false` it checks the stream's `fail()` and prints `Input error` or `Invalid ...`.
8. In the first file a record has started, but its number is missing, so the read in the function fails: `Input error`. In the second, the number is complete: `>>` reads it, and only finishing the line fails, which just means there's no next name. The program prints the report.
9. A report with only the shipments before the empty line, and no message. That's not a bug of the program, but a limit of its contract: an empty line where a name would be ends the data, and no empty line may be left between shipments. If the file was meant to hold more shipments, though, the report is incomplete.
10. Because it works correctly only for data that follow this lesson's contract. It doesn't tell an empty line in the middle of a file from the ending of the data, doesn't check text after the number on its line, and on an error doesn't say where in the file it is.

</details>

## Summary

- A function with a `std::istream&` parameter reads from any input stream: from `std::cin` and from an open `std::ifstream`. To move from the keyboard to a file, you change only the calling code.
- `main` chooses the source, opens the file and checks the opening, reads the names, recognises the ending of the data, builds the vector and prints the result. The function reads and checks the values of one record, opens nothing and prints nothing.
- You pass a stream by a reference without `const`. A stream may not be copied (`call to deleted constructor of 'std::istream'`), and reading changes it.
- The same data give the same result from the keyboard and from a file. In a file the data are usually ended by the end of the file, also when there's no line end after the last number.
- The contract defines for which data the program works correctly. It also decides what an empty file means: here, a list without shipments.
- An empty line in the middle of a file silently ends the reading. That's a limit of the contract taken over from the keyboard, not a reading of all the records.

## What's next

The program of this lesson trusts the file's format: an empty line ends the reading, and on an error you don't know where in the file it is. The next lesson of Module 12 will deal with recognising more precisely where the data in a file end and where the error is. It's in preparation.

---

## Example solutions

Look here **after your own attempt**. Your names may differ, as long as the standard output is as required.

<details>
<summary>Section 8: mission, school library loans</summary>

**`main.cpp`**:

<!-- example: loans -->
```cpp
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

struct Loan {
    std::string title;
    int copies;
};

bool read_loan_values(std::istream& input, const std::string& title, Loan& result) {
    int copies{0};
    input >> copies;

    if (input.fail()) {
        return false;
    }

    if (copies < 0 || copies > 12) {
        return false;
    }

    result = Loan{title, copies};
    return true;
}

int main() {
    std::ifstream loans_file{"loans.txt"};

    if (loans_file.fail()) {
        std::cout << "Cannot open loans.txt\n";
        return 0;
    }

    std::vector<Loan> loans{};
    std::string title{};
    std::getline(loans_file, title);

    while (!loans_file.fail() && !title.empty()) {
        Loan loan{"", 0};
        const bool accepted{read_loan_values(loans_file, title, loan)};

        if (!accepted) {
            if (loans_file.fail()) {
                std::cout << "Input error\n";
            } else {
                std::cout << "Invalid loans\n";
            }

            return 0;
        }

        loans.push_back(loan);

        std::string rest{};
        std::getline(loans_file, rest);

        if (!loans_file.fail()) {
            std::getline(loans_file, title);
        }
    }

    int total_copies{0};
    std::cout << "Loans: " << loans.size() << "\n";

    for (const Loan& loan : loans) {
        std::cout << loan.title << ": " << loan.copies << "\n";
        total_copies += loan.copies;
    }

    std::cout << "Total copies: " << total_copies << "\n";
}
```

**`CMakeLists.txt`**: the same as in the original `lesson_05_first_program`, unchanged. `loans.txt` isn't in `add_executable`.

**`loans.txt`** with the data A, in the folder `library_loans`, next to `main.cpp` and `CMakeLists.txt`:

<!-- run: loans -->

<!-- datafile: loans loans.txt -->
```text
Science Atlas
2
History Notes
3
```

<!-- output: loans -->
```text
Loans: 2
Science Atlas: 2
History Notes: 3
Total copies: 5
```

- **Running it:** the **Working directory** field of the `first_program` configuration points at the folder `library_loans`, the one with `loans.txt`. In the terminal you run the program from the folder `library_loans`.
- **The reading function:** `read_loan_values` gets the stream through `std::istream&`, as after the fix of section 7, the title through `const std::string&` and the record through `Loan&`. It reads the number into the local variable `copies`, checks `fail()`, then the range from 0 to 12, and only then assigns the whole record. It prints nothing and doesn't know that it reads from a file.
- **`main`:** opens `loans.txt` and checks the opening, and then does the same as `main` of section 3: reads the titles, ends the loop at the end of the file or an empty line, after a refusal chooses the message with `loans_file.fail()`, finishes the number line and only then reads the next title.
- **The stream variable** is called `loans_file` here, and the function's parameter `input`. The names may differ, because the parameter is another name for the passed stream anyway.
- **Other correct solutions:** the range written as `const int` constants, the range condition split into two `if`s, a `bool` flag instead of `return 0;` in the loop, as in lesson 7.4.

| Case | The file `loans.txt` | Standard output |
|---|---|---|
| A | `Science Atlas`, `2`, `History Notes`, `3` | 2 entries, `Total copies: 5` |
| B | an empty file | `Loans: 0`, `Total copies: 0` |
| C | a missing file | `Cannot open loans.txt` |
| D | `Science Atlas`, `2`, `History Notes`, `seven` | `Input error` |
| E | `Science Atlas`, `2`, `History Notes`, `-1` | `Invalid loans` |
| F | `Science Atlas`, `2`, `History Notes` | `Input error` |
| G | `Science Atlas`, `2`, an empty line | 1 entry, `Total copies: 2` |
| H | `Science Atlas`, `2`, an empty line, `History Notes`, `3` | 1 entry, `Total copies: 2` |
| I | the data A with no line end after `3` | 2 entries, `Total copies: 5` |
| J | `Science Atlas`, `2`, `Science Atlas`, `4` | 2 entries, `Total copies: 6` |

The other control cases, checked automatically:

**K: one entry.**

<!-- run: loans -->

<!-- datafile: loans loans.txt -->
```text
Poetry for Kids
1
```

<!-- output: loans -->
```text
Loans: 1
Poetry for Kids: 1
Total copies: 1
```

**L: both limits of the range,** 0 and 12.

<!-- run: loans -->

<!-- datafile: loans loans.txt -->
```text
Science Atlas
0
History Notes
12
```

<!-- output: loans -->
```text
Loans: 2
Science Atlas: 0
History Notes: 12
Total copies: 12
```

**M: 13 copies,** one too many.

<!-- run: loans -->

<!-- datafile: loans loans.txt -->
```text
Science Atlas
2
History Notes
13
```

<!-- output: loans -->
```text
Invalid loans
```

**N: the largest possible total,** five entries of 12 copies.

<!-- run: loans -->

<!-- datafile: loans loans.txt -->
```text
Science Atlas
12
History Notes
12
Poetry for Kids
12
Space Facts
12
Animal Stories
12
```

<!-- output: loans -->
```text
Loans: 5
Science Atlas: 12
History Notes: 12
Poetry for Kids: 12
Space Facts: 12
Animal Stories: 12
Total copies: 60
```

**O: a word instead of the number in the first entry.**

<!-- run: loans -->

<!-- datafile: loans loans.txt -->
```text
Science Atlas
two
```

<!-- output: loans -->
```text
Input error
```

**P: only a title, with no line end.** The file ends right after the first title.

<!-- run: loans -->

<!-- datafile: loans loans.txt noeol -->
```text
Science Atlas
```

<!-- output: loans -->
```text
Input error
```

**The control program** checks the function's agreement on a refusal, which the report doesn't show, because after `false` the program ends. The type and the function are the same as above, but `main` reads from `std::cin`: the same function works unchanged with the keyboard. `main` prepares the record `Old Title` with the number 1, reads one title, calls the function and prints its result and the state of the record. Running it is optional. You can replace the type and the function with your own, if you also change the names in `main`.

<!-- example: loan_values_check -->
```cpp
#include <iostream>
#include <string>

struct Loan {
    std::string title;
    int copies;
};

bool read_loan_values(std::istream& input, const std::string& title, Loan& result) {
    int copies{0};
    input >> copies;

    if (input.fail()) {
        return false;
    }

    if (copies < 0 || copies > 12) {
        return false;
    }

    result = Loan{title, copies};
    return true;
}

int main() {
    Loan result{"Old Title", 1};
    std::string title{};
    std::getline(std::cin, title);

    const bool accepted{read_loan_values(std::cin, title, result)};

    if (accepted) {
        std::cout << "Returned: true\n";
    } else {
        std::cout << "Returned: false\n";
    }

    std::cout << "Result: " << result.title << ", " << result.copies << "\n";
}
```

A valid number changes the record:

<!-- input: loan_values_check -->
```text
History Notes
3
```

<!-- output: loan_values_check -->
```text
Returned: true
Result: History Notes, 3
```

After a refusal the record stays unchanged, also when the number was read but is outside the range:

<!-- input: loan_values_check -->
```text
History Notes
seven
```

<!-- output: loan_values_check -->
```text
Returned: false
Result: Old Title, 1
```

<!-- input: loan_values_check -->
```text
History Notes
13
```

<!-- output: loan_values_check -->
```text
Returned: false
Result: Old Title, 1
```

<!-- input: loan_values_check -->
```text
History Notes
```

<!-- output: loan_values_check -->
```text
Returned: false
Result: Old Title, 1
```

</details>

**Previous lesson:** [Lesson 12.1: Your first data file](lesson_01_first_data_file.en.md) · **Next lesson:** in preparation · [Course overview](../../README.en.md)

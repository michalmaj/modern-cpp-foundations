# Lesson 10.3: Building a vector of records from input

[Polski](lesson_03_building_a_vector_of_records.md) · **English** · [Course overview](../../README.en.md)

> **Module 10, lesson 3** · about 80–100 minutes, can be split into two sessions
> **You need:** your `cpp-workspace` folder and the original `lesson_05_first_program` project, as before. You won't need the debugger in this lesson.
> **Pilot version.** The programs in this lesson are checked automatically on Windows, Ubuntu and macOS, including with the given input data. Typing input in CLion's **Run** window is described without a manual check on every system.

## Before you start

This lesson assumes that you:

- add elements to an empty vector with `push_back`, only after a successful read, and know that `size()` grows by 1 with each addition (lesson 6.2);
- go through a vector of records with the loop `for (const Product& product : products)` (lesson 8.4) and change its elements with the loop `for (Product& product : products)` (lesson 9.3);
- know that a copy of a record is independent of it (lesson 8.2);
- know that an executed `return` ends the whole function call, even inside a loop (lessons 5.4 and 9.4), and that `return 0;` ends `main` (lesson 1.3);
- read the fields into local variables, check the read and the rules, and only then create the record (lesson 10.1);
- read a name with `std::getline`, numbers with `>>`, and finish the number line with `std::getline(std::cin, rest)` (lesson 10.2).

## The situation

In lesson 10.2 the program read exactly two shipments, each into its own variables. Five shipments would need five sets of variables, and when the number of shipments comes only with the data, such a program can't be written at all.

Now the first line of the data says how many records follow. The program reads that number, then reads and checks the records one by one in a loop, and adds each accepted one to a vector with `push_back`. You already know all of these pieces. What's new is joining them in one program: reading from input, your own type and a collection.

The main rule of this lesson: **a valid, complete record is created first, and only then does it go into the vector.**

After this lesson you will:

- read the number of records, check its range, and read exactly as many records in a loop as the data announce;
- finish the previous number line at the start of each pass;
- add only complete, checked records with `push_back`;
- stop reading at the first error, with no partial report;
- tell adding a new element from changing an existing one;
- choose data that reveal a record added too early.

## 1. Prepare the project

In `cpp-workspace`, create a folder `lesson_10_3` and copy `main.cpp` and `CMakeLists.txt` from the original `lesson_05_first_program` into it. You type the program of section 2 into `main.cpp` in that folder.

The programs in this lesson print no questions. Type the data line by line, as in lesson 10.2. The program stops by itself after reading the announced number of records.

## 2. A list of shipments

The program reads a list of shipments. The first line gives the number of shipments, from 0 to 5. Then each shipment takes two lines, as in lesson 10.2: the full name of the destination and the number of boxes. The name can't be empty, and the number of boxes must not be negative.

<!-- example: shipment_list -->
```cpp
#include <iostream>
#include <string>
#include <vector>

struct Shipment {
    std::string destination;
    int boxes;
};

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

    int total_boxes{0};
    std::cout << "Shipments: " << shipments.size() << "\n";

    for (const Shipment& shipment : shipments) {
        std::cout << shipment.destination << ": " << shipment.boxes << "\n";
        total_boxes += shipment.boxes;
    }

    std::cout << "Total boxes: " << total_boxes << "\n";
}
```

Run the program and type:

<!-- input: shipment_list -->
```text
2
North Hub
4
South Depot
7
```

<!-- output: shipment_list -->
```text
Shipments: 2
North Hub: 4
South Depot: 7
Total boxes: 11
```

| Code | What it does |
|---|---|
| `std::vector<Shipment> shipments{};` | creates an empty vector of shipments, without `const`, because the program will add to it |
| `std::cin >> count;` | reads the number of shipments |
| `return 0;` | ends `main` at once, after printing the message (section 3) |
| `for (int index{0}; index < count; ++index)` | runs one pass for each announced shipment |
| `std::getline(std::cin, rest);` | finishes the previous number line (section 4) |
| `const Shipment shipment{destination, boxes};` | creates a complete record from data that were read and checked |
| `shipments.push_back(shipment);` | adds that record at the end of the vector |
| `shipments.size()` | gives how many records are really in the vector |

- **Each pass has its own local variables** `rest`, `destination` and `boxes`, with starting values, like the variable `measurement` in lesson 6.2.
- **The report comes from the vector:** the number of shipments comes from `size()`, and the lines and the total from the fields of its elements.

## 3. The number of records first

The program checks the number of shipments like any value it reads: first `std::cin.fail()`, then the rules. `two` gives `Input error`, while `-1` or `6` are values that were read correctly but aren't allowed, so they give `Invalid shipments`. In both cases the program reads no shipment.

Each check that finds an error prints a message and executes `return 0;`. `main` is a function too, and an executed `return` ends its whole call (lesson 5.4), so the remaining lines of `main` don't run. The exit code 0 only says that the program ended normally, and the message says what the result is.

`count` and the loop counter are of type `int`, because the range is small and checked before the loop. Still, `count` is only an **announcement** in the data, while `shipments.size()` is the number of records that really went into the vector. With valid data they are equal, but the report describes the vector, so it uses `size()`.

## 4. The loop and finishing the previous line

Each pass starts by finishing the previous line, and only then reads the name and the number:

<!-- fragment -->
```cpp
for (int index{0}; index < count; ++index) {
    std::string rest{};
    std::getline(std::cin, rest);

    // Check the read.
    // Read the name and the fields of the current record.
    // Check the record, create it and add it.
}
```

Trace the main data:

| Pass | `getline(rest)` finishes | `destination` | `boxes` | `size()` after the pass |
|---|---|---|---|---|
| 1 | the line with the number of shipments `2` | `North Hub` | 4 | 1 |
| 2 | the line with the number of boxes `4` | `South Depot` | 7 | 2 |

- **In the first pass** the previous line is the line with the number of shipments: after `>> count`, its end stayed in the input (lesson 10.2).
- **In each later pass** it's the number line of the previous shipment.
- **After the last shipment** there is no further pass, so the line with `7` stays unfinished, like the last line in lesson 10.2. Valid data that end right after `7`, with no end of line, would be turned into `Input error` by an extra `getline` after the loop. The course's automatic tests don't run this case, because in them every line has its end.

Finishing at the start of the pass therefore covers the line with the number of records and never runs after the last number. `rest` still checks nothing (lesson 10.2).

In the program of section 2, the read by `getline(rest)` is checked by the same `if` as the reads of the name and the number, after all the reads of the pass: when one read fails, the following ones fail too (lesson 4.6).

## 5. A complete record first, then `push_back`

Each pass takes the same steps, in this order:

1. read the fields into local variables;
2. check `std::cin.fail()`;
3. check the value rules;
4. create a complete record with `{}`;
5. add it with `push_back`;
6. go on to the next pass.

<!-- fragment -->
```cpp
const Shipment shipment{destination, boxes};
shipments.push_back(shipment);
```

- `shipment` is a complete record: both fields have values that were read and checked.
- `push_back` works as in lesson 6.2, only it adds a record: a **new element** with the same field values goes to the end of `shipments`. The number of elements grows by one, and the order of the elements is the order of the data.
- **The vector stores its own element.** It's a copy of the record `shipment`, independent of it like the copy in lesson 8.2, and not a second name for the same object. At the end of the pass the local `shipment` disappears, and the element in the vector stays. A later change of `destination` or `boxes` changes nothing in the vector.
- **`push_back` checks nothing.** An empty name or `-2` boxes are ordinary field values to the vector. The program decides what goes into the vector: it calls `push_back` only after all the checks.

## 6. An empty list and an error in a later record

**Predict** the result for the data `0` alone. Running it is optional.

<!-- input: shipment_list -->
```text
0
```

<details>
<summary>The standard output for 0 shipments</summary>

<!-- output: shipment_list -->
```text
Shipments: 0
Total boxes: 0
```

</details>

The loop doesn't run even once, so the program reads no name or number and doesn't call `getline(rest)`. An empty vector is a valid result: the report gives 0 shipments and the total 0, with no stand-in record. `0` without an end of line gives the same result, but the automatic tests don't run that case.

**Predict** also the result when the first shipment is valid and the second has `-2` boxes:

<!-- input: shipment_list -->
```text
2
North Hub
4
South Depot
-2
```

<details>
<summary>The standard output when the second shipment has -2 boxes</summary>

<!-- output: shipment_list -->
```text
Invalid shipments
```

</details>

When the program reads the second shipment, the first is already in the vector. The program doesn't remove it, but it doesn't show it either: it prints only `Invalid shipments` and stops. The result is either the full report of all the announced shipments or one message, never a part of the vector.

| Situation | Example | Result |
|---|---|---|
| a failed read | `two` instead of the number of shipments, `seven` instead of the number of boxes of the second shipment, 3 shipments announced but only 2 in the data | `Input error` |
| a successful read, a value not allowed | the number of shipments `-1` or `6`, an empty name of the second shipment, `-2` boxes | `Invalid shipments` |
| a successful read, values allowed | 0, 1 or 5 shipments | the report |

<details>
<summary>The other data in the table and their results</summary>

<!-- input: shipment_list -->
```text
two
```

<!-- output: shipment_list -->
```text
Input error
```

<!-- input: shipment_list -->
```text
2
North Hub
4
South Depot
seven
```

<!-- output: shipment_list -->
```text
Input error
```

<!-- input: shipment_list -->
```text
3
North Hub
4
South Depot
7
```

<!-- output: shipment_list -->
```text
Input error
```

<!-- input: shipment_list -->
```text
-1
```

<!-- output: shipment_list -->
```text
Invalid shipments
```

<!-- input: shipment_list -->
```text
6
```

<!-- output: shipment_list -->
```text
Invalid shipments
```

<!-- input: shipment_list -->
```text
2
North Hub
4

7
```

<!-- output: shipment_list -->
```text
Invalid shipments
```

<!-- input: shipment_list -->
```text
1
East Gate
3
```

<!-- output: shipment_list -->
```text
Shipments: 1
East Gate: 3
Total boxes: 3
```

<!-- input: shipment_list -->
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

<!-- output: shipment_list -->
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

## 7. Adding versus changing

| Operation | Meaning |
|---|---|
| `shipments.push_back(shipment)` | adds a new element at the end, and `size()` grows by 1 (lesson 6.2) |
| `for (Shipment& shipment : shipments)` and a change of a field | changes existing elements, and `size()` stays the same (lesson 9.3) |
| `for (const Shipment& shipment : shipments)` | only reads existing elements (lesson 8.4) |

`push_back` never updates an existing element: every call adds a new one. The report in section 2 only reads the elements, so its loop uses `const Shipment&`. In this lesson the programs don't change the elements after reading them.

## 8. Mission: workshop orders

A workshop takes several orders. The program reads their list, checks each order, and prints all the orders and the total of the work that is left.

**Input data:** the first line gives the number of orders. Then each order takes two lines:

1. the client's name, which may contain spaces;
2. two numbers separated by a space: the planned units of work and the completed units of work.

**Rules:**

- There are from 0 to 5 orders.
- The client's name can't be empty. Data that follow the agreement have no spaces at its start or end, and the program doesn't check for them. The same client may have several orders.
- The number of planned units must be greater than zero.
- The number of completed units must not be negative and must not exceed the number of planned units.
- All numbers are small and fit in an `int`, and so does their total.
- Text after the numbers is outside the agreement, and the program doesn't check it.

**Requirements:**

- The program defines its own order type with three fields: the client's name (`std::string`), the number of planned units (`int`) and the number of completed units (`int`). You choose the names of the type, the fields and the vector yourself.
- The orders go into an initially empty vector with `push_back`, only after the read and the rules are checked. The reading is in `main`, with no questions.
- When the required data can't be read, the program prints exactly `Input error`.
- When the read succeeded but the number of orders or the values of an order break the rules, the program prints exactly `Invalid orders`.
- At the first error the program prints the message and stops, with no part of the report.
- When everything is right, the program prints the number of orders from `size()`, each order in the order of the data, and the total of remaining units, as in the example below. All of this information comes from the elements of the vector.

In `cpp-workspace`, create a folder `workshop_orders`, copy `CMakeLists.txt` from the original `lesson_05_first_program` into it, create an empty `main.cpp`, and write the program yourself.

For the data:

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

the standard output must be:

<!-- output: orders -->
```text
Orders: 3
North Library: planned 12, completed 5, remaining 7
City Archive: planned 8, completed 8, remaining 0
Green Workshop: planned 6, completed 0, remaining 6
Remaining total: 13
```

When there are zero orders:

<!-- input: orders -->
```text
0
```

<!-- output: orders -->
```text
Orders: 0
Remaining total: 0
```

The second order has more completed units than planned. The first may already be in the vector, but there is no report:

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

Instead of the number of completed units of the second order, there is a word:

<!-- input: orders -->
```text
2
North Library
12 5
City Archive
8 done
```

<!-- output: orders -->
```text
Input error
```

The number of orders is negative:

<!-- input: orders -->
```text
-1
```

<!-- output: orders -->
```text
Invalid orders
```

A word instead of the number of orders, for example `three`, gives `Input error`.

**These aren't the shipments under another name.** The number line has two numbers, and one of the rules connects them. You have to decide yourself:

1. how to name the type, its fields and the vector, and which local variables you need to read one order;
2. how to write the loop counter and the loop condition;
3. where to finish the previous number line;
4. in what order to check the read and the rules, and how to stop the program at an error;
5. where to create the record and call `push_back`;
6. how to print the orders with a loop that uses a `const` reference;
7. how to calculate the total of remaining units from the fields of the vector's elements.

**Before you write the program**, prepare a table of cases: zero, one, two and five orders, names with spaces, completed and unstarted orders, a number of orders that isn't allowed, an empty name, units that aren't allowed, a word instead of a number, an error in an order after a valid one, a missing announced order, and a missing last number. Write down the expected result for each.

**Then** run the program for the main data and for one of two cases: zero orders or an error in the second order. All the cases in the full list of check cases are checked automatically, so you don't have to run the others. Analyse on paper the cases in which the data end.

### Success criterion

- The program builds as C++20 and prints exactly the results shown for the main data and for the second case you chose, with the clients' names including their spaces.
- The previous number line is finished at the start of the pass, and there is no read after the last number.
- `std::cin.fail()` is checked before the rules, the record is created and added to the vector only after both checks, and at an error there is no part of the report.
- The number of orders comes from `size()`, and the lines and the total from the elements of the vector, read through a `const` reference.
- The table of cases was made before you ran the program.
- You can explain why, after an error in the second order, the first may be in the vector, and yet the program doesn't print it.

When the result is right, you can save the project in Git, as in lesson 1.5.

<details>
<summary>Hint 1</summary>

How do you create an initially empty collection of orders? What should happen after one order has been read successfully?

</details>

<details>
<summary>Hint 2</summary>

Each pass of the loop should prepare the local data of one order, check them, and only then add the complete record to the vector.

</details>

<details>
<summary>Hint 3</summary>

At the start of the pass, finish the previous number line. Read the name and both numbers. After a successful read and a check of the values, create the record and add it with `push_back`, and after reading all the orders, go through the vector and calculate the result.

</details>

<details>
<summary>The full list of check cases: open it after preparing your own table</summary>

Successive lines of the data are separated by `/`. For valid data, the "Result" column gives the number of orders and the total of remaining units. The program then prints all the orders in the order of the data.

| | Data | Result | What it checks |
|---|---|---|---|
| A | `3` / `North Library` / `12 5` / `City Archive` / `8 8` / `Green Workshop` / `6 0` | 3 orders, total 13 | the data from the requirements: names with spaces, a completed and an unstarted order |
| B | `0` | 0 orders, total 0 | an empty vector (the data from the requirements) |
| C | `1` / `Harbor Office` / `10 3` | 1 order, total 7 | one order |
| D | `2` / `Park School` / `9 4` / `City Archive` / `8 2` | 2 orders, total 11 | two orders, a different order of names |
| E | `5` / `Art Room` / `4 1` / `Book Club` / `6 6` / `Art Room` / `3 0` / `Main Office` / `10 9` / `Tool Shed` / `2 1` | 5 orders, total 8 | the largest number of orders, the same client twice |
| F | `-1` | `Invalid orders` | a negative number of orders (the data from the requirements) |
| G | `6` | `Invalid orders` | a number of orders greater than 5: the program reads no order |
| H | `three` | `Input error` | a word instead of the number of orders |
| I | `2` / an empty line / `12 5` / `City Archive` / `8 8` | `Invalid orders` | an empty name of the first order |
| J | `2` / `North Library` / `12 5` / an empty line / `8 8` | `Invalid orders` | an empty name of a later order |
| K | `2` / `North Library` / `12 5` / `City Archive` / `0 0` | `Invalid orders` | zero planned units |
| L | `1` / `North Library` / `-4 0` | `Invalid orders` | a negative number of planned units |
| M | `1` / `North Library` / `12 -1` | `Invalid orders` | a negative number of completed units |
| N | `2` / `North Library` / `12 5` / `City Archive` / `8 9` | `Invalid orders` | more completed units than planned, after a valid order (the data from the requirements) |
| O | `2` / `North Library` / `12 5` / `City Archive` / `8 done` | `Input error` | a word instead of the second number, after a valid order (the data from the requirements) |
| P | `2` / `North Library` / `twelve 5` / `City Archive` / `8 8` | `Input error` | a word instead of the first number |
| Q | `2` / `North Library` / `12 5`, then the end of the data | `Input error` | an announced order is missing: reading its name fails |
| R | `2` / `North Library` / `12 5` / `City Archive` / `8`, then the end of the data | `Input error` | a missing last number |

**The automatic tests and your runs.** All the cases are checked automatically: the reference solution is run for each of them, and its whole standard output is compared with the expected one. The solution and its results are in [Example solutions](#example-solutions).

</details>

An example solution is in [Example solutions](#example-solutions).

## 9. Find the bug: a record added too early

Do this task **after the mission**: the program below should work the same as the program of section 2. You can copy it into `main.cpp` in the `lesson_10_3` folder.

<details>
<summary>The program to check: open it after writing your own program</summary>

<!-- example: shipment_list_early_bug -->
```cpp
#include <iostream>
#include <string>
#include <vector>

struct Shipment {
    std::string destination;
    int boxes;
};

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

        const Shipment shipment{destination, boxes};
        shipments.push_back(shipment);

        std::cin >> boxes;

        if (std::cin.fail()) {
            std::cout << "Input error\n";
            return 0;
        }

        if (destination.empty() || boxes < 0) {
            std::cout << "Invalid shipments\n";
            return 0;
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

Data in which every shipment has 0 boxes:

<!-- input: shipment_list_early_bug -->
```text
2
North Hub
0
South Depot
0
```

1. **Predict** the result of this program and of the program of section 2 for these data.
2. Run the program for these data and compare the result with your prediction.
3. Choose your own valid data for which this program prints a wrong result.
4. For your data, **predict** when each record is created and added to the vector, what number of boxes its field has at that moment, and what number `>>` reads later.
5. Run the program for your data.
6. Explain why the number of boxes that was read correctly didn't get into the vector's element. Does a later change of the variable `boxes` change that element?
7. Move the creation of the record and `push_back` after both checks, and run the fixed program for your data. Why must `push_back` come only after all the fields are checked?
8. The buggy program adds the record before it checks the read. What would be in the vector if a word were typed instead of the number of boxes? Why doesn't it show in the result?

</details>

The results, example data and the fixed program are in [Example solutions](#example-solutions).

## 10. When something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `Input error` for valid data | The line with the number of records isn't finished, because `getline(rest)` is missing or stands only at the end of the pass. The first name is empty, and the read of the number hits the real name. | Call `std::getline(std::cin, rest)` at the start of every pass. |
| The report has zeros instead of the numbers that were read | The record is created and added to the vector before the program reads the numbers (section 9). | Create the record and call `push_back` after the read and both checks. |
| After `Input error` or `Invalid orders` the program still prints a report | `return 0;` is missing after the message, so the loop and the report go on. | After an error message, end `main` with `return 0;`. |
| The report contains an order with the number 0, although the data had a word | The `std::cin.fail()` check before `push_back` is missing. You can't rely on the contents of a variable after a failed read (lesson 4.6). | Check the read before the rules and before adding the record. |
| `Remaining total` is smaller than it should be, or some remaining number is negative | The program lets through more completed units than planned. | Check this rule for every order. |
| The program waits, although all the lines were typed | The announced number of records is greater than the number typed, or a number is missing. `>>` skips empty lines and waits for a number (lesson 10.1). | Type the missing data, or correct the number in the first line. |
| The compiler reports `no matching member function for call to 'push_back'` | The vector is `const`, so nothing can be added to it (lesson 6.2). | Remove `const` from the definition of the vector that should receive the records. |

## 11. Explain

Answer in your own words, preferably in writing. Only then compare with the example answers.

1. Why is the vector of shipments empty at the start, and why doesn't it have `const`?
2. What does `shipments.push_back(shipment)` do? Where does the new element go, and how does `size()` change?
3. Why is the record created and added to the vector only after the read and the rules are checked? Would `push_back` check whether it is valid?
4. If the program changed the variable `boxes` after `push_back`, would the vector's element change? Why?
5. Why does `getline(rest)` stand at the start of the pass and not after the loop? What does it finish in the first pass, and what in the second?
6. What does the program do for the data `0`? Why is that a valid result and not an error?
7. The first order is valid and the second has `8 9`. What is in the vector then, and what does the program print? Why doesn't it print the first order?
8. How does the announced number of orders differ from the vector's `size()`? Why does the report use `size()`?
9. How does `push_back` differ from changing a field of an element in a loop with a reference without `const`? Why does the report's loop use a `const` reference?

<details>
<summary>Example answers</summary>

1. Before the program reads anything, there is no shipment yet, so the vector is created empty with `{}`. It has no `const`, because the program will add elements to it (lesson 6.2).
2. It adds at the end of the vector a new element with the field values of the record `shipment`. The earlier elements stay in their places, and `size()` grows by 1. So the order of the elements is the order of the `push_back` calls.
3. Because only complete and valid records should go into the vector. `push_back` checks nothing: it would also add a record with an empty name or with a number that isn't allowed. The program decides what goes into the vector, by calling `push_back` only after both checks.
4. No. The vector stores its own element, a copy of the record at the moment of the `push_back` call (lesson 8.2). The element isn't a second name for the variable `boxes` or for the local record, so a later change of `boxes` doesn't affect it. That is the bug of section 9.
5. Because before each name the line of the previous number must be finished. In the first pass it's the line with the number of records, and in the second the number line of the first record. After the loop no name follows, so the program doesn't finish the line. If the data ended right after the last number, with no end of line, an extra `getline` would fail and turn valid data into `Input error`.
6. It reads the number 0, checks that it's in range, and doesn't run the loop even once. The vector stays empty, and the report gives 0 orders and the total 0. Zero orders is an allowed situation, not missing data: the number was read correctly.
7. The vector holds the first order, because it was added before the program read the second. The second wasn't added. The program prints only `Invalid orders` and stops, because the result is about the whole list: a partial report would look complete.
8. The announced number is a value read from the data, while `size()` says how many records are really in the vector. With valid data they are equal. The report describes the contents of the vector, so it takes the number of orders from `size()`.
9. `push_back` adds a new element and increases `size()`. A loop with a reference without `const`, for example `for (Shipment& shipment : shipments)`, changes the fields of elements that are already in the vector, and their number doesn't change (lesson 9.3). The report only reads the elements, so a `const` reference is enough and makes sure that the report changes nothing.

</details>

## Summary

- The first line of the data announces the number of records. The program checks its read and its range before the loop, and zero records is a valid, empty list.
- Each pass starts by finishing the previous line, so there is no read after the last number.
- Each pass reads the fields into local variables, checks `std::cin.fail()`, then the rules, and only then creates a complete record and adds it with `push_back`.
- `push_back` checks nothing: it adds the vector's own element at the end and increases `size()`.
- At the first error the program prints only a message and stops, with no partial report.
- The report comes from the vector: the number of records from `size()`, and the rest from the fields of the elements, read through a `const` reference.

## What's next

In this lesson the number of records was known from the first line of the data, and all the reading was in `main`. In the next lesson the reading of one record moves into its own function, and the program reads records until the end of the data. Lesson 10.4 is in preparation.

---

## Example solutions

Look here **after your own attempt**. Your names may differ, as long as the standard output is the one required.

<details>
<summary>Section 8: the mission, workshop orders</summary>

<!-- example: orders -->
```cpp
#include <iostream>
#include <string>
#include <vector>

struct Order {
    std::string client;
    int planned_units;
    int completed_units;
};

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

    int remaining_total{0};
    std::cout << "Orders: " << orders.size() << "\n";

    for (const Order& order : orders) {
        const int remaining{order.planned_units - order.completed_units};
        std::cout << order.client << ": planned " << order.planned_units << ", completed " << order.completed_units << ", remaining " << remaining << "\n";
        remaining_total += remaining;
    }

    std::cout << "Remaining total: " << remaining_total << "\n";
}
```

1. **An empty vector at the start,** because before the reading there is no order yet. The elements are added only in the loop.
2. **The number of orders first,** because it decides how many passes the loop makes.
3. **A check of its range** before the loop, because `-1` or `6` are values that were read correctly but aren't allowed. The program then reads no order.
4. **For zero orders** the condition `index < count` is false at once, so the loop doesn't run and the vector stays empty.
5. **Finishing at the start of the pass,** because an unfinished line comes before each name: in the first pass the line with the number of orders, in the later ones the number line of the previous order.
6. **No finishing after the loop,** because the program reads no further name. An extra `getline` could turn valid data into `Input error` when they end without an end of line.
7. **Starting values of the local variables,** because after a failed read a variable may keep its earlier value. Each pass starts with its own, new variables.
8. **The read before the values,** because you can't rely on the contents of variables after a failed read. The rules make sense only for numbers that were really read.
9. **An order that isn't allowed doesn't go into the vector,** because `return 0;` ends `main` before the program reaches `push_back`.
10. **`push_back` after creating a complete record,** because only orders whose fields have all been read and checked should go into the vector.
11. **The vector stores its own element:** a copy of the record `order`, independent of it. The local record disappears at the end of the pass, and the element stays.
12. **`size()` is the number of records added,** because each `push_back` call increases it by 1, and nothing else changes it.
13. **Earlier valid orders may stay in the vector** after an error in a later one. The program doesn't remove them, because it stops right away.
14. **Still no partial report,** because the result is about the whole list. A report of some of the orders would look complete, although the data were wrong.
15. **Printing through `const Order&`,** because the loop only reads the elements and doesn't copy them in each pass (lesson 8.4).
16. **No modifiable reference,** because the report changes nothing. `const` makes sure the compiler won't allow an accidental change.
17. **Adding versus changing:** `push_back` adds a new element and increases `size()`, while a change through `Order&` would affect existing elements (lesson 9.3). The mission doesn't change the orders after reading them.
18. **No function that reads a record,** because reading one order fits readably into the loop in `main`, and the agreement doesn't require such a function.
19. **What is left for lesson 10.4:** a function that reads one record, and reading records up to the end of the data when their number isn't announced.

**Other valid solutions:** instead of `return 0;` you can use a `bool` flag, as in lessons 4.5 and 7.4. The loop then runs while the flag is true and announced records remain, and after the loop the program chooses the message or the report. The rules can stand in several separate conditions with the same message. The total can be calculated in a separate loop over the vector, and the remaining units directly in the print statement.

Each case in the list of check cases is a separate run of this program. Cases A, B, F, N and O are the data from the mission's text. The others are below, in the order of the list of check cases.

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
<summary>Section 9: the results before the fix, and the fixed program</summary>

Before the fix, for the data with zero boxes:

<!-- output: shipment_list_early_bug -->
```text
Shipments: 2
North Hub: 0
South Depot: 0
Total boxes: 0
```

- **This case masks the bug.** The program of section 2 prints the same for these data. The buggy program creates each record with 0 boxes, the starting value of the variable `boxes`, and the data have 0 too. The record in the vector matches the data by chance.
- **Data that reveal the bug:** any valid data in which at least one shipment has a positive number of boxes, for example the data of section 2. The correct result is the report with the numbers 4 and 7 and the total 11, but the buggy program prints:

<!-- input: shipment_list_early_bug -->
```text
2
North Hub
4
South Depot
7
```

<!-- output: shipment_list_early_bug -->
```text
Shipments: 2
North Hub: 0
South Depot: 0
Total boxes: 0
```

- **When the record is created:** right after the name is read, while `boxes` still has its starting value 0. `push_back` adds an element with 0 boxes to the vector.
- **Why the number doesn't get into the vector:** `>>` reads 4 and stores it in the variable `boxes`, and both checks pass. But the vector's element is its own copy of the record from the moment of `push_back`, not a second name for the variable `boxes`. The change of `boxes` doesn't affect it, so the report shows 0.
- **A word instead of the number of boxes:** the vector would already hold a record whose number of boxes was never read. The result is `Input error` anyway, because the program stops with no report, so in this program it doesn't show. If the program printed the shipments from the vector after an error, it would show a number of boxes that wasn't in the data.
- **The fix:** move the creation of the record and `push_back` after both checks. Then only a record whose fields have all been read and checked goes into the vector. The fixed program is the program of section 2:

<!-- example: shipment_list_early_fixed -->
```cpp
#include <iostream>
#include <string>
#include <vector>

struct Shipment {
    std::string destination;
    int boxes;
};

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

    int total_boxes{0};
    std::cout << "Shipments: " << shipments.size() << "\n";

    for (const Shipment& shipment : shipments) {
        std::cout << shipment.destination << ": " << shipment.boxes << "\n";
        total_boxes += shipment.boxes;
    }

    std::cout << "Total boxes: " << total_boxes << "\n";
}
```

<!-- input: shipment_list_early_fixed -->
```text
2
North Hub
4
South Depot
7
```

<!-- output: shipment_list_early_fixed -->
```text
Shipments: 2
North Hub: 4
South Depot: 7
Total boxes: 11
```

For the data with zero boxes the fixed program prints the same as the buggy program:

<!-- input: shipment_list_early_fixed -->
```text
2
North Hub
0
South Depot
0
```

<!-- output: shipment_list_early_fixed -->
```text
Shipments: 2
North Hub: 0
South Depot: 0
Total boxes: 0
```

</details>

**Previous lesson:** [Lesson 10.2: Names with spaces: `>>` and `std::getline`](lesson_02_names_with_spaces.en.md) · **Next lesson:** in preparation · [Course overview](../../README.en.md)

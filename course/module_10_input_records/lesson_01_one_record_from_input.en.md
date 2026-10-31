# Lesson 10.1: One record from input

[Polski](lesson_01_one_record_from_input.md) · **English** · [Course overview](../../README.en.md)

> **Module 10, lesson 1** · about 65–80 minutes
> **You need:** your `cpp-workspace` folder and the original `lesson_05_first_program` project, as before. You won't need the debugger in this lesson.
> **Pilot version.** The programs in this lesson are checked automatically on Windows, Ubuntu and macOS, including with the given input data. Typing input in CLion's **Run** window is described without a manual check on every system.

## Before you start

This lesson assumes that you:

- read a number and a single word with `std::cin >>` (lessons 2.6 and 2.7);
- check with `std::cin.fail()` whether a read succeeded, and tell a rejected value from a failed read (lesson 4.5);
- know that after a failed read you can't rely on the variable's value (lesson 4.6);
- choose one of several possibilities with `if`, `else if` and `else` (lesson 3.3), and combine conditions with `||` (lesson 3.4);
- define your own type with `struct` and create an object of it with `{}` (lesson 8.1);
- know the rule "check first, then change" from lesson 9.2.

## The situation

Until now, the values of records were written in the code:

<!-- fragment -->
```cpp
const Parcel parcel{"BX-7", 5};
```

In this course, a **record** is an object that stores several related pieces of information, for example a parcel's identifier and its weight. We describe its type with the `struct` you already know. "Record" isn't a C++ keyword. The definition `struct Parcel` describes what every parcel consists of, and a record is one concrete object of that type, for example `parcel`.

Now the identifier and the weight aren't known when the program is written. The program gets them only after it starts, from the standard input. But the data may be wrong: a word may appear instead of the weight, the weight may be missing, or it may be zero. The program shouldn't build a parcel from such data.

What's new isn't C++ syntax, but the order of operations you already know:

1. read the values into ordinary variables;
2. check whether the read succeeded;
3. check whether the values follow the rules;
4. only then create a complete record and use its fields as in Module 8.

After this lesson you'll:

- read the fields of one record with `>>` into initialised local variables;
- check first whether the read succeeded, and only then the rules for the values;
- tell a failed read from a value that was read correctly but isn't allowed;
- create a record with `{}` only when all its fields have been read and accepted;
- predict how the program behaves when fields are missing or wrong;
- choose data that reveal a wrong order of checks.

## 1. Prepare the project

In `cpp-workspace`, create a folder `lesson_10_1` and copy `main.cpp` and `CMakeLists.txt` from the original `lesson_05_first_program` into it. You type the program from section 2 into this folder's `main.cpp`.

The programs in this lesson print no questions. After starting one, type all the values straight away, separated by spaces, and press **Enter**.

## 2. One parcel from the input

A parcel has an identifier and a weight in arbitrary units. The identifier is one ASCII word, with no spaces. The weight must be greater than zero.

<!-- example: parcel -->
```cpp
#include <iostream>
#include <string>

struct Parcel {
    std::string id;
    int weight;
};

int main() {
    std::string id{};
    int weight{0};

    std::cin >> id;
    std::cin >> weight;

    if (std::cin.fail()) {
        std::cout << "Input error\n";
    } else if (weight <= 0) {
        std::cout << "Invalid parcel\n";
    } else {
        const Parcel parcel{id, weight};

        std::cout << "Parcel: " << parcel.id << "\n";
        std::cout << "Weight: " << parcel.weight << "\n";
    }
}
```

Run the program and type:

<!-- input: parcel -->
```text
BX-7 5
```

<!-- output: parcel -->
```text
Parcel: BX-7
Weight: 5
```

| Code | What it does |
|---|---|
| `std::string id{};` and `int weight{0};` | prepare the variables for the values being read, with starting values |
| two `>>` reads | store the word `BX-7` and the number 5 in these variables |
| `if (std::cin.fail())` | checks whether **both** reads succeeded |
| `else if (weight <= 0)` | checks the parcel's rule, but only after a successful read |
| `const Parcel parcel{id, weight};` | creates the record from the values that were read and checked |

- **The record comes into being only in the last branch.** With wrong data the program doesn't create it at all, so there's no parcel with an accidental identifier or weight.
- **One `fail()` after both reads is enough.** When the first read fails, the stream stays in the error state and the second one fails too (lesson 4.6). So after both reads, `fail()` gives `false` only when both succeeded.
- **`parcel` has `const`,** because it doesn't change after it's created. The variables `id` and `weight` can't have `const`, because `>>` stores values in them (lesson 2.6).
- **The program prints exactly one of three results:** the parcel, `Input error` or `Invalid parcel`. It doesn't ask again, so it needs no loop.

## 3. The read first, then the rules

Two cases look similar, but they're two different problems. **Predict** the result of each and compare it with the collapsed result. Running them is optional.

**Case A:** a word instead of the weight.

<!-- input: parcel -->
```text
BX-7 five
```

<details>
<summary>Standard output for case A</summary>

<!-- output: parcel -->
```text
Input error
```

</details>

**Case B:** a weight equal to zero.

<!-- input: parcel -->
```text
BX-7 0
```

<details>
<summary>Standard output for case B</summary>

<!-- output: parcel -->
```text
Invalid parcel
```

</details>

| | A: `BX-7 five` | B: `BX-7 0` |
|---|---|---|
| Did the read of the weight succeed? | no: `five` isn't an `int` number | yes: 0 is a valid `int` number |
| What does the program check? | `fail()` gives `true`, so it stops there | `fail()` gives `false`, so it checks the rule: 0 isn't positive |
| Result | `Input error` | `Invalid parcel` |

This is the same split as in lesson 4.5: **a failed read** and **a rejected value**. `std::cin.fail()` only says whether a number could be read. It knows nothing about the parcel's rules: 0 and -3 are ordinary, correctly read numbers to it. Only the condition `weight <= 0` checks the rule.

**Why this order?** After a failed read you can't rely on the value of `weight` (lesson 4.6), because that number doesn't come from the data. So first you need to know whether there are any data at all, and only then ask whether they're good.

## 4. A missing value and the end of the data

The data may end before the program has read all the values:

<!-- input: parcel -->
```text
BX-7
```

<details>
<summary>Standard output when the data end after BX-7</summary>

<!-- output: parcel -->
```text
Input error
```

</details>

The identifier was read, but there's no weight: reading the number fails, because the data have ended (lesson 4.6). This isn't a complete record, so the program doesn't create it. It doesn't tell whether the cause was text instead of a number or the end of the data: in both cases it prints `Input error`.

**You can't cause this case by typing the data yourself.** When you type `BX-7` and press **Enter**, the program simply waits for the weight, as in lesson 2.6. The end of the data happens when the data arrive in one piece, for example in the course's automatic tests. Predict this case on paper, as in lesson 4.5.

**`>>` isn't `getline`.** `>>` skips whitespace before a value, including empty lines. So pressing **Enter** alone ends nothing: the program keeps waiting. In lesson 7.4, `std::getline` treated an empty line differently, as a successful read of an empty text.

## 5. Gaps and spaces in the data

`>>` skips whitespace before a value and stops reading at the first whitespace after it. Whitespace means a space, a tab and the end of a line, so the values don't have to stand on one line. **Predict** what the program prints when the identifier and the weight are on separate lines:

<!-- input: parcel -->
```text
BX-7
5
```

<details>
<summary>Standard output for the values on two lines</summary>

<!-- output: parcel -->
```text
Parcel: BX-7
Weight: 5
```

</details>

This lesson has two deliberate limits.

**The identifier can't contain a space.** `>>` reads one word into a `std::string` (lesson 2.7). **Predict** the result for a name with a space:

<!-- input: parcel -->
```text
Big box 5
```

<details>
<summary>Standard output for Big box 5</summary>

<!-- output: parcel -->
```text
Input error
```

</details>

Only `Big` goes into `id`, and the read of the weight runs into `box` and fails. You'll read text with spaces in lesson 10.2.

**The program doesn't check what comes after the last value.** A successful read of two values doesn't prove that no more characters follow:

<!-- input: parcel -->
```text
BX-7 5 kg
```

<details>
<summary>Standard output for BX-7 5 kg</summary>

<!-- output: parcel -->
```text
Parcel: BX-7
Weight: 5
```

</details>

The program reads exactly two values, and `kg` stays unread in the input, like the rest of the line in lesson 2.7. Likewise, `5kg` would give the weight 5, like `12abc` in lesson 4.5. Data that follow the agreement contain exactly the required values, and in this lesson we deliberately leave out checking the rest of the line.

| Situation | Example | The program's result |
|---|---|---|
| a failed read of a required value | `BX-7 five`, `BX-7`, `Big box 5` | `Input error` |
| a value that was read, but breaks the rules | `BX-7 0` | `Invalid parcel` |
| extra text after the last value | `BX-7 5 kg` | outside this lesson's checks: the program prints the parcel |

## 6. Mission: room occupancy

The program reads the data of one room and prints how many free seats it has.

**Input data:** three values separated by whitespace: the room's code, the number of all seats (the capacity) and the number of occupied seats.

**Rules:**

- The code is a non-empty ASCII text with no spaces. The program doesn't check its characters. We read one room, so whether the code is unique doesn't matter.
- The capacity must be greater than zero.
- The number of occupied seats must be non-negative and can't exceed the capacity.
- All numbers are small and fit in an `int`.
- The free seats are the capacity minus the number of occupied seats.

**Requirements:**

- The program defines its own type with three fields: the code (`std::string`), the capacity (`int`) and the number of occupied seats (`int`). You choose the names of the type and the fields yourself. The type has no field for the free seats: that's a value calculated from the other two fields.
- The program reads three values with `>>` into local variables in `main`. It prints no questions, doesn't ask again and uses neither `std::getline` nor a vector.
- When the read failed, the program prints exactly `Input error` and doesn't check the rules.
- When the read succeeded but the values break the rules, the program prints exactly `Invalid room`.
- Only when everything is right does the program create the room record with `{}` and print four lines as in the example below. The number of free seats comes from the fields of that record.

In `cpp-workspace`, create a folder `room_check`, copy `CMakeLists.txt` from the original `lesson_05_first_program` into it, create an empty `main.cpp` and write the program on your own.

For the data:

<!-- input: room -->
```text
R-12 12 8
```

the standard output must be:

<!-- output: room -->
```text
Room: R-12
Capacity: 12
Occupied: 8
Available: 4
```

Reading the third value fails:

<!-- input: room -->
```text
R-12 12 eight
```

<!-- output: room -->
```text
Input error
```

The read succeeds, but more seats are occupied than there are in total:

<!-- input: room -->
```text
R-12 8 9
```

<!-- output: room -->
```text
Invalid room
```

In one run, the program prints only one of these three results.

**This isn't the parcel under another name.** A room has a third field, and one of the rules connects two numbers. You decide on your own:

1. what to call the type and the fields, and which types to use;
2. which local variables you need for reading, and why they must have starting values;
3. how to check that all three reads succeeded;
4. how to separate a failed read from values that aren't allowed, and in which order to check them;
5. how to write the three rules for the values;
6. where to create the record, and how to initialise its fields;
7. how to calculate the free seats from the record's fields;
8. why checking the numbers alone, without the stream's state, isn't enough.

**Before you write the program**, prepare a table of cases: a valid room, an empty and a full room, a capacity of 1, a zero and a negative capacity, a negative number of occupied seats, more occupied seats than seats in total, a word instead of the first or the second number, a missing last value. For each, write down the expected result: the room's four lines, `Input error` or `Invalid room`.

**Then** run the program for the three data shown above. Every case in the full list of check cases is checked automatically, so you don't need to run the others. Analyse the cases with a missing value on paper: typing the data yourself, you can't cause the end of the data (section 4).

### Success criterion

- The program builds as C++20 and, for the three data shown above, prints exactly the results shown.
- There is one type with three fields, with no field for the free seats.
- The variables for reading have starting values, and the record comes into being only after the read and all the rules have been checked.
- `std::cin.fail()` is checked before the rules for the values.
- The number of free seats comes from the fields of the created record.
- The table of cases was made before running the program.
- You can explain the difference between `Input error` and `Invalid room`.

When the result matches, you can save the project in Git, as in lesson 1.5.

<details>
<summary>Hint 1</summary>

Before you create the record, think about whether all its fields could be read.

</details>

<details>
<summary>Hint 2</summary>

A failed read and a value that doesn't follow the room's rules are two different situations. In which order should the program check them?

</details>

<details>
<summary>Hint 3</summary>

Prepare ordinary variables, read the data into them, check the success and the limits, and only then initialise the room record with `{}`.

</details>

<details>
<summary>The full list of check cases: open it after preparing your own table</summary>

For a valid room, the "Result" column gives the number of free seats. The program then prints all four lines.

| | Data | Result | What it checks |
|---|---|---|---|
| A | `R-12 12 8` | 4 | the data in the requirements |
| B | `R-01 10 0` | 10 | an empty room: 0 occupied seats is a valid value |
| C | `R-02 10 10` | 0 | a full room: the occupied seats equal the capacity |
| D | `R-03 1 0` | 1 | the smallest capacity |
| E | `R-04 1 1` | 0 | one seat, occupied |
| F | `R-05 0 0` | `Invalid room` | a zero capacity |
| G | `R-06 -2 0` | `Invalid room` | a negative capacity |
| H | `R-07 10 -1` | `Invalid room` | a negative number of occupied seats |
| I | `R-08 8 9` | `Invalid room` | more occupied seats than seats in total |
| J | `R-09 twelve 3` | `Input error` | a word instead of the first number |
| K | `R-10 12 eight` | `Input error` | a word instead of the second number |
| L | `R-11 12` | `Input error` | a missing last value: the data end |
| M | `R-13` | `Input error` | the code alone, with no numbers |
| N | an empty line | `Input error` | no value at all: an empty line, followed by the end of the data |
| O | `LAB-2`, `30` and `25`, each on its own line | 5 | values on separate lines |
| P | `Aula-3   20   5` | 15 | several spaces between the values, another code |
| Q | `R-14 6 2 extra` | 4 | extra text after the third value: outside this lesson's checks |

**Automatic tests and your own runs.** Every case is checked automatically: the reference solution is run for each of them, and its whole standard output is compared with the expected one. The solution and its results are in [Example solutions](#example-solutions).

</details>

The example solution is in [Example solutions](#example-solutions).

## 7. Find the bug: the weight checked before the read

Do this task **after the mission**: the program below is meant to work the same way as the program in section 2. You can type it in or copy it into `main.cpp`.

<details>
<summary>The program to check: open it after writing your own program</summary>

<!-- example: parcel_order_bug -->
```cpp
#include <iostream>
#include <string>

struct Parcel {
    std::string id;
    int weight;
};

int main() {
    std::string id{};
    int weight{0};

    std::cin >> id;
    std::cin >> weight;

    if (weight <= 0) {
        std::cout << "Invalid parcel\n";
    } else if (std::cin.fail()) {
        std::cout << "Input error\n";
    } else {
        const Parcel parcel{id, weight};

        std::cout << "Parcel: " << parcel.id << "\n";
        std::cout << "Weight: " << parcel.weight << "\n";
    }
}
```

Valid data:

<!-- input: parcel_order_bug -->
```text
BX-7 5
```

1. **Predict** the result for these data. They're the same data as in section 2, so compare your answer with the result in section 2. Running it is optional.
2. Choose your own data for which this program prints a wrong result.
3. For your data, **predict**: will the read of the weight succeed? Which branch will this program choose, and which the program in section 2?
4. Run the program for your data.
5. Explain how a failed read and a weight that isn't allowed differ here, and why the program mixed them up.
6. Fix the order of the checks.
7. Run the fixed program for your data.
8. Did the fix need a new C++ construct? What actually changed?

</details>

The results, example data and the fixed program are in [Example solutions](#example-solutions).

## 8. When something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| The program prints nothing and waits | Not all values have been typed yet. `>>` waits for the next one, and an empty line doesn't supply it (section 4). | Type the missing values and press **Enter**. |
| `Invalid room` or `Invalid parcel` for a word instead of a number | The program checks the rules before `std::cin.fail()` (section 7). | Check the read first, then the rules. |
| The program prints a room, although one of the numbers was a word | The program doesn't check `std::cin.fail()` and uses a value that doesn't come from the data. | Check `std::cin.fail()` after all the reads, before you use the values. |
| For a capacity of 0 the program prints a room | The condition lets 0 through, for example `capacity < 0` instead of `capacity <= 0`. | The capacity must be greater than zero, so 0 must be rejected too. |
| `Available` is negative | The rule that there can't be more occupied seats than seats in total is missing. | Reject data in which the number of occupied seats exceeds the capacity. |
| A code with a space, for example `R 12 12 8`, gives a room `R` with wrong numbers | `>>` reads one word: the code becomes `R`, and the numbers shift by one value. | The code in this lesson has no spaces. You'll read text with spaces in lesson 10.2. |
| A compile error at `>>` whose first line ends with `'const int'` | The variable you read into has `const` (lesson 2.6). | Remove `const` from that variable. The record created after the checks can have `const`. |

## 9. Explain

Answer in your own words, preferably in writing. Only then compare with the example answers.

1. Why does the program read the data into local variables with starting values, and create the record only after the checks?
2. Does `std::cin.fail()` check whether the capacity is positive? How does it differ from the condition `capacity <= 0`?
3. Can the number `-1` be read correctly into an `int`? What does the room program print for `R-07 10 -1`?
4. What happens when a word appears instead of a number? And when the last value is missing? Why is no record created in either case?
5. Why does a room code with a space need a different way of reading? Does `>>` need the values on separate lines?
6. Do three successful reads guarantee that no more data follow the last value?
7. Why doesn't the program calculate the free seats after a failed read?
8. How do `Input error` and `Invalid room` differ? Why does the program check them in this order?
9. Why does the room type have no field for the free seats?

<details>
<summary>Example answers</summary>

1. Because before the checks, it isn't known whether the values are complete and valid. Local variables can hold values from a failed read, but the program builds nothing from them. A record created at the end always has all its fields read and accepted. The starting values are needed because after a failed read a variable may keep the value it had. Without a starting value that would be an indeterminate value, and reading it would be a bug in the program.
2. No. `fail()` only says whether the read succeeded, that is, whether there was an `int` number in the data. `capacity <= 0` checks the room's rule for a number that has already been read correctly. A capacity of 0 is a successful read and, at the same time, a value that isn't allowed.
3. Yes. -1 is a valid `int` number, so `fail()` gives `false`. But it breaks the rule of a non-negative number of occupied seats, so the program prints `Invalid room`.
4. In both cases reading the number fails: a word isn't a number, and after the end of the data there's nothing to read. `fail()` gives `true` and the program prints `Input error`. No record is created, because the program doesn't have all the values from the data.
5. Because `>>` stops reading text at the first whitespace, so a space would split the code into two values. A whole line with spaces is read by `std::getline`, and you'll learn how to combine it with `>>` in lesson 10.2. Separate lines aren't needed: a space, a tab and the end of a line all separate values the same way.
6. No. The program reads exactly three values, and whatever follows stays unread in the input. For `R-14 6 2 extra` the program prints the room (case Q). In this lesson we deliberately don't check this: data that follow the agreement have exactly three values.
7. Because after a failed read you can't rely on the variables' values (lesson 4.6). A result calculated from them would look like a real number of free seats, although it wouldn't come from the data.
8. `Input error` means that not all values could be read. `Invalid room` means that all values were read correctly, but they break the room's rules. We check the read first, because the rules make sense only for values that come from the data. In the reverse order, a missing valid number could be taken for a value that isn't allowed, as in section 7.
9. Because the free seats follow from two other fields. A separate field could disagree with them, and the program would have to make sure it's always up to date. Calculating them from the record's fields always gives a result that matches the capacity and the number of occupied seats.

</details>

## Summary

- A record is an object of a struct that stores several related pieces of information. When its values come from the input, the program first reads them into local variables with starting values.
- The order is fixed: the read, checking the read with `std::cin.fail()`, checking the rules, and only then creating the record with `{}`.
- `fail()` says whether a read succeeded, not whether a value is allowed. A failed read and a value that isn't allowed are two different results.
- After a failed read you can't rely on the variables' values, which is why the rules are checked only after a successful read.
- `>>` separates values by any whitespace, including the end of a line, and reads text only up to the first space. It doesn't check what comes after the last value.
- With wrong data the program creates no record and prints nothing from one.

## What's next

In this lesson the text in the record was a single word. In the next lesson a record will contain text with spaces next to numbers, so the program will combine `>>` with `std::getline`. Go on to lesson [10.2: Names with spaces: `>>` and `std::getline`](lesson_02_names_with_spaces.en.md).

---

## Example solutions

Look here **after your own attempt**. Your names may differ, as long as the standard output is as required.

<details>
<summary>Section 6: the mission, room occupancy</summary>

<!-- example: room -->
```cpp
#include <iostream>
#include <string>

struct Room {
    std::string code;
    int capacity;
    int occupied;
};

int main() {
    std::string code{};
    int capacity{0};
    int occupied{0};

    std::cin >> code;
    std::cin >> capacity;
    std::cin >> occupied;

    if (std::cin.fail()) {
        std::cout << "Input error\n";
    } else if (capacity <= 0 || occupied < 0 || occupied > capacity) {
        std::cout << "Invalid room\n";
    } else {
        const Room room{code, capacity, occupied};

        std::cout << "Room: " << room.code << "\n";
        std::cout << "Capacity: " << room.capacity << "\n";
        std::cout << "Occupied: " << room.occupied << "\n";
        std::cout << "Available: " << room.capacity - room.occupied << "\n";
    }
}
```

1. **Your own type,** because the code, the capacity and the number of occupied seats describe one room. The fields have names, and the record can later be passed as a whole, as in Module 8.
2. **Local variables first,** because `>>` needs a place to store the value it reads, and we create the record once, with all the values. The starting values mean that no variable has an indeterminate value, even after a failed read.
3. **The record isn't created straight away.** You could read directly into the fields of an existing record, but then after an error there would be a room with some fields from the data and some from the starting values. A record created at the end is always complete.
4. **`>>`, not `getline`,** because each value is one word or one number. `>>` skips whitespace before a value and stops at the first whitespace after it. `std::getline` reads a whole line, with spaces.
5. **A code without spaces,** because `>>` reads one word into a `std::string`. A code with a space would split into two values.
6. **What `std::cin.fail()` detects:** that some value couldn't be read, because the data had a word instead of a number, or the data ended.
7. **What `std::cin.fail()` doesn't detect:** values that were read correctly but break the rules (0, negative numbers, more occupied seats than seats in total), or extra text after the third value.
8. **The rules after checking the read,** because after a failed read the variables' values don't come from the data. For `R-11 12`, the number of occupied seats stays 0, so it looks valid. That's why checking the numbers alone isn't enough: only the stream's state says whether the read succeeded.
9. **A positive capacity,** because a room with no seats makes no sense in this agreement, and free seats calculated from a capacity of 0 would mean nothing.
10. **Non-negative occupied seats,** because the number of occupied seats can't be less than zero.
11. **Occupied seats no greater than the capacity,** because a room can't have more occupied seats than it has. Without this rule, the number of free seats would come out negative.
12. **No field for the free seats,** because that's a value calculated from two fields. A separate field could disagree with them.
13. **When the data are rejected, there's no room object.** The program prints only a message, so there's nothing to print partly or with wrong values.
14. **No loop,** because the agreement allows one attempt at reading. Asking again, from lessons 4.5 and 4.6, isn't needed here.
15. **When a number is missing,** as in `R-11 12`, reading the last value runs into the end of the data and fails. The program prints `Input error`.
16. **Deliberately outside the checks:** extra text after the third value (case Q), the code's characters, and numbers outside the range of `int`.

**Other valid solutions:** each rule can be checked in its own `else if`, with the same message. The fields can have other names and another order, as long as the values in `{}` stand in the same order as the fields. The number of free seats can be stored in a `const int` variable, calculated from the record's fields.

Each case in the list of check cases is a separate run of this program. The first three runs are the data in the mission, including case A. Then come cases B to Q, in the order of the list of check cases.

<!-- input: room -->
```text
R-01 10 0
```

<!-- output: room -->
```text
Room: R-01
Capacity: 10
Occupied: 0
Available: 10
```

<!-- input: room -->
```text
R-02 10 10
```

<!-- output: room -->
```text
Room: R-02
Capacity: 10
Occupied: 10
Available: 0
```

<!-- input: room -->
```text
R-03 1 0
```

<!-- output: room -->
```text
Room: R-03
Capacity: 1
Occupied: 0
Available: 1
```

<!-- input: room -->
```text
R-04 1 1
```

<!-- output: room -->
```text
Room: R-04
Capacity: 1
Occupied: 1
Available: 0
```

<!-- input: room -->
```text
R-05 0 0
```

<!-- output: room -->
```text
Invalid room
```

<!-- input: room -->
```text
R-06 -2 0
```

<!-- output: room -->
```text
Invalid room
```

<!-- input: room -->
```text
R-07 10 -1
```

<!-- output: room -->
```text
Invalid room
```

<!-- input: room -->
```text
R-08 8 9
```

<!-- output: room -->
```text
Invalid room
```

<!-- input: room -->
```text
R-09 twelve 3
```

<!-- output: room -->
```text
Input error
```

<!-- input: room -->
```text
R-10 12 eight
```

<!-- output: room -->
```text
Input error
```

<!-- input: room -->
```text
R-11 12
```

<!-- output: room -->
```text
Input error
```

<!-- input: room -->
```text
R-13
```

<!-- output: room -->
```text
Input error
```

Case N is an empty line, followed by the end of the data:

<!-- input: room -->
```text
```

<!-- output: room -->
```text
Input error
```

<!-- input: room -->
```text
LAB-2
30
25
```

<!-- output: room -->
```text
Room: LAB-2
Capacity: 30
Occupied: 25
Available: 5
```

<!-- input: room -->
```text
Aula-3   20   5
```

<!-- output: room -->
```text
Room: Aula-3
Capacity: 20
Occupied: 5
Available: 15
```

<!-- input: room -->
```text
R-14 6 2 extra
```

<!-- output: room -->
```text
Room: R-14
Capacity: 6
Occupied: 2
Available: 4
```

</details>

<details>
<summary>Section 7: the results before the fix, and the fixed program</summary>

Before the fix, for the valid data `BX-7 5`:

<!-- output: parcel_order_bug -->
```text
Parcel: BX-7
Weight: 5
```

- **For valid data, the order of the checks doesn't matter.** The read succeeds and the weight is positive, so both programs reach the last branch.
- **Data that reveal the bug:** data for which reading the weight fails, for example a word instead of a number. The correct result is `Input error`, but the program with the bug prints:

<!-- input: parcel_order_bug -->
```text
BX-7 five
```

<!-- output: parcel_order_bug -->
```text
Invalid parcel
```

A missing weight gives the same wrong result:

<!-- input: parcel_order_bug -->
```text
BX-7
```

<!-- output: parcel_order_bug -->
```text
Invalid parcel
```

- **The cause:** the program checks `weight <= 0` before it checks the read. After a failed read, `weight` holds 0: with a word instead of a number, the failed read stores it, and at the end of the data the starting value stays. That number doesn't come from the data, but the program judges it as a weight, so it calls the lack of a valid number a weight that isn't allowed.
- **`>>` worked correctly:** it reported the failed read through `fail()`. The bug is in the order of the checks in our program.
- **Data that don't reveal the bug:** a valid weight, 0 and negative numbers, because both programs print the same for them. Also `BX-7 5kg`, because `>>` reads the number 5 from it.
- **The fix:** swap the order of the checks, `std::cin.fail()` first, then `weight <= 0`. No new C++ construct is needed: the same `if`, `else if`, `else` and the same two conditions stay, only in a different order. The fixed program is the program in section 2:

<!-- example: parcel_order_fixed -->
```cpp
#include <iostream>
#include <string>

struct Parcel {
    std::string id;
    int weight;
};

int main() {
    std::string id{};
    int weight{0};

    std::cin >> id;
    std::cin >> weight;

    if (std::cin.fail()) {
        std::cout << "Input error\n";
    } else if (weight <= 0) {
        std::cout << "Invalid parcel\n";
    } else {
        const Parcel parcel{id, weight};

        std::cout << "Parcel: " << parcel.id << "\n";
        std::cout << "Weight: " << parcel.weight << "\n";
    }
}
```

<!-- input: parcel_order_fixed -->
```text
BX-7 five
```

<!-- output: parcel_order_fixed -->
```text
Input error
```

</details>

**Previous lesson:** [Lesson 9.5: A delivery drone fleet (the Module 9 test)](../module_09_mutable_references/lesson_05_drone_fleet.en.md) · **Next lesson:** [Lesson 10.2: Names with spaces: `>>` and `std::getline`](lesson_02_names_with_spaces.en.md) · [Course overview](../../README.en.md)

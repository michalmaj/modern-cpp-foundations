# Lesson 10.4: A record-reading function and the ending of the data

[Polski](lesson_04_reading_function_and_end_of_data.md) · **English** · [Course overview](../../README.en.md)

> **Module 10, lesson 4** · about 90–110 minutes, can be split into two sessions
> **You need:** your `cpp-workspace` folder and the original `lesson_05_first_program` project, as before. You won't need the debugger in this lesson.
> **Pilot version.** The programs in this lesson are checked automatically on Windows, Ubuntu and macOS, including with the given input data. Typing input in CLion's **Run** window is described without a manual check on every system.

## Before you start

This lesson assumes that you:

- remember that a read can succeed and reach the end of the data at the same time, and that after a failed read the following reads fail too, until the stream is restored with `clear()` (lesson 4.6);
- tell an empty line from a failed read, and end a `while` loop when a read fails or the line is empty (lesson 7.4);
- pass an existing record to a function through `T&`, and a `bool` function checks the conditions first and changes nothing in it on a refusal (lessons 9.1 and 9.2);
- read a name with `std::getline`, numbers with `>>`, and finish the number line with `std::getline(std::cin, rest)` (lesson 10.2);
- add only complete, checked records to a vector with `push_back`, and at the first error end `main` with `return 0;`, with no partial report (lesson 10.3).

## The situation

In lesson 10.3 the first line of the data announced the number of shipments, and all the reading was in `main`. Often, though, nobody counts the records in advance: the data simply end. The program then reads one record after another, until it meets an empty line or the end of the data where the next name would be. Along the way it tells three situations apart:

1. **a valid record:** a non-empty name and valid numbers, so the record goes into the vector;
2. **the ending of the data:** an empty line or the end of the data where a name would be, so the program prints the report;
3. **a record error:** the name is there, but the numbers can't be read or break the rules, so the program prints only a message.

Reading the numbers of one record moves into a separate function, which gets the input stream and the record to fill through references. The main rule of this lesson: **the function changes the result record only once all its numbers have been read and follow the rules.**

After this lesson you will:

- pass `std::cin` to a function through a `std::istream&` parameter;
- write a `bool` function that fills an existing record through `T&`, and leaves it unchanged on a refusal;
- read records up to an empty line or to the end of the data, and tell the ending of the data from an incomplete record;
- after a refusal, tell a failed read from a value that isn't allowed;
- choose data that reveal a result assigned too early.

## 1. Prepare the project

In `cpp-workspace`, create a folder `lesson_10_4` and copy `main.cpp` and `CMakeLists.txt` from the original `lesson_05_first_program` into it. You type the program of section 2 into `main.cpp` in that folder.

The programs in this lesson print no questions. Type the data line by line, as in lesson 10.3, and after the last record press **Enter** once more: an empty line ends the data. You don't have to cause the end of the data yourself.

## 2. A list of shipments with no announced count

Each shipment takes two lines, as in lesson 10.3: the full name of the destination and the number of boxes, which can't be negative. Nobody announces the number of shipments. Data that follow the agreement contain at most 5 of them.

<!-- example: shipment_reader -->
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

Run the program, type the data, and finish with an empty line:

<!-- input: shipment_reader -->
```text
North Hub
4
South Depot
7

```

<!-- output: shipment_reader -->
```text
Shipments: 2
North Hub: 4
South Depot: 7
Total boxes: 11
```

| Code | What it does |
|---|---|
| `bool read_shipment_values(...)` | reads and checks the number of boxes of one shipment, and on success fills the result record (section 3) |
| `result = Shipment{destination, boxes};` | gives the result record new values of both fields |
| `std::getline(std::cin, destination);` before the loop | reads the first name |
| `while (!std::cin.fail() && !destination.empty())` | repeats the passes while reading the name succeeded and the name isn't empty (section 5) |
| `Shipment shipment{"", 0};` | prepares the record that the function is to fill |
| `if (!accepted)` | after a refusal chooses the message and ends `main` (section 6) |
| `std::getline(std::cin, rest);` | after an accepted record finishes its number line |

- **`main` reads the names and decides about the ending of the data.** The function gets only a name that was read successfully and isn't empty.
- **The function reads and checks the number** of one record, and reports success with its `bool` result. It prints nothing.
- **An empty line is no longer a record error.** In lesson 10.3 an empty name gave `Invalid shipments`, because the program was waiting for an announced record. Here an empty line where a name would be means the ending of the data.

## 3. The function fills an existing record

The header of the function of section 2:

<!-- fragment -->
```cpp
bool read_shipment_values(std::istream& input, const std::string& destination, Shipment& result)
```

- **`std::istream& input`:** `std::cin` is an existing object of type `std::istream`, that is, an input stream, available after `#include <iostream>`. A parameter with `&` is another name for the object passed (lesson 9.1), so `input >> boxes` reads from the same `std::cin`, from where `main` stopped. The function opens no new input. There's no `const`, because reading changes the stream: it takes characters out of it and can change its state.
- **`const std::string& destination`:** `main` has already read the name, and the function only uses it, so it gets it through `const&`, like the text in lesson 7.3.
- **`Shipment& result`:** the function fills an object prepared by `main`, instead of creating a new record and returning it by value, as in lesson 8.5. That agreement is good when there's one result. Here there are two: whether the read succeeded, and the complete record. `bool` tells about success, and the record goes into the caller's object.

**`std::getline` works the same way.** Lesson 5.2 said that library functions don't always receive their data the way an `int` parameter does. `std::getline(std::cin, line)` gets the stream and the text through references without `const`: it reads from the stream and changes `line`. Our function has the same shape.

The function takes its steps in this order:

1. prepare the local variable `boxes` with a starting value;
2. read the number with `>>`;
3. check `input.fail()`;
4. check the rules;
5. assign the complete record to `result`;
6. return `true`.

Every refusal is a `return false;` before step 5, so **after `false` the record `result` is unchanged**, and it must not be taken for a newly read record. That's the "all or nothing" rule of lesson 9.2: no changes to the fields during the checks, and no restoring. After `false` the program of section 2 stops anyway, but another caller may go on using its record, so the agreement always holds (section 8).

**Assigning a whole record.** `Shipment{destination, boxes}` is the value of a whole record: the type name and braces, as when a record is created, but without the object's name. `result = ...;` assigns it to an existing object, so both fields get new values at once, like the variable in `second = first;` in lesson 2.2. Lesson 8.2 mentioned this kind of assignment. No second result record and no vector element are created: `result` is still `shipment` from `main`, and only `push_back` adds the element.

## 4. Who recognises the ending of the data

| Situation | What the data have where a record would be | Who recognises it | What next |
|---|---|---|---|
| a valid record | a non-empty name, followed by a valid number | `main` reads the name, and the function the number and returns `true` | `push_back` and the next name |
| the ending of the data | an empty line or the end of the data | `main`, right after reading the name | the report |
| a record error | a non-empty name, followed by a word, a number not allowed or the end of the data | the function, which returns `false` | a message and the end of the program |

**Why does `main` read the name?** Because it's at the name that it's decided whether the data have ended. If the function read the name too, its result would have to express the three situations of the table, and `bool` has only two values. When `main` reads the name, the function is called only once a record has started. Its `true` then means "a complete, valid record is in `result`", and `false` means "there's no new record".

**An incomplete record is not the ending of the data.** When the data end right after a non-empty name, the record has already started, but its number is missing. The read in the function fails, and the program prints `Input error`, not the report.

## 5. The loop in `main` and the last number

The loop's condition joins two checks of lesson 7.4, in the same order: whether reading the name succeeded, and whether the name isn't empty. Thanks to short-circuit evaluation (lesson 3.4), `empty()` is checked only after a successful read. `main` reads the first name before the loop, and each next one at the end of a pass.

Trace the main data:

| Pass | `destination` | The function | `getline(rest)` finishes | The next name |
|---|---|---|---|---|
| 1 | `North Hub` | reads 4, returns `true` | the line with `4` | `South Depot` |
| 2 | `South Depot` | reads 7, returns `true` | the line with `7` | an empty line, the end of the loop |

**After an accepted record the program finishes its number line,** because another name may follow it. In lesson 10.3 there was no read after the last record, because the program knew the number of records. Here it learns that the record was the last only when it tries to read the next name.

**The last number at the very end of the data.** When the data end right after `7`, with no end of line, `>>` reads 7 correctly, although the stream has already reached the end of the data (lesson 4.6), and the function returns `true`. Only `getline(rest)` fails. That's not an error of the last record: its number has been read and checked, and the record is in the vector. That's why `main` reads the next name only after finishing the line successfully, and `fail()` in the condition ends the loop. If the program printed `Input error` after a failed `getline(rest)`, it would reject valid data.

| Where the data end | What fails | Result |
|---|---|---|
| right after a name, before its number | `>>` in the function | `Input error` |
| right after the last number, with no end of line | `getline(rest)` | the report |
| after the end of the line with the last number | reading the next name | the report |

The course's automatic tests check the first and the last row of this table. They don't run the middle one, because in them every line has its end.

<details>
<summary>The data of the table and their results</summary>

The data end right after the name of the second shipment:

<!-- input: shipment_reader -->
```text
North Hub
4
South Depot
```

<!-- output: shipment_reader -->
```text
Input error
```

The data end after the end of the line with `7`, with no empty line:

<!-- input: shipment_reader -->
```text
North Hub
4
South Depot
7
```

<!-- output: shipment_reader -->
```text
Shipments: 2
North Hub: 4
South Depot: 7
Total boxes: 11
```

</details>

## 6. A refusal: a failed read or a value not allowed

The function returns `false` in two situations: when reading the number failed, and when the number read is negative. That's why after a refusal `main` checks the state of the stream: after a failed read `std::cin.fail()` gives `true` and the program prints `Input error`, and otherwise `Invalid shipments`.

This works because the function doesn't call `clear()`, so the state after a failed read stays until `main` checks it (lesson 4.6). `false` says that there's no new record, and `fail()` says whether a read failed: they are two separate pieces of information. This convention belongs to this particular function, not to every `bool`.

**Predict** the results for three sets of data. Running them is optional.

The second shipment has `-2` boxes:

<!-- input: shipment_reader -->
```text
North Hub
4
South Depot
-2
```

<details>
<summary>The standard output when the second shipment has -2 boxes</summary>

<!-- output: shipment_reader -->
```text
Invalid shipments
```

</details>

A word stands instead of the number of boxes of the second shipment:

<!-- input: shipment_reader -->
```text
North Hub
4
South Depot
seven
```

<details>
<summary>The standard output when a word stands instead of the number</summary>

<!-- output: shipment_reader -->
```text
Input error
```

</details>

The data start with an empty line:

<!-- input: shipment_reader -->
```text

```

<details>
<summary>The standard output for an empty line</summary>

<!-- output: shipment_reader -->
```text
Shipments: 0
Total boxes: 0
```

</details>

- **An error in the second shipment:** the first is already in the vector, but the program prints only the message and stops, as in lesson 10.3.
- **An empty line at the start:** the loop doesn't run even once. An empty vector is a valid result, with no stand-in record. Input with no characters at all gives the same report, but the automatic tests don't run that case.

| Situation | Example | Result |
|---|---|---|
| a failed read of a number | `seven` instead of the number of boxes, the end of the data after a name | `Input error` |
| a successful read, a value not allowed | `-2` boxes | `Invalid shipments` |
| the ending of the data | an empty line or the end of the data where a name would be, also before the first shipment | the report |

<details>
<summary>Other data and their results</summary>

One shipment, followed by the end of the data:

<!-- input: shipment_reader -->
```text
East Gate
3
```

<!-- output: shipment_reader -->
```text
Shipments: 1
East Gate: 3
Total boxes: 3
```

Five shipments, followed by the end of the data:

<!-- input: shipment_reader -->
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

<!-- output: shipment_reader -->
```text
Shipments: 5
Central Hub: 2
North Hub: 4
River Port: 0
South Depot: 7
West End Depot: 1
Total boxes: 14
```

An empty line after the first shipment ends the data, even when more lines follow it. The program doesn't read them:

<!-- input: shipment_reader -->
```text
North Hub
4

South Depot
7
```

<!-- output: shipment_reader -->
```text
Shipments: 1
North Hub: 4
Total boxes: 4
```

</details>

## 7. Mission: team results

The program reads the results of the teams of a tournament one after another, until the data end, and prints all the teams and the total of the wins.

**Input data:** each team takes two lines:

1. the name of the team, which may contain spaces;
2. two numbers separated by a space: the number of matches played and the number of matches won.

Nobody announces the number of teams. After the last team there's an empty line, or the data end.

**Rules:**

- The name of a team isn't empty, because an empty line ends the data. In data that follow the agreement it has no spaces at its start or end. Two teams may have the same name.
- The number of matches played can't be negative, and the number won can't be negative or greater than the number played. 0 played and 0 won is allowed.
- There are at most 5 teams, and the numbers are small and fit in `int`, as does their total. Text after the numbers is outside the agreement, and the program doesn't check it.

**Requirements:**

- The program defines its own team type with three fields: the name (`std::string`), the number played (`int`) and the number won (`int`).
- A separate function reads and checks the numbers of one team. It gets the stream through `std::istream&`, the name through `const std::string&`, and an existing result record through a reference without `const`. It reads the numbers into local variables, and assigns the record only after checking the read and the rules. It returns `true` or `false`, and after `false` the result record stays unchanged. It prints nothing.
- `main` reads the names, recognises the ending of the data, and, only after `true`, adds the record with `push_back` to a vector that starts empty. The reading has no prompts.
- When a required number can't be read, the program prints exactly `Input error`, and when the numbers break the rules, exactly `Invalid teams`. In both cases it stops with no part of the report.
- After the ending of the data, the program prints the number of teams from `size()`, each team in the order of the data and the total of the wins, as in the example below, all from the elements of the vector.

In `cpp-workspace`, create a folder `team_results`, copy `CMakeLists.txt` from the original `lesson_05_first_program` into it, create an empty `main.cpp` and write the program on your own.

For data that end with an empty line:

<!-- input: teams -->
```text
Maple Owls
6 4
River Foxes
3 3

```

the standard output must be:

<!-- output: teams -->
```text
Teams: 2
Maple Owls: played 6, won 4
River Foxes: played 3, won 3
Wins total: 7
```

The same data with no empty line, ended by the end of the data, give the same result:

<!-- input: teams -->
```text
Maple Owls
6 4
River Foxes
3 3
```

<!-- output: teams -->
```text
Teams: 2
Maple Owls: played 6, won 4
River Foxes: played 3, won 3
Wins total: 7
```

A word stands instead of the number of wins of the second team. The first may already be in the vector, but there's no report:

<!-- input: teams -->
```text
Maple Owls
6 4
River Foxes
3 won
```

<!-- output: teams -->
```text
Input error
```

The second team has more wins than matches played:

<!-- input: teams -->
```text
Maple Owls
6 4
River Foxes
3 4
```

<!-- output: teams -->
```text
Invalid teams
```

The data start with an empty line:

<!-- input: teams -->
```text

```

<!-- output: teams -->
```text
Teams: 0
Wins total: 0
```

When a number is missing after a non-empty name, the result is `Input error`, not the ending of the data.

**This isn't the shipments with another name.** The number line has two numbers, and one of the rules joins them. You have to decide on your own:

1. how to name the type, its fields, the vector, the function and its parameters;
2. in which order the function reads the numbers and checks the read and the rules, and where it assigns the result record;
3. where `main` reads the next names, how it recognises the ending of the data, and when it finishes the number line;
4. where to call `push_back`, and how to tell `Input error` from `Invalid teams` after a refusal;
5. how to print the teams and compute the total of the wins from the elements of the vector;
6. which data would reveal that the function changes the result record before checking the rules.

**Before you write the program**, prepare a table of cases with the expected results: an empty line at the start, one, two and five teams, both ways of ending, a repeated name, a team with no matches, only wins and only losses, negative numbers, more wins than matches played, a word instead of each of the numbers, no numbers after a name, the last number missing, and an error in a team after a valid one.

**Then** run the program for the main data and for one of the two errors in the second team. The other cases of the full list of check cases are checked automatically, and analyse on paper the ones in which the data end with no empty line.

### Success criteria

- The program builds as C++20 and, for the main data and the chosen error in the second team, prints exactly the results shown.
- The function gets the stream, the name and the result record through references, and assigns the record only after checking the read and the rules.
- `main` stops reading after an empty line and after the end of the data where a name would be, and prints `Input error` for an incomplete team.
- `push_back` runs only after `true`, and on an error there's no part of the report.
- The number of teams comes from `size()`, and the lines and the total from the elements of the vector, read through a `const` reference.
- The table of cases was written before running the program.
- You can explain why both ways of ending the data give the same result.

When the result matches, you can save the project in Git, as in lesson 1.5.

<details>
<summary>Hint 1</summary>

Which task belongs to `main`, and which to the function that reads the numbers? Who recognises the end of the whole input?

</details>

<details>
<summary>Hint 2</summary>

The function should first read the numbers into local variables. What will happen to the result record if the read fails?

</details>

<details>
<summary>Hint 3</summary>

Only after the numbers have been read and checked successfully, assign the complete record to the `T&` parameter. In `main`, add it with `push_back` only when the function returns success.

</details>

<details>
<summary>The full list of check cases: open after preparing your own table</summary>

The lines of the data are separated by `/`. For valid data, the "Result" column gives the number of teams and the total of the wins. The program then prints all the teams in the order of the data.

| | Data | Result | What it checks |
|---|---|---|---|
| A | `Maple Owls` / `6 4` / `River Foxes` / `3 3` / an empty line | 2 teams, total 7 | the data of the requirements: names with spaces, ending by an empty line |
| B | `Maple Owls` / `6 4` / `River Foxes` / `3 3`, then the end of the data | 2 teams, total 7 | the end of the data after a complete team (the data of the requirements) |
| C | `Maple Owls` / `6 4` / `River Foxes` / `3 won` | `Input error` | a word instead of the second number, after a valid team (the data of the requirements) |
| D | `Maple Owls` / `6 4` / `River Foxes` / `3 4` | `Invalid teams` | more wins than matches played, after a valid team (the data of the requirements) |
| E | an empty line | 0 teams, total 0 | an empty vector (the data of the requirements) |
| F | `Lake Herons` / `5 2`, then the end of the data | 1 team, total 2 | one team |
| G | `Maple Owls` / `6 4` / `River Foxes` / `3 3` / `Hill Bears` / `0 0` / `Maple Owls` / `2 0` / `Sea Gulls` / `4 1` / an empty line | 5 teams, total 8 | the largest number of teams, the same name twice, a team with no matches, only wins and only losses |
| H | `Maple Owls` / `-1 0` | `Invalid teams` | a negative number played |
| I | `Maple Owls` / `6 -1` | `Invalid teams` | a negative number won |
| J | `Maple Owls` / `4 5` | `Invalid teams` | more wins than matches played in the first team |
| K | `Maple Owls` / `six 4` | `Input error` | a word instead of the first number |
| L | `Maple Owls`, then the end of the data | `Input error` | no numbers after a non-empty name |
| M | `Maple Owls` / `6`, then the end of the data | `Input error` | the last number missing |
| N | `Maple Owls` / `6 4` / `River Foxes`, then the end of the data | `Input error` | the end of the data after the name of the second team: an incomplete record isn't the ending of the data |

**The automatic tests and your runs.** All the cases are checked automatically: the reference solution is run for each of them, and its whole standard output is compared with the expected one. The solution and its results are in [Example solutions](#example-solutions).

</details>

An example solution is in [Example solutions](#example-solutions).

## 8. Find the bug: a result assigned too early

Do this task **after the mission**. The program below checks the function `read_shipment_values` for one shipment. It prepares the record `result` with the values `Old Place` and 9, reads a name, calls the function, and then prints its result and the state of `result`. The function should work exactly as in section 2. You can copy the program into `main.cpp` in the `lesson_10_4` folder. Type a name, and a number on the next line.

<details>
<summary>The program to check: open after writing your own program</summary>

<!-- example: shipment_values_early_bug -->
```cpp
#include <iostream>
#include <string>

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

    result = Shipment{destination, boxes};

    if (boxes < 0) {
        return false;
    }

    return true;
}

int main() {
    Shipment result{"Old Place", 9};
    std::string destination{};
    std::getline(std::cin, destination);

    const bool accepted{read_shipment_values(std::cin, destination, result)};

    if (accepted) {
        std::cout << "Returned: true\n";
    } else {
        std::cout << "Returned: false\n";
    }

    std::cout << "Result: " << result.destination << ", " << result.boxes << "\n";
}
```

Data with a positive number of boxes:

<!-- input: shipment_values_early_bug -->
```text
North Hub
4
```

1. **Predict** what this program prints for these data, and what it would print with the function of section 2.
2. Run the program for these data and compare the result with your prediction.
3. Choose your own data for which the function of this program breaks its agreement.
4. For your data, **predict** what the function returns and which values `result` has afterwards.
5. Run the program for your data.
6. Point to the line where the function changes `result` too early. Why doesn't the `return false;` after that line bring back `Old Place` and 9?
7. Move the assignment after both checks and run the fixed program for your data.
8. Does a word instead of the number of boxes reveal this bug? Why wouldn't this bug change any result in the program of section 2?

</details>

The results, example data and the fixed program are in [Example solutions](#example-solutions).

## 9. When something goes differently

| What you see | What it means | What to do |
|---|---|---|
| The report has only the first record, although several were typed | `getline(rest)` is missing after an accepted record. Reading the next name gets the empty rest of the number line, and an empty name ends the data. | After `push_back`, finish the line with `std::getline(std::cin, rest)`, and only then read the next name. |
| The report has empty names and zeros | The result record's parameter has no `&`, so the function fills its own copy, and the object in `main` stays as it was prepared (lesson 9.1). | Pass the result record through a reference without `const`. |
| `Invalid teams` instead of `Input error` for a word in place of a number | After `false` the program always prints the same message, instead of checking the state of the stream. | After `false`, check `std::cin.fail()`: `true` means `Input error`. |
| The program waits, although all the records have been typed | The program waits for the next name, because only an empty line ends the data. If it waits right after a name, `>>` skips empty lines and waits for a number (lesson 10.1). | After the last record, press **Enter** on an empty line. After a name, type its numbers. |
| The compiler reports `call to deleted constructor of 'std::istream'` | The stream parameter has no `&`. A stream can't be passed by value, and the function is meant to work on the existing `std::cin`. | Write the parameter as `std::istream&`. |
| The compiler reports `invalid operands to binary expression ('const std::istream' ...` at `>>` | The stream parameter has `const`, but reading changes the stream. | Remove `const` from the stream parameter. |
| The function returns `false`, but the result record has new values | The function assigns the record before checking the rules (section 8). | Assign the record only after all the checks. |

## 10. Explain

Answer in your own words, preferably in writing. Only then compare with the example answers.

1. What does the function get through the parameter `std::istream& input` when `main` passes `std::cin`? Does the function open a new input?
2. Why does the result record go into the function through a reference without `const`, instead of being returned by value, as in lesson 8.5?
3. What do `true` and `false` of the function `read_shipment_values` mean? What is the state of `result` after `false`?
4. Why does the function read the number into a local variable and assign the whole record only at the end?
5. Why does `main`, and not the function, read the name and recognise the ending of the data?
6. What does the program do when the first line is empty? Why isn't that an error?
7. The data end right after the name of the second shipment. Why is the result `Input error`, and not a report with one shipment?
8. The data end right after the last number, with no end of line. Why does `getline(rest)` fail, and why does the program print the report anyway?
9. The function returned `false`. How does `main` know whether to print `Input error` or `Invalid shipments`?
10. The first team is valid, and the second has `3 4`. What's in the vector, and what does the program print? Why is `push_back` in `main`, and not in the function?

<details>
<summary>Example answers</summary>

1. It gets another name for the existing object `std::cin`, the input stream of type `std::istream`. It opens no new input: `input >> boxes` goes on reading the same data, from where `main` stopped.
2. Because the function has two things to pass on: whether the read succeeded, and the complete record. `bool` tells about success, and the record goes into the object the caller prepared. Returning a new record by value (lesson 8.5) is good when there's one result.
3. `true`: the number was read and checked, and `result` holds a complete, valid record. `false`: there's no new record, and `result` is exactly as before the call.
4. Because while reading, it isn't known yet whether the record will be valid. If the function changed `result` before the checks, a record that isn't allowed would stay in it after a refusal, and `return false;` doesn't undo that.
5. Because it's at the name that it's decided whether the data have ended. If the function read the name too, its `bool` would have to express three situations: a record, the ending of the data and an error. When `main` recognises the ending, `true` and `false` have one meaning each.
6. Reading the name succeeds, but the name is empty, so the loop doesn't run even once, and the program prints a report with zero shipments. An empty line where a name would be is the agreed ending of the data, and an empty vector is a valid result.
7. Because the record has already started: the name isn't empty, but its number is missing. The read in the function fails, so it's an incomplete record, not the ending of the data. A report with one shipment would suggest that the data were complete.
8. `>>` read 7 and reached the end of the data, so `getline(rest)` has nothing left to read. The number of the last record, though, has been read and checked, and the record is in the vector. A failed `getline(rest)` only means that there's no next name, so the loop ends normally.
9. It checks `std::cin.fail()`. The function doesn't restore the stream with `clear()`, so after a failed read `fail()` still gives `true`, and after a number that was read but isn't allowed it gives `false`.
10. The vector holds the first team, because it was added before the program read the second. The program prints only `Invalid teams`, with no report. `push_back` is in `main` because `main` builds the vector and decides what it holds, while the function only prepares one record.

</details>

## Summary

- When the number of records isn't announced, the program reads them up to an empty line or to the end of the data where a name would be. An empty vector is a valid result.
- `main` reads the names, recognises the ending of the data, adds the records with `push_back` and prints the report.
- The function gets the stream through `std::istream&`, the name through `const std::string&` and the result record through `T&`. It assigns the whole record only after checking the read and the rules, so after `false` the record is unchanged.
- After a refusal, `std::cin.fail()` tells a failed read from a value that isn't allowed.
- The end of the data after a non-empty name is `Input error`, while the end of the data right after the last valid number isn't an error.
- After an accepted record, the program finishes its number line, and only then reads the next name.

## What's next

In lesson 10.5, the Module 10 test, you'll bring together on your own what this module has taught you. Lesson 10.5 is in preparation.

---

## Example solutions

Look here **after your own attempt**. Your names may differ, as long as the standard output is as required.

<details>
<summary>Section 7: the mission, team results</summary>

<!-- example: teams -->
```cpp
#include <iostream>
#include <string>
#include <vector>

struct Team {
    std::string name;
    int played;
    int won;
};

bool read_team_values(std::istream& input, const std::string& name, Team& result) {
    int played{0};
    int won{0};
    input >> played;
    input >> won;

    if (input.fail()) {
        return false;
    }

    if (played < 0 || won < 0 || won > played) {
        return false;
    }

    result = Team{name, played, won};
    return true;
}

int main() {
    std::vector<Team> teams{};
    std::string name{};
    std::getline(std::cin, name);

    while (!std::cin.fail() && !name.empty()) {
        Team team{"", 0, 0};
        const bool accepted{read_team_values(std::cin, name, team)};

        if (!accepted) {
            if (std::cin.fail()) {
                std::cout << "Input error\n";
            } else {
                std::cout << "Invalid teams\n";
            }

            return 0;
        }

        teams.push_back(team);

        std::string rest{};
        std::getline(std::cin, rest);

        if (!std::cin.fail()) {
            std::getline(std::cin, name);
        }
    }

    int wins_total{0};
    std::cout << "Teams: " << teams.size() << "\n";

    for (const Team& team : teams) {
        std::cout << team.name << ": played " << team.played << ", won " << team.won << "\n";
        wins_total += team.won;
    }

    std::cout << "Wins total: " << wins_total << "\n";
}
```

1. **`main` reads the name,** because it's at the name that it's decided whether the data have ended. The function gets a name that has already been read.
2. **`main` recognises the ending of the data:** an empty line and a failed read of the name. The function is called only once a record has started.
3. **`std::istream&`,** because the function is to read from the existing stream `std::cin`, from where `main` stopped. Without `const`, because reading changes the stream.
4. **`Team&` as the result parameter,** because the function has two results: `bool` tells about success, and the record goes into the caller's object.
5. **The result record unchanged on `false`:** every refusal is a `return false;` before the assignment, so the caller gets its record back unchanged (lesson 9.2).
6. **The local variables `played` and `won`,** because while reading, it isn't known yet whether a valid record will come out. The fields of `result` wait for the end of the checks.
7. **The read before the values:** after a failed read the content of a variable can't be relied on (lesson 4.6), so the rules make sense only for numbers that were really read.
8. **The assignment after all the checks,** with one `result = Team{name, played, won};`, so the record changes all at once, and only when it's complete and valid.
9. **`push_back` in `main`,** because `main` builds the vector, and the function is responsible for one record. `main` adds the record only after `true`.
10. **The number of records isn't needed,** because the loop repeats the passes as long as a non-empty line, read successfully, stands where a name would be.
11. **An empty line ends the reading,** because it's a successful read of a text of length zero (lesson 7.4), and in the agreement on the data a team's name isn't empty.
12. **The end of the data before the next name ends the reading,** because all the earlier records are complete, and no new one has started.
13. **The end of the data inside a record is an error:** after a non-empty name the record has started, so a missing number is a failed read and `Input error`.
14. **The last number may end at the end of the data:** `>>` reads it correctly, although the stream has reached the end (lesson 4.6). Only `getline(rest)` fails.
15. **The last record is accepted,** because its numbers have been read and checked. A failed `getline(rest)` only means that there's no next name, so `main` doesn't read it and ends the loop.
16. **`false` and `fail()` are two pieces of information:** `false` says that there's no new record, and `std::cin.fail()` after `false` says whether a failed read was the cause. This works because the function doesn't call `clear()`.
17. **Earlier teams may stay in the vector** after an error in a later one. The program doesn't remove them, because it stops right away.
18. **Still, no partial report,** because the result is about all the data. A report of part of the teams would look complete.
19. **No new result type,** because `main` itself recognises the ending of the data. The two values of `bool` are enough for the function, and the state of the stream gives the reason for a refusal.
20. **No full check of the line,** because the agreement on the data says where the names and the numbers stand. `getline(rest)` finishes the number line, but doesn't check the text after the numbers (lesson 10.2).

**Other valid solutions:** instead of `return 0;` you can use a `bool` flag, as in lesson 7.4. The loop may also start each pass by reading the name, as in lesson 7.4: when `getline(rest)` fails, the next read of the name fails too (lesson 4.6), so the loop ends the same way. The function may assign the fields of `result` one by one instead of the whole record, as long as it does so only after all the checks. The function's result can also be checked directly in the `if` condition, without the variable `accepted`.

Each case of the list of check cases is a separate run of this program. Cases A–E are the data of the mission text. The others are below, in the order of the list of check cases.

<!-- input: teams -->
```text
Lake Herons
5 2
```

<!-- output: teams -->
```text
Teams: 1
Lake Herons: played 5, won 2
Wins total: 2
```

<!-- input: teams -->
```text
Maple Owls
6 4
River Foxes
3 3
Hill Bears
0 0
Maple Owls
2 0
Sea Gulls
4 1

```

<!-- output: teams -->
```text
Teams: 5
Maple Owls: played 6, won 4
River Foxes: played 3, won 3
Hill Bears: played 0, won 0
Maple Owls: played 2, won 0
Sea Gulls: played 4, won 1
Wins total: 8
```

<!-- input: teams -->
```text
Maple Owls
-1 0
```

<!-- output: teams -->
```text
Invalid teams
```

<!-- input: teams -->
```text
Maple Owls
6 -1
```

<!-- output: teams -->
```text
Invalid teams
```

<!-- input: teams -->
```text
Maple Owls
4 5
```

<!-- output: teams -->
```text
Invalid teams
```

<!-- input: teams -->
```text
Maple Owls
six 4
```

<!-- output: teams -->
```text
Input error
```

<!-- input: teams -->
```text
Maple Owls
```

<!-- output: teams -->
```text
Input error
```

<!-- input: teams -->
```text
Maple Owls
6
```

<!-- output: teams -->
```text
Input error
```

<!-- input: teams -->
```text
Maple Owls
6 4
River Foxes
```

<!-- output: teams -->
```text
Input error
```

**The check program** checks the function's agreement on a refusal, which can't be seen in the mission's report, because after `false` the program stops. The type and the function are the same as above. `main` prepares the record `Old Team` with the numbers 1 and 0, reads one name, calls the function and prints its result and the state of the record. It's a tool, not an extra task: running it is optional. You can swap in your own type and function, if you also change the names in `main`.

<!-- example: team_values_check -->
```cpp
#include <iostream>
#include <string>

struct Team {
    std::string name;
    int played;
    int won;
};

bool read_team_values(std::istream& input, const std::string& name, Team& result) {
    int played{0};
    int won{0};
    input >> played;
    input >> won;

    if (input.fail()) {
        return false;
    }

    if (played < 0 || won < 0 || won > played) {
        return false;
    }

    result = Team{name, played, won};
    return true;
}

int main() {
    Team result{"Old Team", 1, 0};
    std::string name{};
    std::getline(std::cin, name);

    const bool accepted{read_team_values(std::cin, name, result)};

    if (accepted) {
        std::cout << "Returned: true\n";
    } else {
        std::cout << "Returned: false\n";
    }

    std::cout << "Result: " << result.name << ", played " << result.played << ", won " << result.won << "\n";
}
```

Valid numbers, zeros included, change the record:

<!-- input: team_values_check -->
```text
River Foxes
3 3
```

<!-- output: team_values_check -->
```text
Returned: true
Result: River Foxes, played 3, won 3
```

<!-- input: team_values_check -->
```text
River Foxes
0 0
```

<!-- output: team_values_check -->
```text
Returned: true
Result: River Foxes, played 0, won 0
```

After a refusal the record stays unchanged. For `3 won` the first number has been read, and still the record doesn't change:

<!-- input: team_values_check -->
```text
River Foxes
3 won
```

<!-- output: team_values_check -->
```text
Returned: false
Result: Old Team, played 1, won 0
```

<!-- input: team_values_check -->
```text
River Foxes
3 4
```

<!-- output: team_values_check -->
```text
Returned: false
Result: Old Team, played 1, won 0
```

<!-- input: team_values_check -->
```text
River Foxes
-1 0
```

<!-- output: team_values_check -->
```text
Returned: false
Result: Old Team, played 1, won 0
```

<!-- input: team_values_check -->
```text
River Foxes
```

<!-- output: team_values_check -->
```text
Returned: false
Result: Old Team, played 1, won 0
```

</details>

<details>
<summary>Section 8: the results before the fix, and the fixed program</summary>

Before the fix, for the data with a positive number of boxes:

<!-- output: shipment_values_early_bug -->
```text
Returned: true
Result: North Hub, 4
```

- **This case masks the bug.** The function of section 2 would print the same: the number is read and allowed, so both versions assign the same record and return `true`.
- **Data that reveal the bug:** any negative number of boxes, for example `-2`. The read succeeds, and the rules should reject it. The correct result is `Returned: false` and `Result: Old Place, 9`, but the buggy program prints:

<!-- input: shipment_values_early_bug -->
```text
North Hub
-2
```

<!-- output: shipment_values_early_bug -->
```text
Returned: false
Result: North Hub, -2
```

- **Where the bug is:** `result = Shipment{destination, boxes};` stands between the check of the read and the check of the rules. For `-2` the assignment runs before the function knows that the number isn't allowed.
- **Why `return false;` doesn't bring back `Old Place` and 9:** `return` ends the call, but doesn't undo earlier changes (lesson 9.2). Nobody kept the old values, and `result` is another name for the object in `main`, so the change is already in it. The function returns `false`, while the record holds a shipment that isn't allowed.
- **A word instead of the number doesn't reveal the bug:** the function checks the read before the assignment, so for `seven` it returns `false` and changes nothing. Only a number that can be read but breaks the rules reveals the bug:

<!-- input: shipment_values_early_bug -->
```text
North Hub
seven
```

<!-- output: shipment_values_early_bug -->
```text
Returned: false
Result: Old Place, 9
```

- **In the program of section 2 this bug wouldn't change any result:** after `false` the program prints the message and stops, so nobody reads the changed record. The function would still break its agreement, and a program that goes on using the record after a refusal would get data that aren't allowed.
- **The fix:** move the assignment after both checks. The fixed function is the function of section 2:

<!-- example: shipment_values_early_fixed -->
```cpp
#include <iostream>
#include <string>

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
    Shipment result{"Old Place", 9};
    std::string destination{};
    std::getline(std::cin, destination);

    const bool accepted{read_shipment_values(std::cin, destination, result)};

    if (accepted) {
        std::cout << "Returned: true\n";
    } else {
        std::cout << "Returned: false\n";
    }

    std::cout << "Result: " << result.destination << ", " << result.boxes << "\n";
}
```

<!-- input: shipment_values_early_fixed -->
```text
North Hub
-2
```

<!-- output: shipment_values_early_fixed -->
```text
Returned: false
Result: Old Place, 9
```

For the data with a positive number of boxes and for the word, the fixed program prints the same as the buggy one:

<!-- input: shipment_values_early_fixed -->
```text
North Hub
4
```

<!-- output: shipment_values_early_fixed -->
```text
Returned: true
Result: North Hub, 4
```

<!-- input: shipment_values_early_fixed -->
```text
North Hub
seven
```

<!-- output: shipment_values_early_fixed -->
```text
Returned: false
Result: Old Place, 9
```

</details>

**Previous lesson:** [Lesson 10.3: Building a vector of records from input](lesson_03_building_a_vector_of_records.en.md) · **Next lesson:** in preparation · [Course overview](../../README.en.md)

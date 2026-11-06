# Lesson 12.3: Where the data end and where the error is

[Polski](lesson_03_end_of_data_and_errors.md) · **English** · [Course overview](../../README.en.md)

> **Module 12, lesson 3** · about 90–110 minutes, can be split into two sessions
> **You need:** your `cpp-workspace` folder and the original `lesson_05_first_program` project, as before. You won't need the debugger in this lesson.
> **Pilot version.** The programs in this lesson are checked automatically on Windows, Ubuntu and macOS, with the given data files. The steps in CLion (a new file, the **Working directory** field) are the same as in lesson 12.1: they are described according to the CLion 2026.3 documentation, without a manual check on every system.

## Before you start

This lesson assumes that you:

- read lines with `std::getline`, and know from lesson 7.4 that an empty line is a successful read with an empty text, while a failed read means that there was no line left;
- remember from lessons 4.6 and 7.4 that reading the last line can succeed although the stream has already reached the end of the data, so `fail()` decides whether a read succeeded;
- write a counter that starts at 0 and grows by 1 (lesson 4.2);
- pass an existing object to a function by a reference without `const`, so that the function can change it, also a vector (lessons 9.1 and 9.3);
- know the program of lesson 12.2, its data contract and case I, where an empty line between shipments ended the reading;
- open a file with `std::ifstream`, check opening with `fail()`, create a data file in a project and check the **Working directory** field (lesson 12.1).

## The situation

In a school biology room, someone records the state of the plants every day in a file, `watering.txt`: the plant's name, and on the next line `watered` if the plant has been watered, or `dry` if its soil is dry. The file is written by hand, so it has mistakes now and then: a stray empty line, a typo in a status, a missing last line.

The program must read the **whole** file and print a report. If the file contains an error, it prints no report, but the number of the line to correct, the same as the line number in an editor.

After this lesson you will:

- tell the end of a file from an empty line;
- read a file so that only the end of the file ends the data;
- number the physical lines of a file while reading, with one counter that grows after every successful `std::getline`;
- report an empty line, an invalid status and an incomplete record with a line number, without a partial report;
- read a last line without a line end correctly.

## 1. The starting point: data that disappear

In lesson 12.2, section 6, the shipments program got this file, `shipments.txt`:

```text
North Hub
4

South Depot
7
```

and printed:

```text
Shipments: 1
North Hub: 4
Total boxes: 4
```

There was no message, and `South Depot` didn't make it into the report. Answer on paper before you read on:

1. Had the file ended when the program stopped reading?
2. Were all the data read?
3. Why didn't the program report an error?
4. How would the program know that the empty line means the end of the data, and not a mistake in the file?
5. What should the program do if it has to process the whole file?

## 2. An empty line isn't the end of the file

The answers:

1. No. After the empty line there are two more lines, `South Depot` and `7`. The program stopped reading before the file ended.
2. No. The last shipment stayed in the file, unread.
3. Because lesson 12.2's contract said so: an empty line where a name would be ends the data. Reading the empty line succeeded, but the name was empty, so the loop condition `!input.fail() && !destination.empty()` ended the loop. For the program, this was an ordinary ending of the data.
4. It couldn't. An empty line on its own doesn't say whether someone meant to end the list or left a gap by accident. In lesson 12.2 the contract decided it, taken over from typing at the keyboard, where an empty line is typed on purpose.
5. Read until the end of the file, treat the empty line as a data error, and say where it is.

The program of lesson 12.2 wasn't wrong: it worked correctly for data that followed its contract. **In this lesson we change the contract: only the end of the file ends the list of records, and an empty line is a data error.**

**The end of the file and an empty line.** In the table, `\n` stands for the line end character, the same one a program prints with `"\n"`.

| File contents | Physical lines | Successive `std::getline` calls |
|---|---|---|
| nothing (an empty file) | 0 | a failed read at once |
| `\n` | 1, empty | an empty text, then a failed read |
| `Basil` | 1 | `Basil`, then a failed read |
| `Basil\n` | 1 | `Basil`, then a failed read |
| `Basil\nwatered\n` | 2 | `Basil`, `watered`, then a failed read |
| `Basil\nwatered\n\n` | 3, the third empty | `Basil`, `watered`, an empty text, then a failed read |

- **A line end ends a line; it doesn't start a new one.** `Basil\n` has one line, just like `Basil`. Only a second line end right after the first creates a new, empty line.
- **An empty line is a successful read:** `fail()` gives `false`, and the text is empty (lesson 7.4). **The end of the file is a failed read:** `std::getline` finds no line any more, and `fail()` gives `true`.
- **A last line without a line end (without a trailing newline) is a successful read too.** In the file `Basil\nwatered`, the second call delivers `watered` and reaches the end of the file: `eof()` already gives `true`, but `fail()` gives `false`. Only the third call fails. That's why the program doesn't ask, before reading, whether the file has ended. It tries to read a line first, and then checks `fail()`.
- **We treat a failed read as the end of the file.** That's what it is in an ordinary text file that has been opened. Rare failures, such as a disk error, also give a failed read, but recognising them is beyond this lesson.

**Why no numbers?** Before a number, `>>` skips whitespace, line ends included (lesson 2.6). If an empty line stood between a name and its number, `>>` would skip it without a trace: the program wouldn't notice the empty line, and would count the numbers of the following lines wrongly. To see every line, you have to read it whole with `std::getline`. A line holding a number would then have to be turned into a number, which we can't do yet. That's why both fields of a record are text in this lesson, and the program isn't a corrected version of the shipments program. We change the data format in order to improve the way the file is read and its structure is checked.

## 3. The new data contract

> **The contract of `watering.txt`.**
>
> - Each record takes exactly two physical lines: the plant's name and its status.
> - The name isn't empty, may contain spaces and may repeat. The program keeps it exactly, with all its characters.
> - The status is exactly `watered` or `dry`. The case of letters matters, and extra spaces aren't allowed, so `Watered`, `DRY` and `dry ` are invalid.
> - **Only the end of the file ends the data,** at the place where the next record would start.
> - Every empty line is an error: where a name is expected, where a status is expected, and at the end of the file.
> - The last line may have no line end.
> - The number of records isn't limited. In the examples there are from 0 to 5.
>
> An empty line is a line without any character. A line of spaces only isn't empty (lesson 7.4): as a name it is accepted, and as a status it is invalid.

| Situation | Standard output |
|---|---|
| the file couldn't be opened | `Cannot open watering.txt` |
| an empty line where a name or a status is expected | `Empty line N`, where N is the number of the empty line |
| a non-empty status other than `watered` and `dry` | `Invalid line N`, where N is the number of the status line |
| the file ends right after a name, with no status line | `Incomplete record on line N`, where N is the number of that name's line |
| the whole file is valid | `Plants: N`, each plant in the order of the file, for example `Basil: watered`, and `Watered total: T` |

- **N is always the number of a physical line of the file**, counted from 1, as in an editor. `T` is the number of plants with the status `watered`.
- The program reports the first error and ends with exit code 0, **without a partial report**. It prints the report only after reading the whole file. It doesn't sort the plants or remove repeats.
- **An incomplete record points to the last line that exists.** The status line isn't in the file, so the program can't give its number. It gives the number of the name's line, where the record started: that's the line after which the status must be added.
- **An empty status line isn't an incomplete record.** In the file `Basil\n\n` the second line exists, it's just empty: `Empty line 2`. In the file `Basil\n` there's no second line: `Incomplete record on line 1`.
- **The checks follow from the contract.** The program checks exactly what the contract calls an error, and nothing more: it doesn't trim spaces from names or fix the case of letters. Another contract would need other checks.

## 4. One `std::getline`, one physical line

**The numbering rule:** the line counter starts at 0 and grows by 1 **exactly after each successful `std::getline`**. A failed read delivers no line, so it doesn't change the counter. The end of the file isn't a line either. After a successful read, then, the counter is the number of the line just read, and a message can give it with no calculation at all.

The steps for a file whose second record has an invalid status:

```text
Basil
watered
Mint
soaked
```

| `std::getline` call | Text read | `fail()` | Counter after the call | Check |
|---|---|---|---|---|
| 1 (name) | `Basil` | `false` | 1 | non-empty name |
| 2 (status) | `watered` | `false` | 2 | allowed status, record accepted |
| 3 (name) | `Mint` | `false` | 3 | non-empty name |
| 4 (status) | `soaked` | `false` | 4 | status not allowed: `Invalid line 4` |

**A record number isn't a line number.** The error is in the second record, but on the fourth line. `Invalid line 2` would point to the line `watered`, which is correct. A message about "record 2" would leave you to work out which of two lines to correct, and someone correcting the file in an editor sees line numbers, not record numbers. That's why the program has a separate line counter, and knows the number of records from the size of the vector.

The steps for the file `Basil\n`, where the status is missing:

| `std::getline` call | Text read | `fail()` | Counter after the call | Check |
|---|---|---|---|---|
| 1 (name) | `Basil` | `false` | 1 | non-empty name |
| 2 (status) | nothing | `true` | 1 | no status: `Incomplete record on line 1` |

If the counter also grew after a failed read, the program would print `Incomplete record on line 2`, the number of a line that isn't in the file.

## 5. The demonstration program

In `cpp-workspace`, create a folder `lesson_12_3`, and copy `main.cpp` and `CMakeLists.txt` from the original `lesson_05_first_program` into it. Open the folder in CLion (**File | Open**, then **Trust Project** and the **Debug** profile). Next to `main.cpp`, create a file `watering.txt`, as with `steps.txt` in lesson 12.1, section 3, and check the **Working directory** field, as in section 4 of that lesson. Replace the contents of `main.cpp` with this program:

<!-- example: watering -->
```cpp
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

struct Plant {
    std::string name;
    std::string status;
};

bool read_plants(std::istream& input, std::vector<Plant>& plants, std::string& error, int& error_line) {
    int line_number{0};
    std::string name{};
    std::getline(input, name);

    while (!input.fail()) {
        ++line_number;

        if (name.empty()) {
            error = "empty";
            error_line = line_number;
            return false;
        }

        std::string status{};
        std::getline(input, status);

        if (input.fail()) {
            error = "incomplete";
            error_line = line_number;
            return false;
        }

        ++line_number;

        if (status.empty()) {
            error = "empty";
            error_line = line_number;
            return false;
        }

        if (status != "watered" && status != "dry") {
            error = "invalid";
            error_line = line_number;
            return false;
        }

        plants.push_back(Plant{name, status});
        std::getline(input, name);
    }

    return true;
}

int main() {
    std::ifstream input{"watering.txt"};

    if (input.fail()) {
        std::cout << "Cannot open watering.txt\n";
        return 0;
    }

    std::vector<Plant> plants{};
    std::string error{};
    int error_line{0};
    const bool complete{read_plants(input, plants, error, error_line)};

    if (!complete) {
        if (error == "empty") {
            std::cout << "Empty line " << error_line << "\n";
        } else if (error == "invalid") {
            std::cout << "Invalid line " << error_line << "\n";
        } else {
            std::cout << "Incomplete record on line " << error_line << "\n";
        }

        return 0;
    }

    int watered_total{0};
    std::cout << "Plants: " << plants.size() << "\n";

    for (const Plant& plant : plants) {
        std::cout << plant.name << ": " << plant.status << "\n";

        if (plant.status == "watered") {
            ++watered_total;
        }
    }

    std::cout << "Watered total: " << watered_total << "\n";
}
```

- **`read_plants` reads the whole file.** It gets the stream through `std::istream&`, like the function of lesson 12.2, a vector to fill, and two variables to describe an error. It returns `true` when the whole file is valid, and `false` at the first error. It prints nothing and doesn't know the file's name.
- **`std::string& error` and `int& error_line`** work like the `Product&` parameter of lesson 9.1, only for a text and a number: the function writes the kind of error and the line number into them, and after the return `main` reads them from its own variables. It also gets the vector by a reference without `const` (lesson 9.3) and adds records to it with `push_back`.
- **The name is read before the loop and at the end of its body**, as in lesson 10.4. The loop body runs only after a successful read of a name, so its first statement, `++line_number;`, counts that name's line.
- **The loop condition is just `!input.fail()`.** In lesson 12.2 it also had a non-empty-name condition, so an empty line ended the loop. Here only a failed read of a name ends the loop, that is, the end of the file. The first `if` in the loop checks for an empty name and reports an error.
- **The status:** a failed read of the status means that the file ended in the middle of a record. The counter hasn't grown, so it points to the name's line. After a successful read, the counter grows and points to the status line. The empty-line check comes first, then the allowed word, so an empty line never gives `Invalid line`.
- **The kind of error is a text: `"empty"`, `"invalid"` or `"incomplete"`.** The function only describes the error, and `main` chooses the full message, as after a refusal in lesson 12.2.
- **No partial report.** On an error, the vector may already hold earlier plants, but `main` prints only the message after `false`, and ends. The report is made only after `true`. The number of plants is `plants.size()`, and `watered_total` grows for every status `watered`.

Type data A into `watering.txt`:

<!-- run: watering -->

<!-- datafile: watering watering.txt -->
```text
Basil
watered
Mint
dry
Fern
watered
```

Build and run the program. This is the first required run.

<!-- output: watering -->
```text
Plants: 3
Basil: watered
Mint: dry
Fern: watered
Watered total: 2
```

## 6. Edge cases

Each case is different contents of `watering.txt`, or no file. You don't change the program or build it again.

**D: an empty line in the middle.** It's the file of section 1, only in the new format:

<!-- run: watering -->

<!-- datafile: watering watering.txt -->
```text
Basil
watered

Mint
dry
```

**Predict** the result, then run the program. This is the second required run.

<details>
<summary>Standard output for D</summary>

<!-- output: watering -->
```text
Empty line 3
```

The third `std::getline` reads the empty line. The read succeeded, the counter is 3, and the name is empty, so the function reports an error. The program doesn't print a report with one plant: the record `Mint` doesn't silently disappear.

</details>

**G: an incomplete record.** The file ends right after the first name:

<!-- run: watering -->

<!-- datafile: watering watering.txt -->
```text
Basil
```

**Predict** the result, then run the program. This is the third required run.

<details>
<summary>Standard output for G</summary>

<!-- output: watering -->
```text
Incomplete record on line 1
```

These are the second steps of section 4: reading the status fails, and the counter stays at 1.

</details>

Predict the other cases on paper before you open the collapsed block. Running them is optional.

**B: an empty file.** `watering.txt` exists, but there isn't a single character in it.

<!-- run: watering -->

<!-- datafile: watering watering.txt -->
```text
```

<details>
<summary>Standard output for B</summary>

<!-- output: watering -->
```text
Plants: 0
Watered total: 0
```

The first read of a name fails. That's the end of the file where a record would start, so a valid end of a list with no plants. An empty file contains no line, so it doesn't contain an empty line either.

</details>

**C: no file.** There's no `watering.txt` in the working directory.

<!-- run: watering -->

<details>
<summary>Standard output for C</summary>

<!-- output: watering -->
```text
Cannot open watering.txt
```

The program doesn't print `Plants: 0`, because it doesn't know what's in a file it hasn't opened.

</details>

**E: an empty status line.** After `Basil` there are two line ends, that is, `Basil\n\n`.

<!-- run: watering -->

<!-- datafile: watering watering.txt -->
```text
Basil

```

<details>
<summary>Standard output for E</summary>

<!-- output: watering -->
```text
Empty line 2
```

The second line exists, it's just empty. This isn't an incomplete record, as in G.

</details>

**F: an invalid status.**

<!-- run: watering -->

<!-- datafile: watering watering.txt -->
```text
Basil
soaked
```

<details>
<summary>Standard output for F</summary>

<!-- output: watering -->
```text
Invalid line 2
```

</details>

**H: the last status without a line end.** The file is exactly `Basil\nwatered`.

<!-- run: watering -->

<!-- datafile: watering watering.txt noeol -->
```text
Basil
watered
```

<details>
<summary>Standard output for H</summary>

<!-- output: watering -->
```text
Plants: 1
Basil: watered
Watered total: 1
```

`std::getline` delivers `watered` and reaches the end of the file, but `fail()` gives `false`, so the record is complete. The next read of a name fails: that's a valid end of the data. The same file with a line end after `watered` gives exactly the same report (case K below). A file without a line end at the end happens easily, when you don't press **Enter** after the last word. You don't have to prepare such a file.

</details>

**I: an empty line at the end.** The file is `Basil\nwatered\n\n`.

<!-- run: watering -->

<!-- datafile: watering watering.txt -->
```text
Basil
watered

```

<details>
<summary>Standard output for I</summary>

<!-- output: watering -->
```text
Empty line 3
```

The first line end after `watered` ends line 2. The second creates line 3, an empty one. In lesson 12.2 an empty line at the end ended the data (that lesson's case C). Here it's an error, because the contract has changed.

</details>

**J: an invalid status in the second record.** It's the file of the steps in section 4.

<!-- run: watering -->

<!-- datafile: watering watering.txt -->
```text
Basil
watered
Mint
soaked
```

<details>
<summary>Standard output for J</summary>

<!-- output: watering -->
```text
Invalid line 4
```

The first record was valid, but it isn't in a report: on an error there is no report at all.

</details>

Where the file can end, and what the program prints then:

| Where the file ends | Case | Result |
|---|---|---|
| before the first name: an empty file | B | a report with no plants |
| right after a name, with no status line | G | `Incomplete record on line 1` |
| right after a status, with no line end | H | a report |
| after the line end that follows a status | K | a report |
| after an empty line that follows a status | I | `Empty line 3` |

<details>
<summary>More control cases: open after your predictions</summary>

All these cases are checked automatically. The results follow from the contract of section 3.

**K: data H with a line end after `watered`.**

<!-- run: watering -->

<!-- datafile: watering watering.txt -->
```text
Basil
watered
```

<!-- output: watering -->
```text
Plants: 1
Basil: watered
Watered total: 1
```

**L: a single empty line.** The file holds just one line end.

<!-- run: watering -->

<!-- datafile: watering watering.txt -->
```text

```

<!-- output: watering -->
```text
Empty line 1
```

**M: a name only, without a line end.** The file is exactly `Basil`.

<!-- run: watering -->

<!-- datafile: watering watering.txt noeol -->
```text
Basil
```

<!-- output: watering -->
```text
Incomplete record on line 1
```

**N: an invalid status without a line end.**

<!-- run: watering -->

<!-- datafile: watering watering.txt noeol -->
```text
Basil
soaked
```

<!-- output: watering -->
```text
Invalid line 2
```

**O: a space after the status.** The second line holds `watered` and one space.

<!-- run: watering -->

<!-- datafile: watering watering.txt -->
```text
Basil
watered 
```

<!-- output: watering -->
```text
Invalid line 2
```

**P: the same name twice.** Each occurrence is a separate record.

<!-- run: watering -->

<!-- datafile: watering watering.txt -->
```text
Basil
watered
Basil
dry
```

<!-- output: watering -->
```text
Plants: 2
Basil: watered
Basil: dry
Watered total: 1
```

**Q: five records,** one of them with a space in its name.

<!-- run: watering -->

<!-- datafile: watering watering.txt -->
```text
Basil
watered
Mint
dry
Fern
watered
Peace Lily
watered
Aloe
dry
```

<!-- output: watering -->
```text
Plants: 5
Basil: watered
Mint: dry
Fern: watered
Peace Lily: watered
Aloe: dry
Watered total: 3
```

**R: an error after three valid records.** The status `Dry` is written with a capital letter.

<!-- run: watering -->

<!-- datafile: watering watering.txt -->
```text
Basil
watered
Mint
dry
Fern
watered
Rose
Dry
```

<!-- output: watering -->
```text
Invalid line 8
```

</details>

## 7. Diagnostic: the old rule on new data

**The situation.** Someone moved lesson 12.2's ending rule into the watering log: an empty line where a name would be ends the data. In the program of section 5, they changed only two places of the function `read_plants`:

| The program of section 5 | The program with the old rule |
|---|---|
| `while (!input.fail()) {` | `while (!input.fail() && !name.empty()) {` |
| at the start of the loop, `if (name.empty())` with the error `"empty"` | no such check |

<details>
<summary>The whole program with the old rule</summary>

<!-- example: watering_old_rule -->
```cpp
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

struct Plant {
    std::string name;
    std::string status;
};

bool read_plants(std::istream& input, std::vector<Plant>& plants, std::string& error, int& error_line) {
    int line_number{0};
    std::string name{};
    std::getline(input, name);

    while (!input.fail() && !name.empty()) {
        ++line_number;

        std::string status{};
        std::getline(input, status);

        if (input.fail()) {
            error = "incomplete";
            error_line = line_number;
            return false;
        }

        ++line_number;

        if (status.empty()) {
            error = "empty";
            error_line = line_number;
            return false;
        }

        if (status != "watered" && status != "dry") {
            error = "invalid";
            error_line = line_number;
            return false;
        }

        plants.push_back(Plant{name, status});
        std::getline(input, name);
    }

    return true;
}

int main() {
    std::ifstream input{"watering.txt"};

    if (input.fail()) {
        std::cout << "Cannot open watering.txt\n";
        return 0;
    }

    std::vector<Plant> plants{};
    std::string error{};
    int error_line{0};
    const bool complete{read_plants(input, plants, error, error_line)};

    if (!complete) {
        if (error == "empty") {
            std::cout << "Empty line " << error_line << "\n";
        } else if (error == "invalid") {
            std::cout << "Invalid line " << error_line << "\n";
        } else {
            std::cout << "Incomplete record on line " << error_line << "\n";
        }

        return 0;
    }

    int watered_total{0};
    std::cout << "Plants: " << plants.size() << "\n";

    for (const Plant& plant : plants) {
        std::cout << plant.name << ": " << plant.status << "\n";

        if (plant.status == "watered") {
            ++watered_total;
        }
    }

    std::cout << "Watered total: " << watered_total << "\n";
}
```

</details>

You don't need to type or run the program with the old rule: its results are checked automatically. Answer on paper:

1. **Predict** what the program with the old rule prints for data D of section 6.
2. Point to the condition that ends the reading. Why isn't the record `Mint` read?
3. Why isn't this the end of the file? What does `fail()` give after reading the empty line?
4. Compare your answer with the result of the second required run, the program of section 5 on the same data.
5. Where does the 3 in `Empty line 3` come from?
6. If the file was meant to hold two plants, which result is safer, and why?
7. Answer questions 1 and 6 for data I of section 6 too.

<details>
<summary>What happens: open after your answers</summary>

The results of the program with the old rule, checked automatically. Data D:

<!-- run: watering_old_rule -->

<!-- datafile: watering_old_rule watering.txt -->
```text
Basil
watered

Mint
dry
```

<!-- output: watering_old_rule -->
```text
Plants: 1
Basil: watered
Watered total: 1
```

Data I:

<!-- run: watering_old_rule -->

<!-- datafile: watering_old_rule watering.txt -->
```text
Basil
watered

```

<!-- output: watering_old_rule -->
```text
Plants: 1
Basil: watered
Watered total: 1
```

1. For D the program with the old rule prints a report with one plant, and no message.
2. The third `std::getline` reads the empty line. The read succeeded, so `!input.fail()` gives `true`, but `!name.empty()` gives `false`, and the loop ends. The function returns `true` as if the whole file were valid, and lines 4 and 5 stay unread.
3. Because line 3 exists: `fail()` gives `false`. The end of the file is a failed read, and here the read succeeded, only the text is empty.
4. The program of section 5 prints `Empty line 3` for the same bytes. Only a failed read ends its loop, and an empty name is an error.
5. From the counter: `Basil` is line 1, `watered` line 2, and the empty line is the third successful `std::getline`, so the counter is 3.
6. `Empty line 3` is safer. A report with one plant looks complete, and nothing warns that `Mint` has disappeared. The message gives no result that anyone could take for a full one, and it says which line to correct. When a file must be processed whole, a silent loss of data is more dangerous than an open error.
7. For I the old rule also prints a report with one plant, and the new program `Empty line 3`. By lesson 12.2's contract the report was correct, because an empty line at the end ended the data. The new contract is stricter: an empty line may not be left even at the end of the file.

The program of lesson 12.2 had no bug: it worked by its contract. The contract changed, so the ending rule had to change, and with it the loop condition.

</details>

## 8. Mission: a chore log

A school club records its chores and their state in a file. The program reads the file `chores.txt` and prints all the chores and the number of chores done.

**The contract of `chores.txt`:**

- each record takes exactly two physical lines: the chore's name and its status;
- the name isn't empty, may contain spaces and may repeat, and the program keeps it exactly;
- the status is exactly `done` or `pending`, with the case of letters mattering and no extra spaces;
- only the end of the file ends the data, at the place where the next record would start;
- every empty line is an error, and after a name there must be a line with a status;
- the last line may have no line end.

**The messages:**

| Situation | Standard output |
|---|---|
| the file couldn't be opened | `Cannot open chores.txt` |
| an empty line | `Empty line N` |
| a non-empty status other than `done` and `pending` | `Invalid line N` |
| the file ends right after a name | `Incomplete record on line N`, where N is the number of that name's line |
| the whole file is valid | `Tasks: N`, each chore in the order of the file, for example `Clean tables: done`, and `Done total: T` |

N is the number of a physical line of the file, and `T` is the number of chores with the status `done`. The program doesn't sort the chores or remove repeats. After an error it prints only one message, without a partial report, and ends with exit code 0.

**The requirements:**

- The program defines its own record type with two text fields, and collects the records in a vector.
- One function reads the whole file, and gets the stream through `std::istream&`. It reads every line with `std::getline`, without `>>`, counts the physical lines, and at the first error passes its kind and its line number to `main`. `fail()` after a read decides whether a line has been read. The function prints nothing, opens no file and doesn't use `std::cin`.
- `main` opens `chores.txt`, checks the opening, calls the function, and prints either one message or the full report.

In `cpp-workspace`, create a folder `chore_log`, copy `CMakeLists.txt` from the original `lesson_05_first_program` into it, and create an empty `main.cpp` and a file `chores.txt`. Leave `CMakeLists.txt` unchanged, and don't add `chores.txt` to `add_executable`. Open the folder in CLion and check **Working directory**, as in lesson 12.1, section 4. One `main.cpp` file is enough. Write the program yourself. You may look at the program of section 5.

```text
chore_log/
├── CMakeLists.txt
├── chores.txt
└── main.cpp
```

You decide on your own:

1. how to name the record type, its fields, the vector, the function and its parameters;
2. how the function passes the kind of error and the line number to `main`;
3. where the line counter starts and in which places it grows;
4. how the function recognises a valid end of the data;
5. how it recognises an incomplete record, and which number it gives then;
6. how it tells an empty line from no line;
7. in what order it checks for an empty line and for an allowed status;
8. how to prevent a partial report;
9. whether a last record without a line end needs code of its own;
10. which files will test an empty file, a missing file and an error in a later record.

**Cases A–J.** Each case is different contents of `chores.txt`, or no file.

**A: three chores.**

<!-- run: chores -->

<!-- datafile: chores chores.txt -->
```text
Clean tables
done
Sort books
pending
Water plants
done
```

<!-- output: chores -->
```text
Tasks: 3
Clean tables: done
Sort books: pending
Water plants: done
Done total: 2
```

**B: an empty file.**

<!-- run: chores -->

<!-- datafile: chores chores.txt -->
```text
```

<!-- output: chores -->
```text
Tasks: 0
Done total: 0
```

**C: no file.** There's no `chores.txt` in the working directory.

<!-- run: chores -->

<!-- output: chores -->
```text
Cannot open chores.txt
```

**D: an empty first line.** The file holds just one line end.

<!-- run: chores -->

<!-- datafile: chores chores.txt -->
```text

```

<!-- output: chores -->
```text
Empty line 1
```

**E: an empty status.** The file is `Clean tables\n\n`.

<!-- run: chores -->

<!-- datafile: chores chores.txt -->
```text
Clean tables

```

<!-- output: chores -->
```text
Empty line 2
```

**F: an invalid status of the second chore.**

<!-- run: chores -->

<!-- datafile: chores chores.txt -->
```text
Clean tables
done
Sort books
later
```

<!-- output: chores -->
```text
Invalid line 4
```

**G: no status for the second chore.**

<!-- run: chores -->

<!-- datafile: chores chores.txt -->
```text
Clean tables
done
Sort books
```

<!-- output: chores -->
```text
Incomplete record on line 3
```

**H: an empty line after a valid chore.** The file is `Clean tables\ndone\n\n`.

<!-- run: chores -->

<!-- datafile: chores chores.txt -->
```text
Clean tables
done

```

<!-- output: chores -->
```text
Empty line 3
```

**I: the last status without a line end.** The file is exactly `Clean tables\ndone`.

<!-- run: chores -->

<!-- datafile: chores chores.txt noeol -->
```text
Clean tables
done
```

<!-- output: chores -->
```text
Tasks: 1
Clean tables: done
Done total: 1
```

**J: the same name twice.**

<!-- run: chores -->

<!-- datafile: chores chores.txt -->
```text
Clean tables
done
Clean tables
pending
```

<!-- output: chores -->
```text
Tasks: 2
Clean tables: done
Clean tables: pending
Done total: 1
```

**Before you write the program**, trace cases A, D, G and H on paper, as in the tables of section 4: the `std::getline` call, the text read, `fail()`, the counter and the check.

**Then run the program for A.** This is the fourth required run. **Then for F**, changing only the contents of `chores.txt`. This is the fifth required run: the error is on a later line, so it checks the numbering. Trace the other cases on paper, line by line of your program. All of them are checked automatically in the reference solution.

### Success criteria

- The program builds as C++20 and prints exactly the shown results for A and for F.
- Your predictions for B–E and G–J match the results given above.
- The function gets the stream through `std::istream&`, reads every line with `std::getline`, and grows the counter only after a successful read.
- There's no `std::cin`, `std::cout`, `>>` or opening of a file in the function, and `eof()` doesn't control the loop.
- After an error the program prints no part of the report.
- `chores.txt` isn't in `add_executable`, `CMakeLists.txt` is the one of lesson 0.5, and **Working directory** points to the folder with `chores.txt`.
- You can explain why G gives the number 3 and not 4, and why H gives an error but I a report.

When the result matches, you can save the project in Git, as in lesson 1.5: `main.cpp`, `CMakeLists.txt` and `chores.txt` with data A, without the build folder.

<details>
<summary>Hint 1: the end of the file and an empty line</summary>

After each `std::getline` there are two different questions. Did the read succeed, that is, was there one more line in the file? `fail()` tells you that. Is the line that was read empty? `empty()` tells you that, but only after a successful read. Which result means a valid end of the data, and which an error, if it happens where a name is expected? And where a status is expected?

</details>

<details>
<summary>Hint 2: the numbering</summary>

The counter says how many lines have been read so far. Grow it after every successful `std::getline`, also after reading a status, not once per record. After a failed read, leave it unchanged: then it points to the last line that exists.

</details>

<details>
<summary>Hint 3: the report and the errors</summary>

A failed read of the status after a non-empty name is an incomplete record. Check the status in two steps: first whether the line is empty, then whether it's `done` or `pending`. Add the record to the vector only after both checks, and print the report in `main` only when the function has read the whole file without an error.

</details>

An example solution is in [Example solutions](#example-solutions).

## 9. When something goes differently

| What you see | What it means | What to do |
|---|---|---|
| `Incomplete record on line 2` instead of `line 1` | The counter also grows after a failed read, for example right after `std::getline`, before `fail()` is checked. | Grow the counter only when you know that the read succeeded. |
| `Invalid line 2` instead of `Invalid line 4` | The program counts records, not lines, or grows the counter once per record. | Grow the counter after every successful `std::getline`, also after reading a status. |
| An empty line gives a report instead of `Empty line N` | The loop condition still has `!name.empty()` from lesson 12.2 (section 7). | Only a failed read of a name ends the loop. Check for an empty name in the loop body. |
| An empty status gives `Invalid line N` instead of `Empty line N` | The check of the allowed word comes before the check for an empty line. | Check `empty()` first, then the allowed word. |
| The last record without a line end disappears or gives an error | The program checks `eof()` instead of whether the read succeeded. After a successful read of the last line, `eof()` may already give `true` (section 2). | `fail()` after a read decides whether a line has been read. |
| `Invalid line N`, although the status looks right | The line has a character you can't see: a space at the end, a capital letter, or, in a file from Windows read on Linux or macOS, a `\r` character before the line end. | Correct that line. Create a file from another system again in CLion, and retype the data. |
| Part of the report comes before the error message | The program prints records while reading. | Read the whole file first, and print the report only after `true`. |
| `Cannot open chores.txt`, although the file exists | The file isn't in the working directory, or has another name. | Follow the steps of lesson 12.1, section 7: the name, the case of letters, **Working directory**, where the file is. |

## 10. Explain

Answer in your own words, preferably in writing. Only then compare with the example answers.

1. Why doesn't an empty line mean the end of the file?
2. When does `std::getline` successfully read an empty line?
3. How does the program recognise the end of the data before a new record?
4. Why doesn't the line counter grow after a failed `std::getline`?
5. Why isn't a record number enough to point to an error?
6. How does `Empty line 2` differ from `Incomplete record on line 1`? Give a file for each of these messages.
7. Why can a last status without a line end be valid?
8. Why does `>>` make it hard to keep track of physical lines?
9. Why must a partial report not be printed on an error?
10. Why isn't the program of this lesson a reader of any text file yet?

<details>
<summary>Example answers</summary>

1. Because the empty line is in the file: `std::getline` reads it, `fail()` gives `false`, and more lines may follow it. The end of the file is the situation where there's no line left, so the read fails.
2. When the file has two line ends in a row, or starts with a line end. The read then takes just the line end: `fail()` gives `false`, and the text is empty.
3. By a failed read of a name: `fail()` gives `true` where the next record would start. Only that ends the data.
4. Because a failed read delivers no line. The counter should point to lines that really are in the file. If it grew after a failed read, an incomplete record would point to a line that doesn't exist.
5. Because a record takes two lines, and the person correcting the file sees line numbers in the editor. "Record 2" doesn't say whether the error is in the name or in the status. A line number points to exactly one place.
6. `Empty line 2`: the second line exists, but is empty, for example `Basil\n\n`. `Incomplete record on line 1`: there's no second line, the file ends after the name, for example `Basil\n` or `Basil`.
7. Because `std::getline` reads the characters up to the end of the file and gives `fail()` equal to `false`. A set `eof()` only means that the stream has reached the end of the file. Only the next read fails, where a name would be, and that's a valid end of the data.
8. Because before a value `>>` skips whitespace, line ends included. It can skip an empty line without a trace, and the program doesn't know how many lines it has passed. That's why we read every line whole with `std::getline`.
9. Because a partial report would look like a full one. Someone could use it, not knowing that part of the data wasn't checked or read. An error message says clearly: the file must be corrected.
10. Because it knows only one format: two lines per record and two fixed status words. It stops at the first error and reads no further, doesn't trim spaces, and doesn't turn text into numbers. It works correctly for data that follow its contract, and a file with another structure would need other checks.

</details>

## Summary

- The end of the file is a failed read: there's no line left. An empty line is a successful read with an empty text. In this lesson only the end of the file ends the data, and every empty line is an error.
- A line end ends a line; it doesn't start a new one. Only a second line end in a row creates an empty line. A last line without a line end is read as usual.
- `fail()` after a read decides whether a line has been read, not `eof()`.
- One counter, grown after every successful `std::getline`, gives the number of the physical line. A record number is something else.
- `Empty line N` points to an empty line, `Invalid line N` to a line with a status that isn't allowed, and `Incomplete record on line N` to the name's line after which the file ended.
- The reading function describes an error through references, and `main` chooses the message. The report is made only after the whole file has been read without an error.

## What's next

The next lesson is the Module 12 test. It's in preparation.

---

## Example solutions

Look here **after your own attempt**. Your names may differ, as long as the standard output is the required one.

<details>
<summary>Section 8: mission, a chore log</summary>

**`main.cpp`**:

<!-- example: chores -->
```cpp
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

struct Chore {
    std::string name;
    std::string status;
};

bool read_chores(std::istream& input, std::vector<Chore>& chores, std::string& error, int& error_line) {
    int line_number{0};
    std::string name{};
    std::getline(input, name);

    while (!input.fail()) {
        ++line_number;

        if (name.empty()) {
            error = "empty";
            error_line = line_number;
            return false;
        }

        std::string status{};
        std::getline(input, status);

        if (input.fail()) {
            error = "incomplete";
            error_line = line_number;
            return false;
        }

        ++line_number;

        if (status.empty()) {
            error = "empty";
            error_line = line_number;
            return false;
        }

        if (status != "done" && status != "pending") {
            error = "invalid";
            error_line = line_number;
            return false;
        }

        chores.push_back(Chore{name, status});
        std::getline(input, name);
    }

    return true;
}

int main() {
    std::ifstream chores_file{"chores.txt"};

    if (chores_file.fail()) {
        std::cout << "Cannot open chores.txt\n";
        return 0;
    }

    std::vector<Chore> chores{};
    std::string error{};
    int error_line{0};
    const bool complete{read_chores(chores_file, chores, error, error_line)};

    if (!complete) {
        if (error == "empty") {
            std::cout << "Empty line " << error_line << "\n";
        } else if (error == "invalid") {
            std::cout << "Invalid line " << error_line << "\n";
        } else {
            std::cout << "Incomplete record on line " << error_line << "\n";
        }

        return 0;
    }

    int done_total{0};
    std::cout << "Tasks: " << chores.size() << "\n";

    for (const Chore& chore : chores) {
        std::cout << chore.name << ": " << chore.status << "\n";

        if (chore.status == "done") {
            ++done_total;
        }
    }

    std::cout << "Done total: " << done_total << "\n";
}
```

**`CMakeLists.txt`**: the one of the original `lesson_05_first_program`, unchanged. `chores.txt` isn't in `add_executable`.

**`chores.txt`** with data A, in the folder `chore_log`, next to `main.cpp` and `CMakeLists.txt`:

<!-- run: chores -->

<!-- datafile: chores chores.txt -->
```text
Clean tables
done
Sort books
pending
Water plants
done
```

<!-- output: chores -->
```text
Tasks: 3
Clean tables: done
Sort books: pending
Water plants: done
Done total: 2
```

- **Running it:** the **Working directory** field of the `first_program` configuration points to the folder `chore_log`, the one with `chores.txt`. In the terminal you run the program from the folder `chore_log`.
- **The reading model:** `read_chores` reads a name, and in a loop that lasts while reading a name succeeds, it checks for an empty name, reads the status, checks that read, an empty line and the allowed word, adds the record, and reads the next name. A failed read of a name ends the loop and means a valid end of the data.
- **Returning an error:** the function returns `false` and writes the kind of error into `error` (`"empty"`, `"invalid"` or `"incomplete"`), and the line number into `error_line`. `main` turns the kind into a message.
- **The numbering:** `line_number` grows once after a successful read of a name, at the start of the loop, and once after a successful read of the status. After a failed read of the status it doesn't grow, so `Incomplete record` gives the name's line.
- **No line end at the end:** needs no code of its own. The last line is a successful read, and only the next, failed read of a name ends the loop.
- **No partial report:** `main` prints the report only after `true`. After `false` the vector may hold earlier chores, but nothing from it is printed.
- **Other correct solutions:** a loop with a `bool` flag that reads the name at the start of each pass, as in lesson 7.4; a separate small function that reads one line and grows the counter only after a successful read, called for the name and for the status. What matters is that the counter grows only after a successful read, and that the report is made only at the end.

| Case | The file `chores.txt` | Standard output |
|---|---|---|
| A | `Clean tables`, `done`, `Sort books`, `pending`, `Water plants`, `done` | 3 chores, `Done total: 2` |
| B | an empty file | `Tasks: 0`, `Done total: 0` |
| C | no file | `Cannot open chores.txt` |
| D | a single empty line | `Empty line 1` |
| E | `Clean tables`, an empty line | `Empty line 2` |
| F | `Clean tables`, `done`, `Sort books`, `later` | `Invalid line 4` |
| G | `Clean tables`, `done`, `Sort books` | `Incomplete record on line 3` |
| H | `Clean tables`, `done`, an empty line | `Empty line 3` |
| I | `Clean tables`, `done` without a line end | 1 chore, `Done total: 1` |
| J | `Clean tables`, `done`, `Clean tables`, `pending` | 2 chores, `Done total: 1` |

More control cases, checked automatically:

**K: one chore,** with the status `pending`.

<!-- run: chores -->

<!-- datafile: chores chores.txt -->
```text
Water plants
pending
```

<!-- output: chores -->
```text
Tasks: 1
Water plants: pending
Done total: 0
```

**L: five chores,** all of them done.

<!-- run: chores -->

<!-- datafile: chores chores.txt -->
```text
Clean tables
done
Sort books
done
Water plants
done
Fold laundry
done
Empty bins
done
```

<!-- output: chores -->
```text
Tasks: 5
Clean tables: done
Sort books: done
Water plants: done
Fold laundry: done
Empty bins: done
Done total: 5
```

**M: `Done` with a capital letter.**

<!-- run: chores -->

<!-- datafile: chores chores.txt -->
```text
Clean tables
Done
```

<!-- output: chores -->
```text
Invalid line 2
```

**N: a space after `done`.**

<!-- run: chores -->

<!-- datafile: chores chores.txt -->
```text
Clean tables
done 
```

<!-- output: chores -->
```text
Invalid line 2
```

**O: an incomplete first record.**

<!-- run: chores -->

<!-- datafile: chores chores.txt -->
```text
Clean tables
```

<!-- output: chores -->
```text
Incomplete record on line 1
```

**P: no status after three valid chores.**

<!-- run: chores -->

<!-- datafile: chores chores.txt -->
```text
Clean tables
done
Sort books
pending
Water plants
done
Fold laundry
```

<!-- output: chores -->
```text
Incomplete record on line 7
```

**Q: an empty line between chores.** More data follow it, but the result is the same as in H.

<!-- run: chores -->

<!-- datafile: chores chores.txt -->
```text
Clean tables
done

Sort books
pending
```

<!-- output: chores -->
```text
Empty line 3
```

**R: an invalid status without a line end.**

<!-- run: chores -->

<!-- datafile: chores chores.txt noeol -->
```text
Clean tables
later
```

<!-- output: chores -->
```text
Invalid line 2
```

</details>

**Previous lesson:** [Lesson 12.2: Records from a file: the same reading function](lesson_02_records_from_a_file.en.md) · **Next lesson:** the Module 12 test, in preparation · [Course overview](../../README.en.md)

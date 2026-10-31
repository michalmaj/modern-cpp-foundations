# Lesson 10.2: Names with spaces: `>>` and `std::getline`

[Polski](lesson_02_names_with_spaces.md) · **English** · [Course overview](../../README.en.md)

> **Module 10, lesson 2** · about 75–90 minutes
> **You need:** your `cpp-workspace` folder and the original `lesson_05_first_program` project, as before. You won't need the debugger in this lesson.
> **Pilot version.** The programs in this lesson are checked automatically on Windows, Ubuntu and macOS, including with the given input data. Typing input in CLion's **Run** window is described without a manual check on every system.

## Before you start

This lesson assumes that you:

- read a single word or a number with `std::cin >>`, and a whole line with spaces with `std::getline`, and remember that after `>>` the end of the line stays in the input (lesson 2.7);
- know that after a failed read the following reads fail too, and that the rest of a line can be read with `std::getline` into a helper variable (lesson 4.6);
- tell an empty line, which is a successful read of an empty text, from a failed read (lesson 7.4);
- define your own type with `struct` (lesson 8.1);
- read data into local variables, check the read and the rules, and only then create a record (lesson 10.1).

## The situation

In lesson 10.1 the parcel's identifier was a single word, because `>>` reads text only up to the first space. But names of places often have several words, for example `North Hub`. A whole line with spaces is read by `std::getline`, and numbers are still read by `>>`.

Lesson 2.7 advised: `getline` first, then `>>`. That's enough for one record. With two records, the first record's number is followed by the second record's name, so `getline` comes after `>>`, and then `getline` may read an empty text. Lesson 2.7 said you'd learn how to deal with this later. This lesson shows how.

That's why the programs in this lesson read **exactly two records**, each into its own variables. One record wouldn't reveal the problem, and many records in a vector are the topic of lesson 10.3.

After this lesson you will:

- read a full name with spaces with `std::getline`, and numbers with `>>`;
- explain what stays in the input after a number is read;
- finish a number line with `std::getline(std::cin, rest)` before you read the next name;
- tell a correctly read empty name from a failed read;
- create two records only after all the data have been checked;
- choose data that reveal a wrong order of reads.

## 1. Prepare the project

In `cpp-workspace`, create a folder `lesson_10_2` and copy `main.cpp` and `CMakeLists.txt` from the original `lesson_05_first_program` into it. You type the program from section 2 into this folder's `main.cpp`.

The programs in this lesson print no questions. Type the data line by line, as in the data block shown, and press **Enter** after each line. The program ends by itself after reading the last number. In the **Run** window the typed lines are mixed with the output, as in lesson 7.4.

## 2. Two shipments

The program reads the data of two shipments sent to different places. Each shipment takes two lines:

1. the full name of the destination, which may contain spaces;
2. the number of boxes.

The name can't be empty. The number of boxes must be non-negative, so 0 is allowed.

<!-- example: shipments -->
```cpp
#include <iostream>
#include <string>

struct Shipment {
    std::string destination;
    int boxes;
};

int main() {
    std::string first_destination{};
    int first_boxes{0};
    std::string rest{};
    std::string second_destination{};
    int second_boxes{0};

    std::getline(std::cin, first_destination);
    std::cin >> first_boxes;

    if (!std::cin.fail()) {
        std::getline(std::cin, rest);
        std::getline(std::cin, second_destination);
        std::cin >> second_boxes;
    }

    if (std::cin.fail()) {
        std::cout << "Input error\n";
    } else if (first_destination.empty() || first_boxes < 0 || second_destination.empty() || second_boxes < 0) {
        std::cout << "Invalid shipment\n";
    } else {
        const Shipment first{first_destination, first_boxes};
        const Shipment second{second_destination, second_boxes};

        std::cout << "Shipment 1: " << first.destination << ", boxes " << first.boxes << "\n";
        std::cout << "Shipment 2: " << second.destination << ", boxes " << second.boxes << "\n";
        std::cout << "Total boxes: " << first.boxes + second.boxes << "\n";
    }
}
```

Run the program and type:

<!-- input: shipments -->
```text
North Hub
4
South Depot
7
```

<!-- output: shipments -->
```text
Shipment 1: North Hub, boxes 4
Shipment 2: South Depot, boxes 7
Total boxes: 11
```

| Code | What it does |
|---|---|
| `std::getline(std::cin, first_destination);` | reads the whole first line, with its space: `North Hub` |
| `std::cin >> first_boxes;` | reads the number 4 |
| `if (!std::cin.fail())` | reads on only when the first shipment was read |
| `std::getline(std::cin, rest);` | finishes the line with the number 4 (section 3) |
| `std::getline(std::cin, second_destination);` | reads `South Depot` |
| `std::cin >> second_boxes;` | reads the number 7 |
| `const Shipment first{...}` and `second{...}` | create two records, only after all the checks |

- **Each shipment has its own variables and its own record,** with no vector and no loop.
- **The stream's state first, then the rules:** `std::cin.fail()` before `empty()` and `< 0`, as in lesson 10.1.
- **The total comes from the records' fields.**
- **One of three results:** the report, `Input error` or `Invalid shipment`. When the second shipment is wrong, the program doesn't print the first one either.

## 3. What stays in the input after a number

Follow what each operation reads and what comes next in the input right after it:

| After the operation | The variable gets | Next in the input |
|---|---|---|
| `std::getline(std::cin, first_destination)` | `North Hub` | `4` |
| `std::cin >> first_boxes` | 4 | **the end of the line after `4`** |
| `std::getline(std::cin, rest)` | an empty text | `South Depot` |
| `std::getline(std::cin, second_destination)` | `South Depot` | `7` |
| `std::cin >> second_boxes` | 7 | the end of the line after `7`, which the program no longer reads |

`getline` takes the end of the line from the input, but doesn't store it in the text (lesson 7.4). `>>` stops at the first whitespace after the number and **leaves it in the input**. So after `4`, what comes next is the end of the same line, not `South Depot`.

If the program called `std::getline(std::cin, second_destination)` right after `>> first_boxes`, it would read only that end of the line, which gives an empty text. `South Depot` would keep waiting in the input. That's the problem from lesson 2.7.

That's why there's an extra read between the number and the next name:

<!-- fragment -->
```cpp
std::cin >> first_boxes;
// Check the read.

std::getline(std::cin, rest);
// Check the read.

std::getline(std::cin, second_destination);
// Check the read.
```

`std::getline(std::cin, rest)` is the construct from lesson 4.6 in a new role:

- it reads what's left of the current line, here nothing;
- it also takes the end of the line from the input, but doesn't store it in `rest`;
- an empty `rest` is a **successful** read: it means neither an error nor the end of the data;
- it doesn't check which characters it read. It's not a check of the data, just a move to the next line.

Each of these three reads can fail, but the program in section 2 doesn't need a separate `if` after each. The check after the first number decides whether to read on. The check at the end covers the other reads: when one fails, the following ones fail too (lesson 4.6).

**We don't finish the line after the last number,** because the program reads no next name. An extra `getline` would even do harm. When the data end right after `7`, with no end of line, for example in a file, reading `7` succeeds, although the stream has reached the end of the data (lesson 4.6). The next `getline` would have nothing to read and would fail, so the program would print `Input error` for valid data. The course's automatic tests don't run this case, because in them every line has its end.

## 4. An empty name versus missing data

Lesson 7.4 told two situations apart:

- **an empty line** is a successful read of an empty text: `fail()` gives `false`, and `empty()` gives `true`;
- **a missing line** is a failed read: `fail()` gives `true`, and you can't rely on the variable's contents.

**Predict** the result for data in which the second name is an empty line. Running it is optional.

<!-- input: shipments -->
```text
North Hub
4

7
```

<details>
<summary>The standard output for an empty second name</summary>

<!-- output: shipments -->
```text
Invalid shipment
```

</details>

The empty line was read correctly, so the program checks the rules and rejects the empty name.

**Predict** the result too when the data end right after `4`. You can't cause this case by hand: **Enter** instead of the second name gives an empty name. Follow it on paper.

<!-- input: shipments -->
```text
North Hub
4
```

<details>
<summary>The standard output when the data end after 4</summary>

<!-- output: shipments -->
```text
Input error
```

</details>

`getline(rest)` takes the end of the line after `4`, but there's no second name any more. The next `getline` supplies no line and fails, so the program prints `Input error` and doesn't check the names. The order is fixed:

1. try to read the data;
2. check `std::cin.fail()`;
3. only after a successful read, check `empty()` and the rules for the numbers;
4. create the records only from accepted data.

| Situation | Example | Result |
|---|---|---|
| a failed read | `four` instead of the first number, `seven` instead of the second, no second shipment | `Input error` |
| a successful read, a value that isn't allowed | an empty first or second name, `-2` boxes | `Invalid shipment` |
| a successful read, allowed values | 0 boxes in the first shipment | the report of both shipments |

<details>
<summary>The other data in the table and their results</summary>

<!-- input: shipments -->
```text
North Hub
four
South Depot
7
```

<!-- output: shipments -->
```text
Input error
```

<!-- input: shipments -->
```text
North Hub
4
South Depot
seven
```

<!-- output: shipments -->
```text
Input error
```

<!-- input: shipments -->
```text

4
South Depot
7
```

<!-- output: shipments -->
```text
Invalid shipment
```

<!-- input: shipments -->
```text
North Hub
4
South Depot
-2
```

<!-- output: shipments -->
```text
Invalid shipment
```

<!-- input: shipments -->
```text
North Hub
0
South Depot
7
```

<!-- output: shipments -->
```text
Shipment 1: North Hub, boxes 0
Shipment 2: South Depot, boxes 7
Total boxes: 7
```

</details>

## 5. What the program doesn't check

We leave two things out on purpose.

**Text after a number.** **Predict** the result for data with an extra word after the first number:

<!-- input: shipments -->
```text
North Hub
4 extra
South Depot
7
```

<details>
<summary>The standard output for 4 extra</summary>

<!-- output: shipments -->
```text
Shipment 1: North Hub, boxes 4
Shipment 2: South Depot, boxes 7
Total boxes: 11
```

</details>

`rest` gets ` extra`, with a space at the start, and the program doesn't judge this text. Such data are outside the agreement, because a valid number line contains only the number. The program reports no error, but it doesn't confirm that the line was valid either. Text after the last number stays unread, as in lesson 10.1.

**Names that aren't empty but aren't valid.** `empty()` rejects only a text of length zero. A name made only of spaces isn't empty (lesson 7.4), so it passes this check. In data that follow the agreement a name has no spaces at the start or the end, and the program neither removes nor detects such spaces. So `empty()` says only that the name isn't empty, not that it's valid.

## 6. Mission: reading progress of two books

The program reads the data of two books and prints how many pages are left to read in both together.

**Input data:** each book takes two lines:

1. the title, which may contain spaces;
2. two numbers separated by a space: the number of all pages and the number of pages already read.

**Rules:**

- The title can't be empty. In data that follow the agreement it has no spaces at the start or the end, and the program doesn't check them.
- The number of pages must be greater than zero.
- The number of pages read must be non-negative and can't exceed the number of pages.
- All numbers are small and fit in `int`, and so does their total.
- Text after the numbers is outside the agreement, and the program doesn't check it.

**Requirements:**

- The program defines its own book type with three fields: the title (`std::string`), the number of pages (`int`) and the number of pages read (`int`). You choose the names of the type and the fields yourself.
- The reading is in `main`, into local variables with starting values: the titles with `std::getline`, the numbers with `>>`. No questions, no asking again and no vector.
- When the required data can't be read, including when the data end after the first book, the program prints exactly `Input error`.
- When the read succeeded but a title is empty or the numbers break the rules, the program prints exactly `Invalid books`.
- Only when everything is right does the program create two records with `{}` and print seven lines as in the example below, with the books in the order of the data. The total of unread pages comes from the fields of both records.

In `cpp-workspace`, create a folder `reading_progress`, copy `CMakeLists.txt` from the original `lesson_05_first_program` into it, create an empty `main.cpp` and write the program yourself.

For the data:

<!-- input: books -->
```text
Ocean Atlas
120 50
Quiet Garden
80 80
```

the standard output must be:

<!-- output: books -->
```text
Book 1: Ocean Atlas
Pages: 120
Read: 50
Book 2: Quiet Garden
Pages: 80
Read: 80
Unread total: 70
```

The second book's title is an empty line. The read succeeds, but the title is empty:

<!-- input: books -->
```text
Ocean Atlas
120 50

80 80
```

<!-- output: books -->
```text
Invalid books
```

There's a word instead of the second book's number of pages:

<!-- input: books -->
```text
Ocean Atlas
120 50
Quiet Garden
eighty 20
```

<!-- output: books -->
```text
Input error
```

For one run the program prints only one of these three results.

**These aren't shipments under another name.** The number line has two numbers, and one of the rules connects both. You have to decide yourself:

1. how to name the type and the fields, and which local variables you need for reading;
2. which values to read with `std::getline`, and which with `>>`;
3. where to finish the first book's number line, and why the last one doesn't need finishing;
4. when to check whether the reads succeeded;
5. how to separate `Input error` from `Invalid books`, including for an empty title;
6. how to write the rules for both books;
7. where to create the two records;
8. how to calculate the total of unread pages from the records' fields.

**Before you write the program**, prepare a table of cases: titles with spaces and one-word titles, books read through and books not started, empty titles, numbers of pages that aren't allowed, a word instead of a number, no second book, and a missing last number. For each, write down the expected result.

**Then** run the program for the main data and for one of the two other examples. Every case in the full list of check cases is checked automatically, so you don't need to run the others. Analyse the cases in which the data end on paper, as in section 4.

### Success criterion

- The program builds as C++20 and, for the main data and the second example you chose, prints exactly the results shown.
- The titles keep their inner spaces.
- The first book's number line is finished before the second title is read, and there's no read after the last number.
- `std::cin.fail()` is checked before the titles and the rules for the pages, and both records come into being only after all the checks.
- The table of cases was made before running the program.
- You can explain why an empty title gives `Invalid books`, and a missing title `Input error`.

When the result matches, you can save the project in Git, as in lesson 1.5.

<details>
<summary>Hint 1</summary>

How does the program know where the second book's title starts? What was left after reading the first book's numbers?

</details>

<details>
<summary>Hint 2</summary>

`>>` reads the numbers, but it doesn't have to take the end-of-line character. Before you read a new title, finish the current line.

</details>

<details>
<summary>Hint 3</summary>

After checking that the first book's numbers were read, use `getline` to read the rest of their line. Only with the next `getline` read the second book's title. Create the records after checking the whole input.

</details>

<details>
<summary>The full list of check cases: open it after preparing your own table</summary>

Successive lines of the data are separated by `/`. For valid data, the "Result" column gives the total of unread pages. The program then prints all seven lines, with the books in the order of the data.

| | Data | Result | What it checks |
|---|---|---|---|
| A | `Ocean Atlas` / `120 50` / `Quiet Garden` / `80 80` | 70 | the data in the requirements: two titles with spaces, the first book started, the second read through |
| B | `Atlas` / `100 10` / `Night Train` / `50 0` | 140 | a one-word title, then a title with a space |
| C | `Deep Blue Sea` / `300 120` / `Maps` / `40 0` | 220 | a title with spaces, then a one-word one |
| D | `One Page` / `1 1` / `Long Road Home` / `90 90` | 0 | both books read through, the smallest number of pages |
| E | `First Light` / `200 0` / `Second Wind` / `150 0` | 350 | neither book started |
| F | an empty line / `120 50` / `Quiet Garden` / `80 80` | `Invalid books` | an empty first title |
| G | `Ocean Atlas` / `120 50` / an empty line / `80 80` | `Invalid books` | an empty second title (the data in the requirements) |
| H | `Ocean Atlas` / `0 0` / `Quiet Garden` / `80 80` | `Invalid books` | zero pages in the first book |
| I | `Ocean Atlas` / `120 50` / `Quiet Garden` / `0 0` | `Invalid books` | zero pages in the second book |
| J | `Ocean Atlas` / `120 50` / `Quiet Garden` / `-5 0` | `Invalid books` | a negative number of pages |
| K | `Ocean Atlas` / `120 -1` / `Quiet Garden` / `80 80` | `Invalid books` | a negative number of pages read in the first book |
| L | `Ocean Atlas` / `120 50` / `Quiet Garden` / `80 -1` | `Invalid books` | a negative number of pages read in the second book |
| M | `Ocean Atlas` / `120 121` / `Quiet Garden` / `80 80` | `Invalid books` | more pages read than pages in total in the first book |
| N | `Ocean Atlas` / `120 50` / `Quiet Garden` / `80 81` | `Invalid books` | more pages read than pages in total in the second book |
| O | `Ocean Atlas` / `many 50` / `Quiet Garden` / `80 80` | `Input error` | a word instead of the first number |
| P | `Ocean Atlas` / `120 half` / `Quiet Garden` / `80 80` | `Input error` | a word instead of the second number |
| Q | `Ocean Atlas` / `120 50` / `Quiet Garden` / `eighty 20` | `Input error` | a failed read of a number in the second book (the data in the requirements) |
| R | `Ocean Atlas` / `120 50`, then the end of the data | `Input error` | no second book: reading the second title fails |
| S | `Ocean Atlas` / `120 50` / `Quiet Garden` / `80`, then the end of the data | `Input error` | a missing last number |
| T | `Ocean Atlas` / `120 50 pages` / `Quiet Garden` / `80 80` | 70 | text after the first book's numbers: `rest` takes it, but the program doesn't check it |
| U | `Ocean Atlas` / `120 50` / `Quiet Garden` / `80 80 done` | 70 | text after the last number: it stays unread, outside the checks |

**Automatic tests and your own runs.** Every case is checked automatically: the reference solution is run for each of them, and its whole standard output is compared with the expected one. The solution and its results are in [Example solutions](#example-solutions).

</details>

The example solution is in [Example solutions](#example-solutions).

## 7. Find the bug: the line finished in the wrong place

Do this task **after the mission**: the program below is meant to work the same way as the program in section 2. You can copy it into `main.cpp` in the `lesson_10_2` folder.

<details>
<summary>The program to check: open it after writing your own program</summary>

<!-- example: shipments_order_bug -->
```cpp
#include <iostream>
#include <string>

struct Shipment {
    std::string destination;
    int boxes;
};

int main() {
    std::string first_destination{};
    int first_boxes{0};
    std::string rest{};
    std::string second_destination{};
    int second_boxes{0};

    std::getline(std::cin, first_destination);
    std::cin >> first_boxes;

    if (!std::cin.fail()) {
        std::getline(std::cin, second_destination);
        std::getline(std::cin, rest);
        std::cin >> second_boxes;
    }

    if (std::cin.fail()) {
        std::cout << "Input error\n";
    } else if (first_destination.empty() || first_boxes < 0 || second_destination.empty() || second_boxes < 0) {
        std::cout << "Invalid shipment\n";
    } else {
        const Shipment first{first_destination, first_boxes};
        const Shipment second{second_destination, second_boxes};

        std::cout << "Shipment 1: " << first.destination << ", boxes " << first.boxes << "\n";
        std::cout << "Shipment 2: " << second.destination << ", boxes " << second.boxes << "\n";
        std::cout << "Total boxes: " << first.boxes + second.boxes << "\n";
    }
}
```

Data in which the second name is an empty line:

<!-- input: shipments_order_bug -->
```text
North Hub
4

7
```

1. **Predict** this program's result for these data. The program in section 2 prints `Invalid shipment` for them (section 4).
2. Run the program for these data and compare the result with your prediction.
3. Choose your own valid data, with a non-empty second name, for which this program prints a wrong result.
4. For your data, **predict** what ends up in `second_destination`, and what in `rest`.
5. Run the program for your data.
6. Explain why `getline` read the wrong part of the input.
7. Fix the order of the calls and run the fixed program for your data.
8. Why doesn't an empty `rest` in the fixed program mean a failed read?

</details>

The results, example data and the fixed program are in [Example solutions](#example-solutions).

## 8. When something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `Input error` for valid data with a title with a space | The title is read with `>>`: the variable gets the first word, and the read of a number runs into the second. | Read the title with `std::getline`. |
| `Input error` for valid data, although `getline` reads the titles | The first book's number line isn't finished. The second title is empty, and the read of a number runs into the real title. | After the first book's numbers, call `std::getline(std::cin, rest)`. |
| `Invalid books` or `Invalid shipment` for valid data | The line is finished only after the second title is read (section 7). | Finish the line before reading the next title. |
| An empty title gives `Input error` | The program checks for an empty title together with `std::cin.fail()`, but an empty line is a successful read. | Judge an empty title together with the rules for the pages, after checking the read. |
| An empty title gives a report | The `empty()` check is missing. | Reject an empty title just like numbers that aren't allowed. |
| `Unread total` is negative | The program lets through more pages read than pages in total. | Check this rule for both books. |
| The program waits, although all lines were typed | An empty line was typed instead of the numbers, or too few numbers. `>>` skips empty lines and waits for a number (lesson 10.1). | Type the missing numbers. |

## 9. Explain

Answer in your own words, preferably in writing. Only then compare with the example answers.

1. What does `>>` read from the line `Ocean Atlas`, and what does `std::getline` read? Why do we read the title with `getline`, and the numbers with `>>`?
2. What stays in the input right after `120 50` is read with two `>>`? What would a `getline` called at that point get?
3. What is `rest` for? Does an empty `rest` mean a failed read or the end of the data?
4. How does an empty title of the second book differ from a missing second book? What result does each of these cases give?
5. Why does the program check `std::cin.fail()` before it checks `empty()`?
6. How do `Input error` and `Invalid books` differ? Give one example of data for each result.
7. What does the program do with the text `pages` in the line `120 50 pages`? Does that mean this line is valid?
8. Why doesn't the program finish the line after the second book's last number?
9. The two books are in two separate records. What would be hard if there were ten books, or if their number weren't known in advance?

<details>
<summary>Example answers</summary>

1. `>>` reads only `Ocean`, because it stops reading text at the first space, and `Atlas` stays in the input. `std::getline` reads the whole line, `Ocean Atlas`, with the space in the middle. A title may have spaces, so `getline` reads it. Each number is a single value, so `>>` reads it: it skips whitespace before the number and stops reading at the first whitespace after it.
2. The end of that line, because `>>` stops before it and leaves it in the input. A `getline` called at that point would read only that end of the line and would get an empty text, while the next title would keep waiting.
3. `rest` takes the rest of the number line, and `getline` takes its end along with it. Thanks to that, the next `getline` starts at a new line. An empty `rest` is a successful read: there were no other characters in the line after the numbers. A failed read or the end of the data is shown by `std::cin.fail()`, not by the contents of `rest`.
4. An empty title is an empty line: the read succeeds, and the text is empty. The program goes on to the rules and prints `Invalid books`. When there's no second book, `getline` supplies no line and fails. The program then prints `Input error`.
5. Because after a failed read you can't rely on the variable's contents (lessons 4.6 and 7.4). An empty title means something only when it was really read. In the reverse order, missing data could be taken for an empty title.
6. `Input error` means that the required data couldn't be read, for example `eighty 20` instead of the numbers, or the data end after the first book. `Invalid books` means that everything was read, but the values break the rules, for example an empty title or `80 81`.
7. `>>` reads 120 and 50, and `getline(rest)` takes ` pages` along with the end of the line. The program doesn't check this text, so it prints the report (case T). That doesn't mean the line is valid: data with extra text are outside the agreement, and the program simply doesn't judge them.
8. Because after the last number the program reads no more titles. An extra `getline` would be unnecessary. If the data ended right after the last number, with no end of line, such a `getline` would fail and turn valid data into `Input error`.
9. Here each book needs its own variables, its own reads and its own record. With ten books the code would be long and repetitive, and with an unknown number of books it couldn't be written this way at all. The records will have to be added to a vector, which is the topic of lesson 10.3.

</details>

## Summary

- A name with spaces is read by `std::getline`, and the numbers by `>>`.
- After a number is read with `>>`, the end of the line stays in the input. A `getline` called right after it would read an empty text.
- `std::getline(std::cin, rest)` finishes the number line before the next name is read. An empty `rest` is a successful read, and the program doesn't check the contents of `rest`.
- We don't finish the line after the last number, because an extra read could turn valid data into an error.
- An empty name is a successful read and a value that isn't allowed, while a missing name is a failed read. That's why `std::cin.fail()` comes first, then `empty()`.
- The records come into being only after all the data have been checked, and the result comes from their fields.

## What's next

In this lesson the program read exactly two records, each into its own variables. In the next lesson the records read from the input will go into a vector with `push_back`. Lesson 10.3 is in preparation.

---

## Example solutions

Look here **after your own attempt**. Your names may differ, as long as the standard output is as required.

<details>
<summary>Section 6: the mission, reading progress of two books</summary>

<!-- example: books -->
```cpp
#include <iostream>
#include <string>

struct Book {
    std::string title;
    int pages;
    int pages_read;
};

int main() {
    std::string first_title{};
    int first_pages{0};
    int first_pages_read{0};
    std::string rest{};
    std::string second_title{};
    int second_pages{0};
    int second_pages_read{0};

    std::getline(std::cin, first_title);
    std::cin >> first_pages;
    std::cin >> first_pages_read;

    if (!std::cin.fail()) {
        std::getline(std::cin, rest);
        std::getline(std::cin, second_title);
        std::cin >> second_pages;
        std::cin >> second_pages_read;
    }

    if (std::cin.fail()) {
        std::cout << "Input error\n";
    } else if (first_title.empty() || first_pages <= 0 || first_pages_read < 0 || first_pages_read > first_pages) {
        std::cout << "Invalid books\n";
    } else if (second_title.empty() || second_pages <= 0 || second_pages_read < 0 || second_pages_read > second_pages) {
        std::cout << "Invalid books\n";
    } else {
        const Book first{first_title, first_pages, first_pages_read};
        const Book second{second_title, second_pages, second_pages_read};
        const int unread_total{(first.pages - first.pages_read) + (second.pages - second.pages_read)};

        std::cout << "Book 1: " << first.title << "\n";
        std::cout << "Pages: " << first.pages << "\n";
        std::cout << "Read: " << first.pages_read << "\n";
        std::cout << "Book 2: " << second.title << "\n";
        std::cout << "Pages: " << second.pages << "\n";
        std::cout << "Read: " << second.pages_read << "\n";
        std::cout << "Unread total: " << unread_total << "\n";
    }
}
```

1. **The title with `getline`,** because it may contain spaces, and `>>` would read only its first word.
2. **The numbers with `>>`,** because each is a single value, and `>>` skips the space between them.
3. **Finishing the first number line,** because after `>>` the end of that line stays in the input. Without `getline(rest)` the second title would be empty, and the read of a number would run into the real title.
4. **No finishing after the last number,** because the program reads no next title.
5. **Checking `getline`:** reading a title can fail too, when there are no more data. Then you can't rely on the contents of the title's variable. So the check at the end also covers both `getline` reads after the first book.
6. **An empty title isn't a failed read.** An empty line is read correctly (lesson 7.4), so the program judges it together with the rules for the pages and prints `Invalid books`.
7. **`fail()` doesn't know the book's rules:** 0 pages, or 81 pages read out of 80, are correctly read numbers. The rules are checked by separate conditions.
8. **Text after the numbers is outside the checks.** `getline(rest)` takes the rest of the first number line, but the program doesn't judge it (case T). Text after the last number stays unread in the input (case U). Such data are outside the agreement.
9. **Starting values for the variables,** because after a failed read a variable can keep its previous value. Without a starting value, that would be an indeterminate value.
10. **The records at the end,** because only then is it known that both books are complete and valid. With an error in the second book the first record isn't created either, so nothing is printed partly.
11. **No vector,** because there are exactly two books, and each has its own variables and its own record. A vector of records is the topic of lesson 10.3.
12. **No function that reads a record,** because the two reads fit readably in `main`, and the agreement doesn't require such a function.
13. **The last number at the end of the data.** When the data end right after the last number, with no end of line, reading it still succeeds (lesson 4.6). The program does no further read after it, so it doesn't turn valid data into `Input error`. The course's automatic tests don't run this case.
14. **Preparing for lesson 10.3.** The pattern for one record is fixed: the name with `getline`, the numbers with `>>`, and finishing the line before the next name. With many records the same pattern will repeat for each of them, and the finished records will go into a vector.

**Other valid solutions:** the rules for both books can stand in one condition, or each in its own `else if`, with the same message. The check after the first book can also be left out, keeping only the one at the end: the results are the same, because after a failed read the following reads fail too (lesson 4.6). The check after the first book, however, shows directly that the line is finished only after the numbers were read successfully. The fields can have other names, and the total can be calculated directly in the output statement.

Each case in the list of check cases is a separate run of this program. Cases A, G and Q are the data in the mission. The others are below, in the order of the list of check cases.

<!-- input: books -->
```text
Atlas
100 10
Night Train
50 0
```

<!-- output: books -->
```text
Book 1: Atlas
Pages: 100
Read: 10
Book 2: Night Train
Pages: 50
Read: 0
Unread total: 140
```

<!-- input: books -->
```text
Deep Blue Sea
300 120
Maps
40 0
```

<!-- output: books -->
```text
Book 1: Deep Blue Sea
Pages: 300
Read: 120
Book 2: Maps
Pages: 40
Read: 0
Unread total: 220
```

<!-- input: books -->
```text
One Page
1 1
Long Road Home
90 90
```

<!-- output: books -->
```text
Book 1: One Page
Pages: 1
Read: 1
Book 2: Long Road Home
Pages: 90
Read: 90
Unread total: 0
```

<!-- input: books -->
```text
First Light
200 0
Second Wind
150 0
```

<!-- output: books -->
```text
Book 1: First Light
Pages: 200
Read: 0
Book 2: Second Wind
Pages: 150
Read: 0
Unread total: 350
```

<!-- input: books -->
```text

120 50
Quiet Garden
80 80
```

<!-- output: books -->
```text
Invalid books
```

<!-- input: books -->
```text
Ocean Atlas
0 0
Quiet Garden
80 80
```

<!-- output: books -->
```text
Invalid books
```

<!-- input: books -->
```text
Ocean Atlas
120 50
Quiet Garden
0 0
```

<!-- output: books -->
```text
Invalid books
```

<!-- input: books -->
```text
Ocean Atlas
120 50
Quiet Garden
-5 0
```

<!-- output: books -->
```text
Invalid books
```

<!-- input: books -->
```text
Ocean Atlas
120 -1
Quiet Garden
80 80
```

<!-- output: books -->
```text
Invalid books
```

<!-- input: books -->
```text
Ocean Atlas
120 50
Quiet Garden
80 -1
```

<!-- output: books -->
```text
Invalid books
```

<!-- input: books -->
```text
Ocean Atlas
120 121
Quiet Garden
80 80
```

<!-- output: books -->
```text
Invalid books
```

<!-- input: books -->
```text
Ocean Atlas
120 50
Quiet Garden
80 81
```

<!-- output: books -->
```text
Invalid books
```

<!-- input: books -->
```text
Ocean Atlas
many 50
Quiet Garden
80 80
```

<!-- output: books -->
```text
Input error
```

<!-- input: books -->
```text
Ocean Atlas
120 half
Quiet Garden
80 80
```

<!-- output: books -->
```text
Input error
```

<!-- input: books -->
```text
Ocean Atlas
120 50
```

<!-- output: books -->
```text
Input error
```

<!-- input: books -->
```text
Ocean Atlas
120 50
Quiet Garden
80
```

<!-- output: books -->
```text
Input error
```

<!-- input: books -->
```text
Ocean Atlas
120 50 pages
Quiet Garden
80 80
```

<!-- output: books -->
```text
Book 1: Ocean Atlas
Pages: 120
Read: 50
Book 2: Quiet Garden
Pages: 80
Read: 80
Unread total: 70
```

<!-- input: books -->
```text
Ocean Atlas
120 50
Quiet Garden
80 80 done
```

<!-- output: books -->
```text
Book 1: Ocean Atlas
Pages: 120
Read: 50
Book 2: Quiet Garden
Pages: 80
Read: 80
Unread total: 70
```

</details>

<details>
<summary>Section 7: the results before the fix, and the fixed program</summary>

Before the fix, for the data with an empty second name:

<!-- output: shipments_order_bug -->
```text
Invalid shipment
```

- **This case masks the bug.** Both programs print `Invalid shipment`, but for different reasons. In the program in section 2, `second_destination` gets the empty line from the data. In the buggy program it gets the end of the line after `4`, that is an empty text, and the empty line from the data ends up in `rest`. The result is the same, so these data don't reveal the bug.
- **Data that reveal the bug:** any valid data with a non-empty second name, for example the data in section 2. The correct result is the report of both shipments, and the buggy program prints:

<!-- input: shipments_order_bug -->
```text
North Hub
4
South Depot
7
```

<!-- output: shipments_order_bug -->
```text
Invalid shipment
```

- **What ends up in the variables:** `second_destination` gets an empty text, that is the rest of the line after `4`. `rest` gets `South Depot`, and `>>` reads 7. All reads succeeded, so the program checks the rules and rejects the empty name.
- **The cause:** `getline` reads from the place where the previous read stopped. After `>> first_boxes` that place is the end of the line with the number 4. The first `getline` after the number always reads the rest of that line, whichever variable it stores the text in. The buggy program stores it in `second_destination`.
- **The fix:** swap the order of the two calls: first `getline` into `rest`, then `getline` into `second_destination`. The fixed program is the program in section 2:

<!-- example: shipments_order_fixed -->
```cpp
#include <iostream>
#include <string>

struct Shipment {
    std::string destination;
    int boxes;
};

int main() {
    std::string first_destination{};
    int first_boxes{0};
    std::string rest{};
    std::string second_destination{};
    int second_boxes{0};

    std::getline(std::cin, first_destination);
    std::cin >> first_boxes;

    if (!std::cin.fail()) {
        std::getline(std::cin, rest);
        std::getline(std::cin, second_destination);
        std::cin >> second_boxes;
    }

    if (std::cin.fail()) {
        std::cout << "Input error\n";
    } else if (first_destination.empty() || first_boxes < 0 || second_destination.empty() || second_boxes < 0) {
        std::cout << "Invalid shipment\n";
    } else {
        const Shipment first{first_destination, first_boxes};
        const Shipment second{second_destination, second_boxes};

        std::cout << "Shipment 1: " << first.destination << ", boxes " << first.boxes << "\n";
        std::cout << "Shipment 2: " << second.destination << ", boxes " << second.boxes << "\n";
        std::cout << "Total boxes: " << first.boxes + second.boxes << "\n";
    }
}
```

<!-- input: shipments_order_fixed -->
```text
North Hub
4
South Depot
7
```

<!-- output: shipments_order_fixed -->
```text
Shipment 1: North Hub, boxes 4
Shipment 2: South Depot, boxes 7
Total boxes: 11
```

- **An empty `rest` in the fixed program:** `rest` is empty because there were no other characters after `4`. The read succeeded, and `getline` took the end of the line. A failed read is shown by `std::cin.fail()`, not by an empty text.

</details>

**Previous lesson:** [Lesson 10.1: One record from input](lesson_01_one_record_from_input.en.md) · **Next lesson:** in preparation · [Course overview](../../README.en.md)

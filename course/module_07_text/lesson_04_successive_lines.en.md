# Lesson 7.4: Processing successive lines with `std::getline`

[Polski](lesson_04_successive_lines.md) · **English** · [Course overview](../../README.en.md)

> **Module 7, lesson 4** · about 65–80 minutes
> **You need:** your `cpp-workspace` folder and the original `lesson_05_first_program` project, as before. Your `initials` project from lesson 7.3 will also be useful. You won't need the debugger in this lesson.
> **Pilot version.** The programs in this lesson are checked automatically on Windows, Ubuntu and macOS, including with the given input data. Typing input in CLion's **Run** window is described without a manual check on every system.

## Before you start

This lesson assumes that you:

- read a whole line of text with `std::getline` (lesson 2.7);
- check with `std::cin.fail()` whether a read succeeded, and end a `while` loop with a `bool` flag (lesson 4.5);
- remember the rule "success first, then the end of the data" (lesson 4.6);
- store sizes in the type `std::size_t` (lesson 6.3);
- write a function that gets a text through `const std::string&` and returns its initials as a new `std::string` (lesson 7.3).

## The situation

In lesson 7.3, the text was written in the code, and a function worked out its initials:

<!-- fragment -->
```cpp
const std::string name{"Ada Lovelace"};
```

But what if the user types the texts while the program runs, and nobody knows in advance how many there will be? A separate variable and a separate function call for each text are out of the question. You need a loop that repeats four steps:

1. read one line;
2. check whether that's the end;
3. if not, analyse the line and print the result;
4. go back to reading the next line.

The earlier lines don't need to be stored: two counters are enough for the summary. You already know every operation you need; what's new is putting them together.

After this lesson you will:

- read successive lines in a `while` loop controlled by a `bool` flag;
- tell an empty line from a failed read, also for the last line of the data;
- combine a reading loop with a text function, and count the processed lines and characters.

## 1. Prepare the project

In `cpp-workspace`, create a folder `lesson_7_4` and copy `main.cpp` and `CMakeLists.txt` into it from the original `lesson_05_first_program`. You type the programs from sections 2 and 4 into that folder's `main.cpp`.

The programs in this lesson print no questions. After you start one, type the data straight away and end each line with **Enter**. An empty line is just pressing **Enter**, with no character.

## 2. One line: a reminder of `std::getline`

The program reads one line and prints it in square brackets, together with its number of characters:

<!-- example: one_line -->
```cpp
#include <iostream>
#include <string>

int main() {
    std::string line{};
    std::getline(std::cin, line);

    if (std::cin.fail()) {
        std::cout << "Input could not be read\n";
    } else {
        std::cout << "Line: [" << line << "]\n";
        std::cout << "Characters: " << line.size() << "\n";
    }
}
```

Run the program, type `Ada Lovelace` and press **Enter**:

<!-- input: one_line -->
```text
Ada Lovelace
```

**Predict:** will the space stay in the text? How many characters will the program print?

<details>
<summary>Standard output</summary>

<!-- output: one_line -->
```text
Line: [Ada Lovelace]
Characters: 12
```

</details>

`std::getline` reads a **whole line** with its spaces, not one word like `>>` (lesson 2.7). The read ends at the **end-of-line character**, which pressing **Enter** produces. It's the same character the program prints with `"\n"`. `getline` takes it from the input but **doesn't add** it to the text. That's why `Ada Lovelace` has 12 characters: 11 letters and one space.

**Why only `getline`.** After a read with `>>`, the end-of-line character stays in the input, and a `getline` called straight after it would read it as an empty line (lesson 2.7). In this lesson an empty line means the end of the work, so such a leftover character would end the reading before the first text. That's why the programs in this lesson read their data only with `std::getline`. How to combine both kinds of reading comes later.

## 3. An empty line versus a failed read

**Predict** what happens in the program from section 2 when you press **Enter** straight away, without typing any character: will the read succeed? Compare with the result below. Running it is optional.

<!-- input: one_line -->
```text

```

<details>
<summary>Standard output</summary>

<!-- output: one_line -->
```text
Line: []
Characters: 0
```

</details>

This is the most important distinction in this lesson:

- **An empty line is a successful read.** The input held just the end-of-line character. The text is empty: `line.size()` gives 0, and `line.empty()` gives `true`. The program didn't take the `fail()` branch.
- **A failed read** means that `getline` delivered no line, because the input had neither characters nor an end-of-line character left. Usually that's the end of the data. `std::cin.fail()` then gives `true`.

Less often a read fails for other reasons, for example an input error, but here they don't need to be told apart: every failed read ends the processing.

| Situation | What's waiting in the input | `std::cin.fail()` | `line` after the read | The program's decision |
|---|---|---|---|---|
| an ordinary line | characters and the end-of-line character | `false` | the text without the end-of-line character | process it |
| an empty line | just the end-of-line character | `false` | an empty text, `empty()` gives `true` | stop |
| no data | nothing | `true` | its contents can't be relied on | stop |

The order of checks after each read:

1. Did the read succeed? If not, the processing ends.
2. Is the line empty? If so, the processing ends.
3. Only a non-empty, successfully read line goes on to be analysed.

That's the rule from lesson 4.5: after a failed read, no decision is based on the variable's contents. An empty line means "that's all" only when the read succeeded. You'll trace the no-data case on paper in section 5.

## 4. Many lines: a loop with a flag

The program reads successive lines until it meets an empty line or a read fails, and counts the processed lines and their characters:

<!-- example: line_counter -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>

int main() {
    bool reading{true};
    std::size_t line_count{0};
    std::size_t character_count{0};

    while (reading) {
        std::string line{};
        std::getline(std::cin, line);

        if (std::cin.fail()) {
            reading = false;
        } else if (line.empty()) {
            reading = false;
        } else {
            ++line_count;
            character_count += line.size();
        }
    }

    std::cout << "Lines: " << line_count << "\n";
    std::cout << "Characters: " << character_count << "\n";
}
```

Run the program and type `Ada`, `Bob`, and then an empty line:

<!-- input: line_counter -->
```text
Ada
Bob

```

**Predict** both numbers. Will the empty line at the end be counted?

<details>
<summary>Standard output</summary>

<!-- output: line_counter -->
```text
Lines: 2
Characters: 6
```

</details>

- **The flag `reading`** starts as `true`, and the loop's condition is the flag itself, like a `bool` value in an `if` condition in lesson 3.2. The program sets it to `false` after a failed read and after an empty line.
- **One read per pass**, followed by one decision: stop or process.
- **`line` is created anew in every pass**, so nothing from the previous line stays in it.
- **The counters grow only in the last branch**, that is, for a line that really went on to be analysed. `character_count` gets `line.size()`: spaces count, but end-of-line characters don't. Both counters have the type `std::size_t`, like sizes in lesson 6.3.

**Why one flag?** The summary is the same for both causes of ending, so, unlike in lesson 4.5, the program doesn't need to know what ended the loop.

| Attempt | Line read | `fail()` | `empty()` | Decision | `reading` after the attempt | `line_count` | `character_count` |
|---|---|---|---|---|---|---|---|
| 1 | `Ada` | `false` | `false` | process | `true` | 1 | 3 |
| 2 | `Bob` | `false` | `false` | process | `true` | 2 | 6 |
| 3 | empty | `false` | `true` | stop | `false` | 2 | 6 |

## 5. The end of the data and the last line

You don't need to cause the end of the data yourself: assume that the input ends after the last line given, and trace the program on paper. **Predict:** how will the table from section 4 change when the data ends straight after the line `Bob`, with no empty line?

<details>
<summary>The answer and the standard output</summary>

Attempts 1 and 2 go the same way. In attempt 3, `getline` delivers no line: `fail()` gives `true`, and the program sets `reading` to `false` without checking `empty()`. The counters don't change, so the summary is the same as after an empty line. The course's automatic tests check this case on Windows, Ubuntu and macOS:

<!-- input: line_counter -->
```text
Ada
Bob
```

<!-- output: line_counter -->
```text
Lines: 2
Characters: 6
```

</details>

**A last line without an end-of-line character.** The data can also end straight after the last character of a line, for example in a text file. Trace this data: `Ada`, an end-of-line character, `Bob` and nothing more:

| Attempt | What `getline` delivers | `fail()` | Decision | `line_count` | `character_count` |
|---|---|---|---|---|---|
| 1 | `Ada` | `false` | process | 1 | 3 |
| 2 | `Bob`, and the data ends straight after it | `false` | process | 2 | 6 |
| 3 | nothing | `true` | stop | 2 | 6 |

In attempt 2 the stream reached the end of the data, and yet the read **succeeded**: `fail()` gives `false`, and `line` holds `Bob`. It's the situation from lesson 4.6, where the last number without an end of line was read correctly, although `eof()` already gave `true`. So the program processes `Bob` like any other line, and only the next, failed attempt ends the loop. A program that stopped as soon as `eof()` gave `true` would lose `Bob`. The course's automatic tests don't run this case, because in them every line ends with an end-of-line character.

**After a failed read, don't use `line`.** If `line` were created before the loop, after attempt 3 it could still hold `Bob`, and a program that doesn't check `fail()` first could process that line a second time. That can't happen in the program from section 4.

## 6. An empty line isn't the same as spaces

| Text | `size()` | `empty()` | In this lesson |
|---|---|---|---|
| `""`, an empty line | 0 | `true` | ends the reading |
| `" "`, one space | 1 | `false` | an ordinary data line |
| `"   "`, three spaces | 3 | `false` | an ordinary data line |

**Only a line of length zero ends the reading.** A line of one or more spaces isn't empty: it has characters, only none of them is a letter. The program doesn't remove its spaces and doesn't treat it as empty.

Data for the program from section 4: three spaces and **Enter**, then **Enter** once more:

<!-- input: line_counter -->
```text
   

```

**Predict** the result and compare it with the result below. Running it is optional.

<details>
<summary>Standard output</summary>

<!-- output: line_counter -->
```text
Lines: 1
Characters: 3
```

</details>

The first line isn't empty, so it was processed and counted, with its three spaces. Only the second, truly empty line ended the loop.

## 7. Mission: a log of short texts

The program gets successive lines with short texts, for example first names and surnames. It numbers each line, prints it and gives its initials, and at the end it prints a summary.

**What data is possible.** The same as in lesson 7.3: the letters `A`–`Z` and `a`–`z` and ordinary spaces, with no digits, tabs, punctuation or Polish letters. There can be several spaces, they can stand at the start and the end of a line, and a line can consist of spaces only. You don't need to check these assumptions.

**Rules:**

- The program processes successive lines until it reads an empty line or a read fails. The empty line isn't reported, and the program doesn't read anything that stands after it.
- For each processed line it prints `Line N: [TEXT]` and `Initials N: [RESULT]`: the number from 1, the original line with all its spaces, and its initials, as in lesson 7.3.
- At the end it prints `Lines processed: N` and `Characters processed: N`. The number of characters is the sum of `size()` over the processed lines: with spaces, but without end-of-line characters and without the initials.
- The summary doesn't depend on what ended the reading. The program prints no questions and no message about finishing.

**Requirements:**

- At least one function of your own gets a text through `const std::string&` and returns its initials as a new `std::string`, without reading or printing anything. You can copy it from your `initials` project from lesson 7.3.
- `main` reads the lines with `std::getline` in a `while` loop controlled by a `bool` flag, and does all the printing.
- The program doesn't store the earlier lines.

In `cpp-workspace`, create a folder `texts_log`, copy `CMakeLists.txt` into it from the original `lesson_05_first_program`, create an empty `main.cpp` and write the program yourself.

For this input:

<!-- input: texts_log -->
```text
Ada Lovelace
Mary ann SMITH

Ignored line
```

the standard output must be:

<!-- output: texts_log -->
```text
Line 1: [Ada Lovelace]
Initials 1: [AL]
Line 2: [Mary ann SMITH]
Initials 2: [MaS]
Lines processed: 2
Characters processed: 26
```

`Ada Lovelace` has 12 characters and `Mary ann SMITH` 14, 26 in total. `Ignored line` stands after the empty line, so the program doesn't read it. When you type the data yourself, the program ends straight after the empty line.

When the first line is empty, the program processes no line. It's an empty line, not missing data:

<!-- input: texts_log -->
```text

```

<!-- output: texts_log -->
```text
Lines processed: 0
Characters processed: 0
```

A line of three spaces isn't empty, so the program processes it. It has no words, so its initials are empty:

<!-- input: texts_log -->
```text
   

```

<!-- output: texts_log -->
```text
Line 1: [   ]
Initials 1: []
Lines processed: 1
Characters processed: 3
```

**The initials function isn't a new task here:** it comes from lesson 7.3. What's new is controlling the reading. You decide on your own:

1. where to create the variable for the current line;
2. when to check `std::cin.fail()`, and when `line.empty()`;
3. when to increase the line counter, and how to number the report with it;
4. when to call the initials function;
5. how to print the line so that its spaces stay visible;
6. how to count the characters with `size()`;
7. how to keep a line's report separate from the summary;
8. why the initials function shouldn't call `getline` itself.

**Before you write the program**, prepare a table of cases: an empty first line, one line, data that ends without an empty line, only spaces, spaces at the start and the end, an empty line between two texts, and mixed letter case. For each, write down the initials, and the numbers of lines and characters from the summary.

**Then** run the program for the data from the example, without `Ignored line`, and for one case from your table, preferably a line of only spaces, followed by an empty line. In the terminal, the lines you type mix with the report, because the program answers straight after each line. Trace the cases that end with the end of the data on paper. Every case in the full list of check cases is checked automatically, so you don't need to run the others.

### Success criteria

- The program builds as C++20 and, for the data from the example, prints exactly the six lines shown above.
- The read's success is checked before `line.empty()`, and the initials function reads and prints nothing.
- An empty line goes neither into the report nor into the counters, and a line of spaces only is processed.
- The last line before the end of the data is processed exactly once.
- The summary appears after the loop and is the same for both ways of ending.
- The table of cases was made before you ran the program.
- You can explain why the program doesn't need a vector of all the lines.

When the result matches, you can save the project in Git, as in lesson 1.5.

<details>
<summary>Hint 1</summary>

Which three decisions must be made after each attempt to read one line: did the read succeed, is the text empty, should it be processed?

</details>

<details>
<summary>Hint 2</summary>

The counter of processed lines should grow only for a line that really went on to be analysed. The empty line that ends the input isn't a record.

</details>

<details>
<summary>Hint 3</summary>

For each non-empty line, call the initials function you know, print the two report lines, and add `line.size()` to the total number of characters. Print the summary only after the loop ends.

</details>

<details>
<summary>The full list of check cases: open it after preparing your own table</summary>

| | Input | Initials | Lines | Characters | What it checks |
|---|---|---|---|---|---|
| A | `Ada Lovelace`, `Mary ann SMITH`, an empty line, `Ignored line` | `AL`, `MaS` | 2 | 26 | the example data; nothing is read after the empty line |
| B | an empty line | none | 0 | 0 | an empty first line |
| C | `Ada`, an empty line | `A` | 1 | 3 | one line |
| D | `Ada Lovelace`, `Mary ann SMITH`, the end of the data | `AL`, `MaS` | 2 | 26 | the end of the data instead of an empty line: the same report as in A |
| E | three spaces, an empty line | an empty result | 1 | 3 | spaces only are data |
| F | `  Ada  `, an empty line | `A` | 1 | 7 | spaces at the start and the end |
| G | `A  B   C`, an empty line | `ABC` | 1 | 8 | several spaces between words |
| H | `A`, an empty line | `A` | 1 | 1 | one letter |
| I | `Bo`, `Grace Hopper`, `Alan Mathison Turing`, an empty line | `B`, `GH`, `AMT` | 3 | 34 | lines of different lengths |
| J | `Grace Hopper`, an empty line, `Ada Lovelace` | `GH` | 1 | 12 | a text after the empty line isn't processed |
| K | `Al`, `Bo`, `Cy`, `Di`, `Ed`, the end of the data | `A`, `B`, `C`, `D`, `E` | 5 | 10 | numbering up to 5; the last line before the end of the data |
| L | `ada lovelace`, `ADA LOVELACE`, `ada Lovelace`, an empty line | `al`, `AL`, `aL` | 3 | 36 | letter case in the initials |

**Automatic tests and your own runs.** Every case is checked automatically. The reference solution reads its data from the input itself, so it needs no separate check program. Cases A, B and E are shown above, and the others are in [Example solutions](#example-solutions). In cases D and K the data ends after the last line given. The empty line in case B is one end-of-line character, not missing data. The tests don't run a last line without an end-of-line character (section 5).

</details>

An example solution is in [Example solutions](#example-solutions).

## 8. Find the bug: the empty line in the counter

Do this task **after the mission**: the program below contains almost the whole solution. It reports the successive lines correctly, but its summary doesn't always match. Like the mission's program, it prints no questions.

<details>
<summary>The program to check: open it after writing your own program</summary>

<!-- example: texts_log_count_bug -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>

std::string initials_of(const std::string& text) {
    std::string result{};

    for (std::size_t index{0}; index < text.size(); ++index) {
        const bool word_can_start{index == 0 || text[index - 1] == ' '};

        if (text[index] != ' ' && word_can_start) {
            result.push_back(text[index]);
        }
    }

    return result;
}

int main() {
    bool reading{true};
    std::size_t lines_processed{0};
    std::size_t characters_processed{0};

    while (reading) {
        std::string line{};
        std::getline(std::cin, line);

        if (std::cin.fail()) {
            reading = false;
        } else {
            ++lines_processed;

            if (line.empty()) {
                reading = false;
            } else {
                characters_processed += line.size();

                const std::string initials{initials_of(line)};

                std::cout << "Line " << lines_processed << ": [" << line << "]\n";
                std::cout << "Initials " << lines_processed << ": [" << initials << "]\n";
            }
        }
    }

    std::cout << "Lines processed: " << lines_processed << "\n";
    std::cout << "Characters processed: " << characters_processed << "\n";
}
```

1. **Predict** the result for two sets: (a) `Ada Lovelace` and `Mary ann SMITH`, after which the data ends; (b) `Ada` and an empty line.
2. Set (a) ends with the end of the data, so trace it on paper and compare with the result in Example solutions. Is the summary correct? Will the fix from step 5 change anything here?
3. Run the program for set (b). How many lines does the summary give, and how many `Line N` reports did the program print?
4. Point to the place where the program increases the counter. For which reads does that happen?
5. Fix the order: the counter should grow only once it's known that the line isn't empty.
6. Run the fixed program for set (b). You can also check an empty first line.

</details>

The program's output before the fix, and the fixed program, are in [Example solutions](#example-solutions).

## 9. When something goes differently

| What you see | What it means | What to do |
|---|---|---|
| The summary has one line too many | The counter grows before the program checks whether the line is empty (section 8). | Increase the counter only in the branch that processes the line. |
| The program prints `Line N: []` for the empty line at the end | The line is processed before the program checks whether it's empty. | Check `fail()` first, then `empty()`, and only then process. |
| A line of spaces only ends the reading | The program treats spaces as an empty line. | Only a line for which `line.empty()` gives `true` ends the reading. Spaces only are an ordinary data line. |
| After an empty line, the program waits for more data | The empty line doesn't change the flag, for example because the program checks something other than `line.empty()`. | After an empty line, set the flag to `false`. |
| The number of characters is larger by the number of lines | The program counts the end-of-line character, for example it adds `line.size() + 1`. | `getline` doesn't add the end-of-line character to the text. Add just `line.size()`. |
| The summary appears after every line | The summary is printed inside the loop. | Print the summary after the loop. |
| Spaces from the start or the end of a line are missing from the report | The line was read with `>>`, or the program prints something other than the original text. | Read the line with `std::getline` and print it unchanged. |
| The program stops reading before you type the first text | Before `getline` there's a read with `>>`, which left an end-of-line character (section 2). | In this lesson, read data only with `std::getline`. |

## 10. Explain

Answer in your own words, preferably in writing. Only then compare with the example answers.

1. How does reading one line differ from reading successive lines?
2. Does `getline` keep spaces? Does it add the end-of-line character to the text?
3. Can an empty line be read successfully? What does `line.empty()` give then? Is the text `"   "` empty?
4. Why do we check the read's success first, and only then `empty()`?
5. Does the end of the data always mean that the line read last is invalid?
6. Why doesn't the program store all the lines in a vector?
7. Why shouldn't the initials function read the input itself?

<details>
<summary>Example answers</summary>

1. One read gives one text. When there are many lines, and their number isn't known in advance, the read stands in a loop: one attempt per pass, until an empty line or a failed read ends the work.
2. It keeps every space, also at the start and the end of the line. It doesn't add the end-of-line character: it takes it from the input, but that character only ends the read. That's why it isn't in `size()`.
3. Yes. An empty line is a successful read: `fail()` gives `false`, and the text read has no characters, so `line.empty()` gives `true`. In this lesson it's the user's signal that there are no more texts. The text `"   "` isn't empty: it has three characters, spaces, so `size()` gives 3 and `empty()` gives `false`. It's an ordinary data line with empty initials.
4. Because after a failed read, the contents of `line` can't be relied on. First you need to know whether a line was read at all. Only then do its contents, including whether it's empty, mean anything.
5. No. The last line can be read successfully even when the data ends straight after it. `fail()` decides whether it's processed, and only the next, failed attempt ends the loop.
6. Because each line's result needs only that line, and the summary needs only two counters. No later decision needs the earlier lines. A vector would be needed if the program had to go back to all the lines after reading them, for example to print them in a different order.
7. Because its job is only to work out the initials of a given text. A function that doesn't read the input works for any text: one written in the code, as in lesson 7.3, and one read from the input, as here. `main` is responsible for reading, ending the work and printing, as in the division of responsibilities from lesson 5.5.

</details>

## Summary

- `std::getline` reads a whole line with its spaces. The end-of-line character ends the read, but doesn't go into the text.
- An empty line is a successful read with an empty text. A failed read means there's no line, usually because the data has ended.
- After each read: `fail()` first, then `empty()`, and only then processing.
- A `while` loop with a `bool` flag makes one read per pass. The last line before the end of the data must be processed too.
- A line of spaces only isn't empty.
- The counters grow only for processed lines, and the earlier lines don't need to be stored.

## What's next

In the Module 7 test you'll use the skills from the whole module: analysing characters and their positions, building a new text, and reading many lines: [Lesson 7.5: Parcel code check (the Module 7 test)](lesson_05_parcel_code_check.en.md).

---

## Example solutions

Look here **after your own attempt**. Your names may differ, as long as the standard output is as required.

<details>
<summary>Section 7: the mission, a log of short texts</summary>

<!-- example: texts_log -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>

std::string initials_of(const std::string& text) {
    std::string result{};

    for (std::size_t index{0}; index < text.size(); ++index) {
        const bool word_can_start{index == 0 || text[index - 1] == ' '};

        if (text[index] != ' ' && word_can_start) {
            result.push_back(text[index]);
        }
    }

    return result;
}

int main() {
    bool reading{true};
    std::size_t lines_processed{0};
    std::size_t characters_processed{0};

    while (reading) {
        std::string line{};
        std::getline(std::cin, line);

        if (std::cin.fail()) {
            reading = false;
        } else if (line.empty()) {
            reading = false;
        } else {
            ++lines_processed;
            characters_processed += line.size();

            const std::string initials{initials_of(line)};

            std::cout << "Line " << lines_processed << ": [" << line << "]\n";
            std::cout << "Initials " << lines_processed << ": [" << initials << "]\n";
        }
    }

    std::cout << "Lines processed: " << lines_processed << "\n";
    std::cout << "Characters processed: " << characters_processed << "\n";
}
```

1. **Why a loop.** Every line needs the same steps: reading, a decision and a report. The loop repeats them for successive lines, without separate code for each one.
2. **The number of lines needn't be known in advance.** The loop doesn't count passes up to any limit. It runs while the flag `reading` is true, and a situation in the data ends it: an empty line or a failed read.
3. **The read first, then the analysis.** `std::cin.fail()` is checked first, because after a failed read the contents of `line` can't be relied on. Only after a successful read does the program check `line.empty()`.
4. **An empty line ends the work**, because it's the agreed signal from the user. It isn't a record, so it goes neither into the report nor into the counters.
5. **Spaces only don't end the work.** `"   "` has three characters, so `empty()` gives `false`. The line is processed, and the function returns empty initials for it.
6. **The last line may have no end-of-line character.** When the data ends straight after its last character, `getline` still delivers it, and `fail()` gives `false`. The program processes it, and only the next, failed attempt ends the loop.
7. **The counter after the checks.** `++lines_processed` stands in the branch for a non-empty, successfully read line. So the number in the report and the count in the summary concern only processed lines.
8. **The function for each line separately.** Each line is a separate text with its own initials. `initials_of` gets it through `const std::string&`, without copying, and returns a new text that `main` prints straight away.
9. **No vector.** A line's report is made straight after the line is read, and the summary needs only two numbers. No decision needs the earlier lines.
10. **The same summary.** Both causes of ending set the same flag, and the summary stands after the loop, so it doesn't depend on what ended it.
11. **Only `getline`.** After a read with `>>`, an end-of-line character would stay in the input. `getline` would read it as an empty line, and the program would end before processing any text.
12. **What we leave for later:** telling the causes of a failed read apart, combining `>>` with `getline`, checking whether the lines meet the mission's assumptions, for example whether they contain digits, and reading data from files.

**Other correct layouts.** Both branches that end the loop can be joined in one condition: `if (std::cin.fail() || line.empty())`. Short-circuit evaluation from lesson 3.4 then checks `line.empty()` only after a successful read. What matters is that the processing and the counters stand only in the branch for a non-empty, successfully read line. In other programs you may also meet the read written straight into the loop's condition: `while (std::getline(std::cin, line))`. It's correct C++, but understanding it needs knowledge about streams that we don't have yet, so in this course we stay with the flag and `std::cin.fail()`.

**The results of the remaining check cases.** Cases A, B and E are in the mission's text. In cases D and K the data ends after the last line given.

Case C, `Ada` and an empty line:

<!-- input: texts_log -->
```text
Ada

```

<!-- output: texts_log -->
```text
Line 1: [Ada]
Initials 1: [A]
Lines processed: 1
Characters processed: 3
```

Case D, the same two lines as in A, after which the data ends:

<!-- input: texts_log -->
```text
Ada Lovelace
Mary ann SMITH
```

<!-- output: texts_log -->
```text
Line 1: [Ada Lovelace]
Initials 1: [AL]
Line 2: [Mary ann SMITH]
Initials 2: [MaS]
Lines processed: 2
Characters processed: 26
```

Case F, `  Ada  ` with two spaces at the start and two at the end:

<!-- input: texts_log -->
```text
  Ada  

```

<!-- output: texts_log -->
```text
Line 1: [  Ada  ]
Initials 1: [A]
Lines processed: 1
Characters processed: 7
```

Case G, `A  B   C`:

<!-- input: texts_log -->
```text
A  B   C

```

<!-- output: texts_log -->
```text
Line 1: [A  B   C]
Initials 1: [ABC]
Lines processed: 1
Characters processed: 8
```

Case H, `A`:

<!-- input: texts_log -->
```text
A

```

<!-- output: texts_log -->
```text
Line 1: [A]
Initials 1: [A]
Lines processed: 1
Characters processed: 1
```

Case I, lines of different lengths, 2, 12 and 20 characters:

<!-- input: texts_log -->
```text
Bo
Grace Hopper
Alan Mathison Turing

```

<!-- output: texts_log -->
```text
Line 1: [Bo]
Initials 1: [B]
Line 2: [Grace Hopper]
Initials 2: [GH]
Line 3: [Alan Mathison Turing]
Initials 3: [AMT]
Lines processed: 3
Characters processed: 34
```

Case J, an empty line between two texts:

<!-- input: texts_log -->
```text
Grace Hopper

Ada Lovelace
```

<!-- output: texts_log -->
```text
Line 1: [Grace Hopper]
Initials 1: [GH]
Lines processed: 1
Characters processed: 12
```

Case K, five short lines, after which the data ends:

<!-- input: texts_log -->
```text
Al
Bo
Cy
Di
Ed
```

<!-- output: texts_log -->
```text
Line 1: [Al]
Initials 1: [A]
Line 2: [Bo]
Initials 2: [B]
Line 3: [Cy]
Initials 3: [C]
Line 4: [Di]
Initials 4: [D]
Line 5: [Ed]
Initials 5: [E]
Lines processed: 5
Characters processed: 10
```

Case L, mixed letter case:

<!-- input: texts_log -->
```text
ada lovelace
ADA LOVELACE
ada Lovelace

```

<!-- output: texts_log -->
```text
Line 1: [ada lovelace]
Initials 1: [al]
Line 2: [ADA LOVELACE]
Initials 2: [AL]
Line 3: [ada Lovelace]
Initials 3: [aL]
Lines processed: 3
Characters processed: 36
```

</details>

<details>
<summary>Section 8: the output before the fix, and the fixed program</summary>

Before the fix, set (a): `Ada Lovelace` and `Mary ann SMITH`, after which the data ends:

<!-- input: texts_log_count_bug -->
```text
Ada Lovelace
Mary ann SMITH
```

<!-- output: texts_log_count_bug -->
```text
Line 1: [Ada Lovelace]
Initials 1: [AL]
Line 2: [Mary ann SMITH]
Initials 2: [MaS]
Lines processed: 2
Characters processed: 26
```

Set (b): `Ada` and an empty line:

<!-- input: texts_log_count_bug -->
```text
Ada

```

<!-- output: texts_log_count_bug -->
```text
Line 1: [Ada]
Initials 1: [A]
Lines processed: 2
Characters processed: 3
```

| Attempt | Line read | `fail()` | `lines_processed` after `++` | `empty()` | Action |
|---|---|---|---|---|---|
| 1 | `Ada` | `false` | 1 | `false` | report `Line 1` |
| 2 | empty | `false` | **2** | `true` | the loop ends |

An empty first line:

<!-- input: texts_log_count_bug -->
```text

```

<!-- output: texts_log_count_bug -->
```text
Lines processed: 1
Characters processed: 0
```

- **The cause:** the program increases the counter after every successful read, before it checks whether the line is empty. The empty line at the end is a successful read, so it gets counted too, although it isn't a record. The `Line N` reports are correct, because the program prints nothing for an empty line. Only the summary is wrong. Setting the flag to `false` ends the loop, but doesn't undo the `++lines_processed;` that has already run.
- **Why set (a) doesn't reveal the bug:** the data ends without an empty line. The last attempt fails, and the counter doesn't grow after a failed read, so the summary is correct.
- **The fix:** move `++lines_processed;` into the branch for a non-empty line, before `characters_processed += line.size();`. The `else` branch then holds just an `if`, which can be written as `else if`.

The fixed program is the reference solution from section 7. For an empty first line it gives `Lines processed: 0` (case B), for `Ada` and an empty line `Lines processed: 1` (case C), and for set (a) the same report as before (case D). Neither version reads outside the text: the initials function is the same as in the reference solution.

</details>

**Previous lesson:** [Lesson 7.3: A function creates a new text](lesson_03_a_function_creates_a_new_text.en.md) · **Next lesson:** [Lesson 7.5: Parcel code check (the Module 7 test)](lesson_05_parcel_code_check.en.md) · [Course overview](../../README.en.md)

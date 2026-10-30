# Lesson 7.5: Parcel code check (the Module 7 test)

[Polski](lesson_05_parcel_code_check.md) · **English** · [Course overview](../../README.en.md)

> **Module 7, lesson 5: the test** · about 95–115 minutes, in two sessions
> **You need:** your `cpp-workspace` folder and the original `lesson_05_first_program` project.
> **Pilot version.** The reference solutions in this lesson are checked automatically on Windows, Ubuntu and macOS, with the given input data. Nothing grades your own work automatically: you check it yourself, against the criteria. Typing input in CLion's **Run** window is described without a manual check on every system.

## How this test works

This lesson introduces nothing new. You check whether you can design on your own a program that **reads successive texts, transforms them and checks their format**, then builds a report from the results of cooperating functions. You also analyse two short problems in code and explain your decisions.

The lesson has two parts:

- **Part A: the test.** Requirements, examples, tasks, questions and criteria. No hints and no solution code. Everything you need is from Modules 1–7.
- **Part B: checking and discussion.** Hints, the full list of check cases, the reference solution, fixes, answers and self-assessment. Go there after doing Part A, or when you consciously decide to stop trying on your own.

Looking at Part B, at earlier lessons or at your notes isn't a failure. What matters is that you **honestly note what you did on your own and what with help**. A suggested split into two sessions:

- **first:** analysing the requirements, designing both functions, writing them and checking them with test printouts, connecting them to the reading loop;
- **second:** the boundary cases, the full report, the empty line and the line of spaces, task 2, comparing with the solution, task 3 and the self-assessment.

**You may use:** CLion or the terminal, CMake and Ninja, as before; a `CMakeLists.txt` copied from the original `lesson_05_first_program`; case and trace tables, and temporary test printouts. You won't need the debugger. You don't need to end the data from the keyboard: you analyse the cases where the data ends without an empty line on paper.

---

# Part A: the test

## Task 1: Parcel code check

A parcel pickup point receives one submission after another. Each non-empty line contains one parcel code, typed by a person, sometimes with spaces: `A B - 1 2 3 4` instead of `AB-1234`. The program removes the spaces from each code, checks whether what's left has the required format, and prepares a report. It checks only how the text is built, not whether the parcel really exists.

**Preparation:** in `cpp-workspace`, create a folder `parcel_codes`, copy `CMakeLists.txt` from the original `lesson_05_first_program` into it, create an **empty** `main.cpp` and write the whole program on your own.

### The code format

Once the spaces are removed, a valid code has **exactly seven characters**: two capital letters, a hyphen and four digits, for example `AB-1234`. Indices count from 0, as in lesson 7.2:

| Index in C++ | Requirement |
|---|---|
| 0 | a capital letter from `A` to `Z` |
| 1 | a capital letter from `A` to `Z` |
| 2 | a hyphen `-` |
| 3 | a digit from `0` to `9` |
| 4 | a digit from `0` to `9` |
| 5 | a digit from `0` to `9` |
| 6 | a digit from `0` to `9` |

- Valid codes include `AB-1234`, `AA-0000`, `ZZ-9999` and `BC-0102`. The letters may repeat, and the digits may start with a zero.
- **Letter case matters.** The program doesn't turn lower-case letters into capitals, so `Ab-1234` and `ab-1234` are invalid.
- The four digits are four characters, not a number: you only check that each of them is a digit and stands in its place.

### Input data

- The program reads successive lines with `std::getline`. It asks no questions: after starting it, type the codes straight away, each on its own line.
- **Each non-empty line is one code.** Before checking the format, the program removes **all** ordinary spaces from the code, not only those at the start and the end. The lines `  AB-1234  `, `A B - 1 2 3 4` and `AA-00 00` give the codes `AB-1234`, `AB-1234` and `AA-0000`, so all three are valid. The original line stays unchanged.
- The reading ends after the **first empty line** or after a **failed read**, usually at the end of the data. The program doesn't read what comes after the empty line. It checks the last line before the end of the data, even when no end-of-line character ends it (lesson 7.4).
- **What data is possible.** The lines contain printable ASCII characters: letters, digits, ordinary spaces and punctuation, with no tabs and no Polish letters. You don't need to check these assumptions. Any character that doesn't fit the format, for example `_`, `!` or a lower-case letter, makes the code invalid.

### An empty line versus a line of spaces

This is the most important decision in this program:

- **An empty line** has length zero. It ends the reading: the program doesn't check it as a code, doesn't increase any counter, and prints the summary.
- **A line of spaces only**, for example three of them, isn't empty. It's one submitted code: once the spaces are removed, an empty text is left, which doesn't have the code format. So the program counts an invalid code and reads the next line.

So it's the **original line**, before the program removes its spaces, that decides whether the reading ends. An empty text left after removing the spaces doesn't end the reading.

### The report

For each checked code, the program prints one line straight away: `Code N: valid` or `Code N: invalid`. `N` is the code's number, from 1, given in order to every code, the invalid ones included.

After the reading ends, it prints three lines:

- `Codes processed: N`: the number of checked codes;
- `Valid codes: N`: the number of valid codes;
- `Invalid codes: N`: the number of invalid codes.

The number of checked codes always equals the number of valid codes plus the number of invalid ones. When there were no codes, all three numbers are 0. The program prints no other messages: neither the codes themselves nor any information about what ended the reading.

### The functions

The program has at least two functions of its own:

1. a function that creates from the text it gets a **new text without spaces**, with the other characters in the same order, and returns it by value; it builds the new text with `push_back`, as in lesson 7.3;
2. a function that answers, for a code **already without spaces**, whether it has the required format: it returns `true` or `false`.

**Requirements for the functions:**

- Both get the text through `const std::string&`. They read nothing, print nothing and don't change the text they get.
- **The function checking the format must not read a character outside the text.** It must work correctly for every text: empty, one character long, too short and too long. A character that belongs to the text has an index smaller than `size()` (lesson 7.2).
- You write the functions' names and headers on your own: choose the result type to fit the function's task. You may add helper functions of your own, but you don't have to.

`main` reads the lines with `std::getline` in a `while` loop with a `bool` flag, as in lesson 7.4. It recognises the end of the data, numbers the codes, calls both functions, prints each code's result, counts the codes and prints the summary. It doesn't repeat the functions' algorithms. The program doesn't store earlier lines and uses no variables declared outside functions. You may use `std::size_t` for the counters.

### Examples

**Example A:** six lines. The fifth is made of three spaces, and the sixth is empty.

<!-- input: parcel_codes -->
```text
AB-1234
A B - 1 2 3 4
Ab-1234
AB-123
   

```

<!-- output: parcel_codes -->
```text
Code 1: valid
Code 2: valid
Code 3: invalid
Code 4: invalid
Code 5: invalid
Codes processed: 5
Valid codes: 2
Invalid codes: 3
```

Code 2 is `AB-1234` once the spaces are removed. In code 3 the second letter is lower-case, code 4 has only three digits, and nothing is left of line 5 once its spaces are removed. The empty sixth line ends the reading.

**Example B:** the first line is empty. It's an empty line, not missing data.

<!-- input: parcel_codes -->
```text

```

<!-- output: parcel_codes -->
```text
Codes processed: 0
Valid codes: 0
Invalid codes: 0
```

**Example C:** a line of three spaces, then an empty line.

<!-- input: parcel_codes -->
```text
   

```

<!-- output: parcel_codes -->
```text
Code 1: invalid
Codes processed: 1
Valid codes: 0
Invalid codes: 1
```

**Example D:** `AB-1234`, an empty line and `ZZ-9999`. **Predict** the report before you write the program.

<!-- input: parcel_codes -->
```text
AB-1234

ZZ-9999
```

<details>
<summary>Standard output for example D</summary>

<!-- output: parcel_codes -->
```text
Code 1: valid
Codes processed: 1
Valid codes: 1
Invalid codes: 0
```

`ZZ-9999` has a valid format, but it comes after the empty line, so the program doesn't read it. Whether a code is valid doesn't matter when its line is already outside the processing.

</details>

### How to work

1. **Design both functions before you start writing `main`.** For each, write in one sentence its task, its parameter and its result type.
2. **Prepare a table of cases:** valid codes with `A`, `Z`, `0` and `9`; spaces at the start, at the end and in the middle; a lower-case letter; a digit instead of a letter; another character instead of the hyphen; a letter among the digits; a code that's too short and one that's too long; a hyphen alone; spaces only; an empty first line; a code after the empty line; data that ends without an empty line. For each, write down the expected result.
3. **Check each function on its own** with the test printouts from lesson 5.5, using texts written in the code:
   - removing spaces: spaces in different places, spaces only and an empty text, with the result in square brackets so that the spaces show;
   - checking the format: a few valid codes, codes with a mistake at different positions, too short ones, too long ones and an empty text. `bool` values print as `1` or `0`.
4. **Remove the test printouts** and connect the functions to the reading loop.
5. **Run the whole program** for examples A, B and C and for 1–2 other cases from your table. End each line with **Enter**, and type an empty line as **Enter** alone. In the terminal the lines you type mix with the report, because the program answers straight after each line. Analyse the cases where the data ends without an empty line on paper. Every case in the full list of check cases is checked automatically.

When the result matches, you can save the project in Git, as in lesson 1.5. Before you commit, check `git status`: only `main.cpp` and `CMakeLists.txt` go into the history.

## Task 2: Diagnostics

Do this task **after task 1**: both problems are about a function similar to your function checking the format.

<details>
<summary>Diagnostic A: the bound of the letter range</summary>

In `cpp-workspace`, create a folder `diagnosis_7`, copy `main.cpp` and `CMakeLists.txt` from the original `lesson_05_first_program` into it, and put the program below into `main.cpp`: you may type it or copy it. The program checks the function with two tests written in the code, like your test printouts. The requirement: indices 0 and 1 hold capital letters from `A` to `Z`, `A` and `Z` **included**.

<!-- example: letter_range_bug -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>

bool is_valid_code(const std::string& code) {
    if (code.size() != 7) {
        return false;
    }

    const bool first_is_capital{code[0] > 'A' && code[0] <= 'Z'};
    const bool second_is_capital{code[1] >= 'A' && code[1] <= 'Z'};
    const bool has_hyphen{code[2] == '-'};
    bool all_digits{true};

    for (std::size_t index{3}; index < code.size(); ++index) {
        const bool is_digit{code[index] >= '0' && code[index] <= '9'};

        if (!is_digit) {
            all_digits = false;
        }
    }

    return first_is_capital && second_is_capital && has_hyphen && all_digits;
}

int main() {
    const std::string first_test{"BC-1234"};
    const std::string second_test{"AB-1234"};

    std::cout << "Test BC-1234: " << is_valid_code(first_test) << "\n";
    std::cout << "Test AB-1234: " << is_valid_code(second_test) << "\n";
}
```

1. **Predict** the result of both tests. Both codes are valid by the requirements.
2. Run the program. Which test gives the result the requirements expect, and which doesn't?
3. Why doesn't the test `BC-1234` reveal the bug?
4. Find the condition that rejects `AB-1234`, and point to the wrong bound of the range in it.
5. Fix the condition.
6. Add a test of the code `AA-0000` and run the program again.
7. Add a test of the code `aB-1234`: a lower-case letter at the fixed position must still give `0`.

</details>

<details>
<summary>Diagnostic B: an index before the length check</summary>

You **only analyse this fragment on paper**: don't run it. It's the start of another version of the function checking the format:

<!-- fragment -->
```cpp
bool is_valid_code(const std::string& code) {
    const bool has_hyphen{code[2] == '-'};
    const bool last_is_digit{code[6] >= '0' && code[6] <= '9'};

    if (code.size() != 7) {
        return false;
    }

    // ...the other positions, then the result
}
```

Consider calling this function with the text `"AB-"`:

1. How many characters does this text have?
2. What indices do its characters have?
3. Why is the read `code[6]` wrong here?
4. Can you predict what the program will do with such a read?
5. Which check must come before reading the characters at specific positions?
6. Why should the length check come before checking the letters, the hyphen and the digits?

</details>

The results, fixes and answers are in Part B, in [Diagnostics: results and fixes](#diagnostics-results-and-fixes).

## Task 3: Explain your design

Answer briefly, in writing, referring to your own program from task 1:

1. Why does your program check whether the line is empty before it removes the spaces? Why is a line of spaces only an invalid code and not the end of the data?
2. Why is the code without spaces a separate `std::string`, while the original line stays unchanged?
3. Why does the function removing spaces return a text, while the function checking the format returns a `bool`?
4. Why does your function checking the format know the code's length before it reads any character? For which codes in your table does that order matter?
5. Why doesn't the program need to store all the codes?
6. Does the number of checked codes being equal to the valid ones plus the invalid ones prove that every code was judged correctly?

## Success criteria

You pass the test when you meet **all** the criteria. You may use Part B while doing so, as long as you note it honestly in the self-assessment.

- `parcel_codes/main.cpp` was written from an empty file, in valid C++20. The program builds without errors.
- The program reads the lines with `std::getline` in a `while` loop with a `bool` flag, checks the read's success before `empty()`, and ends the reading after the first empty line or after a failed read.
- There are two functions with the tasks from the requirements. Both get the text through `const std::string&`, read and print nothing, and don't change the text they get. The result type of each fits its task.
- The function removing spaces builds a new text with `push_back` and removes every space, also from the middle of the code. The function checking the format reads no character outside the text, also for an empty text and for codes shorter than seven characters.
- A line of spaces only is counted as an invalid code, and the original line decides whether the reading ends. The program doesn't store earlier lines.
- The standard output for examples A, B and C and for the cases you typed matches the requirements. The cases that end without an empty line match your analysis on paper and the full list of check cases.
- The functions were checked on their own with test printouts, and the final program contains no such printouts.
- The bug in diagnostic A was fixed and the fix was checked, and the fragment in diagnostic B was analysed without running it.
- You can explain every line of your program and answer the questions in task 3.

The names of the functions and variables, and the split of the program, may differ from the reference solution, as long as they're readable and meet the requirements. A correct result is a necessary condition, but **not proof of understanding**. That's why tasks 2 and 3 are part of the test.

---

# Part B: checking and discussion

Come here after doing Part A, or when you consciously decide to stop trying on your own.

## How to check your work

- **Standard output:** compare the program's lines with the expected ones, character by character. Ignore the lines you type: you see them in the terminal, but they aren't part of the program's standard output.
- **End of the data:** check the cases that end without an empty line with a trace table, and compare them with the full list of check cases. Each of them is checked automatically there.
- **Functions:** does each have a task you can describe in one sentence? Does some algorithm also appear in `main`?
- **Order:** does the original line decide whether the reading ends? Does the function checking the format know the code's length before it reads the first character?

## Hints

<details>
<summary>Hint 1</summary>

Which tasks of the program can separate functions do? Are removing spaces and checking the format the same responsibility?

</details>

<details>
<summary>Hint 2</summary>

First decide whether the original line ends the reading. If it doesn't, create the text without spaces, and check the format only on that text.

</details>

<details>
<summary>Hint 3</summary>

Before reading characters by their indices, check that the code has exactly seven characters. Then examine the two places for capital letters, the one for the hyphen and the four for digits.

</details>

## The full list of check cases

<details>
<summary>Open it after preparing your own table</summary>

Examples A–D are checked in Part A. Every case below is checked automatically, with the reference solution, which reads the data from the input itself. Each case is a separate run of the program.

**Valid codes**, all in one input, in case E:

| Line | Code without spaces | What it checks |
|---|---|---|
| `AB-1234` | `AB-1234` | an ordinary valid code |
| `AA-0000` | `AA-0000` | `A` twice, zeros only |
| `ZZ-9999` | `ZZ-9999` | `Z` twice, nines only |
| `BC-0102` | `BC-0102` | a zero at the start of the digits |
| `  AB-1234  ` | `AB-1234` | two spaces at the start and two at the end |
| `A B - 1 2 3 4` | `AB-1234` | spaces between all the characters |
| `AA-00 00` | `AA-0000` | a space among the digits |

**Invalid codes**, all in one input, in case F:

| Line | Why it's invalid |
|---|---|
| `Ab-1234` | a lower-case letter at index 1 |
| `ab-1234` | two lower-case letters |
| `aB-1234` | a lower-case letter at index 0 |
| `A1-1234` | a digit instead of the second letter |
| `AB_1234` | `_` instead of the hyphen |
| `AB-123` | too short: 6 characters |
| `AB-12345` | too long: 8 characters |
| `AB-A234` | a letter at index 3, the first of the digits |
| `AB-12A4` | a letter among the digits, at index 5 |
| `AB-123A` | a letter at index 6, the last one |
| `AB-1234!` | an extra character: 8 characters |
| `-` | one character |
| three spaces | an empty text is left once the spaces are removed |

**Processing many lines:**

| | Input | Code results | Checked, valid, invalid | What it checks |
|---|---|---|---|---|
| A | example A | valid, valid, invalid, invalid, invalid | 5, 2, 3 | the data from Part A |
| B | an empty line | — | 0, 0, 0 | an empty first line |
| C | three spaces, an empty line | invalid | 1, 0, 1 | spaces only are a code, not the end of the data |
| D | `AB-1234`, an empty line, `ZZ-9999` | valid | 1, 1, 0 | nothing is read after the empty line |
| E | seven valid codes, an empty line | valid 7 times | 7, 7, 0 | the table of valid codes |
| F | thirteen invalid codes, an empty line | invalid 13 times | 13, 0, 13 | the table of invalid codes; a rejected code doesn't end the reading |
| G | `AB-123`, `ZZ-9999`, `A1-1234`, `AA-00 00`, an empty line | invalid, valid, invalid, valid | 4, 2, 2 | a valid code after an invalid one |
| H | `BC-0102`, an empty line | valid | 1, 1, 0 | one valid code |
| I | `AB-12345`, an empty line | invalid | 1, 0, 1 | one invalid code |
| J | `AB-1234`, the end of the data | valid | 1, 1, 0 | the end of the data after one code |
| K | `ZZ-9999`, `AB_1234`, `A B - 1 2 3 4`, the end of the data | valid, invalid, valid | 3, 2, 1 | the end of the data after several codes |
| L | `AB-1234`, one space, `BC-0102`, an empty line | valid, invalid, valid | 3, 2, 1 | a line with a space in the middle of the data doesn't end the reading |

**Automatic tests and your own runs.** In cases J and K the data ends after the last line given. The empty line in case B is one end-of-line character, not missing data. The tests don't run a last line without an end-of-line character, because in them every line ends with an end-of-line character.

Case E, seven valid codes:

<!-- input: parcel_codes -->
```text
AB-1234
AA-0000
ZZ-9999
BC-0102
  AB-1234  
A B - 1 2 3 4
AA-00 00

```

<!-- output: parcel_codes -->
```text
Code 1: valid
Code 2: valid
Code 3: valid
Code 4: valid
Code 5: valid
Code 6: valid
Code 7: valid
Codes processed: 7
Valid codes: 7
Invalid codes: 0
```

Case F, thirteen invalid codes:

<!-- input: parcel_codes -->
```text
Ab-1234
ab-1234
aB-1234
A1-1234
AB_1234
AB-123
AB-12345
AB-A234
AB-12A4
AB-123A
AB-1234!
-
   

```

<!-- output: parcel_codes -->
```text
Code 1: invalid
Code 2: invalid
Code 3: invalid
Code 4: invalid
Code 5: invalid
Code 6: invalid
Code 7: invalid
Code 8: invalid
Code 9: invalid
Code 10: invalid
Code 11: invalid
Code 12: invalid
Code 13: invalid
Codes processed: 13
Valid codes: 0
Invalid codes: 13
```

Case G, valid codes alternating with invalid ones:

<!-- input: parcel_codes -->
```text
AB-123
ZZ-9999
A1-1234
AA-00 00

```

<!-- output: parcel_codes -->
```text
Code 1: invalid
Code 2: valid
Code 3: invalid
Code 4: valid
Codes processed: 4
Valid codes: 2
Invalid codes: 2
```

Case H, one valid code:

<!-- input: parcel_codes -->
```text
BC-0102

```

<!-- output: parcel_codes -->
```text
Code 1: valid
Codes processed: 1
Valid codes: 1
Invalid codes: 0
```

Case I, one invalid code:

<!-- input: parcel_codes -->
```text
AB-12345

```

<!-- output: parcel_codes -->
```text
Code 1: invalid
Codes processed: 1
Valid codes: 0
Invalid codes: 1
```

Case J, one code, after which the data ends:

<!-- input: parcel_codes -->
```text
AB-1234
```

<!-- output: parcel_codes -->
```text
Code 1: valid
Codes processed: 1
Valid codes: 1
Invalid codes: 0
```

Case K, three codes, after which the data ends:

<!-- input: parcel_codes -->
```text
ZZ-9999
AB_1234
A B - 1 2 3 4
```

<!-- output: parcel_codes -->
```text
Code 1: valid
Code 2: invalid
Code 3: valid
Codes processed: 3
Valid codes: 2
Invalid codes: 1
```

Case L, a line of one space between two codes:

<!-- input: parcel_codes -->
```text
AB-1234
 
BC-0102

```

<!-- output: parcel_codes -->
```text
Code 1: valid
Code 2: invalid
Code 3: valid
Codes processed: 3
Valid codes: 2
Invalid codes: 1
```

</details>

## The reference solution

<details>
<summary>Task 1: parcel code check</summary>

<!-- example: parcel_codes -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>

std::string without_spaces(const std::string& text) {
    std::string result{};

    for (const char symbol : text) {
        if (symbol != ' ') {
            result.push_back(symbol);
        }
    }

    return result;
}

bool is_valid_code(const std::string& code) {
    if (code.size() != 7) {
        return false;
    }

    const bool first_is_capital{code[0] >= 'A' && code[0] <= 'Z'};
    const bool second_is_capital{code[1] >= 'A' && code[1] <= 'Z'};
    const bool has_hyphen{code[2] == '-'};
    bool all_digits{true};

    for (std::size_t index{3}; index < code.size(); ++index) {
        const bool is_digit{code[index] >= '0' && code[index] <= '9'};

        if (!is_digit) {
            all_digits = false;
        }
    }

    return first_is_capital && second_is_capital && has_hyphen && all_digits;
}

int main() {
    bool reading{true};
    std::size_t codes_processed{0};
    std::size_t valid_codes{0};
    std::size_t invalid_codes{0};

    while (reading) {
        std::string line{};
        std::getline(std::cin, line);

        if (std::cin.fail()) {
            reading = false;
        } else if (line.empty()) {
            reading = false;
        } else {
            const std::string code{without_spaces(line)};
            const bool valid{is_valid_code(code)};

            ++codes_processed;

            if (valid) {
                ++valid_codes;
                std::cout << "Code " << codes_processed << ": valid\n";
            } else {
                ++invalid_codes;
                std::cout << "Code " << codes_processed << ": invalid\n";
            }
        }
    }

    std::cout << "Codes processed: " << codes_processed << "\n";
    std::cout << "Valid codes: " << valid_codes << "\n";
    std::cout << "Invalid codes: " << invalid_codes << "\n";
}
```

| Function | Task | Parameter | Result |
|---|---|---|---|
| `without_spaces` | a new text: every character except the spaces, in the same order | the text through `const&` | `std::string` |
| `is_valid_code` | whether the text has the code format: seven characters, two capital letters, a hyphen and four digits | the code without spaces through `const&` | `bool` |
| `main` | reading the lines, the end of the reading, numbering, calling the functions, the counters and the whole report | — | — |

**Data flow for code 2 in example A:**

| Step | What happens |
|---|---|
| 1 | `std::getline` reads the second line, `A B - 1 2 3 4`: 13 characters, spaces included. |
| 2 | `std::cin.fail()` gives `false`: the read succeeded. |
| 3 | `line.empty()` gives `false`: the original line isn't empty, so it's a code to check. |
| 4 | `main` passes `line` to `without_spaces`. |
| 5 | The function returns a new text, `AB-1234`, which `main` stores in `code`. `line` doesn't change. |
| 6 | `main` passes `code` to `is_valid_code`. `code.size()` gives 7, so the guard clause doesn't end the function. |
| 7 | `code[0]` is `A` and `code[1]` is `B`: both are capital letters. |
| 8 | `code[2]` is `-`. |
| 9 | The loop from index 3 to 6 reads `1`, `2`, `3` and `4`. They're all digits, so `all_digits` stays `true`. |
| 10 | The function returns `true`, and `main` stores that result in `valid`. |
| 11 | `codes_processed` grows to 2, and so does `valid_codes`. |
| 12 | `main` prints `Code 2: valid` and reads the next line. |

**Discussion:**

1. **The read's success first.** `std::cin.fail()` is checked first, because after a failed read you can't rely on what `line` holds (lesson 7.4).
2. **The end of the reading depends on the original line.** `line.empty()` comes before the call to `without_spaces`. An empty line is the agreed end signal, and that signal is about the line the user typed, not about the text after it was transformed.
3. **Spaces only are a submitted code.** The line `"   "` has three characters, so `empty()` gives `false` and the program checks it as a code. If the text without spaces decided whether the reading ends, this line would end it. Cases A, C, F and L check this.
4. **A new text.** The code without spaces is a different text from the line: it has other characters and another length. `without_spaces` builds it in the local `result` with `push_back`, as in lesson 7.3, and returns it by value.
5. **The original stays unchanged.** The function gets the line through `const std::string&`, so it can only read it: a program that tried to change the parameter wouldn't build. The input and the text to check are two separate objects: `line` and `code`.
6. **Removing spaces first, then the format.** The format rule is about the code without spaces. `A B - 1 2 3 4` has 13 characters, and only once its spaces are removed does it have 7 characters that match the format.
7. **A `bool` result.** The question "does the code have the required format?" has two answers: yes or no. The function only answers, and `main` decides what to print and which counter to increase. That's why you can check the function with test printouts, without the whole program, as in lesson 5.5.
8. **The length first.** The guard clause `if (code.size() != 7)` from lesson 5.4 ends the function before it reads any character. After it, every index from 0 to 6 is known to exist. Codes that are too short, a hyphen alone and an empty text get `false` without any character being read.
9. **The positions.** At indices 0 and 1 the function checks the range from `'A'` to `'Z'`, as in lesson 7.1. At index 2 it compares the character with `'-'`. The loop from index 3 to the last one sets `all_digits` to `false` for every character outside the range from `'0'` to `'9'`. The function returns `true` only when all four conditions hold.
10. **Lower-case letters.** Capital and lower-case letters are two separate ASCII ranges (lesson 7.1). `'b'` doesn't fit into the range from `'A'` to `'Z'`, so `Ab-1234` is invalid. The program changes nothing: it checks each character exactly as it stands in the code.
11. **Three counters.** `codes_processed` grows for every checked code and gives its number. Exactly one of the other two counters grows with it: in the `if` branch or in the `else` branch. That's why `codes_processed` always equals `valid_codes + invalid_codes`.
12. **An empty code is invalid.** Removing the spaces from `"   "` leaves an empty text. Its `size()` gives 0, so the guard clause returns `false` before the function reads `code[0]`. An empty text is a correct result of removing spaces (lesson 7.3), but not a valid code.
13. **The last line at the end of the data.** When the data ends right after a line's last character, with no end-of-line character, `getline` still delivers that line, and `fail()` gives `false`. The program checks it, and only the next, failed attempt ends the loop (lesson 7.4).
14. **No vector.** Each code's result is ready right after it's read, and the summary needs only three numbers. No decision needs earlier lines, so a vector of texts isn't needed.

**Other correct layouts.** This is one possible split. Each position can also be checked with its own guard clause, for example `if (code[2] != '-') { return false; }`, and the four digits with four conditions instead of a loop. The length can be checked in the same condition as the characters: in `code.size() == 7 && code[0] >= 'A' && ...` the short-circuit evaluation from lesson 3.4 reads the characters only when the length is right. You may add a small helper function that gets one `char` and answers whether it's a capital letter. In `main`, `codes_processed` may grow at the start of the processing branch, as in lesson 7.4, and the two end conditions may be joined into `if (std::cin.fail() || line.empty())`. What matters is that the original line decides whether the reading ends, and that the length is known before the first character is read.

</details>

## Diagnostics: results and fixes

<details>
<summary>Diagnostic A: the bound of the letter range</summary>

Before the fix:

<!-- output: letter_range_bug -->
```text
Test BC-1234: 1
Test AB-1234: 0
```

- Both codes are valid by the requirements, so both tests should give `1`.
- `BC-1234` doesn't reveal the bug: its first letter is `B`, and `B` is greater than `A`, so the wrong condition lets it through.
- `AB-1234` reveals the bug: `'A' > 'A'` gives `false`, so the function rejects a valid code.
- **The cause:** the condition `code[0] > 'A'` leaves out the lower bound of the range. The bug affects only the letter `A` at index 0: every other capital letter passes.
- **The fix:** `code[0] >= 'A' && code[0] <= 'Z'`, as for index 1.

After the fix, with the added tests:

<!-- example: letter_range_fixed -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>

bool is_valid_code(const std::string& code) {
    if (code.size() != 7) {
        return false;
    }

    const bool first_is_capital{code[0] >= 'A' && code[0] <= 'Z'};
    const bool second_is_capital{code[1] >= 'A' && code[1] <= 'Z'};
    const bool has_hyphen{code[2] == '-'};
    bool all_digits{true};

    for (std::size_t index{3}; index < code.size(); ++index) {
        const bool is_digit{code[index] >= '0' && code[index] <= '9'};

        if (!is_digit) {
            all_digits = false;
        }
    }

    return first_is_capital && second_is_capital && has_hyphen && all_digits;
}

int main() {
    const std::string first_test{"BC-1234"};
    const std::string second_test{"AB-1234"};
    const std::string third_test{"AA-0000"};
    const std::string fourth_test{"aB-1234"};

    std::cout << "Test BC-1234: " << is_valid_code(first_test) << "\n";
    std::cout << "Test AB-1234: " << is_valid_code(second_test) << "\n";
    std::cout << "Test AA-0000: " << is_valid_code(third_test) << "\n";
    std::cout << "Test aB-1234: " << is_valid_code(fourth_test) << "\n";
}
```

<!-- output: letter_range_fixed -->
```text
Test BC-1234: 1
Test AB-1234: 1
Test AA-0000: 1
Test aB-1234: 0
```

`AA-0000` checks the letter `A` at both positions and the digit `0`. `aB-1234` checks that the fix didn't go too far: in ASCII the lower-case `a` comes after all the capital letters, so the upper bound `<= 'Z'` still rejects it. The function in the fixed program is the same as in the reference solution. Neither version reads outside the text, because the length is checked before the first character is read.

</details>

<details>
<summary>Diagnostic B: an index before the length check</summary>

1. Three: `size()` gives 3.
2. 0, 1 and 2. They hold `A`, `B` and `-`.
3. A character that belongs to the text has an index smaller than `size()`, here smaller than 3. Index 6 is greater than `size()`, so there's no such character, and in C++20 such a read is undefined behaviour (lesson 7.2). The read `code[2]` in the first line is fine: index 2 belongs to the text.
4. No. The language standard doesn't say what happens then. The program may give a random result, end with an error, or seem to work correctly, and behave differently on another computer. The fragment builds, because the compiler doesn't check indices (lesson 6.3). That's why we don't run such code "to see what comes out".
5. The length check: `if (code.size() != 7)` with `return false;`, the guard clause from lesson 5.4. After it, every index from 0 to 6 is known to exist.
6. Because every check of a letter, the hyphen or a digit reads a character. The program runs the statements in order, so a length check further down won't undo a read that has already happened. Codes that are too short are ordinary data: `AB-123`, a hyphen alone, or an empty text from a line of spaces. Only when the length is 7 do all the indices from 0 to 6 belong to the text.

The safe version of this start has the guard clause before the first character is read, like the reference solution:

<!-- fragment -->
```cpp
bool is_valid_code(const std::string& code) {
    if (code.size() != 7) {
        return false;
    }

    const bool has_hyphen{code[2] == '-'};
    const bool last_is_digit{code[6] >= '0' && code[6] <= '9'};

    // ...the other positions, then the result
}
```

</details>

## Answers to task 3

<details>
<summary>Sample answers</summary>

1. Because only the original tells an empty line from a line of spaces: the empty one has length zero, and `"   "` has three characters. Once the spaces are removed, both give an empty text. If the program checked for the end only on the text without spaces, the line of spaces would end the reading, and the next codes wouldn't be checked. Such a line is a submitted code: someone typed something in it. Once its spaces are removed, no character is left, and an empty text doesn't have seven characters, so it's an invalid code.
2. Because it's a different text from the line: it has other characters and another length. The function builds it from scratch and returns it, and the line stays as it was typed, because the function gets it through `const&` and can only read it.
3. Because the first function creates a new text, so its result is a `std::string`. The second answers a question that has only two answers, yes or no, so its result is a `bool`. `main` decides, based on that answer, what to print and which counter to increase.
4. Because a character can be read only when its index is smaller than `size()`, and only at length 7 do all the indices from 0 to 6 exist. The order matters for codes shorter than seven characters, for example `AB-123`, `-` or the empty text from a line of spaces. For them, index 6 doesn't belong to the text. The length check also rejects codes that are too long, like `AB-12345`, but their characters at indices 0 to 6 exist.
5. Because each code's result is ready right after it's read, and the summary needs only three counters. No later decision needs the earlier codes.
6. No. The equality says only that every checked code went into exactly one of the two groups. The function from diagnostic A puts `AB-1234` among the invalid codes, and the counters still add up. Only cases with expected results check that the judgement is correct.

</details>

## Self-assessment

For each criterion, mark one answer:

| Criterion | On my own | With a hint | After looking at the solution | To revise |
|---|---|---|---|---|
| Splitting the program into two functions and `main` | | | | |
| A new text without spaces, built with `push_back` | | | | |
| Checking the length before reading characters | | | | |
| Capital letters, the hyphen and the digits at the right positions | | | | |
| The reading loop: the empty line and the end of the data | | | | |
| A line of spaces only as an invalid code | | | | |
| Numbering the codes and the three counters | | | | |
| Test printouts of the functions | | | | |
| A table of cases | | | | |
| Diagnostic A (the bound of the letter range) | | | | |
| Diagnostic B (an index before the length check) | | | | |
| The explanations in task 3 | | | | |

If anything is marked in the "To revise" column, go back to the relevant lesson:

| Topic | Lesson |
|---|---|
| `char`, comparing characters and ASCII ranges | [7.1](lesson_01_first_characters.en.md) |
| indices, `std::size_t` and characters that belong to the text | [7.2](lesson_02_positions_and_neighbours.en.md) |
| a function that gets `const std::string&` and creates a new text | [7.3](lesson_03_a_function_creates_a_new_text.en.md) |
| successive lines, the empty line and the end of the data | [7.4](lesson_04_successive_lines.en.md) |
| several `return` statements and the guard clause | [5.4](../module_05_functions/lesson_04_several_returns.en.md) |
| functions returning `bool`, splitting responsibilities and test printouts | [5.5](../module_05_functions/lesson_05_several_functions.en.md) |
| short-circuit evaluation of `&&` and `\|\|` | [3.4](../module_03_decisions_and_conditions/lesson_04_combining_conditions.en.md) |
| reading out of range and undefined behaviour | [6.3](../module_06_collections/lesson_03_positions_and_neighbours.en.md) |

Then try the task again, for example with a different code format: three capital letters, a hyphen and three digits.

---

## Module 7 summary

After five lessons, you can:

- tell a `char` character from a `std::string` text, and the literal `'A'` from `"A"`;
- go through a text character by character and recognise capital and lower-case letters, digits and other characters in ASCII text;
- read characters through an index of type `std::size_t`, only within the text, and compare neighbouring characters;
- write functions that get a text through `const std::string&` and return a new `std::string`;
- read successive lines with `std::getline` and tell an empty line from a failed read;
- design programs that read successive texts, transform them, check their format and build a report from the results of cooperating functions.

This module showed three kinds of work with text. They don't exclude each other: one program often combines several of them.

| Kind of work | Question | Example from the module | Typical result |
|---|---|---|---|
| analysing an existing text | what is in the text? | kinds of characters (7.1), neighbouring characters (7.2) | numbers or a report |
| building a new text | what new text to build from the given one? | initials (7.3), a text without spaces (7.5) | a new `std::string` |
| checking that a text is valid | does the text meet the rules? | a parcel code (7.5) | `true` or `false` |

Lesson 7.4 doesn't add a fourth kind: it organises the processing of many lines, and each of them can be analysed, transformed or checked. The test combines everything in one program: for each line it builds a text without spaces, checks its format and counts the results.

All of this is about ASCII text. Text has many more possibilities, which you'll meet in later modules.

## What's next

In Module 8, "Your own data types: `struct` and records", you'll define your own type that joins several pieces of information about one object. Start with your first struct: [Lesson 8.1: Your first struct: several pieces of data describing one object](../module_08_structs/lesson_01_first_struct.en.md).

**Previous lesson:** [Lesson 7.4: Processing successive lines with `std::getline`](lesson_04_successive_lines.en.md) · **Next lesson:** [Lesson 8.1: Your first struct: several pieces of data describing one object](../module_08_structs/lesson_01_first_struct.en.md) · [Course overview](../../README.en.md)

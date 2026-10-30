# Lesson 7.1: First characters: `char` and going through a `std::string`

[Polski](lesson_01_first_characters.md) · **English** · [Course overview](../../README.en.md)

> **Module 7, lesson 1** · about 60–75 minutes
> **You need:** your `cpp-workspace` folder and the original `lesson_05_first_program` project, as before. You won't need the debugger in this lesson.
> **Pilot version.** The programs in this lesson are checked automatically on Windows, Ubuntu and macOS, including with the given input data. Typing input in CLion's **Run** window is described without a manual check on every system.

## Before you start

This lesson assumes that you:

- store text in a `std::string` variable and know that it needs `#include <string>` (lesson 2.7);
- combine conditions with the `&&` and `||` operators (lesson 3.4);
- go through a vector with a range-based loop and get `size()` and `empty()` (lessons 6.1 and 6.2);
- count events with a counter (lesson 4.2).

## The situation

In lesson 6.1, a range-based loop went through the successive elements of a vector:

<!-- fragment -->
```cpp
const std::vector<int> numbers{3, 7, 5};

for (const int number : numbers) {
    std::cout << number << "\n";
}
```

Text is made of successive elements too: `"ABC"` is A, then B, then C. But a program that knows only the whole text can't answer questions about its inside: how many digits are in it? how many letters? are there spaces?

**Can a text be gone through like the elements of a vector?** Yes. A `std::string` also lets you go through its successive elements, and each of them is one **character**, a value of a new type, `char`. `std::string` is a different type from `std::vector`, but the way of going through it is similar.

After this lesson you will:

- write variables of type `char` and tell `'A'` from `"A"`;
- explain that a `std::string` stores a sequence of `char` elements;
- go through a text character by character with a range-based loop, spaces and punctuation included;
- get the number of elements of a text with `size()` and check for an empty text with `empty()`;
- recognise capital and lower-case letters, digits and other characters in ASCII text;
- explain why this analysis is correct only for ASCII text.

## 1. Prepare the project

In `cpp-workspace`, create a folder `lesson_7_1` and copy `main.cpp` and `CMakeLists.txt` from the original `lesson_05_first_program` into it. You type the programs from sections 2–7 into `main.cpp` in this folder.

## 2. Your first `char`

<!-- example: first_chars -->
```cpp
#include <iostream>
#include <string>

int main() {
    const char first{'A'};
    const char second{'7'};
    const char third{'!'};
    const std::string text{"A"};

    std::cout << first << "\n";
    std::cout << second << "\n";
    std::cout << third << "\n";
    std::cout << text << " has " << text.size() << " element\n";
}
```

<!-- output: first_chars -->
```text
A
7
!
A has 1 element
```

- **`char`** is a type that stores **one character**. `'A'` is a letter, `'!'` is a punctuation mark.
- **`'7'` is a character, not the number 7.** Compare `const int number{7};` and `const char digit{'7'};`. Both values print as `7`, but they serve different purposes: `int` for counting, `char` for writing a character in a text. We'll come back to turning a digit character into a number later in the course.
- `std::cout` prints a `char` as a character, just like text.

## 3. Apostrophes and quotation marks

| Notation | What it is |
|---|---|
| `'A'` | a **character literal** in apostrophes: one character, type `char` |
| `"A"` | a **text literal** (string literal) in quotation marks: a text, here one character long |

- A `std::string` can be created from the text literal `"A"`, as in `const std::string text{"A"};` above. But the literal `"A"` itself **is not** of type `std::string`: it's fixed text from the code, from which a `std::string` is then created.
- A `std::string` can contain one character, like `text` above, many characters, or none.
- **Apostrophes: always exactly one character.** Quotation marks: a text of any length.

**Predict** whether this program builds:

<!-- broken: char_from_text at=5:23 errors=1 error=^cannot initialize a variable of type 'const char' with an lvalue of type 'const char\[2\]' -->
```cpp
#include <iostream>
#include <string>

int main() {
    const char symbol{"A"};

    std::cout << symbol << "\n";
}
```

<details>
<summary>What the compiler reports, and why</summary>

The program won't build. On line 5, the compiler reports `cannot initialize a variable of type 'const char' with an lvalue of type 'const char[2]'`: a `char` variable can't be initialised with a text literal. `"A"` is a text, not a single character. The notation `const char[2]` means that this literal stores two elements: the letter A and an invisible character that ends the text. For now, it's enough to remember that it isn't a `char`.

**The fix:** when you need one character, use apostrophes: `const char symbol{'A'};`.

</details>

## 4. A range-based loop over a text

<!-- example: cat_letters -->
```cpp
#include <iostream>
#include <string>

int main() {
    const std::string text{"Cat"};

    for (const char symbol : text) {
        std::cout << symbol << "\n";
    }
}
```

**Predict** how many lines the program prints, and in what order. Then run it.

<details>
<summary>Standard output</summary>

<!-- output: cat_letters -->
```text
C
a
t
```

</details>

It's the same range-based loop as in lesson 6.1, only over a text:

- `text` has three elements, so the body runs three times;
- `symbol` gets the values `'C'`, `'a'` and `'t'` in turn, in the order of the text;
- the type of the loop variable is the type of the text's elements: `char`. `const`, because the body only reads the character;
- there's no counter or index to look after.

## 5. Spaces and other characters

Spaces and punctuation are elements of the text too. This program puts each element in square brackets, so that a space is visible:

<!-- example: bracketed -->
```cpp
#include <iostream>
#include <string>

int main() {
    const std::string text{"A 7!"};

    std::cout << "Elements: " << text.size() << "\n";

    for (const char symbol : text) {
        std::cout << "[" << symbol << "]\n";
    }
}
```

**Predict** the number of elements and every line of output.

<details>
<summary>Standard output</summary>

<!-- output: bracketed -->
```text
Elements: 4
[A]
[ ]
[7]
[!]
```

</details>

The text `"A 7!"` has **four** elements: `A`, a space, `7` and `!`. A space doesn't disappear while going through the text: it's an ordinary character, just invisible without the brackets.

`text.size()` gives the number of elements of a text, as for a vector. There's no need to count characters with a separate counter.

## 6. An empty text

<!-- example: empty_text -->
```cpp
#include <iostream>
#include <string>

int main() {
    const std::string empty_text{};

    std::cout << "Elements: " << empty_text.size() << "\n";

    if (empty_text.empty()) {
        std::cout << "The text is empty\n";
    }

    for (const char symbol : empty_text) {
        std::cout << "[" << symbol << "]\n";
    }

    std::cout << "Done\n";
}
```

**Predict** how many times the loop body runs.

<details>
<summary>Standard output</summary>

<!-- output: empty_text -->
```text
Elements: 0
The text is empty
Done
```

</details>

Empty `{}` create a text with no elements. `size()` gives 0, `empty()` gives `true`, and the range-based loop makes no passes, as for an empty vector in lesson 6.1. An empty text is a valid case that has to be taken into account.

## 7. The boundary: ASCII text

In this lesson we analyse **ASCII** text: English letters, digits, the space and basic punctuation. For such text, one `char` element is one character. A `std::string` can also store text with Polish letters, but it doesn't recognise them by itself. In the common UTF-8 encoding, a letter such as `ż` takes **several** `char` elements. For such text, `size()` gives the number of `char` elements, not the number of letters a person sees, the range-based loop reads one letter as several elements, and the comparisons in this lesson don't recognise Polish letters. That's a deliberate limit of this lesson, not a mistake. That's why all the data in the tasks is ASCII.

## 8. Recognising digits

Characters can be compared like numbers: `<`, `>`, `<=`, `>=`, `==`. The digits from `'0'` to `'9'` follow one another in order, so the condition `symbol >= '0' && symbol <= '9'` is true exactly for a digit:

<!-- example: room_digits -->
```cpp
#include <iostream>
#include <string>

int main() {
    const std::string label{"Room 12"};
    int digits{0};

    for (const char symbol : label) {
        if (symbol >= '0' && symbol <= '9') {
            ++digits;
        }
    }

    std::cout << "Digits: " << digits << "\n";
}
```

**Predict** the result and run the program.

<details>
<summary>Standard output</summary>

<!-- output: room_digits -->
```text
Digits: 2
```

</details>

- The loop goes through seven elements: `R`, `o`, `o`, `m`, a space, `1` and `2`.
- The counter grows only for `'1'` and `'2'`.
- We compare **characters**: `'0'` and `'9'` stand in apostrophes. Without apostrophes, `0` and `9` would be `int` numbers, which is something else.

In ASCII text you recognise a capital letter of the English alphabet, from `'A'` to `'Z'`, and a lower-case one, from `'a'` to `'z'`, the same way: the letters in each of those ranges also follow one another in order. But capital and lower-case letters are **two separate ranges**. Every character that is neither a letter nor a digit is an "other" character: a space, a hyphen, an exclamation mark and every other punctuation mark.

## 9. Mission: a character report

The program prepares a report on the contents of a short message. The message is written in the code and contains only ASCII characters:

<!-- fragment -->
```cpp
const std::string message{"Box 7 - ready!"};
```

**Requirements:**

- The program prints four lines:
  - `Characters: N`: the number of all the elements of the message;
  - `Letters: N`: the number of letters of the English alphabet, capital and lower-case;
  - `Digits: N`: the number of digits;
  - `Other: N`: the number of other characters: spaces, hyphens, exclamation marks and other punctuation.
- **Every element of the message belongs to exactly one category:** a letter, a digit or other. So the sum of the three categories equals the number of all the elements.
- The program uses `std::string`, a range-based loop with a `const char` variable, `int` counters and `size()`. It doesn't change the message, reads nothing from the input and uses no extra libraries.
- After changing only the message in the braces, the program gives a correct report for the new ASCII text, an empty one included.

In `cpp-workspace`, create a folder `message_report`, copy `CMakeLists.txt` from the original `lesson_05_first_program` into it, create an empty `main.cpp` and write the program on your own.

For the message above, the standard output must be:

<!-- output: message_report -->
```text
Characters: 14
Letters: 8
Digits: 1
Other: 5
```

There are 8 letters: three in `Box` and five in `ready`. There's one digit, `7`. There are 5 other characters: three spaces, a hyphen and an exclamation mark.

**This isn't the program from section 8 with different messages.** There, there was one counter and one condition. You have to decide on your own:

1. how to recognise a letter, given that capital and lower-case letters are two ranges;
2. in what order to check the categories, so that no character increases two counters;
3. how to recognise an "other" character without listing every possible punctuation mark;
4. where to get the number of all the elements from;
5. how to check that the report adds up.

**Before you write the program**, prepare a table of cases: the message from the requirements, an empty text, only capital letters, only lower-case letters, only digits, only spaces and hyphens, one character from each category, and a character that is neither a letter nor a digit, for example `_`. For each, write down the four numbers of the report.

**Then:** run the program for the message from the requirements, and then change the message to 3–4 cases from your table, for example an empty text, `AbC`, `019` and ` -- `. Every case in the full list of check cases is checked automatically, so you don't need to type them all.

### Success criteria

- The program builds as C++20 and, for the message from the requirements, prints exactly the four lines shown above.
- Capital and lower-case letters count as letters, digits as digits, and everything else, the space included, as other.
- Every element increases exactly one of the three counters, so their sum equals the number of all the elements.
- For an empty text the program prints only zeros.
- The program uses no indices, no input and no extra libraries.
- The table of cases was made before the program was run.
- You can explain why your program never counts a character twice.

When the result matches, you can save the project in Git, as in lesson 1.5.

<details>
<summary>Hint 1</summary>

Can you go through each character of the message the same way as you went through the elements of a vector earlier?

</details>

<details>
<summary>Hint 2</summary>

Each character can belong to one of three categories: a letter, a digit or other. How do you recognise each of them?

</details>

<details>
<summary>Hint 3</summary>

Remember lower-case and capital letters, and that each character should increase exactly one category counter.

</details>

<details>
<summary>The full list of check cases: open it after preparing your own table</summary>

| | Message | All | Letters | Digits | Other | What it checks |
|---|---|---|---|---|---|---|
| A | `Box 7 - ready!` | 14 | 8 | 1 | 5 | the data from the requirements |
| B | an empty text | 0 | 0 | 0 | 0 | an empty text |
| C | `ABC` | 3 | 3 | 0 | 0 | only capital letters |
| D | `xyz` | 3 | 3 | 0 | 0 | only lower-case letters |
| E | `019` | 3 | 0 | 3 | 0 | only digits, `0` and `9` included |
| F | ` -- ` (a space, two hyphens, a space) | 4 | 0 | 0 | 4 | spaces and punctuation |
| G | `A0!` | 3 | 1 | 1 | 1 | one of each category |
| H | `A1 B2` | 5 | 2 | 2 | 1 | mixed categories with a space |
| I | `z_9` | 3 | 1 | 1 | 1 | `_` is an other character |
| J | `AbC` | 3 | 3 | 0 | 0 | capital and lower-case letters together (section 10) |

In every row, the sum of letters, digits and others equals the number of all the elements.

**Automatic tests and your own runs.** Every case is checked automatically by a check program. It has the same report as the reference solution, but it reads the message from the input as one line, with `std::getline` from lesson 2.7. An empty text is an empty line in it. It's only a checking tool, not part of the mission: in the mission the message is written in the code. The check program and its results are in [Example solutions](#example-solutions), because they contain the solution.

</details>

An example solution is in [Example solutions](#example-solutions).

## 10. Find the bug: lost lower-case letters

Do this task **after the mission**: the program below contains the whole report. It reads the message from the input as one line, like the check program, and prints no question: after you start it, type the text and press **Enter**. The requirement: letters are the capital **and lower-case** letters of the English alphabet.

<details>
<summary>The program to check: open it after writing your own program</summary>

<!-- example: letters_bug -->
```cpp
#include <iostream>
#include <string>

int main() {
    std::string message{};
    std::getline(std::cin, message);

    if (std::cin.fail()) {
        std::cout << "Input could not be read\n";
    } else {
        int letters{0};
        int digits{0};
        int other{0};

        for (const char symbol : message) {
            if (symbol >= 'A' && symbol <= 'Z') {
                ++letters;
            } else if (symbol >= '0' && symbol <= '9') {
                ++digits;
            } else {
                ++other;
            }
        }

        std::cout << "Characters: " << message.size() << "\n";
        std::cout << "Letters: " << letters << "\n";
        std::cout << "Digits: " << digits << "\n";
        std::cout << "Other: " << other << "\n";
    }
}
```

1. **Predict** the report for `ABC` and for `AbC`.
2. Run the program and type `ABC`. Is the report correct?
3. Run it again and type `AbC`.
4. The sum of letters, digits and others still equals the number of all the elements. Why doesn't this check reveal the bug?
5. Find the missing range of characters.
6. Fix the condition.
7. Run the fixed program for `AbC`, the text that revealed the bug. The result for `ABC` is checked automatically.

</details>

The program's output before the fix, and the fixed program, are in [Example solutions](#example-solutions).

## 11. When something goes differently

| What you see | What it means | What to do |
|---|---|---|
| `cannot initialize a variable of type 'const char' with ...` | A `char` variable gets a text literal in quotation marks (section 3). | Write a single character in apostrophes: `'A'`. |
| `comparison between pointer and integer` when comparing a character | A character is compared with a text literal, for example `symbol == "-"`. | Compare with a character literal: `symbol == '-'`. |
| The number of letters is too small | The condition covers only capital or only lower-case letters (section 10). | A letter is the range `'A'`–`'Z'` **or** the range `'a'`–`'z'`. |
| The sum of the categories is larger than the number of elements | One character increases two counters, for example two separate `if`s instead of `else if`. | Check the categories in one `if` / `else if` / `else` chain. |
| Digits aren't counted | The condition compares with the numbers `0` and `9` instead of the characters `'0'` and `'9'`. | Use apostrophes. |
| The numbers don't add up for a text with a Polish letter | In UTF-8 a Polish letter takes several `char` elements (section 7). | In this lesson, use text without Polish letters. |

## 12. Explain

Answer in your own words, preferably in writing. Only then compare with the example answers.

1. What does a variable of type `char` store?
2. How does `'A'` differ from `"A"`? Does the literal `"A"` have the type `std::string`?
3. What does a `std::string` store?
4. What is the type of the loop variable of a range-based loop over a text, and why?
5. Is a space an element of a text?
6. What do `size()` and `empty()` give for a text?
7. How many passes does a range-based loop make over an empty text?
8. How do you recognise an ASCII digit, and why must `'0'` be in apostrophes?
9. Why do you have to take lower-case and capital letters into account separately?
10. How do you make sure no character is counted twice?
11. Why can `size()` give a different number from the number of letters visible in a UTF-8 text?

<details>
<summary>Example answers</summary>

1. One character, for example a letter, a digit, a space or a punctuation mark.
2. `'A'` is a character literal: one character of type `char`. `"A"` is a text literal. A `std::string` can be created from it, but the literal itself doesn't have the type `std::string`.
3. A sequence of `char` elements: zero, one or many characters.
4. `char`, because the elements of a text are of type `char`. The type of the loop variable is the type of the elements, like `int` for a `std::vector<int>`.
5. Yes. A space is an ordinary character: it counts in `size()`, and the loop gets it like any other element.
6. `size()` gives the number of elements of the text, and `empty()` gives `true` when the text has no elements.
7. Zero. The body doesn't run even once.
8. With the condition `symbol >= '0' && symbol <= '9'`, because the digits follow one another in order. The apostrophes are needed because we compare characters: `0` without apostrophes is an `int` number, not the character `'0'`.
9. Because in ASCII they're two separate ranges of characters. A condition only for `'A'`–`'Z'` misses every lower-case letter.
10. Check the categories in one `if` / `else if` / `else` chain. Then exactly one branch runs for each character.
11. Because `size()` counts `char` elements, and in UTF-8 one visible letter, for example `ż`, can take several such elements.

</details>

## Summary

- **`char`** stores one character. You write a character literal in apostrophes: `'A'`, `'7'`, `'!'`.
- `"A"` in quotation marks is a text literal from which a `std::string` can be created, but it isn't a `char`.
- **`std::string`** stores a sequence of `char` elements. The range-based loop `for (const char symbol : text)` goes through them in turn, spaces and punctuation included.
- `size()` gives the number of elements of a text, and `empty()` checks whether a text is empty. An empty text gives zero loop passes.
- You compare characters with character literals. In ASCII a digit is `'0'`–`'9'`, a capital letter `'A'`–`'Z'`, and a lower-case one `'a'`–`'z'`.
- An `if` / `else if` / `else` chain puts every character into exactly one category.
- This analysis is correct for ASCII text. In UTF-8 one Polish letter can take several `char` elements.

## What's next

In this lesson the loop went through the characters in turn. In the next lesson you'll read the character at a chosen position and compare neighbouring characters, like the elements of a vector in lesson 6.3: [Lesson 7.2: Positions and neighbouring characters in a `std::string`](lesson_02_positions_and_neighbours.en.md).

---

## Example solutions

Look here **after your own attempt**. Your names may differ, as long as the standard output is as required.

<details>
<summary>Section 9: the mission, a character report</summary>

<!-- example: message_report -->
```cpp
#include <iostream>
#include <string>

int main() {
    const std::string message{"Box 7 - ready!"};

    int letters{0};
    int digits{0};
    int other{0};

    for (const char symbol : message) {
        if ((symbol >= 'A' && symbol <= 'Z') || (symbol >= 'a' && symbol <= 'z')) {
            ++letters;
        } else if (symbol >= '0' && symbol <= '9') {
            ++digits;
        } else {
            ++other;
        }
    }

    std::cout << "Characters: " << message.size() << "\n";
    std::cout << "Letters: " << letters << "\n";
    std::cout << "Digits: " << digits << "\n";
    std::cout << "Other: " << other << "\n";
}
```

1. **The range-based loop:** a `std::string` lets you go through its successive elements, like a vector, so each character reaches the loop body exactly once.
2. **The loop variable is a `char`**, because the elements of a text are of type `char`. `const`, because the body only reads the character.
3. **Capital and lower-case letters** are two ranges joined with `||`. The parentheses around each range show which `&&` conditions belong together.
4. **No double counting:** the `if` / `else if` / `else` chain runs exactly one branch for each character. That's why the sum of the three counters always equals `message.size()`.
5. **A space** is neither a letter nor a digit, so it goes into the `else` branch, the `Other` category, like a hyphen and an exclamation mark.
6. **An empty text:** the loop makes no passes, so the counters stay at their initial values of 0, and `size()` gives 0.
7. **The ASCII limit:** the ranges `'A'`–`'Z'` and `'a'`–`'z'` cover only English letters. For a UTF-8 text with a Polish letter, each of its `char` elements would go to `Other`, and `Characters` wouldn't be the number of visible letters. The program is correct for ASCII text, not for any Unicode text.

The categories can also be checked in a different order, for example digits first, as long as the `else if` chain makes each character go into one category.

**The check program** checks every case in the list of check cases. The loop and the report are the same as above, apart from the indentation. There's one difference: the message is read from the input as one line with `std::getline` (lesson 2.7), so it has no `const`.

<!-- example: message_report_check -->
```cpp
#include <iostream>
#include <string>

int main() {
    std::string message{};
    std::getline(std::cin, message);

    if (std::cin.fail()) {
        std::cout << "Input could not be read\n";
    } else {
        int letters{0};
        int digits{0};
        int other{0};

        for (const char symbol : message) {
            if ((symbol >= 'A' && symbol <= 'Z') || (symbol >= 'a' && symbol <= 'z')) {
                ++letters;
            } else if (symbol >= '0' && symbol <= '9') {
                ++digits;
            } else {
                ++other;
            }
        }

        std::cout << "Characters: " << message.size() << "\n";
        std::cout << "Letters: " << letters << "\n";
        std::cout << "Digits: " << digits << "\n";
        std::cout << "Other: " << other << "\n";
    }
}
```

Each case is one line of input, in the order of the list of check cases, from A to J. Case B is an empty line.

<!-- input: message_report_check -->
```text
Box 7 - ready!
```

<!-- output: message_report_check -->
```text
Characters: 14
Letters: 8
Digits: 1
Other: 5
```

<!-- input: message_report_check -->
```text

```

<!-- output: message_report_check -->
```text
Characters: 0
Letters: 0
Digits: 0
Other: 0
```

<!-- input: message_report_check -->
```text
ABC
```

<!-- output: message_report_check -->
```text
Characters: 3
Letters: 3
Digits: 0
Other: 0
```

<!-- input: message_report_check -->
```text
xyz
```

<!-- output: message_report_check -->
```text
Characters: 3
Letters: 3
Digits: 0
Other: 0
```

<!-- input: message_report_check -->
```text
019
```

<!-- output: message_report_check -->
```text
Characters: 3
Letters: 0
Digits: 3
Other: 0
```

<!-- input: message_report_check -->
```text
 -- 
```

<!-- output: message_report_check -->
```text
Characters: 4
Letters: 0
Digits: 0
Other: 4
```

<!-- input: message_report_check -->
```text
A0!
```

<!-- output: message_report_check -->
```text
Characters: 3
Letters: 1
Digits: 1
Other: 1
```

<!-- input: message_report_check -->
```text
A1 B2
```

<!-- output: message_report_check -->
```text
Characters: 5
Letters: 2
Digits: 2
Other: 1
```

<!-- input: message_report_check -->
```text
z_9
```

<!-- output: message_report_check -->
```text
Characters: 3
Letters: 1
Digits: 1
Other: 1
```

<!-- input: message_report_check -->
```text
AbC
```

<!-- output: message_report_check -->
```text
Characters: 3
Letters: 3
Digits: 0
Other: 0
```

</details>

<details>
<summary>Section 10: the output before the fix, and the fixed program</summary>

Before the fix, for `ABC`:

<!-- input: letters_bug -->
```text
ABC
```

<!-- output: letters_bug -->
```text
Characters: 3
Letters: 3
Digits: 0
Other: 0
```

For `AbC`:

<!-- input: letters_bug -->
```text
AbC
```

<!-- output: letters_bug -->
```text
Characters: 3
Letters: 2
Digits: 0
Other: 1
```

- For `ABC` the report is correct: all the letters are capitals, so the missing range doesn't matter.
- For `AbC` the lower-case letter `b` goes to `Other`: there are 2 letters instead of 3.
- **The sum still adds up** (2 + 0 + 1 = 3), because `b` increased a different counter, but only one. The sum check detects double counting, but not a character put into the wrong category.
- **The cause:** the letter condition covers only the range `'A'`–`'Z'`.
- **The fix:** `(symbol >= 'A' && symbol <= 'Z') || (symbol >= 'a' && symbol <= 'z')`.

The fixed program is the check program from section 9: it differs from the buggy program only in that condition. For both texts it gives the results from the list of check cases: cases C and J.

</details>

**Previous lesson:** [Lesson 6.6: A training log (the Module 6 test)](../module_06_collections/lesson_06_training_log.en.md) · **Next lesson:** [Lesson 7.2: Positions and neighbouring characters in a `std::string`](lesson_02_positions_and_neighbours.en.md) · [Course overview](../../README.en.md)

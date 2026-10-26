# Lesson 7.3: A function creates a new text

[Polski](lesson_03_a_function_creates_a_new_text.md) · **English** · [Course overview](../../README.en.md)

> **Module 7, lesson 3** · about 60–75 minutes
> **You need:** your `cpp-workspace` folder and the original `lesson_05_first_program` project, as before. You won't need the debugger in this lesson.
> **Pilot version.** The programs in this lesson are checked automatically on Windows, Ubuntu and macOS, including with the given input data. Typing input in CLion's **Run** window is described without a manual check on every system.

## Before you start

This lesson assumes that you:

- write functions that get a vector through `const std::vector<int>&` (lesson 6.4), and functions that build a new vector with `push_back` and return it by value (lesson 6.5);
- go through a text with a range-based loop and compare characters (lesson 7.1);
- read characters through an index and compare a character with the previous one (lesson 7.2);
- remember short-circuit evaluation of `&&` and `||` (lesson 3.4).

## The situation

In lesson 6.5, a function got a vector, chose elements from it and returned a **new** vector. Text often works the same way. From the text `"A B C"` you want the same text without spaces, `"ABC"`. Counting the spaces isn't enough: you need a new sequence of characters. You'll build it in a separate `std::string`, and the input text will stay unchanged.

After this lesson you will:

- write functions that get a text through `const std::string&` and return a new `std::string`;
- build a new text character by character with `push_back`;
- tell the input text from the result text, and recognise an empty result as correct;
- recognise the start of a word, also when several spaces separate the words;
- design on your own a function that works out initials.

## 1. Prepare the project

In `cpp-workspace`, create a folder `lesson_7_3` and copy `main.cpp` and `CMakeLists.txt` from the original `lesson_05_first_program` into it. You type the programs from sections 2 and 3 into `main.cpp` in this folder.

## 2. A function that returns a new text

<!-- example: spaces_removed -->
```cpp
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

int main() {
    const std::string source{"A B  C"};

    std::cout << "Original: [" << source << "]\n";

    const std::string selected{without_spaces(source)};

    std::cout << "Selected: [" << selected << "]\n";
    std::cout << "Original after: [" << source << "]\n";
}
```

**Predict** all three lines. After the call to `without_spaces`, are there still spaces in `source`? The square brackets show where the text starts and ends, so the spaces are visible too.

<details>
<summary>Standard output</summary>

<!-- output: spaces_removed -->
```text
Original: [A B  C]
Selected: [ABC]
Original after: [A B  C]
```

</details>

It's the same layout as in lesson 6.5, only for text:

| Notation | Meaning in this lesson |
|---|---|
| `const std::string& text` | an existing text made available to the function for reading, without copying |
| `std::string result{}` | a new, local text that the function builds; empty at first |
| `result.push_back(symbol)` | adding one character at the end of the new text |
| `return result;` | returning the finished text by value |
| `const std::string selected{...}` | receiving the result, which `main` doesn't intend to change |

- **`push_back` for a text** works as for a vector in lesson 6.2: it adds one element at the end, and here the element is one `char`. Spaces aren't added, and the other characters go into the result in the same order as in the input text.
- **`const` applies only to the parameter.** The function can't change `text`, but it does change its local `result`, because it adds characters to it, so `result` has no `const`. The result received in `main` has `const`, because `main` doesn't change it any more.
- **The original is unchanged:** the function only reads `text` and builds a separate result. The third line confirms it.
- **Returning by value** works as in lesson 6.5: the caller gets its own, finished result.

Strings can also be joined in other ways, for example with `+` from lesson 2.7. In this lesson we build the result character by character, so we use only `push_back`.

## 3. An empty result

<!-- example: only_spaces -->
```cpp
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

int main() {
    const std::string source{"   "};
    const std::string selected{without_spaces(source)};

    std::cout << "Original: [" << source << "]\n";
    std::cout << "Selected: [" << selected << "]\n";
    std::cout << "Selected size: " << selected.size() << "\n";

    if (selected.empty()) {
        std::cout << "The result is empty\n";
    }
}
```

**Predict** the result for a text made only of spaces.

<details>
<summary>Standard output</summary>

<!-- output: only_spaces -->
```text
Original: [   ]
Selected: []
Selected size: 0
The result is empty
```

</details>

The function found no character to keep, so it returned an empty text. **That's a correct result, not an error:** the result exists, its `size()` is 0, and `empty()` gives `true`. No separate error code or special value is needed. The only thing you don't do with an empty result is read its characters, for example `selected[0]`: there's no such character (lesson 7.2).

## 4. Mission: initials

The program gets a first name and a surname written in a text, and creates a new text with the first letter of each word. The text is written in the code:

<!-- fragment -->
```cpp
const std::string name{"  Ada   Lovelace  "};
```

**What data is possible.** The text contains only capital letters `A`–`Z`, lower-case letters `a`–`z` and ordinary spaces. It has no digits, hyphens, apostrophes, commas, tabs or Polish letters. That's a deliberate simplification, so you don't need to check for other characters.

**Rules:**

- **A word** is a non-empty run of letters. Words are separated by one or more spaces. Spaces can also stand at the start and at the end of the text.
- Each word gives **exactly one** initial: its first letter.
- Spaces never go into the result.
- **Letter case stays unchanged.** For `"Mary ann SMITH"` the result is `"MaS"`, not `"MAS"`. The program chooses existing characters and doesn't change them.
- An empty text, or a text of only spaces, gives an empty result.

**Requirements:**

- The program has its own function that gets the text through `const std::string&`, creates a local empty `std::string`, adds the initials to it with `push_back` and returns it by value. The function reads nothing from the input, prints nothing and doesn't change the input text. You choose its name yourself.
- `main` prepares the text, calls the function, receives the result and prints two lines: `Name: [TEXT]` and `Initials: [RESULT]`. It prints an empty result as `Initials: []`. It prints nothing else and doesn't repeat the function's algorithm.
- If you compare a character with the previous one, remember that the first character of the text has no predecessor (lesson 7.2).
- The program reads nothing from the input.

In `cpp-workspace`, create a folder `initials`, copy `CMakeLists.txt` from the original `lesson_05_first_program` into it, create an empty `main.cpp` and write the program on your own.

For the text above, the standard output must be:

<!-- output: initials -->
```text
Name: [  Ada   Lovelace  ]
Initials: [AL]
```

**This isn't the function from section 2 with a different condition.** There, the only thing that decided about a character was whether it's a space. Here, a character's place also matters: a letter goes into the result only when it **starts a word**. It isn't enough to remove the spaces, to keep every letter, or to take the character after every space, because there can be several spaces between words. You have to decide on your own:

1. what to call the function and how to write its header;
2. whether you go through the text with a range-based loop or an index loop;
3. how to recognise the start of the first word, also after spaces at the start of the text;
4. how to recognise the start of the next word after several spaces;
5. how to make sure no space goes into the result;
6. what the function returns for an empty text and for only spaces.

**Before you write the program**, prepare a table of cases: the data from the requirements, two words separated by one and by two spaces, spaces only at the start and only at the end, one word, one letter, an empty text, one space, only spaces, mixed letter case, and three words with different numbers of spaces. For each, write down the expected result.

**Then:** run the program for the data from the requirements, and then change the text to 3–4 cases from your table, for example `"Ada  Lovelace"`, `"Mary ann SMITH"`, `"   "` and an empty text. Every case in the full list of check cases is checked automatically, so you don't need to type them all.

### Success criteria

- The program builds as C++20 and, for the data from the requirements, prints exactly the two lines shown above.
- The function gets the text through `const std::string&`, builds the result with `push_back` and returns it as a `std::string`. It reads and prints nothing.
- Each word gives one initial, whatever the number of spaces before and after it.
- There are no spaces in the result, and the letter case is the same as in the input text.
- An empty text and only spaces give `Initials: []`.
- The program never reads a character outside the text.
- The table of cases was made before the program was run.
- You can explain how your function recognises the start of a word.

When the result matches, you can save the project in Git, as in lesson 1.5.

<details>
<summary>Hint 1</summary>

Which characters are needed in the new text, and which should stay only in the input text?

</details>

<details>
<summary>Hint 2</summary>

The first letter of each word matters. How do you recognise the start of the next word if there's more than one space between words?

</details>

<details>
<summary>Hint 3</summary>

Make sure you add only a letter to the result, not a space. You can look at the previous character, or remember that you're expecting the start of a new word.

</details>

<details>
<summary>The full list of check cases: open it after preparing your own table</summary>

| | Text | Initials | What it checks |
|---|---|---|---|
| A | `  Ada   Lovelace  ` | `AL` | the data from the requirements: spaces at the start, in the middle and at the end |
| B | `Ada Lovelace` | `AL` | two words, one space |
| C | `Ada  Lovelace` | `AL` | two spaces between the words |
| D | `  Ada` | `A` | spaces only at the start |
| E | `Ada  ` | `A` | spaces only at the end |
| F | `Ada` | `A` | one word, no spaces |
| G | `A` | `A` | one letter |
| H | an empty text | empty | an empty text |
| I | one space | empty | one space |
| J | three spaces | empty | only spaces |
| K | `Mary ann SMITH` | `MaS` | letter case unchanged |
| L | `a B c` | `aBc` | lower-case and capital initials |
| M | `A  B   C` | `ABC` | three words, different numbers of spaces |
| N | `Ada Ada` | `AA` | a repeated word |
| O | `AA BB` | `AB` | only the first letter of a word |

**Automatic tests and your own runs.** Every case is checked automatically by a check program. It has the same function as the reference solution, but it reads the text from the input as one line, with `std::getline` from lesson 2.7. Spaces at the start and the end of the line are kept, and an empty text is an empty line, not missing data. It's only a checking tool, not part of the mission. The check program and its results are in [Example solutions](#example-solutions), because they contain the solution.

</details>

An example solution is in [Example solutions](#example-solutions).

## 5. Find the bug: a space as an initial

Do this task **after the mission**: the program below contains almost the whole solution. It reads the text from the input as one line, like the check program, and prints no question: after you start it, type the text and press **Enter**. The function checks whether a character stands at the start of the text or straight after a space.

<details>
<summary>The program to check: open it after writing your own program</summary>

<!-- example: initials_space_bug -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>

std::string initials_of(const std::string& text) {
    std::string result{};

    for (std::size_t index{0}; index < text.size(); ++index) {
        const bool word_can_start{index == 0 || text[index - 1] == ' '};

        if (word_can_start) {
            result.push_back(text[index]);
        }
    }

    return result;
}

int main() {
    std::string name{};
    std::getline(std::cin, name);

    if (std::cin.fail()) {
        std::cout << "Input could not be read\n";
    } else {
        const std::string initials{initials_of(name)};

        std::cout << "Name: [" << name << "]\n";
        std::cout << "Initials: [" << initials << "]\n";
    }
}
```

1. **Predict** the result for `Ada Lovelace` and for `Ada  Lovelace`, with two spaces.
2. Run the program for `Ada Lovelace`. Is the result correct?
3. Run it for `Ada  Lovelace`.
4. Trace the characters from index 3 to 5: at which character does a space go into the result?
5. Point to the missing check.
6. Fix the function.
7. Check both cases again, and also `  Ada`, three spaces, `Ada` and `A  B   C`.

</details>

The program's output before the fix, and the fixed program, are in [Example solutions](#example-solutions).

## 6. When something goes differently

| What you see | What it means | What to do |
|---|---|---|
| There's a space in the result, for example `Initials: [A L]` | The program adds a character that stands after a space, although it's a space itself (section 5). | Add only a character that isn't a space to the result. |
| The result starts with a space when the text starts with spaces | The first character of the text is added without checking that it's a letter. | The first character must also be a letter to go into the result. |
| The first initial is missing | The first word isn't recognised, because there's no space before it. | The start of the text can also be the start of a word. |
| Too many initials, for example `AdaLovelace` instead of `AL` | The program adds every letter, not only the first one in a word. | A letter goes into the result only when it starts a word. |
| A compile error at `push_back` in which the compiler mentions `const` | The program adds a character to the `const&` parameter, or to a result declared `const`. | Build the result in a local `std::string` without `const`. |
| A compile error at `push_back` with `'const char[2]'` | `push_back` gets a text in quotation marks, for example `"A"`. | `push_back` takes one character: `'A'` or a `char` variable. |
| Strange characters, or the program ends unexpectedly | Probably a read of `text[index - 1]` for index 0. | The first character has no predecessor (lesson 7.2). Check it separately, or use short-circuit evaluation from lesson 3.4. |

## 7. Explain

Answer in your own words, preferably in writing. Only then compare with the example answers.

1. What does the parameter `const std::string&` mean, and why doesn't the function need to copy the text?
2. Why does the local result have no `const`, while the result received in `main` can have it?
3. What does `push_back(char)` do on a text?
4. How does returning a `std::string` differ from returning an `int`? Does `return result;` return a reference to a local variable?
5. Does the function change the original text?
6. What does an empty result mean, and how does it differ from a failure?
7. Why can't several spaces between words give several initials?
8. Why do spaces at the start of the text need care?
9. How does your program keep the letter case?
10. In this mission, when is a range-based loop more convenient, and when an index loop?
11. Why doesn't the case `Ada Lovelace` reveal the bug in section 5?

<details>
<summary>Example answers</summary>

1. The parameter refers to the caller's existing text and lets the function only read it, like `const&` for a vector in lesson 6.4. A function that only reads a text doesn't need a copy of it.
2. The function adds characters to the local result, so it has to change it. `main` gets a finished result and, if it doesn't change it, marks it `const`.
3. It adds one character at the end of the text. The earlier characters stay, and `size()` grows by 1.
4. The mechanism is the same: `return` passes the result to the place of the call by value. Only the type differs: instead of one number, the caller gets a whole new text. It isn't a reference to a local variable, but the caller's own result, as in lesson 6.5.
5. No. It gets it through `const&`, so it can only read it. The chosen characters go into a separate text.
6. That no character met the condition, for example the text was empty or made only of spaces. The function worked correctly, and its result is a text with no characters: `size()` gives 0, and `empty()` gives `true`.
7. Because each word starts only once. Spaces are separators, not words: an extra space doesn't start a new word, and an initial is a letter, not a space.
8. Because before the first word there may be no character at all, or several spaces. The function has to recognise the first letter in both situations, without adding any of those spaces.
9. It adds to the result exactly the character that stands in the text, without any conversion. A capital letter stays capital, and a lower-case one stays lower-case.
10. An index loop gives direct access to the previous character, but needs care at index 0. A range-based loop has no indices, so the previous character has to be remembered in a separate variable. Both ways are correct.
11. Because there's only one space between the words. After a single space, the next character is already a letter, so the wrong condition has no chance to add a space.

</details>

## Summary

- A function can get a text through `const std::string&`, build a new `std::string` and return it by value, like a vector in lesson 6.5.
- `push_back(char)` adds one character at the end of the new text. The result is built in a local `std::string` without `const`.
- The input text stays unchanged, and the chosen characters keep its order.
- An empty text is a correct result, not an error. You recognise it with `empty()`, and in brackets it looks like this: `[]`.
- The start of a word is a letter that stands at the start of the text or straight after a space. Several spaces in a row don't create new words.
- When comparing with the previous character, remember that the first character has no predecessor.

## What's next

In this lesson the text was written in the code. In the next lesson the program will read successive lines of text from the input with `std::getline` and analyse each of them: [Lesson 7.4: Processing successive lines with `std::getline`](lesson_04_successive_lines.en.md).

---

## Example solutions

Look here **after your own attempt**. Your names may differ, as long as the standard output is as required.

<details>
<summary>Section 4: the mission, initials</summary>

<!-- example: initials -->
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
    const std::string name{"  Ada   Lovelace  "};
    const std::string initials{initials_of(name)};

    std::cout << "Name: [" << name << "]\n";
    std::cout << "Initials: [" << initials << "]\n";
}
```

1. **The parameter has `const&`**, because the function only reads the text and doesn't need a copy of it.
2. **The local result has no `const`**, because the function adds the initials to it.
3. **Returning a `std::string` by value:** `main` gets a finished, own result, like a vector in lesson 6.5.
4. **The first word:** for index 0, `word_can_start` is true, because the start of the text can also start a word. The left part `index == 0` is true then, so `||` doesn't evaluate the right part: `text[index - 1]` isn't read for index 0. That's short-circuit evaluation from lesson 3.4 in practice.
5. **The next words:** for indices from 1 upwards, `word_can_start` is true when the previous character is a space.
6. **Several spaces:** a character after a space goes into the result only when it isn't a space itself: `text[index] != ' '`. The second and later spaces stand after a space, but they're spaces, so they don't go into the result.
7. **Spaces at the start:** the first space stands at the start of the text, and the next ones after spaces, but none is a letter, so none goes into the result. Only the first letter after them is added.
8. **Spaces at the end:** after the last word there are no more letters, so nothing else is added.
9. **An empty text:** the loop makes no passes, so the function returns the empty `result`.
10. **Letter case:** `push_back(text[index])` adds the character exactly as it stands in the text.
11. **The original unchanged:** the function gets `text` through `const&` and only reads it.
12. **Other correct algorithms:** you can go through the text with a range-based loop and remember in a `bool` variable whether the previous character was a space, as in the program below. You can also check the first character separately and start the loop comparing with the previous one at index 1. What matters is that each word gives one initial and a space never goes into the result.

**Another correct algorithm: a range-based loop and a variable that remembers the previous character.**

<!-- example: initials_with_flag -->
```cpp
#include <iostream>
#include <string>

std::string initials_of(const std::string& text) {
    std::string result{};
    bool after_space{true};

    for (const char symbol : text) {
        if (symbol != ' ' && after_space) {
            result.push_back(symbol);
        }

        after_space = (symbol == ' ');
    }

    return result;
}

int main() {
    const std::string name{"  Ada   Lovelace  "};
    const std::string initials{initials_of(name)};

    std::cout << "Name: [" << name << "]\n";
    std::cout << "Initials: [" << initials << "]\n";
}
```

<!-- output: initials_with_flag -->
```text
Name: [  Ada   Lovelace  ]
Initials: [AL]
```

`after_space` says whether the previous character was a space. At the start it's `true`, because the first character of the text can also start a word, just like a character after a space. After each character the variable gets a new value: `true` when that character was a space, and `false` otherwise. This version needs no indices, so there's also no risk of reading before the first character.

**The check program** checks every case in the list of check cases. The function is the same as in the reference solution, and in `main` the text is read from the input as one line with `std::getline`, so it has no `const`. `std::getline` keeps the spaces at the start and the end of the line.

<!-- example: initials_check -->
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
    std::string name{};
    std::getline(std::cin, name);

    if (std::cin.fail()) {
        std::cout << "Input could not be read\n";
    } else {
        const std::string initials{initials_of(name)};

        std::cout << "Name: [" << name << "]\n";
        std::cout << "Initials: [" << initials << "]\n";
    }
}
```

Each case is one line of input, in the order of the list of check cases, from A to O. Case H is an empty line, case I is one space, and case J is three spaces.

<!-- input: initials_check -->
```text
  Ada   Lovelace  
```

<!-- output: initials_check -->
```text
Name: [  Ada   Lovelace  ]
Initials: [AL]
```

<!-- input: initials_check -->
```text
Ada Lovelace
```

<!-- output: initials_check -->
```text
Name: [Ada Lovelace]
Initials: [AL]
```

<!-- input: initials_check -->
```text
Ada  Lovelace
```

<!-- output: initials_check -->
```text
Name: [Ada  Lovelace]
Initials: [AL]
```

<!-- input: initials_check -->
```text
  Ada
```

<!-- output: initials_check -->
```text
Name: [  Ada]
Initials: [A]
```

<!-- input: initials_check -->
```text
Ada  
```

<!-- output: initials_check -->
```text
Name: [Ada  ]
Initials: [A]
```

<!-- input: initials_check -->
```text
Ada
```

<!-- output: initials_check -->
```text
Name: [Ada]
Initials: [A]
```

<!-- input: initials_check -->
```text
A
```

<!-- output: initials_check -->
```text
Name: [A]
Initials: [A]
```

<!-- input: initials_check -->
```text

```

<!-- output: initials_check -->
```text
Name: []
Initials: []
```

<!-- input: initials_check -->
```text
 
```

<!-- output: initials_check -->
```text
Name: [ ]
Initials: []
```

<!-- input: initials_check -->
```text
   
```

<!-- output: initials_check -->
```text
Name: [   ]
Initials: []
```

<!-- input: initials_check -->
```text
Mary ann SMITH
```

<!-- output: initials_check -->
```text
Name: [Mary ann SMITH]
Initials: [MaS]
```

<!-- input: initials_check -->
```text
a B c
```

<!-- output: initials_check -->
```text
Name: [a B c]
Initials: [aBc]
```

<!-- input: initials_check -->
```text
A  B   C
```

<!-- output: initials_check -->
```text
Name: [A  B   C]
Initials: [ABC]
```

<!-- input: initials_check -->
```text
Ada Ada
```

<!-- output: initials_check -->
```text
Name: [Ada Ada]
Initials: [AA]
```

<!-- input: initials_check -->
```text
AA BB
```

<!-- output: initials_check -->
```text
Name: [AA BB]
Initials: [AB]
```

</details>

<details>
<summary>Section 5: the output before the fix, and the fixed program</summary>

Before the fix, for `Ada Lovelace`:

<!-- input: initials_space_bug -->
```text
Ada Lovelace
```

<!-- output: initials_space_bug -->
```text
Name: [Ada Lovelace]
Initials: [AL]
```

For `Ada  Lovelace`, with two spaces:

<!-- input: initials_space_bug -->
```text
Ada  Lovelace
```

<!-- output: initials_space_bug -->
```text
Name: [Ada  Lovelace]
Initials: [A L]
```

| Index | Character | Previous character | `word_can_start` | Added? |
|---|---|---|---|---|
| 3 | a space | `a` | `false` | no |
| 4 | a space | a space | `true` | **yes: a space goes into the result** |
| 5 | `L` | a space | `true` | yes |

For the other texts:

<!-- input: initials_space_bug -->
```text
  Ada
```

<!-- output: initials_space_bug -->
```text
Name: [  Ada]
Initials: [  A]
```

<!-- input: initials_space_bug -->
```text
   
```

<!-- output: initials_space_bug -->
```text
Name: [   ]
Initials: [   ]
```

<!-- input: initials_space_bug -->
```text
Ada
```

<!-- output: initials_space_bug -->
```text
Name: [Ada]
Initials: [A]
```

<!-- input: initials_space_bug -->
```text
A  B   C
```

<!-- output: initials_space_bug -->
```text
Name: [A  B   C]
Initials: [A B  C]
```

- For `Ada Lovelace` and `Ada` the result is correct: after a single space there's already a letter, and without spaces there's nothing to get wrong.
- For two spaces in a row, spaces at the start and only spaces, spaces go into the result: the second space stands after a space, and the function doesn't check whether the character itself is a letter.
- **The cause:** the condition `if (word_can_start)` checks only the character's place, not the character itself.
- **The fix:** `if (text[index] != ' ' && word_can_start)`.

There's no read outside the text here: for index 0, the short-circuit `||` skips `text[index - 1]`.

The fixed program is the check program from section 4: it differs from the buggy program only in that condition. For all six texts it gives the results from the list of check cases: cases B, C, D, J, F and M.

</details>

**Previous lesson:** [Lesson 7.2: Positions and neighbouring characters in a `std::string`](lesson_02_positions_and_neighbours.en.md) · **Next lesson:** [Lesson 7.4: Processing successive lines with `std::getline`](lesson_04_successive_lines.en.md) · [Course overview](../../README.en.md)

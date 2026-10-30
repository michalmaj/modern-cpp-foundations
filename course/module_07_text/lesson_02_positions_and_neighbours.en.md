# Lesson 7.2: Positions and neighbouring characters in a `std::string`

[Polski](lesson_02_positions_and_neighbours.md) · **English** · [Course overview](../../README.en.md)

> **Module 7, lesson 2** · about 60–75 minutes
> **You need:** your `cpp-workspace` folder and the original `lesson_05_first_program` project, as before. You won't need the debugger in this lesson.
> **Pilot version.** The programs in this lesson are checked automatically on Windows, Ubuntu and macOS, including with the given input data. Typing input in CLion's **Run** window is described without a manual check on every system.

## Before you start

This lesson assumes that you:

- go through a text character by character with a range-based loop and compare characters with character literals (lesson 7.1);
- read vector elements through an index, use `std::size_t` from `<cstddef>`, and compare neighbouring elements with a loop from index 1 (lesson 6.3).

## The situation

The range-based loop from lesson 7.1 reads every character of the text `"Book"`. But try to answer these questions with it alone:

- Which character stands in the second position?
- Are the two middle characters the same?
- In which position does a character repeat?
- How do you compare each character with the previous one?

Questions like these need the **position** of a character, not only its value. A text has positions just like a vector in lesson 6.3, so you'll use indices here. When the position isn't needed, a range-based loop is still the natural choice.

After this lesson you will:

- read the character at a chosen index with `text[index]`, with indices from 0, and turn an index into a position shown to a person;
- read the first and last character of a non-empty text;
- go through a text with an index loop using `std::size_t`;
- safely compare neighbouring characters, also in an empty and a one-character text;
- count every pair of identical neighbouring characters, overlapping pairs included.

## 1. Prepare the project

In `cpp-workspace`, create a folder `lesson_7_2` and copy `main.cpp` and `CMakeLists.txt` from the original `lesson_05_first_program` into it. You type the programs from sections 2–5 into `main.cpp` in this folder.

## 2. The character at a chosen position

<!-- example: book_by_index -->
```cpp
#include <iostream>
#include <string>

int main() {
    const std::string text{"Book"};

    std::cout << text[0] << "\n";
    std::cout << text[1] << "\n";
    std::cout << text[2] << "\n";
    std::cout << text[3] << "\n";
}
```

<!-- output: book_by_index -->
```text
B
o
o
k
```

| Position for a person | Index in C++ | Character |
|---|---|---|
| 1 | 0 | `B` |
| 2 | 1 | `o` |
| 3 | 2 | `o` |
| 4 | 3 | `k` |

The notation is the same as for a vector in lesson 6.3: read `text[1]` as "the character of `text` at index 1". The result is one character of type `char`. **Indices start at 0**, so `text.size()` gives 4, and the fourth position has the index 3.

**One detail differs between a text and a vector.** For a `std::string`, reading `text[text.size()]` is allowed and gives a special null character that **isn't part of the text's contents**. For an index greater than `size()` the behaviour is undefined, as for a vector. You don't need to remember this detail. The rule is enough: **a character that belongs to the text has an index with `index < text.size()`.**

## 3. The first and last character

<!-- example: first_and_last_char -->
```cpp
#include <iostream>
#include <string>

int main() {
    const std::string text{"Book"};

    if (!text.empty()) {
        std::cout << text[0] << "\n";
        std::cout << text[text.size() - 1] << "\n";
    }
}
```

**Predict** both lines and run the program.

<details>
<summary>Standard output</summary>

<!-- output: first_and_last_char -->
```text
B
k
```

</details>

- The first character has the index 0, and the last one `size() - 1`, as in lesson 6.3.
- **`empty()` first.** An empty text has no first or last character. And `size() - 1` for an empty text doesn't give −1, because the result of `size()` is an unsigned number. That's why we don't work out the last position before checking that the text isn't empty.

## 4. A loop over positions

<!-- example: char_positions -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>

int main() {
    const std::string text{"Cat"};

    for (std::size_t index{0}; index < text.size(); ++index) {
        std::cout << "Position " << index + 1 << ": " << text[index] << "\n";
    }
}
```

**Predict** every line and run the program.

<details>
<summary>Standard output</summary>

<!-- output: char_positions -->
```text
Position 1: C
Position 2: a
Position 3: t
```

</details>

This is the loop from lesson 6.3, only over a text: the `std::size_t` index starts at 0, the condition `index < text.size()` allows only characters that belong to the text, `text[index]` reads the current character, and the loop ends before the index reaches `size()`. We keep the index in a `std::size_t` for the same reason as in 6.3: it matches the result of `size()`. If you store `size()` in an `int` with `{}`, the compiler rejects it as a narrowing conversion.

**The position for a person is `index + 1`.** A text's indexing always starts at 0. Numbering from 1 is only a way to show the result.

## 5. Neighbouring characters

For the current index `index`, the previous character has the index `index - 1`:

<!-- example: neighbour_pairs -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>

int main() {
    const std::string text{"Book"};

    for (std::size_t index{1}; index < text.size(); ++index) {
        const char previous{text[index - 1]};
        const char current{text[index]};

        std::cout << previous << current << "\n";
    }
}
```

**Predict** how many lines the program prints, and which.

<details>
<summary>Standard output</summary>

<!-- output: neighbour_pairs -->
```text
Bo
oo
ok
```

</details>

| Current index | Previous character | Current character | The same? |
|---|---|---|---|
| 1 | `B` | `o` | no |
| 2 | `o` | `o` | yes |
| 3 | `o` | `k` | no |

**Answer before you open the answers:**

1. How many pairs of neighbouring characters does a four-character text have?
2. Why does the loop start at index 1?
3. What happens for a one-character text, and for an empty one?
4. Which positions for a person does the pair at index 2 form?
5. Is comparing `text[index - 1]` with `text[index]` safe for index 1? And for the last index in the loop?

<details>
<summary>Answers</summary>

1. Three. Every character except the first forms a pair with the previous one.
2. Because the character at index 0 has no predecessor. From index 1 on, the previous character, `index - 1`, always exists.
3. For one character `1 < 1` gives `false`, and for an empty text `1 < 0` gives `false`, so the loop makes no passes. There's no pair, so there's nothing to compare. This loop needs no separate `empty()` check.
4. The indices 1 and 2, which are positions 2 and 3: `index` and `index + 1`.
5. Yes. For index 1 we compare the indices 0 and 1. The last pass has `index` equal to `size() - 1`, so both characters belong to the text. Then the condition `index < text.size()` gives `false` and the loop ends.

</details>

**We compare exact `char` values.** `'A'` and `'A'` are the same, but `'A'` and `'a'` aren't: they're different characters. Two neighbouring spaces are the same, and so are two full stops or two `'1'` digits. We don't ignore letter case, and we don't remove anything from the text.

## 6. Mission: a map of repeated characters

The program looks in a short ASCII text for every pair of neighbouring, identical characters and gives their positions. The text is written in the code:

<!-- fragment -->
```cpp
const std::string text{"coffee 111"};
```

**Requirements:**

- The first line: `Characters: N`, the number of elements of the text.
- For each pair of neighbouring, identical characters, in order from the start of the text, the program prints `Pair X-Y: [C]`: `X` and `Y` are the positions of both characters, counted from 1, and `C` is the repeated character, in square brackets so that a pair of spaces is visible too.
- The last line: `Repeated pairs: N`, the number of such pairs.
- **Pairs may overlap.** In `"AAA"` there are two pairs: positions 1–2 and 2–3. In `"AAAA"` there are three: 1–2, 2–3 and 3–4. A character that belongs to one pair can also belong to the next.
- We compare characters exactly: `'A'` and `'a'` don't form a pair, and two spaces do.
- When there's no pair, the program prints only `Characters: N` and `Repeated pairs: 0`, with no extra message.
- The program works after changing only the text in the braces, also for an empty and a one-character text, and never reads characters outside the text. It reads nothing from the input and doesn't change the text.

In `cpp-workspace`, create a folder `repeated_pairs`, copy `CMakeLists.txt` from the original `lesson_05_first_program` into it, create an empty `main.cpp` and write the program on your own.

For the text above, the standard output must be:

<!-- output: repeated_pairs -->
```text
Characters: 10
Pair 3-4: [f]
Pair 5-6: [e]
Pair 8-9: [1]
Pair 9-10: [1]
Repeated pairs: 4
```

In `coffee`, `f` and `e` repeat. The final `111` gives two overlapping pairs. The space is an element of the text, but it doesn't form a pair here.

**This isn't the program from section 5 with a different text.** That program only printed the pairs. You have to decide on your own:

1. how to recognise a pair of identical characters;
2. where the counter stands and when it grows;
3. how to work out the numbers of both positions from the current index;
4. how to print the repeated character;
5. how to make sure overlapping pairs aren't lost;
6. what the program prints when there are no pairs, also for an empty and a one-character text.

**Before you write the program**, prepare a table of cases: an empty text, one character, two different characters, two, three and four identical characters, two separate pairs, capital and lower-case letters next to each other, two spaces, a repeated full stop, and a repeated digit. For each, write down the expected `Pair` lines and the counter.

**Then:** run the program for the text from the requirements, and then change the text to 3–4 cases from your table, for example `"AAA"`, `"AABB"`, `"aAa"` and an empty text. Every case in the full list of check cases is checked automatically, so you don't need to type them all.

### Success criteria

- The program builds as C++20 and, for the text from the requirements, prints exactly the six lines shown above.
- Overlapping pairs are counted: `"AAA"` gives two pairs and `"AAAA"` three.
- The positions in the `Pair` lines are counted from 1, and the pairs are printed in order from the start of the text.
- Letter case matters, and spaces and punctuation can form pairs.
- An empty and a one-character text give `Repeated pairs: 0`, and the program never reads a character outside the text.
- The indices are of type `std::size_t`.
- The table of cases was made before the program was run.
- You can explain why `"AAA"` gives two pairs.

When the result matches, you can save the project in Git, as in lesson 1.5.

<details>
<summary>Hint 1</summary>

How do you check whether the current character is the same as the one directly before it?

</details>

<details>
<summary>Hint 2</summary>

Think about which index you can safely start comparing neighbours from, and how to turn their indices into position numbers from 1.

</details>

<details>
<summary>Hint 3</summary>

Increase the counter for every identical pair. Don't skip the next comparison, because one character can belong to two neighbouring pairs.

</details>

<details>
<summary>The full list of check cases: open it after preparing your own table</summary>

| | Text | `Pair` lines | Counter | What it checks |
|---|---|---|---|---|
| A | `coffee 111` | 3-4 `[f]`, 5-6 `[e]`, 8-9 `[1]`, 9-10 `[1]` | 4 | the data from the requirements |
| B | an empty text | — | 0 | an empty text |
| C | `A` | — | 0 | one character |
| D | `AB` | — | 0 | two different characters |
| E | `AA` | 1-2 `[A]` | 1 | the shortest pair |
| F | `AAA` | 1-2 `[A]`, 2-3 `[A]` | 2 | two overlapping pairs |
| G | `AAAA` | 1-2, 2-3, 3-4, each `[A]` | 3 | three overlapping pairs |
| H | `AABB` | 1-2 `[A]`, 3-4 `[B]` | 2 | two separate pairs |
| I | `aAa` | — | 0 | letter case matters |
| J | `aAAa` | 2-3 `[A]` | 1 | a pair of capitals in the middle |
| K | two spaces | 1-2 `[ ]` | 1 | a pair of spaces |
| L | `...` | 1-2 `[.]`, 2-3 `[.]` | 2 | repeated punctuation |
| M | `bookkeeper` | 2-3 `[o]`, 4-5 `[k]`, 6-7 `[e]` | 3 | three different repetitions |
| N | `1233` | 3-4 `[3]` | 1 | a repeated digit at the end |

**Automatic tests and your own runs.** Every case is checked automatically by a check program. It has the same report as the reference solution, but it reads the text from the input as one line, with `std::getline` from lesson 2.7. An empty text is an empty line in it, not missing data. It's only a checking tool, not part of the mission. The check program and its results are in [Example solutions](#example-solutions), because they contain the solution.

</details>

An example solution is in [Example solutions](#example-solutions).

## 7. Find the bug: lost overlapping pairs

Do this task **after the mission**: the program below contains almost the whole algorithm of the mission. It reads the text from the input as one line, like the check program, and prints no question: after you start it, type the text and press **Enter**. The requirement: overlapping pairs count too.

<details>
<summary>The program to check: open it after writing your own program</summary>

<!-- example: pairs_skip_bug -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>

int main() {
    std::string text{};
    std::getline(std::cin, text);

    if (std::cin.fail()) {
        std::cout << "Input could not be read\n";
    } else {
        int repeated_pairs{0};

        std::cout << "Characters: " << text.size() << "\n";

        for (std::size_t index{1}; index < text.size(); ++index) {
            if (text[index] == text[index - 1]) {
                std::cout << "Pair " << index << "-" << index + 1 << ": [" << text[index] << "]\n";
                ++repeated_pairs;
                ++index;
            }
        }

        std::cout << "Repeated pairs: " << repeated_pairs << "\n";
    }
}
```

1. **Predict** the report for `AABB`, `AAA` and `AAAA`.
2. Run the program for `AABB`. Is the report correct?
3. Run it for `AAA`. Trace the values of `index` in a table: which comparison didn't run?
4. Run it for `AAAA`.
5. Point to the statement that skips a comparison.
6. Fix the program.
7. Run the fixed program for `AAA` and `AAAA`, the texts that revealed the bug. The result for `AABB` is checked automatically.

</details>

The program's output before the fix, and the fixed program, are in [Example solutions](#example-solutions).

## 8. When something goes differently

| What you see | What it means | What to do |
|---|---|---|
| `comparison of integers of different signs` | An `int` index is compared with `size()`. This warning appears only with additional warnings turned on (lesson 6.3). | Declare the index as `std::size_t` (lesson 6.3). |
| The positions in the report are one too small, for example `Pair 2-3` instead of `Pair 3-4` | The program prints indices instead of positions. | The pair at index `index` is positions `index` and `index + 1`. |
| `"AAA"` gives one pair instead of two | The program skips a comparison after finding a pair (section 7). | Every index from 1 to the end must be compared. |
| A pair of `'A'` and `'a'` is counted | The program compares the characters without telling letter case apart, for example through letter ranges. | Compare exactly: `text[index] == text[index - 1]`. |
| Strange characters, or the program ends unexpectedly | Probably a read outside the text: an index greater than `size()`, or `index - 1` for index 0. | A loop over neighbours starts at index 1 and has the condition `index < text.size()`. |
| A `Pair` line for spaces looks empty | A space is invisible without the brackets. | Print the character in square brackets, as in the requirements. |

## 9. Explain

Answer in your own words, preferably in writing. Only then compare with the example answers.

1. Why does the first character have the index 0, and how do you work out the position for a person from the index?
2. What does `text[index]` mean, and what type is the result?
3. What condition must the index of a character that belongs to the text meet?
4. Why do we check `empty()` before reading the last character?
5. What is a `std::size_t` index for?
6. When do you choose a range-based loop, and when an index loop?
7. Why does comparing neighbours start at index 1, and how many pairs does a three-character text have?
8. Why does `"AAA"` give two identical pairs?
9. Do `'A'` and `'a'` form a pair? And two neighbouring spaces?
10. Why doesn't this program always analyse a text with Polish letters correctly?

<details>
<summary>Example answers</summary>

1. Because in C++ an index is the distance from the start of the text: the first character is 0 positions from the start. The position for a person is `index + 1`.
2. The character of the text at the given index. The result is of type `char`.
3. `index < text.size()`. For a `std::string`, reading `text[text.size()]` is allowed, but it gives a special null character that isn't part of the text's contents.
4. Because an empty text has no last character, and `size() - 1` for a size of 0 doesn't give −1, but a huge number, because the result of `size()` is unsigned.
5. Because that's the type of the result of `size()`. We don't mix it with `int`. Storing `size()` in an `int` with `{}` is a narrowing conversion, which the compiler rejects. Comparing an `int` with `size()` is valid C++, but before the comparison the `int` is converted to an unsigned type, so a negative number would give a wrong result. The compiler warns about it only with additional warnings turned on (lesson 6.3).
6. A range-based loop when you need only the successive characters, as in lesson 7.1. An index loop when you need the position or a neighbour.
7. Because the character at index 0 has no predecessor. A three-character text has two pairs: indices 0–1 and 1–2.
8. Because the middle `A` belongs to two pairs: with the first and with the last character. Each comparison of neighbours counts separately.
9. `'A'` and `'a'` don't: they're different characters. Two spaces do: they're two identical characters.
10. Because in UTF-8 a Polish letter takes several `char` elements. Positions and comparisons apply to `char` elements, not to the letters a person sees. That's why the data in this lesson is ASCII.

</details>

## Summary

- `text[index]` reads the character of the text at the given index. Indices start at 0, and the position for a person is `index + 1`.
- A character that belongs to the text has an index with `index < text.size()`.
- The first character is `text[0]`, the last `text[text.size() - 1]`, both only for a non-empty text.
- A loop over positions: `for (std::size_t index{0}; index < text.size(); ++index)`, with `std::size_t` from `<cstddef>`.
- You go through pairs of neighbours from index 1: `text[index - 1]` and `text[index]`. That loop is safe for an empty and a one-character text.
- You compare characters exactly with `==`: letter case matters, and a space is an ordinary character.
- Pairs can overlap: one character can belong to two neighbouring pairs.
- Positions apply to `char` elements, so the analysis is correct for ASCII text.

## What's next

In this lesson the text was only read. In the next lesson a function will get a text through `const std::string&` and build a new text from it: [Lesson 7.3: A function creates a new text](lesson_03_a_function_creates_a_new_text.en.md).

---

## Example solutions

Look here **after your own attempt**. Your names may differ, as long as the standard output is as required.

<details>
<summary>Section 6: the mission, a map of repeated characters</summary>

<!-- example: repeated_pairs -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>

int main() {
    const std::string text{"coffee 111"};

    int repeated_pairs{0};

    std::cout << "Characters: " << text.size() << "\n";

    for (std::size_t index{1}; index < text.size(); ++index) {
        if (text[index] == text[index - 1]) {
            std::cout << "Pair " << index << "-" << index + 1 << ": [" << text[index] << "]\n";
            ++repeated_pairs;
        }
    }

    std::cout << "Repeated pairs: " << repeated_pairs << "\n";
}
```

1. **An index loop**, because we need the position and the previous character, which a range-based loop doesn't give.
2. **Starting at index 1**, because each pair is a character with the previous one, and the first character has no predecessor. For an empty and a one-character text the loop makes no passes.
3. **`std::size_t`**, because, as in lesson 6.3, the index is compared with the result of `size()`.
4. **The previous character** is `text[index - 1]`. For every index from 1 upwards, that index belongs to the text.
5. **Comparing characters** with `==` checks whether it's exactly the same character: `'A'` and `'a'` are different.
6. **Positions:** the pair is the indices `index - 1` and `index`, which are the positions `index` and `index + 1`.
7. **`"AAA"` gives two pairs**, because the loop compares the indices 0–1, then 1–2. Both comparisons come out "the same".
8. **We don't skip indices:** after finding a pair, the loop moves on only to the next index, through the `++index` in the header. That way the character from the previous pair takes part in the next comparison.
9. **Spaces and punctuation** are ordinary characters, so `==` treats them like letters. The brackets in the report show that a pair is made of spaces.
10. **The ASCII limit:** positions and comparisons apply to `char` elements. A Polish letter in UTF-8 is several such elements, so the positions wouldn't match the letters a person sees.

Pairs can also be detected differently, for example by comparing a character with the next one in a loop with a different condition, as long as no comparison reaches outside the text and overlapping pairs are counted.

**The check program** checks every case in the list of check cases. The report and the loop are the same as above, apart from the indentation. The text is read from the input as one line with `std::getline`, so it has no `const`.

<!-- example: repeated_pairs_check -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>

int main() {
    std::string text{};
    std::getline(std::cin, text);

    if (std::cin.fail()) {
        std::cout << "Input could not be read\n";
    } else {
        int repeated_pairs{0};

        std::cout << "Characters: " << text.size() << "\n";

        for (std::size_t index{1}; index < text.size(); ++index) {
            if (text[index] == text[index - 1]) {
                std::cout << "Pair " << index << "-" << index + 1 << ": [" << text[index] << "]\n";
                ++repeated_pairs;
            }
        }

        std::cout << "Repeated pairs: " << repeated_pairs << "\n";
    }
}
```

Each case is one line of input, in the order of the list of check cases, from A to N. Case B is an empty line, and case K is a line with two spaces.

<!-- input: repeated_pairs_check -->
```text
coffee 111
```

<!-- output: repeated_pairs_check -->
```text
Characters: 10
Pair 3-4: [f]
Pair 5-6: [e]
Pair 8-9: [1]
Pair 9-10: [1]
Repeated pairs: 4
```

<!-- input: repeated_pairs_check -->
```text

```

<!-- output: repeated_pairs_check -->
```text
Characters: 0
Repeated pairs: 0
```

<!-- input: repeated_pairs_check -->
```text
A
```

<!-- output: repeated_pairs_check -->
```text
Characters: 1
Repeated pairs: 0
```

<!-- input: repeated_pairs_check -->
```text
AB
```

<!-- output: repeated_pairs_check -->
```text
Characters: 2
Repeated pairs: 0
```

<!-- input: repeated_pairs_check -->
```text
AA
```

<!-- output: repeated_pairs_check -->
```text
Characters: 2
Pair 1-2: [A]
Repeated pairs: 1
```

<!-- input: repeated_pairs_check -->
```text
AAA
```

<!-- output: repeated_pairs_check -->
```text
Characters: 3
Pair 1-2: [A]
Pair 2-3: [A]
Repeated pairs: 2
```

<!-- input: repeated_pairs_check -->
```text
AAAA
```

<!-- output: repeated_pairs_check -->
```text
Characters: 4
Pair 1-2: [A]
Pair 2-3: [A]
Pair 3-4: [A]
Repeated pairs: 3
```

<!-- input: repeated_pairs_check -->
```text
AABB
```

<!-- output: repeated_pairs_check -->
```text
Characters: 4
Pair 1-2: [A]
Pair 3-4: [B]
Repeated pairs: 2
```

<!-- input: repeated_pairs_check -->
```text
aAa
```

<!-- output: repeated_pairs_check -->
```text
Characters: 3
Repeated pairs: 0
```

<!-- input: repeated_pairs_check -->
```text
aAAa
```

<!-- output: repeated_pairs_check -->
```text
Characters: 4
Pair 2-3: [A]
Repeated pairs: 1
```

<!-- input: repeated_pairs_check -->
```text
  
```

<!-- output: repeated_pairs_check -->
```text
Characters: 2
Pair 1-2: [ ]
Repeated pairs: 1
```

<!-- input: repeated_pairs_check -->
```text
...
```

<!-- output: repeated_pairs_check -->
```text
Characters: 3
Pair 1-2: [.]
Pair 2-3: [.]
Repeated pairs: 2
```

<!-- input: repeated_pairs_check -->
```text
bookkeeper
```

<!-- output: repeated_pairs_check -->
```text
Characters: 10
Pair 2-3: [o]
Pair 4-5: [k]
Pair 6-7: [e]
Repeated pairs: 3
```

<!-- input: repeated_pairs_check -->
```text
1233
```

<!-- output: repeated_pairs_check -->
```text
Characters: 4
Pair 3-4: [3]
Repeated pairs: 1
```

</details>

<details>
<summary>Section 7: the output before the fix, and the fixed program</summary>

Before the fix, for `AABB`:

<!-- input: pairs_skip_bug -->
```text
AABB
```

<!-- output: pairs_skip_bug -->
```text
Characters: 4
Pair 1-2: [A]
Pair 3-4: [B]
Repeated pairs: 2
```

For `AAA`:

<!-- input: pairs_skip_bug -->
```text
AAA
```

<!-- output: pairs_skip_bug -->
```text
Characters: 3
Pair 1-2: [A]
Repeated pairs: 1
```

For `AAAA`:

<!-- input: pairs_skip_bug -->
```text
AAAA
```

<!-- output: pairs_skip_bug -->
```text
Characters: 4
Pair 1-2: [A]
Pair 3-4: [A]
Repeated pairs: 2
```

| Pass | `index` at the comparison | Positions compared | A pair? | `index` after the body and after the header's `++index` |
|---|---|---|---|---|
| 1 | 1 | 1–2 | yes | 2, then 3 |
| — | 3 | — | the condition `3 < 3` gives `false` | end |

- For `AABB` the result is correct: the pairs are separate, so the skipped comparison, positions 2–3 (`A` and `B`), wouldn't have been a pair anyway.
- For `AAA` the skipped comparison, positions 2–3, **is** a pair: the result is 1 instead of 2. For `AAAA` the program finds the pairs 1–2 and 3–4 but loses 2–3: the result is 2 instead of 3.
- **The cause:** the extra `++index;` in the body after finding a pair. Together with the `++index` in the header it moves the index on by two, so the next comparison doesn't run. The program assumes separate pairs, but the requirement is about overlapping ones.
- **The fix:** remove `++index;` from the body. Only the loop header changes the index.

There's no read outside the text here: after the extra step, the condition `index < text.size()` still checks the index before any read.

The fixed program is the check program from section 6: it differs from the buggy program only in that one line. For all three texts it gives the results from the list of check cases: cases H, F and G.

</details>

**Previous lesson:** [Lesson 7.1: First characters: `char` and going through a `std::string`](lesson_01_first_characters.en.md) · **Next lesson:** [Lesson 7.3: A function creates a new text](lesson_03_a_function_creates_a_new_text.en.md) · [Course overview](../../README.en.md)

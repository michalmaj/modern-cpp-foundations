# Lesson 1.3: A program from a blank page

[Polski](lesson_03_a_program_from_a_blank_page.md) · **English** · [Course overview](../../README.en.md)

> **Module 1, lesson 3** · about 75 minutes
> **You need:** the `cpp-workspace` folder and the original `lesson_05_first_program` project from [lesson 1.1](lesson_01_first_program_inside.en.md), and the way of working from [lesson 1.2](lesson_02_when_the_compiler_complains.en.md).
> **Pilot version:** the CLion steps follow the CLion 2026.2 documentation. Button names in your version may differ slightly.

## Before you start

This lesson assumes that after lessons 1.1 and 1.2:

- you understand a program that prints text: `#include <iostream>`, `main`, `std::cout << "…";` statements, `\n` and the semicolon;
- you can build a program, run it and compare its output with the expected one;
- when there is a compile error, you work in the loop from lesson 1.2: **see the problem → read the diagnostics → form a hypothesis → fix one thing → build again → check the result**.

## The situation

So far there has always been a ready program, or almost ready code. Today you'll start from an **empty file** `main.cpp` and write a whole program in it yourself.

You'll also learn four small new things, because many simple programs can't be written without them: how to print a quote `"`, how to print a backslash `\`, how to add a comment, and what `return 0;` at the end of `main` means.

After this lesson you will:

- start from an empty `main.cpp` and write the program skeleton on your own;
- write a program that prints several lines in a given order;
- print `"` and `\` inside text, and tell what is in the code apart from what appears in the output;
- add comments that help the reader, knowing that they are not statements;
- explain what a program's exit code is and how it differs from the text the program prints;
- explain every important line of your own program.

## 1. Prepare an empty `main.cpp`

"From a blank page" means here: **you write `main.cpp` yourself**. You take `CMakeLists.txt` ready-made, the same as always.

1. In `cpp-workspace`, create a folder `lesson_1_3`.
2. Copy `main.cpp` and `CMakeLists.txt` into it from the original course folder `lesson_05_first_program`, as in lessons 1.1 and 1.2.
3. Open `cpp-workspace/lesson_1_3` in CLion and check that the CMake window says `Clang 22`.
4. Open `main.cpp` in CLion's editor. Select all the text (<kbd>Ctrl</kbd> + <kbd>A</kbd>, on macOS <kbd>⌘ Cmd</kbd> + <kbd>A</kbd>) and delete it with <kbd>Delete</kbd> or <kbd>Backspace</kbd>.

You delete the file's **content**, not the file itself. Don't delete anything in the file window: `main.cpp` and `CMakeLists.txt` must stay in the folder. The programs from lessons 1.1 and 1.2 are in their own folders, and nothing happens to them.

Don't build the empty file yet. A program without `main` won't build, and that error comes from a different tool than the compiler. We'll come back to it in lesson 1.4.

## 2. Recall the program skeleton

Don't look at the earlier lessons. Answer from memory, preferably on paper, and only then check.

**1.** What must stand at the very top of the file so that the compiler knows `std::cout`? Does that line end with a semicolon?

<details>
<summary>Check</summary>

`#include <iostream>`. It's a preprocessor directive, not a statement, so it doesn't end with a semicolon.

</details>

**2.** How does the part of the program that the computer runs after starting begin, and how does it end?

<details>
<summary>Check</summary>

It begins with `int main() {` and ends with the brace `}`. You write the statements between them.

</details>

**3.** What does a statement look like that prints one line of text and moves to the next? What four parts does it have?

<details>
<summary>Check</summary>

`std::cout << "text\n";` – where the text is sent (`std::cout`), "send to" (`<<`), the text in quotes ending with `\n`, and the semicolon.

</details>

## 3. Your first program from a blank page

The café on the corner needs a program that prints a sign for its door. **In the empty `main.cpp`, write a whole program** that prints exactly:

<!-- output: coffee_corner -->
```text
COFFEE CORNER
Open: 8:00 - 16:00
Please come in!
```

You only need what you already know. Don't copy code from earlier lessons: type it on the keyboard.

When you're done: **Build | Build Project**, then **Run**. Compare the output with the expected one, character by character. If the build fails, work in the loop from lesson 1.2.

<details>
<summary>Hint 1</summary>

Start with the skeleton from section 2: three elements, with no statement inside. Only then add the statements.

</details>

<details>
<summary>Hint 2</summary>

Write the skeleton and one statement, for the first line, and build the program. Once it works, add the others. A small step is easier to check.

</details>

An example solution is in [Example solutions](#example-solutions). Look there only after a successful attempt.

**Stop for a moment.** That was your first program written entirely on your own, from the first line to the last, without a ready model.

## 4. A quote and a backslash in text

### The quote

The program should print:

<!-- output: press_one -->
```text
Press "1" to start.
```

The first attempt that comes to mind:

<!-- broken: press_one_plain at=4:26 errors=2 error=^expected ';' after expression$ -->
```cpp
#include <iostream>

int main() {
    std::cout << "Press "1" to start.\n";
}
```

**Predict:** will this program build? Then check: replace the content of `main.cpp` with it and build. Don't worry about the café program, you'll write it again in section 6.

Go through the loop from lesson 1.2. The message talks about a missing semicolon, and yet there is a semicolon at the end of the line. Look at the **position** the compiler points to. What stands just before it?

<details>
<summary>Explanation: read it after your own attempt</summary>

The compiler reads text from a `"` to the **next** `"`. So the text `"Press "` ends at the second quote. Right after it stands `1`, and the compiler expected the end of the statement there. Hence `expected ';' after expression` at the position where `1` begins.

The message points to the right **place**, but its suggestion, a semicolon, is not the solution here. The hypothesis has to explain the cause: the second quote ended the text too early.

The same problem gives a second error right next to it, at position 27, and two `warning:` lines (a warning: the compiler noticed something suspicious, but a warning alone doesn't stop the build). They all have one cause, as in lesson 1.2: fix it, and they disappear together.

</details>

For a quote to be **part of the text** and not its end, put a backslash before it: `\"`.

<!-- example: press_one -->
```cpp
#include <iostream>

int main() {
    std::cout << "Press \"1\" to start.\n";
}
```

The code has `\"`, and the output shows just `"`.

### The backslash

**Predict** what this program prints, and write your answer down. Then run it.

<!-- example: path_plain -->
```cpp
#include <iostream>

int main() {
    std::cout << "C:\new\notes.txt\n";
}
```

<details>
<summary>The program's output</summary>

<!-- output: path_plain -->
```text
C:
ew
otes.txt
```

</details>

The program built, but printed something other than the code suggests. Inside text, a backslash `\` starts a **special notation**: together with the next character, it means something other than those two characters on their own. So the `\n` in the middle of the path did what it always does: it moved to a new line. The compiler reported no error, because the code is valid C++; it just does something other than we wanted (lesson 1.2).

To print one backslash, write **two** in the text: `\\`.

<!-- example: path_fixed -->
```cpp
#include <iostream>

int main() {
    std::cout << "C:\\new\\notes.txt\n";
}
```

<!-- output: path_fixed -->
```text
C:\new\notes.txt
```

### Code and output

| In the code, inside `"…"` | In the program's output |
|---|---|
| `\n` | a move to a new line |
| `\"` | `"` |
| `\\` | `\` |

C++ has a few more notations like these. You'll learn them when you need them. These three are enough for most texts.

## 5. Comments

A **comment** is a note for the people reading the code. It starts with `//` and lasts to the end of the line. The compiler skips it, so a comment **is not a statement** and does nothing while the program runs.

**Predict** how many lines this program prints, and which ones:

<!-- example: comments -->
```cpp
#include <iostream>

int main() {
    // The sign hangs on the door, so every line must stay short.
    std::cout << "COFFEE CORNER\n";
    std::cout << "Comments start with // in C++.\n";
}
```

<details>
<summary>The program's output</summary>

<!-- output: comments -->
```text
COFFEE CORNER
Comments start with // in C++.
```

</details>

- The first line in `main` is a comment: it prints nothing.
- `//` **inside quotes** is not a comment, just ordinary text. The compiler sees the `"` first and knows it's text.

**A good comment** says what the code itself doesn't show: why something is done this way. A comment `// prints COFFEE CORNER` above `std::cout << "COFFEE CORNER\n";` only repeats the code, so it doesn't help. Programs in this course will have few comments, and only where something needs explaining.

**An observation:** in this program, put `//` at the start of the second statement, build it and run it. That line disappears from the output, because the statement has become a comment. This is how you can temporarily **switch off** a piece of code, for example while looking for the cause of a problem. That's different from a comment that explains something. After the observation, delete the `//` so that the statement works again.

## 6. `return 0;` and the exit code

Every time a program finished, CLion added `Process finished with exit code 0` below its output. Where does that `0` come from?

- `main` is a **function**: a named piece of a program. The system runs the function `main` when your program starts.
- When it finishes, `main` hands **one whole number** to whoever started the program: the **exit code**. The word `int` before `main` means exactly that: "integer", a whole number. You'll learn about types properly in Module 2.
- By convention, `0` means "everything is fine". Another number means "something went wrong", and what exactly is up to the program's author.
- The statement `return 0;` ends `main` and hands over the code `0`.
- **When the program reaches the end of `main` without a `return`, it works the same as `return 0;`.** That's why all the programs so far ended with exit code 0, although they had no `return`. So in `main` you may write `return 0;` at the end to show this explicitly, or leave it out. Both versions are correct.

**An experiment.** Write the café program from section 3 again, from memory. It's good practice. Add `return 3;` to it as the last statement in `main`, before `}`. Build and run.

<!-- example: coffee_corner_exit_3 exit=3 -->
```cpp
#include <iostream>

int main() {
    std::cout << "COFFEE CORNER\n";
    std::cout << "Open: 8:00 - 16:00\n";
    std::cout << "Please come in!\n";
    return 3;
}
```

**Predict:** will the program's output change? And the last line in the Run window?

<details>
<summary>What happened</summary>

<!-- output: coffee_corner_exit_3 -->
```text
COFFEE CORNER
Open: 8:00 - 16:00
Please come in!
```

The program printed the same three lines as before, and CLion showed `Process finished with exit code 3`. The exit code **is not part of the program's output**: the program doesn't print it, it hands it to the system. The `Process finished …` line is added by CLion.

</details>

Finally, change `return 3;` to `return 0;`. From now on you may end `main` with `return 0;`.

## 7. Mission: a cinema ticket

A cinema wants to print a ticket from a program. In `cpp-workspace`, create a folder `cinema_ticket`, copy `main.cpp` and `CMakeLists.txt` into it from the original `lesson_05_first_program`, open it in CLion and check `Clang 22`. Then **delete the whole content of `main.cpp`**, as in section 1, and write the program from a blank page.

The program must print exactly:

<!-- output: cinema_ticket -->
```text
CINEMA TICKET
Film: "The Long Night"
Row 7, seat 12
File: C:\tickets\night.txt
Enjoy the film!
```

**You may use:** `#include <iostream>`, `int main() { … }`, `std::cout << "…";`, `\n`, `\"`, `\\`, `//` comments and `return 0;`. Nothing else is needed.

### Success criteria

- `main.cpp` was written from an empty file, without copying earlier programs.
- The program builds without errors and prints **exactly** the five lines above: the same characters, quotes and backslashes, and no extra lines.
- CLion shows `Process finished with exit code 0`.
- The program has at least one comment that explains something non-obvious instead of repeating the code.
- You can explain every line of the program: what it does and why it is written exactly this way.

<details>
<summary>Hint 1</summary>

The skeleton first, then one line of the ticket at a time. After each statement you add, build the program and compare the output.

</details>

<details>
<summary>Hint 2</summary>

Go through the expected output character by character. Which characters have a special meaning inside text in C++? How many of them are in each line?

</details>

### Variant: check that you understand your own code

Without looking at the solution, change your program so that it prints:

<!-- output: cinema_ticket_variant -->
```text
CINEMA TICKET
Film: "The Short Day"
File: C:\tickets\day.txt
Row 3, seat 4
Enjoy the film!
```

Two lines changed, and two others swapped places. If you understand your program, a few changes are enough.

Example solutions for the mission and the variant are in [Example solutions](#example-solutions).

## 8. When something goes differently

| What you see | What it means | What to do |
|---|---|---|
| An error in a line with a quote inside the text, although the message talks about something else, for example a semicolon or `invalid suffix on literal` (on Windows, the latter may be a `warning`) | A quote in the middle of the text ended it too early. | Check that every `"` that should appear in the output is written as `\"`. |
| The program builds, but letters are missing from a path, or there is a new line or a gap | A single `\` with the next letter is a special notation, for example `\n` (a new line) or `\t` (a gap, called a tab). | Write every backslash that should appear in the output as `\\`. |
| The build fails, and `main.cpp` is almost empty or has no `main` | Without `main`, no program is created. This error comes from a different tool than the compiler (lesson 1.4). | Write the program skeleton with `int main() { … }`. |
| A line disappeared from the output | The statement starts with `//`, so it's a comment. | Remove the `//` before the statement. |
| CLion shows an `exit code` other than 0 | `main` returns a different number, for example `return 3;`. | Change it to `return 0;` or remove the `return`. |
| `main.cpp` or `CMakeLists.txt` is gone | The file was deleted instead of its content. | Copy it again from the original `lesson_05_first_program`. |

## 9. Explain

Answer in your own words, preferably in writing. Only then compare with the example answer.

**1.** The code says `"C:\\tickets\\night.txt\n"`. How many backslashes appear in the output, and why?

<details>
<summary>Example answer</summary>

Two. Each `\\` in the text means one `\` in the output. The `\n` at the end prints no backslash; it moves to a new line.

</details>

**2.** Can adding a comment change the program's output? What about putting `//` before a statement?

<details>
<summary>Example answer</summary>

A comment changes nothing, because the compiler skips it. Putting `//` before a statement does change the output, because the statement becomes a comment and is no longer run.

</details>

**3.** A program printed "Everything went wrong!", and CLion showed `exit code 0`. Is that a contradiction?

<details>
<summary>Example answer</summary>

No. The text is the program's output, and the exit code is a separate number handed to the system. A program can print any text and end with code 0, because the two are independent.

</details>

**4.** Why did all the programs from lessons 1.1 and 1.2 end with code 0, although they had no `return 0;`?

<details>
<summary>Example answer</summary>

Because when a program reaches the end of `main` without a `return`, it works the same as `return 0;`.

</details>

**5.** Choose the line of the mission that was hardest for you, and explain each of its characters that doesn't appear in the output.

<details>
<summary>Example answer</summary>

For example `std::cout << "Film: \"The Long Night\"\n";`. Not in the output: `std::cout <<` (sending the text), the quotes that open and close the text, the backslashes before the inner quotes (`\"` gives just `"`), `\n` (a move to a new line) and the semicolon (the end of the statement).

</details>

## Summary

- You start a program from a blank page with the skeleton: `#include <iostream>`, `int main() {`, `}`. You add statements one at a time and build after each.
- Inside text, `\` starts a special notation: `\n` is a new line, `\"` is a quote, `\\` is one backslash. What you see in the code isn't always what appears in the output.
- A `//` comment is a note for people, not a statement. Write one where something needs explaining.
- `main` hands the system an exit code: `0` means "fine". `return 0;` does this explicitly; the end of `main` without a `return` works the same. The exit code isn't part of the program's output.

After this lesson you can say: **"I can write a small C++ program on my own, fix basic errors and check that it works."**

## What's next

Every time, you click **Build** and a program appears. In lesson 1.4 you'll see what happens along the way: how source code becomes an executable, and what `CMakeLists.txt` describes. **Lesson 1.4 is in preparation.**

---

## Example solutions

Look here **after your own attempt**. Your code may differ, for example in comments, empty lines, or whether there is a `return 0;` at the end, and still be right, as long as it meets the criteria.

<details>
<summary>Section 3: the café sign</summary>

<!-- example: coffee_corner -->
```cpp
#include <iostream>

int main() {
    std::cout << "COFFEE CORNER\n";
    std::cout << "Open: 8:00 - 16:00\n";
    std::cout << "Please come in!\n";
}
```

A three-part skeleton, with three statements in it, in the order of the output lines. Each text ends with `\n`.

</details>

<details>
<summary>Section 7: the mission, a cinema ticket</summary>

<!-- example: cinema_ticket -->
```cpp
#include <iostream>

int main() {
    std::cout << "CINEMA TICKET\n";
    std::cout << "Film: \"The Long Night\"\n";
    std::cout << "Row 7, seat 12\n";
    // Each \\ in the code prints one backslash.
    std::cout << "File: C:\\tickets\\night.txt\n";
    std::cout << "Enjoy the film!\n";
    return 0;
}
```

- The quotes around the film title are part of the text, so each is written as `\"`.
- In the path, each `\` is written as `\\`. A single one would give `\t` (a tab) and `\n` (a new line) instead of letters.
- The comment explains the line that might surprise a reader.
- `return 0;` at the end is optional; it shows explicitly that the program ends correctly.

</details>

<details>
<summary>Section 7: the variant</summary>

<!-- example: cinema_ticket_variant -->
```cpp
#include <iostream>

int main() {
    std::cout << "CINEMA TICKET\n";
    std::cout << "Film: \"The Short Day\"\n";
    // Each \\ in the code prints one backslash.
    std::cout << "File: C:\\tickets\\day.txt\n";
    std::cout << "Row 3, seat 4\n";
    std::cout << "Enjoy the film!\n";
    return 0;
}
```

The texts of two statements changed, and two others swapped places. The comment moved together with the line it explains.

</details>

**Previous lesson:** [Lesson 1.2: When the compiler complains](lesson_02_when_the_compiler_complains.en.md) · **Next lesson:** in preparation · [Course overview](../../README.en.md)

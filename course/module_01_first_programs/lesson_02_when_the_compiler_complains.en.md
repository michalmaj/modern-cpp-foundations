# Lesson 1.2: When the compiler complains

[Polski](lesson_02_when_the_compiler_complains.md) · **English** · [Course overview](../../README.en.md)

> **Module 1, lesson 2** · about 60–75 minutes
> **You need:** the `cpp-workspace` folder and the original `lesson_05_first_program` project from [lesson 1.1](lesson_01_first_program_inside.en.md).
> **Pilot version:** the CLion steps follow the CLion 2026.2 documentation. Button names in your version may differ slightly.

## Before you start

This lesson assumes that after lesson 1.1:

- you can copy a project into `cpp-workspace`, open it in CLion and check that it says `Clang 22`;
- you understand the statement `std::cout << "…";`: what `std::cout`, `<<`, the text in quotes, `\n` and the semicolon do.

## The situation

Every programmer sees compile errors every day. That's not a failure, just a normal part of the work. The compiler doesn't guess what the code was meant to say: when it doesn't understand something, it stops the build and tells you **where** and **what** doesn't fit.

Today you'll deliberately break a working program in three ways and learn to read these messages. The point is not to memorise three fixes. The point is a **way of working** that also helps with messages you haven't seen yet:

**see the problem → read the diagnostics → form a hypothesis → fix one thing → build again → check the result**

*Diagnostics* are the messages the compiler prints about problems in the code. A *hypothesis* is your guess about the cause, before you check it.

After this lesson you will:

- recognise that a build failed, and tell compiler messages apart from the output of a running program;
- read the file name, line number and position in the line from a message;
- find the first relevant piece of information among many lines of build output;
- form a hypothesis about the cause, fix one thing and check the effect;
- explain why one mistake can produce several messages;
- explain the role of `;`, `#include <iostream>` and `std::` in your programs.

## 1. Prepare a copy for experiments

The programs and the mission from lesson 1.1 stay untouched. To break things, you need a separate copy:

1. In `cpp-workspace`, create a folder `lesson_1_2`.
2. Copy `main.cpp` and `CMakeLists.txt` into it from the original course folder `lesson_05_first_program`, as in lesson 1.1.
3. Open `cpp-workspace/lesson_1_2` in CLion and check that the CMake window says `Clang 22`.
4. Replace the whole content of `main.cpp` with the familiar program from lesson 1.1:

<!-- example: start -->
```cpp
#include <iostream>

int main() {
    std::cout << "Good morning!\n";
    std::cout << "Time to write some C++.\n";
}
```

5. Build it with **Build | Build Project**, then click **Run**. The output:

<!-- output: start -->
```text
Good morning!
Time to write some C++.
```

In this lesson you always **build** first (**Build | Build Project**) and click **Run** only once the build has succeeded. This way you see separately whether the problem is with building or with what the program prints.

**Important:** the code you are about to break is part of the exercise, not an example to keep. After each experiment, you restore the correct program.

## 2. Two different problems

Before you break anything, tell two situations apart:

| | The program doesn't build | The program builds, but prints something other than you want |
|---|---|---|
| What you see | Messages with the word `error` in the **Build** window. No new program is created. | The build succeeds, and the **Run** window shows different text than expected. |
| Who notices the problem | The compiler. | You, when you compare the output with the expected one. |
| Example | A missing semicolon. | A typo in the text, for example `"Good mornign!\n"`, or a missing `\n`. |

The compiler checks whether the code is correctly written C++: whether the statements have the right form and whether it knows the names used. **It doesn't check whether the program does what you want.** Text with a typo is ordinary, valid text to the compiler. That's why a successful build doesn't yet mean the program is right: you always have to check the output.

## 3. Experiment A: a missing semicolon (step by step)

**The change.** In line 4, delete the semicolon at the end. Your `main.cpp` now looks like this:

<!-- broken: no_semicolon at=4:35 errors=1 error=^expected ';' after expression$ -->
```cpp
#include <iostream>

int main() {
    std::cout << "Good morning!\n"
    std::cout << "Time to write some C++.\n";
}
```

**Predict:** will this program build? Write your answer down.

CLion may already underline something in red in the editor. That's CLion analysing the code as you type. The build is what decides, though, so build the program: **Build | Build Project**.

### Step 1. See the problem

The **Build** window shows the build output, roughly like this:

```text
[3/4] Building CXX object CMakeFiles/first_program.dir/main.cpp.o
FAILED: CMakeFiles/first_program.dir/main.cpp.o
/opt/homebrew/opt/llvm@22/bin/clang++ … -c /Users/ola/cpp-workspace/lesson_1_2/main.cpp
/Users/ola/cpp-workspace/lesson_1_2/main.cpp:4:35: error: expected ';' after expression
    4 |     std::cout << "Good morning!\n"
      |                                   ^
      |                                   ;
1 error generated.
ninja: build stopped: subcommand failed.
```

The details will be slightly different for you: the paths, the compiler's name, `main.cpp.obj` instead of `main.cpp.o` on Windows, sometimes `FAILED: [code=1]`. That doesn't matter.

How can you tell that the build failed? There are the words `FAILED` and `error`, and at the end `1 error generated.` and `build stopped`. No new executable was created.

### Step 2. Read the diagnostics

Read from the top and look for **the first piece of information that points to a place in your code**:

- `[3/4] Building CXX object …`: an ordinary build step, as in lesson 0.5;
- `FAILED: …`: which step failed. Here, compiling `main.cpp`;
- the long line with `clang++`: the command that ran the compiler. You can skip it;
- **`…/main.cpp:4:35: error: expected ';' after expression`**: this is the information you need.

Take it apart:

| Part | Meaning |
|---|---|
| `…/main.cpp` | The file with the problem. |
| `4` | The line number. CLion shows line numbers on the left side of the editor. |
| `35` | The position in the line (the column): the 35th character from the left, counting spaces. |
| `error` | The kind of message: an error that prevents the program from being built. |
| `expected ';' after expression` | The description. The expression here is `std::cout << "Good morning!\n"`. |

Below it, the compiler shows that line of code. The `^` marks position 35, right after the closing quote, and on the line below the compiler suggests what is missing there: `;`.

### Step 3. Form a hypothesis

For example: "In line 4, the semicolon after the text is missing, so the compiler doesn't know where the first statement ends."

Why does it matter? The **syntax** of a language is its rules for writing code, and in C++ a `std::cout << …` statement ends with a semicolon. Going to a new line means nothing to the compiler. Without the semicolon it reads on and attaches the `std::cout` from line 5 to the first statement, which no longer makes sense.

**Is the place it points to always the cause?** Here, yes: the compiler pointed exactly to the place where something is missing. That's why there is no wrong character under the `^`, just an empty space. But the compiler notices a problem only when something stops fitting, and that can be later than the mistake itself. So treat the place it points to as **where to start looking**: check it and what comes before it. In experiment B you'll see that the cause can be on a different line entirely.

### Step 4. Fix one thing

Add the semicolon at the end of line 4. Change nothing else.

### Step 5. Build again

**Build | Build Project.** This time there is no `error` in the Build window, and the last step is `Linking CXX executable first_program` (`first_program.exe` on Windows).

### Step 6. Check the result

Click **Run**. The program prints two lines, as in section 1. The hypothesis is confirmed.

## 4. Experiment B: the compiler doesn't know a name

This time you'll do more of the work yourself.

**The change.** Start from the correct program. Delete the first two lines: `#include <iostream>` and the empty line below it. Your `main.cpp`:

<!-- broken: no_include at=2:5 errors=2 error=^use of undeclared identifier 'std'$ -->
```cpp
int main() {
    std::cout << "Good morning!\n";
    std::cout << "Time to write some C++.\n";
}
```

**Predict:** will the program build? Build it (**Build | Build Project**).

**Read the diagnostics yourself.** Find the lines with `main.cpp` and `error` in the Build window and answer:

1. How many `error` messages are there?
2. Which lines and positions do they refer to?
3. What do they say? An *identifier* here means "a name", and *undeclared* means one the compiler doesn't know.

<details>
<summary>Check your answers</summary>

```text
…/main.cpp:2:5: error: use of undeclared identifier 'std'
…/main.cpp:3:5: error: use of undeclared identifier 'std'
2 errors generated.
```

1. Two.
2. Line 2, position 5, and line 3, position 5: where `std` starts in both.
3. "The name `std` was used, but the compiler doesn't know it."

</details>

**Form a hypothesis before you fix anything.** The messages point to lines 2 and 3, but nothing was changed in them. What did change? Write your hypothesis down.

**Explanation.** The compiler reads the file from the top and must know every name you use. `std::cout` isn't built into the language: it's part of the **standard library**, and the compiler only learns about it from the line `#include <iostream>`.

- Lines that start with `#` are **preprocessor directives**: instructions for the build tools, carried out before the actual compiling. **They are not statements of the program.** They don't run while the program runs, they don't stand inside `main`, and they don't end with a semicolon.
- `#include <iostream>` means: "insert here the **declarations** from the part of the standard library called `iostream`". A declaration tells the compiler that something with a given name exists and how to use it. One of these declarations is `std::cout`.
- Without that line, the compiler knows neither `std` nor `std::cout`.

This is the case promised in experiment A: **the cause is somewhere other than the lines the messages point to**. The compiler shows where an unknown name was used, but what's missing is at the very top of the file.

**One mistake, several messages.** One missing line produced two messages, one for each place where `std` is used. If the program had ten such statements, there would be ten messages, and still one mistake. So don't fix each message separately: look for **the common cause**.

**Fix one thing:** restore `#include <iostream>` and the empty line at the top of the file. Build again. Both messages disappear at once, although only one place changed. Click **Run** and check the output.

## 5. Experiment C: `cout` instead of `std::cout`

This time you only get the task. Go through the steps on your own.

**The change.** Start from the correct program. In line 5, delete `std::`, so that only `cout` is left:

<!-- broken: no_std at=5:5 errors=1 error=^use of undeclared identifier 'cout'; did you mean 'std::cout'\?$ -->
```cpp
#include <iostream>

int main() {
    std::cout << "Good morning!\n";
    cout << "Time to write some C++.\n";
}
```

**The task:**

1. Predict whether the program will build.
2. Build it and find the first relevant information: the file, line, position and description.
3. Write down a hypothesis: what is wrong and **why**. "You have to add `std::`" doesn't yet answer the question "why".
4. Fix one thing, build again and check the output.

<details>
<summary>Hint (about the way of working)</summary>

The message has two parts separated by a semicolon. The second one is the compiler's suggestion. Below the message there is also a `note:` line, which is extra information. Which file does it lead to? Is it your file?

</details>

<details>
<summary>Explanation: read it after your own attempt</summary>

```text
…/main.cpp:5:5: error: use of undeclared identifier 'cout'; did you mean 'std::cout'?
    5 |     cout << "Time to write some C++.\n";
      |     ^~~~
      |     std::cout
…/iostream:…: note: 'std::cout' declared here
1 error generated.
```

- **What the message says:** "the name `cout` was used, but the compiler doesn't know it; did you mean `std::cout`?".
- **The `note:` line** leads to the standard library's `iostream` file, to where `std::cout` is declared. Its path and line number depend on the system, because each one has a different standard library. It's not your file, and you don't change anything in it.
- **Why:** the names of the standard library belong to a group of names called `std` (the technical term is *namespace*; you'll learn more about them later). `std::cout` is the full name: "`cout` from the group `std`". Plain `cout` is a **different name** to the compiler, looked up outside that group. Nobody declared it, so the compiler doesn't know it. `#include <iostream>` is in place, so the compiler knows `std::cout`, and that's why it can suggest it.
- **The fix:** restore `std::` in line 5.
- **The compiler's suggestion** was right here, but treat it as a hypothesis to check, not an order. Understand why it makes sense before you accept it.

On the internet you may come across the line `using namespace std;`, which lets you write plain `cout`. This course doesn't use it: the full name `std::cout` tells you right away where it comes from.

</details>

## 6. Mission: a shopping list

Someone wrote a program that should print a shopping list, but the program doesn't build, and maybe that's not all. Repair it.

**Prepare the project:**

1. Create `cpp-workspace/shopping_list` and copy `main.cpp` and `CMakeLists.txt` into it from the original `lesson_05_first_program`.
2. Open it in CLion and check that it says `Clang 22`.
3. Replace the content of `main.cpp` with this code (copy it from here):

<!-- broken: shopping_list_start at=2:5 errors=4 error=^use of undeclared identifier 'std'$ -->
```cpp
int main() {
    std::cout << "SHOPPING LIST\n";
    std::cout << "- bread\n"
    cout << "- milk\n";
    std::cout << "- apples";
    std::cout << "TOTAL: 3 items\n";
}
```

**Goal:** the program builds without errors and prints exactly:

<!-- output: shopping_list -->
```text
SHOPPING LIST
- bread
- milk
- apples
TOTAL: 3 items
```

**The way of working:**

1. Build the program.
2. Read the messages.
3. Choose one problem.
4. Write down a guess about its cause.
5. Make one fix.
6. Build again.
7. Repeat until the program builds **and** prints the expected output.

**Diagnostic log.** Record each fix as one row, for example in your notes:

| # | Symptom: what I see | Guess: why | Fix: one change | Result: what I see after building |
|---|---|---|---|---|
| 1 | | | | |

### Success criteria

- The program builds without any `error`.
- The program prints **exactly** the five expected lines.
- Each row of the log describes one fix, and the program was built again after every fix.
- The log shows which problems the compiler reported, and which one was found only by comparing the output with the expected one.
- You can explain every fix in your own words.

<details>
<summary>Hint 1</summary>

How many different causes can the messages from the first build have? Can several messages have one cause?

</details>

<details>
<summary>Hint 2</summary>

After every fix, read the messages again: new ones may appear, and the line numbers may shift. Once the program finally builds, don't stop: compare the output with the expected one, character by character.

</details>

An example solution, with an example log, is in [Example solutions](#example-solutions).

## 7. When something goes differently

| What you see | What it means | What to do |
|---|---|---|
| A great many messages | Several of them may have one cause. | Start with the first message that points to `main.cpp`. Fix one thing and build again: often several messages disappear at once. |
| New messages appeared after a fix | The compiler got further and noticed something it hadn't checked before. Or the fix introduced a new problem. | Read the messages again. If the fix didn't explain anything, undo it (<kbd>Ctrl</kbd> + <kbd>Z</kbd>, on macOS <kbd>⌘ Cmd</kbd> + <kbd>Z</kbd>) and form a new hypothesis. |
| The message text differs from the lesson | The wording depends on the compiler version and the system. | Look for the same information: the file, line, position and the meaning of the description. |
| The line number doesn't match what you see in the editor | The code changed since the last build, for example a line was added at the top. | Build again and read the new messages. |
| The build succeeded, but the output differs from the expected one | This is not a problem for the compiler: the code is valid C++, but it does something other than you want. | Compare the output with the expected one character by character, and find the statement that prints the differing part. |
| In the terminal, the program prints an old result | The last build failed, so the previous executable is still there (lesson 0.5). | Check the build output and fix the errors. Run the program only after a successful build. |

## 8. Explain

Answer in your own words, preferably in writing. Only then compare with the example answer.

**1.** How does a program that doesn't build differ from a program that builds but prints the wrong text? Who notices each of these problems?

<details>
<summary>Example answer</summary>

When the program doesn't build, the compiler reports an `error` and no new program is created. The code isn't valid C++. When the program builds but prints the wrong text, the code is valid C++, but it does something other than we wanted. The compiler won't notice; you see it only by comparing the output with the expected one.

</details>

**2.** What do the numbers in `main.cpp:4:35` mean?

<details>
<summary>Example answer</summary>

Line 4 and position 35 in that line: the place where the compiler noticed the problem.

</details>

**3.** Why did one missing `#include` produce two messages in experiment B? How many fixes were needed?

<details>
<summary>Example answer</summary>

The compiler reported a problem in every place where the unknown name `std` was used, that is, in two statements. There was one cause, so one fix was enough: restoring `#include <iostream>`.

</details>

**4.** How does `#include <iostream>` differ from the statement `std::cout << "…";`?

<details>
<summary>Example answer</summary>

`#include <iostream>` is a preprocessor directive, carried out before compiling: it gives the compiler the declarations from the standard library, including `std::cout`. It doesn't run while the program runs. `std::cout << "…";` is a statement in `main` that runs while the program runs: it prints text.

</details>

**5.** Why is it worth fixing one thing at a time and building after every change?

<details>
<summary>Example answer</summary>

Because then you know what each change did: whether the hypothesis was right and whether the fix broke something. One cause can produce several messages, and new ones can appear after a fix. After many changes at once, it's hard to tell which did what.

</details>

## Summary

- Compile errors are a normal part of programming. A message says **where** (file, line, position) and **what** doesn't fit for the compiler.
- Read the build output from the top and look for the first information that points to a place in your code. That place is where you start looking: the cause can be earlier, even on another line.
- One mistake can produce several messages, and other mistakes can stay invisible until you fix the first one.
- Work in a loop: **see the problem → read the diagnostics → form a hypothesis → fix one thing → build again → check the result**.
- `;` ends a statement. `#include <iostream>` gives the compiler declarations, including `std::cout`. `std::` says that a name comes from the standard library.
- A successful build doesn't mean a correct program: the compiler doesn't check whether the program does what you want. You always have to check the output.

---

## Example solutions

Look here **after your own attempt**. Your order of fixes may differ and still be right, as long as each fix was reasoned and the program prints exactly the expected output.

<details>
<summary>Mission: an example diagnostic log</summary>

| # | Symptom: what I see | Guess: why | Fix: one change | Result: what I see after building |
|---|---|---|---|---|
| 1 | 4 errors `use of undeclared identifier 'std'` in lines 2, 3, 5 and 6. | They are all about the unknown name `std`. `#include <iostream>` is missing: one cause, four messages. | I add `#include <iostream>` and an empty line at the top. | New messages: `expected ';' after expression` in line 5 and `use of undeclared identifier 'cout'` in line 6. They weren't there before. The line numbers moved by 2. |
| 2 | `5:29: error: expected ';' after expression` | The semicolon after the text `"- bread\n"` is missing. | I add `;` at the end of line 5. | One error is left: `cout` in line 6. |
| 3 | `6:5: error: use of undeclared identifier 'cout'; did you mean 'std::cout'?` | `std::` is missing, so `cout` is a name that nobody declared. | I add `std::` before `cout`. | The build succeeds. Run: `- applesTOTAL: 3 items` on one line. |
| 4 | The output differs from the expected one: two lines are glued together. The compiler reported nothing. | The text `"- apples"` doesn't end with `\n`. | I add `\n` to that text. | The output matches the expected one. |

**Why did new errors appear after fix 1?** A compiler that doesn't understand the start of a statement often skips the rest of it, up to the next semicolon. In the original code, the semicolon in line 3 was missing, so that statement ran on to the end of line 4. The `cout` mistake was hidden inside it. So the number of messages doesn't have to equal the number of mistakes, in either direction.

</details>

<details>
<summary>Mission: the code after each fix</summary>

After fix 1:

<!-- broken: shopping_list_after_include at=5:29 errors=2 error=^expected ';' after expression$ -->
```cpp
#include <iostream>

int main() {
    std::cout << "SHOPPING LIST\n";
    std::cout << "- bread\n"
    cout << "- milk\n";
    std::cout << "- apples";
    std::cout << "TOTAL: 3 items\n";
}
```

After fix 2:

<!-- broken: shopping_list_after_semicolon at=6:5 errors=1 error=^use of undeclared identifier 'cout'; did you mean 'std::cout'\?$ -->
```cpp
#include <iostream>

int main() {
    std::cout << "SHOPPING LIST\n";
    std::cout << "- bread\n";
    cout << "- milk\n";
    std::cout << "- apples";
    std::cout << "TOTAL: 3 items\n";
}
```

After fix 3, the program builds, but prints:

<!-- example: shopping_list_builds -->
```cpp
#include <iostream>

int main() {
    std::cout << "SHOPPING LIST\n";
    std::cout << "- bread\n";
    std::cout << "- milk\n";
    std::cout << "- apples";
    std::cout << "TOTAL: 3 items\n";
}
```

<!-- output: shopping_list_builds -->
```text
SHOPPING LIST
- bread
- milk
- applesTOTAL: 3 items
```

After fix 4, that is, the solution:

<!-- example: shopping_list -->
```cpp
#include <iostream>

int main() {
    std::cout << "SHOPPING LIST\n";
    std::cout << "- bread\n";
    std::cout << "- milk\n";
    std::cout << "- apples\n";
    std::cout << "TOTAL: 3 items\n";
}
```

</details>

**Previous lesson:** [Lesson 1.1: The first program, from the inside](lesson_01_first_program_inside.en.md) · **Next lesson:** [Lesson 1.3: A program from a blank page](lesson_03_a_program_from_a_blank_page.en.md) · [Course overview](../../README.en.md)

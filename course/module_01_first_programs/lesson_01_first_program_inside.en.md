# Lesson 1.1: The first program, from the inside

[Polski](lesson_01_first_program_inside.md) · **English** · [Course overview](../../README.en.md)

> **Module 1, lesson 1** · about 60 minutes
> **You need:** the `lesson_05_first_program` project from [lesson 0.5](../module_00_tooling/lesson_05_first_program_in_clion.en.md) and CLion with the `LLVM 22` toolchain you created in lesson 0.5, section 4.
> **Pilot version:** the CLion steps follow the CLion 2026.2 documentation. Button names in your version may differ slightly.

## Before you start

This lesson assumes that after Module 0:

- you can create folders and copy files in the file window;
- you can open a project in CLion, build it and run it (**Run**);
- you know that after changing the code, the program has to be built again before you see the new result.

## The situation

In Module 0 the program was a black box to you: only the text in quotes changed. Today you'll look inside. You'll read `main.cpp` line by line, predict what the program prints, change it, and at the end write your first own C++ statements.

Today's path: **recognise → predict → change → fill in → write → explain**.

After this lesson you will:

- work on your own copy of the project in a `cpp-workspace` folder, not on the course materials;
- point out `main` in a program: the place where your code starts running;
- recognise statements that print text, and their parts: `std::cout`, `<<`, text in quotes and the semicolon;
- predict the order in which a program prints its messages;
- add statements that print text on your own, build the program and check the result.

## 1. Set up your own workspace

The `lesson_05_first_program` folder belongs to the course materials. From today, treat it as the **original**: you don't work in it, you only copy what you need from it. You work on a **copy** in your own workspace folder, `cpp-workspace`.

This way:

- your work stays with you, even if you download the course materials again one day;
- you can always go back to the original example: just copy it again;
- every larger task can have its own folder, so nothing overwrites your earlier work.

**Step 1. Create `cpp-workspace`.** Open your home folder in the file window, as in lesson 0.2: in the terminal type `cd ~`, then:

| Windows | macOS | Linux |
|---|---|---|
| `explorer .` | `open .` | `xdg-open .` |

Create a folder `cpp-workspace` there, and inside it a folder `lesson_1_1`.

**Step 2. Copy the project.** In a second file window, open the course folder `lesson_05_first_program` (downloaded in lesson 0.5). Copy **only two files** from it: `main.cpp` and `CMakeLists.txt`.

1. Click `main.cpp`, hold <kbd>Ctrl</kbd> (on macOS <kbd>⌘ Cmd</kbd>) and click `CMakeLists.txt`. Both files are selected.
2. Copy them: <kbd>Ctrl</kbd> + <kbd>C</kbd> (on macOS <kbd>⌘ Cmd</kbd> + <kbd>C</kbd>).
3. Go to `cpp-workspace/lesson_1_1` and paste: <kbd>Ctrl</kbd> + <kbd>V</kbd> (on macOS <kbd>⌘ Cmd</kbd> + <kbd>V</kbd>).

Use copy and paste, not dragging: dragging can **move** the files instead of copying them.

Don't copy anything else. The build folders (`cmake-build-debug`, `build-terminal` and others) are the build results of that copy of the project, and the hidden `.idea` folder holds CLion's settings for that location. CLion and CMake will create their own for the new copy.

Check that you have this layout:

```text
cpp-workspace
└── lesson_1_1
    ├── CMakeLists.txt
    └── main.cpp
```

**Step 3. Open the copy in CLion.** Choose **File | Open** and select the `cpp-workspace/lesson_1_1` folder. If CLion asks whether to open the project in the same window (**This Window**) or a new one (**New Window**), choose **This Window**. Then, as in lesson 0.5: **Trust Project**, and in the **CMake Profiles** window confirm the **Debug** profile (**OK**).

**Step 4. Check the compiler.** This is a new project, so CLion may have chosen its default toolchain for it. In the **CMake** window, find the line with `The CXX compiler identification is`. It must say **`Clang 22`**. If it says something else:

1. Open the settings (**File | Settings**, on macOS **CLion | Settings**) and go to **Build, Execution, Deployment | CMake**.
2. In the **Debug** profile, choose `LLVM 22` in the **Toolchain** field. The toolchain from lesson 0.5 still exists; you only need to select it for this project.
3. Click **OK** and check the CMake window again.

**Step 5. Start from the original code.** The message was changed in lessons 0.5 and 0.6, so your `main.cpp` may look different. Open `main.cpp` in the copy and check that it looks exactly like this. If not, replace its whole content with this code (copy it from here):

<!-- example: original source=../module_00_tooling/lesson_05_first_program/main.cpp -->
```cpp
#include <iostream>

int main() {
    std::cout << "Hello! My first C++20 program works.\n";
}
```

Click **Run** (▶). The program's output appears in the Run window:

<!-- output: original -->
```text
Hello! My first C++20 program works.
```

Below it, CLion adds `Process finished with exit code 0`. That line doesn't come from your program but from CLion, so this lesson leaves it out of the expected outputs.

Prefer building in the terminal? The commands from [lesson 0.6](../module_00_tooling/lesson_06_same_program_without_clion.en.md) work the same way in the `cpp-workspace/lesson_1_1` folder.

## 2. Recognise: what is in `main.cpp`

The program has five lines, one of them empty. You don't need to understand all of them fully today.

| Line | What it does | Today |
|---|---|---|
| `#include <iostream>` | Adds to the program the part of the C++ **standard library** (ready-made tools that come with the language) that prints text. Without it, the program wouldn't know `std::cout`. | Recognise it. More in lesson 1.2. |
| (empty line) | Nothing. It's only there for readability. | |
| `int main() {` | The start of **`main`**. This is where your code starts running. The brace `{` opens the part where you write statements. | Remember: the code to run goes between `{` and `}`. You'll learn what `int` means later. |
| `std::cout << "Hello! My first C++20 program works.\n";` | A **statement**: one instruction for the computer. This one prints text. | Understand it. We take it apart below. |
| `}` | The brace that closes `main`. When the program gets here, it ends. | Understand it. |

Now the most important line, piece by piece:

<!-- fragment -->
```cpp
std::cout << "Hello! My first C++20 program works.\n";
```

- **`std::cout`** is where the program sends text to be shown: CLion's Run window or the terminal. `std::` means that `cout` comes from the standard library. For now, always write them together: `std::cout`.
- **`<<`** reads here as "send to": send what is on the right to `std::cout`. The arrows show the direction: the text flows left, into `std::cout`.
- **`"…"`** is **text in quotes** (the technical term is *string literal*). The program prints it exactly as written: the same letters, spaces and characters. The quotes themselves only mark where the text starts and ends; they don't appear in the output.
- **`\n`** at the end of the text is not two characters to print but an instruction: "go to a new line". You'll see what it does in section 4.
- **`;`** (the semicolon) ends the statement, a bit like a full stop ends a sentence.

**What can you already change safely, and what should you leave alone for now?**

| You can change | Leave unchanged for now |
|---|---|
| the text between the quotes (in plain English letters, see below) | `#include <iostream>` |
| the number of `std::cout << "…";` statements and their order, as long as they are between `{` and `}` | `int main() {` and the closing `}` |
| | the parts of each statement: `std::cout`, `<<`, the quotes and `;` |

In this module, program messages use only plain English letters, without accented characters such as Polish ones. This is not a limit of C++: the Windows console doesn't always show such characters correctly without extra settings, and we'll deal with that later.

**Check yourself:**

**1.** How many statements are there in `main`?

<details>
<summary>Answer</summary>

One: the line that starts with `std::cout` and ends with a semicolon.

</details>

**2.** Which characters of this statement can you see in the program's output?

<details>
<summary>Answer</summary>

Only the text between the quotes, without `\n`. The quotes, `std::cout`, `<<`, `\n` and `;` tell the computer what to do, but are not printed themselves. Instead of `\n`, the output moves to a new line.

</details>

## 3. Predict: two statements

Replace the whole content of `main.cpp` with this program (copy it from here):

<!-- example: two_lines -->
```cpp
#include <iostream>

int main() {
    std::cout << "Good morning!\n";
    std::cout << "Time to write some C++.\n";
}
```

**Before you click Run, predict:** how many lines will the program print, and in what order? Write your answer down, for example in your notes.

Now click **Run** and compare the output with your prediction.

<details>
<summary>The program's output</summary>

<!-- output: two_lines -->
```text
Good morning!
Time to write some C++.
```

</details>

**What happened?** The program runs the statements in `main` **one after another, from top to bottom**. First, the first statement printed its text and moved to a new line (`\n`); then the second one did the same.

## 4. Change: order and new lines

### Change 1: the order

**Goal:** the program prints the same two messages, but in reverse order:

<!-- output: swapped -->
```text
Time to write some C++.
Good morning!
```

Don't change the text. Only change the order of the statements. In CLion you can cut a whole line (<kbd>Ctrl</kbd> + <kbd>X</kbd>, on macOS <kbd>⌘ Cmd</kbd> + <kbd>X</kbd>, with the cursor on that line) and paste it somewhere else.

Click **Run** and check the output. Then answer for yourself: **why** did the output change, even though no text changed?

### Change 2: without `\n`

In the program after change 1, remove `\n` from the **first** statement, the one with `Time to write some C++.`. Remove only those two characters, `\` and `n`; the closing quote stays.

**Predict:** how many lines will the program print now? Where will `Good morning!` start? Write your answer down, then click **Run**.

<details>
<summary>The program's output</summary>

<!-- output: no_newline -->
```text
Time to write some C++.Good morning!
```

</details>

**What happened?** A new statement doesn't start a new line by itself. The output moves to a new line only when the text contains `\n`. Without it, the second text starts right after the first, not even with a space.

The code for both changes is in [Example solutions](#example-solutions) at the end of the lesson. Look there after your own attempt.

## 5. Fill in: the missing step

The assembly instructions for a lamp have three steps, but the program is missing the middle one. Replace the whole content of `main.cpp` with this incomplete code:

<!-- fragment -->
```cpp
#include <iostream>

int main() {
    std::cout << "Step 1: Open the box.\n";
    _______________________________________
    std::cout << "Step 3: Plug in the lamp.\n";
}
```

**Your task:** replace the line of underscores (`____`) with **your own statement**, so that the program prints exactly:

<!-- output: lamp_steps -->
```text
Step 1: Open the box.
Step 2: Take out the cable.
Step 3: Plug in the lamp.
```

Type this one statement on the keyboard; don't copy it. The code won't build as it is: the underscores are not a C++ statement. You can build the program only once you've filled in the gap.

**Check:** click **Run** and compare the output with the expected one, character by character, including the full stops and capital letters.

<details>
<summary>Hint 1</summary>

Which of the existing lines does almost the same as the missing one should?

</details>

<details>
<summary>Hint 2</summary>

Your statement has the same shape as the `Step 1` line, only with different text in the quotes. `\n` at the end of the text, `;` at the end of the statement.

</details>

An example solution is in [Example solutions](#example-solutions).

## 6. Mission: a parcel label

You're sending a parcel with something fragile in it, and you need a program that prints the label to stick on it.

**Prepare the project.** The mission gets its own folder, so that it doesn't overwrite the exercises in `lesson_1_1`:

1. In `cpp-workspace`, create a folder `parcel_label`.
2. Copy `main.cpp` and `CMakeLists.txt` into it from the **original** course folder `lesson_05_first_program`, as in section 1.
3. Open `cpp-workspace/parcel_label` in CLion and check that the CMake window says `Clang 22` (section 1, step 4).

Your `cpp-workspace` now looks like this:

```text
cpp-workspace
├── lesson_1_1
│   ├── CMakeLists.txt
│   └── main.cpp
└── parcel_label
    ├── CMakeLists.txt
    └── main.cpp
```

**The task.** Change `main.cpp` in `parcel_label` so that the program prints exactly these three lines:

<!-- output: parcel_label -->
```text
TO: Ola Nowak
FROM: Modern C++ Foundations
FRAGILE - HANDLE WITH CARE
```

Print each line with its own statement. You write the code yourself: you already know everything you need.

### Success criteria

- The program prints **exactly** these three lines, in this order: the same letters (capital and small), spaces, colons and dash.
- There are no extra lines, no empty lines, and no text glued together on one line.
- Each line of the output comes from its own statement, and each statement ends with a semicolon.
- The program was built from the `cpp-workspace/parcel_label` folder, and the CMake window says `Clang 22`.
- You can point out which statement prints which line.

<details>
<summary>Hint 1</summary>

How many lines does the output have? That's how many statements you need. Which program in this lesson has the most similar shape?

</details>

<details>
<summary>Hint 2</summary>

Start with one line: make the program print only `TO: Ola Nowak`. Click **Run** and check. Then add the next statement below it and check again. Small steps are easier to check.

</details>

An example solution is in [Example solutions](#example-solutions). Look there only once your program meets all the criteria, or if you're really stuck.

## 7. When something goes differently

When the build fails, CLion shows the compiler's messages in the **Build** window. **Read them from the top** and find the first piece of information that points to a place in your code: the file `main.cpp` and a line number. Start looking for the cause there. [Lesson 1.2](lesson_02_when_the_compiler_complains.en.md) shows how to read these messages.

| What you see | What it means | What to do |
|---|---|---|
| Two messages glued together on one line | The first text is missing `\n`. | Add `\n` at the end of the text, before the closing quote. |
| An extra empty line | One text has `\n` twice, or there is a statement that prints only `\n`. | Each text should end with a single `\n`. |
| The build fails with an error (`error:`) | The compiler doesn't understand some line. | Check one by one: does every statement end with `;`? Does every text have a quote at the start and at the end? Are the statements between `{` and `}`? Are the underscores from section 5 still there? |
| An error on a line with text, although everything looks fine | A quote may be a "curly" one (`“` or `”`), for example after copying text from a document or a chat app. | Delete the quotes and type them on the keyboard in CLion: `"`. |
| The output of a different exercise | A different project is open in CLion. | Check the project name at the top of the CLion window. Open the right folder (**File \| Open**). |
| The CMake window shows a compiler other than `Clang 22` | This project uses a different toolchain. | Section 1, step 4. Then **Tools \| CMake \| Reset Cache and Reload Project**. |
| Different capital letters or a missing space in the output | The program prints the text exactly as written. | Compare the text in the code with the expected output, character by character. |

## 8. Explain

Answer in your own words, preferably in writing. Only then compare with the example answer.

**1.** Why did the messages appear in this order and not another?

<details>
<summary>Example answer</summary>

The program runs the statements in `main` one after another, from top to bottom. The message from the higher statement appears first. After swapping the statements, the order of the messages changed, even though the text stayed the same.

</details>

**2.** What does each statement you added in the mission do?

<details>
<summary>Example answer</summary>

Each one sends one text to `std::cout`, which prints it, and the `\n` at the end of the text moves to a new line. The first prints the recipient, the second the sender, the third the warning.

</details>

**3.** What do you have to do after changing the code to see the new result?

<details>
<summary>Example answer</summary>

Save the file, build the program again and run it. Run in CLion does this in one click: it builds first if needed, then runs. In the terminal, you build (`cmake --build …`) and run the program yourself.

</details>

**4.** Which parts of the program do you already understand, and which will you learn later?

<details>
<summary>Example answer</summary>

I understand: the code runs from `{` to `}` in `main`, from top to bottom; `std::cout << "…";` prints a text; `\n` moves to a new line; `;` ends a statement. For now I only recognise `#include <iostream>`, `int` before `main`, and `std::`. I'll learn what they mean in the next lessons.

</details>

## Summary

- You work on a **copy** of the project in `cpp-workspace`. The course's original stays untouched, and you can always copy it again.
- You write your code in **`main`**, between `{` and `}`. The program runs the statements one after another, from top to bottom.
- `std::cout << "…";` is a **statement** that prints **text in quotes**. The semicolon ends it.
- The text is printed exactly as written. **`\n`** moves to a new line; without it, the next text appears on the same line.
- After changing the code, the program has to be built again; Run in CLion does this for you.

---

## Example solutions

Look here **after your own attempt** and after checking the output. Your solution may differ, for example in empty lines in the code, and still be right, as long as the program prints exactly the expected output.

<details>
<summary>Section 4, change 1: the order</summary>

<!-- example: swapped -->
```cpp
#include <iostream>

int main() {
    std::cout << "Time to write some C++.\n";
    std::cout << "Good morning!\n";
}
```

The texts didn't change; only the order of the statements did. The program runs them from top to bottom, so it prints `Time to write some C++.` first.

</details>

<details>
<summary>Section 4, change 2: without <code>\n</code></summary>

<!-- example: no_newline -->
```cpp
#include <iostream>

int main() {
    std::cout << "Time to write some C++.";
    std::cout << "Good morning!\n";
}
```

The first text doesn't end with `\n`, so the program doesn't move to a new line, and `Good morning!` appears right after the full stop.

</details>

<details>
<summary>Section 5: the missing step</summary>

<!-- example: lamp_steps -->
```cpp
#include <iostream>

int main() {
    std::cout << "Step 1: Open the box.\n";
    std::cout << "Step 2: Take out the cable.\n";
    std::cout << "Step 3: Plug in the lamp.\n";
}
```

The new statement sits between the two existing ones, because its message has to appear between theirs.

</details>

<details>
<summary>Section 6: the mission, a parcel label</summary>

<!-- example: parcel_label -->
```cpp
#include <iostream>

int main() {
    std::cout << "TO: Ola Nowak\n";
    std::cout << "FROM: Modern C++ Foundations\n";
    std::cout << "FRAGILE - HANDLE WITH CARE\n";
}
```

Three lines of output are three statements, in the same order. Each text ends with `\n`, so each line of the label starts on a new line.

</details>

**Previous lesson:** [Lesson 0.6: The same program without CLion](../module_00_tooling/lesson_06_same_program_without_clion.en.md) · **Next lesson:** [Lesson 1.2: When the compiler complains](lesson_02_when_the_compiler_complains.en.md) · [Course overview](../../README.en.md)

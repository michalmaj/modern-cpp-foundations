# Lesson 1.6: From an idea to a working program, on your own

[Polski](lesson_06_from_idea_to_working_program.md) · **English** · [Course overview](../../README.en.md)

> **Module 1, lesson 6: the module test** · about 90 minutes
> **You need:** the `cpp-workspace` folder with the Git repository from [lesson 1.5](lesson_05_save_the_history_of_your_work.en.md), and the original `lesson_05_first_program` project.
> **Pilot version.** The reference solutions and the commands in this lesson are checked automatically on Windows, Ubuntu and macOS. Nothing grades your work automatically: you check it yourself, against the criteria.

## How this test works

This lesson introduces nothing new. You check whether you can go the whole way on your own: from the requirements, through the code, building and checking the output, to saving your work in Git. You'll also diagnose two problems and explain what was done.

The lesson has two parts:

- **Part A: the test.** Only the tasks, the requirements, the expected outputs and the criteria. No hints and no solution code. Everything you need, you know from lessons 1.1–1.5.
- **Part B: checking and discussion.** Hints, example solutions, explanations and a self-assessment. Go there after finishing part A, or when you knowingly decide to stop trying on your own.

Looking at part B, at the earlier lessons or at your notes is not a failure. It's a normal part of learning. Only one thing matters: **note honestly what you did on your own and what with help**. At the end there is a self-assessment that tells them apart. It shows what is worth going over again before Module 2.

**You may use:**

- the terminal, CMake and Ninja (the commands from lessons 0.6 and 1.4);
- CLion as an editor and IDE;
- Git in the terminal (lesson 1.5);
- a `CMakeLists.txt` copied from the original `lesson_05_first_program`. You don't need to write CMake from memory.

---

# Part A: the test

## Task 1: A board for the games night

The city library is organising a board games night and wants to show information in a terminal at the entrance.

**Setup:**

- In `cpp-workspace`, create a new folder `board_games_night`.
- Copy `CMakeLists.txt` into it from the original `lesson_05_first_program`.
- Create an **empty** `main.cpp` in it, and write the whole program yourself.
- Don't change the earlier projects in `cpp-workspace`.

**Requirements:**

- The program prints **exactly** the text below, line by line, including the empty line:

<!-- output: board_games_night -->
```text
BOARD GAMES NIGHT
=================
Where: City Library, room "Blue"
When: Friday, 18:00
Bring: your favourite game

Sign-up sheet: \\library\games\list.txt
Have fun!
```

- The program has at least one comment that explains something non-obvious instead of repeating the code.
- The program ends correctly: exit code 0.
- Build the program and run it. Compare the output with the expected one, character by character.
- When the output matches, **save this version in the Git history**: only this project's source files. Before you save, check what will go into the commit.

## Task 2: A change of plans

The library changed the room and the time, and also wants to encourage people to borrow games. Change your program so that it prints exactly:

<!-- output: board_games_night_changed -->
```text
BOARD GAMES NIGHT
=================
Where: City Library, room "Green"
When: Friday, 19:30
Sign-up sheet: \\library\games\list.txt

Bring: your favourite game, or "Dixit" from the shelf
Have fun!
```

- Before saving, see how this version differs from the saved one, and be able to describe it.
- Build and run the changed program and check the output.
- Save a **second commit**.
- Confirm that the history contains both versions and that the project has no unsaved changes.

If you want to check your independence, do this task without looking at the solution of task 1.

## Task 3: Two reports

In `cpp-workspace`, create a folder `diagnosis` and copy `main.cpp` and `CMakeLists.txt` into it from the original `lesson_05_first_program`. Build it with the terminal commands, in the `build-terminal` folder.

**Report 1.** Someone wanted to print `Saving to C:\games\list.txt` and wrote this `main.cpp`:

<!-- broken: diagnosis_backslash at=4:18 errors=1 error=^expected expression$ -->
```cpp
#include <iostream>

int main() {
    std::cout << "Saving to C:\";
    std::cout << "games\\list.txt\n";
}
```

**Report 2.** Someone else renamed the program to `board_games`, and their `CMakeLists.txt` looks like this (`main.cpp` is already correct):

```cmake
cmake_minimum_required(VERSION 3.28)
project(first_program LANGUAGES CXX)

add_executable(board_games main.cpp)
target_compile_features(first_program PRIVATE cxx_std_20)
set_target_properties(first_program PROPERTIES CXX_EXTENSIONS OFF)
```

**For each report:**

1. Run the right step: configuring or building.
2. Determine the stage of the problem: configuring, compiling or linking.
3. Find the first relevant piece of information and write it down.
4. Form a hypothesis about the cause.
5. Fix the problem with one change.
6. Check that everything works after the change. The program from report 1 prints `Saving to C:\games\list.txt`, and after report 2 the program is called `board_games` and runs.

Record the results in a table:

| Report | Stage | First relevant information | Hypothesis | Fix | Check |
|---|---|---|---|---|---|
| 1 | | | | | |
| 2 | | | | | |

You don't need to save the `diagnosis` project in Git.

## Task 4: Explain

Answer briefly, in writing, referring to what was done in tasks 1–3:

1. What is the role of `main.cpp` in your `board_games_night` project?
2. What is `CMakeLists.txt` for? What happens if its lines don't match each other (report 2)?
3. What does the compiler do with your `main.cpp`?
4. How does compiling differ from linking? Which of these stages would report a problem if your program had `mian` instead of `main`?
5. Why didn't just saving the changed `main.cpp` in task 2 change the program built earlier?
6. Why can a program work incorrectly even though it built without errors? Give an example from this test.
7. Which line of your program took the longest to think through, and why?

## Success criteria

You pass the test when you meet **all** the criteria:

- `board_games_night/main.cpp` was written from an empty file, in valid C++20.
- The program builds without errors and runs, and its output is **exactly** as in task 1, and after the change exactly as in task 2.
- The program ends with exit code 0.
- The program has a meaningful comment.
- Both reports from task 3 are diagnosed: the right stage, a quote from the tools' output, a hypothesis, one fix and a check.
- The Git history has **two commits** of the `board_games_night` project, with messages that say what each version brings. `git status` shows no unsaved changes in this project.
- The history has no files generated by the tools and no CLion settings: for this project, only `main.cpp` and `CMakeLists.txt` are saved.
- You can explain every line of your program and every command that was used (task 4).

A working program, the right output and a clean `git status` are necessary, but they are **not proof of understanding**. The proof is that you can explain why the program works and how the causes of the problems were found. That's why task 4 is part of the test.

---

# Part B: checking and discussion

Come here after finishing part A, or when you knowingly decide to stop trying on your own.

## How to check your work

- **The program's output:** run the program and compare it with the expected one character by character, including the empty line, the quotes and the number of backslashes.
- **The exit code:** in CLion it's below the output: `Process finished with exit code 0`.
- **The history:**
  - `git log --oneline` shows two new commits;
  - `git status` doesn't show `board_games_night` files;
  - `git ls-files board_games_night` shows only `CMakeLists.txt` and `main.cpp`.

## Hints

Each hint is about the way of thinking. Open them one at a time, and only when you need them.

<details>
<summary>Task 1: where to start?</summary>

With the program skeleton (lesson 1.3), then one line of output at a time. After each statement you add, build and compare the output.

</details>

<details>
<summary>Task 1: the empty line and the backslashes</summary>

An empty line is a line with nothing but a move to a new line. How many `\` characters must there be in the code for two to appear next to each other in the output?

</details>

<details>
<summary>Task 3: report 1</summary>

What does `\` mean inside text right before `"`? So where does the first text end?

</details>

<details>
<summary>Task 3: report 2</summary>

Which step reports the error: configuring or building? How many times does the program's name appear in `CMakeLists.txt`, and is it the same everywhere?

</details>

## Example solutions

<details>
<summary>Task 1: the program</summary>

<!-- example: board_games_night -->
```cpp
#include <iostream>

int main() {
    std::cout << "BOARD GAMES NIGHT\n";
    std::cout << "=================\n";
    std::cout << "Where: City Library, room \"Blue\"\n";
    std::cout << "When: Friday, 18:00\n";
    std::cout << "Bring: your favourite game\n";
    std::cout << "\n";
    // In the code, \\ prints one backslash, so \\\\ prints two.
    std::cout << "Sign-up sheet: \\\\library\\games\\list.txt\n";
    std::cout << "Have fun!\n";
    return 0;
}
```

- The quotes around `Blue` are part of the text, so each is written as `\"`.
- The path starts with two backslashes, so the code has four (`\\\\`). Every further backslash is `\\` in the code.
- A statement with just `\n` prints the empty line. Adding a second `\n` to the previous line works just as well.
- The comment explains the hardest line. `return 0;` is optional: the end of `main` without `return` works the same.

</details>

<details>
<summary>Task 2: the changed program</summary>

<!-- example: board_games_night_changed -->
```cpp
#include <iostream>

int main() {
    std::cout << "BOARD GAMES NIGHT\n";
    std::cout << "=================\n";
    std::cout << "Where: City Library, room \"Green\"\n";
    std::cout << "When: Friday, 19:30\n";
    // In the code, \\ prints one backslash, so \\\\ prints two.
    std::cout << "Sign-up sheet: \\\\library\\games\\list.txt\n";
    std::cout << "\n";
    std::cout << "Bring: your favourite game, or \"Dixit\" from the shelf\n";
    std::cout << "Have fun!\n";
    return 0;
}
```

Before the second commit, `git diff` shows the changed room and time lines. It also shows that the `Sign-up sheet` line and the empty line moved above `Bring`, and that the `Bring` line has new text. An example walk-through in Git, in the `cpp-workspace` folder:

```text
git status
git add board_games_night/main.cpp board_games_night/CMakeLists.txt
git status
git commit -m "Add the board games night board"
```

and after the change:

```text
git diff
git add board_games_night/main.cpp
git diff --staged
git commit -m "Move the board games night to the Green room"
git log --oneline
git status
git ls-files board_games_night
```

</details>

<details>
<summary>Task 3: report 1</summary>

- **Stage:** compiling. Configuring succeeded, and the build stopped at `main.cpp`.
- **First relevant information:** `warning: missing terminating '"' character` in line 4, followed by `error: expected expression` at the same place. Here the warning says the most.
- **Hypothesis:** `\"` at the end of the text is a quote inside the text, not its end (lesson 1.3). So the text never ends.
- **Fix:** write the backslash that should appear in the output as `\\`:

<!-- example: diagnosis_backslash_fixed -->
```cpp
#include <iostream>

int main() {
    std::cout << "Saving to C:\\";
    std::cout << "games\\list.txt\n";
}
```

<!-- output: diagnosis_backslash_fixed -->
```text
Saving to C:\games\list.txt
```

</details>

<details>
<summary>Task 3: report 2</summary>

- **Stage:** configuring. The error appears already on `cmake -S . -B build-terminal …`, and neither the compiler nor the linker started. If `build-terminal` was configured before, `cmake --build` shows the same error, because it runs CMake again first.
- **First relevant information:**

```text
CMake Error at CMakeLists.txt:5 (target_compile_features):
  Cannot specify compile features for target "first_program" which is not
  built by this project.
```

  A second error, in line 6 (`set_target_properties`), has the same cause: one cause, two messages, as in lesson 1.2.
- **Hypothesis:** the program was renamed only in `add_executable`. The next two lines still talk about `first_program`, which the project no longer builds (lesson 1.4, experiment C).
- **Fix:** write `board_games` in both lines. After configuring and building, `build-terminal` contains the program `board_games` (`board_games.exe` on Windows).

</details>

## Example answers to task 4

<details>
<summary>Show the example answers</summary>

1. `main.cpp` is the program's source code. Running starts at `main`, and the statements print the board one after another, from top to bottom.
2. `CMakeLists.txt` tells the tools which program to build, from which file and in which standard. When its lines don't match, configuring fails and nothing gets built.
3. It checks whether the code is valid C++, and translates it into an object file.
4. Compiling checks and translates one file, and linking joins the object file with the library code and the startup code into a program. The linker would report the `mian` typo, because the compiler would accept `mian` as a valid function name.
5. The program is a separate file, created when building. It changes only after building again.
6. Because the compiler checks that the code is valid C++, not that the text is what we want. For example, a missing `\n`, or one backslash instead of two, gives a valid program with a different output.
7. This answer is personal. A good answer names a specific line and says what the doubt was about, for example the number of backslashes in the path.

</details>

## Self-assessment

For each criterion, mark one answer:

| Criterion | On my own | With a hint | After looking at the solution | To go over again |
|---|---|---|---|---|
| Writing the program from an empty `main.cpp` | | | | |
| The exact output, including `\"`, `\\` and the empty line | | | | |
| Building and running | | | | |
| Diagnosing report 1 (compiling) | | | | |
| Diagnosing report 2 (configuring) | | | | |
| Two commits without generated files | | | | |
| The explanations in task 4 | | | | |

If anything is marked "To go over again", go back to the matching lesson:

| Topic | Lesson |
|---|---|
| the skeleton and statements | 1.1 and 1.3 |
| compiler messages | 1.2 |
| `\"`, `\\`, comments | 1.3 |
| the build stages and `CMakeLists.txt` | 1.4 |
| Git | 1.5 |

Then try the task again, for example with a different text for the board.

---

## Module 1 summary

After six lessons, you can:

- read small C++20 programs and write them on your own, starting from an empty file;
- print text in a given order, with `\n`, `\"` and `\\`, and add comments where something needs explaining;
- read compiler messages, form hypotheses and fix one thing at a time;
- tell configuring, compiling, linking and running the program apart, and recognise from the tools' output where the problem is;
- use a simple CMake project and understand its lines;
- save the history of your own work in Git, without the files the tools generate.

## What's next: Module 2

So far, your programs always print the same text. In Module 2 they will start to **remember and calculate**: you'll learn about values, types, variables, expressions and calculations, and how to read simple input from the user. Start with [lesson 2.1: Values the program remembers](../module_02_values_and_calculations/lesson_01_values_the_program_remembers.en.md). Module 2 is in development: further lessons are in preparation.

**Previous lesson:** [Lesson 1.5: Save the history of your work](lesson_05_save_the_history_of_your_work.en.md) · **Next lesson:** [Lesson 2.1: Values the program remembers](../module_02_values_and_calculations/lesson_01_values_the_program_remembers.en.md) · [Course overview](../../README.en.md)

# Lesson 1.4: From source code to an executable

[Polski](lesson_04_from_source_code_to_an_executable.md) · **English** · [Course overview](../../README.en.md)

> **Module 1, lesson 4** · about 75 minutes
> **You need:** the `cpp-workspace` folder, the original `lesson_05_first_program` project, and the terminal commands from [lesson 0.6](../module_00_tooling/lesson_06_same_program_without_clion.en.md).
> **Pilot version:** the terminal commands in this lesson are checked automatically on Windows, Ubuntu and macOS. The CLion steps follow the CLion 2026.2 documentation.

## Before you start

This lesson assumes that:

- in the terminal, you can go to a folder, configure and build a project with CMake, and run the program (lesson 0.6);
- you read compiler messages with the method from lesson 1.2;
- you know that `main` is the function where the program starts running (lesson 1.3).

## The situation

You've clicked **Build** and typed `cmake --build` many times, and a program appeared. What happens along the way? Today you'll do these steps by hand, see at which of them different kinds of errors arise, and read the `CMakeLists.txt` file that describes the project.

The most important skill in this lesson: **when a build fails, recognise at which stage, and look for the cause based on that.** You don't need to memorise the messages.

After this lesson you will:

- explain the path from source code to a program: the preprocessor and compiling, the object file, linking, the executable;
- compile and link a program in two separate steps, and tell an object file apart from an executable;
- recognise whether a build stopped at compiling, at linking, or already at the CMake configuration;
- explain what CMake and Ninja do, and what each line of `CMakeLists.txt` says;
- change the name of a program in `CMakeLists.txt`.

## 1. Prepare a copy and a terminal

1. In `cpp-workspace`, create a folder `lesson_1_4` and copy `main.cpp` and `CMakeLists.txt` into it from the original `lesson_05_first_program`.
2. Open a terminal and go to `cpp-workspace/lesson_1_4`, as in lesson 0.6 (`cd` and the path in quotes). Check with `ls` (`ls -F` on macOS and Ubuntu): there are only two files.

The `main.cpp` file is the familiar program:

<!-- example: original source=../module_00_tooling/lesson_05_first_program/main.cpp -->
```cpp
#include <iostream>

int main() {
    std::cout << "Hello! My first C++20 program works.\n";
}
```

<!-- output: original -->
```text
Hello! My first C++20 program works.
```

You can change the code in CLion (open this folder in it) or in another text editor that saves plain text. You'll build and run in the terminal.

## 2. From code to a program

Building a program takes several steps:

```text
main.cpp  ──►  preprocessor and compiling  ──►  main.o  ──►  linking  ──►  program
(source code)                                (object file)               (executable)
```

- **Source code** (`main.cpp`) is the text of the program in C++. People write it, and the compiler reads it.
- **The preprocessor** is the first step of compiling. It handles the lines that start with `#`. For example, `#include <iostream>` inserts declarations from the standard library, including `std::cout`. It does this before the actual compiling starts (lesson 1.2).
- **Compiling** checks the C++ in **this one file** and translates it into machine code, the instructions for the processor. All the errors from lessons 1.2 and 1.3 came from here. The result is an **object file**, for example `main.o`.
- **An object file is not a program yet.** Two things are missing from it:
  - the ready code of the standard library that actually prints the text. `#include` only gave the compiler the declaration of `std::cout`, the information that such a thing exists;
  - the **startup code**: a short piece that every program has. It prepares the program to run and calls your `main` function.
- **Linking** is done by the **linker**. It joins the object file with the standard library code and the startup code into one **executable**. While doing so, it checks that everything the program needs really exists.

**Who does all this?** You type one command, `clang++`, but `clang++` is also a **driver**: it runs the right tools for you. For compiling it uses the Clang compiler, and for linking it starts your system's linker: `ld` on Ubuntu and macOS (two different linkers with the same name), and `lld-link` on Windows. In lesson 0.6, one `clang++ … -o …` command did both stages at once. Today you'll separate them.

## 3. Experiment A: building in two stages

### Step 1: compiling only

**Predict:** what new files will appear in the folder? Will there be a program you can run?

| System | Command |
|---|---|
| Windows | `clang++ -std=c++20 -c main.cpp` |
| macOS | `/opt/homebrew/opt/llvm@22/bin/clang++ -std=c++20 -c main.cpp` |
| Ubuntu | `clang++-22 -std=c++20 -c main.cpp` |

`-c` means "compile only". On a Mac with an Intel processor, type `/usr/local/opt/llvm@22` instead of `/opt/homebrew/opt/llvm@22`, as in lesson 0.6.

The command prints nothing. Check with `ls` (`ls -F` on macOS and Ubuntu). A file **`main.o`** has appeared, with the same name on all three systems. That's the object file. There is no program yet, and don't try to run `main.o`: it isn't a program.

### Step 2: linking

**Predict:** what will appear now? What will the program print?

| System | Linking | Running |
|---|---|---|
| Windows | `clang++ main.o -o hello.exe` | `.\hello.exe` |
| macOS | `/opt/homebrew/opt/llvm@22/bin/clang++ main.o -o hello` | `./hello` |
| Ubuntu | `clang++-22 main.o -o hello` | `./hello` |

This command gets the object file, not `main.cpp`. So `clang++` knows that compiling is already done and only starts the linker. That's why there is no `-std=c++20` here: there's nothing left to compile.

An executable `hello` (`hello.exe` on Windows) has appeared, and it prints the familiar message.

### The same in CMake

CMake with Ninja does the same two stages for you. In the output of `cmake --build` (lesson 0.6) and in CLion's Build window, they appeared as two lines:

```text
Building CXX object CMakeFiles/first_program.dir/main.cpp.o
Linking CXX executable first_program
```

`Building CXX object` is compiling, and `Linking CXX executable` is linking. The tool chooses the file names: CMake calls the object file `main.cpp.o`, and `main.cpp.obj` on Windows. `clang++` on its own called it `main.o`. The numbers in brackets, such as `[3/4]`, depend on the project and the tool versions, so don't rely on them.

## 4. Experiment B: your first link error

Less guidance this time. Replace the content of `main.cpp` with this code: `main` has become `mian`, and there is a `return 0;` at the end.

<!-- broken: mian stage=link error=undefined reference to .main'|undefined symbol: main\b|"_main", referenced from -->
```cpp
#include <iostream>

int mian() {
    std::cout << "Hello! My first C++20 program works.\n";
    return 0;
}
```

**Predict:** will step 1 (compiling) succeed? And step 2 (linking)? Then do both steps with the same commands as in experiment A.

Compiling goes through without any message, and `main.o` appears again. Linking fails. The output depends on the system:

**Ubuntu:**

```text
/usr/bin/ld: /lib/x86_64-linux-gnu/Scrt1.o: in function `_start':
(.text+0x1b): undefined reference to `main'
clang++-22: error: linker command failed with exit code 1 (use -v to see invocation)
```

**macOS:**

```text
Undefined symbols for architecture arm64:
  "_main", referenced from:
      <initial-undefines>
ld: symbol(s) not found for architecture arm64
clang++: error: linker command failed with exit code 1 (use -v to see invocation)
```

**Windows:**

```text
lld-link: error: subsystem must be defined
clang++: error: linker command failed with exit code 1 (use -v to see invocation)
```

**Don't memorise these messages.** Answer the questions, then check.

**1.** At which stage did the build stop? How can you tell?

<details>
<summary>Answer</summary>

At linking. Compiling succeeded: `main.o` was created and there was no message. Step 2 failed, and on every system the last line says `linker command failed`. No message points to a line in `main.cpp` (like `main.cpp:4:5`), because the linker doesn't read the source code: it gets a ready object file.

</details>

**2.** Why did the compiler report no error?

<details>
<summary>Answer</summary>

Because `mian` is a valid function name in C++. The compiler only checks whether this one file is valid C++. It doesn't know that this file is meant to be a whole program, or that `main` is missing from it.

</details>

**3.** Who needs the `main` function?

<details>
<summary>Answer</summary>

The startup code, which the linker adds to every program: it is what calls `main`. On Ubuntu you can see that `_start` is looking for it, and on macOS the linker lists the missing `_main` (the name with an extra `_` is normal on that system). On Windows, `lld-link` recognises the kind of program (a terminal program) from the `main` function itself, so without it, it says that this kind (the *subsystem*) isn't defined. The messages differ, but the cause is the same: there is no `main`.

</details>

**Notice one more thing:** the program `hello` from experiment A has disappeared. `clang++` removes a file it failed to build, so that no half-finished program is left behind. When compiling itself fails, linking doesn't even start, and the old program stays (lesson 1.2).

**Fix it:** change `mian` back to `main`, do both steps again and run the program.

<!-- example: main_with_return -->
```cpp
#include <iostream>

int main() {
    std::cout << "Hello! My first C++20 program works.\n";
    return 0;
}
```

<!-- output: main_with_return -->
```text
Hello! My first C++20 program works.
```

### A compile error vs. a link error

| | A missing semicolon (lesson 1.2) | `mian` instead of `main` |
|---|---|---|
| Stage | compiling | linking |
| Object file | not created | created |
| Who reports it | the compiler | the linker (through `clang++`) |
| Place in the message | `main.cpp:line:position` | no line in `main.cpp`; the name of what's missing |
| What's wrong | the code isn't valid C++ | the code is valid, but a part needed to build the program is missing |

An empty `main.cpp`, which lesson 1.3 warned you not to build, gives the same kind of error: an empty file compiles without trouble, but there is no `main` in it.

## 5. CMake, Ninja and `CMakeLists.txt`

When you build with CMake, you don't need to remember the commands from experiments A and B:

- **CMake** (configuring, `cmake -S . -B …`) reads `CMakeLists.txt`, checks the compiler and writes a **build plan**: which commands to run and in what order;
- **Ninja** (building, `cmake --build …`) carries out the plan: it runs `clang++` to compile, then to link. It redoes only what's needed, for example after `main.cpp` changes.

These are two different jobs: CMake plans, Ninja carries out.

### What `CMakeLists.txt` says

```cmake
cmake_minimum_required(VERSION 3.28)
project(first_program LANGUAGES CXX)

add_executable(first_program main.cpp)
target_compile_features(first_program PRIVATE cxx_std_20)
set_target_properties(first_program PROPERTIES CXX_EXTENSIONS OFF)
```

| Line | What it tells the tools |
|---|---|
| `cmake_minimum_required(VERSION 3.28)` | This project needs CMake 3.28 or newer. An older CMake stops with a message about the required version. |
| `project(first_program LANGUAGES CXX)` | The name of the whole **project** and its language: `CXX` is CMake's name for C++. This is where CMake looks for a C++ compiler and checks that it works. |
| `add_executable(first_program main.cpp)` | Build an **executable** called `first_program` from the file `main.cpp`. In CMake, such a program is called a **target**. |
| `target_compile_features(first_program PRIVATE cxx_std_20)` | Compile this program as C++20. That's why the commands show `-std=c++20`. Skip `PRIVATE` for now. |
| `set_target_properties(first_program PROPERTIES CXX_EXTENSIONS OFF)` | Use plain standard C++20, without extras specific to one compiler. |

The project name and the program name are the same here (`first_program`), but they are two different things: the project is the whole, and a target is one program in it.

You know **Debug and Release** from lesson 0.5. This choice isn't written in `CMakeLists.txt`: you make it when configuring (`-DCMAKE_BUILD_TYPE=Debug`) or in a CLion CMake profile. In this course we always use Debug for now.

### Experiment C: rename the program

1. Restore the original `main.cpp`: copy it again from `lesson_05_first_program` and replace the file in `lesson_1_4` with it.
2. Configure and build the project in the terminal with the commands from lesson 0.6, in the `build-terminal` folder, and run the program:

   | System | Configuring |
   |---|---|
   | Windows | `cmake -S . -B build-terminal -G Ninja -DCMAKE_BUILD_TYPE=Debug "-DCMAKE_CXX_COMPILER=C:\Program Files\LLVM\bin\clang++.exe"` |
   | macOS | `cmake -S . -B build-terminal -G Ninja -DCMAKE_BUILD_TYPE=Debug -DCMAKE_CXX_COMPILER=/opt/homebrew/opt/llvm@22/bin/clang++` |
   | Ubuntu | `cmake -S . -B build-terminal -G Ninja -DCMAKE_BUILD_TYPE=Debug -DCMAKE_CXX_COMPILER=/usr/bin/clang++-22` |

   Then `cmake --build build-terminal` and `.\build-terminal\first_program.exe` (macOS and Ubuntu: `./build-terminal/first_program`).
3. In `CMakeLists.txt`, replace `first_program` with `hello_cmake` in **three** lines: `add_executable`, `target_compile_features` and `set_target_properties`. Leave the `project(…)` line unchanged. Save the file.

**Predict:** what will appear in `build-terminal` after building again? Will `first_program` disappear?

4. Build again: `cmake --build build-terminal`. You don't need to configure yourself: Ninja notices the change in `CMakeLists.txt` and runs CMake first on its own. You'll see `Re-running CMake...` at the start of the output. Then come compiling and `Linking CXX executable hello_cmake`.
5. Check `ls build-terminal` (`ls -F build-terminal` on macOS and Ubuntu), and run the new program: `.\build-terminal\hello_cmake.exe` (macOS and Ubuntu: `./build-terminal/hello_cmake`).

<details>
<summary>What happened</summary>

`build-terminal` now contains **both** programs: the new `hello_cmake` and the old `first_program`. `add_executable` sets the program's name, so a new file was created. Nobody deleted the old one: CMake and Ninja take care of what they have to build, and don't clean up files created earlier. Just as in lesson 0.5: every executable is a separate file.

</details>

**Go back to the original version.** The safest way is to copy `CMakeLists.txt` again from the original `lesson_05_first_program` and replace the changed file with it. Then `cmake --build build-terminal`. The `hello_cmake` file stays in `build-terminal` until you delete it. You can also delete the whole `build-terminal` folder: it's a build result, and the next configuring creates it again.

## 6. Mission: Which stage complains?

Someone on the team reports four problems. In each case, **one thing** was changed in a working project. Your task: find out at which stage something is wrong, and fix it.

**Prepare the project:**

1. In `cpp-workspace`, create `build_detective` and copy `main.cpp` and `CMakeLists.txt` into it from the original `lesson_05_first_program`.
2. Replace the content of `main.cpp` with the working version:

<!-- example: mission -->
```cpp
#include <iostream>

int main() {
    std::cout << "Build: OK\n";
    std::cout << "Run: OK\n";
    return 0;
}
```

3. Configure `build-terminal` as in experiment C, build and run the program. The expected output:

<!-- output: mission -->
```text
Build: OK
Run: OK
```

**The reports.** Always start from the working version above: before each report, restore it (in `main.cpp` and, for report C, in `CMakeLists.txt`). Then make the change described.

**Report A.** `main.cpp` looks like this:

<!-- broken: mission_main stage=link error=undefined reference to .main'|undefined symbol: main\b|"_main", referenced from -->
```cpp
#include <iostream>

int Main() {
    std::cout << "Build: OK\n";
    std::cout << "Run: OK\n";
    return 0;
}
```

**Report B.** `main.cpp` looks like this:

<!-- example: mission_newline -->
```cpp
#include <iostream>

int main() {
    std::cout << "Build: OK";
    std::cout << "Run: OK\n";
    return 0;
}
```

**Report C.** `main.cpp` is the working one, but one line of `CMakeLists.txt` looks like this:

```cmake
add_executable(first_program program.cpp)
```

**Report D.** `main.cpp` looks like this:

<!-- broken: mission_quote at=4:18 errors=1 error=^expected expression$ -->
```cpp
#include <iostream>

int main() {
    std::cout << "Build: OK\n;
    std::cout << "Run: OK\n";
    return 0;
}
```

**For each report:**

1. **Predict** before you run anything: will the build succeed? Will running it?
2. Build (`cmake --build build-terminal`) and, if possible, run the program.
3. Determine the **stage**: configuring (CMake), compiling, linking, or running the program (it builds, but the output is wrong).
4. Find **the first relevant piece of information**, and copy it down.
5. Write down **the cause**, fix **one thing**, and check the result.

Record the results in a table, for example in your notes:

| Report | Prediction | Stage | First relevant information | Cause | Fix | Result |
|---|---|---|---|---|---|---|
| A | | | | | | |
| B | | | | | | |
| C | | | | | | |
| D | | | | | | |

### Success criteria

- Each report has the right stage assigned, with **a quote from the tools' output** that confirms it. For the report where no tool reports an error, the evidence is the program's output.
- Each report was fixed with one change, and after the fix the program builds and prints the expected two lines.
- For each report, you can say in one sentence **why** the problem stopped the build at exactly that stage, or why no stage stopped it.

<details>
<summary>Hint 1</summary>

Before you read the messages, answer two questions: was an object file created? Was a program created? The answers often point to the stage.

</details>

<details>
<summary>Hint 2</summary>

Check who writes the first message: CMake (`CMake Error`), the compiler (`main.cpp:` with a line number), or the linker (`linker command failed`)? Or does nobody write anything, and yet something is wrong? The first relevant information can also be a `warning`.

</details>

An example solution is in [Example solutions](#example-solutions).

## 7. When something goes differently

| What you see | What it means | What to do |
|---|---|---|
| There's no `main.o` after `clang++ -c` | Compiling failed, or the terminal is in a different folder. | Read the compiler's messages (lesson 1.2). Check `pwd` and `ls`. |
| `no such file or directory: 'main.o'` or a similar message when linking | There's no object file to join. | Do step 1 first, in the same folder. |
| macOS: the `clang++` command works, but it's Apple's compiler | On macOS, plain `clang++` is Apple's compiler (lesson 0.4). | Use the full path from the table. |
| `linker command failed` | Compiling succeeded; linking failed. | Check what is missing: often `main` with a typo or a different capitalisation. |
| `CMake Error at CMakeLists.txt:…` | The problem is in the project description, not in the C++ code. The compiler hasn't started yet. | Read which line of `CMakeLists.txt` the error is about. The safest fix is to restore the original file and make the change again. |
| After renaming the program, the old program runs | The old executable is still in `build-terminal`. | Run the program with the new name, or delete `build-terminal` and configure again. |
| After changing `CMakeLists.txt`, CLion shows messages in the CMake window | CLion reads `CMakeLists.txt` too, and reloads the project. | This lesson builds in the terminal. In CLion you can just edit files. |

## 8. Explain

Answer in your own words, preferably in writing. Only then compare with the example answer.

**1.** How does an object file differ from an executable?

<details>
<summary>Example answer</summary>

An object file is the compiled code of one source file, without the standard library code and without the startup code, so it can't be run. The executable is made from it by linking: it's a complete program.

</details>

**2.** Why can the program with `mian` be compiled, but not linked?

<details>
<summary>Example answer</summary>

The compiler only checks whether the code is valid C++, and `mian` is a valid function name. Only the linker, building the whole program, looks for `main`, which the startup code calls, and doesn't find it.

</details>

**3.** How can you tell from the build output that the problem was reported by the linker, not the compiler?

<details>
<summary>Example answer</summary>

Compiling succeeded, so an object file was created. The output contains `linker command failed`, and the messages don't point to a line in `main.cpp`, but to the name of something that's missing.

</details>

**4.** What does CMake do, and what does Ninja do?

<details>
<summary>Example answer</summary>

CMake reads `CMakeLists.txt` and prepares a build plan. Ninja carries out the plan: it runs `clang++` to compile and to link, and only when something has changed.

</details>

**5.** Why did the old program stay in `build-terminal` after renaming the program in `CMakeLists.txt`?

<details>
<summary>Example answer</summary>

Because changing the name in `add_executable` tells the tools what to build from now on. It doesn't tell them to delete files created earlier. The old executable stays until you delete it.

</details>

## Summary

- The path from code to a program: **source code → preprocessor and compiling → object file → linking → executable**.
- Compiling checks the C++ of one file. Linking joins the object file with the standard library code and the startup code, and checks that nothing is missing, for example `main`.
- `clang++` is also a driver: with `-c` it only compiles, and for an object file it starts the linker.
- You recognise the stage of an error by evidence: `CMake Error` (configuring), `main.cpp:line:position` (compiling), `linker command failed` (linking), wrong output with no message (running the program). Linker messages differ between systems. What matters is the stage and the cause, not the exact words.
- CMake plans the build from `CMakeLists.txt`, and Ninja carries out the plan. `add_executable` sets the program's name and its source file.

## What's next

After four lessons of Module 1, you can write a small program, fix errors, and you know how an executable is made. **Lesson 1.5 is in preparation.**

---

## Example solutions

Look here **after your own attempt**. Your quotes may look different on your system. What matters is whether they point to the same stage.

<details>
<summary>Mission: an example table</summary>

| Report | Prediction | Stage | First relevant information | Cause | Fix | Result |
|---|---|---|---|---|---|---|
| A | It compiles, but won't link. | linking | Ubuntu: ``undefined reference to `main'``; macOS: `"_main", referenced from`; Windows: `undefined symbol: main`. On every system: `linker command failed`. | `Main` is a different name from `main`: capitalisation matters. The startup code finds no `main`. | `Main` → `main` | It builds; the output is right. |
| B | It builds and runs. | running the program | No tool reports an error. The program prints `Build: OKRun: OK` on one line. | The first text is missing `\n`. | Add `\n` | Two lines, as expected. |
| C | It won't build. | configuring (CMake) | `CMake Error at CMakeLists.txt:4 (add_executable):` `Cannot find source file:` `program.cpp` | `CMakeLists.txt` names a file that doesn't exist. The compiler didn't even start. | `program.cpp` → `main.cpp` | It builds; the output is right. |
| D | It won't compile. | compiling | `main.cpp:4:18: warning: missing terminating '"' character`, followed by `main.cpp:4:18: error: expected expression` | The text in line 4 has no closing quote. The warning describes the cause more precisely than the error itself. | Add `"` before `;` | It builds; the output is right. |

- **Report A through CMake:** on Windows, the message is `undefined symbol: main`, not `subsystem must be defined` as in experiment B. CMake tells the linker itself that this is a terminal program. A different message, the same stage, the same cause.
- **Report C:** `cmake --build` reports it, because Ninja sees the change in `CMakeLists.txt` and runs CMake first. The first line is `Re-running CMake...`, followed by `CMake Error` messages.

The program's output in report B:

<!-- output: mission_newline -->
```text
Build: OKRun: OK
```

</details>

**Previous lesson:** [Lesson 1.3: A program from a blank page](lesson_03_a_program_from_a_blank_page.en.md) · **Next lesson:** in preparation · [Course overview](../../README.en.md)

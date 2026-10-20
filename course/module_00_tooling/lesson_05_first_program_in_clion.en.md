# Lesson 0.5: Your first working program in CLion

[Polski](lesson_05_first_program_in_clion.md) · **English** · [Course overview](../../README.en.md)

> **Module 0, lesson 5** · about 45–60 minutes
> **You need:** the tools installed in [lesson 0.4](lesson_04_installing_the_tools.en.md), and internet access to download the project.
> **Pilot version:** the CLion steps follow the CLion 2026.2 documentation. Button names in your version may differ slightly.

## Before you start

This lesson assumes that:

- you can open a terminal, move between folders and start a program by giving its path (lessons 0.1–0.3);
- you know that a **compiler** turns source code into an executable file (lesson 0.3);
- you have LLVM 22, CMake, Ninja and CLion installed, and their versions were checked in the terminal (lesson 0.4).

## The situation

Your workshop is ready. Now you will see it at work: you will take a ready-made C++ source file, turn it into a program and run it.

**You don't need to understand the code yet.** You will learn what every line means in Module 1. Today, what matters is the way from a file to a working program.

After this lesson you will:

- select the right set of tools (toolchain) in CLion and check which compiler the project uses;
- open a ready-made project and recognise the files `main.cpp` and `CMakeLists.txt`;
- build the program in the Debug configuration and run it in CLion;
- tell editing code, building and running apart;
- explain why saving changes to the code doesn't change a program that is already built.

## 1. Understand: editing, building, running

Working with a program means three different activities:

1. **Editing:** you change the text in a source code file, here `main.cpp`.
2. **Building:** the tools turn the source code into an **executable file**. CMake prepares a plan, Ninja carries it out, and the `clang++` compiler does the actual conversion.
3. **Running:** the computer carries out the finished executable file, and the program prints its result.

In CLion, a **toolchain** is the set of tools used for building: the compiler, CMake and Ninja. You need to select it, because CLion may pick a different set on its own, for example the MinGW compiler bundled with CLion on Windows, or Apple's compiler on macOS. The program would probably still build, but not with our compiler.

A program can be built in different **configurations**. **Debug** is the version for learning and finding mistakes; it is the default, and you will use it in this lesson. **Release** is the version prepared for sharing with others; you don't need it yet.

## 2. Download the project

The project for this lesson is in the course repository on GitHub. You don't need Git.

1. Open the course page: [github.com/michalmaj/modern-cpp-foundations](https://github.com/michalmaj/modern-cpp-foundations).
2. Click the green **Code** button, then **Download ZIP**.
3. Extract the downloaded file. On Windows, right-click it and choose **Extract All**. On macOS, double-click it. On Ubuntu, right-click it and choose **Extract**.
4. In the extracted `modern-cpp-foundations-main` folder, go to `course/module_00_tooling/lesson_05_first_program`. Sometimes `modern-cpp-foundations-main` sits inside a second folder with the same name; that's normal.

The `lesson_05_first_program` folder contains two files:

| File | What it is |
|---|---|
| `main.cpp` | The program's C++ **source code**. |
| `CMakeLists.txt` | The **project description** for CMake: which files make up the program, and that it is C++20. |

This is `main.cpp`:

```cpp
#include <iostream>

int main() {
    std::cout << "Hello! My first C++20 program works.\n";
}
```

You don't need to understand these lines. Just notice the text in quotes: it's the message the program will print.

<details>
<summary>Can't download the ZIP file?</summary>

Create a project in CLion instead: **File | New Project**, choose **C++ Executable** and the **C++20** standard. Then replace the entire contents of the two generated files with the text below. Copy and paste it; don't type it by hand.

`CMakeLists.txt`:

```cmake
cmake_minimum_required(VERSION 3.28)
project(first_program LANGUAGES CXX)

add_executable(first_program main.cpp)
target_compile_features(first_program PRIVATE cxx_std_20)
set_target_properties(first_program PROPERTIES CXX_EXTENSIONS OFF)
```

`main.cpp`: the same as in the example above.

Replace both files, not just `main.cpp`: the wizard's `CMakeLists.txt` may require a newer CMake than some systems have.

</details>

## 3. Open the project in CLion

1. Start CLion. On the Welcome screen, click **Open** (or, in an already open window, choose **File | Open**).
2. Select the `lesson_05_first_program` folder and confirm.
3. CLion asks whether you trust the project. Choose **Trust Project**. The project comes from the course, and without trusting it CLion won't build the program.
4. On the first open, CLion shows the **CMake Profiles** window with a **Debug** profile. Keep the defaults and confirm (**OK**). You will select the toolchain in a moment.

CLion loads the project. You can follow the progress in the **CMake** window at the bottom of the screen.

## 4. Select the right toolchain

Open the settings: on Windows and Ubuntu **File | Settings**, on macOS **CLion | Settings**. Go to **Build, Execution, Deployment | Toolchains** and click **+**.

### Windows

1. Choose **Visual Studio**.
2. In the **Name** field, type for example `LLVM 22`.
3. **Toolset:** CLion should find the Build Tools from lesson 0.4 by itself, usually in `C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools`. If the field is empty, select that folder.
4. **Architecture:** `amd64`.
5. **C Compiler:** `C:\Program Files\LLVM\bin\clang.exe`
6. **C++ Compiler:** `C:\Program Files\LLVM\bin\clang++.exe`
7. Leave the CMake and Build Tool fields as they are: CLion will use its own built-in CMake and Ninja.

> **Pilot version:** this configuration has not yet been checked in CLion on Windows. If CLion reports that the compiler doesn't match the Visual Studio toolchain, try **+ → System** instead, with the same compiler paths. That should be enough to build and run the program. The debugger, which we will cover later, may need different settings in that variant.

### macOS

1. Choose **System** and type a name, for example `LLVM 22`.
2. In the terminal, check where Homebrew installed LLVM: `brew --prefix llvm@22`. On computers with an Apple processor (M1 and newer) it is usually `/opt/homebrew/opt/llvm@22`, and on computers with an Intel processor `/usr/local/opt/llvm@22`.
3. **C Compiler:** that path followed by `/bin/clang`, for example `/opt/homebrew/opt/llvm@22/bin/clang`.
4. **C++ Compiler:** that path followed by `/bin/clang++`, for example `/opt/homebrew/opt/llvm@22/bin/clang++`.

Don't choose `/usr/bin/clang++`: that is Apple's compiler.

### Ubuntu

1. Choose **System** and type a name, for example `LLVM 22`.
2. **C Compiler:** `/usr/bin/clang-22`
3. **C++ Compiler:** `/usr/bin/clang++-22`

Don't choose `/usr/bin/c++`, `/usr/bin/g++` or `/usr/bin/clang++`: those are other compilers.

### Every system: use the new toolchain in the Debug profile

1. In the settings, go to **Build, Execution, Deployment | CMake**.
2. Select the **Debug** profile. In the **Toolchain** field, choose the `LLVM 22` toolchain you created.
3. Click **OK**. CLion loads the project again, this time with our compiler.

## 5. Check which compiler the project uses

Open the **CMake** window (at the bottom of the screen, or **View | Tool Windows | CMake**). Find two lines:

```text
-- The CXX compiler identification is Clang 22.1.8
-- Check for working CXX compiler: /usr/bin/clang++-22 - skipped
```

- The first must say **`Clang 22`**. On Windows it also says `with GNU-like command-line`.
- The second shows the path to the compiler you entered in the toolchain (on Windows `C:/Program Files/LLVM/bin/clang++.exe`, on macOS the Homebrew path).

If you see something else, the project uses the wrong compiler:

| The first line shows | Whose compiler it is |
|---|---|
| `GNU 15…` (Windows) | the MinGW bundled with CLion |
| `AppleClang …` (macOS) | Apple's compiler |
| `GNU 13…` or `Clang 18…` (Ubuntu) | the system GCC or an older Clang |
| `Clang 22… with MSVC-like command-line` (Windows) | `clang-cl` instead of `clang++` |

In that case, go back to section 4. Then choose **Tools | CMake | Reset Cache and Reload Project**, so that CLion forgets the previous compiler.

Also check the configuration: at the very top of the CMake window is the command CLion used to run CMake. It should contain `-DCMAKE_BUILD_TYPE=Debug`, and the build folder is called `cmake-build-debug`.

## 6. Build and run the program

**Building.** Choose **Build | Build Project** (<kbd>Ctrl</kbd> + <kbd>F9</kbd> on Windows and Ubuntu, <kbd>⌘ Cmd</kbd> + <kbd>F9</kbd> on macOS). The **Build** window shows the steps, for example:

```text
[1/2] Building CXX object CMakeFiles/first_program.dir/main.cpp.o
[2/2] Linking CXX executable first_program
```

On Windows the file names end in `.obj` and `.exe`. A `cmake-build-debug` folder has appeared in the project folder, and in it the executable file `first_program` (on Windows `first_program.exe`). That is your program.

**Running.** In the toolbar at the top, the run configuration `first_program` is selected. Click the green **Run** button (▶) next to it. The **Run** window shows:

```text
Hello! My first C++20 program works.

Process finished with exit code 0
```

`exit code 0` means the program finished without an error.

Before running, **Run** builds the program by itself if needed. That's why Run usually “just works”, but underneath it is two activities: building and running. The experiment in the next section separates them.

## 7. Experiment: source code versus the finished program

**Step 1. Run the finished program without CLion.** Open CLion's built-in terminal: **View | Tool Windows | Terminal** (<kbd>Alt</kbd> + <kbd>F12</kbd>, on macOS <kbd>⌥ Option</kbd> + <kbd>F12</kbd>). The terminal starts in the project folder; you can check with `pwd`. Run the executable file by giving its path:

| Windows | macOS and Ubuntu |
|---|---|
| `.\cmake-build-debug\first_program.exe` | `./cmake-build-debug/first_program` |

The dot at the start is the current folder, which you know from lesson 0.2. You can't start a program from your own folder by its name alone, because that folder isn't on the `PATH` list (lesson 0.3). The program prints the same message as in the Run window.

**Step 2. Change the code.** In `main.cpp`, change only the text **between the quotes**, for example to `I changed this message!`. Don't remove the quotes or the characters around them. For now, use plain English letters: not every terminal displays other characters correctly (we'll come back to this later). Save the file: **File | Save All** (<kbd>Ctrl</kbd> + <kbd>S</kbd>, on macOS <kbd>⌘ Cmd</kbd> + <kbd>S</kbd>).

**Step 3. Predict before you check.** `main.cpp` has changed, but nothing has been built yet. What will the program print when you start it from the terminal, as in step 1: the old message or the new one?

Check by typing the same command as in step 1. You will see the **old** message.

**Step 4. Build again.** Choose **Build | Build Project**. The Build window shows that the compiler worked again. Start the program from the terminal once more. Now you will see the **new** message.

**Step 5. Build without changes.** Choose **Build | Build Project** once more, without changing anything. The Build window shows a message like `ninja: no work to do`: nothing changed, so there was nothing to build.

**Step 6. Run.** Click **Run** (▶). You see the new message: CLion checked whether anything needed building, then ran the program.

**What happened?** The executable file in `cmake-build-debug` is a separate file that was created by building. Changing and saving `main.cpp` changes only the source code. The program changes only when you build it again.

## 8. The same work without CLion

The same project can be built in an ordinary terminal, without CLion. You don't need to do this now: we will go through it carefully in the next lesson. For the curious: in the project folder, two commands are enough.

```text
cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Debug -DCMAKE_CXX_COMPILER=<path to clang++>
cmake --build build
```

For `<path to clang++>`, use the same path as in the toolchain: on Windows `"C:\Program Files\LLVM\bin\clang++.exe"` (in quotes, because it contains a space), on macOS the Homebrew path, on Ubuntu `/usr/bin/clang++-22`. The program appears in the `build` folder.

## 9. Mission: your own message

Make the program print a message of your choice, using plain English letters, and collect three pieces of evidence:

1. **The right compiler:** the line from the CMake window with `Clang 22`.
2. **Your program works:** the Run window with your message and `Process finished with exit code 0`.
3. **An explanation:** two or three sentences on why, in step 3 of the experiment, the program started from the terminal printed the old message.

### Success criterion

- The CMake window shows `Clang 22` (on Windows with `GNU-like command-line`) and the path to our compiler.
- The Run window shows your message and `exit code 0`.
- Your explanation tells the source code (`main.cpp`) apart from the executable file, and says that the executable only changes after building.

## 10. When things look different

| What you see | What it means | What to do |
|---|---|---|
| The CMake window shows a compiler other than `Clang 22` | The Debug profile uses another toolchain. | Section 4, then **Tools \| CMake \| Reset Cache and Reload Project**. |
| Windows: the Visual Studio toolchain doesn't find the Build Tools | CLion didn't detect the installation from lesson 0.4. | Select the folder `C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools`. If it doesn't exist, go back to lesson 0.4. |
| Windows: CLion reports that the compiler doesn't match the toolchain | This configuration has not been checked yet. | Try the **System** variant from the note in section 4. |
| The Run button is greyed out, or there is no `first_program` configuration | The project hasn't loaded. | Check the CMake window: are there errors? Did you choose **Trust Project**? If the project is in Safe Mode, choose **Trust Project** in the message at the top of the window. |
| Building reports `'iostream' file not found` or `could not open 'kernel32.lib'` | The system tools are missing. | Go back to lesson 0.4, section 4, “System tools”. |
| `CMake 3.28 or higher is required` | CLion uses an older CMake. | In the toolchain settings, switch back to the built-in CMake (**Bundled**). |
| Terminal: the program isn't found | Either it hasn't been built yet, or the path is different. | Build the project. Check `pwd` and `ls cmake-build-debug`. On Windows, remember `.\` and `.exe`. |
| Letters outside plain English look strange in the message | The terminal reads those characters differently. | For now, use plain English letters only. |

## 11. Explain it

**1.** What is the difference between editing, building and running a program?

<details>
<summary>Answer</summary>

Editing changes the source code. Building turns the source code into an executable file. Running carries out that file.

</details>

**2.** Why did the program started from the terminal print the old message after you changed `main.cpp`?

<details>
<summary>Answer</summary>

The executable is a separate file, created by the previous build. Changing `main.cpp` doesn't change it. A new executable is only created when you build again.

</details>

**3.** Why did CLion's Run button show the new message straight away?

<details>
<summary>Answer</summary>

Because before running, CLion builds the program by itself if the code has changed.

</details>

**4.** Why select a toolchain in CLion, if the program would have built anyway?

<details>
<summary>Answer</summary>

Because CLion may pick another compiler on its own, for example MinGW on Windows or Apple's compiler on macOS. The program would build, but not with the compiler this course uses and whose results the lessons describe.

</details>

## Summary

- Here, a C++ project is two files: the source code `main.cpp` and the project description `CMakeLists.txt`.
- A **toolchain** is the set of tools used for building. You check it in the CMake window: it must say `Clang 22`.
- **Building** creates the executable in `cmake-build-debug`. **Run** builds if needed, then runs the program.
- Changing the code doesn't change the program until you build it.

**Previous lesson:** [Lesson 0.4: Set up your workshop: installing the tools](lesson_04_installing_the_tools.en.md) · **Next lesson:** in preparation · [Course overview](../../README.en.md)

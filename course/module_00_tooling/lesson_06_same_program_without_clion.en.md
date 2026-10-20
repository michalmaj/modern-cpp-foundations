# Lesson 0.6: The same program without CLion

[Polski](lesson_06_same_program_without_clion.md) · **English** · [Course overview](../../README.en.md)

> **Module 0, lesson 6** · about 45 minutes
> **You need:** the `lesson_05_first_program` project from [lesson 0.5](lesson_05_first_program_in_clion.en.md) and the tools from [lesson 0.4](lesson_04_installing_the_tools.en.md).

## Before you start

This lesson assumes that after lessons 0.1–0.5:

- you can open a terminal, go to a folder (`cd`) and check where you are (`pwd`, `ls`);
- you start a program from the current folder by giving its path (`./…` or `.\…`);
- you have the `lesson_05_first_program` project and it has already been built in CLion.

If you don't have the project, download it as in [lesson 0.5, section 2](lesson_05_first_program_in_clion.en.md#2-download-the-project). You don't need to open it in CLion this time.

## The situation

In lesson 0.5, CLion built and ran the program with one click. Does that mean it can't be done without CLion? No. CLion doesn't have its own hidden compiler: it called the same tools that were installed in lesson 0.4. Today you will call them yourself, in an ordinary terminal.

After this lesson you will:

- go to a project folder in the terminal and recognise its files;
- configure and build the project with CMake, using the right `clang++` compiler;
- run the built program without CLion;
- compile `main.cpp` directly with the `clang++` command;
- explain what the compiler, CMake and Ninja do;
- tell configuring, building and running apart.

## 1. Recap: what is what

| Item | What it is |
|---|---|
| `main.cpp` | **Source code**: the text of the program in C++. |
| `CMakeLists.txt` | **Project description** for CMake: what the program is made from, and that it is C++20. |
| `cmake-build-debug/first_program` (on Windows `.exe`) | The **executable file** CLion built in lesson 0.5. |
| **building** | Turning source code into an executable file. |

In lesson 0.5, CLion called three tools for you: **CMake**, which prepared a build plan, **Ninja**, which carried out that plan, and the **`clang++`** compiler, which turned the code into a program. Now you will call them yourself.

## 2. Try it: go to the project folder

Open an **ordinary terminal**, not the one inside CLion. Go to the `lesson_05_first_program` folder.

The easiest way to avoid typing a long path: open that folder in a file window and copy its path.

- **Windows:** right-click the folder and choose **Copy as path**.
- **macOS:** select the folder in Finder, hold down <kbd>⌥ Option</kbd>, right-click and choose **Copy “lesson_05_first_program” as Pathname**.
- **Ubuntu:** in the file window, press <kbd>Ctrl</kbd> + <kbd>L</kbd> and copy the path from the address bar.

Then, in the terminal, type `cd`, a space, and paste the path in quotes, for example:

```text
cd "C:\Users\ola\Downloads\modern-cpp-foundations-main\course\module_00_tooling\lesson_05_first_program"
```

Check that you are in the right place (on macOS and Ubuntu, type `ls -F` instead of `ls`):

```text
pwd
ls
```

The list should include `main.cpp`, `CMakeLists.txt` and the `cmake-build-debug` folder from lesson 0.5. Run the program that CLion built back then:

| Windows | macOS and Ubuntu |
|---|---|
| `.\cmake-build-debug\first_program.exe` | `./cmake-build-debug/first_program` |

You will see the message from lesson 0.5, possibly the one you changed in the mission. That file still works, even though CLion is closed.

## 3. Understand: configuring, building, running

From the terminal, a program is created in **three steps**:

| Step | Command | What happens |
|---|---|---|
| 1. **Configuring** | `cmake -S . -B build-terminal …` | CMake reads `CMakeLists.txt`, checks the compiler and writes a **build plan** in the `build-terminal` folder. |
| 2. **Building** | `cmake --build build-terminal` | CMake asks Ninja to carry out the plan, and Ninja runs `clang++`. An executable file is created. |
| 3. **Running** | `./build-terminal/first_program` | The computer carries out the finished program. |

You configure **once**. After each change to the code, building is enough.

The configure command has several parts. You don't need to memorise them:

- `-S .`: the source code is here, in the current folder (you know `.` from lesson 0.2);
- `-B build-terminal`: the build files go into the `build-terminal` folder, separate from CLion's `cmake-build-debug`;
- `-G Ninja`: Ninja will do the building;
- `-DCMAKE_BUILD_TYPE=Debug`: the Debug configuration, as in CLion;
- `-DCMAKE_CXX_COMPILER=…`: the full path to our compiler, so that CMake doesn't pick a different one.

## 4. Try it: build and run from the terminal

Type the three commands for your system.

**Windows (PowerShell):**

```text
cmake -S . -B build-terminal -G Ninja -DCMAKE_BUILD_TYPE=Debug "-DCMAKE_CXX_COMPILER=C:\Program Files\LLVM\bin\clang++.exe"
cmake --build build-terminal
.\build-terminal\first_program.exe
```

The quotes surround the **whole** last part of the configure command, because the path contains a space (`Program Files`). Without them, PowerShell would split it into two parts.

**macOS:**

```text
cmake -S . -B build-terminal -G Ninja -DCMAKE_BUILD_TYPE=Debug -DCMAKE_CXX_COMPILER=/opt/homebrew/opt/llvm@22/bin/clang++
cmake --build build-terminal
./build-terminal/first_program
```

On a computer with an Intel processor, type `/usr/local/opt/llvm@22` instead of `/opt/homebrew/opt/llvm@22`. `brew --prefix llvm@22` shows the exact path.

**Ubuntu:**

```text
cmake -S . -B build-terminal -G Ninja -DCMAKE_BUILD_TYPE=Debug -DCMAKE_CXX_COMPILER=/usr/bin/clang++-22
cmake --build build-terminal
./build-terminal/first_program
```

**Check after each step:**

1. **Configuring:** the output contains `The CXX compiler identification is Clang 22…`, `Check for working CXX compiler:` with the path to our compiler, and at the end `Build files have been written to: …build-terminal`. These are the same lines you saw in CLion's CMake window in lesson 0.5.
2. **Building:** the last line says `Linking CXX executable first_program` (on Windows `first_program.exe`).
3. **Running:** the program prints the same message as the CLion version. It is the same code, so it gives the same result.

## 5. Experiment: the compiler without CMake

Our program is a single short file, so the compiler can handle it on its own. Type:

| System | Compiling | Running |
|---|---|---|
| Windows | `clang++ -std=c++20 main.cpp -o first_program_direct.exe` | `.\first_program_direct.exe` |
| macOS | `/opt/homebrew/opt/llvm@22/bin/clang++ -std=c++20 main.cpp -o first_program_direct` | `./first_program_direct` |
| Ubuntu | `clang++-22 -std=c++20 main.cpp -o first_program_direct` | `./first_program_direct` |

- `-std=c++20` tells the compiler that this is C++20; in the CMake project, the same thing is written in `CMakeLists.txt`.
- `-o first_program_direct` gives the program a name, so that you don't confuse it with the version built by CMake.
- On macOS you give the full path, because plain `clang++` is Apple's compiler (lesson 0.4).

The program prints the same message.

**Why was one command enough?** The program has one file and needs no extra settings, so `clang++` carries out all the steps needed to produce an executable file by itself.

**So why CMake?** Real programs have many files and settings. CMake remembers them in `CMakeLists.txt`, and the same description works in CLion and in the terminal, on every system. That's why **in this course we build with CMake**. Calling `clang++` directly was only an experiment, to see what the compiler does on its own.

## 6. Experiment: one source, three programs

You now have three executable files built from the same `main.cpp`:

- `cmake-build-debug/first_program` (built by CLion);
- `build-terminal/first_program` (built by CMake in the terminal);
- `first_program_direct` (built directly by `clang++`).

**Step 1.** Open `main.cpp` in any text editor (CLion is fine) and change the text between the quotes, for example to `Three programs, one source.` Use plain English letters for now. Save the file.

**Step 2. Predict:** what will each of the three programs print if you run them now, before any building? Write your predictions in the table:

| Program | Prediction | Result |
|---|---|---|
| `cmake-build-debug/first_program` | | |
| `build-terminal/first_program` | | |
| `first_program_direct` | | |

Run all three, each by its own path, and fill in the “Result” column.

**Step 3.** Build only the terminal version: `cmake --build build-terminal`. No need to configure again: the plan already exists. Predict which program will now print the new message, then check all three.

**Step 4.** Compile `first_program_direct` again with the command from section 5 and run it.

**What happened?** Each executable is a separate file. Only the program you build again changes. The others still print the old message. CLion didn't build anything, so `cmake-build-debug/first_program` still has the old version.

## 7. Final mission of Module 0

This mission brings together everything Module 0 has taught you. Do it in an ordinary terminal, without CLion.

1. **Find the project:** go to the `lesson_05_first_program` folder and show `pwd` and the list of files.
2. **Check the compiler:** show the compiler version (the command from lesson 0.4) and the `The CXX compiler identification is Clang 22…` line from configuring.
3. **Configure and build:** use a new build folder, for example `build-mission`.
4. **Run** the built program.
5. **Change the message** to your own, **build again** (without configuring), and show the new result.
6. **Explain** in your own words, one sentence each, what these are for: `main.cpp`, the `clang++` compiler, CMake, Ninja and the executable file.

### Success criterion

- Configuring shows `Clang 22` and the path to our compiler.
- The program in `build-mission` first prints the old message, and after the change and a rebuild, your message.
- Everything was done in the terminal, without CLion.
- The explanations tell the source code apart from the executable, and describe the roles of CMake (the plan), Ninja (carrying out the plan) and the compiler (turning code into a program).

## 8. When things look different

When a command reports an error, **read the first line containing `Error` or `error`**. It usually says what is missing or wrong. The lines after it are often consequences of that first problem.

| What you see | What it means | What to do |
|---|---|---|
| `The source directory … does not appear to contain CMakeLists.txt` | The terminal is in a different folder from the project. | Check `pwd` and `ls`. Go to `lesson_05_first_program`. |
| Windows: `Ignoring extra path from command line: "Files\LLVM\bin\clang++.exe"`, followed by `The CXX compiler identification is unknown` | The quotes are missing: PowerShell split the path at the space in `Program Files`. | Put the whole part in quotes: `"-DCMAKE_CXX_COMPILER=C:\Program Files\LLVM\bin\clang++.exe"`. |
| Configuring shows a compiler other than `Clang 22` | A different compiler path was typed. | Check the path from section 4. |
| A message about changed settings and deleting the cache (`You have changed variables that require your cache to be deleted`) | This build folder already had a configuration with a different compiler. CMake starts it again. | Check that `Clang 22` now appears. If something still doesn't match, delete the build folder in the file window (it goes to the Trash) and configure again. |
| Building ends with an error and there is no program | The executable wasn't created. | Find the first line with `error` in the build output. If you changed the code, check that you didn't remove a quote or another character. |
| The program prints the old message | You ran a program that wasn't rebuilt after the code changed. | Build that program again, or check that you typed the path to the right file. |
| The program isn't recognised when you type just its name | Programs in the current folder aren't on the `PATH` list (lesson 0.3). | Add the path: `./` on macOS and Ubuntu, `.\` on Windows. |
| macOS: `clang++ -std=c++20 …` works, but it's Apple's compiler | On macOS, plain `clang++` is Apple's compiler. | Use the full path from section 5. |

## 9. Explain it

**1.** What is the difference between configuring and building?

<details>
<summary>Answer</summary>

Configuring (`cmake -S . -B …`) prepares the build plan and checks the compiler. Building (`cmake --build …`) carries out that plan and creates the executable file.

</details>

**2.** Why was `cmake --build` enough after changing `main.cpp`, without configuring again?

<details>
<summary>Answer</summary>

The build plan already existed, and nothing in the project itself had changed. Ninja noticed the changed file and built the program again.

</details>

**3.** Why did `first_program_direct` print the old message after `cmake --build build-terminal`?

<details>
<summary>Answer</summary>

Because `cmake --build build-terminal` only built the program in `build-terminal`. `first_program_direct` is a separate file that only changes after compiling it again with `clang++`.

</details>

**4.** Do you need CLion to build a program? So what is it for?

<details>
<summary>Answer</summary>

No. CMake, Ninja and the compiler build the program. CLion calls the same tools and makes work easier: an editor, buttons, windows with results, and later a debugger.

</details>

## Lesson summary

- From the terminal, a program is created in three steps: **configuring** (CMake prepares the plan), **building** (Ninja carries out the plan, calling `clang++`) and **running**.
- Configure once, build after every change to the code.
- A single `main.cpp` can also be compiled directly with `clang++`, but in this course we build with CMake.
- Each executable only changes when it is built again.

## Module 0 summary

Look at the road already behind you:

1. **Lesson 0.1:** files, folders, paths and your first terminal commands.
2. **Lesson 0.2:** moving between folders.
3. **Lesson 0.3:** what commands and programs are, source code and the compiler.
4. **Lesson 0.4:** setting up your workshop: the compiler, CMake, Ninja and CLion.
5. **Lesson 0.5:** your first program, built and run in CLion.
6. **Lesson 0.6:** the same program, built and run on your own, in the terminal.

At the start of Module 0, the terminal may have been completely new to you. Now you can build and run a C++ program on your own.

## What's next: Module 1

In Module 1 you will start to really understand and write C++20 code. You will learn what the lines in `main.cpp` mean, and write your first programs of your own. **Module 1 is in preparation.**

**Previous lesson:** [Lesson 0.5: Your first working program in CLion](lesson_05_first_program_in_clion.en.md) · **Next module:** in preparation · [Course overview](../../README.en.md)

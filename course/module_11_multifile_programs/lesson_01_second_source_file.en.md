# Lesson 11.1: A second source file

[Polski](lesson_01_second_source_file.md) · **English** · [Course overview](../../README.en.md)

> **Module 11, lesson 1** · about 80–100 minutes
> **You need:** your `cpp-workspace` folder and the original `lesson_05_first_program` project, as before. You won't need the debugger in this lesson.
> **Pilot version.** The programs in this lesson, including those built from two source files, are checked automatically on Windows, Ubuntu and macOS, with the given input data. The steps in CLion (a new file, reloading the CMake project, typing input in the **Run** window) are described according to the CLion 2026.2 documentation, without a manual check on every system.

## Before you start

This lesson assumes that you:

- know that building has two stages: the compiler translates a source file into an object file, and the linker joins it with the library code and the startup code into a program (lesson 1.4);
- know the lines of `CMakeLists.txt`, and that `add_executable` gives the program's name and its source file (lesson 1.4);
- tell a function's declaration from its definition, and know that a missing definition of a called function is a link error (lesson 5.6);
- write functions with parameters that return a result (lessons 5.2 and 5.3).

## The situation

The programs of the last modules have grown. The solution of the test in lesson 10.5 has a type, two functions and `main` in one file. The longer a file, the harder it is to find the function you need in it. That's why bigger programs consist of several source files. In this lesson you'll move one function into a second `.cpp` file and answer two questions: **what must `main.cpp` know about a function whose definition is in another file?** And **how do the tools know that the program consists of two files?**

After this lesson you will:

- build one program from two `.cpp` files;
- put a function's declaration in `main.cpp` and its definition in a second file;
- check that a declaration matches its definition;
- add a source file to `add_executable` in `CMakeLists.txt`;
- explain that every `.cpp` file is compiled separately, and that the linker joins the results into one program;
- recognise a link error when the file with a definition exists but isn't built, and fix it in `CMakeLists.txt`.

## 1. Prepare the project

In `cpp-workspace`, create a folder `lesson_11_1` and copy `main.cpp` and `CMakeLists.txt` from the original `lesson_05_first_program` into it. In this lesson you'll change both files in this folder and add a third.

If you work in CLion, open this folder as in lesson 1.1: **File | Open**, then **Trust Project** and the **Debug** profile. In the **CMake** window, check that the compiler is `Clang 22`.

The programs in this lesson print no questions. After starting one, type both numbers straight away, separated by a space, and press **Enter**. We assume valid data: two small non-negative numbers. The programs don't check the read, so that nothing distracts from the split into files. A program meant to accept any data would check the read, as in lesson 4.5.

## 2. The starting point: a declaration and a definition in one file

The program calculates the points for solved tasks. Each solved task gives 3 points, and bonus points are added to the result. Type it into `main.cpp` in the `lesson_11_1` folder:

<!-- example: points_one_file -->
```cpp
#include <iostream>

int calculate_points(int solved, int bonus);

int main() {
    int solved{0};
    int bonus{0};

    std::cin >> solved;
    std::cin >> bonus;

    std::cout << "Points: " << calculate_points(solved, bonus) << "\n";
}

int calculate_points(int solved, int bonus) {
    const int points_per_task{3};
    return solved * points_per_task + bonus;
}
```

This is the layout of lesson 5.6: the declaration, `main`, the definition. Running it is optional. For the data `4 2`:

<!-- input: points_one_file -->
```text
4 2
```

<!-- output: points_one_file -->
```text
Points: 14
```

The same signature appears here in two roles:

| Code | What it is | What it's for |
|---|---|---|
| `int calculate_points(int solved, int bonus);` | a **declaration**: the name, the result type and the parameter types, ending with a semicolon | tells the compiler that the function exists and how to call it, so the call in `main` compiles |
| the same signature with a body in braces | a **definition** | provides the behaviour: the instructions that run at every call. The linker must find it |

Thanks to the declaration, the compiler can compile the call before it sees the definition. That's why the definition can stand below `main`, and, in the next section, in another file.

## 3. A second source file

Now you'll move the definition into a new file. In the `lesson_11_1` folder, next to `main.cpp`, create a file `points.cpp`:

- **In CLion** (according to the CLion 2026.2 documentation): in the **Project** window, right-click the project folder, the one that contains `main.cpp`, and choose **New | C/C++ Source File**. Type the name `points` and leave the type `.cpp`. Don't select the **Create an associated header** option: you'll meet your own header files in the next lesson. In the same window, CLion may offer to add the file to the `first_program` target (**Add to targets**). You can use it or not: you'll check `CMakeLists.txt` in section 4 either way. If CLion puts a comment into the new file, for example with the file name and a date, you can keep it or delete it: a comment doesn't change the program.
- **In another text editor** that saves plain text: save the file as `points.cpp` in the same folder as `main.cpp`.

Then:

1. **Cut** the whole definition of `calculate_points` out of `main.cpp`, from the signature to the closing brace.
2. **Paste** it into `points.cpp`.
3. **Keep** `#include <iostream>`, the declaration and `main` in `main.cpp`.

Don't copy the definition: after the move, it must be only in `points.cpp`.

**`main.cpp`** after the change:

<!-- example: points -->
```cpp
#include <iostream>

int calculate_points(int solved, int bonus);

int main() {
    int solved{0};
    int bonus{0};

    std::cin >> solved;
    std::cin >> bonus;

    std::cout << "Points: " << calculate_points(solved, bonus) << "\n";
}
```

**`points.cpp`**:

<!-- file: points points.cpp -->
```cpp
int calculate_points(int solved, int bonus) {
    const int points_per_task{3};
    return solved * points_per_task + bonus;
}
```

| File | What it contains | What it doesn't contain |
|---|---|---|
| `main.cpp` | `#include <iostream>`, the declaration of `calculate_points` and `main`: reading, the call and printing the result | the definition of `calculate_points` |
| `points.cpp` | the definition of `calculate_points` | `main`, reading, printing and `#include <iostream>` |

- `points.cpp` doesn't need `#include <iostream>`: the function reads and prints nothing, and uses only `int`.
- The program has one `main`, in `main.cpp`. Running starts from it, as before.

You don't build the program yet: first the tools must be told that it has two source files.

## 4. Add the file to `CMakeLists.txt`

The file `points.cpp` in the project folder doesn't change anything by itself. The tools build only the source files that `add_executable` lists, and the copied `CMakeLists.txt` has only `main.cpp`. Change one line in it, so that the whole file looks like this:

<!-- cmake: points -->
```cmake
cmake_minimum_required(VERSION 3.28)
project(first_program LANGUAGES CXX)

add_executable(first_program main.cpp points.cpp)
target_compile_features(first_program PRIVATE cxx_std_20)
set_target_properties(first_program PROPERTIES CXX_EXTENSIONS OFF)
```

- **The only change** from the lesson 0.5 file: in the `add_executable` line, `main.cpp` is followed by a space and `points.cpp`. The other lines stay the same.
- You add a **file name**, not a function name. CMake doesn't know which functions the files contain. It writes a plan: compile every listed file and join the results into the program `first_program`.
- **The order of the names isn't the order of running.** `add_executable(first_program points.cpp main.cpp)` builds the same program. Running always starts from `main`.
- If CLion added `points.cpp` itself, compare that line with the one shown above. In this lesson, all source files stand on one `add_executable` line, separated by spaces.

## 5. Build and run the program of two files

**In CLion** (according to the CLion 2026.2 documentation, without a manual check on every system):

1. After a change to `CMakeLists.txt`, CLion shows a notice that the CMake project needs to be reloaded. Click it, or choose **Tools | CMake | Reload CMake Project**. When CLion added the file to the target itself, it reloads the project automatically.
2. Choose **Build | Build Project**.
3. Click **Run** (▶), type `4 2` in the **Run** window and press **Enter**.

**In the terminal:**

1. Go to the `lesson_11_1` folder, as in lesson 0.6.
2. Configure the project in the `build-terminal` folder, with the same command as in lesson 1.4:

   | System | Configuring |
   |---|---|
   | Windows | `cmake -S . -B build-terminal -G Ninja -DCMAKE_BUILD_TYPE=Debug "-DCMAKE_CXX_COMPILER=C:\Program Files\LLVM\bin\clang++.exe"` |
   | macOS | `cmake -S . -B build-terminal -G Ninja -DCMAKE_BUILD_TYPE=Debug -DCMAKE_CXX_COMPILER=/opt/homebrew/opt/llvm@22/bin/clang++` |
   | Ubuntu | `cmake -S . -B build-terminal -G Ninja -DCMAKE_BUILD_TYPE=Debug -DCMAKE_CXX_COMPILER=/usr/bin/clang++-22` |

   On a Mac with an Intel processor, type `/usr/local/opt/llvm@22` instead of `/opt/homebrew/opt/llvm@22`, as in lesson 0.6.
3. Build: `cmake --build build-terminal`. If `build-terminal` already existed before the change to `CMakeLists.txt`, you don't need to configure again: as in lesson 1.4, Ninja notices the change and runs CMake by itself first (`Re-running CMake...`).
4. Run the program: `.\build-terminal\first_program.exe` (macOS and Ubuntu: `./build-terminal/first_program`), type `4 2` and press **Enter**.

In the build output, in the **Build** window or in the terminal, find the lines about compiling and linking. They look roughly like this:

```text
Building CXX object CMakeFiles/first_program.dir/main.cpp.o
Building CXX object CMakeFiles/first_program.dir/points.cpp.o
Linking CXX executable first_program
```

There are **two** `Building CXX object` lines, one for each `.cpp` file, and **one** `Linking` line. On Windows, object files end in `.obj` and the program in `.exe`. The first two lines may come in another order, and the earlier steps, for example `Scanning ... for CXX dependencies`, prepare the build.

For the data:

<!-- input: points -->
```text
4 2
```

the program prints:

<!-- output: points -->
```text
Points: 14
```

The same as the one-file program in section 2: the function's logic hasn't changed, only the place of its definition has.

**Predict** what the program prints for the data `0 5`, and compare with the collapsed result. Running it is optional.

<!-- input: points -->
```text
0 5
```

<details>
<summary>Standard output for 0 5</summary>

<!-- output: points -->
```text
Points: 5
```

Zero solved tasks give 0 points for tasks, so the result is the bonus points alone: `0 * 3 + 5`.

</details>

## 6. How the compiler and the linker work together

```text
main.cpp    ──►  compiling  ──►  main.cpp.o    ──┐
                                                ├──►  linking  ──►  first_program
points.cpp  ──►  compiling  ──►  points.cpp.o  ──┘
```

- **Every `.cpp` file is compiled separately.** When compiling `main.cpp`, the compiler doesn't see `points.cpp`, and when compiling `points.cpp`, it doesn't see `main.cpp`. Each file gives a separate object file. A source file together with what its `#include` lines insert is called a **translation unit**. You won't need that name in the tasks.
- **A declaration is enough to compile a call.** In `main.cpp`, the compiler knows the name, the result type and the parameter types of `calculate_points` from the declaration, so it can prepare the call. It doesn't need the function's body.
- **The definition is compiled in the second file.** The function's instructions go into `points.cpp.o`.
- **The linker joins both object files into one program.** The call in `main.cpp.o` needs a matching definition, and the linker finds it in `points.cpp.o`. In lesson 5.6 the program had one object file; now the linker searches all the ones it gets.
- **You don't glue the files together by hand.** It's enough that both are in `add_executable`: CMake and Ninja compile each of them and give the linker both object files.

**The declaration and the definition must match**, as in lesson 5.6:

| What | In the declaration (`main.cpp`) | In the definition (`points.cpp`) |
|---|---|---|
| the function's name | `calculate_points` | `calculate_points` |
| the result type | `int` | `int` |
| the number of parameters | 2 | 2 |
| the parameter types, in the same order | `int`, `int` | `int`, `int` |

The parameter names may differ. The compiler that compiles `main.cpp` doesn't see the definition, so it won't compare it with the declaration. Compare them yourself, every time you change one of them. This lesson doesn't cover what a mismatch leads to: keep the declaration and the definition matching.

**We don't join `.cpp` files with `#include`.** `#include` inserts the text of another file (lesson 1.4). The linker joins a program's source files, and `add_executable` lists them. Question 9 in section 10 explains why `#include "points.cpp"` would be a bad idea.

## 7. Mission: the cost of tickets

A cinema's box office sells two kinds of tickets: a **regular** one for 12 units and a **reduced** one for 7 units. The program reads the number of tickets of both kinds and prints the total cost.

**Requirements:**

- The program reads two whole numbers separated by a space: first the number of regular tickets, then the number of reduced tickets. It prints no questions.
- The total cost is the number of regular tickets times 12 plus the number of reduced tickets times 7.
- The program prints exactly one line, `Total cost: N`, with no extra messages.
- **The cost is calculated by your function, whose definition stands in a second `.cpp` file.** You choose the names of the function and its parameters yourself.
- `main.cpp` contains the function's declaration and `main`: reading, calling the function and printing the result. It doesn't contain the function's definition.
- The second `.cpp` file contains only the function's definition: no `main`, no reading and no printing.
- `CMakeLists.txt` is the lesson 0.5 file with the second file added on the `add_executable` line.
- Don't include the second file with `#include`, and don't copy the definition into `main.cpp`.
- The values are non-negative and small, and the result fits in an `int`. The program doesn't need to check the data or handle a failed read.

In `cpp-workspace`, create a folder `ticket_cost`, copy `CMakeLists.txt` from the original `lesson_05_first_program` into it, and create an empty `main.cpp` and a second `.cpp` file with a name of your choice. The second file's name consists of lowercase English letters, digits and `_`, starts with a letter and ends in `.cpp`, for example `prices.cpp`. It can't be `main.cpp`. Write the program yourself.

**Data A:** two regular tickets and three reduced ones.

<!-- input: tickets -->
```text
2 3
```

<!-- output: tickets -->
```text
Total cost: 45
```

**Data B:** no regular tickets.

<!-- input: tickets -->
```text
0 4
```

<!-- output: tickets -->
```text
Total cost: 28
```

**Data C:** no tickets at all.

<!-- input: tickets -->
```text
0 0
```

<!-- output: tickets -->
```text
Total cost: 0
```

**Predict D:** regular tickets only, three of them.

<!-- input: tickets -->
```text
3 0
```

<details>
<summary>Standard output for data D</summary>

<!-- output: tickets -->
```text
Total cost: 36
```

</details>

**This isn't the points calculator with new names.** The function has two prices and other parameters, and you create the project from an empty `main.cpp`. You must decide yourself:

1. what to call the function;
2. what to call its parameters;
3. how to write the declaration;
4. how to write the definition, so that it matches the declaration;
5. where the declaration stands;
6. where the definition stands;
7. what `main()` contains;
8. what to call the second `.cpp` file;
9. which files to list in `add_executable`;
10. which data to check the program with.

**Before you write the program**, prepare a short table: the data A–D and at least one case of your own, with the expected result calculated on paper.

**Then** run the program for data A and one boundary case: B or C. Compare the other cases with the results in your table. All cases A–D are checked automatically in the reference solution.

### Success criterion

- The program builds as C++20 from two `.cpp` files and, for data A and for B or C, prints exactly the result shown.
- Your predictions for the other cases match the results given above.
- `main.cpp` has the function's declaration and `main`, and no definition. The second file contains only the definition: no `main`, reading or printing.
- The declaration matches the definition: the same name, result type, number and types of parameters.
- `CMakeLists.txt` differs from the lesson 0.5 file only by the second file's name on the `add_executable` line.
- At the first build, the output shows both `.cpp` files being compiled.
- No file includes a `.cpp` file with `#include`.
- You can say what the compiler knows about the function when it compiles each of the files, and what the linker joins.

When the result matches, you can save the project in Git, as in lesson 1.5. This time three files belong in the commit: `main.cpp`, the second `.cpp` file and `CMakeLists.txt`. Before the commit, check in `git status` that the second `.cpp` file is among them.

<details>
<summary>Hint 1</summary>

What must `main.cpp` know about a function defined in another file? The compiler that compiles `main.cpp` doesn't look into the second file. What it needs at the place of the call is given by one line ending with a semicolon.

</details>

<details>
<summary>Hint 2</summary>

Why should the definition be in the second `.cpp`, and why must the file be added to CMake? The definition is the function with its body, that is, with the calculation. A file that isn't in `add_executable` isn't compiled, so the linker won't get its definition.

</details>

<details>
<summary>Hint 3</summary>

How do you compare the declaration with the definition, and check the list of sources in `add_executable`? Write both signatures one below the other and compare the name, the result type, the number and the types of the parameters. `add_executable` must contain `main.cpp` and the second file's name, exactly as it is on disk.

</details>

The example solution is in [Example solutions](#example-solutions).

## 8. Find the bug: the file exists, but isn't built

Do this task **after the mission**. Someone prepared a new project of the points calculator the way it's done in every lesson so far: they copied `CMakeLists.txt` from the original `lesson_05_first_program`, and `main.cpp` and `points.cpp` from the `lesson_11_1` folder. Both source files exist and are correct.

Recreate this project: in `cpp-workspace`, create a folder `points_link_check` and copy `main.cpp` and `points.cpp` from `lesson_11_1`, and `CMakeLists.txt` from the original `lesson_05_first_program`, into it. Don't change anything in them.

<details>
<summary>The files of the project to check: open them after the mission</summary>

**`main.cpp`**, the same as in section 3:

<!-- broken: points_link_check stage=link error=undefined reference to .calculate_points\(int, int\)'|undefined symbol: int __cdecl calculate_points\(int, int\)|"calculate_points\(int, int\)", referenced from -->
```cpp
#include <iostream>

int calculate_points(int solved, int bonus);

int main() {
    int solved{0};
    int bonus{0};

    std::cin >> solved;
    std::cin >> bonus;

    std::cout << "Points: " << calculate_points(solved, bonus) << "\n";
}
```

**`points.cpp`**, the same as in section 3:

<!-- file: points_link_check points.cpp -->
```cpp
int calculate_points(int solved, int bonus) {
    const int points_per_task{3};
    return solved * points_per_task + bonus;
}
```

**`CMakeLists.txt`**, the same as in the original `lesson_05_first_program`:

<!-- cmake: points_link_check -->
```cmake
cmake_minimum_required(VERSION 3.28)
project(first_program LANGUAGES CXX)

add_executable(first_program main.cpp)
target_compile_features(first_program PRIVATE cxx_std_20)
set_target_properties(first_program PROPERTIES CXX_EXTENSIONS OFF)
```

</details>

**Before you build**, answer in writing:

1. **Predict:** will the build succeed? If not, at which stage: compiling or linking?
2. Which file contains the definition of `calculate_points`?
3. Which files does `add_executable` in `CMakeLists.txt` list?
4. Why isn't the file `points.cpp` in the project folder enough by itself?

**Then:**

5. Build the project: in the terminal (configure `build-terminal` as in section 5, then `cmake --build build-terminal`) or in CLion (open the folder as in section 1 and choose **Build | Build Project**). Read the build output: which files were compiled, and what does the linker report?
6. Add `points.cpp` to `add_executable`, as in section 4. Don't change `main.cpp` or `points.cpp`.
7. Build the project again (in CLion, reload the CMake project first), run the program and type `4 2`. Compare the result with section 5.
8. Explain why the fix didn't need any change to the function's code.

<details>
<summary>What happens, and why: open it after building the broken project</summary>

1. **Compiling succeeds.** The build output has one `Building CXX object` line, for `main.cpp`. The compiler knows `calculate_points` from the declaration, so the call compiles. `points.cpp` isn't compiled at all, because it isn't in `add_executable`.
2. **Linking fails.** The linker gets only the object file of `main.cpp`. It looks for the definition of `calculate_points`, because `main` calls it, and doesn't find it. The message depends on the system: on Ubuntu ``undefined reference to `calculate_points(int, int)'``, on macOS `"calculate_points(int, int)", referenced from`, and on Windows `undefined symbol: int __cdecl calculate_points(int, int)`. At the end there's `linker command failed`.
3. **No program is created.**

This is the same kind of error as in lesson 5.6, section 7: the called function has no definition in the program. The difference: there, the definition wasn't anywhere; here, it's in a file the tools don't build. For CMake, a file on disk isn't yet part of the program. A file listed in `add_executable` is.

After `points.cpp` is added, Ninja first runs CMake by itself, then compiles `points.cpp` and links the program. `main.cpp` may not be compiled again: it hasn't changed, and its object file already exists. The program prints `Points: 14`, as in section 5.

The C++ code was correct from the start. The error wasn't in any `.cpp` file but in the list of files to build, which is why the fix concerns `CMakeLists.txt` only.

| Situation | The stage that fails | Cause | Fix |
|---|---|---|---|
| a call with no declaration in `main.cpp` | compiling `main.cpp` | the compiler doesn't know the function at the place of the call | add the declaration before `main` |
| `points.cpp` isn't in `add_executable` (this section) | linking | the definition doesn't get into the program | add `points.cpp` to `add_executable` |
| `add_executable` lists a file that isn't in the project folder | configuring (CMake) | CMake doesn't find the source file | fix the name in `add_executable` or the file's name |
| both files in `add_executable`, the declaration matching the definition | the build succeeds | | |

</details>

The fixed project is in [Example solutions](#example-solutions).

## 9. When something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `undefined reference`, `undefined symbol` or `referenced from` with your function's name, and `linker command failed` at the end | Compiling succeeded, but the linker doesn't find the definition: the second file isn't in `add_executable`, or the definition doesn't match the declaration. | Check the `add_executable` line. Then compare the declaration with the definition: the name, the result type, the number and the types of the parameters. |
| At the first build, there's only one `Building CXX object` line, for `main.cpp`, or after a change to `CMakeLists.txt` CLion builds as if nothing had changed | The second file isn't built: it isn't in `add_executable`, or CLion hasn't reloaded the changed `CMakeLists.txt` yet. | Add the file to `add_executable`. In CLion, click the reload notice or choose **Tools \| CMake \| Reload CMake Project**. |
| `CMake Error at CMakeLists.txt:4 (add_executable):` and `Cannot find source file:` | A name in `add_executable` doesn't match the file in the project folder: a typo, a different case, the file in another folder, or an extra extension added by the editor, for example `points.cpp.txt` (Windows hides known extensions by default). The compiler hasn't started yet (lesson 1.4). | Check the file's name in the terminal with `ls`, and compare it with the name in `add_executable`, letter by letter. |
| `use of undeclared identifier` with the function's name, in `main.cpp` | `main.cpp` lacks the declaration, or it stands below the call. A definition in the second file isn't enough for the compiler. | Add the declaration before `main`. |
| The linker reports that the function or `main` is defined more than once, for example `duplicate symbol` or `multiple definition` | The same definition is in two files: the definition was copied instead of moved, both files have a `main`, or `main.cpp` includes the second file with `#include`. | Keep the function's definition only in the second file, and `main` only in `main.cpp`. Don't include `.cpp` files with `#include`. |
| A header file appeared next to `points.cpp`, and `points.cpp` has an `#include` line with its name | **Create an associated header** was selected in CLion's new-file window. | Delete that file, the `#include` line from `points.cpp`, and the header's name from `add_executable` if CLion added it there. You'll meet your own header files in the next lesson. |
| The program prints nothing and waits | It's waiting for the second number. | Type both numbers and press **Enter**. |

## 10. Explain

Answer in your own words, preferably in writing. Only then compare with the example answers.

1. What is in `main.cpp`, and what in `points.cpp`? What isn't in `points.cpp`, and why?
2. Why does `main.cpp` need the declaration of `calculate_points`, if the definition is in `points.cpp`?
3. What does the definition provide, and when do its instructions run?
4. What must be the same in the declaration and in the definition? Why do you have to check that they match yourself?
5. What changed in `CMakeLists.txt`? Does the order of the names in `add_executable` decide the order of running?
6. `points.cpp` is in the project folder. Why isn't that enough to make it part of the program?
7. What does the compiler do, and what the linker, when you build the demonstration? How many object files are created?
8. How can you tell that the error in section 8 is a link error? Why was fixing `CMakeLists.txt` enough?
9. Why don't we include `points.cpp` in `main.cpp` with `#include "points.cpp"`?
10. For `4 2`, the program of two files prints the same as the one-file program. Why? And what would be needed if a third `.cpp` file also called `calculate_points`?

<details>
<summary>Example answers</summary>

1. `main.cpp` has `#include <iostream>`, the declaration of `calculate_points` and `main` with reading, the call and printing the result. `points.cpp` has only the function's definition. It has no `main`, because a program has one `main`, and no reading or printing, because those are `main`'s jobs. It has no `#include <iostream>` either, because the function doesn't use it.
2. Because the compiler compiles `main.cpp` separately and doesn't look into `points.cpp`. At the place of the call, it must know the name, the result type and the parameter types, and the declaration gives them. Without it, compiling `main.cpp` would end with the error `use of undeclared identifier`.
3. The function's body, that is, the instructions of the calculation. They run at every call, while the program runs. A declaration runs nothing.
4. The function's name, the result type, the number of parameters and their types in the same order. The parameter names may differ. The compiler that compiles `main.cpp` doesn't see the definition in `points.cpp`, so it won't compare them.
5. The name `points.cpp` was added to the `add_executable` line: the name of a file to build, not of a function. The order of the names doesn't matter for running, because running always starts from `main`.
6. Because the tools build only the files listed in `add_executable`. CMake doesn't search the folder for `.cpp` files. A file that isn't on the list isn't compiled, so its definitions don't get into the program.
7. The compiler works twice, separately for each `.cpp` file, and creates two object files: `main.cpp.o` and `points.cpp.o` (`.obj` on Windows). The linker joins both, together with the library code and the startup code, into one program `first_program`. It matches the call of `calculate_points` in `main` with the definition in `points.cpp.o`.
8. Compiling `main.cpp` succeeded: there's a `Building CXX object` line, and no message points to an error in a line of `main.cpp`. The output ends with `linker command failed` and a message with the name `calculate_points`. The C++ code was correct; only `points.cpp` was missing from the list of files to build. Once it was added, the definition got into the program.
9. `#include` inserts the whole text of a file, so the definition would be compiled together with `main.cpp`. When `points.cpp` is also in `add_executable`, the definition would get into the program twice, and the linker would report that the function is defined more than once. Without `points.cpp` in `add_executable`, the program would in practice be one file again. The linker joins `.cpp` files, and `add_executable` lists them.
10. Because `main` and the function contain the same instructions. Splitting into files changes how the code is organised and how it's built, not what the program calculates. A third file would need its own copy of the declaration, and every copy would have to be fixed at every change to the function. The next lesson answers this problem.

</details>

## Summary

- One program can consist of several `.cpp` files. The program has one `main`.
- In the file that calls a function, a declaration is enough. The definition can stand in another `.cpp` file.
- The declaration and the definition must match: the name, the result type, the number and types of parameters. The compiler won't compare them across files, so compare them yourself.
- The tools build only the files listed in `add_executable`. You add every new `.cpp` file on that line. The order of the names doesn't change the order of running.
- Every `.cpp` file is compiled separately, into its own object file. The linker joins the object files into one program.
- A file with a definition that isn't in `add_executable` gives a link error. Adding the file in `CMakeLists.txt` fixes it, with no change to the C++ code.
- `.cpp` files aren't included with `#include`.

## What's next

In this lesson, the declaration of `calculate_points` stood in `main.cpp`. But what if different files are to use the same function? Each would then need its own copy of the declaration, and every change to the function would mean fixing all the copies. In the next lesson of Module 11, the declaration will go into one shared place: your own header file. Go on to [lesson 11.2: Your own header file](lesson_02_own_header_file.en.md).

---

## Example solutions

Look here **after your own attempt**. Your names of the function, the parameters and the second file may differ, as long as the standard output is as required.

<details>
<summary>Section 7: the mission, the cost of tickets</summary>

**`main.cpp`**:

<!-- example: tickets -->
```cpp
#include <iostream>

int total_cost(int regular_tickets, int reduced_tickets);

int main() {
    int regular_tickets{0};
    int reduced_tickets{0};

    std::cin >> regular_tickets;
    std::cin >> reduced_tickets;

    std::cout << "Total cost: " << total_cost(regular_tickets, reduced_tickets) << "\n";
}
```

**`tickets.cpp`**, next to `main.cpp`:

<!-- file: tickets tickets.cpp -->
```cpp
int total_cost(int regular_tickets, int reduced_tickets) {
    const int regular_price{12};
    const int reduced_price{7};
    return regular_tickets * regular_price + reduced_tickets * reduced_price;
}
```

**`CMakeLists.txt`**:

<!-- cmake: tickets -->
```cmake
cmake_minimum_required(VERSION 3.28)
project(first_program LANGUAGES CXX)

add_executable(first_program main.cpp tickets.cpp)
target_compile_features(first_program PRIVATE cxx_std_20)
set_target_properties(first_program PROPERTIES CXX_EXTENSIONS OFF)
```

| Data | Standard output | What it checks |
|---|---|---|
| A: `2 3` | `Total cost: 45` | both kinds of tickets |
| B: `0 4` | `Total cost: 28` | no regular tickets |
| C: `0 0` | `Total cost: 0` | no tickets at all |
| D: `3 0` | `Total cost: 36` | regular tickets only |

- **The organisation of the files:** `main.cpp` reads the data, calls the function and prints the result. `tickets.cpp` contains only the definition of `total_cost`. `CMakeLists.txt` lists both files on the `add_executable` line, and the other lines are as in lesson 0.5.
- **The declaration and the definition:** the declaration at the start of `main.cpp` has the same name, result type and parameter types as the definition in `tickets.cpp`. Thanks to it, the call in `main` compiles.
- **The prices are constants in the definition.** They belong to the rule for calculating the cost, so they stand in the function, not in `main`. When a price changes, you change only `tickets.cpp`.
- **Compiling and linking:** the compiler creates two object files, `main.cpp.o` and `tickets.cpp.o`. The linker joins them into one program and matches the call of `total_cost` with the definition.
- **Other correct solutions:** other names for the function, the parameters and the file, for example `ticket_cost` and `prices.cpp`; the result stored first in a `const int` variable in `main`; a declaration without parameter names, `int total_cost(int, int);`; the files in `add_executable` in another order.

</details>

<details>
<summary>Section 8: the fixed project</summary>

Compared with the broken project, one line of `CMakeLists.txt` changes: `add_executable(first_program main.cpp)` becomes `add_executable(first_program main.cpp points.cpp)`.

**`CMakeLists.txt`**:

<!-- cmake: points_link_fixed -->
```cmake
cmake_minimum_required(VERSION 3.28)
project(first_program LANGUAGES CXX)

add_executable(first_program main.cpp points.cpp)
target_compile_features(first_program PRIVATE cxx_std_20)
set_target_properties(first_program PROPERTIES CXX_EXTENSIONS OFF)
```

**`main.cpp`**, unchanged:

<!-- example: points_link_fixed -->
```cpp
#include <iostream>

int calculate_points(int solved, int bonus);

int main() {
    int solved{0};
    int bonus{0};

    std::cin >> solved;
    std::cin >> bonus;

    std::cout << "Points: " << calculate_points(solved, bonus) << "\n";
}
```

**`points.cpp`**, unchanged:

<!-- file: points_link_fixed points.cpp -->
```cpp
int calculate_points(int solved, int bonus) {
    const int points_per_task{3};
    return solved * points_per_task + bonus;
}
```

For the same data as in section 5:

<!-- input: points_link_fixed -->
```text
4 2
```

<!-- output: points_link_fixed -->
```text
Points: 14
```

Compiling and linking succeed: `points.cpp` is now on the list of files to build, so its definition gets into the program.

</details>

**Previous lesson:** [Lesson 10.5: Workshop registrations (the Module 10 test)](../module_10_input_records/lesson_05_workshop_registrations.en.md) · **Next lesson:** [Lesson 11.2: Your own header file](lesson_02_own_header_file.en.md) · [Course overview](../../README.en.md)

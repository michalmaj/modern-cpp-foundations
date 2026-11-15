# Lesson 12.1: Your first data file

[Polski](lesson_01_first_data_file.md) · **English** · [Course overview](../../README.en.md)

> **Module 12, lesson 1** · about 90–110 minutes, can be split into two sessions
> **You need:** your `cpp-workspace` folder and the original `lesson_05_first_program` project, as before. You won't need the debugger in this lesson.
> **Pilot version.** The programs in this lesson are checked automatically on Windows, Ubuntu and macOS, with the given data files. The steps in CLion (a new file, the **Working directory** field of the run configuration) are described according to the CLion 2026.3 documentation, without a manual check on every system.

## Before you start

This lesson assumes that you:

- know that a shell always has a current folder, and that a relative path counts from it (lessons 0.1 and 0.2);
- build and run a project with `main.cpp` and `CMakeLists.txt` in CLion, and know that the executable is created in the build folder, usually `cmake-build-debug` (lesson 0.5);
- read numbers with `>>`, which skips spaces and line ends (lesson 2.6);
- check with `fail()` whether a read worked before you check the value (lessons 4.5 and 10.3);
- first read a number that says how many values follow, then read exactly that many values in a loop, and at the first error end `main` with `return 0;`, with no partial report (lesson 10.3).

## The situation

An app on your phone counts steps and records their number at the end of every day. You want to add up the steps of a few days. The programs of Module 10 got their data from the keyboard, so on every run you had to type it again in the **Run** window. When the data already exists somewhere, it's handier to keep it in a **text file**: you prepare it once, and the program reads it by itself on every run.

In this lesson the program will open the file `steps.txt` by itself and read numbers from it. You'll answer three questions: **how does a program open a file? Where does it look for it? What should it do when the file can't be opened, or when data is missing from it?**

After this lesson you will:

- create a simple text file with data for a program;
- open it with `std::ifstream` and check whether opening worked;
- read numbers from it with the familiar `>>` operator and check every read;
- find the program's working directory in CLion and put the data file there;
- tell a missing file, an empty file and a file that announces zero values apart;
- fix the situation in which a correct program doesn't find a correct file.

## 1. The data file and its contract

`steps.txt` is an ordinary text file, like `list.txt` in lesson 0.1. In it, the data for two days looks like this:

<!-- run: steps -->

<!-- datafile: steps steps.txt -->
```text
2
4200
7350
```

**The file's contract**, that is, the rules the file must follow so that the program can compute a result from it:

- the first number is the number of days, from 0 to 5;
- it is followed by exactly as many numbers as there are days: the steps of the successive days, each number from 0 to 20000;
- the numbers are separated by spaces or line ends. In the examples each one is on its own line, because the file is easier to read that way, but `>>` skips spaces and line ends just as when reading from the keyboard (lesson 2.6). So line boundaries don't matter to the program;
- the program reads only the numbers that the first number announces. Whether anything else follows them in the file isn't checked in this lesson.

The largest possible total is 5 · 20000 = 100000, so for data that follows the contract the result safely fits in an `int`.

The program prints the report only when it has read and checked all the required numbers. Every other situation ends with one message, with no partial report:

| Situation | Standard output |
|---|---|
| the file couldn't be opened | `Cannot open steps.txt` |
| the file is open, but a required number couldn't be read | `Input error` |
| a number is read, but it's outside its range, the number of days included | `Invalid steps` |
| all the required numbers are read and valid | `Days: N` and `Total steps: T` |

After each of these results the program ends with exit code 0, as in Module 10. The messages go to standard output.

**A data file isn't a source file.** `main.cpp` and `steps.txt` are both ordinary text files, but they have different roles:

| | `main.cpp` | `steps.txt` |
|---|---|---|
| what it holds | the program's code | data that the program reads |
| who reads it | the compiler, while building | the running program, while it runs |
| whether it's in `add_executable` | yes | no |
| what you do after changing it | build the program again | nothing: just run the program again |

## 2. Your first file stream: `std::ifstream`

This program opens `steps.txt`, checks the data against the contract and prints the report:

<!-- example: steps -->
```cpp
#include <fstream>
#include <iostream>

int main() {
    std::ifstream input{"steps.txt"};

    if (input.fail()) {
        std::cout << "Cannot open steps.txt\n";
        return 0;
    }

    int days{0};
    input >> days;

    if (input.fail()) {
        std::cout << "Input error\n";
        return 0;
    }

    if (days < 0 || days > 5) {
        std::cout << "Invalid steps\n";
        return 0;
    }

    int total_steps{0};

    for (int day{0}; day < days; ++day) {
        int steps{0};
        input >> steps;

        if (input.fail()) {
            std::cout << "Input error\n";
            return 0;
        }

        if (steps < 0 || steps > 20000) {
            std::cout << "Invalid steps\n";
            return 0;
        }

        total_steps += steps;
    }

    std::cout << "Days: " << days << "\n";
    std::cout << "Total steps: " << total_steps << "\n";
}
```

Only three lines are new: `#include <fstream>`, the creation of the variable `input` and the `input.fail()` check right after it. The rest is the pattern of lesson 10.3, except that the program reads from `input` instead of `std::cin`.

| Code | What it does |
|---|---|
| `#include <fstream>` | includes the header of file streams, just as `<iostream>` includes `std::cin` and `std::cout` |
| `std::ifstream input{"steps.txt"};` | creates a variable `input` of type `std::ifstream` and at once tries to open the file named `steps.txt` for reading. It doesn't read any data yet |
| `input.fail()` right after creating it | `true` when the file couldn't be opened; the same member function as `std::cin.fail()` in lesson 4.5 |
| `input >> days;` | reads a number from the file just as `std::cin >> days;` reads it from the keyboard |
| `input.fail()` after a read | `true` when the read didn't work, as before |

- **`std::ifstream`** is short for *input file stream*. `std::cin` is a stream from the keyboard, and `input` is a stream from a file. You read from both in the same way: with `>>`, and you check success with `fail()`.
- **You choose the variable's name yourself.** `input` is an ordinary variable name, like `count` or `total`.
- **The file closes by itself** when the variable `input` stops existing, here at the end of `main`. You don't have to close it by hand.

**The order of the checks** is the same for every required number:

1. Did the file open? If not: `Cannot open steps.txt`. Without an open file there's nothing to read.
2. Did reading the number work? If not: `Input error`. The program doesn't compare a value it couldn't read with the range.
3. Is the number that was read inside its range? If not: `Invalid steps`.
4. Only then does the program move on to the next number.

**A failed open isn't the same as a failed read.** A failed open means that the program couldn't open the requested file for reading. This can happen when the file isn't where the program looks for it (section 4), or when the system doesn't allow it to be opened. That's why the message says `Cannot open`, not "the file doesn't exist". A failed read means that the file is open, but where a required number should be there's something else, or nothing.

## 3. Prepare the project

The project of this lesson looks like this:

```text
lesson_12_1/
├── CMakeLists.txt
├── main.cpp
└── steps.txt
```

1. In `cpp-workspace`, create a folder `lesson_12_1` and copy `main.cpp` and `CMakeLists.txt` from the original `lesson_05_first_program` into it.
2. Leave `CMakeLists.txt` unchanged. It lists only `main.cpp`, and that's how it should stay.
3. Open the folder in CLion as in lesson 1.1: **File | Open**, then **Trust Project** and the **Debug** profile.
4. Replace the contents of `main.cpp` with the program of section 2.
5. Create a file `steps.txt` in the folder `lesson_12_1`, next to `main.cpp` and `CMakeLists.txt`:
   - **In CLion** (according to the CLion 2026.3 documentation): in the **Project** window, right-click the folder `lesson_12_1` and choose **New | File**, not **New | Directory**: `steps.txt` must be an ordinary text file, not a folder with that name. Type the name `steps.txt` and press **Enter**.
   - **In another text editor** that saves plain text: save the file as `steps.txt` in the folder `lesson_12_1`.
6. Type the three numbers of section 1 into `steps.txt`, each on its own line, and save the file. After the last number you may press **Enter** or not: the program reads the data the same way (section 6, case G).

**Don't add `steps.txt` to `add_executable`.** CMake describes which source files to build the program from, and `steps.txt` isn't code. The compiler never reads it. The file is opened only by the running program, at the moment the line with `std::ifstream` runs.

Don't run the program yet: first find out where it will look for the file.

## 4. The working directory: where the program looks for the file

`"steps.txt"` in the program is a **relative path**: just a name, with no folders. You know from lesson 0.1 that a relative path counts from the current folder. Every running program, not only the shell, has its own current folder. It's called the **working directory**. That's where `pwd` comes from: *print working directory*. The program looks for `steps.txt` precisely in its working directory.

The working directory is **not** automatically:

- the folder where `main.cpp` is;
- the folder with `CMakeLists.txt`;
- the folder where the executable is, for example `cmake-build-debug`;
- the folder `cpp-workspace`, or any other that seems to be the "main" one.

The working directory is a setting of the **run**, not of the code. The same executable, run twice with different working directories, can find the file one time and not the next. The code doesn't change.

**The working directory isn't the build folder either.** The build folder, for example `cmake-build-debug`, is where CMake and Ninja save the object files and the executable. Changing the working directory doesn't build anything and doesn't move the program. It only changes the place from which the program counts relative paths.

**Check the working directory in CLion** (according to the CLion 2026.3 documentation, without a manual check on every system):

1. Choose **Run | Edit Configurations**. The **Run/Debug Configurations** window opens.
2. On the left, in the **CMake Application** group, choose the configuration `first_program`.
3. Find the field **Working directory** and read its value.
4. According to the CLion documentation, the field points to the project folder by default, here `lesson_12_1`. It may be a full path ending in `lesson_12_1`, or the notation `$ProjectFileDir$`, which CLion uses for the project folder. In that case change nothing.
5. If the field is empty or points to another folder, set the folder `lesson_12_1` in it, the one with `steps.txt`: click the folder icon at the end of the field and select `lesson_12_1`, or type its full path.
6. Confirm with **OK**. The change applies only to this configuration, not to other projects.

Don't assume that CLion sets the same folder on every computer and in every version. Always read the field.

**In the terminal,** the program's working directory is the shell's current folder from which you start the program. If you start the program from the folder `lesson_12_1`, with the command of lesson 1.4, the program looks for `steps.txt` precisely in `lesson_12_1`. The terminal is optional in this lesson.

**The course's automatic checks and your computer.** When the course checks the programs of this lesson automatically, it creates the data file itself, each one in a separate, empty folder, and runs the program there. Nobody does that on your computer: you have to create the file yourself and make sure the program runs from the folder where that file is.

## 5. Build and run the demonstration

**In CLion:** choose **Build | Build Project**, then click **Run** (▶) next to the configuration `first_program`. The program doesn't wait for keyboard input: don't type anything in the **Run** window.

**In the terminal** (optional): in the folder `lesson_12_1`, configure and build the project in the folder `build-terminal`, as in lesson 11.1, section 5. Start the program from the folder `lesson_12_1`: `.\build-terminal\first_program.exe` (macOS and Ubuntu: `./build-terminal/first_program`).

For the file of section 1 the program prints:

<!-- output: steps -->
```text
Days: 2
Total steps: 11550
```

The program opened `steps.txt`, read the number of days `2`, then two step counts, and printed their total: 4200 + 7350 = 11550.

## 6. A missing file, an empty file and zero days

The same program, with the same `main.cpp`, gives different results for different files. **Predict** each result before you open the collapsed block. Running these cases is optional: to check them, you change only the contents or the name of `steps.txt`, without building again.

**B: zero days.** The file holds one number, `0`:

<!-- run: steps -->

<!-- datafile: steps steps.txt -->
```text
0
```

<details>
<summary>Standard output for B</summary>

<!-- output: steps -->
```text
Days: 0
Total steps: 0
```

This is a valid file: it says that there were zero days. The program read the number `0`, the loop didn't run a single time, and the total stays 0.

</details>

**C: a missing file.** There's no file `steps.txt` in the working directory.

<!-- run: steps -->

<details>
<summary>Standard output for C</summary>

<!-- output: steps -->
```text
Cannot open steps.txt
```

Opening didn't work, so the program reads nothing. It doesn't print `Days: 0`, because it doesn't know how many days a file it never got contains.

</details>

**D: an empty file.** `steps.txt` exists, but there isn't a single character in it:

<!-- run: steps -->

<!-- datafile: steps steps.txt -->
```text
```

<details>
<summary>Standard output for D</summary>

<!-- output: steps -->
```text
Input error
```

Opening worked, because the file exists. What failed was reading the first required number: there's no number in the file.

</details>

**Three situations, three different results:**

| Case | Opening | Reading the number of days | Result |
|---|---|---|---|
| B: a file with `0` | worked | worked: `0` | a report: zero days |
| C: a missing file | failed | — | `Cannot open steps.txt` |
| D: an empty file | worked | failed | `Input error` |

An empty file isn't the same as a file with a zero. A file with `0` holds information: "there were zero days". An empty file holds no information, not even that. If the program didn't check reading the number of days, an empty file would give the same report as a file with `0`, and the program would present missing data as a valid result.

**E: an error in a later number.** The first two numbers are valid, and where the third should be there's a word:

<!-- run: steps -->

<!-- datafile: steps steps.txt -->
```text
2
4200
seven
```

<details>
<summary>Standard output for E</summary>

<!-- output: steps -->
```text
Input error
```

`seven` isn't a number, so the read fails. The program has already added 4200 to the total, but it doesn't print a report: at the first error it ends with one message.

</details>

**F: a forbidden step count.** The third number is read, but it's negative:

<!-- run: steps -->

<!-- datafile: steps steps.txt -->
```text
2
4200
-1
```

<details>
<summary>Standard output for F</summary>

<!-- output: steps -->
```text
Invalid steps
```

`-1` is read correctly, but it isn't inside the range from 0 to 20000. Here too there's no partial report.

</details>

**G: the last number without a line end.** The file holds the same numbers as in section 1, but after `7350` there's no line end any more:

<!-- run: steps -->

<!-- datafile: steps steps.txt noeol -->
```text
2
4200
7350
```

<details>
<summary>Standard output for G</summary>

<!-- output: steps -->
```text
Days: 2
Total steps: 11550
```

The result is the same as in section 5. As in lesson 4.6, a read with `>>` can work even when the data ends right after the number. What decides an error is `fail()`, not whether a line end came after the last number. You don't have to prepare such a file: this case is checked automatically.

</details>

<details>
<summary>The other check cases: open after your predictions</summary>

All these cases are checked automatically. The results follow from the contract of section 1.

**H: a negative number of days.**

<!-- run: steps -->

<!-- datafile: steps steps.txt -->
```text
-1
```

<!-- output: steps -->
```text
Invalid steps
```

**I: six days.** The program reads no step count, because the number of days is already forbidden.

<!-- run: steps -->

<!-- datafile: steps steps.txt -->
```text
6
1000
2000
3000
4000
5000
6000
```

<!-- output: steps -->
```text
Invalid steps
```

**J: a step count of 20001,** one too many.

<!-- run: steps -->

<!-- datafile: steps steps.txt -->
```text
2
4200
20001
```

<!-- output: steps -->
```text
Invalid steps
```

**K: a word instead of the number of days.**

<!-- run: steps -->

<!-- datafile: steps steps.txt -->
```text
two
4200
7350
```

<!-- output: steps -->
```text
Input error
```

**L: the last required number is missing.** The file announces three days, but holds only two step counts.

<!-- run: steps -->

<!-- datafile: steps steps.txt -->
```text
3
4200
7350
```

<!-- output: steps -->
```text
Input error
```

**M: five days.**

<!-- run: steps -->

<!-- datafile: steps steps.txt -->
```text
5
1000
2000
3000
4000
5000
```

<!-- output: steps -->
```text
Days: 5
Total steps: 15000
```

**N: the largest possible total,** five days of 20000 steps.

<!-- run: steps -->

<!-- datafile: steps steps.txt -->
```text
5
20000
20000
20000
20000
20000
```

<!-- output: steps -->
```text
Days: 5
Total steps: 100000
```

**O: both limits of the step range,** 0 and 20000.

<!-- run: steps -->

<!-- datafile: steps steps.txt -->
```text
2
0
20000
```

<!-- output: steps -->
```text
Days: 2
Total steps: 20000
```

**What this program doesn't check.** The next three cases show the limits of reading with `>>`. The program doesn't see the file's lines, only successive numbers:

**P: all the numbers on one line.** The report is the same as in section 5.

<!-- run: steps -->

<!-- datafile: steps steps.txt -->
```text
2 4200 7350
```

<!-- output: steps -->
```text
Days: 2
Total steps: 11550
```

**Q: empty lines between the numbers.** `>>` skips them, so the report is the same again.

<!-- run: steps -->

<!-- datafile: steps steps.txt -->
```text
2

4200

7350
```

<!-- output: steps -->
```text
Days: 2
Total steps: 11550
```

**R: more numbers than the first one announces.** The program reads one step count, and `7350` stays unread.

<!-- run: steps -->

<!-- datafile: steps steps.txt -->
```text
1
4200
7350
```

<!-- output: steps -->
```text
Days: 1
Total steps: 4200
```

</details>

## 7. Diagnostics: the program doesn't find the file

**The situation.** The program is correct, `steps.txt` exists and holds valid data, and yet the program prints `Cannot open steps.txt`. The same message as in case C, although the file is on the disk. This isn't a compile or link error: the program builds and runs. The problem appears only while it runs, when it opens the file.

Recreate this situation in the project `lesson_12_1`. Don't change any of the files:

1. Open **Run | Edit Configurations** and the configuration `first_program`, as in section 4.
2. In the field **Working directory**, set the folder `cmake-build-debug` inside `lesson_12_1`, that is, the one where the executable is: click the folder icon at the end of the field and select it. If your build folder has a slightly different name, choose the one you have. Confirm with **OK**.
3. **Predict** what the program will print. Then click **Run** (▶).

The program prints `Cannot open steps.txt`. Now find the cause as if nobody had told you:

1. Check the file's name in the code and on the disk: `steps.txt` in both places, with no extra extension, such as `steps.txt.txt`.
2. Check the case of the letters: `Steps.txt` is a different name from `steps.txt`. On Ubuntu the case of letters always matters, while on Windows and usually on macOS it doesn't, so such a mistake may show up only on another computer.
3. Check which working directory the configuration has: the field **Working directory**.
4. Check whether `steps.txt` is in that folder.
5. Fix the configuration or the file's location.
6. Run the same program again, with no change to `main.cpp`.

<details>
<summary>What happens and how to fix it: open after steps 1–4</summary>

- **The name and the case of letters are correct.** The program asks for `steps.txt`, and such a file is in `lesson_12_1`.
- **The working directory is `cmake-build-debug`.** The program looks for `steps.txt` there, and the file isn't there. It's in `lesson_12_1`.
- **The fix:** in the field **Working directory**, set the folder `lesson_12_1` back, as in section 4, and run the program again. It prints the report of section 5 again. You don't change `main.cpp`, and you don't build the program again: only the place where the program looks for the file changes.

You could also copy the file into `cmake-build-debug`, but that's a worse fix. The build folder holds files generated by the tools, and the data belongs to the project. Don't write an absolute path into the program either, for example with the name of your home folder: the program would then work only on your computer.

The same cause comes in several forms. The program doesn't find the file when the working directory points somewhere else (this exercise), when the file was saved in another folder, for example in `cmake-build-debug`, and when the file has a different name from the one the program gives. In each of these cases the same question gives the answer: **what is the working directory, and is a file with exactly this name in it?**

</details>

Before you go on, make sure that **Working directory** points to `lesson_12_1` again.

## 8. Mission: pages read in a session

After every reading session you record how many pages were read. The program reads this data from the file `pages.txt` and gives the number of sessions and the total number of pages.

**The contract of the file `pages.txt`:**

- the first number is the number of sessions, from 0 to 5;
- it is followed by exactly as many numbers as there are sessions: the pages read in the successive sessions, each number from 0 to 500;
- the numbers are separated by spaces or line ends;
- the report is created only when all the required numbers are read and valid.

**The messages:**

| Situation | Standard output |
|---|---|
| the file couldn't be opened | `Cannot open pages.txt` |
| the file is open, but a required number couldn't be read | `Input error` |
| a number is read, but it's outside its range, the number of sessions included | `Invalid pages` |
| all the required numbers are read and valid | `Sessions: N` and `Total pages: T` |

The program prints only one of these results and ends with exit code 0, with no partial report and no questions. The largest possible total is 5 · 500 = 2500.

In `cpp-workspace`, create a folder `reading_pages`, copy `CMakeLists.txt` from the original `lesson_05_first_program` into it, and create an empty `main.cpp` and a file `pages.txt`. Open the folder in CLion. Write the program on your own.

You have to decide on your own:

1. what to call the variable of the file stream;
2. where to check whether opening worked;
3. where to check whether reading the number of sessions worked;
4. how to check the range of the number of sessions;
5. how to read the successive page counts;
6. when to check whether reading each of them worked;
7. when to check whether it's inside its range;
8. how to compute the total;
9. how to prevent a partial report;
10. how to set the working directory of the new project;
11. how to check what the program does when the file is missing;
12. how to tell an empty file from a valid file with zero sessions.

**Cases A–G.** Each case is a different version of `pages.txt`, or no file at all.

**A: three sessions.**

<!-- run: pages -->

<!-- datafile: pages pages.txt -->
```text
3
12
0
25
```

<!-- output: pages -->
```text
Sessions: 3
Total pages: 37
```

**B: zero sessions.**

<!-- run: pages -->

<!-- datafile: pages pages.txt -->
```text
0
```

<!-- output: pages -->
```text
Sessions: 0
Total pages: 0
```

**C: a missing file.** There's no `pages.txt` in the working directory.

<!-- run: pages -->

<!-- output: pages -->
```text
Cannot open pages.txt
```

**D: an empty file.** `pages.txt` exists, but it's empty.

<!-- run: pages -->

<!-- datafile: pages pages.txt -->
```text
```

<!-- output: pages -->
```text
Input error
```

**E: a forbidden page count.**

<!-- run: pages -->

<!-- datafile: pages pages.txt -->
```text
2
15
-1
```

<!-- output: pages -->
```text
Invalid pages
```

**F: a word instead of a page count.**

<!-- run: pages -->

<!-- datafile: pages pages.txt -->
```text
2
15
seven
```

<!-- output: pages -->
```text
Input error
```

**G: incomplete data.** The file announces two sessions, but holds only one page count.

<!-- run: pages -->

<!-- datafile: pages pages.txt -->
```text
2
15
```

<!-- output: pages -->
```text
Input error
```

**Before you write the program,** prepare a short table: cases A–G and at least one of your own, for example with a range limit, with the expected result worked out from the contract.

**Then run the program for A and for D.** Between the runs you change only the contents of `pages.txt`, not the code. Trace the other cases on paper, line by line through your program, and compare them with the results given above. If you have time, run C too: the simplest way is to rename the file for a while, for example to `pages_off.txt`, and then restore `pages.txt`. All of cases A–G are checked automatically in the reference solution.

### Success criteria

- The program builds as C++20 and prints exactly the result shown for A and D.
- Your predictions for B, C, E, F and G agree with the results given above.
- The program checks opening the file before it reads anything from it.
- Every read is checked with `fail()` before the program checks the range of that value.
- After the first error the program prints one message and ends, with no partial report.
- `pages.txt` isn't in `add_executable`, and `CMakeLists.txt` is the one of lesson 0.5.
- The configuration's **Working directory** points to the folder with `pages.txt`, and you can say where the program looks for the file and why.
- You can explain why an empty file gives a different result from a file with `0`.

When the result is right, you can save the project in Git, as in lesson 1.5. This time three files belong in the commit: `main.cpp`, `CMakeLists.txt` and `pages.txt` with data A. The data file is part of the project, because without it the program has nothing to read. Don't add the build folder.

<details>
<summary>Hint 1: opening the file</summary>

Which header gives you the type of a file stream? Create a variable of that type with the file's name in braces, and right after that, before you read the first number, ask it for `fail()`. What should the program print then, and should it go on?

</details>

<details>
<summary>Hint 2: reading and checking</summary>

For every required number the order is the same as in section 2: first the read with `>>`, then `fail()`, only then the range. The number of sessions is a required number too. You read as many page counts as the number of sessions announces, in the loop of lesson 10.3.

</details>

<details>
<summary>Hint 3: the working directory and the report</summary>

`pages.txt` must be in the configuration's working directory, not next to the executable. Check the field **Working directory** of the new project just as in section 4. Print the report after the loop: the program gets there only when no `return 0;` in the loop has run.

</details>

An example solution is in the section [Example solutions](#example-solutions).

## 9. When something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `Cannot open steps.txt`, although the file exists | The file isn't in the working directory, or it has a different name. | Follow the steps of section 7: the name, the case of letters, **Working directory**, the file's location. |
| There's a file `steps.txt.txt` in the folder, or `steps.txt` has no `.txt` extension | The editor added an extension, or the file was saved under another name. Windows hides known extensions by default. | Check the name in the terminal with `ls` and change it to exactly `steps.txt`. |
| `Input error` for data that looks valid | The file was saved as a document, for example in RTF format, not as plain text, or there's a letter where a number should be, for example `O` instead of `0`. | Create the file in CLion (**New \| File**) or in an editor that saves plain text, and type the data again. |
| A report with other numbers than you expect | The program reads a different `steps.txt` from the one you're editing, for example a copy in another folder. | Check **Working directory** and open the file from precisely that folder. |
| The program prints nothing and waits | The program reads from `std::cin` instead of the file stream. | Check that every read uses the file stream's variable, for example `input >> days;`. |

## 10. Explain

Answer in your own words, ideally in writing. Only then compare with the example answers.

1. What is the header `<fstream>` for, and what does the line `std::ifstream input{"steps.txt"};` do?
2. What does the name `steps.txt` without any folder mean? From which folder does the program start looking for it?
3. How does the program know which folder to look in when you run it in CLion, and how when you run it from the terminal?
4. How is `Cannot open steps.txt` different from `Input error`? Give one situation in which each of them appears.
5. Why does an empty file give a different result from a file holding `0`? What would happen if the program didn't check reading the number of days?
6. The program is correct, so is the file, and the program prints `Cannot open steps.txt`. How is that possible? What will you check first?
7. Does `steps.txt` belong in the list of files in `add_executable`? What do you have to do after changing `steps.txt`, and what after changing `main.cpp`?
8. Does a missing line end after the last number always mean a failed read?
9. Why isn't changing the working directory the same as changing the build folder?
10. What doesn't the program of this lesson check? Give two files for which it prints a valid report although they don't look like the one in section 1.

<details>
<summary>Example answers</summary>

1. `<fstream>` includes the file streams. The line creates a variable `input` of type `std::ifstream`, an input file stream, and at once tries to open the file `steps.txt` for reading. It doesn't read data yet: the later `input >> ...` do that.
2. It's a relative path: just the file's name. The program looks for it in its working directory, the current folder of the running program.
3. In CLion the working directory is set by the field **Working directory** of the run configuration. In the terminal it's the shell's current folder from which you start the program. The code itself doesn't set it.
4. `Cannot open steps.txt`: the program couldn't open the file, for example because the file isn't in the working directory. `Input error`: the file opened, but a required number couldn't be read, for example because the file is empty or there's the word `seven` where a number should be.
5. A file with `0` says that there were zero days, so the report `Days: 0` is valid. An empty file says nothing, so reading the number of days fails and the program prints `Input error`. Without the check of the read, `days` would stay 0, and the program would print the same report for an empty file as for a file with `0`, presenting missing data as a result.
6. The program looks for the file in its working directory, and the file is somewhere else or has a slightly different name. First I check the name and the case of letters, then the field **Working directory**, and whether the file is precisely in that folder.
7. No. `add_executable` lists the source files that the compiler translates into the program, and `steps.txt` holds data that the program reads while it runs. After changing `steps.txt` it's enough to run the program again. After changing `main.cpp` you have to build it again, which **Run** in CLion does by itself.
8. No. If the last number is complete, `>>` reads it correctly, even when the data ends right after it, and `fail()` gives `false`. An error appears when a required number is missing or isn't a number.
9. The build folder is where the tools save the built program. The working directory is the place from which the running program counts relative paths. Changing the working directory doesn't move or build the program, and the executable can be in a different folder from the one where it looks for data.
10. The program doesn't check the file's lines, or the data after the required numbers. It prints a valid report, for example, for `2 4200 7350` on one line, for a file with empty lines between the numbers, and for a file in which one more number or a word follows the required numbers.

</details>

## Summary

- Data that a program should read on every run can be kept in an ordinary text file. A data file isn't a source file and doesn't go into `add_executable`.
- `#include <fstream>` gives you file streams. `std::ifstream input{"steps.txt"};` creates a stream and tries to open the file for reading.
- You read from a file just as from the keyboard: with `>>`. You check whether opening and every read worked with `fail()`.
- The order of the checks: opening, reading a value, its range, only then the next value. The report is created after all the required values are read.
- A missing file (`Cannot open`), an empty file (`Input error`) and a file with a zero (a report) are three different situations.
- A relative path counts from the program's working directory. In CLion it's set by the field **Working directory**, and in the terminal it's the shell's current folder. It isn't automatically the folder of `main.cpp` or the folder of the executable.
- When a correct program doesn't find a correct file, you check the name, the case of letters, the working directory and the file's location, not the code.

## What's next

The program of this lesson reads only numbers from a file. In [lesson 12.2: Records from a file: the same reading function](lesson_02_records_from_a_file.en.md), you'll read records from a file, with the same reading function as from the keyboard.

---

## Example solutions

Look here **after your own attempt**. Your variable names may differ, as long as the standard output is as required.

<details>
<summary>Section 8: the mission, pages read in a session</summary>

**`main.cpp`**:

<!-- example: pages -->
```cpp
#include <fstream>
#include <iostream>

int main() {
    std::ifstream reading_log{"pages.txt"};

    if (reading_log.fail()) {
        std::cout << "Cannot open pages.txt\n";
        return 0;
    }

    int sessions{0};
    reading_log >> sessions;

    if (reading_log.fail()) {
        std::cout << "Input error\n";
        return 0;
    }

    if (sessions < 0 || sessions > 5) {
        std::cout << "Invalid pages\n";
        return 0;
    }

    int total_pages{0};

    for (int session{0}; session < sessions; ++session) {
        int pages{0};
        reading_log >> pages;

        if (reading_log.fail()) {
            std::cout << "Input error\n";
            return 0;
        }

        if (pages < 0 || pages > 500) {
            std::cout << "Invalid pages\n";
            return 0;
        }

        total_pages += pages;
    }

    std::cout << "Sessions: " << sessions << "\n";
    std::cout << "Total pages: " << total_pages << "\n";
}
```

**`CMakeLists.txt`**: the one of the original `lesson_05_first_program`, unchanged. `pages.txt` isn't in `add_executable`.

**`pages.txt`** with data A, in the folder `reading_pages`, next to `main.cpp` and `CMakeLists.txt`:

<!-- run: pages -->

<!-- datafile: pages pages.txt -->
```text
3
12
0
25
```

<!-- output: pages -->
```text
Sessions: 3
Total pages: 37
```

- **The run configuration:** the field **Working directory** of the configuration `first_program` points to the folder `reading_pages`, the one with `pages.txt`. In the terminal you start the program from the folder `reading_pages`.
- **The order of the checks:** first `reading_log.fail()` right after opening, then for the number of sessions and every page count: the read, `fail()`, the range. Every error ends `main` with `return 0;`, so the report after the loop is printed only for complete, valid data.
- **An empty file and zero sessions:** for an empty file, reading the number of sessions fails (`Input error`). For a file with `0` the read works, the loop doesn't run once, and the report gives zero sessions and zero pages.
- **Other correct solutions:** another name for the stream, for example `input` or `pages_file`; the ranges written as `const int` constants; a `while` loop with a counter instead of `for`.

| Case | The file `pages.txt` | Standard output |
|---|---|---|
| A | `3`, `12`, `0`, `25` | `Sessions: 3`, `Total pages: 37` |
| B | `0` | `Sessions: 0`, `Total pages: 0` |
| C | no file | `Cannot open pages.txt` |
| D | an empty file | `Input error` |
| E | `2`, `15`, `-1` | `Invalid pages` |
| F | `2`, `15`, `seven` | `Input error` |
| G | `2`, `15` | `Input error` |

The other check cases, checked automatically:

**H: one session.**

<!-- run: pages -->

<!-- datafile: pages pages.txt -->
```text
1
40
```

<!-- output: pages -->
```text
Sessions: 1
Total pages: 40
```

**I: five sessions.**

<!-- run: pages -->

<!-- datafile: pages pages.txt -->
```text
5
10
20
30
40
50
```

<!-- output: pages -->
```text
Sessions: 5
Total pages: 150
```

**J: 500 pages in one session,** the upper limit.

<!-- run: pages -->

<!-- datafile: pages pages.txt -->
```text
1
500
```

<!-- output: pages -->
```text
Sessions: 1
Total pages: 500
```

**K: 501 pages,** one too many.

<!-- run: pages -->

<!-- datafile: pages pages.txt -->
```text
1
501
```

<!-- output: pages -->
```text
Invalid pages
```

**L: a negative number of sessions.**

<!-- run: pages -->

<!-- datafile: pages pages.txt -->
```text
-2
```

<!-- output: pages -->
```text
Invalid pages
```

**M: data A without a line end after the last number.**

<!-- run: pages -->

<!-- datafile: pages pages.txt noeol -->
```text
3
12
0
25
```

<!-- output: pages -->
```text
Sessions: 3
Total pages: 37
```

**N: the largest possible total,** five sessions of 500 pages.

<!-- run: pages -->

<!-- datafile: pages pages.txt -->
```text
5
500
500
500
500
500
```

<!-- output: pages -->
```text
Sessions: 5
Total pages: 2500
```

**O: six sessions.**

<!-- run: pages -->

<!-- datafile: pages pages.txt -->
```text
6
10
10
10
10
10
10
```

<!-- output: pages -->
```text
Invalid pages
```

</details>

**Previous lesson:** [Lesson 11.5: Building a multi-file program (the Module 11 test)](../module_11_multifile_programs/lesson_05_multifile_checkpoint.en.md) · **Next lesson:** [Lesson 12.2: Records from a file: the same reading function](lesson_02_records_from_a_file.en.md) · [Course overview](../../README.en.md)

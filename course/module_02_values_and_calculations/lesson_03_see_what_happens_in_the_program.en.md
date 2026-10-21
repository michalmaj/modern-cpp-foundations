# Lesson 2.3: See what happens in the program

[Polski](lesson_03_see_what_happens_in_the_program.md) · **English** · [Course overview](../../README.en.md)

> **Module 2, lesson 3** · about 60 minutes
> **You need:** the `cpp-workspace` folder, the original `lesson_05_first_program` project, and CLion with the `LLVM 22` toolchain from lesson 0.5.
> **Pilot version.** The programs in this lesson are checked automatically on Windows, Ubuntu and macOS. The debugger steps were prepared from the CLion 2026.2 documentation, but they haven't yet been checked by hand on every configuration. If the debugger doesn't work in your environment, you can trace the values with the `std::cout` method from section 8 and still complete this lesson.

## Before you start

This lesson assumes that after lesson 2.2:

- you understand that the assignment `total = total + 4;` first calculates the right-hand side and then replaces the variable's old value;
- you can fill in a table of variable values after a sequence of statements;
- you can add `std::cout` lines to check a value after every step;
- you open a project in CLion and build it in the **Debug** profile, as in lesson 0.5.

## The situation

A program that builds and runs doesn't have to work correctly. Sometimes the compiler reports nothing, and the result is still wrong. You then know **that** something is wrong, but not **where**. Today you'll meet the **debugger**: a tool that stops a program at a chosen place, shows the values of its variables, and then lets you run it one statement at a time. You'll compare your prediction with what the program really does.

After this lesson you will:

- explain what a debugger is for and what a breakpoint is;
- tell an ordinary run (**Run**) apart from a run under the debugger (**Debug**);
- understand why debugging needs the Debug configuration;
- stop a program before a chosen statement and read the values of its variables;
- run a program step by step with **Step Over**, and watch values change;
- find the first statement after which the program's state differs from your prediction;
- fix a logic error and check the result;
- look for such an error without a debugger too, by printing values.

## 1. Prepare the project

In `cpp-workspace`, create a folder `lesson_2_3` and copy `main.cpp` and `CMakeLists.txt` into it from the original `lesson_05_first_program`.

This time you'll use the debugger, so open this folder in CLion, as in lesson 1.1: **File | Open**, select `cpp-workspace/lesson_2_3`, choose **This Window**, then **Trust Project**, and in the **CMake Profiles** window confirm the **Debug** profile (**OK**).

## 2. Predict first: a receipt

The till in a small shop adds up a receipt. A customer buys bread for 4, milk for 6 and cheese for 7, and at the end hands in a discount coupon worth 2. Someone wrote a program for this. Replace the contents of `main.cpp` with this code, but **don't run it yet**:

<!-- example: receipt_bug -->
```cpp
#include <iostream>

int main() {
    const int bread_price{4};
    const int milk_price{6};
    const int cheese_price{7};
    const int coupon{2};
    int total{0};

    total = total + bread_price;
    total = total + milk_price;
    total = cheese_price;
    total = total - coupon;

    std::cout << "To pay: " << total << "\n";
}
```

Read the code. Copy the table and write in it what `total` **should** be after each statement, for the receipt to be added up correctly:

| Statement | Expected `total` after it runs |
|---|---|
| `int total{0};` | 0 |
| `total = total + bread_price;` | |
| `total = total + milk_price;` | |
| `total = cheese_price;` | |
| `total = total - coupon;` | |

If something already looks suspicious, write it down. You'll check it in a moment.

Now build and run the program (**Run**). Compare the output with the last row of the table.

<details>
<summary>The program's output</summary>

<!-- output: receipt_bug -->
```text
To pay: 5
```

</details>

The program built, the compiler reported nothing, and yet the result doesn't match the receipt. This is a **logic error**: the program does something other than what it was meant to do. The final result only tells you **that** something is wrong. Any of the four statements could be to blame.

**At which moment did the value of `total` become wrong?**

You'll find the answer with the debugger.

## 3. The debugger, breakpoints and the Debug configuration

A **debugger** is a tool that runs your program under its control. It can stop the program, show the current values of its variables, and then continue, one statement at a time.

- **Run** starts the program the ordinary way: it runs from start to finish without stopping.
- **Debug** starts the program under the debugger. The program will stop at the places you mark.
- A **breakpoint** is a marker next to a statement that says: "stop **before** you execute this statement".

**Why the Debug configuration?** In lesson 0.5 you build the program in the CMake **Debug** profile. In this configuration the compiler adds extra **information for the debugger** to the program: which part of the compiled program belongs to which line of code, and where the variables are. Without it, the debugger doesn't know where your statement is. The **Release** configuration is prepared for running fast: the compiler may reorder and combine statements in it, and by default it doesn't add this information. So always use the Debug profile when looking for errors.

## 4. Check the settings before your first session

**1. The right project.** At the top of the CLion window, check that the open project is the one from the `lesson_2_3` folder, and that the editor shows the `main.cpp` with the receipt.

**2. The CMake Debug profile.** Open the **CMake** window and check two things, as in lesson 0.5, section 5: the compiler is `Clang 22` (or newer), and the command at the very top contains `-DCMAKE_BUILD_TYPE=Debug`.

**3. The debug profile.** Watch out for two similar names:

- the **CMake Debug profile** (from lesson 0.5) says **how to build** the program;
- the **debug profile** says **which debugger** traces it.

In the main toolbar, next to the choice of program to run, there is a switcher labelled `Debug | <profile name>`. It shows the debug profile CLion will use for the next session. You'll find all profiles in the settings (on Windows and Ubuntu **File | Settings**, on macOS **CLion | Settings**): **Build, Execution, Deployment | Debugger | Debug Profiles**.

### Ubuntu

CLion prepares a default profile with the bundled **GDB** debugger by itself. Don't change anything.

### macOS

CLion prepares a default profile with the bundled **LLDB** debugger by itself. Don't change anything.

### Windows

On Windows, `clang++` writes the information for the debugger in Microsoft's format (in a `.pdb` file). CLion has a bundled debugger for it, based on **LLDB** and made for the Visual Studio toolchain. So you need a profile of type **LLDB**, not GDB. The surest way is to create such a profile yourself and give it your own name. Then you know what type it is:

1. In the settings, open **Build, Execution, Deployment | Debugger | Debug Profiles**.
2. Under **General-purpose debuggers**, click the **LLDB** tile. CLion adds a new profile of that type to the list.
3. In the **Name** field, type for example `LLDB Visual Studio`. The **Executable** field isn't available for LLDB on Windows: CLion uses its bundled LLDB.
4. Tick **Available for all projects**, so that this profile is available in your next projects too.
5. Click **OK**.
6. In the switcher in the toolbar, choose `Debug | LLDB Visual Studio`.

The toolchain settings (**Toolchains**) also have an older **Debugger** field. In CLion 2026.2 this setting is deprecated: the debug profile decides which debugger a session uses. Don't change it.

**If you used the System toolchain instead of Visual Studio in lesson 0.5,** we have no confirmation that the debugger works in that configuration. Try the steps in section 5. If the program doesn't stop, don't change the toolchain: go to section 8 instead.

## 5. Your first debugger session

**Step 1. Set a breakpoint.** Find the statement `total = total + bread_price;` in the editor. Click in the editor's left margin (the strip with the line numbers) next to it. A breakpoint marker appears there. Clicking it again removes it.

Always set a breakpoint on a line with a statement, not on an empty line or on `}`. Here the chosen statement comes after all the declarations, so every variable already has its starting value.

**Step 2. Start under the debugger.** Click the **Debug** button in the top toolbar, or choose **Run | Debug '…'** from the menu (the program's name is in the quotes). Don't click **Run**: in an ordinary run the program won't stop. CLion builds the program if needed, starts it under the debugger, and stops at the breakpoint. You control the session in the **Debug** window at the bottom of the screen. If you can't see it, open it with **View | Tool Windows | Debug**.

**Step 3. Understand the blue line.** This is the most important thing in this lesson.

> The line with the breakpoint is now highlighted in blue. This is the **current execution point**: the statement that will run **next**. The program stopped **before** it. **This statement hasn't run yet.**

**Step 4. Read the value.** In the **Debug** window, open the **Variables** tab and find `total` in it. Predict first: what is the value of `total` right now? Only then look.

<details>
<summary>What you should see, and why</summary>

`total` has the value **0**, even though the blue statement adds the price of bread. Nothing is broken: that statement hasn't run yet. Only what stands above it has run, and there `total` got its starting value 0.

</details>

The **Variables** tab may show other variables too, for example the prices. Today you watch only `total`. CLion may also show variable values in the editor itself, next to the code.

**Step 5. Run one statement.** On the toolbar of the **Debug** window, find the **Step Over** button (its name appears when you hover the mouse pointer over it). Click it **once**. The blue statement runs, and the blue line moves to the next statement. Check `total` in the **Variables** tab: now you see the value **after** the statement ran.

**Step 6. Step by step, up to the first difference.** Copy this table. In the "expected" column, write the values from the table in section 2. Before each click on **Step Over**, write down what `total` is **now**, and after the click write down the new value.

| Statement in blue (not run yet) | `total` now | Expected `total` after it runs | `total` after **Step Over** |
|---|---|---|---|
| `total = total + bread_price;` | | | |
| `total = total + milk_price;` | | | |
| `total = cheese_price;` | | | |
| `total = total - coupon;` | | | |

The "after" value of one row is the "now" value of the next. You are looking for the **first** row where the last column differs from the expected one. The statement in that row was the first to give a wrong result.

**Step 7. End the session.** When the blue line reaches the statement with `std::cout`, stop clicking **Step Over**. Click **Resume Program** (the button on the toolbar of the **Debug** window, or the menu **Run | Debugging Actions | Resume Program**). The program runs the rest of its statements without stopping, because there are no more breakpoints, and finishes. If you want to end the session earlier, click **Stop** on the toolbar of the **Debug** window.

Don't click **Step Over** past the last statement of the program. The debugger could then move into code that starts and ends programs and doesn't come from your file. If you see an unfamiliar file or code you didn't write, click **Stop**.

The filled-in table and an explanation are in [Example solutions](#example-solutions). Look there after your own attempt.

## 6. Fix and check

Once you know which statement was to blame, fix it. Recall from lesson 2.2 that an assignment **replaces** the variable's old value. What was this statement supposed to do with the total so far?

After the fix, run the program the ordinary way (**Run**). The output must be:

<!-- output: receipt_fixed -->
```text
To pay: 15
```

<details>
<summary>The fixed program</summary>

<!-- example: receipt_fixed -->
```cpp
#include <iostream>

int main() {
    const int bread_price{4};
    const int milk_price{6};
    const int cheese_price{7};
    const int coupon{2};
    int total{0};

    total = total + bread_price;
    total = total + milk_price;
    total = total + cheese_price;
    total = total - coupon;

    std::cout << "To pay: " << total << "\n";
}
```

</details>

If you like, run the fixed program under the debugger again, with the same breakpoint. After the third **Step Over**, `total` is now 17, as in the table in section 2.

## 7. What the debugger gave you

The output `To pay: 5` only said that something was wrong. The debugger let you stop the program before the suspicious statements, see the value **before** and **after** each of them, and compare it with your prediction. The first difference pointed to one specific statement. And you didn't have to change the code to do it.

The debugger doesn't fix the program: it shows what the program does. Deciding what to fix is up to you.

## 8. When the debugger doesn't work: tracing with `std::cout`

This method helps if, in your environment:

- a program started with **Debug** doesn't stop at the breakpoint;
- CLion marks the breakpoint as invalid;
- the **Variables** tab is empty;
- you can't choose the right debug profile.

You know it from lesson 2.2, section 5. Use it on the receipt program, in the version **with the error**:

1. Prepare the table of expected values from section 2.
2. Under every assignment to `total`, add a statement that prints the current value, for example:

<!-- fragment -->
```cpp
std::cout << "total: " << total << "\n";
```

3. Build and run the program (**Run**).
4. Compare each printed line `total: …` with the matching row of the table.
5. Find the first line that doesn't match. The assignment just above the added `std::cout` that printed it was the first to give a wrong result.
6. Remove the temporary `std::cout` statements you added.
7. Fix the wrong statement.
8. Run the program again and check that it prints `To pay: 15`.

<details>
<summary>The program with the added printing, and its output</summary>

<!-- example: receipt_trace -->
```cpp
#include <iostream>

int main() {
    const int bread_price{4};
    const int milk_price{6};
    const int cheese_price{7};
    const int coupon{2};
    int total{0};

    total = total + bread_price;
    std::cout << "total: " << total << "\n";
    total = total + milk_price;
    std::cout << "total: " << total << "\n";
    total = cheese_price;
    std::cout << "total: " << total << "\n";
    total = total - coupon;
    std::cout << "total: " << total << "\n";

    std::cout << "To pay: " << total << "\n";
}
```

<!-- output: receipt_trace -->
```text
total: 4
total: 10
total: 7
total: 5
To pay: 5
```

The third line is 7, where 17 was expected. So the third assignment, `total = cheese_price;`, gave the wrong result.

</details>

**How is this method different from the debugger?** Printing values lets you trace how values change, but it **isn't a full replacement** for the debugger:

- it **requires changing the code** you're examining: it's easy to make a new mistake that way, and the added lines must be removed afterwards;
- it **shows only what you choose** to print, while the debugger shows the values of all variables where the program stopped;
- it **doesn't stop the program**: you can't pause, look around and decide what to check next;
- it **doesn't teach you to use the debugger**, which you'll use in later lessons.

If you use this method because the debugger doesn't work in your environment, you can carry on with Module 2. You'll catch up on using the debugger later, once it works.

## 9. Mission: the school library

In a class library, 20 books stand on the shelf, and none are borrowed. During the day:

- in the morning, pupils borrow 6 books;
- at noon, they return 4 books;
- in the afternoon, they borrow 3 more.

The program must print how many books are on the shelf at the end of the day, and how many are borrowed. Someone wrote it, but the result is wrong.

In `cpp-workspace`, create a folder `school_library`, copy `CMakeLists.txt` and `main.cpp` into it from the original `lesson_05_first_program`, and replace the contents of `main.cpp` with this program. Open the folder in CLion.

<!-- example: library_bug -->
```cpp
#include <iostream>

int main() {
    const int morning_loans{6};
    const int returns{4};
    const int afternoon_loans{3};
    int on_shelf{20};
    int borrowed{0};

    on_shelf = on_shelf - morning_loans;
    borrowed = borrowed + morning_loans;
    on_shelf = on_shelf + returns;
    borrowed = borrowed + returns;
    on_shelf = on_shelf - afternoon_loans;
    borrowed = borrowed + afternoon_loans;

    std::cout << "On the shelf: " << on_shelf << "\n";
    std::cout << "Borrowed: " << borrowed << "\n";
}
```

This time the decisions are yours:

1. From the description of the day, **predict** and write in a table what `on_shelf` and `borrowed` should be after each statement.
2. Run the program (**Run**) and compare the output with the last row of the table.
3. Choose where to stop the program, and find the first statement after which a value differs from your prediction: with the debugger or with the `std::cout` method.
4. Fix the error and check the result.

<details>
<summary>The output of the program with the error</summary>

<!-- output: library_bug -->
```text
On the shelf: 15
Borrowed: 13
```

</details>

### Success criteria

- The table of predicted values of both variables after each statement is filled in **before** you look for the error.
- You know which statement was the first to give a wrong result, and what value the variable had right after it.
- The fix changes only that one statement.
- After the fix, the program builds as C++20 and prints a result that matches the description of the day. Check it only after your own prediction:

<details>
<summary>The expected output after the fix</summary>

<!-- output: library_fixed -->
```text
On the shelf: 15
Borrowed: 5
```

</details>

- You can explain why that statement gave a wrong result.

Once the output matches, you can save the project in Git, as in lesson 1.5.

<details>
<summary>Hint 1</summary>

Which variable has a wrong value at the end? You can set the breakpoint at the first statement that changes it, or simply at the first assignment.

</details>

<details>
<summary>Hint 2</summary>

The books on the shelf and the borrowed books always add up to 20. You can check this after each statement that belongs to one event.

</details>

### Self-assessment

Mark what fits your work:

- I found the error with the **debugger**.
- I found the error by **printing values** with `std::cout`.
- I needed the **hints** or the **example solution** to find the error.

Each of these is fine. If the debugger wasn't available, using it stays for you to catch up on later. If you needed the solution, come back to the mission in a few days and try again.

## 10. When something goes differently

| What you see | What it means | What to do |
|---|---|---|
| The program runs to the end and doesn't stop | You started **Run** instead of **Debug**, or there is no breakpoint. | Set a breakpoint on a statement and start with **Debug**. |
| CLion marks the breakpoint as invalid, or a program started with **Debug** doesn't stop | The debugger can't match the breakpoint to the program: the line has no statement, the program isn't built in the Debug profile, or, on Windows, the active debug profile isn't of type LLDB. | Move the breakpoint to a statement. Check section 4. If that doesn't help, use the method from section 8. |
| At the first stop `total` is 0, not 4 | That's expected: the blue statement hasn't run yet. | Click **Step Over** and check the value again. |
| On Windows, the switcher shows a profile of type GDB | For the format in which `clang++` writes the information for the debugger on Windows, CLion provides its bundled LLDB. | Choose the LLDB profile you created in section 4. |
| After **Step Over**, an unfamiliar file or code you didn't write opens | The debugger went past the last statement of your program. | Click **Stop**. Next time, end the session with **Resume Program** when the blue line reaches `std::cout`. |
| The debugger shows code from another exercise | Another project is open in CLion. | Open the right folder (**File \| Open**). |
| After the fix, the result is still wrong | A different statement was fixed than the one to blame, or a new mistake crept in. | Go back to the table and find the first difference again. |

## 11. Explain

Answer in your own words, preferably in writing. Only then compare with the example answer.

**1.** How is starting a program with **Run** different from starting it with **Debug**?

<details>
<summary>Example answer</summary>

**Run** executes the program from start to finish without stopping. **Debug** starts it under the debugger, which stops the program at breakpoints and lets you look at the values of variables and execute statements one after another.

</details>

**2.** What does the blue line in the editor mean during a debugging session? Has that statement already run?

<details>
<summary>Example answer</summary>

It is the current execution point: the statement that will run next. It hasn't run yet. Its effect is visible only after **Step Over**.

</details>

**3.** Why did `total` have the value 0 at the first stop, even though the breakpoint was on the statement that adds the price of bread?

<details>
<summary>Example answer</summary>

Because the program stops **before** the statement with the breakpoint. At that moment only the initialisation `int total{0};` had run.

</details>

**4.** Why wasn't the output `To pay: 5` alone enough to point to the wrong statement?

<details>
<summary>Example answer</summary>

The final result shows only the combined effect of all the statements. Any of them could have been to blame. Only comparing the value after each statement with the prediction pointed to the first one that gave a wrong result.

</details>

**5.** Give two differences between finding an error with the debugger and printing values with `std::cout`.

<details>
<summary>Example answer</summary>

For example: printing requires changing the code, and the debugger doesn't. Printing shows only the values you chose, while the debugger shows all the variables where the program stopped. The debugger lets you pause the program, and printing doesn't.

</details>

## Summary

- A **logic error** is when a program builds and runs, but does something other than what it was meant to do. The compiler won't report it.
- A **debugger** runs a program under its control: it stops it, shows the values of variables, and lets you execute statements one after another.
- A **breakpoint** stops the program **before** the marked statement runs.
- Debugging needs a program built in the **Debug** configuration. The debug profile chooses which debugger CLion traces it with.
- The **blue line** is the statement that will run next. Its effect is visible after **Step Over**.
- You look for the **first** statement after which a value differs from the prediction. That's where the error is.
- Printing values with `std::cout` can also find that statement, but it requires changing the code and doesn't replace the debugger.

## What's next

You can now compare your prediction with what the program really does, and find the first wrong statement. **Lesson 2.4 is in preparation.**

---

## Example solutions

Look here **after your own attempt**.

<details>
<summary>Sections 2 and 5: the tables for the receipt</summary>

Expected values (section 2):

| Statement | Expected `total` after it runs |
|---|---|
| `int total{0};` | 0 |
| `total = total + bread_price;` | 4 |
| `total = total + milk_price;` | 10 |
| `total = cheese_price;` | 17 |
| `total = total - coupon;` | 15 |

The debugger session (section 5):

| Statement in blue (not run yet) | `total` now | Expected `total` after it runs | `total` after **Step Over** |
|---|---|---|---|
| `total = total + bread_price;` | 0 | 4 | 4 |
| `total = total + milk_price;` | 4 | 10 | 10 |
| `total = cheese_price;` | 10 | 17 | **7** |
| `total = total - coupon;` | 7 | 15 | 5 |

The first difference is in the third row: after `total = cheese_price;`, `total` is 7 instead of 17. This assignment **replaces** the total so far (10) with the price of cheese alone (7), instead of adding it. The last statement is correct: it subtracts the coupon, but from the wrong total, which is why the final result is 5. The correct statement is `total = total + cheese_price;`.

</details>

<details>
<summary>Section 9: mission, the school library</summary>

| Statement | `on_shelf` | `borrowed` |
|---|---|---|
| `int on_shelf{20};` and `int borrowed{0};` | 20 | 0 |
| `on_shelf = on_shelf - morning_loans;` | 14 | 0 |
| `borrowed = borrowed + morning_loans;` | 14 | 6 |
| `on_shelf = on_shelf + returns;` | 18 | 6 |
| `borrowed = borrowed + returns;` | 18 | expected 2, the program gives **10** |
| `on_shelf = on_shelf - afternoon_loans;` | 15 | expected 2, the program gives 10 |
| `borrowed = borrowed + afternoon_loans;` | 15 | expected 5, the program gives 13 |

The first difference appears after `borrowed = borrowed + returns;`: `borrowed` is 10 instead of 2. Returned books go back to the shelf, so the number of borrowed books must **decrease**, but the program increases it. At that point the shelf and the readers hold 28 books together, not 20. The fixed program:

<!-- example: library_fixed -->
```cpp
#include <iostream>

int main() {
    const int morning_loans{6};
    const int returns{4};
    const int afternoon_loans{3};
    int on_shelf{20};
    int borrowed{0};

    on_shelf = on_shelf - morning_loans;
    borrowed = borrowed + morning_loans;
    on_shelf = on_shelf + returns;
    borrowed = borrowed - returns;
    on_shelf = on_shelf - afternoon_loans;
    borrowed = borrowed + afternoon_loans;

    std::cout << "On the shelf: " << on_shelf << "\n";
    std::cout << "Borrowed: " << borrowed << "\n";
}
```

Its output is the one in the success criteria: `On the shelf: 15` and `Borrowed: 5`.

</details>

**Previous lesson:** [Lesson 2.2: When values change](lesson_02_when_values_change.en.md) · **Next lesson:** in preparation · [Course overview](../../README.en.md)

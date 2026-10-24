# Lesson 5.1: Your first function (`void`)

[Polski](lesson_01_the_first_function.md) · **English** · [Course overview](../../README.en.md)

> **Module 5, lesson 1** · about 60–75 minutes
> **You need:** the `cpp-workspace` folder and the original `lesson_05_first_program` project, as before. You don't need the debugger in this lesson.
> **Pilot version.** The programs in this lesson are checked automatically on Windows, Ubuntu and macOS, including with the given input data. Typing input into CLion's **Run** window is described without a manual check on every system.

## Before you start

This lesson assumes that after Module 4 you:

- write programs with `if`/`else` and with `while` and `for` loops;
- check the range of the data before the program starts working;
- know that `main` is a function, where the program starts running (lesson 1.3);
- read compiler messages and fix compile errors (lesson 1.2).

## The situation

Your programs already do a lot, but each one is a single long `main`. When the same piece has to run in several places of a program, you have to write it several times. In this lesson you'll meet a way to **name** such a piece, write it **once** and run it wherever it's needed: **your own function**.

After this lesson you will:

- explain why a piece of code is moved into a function;
- point out, in a function, `void`, its name, the empty parentheses and its body;
- tell a function's definition from its call;
- predict the order in which a program with a function runs, also when the function isn't called or is called several times;
- find a call that is one too many;
- write your own `void` function and decide where to call it in a program with a loop.

## 1. Prepare the project

In `cpp-workspace`, create a `lesson_5_1` folder and copy `main.cpp` and `CMakeLists.txt` into it from the original `lesson_05_first_program`. You type the programs from sections 2–9 into that folder's `main.cpp`.

## 2. The same piece in two places

In a workshop class, the instructor reminds everyone of the safety rules twice: at the morning briefing and at the afternoon briefing. You know everything in this program:

<!-- example: briefing_repeated -->
```cpp
#include <iostream>

int main() {
    std::cout << "Morning briefing\n";
    std::cout << "Wear safety glasses\n";
    std::cout << "Keep tools organised\n";

    std::cout << "Afternoon briefing\n";
    std::cout << "Wear safety glasses\n";
    std::cout << "Keep tools organised\n";
}
```

<!-- output: briefing_repeated -->
```text
Morning briefing
Wear safety glasses
Keep tools organised
Afternoon briefing
Wear safety glasses
Keep tools organised
```

The program works correctly. But think about it and write down short answers:

1. What has to change in the code if one rule is updated?
2. How many places do you then have to check?
3. What happens if you change only one copy?
4. Do these two statements share a job that could be given a name?

<details>
<summary>Discussion</summary>

The rules are written twice, so every change has to be made in two places. If you change only one copy, the program still builds and runs, but it gives **different** rules in the morning and in the afternoon. Nobody notices straight away, because the compiler has nothing to report here: repeated code is valid C++. It's a problem for readability and for later changes, not an error in the language.

Both statements share one job: **showing the workshop rules**. Such a job can be given a name and written in one place.

</details>

## 3. Your first function

Here are the workshop rules written as a function:

<!-- fragment -->
```cpp
void show_workshop_rules() {
    std::cout << "Wear safety glasses\n";
    std::cout << "Keep tools organised\n";
}
```

This is a **function definition**: a description of what the function does. Its parts:

| Part | In the code | Meaning |
|---|---|---|
| **Result type** | `void` | The function doesn't pass any result back to the place where it was called. That doesn't mean it does nothing: this function prints two lines. |
| **Name** | `show_workshop_rules` | Describes the function's job. We write it like variable names: lower-case letters, with words joined by `_`. |
| **Parentheses** | `()` | Empty: this function doesn't need any data from outside. You'll see what can go in them in the next lesson. |
| **Body** | the statements between `{` and `}` | What the function does when it's called. |

You write the definition **outside** `main`, before it, as in the next section.

## 4. Calling the function from `main`

This program does the same as the program in section 2:

<!-- example: briefing_function -->
```cpp
#include <iostream>

void show_workshop_rules() {
    std::cout << "Wear safety glasses\n";
    std::cout << "Keep tools organised\n";
}

int main() {
    std::cout << "Morning briefing\n";
    show_workshop_rules();

    std::cout << "Afternoon briefing\n";
    show_workshop_rules();
}
```

<!-- output: briefing_function -->
```text
Morning briefing
Wear safety glasses
Keep tools organised
Afternoon briefing
Wear safety glasses
Keep tools organised
```

The standard output is identical to section 2. What changed is how it's written: the rules appear in the code **once**.

- **`show_workshop_rules();`** is a **function call**: the name, empty parentheses and a semicolon. A call says: "run this function's statements now".
- **`main` is a function too** (lesson 1.3), but it has a special role: the program starts running from it. The program doesn't start with `show_workshop_rules`, even though that function stands higher up in the file. You've known the word `int` before `main` since the start of the course. It's also a special part of `main`, which we'll come back to when you meet functions that pass back a result.
- You call your own function the same way as the `std::getline(…)` you already know: by its name and parentheses. In `std::getline`'s parentheses stood the data to read. The parentheses of `show_workshop_rules()` are empty.

## 5. The order of execution

The program in section 4 runs in this order:

| Step | Where the program is | What happens | On the screen |
|---|---|---|---|
| 1 | `main` | the program starts | |
| 2 | `main` | printing | `Morning briefing` |
| 3 | `main` | the first call of `show_workshop_rules()`: going into the function | |
| 4 | function | the first statement of the body | `Wear safety glasses` |
| 5 | function | the second statement of the body | `Keep tools organised` |
| 6 | `main` | the end of the function's body: back to just after the call | |
| 7 | `main` | printing | `Afternoon briefing` |
| 8 | `main` | the second call of the same function | |
| 9 | function | both statements of the body | `Wear safety glasses`, `Keep tools organised` |
| 10 | `main` | back to just after the second call, the end of `main`: the program ends | |

The program doesn't paste the function's contents into `main`. At a call it **goes into** the function, runs its statements from top to bottom, and **comes back** to just after the call.

**Predict.** How many times will the statements inside the function run if you call it twice? And how many lines will this program print, with three calls?

<!-- example: briefing_three_calls -->
```cpp
#include <iostream>

void show_workshop_rules() {
    std::cout << "Wear safety glasses\n";
    std::cout << "Keep tools organised\n";
}

int main() {
    std::cout << "Morning briefing\n";
    show_workshop_rules();

    std::cout << "Afternoon briefing\n";
    show_workshop_rules();

    std::cout << "Evening briefing\n";
    show_workshop_rules();
}
```

<details>
<summary>Answer and standard output for three calls</summary>

The function's body runs once for each call. With two calls, both statements of the body run twice; with three, three times. This program prints 9 lines: 3 briefing names and 3 × 2 lines of rules.

<!-- output: briefing_three_calls -->
```text
Morning briefing
Wear safety glasses
Keep tools organised
Afternoon briefing
Wear safety glasses
Keep tools organised
Evening briefing
Wear safety glasses
Keep tools organised
```

</details>

## 6. A definition isn't a call

In this program the function is defined, but `main` doesn't call it:

<!-- example: rules_not_called -->
```cpp
#include <iostream>

void show_workshop_rules() {
    std::cout << "Wear safety glasses\n";
    std::cout << "Keep tools organised\n";
}

int main() {
    std::cout << "Morning briefing\n";
    std::cout << "Afternoon briefing\n";
}
```

**Predict** what the program will print. Write your answer down, then run it.

<details>
<summary>Standard output and explanation</summary>

<!-- output: rules_not_called -->
```text
Morning briefing
Afternoon briefing
```

The rules didn't appear. **Writing a function's definition doesn't run its statements.** The program starts with `main` and runs only what `main` tells it to. The function stands higher up in the file, but without a call its body doesn't run.

</details>

Now add **one** call, right after `Morning briefing`. Predict the result and run the program:

<!-- example: rules_called_once -->
```cpp
#include <iostream>

void show_workshop_rules() {
    std::cout << "Wear safety glasses\n";
    std::cout << "Keep tools organised\n";
}

int main() {
    std::cout << "Morning briefing\n";
    show_workshop_rules();
    std::cout << "Afternoon briefing\n";
}
```

<details>
<summary>Standard output for one call</summary>

<!-- output: rules_called_once -->
```text
Morning briefing
Wear safety glasses
Keep tools organised
Afternoon briefing
```

</details>

Add a second call, right after `Afternoon briefing`. You get the program from section 4 and its result: the rules appear twice. **Zero calls, zero runs. One call, one run. Two calls, two runs.**

## 7. One change, every call

Go back to the program in section 4. The instructor changes the second rule to `Keep the floor clear`. Change **only one** line, in the function's body:

<!-- example: briefing_changed -->
```cpp
#include <iostream>

void show_workshop_rules() {
    std::cout << "Wear safety glasses\n";
    std::cout << "Keep the floor clear\n";
}

int main() {
    std::cout << "Morning briefing\n";
    show_workshop_rules();

    std::cout << "Afternoon briefing\n";
    show_workshop_rules();
}
```

**Predict** in how many places of the standard output the new text will appear. Then run the program.

<details>
<summary>Standard output after the change</summary>

<!-- output: briefing_changed -->
```text
Morning briefing
Wear safety glasses
Keep the floor clear
Afternoon briefing
Wear safety glasses
Keep the floor clear
```

The new text appears in both places, although one line was changed. Both calls run the same function body.

</details>

A function gives you **one place** where statements that run many times are written. That doesn't mean every line, or every repetition, must go into a separate function. A function makes sense when its statements share **a clear job** that can be given a name, like "show the workshop rules".

## 8. Find the bug: one call too many

The requirement: the program prints the workshop's plan for the day: `Session 1`, `Lunch`, `Session 2`, and at the end `See you tomorrow`. The rules appear **exactly twice: right after the name of each session**.

<!-- example: day_plan_bug -->
```cpp
#include <iostream>

void show_workshop_rules() {
    std::cout << "Wear safety glasses\n";
    std::cout << "Keep tools organised\n";
}

int main() {
    std::cout << "Session 1\n";
    show_workshop_rules();
    std::cout << "Lunch\n";
    show_workshop_rules();
    std::cout << "Session 2\n";
    show_workshop_rules();
    std::cout << "See you tomorrow\n";
}
```

1. Read the requirement and write down what the standard output **should** be.
2. **Predict** what **this** program will print.
3. Run it.
4. Compare how many times the rules appear, and where.
5. Find the call that is one too many.
6. Fix the program.
7. Run it again and check that the result matches the requirement.

The program's output before the fix, and the fixed program, are in [Example solutions](#example-solutions). Look there after your own attempt.

## 9. A function written below `main`

In this program the function's definition stands **after** `main`:

<!-- broken: rules_after_main at=5:5 errors=1 error=^use of undeclared identifier 'show_workshop_rules'$ -->
```cpp
#include <iostream>

int main() {
    std::cout << "Morning briefing\n";
    show_workshop_rules();
}

void show_workshop_rules() {
    std::cout << "Wear safety glasses\n";
    std::cout << "Keep tools organised\n";
}
```

**Predict** whether this program will build. Then try to build it and read the compiler's message.

<details>
<summary>What the compiler reports, and why</summary>

The program won't build. The compiler reports `use of undeclared identifier 'show_workshop_rules'` on line 5: it doesn't know that name. You know the same message from lessons 3.2 and 4.3, where it was about a variable.

The compiler reads the file from the top. When it reaches the call on line 5, it hasn't seen any function with that name yet. The definition stands further down, but at this point the compiler doesn't know about it yet.

</details>

**The fix:** move the whole definition of the function **before** `main`. For now, this course uses this pattern: **a function must be written in the file before you call it**. There are other ways to arrange functions in a file. You'll meet them later. The fixed program is in [Example solutions](#example-solutions).

## 10. Mission: breaks between rounds

The program lays out a training plan with breaks. The user gives the number of rounds. The program prints the rounds one after another, with a break **between** them.

**Requirements:**

- The program asks `Enter round count (0-5):` and reads a whole number. We assume the user types a whole number.
- For a number outside the range 0 to 5, the program prints only `Invalid round count` and doesn't start the plan. It doesn't ask again.
- For a valid number, it prints the rounds from 1 up to and including the given number, each as `Round N`.
- Between two consecutive rounds it prints a break, exactly these two lines:

  ```text
  Break: drink water
  Break: stretch
  ```

- There's no break before the first round and none after the last round.
- At the end of the plan it prints `Training complete`.
- The break is printed by **your own `void` function with no parameters**, defined before `main`. The break lines appear in the code only in that function. The round number is printed by code in `main`.
- Don't use variables declared outside functions.

In `cpp-workspace`, create a `round_breaks` folder, copy `CMakeLists.txt` into it from the original `lesson_05_first_program`, create an empty `main.cpp` and write the program on your own.

For 3 rounds the standard output must be as follows:

<!-- input: round_breaks -->
```text
3
```

<!-- output: round_breaks -->
```text
Enter round count (0-5):
Round 1
Break: drink water
Break: stretch
Round 2
Break: drink water
Break: stretch
Round 3
Training complete
```

**This isn't the workshop program with different text.** There, the function was called in two fixed places in `main`. Here, the number of rounds depends on the data, and the break must appear only in some places of the repetition. The function itself doesn't know which round is on. `main` decides **when** to call it. You have to decide on your own:

1. how to control the number of rounds;
2. where to print the current round;
3. what decides whether a round is followed by a break;
4. where to put the function call;
5. how to avoid a break after the last round;
6. what the program does for zero rounds.

**Before you write the program**, prepare a table of test cases: zero rounds, one round, two rounds, three rounds, the largest allowed number of rounds, and the values just outside the range on both sides. For each case, write down the expected standard output, also for 0 and 1, and the number of breaks.

**Then work in this order:**

1. Design where in the program, and under what condition, the function call stands.
2. Write the program.
3. Run it for 2 and 3 rounds and compare the results with your table.
4. Change one line of the break in the function for a moment. **Predict** in how many places of the result for 3 rounds the change will appear, and check.
5. Restore the required break text.
6. Check the remaining cases in your table: 0, 1, 5, -1 and 6.

### Success criteria

- The program builds as C++20, and its standard output for 3 rounds is exactly as shown above.
- For every number from 0 to 5, the program prints the right rounds, breaks only between rounds, and `Training complete`. For any other number it prints only the question and `Invalid round count`.
- The break is printed by your `void` function with no parameters, defined before `main`. The break lines appear in the code only once, in that function.
- The function doesn't print the round number. The program doesn't use variables declared outside functions.
- The table of cases was made before running the program.
- The same program handles every case, without changing the code.
- You can point out the function's definition and its call in your program, and explain why there's no break after the last round.

When the result matches, you can save the project in Git, as in lesson 1.5.

<details>
<summary>Hint 1</summary>

Which statements must always run together, whatever the round number?

</details>

<details>
<summary>Hint 2</summary>

How does the program recognise whether the current round will be followed by another one?

</details>

<details>
<summary>Hint 3</summary>

Think about whether the function should be called before the round is printed, after every round, or only after some rounds.

</details>

<details>
<summary>The full list of check cases: open it after preparing your own table</summary>

| Number of rounds | Standard output after the question | Breaks | What it checks |
|---|---|---|---|
| 3 | `Round 1`, a break, `Round 2`, a break, `Round 3`, `Training complete` | 2 | several rounds |
| 0 | `Training complete` | 0 | zero rounds |
| 1 | `Round 1`, `Training complete` | 0 | one round: no break after the last |
| 2 | `Round 1`, a break, `Round 2`, `Training complete` | 1 | the smallest number of rounds with a break |
| 5 | `Round 1` … `Round 5`, a break between every pair, `Training complete` | 4 | the largest allowed number |
| -1 | `Invalid round count` | 0 | just below the range |
| 6 | `Invalid round count` | 0 | just above the range |

Case 3 is checked above, with the mission's text.

<!-- input: round_breaks -->
```text
0
```

<!-- output: round_breaks -->
```text
Enter round count (0-5):
Training complete
```

<!-- input: round_breaks -->
```text
1
```

<!-- output: round_breaks -->
```text
Enter round count (0-5):
Round 1
Training complete
```

<!-- input: round_breaks -->
```text
2
```

<!-- output: round_breaks -->
```text
Enter round count (0-5):
Round 1
Break: drink water
Break: stretch
Round 2
Training complete
```

<!-- input: round_breaks -->
```text
5
```

<!-- output: round_breaks -->
```text
Enter round count (0-5):
Round 1
Break: drink water
Break: stretch
Round 2
Break: drink water
Break: stretch
Round 3
Break: drink water
Break: stretch
Round 4
Break: drink water
Break: stretch
Round 5
Training complete
```

<!-- input: round_breaks -->
```text
-1
```

<!-- output: round_breaks -->
```text
Enter round count (0-5):
Invalid round count
```

<!-- input: round_breaks -->
```text
6
```

<!-- output: round_breaks -->
```text
Enter round count (0-5):
Invalid round count
```

</details>

An example solution is in [Example solutions](#example-solutions).

## 11. When something goes differently

| What you see | What it means | What to do |
|---|---|---|
| `use of undeclared identifier` with your function's name | The call stands in the file before the function's definition, or the name in the call differs from the name in the definition. | Move the definition before `main`. Compare the names character by character. |
| A compile error at the function's definition | The definition stands inside `main`, between its braces. | Write the definition outside `main`, before it. Only the call stands in `main`. |
| The function's statements don't appear in the result | The function isn't called, or the call is missing its parentheses: for example `show_break;` doesn't call anything, and the compiler shows at most a warning. | A call is the name, `()` and a semicolon. |
| A break appears after the last round | The call runs in every iteration of the loop, with no condition. | Think about which rounds need a break after them (hint 2). |
| A break appears before the first round | The call stands before the round is printed and also runs in the first iteration. | Check the one-round case in your table. |
| The same lines appear once too often | There's an extra function call (section 8). | Count the calls and compare with the requirement. |
| The program does nothing and waits | It's waiting for a number, as in lesson 2.6. | Type a number and press **Enter**. |

## 12. Explain

Answer in your own words, preferably in writing. Only then compare with the example answers.

1. Why do we create our own function?
2. What does `void` mean?
3. Can a `void` function print text?
4. Why are the parentheses empty in this lesson's functions?
5. How does a function's definition differ from its call?
6. Will a function run on its own if it's defined before `main`?
7. What happens after the last statement of the function's body has run?
8. How many times will the statements of a function called three times run?
9. Why does changing a function's contents affect all its calls?
10. Why don't we call the function after the last round in the mission?
11. What happens in the mission for zero rounds?
12. Does every statement in a program have to go into its own function?

<details>
<summary>Example answers</summary>

1. To give a name to a piece of code with a shared job, write it once, and run it wherever it's needed. A change to that piece then needs a change in one place.
2. That the function doesn't pass any result back to the place of the call.
3. Yes. `void` only says that the function doesn't pass back a result. Its body can run any statements you know, for example `std::cout`.
4. Because these functions don't need any data from outside: they always do the same thing.
5. The definition describes what the function does: the result type, the name, the parentheses and the body. The call, the name with parentheses and a semicolon, tells the program to run those statements at that point.
6. No. The program starts with `main`, and a function's body runs only when the program reaches its call.
7. The program comes back to just after the call and runs the remaining statements of the function that called it, here `main`.
8. Three times: once for each call.
9. Because every call runs the same body, written in one place. There are no separate copies that would need changing.
10. Because the break must be **between** rounds. After the last round there's no next round, so no break is needed. A condition in `main` decides whether to call it, because the function itself doesn't know which round is on.
11. The rounds loop doesn't run at all, so no round and no break appear. The program prints only the question and `Training complete`.
12. No. A function makes sense when its statements share a clear job. Moving every line into a separate function doesn't improve a program.

</details>

## Summary

- **Your own function** is a named piece of code with one job. You write it once and run it wherever you call it.
- A `void` function's definition has the result type `void`, a name, parentheses and a body in braces: `void show_workshop_rules() { … }`.
- `void` means the function doesn't pass a result back to the place of the call. The function can still print text.
- Empty parentheses mean the function doesn't need any data from outside.
- **A definition isn't a call.** The function's body runs only when the program reaches the call `show_workshop_rules();`. Each call runs it once.
- After the body has run, the program comes back to just after the call.
- `main` is a function too: the program starts running from it.
- For now, a function's definition stands in the file before the place where it's called. Otherwise the compiler reports `use of undeclared identifier`.
- A change in the function's body changes the result of every call.
- The code that calls a function decides when to call it, for example with a condition in a loop in `main`.

## What's next

The functions in this lesson do exactly the same thing every time. In the next lesson you'll see how to pass data to a function, so that one function can work with different values: [Lesson 5.2: Parameters, arguments and passing by value](lesson_02_parameters_and_arguments.en.md).

---

## Example solutions

Look here **after your own attempt**. Your names may differ, as long as the standard output is as required.

<details>
<summary>Section 8: the output before the fix, and the fixed program</summary>

Before the fix:

<!-- output: day_plan_bug -->
```text
Session 1
Wear safety glasses
Keep tools organised
Lunch
Wear safety glasses
Keep tools organised
Session 2
Wear safety glasses
Keep tools organised
See you tomorrow
```

- **The rules appear three times**, and the requirement says: twice, right after the name of each session.
- **The cause:** the call after `Lunch` is one too many. The function itself is correct. The bug is in the **place of the call**.
- **The fix:** remove the call that stands after `Lunch`.

<!-- example: day_plan_fixed -->
```cpp
#include <iostream>

void show_workshop_rules() {
    std::cout << "Wear safety glasses\n";
    std::cout << "Keep tools organised\n";
}

int main() {
    std::cout << "Session 1\n";
    show_workshop_rules();
    std::cout << "Lunch\n";
    std::cout << "Session 2\n";
    show_workshop_rules();
    std::cout << "See you tomorrow\n";
}
```

<!-- output: day_plan_fixed -->
```text
Session 1
Wear safety glasses
Keep tools organised
Lunch
Session 2
Wear safety glasses
Keep tools organised
See you tomorrow
```

</details>

<details>
<summary>Section 9: the fixed program</summary>

The definition stands before `main`, so at the line of the call the compiler already knows the function:

<!-- example: rules_before_main -->
```cpp
#include <iostream>

void show_workshop_rules() {
    std::cout << "Wear safety glasses\n";
    std::cout << "Keep tools organised\n";
}

int main() {
    std::cout << "Morning briefing\n";
    show_workshop_rules();
}
```

<!-- output: rules_before_main -->
```text
Morning briefing
Wear safety glasses
Keep tools organised
```

</details>

<details>
<summary>Section 10: the mission, breaks between rounds</summary>

<!-- example: round_breaks -->
```cpp
#include <iostream>

void show_break() {
    std::cout << "Break: drink water\n";
    std::cout << "Break: stretch\n";
}

int main() {
    int round_count{0};

    std::cout << "Enter round count (0-5):\n";
    std::cin >> round_count;

    if (round_count >= 0 && round_count <= 5) {
        for (int round_number{1}; round_number <= round_count; ++round_number) {
            std::cout << "Round " << round_number << "\n";

            if (round_number < round_count) {
                show_break();
            }
        }

        std::cout << "Training complete\n";
    } else {
        std::cout << "Invalid round count\n";
    }
}
```

- The **definition** of the function `show_break` stands before `main`. The **call** `show_break();` stands in the loop, in `main`.
- **The function doesn't know which round is on.** It always prints the same two lines. `main` decides whether a break is needed: round `round_number` is followed by another round only when `round_number < round_count`.
- **After the last round** the condition gives `false`, so there's no break. For one round, the condition `1 < 1` gives `false` already in the first iteration.
- **For zero rounds** the loop condition `1 <= 0` gives `false` straight away. There's no round and no break, and the program prints `Training complete`.
- **Another correct solution:** call the function **before** printing the round, but only from the second round on, with the condition `round_number > 1`. The result is the same.
- The range is checked with `if`/`else` before the program starts the plan, as in lesson 4.1.
- The function doesn't need the round number, because the break is always the same. If the break had to show the round number, the function would have to get it. You'll see how to pass data to a function in the next lesson.

</details>

**Previous lesson:** [Lesson 4.7: The program repeats actions (the Module 4 test)](../module_04_repeating_actions/lesson_07_the_program_repeats.en.md) · **Next lesson:** [Lesson 5.2: Parameters, arguments and passing by value](lesson_02_parameters_and_arguments.en.md) · [Course overview](../../README.en.md)

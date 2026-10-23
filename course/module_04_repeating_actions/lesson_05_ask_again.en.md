# Lesson 4.5: Asking again for a valid value

[Polski](lesson_05_ask_again.md) · **English** · [Course overview](../../README.en.md)

> **Module 4, lesson 5** · about 75–90 minutes
> **You need:** the `cpp-workspace` folder and the original `lesson_05_first_program` project, as before. You don't need the debugger in this lesson.
> **Pilot version.** The programs in this lesson are checked automatically on Windows, Ubuntu and macOS, including with the given input data. Typing input into CLion's **Run** window is described without a manual check on every system.

## Before you start

This lesson assumes that:

- you check a correctly read value with `if`, and tell a wrong value from a failed read (lesson 3.5);
- you combine conditions with `&&`, `||` and `!` (lesson 3.4);
- you write a `while` loop that repeats an action until a goal is reached, and explain why it ends (lessons 4.1 and 4.4);
- you increase a counter with `++` (lesson 4.3).

## The situation

A program asks for a number of study sessions. Values from 1 to 5 are acceptable. In Module 3 you learned to check a number that was read: if it fits, the program accepts it; if not, it prints a message and ends.

Now the requirement changes: **if the user gives a number outside the range, the program should ask again**. The program has to keep asking until it gets a suitable value, i.e. until it reaches a goal, as in lesson 4.4. Along the way something new comes up: sometimes a number can't be read at all. The program has to notice that before it starts checking the value.

After this lesson you'll be able to:

- ask again in a `while` loop, as long as the value read doesn't meet the requirements;
- check with `std::cin.fail()` whether reading a number succeeded, and understand calling a member function with a dot;
- check the value only after a successful read;
- end the loop for two reasons: after accepting a value, or after a failed read;
- explain why running out of data must not lead to asking forever;
- tell a rejected value from a failed read, and plan tests with several attempts in a row.

## 1. Prepare the project

In `cpp-workspace`, create a `lesson_4_5` folder and copy `main.cpp` and `CMakeLists.txt` into it from the original `lesson_05_first_program`. You type the programs from sections 3–7 into that folder's `main.cpp`.

## 2. One check isn't enough

This is how a value was checked in Module 3:

<!-- fragment -->
```cpp
std::cout << "Enter session count (1-5):\n";
std::cin >> sessions;

if (sessions >= 1 && sessions <= 5) {
    std::cout << "Accepted sessions: " << sessions << "\n";
} else {
    std::cout << "Session count out of range\n";
}
```

**Think about it:** what would have to change for the program to ask again after a wrong value? `if` chooses one path, and the program carries on. It doesn't go back to the read. To ask again, the program has to **go back to the read**. And going back to the same piece of code is a job for a loop.

## 3. Ask while the value is wrong

The first, **simplified** version assumes that every read of a number succeeds, and that the user eventually gives a value in the range. It isn't a complete solution yet. It only shows how a loop goes back to the question.

<!-- example: sessions_simple -->
```cpp
#include <iostream>

int main() {
    int sessions{0};

    std::cout << "Enter session count (1-5):\n";
    std::cin >> sessions;

    while (sessions < 1 || sessions > 5) {
        std::cout << "Session count out of range\n";
        std::cout << "Enter session count (1-5):\n";
        std::cin >> sessions;
    }

    std::cout << "Accepted sessions: " << sessions << "\n";
}
```

**Predict** what the program will print when the user gives first 0, then 3. And when they give 9, then 6, then 2? Then check.

<!-- input: sessions_simple -->
```text
0
3
```

<details>
<summary>Standard output for 0 and 3</summary>

<!-- output: sessions_simple -->
```text
Enter session count (1-5):
Session count out of range
Enter session count (1-5):
Accepted sessions: 3
```

</details>

<!-- input: sessions_simple -->
```text
9
6
2
```

<details>
<summary>Standard output for 9, 6 and 2</summary>

<!-- output: sessions_simple -->
```text
Enter session count (1-5):
Session count out of range
Enter session count (1-5):
Session count out of range
Enter session count (1-5):
Accepted sessions: 2
```

</details>

The `while` condition checks the value **after every attempt**. As long as the number read is outside the range, the loop body prints a message and reads another number. The first value in the range makes the condition give `false`, and the loop ends.

**But what if text appears instead of a number, or the data runs out?** Then reading the number **fails**. The input stream remembers that the read failed, and every further read of the same kind also fails at once, without waiting for new data. The variable `sessions` gets no new value typed by the user, and the loop's condition checks a value that can't be relied on. Such a loop could ask forever. That's why we run this program only with data that ends in a valid number. A complete version must first check **whether the read succeeded**.

## 4. Did the read succeed? `std::cin.fail()`

`std::cin` is the program's standard input. After every read you can ask whether it succeeded:

<!-- fragment -->
```cpp
std::cin >> sessions;

if (std::cin.fail()) {
    std::cout << "Input could not be read\n";
}
```

- `std::cin` represents the standard input stream, from which the program reads data.
- **The dot** after `std::cin` lets you refer to a function that belongs to this object, i.e. to its **member function**. `std::cin.fail()` is a question asked of the stream `std::cin`.
- `fail` is the name of that function. **The parentheses** `()` mean that the function is called, i.e. that the question is asked now.
- The result is a `bool`: `true` when the stream is in a read-error state, and `false` when the reads so far succeeded. That's why `std::cin.fail()` can stand in an `if` condition.

**What exactly does `true` mean?** That a read failed. It does **not** say why. The cause might be text instead of a number, but also simply that the data ran out. This lesson doesn't tell these causes apart, which is why the program prints a neutral message, `Input could not be read`, not "text was typed" or "end of data".

## 5. Two reasons to end

The complete program can end the loop for two reasons, and each one has its own `bool` variable:

- `accepted`: we got a value that meets the requirements;
- `read_failed`: a read failed.

These are ordinary `bool` variables, **flags** describing the program's state, not a new type. The loop runs while neither of them is set: `!accepted && !read_failed`.

<!-- example: sessions -->
```cpp
#include <iostream>

int main() {
    int sessions{0};
    bool accepted{false};
    bool read_failed{false};

    while (!accepted && !read_failed) {
        std::cout << "Enter session count (1-5):\n";
        std::cin >> sessions;

        if (std::cin.fail()) {
            read_failed = true;
        } else if (sessions >= 1 && sessions <= 5) {
            accepted = true;
        } else {
            std::cout << "Session count out of range\n";
        }
    }

    if (accepted) {
        std::cout << "Accepted sessions: " << sessions << "\n";
    } else {
        std::cout << "Input could not be read\n";
    }
}
```

In every iteration the order is always the same:

1. The program prints the question.
2. It tries to read a number, **once per iteration**.
3. It checks whether the read succeeded.
4. If not, it sets `read_failed` and doesn't ask again.
5. If so, it checks whether the number is in the range.
6. If it isn't, it prints a message. The flags don't change, so the loop asks again.
7. If it is, it sets `accepted`, and the loop ends.

**Checking the range doesn't replace checking the read.** The `if`/`else if` chain checks `std::cin.fail()` first. The program gets to comparing `sessions` with the range only when the read succeeded. After a failed read, no decision is based on the value of `sessions`, because the program doesn't know whether that value has anything to do with the user's data. The order of conditions in the chain matters, as in lesson 3.3.

After the loop, checking one flag is enough: if `accepted` isn't set, the loop must have ended because of a failed read.

## 6. Trace the attempts

The user types `0`, `6` and `3`, in that order. **Predict**: copy the table and fill it in before you run the program.

| Attempt | Value read | Read succeeded? | Meets the requirements? | `accepted` after the attempt | `read_failed` after the attempt | Another question? |
|---|---|---|---|---|---|---|
| 1 | | | | | | |
| 2 | | | | | | |
| 3 | | | | | | |

How many read attempts were there, and how many rejected values? You'll find the completed table in [Example solutions](#example-solutions). Now run the program with this data, and also with 3 and with 5 given straight away.

<!-- input: sessions -->
```text
0
6
3
```

<details>
<summary>Standard output for 0, 6 and 3</summary>

<!-- output: sessions -->
```text
Enter session count (1-5):
Session count out of range
Enter session count (1-5):
Session count out of range
Enter session count (1-5):
Accepted sessions: 3
```

</details>

<!-- input: sessions -->
```text
3
```

<details>
<summary>Standard output for 3</summary>

<!-- output: sessions -->
```text
Enter session count (1-5):
Accepted sessions: 3
```

</details>

<!-- input: sessions -->
```text
5
```

<details>
<summary>Standard output for 5</summary>

<!-- output: sessions -->
```text
Enter session count (1-5):
Accepted sessions: 5
```

</details>

## 7. When the data runs out

Data isn't always typed by a person who will give another number. It may come from a file or an automatic test, and then it simply **runs out**. That's how the programs in this course are checked: the data is passed to the program all at once, and after the last line nothing more comes.

The program gets only `0`. **Predict**: how many times will it ask for a number, what will it print, and will it end?

<!-- input: sessions -->
```text
0
```

<details>
<summary>Standard output when the data runs out after 0</summary>

<!-- output: sessions -->
```text
Enter session count (1-5):
Session count out of range
Enter session count (1-5):
Input could not be read
```

| Attempt | What happens | `accepted` | `read_failed` | Another question? |
|---|---|---|---|---|
| 1 | read succeeds: 0, out of range, message | `false` | `false` | yes |
| 2 | read **fails**: there's no more data | `false` | `true` | no: the loop ends |

The program asks a second time, tries to read a number, finds that the read failed, and ends normally. That isn't "another wrong number". The program read nothing.

</details>

The shortest case: there's no data from the very start. The program gets only an empty line and no number.

<!-- input: sessions -->
```text
```

<details>
<summary>Standard output when there's no number at all</summary>

<!-- output: sessions -->
```text
Enter session count (1-5):
Input could not be read
```

</details>

**A program with an input loop must not ask forever when the data runs out.** It mustn't assume that new data will surely come. This program ends on its own, thanks to the `read_failed` flag, not because someone stopped it. The course's automatic tests do have a time limit, but that limit only **detects** a program that doesn't end. A correct program never relies on it.

## 8. Text instead of a number

The program asks for a number, and the user types `abc`. **Predict** what will happen. And what if they first type `7`, then `abc`?

<!-- input: sessions -->
```text
abc
```

<details>
<summary>Standard output for abc</summary>

<!-- output: sessions -->
```text
Enter session count (1-5):
Input could not be read
```

</details>

<!-- input: sessions -->
```text
7
abc
```

<details>
<summary>Standard output for 7, then abc</summary>

<!-- output: sessions -->
```text
Enter session count (1-5):
Session count out of range
Enter session count (1-5):
Input could not be read
```

</details>

After `abc`, reading the number fails, so the program doesn't check the value and doesn't ask again. That's a deliberate limit of this lesson. After a failed read the stream is in an error state, and another read of the same kind would fail too. In lesson 4.6 you'll learn to bring the stream back to a state in which reading can continue, and to tell text from the end of the data.

One honest caveat: reading a number with `>>` doesn't check the whole line that was typed. After typing `12abc`, the program reads the number 12, and the characters `abc` stay in the stream for later. Checking whole lines isn't part of this lesson.

## 9. A rejected value, a failed read, the end of the data

| Situation | Example | What happened | What the program does |
|---|---|---|---|
| **A rejected value** | `6` | The read succeeded: it's a valid `int`, but it doesn't meet the requirements. | Prints a message and safely asks again. |
| **A failed read** | `abc` | Reading the number failed. The stream is in an error state and doesn't allow simply repeating the same read. | Ends with the message `Input could not be read`. |
| **The end of the data** | nothing after `0` | The data ran out, so the next read fails. The program mustn't assume new data will come. | This is a failed read too: the same message and the same ending. |

In this lesson both kinds of failed read end the same safe way. In lesson 4.6 this model will be extended.

## 10. Analyse: a loop that doesn't check the read

**Analyse this fragment on paper; don't run it.** It has only one flag and checks only the range:

<!-- fragment -->
```cpp
bool accepted{false};

while (!accepted) {
    std::cout << "Enter session count (1-5):\n";
    std::cin >> sessions;

    if (sessions >= 1 && sessions <= 5) {
        accepted = true;
    } else {
        std::cout << "Session count out of range\n";
    }
}
```

Answer the questions before you look at the solution:

1. What happens when the user gives a valid number straight away, for example 3?
2. What happens when they give a number outside the range, for example 6?
3. What happens when a read fails, for example after `abc` or when the data runs out?
4. Why doesn't another read in the next iteration fix the problem by itself?
5. What extra check is needed?

The answers and a trace table are in [Example solutions](#example-solutions). The fixed, safe program is the one from section 5.

## 11. Mission: choosing a workstation

A lab has workstations 1 to 3 and 7 to 9 available. Workstations 4 to 6 are unavailable. The program asks for a workstation number. If the chosen workstation is unavailable, it says so and asks again. If it's available, it stops asking, and prints the chosen workstation and the number of **correctly read but unavailable** numbers it rejected before the choice. If reading a number fails, the program ends without confirming any choice.

**Requirements:**

- A `while` loop with two reasons to end: a workstation chosen, or a failed read.
- In each iteration the program prints `Enter station number:` and reads a whole number.
- First it checks whether the read succeeded. Only then does it check whether the workstation is available.
- For an unavailable number it prints `Station unavailable` and asks again.
- It counts only rejected numeric values. A failed read isn't a rejected number.
- After a choice it prints `Selected station: N` and `Rejected selections: R`.
- After a failed read it prints only `Input could not be read`, with no choice report.

In `cpp-workspace`, create a `station_choice` folder, copy `CMakeLists.txt` into it from the original `lesson_05_first_program`, create an empty `main.cpp` and write the program on your own.

Standard output for four situations must be as follows. A choice straight away, with `2` typed:

<!-- input: station_choice -->
```text
2
```

<!-- output: station_choice -->
```text
Enter station number:
Selected station: 2
Rejected selections: 0
```

One unavailable number, with `5` and `8` typed:

<!-- input: station_choice -->
```text
5
8
```

<!-- output: station_choice -->
```text
Enter station number:
Station unavailable
Enter station number:
Selected station: 8
Rejected selections: 1
```

The data runs out after `5`:

<!-- input: station_choice -->
```text
5
```

<!-- output: station_choice -->
```text
Enter station number:
Station unavailable
Enter station number:
Input could not be read
```

Text instead of a number, i.e. `abc` typed:

<!-- input: station_choice -->
```text
abc
```

<!-- output: station_choice -->
```text
Enter station number:
Input could not be read
```

**This isn't the program from section 5 with new names.** There, the acceptable values formed one continuous range, and the program only accepted or rejected a value. Here:

- the available workstations belong to **two separate** ranges, so you have to build the availability condition yourself from `&&` and `||`;
- the program also keeps a **rejection counter**, which changes in only one of the three situations;
- the choice report and the failed-read message mean different things and never appear together.

**Before you write the program**, prepare two things:

- a trace table for the data `0`, `5`, `2`: the attempt, the value read, whether the read succeeded, whether the workstation is available, both flags, and the rejection counter after the attempt;
- a table of test cases: all four boundaries of both ranges, the values right next to them, a negative number, several rejections before a choice, a failed read after a rejection, and the end of the data after several rejections. Write down the expected standard output for each case.

### Success criteria

- The program builds as C++20, and its standard output for the four situations above is exactly as shown.
- The `while` loop ends for two named reasons stored in `bool` variables. The read happens once per iteration.
- The read's success is checked with `std::cin.fail()` **before** availability is checked. After a failed read, no decision is based on the number's value.
- The availability condition accepts exactly workstations 1–3 and 7–9.
- The rejection counter grows only after a successful read of an unavailable number.
- After a failed read, neither `Selected station` nor `Rejected selections` appears.
- The trace table and the table of cases were made before running the program.
- You can explain why the program also ends when the data runs out.

When the result matches, you can save the project in Git, as in lesson 1.5.

<details>
<summary>Hint 1</summary>

Think about which two events can end the repeated asking.

</details>

<details>
<summary>Hint 2</summary>

The availability condition covers two separate ranges. Each range needs two comparisons.

</details>

<details>
<summary>Hint 3</summary>

The rejection counter should change only after a successful read of a value that doesn't meet the requirements.

</details>

<details>
<summary>The full list of control cases: open after preparing your own table</summary>

| Data | Result | Rejections | What it checks |
|---|---|---|---|
| `2` | choice 2 | 0 | an available number straight away |
| `5`, `8` | choice 8 | 1 | one rejection |
| `5`, end of data | `Input could not be read` | — | the end of the data after a rejection |
| `abc` | `Input could not be read` | — | text instead of a number |
| `1` | choice 1 | 0 | the lower boundary of the first range |
| `3` | choice 3 | 0 | the upper boundary of the first range |
| `7` | choice 7 | 0 | the lower boundary of the second range |
| `9` | choice 9 | 0 | the upper boundary of the second range |
| `4`, `7` | choice 7 | 1 | the start of the unavailable area |
| `6`, `9` | choice 9 | 1 | the end of the unavailable area |
| `0`, `5`, `2` | choice 2 | 2 | two rejections |
| `-1`, `3` | choice 3 | 1 | a negative number |
| `4`, `abc` | `Input could not be read` | — | a failed read after a rejection |
| `4`, `6`, end of data | `Input could not be read` | — | the end of the data after two rejections |
| no data | `Input could not be read` | — | the end of the data before the first number |

The first four cases are checked above, in the mission's description.

<!-- input: station_choice -->
```text
1
```

<!-- output: station_choice -->
```text
Enter station number:
Selected station: 1
Rejected selections: 0
```

<!-- input: station_choice -->
```text
3
```

<!-- output: station_choice -->
```text
Enter station number:
Selected station: 3
Rejected selections: 0
```

<!-- input: station_choice -->
```text
7
```

<!-- output: station_choice -->
```text
Enter station number:
Selected station: 7
Rejected selections: 0
```

<!-- input: station_choice -->
```text
9
```

<!-- output: station_choice -->
```text
Enter station number:
Selected station: 9
Rejected selections: 0
```

<!-- input: station_choice -->
```text
4
7
```

<!-- output: station_choice -->
```text
Enter station number:
Station unavailable
Enter station number:
Selected station: 7
Rejected selections: 1
```

<!-- input: station_choice -->
```text
6
9
```

<!-- output: station_choice -->
```text
Enter station number:
Station unavailable
Enter station number:
Selected station: 9
Rejected selections: 1
```

<!-- input: station_choice -->
```text
0
5
2
```

<!-- output: station_choice -->
```text
Enter station number:
Station unavailable
Enter station number:
Station unavailable
Enter station number:
Selected station: 2
Rejected selections: 2
```

<!-- input: station_choice -->
```text
-1
3
```

<!-- output: station_choice -->
```text
Enter station number:
Station unavailable
Enter station number:
Selected station: 3
Rejected selections: 1
```

<!-- input: station_choice -->
```text
4
abc
```

<!-- output: station_choice -->
```text
Enter station number:
Station unavailable
Enter station number:
Input could not be read
```

<!-- input: station_choice -->
```text
4
6
```

<!-- output: station_choice -->
```text
Enter station number:
Station unavailable
Enter station number:
Station unavailable
Enter station number:
Input could not be read
```

<!-- input: station_choice -->
```text
```

<!-- output: station_choice -->
```text
Enter station number:
Input could not be read
```

</details>

An example solution is in [Example solutions](#example-solutions).

## 12. When something goes differently

| What you see | What it means | What to do |
|---|---|---|
| The question repeats forever | The loop doesn't check whether the read succeeded, and after a failed read it has no way to end. | Stop the program, as in lesson 4.1. Add a `std::cin.fail()` check and a flag that ends the loop. |
| After `abc` the program says "out of range" | The value is checked before the program checks the read. | In the `if`/`else if` chain, check `std::cin.fail()` first. |
| After a failed read, a choice report appears | After the loop, the program doesn't check which flag ended it. | Print the report only when the value was accepted. |
| The rejection counter is one too high | The counter also grows after a failed read, or after accepting a value. | Increase it only in the branch for a correctly read, unavailable value. |
| The question appears twice in a row without a read | The question or the read is in the wrong place, for example the question both before the loop and in it. | One question and one read per iteration, both in the loop body. |
| Workstations 4–6 are accepted, or 1–3 rejected | The availability condition combines the comparisons with the wrong operators. | Each range is two comparisons with `&&`. The two ranges are joined with `\|\|`. Add parentheses. |
| The program does nothing and waits | It's waiting for another number, as in lesson 2.6. | Type a number and press **Enter**. |

## 13. Explain

Answer briefly, preferably in writing. Only then compare with the example answer.

**1.** Why isn't a single `if` enough to ask again?

<details>
<summary>Example answer</summary>

Because `if` chooses one path and the program carries on. It doesn't go back to the read. Asking again requires going back to the same piece of code, i.e. a loop.

</details>

**2.** What makes the loop ask again, and why is the read in its body?

<details>
<summary>Example answer</summary>

After a rejected value neither flag changes, so the condition `!accepted && !read_failed` still gives `true`, and the program goes back to the start of the body. Every iteration is a new attempt: a new question and a new read. If the read were before the loop, the loop would check the same value over and over.

</details>

**3.** What does `std::cin.fail()` check, and what does the dot in it mean?

<details>
<summary>Example answer</summary>

It checks whether the input stream is in a read-error state, i.e. whether a read failed. The dot refers to a member function of the object `std::cin`, and the parentheses call it. The result is a `bool`.

</details>

**4.** Why doesn't the program check the number's value after a failed read?

<details>
<summary>Example answer</summary>

Because the read delivered no new value from the user. The program doesn't know whether the number in the variable has anything to do with the data typed, so it can't base a decision on it.

</details>

**5.** How does typing `0` differ from typing `abc`?

<details>
<summary>Example answer</summary>

`0` is a successful read of a valid `int` that doesn't meet the requirements, so the program asks again. `abc` is a failed read of a number. The stream is then in an error state, so the program ends.

</details>

**6.** Why doesn't the program in this lesson ask again after `abc`?

<details>
<summary>Example answer</summary>

Because after a failed read the stream is in an error state, and another read of the same kind would fail too. We can't yet bring the stream back into working order. Lesson 4.6 teaches that.

</details>

**7.** What happens when the input data runs out?

<details>
<summary>Example answer</summary>

The next read fails, `std::cin.fail()` gives `true`, the program sets `read_failed`, the loop ends, and the program prints `Input could not be read` and ends normally. It doesn't ask even once more.

</details>

**8.** Why does the loop have two reasons to end?

<details>
<summary>Example answer</summary>

Because it can end with a success, accepting a value, or with a failure, a failed read. After the loop, the program has to know what happened, so it can print the right message. Each reason is recorded by its own flag.

</details>

**9.** Why doesn't a failed read increase the count of rejected workstations in the mission?

<details>
<summary>Example answer</summary>

Because the counter counts numbers the program read and rejected as unavailable. After a failed read there's no number, so there's nothing to reject.

</details>

**10.** What will lesson 4.6 teach?

<details>
<summary>Example answer</summary>

How to bring the stream back into working order after a failed read, so the program can ask again after text too, and how to tell text from the end of the data.

</details>

## Summary

- To ask again, the program has to go back to the read. So the question and the read stand in the body of a `while` loop, once per iteration.
- `std::cin.fail()` checks whether a read failed. It's a call to a **member function**: the dot refers to a function of the object `std::cin`, and the parentheses call it. The result is a `bool`.
- `fail()` doesn't say why a read failed: the cause may be text or the end of the data. That's why the message is neutral.
- **Check the read first, the value only afterwards.** After a failed read, no decision is based on the variable's value.
- An input loop has two reasons to end, recorded in two flags: a value accepted, or a read failed.
- A rejected value lets the program safely ask again. A failed read, including the end of the data, ends the program in this lesson.
- A program with an input loop must not ask forever when the data runs out.

## What's next

The program in this lesson ends after every failed read, even after a simple typo. In lesson 4.6 you'll learn to bring the stream back into working order, discard the bad entry and ask again, while telling a bad entry from the end of the data: [Lesson 4.6: A failed read, recovering the stream and the end of the data](lesson_06_recover_and_end_of_input.en.md).

---

## Example solutions

Look here **after your own attempt**. Your names may differ, as long as the standard output is as required.

<details>
<summary>Section 6: the table for 0, 6 and 3</summary>

| Attempt | Value read | Read succeeded? | Meets the requirements? | `accepted` after the attempt | `read_failed` after the attempt | Another question? |
|---|---|---|---|---|---|---|
| 1 | 0 | yes | no: too small | `false` | `false` | yes |
| 2 | 6 | yes | no: too large | `false` | `false` | yes |
| 3 | 3 | yes | yes | `true` | `false` | no: the loop ends |

There were three read attempts and two rejected values. The number of attempts isn't the number of rejections: the last attempt gave an accepted value.

</details>

<details>
<summary>Section 10: the loop without a read check</summary>

1. **A valid number, for example 3:** the read succeeds, 3 is in the range, `accepted` becomes `true`, and the loop ends. The program works correctly.
2. **A number outside the range, for example 6:** the read succeeds, the program prints a message and asks again. Also correct.
3. **A failed read:**

| Attempt | Read | Value of `sessions` | Range condition | `accepted` | Another question? |
|---|---|---|---|---|---|
| 1 | **fails** (`abc` or the end of the data) | can't be relied on | depends on an accidental value | `false`, if the condition doesn't pass | yes |
| 2 | **fails at once**: the stream is already in an error state | still the same | the same result | `false` | yes |
| … | **fails at once** | still the same | the same result | `false` | yes |

4. **Another read changes nothing:** a stream in an error state takes no new data, so every next attempt fails at once. The value in the variable doesn't change, the condition gives the same result every time, and the loop prints the question and the message forever. It might also accept a value nobody typed, if that accidental value happens to be in the range.
5. **The missing piece is a `std::cin.fail()` check** before the range check, and a second reason for the loop to end, the `read_failed` flag. That's how the program in section 5 works.

</details>

<details>
<summary>Section 11: the mission, choosing a workstation</summary>

<!-- example: station_choice -->
```cpp
#include <iostream>

int main() {
    int station{0};
    int rejected_count{0};
    bool selected{false};
    bool read_failed{false};

    while (!selected && !read_failed) {
        std::cout << "Enter station number:\n";
        std::cin >> station;

        if (std::cin.fail()) {
            read_failed = true;
        } else if ((station >= 1 && station <= 3) || (station >= 7 && station <= 9)) {
            selected = true;
        } else {
            std::cout << "Station unavailable\n";
            ++rejected_count;
        }
    }

    if (selected) {
        std::cout << "Selected station: " << station << "\n";
        std::cout << "Rejected selections: " << rejected_count << "\n";
    } else {
        std::cout << "Input could not be read\n";
    }
}
```

| Attempt | Value read | Read succeeded? | Available? | `selected` | `read_failed` | `rejected_count` |
|---|---|---|---|---|---|---|
| 1 | 0 | yes | no | `false` | `false` | 1 |
| 2 | 5 | yes | no | `false` | `false` | 2 |
| 3 | 2 | yes | yes | `true` | `false` | 2 |

- **Two flags:** `selected` for success and `read_failed` for failure. The loop runs while neither is set.
- **The order in the chain:** first `std::cin.fail()`, then availability. After a failed read, the number isn't compared.
- **The availability condition:** each range is two comparisons joined with `&&`, and the two ranges are joined with `||`. The parentheses show the grouping, as in lesson 3.4.
- **The rejection counter** grows only in the `else` branch, i.e. after a successful read of an unavailable number.
- **After the loop,** the choice report appears only when `selected` is `true`. Otherwise the loop was ended by a failed read.

</details>

**Previous lesson:** [Lesson 4.4: Repeating until the goal is reached](lesson_04_repeat_until_the_goal.en.md) · **Next lesson:** [Lesson 4.6: A failed read, recovering the stream and the end of the data](lesson_06_recover_and_end_of_input.en.md) · [Course overview](../../README.en.md)

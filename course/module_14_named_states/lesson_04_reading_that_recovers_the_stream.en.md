# Lesson 14.4: Try again: reading that recovers the stream

[Polski](lesson_04_reading_that_recovers_the_stream.md) · **English** · [Course overview](../../README.en.md)

> **Module 14, lesson 4** · about 95–120 minutes, in two sessions: sections 1–5 are the reading and recovery mechanism, sections 6–10 the sequence tests and the mission
> **You need:** your `cpp-workspace` folder and the original `lesson_05_first_program` project, as before. You won't need the debugger in this lesson.
> **Pilot version.** The programs in this lesson are checked automatically on Windows, Ubuntu and macOS, including with the given input data and together with their exit codes. Typing input into CLion's **Run** window is described without a manual check on every system.

## Before you start

This lesson assumes that you:

- know from lesson 4.6 that a failed read leaves two obstacles: the stream's error state and the text left in the input; you know `clear()`, discarding the rest of the line with `std::getline`, `eof()` and the order "first the success of the read, then the end of the data";
- write reading functions with a `std::istream&` parameter that read into local variables and assign the result only after the checks (lesson 10.4);
- create a stream from text with `std::istringstream` in tests and give every independent case a new stream (lesson 13.3);
- return a named result of an `enum class` type from a function, handle every result with a `switch` statement and check the result and the state of the data separately in tests (lessons 14.1–14.3).

## The situation

A ticket machine asks how many tickets someone wants: from 1 to 6. People make mistakes. Someone types `abc`, someone `9`, someone `3 tickets`, and someone presses Enter without typing anything. The program has to say what's wrong, let the person try again, and end by itself when there's no more data. It isn't a real sales system: you practise reading on this machine.

In lesson 4.6 such a read stood in a loop in `main`. Here it goes into a function that returns a named result every time and prepares the stream for the next attempt by itself.

You'll answer the question: **how do you write a reading function that lets you try again after a bad entry, doesn't lose the last number, and doesn't loop forever when the data runs out?**

After this lesson you will:

- tell apart four results of a read: `accepted`, `out_of_range`, `invalid_input` and `end_of_input`;
- explain what `clear()` repairs and what `ignore` removes, and why a failed read needs both;
- recognise the end of the data before you try to read the next number, also when the last number has no line end;
- read into a local variable and leave the result parameter unchanged on a refusal;
- handle the results with a `switch` statement and end the loop after `end_of_input`;
- test whole sequences of reads on one stream.

## 1. Two obstacles after `abc`

A stream holds three lines:

| Line | Content |
|---|---|
| 1 | `2` |
| 2 | `abc` |
| 3 | `5` |

The first read of a number gives 2, and the second meets `abc` and fails. What has to happen for the third read to give 5? The program below checks this on three streams with the same text, `"2\nabc\n5\n"`. The function `try_read` reads one number and prints what happened. Stream A stays as it is after the error, stream B gets only `clear()`, and stream C gets `clear()` and `ignore`.

<!-- example: recovery_steps -->
```cpp
#include <iostream>
#include <limits>
#include <sstream>
#include <string>

void try_read(std::istream& input, const std::string& label) {
    int number{0};
    input >> number;

    if (input.fail()) {
        std::cout << label << ": read failed\n";
    } else {
        std::cout << label << ": read " << number << "\n";
    }
}

int main() {
    std::istringstream input_a{"2\nabc\n5\n"};
    try_read(input_a, "A1");
    try_read(input_a, "A2");
    try_read(input_a, "A3");

    std::istringstream input_b{"2\nabc\n5\n"};
    try_read(input_b, "B1");
    try_read(input_b, "B2");
    input_b.clear();
    try_read(input_b, "B3");

    std::istringstream input_c{"2\nabc\n5\n"};
    try_read(input_c, "C1");
    try_read(input_c, "C2");
    input_c.clear();
    input_c.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
    try_read(input_c, "C3");
}
```

You may run this program, but you don't have to: it's enough to predict the result and compare it with the output below. If you want to run it, create a folder `lesson_14_4` in `cpp-workspace`, copy `main.cpp` and `CMakeLists.txt` into it from the original `lesson_05_first_program`, and replace the contents of `main.cpp` with the program above. The programs of sections 1–7 are one-file programs, and they can all be made in this folder, one after another.

**Predict** the results A3, B3 and C3 before you open the output.

<details>
<summary>Standard output</summary>

<!-- output: recovery_steps -->
```text
A1: read 2
A2: read failed
A3: read failed
B1: read 2
B2: read failed
B3: read failed
C1: read 2
C2: read failed
C3: read 5
```

</details>

- **A3: the read fails,** because the stream is in the error state. As long as that state lasts, every further read fails at once, as in lesson 4.6. The program never gets to `5`.
- **B3: it still fails.** `clear()` removed the error flag, but it removed no character. The read meets the same `abc` again.
- **C3: the read gives 5.** `clear()` restored the normal state, and `ignore` took `abc` out of the input together with the line end. The next read starts at the line with `5`.

| Step | Stream state | What waits in the input |
|---|---|---|
| after the failed read of `abc` | error: `fail()` gives `true` | `abc`, the line end, then `5` |
| after `clear()` | normal: `fail()` gives `false` | **still** `abc`, the line end, then `5` |
| after `ignore` | normal | `5` and the line end |

**`clear()` repairs the state, and `ignore` removes characters.** A failed read needs both, in this order.

## 2. `ignore`: discarding the rest of the line

In the program of section 1, recovering the stream takes two lines:

<!-- fragment -->
```cpp
input_c.clear();
input_c.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
```

In lesson 4.6, `std::getline` into a helper variable discarded the rest of the line:

<!-- fragment -->
```cpp
std::cin.clear();

std::string discarded_line{""};
std::getline(std::cin, discarded_line);
```

Lesson 4.6 said that there are other ways to discard data from the input too. `ignore` is one of them: a member function of the stream that takes characters out of the input and throws them away at once. It needs no variable for the text to go into.

| Part | Meaning |
|---|---|
| `input_c.ignore(…)` | take characters out of the stream `input_c` and throw them away |
| `std::numeric_limits<std::streamsize>::max()` | the largest value of the type `std::streamsize`, which the library uses to count characters; for `ignore` this one value means **no limit on the number of characters** |
| `'\n'` | stop at the end of the line; the line end is taken away too |

When the data ends before the line does, `ignore` stops at the end of the data.

Read the whole expression as one command: **discard the remaining characters up to the end of the line or the end of the data.** `std::numeric_limits` needs `#include <limits>`. A program may build without that include, because other headers sometimes include it, but you mustn't rely on that.

**First `clear()`, then `ignore`.** On a stream in the error state `ignore` does nothing, just like `getline` in lesson 4.6. In section 7 you'll see what happens when `clear()` is missing.

`getline` and `ignore` have different uses. `getline` reads text into a variable and is useful when that text is needed, for example when a program reads whole lines, as in lesson 12.3. `ignore` only throws characters away. The earlier programs of the course don't need to change anything: discarding with `getline` still works in them.

<details>
<summary>For the curious: <code>ignore()</code> without arguments, a fixed number of characters, and the difference from <code>getline</code></summary>

| Call | What it does | The effect after a failed read of `abc` |
|---|---|---|
| `input.ignore()` | takes **one** character | `bc` is left: the next attempts meet `b`, then `c`, so one entry becomes three failed reads |
| `input.ignore(1000, '\n')` | takes at most 1000 characters | enough for short lines, but from a line longer than 1000 characters the rest goes into the next attempt |
| `input.ignore(std::numeric_limits<std::streamsize>::max(), '\n')` | takes everything up to the end of the line, without a limit | the whole line with `abc` is gone |

**`getline` and `ignore` aren't interchangeable in every situation.** In this lesson they take the same characters, but `getline` stores them in a `std::string` variable. They also differ in the stream state at the very end of the data: when the stream is in the normal state but there's no character left to take, `getline` reports a failed read (`fail()` gives `true`), and `ignore` only reaches the end of the data (`eof()` gives `true`).

</details>

## 3. The end of the data before reading the number

The reading function will be called many times, until the data runs out. So every time, it first has to find out whether there's another entry. Two lines do it:

<!-- fragment -->
```cpp
input >> std::ws;

if (input.eof()) {
    return ReadResult::end_of_input;
}
```

- **`input >> std::ws;`** skips **whitespace**: spaces, tabs and line ends. So it also skips empty lines and lines with only spaces. It stops at the first character that isn't whitespace, or at the end of the data. It removes nothing but whitespace.
- **`eof()` after `std::ws`** answers the question: is there anything left after the whitespace? If not, there's no next entry, and the function returns `end_of_input` before it tries to read a number.

**Why not check `eof()` after reading the number?** Lesson 4.6 showed that a successful read of the last number can reach the end of the data. When the data ends with `4` and no line end, `>>` reads 4, and `eof()` already gives `true`. That isn't an error. So after reading the number, `eof()` doesn't say whether the read succeeded. The function asks about the end of the data before the read, and after the read it only checks whether the read succeeded.

Successive calls of this lesson's function on one stream, with the range 1–6:

| Data | Results of the successive calls |
|---|---|
| `""` | `end_of_input` |
| `"4"` | `accepted` (4), `end_of_input` |
| `"4\n"` | `accepted` (4), `end_of_input` |
| `"abc"` | `invalid_input`, `end_of_input` |
| `"abc\n"` | `invalid_input`, `end_of_input` |
| `"4\n5"` | `accepted` (4), `accepted` (5), `end_of_input` |

- **The last `4` without a line end** is accepted. Only the next call finds no entry.
- **The last `abc` without a line end** doesn't vanish: the function reports `invalid_input`. Reading the number stops at `a`, so it doesn't reach the end of the data. Only discarding the rest of the line takes `abc` away and reaches the end. The next call gives `end_of_input`.
- **Every further call after the end of the data** also gives `end_of_input`. The function doesn't call `clear()` then, and there's nothing to recover.

**Skipping whitespace isn't discarding the rest of the line:**

| Operation | What it removes | When |
|---|---|---|
| `input >> std::ws` | the whitespace before the entry, empty lines included | at the start of every attempt |
| discarding the rest of the line with `ignore` | all characters up to the end of the current line, bad text included | after every attempt that found an entry |

**A failure of the data source isn't the end of the data.** This lesson's function assumes a working source: text in memory, a file or the keyboard, from which data can be read with the normal stream operations. `input.bad()` gives `true` when the source itself failed, not an entry. That doesn't happen in the course's programs. If it did happen, the function wouldn't try to recover the stream: it returns `end_of_input` only as a signal that further reading is impossible, and changes nothing. That doesn't mean the data has ended. A program that must tell the two situations apart checks `input.bad()` after `end_of_input`.

<details>
<summary>For the curious: why lesson 4.6's order isn't enough here</summary>

In lesson 4.6 the program first checked whether the read succeeded, and only after a failed read `eof()`. In a function that is called until the end of the data, that's not enough.

A failed read that reached the end of the data sets `fail()` and `eof()` at the same time, for example when the last entry is a lone `-` sign or a number too large for `int`, without a line end. The stream state looks exactly the same when there's no data left at all. A function that recognises the end of the data after a failed read would then report `end_of_input` instead of `invalid_input`, and the last bad entry would vanish. For the data `"4\n-"` it would give `accepted`, `end_of_input` instead of `accepted`, `invalid_input`, `end_of_input`.

That's why the function recognises the end of the data before reading the number, after `std::ws`. After the read, the stream state is needed for one question only: did the read succeed?

One more small thing: when the accepted number was the last character of the data, discarding the rest of the line has nothing to take and sets `fail()`. The result `accepted` and the value read are already settled then, and the next call returns `end_of_input` anyway.

</details>

## 4. The function `read_number`

The four possible endings of a read get their own names:

<!-- fragment -->
```cpp
enum class ReadResult {
    accepted,
    out_of_range,
    invalid_input,
    end_of_input
};
```

The function gets the stream, the allowed range and a variable for the result:

<!-- fragment -->
```cpp
ReadResult read_number(std::istream& input, int minimum, int maximum, int& result);
```

**One call looks for the next character that isn't whitespace, tries to read a number from there, and then uses up the rest of the current line.** Empty lines and lines with only whitespace aren't separate attempts. From here on, the text where an attempt starts, up to the end of its line, is called an **entry**.

### The contract of `read_number`

**Assumptions:** `minimum <= maximum`, and the data source works (section 3). The function doesn't check this.

| Result | When | `result` |
|---|---|---|
| `ReadResult::accepted` | the read of an `int` succeeded, and the number is from `minimum` to `maximum` | gets the number read |
| `ReadResult::out_of_range` | the read succeeded, but the number is less than `minimum` or greater than `maximum` | unchanged |
| `ReadResult::invalid_input` | the read of an `int` failed | unchanged |
| `ReadResult::end_of_input` | there's no next entry | unchanged |

**`result` changes only on `accepted`.** With every other result it keeps its value from before the call. The function prints nothing.

**The function tries to read an integer at the start of the entry and discards the rest of the line.** It doesn't check whether the whole entry is a single number. For the range 1–6:

| Entry | Result | Why |
|---|---|---|
| `3` | `accepted`, value 3 | |
| `3.5` | `accepted`, value 3 | `>>` reads 3 and stops at the dot; `.5` is discarded |
| `3 tickets` | `accepted`, value 3 | ` tickets` is discarded |
| `2 5` | `accepted`, value 2 | `5` stands on the same line, so it's discarded |
| `12abc` | `out_of_range` | the read gives 12, and 12 is out of the range |
| `abc` | `invalid_input` | there's no number at the start of the entry |

This is a deliberate limit of this function, not a strict check of the whole entry: `3.5` isn't a valid way of writing an integer, and the function accepts 3 anyway. Just as in lesson 4.6, the program recovers the input after a failed read, but it doesn't check whole lines.

**A number too large for `int`.** If the written number doesn't fit in `int`, for example `999999999999999999999999`, the read fails. The function then returns `invalid_input`, not `out_of_range`: it doesn't know the value of the number typed.

**Why a local variable?** A failed read may store a different value in the variable, and lesson 4.6 said: you mustn't rely on the value after a failed read. A successful read of a number out of the range also stores that number. That's why the function reads into the variable `value`, and copies it into `result` only after all the checks, as in lesson 10.4.

### The whole function

In section 2 the call of `ignore` was written out directly. In the function the same operation is needed in two places, so it gets its own name: `discard_rest_of_line`. Inside is exactly the same call.

<!-- fragment -->
```cpp
enum class ReadResult {
    accepted,
    out_of_range,
    invalid_input,
    end_of_input
};

void discard_rest_of_line(std::istream& input) {
    input.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
}

ReadResult read_number(std::istream& input, int minimum, int maximum, int& result) {
    if (input.bad()) {
        return ReadResult::end_of_input;
    }

    input >> std::ws;

    if (input.eof()) {
        return ReadResult::end_of_input;
    }

    int value{0};
    input >> value;

    if (input.fail()) {
        if (input.bad()) {
            return ReadResult::end_of_input;
        }

        input.clear();
        discard_rest_of_line(input);
        return ReadResult::invalid_input;
    }

    discard_rest_of_line(input);

    if (value < minimum || value > maximum) {
        return ReadResult::out_of_range;
    }

    result = value;
    return ReadResult::accepted;
}
```

| Step | Code | What for |
|---|---|---|
| 1 | `if (input.bad())` at the start | the source stopped working: there's nothing to try |
| 2 | `input >> std::ws;` | skips whitespace and empty lines |
| 3 | `if (input.eof())` | there's no next entry: `end_of_input` |
| 4 | `input >> value;` | the read into a local variable |
| 5 | `if (input.fail())` | the read failed. `fail()` gives `true` for a failed source too, so `bad()` comes first: a failure ends reading without recovery. An ordinary bad entry: `clear()`, discarding the rest of the line, `invalid_input` |
| 6 | `discard_rest_of_line(input);` after a successful read | the rest of the line is gone, also after a valid number |
| 7 | the range check | a number out of the range: `out_of_range`, `result` unchanged |
| 8 | `result = value;` | only now: `accepted` |

The result depends on what the read and the range check gave. Discarding the rest of the line in step 6 may reach the end of the data, but it no longer changes the result. The function doesn't call `clear()` at the start of every attempt: it clears the state only when it has just recognised a failed read of a bad entry.

## 5. A program that asks again

`main` asks for the number of tickets as long as there's data:

<!-- fragment -->
```cpp
int main() {
    int tickets{0};
    bool input_ended{false};

    while (!input_ended) {
        std::cout << "How many tickets (1-6)?\n";
        const ReadResult result{read_number(std::cin, 1, 6, tickets)};

        switch (result) {
            case ReadResult::accepted:
                std::cout << "Tickets: " << tickets << "\n";
                break;
            case ReadResult::out_of_range:
                std::cout << "Choose from 1 to 6 tickets\n";
                break;
            case ReadResult::invalid_input:
                std::cout << "Not a whole number, try again\n";
                break;
            case ReadResult::end_of_input:
                input_ended = true;
                break;
        }
    }

    std::cout << "No more requests\n";
}
```

- **`const ReadResult result{read_number(std::cin, 1, 6, tickets)};`** calls the function once per question and keeps the result, as in lesson 14.3.
- **The `switch` does something different for each result:** on `accepted` it gives the number of tickets, on a refusal it says what to fix, and on `end_of_input` it sets `input_ended`. The `case` labels name all four results.
- **`break` ends only the `switch`.** The loop is ended by the condition `!input_ended`, like the flag `input_ended` in lesson 4.6.
- **Recovering the stream is inside the function.** `main` calls neither `clear()` nor `ignore`: after every call the stream is ready for the next attempt.

**This is the first required run.** Create a folder `lesson_14_4` in `cpp-workspace` (if you didn't in section 1), copy `main.cpp` and `CMakeLists.txt` into it from the original `lesson_05_first_program`, and replace the contents of `main.cpp` with the full program below. **Predict** the program's answers to four entries: `2`, `abc`, `9`, `3 tickets`. Then run the program and type them into the **Run** window, each followed by Enter.

You don't have to end the data from the keyboard. When you're done, stop the program with the **Stop** button. In the automatic check the data ends after the last line, so the program prints `No more requests` by itself.

<details>
<summary>The full program</summary>

<!-- example: ticket_requests -->
```cpp
#include <iostream>
#include <limits>

enum class ReadResult {
    accepted,
    out_of_range,
    invalid_input,
    end_of_input
};

void discard_rest_of_line(std::istream& input) {
    input.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
}

ReadResult read_number(std::istream& input, int minimum, int maximum, int& result) {
    if (input.bad()) {
        return ReadResult::end_of_input;
    }

    input >> std::ws;

    if (input.eof()) {
        return ReadResult::end_of_input;
    }

    int value{0};
    input >> value;

    if (input.fail()) {
        if (input.bad()) {
            return ReadResult::end_of_input;
        }

        input.clear();
        discard_rest_of_line(input);
        return ReadResult::invalid_input;
    }

    discard_rest_of_line(input);

    if (value < minimum || value > maximum) {
        return ReadResult::out_of_range;
    }

    result = value;
    return ReadResult::accepted;
}

int main() {
    int tickets{0};
    bool input_ended{false};

    while (!input_ended) {
        std::cout << "How many tickets (1-6)?\n";
        const ReadResult result{read_number(std::cin, 1, 6, tickets)};

        switch (result) {
            case ReadResult::accepted:
                std::cout << "Tickets: " << tickets << "\n";
                break;
            case ReadResult::out_of_range:
                std::cout << "Choose from 1 to 6 tickets\n";
                break;
            case ReadResult::invalid_input:
                std::cout << "Not a whole number, try again\n";
                break;
            case ReadResult::end_of_input:
                input_ended = true;
                break;
        }
    }

    std::cout << "No more requests\n";
}
```

</details>

<!-- input: ticket_requests -->
```text
2
abc
9
3 tickets
```

<details>
<summary>Standard output for these four entries</summary>

<!-- output: ticket_requests -->
```text
How many tickets (1-6)?
Tickets: 2
How many tickets (1-6)?
Not a whole number, try again
How many tickets (1-6)?
Choose from 1 to 6 tickets
How many tickets (1-6)?
Tickets: 3
How many tickets (1-6)?
No more requests
```

</details>

The second check starts with two empty lines:

<!-- input: ticket_requests -->
```text


5
```

<details>
<summary>Standard output for the data with empty lines</summary>

<!-- output: ticket_requests -->
```text
How many tickets (1-6)?
Tickets: 5
How many tickets (1-6)?
No more requests
```

</details>

The empty lines give no message: `std::ws` skips them, so they aren't attempts. The line `3 tickets` gives 3 tickets, because the function accepts the number at the start of the entry.

## 6. Sequence tests on one stream

In lesson 13.3 every independent case got a new `std::istringstream` and one call. That rule stays: **every test scenario gets a new stream.** Within a scenario, though, the function is called several times **on the same stream**, because that's exactly what the program does: it reads successive entries from one source. Lesson 13.3 said so directly: one stream is right when the program has to read successive data from one source.

You check every call twice: the result and the value of `tickets` after the call. The function `check_read_result` compares the result, built like `check_issue_result` in lesson 14.3. The text of a result comes from `read_result_text`, a `switch` with the fallback `"unknown"`, tested as in lesson 14.3:

<!-- fragment -->
```cpp
void check_read_result(const std::string& name, ReadResult expected, ReadResult actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << read_result_text(expected) << ", actual " << read_result_text(actual) << "\n";
        ++failed;
    }
}
```

The start of scenario S1. The call of `read_number` stands directly in the argument, like the call of the tested function in lesson 13.1. The check of `tickets` on the next line already sees the state after that call:

<!-- fragment -->
```cpp
std::istringstream input_s1{"2\nabc\n5\n"};
int tickets_s1{-1};
check_read_result("S1 call 1 result", ReadResult::accepted, read_number(input_s1, 1, 6, tickets_s1), checks, failed);
check_int("S1 call 1 tickets", 2, tickets_s1, checks, failed);
check_read_result("S1 call 2 result", ReadResult::invalid_input, read_number(input_s1, 1, 6, tickets_s1), checks, failed);
check_int("S1 call 2 tickets", 2, tickets_s1, checks, failed);
```

**The scenarios**, range 1–6, `tickets` equal to −1 at the start of every scenario. The expected results follow from the contract of section 4:

| Scenario | Data | Successive calls: the result and `tickets` after it | What it checks |
|---|---|---|---|
| S1 | `"2\nabc\n5\n"` | `accepted` 2; `invalid_input` 2; `accepted` 5; `end_of_input` 5 | recovering after a bad entry |
| S2 | `"7\n3"` | `out_of_range` −1; `accepted` 3; `end_of_input` 3 | a range refusal, the last number without a line end |
| S3 | `""` | `end_of_input` −1; `end_of_input` −1 | no data, and a call after the end of the data |
| S4 | `"4\n999999999999999999999999"` | `accepted` 4; `invalid_input` 4; `end_of_input` 4 | a number too large for `int` as the last entry without a line end |
| S5 | `"3 tickets\n5\n"` | `accepted` 3; `accepted` 5; `end_of_input` 5 | discarding the rest of the line after a valid number |

- **The starting value is −1, not 0.** −1 lies outside the range, and no valid read gives it. So every change of `tickets` after a refusal shows up in a `FAIL` line. With 0, some such changes would hide.
- **After a refusal `tickets` stays unchanged:** in S1 still 2 after `abc`, in S4 still 4 after the too large number.

**The number of checks:** 15 calls with 2 checks each give 30, plus 4 checks of `read_result_text`, 34 in total.

**This is the second required run.** Replace the contents of `main.cpp` with the test program below. You can copy the functions `check_int` and `check_text` from lesson 14.3. **Predict** the last line before you run the program.

<details>
<summary>The full test program</summary>

<!-- example: ticket_tests -->
```cpp
#include <iostream>
#include <limits>
#include <sstream>
#include <string>

enum class ReadResult {
    accepted,
    out_of_range,
    invalid_input,
    end_of_input
};

void discard_rest_of_line(std::istream& input) {
    input.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
}

ReadResult read_number(std::istream& input, int minimum, int maximum, int& result) {
    if (input.bad()) {
        return ReadResult::end_of_input;
    }

    input >> std::ws;

    if (input.eof()) {
        return ReadResult::end_of_input;
    }

    int value{0};
    input >> value;

    if (input.fail()) {
        if (input.bad()) {
            return ReadResult::end_of_input;
        }

        input.clear();
        discard_rest_of_line(input);
        return ReadResult::invalid_input;
    }

    discard_rest_of_line(input);

    if (value < minimum || value > maximum) {
        return ReadResult::out_of_range;
    }

    result = value;
    return ReadResult::accepted;
}

std::string read_result_text(ReadResult result) {
    switch (result) {
        case ReadResult::accepted:
            return "accepted";
        case ReadResult::out_of_range:
            return "out_of_range";
        case ReadResult::invalid_input:
            return "invalid_input";
        case ReadResult::end_of_input:
            return "end_of_input";
    }

    return "unknown";
}

void check_read_result(const std::string& name, ReadResult expected, ReadResult actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << read_result_text(expected) << ", actual " << read_result_text(actual) << "\n";
        ++failed;
    }
}

void check_int(const std::string& name, int expected, int actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << expected << ", actual " << actual << "\n";
        ++failed;
    }
}

void check_text(const std::string& name, const std::string& expected, const std::string& actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected \"" << expected << "\", actual \"" << actual << "\"\n";
        ++failed;
    }
}

int main() {
    int checks{0};
    int failed{0};

    check_text("read_result_text(accepted)", "accepted", read_result_text(ReadResult::accepted), checks, failed);
    check_text("read_result_text(out_of_range)", "out_of_range", read_result_text(ReadResult::out_of_range), checks, failed);
    check_text("read_result_text(invalid_input)", "invalid_input", read_result_text(ReadResult::invalid_input), checks, failed);
    check_text("read_result_text(end_of_input)", "end_of_input", read_result_text(ReadResult::end_of_input), checks, failed);

    std::istringstream input_s1{"2\nabc\n5\n"};
    int tickets_s1{-1};
    check_read_result("S1 call 1 result", ReadResult::accepted, read_number(input_s1, 1, 6, tickets_s1), checks, failed);
    check_int("S1 call 1 tickets", 2, tickets_s1, checks, failed);
    check_read_result("S1 call 2 result", ReadResult::invalid_input, read_number(input_s1, 1, 6, tickets_s1), checks, failed);
    check_int("S1 call 2 tickets", 2, tickets_s1, checks, failed);
    check_read_result("S1 call 3 result", ReadResult::accepted, read_number(input_s1, 1, 6, tickets_s1), checks, failed);
    check_int("S1 call 3 tickets", 5, tickets_s1, checks, failed);
    check_read_result("S1 call 4 result", ReadResult::end_of_input, read_number(input_s1, 1, 6, tickets_s1), checks, failed);
    check_int("S1 call 4 tickets", 5, tickets_s1, checks, failed);

    std::istringstream input_s2{"7\n3"};
    int tickets_s2{-1};
    check_read_result("S2 call 1 result", ReadResult::out_of_range, read_number(input_s2, 1, 6, tickets_s2), checks, failed);
    check_int("S2 call 1 tickets", -1, tickets_s2, checks, failed);
    check_read_result("S2 call 2 result", ReadResult::accepted, read_number(input_s2, 1, 6, tickets_s2), checks, failed);
    check_int("S2 call 2 tickets", 3, tickets_s2, checks, failed);
    check_read_result("S2 call 3 result", ReadResult::end_of_input, read_number(input_s2, 1, 6, tickets_s2), checks, failed);
    check_int("S2 call 3 tickets", 3, tickets_s2, checks, failed);

    std::istringstream input_s3{""};
    int tickets_s3{-1};
    check_read_result("S3 call 1 result", ReadResult::end_of_input, read_number(input_s3, 1, 6, tickets_s3), checks, failed);
    check_int("S3 call 1 tickets", -1, tickets_s3, checks, failed);
    check_read_result("S3 call 2 result", ReadResult::end_of_input, read_number(input_s3, 1, 6, tickets_s3), checks, failed);
    check_int("S3 call 2 tickets", -1, tickets_s3, checks, failed);

    std::istringstream input_s4{"4\n999999999999999999999999"};
    int tickets_s4{-1};
    check_read_result("S4 call 1 result", ReadResult::accepted, read_number(input_s4, 1, 6, tickets_s4), checks, failed);
    check_int("S4 call 1 tickets", 4, tickets_s4, checks, failed);
    check_read_result("S4 call 2 result", ReadResult::invalid_input, read_number(input_s4, 1, 6, tickets_s4), checks, failed);
    check_int("S4 call 2 tickets", 4, tickets_s4, checks, failed);
    check_read_result("S4 call 3 result", ReadResult::end_of_input, read_number(input_s4, 1, 6, tickets_s4), checks, failed);
    check_int("S4 call 3 tickets", 4, tickets_s4, checks, failed);

    std::istringstream input_s5{"3 tickets\n5\n"};
    int tickets_s5{-1};
    check_read_result("S5 call 1 result", ReadResult::accepted, read_number(input_s5, 1, 6, tickets_s5), checks, failed);
    check_int("S5 call 1 tickets", 3, tickets_s5, checks, failed);
    check_read_result("S5 call 2 result", ReadResult::accepted, read_number(input_s5, 1, 6, tickets_s5), checks, failed);
    check_int("S5 call 2 tickets", 5, tickets_s5, checks, failed);
    check_read_result("S5 call 3 result", ReadResult::end_of_input, read_number(input_s5, 1, 6, tickets_s5), checks, failed);
    check_int("S5 call 3 tickets", 5, tickets_s5, checks, failed);

    std::cout << "Checks: " << checks << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }
}
```

</details>

<details>
<summary>Standard output</summary>

<!-- output: ticket_tests -->
```text
PASS read_result_text(accepted)
PASS read_result_text(out_of_range)
PASS read_result_text(invalid_input)
PASS read_result_text(end_of_input)
PASS S1 call 1 result
PASS S1 call 1 tickets
PASS S1 call 2 result
PASS S1 call 2 tickets
PASS S1 call 3 result
PASS S1 call 3 tickets
PASS S1 call 4 result
PASS S1 call 4 tickets
PASS S2 call 1 result
PASS S2 call 1 tickets
PASS S2 call 2 result
PASS S2 call 2 tickets
PASS S2 call 3 result
PASS S2 call 3 tickets
PASS S3 call 1 result
PASS S3 call 1 tickets
PASS S3 call 2 result
PASS S3 call 2 tickets
PASS S4 call 1 result
PASS S4 call 1 tickets
PASS S4 call 2 result
PASS S4 call 2 tickets
PASS S4 call 3 result
PASS S4 call 3 tickets
PASS S5 call 1 result
PASS S5 call 1 tickets
PASS S5 call 2 result
PASS S5 call 2 tickets
PASS S5 call 3 result
PASS S5 call 3 tickets
Checks: 34, failed: 0
```

Exit code: 0.

</details>

## 7. Diagnostic: `ignore` without `clear()`

Someone decides that since the bad text has to be removed, discarding it is enough, and leaves out `clear()`:

<!-- fragment -->
```cpp
if (input.fail()) {
    if (input.bad()) {
        return ReadResult::end_of_input;
    }

    discard_rest_of_line(input);
    return ReadResult::invalid_input;
}
```

**This is the third required run.** Follow the steps in order:

1. **Predict** from the scenario table of section 6: which scenario will notice it? Which calls will give `FAIL`, and what will follow `actual`?
2. In the test program of section 6, delete the line `input.clear();` in `read_number`. Change nothing else, neither the tests nor the expected results.
3. Run the tests. Write down the `FAIL` lines, the summary and the exit code.
4. Restore `input.clear();` and run the same tests again.

**Don't run the program of section 5 with this bug.** After the first bad entry it would print `Not a whole number, try again` forever, and you'd have to stop it with the **Stop** button. The test program calls the function a fixed number of times, so it always ends.

<details>
<summary>What happens and how to fix it: open after steps 1–4</summary>

The test program with this change, and no other change:

<!-- example: ticket_tests_no_clear exit=1 -->
```cpp
#include <iostream>
#include <limits>
#include <sstream>
#include <string>

enum class ReadResult {
    accepted,
    out_of_range,
    invalid_input,
    end_of_input
};

void discard_rest_of_line(std::istream& input) {
    input.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
}

ReadResult read_number(std::istream& input, int minimum, int maximum, int& result) {
    if (input.bad()) {
        return ReadResult::end_of_input;
    }

    input >> std::ws;

    if (input.eof()) {
        return ReadResult::end_of_input;
    }

    int value{0};
    input >> value;

    if (input.fail()) {
        if (input.bad()) {
            return ReadResult::end_of_input;
        }

        discard_rest_of_line(input);
        return ReadResult::invalid_input;
    }

    discard_rest_of_line(input);

    if (value < minimum || value > maximum) {
        return ReadResult::out_of_range;
    }

    result = value;
    return ReadResult::accepted;
}

std::string read_result_text(ReadResult result) {
    switch (result) {
        case ReadResult::accepted:
            return "accepted";
        case ReadResult::out_of_range:
            return "out_of_range";
        case ReadResult::invalid_input:
            return "invalid_input";
        case ReadResult::end_of_input:
            return "end_of_input";
    }

    return "unknown";
}

void check_read_result(const std::string& name, ReadResult expected, ReadResult actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << read_result_text(expected) << ", actual " << read_result_text(actual) << "\n";
        ++failed;
    }
}

void check_int(const std::string& name, int expected, int actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << expected << ", actual " << actual << "\n";
        ++failed;
    }
}

void check_text(const std::string& name, const std::string& expected, const std::string& actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected \"" << expected << "\", actual \"" << actual << "\"\n";
        ++failed;
    }
}

int main() {
    int checks{0};
    int failed{0};

    check_text("read_result_text(accepted)", "accepted", read_result_text(ReadResult::accepted), checks, failed);
    check_text("read_result_text(out_of_range)", "out_of_range", read_result_text(ReadResult::out_of_range), checks, failed);
    check_text("read_result_text(invalid_input)", "invalid_input", read_result_text(ReadResult::invalid_input), checks, failed);
    check_text("read_result_text(end_of_input)", "end_of_input", read_result_text(ReadResult::end_of_input), checks, failed);

    std::istringstream input_s1{"2\nabc\n5\n"};
    int tickets_s1{-1};
    check_read_result("S1 call 1 result", ReadResult::accepted, read_number(input_s1, 1, 6, tickets_s1), checks, failed);
    check_int("S1 call 1 tickets", 2, tickets_s1, checks, failed);
    check_read_result("S1 call 2 result", ReadResult::invalid_input, read_number(input_s1, 1, 6, tickets_s1), checks, failed);
    check_int("S1 call 2 tickets", 2, tickets_s1, checks, failed);
    check_read_result("S1 call 3 result", ReadResult::accepted, read_number(input_s1, 1, 6, tickets_s1), checks, failed);
    check_int("S1 call 3 tickets", 5, tickets_s1, checks, failed);
    check_read_result("S1 call 4 result", ReadResult::end_of_input, read_number(input_s1, 1, 6, tickets_s1), checks, failed);
    check_int("S1 call 4 tickets", 5, tickets_s1, checks, failed);

    std::istringstream input_s2{"7\n3"};
    int tickets_s2{-1};
    check_read_result("S2 call 1 result", ReadResult::out_of_range, read_number(input_s2, 1, 6, tickets_s2), checks, failed);
    check_int("S2 call 1 tickets", -1, tickets_s2, checks, failed);
    check_read_result("S2 call 2 result", ReadResult::accepted, read_number(input_s2, 1, 6, tickets_s2), checks, failed);
    check_int("S2 call 2 tickets", 3, tickets_s2, checks, failed);
    check_read_result("S2 call 3 result", ReadResult::end_of_input, read_number(input_s2, 1, 6, tickets_s2), checks, failed);
    check_int("S2 call 3 tickets", 3, tickets_s2, checks, failed);

    std::istringstream input_s3{""};
    int tickets_s3{-1};
    check_read_result("S3 call 1 result", ReadResult::end_of_input, read_number(input_s3, 1, 6, tickets_s3), checks, failed);
    check_int("S3 call 1 tickets", -1, tickets_s3, checks, failed);
    check_read_result("S3 call 2 result", ReadResult::end_of_input, read_number(input_s3, 1, 6, tickets_s3), checks, failed);
    check_int("S3 call 2 tickets", -1, tickets_s3, checks, failed);

    std::istringstream input_s4{"4\n999999999999999999999999"};
    int tickets_s4{-1};
    check_read_result("S4 call 1 result", ReadResult::accepted, read_number(input_s4, 1, 6, tickets_s4), checks, failed);
    check_int("S4 call 1 tickets", 4, tickets_s4, checks, failed);
    check_read_result("S4 call 2 result", ReadResult::invalid_input, read_number(input_s4, 1, 6, tickets_s4), checks, failed);
    check_int("S4 call 2 tickets", 4, tickets_s4, checks, failed);
    check_read_result("S4 call 3 result", ReadResult::end_of_input, read_number(input_s4, 1, 6, tickets_s4), checks, failed);
    check_int("S4 call 3 tickets", 4, tickets_s4, checks, failed);

    std::istringstream input_s5{"3 tickets\n5\n"};
    int tickets_s5{-1};
    check_read_result("S5 call 1 result", ReadResult::accepted, read_number(input_s5, 1, 6, tickets_s5), checks, failed);
    check_int("S5 call 1 tickets", 3, tickets_s5, checks, failed);
    check_read_result("S5 call 2 result", ReadResult::accepted, read_number(input_s5, 1, 6, tickets_s5), checks, failed);
    check_int("S5 call 2 tickets", 5, tickets_s5, checks, failed);
    check_read_result("S5 call 3 result", ReadResult::end_of_input, read_number(input_s5, 1, 6, tickets_s5), checks, failed);
    check_int("S5 call 3 tickets", 5, tickets_s5, checks, failed);

    std::cout << "Checks: " << checks << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }
}
```

<!-- output: ticket_tests_no_clear -->
```text
PASS read_result_text(accepted)
PASS read_result_text(out_of_range)
PASS read_result_text(invalid_input)
PASS read_result_text(end_of_input)
PASS S1 call 1 result
PASS S1 call 1 tickets
PASS S1 call 2 result
PASS S1 call 2 tickets
FAIL S1 call 3 result: expected accepted, actual invalid_input
FAIL S1 call 3 tickets: expected 5, actual 2
FAIL S1 call 4 result: expected end_of_input, actual invalid_input
FAIL S1 call 4 tickets: expected 5, actual 2
PASS S2 call 1 result
PASS S2 call 1 tickets
PASS S2 call 2 result
PASS S2 call 2 tickets
PASS S2 call 3 result
PASS S2 call 3 tickets
PASS S3 call 1 result
PASS S3 call 1 tickets
PASS S3 call 2 result
PASS S3 call 2 tickets
PASS S4 call 1 result
PASS S4 call 1 tickets
PASS S4 call 2 result
PASS S4 call 2 tickets
PASS S4 call 3 result
PASS S4 call 3 tickets
PASS S5 call 1 result
PASS S5 call 1 tickets
PASS S5 call 2 result
PASS S5 call 2 tickets
PASS S5 call 3 result
PASS S5 call 3 tickets
Checks: 34, failed: 4
```

Exit code: 1. It comes from four real `FAIL` lines: `main` returns 1 because `failed` is greater than 0.

| Scenario | What happens | `FAIL` checks |
|---|---|---|
| S1 | call 2 correctly reports `invalid_input`, but the stream stays in the error state; `ignore` takes nothing, so calls 3 and 4 meet the same error again | the result and `tickets` in calls 3 and 4 |
| S4 | the failed read of the too large number reaches the end of the data, so the next call finds the end anyway | none |
| S2, S3, S5 | there's no failed read in them | none |

- **`ignore` on a stream in the error state does nothing.** The read in call 3 meets the same `abc`. The stream never leaves the error state, so the function never gets to `5`.
- **The result of call 2 is correct.** The bug shows only in the next calls on the same stream. A test of a single call, as in lesson 13.3, wouldn't notice it.
- **In a program with a loop** every call would return `invalid_input`, and `end_of_input` would never come.

**The fix:** restore `input.clear();` before discarding the rest of the line. The same tests, with the same expected results, print `PASS` 34 times and `Checks: 34, failed: 0`, and the exit code is 0.

</details>

### Optional: the end of the data checked too late

Only read this variant and predict its effect. Someone moves the `eof()` check after the read of the number:

<!-- fragment -->
```cpp
input >> std::ws;

int value{0};
input >> value;

if (input.eof()) {
    return ReadResult::end_of_input;
}
```

**Predict:** which scenario of section 6 will lose a number, and which a bad entry?

<details>
<summary>The answer and the program that checks it</summary>

- **S2:** `3` is the last character of the data. The read gives 3 and reaches the end, so `eof()` gives `true` and the function returns `end_of_input`. The valid number is lost, and `tickets` stays −1. That's the trap from lesson 4.6.
- **S4:** the failed read of the too large number reaches the end too. The function returns `end_of_input` instead of `invalid_input`, so the last bad entry vanishes.
- **S1, S3, S5:** unchanged, because none of their reads of a number ends at the very end of the data.

<!-- example: ticket_tests_eof_after exit=1 -->
```cpp
#include <iostream>
#include <limits>
#include <sstream>
#include <string>

enum class ReadResult {
    accepted,
    out_of_range,
    invalid_input,
    end_of_input
};

void discard_rest_of_line(std::istream& input) {
    input.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
}

ReadResult read_number(std::istream& input, int minimum, int maximum, int& result) {
    if (input.bad()) {
        return ReadResult::end_of_input;
    }

    input >> std::ws;

    int value{0};
    input >> value;

    if (input.eof()) {
        return ReadResult::end_of_input;
    }

    if (input.fail()) {
        if (input.bad()) {
            return ReadResult::end_of_input;
        }

        input.clear();
        discard_rest_of_line(input);
        return ReadResult::invalid_input;
    }

    discard_rest_of_line(input);

    if (value < minimum || value > maximum) {
        return ReadResult::out_of_range;
    }

    result = value;
    return ReadResult::accepted;
}

std::string read_result_text(ReadResult result) {
    switch (result) {
        case ReadResult::accepted:
            return "accepted";
        case ReadResult::out_of_range:
            return "out_of_range";
        case ReadResult::invalid_input:
            return "invalid_input";
        case ReadResult::end_of_input:
            return "end_of_input";
    }

    return "unknown";
}

void check_read_result(const std::string& name, ReadResult expected, ReadResult actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << read_result_text(expected) << ", actual " << read_result_text(actual) << "\n";
        ++failed;
    }
}

void check_int(const std::string& name, int expected, int actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << expected << ", actual " << actual << "\n";
        ++failed;
    }
}

void check_text(const std::string& name, const std::string& expected, const std::string& actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected \"" << expected << "\", actual \"" << actual << "\"\n";
        ++failed;
    }
}

int main() {
    int checks{0};
    int failed{0};

    check_text("read_result_text(accepted)", "accepted", read_result_text(ReadResult::accepted), checks, failed);
    check_text("read_result_text(out_of_range)", "out_of_range", read_result_text(ReadResult::out_of_range), checks, failed);
    check_text("read_result_text(invalid_input)", "invalid_input", read_result_text(ReadResult::invalid_input), checks, failed);
    check_text("read_result_text(end_of_input)", "end_of_input", read_result_text(ReadResult::end_of_input), checks, failed);

    std::istringstream input_s1{"2\nabc\n5\n"};
    int tickets_s1{-1};
    check_read_result("S1 call 1 result", ReadResult::accepted, read_number(input_s1, 1, 6, tickets_s1), checks, failed);
    check_int("S1 call 1 tickets", 2, tickets_s1, checks, failed);
    check_read_result("S1 call 2 result", ReadResult::invalid_input, read_number(input_s1, 1, 6, tickets_s1), checks, failed);
    check_int("S1 call 2 tickets", 2, tickets_s1, checks, failed);
    check_read_result("S1 call 3 result", ReadResult::accepted, read_number(input_s1, 1, 6, tickets_s1), checks, failed);
    check_int("S1 call 3 tickets", 5, tickets_s1, checks, failed);
    check_read_result("S1 call 4 result", ReadResult::end_of_input, read_number(input_s1, 1, 6, tickets_s1), checks, failed);
    check_int("S1 call 4 tickets", 5, tickets_s1, checks, failed);

    std::istringstream input_s2{"7\n3"};
    int tickets_s2{-1};
    check_read_result("S2 call 1 result", ReadResult::out_of_range, read_number(input_s2, 1, 6, tickets_s2), checks, failed);
    check_int("S2 call 1 tickets", -1, tickets_s2, checks, failed);
    check_read_result("S2 call 2 result", ReadResult::accepted, read_number(input_s2, 1, 6, tickets_s2), checks, failed);
    check_int("S2 call 2 tickets", 3, tickets_s2, checks, failed);
    check_read_result("S2 call 3 result", ReadResult::end_of_input, read_number(input_s2, 1, 6, tickets_s2), checks, failed);
    check_int("S2 call 3 tickets", 3, tickets_s2, checks, failed);

    std::istringstream input_s3{""};
    int tickets_s3{-1};
    check_read_result("S3 call 1 result", ReadResult::end_of_input, read_number(input_s3, 1, 6, tickets_s3), checks, failed);
    check_int("S3 call 1 tickets", -1, tickets_s3, checks, failed);
    check_read_result("S3 call 2 result", ReadResult::end_of_input, read_number(input_s3, 1, 6, tickets_s3), checks, failed);
    check_int("S3 call 2 tickets", -1, tickets_s3, checks, failed);

    std::istringstream input_s4{"4\n999999999999999999999999"};
    int tickets_s4{-1};
    check_read_result("S4 call 1 result", ReadResult::accepted, read_number(input_s4, 1, 6, tickets_s4), checks, failed);
    check_int("S4 call 1 tickets", 4, tickets_s4, checks, failed);
    check_read_result("S4 call 2 result", ReadResult::invalid_input, read_number(input_s4, 1, 6, tickets_s4), checks, failed);
    check_int("S4 call 2 tickets", 4, tickets_s4, checks, failed);
    check_read_result("S4 call 3 result", ReadResult::end_of_input, read_number(input_s4, 1, 6, tickets_s4), checks, failed);
    check_int("S4 call 3 tickets", 4, tickets_s4, checks, failed);

    std::istringstream input_s5{"3 tickets\n5\n"};
    int tickets_s5{-1};
    check_read_result("S5 call 1 result", ReadResult::accepted, read_number(input_s5, 1, 6, tickets_s5), checks, failed);
    check_int("S5 call 1 tickets", 3, tickets_s5, checks, failed);
    check_read_result("S5 call 2 result", ReadResult::accepted, read_number(input_s5, 1, 6, tickets_s5), checks, failed);
    check_int("S5 call 2 tickets", 5, tickets_s5, checks, failed);
    check_read_result("S5 call 3 result", ReadResult::end_of_input, read_number(input_s5, 1, 6, tickets_s5), checks, failed);
    check_int("S5 call 3 tickets", 5, tickets_s5, checks, failed);

    std::cout << "Checks: " << checks << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }
}
```

<!-- output: ticket_tests_eof_after -->
```text
PASS read_result_text(accepted)
PASS read_result_text(out_of_range)
PASS read_result_text(invalid_input)
PASS read_result_text(end_of_input)
PASS S1 call 1 result
PASS S1 call 1 tickets
PASS S1 call 2 result
PASS S1 call 2 tickets
PASS S1 call 3 result
PASS S1 call 3 tickets
PASS S1 call 4 result
PASS S1 call 4 tickets
PASS S2 call 1 result
PASS S2 call 1 tickets
FAIL S2 call 2 result: expected accepted, actual end_of_input
FAIL S2 call 2 tickets: expected 3, actual -1
PASS S2 call 3 result
FAIL S2 call 3 tickets: expected 3, actual -1
PASS S3 call 1 result
PASS S3 call 1 tickets
PASS S3 call 2 result
PASS S3 call 2 tickets
PASS S4 call 1 result
PASS S4 call 1 tickets
FAIL S4 call 2 result: expected invalid_input, actual end_of_input
PASS S4 call 2 tickets
PASS S4 call 3 result
PASS S4 call 3 tickets
PASS S5 call 1 result
PASS S5 call 1 tickets
PASS S5 call 2 result
PASS S5 call 2 tickets
PASS S5 call 3 result
PASS S5 call 3 tickets
Checks: 34, failed: 4
```

Exit code: 1.

</details>

## 8. Mission: survey ratings

After a workshop the participants rate it on a scale from 1 to 5. The ratings reach the program as successive entries, one per line. Mistakes happen: an empty line, text instead of a number, a number off the scale. Your task is a function that goes through all the entries and counts what was in them, and a test program that checks it together with the reading function.

`read_number` stays as in the demonstration. What's new is a function that calls it until the end of the data:

<!-- fragment -->
```cpp
struct SurveyCounts {
    int accepted;
    int out_of_range;
    int invalid_input;
    int sum;
};

SurveyCounts count_ratings(std::istream& input);
```

**The contract of `count_ratings`:**

- it calls `read_number` with the range 1–5 until it gets `end_of_input`;
- on `accepted` it increases `accepted` by 1 and adds the rating read to `sum`;
- on `out_of_range` it increases `out_of_range` by 1;
- on `invalid_input` it increases `invalid_input` by 1;
- on `end_of_input` it stops: the end of the data itself isn't a refusal and isn't counted;
- refusals don't change `sum`;
- it prints nothing and returns the counts.

The first three fields of `SurveyCounts` have the same names as the results they count, and `sum` is the sum of the accepted ratings. You don't compute an average.

**Rules:**

- Copy `ReadResult`, `discard_rest_of_line`, `read_number`, `read_result_text` and `check_read_result` from section 6 without changes, and `check_int` from lesson 14.3.
- Every scenario has its own `std::istringstream`. Within a scenario, the successive calls use the same stream.
- Two kinds of scenarios. **Reading scenarios** call `read_number` with the range 1–5 and check the result and the rating after every call. **Counting scenarios** call `count_ratings` and check all four fields.
- The rating variable starts every reading scenario at a value outside the range and different from 0, for example −1.

Create a folder `survey_ratings` in `cpp-workspace`, copy `main.cpp` and `CMakeLists.txt` into it from the original `lesson_05_first_program`, and open it in CLion. Write everything in one file, `main.cpp`. Leave `CMakeLists.txt` unchanged.

**Order of work:**

1. **First the scenario table.** Before you write code, list the scenarios with their data and the expected results derived from the contract. The table must contain at least:
   - an accepted rating;
   - a refusal because of the range, with the rating unchanged;
   - a bad entry followed by a valid one;
   - two bad entries in a row;
   - a last valid rating without a line end;
   - a last bad entry without a line end;
   - an unchanged rating after a bad entry;
   - a counting scenario with mixed entries and an empty line;
   - a counting scenario without data.

   Below the table, write down a prediction: which checks will fail when `read_number` starts to read straight into `result` instead of into a local variable? Will the counting scenarios notice it?
2. Define `SurveyCounts` and write `count_ratings`.
3. Write the test program: the checks from your table, and at the end the summary and the exit code as in section 6.
4. **This is the fourth required run:** run the test program. Every check should print `PASS`, and the exit code should be 0.
5. **A deliberate bug.** In `read_number`, write `input >> result;` instead of `int value{0};` and `input >> value;`, use `result` instead of `value` in the range check, and delete the line `result = value;`. Don't change the tests or the expected results. **This is the fifth required run:** run the tests, write down the `FAIL` lines, the summary and the exit code, and compare them with your prediction from step 1. Then restore the local variable and run the same tests again.

If you want, also write a program that reads ratings from the keyboard with `count_ratings(std::cin)` and prints the counts. This step is optional, and an example is in the sample solution.

### Success criteria

- [ ] The program builds as C++20, and `CMakeLists.txt` is as in lesson 0.5.
- [ ] `read_number` is as in section 6 and is called with the range 1–5.
- [ ] `SurveyCounts` has the fields `accepted`, `out_of_range`, `invalid_input` and `sum`.
- [ ] `count_ratings` gets the stream through `std::istream&`, calls `read_number` in a loop and handles the four results with a `switch` statement with a label for each of them.
- [ ] The loop ends after `end_of_input`, and the end of the data isn't counted as a refusal.
- [ ] Only accepted ratings go into `sum`. `count_ratings` prints nothing.
- [ ] The scenario table was made before the code, has every required kind, and has expected results from the contract.
- [ ] Every scenario has its own stream, and the successive calls within a scenario use the same stream.
- [ ] The reading scenarios check the result and the rating after every call. The rating starts at a value outside the range and different from 0.
- [ ] The counting scenarios check all four fields of `SurveyCounts`.
- [ ] With the correct function every check passes, and the exit code is 0.
- [ ] With the deliberate bug, the checks of the rating after refusals print `FAIL`, and the exit code is 1. The result matches your prediction, or you can explain the difference.
- [ ] After the local variable is restored, the same tests, unchanged, pass again with exit code 0.

When the result matches, you can save the project in Git, as in lesson 1.5: `main.cpp` and `CMakeLists.txt`, without the build folder.

<details>
<summary>Hint 1: named results</summary>

What does `read_number` return after a valid read, what after each of the two refusals, and what when there's no data left? Which of these results changes which counter, and which ends the loop? Does any result need something added to the sum?

</details>

<details>
<summary>Hint 2: recovering</summary>

Why isn't `clear()` without discarding the rest of the line enough? What would reach the next call if only the error state were removed after `abc`? Which of your scenarios shows that the valid entry after a bad one really is read?

</details>

<details>
<summary>Hint 3: the end of the data and staying unchanged</summary>

When should the loop in `count_ratings` end, and why isn't the end of the data a refusal? How do you check that the rating after a refusal has the same value as before the call? What value should the rating start at so that every change shows? Are the counts alone enough to check this?

</details>

<details>
<summary>The full list of control scenarios: open after making your own table</summary>

Reading scenarios, range 1–5, the rating −1 at the start:

| Scenario | Data | Successive calls: the result and the rating after it | What it checks |
|---|---|---|---|
| R1 | `"abc\n4\n"` | `invalid_input` −1; `accepted` 4; `end_of_input` 4 | a bad entry, then a valid one; the rating unchanged after the bad entry |
| R2 | `"0\n6\n1"` | `out_of_range` −1; `out_of_range` −1; `accepted` 1; `end_of_input` 1 | the numbers just past both bounds; the lowest rating accepted; the last valid rating without a line end |
| R3 | `"2\nxyz"` | `accepted` 2; `invalid_input` 2; `end_of_input` 2 | the last bad entry without a line end; the rating unchanged after an earlier accepted one |

Counting scenarios:

| Scenario | Data | `accepted` | `out_of_range` | `invalid_input` | `sum` | What it checks |
|---|---|---:|---:|---:|---:|---|
| C1 | `"5\n\nabc\nxyz\n0\n3 stars\n4"` | 3 | 1 | 2 | 12 | every kind of result, an empty line, two bad entries in a row, a numeric prefix, the last rating without a line end |
| C2 | `""` | 0 | 0 | 0 | 0 | no data: the end of the data isn't a refusal |

Your table doesn't have to have exactly these scenarios. It must have every kind listed in step 1 of the mission.

</details>

The sample solution is in [Sample solutions](#sample-solutions).

## 9. When something goes differently

| What you see | What it means | What to do |
|---|---|---|
| The same message about a bad entry repeats forever | After a failed read, `clear()` or discarding the rest of the line is missing, so the next attempt meets the same text (sections 1 and 7). | Stop the program with the **Stop** button. After a failed read, call `clear()` and then discard the rest of the line. |
| The mission's test program doesn't end | The loop in `count_ratings` waits for `end_of_input`, and for the same reason as above every attempt gives `invalid_input`. | Stop the program and check the recovery in `read_number`. |
| The last number without a line end gives `end_of_input` instead of `accepted` | The function checks `eof()` after reading the number (section 7, the optional variant). | Check the end of the data before reading the number, after `input >> std::ws`. |
| The last bad entry without a line end gives `end_of_input` instead of `invalid_input` | The function recognises the end of the data after a failed read (section 3). | As above: the end of the data before the read, and only `fail()` after it. |
| After a refusal the result variable has another value, for example 0 | The read goes straight into `result`, or the assignment stands before the range check. | Read into a local variable and assign only on `accepted`. |
| `3 tickets` gives two results: `accepted` and `invalid_input` | After a successful read, discarding the rest of the line is missing, so ` tickets` goes into the next attempt. | Call `discard_rest_of_line(input);` after a successful read too. |
| `abc` gives three `invalid_input` results | `ignore()` without arguments takes only one character. | Use the full form with `std::numeric_limits<std::streamsize>::max()` and `'\n'`. |
| `3.5` is accepted as 3 | That's how this function works: it reads the number at the start of the entry and discards the rest of the line (section 4). | That's intended. A strict check of the whole entry isn't part of this lesson. |
| An empty line gives no message | `std::ws` skips empty lines, so they aren't attempts. | That's intended. |
| An error with `use of undeclared identifier 'ws'; did you mean 'std::ws'?` | `std::` is missing before `ws`. | Write `input >> std::ws;`. |
| A warning with `enumeration value '…' not handled in switch` | A label for one of the four results is missing in the `switch` (lesson 14.2). | Add the label. |

## 10. Explain

Answer in your own words, preferably in writing. Only then compare with the sample answers.

1. What does `clear()` repair, and what doesn't it repair?
2. Why does a failed read need both `clear()` and discarding the rest of the line? What happens when one of them is missing?
3. What does `std::numeric_limits<std::streamsize>::max()` mean in the call of `ignore`, and why isn't `ignore()` without arguments enough?
4. How does `input >> std::ws` differ from discarding the rest of the line?
5. Why does the function recognise the end of the data before reading the number, and not after it?
6. The data ends with `4` and no line end. Why isn't that an error, and what will two more calls return?
7. The data ends with `abc` and no line end. Why does the function report `invalid_input`, and not `end_of_input` straight away?
8. Why does `12abc` give `out_of_range`, and `3.5` give `accepted`? Does the function check the whole entry?
9. Why does a number too large for `int` give `invalid_input`, and not `out_of_range`?
10. Why does the function read into a local variable, and why does a test scenario start at −1 and not at 0?
11. Why does every test scenario have its own stream, while the successive calls within a scenario use the same one?
12. In the mission, reading straight into `result` didn't change any counter. Why didn't the counting tests detect it, and what did?

<details>
<summary>Sample answers</summary>

1. It repairs the stream state: it removes the flag of a failed read, so further reads can succeed again. It removes no character, creates no data and changes no variable. The bad text still waits in the input.
2. Because there are two obstacles: the error state and the bad text. Without `clear()` the stream stays in the error state, and `ignore` takes nothing, so every read fails at once. Without discarding the rest of the line the state is normal, but the next read meets the same text. In both cases a program with a loop would repeat the same message forever.
3. It's the largest value of the type the library uses to count characters. For `ignore` this value means no limit, so `ignore` takes characters up to the end of the line or the end of the data. `ignore()` without arguments takes one character: after `abc`, `bc` is left, and the next attempts meet the next letters.
4. `std::ws` removes only the whitespace before an entry, empty lines included, and stops at the first other character. Discarding the rest of the line removes all characters up to the end of the current line, bad text included. `std::ws` stands at the start of every attempt, and discarding the rest of the line after every attempt that found an entry.
5. Because after the read `eof()` doesn't say whether the read succeeded. A successful read of the last number without a line end also reaches the end of the data, and a failed read that reached the end looks the same as no data. Before the read, after `std::ws`, `eof()` answers one question: is there another entry?
6. Because `>>` reads 4 and only then reaches the end of the data. `fail()` gives `false`, so the read succeeded, and `eof()` only says there's nothing after it. The first call returns `accepted` with the value 4, the next one `end_of_input`, and the one after that `end_of_input` again.
7. Because `abc` is an entry, only a bad one. Reading the number stops at `a` and doesn't reach the end of the data, so the function recovers the stream and reports `invalid_input`. Only discarding the rest of the line reaches the end. If the function reported the end of the data straight away, the last bad entry would vanish and nobody would learn about it.
8. Because the function reads the number at the start of the entry and discards the rest of the line without checking it. From `12abc` it reads 12, and that's out of the range 1–6. From `3.5` it reads 3 and discards `.5`. The function doesn't check whether the whole entry is a single number.
9. Because the read of such a number fails. `out_of_range` means that the number read is known, it just lies outside the range. The function never gets a number too large for `int`, so it can't judge its range.
10. Because a failed read may store a different value in the variable, and a read of a number out of the range stores that number. The local variable protects `result`, which must change only on `accepted`. Starting at −1 makes every change after a refusal visible. With 0, a change to 0 after a failed read, for example in the mission's variant, would go unnoticed.
11. Because the scenarios are independent of each other: each starts from its own data, and the result of one mustn't depend on what the previous one did. Within a scenario the calls aren't independent: they check whether after every entry the stream is ready for the next one. That's why they use the same stream, like a program that reads successive entries.
12. Because the counts depend only on the named results, and only accepted ratings go into the sum. The results were correct, and so were the accepted ratings. The change affected only the rating after refusals, which `count_ratings` doesn't use. The checks of the rating in the reading scenarios, which call `read_number` directly, detected it.

</details>

## Summary

- A failed read leaves two obstacles: the error state and the bad text. **`clear()` repairs the state, and `ignore` removes characters.** Both are needed, `clear()` first.
- `input.ignore(std::numeric_limits<std::streamsize>::max(), '\n');` discards the remaining characters up to the end of the line or the end of the data. It needs `#include <limits>`.
- **You recognise the end of the data before reading the number:** `input >> std::ws;` skips whitespace and empty lines, and `eof()` says whether there's another entry. After reading the number you only check whether the read succeeded. The last number without a line end is accepted, and the last bad entry without one is reported.
- The function `read_number` returns one of four named results, recovers the stream by itself and changes `result` only on `accepted`. It reads the number at the start of the entry and discards the rest of the line without checking it. A number too large for `int` is `invalid_input`.
- A failure of the data source isn't the end of the data. The function assumes a working source, and on a failure it stops reading, without recovery.
- Sequence tests: every scenario has a new stream, and within a scenario the successive calls use the same one. After every call you check the result and the value of the result variable, and the variable starts at a value that no valid read gives.

## What's next

This was the last lesson of Module 14 with new skills. The planned lesson 14.5 is the module test: a measuring-station program in which you combine named states, `switch`, named results and reading that recovers the stream. That lesson is in preparation.

---

## Sample solutions

Look here **after your own attempt**. Your check names, variable names, choice of scenarios and their order may differ, as long as they meet the contract and the checklist.

<details>
<summary>Section 8: the mission, survey ratings</summary>

**`count_ratings`:** the loop runs until `end_of_input` comes. Each result is handled by its own `case` label, ended by `break`. A rating goes into the sum only in the label `accepted`. `end_of_input` sets the flag `input_ended` and counts nothing. The rating goes into the variable `rating`, which only `read_number` changes, and only on `accepted`.

**Scenarios:** the reference program has three reading scenarios, R1–R3, with 10 calls and 2 checks each, so 20, and two counting scenarios, C1 and C2, with 4 checks each, so 8. 28 in total.

**The prediction:** when reading straight into `result`, the named results don't change, but the rating after refusals does. After a failed read the C++ standard requires 0 to be stored in the variable, and after a read of a number out of the range that number stays in it. `FAIL` comes from the checks of the rating in R1 after `abc`, in R2 after `0` and after `6`, and in R3 after `xyz` and after the end of the data. The counting scenarios pass.

**`main.cpp`:**

<!-- example: survey_tests -->
```cpp
#include <iostream>
#include <limits>
#include <sstream>
#include <string>

enum class ReadResult {
    accepted,
    out_of_range,
    invalid_input,
    end_of_input
};

void discard_rest_of_line(std::istream& input) {
    input.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
}

ReadResult read_number(std::istream& input, int minimum, int maximum, int& result) {
    if (input.bad()) {
        return ReadResult::end_of_input;
    }

    input >> std::ws;

    if (input.eof()) {
        return ReadResult::end_of_input;
    }

    int value{0};
    input >> value;

    if (input.fail()) {
        if (input.bad()) {
            return ReadResult::end_of_input;
        }

        input.clear();
        discard_rest_of_line(input);
        return ReadResult::invalid_input;
    }

    discard_rest_of_line(input);

    if (value < minimum || value > maximum) {
        return ReadResult::out_of_range;
    }

    result = value;
    return ReadResult::accepted;
}

std::string read_result_text(ReadResult result) {
    switch (result) {
        case ReadResult::accepted:
            return "accepted";
        case ReadResult::out_of_range:
            return "out_of_range";
        case ReadResult::invalid_input:
            return "invalid_input";
        case ReadResult::end_of_input:
            return "end_of_input";
    }

    return "unknown";
}

struct SurveyCounts {
    int accepted;
    int out_of_range;
    int invalid_input;
    int sum;
};

SurveyCounts count_ratings(std::istream& input) {
    SurveyCounts counts{0, 0, 0, 0};
    int rating{0};
    bool input_ended{false};

    while (!input_ended) {
        const ReadResult result{read_number(input, 1, 5, rating)};

        switch (result) {
            case ReadResult::accepted:
                ++counts.accepted;
                counts.sum += rating;
                break;
            case ReadResult::out_of_range:
                ++counts.out_of_range;
                break;
            case ReadResult::invalid_input:
                ++counts.invalid_input;
                break;
            case ReadResult::end_of_input:
                input_ended = true;
                break;
        }
    }

    return counts;
}

void check_read_result(const std::string& name, ReadResult expected, ReadResult actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << read_result_text(expected) << ", actual " << read_result_text(actual) << "\n";
        ++failed;
    }
}

void check_int(const std::string& name, int expected, int actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << expected << ", actual " << actual << "\n";
        ++failed;
    }
}

int main() {
    int checks{0};
    int failed{0};

    std::istringstream input_r1{"abc\n4\n"};
    int rating_r1{-1};
    check_read_result("R1 call 1 result", ReadResult::invalid_input, read_number(input_r1, 1, 5, rating_r1), checks, failed);
    check_int("R1 call 1 rating", -1, rating_r1, checks, failed);
    check_read_result("R1 call 2 result", ReadResult::accepted, read_number(input_r1, 1, 5, rating_r1), checks, failed);
    check_int("R1 call 2 rating", 4, rating_r1, checks, failed);
    check_read_result("R1 call 3 result", ReadResult::end_of_input, read_number(input_r1, 1, 5, rating_r1), checks, failed);
    check_int("R1 call 3 rating", 4, rating_r1, checks, failed);

    std::istringstream input_r2{"0\n6\n1"};
    int rating_r2{-1};
    check_read_result("R2 call 1 result", ReadResult::out_of_range, read_number(input_r2, 1, 5, rating_r2), checks, failed);
    check_int("R2 call 1 rating", -1, rating_r2, checks, failed);
    check_read_result("R2 call 2 result", ReadResult::out_of_range, read_number(input_r2, 1, 5, rating_r2), checks, failed);
    check_int("R2 call 2 rating", -1, rating_r2, checks, failed);
    check_read_result("R2 call 3 result", ReadResult::accepted, read_number(input_r2, 1, 5, rating_r2), checks, failed);
    check_int("R2 call 3 rating", 1, rating_r2, checks, failed);
    check_read_result("R2 call 4 result", ReadResult::end_of_input, read_number(input_r2, 1, 5, rating_r2), checks, failed);
    check_int("R2 call 4 rating", 1, rating_r2, checks, failed);

    std::istringstream input_r3{"2\nxyz"};
    int rating_r3{-1};
    check_read_result("R3 call 1 result", ReadResult::accepted, read_number(input_r3, 1, 5, rating_r3), checks, failed);
    check_int("R3 call 1 rating", 2, rating_r3, checks, failed);
    check_read_result("R3 call 2 result", ReadResult::invalid_input, read_number(input_r3, 1, 5, rating_r3), checks, failed);
    check_int("R3 call 2 rating", 2, rating_r3, checks, failed);
    check_read_result("R3 call 3 result", ReadResult::end_of_input, read_number(input_r3, 1, 5, rating_r3), checks, failed);
    check_int("R3 call 3 rating", 2, rating_r3, checks, failed);

    std::istringstream input_c1{"5\n\nabc\nxyz\n0\n3 stars\n4"};
    const SurveyCounts counts_c1{count_ratings(input_c1)};
    check_int("C1 accepted", 3, counts_c1.accepted, checks, failed);
    check_int("C1 out_of_range", 1, counts_c1.out_of_range, checks, failed);
    check_int("C1 invalid_input", 2, counts_c1.invalid_input, checks, failed);
    check_int("C1 sum", 12, counts_c1.sum, checks, failed);

    std::istringstream input_c2{""};
    const SurveyCounts counts_c2{count_ratings(input_c2)};
    check_int("C2 accepted", 0, counts_c2.accepted, checks, failed);
    check_int("C2 out_of_range", 0, counts_c2.out_of_range, checks, failed);
    check_int("C2 invalid_input", 0, counts_c2.invalid_input, checks, failed);
    check_int("C2 sum", 0, counts_c2.sum, checks, failed);

    std::cout << "Checks: " << checks << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }
}
```

<!-- output: survey_tests -->
```text
PASS R1 call 1 result
PASS R1 call 1 rating
PASS R1 call 2 result
PASS R1 call 2 rating
PASS R1 call 3 result
PASS R1 call 3 rating
PASS R2 call 1 result
PASS R2 call 1 rating
PASS R2 call 2 result
PASS R2 call 2 rating
PASS R2 call 3 result
PASS R2 call 3 rating
PASS R2 call 4 result
PASS R2 call 4 rating
PASS R3 call 1 result
PASS R3 call 1 rating
PASS R3 call 2 result
PASS R3 call 2 rating
PASS R3 call 3 result
PASS R3 call 3 rating
PASS C1 accepted
PASS C1 out_of_range
PASS C1 invalid_input
PASS C1 sum
PASS C2 accepted
PASS C2 out_of_range
PASS C2 invalid_input
PASS C2 sum
Checks: 28, failed: 0
```

Exit code: 0.

**The deliberate bug:** reading straight into `result`, with no other change:

<!-- fragment -->
```cpp
input >> result;
```

<!-- example: survey_tests_direct_read exit=1 -->
```cpp
#include <iostream>
#include <limits>
#include <sstream>
#include <string>

enum class ReadResult {
    accepted,
    out_of_range,
    invalid_input,
    end_of_input
};

void discard_rest_of_line(std::istream& input) {
    input.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
}

ReadResult read_number(std::istream& input, int minimum, int maximum, int& result) {
    if (input.bad()) {
        return ReadResult::end_of_input;
    }

    input >> std::ws;

    if (input.eof()) {
        return ReadResult::end_of_input;
    }

    input >> result;

    if (input.fail()) {
        if (input.bad()) {
            return ReadResult::end_of_input;
        }

        input.clear();
        discard_rest_of_line(input);
        return ReadResult::invalid_input;
    }

    discard_rest_of_line(input);

    if (result < minimum || result > maximum) {
        return ReadResult::out_of_range;
    }

    return ReadResult::accepted;
}

std::string read_result_text(ReadResult result) {
    switch (result) {
        case ReadResult::accepted:
            return "accepted";
        case ReadResult::out_of_range:
            return "out_of_range";
        case ReadResult::invalid_input:
            return "invalid_input";
        case ReadResult::end_of_input:
            return "end_of_input";
    }

    return "unknown";
}

struct SurveyCounts {
    int accepted;
    int out_of_range;
    int invalid_input;
    int sum;
};

SurveyCounts count_ratings(std::istream& input) {
    SurveyCounts counts{0, 0, 0, 0};
    int rating{0};
    bool input_ended{false};

    while (!input_ended) {
        const ReadResult result{read_number(input, 1, 5, rating)};

        switch (result) {
            case ReadResult::accepted:
                ++counts.accepted;
                counts.sum += rating;
                break;
            case ReadResult::out_of_range:
                ++counts.out_of_range;
                break;
            case ReadResult::invalid_input:
                ++counts.invalid_input;
                break;
            case ReadResult::end_of_input:
                input_ended = true;
                break;
        }
    }

    return counts;
}

void check_read_result(const std::string& name, ReadResult expected, ReadResult actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << read_result_text(expected) << ", actual " << read_result_text(actual) << "\n";
        ++failed;
    }
}

void check_int(const std::string& name, int expected, int actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << expected << ", actual " << actual << "\n";
        ++failed;
    }
}

int main() {
    int checks{0};
    int failed{0};

    std::istringstream input_r1{"abc\n4\n"};
    int rating_r1{-1};
    check_read_result("R1 call 1 result", ReadResult::invalid_input, read_number(input_r1, 1, 5, rating_r1), checks, failed);
    check_int("R1 call 1 rating", -1, rating_r1, checks, failed);
    check_read_result("R1 call 2 result", ReadResult::accepted, read_number(input_r1, 1, 5, rating_r1), checks, failed);
    check_int("R1 call 2 rating", 4, rating_r1, checks, failed);
    check_read_result("R1 call 3 result", ReadResult::end_of_input, read_number(input_r1, 1, 5, rating_r1), checks, failed);
    check_int("R1 call 3 rating", 4, rating_r1, checks, failed);

    std::istringstream input_r2{"0\n6\n1"};
    int rating_r2{-1};
    check_read_result("R2 call 1 result", ReadResult::out_of_range, read_number(input_r2, 1, 5, rating_r2), checks, failed);
    check_int("R2 call 1 rating", -1, rating_r2, checks, failed);
    check_read_result("R2 call 2 result", ReadResult::out_of_range, read_number(input_r2, 1, 5, rating_r2), checks, failed);
    check_int("R2 call 2 rating", -1, rating_r2, checks, failed);
    check_read_result("R2 call 3 result", ReadResult::accepted, read_number(input_r2, 1, 5, rating_r2), checks, failed);
    check_int("R2 call 3 rating", 1, rating_r2, checks, failed);
    check_read_result("R2 call 4 result", ReadResult::end_of_input, read_number(input_r2, 1, 5, rating_r2), checks, failed);
    check_int("R2 call 4 rating", 1, rating_r2, checks, failed);

    std::istringstream input_r3{"2\nxyz"};
    int rating_r3{-1};
    check_read_result("R3 call 1 result", ReadResult::accepted, read_number(input_r3, 1, 5, rating_r3), checks, failed);
    check_int("R3 call 1 rating", 2, rating_r3, checks, failed);
    check_read_result("R3 call 2 result", ReadResult::invalid_input, read_number(input_r3, 1, 5, rating_r3), checks, failed);
    check_int("R3 call 2 rating", 2, rating_r3, checks, failed);
    check_read_result("R3 call 3 result", ReadResult::end_of_input, read_number(input_r3, 1, 5, rating_r3), checks, failed);
    check_int("R3 call 3 rating", 2, rating_r3, checks, failed);

    std::istringstream input_c1{"5\n\nabc\nxyz\n0\n3 stars\n4"};
    const SurveyCounts counts_c1{count_ratings(input_c1)};
    check_int("C1 accepted", 3, counts_c1.accepted, checks, failed);
    check_int("C1 out_of_range", 1, counts_c1.out_of_range, checks, failed);
    check_int("C1 invalid_input", 2, counts_c1.invalid_input, checks, failed);
    check_int("C1 sum", 12, counts_c1.sum, checks, failed);

    std::istringstream input_c2{""};
    const SurveyCounts counts_c2{count_ratings(input_c2)};
    check_int("C2 accepted", 0, counts_c2.accepted, checks, failed);
    check_int("C2 out_of_range", 0, counts_c2.out_of_range, checks, failed);
    check_int("C2 invalid_input", 0, counts_c2.invalid_input, checks, failed);
    check_int("C2 sum", 0, counts_c2.sum, checks, failed);

    std::cout << "Checks: " << checks << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }
}
```

<!-- output: survey_tests_direct_read -->
```text
PASS R1 call 1 result
FAIL R1 call 1 rating: expected -1, actual 0
PASS R1 call 2 result
PASS R1 call 2 rating
PASS R1 call 3 result
PASS R1 call 3 rating
PASS R2 call 1 result
FAIL R2 call 1 rating: expected -1, actual 0
PASS R2 call 2 result
FAIL R2 call 2 rating: expected -1, actual 6
PASS R2 call 3 result
PASS R2 call 3 rating
PASS R2 call 4 result
PASS R2 call 4 rating
PASS R3 call 1 result
PASS R3 call 1 rating
PASS R3 call 2 result
FAIL R3 call 2 rating: expected 2, actual 0
PASS R3 call 3 result
FAIL R3 call 3 rating: expected 2, actual 0
PASS C1 accepted
PASS C1 out_of_range
PASS C1 invalid_input
PASS C1 sum
PASS C2 accepted
PASS C2 out_of_range
PASS C2 invalid_input
PASS C2 sum
Checks: 28, failed: 5
```

Exit code: 1.

| Scenario | Call | Result | Expected rating | Actual rating |
|---|---|---|---:|---:|
| R1 | 1: `abc` | `invalid_input`, correct | −1 | 0 |
| R2 | 1: `0` | `out_of_range`, correct | −1 | 0 |
| R2 | 2: `6` | `out_of_range`, correct | −1 | 6 |
| R3 | 2: `xyz` | `invalid_input`, correct | 2 | 0 |
| R3 | 3: the end of the data | `end_of_input`, correct | 2 | 0 |
| C1, C2 | all | the counts correct | — | — |

- **Every named result is correct,** and still the function breaks the contract: after a refusal it changes `result`. That's the same lesson as in 14.3: a correct result doesn't guarantee a correct state.
- **The counting scenarios don't see it.** The counts depend only on the results, and only accepted ratings go into the sum, and those are correct. The bug is detected by the checks of the rating in the scenarios that call `read_number` directly.
- **The last `FAIL` in R3** shows the effect of the earlier error: `end_of_input` changes nothing, so the 0 is left from the previous call.
- **Exit code 1** comes from five real `FAIL` lines.

**After the fix:** with the local variable restored, the program is again the same as the first version. The same 28 checks print `PASS` and `Checks: 28, failed: 0`, and the exit code is 0. The expected results didn't change.

**Optional: a report from the keyboard.** The same `count_ratings` reads from `std::cin`:

<!-- example: survey_report -->
```cpp
#include <iostream>
#include <limits>

enum class ReadResult {
    accepted,
    out_of_range,
    invalid_input,
    end_of_input
};

void discard_rest_of_line(std::istream& input) {
    input.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
}

ReadResult read_number(std::istream& input, int minimum, int maximum, int& result) {
    if (input.bad()) {
        return ReadResult::end_of_input;
    }

    input >> std::ws;

    if (input.eof()) {
        return ReadResult::end_of_input;
    }

    int value{0};
    input >> value;

    if (input.fail()) {
        if (input.bad()) {
            return ReadResult::end_of_input;
        }

        input.clear();
        discard_rest_of_line(input);
        return ReadResult::invalid_input;
    }

    discard_rest_of_line(input);

    if (value < minimum || value > maximum) {
        return ReadResult::out_of_range;
    }

    result = value;
    return ReadResult::accepted;
}

struct SurveyCounts {
    int accepted;
    int out_of_range;
    int invalid_input;
    int sum;
};

SurveyCounts count_ratings(std::istream& input) {
    SurveyCounts counts{0, 0, 0, 0};
    int rating{0};
    bool input_ended{false};

    while (!input_ended) {
        const ReadResult result{read_number(input, 1, 5, rating)};

        switch (result) {
            case ReadResult::accepted:
                ++counts.accepted;
                counts.sum += rating;
                break;
            case ReadResult::out_of_range:
                ++counts.out_of_range;
                break;
            case ReadResult::invalid_input:
                ++counts.invalid_input;
                break;
            case ReadResult::end_of_input:
                input_ended = true;
                break;
        }
    }

    return counts;
}

int main() {
    std::cout << "Enter ratings from 1 to 5, one per line:\n";
    const SurveyCounts counts{count_ratings(std::cin)};

    std::cout << "Ratings: " << counts.accepted << "\n";
    std::cout << "Sum: " << counts.sum << "\n";
    std::cout << "Out of range: " << counts.out_of_range << "\n";
    std::cout << "Invalid entries: " << counts.invalid_input << "\n";
}
```

<!-- input: survey_report -->
```text
5
3
abc
9

4
```

<!-- output: survey_report -->
```text
Enter ratings from 1 to 5, one per line:
Ratings: 3
Sum: 12
Out of range: 1
Invalid entries: 1
```

The empty line isn't counted, `abc` is a bad entry, and `9` is off the scale.

**Self-assessment.** Compare your work with the checklist in section 8. In particular, check:
- whether your table was made before the code and has every required kind of scenario, including the last rating and the last bad entry without a line end;
- whether every scenario has its own stream, and the successive calls within a scenario use the same one;
- whether after every call of `read_number` you check both the result and the rating;
- whether the end of the data ends the loop and increases no counter;
- whether your prediction from step 1 matched the result of step 5, and if not, whether you can explain the difference.

If the answer to any of these is "no", go back to the matching section of the lesson before you move on.

</details>

**Previous lesson:** [Lesson 14.3: A function explains why it refused](lesson_03_function_explains_refusal.en.md) · **Next lesson:** 14.5, in preparation · [Course overview](../../README.en.md)

# Lesson 4.6: A failed read, recovering the stream and the end of the data

[Polski](lesson_06_recover_and_end_of_input.md) · **English** · [Course overview](../../README.en.md)

> **Module 4, lesson 6** · about 90–105 minutes, can be split into two sessions (for example sections 1–8, then 9–13)
> **You need:** the `cpp-workspace` folder and the original `lesson_05_first_program` project, as before. You don't need the debugger in this lesson.
> **Pilot version.** The programs in this lesson are checked automatically on Windows, Ubuntu and macOS, including with the given input data. Typing input into CLion's **Run** window is described without a manual check on every system.

## Before you start

This lesson assumes that after lesson 4.5:

- you ask again in a `while` loop when the number read doesn't meet the requirements;
- you check with `std::cin.fail()` whether a read succeeded, before checking the value;
- you end a loop for two reasons, recorded in two flags;
- you read a whole line of text with `std::getline` (lesson 2.7).

## The situation

The program in lesson 4.5 asked for a number of study sessions from 1 to 5. It told three situations apart:

- `3`: the read succeeds, the value is acceptable, the program accepts it;
- `0`: the read succeeds, the value is unacceptable, the program asks again;
- `abc`: the read fails, the program ends.

The last reaction is safe, but harsh: a single typo ends the whole program. The new requirement says: **after `abc`, the program should report the problem and let the user type a number again.** For the data `abc`, `0`, `3` the program should:

1. find that `abc` couldn't be read as a number;
2. remove whatever is in the way, and ask again;
3. read `0`: a number, but outside the range, so ask again;
4. read `3` and accept that value.

At the same time, the program must still end when **the data runs out**. After the end of the data there's nothing to fix and nothing to ask.

After this lesson you'll be able to:

- explain why, after a failed read, simply repeating `std::cin >> value` doesn't help;
- bring the stream back into working order with `std::cin.clear()`, and discard the rest of the bad line with `std::getline`;
- recognise the end of the data with `std::cin.eof()`, and check it in the right order;
- tell an unacceptable value, a failed read of a number, and no more data apart;
- understand why `12abc` gives the number 12;
- combine recovering the input with a loop that builds up a result.

## 1. Prepare the project

In `cpp-workspace`, create a `lesson_4_6` folder and copy `main.cpp` and `CMakeLists.txt` into it from the original `lesson_05_first_program`. You type the programs from sections 7 and 9 into that folder's `main.cpp`.

## 2. Two obstacles after `abc`

After the failed read of `abc`, **two different** things block further reading:

- **The error state.** The stream `std::cin` remembers that a read failed: `std::cin.fail()` gives `true`. As long as that state lasts, every further read fails at once, as in lesson 4.5.
- **The leftover text.** The characters `abc` weren't read as a number, so they **are still waiting** in the input. If the program tried to read a number again, it would meet the same characters.

Keep two things apart here:

- **the value of a variable**, such as `sessions`, is a number stored in the program;
- **the state of the stream**, i.e. what `fail()` and `eof()` show, and the characters waiting in the input, describe `std::cin`.

Fixing one doesn't fix the other. So two separate actions are needed.

## 3. Restoring the state: `std::cin.clear()`

<!-- fragment -->
```cpp
std::cin.clear();
```

- `clear` is another member function of the object `std::cin`, called with a dot, like `fail()` in lesson 4.5.
- It brings the stream back to its normal state, i.e. it removes the failed-read mark. After `clear()`, `std::cin.fail()` gives `false`, and further reads can succeed again, **as long as there's still some data**.
- **`clear()` doesn't remove any characters from the input.** The text `abc` is still waiting there.
- **`clear()` doesn't create new data.** If the data has run out, there's still none after `clear()`.
- `clear()` doesn't change the value of any variable. It changes only the stream's state.

## 4. Discarding the rest of the line: `std::getline`

The leftover text is removed by `std::getline`, which you know from lesson 2.7. It reads the rest of the current line into a helper variable that we then don't use:

<!-- fragment -->
```cpp
std::cin.clear();

std::string discarded_line{""};
std::getline(std::cin, discarded_line);
```

- `discarded_line` gets the rest of the bad line, including its end. There's no need to print it or use it. What matters is that **those characters are taken out of the input**.
- So the next read attempt starts at a new line, not at the same bad characters.
- The order matters: **first `clear()`, then `getline`**. As long as the stream is in an error state, `getline` would fail at once too.
- Programs that use `std::string` need `#include <string>`.

**All** of the rest of the line is discarded. If the user types `abc 2` on one line, the program discards the whole of `abc 2`, and doesn't accept `2` as another answer. The next attempt is about the next line only.

There are other ways to discard data from the input too. You'll meet them later in the course. Here `std::getline` is enough.

## 5. The end of the data: `std::cin.eof()`

After a failed read, the program needs to know **why** it failed. Was there text in the input that can be discarded, or did the data simply run out? `std::cin.eof()` (*end of file*, the end of the data) answers that:

- it gives `true` when, during the operations so far, the stream **reached the end of the data**;
- it describes the state after operations that have already happened. It doesn't predict whether someone is about to type something;
- the end of the data isn't an unacceptable number, nor bad text. There's nothing to discard and nothing to wait for. **After the end of the data, the program stops trying**, and `clear()` changes nothing here.

The programs in this course are checked automatically: the data comes all at once, and after the last line it ends. The program must then end by itself, safely.

**A very important order: success first, then the end of the data.** A read `std::cin >> value` can **successfully** read the last number and reach the end of the data at the same time, for example when there isn't even a line end after the number. Then `std::cin.eof()` gives `true`, but `std::cin.fail()` gives `false`, and the number was read correctly. If the program checked `eof()` first, it would throw away a good, final answer. So the decision always has this order:

1. If the read succeeded (`!std::cin.fail()`), the program checks the number read.
2. Otherwise, if the data has run out (`std::cin.eof()`), the program stops trying.
3. Otherwise the read stopped at bad text: the program restores the stream and discards the rest of the line.

So the result `eof() == true` on its own doesn't mean that the last read failed to deliver a valid value.

## 6. A table of the stream's state

| Step | Value of `sessions` | `fail()` | `eof()` | What's left of the current line |
|---|---|---|---|---|
| read `3` | 3 | `false` | `false` | only the line end |
| read `0` | 0: the read succeeded, but the value is unacceptable | `false` | `false` | only the line end |
| read `abc` | can't be relied on | `true` | `false` | `abc` and the line end |
| after `clear()` | unchanged | `false` | `false` | **still** `abc` and the line end |
| after `getline` | unchanged | `false` | `false` | nothing: the line discarded |
| a read when there's no more data | can't be relied on | `true` | `true` | nothing |

`clear()` changes only the stream's state, and `getline` only takes characters out of the input. Neither of them changes the value of `sessions`, or the requirements that value must meet.

## 7. The complete program

<!-- example: sessions_recover -->
```cpp
#include <iostream>
#include <string>

int main() {
    int sessions{0};
    bool accepted{false};
    bool input_ended{false};

    while (!accepted && !input_ended) {
        std::cout << "Enter session count (1-5):\n";
        std::cin >> sessions;

        if (!std::cin.fail()) {
            if (sessions >= 1 && sessions <= 5) {
                accepted = true;
            } else {
                std::cout << "Session count out of range\n";
            }
        } else if (std::cin.eof()) {
            input_ended = true;
        } else {
            std::cin.clear();
            std::string discarded_line{""};
            std::getline(std::cin, discarded_line);

            if (std::cin.fail() || std::cin.eof()) {
                input_ended = true;
            } else {
                std::cout << "Invalid integer input, try again\n";
            }
        }
    }

    if (accepted) {
        std::cout << "Accepted sessions: " << sessions << "\n";
    } else {
        std::cout << "Input ended\n";
    }
}
```

- **Two flags.** `accepted` means an accepted value, and `input_ended` no more data. The loop runs while neither of them is set.
- **First branch: the read succeeded.** Only here does the program check the range. For a value outside it, it prints `Session count out of range`, and the flags don't change, so the program asks again.
- **Second branch: the read failed because the data ran out.** The program sets `input_ended`. It doesn't call `clear()` and doesn't ask again.
- **Third branch: the read failed for another reason, i.e. because of bad text.** The program restores the state, discards the rest of the line and prints `Invalid integer input, try again`, after which the loop asks again.
- **The end of the data while discarding.** If the bad line was the last one and had no line end, `getline` reaches the end of the data, and `eof()` gives `true`. The program then doesn't promise another attempt: it sets `input_ended`, and the loop reads nothing more. The `fail()` check covers the rare situation in which discarding didn't work at all.
- **Messages.** `Session count out of range` means a number outside the range, `Invalid integer input, try again` a failed read with another attempt possible, `Input ended` no more data, and `Accepted sessions: N` an accepted value.

## 8. Predict and check

**Predict**, for each set of data: how many times will the question be asked, which messages will appear, and how will the program end? Write your answers down, then run the program.

| Set | Data, line by line |
|---|---|
| A | `abc`, `0`, `3` |
| B | `3` |
| C | `0`, `3` |
| D | `abc`, `3` |
| E | `abc`, `xyz`, `3` |
| F | `abc 2`, `4` |
| G | `0`, then the end of the data |
| H | `abc`, then the end of the data |
| I | no number at all |

<!-- input: sessions_recover -->
```text
abc
0
3
```

<details>
<summary>Standard output for set A: abc, 0, 3</summary>

<!-- output: sessions_recover -->
```text
Enter session count (1-5):
Invalid integer input, try again
Enter session count (1-5):
Session count out of range
Enter session count (1-5):
Accepted sessions: 3
```

</details>

<!-- input: sessions_recover -->
```text
3
```

<details>
<summary>Standard output for set B: 3</summary>

<!-- output: sessions_recover -->
```text
Enter session count (1-5):
Accepted sessions: 3
```

</details>

<!-- input: sessions_recover -->
```text
0
3
```

<details>
<summary>Standard output for set C: 0, 3</summary>

<!-- output: sessions_recover -->
```text
Enter session count (1-5):
Session count out of range
Enter session count (1-5):
Accepted sessions: 3
```

</details>

<!-- input: sessions_recover -->
```text
abc
3
```

<details>
<summary>Standard output for set D: abc, 3</summary>

<!-- output: sessions_recover -->
```text
Enter session count (1-5):
Invalid integer input, try again
Enter session count (1-5):
Accepted sessions: 3
```

</details>

<!-- input: sessions_recover -->
```text
abc
xyz
3
```

<details>
<summary>Standard output for set E: abc, xyz, 3</summary>

<!-- output: sessions_recover -->
```text
Enter session count (1-5):
Invalid integer input, try again
Enter session count (1-5):
Invalid integer input, try again
Enter session count (1-5):
Accepted sessions: 3
```

</details>

<!-- input: sessions_recover -->
```text
abc 2
4
```

<details>
<summary>Standard output for set F: abc 2, 4</summary>

<!-- output: sessions_recover -->
```text
Enter session count (1-5):
Invalid integer input, try again
Enter session count (1-5):
Accepted sessions: 4
```

The whole line `abc 2` was discarded, so `2` wasn't a separate answer. The program accepted only `4`, from the next line.

</details>

<!-- input: sessions_recover -->
```text
0
```

<details>
<summary>Standard output for set G: 0, then the end of the data</summary>

<!-- output: sessions_recover -->
```text
Enter session count (1-5):
Session count out of range
Enter session count (1-5):
Input ended
```

</details>

<!-- input: sessions_recover -->
```text
abc
```

<details>
<summary>Standard output for set H: abc, then the end of the data</summary>

<!-- output: sessions_recover -->
```text
Enter session count (1-5):
Invalid integer input, try again
Enter session count (1-5):
Input ended
```

| Attempt | What happens | `fail()` after the read | `eof()` after the read | What the program does |
|---|---|---|---|---|
| 1 | `abc` isn't a number | `true` | `false` | `clear()`, `getline` discards `abc`, message, another attempt |
| 2 | there's no more data | `true` | `true` | `input_ended`: no more attempts |

The line `abc` ended normally, so after discarding it the program could ask once more. Only the next attempt met the end of the data.

</details>

<!-- input: sessions_recover -->
```text
```

<details>
<summary>Standard output for set I: no number at all</summary>

<!-- output: sessions_recover -->
```text
Enter session count (1-5):
Input ended
```

</details>

Each of these runs ends by itself. The loop doesn't go on forever, neither after bad text nor after the end of the data.

## 9. Experiment: `12abc`

The program prints the number read, then the rest of the same line:

<!-- example: prefix_read -->
```cpp
#include <iostream>
#include <string>

int main() {
    int number{0};
    std::string rest_of_line{""};

    std::cout << "Enter a number:\n";
    std::cin >> number;

    if (!std::cin.fail()) {
        std::cout << "Number: " << number << "\n";
        std::getline(std::cin, rest_of_line);
        std::cout << "Left in the line: [" << rest_of_line << "]\n";
    } else {
        std::cout << "Invalid integer input\n";
    }
}
```

**Predict**: for `12abc`, will reading the number fail? And for `12`? And for `abc`?

<!-- input: prefix_read -->
```text
12abc
```

<details>
<summary>Standard output for 12abc</summary>

<!-- output: prefix_read -->
```text
Enter a number:
Number: 12
Left in the line: [abc]
```

</details>

<!-- input: prefix_read -->
```text
12
```

<details>
<summary>Standard output for 12</summary>

<!-- output: prefix_read -->
```text
Enter a number:
Number: 12
Left in the line: []
```

</details>

<!-- input: prefix_read -->
```text
abc
```

<details>
<summary>Standard output for abc</summary>

<!-- output: prefix_read -->
```text
Enter a number:
Invalid integer input
```

</details>

`std::cin >> number` reads as many digits as it can, and stops at the first character that doesn't fit a number. For `12abc` the read **succeeds**: the number is 12, and `abc` stays in the input. In the same way, the program in section 7 accepts `3abc` as 3:

<!-- input: sessions_recover -->
```text
3abc
```

<details>
<summary>Standard output of the section 7 program for 3abc</summary>

<!-- output: sessions_recover -->
```text
Enter session count (1-5):
Accepted sessions: 3
```

</details>

So a successful read of a leading number doesn't mean that the whole line was a valid number. **This lesson teaches recovering after a failed read, not fully checking the contents of a whole line.** The programs in this lesson aren't robust against arbitrary data.

## 10. Find the bug: `clear()` alone isn't enough

**Analyse this fragment on paper; don't run it.** After a failed read, the program restores the stream's state, but doesn't discard the rest of the line:

<!-- fragment -->
```cpp
while (!accepted && !input_ended) {
    std::cout << "Enter session count (1-5):\n";
    std::cin >> sessions;

    if (!std::cin.fail()) {
        if (sessions >= 1 && sessions <= 5) {
            accepted = true;
        } else {
            std::cout << "Session count out of range\n";
        }
    } else if (std::cin.eof()) {
        input_ended = true;
    } else {
        std::cin.clear();
        std::cout << "Invalid integer input, try again\n";
    }
}
```

1. Trace the first attempt for the data `abc`, `3`: what happens to the error state?
2. What's left in the input after `clear()`?
3. What will the next read meet? Will it ever get to `3`?
4. Which step is missing?
5. Compare the fixed fragment with the program in section 7.

The trace table and the answers are in [Example solutions](#example-solutions).

## 11. Mission: putting a shipment together

A worker is putting a shipment together. The goal is to collect **at least 10 items**. The program asks for the size of the next batch of items. An acceptable batch has 1 to 4 items.

**Requirements:**

- The program asks `Enter batch size (1-4):` and reads a whole number.
- It adds an acceptable batch to the number collected, and prints the progress: `Collected: N`.
- For a number outside the range, it prints `Batch size out of range` and asks again. The number collected doesn't change.
- After a badly written number, it prints `Invalid integer input, try again`, recovers the input and asks again. The number collected doesn't change.
- After collecting at least 10 items, it stops, without another question, and prints `Target reached: N items`.
- When the data runs out before the goal is reached, it stops and prints `Input ended: N items collected`.
- The program isn't robust against arbitrary data: `2abc` is accepted as 2, as in section 9.

In `cpp-workspace`, create a `shipment` folder, copy `CMakeLists.txt` into it from the original `lesson_05_first_program`, create an empty `main.cpp` and write the program on your own.

Standard output for four examples must be as follows. The goal reached after the batches `3`, `4`, `3`:

<!-- input: shipment -->
```text
3
4
3
```

<!-- output: shipment -->
```text
Enter batch size (1-4):
Collected: 3
Enter batch size (1-4):
Collected: 7
Enter batch size (1-4):
Collected: 10
Target reached: 10 items
```

Bad text in the middle, with the data `2`, `abc`, `4`, `4`:

<!-- input: shipment -->
```text
2
abc
4
4
```

<!-- output: shipment -->
```text
Enter batch size (1-4):
Collected: 2
Enter batch size (1-4):
Invalid integer input, try again
Enter batch size (1-4):
Collected: 6
Enter batch size (1-4):
Collected: 10
Target reached: 10 items
```

The data runs out after the batches `2` and `3`:

<!-- input: shipment -->
```text
2
3
```

<!-- output: shipment -->
```text
Enter batch size (1-4):
Collected: 2
Enter batch size (1-4):
Collected: 5
Enter batch size (1-4):
Input ended: 5 items collected
```

Values outside the range, with the data `0`, `3`, `5`, `3`, `4`:

<!-- input: shipment -->
```text
0
3
5
3
4
```

<!-- output: shipment -->
```text
Enter batch size (1-4):
Batch size out of range
Enter batch size (1-4):
Collected: 3
Enter batch size (1-4):
Batch size out of range
Enter batch size (1-4):
Collected: 6
Enter batch size (1-4):
Collected: 10
Target reached: 10 items
```

**This isn't the program from section 7 with new messages.** There, the loop waited for **one** acceptable value, which ended the work. Here a single valid batch doesn't end the work: the loop keeps going until **the sum collected** reaches the goal, as in lesson 4.4, and along the way it has to cope with bad data and with the end of the data. You have to decide on your own:

1. where to keep the number of items collected, and how to use it in the loop's condition;
2. in which situations the number collected should change, and in which it shouldn't;
3. how to recover the input after bad text, and when to stop trying instead;
4. how, after the loop, to tell reaching the goal from an earlier end of the data.

**Before you write the program**, prepare two things:

- a trace table for the data `2`, `abc`, `4`, `4`: the attempt, what was read, `fail()` and `eof()`, what the program does, and the number collected after the attempt;
- a table of test cases: the goal reached exactly and passed, batches of 0, negative and over 4, bad text once and several times, text and an out-of-range number in one sequence, a line with bad text and extra characters, and the end of the data before the first batch, after several valid batches and after several bad entries. Write down the expected standard output for each case.

### Success criteria

- The program builds as C++20, and its standard output for the four examples above is exactly as shown.
- The `while` loop ends after collecting at least 10 items, or after the end of the data. There's no question after the goal is reached.
- The number collected grows only by correctly read, acceptable batches. Values outside the range and bad text don't change it.
- After a failed read, the program first checks for the end of the data. Only if the data hasn't run out does it call `std::cin.clear()` and discard the rest of the line with `std::getline`.
- If the end of the data appears while discarding, the program doesn't try to read any more.
- `Target reached` appears only after the goal is reached, and `Input ended` only when it wasn't.
- The trace table and the table of cases were made before running the program.
- You can explain why the program also ends after the end of the data.

When the result matches, you can save the project in Git, as in lesson 1.5.

<details>
<summary>Hint 1</summary>

Which two events can end the work: reaching the goal, or no more data?

</details>

<details>
<summary>Hint 2</summary>

In which cases should the number of items collected change?

</details>

<details>
<summary>Hint 3</summary>

After a failed read, first find out whether the data has run out. Only when it's possible to continue, remove the error state and the leftover text.

</details>

<details>
<summary>The full list of control cases: open after preparing your own table</summary>

| Data | Ending | Collected | What it checks |
|---|---|---|---|
| `3`, `4`, `3` | goal | 10 | the goal reached exactly |
| `2`, `abc`, `4`, `4` | goal | 10 | bad text, then success |
| `2`, `3`, end | end of the data | 5 | the end of the data after valid batches |
| `0`, `3`, `5`, `3`, `4` | goal | 10 | a zero and a too-large batch |
| `4`, `4`, `4` | goal | 12 | the goal passed by the last batch |
| `-1`, `4`, `4`, `2` | goal | 10 | a negative batch |
| `abc`, `xyz`, `4`, `4`, `2` | goal | 10 | several bad texts |
| `abc`, `9`, `4`, `4`, `2` | goal | 10 | text and an out-of-range number |
| `x 3`, `4`, `4`, `2` | goal | 10 | a line with extra characters, discarded as a whole |
| no data | end of the data | 0 | the end of the data before the first batch |
| `abc`, `7`, end | end of the data | 0 | the end of the data after bad entries |

The first four cases are checked above, in the mission's description.

<!-- input: shipment -->
```text
4
4
4
```

<!-- output: shipment -->
```text
Enter batch size (1-4):
Collected: 4
Enter batch size (1-4):
Collected: 8
Enter batch size (1-4):
Collected: 12
Target reached: 12 items
```

<!-- input: shipment -->
```text
-1
4
4
2
```

<!-- output: shipment -->
```text
Enter batch size (1-4):
Batch size out of range
Enter batch size (1-4):
Collected: 4
Enter batch size (1-4):
Collected: 8
Enter batch size (1-4):
Collected: 10
Target reached: 10 items
```

<!-- input: shipment -->
```text
abc
xyz
4
4
2
```

<!-- output: shipment -->
```text
Enter batch size (1-4):
Invalid integer input, try again
Enter batch size (1-4):
Invalid integer input, try again
Enter batch size (1-4):
Collected: 4
Enter batch size (1-4):
Collected: 8
Enter batch size (1-4):
Collected: 10
Target reached: 10 items
```

<!-- input: shipment -->
```text
abc
9
4
4
2
```

<!-- output: shipment -->
```text
Enter batch size (1-4):
Invalid integer input, try again
Enter batch size (1-4):
Batch size out of range
Enter batch size (1-4):
Collected: 4
Enter batch size (1-4):
Collected: 8
Enter batch size (1-4):
Collected: 10
Target reached: 10 items
```

<!-- input: shipment -->
```text
x 3
4
4
2
```

<!-- output: shipment -->
```text
Enter batch size (1-4):
Invalid integer input, try again
Enter batch size (1-4):
Collected: 4
Enter batch size (1-4):
Collected: 8
Enter batch size (1-4):
Collected: 10
Target reached: 10 items
```

<!-- input: shipment -->
```text
```

<!-- output: shipment -->
```text
Enter batch size (1-4):
Input ended: 0 items collected
```

<!-- input: shipment -->
```text
abc
7
```

<!-- output: shipment -->
```text
Enter batch size (1-4):
Invalid integer input, try again
Enter batch size (1-4):
Batch size out of range
Enter batch size (1-4):
Input ended: 0 items collected
```

</details>

An example solution is in [Example solutions](#example-solutions).

## 12. When something goes differently

| What you see | What it means | What to do |
|---|---|---|
| The same bad-text message repeats forever | After `clear()` the rest of the line isn't discarded, so the next read meets the same characters (section 10). | Stop the program. After `clear()`, add `std::getline` into a helper variable. |
| The question repeats forever after the end of the data | The program calls `clear()` even when the data has run out, and keeps trying. | After a failed read, first check `std::cin.eof()`, and then stop trying. |
| The last valid number is thrown away | The program checks `eof()` before checking whether the read succeeded. | First `!std::cin.fail()`, and only in the failure branch `eof()` (section 5). |
| `getline` discards nothing, and the error repeats | `getline` is before `clear()`, so it fails too. | First `clear()`, then `getline`. |
| After `abc 2` the program accepts `2` | Only the bad word is discarded, not the whole line. | Discard the rest of the line with `std::getline`. |
| `3abc` is accepted as 3 | That's how reading a number with `>>` works (section 9). | It's a known limit of this lesson, not a bug in your program. |
| The sum changes after bad data | The addition is outside the branch for a successful, acceptable read. | Add a batch only after a successful read of a value in the range. |
| The program does nothing and waits | It's waiting for another line of data, as in lesson 2.6. | Type a number and press **Enter**. |

## 13. Explain

Answer briefly, preferably in writing. Only then compare with the example answer.

**1.** Why doesn't simply repeating `std::cin >> sessions` help after `abc`?

<details>
<summary>Example answer</summary>

Because the stream is in an error state, so every further read fails at once. Even after restoring the state, the same characters `abc` would still be waiting in the input.

</details>

**2.** What does `std::cin.clear()` do, and what doesn't it do?

<details>
<summary>Example answer</summary>

It brings the stream back to its normal state, so further reads can succeed again. It doesn't remove characters from the input, doesn't create new data, and doesn't change the value of any variable.

</details>

**3.** Why do we call `std::getline` after `clear()`, and why in that order?

<details>
<summary>Example answer</summary>

`getline` takes the rest of the bad line out of the input, so that the next read starts at a new line. It has to come after `clear()`, because as long as the stream is in an error state, `getline` would fail at once too.

</details>

**4.** Why do we check `eof()` only when the read failed?

<details>
<summary>Example answer</summary>

Because a successful read of the last number can also reach the end of the data. Then `eof()` gives `true`, and yet the number is valid. Checking `eof()` first would throw away a good answer.

</details>

**5.** Why doesn't the program call `clear()` and ask again after the end of the data?

<details>
<summary>Example answer</summary>

Because there's nothing left to read. `clear()` won't create new data, so further questions would get no answer, and the loop might go on forever.

</details>

**6.** Why does the program also check for the end of the data after discarding the line?

<details>
<summary>Example answer</summary>

Because the bad line might have been the last one. Then `getline` reaches the end of the data, and there's no point promising another attempt or reading on.

</details>

**7.** How do `0`, `abc` and the end of the data differ?

<details>
<summary>Example answer</summary>

`0` is a successful read of an unacceptable number: the program asks again. `abc` is a failed read after which the input can be recovered: `clear()`, discarding the line, and asking again. The end of the data is a failed read after which there's nothing to recover: the program stops trying.

</details>

**8.** Why does `12abc` give the number 12, and not a failed read?

<details>
<summary>Example answer</summary>

Because `>>` reads as many digits as it can, and stops at the first character that doesn't fit. The digits `12` make a valid number, and `abc` stays in the input. The read succeeds, even though the whole line isn't a valid number.

</details>

**9.** Why doesn't the loop in the mission end after the first valid batch?

<details>
<summary>Example answer</summary>

Because the goal is the sum collected, not a single valid answer. The loop's condition checks whether at least 10 items have been collected yet, and one batch has at most 4.

</details>

## Summary

- After a failed read there are two obstacles: the stream's **error state** and the **leftover text** in the input. Each needs a separate action.
- `std::cin.clear()` brings the stream back to its normal state. It doesn't remove characters, create data, or change variables.
- `std::getline` into a helper variable discards the rest of the bad line, as a whole. First `clear()`, then `getline`.
- `std::cin.eof()` says whether the stream reached the end of the data. The end of the data ends the attempts: there's nothing to fix.
- The order of decisions: **the read's success first**, then the end of the data, and recovery only last. A successful read of the last number can set `eof()` and still give a valid value.
- If the data runs out while the line is being discarded, the program doesn't try to read any more.
- `>>` reads a number from the start of a line, so `12abc` gives 12. The program recovers the input after a failed read, but doesn't check whole lines.

## What's next

This was the last lesson of Module 4 with new skills. In lesson 4.7 you'll test them in an independent test: [Lesson 4.7: The program repeats actions (the Module 4 test)](lesson_07_the_program_repeats.en.md).

---

## Example solutions

Look here **after your own attempt**. Your names may differ, as long as the standard output is as required.

<details>
<summary>Section 10: clear() alone isn't enough</summary>

For the data `abc`, `3`:

| Attempt | What the read meets | `fail()` after the read | What the program does | What's left in the input |
|---|---|---|---|---|
| 1 | `abc` | `true` | `clear()`, message | **still** `abc` and the line end, then `3` |
| 2 | `abc` **again** | `true` | `clear()`, message | still `abc` … |
| 3 | `abc` **again** | `true` | `clear()`, message | still `abc` … |
| … | … | `true` | forever | nothing changes |

1. **The error state:** after the failed read, `clear()` removes it, so another read can run.
2. **In the input,** `abc` with its line end stays: `clear()` removes nothing.
3. **The next read** meets the same `abc`, fails again, and so on, round and round. The program never gets to `3`, and `eof()` doesn't give `true`, because the data doesn't run out. The loop prints the question and the message forever.
4. **The missing step is discarding the rest of the line:** `std::getline(std::cin, discarded_line);` after `clear()`, and after it a check that the data hasn't run out.
5. That's how the program in section 7 works.

</details>

<details>
<summary>Section 11: the mission, putting a shipment together</summary>

<!-- example: shipment -->
```cpp
#include <iostream>
#include <string>

int main() {
    const int target{10};
    int collected{0};
    int batch{0};
    bool input_ended{false};

    while (collected < target && !input_ended) {
        std::cout << "Enter batch size (1-4):\n";
        std::cin >> batch;

        if (!std::cin.fail()) {
            if (batch >= 1 && batch <= 4) {
                collected += batch;
                std::cout << "Collected: " << collected << "\n";
            } else {
                std::cout << "Batch size out of range\n";
            }
        } else if (std::cin.eof()) {
            input_ended = true;
        } else {
            std::cin.clear();
            std::string discarded_line{""};
            std::getline(std::cin, discarded_line);

            if (std::cin.fail() || std::cin.eof()) {
                input_ended = true;
            } else {
                std::cout << "Invalid integer input, try again\n";
            }
        }
    }

    if (collected >= target) {
        std::cout << "Target reached: " << collected << " items\n";
    } else {
        std::cout << "Input ended: " << collected << " items collected\n";
    }
}
```

| Attempt | What was read | `fail()` | `eof()` | What the program does | `collected` after the attempt |
|---|---|---|---|---|---|
| 1 | 2 | `false` | `false` | an acceptable batch, added | 2 |
| 2 | `abc` | `true` | `false` | `clear()`, the line discarded, message | 2 |
| 3 | 4 | `false` | `false` | an acceptable batch, added | 6 |
| 4 | 4 | `false` | `false` | an acceptable batch, added | 10 |

After the fourth attempt, `collected < target` gives `false`, so the loop ends and asks no further question.

- **Goal and progress:** `target` is the goal, and `collected` is the progress and the accumulator. The loop's condition combines the goal loop of lesson 4.4 with the end-of-data flag.
- **The sum changes in only one place:** after a successful read of a batch in the range. Values outside the range and bad text don't change it.
- **The order after a failed read:** first `eof()`, i.e. the end of the data and the end of the attempts. Only otherwise `clear()`, `getline`, and another check for the end of the data.
- **After the loop,** the sum decides the result: `collected >= target` means success. Otherwise the loop was ended by the end of the data.
- **The ending:** every accepted batch is at least 1 item, so with valid batches the goal is reached after at most 10 accepted batches. The total number of attempts isn't limited in advance, because the user can keep giving bad data. But all data is finite, and the end of the data always ends the loop.

</details>

**Previous lesson:** [Lesson 4.5: Asking again for a valid value](lesson_05_ask_again.en.md) · **Next lesson:** [Lesson 4.7: The program repeats actions (the Module 4 test)](lesson_07_the_program_repeats.en.md) · [Course overview](../../README.en.md)

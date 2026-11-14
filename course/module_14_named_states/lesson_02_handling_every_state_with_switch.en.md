# Lesson 14.2: Handling every state with `switch`

[Polski](lesson_02_handling_every_state_with_switch.md) · **English** · [Course overview](../../README.en.md)

> **Module 14, lesson 2** · about 80–100 minutes, can be split into two sessions (sections 1–7, then the mission)
> **You need:** your `cpp-workspace` folder and the original `lesson_05_first_program` project, as before. You won't need the debugger in this lesson.
> **Pilot version.** The programs in this lesson are checked automatically on Windows, Ubuntu and macOS, together with their exit codes. The program that mustn't build is checked together with the place of its first error. Compiler warnings aren't checked automatically.

## Before you start

This lesson assumes that you:

- define an `enum class` type, compare its values, and write the function `status_text`, which turns a state into text (lesson 14.1);
- write chains of `if` conditions (lessons 3.1–3.3) and functions with several `return`s, where the first one that runs ends the function (lessons 5.3–5.4);
- write one-file test programs with the function `check_text` that end with exit code 1 when a check fails (lessons 13.1–13.3);
- choose test cases so that they tell a correct function from a version with a bug (lesson 13.2).

## The situation

We're back at the online shop of lesson 14.1. The function `status_text` has a separate `if` condition for each of the three order states. It works, but to be sure that it handles every state, you have to read every condition in turn. The warehouse also needs a second function: a different next action for each state.

In this lesson you'll answer the question: **how do you write "do something different for each state" in one place, and what won't this construct check for you?**

After this lesson you will:

- recognise a chain of `if`s that compares one value with consecutive states as a candidate for `switch`;
- write a `switch` statement with a `case` label for each value of an `enum class` type;
- end the handling of a state with `return` when the function should return its result right away, or with `break` when the function still has something to do after the `switch`;
- recognise fallthrough to the next label when a `break` is missing, and catch it with a test;
- decide deliberately whether a `switch` needs a `default` label;
- tell apart a compile error, a compiler warning and a bug in behaviour, which only a test catches.

## 1. The same choice in one place: `switch`

In lesson 14.1 the function `status_text` turned an order's state into text with three `if` conditions:

<!-- fragment -->
```cpp
std::string status_text(OrderStatus status) {
    if (status == OrderStatus::received) {
        return "received";
    }

    if (status == OrderStatus::preparing) {
        return "preparing";
    }

    if (status == OrderStatus::sent) {
        return "sent";
    }

    return "unknown";
}
```

Look at these conditions. Each one compares **the same variable**, `status`, with another value of **the same type**, `OrderStatus`. To be sure that the function handles every state, you have to read all three conditions and check that each one has `status` in it, that no state is repeated and that none is missing.

For this situation, one value with a few known, named possibilities, C++ has a construct of its own: the **`switch` statement**. The same function looks like this with it:

<!-- fragment -->
```cpp
std::string status_text(OrderStatus status) {
    switch (status) {
        case OrderStatus::received:
            return "received";
        case OrderStatus::preparing:
            return "preparing";
        case OrderStatus::sent:
            return "sent";
    }

    return "unknown";
}
```

- `switch (status)` starts the `switch` statement. The parentheses hold the value by which the program chooses what to do. Here it's the variable `status`. The program evaluates it once, at the start.
- The braces after the parentheses enclose the whole body of the `switch`.
- `case OrderStatus::received:` is a **`case` label**. It names one value and marks the place where the program starts when `status` has exactly that value. After the word `case` comes the name of the value together with the name of the type, as in lesson 14.1, and the label ends with a **colon**, not a semicolon.
- Below the label are the statements for this value. Here it's one statement, `return "received";`. As in lesson 5.4, `return` ends the whole function right away and hands over its result.
- Each of the three states has a label of its own. We indent the labels one level deeper than `switch`, and the statements below them one level more, so you can see what belongs to which label.
- **After the `switch` comes `return "unknown";`**, the same fallback as in lesson 14.1. Each of the three states has its label and ends the function earlier. The function still has a path on which no label matches, though: then the program skips the whole body of the `switch` and reaches this line. A function that promises a result must return one on every path (lesson 5.4), this one too.

**The contract doesn't change.** The structure of the function changed, not its results:

| State | Text returned by `status_text` |
|---|---|
| `OrderStatus::received` | `"received"` |
| `OrderStatus::preparing` | `"preparing"` |
| `OrderStatus::sent` | `"sent"` |

**When `switch`, and when `if`?** A `switch` is readable when you choose by one value that has a few known possibilities, and do something different for each: the labels form a list of the handled states. You stay with a chain of `if`s when the conditions differ, for example the range `count >= 1 && count <= 24`, or when you compare texts. The value in the parentheses of a `switch` must be a whole number, for example an `int`, or a value of an enumeration type. You can't use the text of a `std::string` in a `switch`, which is why `parse_status` from lesson 14.1 stays with `if`.

The full program:

<!-- example: order_switch -->
```cpp
#include <iostream>
#include <string>

enum class OrderStatus {
    received,
    preparing,
    sent
};

std::string status_text(OrderStatus status) {
    switch (status) {
        case OrderStatus::received:
            return "received";
        case OrderStatus::preparing:
            return "preparing";
        case OrderStatus::sent:
            return "sent";
    }

    return "unknown";
}

int main() {
    OrderStatus status{OrderStatus::received};
    std::cout << "Order: " << status_text(status) << "\n";

    status = OrderStatus::sent;
    std::cout << "Order: " << status_text(status) << "\n";
}
```

**This is the first required run.** In `cpp-workspace`, create a folder `lesson_14_2`, copy `main.cpp` and `CMakeLists.txt` from the original `lesson_05_first_program` into it, and open it in CLion. Replace the contents of `main.cpp` with this program. **Predict** what it prints, then build it and run it. Leave `CMakeLists.txt` unchanged. You type the later programs of this lesson into the same `main.cpp`.

<details>
<summary>Standard output</summary>

<!-- output: order_switch -->
```text
Order: received
Order: sent
```

</details>

## 2. How `switch` works

The program runs a `switch` in a few steps:

| Step | What the program does |
|---|---|
| 1 | Evaluates the value in the parentheses of the `switch`. |
| 2 | Looks for the `case` label with that value. |
| 3 | Goes to the label it found and starts running statements from there. |
| 4 | Runs the following statements downwards, until something ends the execution or it reaches the closing brace of the `switch`. |
| 5 | When no `case` label matches, it goes to the `default` label if the `switch` has one (section 6). If it doesn't, it skips the whole body of the `switch`. |

For `status_text(OrderStatus::preparing)` the program evaluates `status`, finds the label `case OrderStatus::preparing:`, runs `return "preparing";`, and the function ends. The statement below the label `received` doesn't run, because the program started lower down.

**A label isn't an `if`.** In a chain of `if`s each condition has its own block in braces. The program checks the conditions in turn and runs the block of the one that holds. In a `switch` the program only chooses **the place where it starts**. A `case` label has no braces of its own and closes nothing: it's a marker of a place in the code. Once execution has started, the program doesn't check the following labels. If it reaches the next label, it passes it and runs the statements below it.

In `status_text` this causes no trouble, because below each label there's a `return`, which ends the whole function before the program reaches the next label. In section 3 you'll see a function where the labels must end differently.

**The key rule of this lesson:** a `switch` chooses where to start. A `case` label doesn't end the handling of a state by itself. You write the end explicitly, for example with `return` or `break`.

## 3. `return` leaves the function, `break` leaves the `switch`

The warehouse needs a second function: what has to be done with an order in a given state.

**The contract of `next_step`:**

| State | Next action |
|---|---|
| `OrderStatus::received` | `"Confirm order"` |
| `OrderStatus::preparing` | `"Pack order"` |
| `OrderStatus::sent` | `"Track delivery"` |

We'll write this function differently from `status_text`. The labels don't return the result themselves; they assign a text to a variable, and the function returns it once, after the `switch`:

<!-- fragment -->
```cpp
std::string next_step(OrderStatus status) {
    std::string action{"unknown"};

    switch (status) {
        case OrderStatus::received:
            action = "Confirm order";
            break;
        case OrderStatus::preparing:
            action = "Pack order";
            break;
        case OrderStatus::sent:
            action = "Track delivery";
            break;
    }

    return action;
}
```

- `std::string action{"unknown"};` creates a variable for the result. It starts from the fallback text, like `status_text`: if no label matched, the `switch` wouldn't change `action`, and the function would return `"unknown"`.
- Below each label are two statements: the assignment of a text and `break;`.
- **`break;` exits the `switch`.** The program leaves its body and goes to the first statement after the closing brace of the `switch`. Here that's `return action;`.
- **`break` doesn't end the function.** It ends only the `switch`. Only `return action;` ends the function.
- In this lesson `break` is always inside a `switch`, and it ends that `switch`.

**What happens to `action` after `break`?** Nothing: the variable keeps the text that the label assigned. For `OrderStatus::preparing` the program assigns `"Pack order"`, `break` ends the `switch`, and `return action;` returns `"Pack order"`. `break` erases nothing and doesn't stop the program. It only changes the place where the program carries on.

| | `return` | `break` |
|---|---|---|
| What it ends | the whole function | only the `switch` |
| Where the program carries on | where the function was called, with its result | at the first statement after the `switch`, in the same function |
| When you use it | when the result is known right away, below the label | when the function still has something to do after the `switch`, for example return the collected result |

**After `return` you don't need `break`.** In `status_text` no label has a `break`, and that's how it should be: `return` ends the whole function, so a statement below it would never run. Instead of the rule "a `break` after every label", ask yourself: **how does this label end, and where does the program carry on?**

The full program with both functions:

<!-- example: order_next_step -->
```cpp
#include <iostream>
#include <string>

enum class OrderStatus {
    received,
    preparing,
    sent
};

std::string status_text(OrderStatus status) {
    switch (status) {
        case OrderStatus::received:
            return "received";
        case OrderStatus::preparing:
            return "preparing";
        case OrderStatus::sent:
            return "sent";
    }

    return "unknown";
}

std::string next_step(OrderStatus status) {
    std::string action{"unknown"};

    switch (status) {
        case OrderStatus::received:
            action = "Confirm order";
            break;
        case OrderStatus::preparing:
            action = "Pack order";
            break;
        case OrderStatus::sent:
            action = "Track delivery";
            break;
    }

    return action;
}

int main() {
    OrderStatus status{OrderStatus::received};
    std::cout << status_text(status) << ": " << next_step(status) << "\n";

    status = OrderStatus::preparing;
    std::cout << status_text(status) << ": " << next_step(status) << "\n";

    status = OrderStatus::sent;
    std::cout << status_text(status) << ": " << next_step(status) << "\n";
}
```

**This is the second required run.** Replace the contents of `main.cpp` with this program. **Predict** all three lines of the output, then build the program and run it.

<details>
<summary>Standard output</summary>

<!-- output: order_next_step -->
```text
received: Confirm order
preparing: Pack order
sent: Track delivery
```

</details>

## 4. A test program: every state, both functions

Each label is a separate path through the function. A mistake below one label spoils the result for one state only, so you check both functions **for every state**. The expected results come from the contracts of sections 1 and 3:

| State | `status_text` | `next_step` |
|---|---|---|
| `received` | `"received"` | `"Confirm order"` |
| `preparing` | `"preparing"` | `"Pack order"` |
| `sent` | `"sent"` | `"Track delivery"` |

Both functions return text, so `check_text` from lesson 13.3 is enough. There are six checks, one for each cell of the table that holds a result.

**This is the third required run. It has three stages:** now you'll run the tests of the correct functions, in section 5 the same tests after removing one `break`, and finally again after the fix. Replace the contents of `main.cpp` with the program below. You can copy the function `check_text` from lesson 13.3, and the state functions from sections 1 and 3. **Predict** the last line of the output before you run the program.

<details>
<summary>The full test program</summary>

<!-- example: order_switch_tests -->
```cpp
#include <iostream>
#include <string>

enum class OrderStatus {
    received,
    preparing,
    sent
};

std::string status_text(OrderStatus status) {
    switch (status) {
        case OrderStatus::received:
            return "received";
        case OrderStatus::preparing:
            return "preparing";
        case OrderStatus::sent:
            return "sent";
    }

    return "unknown";
}

std::string next_step(OrderStatus status) {
    std::string action{"unknown"};

    switch (status) {
        case OrderStatus::received:
            action = "Confirm order";
            break;
        case OrderStatus::preparing:
            action = "Pack order";
            break;
        case OrderStatus::sent:
            action = "Track delivery";
            break;
    }

    return action;
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

    check_text("status_text(received)", "received", status_text(OrderStatus::received), checks, failed);
    check_text("status_text(preparing)", "preparing", status_text(OrderStatus::preparing), checks, failed);
    check_text("status_text(sent)", "sent", status_text(OrderStatus::sent), checks, failed);

    check_text("next_step(received)", "Confirm order", next_step(OrderStatus::received), checks, failed);
    check_text("next_step(preparing)", "Pack order", next_step(OrderStatus::preparing), checks, failed);
    check_text("next_step(sent)", "Track delivery", next_step(OrderStatus::sent), checks, failed);

    std::cout << "Checks: " << checks << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

</details>

<details>
<summary>Standard output</summary>

<!-- output: order_switch_tests -->
```text
PASS status_text(received)
PASS status_text(preparing)
PASS status_text(sent)
PASS next_step(received)
PASS next_step(preparing)
PASS next_step(sent)
Checks: 6, failed: 0
```

Under the output, CLion adds `Process finished with exit code 0`.

</details>

- **6 checks:** three each for `status_text` and `next_step`, one for each state.
- **The expected results are ready strings from the tables**, not the results of a second call of the function under test (lesson 13.1).

## 5. Diagnostic: a missing `break`

Someone edits `next_step` and carelessly removes one line: the `break;` below `action = "Confirm order";`. The function now looks like this:

<!-- fragment -->
```cpp
std::string next_step(OrderStatus status) {
    std::string action{"unknown"};

    switch (status) {
        case OrderStatus::received:
            action = "Confirm order";
        case OrderStatus::preparing:
            action = "Pack order";
            break;
        case OrderStatus::sent:
            action = "Track delivery";
            break;
    }

    return action;
}
```

It still has three labels and three assignments, and each line on its own looks correct.

**Stages 2 and 3 of the third required run.** Follow the steps in order:

1. **Predict** before you change anything: will the program build? If it will, which of the six checks will fail, and what will its `FAIL` line print after `actual`?
2. In the test program of section 4, remove the line `break;` below `action = "Confirm order";`. Change nothing else, neither the tests nor the expected results.
3. Build the program. Check whether the compiler reported anything.
4. Run the tests. Write down the `FAIL` line, the summary and the exit code.
5. Restore the `break;` and run the same tests once more.

<details>
<summary>What happens and how to fix it: open after steps 1–5</summary>

**Stage:** the program's behaviour. The program builds: every line is valid C++. With the settings of lesson 0.5, Clang reports neither an error nor a warning. We check this program automatically with additional warnings too, treated as errors, and it still builds without a word. Some compilers can warn about fallthrough to the next label, but only with suitable settings. Don't rely on that: the absence of a warning doesn't mean that the function is correct.

**What happens for `OrderStatus::received`:**

| Step | What the program does | `action` after this step |
|---|---|---|
| 1 | Creates `action` with the fallback text. | `"unknown"` |
| 2 | The `switch` goes to the label `case OrderStatus::received:`. | `"unknown"` |
| 3 | Runs `action = "Confirm order";`. | `"Confirm order"` |
| 4 | There's no `break`, so it goes on downwards and passes the label `case OrderStatus::preparing:`. | `"Confirm order"` |
| 5 | Runs `action = "Pack order";`. The new text replaces the previous one. | `"Pack order"` |
| 6 | `break;` ends the `switch`. | `"Pack order"` |
| 7 | `return action;` returns the result. | returns `"Pack order"` |

This is **fallthrough** to the next label: without `break`, execution doesn't end with the statements of one label but flows on, into the statements below the next one. Exactly as section 2 describes.

**The map of effects:**

| Call | Expected result | Actual result | Test |
|---|---|---|---|
| `next_step(OrderStatus::received)` | `"Confirm order"` | `"Pack order"` | `FAIL` |
| `next_step(OrderStatus::preparing)` | `"Pack order"` | `"Pack order"` | `PASS` |
| `next_step(OrderStatus::sent)` | `"Track delivery"` | `"Track delivery"` | `PASS` |
| `status_text` for the three states | as in the table of section 4 | unchanged | `PASS` |

For `preparing` and `sent` the program starts lower down, at their own labels, and reaches their own `break`s. The missing `break` is higher up, so it doesn't affect these states. That's why the bug shows in one test only. A suite that checked `next_step` only for `preparing` and `sent` would pass completely (lesson 13.2).

The test program with the `break` removed, and no other change:

<!-- example: order_switch_tests_fallthrough exit=1 -->
```cpp
#include <iostream>
#include <string>

enum class OrderStatus {
    received,
    preparing,
    sent
};

std::string status_text(OrderStatus status) {
    switch (status) {
        case OrderStatus::received:
            return "received";
        case OrderStatus::preparing:
            return "preparing";
        case OrderStatus::sent:
            return "sent";
    }

    return "unknown";
}

std::string next_step(OrderStatus status) {
    std::string action{"unknown"};

    switch (status) {
        case OrderStatus::received:
            action = "Confirm order";
        case OrderStatus::preparing:
            action = "Pack order";
            break;
        case OrderStatus::sent:
            action = "Track delivery";
            break;
    }

    return action;
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

    check_text("status_text(received)", "received", status_text(OrderStatus::received), checks, failed);
    check_text("status_text(preparing)", "preparing", status_text(OrderStatus::preparing), checks, failed);
    check_text("status_text(sent)", "sent", status_text(OrderStatus::sent), checks, failed);

    check_text("next_step(received)", "Confirm order", next_step(OrderStatus::received), checks, failed);
    check_text("next_step(preparing)", "Pack order", next_step(OrderStatus::preparing), checks, failed);
    check_text("next_step(sent)", "Track delivery", next_step(OrderStatus::sent), checks, failed);

    std::cout << "Checks: " << checks << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

<!-- output: order_switch_tests_fallthrough -->
```text
PASS status_text(received)
PASS status_text(preparing)
PASS status_text(sent)
FAIL next_step(received): expected "Confirm order", actual "Pack order"
PASS next_step(preparing)
PASS next_step(sent)
Checks: 6, failed: 1
```

Exit code: 1.

**The fix:** restore the `break;` below `action = "Confirm order";`. The program is the same as in section 4 again. The same tests, with the same expected results, print `PASS` six times and `Checks: 6, failed: 0`, and the program ends with exit code 0.

</details>

## 6. The `default` label and a new state

The shop introduces a fourth state: a cancelled order. Someone adds the value `cancelled` to the type, but forgets to update `status_text`:

<!-- fragment -->
```cpp
enum class OrderStatus {
    received,
    preparing,
    sent,
    cancelled
};

std::string status_text(OrderStatus status) {
    switch (status) {
        case OrderStatus::received:
            return "received";
        case OrderStatus::preparing:
            return "preparing";
        case OrderStatus::sent:
            return "sent";
    }

    return "unknown";
}
```

Such a program builds. `cancelled` has no label, so for a cancelled order the program skips the body of the `switch`, and the function returns `"unknown"`. With the settings of lesson 0.5, though, Clang prints a **compiler warning** during the build, at the line `switch (status) {`:

```text
warning: enumeration value 'cancelled' not handled in switch [-Wswitch]
```

The compiler knows all the values of the type `OrderStatus` and sees that one of them has no label in this `switch`. In the square brackets it gives the name of this warning, `-Wswitch`. That's why a `switch` is a good place to handle all the states: after a new value is added, the compiler can point to the `switch` that needs updating.

Keep in mind, though:

- it's a **warning**, not an error: the program builds and runs, and only returns the fallback text for `cancelled`;
- whether such a warning appears, and how it's worded, depends on the compiler and its settings;
- with a setting that treats warnings as errors, the build stops, and the message starts with `error:` instead of `warning:`;
- **the absence of a warning doesn't prove that every state is handled correctly.** The compiler only checks that every value has a label, not that the label does the right thing.

This warning isn't checked automatically, so this code is only for reading.

**The `default` label.** A `switch` can have one special label, `default:`. The program starts from it when no `case` label matches:

<!-- example: order_default -->
```cpp
#include <iostream>
#include <string>

enum class OrderStatus {
    received,
    preparing,
    sent,
    cancelled
};

std::string status_text(OrderStatus status) {
    switch (status) {
        case OrderStatus::received:
            return "received";
        case OrderStatus::preparing:
            return "preparing";
        case OrderStatus::sent:
            return "sent";
        default:
            return "unknown";
    }
}

int main() {
    std::cout << status_text(OrderStatus::sent) << "\n";
    std::cout << status_text(OrderStatus::cancelled) << "\n";
}
```

<!-- output: order_default -->
```text
sent
unknown
```

- `default:` usually comes at the end of the `switch`. It handles **every value that has no `case` label of its own**.
- `default` is **optional**. The earlier functions of this lesson don't have one, and they work correctly.
- Here the fallback has moved inside the `switch`. Every path through the `switch`, the one through `default` too, ends with a `return`, so there's no final `return` after the `switch` any more.
- **The compiler stays silent.** `cancelled` has no label of its own, but it goes to `default`, so from the compiler's point of view every value is handled. The warning about an unhandled value doesn't appear, and the program builds and returns `unknown` for a cancelled order.

You don't have to run this program: it's checked automatically, and you can see its result above.

**`default` doesn't replace the labels.** It doesn't know what `cancelled` is. It does the same for every value without a label of its own, including one that someone adds a year from now.

| | Without `default` | With `default` |
|---|---|---|
| A new state without a label | the program skips the `switch` and reaches the fallback after it | the program goes to `default` |
| The warning about an unhandled value | may appear | doesn't appear |
| What catches the oversight | the warning, if it appears, and a test of the new state | only a test of the new state |

**The rule of this lesson:** for an `enum class` type whose values you all know, write a `case` label for every value. Add `default` deliberately: when the same behaviour is truly correct for every value without a label of its own, future ones included. Don't add it just to make the compiler stop warning. With `default` or without it, only a test reliably catches an overlooked state, which is why you also add the tests of a value when you add it to the type.

## 7. Error, warning, test: what catches what

One more mistake while copying labels. The second label was meant to be about `preparing`, but the name `received` stayed in it:

<!-- broken: order_duplicate_case at=14:14 errors=1 error=^duplicate case value 'received' -->
```cpp
#include <iostream>
#include <string>

enum class OrderStatus {
    received,
    preparing,
    sent
};

std::string status_text(OrderStatus status) {
    switch (status) {
        case OrderStatus::received:
            return "received";
        case OrderStatus::received:
            return "preparing";
        case OrderStatus::sent:
            return "sent";
    }

    return "unknown";
}

int main() {
    std::cout << status_text(OrderStatus::preparing) << "\n";
}
```

This program won't build. You don't have to build it: like the program in section 6, it's checked automatically. The compiler reports one error on line 14, at the second label. Its message starts with `duplicate case value 'received'`: the value `received` already has a label. Clang also adds the note `note: previous case defined here`, which points to the first label, on line 12. Each value can have only one label in a `switch`, because otherwise the program wouldn't know which one to start from.

In this lesson you see four different situations. They aren't four names for the same problem:

| What happens | Example from this lesson | Is a program created | What catches it |
|---|---|---|---|
| **A compile error:** the code breaks a rule of the C++ language | two labels `case OrderStatus::received:` (this section) | no | the compiler, always |
| **A compiler warning:** the code is valid C++, but the compiler considers it suspicious | `cancelled` without a label and without `default` (section 6) | yes | the compiler, if this warning is turned on |
| **A warning treated as an error** | the same, with a setting that turns warnings into errors | no | the compiler, only with such a setting |
| **A bug in behaviour:** the program builds, but gives a wrong result | the missing `break` in `next_step` (section 5) | yes, without a word | a test |

The compiler checks the rules of the language and, where it can, warns about suspicious code. It doesn't know your contract, though: it doesn't know that the next action for `received` is `"Confirm order"`. Only a test checks that.

## 8. Mission: parking spaces

The car park below an office building shows on a board the state of each space and a short instruction for the driver. A space is available, reserved, occupied, or closed. Store this state as an enumeration type `ParkingSpace`, and handle it with two functions that use `switch`.

**The contract:**

| State | `space_text` | `parking_instruction` |
|---|---|---|
| `ParkingSpace::available` | `"available"` | `"Park here"` |
| `ParkingSpace::reserved` | `"reserved"` | `"Reservation required"` |
| `ParkingSpace::occupied` | `"occupied"` | `"Space occupied"` |
| `ParkingSpace::closed` | `"closed"` | `"Do not enter"` |

**The functions:**

- `std::string space_text(ParkingSpace state)`: the state's text from the table. Write it with a `switch` in which each label returns the result right away with `return`. After the `switch`, add the fallback, `"unknown"`.
- `std::string parking_instruction(ParkingSpace state)`: the driver's instruction from the table. Write it with a `switch` in which each label assigns a text to a variable and exits the `switch` with `break`. The variable starts from the fallback text, `"unknown"`, and the function has one `return`, after the `switch`.

**The rules:**

- In both functions each of the four values has a `case` label of its own. Write the labels in the order of the table.
- Don't add `default`.
- Don't solve the mission with a chain of `if`s. You can organise the checking function and `main` your own way.

In `cpp-workspace`, create a folder `parking_space`, copy `main.cpp` and `CMakeLists.txt` from the original `lesson_05_first_program` into it, and open it in CLion. Write everything in one file, `main.cpp`. Leave `CMakeLists.txt` unchanged.

**The order of work:**

1. **The test plan first.** Before you write any code, prepare a table of checks: the check's name, the call and the expected result from the contract, for both functions and each of the four values. Below it, add a prediction: which check will fail when `parking_instruction` lacks the `break` below the label `reserved`, and which text will then appear after `actual`.
2. Define `ParkingSpace` and write both functions.
3. Write the test program: `check_text` from lesson 13.3, the checks from your table, and at the end the summary and the exit code as in section 4.
4. **This is the fourth required run:** run the test program with the correct functions. Every check should print `PASS`, and the exit code should be 0.
5. **A deliberate bug.** In `parking_instruction`, remove the `break` below the label `ParkingSpace::reserved`. Don't change the tests or the expected results. **This is the fifth required run:** build the program and run the tests. Write down whether the compiler reported anything, which check failed, what it printed after `actual` and what the exit code is. Compare this with your prediction from step 1. Then restore the `break` and run the same tests once more.

You don't have to run any other versions. If you like, also check what happens when you remove the whole label `closed` from `parking_instruction`, together with its statements: what the compiler reports and which test fails.

### Success criteria

- [ ] The program builds as C++20, and `CMakeLists.txt` is the one from lesson 0.5.
- [ ] `ParkingSpace` is an `enum class` type with the four values of the contract.
- [ ] `space_text` uses a `switch`: each label ends the function with `return`, and the fallback comes after the `switch`.
- [ ] `parking_instruction` uses a `switch`: each label assigns a text and exits the `switch` with `break`, and the function has one `return`, after the `switch`.
- [ ] Both functions have a `case` label for each of the four values, no value is repeated, and the texts agree with the table letter for letter.
- [ ] No label falls through to the next one by accident.
- [ ] Neither function has `default`, and you can say what `default` would change for a new, fifth state.
- [ ] The test program checks both functions for each of the four values, and the expected results come from the table, not from calls of the functions under test.
- [ ] With the correct functions, every check passes and the exit code is 0.
- [ ] After removing the `break` below `reserved`, the program builds, only the check of `parking_instruction` for `reserved` prints `FAIL`, and the exit code is 1. The result agrees with your prediction, or you can explain the difference.
- [ ] After restoring the `break`, the same tests, unchanged, pass again with exit code 0.
- [ ] You can say why the mere fact that the program builds doesn't prove that every state is handled correctly.

When the result matches, you can save the project in Git, as in lesson 1.5: `main.cpp` and `CMakeLists.txt`, without the build folder.

<details>
<summary>Hint 1: the values</summary>

How many values does `ParkingSpace` have, and how do you know that those are all of them? Each one needs a label of its own in each of the two functions, and a text of its own from the table. How do you check that none is missing and none is repeated? Compare the number of `case` labels in each function with the number of rows in the table.

</details>

<details>
<summary>Hint 2: the control flow</summary>

In `space_text` the result for a given state is known right away, below the label. In `parking_instruction` the function returns its result only after the `switch`. Which statement ends the whole function, and which one only the `switch`? Where does the program carry on after each of them? Compare with the table in section 3.

</details>

<details>
<summary>Hint 3: the diagnostic</summary>

Suppose that below the label `reserved` the program has already assigned a text, but doesn't meet a `break`. Which statement is lower down, below the next label? What happens to the text that's already in the variable, and what does the function return in the end? Which of your checks will notice it, and which will pass unchanged?

</details>

## 9. When something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| An error with `expected ':' after 'case'` | The label ends with a semicolon instead of a colon. | End the label with a colon: `case ParkingSpace::reserved:`. |
| An error with `use of undeclared identifier 'reserved'` | After `case` comes the name of a value without the name of the type. | Write `case ParkingSpace::reserved:`. |
| An error with `duplicate case value` | Two labels have the same value, for example after copying (section 7). | Change the second one to the value that's missing. |
| An error with `value of type 'OrderStatus' is not implicitly convertible to 'ParkingSpace'` | A label has a value of another type than the value in the parentheses of the `switch`, for example after copying from section 1. | Use a value of the type `ParkingSpace`. |
| An error with `statement requires expression of integer type` at `switch` | The parentheses of the `switch` hold the text of a `std::string`. | `switch` works with whole numbers and enumeration types. Compare texts in a chain of `if`s, as in `parse_status` from lesson 14.1. |
| A warning with `enumeration value '…' not handled in switch` | One of the values has no `case` label in this `switch` (section 6). | Add a label for this value, and check its result in the tests. |
| A `FAIL` for one state, with the text of the following label after `actual` | The label of this state lacks a `break`, so execution falls through to the next one (section 5). | Add `break;` after the assignment. |
| A `FAIL` for one state, with `unknown` after `actual` | This value has no `case` label, so the function returns the fallback text. | Add a label with the right text. |

## 10. Explain

Answer in your own words, preferably in writing. Only then compare with the example answers.

1. When is a `switch` more readable than several `if` conditions, and when do you stay with `if`?
2. What goes in the parentheses of a `switch`, and what does the label `case OrderStatus::sent:` mean?
3. Does a `case` label end the execution of the statements below the previous label?
4. What does `break` do, and what does `return` do? Where does the program carry on after each of them?
5. What happens to the value of `action` in `next_step` after `break` runs?
6. Is a `break` needed after a `return` below a label?
7. Why does removing the `break` below `"Confirm order"` change the result for `received` only?
8. What is `default` for, and why can it hide a new state that nobody added to the `switch`?
9. Does the absence of a compiler warning prove that a `switch` handles every state correctly?
10. How does the error with two `received` labels differ from the bug with the missing `break`?
11. Why do you test a function for every value of an `enum class`, not just for one or two?

<details>
<summary>Example answers</summary>

1. When you choose by one value with a few known possibilities, for example an `enum class` state, and do something different for each: the labels form a list of the handled states. You stay with `if` when the conditions differ, for example ranges or comparisons of several variables, and when you compare texts, because `switch` doesn't work with `std::string`.
2. The value by which the program chooses, for example the variable `status`. The label marks the place where the program starts when that value is `OrderStatus::sent`.
3. No. A label only marks a starting place. If execution reaches the next label, the program passes it and runs the statements below it.
4. `break` ends the `switch`: the program carries on from the first statement after the `switch`, in the same function. `return` ends the whole function: the program goes back to where the function was called, with its result.
5. It keeps the text assigned below the label. `break` only moves execution past the `switch`, to `return action;`, which returns that text.
6. No. `return` ends the whole function, so a `break` below it would never run.
7. For `received`, execution falls through to the label `preparing` and assigns `"Pack order"`, which replaces `"Confirm order"`. For `preparing` and `sent` the program starts at their own labels, lower down, and reaches their own `break`s.
8. `default` is the starting place for every value without a `case` label of its own. A new state goes to `default` and gets its behaviour, for example the fallback text. The compiler considers it handled, so it doesn't warn, and the program builds and keeps running.
9. No. The warning may be turned off, or the compiler may not have it at all, and `default` silences it. Even when every value has a label, a label can return the wrong text or lack its `break`. The missing `break` of section 5 builds without warnings.
10. Two labels with the same value break a rule of the language, so the program doesn't build, and the compiler always reports it. A missing `break` is valid C++: the program builds and runs, it just gives a wrong result, which only a test catches.
11. Because each label is a separate path through the function, and a bug below one label changes the result for one state only. A suite that skips this state passes despite the bug, like the checks of `preparing` and `sent` in section 5.

</details>

## Summary

- A `switch` chooses by one value, for example an `enum class` state. Each `case` label names one value and marks the place where the program starts.
- **A label ends nothing by itself.** Once it has entered a label, the program runs the following statements downwards, the ones below the next labels too, until something ends the execution.
- `return` ends the whole function and needs no `break`. `break` ends only the `switch`, and the program carries on from the statement after it.
- A missing `break` causes **fallthrough** to the next label: the program builds, and the result for one state is wrong. A test of that state catches it.
- `default` handles every value without a label of its own, a new one too. It's optional, and its presence can silence the warning about an unhandled value. You add it deliberately, not out of habit.
- A compile error, a warning, a warning treated as an error, and a bug in behaviour are four different things. Warnings help, but they don't replace tests.
- You test every value of an enumeration type in every function that handles it.

## What's next

The functions in this lesson take a state and turn it into text. In [lesson 14.3: A function explains why it refused](lesson_03_function_explains_refusal.en.md) an enumeration type becomes a function's result: a function that refuses will say, with a named result, why it refused.

---

## Example solutions

Look here **after your own attempt**. Your check names, variable names and the order of checks may differ, as long as they meet the contract and the success criteria.

<details>
<summary>Section 8: the mission, parking spaces</summary>

**The test plan:**

| Check | Call | Expected result |
|---|---|---|
| `space_text(available)` | `space_text(ParkingSpace::available)` | `"available"` |
| `space_text(reserved)` | `space_text(ParkingSpace::reserved)` | `"reserved"` |
| `space_text(occupied)` | `space_text(ParkingSpace::occupied)` | `"occupied"` |
| `space_text(closed)` | `space_text(ParkingSpace::closed)` | `"closed"` |
| `parking_instruction(available)` | `parking_instruction(ParkingSpace::available)` | `"Park here"` |
| `parking_instruction(reserved)` | `parking_instruction(ParkingSpace::reserved)` | `"Reservation required"` |
| `parking_instruction(occupied)` | `parking_instruction(ParkingSpace::occupied)` | `"Space occupied"` |
| `parking_instruction(closed)` | `parking_instruction(ParkingSpace::closed)` | `"Do not enter"` |

**The prediction:** without the `break` below `reserved`, execution falls through to the label `occupied`, which assigns `"Space occupied"`. Only `parking_instruction(reserved)` fails, with `"Space occupied"` after `actual`. The other seven checks pass, and the exit code is 1.

**`main.cpp`:**

<!-- example: parking_space_tests -->
```cpp
#include <iostream>
#include <string>

enum class ParkingSpace {
    available,
    reserved,
    occupied,
    closed
};

std::string space_text(ParkingSpace state) {
    switch (state) {
        case ParkingSpace::available:
            return "available";
        case ParkingSpace::reserved:
            return "reserved";
        case ParkingSpace::occupied:
            return "occupied";
        case ParkingSpace::closed:
            return "closed";
    }

    return "unknown";
}

std::string parking_instruction(ParkingSpace state) {
    std::string instruction{"unknown"};

    switch (state) {
        case ParkingSpace::available:
            instruction = "Park here";
            break;
        case ParkingSpace::reserved:
            instruction = "Reservation required";
            break;
        case ParkingSpace::occupied:
            instruction = "Space occupied";
            break;
        case ParkingSpace::closed:
            instruction = "Do not enter";
            break;
    }

    return instruction;
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

    check_text("space_text(available)", "available", space_text(ParkingSpace::available), checks, failed);
    check_text("space_text(reserved)", "reserved", space_text(ParkingSpace::reserved), checks, failed);
    check_text("space_text(occupied)", "occupied", space_text(ParkingSpace::occupied), checks, failed);
    check_text("space_text(closed)", "closed", space_text(ParkingSpace::closed), checks, failed);

    check_text("parking_instruction(available)", "Park here", parking_instruction(ParkingSpace::available), checks, failed);
    check_text("parking_instruction(reserved)", "Reservation required", parking_instruction(ParkingSpace::reserved), checks, failed);
    check_text("parking_instruction(occupied)", "Space occupied", parking_instruction(ParkingSpace::occupied), checks, failed);
    check_text("parking_instruction(closed)", "Do not enter", parking_instruction(ParkingSpace::closed), checks, failed);

    std::cout << "Checks: " << checks << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

<!-- output: parking_space_tests -->
```text
PASS space_text(available)
PASS space_text(reserved)
PASS space_text(occupied)
PASS space_text(closed)
PASS parking_instruction(available)
PASS parking_instruction(reserved)
PASS parking_instruction(occupied)
PASS parking_instruction(closed)
Checks: 8, failed: 0
```

Exit code: 0.

- **`space_text`:** four labels, each ends the function with `return`, so none needs a `break`. The fallback comes after the `switch`.
- **`parking_instruction`:** four labels, each assigns a text and exits the `switch` with `break`. The only `return` comes after the `switch` and returns what the label assigned.
- **The last `break`, below `closed`:** after it there's only the closing brace of the `switch`, so without it the result would be the same. It's still worth writing: if someone added another label below `closed`, the missing `break` would become a bug.
- **Without `default`:** each of the four values has a label. If someone added a fifth state to the type, Clang could warn at both `switch`es. With `default` there'd be no warning, and the new state would quietly get the behaviour of `default`. In both versions, only a test of the new state reliably catches the oversight.

**The deliberate bug:** in `parking_instruction` there's no `break` below `instruction = "Reservation required";`. Only this one place changes, and the test program stays the same:

<!-- example: parking_space_tests_fallthrough exit=1 -->
```cpp
#include <iostream>
#include <string>

enum class ParkingSpace {
    available,
    reserved,
    occupied,
    closed
};

std::string space_text(ParkingSpace state) {
    switch (state) {
        case ParkingSpace::available:
            return "available";
        case ParkingSpace::reserved:
            return "reserved";
        case ParkingSpace::occupied:
            return "occupied";
        case ParkingSpace::closed:
            return "closed";
    }

    return "unknown";
}

std::string parking_instruction(ParkingSpace state) {
    std::string instruction{"unknown"};

    switch (state) {
        case ParkingSpace::available:
            instruction = "Park here";
            break;
        case ParkingSpace::reserved:
            instruction = "Reservation required";
        case ParkingSpace::occupied:
            instruction = "Space occupied";
            break;
        case ParkingSpace::closed:
            instruction = "Do not enter";
            break;
    }

    return instruction;
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

    check_text("space_text(available)", "available", space_text(ParkingSpace::available), checks, failed);
    check_text("space_text(reserved)", "reserved", space_text(ParkingSpace::reserved), checks, failed);
    check_text("space_text(occupied)", "occupied", space_text(ParkingSpace::occupied), checks, failed);
    check_text("space_text(closed)", "closed", space_text(ParkingSpace::closed), checks, failed);

    check_text("parking_instruction(available)", "Park here", parking_instruction(ParkingSpace::available), checks, failed);
    check_text("parking_instruction(reserved)", "Reservation required", parking_instruction(ParkingSpace::reserved), checks, failed);
    check_text("parking_instruction(occupied)", "Space occupied", parking_instruction(ParkingSpace::occupied), checks, failed);
    check_text("parking_instruction(closed)", "Do not enter", parking_instruction(ParkingSpace::closed), checks, failed);

    std::cout << "Checks: " << checks << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

<!-- output: parking_space_tests_fallthrough -->
```text
PASS space_text(available)
PASS space_text(reserved)
PASS space_text(occupied)
PASS space_text(closed)
PASS parking_instruction(available)
FAIL parking_instruction(reserved): expected "Reservation required", actual "Space occupied"
PASS parking_instruction(occupied)
PASS parking_instruction(closed)
Checks: 8, failed: 1
```

Exit code: 1.

- **The compiler:** reports nothing. The program is valid C++.
- **The run for `reserved`:** the label `reserved` assigns `"Reservation required"`, but has no `break`, so execution falls through to the label `occupied` and assigns `"Space occupied"`. Only the `break` below `occupied` ends the `switch`.
- **The tests:** only `parking_instruction(reserved)` fails. `occupied` starts at its own label, and nothing changed in `space_text`.
- **If your labels are in another order,** the text of the label that comes below `reserved` in your code appears after `actual`. If `reserved` were the last one, removing its `break` wouldn't change anything: there's no statement after it.

**After the fix:** after restoring the `break`, the program is the same as the first version again. The same eight checks print `PASS` and `Checks: 8, failed: 0`, and the exit code is 0.

**Self-assessment.** Compare your work with the success criteria in section 8. Check in particular:
- that you can explain why the labels in `space_text` need no `break`, while each one in `parking_instruction` needs one;
- that both functions have four labels each, and no value is repeated;
- that the expected results in the tests are strings from the contract;
- that your prediction from step 1 agreed with the result of step 5, and if it didn't, that you can explain the difference;
- that you can say what `default` would change in each of the two functions.

If the answer to one of these is "no", go back to the corresponding section of the lesson before moving on.

</details>

**Previous lesson:** [Lesson 14.1: A named state instead of text](lesson_01_named_state_instead_of_text.en.md) · **Next lesson:** [Lesson 14.3: A function explains why it refused](lesson_03_function_explains_refusal.en.md) · [Course overview](../../README.en.md)

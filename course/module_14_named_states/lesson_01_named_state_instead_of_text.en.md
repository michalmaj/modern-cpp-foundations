# Lesson 14.1: A named state instead of text

[Polski](lesson_01_named_state_instead_of_text.md) · **English** · [Course overview](../../README.en.md)

> **Module 14, lesson 1** · about 75–90 minutes, can be split into two sessions (sections 1–8, then the mission)
> **You need:** your `cpp-workspace` folder and the original `lesson_05_first_program` project, as before. You won't need the debugger in this lesson.
> **Pilot version.** The programs in this lesson are checked automatically on Windows, Ubuntu and macOS, together with their exit codes. The programs that mustn't build are checked together with the place of their first error.

## Before you start

This lesson assumes that you:

- compare values with `==` and `!=`, texts too (lessons 3.2 and 3.4);
- write `bool` functions, including ones that return the result of a comparison directly, for example `return count >= 1 && count <= 24;` (lessons 5.3–5.5);
- define your own type with `struct` and use it in functions (lessons 8.1 and 8.3);
- write a `bool` function that changes a result parameter `T&` only after checking, and leaves it unchanged when it refuses (lessons 9.2 and 10.4);
- write one-file test programs with the functions `check_bool` and `check_text` that end with exit code 1 when a check fails (lessons 13.1–13.3).

## The situation

An online shop tracks its orders. Each one is in one of three states: received, being prepared, or sent. So far we've stored such a state as text, like the `status` field of the cinema screenings in lesson 12.4: `"received"`, `"preparing"`, `"sent"`.

Text has one weakness: **every string is valid text**. If someone writes `"preparingg"` instead of `"preparing"` somewhere in the program, the compiler has nothing to report. The program builds, runs and does the wrong thing. In this lesson you'll answer the question: **can a state be stored so that only three names are allowed, and the compiler catches a typo in a name?**

After this lesson you will:

- recognise the problem of states stored as arbitrary strings;
- define an enumeration type with `enum class`, a closed set of named states;
- create variables of that type, compare states with `==` and `!=`, pass them to functions and return them from functions;
- turn a state into text for printing, and parse a state from text, in two separate functions;
- refuse an unknown name without changing the result;
- tell a typo in a state's name, which the compiler catches, from a bug that only tests catch.

## 1. A state stored as text

A warehouse packs the orders that are being prepared. This program checks an order's state and decides whether it needs packing:

<!-- example: order_text -->
```cpp
#include <iostream>
#include <string>

bool needs_packing(const std::string& status) {
    return status == "preparingg";
}

int main() {
    std::string status{"preparing"};

    if (needs_packing(status)) {
        std::cout << "Pack the order\n";
    } else {
        std::cout << "Nothing to pack\n";
    }
}
```

**Predict** what it prints. The order is being prepared, so it should be packed. Yet the program prints:

<!-- output: order_text -->
```text
Nothing to pack
```

The function `needs_packing` has a typo: `"preparingg"`, with two `g`s. The compiler doesn't report it, and it's right not to, because `"preparingg"` is perfectly valid text. Comparing two different texts simply gives `false`. The bug shows up only for someone who runs the program and notices the wrong result, or in a test that checks `needs_packing` for an order being prepared.

You don't have to run this program: it's checked automatically, and you can see its result above.

**Where the problem is:** the type `std::string` accepts every string. The program knows only three order states, but the type of the variable `status` doesn't know that. The agreement "only three strings are allowed" exists only in the heads of the people who write the code.

## 2. An enumeration type: `enum class`

C++ lets you define a type with a **closed set of named values**:

<!-- fragment -->
```cpp
enum class OrderStatus {
    received,
    preparing,
    sent
};
```

- `enum class` is two keywords that together start the definition of an **enumeration type**. Such a type lists all of its allowed values.
- `OrderStatus` is the **name of the type**. We write it like the names of the structs in Module 8, with a capital letter at the start of each word.
- `received`, `preparing` and `sent` are the **names of the values** of that type: its **enumerators**. Commas separate them. The type has no other values.
- A semicolon follows the closing brace, as after a `struct` definition.
- The definition comes before the functions that use the type, like a struct definition.

**These aren't strings.** `received` has no quotation marks, because it isn't text. It's the name of a value, just as `count` is the name of a variable. Each order state is now **a value of the type `OrderStatus`**, not an agreed-upon word.

C++ also has an older form of this construct, plain `enum`, without `class`. In this course we use `enum class`, because the name of its value is always written together with the name of the type. That way two different types can have a value with the same name, and the compiler won't let you mix up a state of one type with a state of the other.

## 3. A variable with a named state

You create a variable of the type `OrderStatus` like any other:

<!-- fragment -->
```cpp
OrderStatus status{OrderStatus::preparing};
```

- `OrderStatus` before the variable's name is its type, like `int` or `std::string`.
- `OrderStatus::preparing` names **one particular value**: the value `preparing` of the type `OrderStatus`. You know the `::` sign from `std::cout`: there it means the name `cout` from the standard library `std`, here the name `preparing` from the type `OrderStatus`.
- The name `preparing` alone, without `OrderStatus::`, won't work. You always write the values of an `enum class` together with the type.

The state changes with an ordinary assignment:

<!-- fragment -->
```cpp
status = OrderStatus::sent;
```

A variable of the type `OrderStatus` can only be assigned a value of the type `OrderStatus`. The string `"sent"` is text, not an order state, so `status = "sent";` won't build.

**The compiler checks the names of the type and of its values.** If you write `OrderStatus::sendt`, the compiler finds no such value in the type `OrderStatus` and reports an error before the program even exists. That's exactly what section 1 was missing.

## 4. Comparing states

The question "has the order been sent yet?" is a `bool` function:

<!-- fragment -->
```cpp
bool was_sent(OrderStatus status) {
    return status == OrderStatus::sent;
}
```

- You pass a parameter of the type `OrderStatus` by value, like an `int`: it's a small value, and the function doesn't change it.
- `==` compares two states: it gives `true` when they're the same enumerator. `!=` gives `true` when the values differ.
- The function returns the result of the comparison directly, like the functions in lesson 5.5.

The full program:

<!-- example: order_states -->
```cpp
#include <iostream>

enum class OrderStatus {
    received,
    preparing,
    sent
};

bool was_sent(OrderStatus status) {
    return status == OrderStatus::sent;
}

int main() {
    OrderStatus status{OrderStatus::received};

    if (status != OrderStatus::sent) {
        std::cout << "Order not sent yet\n";
    }

    status = OrderStatus::sent;

    if (was_sent(status)) {
        std::cout << "Order sent\n";
    }
}
```

**This is the first required run.** In `cpp-workspace`, create a folder `lesson_14_1`, copy `main.cpp` and `CMakeLists.txt` from the original `lesson_05_first_program` into it, and open it in CLion. Replace the contents of `main.cpp` with this program, build it and run it. Leave `CMakeLists.txt` unchanged. You type the later programs of this lesson into the same `main.cpp`.

<details>
<summary>Standard output</summary>

<!-- output: order_states -->
```text
Order not sent yet
Order sent
```

</details>

**One name for one state.** When the state was text, a sent order could be `"sent"` in one place of the program, `"shipped"` in another and `"dispatched"` in a third. Each of these strings is valid, and comparisons between them give `false`. Now a sent order is always `OrderStatus::sent`, because the type has no other name for this state.

`enum class` doesn't solve everything, though. A function that compares the state with `OrderStatus::received` by mistake, instead of `OrderStatus::sent`, builds without any warning. Both names exist, so the compiler has nothing to report. Only a test catches such a bug.

## 5. A state isn't text: turning it into a string

The program should print the order's state. The simplest idea, printing the variable with `std::cout`, doesn't work:

<!-- broken: order_print at=11:15 error=^invalid operands to binary expression -->
```cpp
#include <iostream>

enum class OrderStatus {
    received,
    preparing,
    sent
};

int main() {
    OrderStatus status{OrderStatus::preparing};
    std::cout << status << "\n";
}
```

This program won't build. You don't have to build it: like the program in section 1, it's checked automatically, and you know its result from the description. The compiler reports an error on line 11, at `<<`. Its message starts with `invalid operands to binary expression`: there's no `<<` operation that prints a value of the type `OrderStatus`. Below this message the compiler may print a long list of `note:` lines about other types that can be printed. Reading the first line of the error is enough.

This isn't an oversight. **A state is a value of a type, and text is its representation.** What the text looks like is the program's decision: it could be `sent`, `Wysłane` or `SENT`. That's why you write the conversion from a state to text explicitly, in a function of its own:

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

| State | Text returned by `status_text` |
|---|---|
| `OrderStatus::received` | `"received"` |
| `OrderStatus::preparing` | `"preparing"` |
| `OrderStatus::sent` | `"sent"` |

- Each state has its own condition and its own `return`, like the functions with several `return`s in lesson 5.4.
- **The last line, `return "unknown";`, is the fallback.** For the three defined states it doesn't run, because each of them ends the function earlier. It's still needed. A function that promises a result must return one on every path (lesson 5.4), and the compiler doesn't treat three separate conditions as a complete set. Without this line it reports that the function doesn't return a value on all paths.
- **What would happen if someone added a fourth state to the type** and didn't update this function? For the new state the function returns `unknown`. So the type doesn't protect you from every oversight. A test that checks the text of each state catches such an oversight.

Printing the state now looks like this: `std::cout << status_text(status) << "\n";`.

## 6. Text to state: a parsing function

Sometimes you need to go the other way: you get text, for example from a file or from a user, and want to know which state it is. **`enum class` doesn't turn text into a state by itself.** You write this conversion as a function too, and the function decides which strings it accepts as state names:

<!-- fragment -->
```cpp
bool parse_status(const std::string& text, OrderStatus& result) {
    if (text == "received") {
        result = OrderStatus::received;
        return true;
    }

    if (text == "preparing") {
        result = OrderStatus::preparing;
        return true;
    }

    if (text == "sent") {
        result = OrderStatus::sent;
        return true;
    }

    return false;
}
```

**The contract of `parse_status`:**

| Text | Function's result | `result` after the call |
|---|---|---|
| `"received"` | `true` | `OrderStatus::received` |
| `"preparing"` | `true` | `OrderStatus::preparing` |
| `"sent"` | `true` | `OrderStatus::sent` |
| any other, for example `"preparring"`, `""` or `"Sent"` | `false` | **unchanged** |

- This is **parsing a state from text**. You know the interface from lesson 10.4: the `bool` says whether it worked, and the result goes into the result parameter `OrderStatus& result`.
- **An unknown state name doesn't change the result.** The function assigns `result` only when it recognises the name. Every refusal is `return false;` without an assignment, so the caller gets its state back unchanged. It's the same "all or nothing" rule as in lessons 9.2 and 10.4.
- **Upper and lower case matter.** `"Sent"` is a different text from `"sent"`, so the function refuses it. That's what the contract says.
- The text can come from anywhere in the program. In this lesson you write it directly in the code, to check the conversion itself.

## 7. A test program for the order state

You check the three functions of sections 4–6 with a test program, as in Module 13. You know `check_bool` and `check_text` from lessons 13.2 and 13.3. Only `check_status`, which compares two states, is new:

<!-- fragment -->
```cpp
void check_status(const std::string& name, OrderStatus expected, OrderStatus actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << status_text(expected) << ", actual " << status_text(actual) << "\n";
        ++failed;
    }
}
```

It compares the states with `==`. To print the `FAIL` line, though, it needs text, so it uses `status_text`. It's the same rule as in section 5: a state is a value, and to print it you turn it into text.

**The cases for `parse_status`**, with the expected results from the contract in section 6:

| Case | Text | `result` before the call | Expected result | `result` after the call | Why this case |
|---|---|---|---|---|---|
| A | `"received"` | `sent` | `true` | `received` | a known name |
| B | `"preparing"` | `received` | `true` | `preparing` | a known name |
| C | `"sent"` | `received` | `true` | `sent` | a known name |
| D | `"preparring"` | `preparing` | `false` | `preparing`, unchanged | a typo in the name |
| E | `""` | `received` | `false` | `received`, unchanged | empty text |

**Why does `result` start from a state other than the expected one?** In case A the expected result is `received`, so `result` starts from `sent`. If it started from `received`, the test would also pass for a faulty function that never assigns the result. In cases D and E it's the other way round: you check that the state from before the call stays.

Each case has its own result variable, just as each case in lesson 13.3 had its own stream and record. You check the functions `was_sent` and `status_text` for each of the three states.

**This is the second required run.** Replace the contents of `main.cpp` with the full test program below. You can copy the checking functions from lessons 13.2 and 13.3, and the state functions from sections 4–6. **Predict** how many checks there will be before you run the program.

<details>
<summary>The full test program</summary>

<!-- example: order_status_tests -->
```cpp
#include <iostream>
#include <string>

enum class OrderStatus {
    received,
    preparing,
    sent
};

bool was_sent(OrderStatus status) {
    return status == OrderStatus::sent;
}

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

bool parse_status(const std::string& text, OrderStatus& result) {
    if (text == "received") {
        result = OrderStatus::received;
        return true;
    }

    if (text == "preparing") {
        result = OrderStatus::preparing;
        return true;
    }

    if (text == "sent") {
        result = OrderStatus::sent;
        return true;
    }

    return false;
}

std::string bool_text(bool value) {
    if (value) {
        return "true";
    }

    return "false";
}

void check_bool(const std::string& name, bool expected, bool actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << bool_text(expected) << ", actual " << bool_text(actual) << "\n";
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

void check_status(const std::string& name, OrderStatus expected, OrderStatus actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << status_text(expected) << ", actual " << status_text(actual) << "\n";
        ++failed;
    }
}

int main() {
    int checks{0};
    int failed{0};

    check_bool("was_sent(received)", false, was_sent(OrderStatus::received), checks, failed);
    check_bool("was_sent(preparing)", false, was_sent(OrderStatus::preparing), checks, failed);
    check_bool("was_sent(sent)", true, was_sent(OrderStatus::sent), checks, failed);

    check_text("status_text(received)", "received", status_text(OrderStatus::received), checks, failed);
    check_text("status_text(preparing)", "preparing", status_text(OrderStatus::preparing), checks, failed);
    check_text("status_text(sent)", "sent", status_text(OrderStatus::sent), checks, failed);

    OrderStatus result_a{OrderStatus::sent};
    const bool accepted_a{parse_status("received", result_a)};
    check_bool("A accepted", true, accepted_a, checks, failed);
    check_status("A result", OrderStatus::received, result_a, checks, failed);

    OrderStatus result_b{OrderStatus::received};
    const bool accepted_b{parse_status("preparing", result_b)};
    check_bool("B accepted", true, accepted_b, checks, failed);
    check_status("B result", OrderStatus::preparing, result_b, checks, failed);

    OrderStatus result_c{OrderStatus::received};
    const bool accepted_c{parse_status("sent", result_c)};
    check_bool("C accepted", true, accepted_c, checks, failed);
    check_status("C result", OrderStatus::sent, result_c, checks, failed);

    OrderStatus result_d{OrderStatus::preparing};
    const bool accepted_d{parse_status("preparring", result_d)};
    check_bool("D accepted", false, accepted_d, checks, failed);
    check_status("D result", OrderStatus::preparing, result_d, checks, failed);

    OrderStatus result_e{OrderStatus::received};
    const bool accepted_e{parse_status("", result_e)};
    check_bool("E accepted", false, accepted_e, checks, failed);
    check_status("E result", OrderStatus::received, result_e, checks, failed);

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

<!-- output: order_status_tests -->
```text
PASS was_sent(received)
PASS was_sent(preparing)
PASS was_sent(sent)
PASS status_text(received)
PASS status_text(preparing)
PASS status_text(sent)
PASS A accepted
PASS A result
PASS B accepted
PASS B result
PASS C accepted
PASS C result
PASS D accepted
PASS D result
PASS E accepted
PASS E result
Checks: 16, failed: 0
```

Under the output, CLion adds `Process finished with exit code 0`.

</details>

- **16 checks:** three each for `was_sent` and `status_text`, two for each of the five `parse_status` cases.
- **The expected results come from the contract**, not from a second call of the function under test. Even for `status_text`, the expected text is a ready string from the table in section 5.
- `PASS D accepted` means: the check of case D's result agrees. The expected result is `false`, and the function returned `false`.

## 8. Diagnostic: a typo in a state's name

Go back to the warehouse of section 1. The same program, with a state instead of text and with the same mistake, a doubled letter:

<!-- broken: order_packing_typo at=10:35 errors=1 error=^no member named 'preparring' in 'OrderStatus' -->
```cpp
#include <iostream>

enum class OrderStatus {
    received,
    preparing,
    sent
};

bool needs_packing(OrderStatus status) {
    return status == OrderStatus::preparring;
}

int main() {
    OrderStatus status{OrderStatus::preparing};

    if (needs_packing(status)) {
        std::cout << "Pack the order\n";
    } else {
        std::cout << "Nothing to pack\n";
    }
}
```

**This is the third required run.** Follow the steps in order:

1. **Predict** before you build anything: will this program build? If it will, what will it print? If it won't, on which line will the compiler report an error?
2. Type the program into `main.cpp` and build it.
3. Find the first error: the file, the line and the name it's about.
4. Compare with section 1: there the same mistake built without a word.
5. Fix the name and build the program again.
6. Run the fixed version and check what it prints.

<details>
<summary>What happens and how to fix it: open after steps 1–6</summary>

**Stage:** compilation. The program doesn't build, so there's nothing to run. The compiler reports one error on line 10, at the name `preparring`. On the systems where we check the course, the message starts with `no member named 'preparring' in 'OrderStatus'`: the type `OrderStatus` has no value with this name. Clang often adds a suggestion like `did you mean 'preparing'?`. The exact wording may depend on the compiler's version, but it always points to the same line and the same name.

**The difference from section 1:**
- `"preparingg"` is a string. Every string is a valid value of `std::string`, so the compiler has nothing to report. The bug shows up only when the program runs, or in a test.
- `OrderStatus::preparring` is the name of a value, and the type `OrderStatus` has only three names. An unknown name doesn't quietly create a fourth state: the program isn't created at all.

**The fix:** `OrderStatus::preparing` on line 10. The fixed program:

<!-- example: order_packing -->
```cpp
#include <iostream>

enum class OrderStatus {
    received,
    preparing,
    sent
};

bool needs_packing(OrderStatus status) {
    return status == OrderStatus::preparing;
}

int main() {
    OrderStatus status{OrderStatus::preparing};

    if (needs_packing(status)) {
        std::cout << "Pack the order\n";
    } else {
        std::cout << "Nothing to pack\n";
    }
}
```

<!-- output: order_packing -->
```text
Pack the order
```

**What the compiler won't catch:** if line 10 said `OrderStatus::sent`, the program would build without warnings and print `Nothing to pack`. That's a valid name, just the wrong one. A test that checks `needs_packing` for an order being prepared catches such a bug.

</details>

## 9. Mission: the status of a fault report

The technical department keeps fault reports. A report is open, being investigated, or closed. Store this state as an enumeration type, and write the functions and a test program for it.

**The type:**

<!-- fragment -->
```cpp
enum class ReportStatus {
    opened,
    investigating,
    closed
};
```

**The contract of the functions:**

- `bool needs_work(ReportStatus status)`: `true` when the report still needs work, that is, isn't closed. For `closed` it returns `false`.
- `std::string report_status_text(ReportStatus status)`: the state's text, as in the table below.
- `bool parse_report_status(const std::string& text, ReportStatus& result)`: parses a state from text by the same table. For an unknown text it returns `false` and doesn't change `result`. Upper and lower case are told apart.

| Text | State |
|---|---|
| `"opened"` | `ReportStatus::opened` |
| `"investigating"` | `ReportStatus::investigating` |
| `"closed"` | `ReportStatus::closed` |
| `"unknown"` | refused |
| `"Closed"` | refused |

In `cpp-workspace`, create a folder `report_status`, copy `main.cpp` and `CMakeLists.txt` from the original `lesson_05_first_program` into it, and open it in CLion. Write everything in one file, `main.cpp`. Leave `CMakeLists.txt` unchanged.

**The order of work:**

1. **The table of cases first.** Before you write any code, prepare the table of cases for `parse_report_status`, as in section 7: the text, the state of `result` before the call, the expected result, the state after the call, and the reason. It must contain the three known names, `"unknown"`, `"Closed"` and **at least one wrong text of your own**, different from the ones in this lesson. For each refused case, write down which state must stay in `result` and why.
2. Define `ReportStatus` and write the three functions.
3. Write the test program: a checking function for `ReportStatus` states, checks of `needs_work` and `report_status_text` for each of the three states, and two checks, the result and the state, for each case in the table. At the end, the summary and the exit code as in section 7.
4. **This is the fourth required run:** run the test program with the correct functions. Every check should print `PASS`, and the exit code should be 0.
5. **A deliberate bug.** In `report_status_text`, change one letter in one of the returned texts, for example drop a letter from `"investigating"`. **This is the fifth required run:** build the program and run the tests. Write down whether the compiler reported anything, which test failed and what the exit code is. Then restore the correct text.

You don't have to run any other versions. If you like, also check what happens after a typo in the name of a value, for example `ReportStatus::closd`, and compare with step 5.

### Success criteria

- [ ] The program builds as C++20, and `CMakeLists.txt` is the one from lesson 0.5.
- [ ] `ReportStatus` is an `enum class` type with the three values of the contract; states aren't stored as strings anywhere.
- [ ] `needs_work` uses a comparison of states and returns results that agree with the contract.
- [ ] `report_status_text` returns the text from the table for each state and has an explicit fallback at the end.
- [ ] `parse_report_status` recognises the three known names, refuses every other text, and doesn't change `result` when it refuses.
- [ ] The table of cases contains `"unknown"`, `"Closed"` and at least one wrong text of your own, with a reason.
- [ ] In the cases of known names, `result` starts from a state other than the expected one; in the refused cases, the test checks that the state from before the call stays.
- [ ] The expected results in the tests come from the contract, not from calls of the functions under test.
- [ ] With the correct functions, every check passes and the exit code is 0.
- [ ] With the deliberate typo in a text, the program builds, the test of that state's text prints `FAIL`, and the exit code is 1.
- [ ] You can say which mistake the compiler catches, which one only tests catch, and why.

When the result matches, you can save the project in Git, as in lesson 1.5: `main.cpp` and `CMakeLists.txt`, without the build folder.

<details>
<summary>Hint 1: defining the state</summary>

The set of states is closed: a report can be in only one of the three states of the contract. Which keywords start the definition of such a type, where do you write the names of its values, and what separates them? Where in the file must this definition go so that the functions can use it? Compare with section 2.

</details>

<details>
<summary>Hint 2: the text representation</summary>

You have two conversions in opposite directions. One gets a state and always returns some text, the fallback included. The other gets text and can't always return a state, so it reports success with a `bool` and returns the state through a result parameter. In which of them are the texts from the table the result, and in which are they what you compare the input with?

</details>

<details>
<summary>Hint 3: an unknown text</summary>

When may the parsing function assign something to `result`? Only when it knows which state it is. So what stays in `result` if no condition matches and the function reaches its last line? In a test, how do you tell a function that changes nothing from one that happens to assign the same state that was already there?

</details>

## 10. When something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| An error with `no member named '…' in 'ReportStatus'` | The name of the value after `ReportStatus::` doesn't exist in that type, for example because of a typo. | Compare the name with the type's definition. Fix the name in the code, not in the definition. |
| An error with `use of undeclared identifier 'opened'` | The name of a value without the name of the type before it. | Write `ReportStatus::opened`. |
| An error with `invalid operands to binary expression` at `<<` | The program tries to print a state directly with `std::cout` (section 5). | Print the state's text: `report_status_text(status)`. |
| An error when initialising or assigning a string, for example with `cannot initialize a variable of type 'ReportStatus'` | Text goes into a state variable, for example `"opened"`. | A state is a value of the type: `ReportStatus::opened`. Turn text into a state with the parsing function. |
| A warning or an error that the function doesn't return a value on all paths | The text conversion function lacks the fallback at its end (section 5). | Add a final `return` with a fallback text. |
| A test of a known name passes although the parsing function assigns nothing | `result` starts from the state that is the expected result (section 7). | Start from a state other than the expected one. |
| A `FAIL` line shows the same text after `expected` and after `actual` | The checking function prints the states with `report_status_text`, and it returns the same text for two different states. | Look at the tests of `report_status_text`: one of them points to the wrong text. |

## 11. Explain

Answer in your own words, preferably in writing. Only then compare with the example answers.

1. How does a variable of the type `OrderStatus` differ from a variable of the type `std::string` that holds the word `"sent"`?
2. What does it mean that an enumeration type has a closed set of values?
3. What does `OrderStatus::sent` mean? What does each of its parts mean?
4. When does `status == OrderStatus::sent` give `true`, and when does `status != OrderStatus::sent` give `true`?
5. Why does the typo in `OrderStatus::preparring` stop the compilation, while the typo in `"preparingg"` doesn't?
6. Why can't the program be built with `std::cout << status`, and how do you print a state?
7. Why does `status_text` end with `return "unknown";`, if each of the three states has its own condition?
8. How do you check in a test that the parsing function refuses an unknown text?
9. Why mustn't the function change the result parameter after a failed parse?
10. If the compiler checks state names, why test functions that use `enum class` at all?

<details>
<summary>Example answers</summary>

1. A variable of the type `OrderStatus` can have only one of the three values defined in the type, and the compiler checks that. A variable of the type `std::string` can hold any string, even one with a typo, and the compiler has no way of checking it.
2. All the allowed values are listed in the type's definition. There are no others, and you can't add one elsewhere in the program just by using a new name.
3. The value `sent` of the type `OrderStatus`. `OrderStatus` is the name of the type, `::` means "a name from inside", as in `std::cout`, and `sent` is the name of the value.
4. `==` gives `true` when `status` has the value `OrderStatus::sent`. `!=` gives `true` when `status` has any other value, that is `received` or `preparing`.
5. `preparring` must be the name of a value of the type `OrderStatus`, and the type has only three names, so the compiler reports an error. `"preparingg"` is a string, and every string is a valid value of `std::string`: the comparison is legal and simply gives `false`.
6. There's no `<<` operation that prints a value of the type `OrderStatus`. A state is a value, not text. Only a conversion function gives you text, for example `std::cout << status_text(status)`.
7. A function that returns a result must return it on every path, and the compiler doesn't treat three separate conditions as a complete set. This line is also the fallback: if a new state were added to the type without updating the function, it would return `unknown`, and a test would show it.
8. Call it with an unknown text and check two things: that it returns `false`, and that `result` has the same state as before the call.
9. Because the caller would get a state that the text never meant. The contract says: with `false` the result is unchanged, so the caller can keep relying on its previous state. It's the "all or nothing" rule of lessons 9.2 and 10.4.
10. Because the compiler only checks that a name exists. It doesn't check whether the program uses the right name, whether a function returns the right text, or whether it recognises the right strings. Comparing with `OrderStatus::received` instead of `OrderStatus::sent`, or a typo in the text that `status_text` returns, builds without warnings. Only a test catches them.

</details>

## Summary

- A state stored as text accepts every string, even one with a typo. The compiler has nothing to report, and the bug shows up only when the program runs, or in a test.
- `enum class` defines an **enumeration type** with a closed set of named values. A state is a value of that type, not an agreed-upon string.
- You name one particular value with `Type::value`, for example `OrderStatus::sent`. The compiler checks the names of the type and of its values: an unknown name is a compile error.
- You compare states with `==` and `!=`, pass them to functions and return them from functions like other small values.
- **A state is a value of a type, and text is its representation.** You write the conversion from a state to text, and parsing a state from text, as two explicit functions.
- The parsing function returns `bool` and doesn't change the result parameter for an unknown text.
- The compiler catches unknown names. Mistakes with valid names, and bugs in the texts, are caught only by tests.

## What's next

The function `status_text` checks the states one by one with separate conditions, and you learn about a new state that wasn't added there only from a test. In [lesson 14.2: Handling every state with `switch`](lesson_02_handling_every_state_with_switch.en.md) you'll meet a construct that handles the different values of such a type in one place.

---

## Example solutions

Look here **after your own attempt**. Your case names, your own wrong texts and the order of checks may differ, as long as they meet the contract and the success criteria.

<details>
<summary>Section 9: the mission, the status of a fault report</summary>

**The table of cases for `parse_report_status`:**

| Case | Text | `result` before the call | Expected result | `result` after the call | Why this case |
|---|---|---|---|---|---|
| A | `"opened"` | `closed` | `true` | `opened` | a known name |
| B | `"investigating"` | `opened` | `true` | `investigating` | a known name |
| C | `"closed"` | `opened` | `true` | `closed` | a known name |
| D | `"unknown"` | `investigating` | `false` | `investigating`, unchanged | an unknown word |
| E | `"Closed"` | `opened` | `false` | `opened`, unchanged | a capital letter: the contract tells cases apart |
| F | `"open"` | `investigating` | `false` | `investigating`, unchanged | a case of your own: the start of a known name isn't a name yet |

Other good cases of your own: `""`, `" closed"` with a space at the start, `"closed "` with a space at the end, `"CLOSED"`. Each must be refused, because it isn't exactly one of the three names.

**`main.cpp`:**

<!-- example: report_status_tests -->
```cpp
#include <iostream>
#include <string>

enum class ReportStatus {
    opened,
    investigating,
    closed
};

bool needs_work(ReportStatus status) {
    return status != ReportStatus::closed;
}

std::string report_status_text(ReportStatus status) {
    if (status == ReportStatus::opened) {
        return "opened";
    }

    if (status == ReportStatus::investigating) {
        return "investigating";
    }

    if (status == ReportStatus::closed) {
        return "closed";
    }

    return "unknown";
}

bool parse_report_status(const std::string& text, ReportStatus& result) {
    if (text == "opened") {
        result = ReportStatus::opened;
        return true;
    }

    if (text == "investigating") {
        result = ReportStatus::investigating;
        return true;
    }

    if (text == "closed") {
        result = ReportStatus::closed;
        return true;
    }

    return false;
}

std::string bool_text(bool value) {
    if (value) {
        return "true";
    }

    return "false";
}

void check_bool(const std::string& name, bool expected, bool actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << bool_text(expected) << ", actual " << bool_text(actual) << "\n";
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

void check_report_status(const std::string& name, ReportStatus expected, ReportStatus actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << report_status_text(expected) << ", actual " << report_status_text(actual) << "\n";
        ++failed;
    }
}

int main() {
    int checks{0};
    int failed{0};

    check_bool("needs_work(opened)", true, needs_work(ReportStatus::opened), checks, failed);
    check_bool("needs_work(investigating)", true, needs_work(ReportStatus::investigating), checks, failed);
    check_bool("needs_work(closed)", false, needs_work(ReportStatus::closed), checks, failed);

    check_text("report_status_text(opened)", "opened", report_status_text(ReportStatus::opened), checks, failed);
    check_text("report_status_text(investigating)", "investigating", report_status_text(ReportStatus::investigating), checks, failed);
    check_text("report_status_text(closed)", "closed", report_status_text(ReportStatus::closed), checks, failed);

    ReportStatus result_a{ReportStatus::closed};
    const bool accepted_a{parse_report_status("opened", result_a)};
    check_bool("A accepted", true, accepted_a, checks, failed);
    check_report_status("A result", ReportStatus::opened, result_a, checks, failed);

    ReportStatus result_b{ReportStatus::opened};
    const bool accepted_b{parse_report_status("investigating", result_b)};
    check_bool("B accepted", true, accepted_b, checks, failed);
    check_report_status("B result", ReportStatus::investigating, result_b, checks, failed);

    ReportStatus result_c{ReportStatus::opened};
    const bool accepted_c{parse_report_status("closed", result_c)};
    check_bool("C accepted", true, accepted_c, checks, failed);
    check_report_status("C result", ReportStatus::closed, result_c, checks, failed);

    ReportStatus result_d{ReportStatus::investigating};
    const bool accepted_d{parse_report_status("unknown", result_d)};
    check_bool("D accepted", false, accepted_d, checks, failed);
    check_report_status("D result", ReportStatus::investigating, result_d, checks, failed);

    ReportStatus result_e{ReportStatus::opened};
    const bool accepted_e{parse_report_status("Closed", result_e)};
    check_bool("E accepted", false, accepted_e, checks, failed);
    check_report_status("E result", ReportStatus::opened, result_e, checks, failed);

    ReportStatus result_f{ReportStatus::investigating};
    const bool accepted_f{parse_report_status("open", result_f)};
    check_bool("F accepted", false, accepted_f, checks, failed);
    check_report_status("F result", ReportStatus::investigating, result_f, checks, failed);

    std::cout << "Checks: " << checks << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

<!-- output: report_status_tests -->
```text
PASS needs_work(opened)
PASS needs_work(investigating)
PASS needs_work(closed)
PASS report_status_text(opened)
PASS report_status_text(investigating)
PASS report_status_text(closed)
PASS A accepted
PASS A result
PASS B accepted
PASS B result
PASS C accepted
PASS C result
PASS D accepted
PASS D result
PASS E accepted
PASS E result
PASS F accepted
PASS F result
Checks: 18, failed: 0
```

Exit code: 0.

- **`needs_work`:** one condition, `!=`, because a report needs work in every state except closed. `status == ReportStatus::opened || status == ReportStatus::investigating` is correct too.
- **`report_status_text`:** the same structure as `status_text` in section 5, with the fallback at the end.
- **`parse_report_status`:** assigns `result` only after recognising a name. `"Closed"` and `"open"` aren't exactly any of the three names, so the function reaches `return false;` and changes nothing.
- **The checking function:** compares the states with `==`, and turns them into text for the `FAIL` line. Yours may have another name, for example `check_status`.

**The deliberate bug:** in `report_status_text` the text `"investigatng"`, without the `i` before the `n`. Only this one line changes, and the test program stays the same:

<!-- example: report_status_tests_typo exit=1 -->
```cpp
#include <iostream>
#include <string>

enum class ReportStatus {
    opened,
    investigating,
    closed
};

bool needs_work(ReportStatus status) {
    return status != ReportStatus::closed;
}

std::string report_status_text(ReportStatus status) {
    if (status == ReportStatus::opened) {
        return "opened";
    }

    if (status == ReportStatus::investigating) {
        return "investigatng";
    }

    if (status == ReportStatus::closed) {
        return "closed";
    }

    return "unknown";
}

bool parse_report_status(const std::string& text, ReportStatus& result) {
    if (text == "opened") {
        result = ReportStatus::opened;
        return true;
    }

    if (text == "investigating") {
        result = ReportStatus::investigating;
        return true;
    }

    if (text == "closed") {
        result = ReportStatus::closed;
        return true;
    }

    return false;
}

std::string bool_text(bool value) {
    if (value) {
        return "true";
    }

    return "false";
}

void check_bool(const std::string& name, bool expected, bool actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << bool_text(expected) << ", actual " << bool_text(actual) << "\n";
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

void check_report_status(const std::string& name, ReportStatus expected, ReportStatus actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << report_status_text(expected) << ", actual " << report_status_text(actual) << "\n";
        ++failed;
    }
}

int main() {
    int checks{0};
    int failed{0};

    check_bool("needs_work(opened)", true, needs_work(ReportStatus::opened), checks, failed);
    check_bool("needs_work(investigating)", true, needs_work(ReportStatus::investigating), checks, failed);
    check_bool("needs_work(closed)", false, needs_work(ReportStatus::closed), checks, failed);

    check_text("report_status_text(opened)", "opened", report_status_text(ReportStatus::opened), checks, failed);
    check_text("report_status_text(investigating)", "investigating", report_status_text(ReportStatus::investigating), checks, failed);
    check_text("report_status_text(closed)", "closed", report_status_text(ReportStatus::closed), checks, failed);

    ReportStatus result_a{ReportStatus::closed};
    const bool accepted_a{parse_report_status("opened", result_a)};
    check_bool("A accepted", true, accepted_a, checks, failed);
    check_report_status("A result", ReportStatus::opened, result_a, checks, failed);

    ReportStatus result_b{ReportStatus::opened};
    const bool accepted_b{parse_report_status("investigating", result_b)};
    check_bool("B accepted", true, accepted_b, checks, failed);
    check_report_status("B result", ReportStatus::investigating, result_b, checks, failed);

    ReportStatus result_c{ReportStatus::opened};
    const bool accepted_c{parse_report_status("closed", result_c)};
    check_bool("C accepted", true, accepted_c, checks, failed);
    check_report_status("C result", ReportStatus::closed, result_c, checks, failed);

    ReportStatus result_d{ReportStatus::investigating};
    const bool accepted_d{parse_report_status("unknown", result_d)};
    check_bool("D accepted", false, accepted_d, checks, failed);
    check_report_status("D result", ReportStatus::investigating, result_d, checks, failed);

    ReportStatus result_e{ReportStatus::opened};
    const bool accepted_e{parse_report_status("Closed", result_e)};
    check_bool("E accepted", false, accepted_e, checks, failed);
    check_report_status("E result", ReportStatus::opened, result_e, checks, failed);

    ReportStatus result_f{ReportStatus::investigating};
    const bool accepted_f{parse_report_status("open", result_f)};
    check_bool("F accepted", false, accepted_f, checks, failed);
    check_report_status("F result", ReportStatus::investigating, result_f, checks, failed);

    std::cout << "Checks: " << checks << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

<!-- output: report_status_tests_typo -->
```text
PASS needs_work(opened)
PASS needs_work(investigating)
PASS needs_work(closed)
PASS report_status_text(opened)
FAIL report_status_text(investigating): expected "investigating", actual "investigatng"
PASS report_status_text(closed)
PASS A accepted
PASS A result
PASS B accepted
PASS B result
PASS C accepted
PASS C result
PASS D accepted
PASS D result
PASS E accepted
PASS E result
PASS F accepted
PASS F result
Checks: 18, failed: 1
```

Exit code: 1.

- **The compiler:** reports nothing. `"investigatng"` is a valid string, just like `"preparingg"` in section 1.
- **The tests:** only the check of the text of the state `investigating` fails. Parsing has its own strings, so cases A–F pass.
- **The conclusion:** an enumeration type protects the names of the states, but not the texts you make from them. The text of each state needs its own test.

**Self-assessment.** Compare your work with the success criteria in section 9. Check in particular:
- that no state is stored as a string in the program, except the texts in the two conversion functions;
- that your own wrong text has a written reason, and that the test then also checks the state of `result`;
- that in the cases of known names `result` starts from a state other than the expected one;
- that you can point to one mistake the compiler reports and one that only a test catches.

If the answer to one of these is "no", go back to the corresponding section of the lesson before moving on.

</details>

**Previous lesson:** [Lesson 13.5: Workshop reservations (the Module 13 test)](../module_13_testing_functions/lesson_05_workshop_reservations.en.md) · **Next lesson:** [Lesson 14.2: Handling every state with `switch`](lesson_02_handling_every_state_with_switch.en.md) · [Course overview](../../README.en.md)

# Lesson 5.4: Several ways to `return`

[Polski](lesson_04_several_returns.md) · **English** · [Course overview](../../README.en.md)

> **Module 5, lesson 4** · about 70–90 minutes
> **You need:** the `cpp-workspace` folder and the original `lesson_05_first_program` project, as before. You don't need the debugger in this lesson.
> **Pilot version.** The programs in this lesson are checked automatically on Windows, Ubuntu and macOS, including with the given input data. Typing input into CLion's **Run** window is described without a manual check on every system.

## Before you start

This lesson assumes that after lesson 5.3 you:

- write functions with a result type and one `return` at the end;
- know that running `return` ends the function's call and passes the result back;
- write `if` and `else if` chains and combine conditions with `&&` and `||` (lessons 3.3 and 3.4);
- use variables of type `std::string` (lesson 2.7).

## The situation

In lesson 5.3, every function worked out its result with the same formula every time. Often, though, the result **depends on the data**: for some values the function should return one thing, for others something completely different. In this lesson a function makes a decision and ends at the place that fits the data it received.

After this lesson you will:

- write functions with several `return` statements;
- predict which `return` will run for a given argument;
- explain why, after a `return` has run, later conditions aren't checked;
- use a guard clause to handle a special case;
- return text of type `std::string`;
- find condition-order bugs and choose the cases that reveal them;
- recognise a function in which one of the paths returns no result;
- design a classifying function with rules in a set order of precedence.

## 1. Prepare the project

In `cpp-workspace`, create a `lesson_5_4` folder and copy `main.cpp` and `CMakeLists.txt` into it from the original `lesson_05_first_program`. You type the programs from sections 2–7 into that folder's `main.cpp`.

## 2. The result depends on the data

A competition gives from 0 to 10 points. The function has to limit a score to that range: a value below 0 gives 0, a value above 10 gives 10, and a value from 0 to 10 stays as it is. One formula isn't enough, because the result depends on which value the function gets:

<!-- example: limit_points -->
```cpp
#include <iostream>

int limit_points(int points) {
    if (points < 0) {
        return 0;
    }

    if (points > 10) {
        return 10;
    }

    return points;
}

int main() {
    std::cout << "-3 -> " << limit_points(-3) << "\n";
    std::cout << "0 -> " << limit_points(0) << "\n";
    std::cout << "4 -> " << limit_points(4) << "\n";
    std::cout << "10 -> " << limit_points(10) << "\n";
    std::cout << "13 -> " << limit_points(13) << "\n";
}
```

The function has **three** `return` statements: two in `if` blocks and one at the end.

**Predict** the five lines before you run the program.

<details>
<summary>Standard output</summary>

<!-- output: limit_points -->
```text
-3 -> 0
0 -> 0
4 -> 4
10 -> 10
13 -> 10
```

</details>

This is deliberate **limiting** of the result to a range: a score that's too low becomes 0, and one that's too high becomes 10. It's not a way of handling all bad data. In section 5 you'll see a different model: the function recognises an unacceptable value and returns a message about it.

## 3. Which `return` runs?

Trace the calls `limit_points(-3)`, `limit_points(4)` and `limit_points(13)`. Copy the table and fill it in:

| Argument | `points < 0` | `points > 10` | Which `return` ran | Result |
|---|---|---|---|---|
| -3 | | | | |
| 4 | | | | |
| 13 | | | | |

<details>
<summary>The filled-in table and explanation</summary>

| Argument | `points < 0` | `points > 10` | Which `return` ran | Result |
|---|---|---|---|---|
| -3 | `true` | **not checked** | `return 0;` in the first `if` | 0 |
| 4 | `false` | `false` | the final `return points;` | 4 |
| 13 | `false` | `true` | `return 10;` in the second `if` | 10 |

- **For -3** the first condition is true, so `return 0;` runs. The function **ends at once**: the second condition isn't checked any more, and the place of the call gets 0.
- **For 4** both conditions are false, so the program reaches the final `return points;`.
- **For 13** the first condition is false and the second is true: `return 10;` runs.

</details>

**A function can have several `return` statements, but in one call only one of them runs: the first one the program reaches.** The function doesn't go through all the paths and then choose a result. It goes from the top, checks the conditions in turn, and ends at the first `return` that runs.

## 4. A guard clause

A function often has one **special case** that has to be handled differently from the rest. For example, a number of minutes can't be negative, and for a negative value the function should return 0. Such a case can be checked **at the start** and the function ended straight away:

<!-- fragment -->
```cpp
int seconds_from_minutes(int minutes) {
    if (minutes < 0) {
        return 0;
    }

    return minutes * 60;
}
```

This is a **guard clause**: an early check for a situation that needs a separate ending of the function. It's not a new C++ statement, just a way of arranging the `if` and `return` you know. After the special case is handled, the rest of the function deals only with ordinary data and doesn't have to sit in an extra `else`.

The same function can also look like this:

<!-- fragment -->
```cpp
int seconds_from_minutes(int minutes) {
    if (minutes < 0) {
        return 0;
    } else {
        return minutes * 60;
    }
}
```

Both versions are correct and return the same results. An `else` after `return` isn't a mistake. A guard clause is a tool for readability: it's especially useful when a longer part of the function is left after the special case has been handled.

## 5. A result of type `std::string`

A function can return text. This function describes the progress of a job with 10 stages:

<!-- example: progress_status -->
```cpp
#include <iostream>
#include <string>

std::string progress_status(int completed) {
    if (completed < 0 || completed > 10) {
        return "Invalid progress";
    }

    if (completed == 10) {
        return "Complete";
    }

    if (completed >= 5) {
        return "In progress";
    }

    return "Getting started";
}

int main() {
    const std::string status{progress_status(5)};
    std::cout << "5: " << status << "\n";

    std::cout << "-1: " << progress_status(-1) << "\n";
    std::cout << "0: " << progress_status(0) << "\n";
    std::cout << "4: " << progress_status(4) << "\n";
    std::cout << "9: " << progress_status(9) << "\n";
    std::cout << "10: " << progress_status(10) << "\n";
    std::cout << "11: " << progress_status(11) << "\n";
}
```

- The result type is `std::string`, which you know from lesson 2.7. The function needs the `<string>` header.
- The first `if` is a guard clause: an unacceptable number of stages gives `Invalid progress` straight away, and the later rules no longer apply to it.
- Every `return` that runs ends the call and passes back one text.
- The function **prints nothing**. The returned text can be stored in a variable, like `status`, or printed straight away with `std::cout` in `main`.

**Predict** the seven lines. For each one, point out which `return` ran.

<details>
<summary>Standard output</summary>

<!-- output: progress_status -->
```text
5: In progress
-1: Invalid progress
0: Getting started
4: Getting started
9: In progress
10: Complete
11: Invalid progress
```

</details>

**The result type applies to every `return`.** In this program someone left the result type as `int`, although the function returns text:

<!-- broken: wrong_result_type at=6:16 errors=2 error=^cannot initialize return object of type 'int' -->
```cpp
#include <iostream>
#include <string>

int progress_status(int completed) {
    if (completed == 10) {
        return "Complete";
    }

    return "Not complete";
}

int main() {
    std::cout << progress_status(10) << "\n";
}
```

**Predict** whether the program will build. Then try to build it.

<details>
<summary>What the compiler reports, and why</summary>

The program won't build. The compiler reports **two** errors, one for each `return`. The first is on line 6: `cannot initialize return object of type 'int' with an lvalue of type 'const char[9]'`. The function promises an `int` result but tries to return text. Every `return` must give a value that matches the function's result type. The fix is one change. You'll find it in [Example solutions](#example-solutions).

</details>

## 6. Find the bug: the order of conditions

The requirement is the same as in section 5: 10 stages is `Complete`, 5 to 9 is `In progress`, 0 to 4 is `Getting started`. In this version someone swapped the order of two rules:

<!-- example: progress_order_bug -->
```cpp
#include <iostream>
#include <string>

std::string progress_status(int completed) {
    if (completed < 0 || completed > 10) {
        return "Invalid progress";
    }

    if (completed >= 5) {
        return "In progress";
    }

    if (completed == 10) {
        return "Complete";
    }

    return "Getting started";
}

int main() {
    std::cout << "4: " << progress_status(4) << "\n";
    std::cout << "5: " << progress_status(5) << "\n";
    std::cout << "9: " << progress_status(9) << "\n";
    std::cout << "10: " << progress_status(10) << "\n";
}
```

1. Read the requirement and write down the correct result for 4, 5, 9 and 10.
2. **Predict** what **this** program will print.
3. Run it.
4. Find the first result that doesn't match the requirement.
5. Explain which `return` ran too early.
6. Fix the order of the conditions.
7. Check all four cases again.

The output before the fix, and the fixed program, are in [Example solutions](#example-solutions). Look there after your own attempt.

## 7. A path without `return`

This version of `limit_points` from section 2 is missing a part. **Analyse it on paper; don't run it:**

<!-- fragment -->
```cpp
int limit_points(int points) {
    if (points < 0) {
        return 0;
    }

    if (points > 10) {
        return 10;
    }
}
```

1. Point out every path a call of this function can take.
2. Find an argument for which the program doesn't reach any `return`.
3. Explain why this isn't a correct solution.
4. Suggest the missing `return`. What result should it give, according to the requirement?

<details>
<summary>Discussion</summary>

- There are three paths: an argument below 0 reaches `return 0;`, an argument above 10 reaches `return 10;`, and an argument from 0 to 10, for example 4, skips both `if`s and reaches the function's closing brace **without any `return`**.
- The function promises an `int` result but doesn't pass one back for such arguments. The compiler may report a warning, and the program may build anyway. But a call that reaches the end of the function without `return` has **undefined behaviour**: its result isn't determined and can't be relied on. The special rule from lesson 5.3 applies only to `main`. An ordinary function doesn't get the result 0 automatically.
- **The missing `return`:** `return points;` at the end, because values from 0 to 10 should stay as they are. The final `return` must return a result that matches the requirement. Just adding any `return` to stop the compiler warning isn't enough.

</details>

**For every possible path of execution, a function that returns a value must deliver a correct result.**

## 8. Mission: the queue status

A service point shows the status of its queue on a screen. The program gets the number of people waiting and the number of available desks, and a function works out the status. It's a simplified model for practice, not a real queueing system.

**Data:**

- the number of people waiting: a whole number from 0 to 12 inclusive;
- the number of available desks: a whole number from 0 to 4 inclusive.

**Rules**, in this order of precedence:

1. If either value is outside its range, the status is `Invalid queue data`. This rule takes precedence over all the others.
2. If nobody is waiting, the status is `Queue empty`, even when there are no desks.
3. If someone is waiting but there are no desks, the status is `No desks available`.
4. If the number of people waiting is **greater than** three times the number of desks, the status is `Busy queue`. That's "greater than", not "greater than or equal to".
5. In all other valid cases the status is `Manageable queue`.

Several rules can fit the same data. Then the rule higher on the list applies.

**Program requirements:**

- The program prints `Enter waiting people and available desks:` and reads two whole numbers: the number of people, then the number of desks.
- If not both numbers could be read, it prints only `Input could not be read` and doesn't work out a status. It doesn't ask again.
- Otherwise it prints one line: `Queue status: STATUS`, where `STATUS` is the text returned by the function.
- The status is worked out by **your own function**, which takes two `int` parameters and returns a `std::string`. It applies rules 1–5, including the range check, and has several `return` statements. It prints nothing and reads nothing. You choose the names of the function and its parameters, and the order of the parameters.
- `main` is responsible for the question, the read, checking that the read succeeded, calling the function and printing the report. It doesn't repeat the classification rules.
- Don't use variables declared outside functions.

In `cpp-workspace`, create a `queue_status` folder, copy `CMakeLists.txt` into it from the original `lesson_05_first_program`, create an empty `main.cpp` and write the program on your own.

For the data `4` and `1` the standard output must be as follows:

<!-- input: queue_status -->
```text
4
1
```

<!-- output: queue_status -->
```text
Enter waiting people and available desks:
Queue status: Busy queue
```

**Predict**, before you write the program: what status will it print for the data `0`, `0`, and what for `3`, `1`?

<!-- input: queue_status -->
```text
0
0
```

<details>
<summary>Standard output for 0 and 0</summary>

<!-- output: queue_status -->
```text
Enter waiting people and available desks:
Queue status: Queue empty
```

Two rules fit here: nobody is waiting (rule 2), and there are no desks (rule 3). Rule 2 wins, because it's higher.

</details>

<!-- input: queue_status -->
```text
3
1
```

<details>
<summary>Standard output for 3 and 1</summary>

<!-- output: queue_status -->
```text
Enter waiting people and available desks:
Queue status: Manageable queue
```

3 people is exactly three times one desk, not more, so rule 4 doesn't fit.

</details>

**This isn't `progress_status` with new text.** There, there was one value and thresholds along one axis. Here the function gets **two values with different roles**, and the rules can overlap: some data fits several rules at once. You have to decide on your own:

1. how to name the function and its parameters, and in what order to take them;
2. how to check both ranges, and how that rule affects the others;
3. in what order to check the remaining rules, so that the right one always wins;
4. what the function returns when no earlier rule fits;
5. how not to print a status after a failed read.

**Before you write the program**, prepare a table of test cases. Include cases where **two rules fit at once**, the three-times boundary (exactly three times, and one more), values just outside both ranges, also combined with zero people, text instead of the first and instead of the second number, and data that ends after one number. For each case, write down the expected standard output.

Analyse the cases where the data ends early on paper, as in lessons 4.5–5.3, instead of running them, and compare with the collapsed list of check cases. This lesson's program is checked separately for such data, by the course's automatic tests.

### Success criteria

- The program builds as C++20, and its standard output for the data `4`, `1`, for `0`, `0` and for `3`, `1` is exactly as shown above.
- For every case you can type, the standard output matches the list of check cases. You check the cases where the data ends early by reasoning.
- The status is worked out by your function, which returns a `std::string`, has two `int` parameters and several `return` statements. The function neither prints nor reads anything, and the rules aren't repeated in `main`.
- For any two whole numbers, the function reaches some `return`.
- After a failed read, `Queue status` doesn't appear.
- The program doesn't use variables declared outside functions.
- The table of cases was made before running the program.
- You can explain why your order of conditions matches the precedence of the rules.

When the result matches, you can save the project in Git, as in lesson 1.5.

<details>
<summary>Hint 1</summary>

Which data should be rejected before we even start working out the queue status?

</details>

<details>
<summary>Hint 2</summary>

Check the case of zero people and zero desks. Which rule should win if several conditions could fit?

</details>

<details>
<summary>Hint 3</summary>

After the special cases are handled, the function can return a result for all the remaining valid data. Every `return` that runs ends the function.

</details>

<details>
<summary>The full list of check cases: open it after preparing your own table</summary>

| People | Desks | Status | What it checks |
|---|---|---|---|
| 4 | 1 | `Busy queue` | one more than three times |
| 0 | 0 | `Queue empty` | rule 2 before rule 3 |
| 3 | 1 | `Manageable queue` | exactly three times |
| 0 | 4 | `Queue empty` | an empty queue with desks |
| 1 | 0 | `No desks available` | no desks |
| 12 | 0 | `No desks available` | no desks with a full queue |
| 1 | 1 | `Manageable queue` | an ordinary load |
| 2 | 2 | `Manageable queue` | an ordinary load |
| 12 | 4 | `Manageable queue` | the upper limits, exactly three times |
| 12 | 3 | `Busy queue` | three times exceeded |
| -1 | 2 | `Invalid queue data` | people just below the range |
| 13 | 2 | `Invalid queue data` | people just above the range |
| 2 | -1 | `Invalid queue data` | desks just below the range |
| 2 | 5 | `Invalid queue data` | desks just above the range |
| 0 | 5 | `Invalid queue data` | rule 1 before rule 2 |
| `abc` | `2` | `Input could not be read` | text instead of the first number |
| `2` | `abc` | `Input could not be read` | text instead of the second number |
| `2` | the end of the data | `Input could not be read` | the data ends after one number |
| no data | no data | `Input could not be read` | the data ends at once |

In the rows with `Input could not be read`, the program prints only the question and that message. In the others it prints the question and `Queue status: …`. The first three cases are checked above, with the mission's text.

<!-- input: queue_status -->
```text
0
4
```

<!-- output: queue_status -->
```text
Enter waiting people and available desks:
Queue status: Queue empty
```

<!-- input: queue_status -->
```text
1
0
```

<!-- output: queue_status -->
```text
Enter waiting people and available desks:
Queue status: No desks available
```

<!-- input: queue_status -->
```text
12
0
```

<!-- output: queue_status -->
```text
Enter waiting people and available desks:
Queue status: No desks available
```

<!-- input: queue_status -->
```text
1
1
```

<!-- output: queue_status -->
```text
Enter waiting people and available desks:
Queue status: Manageable queue
```

<!-- input: queue_status -->
```text
2
2
```

<!-- output: queue_status -->
```text
Enter waiting people and available desks:
Queue status: Manageable queue
```

<!-- input: queue_status -->
```text
12
4
```

<!-- output: queue_status -->
```text
Enter waiting people and available desks:
Queue status: Manageable queue
```

<!-- input: queue_status -->
```text
12
3
```

<!-- output: queue_status -->
```text
Enter waiting people and available desks:
Queue status: Busy queue
```

<!-- input: queue_status -->
```text
-1
2
```

<!-- output: queue_status -->
```text
Enter waiting people and available desks:
Queue status: Invalid queue data
```

<!-- input: queue_status -->
```text
13
2
```

<!-- output: queue_status -->
```text
Enter waiting people and available desks:
Queue status: Invalid queue data
```

<!-- input: queue_status -->
```text
2
-1
```

<!-- output: queue_status -->
```text
Enter waiting people and available desks:
Queue status: Invalid queue data
```

<!-- input: queue_status -->
```text
2
5
```

<!-- output: queue_status -->
```text
Enter waiting people and available desks:
Queue status: Invalid queue data
```

<!-- input: queue_status -->
```text
0
5
```

<!-- output: queue_status -->
```text
Enter waiting people and available desks:
Queue status: Invalid queue data
```

<!-- input: queue_status -->
```text
abc
2
```

<!-- output: queue_status -->
```text
Enter waiting people and available desks:
Input could not be read
```

<!-- input: queue_status -->
```text
2
abc
```

<!-- output: queue_status -->
```text
Enter waiting people and available desks:
Input could not be read
```

<!-- input: queue_status -->
```text
2
```

<!-- output: queue_status -->
```text
Enter waiting people and available desks:
Input could not be read
```

<!-- input: queue_status -->
```text
```

<!-- output: queue_status -->
```text
Enter waiting people and available desks:
Input could not be read
```

</details>

An example solution is in [Example solutions](#example-solutions).

## 9. When something goes differently

| What you see | What it means | What to do |
|---|---|---|
| The result for one value is "taken over" by another rule | A more general condition stands before a more specific one, and its `return` ends the function too early (section 6). | Arrange the conditions by precedence. Check a case that fits two rules. |
| Unacceptable data gets an ordinary status | The range check stands after another rule, or misses one of the values. | Check the range of both values at the start of the function, as a guard clause. |
| A warning that a function doesn't return a value on all paths | Some path through the function doesn't end in a `return` (section 7). | Find an argument that skips every `return`, and add a result that matches the requirement. |
| `cannot initialize return object of type …` | A `return` gives a value of a different type from the function's result type (section 5). | Every `return` must give a value that matches the result type. |
| A compile error with `std::string` | The `<string>` header is missing. | Add `#include <string>`. |
| For 3 people and 1 desk the status is `Busy queue` | The condition uses `>=` instead of `>`. | The rule says "greater than". Check exactly three times. |
| A status appears after a failed read | The function is called before the read is checked, or outside the branch for a successful read. | Call the function only when both reads succeeded. |
| The program does nothing and waits | It's waiting for another number, as in lesson 2.6. | Type a number and press **Enter**. Don't check a case where the data runs out this way: trace it on paper. |

## 10. Explain

Answer in your own words, preferably in writing. Only then compare with the example answers.

1. Can a function contain several `return` statements?
2. How many of them run during one call?
3. What happens after a `return` runs?
4. Why might a later condition never be checked?
5. What does a guard clause mean?
6. Is it a new C++ construct?
7. Is an `else` after `return` always wrong?
8. Why does the order of conditions affect the result?
9. What happens if there's a path that returns no value?
10. Does an ordinary function returning `int` automatically return zero?
11. Can a function return a `std::string`?
12. Does it then have to print the text?
13. Why doesn't a classifying function need to know how the data was read?
14. Why do we check for invalid data before the other rules?
15. Why do we need tests in which two conditions fit at once?
16. What result should the function return if all the special conditions are false?

<details>
<summary>Example answers</summary>

1. Yes; for example, `limit_points` has three.
2. Only one: the first one the program reaches in that call.
3. The function's call ends at once, and the result goes to the place of the call. The function's remaining statements don't run.
4. Because an earlier condition was true and its `return` ended the function before the program reached the later condition.
5. An early check for a special case, for example unacceptable data, with a `return` that ends the function straight away. The rest of the function then deals only with ordinary data.
6. No. It's a way of arranging the `if` and `return` you know.
7. No. Both versions can be correct. A guard clause is a choice for readability, not the only allowed style.
8. Because the first true condition ends the function with its `return`. If a more general condition stands higher, it catches data that should go to a more specific rule.
9. For the arguments that take that path, the call has undefined behaviour. The compiler may only warn, and the program may build, but its result can't be relied on.
10. No. That rule applies only to `main` (lesson 5.3).
11. Yes, for example `progress_status`. The `<string>` header is needed.
12. No. It returns the text, and the place of the call decides about printing it.
13. Because it gets ready values as arguments. Reading, and checking whether the read succeeded, belong to `main`.
14. Because invalid data could fit later rules, for example 0 people and 5 desks would fit "empty queue". The invalid-data rule takes precedence, so it has to be checked first.
15. Because only such tests show whether the right rule wins. When only one rule fits, a wrong order of conditions often still gives the correct result.
16. The result for the ordinary case that matches the requirements: `Manageable queue` in the mission, the unchanged `points` in `limit_points`.

</details>

## Summary

- A function can have **several `return` statements**. In one call only one runs: the first one the program reaches.
- **A `return` that runs ends the call at once.** The function's later conditions and statements are no longer checked or run.
- A **guard clause** is an early check for a special case, with a `return` at the start of the function. It's a way of arranging the `if` and `return` you know, not a new statement. The version with `else` is correct too.
- **The order of conditions matters.** Every condition can be correct on its own, and the function can still give a wrong result if a more general rule stands before a more specific one.
- Test cases where **two rules fit at once**, and boundaries, for example "exactly three times".
- A function can return a `std::string`. Every `return` must give a value that matches the result type.
- **Every path through a function that returns a value must end in a `return` with a correct result.** A missing `return` on some path is undefined behaviour, even if the compiler only warns.

## What's next

Your functions can now take data, make decisions and return results. In the next lesson you'll build a program from several cooperating functions, each with its own job: [Lesson 5.5: Several functions, one program](lesson_05_several_functions.en.md).

---

## Example solutions

Look here **after your own attempt**. Your names may differ, as long as the standard output is as required.

<details>
<summary>Section 5: the corrected result type</summary>

It's enough to change the result type from `int` to `std::string`. The `<string>` header is already in the program:

<!-- example: right_result_type -->
```cpp
#include <iostream>
#include <string>

std::string progress_status(int completed) {
    if (completed == 10) {
        return "Complete";
    }

    return "Not complete";
}

int main() {
    std::cout << progress_status(10) << "\n";
}
```

<!-- output: right_result_type -->
```text
Complete
```

</details>

<details>
<summary>Section 6: the output before the fix, and the fixed program</summary>

Before the fix:

<!-- output: progress_order_bug -->
```text
4: Getting started
5: In progress
9: In progress
10: In progress
```

- **For 4, 5 and 9** the results are correct. These cases don't reveal the bug.
- **For 10** the requirement says `Complete`, but the program prints `In progress`.
- **The cause:** the condition `completed >= 5` is also true for 10. It stands higher, so its `return "In progress";` ends the function before the program reaches `completed == 10`. That rule is never reached. Every condition on its own is correct, but the order isn't.
- **The fix:** check `completed == 10` before `completed >= 5`.

<!-- example: progress_order_fixed -->
```cpp
#include <iostream>
#include <string>

std::string progress_status(int completed) {
    if (completed < 0 || completed > 10) {
        return "Invalid progress";
    }

    if (completed == 10) {
        return "Complete";
    }

    if (completed >= 5) {
        return "In progress";
    }

    return "Getting started";
}

int main() {
    std::cout << "4: " << progress_status(4) << "\n";
    std::cout << "5: " << progress_status(5) << "\n";
    std::cout << "9: " << progress_status(9) << "\n";
    std::cout << "10: " << progress_status(10) << "\n";
}
```

<!-- output: progress_order_fixed -->
```text
4: Getting started
5: In progress
9: In progress
10: Complete
```

</details>

<details>
<summary>Section 8: the mission, the queue status</summary>

<!-- example: queue_status -->
```cpp
#include <iostream>
#include <string>

std::string queue_status(int waiting, int desks) {
    const bool waiting_valid{waiting >= 0 && waiting <= 12};
    const bool desks_valid{desks >= 0 && desks <= 4};

    if (!waiting_valid || !desks_valid) {
        return "Invalid queue data";
    }

    if (waiting == 0) {
        return "Queue empty";
    }

    if (desks == 0) {
        return "No desks available";
    }

    if (waiting > 3 * desks) {
        return "Busy queue";
    }

    return "Manageable queue";
}

int main() {
    int waiting_people{0};
    int available_desks{0};

    std::cout << "Enter waiting people and available desks:\n";
    std::cin >> waiting_people;
    std::cin >> available_desks;

    if (std::cin.fail()) {
        std::cout << "Input could not be read\n";
    } else {
        const std::string status{queue_status(waiting_people, available_desks)};
        std::cout << "Queue status: " << status << "\n";
    }
}
```

- **The order of conditions matches the precedence of the rules.** The guard clause for invalid data stands first, so 0 people and 5 desks give `Invalid queue data`, not `Queue empty`. The empty queue stands before the missing desks, so 0 and 0 give `Queue empty`.
- **`waiting > 3 * desks`** stands after the `desks == 0` check. For zero desks this rule wouldn't be reached anyway. The comparison is strict: 3 people at 1 desk is still `Manageable queue`.
- **The final `return`** handles all the remaining valid data. Every pair of whole numbers reaches some `return`.
- **The function** prints nothing and doesn't know where the numbers came from. **`main`** checks the read, and only after a successful read calls the function and prints the report.
- This order isn't the only correct way to write it. For example, two separate `if`s checking the ranges at the start of the function give the same results. But checking `desks == 0` before `waiting == 0` would give the wrong result for 0 and 0. What counts is whether the right rule wins for all data.

</details>

**Previous lesson:** [Lesson 5.3: A function returns a result (`return`)](lesson_03_returning_a_result.en.md) · **Next lesson:** [Lesson 5.5: Several functions, one program](lesson_05_several_functions.en.md) · [Course overview](../../README.en.md)

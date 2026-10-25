# Lesson 5.7: A program built from your own functions (the Module 5 test)

[Polski](lesson_07_a_program_of_functions.md) · **English** · [Course overview](../../README.en.md)

> **Module 5, lesson 7: the test** · about 100–120 minutes, and it can be split into two sessions
> **You need:** the `cpp-workspace` folder and the original `lesson_05_first_program` project.
> **Pilot version.** The reference solutions in this lesson are checked automatically on Windows, Ubuntu and macOS, with the given input data. Nothing grades your work automatically: you check it yourself, against the criteria.

## How this test works

This lesson introduces nothing new. You check whether you can design several cooperating functions on your own: decide **what has to be worked out**, **which function should do it**, and **who needs its result**. You also fix three short programs with bugs, recognise a compile error and a link error, and explain your decisions.

The lesson has two parts:

- **Part A: the test.** Requirements, examples, tasks, questions and criteria. No hints and no solution code. You know everything you need from Modules 1–5.
- **Part B: checking and discussion.** Hints, the full list of check cases, example solutions, explanations and a self-assessment. Go there after doing part A, or when you consciously decide to stop trying on your own.

Looking at part B, earlier lessons or your notes isn't a failure. What matters is **noting honestly what you did on your own and what you did with help**. A suggested split into two sessions:

- **first:** designing the functions and writing down their jobs, writing the program for task 1, checking the functions on their own, and the basic cases of the whole program;
- **second:** the boundary cases, tasks 2 and 3, comparing with the solution, the questions and the self-assessment.

**You may use:** CLion or the terminal, CMake and Ninja, as before; `CMakeLists.txt` copied from the original `lesson_05_first_program`; trace and case tables, and temporary test printouts. You don't need the debugger. You don't have to end the data from the keyboard: you analyse the cases where the data ends early on paper.

---

# Part A: the test

## Task 1: A bike rental

A small rental shop has a few bikes. An employee handles customers' requests one after another: each customer asks for a certain number of bikes, and the program decides whether the request can be accepted. After a request is accepted, there are fewer bikes available. After all the planned requests, the program prints a summary. It's a simplified model for practice: there are no returns, prices, rental times or customer details.

**Preparation:** in `cpp-workspace`, create a `bike_rental` folder, copy `CMakeLists.txt` into it from the original `lesson_05_first_program`, create an **empty** `main.cpp` and write the whole program on your own.

**The day's plan:**

- The program prints `Enter available bikes (0-6) and request count (0-5):` and reads two whole numbers: the number of available bikes and the number of requests to handle.
- From 0 to 6 bikes and from 0 to 5 requests are allowed, inclusive. Zero is a valid value for both.
- If the read fails, the program prints only `Input could not be read` and ends.
- If either value is outside its range, it prints only `Invalid rental plan` and ends.

**Requests:**

- For each request in turn, the program prints `Enter bikes for request N:`, where `N` is the request number starting from 1, and reads the number of bikes asked for.
- A customer can ask for 1, 2 or 3 bikes. A request is **accepted** if it's within that range and the shop has at least that many bikes available. Otherwise it's **rejected**. There are no partial rentals: for a request for 3 bikes with 2 available, the whole request is rejected.
- A correctly read number outside the range, for example 0 or 4, is a **rejected request**, not a failed read. The program then moves on to the next request.
- After each request, the program prints `Request N: Accepted` or `Request N: Rejected`.
- An accepted request reduces the number of available bikes by the number of bikes asked for. A rejected one doesn't change it at all. The number of available bikes is never negative.
- If reading the number of bikes for a request fails, for example after text or when the data ends early, the program prints `Input could not be read` and ends, with no summary and no further read attempts. The lines printed earlier stay.

**The summary** is printed only when all the planned requests have been read, in this order:

- `Accepted requests: N`
- `Rejected requests: N`
- `Bikes remaining: N`

The number of accepted requests isn't the number of bikes rented: one request can be for several bikes.

**Functions:**

- The program has **at least three sensible own functions besides `main`**. At least one returns a `bool`, and at least one an `int`.
- **At least one own function calls another own function** and uses its result.
- Data passes through parameters and returned values. The calculating and checking functions neither read nor print anything.
- You choose the names, the parameters and the split yourself. As a starting point, you can separate three responsibilities:
  1. whether the number of bikes asked for is acceptable;
  2. whether the request can be served with the bikes available now;
  3. how many bikes will actually be assigned: for an accepted request, as many as asked for; for a rejected one, zero.

  This is a suggestion, not a list of required functions. Another split is fine if every function has a real job, important rules aren't repeated, and the code stays readable.
- **`main`** prints the questions, reads the data, checks the read and the plan, handles exactly the planned number of requests, calls the functions, updates the number of available bikes and the counters, and prints the results.
- **The file layout** is your choice: helper functions' definitions before the functions that use them, with `main` at the end, or declarations at the start, then `main`, and the definitions below.
- Don't use variables declared outside functions.

**Example A:** two requests accepted, two rejected. The data:

<!-- input: bike_rental -->
```text
5
4
2
3
1
0
```

<!-- output: bike_rental -->
```text
Enter available bikes (0-6) and request count (0-5):
Enter bikes for request 1:
Request 1: Accepted
Enter bikes for request 2:
Request 2: Accepted
Enter bikes for request 3:
Request 3: Rejected
Enter bikes for request 4:
Request 4: Rejected
Accepted requests: 2
Rejected requests: 2
Bikes remaining: 0
```

The first two requests use all 5 bikes. The third can't be served, because there are no bikes left. The fourth asks for 0 bikes, so it's not acceptable.

**Example B:** no planned requests. The program doesn't ask about any request:

<!-- input: bike_rental -->
```text
0
0
```

<!-- output: bike_rental -->
```text
Enter available bikes (0-6) and request count (0-5):
Accepted requests: 0
Rejected requests: 0
Bikes remaining: 0
```

**Example C:** 2 bikes, 3 requests, asking for 3, 1 and 1 bikes. **Predict** the whole standard output before you write the program:

<!-- input: bike_rental -->
```text
2
3
3
1
1
```

<details>
<summary>Standard output for example C</summary>

<!-- output: bike_rental -->
```text
Enter available bikes (0-6) and request count (0-5):
Enter bikes for request 1:
Request 1: Rejected
Enter bikes for request 2:
Request 2: Accepted
Enter bikes for request 3:
Request 3: Accepted
Accepted requests: 2
Rejected requests: 1
Bikes remaining: 0
```

The request for 3 bikes with 2 available is rejected and doesn't change the state. The next two requests for 1 bike each are accepted, and at the end no bikes are left.

</details>

**Before you write the program**, write down on paper:

- which functions you'll create, what each receives, what it returns, and who calls it;
- a table of test cases: a plan with no requests, the plan's limits and the values just outside them, a request that uses exactly the remaining bikes, a request larger than availability followed by a smaller one, several acceptances and several rejections in a row, requests for 0, -1 and 4, text instead of the plan data and instead of the number in a request, and data that ends before the first request and after several requests. For each case, write down the expected standard output.

Analyse the cases where the data ends early on paper, instead of running them, and compare with the full list of check cases in part B.

**Check the functions on their own first**, with test printouts as in lesson 5.5:

1. Choose one function.
2. Work out what result it should return for specific arguments.
3. Write down the prediction.
4. Temporarily print the result of its call.
5. Compare.
6. Check a boundary case.
7. Repeat for the function that uses another own function.
8. Remove the test printouts before you check the final standard output.

Check at least: a valid request for 1 and for 3 bikes, an unacceptable request for 0 and for 4, enough and not enough available bikes, a situation where exactly as many bikes are available as are asked for, and the result of a function that uses another function.

When the result matches, you can save the project in Git, as in lesson 1.5. Before committing, check `git status`: only `main.cpp` and `CMakeLists.txt` go into the history.

## Task 2: Three bug reports

In `cpp-workspace`, create a `diagnosis_5` folder, and copy `main.cpp` and `CMakeLists.txt` into it from the original `lesson_05_first_program`. Type each of the programs below in turn into that folder's `main.cpp`.

**Report A: scope.** The function should work out how many bikes will be left at a station with 6 bikes after 2 are rented. The program doesn't build:

<!-- broken: bikes_scope at=4:12 errors=1 error=^use of undeclared identifier 'station_bikes' -->
```cpp
#include <iostream>

int bikes_after_rental(int rented_bikes) {
    return station_bikes - rented_bikes;
}

int main() {
    const int station_bikes{6};
    std::cout << "Bikes left: " << bikes_after_rental(2) << "\n";
}
```

1. Point out the name the compiler doesn't know at the place where it's used.
2. Explain why the function has no access to `main`'s variable.
3. Suggest a parameter, and fix the call so that it passes the right argument. Don't use a variable declared outside functions.
4. Build and run the fixed program. The required result is `Bikes left: 4`.

**Report B: printing and the result.** The requirement: the program prints **exactly one** line, `Wheels needed: 6`, the number of wheels needed for 3 bikes.

<!-- example: wheels_bug -->
```cpp
#include <iostream>

int wheels_needed(int bikes) {
    const int wheels{bikes * 2};
    std::cout << wheels << "\n";
    return wheels;
}

int main() {
    const int wheels{wheels_needed(3)};
    std::cout << "Wheels needed: " << wheels << "\n";
}
```

1. **Predict** the standard output.
2. Run the program and compare.
3. Point out the statements that actually print text.
4. Separate the calculation from the presentation of the result.
5. Check the fix.

**Report C: `return` in a loop.** The function should work out the total number of training steps: each round has 2 steps, so for 3 rounds the result is 6.

<!-- example: steps_bug -->
```cpp
#include <iostream>

int total_training_steps(int rounds) {
    int total{0};

    for (int round_number{0}; round_number < rounds; ++round_number) {
        total += 2;
        return total;
    }

    return total;
}

int main() {
    std::cout << "Rounds: 0, steps: " << total_training_steps(0) << "\n";
    std::cout << "Rounds: 1, steps: " << total_training_steps(1) << "\n";
    std::cout << "Rounds: 3, steps: " << total_training_steps(3) << "\n";
}
```

1. Write down the correct result for 0, 1 and 3 rounds.
2. **Predict** what **this** program will print.
3. Run it and find the case that reveals the bug.
4. Explain what `return` does inside the loop.
5. Fix the function and check all three cases again.

Write the results in a table:

| Report | The case that reveals the bug | The cause | The fix | The check |
|---|---|---|---|---|
| A | | | | |
| B | | | | |
| C | | | | |

You don't need to save the `diagnosis_5` project in Git.

## Task 3: Compiling or linking?

Neither program builds, but for different reasons. You can type them into the `main.cpp` of the `diagnosis_5` folder and build them.

**Case A:**

<!-- broken: bikes_undeclared at=4:36 errors=1 error=^use of undeclared identifier 'bikes_left' -->
```cpp
#include <iostream>

int main() {
    std::cout << "Bikes left: " << bikes_left(2) << "\n";
}

int bikes_left(int rented_bikes) {
    return 6 - rented_bikes;
}
```

**Case B:**

<!-- broken: bikes_no_definition stage=link error=undefined reference to .bikes_left\(int\)'|undefined symbol: int __cdecl bikes_left\(int\)|"bikes_left\(int\)", referenced from -->
```cpp
#include <iostream>

int bikes_left(int rented_bikes);

int main() {
    std::cout << "Bikes left: " << bikes_left(2) << "\n";
}
```

For each case:

1. Point out the declaration, the definition and the call, if they're there.
2. Point out the build stage that fails: compiling or linking.
3. Explain why it's that stage.
4. Suggest a fix.

You don't need to remember the linkers' exact messages. What matters is the stage and the cause.

## Task 4: Explain your design

Answer briefly, in writing, referring to your own program from task 1:

1. Why did you choose these functions? What job does each of them have?
2. Which function checks whether the number of bikes asked for is acceptable?
3. Which function decides about assigning bikes?
4. Which function calls another own function? What values does it pass, and what result does it get?
5. Why don't your functions need to know `main`'s local variables?
6. Why does the number of available bikes change exactly at the place in the program where you change it?
7. Can a function correctly return a `bool` without printing anything? Point out such a function in your program.
8. What would happen if two `int` arguments were swapped in a call, for example the bikes asked for and the bikes available? Would the compiler report it?
9. Why isn't a test with one request enough?
10. Why doesn't a correct result from a helper function guarantee that the whole program is correct?
11. Why does your program compile? Which functions does the compiler know at the places where they're called, and from where?
12. Why doesn't the program print the summary after a failed read?

## Success criteria

You pass the test when you meet **all** the criteria. You may use part B as you go, as long as you note it honestly in the self-assessment.

- `bike_rental/main.cpp` was written from an empty file, in correct C++20. The program builds with no errors.
- The program has at least three sensible own functions besides `main`, including at least one that returns a `bool` and at least one that returns an `int`. At least one own function calls another and uses its result.
- The calculating and checking functions neither read nor print anything. The request rules aren't repeated in `main`, and no function exists just to meet the number.
- The number of available bikes and the counters change in `main`, based on the functions' results: an accepted request reduces the availability, a rejected one doesn't change it.
- The standard output for examples A, B and C, and for the cases you can type, matches the requirements. The cases where the data ends early match your trace table.
- After a failed read or an invalid plan, no summary appears.
- The functions were checked on their own with test printouts, and the final program contains no such printouts.
- The table of cases was made before running the program.
- All three reports in task 2 were diagnosed and fixed, and the fixes were checked.
- In task 3, the stage and the cause of both errors were identified correctly.
- You can explain every line of your program and answer the questions in task 4.

The names of functions and variables, and the program's split, may differ from the reference solution, as long as they're readable and meet the requirements. A correct result is a necessary condition, but **not proof of understanding**. That's why tasks 2–4 are part of the test.

---

# Part B: checking and discussion

Come here after doing part A, or when you consciously decide to stop trying on your own.

## How to check your work

- **Standard output:** run the program for every case in your table that you can type, and compare the program's lines with the expected ones, character by character. Skip the typed data shown by the echo.
- **The end of the data:** check the cases where the data runs out with a trace table, and compare with the full list of check cases. Each of them is checked there automatically.
- **Functions:** does each one have a job that can be described in one sentence? Does any function only pass its arguments on? Does any rule stand in two places?
- **State:** do the number of available bikes and the counters change in one place, only based on a function's result?

## Hints

Open them one at a time, and only when you need them.

<details>
<summary>Task 1, hint 1</summary>

Which decisions about a single request shouldn't depend on how the program reads the data?

</details>

<details>
<summary>Task 1, hint 2</summary>

Separate checking the acceptable number of bikes from checking the current availability. Think about which function can use the other one's result.

</details>

<details>
<summary>Task 1, hint 3</summary>

Let the functions return the information needed to make a decision. `main` can use the result to update the available bikes and the request counters.

</details>

<details>
<summary>Task 2, report A</summary>

Where is `station_bikes` declared? How did a function get data from the place of the call in lesson 5.2?

</details>

<details>
<summary>Task 2, report B</summary>

How many `std::cout` statements run in the whole program? Compare with lesson 5.3.

</details>

<details>
<summary>Task 2, report C</summary>

Trace the call for 3 rounds. How many iterations of the loop run before the function ends? Compare with lesson 5.4.

</details>

## The full list of check cases: task 1

<details>
<summary>Open it after preparing your own table</summary>

The first three cases are checked in part A. In the "Result" column, `A` is an accepted and `R` a rejected request, in the order of the requests.

| Data | Result | What it checks |
|---|---|---|
| `5`, `4`, `2`, `3`, `1`, `0` | A A R R; summary 2, 2, 0 | example A |
| `0`, `0` | summary 0, 0, 0 | example B: no requests |
| `2`, `3`, `3`, `1`, `1` | R A A; summary 2, 1, 0 | example C: a request larger than availability |
| `6`, `0` | summary 0, 0, 6 | a plan with no requests, a full station |
| `0`, `1`, `1` | R; summary 0, 1, 0 | no bikes |
| `1`, `1`, `1` | A; summary 1, 0, 0 | one request for all available bikes |
| `2`, `1`, `3` | R; summary 0, 1, 2 | a request larger than availability, no partial rental |
| `6`, `5`, `1`, `1`, `1`, `1`, `1` | A A A A A; summary 5, 0, 1 | the largest plan, several acceptances in a row |
| `3`, `2`, `1`, `2` | A A; summary 2, 0, 0 | a request uses exactly the remaining bikes |
| `4`, `3`, `3`, `3`, `1` | A R A; summary 2, 1, 0 | a rejection, then a smaller, accepted request |
| `1`, `3`, `2`, `3`, `2` | R R R; summary 0, 3, 1 | several rejections in a row |
| `4`, `3`, `0`, `-1`, `4` | R R R; summary 0, 3, 4 | requests for 0, -1 and 4 bikes |
| `6`, `5`, `3`, `4`, `2`, `2`, `1` | A R A R A; summary 3, 2, 0 | a mixed sequence |
| `-1`, `2` | `Invalid rental plan` | bikes just below the range |
| `7`, `2` | `Invalid rental plan` | bikes just above the range |
| `3`, `-1` | `Invalid rental plan` | requests just below the range |
| `3`, `6` | `Invalid rental plan` | requests just above the range |
| `abc`, `2` | `Input could not be read` | text instead of the number of bikes |
| `3`, `abc` | `Input could not be read` | text instead of the request count |
| no data | `Input could not be read` | the data ends at once |
| `3`, `2`, then the end of the data | the question for request 1, then `Input could not be read` | the data ends before the first request |
| `3`, `2`, `1`, then the end of the data | A; the question for request 2, then `Input could not be read` | the data ends after one request |
| `3`, `3`, `1`, `abc` | A; the question for request 2, then `Input could not be read` | text instead of a number in a request |
| `5`, `4`, `1`, `1`, then the end of the data | A A; the question for request 3, then `Input could not be read` | the data ends after several requests |

<!-- input: bike_rental -->
```text
6
0
```

<!-- output: bike_rental -->
```text
Enter available bikes (0-6) and request count (0-5):
Accepted requests: 0
Rejected requests: 0
Bikes remaining: 6
```

<!-- input: bike_rental -->
```text
0
1
1
```

<!-- output: bike_rental -->
```text
Enter available bikes (0-6) and request count (0-5):
Enter bikes for request 1:
Request 1: Rejected
Accepted requests: 0
Rejected requests: 1
Bikes remaining: 0
```

<!-- input: bike_rental -->
```text
1
1
1
```

<!-- output: bike_rental -->
```text
Enter available bikes (0-6) and request count (0-5):
Enter bikes for request 1:
Request 1: Accepted
Accepted requests: 1
Rejected requests: 0
Bikes remaining: 0
```

<!-- input: bike_rental -->
```text
2
1
3
```

<!-- output: bike_rental -->
```text
Enter available bikes (0-6) and request count (0-5):
Enter bikes for request 1:
Request 1: Rejected
Accepted requests: 0
Rejected requests: 1
Bikes remaining: 2
```

<!-- input: bike_rental -->
```text
6
5
1
1
1
1
1
```

<!-- output: bike_rental -->
```text
Enter available bikes (0-6) and request count (0-5):
Enter bikes for request 1:
Request 1: Accepted
Enter bikes for request 2:
Request 2: Accepted
Enter bikes for request 3:
Request 3: Accepted
Enter bikes for request 4:
Request 4: Accepted
Enter bikes for request 5:
Request 5: Accepted
Accepted requests: 5
Rejected requests: 0
Bikes remaining: 1
```

<!-- input: bike_rental -->
```text
3
2
1
2
```

<!-- output: bike_rental -->
```text
Enter available bikes (0-6) and request count (0-5):
Enter bikes for request 1:
Request 1: Accepted
Enter bikes for request 2:
Request 2: Accepted
Accepted requests: 2
Rejected requests: 0
Bikes remaining: 0
```

<!-- input: bike_rental -->
```text
4
3
3
3
1
```

<!-- output: bike_rental -->
```text
Enter available bikes (0-6) and request count (0-5):
Enter bikes for request 1:
Request 1: Accepted
Enter bikes for request 2:
Request 2: Rejected
Enter bikes for request 3:
Request 3: Accepted
Accepted requests: 2
Rejected requests: 1
Bikes remaining: 0
```

<!-- input: bike_rental -->
```text
1
3
2
3
2
```

<!-- output: bike_rental -->
```text
Enter available bikes (0-6) and request count (0-5):
Enter bikes for request 1:
Request 1: Rejected
Enter bikes for request 2:
Request 2: Rejected
Enter bikes for request 3:
Request 3: Rejected
Accepted requests: 0
Rejected requests: 3
Bikes remaining: 1
```

<!-- input: bike_rental -->
```text
4
3
0
-1
4
```

<!-- output: bike_rental -->
```text
Enter available bikes (0-6) and request count (0-5):
Enter bikes for request 1:
Request 1: Rejected
Enter bikes for request 2:
Request 2: Rejected
Enter bikes for request 3:
Request 3: Rejected
Accepted requests: 0
Rejected requests: 3
Bikes remaining: 4
```

<!-- input: bike_rental -->
```text
6
5
3
4
2
2
1
```

<!-- output: bike_rental -->
```text
Enter available bikes (0-6) and request count (0-5):
Enter bikes for request 1:
Request 1: Accepted
Enter bikes for request 2:
Request 2: Rejected
Enter bikes for request 3:
Request 3: Accepted
Enter bikes for request 4:
Request 4: Rejected
Enter bikes for request 5:
Request 5: Accepted
Accepted requests: 3
Rejected requests: 2
Bikes remaining: 0
```

<!-- input: bike_rental -->
```text
-1
2
```

<!-- output: bike_rental -->
```text
Enter available bikes (0-6) and request count (0-5):
Invalid rental plan
```

<!-- input: bike_rental -->
```text
7
2
```

<!-- output: bike_rental -->
```text
Enter available bikes (0-6) and request count (0-5):
Invalid rental plan
```

<!-- input: bike_rental -->
```text
3
-1
```

<!-- output: bike_rental -->
```text
Enter available bikes (0-6) and request count (0-5):
Invalid rental plan
```

<!-- input: bike_rental -->
```text
3
6
```

<!-- output: bike_rental -->
```text
Enter available bikes (0-6) and request count (0-5):
Invalid rental plan
```

<!-- input: bike_rental -->
```text
abc
2
```

<!-- output: bike_rental -->
```text
Enter available bikes (0-6) and request count (0-5):
Input could not be read
```

<!-- input: bike_rental -->
```text
3
abc
```

<!-- output: bike_rental -->
```text
Enter available bikes (0-6) and request count (0-5):
Input could not be read
```

<!-- input: bike_rental -->
```text
```

<!-- output: bike_rental -->
```text
Enter available bikes (0-6) and request count (0-5):
Input could not be read
```

<!-- input: bike_rental -->
```text
3
2
```

<!-- output: bike_rental -->
```text
Enter available bikes (0-6) and request count (0-5):
Enter bikes for request 1:
Input could not be read
```

<!-- input: bike_rental -->
```text
3
2
1
```

<!-- output: bike_rental -->
```text
Enter available bikes (0-6) and request count (0-5):
Enter bikes for request 1:
Request 1: Accepted
Enter bikes for request 2:
Input could not be read
```

<!-- input: bike_rental -->
```text
3
3
1
abc
```

<!-- output: bike_rental -->
```text
Enter available bikes (0-6) and request count (0-5):
Enter bikes for request 1:
Request 1: Accepted
Enter bikes for request 2:
Input could not be read
```

<!-- input: bike_rental -->
```text
5
4
1
1
```

<!-- output: bike_rental -->
```text
Enter available bikes (0-6) and request count (0-5):
Enter bikes for request 1:
Request 1: Accepted
Enter bikes for request 2:
Request 2: Accepted
Enter bikes for request 3:
Input could not be read
```

</details>

## Example solutions

Look here **after your own attempt**.

<details>
<summary>Task 1: an example solution</summary>

<!-- example: bike_rental -->
```cpp
#include <iostream>

bool is_valid_plan(int available_bikes, int request_count) {
    const bool bikes_valid{available_bikes >= 0 && available_bikes <= 6};
    const bool count_valid{request_count >= 0 && request_count <= 5};
    return bikes_valid && count_valid;
}

bool is_valid_request(int requested_bikes) {
    return requested_bikes >= 1 && requested_bikes <= 3;
}

bool can_serve(int requested_bikes, int available_bikes) {
    return is_valid_request(requested_bikes) && requested_bikes <= available_bikes;
}

int bikes_to_assign(int requested_bikes, int available_bikes) {
    if (!can_serve(requested_bikes, available_bikes)) {
        return 0;
    }

    return requested_bikes;
}

int main() {
    int available_bikes{0};
    int request_count{0};

    std::cout << "Enter available bikes (0-6) and request count (0-5):\n";
    std::cin >> available_bikes;
    std::cin >> request_count;

    if (std::cin.fail()) {
        std::cout << "Input could not be read\n";
    } else if (!is_valid_plan(available_bikes, request_count)) {
        std::cout << "Invalid rental plan\n";
    } else {
        int accepted_requests{0};
        int rejected_requests{0};
        int request_number{1};
        bool input_failed{false};

        while (request_number <= request_count && !input_failed) {
            int requested_bikes{0};

            std::cout << "Enter bikes for request " << request_number << ":\n";
            std::cin >> requested_bikes;

            if (std::cin.fail()) {
                input_failed = true;
            } else {
                const int assigned_bikes{bikes_to_assign(requested_bikes, available_bikes)};

                if (assigned_bikes > 0) {
                    available_bikes = available_bikes - assigned_bikes;
                    ++accepted_requests;
                    std::cout << "Request " << request_number << ": Accepted\n";
                } else {
                    ++rejected_requests;
                    std::cout << "Request " << request_number << ": Rejected\n";
                }

                ++request_number;
            }
        }

        if (input_failed) {
            std::cout << "Input could not be read\n";
        } else {
            std::cout << "Accepted requests: " << accepted_requests << "\n";
            std::cout << "Rejected requests: " << rejected_requests << "\n";
            std::cout << "Bikes remaining: " << available_bikes << "\n";
        }
    }
}
```

| Function | Job | Parameters | Result | Called by |
|---|---|---|---|---|
| `is_valid_plan` | whether the day's plan is acceptable | bikes, request count | `bool` | `main` |
| `is_valid_request` | whether a request is within 1–3 | bikes asked for | `bool` | `can_serve` |
| `can_serve` | whether a request can be served with the current availability | bikes asked for and available | `bool` | `bikes_to_assign` |
| `bikes_to_assign` | how many bikes to assign: the number asked for, or 0 | bikes asked for and available | `int` | `main` |

- **Cooperation:** `bikes_to_assign` uses `can_serve`, and `can_serve` uses `is_valid_request`. Each rule appears in the code once: the request range only in `is_valid_request`, the comparison with availability only in `can_serve`.
- **Possible results:** `is_valid_request` gives `true` for 1, 2 and 3. `can_serve` gives `true` only when the request is acceptable and not larger than the availability, including when it's exactly equal. `bikes_to_assign` gives 0 for a rejected request, or the number of bikes asked for.
- **`main` changes the state.** The functions get copies of the values, as in lesson 5.2, and change nothing outside themselves. `main` subtracts the assigned bikes from `available_bikes` and increases one of the counters. That way the shop's state changes in one place, and the availability can't drop below zero: `bikes_to_assign` never returns more than the number of available bikes.
- **The loop** handles exactly `request_count` requests, and ends early only when a read fails. The `input_failed` flag works as in lesson 4.5. For zero requests the loop doesn't run at all.
- **A failed read:** the earlier results stay, and the program prints `Input could not be read` instead of the summary.
- **The file layout:** this solution writes the helper functions' definitions before the functions that use them, with `main` at the end. The other layout is correct too: the declarations of the four functions at the start, then `main`, and the definitions below, in any order, as in lesson 5.6.
- **Other splits** are correct too, for example without a separate `can_serve` function, or without a function for the plan and with the plan checked in `main`, as long as every function has a real job and the rules aren't repeated.

**The flow of calls** for example A: request 1 (2 bikes, with 5 available) and request 3 (1 bike, with 0 available):

| Step | Request 1 | Request 3 |
|---|---|---|
| available bikes before the request | 5 | 0 |
| `main` calls | `bikes_to_assign(2, 5)` | `bikes_to_assign(1, 0)` |
| `bikes_to_assign` calls | `can_serve(2, 5)` | `can_serve(1, 0)` |
| `can_serve` calls | `is_valid_request(2)`: `true` | `is_valid_request(1)`: `true` |
| `can_serve` compares | `2 <= 5`: `true`, returns `true` | `1 <= 0`: `false`, returns `false` |
| `bikes_to_assign` returns | 2 | 0 |
| `main`'s decision | accepted: `Request 1: Accepted` | rejected: `Request 3: Rejected` |
| available bikes after the request | 5 - 2 = 3 | unchanged: 0 |
| counters | accepted: 1 | rejected: 1 |

**Test printouts** for these functions, in a separate program, as in lesson 5.5:

<!-- example: rental_checks -->
```cpp
#include <iostream>

bool is_valid_plan(int available_bikes, int request_count) {
    const bool bikes_valid{available_bikes >= 0 && available_bikes <= 6};
    const bool count_valid{request_count >= 0 && request_count <= 5};
    return bikes_valid && count_valid;
}

bool is_valid_request(int requested_bikes) {
    return requested_bikes >= 1 && requested_bikes <= 3;
}

bool can_serve(int requested_bikes, int available_bikes) {
    return is_valid_request(requested_bikes) && requested_bikes <= available_bikes;
}

int bikes_to_assign(int requested_bikes, int available_bikes) {
    if (!can_serve(requested_bikes, available_bikes)) {
        return 0;
    }

    return requested_bikes;
}

int main() {
    std::cout << "Plan 0, 0 valid: " << is_valid_plan(0, 0) << "\n";
    std::cout << "Plan 7, 2 valid: " << is_valid_plan(7, 2) << "\n";

    std::cout << "Request 1 valid: " << is_valid_request(1) << "\n";
    std::cout << "Request 3 valid: " << is_valid_request(3) << "\n";
    std::cout << "Request 0 valid: " << is_valid_request(0) << "\n";
    std::cout << "Request 4 valid: " << is_valid_request(4) << "\n";

    std::cout << "Serve 2 of 2: " << can_serve(2, 2) << "\n";
    std::cout << "Serve 3 of 2: " << can_serve(3, 2) << "\n";
    std::cout << "Serve 1 of 0: " << can_serve(1, 0) << "\n";
    std::cout << "Serve 4 of 6: " << can_serve(4, 6) << "\n";

    std::cout << "Assign 3 of 5: " << bikes_to_assign(3, 5) << "\n";
    std::cout << "Assign 3 of 2: " << bikes_to_assign(3, 2) << "\n";
    std::cout << "Assign 0 of 5: " << bikes_to_assign(0, 5) << "\n";
    std::cout << "Assign 2 of 2: " << bikes_to_assign(2, 2) << "\n";
}
```

<!-- output: rental_checks -->
```text
Plan 0, 0 valid: 1
Plan 7, 2 valid: 0
Request 1 valid: 1
Request 3 valid: 1
Request 0 valid: 0
Request 4 valid: 0
Serve 2 of 2: 1
Serve 3 of 2: 0
Serve 1 of 0: 0
Serve 4 of 6: 0
Assign 3 of 5: 3
Assign 3 of 2: 0
Assign 0 of 5: 0
Assign 2 of 2: 2
```

</details>

<details>
<summary>Task 2, report A: the cause and the fix</summary>

The compiler reports `use of undeclared identifier 'station_bikes'` on line 4. The variable `station_bikes` is local to `main`, and the function sees only its parameters and its own variables (lesson 5.2). The fix: the function gets the number of bikes at the station as a parameter, and `main` passes it as an argument.

<!-- example: bikes_scope_fixed -->
```cpp
#include <iostream>

int bikes_after_rental(int station_bikes, int rented_bikes) {
    return station_bikes - rented_bikes;
}

int main() {
    const int station_bikes{6};
    std::cout << "Bikes left: " << bikes_after_rental(station_bikes, 2) << "\n";
}
```

<!-- output: bikes_scope_fixed -->
```text
Bikes left: 4
```

The parameter can have the same name as the variable in `main`. They're still two different variables: the parameter only receives the argument's value.

</details>

<details>
<summary>Task 2, report B: the output before the fix, and the fix</summary>

Before the fix:

<!-- output: wheels_bug -->
```text
6
Wheels needed: 6
```

Both the function and `main` print the number, and the requirement says one line. The function works out and returns the result, and `main` decides about the presentation. The fix removes the printing from the function:

<!-- example: wheels_fixed -->
```cpp
#include <iostream>

int wheels_needed(int bikes) {
    const int wheels{bikes * 2};
    return wheels;
}

int main() {
    const int wheels{wheels_needed(3)};
    std::cout << "Wheels needed: " << wheels << "\n";
}
```

<!-- output: wheels_fixed -->
```text
Wheels needed: 6
```

A function that prints and returns its result is valid C++. Here it doesn't meet the requirement, and it mixes the calculation with the presentation.

</details>

<details>
<summary>Task 2, report C: the output before the fix, and the fix</summary>

Before the fix:

<!-- output: steps_bug -->
```text
Rounds: 0, steps: 0
Rounds: 1, steps: 2
Rounds: 3, steps: 2
```

- **For 0 and 1 rounds** the result is correct, so these tests don't reveal the bug.
- **For 3 rounds** the result is 2 instead of 6.
- **The cause:** `return total;` stands **in the loop's body**. `return` doesn't end one iteration: it ends **the whole call of the function** (lesson 5.4). So the function ends after the first iteration, with the result 2. For 0 rounds the loop doesn't run, and for 1 round the first iteration is the only one, which is why both cases look right.
- **The fix:** remove the `return` from the loop. The final `return` returns the result, after all the iterations.

<!-- example: steps_fixed -->
```cpp
#include <iostream>

int total_training_steps(int rounds) {
    int total{0};

    for (int round_number{0}; round_number < rounds; ++round_number) {
        total += 2;
    }

    return total;
}

int main() {
    std::cout << "Rounds: 0, steps: " << total_training_steps(0) << "\n";
    std::cout << "Rounds: 1, steps: " << total_training_steps(1) << "\n";
    std::cout << "Rounds: 3, steps: " << total_training_steps(3) << "\n";
}
```

<!-- output: steps_fixed -->
```text
Rounds: 0, steps: 0
Rounds: 1, steps: 2
Rounds: 3, steps: 6
```

</details>

<details>
<summary>Task 3: answers</summary>

**Case A.** There's no separate declaration. The definition stands below `main`, and the call `bikes_left(2)` is in `main`. **Compiling fails:** the compiler reports `use of undeclared identifier 'bikes_left'` on line 4, because it reads the file from the top and doesn't know that name yet at the place of the call. The fix: add the declaration `int bikes_left(int rented_bikes);` before `main`, or move the definition above `main`.

**Case B.** The declaration stands before `main`, the call is in `main`, and there's no definition anywhere. **Compiling succeeds**, because the declaration is enough for the compiler. **Linking fails:** the linker can't find the called function's definition, so no program is created. The message depends on the system, but it contains the name `bikes_left(int)`, and `linker command failed` appears at the end. The fix: add a definition that matches the declaration:

<!-- example: bikes_declared -->
```cpp
#include <iostream>

int bikes_left(int rented_bikes);

int main() {
    std::cout << "Bikes left: " << bikes_left(2) << "\n";
}

int bikes_left(int rented_bikes) {
    return 6 - rented_bikes;
}
```

<!-- output: bikes_declared -->
```text
Bikes left: 4
```

</details>

## Example answers to task 4

<details>
<summary>Open it after writing your own answers</summary>

The answers are about the reference solution. Yours may differ, as long as they describe your program.

1. Each function answers one question: is the plan acceptable, is the request within the range, can it be served, how many bikes to assign. Each can be named in one sentence and checked on its own.
2. `is_valid_request`.
3. `bikes_to_assign`, which uses `can_serve`.
4. `bikes_to_assign` calls `can_serve` with the number of bikes asked for and available, and gets a `bool`. `can_serve` calls `is_valid_request` with the number of bikes asked for, and also gets a `bool`.
5. Because they get the values they need as arguments. `main`'s variables are local, and the functions have no access to them (lesson 5.2, report A).
6. Because `main` holds the shop's state, and the functions work on copies of the values. Changing it in one place, after the result of `bikes_to_assign`, guarantees that a rejected request changes nothing.
7. Yes, for example `is_valid_request` and `can_serve`. They return an answer, and `main` decides what to print.
8. The compiler wouldn't report it, because both arguments are `int`s (lesson 5.2). The program would make wrong decisions, for example `can_serve(5, 2)` instead of `can_serve(2, 5)`. A test with different values would reveal it.
9. Because one request doesn't check how the availability changes between requests, a rejection after the bikes are used up, or counters greater than 1.
10. Because `main` can use a correct result wrongly, for example forget to subtract the bikes or increase the wrong counter (lesson 5.5).
11. Each helper function's definition stands before the function that calls it, and all of them before `main`, so at every call the compiler already knows the function. In the layout with declarations, the declarations at the start of the file would give it that knowledge (lesson 5.6).
12. Because the plan wasn't fully carried out: some requests weren't read, so the numbers in the summary wouldn't describe the planned day.

</details>

## Self-assessment

For each criterion, mark one answer:

| Criterion | On my own | With a hint | After looking at the solution | To review |
|---|---|---|---|---|
| Designing the functions and their jobs | | | | |
| A function that calls another function | | | | |
| Passing arguments and receiving results | | | | |
| Functions with no input or output | | | | |
| Updating the state in `main` | | | | |
| Handling requests in a loop, and the counters | | | | |
| A failed read and the end of the data | | | | |
| Test printouts of functions | | | | |
| A table of cases with boundaries | | | | |
| Report A (scope) | | | | |
| Report B (printing and the result) | | | | |
| Report C (`return` in a loop) | | | | |
| Task 3 (compiling and linking) | | | | |
| The explanations in task 4 | | | | |

If anything is marked in the "To review" column, go back to the matching lesson:

| Topic | Lesson |
|---|---|
| definition, call and `void` | 5.1 |
| parameters, arguments, passing by value and scope | 5.2 |
| `return`, the result type and `std::cout` | 5.3 |
| several ways to `return`, and guard clauses | 5.4 |
| functions working together, and test printouts | 5.5 |
| declaration, definition, compiling and linking | 5.6 |
| loops, counters and the end of the data | Module 4 |
| conditions, `&&` and `\|\|` | Module 3 |

Then try the task again, for example with a different number of bikes or a different range of requests.

---

## Module 5 summary

After seven lessons you can:

- define and call your own functions, including `void` functions;
- pass arguments to functions and understand passing by value;
- use local variables and know where a parameter exists;
- return results with `return` and tell calculating from printing;
- use results of type `int`, `double`, `bool` and `std::string`;
- write functions with several ways to `return`, and guard clauses;
- build functions that use other functions, and split a program into jobs;
- check functions with simple test printouts;
- write declarations and definitions, and tell compile errors from link errors.

These are the basics. Functions in C++ have many more possibilities, which you'll meet in later modules.

## What's next

In Module 6, "Collections of data: `std::vector`", your programs will start to store many values of the same kind and process them with one loop. Start with your first vector: [Lesson 6.1: Your first `std::vector` and the range-based `for` loop](../module_06_collections/lesson_01_the_first_vector.en.md).

**Previous lesson:** [Lesson 5.6: Declaration, definition and linking](lesson_06_declaration_and_definition.en.md) · **Next lesson:** [Lesson 6.1: Your first `std::vector` and the range-based `for` loop](../module_06_collections/lesson_01_the_first_vector.en.md) · [Course overview](../../README.en.md)

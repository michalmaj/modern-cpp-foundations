# Lesson 5.5: Several functions, one program

[Polski](lesson_05_several_functions.md) · **English** · [Course overview](../../README.en.md)

> **Module 5, lesson 5** · about 80–95 minutes
> **You need:** the `cpp-workspace` folder and the original `lesson_05_first_program` project, as before. You don't need the debugger in this lesson.
> **Pilot version.** The programs in this lesson are checked automatically on Windows, Ubuntu and macOS, including with the given input data. Typing input into CLion's **Run** window is described without a manual check on every system.

## Before you start

This lesson assumes that after lesson 5.4 you:

- write functions with parameters that return `bool`, `int`, `double` or `std::string`;
- know that a parameter receives the argument's value, and that a `return` that runs ends the call;
- use several `return` statements and guard clauses;
- keep reading and printing in `main`, and calculations in functions.

## The situation

So far every program has had one own function, sometimes called several times, and a `main` that used it. A bigger problem, though, is made of several smaller jobs: something has to be checked, something calculated, something chosen. In this lesson one program will consist of **several functions with different jobs**, and functions will use the results of **other functions**. The point isn't to have as many functions as possible, but to split the problem sensibly.

After this lesson you will:

- split a problem into several jobs and point out each function's job;
- write a function that calls another own function and uses its result;
- trace the order of calls and returns between functions;
- check individual functions with controlled calls and printouts;
- tell checking one function from checking the whole program;
- find a function that ignores a helper function's result;
- design a program from at least three cooperating functions.

## 1. Prepare the project

In `cpp-workspace`, create a `lesson_5_5` folder and copy `main.cpp` and `CMakeLists.txt` into it from the original `lesson_05_first_program`. You type the programs from sections 2–8 into that folder's `main.cpp`.

## 2. A program does several things

The measurement station from lesson 4.7 has to answer three questions: is the number of measurements acceptable (1 to 24), is the temperature within the range (-20 to 40), and what description fits the data. In this version everything is in `main`, for fixed data:

<!-- example: station_all_in_main -->
```cpp
#include <iostream>
#include <string>

int main() {
    const int count{2};
    const double temperature{-3.0};

    std::string status{""};

    if (count < 1 || count > 24) {
        status = "Invalid station data";
    } else if (temperature < -20.0 || temperature > 40.0) {
        status = "Invalid station data";
    } else if (temperature < 0.0) {
        status = "Below freezing";
    } else {
        status = "Measurement ready";
    }

    std::cout << "Status: " << status << "\n";
}
```

<!-- output: station_all_in_main -->
```text
Status: Below freezing
```

This is a correct program. But think about it:

1. Which part of the code is responsible for the number of measurements, which for the temperature, and which chooses the description?
2. Can each of these jobs be checked separately, for example just the temperature rule for -21 and -20?
3. Does choosing the description need to know the details of the ranges, or is an answer of "good" or "bad" enough?

<details>
<summary>Discussion</summary>

All three jobs are mixed up in one `if` chain. To check just the temperature rule, you have to change the data of the whole program and look at a description that also depends on other rules. Choosing the description doesn't need to know the numbers 1, 24, -20 and 40: it's enough for it to know whether the data is acceptable. This isn't a C++ error. It's a matter of readability, of splitting responsibilities, and of being able to check things separately.

</details>

## 3. Three functions, each with its own job

The same problem, split into three functions:

<!-- example: station_functions -->
```cpp
#include <iostream>
#include <string>

bool is_valid_measurement_count(int count) {
    return count >= 1 && count <= 24;
}

bool is_valid_temperature(double temperature) {
    return temperature >= -20.0 && temperature <= 40.0;
}

std::string measurement_status(int count, double temperature) {
    if (!is_valid_measurement_count(count)) {
        return "Invalid station data";
    }

    if (!is_valid_temperature(temperature)) {
        return "Invalid station data";
    }

    if (temperature < 0.0) {
        return "Below freezing";
    }

    return "Measurement ready";
}

int main() {
    std::cout << "2, -3.0: " << measurement_status(2, -3.0) << "\n";
    std::cout << "2, 12.5: " << measurement_status(2, 12.5) << "\n";
    std::cout << "0, 12.5: " << measurement_status(0, 12.5) << "\n";
    std::cout << "2, 41.0: " << measurement_status(2, 41.0) << "\n";
}
```

| Function | Job | Receives | Returns |
|---|---|---|---|
| `is_valid_measurement_count` | whether the number of measurements is acceptable | the number of measurements | `bool` |
| `is_valid_temperature` | whether the temperature is within the range | the temperature | `bool` |
| `measurement_status` | which description fits the data | the number of measurements and the temperature | `std::string` |
| `main` | calls the function and prints the results | | |

`measurement_status` **doesn't repeat** the range conditions. Instead it calls the two small functions and uses their answers. Each function has a separate job. This is one possible split, not the only correct one.

**Predict** the four lines and run the program.

<details>
<summary>Standard output</summary>

<!-- output: station_functions -->
```text
2, -3.0: Below freezing
2, 12.5: Measurement ready
0, 12.5: Invalid station data
2, 41.0: Invalid station data
```

</details>

## 4. A function calls a function

In lessons 5.1–5.4 the pattern was always the same: `main` calls an own function, and the result goes back to `main`. Now the path is longer:

**`main` → `measurement_status` → a checking function → the result goes back to `measurement_status` → the result goes back to `main`**

- `main` doesn't have to call every function. The checking functions are called by `measurement_status`.
- An own function can call another own function the same way `main` does: by its name, with arguments in parentheses.
- A helper function's result goes to **the function that called it**, here `measurement_status`, and becomes a value in its condition.
- The helper function doesn't know who will finally print the report, and doesn't need to.
- Data passes between functions only through arguments and returned results, by value, as in lesson 5.2. The functions have no shared variables.

This is how the call `measurement_status(2, -3.0)` runs:

| Step | Where the program is | What happens |
|---|---|---|
| 1 | `main` | Calls `measurement_status(2, -3.0)`. |
| 2 | `measurement_status` | `count` = 2, `temperature` = -3.0. Checks the first condition. |
| 3 | `measurement_status` | Calls `is_valid_measurement_count(2)`. |
| 4 | `is_valid_measurement_count` | Works out `2 >= 1 && 2 <= 24` and returns `true`. |
| 5 | `measurement_status` | Comes back with the result `true`. `!true` is `false`, so the first `return` doesn't run. |
| 6 | `measurement_status` | Checks the second condition. |
| 7 | `measurement_status` | Calls `is_valid_temperature(-3.0)`. |
| 8 | `is_valid_temperature` | Works out `-3.0 >= -20.0 && -3.0 <= 40.0` and returns `true`. |
| 9 | `measurement_status` | Comes back with the result `true`. The second `return` doesn't run. |
| 10 | `measurement_status` | Checks `-3.0 < 0.0`: `true`. |
| 11 | `measurement_status` | `return "Below freezing";` ends the call. |
| 12 | `main` | Gets the text `Below freezing` and prints it. |

You don't need to memorise this table. Every step can be read from the code: a call, running the function, coming back with a result.

**Predict** for the call `measurement_status(0, 12.5)`: which checking functions will be called, and which won't?

<details>
<summary>Answer</summary>

Only `is_valid_measurement_count(0)`. It returns `false`, so `!false` is `true`, and the first `return "Invalid station data";` runs. The call of `measurement_status` ends at once, as in lesson 5.4. The program never reaches the second condition, so `is_valid_temperature` **isn't called**.

</details>

**The order of definitions.** In the program in section 3, the two small helper functions come first, then the function that uses them, and `main` at the end. That way, at every call, the compiler already knows the function being called, as in lesson 5.1. In lesson 5.6 you'll see another way of arranging functions in a file.

## 5. Check one function

Each small function can be checked on its own. All it takes is a few calls with chosen arguments, printing the results. This program **checks the functions**; it doesn't run the station. The functions are the same as in section 3:

<!-- example: station_checks -->
```cpp
#include <iostream>
#include <string>

bool is_valid_measurement_count(int count) {
    return count >= 1 && count <= 24;
}

bool is_valid_temperature(double temperature) {
    return temperature >= -20.0 && temperature <= 40.0;
}

std::string measurement_status(int count, double temperature) {
    if (!is_valid_measurement_count(count)) {
        return "Invalid station data";
    }

    if (!is_valid_temperature(temperature)) {
        return "Invalid station data";
    }

    if (temperature < 0.0) {
        return "Below freezing";
    }

    return "Measurement ready";
}

int main() {
    std::cout << "Count 0 valid: " << is_valid_measurement_count(0) << "\n";
    std::cout << "Count 1 valid: " << is_valid_measurement_count(1) << "\n";
    std::cout << "Count 24 valid: " << is_valid_measurement_count(24) << "\n";
    std::cout << "Count 25 valid: " << is_valid_measurement_count(25) << "\n";

    std::cout << "Temperature -21.0 valid: " << is_valid_temperature(-21.0) << "\n";
    std::cout << "Temperature -20.0 valid: " << is_valid_temperature(-20.0) << "\n";
    std::cout << "Temperature 40.0 valid: " << is_valid_temperature(40.0) << "\n";
    std::cout << "Temperature 41.0 valid: " << is_valid_temperature(41.0) << "\n";

    std::cout << "Status 2, -21.0: " << measurement_status(2, -21.0) << "\n";
}
```

`bool` values are printed as `1` (`true`) or `0` (`false`), as in lesson 3.2.

**Predict** every line before you run the program. Write your expectations in a table: argument, expected result.

<details>
<summary>Standard output</summary>

<!-- output: station_checks -->
```text
Count 0 valid: 0
Count 1 valid: 1
Count 24 valid: 1
Count 25 valid: 0
Temperature -21.0 valid: 0
Temperature -20.0 valid: 1
Temperature 40.0 valid: 1
Temperature 41.0 valid: 0
Status 2, -21.0: Invalid station data
```

</details>

This is what a **simple test printout** looks like:

1. Choose a function and arguments, preferably the boundaries and the values right next to them.
2. Write down the expected result.
3. Call the function and print the result.
4. Compare.

This isn't a new tool or a testing system. It's ordinary calls and `std::cout`. Test printouts help while you work, but they don't stay in the program that serves the user: that's why they're a separate program here.

## 6. Checking a function vs checking the program

The last two groups of lines in section 5 ask **different questions**:

- `is_valid_temperature(-21.0)` gives `0`: is **the temperature rule** correct?
- `measurement_status(2, -21.0)` gives `Invalid station data`: does the calling function **use the rule's result correctly**?

The first question checks one function. The second also checks how the functions work together. **Functions can be correct on their own, and the program can still use them wrongly.** A few test printouts don't give a full guarantee of correctness, but well-chosen boundaries catch many bugs early. Section 7 shows such a cooperation bug.

## 7. Find the bug: an ignored result

The requirement is the same as in section 3: the number of measurements from 1 to 24, the temperature from -20 to 40, and the description `Invalid station data` for data outside the range. Both helper functions are correct. The bug is somewhere else:

<!-- example: status_ignored_bug -->
```cpp
#include <iostream>
#include <string>

bool is_valid_measurement_count(int count) {
    return count >= 1 && count <= 24;
}

bool is_valid_temperature(double temperature) {
    return temperature >= -20.0 && temperature <= 40.0;
}

std::string measurement_status(int count, double temperature) {
    if (!is_valid_measurement_count(count)) {
        return "Invalid station data";
    }

    is_valid_temperature(temperature);

    if (temperature < 0.0) {
        return "Below freezing";
    }

    return "Measurement ready";
}

int main() {
    std::cout << "2, 12.5: " << measurement_status(2, 12.5) << "\n";
    std::cout << "0, 12.5: " << measurement_status(0, 12.5) << "\n";
    std::cout << "2, -21.0: " << measurement_status(2, -21.0) << "\n";
    std::cout << "2, 41.0: " << measurement_status(2, 41.0) << "\n";
}
```

The program builds with no errors and no warnings.

1. Read the requirement and write down the correct description for the four pairs of data.
2. **Predict** what **this** program will print.
3. Run it and find the mismatches.
4. Work out which function is responsible for the rule whose result doesn't match.
5. Find the place where its result was skipped.
6. Fix how the functions work together.
7. Check all four cases again.

The output before the fix, and the fix, are in [Example solutions](#example-solutions). Look there after your own attempt.

## 8. Does every statement need a function?

More functions don't automatically make a better program. This function only passes its arguments on and adds nothing:

<!-- fragment -->
```cpp
std::string station_status(int count, double temperature) {
    return measurement_status(count, temperature);
}
```

A program with it isn't more readable: when tracing, you have to go through one more call, and there's no new rule to check. Before you move something into a function, ask:

- Does it have a named job that can be described in one sentence?
- Is its result or action understandable without reading the whole program?
- Can it be checked on its own?
- Does it prevent an important rule from being repeated?
- Does the split make the program harder to trace?

There's no fixed number of lines after which a function is "too long". What counts is a clear job.

## 9. Mission: the cost of a parcel delivery

The program works out the cost of delivering a parcel, in whole zloty. It's a simplified pricing model for practice, not a real carrier's price list.

**Data:**

- the parcel's weight in whole kilograms: a whole number from 1 to 8 inclusive;
- the delivery zone: a whole number from 1 to 3 inclusive.

**The price** is a base price that depends on the weight, plus a surcharge that depends on the zone:

| Weight | Base price |
|---|---|
| 1–2 kg | 5 zł |
| 3–5 kg | 8 zł |
| 6–8 kg | 12 zł |

| Zone | Surcharge |
|---|---|
| 1 | 0 zł |
| 2 | 3 zł |
| 3 | 6 zł |

**Requirements:**

- The program prints `Enter parcel weight and delivery zone:` and reads two whole numbers: the weight, then the zone.
- If the read fails, it prints only `Input could not be read`.
- If both numbers were read but at least one is outside its range, it prints only `Invalid shipping data`.
- For valid data it prints `Shipping cost: N`, where `N` is the cost in whole zloty.
- The program doesn't ask again.
- The program has **at least three own functions besides `main`**. **At least one of them calls another own function.** The calculating and checking functions print nothing and read nothing.
- `main` prints the question, reads the data, checks the read, uses your function to check the data, gets the cost and prints the report. The rules for the base price and the surcharges aren't in `main`.
- The helper functions' definitions stand before the functions that use them, and all of them before `main`.
- Don't use variables declared outside functions.

In `cpp-workspace`, create a `shipping_cost` folder, copy `CMakeLists.txt` into it from the original `lesson_05_first_program`, create an empty `main.cpp` and write the program on your own.

For the data `2` and `3` (a 5 zł base price and a 6 zł surcharge):

<!-- input: shipping_cost -->
```text
2
3
```

<!-- output: shipping_cost -->
```text
Enter parcel weight and delivery zone:
Shipping cost: 11
```

For the data `6` and `2` (a 12 zł base price and a 3 zł surcharge):

<!-- input: shipping_cost -->
```text
6
2
```

<!-- output: shipping_cost -->
```text
Enter parcel weight and delivery zone:
Shipping cost: 15
```

**This isn't the measurement station with new names.** There, two functions checked ranges and a third chose a description. Here there are **two separate pricing rules**, and an `int` result that's built from the results of other functions. You have to decide on your own:

1. which jobs to move into functions, and what parameters and result types to give them;
2. which function knows the base-price rules, and which knows the surcharges;
3. which function uses another's result, so as not to repeat its rules;
4. in what order to write the definitions;
5. what stays in `main`.

**Check the functions on their own first.** Before you run the whole program with data, prepare a separate program with test printouts, as in section 5:

1. Choose a function.
2. Prepare arguments: the weight boundaries (2 and 3, 5 and 6), the zone boundaries, values outside the range.
3. Write down the expected result.
4. Print the actual result of the call.
5. Compare.
6. Only then check the program as a whole.

The program that serves the user contains no test printouts.

**Before you write the program**, also prepare a table of cases for the whole program: every weight and zone boundary from both sides, values outside the range for the weight and for the zone, text instead of the first and instead of the second number, and data that ends after one number. For each case, write down the expected standard output.

Analyse the cases where the data ends early on paper, as in lessons 4.5–5.4, instead of running them, and compare with the collapsed list of check cases. This lesson's program is checked separately for such data, by the course's automatic tests.

### Success criteria

- The program builds as C++20, and its standard output for the data `2`, `3` and `6`, `2` is exactly as shown above.
- For every case you can type, the standard output matches the list of check cases. You check the cases where the data ends early by reasoning.
- The program has at least three own functions besides `main`, and at least one of them calls another own function and uses its result.
- Each pricing rule appears in the code once, in a function. `main` contains no weight thresholds or surcharges.
- The calculating and checking functions neither print nor read anything.
- After a failed read or out-of-range data, `Shipping cost` doesn't appear.
- Before checking the whole program, the functions were checked with test printouts, and the final program has no such printouts.
- The program doesn't use variables declared outside functions.
- You can say, for every function: what its job is, what it receives, what it returns, and who calls it.

When the result matches, you can save the project in Git, as in lesson 1.5.

<details>
<summary>Hint 1</summary>

Point out three different jobs: checking the data, working out the base price, and working out the final cost.

</details>

<details>
<summary>Hint 2</summary>

Think about which function knows the base-price rules, and which one can use its result without repeating those rules.

</details>

<details>
<summary>Hint 3</summary>

If the function that works out the total cost needs the base price, it can call another own function and use the value it gets in a further calculation.

</details>

<details>
<summary>The full list of check cases: open it after preparing your own table</summary>

| Weight | Zone | Standard output after the question | What it checks |
|---|---|---|---|
| 2 | 3 | `Shipping cost: 11` | the example in the text |
| 6 | 2 | `Shipping cost: 15` | the example in the text |
| 1 | 1 | `Shipping cost: 5` | the lower limits |
| 2 | 2 | `Shipping cost: 8` | the end of the first weight band |
| 3 | 1 | `Shipping cost: 8` | the start of the second weight band |
| 3 | 3 | `Shipping cost: 14` | the second band, the highest surcharge |
| 4 | 2 | `Shipping cost: 11` | the middle of the second band |
| 5 | 2 | `Shipping cost: 11` | the end of the second band |
| 6 | 3 | `Shipping cost: 18` | the start of the third band |
| 8 | 1 | `Shipping cost: 12` | the upper weight limit |
| 8 | 3 | `Shipping cost: 18` | the upper limits |
| 0 | 1 | `Invalid shipping data` | the weight just below the range |
| -1 | 1 | `Invalid shipping data` | a negative weight |
| 9 | 1 | `Invalid shipping data` | the weight just above the range |
| 1 | 0 | `Invalid shipping data` | the zone just below the range |
| 1 | 4 | `Invalid shipping data` | the zone just above the range |
| `abc` | `1` | `Input could not be read` | text instead of the weight |
| `1` | `abc` | `Input could not be read` | text instead of the zone |
| `1` | the end of the data | `Input could not be read` | the data ends after one number |
| no data | no data | `Input could not be read` | the data ends at once |

The first two cases are checked above, with the mission's text.

<!-- input: shipping_cost -->
```text
1
1
```

<!-- output: shipping_cost -->
```text
Enter parcel weight and delivery zone:
Shipping cost: 5
```

<!-- input: shipping_cost -->
```text
2
2
```

<!-- output: shipping_cost -->
```text
Enter parcel weight and delivery zone:
Shipping cost: 8
```

<!-- input: shipping_cost -->
```text
3
1
```

<!-- output: shipping_cost -->
```text
Enter parcel weight and delivery zone:
Shipping cost: 8
```

<!-- input: shipping_cost -->
```text
3
3
```

<!-- output: shipping_cost -->
```text
Enter parcel weight and delivery zone:
Shipping cost: 14
```

<!-- input: shipping_cost -->
```text
4
2
```

<!-- output: shipping_cost -->
```text
Enter parcel weight and delivery zone:
Shipping cost: 11
```

<!-- input: shipping_cost -->
```text
5
2
```

<!-- output: shipping_cost -->
```text
Enter parcel weight and delivery zone:
Shipping cost: 11
```

<!-- input: shipping_cost -->
```text
6
3
```

<!-- output: shipping_cost -->
```text
Enter parcel weight and delivery zone:
Shipping cost: 18
```

<!-- input: shipping_cost -->
```text
8
1
```

<!-- output: shipping_cost -->
```text
Enter parcel weight and delivery zone:
Shipping cost: 12
```

<!-- input: shipping_cost -->
```text
8
3
```

<!-- output: shipping_cost -->
```text
Enter parcel weight and delivery zone:
Shipping cost: 18
```

<!-- input: shipping_cost -->
```text
0
1
```

<!-- output: shipping_cost -->
```text
Enter parcel weight and delivery zone:
Invalid shipping data
```

<!-- input: shipping_cost -->
```text
-1
1
```

<!-- output: shipping_cost -->
```text
Enter parcel weight and delivery zone:
Invalid shipping data
```

<!-- input: shipping_cost -->
```text
9
1
```

<!-- output: shipping_cost -->
```text
Enter parcel weight and delivery zone:
Invalid shipping data
```

<!-- input: shipping_cost -->
```text
1
0
```

<!-- output: shipping_cost -->
```text
Enter parcel weight and delivery zone:
Invalid shipping data
```

<!-- input: shipping_cost -->
```text
1
4
```

<!-- output: shipping_cost -->
```text
Enter parcel weight and delivery zone:
Invalid shipping data
```

<!-- input: shipping_cost -->
```text
abc
1
```

<!-- output: shipping_cost -->
```text
Enter parcel weight and delivery zone:
Input could not be read
```

<!-- input: shipping_cost -->
```text
1
abc
```

<!-- output: shipping_cost -->
```text
Enter parcel weight and delivery zone:
Input could not be read
```

<!-- input: shipping_cost -->
```text
1
```

<!-- output: shipping_cost -->
```text
Enter parcel weight and delivery zone:
Input could not be read
```

<!-- input: shipping_cost -->
```text
```

<!-- output: shipping_cost -->
```text
Enter parcel weight and delivery zone:
Input could not be read
```

</details>

An example solution is in [Example solutions](#example-solutions).

## 10. When something goes differently

| What you see | What it means | What to do |
|---|---|---|
| `use of undeclared identifier` with your function's name | The function is called in the file before its definition, also by another function. | Write helper functions before the functions that use them. |
| Out-of-range data gets an ordinary result | The checking function's result is skipped, or the function isn't called (section 7). | Check that the result of every call is used in a condition or a calculation. |
| A test printout shows a good result, but the whole program a bad one | The function is correct, but the function using it, or `main`, uses it wrongly (section 6). | Also check the cooperation: call the calling function for the same boundaries. |
| The cost is wrong only at a boundary, for example for 2 kg or 5 kg | A threshold in the base-price function uses `<` instead of `<=`, or the other way round. | Check that function with printouts for 2, 3, 5 and 6. |
| The pricing rules are repeated in several places | Instead of calling a function, the code repeats its conditions. | Let one function know the rule, and let the others use its result. |
| Test printouts appear in the program's output | The test program and the final program are mixed together. | Keep the test printouts in a separate program, or remove them before the final check. |
| A cost appears after a failed read | The functions are called before the read is checked. | First check `std::cin.fail()`, then the range, and only then work out the cost. |
| The program does nothing and waits | It's waiting for another number, as in lesson 2.6. | Type a number and press **Enter**. Don't check a case where the data runs out this way: trace it on paper. |

## 11. Explain

Answer in your own words, preferably in writing. Only then compare with the example answers.

1. Why might a program need more than one own function?
2. Can an own function call another own function?
3. What happens to a helper function's result?
4. Does every function have to be called directly by `main`?
5. Why can a range-checking function return `bool`?
6. Why can a cost-calculating function return `int`?
7. Can a function use another function's result in its `return`?
8. Why is it worth separating calculations from printing?
9. Does each function being correct on its own guarantee that the whole program is correct?
10. Why do we prepare test printouts?
11. How does a test printout differ from the program's ordinary report?
12. Why is testing range boundaries important?
13. Should every single statement have its own function?
14. Why don't we use variables declared outside functions here?
15. Why does the order of definitions matter with the current way of organising the code?
16. Do we already need new ways of passing data to create several cooperating functions?

<details>
<summary>Example answers</summary>

1. Because a bigger problem is made of several jobs. Each of them can be named, written once and checked on its own.
2. Yes. It calls it the same way `main` does: by its name and arguments.
3. It goes to the function that called it and becomes a value there, for example in a condition or a calculation.
4. No. A function can be called by any function defined after it in the file, just as `measurement_status` calls the checking functions.
5. Because it answers a yes-or-no question: is the value acceptable.
6. Because the cost in this task is a number of whole zloty.
7. Yes, for example `return base_price(weight) + zone_surcharge(zone);`.
8. Because a function that only calculates can be called from different places and checked on its own. The place of the call decides what to print.
9. No. The functions can be correct, and the calling function or `main` can still use them wrongly, for example by skipping a result (section 7).
10. To check one function for chosen arguments before the whole program starts to depend on it.
11. A test printout shows one function's result for one argument and is for the person writing the program. The report is part of the program for the user. Test printouts don't stay in the final program.
12. Because bugs often sit exactly at the boundaries, for example `<` instead of `<=`. A value in the middle of a band doesn't reveal them.
13. No. A function makes sense when it has a clear job. A function that only passes its arguments on doesn't improve the program.
14. Because the functions pass data through arguments and returned results. That way each one depends only on what it received, and can be checked on its own.
15. Because the compiler reads the file from the top, and at the place of a call it must already know the function being called. That's why helper functions stand before the functions that use them.
16. No. The parameters, arguments and `return` you know from lessons 5.2–5.4 are enough.

</details>

## Summary

- One program can consist of **several functions with different jobs**. Each should have a job that can be named.
- **An own function can call another own function.** A helper function's result goes to the function that called it.
- Data passes between functions through arguments and returned results. The call, the run and the return can be traced in a table, step by step.
- Helper functions stand in the file before the functions that use them, and all of them before `main`.
- A **test printout** is a few calls with chosen arguments and a comparison of the results with expectations. It doesn't stay in the program for the user.
- Checking one function isn't the same as checking the program. **Functions can be correct on their own and still work together wrongly**, for example when a helper function's result is skipped.
- More functions don't mean a better program. A function makes sense when it has a clear job.

## What's next

Your programs now consist of several functions, arranged in the file so that each is written before it's called. In the next lesson you'll see another way of arranging functions: [Lesson 5.6: Declaration, definition and linking](lesson_06_declaration_and_definition.en.md).

---

## Example solutions

Look here **after your own attempt**. Your names may differ, as long as the standard output is as required.

<details>
<summary>Section 7: the output before the fix, and the fix</summary>

Before the fix:

<!-- output: status_ignored_bug -->
```text
2, 12.5: Measurement ready
0, 12.5: Invalid station data
2, -21.0: Below freezing
2, 41.0: Measurement ready
```

- **For 2, 12.5 and 0, 12.5** the results are correct. These cases don't reveal the bug: the first temperature is within the range, and the second pair is rejected already on the number of measurements.
- **For 2, -21.0 and 2, 41.0** the requirement says `Invalid station data`, but the program prints `Below freezing` and `Measurement ready`.
- **The cause:** the function `is_valid_temperature` is correct and it is called, but the line `is_valid_temperature(temperature);` **throws its result away**. No decision uses the answer `false`. The compiler doesn't warn, because calling a function on its own is a valid statement.
- **The fix:** use the result in a condition, as in section 3:

<!-- fragment -->
```cpp
    if (!is_valid_temperature(temperature)) {
        return "Invalid station data";
    }
```

The fixed program, with the same four cases:

<!-- example: status_ignored_fixed -->
```cpp
#include <iostream>
#include <string>

bool is_valid_measurement_count(int count) {
    return count >= 1 && count <= 24;
}

bool is_valid_temperature(double temperature) {
    return temperature >= -20.0 && temperature <= 40.0;
}

std::string measurement_status(int count, double temperature) {
    if (!is_valid_measurement_count(count)) {
        return "Invalid station data";
    }

    if (!is_valid_temperature(temperature)) {
        return "Invalid station data";
    }

    if (temperature < 0.0) {
        return "Below freezing";
    }

    return "Measurement ready";
}

int main() {
    std::cout << "2, 12.5: " << measurement_status(2, 12.5) << "\n";
    std::cout << "0, 12.5: " << measurement_status(0, 12.5) << "\n";
    std::cout << "2, -21.0: " << measurement_status(2, -21.0) << "\n";
    std::cout << "2, 41.0: " << measurement_status(2, 41.0) << "\n";
}
```

<!-- output: status_ignored_fixed -->
```text
2, 12.5: Measurement ready
0, 12.5: Invalid station data
2, -21.0: Invalid station data
2, 41.0: Invalid station data
```

</details>

<details>
<summary>Section 9: the mission, the delivery cost</summary>

First, the program with test printouts that checks the functions on their own:

<!-- example: shipping_checks -->
```cpp
#include <iostream>

bool is_valid_shipping_data(int weight, int zone) {
    return weight >= 1 && weight <= 8 && zone >= 1 && zone <= 3;
}

int base_price(int weight) {
    if (weight <= 2) {
        return 5;
    }

    if (weight <= 5) {
        return 8;
    }

    return 12;
}

int zone_surcharge(int zone) {
    if (zone == 1) {
        return 0;
    }

    if (zone == 2) {
        return 3;
    }

    return 6;
}

int shipping_cost(int weight, int zone) {
    return base_price(weight) + zone_surcharge(zone);
}

int main() {
    std::cout << "Valid 1, 1: " << is_valid_shipping_data(1, 1) << "\n";
    std::cout << "Valid 0, 1: " << is_valid_shipping_data(0, 1) << "\n";
    std::cout << "Valid 8, 3: " << is_valid_shipping_data(8, 3) << "\n";
    std::cout << "Valid 9, 1: " << is_valid_shipping_data(9, 1) << "\n";
    std::cout << "Valid 2, 4: " << is_valid_shipping_data(2, 4) << "\n";

    std::cout << "Base price 2: " << base_price(2) << "\n";
    std::cout << "Base price 3: " << base_price(3) << "\n";
    std::cout << "Base price 5: " << base_price(5) << "\n";
    std::cout << "Base price 6: " << base_price(6) << "\n";

    std::cout << "Surcharge 1: " << zone_surcharge(1) << "\n";
    std::cout << "Surcharge 2: " << zone_surcharge(2) << "\n";
    std::cout << "Surcharge 3: " << zone_surcharge(3) << "\n";

    std::cout << "Cost 2, 3: " << shipping_cost(2, 3) << "\n";
    std::cout << "Cost 6, 2: " << shipping_cost(6, 2) << "\n";
}
```

<!-- output: shipping_checks -->
```text
Valid 1, 1: 1
Valid 0, 1: 0
Valid 8, 3: 1
Valid 9, 1: 0
Valid 2, 4: 0
Base price 2: 5
Base price 3: 8
Base price 5: 8
Base price 6: 12
Surcharge 1: 0
Surcharge 2: 3
Surcharge 3: 6
Cost 2, 3: 11
Cost 6, 2: 15
```

Then the final program, with the same functions and no test printouts:

<!-- example: shipping_cost -->
```cpp
#include <iostream>

bool is_valid_shipping_data(int weight, int zone) {
    return weight >= 1 && weight <= 8 && zone >= 1 && zone <= 3;
}

int base_price(int weight) {
    if (weight <= 2) {
        return 5;
    }

    if (weight <= 5) {
        return 8;
    }

    return 12;
}

int zone_surcharge(int zone) {
    if (zone == 1) {
        return 0;
    }

    if (zone == 2) {
        return 3;
    }

    return 6;
}

int shipping_cost(int weight, int zone) {
    return base_price(weight) + zone_surcharge(zone);
}

int main() {
    int weight{0};
    int zone{0};

    std::cout << "Enter parcel weight and delivery zone:\n";
    std::cin >> weight;
    std::cin >> zone;

    if (std::cin.fail()) {
        std::cout << "Input could not be read\n";
    } else if (!is_valid_shipping_data(weight, zone)) {
        std::cout << "Invalid shipping data\n";
    } else {
        std::cout << "Shipping cost: " << shipping_cost(weight, zone) << "\n";
    }
}
```

| Function | Job | Receives | Returns | Who calls it |
|---|---|---|---|---|
| `is_valid_shipping_data` | whether the weight and zone are acceptable | the weight and the zone | `bool` | `main` |
| `base_price` | the base price by weight | the weight | `int` | `shipping_cost` |
| `zone_surcharge` | the surcharge by zone | the zone | `int` | `shipping_cost` |
| `shipping_cost` | the total cost | the weight and the zone | `int` | `main` |

- **Cooperation:** `shipping_cost` doesn't know the weight thresholds or the surcharges. It calls `base_price` and `zone_surcharge` and adds their results in its `return`. Each pricing rule appears in the code once.
- **The order of definitions:** `base_price` and `zone_surcharge` stand before `shipping_cost`, which calls them, and all of them before `main`.
- **An assumption:** `base_price` and `zone_surcharge` calculate correctly only for data within the range. For 9 kg, `base_price` would return 12. That's why `main` calls `shipping_cost` only after checking `is_valid_shipping_data`.
- **Checking on their own:** the program with test printouts checks every function at its boundaries (2 and 3, 5 and 6, every zone, out-of-range values), and the last two printouts check the cooperation. The final program contains only the report.
- **A failed read:** `main` checks `std::cin.fail()` first. After a failed read, including when the data ends after one number, no pricing function is called.
- This is one correct split. Another readable split is fine too if it meets the requirements, for example without a separate `zone_surcharge` function, with the surcharge worked out in `shipping_cost`.

</details>

**Previous lesson:** [Lesson 5.4: Several ways to `return`](lesson_04_several_returns.en.md) · **Next lesson:** [Lesson 5.6: Declaration, definition and linking](lesson_06_declaration_and_definition.en.md) · [Course overview](../../README.en.md)

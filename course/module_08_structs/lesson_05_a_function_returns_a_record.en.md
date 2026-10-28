# Lesson 8.5: A function returns a record with several results

[Polski](lesson_05_a_function_returns_a_record.md) · **English** · [Course overview](../../README.en.md)

> **Module 8, lesson 5** · about 75–90 minutes
> **You need:** your `cpp-workspace` folder and the original `lesson_05_first_program` project, as before. You won't need the debugger in this lesson.
> **Pilot version.** The programs in this lesson are checked automatically on Windows, Ubuntu and macOS. None of them asks for data: every value is written in the code. Only the check program in the solutions part reads data from the input.

## Before you start

This lesson assumes that you:

- write functions with a result type and `return` (lesson 5.3), and know that a function can return a new vector or a new text by value (lessons 6.5 and 7.3);
- define a struct, initialise all its fields in `{}`, and change the fields of an object without `const` (lessons 8.1 and 8.2);
- write functions that get a record by `const Product&` (lesson 8.3);
- go through a vector of records with `for (const Product& product : products)`, write a function for the whole vector, and store numbers of records as `std::size_t` (lesson 8.4).

## The situation

In lesson 8.3 two functions asked about one product: `stock_value` returned the stock value as an `int`, and `needs_restock` answered with a `bool` whether the stock needs topping up. That's a good design: each function answers one question.

Sometimes, though, several results belong to **one analysis**, and it's handier to hand them over together. A function returns one value, but that value can be a record of our own type, with several fields. Then one function hands over the whole set of answers, and `main` reads the fields from it.

After this lesson you will:

- design your own result type and tell it from the type of the input data;
- write a function that creates a local result, changes its fields, and returns it by value;
- receive the returned record in `main` and read its fields;
- combine a sum, a count and a yes-or-no answer in one result;
- keep, in a loop, information about what happened in all the records seen so far;
- choose data that reveal that such information gets lost.

## 1. Prepare the project

In `cpp-workspace`, create a folder `lesson_8_5` and copy `main.cpp` and `CMakeLists.txt` from the original `lesson_05_first_program` into it. You type the program from section 3 into that folder's `main.cpp`. The type `Product` comes from the earlier lessons of Module 8.

## 2. A result type

The result of analysing one product has two parts: the stock value and the answer whether it needs topping up. You can gather them in a separate struct:

<!-- fragment -->
```cpp
struct ProductReport {
    int stock_value;
    bool needs_restock;
};
```

| Type | What it describes |
|---|---|
| `Product` | the data of one product: the name, the stock, the minimum and the price |
| `ProductReport` | the result of analysing one product: the stock value and the restocking decision |

- **These are two different types,** each with its own fields. `Product` is data, and `ProductReport` is the answers to questions about that data.
- **The result's fields don't have to repeat the input's fields.** `ProductReport` has no name, stock or price, only what the analysis calculates.
- **The separate functions from lesson 8.3 are still correct.** A result struct is useful when several results come from one analysis and it's handy to pass them on together.

## 3. A function returns a record

<!-- example: product_report -->
```cpp
#include <iostream>
#include <string>

struct Product {
    std::string name;
    int stock;
    int minimum;
    int unit_price;
};

struct ProductReport {
    int stock_value;
    bool needs_restock;
};

ProductReport inspect_product(const Product& product) {
    ProductReport result{0, false};

    result.stock_value = product.stock * product.unit_price;
    result.needs_restock = product.stock < product.minimum;

    return result;
}

int main() {
    const Product tea{"Tea", 3, 8, 6};
    const ProductReport report{inspect_product(tea)};

    std::cout << "Product: " << tea.name << "\n";
    std::cout << "Stock value: " << report.stock_value << "\n";

    if (report.needs_restock) {
        std::cout << "Restock needed: yes\n";
    } else {
        std::cout << "Restock needed: no\n";
    }
}
```

Type the program and **predict** the result. You know the numbers from lesson 8.3 already, so running it is optional.

<details>
<summary>Standard output</summary>

<!-- output: product_report -->
```text
Product: Tea
Stock value: 18
Restock needed: yes
```

</details>

| Step in `inspect_product` | What happens |
|---|---|
| `ProductReport result{0, false};` | a local result is created with starting values for all the fields |
| `result.stock_value = ...;` | the function stores the stock value in a field: `3 * 6`, that is 18 |
| `result.needs_restock = ...;` | the function stores the answer in the second field: `3 < 8`, that is `true` |
| `return result;` | the function hands over the whole record: both fields at once |

- **The function's result type is `ProductReport`.** `return 18;` returns one number, and `return result;` a whole object with several fields, because that's the function's result type.
- **`main` receives the whole record** in one variable, `report`, and reads the fields from it with a dot: `report.stock_value` and `report.needs_restock`. An `if` chooses the text `yes` or `no`, as before.
- **The function prints nothing.** `main` takes the product's name from `tea`, because the result doesn't repeat it.

## 4. Input and result

| Place | Code | Role |
|---|---|---|
| the parameter | `const Product& product` | the input: an existing product, for reading only |
| a local variable | `ProductReport result{0, false};` | the result being built: the function changes its fields, so it isn't `const` |
| the function's result type | `ProductReport` | what the function hands over |
| receiving in `main` | `const ProductReport report{inspect_product(tea)};` | the finished result, which `main` doesn't change any more |

The `const` at the parameter concerns only the product. It doesn't forbid creating or changing the local result: that's a separate object, which belongs to the function.

## 5. Returning by value

You know the same model from lessons 6.5 and 7.3, where a function returned a new vector or a new text. Now it returns an object of our type:

1. the function creates a local result;
2. it prepares the values of its fields;
3. it returns the result by value;
4. the calling code receives it in its own variable.

The variable `result` ends together with the function, but its value reaches `main` as the result. **It isn't a reference to the function's variable:** `main` has its own record. Modern C++ returns such objects efficiently, and you'll learn how exactly later. For this lesson the model is enough.

**Predict:** this time the result was received without `const`, and then one of its fields was changed.

<!-- fragment -->
```cpp
const Product tea{"Tea", 3, 8, 6};
ProductReport report{inspect_product(tea)};

report.stock_value = 0;
```

What is `report.stock_value` now, and what is `tea.stock`? Could `inspect_product` have changed `tea`?

<details>
<summary>Answer</summary>

`report.stock_value` is 0, and `tea.stock` is still 3. `report` is a separate object, so changing its field doesn't affect the product, like the copy in lesson 8.2. The function couldn't have changed `tea` either: it got the product by `const&`, and worked on its own local result.

</details>

## 6. Mission: one analysis, three results

The program goes through energy meter readings in a simplified system, with no real devices and no units. The numbers are notional. One analysis of the whole list of meters has to give three results.

**Data:**

| Meter | Usage | Limit | Verified? |
|---|---:|---:|---|
| `Kitchen` | 8 | 6 | yes |
| `Office` | 3 | 5 | yes |
| `Hall` | 7 | 7 | no |
| `Lab` | 10 | 8 | no |

**Rules:**

- Usage is non-negative, and the limit is positive. The numbers are small, and the program doesn't check the data.
- **The total usage** is the sum of the usage of all the meters, unverified ones included.
- **A meter is above its limit** when its usage is **greater** than the limit. Usage equal to the limit isn't above it. Verification doesn't matter here.
- **An unverified reading exists** when at least one meter has an unverified reading, anywhere in the list. It doesn't have to be the last meter, or a meter above its limit.

These are three different kinds of information: a sum, a count and a yes-or-no answer.

**Requirements:**

- The program defines two types of its own. The meter type has four fields: the name (a text), the usage and the limit (whole numbers), and whether it's verified (yes or no). The result type has three fields: the total usage (`int`), the number of meters above their limit (`std::size_t`), and whether an unverified reading exists (`bool`). You choose the names of the types and the fields, and the order of the fields, on your own.
- All the meters are elements of one `const` vector, initialised in the code in the order of the table. No separate variable per meter and no `push_back`.
- The program has its own analysing function. It gets the whole vector by `const&`, creates a local result with starting values for all the fields, goes through the meters by `const&`, updates the result's three fields, and returns the whole result. It doesn't change the data, prints nothing and reads nothing from the input. You choose the names of the function and the parameter on your own. No other functions are needed.
- `main` creates the vector, calls the function once, and receives the result into one variable. It takes the number of meters from `size()`, and the other lines of the report from the result's fields. It calculates nothing a second time.
- The program prints exactly four lines, as in the example below: `Meters`, `Total usage`, `Above limit` and `Has unverified`, the last one with the word `yes` or `no`. It prints no meter names and no other messages.

In `cpp-workspace`, create a folder `meter_summary`, copy `CMakeLists.txt` from the original `lesson_05_first_program` into it, create an empty `main.cpp` and write the program on your own.

For the data above, the standard output must be:

<!-- output: meter_summary -->
```text
Meters: 4
Total usage: 28
Above limit: 2
Has unverified: yes
```

The total usage is 8 + 3 + 7 + 10, that is 28. `Kitchen` and `Lab` are above their limits, and `Hall` has usage equal to its limit. `Hall` and `Lab` don't have verified readings.

**This isn't the program about products with different names.** You have to decide on your own:

1. what to call both types and their fields;
2. what starting values the result has, and why exactly these;
3. how to change the sum in the loop, and how to change the count of meters above their limits;
4. how to make sure the information about an unverified reading doesn't get lost at the following meters;
5. how to return the result, and how to read its fields in `main`;
6. what the program prints for an empty vector;
7. whether the order of the meters can change the result.

**Before you write the program**, prepare a table of cases: an empty vector, one meter below its limit, at the limit and above it, all readings verified, one unverified reading at the start, in the middle and at the end of the list, and several unverified ones. For each, write down all three results.

**Then** run the program for the data from the requirements and for an empty vector. Change only the contents of the vector's braces. Every case in the full list of check cases is checked automatically.

### Success criteria

- The program builds as C++20 and, for the data from the requirements, prints exactly the four lines shown above.
- There are two types, a meter type with four fields and a result type with three fields of the types `int`, `std::size_t` and `bool`, and one `const` vector with four records, initialised in the code.
- The analysing function gets the vector by `const&`, builds a local result with starting values for all the fields, and returns the whole record. It prints nothing and changes nothing.
- `main` calls the function once and doesn't repeat its calculations.
- Usage equal to the limit isn't above it, and an unverified reading, once found, stays in the result, wherever it is in the list.
- For an empty vector the program prints `Meters: 0`, `Total usage: 0`, `Above limit: 0` and `Has unverified: no`.
- The table of cases was made before the program was run.
- You can explain how the result type differs from the meter type.

When the result matches, you can save the project in Git, as in lesson 1.5.

<details>
<summary>Hint 1</summary>

One analysis has to return three related results. What type of your own could you use to store them together?

</details>

<details>
<summary>Hint 2</summary>

Create a local result record with starting values. During the loop, update the right fields, and at the end return the whole record.

</details>

<details>
<summary>Hint 3</summary>

The sum grows by the usage, the count grows only when a limit is exceeded, and the information about an unverified reading should stay true if even one such reading has already appeared.

</details>

<details>
<summary>The full list of check cases: open it after preparing your own table</summary>

`8/6` means usage 8 with a limit of 6. An asterisk marks an unverified reading.

| | Meter list | Meters | Total usage | Above limit | Has unverified | What it checks |
|---|---|---:|---:|---:|---|---|
| A | the data from the requirements | 4 | 28 | 2 | yes | the data from the requirements |
| B | no meters | 0 | 0 | 0 | no | an empty vector |
| C | `Solo` 3/5 | 1 | 3 | 0 | no | one verified meter below its limit |
| D | `Peak` 9/5 | 1 | 9 | 1 | no | one verified meter above its limit |
| E | `Draft` 2/5* | 1 | 2 | 0 | yes | one unverified meter below its limit |
| F | `Edge` 7/7 | 1 | 7 | 0 | no | usage equal to the limit |
| G | `Alpha` 0/4, `Beta` 2/5, `Gamma` 4/6 | 3 | 6 | 0 | no | all below their limits and verified; zero usage |
| H | `Alpha` 6/5*, `Beta` 9/8, `Gamma` 4/1* | 3 | 19 | 3 | yes | all above their limits; several unverified |
| I | `Barn` 2/5*, `Loft` 3/5, `Yard` 4/5 | 3 | 9 | 0 | yes | an unverified reading at the start |
| J | `Loft` 3/5, `Yard` 4/5, `Barn` 2/5* | 3 | 9 | 0 | yes | an unverified reading at the end |
| K | `Loft` 3/5, `Barn` 2/5*, `Yard` 4/5 | 3 | 9 | 0 | yes | an unverified reading in the middle |
| L | `North` 6/4, `South` 6/4, `West` 6/4 | 3 | 18 | 3 | no | the same numbers in several records |
| M | the data from the requirements in reverse order | 4 | 28 | 2 | yes | another order, the same result |

**Automatic tests and your own runs.** Every case is checked automatically by a check program. It has the same types, the same function and the same report as the reference solution, but it reads the meters from the input. It's only a checking tool, not part of the mission: in the mission, the vector is written in the code. The check program and its results are in [Example solutions](#example-solutions), because they contain the solution.

</details>

An example solution is in [Example solutions](#example-solutions).

## 7. Find the bug: the flag forgets an earlier reading

Do this task **after the mission**: the program below contains a function similar to yours. You may type the program or copy it into `main.cpp`.

<details>
<summary>The program to check: open it after writing your own program</summary>

<!-- example: unverified_flag_bug -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>
#include <vector>

struct Meter {
    std::string name;
    int usage;
    int limit;
    bool verified;
};

struct MeterSummary {
    int total_usage;
    std::size_t above_limit;
    bool has_unverified;
};

MeterSummary summarise_meters(const std::vector<Meter>& meters) {
    MeterSummary result{0, 0, false};

    for (const Meter& meter : meters) {
        result.total_usage += meter.usage;

        if (meter.usage > meter.limit) {
            ++result.above_limit;
        }

        result.has_unverified = !meter.verified;
    }

    return result;
}

int main() {
    const std::vector<Meter> meters{
        {"Garage", 4, 6, true},
        {"Attic", 9, 5, true},
        {"Porch", 2, 3, false}
    };

    const MeterSummary summary{summarise_meters(meters)};

    std::cout << "Meters: " << meters.size() << "\n";
    std::cout << "Total usage: " << summary.total_usage << "\n";
    std::cout << "Above limit: " << summary.above_limit << "\n";

    if (summary.has_unverified) {
        std::cout << "Has unverified: yes\n";
    } else {
        std::cout << "Has unverified: no\n";
    }
}
```

1. **Predict** the standard output for the data in the program.
2. Run the program. Are all three results correct?
3. Change the data in the vector so that the bug becomes visible. First write down the correct results for your data, then run the program.
4. Trace the value of the field `has_unverified` after each pass of the loop.
5. Explain why information, once found, mustn't be forgotten because of a later meter.
6. Fix the function so that the sum and the count of meters above their limits work as before.
7. Run the fixed program for your vector.
8. Predict what the fixed program prints for an empty vector.
9. Predict the result for a vector in which all readings are verified.

</details>

The results, example data and the fixed program are in [Example solutions](#example-solutions).

## 8. When something goes differently

| What you see | What it means | What to do |
|---|---|---|
| The warning `non-void function does not return a value` | The function doesn't return a result: the `return` is missing. The result of such a call isn't defined (lesson 5.3). | At the end of the function, return the whole record: `return result;`. |
| `no viable conversion from 'ProductReport' to ...` | The function's result, a whole record, goes into a variable of another type, for example `int`. | Receive the whole record, and read the number from its field, for example `report.stock_value`. |
| `invalid operands to binary expression` at `std::cout << report` | `std::cout` won't print a whole record at once. | Print the fields one by one, for example `report.stock_value`. |
| `cannot assign to variable ... with const-qualified type` | The function changes the input record through `const&`, or `main` changes a result received as `const`. | Change only the local result in the function. Only read the input data. |
| The results are random numbers | The local result was created without starting values, for example `ProductReport result;`. Reading such fields is undefined behaviour, and the compiler doesn't have to warn about it. | Give the starting values of all the result's fields in `{}`. |
| `Has unverified` depends only on the last meter | The field is overwritten in each pass of the loop (section 7). | Set it to `true` when you meet an unverified reading, and never set it back. |
| `Above limit` also counts usage equal to the limit | The condition uses `>=` instead of `>`. | Above the limit means usage **greater** than the limit. |
| `Total usage` is too small | The addition of the usage stands inside a condition, so some meters, for example unverified ones, don't get into the sum. | Add the usage of every meter, outside any condition. |

## 9. Explain

Answer in your own words, preferably in writing. Only then compare with the example answers.

1. Why can one analysis have several results? When is it worth gathering them in one record, and when are separate functions enough?
2. What does the input struct describe, and what does the result struct describe? Does the result have to repeat the input's fields?
3. Can a function return your own type? What does `return result;` mean then?
4. Why isn't the local result `const`, although the parameter is?
5. Does the function return a reference to its local object? What happens to `result` when the function ends?
6. Why can the result's fields have different types? Give an example from the mission.
7. What values does the result have for an empty vector, and where do they come from?
8. How do you keep, in a loop, a yes-or-no piece of information that concerns all the records seen so far, not only the current one?
9. Why does the function return the result instead of printing it?

<details>
<summary>Example answers</summary>

1. Because one pass over the data can answer several questions at once, for example about the sum, the number of limits exceeded and missing verification. A record is useful when these answers belong to one analysis and are needed together. Separate functions are enough when the questions are independent, as in lesson 8.3.
2. The input struct describes data, for example one meter. The result struct describes the answers of the analysis. The result doesn't have to repeat the input's fields: it contains only what the analysis calculates.
3. Yes. The function's result type is then the struct's name, and `return result;` hands over the whole object, with all its fields.
4. Because the function changes the result's fields during the calculation. The `const` at the parameter concerns only the input data, and the local result is a separate object of the function.
5. No. The result is returned by value: `result` ends together with the function, and the calling code gets its own record, like the vector in lesson 6.5.
6. Because each field answers a different question and has a type that fits the answer: the total usage is an `int`, a number of meters is a `std::size_t`, and a yes-or-no answer is a `bool`.
7. The starting values: zero, zero and `false`. The loop makes no pass, so the function returns the result as it created it at the start. It's a valid record, with no special code.
8. Start with `false` and set `true` when the case you're looking for appears, but never copy into the field an answer that concerns only the current record. A `true`, once set, stays until the end of the loop.
9. Because then the function only calculates, and `main` decides what to print and how. The same result can be printed differently, checked, or passed on.

</details>

## Summary

- When several results belong to one analysis, you can define a result type and return an object of it.
- The input type describes data, and the result type describes answers. They're different structs with different fields.
- The function creates a local result with starting values, changes its fields, and returns it by value: `return result;`.
- `main` receives the whole record and reads its fields, and the input data doesn't change.
- A sum grows by every value, a count only when a condition holds, and a flag, once set to `true`, doesn't change any more.
- An empty vector gives a valid result: the starting values.

## What's next

In this lesson one function returned several results at once. The next lesson of Module 8 is in preparation.

---

## Example solutions

Look here **after your own attempt**. Your names may differ, as long as the standard output is as required.

<details>
<summary>Section 6: the mission, a meter report</summary>

<!-- example: meter_summary -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>
#include <vector>

struct Meter {
    std::string name;
    int usage;
    int limit;
    bool verified;
};

struct MeterSummary {
    int total_usage;
    std::size_t above_limit;
    bool has_unverified;
};

MeterSummary summarise_meters(const std::vector<Meter>& meters) {
    MeterSummary result{0, 0, false};

    for (const Meter& meter : meters) {
        result.total_usage += meter.usage;

        if (meter.usage > meter.limit) {
            ++result.above_limit;
        }

        if (!meter.verified) {
            result.has_unverified = true;
        }
    }

    return result;
}

int main() {
    const std::vector<Meter> meters{
        {"Kitchen", 8, 6, true},
        {"Office", 3, 5, true},
        {"Hall", 7, 7, false},
        {"Lab", 10, 8, false}
    };

    const MeterSummary summary{summarise_meters(meters)};

    std::cout << "Meters: " << meters.size() << "\n";
    std::cout << "Total usage: " << summary.total_usage << "\n";
    std::cout << "Above limit: " << summary.above_limit << "\n";

    if (summary.has_unverified) {
        std::cout << "Has unverified: yes\n";
    } else {
        std::cout << "Has unverified: no\n";
    }
}
```

1. **Two types of your own,** because they describe different things: `Meter` is the data of one meter, and `MeterSummary` is the answers of the analysis of the whole list.
2. **Different fields:** the result has no name and no limit. It has a sum, a number and a yes-or-no answer, which no meter stores.
3. **A record instead of one number,** because one analysis gives three answers. A function returning an `int` would hand over only one, and three separate functions would go through the vector three times and split one analysis.
4. **Zero, zero and `false` at the start,** because that's what the result looks like before the program has seen any meter: an empty sum, no limits exceeded, no unverified reading.
5. **The sum:** `result.total_usage += meter.usage;` for every meter, with no condition, so unverified ones count too.
6. **The count:** `++result.above_limit;` only when `meter.usage > meter.limit`.
7. **Equality isn't exceeding the limit,** because the rule speaks of usage greater than the limit. `Hall` has 7 with a limit of 7, so it doesn't count.
8. **The flag doesn't go back to `false`:** the program sets it to `true` inside `if (!meter.verified)`, and apart from the starting value it stores `false` nowhere. A later verified meter no longer changes this information.
9. **An empty vector gives a valid record:** the loop makes no pass, so the function returns the starting values.
10. **By value,** because `main` is to get its own, finished result, like the new vector in lesson 6.5. The local `result` ends with the function, so a reference to it wouldn't make sense.
11. **The input doesn't change:** the vector is `const`, and the function gets it and goes through it by `const&`. The function changes only its own local result.
12. **Printing in `main`,** because the function is only to calculate. `main` can print the same result differently, or use it further.

**The order of the meters doesn't change the result:** the sum and the number of limits exceeded don't depend on the order, and the flag answers whether an unverified reading appeared anywhere. Cases I, J, K and M check this.

**Other correct solutions:** instead of the `if`, you can write `result.has_unverified = result.has_unverified || !meter.verified;`, which gives the same. The types and fields can have other names and another order, as long as the values in the braces stand in the same order as the fields.

**The check program** checks every case in the list of check cases. The types and the function are the same as above, and so is the report from receiving the result on, apart from the indentation. There's one difference: the vector isn't written in the code, it's built from the input. The program reads the number of meters, then each meter: the name, the usage, the limit, and `yes` or `no` for the verification, turned into a `bool` with a comparison, as in lesson 3.4. Each meter read goes to the end of the vector with `push_back`, as in the check program of lesson 8.4. The mission needs neither input nor `push_back`.

<!-- example: meter_summary_check -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>
#include <vector>

struct Meter {
    std::string name;
    int usage;
    int limit;
    bool verified;
};

struct MeterSummary {
    int total_usage;
    std::size_t above_limit;
    bool has_unverified;
};

MeterSummary summarise_meters(const std::vector<Meter>& meters) {
    MeterSummary result{0, 0, false};

    for (const Meter& meter : meters) {
        result.total_usage += meter.usage;

        if (meter.usage > meter.limit) {
            ++result.above_limit;
        }

        if (!meter.verified) {
            result.has_unverified = true;
        }
    }

    return result;
}

int main() {
    std::vector<Meter> meters{};
    int count{0};

    std::cin >> count;

    for (int number{1}; number <= count; ++number) {
        std::string name{};
        int usage{0};
        int limit{0};
        std::string verified_answer{};

        std::cin >> name;
        std::cin >> usage;
        std::cin >> limit;
        std::cin >> verified_answer;

        const Meter meter{name, usage, limit, verified_answer == "yes"};
        meters.push_back(meter);
    }

    if (std::cin.fail()) {
        std::cout << "Input could not be read\n";
    } else {
        const MeterSummary summary{summarise_meters(meters)};

        std::cout << "Meters: " << meters.size() << "\n";
        std::cout << "Total usage: " << summary.total_usage << "\n";
        std::cout << "Above limit: " << summary.above_limit << "\n";

        if (summary.has_unverified) {
            std::cout << "Has unverified: yes\n";
        } else {
            std::cout << "Has unverified: no\n";
        }
    }
}
```

Each case starts with the number of meters. Then each meter takes one line: the name, the usage, the limit, and `yes` or `no` for the verification. The cases are in the order of the list of check cases, from A to M.

<!-- input: meter_summary_check -->
```text
4
Kitchen 8 6 yes
Office 3 5 yes
Hall 7 7 no
Lab 10 8 no
```

<!-- output: meter_summary_check -->
```text
Meters: 4
Total usage: 28
Above limit: 2
Has unverified: yes
```

<!-- input: meter_summary_check -->
```text
0
```

<!-- output: meter_summary_check -->
```text
Meters: 0
Total usage: 0
Above limit: 0
Has unverified: no
```

<!-- input: meter_summary_check -->
```text
1
Solo 3 5 yes
```

<!-- output: meter_summary_check -->
```text
Meters: 1
Total usage: 3
Above limit: 0
Has unverified: no
```

<!-- input: meter_summary_check -->
```text
1
Peak 9 5 yes
```

<!-- output: meter_summary_check -->
```text
Meters: 1
Total usage: 9
Above limit: 1
Has unverified: no
```

<!-- input: meter_summary_check -->
```text
1
Draft 2 5 no
```

<!-- output: meter_summary_check -->
```text
Meters: 1
Total usage: 2
Above limit: 0
Has unverified: yes
```

<!-- input: meter_summary_check -->
```text
1
Edge 7 7 yes
```

<!-- output: meter_summary_check -->
```text
Meters: 1
Total usage: 7
Above limit: 0
Has unverified: no
```

<!-- input: meter_summary_check -->
```text
3
Alpha 0 4 yes
Beta 2 5 yes
Gamma 4 6 yes
```

<!-- output: meter_summary_check -->
```text
Meters: 3
Total usage: 6
Above limit: 0
Has unverified: no
```

<!-- input: meter_summary_check -->
```text
3
Alpha 6 5 no
Beta 9 8 yes
Gamma 4 1 no
```

<!-- output: meter_summary_check -->
```text
Meters: 3
Total usage: 19
Above limit: 3
Has unverified: yes
```

<!-- input: meter_summary_check -->
```text
3
Barn 2 5 no
Loft 3 5 yes
Yard 4 5 yes
```

<!-- output: meter_summary_check -->
```text
Meters: 3
Total usage: 9
Above limit: 0
Has unverified: yes
```

<!-- input: meter_summary_check -->
```text
3
Loft 3 5 yes
Yard 4 5 yes
Barn 2 5 no
```

<!-- output: meter_summary_check -->
```text
Meters: 3
Total usage: 9
Above limit: 0
Has unverified: yes
```

<!-- input: meter_summary_check -->
```text
3
Loft 3 5 yes
Barn 2 5 no
Yard 4 5 yes
```

<!-- output: meter_summary_check -->
```text
Meters: 3
Total usage: 9
Above limit: 0
Has unverified: yes
```

<!-- input: meter_summary_check -->
```text
3
North 6 4 yes
South 6 4 yes
West 6 4 yes
```

<!-- output: meter_summary_check -->
```text
Meters: 3
Total usage: 18
Above limit: 3
Has unverified: no
```

<!-- input: meter_summary_check -->
```text
4
Lab 10 8 no
Hall 7 7 no
Office 3 5 yes
Kitchen 8 6 yes
```

<!-- output: meter_summary_check -->
```text
Meters: 4
Total usage: 28
Above limit: 2
Has unverified: yes
```

</details>

<details>
<summary>Section 7: the results before the fix, and the fixed program</summary>

Before the fix, for the data in the program:

<!-- output: unverified_flag_bug -->
```text
Meters: 3
Total usage: 15
Above limit: 1
Has unverified: yes
```

- **All three results look right.** The sum 4 + 9 + 2 is 15, only `Attic` is above its limit, and `Porch` has an unverified reading. But `Porch` stands at the end of the list, and the function copies into the flag the answer about the current meter. So the final flag describes only the last meter, and here that happens to be the correct answer.
- **Data that reveal the bug:** an unverified reading followed by at least one verified meter. For example, adding `{"Shed", 1, 4, true}` at the end. The correct results are 4, 16, 1 and `yes`. The program with the bug prints:

<!-- example: unverified_flag_revealed -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>
#include <vector>

struct Meter {
    std::string name;
    int usage;
    int limit;
    bool verified;
};

struct MeterSummary {
    int total_usage;
    std::size_t above_limit;
    bool has_unverified;
};

MeterSummary summarise_meters(const std::vector<Meter>& meters) {
    MeterSummary result{0, 0, false};

    for (const Meter& meter : meters) {
        result.total_usage += meter.usage;

        if (meter.usage > meter.limit) {
            ++result.above_limit;
        }

        result.has_unverified = !meter.verified;
    }

    return result;
}

int main() {
    const std::vector<Meter> meters{
        {"Garage", 4, 6, true},
        {"Attic", 9, 5, true},
        {"Porch", 2, 3, false},
        {"Shed", 1, 4, true}
    };

    const MeterSummary summary{summarise_meters(meters)};

    std::cout << "Meters: " << meters.size() << "\n";
    std::cout << "Total usage: " << summary.total_usage << "\n";
    std::cout << "Above limit: " << summary.above_limit << "\n";

    if (summary.has_unverified) {
        std::cout << "Has unverified: yes\n";
    } else {
        std::cout << "Has unverified: no\n";
    }
}
```

<!-- output: unverified_flag_revealed -->
```text
Meters: 4
Total usage: 16
Above limit: 1
Has unverified: no
```

| After the pass for | `has_unverified` with the bug | `has_unverified` correctly |
|---|---|---|
| `Garage`, verified | `false` | `false` |
| `Attic`, verified | `false` | `false` |
| `Porch`, unverified | `true` | `true` |
| `Shed`, verified | **`false`** | `true` |

- **The cause:** the line `result.has_unverified = !meter.verified;` replaces the flag in each pass with the answer about the current meter. But the field is to describe the whole list seen so far: an unverified reading, once found, doesn't stop existing just because the next meter is verified. The sum and the count of meters above their limits work correctly, so they won't reveal the bug on their own.
- **The fix:** set the flag only when you meet an unverified reading, and never set it back.

<!-- example: unverified_flag_fixed -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>
#include <vector>

struct Meter {
    std::string name;
    int usage;
    int limit;
    bool verified;
};

struct MeterSummary {
    int total_usage;
    std::size_t above_limit;
    bool has_unverified;
};

MeterSummary summarise_meters(const std::vector<Meter>& meters) {
    MeterSummary result{0, 0, false};

    for (const Meter& meter : meters) {
        result.total_usage += meter.usage;

        if (meter.usage > meter.limit) {
            ++result.above_limit;
        }

        if (!meter.verified) {
            result.has_unverified = true;
        }
    }

    return result;
}

int main() {
    const std::vector<Meter> meters{
        {"Garage", 4, 6, true},
        {"Attic", 9, 5, true},
        {"Porch", 2, 3, false},
        {"Shed", 1, 4, true}
    };

    const MeterSummary summary{summarise_meters(meters)};

    std::cout << "Meters: " << meters.size() << "\n";
    std::cout << "Total usage: " << summary.total_usage << "\n";
    std::cout << "Above limit: " << summary.above_limit << "\n";

    if (summary.has_unverified) {
        std::cout << "Has unverified: yes\n";
    } else {
        std::cout << "Has unverified: no\n";
    }
}
```

<!-- output: unverified_flag_fixed -->
```text
Meters: 4
Total usage: 16
Above limit: 1
Has unverified: yes
```

For an empty vector the fixed program prints the same as the check program in case B: the loop makes no pass, so the starting values stay. When all readings are verified, both versions return `false`, because the flag never gets `true`. So neither an empty vector, nor such a vector, nor a list with the unverified reading at the end reveals the bug: you need an unverified reading followed by a verified one. The data from the mission also end with an unverified reading (`Lab`), so the same bug in your program would go unnoticed for them. Cases I, K and M from the list of check cases reveal it.

</details>

**Previous lesson:** [Lesson 8.4: Many records in a `std::vector`](lesson_04_many_records_in_a_vector.en.md) · **Next lesson:** in preparation · [Course overview](../../README.en.md)

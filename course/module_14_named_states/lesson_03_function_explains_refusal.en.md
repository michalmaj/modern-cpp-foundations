# Lesson 14.3: A function explains why it refused

[Polski](lesson_03_function_explains_refusal.md) · **English** · [Course overview](../../README.en.md)

> **Module 14, lesson 3** · about 90–110 minutes, can be split into two sessions (sections 1–7, then the mission)
> **You need:** your `cpp-workspace` folder and the original `lesson_05_first_program` project, as before. You won't need the debugger in this lesson.
> **Pilot version.** The programs in this lesson are checked automatically on Windows, Ubuntu and macOS, together with their exit codes. The programs that mustn't build are checked together with the place of their first error. No program asks for input: all the values are written in the code.

## Before you start

This lesson assumes that you:

- write a function that changes data passed by `&` only when the conditions are met and returns `bool`, like `issue_units` in lesson 9.2;
- know that `false` from such a function doesn't say which condition wasn't met (lesson 9.4);
- define an `enum class` type, compare its values with `==` and turn them into text (lesson 14.1);
- handle every value of an enumeration with a `switch` statement and end a label with `return` or `break` (lesson 14.2);
- write one-file test programs with the functions `check_int`, `check_bool` and `check_text` that end with exit code 1 when a check fails, and choose cases that tell a correct function from a version with a bug (lessons 13.1–13.3).

## The situation

We're back in the warehouse from lesson 9.2. The function `issue_units` issues goods only when it's allowed, and returns `true` or `false`. When an issue fails, the warehouse gets `false` and doesn't know what to fix: the amount in the request or the stock. Lesson 9.4 said that if the program had to give the cause of a refusal, it would need a result that carries more information. In this lesson you design such a result.

You'll answer the question: **how should a function say why it refused, and how do you check separately what it said and what it did to the data?**

After this lesson you will:

- recognise when `bool` isn't enough, because a refusal has several different reasons;
- design an `enum class` type whose values name every possible ending of an operation, and return it from a function;
- handle each result separately in the calling code, with a `switch` statement;
- keep the operation result apart from its effect, the change to the data passed by `&`, and make sure a refusal changes nothing;
- check the named result and the state of the data after the call separately in tests;
- set and test the refusal precedence when several reasons apply at once.

## 1. What `false` says

This was the function from lesson 9.2:

<!-- fragment -->
```cpp
bool issue_units(Product& product, int amount) {
    if (amount <= 0 || amount > product.stock) {
        return false;
    }

    product.stock -= amount;
    return true;
}
```

One refusal condition joins two different reasons with `||`. For a product `tea` with 7 units:

| Call | Reason for refusal | Result |
|---|---|---|
| `issue_units(tea, 0)` | an invalid amount | `false` |
| `issue_units(tea, 8)` | not enough goods | `false` |

The caller gets the same thing in both cases. To give the reason, it would have to check the amount once more itself:

<!-- fragment -->
```cpp
const bool accepted{issue_units(tea, amount)};

if (!accepted) {
    if (amount <= 0) {
        std::cout << "Invalid amount\n";
    } else {
        std::cout << "Not enough stock\n";
    }
}
```

That works, but the rule now stands in two places: in the function and in `main`. If someone changes it in the function, for example to refuse requests of fewer than 2 units, and forgets `main`, the report for a request of 1 gives the wrong reason: `Not enough stock`, although there are enough goods. The function checks the conditions, so the function itself should know the reason for a refusal and report it.

## 2. A named result and the contract

An issue can end in three ways. Each gets its own name, in an enumeration from lesson 14.1:

<!-- fragment -->
```cpp
enum class IssueResult {
    issued,
    invalid_amount,
    insufficient_stock
};
```

- `IssueResult::issued`: the goods were issued;
- `IssueResult::invalid_amount`: an invalid request, an amount of 0 or less;
- `IssueResult::insufficient_stock`: not enough goods in stock.

Each of them is a **named result**: a value of the same type, `IssueResult`. It isn't text, a number or a separate way of reporting errors. A refusal result is as ordinary a value as a success result.

The new version of the function returns this type:

<!-- fragment -->
```cpp
IssueResult issue_units(int requested, int& stock);
```

**What changes compared with lesson 9.2:**

| | Lesson 9.2 | This lesson |
|---|---|---|
| Result type | `bool` | `IssueResult` |
| Data it changes | the whole record: `Product& product` | only the stock: `int& stock` |
| Order of the parameters | the record first, then the amount | the requested amount first, then the stock |
| Refusal conditions | one condition with `||` | two separate conditions, because each reason has its own result |

**What stays the same:** an amount of 0 or less is refused, issuing the whole stock is allowed, with an empty stock every positive request is refused, and a refusal changes nothing. The function still prints nothing. It doesn't need the product's name or price to issue goods, so it gets only the number of units in stock, kept in an `int` variable.

**The result and the effect are two different things**, as in lesson 9.2:

| What | How it reaches the caller | When |
|---|---|---|
| **The result:** how the operation ended | the `IssueResult` value given by `return` | always |
| **The effect:** a smaller stock | a change to the variable passed as `int& stock` | only with `issued` |

The named result doesn't replace the parameter `int& stock`. The function doesn't return the new stock instead of the result: it returns how the operation ended, and changes the stock through the reference, and only on success.

### The contract of `issue_units`

**Assumption:** `stock` is 0 or more on entry. The function doesn't check it: it's a condition the caller takes care of.

- When `requested <= 0`: the result is `IssueResult::invalid_amount`, `stock` unchanged.
- When `requested > stock`: the result is `IssueResult::insufficient_stock`, `stock` unchanged.
- In every other case, that is when `requested > 0` and `requested <= stock`: `stock` decreases by `requested`, and the result is `IssueResult::issued`.

**After a refusal, `stock` has exactly the same value as before the call.** The function mustn't decrease the stock first and report a refusal afterwards.

The cases from the contract, with the result written without `IssueResult::`:

| Case | `requested` | `stock` before | Result | `stock` after |
|---|---:|---:|---|---:|
| A | 3 | 7 | `issued` | 4 |
| B | 7 | 7 | `issued` | 0 |
| C | 0 | 7 | `invalid_amount` | 7 |
| D | -2 | 7 | `invalid_amount` | 7 |
| E | 8 | 7 | `insufficient_stock` | 7 |
| F | 1 | 0 | `insufficient_stock` | 0 |
| G | 1 | 7 | `issued` | 6 |

Every row follows from the three rules above, not from the function's code. B issues the whole stock, and F shows an empty warehouse.

## 3. The function and a program that handles every result

<!-- example: issue_requests -->
```cpp
#include <iostream>
#include <vector>

enum class IssueResult {
    issued,
    invalid_amount,
    insufficient_stock
};

IssueResult issue_units(int requested, int& stock) {
    if (requested <= 0) {
        return IssueResult::invalid_amount;
    }

    if (requested > stock) {
        return IssueResult::insufficient_stock;
    }

    stock -= requested;
    return IssueResult::issued;
}

int main() {
    int stock{7};
    const std::vector<int> requests{3, 0, 8, 4};

    std::cout << "Stock: " << stock << "\n";

    for (const int requested : requests) {
        const IssueResult result{issue_units(requested, stock)};

        std::cout << "Request " << requested << ": ";

        switch (result) {
            case IssueResult::issued:
                std::cout << "Units issued, " << stock << " left\n";
                break;
            case IssueResult::invalid_amount:
                std::cout << "Invalid amount, ask for at least 1\n";
                break;
            case IssueResult::insufficient_stock:
                std::cout << "Not enough stock, only " << stock << " available\n";
                break;
        }
    }

    std::cout << "Final stock: " << stock << "\n";
}
```

**This is the first required run.** In `cpp-workspace`, create a folder `lesson_14_3`, copy `main.cpp` and `CMakeLists.txt` from the original `lesson_05_first_program` into it, and replace the contents of `main.cpp` with the program above. **Predict** all six lines, then run the program.

<details>
<summary>Standard output</summary>

<!-- output: issue_requests -->
```text
Stock: 7
Request 3: Units issued, 4 left
Request 0: Invalid amount, ask for at least 1
Request 8: Not enough stock, only 4 available
Request 4: Units issued, 0 left
Final stock: 0
```

</details>

- **The checks first, then the change.** Each guard clause ends the function with its own result before `stock -= requested;` runs. Only a request that passed both checks reaches the change, as in lesson 9.2.
- **Each reason has its own `return`.** The `||` condition from lesson 9.2 is split into two `if`s, because each reason for refusal has a different result value. Each check appears in the function once.
- **`const IssueResult result{issue_units(requested, stock)};`** calls the function once and keeps the result. The `switch` then looks at the kept value. A second call would be another attempt to issue goods (lesson 9.2).
- **The `switch` in `main` does something different for each result:** after an issue it says how many are left, for an invalid request it says what amount is allowed, and for missing goods it says how many are available. The `case` labels name all three results, as in lesson 14.2.
- **Here `break` leaves only the `switch`.** The loop carries on and takes the next request.
- **Refusals don't change the stock:** after the requests 0 and 8 there are still 4 units, so the last request, 4, issues everything that's left.

**Does the order of the two checks matter here?** Not with this contract. When `requested <= 0`, the condition `requested > stock` is false, because `stock` is at least 0. The two reasons for refusal never apply at once, so swapping the two `if`s doesn't change any result. That follows from the assumption that `stock` isn't negative. Moving the change of the stock before the checks, though, isn't allowed: a refusal would then leave the stock decreased. In the mission two reasons for refusal can apply at once, and there the order of the checks changes the result.

## 4. The result is a value of type `IssueResult`

Two habits from earlier lessons don't work here. Neither program below builds. You don't have to build them: they're checked automatically, and you know their result from the description.

**The result in an `if` condition, like `bool` in lesson 9.2:**

<!-- broken: issue_if_bool at=25:9 errors=1 error=^value of type 'IssueResult' is not contextually convertible to 'bool' -->
```cpp
#include <iostream>

enum class IssueResult {
    issued,
    invalid_amount,
    insufficient_stock
};

IssueResult issue_units(int requested, int& stock) {
    if (requested <= 0) {
        return IssueResult::invalid_amount;
    }

    if (requested > stock) {
        return IssueResult::insufficient_stock;
    }

    stock -= requested;
    return IssueResult::issued;
}

int main() {
    int stock{7};

    if (issue_units(3, stock)) {
        std::cout << "Units issued\n";
    }
}
```

The compiler reports an error on line 25: `value of type 'IssueResult' is not contextually convertible to 'bool'`. A value of an `enum class` type can't be used where a `bool` is needed. That's a good thing: it wouldn't be clear whether "true" means `issued` or one of the refusals.

**A comparison with text:**

<!-- broken: issue_compare_text at=26:16 errors=1 error=^invalid operands to binary expression -->
```cpp
#include <iostream>

enum class IssueResult {
    issued,
    invalid_amount,
    insufficient_stock
};

IssueResult issue_units(int requested, int& stock) {
    if (requested <= 0) {
        return IssueResult::invalid_amount;
    }

    if (requested > stock) {
        return IssueResult::insufficient_stock;
    }

    stock -= requested;
    return IssueResult::issued;
}

int main() {
    int stock{7};
    const IssueResult result{issue_units(3, stock)};

    if (result == "issued") {
        std::cout << "Units issued\n";
    }
}
```

The error on line 26 starts with `invalid operands to binary expression`, as when printing a state in lesson 14.1. This time there's no `==` for the pair: a value of type `IssueResult` and text in quotes. The result isn't the text `"issued"` but the value `IssueResult::issued`. Before this error Clang may also print a warning about comparing with text in quotes. What stops the build is the error.

In both cases the fix is the same: keep the result in a variable and compare it with a value of the same type, or handle every value with a `switch` statement, as in section 3.

<!-- fragment -->
```cpp
const IssueResult result{issue_units(3, stock)};

if (result == IssueResult::issued) {
    std::cout << "Units issued\n";
}
```

## 5. The result as text

In the tests a `FAIL` line has to show the result, and `std::cout` can't print an `IssueResult` value directly (lesson 14.1). The function `issue_result_text` turns a result into text the same way as `status_text` in lesson 14.2: a `switch` in which every label returns the text at once, and a fallback after the `switch`.

<!-- fragment -->
```cpp
std::string issue_result_text(IssueResult result) {
    switch (result) {
        case IssueResult::issued:
            return "issued";
        case IssueResult::invalid_amount:
            return "invalid_amount";
        case IssueResult::insufficient_stock:
            return "insufficient_stock";
    }

    return "unknown";
}
```

| Result | Text |
|---|---|
| `IssueResult::issued` | `"issued"` |
| `IssueResult::invalid_amount` | `"invalid_amount"` |
| `IssueResult::insufficient_stock` | `"insufficient_stock"` |

The text is only for printing. The program compares results as `IssueResult` values.

## 6. A test program: the result and the state separately

Each call to `issue_units` has two properties to check: **the named result** and **the state after the call**. You check them separately, because a function can get one wrong and the other right.

Two check functions are needed. `check_int` from lesson 13.3 compares the stock. `check_issue_result` compares two `IssueResult` values with `==`, and turns them into text with `issue_result_text` for the `FAIL` line. It's built like `check_status` from lesson 14.1:

<!-- fragment -->
```cpp
void check_issue_result(const std::string& name, IssueResult expected, IssueResult actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << issue_result_text(expected) << ", actual " << issue_result_text(actual) << "\n";
        ++failed;
    }
}
```

Three rules of this program:

- **The test compares with exactly the result the contract gives.** A check "the result isn't `issued`" passes for both refusals, even when the function gives the wrong reason. `IssueResult::invalid_amount` and `IssueResult::insufficient_stock` are different results, so the test checks which one came back.
- **`issue_result_text` has its own tests too.** The comparison in `check_issue_result` is about values, so PASS and FAIL are right even if a text is wrong. A wrong text would spoil what the `FAIL` line says, though, for example `expected issued, actual issued`. That's why the first three checks compare the texts with the table in section 5, using `check_text`. The expected results are strings from the table, not calls to the same function.
- **Each case has its own stock variable.** `stock_a` starts at 7, `stock_f` at 0, each as in the table in section 2. If the cases shared one variable, B would start from the stock that A left.

**The number of checks:** 7 cases with 2 checks each give 14, plus 3 checks of the text, 17 in all. A case is one call with data from the table. A check is one comparison with one `PASS` or `FAIL` line.

**This is the second required run.** Replace the contents of `main.cpp` with the program below. You can copy the functions `check_int` and `check_text` from lesson 13.3, and the others from sections 3, 5 and 6. **Predict** the last line of the output before you run the program.

<details>
<summary>The full test program</summary>

<!-- example: issue_tests -->
```cpp
#include <iostream>
#include <string>

enum class IssueResult {
    issued,
    invalid_amount,
    insufficient_stock
};

IssueResult issue_units(int requested, int& stock) {
    if (requested <= 0) {
        return IssueResult::invalid_amount;
    }

    if (requested > stock) {
        return IssueResult::insufficient_stock;
    }

    stock -= requested;
    return IssueResult::issued;
}

std::string issue_result_text(IssueResult result) {
    switch (result) {
        case IssueResult::issued:
            return "issued";
        case IssueResult::invalid_amount:
            return "invalid_amount";
        case IssueResult::insufficient_stock:
            return "insufficient_stock";
    }

    return "unknown";
}

void check_issue_result(const std::string& name, IssueResult expected, IssueResult actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << issue_result_text(expected) << ", actual " << issue_result_text(actual) << "\n";
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

    check_text("issue_result_text(issued)", "issued", issue_result_text(IssueResult::issued), checks, failed);
    check_text("issue_result_text(invalid_amount)", "invalid_amount", issue_result_text(IssueResult::invalid_amount), checks, failed);
    check_text("issue_result_text(insufficient_stock)", "insufficient_stock", issue_result_text(IssueResult::insufficient_stock), checks, failed);

    int stock_a{7};
    const IssueResult result_a{issue_units(3, stock_a)};
    check_issue_result("A result", IssueResult::issued, result_a, checks, failed);
    check_int("A stock", 4, stock_a, checks, failed);

    int stock_b{7};
    const IssueResult result_b{issue_units(7, stock_b)};
    check_issue_result("B result", IssueResult::issued, result_b, checks, failed);
    check_int("B stock", 0, stock_b, checks, failed);

    int stock_c{7};
    const IssueResult result_c{issue_units(0, stock_c)};
    check_issue_result("C result", IssueResult::invalid_amount, result_c, checks, failed);
    check_int("C stock", 7, stock_c, checks, failed);

    int stock_d{7};
    const IssueResult result_d{issue_units(-2, stock_d)};
    check_issue_result("D result", IssueResult::invalid_amount, result_d, checks, failed);
    check_int("D stock", 7, stock_d, checks, failed);

    int stock_e{7};
    const IssueResult result_e{issue_units(8, stock_e)};
    check_issue_result("E result", IssueResult::insufficient_stock, result_e, checks, failed);
    check_int("E stock", 7, stock_e, checks, failed);

    int stock_f{0};
    const IssueResult result_f{issue_units(1, stock_f)};
    check_issue_result("F result", IssueResult::insufficient_stock, result_f, checks, failed);
    check_int("F stock", 0, stock_f, checks, failed);

    int stock_g{7};
    const IssueResult result_g{issue_units(1, stock_g)};
    check_issue_result("G result", IssueResult::issued, result_g, checks, failed);
    check_int("G stock", 6, stock_g, checks, failed);

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

<!-- output: issue_tests -->
```text
PASS issue_result_text(issued)
PASS issue_result_text(invalid_amount)
PASS issue_result_text(insufficient_stock)
PASS A result
PASS A stock
PASS B result
PASS B stock
PASS C result
PASS C stock
PASS D result
PASS D stock
PASS E result
PASS E stock
PASS F result
PASS F stock
PASS G result
PASS G stock
Checks: 17, failed: 0
```

Exit code: 0.

</details>

## 7. Diagnostic: the wrong reason for refusal

Someone writes the second guard clause by copying the first one and forgets to change the result:

<!-- fragment -->
```cpp
IssueResult issue_units(int requested, int& stock) {
    if (requested <= 0) {
        return IssueResult::invalid_amount;
    }

    if (requested > stock) {
        return IssueResult::invalid_amount;
    }

    stock -= requested;
    return IssueResult::issued;
}
```

The function still refuses exactly when it should, and still doesn't change the stock when it refuses. It only gets the reason wrong.

**This is the third required run.** Follow the steps in order:

1. **Predict** from the table in section 2, before you change anything: which cases does the second clause handle? Which of their checks will fail, and which will pass? What will the last line say?
2. In the test program from section 6, change `return IssueResult::insufficient_stock;` in the second clause to `return IssueResult::invalid_amount;`. Change nothing else, neither the tests nor the expected results.
3. Run the tests. Note the `FAIL` lines, the summary and the exit code.
4. Restore `return IssueResult::insufficient_stock;` and run the same tests again.

<details>
<summary>What happens and how to fix it: open after steps 1–4</summary>

**The map of effects:**

| Case | Data | Expected result | Actual result | Check of the result | Check of the stock |
|---|---|---|---|---|---|
| E | 8 units with a stock of 7 | `insufficient_stock` | `invalid_amount` | `FAIL` | `PASS` |
| F | 1 unit with a stock of 0 | `insufficient_stock` | `invalid_amount` | `FAIL` | `PASS` |
| A–D, G | as in the table | as in the table | unchanged | `PASS` | `PASS` |
| texts | three values | as in the table in section 5 | unchanged | `PASS` | — |

- **One line is changed.** Only positive requests reach the second clause, and it refuses only those larger than the stock, so the bug affects exactly cases E and F.
- **The stock is right,** because the clause still ends the function before the stock changes. That's why the checks of the stock pass. Not every bug spoils the result and the data at once.
- **With `bool` such a mistake couldn't be seen in the result:** both refusals gave the same `false`. A named result says **what** failed, and the test checks whether it tells the truth.

The test program with this change, and no other:

<!-- example: issue_tests_wrong_reason exit=1 -->
```cpp
#include <iostream>
#include <string>

enum class IssueResult {
    issued,
    invalid_amount,
    insufficient_stock
};

IssueResult issue_units(int requested, int& stock) {
    if (requested <= 0) {
        return IssueResult::invalid_amount;
    }

    if (requested > stock) {
        return IssueResult::invalid_amount;
    }

    stock -= requested;
    return IssueResult::issued;
}

std::string issue_result_text(IssueResult result) {
    switch (result) {
        case IssueResult::issued:
            return "issued";
        case IssueResult::invalid_amount:
            return "invalid_amount";
        case IssueResult::insufficient_stock:
            return "insufficient_stock";
    }

    return "unknown";
}

void check_issue_result(const std::string& name, IssueResult expected, IssueResult actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << issue_result_text(expected) << ", actual " << issue_result_text(actual) << "\n";
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

    check_text("issue_result_text(issued)", "issued", issue_result_text(IssueResult::issued), checks, failed);
    check_text("issue_result_text(invalid_amount)", "invalid_amount", issue_result_text(IssueResult::invalid_amount), checks, failed);
    check_text("issue_result_text(insufficient_stock)", "insufficient_stock", issue_result_text(IssueResult::insufficient_stock), checks, failed);

    int stock_a{7};
    const IssueResult result_a{issue_units(3, stock_a)};
    check_issue_result("A result", IssueResult::issued, result_a, checks, failed);
    check_int("A stock", 4, stock_a, checks, failed);

    int stock_b{7};
    const IssueResult result_b{issue_units(7, stock_b)};
    check_issue_result("B result", IssueResult::issued, result_b, checks, failed);
    check_int("B stock", 0, stock_b, checks, failed);

    int stock_c{7};
    const IssueResult result_c{issue_units(0, stock_c)};
    check_issue_result("C result", IssueResult::invalid_amount, result_c, checks, failed);
    check_int("C stock", 7, stock_c, checks, failed);

    int stock_d{7};
    const IssueResult result_d{issue_units(-2, stock_d)};
    check_issue_result("D result", IssueResult::invalid_amount, result_d, checks, failed);
    check_int("D stock", 7, stock_d, checks, failed);

    int stock_e{7};
    const IssueResult result_e{issue_units(8, stock_e)};
    check_issue_result("E result", IssueResult::insufficient_stock, result_e, checks, failed);
    check_int("E stock", 7, stock_e, checks, failed);

    int stock_f{0};
    const IssueResult result_f{issue_units(1, stock_f)};
    check_issue_result("F result", IssueResult::insufficient_stock, result_f, checks, failed);
    check_int("F stock", 0, stock_f, checks, failed);

    int stock_g{7};
    const IssueResult result_g{issue_units(1, stock_g)};
    check_issue_result("G result", IssueResult::issued, result_g, checks, failed);
    check_int("G stock", 6, stock_g, checks, failed);

    std::cout << "Checks: " << checks << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

<!-- output: issue_tests_wrong_reason -->
```text
PASS issue_result_text(issued)
PASS issue_result_text(invalid_amount)
PASS issue_result_text(insufficient_stock)
PASS A result
PASS A stock
PASS B result
PASS B stock
PASS C result
PASS C stock
PASS D result
PASS D stock
FAIL E result: expected insufficient_stock, actual invalid_amount
PASS E stock
FAIL F result: expected insufficient_stock, actual invalid_amount
PASS F stock
PASS G result
PASS G stock
Checks: 17, failed: 2
```

Exit code: 1. It comes from two real `FAIL` lines: `main` returns 1 because `failed` is greater than 0.

**The fix:** restore `return IssueResult::insufficient_stock;`. The program is again the one from section 6. The same tests, with the same expected results, print `PASS` 17 times and `Checks: 17, failed: 0`, and the exit code is 0. You don't change the expected results: it's the function that must meet the contract, not the tests that must fit the function.

</details>

### The other way round: the right result, the wrong state

Only read this variant and predict its effect. Running it is optional. Someone decides that since the goods are short anyway, the warehouse will issue what it has, and adds one line to the second clause:

<!-- fragment -->
```cpp
if (requested > stock) {
    stock = 0;
    return IssueResult::insufficient_stock;
}
```

**Predict:** which checks from section 6 will fail? Will case F notice it?

<details>
<summary>The answer and a program that checks it</summary>

- **E:** the result is right, `insufficient_stock`, so the check of the result passes. The stock drops from 7 to 0, though, so the check of the stock gives `FAIL`.
- **F:** the stock is already 0, so `stock = 0;` changes nothing and both checks pass. Only a case with something in stock before the refusal catches this bug.
- **Conclusion:** the function reports a refusal and changes the data anyway, so it breaks the contract. A right named result doesn't guarantee a right state. A test that checked only the result would pass completely.

<!-- example: issue_tests_changed_stock exit=1 -->
```cpp
#include <iostream>
#include <string>

enum class IssueResult {
    issued,
    invalid_amount,
    insufficient_stock
};

IssueResult issue_units(int requested, int& stock) {
    if (requested <= 0) {
        return IssueResult::invalid_amount;
    }

    if (requested > stock) {
        stock = 0;
        return IssueResult::insufficient_stock;
    }

    stock -= requested;
    return IssueResult::issued;
}

std::string issue_result_text(IssueResult result) {
    switch (result) {
        case IssueResult::issued:
            return "issued";
        case IssueResult::invalid_amount:
            return "invalid_amount";
        case IssueResult::insufficient_stock:
            return "insufficient_stock";
    }

    return "unknown";
}

void check_issue_result(const std::string& name, IssueResult expected, IssueResult actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << issue_result_text(expected) << ", actual " << issue_result_text(actual) << "\n";
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

    check_text("issue_result_text(issued)", "issued", issue_result_text(IssueResult::issued), checks, failed);
    check_text("issue_result_text(invalid_amount)", "invalid_amount", issue_result_text(IssueResult::invalid_amount), checks, failed);
    check_text("issue_result_text(insufficient_stock)", "insufficient_stock", issue_result_text(IssueResult::insufficient_stock), checks, failed);

    int stock_a{7};
    const IssueResult result_a{issue_units(3, stock_a)};
    check_issue_result("A result", IssueResult::issued, result_a, checks, failed);
    check_int("A stock", 4, stock_a, checks, failed);

    int stock_b{7};
    const IssueResult result_b{issue_units(7, stock_b)};
    check_issue_result("B result", IssueResult::issued, result_b, checks, failed);
    check_int("B stock", 0, stock_b, checks, failed);

    int stock_c{7};
    const IssueResult result_c{issue_units(0, stock_c)};
    check_issue_result("C result", IssueResult::invalid_amount, result_c, checks, failed);
    check_int("C stock", 7, stock_c, checks, failed);

    int stock_d{7};
    const IssueResult result_d{issue_units(-2, stock_d)};
    check_issue_result("D result", IssueResult::invalid_amount, result_d, checks, failed);
    check_int("D stock", 7, stock_d, checks, failed);

    int stock_e{7};
    const IssueResult result_e{issue_units(8, stock_e)};
    check_issue_result("E result", IssueResult::insufficient_stock, result_e, checks, failed);
    check_int("E stock", 7, stock_e, checks, failed);

    int stock_f{0};
    const IssueResult result_f{issue_units(1, stock_f)};
    check_issue_result("F result", IssueResult::insufficient_stock, result_f, checks, failed);
    check_int("F stock", 0, stock_f, checks, failed);

    int stock_g{7};
    const IssueResult result_g{issue_units(1, stock_g)};
    check_issue_result("G result", IssueResult::issued, result_g, checks, failed);
    check_int("G stock", 6, stock_g, checks, failed);

    std::cout << "Checks: " << checks << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

<!-- output: issue_tests_changed_stock -->
```text
PASS issue_result_text(issued)
PASS issue_result_text(invalid_amount)
PASS issue_result_text(insufficient_stock)
PASS A result
PASS A stock
PASS B result
PASS B stock
PASS C result
PASS C stock
PASS D result
PASS D stock
PASS E result
FAIL E stock: expected 7, actual 0
PASS F result
PASS F stock
PASS G result
PASS G stock
Checks: 17, failed: 1
```

Exit code: 1.

</details>

## 8. Mission: topping up a card

A transport card has a balance in points, not money, and can be active or blocked. A machine tops up the card, but not always: the card must be active, the amount must be allowed, and the balance mustn't go over a limit. When the machine refuses, it shows the reason. Your task is a top-up function that returns a named result, and a test program that checks this result and the card after the call.

It's a different problem from issuing goods. The data that change are a record with two fields, there are three reasons for refusal, and several of them can apply at once.

**The types and the signature:**

<!-- fragment -->
```cpp
enum class TopUpResult {
    added,
    inactive_card,
    invalid_amount,
    limit_exceeded
};

struct Card {
    int balance;
    bool active;
};

TopUpResult top_up(Card& card, int amount);
```

**The contract of `top_up`:**

- **Assumption:** on entry, `card.balance` is from 0 to 100. The function doesn't check it.
- A valid top-up amount is from 1 to 50.
- The balance after a top-up mustn't go over 100. A balance of exactly 100 is allowed.
- When the card is inactive, that is `card.active` is `false`: the result is `TopUpResult::inactive_card`.
- When the card is active but the amount is less than 1 or more than 50: the result is `TopUpResult::invalid_amount`.
- When the card is active and the amount valid, but the balance after the top-up would be more than 100: the result is `TopUpResult::limit_exceeded`.
- In every other case the balance grows by `amount`, and the result is `TopUpResult::added`.
- **No refusal changes the card:** neither the balance nor the field `active`. The field `active` doesn't change on success either.

**The refusal precedence.** When several reasons for refusal apply at once, the result is the first of them in this list:

1. `inactive_card`;
2. `invalid_amount`;
3. `limit_exceeded`.

So for an inactive card and an amount of 0, the result is `inactive_card`, not `invalid_amount`. It's a design decision for our machine, not a rule of every payment system: another program could choose another order. What matters is that the contract states it, and the function and the tests follow it. Checking the data before an operation changes anything is **validation**, and in this mission the validation order is part of the contract.

**The format of the case table**, with one case as an example:

| Case | Balance before | Active | Amount | Result | Balance after | Active after |
|---|---:|---|---:|---|---:|---|
| A | 40 | `true` | 20 | `added` | 60 | `true` |

**Rules:**

- `top_up` gets the card by `&` and the amount by value. It checks all the conditions before it changes the card, and prints nothing.
- Each check appears in the function once.
- The test program compares the result as a `TopUpResult` value, not as text. The text of the result is only for the `FAIL` lines. It comes from the function `std::string top_up_result_text(TopUpResult result)`, written with a `switch` with a `case` label for each of the four values and the fallback `"unknown"`. Check it for each value, like `issue_result_text` in section 6. The texts are the names of the values: `"added"`, `"inactive_card"`, `"invalid_amount"`, `"limit_exceeded"`.
- Each case has its own `Card` object with the starting state from your table.
- For each case you check three things: the result, the balance after the call and the field `active` after the call. For the result, write a check function for `TopUpResult`, like `check_issue_result`. You can copy `check_int`, `check_bool` and `check_text` from lesson 13.3.

In `cpp-workspace`, create a folder `card_top_up`, copy `main.cpp` and `CMakeLists.txt` from the original `lesson_05_first_program` into it, and open it in CLion. Write everything in the one file `main.cpp`. Leave `CMakeLists.txt` unchanged.

**The order of work:**

1. **The case table first.** Before you write any code, prepare a table in the format above. Work out the expected results from the contract. The table must contain at least:
   - a typical top-up;
   - a top-up after which the balance is exactly 100;
   - a refusal because of the limit;
   - a refusal because of an invalid amount;
   - a refusal because of an inactive card;
   - a case in which two reasons for refusal apply at once;
   - the balance and `active` after the call for each case.

   Under the table, write a prediction: which checks will fail, and what will they print after `actual`, when the function starts refusing a top-up also when the balance after it would be exactly 100?
2. Define `TopUpResult` and `Card`, and write `top_up` and `top_up_result_text`.
3. Write the test program: the check functions, the checks from your table, and at the end the summary and the exit code as in section 6.
4. **This is the fourth required run:** run the test program with the correct function. Every check should print `PASS`, and the exit code should be 0.
5. **A deliberate bug.** In the limit condition in `top_up`, change `>` to `>=`, so that the function refuses a top-up also when the balance after it would be exactly 100. If your condition has another form, make a bug with the same meaning. Don't change the tests or the expected results. **This is the fifth required run:** run the tests, note the `FAIL` lines, the summary and the exit code, and compare them with your prediction from step 1. Then restore the correct condition and run the same tests again.

You don't have to run any other versions. If you like, also check what happens when you swap the check of the card and the check of the amount in `top_up`: which of your cases will notice? It's discussed in the example solution.

### Success criteria

- [ ] The program builds as C++20, and `CMakeLists.txt` is the one from lesson 0.5.
- [ ] `TopUpResult` has the four values from the contract, and `Card` has two fields: `balance` and `active`.
- [ ] `top_up` gets the card by `&` and the amount by value, returns `TopUpResult` and prints nothing.
- [ ] All the checks come before the balance changes, each appears once, and their order matches the refusal precedence.
- [ ] A refusal changes neither the balance nor `active`. A top-up increases the balance by exactly the amount and doesn't change `active`.
- [ ] `top_up_result_text` uses a `switch` with a `case` label for each of the four values, and the test program checks it for each of them.
- [ ] The case table was made before the code, and the expected results follow from the contract. The table has all the required kinds of case, including a case with two reasons for refusal at once.
- [ ] Each case has its own `Card` object, and the program checks its result, balance and `active`.
- [ ] The program compares the result as a `TopUpResult` value, not as text.
- [ ] With the correct function every check passes, and the exit code is 0.
- [ ] With the bug at the limit's boundary, `FAIL` is printed only by the checks of the result and the balance in the cases where the balance was to be exactly 100, and the exit code is 1. The output matches your prediction, or you can explain the difference.
- [ ] After the correct condition is restored, the same tests, unchanged, pass again with exit code 0.
- [ ] You can explain why the validation order is part of the contract of `top_up`, and which case in your table checks it.

When the output matches, you can save the project in Git, as in lesson 1.5: `main.cpp` and `CMakeLists.txt`, without the build folder.

<details>
<summary>Hint 1: the kinds of result</summary>

Which `TopUpResult` values describe every possible ending of the operation? For each of them, find the rule in the contract that gives it, and write at least one case with that result. Does each of the four values appear as an expected result in your table?

</details>

<details>
<summary>Hint 2: an unchanged card</summary>

At what point is it safe to change the balance? Which data must be checked before that change? How much room is left on the card up to the limit of 100, and how do you compare the amount with it? After every refusal the card must look exactly as it did before the call.

</details>

<details>
<summary>Hint 3: the refusal precedence</summary>

What should be returned if the card is inactive and the amount is invalid at the same time? Which check must then come higher in the function? Which case in your table would give another result if those two checks were swapped?

</details>

<details>
<summary>The full list of check cases: open after preparing your own table</summary>

In every case the field `active` after the call has the same value as before it.

| Case | Balance before | Active | Amount | Result | Balance after | What it checks |
|---|---:|---|---:|---|---:|---|
| A | 40 | `true` | 20 | `added` | 60 | a typical top-up |
| B | 80 | `true` | 20 | `added` | 100 | a balance exactly at the limit |
| C | 100 | `true` | 1 | `limit_exceeded` | 100 | a full card, the smallest amount |
| D | 80 | `true` | 21 | `limit_exceeded` | 80 | the limit exceeded by 1 |
| E | 50 | `true` | 0 | `invalid_amount` | 50 | an amount 1 too small |
| F | 50 | `true` | -1 | `invalid_amount` | 50 | a negative amount |
| G | 50 | `true` | 51 | `invalid_amount` | 50 | an amount 1 too large |
| H | 30 | `false` | 10 | `inactive_card` | 30 | an inactive card, a valid amount |
| I | 0 | `true` | 50 | `added` | 50 | an empty card, the largest amount |
| J | 100 | `false` | 0 | `inactive_card` | 100 | two reasons at once: an inactive card and an invalid amount |

**Two reasons for refusal at once** apply in two cases, and in both the refusal precedence decides the result. In J the card is inactive and the amount invalid: the result is `inactive_card`. In G the amount 51 is invalid, and the balance after the top-up would also go over the limit: the result is `invalid_amount`. In the other refusals one reason applies, so their result doesn't depend on the order of the checks.

Your table doesn't have to contain all ten cases. It must contain every kind listed in step 1 of the mission. The reference program in the example solution checks eight of them: all except C and F, which are of the same kinds as D and E.

</details>

An example solution is in [Example solutions](#example-solutions).

## 9. When something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| An error with `value of type 'TopUpResult' is not contextually convertible to 'bool'` | The call to `top_up` stands in an `if` condition, like a function returning `bool` (section 4). | Keep the result in a variable and compare it with a `TopUpResult` value, or handle it with a `switch`. |
| An error with `invalid operands to binary expression` at `==` | The result is compared with text in quotes (section 4). | Compare it with a value, for example `TopUpResult::added`. |
| A `FAIL` of the result with `expected inactive_card, actual invalid_amount` for an inactive card with an invalid amount | The function checks the amount before the card. | Put the checks in the order of the refusal precedence. |
| A `FAIL` of the result with `expected invalid_amount, actual limit_exceeded` for an amount that's too large | The function checks the limit before the amount. | Check the limit only after the amount, following the refusal precedence. |
| `FAIL` of the result and of the balance only in the case where the balance was to be exactly 100 | The limit condition also refuses a balance equal to 100, for example `>=` instead of `>`. | Refuse only a balance that would be more than 100. |
| A refusal result is right, but the check of the balance gives `FAIL` | The function changes the balance before a check or on a refusal path (section 7). | All the checks first, then one change of the balance just before `return TopUpResult::added;`. |
| The result matches the table, but the balance is off in later cases | Several cases use one `Card` object, so each starts from the balance the previous one left. | Create a separate `Card` object for each case. |
| A `FAIL` with the same text after `expected` and after `actual`, for example `expected added, actual added` | The results differ, but `top_up_result_text` returns the same text for two values. | Fix the text in `top_up_result_text`. Its own checks should catch it too. |
| A warning with `enumeration value '…' not handled in switch` | A label for one of the values is missing in `top_up_result_text` (lesson 14.2). | Add the label with the right text. |
| A warning with `non-void function does not return a value in all control paths` | `return TopUpResult::added;` is missing after the change of the balance. Calling such a function has undefined behaviour (lesson 5.4). | Add `return TopUpResult::added;` after the change of the balance. |

## 10. Explain

Answer in your own words, preferably in writing. Only then compare with the example answers.

1. How does a `bool` result differ from a named result? When does `bool` stop being enough?
2. Why does an `enum class` describe several reasons for refusal better than text or a number?
3. What does the parameter `int& stock` mean? Does returning a named result change the data by itself?
4. Why must the data stay exactly as they were before the call after a refusal?
5. Does a right named result guarantee a right state of the data? Give an example from this lesson.
6. Why does the test compare with the exact result from the contract, and why isn't it enough to check that the result isn't `issued`?
7. What does a `FAIL` of the check of the balance mean when the check of the result gives `PASS`?
8. Why does swapping the two refusal checks in `issue_units` not change the results, while swapping the check of the card and the check of the amount in `top_up` does?
9. Why is the validation order part of the contract of `top_up`? Which case checks it, and why aren't cases with one reason for refusal enough?
10. Why does the calling code handle each result separately, for example with a `switch` statement?
11. After a bug is introduced, a test gives `FAIL`. May you change the expected result to get `PASS` again?

<details>
<summary>Example answers</summary>

1. A `bool` has two values, so it only answers whether the operation succeeded. A named result has as many values as there are different endings of the operation, and names each of them. `bool` stops being enough when the caller must react differently to different reasons for refusal, for example say whether the amount was wrong or the goods ran short.
2. Because the set of values is closed and known to the compiler. A typo in a value's name is a compile error (lesson 14.1), the result can't be mixed up with text or a number, and a `switch` can handle each value separately. The text `"insuficient"` with a typo or the number `2` doesn't say what it means, and the compiler can't check it.
3. That the function gets access to the caller's variable, not a copy of it, so it can change that variable (lesson 9.1). Returning the result changes nothing: `return` only passes the `IssueResult` value. The stock is changed by a separate statement, `stock -= requested;`, which runs only on success.
4. Because a refusal result means "the operation didn't happen". The caller then assumes the data are as they were before the call and, for example, reports the amount available in stock. If a refusal changed the data, that report and later operations would be wrong.
5. No. In the variant with `stock = 0;` the function returns the right `insufficient_stock`, but the stock drops from 7 to 0. That's why you check the result and the state separately.
6. Because `invalid_amount` and `insufficient_stock` are different results, and the contract says which one must come back. A check "not `issued`" passes for both refusals, so it wouldn't catch the mistake from section 7.
7. That the function ended with the right result but changed the data against the contract: it refused and changed the balance anyway, or changed it by the wrong amount on success. It's a bug in the effect, not in the result.
8. In `issue_units` the two reasons for refusal never apply at once: with `stock` at least 0, a request of 0 or less isn't larger than the stock. In `top_up` a card can be inactive and have an invalid amount at the same time, and then the check that comes higher decides the result.
9. Because when several reasons apply at once, the contract must say which result comes back, and the function gives it only with a particular order of checks. A case with two reasons at once checks it, for example an inactive card and an amount of 0. Cases with one reason give the same result with any order of checks, so they won't catch a swap.
10. Because each result needs a different reaction: on success the program shows the new stock, for an invalid amount it says what is allowed, and for missing goods it says how many are available. A `switch` with a label for each value shows in one place that no result was left out.
11. No. The expected result comes from the contract, not from what the function does. A `FAIL` means the function doesn't meet the contract, so you fix the function. Changing the expectations would hide the bug, and the test would stop checking anything.

</details>

## Summary

- `bool` only says whether an operation succeeded. When a refusal has several reasons and the caller must react to each differently, the function returns a **named result**: a value of an `enum class` type that names every possible ending of the operation.
- **The result and the effect are two different things.** The result comes back through `return`. The effect is a change to the data passed by `&`, made only on success. After a refusal the data are exactly as they were before the call.
- The calling code keeps the result in a variable and handles each value separately, for example with a `switch` statement. The result isn't compared with text or used as a `bool`.
- A test checks the named result and the state of the data after the call separately, and compares the result with the exact value from the contract. You test the function that turns the result into text too.
- When several reasons for refusal can apply at once, the contract sets the **refusal precedence**, and the function checks the conditions in that order. Only a case in which two reasons apply at once catches a wrong order.
- After a `FAIL` you fix the function, not the expected results, and run the same tests again.

## What's next

In this lesson a function that changes data says with a named result why it refused. In [lesson 14.4: Try again: reading that recovers the stream](lesson_04_reading_that_recovers_the_stream.en.md) the same idea goes into a reading function: it will tell a valid entry from an invalid one, and after an invalid entry it will get the input ready for another try.

---

## Example solutions

Look here **after your own attempt**. Your names of checks, names of variables, choice of cases and order of checks in the test program may differ, as long as they meet the contract and the checklist.

<details>
<summary>Section 8: the mission, topping up a card</summary>

**The order of the checks in `top_up`** follows from the refusal precedence: the card first, then the amount, then the limit. The change of the balance comes last, after all the checks. The function checks the limit only after the amount, because by then it's known that the amount is from 1 to 50. That's why the result for an amount of 51 with a balance of 50 is `invalid_amount`, although the balance would also go over the limit. The condition `amount > 100 - card.balance` compares the amount with the room left on the card up to the limit: with a balance of 80 there are 20 left, so an amount of 20 still fits, and 21 doesn't.

**The cases:** the reference program checks eight cases from the full list, A, B, D, E, G, H, I and J, with three checks per case, 24 in all. Add 4 checks of the text, 28 altogether. Cases C and F are of the same kinds as D and E.

**The prediction:** with the bug `>=` instead of `>`, the function refuses a top-up after which the balance would be exactly 100. Of the eight cases, that affects only B, a balance of 80 and an amount of 20. `FAIL` will be printed by the check of the result, with `limit_exceeded` after `actual`, and by the check of the balance, with 80 after `actual`, because a refusal doesn't change the balance. The other 26 checks will pass, and the exit code will be 1.

**`main.cpp`:**

<!-- example: top_up_tests -->
```cpp
#include <iostream>
#include <string>

enum class TopUpResult {
    added,
    inactive_card,
    invalid_amount,
    limit_exceeded
};

struct Card {
    int balance;
    bool active;
};

TopUpResult top_up(Card& card, int amount) {
    if (!card.active) {
        return TopUpResult::inactive_card;
    }

    if (amount < 1 || amount > 50) {
        return TopUpResult::invalid_amount;
    }

    if (amount > 100 - card.balance) {
        return TopUpResult::limit_exceeded;
    }

    card.balance += amount;
    return TopUpResult::added;
}

std::string top_up_result_text(TopUpResult result) {
    switch (result) {
        case TopUpResult::added:
            return "added";
        case TopUpResult::inactive_card:
            return "inactive_card";
        case TopUpResult::invalid_amount:
            return "invalid_amount";
        case TopUpResult::limit_exceeded:
            return "limit_exceeded";
    }

    return "unknown";
}

std::string bool_text(bool value) {
    if (value) {
        return "true";
    }

    return "false";
}

void check_top_up_result(const std::string& name, TopUpResult expected, TopUpResult actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << top_up_result_text(expected) << ", actual " << top_up_result_text(actual) << "\n";
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

int main() {
    int checks{0};
    int failed{0};

    check_text("top_up_result_text(added)", "added", top_up_result_text(TopUpResult::added), checks, failed);
    check_text("top_up_result_text(inactive_card)", "inactive_card", top_up_result_text(TopUpResult::inactive_card), checks, failed);
    check_text("top_up_result_text(invalid_amount)", "invalid_amount", top_up_result_text(TopUpResult::invalid_amount), checks, failed);
    check_text("top_up_result_text(limit_exceeded)", "limit_exceeded", top_up_result_text(TopUpResult::limit_exceeded), checks, failed);

    Card card_a{40, true};
    const TopUpResult result_a{top_up(card_a, 20)};
    check_top_up_result("A result", TopUpResult::added, result_a, checks, failed);
    check_int("A balance", 60, card_a.balance, checks, failed);
    check_bool("A active", true, card_a.active, checks, failed);

    Card card_b{80, true};
    const TopUpResult result_b{top_up(card_b, 20)};
    check_top_up_result("B result", TopUpResult::added, result_b, checks, failed);
    check_int("B balance", 100, card_b.balance, checks, failed);
    check_bool("B active", true, card_b.active, checks, failed);

    Card card_d{80, true};
    const TopUpResult result_d{top_up(card_d, 21)};
    check_top_up_result("D result", TopUpResult::limit_exceeded, result_d, checks, failed);
    check_int("D balance", 80, card_d.balance, checks, failed);
    check_bool("D active", true, card_d.active, checks, failed);

    Card card_e{50, true};
    const TopUpResult result_e{top_up(card_e, 0)};
    check_top_up_result("E result", TopUpResult::invalid_amount, result_e, checks, failed);
    check_int("E balance", 50, card_e.balance, checks, failed);
    check_bool("E active", true, card_e.active, checks, failed);

    Card card_g{50, true};
    const TopUpResult result_g{top_up(card_g, 51)};
    check_top_up_result("G result", TopUpResult::invalid_amount, result_g, checks, failed);
    check_int("G balance", 50, card_g.balance, checks, failed);
    check_bool("G active", true, card_g.active, checks, failed);

    Card card_h{30, false};
    const TopUpResult result_h{top_up(card_h, 10)};
    check_top_up_result("H result", TopUpResult::inactive_card, result_h, checks, failed);
    check_int("H balance", 30, card_h.balance, checks, failed);
    check_bool("H active", false, card_h.active, checks, failed);

    Card card_i{0, true};
    const TopUpResult result_i{top_up(card_i, 50)};
    check_top_up_result("I result", TopUpResult::added, result_i, checks, failed);
    check_int("I balance", 50, card_i.balance, checks, failed);
    check_bool("I active", true, card_i.active, checks, failed);

    Card card_j{100, false};
    const TopUpResult result_j{top_up(card_j, 0)};
    check_top_up_result("J result", TopUpResult::inactive_card, result_j, checks, failed);
    check_int("J balance", 100, card_j.balance, checks, failed);
    check_bool("J active", false, card_j.active, checks, failed);

    std::cout << "Checks: " << checks << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

<!-- output: top_up_tests -->
```text
PASS top_up_result_text(added)
PASS top_up_result_text(inactive_card)
PASS top_up_result_text(invalid_amount)
PASS top_up_result_text(limit_exceeded)
PASS A result
PASS A balance
PASS A active
PASS B result
PASS B balance
PASS B active
PASS D result
PASS D balance
PASS D active
PASS E result
PASS E balance
PASS E active
PASS G result
PASS G balance
PASS G active
PASS H result
PASS H balance
PASS H active
PASS I result
PASS I balance
PASS I active
PASS J result
PASS J balance
PASS J active
Checks: 28, failed: 0
```

Exit code: 0.

**The bug at the limit's boundary.** `>` changed to `>=` in the limit condition, with no other change:

<!-- example: top_up_tests_limit exit=1 -->
```cpp
#include <iostream>
#include <string>

enum class TopUpResult {
    added,
    inactive_card,
    invalid_amount,
    limit_exceeded
};

struct Card {
    int balance;
    bool active;
};

TopUpResult top_up(Card& card, int amount) {
    if (!card.active) {
        return TopUpResult::inactive_card;
    }

    if (amount < 1 || amount > 50) {
        return TopUpResult::invalid_amount;
    }

    if (amount >= 100 - card.balance) {
        return TopUpResult::limit_exceeded;
    }

    card.balance += amount;
    return TopUpResult::added;
}

std::string top_up_result_text(TopUpResult result) {
    switch (result) {
        case TopUpResult::added:
            return "added";
        case TopUpResult::inactive_card:
            return "inactive_card";
        case TopUpResult::invalid_amount:
            return "invalid_amount";
        case TopUpResult::limit_exceeded:
            return "limit_exceeded";
    }

    return "unknown";
}

std::string bool_text(bool value) {
    if (value) {
        return "true";
    }

    return "false";
}

void check_top_up_result(const std::string& name, TopUpResult expected, TopUpResult actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << top_up_result_text(expected) << ", actual " << top_up_result_text(actual) << "\n";
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

int main() {
    int checks{0};
    int failed{0};

    check_text("top_up_result_text(added)", "added", top_up_result_text(TopUpResult::added), checks, failed);
    check_text("top_up_result_text(inactive_card)", "inactive_card", top_up_result_text(TopUpResult::inactive_card), checks, failed);
    check_text("top_up_result_text(invalid_amount)", "invalid_amount", top_up_result_text(TopUpResult::invalid_amount), checks, failed);
    check_text("top_up_result_text(limit_exceeded)", "limit_exceeded", top_up_result_text(TopUpResult::limit_exceeded), checks, failed);

    Card card_a{40, true};
    const TopUpResult result_a{top_up(card_a, 20)};
    check_top_up_result("A result", TopUpResult::added, result_a, checks, failed);
    check_int("A balance", 60, card_a.balance, checks, failed);
    check_bool("A active", true, card_a.active, checks, failed);

    Card card_b{80, true};
    const TopUpResult result_b{top_up(card_b, 20)};
    check_top_up_result("B result", TopUpResult::added, result_b, checks, failed);
    check_int("B balance", 100, card_b.balance, checks, failed);
    check_bool("B active", true, card_b.active, checks, failed);

    Card card_d{80, true};
    const TopUpResult result_d{top_up(card_d, 21)};
    check_top_up_result("D result", TopUpResult::limit_exceeded, result_d, checks, failed);
    check_int("D balance", 80, card_d.balance, checks, failed);
    check_bool("D active", true, card_d.active, checks, failed);

    Card card_e{50, true};
    const TopUpResult result_e{top_up(card_e, 0)};
    check_top_up_result("E result", TopUpResult::invalid_amount, result_e, checks, failed);
    check_int("E balance", 50, card_e.balance, checks, failed);
    check_bool("E active", true, card_e.active, checks, failed);

    Card card_g{50, true};
    const TopUpResult result_g{top_up(card_g, 51)};
    check_top_up_result("G result", TopUpResult::invalid_amount, result_g, checks, failed);
    check_int("G balance", 50, card_g.balance, checks, failed);
    check_bool("G active", true, card_g.active, checks, failed);

    Card card_h{30, false};
    const TopUpResult result_h{top_up(card_h, 10)};
    check_top_up_result("H result", TopUpResult::inactive_card, result_h, checks, failed);
    check_int("H balance", 30, card_h.balance, checks, failed);
    check_bool("H active", false, card_h.active, checks, failed);

    Card card_i{0, true};
    const TopUpResult result_i{top_up(card_i, 50)};
    check_top_up_result("I result", TopUpResult::added, result_i, checks, failed);
    check_int("I balance", 50, card_i.balance, checks, failed);
    check_bool("I active", true, card_i.active, checks, failed);

    Card card_j{100, false};
    const TopUpResult result_j{top_up(card_j, 0)};
    check_top_up_result("J result", TopUpResult::inactive_card, result_j, checks, failed);
    check_int("J balance", 100, card_j.balance, checks, failed);
    check_bool("J active", false, card_j.active, checks, failed);

    std::cout << "Checks: " << checks << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

<!-- output: top_up_tests_limit -->
```text
PASS top_up_result_text(added)
PASS top_up_result_text(inactive_card)
PASS top_up_result_text(invalid_amount)
PASS top_up_result_text(limit_exceeded)
PASS A result
PASS A balance
PASS A active
FAIL B result: expected added, actual limit_exceeded
FAIL B balance: expected 100, actual 80
PASS B active
PASS D result
PASS D balance
PASS D active
PASS E result
PASS E balance
PASS E active
PASS G result
PASS G balance
PASS G active
PASS H result
PASS H balance
PASS H active
PASS I result
PASS I balance
PASS I active
PASS J result
PASS J balance
PASS J active
Checks: 28, failed: 2
```

Exit code: 1.

| Case | Expected result | Actual result | Expected balance | Actual balance | Checks with `FAIL` |
|---|---|---|---:|---:|---|
| B | `added` | `limit_exceeded` | 100 | 80 | the result and the balance |
| D | `limit_exceeded` | `limit_exceeded` | 80 | 80 | none |
| A, I | `added` | `added` | as in the table | as in the table | none |
| E, G, H, J | as in the table | unchanged | as in the table | as in the table | none |

- **Only B catches it,** the only case in which the balance after the top-up is exactly 100. In D the balance would go over the limit, so the refusal is right with both conditions. Without a case at the boundary the bug would go unnoticed (lesson 13.2).
- **Two `FAIL`s from one case:** the result is wrong, and the balance stays 80, because the function rightly doesn't change the card on a refusal. The field `active` is right.
- **Exit code 1** comes from two real `FAIL` lines.

**After the fix:** with `>` restored, the program is again the first version. The same 28 checks print `PASS` and `Checks: 28, failed: 0`, and the exit code is 0. The expected results didn't change.

**An extra diagnostic: a swapped validation order.** The function checks the amount before the card. The rest of the function and the program is unchanged:

<!-- example: top_up_tests_order exit=1 -->
```cpp
#include <iostream>
#include <string>

enum class TopUpResult {
    added,
    inactive_card,
    invalid_amount,
    limit_exceeded
};

struct Card {
    int balance;
    bool active;
};

TopUpResult top_up(Card& card, int amount) {
    if (amount < 1 || amount > 50) {
        return TopUpResult::invalid_amount;
    }

    if (!card.active) {
        return TopUpResult::inactive_card;
    }

    if (amount > 100 - card.balance) {
        return TopUpResult::limit_exceeded;
    }

    card.balance += amount;
    return TopUpResult::added;
}

std::string top_up_result_text(TopUpResult result) {
    switch (result) {
        case TopUpResult::added:
            return "added";
        case TopUpResult::inactive_card:
            return "inactive_card";
        case TopUpResult::invalid_amount:
            return "invalid_amount";
        case TopUpResult::limit_exceeded:
            return "limit_exceeded";
    }

    return "unknown";
}

std::string bool_text(bool value) {
    if (value) {
        return "true";
    }

    return "false";
}

void check_top_up_result(const std::string& name, TopUpResult expected, TopUpResult actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << top_up_result_text(expected) << ", actual " << top_up_result_text(actual) << "\n";
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

int main() {
    int checks{0};
    int failed{0};

    check_text("top_up_result_text(added)", "added", top_up_result_text(TopUpResult::added), checks, failed);
    check_text("top_up_result_text(inactive_card)", "inactive_card", top_up_result_text(TopUpResult::inactive_card), checks, failed);
    check_text("top_up_result_text(invalid_amount)", "invalid_amount", top_up_result_text(TopUpResult::invalid_amount), checks, failed);
    check_text("top_up_result_text(limit_exceeded)", "limit_exceeded", top_up_result_text(TopUpResult::limit_exceeded), checks, failed);

    Card card_a{40, true};
    const TopUpResult result_a{top_up(card_a, 20)};
    check_top_up_result("A result", TopUpResult::added, result_a, checks, failed);
    check_int("A balance", 60, card_a.balance, checks, failed);
    check_bool("A active", true, card_a.active, checks, failed);

    Card card_b{80, true};
    const TopUpResult result_b{top_up(card_b, 20)};
    check_top_up_result("B result", TopUpResult::added, result_b, checks, failed);
    check_int("B balance", 100, card_b.balance, checks, failed);
    check_bool("B active", true, card_b.active, checks, failed);

    Card card_d{80, true};
    const TopUpResult result_d{top_up(card_d, 21)};
    check_top_up_result("D result", TopUpResult::limit_exceeded, result_d, checks, failed);
    check_int("D balance", 80, card_d.balance, checks, failed);
    check_bool("D active", true, card_d.active, checks, failed);

    Card card_e{50, true};
    const TopUpResult result_e{top_up(card_e, 0)};
    check_top_up_result("E result", TopUpResult::invalid_amount, result_e, checks, failed);
    check_int("E balance", 50, card_e.balance, checks, failed);
    check_bool("E active", true, card_e.active, checks, failed);

    Card card_g{50, true};
    const TopUpResult result_g{top_up(card_g, 51)};
    check_top_up_result("G result", TopUpResult::invalid_amount, result_g, checks, failed);
    check_int("G balance", 50, card_g.balance, checks, failed);
    check_bool("G active", true, card_g.active, checks, failed);

    Card card_h{30, false};
    const TopUpResult result_h{top_up(card_h, 10)};
    check_top_up_result("H result", TopUpResult::inactive_card, result_h, checks, failed);
    check_int("H balance", 30, card_h.balance, checks, failed);
    check_bool("H active", false, card_h.active, checks, failed);

    Card card_i{0, true};
    const TopUpResult result_i{top_up(card_i, 50)};
    check_top_up_result("I result", TopUpResult::added, result_i, checks, failed);
    check_int("I balance", 50, card_i.balance, checks, failed);
    check_bool("I active", true, card_i.active, checks, failed);

    Card card_j{100, false};
    const TopUpResult result_j{top_up(card_j, 0)};
    check_top_up_result("J result", TopUpResult::inactive_card, result_j, checks, failed);
    check_int("J balance", 100, card_j.balance, checks, failed);
    check_bool("J active", false, card_j.active, checks, failed);

    std::cout << "Checks: " << checks << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

<!-- output: top_up_tests_order -->
```text
PASS top_up_result_text(added)
PASS top_up_result_text(inactive_card)
PASS top_up_result_text(invalid_amount)
PASS top_up_result_text(limit_exceeded)
PASS A result
PASS A balance
PASS A active
PASS B result
PASS B balance
PASS B active
PASS D result
PASS D balance
PASS D active
PASS E result
PASS E balance
PASS E active
PASS G result
PASS G balance
PASS G active
PASS H result
PASS H balance
PASS H active
PASS I result
PASS I balance
PASS I active
FAIL J result: expected inactive_card, actual invalid_amount
PASS J balance
PASS J active
Checks: 28, failed: 1
```

Exit code: 1.

- **Only J catches it:** an inactive card and an amount of 0. The contract gives precedence to `inactive_card`, and the function reaches the check of the amount first and returns `invalid_amount`. The balance and `active` are right, because the refusal changes nothing.
- **Cases in which the card and the amount aren't wrong at once don't catch it.** H is an inactive card with a valid amount: the check of the amount lets it through, and the check of the card gives `inactive_card`, as in the contract. E and G are invalid amounts on an active card: with an active card the result `invalid_amount` is the same in both orders. Each rule on its own works, and the bug is in their order.
- **G checks another pair of reasons:** the amount 51 is invalid, and the balance would go over the limit. This case doesn't catch a swap of the card check and the amount check, but it would catch a swap of the amount check and the limit check: the function would then return `limit_exceeded`.
- **If your case with two reasons is another pair,** for example an inactive card with a full balance and an amount of 1, the swap of the card and the amount doesn't affect it, because the amount 1 is valid. Such a case catches a swap of the card check and the limit check instead. Each pair of reasons that can apply at once needs its own case.

**Self-assessment.** Compare your work with the checklist in section 8. In particular, check:
- whether your table was made before the code and has all the required kinds of case, including a balance of exactly 100 and two reasons for refusal at once;
- whether each case has its own `Card` object, and whether you check its result, balance and `active`;
- whether you compare the result as a `TopUpResult` value, with the text used only for the `FAIL` line;
- whether your prediction from step 1 matched the result of step 5, and if it didn't, whether you can explain the difference;
- whether you can point to a case that would catch a swap of the card check and the amount check.

If the answer to any of these is "no", go back to that part of the lesson before you move on.

</details>

**Previous lesson:** [Lesson 14.2: Handling every state with `switch`](lesson_02_handling_every_state_with_switch.en.md) · **Next lesson:** [Lesson 14.4: Try again: reading that recovers the stream](lesson_04_reading_that_recovers_the_stream.en.md) · [Course overview](../../README.en.md)

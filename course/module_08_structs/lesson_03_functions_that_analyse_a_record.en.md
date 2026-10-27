# Lesson 8.3: Functions that analyse a record

[Polski](lesson_03_functions_that_analyse_a_record.md) · **English** · [Course overview](../../README.en.md)

> **Module 8, lesson 3** · about 65–80 minutes
> **You need:** your `cpp-workspace` folder and the original `lesson_05_first_program` project, as before. You won't need the debugger in this lesson.
> **Pilot version.** The programs in this lesson are checked automatically on Windows, Ubuntu and macOS. None of them asks for data: every value is written in the code. Only the check program in the solutions part reads data from the input.

## Before you start

This lesson assumes that you:

- define a struct, create its objects in `{}` and read fields with `.` (lesson 8.1), and create a copy of a record with `Book before{current};` (lesson 8.2);
- write functions that return an `int` or a `bool` result, and leave the printing to `main` (lessons 5.3 and 5.5);
- know that a function can call another function whose definition stands higher up in the file (lessons 5.5 and 5.6);
- know the `const&` parameter, through which a function reads an existing vector or text without copying it (lessons 6.4 and 7.3).

## The situation

In the mission of lesson 8.1, the stock value was calculated in `main`, from the fields of one object: `product.stock * product.unit_price`. What if this value has to be calculated for several products, or used in another program? Such a calculation is a good candidate for a function (lesson 5.5).

The function could get the fields separately, as two `int` parameters, but then every call has to pick the right fields in the right order, and two `int` arguments are easy to swap (lessons 5.2 and 8.1). It's simpler to pass the function **the whole existing record, for reading**. The parameter then has the type `Product`, a type we defined ourselves.

After this lesson you will:

- write functions with a parameter of your own type, passed by `const&`, and read fields through the parameter's name;
- call one function for different objects;
- match the result type to the question: a number is an `int`, and a yes-or-no answer is a `bool`;
- tell a by-value parameter from a `const&` parameter and from the copy in lesson 8.2;
- design two cooperating functions that only read a record;
- choose data that reveal mixed-up fields in a calculation.

## 1. Prepare the project

In `cpp-workspace`, create a folder `lesson_8_3` and copy `main.cpp` and `CMakeLists.txt` from the original `lesson_05_first_program` into it. You type the programs from sections 2 and 4 into that folder's `main.cpp`. The type `Product` comes from the mission of lesson 8.1.

## 2. A function that gets a record

<!-- example: stock_values -->
```cpp
#include <iostream>
#include <string>

struct Product {
    std::string name;
    int stock;
    int minimum;
    int unit_price;
};

int stock_value(const Product& product) {
    return product.stock * product.unit_price;
}

int main() {
    const Product tea{"Tea", 3, 8, 6};
    const Product rice{"Rice", 8, 8, 4};

    const int tea_value{stock_value(tea)};
    const int rice_value{stock_value(rice)};

    std::cout << tea.name << " stock value: " << tea_value << "\n";
    std::cout << rice.name << " stock value: " << rice_value << "\n";
}
```

**Predict** both lines, then run the program.

<details>
<summary>Standard output</summary>

<!-- output: stock_values -->
```text
Tea stock value: 18
Rice stock value: 32
```

</details>

- **`Product` is our type,** here in the role of a parameter type. The struct's definition stands before the function, because the function uses the type `Product` already in its header.
- **`product` is the parameter's name.** In the first call it means the object `tea`, and in the second `rice`. The function doesn't know the names of the objects in `main`, just as `count_cold_days` in lesson 6.4 didn't know the names of the vectors. The capital letter tells the type `Product` from the parameter `product`.
- **`product.stock` and `product.unit_price`** read two fields of the record passed in. The result depends on two fields of one object.
- **The function returns an `int`:** the stock value. It prints nothing and doesn't change the record: `main` prints.
- **The formula stands in the code once,** and works for both products: `3 * 6` gives 18, and `8 * 4` gives 32.

## 3. What `const Product&` means

| Part | Meaning |
|---|---|
| `Product` | the parameter's type: our own type |
| `&` | the parameter refers to an existing object from the place of the call, and isn't a copy of it |
| `const` | through this parameter the function can only read the record |
| `product` | the parameter's name, through which the function reads the fields: `product.stock` |

It's the same notation as `const std::vector<int>&` in lesson 6.4 and `const std::string&` in lesson 7.3, only with our type. The model doesn't change: **the function gets the ability to read an existing record, without creating a copy of it.** During the call `stock_value(tea)`, the name `product` is another name for the object `tea`.

- **You can't change a field through `const&`.** The line `product.stock = 0;` in this function wouldn't build, much like changing a field of a `const` object in lesson 8.2.
- **The `const` concerns access through the parameter.** It doesn't make the object in `main` constant. `tea` and `rice` are `const` because `main` doesn't change them, but that's a separate decision, as with the vector in lesson 6.4.

## 4. A second function: a yes-or-no answer

You can ask a second question about the same product: **is the stock lower than the required minimum?** Add a second function below `stock_value` and change `main` as below:

<!-- example: restock_check -->
```cpp
#include <iostream>
#include <string>

struct Product {
    std::string name;
    int stock;
    int minimum;
    int unit_price;
};

int stock_value(const Product& product) {
    return product.stock * product.unit_price;
}

bool needs_restock(const Product& product) {
    return product.stock < product.minimum;
}

int main() {
    const Product tea{"Tea", 3, 8, 6};

    const int value{stock_value(tea)};
    const bool restock{needs_restock(tea)};

    std::cout << "Product: " << tea.name << "\n";
    std::cout << "Stock value: " << value << "\n";

    if (restock) {
        std::cout << "Restock needed: yes\n";
    } else {
        std::cout << "Restock needed: no\n";
    }
}
```

**Predict** all three lines, then run the program.

<details>
<summary>Standard output</summary>

<!-- output: restock_check -->
```text
Product: Tea
Stock value: 18
Restock needed: yes
```

</details>

- **The parameter is the same** as in `stock_value`: `const Product&`.
- **The function reads other fields:** `stock` and `minimum`, not the price.
- **The result has another type:** `bool`, because the function answers a yes-or-no question, like `is_even` in lesson 5.3.
- **The function still prints nothing.** `main` chooses the text `yes` or `no` with an `if`.

| Function | Question | Fields read | Result |
|---|---|---|---|
| `stock_value` | what's the stock value? | `stock`, `unit_price` | `int` |
| `needs_restock` | is the stock below the minimum? | `stock`, `minimum` | `bool` |

This is how the program runs:

| Step | What happens |
|---|---|
| `main` creates the record | `tea`: `Tea`, 3, 8, 6 |
| `stock_value(tea)` | `product` refers to `tea`; the function calculates `3 * 6` and returns 18 |
| `needs_restock(tea)` | `product` refers to `tea` again; `3 < 8` gives `true` |
| `main` prints the report | the name from `tea.name`, the number 18 and, through an `if`, `yes` |
| after both calls | `tea` still has the same fields: `Tea`, 3, 8, 6 |

The whole record goes into the function, and one simple value comes back to `main`. The function creates no new record and no copy: it only calculates from the fields of the existing object. `main` uses the results and doesn't repeat the formulas.

## 5. By value, a copy and `const&`

| Code | What happens |
|---|---|
| `Product copy{original};` | an independent object is created with the values of the original's fields (lesson 8.2) |
| `int stock_value(Product product)` | a by-value parameter: each call creates a separate parameter object with the values of the argument's fields |
| `int stock_value(const Product& product)` | a `const&` parameter: the function reads the existing object through a reference, without a copy |

- **Passing a record by value is valid C++.** A function with the parameter `Product product` would build too, and return the same result. The parameter would then be a copy of the argument, like `before` in lesson 8.2, with its own copy of the text in the `std::string` field too.
- **`const&` avoids that copy** for plain reading. That's why a record that a function only reads is passed by `const&`, like a vector and a text, and single numbers still by value (lesson 6.4).
- **This doesn't mean that passing by value is always bad.** We choose `const&` because the functions in this lesson only read records.
- **A `const&` parameter isn't the copy from lesson 8.2.** A copy is a separate object with its own values, and a `const&` parameter is another name for the object from the place of the call.

## 6. Mission: an equipment loan check

An equipment rental checks one loan of a device. The program answers the question: **do we need to contact the person who borrowed the equipment?**

**Data:** the device `Camera`, used for 9 days, 7 days allowed, not returned yet.

**Rules:**

- The numbers of days are whole and non-negative.
- **The number of overdue days:** when the number of days used exceeds the number of days allowed, it's their difference, and otherwise 0. Overdue days are never negative.
- **Contact is needed** only when the loan is overdue **and** the device hasn't been returned yet.

The number of overdue days describes how the loan went, and the need for contact is a current decision. These are two different questions on purpose: a device returned late has a positive number of overdue days, but contact is no longer needed.

**Requirements:**

- The program defines its own type with four fields: the device's name, the number of days used, the number of days allowed, and whether the device has been returned. You choose the names of the type and the fields, their types and their order on your own.
- The program has two functions of its own that analyse the record: the first calculates the number of overdue days, and the second decides whether contact is needed. Each gets the whole record by `const&`, returns one result, doesn't change the record, prints nothing and reads nothing from the input. You choose the names of the functions and the parameters, and the result types, on your own.
- The second function may use the first, but doesn't have to.
- `main` creates one `const` object with the loan's data, calls both functions, receives their results and prints the report. It doesn't calculate the number of overdue days itself, doesn't decide about contact, and reads nothing from the input.
- The program prints exactly six lines, as in the example below: `Item`, `Days used`, `Allowed days`, `Returned`, `Overdue days` and `Contact needed`. The `Returned` and `Contact needed` lines end with the word `yes` or `no`.

In `cpp-workspace`, create a folder `equipment_loan`, copy `CMakeLists.txt` from the original `lesson_05_first_program` into it, create an empty `main.cpp` and write the program on your own.

For the data above, the standard output must be:

<!-- output: equipment_loan -->
```text
Item: Camera
Days used: 9
Allowed days: 7
Returned: no
Overdue days: 2
Contact needed: yes
```

The camera was used 2 days longer than the loan allows, and it still hasn't come back, so contact is needed.

**This isn't the program about products with different names.** You have to decide on your own:

1. what to call the type, its fields and both functions;
2. what type each field has, and what result type each function has;
3. which fields each function needs;
4. how to make sure the number of overdue days is never negative;
5. how the second function combines the delay with the information about the return, and whether it uses the first function;
6. in what order to define the functions;
7. what `main` does, and what it shouldn't do.

**Before you write the program**, prepare a table of cases: no delay, the limit reached exactly, the limit exceeded with the device not returned and returned, a return on time, zero days allowed, and zero days used. For each, write down `Overdue days` and `Contact needed`.

**Then** run the program for the data from the requirements and for two other cases from your table, for example the limit reached exactly and a device returned late. Change only the values in the object's braces. Every case in the full list of check cases is checked automatically.

### Success criteria

- The program builds as C++20 and, for the data from the requirements, prints exactly the six lines shown above.
- There's one type with four fields, and one `const` object of that type.
- Both functions get the record by `const&`, print nothing and don't change the record.
- The first function returns a number of days, never negative. The second returns a yes-or-no answer, and `main` chooses the text `yes` or `no`.
- A number of days equal to the limit isn't a delay, and a returned device never needs contact.
- `main` doesn't repeat the functions' calculations.
- The table of cases was made before the program was run.
- You can say what each function is responsible for, and what `main` is responsible for.

When the result matches, you can save the project in Git, as in lesson 1.5.

<details>
<summary>Hint 1</summary>

Which pieces of information describe one loan? Can both functions get the same record?

</details>

<details>
<summary>Hint 2</summary>

The first function calculates a number of days, the second answers yes or no. Which fields does each of them need?

</details>

<details>
<summary>Hint 3</summary>

The number of overdue days can't be negative. Contact makes sense only when the loan is past its deadline and the equipment still hasn't been returned.

</details>

<details>
<summary>The full list of check cases: open it after preparing your own table</summary>

| | Device | Days | Limit | Returned | Overdue | Contact | What it checks |
|---|---|---:|---:|---|---:|---|---|
| A | `Camera` | 9 | 7 | no | 2 | yes | the data from the requirements: the limit exceeded, the equipment not returned |
| B | `Tripod` | 5 | 7 | no | 0 | no | before the deadline |
| C | `Cable` | 7 | 7 | no | 0 | no | the limit reached exactly |
| D | `Mixer` | 10 | 7 | yes | 3 | no | returned late: a delay without contact |
| E | `Lens` | 10 | 7 | no | 3 | yes | the same days as D, but not returned |
| F | `Light` | 0 | 0 | no | 0 | no | zero days and zero days allowed |
| G | `Microphone` | 1 | 0 | no | 1 | yes | zero days allowed |
| H | `Screen` | 8 | 8 | yes | 0 | no | returned exactly on time |
| I | `Battery` | 5 | 3 | yes | 2 | no | returned late with another limit |
| J | `Charger` | 0 | 5 | no | 0 | no | zero days used |

**Automatic tests and your own runs.** Every case is checked automatically by a check program. It has the same type, the same functions and the same report as the reference solution, but it reads the loan's data from the input, one value per line. It's only a checking tool, not part of the mission: in the mission, the data is written in the code. The check program and its results are in [Example solutions](#example-solutions), because they contain the solution.

</details>

An example solution is in [Example solutions](#example-solutions).

## 7. Find the bug: swapped fields in a subtraction

Do this task **after the mission**: the program below contains functions similar to yours. Someone checks the loan of a tripod in it. You may type the program or copy it into `main.cpp`.

<details>
<summary>The program to check: open it after writing your own program</summary>

<!-- example: loan_overdue_bug -->
```cpp
#include <iostream>
#include <string>

struct Loan {
    std::string item;
    int days_used;
    int allowed_days;
    bool returned;
};

int overdue_days(const Loan& loan) {
    if (loan.days_used > loan.allowed_days) {
        return loan.allowed_days - loan.days_used;
    }

    return 0;
}

bool needs_contact(const Loan& loan) {
    return overdue_days(loan) > 0 && !loan.returned;
}

int main() {
    const Loan loan{"Tripod", 5, 7, false};

    std::cout << "Item: " << loan.item << "\n";
    std::cout << "Overdue days: " << overdue_days(loan) << "\n";

    if (needs_contact(loan)) {
        std::cout << "Contact needed: yes\n";
    } else {
        std::cout << "Contact needed: no\n";
    }
}
```

1. **Predict** the standard output for the data in the program: a tripod used for 5 days with 7 allowed, not returned. Then run the program. Does the result look right?
2. Which line of `overdue_days` returns the result for this data? Which lines of this function doesn't the program run at all then?
3. Change the values in `{}` so that the bug becomes visible. First write down the correct result for your data, then run the program.
4. Trace the data flow for your data: which fields go into the subtraction, what number `overdue_days` returns, and what `needs_contact` does with that number.
5. Point to the line with the bug. Why didn't the compiler report it?
6. Fix the function.
7. Run the fixed program for your data.

</details>

The results, example data and the fixed program are in [Example solutions](#example-solutions).

## 8. When something goes differently

| What you see | What it means | What to do |
|---|---|---|
| `cannot assign to variable 'product' with const-qualified type 'const Product &'` | The function changes a field through a `const&` parameter. | A function that analyses a record only reads it: calculate the result and return it. |
| `unknown type name` with your type's name, in a function header | The function stands in the file before the struct's definition. | Put the struct's definition before the functions that use it. |
| `use of undeclared identifier` in a function | The function uses a name it doesn't know there: a field alone (`stock`), an object from `main` (`tea`), or a function defined further down. | Read fields through the parameter: `product.stock`, not as the hint with `Product::` suggests. Define the called function higher up. |
| The warning `address of function ... will always evaluate to 'true'`, and the program always prints `yes` | The condition holds only the function's name, without a call. | Call the function with an argument, for example `needs_restock(tea)`. |
| The program works, although the parameter has no `const&` | A by-value parameter is valid C++, but the function gets a copy of the record (section 5). | In the mission, pass the record by `const&`: the function only reads it. |
| `Overdue days` is negative | The function subtracts the fields in the reverse order (section 7), or subtracts even when the limit isn't exceeded. | Subtract only when the limit is exceeded: subtract the number of days allowed from the number of days used. Otherwise return 0. |
| `Contact needed: yes` although there's no delay, for example for a number of days equal to the limit | The contact condition allows equality: `>=` instead of `>` when comparing the days with the limit, or the first function's result with zero. | Contact requires a delay: a number of days **greater** than the limit, that is, a positive result of the first function. |
| `Contact needed: yes` for a returned device | The second function checks only the delay. | Contact also requires that the device hasn't been returned. |

## 9. Explain

Answer in your own words, preferably in writing. Only then compare with the example answers.

1. What does the parameter `const Product& product` mean? What in it is the type, and what is the name?
2. Does `stock_value(tea)` get a copy of the whole record? How does its parameter differ from `const Product snapshot{tea};`?
3. How does the function read a field of the record passed in? Why doesn't it write `tea.stock`?
4. Can the function change a field through a `const&` parameter? Does the object in `main` become constant because of it?
5. Is passing a record by value a mistake? Why do we choose `const&` in this lesson?
6. When should a function's result have the type `int`, and when `bool`? Give examples from this lesson.
7. Why do the calculations stand in functions, and the printing in `main`?
8. Does a function that calls another function need a new C++ mechanism? What must be true?
9. Why are two `int` fields easy to mix up in a calculation, and why won't the compiler notice?
10. Which data let you tell the correct formula for overdue days from the formula with swapped fields, and which data don't?

<details>
<summary>Example answers</summary>

1. The function gets access to an existing object of the type `Product`, for reading only and without a copy. `Product` is our own type, `&` means a reference, `const` forbids changes through the parameter, and `product` is the parameter's name.
2. No. The parameter `product` refers to `tea`: for the duration of the call it's another name for the same object. `const Product snapshot{tea};` creates a new, separate object with a copy of the values of all the fields.
3. Through the parameter's name and a dot: `product.stock`. The function doesn't know the names of the objects in `main`, and it has to work for any product it gets.
4. No: through `const&` a field can only be read, and an attempt to assign to it doesn't build. The object in `main` doesn't become constant, because the `const` in the parameter concerns only access through that parameter.
5. No, it's valid C++. A by-value parameter is, however, a copy of the whole record, the text in the `std::string` field included. The functions in this lesson only read records, so a copy isn't needed.
6. `int` when the answer is a number: the stock value, the number of overdue days. `bool` when the answer is yes or no: whether to restock, whether contact is needed.
7. Because a function with one task works for different records, the formula stands in one place, and it can be checked separately. `main` creates the data, calls the functions and decides what to print (lesson 5.5).
8. No. You call it just as from `main`: by its name, with an argument in parentheses. At the place of the call the compiler must already know the called function, so its definition (or a declaration from lesson 5.6) stands higher up in the file.
9. Because the compiler checks types, not what the fields mean. `loan.allowed_days - loan.days_used` and `loan.days_used - loan.allowed_days` are two valid expressions of type `int`. In the same way, in lesson 8.1 the swapped values of two `int` fields built without an error.
10. Data for which the formula really runs: a number of days used greater than the limit. Then the correct formula gives a positive number, and the swapped one a negative number. Data without a delay, a number of days equal to the limit included, end at `return 0;` and give the same result in both versions.

</details>

## Summary

- A function can get a whole record. The parameter `const Product& product` gives it access to an existing object, for reading only and without a copy.
- You read fields through the parameter's name, `product.stock`, and you call one function for different objects.
- The result type follows from the question: a number is an `int`, and a yes-or-no answer is a `bool`.
- Passing a record by value is valid too, but it creates a copy of it. For plain reading we choose `const&`.
- Functions that analyse a record calculate, and `main` creates the data, calls the functions and prints the report.
- You check a formula with data for which it really runs.

## What's next

In this lesson each function analysed one record. In the next lesson many records go into one vector, and functions analyse the whole collection: [Lesson 8.4: Many records in a `std::vector`](lesson_04_many_records_in_a_vector.en.md).

---

## Example solutions

Look here **after your own attempt**. Your names may differ, as long as the standard output is as required.

<details>
<summary>Section 6: the mission, an equipment loan check</summary>

<!-- example: equipment_loan -->
```cpp
#include <iostream>
#include <string>

struct Loan {
    std::string item;
    int days_used;
    int allowed_days;
    bool returned;
};

int overdue_days(const Loan& loan) {
    if (loan.days_used > loan.allowed_days) {
        return loan.days_used - loan.allowed_days;
    }

    return 0;
}

bool needs_contact(const Loan& loan) {
    return overdue_days(loan) > 0 && !loan.returned;
}

int main() {
    const Loan loan{"Camera", 9, 7, false};

    const int overdue{overdue_days(loan)};
    const bool contact{needs_contact(loan)};

    std::cout << "Item: " << loan.item << "\n";
    std::cout << "Days used: " << loan.days_used << "\n";
    std::cout << "Allowed days: " << loan.allowed_days << "\n";

    if (loan.returned) {
        std::cout << "Returned: yes\n";
    } else {
        std::cout << "Returned: no\n";
    }

    std::cout << "Overdue days: " << overdue << "\n";

    if (contact) {
        std::cout << "Contact needed: yes\n";
    } else {
        std::cout << "Contact needed: no\n";
    }
}
```

1. **Your own type,** because four pieces of data describe one loan: the name, the number of days, the limit and the return belong to one record.
2. **The whole record in a function,** because each function needs several fields of the same loan. One parameter instead of several fields leaves no argument order to mix up.
3. **`const&`,** because the functions only read the record.
4. **No copy:** during the call, the parameter `loan` refers to the object in `main`, which is also called `loan`. The call connects them, not the name. The copy from lesson 8.2 isn't needed: nobody changes the record or has to remember its old state.
5. **`int`,** because `overdue_days` answers the question "how many days?".
6. **`bool`,** because `needs_contact` answers the question "whether?". `main` chooses the text `yes` or `no`.
7. **Fields and results:** the number of overdue days depends on `days_used` and `allowed_days`, and the need for contact on the delay and on `returned`. The device's name affects no result: it only goes into the report.
8. **The delay isn't negative:** the subtraction runs only when the number of days exceeds the limit, so the difference is positive. In the other cases the function returns 0. For 0 days and a limit of 0 the values are equal, and 0 doesn't exceed 0, so the delay is 0. Without a delay, contact isn't needed.
9. **Returned equipment:** `needs_contact` requires a delay **and** no return (`&&` and `!` from lesson 3.4). A late return leaves a positive delay, for example 3 days for `Mixer`, but contact is no longer needed.
10. **Printing in `main`:** the functions only calculate. `main` creates the record, calls the functions, stores their results and prints the report, without repeating the calculations.
11. **The record doesn't change:** the object is `const`, and the functions get `const&`, so the compiler wouldn't let a field change. The report prints the fields after both calls, and shows the same values that stand in `{}`.
12. **No new record:** the function that returns a number calculates it from the fields of the existing record and returns just the number. It creates no `Loan` object and no copy.

**The order of definitions:** `needs_contact` calls `overdue_days`, so `overdue_days` stands higher up in the file, like the helper functions in lesson 5.5. Separate declarations from lesson 5.6 aren't needed.

**Other correct solutions:** the second function can check the conditions itself, `return loan.days_used > loan.allowed_days && !loan.returned;`, because the delay is positive exactly when the number of days exceeds the limit. Calling the first function has the advantage that the delay rule stands in one place. The first function can use `if` and `else`. The fields can have other names and another order, as long as the values in `{}` stand in the same order as the fields.

**The check program** checks every case in the list of check cases. The struct and both functions are the same as above, and so is `main` from the creation of the object on, apart from the indentation. There's one difference: the loan's data is read from the input into ordinary variables, and the object `loan` is created from their values. The device names are one word each, so `>>` reads everything. The program reads the information about the return as the text `yes` or `no`, and turns it into a `bool` with a comparison, as in lesson 3.4.

<!-- example: equipment_loan_check -->
```cpp
#include <iostream>
#include <string>

struct Loan {
    std::string item;
    int days_used;
    int allowed_days;
    bool returned;
};

int overdue_days(const Loan& loan) {
    if (loan.days_used > loan.allowed_days) {
        return loan.days_used - loan.allowed_days;
    }

    return 0;
}

bool needs_contact(const Loan& loan) {
    return overdue_days(loan) > 0 && !loan.returned;
}

int main() {
    std::string item{};
    int days_used{0};
    int allowed_days{0};
    std::string returned_answer{};

    std::cin >> item;
    std::cin >> days_used;
    std::cin >> allowed_days;
    std::cin >> returned_answer;

    if (std::cin.fail()) {
        std::cout << "Input could not be read\n";
    } else {
        const Loan loan{item, days_used, allowed_days, returned_answer == "yes"};

        const int overdue{overdue_days(loan)};
        const bool contact{needs_contact(loan)};

        std::cout << "Item: " << loan.item << "\n";
        std::cout << "Days used: " << loan.days_used << "\n";
        std::cout << "Allowed days: " << loan.allowed_days << "\n";

        if (loan.returned) {
            std::cout << "Returned: yes\n";
        } else {
            std::cout << "Returned: no\n";
        }

        std::cout << "Overdue days: " << overdue << "\n";

        if (contact) {
            std::cout << "Contact needed: yes\n";
        } else {
            std::cout << "Contact needed: no\n";
        }
    }
}
```

Each case is four lines of input: the device's name, the number of days used, the number of days allowed, and `yes` or `no` for the return, in the order of the list of check cases, from A to J.

<!-- input: equipment_loan_check -->
```text
Camera
9
7
no
```

<!-- output: equipment_loan_check -->
```text
Item: Camera
Days used: 9
Allowed days: 7
Returned: no
Overdue days: 2
Contact needed: yes
```

<!-- input: equipment_loan_check -->
```text
Tripod
5
7
no
```

<!-- output: equipment_loan_check -->
```text
Item: Tripod
Days used: 5
Allowed days: 7
Returned: no
Overdue days: 0
Contact needed: no
```

<!-- input: equipment_loan_check -->
```text
Cable
7
7
no
```

<!-- output: equipment_loan_check -->
```text
Item: Cable
Days used: 7
Allowed days: 7
Returned: no
Overdue days: 0
Contact needed: no
```

<!-- input: equipment_loan_check -->
```text
Mixer
10
7
yes
```

<!-- output: equipment_loan_check -->
```text
Item: Mixer
Days used: 10
Allowed days: 7
Returned: yes
Overdue days: 3
Contact needed: no
```

<!-- input: equipment_loan_check -->
```text
Lens
10
7
no
```

<!-- output: equipment_loan_check -->
```text
Item: Lens
Days used: 10
Allowed days: 7
Returned: no
Overdue days: 3
Contact needed: yes
```

<!-- input: equipment_loan_check -->
```text
Light
0
0
no
```

<!-- output: equipment_loan_check -->
```text
Item: Light
Days used: 0
Allowed days: 0
Returned: no
Overdue days: 0
Contact needed: no
```

<!-- input: equipment_loan_check -->
```text
Microphone
1
0
no
```

<!-- output: equipment_loan_check -->
```text
Item: Microphone
Days used: 1
Allowed days: 0
Returned: no
Overdue days: 1
Contact needed: yes
```

<!-- input: equipment_loan_check -->
```text
Screen
8
8
yes
```

<!-- output: equipment_loan_check -->
```text
Item: Screen
Days used: 8
Allowed days: 8
Returned: yes
Overdue days: 0
Contact needed: no
```

<!-- input: equipment_loan_check -->
```text
Battery
5
3
yes
```

<!-- output: equipment_loan_check -->
```text
Item: Battery
Days used: 5
Allowed days: 3
Returned: yes
Overdue days: 2
Contact needed: no
```

<!-- input: equipment_loan_check -->
```text
Charger
0
5
no
```

<!-- output: equipment_loan_check -->
```text
Item: Charger
Days used: 0
Allowed days: 5
Returned: no
Overdue days: 0
Contact needed: no
```

</details>

<details>
<summary>Section 7: the results before the fix, and the fixed program</summary>

Before the fix, for a tripod used for 5 days with 7 allowed:

<!-- output: loan_overdue_bug -->
```text
Item: Tripod
Overdue days: 0
Contact needed: no
```

- **The result looks right.** 5 doesn't exceed 7, so the condition in `overdue_days` is false and the function returns 0 from its last line. The subtraction doesn't run at all, so the bug in it has no effect on the result. The correct function would return the same.
- **Data that reveal the bug:** any data in which the number of days used exceeds the limit. For example the data from the mission: `Camera`, 9 days with 7 allowed, not returned. The correct result is 2 overdue days and contact needed. The program with the bug prints:

<!-- example: loan_overdue_revealed -->
```cpp
#include <iostream>
#include <string>

struct Loan {
    std::string item;
    int days_used;
    int allowed_days;
    bool returned;
};

int overdue_days(const Loan& loan) {
    if (loan.days_used > loan.allowed_days) {
        return loan.allowed_days - loan.days_used;
    }

    return 0;
}

bool needs_contact(const Loan& loan) {
    return overdue_days(loan) > 0 && !loan.returned;
}

int main() {
    const Loan loan{"Camera", 9, 7, false};

    std::cout << "Item: " << loan.item << "\n";
    std::cout << "Overdue days: " << overdue_days(loan) << "\n";

    if (needs_contact(loan)) {
        std::cout << "Contact needed: yes\n";
    } else {
        std::cout << "Contact needed: no\n";
    }
}
```

<!-- output: loan_overdue_revealed -->
```text
Item: Camera
Overdue days: -2
Contact needed: no
```

| Step | Value |
|---|---|
| `loan.days_used > loan.allowed_days` | `9 > 7` gives `true` |
| `loan.allowed_days - loan.days_used` | `7 - 9` gives -2 |
| `overdue_days(loan)` | returns -2 |
| `overdue_days(loan) > 0` in `needs_contact` | `-2 > 0` gives `false` |
| `needs_contact(loan)` | returns `false`, although the equipment hasn't come back |

- **The cause:** the condition recognises the exceeded limit correctly, but the formula subtracts the fields in the reverse order: it subtracts the number of days used from the limit. Both fields are `int`, so the compiler accepts both expressions, like the swapped values in lesson 8.1.
- **One wrong formula spoils two lines.** `needs_contact` uses the result of `overdue_days`, so a negative delay makes the contact disappear. For a device that's already been returned, only the `Overdue days` line would be wrong.
- **The fix:** subtract the number of days allowed from the number of days used: `return loan.days_used - loan.allowed_days;`.

<!-- example: loan_overdue_fixed -->
```cpp
#include <iostream>
#include <string>

struct Loan {
    std::string item;
    int days_used;
    int allowed_days;
    bool returned;
};

int overdue_days(const Loan& loan) {
    if (loan.days_used > loan.allowed_days) {
        return loan.days_used - loan.allowed_days;
    }

    return 0;
}

bool needs_contact(const Loan& loan) {
    return overdue_days(loan) > 0 && !loan.returned;
}

int main() {
    const Loan loan{"Camera", 9, 7, false};

    std::cout << "Item: " << loan.item << "\n";
    std::cout << "Overdue days: " << overdue_days(loan) << "\n";

    if (needs_contact(loan)) {
        std::cout << "Contact needed: yes\n";
    } else {
        std::cout << "Contact needed: no\n";
    }
}
```

<!-- output: loan_overdue_fixed -->
```text
Item: Camera
Overdue days: 2
Contact needed: yes
```

For the tripod's data, the fixed program prints the same as before the fix, because for that data the function still ends at `return 0;`. That's why data without a delay aren't enough to check the formula: you need data for which the formula really runs.

</details>

**Previous lesson:** [Lesson 8.2: Changing fields and an independent copy of a record](lesson_02_changing_fields_and_copies.en.md) · **Next lesson:** [Lesson 8.4: Many records in a `std::vector`](lesson_04_many_records_in_a_vector.en.md) · [Course overview](../../README.en.md)

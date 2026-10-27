# Lesson 8.4: Many records in a `std::vector`

[Polski](lesson_04_many_records_in_a_vector.md) · **English** · [Course overview](../../README.en.md)

> **Module 8, lesson 4** · about 65–80 minutes
> **You need:** your `cpp-workspace` folder and the original `lesson_05_first_program` project, as before. You won't need the debugger in this lesson.
> **Pilot version.** The programs in this lesson are checked automatically on Windows, Ubuntu and macOS. None of them asks for data: every value is written in the code. Only the check program in the solutions part reads data from the input.

## Before you start

This lesson assumes that you:

- store numbers in a `std::vector<int>`, go through them with a range-based loop, and check `size()` and `empty()` (lessons 6.1 and 6.2);
- know that numbers of elements have the type `std::size_t`, which takes no negative values (lesson 6.3);
- pass a vector to a function by `const std::vector<int>&` (lesson 6.4);
- define a struct, create its objects with the values of all the fields in `{}` (lesson 8.1), and create a copy of a record with `Product copy{original};` (lesson 8.2);
- write functions that get a record by `const Product&` and return an `int` or a `bool` (lesson 8.3).

## The situation

In lesson 8.3 the function `stock_value` calculated the stock value of one product, and it worked for any product it got. What if the storeroom has a dozen or more products, and you need the total stock value? A separate variable and a separate call for each product mean a lot of repetition, and each new product means more lines of code.

You know this problem from Module 6: there, one `std::vector<int>` held many numbers. The same `std::vector` can store elements of our own type. Then **each element is a whole record** with several related pieces of data. It isn't a new kind of collection: only the type of the elements changes.

After this lesson you will:

- create a vector of records and initialise it with nested braces;
- go through the records with the loop `for (const Product& product : products)` and read their fields;
- explain why the loop variable doesn't copy the successive records;
- write a function that gets a whole vector of records and uses a function for one record;
- handle an empty vector and a vector with one record correctly;
- choose data that reveal a disagreement between the assessment of records and the summary.

## 1. Prepare the project

In `cpp-workspace`, create a folder `lesson_8_4` and copy `main.cpp` and `CMakeLists.txt` from the original `lesson_05_first_program` into it. You type the programs from sections 2 and 5 into that folder's `main.cpp`. The type `Product` comes from lessons 8.1 and 8.3.

## 2. A vector of records

<!-- example: product_names -->
```cpp
#include <iostream>
#include <string>
#include <vector>

struct Product {
    std::string name;
    int stock;
    int minimum;
    int unit_price;
};

int main() {
    const std::vector<Product> products{
        {"Tea", 3, 8, 6},
        {"Rice", 8, 8, 4},
        {"Pens", 10, 7, 2}
    };

    for (const Product& product : products) {
        std::cout << product.name << "\n";
    }
}
```

Type the program and **predict** what it prints. You don't have to run it: in section 5 you'll extend it, and run it then.

<details>
<summary>Standard output</summary>

<!-- output: product_names -->
```text
Tea
Rice
Pens
```

</details>

| Code | Meaning |
|---|---|
| `std::vector<Product>` | a vector whose elements have the type `Product`, just as the elements of `std::vector<int>` had the type `int` |
| the outer pair of braces | holds all the elements of the vector, like `{3, 7, 5, 9}` in lesson 6.1 |
| `{"Tea", 3, 8, 6}` | an inner pair of braces: one record, with the values in the order of the fields, as in lesson 8.1 |
| the commas between the inner pairs | separate the successive records |

- **Each record has the values of all four fields,** like every object in lessons 8.1–8.3.
- **`products.size()` is the number of records,** here 3, and `products.empty()` gives `false`. A record counts as one element, although it has four fields.
- **`const`,** because the program changes neither the vector nor the records in it.
- **One `Product` object describes one product, and `products` is a collection of products.** We choose the names as in lesson 6.1: the vector in the plural, an element in the singular.

## 3. A loop over records

Read the loop `for (const Product& product : products)` as "for each product in `products`".

| Part | Meaning |
|---|---|
| `const Product& product` | the loop variable: in each pass it refers to the next element of the vector |
| `:` and `products` | as in lesson 6.1: the vector whose elements the loop goes through |
| `product.name` | the field `name` of the current element |

- In the first pass `product` refers to the record `Tea`, in the second to `Rice`, and in the third to `Pens`. The order of the passes is the order of the records in the vector.
- **`&`:** the loop variable is another name for an existing element, not a copy of it. It's the same model as the parameter `const Product&` in lesson 8.3.
- **`const`:** you can't change the element through `product`.

## 4. Why `const Product&`?

| Code | What happens |
|---|---|
| `int stock_value(const Product& product)` | the parameter refers to the object from the place of the call (lesson 8.3) |
| `for (const Product& product : products)` | the loop variable refers to the elements of the vector, one after another |
| `Product copy{original};` | a new object is created with a copy of the values of all the fields (lesson 8.2) |

In the first two rows the model is the same: `const Product&` gives access to an existing record, for reading only and without a copy. A new object is created only in the third.

In lesson 6.4 the loop variable `const int temperature` copied one number, and such a copy is cheap. A record is several fields, a text among them. **The loop `for (const Product product : products)`, without `&`, is valid C++ too,** but its variable is a separate copy of the element in each pass, the text in the `std::string` field included. For plain reading this copy isn't needed, which is why we choose `const Product&`. In your project such a loop builds without a message, although a compiler with extra warnings turned on may remind you of the copy.

## 5. A function for the whole vector

Extend the program from section 2: add two functions before `main` and change `main` as below. The function `stock_value` is the same as in lesson 8.3.

<!-- example: stock_total -->
```cpp
#include <iostream>
#include <string>
#include <vector>

struct Product {
    std::string name;
    int stock;
    int minimum;
    int unit_price;
};

int stock_value(const Product& product) {
    return product.stock * product.unit_price;
}

int total_stock_value(const std::vector<Product>& products) {
    int total{0};

    for (const Product& product : products) {
        total += stock_value(product);
    }

    return total;
}

int main() {
    const std::vector<Product> products{
        {"Tea", 3, 8, 6},
        {"Rice", 8, 8, 4},
        {"Pens", 10, 7, 2}
    };

    std::cout << "Products: " << products.size() << "\n";
    std::cout << "Total stock value: " << total_stock_value(products) << "\n";
}
```

**Predict** both lines, then run the program.

<details>
<summary>Standard output</summary>

<!-- output: stock_total -->
```text
Products: 3
Total stock value: 70
```

</details>

- **`total_stock_value` gets the whole vector** by `const std::vector<Product>&`, like `count_cold_days` in lesson 6.4. Only now the elements are records.
- **`total`** is the accumulator from lesson 4.2: it starts at 0, and the loop adds the successive values to it.
- **The loop takes the records by `const Product&` and calls `stock_value` for each:** 18, 32 and 20. The formula `stock * unit_price` stands in the program only once.
- **The function returns one number** and prints nothing. `main` prints the number of records straight from `size()`, and the function's result.

| Function | Gets | Returns |
|---|---|---|
| `stock_value` | one record: `const Product&` | the stock value of one product |
| `total_stock_value` | the whole vector: `const std::vector<Product>&` | the sum of the stock values of all the products |

**One function knows the rule for one element, and the other organises the analysis of the whole collection.** If the stock value were calculated differently, you'd change only `stock_value`, and `total_stock_value` would use the new rule straight away.

## 6. An empty vector and one record

<!-- fragment -->
```cpp
const std::vector<Product> no_products{};
const std::vector<Product> one_product{
    {"Tea", 3, 8, 6}
};
```

**Predict** how many passes the loop in `total_stock_value` makes for each of these vectors, and what result the function returns.

<details>
<summary>A program that checks both cases</summary>

<!-- example: stock_total_small -->
```cpp
#include <iostream>
#include <string>
#include <vector>

struct Product {
    std::string name;
    int stock;
    int minimum;
    int unit_price;
};

int stock_value(const Product& product) {
    return product.stock * product.unit_price;
}

int total_stock_value(const std::vector<Product>& products) {
    int total{0};

    for (const Product& product : products) {
        total += stock_value(product);
    }

    return total;
}

int main() {
    const std::vector<Product> no_products{};
    const std::vector<Product> one_product{
        {"Tea", 3, 8, 6}
    };

    if (no_products.empty()) {
        std::cout << "No products\n";
    }

    std::cout << "Total stock value: " << total_stock_value(no_products) << "\n";
    std::cout << "Products: " << one_product.size() << "\n";
    std::cout << "Total stock value: " << total_stock_value(one_product) << "\n";
}
```

<!-- output: stock_total_small -->
```text
No products
Total stock value: 0
Products: 1
Total stock value: 18
```

</details>

- **An empty vector is valid data, not an error.** The loop makes zero passes, so the function returns the accumulator's starting value, which is 0, like `count_cold_days` for an empty vector in lesson 6.4. No special condition and no error code are needed. We read no element from an empty vector.
- **A vector with one record** still has two pairs of braces: the outer one for the vector and the inner one for the record. The loop makes one pass.

## 7. Mission: which releases are ready?

A team prepares several releases of a program. It's a simplified model, without real tools or systems. The program checks which releases are ready.

**Data:**

| Name | Checks completed | Checks required | Blocked |
|---|---:|---:|---|
| `Core` | 5 | 5 | no |
| `Mobile` | 4 | 5 | no |
| `Docs` | 3 | 3 | yes |
| `Tools` | 2 | 2 | no |
| `API` | 1 | 2 | yes |

**Rules:**

- The number of required checks is from 1 to 20. The number of completed checks is non-negative and doesn't exceed the number of required ones. The program doesn't check these assumptions: the data is written in the code.
- A release is **ready** when, at the same time, all the required checks are completed **and** the release isn't blocked.
- A release with its checks completed but blocked isn't ready. Nor is a release without a block but with checks not completed. The name doesn't affect the assessment.

**Requirements:**

- The program defines its own type with four fields: the release's name (a text), the number of completed checks and the number of required checks (whole numbers), and whether it's blocked (yes or no). You choose the names of the type and the fields, and their C++ types, on your own.
- All the releases are elements of one `const` vector, initialised in the code in the order of the table. No separate variable per release and no `push_back`.
- The program has two functions of its own. The first gets one release by `const&` and decides whether it's ready. The second gets the whole vector by `const&`, goes through the releases by `const&`, uses the first function and returns the number of ready releases. Neither changes the data, prints anything or reads anything from the input. You choose the names of the functions and the parameters, and the result types, on your own.
- `main` creates the vector, reads the number of releases with `size()`, prints the status of each release based on the first function, calls the second function, calculates the number of releases that aren't ready as a difference, and prints the summary.
- The program prints `Releases: N` first, then one line `NAME: ready` or `NAME: not ready` for each release, in the order of the vector, and finally `Ready: N` and `Not ready: N`. It prints nothing else, field values included.

In `cpp-workspace`, create a folder `release_review`, copy `CMakeLists.txt` from the original `lesson_05_first_program` into it, create an empty `main.cpp` and write the program on your own.

For the data above, the standard output must be:

<!-- output: release_review -->
```text
Releases: 5
Core: ready
Mobile: not ready
Docs: not ready
Tools: ready
API: not ready
Ready: 2
Not ready: 3
```

`Core` and `Tools` are ready. `Mobile` doesn't have all its checks, `Docs` is blocked, and `API` has both obstacles.

**This isn't the program about products with different names.** You have to decide on your own:

1. what to call the type, its fields and both functions, and what types the fields and the functions' results have;
2. which braces belong to the vector, and which to a record;
3. how to combine the two readiness conditions in the function for one release;
4. how the function for the whole vector uses the function for one release;
5. what the program prints for an empty vector;
6. how to print the status of each release in the order of the vector;
7. how to calculate the number of releases that aren't ready without repeating the readiness rule.

**Before you write the program**, prepare a table of cases: an empty vector, one ready release, one blocked, one with checks not completed, all ready, none ready, and two releases with the same numbers of checks but a different block. For each, write down the releases' statuses, and `Ready` and `Not ready`.

**Then** run the program for the data from the requirements and for an empty vector. Change only the contents of the vector's braces. Every case in the full list of check cases is checked automatically.

### Success criteria

- The program builds as C++20 and, for the data from the requirements, prints exactly the eight lines shown above.
- There's one type with four fields, and one `const` vector with five records, initialised in the code.
- Both functions get the data by `const&`, print nothing and change nothing, and the readiness rule stands in one place: the function for the vector and `main` use the function for one release.
- For an empty vector the program prints `Releases: 0`, `Ready: 0` and `Not ready: 0`, with no lines with names.
- The statuses stand in the order of the vector, and each release appears exactly once.
- The table of cases was made before the program was run.
- You can point out which braces belong to the vector, and which to a record.

When the result matches, you can save the project in Git, as in lesson 1.5.

<details>
<summary>Hint 1</summary>

How do you store several releases, each with its own name, numbers of checks and information about a block?

</details>

<details>
<summary>Hint 2</summary>

One function can assess a single record. Another can go through the whole vector and count how many records meet the same rule.

</details>

<details>
<summary>Hint 3</summary>

Don't duplicate the readiness condition in several places. In the loop over the vector, use the function for a single record, and remember the empty collection.

</details>

<details>
<summary>The full list of check cases: open it after preparing your own table</summary>

`3/5` means 3 of 5 required checks completed.

| | Releases | Ready ones | Ready | Not ready | What it checks |
|---|---|---|---:|---:|---|
| A | the data from the requirements | `Core`, `Tools` | 2 | 3 | the data from the requirements |
| B | no releases | none, no lines with names | 0 | 0 | an empty vector |
| C | `Solo` 3/3 | `Solo` | 1 | 0 | one ready release |
| D | `Beta` 2/3 | none | 0 | 1 | one release with checks not completed |
| E | `Lock` 3/3, blocked | none | 0 | 1 | one blocked release |
| F | `Alpha` 1/1, `Beta` 4/4, `Gamma` 20/20 | all | 3 | 0 | all ready; 1 and 20 required checks |
| G | `Alpha` 0/1, `Beta` 2/2 blocked, `Gamma` 1/3 blocked | none | 0 | 3 | none ready; zero completed checks; both obstacles at once |
| H | `Left` 2/2, `Right` 2/2 blocked | `Left` | 1 | 1 | the same numbers of checks, a different block |
| I | the data from the requirements in reverse order | `Tools`, `Core` | 2 | 3 | the order of the report |
| J | `Web` 3/3, `Site` 3/3 | `Web`, `Site` | 2 | 0 | the same numbers, different names |

**Automatic tests and your own runs.** Every case is checked automatically by a check program. It has the same type, the same functions and the same report as the reference solution, but it reads the releases from the input. It's only a checking tool, not part of the mission: in the mission, the vector is written in the code. The check program and its results are in [Example solutions](#example-solutions), because they contain the solution.

</details>

An example solution is in [Example solutions](#example-solutions).

## 8. Find the bug: an incomplete condition in the summary

Do this task **after the mission**: the program below contains functions similar to yours. You may type the program or copy it into `main.cpp`.

<details>
<summary>The program to check: open it after writing your own program</summary>

<!-- example: ready_count_bug -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>
#include <vector>

struct Release {
    std::string name;
    int completed_checks;
    int required_checks;
    bool blocked;
};

bool is_ready(const Release& release) {
    return release.completed_checks == release.required_checks && !release.blocked;
}

std::size_t count_ready(const std::vector<Release>& releases) {
    std::size_t ready{0};

    for (const Release& release : releases) {
        if (!release.blocked) {
            ++ready;
        }
    }

    return ready;
}

int main() {
    const std::vector<Release> releases{
        {"Web", 4, 4, false},
        {"Desktop", 2, 3, true}
    };

    for (const Release& release : releases) {
        if (is_ready(release)) {
            std::cout << release.name << ": ready\n";
        } else {
            std::cout << release.name << ": not ready\n";
        }
    }

    std::cout << "Ready: " << count_ready(releases) << "\n";
}
```

1. **Predict** the standard output for the data in the program.
2. Run the program. Does the number after `Ready` agree with the statuses?
3. Add one release to the vector so that the bug becomes visible. First write down the correct report for your data, then run the program.
4. Compare the status of each release with the number after `Ready`.
5. Find the difference between the rule by which the program assesses one release and the rule by which it counts the ready ones.
6. Explain why counting must use the same rule as the statuses.
7. Fix the counting function without changing the data in the vector.
8. Run the fixed program for your vector: in it you check both cases at once, the original data and the release you added.
9. Predict what both versions of the counting function return for an empty vector.

</details>

The results, example data and the fixed program are in [Example solutions](#example-solutions).

## 9. A copy or a reference?

<!-- fragment -->
```cpp
int stock_value(const Product& product)    // 1
for (const Product& product : products)    // 2
const Product copy{tea};                   // 3
```

1. In which line is a new object with its own field values created?
2. In which lines does the program only read an existing object? Which object is it?
3. Why doesn't the loop over records need to create a copy of each element?
4. Can you change a field of an element through `const Product&`?

<details>
<summary>Answers</summary>

1. Only in line 3. `copy` is a new object with a copy of the values of all the fields of `tea`, independent of the original (lesson 8.2).
2. In lines 1 and 2. The parameter `product` is another name for the object given in the call, and the loop variable `product` is another name for the next element of the vector.
3. Because it only reads the fields. The element already exists in the vector, and the reference gives access to it for one pass. A copy would be useful only if an old state had to be kept, as in lesson 8.2.
4. No. `const` allows reading only: the line `product.stock = 0;` in such a loop doesn't build. Changing elements of a vector of records is a separate topic, which this lesson doesn't introduce.

</details>

## 10. When something goes differently

| What you see | What it means | What to do |
|---|---|---|
| `no matching constructor for initialization of 'const std::vector<...>'` | A record's values stand in the vector's braces without their own braces, for example `{"Tea", 3, 8, 6}` instead of `{{"Tea", 3, 8, 6}}`. | Put each record in its own pair of braces inside the vector's braces. |
| A number field has the value 0, and a `bool` field the value `false`, although you didn't give them | The inner braces hold fewer values than there are fields. The program builds, and the missing fields get 0, `false` or an empty text. | Give the value of every field in every record. |
| `cannot assign to variable ... with const-qualified type` in a loop or in a function | The code changes a field through `const&`. | Functions and loops in this lesson only read records. |
| `non-constant-expression cannot be narrowed` at the number of records | You store the result of `size()`, or a difference with it, in an `int` variable with `{}` (lesson 6.3). | Store numbers of records in `std::size_t`. |
| `Not ready` is a huge number | The subtraction stands in the reverse order: you subtract the number of all releases from the number of ready ones. A `std::size_t` result can't be negative (lesson 6.3). | Subtract the number of ready releases from the number of all releases. |
| `Ready` doesn't agree with the statuses in the report | The counting function checks a different condition than the function for one release (section 8). | In the counting loop, use the function for one release. |
| A blocked release has the status `ready` | The condition leaves out the block, or joins the conditions with `\|\|`. | A release is ready only when both conditions hold at once. |
| The program works, although the loop variable has no `&` | The loop copies each record. It's valid C++, but for plain reading the copy is unnecessary (section 4). | To read the records, use a loop variable with `const&`. |

## 11. Explain

Answer in your own words, preferably in writing. Only then compare with the example answers.

1. What does `std::vector<Product>` mean? Does each element store a whole record?
2. What do the outer braces, and what do the inner braces, belong to in the initialisation of a vector of records?
3. What does `products.size()` return? What does `empty()` give for an empty vector?
4. What does a range-based loop do for an empty vector, and what does a summing or counting function return then?
5. Why can a function get the whole vector by `const std::vector<Product>&`?
6. When should a function analyse one record, and when the whole collection?
7. Why should the readiness condition stand in one function?
8. Does a correct summary count prove that every record was assessed correctly?
9. When is a loop over indices useful instead of a range-based loop?

<details>
<summary>Example answers</summary>

1. It's a vector whose elements have the type `Product`. Yes: each element is a whole record, with all its fields.
2. The outer braces hold all the elements of the vector. Each inner pair is one record, with the field values in the order of the struct's definition.
3. The number of elements, that is records, as a `std::size_t`. For an empty vector `empty()` gives `true`, and `size()` gives 0.
4. It makes no pass at all. The function then returns the starting value of the accumulator or counter, which is 0.
5. Because it only reads the records. Thanks to `&` the function reads the existing vector without copying it, and `const` doesn't let it change the vector through the parameter, as in lesson 6.4.
6. One record when the question is about one object, for example "is this release ready?". The whole collection when the answer depends on many records, for example "how many releases are ready?".
7. Because then the statuses and the count use the same rule and can't drift apart. You change the rule in one place.
8. No. The count can agree by chance, as in the masking case in section 8. Two mistakes can also cancel out: one ready release counted as not ready and one release that isn't ready counted as ready give a correct total. That's why we also check the statuses of single records.
9. When the position of a record matters, for example when numbering the lines of a report or comparing neighbouring records (lesson 6.3). For just going through the successive records, a range-based loop is enough.

</details>

## Summary

- `std::vector<Product>` is the familiar vector with records as its elements, initialised with nested braces: the outer ones for the vector, the inner ones for each record.
- `size()` gives the number of records, and `empty()` tells whether the vector is empty.
- `for (const Product& product : products)` goes through the records in the order of the vector, without copying or changing them.
- The function for one record knows the rule, and the function for the whole vector (`const std::vector<Product>&`) uses it in a loop.
- An empty vector is valid data: the loop makes no pass, and the sum or count is 0.
- A correct summary result doesn't prove that each record was assessed correctly: check the results for single records too.

## What's next

In this lesson the functions analysed a collection of records and returned one number. The next lesson of Module 8 is in preparation.

---

## Example solutions

Look here **after your own attempt**. Your names may differ, as long as the standard output is as required.

<details>
<summary>Section 7: the mission, release readiness</summary>

<!-- example: release_review -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>
#include <vector>

struct Release {
    std::string name;
    int completed_checks;
    int required_checks;
    bool blocked;
};

bool is_ready(const Release& release) {
    return release.completed_checks == release.required_checks && !release.blocked;
}

std::size_t count_ready(const std::vector<Release>& releases) {
    std::size_t ready{0};

    for (const Release& release : releases) {
        if (is_ready(release)) {
            ++ready;
        }
    }

    return ready;
}

int main() {
    const std::vector<Release> releases{
        {"Core", 5, 5, false},
        {"Mobile", 4, 5, false},
        {"Docs", 3, 3, true},
        {"Tools", 2, 2, false},
        {"API", 1, 2, true}
    };

    const std::size_t total{releases.size()};
    const std::size_t ready{count_ready(releases)};

    std::cout << "Releases: " << total << "\n";

    for (const Release& release : releases) {
        if (is_ready(release)) {
            std::cout << release.name << ": ready\n";
        } else {
            std::cout << release.name << ": not ready\n";
        }
    }

    std::cout << "Ready: " << ready << "\n";
    std::cout << "Not ready: " << total - ready << "\n";
}
```

1. **A vector of records,** because each release is several pieces of data that must stay together, and there are many releases. One vector replaces five separate variables, and a new release is just a new line in the braces.
2. **Nested braces:** the outer ones hold the elements of the vector, and each inner pair is one record: the name, two numbers of checks and the block, in the order of the fields.
3. **`const&` in the loop,** because the loop only reads the records. `const` makes sure it changes none of them.
4. **`release.name`** is the field `name` of the record the loop variable refers to in the current pass.
5. **No copy:** a record contains a text, and to read the name and the numbers a copy in every pass is unnecessary.
6. **`bool` for one release,** because `is_ready` answers a yes-or-no question. `main` chooses the text `ready` or `not ready`.
7. **`std::size_t` for the collection,** because `count_ready` returns a number of records, and numbers of elements have the type `std::size_t` in the course, like the result of `size()`. Thanks to that, `total - ready` doesn't mix types.
8. **`count_ready` calls `is_ready`,** so the readiness rule stands in the program once. The statuses and the count can't drift apart.
9. **An empty vector gives zero:** the loop in `count_ready` makes no pass, so the counter stays 0. The loop in `main` doesn't print any name either.
10. **Not ready is a difference,** because each release is either ready or not. There can't be more ready releases than all of them, so this difference is always correct. Subtracting the other way round would give a huge number, like `0 - 1` in lesson 6.3.
11. **The data doesn't change:** the vector is `const`, and the functions and loops get the records by `const&`, so the compiler wouldn't let them change.
12. **No `push_back` and no input,** because all the releases are known in advance, so a vector initialised in the code is enough.
13. **No indices,** because going through the records in order doesn't need a position (lesson 6.3).
14. **The same model works for other records:** a function for one element with a `const Type&` parameter, and a function for the collection with a `const std::vector<Type>&` parameter, which uses the first one in a loop with `const Type&`.

**Two passes over the vector:** `main` goes through the releases to print the statuses, and `count_ready` goes through them once more to count the ready ones. With a few records this doesn't matter, and thanks to it the counting function prints nothing, and `main` doesn't repeat the readiness rule.

**Other correct solutions:** with data that follows the rules, the condition `release.completed_checks >= release.required_checks` gives the same result as `==`. `main` can store the number of releases that aren't ready in a separate `std::size_t` variable. The fields can have other names and another order, as long as the values in the braces stand in the same order as the fields.

**The check program** checks every case in the list of check cases. The struct and both functions are the same as above, and so is the report from the calculation of the number of releases on, apart from the indentation. There's one difference: the vector isn't written in the code, it's built from the input. The program reads the number of releases, then each release: the name, two numbers of checks, and `yes` or `no` for the block, turned into a `bool` with a comparison, as in lesson 3.4. Each release read goes to the end of the vector with `push_back`, like the numbers in lesson 6.2. The mission needs neither input nor `push_back`.

<!-- example: release_review_check -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>
#include <vector>

struct Release {
    std::string name;
    int completed_checks;
    int required_checks;
    bool blocked;
};

bool is_ready(const Release& release) {
    return release.completed_checks == release.required_checks && !release.blocked;
}

std::size_t count_ready(const std::vector<Release>& releases) {
    std::size_t ready{0};

    for (const Release& release : releases) {
        if (is_ready(release)) {
            ++ready;
        }
    }

    return ready;
}

int main() {
    std::vector<Release> releases{};
    int count{0};

    std::cin >> count;

    for (int number{1}; number <= count; ++number) {
        std::string name{};
        int completed_checks{0};
        int required_checks{0};
        std::string blocked_answer{};

        std::cin >> name;
        std::cin >> completed_checks;
        std::cin >> required_checks;
        std::cin >> blocked_answer;

        const Release release{name, completed_checks, required_checks, blocked_answer == "yes"};
        releases.push_back(release);
    }

    if (std::cin.fail()) {
        std::cout << "Input could not be read\n";
    } else {
        const std::size_t total{releases.size()};
        const std::size_t ready{count_ready(releases)};

        std::cout << "Releases: " << total << "\n";

        for (const Release& release : releases) {
            if (is_ready(release)) {
                std::cout << release.name << ": ready\n";
            } else {
                std::cout << release.name << ": not ready\n";
            }
        }

        std::cout << "Ready: " << ready << "\n";
        std::cout << "Not ready: " << total - ready << "\n";
    }
}
```

Each case starts with the number of releases. Then each release takes one line: the name, the number of completed checks, the number of required checks, and `yes` or `no` for the block. The cases are in the order of the list of check cases, from A to J.

<!-- input: release_review_check -->
```text
5
Core 5 5 no
Mobile 4 5 no
Docs 3 3 yes
Tools 2 2 no
API 1 2 yes
```

<!-- output: release_review_check -->
```text
Releases: 5
Core: ready
Mobile: not ready
Docs: not ready
Tools: ready
API: not ready
Ready: 2
Not ready: 3
```

<!-- input: release_review_check -->
```text
0
```

<!-- output: release_review_check -->
```text
Releases: 0
Ready: 0
Not ready: 0
```

<!-- input: release_review_check -->
```text
1
Solo 3 3 no
```

<!-- output: release_review_check -->
```text
Releases: 1
Solo: ready
Ready: 1
Not ready: 0
```

<!-- input: release_review_check -->
```text
1
Beta 2 3 no
```

<!-- output: release_review_check -->
```text
Releases: 1
Beta: not ready
Ready: 0
Not ready: 1
```

<!-- input: release_review_check -->
```text
1
Lock 3 3 yes
```

<!-- output: release_review_check -->
```text
Releases: 1
Lock: not ready
Ready: 0
Not ready: 1
```

<!-- input: release_review_check -->
```text
3
Alpha 1 1 no
Beta 4 4 no
Gamma 20 20 no
```

<!-- output: release_review_check -->
```text
Releases: 3
Alpha: ready
Beta: ready
Gamma: ready
Ready: 3
Not ready: 0
```

<!-- input: release_review_check -->
```text
3
Alpha 0 1 no
Beta 2 2 yes
Gamma 1 3 yes
```

<!-- output: release_review_check -->
```text
Releases: 3
Alpha: not ready
Beta: not ready
Gamma: not ready
Ready: 0
Not ready: 3
```

<!-- input: release_review_check -->
```text
2
Left 2 2 no
Right 2 2 yes
```

<!-- output: release_review_check -->
```text
Releases: 2
Left: ready
Right: not ready
Ready: 1
Not ready: 1
```

<!-- input: release_review_check -->
```text
5
API 1 2 yes
Tools 2 2 no
Docs 3 3 yes
Mobile 4 5 no
Core 5 5 no
```

<!-- output: release_review_check -->
```text
Releases: 5
API: not ready
Tools: ready
Docs: not ready
Mobile: not ready
Core: ready
Ready: 2
Not ready: 3
```

<!-- input: release_review_check -->
```text
2
Web 3 3 no
Site 3 3 no
```

<!-- output: release_review_check -->
```text
Releases: 2
Web: ready
Site: ready
Ready: 2
Not ready: 0
```

</details>

<details>
<summary>Section 8: the results before the fix, and the fixed program</summary>

Before the fix, for the data in the program:

<!-- output: ready_count_bug -->
```text
Web: ready
Desktop: not ready
Ready: 1
```

- **The result looks right.** `Web` is ready, and `Desktop` is blocked. The counting function checks only the block, so it counts `Web` and skips `Desktop`, which by chance gives the correct 1.
- **Data that reveal the bug:** a release without a block, but with checks not completed. For example `{"Mobile", 4, 5, false}` from the mission. The correct report is `Mobile: not ready` and `Ready: 1`. The program with the bug prints:

<!-- example: ready_count_revealed -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>
#include <vector>

struct Release {
    std::string name;
    int completed_checks;
    int required_checks;
    bool blocked;
};

bool is_ready(const Release& release) {
    return release.completed_checks == release.required_checks && !release.blocked;
}

std::size_t count_ready(const std::vector<Release>& releases) {
    std::size_t ready{0};

    for (const Release& release : releases) {
        if (!release.blocked) {
            ++ready;
        }
    }

    return ready;
}

int main() {
    const std::vector<Release> releases{
        {"Web", 4, 4, false},
        {"Desktop", 2, 3, true},
        {"Mobile", 4, 5, false}
    };

    for (const Release& release : releases) {
        if (is_ready(release)) {
            std::cout << release.name << ": ready\n";
        } else {
            std::cout << release.name << ": not ready\n";
        }
    }

    std::cout << "Ready: " << count_ready(releases) << "\n";
}
```

<!-- output: ready_count_revealed -->
```text
Web: ready
Desktop: not ready
Mobile: not ready
Ready: 2
```

| Release | Status from `is_ready` | Does `count_ready` count it? |
|---|---|---|
| `Web` 4/4 | ready | yes |
| `Desktop` 2/3, blocked | not ready | no |
| `Mobile` 4/5 | not ready | **yes** |

- **The cause:** `is_ready` checks both conditions, and `count_ready` only the block. The two functions apply two different readiness rules, so the statuses report one ready release, and the count two.
- **The fix:** in the counting loop, use `is_ready`: `if (is_ready(release))`. We don't change the data in the vector.

<!-- example: ready_count_fixed -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>
#include <vector>

struct Release {
    std::string name;
    int completed_checks;
    int required_checks;
    bool blocked;
};

bool is_ready(const Release& release) {
    return release.completed_checks == release.required_checks && !release.blocked;
}

std::size_t count_ready(const std::vector<Release>& releases) {
    std::size_t ready{0};

    for (const Release& release : releases) {
        if (is_ready(release)) {
            ++ready;
        }
    }

    return ready;
}

int main() {
    const std::vector<Release> releases{
        {"Web", 4, 4, false},
        {"Desktop", 2, 3, true},
        {"Mobile", 4, 5, false}
    };

    for (const Release& release : releases) {
        if (is_ready(release)) {
            std::cout << release.name << ": ready\n";
        } else {
            std::cout << release.name << ": not ready\n";
        }
    }

    std::cout << "Ready: " << count_ready(releases) << "\n";
}
```

<!-- output: ready_count_fixed -->
```text
Web: ready
Desktop: not ready
Mobile: not ready
Ready: 1
```

For the original two releases the fixed program prints the same as before the fix, because both rules assess `Web` and `Desktop` the same way. For an empty vector both versions return 0, because the loop makes no pass. So neither the masking case nor the empty vector reveals the bug: you need a release that the two rules assess differently.

</details>

**Previous lesson:** [Lesson 8.3: Functions that analyse a record](lesson_03_functions_that_analyse_a_record.en.md) · **Next lesson:** in preparation · [Course overview](../../README.en.md)

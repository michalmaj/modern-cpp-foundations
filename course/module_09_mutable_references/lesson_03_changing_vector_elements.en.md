# Lesson 9.3: Changing the elements of a vector through a reference

[Polski](lesson_03_changing_vector_elements.md) · **English** · [Course overview](../../README.en.md)

> **Module 9, lesson 3** · about 75–90 minutes
> **You need:** your `cpp-workspace` folder and the original `lesson_05_first_program` project, as before. You won't need the debugger in this lesson.
> **Pilot version.** The programs in this lesson are checked automatically on Windows, Ubuntu and macOS. None of them asks for data: all the values are written in the code. Only the check program in the solutions part reads data from the input.

## Before you start

This lesson assumes that:

- you go through a vector with a range loop (lesson 6.1) and pass it to a function through `const&` (lesson 6.4);
- you go through a vector of records with the loop `for (const Product& product : products)` and count records in a `std::size_t` variable (lesson 8.4);
- you write a function with a `Product&` parameter that changes the record it gets (lesson 9.1);
- you know the function `issue_units` from lesson 9.2: it issues goods only when the conditions are met, and on a refusal it leaves the record unchanged and returns `false`.

## The situation

The function `issue_units` from lesson 9.2 changes one product. A warehouse, though, stores many products in one vector, and wants to issue 4 units from **each** of them. The `const Product&` loop from lesson 8.4 can only read the elements. The function from lesson 6.5 created a new vector, but here the records already in the vector must change.

Two things are needed: a loop whose variable lets you change the real element of the vector, and a function whose caller allows it to change the whole existing vector.

After this lesson you'll:

- go through the elements of a vector with the loop `for (Product& product : products)` and change them through the loop variable;
- write a function with a `std::vector<Product>&` parameter that changes the elements of an existing vector;
- tell the loop variables `const Product&`, `Product&` and `Product` apart;
- split the work between a function for one record and a function for the whole collection;
- count only the records that really changed;
- choose data that reveal that a loop changes copies of the elements.

## 1. Prepare the project

In `cpp-workspace`, create a folder `lesson_9_3` and copy `main.cpp` and `CMakeLists.txt` into it from the original `lesson_05_first_program`. You type the program from section 3 into `main.cpp` in that folder.

## 2. A loop that changes the elements

The vector `products` stores three products: `Tea` (3 units), `Rice` (8) and `Pens` (10). We want to try to issue 4 units from each of them. We aren't looking for a product with a particular name: we go through all the records and perform the same controlled operation on each.

<!-- fragment -->
```cpp
for (Product& product : products) {
    issue_units(product, 4);
}
```

| Part | Meaning |
|---|---|
| `Product& product` | the loop variable: in each pass, another name for the next element of the vector, which allows changing it |
| `products` | a vector of existing records |
| `issue_units(product, 4)` | the function from lesson 9.2 gets the current element through `Product&` |

- **`product` refers to the real elements in turn:** in the first pass to `Tea`, in the second to `Rice`, in the third to `Pens`.
- **`&` lets you change a field of the element.** A change through `product` changes the record in the vector, not a copy.
- **`issue_units` is still responsible for the conditions of one operation.** A refused issue leaves that one record unchanged.
- **Each element is processed independently.** A refusal for one product doesn't stop the loop and doesn't change the others.
- **The loop doesn't add, remove or rearrange elements.** After it, the vector has the same number of elements, in the same order. Only fields change.

## 3. A function for the whole vector

We move the work on the whole collection into a function. It gets the vector through `std::vector<Product>&`.

<!-- example: issue_each -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>
#include <vector>

struct Product {
    std::string name;
    int stock;
    int minimum;
    int unit_price;
};

bool issue_units(Product& product, int amount) {
    if (amount <= 0 || amount > product.stock) {
        return false;
    }

    product.stock -= amount;
    return true;
}

std::size_t issue_from_each(std::vector<Product>& products, int amount) {
    std::size_t accepted{0};

    for (Product& product : products) {
        if (issue_units(product, amount)) {
            ++accepted;
        }
    }

    return accepted;
}

int main() {
    std::vector<Product> products{
        {"Tea", 3, 8, 6},
        {"Rice", 8, 8, 4},
        {"Pens", 10, 7, 2}
    };

    const std::size_t accepted{issue_from_each(products, 4)};

    std::cout << "Accepted: " << accepted << "\n";

    for (const Product& product : products) {
        std::cout << product.name << ": " << product.stock << "\n";
    }
}
```

**Predict** all four lines, then run the program.

<details>
<summary>Standard output, and how the loop runs</summary>

<!-- output: issue_each -->
```text
Accepted: 2
Tea: 3
Rice: 4
Pens: 6
```

| Pass | `product` refers to | `stock` before | `issue_units(product, 4)` | `stock` after | `accepted` |
|---|---|---:|---|---:|---:|
| 1 | `Tea` | 3 | `false`: not enough units | 3 | 0 |
| 2 | `Rice` | 8 | `true` | 4 | 1 |
| 3 | `Pens` | 10 | `true` | 6 | 2 |

</details>

- **`std::vector<Product>& products`:** the function gets the existing vector from `main`, not a copy of it, and may change its elements. This is the agreement from lesson 9.1, only for the whole collection.
- **The `Product&` loop** visits the real elements of that vector.
- **The division of work:** `issue_units` decides about one product, and `issue_from_each` organises the work on the collection. The issuing rule isn't in the second function.
- **The counter grows only after an accepted issue.** A refusal changes nothing, so it isn't counted as a change. The result is a number of records, so its type is `std::size_t`, as in lesson 8.4.
- **The call in the condition itself:** the result of `issue_units` is used only for the counter, so the call stands in the `if`. It runs once in each pass.
- **The function prints nothing,** and doesn't change the names or the number of records. The report in `main` only reads the elements, so it uses a `const Product&` loop.
- **`products` in `main` has no `const`,** because its elements are meant to change.

**`&` is needed at two levels.** The parameter `std::vector<Product>&` gives access to the vector from `main`, and the loop variable `Product&` to its elements. Without either of them, the change would go to a copy: to the function's own vector, or to a separate object in the loop.

## 4. Three ways of passing a vector

| Parameter | Meaning |
|---|---|
| `std::vector<Product> products` | the function gets a separate vector, passed by value |
| `const std::vector<Product>& products` | the function reads the existing vector |
| `std::vector<Product>& products` | the function may change the existing vector |

Passing by value is valid C++: the function may change its vector, but the caller's vector stays the same. Nor is `&` always better. The choice follows from the function's job: reading, changing the existing collection, or working on its own copy.

The same goes for the loop variable:

<!-- fragment -->
```cpp
for (const Product& product : products)   // 1
for (Product& product : products)         // 2
for (Product product : products)          // 3
```

| | The loop variable | Changing a field through the loop variable |
|---|---|---|
| 1 | another name for the element, read-only | won't build |
| 2 | another name for the element, which allows changing it | changes the element of the vector |
| 3 | a separate object with a copy of the element's values | changes only that object, and the element stays unchanged |

Form 3 is valid C++, but it isn't suitable for changing the elements.

## 5. A `const` vector and an empty vector

**Predict on paper** two situations for the function `issue_from_each` from section 3:

<!-- fragment -->
```cpp
const std::vector<Product> fixed_products{
    {"Tea", 3, 8, 6}
};
std::vector<Product> no_products{};

const std::size_t first{issue_from_each(fixed_products, 4)};    // 1
const std::size_t second{issue_from_each(no_products, 4)};      // 2
```

1. Will call 1 build? Why?
2. How many passes will the loop make in call 2, what will change, and what will the result be?

<details>
<summary>Answers</summary>

1. **No.** The compiler reports `no matching function for call to 'issue_from_each'`, with a note that the first argument would lose its `const`. The `const` on the vector promises that the collection won't change, and the parameter `std::vector<Product>&` asks for the right to change it. The rejection is correct, as for a single record in lesson 9.1. Don't remove the `const` just to silence the compiler: if the stock must stay the same, this function isn't for it. A function with a `const std::vector<Product>&` parameter would accept this vector, because it promises only to read.
2. **Zero passes.** The loop reads no element, nothing changes, and the function returns the counter's starting value, 0. An empty vector is valid data: no separate condition is needed, and reading `no_products[0]` would be a mistake, because there is no such element.

</details>

## 6. Mission: settling city bikes

A bike rental stores its city bikes in one vector. Each bike has an identifier, the total number of rides recorded in its history, and the number of today's rides waiting to be settled. At the end of the day the pending rides must be moved into the history. We don't create a new fleet: **we change the existing records**.

**Data:**

| Bike | Total rides | Pending rides |
|---|---:|---:|
| B-01 | 12 | 3 |
| B-02 | 7 | 0 |
| B-03 | 20 | 2 |
| B-04 | 0 | 1 |

**Rules:**

- The numbers are non-negative and small. The data meet these assumptions, so the program doesn't check them.
- **Settling one bike:** if the number of pending rides is positive, it's added to the total number of rides, and the number of pending rides drops to 0. The record has been changed. If there are 0 pending rides, no field changes.
- The identifier never changes. The same rides must not be added a second time by a later settlement.
- **Settling the fleet** settles every bike and tells how many records really changed.

**Requirements:**

- The program defines its own type with three fields: an identifier (`std::string`), a total number of rides (`int`) and a number of pending rides (`int`). You choose the names of the type and the fields.
- There's one vector of these records in `main`, initialised in the code in the order of the table. No separate variable for each bike, and no `push_back`.
- **The function for one bike** gets one existing record, settles it according to the rules, and returns an answer whether it changed it.
- **The function for the fleet** gets the existing vector, visits all its records, calls the function for one bike for each of them, and returns the number of changed records. It doesn't repeat the settling rule, and doesn't change the number or the order of the elements.
- Neither of these functions prints anything or reads anything from the input. You choose their names and parameters.
- `main` prints the number of bikes (from `size()`) and the state before the settlement, then **settles the same fleet twice**, prints both results and the state after both settlements, exactly as in the example below.
- The program reads nothing from the input.

In `cpp-workspace`, create a folder `city_bikes`, copy `CMakeLists.txt` into it from the original `lesson_05_first_program`, create an empty `main.cpp`, and write the program yourself.

For the data in the table, the standard output must be:

<!-- output: city_bikes -->
```text
Bikes: 4
Before:
B-01: total 12, pending 3
B-02: total 7, pending 0
B-03: total 20, pending 2
B-04: total 0, pending 1
Updated: 3
Updated again: 0
After:
B-01: total 15, pending 0
B-02: total 7, pending 0
B-03: total 22, pending 0
B-04: total 1, pending 0
```

The first settlement changes three records, because `B-02` has no pending rides. The second, on **the same vector**, changes none: the first one has already set all the pending rides to zero.

For an empty fleet the program must print:

<!-- output: city_bikes_empty -->
```text
Bikes: 0
Before:
Updated: 0
Updated again: 0
After:
```

**This isn't issuing goods with other names.** You have to decide yourself:

1. how to name the type, its fields and both functions;
2. what result types both functions have;
3. how to pass one record, and how to pass the whole vector;
4. which loop variable lets you change an element of the vector, and which is enough for printing;
5. when a bike needs settling;
6. in which order to change the two fields;
7. how to count only the records that really changed;
8. why the second settlement must not add anything;
9. what the program does for an empty fleet.

**Before you write the program**, prepare a table of cases: the data from the requirements, an empty fleet, one bike without pending rides, one bike with pending rides, all bikes without pending rides, all with pending rides, two bikes with the same numbers, and the fleet from the requirements in reverse order. For each, write down both results of the settlement and the state after it.

Check the table with a sum as well: the sum of the total rides after the settlement must equal the sum of the total rides before it plus all the pending rides. For the data from the requirements: 39 + 6 = 45. This relation checks your reasoning, but it doesn't replace checking each record.

**Then** run the program for the data from the requirements and for an empty fleet. Change only the vector's initialisation while doing so. All the cases of the full check list are checked automatically.

### Success criterion

- The program builds as C++20 and, for both runs, prints exactly the lines shown above.
- The function for one bike changes the record only when there are pending rides. The function for the fleet calls it for each element and counts only real changes.
- The result types fit the answers: yes or no for one bike, a number of records for the fleet.
- Both functions change the existing data from `main`, not copies of them. They print and read nothing.
- Both settlements concern the same vector, and the second returns 0.
- The table of cases was ready before you ran the program.
- You can explain why `&` stands both in the vector parameter and in the loop variable.

When the result matches, you can save the project in Git, as in lesson 1.5.

<details>
<summary>Hint 1</summary>

Should the function prepare a new fleet, or change the bikes already stored in the existing vector?

</details>

<details>
<summary>Hint 2</summary>

One function can settle a single bike. Another can go through the whole fleet and call it for each element. Which references do you need?

</details>

<details>
<summary>Hint 3</summary>

After a correct settlement, the pending rides must be added to the history and set to zero. A second pass on the same vector must not settle them again.

</details>

<details>
<summary>The full list of check cases: open after preparing your own table</summary>

Each bike is written as its identifier, its total rides and its pending rides.

| | Fleet | Results | After the settlement | Sum of the total rides | What it checks |
|---|---|---|---|---|---|
| A | B-01 12 3, B-02 7 0, B-03 20 2, B-04 0 1 | 3, then 0 | B-01 15 0, B-02 7 0, B-03 22 0, B-04 1 0 | 39 + 6 = 45 | the data from the requirements: mixed records, a total of zero at B-04 |
| B | empty | 0, then 0 | empty | 0 + 0 = 0 | an empty fleet |
| C | C-01 5 0 | 0, then 0 | C-01 5 0 | 5 + 0 = 5 | one bike without pending rides |
| D | D-01 4 6 | 1, then 0 | D-01 10 0 | 4 + 6 = 10 | one bike with pending rides |
| E | E-01 3 0, E-02 0 0, E-03 9 0 | 0, then 0 | unchanged | 12 + 0 = 12 | no bike needs settling |
| F | F-01 1 2, F-02 5 5, F-03 0 4 | 3, then 0 | F-01 3 0, F-02 10 0, F-03 4 0 | 6 + 11 = 17 | every bike needs settling |
| G | G-01 6 2, G-02 6 2 | 2, then 0 | G-01 8 0, G-02 8 0 | 12 + 4 = 16 | two bikes with the same numbers |
| H | B-04 0 1, B-03 20 2, B-02 7 0, B-01 12 3 | 3, then 0 | B-04 1 0, B-03 22 0, B-02 7 0, B-01 15 0 | 39 + 6 = 45 | the reverse order, kept in the printout |
| I | I-01 2 0, I-02 3 0, I-03 1 7 | 1, then 0 | I-03 8 0, the rest unchanged | 6 + 7 = 13 | only the last bike needs settling |
| J | J-01 4 5, J-02 6 0, J-03 8 0 | 1, then 0 | J-01 9 0, the rest unchanged | 18 + 5 = 23 | only the first bike needs settling |

In every case the identifiers, the number of bikes and their order after the settlement are the same as before it.

**Automatic tests and your own tries.** All the cases are checked automatically by a check program. It has the same type and the same functions as the reference solution, but it reads the fleet from the input. It's only a checking tool, not part of the mission: in the mission the data are written in the code. The check program and its results are in [Example solutions](#example-solutions), because they contain the solution.

</details>

An example solution is in [Example solutions](#example-solutions).

## 7. Find the bug: a copy of the element changes

Do this task **after the mission**: the program below is meant to settle a fleet, like your program. You can type the program or copy it into `main.cpp`.

<details>
<summary>The program to check: open after writing your own program</summary>

<!-- example: fleet_copy_bug -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>
#include <vector>

struct Bike {
    std::string id;
    int total_rides;
    int pending_rides;
};

bool settle_bike(Bike& bike) {
    if (bike.pending_rides <= 0) {
        return false;
    }

    bike.total_rides += bike.pending_rides;
    bike.pending_rides = 0;
    return true;
}

std::size_t settle_fleet(std::vector<Bike>& bikes) {
    std::size_t updated{0};

    for (Bike bike : bikes) {
        if (settle_bike(bike)) {
            ++updated;
        }
    }

    return updated;
}

int main() {
    std::vector<Bike> bikes{
        {"B-01", 12, 0},
        {"B-02", 7, 0},
        {"B-03", 20, 0}
    };

    std::cout << "Bikes: " << bikes.size() << "\n";
    std::cout << "Before:\n";

    for (const Bike& bike : bikes) {
        std::cout << bike.id << ": total " << bike.total_rides << ", pending " << bike.pending_rides << "\n";
    }

    const std::size_t updated{settle_fleet(bikes)};
    const std::size_t updated_again{settle_fleet(bikes)};

    std::cout << "Updated: " << updated << "\n";
    std::cout << "Updated again: " << updated_again << "\n";
    std::cout << "After:\n";

    for (const Bike& bike : bikes) {
        std::cout << bike.id << ": total " << bike.total_rides << ", pending " << bike.pending_rides << "\n";
    }
}
```

1. **Predict** the result for the data in the program: no bike has pending rides.
2. Run the program. Does the result look correct?
3. Change the data so that at least one bike has a positive number of pending rides. Write down the correct result for your data.
4. **Predict** what this program prints on the `Updated` and `Updated again` lines.
5. **Predict** the state of the bikes in the `After` part.
6. Run the program.
7. Point to the place where the copies are made.
8. Explain why the function for one bike works correctly, while the function for the fleet doesn't keep its agreement.
9. Fix the loop.
10. Run the fixed program for your data.

</details>

The results, example data and the fixed program are in [Example solutions](#example-solutions).

## 8. When something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `Updated` is greater than 0, but `After` shows the old state | The loop in the fleet function copies the elements, and the function for one bike changes the copies (section 7). | The loop variable in a function that changes the elements needs `&`. |
| The changes are visible in the function, but not in `main` | The function gets the vector by value and changes its own copy. | Pass the vector through `&`. |
| `Updated again` is greater than 0, and the totals grow a second time | The function for one bike doesn't set the pending rides to zero. | After adding, set the number of pending rides to 0. |
| The pending rides drop to 0, but the total doesn't change | The function sets the pending rides to zero before adding them to the history. | Add first, then set to zero. |
| `Updated` equals the number of all the bikes | The counter grows in every pass, not only after a change. | Increase the counter only when the function for one bike reports a change. |
| A bike without pending rides is counted as changed | The function for one bike reports a change although it changed nothing. | When there's nothing to settle, leave the record and return `false`. |
| `binding reference of type ... drops 'const' qualifier` | A `&` loop goes through a `const` vector or a `const&` parameter. | A function that changes the elements needs a `&` parameter without `const`. |
| `no matching function for call to ...` with the note `would lose const qualifier` | A `const` vector goes into a function with a `&` parameter (section 5). | Decide whether the fleet is meant to change. If so, remove the `const` from the vector. |

## 9. Explain

Answer in your own words, preferably in writing. Only then compare with the example answers.

1. How do the parameters `std::vector<Product> products`, `const std::vector<Product>& products` and `std::vector<Product>& products` differ? What does the choice depend on?
2. How do the loop variables `const Product& product`, `Product& product` and `Product product` differ?
3. Why does a function that changes the elements need `&` in two places? What happens if one of them is missing?
4. Why does the fleet function call the function for one bike instead of repeating its condition and its changes?
5. Why does the counter grow only when the function for one record reports a change? What would a counter increased in every pass count?
6. Can the loop `for (Product& product : products)` change the number or the order of the vector's elements?
7. What does the fleet function do when the vector is empty? Why doesn't it need a separate condition?
8. Why does the second settlement of the same fleet return 0? What would it mean if it returned 3?
9. In the buggy version the counter reports a change although the vector didn't change. How is that possible? Why doesn't a fleet without pending rides reveal the bug?
10. When is it better to change the existing vector, and when to return a new one, like `keep_negative` in lesson 6.5?

<details>
<summary>Example answers</summary>

1. By value, the function gets a separate vector: it may change it, but the caller's vector stays the same. Through `const&` it only reads the existing vector. Through `&` it may change the existing vector and its elements. The choice depends on the function's job: reading, changing the caller's collection, or working on its own copy.
2. `const Product&` is another name for the element, read-only. `Product&` is another name for the element through which it can be changed. `Product` is a separate object with a copy of the element's values: changing it doesn't affect the vector.
3. Because the change must reach the elements of the vector from `main`. The `&` parameter gives access to that vector, and the `&` loop variable to its elements. Without `&` in the parameter, the function would change the elements of its own copy of the vector. Without `&` in the loop variable, it would change copies of the elements.
4. Because the rule for settling one bike should be in one place. The fleet function only organises the work on the collection. If the rule changed, fixing one function would be enough.
5. Because the result must tell how many records really changed. A bike without pending rides stays unchanged, so it isn't counted. A counter increased in every pass would simply count all the bikes, the same as `size()`.
6. No. The loop visits the existing elements in turn and may change their fields, but it doesn't add, remove or rearrange elements.
7. The loop makes zero passes, nothing changes, and the function returns the counter's starting value, 0. An empty vector is valid data, and the function reads no element.
8. Because the first settlement changed the elements of the same vector and set the pending rides to zero. A result of 3 would mean that the rides were added a second time, or that the first settlement changed copies.
9. The function for one bike really changes the object it gets and reports the change, but it gets a copy of the element. The counter grows, while the element in the vector stays old. When no bike has pending rides, both versions change nothing and return 0, so they look the same.
10. Changing the existing vector fits when the collection represents the current state and the previous one isn't needed, like the fleet after the settlement. A new vector fits when the original must stay unchanged or the result is a different collection, for example selected elements, as in lesson 6.5. These are two different agreements, not a better and a worse version.

</details>

## Summary

- The loop `for (Product& product : products)` gives access, in each pass, to the real element of the vector, which allows changing it.
- A function with a `std::vector<Product>&` parameter may change the elements of the caller's existing vector. For reading only, `const std::vector<Product>&` is enough.
- The change must go through `&` at both levels: the vector and the element. A loop variable without `&` is a copy, and changing it doesn't affect the vector.
- The function for one record holds the rule, and the function for the collection calls it for each element and counts the real changes.
- The loop doesn't change the number or the order of the elements. For an empty vector it makes zero passes.

## What's next

In this lesson a function went through all the records and changed the ones that needed a change. In the next lesson a function will find one record in a vector by the value of a field and change only that one. It's in preparation.

---

## Example solutions

Look here **after your own attempt**. Your names may differ, as long as the standard output is as required.

<details>
<summary>Section 6: the mission, settling city bikes</summary>

<!-- example: city_bikes -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>
#include <vector>

struct Bike {
    std::string id;
    int total_rides;
    int pending_rides;
};

bool settle_bike(Bike& bike) {
    if (bike.pending_rides <= 0) {
        return false;
    }

    bike.total_rides += bike.pending_rides;
    bike.pending_rides = 0;
    return true;
}

std::size_t settle_fleet(std::vector<Bike>& bikes) {
    std::size_t updated{0};

    for (Bike& bike : bikes) {
        if (settle_bike(bike)) {
            ++updated;
        }
    }

    return updated;
}

int main() {
    std::vector<Bike> bikes{
        {"B-01", 12, 3},
        {"B-02", 7, 0},
        {"B-03", 20, 2},
        {"B-04", 0, 1}
    };

    std::cout << "Bikes: " << bikes.size() << "\n";
    std::cout << "Before:\n";

    for (const Bike& bike : bikes) {
        std::cout << bike.id << ": total " << bike.total_rides << ", pending " << bike.pending_rides << "\n";
    }

    const std::size_t updated{settle_fleet(bikes)};
    const std::size_t updated_again{settle_fleet(bikes)};

    std::cout << "Updated: " << updated << "\n";
    std::cout << "Updated again: " << updated_again << "\n";
    std::cout << "After:\n";

    for (const Bike& bike : bikes) {
        std::cout << bike.id << ": total " << bike.total_rides << ", pending " << bike.pending_rides << "\n";
    }
}
```

1. **The vector without `const`,** because the settlement must change its elements.
2. **The vector parameter with `&`,** because the function must change the fleet from `main`, not its own copy.
3. **The loop variable with `&`,** because the function for one bike must get the real element of the vector, not a copy.
4. **Both levels are needed:** without the first, a copy of the vector would change; without the second, copies of the elements. Either way, the fleet in `main` would stay old.
5. **`bool` for one bike,** because the answer is "changed" or "unchanged", and the fleet function needs it for the counter.
6. **A number for the fleet, of type `std::size_t`,** because the result is a number of records, as in lesson 8.4.
7. **Unchanged bikes aren't counted,** because the result must tell how many records really changed.
8. **A copy of the element isn't enough,** because the change of the copy disappears after the loop's pass, and the element in the vector stays old (section 7).
9. **The identifier doesn't change,** because the function for one bike doesn't touch it.
10. **Only a positive number of pending rides,** because at zero there's nothing to settle, and the record must stay unchanged. The order of the changes matters: first adding to the history, then setting to zero.
11. **The second settlement returns 0,** because the first one changed the elements of the same vector and set all the pending rides to zero.
12. **An empty vector works** without a separate condition: the loops make zero passes, and the function returns the counter's starting value, 0.
13. **Different references for reading and for changing:** printing only reads, so it uses `const Bike&`, and settling changes, so it uses `Bike&`. Each loop gets only the rights it needs.
14. **No search by identifier,** because the settlement concerns every bike, not one chosen bike.
15. **Unlike lesson 6.5:** `keep_negative` left the original unchanged and returned a new vector with selected elements. Here the fleet must show the current state, so we change its existing elements. If the state before the settlement had to be kept, a copy of the vector or a function returning a new one would be better.

**Other correct solutions:**

- the condition `bike.pending_rides == 0` instead of `<= 0`, because the data are non-negative;
- the result of the function for one bike stored in a `const bool` variable before the `if`, as in lesson 9.2;
- each settlement's result printed right after its call, as long as the order of the lines stays the same.

**An empty fleet:** the same program with `std::vector<Bike> bikes{};` in place of the vector of four bikes.

<!-- example: city_bikes_empty -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>
#include <vector>

struct Bike {
    std::string id;
    int total_rides;
    int pending_rides;
};

bool settle_bike(Bike& bike) {
    if (bike.pending_rides <= 0) {
        return false;
    }

    bike.total_rides += bike.pending_rides;
    bike.pending_rides = 0;
    return true;
}

std::size_t settle_fleet(std::vector<Bike>& bikes) {
    std::size_t updated{0};

    for (Bike& bike : bikes) {
        if (settle_bike(bike)) {
            ++updated;
        }
    }

    return updated;
}

int main() {
    std::vector<Bike> bikes{};

    std::cout << "Bikes: " << bikes.size() << "\n";
    std::cout << "Before:\n";

    for (const Bike& bike : bikes) {
        std::cout << bike.id << ": total " << bike.total_rides << ", pending " << bike.pending_rides << "\n";
    }

    const std::size_t updated{settle_fleet(bikes)};
    const std::size_t updated_again{settle_fleet(bikes)};

    std::cout << "Updated: " << updated << "\n";
    std::cout << "Updated again: " << updated_again << "\n";
    std::cout << "After:\n";

    for (const Bike& bike : bikes) {
        std::cout << bike.id << ": total " << bike.total_rides << ", pending " << bike.pending_rides << "\n";
    }
}
```

**The check program** checks all the cases of the check list. The type and both functions are the same as above, and so is the report from printing the number of bikes on, apart from the indentation. There's one difference: the vector isn't written in the code, but is built from the input. The program reads the number of bikes, then each bike: its identifier and two numbers. Each bike read goes to the end of the vector with `push_back`, as in the check programs of lessons 8.4–8.6. The mission needs neither the input nor `push_back`.

<!-- example: city_bikes_check -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>
#include <vector>

struct Bike {
    std::string id;
    int total_rides;
    int pending_rides;
};

bool settle_bike(Bike& bike) {
    if (bike.pending_rides <= 0) {
        return false;
    }

    bike.total_rides += bike.pending_rides;
    bike.pending_rides = 0;
    return true;
}

std::size_t settle_fleet(std::vector<Bike>& bikes) {
    std::size_t updated{0};

    for (Bike& bike : bikes) {
        if (settle_bike(bike)) {
            ++updated;
        }
    }

    return updated;
}

int main() {
    std::vector<Bike> bikes{};
    int count{0};

    std::cin >> count;

    for (int number{1}; number <= count; ++number) {
        std::string id{};
        int total_rides{0};
        int pending_rides{0};

        std::cin >> id;
        std::cin >> total_rides;
        std::cin >> pending_rides;

        const Bike bike{id, total_rides, pending_rides};
        bikes.push_back(bike);
    }

    if (std::cin.fail()) {
        std::cout << "Input could not be read\n";
    } else {
        std::cout << "Bikes: " << bikes.size() << "\n";
        std::cout << "Before:\n";

        for (const Bike& bike : bikes) {
            std::cout << bike.id << ": total " << bike.total_rides << ", pending " << bike.pending_rides << "\n";
        }

        const std::size_t updated{settle_fleet(bikes)};
        const std::size_t updated_again{settle_fleet(bikes)};

        std::cout << "Updated: " << updated << "\n";
        std::cout << "Updated again: " << updated_again << "\n";
        std::cout << "After:\n";

        for (const Bike& bike : bikes) {
            std::cout << bike.id << ": total " << bike.total_rides << ", pending " << bike.pending_rides << "\n";
        }
    }
}
```

Each case starts with the number of bikes. Then each bike takes one line: its identifier, its total rides and its pending rides. The cases are in the order of the check list, from A to J.

<!-- input: city_bikes_check -->
```text
4
B-01 12 3
B-02 7 0
B-03 20 2
B-04 0 1
```

<!-- output: city_bikes_check -->
```text
Bikes: 4
Before:
B-01: total 12, pending 3
B-02: total 7, pending 0
B-03: total 20, pending 2
B-04: total 0, pending 1
Updated: 3
Updated again: 0
After:
B-01: total 15, pending 0
B-02: total 7, pending 0
B-03: total 22, pending 0
B-04: total 1, pending 0
```

<!-- input: city_bikes_check -->
```text
0
```

<!-- output: city_bikes_check -->
```text
Bikes: 0
Before:
Updated: 0
Updated again: 0
After:
```

<!-- input: city_bikes_check -->
```text
1
C-01 5 0
```

<!-- output: city_bikes_check -->
```text
Bikes: 1
Before:
C-01: total 5, pending 0
Updated: 0
Updated again: 0
After:
C-01: total 5, pending 0
```

<!-- input: city_bikes_check -->
```text
1
D-01 4 6
```

<!-- output: city_bikes_check -->
```text
Bikes: 1
Before:
D-01: total 4, pending 6
Updated: 1
Updated again: 0
After:
D-01: total 10, pending 0
```

<!-- input: city_bikes_check -->
```text
3
E-01 3 0
E-02 0 0
E-03 9 0
```

<!-- output: city_bikes_check -->
```text
Bikes: 3
Before:
E-01: total 3, pending 0
E-02: total 0, pending 0
E-03: total 9, pending 0
Updated: 0
Updated again: 0
After:
E-01: total 3, pending 0
E-02: total 0, pending 0
E-03: total 9, pending 0
```

<!-- input: city_bikes_check -->
```text
3
F-01 1 2
F-02 5 5
F-03 0 4
```

<!-- output: city_bikes_check -->
```text
Bikes: 3
Before:
F-01: total 1, pending 2
F-02: total 5, pending 5
F-03: total 0, pending 4
Updated: 3
Updated again: 0
After:
F-01: total 3, pending 0
F-02: total 10, pending 0
F-03: total 4, pending 0
```

<!-- input: city_bikes_check -->
```text
2
G-01 6 2
G-02 6 2
```

<!-- output: city_bikes_check -->
```text
Bikes: 2
Before:
G-01: total 6, pending 2
G-02: total 6, pending 2
Updated: 2
Updated again: 0
After:
G-01: total 8, pending 0
G-02: total 8, pending 0
```

<!-- input: city_bikes_check -->
```text
4
B-04 0 1
B-03 20 2
B-02 7 0
B-01 12 3
```

<!-- output: city_bikes_check -->
```text
Bikes: 4
Before:
B-04: total 0, pending 1
B-03: total 20, pending 2
B-02: total 7, pending 0
B-01: total 12, pending 3
Updated: 3
Updated again: 0
After:
B-04: total 1, pending 0
B-03: total 22, pending 0
B-02: total 7, pending 0
B-01: total 15, pending 0
```

<!-- input: city_bikes_check -->
```text
3
I-01 2 0
I-02 3 0
I-03 1 7
```

<!-- output: city_bikes_check -->
```text
Bikes: 3
Before:
I-01: total 2, pending 0
I-02: total 3, pending 0
I-03: total 1, pending 7
Updated: 1
Updated again: 0
After:
I-01: total 2, pending 0
I-02: total 3, pending 0
I-03: total 8, pending 0
```

<!-- input: city_bikes_check -->
```text
3
J-01 4 5
J-02 6 0
J-03 8 0
```

<!-- output: city_bikes_check -->
```text
Bikes: 3
Before:
J-01: total 4, pending 5
J-02: total 6, pending 0
J-03: total 8, pending 0
Updated: 1
Updated again: 0
After:
J-01: total 9, pending 0
J-02: total 6, pending 0
J-03: total 8, pending 0
```

</details>

<details>
<summary>Section 7: the results before the fix, and the fixed program</summary>

Before the fix, for a fleet without pending rides:

<!-- output: fleet_copy_bug -->
```text
Bikes: 3
Before:
B-01: total 12, pending 0
B-02: total 7, pending 0
B-03: total 20, pending 0
Updated: 0
Updated again: 0
After:
B-01: total 12, pending 0
B-02: total 7, pending 0
B-03: total 20, pending 0
```

- **For such a fleet the result is correct,** because no bike needs settling. The correct version also returns 0 and changes nothing.
- **Data that reveal the bug:** any fleet with at least one bike with a positive number of pending rides. For example `B-01` with 3 pending rides. The correct result is `Updated: 1`, `Updated again: 0` and `B-01: total 15, pending 0`. The buggy program prints:

<!-- example: fleet_copy_revealed -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>
#include <vector>

struct Bike {
    std::string id;
    int total_rides;
    int pending_rides;
};

bool settle_bike(Bike& bike) {
    if (bike.pending_rides <= 0) {
        return false;
    }

    bike.total_rides += bike.pending_rides;
    bike.pending_rides = 0;
    return true;
}

std::size_t settle_fleet(std::vector<Bike>& bikes) {
    std::size_t updated{0};

    for (Bike bike : bikes) {
        if (settle_bike(bike)) {
            ++updated;
        }
    }

    return updated;
}

int main() {
    std::vector<Bike> bikes{
        {"B-01", 12, 3},
        {"B-02", 7, 0},
        {"B-03", 20, 0}
    };

    std::cout << "Bikes: " << bikes.size() << "\n";
    std::cout << "Before:\n";

    for (const Bike& bike : bikes) {
        std::cout << bike.id << ": total " << bike.total_rides << ", pending " << bike.pending_rides << "\n";
    }

    const std::size_t updated{settle_fleet(bikes)};
    const std::size_t updated_again{settle_fleet(bikes)};

    std::cout << "Updated: " << updated << "\n";
    std::cout << "Updated again: " << updated_again << "\n";
    std::cout << "After:\n";

    for (const Bike& bike : bikes) {
        std::cout << bike.id << ": total " << bike.total_rides << ", pending " << bike.pending_rides << "\n";
    }
}
```

<!-- output: fleet_copy_revealed -->
```text
Bikes: 3
Before:
B-01: total 12, pending 3
B-02: total 7, pending 0
B-03: total 20, pending 0
Updated: 1
Updated again: 1
After:
B-01: total 12, pending 3
B-02: total 7, pending 0
B-03: total 20, pending 0
```

| Moment | `bike` in the loop (a copy) | `B-01` in the vector |
|---|---|---|
| before the first settlement | doesn't exist | total 12, pending 3 |
| the first pass, after `settle_bike(bike)` | total 15, pending 0; counter 1 | total 12, pending 3 |
| after the first settlement | doesn't exist | total 12, pending 3 |
| the second settlement | the same situation: a new copy, the counter 1 again | total 12, pending 3 |

- **Where the copies are made:** in the loop `for (Bike bike : bikes)`. In each pass, `bike` is a new object with the values of the current element.
- **The function for one bike works correctly:** it changes the object it gets, and reports the change. But it gets a copy, so the counter grows while the element in the vector stays old. The fleet function breaks its agreement: it reports changed records that aren't in the data.
- **The counter doesn't prove the effect.** The program reports a performed operation, although the stored data didn't change. Only `After` and the second settlement show the problem.
- **The fix:** the loop variable `Bike& bike`. The compiler reports no error in the version with a copy, because it's valid C++: changing a copy is allowed, it just doesn't fit the function's job.

<!-- example: fleet_copy_fixed -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>
#include <vector>

struct Bike {
    std::string id;
    int total_rides;
    int pending_rides;
};

bool settle_bike(Bike& bike) {
    if (bike.pending_rides <= 0) {
        return false;
    }

    bike.total_rides += bike.pending_rides;
    bike.pending_rides = 0;
    return true;
}

std::size_t settle_fleet(std::vector<Bike>& bikes) {
    std::size_t updated{0};

    for (Bike& bike : bikes) {
        if (settle_bike(bike)) {
            ++updated;
        }
    }

    return updated;
}

int main() {
    std::vector<Bike> bikes{
        {"B-01", 12, 3},
        {"B-02", 7, 0},
        {"B-03", 20, 0}
    };

    std::cout << "Bikes: " << bikes.size() << "\n";
    std::cout << "Before:\n";

    for (const Bike& bike : bikes) {
        std::cout << bike.id << ": total " << bike.total_rides << ", pending " << bike.pending_rides << "\n";
    }

    const std::size_t updated{settle_fleet(bikes)};
    const std::size_t updated_again{settle_fleet(bikes)};

    std::cout << "Updated: " << updated << "\n";
    std::cout << "Updated again: " << updated_again << "\n";
    std::cout << "After:\n";

    for (const Bike& bike : bikes) {
        std::cout << bike.id << ": total " << bike.total_rides << ", pending " << bike.pending_rides << "\n";
    }
}
```

<!-- output: fleet_copy_fixed -->
```text
Bikes: 3
Before:
B-01: total 12, pending 3
B-02: total 7, pending 0
B-03: total 20, pending 0
Updated: 1
Updated again: 0
After:
B-01: total 15, pending 0
B-02: total 7, pending 0
B-03: total 20, pending 0
```

For a fleet without pending rides the fixed program prints the same as before the fix. That's why such a fleet isn't enough to check whether the loop changes the elements of the vector.

</details>

**Previous lesson:** [Lesson 9.2: A change only when the conditions are met](lesson_02_a_change_only_when_allowed.en.md) · **Next lesson:** in preparation · [Course overview](../../README.en.md)

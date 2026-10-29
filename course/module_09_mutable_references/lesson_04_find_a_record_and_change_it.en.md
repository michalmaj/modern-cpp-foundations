# Lesson 9.4: Find a record and change the right object

[Polski](lesson_04_find_a_record_and_change_it.md) · **English** · [Course overview](../../README.en.md)

> **Module 9, lesson 4** · about 80–95 minutes
> **You need:** your `cpp-workspace` folder and the original `lesson_05_first_program` project, as before. You won't need the debugger in this lesson.
> **Pilot version.** The programs in this lesson are checked automatically on Windows, Ubuntu and macOS. None of them asks for data: all the values are written in the code. Only the check program in the solutions part reads data from the input.

## Before you start

This lesson assumes that:

- you know that an executed `return` ends the whole function call, also when it stands in a loop (lessons 5.4 and 5.7);
- you pass a text to a function through `const std::string&` (lesson 7.3) and compare texts with `==` (lesson 3.4);
- you know the function `issue_units` from lesson 9.2: it issues goods only when the conditions are met, and returns `bool`;
- you change the elements of a vector in a function with a `std::vector<Product>&` parameter and the loop `for (Product& product : products)` (lesson 9.3).

## The situation

In lesson 9.3 the function `issue_from_each` tried to issue goods from **every** product. Now the warehouse gets a different request: **issue 4 units of the product named `Pens`**. Nothing may be issued from the other products.

The function must get the existing vector and the product's name, find the right record, call `issue_units` for it, and return the result. If there's no product with that name, nothing changes.

After this lesson you'll:

- search a vector for a record by the value of one text field;
- end a function with `return` in the loop once the record is found, and put `return false;` after the loop;
- change only the record found, using the function for one record;
- tell finding a record from the success of the operation;
- choose data that reveal a `return` that comes too early.

## 1. Prepare the project

In `cpp-workspace`, create a folder `lesson_9_4` and copy `main.cpp` and `CMakeLists.txt` into it from the original `lesson_05_first_program`. You type the program from section 2 into `main.cpp` in that folder.

## 2. Searching for a product by name

<!-- example: issue_by_name -->
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

bool issue_units(Product& product, int amount) {
    if (amount <= 0 || amount > product.stock) {
        return false;
    }

    product.stock -= amount;
    return true;
}

bool issue_named(std::vector<Product>& products, const std::string& name, int amount) {
    for (Product& product : products) {
        if (product.name == name) {
            return issue_units(product, amount);
        }
    }

    return false;
}

int main() {
    std::vector<Product> products{
        {"Tea", 3, 8, 6},
        {"Rice", 8, 8, 4},
        {"Pens", 10, 7, 2}
    };

    std::cout << "Products: " << products.size() << "\n";

    const bool pens_issued{issue_named(products, "Pens", 4)};

    if (pens_issued) {
        std::cout << "Issue Pens: accepted\n";
    } else {
        std::cout << "Issue Pens: refused\n";
    }

    const bool tea_issued{issue_named(products, "Tea", 4)};

    if (tea_issued) {
        std::cout << "Issue Tea: accepted\n";
    } else {
        std::cout << "Issue Tea: refused\n";
    }

    const bool water_issued{issue_named(products, "Water", 1)};

    if (water_issued) {
        std::cout << "Issue Water: accepted\n";
    } else {
        std::cout << "Issue Water: refused\n";
    }

    for (const Product& product : products) {
        std::cout << product.name << ": " << product.stock << "\n";
    }
}
```

**Predict** all seven lines, then run the program.

<details>
<summary>Standard output</summary>

<!-- output: issue_by_name -->
```text
Products: 3
Issue Pens: accepted
Issue Tea: refused
Issue Water: refused
Tea: 3
Rice: 8
Pens: 6
```

</details>

- **`std::vector<Product>& products`** is the existing vector from `main`, which the function may change. **`const std::string& name`** is the name searched for, available for reading without copying, as in lesson 7.3. The call passes a literal, for example `"Pens"`: for the duration of the call a `std::string` is created from it (lesson 7.1), and `name` refers to that text. **`int amount`** is an ordinary number.
- **`product`** refers to the real elements of the vector in turn, as in lesson 9.3.
- **`product.name == name`** checks whether the current record has the name searched for. If not, the loop moves on to the next element.
- **On a match,** `issue_units` tries to perform the operation on that one record, and `return issue_units(product, amount);` returns its result and **ends the whole function** `issue_named`. The function doesn't look at the further elements.
- **`return false;` after the loop** runs only when the loop has gone through all the records and none matched.

What happened to each product?

- **`Pens`** is the third element: the function goes past `Tea` and `Rice`, finds `Pens`, and issues 4 units.
- **`Tea`** is found at once, but `issue_units` refuses, because there are only 3 units. The stock doesn't change.
- **`Water`** isn't in the vector: the loop goes through all three records, and the function returns `false`.
- **`Rice`** takes part in no operation. The vector still has three products, in the same order.

The two refusals have different causes, and the result is the same: `false`.

## 3. `return` in the loop and after the loop

| Situation | What happens |
|---|---|
| the current record doesn't match | the loop moves on to the next record |
| the current record matches, the operation is accepted | the function ends with `true` |
| the current record matches, the operation is refused | the function ends with `false` |
| no record matches | the loop ends, and then the function returns `false` |

`return` doesn't end one pass of the loop, but **the whole function call**, as in report C of lesson 5.7. Here that's intended: once the record is found, the job is done. That's why it matters **where** `return false;` stands. Compare:

<!-- fragment -->
```cpp
for (Product& product : products) {
    if (product.name == name) {
        return issue_units(product, amount);
    }
}

return false;
```

<!-- fragment -->
```cpp
for (Product& product : products) {
    if (product.name == name) {
        return issue_units(product, amount);
    }

    return false;
}
```

In the first version, `false` means: all the records were checked, and none matched. In the second, `return false;` stands in the loop's body, so the function ends already after the first record that doesn't match, and doesn't check the further ones.

## 4. Found, or succeeded?

The function `issue_named` has this agreement:

- **`true`:** a record was found and the requested operation was performed;
- **`false`:** the operation didn't happen, and **the whole collection is unchanged**.

`false` has two possible causes: there's no record with that name, or there is one, but the function for one record refused. The `bool` result tells only **whether the operation happened**. A `false` alone doesn't prove that the record is missing, and the `bool` doesn't answer the question whether the name exists.

If the program had to give the cause of a refusal, it would need a result that carries more information. In this lesson that isn't needed: the caller only wants to know whether the operation happened.

**Unique names.** The function ends at the **first** matching record. In our data each name appears at most once, so there can be only one matching record. This is an assumption about the data: the programs in this lesson don't check whether names repeat.

## 5. An empty vector, and a refusal after finding

**Predict on paper**, for the function `issue_named` from section 2:

1. What happens for `std::vector<Product> no_products{};` and the call `issue_named(no_products, "Tea", 1)`?
2. The name matches a record, but `issue_units` refuses, as for `Tea` in section 2. What does `issue_named` return? Does it search further?

<details>
<summary>Answers</summary>

1. **Zero passes.** The loop reads no element, and the function reaches the `return false;` after the loop. Nothing changes. That's the correct result: no separate condition is needed, and reading `no_products[0]` would be a mistake, because there is no such element.
2. **It returns `false` and doesn't search further.** The search finds the right record, `issue_units` returns `false`, and `return issue_units(product, amount);` passes that result on. No record changes. Searching for another record would make no sense, because the names are unique.

</details>

## 6. Mission: issuing equipment by code

A school's equipment loan desk stores its items in one vector. Each item has a unique code, information on whether it's available, and the number of earlier loans. The program gets requests to issue particular items, given by their codes. What matters most is that **exactly the right record** changes.

**Data:**

| Code | Available? | Earlier loans |
|---|---|---:|
| CAM-01 | yes | 2 |
| MIC-02 | no | 4 |
| TAB-03 | yes | 0 |
| LAP-04 | yes | 1 |

The requests, in this order: `TAB-03`, `MIC-02`, `BAD-99`, `TAB-03` again, and `CAM-01`.

**Rules:**

- The codes are non-empty, unique, and made of plain ASCII text. The numbers of loans are non-negative. The data meet these assumptions, so the program doesn't check them.
- **Issuing an item:** if the item is available, it becomes unavailable, and its number of loans grows by 1. If it's unavailable, no field changes.
- **A request to issue by code:** if the vector has an item with that code, the program tries to issue it. If there's no such code, nothing changes. Other items never change.
- An item's code never changes, and the vector always has the same elements in the same order.

**Requirements:**

- The program defines its own type with three fields: a code (`std::string`), the availability (`bool`) and the number of loans (`int`). You choose the names of the type and the fields.
- There's one vector of these records in `main`, initialised in the code in the order of the table. No separate variable for each item, and no `push_back`.
- **The function for one item** gets an existing record, issues it according to the rules, and returns `bool`: `true` when it issued it, `false` when the item was unavailable.
- **The function for the collection** gets the existing vector and the code searched for, finds the item with that code, calls the function for one item for it, and returns that function's result. When the code isn't there, it returns `false`. It doesn't repeat the issuing rule.
- Neither of these functions prints anything or reads anything from the input. You choose their names and parameters.
- `main` prints the number of items (from `size()`) and the state before the requests, then performs each request **exactly once, on the same vector**, prints its result (`accepted` for `true`, `refused` for `false`), and at the end the state after all the requests, exactly as in the example below.
- The program reads nothing from the input.

In `cpp-workspace`, create a folder `school_loans`, copy `CMakeLists.txt` into it from the original `lesson_05_first_program`, create an empty `main.cpp`, and write the program yourself.

For the data in the table, the standard output must be:

<!-- output: school_loans -->
```text
Equipment: 4
Before:
CAM-01: available yes, loans 2
MIC-02: available no, loans 4
TAB-03: available yes, loans 0
LAP-04: available yes, loans 1
Borrow TAB-03: accepted
Borrow MIC-02: refused
Borrow BAD-99: refused
Borrow TAB-03 again: refused
Borrow CAM-01: accepted
After:
CAM-01: available no, loans 3
MIC-02: available no, loans 4
TAB-03: available no, loans 1
LAP-04: available yes, loans 1
```

Only `TAB-03` and `CAM-01` change. The second request for `TAB-03` is refused, because the first issue changed its state. `LAP-04` stays unchanged although it's available: nobody asked for it.

**The empty-vector variant:** the same type and the same functions, an empty vector, and one request, `CAM-01`. `main` then prints only the number of items and the request's result:

<!-- output: school_loans_empty -->
```text
Equipment: 0
Borrow CAM-01: refused
```

**This isn't issuing goods with other names.** You have to decide yourself:

1. how to name the type, its fields and both functions;
2. what agreements both functions have: what they get, and what their result means;
3. why the record and the vector are passed through `&`, and the code through `const std::string&`;
4. which field is the search key, and how to compare it;
5. when to end the function inside the loop, and what to return after checking all the records;
6. which two fields a successful issue changes, and which field the function doesn't touch;
7. why the second request for `TAB-03` is refused;
8. how to make sure that other records don't change;
9. how to print the availability as `yes` or `no`.

**Before you write the program**, prepare a table of cases: the data from the requirements, an empty vector, one available item, one unavailable item, a code that isn't there, the code of the first, the middle and the last item, the same request twice, and a refusal followed by a successful issue of another item. For each, write down the results and the records that should change, with their new state. The other records must stay unchanged, and the `After` report shows them all: a correct `bool` result doesn't prove that the right record changed.

**Then** run the program for the data from the requirements and for the empty-vector variant. All the cases of the full check list are checked automatically.

### Success criterion

- The program builds as C++20 and, for both runs, prints exactly the lines shown above.
- The function for one item checks the availability before changing anything, and changes nothing on a refusal.
- The function for the collection goes through the existing records, compares the codes with `==`, ends once it finds the code, and returns `false` only after checking all the records. It doesn't repeat the issuing rule.
- Both functions change the existing data from `main`, not copies of them. They print and read nothing.
- All the requests concern the same vector, and only the issued items change.
- The table of cases was ready before you ran the program.
- You can explain why `return false;` stands after the loop, not in it.

When the result matches, you can save the project in Git, as in lesson 1.5.

<details>
<summary>Hint 1</summary>

Which function should know the rule for lending one item, and which should be responsible for finding the right item in the vector?

</details>

<details>
<summary>Hint 2</summary>

Go through the existing records through a modifiable reference. Compare the code of the current element with the code searched for.

</details>

<details>
<summary>Hint 3</summary>

Once you find the record, return the result of the function that performs the operation. If the code isn't in any record, return `false` only after the whole loop has finished.

</details>

<details>
<summary>The full list of check cases: open after preparing your own table</summary>

Each item is written as its code, its availability and its number of loans.

| | Items | Requests | Results | Changed records | What it checks |
|---|---|---|---|---|---|
| A | CAM-01 yes 2, MIC-02 no 4, TAB-03 yes 0, LAP-04 yes 1 | TAB-03, MIC-02, BAD-99, TAB-03, CAM-01 | accepted, refused, refused, refused, accepted | TAB-03 no 1, CAM-01 no 3 | the data from the requirements |
| B | none | CAM-01 | refused | none | an empty vector |
| C | CAM-01 yes 0 | CAM-01 | accepted | CAM-01 no 1 | one available item |
| D | CAM-01 no 3 | CAM-01 | refused | none | one unavailable item |
| E | CAM-01 yes 2, MIC-02 yes 0, TAB-03 yes 5 | XYZ-00 | refused | none | a code that isn't there, in a non-empty vector |
| F | as in E | CAM-01 | accepted | CAM-01 no 3 | a match at the first position |
| G | as in E | MIC-02 | accepted | MIC-02 no 1 | a match in the middle |
| H | as in E | TAB-03 | accepted | TAB-03 no 6 | a match at the last position |
| I | LAP-04 yes 1, PRO-05 yes 3 | LAP-04, LAP-04 | accepted, refused | LAP-04 no 2 | a successful issue, then the same request |
| J | MIC-02 no 4, TAB-03 yes 0 | MIC-02, TAB-03 | refused, accepted | TAB-03 no 1 | a refusal, then a successful issue of another item |
| K | CAM-01 yes 0, MIC-02 yes 1, TAB-03 yes 2 | TAB-03, CAM-01, MIC-02 | accepted, accepted, accepted | all three | several successful issues of different items |

In every case, the records outside the "Changed records" column are the same after the requests as before them, and the codes, the number of items and their order don't change.

**Automatic tests and your own tries.** All the cases are checked automatically by a check program. It has the same type and the same functions as the reference solution, but it reads the items and the requests from the input. It's only a checking tool, not part of the mission: in the mission the data are written in the code. The check program and its results are in [Example solutions](#example-solutions), because they contain the solution.

</details>

An example solution is in [Example solutions](#example-solutions).

## 7. Find the bug: the search ends too early

Do this task **after the mission**: the program below is meant to issue the item with the given code, like your program.

<details>
<summary>The program to check: open only after doing the task yourself</summary>

<!-- example: borrow_early_bug -->
```cpp
#include <iostream>
#include <string>
#include <vector>

struct Equipment {
    std::string code;
    bool available;
    int loans;
};

bool borrow_item(Equipment& item) {
    if (!item.available) {
        return false;
    }

    item.available = false;
    ++item.loans;
    return true;
}

bool borrow_by_code(std::vector<Equipment>& items, const std::string& code) {
    for (Equipment& item : items) {
        if (item.code == code) {
            return borrow_item(item);
        }

        return false;
    }

    return false;
}

void print_items(const std::vector<Equipment>& items) {
    for (const Equipment& item : items) {
        std::cout << item.code << ": available ";

        if (item.available) {
            std::cout << "yes";
        } else {
            std::cout << "no";
        }

        std::cout << ", loans " << item.loans << "\n";
    }
}

int main() {
    std::vector<Equipment> items{
        {"CAM-01", true, 2},
        {"MIC-02", false, 4},
        {"TAB-03", true, 0}
    };
    const std::string code{"CAM-01"};

    std::cout << "Before:\n";
    print_items(items);

    const bool borrowed{borrow_by_code(items, code)};

    if (borrowed) {
        std::cout << "Borrow " << code << ": accepted\n";
    } else {
        std::cout << "Borrow " << code << ": refused\n";
    }

    std::cout << "After:\n";
    print_items(items);
}
```

The report is printed by the function `print_items`, which only reads the vector, to make the program shorter. The bug isn't in it.

1. **Predict** the result for the data in the program: the code searched for belongs to the first item. Then run the program. Does the result look correct?
2. Change `code` so that the bug becomes visible. Write down the correct result and the state of all the records for your value.
3. **Predict** how many passes of the loop this program makes for your value, what the result will be, and the state of all the records. Then run the program.
4. Point to the `return` that runs too early.
5. Explain why the current record not matching doesn't mean that none matches.
6. Fix the function and run it again for your value.
7. **Predict** the result of both versions for an empty vector. Why doesn't an empty vector reveal the bug?

</details>

The results, an example value and the fixed program are in [Example solutions](#example-solutions).

## 8. When something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| Only the first item's code works, and later ones are refused | `return false;` stands in the loop and ends the function after the first record that doesn't match (section 7). | Move `return false;` after the loop. |
| One request issues several items | The function calls the operation for every element, or doesn't end after the match. | Call the operation only for the record whose code matches, and return its result at once. |
| The result is `accepted`, but `After` shows the old state | The loop variable or the vector parameter has no `&`, so a copy changes (lesson 9.3). | A function that changes the elements needs `&` in the parameter and in the loop variable. |
| The second request for `TAB-03` is accepted | The function for one item doesn't check the availability, or doesn't set it to `false`. | Check the availability before the change, and mark the item as unavailable after issuing it. |
| A refused request raises the number of loans | The function changes a field before checking the availability (lesson 9.2). | Check first, then change both fields. |
| The warning `non-void function does not return a value in all control paths` | `return false;` after the loop is missing. When the code isn't there, the call reaches the end of the function without `return`, which is undefined behaviour (lesson 5.4). | Add `return false;` after the loop. |
| The error `no viable conversion from ... to 'bool'` in a condition | The condition has `=` (assignment) instead of `==` (comparison). | Compare the codes with `==`. |
| The availability prints as `1` or `0` | The program prints the `bool` value directly (lesson 3.2). | Choose the text `yes` or `no` with an `if`. |

## 9. Explain

Answer in your own words, preferably in writing. Only then compare with the example answers.

1. Why do we search by one particular field, and why must that field be unique?
2. Why do we compare the codes with `==`, and pass the code through `const std::string&`?
3. Why does the function get the vector through `&`, and why does the loop variable also have `&`?
4. What does a `return` executed inside a loop do?
5. Why must `return false;` not run after the first record that doesn't match?
6. What does `false` mean if the record was found, and what if none was found? Can you tell from `false` alone which of these happened?
7. Why does only the function for one item know the availability rule?
8. Why is the second request for `TAB-03` refused?
9. Do correct `accepted` and `refused` results prove that all the records are in the correct state?
10. How is this lesson different from lesson 9.3?

<details>
<summary>Example answers</summary>

1. Because a request points to one particular record, and the code field identifies it. If two records had the same code, the function would change only the first of them, and the request would be ambiguous. That's why the codes in the data are unique.
2. `==` checks whether two texts are the same, as in lesson 3.4. The code is only read, so `const std::string&` is enough: the function gets the text for reading, without copying and without the right to change it.
3. Because the change must concern the item in the vector from `main`. The `&` parameter gives access to that vector, and the `&` loop variable to its elements, as in lesson 9.3. Without either of them, a copy would change.
4. It ends the whole function call and passes on the result, not just one pass of the loop. The further elements are no longer checked.
5. Because the current record not matching tells only that the one searched for is elsewhere or missing. Only after checking all the records is it known that the code isn't there.
6. When the record was found, `false` means that the function for one item refused. When none was found, `false` means that there was nothing to issue. In both cases nothing changed. From `false` alone you can't tell which case happened: the result tells only whether the operation happened.
7. Because the rule should be in one place. The function for the collection only finds the right record and passes it on. If the rule changed, fixing one function would be enough.
8. Because all the requests concern the same vector. The first issue changed `TAB-03` to unavailable, so on the second one the function for one item refuses.
9. No. The results can be right while the wrong record or a copy changed. That's why the check cases check the state of all the records after the requests.
10. In lesson 9.3 the function went through all the records and changed each one that needed a change. Here it searches for one record, changes only that one, and ends once it finds it.

</details>

## Summary

- A searching function goes through the existing vector through `&`, compares the key field with the text searched for using `==`, and changes only the record found, using the function for one record.
- `return` in a loop ends the whole function call. After finding the record that's intended, and `return false;` stands after the loop, because "not found" is known only after checking all the records.
- `false` means that the operation didn't happen and the collection is unchanged. It can come from a missing record or from a refusal, and the result alone doesn't tell these causes apart.
- For an empty vector the loop makes no pass, and the function returns `false`.
- A correct `bool` result doesn't prove a correct state: all the records have to be checked.

## What's next

The next lesson is the Module 9 test. In it you'll use the skills of the whole module: a controlled change of one record, changing the elements of a vector, and searching for a record to change. It's in preparation.

---

## Example solutions

Look here **after your own attempt**. Your names may differ, as long as the standard output is as required.

<details>
<summary>Section 6: the mission, issuing equipment by code</summary>

<!-- example: school_loans -->
```cpp
#include <iostream>
#include <string>
#include <vector>

struct Equipment {
    std::string code;
    bool available;
    int loans;
};

bool borrow_item(Equipment& item) {
    if (!item.available) {
        return false;
    }

    item.available = false;
    ++item.loans;
    return true;
}

bool borrow_by_code(std::vector<Equipment>& items, const std::string& code) {
    for (Equipment& item : items) {
        if (item.code == code) {
            return borrow_item(item);
        }
    }

    return false;
}

int main() {
    std::vector<Equipment> items{
        {"CAM-01", true, 2},
        {"MIC-02", false, 4},
        {"TAB-03", true, 0},
        {"LAP-04", true, 1}
    };

    std::cout << "Equipment: " << items.size() << "\n";
    std::cout << "Before:\n";

    for (const Equipment& item : items) {
        std::cout << item.code << ": available ";

        if (item.available) {
            std::cout << "yes";
        } else {
            std::cout << "no";
        }

        std::cout << ", loans " << item.loans << "\n";
    }

    const bool tab_borrowed{borrow_by_code(items, "TAB-03")};

    if (tab_borrowed) {
        std::cout << "Borrow TAB-03: accepted\n";
    } else {
        std::cout << "Borrow TAB-03: refused\n";
    }

    const bool mic_borrowed{borrow_by_code(items, "MIC-02")};

    if (mic_borrowed) {
        std::cout << "Borrow MIC-02: accepted\n";
    } else {
        std::cout << "Borrow MIC-02: refused\n";
    }

    const bool bad_borrowed{borrow_by_code(items, "BAD-99")};

    if (bad_borrowed) {
        std::cout << "Borrow BAD-99: accepted\n";
    } else {
        std::cout << "Borrow BAD-99: refused\n";
    }

    const bool tab_borrowed_again{borrow_by_code(items, "TAB-03")};

    if (tab_borrowed_again) {
        std::cout << "Borrow TAB-03 again: accepted\n";
    } else {
        std::cout << "Borrow TAB-03 again: refused\n";
    }

    const bool cam_borrowed{borrow_by_code(items, "CAM-01")};

    if (cam_borrowed) {
        std::cout << "Borrow CAM-01: accepted\n";
    } else {
        std::cout << "Borrow CAM-01: refused\n";
    }

    std::cout << "After:\n";

    for (const Equipment& item : items) {
        std::cout << item.code << ": available ";

        if (item.available) {
            std::cout << "yes";
        } else {
            std::cout << "no";
        }

        std::cout << ", loans " << item.loans << "\n";
    }
}
```

1. **The vector without `const`,** because the requests must change its elements.
2. **The vector parameter with `&`,** because the function must change the item in the vector from `main`, not in a copy.
3. **The loop variable with `&`,** because the function for one item must get the real element, not a copy of it.
4. **The code through `const std::string&`,** because the function only reads and compares it. It needs neither a copy nor the right to change it.
5. **`==`,** because we check whether the current record's code is exactly the one searched for.
6. **`borrow_item` knows the availability rule,** because it's the rule of one item: it checks the availability before the change, and then changes two fields.
7. **`borrow_by_code` doesn't repeat it:** it only finds the record and passes it to `borrow_item`. The rule is in one place.
8. **A match ends the search,** because the codes are unique, so later records can't match, and the job is already done.
9. **`return` in the loop ends the whole function,** not one pass. That's why `return borrow_item(item);` passes the result straight to `main`.
10. **`return false;` stands after the loop,** because only after checking all the records is it known that the code isn't there.
11. **An unavailable item doesn't change,** because `borrow_item` ends with `return false;` before the changes, as in lesson 9.2.
12. **A missing code changes nothing,** because without a match `borrow_item` isn't called for any record.
13. **The second request for `TAB-03` is refused,** because the first one changed the same record in the same vector to unavailable.
14. **The other items keep their state,** because the operation concerns only the record whose code matches.
15. **No distinction between the two reasons for a refusal,** because the report needs only to know whether the issue happened. If the program had to give the cause, it would need a result that carries more information.
16. **No pointer, iterator or index,** because the `&` loop variable gives access to the element found, and `return` passes the result on at once.
17. **The number of elements doesn't change:** the functions change only the fields of existing records, and add or remove nothing.
18. **Unlike lesson 9.3:** there the function changed every record that needed a change, and counted the changes. Here it searches for one record, changes only that one, and ends once it finds it.

**Other correct solutions:**

- the condition `if (item.available == false)` instead of `if (!item.available)`;
- `item.loans += 1;` instead of `++item.loans;`;
- your own function that prints the state of all the items, called for `Before` and for `After`, as long as it gets the vector through `const&`;
- the request's code stored in a `const std::string` variable and used in the call and in the text.

This isn't the only correct solution: yours may have other names and a different layout of `main`, as long as it meets the requirements.

**The empty-vector variant:**

<!-- example: school_loans_empty -->
```cpp
#include <iostream>
#include <string>
#include <vector>

struct Equipment {
    std::string code;
    bool available;
    int loans;
};

bool borrow_item(Equipment& item) {
    if (!item.available) {
        return false;
    }

    item.available = false;
    ++item.loans;
    return true;
}

bool borrow_by_code(std::vector<Equipment>& items, const std::string& code) {
    for (Equipment& item : items) {
        if (item.code == code) {
            return borrow_item(item);
        }
    }

    return false;
}

int main() {
    std::vector<Equipment> items{};

    std::cout << "Equipment: " << items.size() << "\n";

    const bool cam_borrowed{borrow_by_code(items, "CAM-01")};

    if (cam_borrowed) {
        std::cout << "Borrow CAM-01: accepted\n";
    } else {
        std::cout << "Borrow CAM-01: refused\n";
    }
}
```

**The check program** checks all the cases of the check list. The type and both functions are the same as above. The difference is in `main`: the program reads the number of items, then each item (its code, `yes` or `no` for the availability, and its number of loans), and then the number of requests. Each item goes to the end of the vector with `push_back`, as in the check programs of lessons 8.4–9.3. The program reads the requests' codes one at a time, only in the loop over the requests, and performs each request at once. It prints `Before`, the result of each request and `After`, like the mission, but without the word `again`. The mission needs neither the input nor `push_back`.

<!-- example: school_loans_check -->
```cpp
#include <iostream>
#include <string>
#include <vector>

struct Equipment {
    std::string code;
    bool available;
    int loans;
};

bool borrow_item(Equipment& item) {
    if (!item.available) {
        return false;
    }

    item.available = false;
    ++item.loans;
    return true;
}

bool borrow_by_code(std::vector<Equipment>& items, const std::string& code) {
    for (Equipment& item : items) {
        if (item.code == code) {
            return borrow_item(item);
        }
    }

    return false;
}

int main() {
    std::vector<Equipment> items{};
    int count{0};

    std::cin >> count;

    for (int number{1}; number <= count; ++number) {
        std::string code{};
        std::string available_answer{};
        int loans{0};

        std::cin >> code;
        std::cin >> available_answer;
        std::cin >> loans;

        const Equipment item{code, available_answer == "yes", loans};
        items.push_back(item);
    }

    int request_count{0};
    std::cin >> request_count;

    if (std::cin.fail()) {
        std::cout << "Input could not be read\n";
    } else {
        std::cout << "Equipment: " << items.size() << "\n";
        std::cout << "Before:\n";

        for (const Equipment& item : items) {
            std::cout << item.code << ": available ";

            if (item.available) {
                std::cout << "yes";
            } else {
                std::cout << "no";
            }

            std::cout << ", loans " << item.loans << "\n";
        }

        for (int number{1}; number <= request_count; ++number) {
            std::string code{};
            std::cin >> code;

            const bool borrowed{borrow_by_code(items, code)};

            if (borrowed) {
                std::cout << "Borrow " << code << ": accepted\n";
            } else {
                std::cout << "Borrow " << code << ": refused\n";
            }
        }

        std::cout << "After:\n";

        for (const Equipment& item : items) {
            std::cout << item.code << ": available ";

            if (item.available) {
                std::cout << "yes";
            } else {
                std::cout << "no";
            }

            std::cout << ", loans " << item.loans << "\n";
        }
    }
}
```

Each case starts with the number of items. Then each item takes one line: its code, its availability and its number of loans. Next come the number of requests and the requests' codes, one per line. The cases are in the order of the check list, from A to K.

<!-- input: school_loans_check -->
```text
4
CAM-01 yes 2
MIC-02 no 4
TAB-03 yes 0
LAP-04 yes 1
5
TAB-03
MIC-02
BAD-99
TAB-03
CAM-01
```

<!-- output: school_loans_check -->
```text
Equipment: 4
Before:
CAM-01: available yes, loans 2
MIC-02: available no, loans 4
TAB-03: available yes, loans 0
LAP-04: available yes, loans 1
Borrow TAB-03: accepted
Borrow MIC-02: refused
Borrow BAD-99: refused
Borrow TAB-03: refused
Borrow CAM-01: accepted
After:
CAM-01: available no, loans 3
MIC-02: available no, loans 4
TAB-03: available no, loans 1
LAP-04: available yes, loans 1
```

<!-- input: school_loans_check -->
```text
0
1
CAM-01
```

<!-- output: school_loans_check -->
```text
Equipment: 0
Before:
Borrow CAM-01: refused
After:
```

<!-- input: school_loans_check -->
```text
1
CAM-01 yes 0
1
CAM-01
```

<!-- output: school_loans_check -->
```text
Equipment: 1
Before:
CAM-01: available yes, loans 0
Borrow CAM-01: accepted
After:
CAM-01: available no, loans 1
```

<!-- input: school_loans_check -->
```text
1
CAM-01 no 3
1
CAM-01
```

<!-- output: school_loans_check -->
```text
Equipment: 1
Before:
CAM-01: available no, loans 3
Borrow CAM-01: refused
After:
CAM-01: available no, loans 3
```

<!-- input: school_loans_check -->
```text
3
CAM-01 yes 2
MIC-02 yes 0
TAB-03 yes 5
1
XYZ-00
```

<!-- output: school_loans_check -->
```text
Equipment: 3
Before:
CAM-01: available yes, loans 2
MIC-02: available yes, loans 0
TAB-03: available yes, loans 5
Borrow XYZ-00: refused
After:
CAM-01: available yes, loans 2
MIC-02: available yes, loans 0
TAB-03: available yes, loans 5
```

<!-- input: school_loans_check -->
```text
3
CAM-01 yes 2
MIC-02 yes 0
TAB-03 yes 5
1
CAM-01
```

<!-- output: school_loans_check -->
```text
Equipment: 3
Before:
CAM-01: available yes, loans 2
MIC-02: available yes, loans 0
TAB-03: available yes, loans 5
Borrow CAM-01: accepted
After:
CAM-01: available no, loans 3
MIC-02: available yes, loans 0
TAB-03: available yes, loans 5
```

<!-- input: school_loans_check -->
```text
3
CAM-01 yes 2
MIC-02 yes 0
TAB-03 yes 5
1
MIC-02
```

<!-- output: school_loans_check -->
```text
Equipment: 3
Before:
CAM-01: available yes, loans 2
MIC-02: available yes, loans 0
TAB-03: available yes, loans 5
Borrow MIC-02: accepted
After:
CAM-01: available yes, loans 2
MIC-02: available no, loans 1
TAB-03: available yes, loans 5
```

<!-- input: school_loans_check -->
```text
3
CAM-01 yes 2
MIC-02 yes 0
TAB-03 yes 5
1
TAB-03
```

<!-- output: school_loans_check -->
```text
Equipment: 3
Before:
CAM-01: available yes, loans 2
MIC-02: available yes, loans 0
TAB-03: available yes, loans 5
Borrow TAB-03: accepted
After:
CAM-01: available yes, loans 2
MIC-02: available yes, loans 0
TAB-03: available no, loans 6
```

<!-- input: school_loans_check -->
```text
2
LAP-04 yes 1
PRO-05 yes 3
2
LAP-04
LAP-04
```

<!-- output: school_loans_check -->
```text
Equipment: 2
Before:
LAP-04: available yes, loans 1
PRO-05: available yes, loans 3
Borrow LAP-04: accepted
Borrow LAP-04: refused
After:
LAP-04: available no, loans 2
PRO-05: available yes, loans 3
```

<!-- input: school_loans_check -->
```text
2
MIC-02 no 4
TAB-03 yes 0
2
MIC-02
TAB-03
```

<!-- output: school_loans_check -->
```text
Equipment: 2
Before:
MIC-02: available no, loans 4
TAB-03: available yes, loans 0
Borrow MIC-02: refused
Borrow TAB-03: accepted
After:
MIC-02: available no, loans 4
TAB-03: available no, loans 1
```

<!-- input: school_loans_check -->
```text
3
CAM-01 yes 0
MIC-02 yes 1
TAB-03 yes 2
3
TAB-03
CAM-01
MIC-02
```

<!-- output: school_loans_check -->
```text
Equipment: 3
Before:
CAM-01: available yes, loans 0
MIC-02: available yes, loans 1
TAB-03: available yes, loans 2
Borrow TAB-03: accepted
Borrow CAM-01: accepted
Borrow MIC-02: accepted
After:
CAM-01: available no, loans 1
MIC-02: available no, loans 2
TAB-03: available no, loans 3
```

</details>

<details>
<summary>Section 7: the results before the fix, and the fixed program</summary>

Before the fix, for the code of the first item:

<!-- output: borrow_early_bug -->
```text
Before:
CAM-01: available yes, loans 2
MIC-02: available no, loans 4
TAB-03: available yes, loans 0
Borrow CAM-01: accepted
After:
CAM-01: available no, loans 3
MIC-02: available no, loans 4
TAB-03: available yes, loans 0
```

- **For the first item the result is correct,** because the match happens in the first pass, before the wrong `return false;` has a chance to run.
- **Data that reveal the bug:** the code of an item that isn't first. For example `TAB-03`, the third one, which is available. The correct result is `accepted` and `TAB-03: available no, loans 1`. The buggy program prints:

<!-- example: borrow_early_revealed -->
```cpp
#include <iostream>
#include <string>
#include <vector>

struct Equipment {
    std::string code;
    bool available;
    int loans;
};

bool borrow_item(Equipment& item) {
    if (!item.available) {
        return false;
    }

    item.available = false;
    ++item.loans;
    return true;
}

bool borrow_by_code(std::vector<Equipment>& items, const std::string& code) {
    for (Equipment& item : items) {
        if (item.code == code) {
            return borrow_item(item);
        }

        return false;
    }

    return false;
}

void print_items(const std::vector<Equipment>& items) {
    for (const Equipment& item : items) {
        std::cout << item.code << ": available ";

        if (item.available) {
            std::cout << "yes";
        } else {
            std::cout << "no";
        }

        std::cout << ", loans " << item.loans << "\n";
    }
}

int main() {
    std::vector<Equipment> items{
        {"CAM-01", true, 2},
        {"MIC-02", false, 4},
        {"TAB-03", true, 0}
    };
    const std::string code{"TAB-03"};

    std::cout << "Before:\n";
    print_items(items);

    const bool borrowed{borrow_by_code(items, code)};

    if (borrowed) {
        std::cout << "Borrow " << code << ": accepted\n";
    } else {
        std::cout << "Borrow " << code << ": refused\n";
    }

    std::cout << "After:\n";
    print_items(items);
}
```

<!-- output: borrow_early_revealed -->
```text
Before:
CAM-01: available yes, loans 2
MIC-02: available no, loans 4
TAB-03: available yes, loans 0
Borrow TAB-03: refused
After:
CAM-01: available yes, loans 2
MIC-02: available no, loans 4
TAB-03: available yes, loans 0
```

| Pass | `item` | `item.code == code` | What runs |
|---|---|---|---|
| 1 | `CAM-01` | `false` | `return false;` in the loop: the function ends |
| 2 | `MIC-02` | not checked | — |
| 3 | `TAB-03` | not checked | — |

- **The loop makes one pass.** `return false;` stands in the loop's body, after the `if`, so it runs in the first pass in which the code doesn't match. The function ends before it reaches `TAB-03`.
- **The current record not matching doesn't mean that none matches.** This `return false;` announces "not found" after checking one record of three. The existing, available item is neither found nor issued, and the report says `refused`.
- **The fix:** move `return false;` after the loop. Then it runs only after all the records have been checked.
- **Compared with lesson 5.7:** in report C, `return total;` also stood in the loop's body without a condition, and ended the function after the first pass. There it was masked by 0 and 1 rounds, here by a match at the first position and by an empty vector. What's new is that this loop also has an intended `return`, after the match, and that the bug has an effect on the data: the right record exists, but doesn't change.

<!-- example: borrow_early_fixed -->
```cpp
#include <iostream>
#include <string>
#include <vector>

struct Equipment {
    std::string code;
    bool available;
    int loans;
};

bool borrow_item(Equipment& item) {
    if (!item.available) {
        return false;
    }

    item.available = false;
    ++item.loans;
    return true;
}

bool borrow_by_code(std::vector<Equipment>& items, const std::string& code) {
    for (Equipment& item : items) {
        if (item.code == code) {
            return borrow_item(item);
        }
    }

    return false;
}

void print_items(const std::vector<Equipment>& items) {
    for (const Equipment& item : items) {
        std::cout << item.code << ": available ";

        if (item.available) {
            std::cout << "yes";
        } else {
            std::cout << "no";
        }

        std::cout << ", loans " << item.loans << "\n";
    }
}

int main() {
    std::vector<Equipment> items{
        {"CAM-01", true, 2},
        {"MIC-02", false, 4},
        {"TAB-03", true, 0}
    };
    const std::string code{"TAB-03"};

    std::cout << "Before:\n";
    print_items(items);

    const bool borrowed{borrow_by_code(items, code)};

    if (borrowed) {
        std::cout << "Borrow " << code << ": accepted\n";
    } else {
        std::cout << "Borrow " << code << ": refused\n";
    }

    std::cout << "After:\n";
    print_items(items);
}
```

<!-- output: borrow_early_fixed -->
```text
Before:
CAM-01: available yes, loans 2
MIC-02: available no, loans 4
TAB-03: available yes, loans 0
Borrow TAB-03: accepted
After:
CAM-01: available yes, loans 2
MIC-02: available no, loans 4
TAB-03: available no, loans 1
```

**An empty vector:** both versions return `false`. The loop makes no pass, so the wrong `return false;` in its body never runs, and both functions reach the `return false;` after the loop. That's why an empty vector doesn't reveal the bug.

</details>

**Previous lesson:** [Lesson 9.3: Changing the elements of a vector through a reference](lesson_03_changing_vector_elements.en.md) · **Next lesson:** in preparation · [Course overview](../../README.en.md)

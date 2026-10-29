# Lesson 9.2: A change only when the conditions are met

[Polski](lesson_02_a_change_only_when_allowed.md) · **English** · [Course overview](../../README.en.md)

> **Module 9, lesson 2** · about 75–90 minutes
> **You need:** your `cpp-workspace` folder and the original `lesson_05_first_program` project, as before. You won't need the debugger in this lesson.
> **Pilot version.** The programs in this lesson are checked automatically on Windows, Ubuntu and macOS. None of them asks for data: all the values are written in the code. Only the check program in the solutions part reads data from the input.

## Before you start

This lesson assumes that:

- you write a function with a `Product&` parameter that changes the record it gets (lesson 9.1);
- you write functions that return `bool` (lesson 5.3), and guard clauses with an early `return` (lesson 5.4);
- you join conditions with the `||` operator and know that its right side isn't evaluated when the left side already decides the result (lesson 3.4);
- you know the "all or nothing" rule from the reservations in lesson 8.2, where `main` checked the free seats before changing the field.

## The situation

A warehouse issues goods. The product `Tea` has 8 units. Issuing 3 units is possible, but issuing 6 of the remaining 5 isn't: the stock can't fall below zero. The function from lesson 9.1 changed the record every time. Here the change is allowed only when the conditions are met, and the caller must find out whether the operation was accepted.

In lesson 8.2 the condition was checked by `main`. If goods were issued in several places of a program, the rule would stand in each of them, and one forgotten check would spoil the record. Now the rule belongs to the function that changes the record: the function first checks the conditions, changes the record only when that's allowed, and returns a `bool` that tells whether it accepted the operation.

After this lesson you'll:

- write a function with a `&` parameter that changes a record only when the conditions are met, and returns `bool`;
- tell a function's result (`true` or `false`) from its effect (the changed record);
- protect a record with a guard clause: all the checks first, then all the changes;
- leave the whole record unchanged when an operation is refused;
- predict the result and the state of a record after a series of accepted and refused operations;
- choose data that reveal a change made before the check.

## 1. Prepare the project

In `cpp-workspace`, create a folder `lesson_9_2` and copy `main.cpp` and `CMakeLists.txt` into it from the original `lesson_05_first_program`. You type the program from section 2 into `main.cpp` in that folder. You know the `Product` type from lesson 9.1.

## 2. Issuing goods

<!-- example: issue -->
```cpp
#include <iostream>
#include <string>

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

int main() {
    Product tea{"Tea", 8, 8, 6};

    std::cout << "Product: " << tea.name << "\n";
    std::cout << "Before: " << tea.stock << "\n";

    const bool first_accepted{issue_units(tea, 3)};

    if (first_accepted) {
        std::cout << "Issue 3: accepted\n";
    } else {
        std::cout << "Issue 3: refused\n";
    }

    std::cout << "After first: " << tea.stock << "\n";

    const bool second_accepted{issue_units(tea, 6)};

    if (second_accepted) {
        std::cout << "Issue 6: accepted\n";
    } else {
        std::cout << "Issue 6: refused\n";
    }

    std::cout << "After second: " << tea.stock << "\n";
}
```

**Predict** all six lines, then run the program. In particular: will the second issue be accepted?

<details>
<summary>Standard output</summary>

<!-- output: issue -->
```text
Product: Tea
Before: 8
Issue 3: accepted
After first: 5
Issue 6: refused
After second: 5
```

</details>

- **`Product& product`** lets the function change the existing product (lesson 9.1). The function only reads **`int amount`**, so it gets it by value.
- **The refusal condition** joins two cases with `||`: an amount of 0 or less, and an amount larger than the stock. When either holds, the function returns `false`, and the stock doesn't change.
- **Only after the check** does the function subtract the amount. By then it's known that `amount` doesn't exceed `product.stock`, so the stock won't fall below zero. **`return true;`** means that the operation was accepted and performed.
- **The second call sees the state after the first:** 5 units are left, so 6 is too many.
- **`main` stores the result of each call in a `bool` variable.** The function runs once, when the variable is initialised: it changes the record or not, and returns the result. The `if` then only checks the stored result.
- **The function prints nothing.** It reports a refusal through its result, and the report belongs to `main`.

## 3. The result and the effect

The function `issue_units` has an **effect**, the changed record, and a **result**, the `true` or `false` passed back to the call site. These are two independent features.

| Function | Effect |
|---|---|
| `void receive_delivery(Product& product, int delivered)` | changes the record, returns no value |
| `bool issue_units(Product& product, int amount)` | may change the record, and reports success |
| a function with a `const Product&` parameter and a `Product` result | creates a new value, doesn't change the original through the parameter |

- **`void` isn't required for a function that changes a record.** The delivery from lesson 9.1 was always accepted, so there was nothing to report. An issue may be refused.
- **`bool` is the type of the result, not a new way of passing the object.** The object still goes into the function through `&`.
- **A new value instead of changing the existing one is still often a good design,** for example when the original must stay unchanged (lesson 8.5).

**The agreement in this lesson:** `true` means that the operation was accepted and performed. `false` means a refusal, after which **all the fields of the record are unchanged**. This is the agreement of our functions, not the meaning of every `bool` in C++: `is_even` from lesson 5.3 returns `bool` too, but it only answers a question.

We accept only positive amounts, so `true` always means a real change, and an amount of 0 is refused. In lesson 8.2, zero new reservations were accepted as an update without a change. That's a valid agreement too, just a different one.

## 4. A guard clause protects the record

<!-- fragment -->
```cpp
if (amount <= 0 || amount > product.stock) {
    return false;
}
```

This is a guard clause, known from lesson 5.4. When the condition holds, the function ends, `product.stock -= amount;` doesn't run, and the caller's object stays unchanged. It isn't a new C++ construct. What's new is its job: the guard clause protects the state of an object passed by `&`.

**Predict on paper.** The product now has 5 units, as after the program in section 2. A program calls `issue_units(tea, 0)`, `issue_units(tea, 5)` and `issue_units(tea, 1)`, in that order. For each call, write down: what `tea.stock` is before it, the value of both conditions, which `return` runs, what the result is, and what `tea.stock` is after the call.

<details>
<summary>The answer, and a program that checks it</summary>

| Call | `tea.stock` before | `amount <= 0` | `amount > product.stock` | Which `return` | Result | `tea.stock` after |
|---|---:|---|---|---|---|---:|
| `issue_units(tea, 0)` | 5 | `true` | **not checked** | `return false;` | `false` | 5 |
| `issue_units(tea, 5)` | 5 | `false` | `false` | `return true;` | `true` | 0 |
| `issue_units(tea, 1)` | 0 | `false` | `true` | `return false;` | `false` | 0 |

- **0 units:** the left side of `||` is true, so the right side isn't evaluated (lesson 3.4). A refusal.
- **5 units of 5:** issuing the whole stock is allowed, because 5 isn't greater than 5. The stock falls to 0.
- **1 unit of 0:** not enough goods. The refusal doesn't change the stock, which is already 0.

This program makes those three calls. Running it is optional.

<!-- example: issue_boundaries -->
```cpp
#include <iostream>
#include <string>

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

int main() {
    Product tea{"Tea", 5, 8, 6};

    std::cout << "Before: " << tea.stock << "\n";

    const bool zero_accepted{issue_units(tea, 0)};

    if (zero_accepted) {
        std::cout << "Issue 0: accepted\n";
    } else {
        std::cout << "Issue 0: refused\n";
    }

    std::cout << "After: " << tea.stock << "\n";

    const bool all_accepted{issue_units(tea, 5)};

    if (all_accepted) {
        std::cout << "Issue 5: accepted\n";
    } else {
        std::cout << "Issue 5: refused\n";
    }

    std::cout << "After: " << tea.stock << "\n";

    const bool one_accepted{issue_units(tea, 1)};

    if (one_accepted) {
        std::cout << "Issue 1: accepted\n";
    } else {
        std::cout << "Issue 1: refused\n";
    }

    std::cout << "After: " << tea.stock << "\n";
}
```

<!-- output: issue_boundaries -->
```text
Before: 5
Issue 0: refused
After: 5
Issue 5: accepted
After: 0
Issue 1: refused
After: 0
```

</details>

## 5. All or nothing

**First we check all the conditions, and only then do we change the state.**

When an operation changes two fields, a wrong layout is easy to write:

1. Change the first field.
2. Check the condition.
3. If the condition isn't met, return `false`.

Such a function reports a refusal, but it leaves the record **partly changed**: one field is already different. The caller gets `false` and assumes that nothing changed.

The correct layout:

1. Check all the requirements.
2. If any of them isn't met, end the function without any change.
3. If all of them are met, make all the planned changes.
4. Return `true`.

This is the **"all or nothing"** rule: an operation changes all the fields it's meant to change, or none of them. In lesson 8.2, `main` enforced it; now the function does, so every call is protected.

## 6. Mission: a city travel card

A program stores one record of a city travel card: its name, the number of credits available, and the number of rides paid. Credits are points by convention, not money. At each attempt to pay for a ride, the program decides whether to accept it.

**Data:** the card `City Pass` with 20 credits and 2 rides. Then three attempts to pay, in this order: 7, 15 and 13 credits.

**Rules:**

- At the start, the balance and the number of rides are non-negative. The fare of a ride is a whole number.
- A payment is **accepted** only when the fare is greater than zero and the balance covers the whole fare, including exactly. An accepted payment lowers the balance by exactly the fare and raises the number of rides by 1.
- In every other situation the payment is **refused**. A fare of 0 and a negative fare are invalid requests. A refused payment changes no field: the program never takes part of a fare, and the balance is never negative.
- The card's name never changes.

**Requirements:**

- The program defines its own type with three fields: a name (`std::string`), a balance of credits (`int`) and a number of rides (`int`). You choose the names of the type and the fields.
- There's **one** object of that type in `main`. The program doesn't create new cards for later attempts.
- The program has one function of your own that tries to pay for one ride: it gets the existing record and the fare (`int`) and returns `bool`, `true` for an accepted payment and `false` for a refused one. It prints nothing and reads nothing from the input. You choose the names of the function and its parameters.
- `main` calls this function **three times for the same object**: for 7, 15 and 13. After each call it prints the result of the attempt, chosen with an `if` based on the function's result, and the current state of the card.
- The program prints exactly eight lines, as in the example below. The words `credits` and `rides` always have the same form, whatever the number.
- The program reads nothing from the input.

In `cpp-workspace`, create a folder `city_pass`, copy `CMakeLists.txt` into it from the original `lesson_05_first_program`, create an empty `main.cpp`, and write the program yourself.

For the data above, the standard output must be:

<!-- output: city_pass -->
```text
Card: City Pass
Before: 20 credits, 2 rides
Fare 7: accepted
After first: 13 credits, 3 rides
Fare 15: refused
After second: 13 credits, 3 rides
Fare 13: accepted
After third: 0 credits, 4 rides
```

The second attempt is refused, because only 13 credits are left after the first. The third uses up the whole remaining balance.

**This isn't issuing goods with other names:** an accepted payment changes two fields. You have to decide yourself:

1. how to name the type, its fields and the function;
2. why the object in `main` has no `const`, and why the record parameter has `&`;
3. how to pass the fare;
4. why the function returns `bool`, not `void`;
5. which conditions cause a refusal, and how to write them;
6. why these conditions must be checked before any change;
7. which two fields an accepted payment changes, and which one the function doesn't touch;
8. how to make a refusal leave the record exactly as it was;
9. how `main` receives the result of each attempt;
10. why each later attempt works on the balance left by the previous one.

**Before you write the program**, prepare a table of cases: the data from the requirements, a fare of 1, a fare equal to the balance, a fare 1 above the balance, a fare of 0, a negative fare, an empty balance, two accepted payments in a row, and a refusal followed by an accepted payment. For each attempt, write down the result, the balance and the number of rides.

**Then** run the program for the data from the requirements and for one variant that starts with two refusals, for example: a balance of 10, 0 rides, fares 0, 11 and 10. Change only the data while doing so. All the cases of the full check list are checked automatically.

### Success criterion

- The program builds as C++20 and, for the data from the requirements, prints exactly the eight lines shown above.
- The function gets the record through `&` and the fare by value, returns `bool`, and prints and reads nothing.
- All the checks stand before the changes. On a refusal no field changes, and on an accepted payment exactly two change.
- All three calls concern the same object, and `main` chooses `accepted` or `refused` based on the function's result.
- The table of cases was ready before you ran the program.
- You can explain why the conditions are checked before the fields change.

When the result matches, you can save the project in Git, as in lesson 1.5.

<details>
<summary>Hint 1</summary>

Should the payment be accepted in every situation? What should happen to the record when there aren't enough credits?

</details>

<details>
<summary>Hint 2</summary>

The function must answer `true` or `false`. First decide whether the operation is allowed, and only then change the state of the card.

</details>

<details>
<summary>Hint 3</summary>

For an accepted payment, change the balance and the number of rides. For a refusal, end the function without changing any field. The next call works with the state left by the previous one.

</details>

<details>
<summary>The full list of check cases: open after preparing your own table</summary>

The "After each attempt" column gives the result, followed by the balance and the number of rides.

| | Name | At the start | Fares | After each attempt | What it checks |
|---|---|---|---|---|---|
| A | `City Pass` | 20 credits, 2 rides | 7, 15, 13 | `accepted` 13/3, `refused` 13/3, `accepted` 0/4 | the data from the requirements: an acceptance, a refusal, using up the whole balance |
| B | `Student` | 10 credits, 0 rides | 1 | `accepted` 9/1 | the lowest positive fare |
| C | `Weekend` | 10 credits, 0 rides | 10 | `accepted` 0/1 | a fare equal to the balance |
| D | `Night` | 10 credits, 0 rides | 11 | `refused` 10/0 | a fare 1 above the balance |
| E | `Day Card` | 10 credits, 2 rides | 0, -3 | `refused` 10/2, `refused` 10/2 | a fare of 0 and a negative fare, two refusals in a row |
| F | `Empty` | 0 credits, 4 rides | 1, 0 | `refused` 0/4, `refused` 0/4 | an empty balance |
| G | `Commuter` | 12 credits, 1 ride | 4, 5 | `accepted` 8/2, `accepted` 3/3 | two accepted payments in a row |
| H | `City Pass` | 10 credits, 0 rides | 0, 11, 10 | `refused` 10/0, `refused` 10/0, `accepted` 0/1 | refusals don't spoil a later accepted payment |

In every case the card's name after the attempts is the same as at the start. A correct balance alone doesn't prove that the program works: for each attempt, check the result and the number of rides as well.

**Automatic tests and your own tries.** All the cases are checked automatically by a check program. It has the same type and the same function as the reference solution, but it reads the starting state and the fares from the input, and prints the result and the state after each attempt. It's only a checking tool, not part of the mission: in the mission the data are written in the code, and there are exactly three attempts. The check program and its results are in [Example solutions](#example-solutions), because they contain the solution.

</details>

An example solution is in [Example solutions](#example-solutions).

## 7. Find the bug: a change before the refusal

Do this task **after the mission**: the program below is meant to take one payment from a card, like your program. You can type the program or copy it into `main.cpp`.

<details>
<summary>The program to check: open after writing your own program</summary>

<!-- example: fare_order_bug -->
```cpp
#include <iostream>
#include <string>

struct TravelCard {
    std::string name;
    int credits;
    int rides;
};

bool pay_fare(TravelCard& card, int fare) {
    ++card.rides;

    if (fare <= 0 || fare > card.credits) {
        return false;
    }

    card.credits -= fare;
    return true;
}

int main() {
    TravelCard card{"City Pass", 20, 2};
    const int fare{7};

    std::cout << "Card: " << card.name << "\n";
    std::cout << "Before: " << card.credits << " credits, " << card.rides << " rides\n";

    const bool paid{pay_fare(card, fare)};

    if (paid) {
        std::cout << "Fare " << fare << ": accepted\n";
    } else {
        std::cout << "Fare " << fare << ": refused\n";
    }

    std::cout << "After: " << card.credits << " credits, " << card.rides << " rides\n";
}
```

1. **Predict** the result and the state of the card for the data in the program, a fare of 7.
2. Run the program. Does the result look correct?
3. Change `fare` to a fare that the function should refuse. Write down the correct outcome for your value: the result of the attempt, the balance and the number of rides.
4. For your value, trace both fields of the record line by line in the function. Then run the program.
5. Point to the field that changed too early.
6. Explain why returning `false` isn't enough to make the refusal correct.
7. Fix the order of the checks and the changes.
8. Run the fixed program for your value. Predict what it prints for a fare of 7, and explain why the fix doesn't change the outcome of an accepted payment.
9. Use this example to justify the "all or nothing" rule.

</details>

The results, an example value and the fixed program are in [Example solutions](#example-solutions).

## 8. When something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| A refused payment raises the number of rides | The function changes a field before checking the conditions (section 7). | Check all the conditions first, then change both fields. |
| The balance is negative | The function doesn't compare the fare with the balance, or does so after subtracting the fare. | Compare the fare with the balance before any change. |
| A fare equal to the balance is refused | The refusal condition uses `>=` instead of `>`. | A balance equal to the fare is enough. Refuse only when the fare is greater than the balance. |
| A fare of 0 or a negative fare is accepted | The function doesn't check whether the fare is greater than zero. | Add that condition to the guard clause. |
| `accepted` or `refused` doesn't match the state of the card | `main` doesn't use the function's result, or has the `if` branches swapped. | Store the result of the call in a `bool` variable and choose the text based on it. |
| One attempt changes the balance twice | The function is called twice: once on its own and once in the `if` condition. Each call is a separate attempt to pay. | Call the function once, store the result, and check the stored value. |
| A later attempt works from the starting balance | The call concerns a copy, or the function gets the card by value (lesson 9.1). | Call the function for the same object, passed through `&`. |
| The warning `non-void function does not return a value in all control paths` | After an accepted payment the function reaches its end without `return true;`. Such a call has undefined behaviour (lesson 5.4). | Add `return true;` after changing the fields. |

## 9. Explain

Answer in your own words, preferably in writing. Only then compare with the example answers.

1. Why can a function that changes a record return `bool`? What is its result, and what is its effect?
2. What do `true` and `false` mean in this lesson? Does every C++ function that returns `bool` have this meaning?
3. What must a function do so that `false` means a refusal without any change?
4. Why is a fare of 0 refused in the mission? How is that different from zero new reservations in lesson 8.2?
5. Why must the balance be checked before it's lowered?
6. What does "all or nothing" mean for an operation that changes two fields?
7. A function raises the ride count before checking the fare, but still returns `false` on a refusal. Why is that a bug?
8. Why does the second attempt in the mission see the balance after the first, and why can the third succeed despite the earlier refusal?
9. Why does the function print nothing, and why does `main` store its result in a variable?
10. How do a function that only reads a record, a function that changes it, and a function that returns a new value differ? When would a new value be better in the mission?

<details>
<summary>Example answers</summary>

1. Because changing an object and returning a value are two independent features of a function. The effect is the changed record, which `main` sees after the call. The result is `true` or `false`: whether the operation was accepted.
2. `true`: the operation was accepted and performed according to the agreement. `false`: the operation was refused, and all the fields of the record are unchanged. This is the agreement of our functions, not a rule of C++. Other functions returning `bool` may only answer a question, like `is_even` from lesson 5.3.
3. It must check all the conditions before changing any field, and end with `return false;` on a refusal. Then no change has time to happen.
4. Because the mission's agreement says that a ride for 0 credits is an invalid request: accepting it would add a ride without a payment. In lesson 8.2, zero reservations were accepted as an update without a change. That's a different agreement, also valid. In the mission `true` always means a real change.
5. Because only before the change is it known whether the balance covers the whole fare. After the subtraction it would be too late: the balance could already be negative, and the card in an invalid state.
6. That an accepted payment changes both fields, the balance and the number of rides, and a refused one changes neither. It never changes just one.
7. Because the refusal then leaves the record partly changed: the number of rides grows although no fare was taken. `false` reports the refusal correctly, but the caller assumes that nothing changed, while the state of the card is already different.
8. Because all the calls get the same object through `&`. After the first payment the balance is 13, so 15 is too much. The refusal changed nothing, so the third attempt still sees 13, and 13 isn't greater than 13.
9. The function is responsible for the rule and the change, and the report belongs to `main`. That way the same function can be called in a program with a different report, as in the check program. The variable remembers the result of the only call: if `main` called the function again to check the result, it would make a second attempt to pay.
10. A function that only reads gets `const&` and changes nothing. A function that changes gets `&` and changes the existing record. A function that returns a new value gets `const&` and leaves the original unchanged. In the mission a new value would be better for a preview, for example: if the program had to show the state of the card after a payment before really taking it.

</details>

## Summary

- A function with a `&` parameter can change a record only when the conditions are met, and return `bool`. The result tells whether the operation was accepted, and the effect is the changed record.
- In this lesson `true` means an operation that was accepted and performed, and `false` a refusal after which all the fields are unchanged. This is the agreement of our functions, not the meaning of every `bool`.
- All or nothing: the guard clause with `return false;` stands before all the changes. A change before the check can leave a record partly changed despite `false`.
- `main` stores the result of each call and prints the report based on it. Later calls on the same object start from the state left by the previous ones, also after a refusal.

## What's next

In this lesson a function changed one record. In the next lesson you'll change many records stored in a vector, through a reference: [Lesson 9.3: Changing the elements of a vector through a reference](lesson_03_changing_vector_elements.en.md).

---

## Example solutions

Look here **after your own attempt**. Your names may differ, as long as the standard output is as required.

<details>
<summary>Section 6: the mission, a city travel card</summary>

<!-- example: city_pass -->
```cpp
#include <iostream>
#include <string>

struct TravelCard {
    std::string name;
    int credits;
    int rides;
};

bool pay_fare(TravelCard& card, int fare) {
    if (fare <= 0 || fare > card.credits) {
        return false;
    }

    card.credits -= fare;
    ++card.rides;
    return true;
}

int main() {
    TravelCard card{"City Pass", 20, 2};
    const int first_fare{7};
    const int second_fare{15};
    const int third_fare{13};

    std::cout << "Card: " << card.name << "\n";
    std::cout << "Before: " << card.credits << " credits, " << card.rides << " rides\n";

    const bool first_paid{pay_fare(card, first_fare)};

    if (first_paid) {
        std::cout << "Fare " << first_fare << ": accepted\n";
    } else {
        std::cout << "Fare " << first_fare << ": refused\n";
    }

    std::cout << "After first: " << card.credits << " credits, " << card.rides << " rides\n";

    const bool second_paid{pay_fare(card, second_fare)};

    if (second_paid) {
        std::cout << "Fare " << second_fare << ": accepted\n";
    } else {
        std::cout << "Fare " << second_fare << ": refused\n";
    }

    std::cout << "After second: " << card.credits << " credits, " << card.rides << " rides\n";

    const bool third_paid{pay_fare(card, third_fare)};

    if (third_paid) {
        std::cout << "Fare " << third_fare << ": accepted\n";
    } else {
        std::cout << "Fare " << third_fare << ": refused\n";
    }

    std::cout << "After third: " << card.credits << " credits, " << card.rides << " rides\n";
}
```

1. **The record through `&`,** because the function must change the existing card, not its own copy.
2. **`bool`, not `void`,** because a payment may be refused, and `main` must know that to print `accepted` or `refused`.
3. **`false`** means: the payment was refused, and no field changed.
4. **`true`** means: the payment was accepted, the balance is lower by exactly the fare, and there's one more ride.
5. **A positive fare,** because a fare of 0 would add a ride without a payment, and a negative fare would raise the balance. Both are invalid requests.
6. **The balance before taking the fare,** because only then is it known whether it covers the whole fare. After the subtraction the balance could already be negative.
7. **The order:** first the guard clause, then both changes, and `return true;` at the end. The order of the two changes after the check doesn't matter.
8. **Both fields unchanged on a refusal,** because `return false;` ends the function before any change runs.
9. **The number of rides can't be raised before the check,** because a refusal would leave the record partly changed, as in the diagnostic of section 7.
10. **The second attempt sees the balance after the first,** because both concern the same object, `card`. 15 is greater than 13, so it's a refusal.
11. **The third attempt can succeed,** because the refusal changed nothing: the balance is still 13, and 13 isn't greater than 13.
12. **No new object for each attempt,** because the card is one thing whose state changes over time. A new card with the starting values would lose the earlier payments.
13. **The function prints nothing,** because it's responsible only for the rule and the change. The report belongs to `main`, so the same function works in a program with a different report, like the check program below.
14. **When a new value would be better:** if the program had to show a preview, the state of the card after a payment without taking it from the card, or compare the state before and after. Then a function with `const&` that returns a new record would fit, as in lesson 8.5, or a copy made before the change, as in lesson 8.2.

**Other correct solutions:**

- `card.rides += 1;` instead of `++card.rides;`;
- the changes of the two fields in the opposite order, still after the guard clause;
- two separate guard clauses, one for a fare of 0 or less and one for a balance that's too low: both before the changes;
- the fares written directly in the calls and in the texts. Then, though, each fare has to be changed in two places;
- the call in the condition itself, `if (pay_fare(card, first_fare))`: the function also runs once, but the change of the card is then hidden in the condition. A variable holding the result shows it more clearly.

**The check program** checks all the cases of the check list. The type and the function are the same as above. The difference is in `main`: the program reads the name, the starting state and the fares from the input, calls the function for each fare on the same object, prints the result and the state after each attempt, and the name at the end. It reads the input in the same way as the check program of lesson 9.1: the name with `std::getline`, the numbers with `>>`, and the fares first into a vector of `int`, so that it can check the reading before anything changes. The mission needs neither the input nor a vector.

<!-- example: city_pass_check -->
```cpp
#include <iostream>
#include <string>
#include <vector>

struct TravelCard {
    std::string name;
    int credits;
    int rides;
};

bool pay_fare(TravelCard& card, int fare) {
    if (fare <= 0 || fare > card.credits) {
        return false;
    }

    card.credits -= fare;
    ++card.rides;
    return true;
}

int main() {
    std::string name{};
    int credits{0};
    int rides{0};
    int count{0};
    std::vector<int> fares{};

    std::getline(std::cin, name);
    std::cin >> credits;
    std::cin >> rides;
    std::cin >> count;

    for (int number{1}; number <= count; ++number) {
        int fare{0};
        std::cin >> fare;
        fares.push_back(fare);
    }

    if (std::cin.fail()) {
        std::cout << "Input could not be read\n";
    } else {
        TravelCard card{name, credits, rides};

        std::cout << "Before: " << card.credits << " credits, " << card.rides << " rides\n";

        for (const int fare : fares) {
            const bool paid{pay_fare(card, fare)};

            if (paid) {
                std::cout << "Fare " << fare << ": accepted\n";
            } else {
                std::cout << "Fare " << fare << ": refused\n";
            }

            std::cout << "After: " << card.credits << " credits, " << card.rides << " rides\n";
        }

        std::cout << "Card: " << card.name << "\n";
    }
}
```

Each case is the card's name on the first line, then the balance, the number of rides, the number of attempts and the fares, in the order of the check list, from A to H.

<!-- input: city_pass_check -->
```text
City Pass
20
2
3
7
15
13
```

<!-- output: city_pass_check -->
```text
Before: 20 credits, 2 rides
Fare 7: accepted
After: 13 credits, 3 rides
Fare 15: refused
After: 13 credits, 3 rides
Fare 13: accepted
After: 0 credits, 4 rides
Card: City Pass
```

<!-- input: city_pass_check -->
```text
Student
10
0
1
1
```

<!-- output: city_pass_check -->
```text
Before: 10 credits, 0 rides
Fare 1: accepted
After: 9 credits, 1 rides
Card: Student
```

<!-- input: city_pass_check -->
```text
Weekend
10
0
1
10
```

<!-- output: city_pass_check -->
```text
Before: 10 credits, 0 rides
Fare 10: accepted
After: 0 credits, 1 rides
Card: Weekend
```

<!-- input: city_pass_check -->
```text
Night
10
0
1
11
```

<!-- output: city_pass_check -->
```text
Before: 10 credits, 0 rides
Fare 11: refused
After: 10 credits, 0 rides
Card: Night
```

<!-- input: city_pass_check -->
```text
Day Card
10
2
2
0
-3
```

<!-- output: city_pass_check -->
```text
Before: 10 credits, 2 rides
Fare 0: refused
After: 10 credits, 2 rides
Fare -3: refused
After: 10 credits, 2 rides
Card: Day Card
```

<!-- input: city_pass_check -->
```text
Empty
0
4
2
1
0
```

<!-- output: city_pass_check -->
```text
Before: 0 credits, 4 rides
Fare 1: refused
After: 0 credits, 4 rides
Fare 0: refused
After: 0 credits, 4 rides
Card: Empty
```

<!-- input: city_pass_check -->
```text
Commuter
12
1
2
4
5
```

<!-- output: city_pass_check -->
```text
Before: 12 credits, 1 rides
Fare 4: accepted
After: 8 credits, 2 rides
Fare 5: accepted
After: 3 credits, 3 rides
Card: Commuter
```

<!-- input: city_pass_check -->
```text
City Pass
10
0
3
0
11
10
```

<!-- output: city_pass_check -->
```text
Before: 10 credits, 0 rides
Fare 0: refused
After: 10 credits, 0 rides
Fare 11: refused
After: 10 credits, 0 rides
Fare 10: accepted
After: 0 credits, 1 rides
Card: City Pass
```

</details>

<details>
<summary>Section 7: the results before the fix, and the fixed program</summary>

Before the fix, for a fare of 7:

<!-- output: fare_order_bug -->
```text
Card: City Pass
Before: 20 credits, 2 rides
Fare 7: accepted
After: 13 credits, 3 rides
```

- **For an accepted payment the result is correct,** because both changes run anyway: the number of rides grows by 1, and the balance falls by 7. Only their order differs, and the report doesn't show it.
- **Data that reveal the bug:** any fare that the function should refuse. For example 25, more than the balance. The correct outcome is `refused` and an unchanged state: 20 credits, 2 rides. The buggy program prints:

<!-- example: fare_order_revealed -->
```cpp
#include <iostream>
#include <string>

struct TravelCard {
    std::string name;
    int credits;
    int rides;
};

bool pay_fare(TravelCard& card, int fare) {
    ++card.rides;

    if (fare <= 0 || fare > card.credits) {
        return false;
    }

    card.credits -= fare;
    return true;
}

int main() {
    TravelCard card{"City Pass", 20, 2};
    const int fare{25};

    std::cout << "Card: " << card.name << "\n";
    std::cout << "Before: " << card.credits << " credits, " << card.rides << " rides\n";

    const bool paid{pay_fare(card, fare)};

    if (paid) {
        std::cout << "Fare " << fare << ": accepted\n";
    } else {
        std::cout << "Fare " << fare << ": refused\n";
    }

    std::cout << "After: " << card.credits << " credits, " << card.rides << " rides\n";
}
```

<!-- output: fare_order_revealed -->
```text
Card: City Pass
Before: 20 credits, 2 rides
Fare 25: refused
After: 20 credits, 3 rides
```

| Moment | `card.credits` | `card.rides` |
|---|---:|---:|
| before the call | 20 | 2 |
| after `++card.rides;` | 20 | **3** |
| the condition: 25 is greater than 20, `return false;` | 20 | 3 |
| after returning to `main` | 20 | 3 |

- **The field changed too early:** the number of rides. The function raises it before it knows whether the payment is allowed.
- **Why `false` isn't enough:** the result reports the refusal correctly, but the record is already partly changed. The caller assumes that nothing changed after `false`, while the card has a ride that nobody paid for. Every other refusal works the same way, for example a fare of 0 or a negative fare.
- **The fix:** move `++card.rides;` after the guard clause, next to `card.credits -= fare;`. Then all the checks stand before all the changes.

<!-- example: fare_order_fixed -->
```cpp
#include <iostream>
#include <string>

struct TravelCard {
    std::string name;
    int credits;
    int rides;
};

bool pay_fare(TravelCard& card, int fare) {
    if (fare <= 0 || fare > card.credits) {
        return false;
    }

    card.credits -= fare;
    ++card.rides;
    return true;
}

int main() {
    TravelCard card{"City Pass", 20, 2};
    const int fare{25};

    std::cout << "Card: " << card.name << "\n";
    std::cout << "Before: " << card.credits << " credits, " << card.rides << " rides\n";

    const bool paid{pay_fare(card, fare)};

    if (paid) {
        std::cout << "Fare " << fare << ": accepted\n";
    } else {
        std::cout << "Fare " << fare << ": refused\n";
    }

    std::cout << "After: " << card.credits << " credits, " << card.rides << " rides\n";
}
```

<!-- output: fare_order_fixed -->
```text
Card: City Pass
Before: 20 credits, 2 rides
Fare 25: refused
After: 20 credits, 2 rides
```

For a fare of 7 the fixed program prints the same as before the fix: `Fare 7: accepted` and `After: 13 credits, 3 rides`. For an accepted payment both versions make the same two changes, so such a case doesn't tell them apart. That's why checking the order needs a refusal.

**All or nothing:** an accepted payment changes both fields, a refused one neither. On a refusal, the buggy version changed one field of two, a state that the agreement doesn't allow.

</details>

**Previous lesson:** [Lesson 9.1: A function changes an existing record](lesson_01_a_function_changes_a_record.en.md) · **Next lesson:** [Lesson 9.3: Changing the elements of a vector through a reference](lesson_03_changing_vector_elements.en.md) · [Course overview](../../README.en.md)

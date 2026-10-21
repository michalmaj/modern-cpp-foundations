# Lesson 3.4: Combining conditions (`&&`, `||`, `!`)

[Polski](lesson_04_combining_conditions.md) · **English** · [Course overview](../../README.en.md)

> **Module 3, lesson 4** · about 60–75 minutes
> **You need:** the `cpp-workspace` folder and the original `lesson_05_first_program` project, as before. You don't need the debugger in this lesson.
> **Pilot version.** The programs in this lesson are checked automatically on Windows, Ubuntu and macOS, including with the given input data.

## Before you start

This lesson assumes that after lessons 3.1–3.3:

- you write `if`, `else` and `else if` chains, always with braces;
- you store the result of a comparison in a `bool` variable and use it as a condition;
- you know that a stored `bool` value doesn't change by itself when the data changes later;
- you check every limit from both sides.

## The situation

So far, each condition asked one question: is the number less than 5, is the day Saturday. Requirements often combine several questions, though: "from 1 to 10", "on Saturday **or** Sunday", "**not** on the cleaning day". Today you'll meet three operators that combine conditions: `&&` ("and"), `||` ("or") and `!` ("not"). You'll also learn to turn requirements written in words into readable conditions in code.

After this lesson you will:

- explain the meaning of `&&`, `||` and `!`, and choose the operator that fits a requirement;
- check whether a number lies in a range;
- know that `||` gives "yes" also when both conditions are satisfied;
- write combined conditions readably, with named `bool` variables and parentheses;
- understand when the right-hand side of `&&` and `||` isn't evaluated at all;
- find a bug in a combined condition, and choose the test cases that reveal it.

## 1. Prepare the project

In `cpp-workspace`, create a folder `lesson_3_4` and copy `main.cpp` and `CMakeLists.txt` into it from the original `lesson_05_first_program`. You type the programs from sections 2–7 into that folder's `main.cpp`.

## 2. A number in a range: `&&`

The program must check whether a number lies in the range **from 1 to 10 inclusive**. You already know both comparisons it needs: `number >= 1` and `number <= 10`. How do you write a condition that is satisfied only when **both** comparisons answer "yes"?

<!-- example: range_check -->
```cpp
#include <iostream>

int main() {
    int number{0};

    std::cout << "Enter a number:\n";
    std::cin >> number;

    const bool in_range{number >= 1 && number <= 10};

    if (in_range) {
        std::cout << "In range\n";
    } else {
        std::cout << "Out of range\n";
    }
}
```

- **`&&`** is the logical **"and"**. The whole expression `number >= 1 && number <= 10` is true only when **both** comparisons are true. If just one is false, the whole thing is false.
- `in_range` is a `bool` variable that stores the result of the whole expression. `if (in_range)` uses it as in lesson 3.2.
- A logical operator changes nothing: `number` has the same value after the comparison.

In C++ a range isn't written as at school, as one chain of inequalities with the number in the middle. You have to join **two** comparisons explicitly with `&&`, as above.

**Predict** what the program prints for 0, 1, 5, 10 and 11. Write down your answers, then run it five times.

<!-- input: range_check -->
```text
0
```

<details>
<summary>The standard output for 0</summary>

<!-- output: range_check -->
```text
Enter a number:
Out of range
```

</details>

<!-- input: range_check -->
```text
1
```

<details>
<summary>The standard output for 1</summary>

<!-- output: range_check -->
```text
Enter a number:
In range
```

</details>

<!-- input: range_check -->
```text
5
```

<details>
<summary>The standard output for 5</summary>

<!-- output: range_check -->
```text
Enter a number:
In range
```

</details>

<!-- input: range_check -->
```text
10
```

<details>
<summary>The standard output for 10</summary>

<!-- output: range_check -->
```text
Enter a number:
In range
```

</details>

<!-- input: range_check -->
```text
11
```

<details>
<summary>The standard output for 11</summary>

<!-- output: range_check -->
```text
Enter a number:
Out of range
```

</details>

0 and 11 are ordinary numbers, read correctly. They simply **don't meet the condition**: they lie out of the range from 1 to 10. For 0 the first comparison is false, and for 11 the second. In both cases that's enough to make the whole `&&` false.

## 3. One condition is enough: `||`

Classes take place **on Saturday or Sunday**. Days of the week are numbered: 1 is Monday, …, 6 is Saturday, 7 is Sunday.

<!-- example: weekend_check -->
```cpp
#include <iostream>

int main() {
    int day{0};

    std::cout << "Enter day (1-7):\n";
    std::cin >> day;

    const bool is_weekend{day == 6 || day == 7};

    if (is_weekend) {
        std::cout << "Weekend\n";
    } else {
        std::cout << "Weekday\n";
    }
}
```

**Predict** the result for the days 5, 6 and 7, then check.

<!-- input: weekend_check -->
```text
5
```

<!-- output: weekend_check -->
```text
Enter day (1-7):
Weekday
```

<!-- input: weekend_check -->
```text
6
```

<!-- output: weekend_check -->
```text
Enter day (1-7):
Weekend
```

<!-- input: weekend_check -->
```text
7
```

<!-- output: weekend_check -->
```text
Enter day (1-7):
Weekend
```

- **`||`** is the logical **"or"**. The whole expression is true when **at least one** condition is true, and false only when **both** are false.
- `||` doesn't pick the "better" condition, and changes nothing. It only answers "yes" or "no" for the whole thing.

**"Or" includes "both at once".** In the weekend example a day can't be both 6 and 7, so you don't see it. This program shows it directly: you can come in with a ticket **or** by being on the guest list.

<!-- example: entry_check -->
```cpp
#include <iostream>
#include <string>

int main() {
    std::string ticket_answer{""};
    std::string list_answer{""};

    std::cout << "Do you have a ticket? (yes/no)\n";
    std::cin >> ticket_answer;
    std::cout << "Are you on the guest list? (yes/no)\n";
    std::cin >> list_answer;

    const bool has_ticket{ticket_answer == "yes"};
    const bool on_guest_list{list_answer == "yes"};

    if (has_ticket || on_guest_list) {
        std::cout << "Come in\n";
    } else {
        std::cout << "Sorry, no entry\n";
    }
}
```

**Predict** the result for four combinations: a ticket but not on the list, no ticket but on the list, **both a ticket and the list**, and neither.

<!-- input: entry_check -->
```text
yes
no
```

<!-- output: entry_check -->
```text
Do you have a ticket? (yes/no)
Are you on the guest list? (yes/no)
Come in
```

<!-- input: entry_check -->
```text
no
yes
```

<!-- output: entry_check -->
```text
Do you have a ticket? (yes/no)
Are you on the guest list? (yes/no)
Come in
```

<!-- input: entry_check -->
```text
yes
yes
```

<details>
<summary>The standard output for "yes" and "yes"</summary>

<!-- output: entry_check -->
```text
Do you have a ticket? (yes/no)
Are you on the guest list? (yes/no)
Come in
```

Both conditions are true, so `||` gives "yes". In C++, "or" doesn't mean "one or the other, but not both".

</details>

<!-- input: entry_check -->
```text
no
no
```

<!-- output: entry_check -->
```text
Do you have a ticket? (yes/no)
Are you on the guest list? (yes/no)
Sorry, no entry
```

**`&&` or `||`?** Compare:

| Left condition | Right condition | `left && right` | `left \|\| right` |
|---|---|---|---|
| `true` | `true` | `true` | `true` |
| `true` | `false` | `false` | `true` |
| `false` | `true` | `false` | `true` |
| `false` | `false` | `false` | `false` |

**Choose the operator.** Copy the table and write `&&` or `||` next to each requirement:

| Requirement | Operator |
|---|---|
| The temperature is from 18 to 24 degrees. | |
| The day is Tuesday or Thursday. | |
| The person is at least 18 and has a ticket. | |
| The answer is `yes` or `y`. | |
| The score is from 0 to 100 points. | |

The answers are in [Example solutions](#example-solutions).

## 4. Negation: `!`

Sometimes a requirement says "if **not**". To negate a logical value you use **`!`**, the logical "not":

<!-- example: weekday_notice -->
```cpp
#include <iostream>

int main() {
    int day{0};

    std::cout << "Enter day (1-7):\n";
    std::cin >> day;

    const bool is_weekend{day == 6 || day == 7};

    if (!is_weekend) {
        std::cout << "Not a weekend\n";
    }

    std::cout << "Day checked\n";
}
```

<!-- input: weekday_notice -->
```text
3
```

<!-- output: weekday_notice -->
```text
Enter day (1-7):
Not a weekend
Day checked
```

<!-- input: weekday_notice -->
```text
6
```

<!-- output: weekday_notice -->
```text
Enter day (1-7):
Day checked
```

- `!` reverses a logical value: `!true` gives `false`, and `!false` gives `true`.
- `!is_weekend` reads "not weekend". The result is a **new** logical value, and `is_weekend` doesn't change.
- **`!` isn't `!=`.** The `!=` from lesson 3.2 compares two values ("are they different?"). `!` stands before **one** logical value and reverses it.
- Use `if (!condition)` where the requirement really says "if not …". Avoid double negations: they can usually be written more simply.

## 5. Readable conditions

A swimming pool is open when the water temperature is **from 24 to 28 degrees** and it is **not** Monday, because the pool is cleaned on Mondays. This requirement combines several questions. Instead of writing them in one long condition, give each part a name:

<!-- example: pool_open -->
```cpp
#include <iostream>

int main() {
    int water_temperature_c{0};
    int day{0};

    std::cout << "Enter water temperature:\n";
    std::cin >> water_temperature_c;
    std::cout << "Enter day (1-7):\n";
    std::cin >> day;

    const bool water_ok{water_temperature_c >= 24 && water_temperature_c <= 28};
    const bool is_cleaning_day{day == 1};

    if (water_ok && !is_cleaning_day) {
        std::cout << "Pool open\n";
    } else {
        std::cout << "Pool closed\n";
    }
}
```

<!-- input: pool_open -->
```text
26
3
```

<!-- output: pool_open -->
```text
Enter water temperature:
Enter day (1-7):
Pool open
```

<!-- input: pool_open -->
```text
26
1
```

<!-- output: pool_open -->
```text
Enter water temperature:
Enter day (1-7):
Pool closed
```

<!-- input: pool_open -->
```text
30
3
```

<!-- output: pool_open -->
```text
Enter water temperature:
Enter day (1-7):
Pool closed
```

- `water_ok` and `is_cleaning_day` are **names for parts of the requirement**. The condition `water_ok && !is_cleaning_day` reads almost like a sentence: "the water is fine and it's not the cleaning day".
- Each of these variables **stores a result** calculated at the moment of initialisation, as in lesson 3.2. If the temperature or the day changed later, `water_ok` and `is_cleaning_day` wouldn't recalculate themselves.

**Parentheses.** When a condition combines several groups, show what belongs with what in one of two ways: with named `bool` variables, as above, or with parentheses, for example `(age >= 18 && has_ticket) || on_guest_list`. In C++, `&&` takes precedence over `||`, so it is grouped first, much like multiplication before addition in lesson 2.4. But don't rely on that rule when writing: when one condition contains both `&&` and `||`, always add parentheses so the grouping is visible at once.

## 6. Short-circuit evaluation

`&&` and `||` evaluate their conditions **from the left**, and can finish early:

- **`&&`:** the left condition is evaluated first. If it is **false**, the result of the whole thing is already known (`false`), so the right condition **isn't evaluated**.
- **`||`:** the left condition is evaluated first. If it is **true**, the result of the whole thing is already known (`true`), so the right condition **isn't evaluated**.

This is **short-circuit evaluation**: evaluation stops as soon as the result is certain. The right-hand side is evaluated only when it is needed to settle the result.

**Check yourself.** For each row, answer: must the right condition be evaluated?

| Expression | Value | Is the right condition evaluated? |
|---|---|---|
| `number >= 1 && number <= 10` | `number` is 0 | |
| `number >= 1 && number <= 10` | `number` is 5 | |
| `day == 6 \|\| day == 7` | `day` is 6 | |
| `day == 6 \|\| day == 7` | `day` is 3 | |

The answers are in [Example solutions](#example-solutions).

You can't tell from a `true` or `false` result alone whether both conditions were evaluated. For a `day` of 6, the expression `day == 6 || day == 7` gives `true`, although the comparison `day == 7` never ran. In the next lesson this rule will become practical: it lets you check a value safely before the program uses it.

## 7. Find the bug: the wrong day

The requirement: the program prints `Weekend` on **Saturday or Sunday** (days 6 and 7), and `Weekday` on the other days. This program builds and runs, but doesn't meet the requirement:

<!-- example: weekend_bug -->
```cpp
#include <iostream>

int main() {
    int day{0};

    std::cout << "Enter day (1-7):\n";
    std::cin >> day;

    const bool is_weekend{day == 5 || day == 6};

    if (is_weekend) {
        std::cout << "Weekend\n";
    } else {
        std::cout << "Weekday\n";
    }
}
```

1. Read the requirement and **predict** what the program **should** print for the days 5, 6 and 7.
2. Before running the program, think: which of these days will reveal the bug? Would checking only Saturday be enough?
3. Run the program for 5, 6 and 7.
4. Find the wrong part of the condition.
5. Fix the program.
6. Check all three days again.

The output before the fix, and the fixed program, are in [Example solutions](#example-solutions).

## 8. Mission: weekend workshops

The workshops are for people aged **12 to 17 inclusive**, and take place only on **Saturday** (day 6) **or Sunday** (day 7). The program asks for the age and the number of the day of the week, then prints:

- `Entry allowed`, if **all** the requirements are met;
- `Entry denied` otherwise.

In `cpp-workspace`, create a folder `weekend_workshop`, copy `CMakeLists.txt` into it from the original `lesson_05_first_program`, create an empty `main.cpp`, and write the program on your own. We assume the reads succeed, and the day number is one of the numbers from 1 to 7.

For age 15 and day 6, the standard output must be:

<!-- input: weekend_workshop -->
```text
15
6
```

<!-- output: weekend_workshop -->
```text
Enter age:
Enter day (1-7):
Entry allowed
```

**Before you write the program**, prepare a table of predictions: choose combinations of age and day that check both age limits from both sides, an allowed and a disallowed day, both weekend days, and cases in which only one of the two conditions is met. For each combination, write the expected result.

### Success criteria

- The program builds as C++20, and for each combination prints the requests and exactly one line: `Entry allowed` or `Entry denied`, according to the requirements.
- The age and the day are `int` variables with starting values, read with `std::cin`.
- `&&` checks the age limits, and `||` the weekend days.
- At least one part of the requirement is stored in a named `bool` variable, and an `if`/`else` with braces makes the decision.
- The table of predictions was prepared before running the program.
- You can explain for every combination why it was accepted or rejected.

Once the output matches, you can save the project in Git, as in lesson 1.5.

<details>
<summary>Hint 1</summary>

The requirement has two parts: the age and the day. Store each of them as a separate `bool` variable. Which part needs "and", and which "or"?

</details>

<details>
<summary>Hint 2</summary>

Entry is allowed when both parts are met at once. Which operator joins two `bool` variables in the `if` condition?

</details>

<details>
<summary>The full list of control cases: open after your own attempt</summary>

| Age | Day | Result | What it checks |
|---|---|---|---|
| 11 | 6 | `Entry denied` | age right below the range |
| 12 | 6 | `Entry allowed` | the lower age limit |
| 17 | 7 | `Entry allowed` | the upper age limit, Sunday |
| 18 | 7 | `Entry denied` | age right above the range |
| 15 | 5 | `Entry denied` | a good age, a day outside the weekend |
| 15 | 6 | `Entry allowed` | Saturday |
| 15 | 7 | `Entry allowed` | Sunday |
| 12 | 5 | `Entry denied` | a good age at the limit, the wrong day |

The combination 15 and 6 is checked above, with the mission text.

<!-- input: weekend_workshop -->
```text
11
6
```

<!-- output: weekend_workshop -->
```text
Enter age:
Enter day (1-7):
Entry denied
```

<!-- input: weekend_workshop -->
```text
12
6
```

<!-- output: weekend_workshop -->
```text
Enter age:
Enter day (1-7):
Entry allowed
```

<!-- input: weekend_workshop -->
```text
17
7
```

<!-- output: weekend_workshop -->
```text
Enter age:
Enter day (1-7):
Entry allowed
```

<!-- input: weekend_workshop -->
```text
18
7
```

<!-- output: weekend_workshop -->
```text
Enter age:
Enter day (1-7):
Entry denied
```

<!-- input: weekend_workshop -->
```text
15
5
```

<!-- output: weekend_workshop -->
```text
Enter age:
Enter day (1-7):
Entry denied
```

<!-- input: weekend_workshop -->
```text
15
7
```

<!-- output: weekend_workshop -->
```text
Enter age:
Enter day (1-7):
Entry allowed
```

<!-- input: weekend_workshop -->
```text
12
5
```

<!-- output: weekend_workshop -->
```text
Enter age:
Enter day (1-7):
Entry denied
```

</details>

### Variant: a hint about the schedule

When the day is **not** a weekend day, the program must additionally print `Workshops run only at the weekend`, after the line with the result. For the other days nothing changes. Add this on your own, using `!`, and check the days 5 and 6.

<details>
<summary>The variant's cases: open after your own attempt</summary>

<!-- input: weekend_workshop_variant -->
```text
15
5
```

<!-- output: weekend_workshop_variant -->
```text
Enter age:
Enter day (1-7):
Entry denied
Workshops run only at the weekend
```

<!-- input: weekend_workshop_variant -->
```text
11
6
```

<!-- output: weekend_workshop_variant -->
```text
Enter age:
Enter day (1-7):
Entry denied
```

<!-- input: weekend_workshop_variant -->
```text
15
6
```

<!-- output: weekend_workshop_variant -->
```text
Enter age:
Enter day (1-7):
Entry allowed
```

</details>

Example solutions are in [Example solutions](#example-solutions).

## 9. When something goes differently

| What you see | What it means | What to do |
|---|---|---|
| Values in the range are rejected, or values outside it accepted | `&&` was confused with `\|\|` in the range condition. | A range is "at least the lower limit **and** at most the upper": `&&`. |
| A condition with "or" is never satisfied | `&&` was used instead of `\|\|`. A day can't be both 6 and 7. | When one condition is enough, use `\|\|`. |
| It works for values in the middle, but goes wrong at a limit | A limit is shifted, or `<` was used instead of `<=`. | Check both limits from both sides. |
| A compile error at `&` or `\|` | The logical operators are written with two characters. | Use `&&` and `\|\|`. |
| `!` was confused with `!=` | `!` reverses one logical value, while `!=` compares two values. | Negating a condition is `!condition`, and a comparison is `a != b`. |
| A long condition is hard to read | One expression has too many parts. | Name the parts with `bool` variables, or add parentheses. |

## 10. Explain

Answer in your own words, preferably in writing. Only then compare with the example answer.

**1.** When is an expression with `&&` true, and when is an expression with `||` true?

<details>
<summary>Example answer</summary>

`&&` is true when both conditions are true. `||` is true when at least one condition is true, including when both are.

</details>

**2.** How do you check in C++ whether `number` lies in the range from 1 to 10 inclusive?

<details>
<summary>Example answer</summary>

With two comparisons joined by `&&`: `number >= 1 && number <= 10`.

</details>

**3.** How does `!is_weekend` differ from `day != 6`?

<details>
<summary>Example answer</summary>

`!is_weekend` reverses one logical value: it gives `true` when `is_weekend` is `false`. `day != 6` compares two values and gives `true` when `day` is different from 6.

</details>

**4.** Why, for a `day` of 6, isn't the comparison `day == 7` evaluated in the expression `day == 6 || day == 7`?

<details>
<summary>Example answer</summary>

Because the left condition, `day == 6`, is true, and an `||` with one true condition is already true. The result is known, so the right-hand side doesn't need evaluating.

</details>

**5.** Why is the combination 15 and 5 rejected in the mission, although the age is suitable?

<details>
<summary>Example answer</summary>

Because entry requires both parts to be met at once (`&&`): the age is in range, but day 5 is neither Saturday nor Sunday, so the second part is false.

</details>

## Summary

- **`&&`** ("and") is true when both conditions are true. You write a range as two comparisons joined by `&&`, for example `number >= 1 && number <= 10`.
- **`||`** ("or") is true when at least one condition is true, including when both are.
- **`!`** ("not") reverses one logical value. It isn't `!=`.
- Write combined conditions readably: name the parts of a requirement with `bool` variables, and add parentheses when mixing `&&` and `||`.
- **Short-circuit evaluation:** `&&` doesn't evaluate its right side when the left is false, and `||` when the left is true.
- A value that doesn't meet a condition is usually correctly read data that lies out of range. Check both limits, and each part of a combined condition separately.

## What's next

Your programs now combine several conditions. In lesson 3.5 you'll use this skill to **check data before the program uses it**, for example so that it never divides by zero: [Lesson 3.5: Checking data before calculating](lesson_05_check_before_calculating.en.md).

---

## Example solutions

Look here **after your own attempt**. Your names may differ, as long as the standard output is as required.

<details>
<summary>Section 3: choose the operator</summary>

| Requirement | Operator |
|---|---|
| The temperature is from 18 to 24 degrees. | `&&` |
| The day is Tuesday or Thursday. | `\|\|` |
| The person is at least 18 and has a ticket. | `&&` |
| The answer is `yes` or `y`. | `\|\|` |
| The score is from 0 to 100 points. | `&&` |

</details>

<details>
<summary>Section 6: short-circuit evaluation</summary>

| Expression | Value | Is the right condition evaluated? |
|---|---|---|
| `number >= 1 && number <= 10` | `number` is 0 | no: the left is false, so the whole is false |
| `number >= 1 && number <= 10` | `number` is 5 | yes: the left is true, so the result depends on the right |
| `day == 6 \|\| day == 7` | `day` is 6 | no: the left is true, so the whole is true |
| `day == 6 \|\| day == 7` | `day` is 3 | yes: the left is false, so the result depends on the right |

</details>

<details>
<summary>Section 7: the output before the fix, and the fixed program</summary>

Before the fix, for the days 5, 6 and 7:

<!-- input: weekend_bug -->
```text
5
```

<!-- output: weekend_bug -->
```text
Enter day (1-7):
Weekend
```

<!-- input: weekend_bug -->
```text
6
```

<!-- output: weekend_bug -->
```text
Enter day (1-7):
Weekend
```

<!-- input: weekend_bug -->
```text
7
```

<!-- output: weekend_bug -->
```text
Enter day (1-7):
Weekday
```

Friday (5) is treated as a weekend day, and Sunday (7) as a weekday. Saturday (6) gives the correct result, so testing Saturday alone wouldn't have found the bug: you have to check each of the days the requirement mentions, and the day next to them. The condition should check 6 and 7: `day == 6 || day == 7`. The fixed program is the program from section 3.

</details>

<details>
<summary>Section 8: mission, weekend workshops</summary>

<!-- example: weekend_workshop -->
```cpp
#include <iostream>

int main() {
    int age{0};
    int day{0};

    std::cout << "Enter age:\n";
    std::cin >> age;
    std::cout << "Enter day (1-7):\n";
    std::cin >> day;

    const bool age_allowed{age >= 12 && age <= 17};
    const bool is_weekend{day == 6 || day == 7};

    if (age_allowed && is_weekend) {
        std::cout << "Entry allowed\n";
    } else {
        std::cout << "Entry denied\n";
    }
}
```

- `age_allowed` is the age range: both comparisons must be true, so `&&`.
- `is_weekend` is Saturday or Sunday: one of the two conditions is enough, so `||`.
- Entry requires both parts at once, so the `if` has `age_allowed && is_weekend`. The names make the condition read like the requirement.

</details>

<details>
<summary>Section 8: the variant with a hint about the schedule</summary>

<!-- example: weekend_workshop_variant -->
```cpp
#include <iostream>

int main() {
    int age{0};
    int day{0};

    std::cout << "Enter age:\n";
    std::cin >> age;
    std::cout << "Enter day (1-7):\n";
    std::cin >> day;

    const bool age_allowed{age >= 12 && age <= 17};
    const bool is_weekend{day == 6 || day == 7};

    if (age_allowed && is_weekend) {
        std::cout << "Entry allowed\n";
    } else {
        std::cout << "Entry denied\n";
    }

    if (!is_weekend) {
        std::cout << "Workshops run only at the weekend\n";
    }
}
```

The second decision is separate, as in lesson 3.2: `!is_weekend` is true for every day outside the weekend, whatever the age.

</details>

**Previous lesson:** [Lesson 3.3: Choosing among many possibilities (`else if`)](lesson_03_many_possibilities.en.md) · **Next lesson:** [Lesson 3.5: Checking data before calculating](lesson_05_check_before_calculating.en.md) · [Course overview](../../README.en.md)

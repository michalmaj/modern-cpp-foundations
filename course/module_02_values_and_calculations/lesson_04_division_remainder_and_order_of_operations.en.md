# Lesson 2.4: Division, remainder and the order of operations

[Polski](lesson_04_division_remainder_and_order_of_operations.md) · **English** · [Course overview](../../README.en.md)

> **Module 2, lesson 4** · about 60–75 minutes
> **You need:** the `cpp-workspace` folder and the original `lesson_05_first_program` project, as before. You don't need the debugger in this lesson.
> **Pilot version.** The examples in this lesson are checked automatically on Windows, Ubuntu and macOS.

## Before you start

This lesson assumes that after lessons 2.1–2.3:

- you create `int` variables and `const int` constants with a starting value in `{}`;
- you calculate with `+`, `-` and `*`, and print results with `std::cout`;
- you predict values before running a program and compare them with the output;
- you look for the first place where a calculation gives a different result than predicted: with the debugger or by printing values.

## The situation

At school, 7 divided by 2 is 3.5. In a program, dividing whole numbers follows its own, precisely defined rules and gives a different result. Today you'll learn these rules, a new operation that calculates the **remainder of a division**, and the rules that say how the operations in a longer expression are grouped.

After this lesson you will:

- divide whole numbers with the `/` operator and predict the result for positive numbers;
- explain why `7 / 2` gives `3`, and where the fractional part goes;
- calculate the remainder of a division with the `%` operator, and tell it apart from `/`;
- use `/` and `%` together in a practical task;
- predict how an expression with several operations is grouped, and change that with parentheses;
- find the error in a calculation that builds but calculates something other than intended.

## 1. Prepare the project

In `cpp-workspace`, create a folder `lesson_2_4` and copy `main.cpp` and `CMakeLists.txt` into it from the original `lesson_05_first_program`. You type the programs from sections 2–8 into that folder's `main.cpp`.

## 2. What is 7 / 2?

In C++, division is written with a slash, `/`. Replace the contents of `main.cpp` with this program:

<!-- example: divide_seven -->
```cpp
#include <iostream>

int main() {
    const int result{7 / 2};
    std::cout << result << "\n";
}
```

**Predict** what the program prints. Write your answer down, then build and run it.

<details>
<summary>The program's output</summary>

<!-- output: divide_seven -->
```text
3
```

</details>

Not 3.5, but 3. This isn't a bug in the program, it's a rule:

- the numbers on both sides of an operator are its **operands**. Here both operands, `7` and `2`, are of type `int`, that is, whole numbers;
- when both operands are whole numbers, `/` performs **integer division**, and its result is a whole number too;
- for positive numbers, that result is the **whole part** of the quotient: how many times 2 fits into 7 completely. The fractional part isn't kept;
- C++ **doesn't round** this result to the nearest whole number. It simply never produces the fraction.

**The fractional part disappears in the division itself, not when the result is stored in a variable.** `7 / 2` gives `3` straight away. There is no 3.5 along the way that the `int` variable then "cuts down". Check this in the next program: its last line prints the result of a division without any variable. The parentheses around the division in `std::cout` show clearly what is to be calculated, as in lesson 2.1.

<!-- example: division_cases -->
```cpp
#include <iostream>

int main() {
    std::cout << "8 / 2 = " << (8 / 2) << "\n";
    std::cout << "9 / 2 = " << (9 / 2) << "\n";
    std::cout << "10 / 3 = " << (10 / 3) << "\n";
    std::cout << "3 / 5 = " << (3 / 5) << "\n";
    std::cout << "7 / 2 = " << (7 / 2) << "\n";
}
```

**Predict** every result before you run the program.

<details>
<summary>The program's output</summary>

<!-- output: division_cases -->
```text
8 / 2 = 4
9 / 2 = 4
10 / 3 = 3
3 / 5 = 0
7 / 2 = 3
```

</details>

- `8 / 2` divides without a remainder, so the result is the same as in maths: 4.
- `9 / 2` gives 4, not 5. If C++ rounded 4.5, the result could be 5. It doesn't round: it counts how many times 2 fits into 9 completely.
- `10 / 3` gives 3: three threes fit into 10, and 1 is left over.
- `3 / 5` gives 0: 5 doesn't fit into 3 even once. That the mathematical result is 0.6 changes nothing here.
- The last line doesn't store the result in any variable, and it still prints 3. This confirms that the fractional part disappears in the division itself.

For now, this course divides only **positive numbers**. For negative numbers the rules are precisely defined too. You'll learn them later.

## 3. The remainder of a division: `%`

A classroom has 17 crayons to share out into boxes of 5. How many boxes will be full, and how many crayons will be left over? Two operators answer this:

<!-- example: groups_and_remainder -->
```cpp
#include <iostream>

int main() {
    const int full_groups{17 / 5};
    const int remaining_items{17 % 5};

    std::cout << "Full groups: " << full_groups << "\n";
    std::cout << "Remaining items: " << remaining_items << "\n";
}
```

<!-- output: groups_and_remainder -->
```text
Full groups: 3
Remaining items: 2
```

- `/` tells you how many **full groups** there are: `17 / 5` gives `3`.
- `%` tells you how many items are **left over**: `17 % 5` gives `2`. It is the **remainder operator**.
- Together they describe everything: 3 full groups of 5 make 15 crayons, and with the remaining 2 there are 17.

**Watch out for the `%` sign.** In C++ it has nothing to do with percentages. `17 % 5` doesn't mean "17 percent of 5". It is always the remainder of dividing 17 by 5.

As with `/`, both numbers used with `%` in this lesson are positive.

## 4. Never divide by zero

> **An important rule:** in C++ you **must not** perform integer division by zero or calculate the remainder of a division by zero: neither `/ 0` nor `% 0`.

Such an operation has **undefined behaviour** in C++. This means the language doesn't specify what happens. The program may suddenly stop, print a random value, or behave differently on different computers. The compiler sometimes warns about a division by zero that is visible in the code, but it can't always notice it before the program runs.

In this lesson, the divisor is always a **known positive number**, written in the code. You'll learn how to check a divisor whose value you don't know in advance in Module 3.

## 5. The order of operations

You now know five arithmetic operators: `+`, `-`, `*`, `/` and `%`. When an expression has several of them, C++ has to know which operations belong together. Two rules decide this:

| Level | Operators | On the same level |
|---|---|---|
| higher (grouped first) | `*`, `/`, `%` | left to right |
| lower | `+`, `-` | left to right |

- **Precedence:** `*`, `/` and `%` are grouped with their numbers before `+` and `-`.
- **Associativity:** when several operators are on the same level, in the expressions of this lesson they are grouped from left to right.
- **Parentheses** change the grouping: what is in parentheses forms one whole.

The easiest way to predict a result is to add **invisible parentheses** in your head. Check this on two pairs of expressions:

<!-- example: grouping -->
```cpp
#include <iostream>

int main() {
    const int first{20 / 5 * 2};
    const int second{20 / (5 * 2)};
    const int third{10 - 8 / 2};
    const int fourth{(10 - 8) / 2};

    std::cout << "20 / 5 * 2 = " << first << "\n";
    std::cout << "20 / (5 * 2) = " << second << "\n";
    std::cout << "10 - 8 / 2 = " << third << "\n";
    std::cout << "(10 - 8) / 2 = " << fourth << "\n";
}
```

**Predict** all four results, then run the program.

<details>
<summary>The program's output</summary>

<!-- output: grouping -->
```text
20 / 5 * 2 = 8
20 / (5 * 2) = 2
10 - 8 / 2 = 6
(10 - 8) / 2 = 1
```

</details>

| Expression | Invisible parentheses | Calculation | Result |
|---|---|---|---|
| `20 / 5 * 2` | `(20 / 5) * 2` | 4 · 2 | 8 |
| `20 / (5 * 2)` | already in parentheses | 20 / 10 | 2 |
| `10 - 8 / 2` | `10 - (8 / 2)` | 10 − 4 | 6 |
| `(10 - 8) / 2` | already in parentheses | 2 / 2 | 1 |

**Watch out for a common mistake.** You sometimes hear the rule "multiplication first, then division". That's wrong, in C++ and in maths: `*` and `/` are on the **same** level. In `20 / 5 * 2` the division comes first, because it stands further to the left. If you want the multiplication first, write it in parentheses, as in `20 / (5 * 2)`.

**Parentheses for clarity.** If you aren't sure how an expression will be grouped, or you don't want the reader to have to think about it, add parentheses even when they change nothing: `(20 / 5) * 2` means the same as `20 / 5 * 2`, but it's quicker to read. The same was true of the parentheses in `std::cout` in lesson 2.1.

Precedence and associativity only say **which operations belong together**. They don't describe the general order in which C++ evaluates all the parts of longer statements. In the expressions of this lesson, built from numbers, variables and arithmetic operators, the grouping alone is enough to predict the result.

## 6. Predict on your own: six expressions

Each of these expressions tests a different trap. Copy the table, and for each row:

1. **predict** the result;
2. write down the **grouping**, that is, the invisible parentheses;
3. check the result in the program below;
4. if the result differs from your prediction, **explain** where the difference comes from.

| | Expression | Grouping | Prediction | Program's result |
|---|---|---|---|---|
| a | `17 / 4` | | | |
| b | `17 % 4` | | | |
| c | `12 / 2 * 3` | | | |
| d | `12 / (2 * 3)` | | | |
| e | `2 + 3 * 4` | | | |
| f | `(2 + 3) * 4` | | | |

Only when the table is filled in, run the program:

<!-- example: predictions -->
```cpp
#include <iostream>

int main() {
    const int a{17 / 4};
    const int b{17 % 4};
    const int c{12 / 2 * 3};
    const int d{12 / (2 * 3)};
    const int e{2 + 3 * 4};
    const int f{(2 + 3) * 4};

    std::cout << "a: " << a << "\n";
    std::cout << "b: " << b << "\n";
    std::cout << "c: " << c << "\n";
    std::cout << "d: " << d << "\n";
    std::cout << "e: " << e << "\n";
    std::cout << "f: " << f << "\n";
}
```

<details>
<summary>The program's output</summary>

<!-- output: predictions -->
```text
a: 4
b: 1
c: 18
d: 2
e: 14
f: 20
```

</details>

The filled-in table with the grouping and a description of each trap is in [Example solutions](#example-solutions).

## 7. A program that calculates something else

Two classes go to a sports lesson together. The first has 14 pupils, the second 16. All of them together split into teams of 5. **The requirement:** the program must print how many teams there will be.

**Step 1. Predict the correct result** from the description alone. Write it down.

**Step 2. Read the program**, and think about what the expression in `teams` really calculates:

<!-- example: teams_bug -->
```cpp
#include <iostream>

int main() {
    const int first_class_pupils{14};
    const int second_class_pupils{16};
    const int team_size{5};

    const int teams{first_class_pupils + second_class_pupils / team_size};

    std::cout << "Teams: " << teams << "\n";
}
```

**Step 3. Run the program**, and compare the output with your prediction.

<details>
<summary>The program's output</summary>

<!-- output: teams_bug -->
```text
Teams: 17
```

</details>

The program built and runs, but 17 teams of 5 would be 85 people, and there are only 30 pupils.

**Step 4. Find the cause.** Add the invisible parentheses to the expression in `teams`, as in section 5. Which operation is grouped with which? You can also print part of the expression with `std::cout`, or, if the debugger has worked for you since lesson 2.3, split the calculation into several constants and look at their values. That isn't necessary here: reading the expression carefully is enough.

**Step 5. Fix the expression** so that it calculates what the description requires.

**Step 6. Check the result.** After the fix, the program must print:

<!-- output: teams_fixed -->
```text
Teams: 6
```

<details>
<summary>Explanation and the fixed program: read them after your own attempt</summary>

`/` is grouped before `+`, so the expression means `first_class_pupils + (second_class_pupils / team_size)`. Only the second class is split into teams: `16 / 5` gives 3, and then the program adds the whole first class, 14 pupils. The result is 17, a number that makes no sense: part of it is pupils, part of it is teams.

The intended calculation is "first add up all the pupils, then divide by the team size". So the addition has to go in parentheses:

<!-- example: teams_fixed -->
```cpp
#include <iostream>

int main() {
    const int first_class_pupils{14};
    const int second_class_pupils{16};
    const int team_size{5};

    const int teams{(first_class_pupils + second_class_pupils) / team_size};

    std::cout << "Teams: " << teams << "\n";
}
```

Now `30 / 5` gives 6.

</details>

## 8. Mission: badge kits

The organisers of a school festival have 29 badges. They put 6 badges into each kit for a team. They want to know how many **full** kits they can prepare, and how many badges will be left unused.

In `cpp-workspace`, create a folder `badge_kits`, copy `CMakeLists.txt` into it from the original `lesson_05_first_program`, create an empty `main.cpp`, and write the program on your own. The program must print exactly:

<!-- output: badge_kits -->
```text
Badges: 29
Badges per kit: 6
Full kits: 4
Badges left: 5
```

### Success criteria

- The program builds as C++20 and prints exactly the output above.
- The number of badges and the number of badges per kit have their own variables, with meaningful English names and starting values.
- Values that don't change in the program are `const`.
- The number of full kits is calculated with `/`, and the number of badges left with `%`. The numbers 4 and 5 are **calculated by the program**: they don't appear in the code.
- The numbers 29 and 6 appear in the code **only once**, in the declarations. The calculations and the output use the variables. That way, a single value is enough to change in the variant.
- The program uses only what you already know: `int`, `const`, `{}`, `+`, `-`, `*`, `/`, `%` and `std::cout`.
- You can check the result without a computer: full kits times 6, plus the badges left, gives 29.

Once the output matches, you can save the project in Git, as in lesson 1.5.

<details>
<summary>Hint 1</summary>

The question "how many full kits" is a question about the number of full groups. The question "how many are left" is a question about the remainder. Which operators answer them?

</details>

<details>
<summary>Hint 2</summary>

Four constants are enough: two with the data and two with the results of the calculations. Print each on its own line, in the order of the required output.

</details>

### Variant: more badges

The organisers have received extra badges, and there are now 32. **Predict** the new results, then change **only one starting value** in the program. The output must be:

<!-- output: badge_kits_variant -->
```text
Badges: 32
Badges per kit: 6
Full kits: 5
Badges left: 2
```

**And one more question:** how many will be left if there are 30 badges? Predict, check in the program, then compare:

<details>
<summary>The output for 30 badges</summary>

<!-- output: badge_kits_exact -->
```text
Badges: 30
Badges per kit: 6
Full kits: 5
Badges left: 0
```

30 divides by 6 without a remainder, so `%` gives 0. A remainder of zero is an ordinary, correct result.

</details>

Example solutions are in [Example solutions](#example-solutions).

## 9. When something goes differently

| What you see | What it means | What to do |
|---|---|---|
| You expected 3.5, and the program prints 3 | Both operands are whole numbers, so `/` performs integer division. | That's expected. If you need the remainder, use `%`. You'll meet numbers with a fractional part in lesson 2.5. |
| The result is the number "left over" when it should be the number of full groups (or the other way round) | `/` and `%` have swapped places. | `/` gives full groups, `%` gives the remainder. |
| A longer expression gives a different result than predicted | The operations were grouped differently than you assumed. | Add the invisible parentheses following section 5. Write the intended grouping with real parentheses. |
| `20 / 5 * 2` gives 8, and you expected 2 | You assumed that multiplication comes before division. | `*` and `/` are on the same level and are grouped from the left. Write `20 / (5 * 2)` if that's what you mean. |
| An expression divides by zero or uses `% 0` | Undefined behaviour, even if the program built. | Remove it. The divisor must be a positive number. |
| `%` was supposed to calculate a percentage | `%` is the remainder of a division, not a percentage. | We don't calculate percentages in this lesson. |

## 10. Explain

Answer in your own words, preferably in writing. Only then compare with the example answer.

**1.** Why does `7 / 2` give `3` in C++?

<details>
<summary>Example answer</summary>

Both operands are of type `int`, so `/` performs integer division. The result is the whole part of the quotient: how many times 2 fits into 7 completely. The fractional part isn't kept, and nothing is rounded.

</details>

**2.** In `const int result{7 / 2};`, does the fractional part disappear because the result goes into a variable of type `int`?

<details>
<summary>Example answer</summary>

No. It disappears in the division itself: `7 / 2` gives 3 straight away. You can see this in section 2, where `(7 / 2)` printed without a variable also gives 3.

</details>

**3.** How do `/` and `%` differ? Explain with the example of 17 crayons in boxes of 5.

<details>
<summary>Example answer</summary>

`17 / 5` gives 3, the number of full boxes. `17 % 5` gives 2, the number of crayons left over. 3 boxes of 5 and 2 crayons make 17 altogether.

</details>

**4.** What is `20 / 5 * 2`, and why isn't it 2?

<details>
<summary>Example answer</summary>

8. `/` and `*` are on the same level and are grouped from left to right, so the expression means `(20 / 5) * 2`, that is, 4 · 2. The result 2 would come from `20 / (5 * 2)`.

</details>

**5.** Why is the divisor in this lesson always a known positive number?

<details>
<summary>Example answer</summary>

Because integer division by zero and the remainder of a division by zero have undefined behaviour in C++. We'll learn later how to check a divisor we don't know in advance. Here the divisor is a positive number written in the code.

</details>

## Summary

- When both operands are whole numbers, `/` performs **integer division**: for positive numbers it gives the whole part of the quotient, without rounding. The fractional part disappears in the division itself.
- `%` gives the **remainder of a division**. Together, `/` and `%` answer "how many full groups?" and "how many are left?". `%` has nothing to do with percentages.
- You **must not** divide by zero or take the remainder of a division by zero: it is undefined behaviour.
- `*`, `/` and `%` are grouped before `+` and `-`. Operators on the same level are grouped from left to right in these expressions. "Multiplication before division" is a wrong rule.
- Parentheses change the grouping and help the reader. It's worth writing the intended calculation with parentheses.
- With a longer expression, first add the invisible parentheses, then calculate.

## What's next

Dividing whole numbers gives whole numbers. But what if you need the result 3.5, for example an average or a price per kilogram? You'll meet numbers with a fractional part in lesson 2.5. **Lesson 2.5 is in preparation.**

---

## Example solutions

Look here **after your own attempt**. Your names may differ, as long as the output is as required.

<details>
<summary>Section 6: six expressions</summary>

| | Expression | Grouping | Result | The trap |
|---|---|---|---|---|
| a | `17 / 4` | — | 4 | Expecting a fractional result (4.25). Integer division gives the whole part: 4. |
| b | `17 % 4` | — | 1 | Confusing `%` with `/`. Four fours make 16, and 1 is left over. |
| c | `12 / 2 * 3` | `(12 / 2) * 3` | 18 | Assuming that multiplication comes before division. That gives 2 instead of 18. |
| d | `12 / (2 * 3)` | already in parentheses | 2 | Ignoring the parentheses. Without them the result would be 18. |
| e | `2 + 3 * 4` | `2 + (3 * 4)` | 14 | Calculating from the left without precedence: (2 + 3) · 4 = 20. |
| f | `(2 + 3) * 4` | already in parentheses | 20 | Ignoring the parentheses. Without them the result would be 14. |

</details>

<details>
<summary>Section 8: mission, badge kits</summary>

<!-- example: badge_kits -->
```cpp
#include <iostream>

int main() {
    const int badges{29};
    const int badges_per_kit{6};

    const int full_kits{badges / badges_per_kit};
    const int badges_left{badges % badges_per_kit};

    std::cout << "Badges: " << badges << "\n";
    std::cout << "Badges per kit: " << badges_per_kit << "\n";
    std::cout << "Full kits: " << full_kits << "\n";
    std::cout << "Badges left: " << badges_left << "\n";
}
```

- Neither the number of badges nor the kit size changes while the program runs, so both are `const`. The results of the calculations don't change either.
- The check: 4 · 6 + 5 = 29.

</details>

<details>
<summary>Section 8: the variant with 32 badges</summary>

<!-- example: badge_kits_variant -->
```cpp
#include <iostream>

int main() {
    const int badges{32};
    const int badges_per_kit{6};

    const int full_kits{badges / badges_per_kit};
    const int badges_left{badges % badges_per_kit};

    std::cout << "Badges: " << badges << "\n";
    std::cout << "Badges per kit: " << badges_per_kit << "\n";
    std::cout << "Full kits: " << full_kits << "\n";
    std::cout << "Badges left: " << badges_left << "\n";
}
```

Only the starting value of `badges` changed. The calculations stayed the same. The check: 5 · 6 + 2 = 32.

</details>

<details>
<summary>Section 8: 30 badges</summary>

<!-- example: badge_kits_exact -->
```cpp
#include <iostream>

int main() {
    const int badges{30};
    const int badges_per_kit{6};

    const int full_kits{badges / badges_per_kit};
    const int badges_left{badges % badges_per_kit};

    std::cout << "Badges: " << badges << "\n";
    std::cout << "Badges per kit: " << badges_per_kit << "\n";
    std::cout << "Full kits: " << full_kits << "\n";
    std::cout << "Badges left: " << badges_left << "\n";
}
```

The check: 5 · 6 + 0 = 30.

</details>

**Previous lesson:** [Lesson 2.3: See what happens in the program](lesson_03_see_what_happens_in_the_program.en.md) · **Next lesson:** in preparation · [Course overview](../../README.en.md)

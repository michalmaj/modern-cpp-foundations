# Lesson 2.5: Numbers with a fractional part: `double` and `auto`

[Polski](lesson_05_numbers_with_a_fractional_part.md) · **English** · [Course overview](../../README.en.md)

> **Module 2, lesson 5** · about 75 minutes
> **You need:** the `cpp-workspace` folder and the original `lesson_05_first_program` project, as before. You don't need the debugger in this lesson.
> **Pilot version.** The examples in this lesson are checked automatically on Windows, Ubuntu and macOS.

## Before you start

This lesson assumes that after lesson 2.4:

- you know that `7 / 2` gives `3` in C++, because both operands are whole numbers and `/` performs integer division;
- you predict how operations are grouped by adding invisible parentheses;
- you create `const int` constants with a starting value in `{}`.

## The situation

In lesson 2.4, dividing whole numbers always gave a whole number. But many quantities have a fractional part: a distance of 7.5 km, a time of 2.5 hours, the average of several measurements. Today you'll meet the `double` type, which stores such numbers, and you'll see that **the types of the values taking part in a calculation decide what kind of calculation it is and what result it gives**. At the end you'll meet `auto`: a way for the compiler to work out a variable's type from its starting value.

After this lesson you will:

- tell whole numbers apart from numbers with a fractional part, and write `double` literals such as `7.0` and `2.5`;
- create `double` variables and constants;
- explain the difference between `7 / 2` and `7.0 / 2`;
- know that the type of the result variable doesn't fix an earlier integer division;
- predict the results of simple operations that combine `int` and `double`;
- know that `double` stores approximate values;
- explain how `auto` works out a type, and that this type doesn't change afterwards;
- choose types on your own in a program that calculates.

## 1. Prepare the project

In `cpp-workspace`, create a folder `lesson_2_5` and copy `main.cpp` and `CMakeLists.txt` into it from the original `lesson_05_first_program`. You type the programs from sections 2–11 into that folder's `main.cpp`.

## 2. Two versions of the same division

Replace the contents of `main.cpp` with this program:

<!-- example: two_divisions -->
```cpp
#include <iostream>

int main() {
    std::cout << (7 / 2) << "\n";
    std::cout << (7.0 / 2) << "\n";
}
```

**Predict** both results. Write them down, then run the program.

<details>
<summary>The program's output</summary>

<!-- output: two_divisions -->
```text
3
3.5
```

</details>

The first line is the integer division you know from lesson 2.4. The second differs only in how one number is written, and it gives a different result:

- `7` and `2` are **integer literals**: numbers of type `int`, written directly in the code;
- `7.0` is a **`double` literal**: a number with a fractional part, even if that part is zero;
- when both operands of `/` are whole numbers, integer division is performed and the result is a whole number;
- when one of the operands is of type `double`, the other is converted to `double` for this calculation. A **floating-point division** is then performed, and its result can have a fractional part.

This rule applies to the simple operations of this lesson: `+`, `-`, `*` and `/` with `int` and `double` numbers. It isn't the complete set of rules for combining types in C++. The `%` operator from lesson 2.4 works only with whole numbers, so we don't use it with `double`.

## 3. The `double` type

The `double` type stores numbers with a fractional part. This is how you write a few ordinary measurements:

<!-- example: double_values -->
```cpp
#include <iostream>

int main() {
    const double distance_km{7.5};
    const double walk_time_h{2.5};
    const double shelf_length_m{0.75};
    const double measured_length_m{3.0};

    std::cout << "Distance: " << distance_km << " km\n";
    std::cout << "Walk time: " << walk_time_h << " h\n";
    std::cout << "Shelf length: " << shelf_length_m << " m\n";
    std::cout << "Measured length: " << measured_length_m << " m\n";
}
```

**Predict** what the last line prints, then run the program.

<details>
<summary>The program's output</summary>

<!-- output: double_values -->
```text
Distance: 7.5 km
Walk time: 2.5 h
Shelf length: 0.75 m
Measured length: 3 m
```

</details>

- In code, the fractional part is always separated with a **dot**: `7.5`. That's also how this course writes such numbers in English text.
- `measured_length_m` is of type `double` and has the value `3.0`, but `std::cout` prints it as `3`. **You can't always tell a number's type from how it looks on the screen.** You read the type from the code.
- The `double` type suits measured quantities: distances, times, lengths, averages. We don't use it for money in this lesson, because exact amounts need a separate approach.
- C++ has other number types too. For now you're meeting two: `int` for whole numbers and `double` for numbers with a fractional part.

## 4. A variable's type doesn't change the past

What happens when the result of an integer division goes into a variable of type `double`?

<!-- example: type_too_late -->
```cpp
#include <iostream>

int main() {
    const double first{7 / 2};
    const double second{7.0 / 2};

    std::cout << "first: " << first << "\n";
    std::cout << "second: " << second << "\n";
}
```

**Predict** both values, then run the program.

<details>
<summary>The program's output</summary>

<!-- output: type_too_late -->
```text
first: 3
second: 3.5
```

</details>

- `first` is of type `double`, but it stores **3**. Why? First the starting value `7 / 2` is calculated. Both operands are whole numbers, so it's an integer division and the result is 3. Only this finished value goes into `first`.
- `second` stores **3.5**, because in `7.0 / 2` one operand is of type `double`.
- **The kind of division depends on the operands**, not on the type of the variable that receives the result. A `double` variable doesn't make the calculation happen again: it receives the value that has already been produced.
- `first` prints as `3`, not `3.0`. As in section 3: how a value looks on the screen doesn't tell you its type.

### Check: a half

This program was supposed to store a half:

<!-- example: half_bug -->
```cpp
#include <iostream>

int main() {
    const double half{1 / 2};
    std::cout << "half: " << half << "\n";
}
```

1. **Predict** what this program prints.
2. Explain where that result comes from.
3. Fix the program so that it prints `half: 0.5`. Don't change the type of `half`.

<details>
<summary>The output, the explanation and the fix: read them after your own attempt</summary>

<!-- output: half_bug -->
```text
half: 0
```

`1 / 2` is an integer division: 2 doesn't fit into 1 even once, so the result is 0. That `half` is of type `double` changes nothing. It's enough for one operand to be of type `double`:

<!-- example: half_fixed -->
```cpp
#include <iostream>

int main() {
    const double half{1.0 / 2};
    std::cout << "half: " << half << "\n";
}
```

<!-- output: half_fixed -->
```text
half: 0.5
```

</details>

## 5. Mixing `int` and `double`

Someone does the long jump three times and wants to know the average length of a jump. The lengths are measurements, so they are of type `double`. The number of jumps is a whole number, so it is of type `int`:

<!-- example: average_jump -->
```cpp
#include <iostream>

int main() {
    const double first_jump_m{1.5};
    const double second_jump_m{2.5};
    const double third_jump_m{3.5};
    const int jumps{3};

    const double average_jump_m{(first_jump_m + second_jump_m + third_jump_m) / jumps};

    std::cout << "Average jump: " << average_jump_m << " m\n";
}
```

<!-- output: average_jump -->
```text
Average jump: 2.5 m
```

The sum in the parentheses is a `double` (7.5). It is divided by `jumps`, which is of type `int`. One operand is of type `double`, so this is a floating-point division, and the result is 2.5. The parentheses are needed for the reasons from lesson 2.4: without them, only the third jump would be divided by `jumps`.

**The rule for the simple operations of this lesson:** if in `+`, `-`, `*` or `/` one operand is of type `int` and the other of type `double`, the calculation is done in `double` and the result is of type `double`. In a longer expression, this rule applies to **each operation separately**, in the grouping order from lesson 2.4.

### Predict on your own: seven expressions

Copy the table. For each expression, **predict** the result and mark whether there is an integer division along the way. Add the invisible parentheses first.

| | Expression | Is there an integer division? | Prediction | Program's result |
|---|---|---|---|---|
| a | `7 / 2` | | | |
| b | `7 / 2.0` | | | |
| c | `1.5 + 2` | | | |
| d | `2.5 * 2` | | | |
| e | `10 - 0.25` | | | |
| f | `1 / 2 * 4.0` | | | |
| g | `1.0 / 2 * 4` | | | |

Only when the table is filled in, run the program:

<!-- example: mixed_predictions -->
```cpp
#include <iostream>

int main() {
    std::cout << "a: " << (7 / 2) << "\n";
    std::cout << "b: " << (7 / 2.0) << "\n";
    std::cout << "c: " << (1.5 + 2) << "\n";
    std::cout << "d: " << (2.5 * 2) << "\n";
    std::cout << "e: " << (10 - 0.25) << "\n";
    std::cout << "f: " << (1 / 2 * 4.0) << "\n";
    std::cout << "g: " << (1.0 / 2 * 4) << "\n";
}
```

<details>
<summary>The program's output</summary>

<!-- output: mixed_predictions -->
```text
a: 3
b: 3.5
c: 3.5
d: 5
e: 9.75
f: 0
g: 2
```

</details>

The filled-in table with explanations is in [Example solutions](#example-solutions).

**Don't add `.0` everywhere.** The number of jumps, pupils or laps is a whole number and should stay `int`. A floating-point calculation is needed when a quantity can have a fractional part, or when the result should have one, such as an average. Then at least one operand of the division must be of type `double`. Ideally it's the value that naturally has a fractional part, such as a length or a time.

## 6. `double` is an approximation

A `double` isn't a mathematical number with unlimited precision. The computer stores it in binary form, and **not every decimal number can be stored exactly that way**. For example, 0.1 is stored in a `double` as a value very close to 0.1, but not exactly 0.1. That's why the results of some calculations are approximate.

Usually you don't see this: by default, `std::cout` prints a `double` in a shortened form, with at most six significant digits. But remember that the printed number isn't always exactly the one the program stores.

For now, the examples in this course use values such as `0.5`, `0.25`, `1.5`, `2.5`, `3.75`, which a `double` stores exactly. Their results are predictable and the same on every system. You'll learn how to work with approximations in more serious calculations later.

## 7. Braces guard the value

You write the starting value in `{}`, as before: `int count{3};`, `double average{2.5};`. This notation has one more advantage. What happens if you try to store a number with a fractional part in an `int` variable? **Predict**, then build:

<!-- broken: narrowing at=4 errors=1 error=^type 'double' cannot be narrowed to 'int' in initializer list -->
```cpp
#include <iostream>

int main() {
    const int ticket_count{2.5};
    std::cout << ticket_count << "\n";
}
```

The program won't build. On line 4, the compiler reports `type 'double' cannot be narrowed to 'int' in initializer list`. On the same line it also prints the warning `implicit conversion from 'double' to 'int' changes value from 2.5 to 2`: after such a change, 2.5 would become 2. The number 2.5 can't fit into an `int` without losing its fractional part. A change of type like this, which could change the value, is called a **narrowing conversion**. Initialisation with `{}` doesn't allow it: instead of silently storing 2 in `ticket_count`, the compiler stops the build. Skip the `note:` line suggesting an explicit cast for now: here the right fix is choosing the type.

Restore correct code. The number of tickets is a whole number, so write, for example, `{2}`. If the value really had to have a fractional part, the variable would have to be of type `double`.

Not every change of type is an error. A whole number can be stored in a `double` without losing anything, so this builds and runs:

<!-- example: whole_number_in_double -->
```cpp
#include <iostream>

int main() {
    const double distance_km{7};
    std::cout << "Distance: " << distance_km << " km\n";
}
```

<!-- output: whole_number_in_double -->
```text
Distance: 7 km
```

## 8. `auto`: the type from the starting value

So far, every variable had its type written out: `int` or `double`. Instead of a type you can write `auto`. Then **the compiler works out the type from the starting value**:

<!-- example: auto_types -->
```cpp
#include <iostream>

int main() {
    auto ticket_count{3};
    auto distance_km{7.5};
    auto first{7 / 2};
    auto second{7.0 / 2};

    std::cout << "ticket_count: " << ticket_count << "\n";
    std::cout << "distance_km: " << distance_km << "\n";
    std::cout << "first: " << first << "\n";
    std::cout << "second: " << second << "\n";
}
```

**Predict** the type and value of each variable, then run the program.

<details>
<summary>The program's output</summary>

<!-- output: auto_types -->
```text
ticket_count: 3
distance_km: 7.5
first: 3
second: 3.5
```

</details>

| Declaration | Starting value | Type worked out by the compiler | Value |
|---|---|---|---|
| `auto ticket_count{3};` | an integer literal | `int` | 3 |
| `auto distance_km{7.5};` | a literal with a dot | `double` | 7.5 |
| `auto first{7 / 2};` | a division of two `int`s | `int` | 3 |
| `auto second{7.0 / 2};` | a `double` divided by an `int` | `double` | 3.5 |

- `auto` **doesn't mean** "any type". Each of these variables has one specific type, which the compiler worked out from the starting value before the program even runs.
- That type **doesn't change** while the program runs. `ticket_count` is an `int` from its declaration to the end, just as if you had written `int ticket_count{3};`.
- `auto` **doesn't perform** any extra calculation, and fixes nothing. `first` receives the result of an integer division, 3, and its type is `int`, because that is the type of the result of `7 / 2`.
- These values don't change, so following the rule from lesson 2.2 they could also be `const`, for example `const auto ticket_count{3};`. Here `const` is left out to focus on `auto`.

You work out the type of an `auto` variable the same way the compiler does: look at the starting value and apply the rules from sections 2–5.

## 9. `auto` or an explicit type?

`auto` doesn't replace types everywhere. Compare:

<!-- example: auto_or_explicit -->
```cpp
#include <iostream>

int main() {
    const double daily_distance_km{7.5};
    const int days{3};

    const auto total_distance_km{daily_distance_km * days};

    std::cout << "Total distance: " << total_distance_km << " km\n";
}
```

<!-- output: auto_or_explicit -->
```text
Total distance: 22.5 km
```

- For the **data**, `daily_distance_km` and `days`, the explicit type tells the reader what the value is: a distance with a fractional part, and a whole number. With `auto`, the type would still be worked out, but it would depend on whether someone wrote `7.5` or `7`.
- For the **result**, `total_distance_km`, the type follows clearly from the calculation: `double` times `int` gives `double`. `auto` hides nothing here.

A program with only explicit types is just as good. `auto` is a convenience, not an obligation. If you aren't sure which type the compiler will work out, write the type explicitly.

## 10. Fix the calculation

A ribbon is 10 m long and must be cut into 4 equal pieces. **The requirement:** the program must print the length of one piece.

**Step 1. Predict the correct result** from the description.

**Step 2. Run the program** and compare the output with your prediction:

<!-- example: ribbon_bug -->
```cpp
#include <iostream>

int main() {
    const int ribbon_length_m{10};
    const int pieces{4};

    const double piece_length_m{ribbon_length_m / pieces};

    std::cout << "Piece length: " << piece_length_m << " m\n";
}
```

<details>
<summary>The program's output</summary>

<!-- output: ribbon_bug -->
```text
Piece length: 2 m
```

</details>

**Step 3. Find the cause.** The result `piece_length_m` is already of type `double`, so changing the type of the result won't help. Check the operands of the division: what types are they, and what kind of division do they perform?

**Step 4. Fix the program** by changing the type of the value that can naturally have a fractional part. The number of pieces should stay a whole number.

**Step 5. Check the result.** After the fix, the program must print:

<!-- output: ribbon_fixed -->
```text
Piece length: 2.5 m
```

<details>
<summary>Explanation and the fixed program: read them after your own attempt</summary>

Both operands, `ribbon_length_m` and `pieces`, are of type `int`, so `ribbon_length_m / pieces` is an integer division: 10 / 4 gives 2. The `double` type of `piece_length_m` doesn't change the calculation that has already happened (section 4).

The length of the ribbon is a measurement that could be, say, 10.5 m, so the `double` type suits it. The number of pieces is a whole number and stays `int`:

<!-- example: ribbon_fixed -->
```cpp
#include <iostream>

int main() {
    const double ribbon_length_m{10.0};
    const int pieces{4};

    const double piece_length_m{ribbon_length_m / pieces};

    std::cout << "Piece length: " << piece_length_m << " m\n";
}
```

Now one operand is of type `double`, so this is a floating-point division: 10.0 / 4 gives 2.5.

</details>

## 11. Choose the type

For each quantity, choose `int` or `double`, and briefly justify your choice. Ask yourself: can this quantity have a fractional part?

| Quantity | Type | Why |
|---|---|---|
| the number of pupils in a class | | |
| height in metres, for example 1.62 | | |
| the number of pages in a book | | |
| a running time measured with a stopwatch, for example 12.4 s | | |
| the average of several marks | | |
| the number of laps of a track | | |

Example answers are in [Example solutions](#example-solutions).

## 12. Mission: the average lap time

In a running training session, 5 laps of a track took 37.5 seconds altogether, according to the stopwatch. The program must calculate the average time of one lap.

In `cpp-workspace`, create a folder `lap_times`, copy `CMakeLists.txt` into it from the original `lesson_05_first_program`, create an empty `main.cpp`, and write the program on your own. The program must print exactly:

<!-- output: lap_times -->
```text
Laps: 5
Total time: 37.5 s
Average lap time: 7.5 s
```

### Success criteria

- The program builds as C++20 and prints exactly the output above.
- The number of laps, the total time and the average time have their own constants with meaningful English names.
- Each constant has a type that fits its meaning: you can justify why the number of laps is `int` and the times are `double`. If you use `auto` for one of them, you can say which type the compiler works out.
- The average is **calculated by the program**: the number 7.5 doesn't appear in the code. The numbers 5 and 37.5 appear in the code only once, in the declarations.
- The program uses only what you already know: `int`, `double`, `auto`, `const`, `{}`, arithmetic operations and `std::cout`.
- You can explain why the result has a fractional part even though the number of laps is a whole number.

Once the output matches, you can save the project in Git, as in lesson 1.5.

<details>
<summary>Hint 1</summary>

Which of these quantities can have a fractional part, and which is always a whole number? That decides the type of each constant.

</details>

<details>
<summary>Hint 2</summary>

The average is the total time divided by the number of laps. Check the types of the operands of this division, and whether an integer division will be performed.

</details>

### Variant: a slower session

In the next session, 5 laps took 42.5 seconds. **Predict** the new average, then change **only one starting value** in the program. The output must be:

<!-- output: lap_times_variant -->
```text
Laps: 5
Total time: 42.5 s
Average lap time: 8.5 s
```

Example solutions are in [Example solutions](#example-solutions).

## 13. When something goes differently

| What you see | What it means | What to do |
|---|---|---|
| A division result has no fractional part, although it should | Both operands are whole numbers, so an integer division was performed. The type of the result variable doesn't change that. | Check the operands. The value that naturally has a fractional part should be of type `double`. |
| `std::cout` prints `3`, and the variable is of type `double` | The value is 3.0. `std::cout` doesn't print `.0`. | Nothing. Read the type from the code, not from the screen. |
| An error containing `cannot be narrowed` at `{}` | The value in `{}` wouldn't fit into the variable's type without changing, for example 2.5 in an `int`. | Check that the variable has the right type. A value with a fractional part needs `double`. |
| `7,5` instead of `7.5` in the code | In C++, the fractional part is separated with a dot. A comma means something else in code. | Write `7.5`. |
| An error with `%` and a `double` number | `%` works only with whole numbers. | Don't use `%` with `double` in this lesson. |
| An `auto` variable has a different type than you assumed | The compiler worked out the type from the starting value; for example, `auto x{7 / 2};` gives `int`. | Check the type of the starting value. When in doubt, write the type explicitly. |

## 14. Explain

Answer in your own words, preferably in writing. Only then compare with the example answer.

**1.** Why does `7 / 2` give `3`, and `7.0 / 2` give `3.5`?

<details>
<summary>Example answer</summary>

In `7 / 2` both operands are of type `int`, so an integer division is performed. In `7.0 / 2` the first operand is of type `double`, so the second is converted to `double` and a floating-point division is performed, whose result has a fractional part.

</details>

**2.** Why does `const double first{7 / 2};` store 3, even though it is of type `double`?

<details>
<summary>Example answer</summary>

Because `7 / 2` is calculated first, and that is an integer division that gives 3. Only this value goes into the variable. The type of the variable doesn't change the kind of division.

</details>

**3.** If a program prints `3`, does that mean the value is of type `int`?

<details>
<summary>Example answer</summary>

No. A `double` value equal to 3.0 also prints as `3`. You have to read the type from the code.

</details>

**4.** What is the type of `x` in `auto x{7.0 / 2};`, and how do you know? Can it later become an `int`?

<details>
<summary>Example answer</summary>

`double`, because the starting value `7.0 / 2` is of type `double`. The compiler works out the type once, at the declaration. It doesn't change afterwards.

</details>

**5.** Why is the number of laps in the mission of type `int` and not `double`?

<details>
<summary>Example answer</summary>

Because there is always a whole number of laps. The times are what have a fractional part. It's enough for the total time to be of type `double` for the division by the number of laps to be a floating-point one.

</details>

## Summary

- `double` stores numbers with a fractional part. A `double` literal has a dot: `7.5`, `7.0`.
- The kind of division depends on the **operands**: two `int`s give an integer division, and when one operand is of type `double`, a floating-point division is performed.
- The type of the result variable **doesn't change** a calculation that has already happened: `const double first{7 / 2};` stores 3.
- In simple operations with `int` and `double`, the calculation is done in `double`. In a longer expression, this applies to each operation separately.
- `double` stores **approximate** values: not every decimal number can be stored exactly. A printed number doesn't always reveal its type or its exact value.
- Initialisation with `{}` doesn't let a value that would change be stored silently, for example 2.5 in an `int`.
- `auto` works out one specific type from the starting value, at the declaration. That type doesn't change afterwards, and `auto` calculates nothing for you.
- An explicit type is good for data, and `auto` where the type follows clearly from the starting value.

## What's next

Your programs now calculate with whole and fractional numbers, but all their data is written in the code. In lesson 2.6, a program will start taking numbers from the user. **Lesson 2.6 is in preparation.**

---

## Example solutions

Look here **after your own attempt**. Your names may differ, as long as the output is as required.

<details>
<summary>Section 5: seven expressions</summary>

| | Expression | Grouping | Is there an integer division? | Result | Explanation |
|---|---|---|---|---|---|
| a | `7 / 2` | — | yes | 3 | Two `int`s. |
| b | `7 / 2.0` | — | no | 3.5 | One operand is `double`. It doesn't matter whether it is on the left or on the right. |
| c | `1.5 + 2` | — | no | 3.5 | `double` plus `int` gives `double`. |
| d | `2.5 * 2` | — | no | 5 | The result is of type `double` and equals 5.0, but it prints as `5`. |
| e | `10 - 0.25` | — | no | 9.75 | `int` minus `double` gives `double`. |
| f | `1 / 2 * 4.0` | `(1 / 2) * 4.0` | yes | 0 | First `1 / 2`: two `int`s, result 0. Only then the multiplication by `4.0`, that is, 0 · 4.0 = 0. The `4.0` doesn't fix the division that has already happened. |
| g | `1.0 / 2 * 4` | `(1.0 / 2) * 4` | no | 2 | `1.0 / 2` gives 0.5, and 0.5 · 4 gives 2.0, printed as `2`. |

</details>

<details>
<summary>Section 11: choose the type</summary>

| Quantity | Type | Why |
|---|---|---|
| the number of pupils in a class | `int` | Pupils are counted whole. |
| height in metres | `double` | A measurement with a fractional part. |
| the number of pages in a book | `int` | Pages are counted whole. |
| a running time measured with a stopwatch | `double` | A measurement with a fractional part. |
| the average of several marks | `double` | An average usually has a fractional part, even when the marks are whole numbers. |
| the number of laps of a track | `int` | Laps are counted whole. |

For an average of whole-number marks, remember section 4: a `double` variable for the result isn't enough. One operand of the division must also be of type `double`.

</details>

<details>
<summary>Section 12: mission, the average lap time</summary>

<!-- example: lap_times -->
```cpp
#include <iostream>

int main() {
    const int laps{5};
    const double total_time_s{37.5};

    const double average_lap_time_s{total_time_s / laps};

    std::cout << "Laps: " << laps << "\n";
    std::cout << "Total time: " << total_time_s << " s\n";
    std::cout << "Average lap time: " << average_lap_time_s << " s\n";
}
```

- `laps` is of type `int`, because there is always a whole number of laps. `total_time_s` is of type `double`, because it is a time measurement.
- `total_time_s / laps` is a `double` divided by an `int`, so a floating-point division is performed: 37.5 / 5 gives 7.5.
- Instead of `const double average_lap_time_s` you could write `const auto average_lap_time_s`. The compiler would work out the type `double`, because that's the type of the result of the division.

</details>

<details>
<summary>Section 12: the variant</summary>

<!-- example: lap_times_variant -->
```cpp
#include <iostream>

int main() {
    const int laps{5};
    const double total_time_s{42.5};

    const double average_lap_time_s{total_time_s / laps};

    std::cout << "Laps: " << laps << "\n";
    std::cout << "Total time: " << total_time_s << " s\n";
    std::cout << "Average lap time: " << average_lap_time_s << " s\n";
}
```

Only the starting value of `total_time_s` changed. The calculation stayed the same: 42.5 / 5 gives 8.5.

</details>

**Previous lesson:** [Lesson 2.4: Division, remainder and the order of operations](lesson_04_division_remainder_and_order_of_operations.en.md) · **Next lesson:** in preparation · [Course overview](../../README.en.md)

# Lesson 3.2: Two possibilities (`else`), equality and `bool`

[Polski](lesson_02_two_ways.md) · **English** · [Course overview](../../README.en.md)

> **Module 3, lesson 2** · about 75 minutes
> **You need:** the `cpp-workspace` folder and the original `lesson_05_first_program` project, as before. You don't need the debugger in this lesson.
> **Pilot version.** The programs in this lesson are checked automatically on Windows, Ubuntu and macOS, including with the given input data.

## Before you start

This lesson assumes that after lesson 3.1:

- you write an `if` with a `<`, `<=`, `>` or `>=` comparison, and know that its block runs only when the answer is "yes";
- you check a program exactly at a limit and right next to it;
- you know assignment (lesson 2.2), the remainder `%` (lesson 2.4) and `std::string` (lesson 2.7).

## The situation

In lesson 3.1, a program could do something or skip it. Often, though, you need to choose **one of two** possibilities: passed or not passed, the right code or a wrong one. Today you'll meet `else`, the second way. You'll also learn to check whether values are **equal**, and you'll learn the name of the "yes" or "no" answer that a comparison gives.

After this lesson you will:

- choose one of two branches with `if` and `else`, and predict which one runs;
- check equality with the `==` operator and inequality with `!=`, also for text;
- tell assignment `=` apart from comparison `==`;
- explain what `bool`, `true` and `false` are, and store the result of a comparison in a `bool` variable;
- know where to declare a variable that you use after an `if`;
- write a program with two independent decisions, and check it for different combinations of data.

## 1. Prepare the project

In `cpp-workspace`, create a folder `lesson_3_2` and copy `main.cpp` and `CMakeLists.txt` into it from the original `lesson_05_first_program`. You type the programs from sections 2–8 into that folder's `main.cpp`.

## 2. One of two ways: `else`

Passing requires at least 50 points. The program must print `Passed` or `Not passed`, and at the end, always, `Score checked`:

<!-- example: pass_check -->
```cpp
#include <iostream>

int main() {
    int score{0};

    std::cout << "Enter score:\n";
    std::cin >> score;

    if (score >= 50) {
        std::cout << "Passed\n";
    } else {
        std::cout << "Not passed\n";
    }

    std::cout << "Score checked\n";
}
```

**Predict** what the program prints for 49, 50 and 51 points. Then run it three times.

<!-- input: pass_check -->
```text
49
```

<details>
<summary>The standard output for 49</summary>

<!-- output: pass_check -->
```text
Enter score:
Not passed
Score checked
```

</details>

<!-- input: pass_check -->
```text
50
```

<details>
<summary>The standard output for 50</summary>

<!-- output: pass_check -->
```text
Enter score:
Passed
Score checked
```

</details>

<!-- input: pass_check -->
```text
51
```

<details>
<summary>The standard output for 51</summary>

<!-- output: pass_check -->
```text
Enter score:
Passed
Score checked
```

</details>

- When the condition is satisfied, the program executes the **first branch**, the block after `if`.
- Otherwise it executes the **`else` branch** ("else" meaning "otherwise").
- **Exactly one** of the two branches runs, never both one after the other.
- `else` **has no condition of its own**. Its block runs when the condition at `if` isn't satisfied.
- After the chosen branch the program carries on: `Score checked` always appears.
- The braces mark both branches, and the indentation helps you see them. `else` comes right after the closing brace of the first branch.

**`if` or `if`/`else`?** A plain `if` from lesson 3.1 is an **optional** action: do something, or do nothing. `if`/`else` is a choice of **one of two alternatives**: do this, or do that. In this program, the two messages are two possible answers to the same question, so `else` fits.

## 3. Assignment `=` and comparison `==`

You know assignment from lesson 2.2: `count = 5;` **changes** the value of a variable. To check whether values are equal, you use a different operator: **`==`**, two equals signs. Compare both in one program:

<!-- example: assign_and_compare -->
```cpp
#include <iostream>

int main() {
    int count{3};

    if (count == 5) {
        std::cout << "count is 5\n";
    } else {
        std::cout << "count is not 5\n";
    }
    std::cout << "count: " << count << "\n";

    count = 5;
    std::cout << "count: " << count << "\n";

    if (count == 5) {
        std::cout << "count is 5\n";
    } else {
        std::cout << "count is not 5\n";
    }
}
```

**Predict** all four lines, then run the program.

<details>
<summary>The program's output</summary>

<!-- output: assign_and_compare -->
```text
count is not 5
count: 3
count: 5
count is 5
```

</details>

- `count == 5` **checks** whether `count` is equal to 5, and gives the answer "yes" or "no". It changes nothing: after the first comparison, `count` is still 3.
- `count = 5;` **stores** the value 5 in `count`. It's a command, not a question.
- These are two different operations, not two ways of writing the same thing. Read `==` as "is it equal to?", and `=` as "gets the value".

## 4. Inequality: `!=`

**`!=`** checks whether values are **different**. It gives "yes" when they differ, and "no" when they are equal:

<!-- example: door_code -->
```cpp
#include <iostream>

int main() {
    const int expected_code{1234};
    int code{0};

    std::cout << "Enter door code:\n";
    std::cin >> code;

    if (code != expected_code) {
        std::cout << "Wrong code\n";
    } else {
        std::cout << "Door open\n";
    }
}
```

<!-- input: door_code -->
```text
4321
```

<!-- output: door_code -->
```text
Enter door code:
Wrong code
```

<!-- input: door_code -->
```text
1234
```

<!-- output: door_code -->
```text
Enter door code:
Door open
```

`==` and `!=` always give opposite answers: when one says "yes", the other says "no". You could write the same program with `==` by swapping the branches. Choose the form that reads more naturally for the requirement.

## 5. The answer has a name: `bool`

In lesson 3.1, a comparison gave the answer "yes" or "no". In C++ that answer is a value of type **`bool`** (a logical value). The `bool` type has only two values:

- **`true`**, meaning "yes";
- **`false`**, meaning "no".

You create a `bool` variable just like any other:

<!-- fragment -->
```cpp
bool is_ready{true};
bool is_finished{false};
```

Most often, though, a `bool` value comes from a comparison. This program checks whether a number is even, that is, whether the remainder of dividing it by 2 is 0:

<!-- example: even_check -->
```cpp
#include <iostream>

int main() {
    int number{0};

    std::cout << "Enter a whole number:\n";
    std::cin >> number;

    const bool is_even{number % 2 == 0};

    if (is_even) {
        std::cout << "Even\n";
    } else {
        std::cout << "Odd\n";
    }
}
```

**Predict** the result for 8, 7 and 0, then check.

<!-- input: even_check -->
```text
8
```

<!-- output: even_check -->
```text
Enter a whole number:
Even
```

<!-- input: even_check -->
```text
7
```

<!-- output: even_check -->
```text
Enter a whole number:
Odd
```

<!-- input: even_check -->
```text
0
```

<details>
<summary>The standard output for 0</summary>

<!-- output: even_check -->
```text
Enter a whole number:
Even
```

0 is even: 0 divides by 2 without a remainder, so `0 % 2` gives 0.

</details>

- `number % 2 == 0`: first `%` calculates the remainder of dividing by 2 (lesson 2.4), then `==` checks whether that remainder is 0. The result is of type `bool`.
- `is_even` **stores** that result: `true` for an even number, `false` for an odd one. The value doesn't change, so it's a constant.
- `if (is_even)` uses the stored value. The condition in an `if` is simply a `bool` value: the block runs when it is `true`.

**A stored value doesn't follow changes.** `is_even` holds the answer calculated **at the moment of initialisation**. If you change `number` later, `is_even` doesn't update itself. This program shows that, and also how `std::cout` prints a `bool` value:

<!-- example: stored_bool -->
```cpp
#include <iostream>

int main() {
    int number{8};
    const bool is_even{number % 2 == 0};
    std::cout << "is_even: " << is_even << "\n";

    number = 7;
    std::cout << "number: " << number << "\n";
    std::cout << "is_even: " << is_even << "\n";

    const bool is_even_now{number % 2 == 0};
    std::cout << "is_even_now: " << is_even_now << "\n";
}
```

<details>
<summary>The program's output</summary>

<!-- output: stored_bool -->
```text
is_even: 1
number: 7
is_even: 1
is_even_now: 0
```

</details>

- By default, `std::cout` prints `true` as **`1`** and `false` as **`0`**. That's only how the value is shown on the screen: the variable is still a `bool`, not an `int`. As in lesson 2.5, the way a value looks on the screen doesn't tell you its type.
- After `number = 7;`, `is_even` is still `true` (printed as `1`), because it stores the answer calculated for 8. To get the answer for the new value, you have to calculate the comparison **again**, as in `is_even_now`.

Instead of printing `1` and `0`, programs in this course usually print their own words in the `if`/`else` branches, such as `Even` and `Odd`.

## 6. Text: `==` and `!=` for `std::string`

`std::string` values are compared with the same operators. What's compared is the **text**: whether both strings have the same characters in the same order.

<!-- example: word_check -->
```cpp
#include <iostream>
#include <string>

int main() {
    const std::string expected_answer{"comet"};
    std::string answer{""};

    std::cout << "Enter the answer:\n";
    std::cin >> answer;

    if (answer == expected_answer) {
        std::cout << "Correct\n";
    } else {
        std::cout << "Incorrect\n";
    }
}
```

**Predict** the result for `comet`, `Comet` and `planet`. Then check.

<!-- input: word_check -->
```text
comet
```

<!-- output: word_check -->
```text
Enter the answer:
Correct
```

<!-- input: word_check -->
```text
Comet
```

<details>
<summary>The standard output for Comet</summary>

<!-- output: word_check -->
```text
Enter the answer:
Incorrect
```

</details>

<!-- input: word_check -->
```text
planet
```

<!-- output: word_check -->
```text
Enter the answer:
Incorrect
```

- The comparison **distinguishes upper and lower case**: `Comet` and `comet` are different strings, so the answer is "no". The program doesn't guess that the same word was meant.
- `answer != expected_answer` would give `true` for `Comet` and `planet`, and `false` for `comet`.

**Check yourself.** Answer briefly, then compare with the solutions:

1. When does `a == b` give `true`? When does `a != b` give `true`?
2. Does a comparison change the values of `a` and `b`?
3. What do `==` and `!=` give for two identical strings, and what for two different ones?
4. Which form fits each requirement: `=`, `==` or `!=`?

| Requirement | Form |
|---|---|
| Set the number of points to 0. | |
| Check whether the number of points is 0. | |
| Check whether the answer is something other than `comet`. | |
| Change the answer to `comet`. | |
| Check whether the number is odd. | |

## 7. Two independent decisions

A program can have several `if`/`else` constructs. Each one makes **its own** decision:

<!-- example: weather_report -->
```cpp
#include <iostream>

int main() {
    int temperature_c{0};
    int wind_kmh{0};

    std::cout << "Enter temperature:\n";
    std::cin >> temperature_c;
    std::cout << "Enter wind speed in km/h:\n";
    std::cin >> wind_kmh;

    if (temperature_c >= 20) {
        std::cout << "Warm\n";
    } else {
        std::cout << "Cold\n";
    }

    if (wind_kmh > 30) {
        std::cout << "Windy\n";
    } else {
        std::cout << "Calm\n";
    }
}
```

**Predict** the last two lines for a temperature of 25 and a wind of 10, for a temperature of 15 and a wind of 40, and for the case at the limits: a temperature of 20 and a wind of 30.

<!-- input: weather_report -->
```text
25
10
```

<!-- output: weather_report -->
```text
Enter temperature:
Enter wind speed in km/h:
Warm
Calm
```

<!-- input: weather_report -->
```text
15
40
```

<!-- output: weather_report -->
```text
Enter temperature:
Enter wind speed in km/h:
Cold
Windy
```

<!-- input: weather_report -->
```text
20
30
```

<details>
<summary>The standard output for 20 and 30</summary>

<!-- output: weather_report -->
```text
Enter temperature:
Enter wind speed in km/h:
Warm
Calm
```

20 satisfies `>= 20`, but 30 doesn't satisfy `> 30`.

</details>

In each `if`/`else` construct one branch runs, so the program prints **one** line about the temperature and **one** about the wind. That doesn't mean only one branch runs in the whole program: each decision is separate.

## 8. Where does a variable live?

The program should store the result in a variable `result` and print it **after** the `if`/`else`. Someone declared `result` inside the branches:

<!-- broken: result_in_block at=16 errors=1 error=^use of undeclared identifier 'result'$ -->
```cpp
#include <iostream>
#include <string>

int main() {
    int score{0};

    std::cout << "Enter score:\n";
    std::cin >> score;

    if (score >= 50) {
        std::string result{"Passed"};
    } else {
        std::string result{"Not passed"};
    }

    std::cout << "Result: " << result << "\n";
}
```

1. **Predict** whether this program will build.
2. Build it.
3. Find the cause of the error.
4. Fix the program.
5. Explain why the fix works.

The program won't build. On line 16 the compiler reports `use of undeclared identifier 'result'`: it doesn't know the name `result`. You know this message from lessons 1.2 and 2.1, where it meant a typo or a missing declaration. Here the name is spelt correctly, and is even declared twice, but **inside the blocks** of the `if` and the `else`. On line 16, after the closing brace, neither of those declarations applies any more.

**The rule:** a variable declared inside a block `{ }` exists only in that block, from its declaration to the closing brace. Outside the block, its name is unknown.

**The correct pattern:** if a value is needed **after** the `if`/`else`, declare the variable **before** it, with a starting value, and in the branches only **assign** it the right value:

<!-- example: result_before_if -->
```cpp
#include <iostream>
#include <string>

int main() {
    int score{0};
    std::string result{""};

    std::cout << "Enter score:\n";
    std::cin >> score;

    if (score >= 50) {
        result = "Passed";
    } else {
        result = "Not passed";
    }

    std::cout << "Result: " << result << "\n";
}
```

<!-- input: result_before_if -->
```text
49
```

<!-- output: result_before_if -->
```text
Enter score:
Result: Not passed
```

<!-- input: result_before_if -->
```text
50
```

<!-- output: result_before_if -->
```text
Enter score:
Result: Passed
```

- `result` is declared in `main`, before the `if`, so it exists until the end of `main`, including after the `if`/`else`.
- The branches contain no new declaration, only assignment (lesson 2.2). That's why `result` can't be `const`: its value changes in a branch.
- If the result only needs to be **printed** in a branch, as in section 2, no extra variable is needed. Create one only when the value is needed later.

## 9. Mission: a mini quiz

Write a program with a short quiz of two questions:

1. The user gives one word: the name of the path a planet follows around the Sun. The correct answer is `orbit`.
2. The user gives a whole number. The program checks whether it is even.

The program judges **each question separately**.

In `cpp-workspace`, create a folder `mini_quiz`, copy `CMakeLists.txt` into it from the original `lesson_05_first_program`, create an empty `main.cpp`, and write the program on your own. Read the word first, then the number. Reading both with `std::cin >>` is enough, because the answer is a single word.

For the data `orbit` and `4`, the standard output must be:

<!-- input: mini_quiz -->
```text
orbit
4
```

<!-- output: mini_quiz -->
```text
Name the path of a planet around the Sun:
Enter a whole number:
Answer: correct
Number: even
```

The program must give the correct result for all these data sets, without changing the code:

| Word | Number | Expected last two lines |
|---|---|---|
| `orbit` | `4` | `Answer: correct`, `Number: even` |
| `orbit` | `7` | `Answer: correct`, `Number: odd` |
| `planet` | `10` | `Answer: incorrect`, `Number: even` |
| `Orbit` | `3` | `Answer: incorrect`, `Number: odd` |
| `orbit` | `0` | `Answer: correct`, `Number: even` |

<!-- input: mini_quiz -->
```text
orbit
7
```

<!-- output: mini_quiz -->
```text
Name the path of a planet around the Sun:
Enter a whole number:
Answer: correct
Number: odd
```

<details>
<summary>The other three test cases: standard output</summary>

<!-- input: mini_quiz -->
```text
planet
10
```

<!-- output: mini_quiz -->
```text
Name the path of a planet around the Sun:
Enter a whole number:
Answer: incorrect
Number: even
```

<!-- input: mini_quiz -->
```text
Orbit
3
```

<!-- output: mini_quiz -->
```text
Name the path of a planet around the Sun:
Enter a whole number:
Answer: incorrect
Number: odd
```

<!-- input: mini_quiz -->
```text
orbit
0
```

<!-- output: mini_quiz -->
```text
Name the path of a planet around the Sun:
Enter a whole number:
Answer: correct
Number: even
```

</details>

### Success criteria

- The program builds as C++20, and its standard output for all five data sets is exactly as in the table and the blocks above.
- The answer is a `std::string`, the number an `int`, and the expected word a `const std::string` constant.
- The word is compared with `==`, and evenness is checked with `%` and `==`.
- At least one comparison result is stored in a `bool` variable.
- There are two **separate** `if`/`else` constructs, each with braces.
- The same program gives all the results, without changing the code.
- You can explain why `Orbit` is judged incorrect and why 0 is even.

Once the output matches, you can save the project in Git, as in lesson 1.5.

<details>
<summary>Hint 1</summary>

Two questions are two separate decisions, as in section 7. Each has its own `if`/`else` and prints one of two lines.

</details>

<details>
<summary>Hint 2</summary>

You can store the result of comparing the word, and the result of checking evenness, in `bool` constants with meaningful names, like `is_even` in section 5, and use them as conditions.

</details>

An example solution is in [Example solutions](#example-solutions).

## 10. When something goes differently

| What you see | What it means | What to do |
|---|---|---|
| Both branches ran | The second branch isn't connected to the `if` by `else`; for example, it simply comes after the block. | The alternative branch is `else { … }`, right after the closing brace of the `if` block. |
| A compile error at `else` | `else` doesn't come right after the `if` block, or someone added a condition to it. | `else` has no condition, and must follow the `}` of the `if` block directly. |
| A variable suddenly has a different value, although it was only meant to be checked | There is an assignment `=` where the comparison should be. | Equality is checked with `==`, two characters. |
| The word looks correct, but the program says `incorrect` | The comparison distinguishes upper and lower case. | `Orbit` and `orbit` are different strings. Type the word exactly as the program expects. |
| The screen shows `1` or `0` instead of a word | The program printed a `bool` value. | That's how `true` and `false` are printed by default. Print words in the `if`/`else` branches. |
| A `bool` variable has an "old" answer | It stores the result calculated at initialisation. It doesn't follow later changes. | Calculate the comparison again after the data changes. |
| `use of undeclared identifier` for a variable from an `if` | The variable is declared in a block and used outside it. | Declare it before the `if`, and only assign it in the branches (section 8). |

## 11. Explain

Answer in your own words, preferably in writing. Only then compare with the example answer.

**1.** How does a plain `if` differ from `if`/`else`?

<details>
<summary>Example answer</summary>

A plain `if` runs its block or does nothing. `if`/`else` always runs exactly one of two branches: the `if` block when the condition is satisfied, or the `else` block when it isn't.

</details>

**2.** How does `count = 5;` differ from `count == 5`?

<details>
<summary>Example answer</summary>

`count = 5;` stores the value 5 in `count`. `count == 5` only checks whether `count` is equal to 5 and gives `true` or `false`. It changes nothing.

</details>

**3.** What does `const bool is_even{number % 2 == 0};` store, and will it change when you change `number` later?

<details>
<summary>Example answer</summary>

It stores `true` if `number` was even at the moment of initialisation, and `false` otherwise. It won't change: it's a stored answer, not a rule. After `number` changes, the comparison has to be calculated again.

</details>

**4.** A program printed `is_even: 1`. Is `is_even` of type `int`?

<details>
<summary>Example answer</summary>

No. `is_even` is of type `bool`. By default, `std::cout` prints `true` as `1` and `false` as `0`. You read the type from the code.

</details>

**5.** Why didn't the program in section 8 build, and how was it fixed?

<details>
<summary>Example answer</summary>

`result` was declared inside the `if` and `else` blocks, so it existed only in them. After the `if`/`else`, the name was unknown. The fix declares `result` before the `if`, and only assigns it a value in the branches.

</details>

## Summary

- `if`/`else` chooses **one of two** branches. `else` has no condition and runs when the condition at `if` isn't satisfied. After the chosen branch the program carries on.
- `==` checks equality and `!=` inequality, also for `std::string`. A comparison changes nothing. `=` is assignment, a different operation.
- Comparing `std::string` values distinguishes upper and lower case.
- The result of a comparison is of type `bool`: `true` or `false`. You can store it in a variable and use it as a condition. A stored value doesn't follow later changes in the data.
- By default, `std::cout` prints a `bool` as `1` or `0`. The variable is still a `bool`.
- A variable declared in a block exists only in it. Declare a value you need after the `if`/`else` before it, and assign it in the branches.
- Several separate `if`/`else` constructs make several separate decisions.

## What's next

Your program now chooses one of two ways. Sometimes, though, there are more possibilities: a grade can be A, B, C or D. In lesson 3.3 you'll meet `else if`, and learn to check every limit of such ranges: [Lesson 3.3: Choosing among many possibilities (`else if`)](lesson_03_many_possibilities.en.md).

---

## Example solutions

Look here **after your own attempt**. Your names may differ, as long as the standard output is as required.

<details>
<summary>Section 6: check yourself</summary>

1. `a == b` gives `true` when the values are equal. `a != b` gives `true` when they are different.
2. No. A comparison only checks, and gives `true` or `false`.
3. For two identical strings, `==` gives `true` and `!=` gives `false`. For two different ones it's the other way round: `==` gives `false` and `!=` gives `true`.
4. The forms:

| Requirement | Form |
|---|---|
| Set the number of points to 0. | `points = 0;` |
| Check whether the number of points is 0. | `points == 0` |
| Check whether the answer is something other than `comet`. | `answer != "comet"` |
| Change the answer to `comet`. | `answer = "comet";` |
| Check whether the number is odd. | `number % 2 != 0` |

</details>

<details>
<summary>Section 9: mission, the mini quiz</summary>

<!-- example: mini_quiz -->
```cpp
#include <iostream>
#include <string>

int main() {
    const std::string expected_answer{"orbit"};
    std::string answer{""};
    int number{0};

    std::cout << "Name the path of a planet around the Sun:\n";
    std::cin >> answer;
    std::cout << "Enter a whole number:\n";
    std::cin >> number;

    const bool is_correct{answer == expected_answer};
    const bool is_even{number % 2 == 0};

    if (is_correct) {
        std::cout << "Answer: correct\n";
    } else {
        std::cout << "Answer: incorrect\n";
    }

    if (is_even) {
        std::cout << "Number: even\n";
    } else {
        std::cout << "Number: odd\n";
    }
}
```

- `answer` is text, so a `std::string`. `number` is a whole number, so an `int`. The expected word doesn't change, so it's a constant.
- `is_correct` and `is_even` store the results of two comparisons. The data doesn't change after them, so they can be constants.
- Two separate `if`/`else` constructs make two separate decisions. Each prints one line.

</details>

**Previous lesson:** [Lesson 3.1: The program's first decision (`if`)](lesson_01_the_first_decision.en.md) · **Next lesson:** [Lesson 3.3: Choosing among many possibilities (`else if`)](lesson_03_many_possibilities.en.md) · [Course overview](../../README.en.md)

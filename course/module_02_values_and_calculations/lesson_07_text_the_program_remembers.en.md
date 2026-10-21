# Lesson 2.7: Text the program remembers (`std::string`)

[Polski](lesson_07_text_the_program_remembers.md) · **English** · [Course overview](../../README.en.md)

> **Module 2, lesson 7** · about 60–75 minutes
> **You need:** the `cpp-workspace` folder and the original `lesson_05_first_program` project, as before. You don't need the debugger in this lesson.
> **Pilot version.** The programs in this lesson are checked automatically on Windows, Ubuntu and macOS, including with the given input data.

## Before you start

This lesson assumes that after lessons 2.1–2.6:

- you create variables and constants with a starting value in `{}`, and change variables by assignment;
- you read numbers with `std::cin >>`, and run the same program with different data;
- you tell input data apart from the program's standard output (lesson 2.6, section 6).

## The situation

Your programs already remember and calculate numbers. Text has appeared in them only as a quoted string, printed straight away by `std::cout`. Today a program will start **storing text in a variable**: changing it, joining it with other text, and reading it from the user, including whole lines with spaces.

After this lesson you will:

- explain what `std::string` is for, and tell a text literal apart from a variable holding text;
- create `std::string` variables and constants, print them, and change them by assignment;
- join texts with the `+` operator, and tell that apart from printing several values with `<<`;
- read one word with `std::cin >>` and a whole line with `std::getline`;
- write, on your own, a program whose messages depend on the text that was typed.

## 1. Prepare the project

In `cpp-workspace`, create a folder `lesson_2_7` and copy `main.cpp` and `CMakeLists.txt` into it from the original `lesson_05_first_program`. You type the programs from sections 2–7 into that folder's `main.cpp`.

## 2. Text as a value

Since Module 1 you have printed text directly: `std::cout << "Hello!\n";`. Now store text in a variable:

<!-- example: text_variable -->
```cpp
#include <iostream>
#include <string>

int main() {
    std::string greeting{"Hello!"};
    std::string event_name{"Science Fair"};

    std::cout << greeting << "\n";
    std::cout << "Event: " << event_name << "\n";
}
```

<!-- output: text_variable -->
```text
Hello!
Event: Science Fair
```

- `"Hello!"` is a **text literal**: text written directly in the code, in quotes, as in Module 1.
- `std::string` is a **type from the standard library** that stores text. `greeting` is a variable of that type, and `{"Hello!"}` gives it its starting value, just as `{3}` does for an `int` variable.
- A literal and a variable are two different things, even though here they contain the same text. A literal is a fixed piece of the code. A `std::string` variable stores text that the program can change, join with other text, and read from the user.
- The text in a `std::string` can contain spaces, like `Science Fair`.
- `std::cout` prints text from a variable just as it prints a number.
- The `std::string` type needs the header **`#include <string>`**. Programs that print or read also need `#include <iostream>`, as before. Sometimes a program builds without `#include <string>`, because another header includes it along the way. Don't rely on that: if you use `std::string`, write `#include <string>`.

`std::string` can do more than `int` and `double`, because text can be of any length. For now you need only what's in this lesson.

## 3. Change the text

The assignment from lesson 2.2 works for text too:

<!-- example: status_change -->
```cpp
#include <iostream>
#include <string>

int main() {
    const std::string application_name{"My App"};
    std::string status{"Waiting"};

    std::cout << application_name << ": " << status << "\n";
    status = "Ready";
    std::cout << application_name << ": " << status << "\n";
}
```

**Predict** both lines of the output, then run the program.

<details>
<summary>The program's output</summary>

<!-- output: status_change -->
```text
My App: Waiting
My App: Ready
```

</details>

- `status = "Ready";` replaces the previous text with new text, just as assignment replaces a number. The first `std::cout` comes before the assignment, so it prints the old value.
- `application_name` is `const`, because the program's name shouldn't change. The rule from lesson 2.2 applies to text too. `greeting` from section 2 could also be `const`.

## 4. Join texts

The `+` operator can **join texts**:

<!-- example: join_text -->
```cpp
#include <iostream>
#include <string>

int main() {
    const std::string greeting{"Hello, "};
    const std::string name{"Ada"};

    const std::string message{greeting + name};

    std::cout << message << "\n";
    std::cout << greeting << name << "\n";
}
```

**Predict** the value of `message`, and what both `std::cout` lines print.

<details>
<summary>The program's output</summary>

<!-- output: join_text -->
```text
Hello, Ada
Hello, Ada
```

</details>

- `greeting + name` creates **new text**: `Hello, ` with `Ada` right after it. The space is at the end of `greeting`, so it ends up between the words. `+` doesn't add anything arithmetically here; it attaches one text to the other.
- **The meaning of the operator depends on the types of its operands**, as in lesson 2.5: for numbers `+` adds, and for two `std::string` values it joins.
- The result is stored in a new constant, `message`. It can then be printed, like any value.
- Both lines look the same on the screen, but the program does different things:
  - `std::cout << message` prints **one text, built beforehand**;
  - `std::cout << greeting << name` sends **two texts in turn** to the output, one after the other. No new text is created.
- So `<<` doesn't join texts the way `+` does. When text only needs to reach the screen, `<<` is enough. When you want to store it or use it further, build it with `+`.

**Literals and `+`.** In `greeting + name`, both operands are of type `std::string`. You can also attach a literal to a `std::string`, for example `greeting + "!"`. But `"Hello, " + "Ada"` doesn't join two `std::string` values, because a literal isn't a value of type `std::string`. That's why **in every `+`, at least one operand must be of type `std::string`**. In a longer expression this rule applies to each `+` separately, from left to right, as in lessons 2.4 and 2.5.

## 5. Predict: what does `std::cin >>` read?

You can read text from standard input just like a number:

<!-- example: read_one_word -->
```cpp
#include <iostream>
#include <string>

int main() {
    std::string name{""};

    std::cout << "Enter your name:\n";
    std::cin >> name;
    std::cout << "Name: " << name << "\n";
}
```

`{""}` is an empty text: a starting value that the read will replace. A variable for data isn't `const`, as in lesson 2.6.

**Predict** what the program prints when you type `Ola Nowak`. Write your answer down, then run the program.

<!-- input: read_one_word -->
```text
Ola Nowak
```

<details>
<summary>The program's standard output</summary>

<!-- output: read_one_word -->
```text
Enter your name:
Name: Ola
```

</details>

- `>>` reads **one word** into a `std::string`: it skips the spacing before it, and **a space ends the read**. So `name` gets `Ola`.
- The rest, ` Nowak`, hasn't disappeared. It's still in standard input, unread. This program simply doesn't use it.
- **This doesn't mean that a `std::string` can't hold spaces.** `event_name` in section 2 stores `Science Fair`. The limitation comes from the **read operation** `>>`, not from the type.

## 6. A whole line: `std::getline`

A full name or the name of an event usually contains spaces. To read a whole line, use `std::getline`:

<!-- example: read_full_line -->
```cpp
#include <iostream>
#include <string>

int main() {
    std::string full_name{""};

    std::cout << "Enter your full name:\n";
    std::getline(std::cin, full_name);
    std::cout << "Full name: " << full_name << "\n";
}
```

Run the program and type `Ada Lovelace`:

<!-- input: read_full_line -->
```text
Ada Lovelace
```

<!-- output: read_full_line -->
```text
Enter your full name:
Full name: Ada Lovelace
```

Now run it again and type the same as in section 5, `Ola Nowak`. **Predict** the result.

<!-- input: read_full_line -->
```text
Ola Nowak
```

<details>
<summary>The program's standard output</summary>

<!-- output: read_full_line -->
```text
Enter your full name:
Full name: Ola Nowak
```

</details>

- `std::getline` is a **function from the standard library**: a ready-made, named operation that you call, giving it in parentheses what it should use. You'll learn to write your own functions later. Here you just use a ready-made one.
- In the parentheses you give two things: **where to read from** (`std::cin`) and **where to store the text** (`full_name`, a variable of type `std::string`).
- `std::getline` reads **to the end of the line**, that is, up to where **Enter** was pressed. Spaces are part of the text it reads.
- The end-of-line character itself doesn't go into `full_name`: the variable stores `Ada Lovelace`, with nothing after it.

The same input, `Ola Nowak`, gave `Ola` in section 5 and `Ola Nowak` here. The difference comes from the **read method**, not from the data.

## 7. The same program, a different name

This program builds a greeting from the text it reads:

<!-- example: greeting_message -->
```cpp
#include <iostream>
#include <string>

int main() {
    std::string full_name{""};

    std::cout << "Enter your full name:\n";
    std::getline(std::cin, full_name);

    const std::string message{"Hello, " + full_name + "!"};

    std::cout << message << "\n";
}
```

Run it twice, **without changing the code**: once with `Ada Lovelace` and once with `Grace Hopper`.

<!-- input: greeting_message -->
```text
Ada Lovelace
```

<!-- output: greeting_message -->
```text
Enter your full name:
Hello, Ada Lovelace!
```

<!-- input: greeting_message -->
```text
Grace Hopper
```

<!-- output: greeting_message -->
```text
Enter your full name:
Hello, Grace Hopper!
```

- `"Hello, " + full_name` is a literal plus a `std::string`, so the result is of type `std::string`. The program then attaches `"!"` to it. Each `+` has at least one operand of type `std::string` (section 4).
- As in lesson 2.6: on the screen you'll also see the typed name between the program's lines. That's the echo of the window you type into. The standard output is only the two lines above.

## 8. Watch out: `getline` first, then `>>`

After a read with `std::cin >>`, the end of the line from the **Enter** you pressed stays in standard input. If the program called `std::getline` right after that, it could read only that empty line ending and get an empty text. You'll learn how to deal with this later.

For now, one rule is enough: **if a program reads text with `std::getline` and a number with `>>`, call `std::getline` first, and only then `>>`.** That's how the mission does it.

## 9. Mission: the participant badge

Write a program that prepares a simple badge for a participant at an event. The user gives:

1. the participant's full name, which can contain spaces;
2. a seat number, as a whole number.

The program prints the full name, the seat number, and a greeting with the full name.

In `cpp-workspace`, create a folder `participant_badge`, copy `CMakeLists.txt` into it from the original `lesson_05_first_program`, create an empty `main.cpp`, and write the program on your own.

**The first run:**

<!-- input: participant_badge -->
```text
Ada Lovelace
12
```

The standard output must be exactly:

<!-- output: participant_badge -->
```text
Enter participant name:
Enter seat number:
Participant: Ada Lovelace
Seat: 12
Welcome, Ada Lovelace!
```

**A second run of the same program,** without changing the code:

<!-- input: participant_badge -->
```text
Grace Hopper
8
```

<!-- output: participant_badge -->
```text
Enter participant name:
Enter seat number:
Participant: Grace Hopper
Seat: 8
Welcome, Grace Hopper!
```

### Success criteria

- The program builds as C++20, and its standard output for both sets of data is exactly as above.
- The program has `#include <string>` and `#include <iostream>`.
- The full name goes into a `std::string` variable through `std::getline`, and the seat number into an `int` variable through `std::cin >>`, **in that order**. Both variables have starting values and aren't `const`.
- The greeting `Welcome, …!` is **text built with `+`** and stored in a `std::string` constant.
- The code contains neither `Ada Lovelace`, `Grace Hopper`, 12 nor 8: the data comes from standard input.
- The program uses only what you already know.
- You can explain what in the program is text and what is a number, and why you read the name with `std::getline` and not with `>>`.

Once the output matches, you can save the project in Git, as in lesson 1.5.

<details>
<summary>Hint 1</summary>

The order is as in lesson 2.6: the variables for the data, then a request and a read for each value, and finally the resulting text and the output. Which read method keeps the space between the first name and the surname?

</details>

<details>
<summary>Hint 2</summary>

The greeting is the literal `"Welcome, "`, the full name and the literal `"!"`, joined with `+`. Don't join the seat number with `+`: print it with `<<`, like any number.

</details>

### Variant: a longer name

Run the same program for a participant whose name has several words. **Predict** the result before you see it.

<!-- input: participant_badge -->
```text
Mary Ann Evans
3
```

<details>
<summary>The program's standard output</summary>

<!-- output: participant_badge -->
```text
Enter participant name:
Enter seat number:
Participant: Mary Ann Evans
Seat: 3
Welcome, Mary Ann Evans!
```

</details>

The program works without changes to the code, because `std::getline` reads the whole line, however many spaces it has.

An example solution is in [Example solutions](#example-solutions).

## 10. When something goes differently

| What you see | What it means | What to do |
|---|---|---|
| The compiler doesn't know `std::string` or `std::getline` | A header is missing. | Write `#include <string>`. Even if the program builds without it, don't rely on that. |
| From `Ada Lovelace` the program kept only `Ada` | The text was read with `>>`, which reads one word. | For a whole line, use `std::getline(std::cin, …)`. |
| The words in the joined text are stuck together, for example `Hello,Ada` | `+` attaches texts exactly as they are. A space doesn't appear by itself. | Add a space in one of the texts, for example `"Hello, "`. |
| A compile error at `+` with two quoted texts | Two literals aren't `std::string` values (section 4). | At least one operand of each `+` must be of type `std::string`. Or print the texts with `<<`. |
| `std::getline` read an empty text, although a name was typed | Before `std::getline` there was a read with `>>`, and it left the line ending behind (section 8). | `std::getline` first, then `>>`. |
| The typed text appears on the screen twice, or between the program's lines | One occurrence is echo, not the program's output (lesson 2.6). | Nothing. The standard output is only what `std::cout` prints. |
| Letters with accents, or other characters outside the basic alphabet, display strangely | Displaying such characters depends on the system and console settings. | In this lesson, use letters without accents in the data, for example `Lukasz` instead of `Łukasz`. You'll work with such characters later. |

## 11. Explain

Answer in your own words, preferably in writing. Only then compare with the example answer.

**1.** How does `"Hello!"` differ from `greeting` in `std::string greeting{"Hello!"};`?

<details>
<summary>Example answer</summary>

`"Hello!"` is a text literal: text written directly in the code. `greeting` is a variable of type `std::string`, which stores a copy of that text as its starting value. The variable's value can then be changed by assignment, joined with other text, or read from the user.

</details>

**2.** `std::cout << message` and `std::cout << greeting << name` printed the same thing. How do they differ?

<details>
<summary>Example answer</summary>

`message` is one text, built beforehand with `+` and stored in a variable. In the second statement, `<<` sends two separate texts to the output, one after the other, and no new text is created.

</details>

**3.** Why did the program in section 5 keep only `Ola` after `Ola Nowak` was typed? Does it mean that a `std::string` can't hold spaces?

<details>
<summary>Example answer</summary>

Because `>>` reads one word into a `std::string` and stops at a space. A `std::string` can hold spaces: `event_name` stores `Science Fair`, and `std::getline` reads `Ola Nowak` in full. The limitation comes from the read method.

</details>

**4.** What does `std::getline(std::cin, full_name);` do?

<details>
<summary>Example answer</summary>

It reads a whole line from standard input, up to the end of the line, spaces included, and stores it in `full_name`. The end-of-line character itself doesn't go into the variable.

</details>

**5.** Why does the mission read the full name before the seat number?

<details>
<summary>Example answer</summary>

Because after a number is read with `>>`, the line ending stays in the input, and `std::getline` called afterwards could read an empty text. When `std::getline` runs first and `>>` after it, the problem doesn't occur.

</details>

## Summary

- `std::string` stores text in a variable. It needs `#include <string>`. A quoted text literal and a `std::string` variable are different things, even though they can contain the same text.
- You initialise a `std::string` variable in `{}`, change it by assignment, and print it with `std::cout`. Text that shouldn't change is marked `const`.
- `+` joins texts when at least one operand of each `+` is of type `std::string`. It creates new text. `<<` only sends values to the output one after another.
- `std::cin >>` reads one word into a `std::string`. `std::getline(std::cin, …)` reads a whole line with its spaces, without the end-of-line character.
- A `std::string` can hold spaces. The one-word limit comes from `>>`, not from the type.
- When a program reads text and a number: `std::getline` first, then `>>`.

## What's next

You now know all the tools of Module 2: whole and fractional numbers, text, calculations, constants, data from the user, and ways of finding errors in results. In lesson 2.8 you'll test them in an independent task. **Lesson 2.8 is in preparation.**

---

## Example solutions

Look here **after your own attempt**. Your names may differ, as long as the standard output is as required.

<details>
<summary>Section 9: mission, the participant badge</summary>

<!-- example: participant_badge -->
```cpp
#include <iostream>
#include <string>

int main() {
    std::string participant_name{""};
    int seat_number{0};

    std::cout << "Enter participant name:\n";
    std::getline(std::cin, participant_name);
    std::cout << "Enter seat number:\n";
    std::cin >> seat_number;

    const std::string welcome{"Welcome, " + participant_name + "!"};

    std::cout << "Participant: " << participant_name << "\n";
    std::cout << "Seat: " << seat_number << "\n";
    std::cout << welcome << "\n";
}
```

- `participant_name` is of type `std::string`, because it's text that can contain spaces. That's why `std::getline` reads it. `seat_number` is of type `int`, because a seat number is a whole number. `>>` reads it.
- `std::getline` comes before `>>`, so there's no problem with a leftover line ending.
- `welcome` is new text built with `+`. It doesn't change after it's built, so it's `const`. The seat number reaches the screen through `<<`, without being joined to text.

</details>

**Previous lesson:** [Lesson 2.6: A program that asks the user](lesson_06_a_program_that_asks_the_user.en.md) · **Next lesson:** in preparation · [Course overview](../../README.en.md)

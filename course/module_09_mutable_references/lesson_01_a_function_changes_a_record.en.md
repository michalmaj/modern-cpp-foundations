# Lesson 9.1: A function changes an existing record

[Polski](lesson_01_a_function_changes_a_record.md) · **English** · [Course overview](../../README.en.md)

> **Module 9, lesson 1** · about 65–80 minutes
> **You need:** your `cpp-workspace` folder and the original `lesson_05_first_program` project, as before. You won't need the debugger in this lesson.
> **Pilot version.** The programs in this lesson are checked automatically on Windows, Ubuntu and macOS. None of them asks for data: all the values are written in the code. Only the check program in the solutions part reads data from the input.

## Before you start

This lesson assumes that:

- you know that a parameter passed by value is the function's own value, and that changing it doesn't change the variable at the call site (lesson 5.2);
- you know that a `void` function passes back no result but can have an effect, for example printing a text (lesson 5.1);
- you know the `const&` parameter, through which a function reads an existing object without copying it (lessons 6.4 and 8.3);
- you change the fields of an object without `const`, and create a copy of a record with `Product copy{original};` (lesson 8.2).

## The situation

A warehouse stores the product `Tea` with a stock of 3 units. A delivery of 4 units arrives. The stock of **the same product** should rise to 7. This isn't about a new product, or a separate record with a "second version" of the tea, but about changing the `stock` field in the record that already exists.

What can you do already?

- In lesson 8.2 the fields changed directly in `main`: `tea.stock += 4;`. That works, but then the delivery rule stands in every place that performs it.
- In lessons 8.3 and 8.4 functions got a record through `const&`. They could read it, but not change it.
- In lesson 8.5 a function created a new record with a result and returned it. That's a good design when a separate result is needed. Here, though, the result is to be **the changed state of the existing product**.

What's needed is a function whose caller **allows it to change an existing object**. In this lesson you'll meet the parameter that writes such an agreement into the function's header.

After this lesson you'll:

- tell a parameter passed by value from one passed by `const&` and one passed by `&`;
- write a `void` function with a `Product&` parameter that changes a field of the record it gets;
- explain which object the function changes, and why the change stays after returning to `main`;
- predict the state of a record before a call and after successive calls;
- explain why a `const` object can't go into a function with a `&` parameter;
- choose `const&` when a function only reads, and `&` when its job is to change;
- choose data that reveal that a function changes a copy instead of the original.

## 1. Prepare the project

In `cpp-workspace`, create a folder `lesson_9_1` and copy `main.cpp` and `CMakeLists.txt` from the original `lesson_05_first_program` into it. You type the program from section 2 into this folder's `main.cpp`. The `Product` type comes from Module 8.

## 2. The `Product&` parameter

<!-- example: delivery -->
```cpp
#include <iostream>
#include <string>

struct Product {
    std::string name;
    int stock;
    int minimum;
    int unit_price;
};

void receive_delivery(Product& product, int delivered) {
    product.stock += delivered;
}

int main() {
    Product tea{"Tea", 3, 8, 6};

    std::cout << "Product: " << tea.name << "\n";
    std::cout << "Before: " << tea.stock << "\n";

    receive_delivery(tea, 4);

    std::cout << "After: " << tea.stock << "\n";
}
```

**Predict** all three lines, then run the program. In particular: what is `tea.stock` after the call?

<details>
<summary>Standard output</summary>

<!-- output: delivery -->
```text
Product: Tea
Before: 3
After: 7
```

</details>

| Part | Meaning |
|---|---|
| `Product` | the parameter's type: our record |
| `&` | the parameter refers to an existing object from the call site; it isn't a copy of it |
| no `const` | through this parameter the function may change the fields of that object |
| `product` | the name through which the function reads and changes the fields: `product.stock` |

- **`tea` has no `const`,** because the delivery is meant to change its state.
- **During the call `receive_delivery(tea, 4)` the name `product` is another name for the object `tea`.** The function gets no copy, only access to the same record.
- **`product.stock += delivered;` changes the real field of `tea`,** which is why `main` reads 7 after the return.
- **The other fields don't change.** The function changes only `stock`: `name`, `minimum` and `unit_price` keep the values they had before the call.
- **The `void` result,** because the function gives back no separate value. Its effect is the changed state of the object, which `main` sees after the call. In the next lesson a function that changes a record will also return a result: one doesn't rule out the other.
- **The number of units by value:** the function only reads `int delivered`, so its own value is enough, as in lesson 5.2.

`Product& product` doesn't mean "we remove the `const`". It's an **agreement**: the caller allows the function to change the object it passes. That's why the header tells anyone reading the program that `tea` may look different after the call.

## 3. How the call runs

| Step | What happens | `tea.stock` |
|---|---|---:|
| 1 | `main` creates `tea` | 3 |
| 2 | `receive_delivery(tea, 4)` starts: `product` refers to `tea`, `delivered` gets 4 | 3 |
| 3 | the function reads `product.stock`, that is, the field of `tea` | 3 |
| 4 | `product.stock += delivered;` changes that field | 7 |
| 5 | the function ends, and the name `product` stops existing | 7 |
| 6 | `main` reads `tea.stock` | 7 |

The name `product` exists only during the call, but it changed a field of the object `tea`, which existed before and goes on existing. That's why the change stays. The by-value parameter of lesson 5.2 worked differently: the function changed its own value, and after the return the variable in `main` had its old value.

## 4. Three ways of passing a record

| Parameter | What does the function get? | Does changing a field through the parameter affect the original? |
|---|---|---|
| `Product product` | a separate parameter object, passed by value | no |
| `const Product& product` | read access to an existing object | it can't be changed through this parameter |
| `Product& product` | access to an existing object, with the right to change it | yes |

- **Passing by value is valid C++.** The function may change its parameter object, but that change doesn't affect the original.
- **`const&` restricts only this access.** The function won't change the object through the parameter, but the original itself may change elsewhere, for example in `main`, if it isn't `const` (lesson 8.3).
- **`&` gives a right, not a duty.** A function with a `Product&` parameter may change the record, but its code decides what it really does. For 0 delivered units, `receive_delivery` changes nothing.

**Which one when?** When a function only reads a record, choose `const&`, as in Module 8: the header then promises that it changes nothing, and the compiler enforces it. When the function's job is to change an existing object, choose `&`. When a separate result is needed and the original must stay unchanged, the function can get `const&` and return a new record, as in lesson 8.5. These are three different agreements, not a better and a worse version of the same thing.

## 5. A `const` object won't go into `Product&`

This program differs from the program in section 2 by one word: `tea` has `const`. **Predict** whether it builds. You can check it, but you don't have to.

<!-- broken: delivery_const_tea at=21:5 errors=1 error=^no matching function for call to 'receive_delivery' -->
```cpp
#include <iostream>
#include <string>

struct Product {
    std::string name;
    int stock;
    int minimum;
    int unit_price;
};

void receive_delivery(Product& product, int delivered) {
    product.stock += delivered;
}

int main() {
    const Product tea{"Tea", 3, 8, 6};

    std::cout << "Product: " << tea.name << "\n";
    std::cout << "Before: " << tea.stock << "\n";

    receive_delivery(tea, 4);

    std::cout << "After: " << tea.stock << "\n";
}
```

<details>
<summary>What the compiler reports and why</summary>

The program doesn't build. The compiler reports at line 21 `no matching function for call to 'receive_delivery'` and adds a note that the first argument, `const Product`, would lose its `const`.

- **The rejection is right.** The `const` on `tea` promises that this object won't change. A function with a `Product&` parameter asks for the right to change it. If the compiler called it, it would break the first promise.
- **Don't remove the `const` just to silence the compiler.** If the object really must stay unchanged, this function isn't for it.
- **If the operation really is meant to change the state, the object should be modifiable on purpose,** like `tea` in section 2. Then removing the `const` is a decision about that object, not a way around a message.

A function with a `const Product&` parameter would accept a `const` object without a problem: it promises only to read.

</details>

## 6. Mission: a study log

The program stores one record with the study progress so far: the topic, the total number of minutes and the number of sessions recorded. After each new session the same record is to be updated.

**Data:** the topic `C++`, 90 minutes in total over 2 sessions. Then two new sessions: 35 minutes and 20 minutes.

**Rules:**

- The topic is a non-empty ASCII text. The total number of minutes and the number of sessions are non-negative whole numbers.
- A new session lasts from 1 to 120 minutes. The data meet these assumptions, so the program doesn't check them.
- **Recording a session** adds its time to the total number of minutes and increases the number of sessions by 1. The topic doesn't change.

**Requirements:**

- The program defines a type of its own with three fields: the topic (`std::string`), the total number of minutes (`int`) and the number of sessions (`int`). You choose the names of the type and the fields on your own.
- `main` has **one** object of this type. The program creates no new objects for later states.
- The program has one function of its own, which records one session: it gets the existing record and the session's length, changes the record and returns `void`. It prints nothing and reads nothing from the input. You choose the names of the function and the parameters on your own.
- `main` calls this function **twice for the same object**: first for 35 minutes, then for 20.
- The program prints exactly four lines, as in the example below: `Topic`, `Before` before the first call, `After first` after the first and `After second` after the second. The numbers come from the record's fields as read at that moment. The words `minutes` and `sessions` always stay in the same form, also for the number 1.
- The program reads nothing from the input.

In `cpp-workspace`, create a folder `study_log`, copy `CMakeLists.txt` from the original `lesson_05_first_program` into it, create an empty `main.cpp` and write the program on your own.

For the data above, the standard output must be:

<!-- output: study_log -->
```text
Topic: C++
Before: 90 minutes, 2 sessions
After first: 125 minutes, 3 sessions
After second: 145 minutes, 4 sessions
```

The first session gives 90 + 35, that is 125 minutes, and the third session. The second adds 20 minutes to the **already changed** state: 145 minutes and the fourth session.

**This isn't the product program with other names.** You have to decide on your own:

1. what to call the type, its fields and the function;
2. why the object in `main` has no `const`;
3. which parameter gets the record: by value, by `const&` or by `&`, and why;
4. how to pass the session's length;
5. why the function returns `void`;
6. which two fields the function changes, and which one it doesn't touch;
7. how to call the function a second time so that the change also builds on the result of the first session;
8. where in `main` to print each line so that it shows the state from the right moment.

**Before you write the program**, prepare a table of cases: the data in the requirements, zeros at the start and one session, zeros at the start and two sessions, two sessions of the same length, sessions of 1 and of 120 minutes. For each, write down all the lines of the report.

**Then** run the program for the data in the requirements and for one other case from the table, for example the zeros at the start. Change only the values in the braces and the session lengths. Every case in the full list of check cases is checked automatically.

### Success criterion

- The program builds as C++20 and, for the data in the requirements, prints exactly the four lines shown above.
- There is one type with three fields and one modifiable object of that type.
- The function gets the record by `&` and the session's length by value, returns `void`, changes two fields and doesn't change the topic. It prints nothing and reads nothing.
- Both calls concern the same object, and the second builds on the result of the first.
- The table of cases was made before running the program.
- You can explain why the parameter has no `const` and why it isn't passed by value.

When the result matches, you can save the project in Git, as in lesson 1.5.

<details>
<summary>Hint 1</summary>

Is the new session meant to change the existing log, or to create a separate result? Which way of passing the record matches that responsibility?

</details>

<details>
<summary>Hint 2</summary>

The function must change two fields of one existing object. Think about how a `T` parameter differs from a `T&` one.

</details>

<details>
<summary>Hint 3</summary>

After recording a session, increase the total number of minutes and the number of sessions. Call the function again on the same record, so that the second update builds on the first.

</details>

<details>
<summary>The full list of check cases: open it after preparing your own table</summary>

The "After the sessions" column gives the state after each successive session: the minutes and the number of sessions.

| | Topic | At the start | Sessions | After the sessions | What it checks |
|---|---|---|---|---|---|
| A | `C++` | 90 min, 2 sessions | 35, 20 | 125/3, 145/4 | the data in the requirements |
| B | `Rust` | 0 min, 0 sessions | 45 | 45/1 | zeros at the start and one session |
| C | `Python` | 0 min, 0 sessions | 30, 30 | 30/1, 60/2 | zeros at the start and two sessions of the same length |
| D | `SQL` | 60 min, 1 session | 15 | 75/2 | a non-zero state and one session |
| E | `Git` | 10 min, 1 session | 5, 25 | 15/2, 40/3 | two sessions of different lengths |
| F | `Math` | 0 min, 0 sessions | 1, 120 | 1/1, 121/2 | the shortest and the longest session |
| G | `Modern C++` | 100 min, 4 sessions | 20, 20, 20 | 120/5, 140/6, 160/7 | three sessions: each adds to the earlier ones; a topic with a space |
| H | `Art` | 15 min, 1 session | none | no change | no new session |

In every case the topic after the sessions is the same as at the start.

**Automatic tests and your own runs.** Every case is checked automatically by a check program. It has the same type and the same function as the reference solution, but it reads the starting state and the session lengths from the input, and prints the state after each session. It's only a checking tool, not part of the mission: in the mission, the data are written in the code, and there are exactly two sessions. The check program and its results are in [Example solutions](#example-solutions), because they contain the solution.

</details>

The example solution is in [Example solutions](#example-solutions).

## 7. Find the bug: a copy changes

Do this task **after the mission**: the program below is meant to take a delivery, like the program in section 2. You can type it in or copy it into `main.cpp`.

<details>
<summary>The program to check: open it after writing your own program</summary>

<!-- example: delivery_copy_bug -->
```cpp
#include <iostream>
#include <string>

struct Product {
    std::string name;
    int stock;
    int minimum;
    int unit_price;
};

void receive_delivery(Product product, int delivered) {
    product.stock += delivered;
}

int main() {
    Product tea{"Tea", 3, 8, 6};
    const int delivered{0};

    std::cout << "Product: " << tea.name << "\n";
    std::cout << "Before: " << tea.stock << "\n";

    receive_delivery(tea, delivered);

    std::cout << "After: " << tea.stock << "\n";
}
```

1. Point to the parameter that is passed by value.
2. **Predict** whether `product.stock += delivered;` changes the field of the parameter object.
3. **Predict** whether this change affects `tea.stock` in `main`.
4. Run the program for the data in the program, that is, a delivery of 0 units. Does the result look right?
5. Change the value of `delivered` so that the bug shows. First write down the correct result for your value, then run the program.
6. Explain why changing the parameter object isn't enough.
7. Fix the parameter.
8. Run the fixed program for your value. Predict what it prints for 0.
9. Would a `const Product& product` parameter be enough here too? Why?

</details>

The results, an example value and the fixed program are in [Example solutions](#example-solutions).

## 8. When something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `After` shows the old value, although the function increases the field | The function gets the record by value and changes its own parameter object (section 7). | If the function must change the original, pass it by `&`. |
| `no matching function for call to ...` with the note `would lose const qualifier` | A `const` object goes into a function with a `&` parameter (section 5). | Decide whether the object is meant to change. If so, remove the `const` from the object. If not, don't call a changing function for it. |
| `cannot assign to variable ... with const-qualified type` in the function | The parameter has `const&`, and the function tries to change a field. | A function that is meant to change the record needs a `&` parameter without `const`. |
| After the second call only the last session shows | The function assigns the session's length (`=`) instead of adding it (`+=`). | Add the new session's time to the total so far. |
| The number of sessions doesn't change | The function updates only the minutes. | Recording a session changes two fields: the minutes and the number of sessions. |
| The second `After` line shows the state without the first session | The second call concerns another object, for example a copy made earlier. | Call the function twice for the same object. |
| `Before` already shows the changed values | `Before` is printed after the call. | Print the starting state before the first call. |

## 9. Explain

Answer in your own words, preferably in writing. Only then compare with the example answers.

1. How do the parameters `Product product`, `const Product& product` and `Product& product` differ?
2. What does `Product& product` mean for the caller? Why is it not just "a parameter without `const`"?
3. Why, after the call `receive_delivery(tea, 4)`, does `main` see the new value of `tea.stock`, although the name `product` no longer exists?
4. How does the copy of a record from lesson 8.2 differ from a `Product&` parameter?
5. Why does the function `receive_delivery` return `void`? How does `main` know what changed?
6. The function changes `stock`. What happens to the other fields? Why does that matter in the mission?
7. Why does the second call in the mission build on the first session?
8. Why can't a `const` object be passed to a function with a `&` parameter? When is removing the `const` a good decision, and when isn't it?
9. Why isn't a delivery of 0 units enough to check whether the function changes the original?
10. When is it better to write a function that returns a new record instead of changing an existing one? Why shouldn't every function get `&`?

<details>
<summary>Example answers</summary>

1. By value, the function gets a separate parameter object, so its changes don't affect the original. By `const&`, it gets read-only access to an existing object. By `&`, it gets access to an existing object and may change its fields.
2. That the caller allows the function to change the object passed and, after the call, has to reckon with the changed state. It's an agreement written in the header: a function with `const&` promises only to read, while a function with `&` may change.
3. Because `product` was only another name for the object `tea`. The function changed a field of `tea`, not its own copy. When the name `product` disappears, the object `tea` goes on existing, with the changed field.
4. A copy is a new, independent object with the original's values: its changes don't affect the original. A `Product&` parameter isn't a new object but another name for an existing one, so every change through it affects the original.
5. Because it gives back no separate value: its effect is the changed state of the record. `main` sees that effect by reading the object's fields after the call.
6. They stay as they were: the function changes only the fields its code names. In the mission the topic must stay the same, and only the minutes and the number of sessions change.
7. Because both calls get the same object by `&`. The first changes its fields, and the second starts from the already changed state.
8. Because `const` promises that the object won't change, while a `&` parameter gives the right to change it. The compiler doesn't allow that promise to be broken. Removing the `const` is good when the object really is meant to change. It isn't good when the only aim is to silence the compiler.
9. Because adding 0 changes nothing: a function that changes a copy and one that changes the original give the same result. The difference shows only with a positive delivery.
10. When a separate result is needed and the original must stay unchanged, for example when the state before and after the change must both be shown, or when the result is a different kind of data, like the report in lesson 8.5. A function that only reads should get `const&`: then its header promises that it changes nothing, and the compiler enforces it.

</details>

## Summary

- A `Product& product` parameter gives the function access to an existing object, with the right to change it. During the call, `product` is another name for the object passed.
- Changing a field through such a parameter changes the original, and the change stays after the function returns. Fields the function doesn't change stay as they were.
- `&` is an agreement: the caller allows the function to change the object. A `const` object can't go into such a function.
- By value the function gets a separate object, and by `const&` only read access. The choice depends on the function's job.
- A `void` function can have an effect: the changed state of a record, which the caller reads after the call.
- Successive calls on the same object start from the state left by the earlier ones.

## What's next

In this lesson the function always changed the record, with no conditions. In the next lesson a function will first check whether a change is allowed, leave the record unchanged if it refuses, and return information about success. It's in preparation.

---

## Example solutions

Look here **after your own attempt**. Your names may differ, as long as the standard output is as required.

<details>
<summary>Section 6: the mission, a study log</summary>

<!-- example: study_log -->
```cpp
#include <iostream>
#include <string>

struct StudyLog {
    std::string topic;
    int total_minutes;
    int sessions;
};

void record_session(StudyLog& progress, int minutes) {
    progress.total_minutes += minutes;
    ++progress.sessions;
}

int main() {
    StudyLog progress{"C++", 90, 2};

    std::cout << "Topic: " << progress.topic << "\n";
    std::cout << "Before: " << progress.total_minutes << " minutes, " << progress.sessions << " sessions\n";

    record_session(progress, 35);
    std::cout << "After first: " << progress.total_minutes << " minutes, " << progress.sessions << " sessions\n";

    record_session(progress, 20);
    std::cout << "After second: " << progress.total_minutes << " minutes, " << progress.sessions << " sessions\n";
}
```

1. **The record without `const`,** because each session is meant to change its state.
2. **The parameter with `&`,** because the function is meant to change the existing log, not its own copy.
3. **No `const` in the parameter,** because `const&` would allow only reading, and the function changes two fields.
4. **`void`,** because the function gives back no separate value. Its effect is the changed record, which `main` reads after the call.
5. **The session's length by value,** because the function only reads it. It's a plain number, as in lesson 5.2.
6. **Two fields,** because one session means both extra minutes and one more session. Changing only one of them would leave an inconsistent log.
7. **The topic unchanged,** because the function doesn't touch it. Only the fields named in its code change.
8. **The second call sees the first,** because both concern the same object `progress`. The second session adds 20 minutes to 125, not to 90.
9. **A parameter by value** would change the parameter object: every line of the report would show 90 minutes and 2 sessions, as in the diagnostic in section 7.
10. **No new record,** because the log is meant to show the current progress, and the program doesn't have to store earlier states. Each line of the report is produced at the moment when the state is current.
11. **When a new record would be better:** if the program had to compare the state before and after a session, or keep the original unchanged. Then the function could get `const&` and return a new record, as in lesson 8.5, or `main` could make a copy before the change, as in lesson 8.2.

**Other correct solutions:** instead of `++progress.sessions;` you can write `progress.sessions += 1;`. The fields may have other names and another order, as long as the values in `{}` stand in the same order as the fields. The session lengths may stand in `const int` variables in `main`.

**The check program** checks every case in the list of check cases. The type and the function are the same as above. The difference is in `main`: the program reads the topic, the starting state and the session lengths from the input, calls the function for each session on the same object, prints the state after each, and finally prints the topic. The topic is read by `std::getline`, because it may contain a space, and the numbers by `>>`, only after it, as in the check program of lesson 8.2. The session lengths first go into an `int` vector with `push_back` (lesson 6.2), so that the program can check the reading before it changes anything. The mission needs neither input nor a vector.

<!-- example: study_log_check -->
```cpp
#include <iostream>
#include <string>
#include <vector>

struct StudyLog {
    std::string topic;
    int total_minutes;
    int sessions;
};

void record_session(StudyLog& progress, int minutes) {
    progress.total_minutes += minutes;
    ++progress.sessions;
}

int main() {
    std::string topic{};
    int total_minutes{0};
    int sessions{0};
    int count{0};
    std::vector<int> lengths{};

    std::getline(std::cin, topic);
    std::cin >> total_minutes;
    std::cin >> sessions;
    std::cin >> count;

    for (int number{1}; number <= count; ++number) {
        int minutes{0};
        std::cin >> minutes;
        lengths.push_back(minutes);
    }

    if (std::cin.fail()) {
        std::cout << "Input could not be read\n";
    } else {
        StudyLog progress{topic, total_minutes, sessions};

        std::cout << "Before: " << progress.total_minutes << " minutes, " << progress.sessions << " sessions\n";

        int number{0};

        for (const int minutes : lengths) {
            record_session(progress, minutes);
            ++number;
            std::cout << "After session " << number << ": " << progress.total_minutes << " minutes, " << progress.sessions << " sessions\n";
        }

        std::cout << "Topic: " << progress.topic << "\n";
    }
}
```

Each case is the topic on the first line, then the total number of minutes, the number of sessions, the number of new sessions and their lengths, in the order of the list of check cases, from A to H.

<!-- input: study_log_check -->
```text
C++
90
2
2
35
20
```

<!-- output: study_log_check -->
```text
Before: 90 minutes, 2 sessions
After session 1: 125 minutes, 3 sessions
After session 2: 145 minutes, 4 sessions
Topic: C++
```

<!-- input: study_log_check -->
```text
Rust
0
0
1
45
```

<!-- output: study_log_check -->
```text
Before: 0 minutes, 0 sessions
After session 1: 45 minutes, 1 sessions
Topic: Rust
```

<!-- input: study_log_check -->
```text
Python
0
0
2
30
30
```

<!-- output: study_log_check -->
```text
Before: 0 minutes, 0 sessions
After session 1: 30 minutes, 1 sessions
After session 2: 60 minutes, 2 sessions
Topic: Python
```

<!-- input: study_log_check -->
```text
SQL
60
1
1
15
```

<!-- output: study_log_check -->
```text
Before: 60 minutes, 1 sessions
After session 1: 75 minutes, 2 sessions
Topic: SQL
```

<!-- input: study_log_check -->
```text
Git
10
1
2
5
25
```

<!-- output: study_log_check -->
```text
Before: 10 minutes, 1 sessions
After session 1: 15 minutes, 2 sessions
After session 2: 40 minutes, 3 sessions
Topic: Git
```

<!-- input: study_log_check -->
```text
Math
0
0
2
1
120
```

<!-- output: study_log_check -->
```text
Before: 0 minutes, 0 sessions
After session 1: 1 minutes, 1 sessions
After session 2: 121 minutes, 2 sessions
Topic: Math
```

<!-- input: study_log_check -->
```text
Modern C++
100
4
3
20
20
20
```

<!-- output: study_log_check -->
```text
Before: 100 minutes, 4 sessions
After session 1: 120 minutes, 5 sessions
After session 2: 140 minutes, 6 sessions
After session 3: 160 minutes, 7 sessions
Topic: Modern C++
```

<!-- input: study_log_check -->
```text
Art
15
1
0
```

<!-- output: study_log_check -->
```text
Before: 15 minutes, 1 sessions
Topic: Art
```

</details>

<details>
<summary>Section 7: the results before the fix, and the fixed program</summary>

Before the fix, for a delivery of 0 units:

<!-- output: delivery_copy_bug -->
```text
Product: Tea
Before: 3
After: 3
```

- **The parameter by value:** `Product product`. At the call, a separate parameter object is created with the values of the fields of `tea`.
- **For 0 the result looks right,** because a delivery of 0 units changes nothing: the correct function would also leave 3.
- **Data that reveal the bug:** any positive delivery. For example 4: inside the function `product.stock` ends at 7, but `tea.stock` is still 3 after the return. The correct result is `After: 7`. The program with the bug prints:

<!-- example: delivery_copy_revealed -->
```cpp
#include <iostream>
#include <string>

struct Product {
    std::string name;
    int stock;
    int minimum;
    int unit_price;
};

void receive_delivery(Product product, int delivered) {
    product.stock += delivered;
}

int main() {
    Product tea{"Tea", 3, 8, 6};
    const int delivered{4};

    std::cout << "Product: " << tea.name << "\n";
    std::cout << "Before: " << tea.stock << "\n";

    receive_delivery(tea, delivered);

    std::cout << "After: " << tea.stock << "\n";
}
```

<!-- output: delivery_copy_revealed -->
```text
Product: Tea
Before: 3
After: 3
```

| Moment | `product.stock` in the function | `tea.stock` in `main` |
|---|---:|---:|
| before the call | doesn't exist | 3 |
| at the start of the function | 3 | 3 |
| after `+=` | 7 | 3 |
| after the return | doesn't exist | 3 |

- **The cause:** the function changes its own parameter object, not `tea`. Passing by value is valid C++, but it doesn't fit the function's job: the delivery is meant to change the existing product. The compiler reports no error, because changing the parameter object is allowed.
- **The fix:** the parameter `Product& product`. The function then gets access to `tea`, not a copy.

<!-- example: delivery_copy_fixed -->
```cpp
#include <iostream>
#include <string>

struct Product {
    std::string name;
    int stock;
    int minimum;
    int unit_price;
};

void receive_delivery(Product& product, int delivered) {
    product.stock += delivered;
}

int main() {
    Product tea{"Tea", 3, 8, 6};
    const int delivered{4};

    std::cout << "Product: " << tea.name << "\n";
    std::cout << "Before: " << tea.stock << "\n";

    receive_delivery(tea, delivered);

    std::cout << "After: " << tea.stock << "\n";
}
```

<!-- output: delivery_copy_fixed -->
```text
Product: Tea
Before: 3
After: 7
```

For 0 the fixed program prints the same as before the fix: `After: 3`. That's why a delivery of 0 units isn't enough to check which object the function changes.

**A `const Product& product` parameter wouldn't be enough here.** The function would get access to `tea`, but only for reading, so the line `product.stock += delivered;` wouldn't build: the compiler would report `cannot assign to variable 'product' with const-qualified type 'const Product &'`, as in lesson 8.3. `const&` suits functions that only read. A function that takes a delivery is meant to change, so it needs `&`.

</details>

**Previous lesson:** [Lesson 8.6: Race results (the Module 8 test)](../module_08_structs/lesson_06_race_results.en.md) · **Next lesson:** in preparation · [Course overview](../../README.en.md)

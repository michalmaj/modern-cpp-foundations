# Lesson 8.2: Changing fields and an independent copy of a record

[Polski](lesson_02_changing_fields_and_copies.md) · **English** · [Course overview](../../README.en.md)

> **Module 8, lesson 2** · about 65–80 minutes
> **You need:** your `cpp-workspace` folder and the original `lesson_05_first_program` project, as before. You won't need the debugger in this lesson.
> **Pilot version.** The programs in this lesson are checked automatically on Windows, Ubuntu and macOS. None of them asks for data: every value is written in the code. Only the check program in the solutions part reads data from the input.

## Before you start

This lesson assumes that you:

- define a struct, create its objects with the values in `{}`, and read fields with `.` (lesson 8.1);
- tell initialisation from assignment, and know that assigning one variable's value to another doesn't connect the two variables (lesson 2.2);
- shorten an update with `+=` (lesson 4.2);
- know the `const&` parameter, which lets a function read an existing object without copying it (lessons 6.4 and 7.3).

## The situation

In lesson 8.1 each object got its values once, when it was created, and never changed afterwards. Real data changes, though. A book in a catalogue gets a new edition with extra pages, and after it's read it moves to the finished books. More people sign up for an event.

This lesson answers two questions:

1. **How do you change the data of an existing object?**
2. **How do you keep its previous state**, so that later changes don't change the values you saved?

After this lesson you will:

- change the fields of an object that isn't `const`, and decide deliberately which object may change;
- create a copy of an existing record with `Book before{current};`;
- explain why a copy is independent of the original, its `std::string` fields included;
- tell a copy from a `const&` reference to an existing object;
- compare the state saved before a change with the current state;
- choose data that reveal a change made to the wrong object.

## 1. Prepare the project

In `cpp-workspace`, create a folder `lesson_8_2` and copy `main.cpp` and `CMakeLists.txt` from the original `lesson_05_first_program` into it. You type the programs from sections 2 and 4 into that folder's `main.cpp`. This lesson uses the type `Book` from lesson 8.1, unchanged.

## 2. Changing fields

The catalogue needs an update: the book `Guide` has a new edition, 120 pages long, and it has been read.

<!-- example: book_update -->
```cpp
#include <iostream>
#include <string>

struct Book {
    std::string title;
    int pages;
    bool finished;
};

int main() {
    Book book{"Guide", 100, false};

    std::cout << "Before pages: " << book.pages << "\n";

    if (book.finished) {
        std::cout << "Before finished: yes\n";
    } else {
        std::cout << "Before finished: no\n";
    }

    book.pages = 120;
    book.finished = true;

    std::cout << "After pages: " << book.pages << "\n";

    if (book.finished) {
        std::cout << "After finished: yes\n";
    } else {
        std::cout << "After finished: no\n";
    }
}
```

**Predict** all four lines, then run the program.

<details>
<summary>Standard output</summary>

<!-- output: book_update -->
```text
Before pages: 100
Before finished: no
After pages: 120
After finished: yes
```

</details>

- **`Book book{...}` has no `const`,** because this object's fields are going to change.
- **`book.pages = 120;` is an assignment,** like `count = 5;` in lesson 2.2. A field of a specific object stands on the left, so the new value goes into that field.
- **Changing one field doesn't change the others.** After the first assignment, `title` and `finished` keep their values. `book.finished = true;` then changes another field.
- **The definition of the type `Book` doesn't change.** Every book still has the same three fields. Only the value of one object's field changed.

You change a text field the same way, for example `book.title = "Guide 2";`. The `+=` from lesson 4.2 also works on a number field: `book.pages += 20;` would raise the number of pages from 100 to 120.

The program printed the `Before` lines before it changed the fields. After the assignments, the old values no longer exist in the object: `book.pages` is now 120.

## 3. A `const` object and changing fields

In lesson 8.1 the objects were `const`:

<!-- fragment -->
```cpp
const Book book{"Guide", 100, false};

book.pages = 120;
```

This fragment doesn't build. Clang reports `cannot assign to variable 'book' with const-qualified type 'const Book'`, much like the `int` constant in lesson 2.2. The problem isn't the field's type: `pages` is an ordinary `int` field. The program tries to change it through a `const` object, and such an object is for reading only.

**The fix is a deliberate decision:** remove the `const` only when the object really is supposed to change. **An object that shouldn't change later stays `const`.** Then the compiler makes sure that no line changes it by mistake.

## 4. A copy of a record

The program in section 2 lost the old values. How do you keep them, so that after the update you can compare the state before and after?

<!-- example: book_snapshot -->
```cpp
#include <iostream>
#include <string>

struct Book {
    std::string title;
    int pages;
    bool finished;
};

int main() {
    Book current{"Guide", 100, false};
    const Book before{current};

    current.pages = 120;
    current.finished = true;

    std::cout << "Before: " << before.title << ", " << before.pages << " pages\n";
    std::cout << "Current: " << current.title << ", " << current.pages << " pages\n";

    if (before.finished) {
        std::cout << "Before finished: yes\n";
    } else {
        std::cout << "Before finished: no\n";
    }

    if (current.finished) {
        std::cout << "Current finished: yes\n";
    } else {
        std::cout << "Current finished: no\n";
    }
}
```

**Predict:** how many pages does `before` have after `current.pages` changes?

<details>
<summary>Standard output</summary>

<!-- output: book_snapshot -->
```text
Before: Guide, 100 pages
Current: Guide, 120 pages
Before finished: no
Current finished: yes
```

</details>

1. **`current` is a modifiable object:** its fields change.
2. **`const Book before{current};` creates a new object** of the type `Book`, with the values of all the fields of `current` at this moment. It isn't a new type: `Book` is still the same type, and `before` is one more object.
3. **The whole record is copied,** not only `pages`: the title, the number of pages and `finished`.
4. **`before` is `const`,** because it has to keep the previous state. Nothing should change it.
5. **Later changes to `current` don't change `before`.** They're two separate objects. At first their fields have the same values, because `before` was created from `current`, but afterwards each stores its own.
6. **The `std::string` field belongs to the copy too.** If the program changed `current.title` after creating the copy, `before.title` would still hold `Guide`.

| Moment | `current` | `before` |
|---|---|---|
| after `const Book before{current};` | `Guide`, 100, `false` | `Guide`, 100, `false` |
| after `current.pages = 120;` | `Guide`, 120, `false` | `Guide`, 100, `false` |
| after `current.finished = true;` | `Guide`, 120, `true` | `Guide`, 100, `false` |

It's the same mechanism as in lesson 2.2, where `second` got a copy of the value of `first`: the variables weren't connected, and the later change to `first` didn't change `second`. A copy of a record does the same, only for all the fields at once.

**The order matters:** you create the copy **before** the change. A copy created after the update would already hold the new values.

`Book before{current};` creates a new object from the value of another object, so it's an initialisation, like `int count{3};`. C++ also lets you assign a whole record to an object that already exists, but we don't use that in this lesson.

## 5. A copy, a change and a reference

| Code | Meaning |
|---|---|
| `Book first{...};` and `Book second{...};` | two objects created separately, each with its own values (lesson 8.1) |
| `current.pages = 120;` | the same object gets a new field value |
| `Book copy{original};` | a new object is created with the values of the original's fields |
| `const Book snapshot{original};` | an independent copy is created, which we don't change later |
| `const Book& view{original};` | a reference to an existing object is created, for reading |

The last row is only a reminder of the `const&` idea from lesson 6.4, this time without a function: `view` is another name for the same object `original`. That's exactly why **a reference doesn't keep the old state**: when `original` changes, you read the new values through `view`. Keeping the state from before a change takes a copy. We don't use references in this lesson.

## 6. Mission: before and after new bookings

The program stores information about an event: its name, the maximum number of seats, and the number of people already signed up. New people ask to book seats. The program checks whether all the new bookings can be accepted, and compares the state before the change and after it.

**Data:** the event `C++ Workshop`, 12 seats, 7 people already signed up, 3 new bookings.

**Rules:**

- All the numbers are whole and non-negative. At the start, the number of people signed up doesn't exceed the number of seats.
- New bookings are accepted **all or nothing**. When there are enough free seats for all the new people, exactly enough included, the bookings are accepted. When even one seat is missing, the number of people signed up doesn't change.
- Zero new bookings is an update with no change: the request is accepted, and the number of people signed up stays the same.

**Requirements:**

- The program defines its own type with three fields: the event's name (`std::string`), the number of seats (`int`) and the number of people signed up (`int`). You choose the names of the type and the fields on your own.
- The number of new bookings is an ordinary `int` variable in `main`, not a field: it doesn't describe the lasting state of the event.
- `main` has one modifiable event object and its copy from before the change, marked `const`. The program creates no other objects repeating the same state.
- When the bookings are accepted, the program changes the field with the number of people signed up in the current object.
- The program prints exactly seven lines:
  - `Event`: the event's name;
  - `Capacity`: the number of seats;
  - `Before`: the number of people signed up, from the copy made before the change;
  - `Requested`: the number of new bookings;
  - `Accepted`: `yes` or `no`;
  - `After`: the number of people signed up, from the current object;
  - `Seats left`: the number of seats minus the current number of people signed up.
- The program reads nothing from the input and needs no functions of its own.

In `cpp-workspace`, create a folder `event_bookings`, copy `CMakeLists.txt` from the original `lesson_05_first_program` into it, create an empty `main.cpp` and write the program on your own.

For the data above, the standard output must be:

<!-- output: event_bookings -->
```text
Event: C++ Workshop
Capacity: 12
Before: 7
Requested: 3
Accepted: yes
After: 10
Seats left: 2
```

There are 5 free seats, so the 3 new people fit: 10 people are signed up now, and 2 seats stay free.

**This isn't the program from section 4 with different names.** You have to decide on your own:

1. what to call the type and its fields;
2. which object is going to change, and which is `const`;
3. where in the program to create the copy;
4. how to check whether there are enough free seats for all the new people;
5. which field to change, in which object, and when;
6. which object each line of the report comes from;
7. how to make sure the number of free seats is never negative.

**Before you write the program**, prepare a table of cases: fewer new people than free seats, exactly as many, one more, a full event, an event with nobody signed up, zero new bookings, and zero seats. For each, write down `Accepted`, `After` and `Seats left`.

**Then** run the program for the data from the requirements and for two other cases from your table, for example a rejected request and zero new bookings. Change only the values in the braces and the number of new bookings. Every case in the full list of check cases is checked automatically.

### Success criteria

- The program builds as C++20 and, for the data from the requirements, prints exactly the seven lines shown above.
- There's one type with three fields, one modifiable object, and its `const` copy, created before the change.
- `Before` comes from the copy, and `After` and `Seats left` from the current object.
- A rejected request doesn't change the number of people signed up, and that number never exceeds the number of seats.
- Zero new bookings give `Accepted: yes` and an unchanged number of people signed up.
- The table of cases was made before the program was run.
- You can name the object each line of the report comes from.

When the result matches, you can save the project in Git, as in lesson 1.5.

<details>
<summary>Hint 1</summary>

How do you keep the number of people signed up before the change, if the current record is going to hold the new number later?

</details>

<details>
<summary>Hint 2</summary>

Create an independent record from the current one before you start changing it. Which of these objects should stay `const`?

</details>

<details>
<summary>Hint 3</summary>

Accept the new bookings only when the number of free seats is enough. Change the field of the current object, and read the previous state from the saved copy.

</details>

<details>
<summary>The full list of check cases: open it after preparing your own table</summary>

| | Event | Seats | Before | New | Accepted | After | Free | What it checks |
|---|---|---:|---:|---:|---|---:|---:|---|
| A | `C++ Workshop` | 12 | 7 | 3 | yes | 10 | 2 | the data from the requirements: fewer people than free seats |
| B | `Talk` | 12 | 7 | 5 | yes | 12 | 0 | exactly all the free seats |
| C | `Talk` | 12 | 7 | 6 | no | 7 | 5 | one person too many: the record doesn't change |
| D | `Full` | 5 | 5 | 1 | no | 5 | 0 | a full event |
| E | `Empty` | 10 | 0 | 4 | yes | 4 | 6 | nobody signed up yet |
| F | `No change` | 10 | 4 | 0 | yes | 4 | 6 | zero new bookings |
| G | `No capacity` | 0 | 0 | 1 | no | 0 | 0 | zero seats |
| H | `One seat` | 1 | 0 | 1 | yes | 1 | 0 | one seat, filled |

**Automatic tests and your own runs.** Every case is checked automatically by a check program. It has the same struct and the same logic as the reference solution, but it reads the event's name and the three numbers from the input, one value per line. It's only a checking tool, not part of the mission: in the mission, the data is written in the code. The check program and its results are in [Example solutions](#example-solutions), because they contain the solution.

</details>

An example solution is in [Example solutions](#example-solutions).

## 7. Find the bug: the wrong copy changed

Do this task **after the mission**: the program below contains a type similar to yours. Someone accepts bookings for a meeting in it, and thinks that `copied` is another name for the same event. You may type the program or copy it into `main.cpp`.

<details>
<summary>The program to check: open it after writing your own program</summary>

<!-- example: event_copy_bug -->
```cpp
#include <iostream>
#include <string>

struct Event {
    std::string name;
    int capacity;
    int registered;
};

int main() {
    Event current{"Meeting", 10, 4};
    Event copied{current};
    const int requested{0};

    if (requested <= current.capacity - current.registered) {
        copied.registered += requested;
    }

    std::cout << "Event: " << current.name << "\n";
    std::cout << "Requested: " << requested << "\n";
    std::cout << "Registered: " << current.registered << "\n";
    std::cout << "Seats left: " << current.capacity - current.registered << "\n";
}
```

1. Point to both objects of the type `Event`.
2. Which of them was created as a copy?
3. **Predict** which field of which object really changes.
4. **Predict** the standard output for `requested` equal to 0, then run the program. Does the output look right?
5. Change the value of `requested` so that the bug becomes visible. First write down the correct output for your value, then run the program.
6. Explain the cause of the bug.
7. Fix the update: change the right field of the right object.
8. Run the fixed program for your value and for 0.

</details>

The results, an example value and the fixed program are in [Example solutions](#example-solutions).

## 8. When something goes differently

| What you see | What it means | What to do |
|---|---|---|
| `cannot assign to variable ... with const-qualified type` when a field changes | The field is changed through a `const` object (section 3). | Remove `const` only from the object that's supposed to change. Don't change the copy from before the change. |
| `Before` already shows the new value | The copy was created only after the change. | Create the copy before the change. |
| `After` shows the old value | The program changed the copy instead of the current object (section 7). | Change the field of the current object. |
| `Before` and `After` are always equal, even after accepted bookings | Both lines read the same object, or the change didn't reach the current object. | Check which object each line of the report comes from. |
| The number of people signed up exceeds the number of seats, or `Seats left` is negative | The program adds the new people without checking the free seats. | First compare the new bookings with the number of free seats, then change the field. |
| A rejected request changes the number of people signed up | The field change stands outside the condition. | Change the field only in the branch where the bookings are accepted. |
| Zero new bookings give `Accepted: no` | The condition requires more than zero new people, or uses `<` instead of `<=`. | Zero always fits: it's enough that there are no more new people than free seats. |

## 9. Explain

Answer in your own words, preferably in writing. Only then compare with the example answers.

1. Why could the objects in lesson 8.1 be `const`, while in this lesson the current object isn't?
2. What does `current.registered = 10;` mean? Does it change the struct's definition?
3. What does `Book copy{original};` mean? Is a new object created?
4. Does a later change to `original` change `copy`? Does that also apply to the `std::string` field?
5. Why is `const Book before{current};` a good way to keep an unchanged state, while the record whose fields you update shouldn't be `const`?
6. How does a copy differ from a `const&` reference to an existing object? Why doesn't a reference keep the old state?
7. Why do we create the copy before the change, not after it?
8. Why mustn't the mission update the copy instead of the current record?
9. Why must the free seats be checked before the bookings are accepted?

<details>
<summary>Example answers</summary>

1. Because in lesson 8.1 no object changed. Here the fields of the current object have to get new values, and they can't be changed through a `const` object.
2. It's an assignment of a new value to the field `registered` of the object `current`. The struct's definition doesn't change: the type still has the same fields, and only the value of one field of one object changes.
3. It creates a new object `copy` with the values of all the fields of the object `original` at this moment. Yes, it's a second, separate object of the same type.
4. No. The copy has its own field values, its own text in the `std::string` field included. A change to the original doesn't carry over to the copy.
5. Because the copy has to keep the state from before the change, so nothing should change it, and `const` lets the compiler make sure of that. The current record has to get new values, and `const` wouldn't allow that.
6. A copy is a separate object with its own values. A reference is another name for an existing object: it reads that object's current values, so after the original changes, it shows the new ones.
7. Because a copy keeps the values from the moment it's created. A copy created after the change would already hold the new values.
8. Because changing the copy doesn't change the current record: they're two independent objects. The `After` line and the number of free seats come from the current object, so they wouldn't show the accepted bookings, and the copy would stop showing the state from before the change.
9. Because bookings are accepted all or nothing. If the program changed the field first and checked the seats only afterwards, a rejected request would already have changed the record, or exceeded the number of seats.

</details>

## Summary

- An object without `const` can change its fields: `book.pages = 120;` assigns a new value to that object's field. `+=` works on a number field too.
- Changing a field changes neither the type's definition nor the other fields.
- An object that shouldn't change stays `const`, and the compiler makes sure nothing changes it.
- `Book before{current};` creates a new object with the values of all the fields of `current`, `std::string` fields included. The copy and the original are independent.
- The copy from before a change is created before the update and marked `const`.
- A `const&` reference doesn't keep the old state: it shows the original's current values.

## What's next

In this lesson all the work on records happened in `main`. In the next part of Module 8 a record will go to a function that reads it. It's in preparation.

---

## Example solutions

Look here **after your own attempt**. Your names may differ, as long as the standard output is as required.

<details>
<summary>Section 6: the mission, bookings for an event</summary>

<!-- example: event_bookings -->
```cpp
#include <iostream>
#include <string>

struct Event {
    std::string name;
    int capacity;
    int registered;
};

int main() {
    Event current{"C++ Workshop", 12, 7};
    const Event before{current};
    const int requested{3};

    const int free_seats{current.capacity - current.registered};
    const bool accepted{requested <= free_seats};

    if (accepted) {
        current.registered += requested;
    }

    std::cout << "Event: " << current.name << "\n";
    std::cout << "Capacity: " << current.capacity << "\n";
    std::cout << "Before: " << before.registered << "\n";
    std::cout << "Requested: " << requested << "\n";

    if (accepted) {
        std::cout << "Accepted: yes\n";
    } else {
        std::cout << "Accepted: no\n";
    }

    std::cout << "After: " << current.registered << "\n";
    std::cout << "Seats left: " << current.capacity - current.registered << "\n";
}
```

1. **`current` isn't `const`,** because after the bookings are accepted, its field `registered` gets a new value.
2. **We create the copy before the change,** because it keeps the values from the moment it's created.
3. **The copy can be `const`,** because nothing is supposed to change it. The compiler makes sure nobody changes it by mistake.
4. **`before.registered` keeps 7,** because `before` is a separate object: the change to `current.registered` doesn't affect it.
5. **`current.registered` holds 10,** because after the bookings are accepted, the program changes exactly that field of the current object.
6. **A refusal doesn't change the record:** the `+=` stands only in the branch where `accepted` gives `true`.
7. **Zero new bookings** meet the condition `0 <= free_seats`, so `Accepted: yes`, and adding 0 doesn't change the number of people signed up.
8. **No modifiable reference is needed:** all the changes happen in `main`, on the object `current`.
9. **No functions are needed:** the program checks one condition and changes one field. Passing records to functions is the topic of the next lesson.
10. **The old state is one object, not several variables.** The copy keeps all the fields at once, so you don't have to remember which values to copy into separate variables.
11. **The copy isn't a second name for the object `current`:** it has its own field values. That's why `before` and `current` differ after the update.
12. **Other correct conditions:** `current.registered + requested <= current.capacity` gives the same result. You can also change the field and print `Accepted: yes` in one `if` branch, and print `Accepted: no` in the `else` branch. What matters is that the field changes only after the seats are checked, and only in the current object.

`Seats left` is never negative: at the start the number of people signed up doesn't exceed the number of seats, and new people are added only when they fit.

**The check program** checks every case in the list of check cases. The struct, and the logic from the calculation of the free seats on, are the same as above, apart from the indentation. There's one difference: the event's name and the three numbers are read from the input into ordinary variables, and the object `current` is created from their values. `std::getline` reads the name, because it may contain a space, and `>>` reads the numbers, only after it.

<!-- example: event_bookings_check -->
```cpp
#include <iostream>
#include <string>

struct Event {
    std::string name;
    int capacity;
    int registered;
};

int main() {
    std::string name{};
    int capacity{0};
    int registered{0};
    int requested{0};

    std::getline(std::cin, name);
    std::cin >> capacity;
    std::cin >> registered;
    std::cin >> requested;

    if (std::cin.fail()) {
        std::cout << "Input could not be read\n";
    } else {
        Event current{name, capacity, registered};
        const Event before{current};

        const int free_seats{current.capacity - current.registered};
        const bool accepted{requested <= free_seats};

        if (accepted) {
            current.registered += requested;
        }

        std::cout << "Event: " << current.name << "\n";
        std::cout << "Capacity: " << current.capacity << "\n";
        std::cout << "Before: " << before.registered << "\n";
        std::cout << "Requested: " << requested << "\n";

        if (accepted) {
            std::cout << "Accepted: yes\n";
        } else {
            std::cout << "Accepted: no\n";
        }

        std::cout << "After: " << current.registered << "\n";
        std::cout << "Seats left: " << current.capacity - current.registered << "\n";
    }
}
```

Each case is four lines of input: the event's name, the number of seats, the number of people signed up, and the number of new bookings, in the order of the list of check cases, from A to H.

<!-- input: event_bookings_check -->
```text
C++ Workshop
12
7
3
```

<!-- output: event_bookings_check -->
```text
Event: C++ Workshop
Capacity: 12
Before: 7
Requested: 3
Accepted: yes
After: 10
Seats left: 2
```

<!-- input: event_bookings_check -->
```text
Talk
12
7
5
```

<!-- output: event_bookings_check -->
```text
Event: Talk
Capacity: 12
Before: 7
Requested: 5
Accepted: yes
After: 12
Seats left: 0
```

<!-- input: event_bookings_check -->
```text
Talk
12
7
6
```

<!-- output: event_bookings_check -->
```text
Event: Talk
Capacity: 12
Before: 7
Requested: 6
Accepted: no
After: 7
Seats left: 5
```

<!-- input: event_bookings_check -->
```text
Full
5
5
1
```

<!-- output: event_bookings_check -->
```text
Event: Full
Capacity: 5
Before: 5
Requested: 1
Accepted: no
After: 5
Seats left: 0
```

<!-- input: event_bookings_check -->
```text
Empty
10
0
4
```

<!-- output: event_bookings_check -->
```text
Event: Empty
Capacity: 10
Before: 0
Requested: 4
Accepted: yes
After: 4
Seats left: 6
```

<!-- input: event_bookings_check -->
```text
No change
10
4
0
```

<!-- output: event_bookings_check -->
```text
Event: No change
Capacity: 10
Before: 4
Requested: 0
Accepted: yes
After: 4
Seats left: 6
```

<!-- input: event_bookings_check -->
```text
No capacity
0
0
1
```

<!-- output: event_bookings_check -->
```text
Event: No capacity
Capacity: 0
Before: 0
Requested: 1
Accepted: no
After: 0
Seats left: 0
```

<!-- input: event_bookings_check -->
```text
One seat
1
0
1
```

<!-- output: event_bookings_check -->
```text
Event: One seat
Capacity: 1
Before: 0
Requested: 1
Accepted: yes
After: 1
Seats left: 0
```

</details>

<details>
<summary>Section 7: the results before the fix, and the fixed program</summary>

Before the fix, for `requested` equal to 0:

<!-- output: event_copy_bug -->
```text
Event: Meeting
Requested: 0
Registered: 4
Seats left: 6
```

- **Two objects:** `current` and `copied`. `copied` was created as a copy of `current`.
- **`copied.registered` changes,** not `current.registered`. They're two independent objects, so `current` "knows" nothing about the change.
- **For 0 the output looks right,** because adding zero changes nothing: a correct program would print the same.
- **Data that reveal the bug:** any positive number of new bookings that fits in the free seats. For example 3: the correct output is 7 people signed up and 3 free seats. The program with the bug prints:

<!-- example: event_copy_revealed -->
```cpp
#include <iostream>
#include <string>

struct Event {
    std::string name;
    int capacity;
    int registered;
};

int main() {
    Event current{"Meeting", 10, 4};
    Event copied{current};
    const int requested{3};

    if (requested <= current.capacity - current.registered) {
        copied.registered += requested;
    }

    std::cout << "Event: " << current.name << "\n";
    std::cout << "Requested: " << requested << "\n";
    std::cout << "Registered: " << current.registered << "\n";
    std::cout << "Seats left: " << current.capacity - current.registered << "\n";
}
```

<!-- output: event_copy_revealed -->
```text
Event: Meeting
Requested: 3
Registered: 4
Seats left: 6
```

| Object | `registered` before `+=` | `registered` after `+=` |
|---|---:|---:|
| `current` | 4 | 4 |
| `copied` | 4 | **7** |

- **The cause:** the program assumes that `copied` is another name for the same event. But `Event copied{current};` creates a new, independent object. The bookings went into the copy, and the report reads `current`, which didn't change.
- **The fix:** change the field of the current object: `current.registered += requested;`. The copy then serves no purpose, because this program doesn't print the state from before the change, so it goes.

<!-- example: event_copy_fixed -->
```cpp
#include <iostream>
#include <string>

struct Event {
    std::string name;
    int capacity;
    int registered;
};

int main() {
    Event current{"Meeting", 10, 4};
    const int requested{3};

    if (requested <= current.capacity - current.registered) {
        current.registered += requested;
    }

    std::cout << "Event: " << current.name << "\n";
    std::cout << "Requested: " << requested << "\n";
    std::cout << "Registered: " << current.registered << "\n";
    std::cout << "Seats left: " << current.capacity - current.registered << "\n";
}
```

<!-- output: event_copy_fixed -->
```text
Event: Meeting
Requested: 3
Registered: 7
Seats left: 3
```

For 0 the fixed program prints the same as before the fix, because adding zero changes nothing. That's why the case with zero alone isn't enough to check which object changes.

If the copy were needed to keep the state from before the change, like `before` in the mission, it should be `const`. Then the line `copied.registered += requested;` wouldn't build at all, and the compiler would point out the mistake straight away.

</details>

**Previous lesson:** [Lesson 8.1: Your first struct: several pieces of data describing one object](lesson_01_first_struct.en.md) · **Next lesson:** in preparation · [Course overview](../../README.en.md)

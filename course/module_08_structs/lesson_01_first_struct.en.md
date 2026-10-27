# Lesson 8.1: Your first struct: several pieces of data describing one object

[Polski](lesson_01_first_struct.md) · **English** · [Course overview](../../README.en.md)

> **Module 8, lesson 1** · about 60–75 minutes
> **You need:** your `cpp-workspace` folder and the original `lesson_05_first_program` project, as before. You won't need the debugger in this lesson.
> **Pilot version.** The programs in this lesson are checked automatically on Windows, Ubuntu and macOS. None of them asks for data: every value is written in the code. Only the check program in the solutions part reads data from the input.

## Before you start

This lesson assumes that you:

- declare variables of the types `int`, `bool` and `std::string`, initialise them with `{}` and mark them `const` when they don't change (lessons 2.1, 2.2, 2.7 and 3.2);
- compute results from several values and make decisions with `if` and `else` (Modules 2 and 3);
- know that a dot after an object's name refers to something that belongs to it, as in `std::cin.fail()` (lesson 4.5) or `text.size()` (lesson 7.1).

## The situation

A program stores information about a book:

<!-- fragment -->
```cpp
const std::string title{"C++ Basics"};
const int pages{180};
const bool finished{false};
```

These are three different pieces of information: the title, the number of pages, and whether the book has been read. They all describe one book, but nothing in the code says so: they're three separate variables.

- How do you know these values belong to the same book? Only from the names and from the fact that they stand next to each other.
- What happens when a second book appears? You'll need three more variables, for example `second_title`, `second_pages` and `second_finished`.
- How do you avoid mixing up one book's title with another book's page count? By watching every name.
- Can such a set of data be named as one type, like `int` or `std::string`?

This is valid C++, and in a small program three variables are enough. The trouble grows with the number of objects: every new book means three more names, held together only by your attention. In this lesson you'll define **your own type**, which gathers the data of one book in one place.

After this lesson you will:

- explain what problem `struct` solves;
- define a simple struct with fields of different types;
- tell the definition of a type from the creation of an object;
- create an object and give the values of its fields in `{}`, in the order of the fields;
- read fields with the `.` operator and use them in calculations and conditions;
- create several objects of one type, each with its own field values;
- recognise the mistake of mixed-up field values.

## 1. Prepare the project

In `cpp-workspace`, create a folder `lesson_8_1` and copy `main.cpp` and `CMakeLists.txt` from the original `lesson_05_first_program` into it. You type the programs from sections 3, 5, 7 and 8 into that folder's `main.cpp`.

## 2. Your own type: `struct`

<!-- fragment -->
```cpp
struct Book {
    std::string title;
    int pages;
    bool finished;
};
```

| Code | Meaning |
|---|---|
| `struct` | The keyword that starts the definition of your own type. |
| `Book` | The name of the new type. From now on `Book` is a type, like `int` or `std::string`. |
| `{ }` | The braces enclose the type's definition. |
| `std::string title;` | A **field**: a named part of every book. A field has a type and a name, like a variable declaration. |
| `int pages;`, `bool finished;` | Two more fields, of other types. |
| `;` after `}` | Ends the definition of the whole type. It's needed regardless of the semicolons after the fields. |

- **A type definition doesn't create any book yet.** It only describes what every book consists of: a title, a number of pages and whether it's been read. It's like a form with boxes that nobody has filled in yet. That's why the fields have no values here: each book will get its own.
- **Where the definition stands:** outside `main`, before the place where you use the type, like a function definition in lesson 5.1. A type definition isn't a variable and stores no values, so the rule "no variables declared outside functions" doesn't apply to it.
- **Names:** in this course we write the name of your own type with a capital letter (`Book`), and field names, like variable names, in `snake_case` (`title`, `unit_price`). That way the type `Book` is easy to tell from the object `book`.

C++ also has the keyword `class`, which defines your own types too. In this part of the course we use only `struct`.

## 3. The first object

<!-- example: first_book -->
```cpp
#include <iostream>
#include <string>

struct Book {
    std::string title;
    int pages;
    bool finished;
};

int main() {
    const Book book{"C++ Basics", 180, false};

    std::cout << "Title: " << book.title << "\n";
    std::cout << "Pages: " << book.pages << "\n";

    if (book.finished) {
        std::cout << "Finished: yes\n";
    } else {
        std::cout << "Finished: no\n";
    }
}
```

**Predict** all three lines of the output, then run the program.

<details>
<summary>Standard output</summary>

<!-- output: first_book -->
```text
Title: C++ Basics
Pages: 180
Finished: no
```

</details>

The line `const Book book{"C++ Basics", 180, false};` **creates an object**, one specific book:

- `Book` is the type and `book` is the object's name, just as in `const int pages{180};` the type is `int` and the name is `pages`;
- the values in `{}` go into the fields one after another, **in the same order as the fields stand in the type's definition**:

| Field | Type | Value |
|---|---|---|
| `title` | `std::string` | `"C++ Basics"` |
| `pages` | `int` | `180` |
| `finished` | `bool` | `false` |

- `const`, because the program doesn't change this book, as with any other variable we don't change (lesson 2.2).
- In this lesson we always give the values of **all** the fields, one per field. The compiler checks their types: text won't go into an `int` field. But it can't tell two values of the same type apart when you swap their order (section 8).

## 4. The dot operator

Read `book.title` as "the field `title` of the object `book`". You know the dot from `std::cin.fail()` and `text.size()`: there, a function that belongs to the object stood after the dot; here, a field stands there, a value stored in the object.

| Expression | Type | Value |
|---|---|---|
| `book.title` | `std::string` | `C++ Basics` |
| `book.pages` | `int` | `180` |
| `book.finished` | `bool` | `false` |

You use an object's field like an ordinary variable of its type: you can print `book.pages`, add it to another number or compare it, and put `book.finished` in an `if` condition. That's why the program in section 3 prints `yes` or `no` through an `if`, instead of printing the `bool` value as `1` or `0`.

## 5. Two objects of the same type

<!-- example: two_books -->
```cpp
#include <iostream>
#include <string>

struct Book {
    std::string title;
    int pages;
    bool finished;
};

int main() {
    const Book first{"C++ Basics", 180, false};
    const Book second{"Algorithms", 240, true};

    std::cout << first.title << ": " << first.pages << " pages\n";
    std::cout << second.title << ": " << second.pages << " pages\n";

    int pages_to_read{0};

    if (!first.finished) {
        pages_to_read += first.pages;
    }

    if (!second.finished) {
        pages_to_read += second.pages;
    }

    std::cout << "Pages to read: " << pages_to_read << "\n";
}
```

**Predict** the output. How many pages are left to read?

<details>
<summary>Standard output</summary>

<!-- output: two_books -->
```text
C++ Basics: 180 pages
Algorithms: 240 pages
Pages to read: 180
```

</details>

- **Both objects have the type `Book`,** so they have the same fields: `title`, `pages` and `finished`.
- **The field values differ:** each object stores its own. `second` isn't a copy of `first`, but a second book, created separately.
- **The name before the dot chooses the object.** `first.pages` is the first book's number of pages, and `second.pages` the second book's.
- Only the pages of a book whose own `finished` field gives `false` go into the sum (`!` from lesson 3.4, `+=` from lesson 4.2). Each condition checks a field of the same object the program takes the pages from.

**Change:** in the braces of the object `second`, replace `true` with `false`, and predict the new output before you run the program. You change only the second book's data: the first stays the same.

## 6. Type, object and field

| Code | What it is | Example |
|---|---|---|
| `Book` | your own type | `struct Book { ... };` |
| `first`, `second` | objects of the type `Book`: specific books | `const Book first{"C++ Basics", 180, false};` |
| `pages` | the name of a field declared in the type | `int pages;` |
| `first.pages` | a field of a specific object | `180` |

`pages` on its own, with no object, means nothing: every book has its own `pages`, so you always have to say which book you mean. A specific object of a type is also called an **instance** of that type. In this course we simply say "object".

## 7. Find the bug: the missing semicolon

This program differs from the program in section 3 by one character. **Predict** whether it builds, then try to build it and read the compiler's first message. Find the missing character and fix the program.

<!-- broken: first_book_no_semicolon at=8:2 errors=1 error=^expected ';' after struct -->
```cpp
#include <iostream>
#include <string>

struct Book {
    std::string title;
    int pages;
    bool finished;
}

int main() {
    const Book book{"C++ Basics", 180, false};

    std::cout << "Title: " << book.title << "\n";
    std::cout << "Pages: " << book.pages << "\n";

    if (book.finished) {
        std::cout << "Finished: yes\n";
    } else {
        std::cout << "Finished: no\n";
    }
}
```

<details>
<summary>What the compiler reports, and why</summary>

The program doesn't build. The compiler reports `expected ';' after struct` on line 8: the semicolon after the closing brace of the definition of `Book` is missing.

- The semicolons **after the fields** end the declarations of the fields, like variable declarations.
- The semicolon **after `}`** ends the definition of the whole type. Without it, the compiler doesn't know that the definition has ended.

**The fix:** add `;` after `}`. The fixed program is the program from section 3.

</details>

## 8. Find the bug: swapped values

Do this task **before the mission**. The program describes a room: its name, the number of seats and the number of people signed up. The numbers were worked out earlier in two variables, and the room object was created from their values. You may type the program or copy it into `main.cpp`.

<!-- example: room_order_bug -->
```cpp
#include <iostream>
#include <string>

struct Room {
    std::string name;
    int seats;
    int people;
};

int main() {
    const int available_seats{30};
    const int registered_people{30};

    const Room room{"Lab", registered_people, available_seats};

    std::cout << "Room: " << room.name << "\n";
    std::cout << "Seats: " << room.seats << "\n";
    std::cout << "People: " << room.people << "\n";

    if (room.people >= room.seats) {
        std::cout << "Full: yes\n";
    } else {
        std::cout << "Full: no\n";
    }
}
```

1. Write down the fields of the struct `Room` in the order of the definition.
2. Match each value in `{"Lab", registered_people, available_seats}` with the field that receives it.
3. **Predict** the standard output, then run the program. Does the output look right?
4. Why doesn't the compiler report any error?
5. Change the values of `available_seats` and `registered_people` so that the mistake becomes visible in the output. First write down what the correct output would be for your data, then run the program.
6. Fix the order of the values where the object is created.
7. Run the fixed program for your data and for 30 and 30.

The results, example data and the fixed program are in [Example solutions](#example-solutions).

## 9. Mission: a product card in a storeroom

The program prepares the card of one product in a storeroom. A product has:

- a name;
- the number of pieces in the storeroom, its stock;
- the minimum required number of pieces;
- the price of one piece.

**The product's data:** the name `Tea`, a stock of 3 pieces, a minimum of 8 pieces, and a price of 6 per piece. All the numbers are small, non-negative and whole.

**Requirements:**

- The program defines **its own struct**, one object of which stores all four pieces of the product's data. You choose the type's name, the fields' names and their types on your own.
- It creates one object of that struct, with the values in `{}`, and computes every number of the report from that object's fields. It doesn't copy the product's data into separate variables.
- It prints exactly six lines: `Product: NAME`, `Stock: N`, `Minimum: N`, `Unit price: N`, `Stock value: N` and `To add: N`.
- **The stock value** is the stock times the price of one piece.
- **The number of pieces to add:** when the stock is below the minimum, the difference between the minimum and the stock; otherwise 0. The program never prints a negative number.
- The program reads nothing from the input and needs no functions of its own.

In `cpp-workspace`, create a folder `product_card`, copy `CMakeLists.txt` from the original `lesson_05_first_program` into it, create an empty `main.cpp` and write the program on your own.

For the data above, the standard output must be:

<!-- output: product_card -->
```text
Product: Tea
Stock: 3
Minimum: 8
Unit price: 6
Stock value: 18
To add: 5
```

A stock of 3 times a price of 6 gives a stock value of 18. Reaching the minimum of 8 takes 5 more pieces.

**This isn't the book program with different names.** You have to decide on your own:

1. what to call the type and its four fields;
2. what type each field has;
3. in what order to write the fields, and how to give the object's values in the same order;
4. which fields you need for the stock value, and which for checking the minimum;
5. how to make sure the number of pieces to add is never negative;
6. how to build the whole report from one object.

**Before you write the program**, prepare a table of cases: a stock below the minimum, equal to it and above it, a zero stock, and a zero price. For each, write down the expected stock value and the number of pieces to add.

**Then** run the program for the data from the requirements and for two other cases from your table, for example a stock equal to the minimum and a zero stock. Change only the values in the object's braces. Every case in the full list of check cases is checked automatically.

### Success criteria

- The program builds as C++20 and, for the data from the requirements, prints exactly the six lines shown above.
- There's one struct with four fields and one object of that struct, created with the values in `{}`.
- Every line of the report uses that object's fields, and `main` has no separate variables repeating the product's data.
- The number of pieces to add is never negative, and when the stock equals the minimum or is above it, it's 0.
- The table of cases was made before the program was run.
- You can explain in what order your values in `{}` go into the fields.

When the result matches, you can save the project in Git, as in lesson 1.5.

<details>
<summary>Hint 1</summary>

Which four pieces of information describe one product? Can you enclose them in one type of your own?

</details>

<details>
<summary>Hint 2</summary>

Define the struct's fields, create an object, and use its fields through the dot operator.

</details>

<details>
<summary>Hint 3</summary>

The stock value depends on the stock and the price. The number of pieces to add depends on the stock and the minimum, but it can't be negative.

</details>

<details>
<summary>The full list of check cases: open it after preparing your own table</summary>

| | Product | Stock | Minimum | Price | Stock value | To add | What it checks |
|---|---|---:|---:|---:|---:|---:|---|
| A | `Tea` | 3 | 8 | 6 | 18 | 5 | the data from the requirements: a stock below the minimum |
| B | `Rice` | 8 | 8 | 4 | 32 | 0 | a stock equal to the minimum |
| C | `Pens` | 10 | 7 | 2 | 20 | 0 | a stock above the minimum: no negative number |
| D | `Box` | 0 | 5 | 3 | 0 | 5 | a zero stock |
| E | `Glue` | 1 | 1 | 0 | 0 | 0 | a zero price and a stock equal to the minimum |
| F | `Paper` | 2 | 5 | 1 | 2 | 3 | a price of 1: the value equals the stock |

**Automatic tests and your own runs.** Every case is checked automatically by a check program. It has the same struct and the same report as the reference solution, but it reads the product's data from the input, one value per line. It's only a checking tool, not part of the mission: in the mission, the data is written in the code. The check program and its results are in [Example solutions](#example-solutions), because they contain the solution.

</details>

An example solution is in [Example solutions](#example-solutions).

## 10. When something goes differently

| What you see | What it means | What to do |
|---|---|---|
| `expected ';' after struct` | The semicolon after the closing brace of the definition is missing (section 7). | Add `;` after `}`. |
| `excess elements in struct initializer` | There are more values in `{}` than fields. | Give one value for each field. |
| A message with `no viable conversion` or `cannot initialize a member subobject` where the object is created | A value has a different type than the field it goes into, for example a number stands where the text should be. | Put the values in the order of the fields in the definition. |
| `use of undeclared identifier` with a field's name, for example `title` | The field is used without an object. | Name the object: `book.title`. |
| `'Book' does not refer to a value` | The name of the type stands before the dot, not an object's. | Write the object's name before the dot, for example `book`. |
| The program builds, but the values of two number fields are swapped | The values in `{}` stand in a different order than the fields (section 8). | Compare the order of the values with the order of the fields in the definition. |
| A number field has the value 0, and a `bool` field the value `false`, although you didn't give them | There are fewer values in `{}` than fields. Fields without a value get 0, `false` or an empty text. | Give a value for every field. |
| The program prints `1` or `0` instead of `yes` or `no` | The `bool` field is printed directly. | Choose the text with an `if`, as in section 3. |

## 11. Explain

Answer in your own words, preferably in writing. Only then compare with the example answers.

1. What problem does `struct` solve?
2. Does the definition `struct Book` already create a book?
3. How do `Book`, `book` and `book.pages` differ?
4. Why is a semicolon needed after the struct's closing brace, when there are semicolons after the fields already?
5. How do the values in `{}` get into the object's fields?
6. What does the `.` operator do, and what type is `book.finished`?
7. Can two objects of the type `Book` have different field values? How does the program know which book `first.pages` refers to?
8. Why didn't the compiler detect the swapped values in the room program from section 8?
9. Why can the product object in the mission be `const`?
10. Does the struct in this lesson need constructors or methods?

<details>
<summary>Example answers</summary>

1. It joins several pieces of information that describe one object, for example the title, the number of pages and the reading status of one book. Instead of separate variables, held together only by similar names, the program has one object with named fields.
2. No. The definition only describes which fields every book consists of. A book appears only when you create an object, for example `const Book book{"C++ Basics", 180, false};`.
3. `Book` is the type, `book` is a specific object of that type, and `book.pages` is the field `pages` of that object, the number of pages of that book.
4. The semicolons after the fields end the fields' declarations, and the semicolon after `}` ends the definition of the whole type. They're two different places, so both are needed.
5. In order: the first value goes into the first field of the definition, the second into the second, and so on. That's why the order of the values must match the order of the fields.
6. It chooses a field of a specific object. `book.finished` has the field's type from the definition, `bool`.
7. Yes. Each object stores its own field values. The name before the dot points to the object: `first.pages` is the first book's pages, and `second.pages` the second book's.
8. Because both fields, `seats` and `people`, have the type `int`, and both variables are `int` too. The compiler checks types, not what the values mean, so the number of people can go into the seats field without an error. It's a logic error, not a compile error.
9. Because the program only reads the product's data and computes from it. No field of the object changes.
10. No. We create the object by giving the values of all the fields in `{}`, and read the fields through the dot. Constructors and methods aren't needed here.

</details>

## Summary

- **`struct`** defines your own type: a named group of fields, each with a type and a name. A semicolon stands after the definition's closing brace.
- A type definition doesn't create an object. You create an object like a variable: the type, a name and the values in `{}`, for example `const Book book{"C++ Basics", 180, false};`.
- The values in `{}` go into the fields in the order of their declarations. The compiler checks types, but it can't tell swapped values of the same type apart.
- The `.` operator chooses a field of a specific object: `book.pages` is the number of pages of the book `book`. You use a field like an ordinary variable of its type, in calculations and conditions.
- Several objects of one type have the same fields, but each stores its own values.
- A struct joins data that belongs to one object; it doesn't merely shorten the code.

## What's next

In this lesson each object got its values once, when it was created, and never changed afterwards. In the next part of Module 8 you'll see how an object can change, and what a copy of it is. It's in preparation.

---

## Example solutions

Look here **after your own attempt**. Your names may differ, as long as the standard output is as required.

<details>
<summary>Section 9: the mission, a product card</summary>

<!-- example: product_card -->
```cpp
#include <iostream>
#include <string>

struct Product {
    std::string name;
    int stock;
    int minimum;
    int unit_price;
};

int main() {
    const Product product{"Tea", 3, 8, 6};

    int to_add{0};

    if (product.stock < product.minimum) {
        to_add = product.minimum - product.stock;
    }

    std::cout << "Product: " << product.name << "\n";
    std::cout << "Stock: " << product.stock << "\n";
    std::cout << "Minimum: " << product.minimum << "\n";
    std::cout << "Unit price: " << product.unit_price << "\n";
    std::cout << "Stock value: " << product.stock * product.unit_price << "\n";
    std::cout << "To add: " << to_add << "\n";
}
```

1. **A new type,** because the four pieces of data describe one product. The struct `Product` writes that relation into the code: every product has a name, a stock, a minimum and a price.
2. **Fields and an object:** `name`, `stock`, `minimum` and `unit_price` are the fields declared in the type `Product`. `product` is an object, a specific product with values for those fields.
3. **The order:** `{"Tea", 3, 8, 6}` gives the values in the order of the fields in the definition: the name, the stock, the minimum, the price.
4. **A swap with no error:** the stock, the minimum and the price have the type `int`. If you swapped 3 and 8 in `{}`, the program would build with no error, but the stock would be 8 and the minimum 3. The compiler checks types, not what the numbers mean.
5. **The dot** chooses a field of this one object: `product.stock` is the stock, and `product.minimum` the minimum.
6. **One object:** every line of the report takes its data from `product`, so the stock of one product can't be paired with the price of another. `to_add` is the result of a calculation, not a copy of the product's data.
7. **`const`:** the program only reads the product's fields, so the object can be constant, like any variable we don't change.
8. **A second product** is a second object of the same type, with its own values, for example `const Product rice{"Rice", 8, 8, 4};`. The fields `rice.stock` and `product.stock` are independent of each other.

**The number of pieces to add** starts at 0 and changes only when the stock is below the minimum. That's why the result is 0 for a stock equal to the minimum or above it, and the difference is never negative. The same condition can also be written as an `if` and `else`, with a separate `To add` line in each branch. The fields may have other names and another order, as long as the values in `{}` stand in the same order as the fields.

**The check program** checks every case in the list of check cases. The struct and the report are the same as above, apart from the indentation. There's one difference: the product's data is read from the input into four ordinary variables, and the object is created from their values.

<!-- example: product_card_check -->
```cpp
#include <iostream>
#include <string>

struct Product {
    std::string name;
    int stock;
    int minimum;
    int unit_price;
};

int main() {
    std::string name{};
    int stock{0};
    int minimum{0};
    int unit_price{0};

    std::cin >> name;
    std::cin >> stock;
    std::cin >> minimum;
    std::cin >> unit_price;

    if (std::cin.fail()) {
        std::cout << "Input could not be read\n";
    } else {
        const Product product{name, stock, minimum, unit_price};

        int to_add{0};

        if (product.stock < product.minimum) {
            to_add = product.minimum - product.stock;
        }

        std::cout << "Product: " << product.name << "\n";
        std::cout << "Stock: " << product.stock << "\n";
        std::cout << "Minimum: " << product.minimum << "\n";
        std::cout << "Unit price: " << product.unit_price << "\n";
        std::cout << "Stock value: " << product.stock * product.unit_price << "\n";
        std::cout << "To add: " << to_add << "\n";
    }
}
```

Each case is four lines of input: the name, the stock, the minimum and the price, in the order of the list of check cases, from A to F.

<!-- input: product_card_check -->
```text
Tea
3
8
6
```

<!-- output: product_card_check -->
```text
Product: Tea
Stock: 3
Minimum: 8
Unit price: 6
Stock value: 18
To add: 5
```

<!-- input: product_card_check -->
```text
Rice
8
8
4
```

<!-- output: product_card_check -->
```text
Product: Rice
Stock: 8
Minimum: 8
Unit price: 4
Stock value: 32
To add: 0
```

<!-- input: product_card_check -->
```text
Pens
10
7
2
```

<!-- output: product_card_check -->
```text
Product: Pens
Stock: 10
Minimum: 7
Unit price: 2
Stock value: 20
To add: 0
```

<!-- input: product_card_check -->
```text
Box
0
5
3
```

<!-- output: product_card_check -->
```text
Product: Box
Stock: 0
Minimum: 5
Unit price: 3
Stock value: 0
To add: 5
```

<!-- input: product_card_check -->
```text
Glue
1
1
0
```

<!-- output: product_card_check -->
```text
Product: Glue
Stock: 1
Minimum: 1
Unit price: 0
Stock value: 0
To add: 0
```

<!-- input: product_card_check -->
```text
Paper
2
5
1
```

<!-- output: product_card_check -->
```text
Product: Paper
Stock: 2
Minimum: 5
Unit price: 1
Stock value: 2
To add: 3
```

</details>

<details>
<summary>Section 8: the results before the fix, and the fixed program</summary>

Before the fix, for 30 seats and 30 people:

<!-- output: room_order_bug -->
```text
Room: Lab
Seats: 30
People: 30
Full: yes
```

| Field in the definition | Value in `{}` | What the field gets |
|---|---|---|
| `name` | `"Lab"` | the room's name |
| `seats` | `registered_people` | the number of **people**, not of seats |
| `people` | `available_seats` | the number of **seats**, not of people |

- **The output looks right,** because both numbers are 30: swapping two equal values changes nothing.
- **The compiler reports no error,** because both fields and both variables have the type `int`. The types match, and the compiler doesn't know what the values mean.
- **Data that reveal the bug:** any two different numbers. For example 30 seats and 24 people, that is `available_seats{30}` and `registered_people{24}`. The correct output is 30 seats, 24 people and `Full: no`. The program with the bug prints:

<!-- example: room_order_revealed -->
```cpp
#include <iostream>
#include <string>

struct Room {
    std::string name;
    int seats;
    int people;
};

int main() {
    const int available_seats{30};
    const int registered_people{24};

    const Room room{"Lab", registered_people, available_seats};

    std::cout << "Room: " << room.name << "\n";
    std::cout << "Seats: " << room.seats << "\n";
    std::cout << "People: " << room.people << "\n";

    if (room.people >= room.seats) {
        std::cout << "Full: yes\n";
    } else {
        std::cout << "Full: no\n";
    }
}
```

<!-- output: room_order_revealed -->
```text
Room: Lab
Seats: 24
People: 30
Full: yes
```

The numbers of seats and people are swapped, and on top of that the decision changes: a room with six free seats looks full.

**The fix:** the values in `{}` in the order of the fields: first the number of seats, then the number of people.

<!-- example: room_order_fixed -->
```cpp
#include <iostream>
#include <string>

struct Room {
    std::string name;
    int seats;
    int people;
};

int main() {
    const int available_seats{30};
    const int registered_people{24};

    const Room room{"Lab", available_seats, registered_people};

    std::cout << "Room: " << room.name << "\n";
    std::cout << "Seats: " << room.seats << "\n";
    std::cout << "People: " << room.people << "\n";

    if (room.people >= room.seats) {
        std::cout << "Full: yes\n";
    } else {
        std::cout << "Full: no\n";
    }
}
```

<!-- output: room_order_fixed -->
```text
Room: Lab
Seats: 30
People: 24
Full: no
```

For 30 and 30 the fixed program prints the same as before the fix: with equal values both orders give the same output. That's why data with two equal numbers aren't enough to check the order of the fields.

</details>

**Previous lesson:** [Lesson 7.5: Parcel code check (the Module 7 test)](../module_07_text/lesson_05_parcel_code_check.en.md) · **Next lesson:** in preparation · [Course overview](../../README.en.md)

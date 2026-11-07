# Lesson 13.3: Testing a reading function without a file

[Polski](lesson_03_testing_input_without_a_file.md) · **English** · [Course overview](../../README.en.md)

> **Module 13, lesson 3** · about 85–105 minutes, can be split into two sessions
> **You need:** your `cpp-workspace` folder and the original `lesson_05_first_program` project, as before. The solution of the lesson 12.3 mission, with the function `read_chores`, will be useful too.
> **Pilot version.** The programs in this lesson are checked automatically on Windows, Ubuntu and macOS, together with their exit codes. They need no data files, no **Working directory** field and no typed input.

## Before you start

This lesson assumes that you:

- write the test program of lessons 13.1 and 13.2: the expected result from the contract, `PASS` or `FAIL`, a failure counter, exit code 0 or 1, the functions `check_bool` and `bool_text`;
- know the function `read_shipment_values` from lesson 10.4: it reads a number of boxes from a `std::istream&` stream and fills the result record only on success, and in lesson 12.2 the same function read from a file;
- know the function `read_chores` from the mission of lesson 12.3 and the table in point 2 of that lesson, in which `\n` stood for the line end in a file;
- remember from lesson 4.6 that after a failed read `fail()` gives `true`, and that `clear()` creates no new data;
- keep the size of a vector in the type `std::size_t` and don't mix it with `int` (lesson 6.3);
- write a quotation mark inside a text as `\"` (lesson 1.6).

## The situation

The function `read_shipment_values` has so far been checked in two ways: with data typed on the keyboard (lesson 10.4) and with the file `shipments.txt` (lesson 12.2). Both are good when the program is in use. For testing, though, they have a cost: the data has to be typed every time, or a file has to be prepared and kept in the working directory, it's easy to check, by accident, other file contents than the ones you meant, and a dozen variants of the data means a dozen files or a dozen rounds of typing.

The test program of lesson 13.1 compares the results by itself. All it lacks is a source of data that needs neither the keyboard nor a file. **That source will be a text written in the test program itself.**

After this lesson you will:

- create an input stream from a text with `std::istringstream` and pass it to a function with a `std::istream&` parameter;
- test a reading function without a file and without typing data;
- check several effects of one call in one case: the `bool` result, the result record and the stream state;
- check the contents and order of a vector, the error kind and the physical line number;
- give every independent case a new stream and its own result variables.

## 1. Three data sources, one function

| Source | Object | Where the characters come from |
|---|---|---|
| the keyboard, that is, standard input | `std::cin` | from the program's standard input |
| a text file | `std::ifstream` | from an open file |
| a text in memory | `std::istringstream` | from the text given when the stream is created |

In all three cases a function can take the same parameter, `std::istream&`. A function with such a parameter doesn't know where the characters come from (lesson 12.2), so **the same, unchanged function can be tested with a text written in the code.**

`std::istringstream` doesn't replace `std::ifstream` in a program that has to read a file. The chore log program of lesson 12.3 still reads `chores.txt`. A text in memory is a third data source, especially handy in tests: the data is in the test code, next to the expected result.

## 2. A stream over a text: `std::istringstream`

<!-- example: memory_stream -->
```cpp
#include <iostream>
#include <sstream>

int main() {
    std::istringstream input{"4\n"};
    int boxes{0};
    input >> boxes;

    if (input.fail()) {
        std::cout << "Input error\n";
        return 0;
    }

    std::cout << "Boxes: " << boxes << "\n";
}
```

The program prints:

<!-- output: memory_stream -->
```text
Boxes: 4
```

| Code | What it does |
|---|---|
| `#include <sstream>` | makes `std::istringstream` available |
| `std::istringstream input{"4\n"};` | creates an input stream whose data are the character `4` and a line end |
| `input >> boxes;` | reads a number, just as from `std::cin` |
| `input.fail()` | tells whether the read failed, just as in lesson 4.5 |

- **The name:** *i* for *input*, *string* for text, *stream*, so an input stream over a text.
- **No file is created.** There is no data file, no **Working directory** to set, and the program doesn't wait for the keyboard.
- **The text in quotes is exactly the data.** `\n` is the same line end that stood for the end of a file line in the table of lesson 12.3. `""` is an empty file, `"\n"` is one empty line, and `"Clean tables\ndone"` is two lines without a line end after the last one. Some of this data is hard to type on the keyboard, and in an editor it's easy to change by accident, for example by adding a line end.
- **Characters that have been read are gone from the stream,** just as with `std::cin`. After `input >> boxes`, only the line end is left in it. The stream doesn't go back to the start of the text by itself (point 9).

In `cpp-workspace`, create a folder `lesson_13_3`, copy `main.cpp` and `CMakeLists.txt` from the original `lesson_05_first_program` into it, and open it in CLion. You can run this short program right away in `main.cpp`. This run is optional. You type the next programs of this lesson into the same `main.cpp`, and you leave `CMakeLists.txt` unchanged.

**Why can such a stream be passed to a function with `std::istream&`?** The standard library defines `std::istringstream`, just like `std::ifstream` in lesson 12.2, as a special kind of `std::istream`. It has everything a function needs from an input stream: `>>`, `fail()` and working with `std::getline`. The parameter `input` then becomes another name for the stream over the text:

<!-- fragment -->
```cpp
std::istringstream input{"4\n"};
Shipment shipment{"Old Destination", 1};
const bool accepted{read_shipment_values(input, "North Hub", shipment)};
```

**One way of using it is enough in this lesson:** create a stream with a ready text and read from it. The library also has streams that you write to, and ways to go back to the start of a stream, but the tests in this lesson don't need them. A simpler rule applies: **every independent test case gets a new `std::istringstream`.**

## 3. The contract of `read_shipment_values`

The function is the same as in lessons 10.4 and 12.2, character for character:

<!-- fragment -->
```cpp
bool read_shipment_values(std::istream& input, const std::string& destination, Shipment& result) {
    int boxes{0};
    input >> boxes;

    if (input.fail()) {
        return false;
    }

    if (boxes < 0) {
        return false;
    }

    result = Shipment{destination, boxes};
    return true;
}
```

**The contract:**

- the function gets a stream, a non-empty destination name, read earlier by the caller, and a result record;
- it reads one number of boxes with `>>`;
- `true`: the number has been read and isn't negative, and `result` holds the given name and that number;
- `false`: the read failed or the number is negative, and `result` is **unchanged**;
- after `false`, the stream state tells which reason it was: after a failed read `fail()` gives `true`, and after a number that was read but is negative, `false`;
- the contract sets no upper limit on the number of boxes.

We don't change the function to make it easier to test. The test has to check exactly the function the program uses.

**The cases of the demonstration.** Each one starts from the record `Shipment{"Old Destination", 1}`, that is, from values the function wouldn't write for any of this data. After the call you can see at once whether the record has changed.

| Case | Stream text | Name | Result | Record after the call | `fail()` after the call |
|---|---|---|---|---|---|
| A | `"4\n"` | `North Hub` | `true` | `North Hub`, 4 | not checked |
| B | `"0\n"` | `North Hub` | `true` | `North Hub`, 0 | not checked |
| C | `"-2\n"` | `North Hub` | `false` | unchanged: `Old Destination`, 1 | `false` |
| D | `"seven\n"` | `North Hub` | `false` | unchanged: `Old Destination`, 1 | `true` |
| E | `""` | `North Hub` | `false` | unchanged: `Old Destination`, 1 | `true` |
| F | `"4"` | `North Hub` | `true` | `North Hub`, 4 | not checked |
| G | `"1250\n"` | `West End Depot` | `true` | `West End Depot`, 1250 | not checked |

- **C, D and E differ in the stream state.** In C the number is read but negative, so `fail()` gives `false`. In D `seven` isn't a number, and in E there is no number at all, so `fail()` gives `true`. In all three the record stays unchanged.
- **F, a number without a line end:** `>>` reached the end of the text, but the read succeeded (lesson 10.4, point 5), so the function returns `true`. A missing line end doesn't mean failure.
- **G:** the contract has no upper limit, and a name with spaces goes into the record whole.

## 4. One call, several checks

In lessons 13.1 and 13.2 the function had one result, so every case meant one comparison. `read_shipment_values` has several effects you can observe: it returns a `bool`, it changes or leaves the record, and it can change the stream state. **One call may need several properties checked.**

**An accepted case** (A, B, F, G) confirms three things:

1. the function returned `true`;
2. the name in the record is correct;
3. the number of boxes in the record is correct.

**A refused case** (C, D, E) confirms four:

1. the function returned `false`;
2. the name in the record is unchanged;
3. the number of boxes in the record is unchanged;
4. `fail()` matches the reason for the refusal.

`true` alone isn't enough: the function could return `true` and store the wrong number. `false` alone isn't enough either: it could refuse and still change the record (point 8).

In the accepted cases we don't check `fail()`: the function returns `true` only after a successful read. Nor `eof()`: in F the stream reached the end of the text, but the contract says nothing about it, and a test checks the contract.

**How we count.** We tell two things apart:

- a **case** is one set of data and one call of the function;
- a **check** is one comparison of one property, with one verdict, `PASS` or `FAIL`.

So one case gives three or four checks. The counter of lesson 13.1 now counts checks, so it's called `checks`, and the summary has the form `Checks: N, failed: F`. The exit code depends, as before, on the failure counter.

## 5. Checking functions for a number and a text

`check_bool` and `bool_text` are as in lesson 13.2, only the counter is called `checks`. Numbers and texts need two more functions of the same shape:

<!-- fragment -->
```cpp
void check_int(const std::string& name, int expected, int actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << expected << ", actual " << actual << "\n";
        ++failed;
    }
}

void check_text(const std::string& name, const std::string& expected, const std::string& actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected \"" << expected << "\", actual \"" << actual << "\"\n";
        ++failed;
    }
}
```

- **`check_int`** is `check_equal` from lesson 13.1, under a name that says which type it compares.
- **`check_text`** compares texts and prints them in quotes, written as `\"`. This way you can see an empty text (`""`) and a space at the end.
- **Each function has its own name,** because each takes a different type of value.
- **The name of a check** is the letter of the case and the property checked: `A accepted`, `C destination`, `D fail()`. From a `FAIL` line you can see at once which case and which property doesn't match.

## 6. Tests of a correct read

The first test program checks the accepted cases: A, B, F and G.

<!-- example: shipment_tests -->
```cpp
#include <iostream>
#include <sstream>
#include <string>

struct Shipment {
    std::string destination;
    int boxes;
};

bool read_shipment_values(std::istream& input, const std::string& destination, Shipment& result) {
    int boxes{0};
    input >> boxes;

    if (input.fail()) {
        return false;
    }

    if (boxes < 0) {
        return false;
    }

    result = Shipment{destination, boxes};
    return true;
}

std::string bool_text(bool value) {
    if (value) {
        return "true";
    }

    return "false";
}

void check_bool(const std::string& name, bool expected, bool actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << bool_text(expected) << ", actual " << bool_text(actual) << "\n";
        ++failed;
    }
}

void check_int(const std::string& name, int expected, int actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << expected << ", actual " << actual << "\n";
        ++failed;
    }
}

void check_text(const std::string& name, const std::string& expected, const std::string& actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected \"" << expected << "\", actual \"" << actual << "\"\n";
        ++failed;
    }
}

int main() {
    int checks{0};
    int failed{0};

    std::istringstream input_a{"4\n"};
    Shipment shipment_a{"Old Destination", 1};
    const bool accepted_a{read_shipment_values(input_a, "North Hub", shipment_a)};
    check_bool("A accepted", true, accepted_a, checks, failed);
    check_text("A destination", "North Hub", shipment_a.destination, checks, failed);
    check_int("A boxes", 4, shipment_a.boxes, checks, failed);

    std::istringstream input_b{"0\n"};
    Shipment shipment_b{"Old Destination", 1};
    const bool accepted_b{read_shipment_values(input_b, "North Hub", shipment_b)};
    check_bool("B accepted", true, accepted_b, checks, failed);
    check_text("B destination", "North Hub", shipment_b.destination, checks, failed);
    check_int("B boxes", 0, shipment_b.boxes, checks, failed);

    std::istringstream input_f{"4"};
    Shipment shipment_f{"Old Destination", 1};
    const bool accepted_f{read_shipment_values(input_f, "North Hub", shipment_f)};
    check_bool("F accepted", true, accepted_f, checks, failed);
    check_text("F destination", "North Hub", shipment_f.destination, checks, failed);
    check_int("F boxes", 4, shipment_f.boxes, checks, failed);

    std::istringstream input_g{"1250\n"};
    Shipment shipment_g{"Old Destination", 1};
    const bool accepted_g{read_shipment_values(input_g, "West End Depot", shipment_g)};
    check_bool("G accepted", true, accepted_g, checks, failed);
    check_text("G destination", "West End Depot", shipment_g.destination, checks, failed);
    check_int("G boxes", 1250, shipment_g.boxes, checks, failed);

    std::cout << "Checks: " << checks << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

**This is the first required run.** Replace the contents of `main.cpp` in `lesson_13_3` with this program, build it and run it. **Predict** the number of checks and the exit code.

<details>
<summary>Standard output and exit code</summary>

<!-- output: shipment_tests -->
```text
PASS A accepted
PASS A destination
PASS A boxes
PASS B accepted
PASS B destination
PASS B boxes
PASS F accepted
PASS F destination
PASS F boxes
PASS G accepted
PASS G destination
PASS G boxes
Checks: 12, failed: 0
```

CLion shows `Process finished with exit code 0`.

</details>

- **Every case has its own variables:** the stream `input_a`, the record `shipment_a` and the result `accepted_a`. The letter in the name says which case they belong to. No case uses the variables of another.
- **The function is the same as in lessons 10.4 and 12.2.** Only the calling code has changed: instead of `std::cin` or a file, it gets a stream with a text.
- **Four cases, twelve checks.** The summary counts checks, not cases.

## 7. Tests of a refusal: the record unchanged

**Add the cases C, D and E** from the table in point 3 to `main`, between B and F. Each one gets a new stream with its own text, the starting record `Old Destination`, 1, and the four checks of point 4. An unchanged record means that the expected name is `Old Destination` and the expected number of boxes is 1. The fourth check compares `fail()` of that case's stream, for example `input_c.fail()`, with the value in the table.

**This is the second required run.** Run the program with seven cases. **Predict** the summary.

<details>
<summary>Standard output and exit code</summary>

<!-- output: shipment_all_tests -->
```text
PASS A accepted
PASS A destination
PASS A boxes
PASS B accepted
PASS B destination
PASS B boxes
PASS C accepted
PASS C destination
PASS C boxes
PASS C fail()
PASS D accepted
PASS D destination
PASS D boxes
PASS D fail()
PASS E accepted
PASS E destination
PASS E boxes
PASS E fail()
PASS F accepted
PASS F destination
PASS F boxes
PASS G accepted
PASS G destination
PASS G boxes
Checks: 24, failed: 0
```

CLion shows `Process finished with exit code 0`.

</details>

<details>
<summary>The whole program with the cases A–G: open after your own attempt</summary>

<!-- example: shipment_all_tests -->
```cpp
#include <iostream>
#include <sstream>
#include <string>

struct Shipment {
    std::string destination;
    int boxes;
};

bool read_shipment_values(std::istream& input, const std::string& destination, Shipment& result) {
    int boxes{0};
    input >> boxes;

    if (input.fail()) {
        return false;
    }

    if (boxes < 0) {
        return false;
    }

    result = Shipment{destination, boxes};
    return true;
}

std::string bool_text(bool value) {
    if (value) {
        return "true";
    }

    return "false";
}

void check_bool(const std::string& name, bool expected, bool actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << bool_text(expected) << ", actual " << bool_text(actual) << "\n";
        ++failed;
    }
}

void check_int(const std::string& name, int expected, int actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << expected << ", actual " << actual << "\n";
        ++failed;
    }
}

void check_text(const std::string& name, const std::string& expected, const std::string& actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected \"" << expected << "\", actual \"" << actual << "\"\n";
        ++failed;
    }
}

int main() {
    int checks{0};
    int failed{0};

    std::istringstream input_a{"4\n"};
    Shipment shipment_a{"Old Destination", 1};
    const bool accepted_a{read_shipment_values(input_a, "North Hub", shipment_a)};
    check_bool("A accepted", true, accepted_a, checks, failed);
    check_text("A destination", "North Hub", shipment_a.destination, checks, failed);
    check_int("A boxes", 4, shipment_a.boxes, checks, failed);

    std::istringstream input_b{"0\n"};
    Shipment shipment_b{"Old Destination", 1};
    const bool accepted_b{read_shipment_values(input_b, "North Hub", shipment_b)};
    check_bool("B accepted", true, accepted_b, checks, failed);
    check_text("B destination", "North Hub", shipment_b.destination, checks, failed);
    check_int("B boxes", 0, shipment_b.boxes, checks, failed);

    std::istringstream input_c{"-2\n"};
    Shipment shipment_c{"Old Destination", 1};
    const bool accepted_c{read_shipment_values(input_c, "North Hub", shipment_c)};
    check_bool("C accepted", false, accepted_c, checks, failed);
    check_text("C destination", "Old Destination", shipment_c.destination, checks, failed);
    check_int("C boxes", 1, shipment_c.boxes, checks, failed);
    check_bool("C fail()", false, input_c.fail(), checks, failed);

    std::istringstream input_d{"seven\n"};
    Shipment shipment_d{"Old Destination", 1};
    const bool accepted_d{read_shipment_values(input_d, "North Hub", shipment_d)};
    check_bool("D accepted", false, accepted_d, checks, failed);
    check_text("D destination", "Old Destination", shipment_d.destination, checks, failed);
    check_int("D boxes", 1, shipment_d.boxes, checks, failed);
    check_bool("D fail()", true, input_d.fail(), checks, failed);

    std::istringstream input_e{""};
    Shipment shipment_e{"Old Destination", 1};
    const bool accepted_e{read_shipment_values(input_e, "North Hub", shipment_e)};
    check_bool("E accepted", false, accepted_e, checks, failed);
    check_text("E destination", "Old Destination", shipment_e.destination, checks, failed);
    check_int("E boxes", 1, shipment_e.boxes, checks, failed);
    check_bool("E fail()", true, input_e.fail(), checks, failed);

    std::istringstream input_f{"4"};
    Shipment shipment_f{"Old Destination", 1};
    const bool accepted_f{read_shipment_values(input_f, "North Hub", shipment_f)};
    check_bool("F accepted", true, accepted_f, checks, failed);
    check_text("F destination", "North Hub", shipment_f.destination, checks, failed);
    check_int("F boxes", 4, shipment_f.boxes, checks, failed);

    std::istringstream input_g{"1250\n"};
    Shipment shipment_g{"Old Destination", 1};
    const bool accepted_g{read_shipment_values(input_g, "West End Depot", shipment_g)};
    check_bool("G accepted", true, accepted_g, checks, failed);
    check_text("G destination", "West End Depot", shipment_g.destination, checks, failed);
    check_int("G boxes", 1250, shipment_g.boxes, checks, failed);

    std::cout << "Checks: " << checks << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

</details>

- **A refusal checked from three sides:** the result `false`, the record unchanged, and the stream state. `fail()` tells C, where there was a number but not an allowed one, apart from D and E, where no number could be read. It's the same information that `main` in lesson 10.4 used to choose between `Invalid shipments` and `Input error`.
- **All checks passed.** This means that these seven cases didn't detect a mismatch with the contract, not that the function is correct for all data (lesson 13.2).

## 8. When the `bool` matches but the record doesn't

Here are two versions of `read_shipment_values` with one bug each. Both build, and for the cases A, B, D, E, F and G they give correct results:

| Version | Change in the function | Effect according to the contract |
|---|---|---|
| no check of a negative value | the check `if (boxes < 0)` removed together with its `return false;` | a negative number of boxes is accepted |
| result assigned too early | `result = Shipment{destination, boxes};` stands before `if (boxes < 0)`, as in the program of lesson 10.4, point 8 | the function refuses but changes the record |

**For each version, predict** which checks of the suite A–G will give `FAIL`, with which expected and actual value. In particular: will the check `C accepted` detect the second version? Running both versions is optional: it's enough to change the function in `main.cpp` and then restore it.

<details>
<summary>Review: two versions and their results</summary>

**No check of a negative value.**

<!-- example: shipment_all_tests_negative_bug exit=1 -->
```cpp
#include <iostream>
#include <sstream>
#include <string>

struct Shipment {
    std::string destination;
    int boxes;
};

bool read_shipment_values(std::istream& input, const std::string& destination, Shipment& result) {
    int boxes{0};
    input >> boxes;

    if (input.fail()) {
        return false;
    }

    result = Shipment{destination, boxes};
    return true;
}

std::string bool_text(bool value) {
    if (value) {
        return "true";
    }

    return "false";
}

void check_bool(const std::string& name, bool expected, bool actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << bool_text(expected) << ", actual " << bool_text(actual) << "\n";
        ++failed;
    }
}

void check_int(const std::string& name, int expected, int actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << expected << ", actual " << actual << "\n";
        ++failed;
    }
}

void check_text(const std::string& name, const std::string& expected, const std::string& actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected \"" << expected << "\", actual \"" << actual << "\"\n";
        ++failed;
    }
}

int main() {
    int checks{0};
    int failed{0};

    std::istringstream input_a{"4\n"};
    Shipment shipment_a{"Old Destination", 1};
    const bool accepted_a{read_shipment_values(input_a, "North Hub", shipment_a)};
    check_bool("A accepted", true, accepted_a, checks, failed);
    check_text("A destination", "North Hub", shipment_a.destination, checks, failed);
    check_int("A boxes", 4, shipment_a.boxes, checks, failed);

    std::istringstream input_b{"0\n"};
    Shipment shipment_b{"Old Destination", 1};
    const bool accepted_b{read_shipment_values(input_b, "North Hub", shipment_b)};
    check_bool("B accepted", true, accepted_b, checks, failed);
    check_text("B destination", "North Hub", shipment_b.destination, checks, failed);
    check_int("B boxes", 0, shipment_b.boxes, checks, failed);

    std::istringstream input_c{"-2\n"};
    Shipment shipment_c{"Old Destination", 1};
    const bool accepted_c{read_shipment_values(input_c, "North Hub", shipment_c)};
    check_bool("C accepted", false, accepted_c, checks, failed);
    check_text("C destination", "Old Destination", shipment_c.destination, checks, failed);
    check_int("C boxes", 1, shipment_c.boxes, checks, failed);
    check_bool("C fail()", false, input_c.fail(), checks, failed);

    std::istringstream input_d{"seven\n"};
    Shipment shipment_d{"Old Destination", 1};
    const bool accepted_d{read_shipment_values(input_d, "North Hub", shipment_d)};
    check_bool("D accepted", false, accepted_d, checks, failed);
    check_text("D destination", "Old Destination", shipment_d.destination, checks, failed);
    check_int("D boxes", 1, shipment_d.boxes, checks, failed);
    check_bool("D fail()", true, input_d.fail(), checks, failed);

    std::istringstream input_e{""};
    Shipment shipment_e{"Old Destination", 1};
    const bool accepted_e{read_shipment_values(input_e, "North Hub", shipment_e)};
    check_bool("E accepted", false, accepted_e, checks, failed);
    check_text("E destination", "Old Destination", shipment_e.destination, checks, failed);
    check_int("E boxes", 1, shipment_e.boxes, checks, failed);
    check_bool("E fail()", true, input_e.fail(), checks, failed);

    std::istringstream input_f{"4"};
    Shipment shipment_f{"Old Destination", 1};
    const bool accepted_f{read_shipment_values(input_f, "North Hub", shipment_f)};
    check_bool("F accepted", true, accepted_f, checks, failed);
    check_text("F destination", "North Hub", shipment_f.destination, checks, failed);
    check_int("F boxes", 4, shipment_f.boxes, checks, failed);

    std::istringstream input_g{"1250\n"};
    Shipment shipment_g{"Old Destination", 1};
    const bool accepted_g{read_shipment_values(input_g, "West End Depot", shipment_g)};
    check_bool("G accepted", true, accepted_g, checks, failed);
    check_text("G destination", "West End Depot", shipment_g.destination, checks, failed);
    check_int("G boxes", 1250, shipment_g.boxes, checks, failed);

    std::cout << "Checks: " << checks << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

<!-- output: shipment_all_tests_negative_bug -->
```text
PASS A accepted
PASS A destination
PASS A boxes
PASS B accepted
PASS B destination
PASS B boxes
FAIL C accepted: expected false, actual true
FAIL C destination: expected "Old Destination", actual "North Hub"
FAIL C boxes: expected 1, actual -2
PASS C fail()
PASS D accepted
PASS D destination
PASS D boxes
PASS D fail()
PASS E accepted
PASS E destination
PASS E boxes
PASS E fail()
PASS F accepted
PASS F destination
PASS F boxes
PASS G accepted
PASS G destination
PASS G boxes
Checks: 24, failed: 3
```

Exit code: 1.

**Result assigned too early.**

<!-- example: shipment_all_tests_early_bug exit=1 -->
```cpp
#include <iostream>
#include <sstream>
#include <string>

struct Shipment {
    std::string destination;
    int boxes;
};

bool read_shipment_values(std::istream& input, const std::string& destination, Shipment& result) {
    int boxes{0};
    input >> boxes;

    if (input.fail()) {
        return false;
    }

    result = Shipment{destination, boxes};

    if (boxes < 0) {
        return false;
    }

    return true;
}

std::string bool_text(bool value) {
    if (value) {
        return "true";
    }

    return "false";
}

void check_bool(const std::string& name, bool expected, bool actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << bool_text(expected) << ", actual " << bool_text(actual) << "\n";
        ++failed;
    }
}

void check_int(const std::string& name, int expected, int actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << expected << ", actual " << actual << "\n";
        ++failed;
    }
}

void check_text(const std::string& name, const std::string& expected, const std::string& actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected \"" << expected << "\", actual \"" << actual << "\"\n";
        ++failed;
    }
}

int main() {
    int checks{0};
    int failed{0};

    std::istringstream input_a{"4\n"};
    Shipment shipment_a{"Old Destination", 1};
    const bool accepted_a{read_shipment_values(input_a, "North Hub", shipment_a)};
    check_bool("A accepted", true, accepted_a, checks, failed);
    check_text("A destination", "North Hub", shipment_a.destination, checks, failed);
    check_int("A boxes", 4, shipment_a.boxes, checks, failed);

    std::istringstream input_b{"0\n"};
    Shipment shipment_b{"Old Destination", 1};
    const bool accepted_b{read_shipment_values(input_b, "North Hub", shipment_b)};
    check_bool("B accepted", true, accepted_b, checks, failed);
    check_text("B destination", "North Hub", shipment_b.destination, checks, failed);
    check_int("B boxes", 0, shipment_b.boxes, checks, failed);

    std::istringstream input_c{"-2\n"};
    Shipment shipment_c{"Old Destination", 1};
    const bool accepted_c{read_shipment_values(input_c, "North Hub", shipment_c)};
    check_bool("C accepted", false, accepted_c, checks, failed);
    check_text("C destination", "Old Destination", shipment_c.destination, checks, failed);
    check_int("C boxes", 1, shipment_c.boxes, checks, failed);
    check_bool("C fail()", false, input_c.fail(), checks, failed);

    std::istringstream input_d{"seven\n"};
    Shipment shipment_d{"Old Destination", 1};
    const bool accepted_d{read_shipment_values(input_d, "North Hub", shipment_d)};
    check_bool("D accepted", false, accepted_d, checks, failed);
    check_text("D destination", "Old Destination", shipment_d.destination, checks, failed);
    check_int("D boxes", 1, shipment_d.boxes, checks, failed);
    check_bool("D fail()", true, input_d.fail(), checks, failed);

    std::istringstream input_e{""};
    Shipment shipment_e{"Old Destination", 1};
    const bool accepted_e{read_shipment_values(input_e, "North Hub", shipment_e)};
    check_bool("E accepted", false, accepted_e, checks, failed);
    check_text("E destination", "Old Destination", shipment_e.destination, checks, failed);
    check_int("E boxes", 1, shipment_e.boxes, checks, failed);
    check_bool("E fail()", true, input_e.fail(), checks, failed);

    std::istringstream input_f{"4"};
    Shipment shipment_f{"Old Destination", 1};
    const bool accepted_f{read_shipment_values(input_f, "North Hub", shipment_f)};
    check_bool("F accepted", true, accepted_f, checks, failed);
    check_text("F destination", "North Hub", shipment_f.destination, checks, failed);
    check_int("F boxes", 4, shipment_f.boxes, checks, failed);

    std::istringstream input_g{"1250\n"};
    Shipment shipment_g{"Old Destination", 1};
    const bool accepted_g{read_shipment_values(input_g, "West End Depot", shipment_g)};
    check_bool("G accepted", true, accepted_g, checks, failed);
    check_text("G destination", "West End Depot", shipment_g.destination, checks, failed);
    check_int("G boxes", 1250, shipment_g.boxes, checks, failed);

    std::cout << "Checks: " << checks << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

<!-- output: shipment_all_tests_early_bug -->
```text
PASS A accepted
PASS A destination
PASS A boxes
PASS B accepted
PASS B destination
PASS B boxes
PASS C accepted
FAIL C destination: expected "Old Destination", actual "North Hub"
FAIL C boxes: expected 1, actual -2
PASS C fail()
PASS D accepted
PASS D destination
PASS D boxes
PASS D fail()
PASS E accepted
PASS E destination
PASS E boxes
PASS E fail()
PASS F accepted
PASS F destination
PASS F boxes
PASS G accepted
PASS G destination
PASS G boxes
Checks: 24, failed: 2
```

Exit code: 1.

| Bug | Case | Checks with `FAIL` | Expected | Actual | Failures |
|---|---|---|---|---|---|
| no check of a negative value | C | `C accepted` | `false` | `true` | 3 |
| | | `C destination` | `"Old Destination"` | `"North Hub"` | |
| | | `C boxes` | 1 | -2 | |
| result assigned too early | C | `C destination` | `"Old Destination"` | `"North Hub"` | 2 |
| | | `C boxes` | 1 | -2 | |

- **Both bugs are detected by C,** the only case with a number that was read but isn't allowed. D and E pass for both versions: after a failed read both functions return `false` before they reach the record.
- **In the second version `C accepted` gives `PASS`.** The function returns the correct `bool` and still breaks the contract, because it changes the record. **Testing the return value alone isn't always enough.** If the suite checked only `accepted`, this version would pass every check, and the test program would end with code 0.
- **The same bug, another way of detecting it.** In lesson 10.4 this bug showed up by printing the state of `result` and comparing it with a prediction. Now the test program detects it, every time, without typing data and without reading a printout.
- Each program ends with code 1, because the failure counter is greater than zero.

</details>

## 9. Diagnostic: one stream for two tests

**The situation.** Someone wants to check that the function stores in the record the name it was given. They prepared two independent tests with the same number 4 and different names. They decided that since both need the same text, one stream will do. The function `read_shipment_values` is **correct** here.

<!-- example: shipment_shared_stream exit=1 -->
```cpp
#include <iostream>
#include <sstream>
#include <string>

struct Shipment {
    std::string destination;
    int boxes;
};

bool read_shipment_values(std::istream& input, const std::string& destination, Shipment& result) {
    int boxes{0};
    input >> boxes;

    if (input.fail()) {
        return false;
    }

    if (boxes < 0) {
        return false;
    }

    result = Shipment{destination, boxes};
    return true;
}

std::string bool_text(bool value) {
    if (value) {
        return "true";
    }

    return "false";
}

void check_bool(const std::string& name, bool expected, bool actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << bool_text(expected) << ", actual " << bool_text(actual) << "\n";
        ++failed;
    }
}

void check_int(const std::string& name, int expected, int actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << expected << ", actual " << actual << "\n";
        ++failed;
    }
}

void check_text(const std::string& name, const std::string& expected, const std::string& actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected \"" << expected << "\", actual \"" << actual << "\"\n";
        ++failed;
    }
}

int main() {
    int checks{0};
    int failed{0};
    std::istringstream input{"4"};

    Shipment north{"Old Destination", 1};
    const bool north_accepted{read_shipment_values(input, "North Hub", north)};
    check_bool("North Hub accepted", true, north_accepted, checks, failed);
    check_text("North Hub destination", "North Hub", north.destination, checks, failed);
    check_int("North Hub boxes", 4, north.boxes, checks, failed);

    Shipment south{"Old Destination", 1};
    const bool south_accepted{read_shipment_values(input, "South Depot", south)};
    check_bool("South Depot accepted", true, south_accepted, checks, failed);
    check_text("South Depot destination", "South Depot", south.destination, checks, failed);
    check_int("South Depot boxes", 4, south.boxes, checks, failed);

    std::cout << "Checks: " << checks << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

**This is the third required run: one diagnostic task.** The type `Shipment`, the function `read_shipment_values` and the checking functions are the same as in point 7, so in `main.cpp` it's enough to replace `main`.

1. **Predict** the result of the first call, for `North Hub`.
2. **Predict** the result of the second call, for `South Depot`.
3. Run the program. Find out where in the text `4` the first read ended and what was left in the stream for the second one.
4. Explain why the text `4` doesn't appear in the stream again.
5. Point out the mistake in how the tests are organised: is it in the function or in the test program?
6. Propose the smallest fix.
7. Make it and run the program again.
8. Explain why every independent test should start with its own stream.

<details>
<summary>Standard output and exit code</summary>

<!-- output: shipment_shared_stream -->
```text
PASS North Hub accepted
PASS North Hub destination
PASS North Hub boxes
FAIL South Depot accepted: expected true, actual false
FAIL South Depot destination: expected "South Depot", actual "Old Destination"
FAIL South Depot boxes: expected 4, actual 1
Checks: 6, failed: 3
```

CLion shows `Process finished with exit code 1`.

</details>

<details>
<summary>Explanation and fix</summary>

| Moment | What is left in the stream | Result of the read |
|---|---|---|
| before the first call | `4` | |
| after the first call | nothing: `>>` read `4` and reached the end of the text | the number 4, `fail()` gives `false` |
| after the second call | nothing | a failed read, `fail()` gives `true` |

- **The first test is correct:** `true`, `North Hub`, 4.
- **The second test gets a stream with no data left in it.** `>>` finds no number, so the function returns `false` and leaves the record unchanged. That's exactly what its contract says, so **the function is correct and the mistake is in the test program.**
- **Characters that have been read don't come back.** The stream remembers how far it has got, just as `std::cin` remembers which data has been read. The second call doesn't get a new copy of the text. With the text `"4\n"` the result would be the same: the second read would skip the line end and wouldn't find a number either.
- **`clear()` wouldn't help.** It would remove the mark of the failed read, but it creates no new data (lesson 4.6). After `clear()` the stream would still be empty.
- **The smallest fix:** a separate stream for each test, each with the same text. You don't change the function.

<!-- example: shipment_separate_streams -->
```cpp
#include <iostream>
#include <sstream>
#include <string>

struct Shipment {
    std::string destination;
    int boxes;
};

bool read_shipment_values(std::istream& input, const std::string& destination, Shipment& result) {
    int boxes{0};
    input >> boxes;

    if (input.fail()) {
        return false;
    }

    if (boxes < 0) {
        return false;
    }

    result = Shipment{destination, boxes};
    return true;
}

std::string bool_text(bool value) {
    if (value) {
        return "true";
    }

    return "false";
}

void check_bool(const std::string& name, bool expected, bool actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << bool_text(expected) << ", actual " << bool_text(actual) << "\n";
        ++failed;
    }
}

void check_int(const std::string& name, int expected, int actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << expected << ", actual " << actual << "\n";
        ++failed;
    }
}

void check_text(const std::string& name, const std::string& expected, const std::string& actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected \"" << expected << "\", actual \"" << actual << "\"\n";
        ++failed;
    }
}

int main() {
    int checks{0};
    int failed{0};

    std::istringstream north_input{"4"};
    Shipment north{"Old Destination", 1};
    const bool north_accepted{read_shipment_values(north_input, "North Hub", north)};
    check_bool("North Hub accepted", true, north_accepted, checks, failed);
    check_text("North Hub destination", "North Hub", north.destination, checks, failed);
    check_int("North Hub boxes", 4, north.boxes, checks, failed);

    std::istringstream south_input{"4"};
    Shipment south{"Old Destination", 1};
    const bool south_accepted{read_shipment_values(south_input, "South Depot", south)};
    check_bool("South Depot accepted", true, south_accepted, checks, failed);
    check_text("South Depot destination", "South Depot", south.destination, checks, failed);
    check_int("South Depot boxes", 4, south.boxes, checks, failed);

    std::cout << "Checks: " << checks << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

<!-- output: shipment_separate_streams -->
```text
PASS North Hub accepted
PASS North Hub destination
PASS North Hub boxes
PASS South Depot accepted
PASS South Depot destination
PASS South Depot boxes
Checks: 6, failed: 0
```

Exit code: 0. The same, unchanged function passes both tests.

**Using a stream again isn't a mistake in itself.** The loop in `main` of lesson 10.4 read all the shipments one after another from one `std::cin`, and that was intended: each read was to start where the previous one ended. If a test had to check reading two successive shipments from one source, one stream with both numbers would be right. **The mistake is assuming that two independent cases automatically start from the same data.**

</details>

**The rule from this diagnostic:** test cases have to be independent of each other. The result of one mustn't depend on what the previous one did. That's why every case gets a new stream and its own result variables.

## 10. Mission: tests for the chore log

The chore log program of the lesson 12.3 mission reads the file `chores.txt` with the function `read_chores`. Now the task is different: **test this function without a file**, with texts in `std::istringstream`.

**The contract of the function from lesson 12.3**, without any change:

- the header: `bool read_chores(std::istream& input, std::vector<Chore>& chores, std::string& error, int& error_line)`, and `Chore` has the text fields `name` and `status`;
- every record takes two physical lines: the name of the chore and the status `done` or `pending`, case-sensitive and without extra spaces;
- the data ends only with the end of the data where another record would start, and the last line may have no line end;
- every empty line is an error `"empty"`, a non-empty status other than `done` and `pending` is an error `"invalid"`, and a missing status line after a name is `"incomplete"`;
- on success the function returns `true`, and the vector holds the records in the order of the data;
- at the first error the function returns `false`, and stores in `error` and `error_line` the error kind and the physical line number, counted from 1; for `"incomplete"` it's the number of the name's line.

**What the contract doesn't promise.** After `false`, the vector may hold records read before the error: the program of lesson 12.3 simply doesn't print the report then. After `true`, the function doesn't have to change `error` or `error_line`. The tests check what the contract promises, not accidental details of the implementation.

In `cpp-workspace`, create a folder `chore_log_tests`, copy `main.cpp` and `CMakeLists.txt` from the original `lesson_05_first_program` into it, and open it in CLion. Leave `CMakeLists.txt` unchanged. From the [solution of the lesson 12.3 mission](../module_12_text_files/lesson_03_end_of_data_and_errors.en.md#example-solutions), copy the type `Chore` and the function `read_chores` into `main.cpp`, unchanged, but without its `main` and without `#include <fstream>`. You don't have to write the function from memory: it's the tests that are assessed.

**The cases.** Each text is exactly the data you pass to the constructor of `std::istringstream`:

| Case | Stream text |
|---|---|
| A | `""` |
| B | `"Clean tables\ndone\nSort books\npending\n"` |
| C | `"Clean tables\ndone"` |
| D | `"\n"` |
| E | `"Clean tables\n\n"` |
| F | `"Clean tables\nlater\n"` |
| G | `"Clean tables\n"` |
| H | `"Clean tables\ndone\n\n"` |
| I | `"Clean tables\ndone\nSort books\nlater\n"` |
| J | `"Clean tables\ndone\nSort books"` |
| K | `"Clean tables\ndone\nClean tables\npending"` |
| L | `"Clean tables\ndone \n"` |
| M | `"Clean tables\nlater"` |

You have to decide on your own:

1. how to create a stream with each of these texts and pass it to `read_chores`;
2. how to prepare the result vector and the variables `error` and `error_line` for each case;
3. which properties to check on success and which on an error;
4. how to check the size of the vector, given that `size()` returns `std::size_t`;
5. how to compare the successive records, field by field, and how not to read an element that isn't in the vector;
6. how to compare the error kind and the line number;
7. which cases check the end of the data, which an empty line, which a wrong status, and which a missing final line end;
8. how to show that no case uses the result of the previous one.

**Order of work:**

1. **Settle the expected results before you write code.** For each case, write down on paper: success or error; on success, the number of records and each record; on an error, the kind and the line number. The results have to come from the contract, not from running the function.
2. Write the test program: the checking functions, for each case a separate stream, vector, `error` and `error_line`, then the checks, the summary and exit code 1 after a failure.
3. **This is the fourth required run:** run the program with the correct function. Every check should give `PASS`, and the exit code should be 0. If any gives `FAIL`, first settle from the contract whether the expected result or the check is wrong (lesson 13.2, point 9).
4. **A deliberate bug.** Put the old ending rule of lesson 12.3, point 7, into `read_chores`: the loop condition `while (!input.fail() && !name.empty())`, and no `if (name.empty())` check at the start of the loop. **Predict** which checks will give `FAIL`.
5. **This is the fifth required run:** run the same test program with the buggy function. Write down which cases detected the bug and what the exit code was. If no check gave `FAIL`, add a case that tells the two versions apart. Then restore the correct function and run the tests once more.
6. **Justify your choice.** For the cases C, D, H and J, write one sentence each on what mistake in the function it could detect.

<details>
<summary>Expected results: open after preparing your own</summary>

| Case | Result | Records or error | What it checks |
|---|---|---|---|
| A | `true` | 0 records | an empty text, that is, the end of the data at once |
| B | `true` | `Clean tables`, `done`; `Sort books`, `pending` | two records in order, names with spaces |
| C | `true` | `Clean tables`, `done` | the last status without a line end |
| D | `false` | `"empty"`, line 1 | one empty line, which isn't the same as an empty text |
| E | `false` | `"empty"`, line 2 | an empty line in place of the status |
| F | `false` | `"invalid"`, line 2 | a wrong status of the first record |
| G | `false` | `"incomplete"`, line 1 | no status line, the number of the name's line |
| H | `false` | `"empty"`, line 3 | an empty line after the last complete record |
| I | `false` | `"invalid"`, line 4 | the first error after a correct record, the line number, not the record number |
| J | `false` | `"incomplete"`, line 3 | a name alone without a line end after a correct record |
| K | `true` | `Clean tables`, `done`; `Clean tables`, `pending` | a repeated name, the order of the statuses |
| L | `false` | `"invalid"`, line 2 | a space after the status |
| M | `false` | `"invalid"`, line 2 | a wrong status without a line end |

</details>

### Success criteria

- The program builds as C++20, and `CMakeLists.txt` is as in lesson 0.5.
- `read_chores` is as in the solution of lesson 12.3, and all the test data is in texts passed to `std::istringstream`. The program opens no file and doesn't read `std::cin`.
- The expected results come from the contract and were written before running.
- Every case has its own stream, vector, `error` and `error_line`.
- On success the program checks the result, the size of the vector and each record, field by field, in order. It checks the elements only when the size matches.
- On an error the program checks the result, the error kind and the physical line number.
- Every check has a name and prints `PASS` or `FAIL` with the expected and the actual value, and at the end the program prints a summary.
- With the correct function every check passes and the exit code is 0. With the old ending rule at least one gives `FAIL` and the exit code is 1.
- You can explain why A and D are different cases and why G gives line 1 and J line 3.

When the result matches, you can save the project in Git, as in lesson 1.5: `main.cpp` and `CMakeLists.txt`, without the build folder.

<details>
<summary>Hint 1: the data source</summary>

The function expects `std::istream&`. Which object in this lesson is an input stream that takes its characters from a text in the code? Copy each text from the table into the code exactly, with `\n` at the end or without it: that's the difference between cases, not a detail of notation.

</details>

<details>
<summary>Hint 2: the result of the function</summary>

After calling `read_chores` you have four things to look at: the `bool` result, the vector, `error` and `error_line`. On success what matters is the result and the vector; on an error, the result, `error` and `error_line`. The size of the vector has the type `std::size_t`, so a checking function with parameters of that type will be useful for comparing it (lesson 6.3). Check a record field by field, by index, but only after making sure the size matches.

</details>

<details>
<summary>Hint 3: independent cases</summary>

What would the vector in case C hold if it were the same vector as in case B? What would case C read from the stream of case B? What would be left in `error` if a success case got the variable after an error case? Every case needs a new stream and its own result variables.

</details>

An example solution is in the [Example solutions](#example-solutions) part.

## 11. When something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| The compiler reports an error at `std::istringstream`, for example `implicit instantiation of undefined template 'std::basic_istringstream<char>'` | `#include <sstream>` is missing. The standard doesn't guarantee that `<iostream>` includes it. | Always include `<sstream>` when you use `std::istringstream`. |
| The first case passes, and the next one, with correct data, gives `actual false` | The next case reads from the stream of the previous one, which has no data left (point 9). | Create a new `std::istringstream` for every case. |
| `size` gives more records than the text has | The case got the vector left by the previous case, and the function appends records to it with `push_back`. | Prepare a new, empty vector for every case. |
| The program ends suddenly or prints random values while checking the records | A check reads an element that isn't in the vector: undefined behaviour (lesson 6.3). | Check the elements only when the size of the vector matches. |
| `FAIL ... error_line` for an error in the second record, although the function is correct | The expected result gives the record number or doesn't count the status line. | Count the physical lines from 1, as in the tables of lesson 12.3, point 4. |
| `FAIL ... expected "empty", actual ""` | The function returned `true` and didn't store an error kind, so the variable stayed as it was prepared. The check of `complete` in the same case gives `FAIL` too. | Settle from the contract whether this text is an error. If it is, the bug is in the function. |

## 12. Explain

Answer in your own words, preferably in writing. Only then compare with the example answers.

1. Why can a `std::istringstream` be passed to a function with a `std::istream&` parameter?
2. How does `std::istringstream` differ from `std::ifstream`?
3. Why does a test of a reading function not need a physical file?
4. Why should every independent case get a new stream?
5. What can happen when a second test uses a stream from which the first one has already read the data?
6. Why may checking the `bool` result alone not be enough?
7. How do you check that a record stayed unchanged after a refusal?
8. How do you check the error kind and the line number?
9. Why are an empty stream and a stream with one line end different cases?
10. How can a test detect a bug that doesn't change the return value but changes the result data?

<details>
<summary>Example answers</summary>

1. Because the standard library defines `std::istringstream` as a special kind of `std::istream`, just like `std::ifstream`. It has `>>`, `fail()` and works with `std::getline`, so it has everything a function needs from an input stream. The `std::istream&` parameter becomes another name for the stream over the text.
2. `std::ifstream` reads characters from an open file on disk, and `std::istringstream` from the text given when it's created. A program that reads a file still uses `std::ifstream`. A stream over a text is handy above all in tests.
3. Because the function reads from the stream it's given and doesn't know where the characters come from. A text in `std::istringstream` gives it exactly the same bytes as a file, without a working directory, without preparing a file and without typing data.
4. Because a stream remembers how far reading has got, and characters that have been read don't come back to it. A new stream gives each case its own data from the start, whatever the other cases did.
5. The second test starts reading where the first one ended. If the text has run out, the read fails and the test gives `FAIL` although the function is correct. The mistake is then in the test program, not in the function.
6. Because a function can have several effects: the `bool` result, a record or a vector, and data about an error. It can return the correct `bool` and at the same time store wrong data or change a record that was supposed to stay unchanged.
7. Prepare a record with values the function wouldn't store for this data, such as `Old Destination` and 1, and after the refusal compare each field with those values.
8. Prepare separate variables `error` and `error_line` for the case, and after the call compare `error` with the expected kind, such as `"empty"`, with `check_text`, and `error_line` with the physical line number with `check_int`.
9. An empty stream has no line at all: the first read fails, so the data ends and the result is success with no records. The stream `"\n"` has one empty line: the read succeeds, and the empty name is an error `"empty"` on line 1.
10. By checking, besides the return value, also the record, the vector or the data about the error. For example, a version that refuses but changes the record is detected by the checks of the record's fields, although the check of the `bool` result gives `PASS`.

</details>

## Summary

- `std::istringstream` from `<sstream>` is an input stream over the text given when it's created. A function with a `std::istream&` parameter reads from it just as from `std::cin` and from a file.
- The text in the stream is exactly the data: `""` is an empty file, `"\n"` one empty line, and a text without `\n` at the end is a last line without a line end.
- A reading function doesn't have to be changed to be tested. Only the calling code changes.
- One call can have several effects. A test checks each one the contract promises: the result, the record or the vector, the data about an error and, if the contract mentions it, the stream state.
- A case is one set of data and one call, and a check is one comparison. The summary counts checks.
- Every independent case gets a new stream and its own result variables, because characters that have been read don't come back to the stream. One stream is right when a program has to read successive data from one source.

## What's next

The test programs in this lesson contain a copy of the tested function. If someone changed the function in the chore log program, the copy in the test program would stay old. The next lesson of Module 13 is in preparation.

---

## Example solutions

Look here **after your own attempt**. This is one of the correct solutions. Your names, the order of the cases and the number of checks may differ, as long as every case has its own stream and result variables, and the checks cover everything the contract promises.

<details>
<summary>Section 10: the mission, tests for the chore log</summary>

**`main.cpp`** with the function of lesson 12.3 and the cases A–M:

<!-- example: chore_tests -->
```cpp
#include <cstddef>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

struct Chore {
    std::string name;
    std::string status;
};

bool read_chores(std::istream& input, std::vector<Chore>& chores, std::string& error, int& error_line) {
    int line_number{0};
    std::string name{};
    std::getline(input, name);

    while (!input.fail()) {
        ++line_number;

        if (name.empty()) {
            error = "empty";
            error_line = line_number;
            return false;
        }

        std::string status{};
        std::getline(input, status);

        if (input.fail()) {
            error = "incomplete";
            error_line = line_number;
            return false;
        }

        ++line_number;

        if (status.empty()) {
            error = "empty";
            error_line = line_number;
            return false;
        }

        if (status != "done" && status != "pending") {
            error = "invalid";
            error_line = line_number;
            return false;
        }

        chores.push_back(Chore{name, status});
        std::getline(input, name);
    }

    return true;
}

std::string bool_text(bool value) {
    if (value) {
        return "true";
    }

    return "false";
}

void check_bool(const std::string& name, bool expected, bool actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << bool_text(expected) << ", actual " << bool_text(actual) << "\n";
        ++failed;
    }
}

void check_int(const std::string& name, int expected, int actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << expected << ", actual " << actual << "\n";
        ++failed;
    }
}

void check_size(const std::string& name, std::size_t expected, std::size_t actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << expected << ", actual " << actual << "\n";
        ++failed;
    }
}

void check_text(const std::string& name, const std::string& expected, const std::string& actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected \"" << expected << "\", actual \"" << actual << "\"\n";
        ++failed;
    }
}

int main() {
    int checks{0};
    int failed{0};

    std::istringstream input_a{""};
    std::vector<Chore> chores_a{};
    std::string error_a{};
    int error_line_a{0};
    const bool complete_a{read_chores(input_a, chores_a, error_a, error_line_a)};
    check_bool("A complete", true, complete_a, checks, failed);
    check_size("A size", 0, chores_a.size(), checks, failed);

    std::istringstream input_b{"Clean tables\ndone\nSort books\npending\n"};
    std::vector<Chore> chores_b{};
    std::string error_b{};
    int error_line_b{0};
    const bool complete_b{read_chores(input_b, chores_b, error_b, error_line_b)};
    check_bool("B complete", true, complete_b, checks, failed);
    check_size("B size", 2, chores_b.size(), checks, failed);

    if (chores_b.size() == 2) {
        check_text("B chores[0].name", "Clean tables", chores_b[0].name, checks, failed);
        check_text("B chores[0].status", "done", chores_b[0].status, checks, failed);
        check_text("B chores[1].name", "Sort books", chores_b[1].name, checks, failed);
        check_text("B chores[1].status", "pending", chores_b[1].status, checks, failed);
    }

    std::istringstream input_c{"Clean tables\ndone"};
    std::vector<Chore> chores_c{};
    std::string error_c{};
    int error_line_c{0};
    const bool complete_c{read_chores(input_c, chores_c, error_c, error_line_c)};
    check_bool("C complete", true, complete_c, checks, failed);
    check_size("C size", 1, chores_c.size(), checks, failed);

    if (chores_c.size() == 1) {
        check_text("C chores[0].name", "Clean tables", chores_c[0].name, checks, failed);
        check_text("C chores[0].status", "done", chores_c[0].status, checks, failed);
    }

    std::istringstream input_d{"\n"};
    std::vector<Chore> chores_d{};
    std::string error_d{};
    int error_line_d{0};
    const bool complete_d{read_chores(input_d, chores_d, error_d, error_line_d)};
    check_bool("D complete", false, complete_d, checks, failed);
    check_text("D error", "empty", error_d, checks, failed);
    check_int("D error_line", 1, error_line_d, checks, failed);

    std::istringstream input_e{"Clean tables\n\n"};
    std::vector<Chore> chores_e{};
    std::string error_e{};
    int error_line_e{0};
    const bool complete_e{read_chores(input_e, chores_e, error_e, error_line_e)};
    check_bool("E complete", false, complete_e, checks, failed);
    check_text("E error", "empty", error_e, checks, failed);
    check_int("E error_line", 2, error_line_e, checks, failed);

    std::istringstream input_f{"Clean tables\nlater\n"};
    std::vector<Chore> chores_f{};
    std::string error_f{};
    int error_line_f{0};
    const bool complete_f{read_chores(input_f, chores_f, error_f, error_line_f)};
    check_bool("F complete", false, complete_f, checks, failed);
    check_text("F error", "invalid", error_f, checks, failed);
    check_int("F error_line", 2, error_line_f, checks, failed);

    std::istringstream input_g{"Clean tables\n"};
    std::vector<Chore> chores_g{};
    std::string error_g{};
    int error_line_g{0};
    const bool complete_g{read_chores(input_g, chores_g, error_g, error_line_g)};
    check_bool("G complete", false, complete_g, checks, failed);
    check_text("G error", "incomplete", error_g, checks, failed);
    check_int("G error_line", 1, error_line_g, checks, failed);

    std::istringstream input_h{"Clean tables\ndone\n\n"};
    std::vector<Chore> chores_h{};
    std::string error_h{};
    int error_line_h{0};
    const bool complete_h{read_chores(input_h, chores_h, error_h, error_line_h)};
    check_bool("H complete", false, complete_h, checks, failed);
    check_text("H error", "empty", error_h, checks, failed);
    check_int("H error_line", 3, error_line_h, checks, failed);

    std::istringstream input_i{"Clean tables\ndone\nSort books\nlater\n"};
    std::vector<Chore> chores_i{};
    std::string error_i{};
    int error_line_i{0};
    const bool complete_i{read_chores(input_i, chores_i, error_i, error_line_i)};
    check_bool("I complete", false, complete_i, checks, failed);
    check_text("I error", "invalid", error_i, checks, failed);
    check_int("I error_line", 4, error_line_i, checks, failed);

    std::istringstream input_j{"Clean tables\ndone\nSort books"};
    std::vector<Chore> chores_j{};
    std::string error_j{};
    int error_line_j{0};
    const bool complete_j{read_chores(input_j, chores_j, error_j, error_line_j)};
    check_bool("J complete", false, complete_j, checks, failed);
    check_text("J error", "incomplete", error_j, checks, failed);
    check_int("J error_line", 3, error_line_j, checks, failed);

    std::istringstream input_k{"Clean tables\ndone\nClean tables\npending"};
    std::vector<Chore> chores_k{};
    std::string error_k{};
    int error_line_k{0};
    const bool complete_k{read_chores(input_k, chores_k, error_k, error_line_k)};
    check_bool("K complete", true, complete_k, checks, failed);
    check_size("K size", 2, chores_k.size(), checks, failed);

    if (chores_k.size() == 2) {
        check_text("K chores[0].name", "Clean tables", chores_k[0].name, checks, failed);
        check_text("K chores[0].status", "done", chores_k[0].status, checks, failed);
        check_text("K chores[1].name", "Clean tables", chores_k[1].name, checks, failed);
        check_text("K chores[1].status", "pending", chores_k[1].status, checks, failed);
    }

    std::istringstream input_l{"Clean tables\ndone \n"};
    std::vector<Chore> chores_l{};
    std::string error_l{};
    int error_line_l{0};
    const bool complete_l{read_chores(input_l, chores_l, error_l, error_line_l)};
    check_bool("L complete", false, complete_l, checks, failed);
    check_text("L error", "invalid", error_l, checks, failed);
    check_int("L error_line", 2, error_line_l, checks, failed);

    std::istringstream input_m{"Clean tables\nlater"};
    std::vector<Chore> chores_m{};
    std::string error_m{};
    int error_line_m{0};
    const bool complete_m{read_chores(input_m, chores_m, error_m, error_line_m)};
    check_bool("M complete", false, complete_m, checks, failed);
    check_text("M error", "invalid", error_m, checks, failed);
    check_int("M error_line", 2, error_line_m, checks, failed);

    std::cout << "Checks: " << checks << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

<!-- output: chore_tests -->
```text
PASS A complete
PASS A size
PASS B complete
PASS B size
PASS B chores[0].name
PASS B chores[0].status
PASS B chores[1].name
PASS B chores[1].status
PASS C complete
PASS C size
PASS C chores[0].name
PASS C chores[0].status
PASS D complete
PASS D error
PASS D error_line
PASS E complete
PASS E error
PASS E error_line
PASS F complete
PASS F error
PASS F error_line
PASS G complete
PASS G error
PASS G error_line
PASS H complete
PASS H error
PASS H error_line
PASS I complete
PASS I error
PASS I error_line
PASS J complete
PASS J error
PASS J error_line
PASS K complete
PASS K size
PASS K chores[0].name
PASS K chores[0].status
PASS K chores[1].name
PASS K chores[1].status
PASS L complete
PASS L error
PASS L error_line
PASS M complete
PASS M error
PASS M error_line
Checks: 45, failed: 0
```

Exit code: 0.

- **`check_size`** has parameters of type `std::size_t`, so the size of the vector is compared without mixing it with `int`. It needs `#include <cstddef>`.
- **The elements only after a matching size.** `if (chores_b.size() == 2)` protects against reading an element that isn't there, if a version with a bug returned fewer records. In that case the size check already gives `FAIL`.
- **The order:** `chores[0]` and `chores[1]` are checked separately. In K both records have the same name, so the order shows in the statuses.
- **After an error** the program doesn't check the vector: the contract doesn't promise what is left in it. In H it already holds `Clean tables`. That the chore log program prints no partial report follows from `false`, and `complete` checks that.
- **Other correct solutions:** another split into checking functions, for example one function that checks a whole record, or other names for the checks. What matters is that every case has its own data, and every mismatch gives `FAIL` with the expected and the actual value.

**The old ending rule** (the fifth required run):

<!-- example: chore_tests_old_rule exit=1 -->
```cpp
#include <cstddef>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

struct Chore {
    std::string name;
    std::string status;
};

bool read_chores(std::istream& input, std::vector<Chore>& chores, std::string& error, int& error_line) {
    int line_number{0};
    std::string name{};
    std::getline(input, name);

    while (!input.fail() && !name.empty()) {
        ++line_number;

        std::string status{};
        std::getline(input, status);

        if (input.fail()) {
            error = "incomplete";
            error_line = line_number;
            return false;
        }

        ++line_number;

        if (status.empty()) {
            error = "empty";
            error_line = line_number;
            return false;
        }

        if (status != "done" && status != "pending") {
            error = "invalid";
            error_line = line_number;
            return false;
        }

        chores.push_back(Chore{name, status});
        std::getline(input, name);
    }

    return true;
}

std::string bool_text(bool value) {
    if (value) {
        return "true";
    }

    return "false";
}

void check_bool(const std::string& name, bool expected, bool actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << bool_text(expected) << ", actual " << bool_text(actual) << "\n";
        ++failed;
    }
}

void check_int(const std::string& name, int expected, int actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << expected << ", actual " << actual << "\n";
        ++failed;
    }
}

void check_size(const std::string& name, std::size_t expected, std::size_t actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << expected << ", actual " << actual << "\n";
        ++failed;
    }
}

void check_text(const std::string& name, const std::string& expected, const std::string& actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected \"" << expected << "\", actual \"" << actual << "\"\n";
        ++failed;
    }
}

int main() {
    int checks{0};
    int failed{0};

    std::istringstream input_a{""};
    std::vector<Chore> chores_a{};
    std::string error_a{};
    int error_line_a{0};
    const bool complete_a{read_chores(input_a, chores_a, error_a, error_line_a)};
    check_bool("A complete", true, complete_a, checks, failed);
    check_size("A size", 0, chores_a.size(), checks, failed);

    std::istringstream input_b{"Clean tables\ndone\nSort books\npending\n"};
    std::vector<Chore> chores_b{};
    std::string error_b{};
    int error_line_b{0};
    const bool complete_b{read_chores(input_b, chores_b, error_b, error_line_b)};
    check_bool("B complete", true, complete_b, checks, failed);
    check_size("B size", 2, chores_b.size(), checks, failed);

    if (chores_b.size() == 2) {
        check_text("B chores[0].name", "Clean tables", chores_b[0].name, checks, failed);
        check_text("B chores[0].status", "done", chores_b[0].status, checks, failed);
        check_text("B chores[1].name", "Sort books", chores_b[1].name, checks, failed);
        check_text("B chores[1].status", "pending", chores_b[1].status, checks, failed);
    }

    std::istringstream input_c{"Clean tables\ndone"};
    std::vector<Chore> chores_c{};
    std::string error_c{};
    int error_line_c{0};
    const bool complete_c{read_chores(input_c, chores_c, error_c, error_line_c)};
    check_bool("C complete", true, complete_c, checks, failed);
    check_size("C size", 1, chores_c.size(), checks, failed);

    if (chores_c.size() == 1) {
        check_text("C chores[0].name", "Clean tables", chores_c[0].name, checks, failed);
        check_text("C chores[0].status", "done", chores_c[0].status, checks, failed);
    }

    std::istringstream input_d{"\n"};
    std::vector<Chore> chores_d{};
    std::string error_d{};
    int error_line_d{0};
    const bool complete_d{read_chores(input_d, chores_d, error_d, error_line_d)};
    check_bool("D complete", false, complete_d, checks, failed);
    check_text("D error", "empty", error_d, checks, failed);
    check_int("D error_line", 1, error_line_d, checks, failed);

    std::istringstream input_e{"Clean tables\n\n"};
    std::vector<Chore> chores_e{};
    std::string error_e{};
    int error_line_e{0};
    const bool complete_e{read_chores(input_e, chores_e, error_e, error_line_e)};
    check_bool("E complete", false, complete_e, checks, failed);
    check_text("E error", "empty", error_e, checks, failed);
    check_int("E error_line", 2, error_line_e, checks, failed);

    std::istringstream input_f{"Clean tables\nlater\n"};
    std::vector<Chore> chores_f{};
    std::string error_f{};
    int error_line_f{0};
    const bool complete_f{read_chores(input_f, chores_f, error_f, error_line_f)};
    check_bool("F complete", false, complete_f, checks, failed);
    check_text("F error", "invalid", error_f, checks, failed);
    check_int("F error_line", 2, error_line_f, checks, failed);

    std::istringstream input_g{"Clean tables\n"};
    std::vector<Chore> chores_g{};
    std::string error_g{};
    int error_line_g{0};
    const bool complete_g{read_chores(input_g, chores_g, error_g, error_line_g)};
    check_bool("G complete", false, complete_g, checks, failed);
    check_text("G error", "incomplete", error_g, checks, failed);
    check_int("G error_line", 1, error_line_g, checks, failed);

    std::istringstream input_h{"Clean tables\ndone\n\n"};
    std::vector<Chore> chores_h{};
    std::string error_h{};
    int error_line_h{0};
    const bool complete_h{read_chores(input_h, chores_h, error_h, error_line_h)};
    check_bool("H complete", false, complete_h, checks, failed);
    check_text("H error", "empty", error_h, checks, failed);
    check_int("H error_line", 3, error_line_h, checks, failed);

    std::istringstream input_i{"Clean tables\ndone\nSort books\nlater\n"};
    std::vector<Chore> chores_i{};
    std::string error_i{};
    int error_line_i{0};
    const bool complete_i{read_chores(input_i, chores_i, error_i, error_line_i)};
    check_bool("I complete", false, complete_i, checks, failed);
    check_text("I error", "invalid", error_i, checks, failed);
    check_int("I error_line", 4, error_line_i, checks, failed);

    std::istringstream input_j{"Clean tables\ndone\nSort books"};
    std::vector<Chore> chores_j{};
    std::string error_j{};
    int error_line_j{0};
    const bool complete_j{read_chores(input_j, chores_j, error_j, error_line_j)};
    check_bool("J complete", false, complete_j, checks, failed);
    check_text("J error", "incomplete", error_j, checks, failed);
    check_int("J error_line", 3, error_line_j, checks, failed);

    std::istringstream input_k{"Clean tables\ndone\nClean tables\npending"};
    std::vector<Chore> chores_k{};
    std::string error_k{};
    int error_line_k{0};
    const bool complete_k{read_chores(input_k, chores_k, error_k, error_line_k)};
    check_bool("K complete", true, complete_k, checks, failed);
    check_size("K size", 2, chores_k.size(), checks, failed);

    if (chores_k.size() == 2) {
        check_text("K chores[0].name", "Clean tables", chores_k[0].name, checks, failed);
        check_text("K chores[0].status", "done", chores_k[0].status, checks, failed);
        check_text("K chores[1].name", "Clean tables", chores_k[1].name, checks, failed);
        check_text("K chores[1].status", "pending", chores_k[1].status, checks, failed);
    }

    std::istringstream input_l{"Clean tables\ndone \n"};
    std::vector<Chore> chores_l{};
    std::string error_l{};
    int error_line_l{0};
    const bool complete_l{read_chores(input_l, chores_l, error_l, error_line_l)};
    check_bool("L complete", false, complete_l, checks, failed);
    check_text("L error", "invalid", error_l, checks, failed);
    check_int("L error_line", 2, error_line_l, checks, failed);

    std::istringstream input_m{"Clean tables\nlater"};
    std::vector<Chore> chores_m{};
    std::string error_m{};
    int error_line_m{0};
    const bool complete_m{read_chores(input_m, chores_m, error_m, error_line_m)};
    check_bool("M complete", false, complete_m, checks, failed);
    check_text("M error", "invalid", error_m, checks, failed);
    check_int("M error_line", 2, error_line_m, checks, failed);

    std::cout << "Checks: " << checks << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

<!-- output: chore_tests_old_rule -->
```text
PASS A complete
PASS A size
PASS B complete
PASS B size
PASS B chores[0].name
PASS B chores[0].status
PASS B chores[1].name
PASS B chores[1].status
PASS C complete
PASS C size
PASS C chores[0].name
PASS C chores[0].status
FAIL D complete: expected false, actual true
FAIL D error: expected "empty", actual ""
FAIL D error_line: expected 1, actual 0
PASS E complete
PASS E error
PASS E error_line
PASS F complete
PASS F error
PASS F error_line
PASS G complete
PASS G error
PASS G error_line
FAIL H complete: expected false, actual true
FAIL H error: expected "empty", actual ""
FAIL H error_line: expected 3, actual 0
PASS I complete
PASS I error
PASS I error_line
PASS J complete
PASS J error
PASS J error_line
PASS K complete
PASS K size
PASS K chores[0].name
PASS K chores[0].status
PASS K chores[1].name
PASS K chores[1].status
PASS L complete
PASS L error
PASS L error_line
PASS M complete
PASS M error
PASS M error_line
Checks: 45, failed: 6
```

Exit code: 1.

**The counter raised before the status read is checked:** `++line_number;` stands right after `std::getline(input, status);`, before `if (input.fail())`. That's the mistake lesson 12.3, point 4, warned against.

<!-- example: chore_tests_counter_bug exit=1 -->
```cpp
#include <cstddef>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

struct Chore {
    std::string name;
    std::string status;
};

bool read_chores(std::istream& input, std::vector<Chore>& chores, std::string& error, int& error_line) {
    int line_number{0};
    std::string name{};
    std::getline(input, name);

    while (!input.fail()) {
        ++line_number;

        if (name.empty()) {
            error = "empty";
            error_line = line_number;
            return false;
        }

        std::string status{};
        std::getline(input, status);
        ++line_number;

        if (input.fail()) {
            error = "incomplete";
            error_line = line_number;
            return false;
        }

        if (status.empty()) {
            error = "empty";
            error_line = line_number;
            return false;
        }

        if (status != "done" && status != "pending") {
            error = "invalid";
            error_line = line_number;
            return false;
        }

        chores.push_back(Chore{name, status});
        std::getline(input, name);
    }

    return true;
}

std::string bool_text(bool value) {
    if (value) {
        return "true";
    }

    return "false";
}

void check_bool(const std::string& name, bool expected, bool actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << bool_text(expected) << ", actual " << bool_text(actual) << "\n";
        ++failed;
    }
}

void check_int(const std::string& name, int expected, int actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << expected << ", actual " << actual << "\n";
        ++failed;
    }
}

void check_size(const std::string& name, std::size_t expected, std::size_t actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << expected << ", actual " << actual << "\n";
        ++failed;
    }
}

void check_text(const std::string& name, const std::string& expected, const std::string& actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected \"" << expected << "\", actual \"" << actual << "\"\n";
        ++failed;
    }
}

int main() {
    int checks{0};
    int failed{0};

    std::istringstream input_a{""};
    std::vector<Chore> chores_a{};
    std::string error_a{};
    int error_line_a{0};
    const bool complete_a{read_chores(input_a, chores_a, error_a, error_line_a)};
    check_bool("A complete", true, complete_a, checks, failed);
    check_size("A size", 0, chores_a.size(), checks, failed);

    std::istringstream input_b{"Clean tables\ndone\nSort books\npending\n"};
    std::vector<Chore> chores_b{};
    std::string error_b{};
    int error_line_b{0};
    const bool complete_b{read_chores(input_b, chores_b, error_b, error_line_b)};
    check_bool("B complete", true, complete_b, checks, failed);
    check_size("B size", 2, chores_b.size(), checks, failed);

    if (chores_b.size() == 2) {
        check_text("B chores[0].name", "Clean tables", chores_b[0].name, checks, failed);
        check_text("B chores[0].status", "done", chores_b[0].status, checks, failed);
        check_text("B chores[1].name", "Sort books", chores_b[1].name, checks, failed);
        check_text("B chores[1].status", "pending", chores_b[1].status, checks, failed);
    }

    std::istringstream input_c{"Clean tables\ndone"};
    std::vector<Chore> chores_c{};
    std::string error_c{};
    int error_line_c{0};
    const bool complete_c{read_chores(input_c, chores_c, error_c, error_line_c)};
    check_bool("C complete", true, complete_c, checks, failed);
    check_size("C size", 1, chores_c.size(), checks, failed);

    if (chores_c.size() == 1) {
        check_text("C chores[0].name", "Clean tables", chores_c[0].name, checks, failed);
        check_text("C chores[0].status", "done", chores_c[0].status, checks, failed);
    }

    std::istringstream input_d{"\n"};
    std::vector<Chore> chores_d{};
    std::string error_d{};
    int error_line_d{0};
    const bool complete_d{read_chores(input_d, chores_d, error_d, error_line_d)};
    check_bool("D complete", false, complete_d, checks, failed);
    check_text("D error", "empty", error_d, checks, failed);
    check_int("D error_line", 1, error_line_d, checks, failed);

    std::istringstream input_e{"Clean tables\n\n"};
    std::vector<Chore> chores_e{};
    std::string error_e{};
    int error_line_e{0};
    const bool complete_e{read_chores(input_e, chores_e, error_e, error_line_e)};
    check_bool("E complete", false, complete_e, checks, failed);
    check_text("E error", "empty", error_e, checks, failed);
    check_int("E error_line", 2, error_line_e, checks, failed);

    std::istringstream input_f{"Clean tables\nlater\n"};
    std::vector<Chore> chores_f{};
    std::string error_f{};
    int error_line_f{0};
    const bool complete_f{read_chores(input_f, chores_f, error_f, error_line_f)};
    check_bool("F complete", false, complete_f, checks, failed);
    check_text("F error", "invalid", error_f, checks, failed);
    check_int("F error_line", 2, error_line_f, checks, failed);

    std::istringstream input_g{"Clean tables\n"};
    std::vector<Chore> chores_g{};
    std::string error_g{};
    int error_line_g{0};
    const bool complete_g{read_chores(input_g, chores_g, error_g, error_line_g)};
    check_bool("G complete", false, complete_g, checks, failed);
    check_text("G error", "incomplete", error_g, checks, failed);
    check_int("G error_line", 1, error_line_g, checks, failed);

    std::istringstream input_h{"Clean tables\ndone\n\n"};
    std::vector<Chore> chores_h{};
    std::string error_h{};
    int error_line_h{0};
    const bool complete_h{read_chores(input_h, chores_h, error_h, error_line_h)};
    check_bool("H complete", false, complete_h, checks, failed);
    check_text("H error", "empty", error_h, checks, failed);
    check_int("H error_line", 3, error_line_h, checks, failed);

    std::istringstream input_i{"Clean tables\ndone\nSort books\nlater\n"};
    std::vector<Chore> chores_i{};
    std::string error_i{};
    int error_line_i{0};
    const bool complete_i{read_chores(input_i, chores_i, error_i, error_line_i)};
    check_bool("I complete", false, complete_i, checks, failed);
    check_text("I error", "invalid", error_i, checks, failed);
    check_int("I error_line", 4, error_line_i, checks, failed);

    std::istringstream input_j{"Clean tables\ndone\nSort books"};
    std::vector<Chore> chores_j{};
    std::string error_j{};
    int error_line_j{0};
    const bool complete_j{read_chores(input_j, chores_j, error_j, error_line_j)};
    check_bool("J complete", false, complete_j, checks, failed);
    check_text("J error", "incomplete", error_j, checks, failed);
    check_int("J error_line", 3, error_line_j, checks, failed);

    std::istringstream input_k{"Clean tables\ndone\nClean tables\npending"};
    std::vector<Chore> chores_k{};
    std::string error_k{};
    int error_line_k{0};
    const bool complete_k{read_chores(input_k, chores_k, error_k, error_line_k)};
    check_bool("K complete", true, complete_k, checks, failed);
    check_size("K size", 2, chores_k.size(), checks, failed);

    if (chores_k.size() == 2) {
        check_text("K chores[0].name", "Clean tables", chores_k[0].name, checks, failed);
        check_text("K chores[0].status", "done", chores_k[0].status, checks, failed);
        check_text("K chores[1].name", "Clean tables", chores_k[1].name, checks, failed);
        check_text("K chores[1].status", "pending", chores_k[1].status, checks, failed);
    }

    std::istringstream input_l{"Clean tables\ndone \n"};
    std::vector<Chore> chores_l{};
    std::string error_l{};
    int error_line_l{0};
    const bool complete_l{read_chores(input_l, chores_l, error_l, error_line_l)};
    check_bool("L complete", false, complete_l, checks, failed);
    check_text("L error", "invalid", error_l, checks, failed);
    check_int("L error_line", 2, error_line_l, checks, failed);

    std::istringstream input_m{"Clean tables\nlater"};
    std::vector<Chore> chores_m{};
    std::string error_m{};
    int error_line_m{0};
    const bool complete_m{read_chores(input_m, chores_m, error_m, error_line_m)};
    check_bool("M complete", false, complete_m, checks, failed);
    check_text("M error", "invalid", error_m, checks, failed);
    check_int("M error_line", 2, error_line_m, checks, failed);

    std::cout << "Checks: " << checks << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }

    return 0;
}
```

<!-- output: chore_tests_counter_bug -->
```text
PASS A complete
PASS A size
PASS B complete
PASS B size
PASS B chores[0].name
PASS B chores[0].status
PASS B chores[1].name
PASS B chores[1].status
PASS C complete
PASS C size
PASS C chores[0].name
PASS C chores[0].status
PASS D complete
PASS D error
PASS D error_line
PASS E complete
PASS E error
PASS E error_line
PASS F complete
PASS F error
PASS F error_line
PASS G complete
PASS G error
FAIL G error_line: expected 1, actual 2
PASS H complete
PASS H error
PASS H error_line
PASS I complete
PASS I error
PASS I error_line
PASS J complete
PASS J error
FAIL J error_line: expected 3, actual 4
PASS K complete
PASS K size
PASS K chores[0].name
PASS K chores[0].status
PASS K chores[1].name
PASS K chores[1].status
PASS L complete
PASS L error
PASS L error_line
PASS M complete
PASS M error
PASS M error_line
Checks: 45, failed: 2
```

Exit code: 1.

| Bug | Revealing cases | Checks with `FAIL` | Failures | Code |
|---|---|---|---|---|
| the old ending rule | D, H | `complete`, `error`, `error_line` in both | 6 | 1 |
| the counter before the status read is checked | G, J | only `error_line` in both | 2 | 1 |

- **The old rule** changes the result only when an empty line stands in place of a name: D at the start of the data, H after a complete record. E has an empty line in place of the status, and the function still detects that one.
- **The counter** changes the result only for an incomplete record, because only then does reading the status fail. In G and J, `complete` and `error` give `PASS`: only the check of the line number tells this version apart from the correct one. A test that didn't check `error_line` wouldn't detect this bug.
- **A and D:** an empty text is a correct end of the data, and one empty line is an error. If the suite had only A, the old rule would pass.
- Each program with a bug ends with code 1, because the failure counter is greater than zero, and with the correct function the same suite gives code 0.

**Example justifications for step 6:**

- **C** would detect a function that checks `eof()` instead of `fail()` after reading the status: it would treat the last status without a line end as missing.
- **D** detects the old ending rule: an empty line in place of the first name would end the data without an error.
- **H** detects the same rule after a complete record, that is, the situation of lesson 12.3 in which part of the data disappeared without a message.
- **J** detects a counter raised after a failed read: the number would point to line 4, which isn't in the data.

</details>

**Previous lesson:** [Lesson 13.2: Test cases that catch bugs](lesson_02_test_cases_that_catch_bugs.en.md) · **Next lesson:** in preparation · [Course overview](../../README.en.md)

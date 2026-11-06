# Lesson 12.4: Cinema screenings (the Module 12 test)

[Polski](lesson_04_cinema_screenings.md) · **English** · [Course overview](../../README.en.md)

> **Module 12, lesson 4: the test** · about 100–120 minutes, in two sessions
> **You need:** your `cpp-workspace` folder and the original `lesson_05_first_program` project.
> **Pilot version.** The reference solution and the diagnostic's program are checked automatically on Windows, Ubuntu and macOS, with the given data files. Nothing grades your project automatically: you check it yourself, against the checklist. The steps in CLion (a new file, the **Working directory** field) are the same as in lessons 12.1–12.3: they are described according to the CLion 2026.3 documentation, without a manual check on every system.

## How this test works

This lesson introduces nothing new. You check whether you can **design, write and test on your own a program that reads a text file**, checks its records, points to the number of a bad line, and makes a report only after the whole file has been processed correctly. In it you combine lessons 12.1–12.3.

The test has three parts and a review:

- **Part A: the plan.** A short plan of the data, the reading and the responsibilities, before you write code.
- **Part B: implementation and tests.** The program, written to the specification and checked with the control cases. This is the largest part of the work.
- **Part C: diagnostic and justification.** An error in line numbering, and questions about your decisions. Do it after Part B.
- **Checking and review:** hints, the full list of cases, the reference solution, the diagnostic's explanation, answers and a self-assessment. Go there only after Parts A and B, or when you consciously give up further work on your own.

Looking at a hint or at an earlier lesson isn't a failure. What matters is to **note honestly what was done independently and what with help**. A suggested split into two sessions:

- **first:** the specification, Part A, the project in CLion, the record type, the reading function and case A;
- **second:** the full check of the data, the line numbers, the report, the control cases, Part C and the self-assessment.

**You may use:** CLion or the terminal, CMake and Ninja, as before; `CMakeLists.txt` copied from the original `lesson_05_first_program`; lessons 12.1–12.3 as reminders; the case tables. You won't need the debugger. You know everything you need from Modules 1–12.

---

## Specification: cinema screenings

A small cinema records the day's programme in a file: a film's title and the state of its screening. The program reads this file and prints all the screenings, and how many of them have free seats, how many are sold out and how many are cancelled. It doesn't model times, rooms, prices or tickets.

**Preparation:** in `cpp-workspace`, create a folder `cinema_screenings` and copy `CMakeLists.txt` from the original `lesson_05_first_program` into it. Next to it, create `main.cpp` and the data file `screenings.txt`, as in lesson 12.1, section 3. Leave `CMakeLists.txt` unchanged: `screenings.txt` is data that the running program reads, not a file to compile, so don't add it to `add_executable`. Open the folder in CLion and check the **Working directory** field of the `first_program` configuration, as in lesson 12.1, section 4. The file being next to `main.cpp` isn't enough on its own: the program looks for it in its working directory.

```text
cinema_screenings/
├── CMakeLists.txt
├── main.cpp
└── screenings.txt
```

### The file `screenings.txt`

The file holds zero or more records. Each record takes exactly two physical lines:

1. the film's title;
2. the screening's status: `available` (there are free seats), `full` (the screening is sold out) or `cancelled` (the screening is cancelled).

**The rules:**

- A title isn't an empty line, may contain spaces and may repeat: each occurrence is a separate screening. The program keeps the title exactly, with all its characters, spaces at the start and at the end included. A line of spaces only isn't empty, so it's a valid title.
- A status has exactly one of the three forms. The case of letters matters and there are no extra spaces: `Available`, `FULL`, `Canceled` and `available ` with a space at the end are invalid.
- The number of screenings isn't limited. An empty file, that is, a file without any character, is valid and means zero screenings.
- The data are ASCII text, and the character `\n` ends the lines.

### The end of the data and errors

- **Only the end of the file ends the data,** at the place where the next record would start. An empty line isn't an end marker.
- The last line may have no line end: that isn't an error. A line end after the last status doesn't create an extra, empty line. Only a second line end in a row creates one.
- Lines are numbered from 1, as in an editor. N in the messages is always the number of a physical line of the file.

| Situation | Standard output |
|---|---|
| the file couldn't be opened | `Cannot open screenings.txt` |
| an empty line: before the first record, where a title or a status is expected, between records, or at the end of the file | `Empty line N`, where N is the number of that empty line |
| a non-empty status other than `available`, `full` and `cancelled` | `Invalid line N`, where N is the number of the status line |
| the file ends right after a title, with no status line | `Incomplete record on line N`, where N is the number of that title's line |

- The program checks the records in order, from the start of the file, and reports the **first** error. For each line it first checks whether the line could be read, then whether it's empty, and only at the end whether the status is allowed. So an empty status is `Empty line N`, not `Invalid line N`.
- After an error the program prints only that one message, with no part of the report, and ends with exit code 0. It prints nothing to `std::cerr`.

### The report

When the whole file is valid, the program prints:

```text
Screenings: N
TITLE: STATUS
Available total: A
Full total: F
Cancelled total: C
```

- The line `TITLE: STATUS` repeats for each screening, in the order of the file: the title, a colon, a space and the status, for example `Morning Birds: available`.
- `N` is the number of all the screenings, and `A`, `F` and `C` are the numbers of screenings with the status `available`, `full` and `cancelled`. Each screening counts in exactly one of the three totals, so together they give `N`.
- The program doesn't sort the screenings, remove repeats or add numbers. It prints the report only after checking the whole file. An example report is case A in Part B.

### The required structure

- **A record type** (`struct`) with a title and a status, and **a vector** of records in the order of the file.
- **A reading function** that gets the stream through `std::istream&` and reads the whole file from it: every line with `std::getline`, with a counter of physical lines. It recognises the end of the data and the errors, and passes the kind of the first error and its line number to the calling code. It doesn't open the file, doesn't use `std::cin` and prints nothing. The same function could be called with `std::cin` instead of an open file, with no change to its body, although your program reads only `screenings.txt`.
- **`main`** opens `screenings.txt`, checks the opening, calls the reading function, and prints either one message or the full report. The report with the three totals is made only when the reading function has read the whole file without an error.
- You don't read the fields of a record with `>>`, and you don't control the loop with `eof()`. `fail()` after a read decides whether a line has been read.
- One `main.cpp` file is enough. You may split the program into several files, as in Module 11, but it isn't required and earns no extra points.

**Decide on your own:**

1. how to name the record type, its fields and the vector;
2. which functions the program has and how to name them;
3. which parameters the reading function has and what it returns;
4. how the reading function passes the kind of error and the line number;
5. where the line counter starts and when it grows;
6. how the program recognises a valid end of the data, and how an incomplete record;
7. how it checks whether a status is allowed;
8. where and how it computes the three totals;
9. how it prevents a partial report;
10. which data files it is tested with.

Reminders are in lessons [12.1](lesson_01_first_data_file.en.md) (a data file, the working directory, a failed open), [12.2](lesson_02_records_from_a_file.en.md) (a reading function with `std::istream&`) and [12.3](lesson_03_end_of_data_and_errors.en.md) (the end of the file, empty lines, line numbers).

---

# Part A: the plan

Before you write code, prepare a short plan in writing. A few sentences or a table are enough. The plan answers ten questions:

1. What does one screening look like in the program?
2. What does the program keep the list of screenings in?
3. Where does the program open `screenings.txt`?
4. Which function reads the records?
5. How does that function get the stream?
6. How does the program tell a valid end of the data from an error?
7. How does the program number the lines?
8. How does the reading function pass the kind of error and the line number?
9. Where does the program compute the three totals?
10. When does the program print the report?

Answer briefly too:

1. Why does the reading function take `std::istream&`?
2. Why shouldn't opening an `std::ifstream` be hidden inside a reading function that can be used with different streams?
3. How does the end of the file differ from an empty line?
4. Why does the line counter grow only after a successful `std::getline`?
5. Why is the report made only after the whole file has been checked?

The plan is a required part of the test and is assessed together with the program.

---

# Part B: implementation and tests

Write the program to the specification and your plan. **Before running it**, prepare a table of cases: the file's contents and the predicted result. The results below follow directly from the specification. Each case is different contents of `screenings.txt`, or no file. You don't build the program again.

**A: three valid screenings.**

<!-- run: screenings -->

<!-- datafile: screenings screenings.txt -->
```text
Morning Birds
available
Northern Lights
full
Evening Stories
cancelled
```

<!-- output: screenings -->
```text
Screenings: 3
Morning Birds: available
Northern Lights: full
Evening Stories: cancelled
Available total: 1
Full total: 1
Cancelled total: 1
```

**B: an empty file.** The file exists, but there isn't a single character in it.

<!-- run: screenings -->

<!-- datafile: screenings screenings.txt -->
```text
```

<!-- output: screenings -->
```text
Screenings: 0
Available total: 0
Full total: 0
Cancelled total: 0
```

**C: no file.** There's no `screenings.txt` in the working directory.

<!-- run: screenings -->

<!-- output: screenings -->
```text
Cannot open screenings.txt
```

**D: a single empty line.** The file holds just one line end.

<!-- run: screenings -->

<!-- datafile: screenings screenings.txt -->
```text

```

<!-- output: screenings -->
```text
Empty line 1
```

**E: an empty status.** The file is `Morning Birds\n\n`.

<!-- run: screenings -->

<!-- datafile: screenings screenings.txt -->
```text
Morning Birds

```

<!-- output: screenings -->
```text
Empty line 2
```

**F: no status.** The file is `Morning Birds\n`, so only the title line exists.

<!-- run: screenings -->

<!-- datafile: screenings screenings.txt -->
```text
Morning Birds
```

<!-- output: screenings -->
```text
Incomplete record on line 1
```

**H: the last status without a line end.** The file is exactly `Morning Birds\navailable`. You don't have to prepare such a file: the course's tests check it automatically.

<!-- run: screenings -->

<!-- datafile: screenings screenings.txt noeol -->
```text
Morning Birds
available
```

<!-- output: screenings -->
```text
Screenings: 1
Morning Birds: available
Available total: 1
Full total: 0
Cancelled total: 0
```

**M: an invalid status of the second screening.** The first screening was valid, but there's no partial report.

<!-- run: screenings -->

<!-- datafile: screenings screenings.txt -->
```text
Morning Birds
available
Evening Stories
unknown
```

<!-- output: screenings -->
```text
Invalid line 4
```

The other cases, G and I–T, are in the full list in "Checking and review". They follow from the same specification: none of them has a new rule.

**Run as required**, changing only the contents or the name of `screenings.txt`:

1. A;
2. C: rename the file, for example to `screenings_old.txt`, run the program, and restore the name;
3. D or E;
4. M;
5. F, and then do Part C.

Predict the other cases in your table and compare them with the full list. All of them are checked automatically for the reference solution.

---

# Part C: diagnostic and justification

Do this part **after Part B**.

## Diagnostic: the number of a line that doesn't exist

Someone wrote a program that should point to the line of an incomplete record. When reading the status, though, the line counter grows right after `std::getline`, before the program checks whether the read succeeded:

<!-- fragment -->
```cpp
std::getline(input, status);
++line_number;

if (input.fail()) {
    error = "incomplete";
    error_line = line_number;
    return false;
}
```

The title has already been read correctly and has number 1, and the file is `Morning Birds\n`, as in case F.

1. Predict which number this program prints for F.
2. Explain why that number is wrong.
3. Point to the line of code that causes the problem.
4. Suggest the smallest fix.
5. Check that your program prints `Incomplete record on line 1` for F. This is the fifth required run of Part B. If you like, put the same error into your program, run it for F, and restore the correct order.
6. Explain why a missing status shouldn't grow the counter of physical lines.
7. For which cases of Part B does this error change the result, and for which doesn't it? What follows from that for testing?

## Justification

Answer in your own words, referring to your program:

1. Why does your reading function take `std::istream&`, and not `std::ifstream` by value?
2. Why is an empty file valid?
3. Why doesn't an empty line end the data?
4. When does your program grow the line counter?
5. Why does the program point to the title's line for an incomplete record?
6. Why do the three totals together give the number of screenings?
7. Why is there no partial report after an error, and what in your program ensures it?
8. What role does the program's working directory play?
9. How could the same reading function be used for data from `std::cin`?

---

## Checklist before you hand in

The test is passed when you meet **all** the items of this list. Your split into functions and files may differ from the reference solution, as long as it meets the specification. A correct result for case A alone isn't enough.

- [ ] The plan of Part A was made before the code and matches the program.
- [ ] The program opens `screenings.txt`, checks the opening, and prints `Cannot open screenings.txt` when opening fails.
- [ ] The records are read by a function that gets the stream through `std::istream&`, opens no file, doesn't use `std::cin` and prints nothing.
- [ ] Both lines of a record are read with `std::getline`, without `>>`.
- [ ] The program tells the end of the file from an empty line: an empty file gives a report with no screenings, and every empty line gives `Empty line N`.
- [ ] The counter grows only after a successful `std::getline`, and the numbers in the messages are numbers of physical lines.
- [ ] The program recognises an empty line, a status that isn't allowed and an incomplete record, in the order of checks from the specification.
- [ ] The program reports only the first error, and prints no part of the report after it.
- [ ] The report keeps all the screenings, their order and repeated titles, with the titles unchanged.
- [ ] The three totals are correct and together give the number of screenings.
- [ ] The report and the messages match the specification character for character.
- [ ] The required runs (A, C, D or E, M and F) give the shown results, and the predictions for the other cases match the full list.
- [ ] Part C is done: the counter error is explained, and the fix is pointed out and checked for F.
- [ ] You can explain your decisions: the answers of the justification refer to your program.

When you're done, you can save the project in Git, as in lesson 1.5: `main.cpp`, `CMakeLists.txt` and `screenings.txt` with data A, without the build folder. An ordinary data file belongs to the project and can be tracked together with the code.

## Assessment criteria

The rubric is for self-assessment or for assessment by a teacher. The course has no grading scale and no points threshold: the points show which areas are mastered and which need revision. The checklist above decides whether the test is passed, not the number of points.

| Area | Points | Full points when |
|---|---:|---|
| The plan and the split of responsibilities | 10 | the plan was made before the code, answers the ten questions and the five short questions, and the program matches it |
| Preparing the project and handling the file | 15 | `CMakeLists.txt` is the canonical one and doesn't list the data file, **Working directory** points to the folder with `screenings.txt`, `main` checks the opening before reading, and a missing file gives the exact message |
| A reading function that takes `std::istream&` | 15 | all the reading is in a function with an `std::istream&` parameter, which opens no file, doesn't use `std::cin` and prints nothing, and the answer about using it with `std::cin` is correct |
| EOF, empty lines and numbering | 20 | a failed read of a title recognises the end of the data, every empty line gives `Empty line N`, the counter grows only after a successful `std::getline`, and the numbers are correct for F, G and O too |
| Validation, errors and no partial report | 15 | the three kinds of error are recognised in the order of the specification, the messages are exact, the program reports only the first error, and prints no part of the report after it |
| Records and the report with three totals | 10 | the screenings are in the order of the file, with repeats and unchanged titles, and the three totals are correct and together give the number of screenings |
| Tests, diagnostic and justification | 15 | the table of cases was made before running, the required runs give the shown results, the counter error of Part C is explained and fixed, and the answers refer to the project |
| **Total** | **100** | |

- **A correct result doesn't automatically give all the points:** the plan, the reading function and the structure are assessed by reading the program.
- **Reading without a function with `std::istream&`**, for example all of it in `main`, or in a function that opens the file itself, gets no points for the reading function, even with a good result.
- **A partial report after an error** breaks the specification: it means no points for validation and errors.
- **A good result for A with wrong numbers for F, G or O** doesn't give full points for numbering.
- **Other names** and another, justified split into functions don't cost points. A split into several files earns no extra points, and a single `main.cpp` costs none.

**What is checked automatically, and what isn't.** The course's tests check that the reference solution and the diagnostic's program build and give the shown results. Your runs of the control cases check how your program behaves for those data. **No automatic check looks at your code, your plan or your justification:** a person assesses them by reading the plan and the program.

---

# Checking and review

Come here **only after Parts A and B**, or when you consciously give up further work on your own. Below is the solution's code.

## Hints

<details>
<summary>Hint 1: the data and the functions</summary>

Which actions depend on the contents of the file, and which only on a finished list of screenings? Reading and checking concern every line of the file, in order. The report and the totals need only the list of valid screenings. What of this should the reading function know, and what `main`?

</details>

<details>
<summary>Hint 2: the end of the file and errors</summary>

Tell apart four situations: a failed read of a title; a successful read of an empty line; a failed read of a status after a title; a successful read of a non-empty status that isn't allowed. Which of them is the only valid end of the list, and which means an incomplete record?

</details>

<details>
<summary>Hint 3: numbering and the report</summary>

The line counter says how many lines have been read so far: it grows after every successful `std::getline`, also after a status, and doesn't grow after a failed one. The reading function can write the kind of error and the line number into variables passed by reference, as in lesson 12.3. Compute the totals and the report only when the function has ended with success.

</details>

## The full list of control cases

<details>
<summary>Cases G and I–T, checked automatically for the reference solution</summary>

**G: no status, without a line end.** The file is exactly `Morning Birds`.

<!-- run: screenings -->

<!-- datafile: screenings screenings.txt noeol -->
```text
Morning Birds
```

<!-- output: screenings -->
```text
Incomplete record on line 1
```

**I: an empty line at the end.** The file is `Morning Birds\navailable\n\n`: the second line end creates line 3, an empty one.

<!-- run: screenings -->

<!-- datafile: screenings screenings.txt -->
```text
Morning Birds
available

```

<!-- output: screenings -->
```text
Empty line 3
```

**J: an unknown status.**

<!-- run: screenings -->

<!-- datafile: screenings screenings.txt -->
```text
Morning Birds
postponed
```

<!-- output: screenings -->
```text
Invalid line 2
```

**K: a capital letter in the status.**

<!-- run: screenings -->

<!-- datafile: screenings screenings.txt -->
```text
Morning Birds
Available
```

<!-- output: screenings -->
```text
Invalid line 2
```

**L: a space after the status.** The second line holds `full` and one space.

<!-- run: screenings -->

<!-- datafile: screenings screenings.txt -->
```text
Morning Birds
full 
```

<!-- output: screenings -->
```text
Invalid line 2
```

**N: an empty line between screenings.** More data follow it, but the reading doesn't end after the first screening.

<!-- run: screenings -->

<!-- datafile: screenings screenings.txt -->
```text
Morning Birds
available

Evening Stories
full
```

<!-- output: screenings -->
```text
Empty line 3
```

**O: an incomplete second record.**

<!-- run: screenings -->

<!-- datafile: screenings screenings.txt -->
```text
Morning Birds
available
Evening Stories
```

<!-- output: screenings -->
```text
Incomplete record on line 3
```

**P: the same title twice.** Each occurrence is a separate screening.

<!-- run: screenings -->

<!-- datafile: screenings screenings.txt -->
```text
Morning Birds
available
Morning Birds
full
```

<!-- output: screenings -->
```text
Screenings: 2
Morning Birds: available
Morning Birds: full
Available total: 1
Full total: 1
Cancelled total: 0
```

**Q: five screenings,** two `available`, two `full` and one `cancelled`.

<!-- run: screenings -->

<!-- datafile: screenings screenings.txt -->
```text
Morning Birds
available
Northern Lights
full
Evening Stories
cancelled
Harbour Lights
available
Silent River
full
```

<!-- output: screenings -->
```text
Screenings: 5
Morning Birds: available
Northern Lights: full
Evening Stories: cancelled
Harbour Lights: available
Silent River: full
Available total: 2
Full total: 2
Cancelled total: 1
```

**R: a title with spaces.**

<!-- run: screenings -->

<!-- datafile: screenings screenings.txt -->
```text
The Last Morning Show
cancelled
```

<!-- output: screenings -->
```text
Screenings: 1
The Last Morning Show: cancelled
Available total: 0
Full total: 0
Cancelled total: 1
```

**S: a title of spaces only.** The first line holds three spaces. That isn't an empty line, so the report keeps those spaces before the colon.

<!-- run: screenings -->

<!-- datafile: screenings screenings.txt -->
```text
   
available
```

<!-- output: screenings -->
```text
Screenings: 1
   : available
Available total: 1
Full total: 0
Cancelled total: 0
```

**T: several errors in one file.** The first is an invalid status on line 2. An empty line and the status `Full` follow, but the program reports only the first error.

<!-- run: screenings -->

<!-- datafile: screenings screenings.txt -->
```text
Morning Birds
postponed

Evening Stories
Full
```

<!-- output: screenings -->
```text
Invalid line 2
```

| Case | The file `screenings.txt` | Standard output |
|---|---|---|
| A | three screenings, one with each status | 3 screenings, totals 1, 1 and 1 |
| B | an empty file | `Screenings: 0` and three zeros |
| C | no file | `Cannot open screenings.txt` |
| D | a single empty line | `Empty line 1` |
| E | `Morning Birds`, an empty line | `Empty line 2` |
| F | `Morning Birds` with a line end | `Incomplete record on line 1` |
| G | `Morning Birds` without a line end | `Incomplete record on line 1` |
| H | `Morning Birds`, `available` without a line end | 1 screening, totals 1, 0 and 0 |
| I | `Morning Birds`, `available`, an empty line | `Empty line 3` |
| J | `Morning Birds`, `postponed` | `Invalid line 2` |
| K | `Morning Birds`, `Available` | `Invalid line 2` |
| L | `Morning Birds`, `full` with a space | `Invalid line 2` |
| M | the second screening with the status `unknown` | `Invalid line 4` |
| N | an empty line between screenings | `Empty line 3` |
| O | the second title without a status | `Incomplete record on line 3` |
| P | the same title with two statuses | 2 screenings, totals 1, 1 and 0 |
| Q | five screenings | 5 screenings, totals 2, 2 and 1 |
| R | `The Last Morning Show`, `cancelled` | 1 screening, totals 0, 0 and 1 |
| S | three spaces, `available` | 1 screening, with a title of three spaces |
| T | `postponed` on line 2, more errors after it | `Invalid line 2` |

</details>

## The reference solution

<details>
<summary>The plan and the program of the reference solution</summary>

This is one of the correct solutions, not the only acceptable structure.

| Part of the program | Responsibility | Input | Result |
|---|---|---|---|
| `struct Screening` | one screening | — | the title and the status as `std::string` |
| `is_allowed_status` | checking a status | the status text | `true` or `false` |
| `read_screenings` | reading and checking the whole file | a stream through `std::istream&` and an empty vector | `true` and a filled vector, or `false` with the kind of error and the line number |
| `print_report` | the report and the three totals | the vector of screenings through `const&` | the report lines on standard output |
| `main` | opening the file, calling the reading, a message or the report | `screenings.txt` | standard output |

**`main.cpp`**:

<!-- example: screenings -->
```cpp
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

struct Screening {
    std::string title;
    std::string status;
};

bool is_allowed_status(const std::string& status) {
    return status == "available" || status == "full" || status == "cancelled";
}

bool read_screenings(std::istream& input, std::vector<Screening>& screenings, std::string& error, int& error_line) {
    int line_number{0};
    std::string title{};
    std::getline(input, title);

    while (!input.fail()) {
        ++line_number;

        if (title.empty()) {
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

        if (!is_allowed_status(status)) {
            error = "invalid";
            error_line = line_number;
            return false;
        }

        screenings.push_back(Screening{title, status});
        std::getline(input, title);
    }

    return true;
}

void print_report(const std::vector<Screening>& screenings) {
    int available_total{0};
    int full_total{0};
    int cancelled_total{0};
    std::cout << "Screenings: " << screenings.size() << "\n";

    for (const Screening& screening : screenings) {
        std::cout << screening.title << ": " << screening.status << "\n";

        if (screening.status == "available") {
            ++available_total;
        } else if (screening.status == "full") {
            ++full_total;
        } else {
            ++cancelled_total;
        }
    }

    std::cout << "Available total: " << available_total << "\n";
    std::cout << "Full total: " << full_total << "\n";
    std::cout << "Cancelled total: " << cancelled_total << "\n";
}

int main() {
    std::ifstream screenings_file{"screenings.txt"};

    if (screenings_file.fail()) {
        std::cout << "Cannot open screenings.txt\n";
        return 0;
    }

    std::vector<Screening> screenings{};
    std::string error{};
    int error_line{0};
    const bool complete{read_screenings(screenings_file, screenings, error, error_line)};

    if (!complete) {
        if (error == "empty") {
            std::cout << "Empty line " << error_line << "\n";
        } else if (error == "invalid") {
            std::cout << "Invalid line " << error_line << "\n";
        } else {
            std::cout << "Incomplete record on line " << error_line << "\n";
        }

        return 0;
    }

    print_report(screenings);
}
```

**`CMakeLists.txt`**: the one of the original `lesson_05_first_program`, unchanged. `screenings.txt` isn't in `add_executable`.

**`screenings.txt`** with data A, in the folder `cinema_screenings`, next to `main.cpp` and `CMakeLists.txt`:

<!-- run: screenings -->

<!-- datafile: screenings screenings.txt -->
```text
Morning Birds
available
Northern Lights
full
Evening Stories
cancelled
```

<!-- output: screenings -->
```text
Screenings: 3
Morning Birds: available
Northern Lights: full
Evening Stories: cancelled
Available total: 1
Full total: 1
Cancelled total: 1
```

- **Running it:** the **Working directory** field of the `first_program` configuration points to the folder `cinema_screenings`, the one with `screenings.txt`. In the terminal you run the program from the folder `cinema_screenings`.
- **The reading function:** `read_screenings` gets the stream through `std::istream&`, and the vector, the kind of error and the line number through references without `const`. It opens no file and prints nothing. With `std::cin` the call would be `read_screenings(std::cin, screenings, error, error_line)`, with no change to the function.
- **The order of the checks:** first `fail()` after each `std::getline`, then `empty()`, and for a status `is_allowed_status` at the end. So an empty status gives `Empty line N`, not `Invalid line N`.
- **The numbering:** `line_number` grows once after a successful read of a title, at the start of the loop, and once after a successful read of the status. After a failed read of the status it doesn't grow, so `Incomplete record` gives the title's line.
- **The end of the file and no final line end:** only a failed read of a title ends the loop. A last line without a line end is an ordinary, successful read and needs no code of its own.
- **The totals:** `print_report` goes through the vector once. Each screening grows exactly one counter: `if`, `else if` and `else`. The `else` branch covers `cancelled`, because only screenings with an allowed status get into the vector.
- **No partial report:** `main` calls `print_report` only after `true`. After `false` the vector may hold earlier screenings, but nothing from it is printed.
- **Other correct solutions:** other names; checking the status directly in a condition instead of a separate function; the totals computed in a separate function or in `main`; a loop with a `bool` flag, as in lesson 7.4; the type and the declarations in your own header, and the functions in separate `.cpp` files, as in Module 11. What matters is that the counter grows only after a successful read, and that the report is made only at the end.

</details>

## Diagnostic: explanation and fix

<details>
<summary>Open after doing the diagnostic</summary>

The whole program with the error is the reference solution with one line moved: `++line_number;` stands right after the status is read. Its results are checked automatically.

<!-- example: screenings_counter_bug -->
```cpp
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

struct Screening {
    std::string title;
    std::string status;
};

bool is_allowed_status(const std::string& status) {
    return status == "available" || status == "full" || status == "cancelled";
}

bool read_screenings(std::istream& input, std::vector<Screening>& screenings, std::string& error, int& error_line) {
    int line_number{0};
    std::string title{};
    std::getline(input, title);

    while (!input.fail()) {
        ++line_number;

        if (title.empty()) {
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

        if (!is_allowed_status(status)) {
            error = "invalid";
            error_line = line_number;
            return false;
        }

        screenings.push_back(Screening{title, status});
        std::getline(input, title);
    }

    return true;
}

void print_report(const std::vector<Screening>& screenings) {
    int available_total{0};
    int full_total{0};
    int cancelled_total{0};
    std::cout << "Screenings: " << screenings.size() << "\n";

    for (const Screening& screening : screenings) {
        std::cout << screening.title << ": " << screening.status << "\n";

        if (screening.status == "available") {
            ++available_total;
        } else if (screening.status == "full") {
            ++full_total;
        } else {
            ++cancelled_total;
        }
    }

    std::cout << "Available total: " << available_total << "\n";
    std::cout << "Full total: " << full_total << "\n";
    std::cout << "Cancelled total: " << cancelled_total << "\n";
}

int main() {
    std::ifstream screenings_file{"screenings.txt"};

    if (screenings_file.fail()) {
        std::cout << "Cannot open screenings.txt\n";
        return 0;
    }

    std::vector<Screening> screenings{};
    std::string error{};
    int error_line{0};
    const bool complete{read_screenings(screenings_file, screenings, error, error_line)};

    if (!complete) {
        if (error == "empty") {
            std::cout << "Empty line " << error_line << "\n";
        } else if (error == "invalid") {
            std::cout << "Invalid line " << error_line << "\n";
        } else {
            std::cout << "Incomplete record on line " << error_line << "\n";
        }

        return 0;
    }

    print_report(screenings);
}
```

For F:

<!-- run: screenings_counter_bug -->

<!-- datafile: screenings_counter_bug screenings.txt -->
```text
Morning Birds
```

<!-- output: screenings_counter_bug -->
```text
Incomplete record on line 2
```

For G, the same title without a line end:

<!-- run: screenings_counter_bug -->

<!-- datafile: screenings_counter_bug screenings.txt noeol -->
```text
Morning Birds
```

<!-- output: screenings_counter_bug -->
```text
Incomplete record on line 2
```

For O, where the status of the second screening is missing:

<!-- run: screenings_counter_bug -->

<!-- datafile: screenings_counter_bug screenings.txt -->
```text
Morning Birds
available
Evening Stories
```

<!-- output: screenings_counter_bug -->
```text
Incomplete record on line 4
```

For A, a valid file:

<!-- run: screenings_counter_bug -->

<!-- datafile: screenings_counter_bug screenings.txt -->
```text
Morning Birds
available
Northern Lights
full
Evening Stories
cancelled
```

<!-- output: screenings_counter_bug -->
```text
Screenings: 3
Morning Birds: available
Northern Lights: full
Evening Stories: cancelled
Available total: 1
Full total: 1
Cancelled total: 1
```

1. **The program prints `Incomplete record on line 2`.** Reading the status fails, but the counter has already grown from 1 to 2.
2. **That number is wrong,** because the file has only one line. There's no line 2, so it can't be corrected. The record started on line 1, and that's the line after which the status must be added.
3. **The problem is caused by `++line_number;` right after `std::getline(input, status);`,** before `input.fail()` is checked.
4. **The smallest fix:** move `++line_number;` after the `if (input.fail())` block:

<!-- fragment -->
```cpp
std::getline(input, status);

if (input.fail()) {
    error = "incomplete";
    error_line = line_number;
    return false;
}

++line_number;
```

5. **After the fix** the program prints `Incomplete record on line 1` for F, like the reference solution in Part B.
6. **The counter counts lines that exist in the file.** A failed read delivers no line, so there's nothing to count. A counter grown anyway points to a line that doesn't exist.
7. **The error changes the result only for an incomplete record:** in Part B for F, and in the full list also for G (`line 2`) and O (`line 4`, although the file has three lines). After a successful read of a status the counter grows once in both versions, so for A, M and the other cases the result is the same. That's why case A alone doesn't reveal this error: the tests must also include bad cases, and among them every kind of error.

</details>

## Answers to the questions of Part C

<details>
<summary>Example answers, for the reference solution</summary>

1. Because the function should read from any input stream: from an open file and from `std::cin`. An `std::ifstream` by value would tie it to a file, and a stream may not be copied anyway (lesson 12.2). A reference lets it read from the same stream that `main` prepared.
2. Because the specification allows zero records. The first read of a title fails where a record would start, and that's a valid end of the data. An empty file contains no line, so it doesn't contain an empty line either.
3. Because the empty line is in the file: `std::getline` reads it, `fail()` gives `false`, and more screenings may follow it. Only a failed read of a title ends the data. If an empty line ended the data, the screenings after it would disappear with no message.
4. After every successful `std::getline`: once after the title and once after the status. Never after a failed read.
5. Because the status line isn't in the file, and the record started on the title's line. That's the last line that exists, and the status must be added after it.
6. Because only screenings with one of the three allowed statuses get into the vector, and each screening grows exactly one counter: `if`, `else if` and `else`.
7. Because a partial report would look like a full one, although part of the file is wrong or unread. `main` calls `print_report` only when `read_screenings` returns `true`.
8. The program opens `screenings.txt` by a relative path, so it looks for the file in its working directory, not next to `main.cpp`. In CLion the **Working directory** field sets it, and in the terminal it's the folder you run the program from (lesson 12.1).
9. By calling it with `std::cin` instead of an open file: `read_screenings(std::cin, screenings, error, error_line)`. The function doesn't change, because it knows only `std::istream&`. Only the argument in `main` changes, and the reading rules stay the same.

</details>

## Self-assessment

For each competence, mark one answer:

| Competence | On my own | With a hint | After looking at the solution | To revise |
|---|---|---|---|---|
| A plan of the data, the reading and the responsibilities | | | | |
| A data file, the working directory and a failed open | | | | |
| A reading function with `std::istream&` | | | | |
| The end of the file versus an empty line | | | | |
| Numbers of physical lines | | | | |
| An empty line, a status that isn't allowed, an incomplete record | | | | |
| The first error without a partial report | | | | |
| A report with three totals | | | | |
| Normal, boundary and bad cases | | | | |
| The diagnostic of the line counter | | | | |

If anything is marked in the "To revise" column, go back to the matching lesson:

| Topic | Lesson |
|---|---|
| a data file, `std::ifstream`, the working directory, a failed open | [12.1](lesson_01_first_data_file.en.md) |
| a reading function with `std::istream&`, who opens the file, a stream by reference | [12.2](lesson_02_records_from_a_file.en.md) |
| the end of the file, empty lines, line numbers, the three kinds of error | [12.3](lesson_03_end_of_data_and_errors.en.md) |
| records in a vector, a report after the reading | [10.3](../module_10_input_records/lesson_03_building_a_vector_of_records.en.md) |

---

## Module 12 summary

After four lessons you can:

- open a text file with `std::ifstream`, check the opening, and understand where the program looks for a file given by a relative path;
- tell a failed open from a failed read, and an empty file from a missing one;
- write a reading function with an `std::istream&` parameter that works with a file and with `std::cin`;
- end the data only at the end of the file and tell it from an empty line, also with a last line without a line end;
- number physical lines and point to an empty line, a value that isn't allowed and an incomplete record;
- print the report only after checking the whole file, with no partial report after an error.

## What's next

This is the end of Module 12 and all of its planned lessons. The next modules of the course are in preparation.

**Previous lesson:** [Lesson 12.3: Where the data end and where the error is](lesson_03_end_of_data_and_errors.en.md) · **Next lesson:** in preparation · [Course overview](../../README.en.md)

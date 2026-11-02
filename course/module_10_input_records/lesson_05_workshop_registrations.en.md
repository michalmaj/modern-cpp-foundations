# Lesson 10.5: Workshop registrations (the Module 10 test)

[Polski](lesson_05_workshop_registrations.md) · **English** · [Course overview](../../README.en.md)

> **Module 10, lesson 5: the test** · about 115–140 minutes, in two sessions
> **You need:** your `cpp-workspace` folder and the original `lesson_05_first_program` project.
> **Pilot version.** The reference solutions in this lesson are checked automatically on Windows, Ubuntu and macOS, with the given input data. Nothing grades your own work automatically: you check it yourself, against the criteria. Typing input in CLion's **Run** window is described without a manual check on every system.

## How this test works

This lesson introduces nothing new. You check whether you can design, on your own, a program that **reads from the input a number of records not known in advance, builds a vector of them safely, and then analyses the finished collection with a function that gets it through `const&`**. In it you join lessons 10.1–10.4 with the vector from Module 6, the functions that analyse a collection from Module 8, and the references from Module 9. The only new thing is this combination: a collection built from input data goes into an analysing function that you designed.

The lesson has two parts:

- **Part A: the test.** Task 1: requirements, the data format, the report, examples and the criteria. No hints and no solution code. Everything you need is from Modules 1–10.
- **Part B: checking and discussion.** Hints, the full list of check cases, task 2 (diagnostics) and task 3 (explanations), which you do after task 1, and then the reference solution, fixes, answers and the self-assessment. Go there only after doing Part A, or when you consciously decide to stop trying on your own.

Looking at Part B, at earlier lessons or at your notes isn't a failure. What matters is that you **honestly note what you did on your own and what with help**. A suggested split into two sessions:

- **first:** analysing the data agreement, designing the type and the two functions, the reading loop, and the report for the data in the requirements;
- **second:** errors and boundary cases, the empty import, tasks 2 and 3, comparing with the solution, and the self-assessment.

**You may use:** CLion or the terminal, CMake and Ninja, as before; a `CMakeLists.txt` copied from the original `lesson_05_first_program`; case and trace tables, and temporary test printouts. You won't need the debugger. You don't have to end the data from the keyboard: you end typed data with an empty line, and you analyse on paper the cases in which the data end with no empty line.

---

# Part A: the test

## Task 1: Workshop registrations

The organisers of a set of workshops collect registrations from participants. Each person signs up for one of two groups, **group 1, the basic one**, or **group 2, the advanced one**, and chooses how many sessions they'll attend. The program reads all the registrations from the input, and then prints a report for the organisers. It doesn't model limits on places, payments, dates or session times.

**Preparation:** in `cpp-workspace`, create a folder `workshop_registrations`, copy into it the `CMakeLists.txt` from the original `lesson_05_first_program`, create an **empty** `main.cpp`, and write the whole program on your own.

### Input data

Each registration takes two lines:

1. the participant's full name, which may contain spaces;
2. two numbers separated by a space: the group number and the number of sessions.

For example, in this registration the person `Ala Nowak` signs up for group 1, for two sessions:

```text
Ala Nowak
1 2
```

Nobody announces the number of registrations. The reading ends when there's an **empty line** where the next full name would be, or when **the data end**. An empty line isn't a registration.

### Rules

- The full name isn't empty, because an empty line ends the data. It may contain spaces between words, but in data that follow the agreement it has no spaces at its start or end. Two people may have the same full name: they're still two registrations.
- The group number is exactly 1 or 2.
- The number of sessions is from 1 to 6, inclusive.
- All the data are ASCII text. The numbers are small and fit in `int`, as does their total. Data that follow the agreement have at most 5 registrations.
- The program doesn't check text after the second number, spaces at the start or end of the full name, lines made only of spaces, repeated names, or the number of registrations. Such data are outside the agreement.

### Errors

- **`Input error`:** one of the two numbers of a registration couldn't be read. There's a word instead of the number, or the data end after a non-empty full name or after the first number. A started registration without a required number is an error, not the ending of the data.
- **`Invalid registrations`:** both numbers were read, but the group number isn't 1 or 2, or the number of sessions is outside the range 1–6.
- When one of the numbers couldn't be read, the result is `Input error`, even if the other number breaks the rules.
- At the first error, the program prints exactly one of these messages and stops: it doesn't read any more data and prints no part of the report. Registrations accepted earlier may already be in the vector, and they don't have to be removed. The program doesn't correct the data and doesn't restore the stream.

### The type and the two functions

- The program defines **one own type** of registration with three fields: the full name (`std::string`), the group number (`int`) and the number of sessions (`int`). No extra fields: neither the name of the group, which the number determines, nor the number of all registrations. You choose the names of the type and the fields yourself.
- **The function that reads the numbers of one registration** gets the input stream that `main` reads from, the full name already read by `main`, and an existing result record prepared by `main`. It goes on reading from the same stream, neither copies nor changes the full name, and stores the complete registration in the caller's record. It returns `true` or `false`. On `false`, no field of the result record changes, even when one number has already been read. It prints nothing and adds nothing to the vector.
- **The function that counts the participants of a group** gets the finished collection of registrations and a group number. It goes through the whole collection without copying it and without being able to change its elements, and returns the number of registrations with that group number. It's a number of elements, as in lesson 8.4. It prints nothing, doesn't change the collection and doesn't create a new vector.
- You choose the parameter types and how they're passed yourself, so that the functions keep these agreements. The two functions have different jobs: the first changes one object in a controlled way, the second only reads the whole collection. A third function isn't needed. You may add your own helper function, for example one that prints or adds up, as long as it uses only constructs you know and doesn't change the collection.
- **`main`** reads the full names, recognises the ending of the data, prepares the result record, calls the reading function, and, only after `true`, adds the registration with `push_back` to a vector that starts empty. After a refusal, it chooses the message. The reading function returns only `true` or `false`: no new result type.
- `main` prints the report only after the reading has ended, and only from the elements of the vector. It isn't enough to count the groups and the sessions during the reading without storing the registrations. The program prints no prompts and uses no variables declared outside functions.

### The report

After the ending of the data, the program prints, in this order:

1. `Registrations:` and the number of registrations from `size()`;
2. `Group 1:` and the number of registrations for group 1, from the counting function;
3. `Group 2:` and the number of registrations for group 2, from the same function;
4. `Sessions total:` and the total of the numbers of sessions of all the registrations, computed from the elements of the vector;
5. `Group 2 participants:`, and below it the full names of the participants of group 2, each on its own line, in the order of the data. When group 2 has no registration, there's one line `(none)` instead of them.

The number of registrations, the numbers of participants of the two groups, and the total of sessions are four different pieces of information: for example, the total of sessions isn't a number of participants. The program prints no other messages and no empty lines.

### Examples

**Example A:** the data of the requirements, ended by an empty line.

<!-- input: workshop_registrations -->
```text
Ala Nowak
1 2
Jan Lis
2 4
Maja Kot
1 1
Olek Wrona
2 3

```

<!-- output: workshop_registrations -->
```text
Registrations: 4
Group 1: 2
Group 2: 2
Sessions total: 10
Group 2 participants:
Jan Lis
Olek Wrona
```

Group 1 is `Ala Nowak` and `Maja Kot`, and group 2 is `Jan Lis` and `Olek Wrona`. The total of sessions is 2 + 4 + 1 + 3 = 10.

**Example B:** the same data with no empty line, ended by the end of the data. The result is the same as in example A.

<!-- input: workshop_registrations -->
```text
Ala Nowak
1 2
Jan Lis
2 4
Maja Kot
1 1
Olek Wrona
2 3
```

<!-- output: workshop_registrations -->
```text
Registrations: 4
Group 1: 2
Group 2: 2
Sessions total: 10
Group 2 participants:
Jan Lis
Olek Wrona
```

**Example C:** the data start with an empty line. An empty vector is a valid result, not an error.

<!-- input: workshop_registrations -->
```text

```

<!-- output: workshop_registrations -->
```text
Registrations: 0
Group 1: 0
Group 2: 0
Sessions total: 0
Group 2 participants:
(none)
```

**Example D:** there's a word instead of the number of sessions of the second registration. The first registration may already have gone into the vector, but there's no report.

<!-- input: workshop_registrations -->
```text
Ala Nowak
1 2
Jan Lis
2 four
```

<!-- output: workshop_registrations -->
```text
Input error
```

**Example E:** the second registration has the group number 3.

<!-- input: workshop_registrations -->
```text
Ala Nowak
1 2
Jan Lis
3 4
```

<!-- output: workshop_registrations -->
```text
Invalid registrations
```

**Example F:** all the registrations are for group 1. **Predict** the report before you write the program.

<!-- input: workshop_registrations -->
```text
Ala Nowak
1 1
Maja Kot
1 3

```

<details>
<summary>Standard output for example F</summary>

<!-- output: workshop_registrations -->
```text
Registrations: 2
Group 1: 2
Group 2: 0
Sessions total: 4
Group 2 participants:
(none)
```

No registrations for group 2 isn't an error: that group is simply empty.

</details>

### How to work

The suggested order is a work plan, not twelve separate programs or runs:

1. Write down the agreement: the fields of a registration, the rules and both kinds of errors.
2. Design the registration type.
3. Design the function that reads the numbers of one registration: its parameters, how they're passed and what its result means.
4. Design the function that counts the participants of a group.
5. Create an empty vector.
6. Organise the reading of the full names until the ending of the data.
7. Add only complete registrations to the vector.
8. Handle the first error with no report.
9. Check the empty collection.
10. Print the report from the whole vector.
11. Check the counting of both groups and the total of sessions.
12. Check that the full names of group 2 stand in the order of the data.

**Before you run the program**, prepare a table of cases with the expected results: an empty line at the start; one, two and five registrations; both ways of ending; all the registrations in group 1 and all in group 2; the groups in a mixed order; the same full name twice; group 0, 3 and a negative one; 0, 1, 6, 7 and a negative number of sessions; a word instead of the group number and instead of the number of sessions; the end of the data after a full name and after the first number; an error in a registration after a valid one. For each case, write down the whole expected report or message.

**Run the program** for example A and for one of the errors in the second registration, from example D or E. End each line with **Enter**, and after the last registration press **Enter** once more, on an empty line. Analyse the other cases on paper. All the cases of the full check list are checked automatically.

When the result matches, you can save the project in Git, as in lesson 1.5. Before committing, check `git status`: only `main.cpp` and `CMakeLists.txt` go into the history.

## Success criteria

You pass the test when you meet **all** the criteria. You may use Part B while doing so, as long as you note it honestly in the self-assessment.

- `workshop_registrations/main.cpp` was written from an empty file, in valid C++20. The program builds without errors.
- There's one registration type with three fields of the required types, and the registrations go into one vector, in the order of the data.
- The reading function reads from the same stream as `main`, gets the full name without a copy and without being able to change it, and fills the record prepared by `main`. On a refusal it changes none of its fields, even when one number was read. It must check that both numbers were read before it checks the rules of the group and of the number of sessions, even if the program would print the same results without that check.
- The counting function gets the collection without a copy and without being able to change it, goes through all the elements, and returns the number of registrations of the chosen group. Through its loop variable, too, it reads each element without a copy and without being able to change it: a loop that copies the elements would be correct C++ and give the same result, but this task requires reading without copies.
- Neither of the two functions prints anything. The rules of the group and of the number of sessions stand in one place in the program.
- `main` stops reading after an empty line and after the end of the data where a full name would be, and prints `Input error` for a started, incomplete registration. `push_back` runs only after `true`, and on an error there's no part of the report.
- The report comes from the elements of the vector: the number of registrations from `size()`, the numbers of participants of the groups from the counting function, and the total of sessions and the full names from the elements.
- For example A and the chosen error in the second registration, the program prints exactly the results shown. The other examples and the cases of your table match your analysis on paper and the full check list.
- The table of cases was written before running the program.
- The bug from diagnostic A was fixed and checked, and the fragment from diagnostic B was analysed without running it (task 2 in Part B).
- You can explain every line of your program and answer the questions of task 3.

The names of the type, the fields, the functions and the variables, and the layout of `main`, may differ from the reference solution, as long as they're readable and meet the requirements. A correct result is a necessary condition, but **not proof of understanding**. That's why tasks 2 and 3 are part of the test.

---

# Part B: checking and discussion

Come here **only after doing Part A**, or when you consciously decide to stop trying on your own. This part contains hints, and further on code very close to the solution of task 1.

## How to check your work

- **Standard output:** compare the program's lines with the expected ones, character by character, including the colons, the spaces and the order of the full names. For valid data, check the whole report, not only the numbers.
- **The numbers of the report:** does the number of registrations equal the sum of the numbers of participants of the two groups? Does the total of sessions match the addition in your table? These numbers agreeing doesn't prove correctness, but their disagreeing always means a bug.
- **The record after a refusal:** does the reading function leave the result record unchanged also when the first number was read? The report won't show it, because after an error the program stops. The check program next to the reference solution helps with that.
- **Responsibilities:** does either of the functions print something? Do the rules of the group and of the number of sessions also stand in `main`? Could the counting function change the collection?

## Hints

<details>
<summary>Hint 1</summary>

Which job belongs to the function that reads a single record, and which to the function that analyses the finished collection? Which of them needs a modifiable reference?

</details>

<details>
<summary>Hint 2</summary>

Read the numbers into local variables, and change the result record only after checking all the rules. An empty line where a name would be ends the import, but a missing number after a name is an error.

</details>

<details>
<summary>Hint 3</summary>

After building the vector, pass it through `const&` to the function that counts the participants of a group. The report of the number of registrations, the total of sessions and the names of group 2 should rely on the elements of the finished collection.

</details>

## The full list of check cases

<details>
<summary>Open it after preparing your own table</summary>

The lines of the data are separated by `/`. For valid data, the "Result" column gives the number of registrations, the numbers of participants of groups 1 and 2, the total of sessions, and the full names from group 2. The program then prints the whole report, as in example A.

| | Data | Result | What it checks |
|---|---|---|---|
| A | `Ala Nowak` / `1 2` / `Jan Lis` / `2 4` / `Maja Kot` / `1 1` / `Olek Wrona` / `2 3` / an empty line | 4; 2 and 2; 10; `Jan Lis`, `Olek Wrona` | the data of the requirements: the groups in a mixed order, ending by an empty line |
| B | the same with no empty line, then the end of the data | as in A | the end of the data after a complete registration |
| C | an empty line | 0; 0 and 0; 0; `(none)` | the empty import |
| D | `Ala Nowak` / `1 2` / `Jan Lis` / `2 four` | `Input error` | a word instead of the number of sessions in the second registration; no partial report |
| E | `Ala Nowak` / `1 2` / `Jan Lis` / `3 4` | `Invalid registrations` | group 3 in the second registration; no partial report |
| F | `Ala Nowak` / `1 1` / `Maja Kot` / `1 3` / an empty line | 2; 2 and 0; 4; `(none)` | all the registrations in group 1; one session |
| G | `Ewa Maj` / `2 6`, then the end of the data | 1; 0 and 1; 6; `Ewa Maj` | one registration; all in group 2; six sessions |
| H | `Jan Lis` / `2 4` / `Ala Nowak` / `1 2` / `Jan Lis` / `2 1` / `Anna Maria Zielinska` / `2 6` / `Piotr Nowak` / `1 5` / an empty line | 5; 2 and 3; 18; `Jan Lis`, `Jan Lis`, `Anna Maria Zielinska` | five registrations; the same full name twice; three words on a line; group 1 only at the second position |
| I | `Ala Nowak` / `0 2` | `Invalid registrations` | group 0 |
| J | `Ala Nowak` / `-1 2` | `Invalid registrations` | a negative group |
| K | `Ala Nowak` / `1 0` | `Invalid registrations` | zero sessions |
| L | `Ala Nowak` / `2 7` | `Invalid registrations` | seven sessions |
| M | `Ala Nowak` / `1 -3` | `Invalid registrations` | a negative number of sessions |
| N | `Ala Nowak` / `one 2` | `Input error` | a word instead of the group number |
| O | `Ala Nowak`, then the end of the data | `Input error` | no numbers after a non-empty full name |
| P | `Ala Nowak` / `1`, then the end of the data | `Input error` | the second number missing |
| Q | `Ala Nowak` / `3 four` | `Input error` | a failed read takes precedence over a group that isn't allowed |
| R | `Ala Nowak` / `1 2` / an empty line / `Jan Lis` / `3 4` | 1; 1 and 0; 2; `(none)` | an empty line ends the data, so the program doesn't read the further lines |

**The automatic tests and your runs.** All the cases are checked automatically: the reference solution is run for each of them, and its whole standard output is compared with the expected one. The solution and its results are in [The reference solution](#the-reference-solution).

</details>

## Task 2: Diagnostics

Do this task **after task 1**, before looking at the reference solution. Both problems concern programs similar to yours.

<details>
<summary>Diagnostic A: the counting function ends too early (open only after task 1)</summary>

In `cpp-workspace`, create a folder `diagnosis_10`, copy into it the `main.cpp` and `CMakeLists.txt` from the original `lesson_05_first_program`, and put the program below in `main.cpp`: you may retype it or copy it. The program checks only the counting function, so the registrations are written in the code, not read from the input. The function should work the same as the counting function of task 1.

<!-- example: group_count_bug -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>
#include <vector>

struct Registration {
    std::string name;
    int group;
    int sessions;
};

std::size_t count_group(const std::vector<Registration>& registrations, int group) {
    std::size_t count{0};

    for (const Registration& registration : registrations) {
        if (registration.group == group) {
            ++count;
        }

        return count;
    }

    return count;
}

int main() {
    const std::vector<Registration> registrations{
        {"Ala Nowak", 1, 2}
    };

    std::cout << "Registrations: " << registrations.size() << "\n";
    std::cout << "Group 1: " << count_group(registrations, 1) << "\n";
    std::cout << "Group 2: " << count_group(registrations, 2) << "\n";
}
```

1. **Predict** the result for the data in the program: one registration for group 1. Then run the program. Does the result look correct?
2. **Predict** the result for an empty vector. Why doesn't an empty vector reveal the bug?
3. Change the registrations in the vector so that the bug becomes visible. Write down the correct numbers of participants of both groups for your data.
4. **Predict** how many passes of the loop the function makes for your data and what the program prints. Then run the program.
5. Point to the `return` that runs too early. Why does it end the whole function, not just one pass of the loop?
6. Why doesn't a correct result for one registration prove that the function is correct?
7. In lesson 9.4 a `return` in the loop was intended. How does counting all the matching registrations differ from finding one record?
8. Fix the function and run the program again for your data.

</details>

<details>
<summary>Diagnostic B: an incomplete registration taken for the ending of the data (open only after task 1)</summary>

Analyse this fragment **on paper**, without running it. It's the reading loop of another version of the program of task 1. It reads the full name at the start of each pass, like the loop in lesson 7.4, and after the loop the program prints the report. The function `read_registration_values` works correctly: it reads both numbers, checks the read and the rules, and changes nothing on `false`.

<!-- fragment -->
```cpp
bool reading{true};

while (reading) {
    std::string name{};
    std::getline(std::cin, name);

    if (std::cin.fail() || name.empty()) {
        reading = false;
    } else {
        Registration registration{"", 0, 0};
        const bool accepted{read_registration_values(std::cin, name, registration)};

        if (accepted) {
            registrations.push_back(registration);

            std::string rest{};
            std::getline(std::cin, rest);
        } else {
            reading = false;
        }
    }
}
```

The data, after which the input ends:

```text
Ala Nowak
1 2
Jan Lis
2
```

1. What does the program with this loop print for these data, and what's the correct result?
2. Why has the second registration already started?
3. Why is the missing number of sessions a read error, not the ending of the data?
4. Why mustn't every `false` be treated as the end of the data? What would this version print if the second registration had `3 4`?
5. Why mustn't a report with one registration be printed?
6. How do you separate the decision about the ending of the data from the decision about refusing a registration? What should the `else` branch do after `false`?

</details>

The results, example data and fixes are in [Diagnostics: results and fixes](#diagnostics-results-and-fixes).

## Task 3: Explain your design

Answer briefly, in writing, referring to your own program from task 1, before you open the reference solution:

1. Why does reading the numbers of one registration stand in a separate function, and reading the full names and the whole loop in `main`?
2. How does your reading function get the stream and the result record? Why are both parameters references without `const`?
3. Why mustn't the function change the result record before checking all the rules, although `main` stops after a refusal anyway?
4. When does `main` call `push_back`? What's in the vector after an error in the second registration, and why doesn't the program print part of the report?
5. How does the program tell an empty line from a failed read of a full name, and a started, incomplete registration from the ending of the data?
6. Why does the counting function get the vector through `const&`, and why does its loop variable also have `const&`?
7. Why must the counting function go through the whole collection, when the search in lesson 9.4 ended after finding the record?
8. How do the number of registrations, the numbers of participants of both groups and the total of sessions differ? Which relationship between them always holds, and which only for some data?
9. Why isn't having no participants in group 2 an error? How does your program know it should print `(none)`?
10. The reading function returned `true` for every registration, and the counting function returned numbers. Does that prove the report is correct? How do you check it?

## The reference solution

Look here **after doing tasks 1–3**. Your names and the layout of `main` may differ, as long as the program meets the requirements.

<details>
<summary>Task 1: workshop registrations</summary>

<!-- example: workshop_registrations -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>
#include <vector>

struct Registration {
    std::string name;
    int group;
    int sessions;
};

bool read_registration_values(std::istream& input, const std::string& name, Registration& result) {
    int group{0};
    int sessions{0};
    input >> group;
    input >> sessions;

    if (input.fail()) {
        return false;
    }

    if (group != 1 && group != 2) {
        return false;
    }

    if (sessions < 1 || sessions > 6) {
        return false;
    }

    result = Registration{name, group, sessions};
    return true;
}

std::size_t count_group(const std::vector<Registration>& registrations, int group) {
    std::size_t count{0};

    for (const Registration& registration : registrations) {
        if (registration.group == group) {
            ++count;
        }
    }

    return count;
}

int main() {
    std::vector<Registration> registrations{};
    std::string name{};
    std::getline(std::cin, name);

    while (!std::cin.fail() && !name.empty()) {
        Registration registration{"", 0, 0};
        const bool accepted{read_registration_values(std::cin, name, registration)};

        if (!accepted) {
            if (std::cin.fail()) {
                std::cout << "Input error\n";
            } else {
                std::cout << "Invalid registrations\n";
            }

            return 0;
        }

        registrations.push_back(registration);

        std::string rest{};
        std::getline(std::cin, rest);

        if (!std::cin.fail()) {
            std::getline(std::cin, name);
        }
    }

    const std::size_t basic_count{count_group(registrations, 1)};
    const std::size_t advanced_count{count_group(registrations, 2)};
    int sessions_total{0};

    for (const Registration& registration : registrations) {
        sessions_total += registration.sessions;
    }

    std::cout << "Registrations: " << registrations.size() << "\n";
    std::cout << "Group 1: " << basic_count << "\n";
    std::cout << "Group 2: " << advanced_count << "\n";
    std::cout << "Sessions total: " << sessions_total << "\n";
    std::cout << "Group 2 participants:\n";

    if (advanced_count == 0) {
        std::cout << "(none)\n";
    }

    for (const Registration& registration : registrations) {
        if (registration.group == 2) {
            std::cout << registration.name << "\n";
        }
    }
}
```

1. **`main` reads the full name,** because it's at that line that it's decided whether the data have ended. The reading function is called only once a registration has started.
2. **The stream through `std::istream&`,** because the function should go on reading from the existing `std::cin`, from where `main` stopped. No `const`, because reading changes the stream.
3. **The result record through `Registration&`,** because the function has two results: the `bool` tells about success, and the complete registration goes into the object prepared by `main`.
4. **The read before the assignment:** both numbers first go into local variables, because during the reading it isn't known yet whether a valid registration will come out. After a failed read, the value of a variable can't be relied on (lesson 4.6), so the rules are checked only after `input.fail()`. In this task, a number that couldn't be read is left as 0 (lesson 10.1), and 0 breaks the rules of both fields, so a program without this check would print the same results. The check stays, because the function's agreement mustn't depend on what was left in a variable: with rules that allow 0, as in the mission of lesson 10.4, such a program would accept a number that wasn't in the data.
5. **On `false` the record is unchanged,** because every `return false;` stands before `result = Registration{name, group, sessions};`. That's the "all or nothing" rule from lesson 9.2.
6. **An empty line isn't the same as a failed read:** an empty line is a successful read of a text of length zero (lesson 7.4), and the agreement says it ends the data. A failed read of a full name means there are no data left. Both end the reading, and neither creates a registration.
7. **A missing number after a non-empty full name is an error,** because the registration has already started. The function returns `false`, and `std::cin.fail()` gives `true`, so the result is `Input error`, not a report.
8. **`push_back` only after `true`,** because only complete, checked registrations should go into the vector (lesson 10.3).
9. **The collection through `const std::vector<Registration>&`,** because the counting function should only read the finished vector from `main`: no copy and no way to change it (lesson 8.4).
10. **The element through `const Registration&`,** because the loop only compares the field `group`. Without `&` each pass would copy a registration, and without `const` the loop could change it.
11. **No copy of the vector:** through `const&` the function works on the vector from `main`. A copy wouldn't change the result, but it would give nothing, and for a large collection it would cost time and memory.
12. **`std::size_t`,** because the function returns a number of elements, just like `size()` (lessons 6.3 and 8.4). That's why the program includes `<cstddef>`.
13. **The number of registrations from `size()`,** because the vector holds exactly the accepted registrations. A separate counter in the reading loop would repeat this information and could drift away from it.
14. **The total of sessions isn't a number of participants:** it adds up the fields `sessions`, rather than counting records. For the data of the requirements it's 10 with 4 registrations. The two numbers would be equal only if every registration had one session.
15. **The report only after the reading has ended,** because each of its lines concerns all the data. On an error in a later registration, the program stops with `return 0;` before printing anything of the report.
16. **`false` from the reading function doesn't mean the end of the data:** it means that the started registration is wrong and there's no new record. `main` recognises the ending of the data itself, before calling the function, and `std::cin.fail()` gives the cause of the refusal.
17. **No group 2 isn't an error:** data that follow the agreement may have not a single registration for group 2. The function then returns 0, the loop of full names prints nothing, and `(none)` says that the list is empty.
18. **A function's result doesn't replace checking the collection:** `true` says only that one registration is valid, and the counting function may give a wrong number, as in diagnostic A. `Group 2` and the list under `Group 2 participants:` describe the same elements of the vector, so they must agree, and the check cases compare the whole report.

**Other correct solutions:**

- a loop that reads the full name at the start of each pass, as in lesson 7.4, with a `bool` flag;
- a flag instead of `return 0;`, as long as the program prints no report after an error;
- the group rule written as `group < 1 || group > 2`, or all the rules in one condition joined by `||`;
- the fields of the result record assigned one by one, as long as that happens only after all the checks;
- the decision about `(none)` made with a `bool` flag set in the loop of full names;
- a separate function that adds up the sessions or prints the full names of group 2, getting the vector through `const&`.

This isn't the only correct solution.

Each case of the check list is a separate run of this program. Cases A–F are the examples of Part A. The others are below, in the order of the check list.

<!-- input: workshop_registrations -->
```text
Ewa Maj
2 6
```

<!-- output: workshop_registrations -->
```text
Registrations: 1
Group 1: 0
Group 2: 1
Sessions total: 6
Group 2 participants:
Ewa Maj
```

<!-- input: workshop_registrations -->
```text
Jan Lis
2 4
Ala Nowak
1 2
Jan Lis
2 1
Anna Maria Zielinska
2 6
Piotr Nowak
1 5

```

<!-- output: workshop_registrations -->
```text
Registrations: 5
Group 1: 2
Group 2: 3
Sessions total: 18
Group 2 participants:
Jan Lis
Jan Lis
Anna Maria Zielinska
```

<!-- input: workshop_registrations -->
```text
Ala Nowak
0 2
```

<!-- output: workshop_registrations -->
```text
Invalid registrations
```

<!-- input: workshop_registrations -->
```text
Ala Nowak
-1 2
```

<!-- output: workshop_registrations -->
```text
Invalid registrations
```

<!-- input: workshop_registrations -->
```text
Ala Nowak
1 0
```

<!-- output: workshop_registrations -->
```text
Invalid registrations
```

<!-- input: workshop_registrations -->
```text
Ala Nowak
2 7
```

<!-- output: workshop_registrations -->
```text
Invalid registrations
```

<!-- input: workshop_registrations -->
```text
Ala Nowak
1 -3
```

<!-- output: workshop_registrations -->
```text
Invalid registrations
```

<!-- input: workshop_registrations -->
```text
Ala Nowak
one 2
```

<!-- output: workshop_registrations -->
```text
Input error
```

<!-- input: workshop_registrations -->
```text
Ala Nowak
```

<!-- output: workshop_registrations -->
```text
Input error
```

<!-- input: workshop_registrations -->
```text
Ala Nowak
1
```

<!-- output: workshop_registrations -->
```text
Input error
```

<!-- input: workshop_registrations -->
```text
Ala Nowak
3 four
```

<!-- output: workshop_registrations -->
```text
Input error
```

<!-- input: workshop_registrations -->
```text
Ala Nowak
1 2

Jan Lis
3 4
```

<!-- output: workshop_registrations -->
```text
Registrations: 1
Group 1: 1
Group 2: 0
Sessions total: 2
Group 2 participants:
(none)
```

**The check program** checks the reading function's agreement on a refusal, which the report doesn't show, because after `false` the program stops. The type and the function are the same as above. `main` prepares the record `Old Name` with group 2 and five sessions, reads one full name, calls the function, and prints its result and the state of the record. It's a tool, not an extra task: running it is optional. You may swap in your own type and function, if you also change the names in `main`.

<!-- example: registration_values_check -->
```cpp
#include <iostream>
#include <string>

struct Registration {
    std::string name;
    int group;
    int sessions;
};

bool read_registration_values(std::istream& input, const std::string& name, Registration& result) {
    int group{0};
    int sessions{0};
    input >> group;
    input >> sessions;

    if (input.fail()) {
        return false;
    }

    if (group != 1 && group != 2) {
        return false;
    }

    if (sessions < 1 || sessions > 6) {
        return false;
    }

    result = Registration{name, group, sessions};
    return true;
}

int main() {
    Registration result{"Old Name", 2, 5};
    std::string name{};
    std::getline(std::cin, name);

    const bool accepted{read_registration_values(std::cin, name, result)};

    if (accepted) {
        std::cout << "Returned: true\n";
    } else {
        std::cout << "Returned: false\n";
    }

    std::cout << "Result: " << result.name << ", group " << result.group << ", sessions " << result.sessions << "\n";
}
```

Valid numbers change the record:

<!-- input: registration_values_check -->
```text
Ewa Maj
1 6
```

<!-- output: registration_values_check -->
```text
Returned: true
Result: Ewa Maj, group 1, sessions 6
```

After a refusal the record stays unchanged: after a word instead of the first and instead of the second number, after a missing second number, after a group that isn't allowed and after a number of sessions that isn't allowed. In the last three cases the first number was read, and still the record doesn't change.

<!-- input: registration_values_check -->
```text
Ewa Maj
one 2
```

<!-- output: registration_values_check -->
```text
Returned: false
Result: Old Name, group 2, sessions 5
```

<!-- input: registration_values_check -->
```text
Ewa Maj
1 four
```

<!-- output: registration_values_check -->
```text
Returned: false
Result: Old Name, group 2, sessions 5
```

<!-- input: registration_values_check -->
```text
Ewa Maj
1
```

<!-- output: registration_values_check -->
```text
Returned: false
Result: Old Name, group 2, sessions 5
```

<!-- input: registration_values_check -->
```text
Ewa Maj
3 4
```

<!-- output: registration_values_check -->
```text
Returned: false
Result: Old Name, group 2, sessions 5
```

<!-- input: registration_values_check -->
```text
Ewa Maj
1 7
```

<!-- output: registration_values_check -->
```text
Returned: false
Result: Old Name, group 2, sessions 5
```

</details>

## Diagnostics: results and fixes

<details>
<summary>Diagnostic A: the counting function ends too early</summary>

Before the fix, for one registration for group 1:

<!-- output: group_count_bug -->
```text
Registrations: 1
Group 1: 1
Group 2: 0
```

- **This case masks the bug.** The correct function would print the same. The loop has only one pass, so the `return count;` in its body runs only after the only registration has been checked.
- **An empty vector doesn't reveal the bug either:** the loop doesn't run even once, so both versions reach the `return count;` after the loop and return 0.
- **Data that reveal the bug:** several registrations, among which a matching registration stands further than at the first position. For example, `Ala Nowak` in group 1, `Jan Lis` in group 2 and `Maja Kot` in group 1. The correct result is `Group 1: 2` and `Group 2: 1`. The program with the bug prints:

<!-- example: group_count_revealed -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>
#include <vector>

struct Registration {
    std::string name;
    int group;
    int sessions;
};

std::size_t count_group(const std::vector<Registration>& registrations, int group) {
    std::size_t count{0};

    for (const Registration& registration : registrations) {
        if (registration.group == group) {
            ++count;
        }

        return count;
    }

    return count;
}

int main() {
    const std::vector<Registration> registrations{
        {"Ala Nowak", 1, 2},
        {"Jan Lis", 2, 4},
        {"Maja Kot", 1, 1}
    };

    std::cout << "Registrations: " << registrations.size() << "\n";
    std::cout << "Group 1: " << count_group(registrations, 1) << "\n";
    std::cout << "Group 2: " << count_group(registrations, 2) << "\n";
}
```

<!-- output: group_count_revealed -->
```text
Registrations: 3
Group 1: 1
Group 2: 0
```

| Call | Pass 1: `Ala Nowak`, group 1 | Further passes | Result | Correct result |
|---|---|---|---|---|
| `count_group(registrations, 1)` | matches, `count` = 1, then `return count;` | don't run | 1 | 2 |
| `count_group(registrations, 2)` | doesn't match, `count` = 0, then `return count;` | don't run | 0 | 1 |

- **Where the bug is:** `return count;` stands in the body of the loop, after the `if`. It runs in the first pass, whether or not the registration matches.
- **`return` ends the whole function,** not one pass of the loop (lesson 9.4). After it the loop has no further passes, and the function returns its result after checking only the first element.
- **A correct result for one registration proves nothing,** because with one element the first pass is also the last. Even two registrations, `Ala Nowak` in group 1 and `Jan Lis` in group 2, give a correct `Group 1: 1`, and the bug shows only in `Group 2: 0`. Only a matching registration at a further position reveals it. The data of the requirements of task 1 would reveal it too.
- **The difference from lesson 9.4:** there the function looked for one record, so after finding it the job was done, and a `return` in the loop was intended. The bug was a `return false;` in the body of the loop, after a record that didn't match. Here the function counts all the matching registrations, so the result is known only after the last element, and there should be no `return` in the loop at all.
- **The fix:** remove `return count;` from the body of the loop. Only the `return count;` after the loop stays. The compiler reports no error or warning here, because it's valid C++, just not what the function is for. The fixed function is the function of the reference solution:

<!-- example: group_count_fixed -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>
#include <vector>

struct Registration {
    std::string name;
    int group;
    int sessions;
};

std::size_t count_group(const std::vector<Registration>& registrations, int group) {
    std::size_t count{0};

    for (const Registration& registration : registrations) {
        if (registration.group == group) {
            ++count;
        }
    }

    return count;
}

int main() {
    const std::vector<Registration> registrations{
        {"Ala Nowak", 1, 2},
        {"Jan Lis", 2, 4},
        {"Maja Kot", 1, 1}
    };

    std::cout << "Registrations: " << registrations.size() << "\n";
    std::cout << "Group 1: " << count_group(registrations, 1) << "\n";
    std::cout << "Group 2: " << count_group(registrations, 2) << "\n";
}
```

<!-- output: group_count_fixed -->
```text
Registrations: 3
Group 1: 2
Group 2: 1
```

Now `Group 1` and `Group 2` add up to 3, as many as `Registrations`. In the version with the bug they added up to 1, although the registrations are only in groups 1 and 2.

</details>

<details>
<summary>Diagnostic B: an incomplete registration taken for the ending of the data</summary>

1. **This version prints a report with one registration:** `Registrations: 1`, `Group 1: 1`, `Group 2: 0`, `Sessions total: 2`, `Group 2 participants:` and `(none)`. **The correct result** is only `Input error`.
2. **The second registration has started,** because the read of the full name `Jan Lis` succeeded, and the line isn't empty. From that moment, the program must get both numbers of this registration.
3. **It's a read error,** because the group number was read, but the number of sessions wasn't: the data ended. The function returns `false`, and `std::cin.fail()` gives `true`. The ending of the data would be an empty line, or the end of the data where a full name would be, not in the middle of a registration.
4. **`false` says only that there's no new registration,** not why. The `else` branch sets `reading` to `false` just as an empty line does, so the program confuses an error with the ending. For `3 4`, this version would print the same report with one registration instead of `Invalid registrations`.
5. **A report with one registration would look complete,** although the data were wrong. The organisers wouldn't know that one registration wasn't recorded.
6. **The ending of the data is recognised by the condition `std::cin.fail() || name.empty()` when the full name is read,** before the function is even called. After the call, `false` always means an error in the registration. So the `else` branch should choose the message through `std::cin.fail()` (`Input error` or `Invalid registrations`) and end `main` with `return 0;`, with no report, as in the reference solution.

</details>

## Answers to task 3

<details>
<summary>Example answers</summary>

1. Because they're two different jobs. At the line of the full name it's decided whether the data have ended, so `main` handles that line and the loop. The function gets a registration that has already started and is responsible only for its numbers, so its `true` and `false` each have one meaning.
2. The stream through `std::istream&`, and the record through `Registration&`. The function should read from the existing `std::cin`, and reading changes the stream. It should also fill the object prepared by `main`. With `const` it could do neither, and without `&` it would work on a copy, or not compile at all.
3. Because the agreement says that after `false` the record is unchanged, whatever the caller does. The check program, or another caller, may go on using the record. `return false;` doesn't undo an earlier assignment.
4. Only after `true`. After an error in the second registration the vector holds the first registration, because it was added earlier. The program prints only a message, because the report should concern all the data, and with part of the registrations it would look complete.
5. An empty line is a successful read: `fail()` gives `false`, and `empty()` gives `true`. A failed read of a full name gives `fail()` equal to `true`. Both end the data. An incomplete registration has a non-empty, successfully read full-name line, and then a number is missing: then the function returns `false`, and that's an error.
6. Because the function only reads the finished vector: `&` removes the copy, and `const` guarantees that it won't change it. A loop variable with `const&`, for the same reason, doesn't copy the registrations and can't change them.
7. Because the number of matches is known only after checking the last element. The search in lesson 9.4 had to find one record and could end right after it. The counting function ends only after the loop.
8. The number of registrations counts the records in the vector, the number of participants of a group counts the records with a given group number, and the total of sessions adds up the fields `sessions`. The numbers of participants of groups 1 and 2 always add up to the number of registrations, because each registration belongs to exactly one group. The total of sessions equals the number of registrations only when every registration has one session.
9. Because the agreement allows nobody to sign up for group 2: those are valid data with an empty list. In the reference solution, `(none)` appears when the counting function returns 0 for group 2. Another correct solution is a flag set in the loop of full names.
10. No. `true` tells about one registration, and the counting function may be wrong, as in diagnostic A. I check the whole report for the cases of my table: whether the numbers of the groups add up to the number of registrations, and whether the list of group 2 has as many full names as `Group 2` says.

</details>

## Self-assessment

For each criterion, mark one answer:

| Criterion | On my own | With a hint | After looking at the solution | To review |
|---|---|---|---|---|
| The design of the registration type | | | | |
| The reading function: its parameters and how they're passed | | | | |
| The read before the rules, the record unchanged after a refusal | | | | |
| The ending of the data: an empty line and the end of the data | | | | |
| An incomplete registration and `Input error` | | | | |
| Values that aren't allowed and `Invalid registrations` | | | | |
| `push_back` only after `true`, no partial report | | | | |
| The counting function: `const&`, the whole collection, `std::size_t` | | | | |
| The total of sessions from the elements of the vector | | | | |
| The full names of group 2 in order, and `(none)` | | | | |
| The empty import | | | | |
| The table of cases before running | | | | |
| Diagnostic A (the counting function ends too early) | | | | |
| Diagnostic B (an incomplete registration as the ending of the data) | | | | |
| The explanations of task 3 | | | | |

Running the program correctly for the examples is only part of the evidence. Mastering Module 10 is also shown by the table of cases, both diagnostics and the explanations.

If anything is marked in the "To review" column, go back to the matching lesson:

| Topic | Lesson |
|---|---|
| a record from input, first the read, then the rules | [10.1](lesson_01_one_record_from_input.en.md) |
| a full name with spaces, finishing the number line | [10.2](lesson_02_names_with_spaces.en.md) |
| `push_back` of complete records, no partial report | [10.3](lesson_03_building_a_vector_of_records.en.md) |
| the reading function, `std::istream&`, the ending of the data | [10.4](lesson_04_reading_function_and_end_of_data.en.md) |
| a function that analyses a vector of records, `std::size_t` | [8.4](../module_08_structs/lesson_04_many_records_in_a_vector.en.md) |
| all or nothing, a `bool` result | [9.2](../module_09_mutable_references/lesson_02_a_change_only_when_allowed.en.md) |
| `return` in the loop and after the loop | [9.4](../module_09_mutable_references/lesson_04_find_a_record_and_change_it.en.md) |
| an empty line and a failed read | [7.4](../module_07_text/lesson_04_successive_lines.en.md) |

Then try the task again, for example for loans in a school library, where each loan has a title, section 1 or 2 and a number of days from 1 to 14, and the report gives the number of loans in each section and the titles from one of them.

---

## Module 10 summary

After five lessons, you can:

- read the fields of a record into local variables, check first the read, then the rules, and only then build the record;
- read names with spaces with `std::getline`, numbers with `>>`, and finish the number line;
- build a vector of records with `push_back` only from complete, checked records, and print no partial report at the first error;
- read records until an empty line or the end of the data, and tell the ending of the data from an incomplete record;
- write a function with `std::istream&` and `T&` that fills the result record only on success;
- pass a collection built from input to an analysing function through `const&`, and build a report from its elements.

## What's next

The next module of the course is in preparation.

**Previous lesson:** [Lesson 10.4: A record-reading function and the ending of the data](lesson_04_reading_function_and_end_of_data.en.md) · **Next lesson:** in preparation · [Course overview](../../README.en.md)

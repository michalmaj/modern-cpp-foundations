# Lesson 14.5: The measuring station (the Module 14 test)

[Polski](lesson_05_measuring_station.md) · **English** · [Course overview](../../README.en.md)

> **Module 14, lesson 5: the test** · about 150–190 minutes, in two sessions
> **You need:** your `cpp-workspace` folder and the original `lesson_05_first_program` project. The project of lesson 13.4, as a reminder of the two targets, and the mission of lesson 14.4 will be useful.
> **Pilot version.** The reference solution and its test programs are checked automatically on Windows, Ubuntu and macOS. The application program is built there, but the course's automatic tests don't run it: you run it yourself, by hand. Nothing grades your project automatically: you check it against the checklist. The steps in CLion are the same as in lesson 13.4: they are described according to the CLion 2026.3 documentation, without a manual check on every system.

## How this test works

This lesson introduces no new syntax. You check whether you can **design and test, on your own, a program that processes a sequence of data**: each result of a reading has a name of its own, a bad entry doesn't stop the rest of the work, and the tests check both the named results and their effects. It combines lessons 14.1–14.4 (`enum class`, `switch`, named results with the data unchanged after a refusal, reading that recovers the stream) with the skills of Module 13: a plan before the code, expected results from the contract, `std::istringstream` and two targets.

**The most important condition:** your test must show the bug in the supplied code **before** the fix. `PASS` lines after the fix alone aren't enough to pass the test: they don't show that the test can detect a bug at all.

The test has three parts and a review:

- **Part A: the plan.** The cases and the expected results from the specification, before you see the starter code.
- **Part B: the project and the testing.** A project with two targets, the function `collect_measurements`, the test program, detecting the bug in the supplied code, the fix and the same tests again. This is the largest part of the work.
- **Part C: a change of requirements.** A new named result, a sensor fault: first the tests of the new contract, which fail, then the change in the code and all the tests again.
- **Checking and review:** hints, the full list of cases, the reference solution, explanations, answers and a self-assessment. Go there only after Parts A and B, or when you consciously give up further work on your own.

Looking at a hint or at an earlier lesson isn't a failure. What matters is to **note honestly what was done independently and what with help**. A suggested split into two sessions:

- **first, about 115 minutes:** the specification, Part A, the project in CLion, `collect_measurements`, the test program, detecting the bug and the fix, that is runs 1–3;
- **second, about 55 minutes:** Part C with runs 4 and 5, the justification, the checklist and the self-assessment.

Typically it takes about 170 minutes in total. The range in the header, 150–190 minutes, is an estimate, not a limit: finding your own mistakes in the code and in the tests can take longer.

**You may use:** CLion or the terminal, CMake and Ninja, as before; `CMakeLists.txt` from the original `lesson_05_first_program` and the pattern of two targets from lesson 13.4; the check functions of lessons 13.1–13.3 and 14.3 (you get them in the test program's skeleton); `read_number` and `discard_rest_of_line` from lesson 14.4 (you get them in the starter code); your function `count_ratings` from the mission of lesson 14.4 as a starting point for `collect_measurements`; your earlier case tables. You won't need the debugger. You know everything you need from Modules 1–14.

Treat lessons 13.4 and 14.1–14.4 as reminders of the rules, not as a finished program to copy. You may carry over parts of code consciously, for example the loop of `count_ratings`, but prepare the plan, the cases, the expected results and the way of showing the bug on your own. If you adapt earlier code, note in the self-assessment where it comes from, what was carried over, what was changed and which decisions were made on your own.

---

## Specification: the measuring station

A weather station collects temperature measurements and gives a report at the end: how many measurements it accepted, how many entries it rejected, and what the lowest and the highest temperature were. In this test there is no real sensor: a **simulator** takes its place and sends the readings as text. In the tests you give this text through `std::istringstream`, and in the application program you type it in the **Run** window. The program uses no hardware, files or network.

### The simulator's protocol

- Each reading is one line that starts with a whole number: the temperature in degrees Celsius.
- The simulator may add any text after the number, for example a unit: `19 C`.
- Sometimes it sends an empty line. An empty line isn't a reading.
- The data end when the simulator stops sending.

As in lesson 14.4, the text where an attempt to read starts, up to the end of its line, is called an **entry**.

**The numeric-prefix policy.** The station reads the leading numeric prefix of an entry. It doesn't recognise units or comments and doesn't check the whole line: it discards the rest of the line. So `21 C` gives 21, and `21.5` gives 21 with no error reported.

| Entry | What the station reads | Result |
|---|---|---|
| `21` | 21 | `measured` |
| `21 C` | 21; the rest of the line is discarded | `measured` |
| `21.5` | 21, with no error reported | `measured` |
| `21 30` | 21; `30` is discarded | `measured` |
| `abc` | no number | `invalid_entry` |

This is the same rule as in `read_number` of lesson 14.4. `21.5` isn't a valid notation of a whole-number measurement, and the station accepts 21 anyway: this is a deliberate limit of this program, not a strict check of the line.

### Two ranges

| Range | Values | What a number outside it means |
|---|---|---|
| **the simulator protocol's numeric range** | from −99 to 99 | it isn't a valid message of the simulator, but a bad entry: `invalid_entry` |
| **the range of measurements the station accepts** | from −50 to 50, both bounds included | it's a valid message, but the station doesn't accept it: `out_of_range` |

The range of measurements lies inside the protocol's range. So the number 60 is a valid message with a temperature the station doesn't accept, and the number 100 isn't a valid message at all, just like `abc`.

### The function `read_measurement`

<!-- fragment -->
```cpp
enum class Reading {
    measured,
    out_of_range,
    invalid_entry,
    end_of_data
};

Reading read_measurement(std::istream& input, int& temperature);
```

**One call is one attempt to read**, as in `read_number`: the function looks for the next character that isn't whitespace, tries to read a number from there, and then uses up the rest of the current line. Empty lines and lines with only whitespace aren't attempts. For example, `"21\n\nabc\n23"` is three attempts: 21, `abc` and 23. The fourth call gives `end_of_data`.

| Result | When | `temperature` |
|---|---|---|
| `Reading::measured` | the number lies in the station's range of measurements | gets this number |
| `Reading::out_of_range` | the number lies in the protocol's range, but outside the station's range | unchanged |
| `Reading::invalid_entry` | there's no number at the start of the entry, the number is too large for `int`, or it lies outside the protocol's range | unchanged |
| `Reading::end_of_data` | there's no next entry | unchanged |

- **`temperature` changes only with `measured`.** With every other result it keeps its value from before the call. The function prints nothing.
- **The end of the data isn't a refusal**, and it lasts: once a call has given `end_of_data`, further calls on the same stream give `end_of_data` too.
- As in lesson 14.4, the contract assumes a working source of data: if the source stopped working, the function stops reading and returns `end_of_data` only as a signal to stop, and the caller can recognise it through `input.bad()`.

### The function `collect_measurements`

<!-- fragment -->
```cpp
struct StationReport {
    int measured;
    int out_of_range;
    int invalid_entries;
    int lowest;
    int highest;
};

StationReport collect_measurements(std::istream& input, int limit);
```

**The contract:**

- **Precondition:** `limit > 0`. The function doesn't check it.
- It calls `read_measurement` until it has accepted `limit` measurements or until the data run out.
- **Only accepted measurements count toward the limit.** Refusals, `out_of_range` and `invalid_entry`, are counted in their own fields and don't use up the limit.
- When it has accepted `limit` measurements, it stops at once: **the rest of the data stays unread in the stream**. The next call of `read_measurement` on the same stream reads the next entry.
- When the data run out earlier, it returns a report of what it managed to read. The end of the data itself isn't counted.
- It prints nothing.

| `StationReport` field | Meaning |
|---|---|
| `measured` | the number of accepted measurements |
| `out_of_range` | the number of refusals because of the station's range |
| `invalid_entries` | the number of bad entries |
| `lowest`, `highest` | the lowest and the highest accepted measurement; they mean something only when `measured > 0` |

**A report without measurements.** When the function accepted no measurement, whether with a completely empty stream or with entries none of which was accepted, `measured` is 0, and `lowest` and `highest` are 0 too. These zeros are **placeholders, not measurements**: `measured` decides whether the report contains measurements. A real 0 °C, on the other hand, is an ordinary measurement, because 0 lies in the station's range. The report contains no sum and no average.

### The application program

You get `main.cpp` ready-made in Part B. The program calls `collect_measurements` for `std::cin` with the limit 6, that is it collects six measurements, and prints the report. For these data, typed in consecutive lines (the fourth line is empty):

```text
21
60
abc

18
25
19 C
0
-5
7
```

it prints:

```text
Measurements: 6 of 6
Lowest: -5
Highest: 25
Out of range: 1
Invalid entries: 1
```

The sixth accepted measurement is `-5`, so the program stops after that line: `7` stays unread and doesn't get into the report. When no measurement was accepted, the program prints `No measurements` instead of `Lowest` and `Highest`. In every case it ends with exit code 0: rejecting bad entries is correct behaviour of the station.

This is **a manual run**: the course's automatic tests build the application program, but don't run it. You check that it agrees with this example yourself.

### The required structure

```text
measuring_station/
├── CMakeLists.txt
├── main.cpp
├── function_tests.cpp
├── rules.cpp
└── rules.hpp
```

- **`rules.hpp`:** all the types and declarations, with `#pragma once`. You get it ready-made.
- **`rules.cpp`:** the only definitions of the four functions: you get `discard_rest_of_line`, `read_number` and `read_measurement` ready-made, and you write `collect_measurements` on your own.
- **`main.cpp`:** the application program. You get it ready-made; it includes `rules.hpp`.
- **`function_tests.cpp`:** the test program. You get a skeleton with the check functions and two cases as a pattern, and you add the other cases of your plan. It includes `rules.hpp`, contains no definition of any of the four functions, and reads nothing from `std::cin`.
- **`CMakeLists.txt`:** two targets, `first_program` and `function_tests`, both with `rules.cpp`, in the form of lesson 13.4. Nothing more.
- **Each call of `read_measurement`** in the tests checks the result and `temperature`. **Each scenario of `collect_measurements`** checks each field of the report separately, with its own label. The test program prints `PASS` or `FAIL` with the expected and the actual result, the summary `Checks: N, failed: F`, and ends with exit code 0 or 1, depending on the failures.

**Decide on your own:**

1. which cases you'll check and which rule each of them decides;
2. which results and which reports you expect;
3. which value `temperature` starts from, so that every change is visible;
4. how you'll show that after the limit is reached, the rest of the data stayed in the stream;
5. how you'll write `collect_measurements`;
6. how you'll show the bug before the fix, and how you'll confirm that the fix broke nothing.

You'll find reminders in lessons [13.4](../module_13_testing_functions/lesson_04_tests_next_to_the_program.en.md) (two targets, the shared `rules.cpp`), [14.2](lesson_02_handling_every_state_with_switch.en.md) (`switch` with a label for each value), [14.3](lesson_03_function_explains_refusal.en.md) (a named result, the data unchanged after a refusal, the refusal precedence) and [14.4](lesson_04_reading_that_recovers_the_stream.en.md) (`read_number`, the end of the data, tests of sequences on one stream).

---

# Part A: the plan

Before you see the starter code and before you write any test, prepare a written plan. It consists of two tables. A list of names alone isn't enough: each row gives the data, the expected result and the reason for the choice.

**Direct cases** call `read_measurement` once, on their own stream. `temperature` starts each case at 777: no case gives this value, so every change will be visible.

| Case | Entry | Result | `temperature` after the call | Why |
|---|---|---|---:|---|
| D1 | `"21.5"` | `measured` | 21 | the numeric-prefix policy: the prefix read is 21 |

**Scenarios** call `collect_measurements` on their own stream. Write the expected report straight away in the form `{measured, out_of_range, invalid_entries, lowest, highest}`: in Part B you'll paste it into the test as `StationReport{…}`.

| Case | Stream text | `limit` | Report | In addition | Why |
|---|---|---:|---|---|---|
| C1 | `"21\n18\n25\n30\n"` | 3 | `{3, 0, 0, 18, 25}` | the next call of `read_measurement`: `measured`, 30 | the limit reached, the rest of the data unread; only positive measurements |

The plan has **12 direct cases** (with D1) and **8 scenarios** (with C1). Derive the other rows from the specification on your own.

**The direct cases must cover:**

- both bounds of the station's range, each from both sides;
- both bounds of the protocol's range, each from both sides;
- an entry with no number at the start;
- a real 0;
- no data.

**Each rule separately.** The result depends on three rules: whether there's a number at the start of the entry, whether it lies in the protocol's range, and whether it lies in the station's range. Each of them is checked by a pair of cases that differ only in that rule:

| Rule | Number inside | Number just past the bound |
|---|---:|---:|
| the lower bound of the station's range | −50 | −51 |
| the upper bound of the station's range | 50 | 51 |
| the upper bound of the protocol's range | 99 | 100 |
| the lower bound of the protocol's range | −99 | −100 |

The rule "there's a number at the start of the entry" also needs an entry with no number, for example `abc`. Derive the results of these cases from the table of results. A case that breaks several rules at once doesn't replace a pair: if the function skipped one of the rules, another one could still decide the result, and the bug would stay hidden.

**The scenarios must cover:**

- a completely empty stream;
- entries none of which is accepted, among them a number too large for `int`;
- zero as the first accepted measurement;
- the last valid entry without a line end;
- the last bad entry without a line end;
- an empty line and text after a number;
- two bad entries in a row;
- refusals of each kind, followed by a valid measurement;
- refusals before the limit is reached, and the rest of the data unread after the limit is reached, checked with the next call;
- a scenario with only negative measurements and one with only positive measurements, so that `lowest` and `highest` can't be confused with 0;
- the end of the data before the limit is reached.

One scenario may cover several of these points.

**Answer four questions in the plan:**

1. What are the two ranges, and what does a number outside each of them mean?
2. What does the limit count and what doesn't it count, and what happens to the data after it's reached?
3. What does the report look like for an empty stream, and what for entries without an accepted measurement? How do they differ from a report with a real 0?
4. How will you check that both programs use the same implementation?

The plan is a mandatory part of the test and is assessed together with the test program. Open the starter code only when the plan is ready.

---

# Part B: the project and the testing

In `cpp-workspace`, create the folder `measuring_station` and copy `CMakeLists.txt` from the original `lesson_05_first_program` into it. Create the four other files of the required structure next to it, as in lesson 13.4, and open the folder in CLion.

## The starter code

<details>
<summary>The starter code: open after preparing the plan of Part A</summary>

**`rules.hpp`**:

<!-- fragment -->
```cpp
#pragma once

#include <istream>

enum class ReadResult {
    accepted,
    out_of_range,
    invalid_input,
    end_of_input
};

void discard_rest_of_line(std::istream& input);
ReadResult read_number(std::istream& input, int minimum, int maximum, int& result);

enum class Reading {
    measured,
    out_of_range,
    invalid_entry,
    end_of_data
};

Reading read_measurement(std::istream& input, int& temperature);

struct StationReport {
    int measured;
    int out_of_range;
    int invalid_entries;
    int lowest;
    int highest;
};

StationReport collect_measurements(std::istream& input, int limit);
```

**`rules.cpp`**:

<!-- fragment -->
```cpp
#include "rules.hpp"

#include <limits>

void discard_rest_of_line(std::istream& input) {
    input.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
}

ReadResult read_number(std::istream& input, int minimum, int maximum, int& result) {
    if (input.bad()) {
        return ReadResult::end_of_input;
    }

    input >> std::ws;

    if (input.eof()) {
        return ReadResult::end_of_input;
    }

    int value{0};
    input >> value;

    if (input.fail()) {
        if (input.bad()) {
            return ReadResult::end_of_input;
        }

        input.clear();
        discard_rest_of_line(input);
        return ReadResult::invalid_input;
    }

    discard_rest_of_line(input);

    if (value < minimum || value > maximum) {
        return ReadResult::out_of_range;
    }

    result = value;
    return ReadResult::accepted;
}

Reading read_measurement(std::istream& input, int& temperature) {
    int value{0};
    const ReadResult result{read_number(input, -99, 99, value)};

    switch (result) {
        case ReadResult::accepted:
            break;
        case ReadResult::out_of_range:
            return Reading::out_of_range;
        case ReadResult::invalid_input:
            return Reading::invalid_entry;
        case ReadResult::end_of_input:
            return Reading::end_of_data;
    }

    if (value < -50 || value > 50) {
        return Reading::out_of_range;
    }

    temperature = value;
    return Reading::measured;
}
```

`discard_rest_of_line` and `read_number` are exactly as in lesson 14.4. `read_measurement` reads the number through `read_number` with the protocol's range, from −99 to 99, and checks the station's range itself. In this file, below `read_measurement`, you'll add `collect_measurements` according to the contract.

**This implementation compiles correctly, but it contains one undisclosed logic bug.** Don't look for it by reading the code: find it with your test.

**`main.cpp`**:

<!-- fragment -->
```cpp
#include <iostream>

#include "rules.hpp"

int main() {
    const int limit{6};
    const StationReport report{collect_measurements(std::cin, limit)};

    std::cout << "Measurements: " << report.measured << " of " << limit << "\n";

    if (report.measured > 0) {
        std::cout << "Lowest: " << report.lowest << "\n";
        std::cout << "Highest: " << report.highest << "\n";
    } else {
        std::cout << "No measurements\n";
    }

    std::cout << "Out of range: " << report.out_of_range << "\n";
    std::cout << "Invalid entries: " << report.invalid_entries << "\n";
}
```

**`function_tests.cpp`**, the skeleton:

<!-- fragment -->
```cpp
#include <iostream>
#include <sstream>
#include <string>

#include "rules.hpp"

std::string reading_text(Reading reading) {
    switch (reading) {
        case Reading::measured:
            return "measured";
        case Reading::out_of_range:
            return "out_of_range";
        case Reading::invalid_entry:
            return "invalid_entry";
        case Reading::end_of_data:
            return "end_of_data";
    }

    return "unknown";
}

void check_reading(const std::string& name, Reading expected, Reading actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << reading_text(expected) << ", actual " << reading_text(actual) << "\n";
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

void check_report(const std::string& name, const StationReport& expected, const StationReport& actual, int& checks, int& failed) {
    check_int(name + " measured", expected.measured, actual.measured, checks, failed);
    check_int(name + " out_of_range", expected.out_of_range, actual.out_of_range, checks, failed);
    check_int(name + " invalid_entries", expected.invalid_entries, actual.invalid_entries, checks, failed);
    check_int(name + " lowest", expected.lowest, actual.lowest, checks, failed);
    check_int(name + " highest", expected.highest, actual.highest, checks, failed);
}

int main() {
    int checks{0};
    int failed{0};

    std::istringstream input_d1{"21.5"};
    int temperature_d1{777};
    check_reading("D1 result", Reading::measured, read_measurement(input_d1, temperature_d1), checks, failed);
    check_int("D1 temperature", 21, temperature_d1, checks, failed);

    std::istringstream input_c1{"21\n18\n25\n30\n"};
    const StationReport report_c1{collect_measurements(input_c1, 3)};
    check_report("C1", StationReport{3, 0, 0, 18, 25}, report_c1, checks, failed);
    int next_c1{777};
    check_reading("C1 next result", Reading::measured, read_measurement(input_c1, next_c1), checks, failed);
    check_int("C1 next temperature", 30, next_c1, checks, failed);

    std::cout << "Checks: " << checks << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }
}
```

The skeleton has the check functions and two cases of the plan, D1 and C1, as a pattern:

- `reading_text` turns a result into text for the `FAIL` line, and `check_reading` compares the expected result with the actual one, as in lesson 14.3;
- `check_report` checks each field of the report separately: `"C1"` gives the labels `C1 measured`, `C1 out_of_range`, `C1 invalid_entries`, `C1 lowest` and `C1 highest`;
- in C1, `collect_measurements` is followed by one more call of `read_measurement` **on the same stream**: it checks that the rest of the data stayed unread.

Add the other cases of your plan before the summary line, in the same form.

**Until you write `collect_measurements`, the project won't build:** both programs call this function, and the linker won't find its definition.

</details>

## The order of work

1. **The files.** Copy the starter code into your files. In `rules.cpp`, below `read_measurement`, write `collect_measurements` according to the contract. **Don't change `read_measurement`.**
2. **The test program.** Add all the cases of your plan to the skeleton of `function_tests.cpp`, with the expected results of the plan.
3. **Two targets.** Change `CMakeLists.txt` as in lesson 13.4. CMake looks for all the files of both lists as soon as it loads the project, so the files must exist beforehand. Reload the project and choose **Build | Build Project**.
4. **This is the first mandatory run:** run `first_program` and type the data of the example in the specification in the **Run** window, each line ended with Enter; an empty line is Enter alone. After the line `-5` the program stops by itself and prints the report: it doesn't wait for `7`. Compare the report with the specification.
5. **This is the second mandatory run:** run `function_tests`. With the supplied code, at least one check should give `FAIL`, and the test program should end with exit code 1. Write down the `FAIL` lines, with the expected and the actual results, and the exit code. This is the proof that your test detects the bug.
6. If all the checks gave `PASS`, your test set doesn't detect the bug. First check that your `collect_measurements` passes its scenarios. Then go back to the plan and to the table of pairs: does each rule have a case that decides it on its own? Complete the plan and the tests, and run them again. Don't change `read_measurement` yet.
7. **Find the cause.** From the `FAIL` lines and the contract, point to the place in `read_measurement` that works differently from what the specification says. Write down whether the error is in the function or in the expected result, and how you know.
8. **Fix only the cause in `read_measurement`.** Don't change the test data, the expected results, `main.cpp`, `CMakeLists.txt` or `collect_measurements`.
9. **This is the third mandatory run:** choose **Build Project** and run `function_tests` again. All the checks should give `PASS`, and the exit code should be 0. Rebuilding alone, without running the tests, doesn't confirm the fix.

You fix `FAIL` lines caused by your own `collect_measurements` in `collect_measurements`, still before step 5, if the expected result agrees with the contract. Such extra runs don't count toward the five mandatory ones.

---

# Part C: a change of requirements

Do this part **after Part B**, preferably in the second session.

**The new requirement.** The simulator now reports a sensor fault with the number **−99**. This is a **fault code**, reserved in the protocol: it isn't a temperature. The station has to recognise it as a new named result.

| Number | Meaning | Result |
|---|---|---|
| −99 | the sensor's fault code | `Reading::sensor_fault` |

- `Reading` gets the value `sensor_fault`, before `end_of_data`, and `StationReport` gets the field `sensor_faults`, as the last one:

<!-- fragment -->
```cpp
enum class Reading {
    measured,
    out_of_range,
    invalid_entry,
    sensor_fault,
    end_of_data
};

struct StationReport {
    int measured;
    int out_of_range;
    int invalid_entries;
    int lowest;
    int highest;
    int sensor_faults;
};
```

- `read_measurement` returns `sensor_fault` for −99. `temperature` doesn't change.
- `collect_measurements` counts the faults in `sensor_faults`. A fault isn't a measurement: it doesn't increase `measured`, doesn't change `lowest` or `highest`, and doesn't use up the limit.
- The application program prints the line `Sensor faults: ` with the number of faults at the end of the report.
- `ReadResult`, `read_number` and both ranges stay unchanged. −100 is still a bad entry, and −98 is still a refusal because of the station's range.

**Precedence.** −99 also lies outside the station's range, so two rules fit this number. The contract sets which one decides, like the refusal precedence of lesson 14.3: **you check the fault code before the station's range.**

**The order of work:**

1. **The change map.** Before you change the code, write down in which places of the project `Reading` or `StationReport` appears, and what will change in each of them. Also write down which old expectations the new rule changes, and why only those.
2. **The types.** In `rules.hpp`, add `sensor_fault` and `sensor_faults`.
3. **The labels.** In the `switch` in `collect_measurements`, add a label `sensor_fault` that increases `sensor_faults`, and in `reading_text` a label that returns `"sensor_fault"`. The field `sensor_faults` starts at 0, like the others.
4. **The tests of the new contract.**
   - `check_report` has to check `sensor_faults` too, with a label like the other fields.
   - Complete **every** expected `StationReport{…}` with an explicit sixth value, also in the old scenarios, where it's 0.
   - The new rule changes expectations only where the entry `-99` appears. If your plan has it in one direct case only, that's the only old expectation you change. Write down the reason for every such change.
   - Add a direct case with the entry `-98`, a neighbour of the fault code that the new rule doesn't concern.
   - Add a scenario in which a fault stands between measurements and the limit is reached: check the report and the next call on the same stream.
   - Add a scenario with faults only.
5. **This is the fourth mandatory run:** build the project and run `function_tests`. `read_measurement` doesn't recognise −99 yet, so the checks that describe the fault should give `FAIL`, and the exit code should be 1. Write down the `FAIL` lines. This `FAIL` is expected: the tests already describe the new contract, and the function doesn't yet.
6. **The change of the function.** In `read_measurement`, add the check of the fault code, before the check of the station's range. In `main.cpp`, add the line `Sensor faults`.
7. **This is the fifth mandatory run:** run `function_tests`. All the checks, old and new, should give `PASS`, and the exit code should be 0. If you like, also run `first_program` with data that contain `-99`.

**The explicit sixth value is mandatory.** The compiler won't enforce it: with the project settings of lesson 0.5, `StationReport{3, 0, 0, 18, 25}` for a struct with six fields compiles without a warning, and the missing field silently gets 0. The test would look complete, while saying nothing about faults. The `-Wswitch` warning of lesson 14.2 can point to a `switch` without a `sensor_fault` label, but the tests decide what's correct, not warnings.

## When something goes differently

| What you see | What it means | What to do |
|---|---|---|
| A linker error with `collect_measurements`, for example `undefined reference` or `undefined symbol` | The function is declared in `rules.hpp`, but its definition isn't in `rules.cpp` yet. | Write `collect_measurements` in `rules.cpp`, below `read_measurement`. |
| The test program doesn't end | The loop in `collect_measurements` doesn't get `end_of_data`: the end of the data doesn't end the loop, or the recovery of the stream is broken and every attempt meets the same text. | Stop the program with the **Stop** button. Check what your loop does with `end_of_data`, and compare `read_number` with lesson 14.4. |
| With the supplied code, all the checks give `PASS` | Some rule has no case that decides it on its own. | Go back to the table of pairs of Part A and to hint 3. |
| `lowest` is 0, although all the measurements are positive | `lowest` and `highest` start at 0 instead of at the first accepted measurement. | The first accepted measurement sets both fields. |
| After a zero as the first measurement, `lowest` or `highest` is wrong | 0 in `lowest` is treated as "nothing accepted yet". | `measured` decides whether anything was accepted, not the value in `lowest`. |
| A scenario with refusals before the limit gives too few measurements | The limit counts all attempts, not accepted measurements. | Only `measured` counts toward the limit. |
| In Part C, a fault is counted in `out_of_range` | The check of the station's range comes before the check of the fault code. | Put the checks in the order of precedence. |
| In Part C, an old scenario passes although it doesn't check faults | The expected `StationReport{…}` has five values, and the sixth field silently got 0. | Write an explicit sixth value in every expected report. |
| `21.5` is accepted as 21 | That's how the numeric-prefix policy works. | It's intended. |
| A warning with `enumeration value 'sensor_fault' not handled in switch` | A `switch` has no label for the new value (lesson 14.2). | Add the label and check its effect in the tests. |

## Justification

Answer in your own words, referring to your project:

1. Why do the expected results come from the contract, not from what the program does?
2. Why does the pair 99 and 100 decide the rule of the protocol's range? Would the case `abc` be enough?
3. What did your `FAIL` line before the fix show, and what doesn't it decide?
4. Why isn't the zero in an empty report a measurement, and how do your tests check it?
5. Why does the limit count only accepted measurements, and which case checks it?
6. Why don't you change any expectation after the fix in Part B, while in Part C you change one?
7. Why do you check the fault code before the station's range? Which case detects it?
8. Why do both targets use `rules.cpp`, and why do you run all the tests after every change?

---

## Checklist before you hand in

The test is passed when you meet **all** the items of this list. Your names of cases, variables and checks, and the order of the cases, may differ from the reference solution, as long as they meet the specification. A correct report of the application program, building the project alone, or `PASS` lines after the fix alone aren't enough.

- [ ] 1. The plan of Part A was made before the starter code was opened: 12 direct cases (entry, result, `temperature` after the call) and 8 scenarios (text, `limit`, report in the form `{…}`), each with a reason.
- [ ] 2. All the expected values come from the contract; none comes from running the program.
- [ ] 3. Each rule has a pair that decides it on its own: −50 and −51, 50 and 51, 99 and 100, −99 and −100, plus an entry with no number, for example `abc`.
- [ ] 4. The project has five files and the ten-line `CMakeLists.txt` with `first_program` and `function_tests`; `rules.cpp` is on both lists.
- [ ] 5. The four functions are defined only in `rules.cpp`; `main.cpp` and `function_tests.cpp` include `rules.hpp`.
- [ ] 6. Each case has its own `std::istringstream`; the extra call after the limit is reached uses the same stream as the scenario.
- [ ] 7. Each call of `read_measurement` checks the result and `temperature`, and `temperature` starts from a value no case gives.
- [ ] 8. Each scenario is checked by `check_report`: a separate check and a separate label for each field of the report.
- [ ] 9. The cases cover `21.5`, a real 0, no data, a completely empty stream, entries without an accepted measurement, zero as the first measurement, the last valid and the last bad entry without a line end, an empty line, text after a number, refusals before the limit is reached, and the limit reached with the rest of the data unread.
- [ ] 10. `collect_measurements` counts only accepted measurements toward the limit, sets `lowest` and `highest` from the first accepted measurement, and with a refusal changes only the matching counter.
- [ ] 11. `first_program` was run by hand with the data of the example in the specification and printed the report of the specification.
- [ ] 12. With the supplied code, `function_tests` gave `FAIL` and ended with exit code 1. The `FAIL` lines, the exit code and the cause in `read_measurement` are written down.
- [ ] 13. The fix changed only the cause in `read_measurement`; the same tests with the same expectations gave only `PASS` and exit code 0.
- [ ] 14. Part C: `sensor_fault`, `sensor_faults` and the labels in `collect_measurements` and in `reading_text` are added; every expected `StationReport{…}` has an explicit sixth value; `check_report` checks `sensor_faults`; there are new cases: `-98`, a fault among measurements with the limit reached, and faults only.
- [ ] 15. Part C: before the check of the fault code, run 4 gave `FAIL` and exit code 1. With the check placed before the station's range, run 5 gave only `PASS` and exit code 0. The changed old expectations concern only the entry `-99`, and the reason for the change is written down.
- [ ] 16. The eight questions of the justification have answers that refer to your project, and the self-assessment is filled in, with the adapted code written down.

When you are done, you can save the project `measuring_station` in Git, as in lesson 1.5: the five files, without the build folder.

## Assessment criteria

The rubric is for self-assessment or for assessment by a teacher. The course has no grading scale and no points threshold: the points show which areas are mastered and which need revision. The checklist above decides whether the test is passed, not the number of points.

| Area | Points | Full points when |
|---|---:|---|
| The plan and the contract (Part A) | 10 | items 1 and 2 of the checklist; the answers to the plan's questions are correct |
| The choice of cases and the expected results | 15 | items 3 and 9; each bound is checked from both sides |
| Named results, recovery and the end of the data | 15 | the result of each call is checked; the last valid and the last bad entry without a line end are handled correctly; an empty line isn't an attempt; `end_of_data` ends the loop and isn't counted |
| The report, the limit and unchanged data | 15 | item 10; both cases of a report without measurements and a real 0 are checked; the rest of the data after the limit is checked; `temperature` unchanged after every refusal and fault is checked |
| Two targets and one implementation | 10 | items 4, 5 and 11 |
| The bug: `FAIL`, cause, fix, the same tests | 15 | items 12 and 13 |
| Part C: the change of the contract and regression | 15 | items 14 and 15 |
| Justification and self-assessment | 5 | item 16 |
| **Total** | **100** | |

These don't give full points in their area:

- **named results:** the last value without a line end lost, or the end of the data counted as a refusal;
- **two targets:** a function copied outside `rules.cpp`, even when both targets are defined;
- **the report:** a change of `temperature` or of the report after a refusal that nothing detects;
- **the bug:** no `FAIL` before the fix, `FAIL` with exit code 0, or an expectation changed in Part B;
- **Part C:** an expectation changed beyond the cases with `-99` and the new field, or a solution that relies on a compiler warning instead of on tests.

**Other names** of variables, cases, checks and helper functions take away no points. The names of the targets, files, types and functions of the contract are fixed, though: they come from the specification.

**What is checked automatically, and what isn't.** The course's tests check that the reference solution builds, in each variant with both targets, and that its test programs give the shown results and exit codes. The application program is built, but not run: you check its report of the specification by hand. **No automatic check looks at your project, your plan, your tests or your justification:** a person assesses them by reading the plan and the code and comparing your runs with the checklist.

---

# Checking and review

Go here **only after Parts A and B**, or when you consciously give up further work on your own. The solution's code follows.

## Hints

<details>
<summary>Hint 1: the table of results</summary>

Which rule gives which of the four results? Which two numbers lie outside the station's range and differ only in whether they fit in the protocol's range? Which pair shows each bound from both sides? Write down the result of each case before you run anything.

</details>

<details>
<summary>Hint 2: the report and the limit</summary>

Which call sets `lowest` and `highest` for the first time? What counts toward the limit, and what doesn't? How will you show that the data after the limit are still in the stream: which call, on which stream, will check it?

</details>

<details>
<summary>Hint 3: when everything passes with the supplied code</summary>

Is there a rule of the specification that none of your cases decides on its own? Compare your cases with the table of pairs of Part A: for each pair, write down which result each of the two numbers gives, and why. Complete the plan first, then the tests.

</details>

<details>
<summary>Hint 4: the order in Part C</summary>

First the value, the field and the labels, then the tests: they should fail. Only then the check in `read_measurement`. Which check has to come first for −99? Which old expectations does the new rule change, and why only those?

</details>

## The full list of control cases

<details>
<summary>Cases D1–D13 and C1–C10, results from the contract</summary>

**Direct cases.** Each has its own stream, and `temperature` starts at 777. D13 and the changed result of D8 belong to Part C.

| Case | Entry | Result | `temperature` after the call | What it decides |
|---|---|---|---:|---|
| D1 | `"21.5"` | `measured` | 21 | the numeric-prefix policy, an ordinary measurement |
| D2 | `"-50"` | `measured` | −50 | the station's lower bound, inside |
| D3 | `"-51"` | `out_of_range` | 777 | the station's lower bound, just past it |
| D4 | `"50"` | `measured` | 50 | the station's upper bound, inside |
| D5 | `"51"` | `out_of_range` | 777 | the station's upper bound, just past it |
| D6 | `"99"` | `out_of_range` | 777 | the protocol's upper bound, inside |
| D7 | `"100"` | `invalid_entry` | 777 | the protocol's upper bound, just past it |
| D8 | `"-99"` | `out_of_range`, in Part C `sensor_fault` | 777 | the protocol's lower bound, inside; in Part C the fault code |
| D9 | `"-100"` | `invalid_entry` | 777 | the protocol's lower bound, just past it |
| D10 | `"abc"` | `invalid_entry` | 777 | no number at the start of the entry |
| D11 | `"0"` | `measured` | 0 | a real 0 is a measurement |
| D12 | `""` | `end_of_data` | 777 | no data; `temperature` unchanged at the end too |
| D13 | `"-98"` | `out_of_range` | 777 | Part C: the fault code's neighbour, unchanged |

**Scenarios.** The report has the form `{measured, out_of_range, invalid_entries, lowest, highest}`, and in Part C also `sensor_faults` at the end: in C1–C8 it's 0. C9 and C10 belong to Part C.

| Case | Stream text | `limit` | Report | In addition | What it checks |
|---|---|---:|---|---|---|
| C1 | `"21\n18\n25\n30\n"` | 3 | `{3, 0, 0, 18, 25}` | the next call: `measured`, 30 | the limit reached, the rest unread; only positive measurements |
| C2 | `"21\n\n60\nabc\n19 C\n"` | 5 | `{2, 1, 1, 19, 21}` | | an empty line isn't an attempt; a refusal of each kind and a valid measurement after them; text after a number; the end of the data before the limit |
| C3 | `"abc\nxyz\n-5"` | 4 | `{1, 0, 2, -5, -5}` | | two bad entries in a row; the last valid entry without a line end; one measurement is both the lowest and the highest |
| C4 | `""` | 3 | `{0, 0, 0, 0, 0}` | | a completely empty stream |
| C5 | `"15\nerr"` | 4 | `{1, 0, 1, 15, 15}` | | the last bad entry without a line end |
| C6 | `"60\n70\n-3\n-12\n8\n"` | 2 | `{2, 2, 0, -12, -3}` | the next call: `measured`, 8 | refusals don't use up the limit; the rest unread; only negative measurements |
| C7 | `"0\n5"` | 3 | `{2, 0, 0, 0, 5}` | | zero as the first measurement; the end of the data before the limit |
| C8 | `"60\nabc\n99999999999"` | 3 | `{0, 1, 2, 0, 0}` | | entries without an accepted measurement; a number too large for `int`; placeholders |
| C9 | `"21\n-99\n22\n23\n"` | 2 | `{2, 0, 0, 21, 22, 1}` | the next call: `measured`, 23 | Part C: a fault doesn't use up the limit and doesn't change `lowest` or `highest` |
| C10 | `"-99\n-99"` | 1 | `{0, 0, 0, 0, 0, 2}` | | Part C: faults only, no measurement, placeholders |

Your plan doesn't have to have exactly these cases. It has to have all the kinds listed in Part A and the pairs of the table of pairs.

</details>

## The reference solution

<details>
<summary>The plan and the project of the reference solution, before the fix</summary>

This is one of the correct solutions, not the only acceptable form.

**The answers to the plan's questions, in short:**

1. The protocol's range is −99…99: a number outside it is `invalid_entry`, just like an entry with no number. The station's range is −50…50: a number in the protocol's range but outside the station's range is `out_of_range`.
2. The limit counts only accepted measurements. When it's reached, the function stops, and the rest of the data stays in the stream: C1 and C6 check it with the next call.
3. Both have `measured == 0` and the placeholders `lowest == 0`, `highest == 0`: C4 for the empty stream, C8 for entries without an accepted measurement. A report with a real 0, as in C7, has `measured > 0`, so its `lowest` is a measurement.
4. The four functions are defined only in `rules.cpp`, and this file is on the lists of both targets. The bug in `read_measurement` changes the result of the tests, and the same function gives the application program its report.

**`collect_measurements`:** the loop runs while `measured` is less than `limit` and the data haven't run out. Each result is handled by a separate `case` label, ended by `break`, as in `count_ratings` of lesson 14.4. The first accepted measurement sets `lowest` and `highest`, and each next one is compared with them. `end_of_data` sets the flag `input_ended` and counts nothing.

**`main.cpp`**:

<!-- example: station_given target=function_tests exit=1 -->
```cpp
#include <iostream>

#include "rules.hpp"

int main() {
    const int limit{6};
    const StationReport report{collect_measurements(std::cin, limit)};

    std::cout << "Measurements: " << report.measured << " of " << limit << "\n";

    if (report.measured > 0) {
        std::cout << "Lowest: " << report.lowest << "\n";
        std::cout << "Highest: " << report.highest << "\n";
    } else {
        std::cout << "No measurements\n";
    }

    std::cout << "Out of range: " << report.out_of_range << "\n";
    std::cout << "Invalid entries: " << report.invalid_entries << "\n";
}
```

**`rules.hpp`**:

<!-- file: station_given rules.hpp -->
```cpp
#pragma once

#include <istream>

enum class ReadResult {
    accepted,
    out_of_range,
    invalid_input,
    end_of_input
};

void discard_rest_of_line(std::istream& input);
ReadResult read_number(std::istream& input, int minimum, int maximum, int& result);

enum class Reading {
    measured,
    out_of_range,
    invalid_entry,
    end_of_data
};

Reading read_measurement(std::istream& input, int& temperature);

struct StationReport {
    int measured;
    int out_of_range;
    int invalid_entries;
    int lowest;
    int highest;
};

StationReport collect_measurements(std::istream& input, int limit);
```

**`rules.cpp`**, the supplied code and `collect_measurements`:

<!-- file: station_given rules.cpp -->
```cpp
#include "rules.hpp"

#include <limits>

void discard_rest_of_line(std::istream& input) {
    input.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
}

ReadResult read_number(std::istream& input, int minimum, int maximum, int& result) {
    if (input.bad()) {
        return ReadResult::end_of_input;
    }

    input >> std::ws;

    if (input.eof()) {
        return ReadResult::end_of_input;
    }

    int value{0};
    input >> value;

    if (input.fail()) {
        if (input.bad()) {
            return ReadResult::end_of_input;
        }

        input.clear();
        discard_rest_of_line(input);
        return ReadResult::invalid_input;
    }

    discard_rest_of_line(input);

    if (value < minimum || value > maximum) {
        return ReadResult::out_of_range;
    }

    result = value;
    return ReadResult::accepted;
}

Reading read_measurement(std::istream& input, int& temperature) {
    int value{0};
    const ReadResult result{read_number(input, -99, 99, value)};

    switch (result) {
        case ReadResult::accepted:
            break;
        case ReadResult::out_of_range:
            return Reading::out_of_range;
        case ReadResult::invalid_input:
            return Reading::invalid_entry;
        case ReadResult::end_of_input:
            return Reading::end_of_data;
    }

    if (value < -50 || value > 50) {
        return Reading::out_of_range;
    }

    temperature = value;
    return Reading::measured;
}

StationReport collect_measurements(std::istream& input, int limit) {
    StationReport report{0, 0, 0, 0, 0};
    int temperature{0};
    bool input_ended{false};

    while (report.measured < limit && !input_ended) {
        const Reading reading{read_measurement(input, temperature)};

        switch (reading) {
            case Reading::measured:
                if (report.measured == 0) {
                    report.lowest = temperature;
                    report.highest = temperature;
                } else if (temperature < report.lowest) {
                    report.lowest = temperature;
                } else if (temperature > report.highest) {
                    report.highest = temperature;
                }

                ++report.measured;
                break;
            case Reading::out_of_range:
                ++report.out_of_range;
                break;
            case Reading::invalid_entry:
                ++report.invalid_entries;
                break;
            case Reading::end_of_data:
                input_ended = true;
                break;
        }
    }

    return report;
}
```

**`function_tests.cpp`**, the cases D1–D12 and C1–C8:

<!-- file: station_given function_tests.cpp -->
```cpp
#include <iostream>
#include <sstream>
#include <string>

#include "rules.hpp"

std::string reading_text(Reading reading) {
    switch (reading) {
        case Reading::measured:
            return "measured";
        case Reading::out_of_range:
            return "out_of_range";
        case Reading::invalid_entry:
            return "invalid_entry";
        case Reading::end_of_data:
            return "end_of_data";
    }

    return "unknown";
}

void check_reading(const std::string& name, Reading expected, Reading actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << reading_text(expected) << ", actual " << reading_text(actual) << "\n";
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

void check_report(const std::string& name, const StationReport& expected, const StationReport& actual, int& checks, int& failed) {
    check_int(name + " measured", expected.measured, actual.measured, checks, failed);
    check_int(name + " out_of_range", expected.out_of_range, actual.out_of_range, checks, failed);
    check_int(name + " invalid_entries", expected.invalid_entries, actual.invalid_entries, checks, failed);
    check_int(name + " lowest", expected.lowest, actual.lowest, checks, failed);
    check_int(name + " highest", expected.highest, actual.highest, checks, failed);
}

int main() {
    int checks{0};
    int failed{0};

    std::istringstream input_d1{"21.5"};
    int temperature_d1{777};
    check_reading("D1 result", Reading::measured, read_measurement(input_d1, temperature_d1), checks, failed);
    check_int("D1 temperature", 21, temperature_d1, checks, failed);

    std::istringstream input_d2{"-50"};
    int temperature_d2{777};
    check_reading("D2 result", Reading::measured, read_measurement(input_d2, temperature_d2), checks, failed);
    check_int("D2 temperature", -50, temperature_d2, checks, failed);

    std::istringstream input_d3{"-51"};
    int temperature_d3{777};
    check_reading("D3 result", Reading::out_of_range, read_measurement(input_d3, temperature_d3), checks, failed);
    check_int("D3 temperature", 777, temperature_d3, checks, failed);

    std::istringstream input_d4{"50"};
    int temperature_d4{777};
    check_reading("D4 result", Reading::measured, read_measurement(input_d4, temperature_d4), checks, failed);
    check_int("D4 temperature", 50, temperature_d4, checks, failed);

    std::istringstream input_d5{"51"};
    int temperature_d5{777};
    check_reading("D5 result", Reading::out_of_range, read_measurement(input_d5, temperature_d5), checks, failed);
    check_int("D5 temperature", 777, temperature_d5, checks, failed);

    std::istringstream input_d6{"99"};
    int temperature_d6{777};
    check_reading("D6 result", Reading::out_of_range, read_measurement(input_d6, temperature_d6), checks, failed);
    check_int("D6 temperature", 777, temperature_d6, checks, failed);

    std::istringstream input_d7{"100"};
    int temperature_d7{777};
    check_reading("D7 result", Reading::invalid_entry, read_measurement(input_d7, temperature_d7), checks, failed);
    check_int("D7 temperature", 777, temperature_d7, checks, failed);

    std::istringstream input_d8{"-99"};
    int temperature_d8{777};
    check_reading("D8 result", Reading::out_of_range, read_measurement(input_d8, temperature_d8), checks, failed);
    check_int("D8 temperature", 777, temperature_d8, checks, failed);

    std::istringstream input_d9{"-100"};
    int temperature_d9{777};
    check_reading("D9 result", Reading::invalid_entry, read_measurement(input_d9, temperature_d9), checks, failed);
    check_int("D9 temperature", 777, temperature_d9, checks, failed);

    std::istringstream input_d10{"abc"};
    int temperature_d10{777};
    check_reading("D10 result", Reading::invalid_entry, read_measurement(input_d10, temperature_d10), checks, failed);
    check_int("D10 temperature", 777, temperature_d10, checks, failed);

    std::istringstream input_d11{"0"};
    int temperature_d11{777};
    check_reading("D11 result", Reading::measured, read_measurement(input_d11, temperature_d11), checks, failed);
    check_int("D11 temperature", 0, temperature_d11, checks, failed);

    std::istringstream input_d12{""};
    int temperature_d12{777};
    check_reading("D12 result", Reading::end_of_data, read_measurement(input_d12, temperature_d12), checks, failed);
    check_int("D12 temperature", 777, temperature_d12, checks, failed);

    std::istringstream input_c1{"21\n18\n25\n30\n"};
    const StationReport report_c1{collect_measurements(input_c1, 3)};
    check_report("C1", StationReport{3, 0, 0, 18, 25}, report_c1, checks, failed);
    int next_c1{777};
    check_reading("C1 next result", Reading::measured, read_measurement(input_c1, next_c1), checks, failed);
    check_int("C1 next temperature", 30, next_c1, checks, failed);

    std::istringstream input_c2{"21\n\n60\nabc\n19 C\n"};
    const StationReport report_c2{collect_measurements(input_c2, 5)};
    check_report("C2", StationReport{2, 1, 1, 19, 21}, report_c2, checks, failed);

    std::istringstream input_c3{"abc\nxyz\n-5"};
    const StationReport report_c3{collect_measurements(input_c3, 4)};
    check_report("C3", StationReport{1, 0, 2, -5, -5}, report_c3, checks, failed);

    std::istringstream input_c4{""};
    const StationReport report_c4{collect_measurements(input_c4, 3)};
    check_report("C4", StationReport{0, 0, 0, 0, 0}, report_c4, checks, failed);

    std::istringstream input_c5{"15\nerr"};
    const StationReport report_c5{collect_measurements(input_c5, 4)};
    check_report("C5", StationReport{1, 0, 1, 15, 15}, report_c5, checks, failed);

    std::istringstream input_c6{"60\n70\n-3\n-12\n8\n"};
    const StationReport report_c6{collect_measurements(input_c6, 2)};
    check_report("C6", StationReport{2, 2, 0, -12, -3}, report_c6, checks, failed);
    int next_c6{777};
    check_reading("C6 next result", Reading::measured, read_measurement(input_c6, next_c6), checks, failed);
    check_int("C6 next temperature", 8, next_c6, checks, failed);

    std::istringstream input_c7{"0\n5"};
    const StationReport report_c7{collect_measurements(input_c7, 3)};
    check_report("C7", StationReport{2, 0, 0, 0, 5}, report_c7, checks, failed);

    std::istringstream input_c8{"60\nabc\n99999999999"};
    const StationReport report_c8{collect_measurements(input_c8, 3)};
    check_report("C8", StationReport{0, 1, 2, 0, 0}, report_c8, checks, failed);

    std::cout << "Checks: " << checks << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }
}
```

**`CMakeLists.txt`**:

<!-- cmake: station_given -->
```cmake
cmake_minimum_required(VERSION 3.28)
project(first_program LANGUAGES CXX)

add_executable(first_program main.cpp rules.cpp)
target_compile_features(first_program PRIVATE cxx_std_20)
set_target_properties(first_program PROPERTIES CXX_EXTENSIONS OFF)

add_executable(function_tests function_tests.cpp rules.cpp)
target_compile_features(function_tests PRIVATE cxx_std_20)
set_target_properties(function_tests PROPERTIES CXX_EXTENSIONS OFF)
```

**Before the fix**, with the supplied code, `function_tests` prints:

<!-- output: station_given -->
```text
PASS D1 result
PASS D1 temperature
PASS D2 result
PASS D2 temperature
PASS D3 result
PASS D3 temperature
PASS D4 result
PASS D4 temperature
PASS D5 result
PASS D5 temperature
PASS D6 result
PASS D6 temperature
FAIL D7 result: expected invalid_entry, actual out_of_range
PASS D7 temperature
PASS D8 result
PASS D8 temperature
FAIL D9 result: expected invalid_entry, actual out_of_range
PASS D9 temperature
PASS D10 result
PASS D10 temperature
PASS D11 result
PASS D11 temperature
PASS D12 result
PASS D12 temperature
PASS C1 measured
PASS C1 out_of_range
PASS C1 invalid_entries
PASS C1 lowest
PASS C1 highest
PASS C1 next result
PASS C1 next temperature
PASS C2 measured
PASS C2 out_of_range
PASS C2 invalid_entries
PASS C2 lowest
PASS C2 highest
PASS C3 measured
PASS C3 out_of_range
PASS C3 invalid_entries
PASS C3 lowest
PASS C3 highest
PASS C4 measured
PASS C4 out_of_range
PASS C4 invalid_entries
PASS C4 lowest
PASS C4 highest
PASS C5 measured
PASS C5 out_of_range
PASS C5 invalid_entries
PASS C5 lowest
PASS C5 highest
PASS C6 measured
PASS C6 out_of_range
PASS C6 invalid_entries
PASS C6 lowest
PASS C6 highest
PASS C6 next result
PASS C6 next temperature
PASS C7 measured
PASS C7 out_of_range
PASS C7 invalid_entries
PASS C7 lowest
PASS C7 highest
PASS C8 measured
PASS C8 out_of_range
PASS C8 invalid_entries
PASS C8 lowest
PASS C8 highest
Checks: 68, failed: 2
```

Exit code: 1. This is **a test that detects an error**: the test program works correctly, and exit code 1 comes from the two failed checks.

- **Which cases:** D7 (`100`) and D9 (`-100`), the numbers just past the bounds of the protocol's range. Neither is a valid message of the simulator, so the contract requires `invalid_entry`, and the function returns `out_of_range`. `temperature` stays 777, so the checks of `temperature` pass.
- **The cause:** in `read_measurement`, in the `switch` over the result of `read_number`, the label `ReadResult::out_of_range` returns `Reading::out_of_range`. Here `read_number` refuses because of the **protocol's** range, so by the contract it's a bad entry. The error is in the function, because the expected results agree with the table of results.
- **Why the others pass:** numbers in the protocol's range, D6 (`99`) and D8 (`-99`) among them, get through `read_number` and get the right result from the check of the station's range. An entry with no number gives `invalid_input`, that is `invalid_entry`, regardless of the bug. That's why a test set that checks a bad entry only with `abc` won't detect this bug: it needs the pair 99 and 100.
- **The application program** with the data of the example works correctly too: they contain no number outside the protocol's range.

**The fix:** one change in `rules.cpp`. In the label `case ReadResult::out_of_range:`, it has to be `return Reading::invalid_entry;`. The test program, the expected results, `main.cpp` and `CMakeLists.txt` don't change.

</details>

<details>
<summary>All the files of the project after the fix</summary>

They differ from the previous ones only in one line of `rules.cpp`.

**`main.cpp`**:

<!-- example: station_fixed target=function_tests -->
```cpp
#include <iostream>

#include "rules.hpp"

int main() {
    const int limit{6};
    const StationReport report{collect_measurements(std::cin, limit)};

    std::cout << "Measurements: " << report.measured << " of " << limit << "\n";

    if (report.measured > 0) {
        std::cout << "Lowest: " << report.lowest << "\n";
        std::cout << "Highest: " << report.highest << "\n";
    } else {
        std::cout << "No measurements\n";
    }

    std::cout << "Out of range: " << report.out_of_range << "\n";
    std::cout << "Invalid entries: " << report.invalid_entries << "\n";
}
```

**`rules.hpp`**:

<!-- file: station_fixed rules.hpp -->
```cpp
#pragma once

#include <istream>

enum class ReadResult {
    accepted,
    out_of_range,
    invalid_input,
    end_of_input
};

void discard_rest_of_line(std::istream& input);
ReadResult read_number(std::istream& input, int minimum, int maximum, int& result);

enum class Reading {
    measured,
    out_of_range,
    invalid_entry,
    end_of_data
};

Reading read_measurement(std::istream& input, int& temperature);

struct StationReport {
    int measured;
    int out_of_range;
    int invalid_entries;
    int lowest;
    int highest;
};

StationReport collect_measurements(std::istream& input, int limit);
```

**`rules.cpp`**:

<!-- file: station_fixed rules.cpp -->
```cpp
#include "rules.hpp"

#include <limits>

void discard_rest_of_line(std::istream& input) {
    input.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
}

ReadResult read_number(std::istream& input, int minimum, int maximum, int& result) {
    if (input.bad()) {
        return ReadResult::end_of_input;
    }

    input >> std::ws;

    if (input.eof()) {
        return ReadResult::end_of_input;
    }

    int value{0};
    input >> value;

    if (input.fail()) {
        if (input.bad()) {
            return ReadResult::end_of_input;
        }

        input.clear();
        discard_rest_of_line(input);
        return ReadResult::invalid_input;
    }

    discard_rest_of_line(input);

    if (value < minimum || value > maximum) {
        return ReadResult::out_of_range;
    }

    result = value;
    return ReadResult::accepted;
}

Reading read_measurement(std::istream& input, int& temperature) {
    int value{0};
    const ReadResult result{read_number(input, -99, 99, value)};

    switch (result) {
        case ReadResult::accepted:
            break;
        case ReadResult::out_of_range:
            return Reading::invalid_entry;
        case ReadResult::invalid_input:
            return Reading::invalid_entry;
        case ReadResult::end_of_input:
            return Reading::end_of_data;
    }

    if (value < -50 || value > 50) {
        return Reading::out_of_range;
    }

    temperature = value;
    return Reading::measured;
}

StationReport collect_measurements(std::istream& input, int limit) {
    StationReport report{0, 0, 0, 0, 0};
    int temperature{0};
    bool input_ended{false};

    while (report.measured < limit && !input_ended) {
        const Reading reading{read_measurement(input, temperature)};

        switch (reading) {
            case Reading::measured:
                if (report.measured == 0) {
                    report.lowest = temperature;
                    report.highest = temperature;
                } else if (temperature < report.lowest) {
                    report.lowest = temperature;
                } else if (temperature > report.highest) {
                    report.highest = temperature;
                }

                ++report.measured;
                break;
            case Reading::out_of_range:
                ++report.out_of_range;
                break;
            case Reading::invalid_entry:
                ++report.invalid_entries;
                break;
            case Reading::end_of_data:
                input_ended = true;
                break;
        }
    }

    return report;
}
```

**`function_tests.cpp`**, unchanged:

<!-- file: station_fixed function_tests.cpp -->
```cpp
#include <iostream>
#include <sstream>
#include <string>

#include "rules.hpp"

std::string reading_text(Reading reading) {
    switch (reading) {
        case Reading::measured:
            return "measured";
        case Reading::out_of_range:
            return "out_of_range";
        case Reading::invalid_entry:
            return "invalid_entry";
        case Reading::end_of_data:
            return "end_of_data";
    }

    return "unknown";
}

void check_reading(const std::string& name, Reading expected, Reading actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << reading_text(expected) << ", actual " << reading_text(actual) << "\n";
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

void check_report(const std::string& name, const StationReport& expected, const StationReport& actual, int& checks, int& failed) {
    check_int(name + " measured", expected.measured, actual.measured, checks, failed);
    check_int(name + " out_of_range", expected.out_of_range, actual.out_of_range, checks, failed);
    check_int(name + " invalid_entries", expected.invalid_entries, actual.invalid_entries, checks, failed);
    check_int(name + " lowest", expected.lowest, actual.lowest, checks, failed);
    check_int(name + " highest", expected.highest, actual.highest, checks, failed);
}

int main() {
    int checks{0};
    int failed{0};

    std::istringstream input_d1{"21.5"};
    int temperature_d1{777};
    check_reading("D1 result", Reading::measured, read_measurement(input_d1, temperature_d1), checks, failed);
    check_int("D1 temperature", 21, temperature_d1, checks, failed);

    std::istringstream input_d2{"-50"};
    int temperature_d2{777};
    check_reading("D2 result", Reading::measured, read_measurement(input_d2, temperature_d2), checks, failed);
    check_int("D2 temperature", -50, temperature_d2, checks, failed);

    std::istringstream input_d3{"-51"};
    int temperature_d3{777};
    check_reading("D3 result", Reading::out_of_range, read_measurement(input_d3, temperature_d3), checks, failed);
    check_int("D3 temperature", 777, temperature_d3, checks, failed);

    std::istringstream input_d4{"50"};
    int temperature_d4{777};
    check_reading("D4 result", Reading::measured, read_measurement(input_d4, temperature_d4), checks, failed);
    check_int("D4 temperature", 50, temperature_d4, checks, failed);

    std::istringstream input_d5{"51"};
    int temperature_d5{777};
    check_reading("D5 result", Reading::out_of_range, read_measurement(input_d5, temperature_d5), checks, failed);
    check_int("D5 temperature", 777, temperature_d5, checks, failed);

    std::istringstream input_d6{"99"};
    int temperature_d6{777};
    check_reading("D6 result", Reading::out_of_range, read_measurement(input_d6, temperature_d6), checks, failed);
    check_int("D6 temperature", 777, temperature_d6, checks, failed);

    std::istringstream input_d7{"100"};
    int temperature_d7{777};
    check_reading("D7 result", Reading::invalid_entry, read_measurement(input_d7, temperature_d7), checks, failed);
    check_int("D7 temperature", 777, temperature_d7, checks, failed);

    std::istringstream input_d8{"-99"};
    int temperature_d8{777};
    check_reading("D8 result", Reading::out_of_range, read_measurement(input_d8, temperature_d8), checks, failed);
    check_int("D8 temperature", 777, temperature_d8, checks, failed);

    std::istringstream input_d9{"-100"};
    int temperature_d9{777};
    check_reading("D9 result", Reading::invalid_entry, read_measurement(input_d9, temperature_d9), checks, failed);
    check_int("D9 temperature", 777, temperature_d9, checks, failed);

    std::istringstream input_d10{"abc"};
    int temperature_d10{777};
    check_reading("D10 result", Reading::invalid_entry, read_measurement(input_d10, temperature_d10), checks, failed);
    check_int("D10 temperature", 777, temperature_d10, checks, failed);

    std::istringstream input_d11{"0"};
    int temperature_d11{777};
    check_reading("D11 result", Reading::measured, read_measurement(input_d11, temperature_d11), checks, failed);
    check_int("D11 temperature", 0, temperature_d11, checks, failed);

    std::istringstream input_d12{""};
    int temperature_d12{777};
    check_reading("D12 result", Reading::end_of_data, read_measurement(input_d12, temperature_d12), checks, failed);
    check_int("D12 temperature", 777, temperature_d12, checks, failed);

    std::istringstream input_c1{"21\n18\n25\n30\n"};
    const StationReport report_c1{collect_measurements(input_c1, 3)};
    check_report("C1", StationReport{3, 0, 0, 18, 25}, report_c1, checks, failed);
    int next_c1{777};
    check_reading("C1 next result", Reading::measured, read_measurement(input_c1, next_c1), checks, failed);
    check_int("C1 next temperature", 30, next_c1, checks, failed);

    std::istringstream input_c2{"21\n\n60\nabc\n19 C\n"};
    const StationReport report_c2{collect_measurements(input_c2, 5)};
    check_report("C2", StationReport{2, 1, 1, 19, 21}, report_c2, checks, failed);

    std::istringstream input_c3{"abc\nxyz\n-5"};
    const StationReport report_c3{collect_measurements(input_c3, 4)};
    check_report("C3", StationReport{1, 0, 2, -5, -5}, report_c3, checks, failed);

    std::istringstream input_c4{""};
    const StationReport report_c4{collect_measurements(input_c4, 3)};
    check_report("C4", StationReport{0, 0, 0, 0, 0}, report_c4, checks, failed);

    std::istringstream input_c5{"15\nerr"};
    const StationReport report_c5{collect_measurements(input_c5, 4)};
    check_report("C5", StationReport{1, 0, 1, 15, 15}, report_c5, checks, failed);

    std::istringstream input_c6{"60\n70\n-3\n-12\n8\n"};
    const StationReport report_c6{collect_measurements(input_c6, 2)};
    check_report("C6", StationReport{2, 2, 0, -12, -3}, report_c6, checks, failed);
    int next_c6{777};
    check_reading("C6 next result", Reading::measured, read_measurement(input_c6, next_c6), checks, failed);
    check_int("C6 next temperature", 8, next_c6, checks, failed);

    std::istringstream input_c7{"0\n5"};
    const StationReport report_c7{collect_measurements(input_c7, 3)};
    check_report("C7", StationReport{2, 0, 0, 0, 5}, report_c7, checks, failed);

    std::istringstream input_c8{"60\nabc\n99999999999"};
    const StationReport report_c8{collect_measurements(input_c8, 3)};
    check_report("C8", StationReport{0, 1, 2, 0, 0}, report_c8, checks, failed);

    std::cout << "Checks: " << checks << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }
}
```

**`CMakeLists.txt`**:

<!-- cmake: station_fixed -->
```cmake
cmake_minimum_required(VERSION 3.28)
project(first_program LANGUAGES CXX)

add_executable(first_program main.cpp rules.cpp)
target_compile_features(first_program PRIVATE cxx_std_20)
set_target_properties(first_program PROPERTIES CXX_EXTENSIONS OFF)

add_executable(function_tests function_tests.cpp rules.cpp)
target_compile_features(function_tests PRIVATE cxx_std_20)
set_target_properties(function_tests PROPERTIES CXX_EXTENSIONS OFF)
```

**After the fix**, the same tests print:

<!-- output: station_fixed -->
```text
PASS D1 result
PASS D1 temperature
PASS D2 result
PASS D2 temperature
PASS D3 result
PASS D3 temperature
PASS D4 result
PASS D4 temperature
PASS D5 result
PASS D5 temperature
PASS D6 result
PASS D6 temperature
PASS D7 result
PASS D7 temperature
PASS D8 result
PASS D8 temperature
PASS D9 result
PASS D9 temperature
PASS D10 result
PASS D10 temperature
PASS D11 result
PASS D11 temperature
PASS D12 result
PASS D12 temperature
PASS C1 measured
PASS C1 out_of_range
PASS C1 invalid_entries
PASS C1 lowest
PASS C1 highest
PASS C1 next result
PASS C1 next temperature
PASS C2 measured
PASS C2 out_of_range
PASS C2 invalid_entries
PASS C2 lowest
PASS C2 highest
PASS C3 measured
PASS C3 out_of_range
PASS C3 invalid_entries
PASS C3 lowest
PASS C3 highest
PASS C4 measured
PASS C4 out_of_range
PASS C4 invalid_entries
PASS C4 lowest
PASS C4 highest
PASS C5 measured
PASS C5 out_of_range
PASS C5 invalid_entries
PASS C5 lowest
PASS C5 highest
PASS C6 measured
PASS C6 out_of_range
PASS C6 invalid_entries
PASS C6 lowest
PASS C6 highest
PASS C6 next result
PASS C6 next temperature
PASS C7 measured
PASS C7 out_of_range
PASS C7 invalid_entries
PASS C7 lowest
PASS C7 highest
PASS C8 measured
PASS C8 out_of_range
PASS C8 invalid_entries
PASS C8 lowest
PASS C8 highest
Checks: 68, failed: 0
```

Exit code: 0. All 68 checks pass: 12 direct cases with 2 checks each, 8 scenarios with 5 each, and 2 extra calls with 2 each. The application program with the data of the example prints the report of the specification.

</details>

<details>
<summary>Part C: the change map and the tests before the change of the function</summary>

**The change map:**

| Place | Change |
|---|---|
| `rules.hpp` | `sensor_fault` in `Reading`, `sensor_faults` in `StationReport` |
| `read_measurement` | the check of the fault code before the station's range |
| `collect_measurements` | the starting report with six zeros, the label `sensor_fault` |
| `main.cpp` | the line `Sensor faults` |
| `reading_text` | the label `sensor_fault` |
| `check_report` | the check of `sensor_faults` |
| the expected reports of C1–C8 | an explicit sixth value: 0 |
| D8 | `sensor_fault` instead of `out_of_range`: the only changed old expectation, because only D8 has the entry `-99` |
| new cases | D13, C9, C10 |

`ReadResult`, `read_number` and `discard_rest_of_line` don't change.

**The label in `collect_measurements`:**

<!-- fragment -->
```cpp
            case Reading::sensor_fault:
                ++report.sensor_faults;
                break;
```

**The files after steps 2–4,** without the check of the fault code. `main.cpp` is still as in Part B:

<!-- example: station_sensor_first target=function_tests exit=1 -->
```cpp
#include <iostream>

#include "rules.hpp"

int main() {
    const int limit{6};
    const StationReport report{collect_measurements(std::cin, limit)};

    std::cout << "Measurements: " << report.measured << " of " << limit << "\n";

    if (report.measured > 0) {
        std::cout << "Lowest: " << report.lowest << "\n";
        std::cout << "Highest: " << report.highest << "\n";
    } else {
        std::cout << "No measurements\n";
    }

    std::cout << "Out of range: " << report.out_of_range << "\n";
    std::cout << "Invalid entries: " << report.invalid_entries << "\n";
}
```

**`rules.hpp`**:

<!-- file: station_sensor_first rules.hpp -->
```cpp
#pragma once

#include <istream>

enum class ReadResult {
    accepted,
    out_of_range,
    invalid_input,
    end_of_input
};

void discard_rest_of_line(std::istream& input);
ReadResult read_number(std::istream& input, int minimum, int maximum, int& result);

enum class Reading {
    measured,
    out_of_range,
    invalid_entry,
    sensor_fault,
    end_of_data
};

Reading read_measurement(std::istream& input, int& temperature);

struct StationReport {
    int measured;
    int out_of_range;
    int invalid_entries;
    int lowest;
    int highest;
    int sensor_faults;
};

StationReport collect_measurements(std::istream& input, int limit);
```

**`rules.cpp`**:

<!-- file: station_sensor_first rules.cpp -->
```cpp
#include "rules.hpp"

#include <limits>

void discard_rest_of_line(std::istream& input) {
    input.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
}

ReadResult read_number(std::istream& input, int minimum, int maximum, int& result) {
    if (input.bad()) {
        return ReadResult::end_of_input;
    }

    input >> std::ws;

    if (input.eof()) {
        return ReadResult::end_of_input;
    }

    int value{0};
    input >> value;

    if (input.fail()) {
        if (input.bad()) {
            return ReadResult::end_of_input;
        }

        input.clear();
        discard_rest_of_line(input);
        return ReadResult::invalid_input;
    }

    discard_rest_of_line(input);

    if (value < minimum || value > maximum) {
        return ReadResult::out_of_range;
    }

    result = value;
    return ReadResult::accepted;
}

Reading read_measurement(std::istream& input, int& temperature) {
    int value{0};
    const ReadResult result{read_number(input, -99, 99, value)};

    switch (result) {
        case ReadResult::accepted:
            break;
        case ReadResult::out_of_range:
            return Reading::invalid_entry;
        case ReadResult::invalid_input:
            return Reading::invalid_entry;
        case ReadResult::end_of_input:
            return Reading::end_of_data;
    }

    if (value < -50 || value > 50) {
        return Reading::out_of_range;
    }

    temperature = value;
    return Reading::measured;
}

StationReport collect_measurements(std::istream& input, int limit) {
    StationReport report{0, 0, 0, 0, 0, 0};
    int temperature{0};
    bool input_ended{false};

    while (report.measured < limit && !input_ended) {
        const Reading reading{read_measurement(input, temperature)};

        switch (reading) {
            case Reading::measured:
                if (report.measured == 0) {
                    report.lowest = temperature;
                    report.highest = temperature;
                } else if (temperature < report.lowest) {
                    report.lowest = temperature;
                } else if (temperature > report.highest) {
                    report.highest = temperature;
                }

                ++report.measured;
                break;
            case Reading::out_of_range:
                ++report.out_of_range;
                break;
            case Reading::invalid_entry:
                ++report.invalid_entries;
                break;
            case Reading::sensor_fault:
                ++report.sensor_faults;
                break;
            case Reading::end_of_data:
                input_ended = true;
                break;
        }
    }

    return report;
}
```

**`function_tests.cpp`**, the cases D1–D13 and C1–C10:

<!-- file: station_sensor_first function_tests.cpp -->
```cpp
#include <iostream>
#include <sstream>
#include <string>

#include "rules.hpp"

std::string reading_text(Reading reading) {
    switch (reading) {
        case Reading::measured:
            return "measured";
        case Reading::out_of_range:
            return "out_of_range";
        case Reading::invalid_entry:
            return "invalid_entry";
        case Reading::sensor_fault:
            return "sensor_fault";
        case Reading::end_of_data:
            return "end_of_data";
    }

    return "unknown";
}

void check_reading(const std::string& name, Reading expected, Reading actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << reading_text(expected) << ", actual " << reading_text(actual) << "\n";
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

void check_report(const std::string& name, const StationReport& expected, const StationReport& actual, int& checks, int& failed) {
    check_int(name + " measured", expected.measured, actual.measured, checks, failed);
    check_int(name + " out_of_range", expected.out_of_range, actual.out_of_range, checks, failed);
    check_int(name + " invalid_entries", expected.invalid_entries, actual.invalid_entries, checks, failed);
    check_int(name + " lowest", expected.lowest, actual.lowest, checks, failed);
    check_int(name + " highest", expected.highest, actual.highest, checks, failed);
    check_int(name + " sensor_faults", expected.sensor_faults, actual.sensor_faults, checks, failed);
}

int main() {
    int checks{0};
    int failed{0};

    std::istringstream input_d1{"21.5"};
    int temperature_d1{777};
    check_reading("D1 result", Reading::measured, read_measurement(input_d1, temperature_d1), checks, failed);
    check_int("D1 temperature", 21, temperature_d1, checks, failed);

    std::istringstream input_d2{"-50"};
    int temperature_d2{777};
    check_reading("D2 result", Reading::measured, read_measurement(input_d2, temperature_d2), checks, failed);
    check_int("D2 temperature", -50, temperature_d2, checks, failed);

    std::istringstream input_d3{"-51"};
    int temperature_d3{777};
    check_reading("D3 result", Reading::out_of_range, read_measurement(input_d3, temperature_d3), checks, failed);
    check_int("D3 temperature", 777, temperature_d3, checks, failed);

    std::istringstream input_d4{"50"};
    int temperature_d4{777};
    check_reading("D4 result", Reading::measured, read_measurement(input_d4, temperature_d4), checks, failed);
    check_int("D4 temperature", 50, temperature_d4, checks, failed);

    std::istringstream input_d5{"51"};
    int temperature_d5{777};
    check_reading("D5 result", Reading::out_of_range, read_measurement(input_d5, temperature_d5), checks, failed);
    check_int("D5 temperature", 777, temperature_d5, checks, failed);

    std::istringstream input_d6{"99"};
    int temperature_d6{777};
    check_reading("D6 result", Reading::out_of_range, read_measurement(input_d6, temperature_d6), checks, failed);
    check_int("D6 temperature", 777, temperature_d6, checks, failed);

    std::istringstream input_d7{"100"};
    int temperature_d7{777};
    check_reading("D7 result", Reading::invalid_entry, read_measurement(input_d7, temperature_d7), checks, failed);
    check_int("D7 temperature", 777, temperature_d7, checks, failed);

    std::istringstream input_d8{"-99"};
    int temperature_d8{777};
    check_reading("D8 result", Reading::sensor_fault, read_measurement(input_d8, temperature_d8), checks, failed);
    check_int("D8 temperature", 777, temperature_d8, checks, failed);

    std::istringstream input_d9{"-100"};
    int temperature_d9{777};
    check_reading("D9 result", Reading::invalid_entry, read_measurement(input_d9, temperature_d9), checks, failed);
    check_int("D9 temperature", 777, temperature_d9, checks, failed);

    std::istringstream input_d10{"abc"};
    int temperature_d10{777};
    check_reading("D10 result", Reading::invalid_entry, read_measurement(input_d10, temperature_d10), checks, failed);
    check_int("D10 temperature", 777, temperature_d10, checks, failed);

    std::istringstream input_d11{"0"};
    int temperature_d11{777};
    check_reading("D11 result", Reading::measured, read_measurement(input_d11, temperature_d11), checks, failed);
    check_int("D11 temperature", 0, temperature_d11, checks, failed);

    std::istringstream input_d12{""};
    int temperature_d12{777};
    check_reading("D12 result", Reading::end_of_data, read_measurement(input_d12, temperature_d12), checks, failed);
    check_int("D12 temperature", 777, temperature_d12, checks, failed);

    std::istringstream input_d13{"-98"};
    int temperature_d13{777};
    check_reading("D13 result", Reading::out_of_range, read_measurement(input_d13, temperature_d13), checks, failed);
    check_int("D13 temperature", 777, temperature_d13, checks, failed);

    std::istringstream input_c1{"21\n18\n25\n30\n"};
    const StationReport report_c1{collect_measurements(input_c1, 3)};
    check_report("C1", StationReport{3, 0, 0, 18, 25, 0}, report_c1, checks, failed);
    int next_c1{777};
    check_reading("C1 next result", Reading::measured, read_measurement(input_c1, next_c1), checks, failed);
    check_int("C1 next temperature", 30, next_c1, checks, failed);

    std::istringstream input_c2{"21\n\n60\nabc\n19 C\n"};
    const StationReport report_c2{collect_measurements(input_c2, 5)};
    check_report("C2", StationReport{2, 1, 1, 19, 21, 0}, report_c2, checks, failed);

    std::istringstream input_c3{"abc\nxyz\n-5"};
    const StationReport report_c3{collect_measurements(input_c3, 4)};
    check_report("C3", StationReport{1, 0, 2, -5, -5, 0}, report_c3, checks, failed);

    std::istringstream input_c4{""};
    const StationReport report_c4{collect_measurements(input_c4, 3)};
    check_report("C4", StationReport{0, 0, 0, 0, 0, 0}, report_c4, checks, failed);

    std::istringstream input_c5{"15\nerr"};
    const StationReport report_c5{collect_measurements(input_c5, 4)};
    check_report("C5", StationReport{1, 0, 1, 15, 15, 0}, report_c5, checks, failed);

    std::istringstream input_c6{"60\n70\n-3\n-12\n8\n"};
    const StationReport report_c6{collect_measurements(input_c6, 2)};
    check_report("C6", StationReport{2, 2, 0, -12, -3, 0}, report_c6, checks, failed);
    int next_c6{777};
    check_reading("C6 next result", Reading::measured, read_measurement(input_c6, next_c6), checks, failed);
    check_int("C6 next temperature", 8, next_c6, checks, failed);

    std::istringstream input_c7{"0\n5"};
    const StationReport report_c7{collect_measurements(input_c7, 3)};
    check_report("C7", StationReport{2, 0, 0, 0, 5, 0}, report_c7, checks, failed);

    std::istringstream input_c8{"60\nabc\n99999999999"};
    const StationReport report_c8{collect_measurements(input_c8, 3)};
    check_report("C8", StationReport{0, 1, 2, 0, 0, 0}, report_c8, checks, failed);

    std::istringstream input_c9{"21\n-99\n22\n23\n"};
    const StationReport report_c9{collect_measurements(input_c9, 2)};
    check_report("C9", StationReport{2, 0, 0, 21, 22, 1}, report_c9, checks, failed);
    int next_c9{777};
    check_reading("C9 next result", Reading::measured, read_measurement(input_c9, next_c9), checks, failed);
    check_int("C9 next temperature", 23, next_c9, checks, failed);

    std::istringstream input_c10{"-99\n-99"};
    const StationReport report_c10{collect_measurements(input_c10, 1)};
    check_report("C10", StationReport{0, 0, 0, 0, 0, 2}, report_c10, checks, failed);

    std::cout << "Checks: " << checks << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }
}
```

**`CMakeLists.txt`**:

<!-- cmake: station_sensor_first -->
```cmake
cmake_minimum_required(VERSION 3.28)
project(first_program LANGUAGES CXX)

add_executable(first_program main.cpp rules.cpp)
target_compile_features(first_program PRIVATE cxx_std_20)
set_target_properties(first_program PROPERTIES CXX_EXTENSIONS OFF)

add_executable(function_tests function_tests.cpp rules.cpp)
target_compile_features(function_tests PRIVATE cxx_std_20)
set_target_properties(function_tests PROPERTIES CXX_EXTENSIONS OFF)
```

**The fourth run**, before the change of `read_measurement`:

<!-- output: station_sensor_first -->
```text
PASS D1 result
PASS D1 temperature
PASS D2 result
PASS D2 temperature
PASS D3 result
PASS D3 temperature
PASS D4 result
PASS D4 temperature
PASS D5 result
PASS D5 temperature
PASS D6 result
PASS D6 temperature
PASS D7 result
PASS D7 temperature
FAIL D8 result: expected sensor_fault, actual out_of_range
PASS D8 temperature
PASS D9 result
PASS D9 temperature
PASS D10 result
PASS D10 temperature
PASS D11 result
PASS D11 temperature
PASS D12 result
PASS D12 temperature
PASS D13 result
PASS D13 temperature
PASS C1 measured
PASS C1 out_of_range
PASS C1 invalid_entries
PASS C1 lowest
PASS C1 highest
PASS C1 sensor_faults
PASS C1 next result
PASS C1 next temperature
PASS C2 measured
PASS C2 out_of_range
PASS C2 invalid_entries
PASS C2 lowest
PASS C2 highest
PASS C2 sensor_faults
PASS C3 measured
PASS C3 out_of_range
PASS C3 invalid_entries
PASS C3 lowest
PASS C3 highest
PASS C3 sensor_faults
PASS C4 measured
PASS C4 out_of_range
PASS C4 invalid_entries
PASS C4 lowest
PASS C4 highest
PASS C4 sensor_faults
PASS C5 measured
PASS C5 out_of_range
PASS C5 invalid_entries
PASS C5 lowest
PASS C5 highest
PASS C5 sensor_faults
PASS C6 measured
PASS C6 out_of_range
PASS C6 invalid_entries
PASS C6 lowest
PASS C6 highest
PASS C6 sensor_faults
PASS C6 next result
PASS C6 next temperature
PASS C7 measured
PASS C7 out_of_range
PASS C7 invalid_entries
PASS C7 lowest
PASS C7 highest
PASS C7 sensor_faults
PASS C8 measured
PASS C8 out_of_range
PASS C8 invalid_entries
PASS C8 lowest
PASS C8 highest
PASS C8 sensor_faults
PASS C9 measured
FAIL C9 out_of_range: expected 0, actual 1
PASS C9 invalid_entries
PASS C9 lowest
PASS C9 highest
FAIL C9 sensor_faults: expected 1, actual 0
PASS C9 next result
PASS C9 next temperature
PASS C10 measured
FAIL C10 out_of_range: expected 0, actual 2
PASS C10 invalid_entries
PASS C10 lowest
PASS C10 highest
FAIL C10 sensor_faults: expected 2, actual 0
Checks: 92, failed: 5
```

Exit code: 1. Five checks describe a fault that the function doesn't recognise yet:

- **D8 result:** −99 gets through `read_number`, and then the check of the station's range gives `out_of_range`.
- **C9 and C10:** each fault is counted in `out_of_range`, and `sensor_faults` stays 0.
- **What passes:** the old cases with the explicit sixth value 0, D13, and the checks of `temperature`: after −99 it's still 777. In C9 the limit works too: the fault, counted here as a refusal, doesn't use it up, so `measured`, `lowest`, `highest` and the next call agree.

</details>

<details>
<summary>Part C completed</summary>

In `read_measurement`, the check of the fault code comes before the check of the station's range:

<!-- fragment -->
```cpp
    if (value == -99) {
        return Reading::sensor_fault;
    }

    if (value < -50 || value > 50) {
        return Reading::out_of_range;
    }
```

If it came after it, −99 would still give `out_of_range`: D8, C9 and C10 would detect it.

**`main.cpp`**, with the line `Sensor faults`:

<!-- example: station_sensor target=function_tests -->
```cpp
#include <iostream>

#include "rules.hpp"

int main() {
    const int limit{6};
    const StationReport report{collect_measurements(std::cin, limit)};

    std::cout << "Measurements: " << report.measured << " of " << limit << "\n";

    if (report.measured > 0) {
        std::cout << "Lowest: " << report.lowest << "\n";
        std::cout << "Highest: " << report.highest << "\n";
    } else {
        std::cout << "No measurements\n";
    }

    std::cout << "Out of range: " << report.out_of_range << "\n";
    std::cout << "Invalid entries: " << report.invalid_entries << "\n";
    std::cout << "Sensor faults: " << report.sensor_faults << "\n";
}
```

**`rules.hpp`**:

<!-- file: station_sensor rules.hpp -->
```cpp
#pragma once

#include <istream>

enum class ReadResult {
    accepted,
    out_of_range,
    invalid_input,
    end_of_input
};

void discard_rest_of_line(std::istream& input);
ReadResult read_number(std::istream& input, int minimum, int maximum, int& result);

enum class Reading {
    measured,
    out_of_range,
    invalid_entry,
    sensor_fault,
    end_of_data
};

Reading read_measurement(std::istream& input, int& temperature);

struct StationReport {
    int measured;
    int out_of_range;
    int invalid_entries;
    int lowest;
    int highest;
    int sensor_faults;
};

StationReport collect_measurements(std::istream& input, int limit);
```

**`rules.cpp`**:

<!-- file: station_sensor rules.cpp -->
```cpp
#include "rules.hpp"

#include <limits>

void discard_rest_of_line(std::istream& input) {
    input.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
}

ReadResult read_number(std::istream& input, int minimum, int maximum, int& result) {
    if (input.bad()) {
        return ReadResult::end_of_input;
    }

    input >> std::ws;

    if (input.eof()) {
        return ReadResult::end_of_input;
    }

    int value{0};
    input >> value;

    if (input.fail()) {
        if (input.bad()) {
            return ReadResult::end_of_input;
        }

        input.clear();
        discard_rest_of_line(input);
        return ReadResult::invalid_input;
    }

    discard_rest_of_line(input);

    if (value < minimum || value > maximum) {
        return ReadResult::out_of_range;
    }

    result = value;
    return ReadResult::accepted;
}

Reading read_measurement(std::istream& input, int& temperature) {
    int value{0};
    const ReadResult result{read_number(input, -99, 99, value)};

    switch (result) {
        case ReadResult::accepted:
            break;
        case ReadResult::out_of_range:
            return Reading::invalid_entry;
        case ReadResult::invalid_input:
            return Reading::invalid_entry;
        case ReadResult::end_of_input:
            return Reading::end_of_data;
    }

    if (value == -99) {
        return Reading::sensor_fault;
    }

    if (value < -50 || value > 50) {
        return Reading::out_of_range;
    }

    temperature = value;
    return Reading::measured;
}

StationReport collect_measurements(std::istream& input, int limit) {
    StationReport report{0, 0, 0, 0, 0, 0};
    int temperature{0};
    bool input_ended{false};

    while (report.measured < limit && !input_ended) {
        const Reading reading{read_measurement(input, temperature)};

        switch (reading) {
            case Reading::measured:
                if (report.measured == 0) {
                    report.lowest = temperature;
                    report.highest = temperature;
                } else if (temperature < report.lowest) {
                    report.lowest = temperature;
                } else if (temperature > report.highest) {
                    report.highest = temperature;
                }

                ++report.measured;
                break;
            case Reading::out_of_range:
                ++report.out_of_range;
                break;
            case Reading::invalid_entry:
                ++report.invalid_entries;
                break;
            case Reading::sensor_fault:
                ++report.sensor_faults;
                break;
            case Reading::end_of_data:
                input_ended = true;
                break;
        }
    }

    return report;
}
```

**`function_tests.cpp`**, unchanged since the fourth run:

<!-- file: station_sensor function_tests.cpp -->
```cpp
#include <iostream>
#include <sstream>
#include <string>

#include "rules.hpp"

std::string reading_text(Reading reading) {
    switch (reading) {
        case Reading::measured:
            return "measured";
        case Reading::out_of_range:
            return "out_of_range";
        case Reading::invalid_entry:
            return "invalid_entry";
        case Reading::sensor_fault:
            return "sensor_fault";
        case Reading::end_of_data:
            return "end_of_data";
    }

    return "unknown";
}

void check_reading(const std::string& name, Reading expected, Reading actual, int& checks, int& failed) {
    ++checks;

    if (actual == expected) {
        std::cout << "PASS " << name << "\n";
    } else {
        std::cout << "FAIL " << name << ": expected " << reading_text(expected) << ", actual " << reading_text(actual) << "\n";
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

void check_report(const std::string& name, const StationReport& expected, const StationReport& actual, int& checks, int& failed) {
    check_int(name + " measured", expected.measured, actual.measured, checks, failed);
    check_int(name + " out_of_range", expected.out_of_range, actual.out_of_range, checks, failed);
    check_int(name + " invalid_entries", expected.invalid_entries, actual.invalid_entries, checks, failed);
    check_int(name + " lowest", expected.lowest, actual.lowest, checks, failed);
    check_int(name + " highest", expected.highest, actual.highest, checks, failed);
    check_int(name + " sensor_faults", expected.sensor_faults, actual.sensor_faults, checks, failed);
}

int main() {
    int checks{0};
    int failed{0};

    std::istringstream input_d1{"21.5"};
    int temperature_d1{777};
    check_reading("D1 result", Reading::measured, read_measurement(input_d1, temperature_d1), checks, failed);
    check_int("D1 temperature", 21, temperature_d1, checks, failed);

    std::istringstream input_d2{"-50"};
    int temperature_d2{777};
    check_reading("D2 result", Reading::measured, read_measurement(input_d2, temperature_d2), checks, failed);
    check_int("D2 temperature", -50, temperature_d2, checks, failed);

    std::istringstream input_d3{"-51"};
    int temperature_d3{777};
    check_reading("D3 result", Reading::out_of_range, read_measurement(input_d3, temperature_d3), checks, failed);
    check_int("D3 temperature", 777, temperature_d3, checks, failed);

    std::istringstream input_d4{"50"};
    int temperature_d4{777};
    check_reading("D4 result", Reading::measured, read_measurement(input_d4, temperature_d4), checks, failed);
    check_int("D4 temperature", 50, temperature_d4, checks, failed);

    std::istringstream input_d5{"51"};
    int temperature_d5{777};
    check_reading("D5 result", Reading::out_of_range, read_measurement(input_d5, temperature_d5), checks, failed);
    check_int("D5 temperature", 777, temperature_d5, checks, failed);

    std::istringstream input_d6{"99"};
    int temperature_d6{777};
    check_reading("D6 result", Reading::out_of_range, read_measurement(input_d6, temperature_d6), checks, failed);
    check_int("D6 temperature", 777, temperature_d6, checks, failed);

    std::istringstream input_d7{"100"};
    int temperature_d7{777};
    check_reading("D7 result", Reading::invalid_entry, read_measurement(input_d7, temperature_d7), checks, failed);
    check_int("D7 temperature", 777, temperature_d7, checks, failed);

    std::istringstream input_d8{"-99"};
    int temperature_d8{777};
    check_reading("D8 result", Reading::sensor_fault, read_measurement(input_d8, temperature_d8), checks, failed);
    check_int("D8 temperature", 777, temperature_d8, checks, failed);

    std::istringstream input_d9{"-100"};
    int temperature_d9{777};
    check_reading("D9 result", Reading::invalid_entry, read_measurement(input_d9, temperature_d9), checks, failed);
    check_int("D9 temperature", 777, temperature_d9, checks, failed);

    std::istringstream input_d10{"abc"};
    int temperature_d10{777};
    check_reading("D10 result", Reading::invalid_entry, read_measurement(input_d10, temperature_d10), checks, failed);
    check_int("D10 temperature", 777, temperature_d10, checks, failed);

    std::istringstream input_d11{"0"};
    int temperature_d11{777};
    check_reading("D11 result", Reading::measured, read_measurement(input_d11, temperature_d11), checks, failed);
    check_int("D11 temperature", 0, temperature_d11, checks, failed);

    std::istringstream input_d12{""};
    int temperature_d12{777};
    check_reading("D12 result", Reading::end_of_data, read_measurement(input_d12, temperature_d12), checks, failed);
    check_int("D12 temperature", 777, temperature_d12, checks, failed);

    std::istringstream input_d13{"-98"};
    int temperature_d13{777};
    check_reading("D13 result", Reading::out_of_range, read_measurement(input_d13, temperature_d13), checks, failed);
    check_int("D13 temperature", 777, temperature_d13, checks, failed);

    std::istringstream input_c1{"21\n18\n25\n30\n"};
    const StationReport report_c1{collect_measurements(input_c1, 3)};
    check_report("C1", StationReport{3, 0, 0, 18, 25, 0}, report_c1, checks, failed);
    int next_c1{777};
    check_reading("C1 next result", Reading::measured, read_measurement(input_c1, next_c1), checks, failed);
    check_int("C1 next temperature", 30, next_c1, checks, failed);

    std::istringstream input_c2{"21\n\n60\nabc\n19 C\n"};
    const StationReport report_c2{collect_measurements(input_c2, 5)};
    check_report("C2", StationReport{2, 1, 1, 19, 21, 0}, report_c2, checks, failed);

    std::istringstream input_c3{"abc\nxyz\n-5"};
    const StationReport report_c3{collect_measurements(input_c3, 4)};
    check_report("C3", StationReport{1, 0, 2, -5, -5, 0}, report_c3, checks, failed);

    std::istringstream input_c4{""};
    const StationReport report_c4{collect_measurements(input_c4, 3)};
    check_report("C4", StationReport{0, 0, 0, 0, 0, 0}, report_c4, checks, failed);

    std::istringstream input_c5{"15\nerr"};
    const StationReport report_c5{collect_measurements(input_c5, 4)};
    check_report("C5", StationReport{1, 0, 1, 15, 15, 0}, report_c5, checks, failed);

    std::istringstream input_c6{"60\n70\n-3\n-12\n8\n"};
    const StationReport report_c6{collect_measurements(input_c6, 2)};
    check_report("C6", StationReport{2, 2, 0, -12, -3, 0}, report_c6, checks, failed);
    int next_c6{777};
    check_reading("C6 next result", Reading::measured, read_measurement(input_c6, next_c6), checks, failed);
    check_int("C6 next temperature", 8, next_c6, checks, failed);

    std::istringstream input_c7{"0\n5"};
    const StationReport report_c7{collect_measurements(input_c7, 3)};
    check_report("C7", StationReport{2, 0, 0, 0, 5, 0}, report_c7, checks, failed);

    std::istringstream input_c8{"60\nabc\n99999999999"};
    const StationReport report_c8{collect_measurements(input_c8, 3)};
    check_report("C8", StationReport{0, 1, 2, 0, 0, 0}, report_c8, checks, failed);

    std::istringstream input_c9{"21\n-99\n22\n23\n"};
    const StationReport report_c9{collect_measurements(input_c9, 2)};
    check_report("C9", StationReport{2, 0, 0, 21, 22, 1}, report_c9, checks, failed);
    int next_c9{777};
    check_reading("C9 next result", Reading::measured, read_measurement(input_c9, next_c9), checks, failed);
    check_int("C9 next temperature", 23, next_c9, checks, failed);

    std::istringstream input_c10{"-99\n-99"};
    const StationReport report_c10{collect_measurements(input_c10, 1)};
    check_report("C10", StationReport{0, 0, 0, 0, 0, 2}, report_c10, checks, failed);

    std::cout << "Checks: " << checks << ", failed: " << failed << "\n";

    if (failed > 0) {
        return 1;
    }
}
```

**`CMakeLists.txt`**:

<!-- cmake: station_sensor -->
```cmake
cmake_minimum_required(VERSION 3.28)
project(first_program LANGUAGES CXX)

add_executable(first_program main.cpp rules.cpp)
target_compile_features(first_program PRIVATE cxx_std_20)
set_target_properties(first_program PROPERTIES CXX_EXTENSIONS OFF)

add_executable(function_tests function_tests.cpp rules.cpp)
target_compile_features(function_tests PRIVATE cxx_std_20)
set_target_properties(function_tests PROPERTIES CXX_EXTENSIONS OFF)
```

**The fifth run:**

<!-- output: station_sensor -->
```text
PASS D1 result
PASS D1 temperature
PASS D2 result
PASS D2 temperature
PASS D3 result
PASS D3 temperature
PASS D4 result
PASS D4 temperature
PASS D5 result
PASS D5 temperature
PASS D6 result
PASS D6 temperature
PASS D7 result
PASS D7 temperature
PASS D8 result
PASS D8 temperature
PASS D9 result
PASS D9 temperature
PASS D10 result
PASS D10 temperature
PASS D11 result
PASS D11 temperature
PASS D12 result
PASS D12 temperature
PASS D13 result
PASS D13 temperature
PASS C1 measured
PASS C1 out_of_range
PASS C1 invalid_entries
PASS C1 lowest
PASS C1 highest
PASS C1 sensor_faults
PASS C1 next result
PASS C1 next temperature
PASS C2 measured
PASS C2 out_of_range
PASS C2 invalid_entries
PASS C2 lowest
PASS C2 highest
PASS C2 sensor_faults
PASS C3 measured
PASS C3 out_of_range
PASS C3 invalid_entries
PASS C3 lowest
PASS C3 highest
PASS C3 sensor_faults
PASS C4 measured
PASS C4 out_of_range
PASS C4 invalid_entries
PASS C4 lowest
PASS C4 highest
PASS C4 sensor_faults
PASS C5 measured
PASS C5 out_of_range
PASS C5 invalid_entries
PASS C5 lowest
PASS C5 highest
PASS C5 sensor_faults
PASS C6 measured
PASS C6 out_of_range
PASS C6 invalid_entries
PASS C6 lowest
PASS C6 highest
PASS C6 sensor_faults
PASS C6 next result
PASS C6 next temperature
PASS C7 measured
PASS C7 out_of_range
PASS C7 invalid_entries
PASS C7 lowest
PASS C7 highest
PASS C7 sensor_faults
PASS C8 measured
PASS C8 out_of_range
PASS C8 invalid_entries
PASS C8 lowest
PASS C8 highest
PASS C8 sensor_faults
PASS C9 measured
PASS C9 out_of_range
PASS C9 invalid_entries
PASS C9 lowest
PASS C9 highest
PASS C9 sensor_faults
PASS C9 next result
PASS C9 next temperature
PASS C10 measured
PASS C10 out_of_range
PASS C10 invalid_entries
PASS C10 lowest
PASS C10 highest
PASS C10 sensor_faults
Checks: 92, failed: 0
```

Exit code: 0. All 92 checks pass: 13 direct cases with 2 checks each, 10 scenarios with 6 each, and 3 extra calls with 2 each. The application program with the data of the example prints the same report as in Part B, and `Sensor faults: 0` at the end.

</details>

## Answers to the questions of the justification

<details>
<summary>Sample answers, for the reference solution</summary>

1. Because the contract says what the program has to do. A result taken from what the program does would repeat its error: for `100`, `out_of_range` would be written down, and the bug would go unnoticed (lesson 13.1).
2. Because both numbers lie outside the station's range and differ only in whether they fit in the protocol's range. A difference in their results can therefore come only from this rule. `abc` isn't enough: it gives `invalid_entry` another way, through a failed read, and passes with the bug too.
3. `FAIL D7 result: expected invalid_entry, actual out_of_range` shows that for `100` the actual result differs from the expected one. It doesn't decide by itself whether the error is in the function or in the expectation: that's settled by going back to the table of results (lesson 13.2).
4. Because with `measured == 0` no measurement was accepted, and `lowest` and `highest` only have placeholders. C4 and C8 check the report without measurements, and C7 and D11 check that a real 0 is a measurement.
5. Because the contract talks about the number of measurements, not of attempts: the station has to collect six temperatures, even when bad entries come up on the way. C6 checks it: with the limit 2, two refusals before the measurements can't end the collecting.
6. In Part B the contract didn't change, so the expectations from the contract are still correct: you change the function, not the test. In Part C the contract changed for −99, so the expectation of D8 had to change. All the other old expectations stay, because the new rule doesn't concern them.
7. Because −99 fits two rules, and the contract gives the fault code precedence. Checking the station's range before the fault code would give `out_of_range`. D8, C9 and C10 detect it.
8. Because the tests have to check the same code that the application program uses: a fix in `rules.cpp` gets into both (lesson 13.4). You run all the tests after every change, because a change in one place can break something that worked before: that's the regression check.

</details>

## Self-assessment

For each competence, mark one answer:

| Competence | On my own | With a hint | After looking at the solution | To revise |
|---|---|---|---|---|
| A plan of cases before the code | | | | |
| Expected results from the contract | | | | |
| Pairs that decide each rule | | | | |
| Two targets and the shared `rules.cpp` | | | | |
| `std::istringstream` and sequences on one stream | | | | |
| `collect_measurements` and the limit | | | | |
| A report without measurements and a real 0 | | | | |
| Detecting the bug before the fix | | | | |
| The fix and the same tests | | | | |
| A change of the contract and regression | | | | |

If you adapt earlier code, write below the table which program was used, what was carried over from it, what was changed, and which design decisions were made on your own: the cases, the expected results, the starting value of `temperature` and the way of showing the bug.

If anything is marked in the "To revise" column, go back to the matching lesson:

| Topic | Lesson |
|---|---|
| `enum class`, named states | [14.1](lesson_01_named_state_instead_of_text.en.md) |
| `switch`, a label for each value, `-Wswitch` | [14.2](lesson_02_handling_every_state_with_switch.en.md) |
| a named result, the data unchanged after a refusal, the refusal precedence | [14.3](lesson_03_function_explains_refusal.en.md) |
| `read_number`, recovering the stream, the end of the data, tests of sequences | [14.4](lesson_04_reading_that_recovers_the_stream.en.md) |
| two targets, the shared `rules.cpp`, regression | [13.4](../module_13_testing_functions/lesson_04_tests_next_to_the_program.en.md) |
| cases that tell a bug apart, a plan before the code | [13.5](../module_13_testing_functions/lesson_05_workshop_reservations.en.md) |

---

## Module 14 summary

After five lessons you can:

- name states and function results with an `enum class` type, whose values the compiler checks, instead of text or numbers;
- handle each state in one place with a `switch` statement, with a label for each value;
- write a function that says with a named result why it refused, and leaves the data unchanged after a refusal;
- set a precedence when several rules fit one situation, and check it with a case in which both apply;
- read data so that a bad entry doesn't block the rest of the work and the end of the data is recognised before reading;
- test sequences of entries on one stream, and bring in a change of the contract so that the tests fail first and then all pass.

## What's next

This is the end of Module 14 and all of its planned lessons. Further modules of the course are planned.

**Previous lesson:** [Lesson 14.4: Try again: reading that recovers the stream](lesson_04_reading_that_recovers_the_stream.en.md) · [Course overview](../../README.en.md)

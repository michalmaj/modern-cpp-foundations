# Lesson 8.6: Race results (the Module 8 test)

[Polski](lesson_06_race_results.md) · **English** · [Course overview](../../README.en.md)

> **Module 8, lesson 6: the test** · about 100–115 minutes, in two sessions
> **You need:** your `cpp-workspace` folder and the original `lesson_05_first_program` project.
> **Pilot version.** The reference solutions in this lesson are checked automatically on Windows, Ubuntu and macOS. Nothing grades your own work automatically: you check it yourself, against the criteria. Your program asks for no data: all the values are written in the code. Only the check program in Part B reads data from the input.

## How this test works

This lesson introduces nothing new. You check whether you can design, on your own, **data types of your own and functions that analyse a collection of records**: they count the records that meet conditions, choose the best record and return a summary in a separate struct. You also analyse two short problems in code and explain your decisions.

The lesson has two parts:

- **Part A: the test.** Requirements, examples, tasks, questions and criteria. No hints and no solution code. Everything you need is from Modules 1–8.
- **Part B: checking and discussion.** Hints, the full list of check cases, the reference solution, fixes, answers and self-assessment. Go there after doing Part A, or when you consciously decide to stop trying on your own.

Looking at Part B, at earlier lessons or at your notes isn't a failure. What matters is that you **honestly note what you did on your own and what with help**. A suggested split into two sessions:

- **first:** analysing the requirements, designing both types and both functions, writing them, and the report for the data in the requirements;
- **second:** the boundary cases, task 2, comparing with the solution, task 3 and the self-assessment.

**You may use:** CLion or the terminal, CMake and Ninja, as before; a `CMakeLists.txt` copied from the original `lesson_05_first_program`; case and trace tables, and temporary test printouts. You won't need the debugger.

---

# Part A: the test

## Task 1: Race results

The race office prepares a report on the race: who qualifies for the next stage, how many runners finished and who has the best time. The runners' results are written in the program.

**Preparation:** in `cpp-workspace`, create a folder `race_results`, copy `CMakeLists.txt` from the original `lesson_05_first_program` into it, create an **empty** `main.cpp` and write the whole program on your own.

### The runners' data

Each runner is described by three pieces of information: the name, the race time in seconds, and whether the race was finished.

- The name is a non-empty ASCII text with no spaces. The runners' names in one vector are all different.
- The time is a whole number. A runner who finished the race has a time from 1 to 3600 seconds.
- A runner who didn't finish the race has the time 0 recorded. **That isn't a sporting result:** such a time can't be the best and can't qualify.
- The program doesn't check these assumptions, reads nothing from the input and doesn't convert seconds to minutes.

The data in the requirements, in this order:

| Runner | Time in seconds | Finished? |
|---|---:|---|
| `Ada` | 540 | yes |
| `Bruno` | 620 | yes |
| `Cora` | 510 | yes |
| `Daniel` | 0 | no |
| `Ewa` | 510 | yes |
| `Filip` | 600 | yes |

The **qualifying limit** is the longest time allowed for a qualified runner. In the data in the requirements it's 600 seconds.

### Three different concepts

- **Finished:** the runner's record says that the runner finished the race. That doesn't yet mean qualifying.
- **Qualified:** the runner finished the race **and** has a time less than or equal to the limit. With a limit of 600, a time of 600 qualifies, and 601 no longer does. A runner who didn't finish never qualifies, not even with the recorded time 0.
- **Best result:** the shortest time **among all the runners who finished**, including those who didn't qualify. In a tie, the runner who stands **earlier** in the vector wins. When no runner finished, there's no best result.

### The report

The program prints, in order:

- `Runners: N`: the number of runners in the vector;
- `Qualified runners:`: always, even when no one qualifies;
- under it, the names of the qualified runners, each on a separate line, in the order of the vector, without times;
- `Finishers: N`: the number of runners who finished;
- `Qualified: N`: the number of qualified runners;
- `Best finisher:` with the name of the runner with the best result and their time, for example `Best finisher: Cora (510 s)`, or `Best finisher: none` when there's no best result.

The program prints no other messages and no empty lines.

### Types and functions

- The program defines **two types of its own**: a runner, with three fields, and a race summary. The summary stores five pieces of information about one result of the analysis: the number of runners who finished (`std::size_t`), the number of qualified runners (`std::size_t`), whether a best result was found (`bool`), the name of the runner with the best result (`std::string`) and their time (`int`). You choose the names of the types and the fields on your own.
- All the summary's fields have explicit starting values. When there's no best result, the name and the time keep neutral starting values, and the `bool` field decides whether a result exists. The program then prints neither the name nor the time. Don't start the search from a "very large" number, for example 999999.
- **The function for one runner** gets the runner by `const&` and the limit as an `int` by value. It answers whether that runner qualifies: it returns `true` or `false`.
- **The function for the whole race** gets the vector of runners by `const&` and the limit by value. It creates a local summary, counts the runners who finished, counts the qualified runners **with the help of the function for one runner**, chooses the best result among the runners who finished, and returns the summary by value.
- No function changes the data, prints anything or reads from the input. You write the functions' names and headers on your own. A third function isn't needed, but you may add one if it has a sensible task.
- **`main`** keeps the limit in an `int` variable, and the runners in one `const` vector, initialised in the code in the order of the table. No separate variable per runner and no `push_back`. `main` calls the function for the whole race once, takes the number of runners from `size()`, prints the names of the qualified runners in a loop, using the function for one runner, and takes the rest of the report from the summary's fields. It repeats neither the qualifying condition nor the search for the best result. The program uses no variables declared outside functions.

### Examples

**Example A:** the data in the requirements, limit 600.

<!-- output: race_results -->
```text
Runners: 6
Qualified runners:
Ada
Cora
Ewa
Filip
Finishers: 5
Qualified: 4
Best finisher: Cora (510 s)
```

`Bruno` is over the limit, although the race is finished. `Daniel` didn't finish. `Filip` has a time equal to the limit, which qualifies. `Cora` and `Ewa` have the same shortest time, and `Cora` stands earlier.

Examples B–D are checked automatically by the check program from Part B, which reads the runners from the input: first their number, then each one on a separate line. That data is in the collapsed blocks. In your program the same data goes in the vector's braces. In all the examples the limit is 600.

**Example B:** an empty vector.

<details>
<summary>Data for the check program</summary>

<!-- input: race_results_check -->
```text
0
```

</details>

<!-- output: race_results_check -->
```text
Runners: 0
Qualified runners:
Finishers: 0
Qualified: 0
Best finisher: none
```

**Example C:** two records without a finished race, `Dana` and `Erik`, both with the time 0.

<details>
<summary>Data for the check program</summary>

<!-- input: race_results_check -->
```text
2
Dana 0 no
Erik 0 no
```

</details>

<!-- output: race_results_check -->
```text
Runners: 2
Qualified runners:
Finishers: 0
Qualified: 0
Best finisher: none
```

This is a different case from an empty vector: the records exist, but no race is finished, and the time 0 isn't a result.

**Example D:** `Slow`, who finished in 700 seconds, and `NoFinish`, who didn't finish.

<details>
<summary>Data for the check program</summary>

<!-- input: race_results_check -->
```text
2
Slow 700 yes
NoFinish 0 no
```

</details>

<!-- output: race_results_check -->
```text
Runners: 2
Qualified runners:
Finishers: 1
Qualified: 0
Best finisher: Slow (700 s)
```

`Slow` doesn't qualify, and still has the best result among the runners who finished: whether a best result exists doesn't depend on the limit.

### How to work

1. **Design both types and both functions before you start writing `main`.** For each function, write in one sentence its task, its parameters and its result type.
2. **Prepare a table of cases:** an empty vector; only records without a finished race; one runner who qualifies, one who finished without qualifying and one who didn't finish; a time equal to the limit, one second shorter and one second longer; the best result at the start, in the middle and at the end of the vector; a first record without a finished race; a tie, and the same tie in the reverse order; several finished races with no one qualifying. For each, write down the whole expected report.
3. If you like, check the function for one runner on its own with the test printouts from lesson 5.5: the times 599, 600 and 601, and a record without a finished race with the time 0. Then remove the test printouts.
4. **Run the whole program** for the data in the requirements (example A) and for the data in example D. Change only what's inside the vector's braces, and at the end put the data in the requirements back. Analyse cases B and C on paper: trace what your function returns when the loop makes no pass at all, or never meets a finished race. Every case in the full list of check cases is checked automatically.

When the result matches, you can save the project in Git, as in lesson 1.5. Before you commit, check `git status`: only `main.cpp` and `CMakeLists.txt` go into the history.

## Task 2: Diagnostics

Do this task **after task 1**: both problems are about functions similar to yours.

<details>
<summary>Diagnostic A: the best time starts at zero</summary>

In `cpp-workspace`, create a folder `diagnosis_8`, copy `main.cpp` and `CMakeLists.txt` from the original `lesson_05_first_program` into it, and put the program below into `main.cpp`: you may type it or copy it. The requirements are the same as in task 1.

<!-- example: best_time_bug -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>
#include <vector>

struct Runner {
    std::string name;
    int time_seconds;
    bool finished;
};

struct RaceSummary {
    std::size_t finishers;
    std::size_t qualified;
    bool has_best;
    std::string best_name;
    int best_time;
};

bool is_qualified(const Runner& runner, int limit) {
    return runner.finished && runner.time_seconds <= limit;
}

RaceSummary summarise_race(const std::vector<Runner>& runners, int limit) {
    RaceSummary summary{0, 0, false, "", 0};

    for (const Runner& runner : runners) {
        if (runner.finished) {
            ++summary.finishers;

            if (runner.time_seconds < summary.best_time) {
                summary.has_best = true;
                summary.best_name = runner.name;
                summary.best_time = runner.time_seconds;
            }
        }

        if (is_qualified(runner, limit)) {
            ++summary.qualified;
        }
    }

    return summary;
}

int main() {
    const int limit{600};
    const std::vector<Runner> runners{
        {"Gil", 0, false},
        {"Hana", 0, false}
    };

    const RaceSummary summary{summarise_race(runners, limit)};

    std::cout << "Runners: " << runners.size() << "\n";
    std::cout << "Qualified runners:\n";

    for (const Runner& runner : runners) {
        if (is_qualified(runner, limit)) {
            std::cout << runner.name << "\n";
        }
    }

    std::cout << "Finishers: " << summary.finishers << "\n";
    std::cout << "Qualified: " << summary.qualified << "\n";

    if (summary.has_best) {
        std::cout << "Best finisher: " << summary.best_name << " (" << summary.best_time << " s)\n";
    } else {
        std::cout << "Best finisher: none\n";
    }
}
```

1. **Predict** the standard output for the data in the program.
2. Run the program. Does the result match the requirements?
3. Change the data in the vector so that the bug shows. First write down the correct report for your data, then run the program.
4. Trace the values of the fields `best_time` and `has_best` after each pass of the loop.
5. Explain why 0 isn't suitable as the "best so far" time.
6. What must the program know before it compares a time with the best so far?
7. Fix the function without changing the data.
8. Run the fixed program for your vector.
9. Predict the fixed program's result for a tie, for an empty vector and for the data in example D, then compare it with Part B.

</details>

<details>
<summary>Diagnostic B: changing a record through <code>const&amp;</code></summary>

You **only analyse this fragment on paper**: don't run it. This version of the qualifying function was meant to make sure that a runner without a finished race never fits within the limit. A change of the time was added to it:

<!-- fragment -->
```cpp
bool is_qualified(const Runner& runner, int limit) {
    if (!runner.finished) {
        runner.time_seconds = limit + 1;
    }

    return runner.time_seconds <= limit;
}
```

1. Should a program with this function build?
2. Why not?
3. Is the type of the field `time_seconds` the problem?
4. What does `const&` mean for access through the parameter?
5. Does the qualifying function need to change the record at all?
6. How do you remove the error without removing `const`?

</details>

The results, fixes and answers are in Part B, in [Diagnostics: results and fixes](#diagnostics-results-and-fixes).

## Task 3: Explain your design

Answer briefly, in writing, referring to your own program from task 1:

1. Why are the runner and the summary two different types? Why isn't the limit a field of the runner?
2. Why does the function for one runner return a `bool`, while the function for the whole race returns a struct?
3. Why does the best result need separate information about whether anything was found? Why doesn't a runner without a finished race, with the time 0, win?
4. Why does the runner who stands earlier stay in a tie? What in your report can a change in the order of the runners change, and what can't it?
5. Does zero qualified runners mean that no runner finished? Point to a case in your table.
6. Why does none of your functions change the records?
7. Does the number of qualified runners not exceeding the number of runners who finished prove that the program works correctly?

## Success criteria

You pass the test when you meet **all** the criteria. You may use Part B while doing so, as long as you note it honestly in the self-assessment.

- `race_results/main.cpp` was written from an empty file, in valid C++20. The program builds without errors.
- There are two types of your own: a runner with three fields and a summary with five fields of the required types. All the fields have explicit starting values.
- The function for one runner gets it by `const&` and the limit by value, and returns a `bool`. The function for the whole race gets the vector by `const&` and the limit by value, uses the function for one runner and returns the summary by value. Neither changes the data, prints anything or reads anything.
- The limit is an `int` variable in `main`, and the runners stand in one `const` vector, in the order of the table.
- The standard output for examples A and D matches the requirements. Cases B and C match your analysis on paper and the full list of check cases.
- A runner without a finished race doesn't qualify and doesn't win. A time equal to the limit qualifies. In a tie, the runner who stands earlier wins. A best result exists even with zero qualified runners, as long as at least one race is finished.
- The search for the best result starts from the information "nothing found yet", not from a made-up number. The program reads no elements that don't exist, for example the first element of an empty vector.
- The qualifying condition stands in one place in the program.
- The bug in diagnostic A was fixed and the fix was checked, and the fragment in diagnostic B was analysed without running it.
- You can explain every line of your program and answer the questions in task 3.

The names of the types, fields, functions and variables, and the split of the program, may differ from the reference solution, as long as they're readable and meet the requirements. A correct result is a necessary condition, but **not proof of understanding**. That's why tasks 2 and 3 are part of the test.

---

# Part B: checking and discussion

Come here after doing Part A, or when you consciously decide to stop trying on your own.

## How to check your work

- **Standard output:** compare the program's lines with the expected ones, character by character, including the names under `Qualified runners:` and their order.
- **Boundary cases:** check the empty vector and the vector without finished races with a trace table, and compare them with the full list of check cases. Each case is checked automatically there.
- **Functions:** does each have a task you can describe in one sentence? Does the qualifying condition or the search for the best result also appear in `main`?
- **The logic of the results:** the dependencies described with the reference solution help you catch a bug, but they don't replace cases with expected reports.

## Hints

<details>
<summary>Hint 1</summary>

Which information describes one runner, and which is about the whole race? Should they belong to the same type?

</details>

<details>
<summary>Hint 2</summary>

The function for one runner answers the question about qualifying. The function for the whole collection can count the finished races and the qualifiers, and keep the information about the best finished result.

</details>

<details>
<summary>Hint 3</summary>

Don't assume that a first finished race exists. When searching for the best time, you need to recognise the first valid candidate. A later candidate replaces it only when it has a strictly shorter time.

</details>

## The full list of check cases

<details>
<summary>Open it after preparing your own table</summary>

Examples A–D are in Part A. In every case the limit is 600, and "no" means a race that wasn't finished, with the time 0.

| | Runners (time in seconds) | Qualified runners | Finishers | Qualified | Best finisher | What it checks |
|---|---|---|---:|---:|---|---|
| A | the data in the requirements | `Ada`, `Cora`, `Ewa`, `Filip` | 5 | 4 | `Cora (510 s)` | a tie, a time equal to the limit, the time 0 doesn't win |
| B | none | none | 0 | 0 | `none` | an empty vector |
| C | `Dana` no, `Erik` no | none | 0 | 0 | `none` | records without finished races |
| D | `Slow` 700, `NoFinish` no | none | 1 | 0 | `Slow (700 s)` | a best result without qualifying |
| E | `Solo` 450 | `Solo` | 1 | 1 | `Solo (450 s)` | one runner who qualifies |
| F | `Late` 601 | none | 1 | 0 | `Late (601 s)` | one runner, one second over the limit |
| G | `Quit` no | none | 0 | 0 | `none` | one record without a finished race |
| H | `Edge` 600, `Under` 599, `Over` 601 | `Edge`, `Under` | 3 | 2 | `Under (599 s)` | the limit and one second either side of it; the best in the middle |
| I | `Fast` 300, `Mid` 400, `Last` 500 | `Fast`, `Mid`, `Last` | 3 | 3 | `Fast (300 s)` | the best at the start; several runners qualify |
| J | `Out` no, `Mid` 400, `Fast` 300 | `Mid`, `Fast` | 2 | 2 | `Fast (300 s)` | a first record without a finished race; the best at the end |
| K | `Ewa` 510, `Cora` 510 | `Ewa`, `Cora` | 2 | 2 | `Ewa (510 s)` | the tie in the reverse order |
| L | `Slow` 700, `Slower` 900, `Late` 601 | none | 3 | 0 | `Late (601 s)` | several finished races, no one qualifies |

**Automatic tests and your own runs.** Every case is checked automatically by a check program. It has the same types, the same functions and the same report as the reference solution, but it reads the runners from the input. It's only a checking tool, not part of the mission: in the mission, the vector is written in the code. The check program and its results are with the [reference solution](#the-reference-solution), because they contain the solution.

</details>

## The reference solution

Compare it with your program after finishing Part A. The names, the order of the fields and small decisions may differ, as long as the report is the same for every case in the list of check cases.

<details>
<summary>Task 1: race results</summary>

<!-- example: race_results -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>
#include <vector>

struct Runner {
    std::string name;
    int time_seconds;
    bool finished;
};

struct RaceSummary {
    std::size_t finishers;
    std::size_t qualified;
    bool has_best;
    std::string best_name;
    int best_time;
};

bool is_qualified(const Runner& runner, int limit) {
    return runner.finished && runner.time_seconds <= limit;
}

RaceSummary summarise_race(const std::vector<Runner>& runners, int limit) {
    RaceSummary summary{0, 0, false, "", 0};

    for (const Runner& runner : runners) {
        if (runner.finished) {
            ++summary.finishers;

            if (!summary.has_best || runner.time_seconds < summary.best_time) {
                summary.has_best = true;
                summary.best_name = runner.name;
                summary.best_time = runner.time_seconds;
            }
        }

        if (is_qualified(runner, limit)) {
            ++summary.qualified;
        }
    }

    return summary;
}

int main() {
    const int limit{600};
    const std::vector<Runner> runners{
        {"Ada", 540, true},
        {"Bruno", 620, true},
        {"Cora", 510, true},
        {"Daniel", 0, false},
        {"Ewa", 510, true},
        {"Filip", 600, true}
    };

    const RaceSummary summary{summarise_race(runners, limit)};

    std::cout << "Runners: " << runners.size() << "\n";
    std::cout << "Qualified runners:\n";

    for (const Runner& runner : runners) {
        if (is_qualified(runner, limit)) {
            std::cout << runner.name << "\n";
        }
    }

    std::cout << "Finishers: " << summary.finishers << "\n";
    std::cout << "Qualified: " << summary.qualified << "\n";

    if (summary.has_best) {
        std::cout << "Best finisher: " << summary.best_name << " (" << summary.best_time << " s)\n";
    } else {
        std::cout << "Best finisher: none\n";
    }
}
```

1. **Two data types,** because they describe different things: `Runner` is one runner, and `RaceSummary` is the result of analysing the whole race.
2. **The limit as a separate argument,** because it's a shared rule of the race, not a feature of a runner. As a field it would repeat in every record and could differ between records.
3. **The record by `const&`,** because the functions only read it: no copy and no way to change it.
4. **`is_qualified` returns a `bool`,** because it answers a yes-or-no question.
5. **`summarise_race` returns a struct,** because one analysis gives five related pieces of information.
6. **No finished race, no qualifying:** the condition starts with `runner.finished`, so the time 0 doesn't matter.
7. **The time 0 isn't a result,** only a record of a race that wasn't finished. If it took part in the comparisons, it would beat every real time.
8. **We search for the best only among finished races,** because only they have a real time. The whole search stands inside `if (runner.finished)`.
9. **First we need to know whether a candidate already exists,** because the vector can be empty or have no finished race at all. There's also no "first element" that could be assumed in advance.
10. **The first finished race:** while `has_best` is `false`, the condition `!summary.has_best` is true, so the first finished race becomes the candidate without any comparison. Thanks to the short-circuit evaluation from lesson 3.4, the comparison with the starting value 0 isn't evaluated at all then.
11. **Later comparisons:** once there's a candidate, a new race replaces it only when `runner.time_seconds < summary.best_time`. The name and the time always change together.
12. **A tie doesn't replace the earlier candidate,** because the comparison is strict: an equal time isn't shorter. In the same way, lesson 6.3 kept the first largest drop.
13. **An empty vector:** the loop makes no pass, so the starting values stay: zeros and `has_best` equal to `false`. The program prints `none` and reads no element.
14. **No finished races:** the loop goes through the records, but never enters `if (runner.finished)`, so `has_best` stays `false`.
15. **A best result with zero qualified runners:** the search for the best doesn't depend on the limit, so in example D `Slow` wins without qualifying.
16. **`summarise_race` uses `is_qualified`,** so the qualifying condition stands in the program once. `main` doesn't repeat it either.
17. **The second pass in `main`:** the summary doesn't store a list of names, so `main` goes through the vector again and prints the qualified runners in the order of the vector. `is_qualified` makes the decision, and `main` only prints.
18. **No modifiable references,** because nothing changes the runners: the result is built in the local summary.
19. **No `std::vector<std::string>`,** because the names of the qualified runners can be printed straight away, in the second pass over the runners.
20. **The same model fits other data:** a record type, a function with a decision for one record, a function for the collection that returns a summary with a "found" flag, and choosing the best record with a strict comparison.

**Dependencies between the results** are an extra check of the logic, not a replacement for cases with expected reports:

- **A.** There can't be more qualified runners than runners who finished.
- **B.** There can't be more runners who finished than runners in the vector.
- **C.** A runner without a finished race can't have the best result.
- **D.** If at least one runner qualifies, the best result is within the limit too: it isn't longer than that runner's time.
- **E.** If there are no finished races, there's no best result either.
- **F.** If no one qualifies, a best result can still exist.

**Other correct solutions:** instead of `!summary.has_best || ...`, you can handle the first finished race separately in an `if` and an `else`. The order of the fields and the names may differ. You can also count the qualifiers inside `if (runner.finished)`, as long as `is_qualified` still does it.

**The check program** checks every case in the list of check cases. The types and the functions are the same as above, and so is the report from receiving the result on, apart from the indentation. There's one difference: the vector isn't written in the code, it's built from the input. The program reads the number of runners, then each runner: the name, the time, and `yes` or `no` for finishing, turned into a `bool` with a comparison, as in lesson 3.4. Each runner read goes to the end of the vector with `push_back`, as in the check programs of lessons 8.4 and 8.5. The mission needs neither input nor `push_back`.

<!-- example: race_results_check -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>
#include <vector>

struct Runner {
    std::string name;
    int time_seconds;
    bool finished;
};

struct RaceSummary {
    std::size_t finishers;
    std::size_t qualified;
    bool has_best;
    std::string best_name;
    int best_time;
};

bool is_qualified(const Runner& runner, int limit) {
    return runner.finished && runner.time_seconds <= limit;
}

RaceSummary summarise_race(const std::vector<Runner>& runners, int limit) {
    RaceSummary summary{0, 0, false, "", 0};

    for (const Runner& runner : runners) {
        if (runner.finished) {
            ++summary.finishers;

            if (!summary.has_best || runner.time_seconds < summary.best_time) {
                summary.has_best = true;
                summary.best_name = runner.name;
                summary.best_time = runner.time_seconds;
            }
        }

        if (is_qualified(runner, limit)) {
            ++summary.qualified;
        }
    }

    return summary;
}

int main() {
    const int limit{600};
    std::vector<Runner> runners{};
    int count{0};

    std::cin >> count;

    for (int number{1}; number <= count; ++number) {
        std::string name{};
        int time_seconds{0};
        std::string finished_answer{};

        std::cin >> name;
        std::cin >> time_seconds;
        std::cin >> finished_answer;

        const Runner runner{name, time_seconds, finished_answer == "yes"};
        runners.push_back(runner);
    }

    if (std::cin.fail()) {
        std::cout << "Input could not be read\n";
    } else {
        const RaceSummary summary{summarise_race(runners, limit)};

        std::cout << "Runners: " << runners.size() << "\n";
        std::cout << "Qualified runners:\n";

        for (const Runner& runner : runners) {
            if (is_qualified(runner, limit)) {
                std::cout << runner.name << "\n";
            }
        }

        std::cout << "Finishers: " << summary.finishers << "\n";
        std::cout << "Qualified: " << summary.qualified << "\n";

        if (summary.has_best) {
            std::cout << "Best finisher: " << summary.best_name << " (" << summary.best_time << " s)\n";
        } else {
            std::cout << "Best finisher: none\n";
        }
    }
}
```

Each case starts with the number of runners. Then each runner takes one line: the name, the time, and `yes` or `no` for finishing. Cases B–D are with the examples in Part A. The others stand below, in the order of the list of check cases: first A, then E to L.

<!-- input: race_results_check -->
```text
6
Ada 540 yes
Bruno 620 yes
Cora 510 yes
Daniel 0 no
Ewa 510 yes
Filip 600 yes
```

<!-- output: race_results_check -->
```text
Runners: 6
Qualified runners:
Ada
Cora
Ewa
Filip
Finishers: 5
Qualified: 4
Best finisher: Cora (510 s)
```

<!-- input: race_results_check -->
```text
1
Solo 450 yes
```

<!-- output: race_results_check -->
```text
Runners: 1
Qualified runners:
Solo
Finishers: 1
Qualified: 1
Best finisher: Solo (450 s)
```

<!-- input: race_results_check -->
```text
1
Late 601 yes
```

<!-- output: race_results_check -->
```text
Runners: 1
Qualified runners:
Finishers: 1
Qualified: 0
Best finisher: Late (601 s)
```

<!-- input: race_results_check -->
```text
1
Quit 0 no
```

<!-- output: race_results_check -->
```text
Runners: 1
Qualified runners:
Finishers: 0
Qualified: 0
Best finisher: none
```

<!-- input: race_results_check -->
```text
3
Edge 600 yes
Under 599 yes
Over 601 yes
```

<!-- output: race_results_check -->
```text
Runners: 3
Qualified runners:
Edge
Under
Finishers: 3
Qualified: 2
Best finisher: Under (599 s)
```

<!-- input: race_results_check -->
```text
3
Fast 300 yes
Mid 400 yes
Last 500 yes
```

<!-- output: race_results_check -->
```text
Runners: 3
Qualified runners:
Fast
Mid
Last
Finishers: 3
Qualified: 3
Best finisher: Fast (300 s)
```

<!-- input: race_results_check -->
```text
3
Out 0 no
Mid 400 yes
Fast 300 yes
```

<!-- output: race_results_check -->
```text
Runners: 3
Qualified runners:
Mid
Fast
Finishers: 2
Qualified: 2
Best finisher: Fast (300 s)
```

<!-- input: race_results_check -->
```text
2
Ewa 510 yes
Cora 510 yes
```

<!-- output: race_results_check -->
```text
Runners: 2
Qualified runners:
Ewa
Cora
Finishers: 2
Qualified: 2
Best finisher: Ewa (510 s)
```

<!-- input: race_results_check -->
```text
3
Slow 700 yes
Slower 900 yes
Late 601 yes
```

<!-- output: race_results_check -->
```text
Runners: 3
Qualified runners:
Finishers: 3
Qualified: 0
Best finisher: Late (601 s)
```

</details>

## Diagnostics: results and fixes

<details>
<summary>Diagnostic A: the best time starts at zero</summary>

Before the fix, for the data in the program:

<!-- output: best_time_bug -->
```text
Runners: 2
Qualified runners:
Finishers: 0
Qualified: 0
Best finisher: none
```

- **The result looks right,** because no race is finished: the times are never compared at all. A correct program would print the same. An empty vector behaves the same way.
- **Data that reveal the bug:** any data with at least one finished race. For example, adding `{"Ivo", 580, true}`. The correct report is `Ivo` on the list, 1, 1 and `Best finisher: Ivo (580 s)`. The program with the bug prints:

<!-- example: best_time_revealed -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>
#include <vector>

struct Runner {
    std::string name;
    int time_seconds;
    bool finished;
};

struct RaceSummary {
    std::size_t finishers;
    std::size_t qualified;
    bool has_best;
    std::string best_name;
    int best_time;
};

bool is_qualified(const Runner& runner, int limit) {
    return runner.finished && runner.time_seconds <= limit;
}

RaceSummary summarise_race(const std::vector<Runner>& runners, int limit) {
    RaceSummary summary{0, 0, false, "", 0};

    for (const Runner& runner : runners) {
        if (runner.finished) {
            ++summary.finishers;

            if (runner.time_seconds < summary.best_time) {
                summary.has_best = true;
                summary.best_name = runner.name;
                summary.best_time = runner.time_seconds;
            }
        }

        if (is_qualified(runner, limit)) {
            ++summary.qualified;
        }
    }

    return summary;
}

int main() {
    const int limit{600};
    const std::vector<Runner> runners{
        {"Gil", 0, false},
        {"Hana", 0, false},
        {"Ivo", 580, true}
    };

    const RaceSummary summary{summarise_race(runners, limit)};

    std::cout << "Runners: " << runners.size() << "\n";
    std::cout << "Qualified runners:\n";

    for (const Runner& runner : runners) {
        if (is_qualified(runner, limit)) {
            std::cout << runner.name << "\n";
        }
    }

    std::cout << "Finishers: " << summary.finishers << "\n";
    std::cout << "Qualified: " << summary.qualified << "\n";

    if (summary.has_best) {
        std::cout << "Best finisher: " << summary.best_name << " (" << summary.best_time << " s)\n";
    } else {
        std::cout << "Best finisher: none\n";
    }
}
```

<!-- output: best_time_revealed -->
```text
Runners: 3
Qualified runners:
Ivo
Finishers: 1
Qualified: 1
Best finisher: none
```

| After the pass for | The comparison in the program with the bug | `best_time` | `has_best` |
|---|---|---:|---|
| `Gil`, race not finished | none | 0 | `false` |
| `Hana`, race not finished | none | 0 | `false` |
| `Ivo`, 580 | `580 < 0` gives `false` | 0 | `false` |

- **The cause:** the starting value 0 pretends to be the best time so far, although there hasn't been any time yet. Every real time is positive, so it's never smaller than 0, and the first candidate never appears. The report contradicts itself: `Finishers: 1`, and no best result (dependency E). In lesson 6.1 the highest rainfall could start at 0, because the rainfall values were non-negative and an empty vector was outside the mission. When searching for the shortest time, the same start fails.
- **What the program must know:** whether it already has any candidate. `has_best` stores that information, but the program with the bug doesn't use it in the comparison.
- **The fix:** the first finished race becomes the candidate without a comparison, and only the later ones are compared with it: `if (!summary.has_best || runner.time_seconds < summary.best_time)`.

<!-- example: best_time_fixed -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>
#include <vector>

struct Runner {
    std::string name;
    int time_seconds;
    bool finished;
};

struct RaceSummary {
    std::size_t finishers;
    std::size_t qualified;
    bool has_best;
    std::string best_name;
    int best_time;
};

bool is_qualified(const Runner& runner, int limit) {
    return runner.finished && runner.time_seconds <= limit;
}

RaceSummary summarise_race(const std::vector<Runner>& runners, int limit) {
    RaceSummary summary{0, 0, false, "", 0};

    for (const Runner& runner : runners) {
        if (runner.finished) {
            ++summary.finishers;

            if (!summary.has_best || runner.time_seconds < summary.best_time) {
                summary.has_best = true;
                summary.best_name = runner.name;
                summary.best_time = runner.time_seconds;
            }
        }

        if (is_qualified(runner, limit)) {
            ++summary.qualified;
        }
    }

    return summary;
}

int main() {
    const int limit{600};
    const std::vector<Runner> runners{
        {"Gil", 0, false},
        {"Hana", 0, false},
        {"Ivo", 580, true}
    };

    const RaceSummary summary{summarise_race(runners, limit)};

    std::cout << "Runners: " << runners.size() << "\n";
    std::cout << "Qualified runners:\n";

    for (const Runner& runner : runners) {
        if (is_qualified(runner, limit)) {
            std::cout << runner.name << "\n";
        }
    }

    std::cout << "Finishers: " << summary.finishers << "\n";
    std::cout << "Qualified: " << summary.qualified << "\n";

    if (summary.has_best) {
        std::cout << "Best finisher: " << summary.best_name << " (" << summary.best_time << " s)\n";
    } else {
        std::cout << "Best finisher: none\n";
    }
}
```

<!-- output: best_time_fixed -->
```text
Runners: 3
Qualified runners:
Ivo
Finishers: 1
Qualified: 1
Best finisher: Ivo (580 s)
```

The fixed function is the same as in the reference solution, so the check program, with the same function, covers the other checks from step 9. A tie gives the runner who stands earlier (cases A and K), an empty vector gives `none` (case B), and for example D the result is `Slow (700 s)`. For data without a finished race, the fixed program prints the same as before the fix.

</details>

<details>
<summary>Diagnostic B: changing a record through <code>const&amp;</code></summary>

1. No. Clang reports `cannot assign to variable 'runner' with const-qualified type 'const Runner &'`.
2. Because the function gets the runner by `const&`, and the assignment tries to change one of its fields.
3. No. `time_seconds` is an ordinary `int` field. The problem is the access through a `const` parameter, as in lessons 8.3 and 8.4.
4. That the function has read-only access to an existing runner, without a copy. Through this parameter it can't change any field.
5. No. The function answers a question, and doesn't correct the data. Changing the time would also destroy information that the report reads later.
6. Write the rule as a condition, without changing the record: `return runner.finished && runner.time_seconds <= limit;`. A runner without a finished race drops out already at the first part of the condition.

</details>

## Answers to task 3

<details>
<summary>Sample answers</summary>

1. Because the runner is the data of one person, and the summary is the result of analysing the whole race: they have different fields and different tasks. The limit is a shared qualifying rule, not a feature of a person, so it belongs to the function call, not to the record.
2. Because qualifying is a yes-or-no question about one person. The analysis of the whole race gives several related pieces of information at once, so it returns them in one record.
3. Because the vector can be empty or have no finished race at all, and then there's no best result, although the name and time fields have some starting values. The time 0 means a race that wasn't finished, so it takes no part in the search for the best at all.
4. Because with a strict comparison an equal time doesn't replace the candidate that the program has already stored. Changing the order doesn't change the numbers or the best time, but in a tie it can change the name of the runner with the best result, and also the order of the names on the list of qualified runners.
5. No. In example D `Slow` is over the limit, although the race is finished. Zero qualified runners with at least one finished race means that a best result exists, it's just not within the limit.
6. Because both only answer questions about the data. They get the records by `const&` and build the result in a local summary, so the input data stays as it is in the code.
7. No. It's only an agreement between two numbers. The program from diagnostic A meets it, and still gives a wrong best result. Only cases with expected reports check correctness.

</details>

## Self-assessment

For each criterion, mark one answer:

| Criterion | On my own | With a hint | After looking at the solution | To revise |
|---|---|---|---|---|
| Designing the runner type | | | | |
| Designing the summary type and the starting values | | | | |
| The vector of runners initialised in the code | | | | |
| The qualifying function: `const&` and the limit by value | | | | |
| The function for the whole race returning a summary | | | | |
| Finishing, qualifying and the best result as three different concepts | | | | |
| Choosing the best result with a "found" flag | | | | |
| A tie and the order of the runners | | | | |
| An empty vector and no finished races | | | | |
| The list of qualified runners in order | | | | |
| A table of cases | | | | |
| Diagnostic A (the best time from zero) | | | | |
| Diagnostic B (changing a record through `const&`) | | | | |
| The explanations in task 3 | | | | |

If anything is marked in the "To revise" column, go back to the relevant lesson:

| Topic | Lesson |
|---|---|
| defining a struct, fields and initialisation | [8.1](lesson_01_first_struct.en.md) |
| changing fields and independent copies | [8.2](lesson_02_changing_fields_and_copies.en.md) |
| functions that get a record by `const&` | [8.3](lesson_03_functions_that_analyse_a_record.en.md) |
| a vector of records and a function for the whole collection | [8.4](lesson_04_many_records_in_a_vector.en.md) |
| a function returning a record with several results | [8.5](lesson_05_a_function_returns_a_record.en.md) |
| searching for the largest value, and ties | [6.1](../module_06_collections/lesson_01_the_first_vector.en.md), [6.3](../module_06_collections/lesson_03_positions_and_neighbours.en.md) |
| a vector as a `const&` parameter, and an extra parameter by value | [6.4](../module_06_collections/lesson_04_a_vector_as_a_parameter.en.md) |
| short-circuit evaluation of `&&` and `\|\|` | [3.4](../module_03_decisions_and_conditions/lesson_04_combining_conditions.en.md) |

Then try the task again, for example for a competition where the longest jump wins and a person without a valid attempt has 0 recorded.

---

## Module 8 summary

After six lessons, you can:

- define your own data types, `struct`, with fields of different types, and initialise all the fields in `{}`;
- read and change the fields of an object, and create independent copies of records;
- write functions that get a record or a vector of records by `const&` and return a number, a `bool` answer or a whole record with several results;
- store many records in a `std::vector` and go through them with a range-based loop by `const&`, without copying or changing them;
- separate the input data from the result of the analysis, and the calculations from the printing;
- choose the best record in a collection, also when there may be no candidate or when there's a tie.

Structs have many more possibilities, which you'll meet in later modules.

## What's next

This is the last lesson of Module 8. The next modules of the course are in preparation.

**Previous lesson:** [Lesson 8.5: A function returns a record with several results](lesson_05_a_function_returns_a_record.en.md) · **Next lesson:** in preparation · [Course overview](../../README.en.md)

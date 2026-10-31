# Modern C++ Foundations

[Polski](README.md) · **English**

A course that teaches programming from scratch, in C++. You don't need any previous programming experience. Everyday computer skills are enough.

> **Course status: in preparation.** Module 0 is functionally complete (six lessons, pilot version). All lessons of Module 1 are available too (six lessons, pilot version). All lessons of Module 2 are available too (eight lessons, pilot version). All lessons of Module 3 are available too (six lessons, pilot version). All lessons of Module 4 are available too (seven lessons, pilot version). All lessons of Module 5 are available too (seven lessons, pilot version). All lessons of Module 6 are available too (six lessons, pilot version). All lessons of Module 7 are available too (five lessons, pilot version). All lessons of Module 8 are available too (six lessons, pilot version). All lessons of Module 9 are available too (five lessons, pilot version). Module 10 is in development: its first two lessons are available. See [Course status](#course-status) for details.

## The C++ learning path

Modern C++ Foundations is the first of three courses that together form a C++ learning path:

| Part | Course | What it covers | Repository | Status |
|---|---|---|---|---|
| **A: you are here** | **Modern C++ Foundations** | Programming fundamentals and modern C++ | [modern-cpp-foundations](https://github.com/michalmaj/modern-cpp-foundations) | In preparation |
| B | Advanced Modern C++ | C++ in depth: how the language works “under the hood”, templates, memory management, programs that do several things at once, performance | `advanced-modern-cpp` (not created yet) | Planned |
| C | C++ Vision & AI Systems | C++ in practice: image processing, artificial intelligence and systems where performance matters | `cpp-vision-ai-systems` (not created yet) | Planned |

The A → B → C order is recommended, not required. If you already have equivalent knowledge, you can start with course B or C.

## Who this course is for

Anyone who wants to learn programming from the ground up and learn it properly. The course teaches two things at once: **how to think like a programmer** and **how to write programs in C++**.

C++ is one of the most important programming languages. It is used to build games, web browsers, parts of operating systems, car software, scientific tools and much more.

This is a general course. You don't need to be interested in any particular field: what you learn here applies to every kind of C++ programming.

## You don't need to know how to program

The course starts before your first program. We don't assume you know:

- what a terminal is: a window where you give the computer text commands;
- how the text you write becomes a program you can run;
- what a compiler, Git or a development environment is.

Every new idea is explained before we use it. You don't need to know any other programming language either.

From the first lesson we teach modern C++. We don't start with outdated habits that you would later have to unlearn. Older ways of writing code appear only as historical background, when they help explain something.

## What you will learn

By the end of the course you will be able to:

- write, run and fix C++ programs on your own, from your first `Hello, World!` to small and medium-sized applications;
- solve new problems step by step: understand the task, design a solution, check it and explain why it works;
- read error messages and calmly track down their cause;
- store and process data: numbers, text, lists and your own data types;
- split a program into smaller, readable parts: functions, files, libraries and classes;
- understand how a program uses memory, and write code that manages it safely;
- explain what happens between writing code and running a program;
- check that a program works correctly: write tests, use a debugger (a tool for following a program step by step) and act on warnings;
- use the terminal, Git and GitHub, the tools for recording the history of your code and sharing it, the way professional programmers do.

## How learning works

Most of the work consists of **short, independent tasks**. Each one has its own short story that explains why you are writing the program, and a clear way to check that your solution works. The tasks don't add up to one big application: if you get stuck on one, it won't block the next. Every now and then there is a larger, standalone project that brings several skills together.

Every topic follows the same rhythm:

**understand → experiment → apply → verify → explain**

At first we guide you step by step. Over time you make more of the decisions yourself, until you design solutions on your own.

## What you will work with

**Operating systems:** Windows, Linux and macOS. All three are officially supported. You don't need special hardware: an ordinary computer running one of these systems is enough, plus internet access to install the tools.

**Tools:**

| Tool | What it is for |
|---|---|
| **CLion** | A development environment (IDE): the program where you write, run and check your code. |
| **LLVM/Clang 22 or newer** | A toolset that includes the `clang++` compiler, which translates C++ code into a program your computer can run. |
| **C++20** | The version of the C++ language this course teaches. |
| **CMake** | Describes which files make up a project and how to build a program from them. |
| **Ninja** | Quickly carries out the build steps prepared by CMake. |
| **CTest** | Runs tests that check whether a program works correctly. |

You don't need to understand these names yet, or install anything. Every tool is explained in the course, and you will install them in [lesson 0.4](course/module_00_tooling/lesson_04_installing_the_tools.en.md). It is a pilot version: some installation steps have not yet been checked on every system.

CLion is convenient but not required: every project in the course can also be built and run from the terminal.

On Windows, the compiler also relies on Microsoft tools (Visual Studio Build Tools, including the Windows SDK). Lesson 0.4 shows how to install them.

## Course status

The course is **in preparation**. Here is an honest overview of what exists and what does not yet:

| Item | Status |
|---|---|
| Course overview (this file) | Ready |
| Module 0, lesson 1: [Files, folders and your first look at the terminal](course/module_00_tooling/lesson_01_files_and_terminal.en.md) | Available (pilot version) |
| Module 0, lesson 2: [Moving between folders](course/module_00_tooling/lesson_02_moving_between_folders.en.md) | Available (pilot version) |
| Module 0, lesson 3: [What happens when you type a command?](course/module_00_tooling/lesson_03_commands_and_programs.en.md) | Available (pilot version) |
| Module 0, lesson 4: [Set up your workshop: installing the tools](course/module_00_tooling/lesson_04_installing_the_tools.en.md) | Available (pilot version; the installation steps have not yet been checked on every system) |
| Module 0, lesson 5: [Your first working program in CLion](course/module_00_tooling/lesson_05_first_program_in_clion.en.md) | Available (pilot version; the CLion steps have not yet been checked on every system) |
| Module 0, lesson 6: [The same program without CLion](course/module_00_tooling/lesson_06_same_program_without_clion.en.md) | Available (pilot version) |
| Module 1, lesson 1: [The first program, from the inside](course/module_01_first_programs/lesson_01_first_program_inside.en.md) | Available (pilot version; the CLion steps have not yet been checked on every system) |
| Module 1, lesson 2: [When the compiler complains](course/module_01_first_programs/lesson_02_when_the_compiler_complains.en.md) | Available (pilot version; the CLion steps have not yet been checked on every system) |
| Module 1, lesson 3: [A program from a blank page](course/module_01_first_programs/lesson_03_a_program_from_a_blank_page.en.md) | Available (pilot version; the CLion steps have not yet been checked on every system) |
| Module 1, lesson 4: [From source code to an executable](course/module_01_first_programs/lesson_04_from_source_code_to_an_executable.en.md) | Available (pilot version) |
| Module 1, lesson 5: [Save the history of your work](course/module_01_first_programs/lesson_05_save_the_history_of_your_work.en.md) | Available (pilot version) |
| Module 1, lesson 6: [From an idea to a working program, on your own](course/module_01_first_programs/lesson_06_from_idea_to_working_program.en.md) (the Module 1 test) | Available (pilot version) |
| Module 2, lesson 1: [Values the program remembers](course/module_02_values_and_calculations/lesson_01_values_the_program_remembers.en.md) | Available (pilot version) |
| Module 2, lesson 2: [When values change](course/module_02_values_and_calculations/lesson_02_when_values_change.en.md) | Available (pilot version) |
| Module 2, lesson 3: [See what happens in the program](course/module_02_values_and_calculations/lesson_03_see_what_happens_in_the_program.en.md) | Available (pilot version; the debugger steps in CLion have not yet been checked on every system) |
| Module 2, lesson 4: [Division, remainder and the order of operations](course/module_02_values_and_calculations/lesson_04_division_remainder_and_order_of_operations.en.md) | Available (pilot version) |
| Module 2, lesson 5: [Numbers with a fractional part: `double` and `auto`](course/module_02_values_and_calculations/lesson_05_numbers_with_a_fractional_part.en.md) | Available (pilot version) |
| Module 2, lesson 6: [A program that asks the user](course/module_02_values_and_calculations/lesson_06_a_program_that_asks_the_user.en.md) | Available (pilot version) |
| Module 2, lesson 7: [Text the program remembers (`std::string`)](course/module_02_values_and_calculations/lesson_07_text_the_program_remembers.en.md) | Available (pilot version) |
| Module 2, lesson 8: [From data to result](course/module_02_values_and_calculations/lesson_08_from_data_to_result.en.md) (the Module 2 test) | Available (pilot version) |
| Module 3, lesson 1: [The program's first decision (`if`)](course/module_03_decisions_and_conditions/lesson_01_the_first_decision.en.md) | Available (pilot version) |
| Module 3, lesson 2: [Two possibilities (`else`), equality and `bool`](course/module_03_decisions_and_conditions/lesson_02_two_ways.en.md) | Available (pilot version) |
| Module 3, lesson 3: [Choosing among many possibilities (`else if`)](course/module_03_decisions_and_conditions/lesson_03_many_possibilities.en.md) | Available (pilot version) |
| Module 3, lesson 4: [Combining conditions (`&&`, `\|\|`, `!`)](course/module_03_decisions_and_conditions/lesson_04_combining_conditions.en.md) | Available (pilot version) |
| Module 3, lesson 5: [Checking data before calculating](course/module_03_decisions_and_conditions/lesson_05_check_before_calculating.en.md) | Available (pilot version) |
| Module 3, lesson 6: [The program makes decisions (the Module 3 test)](course/module_03_decisions_and_conditions/lesson_06_the_program_decides.en.md) | Available (pilot version) |
| Module 4, lesson 1: [The first loop (`while`)](course/module_04_repeating_actions/lesson_01_the_first_loop.en.md) | Available (pilot version) |
| Module 4, lesson 2: [Sums and accumulators](course/module_04_repeating_actions/lesson_02_sums_and_accumulators.en.md) | Available (pilot version) |
| Module 4, lesson 3: [The `for` loop: counter, condition and update in one place](course/module_04_repeating_actions/lesson_03_the_for_loop.en.md) | Available (pilot version) |
| Module 4, lesson 4: [Repeating until the goal is reached](course/module_04_repeating_actions/lesson_04_repeat_until_the_goal.en.md) | Available (pilot version) |
| Module 4, lesson 5: [Asking again for a valid value](course/module_04_repeating_actions/lesson_05_ask_again.en.md) | Available (pilot version) |
| Module 4, lesson 6: [A failed read, recovering the stream and the end of the data](course/module_04_repeating_actions/lesson_06_recover_and_end_of_input.en.md) | Available (pilot version) |
| Module 4, lesson 7: [The program repeats actions (the Module 4 test)](course/module_04_repeating_actions/lesson_07_the_program_repeats.en.md) | Available (pilot version) |
| Module 5, lesson 1: [Your first function (`void`)](course/module_05_functions/lesson_01_the_first_function.en.md) | Available (pilot version) |
| Module 5, lesson 2: [Parameters, arguments and passing by value](course/module_05_functions/lesson_02_parameters_and_arguments.en.md) | Available (pilot version) |
| Module 5, lesson 3: [A function returns a result (`return`)](course/module_05_functions/lesson_03_returning_a_result.en.md) | Available (pilot version) |
| Module 5, lesson 4: [Several ways to `return`](course/module_05_functions/lesson_04_several_returns.en.md) | Available (pilot version) |
| Module 5, lesson 5: [Several functions, one program](course/module_05_functions/lesson_05_several_functions.en.md) | Available (pilot version) |
| Module 5, lesson 6: [Declaration, definition and linking](course/module_05_functions/lesson_06_declaration_and_definition.en.md) | Available (pilot version) |
| Module 5, lesson 7: [A program built from your own functions (the Module 5 test)](course/module_05_functions/lesson_07_a_program_of_functions.en.md) | Available (pilot version) |
| Module 6, lesson 1: [Your first `std::vector` and the range-based `for` loop](course/module_06_collections/lesson_01_the_first_vector.en.md) | Available (pilot version) |
| Module 6, lesson 2: [Adding data to a vector: `push_back()` and `empty()`](course/module_06_collections/lesson_02_adding_to_a_vector.en.md) | Available (pilot version) |
| Module 6, lesson 3: [Element positions and neighbouring values in a `std::vector`](course/module_06_collections/lesson_03_positions_and_neighbours.en.md) | Available (pilot version) |
| Module 6, lesson 4: [A vector as a function parameter: `const&`](course/module_06_collections/lesson_04_a_vector_as_a_parameter.en.md) | Available (pilot version) |
| Module 6, lesson 5: [A function creates and returns a new vector](course/module_06_collections/lesson_05_a_function_returns_a_vector.en.md) | Available (pilot version) |
| Module 6, lesson 6: [A training log (the Module 6 test)](course/module_06_collections/lesson_06_training_log.en.md) | Available (pilot version) |
| Module 7, lesson 1: [First characters: `char` and going through a `std::string`](course/module_07_text/lesson_01_first_characters.en.md) | Available (pilot version) |
| Module 7, lesson 2: [Positions and neighbouring characters in a `std::string`](course/module_07_text/lesson_02_positions_and_neighbours.en.md) | Available (pilot version) |
| Module 7, lesson 3: [A function creates a new text](course/module_07_text/lesson_03_a_function_creates_a_new_text.en.md) | Available (pilot version) |
| Module 7, lesson 4: [Processing successive lines with `std::getline`](course/module_07_text/lesson_04_successive_lines.en.md) | Available (pilot version) |
| Module 7, lesson 5: [Parcel code check (the Module 7 test)](course/module_07_text/lesson_05_parcel_code_check.en.md) | Available (pilot version) |
| Module 8, lesson 1: [Your first struct: several pieces of data describing one object](course/module_08_structs/lesson_01_first_struct.en.md) | Available (pilot version) |
| Module 8, lesson 2: [Changing fields and an independent copy of a record](course/module_08_structs/lesson_02_changing_fields_and_copies.en.md) | Available (pilot version) |
| Module 8, lesson 3: [Functions that analyse a record](course/module_08_structs/lesson_03_functions_that_analyse_a_record.en.md) | Available (pilot version) |
| Module 8, lesson 4: [Many records in a `std::vector`](course/module_08_structs/lesson_04_many_records_in_a_vector.en.md) | Available (pilot version) |
| Module 8, lesson 5: [A function returns a record with several results](course/module_08_structs/lesson_05_a_function_returns_a_record.en.md) | Available (pilot version) |
| Module 8, lesson 6: [Race results (the Module 8 test)](course/module_08_structs/lesson_06_race_results.en.md) | Available (pilot version) |
| Module 9, lesson 1: [A function changes an existing record](course/module_09_mutable_references/lesson_01_a_function_changes_a_record.en.md) | Available (pilot version) |
| Module 9, lesson 2: [A change only when the conditions are met](course/module_09_mutable_references/lesson_02_a_change_only_when_allowed.en.md) | Available (pilot version) |
| Module 9, lesson 3: [Changing the elements of a vector through a reference](course/module_09_mutable_references/lesson_03_changing_vector_elements.en.md) | Available (pilot version) |
| Module 9, lesson 4: [Find a record and change the right object](course/module_09_mutable_references/lesson_04_find_a_record_and_change_it.en.md) | Available (pilot version) |
| Module 9, lesson 5: [A delivery drone fleet (the Module 9 test)](course/module_09_mutable_references/lesson_05_drone_fleet.en.md) | Available (pilot version) |
| Module 10, lesson 1: [One record from input](course/module_10_input_records/lesson_01_one_record_from_input.en.md) | Available (pilot version) |
| Module 10, lesson 2: [Names with spaces: `>>` and `std::getline`](course/module_10_input_records/lesson_02_names_with_spaces.en.md) | Available (pilot version) |
| Module 10: the remaining lessons (records from input) | In preparation |
| Further modules | Planned |
| Full course plan | Not published yet |
| Courses B and C | Planned, repositories do not exist yet |

## How to start

Work through the lessons in order, starting with the first:

1. **[Lesson 0.1: Files, folders and your first look at the terminal](course/module_00_tooling/lesson_01_files_and_terminal.en.md)**
2. **[Lesson 0.2: Moving between folders](course/module_00_tooling/lesson_02_moving_between_folders.en.md)**
3. **[Lesson 0.3: What happens when you type a command?](course/module_00_tooling/lesson_03_commands_and_programs.en.md)**
4. **[Lesson 0.4: Set up your workshop: installing the tools](course/module_00_tooling/lesson_04_installing_the_tools.en.md)**
5. **[Lesson 0.5: Your first working program in CLion](course/module_00_tooling/lesson_05_first_program_in_clion.en.md)**
6. **[Lesson 0.6: The same program without CLion](course/module_00_tooling/lesson_06_same_program_without_clion.en.md)**
7. **[Lesson 1.1: The first program, from the inside](course/module_01_first_programs/lesson_01_first_program_inside.en.md)**
8. **[Lesson 1.2: When the compiler complains](course/module_01_first_programs/lesson_02_when_the_compiler_complains.en.md)**
9. **[Lesson 1.3: A program from a blank page](course/module_01_first_programs/lesson_03_a_program_from_a_blank_page.en.md)**
10. **[Lesson 1.4: From source code to an executable](course/module_01_first_programs/lesson_04_from_source_code_to_an_executable.en.md)**
11. **[Lesson 1.5: Save the history of your work](course/module_01_first_programs/lesson_05_save_the_history_of_your_work.en.md)**
12. **[Lesson 1.6: From an idea to a working program, on your own](course/module_01_first_programs/lesson_06_from_idea_to_working_program.en.md)**
13. **[Lesson 2.1: Values the program remembers](course/module_02_values_and_calculations/lesson_01_values_the_program_remembers.en.md)**
14. **[Lesson 2.2: When values change](course/module_02_values_and_calculations/lesson_02_when_values_change.en.md)**
15. **[Lesson 2.3: See what happens in the program](course/module_02_values_and_calculations/lesson_03_see_what_happens_in_the_program.en.md)**
16. **[Lesson 2.4: Division, remainder and the order of operations](course/module_02_values_and_calculations/lesson_04_division_remainder_and_order_of_operations.en.md)**
17. **[Lesson 2.5: Numbers with a fractional part: `double` and `auto`](course/module_02_values_and_calculations/lesson_05_numbers_with_a_fractional_part.en.md)**
18. **[Lesson 2.6: A program that asks the user](course/module_02_values_and_calculations/lesson_06_a_program_that_asks_the_user.en.md)**
19. **[Lesson 2.7: Text the program remembers (`std::string`)](course/module_02_values_and_calculations/lesson_07_text_the_program_remembers.en.md)**
20. **[Lesson 2.8: From data to result (the Module 2 test)](course/module_02_values_and_calculations/lesson_08_from_data_to_result.en.md)**
21. **[Lesson 3.1: The program's first decision (`if`)](course/module_03_decisions_and_conditions/lesson_01_the_first_decision.en.md)**
22. **[Lesson 3.2: Two possibilities (`else`), equality and `bool`](course/module_03_decisions_and_conditions/lesson_02_two_ways.en.md)**
23. **[Lesson 3.3: Choosing among many possibilities (`else if`)](course/module_03_decisions_and_conditions/lesson_03_many_possibilities.en.md)**
24. **[Lesson 3.4: Combining conditions (`&&`, `||`, `!`)](course/module_03_decisions_and_conditions/lesson_04_combining_conditions.en.md)**
25. **[Lesson 3.5: Checking data before calculating](course/module_03_decisions_and_conditions/lesson_05_check_before_calculating.en.md)**
26. **[Lesson 3.6: The program makes decisions (the Module 3 test)](course/module_03_decisions_and_conditions/lesson_06_the_program_decides.en.md)**
27. **[Lesson 4.1: The first loop (`while`)](course/module_04_repeating_actions/lesson_01_the_first_loop.en.md)**
28. **[Lesson 4.2: Sums and accumulators](course/module_04_repeating_actions/lesson_02_sums_and_accumulators.en.md)**
29. **[Lesson 4.3: The `for` loop: counter, condition and update in one place](course/module_04_repeating_actions/lesson_03_the_for_loop.en.md)**
30. **[Lesson 4.4: Repeating until the goal is reached](course/module_04_repeating_actions/lesson_04_repeat_until_the_goal.en.md)**
31. **[Lesson 4.5: Asking again for a valid value](course/module_04_repeating_actions/lesson_05_ask_again.en.md)**
32. **[Lesson 4.6: A failed read, recovering the stream and the end of the data](course/module_04_repeating_actions/lesson_06_recover_and_end_of_input.en.md)**
33. **[Lesson 4.7: The program repeats actions (the Module 4 test)](course/module_04_repeating_actions/lesson_07_the_program_repeats.en.md)**
34. **[Lesson 5.1: Your first function (`void`)](course/module_05_functions/lesson_01_the_first_function.en.md)**
35. **[Lesson 5.2: Parameters, arguments and passing by value](course/module_05_functions/lesson_02_parameters_and_arguments.en.md)**
36. **[Lesson 5.3: A function returns a result (`return`)](course/module_05_functions/lesson_03_returning_a_result.en.md)**
37. **[Lesson 5.4: Several ways to `return`](course/module_05_functions/lesson_04_several_returns.en.md)**
38. **[Lesson 5.5: Several functions, one program](course/module_05_functions/lesson_05_several_functions.en.md)**
39. **[Lesson 5.6: Declaration, definition and linking](course/module_05_functions/lesson_06_declaration_and_definition.en.md)**
40. **[Lesson 5.7: A program built from your own functions (the Module 5 test)](course/module_05_functions/lesson_07_a_program_of_functions.en.md)**
41. **[Lesson 6.1: Your first `std::vector` and the range-based `for` loop](course/module_06_collections/lesson_01_the_first_vector.en.md)**
42. **[Lesson 6.2: Adding data to a vector: `push_back()` and `empty()`](course/module_06_collections/lesson_02_adding_to_a_vector.en.md)**
43. **[Lesson 6.3: Element positions and neighbouring values in a `std::vector`](course/module_06_collections/lesson_03_positions_and_neighbours.en.md)**
44. **[Lesson 6.4: A vector as a function parameter: `const&`](course/module_06_collections/lesson_04_a_vector_as_a_parameter.en.md)**
45. **[Lesson 6.5: A function creates and returns a new vector](course/module_06_collections/lesson_05_a_function_returns_a_vector.en.md)**
46. **[Lesson 6.6: A training log (the Module 6 test)](course/module_06_collections/lesson_06_training_log.en.md)**
47. **[Lesson 7.1: First characters: `char` and going through a `std::string`](course/module_07_text/lesson_01_first_characters.en.md)**
48. **[Lesson 7.2: Positions and neighbouring characters in a `std::string`](course/module_07_text/lesson_02_positions_and_neighbours.en.md)**
49. **[Lesson 7.3: A function creates a new text](course/module_07_text/lesson_03_a_function_creates_a_new_text.en.md)**
50. **[Lesson 7.4: Processing successive lines with `std::getline`](course/module_07_text/lesson_04_successive_lines.en.md)**
51. **[Lesson 7.5: Parcel code check (the Module 7 test)](course/module_07_text/lesson_05_parcel_code_check.en.md)**
52. **[Lesson 8.1: Your first struct: several pieces of data describing one object](course/module_08_structs/lesson_01_first_struct.en.md)**
53. **[Lesson 8.2: Changing fields and an independent copy of a record](course/module_08_structs/lesson_02_changing_fields_and_copies.en.md)**
54. **[Lesson 8.3: Functions that analyse a record](course/module_08_structs/lesson_03_functions_that_analyse_a_record.en.md)**
55. **[Lesson 8.4: Many records in a `std::vector`](course/module_08_structs/lesson_04_many_records_in_a_vector.en.md)**
56. **[Lesson 8.5: A function returns a record with several results](course/module_08_structs/lesson_05_a_function_returns_a_record.en.md)**
57. **[Lesson 8.6: Race results (the Module 8 test)](course/module_08_structs/lesson_06_race_results.en.md)**
58. **[Lesson 9.1: A function changes an existing record](course/module_09_mutable_references/lesson_01_a_function_changes_a_record.en.md)**
59. **[Lesson 9.2: A change only when the conditions are met](course/module_09_mutable_references/lesson_02_a_change_only_when_allowed.en.md)**
60. **[Lesson 9.3: Changing the elements of a vector through a reference](course/module_09_mutable_references/lesson_03_changing_vector_elements.en.md)**
61. **[Lesson 9.4: Find a record and change the right object](course/module_09_mutable_references/lesson_04_find_a_record_and_change_it.en.md)**
62. **[Lesson 9.5: A delivery drone fleet (the Module 9 test)](course/module_09_mutable_references/lesson_05_drone_fleet.en.md)**
63. **[Lesson 10.1: One record from input](course/module_10_input_records/lesson_01_one_record_from_input.en.md)**
64. **[Lesson 10.2: Names with spaces: `>>` and `std::getline`](course/module_10_input_records/lesson_02_names_with_spaces.en.md)**

For lessons 0.1–0.3 all you need is a computer running Windows, macOS or Linux. In lesson 0.4 you will install the course tools.

In Module 1 (lessons 1.1–1.6) you will start reading and writing your own C++20 code. In Module 2 (lessons 2.1–2.8), programs start to remember values, calculate, take data from the user and store text. It ends with the test in lesson 2.8. In Module 3 (lessons 3.1–3.6), programs start to make decisions. It ends with the test in lesson 3.6. In Module 4 (lessons 4.1–4.7), programs start to repeat actions. It ends with the test in lesson 4.7. In Module 5 (lessons 5.1–5.7) you'll learn to split programs into smaller, named parts: your own functions. It ends with the test in lesson 5.7. In Module 6 (lessons 6.1–6.6), programs start to store many values of the same kind in one variable: `std::vector`. It ends with the test in lesson 6.6. In Module 7 (lessons 7.1–7.5), you'll go through text character by character: `char` and `std::string`. It ends with the test in lesson 7.5. In Module 8 (lessons 8.1–8.6), you'll define your own data types: structs that join several pieces of information about one object. It ends with the test in lesson 8.6. In Module 9 (lessons 9.1–9.5), functions start to change existing data on purpose: records passed by a modifiable reference. It ends with the test in lesson 9.5. In Module 10 (so far lessons 10.1–10.2), programs start to build records from data read from the input. The further lessons of Module 10 are in preparation.

## What comes next

The natural next step is **Advanced Modern C++ (B)**, which builds on what you learn here. If you become interested in image processing and artificial intelligence, you can then move on to **C++ Vision & AI Systems (C)**. That course will officially support Ubuntu 24.04 LTS only.

# Modern C++ Foundations

[Polski](README.md) · **English**

A course that teaches programming from scratch, in C++. You don't need any previous programming experience. Everyday computer skills are enough.

> **Course status: in preparation.** The first lesson is available, and more lessons are in preparation. See [Course status](#course-status) for details.

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

You don't need to understand these names yet, or install anything. Every tool is explained in the course. Installation instructions for each system will be published only once they have been verified.

CLion is convenient but not required: every project in the course can also be built and run from the terminal.

On Windows, the compiler also relies on Microsoft tools (Visual Studio Build Tools and the Windows SDK). The exact list of required components will be given in the installation instructions.

## Course status

The course is **in preparation**. Here is an honest overview of what exists and what does not yet:

| Item | Status |
|---|---|
| Course overview (this file) | Ready |
| Module 0, lesson 1: [Files, folders and your first look at the terminal](course/module_00_tooling/lesson_01_files_and_terminal.en.md) | Available (pilot version) |
| Remaining Module 0 lessons: setting up your computer and first steps | In preparation |
| Further modules | Planned |
| Full course plan | Not published yet |
| Courses B and C | Planned, repositories do not exist yet |

## How to start

Start with the first lesson:

**[Lesson 0.1: Files, folders and your first look at the terminal](course/module_00_tooling/lesson_01_files_and_terminal.en.md)**

All you need is a computer running Windows, macOS or Linux. You don't need to install anything.

The next Module 0 lessons are in preparation. In them you will install the tools and check that everything works by running your first program.

## What comes next

The natural next step is **Advanced Modern C++ (B)**, which builds on what you learn here. If you become interested in image processing and artificial intelligence, you can then move on to **C++ Vision & AI Systems (C)**. That course will officially support Ubuntu 24.04 LTS only.

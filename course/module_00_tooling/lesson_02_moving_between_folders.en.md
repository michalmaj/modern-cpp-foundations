# Lesson 0.2: Moving between folders

[Polski](lesson_02_moving_between_folders.md) · **English** · [Course overview](../../README.en.md)

> **Module 0, lesson 2** · about 30–40 minutes
> **You need:** a computer running Windows, macOS or Linux. You don't need to install anything.

## Before you start

This lesson assumes that after [lesson 0.1](lesson_01_files_and_terminal.en.md) you know:

- the difference between a file and a folder;
- what a path is, and the difference between a relative and an absolute path;
- how to open a terminal;
- what `pwd` and `ls` do (on macOS and Linux: `ls -F`).

If any of this sounds unfamiliar, go back to lesson 0.1 for a moment. You don't need the files from that lesson: you will prepare everything you use here from scratch.

## The situation

In lesson 0.1, to look inside the `first-experiment` folder, you typed its name in every command: `ls first-experiment`. With one folder that's fine. Now imagine a folder three levels deeper and ten commands in a row, each with the same long path.

In a file window you just double-click a folder and you are inside. In a terminal you can also “go into” a folder. That's what this lesson teaches.

After this lesson you will:

- change the current folder with the `cd` command;
- move to the parent folder with `cd ..`;
- understand what `.` and `..` mean in paths;
- know that changing the current folder doesn't move anything on the drive;
- predict what `pwd` and `ls` will show after you move to another folder;
- reach a given folder using relative and absolute paths.

## 1. Understand: changing the current folder

From lesson 0.1 you know that a shell is always in some **current folder**, and that relative paths count from it.

The **`cd`** command (from *change directory*) changes that current folder. After `cd` you give the path to the folder you want to go to.

Important: `cd` **doesn't move anything**. It's like walking through a building: you change rooms, and the rooms stay where they are. Only one thing changes: the point from which the shell counts relative paths.

If it succeeds, `cd` prints nothing. So after every move, check where you are with `pwd`.

## 2. Try it: go home

A terminal doesn't always start in your home folder. That depends on the system, its settings, and where the terminal was started from. So first go somewhere you definitely know:

```text
cd ~
```

The `~` sign (tilde) means your home folder. This command works the same way in PowerShell, zsh and bash.

**Predict:** what will `pwd` show now? Type `pwd` and check.

You should see the path to your home folder, for example `C:\Users\ola`, `/Users/ola` or `/home/ola`. If you ever get lost, `cd ~` always brings you back.

## 3. Prepare: a small trip plan

For the exercises you need a small tree of folders. You are planning a trip to Kraków and Gdańsk:

```text
trip-plan
├── krakow
│   └── museums
└── gdansk
    └── beaches
```

You will create it with the mouse, as in lesson 0.1. First open your home folder in a file window (you are in it after `cd ~`):

| Windows | macOS | Linux |
|---|---|---|
| `explorer .` | `open .` | `xdg-open .` |

Then, in the file window:

1. Create a folder named `trip-plan` and go into it (double-click it).
2. Inside, create two folders: `krakow` and `gdansk`.
3. Go into `krakow` and create `museums` in it.
4. Go back one level (with the “Back” arrow in the window), go into `gdansk` and create `beaches` in it.

The names deliberately have no special letters.

> If `trip-plan` already exists because you are doing this lesson a second time, check that it has the folders above and add any that are missing.

Check in the terminal that everything is in place:

| Windows | macOS and Linux |
|---|---|
| `ls trip-plan` | `ls -F trip-plan` |

You should see two folders: `gdansk` and `krakow`.

## 4. Experiment: go into a folder

You are in your home folder.

**Predict:** what will happen if you type `ls krakow` (Windows) or `ls -F krakow` (macOS, Linux)?

Check. The shell will report an error: it can't find that path. This is not a mistake in the lesson. The path `krakow` is relative, so the shell looks for it in the current folder, which is your home folder. But `krakow` is inside `trip-plan`.

Now go into `trip-plan`:

```text
cd trip-plan
```

**Predict** what `pwd` will show, then check. The path should now end with `trip-plan`.

Type `ls krakow` (or `ls -F krakow`) again. This time you will see the `museums` folder. The command is identical to a moment ago, but the current folder is different, so the same relative path leads somewhere else.

Also take a look at the prompt. It often shows where you are, for example `PS C:\Users\ola\trip-plan>` on Windows. Depending on the system it may show the whole path or only the last name. `pwd` always gives you a definite answer.

## 5. Experiment: going up with `..`

From lesson 0.1 you already know `.`, which means “the current folder”. Its partner is **two dots** `..`, which means the **parent folder**: the folder that contains the current one. The parent folder of `trip-plan` is your home folder.

**Predict:** you are in `trip-plan`. Where will you end up after `cd ..`? Check: `cd ..`, then `pwd`. There must be a space between `cd` and `..`.

Now go several levels down with one command. A path can consist of several names, as in lesson 0.1:

| Windows | macOS and Linux |
|---|---|
| `cd trip-plan\krakow\museums` | `cd trip-plan/krakow/museums` |

**Predict** the output of `pwd`, then check.

Now a harder question. You are in `museums`. **Predict** what `ls ..` will show (on macOS and Linux, `ls -F ..`). Write down your answer, and only then check.

<details>
<summary>Explanation</summary>

You will see `museums`. Many people expect the word `krakow` here, but `..` is the `krakow` folder itself, and `ls` shows its **contents**. The only thing in `krakow` is `museums`. Notice also that `ls ..` didn't move you anywhere: check `pwd`.

</details>

`..` can be combined: `..\..` on Windows or `../..` on macOS and Linux means “two levels up”. Check what `ls` shows with such a path, typed from the `museums` folder.

### How high can you go?

Go home (`cd ~`) and repeat `cd ..` a few times, checking `pwd` each time:

| Windows | macOS | Linux |
|---|---|---|
| `C:\Users` → `C:\` → `C:\` | `/Users` → `/` → `/` | `/home` → `/` → `/` |

At some point `pwd` stops changing. You are then in the **root folder**, the highest folder of the tree (`C:\` on Windows, `/` on macOS and Linux). There is nothing above it, so `cd ..` changes nothing. You can look around here with `ls`, but don't change anything: these are system folders.

Go back home: `cd ~`.

## 6. Apply it: `cd` doesn't move anything

Go to the `krakow` folder:

| Windows | macOS and Linux |
|---|---|
| `cd trip-plan\krakow` | `cd trip-plan/krakow` |

Now look at the file window you opened in section 3. Has anything changed in it? Also check in the terminal what is in your home folder, without leaving `krakow`:

| Windows | macOS and Linux |
|---|---|
| `ls ~` | `ls -F ~` |

`trip-plan` is still in your home folder. Nothing has moved: only the place where the shell “stands” has changed. Moving files and folders is a completely different operation. You will learn it later.

## 7. Apply it: an absolute path works from anywhere

A relative path depends on the current folder, and an absolute path doesn't. Build the absolute path to the `gdansk` folder: take the `pwd` output from section 2 and add `trip-plan` and `gdansk`.

| System | Example for the home folder `ola` |
|---|---|
| Windows | `cd C:\Users\ola\trip-plan\gdansk` |
| macOS | `cd /Users/ola/trip-plan/gdansk` |
| Linux (usually) | `cd /home/ola/trip-plan/gdansk` |

Type your own version. It doesn't matter where you are now: this path leads to the same place from any folder. Check `pwd`.

> **Windows:** if your path contains a space, put it in quotes, as in lesson 0.1, for example `cd "C:\Users\Jan Kowalski\trip-plan\gdansk"`.

## 8. Mission: from the museum to the beach

The museums are done; it's beach time. Your task is to get from the `museums` folder to the `beaches` folder.

**Start:** type `cd ~`, then `cd trip-plan\krakow\museums` (Windows) or `cd trip-plan/krakow/museums` (macOS, Linux). Check `pwd`.

**Part A: step by step.** Get to `beaches` by changing folder **one level at a time**: use only `cd ..` or `cd` with a single folder name. Before each command, write down what you expect the end of the `pwd` output to be. After each command, check `pwd`.

| Step | Command | Expected end of `pwd` | Matches? |
|---|---|---|---|
| 1 | | | |
| 2 | | | |
| … | | | |

<details>
<summary>Hint: how many steps?</summary>

Four are enough: twice up, twice down.

</details>

**Part B: in one command.** Go back to the start (`museums`) and reach `beaches` with **one** `cd` command and a relative path.

**Part C: back again.** From `beaches`, go back to your home folder. Do it in two ways: once with a command using `~`, and once using only `..`. How many `..` do you need?

### Success criterion

- After part A and after part B, the output of `pwd` ends with `trip-plan\gdansk\beaches` (Windows) or `trip-plan/gdansk/beaches` (macOS, Linux).
- In `beaches`, `ls` (or `ls -F`) **prints nothing**. That's fine: the folder is empty. No output is not an error. An error would look like the message from section 4.
- After part C, `pwd` shows your home folder.

<details>
<summary>Sample solution</summary>

On macOS and Linux (on Windows use `\` instead of `/`):

- Part A: `cd ..` (→ `krakow`), `cd ..` (→ `trip-plan`), `cd gdansk`, `cd beaches`.
- Part B: `cd ../../gdansk/beaches`.
- Part C: `cd ~` or `cd ../../..` (three levels up: `gdansk`, `trip-plan`, the home folder).

</details>

## 9. Same names, different tools

On Windows you type `cd`, `pwd` and `ls`, just as on macOS and Linux. In PowerShell, however, these are **aliases**: additional, shorter names for PowerShell's own commands:

| You type | In PowerShell it is really |
|---|---|
| `cd` | `Set-Location` |
| `pwd` | `Get-Location` |
| `ls` | `Get-ChildItem` |

They look the same, but they are different tools from the ones on macOS and Linux, so the details differ. That's why `ls -F` from lesson 0.1 doesn't work on Windows, and the table below lists a few more differences. A rule for the future: **the same name doesn't mean the same tool**. When something behaves differently from the example, check the version of the command for your system.

## 10. When things look different

First check `pwd`: most surprises with `cd` come from being in a different folder than you think. If you get lost, `cd ~` takes you home.

| What you see | What it means | What to do |
|---|---|---|
| Windows: `Cannot find path '…' because it does not exist.`<br>macOS: `cd: no such file or directory: krakow`<br>Linux: `bash: cd: krakow: No such file or directory` | There is no such path in the current folder. | Check `pwd` and `ls`: is the folder where you are looking for it, and is the name spelled correctly? |
| macOS and Linux: `command not found: cd..` or `cd..: command not found` | The space between `cd` and `..` is missing. | Type `cd ..`, with a space. In PowerShell `cd..` happens to work, but use the space everywhere. |
| `cd Krakow` (capital letter) works on Windows and usually on macOS, but not on Linux | Linux distinguishes uppercase and lowercase letters in names. Windows and macOS usually don't, although `pwd` may then show the name spelled the way you typed it. | Type names exactly as you see them in `ls`. |
| Plain `cd` (with nothing after it) takes you home on macOS and Linux; on Windows, depending on the PowerShell version, it takes you home or nowhere | This is one of the differences between shells. | Use `cd ~` to go home. It works everywhere. |
| macOS and Linux: after `cd trip-plan\krakow`, a message about a missing folder `trip-plankrakow` | On macOS and Linux the separator is `/`. The `\` character means something else there and the shell removes it, which is why the name in the message is glued together. | Use `/`. PowerShell on Windows accepts both separators, but in this course we write `\` on Windows. |
| `ls` in `beaches` prints nothing | The folder is empty. | Everything is fine. |

## 11. Explain it

Answer in your own words, ideally out loud or on paper. Only then expand the answer.

**1.** You are in `krakow` and type `cd museums`. What changed on the drive, and what changed in the shell?

<details>
<summary>Answer</summary>

Nothing changed on the drive. `museums` is where it was. In the shell, the current folder changed, and with it the starting point of relative paths.

</details>

**2.** Ola is in `trip-plan` and Bartek is in `krakow`. Both type `cd gdansk`. Who succeeds, and why? How can the other person write the command to reach `gdansk`?

<details>
<summary>Answer</summary>

Ola succeeds, because `gdansk` is inside `trip-plan`. There is no `gdansk` folder in `krakow`, so Bartek gets an error. Bartek can type `cd ..\gdansk` (Windows) or `cd ../gdansk` (macOS, Linux), meaning “one level up, then into `gdansk`”, or use an absolute path.

</details>

**3.** You are in `museums`, and `ls ..` shows `museums`. Why not `krakow`?

<details>
<summary>Answer</summary>

Because `..` means the `krakow` folder, and `ls` shows what is **inside** the folder you point it at. The only thing in `krakow` is `museums`.

</details>

**4.** Why does `cd` with an absolute path work regardless of the current folder, while with a relative path it doesn't?

<details>
<summary>Answer</summary>

An absolute path starts from the root folder, so it describes a place in the whole tree. A relative path describes a route from the current folder, so from a different starting point it leads somewhere else, or nowhere.

</details>

## Summary

- `cd path` changes the current folder and doesn't move anything on the drive.
- `.` is the current folder and `..` is the parent folder. Both can be used in paths, for example `..\gdansk` or `../gdansk`.
- `~` is your home folder. `cd ~` is a safe way back from anywhere.
- At the very top of the tree is the root folder: `C:\` (on Windows, for drive `C:`) or `/` (on macOS and Linux).
- A relative path depends on the current folder; an absolute path doesn't.
- After every `cd`, check where you are with `pwd`.

You can keep the `trip-plan` folder, or delete it in the file window.

**Previous lesson:** [Lesson 0.1: Files, folders and your first look at the terminal](lesson_01_files_and_terminal.en.md) · **Next lesson:** in preparation · [Course overview](../../README.en.md)

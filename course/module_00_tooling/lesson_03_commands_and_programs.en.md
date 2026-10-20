# Lesson 0.3: What happens when you type a command?

[Polski](lesson_03_commands_and_programs.md) · **English** · [Course overview](../../README.en.md)

> **Module 0, lesson 3** · about 30 minutes
> **You need:** a computer running Windows, macOS or Linux. You don't need to install anything.

## Before you start

This lesson assumes that after [lesson 0.1](lesson_01_files_and_terminal.en.md) and [lesson 0.2](lesson_02_moving_between_folders.en.md):

- you know what a terminal and a shell are;
- you know paths and can use `pwd`, `ls` and `cd`;
- you know that in PowerShell `pwd`, `ls` and `cd` are aliases (lesson 0.2, section 9).

You don't need any files from the previous lessons.

## The situation

You have typed dozens of commands by now: `pwd`, `ls`, `cd`. Each time, something happened. But who actually did it? Is there something called `pwd` lying somewhere on your drive?

The answer leads straight to the goal of this module: running a program written in C++.

After this lesson you will know:

- what a command is and what the shell does with it;
- that not every command is a separate program;
- what a program and an executable file are;
- how a program differs from source code;
- why installed tools can be started by typing just their name.

## 1. Understand: what the shell does when you press Enter

A **command** is the text you type in the terminal and hand to the shell with the <kbd>Enter</kbd> key. The first word is the **command name**. The rest says what the command should work on, for example `krakow` in `cd krakow`.

When you press <kbd>Enter</kbd>, the shell looks at the name and has two options:

1. **It does the job itself.** Some commands are **built into** the shell. They are its own abilities.
2. **It starts a separate program.** A **program** is a file on the drive containing instructions the computer can carry out. Such a file is called an **executable file**.

On Windows there is one more step first, which you know from lesson 0.2: if the name is an **alias**, PowerShell first replaces it with the real command.

In a moment you will check which option applies to the commands you already use.

## 2. Try it: run a program

Type this command (it's the same on every system):

```text
whoami
```

The name comes from the question *who am I?*. **Predict** what the terminal will show, then check.

| System | Example result |
|---|---|
| Windows | `laptop\ola` |
| macOS and Linux | `ola` |

You will see the name of your account. On Windows it is preceded by the computer's name and a `\`. That's not a path, just the notation “computer\account”.

This result was produced by the **program** `whoami`: it asked the system who is logged in and printed the answer in the terminal.

## 3. Experiment: ask the shell what a command is

The shell can tell you what is behind a given name. Each system uses a different command for this:

| Windows (PowerShell) | macOS and Linux |
|---|---|
| `Get-Command whoami` | `type whoami` |

Result on Windows:

```text
CommandType     Name                Version    Source
-----------     ----                -------    ------
Application     whoami.exe          10.0.26... C:\Windows\system32\whoami.exe
```

Result on macOS and Linux (example):

```text
whoami is /usr/bin/whoami
```

Both answers say the same thing: `whoami` is a **separate program**, and the shell gives the path to its file. On Windows, `Application` in the `CommandType` column tells you this. You can ignore the `Version` column. The path on your computer may look a little different.

**Predict:** what will the shell say about `cd`? Will it find a file for it? Check:

| Windows (PowerShell) | macOS and Linux |
|---|---|
| `Get-Command cd` | `type cd` |

- **macOS and Linux:** `cd is a shell builtin`, meaning it is built into the shell. There is no file at all.
- **Windows:** `Alias` and `cd -> Set-Location`. Also check `Get-Command Set-Location`. You will see `Cmdlet`, a command built into PowerShell. The `Source` column shows no path to a file, only the name of a part of PowerShell.

**Conclusion:** “command” does not mean “file”. Some commands are abilities of the shell itself, and some start separate programs.

## 4. Apply it: a program is a file

Since `whoami` is a file, you can start it by giving its full path. Type the path the shell showed you in section 3, for example:

| Windows | macOS and Linux |
|---|---|
| `C:\Windows\system32\whoami.exe` | `/usr/bin/whoami` |

The result is the same as when you type just `whoami`. On Windows, program names usually end with `.exe`, but you can leave out that ending when you type the command.

How did the shell know where to look when you typed just `whoami`? It has a list of folders where it looks for programs. This list is called **`PATH`**. You don't need to look at it or change it now.

This matters for the next lessons. When you install the compiler, the installer usually adds its folder to this list. Then typing its name is enough, just like `whoami`. Your own program, however, will sit in your own folder, which isn't on the list. That's why you will start it by giving a path. You will see this at the end of the module.

## 5. Understand: a program versus source code

The `whoami` file is not text you can comfortably read. It contains instructions for the computer, not for a person. You don't need to open it.

Someone once wrote this program as ordinary text in a **programming language**. That text is **source code**. Then a special tool, a **compiler**, turned the source code into an executable file:

```text
source code (text)  →  compiler  →  program (executable file)  →  run  →  result in the terminal
```

These are two different files:

- **Source code** is what you read and change. It is text, like `list.txt` from lesson 0.1.
- **A program** is what you run. Changing the source code doesn't change the program until the compiler builds it again.

That is what this course will teach you: to write source code in C++ and turn it into a working program. In the next lessons you will prepare the tools you need, the compiler and CLion. At the end of this module you will run your first program in C++.

## 6. Mission: command detective

Investigate four commands you already use: `pwd`, `cd`, `ls` and `whoami`. For each one, first **predict** what it is, then check with `Get-Command` (Windows) or `type` (macOS, Linux).

| Command | Your prediction | What the shell showed | Kind: built in, alias or separate program? |
|---|---|---|---|
| `pwd` | | | |
| `cd` | | | |
| `ls` | | | |
| `whoami` | | | |

Finally, answer in two or three sentences: **where did the output of `whoami` come from?**

### Success criterion

- The kind in every row matches what the shell showed **on your computer**. Results may differ between systems, and that's fine.
- The table contains at least one command without a separate file behind it, and at least one that is a separate program.
- Your answer about `whoami` says that the shell started a separate program (a file), and that this program printed the result.

You don't need to memorise paths to programs. They can differ between computers.

<details>
<summary>Typical results</summary>

| Command | Windows (PowerShell) | macOS (zsh) | Linux (bash, e.g. Ubuntu) |
|---|---|---|---|
| `pwd` | alias (`Get-Location`, built into PowerShell) | built in | built in |
| `cd` | alias (`Set-Location`, built into PowerShell) | built in | built in |
| `ls` | alias (`Get-ChildItem`, built into PowerShell) | separate program, e.g. `/bin/ls` | usually an alias (`ls --color=auto`) that runs the separate program `ls` |
| `whoami` | separate program, `whoami.exe` | separate program | separate program |

So the same word `ls` is a PowerShell command on Windows and a separate program on macOS. As in lesson 0.2: the same name doesn't mean the same tool.

</details>

## 7. When things look different

| What you see | What it means | What to do |
|---|---|---|
| Windows: after `type whoami`, the message `Cannot find path '…\whoami' because it does not exist.` | In PowerShell, `type` is an alias of a completely different command (`Get-Content`), which shows the contents of a file. | On Windows, use `Get-Command`. |
| macOS and Linux: `command not found: Get-Command` or `Get-Command: command not found` | `Get-Command` is a PowerShell command. | On macOS and Linux, use `type`. |
| Linux (bash): `whoami is hashed (/usr/bin/whoami)` | Bash has remembered where it found this program. It is still a separate file. | Nothing to do. |
| Linux: ``ls is aliased to `ls --color=auto'`` | Here `ls` is an alias: the system adds an option that makes `ls` colour its output. Underneath, the program `ls` still runs. | Write “alias” in the mission. |
| The `type` message is in another language, for example saying the command is built into the shell | Bash translates its messages into the system's language. | What matters is the meaning of the message, not its language. |
| Windows: `The term '…' is not recognized…`<br>macOS and Linux: `… not found` | The shell doesn't know such a command: it isn't built in, and no program with that name was found. | Check the spelling. The same message can appear after installing a tool if something went wrong. We will come back to this when installing. |
| The path to a program differs from the example, for example `/usr/bin/ls` instead of `/bin/ls` | Systems organise their folders differently. | Nothing to do. What matters is that there is a path to a file at all. |

## 8. Explain it

Answer in your own words, ideally out loud or on paper. Only then expand the answer.

**1.** You type `cd krakow`, then `whoami`. Both are typed the same way. What different things happen when you press <kbd>Enter</kbd> in each case?

<details>
<summary>Answer</summary>

`cd` is carried out by the shell itself (on Windows through an alias of a command built into PowerShell). `whoami` is a separate program: the shell finds its file and starts it, and the program itself prints the result.

</details>

**2.** Someone claims: “Every command is a file somewhere on the drive.” Are they right? Give an example from your system.

<details>
<summary>Answer</summary>

No. `cd` has no file of its own: on macOS and Linux it is built into the shell, and on Windows it is an alias of a command built into PowerShell. `whoami`, for example, does have a file.

</details>

**3.** Why can you type just `whoami`, without the full path? What has to happen so that, after installing a compiler, you can start it the same way, by name?

<details>
<summary>Answer</summary>

The shell looks for programs in the folders on the `PATH` list, and the folder with `whoami` is on that list. The compiler's folder has to be on it too. Usually the installer takes care of that.

</details>

**4.** You have a file with C++ source code. Can you run it straight away, like `whoami`? What is missing?

<details>
<summary>Answer</summary>

No. Source code is text for people. First a compiler has to turn it into an executable file, and only that file can be run.

</details>

## Summary

- A **command** is text you hand to the shell. The shell either carries it out itself (a **built-in** command), replaces an alias with the real command, or starts a **separate program**.
- A **program** (executable file) is a file with instructions the computer can carry out. The output you see is printed by the program itself.
- Not every command is a file. You can check with `Get-Command` (Windows) or `type` (macOS, Linux).
- Programs can be started by name because the shell looks for them in the folders on the `PATH` list.
- **Source code** is text written by a person. A **compiler** turns it into a program.

**Previous lesson:** [Lesson 0.2: Moving between folders](lesson_02_moving_between_folders.en.md) · **Next lesson:** in preparation · [Course overview](../../README.en.md)

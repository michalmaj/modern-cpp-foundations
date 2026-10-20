# Lesson 0.1: Files, folders and your first look at the terminal

[Polski](lesson_01_files_and_terminal.md) · **English** · [Course overview](../../README.en.md)

> **Module 0, lesson 1** · about 30–45 minutes
> **You need:** a computer running Windows, macOS or Linux. You don't need to install anything.

## The situation

You download a concert ticket. The browser says “Downloaded”, you close it and… where exactly is that file now?

Your computer knows precisely. In this lesson you will learn to ask it the way programmers do: by typing commands in a **terminal**.

After this lesson you will:

- tell a file from a folder;
- understand what a path is;
- know what a terminal and a shell are for;
- be able to open a terminal on your system;
- be able to check which folder you are in and list what it contains.

## 1. Understand: files, folders and paths

A **file** is a piece of data stored under a name: a photo, a document, a song, a program.

A **folder** (also called a **directory**; both words mean the same thing) is a named container that holds files and other folders. A file cannot contain other files, but a folder can.

Folders inside folders form a tree:

```text
ola                    ← folder
├── Documents          ← folder
│   └── ticket.pdf     ← file
├── Downloads          ← folder
└── Pictures           ← folder
    └── holiday.jpg    ← file
```

`ola` is an example **home folder**: the folder the system gives each person who uses the computer. On your computer it has a different name, usually the same as your account name.

A **path** is the address of a file or folder. It lists the folders one after another, from the very top of the tree to the target, separated by a special character called the **separator**. The path to the ticket looks like this:

| System | Path to `ticket.pdf` |
|---|---|
| Windows | `C:\Users\ola\Documents\ticket.pdf` |
| macOS | `/Users/ola/Documents/ticket.pdf` |
| Linux | `/home/ola/Documents/ticket.pdf` |

Read a path from left to right. On Windows: “on drive `C:`, in folder `Users`, in folder `ola`, in folder `Documents`, there is the file `ticket.pdf`”. On Windows the separator is `\`, and on macOS and Linux it is `/`. The folder at the very top of the tree is the **root folder**. macOS and Linux have just one, written as a single `/`, which is why their paths start with `/`. On Windows each drive has its own root folder, for example `C:\`.

<details>
<summary>Check yourself: what is the path to <code>holiday.jpg</code> on your system?</summary>

- Windows: `C:\Users\ola\Pictures\holiday.jpg`
- macOS: `/Users/ola/Pictures/holiday.jpg`
- Linux: `/home/ola/Pictures/holiday.jpg`

</details>

## 2. Understand: the terminal and the shell

Day to day, you use your computer with a mouse: you click icons and open windows. There is another way: you can **type a command** and read the computer's answer. That's what a terminal is for.

- A **terminal** is a window where you type commands and read the answers.
- A **shell** is the program running in that window. It reads your command, carries it out and prints the result. On Windows we use the **PowerShell** shell. On macOS the default shell is **zsh**, and on Linux it is usually **bash**.

Why bother, when there is a mouse? Most programmer tools are used through commands, including the tool that turns the text you write into a working program. You will meet it in this course. A terminal also shows you exactly what happened and where on the drive.

A shell is always “in” some folder, just as a file window always shows one folder at a time. That folder is the **current folder** (programmers often say *current directory*). Commands work there unless you point them somewhere else.

## 3. Try it: open a terminal

| System | How to open a terminal |
|---|---|
| Windows 11 | Open the Start menu, type `Terminal` and start the **Terminal** app. |
| Windows 10 | Open the Start menu, type `PowerShell` and start **Windows PowerShell**. |
| macOS | Press <kbd>⌘ Cmd</kbd> + <kbd>Space</kbd>, type `Terminal` and press <kbd>Enter</kbd>. |
| Linux | It depends on your system. On Ubuntu, press <kbd>Ctrl</kbd> + <kbd>Alt</kbd> + <kbd>T</kbd> or search for **Terminal** in your applications. |

You will see a window with a short piece of text and a blinking cursor, for example:

```text
PS C:\Users\ola>              ← Windows
ola@MacBook-Air ~ %           ← macOS
ola@laptop:~$                 ← Linux
```

This is the **prompt**: the shell is waiting for a command. On your computer it looks a little different. Don't type it yourself: in this lesson you only type what we show as a command. On macOS and Linux, the `~` in the prompt means your home folder.

> **Windows:** the prompt should start with `PS`. If it doesn't, a window with a different shell (“Command Prompt”) has opened. Close it and open Terminal or PowerShell instead.

The commands in this lesson are short, so type them by hand. Confirm each one with the <kbd>Enter</kbd> key.

## 4. Try it: where am I?

Before you type anything, think: which folder is your shell in right now?

Type this command (it's the same on every system):

```text
pwd
```

`pwd` stands for *print working directory*, which means “show the current folder”. The result looks roughly like this.

Windows:

```text
Path
----
C:\Users\ola
```

macOS: `/Users/ola`. Linux: `/home/ola`.

Your result will contain the name of your own home folder, and that's how it should be. What matters is that it is a **path**: the address of the place where you are. A newly opened terminal usually starts in your home folder.

## 5. Try it: what is here?

Now list what the current folder contains. Here the commands differ between systems:

| Windows (PowerShell) | macOS and Linux |
|---|---|
| `ls` | `ls -F` |

`ls` is short for *list*. On macOS and Linux, the `-F` is an **option**: it asks `ls` to mark folders with a `/` at the end of their name. Don't add this option on Windows, because PowerShell shows what kind of item each entry is in a separate column.

Result on Windows (excerpt):

```text
    Directory: C:\Users\ola

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-----        10/20/2026   9:12 AM                Desktop
d-----        10/20/2026   9:12 AM                Documents
d-----        10/20/2026   9:12 AM                Downloads
```

Result on macOS or Linux (example):

```text
Desktop/    Documents/  Downloads/  Music/      Pictures/
```

How to read it:

- **Windows:** if the `Mode` column starts with `d` (for *directory*), the item is a folder. If it starts with `-`, it is a file. You can ignore the other columns for now.
- **macOS and Linux:** a `/` at the end of a name means a folder, and a name without `/` is a file. If you see other characters at the end, such as `*` or `@`, ignore them for now.

Your list will differ from the example. Dates and column layout may look different too. Most likely you will see only folders, because loose files rarely sit in a home folder. That is about to change.

## 6. Apply it: the terminal and the file window show the same place

Type a command that opens the current folder in an ordinary file window:

| Windows | macOS | Linux |
|---|---|---|
| `explorer .` | `open .` | `xdg-open .` |

The dot `.` is the shortest possible path: it means “the current folder”. So the whole command means “open the folder I'm in right now in a file window”.

Compare the window with the output of `ls`: you see the same folders. The file window and the terminal are two ways of looking at the same data on the drive.

Small differences are normal. For example, on macOS `ls -F` shows a `Library/` folder that Finder hides. And the file window may display translated names (more in section 9).

Now, in that window, create a new folder named `first-experiment`:

- **Windows:** right-click an empty area, choose **New → Folder**, type the name and press <kbd>Enter</kbd>.
- **macOS:** right-click an empty area, choose **New Folder**, type the name and press <kbd>Enter</kbd>.
- **Linux:** right-click an empty area, choose **New Folder**, type the name and confirm.

The name deliberately has no spaces or special letters: such names are easier to type in a terminal.

**Predict before you check:** will `first-experiment` appear in the output of `ls`? How will you tell that it is a folder and not a file?

Go back to the terminal and type `ls` (Windows) or `ls -F` (macOS, Linux) again. The new folder should be among the results:

- Windows: a line with `d-----` in the `Mode` column and the name `first-experiment`;
- macOS and Linux: `first-experiment/`.

## 7. Task: a place for your trip plan

You are planning a trip. Inside `first-experiment` you need a folder for notes and an empty file for a packing list.

**Step 1.** In the file window, go into the `first-experiment` folder and create a folder named `notes` inside it, just like before.

**Step 2.** You will create the file from the terminal. Don't change the current folder (it is still your home folder). Type:

| Windows | macOS and Linux |
|---|---|
| `New-Item first-experiment\list.txt` | `touch first-experiment/list.txt` |

Look at the path `first-experiment\list.txt`. You read it as: “in the folder `first-experiment`, the file `list.txt`”. It doesn't start with `C:\` or `/`, so the shell looks for `first-experiment` in the current folder. A path like this is a **relative path**: it counts from where you are. The paths that `pwd` prints start from the root folder (on Windows with a drive letter, for example `C:\`). Those are **absolute paths**.

On Windows, `New-Item` immediately prints information about the new file. The value `0` in the `Length` column means the file is empty. On macOS and Linux, `touch` prints nothing if everything worked.

> These commands are safe. If `list.txt` already exists, `New-Item` reports an error and changes nothing, and `touch` leaves its contents alone.

**Step 3.** Check the result without opening the file window:

| Windows | macOS and Linux |
|---|---|
| `ls first-experiment` | `ls -F first-experiment` |

### Success criterion

The output shows **exactly two items**: the folder `notes` and the file `list.txt`.

Windows:

```text
    Directory: C:\Users\ola\first-experiment

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-----        10/20/2026   9:30 AM                notes
-a----        10/20/2026   9:31 AM              0 list.txt
```

macOS and Linux:

```text
list.txt  notes/
```

The order may differ, and on Windows the `Mode` column may show fewer dashes. What matters is that `notes` is marked as a folder (`d` or `/`) and `list.txt` as a file.

## 8. Check it: build the full path

Write down the **absolute path** to `list.txt` on your computer. Take the output of `pwd` and add the next names to it, separated by your system's separator.

Then check that the path is correct:

| System | Example |
|---|---|
| Windows | `ls C:\Users\ola\first-experiment\list.txt` |
| macOS | `ls -F /Users/ola/first-experiment/list.txt` |
| Linux (usually) | `ls -F /home/ola/first-experiment/list.txt` |

These are only examples for the home folder `ola`. Your path starts the way your own `pwd` output does.

- If the path is correct, you will see the file `list.txt`.
- If not, the shell will report that it cannot find the path. Compare your path with the output of `pwd`, letter by letter.

> **Windows:** if your path contains a space (for example `C:\Users\Jan Kowalski`), put the whole path in quotes:
> `ls "C:\Users\Jan Kowalski\first-experiment\list.txt"`

## 9. When things look different

First, **read the message**. It usually says what the shell didn't understand or couldn't find, and quotes what was typed. Fix one thing and try again. Depending on your system settings, messages may appear in English or in another language.

| What you see | What it means | What to do |
|---|---|---|
| Windows: `The term 'lss' is not recognized…`<br>macOS: `zsh: command not found: lss`<br>Linux: `lss: command not found` | The shell doesn't know a command with that name. Most often it is a typo. | Compare the command you typed with the lesson, character by character. |
| Windows: `…the parameter name 'F' is ambiguous…` | The macOS and Linux version of a command was typed on Windows. | On Windows, type just `ls`. |
| Windows: `Cannot find path '…' because it does not exist.`<br>macOS and Linux: `No such file or directory` | There is nothing at that path. Either the name is different, or you are in a different folder than you think. | Check `pwd` and the spelling of the name. On Windows the message shows the full path the shell looked for, so compare it with the output of `pwd`. |
| Windows: the prompt doesn't start with `PS`, and `pwd` is an unknown command | “Command Prompt”, a different shell, has opened. | Open Terminal or PowerShell (see section 3). |
| The file window shows different names than the terminal, for example on a Polish system **Pobrane** instead of `Downloads` or **Użytkownicy** instead of `Users` | Windows and macOS can display translated folder names. The terminal shows the real names. They are the same folders. | Nothing to do. On Linux in a non-English language, the real names may be translated too, and then the terminal shows them that way as well. |
| `first-experiment` doesn't appear in the output of `ls` | The folder was created somewhere else or has a different name, for example “New folder”. | Open the window with the command from section 6 and check whether the folder is there and what it is called. |
| Linux: `xdg-open` doesn't work | Your system doesn't have this command. | Open a file window by hand (for example the **Files** app) and go to your home folder (usually called **Home**). Don't use `open` on Linux, because it is a completely different command. |
| macOS asks whether Terminal may access files in some folder | The system protects certain folders, such as `Documents`. | This lesson doesn't need it. You can decline. |

## 10. Explain it

Answer in your own words, ideally out loud or on paper. Only then expand the answer.

**1.** Ola on Windows and Bartek on macOS both type `pwd` and get completely different results. Did either of them make a mistake? What do the two results have in common?

<details>
<summary>Answer</summary>

Neither made a mistake. Both results are absolute paths to the current folder, usually the home folder. They differ because each has a different account name, and their systems write paths differently: Windows starts with a drive letter and uses `\`, macOS starts with `/` and uses `/`.

</details>

**2.** The command `ls first-experiment` (or `ls -F first-experiment`) worked while the current folder was the home folder. What would happen if the current folder were `Downloads`? How could you write the command so that it works no matter what the current folder is?

<details>
<summary>Answer</summary>

The shell would report that it can't find the path. `first-experiment` is a relative path, so the shell looks for it in the current folder, and `Downloads` has no such folder. An absolute path, for example `C:\Users\ola\first-experiment` (Windows), `/Users/ola/first-experiment` (macOS) or `/home/ola/first-experiment` (usually on Linux), works whatever the current folder is.

</details>

**3.** How do you tell in the terminal that `notes` is a folder and `list.txt` is a file? Is it enough to check whether the name contains a dot?

<details>
<summary>Answer</summary>

By the mark the terminal adds: `d` in the `Mode` column on Windows, or `/` at the end of the name on macOS and Linux. A dot in the name proves nothing. The `.txt` ending is just part of the name. A folder can be called `version.2`, and a file may have no dot at all.

</details>

**4.** The current folder was your home folder the whole time. So why was `list.txt` created inside `first-experiment`?

<details>
<summary>Answer</summary>

Because the command was given the path `first-experiment\list.txt` (or `first-experiment/list.txt`). The current folder is only the starting point of a relative path: the shell started from the home folder, went into `first-experiment` and created the file there.

</details>

## Summary

- A **file** stores data. A **folder** stores files and other folders.
- A **path** is an address. An **absolute** path starts from the root folder, and a **relative** path starts from the current folder.
- A **terminal** is a window for typing commands, and a **shell** is the program that carries them out.
- A shell always has a **current folder**.

| Purpose | Windows (PowerShell) | macOS | Linux |
|---|---|---|---|
| Show the current folder | `pwd` | `pwd` | `pwd` |
| Show what a folder contains | `ls` | `ls -F` | `ls -F` |
| Open the current folder in a file window | `explorer .` | `open .` | `xdg-open .` |
| Create an empty file | `New-Item path` | `touch path` | `touch path` |

You can keep the `first-experiment` folder, or delete it in the file window. It will then go to the Trash (called the Recycle Bin on Windows). We deliberately don't delete anything from the terminal yet: deleting there removes things immediately, without the Trash.

**Next lesson:** [Lesson 0.2: Moving between folders](lesson_02_moving_between_folders.en.md) · [Course overview](../../README.en.md)

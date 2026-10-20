# Lesson 1.5: Save the history of your work

[Polski](lesson_05_save_the_history_of_your_work.md) · **English** · [Course overview](../../README.en.md)

> **Module 1, lesson 5** · about 75 minutes
> **You need:** the `cpp-workspace` folder with your projects from lessons 1.1–1.4, a terminal, and, on Windows and Ubuntu, administrator rights to install Git (as in [lesson 0.4](../module_00_tooling/lesson_04_installing_the_tools.en.md)).
> **Pilot version:** the Git commands in this lesson are checked automatically in Windows PowerShell 5.1, PowerShell 7, bash on Ubuntu and zsh on macOS.

## Before you start

This lesson assumes that:

- you have a `cpp-workspace` folder in your home folder with the projects from lessons 1.1–1.4, for example `cinema_ticket` from the lesson 1.3 mission;
- in the terminal, you can go to a folder, list its contents and run a program (Module 0);
- you know which project files you write yourself and which ones the tools create (lesson 1.4).

## The situation

Your cinema ticket program works. You want to change it, but you're afraid of breaking something and not remembering what the working version looked like.

The simplest idea is copies: `cinema_ticket_final`, `cinema_ticket_final_2`, `cinema_ticket_final_really`. After a week, nobody knows which copy is which, how they differ, or which one worked. Every copy drags its build folders along. It's also easy to edit the wrong copy.

Programmers solve this problem with a **version control system**. It's a program that, when you tell it to, saves versions of chosen files, with a description, an author and a date. Later it shows what changed between versions and lets you see any earlier version. The most popular such system is **Git**.

After this lesson you will:

- explain what version control is for, and tell Git apart from GitHub;
- install Git and check its version;
- create a local repository and know what the `.git` folder is for;
- check the state of files (`git status`) and changes (`git diff`);
- choose files to save (`git add`) and create commits with a meaningful message (`git commit`);
- browse the history (`git log`);
- leave out files created by the tools, with `.gitignore`.

## 1. Git and GitHub

| | Git | GitHub |
|---|---|---|
| What it is | A program on your computer. | A service on the internet. |
| What it's for | Saves the history of changes to files and shows it. | Stores Git repositories online and helps people work on them together. |
| What it needs | Nothing beyond installing it. It works without the internet and without an account. | An account and the internet. |
| In this lesson | Yes. | **No.** You don't create an account or publish anything. |

You'll meet GitHub and similar services when you want to share your work with others. Today the whole history stays on your computer.

Three new words:

- A **repository** is a folder whose history Git keeps.
- A **commit** is one saved version, with a description, an author and a date.
- **Version control** is exactly this: saving such versions and comparing them.

## 2. Install Git

### Windows

You install Git the same way as the tools in lesson 0.4, with Chocolatey.

1. Open a terminal **as administrator** (lesson 0.4, section 3).
2. Type:

   ```text
   choco install git -y
   ```

3. When the installation finishes, close the terminal and open a **new, ordinary** one. Only a new terminal knows about the new program (`PATH`, lesson 0.3).

### macOS

You already have Git: Apple includes it in the *Command Line Tools*, which you installed in lesson 0.4. You don't install anything; you only check the version.

If a window asking to install developer tools appears when you check, the *Command Line Tools* are missing. Go back to lesson 0.4 in that case. You can install a newer Git with Homebrew (`brew install git`), but this lesson doesn't need it.

### Ubuntu

In the terminal, type:

```text
sudo apt install -y git
```

The system asks for your password, as in lesson 0.4.

### Check

On every system:

```text
git --version
```

You'll see a version number, for example `git version 2.56.0.windows.2` (Windows), `git version 2.39.5 (Apple Git-154)` (macOS) or `git version 2.43.0` (Ubuntu). Your number may differ. Any version from the last few years is enough for this lesson.

## 3. Create a repository in `cpp-workspace`

One repository will cover your whole `cpp-workspace`: all your projects will share one history. You create the repository in your own working folder, not in the folder with the course materials.

**Step 1. Go to `cpp-workspace`:**

```text
cd ~
cd cpp-workspace
```

Check with `ls` (`ls -F` on macOS and Ubuntu). You see your projects: `lesson_1_1`, `parcel_label`, `cinema_ticket` and others.

**Step 2. Make sure it isn't a repository yet:**

```text
git status
```

The expected result is an **error**, and that's good news:

```text
fatal: not a git repository (or any of the parent directories): .git
```

Git checked this folder and all the folders above it, and found no repository anywhere. So you can safely create a new one. If you see `On branch …` instead, **stop** and read section 10.

**Step 3. Create the repository:**

```text
git init
```

The last line of the output is, for example:

```text
Initialized empty Git repository in /home/ola/cpp-workspace/.git/
```

Before it, there may be lines starting with `hint:`, with a hint about a branch name. Skip them for now. You'll learn about branches later, and whether the name is `master` or `main` doesn't matter today.

`git init` created a hidden folder **`.git`**. Git keeps the whole history there. Don't change anything in it by hand, and **never delete it**: deleting `.git` deletes the whole history. You can see it with `ls -Force` (Windows) or `ls -a` (macOS and Ubuntu).

**Step 4. See the state of the repository:**

```text
git status
```

```text
On branch master

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        build_detective/
        cinema_ticket/
        lesson_1_1/
        ...

nothing added to commit but untracked files present (use "git add" to track)
```

**Describe what you see:** what do `No commits yet` and `Untracked files` mean?

<details>
<summary>Answer</summary>

`No commits yet`: there is no version in the history yet. `Untracked files`: files Git doesn't track yet. It sees them in the folder, but they aren't in the history. The list shows your project folders. On macOS there may also be a `.DS_Store` file, which Finder creates.

</details>

## 4. Introduce yourself to Git

Every commit records **who** created it: a name and an email address. Set them for this repository, in the `cpp-workspace` folder:

```text
git config user.name "<your name or a nickname>"
git config user.email "<your email address>"
```

Instead of the text in angle brackets, type **your own** details, and remove the `<` and `>`. Keep the quotes. Check:

```text
git config user.name
```

**Local or global?**

- Without an extra option, as here, the setting applies **only to this repository**. It's stored in `.git` and doesn't affect other projects on your computer.
- With the `--global` option, it would apply to **all** repositories of your account. You don't use it today.

**Privacy.** The name and email stay in the history of every commit. If you ever publish the repository, everyone will see them. You may use a nickname. How to hide your email address when publishing, you'll learn when the time comes.

## 5. What should go into the history? `.gitignore`

See **all** the files Git sees, including those inside folders:

```text
git status --untracked-files=all
```

The list is long. Here is a part of it:

```text
cinema_ticket/.idea/workspace.xml
cinema_ticket/CMakeLists.txt
cinema_ticket/cmake-build-debug/CMakeCache.txt
cinema_ticket/cmake-build-debug/first_program
cinema_ticket/main.cpp
...
lesson_1_4/build-terminal/CMakeCache.txt
lesson_1_4/build-terminal/first_program
lesson_1_4/build-terminal/hello_cmake
lesson_1_4/hello
lesson_1_4/main.o
```

Your list depends on what was built and what was opened in CLion. The files fall into four groups:

| Group | Examples | Into the history? |
|---|---|---|
| **Your code** | `main.cpp`, `CMakeLists.txt` | **Yes.** This is your work. |
| **Build results** | `build-terminal/`, `cmake-build-debug/`, `main.o`, `hello`, `.exe` files | **No.** The tools recreate them from your code at any time. They change with every build, take up a lot of space and contain paths from your computer. |
| **CLion settings** | `.idea/` folders | **No.** They are CLion's settings for this computer, not part of the program. |
| **System files** | `.DS_Store` (macOS) | **No.** Finder creates them. |

A **`.gitignore`** file tells Git which files not to show and not to add. Create it in `cpp-workspace` with one command:

**Windows (PowerShell):**

```text
Set-Content .gitignore 'build-terminal/', 'cmake-build-*/', '.idea/', '*.o', '*.obj', '*.exe', '/lesson_1_4/hello', '.DS_Store'
```

**macOS and Ubuntu:**

```text
printf '%s\n' 'build-terminal/' 'cmake-build-*/' '.idea/' '*.o' '*.obj' '*.exe' '/lesson_1_4/hello' '.DS_Store' > .gitignore
```

See what was created: `Get-Content .gitignore` (Windows) or `cat .gitignore` (macOS and Ubuntu). It's an ordinary text file, with one rule per line:

| Rule | What it leaves out |
|---|---|
| `build-terminal/` | terminal build folders, in every project |
| `cmake-build-*/` | CLion's build folders, for example `cmake-build-debug/` |
| `.idea/` | CLion's settings |
| `*.o`, `*.obj` | object files (lesson 1.4) |
| `*.exe` | programs on Windows |
| `/lesson_1_4/hello` | the `hello` program from lesson 1.4 on macOS and Ubuntu. It's one specific file, so that no project with a similar name gets hidden by accident. |
| `.DS_Store` | Finder files on macOS |

The file is the same on all systems. Rules that don't apply to your system simply do nothing.

Check again:

```text
git status --untracked-files=all
```

Now each project shows only `main.cpp` and `CMakeLists.txt`, plus the new `.gitignore`. The tools can still create those files and folders; Git simply leaves them out.

**Important:** `.gitignore` only works for files that Git **doesn't track yet**. If a file is already in the history, adding it to `.gitignore` doesn't remove it from there (section 10). That's why you create `.gitignore` **before** the first commit.

## 6. Your first commit

You'll start with one finished project: the cinema ticket from the lesson 1.3 mission. If you don't have a `cinema_ticket` folder, choose another finished project and use its name in the commands.

**Step 1. Choose the files.** Name them exactly, one by one:

```text
git add .gitignore cinema_ticket/main.cpp cinema_ticket/CMakeLists.txt
```

You write the paths with `/` on all systems, also in PowerShell. Git understands them.

On Windows, a warning may appear:

```text
warning: in the working copy of 'cinema_ticket/main.cpp', LF will be replaced by CRLF the next time Git touches it
```

Systems mark the end of a line in text files differently: Windows with two characters (CRLF), macOS and Linux with one (LF). Git on Windows is set up to store one form in the history and use the Windows form in your folder. The warning only says that. Your file and your program are fine, and you don't need to do anything.

**Step 2. Check what is prepared:**

```text
git status
```

```text
On branch master

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
        new file:   .gitignore
        new file:   cinema_ticket/CMakeLists.txt
        new file:   cinema_ticket/main.cpp

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        build_detective/
        lesson_1_1/
        ...
```

`git add` doesn't save a version yet. It copies the current content of the chosen files into the **staging area**: the place where you put together the next commit. `Changes to be committed` is exactly what's in the staging area. The other projects wait in `Untracked files` and won't go into this commit.

You can see the content of the prepared changes with `git diff --staged`. When the output is longer than the screen, Git shows it page by page: <kbd>Space</kbd> shows the next page and <kbd>q</kbd> quits.

**Step 3. Save the version:**

```text
git commit -m "Add the cinema ticket and .gitignore"
```

`-m` gives the **commit message**. A good message says briefly what this version brings. In this course, write messages without accented letters for now, for the same reason as program output: not every Windows console shows them correctly. The output:

```text
[master (root-commit) 6d29aa9] Add the cinema ticket and .gitignore
 3 files changed, 25 insertions(+)
 create mode 100644 .gitignore
 create mode 100644 cinema_ticket/CMakeLists.txt
 create mode 100644 cinema_ticket/main.cpp
```

`6d29aa9` is the start of the **commit identifier**. Yours will be different, because it depends on the content, the author and the time.

**Step 4. Check the state:** `git status`. The ticket's files have disappeared from the list, because they are saved in the history and haven't changed since. Only the other projects are left.

**Step 5. See the history:**

```text
git log
```

```text
commit 6d29aa9f9b6ce4e27c45ff2258689f60a553dc0c
Author: (your name and email from section 4)
Date:   Tue Oct 20 18:28:10 2026 +0000

    Add the cinema ticket and .gitignore
```

You'll see your own details, date and identifier. If the output doesn't fit, <kbd>q</kbd> quits.

**Saving a file vs. a commit.** <kbd>Ctrl</kbd> + <kbd>S</kbd> in the editor saves the file on disk: there is only one, current content, and you overwrite the previous one. A commit saves **a version in the history**: it's created only when you decide, and all earlier versions stay.

## 7. Change the program and save a second version

Less guidance now.

1. In `cinema_ticket/main.cpp`, change the row and seat number, for example `Row 7, seat 12` to `Row 9, seat 5`. Build and run the program as in lesson 1.3, to check that it works.
2. **Predict** what `git status` will show, then check.
3. See the change: `git diff`.
4. Prepare the change for a commit, and check what's in the staging area.
5. Save a second commit with a message that says what changed.
6. See the history in short: `git log --oneline`.

<details>
<summary>Hint: which commands?</summary>

The same as in section 6: first you check (`git status`, `git diff`), then you choose (`git add` with the file name), check again (`git status` or `git diff --staged`) and save (`git commit -m "…"`).

</details>

`git diff` shows the difference between the last saved version and the file on disk:

```text
diff --git a/cinema_ticket/main.cpp b/cinema_ticket/main.cpp
index 9483a09..7c49361 100644
--- a/cinema_ticket/main.cpp
+++ b/cinema_ticket/main.cpp
@@ -3,7 +3,7 @@
 int main() {
     std::cout << "CINEMA TICKET\n";
     std::cout << "Film: \"The Long Night\"\n";
-    std::cout << "Row 7, seat 12\n";
+    std::cout << "Row 9, seat 5\n";
     // Each \\ in the code prints one backslash.
     std::cout << "File: C:\\tickets\\night.txt\n";
     std::cout << "Enjoy the film!\n";
```

The line with `-` is the old content, and the line with `+` is the new one. The other lines are the surroundings, so you can see where the change is. `@@ -3,7 +3,7 @@` says at which line the shown part starts.

After `git add`, a plain `git diff` shows nothing any more, because the file matches the staging area. `git diff --staged` shows the change in the staging area.

`git log --oneline` after the second commit:

```text
63f6aee Change the seat on the ticket
6d29aa9 Add the cinema ticket and .gitignore
```

**See the previous version.** This is the answer to the problem from the start of the lesson. Take the identifier of the **first** commit from `git log --oneline` and type:

```text
git show 6d29aa9:cinema_ticket/main.cpp
```

Instead of `6d29aa9`, type your own identifier. Write the file path with `/`, also on Windows. Git prints the file **as it was in that version**, with `Row 7, seat 12`. Your file on disk hasn't changed: it still has the new version. Git keeps every saved version, and you can look at any of them.

## 8. Mission: keep two stages of your work

Choose **another** project of yours in `cpp-workspace`, for example `parcel_label`, `shopping_list` or `build_detective`. Your task:

1. Check the state of the repository.
2. Save a commit with the working version of this project: only its source files.
3. Make a concrete change to the program, for example add a line of output or change a text. Build and run the program.
4. See the difference.
5. Save a second commit.
6. Explain in your own words what changed between these two versions.

### Success criteria

- `git log --oneline` shows two new commits with messages that say what each version brings.
- `git status` doesn't show any files of this project: neither modified nor untracked.
- `git ls-files <project folder>` (the list of files saved in the history) shows only this project's `main.cpp` and `CMakeLists.txt`: no build results and no CLion settings.
- You can point out which lines changed and why, for example using `git show <identifier>`, which shows the changes a commit made.

<details>
<summary>Hint 1</summary>

First you check, then you choose, then you check again, and finally you save. Go back to the order in section 7.

</details>

<details>
<summary>Hint 2</summary>

Which command shows the change **before** `git add`, and which one **after**? If `git status` still shows the project's files after the commit, something was left in the staging area, or outside it.

</details>

An example walk-through is in [Example solutions](#example-solutions).

## 9. Optional: the other projects

Once you know that `.gitignore` works, you can add whole project folders instead of single files:

```text
git add lesson_1_1 lesson_1_2 lesson_1_3 lesson_1_4 shopping_list build_detective
```

Type only the folders you actually have and haven't saved yet. **Before you commit**, check `git status`: `Changes to be committed` should list only `main.cpp` and `CMakeLists.txt` files. Then save a commit, for example `git commit -m "Add the other projects"`.

In this course you don't add everything at once (`git add .`). You choose files or folders deliberately and check them before saving.

**Git in CLion.** CLion can also show Git changes and history (the **Commit** and **Git** windows). This course doesn't need them: the terminal commands do the same and work the same way in any environment.

## 10. When something goes differently

| What you see | What it means | What to do |
|---|---|---|
| `git` is not recognised | The terminal doesn't know Git yet. | Close the terminal and open a new one (on Windows an ordinary one, not the administrator one). Check `git --version`. If it still doesn't work, repeat the installation. Don't change the `PATH` variable by hand. |
| `git status` **before** `git init` shows `On branch …` | The folder is already inside another repository. | **Don't run `git init`**, and don't delete anything. `git rev-parse --show-toplevel` shows where that repository starts. Check that `cpp-workspace` is where it should be (in your home folder, lesson 1.1). |
| `Author identity unknown` and `Please tell me who you are` on `git commit` | Git doesn't know who you are. | Set your name and email (section 4) and repeat `git commit`. |
| A text editor opened in the terminal | A commit without `-m "…"`: Git is waiting for the message in an editor. | The simplest fix is to give up and repeat with `-m`. In the *Vim* editor (common on Windows and macOS), press <kbd>Esc</kbd>, type `:q!` and press <kbd>Enter</kbd>. In the *nano* editor (common on Ubuntu), press <kbd>Ctrl</kbd> + <kbd>X</kbd>. No commit is created. |
| The `git log`/`git diff` output doesn't end, and there's a `:` at the bottom | Git shows long output page by page. | <kbd>Space</kbd> shows the next page, <kbd>q</kbd> quits. |
| `LF will be replaced by CRLF` (Windows) | Information about line endings (section 6). | Do nothing. |
| The wrong file went into the staging area | `git add` chose too much. | `git restore --staged <file>` takes it out of the staging area. The file on disk doesn't change. |
| `The following paths are ignored by one of your .gitignore files` | You're trying to add a file that `.gitignore` leaves out. | That's protection against a mistake. Don't add it. |
| A build file is already in the history | It was added before `.gitignore` existed. | `git rm --cached <file>`, then a commit. The file stays on disk; it only disappears from the next versions in the history. |
| `git show` with `\` in the path finds no file (Windows) | In `identifier:path`, Git expects `/`. | Type the path with `/`, for example `cinema_ticket/main.cpp`. |

Don't delete the `.git` folder to "start over": you lose the whole history. Every problem in this table is solved without that.

## 11. Explain

Answer in your own words, preferably in writing. Only then compare with the example answer.

**1.** How does Git differ from GitHub? Did this lesson need the internet?

<details>
<summary>Example answer</summary>

Git is a program on my computer that saves the history of changes. GitHub is an internet service for storing repositories and working together. This lesson needed the internet only to install Git. The repository and the commits are on my computer.

</details>

**2.** What is `git add` for, if you still have to run `git commit`?

<details>
<summary>Example answer</summary>

`git add` chooses what goes into the next commit (the staging area), and `git commit` saves exactly what was chosen. This way I decide which files and changes I save, and I can check them before saving.

</details>

**3.** Why don't `build-terminal/` and `.idea/` go into the history?

<details>
<summary>Example answer</summary>

Because they aren't my code. The tools can recreate the build results at any time, and CLion's settings only apply to this computer. In the history they would take up space and clutter every change.

</details>

**4.** How does the output of `git diff` differ from `git diff --staged`?

<details>
<summary>Example answer</summary>

`git diff` shows changes in the files on disk that haven't been prepared for a commit yet. `git diff --staged` shows the changes prepared in the staging area, that is, what the next commit will save.

</details>

**5.** How does saving a file in the editor differ from a commit?

<details>
<summary>Example answer</summary>

Saving a file overwrites its content on disk, and only the latest version remains. A commit saves a chosen version in the history, with a message, an author and a date, and the earlier versions stay and can be looked at.

</details>

## Summary

- Git saves the history of chosen files locally, without the internet and without an account. GitHub is a separate internet service.
- `git init` creates a repository, and its history is in the hidden `.git` folder. Before `git init`, check `git status`: the expected result is `not a git repository`.
- You set your identity for the repository (`git config user.name`, `git config user.email`), without `--global`.
- `.gitignore`, created before the first commit, leaves out build results and IDE settings.
- Working with Git is a loop: **check (`git status`, `git diff`) → choose (`git add` with names) → check (`git diff --staged`) → save (`git commit -m "…"`) → look (`git log`)**.
- You can look at any earlier version (`git show <identifier>:<path>`) without changing the files on disk.

## What's next

You now have a history of your work. **Lesson 1.6 is in preparation.**

---

## Example solutions

Look here **after your own attempt**. Your identifiers, dates and messages will be different.

<details>
<summary>Section 7: an example walk-through</summary>

```text
git status
git diff
git add cinema_ticket/main.cpp
git diff --staged
git commit -m "Change the seat on the ticket"
git log --oneline
```

After the change, `git status` shows `modified:   cinema_ticket/main.cpp` under `Changes not staged for commit`. After `git add`, the same file is under `Changes to be committed`, and after the commit it disappears from the `git status` output.

</details>

<details>
<summary>Section 8: the mission, an example walk-through for <code>parcel_label</code></summary>

```text
git status
git add parcel_label/main.cpp parcel_label/CMakeLists.txt
git status
git commit -m "Add the parcel label"
```

Then a change in `parcel_label/main.cpp`, building and running the program, and then:

```text
git diff
git add parcel_label/main.cpp
git diff --staged
git commit -m "Print the sender's address on the label"
git log --oneline
git ls-files parcel_label
```

`git ls-files parcel_label` shows only:

```text
parcel_label/CMakeLists.txt
parcel_label/main.cpp
```

An explanation of the change, for example: "In the second version, the program prints an extra line with the sender's address. `git diff` showed it as one line with `+` and none with `-`, because nothing was removed."

</details>

**Previous lesson:** [Lesson 1.4: From source code to an executable](lesson_04_from_source_code_to_an_executable.en.md) · **Next lesson:** in preparation · [Course overview](../../README.en.md)

# Lesson 0.4: Set up your workshop: installing the tools

[Polski](lesson_04_installing_the_tools.md) · **English** · [Course overview](../../README.en.md)

> **Module 0, lesson 4** · usually 30 minutes to 2 hours, depending on your computer and internet speed
> **You need:** a computer running Windows 10/11, macOS or Ubuntu 24.04, internet access, a few gigabytes of free disk space and **administrator rights** (see [section 2](#2-before-you-start-installing)).

## Before you start

This lesson assumes that after lessons [0.1](lesson_01_files_and_terminal.en.md), [0.2](lesson_02_moving_between_folders.en.md) and [0.3](lesson_03_commands_and_programs.en.md):

- you can open a terminal and move between folders;
- you know that a command can start a separate program, and that the shell looks for programs in the folders on the `PATH` list;
- you know that a **compiler** turns source code into a program.

## The situation

From lesson 0.3 you know the way from text to program:

```text
source code  →  compiler  →  program
```

Your computer doesn't have a C++ compiler yet. In this lesson you will set up the whole workshop: install the tools you need and check that they are in place. In the next lesson you will use them to run your first C++ program.

After this lesson you will:

- know what each tool you install is for;
- have the course tools installed on your system;
- be able to check their versions in the terminal;
- be able to tell whether you are using the right compiler.

## 1. Understand: what you install, and why

| Tool | What it is for | When you will use it |
|---|---|---|
| **LLVM/Clang 22**, with the `clang++` compiler | The C++ compiler: turns your code into a program. | In the next lesson, for your first program |
| **System tools**: on Windows *Visual Studio Build Tools*, on macOS the *Command Line Tools*, on Ubuntu packages the system installs together with Clang | Ready-made parts that every C++ program uses, such as the **standard library** (ready-made code for printing text or doing calculations), plus the operating system files needed to build a program. | Every time you compile, although you never start them yourself |
| **CMake** | Describes which files make up a project and how to build it. | From the next lesson |
| **Ninja** | Quickly carries out the build steps prepared by CMake. | From the next lesson, “behind the scenes” |
| **CLion** | The development environment (IDE): where you write, run and check your programs. | From the next lesson |

You don't need to understand yet how these tools work inside. It's enough to know what they are for.

You will install most of them with a **package manager**. That's a program that downloads and installs other programs from a trusted source and keeps track of their versions. On Windows you will use **Chocolatey**, on macOS **Homebrew**, and on Ubuntu the built-in **apt**.

## 2. Before you start installing

- **Administrator rights.** Installing system tools needs an account with administrator rights. On Windows you will start the terminal “as administrator”. On macOS and Ubuntu the system will ask for your password.
- **A school, university or work computer.** It often doesn't give you administrator rights. In that case, ask the computer's administrator to install the tools listed in this lesson. Don't look for ways around the restrictions on the internet: it's easy to end up installing something other than what you need.
- **Typing a password in the terminal.** When the terminal asks for a password, **you won't see the characters you type**, not even asterisks. That's normal. Type the password and press <kbd>Enter</kbd>.
- **Long commands.** Some commands in this lesson are long. You can copy and paste them. On Windows and macOS, use the usual shortcut. In the Ubuntu terminal, use <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>V</kbd>.
- **Follow only the part for your system.** Section 3 has separate instructions for Windows, macOS and Ubuntu.

## 3. Install the tools

### Windows

**Step 1. Visual Studio Build Tools.**

1. Download the installer from Microsoft: [Build Tools for Visual Studio 2022](https://aka.ms/vs/17/release/vs_buildtools.exe).
2. Run the downloaded file. The *Visual Studio Installer* opens.
3. On the **Workloads** tab, select **Desktop development with C++**. Leave the other settings as they are.
4. Click **Install** and wait until it finishes. This can take a while, and the installation takes up several gigabytes. If the installer asks you to restart the computer, do so.

This does not install the Visual Studio program. You only get the parts `clang++` will use: the standard library and the Windows system files.

**Step 2. Chocolatey.**

1. Open a terminal **as administrator**: in the Start menu, type `Terminal`, right-click **Terminal** and choose **Run as administrator**.
2. Go to [chocolatey.org/install](https://chocolatey.org/install), choose the **Individual** installation and copy the command shown there.
3. Paste the command into the terminal and press <kbd>Enter</kbd>.
4. When the installation finishes, **close the terminal and open a new one, again as administrator**. The new terminal knows about the new programs (remember `PATH` from lesson 0.3).

**Step 3. LLVM, CMake and Ninja.** In the administrator terminal, type these one by one:

```text
choco install llvm --version=22.1.8 -y
choco install cmake --installargs '"ADD_CMAKE_TO_PATH=System"' -y
choco install ninja -y
```

The `--installargs '"ADD_CMAKE_TO_PATH=System"'` part asks the CMake installer to add CMake to the `PATH` list. Without it, the `cmake` command won't work in the terminal.

**Step 4.** Close the administrator terminal and open a **normal** one. Checking the tools, and all further work, happens without administrator rights.

### macOS

**Step 1. Command Line Tools.** In the terminal, type:

```text
xcode-select --install
```

A window opens asking whether to install the tools. Click **Install** and wait. You get the macOS system files, the linker and other tools the compiler will use. If you see a message that the tools are already installed, move on.

**Step 2. Homebrew.**

1. Go to [brew.sh](https://brew.sh), copy the installation command from the *Install Homebrew* section and paste it into the terminal.
2. The installer asks for your account password.
3. At the end, the installer prints a **Next steps** section with a few commands. **Run them**: they add Homebrew to the `PATH` list.
4. Close the terminal and open a new one. Check `brew --version`.

**Step 3. LLVM 22, CMake and Ninja.**

```text
brew install llvm@22 cmake ninja
```

The `llvm@22` formula is LLVM from the 22 series. Homebrew deliberately **doesn't add** it to the `PATH` list, so that it doesn't hide the compiler supplied by Apple. That's why in section 4 you will start it by its full path.

### Ubuntu 24.04

**Step 1. Programs needed to add the package source.**

```text
sudo apt update
sudo apt install -y wget gnupg ca-certificates
```

`sudo` means “run as administrator”, so the system will ask for your password. Most Ubuntu computers already have these programs, in which case `apt` simply says so.

**Step 2. Add the LLVM package source.** Ubuntu's own packages contain an older version of Clang, and we need version 22. So you add the official package source of the LLVM project ([apt.llvm.org](https://apt.llvm.org)) to the system:

```text
wget -qO- https://apt.llvm.org/llvm-snapshot.gpg.key | sudo tee /etc/apt/trusted.gpg.d/apt.llvm.org.asc
echo "deb https://apt.llvm.org/noble/ llvm-toolchain-noble-22 main" | sudo tee /etc/apt/sources.list.d/llvm-22.list
```

The first command saves a key that lets the system check that the packages really come from LLVM. The second adds the address of the source. Both print what they saved in the terminal. That's normal.

**Step 3. LLVM 22, CMake and Ninja.**

```text
sudo apt update
sudo apt install -y clang-22 cmake ninja-build
```

Together with `clang-22`, the system automatically installs the C++ standard library and the other system tools the compiler uses. You don't need to pick them by hand.

### CLion (every system)

1. Download CLion from [jetbrains.com/clion/download](https://www.jetbrains.com/clion/download/) and install it like any other program. On Ubuntu you can also use the command `sudo snap install clion --classic`.
2. Start CLion. On the first start, choose a licence. If you learn on your own, you can choose the free licence **for non-commercial use**. It needs a JetBrains account, and its condition is that CLion sends anonymous usage statistics to JetBrains, which you can't switch off. Schools and universities have separate licences for computer labs, so on a school computer ask your teacher or the administrator.
3. If CLion offers to create a project or set up tools, you can close that window. You will set it up in the next lesson.

## 4. Check: is your workshop ready?

Open a **new** normal terminal and type the commands for your system.

### The compiler

| System | Command | What to look for in the output |
|---|---|---|
| Windows | `clang++ --version` | `clang version 22.1.8` and `Target: x86_64-pc-windows-msvc` |
| Windows | `Get-Command clang++` | the path `C:\Program Files\LLVM\bin\clang++.exe` |
| macOS | `brew --prefix llvm@22`, then the full path from the output followed by `/bin/clang++ --version`, for example `/opt/homebrew/opt/llvm@22/bin/clang++ --version` | `Homebrew clang version 22.1.8` |
| Ubuntu | `clang++-22 --version` | `clang version 22.1.8`, for example `Ubuntu clang version 22.1.8 (++…)` |

What matters is the **major version number: 22**. The last digits (`.8`) may differ if the lesson says so.

### Is it the right compiler?

One computer can have several compilers with similar names. From lesson 0.3 you know that the shell starts the first program with a given name that it finds. Check:

- **macOS:** type just `clang++ --version`. You will see `Apple clang version …`. That's **Apple's compiler**, not ours. It's part of the system and does no harm, but in this course we use Homebrew clang, by its full path.
- **Ubuntu:** just `clang++ --version` may show an older version, such as `Ubuntu clang version 18…`, or report that the command doesn't exist. Our compiler is `clang++-22`, with the number in its name.
- **Windows:** `Get-Command clang++` must point to the `C:\Program Files\LLVM\bin` folder. If it points somewhere else, such as a Visual Studio or MinGW folder, see section 6.

### CMake and Ninja

| Command | What to look for |
|---|---|
| `cmake --version` | `cmake version 3.28` or newer (for example 4.x) |
| `ninja --version` | a version number, for example `1.11.1` or `1.13.2` |

### System tools

- **Windows:** open **Visual Studio Installer** from the Start menu. The list should include **Visual Studio Build Tools 2022**, with the *Desktop development with C++* workload installed.
- **macOS:** `xcode-select -p` shows a path, for example `/Library/Developer/CommandLineTools`.
- **Ubuntu:** they are installed automatically together with `clang-22`. You don't need to check them separately.

## 5. Mission: workshop report

Fill in the table for your computer:

| Tool | Command you check it with | Your version | Right one? (yes/no) |
|---|---|---|---|
| `clang++` compiler (LLVM 22) | | | |
| CMake | | | |
| Ninja | | | |
| system tools | | | |
| CLion | starting the program | | |

For each row, add one sentence saying **what** that tool will be used for in the next lesson.

### Success criterion

- The compiler reports **version 22** and is **our** compiler: on Windows from `C:\Program Files\LLVM\bin`, on macOS “Homebrew clang” (not “Apple clang”), on Ubuntu `clang++-22`.
- `cmake --version` shows 3.28 or newer, and `ninja --version` prints a version.
- The system tools are installed (checked as in section 4).
- CLion starts.

If everything matches, your workshop is ready. You don't need to compile anything yet: you will do that in the next lesson.

## 6. When things look different

| What you see | What it means | What to do |
|---|---|---|
| A command is not recognised right after installing (`… is not recognized…` or `command not found`) | A terminal opened before the installation has the old `PATH` list. | Close the terminal and open a new one. If that doesn't help, check that the installation finished without errors. |
| Windows: Chocolatey reports that it isn't running in a terminal with administrator rights | The installation needs administrator rights. | Open the terminal with **Run as administrator** (section 3, step 2). |
| No administrator rights on a school or work computer | You can't install these tools without them. | Ask the computer's administrator to install them. Don't use workarounds from the internet. |
| Ubuntu: `E: Unable to locate package clang-22` | The system doesn't know the LLVM package source. | Check that both commands from step 2 were run, then run `sudo apt update`. |
| macOS: `clang++ --version` shows `Apple clang` | That's Apple's compiler, not ours. | That's expected. You start our compiler by the full path from section 4. |
| Ubuntu: `clang++ --version` shows version 18 | That's the older Clang from Ubuntu's own packages. | Use `clang++-22`. |
| Windows: `Get-Command clang++` shows a path other than `C:\Program Files\LLVM\bin` | There is another `clang++` on the computer, which the shell finds first. | Don't uninstall anything blindly. Write down that path. In the next lesson we will give CLion the full path to the right compiler. |
| Windows: the Build Tools installer asks for a restart | Some files are completed after the restart. | Restart the computer, then go on to step 2. |
| The compiler is installed, but later your first compilation reports missing files, such as `'iostream' file not found` or, on Windows, `lld-link: error: could not open 'kernel32.lib'` | The system tools with the standard library are missing. | Come back to this lesson and check the system tools (section 4). This kind of problem only shows up when compiling, in the next lesson. |

## 7. Explain it

Answer in your own words, and only then expand the answer.

**1.** Why do you install system tools (Build Tools on Windows, the Command Line Tools on macOS) when you already have a compiler? What does Ubuntu do about them?

<details>
<summary>Answer</summary>

The compiler alone is not enough. C++ programs use the standard library and operating system files, and those are exactly what the system tools provide. On Ubuntu, the system installs them automatically together with `clang-22`.

</details>

**2.** Why do you have to open a new terminal after installing?

<details>
<summary>Answer</summary>

A terminal reads the `PATH` list when it starts. An old terminal doesn't know about folders the installer added later.

</details>

**3.** On macOS, `clang++ --version` shows “Apple clang”, while the full Homebrew path shows “Homebrew clang version 22”. How is that possible when the command has the same name?

<details>
<summary>Answer</summary>

They are two different programs with the same name, in different folders. The shell starts the first one it finds on the `PATH` list, while the full path points to one specific file, just like running `whoami` by its full path in lesson 0.3.

</details>

**4.** What will CMake and Ninja be used for in the next lesson?

<details>
<summary>Answer</summary>

CMake will describe how to build the project, and Ninja will carry out the build steps. Together, using the compiler, they turn source code into a program.

</details>

## Summary

- You have a ready C++ workshop: the `clang++` compiler from LLVM 22, the system tools, CMake, Ninja and CLion.
- You know what each of these tools is for.
- You can check their versions and tell whether you are using the right compiler.
- After installing something, open a new terminal.

**Previous lesson:** [Lesson 0.3: What happens when you type a command?](lesson_03_commands_and_programs.en.md) · **Next lesson:** [Lesson 0.5: Your first working program in CLion](lesson_05_first_program_in_clion.en.md) · [Course overview](../../README.en.md)

# Lesson command checks

Small scripts that check that the terminal commands taught in the lessons still behave the way the lessons describe them. Run them whenever a lesson's commands or the described behaviour change.

## What this does and does not verify

A passing run means: **the commands in the lessons do what the lessons say, in the shells we tested**.

It does **not** mean that the lesson is correct or good as teaching material. These checks cannot tell whether a learner:

- finds the right option in a graphical interface (file windows, menus, opening a terminal);
- understands an explanation, or can solve the mission on their own;
- copes with an unusual computer setup, a localised system, or a shell configuration we did not test.

Those need a human review of the lesson and a walk-through on real computers.

The checks verify behaviour, such as where `cd` leads, what is a folder or a file, and whether file contents survive. They do not compare full shell messages or formatted output, because those differ between shells, versions and system languages.

## Layout

```text
tests/lessons/
  lib.sh / lib.ps1          shared helpers: temporary folder, fake home folder, checks, cleanup
  module_00_tooling/
    lesson_01.sh / .ps1     checks for lesson 0.1
    lesson_02.sh / .ps1     checks for lesson 0.2
    lesson_03.sh / .ps1     checks for lesson 0.3
```

- **`.sh`** files cover the macOS and Linux instructions and run in both **bash** and **zsh**.
- **`.ps1`** files cover the Windows instructions and run in **Windows PowerShell 5.1** and **PowerShell 7**. On other systems they print `SKIPPED` and exit successfully.

When the Polish and English versions of a lesson use different folder or file names, the same checks run once with each set of names.

## Running locally

From the repository root.

macOS or Linux:

```sh
zsh  tests/lessons/module_00_tooling/lesson_02.sh
bash tests/lessons/module_00_tooling/lesson_02.sh
```

Windows:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File tests\lessons\module_00_tooling\lesson_02.ps1
pwsh -NoProfile -File tests\lessons\module_00_tooling\lesson_02.ps1
```

`-ExecutionPolicy Bypass` applies only to that one `powershell` process. No internet access or extra tools are needed.

Each check prints `ok` or `FAIL` with the expected and actual values. The script exits with a non-zero status if any check failed.

## Safety

- Everything happens in a new temporary folder named `lesson-check.*`, which is removed when the script exits, also on failure.
- The home folder is replaced by a fake one inside that temporary folder. On macOS and Linux `HOME` is changed for the script's own process only. In PowerShell the FileSystem provider's home folder, which `~` uses, is changed and restored afterwards. `cd ~`, plain `cd` and `ls ~` therefore never reach your real home folder.
- The only thing outside the temporary folder is read-only navigation to the root folder (`cd ..` until it stops), which lesson 0.2 describes.
- In CI, the workflow also checks that the runner's real home folder is unchanged and that no `lesson-check.*` folders are left behind.

## Continuous integration

`.github/workflows/lesson-commands.yml` runs all checks:

- on pull requests and pushes to `main` that change `course/**`, `tests/lessons/**` or the workflow itself;
- manually, via *Run workflow*.

It uses four environments:
- Windows PowerShell 5.1 on `windows-2025`;
- PowerShell 7 on `windows-2025`;
- bash on `ubuntu-24.04`;
- zsh on `macos-15`.

## Keeping the checks up to date

If a pull request changes a terminal command, or the behaviour a published lesson describes for it, check whether the matching lesson check needs an update in the same pull request.

You don't need a check for every sentence or example. Add one when a lesson makes a claim about command behaviour that could silently stop being true, such as an exact path, an error, or a difference between shells.

To cover a new lesson, add `lesson_XX.sh` and `lesson_XX.ps1` next to the existing ones. The workflow finds them automatically.

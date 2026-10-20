#!/usr/bin/env bash
# Checks the macOS/Linux commands taught in Module 0, lesson 0.3
# (course/module_00_tooling/lesson_03_commands_and_programs{.md,.en.md}).
# Run with bash or zsh:  bash lesson_03.sh   or   zsh lesson_03.sh
#
# The lesson reads `type` output, which bash may translate into the system
# language. These checks use `command -v` instead: it prints a path for a
# program file and just the name for a built-in command, in any language.

lesson_dir=$(cd "$(dirname "$0")" && pwd)
. "$lesson_dir/../lib.sh"

new_home lesson-03

# Section 2: whoami is a program that prints the account name.
expect_ok "whoami runs" whoami
expect_eq "whoami prints the account name" "$(id -un)" "$(whoami)"

# Section 3: type answers for a program and for a built-in command.
expect_ok "type whoami succeeds" type whoami
expect_ok "type cd succeeds" type cd
program=$(command -v whoami)
case "$program" in
    /*) pass "whoami is a separate program with a path" ;;
    *) fail "whoami is a separate program with a path" "command -v whoami printed: $program" ;;
esac
expect_ok "the whoami program is an executable file" test -f "$program" -a -x "$program"
expect_eq "cd is built into the shell (no file)" "cd" "$(command -v cd)"

# Section 4: running the program by its full path gives the same result.
expect_eq "running whoami by its full path gives the same result" "$(whoami)" "$("$program")"

# Section 6 (mission): pwd is built in; ls is a separate program
# (in scripts; an interactive Ubuntu shell may show an alias, as the lesson says).
expect_eq "pwd is built into the shell (no file)" "pwd" "$(command -v pwd)"
case "$(command -v ls)" in
    /*) pass "ls is a separate program with a path" ;;
    *) fail "ls is a separate program with a path" "command -v ls printed: $(command -v ls)" ;;
esac

# Section 7: unknown commands are reported; Get-Command does not exist here.
expect_fail "type on an unknown command reports an error" type no-such-command-here
expect_fail "Get-Command is not available in this shell" Get-Command whoami

finish "lesson 0.3 (sh)"

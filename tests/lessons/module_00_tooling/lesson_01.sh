#!/usr/bin/env bash
# Checks the macOS/Linux commands taught in Module 0, lesson 0.1
# (course/module_00_tooling/lesson_01_files_and_terminal{.md,.en.md}).
# Run with bash or zsh:  bash lesson_01.sh   or   zsh lesson_01.sh

lesson_dir=$(cd "$(dirname "$0")" && pwd)
. "$lesson_dir/../lib.sh"

# check_lesson LABEL FOLDER SUBFOLDER FILE
# Uses the folder and file names from one language version of the lesson.
check_lesson() {
    label=$1 folder=$2 subfolder=$3 file=$4
    printf -- '--- names from the %s lesson\n' "$label"
    new_home "$label"
    home=$(pwd)

    # Section 4: pwd prints the current folder as an absolute path.
    expect_eq "[$label] pwd prints the current folder" "$HOME" "$(pwd)"
    case "$(pwd)" in /*) pass "[$label] pwd prints an absolute path" ;;
        *) fail "[$label] pwd prints an absolute path" "actual: $(pwd)" ;; esac

    # Section 6: a folder created in the file window shows up in ls -F with a trailing /.
    mkdir "$folder"
    expect_eq "[$label] ls -F marks a folder with /" "$folder/" "$(listing)"
    expect_eq "[$label] ls -F . lists the same as ls -F" "$(listing)" "$(listing .)"

    # Section 7: touch with a relative path creates an empty file inside the folder.
    mkdir "$folder/$subfolder"
    expect_eq "[$label] touch prints nothing" "" "$(touch "$folder/$file" 2>&1)"
    expect_ok "[$label] touch creates the file inside the folder" test -f "$folder/$file"
    expect_fail "[$label] touch does not create the file in the current folder" test -e "$file"
    expect_fail "[$label] the new file is empty" test -s "$folder/$file"
    expect_eq "[$label] ls -F FOLDER shows exactly the file and the subfolder" \
        "$file $subfolder/" "$(listing "$folder")"

    # Section 8: the absolute path built from pwd reaches the same file.
    expect_eq "[$label] ls -F with the absolute path shows the file" \
        "$home/$folder/$file" "$(listing "$home/$folder/$file")"

    # Safety note: touch on an existing file keeps its contents.
    # (touch may update the file's timestamps; the lesson only promises the contents.)
    printf 'milk\n' > "$folder/$file"
    touch "$folder/$file"
    expect_eq "[$label] touch on an existing file keeps its contents" "milk" "$(cat "$folder/$file")"

    # Section 9: a path that does not exist is reported as an error.
    expect_fail "[$label] ls -F on a missing path reports an error" ls -F "no-such-folder"
}

check_lesson pl pierwszy-eksperyment notatki lista.txt
check_lesson en first-experiment notes list.txt

finish "lesson 0.1 (sh)"

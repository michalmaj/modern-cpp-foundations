#!/usr/bin/env bash
# Checks the macOS/Linux commands taught in Module 0, lesson 0.2
# (course/module_00_tooling/lesson_02_moving_between_folders{.md,.en.md}).
# Run with bash or zsh:  bash lesson_02.sh   or   zsh lesson_02.sh

lesson_dir=$(cd "$(dirname "$0")" && pwd)
. "$lesson_dir/../lib.sh"

# check_lesson LABEL TREE MUSEUMS BEACHES
# Uses the folder names from one language version of the lesson:
#   TREE/krakow/MUSEUMS and TREE/gdansk/BEACHES
check_lesson() {
    label=$1 tree=$2 museums=$3 beaches=$4
    printf -- '--- names from the %s lesson\n' "$label"
    new_home "$label"
    home=$(pwd)

    # Section 2: cd ~ goes home from anywhere.
    cd "$LESSON_TMP" || exit 1
    cd ~
    expect_eq "[$label] cd ~ goes to the home folder" "$home" "$(pwd)"

    # Section 3: the practice tree (created in the file window in the lesson).
    mkdir -p "$tree/krakow/$museums" "$tree/gdansk/$beaches"
    expect_eq "[$label] ls -F TREE shows both city folders" "gdansk/ krakow/" "$(listing "$tree")"

    # Section 4: the same relative path depends on the current folder.
    expect_fail "[$label] ls -F krakow fails from the home folder" ls -F krakow
    expect_eq "[$label] cd prints nothing" "" "$(cd "$tree" 2>&1)"
    cd "$tree"
    expect_eq "[$label] cd TREE changes the current folder" "$home/$tree" "$(pwd)"
    expect_eq "[$label] ls -F krakow works from TREE" "$museums/" "$(listing krakow)"

    # Section 5: cd .. goes to the parent folder.
    cd ..
    expect_eq "[$label] cd .. goes to the parent folder" "$home" "$(pwd)"

    cd "$tree/krakow/$museums"
    expect_eq "[$label] cd with a multi-level relative path" "$home/$tree/krakow/$museums" "$(pwd)"
    expect_eq "[$label] ls -F .. shows the contents of the parent folder" "$museums/" "$(listing ..)"
    expect_eq "[$label] ls -F .. does not change the current folder" "$home/$tree/krakow/$museums" "$(pwd)"
    expect_eq "[$label] ls -F ../.. shows two levels up" "gdansk/ krakow/" "$(listing ../..)"

    # Section 6: cd moves nothing; the tree is still in the home folder.
    cd "$home/$tree/krakow"
    expect_eq "[$label] ls -F ~ still shows TREE after cd" "$tree/" "$(listing ~)"
    expect_ok "[$label] the tree is still where it was" test -d "$home/$tree/krakow/$museums"

    # Section 7: an absolute path works from any current folder.
    cd "$home/$tree/krakow/$museums"
    cd "$home/$tree/gdansk"
    expect_eq "[$label] cd with an absolute path" "$home/$tree/gdansk" "$(pwd)"

    # Section 8, part A: one level at a time.
    cd "$home/$tree/krakow/$museums"
    cd .. && cd .. && cd gdansk && cd "$beaches"
    expect_eq "[$label] mission part A (step by step)" "$home/$tree/gdansk/$beaches" "$(pwd)"
    expect_eq "[$label] ls -F in an empty folder prints nothing" "" "$(ls -F)"

    # Section 8, part B: one command with a relative path.
    cd "$home/$tree/krakow/$museums"
    cd "../../gdansk/$beaches"
    expect_eq "[$label] mission part B (one command)" "$home/$tree/gdansk/$beaches" "$(pwd)"

    # Section 8, part C: back home with .. three times, and with ~.
    cd ../../..
    expect_eq "[$label] mission part C (cd ../../..)" "$home" "$(pwd)"
    cd "$home/$tree/gdansk/$beaches"
    cd ~
    expect_eq "[$label] mission part C (cd ~)" "$home" "$(pwd)"

    # Section 10: cd to a missing folder fails and leaves the current folder unchanged.
    expect_fail "[$label] cd to a missing folder reports an error" cd no-such-folder
    expect_eq "[$label] a failed cd leaves the current folder unchanged" "$home" "$(pwd)"
}

check_lesson pl plan-podrozy muzea plaze
check_lesson en trip-plan museums beaches

printf -- '--- shell behaviour described in the lesson\n'
new_home shell
home=$(pwd)
mkdir -p plan-podrozy/krakow

# Section 5: cd .. stops at the root folder.
cd "$LESSON_TMP/shell/home/plan-podrozy/krakow"
i=0
while [ "$i" -lt 64 ]; do
    before=$(pwd)
    cd ..
    [ "$(pwd)" = "$before" ] && break
    i=$((i + 1))
done
expect_eq "cd .. stops at the root folder" "/" "$(pwd)"
cd ..
expect_eq "cd .. in the root folder stays there" "/" "$(pwd)"

# Section 10: plain cd goes home on macOS and Linux.
cd "$home/plan-podrozy"
cd
expect_eq "plain cd goes to the home folder" "$home" "$(pwd)"

# Section 10: cd.. without a space is not a command here.
expect_fail "cd.. without a space reports an error" cd..

# Section 10: a backslash is not a separator on macOS and Linux.
# Unquoted on purpose, as a learner types it: the shell drops the backslash.
cd "$home"
expect_fail 'cd plan-podrozy\krakow reports an error' cd plan-podrozy\krakow
expect_eq "a failed cd leaves the current folder unchanged" "$home" "$(pwd)"

# Section 10: Linux distinguishes letter case. (macOS depends on the disk format, so it is not checked.)
if [ "$(uname)" = Linux ]; then
    expect_fail "Linux: cd with the wrong letter case reports an error" cd Plan-Podrozy
fi

finish "lesson 0.2 (sh)"

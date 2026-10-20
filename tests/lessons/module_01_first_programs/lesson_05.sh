#!/usr/bin/env bash
# Checks the macOS/Linux Git commands taught in Module 1, lesson 1.5
# (course/module_01_first_programs/lesson_05_save_the_history_of_your_work{.md,.en.md}).
# Run with bash or zsh:  bash lesson_05.sh   or   zsh lesson_05.sh
#
# Everything happens in a fake home folder inside a temporary folder. Git's
# global configuration is pointed at an empty file there (GIT_CONFIG_GLOBAL),
# so the runner's own Git settings are neither read nor changed. Checks look
# at behaviour (files, states, history), not at the exact wording of Git.

lesson_dir=$(cd "$(dirname "$0")" && pwd)
. "$lesson_dir/../lib.sh"
course=$(cd "$lesson_dir/../../.." && pwd)/course

new_home git
home=$(pwd)
: > "$LESSON_TMP/global-gitconfig"
GIT_CONFIG_GLOBAL="$LESSON_TMP/global-gitconfig"
export GIT_CONFIG_GLOBAL
printf -- '--- %s\n' "$(git --version)"

# A cpp-workspace as lessons 1.1-1.4 leave it: sources, plus what CMake, CLion,
# the linker and the file window create next to them.
ws="$home/cpp-workspace"
for project in lesson_1_1 parcel_label lesson_1_2 shopping_list lesson_1_3 cinema_ticket lesson_1_4 build_detective; do
    mkdir -p "$ws/$project"
    cp "$course/module_00_tooling/lesson_05_first_program/main.cpp" "$course/module_00_tooling/lesson_05_first_program/CMakeLists.txt" "$ws/$project/"
done
cat > "$ws/cinema_ticket/main.cpp" <<'EOF'
#include <iostream>

int main() {
    std::cout << "CINEMA TICKET\n";
    std::cout << "Film: \"The Long Night\"\n";
    std::cout << "Row 7, seat 12\n";
    // Each \\ in the code prints one backslash.
    std::cout << "File: C:\\tickets\\night.txt\n";
    std::cout << "Enjoy the film!\n";
    return 0;
}
EOF
for project in lesson_1_1 cinema_ticket shopping_list; do
    mkdir -p "$ws/$project/.idea" "$ws/$project/cmake-build-debug/CMakeFiles"
    echo '<project/>' > "$ws/$project/.idea/workspace.xml"
    echo 'cache' > "$ws/$project/cmake-build-debug/CMakeCache.txt"
    echo 'binary' > "$ws/$project/cmake-build-debug/first_program"
done
for project in lesson_1_4 build_detective; do
    mkdir -p "$ws/$project/build-terminal/CMakeFiles"
    echo 'cache' > "$ws/$project/build-terminal/CMakeCache.txt"
    echo 'binary' > "$ws/$project/build-terminal/first_program"
done
echo 'binary' > "$ws/lesson_1_4/build-terminal/hello_cmake"
echo 'object' > "$ws/lesson_1_4/main.o"
echo 'binary' > "$ws/lesson_1_4/hello"
echo 'finder' > "$ws/.DS_Store"

cd ~ && cd cpp-workspace || exit 1

# Section 3: before git init, Git must report that this folder is not in any repository.
show() { printf -- '--- %s\n' "$1"; sed 's/^/     | /'; }
git status 2>&1 | show 'git status before git init'
expect_fail 'git status before git init reports "not a git repository"' git status
git init 2>&1 | show 'git init'
expect_ok 'git init created the repository' test -f .git/HEAD
expect_ok 'git init created the hidden .git folder' test -d .git
expect_eq 'the repository starts in cpp-workspace' "$ws" "$(cd "$(git rev-parse --show-toplevel)" && pwd)"

# Section 4: identity for this repository only.
git config user.name 'Test Learner'
git config user.email 'learner@example.invalid'
expect_eq 'user.name is set in this repository' 'Test Learner' "$(git config --local user.name)"
expect_eq 'the global configuration was not changed' '' "$(git config --global --list 2>/dev/null)"

# Section 5: before .gitignore, Git offers build results and CLion settings too.
untracked=$(git status --porcelain --untracked-files=all)
case "$untracked" in *build-terminal/CMakeCache.txt*) pass 'before .gitignore: build-terminal files are offered' ;;
    *) fail 'before .gitignore: build-terminal files are offered' "$untracked" ;; esac
case "$untracked" in *.idea/workspace.xml*) pass 'before .gitignore: .idea files are offered' ;;
    *) fail 'before .gitignore: .idea files are offered' "$untracked" ;; esac

git status 2>&1 | show 'git status after git init'
git status --untracked-files=all 2>&1 | head -30 | show 'git status --untracked-files=all before .gitignore (first 30 lines)'
# The .gitignore command exactly as the lesson shows it for macOS and Ubuntu.
printf '%s\n' 'build-terminal/' 'cmake-build-*/' '.idea/' '*.o' '*.obj' '*.exe' '/lesson_1_4/hello' '.DS_Store' > .gitignore
expect_eq '.gitignore has the eight rules' 8 "$(grep -c . .gitignore)"
offered=$(git status --porcelain --untracked-files=all | sed 's/^?? //' | LC_ALL=C sort | tr '\n' ' ')
expected=".gitignore build_detective/CMakeLists.txt build_detective/main.cpp cinema_ticket/CMakeLists.txt cinema_ticket/main.cpp lesson_1_1/CMakeLists.txt lesson_1_1/main.cpp lesson_1_2/CMakeLists.txt lesson_1_2/main.cpp lesson_1_3/CMakeLists.txt lesson_1_3/main.cpp lesson_1_4/CMakeLists.txt lesson_1_4/main.cpp parcel_label/CMakeLists.txt parcel_label/main.cpp shopping_list/CMakeLists.txt shopping_list/main.cpp "
expect_eq 'after .gitignore: only sources (and .gitignore) are offered' "$expected" "$offered"
for path in lesson_1_4/build-terminal/hello_cmake lesson_1_4/main.o lesson_1_4/hello cinema_ticket/.idea/workspace.xml cinema_ticket/cmake-build-debug/first_program .DS_Store; do
    expect_ok "ignored: $path" git check-ignore -q "$path"
done
for path in cinema_ticket/main.cpp cinema_ticket/CMakeLists.txt lesson_1_4/main.cpp; do
    expect_fail "not ignored: $path" git check-ignore -q "$path"
done

git status --untracked-files=all 2>&1 | show 'git status --untracked-files=all after .gitignore'
# Section 6: the first commit, with explicitly chosen files.
git add .gitignore cinema_ticket/main.cpp cinema_ticket/CMakeLists.txt 2>&1 | show 'git add'
git status 2>&1 | show 'git status after git add'
expect_eq 'three files are staged' 'A  .gitignore|A  cinema_ticket/CMakeLists.txt|A  cinema_ticket/main.cpp' \
    "$(git status --porcelain | grep -v '^??' | tr '\n' '|' | sed 's/|$//')"
expect_ok 'git diff --staged shows the staged files' sh -c 'git diff --staged | grep -q "Row 7, seat 12"'
git commit -m 'Dodaj bilet do kina i plik .gitignore' 2>&1 | show 'git commit'
expect_ok 'the first commit exists' git rev-parse -q --verify HEAD
git status 2>&1 | show 'git status after the first commit'
git log 2>&1 | show 'git log'
expect_eq 'git log shows one commit' 1 "$(git log --oneline | wc -l | tr -d ' ')"
expect_eq 'the commit has the author from this repository' 'Test Learner <learner@example.invalid>' "$(git log -1 --format='%an <%ae>')"
expect_eq 'nothing staged or modified after the commit' '' "$(git status --porcelain | grep -v '^??')"
case "$(git status --porcelain)" in *'?? lesson_1_1/'*) pass 'the other projects are still untracked' ;;
    *) fail 'the other projects are still untracked' "$(git status --porcelain)" ;; esac

# Section 7: a change, its diff, the second commit.
sed 's/Row 7, seat 12/Row 9, seat 5/' cinema_ticket/main.cpp > cinema_ticket/main.cpp.new && mv cinema_ticket/main.cpp.new cinema_ticket/main.cpp
expect_eq 'git status shows the modified file' ' M cinema_ticket/main.cpp' "$(git status --porcelain | grep -v '^??')"
diff=$(git diff)
git status 2>&1 | show 'git status after the change'
printf '%s\n' "$diff" | show 'git diff'
case "$diff" in *'-    std::cout << "Row 7, seat 12\n";'*'+    std::cout << "Row 9, seat 5\n";'*) pass 'git diff shows the old line with - and the new one with +' ;;
    *) fail 'git diff shows the old line with - and the new one with +' "$diff" ;; esac
expect_eq 'nothing staged yet' '' "$(git diff --staged)"
git add cinema_ticket/main.cpp
expect_eq 'git diff --staged shows the change once it is staged' "$diff" "$(git diff --staged)"
expect_ok 'the second commit succeeds' git commit -q -m 'Nowe miejsce na bilecie'
expect_eq 'git log shows two commits' 2 "$(git log --oneline | wc -l | tr -d ' ')"
git log --oneline 2>&1 | show 'git log --oneline'
old=$(git show HEAD~1:cinema_ticket/main.cpp)
case "$old" in *'Row 7, seat 12'*) pass 'git show HEAD~1:cinema_ticket/main.cpp shows the earlier version' ;;
    *) fail 'git show HEAD~1:cinema_ticket/main.cpp shows the earlier version' "$old" ;; esac
first=$(git log --reverse --format=%h | head -1)
case "$(git show "$first:cinema_ticket/main.cpp")" in *'Row 7, seat 12'*) pass 'git show <first commit>:cinema_ticket/main.cpp works with the short id' ;;
    *) fail 'git show <first commit>:cinema_ticket/main.cpp works with the short id' ;; esac
expect_ok 'the working file still has the new version' grep -q 'Row 9, seat 5' cinema_ticket/main.cpp

# Section 8 (mission): another project, two commits.
git add parcel_label/main.cpp parcel_label/CMakeLists.txt
git commit -q -m 'Add parcel label'
sed 's/Hello! My first C++20 program works\./TO: Ola Nowak/' parcel_label/main.cpp > parcel_label/main.cpp.new && mv parcel_label/main.cpp.new parcel_label/main.cpp
git add parcel_label/main.cpp
git commit -q -m 'Print the recipient'
expect_eq 'git log -- parcel_label shows the two mission commits' 2 "$(git log --oneline -- parcel_label | wc -l | tr -d ' ')"

# Section 9: the remaining projects, folder by folder, after .gitignore.
git add lesson_1_1 lesson_1_2 shopping_list lesson_1_3 lesson_1_4 build_detective
expect_eq 'adding whole project folders stages only their sources' 12 "$(git diff --staged --name-only | wc -l | tr -d ' ')"
git commit -q -m 'Add the other projects'
expect_eq 'nothing left to commit' '' "$(git status --porcelain)"
tracked=$(git ls-files | tr '\n' ' ')
case "$tracked" in *build-terminal*|*cmake-build*|*.idea*|*main.o*|*'lesson_1_4/hello '*|*.DS_Store*) fail 'no build results or CLion settings in the history' "$tracked" ;;
    *) pass 'no build results or CLion settings in the history' ;; esac
expect_eq 'the history holds 17 files: .gitignore and 16 sources' 17 "$(git ls-files | wc -l | tr -d ' ')"

# Section 10 (troubleshooting): adding an ignored file is refused.
git add lesson_1_4/main.o 2>&1 | show 'git add of an ignored file'
expect_fail 'git add of an ignored file is refused' git add lesson_1_4/main.o
# A wrongly staged file can be unstaged; the file stays on disk.
echo '// note' >> lesson_1_1/main.cpp
git add lesson_1_1/main.cpp
git status 2>&1 | show 'git status with a wrongly staged file'
expect_ok 'git restore --staged unstages the file' git restore --staged lesson_1_1/main.cpp
expect_eq 'after git restore --staged the change is still in the file, not staged' ' M lesson_1_1/main.cpp' "$(git status --porcelain)"
# .gitignore does not untrack a file that is already in the history; git rm --cached does, and keeps the file.
mkdir -p notes && echo 'draft' > notes/todo.txt
git add notes/todo.txt && git commit -q -m 'Add notes'
echo 'notes/' >> .gitignore
echo 'draft 2' > notes/todo.txt
expect_eq 'a tracked file is still reported after adding it to .gitignore' ' M notes/todo.txt' "$(git status --porcelain notes)"
git rm -q --cached notes/todo.txt
expect_ok 'git rm --cached keeps the file on disk' test -f notes/todo.txt
expect_eq 'git rm --cached stages the removal from the history' 'D  notes/todo.txt' "$(git status --porcelain notes)"

finish "lesson 1.5 (sh)"

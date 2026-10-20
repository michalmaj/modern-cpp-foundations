#!/usr/bin/env bash
# Runs the macOS/Ubuntu terminal commands of lesson 1.4, exactly as the lesson
# shows them, in a copy of the lesson 0.5 project. Used by the Toolchains workflow.
# Run from the repository root:  zsh tests/toolchains/lesson_14.sh  (macOS)  or  bash tests/toolchains/lesson_14.sh  (Ubuntu)
# The checks never depend on Ninja's step counters ([3/4] and so on).
set -u
message='Hello! My first C++20 program works.'
# The compiler paths exactly as the lesson writes them (macOS: Apple Silicon example path).
case "$(uname)" in
    Darwin) cxx=/opt/homebrew/opt/llvm@22/bin/clang++; direct_cxx=/opt/homebrew/opt/llvm@22/bin/clang++ ;;
    *)      cxx=/usr/bin/clang++-22;                   direct_cxx=clang++-22 ;;
esac
original=$(pwd)/course/module_00_tooling/lesson_05_first_program
base=${TMPDIR:-/tmp}; work=$(mktemp -d "${base%/}/lesson-14.XXXXXX") || exit 1
trap 'cd /; rm -rf -- "$work"' EXIT
cp "$original/main.cpp" "$original/CMakeLists.txt" "$work"
cd "$work" || exit 1
failures=0
check() { if [ "$1" = 0 ]; then echo "ok   $2"; else echo "FAIL $2"; failures=$((failures + 1)); fi; }
show() { printf '%s\n' "$1" | sed 's/^/     | /'; }

# The program of experiment B, and the same program with main spelled correctly.
mian_program='#include <iostream>

int mian() {
    std::cout << "Hello! My first C++20 program works.\n";
    return 0;
}'
main_program='#include <iostream>

int main() {
    std::cout << "Hello! My first C++20 program works.\n";
    return 0;
}'

echo '=== Experiment A: compile and link in two steps'
missing=$("$direct_cxx" main.o -o hello 2>&1); rc=$?
[ "$rc" != 0 ]; check $? 'linking before compiling fails'
printf '%s\n' "$missing" | grep -q "no such file or directory: 'main.o'"; check $? "linking before compiling: no such file or directory: 'main.o'"
compile=$("$direct_cxx" -std=c++20 -c main.cpp 2>&1); check $? "compile only: $direct_cxx -std=c++20 -c main.cpp"
[ -z "$compile" ]; check $? 'compiling prints nothing'
[ -f main.o ]; check $? 'compiling created main.o'
[ ! -e hello ]; check $? 'compiling created no program'
echo '     files after compiling:'; show "$(ls -F)"
link=$("$direct_cxx" main.o -o hello 2>&1); check $? "link: $direct_cxx main.o -o hello"
[ -z "$link" ]; check $? 'linking prints nothing'
[ -x hello ]; check $? 'linking created the program hello'
out=$(./hello); [ "$out" = "$message" ]; check $? "./hello prints the message ($out)"

echo '=== Experiment B: mian instead of main'
printf '%s\n' "$mian_program" > main.cpp
compile=$("$direct_cxx" -std=c++20 -c main.cpp 2>&1); check $? 'mian: compiling succeeds'
[ -z "$compile" ]; check $? 'mian: compiling prints nothing (no warning)'
link=$("$direct_cxx" main.o -o hello 2>&1); rc=$?
[ "$rc" != 0 ]; check $? 'mian: linking fails'
echo '     linker output:'; show "$link"
printf '%s\n' "$link" | grep -q 'linker command failed'; check $? 'mian: clang++ reports "linker command failed"'
printf '%s\n' "$link" | grep -qE "undefined reference to .main'|\"_main\", referenced from"; check $? 'mian: the linker names the missing main'
printf '%s\n' "$link" | grep -qE 'main\.cpp:[0-9]+:[0-9]+'; [ $? != 0 ]; check $? 'mian: no message points to a line of main.cpp'
[ ! -e hello ]; check $? 'mian: the failed link removed hello from experiment A'
printf '%s\n' "$main_program" > main.cpp
"$direct_cxx" -std=c++20 -c main.cpp; check $? 'fixed: compiling succeeds'
"$direct_cxx" main.o -o hello; check $? 'fixed: linking succeeds'
out=$(./hello); [ "$out" = "$message" ]; check $? "fixed: ./hello prints the message ($out)"

echo '=== Experiment C: rename the program in CMakeLists.txt'
cp "$original/main.cpp" main.cpp
configure=$(cmake -S . -B build-terminal -G Ninja -DCMAKE_BUILD_TYPE=Debug -DCMAKE_CXX_COMPILER="$cxx" 2>&1); check $? 'configure succeeds'
printf '%s\n' "$configure" | grep -q 'The CXX compiler identification is Clang 22\.'; check $? 'configure reports Clang 22'
cmake --build build-terminal >/dev/null 2>&1; check $? 'build succeeds'
[ "$(./build-terminal/first_program)" = "$message" ]; check $? 'first_program prints the message'
sed -E '/^(add_executable|target_compile_features|set_target_properties)\(/ s/first_program/hello_cmake/' CMakeLists.txt > CMakeLists.txt.new && mv CMakeLists.txt.new CMakeLists.txt
echo '     CMakeLists.txt after the change:'; show "$(cat CMakeLists.txt)"
grep -q '^project(first_program LANGUAGES CXX)$' CMakeLists.txt; check $? 'the project line is unchanged'
rebuild=$(cmake --build build-terminal 2>&1); check $? 'building after the change succeeds'
echo '     build output:'; show "$rebuild"
printf '%s\n' "$rebuild" | grep -q 'Re-running CMake'; check $? 'the build re-runs CMake by itself'
printf '%s\n' "$rebuild" | grep -q 'Linking CXX executable hello_cmake'; check $? 'the build links hello_cmake'
[ -x build-terminal/hello_cmake ]; check $? 'build-terminal now contains hello_cmake'
[ -x build-terminal/first_program ]; check $? 'the old first_program is still in build-terminal'
[ "$(./build-terminal/hello_cmake)" = "$message" ]; check $? 'hello_cmake prints the message'
cp "$original/CMakeLists.txt" CMakeLists.txt
cmake --build build-terminal >/dev/null 2>&1; check $? 'after copying the original CMakeLists.txt back, the build succeeds'
[ "$(./build-terminal/first_program)" = "$message" ]; check $? 'first_program prints the message again'

echo '=== Mission, situation with a wrong source file name in CMakeLists.txt'
sed 's/add_executable(first_program main.cpp)/add_executable(first_program program.cpp)/' CMakeLists.txt > CMakeLists.txt.new && mv CMakeLists.txt.new CMakeLists.txt
grep -q 'add_executable(first_program program.cpp)' CMakeLists.txt; check $? 'CMakeLists.txt now names program.cpp'
broken=$(cmake --build build-terminal 2>&1); rc=$?
[ "$rc" != 0 ]; check $? 'the build fails'
echo '     build output:'; show "$broken"
printf '%s\n' "$broken" | grep -q 'Re-running CMake'; check $? 'the build re-runs CMake first'
printf '%s\n' "$broken" | grep -qF 'CMake Error at CMakeLists.txt:4 (add_executable):'; check $? 'CMake reports an error in CMakeLists.txt line 4 (add_executable)'
printf '%s\n' "$broken" | grep -q 'Cannot find source file'; check $? 'CMake cannot find the source file'
printf '%s\n' "$broken" | grep -qE 'main\.cpp:[0-9]+:[0-9]+: error|linker command failed'; [ $? != 0 ]; check $? 'neither the compiler nor the linker ran'
fresh=$(cmake -S . -B build-fresh -G Ninja -DCMAKE_BUILD_TYPE=Debug -DCMAKE_CXX_COMPILER="$cxx" 2>&1); rc=$?
[ "$rc" != 0 ]; check $? 'configuring a new build folder fails too'
printf '%s\n' "$fresh" | grep -q 'Cannot find source file'; check $? 'with the same message'
cp "$original/CMakeLists.txt" CMakeLists.txt
cmake --build build-terminal >/dev/null 2>&1; check $? 'fixed: the build succeeds again'

if [ "$failures" -gt 0 ]; then echo "FAILED: $failures check(s)"; exit 1; fi
echo 'PASSED lesson 1.4 commands'

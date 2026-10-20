#!/usr/bin/env bash
# Checks the CMake part of the lesson 1.6 diagnosis task on macOS/Ubuntu: a
# CMakeLists.txt in which the program was renamed in add_executable only.
# The C++ programs of the lesson are checked by lesson_examples.py.
# Run from the repository root:  zsh tests/toolchains/lesson_16.sh  (macOS)  or  bash tests/toolchains/lesson_16.sh  (Ubuntu)
set -u
case "$(uname)" in
    Darwin) cxx=/opt/homebrew/opt/llvm@22/bin/clang++ ;;
    *)      cxx=/usr/bin/clang++-22 ;;
esac
original=$(pwd)/course/module_00_tooling/lesson_05_first_program
base=${TMPDIR:-/tmp}; work=$(mktemp -d "${base%/}/lesson-16.XXXXXX") || exit 1
trap 'cd /; rm -rf -- "$work"' EXIT
cp "$original/main.cpp" "$work"
cd "$work" || exit 1
failures=0
check() { if [ "$1" = 0 ]; then echo "ok   $2"; else echo "FAIL $2"; failures=$((failures + 1)); fi; }
show() { printf '%s\n' "$1" | sed 's/^/     | /'; }

# The broken CMakeLists.txt exactly as the lesson shows it.
cat > CMakeLists.txt <<'EOF'
cmake_minimum_required(VERSION 3.28)
project(first_program LANGUAGES CXX)

add_executable(board_games main.cpp)
target_compile_features(first_program PRIVATE cxx_std_20)
set_target_properties(first_program PROPERTIES CXX_EXTENSIONS OFF)
EOF
configure=$(cmake -S . -B build-terminal -G Ninja -DCMAKE_BUILD_TYPE=Debug -DCMAKE_CXX_COMPILER="$cxx" 2>&1); rc=$?
echo '     configure output:'; show "$configure"
[ "$rc" != 0 ]; check $? 'configuring fails'
printf '%s\n' "$configure" | grep -q 'The CXX compiler identification is Clang 22\.'; check $? 'the compiler itself is fine (Clang 22)'
printf '%s\n' "$configure" | grep -qF 'CMake Error at CMakeLists.txt:5 (target_compile_features):'; check $? 'the first error points to CMakeLists.txt line 5'
printf '%s\n' "$configure" | grep -q 'Cannot specify compile features for target "first_program"'; check $? 'CMake reports the unknown target first_program'
printf '%s\n' "$configure" | grep -qF 'CMake Error at CMakeLists.txt:6 (set_target_properties):'; check $? 'a second error points to line 6: one cause, two messages'
printf '%s\n' "$configure" | grep -qE 'main\.cpp:[0-9]+:[0-9]+|linker command failed'; [ $? != 0 ]; check $? 'neither the compiler nor the linker ran'

# The fix: the same name in all three lines.
sed 's/(first_program PRIVATE/(board_games PRIVATE/; s/(first_program PROPERTIES/(board_games PROPERTIES/' CMakeLists.txt > CMakeLists.txt.new && mv CMakeLists.txt.new CMakeLists.txt
cmake -S . -B build-terminal -G Ninja -DCMAKE_BUILD_TYPE=Debug -DCMAKE_CXX_COMPILER="$cxx" >/dev/null 2>&1; check $? 'after the fix, configuring succeeds'
cmake --build build-terminal >/dev/null 2>&1; check $? 'the build succeeds'
[ "$(./build-terminal/board_games)" = 'Hello! My first C++20 program works.' ]; check $? 'the program is now called board_games and runs'

if [ "$failures" -gt 0 ]; then echo "FAILED: $failures check(s)"; exit 1; fi
echo 'PASSED lesson 1.6 commands'

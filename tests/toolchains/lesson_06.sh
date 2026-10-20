#!/usr/bin/env bash
# Runs the macOS/Ubuntu commands of lesson 0.6, exactly as the lesson shows
# them, in a copy of the lesson 0.5 project. Used by the Toolchains workflow.
# Run from the repository root:  zsh tests/toolchains/lesson_06.sh  (macOS)  or  bash tests/toolchains/lesson_06.sh  (Ubuntu)
set -u
message='Hello! My first C++20 program works.'
# The compiler paths exactly as the lesson writes them (macOS: Apple Silicon example path).
case "$(uname)" in
    Darwin) cxx=/opt/homebrew/opt/llvm@22/bin/clang++; direct_cxx=/opt/homebrew/opt/llvm@22/bin/clang++ ;;
    *)      cxx=/usr/bin/clang++-22;                   direct_cxx=clang++-22 ;;
esac
base=${TMPDIR:-/tmp}; work=$(mktemp -d "${base%/}/lesson-06.XXXXXX") || exit 1
trap 'cd /; rm -rf -- "$work"' EXIT
cp -R course/module_00_tooling/lesson_05_first_program/. "$work"
cd "$work" || exit 1
failures=0
check() { if [ "$1" = 0 ]; then echo "ok   $2"; else echo "FAIL $2"; failures=$((failures + 1)); fi; }

# Lesson section 4: configure, build, run (commands exactly as in the lesson).
configure=$(cmake -S . -B build-terminal -G Ninja -DCMAKE_BUILD_TYPE=Debug -DCMAKE_CXX_COMPILER="$cxx" 2>&1); check $? 'configure succeeds'
echo "$configure" | grep -q 'The CXX compiler identification is Clang 22\.'; check $? 'configure reports Clang 22'
echo "$configure" | grep -qF "Check for working CXX compiler: $cxx"; check $? "configure uses $cxx"
echo "$configure" | grep -q 'Build files have been written to: .*build-terminal'; check $? 'configure writes build-terminal'
[ -f build-terminal/build.ninja ]; check $? 'build-terminal contains the build plan (build.ninja)'
build=$(cmake --build build-terminal 2>&1); check $? 'build succeeds'
echo "$build" | grep -q 'Linking CXX executable first_program'; check $? 'build links first_program'
out=$(./build-terminal/first_program); [ "$out" = "$message" ]; check $? "CMake-built program prints the message ($out)"

# Lesson section 5: compile directly with clang++.
"$direct_cxx" -std=c++20 main.cpp -o first_program_direct; check $? "direct compile succeeds ($direct_cxx)"
d=$(./first_program_direct); [ "$d" = "$out" ]; check $? "direct program prints the same message ($d)"

# Lesson section 6: edit, run old programs, rebuild one, then the other.
sed "s/Hello! My first C++20 program works\./Three programs, one source./" main.cpp > main.cpp.new && mv main.cpp.new main.cpp
[ "$(./build-terminal/first_program)" = "$message" ]; check $? 'after editing: CMake-built program still prints the old message'
[ "$(./first_program_direct)" = "$message" ]; check $? 'after editing: direct program still prints the old message'
cmake --build build-terminal >/dev/null
[ "$(./build-terminal/first_program)" = 'Three programs, one source.' ]; check $? 'after cmake --build: CMake-built program prints the new message'
[ "$(./first_program_direct)" = "$message" ]; check $? 'after cmake --build: direct program still prints the old message'
"$direct_cxx" -std=c++20 main.cpp -o first_program_direct
[ "$(./first_program_direct)" = 'Three programs, one source.' ]; check $? 'after compiling again: direct program prints the new message'

# Lesson section 8: changing the compiler of an existing build folder (recorded).
if [ "$(uname)" = Linux ]; then
    echo '--- configuring an existing build folder with a different compiler:'
    cmake -S . -B build-switch -G Ninja -DCMAKE_CXX_COMPILER=/usr/bin/g++ >/dev/null 2>&1
    cmake -S . -B build-switch -G Ninja -DCMAKE_CXX_COMPILER="$cxx" 2>&1 | grep -iE 'cache|identification' | head -5
fi
echo '--- running a program without ./ :'
first_program_direct 2>&1 | head -1

if [ "$failures" -gt 0 ]; then echo "FAILED: $failures check(s)"; exit 1; fi
echo 'PASSED lesson 0.6 commands'

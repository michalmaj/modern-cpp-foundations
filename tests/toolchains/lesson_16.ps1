# Checks the CMake part of the lesson 1.6 diagnosis task on Windows: a
# CMakeLists.txt in which the program was renamed in add_executable only.
# The C++ programs of the lesson are checked by lesson_examples.py.
# Run from the repository root:  powershell -NoProfile -ExecutionPolicy Bypass -File tests\toolchains\lesson_16.ps1
# Continue: native tools may write to stderr; exit codes are checked explicitly.
$ErrorActionPreference = 'Continue'
$original = Join-Path (Get-Location) 'course/module_00_tooling/lesson_05_first_program'
$work = Join-Path ([IO.Path]::GetTempPath()) ('lesson-16.' + [guid]::NewGuid().ToString('N').Substring(0, 6))
New-Item -ItemType Directory $work | Out-Null
Copy-Item "$original/main.cpp" $work
Push-Location $work
$failures = 0
function Check($ok, $what) { if ($ok) { "ok   $what" } else { "FAIL $what"; $script:failures++ } }
function Show($text) { ($text -split "`n") | ForEach-Object { "     | $_" } }
$compiler = '-DCMAKE_CXX_COMPILER=C:\Program Files\LLVM\bin\clang++.exe'
try {
    "PowerShell $($PSVersionTable.PSVersion)"
    # The broken CMakeLists.txt exactly as the lesson shows it.
    [IO.File]::WriteAllText((Join-Path $work 'CMakeLists.txt'), "cmake_minimum_required(VERSION 3.28)`nproject(first_program LANGUAGES CXX)`n`nadd_executable(board_games main.cpp)`ntarget_compile_features(first_program PRIVATE cxx_std_20)`nset_target_properties(first_program PROPERTIES CXX_EXTENSIONS OFF)`n")
    $configure = (cmake -S . -B build-terminal -G Ninja -DCMAKE_BUILD_TYPE=Debug $compiler 2>&1) -join "`n"
    $rc = $LASTEXITCODE
    '     configure output:'; Show $configure
    Check ($rc -ne 0) 'configuring fails'
    Check ($configure -match 'The CXX compiler identification is Clang 22\.') 'the compiler itself is fine (Clang 22)'
    Check ($configure -match 'CMake Error at CMakeLists\.txt:5 \(target_compile_features\):') 'the first error points to CMakeLists.txt line 5'
    Check ($configure -match 'Cannot specify compile features for target "first_program"') 'CMake reports the unknown target first_program'
    Check ($configure -match 'CMake Error at CMakeLists\.txt:6 \(set_target_properties\):') 'a second error points to line 6: one cause, two messages'
    Check ($configure -notmatch 'main\.cpp:\d+:\d+|linker command failed') 'neither the compiler nor the linker ran'

    # The fix: the same name in all three lines.
    $text = [IO.File]::ReadAllText((Join-Path $work 'CMakeLists.txt')).Replace('(first_program PRIVATE', '(board_games PRIVATE').Replace('(first_program PROPERTIES', '(board_games PROPERTIES')
    [IO.File]::WriteAllText((Join-Path $work 'CMakeLists.txt'), $text)
    cmake -S . -B build-terminal -G Ninja -DCMAKE_BUILD_TYPE=Debug $compiler | Out-Null
    Check ($LASTEXITCODE -eq 0) 'after the fix, configuring succeeds'
    cmake --build build-terminal | Out-Null
    Check ($LASTEXITCODE -eq 0) 'the build succeeds'
    Check ((.\build-terminal\board_games.exe) -eq 'Hello! My first C++20 program works.') 'the program is now called board_games and runs'
} finally {
    Pop-Location
    Remove-Item -LiteralPath $work -Recurse -Force -ErrorAction SilentlyContinue
}
if ($failures -gt 0) { "FAILED: $failures check(s)"; exit 1 }
'PASSED lesson 1.6 commands'
exit 0

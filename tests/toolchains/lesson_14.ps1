# Runs the Windows PowerShell commands of lesson 1.4, exactly as the lesson
# shows them, in a copy of the lesson 0.5 project. Used by the Toolchains
# workflow in both Windows PowerShell 5.1 and PowerShell 7.
# Run from the repository root:  powershell -NoProfile -ExecutionPolicy Bypass -File tests\toolchains\lesson_14.ps1
# The checks never depend on Ninja's step counters ([3/4] and so on).
# Continue: native tools may write to stderr; exit codes are checked explicitly.
$ErrorActionPreference = 'Continue'
$message = 'Hello! My first C++20 program works.'
$original = Join-Path (Get-Location) 'course/module_00_tooling/lesson_05_first_program'
$work = Join-Path ([IO.Path]::GetTempPath()) ('lesson-14.' + [guid]::NewGuid().ToString('N').Substring(0, 6))
New-Item -ItemType Directory $work | Out-Null
Copy-Item "$original/main.cpp", "$original/CMakeLists.txt" $work
Push-Location $work
$failures = 0
function Check($ok, $what) { if ($ok) { "ok   $what" } else { "FAIL $what"; $script:failures++ } }
function Show($text) { ($text -split "`n") | ForEach-Object { "     | $_" } }
# The program of experiment B, and the same program with main spelled correctly.
$mianProgram = "#include <iostream>`n`nint mian() {`n    std::cout << `"Hello! My first C++20 program works.\n`";`n    return 0;`n}`n"
$mainProgram = $mianProgram -replace 'int mian\(\)', 'int main()'
# Write files without a byte order mark, in both PowerShell versions.
function Write-Source($path, $text) { [IO.File]::WriteAllText((Join-Path $work $path), $text) }
try {
    "PowerShell $($PSVersionTable.PSVersion)"

    '=== Experiment A: compile and link in two steps'
    $missing = (clang++ main.o -o hello.exe 2>&1) -join "`n"
    Check ($LASTEXITCODE -ne 0) 'linking before compiling fails'
    Check ($missing -match "no such file or directory: 'main\.o'") "linking before compiling: no such file or directory: 'main.o'"
    $compile = (clang++ -std=c++20 -c main.cpp 2>&1) -join "`n"
    Check ($LASTEXITCODE -eq 0) 'compile only: clang++ -std=c++20 -c main.cpp'
    Check ($compile -eq '') 'compiling prints nothing'
    '     files after compiling:'; Show ((Get-ChildItem -Name) -join "`n")
    Check (Test-Path main.o) 'compiling created main.o'
    Check (-not (Test-Path hello.exe)) 'compiling created no program'
    $link = (clang++ main.o -o hello.exe 2>&1) -join "`n"
    Check ($LASTEXITCODE -eq 0) 'link: clang++ main.o -o hello.exe'
    Check ($link -eq '') 'linking prints nothing'
    Check (Test-Path hello.exe) 'linking created the program hello.exe'
    $out = .\hello.exe
    Check ($out -eq $message) ".\hello.exe prints the message ($out)"

    '=== Experiment B: mian instead of main'
    Write-Source main.cpp $mianProgram
    $compile = (clang++ -std=c++20 -c main.cpp 2>&1) -join "`n"
    Check ($LASTEXITCODE -eq 0) 'mian: compiling succeeds'
    Check ($compile -eq '') 'mian: compiling prints nothing (no warning)'
    $link = (clang++ main.o -o hello.exe 2>&1) -join "`n"
    Check ($LASTEXITCODE -ne 0) 'mian: linking fails'
    '     linker output:'; Show $link
    Check ($link -match 'linker command failed') 'mian: clang++ reports "linker command failed"'
    # Linking by hand, lld-link chooses the kind of program (console) from main; without main it reports this.
    # (Through CMake, which names the kind itself, the message is 'undefined symbol: main' instead.)
    Check ($link -match 'lld-link: error: subsystem must be defined') 'mian: lld-link cannot choose the kind of program without main'
    Check ($link -notmatch 'main\.cpp:\d+:\d+') 'mian: no message points to a line of main.cpp'
    Check (-not (Test-Path hello.exe)) 'mian: the failed link removed hello.exe from experiment A'
    Write-Source main.cpp $mainProgram
    clang++ -std=c++20 -c main.cpp
    Check ($LASTEXITCODE -eq 0) 'fixed: compiling succeeds'
    clang++ main.o -o hello.exe
    Check ($LASTEXITCODE -eq 0) 'fixed: linking succeeds'
    $out = .\hello.exe
    Check ($out -eq $message) "fixed: .\hello.exe prints the message ($out)"

    '=== Experiment C: rename the program in CMakeLists.txt'
    Copy-Item "$original/main.cpp" main.cpp -Force
    $configure = (cmake -S . -B build-terminal -G Ninja -DCMAKE_BUILD_TYPE=Debug "-DCMAKE_CXX_COMPILER=C:\Program Files\LLVM\bin\clang++.exe" 2>&1) -join "`n"
    Check ($LASTEXITCODE -eq 0) 'configure succeeds'
    Check ($configure -match 'The CXX compiler identification is Clang 22\.') 'configure reports Clang 22'
    cmake --build build-terminal | Out-Null
    Check ($LASTEXITCODE -eq 0) 'build succeeds'
    Check ((.\build-terminal\first_program.exe) -eq $message) 'first_program.exe prints the message'
    $lines = Get-Content CMakeLists.txt | ForEach-Object { if ($_ -match '^(add_executable|target_compile_features|set_target_properties)\(') { $_ -replace 'first_program', 'hello_cmake' } else { $_ } }
    Write-Source CMakeLists.txt (($lines -join "`n") + "`n")
    '     CMakeLists.txt after the change:'; Show (Get-Content CMakeLists.txt -Raw)
    Check ((Get-Content CMakeLists.txt) -contains 'project(first_program LANGUAGES CXX)') 'the project line is unchanged'
    $rebuild = (cmake --build build-terminal 2>&1) -join "`n"
    Check ($LASTEXITCODE -eq 0) 'building after the change succeeds'
    '     build output:'; Show $rebuild
    Check ($rebuild -match 'Re-running CMake') 'the build re-runs CMake by itself'
    Check ($rebuild -match 'Linking CXX executable hello_cmake\.exe') 'the build links hello_cmake.exe'
    Check (Test-Path build-terminal\hello_cmake.exe) 'build-terminal now contains hello_cmake.exe'
    Check (Test-Path build-terminal\first_program.exe) 'the old first_program.exe is still in build-terminal'
    Check ((.\build-terminal\hello_cmake.exe) -eq $message) 'hello_cmake.exe prints the message'
    Copy-Item "$original/CMakeLists.txt" CMakeLists.txt -Force
    cmake --build build-terminal | Out-Null
    Check ($LASTEXITCODE -eq 0) 'after copying the original CMakeLists.txt back, the build succeeds'
    Check ((.\build-terminal\first_program.exe) -eq $message) 'first_program.exe prints the message again'

    '=== Mission, situation with a wrong source file name in CMakeLists.txt'
    $text = (Get-Content CMakeLists.txt -Raw) -replace 'add_executable\(first_program main\.cpp\)', 'add_executable(first_program program.cpp)'
    Write-Source CMakeLists.txt $text
    Check ((Get-Content CMakeLists.txt) -contains 'add_executable(first_program program.cpp)') 'CMakeLists.txt now names program.cpp'
    $broken = (cmake --build build-terminal 2>&1) -join "`n"
    Check ($LASTEXITCODE -ne 0) 'the build fails'
    '     build output:'; Show $broken
    Check ($broken -match 'Re-running CMake') 'the build re-runs CMake first'
    Check ($broken -match 'CMake Error at CMakeLists\.txt:4 \(add_executable\):') 'CMake reports an error in CMakeLists.txt line 4 (add_executable)'
    Check ($broken -match 'Cannot find source file') 'CMake cannot find the source file'
    Check ($broken -notmatch 'main\.cpp:\d+:\d+: error|linker command failed') 'neither the compiler nor the linker ran'
    $fresh = (cmake -S . -B build-fresh -G Ninja -DCMAKE_BUILD_TYPE=Debug "-DCMAKE_CXX_COMPILER=C:\Program Files\LLVM\bin\clang++.exe" 2>&1) -join "`n"
    Check ($LASTEXITCODE -ne 0) 'configuring a new build folder fails too'
    Check ($fresh -match 'Cannot find source file') 'with the same message'
    Copy-Item "$original/CMakeLists.txt" CMakeLists.txt -Force
    cmake --build build-terminal | Out-Null
    Check ($LASTEXITCODE -eq 0) 'fixed: the build succeeds again'
} finally {
    Pop-Location
    Remove-Item -LiteralPath $work -Recurse -Force -ErrorAction SilentlyContinue
}
if ($failures -gt 0) { "FAILED: $failures check(s)"; exit 1 }
'PASSED lesson 1.4 commands'
exit 0

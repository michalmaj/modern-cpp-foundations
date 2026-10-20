# Runs the Windows PowerShell commands of lesson 0.6, exactly as the lesson
# shows them, in a copy of the lesson 0.5 project. Used by the Toolchains
# workflow in both Windows PowerShell 5.1 and PowerShell 7.
# Run from the repository root:  powershell -NoProfile -ExecutionPolicy Bypass -File tests\toolchains\lesson_06.ps1
# Continue: native tools may write to stderr; exit codes are checked explicitly.
$ErrorActionPreference = 'Continue'
$message = 'Hello! My first C++20 program works.'
$work = Join-Path ([IO.Path]::GetTempPath()) ('lesson-06.' + [guid]::NewGuid().ToString('N').Substring(0, 6))
Copy-Item -Recurse course/module_00_tooling/lesson_05_first_program $work
Push-Location $work
$failures = 0
function Check($ok, $what) { if ($ok) { "ok   $what" } else { "FAIL $what"; $script:failures++ } }
try {
    "PowerShell $($PSVersionTable.PSVersion)"

    # Lesson section 4: configure, build, run (commands exactly as in the lesson).
    $configure = (cmake -S . -B build-terminal -G Ninja -DCMAKE_BUILD_TYPE=Debug "-DCMAKE_CXX_COMPILER=C:\Program Files\LLVM\bin\clang++.exe" 2>&1) -join "`n"
    Check ($LASTEXITCODE -eq 0) 'configure succeeds'
    Check ($configure -match 'The CXX compiler identification is Clang 22\.') 'configure reports Clang 22'
    Check ($configure -match 'Check for working CXX compiler: C:/Program Files/LLVM/bin/clang\+\+\.exe') 'configure uses LLVM clang++'
    Check ($configure -match 'Build files have been written to: .*build-terminal') 'configure writes build-terminal'
    Check (Test-Path build-terminal\build.ninja) 'build-terminal contains the build plan (build.ninja)'
    $build = (cmake --build build-terminal 2>&1) -join "`n"
    Check ($LASTEXITCODE -eq 0) 'build succeeds'
    Check ($build -match 'Linking CXX executable first_program\.exe') 'build links first_program.exe'
    $out = .\build-terminal\first_program.exe
    Check ($out -eq $message) "CMake-built program prints the message ($out)"

    # Lesson section 5: compile directly with clang++.
    clang++ -std=c++20 main.cpp -o first_program_direct.exe
    Check ($LASTEXITCODE -eq 0) 'direct clang++ compile succeeds'
    Check ((Get-Command clang++).Source -eq 'C:\Program Files\LLVM\bin\clang++.exe') 'clang++ on PATH is LLVM clang++'
    $direct = .\first_program_direct.exe
    Check ($direct -eq $out) "direct program prints the same message ($direct)"

    # Lesson section 6: edit, run old programs, rebuild one, then the other.
    (Get-Content main.cpp) -replace [regex]::Escape($message), 'Three programs, one source.' | Set-Content main.cpp
    Check ((.\build-terminal\first_program.exe) -eq $message) 'after editing: CMake-built program still prints the old message'
    Check ((.\first_program_direct.exe) -eq $message) 'after editing: direct program still prints the old message'
    cmake --build build-terminal | Out-Null
    Check ((.\build-terminal\first_program.exe) -eq 'Three programs, one source.') 'after cmake --build: CMake-built program prints the new message'
    Check ((.\first_program_direct.exe) -eq $message) 'after cmake --build: direct program still prints the old message'
    clang++ -std=c++20 main.cpp -o first_program_direct.exe
    Check ((.\first_program_direct.exe) -eq 'Three programs, one source.') 'after compiling again: direct program prints the new message'

    # Lesson 0.5, section 8 writes the compiler argument with quotes around the path only.
    cmake -S . -B build-05-form -G Ninja -DCMAKE_BUILD_TYPE=Debug -DCMAKE_CXX_COMPILER="C:\Program Files\LLVM\bin\clang++.exe" 2>&1 | Out-Null
    Check ($LASTEXITCODE -eq 0) 'lesson 0.5 quoting form (-DCMAKE_CXX_COMPILER="C:\...") also works'

    # Lesson section 8: what a learner sees without the quotes (recorded, not compared in full).
    $unquoted = (cmake -S . -B build-unquoted -G Ninja -DCMAKE_BUILD_TYPE=Debug -DCMAKE_CXX_COMPILER=C:\Program Files\LLVM\bin\clang++.exe 2>&1) -join "`n"
    Check ($LASTEXITCODE -ne 0) 'without quotes, configure fails'
    "--- message without quotes (first lines):"; ($unquoted -split "`n" | Select-Object -First 8) -join "`n"
} finally {
    Pop-Location
    Remove-Item -LiteralPath $work -Recurse -Force -ErrorAction SilentlyContinue
}
if ($failures -gt 0) { "FAILED: $failures check(s)"; exit 1 }
'PASSED lesson 0.6 commands'
exit 0

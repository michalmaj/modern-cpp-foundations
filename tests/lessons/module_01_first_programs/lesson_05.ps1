# Checks the Windows PowerShell Git commands taught in Module 1, lesson 1.5
# (course/module_01_first_programs/lesson_05_save_the_history_of_your_work{.md,.en.md}).
# Run:  powershell -NoProfile -ExecutionPolicy Bypass -File lesson_05.ps1
#  or:  pwsh -NoProfile -File lesson_05.ps1
#
# Everything happens in a fake home folder inside a temporary folder. Git's
# global configuration is pointed at an empty file there (GIT_CONFIG_GLOBAL),
# so the runner's own Git settings are neither read nor changed. The system
# configuration of Git for Windows (for example core.autocrlf) is kept, as on
# a learner's computer. Checks look at behaviour, not at Git's exact wording.

. (Join-Path $PSScriptRoot '..\lib.ps1')
# Native tools may write to stderr; exit codes are checked explicitly.
$ErrorActionPreference = 'Continue'
$course = Join-Path $PSScriptRoot '..\..\..\course'
$original = Join-Path $course 'module_00_tooling\lesson_05_first_program'

# Files are written with \n line ends, as in the course ZIP and as CLion keeps them.
function Write-Lf([string]$Path, [string]$Text) { [IO.File]::WriteAllText($Path, $Text.Replace("`r`n", "`n")) }
function Edit-Lf([string]$Path, [string]$Old, [string]$New) { Write-Lf $Path ([IO.File]::ReadAllText($Path).Replace($Old, $New)) }
function Get-Status { @(git status --porcelain 2>$null) }

try {
    $lessonHome = New-LessonHome 'git'
    $globalConfig = Join-Path $LessonTmp 'global-gitconfig'
    New-Item -ItemType File $globalConfig | Out-Null
    $env:GIT_CONFIG_GLOBAL = $globalConfig
    Write-Host "--- $(git --version); PowerShell $($PSVersionTable.PSVersion)"
    Write-Host "--- system core.autocrlf = $(git config --system --get core.autocrlf)"

    # A cpp-workspace as lessons 1.1-1.4 leave it.
    $ws = Join-Path $lessonHome 'cpp-workspace'
    foreach ($project in 'lesson_1_1', 'parcel_label', 'lesson_1_2', 'shopping_list', 'lesson_1_3', 'cinema_ticket', 'lesson_1_4', 'build_detective') {
        New-Item -ItemType Directory "$ws\$project" -Force | Out-Null
        Copy-Item "$original\main.cpp", "$original\CMakeLists.txt" "$ws\$project"
    }
    Write-Lf "$ws\cinema_ticket\main.cpp" @'
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

'@
    foreach ($project in 'lesson_1_1', 'cinema_ticket', 'shopping_list') {
        New-Item -ItemType Directory "$ws\$project\.idea", "$ws\$project\cmake-build-debug\CMakeFiles" -Force | Out-Null
        Set-Content "$ws\$project\.idea\workspace.xml" '<project/>'
        Set-Content "$ws\$project\cmake-build-debug\CMakeCache.txt" 'cache'
        Set-Content "$ws\$project\cmake-build-debug\first_program.exe" 'binary'
    }
    foreach ($project in 'lesson_1_4', 'build_detective') {
        New-Item -ItemType Directory "$ws\$project\build-terminal\CMakeFiles" -Force | Out-Null
        Set-Content "$ws\$project\build-terminal\CMakeCache.txt" 'cache'
        Set-Content "$ws\$project\build-terminal\first_program.exe" 'binary'
    }
    Set-Content "$ws\lesson_1_4\build-terminal\hello_cmake.exe" 'binary'
    Set-Content "$ws\lesson_1_4\main.o" 'object'
    Set-Content "$ws\lesson_1_4\hello.exe" 'binary'

    cd ~
    cd cpp-workspace

    function Show([string]$Title, $Lines) { Write-Host "--- $Title"; foreach ($l in @($Lines)) { Write-Host "     | $l" } }
    # Section 3: before git init, Git must report that this folder is not in any repository.
    git status 2>&1 | Out-Null
    Assert-Equal 'git status before git init reports "not a git repository"' $true ($LASTEXITCODE -ne 0)
    $init = (git init 2>&1) -join "`n"
    Assert-Equal 'git init succeeds' 0 $LASTEXITCODE
    Write-Host "     git init said: $init"
    Assert-Equal 'git init created the hidden .git folder' $true (Test-Path -LiteralPath .git -PathType Container)
    $top = git rev-parse --show-toplevel
    Assert-Match 'the repository starts in cpp-workspace' '/cpp-workspace$' $top

    # Section 4: identity for this repository only.
    git config user.name 'Test Learner'
    git config user.email 'learner@example.invalid'
    Assert-Equal 'user.name is set in this repository' 'Test Learner' (git config --local user.name)
    Assert-Equal 'the global configuration was not changed' '' ((git config --global --list 2>$null) -join ',')

    # Section 5: before .gitignore, Git offers build results and CLion settings too.
    $untracked = (git status --porcelain --untracked-files=all) -join "`n"
    Assert-Match 'before .gitignore: build-terminal files are offered' 'build-terminal/CMakeCache\.txt' $untracked
    Assert-Match 'before .gitignore: .idea files are offered' '\.idea/workspace\.xml' $untracked

    # The .gitignore command exactly as the lesson shows it for Windows.
    Set-Content .gitignore 'build-terminal/', 'cmake-build-*/', '.idea/', '*.o', '*.obj', '*.exe', '/lesson_1_4/hello', '.DS_Store'
    Assert-Equal '.gitignore has the eight rules' 8 @(Get-Content .gitignore | Where-Object { $_ }).Count
    $offeredList = [string[]]@(git status --porcelain --untracked-files=all | ForEach-Object { $_.Substring(3) })
    [Array]::Sort($offeredList, [StringComparer]::Ordinal)
    $offered = $offeredList -join ' '
    $expected = '.gitignore build_detective/CMakeLists.txt build_detective/main.cpp cinema_ticket/CMakeLists.txt cinema_ticket/main.cpp lesson_1_1/CMakeLists.txt lesson_1_1/main.cpp lesson_1_2/CMakeLists.txt lesson_1_2/main.cpp lesson_1_3/CMakeLists.txt lesson_1_3/main.cpp lesson_1_4/CMakeLists.txt lesson_1_4/main.cpp parcel_label/CMakeLists.txt parcel_label/main.cpp shopping_list/CMakeLists.txt shopping_list/main.cpp'
    Assert-Equal 'after .gitignore: only sources (and .gitignore) are offered' $expected $offered
    foreach ($path in 'lesson_1_4/build-terminal/hello_cmake.exe', 'lesson_1_4/main.o', 'lesson_1_4/hello.exe', 'cinema_ticket/.idea/workspace.xml', 'cinema_ticket/cmake-build-debug/first_program.exe') {
        git check-ignore -q $path
        Assert-Equal "ignored: $path" 0 $LASTEXITCODE
    }
    foreach ($path in 'cinema_ticket/main.cpp', 'cinema_ticket/CMakeLists.txt', 'lesson_1_4/main.cpp') {
        git check-ignore -q $path
        Assert-Equal "not ignored: $path" 1 $LASTEXITCODE
    }

    # Section 6: the first commit, with explicitly chosen files.
    Show 'git add' (git add .gitignore cinema_ticket/main.cpp cinema_ticket/CMakeLists.txt 2>&1)
    Show 'git status after git add' (git status 2>&1)
    Assert-Equal 'three files are staged' 'A  .gitignore|A  cinema_ticket/CMakeLists.txt|A  cinema_ticket/main.cpp' ((Get-Status | Where-Object { $_ -notlike '`?`?*' }) -join '|')
    Assert-Match 'git diff --staged shows the staged files' 'Row 7, seat 12' ((git diff --staged) -join "`n")
    Show 'git commit' (git commit -m 'Dodaj bilet do kina i plik .gitignore' 2>&1)
    Assert-Equal 'the first commit succeeds' 0 $LASTEXITCODE
    Show 'git log' (git log 2>&1)
    Assert-Equal 'git log shows one commit' 1 @(git log --oneline).Count
    Assert-Equal 'the commit has the author from this repository' 'Test Learner <learner@example.invalid>' (git log -1 --format='%an <%ae>')
    Assert-Equal 'nothing staged or modified after the commit' '' ((Get-Status | Where-Object { $_ -notlike '`?`?*' }) -join '|')
    Assert-Match 'the other projects are still untracked' '\?\? lesson_1_1/' ((Get-Status) -join "`n")

    # Section 7: a change, its diff, the second commit.
    Edit-Lf "$ws\cinema_ticket\main.cpp" 'Row 7, seat 12' 'Row 9, seat 5'
    Assert-Equal 'git status shows the modified file' ' M cinema_ticket/main.cpp' ((Get-Status | Where-Object { $_ -notlike '`?`?*' }) -join '|')
    $diff = (git diff) -join "`n"
    Show 'git diff' ($diff -split "`n")
    Assert-Match 'git diff shows the old line with - and the new one with +' '(?s)-    std::cout << "Row 7, seat 12\\n";.*\+    std::cout << "Row 9, seat 5\\n";' $diff
    Assert-Equal 'nothing staged yet' '' ((git diff --staged) -join "`n")
    Show 'git add of the changed file' (git add cinema_ticket/main.cpp 2>&1)
    Assert-Equal 'git diff --staged shows the change once it is staged' $diff ((git diff --staged) -join "`n")
    git commit -q -m 'Nowe miejsce na bilecie'
    Assert-Equal 'the second commit succeeds' 0 $LASTEXITCODE
    Assert-Equal 'git log shows two commits' 2 @(git log --oneline).Count
    Assert-Match 'git show HEAD~1:cinema_ticket/main.cpp shows the earlier version' 'Row 7, seat 12' ((git show HEAD~1:cinema_ticket/main.cpp) -join "`n")
    $first = @(git log --reverse --format=%h)[0]
    Assert-Match 'git show <first commit>:cinema_ticket/main.cpp works with the short id' 'Row 7, seat 12' ((git show "${first}:cinema_ticket/main.cpp") -join "`n")
    git show "${first}:cinema_ticket\main.cpp" 2>&1 | Out-Null
    Write-Host "     note: git show <id>:cinema_ticket\main.cpp (with a backslash) exits with $LASTEXITCODE"
    Assert-Match 'the working file still has the new version' 'Row 9, seat 5' ([IO.File]::ReadAllText("$ws\cinema_ticket\main.cpp"))

    # Section 8 (mission): another project, two commits.
    git add parcel_label/main.cpp parcel_label/CMakeLists.txt 2>&1 | Out-Null
    git commit -q -m 'Add parcel label'
    Edit-Lf "$ws\parcel_label\main.cpp" 'Hello! My first C++20 program works.' 'TO: Ola Nowak'
    git add parcel_label/main.cpp 2>&1 | Out-Null
    git commit -q -m 'Print the recipient'
    Assert-Equal 'git log -- parcel_label shows the two mission commits' 2 @(git log --oneline -- parcel_label).Count

    # Section 9: the remaining projects, folder by folder, after .gitignore.
    git add lesson_1_1 lesson_1_2 shopping_list lesson_1_3 lesson_1_4 build_detective 2>&1 | Out-Null
    Assert-Equal 'adding whole project folders stages only their sources' 12 @(git diff --staged --name-only).Count
    git commit -q -m 'Add the other projects'
    Assert-Equal 'nothing left to commit' '' ((Get-Status) -join '|')
    $tracked = (git ls-files) -join ' '
    Assert-Equal 'no build results or CLion settings in the history' $false ($tracked -match 'build-terminal|cmake-build|\.idea|main\.o|\.exe')
    Assert-Equal 'the history holds 17 files: .gitignore and 16 sources' 17 @(git ls-files).Count

    # Section 10 (troubleshooting): adding an ignored file is refused.
    Show 'git add of an ignored file' (git add lesson_1_4/main.o 2>&1)
    Assert-Equal 'git add of an ignored file is refused' $true ($LASTEXITCODE -ne 0)
    Edit-Lf "$ws\lesson_1_1\main.cpp" '}' "}`n// note"
    git add lesson_1_1/main.cpp 2>&1 | Out-Null
    git restore --staged lesson_1_1/main.cpp
    Assert-Equal 'git restore --staged unstages the file' 0 $LASTEXITCODE
    Assert-Equal 'after git restore --staged the change is still in the file, not staged' ' M lesson_1_1/main.cpp' ((Get-Status) -join '|')
    New-Item -ItemType Directory notes | Out-Null
    Write-Lf "$ws\notes\todo.txt" "draft`n"
    git add notes/todo.txt 2>&1 | Out-Null
    git commit -q -m 'Add notes'
    Add-Content .gitignore 'notes/'
    Write-Lf "$ws\notes\todo.txt" "draft 2`n"
    Assert-Equal 'a tracked file is still reported after adding it to .gitignore' ' M notes/todo.txt' ((git status --porcelain notes) -join '|')
    git rm -q --cached notes/todo.txt
    Assert-Equal 'git rm --cached keeps the file on disk' $true (Test-Path "$ws\notes\todo.txt")
    Assert-Equal 'git rm --cached stages the removal from the history' 'D  notes/todo.txt' ((git status --porcelain notes) -join '|')
} finally {
    Remove-Item Env:\GIT_CONFIG_GLOBAL -ErrorAction SilentlyContinue
    Remove-LessonTemp
}
Complete-Lesson 'lesson 1.5 (ps1)'

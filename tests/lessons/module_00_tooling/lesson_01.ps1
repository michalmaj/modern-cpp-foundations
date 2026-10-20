# Checks the Windows PowerShell commands taught in Module 0, lesson 0.1
# (course/module_00_tooling/lesson_01_files_and_terminal{.md,.en.md}).
# Run:  powershell -NoProfile -ExecutionPolicy Bypass -File lesson_01.ps1
#  or:  pwsh -NoProfile -File lesson_01.ps1

. (Join-Path $PSScriptRoot '..\lib.ps1')

# Test-Lesson LABEL FOLDER SUBFOLDER FILE
# Uses the folder and file names from one language version of the lesson.
function Test-Lesson([string]$Label, [string]$Folder, [string]$Subfolder, [string]$File) {
    Write-Host "--- names from the $Label lesson"
    $lessonHome = New-LessonHome $Label

    # Section 4: pwd prints the current folder as an absolute path.
    Assert-Equal "[$Label] pwd prints the current folder" $lessonHome (pwd).Path
    Assert-Match "[$Label] pwd prints an absolute path" '^[A-Za-z]:\\' (pwd).Path

    # Section 6: a folder created in File Explorer shows up in ls with Mode starting with d.
    New-Item -ItemType Directory $Folder | Out-Null
    Assert-Equal "[$Label] ls marks a folder with d" "d $Folder" (Get-Listing)
    Assert-Equal "[$Label] ls . lists the same as ls" (Get-Listing) (Get-Listing '.')

    # Section 7: New-Item with a relative path creates an empty file inside the folder.
    New-Item -ItemType Directory "$Folder\$Subfolder" | Out-Null
    Assert-Succeeds "[$Label] New-Item FOLDER\FILE succeeds" { New-Item "$Folder\$File" }
    Assert-Equal "[$Label] New-Item does not create the file in the current folder" $false (Test-Path $File)
    Assert-Equal "[$Label] the new file is empty (Length 0)" 0 (Get-Item "$Folder\$File").Length
    Assert-Equal "[$Label] ls FOLDER shows exactly the file (-) and the subfolder (d)" `
        "- $File, d $Subfolder" (Get-Listing $Folder)

    # Section 8: the absolute path built from pwd reaches the same file, also with a space in it.
    Assert-Equal "[$Label] ls with the absolute path shows the file" "- $File" (Get-Listing "$lessonHome\$Folder\$File")
    New-Item -ItemType Directory "Jan Kowalski\$Folder" | Out-Null
    New-Item "Jan Kowalski\$Folder\$File" | Out-Null
    Assert-Equal "[$Label] ls with an absolute path containing a space" "- $File" `
        (Get-Listing "$lessonHome\Jan Kowalski\$Folder\$File")

    # Safety note: New-Item on an existing file reports an error and keeps its contents.
    Set-Content "$Folder\$File" 'milk'
    Assert-Fails "[$Label] New-Item on an existing file reports an error" { New-Item "$Folder\$File" }
    Assert-Equal "[$Label] New-Item on an existing file keeps its contents" 'milk' (Get-Content "$Folder\$File")

    # Section 9: a missing path and the macOS/Linux option -F are reported as errors.
    Assert-Fails "[$Label] ls on a missing path reports an error" { ls 'no-such-folder' }
    Assert-Fails "[$Label] ls -F reports an error on Windows" { ls -F }
}

try {
    Test-Lesson 'pl' 'pierwszy-eksperyment' 'notatki' 'lista.txt'
    Test-Lesson 'en' 'first-experiment' 'notes' 'list.txt'
} finally {
    Remove-LessonTemp
}
Complete-Lesson 'lesson 0.1 (PowerShell)'

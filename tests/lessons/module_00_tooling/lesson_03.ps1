# Checks the Windows PowerShell commands taught in Module 0, lesson 0.3
# (course/module_00_tooling/lesson_03_commands_and_programs{.md,.en.md}).
# Run:  powershell -NoProfile -ExecutionPolicy Bypass -File lesson_03.ps1
#  or:  pwsh -NoProfile -File lesson_03.ps1

. (Join-Path $PSScriptRoot '..\lib.ps1')

function Test-Lesson {
    $null = New-LessonHome 'lesson-03'

    # Section 2: whoami is a program that prints "computer\account".
    $who = @(whoami)
    Assert-Equal 'whoami prints one line' 1 $who.Count
    Assert-Equal 'whoami ends with the account name' $env:USERNAME.ToLowerInvariant() `
        ($who[0].Split('\')[-1]).ToLowerInvariant()

    # Section 3: Get-Command shows whoami as a separate program (Application) with a file.
    $program = Get-Command whoami
    Assert-Equal 'whoami is an Application' 'Application' $program.CommandType
    Assert-Equal 'the whoami program is a file' $true (Test-Path -LiteralPath $program.Source -PathType Leaf)
    Assert-Match 'the program file ends with .exe' '\.exe$' $program.Source

    # Section 3: cd is an alias of Set-Location, which is a cmdlet built into PowerShell.
    $cd = Get-Command cd
    Assert-Equal 'cd is an Alias' 'Alias' $cd.CommandType
    Assert-Equal 'cd points to Set-Location' 'Set-Location' $cd.ResolvedCommand.Name
    Assert-Equal 'Set-Location is a Cmdlet (built into PowerShell)' 'Cmdlet' (Get-Command Set-Location).CommandType

    # Section 4: running the program by its full path gives the same result.
    Assert-Equal 'running whoami by its full path gives the same result' ($who -join '') ((& $program.Source) -join '')

    # Section 6 (mission): pwd and ls are aliases of cmdlets.
    foreach ($pair in @(@('pwd', 'Get-Location'), @('ls', 'Get-ChildItem'))) {
        $command = Get-Command $pair[0]
        Assert-Equal "$($pair[0]) is an Alias of $($pair[1])" "Alias $($pair[1])" "$($command.CommandType) $($command.ResolvedCommand.Name)"
        Assert-Equal "$($pair[1]) is a Cmdlet" 'Cmdlet' (Get-Command $pair[1]).CommandType
    }

    # Section 7: type is an alias of Get-Content, so `type whoami` fails in an empty folder.
    Assert-Equal 'type is an alias of Get-Content' 'Get-Content' (Get-Alias type).Definition
    Assert-Fails 'type whoami reports an error' { type whoami }
    Assert-Fails 'Get-Command on an unknown command reports an error' { Get-Command no-such-command-here }
}

try {
    Test-Lesson
} finally {
    Remove-LessonTemp
}
Complete-Lesson 'lesson 0.3 (PowerShell)'

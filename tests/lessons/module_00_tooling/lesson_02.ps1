# Checks the Windows PowerShell commands taught in Module 0, lesson 0.2
# (course/module_00_tooling/lesson_02_moving_between_folders{.md,.en.md}).
# Run:  powershell -NoProfile -ExecutionPolicy Bypass -File lesson_02.ps1
#  or:  pwsh -NoProfile -File lesson_02.ps1

. (Join-Path $PSScriptRoot '..\lib.ps1')

# Test-Lesson LABEL TREE MUSEUMS BEACHES
# Uses the folder names from one language version of the lesson:
#   TREE\krakow\MUSEUMS and TREE\gdansk\BEACHES
function Test-Lesson([string]$Label, [string]$Tree, [string]$Museums, [string]$Beaches) {
    Write-Host "--- names from the $Label lesson"
    $lessonHome = New-LessonHome $Label

    # Section 2: cd ~ goes home from anywhere.
    Set-Location -LiteralPath $LessonTmp
    cd ~
    Assert-Equal "[$Label] cd ~ goes to the home folder" $lessonHome (pwd).Path

    # Section 3: the practice tree (created in File Explorer in the lesson).
    New-Item -ItemType Directory "$Tree\krakow\$Museums", "$Tree\gdansk\$Beaches" | Out-Null
    Assert-Equal "[$Label] ls TREE shows both city folders" 'd gdansk, d krakow' (Get-Listing $Tree)

    # Section 4: the same relative path depends on the current folder.
    Assert-Fails "[$Label] ls krakow fails from the home folder" { ls krakow }
    $output = cd $Tree
    Assert-Equal "[$Label] cd prints nothing" $true ($null -eq $output)
    Assert-Equal "[$Label] cd TREE changes the current folder" "$lessonHome\$Tree" (pwd).Path
    Assert-Equal "[$Label] ls krakow works from TREE" "d $Museums" (Get-Listing 'krakow')

    # Section 5: cd .. goes to the parent folder.
    cd ..
    Assert-Equal "[$Label] cd .. goes to the parent folder" $lessonHome (pwd).Path

    cd "$Tree\krakow\$Museums"
    Assert-Equal "[$Label] cd with a multi-level relative path" "$lessonHome\$Tree\krakow\$Museums" (pwd).Path
    Assert-Equal "[$Label] ls .. shows the contents of the parent folder" "d $Museums" (Get-Listing '..')
    Assert-Equal "[$Label] ls .. does not change the current folder" "$lessonHome\$Tree\krakow\$Museums" (pwd).Path
    Assert-Equal "[$Label] ls ..\.. shows two levels up" 'd gdansk, d krakow' (Get-Listing '..\..')

    # Section 6: cd moves nothing; the tree is still in the home folder.
    cd "$lessonHome\$Tree\krakow"
    Assert-Equal "[$Label] ls ~ still shows TREE after cd" "d $Tree" (Get-Listing '~')
    Assert-Equal "[$Label] the tree is still where it was" $true (Test-Path "$lessonHome\$Tree\krakow\$Museums")

    # Section 7: an absolute path works from any current folder.
    cd "$lessonHome\$Tree\krakow\$Museums"
    cd "$lessonHome\$Tree\gdansk"
    Assert-Equal "[$Label] cd with an absolute path" "$lessonHome\$Tree\gdansk" (pwd).Path

    # Section 8, part A: one level at a time.
    cd "$lessonHome\$Tree\krakow\$Museums"
    cd ..; cd ..; cd gdansk; cd $Beaches
    Assert-Equal "[$Label] mission part A (step by step)" "$lessonHome\$Tree\gdansk\$Beaches" (pwd).Path
    Assert-Equal "[$Label] ls in an empty folder prints nothing" 0 @(ls).Count

    # Section 8, part B: one command with a relative path.
    cd "$lessonHome\$Tree\krakow\$Museums"
    cd "..\..\gdansk\$Beaches"
    Assert-Equal "[$Label] mission part B (one command)" "$lessonHome\$Tree\gdansk\$Beaches" (pwd).Path

    # Section 8, part C: back home with .. three times, and with ~.
    cd ..\..\..
    Assert-Equal "[$Label] mission part C (cd ..\..\..)" $lessonHome (pwd).Path
    cd "$lessonHome\$Tree\gdansk\$Beaches"
    cd ~
    Assert-Equal "[$Label] mission part C (cd ~)" $lessonHome (pwd).Path

    # Section 10: cd to a missing folder fails and leaves the current folder unchanged.
    Assert-Fails "[$Label] cd to a missing folder reports an error" { cd no-such-folder }
    Assert-Equal "[$Label] a failed cd leaves the current folder unchanged" $lessonHome (pwd).Path
}

function Test-ShellBehaviour {
    Write-Host '--- shell behaviour described in the lesson'
    $lessonHome = New-LessonHome 'shell'
    New-Item -ItemType Directory 'plan-podrozy\krakow' | Out-Null

    # Section 5: cd .. stops at the root folder of the drive.
    cd "$lessonHome\plan-podrozy\krakow"
    for ($i = 0; $i -lt 64; $i++) {
        $before = (pwd).Path
        cd ..
        if ((pwd).Path -eq $before) { break }
    }
    Assert-Match 'cd .. stops at the root folder of the drive' '^[A-Za-z]:\\$' (pwd).Path
    $root = (pwd).Path
    cd ..
    Assert-Equal 'cd .. in the root folder stays there' $root (pwd).Path

    # Section 9: cd, pwd and ls are aliases of PowerShell commands.
    Assert-Equal 'cd is an alias of Set-Location' 'Set-Location' (Get-Alias cd).Definition
    Assert-Equal 'pwd is an alias of Get-Location' 'Get-Location' (Get-Alias pwd).Definition
    Assert-Equal 'ls is an alias of Get-ChildItem' 'Get-ChildItem' (Get-Alias ls).Definition

    # Section 10: plain cd depends on the PowerShell version.
    cd "$lessonHome\plan-podrozy"
    cd
    if ($PSVersionTable.PSVersion.Major -le 5) {
        Assert-Equal 'Windows PowerShell 5.1: plain cd stays in the current folder' "$lessonHome\plan-podrozy" (pwd).Path
    } else {
        Assert-Equal 'PowerShell 7: plain cd goes to the home folder' $lessonHome (pwd).Path
    }

    # Section 10: cd.. without a space works in PowerShell.
    cd "$lessonHome\plan-podrozy"
    Assert-Succeeds 'cd.. without a space works in PowerShell' { cd.. }
    Assert-Equal 'cd.. goes to the parent folder' $lessonHome (pwd).Path

    # Section 10: Windows accepts the wrong letter case and both separators.
    cd $lessonHome
    Assert-Succeeds 'cd with the wrong letter case works on Windows' { cd Plan-Podrozy }
    cd $lessonHome
    Assert-Succeeds 'cd with / as the separator works in PowerShell' { cd plan-podrozy/krakow }
    Assert-Match 'cd with / reaches the same folder' '\\plan-podrozy\\krakow$' (pwd).Path
}

try {
    Test-Lesson 'pl' 'plan-podrozy' 'muzea' 'plaze'
    Test-Lesson 'en' 'trip-plan' 'museums' 'beaches'
    Test-ShellBehaviour
} finally {
    Remove-LessonTemp
}
Complete-Lesson 'lesson 0.2 (PowerShell)'

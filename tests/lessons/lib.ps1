# Shared helpers for lesson command checks, for Windows PowerShell 5.1 and
# PowerShell 7 on Windows. Dot-source this file from a lesson script; do not
# run it directly.
#
# Every check runs inside a fresh temporary folder. The home folder of the
# FileSystem provider, which `cd ~` and `ls ~` use, is pointed at a fake home
# folder inside it, so `~` never reaches the real home folder. Lesson scripts
# call Remove-LessonTemp in a `finally` block, so the temporary folder is
# removed and the provider home restored also when a check throws.

if ([Environment]::OSVersion.Platform -ne 'Win32NT') {
    Write-Host 'SKIPPED the PowerShell lesson checks describe Windows; use the .sh checks on macOS and Linux'
    exit 0
}

$LessonState = @{ Failures = 0 }
$LessonFs = Get-PSProvider FileSystem
$LessonOriginalHome = $LessonFs.Home
$LessonOriginalLocation = (Get-Location).Path
$LessonTmp = Join-Path ([IO.Path]::GetTempPath()) ('lesson-check.' + [guid]::NewGuid().ToString('N').Substring(0, 6))
New-Item -ItemType Directory -Path $LessonTmp | Out-Null

# New-LessonHome NAME: create a fake home folder, make it `~` and go there.
# Returns the home path as `pwd` prints it, for later comparisons.
function New-LessonHome([string]$Name) {
    $path = Join-Path $LessonTmp "$Name\home"
    New-Item -ItemType Directory -Path $path -Force | Out-Null
    Set-Location -LiteralPath $path
    $LessonFs.Home = (Get-Location).Path
    return (Get-Location).Path
}

function Remove-LessonTemp {
    Set-Location -LiteralPath $LessonOriginalLocation
    $LessonFs.Home = $LessonOriginalHome
    if ((Split-Path -Leaf $LessonTmp) -like 'lesson-check.*' -and (Test-Path -LiteralPath $LessonTmp)) {
        Remove-Item -LiteralPath $LessonTmp -Recurse -Force
    }
}

# Get-Listing [PATH]: what `ls` shows, as "<first letter of Mode> <Name>" items,
# sorted by name and joined with ", ". Returns "<error>" if ls fails.
function Get-Listing([string]$Path = '.') {
    try {
        $items = @(ls $Path -ErrorAction Stop | Sort-Object Name)
        return (($items | ForEach-Object { $_.Mode.Substring(0, 1) + ' ' + $_.Name }) -join ', ')
    } catch {
        return '<error>'
    }
}

function Write-Pass([string]$Description) { Write-Host "ok   $Description" }
function Write-Fail([string]$Description, [string[]]$Details) {
    Write-Host "FAIL $Description"
    foreach ($line in $Details) { Write-Host "     $line" }
    $LessonState.Failures++
}

function Assert-Equal([string]$Description, $Expected, $Actual) {
    if ([string]$Expected -ceq [string]$Actual) { Write-Pass $Description }
    else { Write-Fail $Description @("expected: $Expected", "actual:   $Actual") }
}

function Assert-Match([string]$Description, [string]$Pattern, [string]$Actual) {
    if ($Actual -match $Pattern) { Write-Pass $Description }
    else { Write-Fail $Description @("expected to match: $Pattern", "actual:            $Actual") }
}

# Assert-Succeeds / Assert-Fails DESCRIPTION { commands }: errors inside the
# block count as failure; location changes made by the block are kept.
function Assert-Succeeds([string]$Description, [scriptblock]$Action) {
    $ErrorActionPreference = 'Stop'
    try { $null = & $Action; Write-Pass $Description }
    catch { Write-Fail $Description @("error: $($_.Exception.Message)") }
}

function Assert-Fails([string]$Description, [scriptblock]$Action) {
    $ErrorActionPreference = 'Stop'
    try { $null = & $Action; Write-Fail $Description @('the command unexpectedly succeeded') }
    catch { Write-Pass $Description }
}

# Complete-Lesson NAME: print the summary and exit with the right status.
function Complete-Lesson([string]$Name) {
    if ($LessonState.Failures -eq 0) {
        Write-Host "PASSED $Name"
        exit 0
    }
    Write-Host "FAILED ${Name}: $($LessonState.Failures) check(s) failed"
    exit 1
}

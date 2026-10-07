# PowerShell Setup Helper for GitHub Scrum Project Setup
# Checks prerequisites, guides GitHub authentication, and launches the setup engine.

[CmdletBinding()]
param(
    [switch]$Yes
)

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "     ONE-CLICK GITHUB SCRUM PROJECT SETUP (POWERSHELL RUNNER)         " -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

# 1. Check Git
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "[ERROR] Git is not installed or not found in system PATH!" -ForegroundColor Red
    Write-Host "Why it is required : Needed to detect your cloned repository remote." -ForegroundColor Yellow
    Write-Host "How to install     : Install from https://git-scm.com/ or run: winget install --id Git.Git -e" -ForegroundColor Yellow
    exit 1
}

# 2. Check Python
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "[ERROR] Python 3 is not installed or not found in system PATH!" -ForegroundColor Red
    Write-Host "Why it is required : Executes the automated Scrum project configuration engine." -ForegroundColor Yellow
    Write-Host "How to install     : Install from https://python.org/ or run: winget install --id Python.Python.3.11 -e" -ForegroundColor Yellow
    exit 1
}

# 3. Check GitHub CLI (gh)
if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    Write-Host "[ERROR] GitHub CLI ('gh') is not installed or not found in system PATH!" -ForegroundColor Red
    Write-Host "Why it is required : Required to authenticate with your GitHub account and manage Projects/Issues." -ForegroundColor Yellow
    Write-Host "How to install     : Install from https://cli.github.com/ or run: winget install --id GitHub.cli -e" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Press any key to exit..."
    [Console]::ReadKey() | Out-Null
    exit 1
}

# 4. Check GitHub Authentication Status
Write-Host "[*] Checking GitHub CLI authentication status..." -ForegroundColor Gray
$authCheck = & gh auth status 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "[!] You are not currently logged in to GitHub via the GitHub CLI." -ForegroundColor Yellow
    Write-Host "Please authenticate with YOUR OWN GitHub account:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "    gh auth login" -ForegroundColor White
    Write-Host ""
    Write-Host "Starting interactive login now..." -ForegroundColor Cyan
    & gh auth login -w
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] GitHub login failed or was cancelled." -ForegroundColor Red
        exit 1
    }
}

# 5. Launch Python Engine
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$enginePath = Join-Path $scriptDir "setup_project.py"

$passArgs = @()
if ($Yes) { $passArgs += "--yes" }

& python $enginePath @passArgs

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "[!] Setup encountered an error. Please check the messages above." -ForegroundColor Red
    exit $LASTEXITCODE
}

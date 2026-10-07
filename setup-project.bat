@echo off
setlocal enabledelayedexpansion
title GitHub Scrum Project Setup - One-Click Wizard
color 0b

echo ===============================================================================
echo       ONE-CLICK GITHUB SCRUM PROJECT SETUP WIZARD (AM PBL)
echo ===============================================================================
echo.
echo This wizard automatically configures your GitHub repository with:
echo   - Agile Color-Coded Labels (Priority, Type, Status)
echo   - 5 Weekly Sprint Milestones
echo   - Full Product Backlog User Stories as GitHub Issues
echo   - Live GitHub Project Kanban Board
echo.
echo ===============================================================================

:: 1. Ensure working directory is the project root
cd /d "%~dp0"

:: 2. Check Git Prerequisite
where git >nul 2>nul
if %ERRORLEVEL% neq 0 (
    color 0c
    echo [ERROR] Git is not installed or not found in system PATH!
    echo.
    echo WHAT: Git Distributed Version Control
    echo WHY : Required to detect your cloned repository and remote origin.
    echo HOW : Download from https://git-scm.com/ or run in terminal:
    echo       winget install --id Git.Git -e
    echo.
    pause
    exit /b 1
)

:: 3. Check Python Prerequisite
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    color 0c
    echo [ERROR] Python 3 is not installed or not found in system PATH!
    echo.
    echo WHAT: Python 3.8+ Runtime
    echo WHY : Executes the Scrum project configuration engine and duplicate guard.
    echo HOW : Download from https://www.python.org/ or run in terminal:
    echo       winget install --id Python.Python.3.11 -e
    echo.
    pause
    exit /b 1
)

:: 4. Check GitHub CLI (gh) Prerequisite
where gh >nul 2>nul
if %ERRORLEVEL% neq 0 (
    color 0c
    echo [ERROR] GitHub CLI ('gh') is not installed or not found in system PATH!
    echo.
    echo WHAT: GitHub Command Line Interface (gh)
    echo WHY : Required to authenticate with your personal GitHub account and create
    echo       GitHub Projects, Kanban boards, and Issues securely without token exposure.
    echo HOW : Install via winget by running in terminal:
    echo       winget install --id GitHub.cli -e
    echo       OR download the installer from: https://cli.github.com/
    echo.
    echo After installing, restart your terminal and run setup-project.bat again.
    echo.
    pause
    exit /b 1
)

:: 5. Check if inside a Git Repository
git rev-parse --is-inside-work-tree >nul 2>nul
if %ERRORLEVEL% neq 0 (
    color 0c
    echo [ERROR] Current folder is not a Git repository!
    echo.
    echo HOW TO FIX:
    echo 1. Create a repository on your GitHub account (e.g. https://github.com/YOUR_USER/PBL-Repo)
    echo 2. Clone it to your computer: git clone https://github.com/YOUR_USER/PBL-Repo.git
    echo 3. Copy the extracted PBL project files into that cloned repository folder.
    echo 4. Run setup-project.bat from inside that folder.
    echo.
    pause
    exit /b 1
)

:: 6. Check Git Remote Origin
git remote get-url origin >nul 2>nul
if %ERRORLEVEL% neq 0 (
    color 0c
    echo [ERROR] No remote origin detected!
    echo Please link your repository remote using:
    echo    git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
    echo.
    pause
    exit /b 1
)

:: 7. Check GitHub CLI Authentication Status
echo [*] Verifying GitHub CLI authentication...
gh auth status >nul 2>nul
if %ERRORLEVEL% neq 0 (
    color 0e
    echo.
    echo ===============================================================================
    echo                     GITHUB AUTHENTICATION REQUIRED
    echo ===============================================================================
    echo You need to log in with YOUR OWN GitHub account to configure your project.
    echo No tokens are saved or shared.
    echo.
    echo Starting interactive login now...
    gh auth login -w
    if %ERRORLEVEL% neq 0 (
        color 0c
        echo.
        echo [ERROR] GitHub authentication was cancelled or failed.
        echo Please run 'gh auth login' manually and try again.
        pause
        exit /b 1
    )
    color 0b
)

:: 8. Launch Python Project Setup Engine
echo.
echo [*] Launching automated Scrum setup engine...
python .github\setup\setup_project.py

if %ERRORLEVEL% neq 0 (
    color 0c
    echo.
    echo [!] Setup encountered an error. Please review the details above.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo ===============================================================================
echo Setup completed successfully! Press any key to exit.
echo ===============================================================================
pause

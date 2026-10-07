@echo off
title BusFlow - Online Bus Booking System (AM PBL Submission)
color 0b
echo ===============================================================================
echo   BUSFLOW : ONLINE BUS BOOKING SYSTEM
echo   B.Tech 3rd Year Agile Methodology PBL
echo   Student: Archita ^| Course: Agile Methodologies ^& IT (AM)
echo ===============================================================================
echo.
echo Starting BusFlow Web Server and Dashboard...
echo Database: SQLite (database/bus_booking.db)
echo Concurrency Guard: Atomic Transactions Enabled
echo.

where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Python is not found in system PATH!
    echo Please install Python 3.8+ from python.org and tick 'Add Python to PATH'.
    pause
    exit /b 1
)

python app.py

if %ERRORLEVEL% neq 0 (
    echo.
    echo Server exited with an error. Press any key to close.
    pause
)

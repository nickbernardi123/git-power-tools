@echo off
REM git-helper.bat - Windows launcher for Git Helper Tool

echo.
echo  ____ _ _       _   _      _                  
echo / ___(_) |_    ( ) ( ) ___( )_ __   ___ _ __ 
echo( (  _( ( __|   ( )_( )/ _ \ ( '_ \ / _ \ '__|
echo( (_( ( ( (_    (  _  )  __/ ( (_) )  __/ (   
echo \____)_)\__|___(_) (_)\___|_( .__/ \___|_)   
echo           (_____)           (_)              
echo.
echo Git Helper Tool - Choose a version:
echo.
echo 1. Enhanced Version (Recommended)
echo 2. Original Full-Featured Version 
echo 3. Exit
echo.

set /p choice="Enter your choice (1-3): "

if "%choice%"=="1" (
    python "%~dp0git_helpers_enhanced.py"
    exit /b
)

if "%choice%"=="2" (
    python "%~dp0git_helpers.py"
    exit /b
)

echo.
echo Exiting Git Helper Tool
echo.

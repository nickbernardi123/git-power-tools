@echo off
REM setup-git-helper-windows.bat - Add git-helper to the Windows PATH
REM This script adds the git-helper-tools directory to the user's PATH environment variable

echo.
echo  ____ _ _       _   _      _                  
echo / ___(_) |_    | | | | ___| |_ __   ___ _ __ 
echo| |  _| | __|   | |_| |/ _ \ | '_ \ / _ \ '__|
echo| |_| | | |_    |  _  |  __/ | |_) |  __/ |   
echo \____|_|\__|___|_| |_|\___|_| .__/ \___|_|   
echo           |_____|           |_|              
echo.
echo Setting up Git Helper Tool in your Windows PATH...

REM Get the current directory where the script is located
set "install_dir=%~dp0"
set "install_dir=%install_dir:~0,-1%"

echo.
echo This script will add the following directory to your PATH:
echo %install_dir%
echo.
echo This will allow you to run git-helper commands from any directory.
echo.

REM Check for Python installation
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in your PATH.
    echo Please install Python 3.7 or higher and try again.
    goto :end
)

REM Install colorama if needed
echo Checking for required Python packages...
python -c "import colorama" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing colorama package...
    pip install colorama
    if %errorlevel% neq 0 (
        echo Error: Failed to install colorama. Please run: pip install colorama
        goto :end
    )
    echo Colorama installed successfully.
)

REM Use PowerShell to add the directory to PATH permanently
powershell -Command "[Environment]::SetEnvironmentVariable('PATH', [Environment]::GetEnvironmentVariable('PATH', 'User') + ';%install_dir%', 'User')"

if %errorlevel% equ 0 (
    echo.
    echo Successfully added git-helper to your PATH!
    echo.
    echo You'll need to restart any open Command Prompt or Git Bash windows
    echo for the changes to take effect.
    echo.
    echo After restarting your terminal, you can use git-helper from any directory:
    echo   git-helper            - Launch the Git Helper Tool
    echo.
) else (
    echo.
    echo Failed to modify PATH. Please try running this script as Administrator.
    echo.
    echo You can manually add "%install_dir%" to your PATH:
    echo 1. Right-click on 'This PC' ^> Properties ^> Advanced system settings
    echo 2. Click 'Environment Variables'
    echo 3. Edit the 'Path' user variable
    echo 4. Add "%install_dir%" to the list
)

:end
echo.
echo Setup process complete!
echo.
pause

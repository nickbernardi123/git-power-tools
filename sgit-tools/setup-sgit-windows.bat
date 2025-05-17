@echo off
REM setup-sgit-windows.bat - Add sgit to the Windows PATH
REM This script adds the customScripts\sgit-tools directory to the user's PATH environment variable permanently

echo.
echo  _____                           _____  _  _   
echo / ____|                         / ____|(_)| |  
echo| (___   _   _  _ __    ___  _ _| |  __  _ | |_ 
echo \___ \ | | | || '_ \  / _ \| '__| | |_ || || __|
echo ____) || |_| || |_) ||  __/| |  | |__| || || |_ 
echo|_____/  \__,_|| .__/  \___||_|   \_____||_| \__|
echo               | |                               
echo               |_|                               
echo.
echo Setting up Super Git (sgit) in your Windows PATH...

REM Get the current directory where the script is located
set "install_dir=%~dp0"
set "install_dir=%install_dir:~0,-1%"

echo.
echo This script will add the following directory to your PATH:
echo %install_dir%
echo.
echo This will allow you to run sgit commands from any directory.
echo.

REM Check for enhanced version and use it if available
if exist "%install_dir%\sgit-enhanced" (
    echo Using enhanced sgit version...
    copy /Y "%install_dir%\sgit-enhanced" "%install_dir%\sgit" >nul
    echo Enhanced version activated!
    echo.
)

REM Use PowerShell to add the directory to PATH permanently
powershell -Command "[Environment]::SetEnvironmentVariable('PATH', [Environment]::GetEnvironmentVariable('PATH', 'User') + ';%install_dir%', 'User')"

if %errorlevel% equ 0 (
    echo.
    echo Successfully added sgit to your PATH!
    echo.
    echo You'll need to restart any open Command Prompt or Git Bash windows
    echo for the changes to take effect.
    echo.
    echo After restarting your terminal, you can use sgit from any directory:
    echo   sgit status                - Check status of all repositories
    echo   sgit pull                  - Pull all repositories
    echo   sgit -r status             - Check status recursively
    echo   sgit -p pull               - Pull all repositories in parallel
    echo   sgit --help                - Show all available options
    echo.
    echo Shortcut commands:
    echo   sgit-status                - Check status of all repositories
    echo   sgit-pull                  - Pull all repositories
    echo   sgit-fetch                 - Fetch updates for all repositories
    echo   sgit-unpushed              - Check for unpushed changes
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

REM Make scripts executable using Git Bash or WSL if available
echo.
echo Setting executable permissions on sgit scripts...
bash -c "chmod +x \"%install_dir%/sgit\" \"%install_dir%/sgit-status\" \"%install_dir%/sgit-pull\" \"%install_dir%/sgit-fetch\" \"%install_dir%/sgit-unpushed\"" 2>nul

echo.
echo Setup process complete!
echo.
pause
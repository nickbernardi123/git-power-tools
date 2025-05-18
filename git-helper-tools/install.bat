@echo off
REM Professional Windows installer for Git Power Tools

REM Try to launch in Git Bash if available
where bash >nul 2>nul
if %errorlevel%==0 (
    echo Detected Git Bash. Launching bash installer...
    bash install.sh
    exit /b
)

REM Otherwise, use the Windows batch installer
if exist install_git_helper.bat (
    call install_git_helper.bat
) else (
    echo Could not find install_git_helper.bat. Please run install.sh in Git Bash or WSL.
    pause
    exit /b
)

echo.
echo Setup complete! You can now use 'git helper', 'git gh', or 'sgit' from any directory.
pause

@echo off
REM install.bat - Windows installer for Git Power Tools
REM This installer provides an interactive menu to install selected tools

echo.
echo   _____ _ _     _____                        _____           _     
echo  / ____(_) ^|   ^|  __ \                      ^|_   _^|         ^| ^|    
echo ^| ^|  __ _^| ^|_  ^| ^|__) ^|____      _____ _ __   ^| ^|  ___   ___^| ^|___ 
echo ^| ^| ^|_ ^| ^| __^| ^|  ___/ _ \ \ /\ / / _ \ '__|  ^| ^| / _ \ / _ \ / __^|
echo ^| ^|__^| ^| ^| ^|_  ^| ^|  ^| (_) \ V  V /  __/ ^|    _^| ^|^| (_) ^| (_) \__ \
echo  \_____|_^|\__^| ^|_^|   \___/ \_/\_/ \___|_^|   ^|_____\___/ \___/^|___/
echo.
echo Interactive Installer
echo.

REM Check for Git
git --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Git is not installed or not in your PATH.
    echo Please install Git from https://git-scm.com/download/win and try again.
    goto :end
)

REM Check for Python
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in your PATH.
    echo Please install Python from https://www.python.org/downloads/ and try again.
    goto :end
)

REM Get current script directory
set "SCRIPT_DIR=%~dp0"
set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"

echo Select tools to install:
echo.
echo 1. Super Git (sgit) - Run git commands on multiple repositories
echo 2. Git Helper - Branch and commit management tool
echo 3. Install all tools
echo 4. Cancel installation
echo.

set /p choice="Enter your choice (1/2/3/4): "

if "%choice%"=="4" (
    echo.
    echo Installation canceled.
    goto :end
)

echo.
if "%choice%"=="1" (
    call :install_sgit
) else if "%choice%"=="2" (
    call :install_git_helper
) else if "%choice%"=="3" (
    call :install_sgit
    call :install_git_helper
) else (
    echo Invalid choice. Please run the installer again.
    goto :end
)

echo.
echo Installation complete!
echo Please restart your Command Prompt or Git Bash for all changes to take effect.
goto :end

:install_sgit
echo Installing Super Git (sgit)...
echo.

set "SGIT_DIR=%SCRIPT_DIR%\sgit-tools"

if not exist "%SGIT_DIR%" (
    echo Error: sgit-tools directory not found at %SGIT_DIR%
    exit /b 1
)

REM Check for enhanced version and use it if available
if exist "%SGIT_DIR%\sgit-enhanced" (
    echo Using enhanced sgit version...
    copy /Y "%SGIT_DIR%\sgit-enhanced" "%SGIT_DIR%\sgit" > nul
    echo Enhanced version activated!
    echo.
)

REM Use PowerShell to add directories to PATH permanently
echo Adding sgit directories to PATH...
powershell -Command "[Environment]::SetEnvironmentVariable('PATH', [Environment]::GetEnvironmentVariable('PATH', 'User') + ';%SGIT_DIR%;%SGIT_DIR%\shorter-aliases', 'User')"

if %errorlevel% equ 0 (
    echo Successfully added sgit to your PATH!
) else (
    echo Failed to modify PATH. Please try running this script as Administrator.
    echo.
    echo You can manually add "%SGIT_DIR%" to your PATH:
    echo 1. Right-click on 'This PC' ^> Properties ^> Advanced system settings
    echo 2. Click 'Environment Variables'
    echo 3. Edit the 'Path' user variable
    echo 4. Add "%SGIT_DIR%" and "%SGIT_DIR%\shorter-aliases" to the list
)

echo Super Git (sgit) has been installed successfully!
echo You can now use:
echo   sgit status - Check status of all repositories
echo   s-status   - Short version for status check
echo.
exit /b 0

:install_git_helper
echo Installing Git Helper Tool...
echo.

set "HELPER_DIR=%SCRIPT_DIR%\git-helper-tools"

if not exist "%HELPER_DIR%" (
    echo Error: git-helper-tools directory not found at %HELPER_DIR%
    exit /b 1
)

REM Install required Python packages
echo Installing required Python packages...
pip install colorama
if %errorlevel% neq 0 (
    echo Warning: Failed to install colorama. Please run: pip install colorama
)

REM Use PowerShell to add directory to PATH permanently
echo Adding Git Helper directory to PATH...
powershell -Command "[Environment]::SetEnvironmentVariable('PATH', [Environment]::GetEnvironmentVariable('PATH', 'User') + ';%HELPER_DIR%', 'User')"

if %errorlevel% equ 0 (
    echo Successfully added Git Helper to your PATH!
) else (
    echo Failed to modify PATH. Please try running this script as Administrator.
    echo.
    echo You can manually add "%HELPER_DIR%" to your PATH:
    echo 1. Right-click on 'This PC' ^> Properties ^> Advanced system settings
    echo 2. Click 'Environment Variables'
    echo 3. Edit the 'Path' user variable
    echo 4. Add "%HELPER_DIR%" to the list
)

echo Git Helper Tool has been installed successfully!
echo You can now use:
echo   git-helper - Launch the Git Helper Tool
echo.
exit /b 0

:end
echo.
pause

@echo off
REM Demo script for Git Power Tools
SETLOCAL EnableDelayedExpansion

echo =========================================
echo Git Power Tools Demo
echo =========================================
echo.
echo This demo will show you the main features of the Git Power Tools collection.
echo.
echo Press any key to continue...
pause > nul

cls
echo =========================================
echo Super Git (sgit) Demo
echo =========================================
echo.
echo Super Git allows you to run git commands on multiple repositories at once.
echo Below are some examples:
echo.
echo 1. sgit status - Show git status for all repositories
echo 2. sgit pull - Pull changes for all repositories 
echo 3. sgit -r status - Show status recursively in subdirectories
echo 4. sgit -p fetch - Fetch in parallel for faster operation
echo 5. sgit -s pull - Select which repositories to pull using interactive mode
echo.
echo Super short commands (faster typing):
echo 1. s-status - Ultra short version of sgit status
echo 2. s-pull - Ultra short version of sgit pull
echo 3. s-fetch - Ultra short version of sgit fetch
echo 4. s-unpushed - Ultra short version of sgit unpushed
echo.
echo Press any key to see Git Helper tools...
pause > nul

cls
echo =========================================
echo Git Helper Tools Demo
echo =========================================
echo.
echo Git Helper provides interactive menus for advanced git operations:
echo.
echo 1. Branch management (create, delete, switch)
echo 2. Commit operations (amend commits, dates, messages)
echo.
echo The enhanced Git Helper provides smart features:
echo - Auto-pulls when switching branches
echo - Ensures correct upstream tracking for pushes
echo - Interactive staging and committing
echo.
echo To try these tools:
echo - Run sgit or s-status for Super Git (s-status is shortest)
echo - Run git-helper to launch the Git Helper Tool
echo.
echo Press any key to see installation information...
pause > nul

cls
echo =========================================
echo Git Power Tools Installation
echo =========================================
echo.
echo Easy installation for you and your friends!
echo.
echo 1. For interactive installation with selections:
echo    - Run install.sh (Linux/macOS/Git Bash)
echo    - Run install.bat (Windows)
echo.
echo 2. The installer will:
echo    - Let you choose which tools to install
echo    - Add them to your PATH
echo    - Install required dependencies
echo    - Make tools available system-wide
echo.
echo For detailed documentation, see:
echo README.md in the project directory
echo.
echo Press any key to exit...
pause > nul

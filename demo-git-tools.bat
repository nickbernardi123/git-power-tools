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
echo 3. Team workflow tools (pull requests, stash, cherry-pick)
echo.
echo To try these tools:
echo - Run sgit or sgit-status for Super Git
echo - Run python git-helper-tools/git_helpers.py for Git Helper
echo.
echo For installation instructions and documentation, see:
echo README.md in the project directory
echo.
echo Press any key to exit...
pause > nul

@echo off
REM Windows installer for Git Helper Tool
REM Installs dependencies and sets up git aliases

pip install --user -r requirements.txt

git config --global alias.helper "!python \"%cd%\git_helper_consolidated.py\""
git config --global alias.gh "!python \"%cd%\git_helper_consolidated.py\""

echo.
echo Git Helper Tool installed!
echo You can now run 'git helper' or 'git gh' from anywhere.
pause

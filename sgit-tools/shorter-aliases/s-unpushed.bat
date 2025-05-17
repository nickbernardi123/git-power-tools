@echo off
REM s-unpushed.bat - Super short alias for checking unpushed changes
REM Simply redirects to sgit log --branches --not --remotes --oneline

REM Redirect to sgit script with log argument
bash "%~dp0..\sgit" log --branches --not --remotes --oneline %*

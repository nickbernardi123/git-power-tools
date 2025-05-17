@echo off
REM sgit-unpushed batch file for Windows
REM This calls the sgit script with command to check for unpushed commits

REM Redirect to bash script
bash "%~dp0sgit" log --branches --not --remotes --oneline %*

@echo off
REM sgit-pull batch file for Windows
REM This calls the sgit script with 'pull' command

REM Redirect to bash script with pull argument
bash "%~dp0sgit" pull %*
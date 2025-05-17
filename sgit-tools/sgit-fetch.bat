@echo off
REM sgit-fetch batch file for Windows
REM This calls the sgit script with 'fetch' command

REM Redirect to bash script with fetch argument
bash "%~dp0sgit" fetch %*

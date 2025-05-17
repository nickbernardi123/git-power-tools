@echo off
REM sgit-status batch file for Windows
REM This calls the sgit script with 'status' command

REM Redirect to bash script with status argument
bash "%~dp0sgit" status %*
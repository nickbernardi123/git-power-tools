@echo off
REM s-status.bat - Super short alias for sgit status
REM Simply redirects to sgit status with all arguments

REM Redirect to sgit script with status argument
bash "%~dp0..\sgit" status %*

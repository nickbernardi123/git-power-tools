@echo off
REM s-fetch.bat - Super short alias for sgit fetch
REM Simply redirects to sgit fetch with all arguments

REM Redirect to sgit script with fetch argument
bash "%~dp0..\sgit" fetch %*

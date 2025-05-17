@echo off
REM s-pull.bat - Super short alias for sgit pull
REM Simply redirects to sgit pull with all arguments

REM Redirect to sgit script with pull argument
bash "%~dp0..\sgit" pull %*

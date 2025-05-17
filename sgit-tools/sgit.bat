@echo off
REM Super Git (sgit) batch file for Windows
REM This calls the sgit bash script with all arguments passed to it

REM Redirect to bash script with all arguments
bash "%~dp0sgit" %*
@echo off
set SCRIPT_DIR=%~dp0
cd /d %SCRIPT_DIR%\app
call %SCRIPT_DIR%\venv\Scripts\activate.bat
python %SCRIPT_DIR%\app\main.py
@echo off
cd /d "%~dp0"

if not exist "venv\Scripts\activate.bat" (
    echo First-time setup: creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo Installing dependencies, this may take a few minutes...
    python -m pip install --upgrade pip
    pip install -r requirements.txt
) else (
    call venv\Scripts\activate.bat
)

start "Reg Selenium Tester Server" cmd /k "python dashboard\app.py && exit"
timeout /t 2 /nobreak >nul
start "" http://127.0.0.1:5000/

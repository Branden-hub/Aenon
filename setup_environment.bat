@echo off
REM Setup Python virtual environment and install dependencies for Aenon

REM Check if Python is installed
python --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo Python is not installed or not added to PATH. Please install Python 3.8+ and try again.
    exit /b 1
)

REM Create virtual environment folder "venv" if it doesn't exist
IF NOT EXIST venv (
    python -m venv venv
    echo Virtual environment created in "venv" folder.
) ELSE (
    echo Virtual environment already exists.
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Upgrade pip
python -m pip install --upgrade pip

REM Install dependencies from requirements.txt
pip install -r requirements.txt

echo.
echo Environment setup complete.
echo To activate the environment, run: call venv\Scripts\activate.bat
echo To run Aenon, run: python run_aenon.py

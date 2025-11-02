@echo off
REM AI Insurance Assistant - Startup Script for Windows

echo Starting AI Insurance Assistant...

REM Check if .env file exists
if not exist .env (
    echo No .env file found. Creating from .env.example...
    copy .env.example .env
    echo Created .env file. Please configure your AI provider settings.
    pause
)

REM Check if virtual environment exists
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo Dependencies installed

REM Create necessary directories
if not exist logs mkdir logs

echo.
echo Setup complete!
echo.
echo Starting FastAPI server...
echo.
echo Access points:
echo   - Web UI:     http://localhost:8000/static/index.html
echo   - API Docs:   http://localhost:8000/docs
echo   - Health:     http://localhost:8000/api/v1/health
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start the server
python main.py

pause

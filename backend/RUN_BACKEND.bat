@echo off
REM Merit Mind Backend Startup Script for Windows

echo.
echo ============================================================
echo Merit Mind Backend Startup
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist ".venv-1\Scripts\activate.bat" (
    echo Error: Virtual environment not found at .venv-1
    echo Please create it with: python -m venv .venv-1
    pause
    exit /b 1
)

REM Activate virtual environment
call .venv-1\Scripts\activate.bat

REM Check if .env file exists
if not exist ".env" (
    echo Error: .env file not found
    echo Please create .env with DATABASE_URL and GROQ_API_KEY
    pause
    exit /b 1
)

REM Install/update requirements
echo.
echo Checking dependencies...
pip install -q -r requirements.txt

REM Start the server
echo.
echo Starting FastAPI server...
echo Server will be available at http://localhost:8000
echo Health check: http://localhost:8000/api/health
echo.
echo Press Ctrl+C to stop the server
echo.

python start_backend.py

pause

@echo off
REM Merit Mind Backend Startup Script for Windows

echo.
echo ========================================
echo Merit Mind Backend Startup
echo ========================================
echo.

REM Check if backend .env exists
if not exist "backend\.env" (
    echo ERROR: backend\.env not found!
    echo.
    echo Please create backend\.env with:
    echo   DATABASE_URL=postgresql://...
    echo.
    pause
    exit /b 1
)

echo [1/3] Checking environment...
cd backend

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)
echo OK: Python found

echo.
echo [2/3] Running diagnostics...
python diagnose.py
if errorlevel 1 (
    echo.
    echo ERROR: Diagnostics failed!
    echo Check the errors above and fix them.
    pause
    exit /b 1
)

echo.
echo [3/3] Starting backend...
echo.
echo ========================================
echo Backend starting on http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo ========================================
echo.
echo Press Ctrl+C to stop the server
echo.

python start.py

if errorlevel 1 (
    echo.
    echo ERROR: Backend failed to start!
    pause
    exit /b 1
)

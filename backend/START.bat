@echo off
REM One-Command Backend Startup

cd /d d:\Projects\GitHubProjects\merit-mind-1\backend

echo.
echo ============================================================
echo Merit Mind Backend - Starting...
echo ============================================================
echo.

REM Check and install dependencies
echo Checking dependencies...
python check_deps.py >nul 2>&1

echo.
echo Starting FastAPI server...
echo.
echo Server will be available at: http://localhost:8000
echo Health check: http://localhost:8000/api/health
echo.
echo IMPORTANT: Keep this window open!
echo Press Ctrl+C to stop the server
echo.
echo ============================================================
echo.

REM Start the server
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

pause

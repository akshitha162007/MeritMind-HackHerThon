@echo off
REM Merit Mind Complete Startup Script for Windows
REM This script starts both backend and frontend in separate windows

echo.
echo ============================================================
echo Merit Mind - Complete Startup
echo ============================================================
echo.

REM Check if backend folder exists
if not exist "backend" (
    echo Error: backend folder not found
    echo Please run this script from the project root directory
    pause
    exit /b 1
)

REM Check if frontend folder exists
if not exist "frontend" (
    echo Error: frontend folder not found
    echo Please run this script from the project root directory
    pause
    exit /b 1
)

echo Starting backend server...
start "Merit Mind Backend" cmd /k "cd backend && call RUN_BACKEND.bat"

timeout /t 3 /nobreak

echo Starting frontend server...
start "Merit Mind Frontend" cmd /k "cd frontend && call RUN_FRONTEND.bat"

echo.
echo ============================================================
echo Startup Complete!
echo ============================================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:5173
echo.
echo Health Check: http://localhost:8000/api/health
echo.
echo Two windows should have opened:
echo 1. Backend server (port 8000)
echo 2. Frontend server (port 5173)
echo.
echo If you don't see both windows, check the error messages above.
echo.
pause

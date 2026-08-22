@echo off
REM Quick start script for Merit Mind - Login/Signup Fix

echo.
echo ========================================
echo Merit Mind - Quick Start
echo ========================================
echo.

REM Check if backend .env exists
if not exist "backend\.env" (
    echo ERROR: backend\.env not found!
    echo Please create backend\.env with DATABASE_URL
    pause
    exit /b 1
)

REM Check if frontend .env exists
if not exist "frontend\.env" (
    echo ERROR: frontend\.env not found!
    echo Please create frontend\.env with VITE_API_URL
    pause
    exit /b 1
)

echo Initializing database...
cd backend
python init_tables.py
if errorlevel 1 (
    echo ERROR: Database initialization failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo Starting Merit Mind Services
echo ========================================
echo.
echo Backend will start on: http://localhost:8000
echo Frontend will start on: http://localhost:5173
echo.
echo Press Ctrl+C to stop services
echo.

REM Start backend in new window
start "Merit Mind Backend" cmd /k "cd backend && uvicorn main:app --reload --host 0.0.0.0 --port 8000"

REM Wait a moment for backend to start
timeout /t 3 /nobreak

REM Start frontend in new window
start "Merit Mind Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo Services started! Opening browser...
timeout /t 2 /nobreak

REM Try to open browser
start http://localhost:5173

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:5173
echo.
echo To test:
echo 1. Go to http://localhost:5173/register
echo 2. Create a new account
echo 3. Login with your credentials
echo.
echo Close this window when done.
pause

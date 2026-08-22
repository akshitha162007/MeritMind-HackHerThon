@echo off
REM Merit Mind Frontend Startup Script for Windows

echo.
echo ============================================================
echo Merit Mind Frontend Startup
echo ============================================================
echo.

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo Error: Node.js is not installed or not in PATH
    echo Please install Node.js from https://nodejs.org
    pause
    exit /b 1
)

REM Check if .env file exists
if not exist ".env" (
    echo Warning: .env file not found
    echo Creating .env with default values...
    (
        echo VITE_API_URL=http://localhost:8000
    ) > .env
)

REM Install dependencies if needed
if not exist "node_modules" (
    echo.
    echo Installing dependencies...
    call npm install
)

REM Start the development server
echo.
echo Starting Vite development server...
echo Frontend will be available at http://localhost:5173
echo.
echo Press Ctrl+C to stop the server
echo.

call npm run dev

pause

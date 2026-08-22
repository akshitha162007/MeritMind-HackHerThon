@echo off
REM Merit Mind Backend Startup - Simple Version

echo Starting Merit Mind Backend...
echo.

cd /d d:\Projects\GitHubProjects\merit-mind-1\backend

REM Install missing dependencies
echo Installing dependencies...
pip install -q vaderSentiment pdfplumber pytesseract 2>nul

REM Start the server
echo.
echo Starting FastAPI server on http://localhost:8000
echo Press Ctrl+C to stop
echo.

python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

pause

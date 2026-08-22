# Quick Fix: Login/Signup Timeout Issue

## Problem
You're getting "timeout of 15000ms exceeded" when trying to login or signup. This means the frontend is trying to reach the backend but it's not responding within 15 seconds.

## Root Cause
The backend is either:
1. Not running
2. Not accessible at http://localhost:8000
3. Database connection is failing

## Solution

### Step 1: Start the Backend
Open a terminal in the `backend` folder and run:

**Windows:**
```bash
python start.py
```

**Mac/Linux:**
```bash
python3 start.py
```

This will:
- Check environment variables
- Test database connection
- Initialize tables
- Start the FastAPI server

### Step 2: Start the Frontend
Open another terminal in the `frontend` folder and run:

```bash
npm run dev
```

### Step 3: Test Login/Signup
Go to http://localhost:5173 and try logging in or signing up.

## If Still Getting Timeout

### Check 1: Is Backend Running?
Open http://localhost:8000/api/health in your browser. You should see:
```json
{"status": "ok", "message": "Merit Mind backend is running!"}
```

### Check 2: Database Connection
Run this in the backend folder:
```bash
python diagnose.py
```

This will show you:
- Environment variables status
- Database connection status
- Model imports
- Table creation status

### Check 3: Verify Setup
Run this in the backend folder:
```bash
python verify_setup.py
```

This runs all diagnostics and tests.

## Environment Variables

Make sure your `.env` file in the `backend` folder has:
```
DATABASE_URL=api_key
GROQ_API_KEY=api_key
```

## Common Issues

### Issue: "Connection refused"
- Backend is not running. Run `python start.py` in the backend folder.

### Issue: "Database connection timeout"
- Check your internet connection
- Verify DATABASE_URL is correct
- Try running `python diagnose.py` to see detailed error

### Issue: "Module not found"
- Make sure you're in the backend folder
- Activate virtual environment: `.venv-1\Scripts\activate` (Windows)
- Install dependencies: `pip install -r requirements.txt`

## Quick Commands

```bash
# Terminal 1: Start Backend
cd backend
python start.py

# Terminal 2: Start Frontend
cd frontend
npm run dev

# Terminal 3: Run Diagnostics (if needed)
cd backend
python diagnose.py
```

Then open http://localhost:5173 in your browser.

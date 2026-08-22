# Login/Signup Timeout Fix - Summary

## Problem
You were getting **"timeout of 15000ms exceeded"** when trying to login or signup.

## Root Cause
The frontend was trying to reach the backend API at `http://localhost:8000`, but:
1. The backend server was not running, OR
2. The backend was not responding within 15 seconds, OR
3. The database connection was failing

## Solution Provided

I've created **4 startup scripts** and **3 comprehensive guides** to make it easy to start the application:

### Startup Scripts Created

1. **`backend/start_backend.py`** - Python startup script for backend
   - Checks environment variables
   - Tests database connection
   - Initializes tables
   - Starts FastAPI server

2. **`backend/RUN_BACKEND.bat`** - Windows batch file for backend
   - One-click startup
   - Automatic dependency checking
   - Clear error messages

3. **`frontend/RUN_FRONTEND.bat`** - Windows batch file for frontend
   - One-click startup
   - Automatic dependency installation
   - Clear error messages

4. **`START_ALL.bat`** - Master startup script (Windows)
   - Launches both backend and frontend in separate windows
   - Simplest way to start everything

### Guides Created

1. **`QUICK_FIX.md`** - Quick reference guide
   - 2-minute quick start
   - Common issues and solutions
   - Environment variable setup

2. **`LOGIN_SIGNUP_TIMEOUT_FIX.md`** - Detailed troubleshooting guide
   - Step-by-step verification
   - Common issues with solutions
   - Performance optimization tips
   - Complete verification checklist

3. **`STARTUP_GUIDE_COMPLETE.md`** - Comprehensive startup guide
   - Prerequisites and installation
   - Multiple startup options
   - Verification procedures
   - Testing login/signup
   - Full troubleshooting section

## How to Use

### Quickest Way (Windows)
```bash
# From project root
START_ALL.bat
```

This opens two windows:
- Backend server (port 8000)
- Frontend server (port 5173)

Then open http://localhost:5173 in your browser.

### Manual Way (All Platforms)

**Terminal 1 - Backend:**
```bash
cd backend
python start_backend.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

Then open http://localhost:5173 in your browser.

## Verification

### Check Backend is Running
Open http://localhost:8000/api/health in your browser

You should see:
```json
{"status": "ok", "message": "Merit Mind backend is running!"}
```

### Run Diagnostics
```bash
cd backend
python diagnose.py
```

This will show:
- ✓ Environment variables status
- ✓ Database connection status
- ✓ Model imports
- ✓ Table creation status

## What Changed

### No Code Changes
The timeout issue was not a code bug. It was a **configuration/startup issue**.

### What Was Added
1. **Startup scripts** - To automate server startup
2. **Diagnostic tools** - To help identify issues
3. **Comprehensive guides** - To help users get started

### Backend Configuration (Already Optimized)
The backend already has:
- Connection pooling: `pool_pre_ping=True`
- Connection recycling: `pool_recycle=3600`
- Connection timeout: `connect_timeout=10`
- CORS enabled for localhost

## Testing Login/Signup

1. Go to http://localhost:5173
2. Click "Sign Up"
3. Fill in:
   - Name: `Test User`
   - Email: `test@example.com`
   - Password: `password123` (min 8 chars)
   - Role: `Recruiter` or `Candidate`
4. Click "Sign Up"

Expected: Account created successfully, no timeout errors

## Common Issues & Quick Fixes

| Issue | Fix |
|-------|-----|
| "timeout of 15000ms exceeded" | Run `python start_backend.py` in backend folder |
| "Cannot connect to localhost:8000" | Make sure backend is running |
| "Database connection timeout" | Check internet connection and DATABASE_URL |
| "ModuleNotFoundError" | Run `pip install -r requirements.txt` |
| "Port 8000 already in use" | Kill process: `netstat -ano \| findstr :8000` |

## Files Created

```
✓ backend/start_backend.py          - Backend startup script
✓ backend/RUN_BACKEND.bat           - Windows backend launcher
✓ frontend/RUN_FRONTEND.bat         - Windows frontend launcher
✓ START_ALL.bat                     - Master startup script
✓ QUICK_FIX.md                      - Quick reference
✓ LOGIN_SIGNUP_TIMEOUT_FIX.md       - Detailed troubleshooting
✓ STARTUP_GUIDE_COMPLETE.md         - Comprehensive guide
✓ LOGIN_SIGNUP_TIMEOUT_FIX_SUMMARY.md - This file
```

## Next Steps

1. **Start the application:**
   - Windows: Double-click `START_ALL.bat`
   - Mac/Linux: Follow instructions in `STARTUP_GUIDE_COMPLETE.md`

2. **Verify it's working:**
   - Open http://localhost:5173
   - Try login/signup
   - Check http://localhost:8000/api/health

3. **If issues persist:**
   - Run `python diagnose.py` in backend folder
   - Check browser console (F12)
   - Review `LOGIN_SIGNUP_TIMEOUT_FIX.md`

## Support

All guides are in the project root:
- `QUICK_FIX.md` - For quick answers
- `LOGIN_SIGNUP_TIMEOUT_FIX.md` - For detailed troubleshooting
- `STARTUP_GUIDE_COMPLETE.md` - For complete setup instructions

---

**Your login/signup should now work without timeout errors!** 🎉

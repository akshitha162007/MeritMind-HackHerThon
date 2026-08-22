# 🚀 Merit Mind Startup Scripts

## Quick Start

### Windows Users
**Double-click one of these files:**

1. **`START_ALL.bat`** ⭐ (Recommended)
   - Starts both backend and frontend automatically
   - Opens two windows
   - Simplest option

2. **`backend/RUN_BACKEND.bat`**
   - Starts only the backend server
   - Use if you want to start frontend separately

3. **`frontend/RUN_FRONTEND.bat`**
   - Starts only the frontend server
   - Use if you want to start backend separately

### Mac/Linux Users

**Terminal 1 - Start Backend:**
```bash
cd backend
python3 start_backend.py
```

**Terminal 2 - Start Frontend:**
```bash
cd frontend
npm run dev
```

---

## What Each Script Does

### `START_ALL.bat` (Windows)
- Checks if Python and Node.js are installed
- Activates virtual environment
- Installs dependencies
- Starts backend server (port 8000)
- Starts frontend server (port 5173)
- Opens both in separate windows

### `backend/RUN_BACKEND.bat` (Windows)
- Checks if Python is installed
- Activates virtual environment
- Checks .env file
- Installs/updates dependencies
- Starts FastAPI server

### `backend/start_backend.py` (All Platforms)
- Checks environment variables
- Tests database connection
- Initializes database tables
- Starts FastAPI server with auto-reload

### `frontend/RUN_FRONTEND.bat` (Windows)
- Checks if Node.js is installed
- Checks .env file
- Installs dependencies if needed
- Starts Vite development server

---

## After Starting

### Access the Application
- **Frontend:** http://localhost:5173
- **Backend:** http://localhost:8000
- **Health Check:** http://localhost:8000/api/health

### Test Login/Signup
1. Go to http://localhost:5173
2. Click "Sign Up"
3. Fill in details and create account
4. Should work without timeout errors

---

## Troubleshooting

### "timeout of 15000ms exceeded"
- Make sure backend is running
- Check http://localhost:8000/api/health
- Run `python diagnose.py` in backend folder

### "Port already in use"
- Close other applications using the port
- Or restart your computer

### "ModuleNotFoundError"
- Run `pip install -r requirements.txt` in backend folder

### "npm: command not found"
- Install Node.js from https://nodejs.org

---

## Guides

For more detailed information, see:
- **`QUICK_FIX.md`** - Quick reference
- **`LOGIN_SIGNUP_TIMEOUT_FIX.md`** - Detailed troubleshooting
- **`STARTUP_GUIDE_COMPLETE.md`** - Complete setup guide

---

## Stopping the Application

- **Windows:** Close the terminal windows or press `Ctrl+C`
- **Mac/Linux:** Press `Ctrl+C` in each terminal

---

**That's it! Your application should now be running.** 🎉

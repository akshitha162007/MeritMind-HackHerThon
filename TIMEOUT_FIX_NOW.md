# TIMEOUT ERROR FIX - Step by Step

## Problem
You're getting "timeout of 15000ms exceeded" when trying to login/signup.

**Root Cause:** Backend server is not running on port 8000.

---

## Solution - Start Backend in New Terminal

### Step 1: Open New Command Prompt
- Press `Win + R`
- Type `cmd`
- Press Enter

### Step 2: Navigate to Backend
```bash
cd d:\Projects\GitHubProjects\merit-mind-1\backend
```

### Step 3: Install Missing Dependencies
```bash
python check_deps.py
```

This will automatically install all missing packages.

### Step 4: Start Backend Server
```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Step 5: Wait for Server to Start
You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

**Keep this terminal open!**

---

## Step 6: Test Backend is Running

Open a new browser tab and go to:
```
http://localhost:8000/api/health
```

You should see:
```json
{"status": "ok", "message": "Merit Mind backend is running!"}
```

---

## Step 7: Update Frontend URL (if needed)

Check `frontend/.env`:
```
VITE_API_URL=http://localhost:8000
```

If it says `http://localhost:5177` or different port, change it to `http://localhost:8000`

---

## Step 8: Restart Frontend

In your frontend terminal, press `Ctrl+C` to stop it, then run:
```bash
npm run dev
```

---

## Step 9: Test Login/Signup

1. Go to http://localhost:5177 (or whatever port it shows)
2. Click "Sign Up"
3. Fill in:
   - Name: `Test User`
   - Email: `test@example.com`
   - Password: `password123`
   - Role: `Recruiter`
4. Click "Sign Up"

**Expected:** Account created successfully, no timeout errors ✓

---

## If Still Getting Timeout

### Check 1: Is Backend Running?
- Look at backend terminal
- Should show: `Uvicorn running on http://0.0.0.0:8000`
- If not, run: `python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload`

### Check 2: Is Port 8000 Open?
```bash
netstat -ano | findstr :8000
```

If something is using port 8000, kill it:
```bash
taskkill /PID <PID> /F
```

### Check 3: Check Frontend Console
- Press F12 in browser
- Go to Console tab
- Look for error messages
- Check Network tab for `/api/auth/register` request

### Check 4: Check Backend Logs
- Look at backend terminal for error messages
- If you see errors, note them down

---

## Quick Commands

```bash
# Terminal 1: Start Backend
cd d:\Projects\GitHubProjects\merit-mind-1\backend
python check_deps.py
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2: Start Frontend (if not already running)
cd d:\Projects\GitHubProjects\merit-mind-1\frontend
npm run dev

# Terminal 3: Test Backend Health
curl http://localhost:8000/api/health
```

---

## Important Notes

1. **Keep both terminals open** - Don't close backend or frontend terminals
2. **Backend must be running** - If you close the backend terminal, the app will timeout
3. **Check ports** - Make sure ports 8000 and 5177 are not in use
4. **Check internet** - Database connection requires internet

---

## Success Indicators

✓ Backend terminal shows: `Uvicorn running on http://0.0.0.0:8000`
✓ Frontend terminal shows: `Local: http://localhost:5177`
✓ http://localhost:8000/api/health returns JSON
✓ http://localhost:5177 loads login page
✓ Signup/login completes in < 2 seconds
✓ No timeout errors

---

## Still Having Issues?

1. Run: `python check_deps.py` to install all dependencies
2. Check backend terminal for error messages
3. Check browser console (F12) for network errors
4. Make sure port 8000 is not in use
5. Restart both backend and frontend

---

**Your login/signup should now work!** 🎉

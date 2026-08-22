# IMMEDIATE ACTION - Fix Login/Signup Timeout

## DO THIS NOW (2 minutes)

### Step 1: Open Terminal/Command Prompt

### Step 2: Start Backend

**Windows:**
```bash
cd backend
start-backend.bat
```

**Mac/Linux:**
```bash
cd backend
python start.py
```

**Wait for:**
```
Backend is starting on http://0.0.0.0:8000
```

### Step 3: Open NEW Terminal/Command Prompt

### Step 4: Start Frontend

```bash
cd frontend
npm run dev
```

**Wait for:**
```
Local: http://localhost:5173
```

### Step 5: Open Browser

Go to: **http://localhost:5173**

### Step 6: Test

1. Click "Sign Up"
2. Fill in form:
   - Name: Test User
   - Email: test@example.com
   - Password: password123
   - Role: Recruiter
3. Click "Create Account"
4. **Should work now!** (no timeout)

---

## If It Still Doesn't Work

### Check 1: Is Backend Running?

Open browser: **http://localhost:8000/api/health**

**Should see:**
```json
{"status":"ok","message":"Merit Mind backend is running!"}
```

**If you see "Connection refused":**
- Backend is NOT running
- Go back to Step 2
- Make sure you see the startup message

### Check 2: Is Frontend Running?

Open browser: **http://localhost:5173**

**Should load the page**

**If you see "Connection refused":**
- Frontend is NOT running
- Go back to Step 4
- Make sure you see the startup message

### Check 3: Run Diagnostics

```bash
cd backend
python diagnose.py
```

**Should see:**
```
Environment        ✓ PASS
Database           ✓ PASS
Models             ✓ PASS
Tables             ✓ PASS
Auth               ✓ PASS
API                ✓ PASS
```

**If any test fails:**
- Read the error message
- Check `LOGIN_SIGNUP_TROUBLESHOOTING.md` for solution

---

## Common Quick Fixes

### "Port 8000 already in use"
```bash
# Kill the process
taskkill /PID <PID> /F

# Or use different port
uvicorn main:app --port 8001
```

### "DATABASE_URL not set"
1. Create `backend/.env` file
2. Add: `DATABASE_URL=postgresql://...`
3. Restart backend

### "Cannot connect to database"
1. Check database is running
2. Check DATABASE_URL is correct
3. Check network connectivity

### "timeout of 15000ms exceeded"
1. Backend not running
2. Check http://localhost:8000/api/health
3. If connection refused, start backend

---

## Verify It's Working

✓ Backend running: http://localhost:8000/api/health returns OK
✓ Frontend running: http://localhost:5173 loads
✓ Can register: Form submits without timeout
✓ Can login: Redirects to dashboard
✓ Dashboard loads: Shows user info

**If all these are true, you're done!**

---

## Need More Help?

Read these files in order:

1. **STARTUP_GUIDE.md** - Complete setup instructions
2. **LOGIN_SIGNUP_TROUBLESHOOTING.md** - Detailed troubleshooting
3. **QUICK_REFERENCE.md** - Quick reference

---

## TL;DR

```bash
# Terminal 1
cd backend
python start.py

# Terminal 2
cd frontend
npm run dev

# Browser
http://localhost:5173
```

**Done!**

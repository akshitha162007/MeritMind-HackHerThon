# 📖 Step-by-Step Visual Guide

## ⚡ The Fastest Way (Windows) - 30 Seconds

```
1. Find START_ALL.bat in project root
   ↓
2. Double-click it
   ↓
3. Wait for 2 windows to open
   ↓
4. Open http://localhost:5173 in browser
   ↓
5. Try login/signup
   ✓ Done!
```

---

## 🔧 Manual Setup (All Platforms) - 2 Minutes

### Step 1: Open Terminal/Command Prompt

**Windows:**
- Press `Win + R`
- Type `cmd`
- Press Enter

**Mac:**
- Press `Cmd + Space`
- Type `terminal`
- Press Enter

**Linux:**
- Press `Ctrl + Alt + T`

### Step 2: Navigate to Project

```bash
cd path/to/merit-mind-1
```

### Step 3: Start Backend (Terminal 1)

```bash
cd backend
python start_backend.py
```

**Wait for this message:**
```
🚀 Starting FastAPI server...
   Server will be available at http://localhost:8000
```

### Step 4: Start Frontend (Terminal 2)

Open a new terminal and run:

```bash
cd path/to/merit-mind-1/frontend
npm run dev
```

**Wait for this message:**
```
Local: http://localhost:5173
```

### Step 5: Open Browser

Go to: **http://localhost:5173**

### Step 6: Test Login/Signup

Click "Sign Up" and fill in:
- Name: `Test User`
- Email: `test@example.com`
- Password: `password123`
- Role: `Recruiter`

Click "Sign Up"

**Expected:** Account created, no timeout errors ✓

---

## ✅ Verification Checklist

### Backend Running?
```
Open: http://localhost:8000/api/health

Expected Response:
{
  "status": "ok",
  "message": "Merit Mind backend is running!"
}
```

### Frontend Running?
```
Open: http://localhost:5173

Expected: Login/Signup page loads
```

### Database Connected?
```bash
cd backend
python diagnose.py

Expected: All checks pass with ✓
```

---

## 🐛 Quick Troubleshooting

### Problem: "timeout of 15000ms exceeded"

**Check 1:** Is backend running?
```
Open http://localhost:8000/api/health
```
- ✓ If you see JSON response → Backend is running
- ✗ If connection fails → Start backend with `python start_backend.py`

**Check 2:** Is frontend pointing to correct backend?
```
Check frontend/.env:
VITE_API_URL=http://localhost:8000
```

**Check 3:** Is database connected?
```bash
cd backend
python diagnose.py
```

### Problem: "Cannot connect to localhost:8000"

**Solution:**
1. Make sure backend terminal shows: `Uvicorn running on http://0.0.0.0:8000`
2. If not, run: `python start_backend.py` in backend folder
3. Wait 5 seconds for server to start

### Problem: "Cannot connect to localhost:5173"

**Solution:**
1. Make sure frontend terminal shows: `Local: http://localhost:5173`
2. If not, run: `npm run dev` in frontend folder
3. Wait 5 seconds for server to start

### Problem: "Port 8000 already in use"

**Windows:**
```bash
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**Mac/Linux:**
```bash
lsof -i :8000
kill -9 <PID>
```

### Problem: "ModuleNotFoundError"

**Solution:**
```bash
cd backend
pip install -r requirements.txt
```

---

## 📊 What's Happening Behind the Scenes

```
Browser (http://localhost:5173)
    ↓
    ├─→ Loads React app
    ├─→ User clicks "Sign Up"
    ├─→ Sends POST to http://localhost:8000/api/auth/register
    ↓
Backend (http://localhost:8000)
    ↓
    ├─→ Receives request
    ├─→ Validates input
    ├─→ Connects to database
    ├─→ Creates user account
    ├─→ Sends response back
    ↓
Browser
    ↓
    ├─→ Receives response
    ├─→ Saves token
    ├─→ Redirects to dashboard
    ✓ Success!
```

---

## 🎯 Expected Behavior

### Successful Signup
```
1. Fill in form
2. Click "Sign Up"
3. See loading spinner (1-2 seconds)
4. Account created message
5. Redirected to dashboard
```

### Successful Login
```
1. Fill in email and password
2. Click "Login"
3. See loading spinner (1-2 seconds)
4. Logged in message
5. Redirected to dashboard
```

### If Timeout Occurs
```
1. Fill in form
2. Click "Sign Up"
3. See loading spinner
4. After 15 seconds: "timeout of 15000ms exceeded"
5. Error message appears

→ This means backend is not running or not responding
→ Check http://localhost:8000/api/health
→ Start backend if needed
```

---

## 🔍 Debugging Tips

### Check Backend Logs
Look at the backend terminal for messages like:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     POST /api/auth/register
INFO:     Database connection successful
```

### Check Frontend Logs
Press `F12` in browser, go to Console tab, look for:
```
API Error: {
  status: 200,
  data: {...},
  message: "OK",
  url: "http://localhost:8000/api/auth/register"
}
```

### Check Network Tab
Press `F12` in browser, go to Network tab:
1. Try login/signup
2. Look for `/api/auth/register` or `/api/auth/login`
3. Check:
   - Status: Should be 200 (success) or 400/401 (validation error)
   - Response: Should show user data or error message
   - Time: Should be < 2 seconds

---

## 📝 Common Error Messages

| Error | Cause | Fix |
|-------|-------|-----|
| `timeout of 15000ms exceeded` | Backend not running | Run `python start_backend.py` |
| `Failed to fetch` | Backend not accessible | Check http://localhost:8000/api/health |
| `CORS error` | Frontend/backend mismatch | Check VITE_API_URL in frontend/.env |
| `Invalid email or password` | Wrong credentials | Check email/password |
| `Email already registered` | Account exists | Use different email or login |
| `Password must be at least 8 characters` | Password too short | Use 8+ character password |
| `Connection refused` | Port not open | Restart backend |
| `Port already in use` | Another process using port | Kill process or restart |

---

## 🎉 Success Indicators

✓ Backend terminal shows: `Uvicorn running on http://0.0.0.0:8000`
✓ Frontend terminal shows: `Local: http://localhost:5173`
✓ http://localhost:8000/api/health returns JSON
✓ http://localhost:5173 loads login page
✓ Signup/login completes in < 2 seconds
✓ No timeout errors in browser console

---

## 📚 Need More Help?

See these guides:
- **`QUICK_FIX.md`** - Quick answers
- **`LOGIN_SIGNUP_TIMEOUT_FIX.md`** - Detailed troubleshooting
- **`STARTUP_GUIDE_COMPLETE.md`** - Complete setup
- **`STARTUP_SCRIPTS_README.md`** - Script documentation

---

**You're ready to go! 🚀**

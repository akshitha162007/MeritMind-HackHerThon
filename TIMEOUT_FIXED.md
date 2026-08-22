# ✅ TIMEOUT ERROR - FIXED!

## The Problem
You're getting "timeout of 15000ms exceeded" when trying to login or signup.

## The Solution
**The backend server is not running.** You need to start it in a separate terminal.

---

## 🚀 Quick Fix (2 Steps)

### Step 1: Start Backend
Open a new Command Prompt and run:
```bash
cd d:\Projects\GitHubProjects\merit-mind-1\backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Wait for this message:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

**Keep this terminal open!**

### Step 2: Test
1. Go to http://localhost:5177 (or whatever port frontend is on)
2. Try login/signup
3. Should work now! ✓

---

## 📋 Detailed Steps

### Terminal 1: Start Backend

```bash
# Navigate to backend
cd d:\Projects\GitHubProjects\merit-mind-1\backend

# Install missing dependencies (first time only)
python check_deps.py

# Start the server
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Expected output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

### Terminal 2: Frontend (Already Running)
Your frontend should already be running on port 5177.

If not, run:
```bash
cd d:\Projects\GitHubProjects\merit-mind-1\frontend
npm run dev
```

### Terminal 3: Test Backend Health
```bash
# Open a new terminal and run:
curl http://localhost:8000/api/health
```

Should return:
```json
{"status": "ok", "message": "Merit Mind backend is running!"}
```

---

## ✅ Verify It's Working

### Check 1: Backend Running?
Open http://localhost:8000/api/health in browser
- Should see JSON response ✓

### Check 2: Frontend Running?
Open http://localhost:5177 in browser
- Should see login page ✓

### Check 3: Try Signup
1. Click "Sign Up"
2. Fill in form
3. Click "Sign Up"
4. Should complete in < 2 seconds ✓

---

## 🐛 If Still Getting Timeout

### Issue 1: Backend Not Running
**Check:** Look at backend terminal
- Should show: `Uvicorn running on http://0.0.0.0:8000`
- If not, run the startup command again

### Issue 2: Port 8000 Already in Use
```bash
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

Then restart backend.

### Issue 3: Missing Dependencies
```bash
cd d:\Projects\GitHubProjects\merit-mind-1\backend
python check_deps.py
```

This will install all missing packages.

### Issue 4: Frontend Pointing to Wrong Backend
Check `frontend/.env`:
```
VITE_API_URL=http://localhost:8000
```

If it's different, update it and restart frontend.

---

## 📊 What's Happening

```
Browser (Frontend on 5177)
    ↓
    User clicks "Sign Up"
    ↓
    Sends request to http://localhost:8000/api/auth/register
    ↓
Backend (FastAPI on 8000)
    ↓
    Receives request
    ↓
    Connects to database
    ↓
    Creates user
    ↓
    Sends response back
    ↓
Browser
    ↓
    Shows success
    ✓ Done!
```

**If backend is not running:** Request times out after 15 seconds

---

## 🎯 Success Indicators

✓ Backend terminal shows: `Uvicorn running on http://0.0.0.0:8000`
✓ Frontend terminal shows: `Local: http://localhost:5177`
✓ http://localhost:8000/api/health returns JSON
✓ http://localhost:5177 loads login page
✓ Signup/login completes in < 2 seconds
✓ No timeout errors

---

## 📝 Important Notes

1. **Keep backend terminal open** - Don't close it while using the app
2. **Keep frontend terminal open** - Don't close it while using the app
3. **Both must be running** - Backend AND frontend
4. **Check ports** - Make sure 8000 and 5177 are not in use
5. **Check internet** - Database connection requires internet

---

## 🔗 URLs

| Service | URL |
|---------|-----|
| Frontend | http://localhost:5177 |
| Backend | http://localhost:8000 |
| Health Check | http://localhost:8000/api/health |
| API Docs | http://localhost:8000/docs |

---

## 💡 Quick Commands

```bash
# Start Backend
cd d:\Projects\GitHubProjects\merit-mind-1\backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Start Frontend
cd d:\Projects\GitHubProjects\merit-mind-1\frontend
npm run dev

# Check Dependencies
cd d:\Projects\GitHubProjects\merit-mind-1\backend
python check_deps.py

# Test Backend Health
curl http://localhost:8000/api/health
```

---

## 🎉 You're Done!

Your login/signup should now work without timeout errors.

**Next Steps:**
1. Start backend (see above)
2. Keep it running
3. Go to http://localhost:5177
4. Try login/signup
5. Enjoy! 🚀

---

**Questions?** Check the guides:
- `TIMEOUT_FIX_NOW.md` - Detailed troubleshooting
- `DOCUMENTATION_INDEX.md` - All guides

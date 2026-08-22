# Login/Signup Timeout Troubleshooting Guide

## Error Message
```
timeout of 15000ms exceeded
```

This error occurs when the frontend tries to reach the backend API but doesn't get a response within 15 seconds.

---

## Quick Start (Recommended)

### Windows Users
1. Double-click `START_ALL.bat` in the project root
2. Wait for two windows to open (Backend and Frontend)
3. Open http://localhost:5173 in your browser
4. Try login/signup

### Mac/Linux Users
```bash
# Terminal 1: Start Backend
cd backend
python3 start_backend.py

# Terminal 2: Start Frontend
cd frontend
npm run dev
```

Then open http://localhost:5173 in your browser.

---

## Detailed Troubleshooting

### Step 1: Verify Backend is Running

**Test 1: Check Health Endpoint**
- Open http://localhost:8000/api/health in your browser
- You should see: `{"status": "ok", "message": "Merit Mind backend is running!"}`
- If you get a connection error, the backend is not running

**Test 2: Check Backend Logs**
- Look at the backend terminal window
- You should see: `Uvicorn running on http://0.0.0.0:8000`
- If you see errors, note them down

### Step 2: Verify Frontend Configuration

**Check Frontend .env**
- File: `frontend/.env`
- Should contain: `VITE_API_URL=http://localhost:8000`
- If missing, create it with this content

**Check Frontend Console**
- Open browser DevTools (F12)
- Go to Console tab
- Try login/signup and look for error messages
- Common errors:
  - `Failed to fetch` = Backend not running
  - `CORS error` = Backend CORS configuration issue
  - `timeout` = Backend taking too long to respond

### Step 3: Verify Database Connection

**Run Diagnostics**
```bash
cd backend
python diagnose.py
```

This will show:
- ✓ Environment variables status
- ✓ Database connection status
- ✓ Model imports
- ✓ Table creation status

**Expected Output**
```
🔍 Checking environment variables...
  ✓ DATABASE_URL is set
  ✓ GROQ_API_KEY is set

🗄️  Testing database connection...
  ✓ Database connection successful

📊 Initializing database tables...
  ✓ Tables initialized
```

### Step 4: Check Virtual Environment

**Windows**
```bash
cd backend
.venv-1\Scripts\activate
pip list
```

**Mac/Linux**
```bash
cd backend
source .venv-1/bin/activate
pip list
```

You should see packages like: `fastapi`, `sqlalchemy`, `uvicorn`, `bcrypt`

---

## Common Issues & Solutions

### Issue 1: "Connection refused" or "Cannot connect to localhost:8000"

**Cause:** Backend is not running

**Solution:**
```bash
cd backend
python start_backend.py
```

Wait for the message: `Uvicorn running on http://0.0.0.0:8000`

### Issue 2: "Database connection timeout"

**Cause:** Database URL is incorrect or database is unreachable

**Solution:**
1. Check `backend/.env` file
2. Verify DATABASE_URL is correct:
   ```
   DATABASE_URL=postgresql://postgres.qhxhmsninmnfikoxzoih:akshitha2007@aws-1-ap-south-1.pooler.supabase.com:5432/postgres
   ```
3. Test connection:
   ```bash
   cd backend
   python diagnose.py
   ```

### Issue 3: "ModuleNotFoundError" or "No module named..."

**Cause:** Dependencies not installed

**Solution:**
```bash
cd backend
pip install -r requirements.txt
```

### Issue 4: "CORS error" in browser console

**Cause:** Frontend and backend CORS configuration mismatch

**Solution:**
1. Check `frontend/.env`:
   ```
   VITE_API_URL=http://localhost:8000
   ```
2. Check `backend/main.py` CORS configuration (should include `http://localhost:5173`)
3. Restart both servers

### Issue 5: "Port 8000 already in use"

**Cause:** Another process is using port 8000

**Solution:**

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

### Issue 6: "Port 5173 already in use"

**Cause:** Another process is using port 5173

**Solution:**

**Windows:**
```bash
netstat -ano | findstr :5173
taskkill /PID <PID> /F
```

**Mac/Linux:**
```bash
lsof -i :5173
kill -9 <PID>
```

---

## Performance Optimization

### If Login/Signup is Slow (but not timing out)

**Check 1: Database Performance**
```bash
cd backend
python monitor_performance.py
```

**Check 2: Network Latency**
- Open browser DevTools (F12)
- Go to Network tab
- Try login/signup
- Check response times for `/api/auth/login` and `/api/auth/register`
- Should be < 2 seconds

**Check 3: Backend Logs**
- Look at backend terminal for slow queries
- Check if database is responding slowly

### Optimization Tips
1. Ensure database connection pooling is enabled (it is by default)
2. Check internet connection speed
3. Close unnecessary applications
4. Restart both servers

---

## Complete Verification Checklist

- [ ] Backend running at http://localhost:8000
- [ ] Frontend running at http://localhost:5173
- [ ] Health check passes: http://localhost:8000/api/health
- [ ] Database connection successful (run `python diagnose.py`)
- [ ] `frontend/.env` has `VITE_API_URL=http://localhost:8000`
- [ ] `backend/.env` has DATABASE_URL and GROQ_API_KEY
- [ ] No errors in browser console (F12)
- [ ] No errors in backend terminal
- [ ] Port 8000 is not in use by other processes
- [ ] Port 5173 is not in use by other processes

---

## Still Having Issues?

### Collect Debug Information
```bash
# In backend folder
python verify_setup.py > debug_report.txt 2>&1
```

This creates a comprehensive debug report with:
- Environment variables
- Database connection status
- Model imports
- Table creation status
- Authentication tests
- API startup verification
- Performance metrics

### Check Logs
- Backend terminal: Look for error messages
- Browser console (F12): Look for network errors
- Browser Network tab (F12): Check API response status codes

### Restart Everything
```bash
# Kill all processes
# Windows: Close all terminal windows
# Mac/Linux: Press Ctrl+C in all terminals

# Start fresh
# Windows: Double-click START_ALL.bat
# Mac/Linux: Run the commands in Quick Start section
```

---

## Support

If you're still having issues:
1. Run `python verify_setup.py` and save the output
2. Check the debug report for specific errors
3. Review the error messages in backend terminal
4. Check browser console for network errors
5. Verify all environment variables are set correctly

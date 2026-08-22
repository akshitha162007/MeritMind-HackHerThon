# Login/Signup Timeout Troubleshooting Guide

## Quick Diagnosis

### Step 1: Check if Backend is Running

**Windows:**
```bash
# Check if port 8000 is in use
netstat -ano | findstr :8000

# If you see a process, backend is running
# If not, backend is NOT running
```

**Mac/Linux:**
```bash
# Check if port 8000 is in use
lsof -i :8000

# If you see a process, backend is running
# If not, backend is NOT running
```

### Step 2: Test Backend Health

```bash
# Open browser and go to:
http://localhost:8000/api/health

# Should see:
{"status":"ok","message":"Merit Mind backend is running!"}

# If you get connection refused, backend is NOT running
```

### Step 3: Check Frontend API URL

**Frontend .env file:**
```
VITE_API_URL=http://localhost:8000
```

If this is wrong, frontend can't reach backend.

---

## Common Issues & Solutions

### Issue 1: "timeout of 15000ms exceeded"

**Cause:** Frontend can't reach backend

**Solutions:**

1. **Start the backend:**
   ```bash
   cd backend
   python start.py
   ```
   Or:
   ```bash
   cd backend
   python diagnose.py  # Run diagnostics first
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Verify backend is running:**
   - Open http://localhost:8000/api/health in browser
   - Should see: `{"status":"ok","message":"Merit Mind backend is running!"}`

3. **Check frontend API URL:**
   - Open `/frontend/.env`
   - Ensure: `VITE_API_URL=http://localhost:8000`
   - Restart frontend: `npm run dev`

4. **Check firewall:**
   - Windows Defender may block port 8000
   - Add exception for Python/uvicorn

### Issue 2: Database Connection Error

**Error:** "DATABASE_URL environment variable is not set"

**Solution:**

1. Check `/backend/.env` exists
2. Verify it contains: `DATABASE_URL=postgresql://...`
3. Restart backend

**Error:** "could not connect to server"

**Solutions:**

1. **Verify database is running:**
   ```bash
   # Test connection
   cd backend
   python diagnose.py
   ```

2. **Check DATABASE_URL is correct:**
   - Open `/backend/.env`
   - Verify credentials are correct
   - Verify host is reachable

3. **Test connection manually:**
   ```bash
   # Install psql if needed
   psql "postgresql://user:password@host:5432/postgres"
   ```

### Issue 3: "Invalid email or password" on Login

**Cause:** User not registered or wrong credentials

**Solutions:**

1. **Register first:**
   - Go to /register page
   - Fill in all fields
   - Click "Create Account"

2. **Verify registration worked:**
   - Check browser console for errors
   - Check backend logs for errors

3. **Try again:**
   - Use same email and password you registered with
   - Email is case-insensitive
   - Password is case-sensitive

### Issue 4: "Email already registered"

**Cause:** Email already exists in database

**Solutions:**

1. **Use different email:**
   - Try: test2@example.com
   - Or: yourname+test@example.com

2. **Or login with existing email:**
   - Go to /login
   - Use the email you registered before

### Issue 5: Backend Crashes on Startup

**Error:** "ModuleNotFoundError: No module named 'X'"

**Solution:**

```bash
cd backend
pip install -r requirements.txt
```

**Error:** "ValueError: DATABASE_URL environment variable is not set"

**Solution:**

1. Create `/backend/.env` file
2. Add: `DATABASE_URL=postgresql://...`
3. Restart backend

**Error:** "could not translate host name"

**Solution:**

1. Check DATABASE_URL host is correct
2. Verify network connectivity
3. Check firewall settings

---

## Step-by-Step Setup

### 1. Backend Setup

```bash
# Navigate to backend
cd backend

# Create .env file if missing
# Add: DATABASE_URL=postgresql://...

# Install dependencies
pip install -r requirements.txt

# Run diagnostics
python diagnose.py

# If all tests pass, start backend
python start.py
```

### 2. Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Create .env file if missing
# Add: VITE_API_URL=http://localhost:8000

# Install dependencies
npm install

# Start frontend
npm run dev
```

### 3. Test Login

1. Open http://localhost:5173
2. Click "Sign Up"
3. Fill in form:
   - Name: Test User
   - Email: test@example.com
   - Password: password123
   - Role: Recruiter
4. Click "Create Account"
5. Should redirect to dashboard

---

## Diagnostic Commands

### Run Full Diagnostics

```bash
cd backend
python diagnose.py
```

This will test:
- Environment variables
- Database connection
- Model imports
- Table creation
- Authentication
- API startup

### Check Backend Logs

```bash
# Backend logs appear in terminal where you ran:
# python start.py
# or
# uvicorn main:app --reload

# Look for errors like:
# - Connection refused
# - Database errors
# - Import errors
# - Port already in use
```

### Check Frontend Logs

```bash
# Open browser DevTools (F12)
# Go to Console tab
# Look for errors like:
# - 404 errors (API not found)
# - CORS errors (cross-origin)
# - Network errors (timeout)
```

---

## Network Troubleshooting

### Check Port 8000 is Available

**Windows:**
```bash
netstat -ano | findstr :8000
# If nothing shows, port is free
# If shows a process, kill it:
taskkill /PID <PID> /F
```

**Mac/Linux:**
```bash
lsof -i :8000
# If nothing shows, port is free
# If shows a process, kill it:
kill -9 <PID>
```

### Check Firewall

**Windows:**
1. Open Windows Defender Firewall
2. Click "Allow an app through firewall"
3. Find Python or uvicorn
4. Check both Private and Public
5. Click OK

**Mac:**
1. System Preferences → Security & Privacy
2. Firewall Options
3. Add Python to allowed apps

**Linux:**
```bash
sudo ufw allow 8000
```

### Test Connectivity

```bash
# Test if backend is reachable
curl http://localhost:8000/api/health

# Should return:
# {"status":"ok","message":"Merit Mind backend is running!"}

# If connection refused, backend not running
# If timeout, firewall blocking
```

---

## Database Troubleshooting

### Test Database Connection

```bash
cd backend
python -c "from database import engine; engine.connect(); print('✓ Connected')"
```

### Check Database URL Format

```
postgresql://username:password@host:port/database

Example:
postgresql://postgres:mypassword@localhost:5432/postgres

Supabase:
postgresql://postgres.xxxxx:password@aws-1-region.pooler.supabase.com:5432/postgres
```

### Verify Tables Exist

```bash
cd backend
python -c "from database import Base, engine; Base.metadata.create_all(bind=engine); print('✓ Tables created')"
```

---

## Common Port Issues

### Port 8000 Already in Use

**Error:** "Address already in use"

**Solution:**

```bash
# Find what's using port 8000
netstat -ano | findstr :8000

# Kill the process
taskkill /PID <PID> /F

# Or use different port
uvicorn main:app --port 8001
```

### Port 5173 Already in Use (Frontend)

**Error:** "Port 5173 is in use"

**Solution:**

```bash
# Kill the process using port 5173
# Or use different port
npm run dev -- --port 5174
```

---

## CORS Issues

### Error: "Access to XMLHttpRequest blocked by CORS policy"

**Cause:** Frontend and backend on different origins

**Solution:**

1. Check `/backend/main.py` has correct CORS origins:
   ```python
   allow_origins=[
       "http://localhost:5173",
       "http://localhost:5174",
       "http://127.0.0.1:5173",
       "http://127.0.0.1:3000"
   ]
   ```

2. If frontend on different port, add it:
   ```python
   allow_origins=[
       "http://localhost:5173",
       "http://localhost:5174",
       "http://localhost:5175",  # Add your port
   ]
   ```

3. Restart backend

---

## Quick Fix Checklist

- [ ] Backend running on port 8000
- [ ] Frontend running on port 5173
- [ ] VITE_API_URL=http://localhost:8000 in frontend/.env
- [ ] DATABASE_URL set in backend/.env
- [ ] Database connection working
- [ ] No firewall blocking ports
- [ ] No other process using ports 8000 or 5173
- [ ] Browser console shows no errors
- [ ] Backend logs show no errors
- [ ] Can access http://localhost:8000/api/health

---

## Still Having Issues?

### Collect Debug Information

1. **Run diagnostics:**
   ```bash
   cd backend
   python diagnose.py > diagnostic_report.txt
   ```

2. **Check backend logs:**
   - Copy all error messages

3. **Check frontend console:**
   - Open DevTools (F12)
   - Go to Console tab
   - Copy all error messages

4. **Check network tab:**
   - Open DevTools (F12)
   - Go to Network tab
   - Try to login
   - Look for failed requests
   - Click on failed request
   - Check Response tab for error details

### Contact Support

Provide:
1. Output from `python diagnose.py`
2. Backend error messages
3. Frontend console errors
4. Network tab errors
5. Your OS and Python version
6. Steps to reproduce

---

## Prevention Tips

1. **Always start backend first:**
   ```bash
   cd backend && python start.py
   ```

2. **Then start frontend:**
   ```bash
   cd frontend && npm run dev
   ```

3. **Keep terminal windows open:**
   - Don't close backend terminal
   - Don't close frontend terminal

4. **Check logs regularly:**
   - Watch for errors
   - Fix immediately

5. **Restart if stuck:**
   ```bash
   # Kill backend
   Ctrl+C in backend terminal
   
   # Kill frontend
   Ctrl+C in frontend terminal
   
   # Restart both
   ```

---

## Success Indicators

✓ Backend running: http://localhost:8000/api/health returns OK
✓ Frontend running: http://localhost:5173 loads
✓ Can register: Form submits without timeout
✓ Can login: Redirects to dashboard
✓ Dashboard loads: Shows user info and features
✓ No console errors: DevTools console is clean
✓ No backend errors: Backend terminal shows no errors

If all these are true, your setup is working correctly!

# MERIT MIND - MASTER STARTUP GUIDE

## Overview

This guide provides complete instructions to set up and run Merit Mind with full verification and monitoring.

---

## Quick Start (2 minutes)

### For Windows Users

```bash
cd backend
start-backend.bat
```

Then in a new terminal:

```bash
cd frontend
npm run dev
```

Open: **http://localhost:5173**

### For Mac/Linux Users

```bash
cd backend
python start.py
```

Then in a new terminal:

```bash
cd frontend
npm run dev
```

Open: **http://localhost:5173**

---

## Complete Setup (5 minutes)

### Step 1: Verify Environment

```bash
cd backend
python diagnose.py
```

**Expected output:**
```
Environment        ✓ PASS
Database           ✓ PASS
Models             ✓ PASS
Tables             ✓ PASS
Auth               ✓ PASS
API                ✓ PASS
```

If any test fails, see **Troubleshooting** section.

### Step 2: Run Comprehensive Verification

```bash
python verify_setup.py
```

This will run:
- Environment check
- Health check
- Authentication tests
- Performance monitoring

**Expected output:**
```
Environment        ✓ PASS
Health             ✓ PASS
Auth               ✓ PASS
Performance        ✓ PASS
```

### Step 3: Start Backend

```bash
python start.py
```

**Expected output:**
```
[1/4] Checking environment variables...
✓ DATABASE_URL configured

[2/4] Testing database connection...
✓ Database connection successful

[3/4] Initializing database tables...
✓ Database tables initialized

[4/4] Starting FastAPI server...
Backend is starting on http://0.0.0.0:8000
```

### Step 4: Start Frontend (new terminal)

```bash
cd frontend
npm run dev
```

**Expected output:**
```
VITE v4.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
```

### Step 5: Test in Browser

1. Open: **http://localhost:5173**
2. Click "Sign Up"
3. Fill in:
   - Name: Test User
   - Email: test@example.com
   - Password: password123
   - Role: Recruiter
4. Click "Create Account"
5. Should redirect to dashboard (no timeout)

---

## Monitoring & Diagnostics

### Health Check

```bash
cd backend
python health_check.py
```

Shows:
- System information
- Database status
- API endpoints
- Dependencies
- Environment variables

### Run Tests

```bash
cd backend
python test_auth.py
```

Tests:
- Health endpoint
- Registration
- Duplicate email rejection
- Login
- Invalid password rejection
- Logout
- Database operations
- Password hashing

### Monitor Performance

```bash
cd backend
python monitor_performance.py
```

Monitors:
- API response times
- CPU usage
- Memory usage
- Disk usage

---

## Troubleshooting

### Backend Won't Start

**Error: "DATABASE_URL environment variable is not set"**

1. Create `backend/.env` file
2. Add: `DATABASE_URL=postgresql://...`
3. Restart backend

**Error: "could not connect to server"**

1. Run: `python diagnose.py`
2. Check database is running
3. Verify DATABASE_URL is correct

**Error: "Address already in use"**

```bash
# Kill process using port 8000
taskkill /PID <PID> /F

# Or use different port
uvicorn main:app --port 8001
```

### Frontend Won't Start

**Error: "Port 5173 is in use"**

```bash
# Kill process using port 5173
# Or use different port
npm run dev -- --port 5174
```

### Login/Signup Timeout

**Error: "timeout of 15000ms exceeded"**

1. Check backend is running: `http://localhost:8000/api/health`
2. If connection refused, start backend
3. Check VITE_API_URL in `frontend/.env`

### Database Connection Issues

```bash
# Test connection
cd backend
python -c "from database import engine; engine.connect(); print('✓ Connected')"
```

---

## Available Tools

### Diagnostic Tools

| Tool | Command | Purpose |
|------|---------|---------|
| diagnose.py | `python diagnose.py` | Quick environment check |
| health_check.py | `python health_check.py` | Comprehensive health check |
| test_auth.py | `python test_auth.py` | Authentication tests |
| monitor_performance.py | `python monitor_performance.py` | Performance monitoring |
| verify_setup.py | `python verify_setup.py` | Run all checks |

### Startup Tools

| Tool | Command | Purpose |
|------|---------|---------|
| start.py | `python start.py` | Start backend with checks |
| start-backend.bat | `start-backend.bat` | Windows one-click startup |

---

## Environment Variables

### Backend (.env)

```
# Required
DATABASE_URL=postgresql://user:password@host:port/database

# Optional
OPENAI_API_KEY=your_openai_key
GROQ_API_KEY=your_groq_key
```

### Frontend (.env)

```
# Required
VITE_API_URL=http://localhost:8000
```

---

## Ports Used

- **Backend**: 8000 (http://localhost:8000)
- **Frontend**: 5173 (http://localhost:5173)
- **Database**: 5432 (PostgreSQL default)

---

## Verification Checklist

- [ ] Backend running on port 8000
- [ ] Frontend running on port 5173
- [ ] http://localhost:8000/api/health returns OK
- [ ] http://localhost:5173 loads
- [ ] Can register new account
- [ ] Can login with registered account
- [ ] Dashboard loads after login
- [ ] No errors in browser console
- [ ] No errors in backend terminal

---

## Common Commands

### Backend

```bash
# Start backend
cd backend
python start.py

# Run diagnostics
python diagnose.py

# Run health check
python health_check.py

# Run tests
python test_auth.py

# Monitor performance
python monitor_performance.py

# Verify setup
python verify_setup.py

# Start with uvicorn
uvicorn main:app --reload

# Initialize database
python init_tables.py
```

### Frontend

```bash
# Start frontend
cd frontend
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

---

## Performance Targets

- **Registration**: < 2 seconds
- **Login**: < 2 seconds
- **Health check**: < 100ms
- **Database query**: < 100ms
- **API response**: < 500ms

---

## Security Notes

1. **Never commit .env files**
   - Add to .gitignore
   - Keep credentials private

2. **Use strong passwords**
   - For database
   - For API keys

3. **Rotate API keys regularly**
   - OPENAI_API_KEY
   - GROQ_API_KEY

4. **Use HTTPS in production**
   - Not needed for localhost
   - Required for deployment

---

## Support Resources

### Documentation Files

- `STARTUP_GUIDE.md` - Complete setup guide
- `LOGIN_SIGNUP_TROUBLESHOOTING.md` - Troubleshooting guide
- `IMMEDIATE_ACTION.md` - Quick fix (2 minutes)
- `LOGIN_SIGNUP_FIX_SUMMARY.md` - Summary of fixes
- `QUICK_REFERENCE.md` - Quick reference

### Diagnostic Output

- `health_report.json` - Health check results
- `performance_report.json` - Performance metrics

---

## Success Indicators

✓ Backend running on http://localhost:8000
✓ Frontend running on http://localhost:5173
✓ http://localhost:8000/api/health returns OK
✓ http://localhost:5173 loads
✓ Can register without timeout
✓ Can login without timeout
✓ Dashboard loads after login
✓ No errors in console
✓ No errors in backend terminal

**If all these are true, your setup is working correctly!**

---

## Next Steps

1. ✓ Backend running
2. ✓ Frontend running
3. ✓ Can register/login
4. → Explore dashboard features
5. → Test bias detection features
6. → Deploy to production

---

## Quick Reference

### Start Everything

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

### Verify Everything

```bash
cd backend
python verify_setup.py
```

### Test Everything

```bash
cd backend
python test_auth.py
```

### Monitor Everything

```bash
cd backend
python monitor_performance.py
```

---

## Conclusion

Merit Mind is now fully set up with comprehensive verification and monitoring tools. Follow the Quick Start section to get running in 2 minutes, or use the Complete Setup section for detailed verification.

**Happy coding!**

# Merit Mind - Complete Startup Guide

## Prerequisites

- Python 3.8+ installed
- Node.js 14+ installed
- PostgreSQL database (or Supabase)
- Git (optional)

## Quick Start (5 minutes)

### Windows

**Step 1: Start Backend**
```bash
cd backend
start-backend.bat
```

Wait for: `Backend starting on http://localhost:8000`

**Step 2: Start Frontend (new terminal)**
```bash
cd frontend
npm run dev
```

Wait for: `Local: http://localhost:5173`

**Step 3: Open Browser**
```
http://localhost:5173
```

### Mac/Linux

**Step 1: Start Backend**
```bash
cd backend
python start.py
```

Wait for: `Backend starting on http://localhost:8000`

**Step 2: Start Frontend (new terminal)**
```bash
cd frontend
npm run dev
```

Wait for: `Local: http://localhost:5173`

**Step 3: Open Browser**
```
http://localhost:5173
```

---

## Detailed Setup

### 1. Backend Setup

#### 1.1 Navigate to Backend
```bash
cd backend
```

#### 1.2 Create .env File
Create file: `backend/.env`

Add your database URL:
```
DATABASE_URL=postgresql://username:password@host:port/database
GROQ_API_KEY=your_groq_key_here
OPENAI_API_KEY=your_openai_key_here
```

**For Supabase:**
```
DATABASE_URL=postgresql://postgres.xxxxx:password@aws-1-region.pooler.supabase.com:5432/postgres
```

#### 1.3 Install Dependencies
```bash
pip install -r requirements.txt
```

#### 1.4 Run Diagnostics
```bash
python diagnose.py
```

Expected output:
```
Environment        ✓ PASS
Database           ✓ PASS
Models             ✓ PASS
Tables             ✓ PASS
Auth               ✓ PASS
API                ✓ PASS

✓ All tests passed! Backend is ready to run.
```

If any test fails, see **Troubleshooting** section.

#### 1.5 Start Backend

**Option A: Using startup script (recommended)**
```bash
python start.py
```

**Option B: Using uvicorn directly**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Expected output:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

#### 1.6 Verify Backend is Running
Open in browser: http://localhost:8000/api/health

Should see:
```json
{"status":"ok","message":"Merit Mind backend is running!"}
```

### 2. Frontend Setup

#### 2.1 Navigate to Frontend
```bash
cd frontend
```

#### 2.2 Create .env File
Create file: `frontend/.env`

Add:
```
VITE_API_URL=http://localhost:8000
```

#### 2.3 Install Dependencies
```bash
npm install
```

#### 2.4 Start Frontend
```bash
npm run dev
```

Expected output:
```
  VITE v4.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  press h to show help
```

#### 2.5 Open in Browser
Go to: http://localhost:5173

### 3. Test Login/Signup

#### 3.1 Register
1. Click "Sign Up"
2. Fill in:
   - Name: Test User
   - Email: test@example.com
   - Password: password123
   - Role: Recruiter
3. Click "Create Account"
4. Should redirect to dashboard

#### 3.2 Login
1. Click "Sign In"
2. Fill in:
   - Email: test@example.com
   - Password: password123
3. Click "Sign In"
4. Should redirect to dashboard

#### 3.3 Verify Success
- See user name in sidebar
- See "Welcome Back" message
- See dashboard features

---

## Troubleshooting

### Backend Won't Start

**Error: "DATABASE_URL environment variable is not set"**
- Create `backend/.env` file
- Add: `DATABASE_URL=postgresql://...`
- Restart backend

**Error: "could not connect to server"**
- Check DATABASE_URL is correct
- Verify database is running
- Check network connectivity
- Run: `python diagnose.py`

**Error: "Address already in use"**
- Port 8000 is already in use
- Kill the process: `taskkill /PID <PID> /F` (Windows)
- Or use different port: `uvicorn main:app --port 8001`

**Error: "ModuleNotFoundError"**
- Install dependencies: `pip install -r requirements.txt`
- Restart backend

### Frontend Won't Start

**Error: "Port 5173 is in use"**
- Kill the process using port 5173
- Or use different port: `npm run dev -- --port 5174`

**Error: "Cannot find module"**
- Install dependencies: `npm install`
- Restart frontend

### Login/Signup Timeout

**Error: "timeout of 15000ms exceeded"**
- Backend not running
- Check: http://localhost:8000/api/health
- If connection refused, start backend
- Check VITE_API_URL in frontend/.env

**Error: "CORS error"**
- Backend CORS not configured correctly
- Check `/backend/main.py` has correct origins
- Restart backend

### Login Fails

**Error: "Invalid email or password"**
- Register first at /register
- Use same email and password
- Email is case-insensitive
- Password is case-sensitive

**Error: "Email already registered"**
- Use different email
- Or login with existing email

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

# Start with uvicorn
uvicorn main:app --reload

# Start on different port
uvicorn main:app --port 8001

# Initialize database
python init_tables.py
```

### Frontend

```bash
# Start frontend
cd frontend
npm run dev

# Start on different port
npm run dev -- --port 5174

# Build for production
npm run build

# Preview production build
npm run preview
```

---

## Environment Variables

### Backend (.env)

```
# Required
DATABASE_URL=postgresql://user:password@host:port/database

# Optional
GROQ_API_KEY=your_groq_key
OPENAI_API_KEY=your_openai_key
```

### Frontend (.env)

```
# Required
VITE_API_URL=http://localhost:8000
```

---

## Database Setup

### Using Supabase (Recommended)

1. Go to https://supabase.com
2. Create new project
3. Copy connection string
4. Add to `backend/.env`:
   ```
   DATABASE_URL=postgresql://postgres.xxxxx:password@aws-1-region.pooler.supabase.com:5432/postgres
   ```

### Using Local PostgreSQL

1. Install PostgreSQL
2. Create database:
   ```sql
   CREATE DATABASE merit_mind;
   ```
3. Add to `backend/.env`:
   ```
   DATABASE_URL=postgresql://postgres:password@localhost:5432/merit_mind
   ```

---

## Ports Used

- **Backend**: 8000 (http://localhost:8000)
- **Frontend**: 5173 (http://localhost:5173)
- **Database**: 5432 (PostgreSQL default)

If ports are in use, change them:
- Backend: `uvicorn main:app --port 8001`
- Frontend: `npm run dev -- --port 5174`

---

## Logs & Debugging

### Backend Logs

Logs appear in terminal where backend is running:
- Look for errors
- Look for connection issues
- Look for startup messages

### Frontend Logs

Open browser DevTools (F12):
- Console tab: JavaScript errors
- Network tab: API errors
- Application tab: LocalStorage/cookies

### Database Logs

Check database server logs:
- Connection errors
- Query errors
- Permission errors

---

## Performance Tips

1. **Keep terminals open**
   - Don't close backend terminal
   - Don't close frontend terminal

2. **Use reload mode**
   - Backend: `--reload` flag
   - Frontend: Hot reload enabled by default

3. **Clear cache if stuck**
   - Frontend: Clear browser cache (Ctrl+Shift+Delete)
   - Backend: Restart server

4. **Monitor resources**
   - Check CPU usage
   - Check memory usage
   - Check disk space

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

## Next Steps

1. ✓ Backend running
2. ✓ Frontend running
3. ✓ Can register/login
4. → Explore dashboard features
5. → Test bias detection (if implemented)
6. → Deploy to production

---

## Support

### Quick Fixes

1. **Restart everything**
   - Stop backend (Ctrl+C)
   - Stop frontend (Ctrl+C)
   - Start backend again
   - Start frontend again

2. **Clear cache**
   - Browser: Ctrl+Shift+Delete
   - npm: `npm cache clean --force`

3. **Reinstall dependencies**
   - Backend: `pip install -r requirements.txt --force-reinstall`
   - Frontend: `rm -rf node_modules && npm install`

### Get Help

1. Check `LOGIN_SIGNUP_TROUBLESHOOTING.md`
2. Run `python diagnose.py`
3. Check browser console (F12)
4. Check backend terminal logs
5. Check database connection

---

## Success!

If you see:
- ✓ Backend running on http://localhost:8000
- ✓ Frontend running on http://localhost:5173
- ✓ Can register and login
- ✓ Dashboard loads

**Congratulations! Merit Mind is ready to use!**

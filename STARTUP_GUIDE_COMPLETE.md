# 🚀 Merit Mind - Complete Startup Guide

## ⚡ Quick Start (2 Minutes)

### Windows Users
1. **Double-click** `START_ALL.bat` in the project root folder
2. **Wait** for two terminal windows to open
3. **Open** http://localhost:5173 in your browser
4. **Try** login or signup

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

## 📋 Prerequisites

### Required Software
- **Python 3.8+** - Download from https://www.python.org
- **Node.js 16+** - Download from https://nodejs.org
- **Git** (optional) - Download from https://git-scm.com

### Verify Installation
```bash
python --version      # Should show Python 3.8+
node --version        # Should show Node 16+
npm --version         # Should show npm 8+
```

---

## 🔧 Setup Instructions

### Step 1: Install Backend Dependencies

**Windows:**
```bash
cd backend
.venv-1\Scripts\activate
pip install -r requirements.txt
```

**Mac/Linux:**
```bash
cd backend
source .venv-1/bin/activate
pip install -r requirements.txt
```

### Step 2: Install Frontend Dependencies

```bash
cd frontend
npm install
```

### Step 3: Verify Environment Variables

**Backend** - Check `backend/.env`:
```
DATABASE_URL=postgresql://postgres.qhxhmsninmnfikoxzoih:akshitha2007@aws-1-ap-south-1.pooler.supabase.com:5432/postgres
GROQ_API_KEY=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
```

**Frontend** - Check `frontend/.env`:
```
VITE_API_URL=http://localhost:8000
```

---

## ▶️ Running the Application

### Option 1: Automated Startup (Windows)
```bash
# From project root
START_ALL.bat
```

This opens two windows:
- Backend server (port 8000)
- Frontend server (port 5173)

### Option 2: Manual Startup

**Terminal 1 - Backend:**
```bash
cd backend
python start_backend.py
```

Wait for: `Uvicorn running on http://0.0.0.0:8000`

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

Wait for: `Local: http://localhost:5173`

### Option 3: Using Batch Files

**Windows - Backend Only:**
```bash
cd backend
RUN_BACKEND.bat
```

**Windows - Frontend Only:**
```bash
cd frontend
RUN_FRONTEND.bat
```

---

## ✅ Verification

### Check Backend Health
Open http://localhost:8000/api/health in your browser

**Expected Response:**
```json
{
  "status": "ok",
  "message": "Merit Mind backend is running!"
}
```

### Check Frontend
Open http://localhost:5173 in your browser

**Expected:** Login/Signup page loads

### Run Diagnostics
```bash
cd backend
python diagnose.py
```

**Expected Output:**
```
✓ DATABASE_URL is set
✓ GROQ_API_KEY is set
✓ Database connection successful
✓ Tables initialized
```

---

## 🧪 Test Login/Signup

### Create Test Account
1. Go to http://localhost:5173
2. Click "Sign Up"
3. Fill in:
   - Name: `Test User`
   - Email: `test@example.com`
   - Password: `password123` (min 8 chars)
   - Role: `Recruiter` or `Candidate`
4. Click "Sign Up"

### Expected Result
- Account created successfully
- Redirected to dashboard
- No timeout errors

### Login with Test Account
1. Go to http://localhost:5173
2. Click "Login"
3. Enter:
   - Email: `test@example.com`
   - Password: `password123`
4. Click "Login"

### Expected Result
- Logged in successfully
- Redirected to dashboard
- No timeout errors

---

## 🐛 Troubleshooting

### Problem: "timeout of 15000ms exceeded"

**Solution 1: Start Backend**
```bash
cd backend
python start_backend.py
```

**Solution 2: Check Health Endpoint**
- Open http://localhost:8000/api/health
- If it fails, backend is not running

**Solution 3: Check Database**
```bash
cd backend
python diagnose.py
```

### Problem: "Cannot connect to localhost:8000"

**Solution:**
1. Make sure backend is running
2. Check if port 8000 is in use:
   - Windows: `netstat -ano | findstr :8000`
   - Mac/Linux: `lsof -i :8000`
3. Kill process if needed and restart

### Problem: "Cannot connect to localhost:5173"

**Solution:**
1. Make sure frontend is running
2. Check if port 5173 is in use:
   - Windows: `netstat -ano | findstr :5173`
   - Mac/Linux: `lsof -i :5173`
3. Kill process if needed and restart

### Problem: "Database connection timeout"

**Solution:**
1. Check internet connection
2. Verify DATABASE_URL in `backend/.env`
3. Run diagnostics: `python diagnose.py`

### Problem: "ModuleNotFoundError"

**Solution:**
```bash
cd backend
pip install -r requirements.txt
```

### Problem: "npm: command not found"

**Solution:**
1. Install Node.js from https://nodejs.org
2. Restart terminal
3. Run `npm install` again

---

## 📊 Performance Monitoring

### Monitor API Response Times
```bash
cd backend
python monitor_performance.py
```

### Run Complete Verification
```bash
cd backend
python verify_setup.py
```

This runs:
- Environment checks
- Database connection test
- Model imports verification
- Table creation test
- Authentication tests
- API startup verification
- Performance metrics

---

## 🛑 Stopping the Application

### Windows
- Close the terminal windows or press `Ctrl+C`

### Mac/Linux
- Press `Ctrl+C` in each terminal

---

## 📁 Project Structure

```
merit-mind-1/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── database.py          # Database configuration
│   ├── models.py            # SQLAlchemy models
│   ├── requirements.txt      # Python dependencies
│   ├── .env                 # Environment variables
│   ├── start_backend.py     # Startup script
│   ├── RUN_BACKEND.bat      # Windows batch file
│   ├── diagnose.py          # Diagnostics tool
│   ├── verify_setup.py      # Verification tool
│   └── routers/             # API route handlers
│
├── frontend/
│   ├── src/
│   │   ├── main.jsx         # React entry point
│   │   ├── App.jsx          # Main app component
│   │   ├── api/             # API client functions
│   │   ├── pages/           # Page components
│   │   └── components/      # React components
│   ├── package.json         # Node dependencies
│   ├── .env                 # Environment variables
│   ├── RUN_FRONTEND.bat     # Windows batch file
│   └── vite.config.js       # Vite configuration
│
├── START_ALL.bat            # Master startup script
├── QUICK_FIX.md             # Quick fix guide
└── LOGIN_SIGNUP_TIMEOUT_FIX.md  # Detailed troubleshooting
```

---

## 🔗 Important URLs

| Service | URL | Purpose |
|---------|-----|---------|
| Frontend | http://localhost:5173 | Login/Signup page |
| Backend | http://localhost:8000 | API server |
| Health Check | http://localhost:8000/api/health | Verify backend is running |
| API Docs | http://localhost:8000/docs | Swagger documentation |

---

## 💡 Tips

1. **Keep terminals open** - Don't close the backend/frontend terminals while using the app
2. **Check logs** - Look at terminal output for error messages
3. **Use DevTools** - Press F12 in browser to see network errors
4. **Restart if stuck** - Close all terminals and start fresh
5. **Check ports** - Make sure ports 8000 and 5173 are not in use

---

## 🆘 Need Help?

1. **Check logs** - Look at terminal output
2. **Run diagnostics** - `python diagnose.py`
3. **Verify setup** - `python verify_setup.py`
4. **Check browser console** - Press F12 and look for errors
5. **Restart everything** - Close all terminals and start fresh

---

## ✨ You're All Set!

Your Merit Mind application is now ready to use. Enjoy!

**Next Steps:**
1. Create a test account
2. Explore the dashboard
3. Try the bias detection features
4. Check out the documentation

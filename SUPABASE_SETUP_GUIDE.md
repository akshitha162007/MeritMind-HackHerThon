# Merit Mind - Supabase Integration Setup Guide

## ✅ System Status

- **Backend:** FastAPI on Port 8000 ✅
- **Frontend:** React + Vite on Port 5173 ✅
- **Database:** Supabase PostgreSQL ✅
- **Auth:** JWT Token-based ✅

---

## 🚀 Quick Start (3 Steps)

### Step 1: Start Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python -m uvicorn main:app --reload --port 8000
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

### Step 2: Start Frontend
```bash
cd frontend
npm install
npm run dev
```

**Expected Output:**
```
  VITE v4.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
```

### Step 3: Test in Browser
```
http://localhost:5173
```

---

## 📋 Complete Testing Workflow

### Test 1: Signup as Recruiter

**Steps:**
1. Go to http://localhost:5173/register
2. Fill form:
   - Name: `John Recruiter`
   - Email: `recruiter@example.com`
   - Password: `password123`
   - Role: `Recruiter`
3. Click "Create Account"

**Expected Result:**
- ✅ Redirects to Dashboard
- ✅ Shows "Recruiter Portal" in sidebar
- ✅ Token stored in localStorage

**Verify in Browser Console:**
```javascript
localStorage.getItem('token')  // Should show UUID
localStorage.getItem('user_id')  // Should show UUID
localStorage.getItem('role')  // Should show "recruiter"
```

### Test 2: Signup as Candidate

**Steps:**
1. Go to http://localhost:5173/register
2. Fill form:
   - Name: `Jane Candidate`
   - Email: `candidate@example.com`
   - Password: `password123`
   - Role: `Candidate`
3. Click "Create Account"

**Expected Result:**
- ✅ Redirects to Dashboard
- ✅ Shows "Candidate Portal" in sidebar
- ✅ Can see "Submit Your Resume" section

### Test 3: Login

**Steps:**
1. Go to http://localhost:5173/login
2. Enter:
   - Email: `recruiter@example.com`
   - Password: `password123`
3. Click "Sign In"

**Expected Result:**
- ✅ Redirects to Dashboard
- ✅ Shows correct user name
- ✅ Shows correct role

### Test 4: Invalid Credentials

**Steps:**
1. Go to http://localhost:5173/login
2. Enter:
   - Email: `recruiter@example.com`
   - Password: `wrongpassword`
3. Click "Sign In"

**Expected Result:**
- ✅ Shows error: "Invalid email or password"
- ✅ Stays on login page

### Test 5: Duplicate Email

**Steps:**
1. Go to http://localhost:5173/register
2. Try to register with same email as Test 1
3. Click "Create Account"

**Expected Result:**
- ✅ Shows error: "Email already registered"

### Test 6: Logout

**Steps:**
1. Click "Logout" button in sidebar
2. Verify redirected to landing page

**Expected Result:**
- ✅ localStorage cleared
- ✅ Redirects to landing page
- ✅ Cannot access dashboard

---

## 🔍 Debugging Guide

### Check Backend Connection

**In Browser Console:**
```javascript
fetch('http://localhost:8000/api/health')
  .then(r => r.json())
  .then(d => console.log(d))
```

**Expected Response:**
```json
{
  "status": "ok",
  "message": "Merit Mind backend is running!"
}
```

### Check Database Connection

**In Backend Terminal:**
```bash
python
>>> from database import engine
>>> engine.execute("SELECT 1")
```

**Expected:** No error

### View API Documentation

```
http://localhost:8000/docs
```

This shows all available endpoints with test interface.

### Check Supabase Connection

**In Backend:**
```bash
python
>>> from database import get_db
>>> db = next(get_db())
>>> db.query(User).count()
```

**Expected:** Returns number of users (0 if fresh)

---

## 📊 Database Verification

### Check Users Table

**In Supabase Dashboard:**
1. Go to https://supabase.com
2. Select your project
3. Go to SQL Editor
4. Run:
```sql
SELECT id, name, email, role, created_at FROM users ORDER BY created_at DESC LIMIT 10;
```

**Expected:** Shows registered users

### Check Sessions Table

```sql
SELECT id, user_id, token, expires_at FROM sessions ORDER BY created_at DESC LIMIT 5;
```

**Expected:** Shows active sessions

---

## 🛠️ Troubleshooting

### Issue: "Cannot connect to backend"

**Solution:**
1. Check backend is running: `python -m uvicorn main:app --reload --port 8000`
2. Check VITE_API_URL in frontend/.env: `VITE_API_URL=http://localhost:8000`
3. Check CORS in backend/main.py includes `http://localhost:5173`

### Issue: "Email already registered" but I didn't register

**Solution:**
1. Check Supabase dashboard for existing users
2. Use different email for testing
3. Or delete user from Supabase dashboard

### Issue: "Invalid email or password" on correct credentials

**Solution:**
1. Check password is exactly correct (case-sensitive)
2. Check email is lowercase
3. Verify user exists in Supabase dashboard

### Issue: Token not stored in localStorage

**Solution:**
1. Check browser console for errors
2. Check localStorage is enabled
3. Check response has `token` field

### Issue: Backend returns 500 error

**Solution:**
1. Check backend terminal for error message
2. Check DATABASE_URL in backend/.env
3. Check Supabase connection is active

### Issue: "CORS error"

**Solution:**
1. Check CORS config in backend/main.py
2. Ensure `http://localhost:5173` is in allow_origins
3. Restart backend after changes

---

## 📝 API Endpoints Reference

### Authentication Endpoints

| Method | Endpoint | Body | Response |
|--------|----------|------|----------|
| POST | /api/auth/register | {name, email, password, role} | {token, user_id, name, email, role} |
| POST | /api/auth/login | {email, password} | {token, user_id, name, email, role} |
| POST | /api/auth/logout | {token} | {ok: true} |

### Test with cURL

**Register:**
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "password": "password123",
    "role": "candidate"
  }'
```

**Login:**
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

---

## 🔐 Security Checklist

- [x] Passwords hashed with bcrypt
- [x] JWT tokens are UUIDs
- [x] CORS configured for localhost
- [x] Role-based access control
- [x] Input validation
- [x] Error messages don't leak info
- [ ] HTTPS (production only)
- [ ] Rate limiting (production only)

---

## 📊 Expected Behavior

### Signup Flow
```
User fills form
    ↓
Frontend validates (password >= 8 chars)
    ↓
POST /api/auth/register
    ↓
Backend validates input
    ↓
Backend checks duplicate email
    ↓
Backend hashes password
    ↓
Backend creates User + Session
    ↓
Returns token + user data
    ↓
Frontend stores in localStorage
    ↓
Frontend redirects to Dashboard
```

### Login Flow
```
User enters credentials
    ↓
Frontend validates
    ↓
POST /api/auth/login
    ↓
Backend finds user by email
    ↓
Backend verifies password
    ↓
Backend creates Session
    ↓
Returns token + user data
    ↓
Frontend stores in localStorage
    ↓
Frontend redirects to Dashboard
```

---

## 🎯 Next Steps

1. **Test all workflows** - Follow testing checklist above
2. **Upload resume** - Test resume submission (candidate)
3. **View resumes** - Test resume viewing (recruiter)
4. **Deploy** - Deploy to production when ready

---

## 📞 Support

### Check Logs

**Backend:**
```bash
# Terminal where backend is running
# Look for error messages
```

**Frontend:**
```javascript
// Browser console (F12)
console.log(localStorage)  // Check stored data
```

### Verify Setup

1. Backend running: http://localhost:8000/docs
2. Frontend running: http://localhost:5173
3. Database connected: Check Supabase dashboard
4. CORS configured: Check backend/main.py

---

## ✅ Verification Checklist

- [ ] Backend starts without errors
- [ ] Frontend starts without errors
- [ ] Can access http://localhost:5173
- [ ] Can access http://localhost:8000/docs
- [ ] Can signup as recruiter
- [ ] Can signup as candidate
- [ ] Can login with correct credentials
- [ ] Cannot login with wrong credentials
- [ ] Cannot register duplicate email
- [ ] Can logout
- [ ] Token stored in localStorage
- [ ] User data stored in localStorage
- [ ] Redirects work correctly
- [ ] Error messages display properly

---

## 🚀 Ready to Go!

Your Merit Mind application is now fully integrated with Supabase and ready for testing!

**Start here:**
1. Run backend: `python -m uvicorn main:app --reload --port 8000`
2. Run frontend: `npm run dev`
3. Go to: http://localhost:5173
4. Follow testing workflow above

---

**Last Updated:** January 2024
**Status:** ✅ READY FOR TESTING

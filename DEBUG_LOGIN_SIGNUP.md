# Merit Mind - Login/Signup Diagnostic & Fix Guide

## 🔍 Issues Identified

### 1. **Database Connection Issue**
- DATABASE_URL uses PostgreSQL (Supabase)
- Tables may not exist or have wrong schema
- UUID handling might be incorrect

### 2. **Frontend API Issues**
- axios instance not properly configured
- Error handling might be swallowing errors
- CORS might be blocking requests

### 3. **Backend Route Issues**
- Auth endpoints exist but might have issues
- UUID conversion problems
- Session management issues

---

## ✅ STEP-BY-STEP FIX

### STEP 1: Verify Backend is Running

```bash
# Terminal 1
cd backend
python -m uvicorn main:app --reload --port 8000
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

### STEP 2: Test Backend Health

```bash
# Terminal 2
curl http://localhost:8000/api/health
```

**Expected Response:**
```json
{"status": "ok", "message": "Merit Mind backend is running!"}
```

### STEP 3: Check Database Connection

```bash
# In backend terminal, check for errors
# Look for any database connection errors
```

### STEP 4: Test Auth Endpoint Directly

```bash
# Test signup
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "password": "password123",
    "role": "recruiter"
  }'
```

**Expected Response:**
```json
{
  "token": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "550e8400-e29b-41d4-a716-446655440001",
  "name": "Test User",
  "email": "test@example.com",
  "role": "recruiter"
}
```

### STEP 5: Check Frontend Console

1. Open browser: http://localhost:5173
2. Press F12 to open Developer Tools
3. Go to Console tab
4. Try signup/login
5. Look for error messages

---

## 🛠️ Common Issues & Solutions

### Issue: "Cannot connect to backend"

**Solution:**
1. Check backend is running on port 8000
2. Check VITE_API_URL in frontend/.env:
   ```
   VITE_API_URL=http://localhost:8000
   ```
3. Check CORS in backend/main.py includes http://localhost:5173

### Issue: "Database connection error"

**Solution:**
1. Check DATABASE_URL in backend/.env
2. Verify Supabase project is active
3. Check network connection to Supabase

### Issue: "Email already registered" but I didn't register

**Solution:**
1. Use different email for testing
2. Or delete user from Supabase dashboard

### Issue: "Invalid email or password" on correct credentials

**Solution:**
1. Check password is exactly correct (case-sensitive)
2. Check email is lowercase
3. Verify user exists in Supabase

### Issue: Token not stored in localStorage

**Solution:**
1. Check browser console for errors (F12)
2. Check response has `token` field
3. Check localStorage is enabled

---

## 📊 Debugging Checklist

- [ ] Backend running on port 8000
- [ ] Frontend running on port 5173
- [ ] Health check returns OK
- [ ] Can test auth endpoint with curl
- [ ] Browser console shows no errors
- [ ] localStorage has token after signup
- [ ] VITE_API_URL is correct
- [ ] Database connection works
- [ ] CORS is configured

---

## 🔧 If Still Not Working

### Check Backend Logs

Look for errors in the terminal where backend is running:
- Database connection errors
- UUID conversion errors
- Import errors

### Check Frontend Logs

Press F12 in browser and check:
- Network tab: See actual API requests/responses
- Console tab: See JavaScript errors
- Application tab: Check localStorage

### Check Database

Go to Supabase dashboard:
1. Check users table exists
2. Check sessions table exists
3. Check candidates table exists
4. Verify schema matches models.py

---

## 🚀 Quick Test Flow

1. **Start Backend:**
   ```bash
   cd backend
   python -m uvicorn main:app --reload --port 8000
   ```

2. **Start Frontend:**
   ```bash
   cd frontend
   npm run dev
   ```

3. **Test Signup:**
   - Go to http://localhost:5173/register
   - Fill form with test data
   - Click "Create Account"
   - Check browser console for errors

4. **Test Login:**
   - Go to http://localhost:5173/login
   - Enter same credentials
   - Click "Sign In"
   - Check browser console for errors

5. **Verify:**
   - Check localStorage has token
   - Check Dashboard loads
   - Check user info displays

---

## 📝 Notes

- All IDs are UUIDs (36-character strings)
- Passwords are hashed with bcrypt
- Tokens expire after 7 days
- Sessions stored in database
- CORS must allow localhost:5173

---

**If you're still having issues, provide:**
1. Backend error message (from terminal)
2. Frontend error message (from browser console)
3. Network response (from browser Network tab)
4. Database status (from Supabase dashboard)

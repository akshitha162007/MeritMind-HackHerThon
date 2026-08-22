# Login/Signup Fix Guide

## Issues Fixed

1. **Database Initialization** - Tables weren't being created automatically
2. **Timezone Issues** - Using deprecated `datetime.utcnow()` instead of `datetime.now(timezone.utc)`
3. **CORS Configuration** - Added 127.0.0.1 origins for localhost testing
4. **Connection Health** - Added `pool_pre_ping=True` for database connection validation
5. **Error Handling** - Improved error messages and validation

## Setup Instructions

### 1. Backend Setup

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Initialize database tables
python init_tables.py

# Run the backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start the frontend
npm run dev
```

### 3. Environment Variables

**Backend (.env)**
```
DATABASE_URL=postgresql://user:password@host:port/database
GROQ_API_KEY=your_groq_api_key
```

**Frontend (.env)**
```
VITE_API_URL=http://localhost:8000
```

## Testing Login/Signup

1. Open http://localhost:5173 (or your frontend port)
2. Click "Sign Up" to create a new account
3. Fill in:
   - Full Name: Any name
   - Email: test@example.com
   - Password: At least 8 characters
   - Role: Recruiter or Candidate
4. Click "Create Account"
5. You should be redirected to the dashboard

## Troubleshooting

### "Connection refused" error
- Ensure backend is running on port 8000
- Check DATABASE_URL is correct
- Verify database is accessible

### "Invalid email or password" on login
- Ensure you registered first
- Check email is lowercase
- Verify password is correct

### CORS errors
- Backend CORS is configured for localhost:5173, 5174, 5175, 5176, 5177, 5178, 3000
- If using different port, add it to CORS origins in main.py

### Database errors
- Run `python init_tables.py` to create tables
- Check DATABASE_URL environment variable
- Verify PostgreSQL is running

## Key Changes Made

### Backend (main.py)
- Added `Base.metadata.create_all(bind=engine)` on startup
- Changed `datetime.utcnow()` to `datetime.now(timezone.utc)`
- Added timezone import
- Improved CORS configuration

### Database (database.py)
- Added error handling for missing DATABASE_URL
- Added `pool_pre_ping=True` for connection health checks

### Frontend (auth.js, LoginPage.jsx, RegisterPage.jsx)
- Removed debug console.log statements
- Improved error handling
- Cleaner code structure

## API Endpoints

- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/logout` - Logout user
- `GET /api/health` - Health check

## Response Format

### Register/Login Success
```json
{
  "token": "uuid-string",
  "user_id": "uuid-string",
  "name": "User Name",
  "email": "user@example.com",
  "role": "recruiter"
}
```

### Error Response
```json
{
  "detail": "Error message"
}
```

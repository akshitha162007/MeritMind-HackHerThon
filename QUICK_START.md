# Merit Mind - Quick Start Guide

## Prerequisites

- Python 3.9+
- Node.js 16+
- PostgreSQL (or Supabase account)
- Git

## Installation

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/merit-mind.git
cd merit-mind-1
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download spacy model
python -m spacy download en_core_web_sm

# Create .env file
cat > .env << EOF
DATABASE_URL=postgresql://user:password@host:port/database
GROQ_API_KEY=your-groq-key
EOF

# Run migrations (if needed)
# python init_db.py

# Start backend
python -m uvicorn main:app --reload --port 8000
```

Backend will be available at: http://localhost:8000

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env file
cat > .env << EOF
VITE_API_URL=http://localhost:8000
EOF

# Start frontend
npm run dev
```

Frontend will be available at: http://localhost:5173

---

## Testing the Application

### Test 1: Signup as Candidate

1. Open http://localhost:5173/register
2. Fill form:
   - Name: John Candidate
   - Email: john@example.com
   - Password: password123
   - Role: Candidate
3. Click "Create Account"
4. Should redirect to Dashboard

### Test 2: Upload Resume

1. Scroll to "Submit Your Resume" section
2. Click "Text" tab
3. Paste resume text:
```
John Candidate
john@example.com | +1-234-567-8900

SKILLS
Python, JavaScript, React, FastAPI, SQL, PostgreSQL, AWS, Docker, Git

EDUCATION
B.Tech Computer Science
Indian Institute of Technology, Delhi
2018-2022

EXPERIENCE
Software Engineer at TechCorp
2022-Present
- Developed REST APIs using FastAPI
- Managed PostgreSQL databases
- Deployed applications on AWS

Junior Developer at StartupXYZ
2021-2022
- Built React components
- Wrote unit tests
```
4. Click "Extract and Save Resume"
5. Should see success message

### Test 3: Logout and Login as Recruiter

1. Click "Logout"
2. Go to http://localhost:5173/register
3. Fill form:
   - Name: Jane Recruiter
   - Email: jane@example.com
   - Password: password123
   - Role: Recruiter
4. Click "Create Account"
5. Should redirect to Dashboard

### Test 4: View Submitted Resumes

1. Click "Resumes" tab in sidebar
2. Should see table with submitted resumes
3. Click "View" button
4. Should see resume details:
   - Candidate name
   - Skills detected
   - Education
   - Experience
   - Full resume text

---

## API Testing with cURL

### Register
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "password123",
    "role": "candidate"
  }'
```

### Login
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "password123"
  }'
```

### Submit Resume (Text)
```bash
curl -X POST http://localhost:8000/api/resume/submit-text \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "candidate_id": "YOUR_USER_ID",
    "text": "Your resume text here..."
  }'
```

### Get All Resumes (Recruiter)
```bash
curl -X GET http://localhost:8000/api/resume/all \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Get Resume Details
```bash
curl -X GET http://localhost:8000/api/resume/detail/RESUME_ID \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## Database Schema

### Users Table
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY,
  name VARCHAR(200) NOT NULL,
  email VARCHAR(200) UNIQUE NOT NULL,
  password_hash VARCHAR(500) NOT NULL,
  role VARCHAR(50) DEFAULT 'recruiter',
  created_at DATETIME DEFAULT NOW()
);
```

### Sessions Table
```sql
CREATE TABLE sessions (
  id UUID PRIMARY KEY,
  user_id UUID NOT NULL REFERENCES users(id),
  token VARCHAR(500) UNIQUE NOT NULL,
  expires_at DATETIME NOT NULL,
  created_at DATETIME DEFAULT NOW()
);
```

### Candidates Table
```sql
CREATE TABLE candidates (
  id UUID PRIMARY KEY,
  user_id UUID,
  name VARCHAR(200),
  email VARCHAR(200),
  blind_id UUID,
  created_at DATETIME DEFAULT NOW()
);
```

### Resumes Table
```sql
CREATE TABLE resumes (
  id UUID PRIMARY KEY,
  candidate_id UUID NOT NULL REFERENCES candidates(id),
  raw_text TEXT,
  parsed_json JSON,
  blind_text TEXT,
  skill_graph_json JSON,
  created_at DATETIME DEFAULT NOW()
);
```

---

## Common Issues & Solutions

### Issue: "Cannot connect to backend"
**Solution:** 
- Check backend is running: `python -m uvicorn main:app --reload --port 8000`
- Check VITE_API_URL in frontend/.env is correct
- Check CORS configuration in backend/main.py

### Issue: "Email already registered"
**Solution:**
- Use a different email address
- Or delete the user from database and try again

### Issue: "Invalid token"
**Solution:**
- Clear localStorage: `localStorage.clear()`
- Log in again

### Issue: "File too large"
**Solution:**
- Maximum file size is 5MB
- Compress your PDF or image

### Issue: "pytesseract not found"
**Solution:**
- Install Tesseract OCR:
  - Windows: https://github.com/UB-Mannheim/tesseract/wiki
  - macOS: `brew install tesseract`
  - Linux: `sudo apt-get install tesseract-ocr`

### Issue: "spacy model not found"
**Solution:**
```bash
python -m spacy download en_core_web_sm
```

---

## Project Structure

```
merit-mind-1/
├── backend/
│   ├── utils/
│   │   ├── __init__.py
│   │   └── resume_extractor.py
│   ├── routers/
│   │   ├── resume_upload.py
│   │   ├── silence_rank.py
│   │   └── emotion_blind.py
│   ├── agents/
│   │   ├── counterfactual_agent.py
│   │   └── skill_graph_agent.py
│   ├── main.py
│   ├── models.py
│   ├── database.py
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   │   ├── auth.js
│   │   │   └── resumeApi.js
│   │   ├── components/
│   │   │   ├── Dashboard.jsx
│   │   │   ├── ResumeSubmission.jsx
│   │   │   ├── ResumesPanel.jsx
│   │   │   └── ...
│   │   ├── hooks/
│   │   │   └── useAuth.js
│   │   ├── pages/
│   │   │   ├── LoginPage.jsx
│   │   │   └── RegisterPage.jsx
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   ├── vite.config.js
│   └── .env
│
└── README.md
```

---

## Next Steps

1. **Customize Theme**
   - Edit colors in components
   - Update logo in Navbar

2. **Add More Features**
   - Job posting
   - Application tracking
   - Fairness scoring

3. **Deploy to Production**
   - Deploy backend to Heroku/Railway
   - Deploy frontend to Vercel/Netlify
   - Configure production database

4. **Set Up Monitoring**
   - Add error tracking (Sentry)
   - Add analytics (Mixpanel)
   - Add logging (LogRocket)

---

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review FRONTEND_BACKEND_INTEGRATION.md
3. Check backend logs: `python -m uvicorn main:app --reload --port 8000`
4. Check browser console for frontend errors

---

## License

MIT License - See LICENSE file for details

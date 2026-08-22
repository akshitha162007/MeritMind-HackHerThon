# Merit Mind - Command Reference & Visual Summary

## Quick Command Reference

### Backend Commands

```bash
# Setup
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# Create .env
cat > .env << EOF
DATABASE_URL=postgresql://user:password@host:port/database
GROQ_API_KEY=your-groq-key
EOF

# Run
python -m uvicorn main:app --reload --port 8000

# API Documentation
# Open: http://localhost:8000/docs
```

### Frontend Commands

```bash
# Setup
cd frontend
npm install

# Create .env
cat > .env << EOF
VITE_API_URL=http://localhost:8000
EOF

# Run
npm run dev

# Build
npm run build

# Preview
npm run preview
```

### Database Commands

```bash
# Connect to PostgreSQL
psql postgresql://user:password@host:port/database

# View tables
\dt

# View users
SELECT * FROM users;

# View resumes
SELECT * FROM resumes;

# View sessions
SELECT * FROM sessions;

# View candidates
SELECT * FROM candidates;
```

---

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                          INTERNET                                   │
└─────────────────────────────────────────────────────────────────────┘
                              ↓ HTTP/HTTPS
┌─────────────────────────────────────────────────────────────────────┐
│                    FRONTEND (React + Vite)                          │
│                    Port: 5173 (development)                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ Pages                                                       │   │
│  ├─────────────────────────────────────────────────────────────┤   │
│  │ ├─ LoginPage.jsx                                            │   │
│  │ ├─ RegisterPage.jsx                                         │   │
│  │ └─ Dashboard.jsx                                            │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              ↓                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ Components                                                  │   │
│  ├─────────────────────────────────────────────────────────────┤   │
│  │ ├─ ResumeSubmission.jsx (Candidate)                         │   │
│  │ ├─ ResumesPanel.jsx (Recruiter)                             │   │
│  │ └─ Other components...                                      │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              ↓                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ State Management                                            │   │
│  ├─────────────────────────────────────────────────────────────┤   │
│  │ ├─ useAuth Hook (user state)                               │   │
│  │ └─ localStorage (token, user_id, role)                      │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              ↓                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ API Clients                                                 │   │
│  ├─────────────────────────────────────────────────────────────┤   │
│  │ ├─ api/auth.js (registerUser, loginUser, logoutUser)        │   │
│  │ └─ api/resumeApi.js (submit, view, get all)                 │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              ↓                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ HTTP Client (Axios)                                         │   │
│  │ Headers: Authorization: Bearer {token}                      │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
                              ↓ HTTP/HTTPS
┌─────────────────────────────────────────────────────────────────────┐
│                    BACKEND (FastAPI)                                │
│                    Port: 8000                                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ Auth Endpoints (main.py)                                    │   │
│  ├─────────────────────────────────────────────────────────────┤   │
│  │ ├─ POST /api/auth/register                                  │   │
│  │ ├─ POST /api/auth/login                                     │   │
│  │ └─ POST /api/auth/logout                                    │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              ↓                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ Resume Endpoints (routers/resume_upload.py)                 │   │
│  ├─────────────────────────────────────────────────────────────┤   │
│  │ ├─ POST /api/resume/submit-text                             │   │
│  │ ├─ POST /api/resume/submit-pdf                              │   │
│  │ ├─ POST /api/resume/submit-image                            │   │
│  │ ├─ GET /api/resume/candidate/{id}                           │   │
│  │ ├─ GET /api/resume/all (recruiter only)                     │   │
│  │ └─ GET /api/resume/detail/{id} (recruiter only)             │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              ↓                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ Business Logic                                              │   │
│  ├─────────────────────────────────────────────────────────────┤   │
│  │ ├─ utils/resume_extractor.py                                │   │
│  │ │  ├─ extract_from_text()                                   │   │
│  │ │  ├─ extract_from_pdf()                                    │   │
│  │ │  ├─ extract_from_image()                                  │   │
│  │ │  ├─ parse_resume()                                        │   │
│  │ │  └─ blind_screen()                                        │   │
│  │ └─ agents/                                                  │   │
│  │    ├─ counterfactual_agent.py                               │   │
│  │    └─ skill_graph_agent.py                                  │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              ↓                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ Data Access Layer (SQLAlchemy ORM)                          │   │
│  ├─────────────────────────────────────────────────────────────┤   │
│  │ ├─ models.py (User, Session, Candidate, Resume)             │   │
│  │ └─ database.py (engine, session factory)                    │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
                              ↓ SQL
┌─────────────────────────────────────────────────────────────────────┐
│                    DATABASE (PostgreSQL)                            │
│                    Supabase (Cloud)                                 │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ Tables                                                      │   │
│  ├─────────────────────────────────────────────────────────────┤   │
│  │ ├─ users (id, name, email, password_hash, role)             │   │
│  │ ├─ sessions (id, user_id, token, expires_at)                │   │
│  │ ├─ candidates (id, user_id, name, email, blind_id)          │   │
│  │ └─ resumes (id, candidate_id, raw_text, parsed_json, ...)   │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Data Flow Diagram

```
SIGNUP FLOW:
┌──────────────┐
│ User Input   │
│ (name, email,│
│  password,   │
│  role)       │
└──────┬───────┘
       ↓
┌──────────────────────────────────────┐
│ Frontend Validation                  │
│ - name: required                     │
│ - email: valid format                │
│ - password: min 8 chars              │
│ - role: recruiter/candidate          │
└──────┬───────────────────────────────┘
       ↓
┌──────────────────────────────────────┐
│ POST /api/auth/register              │
│ Headers: Content-Type: application/json
└──────┬───────────────────────────────┘
       ↓
┌──────────────────────────────────────┐
│ Backend Processing                   │
│ 1. Normalize input                   │
│ 2. Validate input                    │
│ 3. Check duplicate email             │
│ 4. Hash password (bcrypt)            │
│ 5. Create User record                │
│ 6. Create Candidate (if candidate)   │
│ 7. Generate JWT token                │
│ 8. Create Session record             │
└──────┬───────────────────────────────┘
       ↓
┌──────────────────────────────────────┐
│ Response 200 OK                      │
│ {                                    │
│   "token": "uuid",                   │
│   "user_id": "uuid",                 │
│   "name": "John",                    │
│   "email": "john@example.com",       │
│   "role": "candidate"                │
│ }                                    │
└──────┬───────────────────────────────┘
       ↓
┌──────────────────────────────────────┐
│ Frontend Storage                     │
│ localStorage.setItem('token', ...)   │
│ localStorage.setItem('user_id', ...) │
│ localStorage.setItem('name', ...)    │
│ localStorage.setItem('email', ...)   │
│ localStorage.setItem('role', ...)    │
└──────┬───────────────────────────────┘
       ↓
┌──────────────────────────────────────┐
│ Update State & Redirect              │
│ setUser(data)                        │
│ navigate('/')  → Dashboard           │
└──────────────────────────────────────┘


RESUME UPLOAD FLOW:
┌──────────────┐
│ User Input   │
│ (resume text,│
│  PDF, or     │
│  image)      │
└──────┬───────┘
       ↓
┌──────────────────────────────────────┐
│ Frontend Validation                  │
│ - Text: not empty                    │
│ - File: correct type                 │
│ - File: size ≤ 5MB                   │
└──────┬───────────────────────────────┘
       ↓
┌──────────────────────────────────────┐
│ POST /api/resume/submit-*            │
│ Headers:                             │
│ - Authorization: Bearer {token}      │
│ - Content-Type: application/json or  │
│   multipart/form-data                │
└──────┬───────────────────────────────┘
       ↓
┌──────────────────────────────────────┐
│ Backend Processing                   │
│ 1. Validate JWT token                │
│ 2. Validate candidate exists         │
│ 3. Validate input                    │
│ 4. Extract text                      │
│    - Text: use as-is                 │
│    - PDF: PyMuPDF → pdfplumber       │
│    - Image: Pytesseract OCR          │
│ 5. Parse resume                      │
│    - Extract skills                  │
│    - Extract education               │
│    - Extract experience              │
│    - Extract contact info            │
│ 6. Generate blind text               │
│ 7. Upsert resume record              │
└──────┬───────────────────────────────┘
       ↓
┌──────────────────────────────────────┐
│ Response 200 OK                      │
│ {                                    │
│   "success": true,                   │
│   "resume_id": "uuid",               │
│   "message": "...",                  │
│   "skills_found": [...],             │
│   "skills_count": 5                  │
│ }                                    │
└──────┬───────────────────────────────┘
       ↓
┌──────────────────────────────────────┐
│ Frontend Display                     │
│ Show success message                 │
│ Clear form                           │
│ Update resume status                 │
└──────────────────────────────────────┘
```

---

## Authentication Flow

```
┌─────────────────────────────────────────────────────────────┐
│ SIGNUP/LOGIN                                                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Frontend                Backend                Database    │
│  ────────                ───────                ────────    │
│                                                             │
│  User Input                                                 │
│      ↓                                                      │
│  Validate                                                   │
│      ↓                                                      │
│  POST /api/auth/register or /api/auth/login                │
│      ├─────────────────────→ Validate input                │
│      │                           ↓                         │
│      │                       Check duplicate               │
│      │                           ↓                         │
│      │                       Hash password                 │
│      │                           ↓                         │
│      │                       Create User ──→ INSERT users  │
│      │                           ↓                         │
│      │                       Generate token                │
│      │                           ↓                         │
│      │                       Create Session ──→ INSERT sessions
│      │                           ↓                         │
│      ←─────────────────────── Return token                 │
│      ↓                                                      │
│  Store in localStorage                                      │
│  - token                                                    │
│  - user_id                                                  │
│  - name                                                     │
│  - email                                                    │
│  - role                                                     │
│      ↓                                                      │
│  Update state                                               │
│      ↓                                                      │
│  Redirect to Dashboard                                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────┐
│ AUTHENTICATED REQUEST (with JWT)                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Frontend                Backend                Database    │
│  ────────                ───────                ────────    │
│                                                             │
│  Get token from localStorage                                │
│      ↓                                                      │
│  Add to header:                                             │
│  Authorization: Bearer {token}                              │
│      ↓                                                      │
│  POST /api/resume/submit-text                              │
│      ├─────────────────────→ Extract token from header      │
│      │                           ↓                         │
│      │                       Query sessions ──→ SELECT     │
│      │                           ↓                         │
│      │                       Validate token                │
│      │                           ↓                         │
│      │                       Check expiration              │
│      │                           ↓                         │
│      │                       Get user from token           │
│      │                           ↓                         │
│      │                       Process request               │
│      │                           ↓                         │
│      ←─────────────────────── Return response              │
│      ↓                                                      │
│  Handle response                                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## File Organization

```
Frontend Structure:
src/
├── api/
│   ├── auth.js                    # Auth API calls
│   └── resumeApi.js               # Resume API calls
├── components/
│   ├── Dashboard.jsx              # Main dashboard
│   ├── ResumeSubmission.jsx        # Candidate upload
│   ├── ResumesPanel.jsx            # Recruiter view
│   └── ...
├── hooks/
│   └── useAuth.js                 # Auth state management
├── pages/
│   ├── LoginPage.jsx              # Login page
│   └── RegisterPage.jsx            # Signup page
├── App.jsx                        # Main app
└── main.jsx                       # Entry point

Backend Structure:
├── utils/
│   └── resume_extractor.py        # Text/PDF/image extraction
├── routers/
│   ├── resume_upload.py           # Resume endpoints
│   ├── silence_rank.py            # Silence rank agent
│   └── emotion_blind.py           # Emotion blind agent
├── agents/
│   ├── counterfactual_agent.py    # Bias detection
│   └── skill_graph_agent.py       # Skill matching
├── main.py                        # FastAPI app
├── models.py                      # SQLAlchemy models
├── database.py                    # Database config
└── requirements.txt               # Dependencies
```

---

## Environment Variables

### Frontend (.env)
```
VITE_API_URL=http://localhost:8000
```

### Backend (.env)
```
DATABASE_URL=postgresql://user:password@host:port/database
GROQ_API_KEY=your-groq-key
```

---

## Testing Checklist

- [ ] Signup as candidate
- [ ] Signup as recruiter
- [ ] Login with correct credentials
- [ ] Login with incorrect credentials (should fail)
- [ ] Upload resume as text
- [ ] Upload resume as PDF
- [ ] Upload resume as image
- [ ] View resume as recruiter
- [ ] Cannot view all resumes as candidate (403)
- [ ] Logout
- [ ] Token persists on page refresh
- [ ] Token cleared on logout
- [ ] File size validation (>5MB rejected)
- [ ] File type validation (wrong type rejected)

---

## Performance Tips

1. **Frontend**
   - Use React.memo for expensive components
   - Lazy load components with React.lazy
   - Optimize images
   - Minimize bundle size

2. **Backend**
   - Use database indexes on frequently queried columns
   - Implement caching for parsed resumes
   - Use connection pooling
   - Optimize spaCy model loading

3. **Database**
   - Index on candidate_id, user_id
   - Partition large tables
   - Regular backups
   - Monitor query performance

---

## Security Checklist

- [x] Passwords hashed with bcrypt
- [x] JWT tokens are UUIDs
- [x] CORS configured for specific origins
- [x] Role-based access control
- [x] Input validation on all endpoints
- [x] File type validation
- [x] File size validation
- [x] SQL injection prevention (SQLAlchemy ORM)
- [x] XSS prevention (React escaping)
- [ ] HTTPS in production
- [ ] Rate limiting
- [ ] CSRF protection
- [ ] Security headers

---

## Useful Links

- **Frontend:** http://localhost:5173
- **Backend:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **API Redoc:** http://localhost:8000/redoc
- **PostgreSQL:** postgresql://user:password@host:port/database

---

## Common Issues Quick Fix

| Issue | Solution |
|-------|----------|
| CORS Error | Check CORS config in main.py |
| 401 Unauthorized | Check token in localStorage |
| 403 Forbidden | Check user role |
| Database Error | Check DATABASE_URL in .env |
| PDF Extraction Error | Install pymupdf: `pip install pymupdf` |
| Image OCR Error | Install tesseract (see troubleshooting) |
| Spacy Model Error | Run: `python -m spacy download en_core_web_sm` |

---

## Next Steps

1. ✅ Setup backend and frontend
2. ✅ Test signup/login flow
3. ✅ Test resume upload
4. ✅ Test resume viewing
5. ⏳ Deploy to production
6. ⏳ Add monitoring
7. ⏳ Add additional features

---

**Last Updated:** January 2024
**Status:** Ready for Testing

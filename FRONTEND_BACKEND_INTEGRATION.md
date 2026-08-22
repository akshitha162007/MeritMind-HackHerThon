# Merit Mind - Frontend & Backend Integration Guide

## System Architecture

```
Frontend (React + Vite)          Backend (FastAPI)           Database (PostgreSQL)
Port: 5173                       Port: 8000                  Supabase
├── Auth Pages                   ├── Auth Endpoints          ├── users
├── Dashboard                    ├── Resume Upload           ├── candidates
├── Resume Upload                ├── Resume Viewing          ├── resumes
└── Resume Viewing               └── Fairness Agents         └── applications
```

## Environment Setup

### Frontend (.env)
```
VITE_API_URL=http://localhost:8000
```

### Backend (.env)
```
DATABASE_URL=postgresql://[user]:[password]@[host]:[port]/[database]
GROQ_API_KEY=[your-groq-key]
```

---

## Complete Workflow

### 1. SIGNUP FLOW

**Frontend: RegisterPage.jsx**
```
User fills form (name, email, password, role)
    ↓
Validates password (min 8 chars)
    ↓
Calls registerUser() from api/auth.js
    ↓
POST /api/auth/register
```

**Backend: main.py**
```
Receives RegisterRequest
    ↓
Validates input (name, email, password length)
    ↓
Checks if email already exists
    ↓
Hashes password with bcrypt
    ↓
Creates User record
    ↓
If role == "candidate": Creates Candidate record
    ↓
Generates UUID token
    ↓
Creates UserSession record
    ↓
Returns AuthResponse (token, user_id, name, email, role)
```

**Frontend: useAuth.js**
```
Receives AuthResponse
    ↓
Stores in localStorage:
  - token
  - user_id
  - name
  - email
  - role
    ↓
Updates user state
    ↓
Redirects to Dashboard
```

---

### 2. LOGIN FLOW

**Frontend: LoginPage.jsx**
```
User enters email & password
    ↓
Calls loginUser() from api/auth.js
    ↓
POST /api/auth/login
```

**Backend: main.py**
```
Receives LoginRequest
    ↓
Finds User by email (case-insensitive)
    ↓
Verifies password with bcrypt
    ↓
If invalid: Returns 401 "Invalid email or password"
    ↓
Generates UUID token
    ↓
Creates UserSession record
    ↓
Returns AuthResponse
```

**Frontend: useAuth.js**
```
Same as signup flow
```

---

### 3. CANDIDATE RESUME UPLOAD FLOW

**Frontend: ResumeSubmission.jsx**
```
Candidate selects upload method (text/PDF/image)
    ↓
Fills form with resume content
    ↓
Clicks submit button
    ↓
Calls appropriate API function:
  - submitResumeText()
  - submitResumePdf()
  - submitResumeImage()
```

**Frontend: api/resumeApi.js**
```
Prepares request:
  - candidate_id from localStorage
  - JWT token from localStorage
  - Content (text/file)
    ↓
POST /api/resume/submit-text (JSON)
POST /api/resume/submit-pdf (FormData)
POST /api/resume/submit-image (FormData)
```

**Backend: routers/resume_upload.py**
```
Receives request with JWT token
    ↓
Validates candidate exists
    ↓
Validates input (text not empty, file type, file size ≤ 5MB)
    ↓
Extracts text from content:
  - Text: Use as-is
  - PDF: PyMuPDF → pdfplumber fallback
  - Image: Pytesseract OCR
    ↓
Parses resume:
  - Extract skills (50+ tech skills list)
  - Extract education (keywords + spacy NER)
  - Extract experience (spacy ORG entities)
  - Extract email/phone (regex)
    ↓
Generates blind_text (anonymize PERSON/ORG/GPE/FAC)
    ↓
Checks if resume exists for candidate
    ↓
If exists: UPDATE resume record
If not: INSERT new resume record
    ↓
Returns success response with skills_found
```

**Frontend: ResumeSubmission.jsx**
```
Receives response
    ↓
Shows success message:
  "Resume submitted successfully. Your recruiter will review your application."
    ↓
Clears form
    ↓
Updates existing resume flag
```

---

### 4. RECRUITER RESUME VIEWING FLOW

**Frontend: Dashboard.jsx**
```
Recruiter clicks "Resumes" tab
    ↓
Renders ResumesPanel component
```

**Frontend: ResumesPanel.jsx**
```
On mount: Calls getAllResumes()
    ↓
GET /api/resume/all with JWT token
```

**Backend: routers/resume_upload.py**
```
Receives request with JWT token
    ↓
Validates user role == "recruiter" or "admin"
    ↓
If candidate: Returns 403 "Access denied"
    ↓
Queries all resumes joined with candidates
    ↓
For each resume:
  - Extract candidate info
  - Extract parsed_json (skills, education, experience)
  - Generate preview (first 200 chars of raw_text)
    ↓
Returns array of resume summaries
```

**Frontend: ResumesPanel.jsx**
```
Receives resume list
    ↓
Renders table with columns:
  - Candidate name
  - Skills count
  - Education count
  - Experience count
  - Submitted date
  - "View" button
```

**Frontend: ResumesPanel.jsx (Detail View)**
```
Recruiter clicks "View" button
    ↓
Calls getResumeDetail(resume_id)
    ↓
GET /api/resume/detail/{resume_id} with JWT token
```

**Backend: routers/resume_upload.py**
```
Receives request with JWT token
    ↓
Validates user role == "recruiter" or "admin"
    ↓
Queries resume by id
    ↓
Returns full resume data:
  - raw_text (full resume)
  - blind_text (anonymized)
  - parsed_json (structured data)
  - candidate info
```

**Frontend: ResumesPanel.jsx**
```
Receives full resume data
    ↓
Renders modal with:
  - Candidate name & blind ID
  - Skills as badges
  - Education list
  - Experience list
  - Full resume text (scrollable)
```

---

## API Endpoints Reference

### Authentication

| Method | Endpoint | Auth | Request | Response |
|--------|----------|------|---------|----------|
| POST | /api/auth/register | No | {name, email, password, role} | {token, user_id, name, email, role} |
| POST | /api/auth/login | No | {email, password} | {token, user_id, name, email, role} |
| POST | /api/auth/logout | Bearer | {token} | {ok: true} |

### Resume Upload

| Method | Endpoint | Auth | Request | Response |
|--------|----------|------|---------|----------|
| POST | /api/resume/submit-text | Bearer | {candidate_id, text} | {success, resume_id, message, skills_found, skills_count} |
| POST | /api/resume/submit-pdf | Bearer | FormData(candidate_id, file) | {success, resume_id, message, skills_found, skills_count} |
| POST | /api/resume/submit-image | Bearer | FormData(candidate_id, file) | {success, resume_id, message, skills_found, skills_count} |
| GET | /api/resume/candidate/{id} | Bearer | - | {has_resume, resume_id, submitted_at, skills_count} |
| GET | /api/resume/all | Bearer (Recruiter) | - | [{resume_id, candidate_id, candidate_name, skills, education, experience, submitted_at}] |
| GET | /api/resume/detail/{id} | Bearer (Recruiter) | - | {resume_id, candidate_id, candidate_name, raw_text, blind_text, parsed_json, submitted_at} |

---

## Error Handling

### HTTP Status Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | Success | Resume uploaded successfully |
| 400 | Bad request | Empty text, wrong file type, file too large |
| 401 | Unauthorized | Missing/invalid JWT token |
| 403 | Forbidden | Candidate accessing recruiter endpoint |
| 404 | Not found | Candidate/resume doesn't exist |
| 409 | Conflict | Email already registered |
| 413 | Payload too large | File > 5MB |
| 500 | Server error | Extraction failed |

### Frontend Error Handling

```javascript
try {
  const data = await submitResumeText(candidate_id, text);
  // Success
} catch (err) {
  const status = err.response?.status;
  const message = err.response?.data?.error || err.response?.data?.detail;
  
  if (status === 400) {
    // Validation error - show field-level message
  } else if (status === 401) {
    // Redirect to login
  } else if (status === 403) {
    // Access denied
  } else if (status === 413) {
    // File too large
  } else if (status === 500) {
    // Server error
  }
}
```

---

## Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND (React)                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  LoginPage/RegisterPage                                         │
│         ↓                                                       │
│  useAuth Hook (manages user state & localStorage)              │
│         ↓                                                       │
│  Dashboard (routes based on user.role)                         │
│    ├─ Candidate: ResumeSubmission component                    │
│    └─ Recruiter: ResumesPanel component                        │
│         ↓                                                       │
│  API Clients (api/auth.js, api/resumeApi.js)                   │
│         ↓                                                       │
│  Axios HTTP Requests (with JWT token in header)                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              ↓ HTTP
┌─────────────────────────────────────────────────────────────────┐
│                      BACKEND (FastAPI)                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  main.py (Auth endpoints)                                       │
│    ├─ POST /api/auth/register                                  │
│    ├─ POST /api/auth/login                                     │
│    └─ POST /api/auth/logout                                    │
│         ↓                                                       │
│  routers/resume_upload.py (Resume endpoints)                   │
│    ├─ POST /api/resume/submit-text                             │
│    ├─ POST /api/resume/submit-pdf                              │
│    ├─ POST /api/resume/submit-image                            │
│    ├─ GET /api/resume/candidate/{id}                           │
│    ├─ GET /api/resume/all (recruiter only)                     │
│    └─ GET /api/resume/detail/{id} (recruiter only)             │
│         ↓                                                       │
│  utils/resume_extractor.py (Text extraction & parsing)         │
│    ├─ extract_from_text()                                      │
│    ├─ extract_from_pdf()                                       │
│    ├─ extract_from_image()                                     │
│    ├─ parse_resume()                                           │
│    └─ blind_screen()                                           │
│         ↓                                                       │
│  models.py (SQLAlchemy ORM)                                    │
│    ├─ User                                                     │
│    ├─ UserSession                                              │
│    ├─ Candidate                                                │
│    └─ Resume                                                   │
│         ↓                                                       │
│  database.py (SQLAlchemy engine)                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              ↓ SQL
┌─────────────────────────────────────────────────────────────────┐
│                   DATABASE (PostgreSQL)                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  users table                                                    │
│  ├─ id (UUID)                                                  │
│  ├─ name (VARCHAR)                                             │
│  ├─ email (VARCHAR, unique)                                    │
│  ├─ password_hash (VARCHAR)                                    │
│  ├─ role (VARCHAR: recruiter/candidate)                        │
│  └─ created_at (DATETIME)                                      │
│                                                                 │
│  sessions table                                                │
│  ├─ id (UUID)                                                  │
│  ├─ user_id (UUID, FK)                                         │
│  ├─ token (VARCHAR, unique)                                    │
│  ├─ expires_at (DATETIME)                                      │
│  └─ created_at (DATETIME)                                      │
│                                                                 │
│  candidates table                                              │
│  ├─ id (UUID)                                                  │
│  ├─ user_id (UUID)                                             │
│  ├─ name (VARCHAR)                                             │
│  ├─ email (VARCHAR)                                            │
│  ├─ blind_id (UUID)                                            │
│  └─ created_at (DATETIME)                                      │
│                                                                 │
│  resumes table                                                 │
│  ├─ id (UUID)                                                  │
│  ├─ candidate_id (UUID, FK)                                    │
│  ├─ raw_text (TEXT)                                            │
│  ├─ parsed_json (JSON)                                         │
│  ├─ blind_text (TEXT)                                          │
│  ├─ skill_graph_json (JSON)                                    │
│  └─ created_at (DATETIME)                                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Testing the Integration

### 1. Start Backend
```bash
cd backend
python -m uvicorn main:app --reload --port 8000
```

### 2. Start Frontend
```bash
cd frontend
npm run dev
```

### 3. Test Signup
1. Go to http://localhost:5173/register
2. Fill form (name, email, password, role)
3. Click "Create Account"
4. Should redirect to dashboard

### 4. Test Login
1. Go to http://localhost:5173/login
2. Enter credentials
3. Click "Sign In"
4. Should redirect to dashboard

### 5. Test Resume Upload (Candidate)
1. Log in as candidate
2. Go to Dashboard
3. Scroll to "Submit Your Resume"
4. Upload resume (text/PDF/image)
5. Should see success message

### 6. Test Resume Viewing (Recruiter)
1. Log in as recruiter
2. Go to Dashboard
3. Click "Resumes" tab
4. Should see table of all resumes
5. Click "View" to see details

---

## Troubleshooting

### Issue: CORS Error
**Solution:** Check CORS configuration in backend/main.py
```python
allow_origins=[
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:5175",
    ...
]
```

### Issue: 401 Unauthorized
**Solution:** Check JWT token in localStorage
```javascript
console.log(localStorage.getItem('token'));
```

### Issue: 403 Forbidden
**Solution:** Check user role
```javascript
console.log(localStorage.getItem('role'));
```

### Issue: Database Connection Error
**Solution:** Check DATABASE_URL in backend/.env
```
DATABASE_URL=postgresql://user:password@host:port/database
```

### Issue: Resume Extraction Fails
**Solution:** Install required packages
```bash
pip install pymupdf pdfplumber pillow pytesseract spacy
python -m spacy download en_core_web_sm
```

---

## Security Best Practices

1. **JWT Token Storage**
   - Stored in localStorage (accessible to XSS)
   - Consider moving to httpOnly cookies in production

2. **Password Hashing**
   - Uses bcrypt with salt
   - Never store plain passwords

3. **CORS Configuration**
   - Whitelist specific origins
   - Don't use "*" in production

4. **Role-Based Access Control**
   - Recruiters can only access recruiter endpoints
   - Candidates can only access candidate endpoints

5. **Input Validation**
   - All inputs validated on backend
   - File type and size checked
   - Email format validated

---

## Performance Optimization

1. **Resume Extraction**
   - Async file upload
   - Lazy loading of spacy model
   - Caching of parsed resumes

2. **Database Queries**
   - Indexed on candidate_id, user_id
   - Pagination for large result sets
   - Connection pooling

3. **Frontend**
   - Code splitting
   - Lazy loading of components
   - Memoization of expensive computations

---

## Deployment Checklist

- [ ] Set VITE_API_URL to production backend URL
- [ ] Set DATABASE_URL to production database
- [ ] Enable HTTPS
- [ ] Configure CORS for production domain
- [ ] Set secure JWT expiration
- [ ] Enable rate limiting
- [ ] Set up monitoring/logging
- [ ] Configure backup strategy
- [ ] Test all workflows end-to-end

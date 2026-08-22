# Merit Mind - Complete Workflow & Integration Checklist

## 1. AUTHENTICATION WORKFLOW

### Signup Flow Diagram
```
┌─────────────────────────────────────────────────────────────────┐
│ FRONTEND: RegisterPage.jsx                                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  User Input:                                                    │
│  ├─ name: "John Doe"                                            │
│  ├─ email: "john@example.com"                                   │
│  ├─ password: "password123"                                     │
│  └─ role: "candidate"                                           │
│                                                                 │
│  Validation:                                                    │
│  ├─ name: required, non-empty                                   │
│  ├─ email: required, valid format                               │
│  ├─ password: required, min 8 characters                        │
│  └─ role: required, "recruiter" or "candidate"                  │
│                                                                 │
│  API Call:                                                      │
│  └─ registerUser({name, email, password, role})                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              ↓ HTTP POST
┌─────────────────────────────────────────────────────────────────┐
│ BACKEND: main.py - POST /api/auth/register                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. Normalize Input:                                            │
│     ├─ name = name.strip()                                      │
│     ├─ email = email.strip().lower()                            │
│     └─ password = password (as-is)                              │
│                                                                 │
│  2. Validate Input:                                             │
│     ├─ name: required, non-empty                                │
│     ├─ email: required, non-empty                               │
│     ├─ password: required, min 8 chars                          │
│     └─ role: must be "recruiter" or "candidate"                 │
│                                                                 │
│  3. Check Duplicate:                                            │
│     └─ Query: SELECT * FROM users WHERE email = ?               │
│        If exists: Return 409 "Email already registered"         │
│                                                                 │
│  4. Hash Password:                                              │
│     └─ password_hash = bcrypt.hashpw(password, salt)            │
│                                                                 │
│  5. Create User:                                                │
│     └─ INSERT INTO users (id, name, email, password_hash, role) │
│        VALUES (uuid4(), name, email, password_hash, role)       │
│                                                                 │
│  6. Create Candidate (if role == "candidate"):                  │
│     └─ INSERT INTO candidates (id, name, email, blind_id)       │
│        VALUES (user.id, name, email, uuid4())                   │
│                                                                 │
│  7. Generate Session:                                           │
│     ├─ token = uuid4()                                          │
│     ├─ expires_at = now() + 7 days                              │
│     └─ INSERT INTO sessions (id, user_id, token, expires_at)    │
│                                                                 │
│  8. Return Response:                                            │
│     └─ {                                                        │
│          "token": "uuid-token",                                 │
│          "user_id": "uuid-user-id",                             │
│          "name": "John Doe",                                    │
│          "email": "john@example.com",                           │
│          "role": "candidate"                                    │
│        }                                                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              ↓ HTTP 200
┌─────────────────────────────────────────────────────────────────┐
│ FRONTEND: useAuth.js - register()                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. Store in localStorage:                                      │
│     ├─ localStorage.setItem('token', data.token)                │
│     ├─ localStorage.setItem('user_id', data.user_id)            │
│     ├─ localStorage.setItem('name', data.name)                  │
│     ├─ localStorage.setItem('email', data.email)                │
│     └─ localStorage.setItem('role', data.role)                  │
│                                                                 │
│  2. Update State:                                               │
│     └─ setUser(data)                                            │
│                                                                 │
│  3. Redirect:                                                   │
│     └─ navigate('/')  // Goes to Dashboard                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ FRONTEND: App.jsx - Conditional Rendering                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  if (user) {                                                    │
│    return <Dashboard user={user} onLogout={logout} />           │
│  } else {                                                       │
│    return <Routes> ... </Routes>  // Landing page               │
│  }                                                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Login Flow Diagram
```
┌─────────────────────────────────────────────────────────────────┐
│ FRONTEND: LoginPage.jsx                                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  User Input:                                                    │
│  ├─ email: "john@example.com"                                   │
│  └─ password: "password123"                                     │
│                                                                 │
│  API Call:                                                      │
│  └─ loginUser({email, password})                                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              ↓ HTTP POST
┌─────────────────────────────────────────────────────────────────┐
│ BACKEND: main.py - POST /api/auth/login                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. Normalize Email:                                            │
│     └─ email = email.strip().lower()                            │
│                                                                 │
│  2. Find User:                                                  │
│     └─ Query: SELECT * FROM users WHERE email = ?               │
│        If not found: Return 401 "Invalid email or password"     │
│                                                                 │
│  3. Verify Password:                                            │
│     └─ bcrypt.checkpw(password, user.password_hash)             │
│        If false: Return 401 "Invalid email or password"         │
│                                                                 │
│  4. Generate Session:                                           │
│     ├─ token = uuid4()                                          │
│     ├─ expires_at = now() + 7 days                              │
│     └─ INSERT INTO sessions (id, user_id, token, expires_at)    │
│                                                                 │
│  5. Return Response:                                            │
│     └─ {                                                        │
│          "token": "uuid-token",                                 │
│          "user_id": "uuid-user-id",                             │
│          "name": "John Doe",                                    │
│          "email": "john@example.com",                           │
│          "role": "candidate"                                    │
│        }                                                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              ↓ HTTP 200
┌─────────────────────────────────────────────────────────────────┐
│ FRONTEND: useAuth.js - login()                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Same as signup flow (store in localStorage, update state)      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. RESUME UPLOAD WORKFLOW

### Candidate Upload Flow
```
┌─────────────────────────────────────────────────────────────────┐
│ FRONTEND: ResumeSubmission.jsx                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  User Action:                                                   │
│  ├─ Select upload method (text/PDF/image)                       │
│  ├─ Provide content                                             │
│  └─ Click submit button                                         │
│                                                                 │
│  Validation:                                                    │
│  ├─ Text: not empty                                             │
│  ├─ File: correct type (PDF/JPG/PNG)                            │
│  └─ File: size ≤ 5MB                                            │
│                                                                 │
│  API Call:                                                      │
│  ├─ submitResumeText(candidate_id, text)                        │
│  ├─ submitResumePdf(candidate_id, file)                         │
│  └─ submitResumeImage(candidate_id, file)                       │
│                                                                 │
│  Headers:                                                       │
│  └─ Authorization: Bearer {token}                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              ↓ HTTP POST
┌─────────────────────────────────────────────────────────────────┐
│ BACKEND: routers/resume_upload.py                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. Validate JWT Token:                                         │
│     ├─ Extract token from Authorization header                  │
│     ├─ Query: SELECT * FROM sessions WHERE token = ?            │
│     ├─ Check: expires_at > now()                                │
│     └─ If invalid: Return 401 "Invalid token"                   │
│                                                                 │
│  2. Validate Candidate:                                         │
│     ├─ Query: SELECT * FROM candidates WHERE id = ?             │
│     └─ If not found: Return 404 "Candidate not found"           │
│                                                                 │
│  3. Validate Input:                                             │
│     ├─ Text: not empty                                          │
│     ├─ File: correct content_type                               │
│     └─ File: size ≤ 5MB                                         │
│                                                                 │
│  4. Extract Text:                                               │
│     ├─ Text: use as-is                                          │
│     ├─ PDF: PyMuPDF → pdfplumber fallback                       │
│     └─ Image: Pytesseract OCR                                   │
│                                                                 │
│  5. Parse Resume:                                               │
│     ├─ extract_from_text/pdf/image()                            │
│     ├─ parse_resume(text)                                       │
│     │  ├─ Extract skills (50+ tech skills)                      │
│     │  ├─ Extract education (keywords + spacy NER)              │
│     │  ├─ Extract experience (spacy ORG entities)               │
│     │  ├─ Extract email (regex)                                 │
│     │  └─ Extract phone (regex)                                 │
│     └─ blind_screen(text)                                       │
│        └─ Replace PERSON/ORG/GPE/FAC with [NAME]/[COMPANY]/etc  │
│                                                                 │
│  6. Upsert Resume:                                              │
│     ├─ Query: SELECT * FROM resumes WHERE candidate_id = ?      │
│     ├─ If exists:                                               │
│     │  └─ UPDATE resumes SET raw_text, parsed_json, blind_text  │
│     └─ If not exists:                                           │
│        └─ INSERT INTO resumes (id, candidate_id, ...)           │
│                                                                 │
│  7. Return Response:                                            │
│     └─ {                                                        │
│          "success": true,                                       │
│          "resume_id": "uuid",                                   │
│          "message": "Resume submitted successfully",            │
│          "skills_found": ["Python", "React", ...],              │
│          "skills_count": 5                                      │
│        }                                                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              ↓ HTTP 200
┌─────────────────────────────────────────────────────────────────┐
│ FRONTEND: ResumeSubmission.jsx                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. Show Success Message:                                       │
│     └─ "Resume submitted successfully. Your recruiter will      │
│        review your application."                                │
│                                                                 │
│  2. Clear Form:                                                 │
│     ├─ setTextInput('')                                         │
│     ├─ setSelectedFile(null)                                    │
│     └─ setImagePreview(null)                                    │
│                                                                 │
│  3. Update State:                                               │
│     └─ checkExistingResume()  // Refresh resume status          │
│                                                                 │
│  4. Auto-hide Message:                                          │
│     └─ setTimeout(() => setSuccess(false), 5000)                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. RECRUITER RESUME VIEWING WORKFLOW

### View All Resumes
```
┌─────────────────────────────────────────────────────────────────┐
│ FRONTEND: ResumesPanel.jsx                                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  On Mount:                                                      │
│  └─ fetchResumes()                                              │
│     └─ getAllResumes()                                          │
│                                                                 │
│  Headers:                                                       │
│  └─ Authorization: Bearer {token}                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              ↓ HTTP GET
┌─────────────────────────────────────────────────────────────────┐
│ BACKEND: routers/resume_upload.py - GET /api/resume/all         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. Validate JWT Token:                                         │
│     └─ (same as upload flow)                                    │
│                                                                 │
│  2. Check Role:                                                 │
│     ├─ If role != "recruiter" and role != "admin":              │
│     └─ Return 403 "Access denied"                               │
│                                                                 │
│  3. Query All Resumes:                                          │
│     └─ SELECT r.*, c.* FROM resumes r                           │
│        JOIN candidates c ON r.candidate_id = c.id               │
│        ORDER BY r.created_at DESC                               │
│                                                                 │
│  4. Build Response:                                             │
│     └─ For each resume:                                         │
│        ├─ resume_id                                             │
│        ├─ candidate_id                                          │
│        ├─ candidate_name                                        │
│        ├─ candidate_blind_id                                    │
│        ├─ skills: parsed_json.skills                            │
│        ├─ education: parsed_json.education                      │
│        ├─ experience: parsed_json.experience                    │
│        ├─ raw_text_preview: raw_text[:200]                      │
│        └─ submitted_at                                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              ↓ HTTP 200
┌─────────────────────────────────────────────────────────────────┐
│ FRONTEND: ResumesPanel.jsx                                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. Render Table:                                               │
│     ├─ Candidate name                                           │
│     ├─ Skills count                                             │
│     ├─ Education count                                          │
│     ├─ Experience count                                         │
│     ├─ Submitted date                                           │
│     └─ "View" button                                            │
│                                                                 │
│  2. Handle View Click:                                          │
│     └─ getResumeDetail(resume_id)                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### View Resume Details
```
┌─────────────────────────────────────────────────────────────────┐
│ FRONTEND: ResumesPanel.jsx (Detail Modal)                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  User Action:                                                   │
│  └─ Click "View" button on resume row                           │
│                                                                 │
│  API Call:                                                      │
│  └─ getResumeDetail(resume_id)                                  │
│                                                                 │
│  Headers:                                                       │
│  └─ Authorization: Bearer {token}                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              ↓ HTTP GET
┌─────────────────────────────────────────────────────────────────┐
│ BACKEND: routers/resume_upload.py - GET /api/resume/detail/{id} │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. Validate JWT Token:                                         │
│     └─ (same as upload flow)                                    │
│                                                                 │
│  2. Check Role:                                                 │
│     ├─ If role != "recruiter" and role != "admin":              │
│     └─ Return 403 "Access denied"                               │
│                                                                 │
│  3. Query Resume:                                               │
│     └─ SELECT * FROM resumes WHERE id = ?                       │
│        If not found: Return 404 "Resume not found"              │
│                                                                 │
│  4. Query Candidate:                                            │
│     └─ SELECT * FROM candidates WHERE id = resume.candidate_id  │
│                                                                 │
│  5. Return Full Data:                                           │
│     └─ {                                                        │
│          "resume_id": "uuid",                                   │
│          "candidate_id": "uuid",                                │
│          "candidate_name": "John Doe",                          │
│          "candidate_blind_id": "uuid",                          │
│          "raw_text": "full resume text",                        │
│          "blind_text": "anonymized text",                       │
│          "parsed_json": {                                       │
│            "skills": [...],                                     │
│            "education": [...],                                  │
│            "experience": [...],                                 │
│            "contact": {...}                                     │
│          },                                                     │
│          "submitted_at": "2024-01-15T10:30:00"                  │
│        }                                                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              ↓ HTTP 200
┌─────────────────────────────────────────────────────────────────┐
│ FRONTEND: ResumesPanel.jsx (Detail Modal)                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. Render Modal:                                               │
│     ├─ Candidate name & blind ID                                │
│     ├─ Skills as badges                                         │
│     ├─ Education list                                           │
│     ├─ Experience list                                          │
│     ├─ Full resume text (scrollable)                            │
│     └─ "Back to Resumes" button                                 │
│                                                                 │
│  2. Handle Back Click:                                          │
│     └─ setSelectedResume(null)  // Close modal                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 4. INTEGRATION CHECKLIST

### Backend Setup
- [x] FastAPI application configured
- [x] CORS middleware configured for localhost:5173
- [x] PostgreSQL database connected
- [x] SQLAlchemy ORM models defined
- [x] Auth endpoints implemented (/api/auth/register, /api/auth/login, /api/auth/logout)
- [x] Resume upload endpoints implemented
- [x] Resume viewing endpoints implemented
- [x] JWT token validation implemented
- [x] Role-based access control implemented
- [x] Error handling with proper HTTP status codes
- [x] Resume extraction utilities implemented
- [x] Database migrations (if needed)

### Frontend Setup
- [x] React application configured
- [x] Vite build tool configured
- [x] VITE_API_URL environment variable set
- [x] Axios HTTP client configured
- [x] useAuth hook implemented
- [x] LoginPage component implemented
- [x] RegisterPage component implemented
- [x] Dashboard component implemented
- [x] ResumeSubmission component implemented
- [x] ResumesPanel component implemented
- [x] API client functions implemented
- [x] Error handling implemented
- [x] Loading states implemented
- [x] localStorage for token storage

### Integration Testing
- [ ] Test signup flow (candidate)
- [ ] Test signup flow (recruiter)
- [ ] Test login flow
- [ ] Test logout flow
- [ ] Test resume upload (text)
- [ ] Test resume upload (PDF)
- [ ] Test resume upload (image)
- [ ] Test resume viewing (recruiter)
- [ ] Test access control (candidate cannot view all resumes)
- [ ] Test error handling (invalid credentials)
- [ ] Test error handling (file too large)
- [ ] Test error handling (wrong file type)
- [ ] Test token expiration
- [ ] Test database persistence

### Deployment Checklist
- [ ] Set production VITE_API_URL
- [ ] Set production DATABASE_URL
- [ ] Enable HTTPS
- [ ] Configure CORS for production domain
- [ ] Set secure JWT expiration
- [ ] Enable rate limiting
- [ ] Set up monitoring/logging
- [ ] Configure backup strategy
- [ ] Test all workflows end-to-end
- [ ] Set up CI/CD pipeline

---

## 5. ENVIRONMENT VARIABLES

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

## 6. RUNNING THE APPLICATION

### Terminal 1: Backend
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python -m uvicorn main:app --reload --port 8000
```

### Terminal 2: Frontend
```bash
cd frontend
npm run dev
```

### Access Points
- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## 7. TROUBLESHOOTING

### CORS Error
```
Access to XMLHttpRequest at 'http://localhost:8000/api/auth/login' 
from origin 'http://localhost:5173' has been blocked by CORS policy
```
**Solution:** Check CORS configuration in backend/main.py

### 401 Unauthorized
```
{"detail": "Invalid or expired token"}
```
**Solution:** 
- Check token in localStorage
- Log in again
- Check token expiration

### 403 Forbidden
```
{"detail": "Access denied"}
```
**Solution:**
- Check user role
- Candidate cannot access recruiter endpoints

### Database Connection Error
```
sqlalchemy.exc.OperationalError: could not connect to server
```
**Solution:**
- Check DATABASE_URL in .env
- Ensure PostgreSQL is running
- Check credentials

### Resume Extraction Error
```
{"error": "Could not extract text from PDF"}
```
**Solution:**
- Install required packages: `pip install pymupdf pdfplumber`
- Check PDF is valid
- Try uploading as text instead

---

## 8. NEXT STEPS

1. **Test the complete workflow**
   - Follow the testing checklist above
   - Test all error scenarios

2. **Customize the application**
   - Update branding/colors
   - Add company logo
   - Customize email templates

3. **Add additional features**
   - Job posting
   - Application tracking
   - Fairness scoring
   - Bias detection

4. **Deploy to production**
   - Set up production database
   - Deploy backend to cloud (Heroku, Railway, etc.)
   - Deploy frontend to CDN (Vercel, Netlify, etc.)
   - Configure custom domain

5. **Monitor and maintain**
   - Set up error tracking (Sentry)
   - Set up analytics (Mixpanel)
   - Monitor performance
   - Regular backups

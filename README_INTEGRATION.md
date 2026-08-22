# Merit Mind - Agentic AI System for Bias-Free Recruitment

## Overview

Merit Mind is a full-stack application that combines AI-powered resume analysis with fairness-aware hiring practices. The system helps recruiters identify and mitigate bias in their hiring processes while providing candidates with transparent, merit-based evaluation.

### Key Features

- **Candidate Portal**
  - Resume submission (text, PDF, image)
  - Application tracking
  - Fairness score transparency

- **Recruiter Portal**
  - Resume management and viewing
  - Bias detection and mitigation
  - Fairness scoring
  - Candidate pipeline management

- **AI Agents**
  - Resume extraction and parsing
  - Skill matching
  - Bias detection
  - Fairness optimization

---

## Technology Stack

### Frontend
- **Framework:** React 18
- **Build Tool:** Vite
- **HTTP Client:** Axios
- **Styling:** Tailwind CSS
- **State Management:** React Hooks + localStorage

### Backend
- **Framework:** FastAPI (Python)
- **Database:** PostgreSQL (Supabase)
- **ORM:** SQLAlchemy
- **Authentication:** JWT + bcrypt
- **Text Processing:** spaCy, PyMuPDF, pdfplumber, pytesseract

### Infrastructure
- **Frontend Port:** 5173 (development)
- **Backend Port:** 8000
- **Database:** PostgreSQL (cloud-hosted)

---

## Project Structure

```
merit-mind-1/
├── backend/
│   ├── utils/
│   │   ├── __init__.py
│   │   └── resume_extractor.py          # Text/PDF/image extraction
│   ├── routers/
│   │   ├── resume_upload.py             # Resume endpoints
│   │   ├── silence_rank.py              # Silence rank agent
│   │   └── emotion_blind.py             # Emotion blind agent
│   ├── agents/
│   │   ├── counterfactual_agent.py      # Bias detection
│   │   └── skill_graph_agent.py         # Skill matching
│   ├── main.py                          # FastAPI app + auth endpoints
│   ├── models.py                        # SQLAlchemy models
│   ├── database.py                      # Database configuration
│   ├── requirements.txt                 # Python dependencies
│   └── .env                             # Environment variables
│
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   │   ├── auth.js                  # Auth API client
│   │   │   └── resumeApi.js             # Resume API client
│   │   ├── components/
│   │   │   ├── Dashboard.jsx            # Main dashboard
│   │   │   ├── ResumeSubmission.jsx     # Candidate upload
│   │   │   ├── ResumesPanel.jsx         # Recruiter view
│   │   │   └── ...                      # Other components
│   │   ├── hooks/
│   │   │   └── useAuth.js               # Auth state management
│   │   ├── pages/
│   │   │   ├── LoginPage.jsx            # Login page
│   │   │   └── RegisterPage.jsx         # Signup page
│   │   ├── App.jsx                      # Main app component
│   │   └── main.jsx                     # Entry point
│   ├── package.json                     # Node dependencies
│   ├── vite.config.js                   # Vite configuration
│   └── .env                             # Environment variables
│
├── FRONTEND_BACKEND_INTEGRATION.md      # Integration guide
├── QUICK_START.md                       # Quick start guide
├── WORKFLOW_AND_INTEGRATION_CHECKLIST.md # Detailed workflows
└── README.md                            # This file
```

---

## Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+
- PostgreSQL (or Supabase account)

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Download spacy model
python -m spacy download en_core_web_sm

# Create .env file
cat > .env << EOF
DATABASE_URL=postgresql://user:password@host:port/database
GROQ_API_KEY=your-groq-key
EOF

# Start backend
python -m uvicorn main:app --reload --port 8000
```

Backend will be available at: **http://localhost:8000**

### 2. Frontend Setup

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

Frontend will be available at: **http://localhost:5173**

---

## Complete Workflow

### 1. Signup (Candidate)

```
User → RegisterPage → POST /api/auth/register → Backend
  ↓
Backend: Hash password, create User + Candidate, generate token
  ↓
Frontend: Store token in localStorage, redirect to Dashboard
```

**Test:**
1. Go to http://localhost:5173/register
2. Fill form (name, email, password, role: "candidate")
3. Click "Create Account"
4. Should redirect to Dashboard

### 2. Login

```
User → LoginPage → POST /api/auth/login → Backend
  ↓
Backend: Verify credentials, generate token
  ↓
Frontend: Store token in localStorage, redirect to Dashboard
```

**Test:**
1. Go to http://localhost:5173/login
2. Enter credentials
3. Click "Sign In"
4. Should redirect to Dashboard

### 3. Upload Resume (Candidate)

```
Candidate → ResumeSubmission → POST /api/resume/submit-* → Backend
  ↓
Backend: Extract text, parse resume, store in database
  ↓
Frontend: Show success message
```

**Test:**
1. Log in as candidate
2. Scroll to "Submit Your Resume"
3. Upload resume (text/PDF/image)
4. Should see success message

### 4. View Resumes (Recruiter)

```
Recruiter → ResumesPanel → GET /api/resume/all → Backend
  ↓
Backend: Query all resumes, return with parsed data
  ↓
Frontend: Render table with resumes
  ↓
Recruiter → Click "View" → GET /api/resume/detail/{id} → Backend
  ↓
Backend: Return full resume data
  ↓
Frontend: Show resume details in modal
```

**Test:**
1. Log in as recruiter
2. Click "Resumes" tab
3. Should see table of all resumes
4. Click "View" to see details

---

## API Endpoints

### Authentication

| Method | Endpoint | Auth | Purpose |
|--------|----------|------|---------|
| POST | /api/auth/register | No | Create new account |
| POST | /api/auth/login | No | Login to account |
| POST | /api/auth/logout | Bearer | Logout from account |

### Resume Management

| Method | Endpoint | Auth | Purpose |
|--------|----------|------|---------|
| POST | /api/resume/submit-text | Bearer | Submit resume as text |
| POST | /api/resume/submit-pdf | Bearer | Submit resume as PDF |
| POST | /api/resume/submit-image | Bearer | Submit resume as image |
| GET | /api/resume/candidate/{id} | Bearer | Get candidate's resume status |
| GET | /api/resume/all | Bearer (Recruiter) | Get all resumes |
| GET | /api/resume/detail/{id} | Bearer (Recruiter) | Get full resume details |

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

## Error Handling

### HTTP Status Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | Success | Resume uploaded successfully |
| 400 | Bad request | Empty text, wrong file type |
| 401 | Unauthorized | Invalid credentials or token |
| 403 | Forbidden | Candidate accessing recruiter endpoint |
| 404 | Not found | Candidate or resume doesn't exist |
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
  const message = err.response?.data?.error;
  
  if (status === 400) {
    // Show validation error
  } else if (status === 401) {
    // Redirect to login
  } else if (status === 403) {
    // Show access denied
  }
}
```

---

## Authentication Flow

### JWT Token Management

1. **Token Generation (Backend)**
   - Generated on signup/login
   - Stored in `sessions` table
   - Expires after 7 days

2. **Token Storage (Frontend)**
   - Stored in `localStorage`
   - Sent in `Authorization: Bearer {token}` header
   - Cleared on logout

3. **Token Validation (Backend)**
   - Extracted from Authorization header
   - Verified against `sessions` table
   - Checked for expiration

### Security Measures

- Passwords hashed with bcrypt
- JWT tokens are UUIDs (cryptographically secure)
- CORS configured for specific origins
- Role-based access control
- Input validation on all endpoints

---

## Resume Extraction

### Supported Formats

1. **Text**
   - Plain text paste
   - Direct parsing

2. **PDF**
   - PyMuPDF (primary)
   - pdfplumber (fallback)

3. **Image**
   - JPG/PNG
   - Pytesseract OCR

### Extraction Process

```
Input (text/PDF/image)
  ↓
Extract raw text
  ↓
Parse resume:
  ├─ Extract skills (50+ tech skills)
  ├─ Extract education (keywords + spaCy NER)
  ├─ Extract experience (spaCy ORG entities)
  ├─ Extract email (regex)
  └─ Extract phone (regex)
  ↓
Generate blind text (anonymize PERSON/ORG/GPE/FAC)
  ↓
Store in database
```

### Parsed Resume Structure

```json
{
  "skills": ["Python", "React", "SQL"],
  "education": ["IIT Delhi", "B.Tech Computer Science"],
  "experience": [
    {"company": "TechCorp"},
    {"company": "StartupXYZ"}
  ],
  "contact": {
    "email": "john@example.com",
    "phone": "+1-234-567-8900"
  }
}
```

---

## Troubleshooting

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
- Check token in localStorage: `localStorage.getItem('token')`
- Log in again
- Check token expiration

### 403 Forbidden
```
{"detail": "Access denied"}
```
**Solution:**
- Check user role: `localStorage.getItem('role')`
- Candidate cannot access recruiter endpoints

### Database Connection Error
```
sqlalchemy.exc.OperationalError: could not connect to server
```
**Solution:**
- Check DATABASE_URL in .env
- Ensure PostgreSQL is running
- Verify credentials

### Resume Extraction Error
```
{"error": "Could not extract text from PDF"}
```
**Solution:**
- Install required packages: `pip install pymupdf pdfplumber`
- Check PDF is valid
- Try uploading as text instead

### pytesseract Error
```
pytesseract.TesseractNotFoundError: tesseract is not installed
```
**Solution:**
- Install Tesseract OCR:
  - Windows: https://github.com/UB-Mannheim/tesseract/wiki
  - macOS: `brew install tesseract`
  - Linux: `sudo apt-get install tesseract-ocr`

---

## Development

### Running Tests

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

### Code Quality

```bash
# Backend linting
cd backend
flake8 .
black .

# Frontend linting
cd frontend
npm run lint
```

---

## Deployment

### Frontend Deployment (Vercel)

```bash
cd frontend
npm run build
vercel deploy
```

### Backend Deployment (Railway/Heroku)

```bash
cd backend
# Set environment variables
# Deploy using platform CLI
```

### Environment Variables

**Frontend (.env.production)**
```
VITE_API_URL=https://api.yourdomain.com
```

**Backend (.env.production)**
```
DATABASE_URL=postgresql://user:password@host:port/database
GROQ_API_KEY=your-groq-key
```

---

## Documentation

- **[FRONTEND_BACKEND_INTEGRATION.md](./FRONTEND_BACKEND_INTEGRATION.md)** - Complete integration guide
- **[QUICK_START.md](./QUICK_START.md)** - Quick start guide
- **[WORKFLOW_AND_INTEGRATION_CHECKLIST.md](./WORKFLOW_AND_INTEGRATION_CHECKLIST.md)** - Detailed workflows and checklist
- **[RESUME_UPLOAD_FIX_SUMMARY.md](./RESUME_UPLOAD_FIX_SUMMARY.md)** - Resume upload feature details
- **[RESUME_UPLOAD_TESTING_GUIDE.md](./RESUME_UPLOAD_TESTING_GUIDE.md)** - Testing guide

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the documentation files
3. Check backend logs: `python -m uvicorn main:app --reload --port 8000`
4. Check browser console for frontend errors

---

## Roadmap

- [ ] Email notifications
- [ ] Advanced bias detection
- [ ] Skill graph visualization
- [ ] Interview scheduling
- [ ] Offer management
- [ ] Analytics dashboard
- [ ] Mobile app
- [ ] API documentation (Swagger)

---

## Contact

For questions or feedback, please reach out to the development team.

---

## Acknowledgments

- FastAPI for the excellent Python web framework
- React for the powerful frontend library
- PostgreSQL for reliable database
- spaCy for NLP capabilities
- All open-source contributors

---

**Last Updated:** January 2024
**Version:** 1.0.0

# Intersectional Compounded Bias Detection & Autonomous Job Rewriting Implementation

## Overview
Implemented two interconnected AI agents for Merit Mind:
1. **Intersectional Compounded Bias Detection Agent** - Detects bias across 8 identity axes simultaneously
2. **Autonomous Job Rewriting Agent** - Autonomously rewrites JDs to be more inclusive

## Backend Implementation

### 1. `/backend/agents/jd_bias_analyzer.py`
**Core bias detection and rewriting engine**

Features:
- Indian-specific bias taxonomy with 8 axes:
  - Gender, Age, Caste, College Tier, Regional Language, Socioeconomic, Matrimonial, Disability
- GPT-4 integration with fallback keyword matching
- Intersectional bias detection (compound axes)
- Autonomous rewriting with 3 variants: Conservative, Balanced, Aggressive

Key Functions:
- `analyze_jd_bias(jd_text)` - Analyzes JD for bias using GPT-4 or keyword fallback
- `generate_rewrite(jd_text, bias_report, variant)` - Generates inclusive rewrite
- Fallback functions for when OpenAI API is unavailable

### 2. `/backend/routers/bias_detection.py`
**5 REST API endpoints with role-based access control**

Endpoints:
1. `POST /api/bias/analyze/{jd_id}` - Run bias analysis (RECRUITER/ADMIN)
2. `GET /api/bias/report/{jd_id}` - Get bias report (RECRUITER sees full, CANDIDATE sees limited)
3. `POST /api/bias/rewrite/{jd_id}` - Generate rewritten JD (RECRUITER/ADMIN)
4. `GET /api/bias/jd-list` - List recruiter's JDs with bias status (RECRUITER)
5. `GET /api/bias/candidate-view/{jd_id}` - Limited bias info for candidates (CANDIDATE)

Access Control:
- Recruiters: Full access to analyze, rewrite, and view all bias data
- Candidates: Limited view - only see if JD was bias-checked, overall score, and summary
- Admin: Full access like recruiters

### 3. Database Integration
Uses existing tables:
- `job_descriptions` - Stores raw_text, inclusive_text, bias_score
- `bias_reports` - Stores individual bias flags with severity and axes
- `intersectional_bias_matrix` - Stores compound bias scores

## Frontend Implementation

### 1. `/frontend/src/api/biasApi.js`
**API client for bias detection endpoints**

Functions:
- `runBiasAnalysis(jd_id)` - Trigger analysis
- `getBiasReport(jd_id)` - Fetch report
- `rewriteJD(jd_id, variant)` - Generate rewrite
- `getJDList()` - List JDs
- `getCandidateBiasView(jd_id)` - Get candidate view

### 2. `/frontend/src/components/BiasDetectionPanel.jsx`
**Recruiter dashboard component**

Sections:
1. **JD Selection Bar** - Dropdown with status indicators (grey/red/yellow/green/blue dots)
2. **Bias Score Overview** - 4 stat cards showing overall score, total flags, intersectional flags, highest severity
3. **Bias Flags Table** - Expandable rows with trigger phrases, axes, severity badges, harmed groups
4. **Intersectional Bias Matrix** - Visual grid showing compound bias scores with color coding
5. **Rewrite Panel** - Variant selector (Conservative/Balanced/Aggressive) with descriptions
6. **Before/After Diff View** - Side-by-side comparison with changes table

Features:
- Demo mode when no JDs exist (shows hardcoded demo data)
- Color-coded severity badges (red/yellow/grey)
- Loading states and error handling
- Real-time bias score updates

### 3. `/frontend/src/components/CandidateBiasView.jsx`
**Candidate dashboard component**

Features:
- Shows all candidate's applications
- For each application:
  - JD title and company
  - Bias check status badge (Bias Reviewed / Pending Review)
  - Bias score with visual progress bar
  - Color-coded status (green/yellow/red)
  - Summary message
- No trigger phrases, matrix, or rewrite data shown to candidates
- No recruiter-level information exposed

### 4. Dashboard Integration
Updated `/frontend/src/components/Dashboard.jsx`:
- Added "Bias Detection" tab for recruiters (first in list)
- Added "Fairness Check" tab for candidates (first in list)
- Proper routing and component rendering

## Data Flow

### Analysis Flow
1. Recruiter selects JD and clicks "Run Bias Analysis"
2. Frontend calls `POST /api/bias/analyze/{jd_id}`
3. Backend calls `analyze_jd_bias()` with GPT-4
4. Results saved to `bias_reports` and `intersectional_bias_matrix` tables
5. Frontend displays bias matrix, flags table, and stats

### Rewriting Flow
1. Recruiter selects variant (Conservative/Balanced/Aggressive)
2. Clicks "Generate Inclusive JD"
3. Frontend calls `POST /api/bias/rewrite/{jd_id}` with variant
4. Backend calls `generate_rewrite()` with GPT-4
5. Results saved to `job_descriptions.inclusive_text`
6. Frontend shows before/after diff with changes table

### Candidate View Flow
1. Candidate logs in and sees "Fairness Check" tab
2. Component fetches candidate's applications
3. For each application, fetches limited bias info via `GET /api/bias/candidate-view/{jd_id}`
4. Displays bias status cards with progress bars

## Indian-Specific Bias Taxonomy

The system detects bias across these axes with Indian context:

- **Gender**: "he should", "male candidate", "brotherhood", "manpower", "assertive", "dominant"
- **Age**: "young", "energetic team", "fresher preferred", "recent graduate", "digital native"
- **Caste**: "cultural fit", "good family background", "well-settled family"
- **College Tier**: "IIT preferred", "NIT preferred", "premier institute", "tier-1 college"
- **Regional Language**: "Hindi mandatory", "Hindi fluency required", "North Indian preferred"
- **Socioeconomic**: "excellent communication", "well-spoken", "presentable personality"
- **Matrimonial**: "willing to relocate", "no family commitments", "available for transfers"
- **Disability**: "physically fit", "no health issues", "able-bodied"

## Intersectional Detection

The system detects compound biases like:
- Gender + Age: "young, energetic male engineer" (excludes women and older workers)
- College Tier + Socioeconomic: "IIT/NIT preferred" (excludes state college graduates)
- Regional Language + Caste: "Hindi mandatory" (South Indian + implicit caste signal)
- Gender + Matrimonial: "without family commitments" (targets married women)

## Demo Mode

When no JDs exist in database:
- Frontend shows "Demo Mode" banner
- Uses hardcoded demo JD and bias results
- Allows testing all features without database setup
- Demo data includes realistic bias flags and intersectional matrix

## Error Handling

Backend:
- 400: Invalid request format
- 401: Missing/invalid token
- 403: Insufficient permissions
- 404: Resource not found
- 500: Analysis/rewrite failed

Frontend:
- Try/catch on all API calls
- User-friendly error messages
- Loading states during async operations
- Graceful fallback to demo mode

## Security & Access Control

- JWT token validation on all endpoints
- Role-based access control (recruiter/candidate/admin)
- Recruiters can only access their own JDs
- Candidates can only view JDs they applied to
- No sensitive data exposed to candidates

## Testing Checklist

- [ ] Recruiter can run bias analysis on JD
- [ ] Bias matrix displays correctly with color coding
- [ ] Recruiter can select rewrite variant
- [ ] Rewrite generates before/after diff
- [ ] Candidate sees limited bias info
- [ ] Candidate cannot access rewrite endpoint (403)
- [ ] Demo mode works when DB is empty
- [ ] All error cases handled gracefully
- [ ] Authorization header validation works
- [ ] Intersectional axes detected correctly

## Files Created

Backend:
- `/backend/agents/jd_bias_analyzer.py` - Bias detection and rewriting engine
- `/backend/routers/bias_detection.py` - REST API endpoints

Frontend:
- `/frontend/src/api/biasApi.js` - API client
- `/frontend/src/components/BiasDetectionPanel.jsx` - Recruiter component
- `/frontend/src/components/CandidateBiasView.jsx` - Candidate component

## Files Modified

Backend:
- `/backend/main.py` - Added bias_detection router import and registration (2 lines)

Frontend:
- `/frontend/src/components/Dashboard.jsx` - Added BiasDetectionPanel and CandidateBiasView imports and rendering

## Dependencies

Already installed:
- `openai` - For GPT-4 API calls
- `fastapi` - For REST endpoints
- `sqlalchemy` - For database queries

No new npm packages required for frontend.

## Environment Variables

Backend needs:
- `OPENAI_API_KEY` - For GPT-4 API calls (optional, falls back to keyword matching)

Frontend uses:
- `VITE_API_URL` - Backend API URL (already configured)

## Performance Considerations

- GPT-4 calls cached in database (bias_reports table)
- Keyword fallback for when API is unavailable
- Matrix generation optimized for display
- Candidate view limited to prevent data exposure
- Demo mode for testing without API calls

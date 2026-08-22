# Quick Reference - Bias Detection Features

## Files Created (5 files)

### Backend
1. `/backend/agents/jd_bias_analyzer.py` - Bias detection and rewriting engine
2. `/backend/routers/bias_detection.py` - REST API endpoints

### Frontend
3. `/frontend/src/api/biasApi.js` - API client
4. `/frontend/src/components/BiasDetectionPanel.jsx` - Recruiter component
5. `/frontend/src/components/CandidateBiasView.jsx` - Candidate component

## Files Modified (2 files)

### Backend
- `/backend/main.py` - Added 2 lines (import + register router)

### Frontend
- `/frontend/src/components/Dashboard.jsx` - Added imports and rendering

## API Endpoints (5 endpoints)

```
POST   /api/bias/analyze/{jd_id}           - Run analysis (RECRUITER/ADMIN)
GET    /api/bias/report/{jd_id}            - Get report (RECRUITER/CANDIDATE)
POST   /api/bias/rewrite/{jd_id}           - Generate rewrite (RECRUITER/ADMIN)
GET    /api/bias/jd-list                   - List JDs (RECRUITER)
GET    /api/bias/candidate-view/{jd_id}    - Candidate view (CANDIDATE)
```

## Key Features

### Bias Detection
- 8 identity axes (Gender, Age, Caste, College Tier, Regional Language, Socioeconomic, Matrimonial, Disability)
- Intersectional bias detection
- Severity scoring (1-10)
- Trigger phrase identification
- Visual bias matrix

### Job Rewriting
- 3 variants: Conservative, Balanced, Aggressive
- Before/after diff view
- Change tracking with reasons
- Bias score recalculation

### Access Control
- Recruiters: Full access
- Candidates: Limited view only
- Admin: Full access

## Demo Data

When no JDs exist:
- Demo JD: "Software Engineer — TechCorp India"
- 4 bias flags detected
- Bias score: 8.4/10
- Intersectional matrix included

## Color Coding

### Severity Badges
- Red: Critical (8-10)
- Yellow: Medium (5-7)
- Grey: Low (1-4)

### Bias Scores
- Red: High bias (>7)
- Yellow: Moderate bias (4-7)
- Green: Low bias (<4)

### Matrix Cells
- Red: High compound bias (>0.7)
- Yellow: Moderate (0.4-0.7)
- Green: Low (0-0.4)
- Grey: No data

## Testing Quick Start

```bash
# Backend
cd backend
python init_tables.py
uvicorn main:app --reload

# Frontend (new terminal)
cd frontend
npm run dev
```

## Test Scenarios

1. **Recruiter Analysis**: Select demo JD → Run Analysis → See matrix
2. **Recruiter Rewrite**: Select variant → Generate → See diff
3. **Candidate View**: Login as candidate → See fairness check
4. **Error Handling**: Try unauthorized access → See 403 error
5. **Demo Mode**: No JDs in DB → See demo data

## Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| "Missing Authorization header" | Ensure token in localStorage |
| "Only recruiters can..." | Login as recruiter |
| "Job description not found" | Check JD ID exists |
| "Run bias analysis first" | Must analyze before rewrite |
| GPT-4 timeout | Falls back to keyword matching |

## Database Queries

```sql
-- Check bias reports
SELECT * FROM bias_reports WHERE jd_id = '{jd_id}';

-- Check matrix
SELECT * FROM intersectional_bias_matrix 
WHERE report_id IN (SELECT id FROM bias_reports WHERE jd_id = '{jd_id}');

-- Check JD updates
SELECT id, title, bias_score, status, inclusive_text 
FROM job_descriptions WHERE id = '{jd_id}';
```

## API Examples

```bash
# Analyze
curl -X POST http://localhost:8000/api/bias/analyze/{jd_id} \
  -H "Authorization: Bearer {token}"

# Get Report
curl -X GET http://localhost:8000/api/bias/report/{jd_id} \
  -H "Authorization: Bearer {token}"

# Rewrite
curl -X POST http://localhost:8000/api/bias/rewrite/{jd_id} \
  -H "Authorization: Bearer {token}" \
  -d '{"variant": "balanced"}'

# List JDs
curl -X GET http://localhost:8000/api/bias/jd-list \
  -H "Authorization: Bearer {token}"

# Candidate View
curl -X GET http://localhost:8000/api/bias/candidate-view/{jd_id} \
  -H "Authorization: Bearer {token}"
```

## Component Props

### BiasDetectionPanel
- No props required
- Uses API to fetch data
- Manages own state

### CandidateBiasView
- No props required
- Uses API to fetch data
- Manages own state

## Environment Variables

```bash
# Backend .env
OPENAI_API_KEY=sk-...  # Optional, falls back to keyword matching

# Frontend .env
VITE_API_URL=http://localhost:8000
```

## Bias Taxonomy Quick Reference

| Axis | Examples |
|------|----------|
| Gender | "he should", "male candidate", "brotherhood" |
| Age | "young", "energetic team", "fresher preferred" |
| Caste | "cultural fit", "good family background" |
| College | "IIT preferred", "NIT preferred", "premier institute" |
| Language | "Hindi mandatory", "North Indian preferred" |
| Socioeconomic | "excellent communication", "well-spoken" |
| Matrimonial | "willing to relocate", "no family commitments" |
| Disability | "physically fit", "no health issues" |

## Intersectional Examples

- Gender + Age: "young, energetic male engineer"
- College + Socioeconomic: "IIT/NIT preferred"
- Language + Caste: "Hindi mandatory"
- Gender + Matrimonial: "without family commitments"

## Rewrite Variants

| Variant | Threshold | Use Case |
|---------|-----------|----------|
| Conservative | Severity >= 8 | Minimal changes |
| Balanced | Severity >= 5 | Recommended |
| Aggressive | All flags | Maximum inclusivity |

## Performance Targets

- Analysis: 5-10s (GPT-4), <1s (keyword)
- Rewrite: 5-10s (GPT-4), <1s (keyword)
- Database: <100ms
- Frontend: <500ms

## Security Checklist

- [x] JWT validation on all endpoints
- [x] Role-based access control
- [x] Recruiter can only access own JDs
- [x] Candidate can only view applied JDs
- [x] No credentials in frontend
- [x] No sensitive data exposed to candidates

## Documentation Files

1. `BIAS_DETECTION_IMPLEMENTATION.md` - Technical details
2. `BIAS_DETECTION_TESTING.md` - Testing guide
3. `BIAS_DETECTION_SUMMARY.md` - Feature summary
4. `IMPLEMENTATION_CHECKLIST.md` - Verification checklist
5. `QUICK_REFERENCE.md` - This file

## Next Steps

1. Run backend: `uvicorn main:app --reload`
2. Run frontend: `npm run dev`
3. Test scenarios from BIAS_DETECTION_TESTING.md
4. Verify database integration
5. Test with real OpenAI API key
6. Gather user feedback
7. Iterate based on feedback

## Support

For issues:
1. Check BIAS_DETECTION_TESTING.md troubleshooting section
2. Check error messages in browser console
3. Check backend logs
4. Verify database connection
5. Verify API key (if using GPT-4)

## Status

✓ Implementation Complete
✓ All requirements met
✓ Ready for testing
✓ Documentation complete

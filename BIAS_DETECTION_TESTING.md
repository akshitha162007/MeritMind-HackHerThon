# Bias Detection Features - Testing Guide

## Quick Start

### Backend Setup
```bash
cd backend
# Ensure OPENAI_API_KEY is set in .env (optional, falls back to keyword matching)
python init_tables.py
uvicorn main:app --reload
```

### Frontend Setup
```bash
cd frontend
npm run dev
```

## Testing Scenarios

### Scenario 1: Recruiter Bias Analysis (Demo Mode)

**Steps:**
1. Register as recruiter: `test@recruiter.com` / `password123`
2. Login and go to Dashboard
3. Click "Bias Detection" tab
4. See "Demo Mode" banner (no JDs in DB)
5. Select "Demo JD - TechCorp India" from dropdown
6. Click "Run Bias Analysis"

**Expected Results:**
- Bias score shows 8.4/10 (red)
- 4 bias flags displayed in table
- Matrix shows compound scores
- Intersectional flags count = 4

**Verify:**
- Severity badges show correct colors (red for 8-9, yellow for 7)
- Harmed groups are descriptive
- Matrix cells are color-coded

### Scenario 2: Recruiter Rewrite JD

**Steps:**
1. After analysis completes, see rewrite panel
2. Select "Balanced" variant (default)
3. Click "Generate Inclusive JD"

**Expected Results:**
- Improvement banner shows: "Bias score reduced from 8.4 to 3.2 (5.2% improvement)"
- Before/After columns show side-by-side comparison
- Changes table shows 4 replacements
- Original phrases highlighted in red, new phrases in green

**Verify:**
- Changes are meaningful (e.g., "young, energetic male" → "experienced engineer")
- Reason column explains each change
- New bias score is lower than original

### Scenario 3: Candidate Fairness Check

**Steps:**
1. Register as candidate: `test@candidate.com` / `password123`
2. Login and go to Dashboard
3. Click "Fairness Check" tab

**Expected Results:**
- See message: "No applications yet"
- No bias data shown (candidates need applications first)

**Verify:**
- Component handles empty state gracefully
- No error messages

### Scenario 4: Candidate Limited View (with Application)

**Prerequisites:**
- Create a job description as recruiter
- Create an application linking candidate to that JD
- Run bias analysis on the JD

**Steps:**
1. Login as candidate
2. Go to "Fairness Check" tab
3. See applied job with bias status

**Expected Results:**
- Job card shows title and company
- "Bias Reviewed" badge (green)
- Bias score: X.X/10
- Progress bar showing bias level
- Message: "This job description has been reviewed for bias and inclusivity by Merit Mind AI"

**Verify:**
- No trigger phrases shown
- No matrix shown
- No rewrite data shown
- Only summary information visible

### Scenario 5: Error Handling

**Test 401 Unauthorized:**
1. Clear localStorage token
2. Try to access bias endpoints
3. Should redirect to login

**Test 403 Forbidden:**
1. Login as candidate
2. Try to access `/api/bias/rewrite/{jd_id}`
3. Should show: "Only recruiters can rewrite job descriptions"

**Test 404 Not Found:**
1. Try to analyze non-existent JD ID
2. Should show: "Job description not found"

**Test 400 Bad Request:**
1. Try to analyze with invalid UUID format
2. Should show: "Invalid JD ID format"

### Scenario 6: Variant Testing

**Conservative Variant:**
1. Run analysis
2. Select "Conservative" variant
3. Generate rewrite
4. Should fix only severity 8-10 flags (fewer changes)

**Aggressive Variant:**
1. Run analysis
2. Select "Aggressive" variant
3. Generate rewrite
4. Should fix all flags (more changes, lower final score)

**Verify:**
- Conservative has fewer changes than Balanced
- Aggressive has more changes than Balanced
- Final scores reflect variant intensity

## API Testing with cURL

### Test Bias Analysis
```bash
curl -X POST http://localhost:8000/api/bias/analyze/{jd_id} \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json"
```

### Test Get Report
```bash
curl -X GET http://localhost:8000/api/bias/report/{jd_id} \
  -H "Authorization: Bearer {token}"
```

### Test Rewrite
```bash
curl -X POST http://localhost:8000/api/bias/rewrite/{jd_id} \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"variant": "balanced"}'
```

### Test JD List
```bash
curl -X GET http://localhost:8000/api/bias/jd-list \
  -H "Authorization: Bearer {token}"
```

### Test Candidate View
```bash
curl -X GET http://localhost:8000/api/bias/candidate-view/{jd_id} \
  -H "Authorization: Bearer {token}"
```

## Database Verification

### Check Bias Reports
```sql
SELECT * FROM bias_reports WHERE jd_id = '{jd_id}';
```

### Check Intersectional Matrix
```sql
SELECT * FROM intersectional_bias_matrix WHERE report_id IN (
  SELECT id FROM bias_reports WHERE jd_id = '{jd_id}'
);
```

### Check Job Description Updates
```sql
SELECT id, title, bias_score, status, inclusive_text FROM job_descriptions WHERE id = '{jd_id}';
```

## Performance Testing

### Load Testing
1. Run analysis on same JD multiple times
2. Should complete in < 5 seconds (with GPT-4)
3. Should complete in < 1 second (with keyword fallback)

### Concurrent Requests
1. Run analysis on multiple JDs simultaneously
2. Should handle without errors
3. Each should complete independently

## Edge Cases

### Empty JD Text
1. Create JD with empty raw_text
2. Run analysis
3. Should return empty bias_flags list
4. Overall score should be 0

### Very Long JD Text
1. Create JD with 10,000+ characters
2. Run analysis
3. Should complete without timeout
4. Should detect all bias flags

### Special Characters
1. Create JD with special characters, emojis, etc.
2. Run analysis
3. Should handle gracefully
4. Should not crash

### Duplicate Analysis
1. Run analysis on same JD twice
2. Second run should replace first results
3. No duplicate entries in database

## UI/UX Testing

### Responsive Design
1. Test on desktop (1920x1080)
2. Test on tablet (768x1024)
3. Test on mobile (375x667)
4. All components should be readable

### Loading States
1. Click "Run Bias Analysis"
2. Button should show "Analyzing..."
3. Button should be disabled
4. Should re-enable after completion

### Error Messages
1. Trigger various errors
2. Messages should be clear and actionable
3. Should not show technical jargon

### Color Coding
1. Verify severity badges use correct colors
2. Verify matrix cells use correct colors
3. Verify score indicators use correct colors

## Accessibility Testing

### Keyboard Navigation
1. Tab through all form elements
2. Should be able to submit forms with Enter
3. Should be able to select dropdowns with arrow keys

### Screen Reader
1. Test with screen reader
2. All labels should be readable
3. Table headers should be announced

### Color Contrast
1. Verify all text meets WCAG AA standards
2. Don't rely on color alone for information

## Demo Mode Testing

### Verify Demo Data
1. Clear database or use fresh instance
2. Load BiasDetectionPanel
3. Should show "Demo Mode" banner
4. Should load demo JD automatically
5. Demo data should be realistic and comprehensive

### Verify Fallback
1. Disable OpenAI API (remove OPENAI_API_KEY)
2. Run analysis
3. Should use keyword fallback
4. Should still detect bias flags
5. Should complete quickly

## Checklist

- [ ] Recruiter can run bias analysis
- [ ] Bias matrix displays with correct colors
- [ ] Recruiter can generate rewrite
- [ ] Before/after diff shows correctly
- [ ] Changes table is accurate
- [ ] Candidate sees limited bias info
- [ ] Candidate cannot access rewrite
- [ ] Demo mode works
- [ ] All error cases handled
- [ ] Authorization works
- [ ] Database saves correctly
- [ ] API responses are valid JSON
- [ ] UI is responsive
- [ ] Loading states work
- [ ] Color coding is correct
- [ ] Intersectional detection works
- [ ] Variants produce different results
- [ ] Performance is acceptable

## Known Limitations

1. GPT-4 API calls may be slow (5-10 seconds)
2. Keyword fallback is less accurate than GPT-4
3. Demo mode uses hardcoded data
4. No real-time updates (requires page refresh)
5. Matrix only shows first 5 axes for display

## Troubleshooting

### "Missing or invalid Authorization header"
- Ensure token is in localStorage
- Ensure token is not expired
- Check Authorization header format: "Bearer {token}"

### "Only recruiters can run bias analysis"
- Ensure logged in as recruiter
- Check user role in database

### "Job description not found"
- Ensure JD ID is correct
- Ensure JD exists in database
- Check UUID format

### "Run bias analysis first before rewriting"
- Must run analysis before rewrite
- Analysis creates bias_reports records
- Rewrite uses those records

### GPT-4 API errors
- Check OPENAI_API_KEY is set
- Check API key is valid
- Check API quota not exceeded
- System will fall back to keyword matching

### Database errors
- Ensure database is running
- Ensure tables are created
- Check DATABASE_URL is correct
- Run `python init_tables.py` if needed

# Financial Evaluation Tool - Deployment Checklist

## Pre-Deployment Steps

### 1. Install Dependencies
```bash
cd flask_app
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

### 2. Run Database Migration
```bash
cd ..
python3 scripts/add_evaluation_tables.py
```

Expected output:
```
✓ Database migration completed successfully!
  - Created/verified 'financial_evaluation' table
  - Created/verified 'evaluation_phase' table
```

### 3. Start Flask Application
```bash
cd flask_app
source .venv/bin/activate
python3 app.py
```

Flask should start on `http://localhost:5000`

## Feature Verification Checklist

### UI Components
- [ ] "Évaluation Financière" button visible in PR checklist header
- [ ] Button has correct styling (gradient blue background)
- [ ] Button icon displays correctly (Euro symbol)
- [ ] Modal opens when button is clicked
- [ ] Modal can be closed with X button

### OI Phase
- [ ] Tab displays correctly
- [ ] Company name and amount inputs are functional
- [ ] "Ajouter" button adds companies to table
- [ ] Companies display in table with delete option
- [ ] "Évaluer OI" button executes evaluation
- [ ] Results show color-coded passed/eliminated companies
- [ ] Gap percentages calculated correctly
- [ ] OA1 tab becomes enabled after evaluation

### OA1 Phase
- [ ] Tab shows only after OI is evaluated
- [ ] Can add companies (limited to OI winners)
- [ ] Evaluation filters for gap < 5%
- [ ] OA2 tab enables after evaluation

### OA2 Phase
- [ ] Tab shows only after OA1 is evaluated
- [ ] Selects only the cheapest supplier
- [ ] Results display winner correctly

### Database Operations
- [ ] "Enregistrer" saves evaluation to database
- [ ] Toast notification confirms save
- [ ] Saved evaluations persist across sessions
- [ ] Multiple evaluations can exist for one PR

### Excel Export
- [ ] "Exporter Excel" downloads file
- [ ] Filename format: `Evaluation_{title}_{timestamp}.xlsx`
- [ ] Excel file opens without errors
- [ ] Summary sheet displays phase statistics
- [ ] OI, OA1, OA2 sheets show results with color coding
- [ ] French language labels display correctly

### Data Integrity
- [ ] No errors in browser console
- [ ] No errors in Flask server logs
- [ ] All API calls return expected status codes
- [ ] Database records properly linked to PR

## API Endpoint Testing

### 1. Create Evaluation
```bash
curl -X POST http://localhost:5000/api/financial-evaluation \
  -H "Content-Type: application/json" \
  -d '{"pr_id": "PR_ID", "title": "Test Evaluation"}'
```
Expected: 201 with evaluation object

### 2. Evaluate Phase
```bash
curl -X POST http://localhost:5000/api/financial-evaluation/EVAL_ID/evaluate-phase \
  -H "Content-Type: application/json" \
  -d '{
    "phase": "OI",
    "companies": [
      {"name": "Company A", "amount": 1000},
      {"name": "Company B", "amount": 1100}
    ],
    "previous_winners": []
  }'
```
Expected: 200 with results

### 3. Export to Excel
```bash
curl -X GET http://localhost:5000/api/financial-evaluation/EVAL_ID/export \
  --output evaluation.xlsx
```
Expected: 200 with xlsx file

### 4. Get Evaluations for PR
```bash
curl -X GET http://localhost:5000/api/pr/PR_ID/evaluations
```
Expected: 200 with array of evaluations

## Performance Notes
- Modal initialization: < 100ms
- Phase evaluation (4-10 companies): < 50ms
- Database save: < 100ms
- Excel export (3 phases): < 500ms
- All operations should complete without noticeable lag

## Browser Compatibility
- ✅ Chrome/Edge (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)
- ✅ Mobile browsers (responsive design)

## Rollback Plan

If issues occur:

1. **Revert code changes:**
   ```bash
   git revert 8b2dc20
   ```

2. **Remove evaluation tables (optional):**
   ```bash
   sqlite3 flask_app/data/pr_data.db
   > DROP TABLE IF EXISTS financial_evaluation;
   > DROP TABLE IF EXISTS evaluation_phase;
   > .quit
   ```

3. **Restart Flask application**

## Known Limitations

1. **Phase Progression:** Phases must be evaluated in order (OI → OA1 → OA2)
2. **Company Names:** Must be unique within a phase
3. **Amounts:** Must be positive numbers
4. **Excel Export:** Limited to 3 phases per evaluation
5. **Concurrent Edits:** Last save wins (no conflict resolution)

## Support Resources

- Implementation details: `FINANCIAL_EVALUATION_IMPLEMENTATION.md`
- Code comments in Flask routes explain each function
- JavaScript functions have detailed JSDoc comments
- CSS classes follow BEM naming convention

## Monitoring

Monitor these metrics after deployment:
- Database file size growth
- API response times
- Excel export generation time
- Number of concurrent evaluations
- User adoption rate

---

**Deployment Date:** _______________
**Deployed By:** _______________
**Notes:** _______________

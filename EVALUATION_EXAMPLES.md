# Financial Evaluation Tool - Usage Examples

## Scenario 1: Simple 3-Company OI Evaluation

### Setup
You want to evaluate 3 equipment suppliers for a purchase request.

### Step 1: Open Evaluation
1. Click "Évaluation Financière" button in PR checklist
2. Modal opens with OI tab selected
3. Change title to: "Évaluation Fournisseurs Équipement XYZ"

### Step 2: Enter Companies

| Fournisseur | Montant | Action |
|-----------|---------|--------|
| TechCorp | €1,000 | Add |
| GlobalTrade | €1,050 | Add |
| LocalSupply | €1,100 | Add |

### Step 3: Evaluate
- Click "Évaluer OI"
- Results show:
  - ✓ Passed: TechCorp (€1,000, 0%), GlobalTrade (€1,050, +5%), LocalSupply (€1,100, +10%)
  - All 3 qualify (gap < 15%)

### Expected Results
- **Minimum price:** €1,000
- **TechCorp Gap:** 0% ✓
- **GlobalTrade Gap:** 5% ✓
- **LocalSupply Gap:** 10% ✓

---

## Scenario 2: 5-Company OI with 4th Disqualified

### Setup
Multiple quotes with one expensive option

### Companies
| Name | Amount |
|------|--------|
| Supplier A | €500 |
| Supplier B | €520 |
| Supplier C | €540 |
| Supplier D | €600 |
| Supplier E | €800 |

### Evaluation Result
- ✓ **Passed (4):** A, B, C, D
  - A: €500 (0%)
  - B: €520 (+4%)
  - C: €540 (+8%)
  - D: €600 (+20%) ← Exceeds 15% but still in top 3

**Note:** Supplier E (€800, +60%) is eliminated because it's beyond top 3 and gap > 15%

---

## Scenario 3: Multi-Phase Complete Evaluation

### Phase 1: OI - Initial Offers (7 suppliers)

**Input:**
```
Company 1: €10,000
Company 2: €10,500
Company 3: €11,000
Company 4: €11,200
Company 5: €12,000
Company 6: €13,000
Company 7: €15,000
```

**OI Results:** Companies 1-4 pass (minimum gap logic)
- Top 3: Companies 1, 2, 3
- 4th: Company 4 (€11,200 = 12% gap, < 15%)
- Eliminated: Companies 5, 6, 7

### Phase 2: OA1 - Improved Offers (from OI winners)

**Input (refined quotes from OI winners):**
```
Company 1: €9,500
Company 2: €10,000
Company 3: €10,200
Company 4: €10,800
```

**OA1 Results:**
- Minimum: €9,500 (Company 1)
- ✓ Pass: Company 1 (0%), Company 2 (+5.26%), Company 3 (+7.37%)
- ✗ Eliminate: Company 4 (+13.68%, > 5% threshold)

### Phase 3: OA2 - Final Offers (from OA1 winners)

**Input (best offers from 3 finalists):**
```
Company 1: €9,200
Company 2: €9,300
Company 3: €9,400
```

**OA2 Results:**
- **Winner:** Company 1 (€9,200)
- Not selected: Companies 2, 3

---

## Scenario 4: Excel Export Example

### When You Export to Excel

The system generates a file: `Evaluation_Fournisseurs_Équipement_XYZ_20240428_143020.xlsx`

### Sheet 1: Résumé (Summary)
| Phase | Passées | Éliminées |
|-------|---------|-----------|
| OI | 4 | 3 |
| OA1 | 3 | 1 |
| OA2 | 1 | 2 |

### Sheet 2: Résultats OI

| Fournisseur | Montant | Écart % | Rang | Statut |
|------------|---------|---------|------|--------|
| Company 1 | €10,000 | 0.00% | 1 | ✓ Sélectionné |
| Company 2 | €10,500 | 5.00% | 2 | ✓ Sélectionné |
| Company 3 | €11,000 | 10.00% | 3 | ✓ Sélectionné |
| Company 4 | €11,200 | 12.00% | 4 | ✓ Sélectionné |
| Company 5 | €12,000 | 20.00% | 5 | ✗ Éliminé |

### Sheet 3: Résultats OA1
(Green rows for passed, red rows for eliminated)

### Sheet 4: Résultats OA2
(Single winner highlighted)

---

## API Usage Examples

### Create Evaluation via cURL

```bash
curl -X POST http://localhost:5000/api/financial-evaluation \
  -H "Content-Type: application/json" \
  -d '{
    "pr_id": "PR-2024-001",
    "title": "Évaluation Services Cloud"
  }'
```

**Response:**
```json
{
  "id": "eval-uuid-1234",
  "pr_id": "PR-2024-001",
  "title": "Évaluation Services Cloud",
  "phase": "OI",
  "status": "active",
  "data": {},
  "created_date": "2024-04-28T14:30:20.123456",
  "updated_date": "2024-04-28T14:30:20.123456"
}
```

### Evaluate OI Phase via cURL

```bash
curl -X POST http://localhost:5000/api/financial-evaluation/eval-uuid-1234/evaluate-phase \
  -H "Content-Type: application/json" \
  -d '{
    "phase": "OI",
    "companies": [
      {"name": "CloudPro", "amount": 5000},
      {"name": "DataSystem", "amount": 5200},
      {"name": "TechHost", "amount": 5500}
    ],
    "previous_winners": []
  }'
```

**Response:**
```json
{
  "phase": "OI",
  "results": {
    "passed": [
      {
        "name": "CloudPro",
        "amount": 5000,
        "gap_percent": 0,
        "rank": 1,
        "status": "passed"
      },
      {
        "name": "DataSystem",
        "amount": 5200,
        "gap_percent": 4,
        "rank": 2,
        "status": "passed"
      },
      {
        "name": "TechHost",
        "amount": 5500,
        "gap_percent": 10,
        "rank": 3,
        "status": "passed"
      }
    ],
    "eliminated": [],
    "reasoning": {
      "CloudPro": {"amount": 5000, "gap_percent": 0, "rank": 1},
      "DataSystem": {"amount": 5200, "gap_percent": 4, "rank": 2},
      "TechHost": {"amount": 5500, "gap_percent": 10, "rank": 3}
    }
  },
  "passed_count": 3,
  "eliminated_count": 0
}
```

---

## Common Gap Percentage Scenarios

### When Minimum = €100

| Amount | Gap % | Formula |
|--------|-------|---------|
| €100 | 0% | (100-100)/100 = 0% |
| €105 | 5% | (105-100)/100 = 5% |
| €110 | 10% | (110-100)/100 = 10% |
| €115 | 15% | (115-100)/100 = 15% |
| €120 | 20% | (120-100)/100 = 20% |

### OI Phase Threshold (< 15%)
- €100 → €114.99 ✓ Acceptable
- €115 → Above ✗ Rejected (unless in top 3)

### OA1 Phase Threshold (< 5%)
- €100 → €104.99 ✓ Acceptable
- €105 → Above ✗ Rejected (unless cheapest)

### OA2 Phase (≤ 0%)
- Only the absolute cheapest wins
- No gap tolerance

---

## Tips & Best Practices

### 1. Accurate Company Names
- Use consistent naming (e.g., "Company Name Inc." not "Company Name Inc")
- Helps with cross-phase tracking

### 2. Realistic Amounts
- Use actual quote values
- Include all relevant costs
- Use consistent currency (EUR in examples)

### 3. Review Before Export
- Check results display correctly
- Verify all expected companies are listed
- Confirm gaps are calculated correctly

### 4. Save Regularly
- Save after each phase evaluation
- Database preserves complete history
- Can review/export later

### 5. Use Consistent Evaluation Criteria
- Apply same threshold logic across evaluations
- Document any exceptions
- Share Excel exports for team review

---

## Troubleshooting

### Problem: Gap calculation seems wrong
**Check:** Is the minimum amount correct?
```
Gap = (Company Amount - Minimum Amount) / Minimum Amount * 100
```

### Problem: Phase won't evaluate
**Check:** 
- Are there companies entered?
- Is previous phase evaluated?
- Are amounts valid numbers?

### Problem: Export file won't open
**Check:**
- File format is .xlsx (modern Excel)
- Not corrupted (try re-exporting)
- Sufficient disk space

### Problem: Results don't match expected
**Check:**
- Amounts entered correctly
- Using correct phase logic
- Companies from previous phase included

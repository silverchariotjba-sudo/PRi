# Financial Evaluations Tool

## Overview

A comprehensive financial evaluation tool has been added to the Flask PR tracking application. This tool implements a three-phase evaluation process for supplier offers (OI, OA1, OA2) with automatic calculations, color-coded results, and Excel export capabilities.

## Features

### 1. **Three-Phase Evaluation Workflow**

#### **OI (Offres Initiales - Initial Offers)**
- Automatically keeps the 3 cheapest suppliers
- Includes 4th supplier if their price gap is less than 15% from the cheapest
- Formula: `Gap% = (Supplier Amount - Cheapest Amount) / Cheapest Amount × 100`
- Suppliers exceeding 15% gap are discarded
- Status: "Relancé OA1" (Sent for Round 1) or "Écarté" (Discarded)

#### **OA1 (Offres Améliorées 1 - Improved Offers Round 1)**
- Keeps the cheapest supplier from this round
- Includes suppliers with price gap less than 5%
- **Special Rule**: Always keeps the supplier who was cheapest in OI, even if their OA1 offer exceeds 5% gap
- This ensures continuity and fairness in negotiations
- Status: "Relancé OA2" (Sent for Round 2) or "Écarté" (Discarded)

#### **OA2 (Offres Améliorées 2 - Improved Offers Round 2)**
- Selects only the cheapest supplier(s)
- If multiple suppliers have the same lowest price, both are advanced for potential OA3
- Status: "Retenu" (Selected) or "Écarté" (Discarded)

### 2. **User Interface**

- **Navbar Button**: "Évaluations" button added to the main navigation bar
- **Evaluations View**: Accessible from the dashboard via the navbar button
- **List View**: Shows all created evaluations with their current phase status
- **Detail View**: Displays evaluation phases as cards with evaluation buttons and results table

### 3. **Data Entry**

- **New Evaluation Modal**: Enter evaluation title and initial supplier data
- **Company Input Form**: Add multiple suppliers with their offer amounts
- **Phase-Specific Forms**: Re-enter amounts for each phase before evaluation

### 4. **Results Display**

Results are shown in a comprehensive table with:
- Phase (OI, OA1, OA2)
- Company name
- Amount offered (formatted with currency)
- Ranking among suppliers in that phase
- Gap percentage with visual formatting
- Status (Relancé/Écarté/Retenu)
- Detailed reason for the decision

### 5. **Excel Export**

- Export complete evaluation to XLSX format
- Professional formatting with:
  - Title and creation date in header
  - Color-coded rows (red for discarded, blue for relaunched, green for selected)
  - Formatted currency amounts
  - Auto-adjusted column widths
  - Professional table styling

### 6. **Data Persistence**

- All evaluations stored in SQLite database
- Tables: `evaluation` (metadata) and `evaluation_result` (results per phase)
- Evaluations can be deleted
- Results are saved after each phase evaluation

## How to Use

### Creating an Evaluation

1. Click the "Évaluations" button in the navbar
2. Click "Nouvelle Évaluation" (New Evaluation)
3. Enter a title (e.g., "Évaluation - PR 2025-001")
4. Add suppliers and their initial offer amounts
5. Click "Créer et Commencer" to create the evaluation

### Evaluating Each Phase

1. Click the phase card (OI, OA1, or OA2)
2. Enter or update the supplier amounts
3. Review the phase description for specific rules
4. Click "Évaluer" to calculate results
5. View color-coded results table
6. Next phase button appears automatically

### Exporting Results

1. Open an evaluation detail view
2. Click "Exporter Excel" to download formatted results
3. File is named: `Evaluation_[ID].xlsx`

## Technical Implementation

### Database Schema

```sql
-- Evaluation metadata
CREATE TABLE evaluation (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    created_date TEXT NOT NULL,
    current_phase TEXT NOT NULL DEFAULT 'OI',
    data_json TEXT NOT NULL,
    results_json TEXT NOT NULL DEFAULT '{}'
)

-- Phase results
CREATE TABLE evaluation_result (
    id TEXT PRIMARY KEY,
    evaluation_id TEXT NOT NULL,
    phase TEXT NOT NULL,
    company_name TEXT NOT NULL,
    amount REAL NOT NULL,
    rank INTEGER,
    gap_percent REAL,
    status TEXT NOT NULL,
    reason TEXT,
    FOREIGN KEY (evaluation_id) REFERENCES evaluation(id) ON DELETE CASCADE
)
```

### API Routes

- `GET /api/evaluations` - List all evaluations
- `POST /api/evaluations` - Create new evaluation
- `GET /api/evaluations/<id>` - Get evaluation details
- `POST /api/evaluations/<id>/evaluate` - Calculate phase results
- `GET /api/evaluations/<id>/export` - Export to Excel
- `DELETE /api/evaluations/<id>` - Delete evaluation

### Evaluation Logic Functions

- `calculate_gap_percent()` - Compute gap percentage
- `evaluate_oi()` - OI phase logic
- `evaluate_oa1()` - OA1 phase logic with special handling
- `evaluate_oa2()` - OA2 phase logic

## Integration Points

### Dashboard
- Evaluations accessible from navbar while on dashboard
- Separate view that doesn't interfere with PR tracking

### Navigation
- Back buttons return to appropriate views
- Modal forms for data entry
- Smooth transitions between list and detail views

## Files Modified

- `flask_app/app.py` - Database tables, evaluation logic, API routes
- `flask_app/templates/index.html` - Evaluations view, modals, HTML structure
- `flask_app/templates/base.html` - Added Évaluations navbar button
- `flask_app/static/js/app.js` - JavaScript functionality, forms, bindings
- `flask_app/static/css/style.css` - Styling for evaluation components

## Example Evaluation Scenario

### OI Phase Input
| Supplier | Amount |
|----------|--------|
| Company A | 100,000€ |
| Company B | 115,000€ |
| Company C | 125,000€ |
| Company D | 130,000€ |
| Company E | 180,000€ |

### OI Results
- Company A: Rank 1, Gap 0%, **Relancé OA1** (3rd cheapest)
- Company B: Rank 2, Gap 15%, **Relancé OA1** (2nd cheapest)
- Company C: Rank 3, Gap 25%, **Relancé OA1** (3rd cheapest)
- Company D: Rank 4, Gap 30%, **Écarté** (Gap > 15%)
- Company E: Rank 5, Gap 80%, **Écarté** (Gap > 15%)

### OA1 Phase (with Company A's new offer of 110,000€)
- Company A: Rank 2, Gap 10%, **Relancé OA2** (Initial cheapest - kept despite 10% gap)
- Company B: Rank 3, Gap 20%, **Écarté** (Gap > 5%)
- Company C: Rank 1, Gap 0%, **Relancé OA2** (Cheapest in OA1)

### OA2 Phase (final round)
- Company A: 105,000€ - **Écarté** (Not cheapest)
- Company C: 120,000€ - **Retenu** (Cheapest, selected)

## Error Handling

- Validation for minimum 2 suppliers
- Validation for valid numerical amounts
- Proper error messages displayed via toast notifications
- Database transaction rollback on errors
- Try-catch blocks in all async operations

## Features Planned for Future

- Support for OA3 phase
- Import evaluations from Excel
- Evaluation templates
- Historical comparison
- Supplier performance metrics
- Budget tracking
- Automated report generation

---

**Status**: Fully implemented and ready for use
**Last Updated**: 2026-04-28

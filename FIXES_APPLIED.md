# Fixes Applied - Database and Data Issues

## Issues Found

1. **Empty Database** - App was displaying empty with no PR data
2. **Missing Evaluation Tables** - Financial evaluation tables not created on init
3. **No Sample Data** - New installations had no data to display

## Solutions Implemented

### 1. Database Table Creation
- Added `financial_evaluation` table to `init_db()` function
- Added `evaluation_phase` table to `init_db()` function
- Tables now created automatically on first app startup
- Removed dependency on separate migration script

### 2. Sample Data Seeding
- Created `seed_sample_data()` function with 4 sample PRs:
  - PR #001: Achat de Serveurs IT (CR status: en-cours)
  - PR #002: Fournitures de Bureau (ED status: en-cours)
  - PR #003: Logiciels de Gestion (CR status: en-cours)
  - PR #004: Maintenance Équipements (REG status: cloturee)
- Each PR includes sample tasks based on category
- Document checklists automatically populated per category

### 3. Initialization Flow
- `seed_sample_data()` called on app startup
- Function checks if DB has existing data before inserting samples
- Won't duplicate data on subsequent app runs
- Old empty database file deleted to force clean initialization

## Testing the Fix

1. Start the Flask app:
   ```bash
   cd flask_app
   source .venv/bin/activate
   python3 app.py
   ```

2. App should now display:
   - Dashboard with 4 sample PRs
   - KPI cards showing statistics
   - PR list in sidebar with sample data
   - Financial Evaluation button in top navbar

## Files Modified

- `flask_app/app.py`:
  - Added `seed_sample_data()` function (24 lines)
  - Added financial evaluation tables to `init_db()` (29 lines)
  - Added call to `seed_sample_data()` in main block
  - Deleted old empty database file

## Migration Path

For users with existing data:
- The seeding function checks `SELECT COUNT(*) FROM pr` before inserting
- If database has any PR records, samples are NOT added
- Existing data is preserved
- No data loss or overwriting occurs

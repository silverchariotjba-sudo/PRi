#!/usr/bin/env python3
"""
Database migration script to add financial evaluation tables.
Run this after adding evaluation features to create necessary tables.
"""

import sqlite3
import os
import sys

# Add parent directory to path so we can import from flask_app
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'flask_app', 'data', 'pr_data.db')

def migrate():
    """Create financial evaluation tables if they don't exist."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Enable foreign keys
    c.execute("PRAGMA foreign_keys = ON")
    
    # Create financial_evaluation table
    c.execute("""
        CREATE TABLE IF NOT EXISTS financial_evaluation (
            id TEXT PRIMARY KEY,
            pr_id TEXT NOT NULL,
            title TEXT NOT NULL,
            phase TEXT DEFAULT 'OI',
            status TEXT DEFAULT 'active',
            data TEXT,
            created_date TEXT NOT NULL,
            updated_date TEXT NOT NULL,
            FOREIGN KEY (pr_id) REFERENCES pr(id) ON DELETE CASCADE
        )
    """)
    
    # Create evaluation_phase table
    c.execute("""
        CREATE TABLE IF NOT EXISTS evaluation_phase (
            id TEXT PRIMARY KEY,
            evaluation_id TEXT NOT NULL,
            phase_name TEXT NOT NULL,
            phase_status TEXT DEFAULT 'pending',
            companies TEXT,
            results TEXT,
            created_date TEXT NOT NULL,
            FOREIGN KEY (evaluation_id) REFERENCES financial_evaluation(id) ON DELETE CASCADE
        )
    """)
    
    conn.commit()
    conn.close()
    
    print("✓ Database migration completed successfully!")
    print(f"  - Created/verified 'financial_evaluation' table")
    print(f"  - Created/verified 'evaluation_phase' table")
    print(f"  - Database location: {DB_PATH}")

if __name__ == "__main__":
    try:
        migrate()
    except Exception as e:
        print(f"✗ Migration failed: {e}", file=sys.stderr)
        sys.exit(1)

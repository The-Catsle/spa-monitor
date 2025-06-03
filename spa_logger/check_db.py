#!/usr/bin/env python3

import sqlite3
from pathlib import Path

# Database configuration
DB_FILE = str(Path(__file__).parent / 'spa_metrics.db')

def check_database():
    """Check database statistics and print results."""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # Get total number of rows
        cursor.execute('SELECT COUNT(*) FROM spa_metrics')
        row_count = cursor.fetchone()[0]
        print(f"Total number of rows in database: {row_count}")
        
        # Get latest timestamp
        cursor.execute('SELECT timestamp FROM spa_metrics ORDER BY timestamp DESC LIMIT 1')
        latest_timestamp = cursor.fetchone()[0]
        print(f"Latest entry timestamp: {latest_timestamp}")
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    check_database() 
#!/usr/bin/env python3

import os
import sys
import sqlite3
import logging
from datetime import datetime
from pathlib import Path

# Add parent directory to path to import spa_monitor
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from spa_monitor import get_spa_status

# Configure logging
log_file = Path(__file__).parent / 'spa_logger.log'
logging.basicConfig(
    filename=str(log_file),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Database configuration
DB_FILE = str(Path(__file__).parent / 'spa_metrics.db')

def create_database():
    """Create the database and table if they don't exist."""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # Create table with all fields from the API response
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS spa_metrics (
                timestamp DATETIME,
                connected BOOLEAN,
                temperatureF FLOAT,
                setpointF FLOAT,
                lights TEXT,
                spaboy_connected BOOLEAN,
                spaboy_producing BOOLEAN,
                ph FLOAT,
                ph_status TEXT,
                orp INTEGER,
                orp_status TEXT,
                pump1 TEXT,
                pump2 TEXT,
                filter_status TEXT,
                filtration_duration INTEGER,
                filtration_frequency INTEGER,
                filter_suspension TEXT,
                errors TEXT
            )
        ''')
        
        conn.commit()
        logging.info("Database and table created successfully")
    except sqlite3.Error as e:
        logging.error(f"Database error: {e}")
        raise
    finally:
        if conn:
            conn.close()

def log_spa_metrics():
    """Get spa status and log it to the database."""
    try:
        # Get current spa status
        status = get_spa_status()
        
        # Connect to database
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # Prepare the data for insertion
        current_time = datetime.now()
        data = (
            current_time,
            status.get('connected'),
            status.get('temperatureF'),
            status.get('setpointF'),
            status.get('lights'),
            status.get('spaboy_connected'),
            status.get('spaboy_producing'),
            status.get('ph'),
            status.get('ph_status'),
            status.get('orp'),
            status.get('orp_status'),
            status.get('pump1'),
            status.get('pump2'),
            status.get('filter_status'),
            status.get('filtration_duration'),
            status.get('filtration_frequency'),
            status.get('filter_suspension'),
            str(status.get('errors', []))
        )
        
        # Insert the data
        cursor.execute('''
            INSERT INTO spa_metrics VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', data)
        
        conn.commit()
        logging.info(f"Successfully logged spa metrics at {current_time}")
        
    except Exception as e:
        logging.error(f"Error logging spa metrics: {e}")
        raise
    finally:
        if conn:
            conn.close()

def main():
    """Main function to create database and log spa metrics."""
    try:
        create_database()
        log_spa_metrics()
    except Exception as e:
        logging.error(f"Unexpected error in main: {e}")
        raise

if __name__ == "__main__":
    main() 
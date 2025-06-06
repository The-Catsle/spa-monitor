#!/usr/bin/env python3

import argparse
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
import plotext as plt
from pint import UnitRegistry

# Database configuration
DB_FILE = str(Path(__file__).parent / 'spa_metrics.db')

# Metric mapping (short names to database columns)
METRICS = {
    'temp': 'temperatureF',
    'setpoint': 'setpointF',
    'ph': 'ph',
    'orp': 'orp'
}

def parse_time_span(time_str):
    """Parse time span string (e.g., '24h', '1d') into hours."""
    ureg = UnitRegistry()
    time = ureg.Quantity(time_str)
    return time.to('hours').magnitude

def get_metric_data(metric, hours_back):
    """Retrieve metric data from the database for the specified time period."""
    if metric not in METRICS:
        raise ValueError(f"Invalid metric. Choose from: {', '.join(METRICS.keys())}")
    
    db_column = METRICS[metric]
    cutoff_time = datetime.now() - timedelta(hours=hours_back)
    
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        query = f'''
            SELECT timestamp, {db_column}
            FROM spa_metrics
            WHERE timestamp >= ?
            ORDER BY timestamp
        '''
        
        cursor.execute(query, (cutoff_time,))
        all_data = cursor.fetchall()
        cleaned_data = []
        for row in all_data:
            # format the timestamp to a datetime object
            str_date = datetime.fromisoformat(row[0]).strftime('%d/%m/%Y %H:%M:%S')
            cleaned_data.append((datetime.fromisoformat(row[0]), row[1]))
        return cleaned_data
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []
    finally:
        if conn:
            conn.close()

def plot_metric(metric, time_span):
    """Plot the specified metric over the given time span."""
    hours_back = parse_time_span(time_span)
    data = get_metric_data(metric, hours_back)
    
    if not data:
        print("No data found for the specified time period")
        return
    
    timestamps, values = zip(*data)
    # Convert datetime objects to timestamps (seconds since epoch)
    timestamps = [ts.timestamp() for ts in timestamps]
    
    plt.clf()
    plt.plot(timestamps, values)
    plt.title(f"{metric.upper()} over the last {time_span}")
    plt.xlabel("Time")
    plt.ylabel(metric.upper())
    
    # Format x-axis with dates
    plt.date_form("%Y-%m-%d %H:%M:%S")
    
    plt.show()

def main():
    parser = argparse.ArgumentParser(description='Plot spa metrics from the database')
    parser.add_argument('--metric', '-m', choices=METRICS.keys(),
                      help='Metric to plot (temp, setpoint, ph, orp)')
    parser.add_argument('--time-span', '-t', type=str, default='24h',
                      help='Time span to plot (e.g., "24h", "1d"). Default: 24h')
    
    args = parser.parse_args()
    plot_metric(args.metric, args.time_span)

if __name__ == "__main__":
    main() 
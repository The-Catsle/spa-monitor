# Spa Monitor

A Python script that monitors your Arctic Spa's PH levels and sends push notifications via Pushover when levels are outside the acceptable range.

## Setup

1. Make the setup script executable and run it:
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

2. Create a `.env` file in the project directory with the following variables:
   ```
   SPA_API_TOKEN=your_spa_api_token
   PUSHOVER_API_TOKEN=your_pushover_api_token
   PUSHOVER_USER_KEY=your_pushover_user_key
   PUSHOVER_PRIORITY=0  # Optional, defaults to 0 (normal priority)
   PUSHOVER_TITLE="Spa Monitor"  # Optional, defaults to "Spa Monitor"
   ```

## Usage

To run the script manually:
```bash
source venv/bin/activate
python spa_monitor.py
```

To set up as a cron job, add an entry to your crontab:
```bash
# Example: Run every hour
0 * * * * cd /path/to/script && ./venv/bin/python spa_monitor.py
```

## Configuration

The script monitors PH levels and sends notifications when:
- PH < 7.0 (too low)
- PH > 7.4 (too high)

These thresholds can be modified in the `spa_monitor.py` file.

## Error Handling

The script will send push notifications for:
- PH levels outside acceptable range
- API connection errors
- Unexpected errors during execution 
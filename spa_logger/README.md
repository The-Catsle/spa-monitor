# Spa Logger

This script logs spa metrics to an SQLite database every 5 minutes. It uses the existing spa_monitor.py functionality to fetch the data.

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Ensure your .env file is in the parent directory with the necessary API tokens:
- SPA_API_TOKEN
- PUSHOVER_API_TOKEN (optional)
- PUSHOVER_USER_KEY (optional)
- CATSLE_SPA_SLACKBOT_TOKEN (optional)

## Usage

Run the script using the provided shell script:
```bash
./run_spa_logger.sh
```

To run every 5 minutes via cron, add this line to your crontab:
```
*/5 * * * * /path/to/spa_logger/run_spa_logger.sh
```

## Files

- `spa_logger.py`: Main script
- `run_spa_logger.sh`: Shell script to run the logger
- `spa_metrics.db`: SQLite database file (created automatically)
- `spa_logger.log`: Log file (created automatically)
- `requirements.txt`: Python dependencies

## Database Schema

The `spa_metrics` table stores the following fields:
- timestamp: When the measurement was taken
- connected: Spa connection status
- temperatureF: Current water temperature
- setpointF: Target temperature
- lights: Light status
- spaboy_connected: SpaBoy connection status
- spaboy_producing: SpaBoy production status
- ph: pH level
- ph_status: pH status
- orp: ORP level
- orp_status: ORP status
- pump1: Pump 1 status
- pump2: Pump 2 status
- filter_status: Filter status
- filtration_duration: Filtration duration
- filtration_frequency: Filtration frequency
- filter_suspension: Filter suspension status
- errors: Any error messages 
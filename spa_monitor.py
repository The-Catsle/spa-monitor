#!/usr/bin/env python3

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
SPA_API_URL = "https://api.myarcticspa.com/v2/spa/status"
SPA_API_TOKEN = os.getenv("SPA_API_TOKEN")
PUSHOVER_API_TOKEN = os.getenv("PUSHOVER_API_TOKEN")
PUSHOVER_USER_KEY = os.getenv("PUSHOVER_USER_KEY")
PUSHOVER_PRIORITY = int(os.getenv("PUSHOVER_PRIORITY", "0"))  # Default to normal priority
PUSHOVER_TITLE = os.getenv("PUSHOVER_TITLE", "Spa Monitor")

# PH thresholds
PH_MIN = 7.0
PH_MAX = 7.4

def get_spa_status():
    """Get the current status of the spa."""
    headers = {"X-API-KEY": SPA_API_TOKEN}
    response = requests.get(SPA_API_URL, headers=headers)
    response.raise_for_status()
    return response.json()

def send_pushover_notification(message):
    """Send a notification via Pushover."""
    data = {
        "token": PUSHOVER_API_TOKEN,
        "user": PUSHOVER_USER_KEY,
        "message": message,
        "title": PUSHOVER_TITLE,
        "priority": PUSHOVER_PRIORITY
    }
    response = requests.post("https://api.pushover.net/1/messages.json", data=data)
    response.raise_for_status()

def check_ph_levels(status):
    """Check PH levels and send notification if outside acceptable range."""
    ph = status.get("ph")
    if ph is None:
        message = "No PH returned from request"
    elif ph < PH_MIN:
        message = f"Warning: Spa PH is too low ({ph:.2f}). Aim for 7.2"
    elif ph > PH_MAX:
        message = f"Warning: Spa PH is too high ({ph:.2f}). Aim for 7.2"
    else:
        message = f"Spa PH is good ({ph:.2f})."

    send_pushover_notification(message)


def main():
    """Main function to check spa status and send notifications if needed."""
    try:
        status = get_spa_status()
        check_ph_levels(status)
    except requests.exceptions.RequestException as e:
        error_message = f"Error checking spa status: {str(e)}"
        send_pushover_notification(error_message)
    except Exception as e:
        error_message = f"Unexpected error: {str(e)}"
        send_pushover_notification(error_message)

if __name__ == "__main__":
    main()

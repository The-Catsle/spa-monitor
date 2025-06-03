#!/bin/bash

cd /home/paul/git/catsle_cub_alerts/spa_logger

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install requirements
python3 -m pip install -r requirements.txt

# Run the spa logger
python3 spa_logger.py 
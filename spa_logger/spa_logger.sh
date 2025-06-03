#!/bin/bash

cd /home/paul/catsle_cub_alerts/spa_logger

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Run the spa logger
python3 spa_logger.py 
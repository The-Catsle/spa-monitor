#!/bin/bash

cd /home/paul/catsle_cub_alerts

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

python spa_monitor.py


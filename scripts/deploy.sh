#!/bin/bash

echo "🚀 Launching Tezus..."

# Activate virtual environment
source venv/bin/activate

# Initialize database
python3 database/schema.py

# Start main script
python3 main.py

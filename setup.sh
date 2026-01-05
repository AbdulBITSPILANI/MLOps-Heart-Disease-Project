#!/bin/bash
# Setup script for MLOps Project

echo "Setting up MLOps Project..."

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir -p data/raw data/processed models mlruns screenshots

# Download dataset
echo "Downloading dataset..."
python src/data/download_data.py

echo "Setup complete!"
echo "To activate the virtual environment, run: source venv/bin/activate"



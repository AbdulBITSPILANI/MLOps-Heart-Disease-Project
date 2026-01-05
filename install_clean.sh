#!/bin/bash
# Clean installation script for Linux/Mac
# This creates a fresh virtual environment and installs dependencies

echo "Creating fresh virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "Upgrading pip..."
python -m pip install --upgrade pip setuptools wheel

echo "Installing project dependencies..."
pip install -r requirements.txt

echo ""
echo "Installation complete!"
echo ""
echo "To activate the virtual environment, run:"
echo "  source venv/bin/activate"
echo ""
echo "To verify installation, run:"
echo "  python -c \"import pandas, numpy, sklearn, mlflow, fastapi; print('All dependencies OK')\""



@echo off
REM Setup script for MLOps Project (Windows)

echo Setting up MLOps Project...

REM Create virtual environment
python -m venv venv
call venv\Scripts\activate.bat

REM Upgrade pip
python -m pip install --upgrade pip

REM Install dependencies
pip install -r requirements.txt

REM Create necessary directories
if not exist "data\raw" mkdir data\raw
if not exist "data\processed" mkdir data\processed
if not exist "models" mkdir models
if not exist "mlruns" mkdir mlruns
if not exist "screenshots" mkdir screenshots

REM Download dataset
echo Downloading dataset...
python src\data\download_data.py

echo Setup complete!
echo To activate the virtual environment, run: venv\Scripts\activate.bat



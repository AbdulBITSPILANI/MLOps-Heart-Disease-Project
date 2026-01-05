@echo off
REM Clean installation script for Windows
REM This creates a fresh virtual environment and installs dependencies

echo Creating fresh virtual environment...
python -m venv venv
call venv\Scripts\activate.bat

echo Upgrading pip...
python -m pip install --upgrade pip setuptools wheel

echo Installing project dependencies...
pip install -r requirements.txt

echo.
echo Installation complete!
echo.
echo To activate the virtual environment, run:
echo   venv\Scripts\activate.bat
echo.
echo To verify installation, run:
echo   python -c "import pandas, numpy, sklearn, mlflow, fastapi; print('All dependencies OK')"



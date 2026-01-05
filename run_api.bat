@echo off
REM Script to run the API server
REM Note: The API binds to 0.0.0.0:8000 but you access it via http://localhost:8000

echo Starting Heart Disease Prediction API...
echo.
echo The API will be available at:
echo   http://localhost:8000
echo   http://127.0.0.1:8000
echo.
echo API Documentation:
echo   http://localhost:8000/docs
echo   http://localhost:8000/redoc
echo.
echo Press Ctrl+C to stop the server
echo.

python src/api/main.py


@echo off
echo ========================================
echo AI Restaurant Recommender - Phase 5
echo ========================================
echo.
echo Starting Streamlit application...
echo.

REM Check if virtual environment exists
if exist "..\..\venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call ..\..\venv\Scripts\activate.bat
) else (
    echo Virtual environment not found at ..\..\venv
    echo Please create a virtual environment first:
    echo   python -m venv ..\..\venv
    echo   ..\..\venv\Scripts\activate
    echo   pip install -r requirements.txt
    pause
    exit /b
)

REM Check if streamlit is installed
python -c "import streamlit" 2>nul
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
)

REM Start the Streamlit app
echo.
echo Opening app in browser...
echo Press Ctrl+C to stop the server
echo.
streamlit run app.py

pause

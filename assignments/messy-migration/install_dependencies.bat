@echo off
echo Installing Python dependencies...
echo.

REM Try py launcher first (most reliable on Windows)
echo Trying py launcher...
py --version >nul 2>&1
if %errorlevel% equ 0 (
    echo Python found via py launcher!
    py -m pip install flask-bcrypt flask-limiter python-dotenv pytest
    goto :success
)

REM Try python command
echo Trying python command...
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo Python found via python command!
    python -m pip install flask-bcrypt flask-limiter python-dotenv pytest
    goto :success
)

REM Try full path based on your installation
echo Trying full path...
"C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python313\python.exe" --version >nul 2>&1
if %errorlevel% equ 0 (
    echo Python found via full path!
    "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python313\python.exe" -m pip install flask-bcrypt flask-limiter python-dotenv pytest
    goto :success
)

echo ERROR: Could not find Python. Please check installation.
pause
exit /b 1

:success
echo.
echo Dependencies installed successfully!
echo You can now run: python init_db.py
echo Then run: python app.py
pause
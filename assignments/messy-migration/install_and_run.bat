@echo off
echo Installing Python dependencies...

REM Try different Python/pip commands
python -m pip install flask-bcrypt flask-limiter python-dotenv pytest
if %errorlevel% neq 0 (
    echo Trying py -m pip...
    py -m pip install flask-bcrypt flask-limiter python-dotenv pytest
    if %errorlevel% neq 0 (
        echo Trying python3 -m pip...
        python3 -m pip install flask-bcrypt flask-limiter python-dotenv pytest
        if %errorlevel% neq 0 (
            echo ERROR: Could not install dependencies. Please check Python installation.
            pause
            exit /b 1
        )
    )
)

echo Dependencies installed successfully!
echo.
echo Initializing database...
python init_db.py
if %errorlevel% neq 0 (
    py init_db.py
    if %errorlevel% neq 0 (
        python3 init_db.py
    )
)

echo.
echo Starting application...
python app.py
if %errorlevel% neq 0 (
    py app.py
    if %errorlevel% neq 0 (
        python3 app.py
    )
)

pause
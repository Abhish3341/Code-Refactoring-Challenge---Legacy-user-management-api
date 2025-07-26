@echo off
echo Fixing Python PATH issue...
echo.

echo Method 1: Trying py launcher...
py --version
if %errorlevel% equ 0 (
    echo Python found via py launcher!
    echo Installing dependencies...
    py -m pip install flask-bcrypt flask-limiter python-dotenv pytest
    if %errorlevel% equ 0 (
        echo Dependencies installed successfully!
        echo Initializing database...
        py init_db.py
        echo Starting application...
        py app.py
        goto :end
    )
)

echo.
echo Method 2: Trying full path...
"C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python313\python.exe" --version
if %errorlevel% equ 0 (
    echo Python found via full path!
    echo Installing dependencies...
    "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python313\python.exe" -m pip install flask-bcrypt flask-limiter python-dotenv pytest
    if %errorlevel% equ 0 (
        echo Dependencies installed successfully!
        echo Initializing database...
        "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python313\python.exe" init_db.py
        echo Starting application...
        "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python313\python.exe" app.py
        goto :end
    )
)

echo.
echo Method 3: Trying alternative paths...
for %%i in (
    "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python3*\python.exe"
    "C:\Python3*\python.exe"
    "C:\Program Files\Python3*\python.exe"
) do (
    if exist "%%i" (
        echo Found Python at: %%i
        "%%i" --version
        "%%i" -m pip install flask-bcrypt flask-limiter python-dotenv pytest
        if %errorlevel% equ 0 (
            echo Dependencies installed successfully!
            "%%i" init_db.py
            "%%i" app.py
            goto :end
        )
    )
)

echo.
echo ERROR: Could not find Python installation.
echo Please follow the manual PATH fix instructions.

:end
pause
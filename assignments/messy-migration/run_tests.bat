@echo off
echo Running tests...

python -m pytest tests/ -v
if %errorlevel% neq 0 (
    echo Trying py -m pytest...
    py -m pytest tests/ -v
    if %errorlevel% neq 0 (
        echo Trying python3 -m pytest...
        python3 -m pytest tests/ -v
    )
)

pause
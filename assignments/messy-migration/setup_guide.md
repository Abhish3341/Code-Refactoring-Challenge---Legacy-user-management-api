# Python Installation and Setup Guide

## Issue: 'pip' is not recognized

This error means Python/pip is not properly installed or not in your system PATH.

## Solution Steps:

### Step 1: Verify Python Installation
Open Command Prompt (cmd) or PowerShell and try these commands:

```bash
python --version
python3 --version
py --version
```

If none work, Python isn't properly installed.

### Step 2: Install Python Properly

#### Option A: Download from Official Site (Recommended)
1. Go to https://www.python.org/downloads/
2. Download Python 3.8+ for Windows
3. **IMPORTANT**: During installation, check "Add Python to PATH"
4. Choose "Install Now"

#### Option B: Using Windows Store Python
If you installed from Windows Store, try:
```bash
python -m pip install flask-bcrypt flask-limiter python-dotenv pytest
```

### Step 3: Alternative Installation Methods

#### If `pip` still doesn't work, try:
```bash
# Method 1: Using python -m pip
python -m pip install flask-bcrypt flask-limiter python-dotenv pytest

# Method 2: Using py launcher
py -m pip install flask-bcrypt flask-limiter python-dotenv pytest

# Method 3: Using python3
python3 -m pip install flask-bcrypt flask-limiter python-dotenv pytest
```

### Step 4: Fix PATH Issues (if needed)

If Python is installed but not in PATH:

1. Find your Python installation directory (usually):
   - `C:\Users\[YourUsername]\AppData\Local\Programs\Python\Python3x\`
   - `C:\Python3x\`

2. Add to PATH:
   - Press Win + R, type `sysdm.cpl`
   - Go to "Advanced" tab → "Environment Variables"
   - Under "System Variables", find "Path"
   - Add these paths:
     - `C:\Users\[YourUsername]\AppData\Local\Programs\Python\Python3x\`
     - `C:\Users\[YourUsername]\AppData\Local\Programs\Python\Python3x\Scripts\`

3. Restart Command Prompt/PowerShell

### Step 5: Verify Installation
```bash
pip --version
python --version
```

## Quick Fix for This Project

If you're still having issues, create a batch file to run the project:
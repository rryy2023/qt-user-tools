@echo off
REM Windows EXE Packaging Script
REM Use GBK encoding for Windows compatibility

echo ========================================
echo Windows EXE Packaging Script
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found, please install Python first
    pause
    exit /b 1
)

echo [OK] Python detected
python --version

REM Check PyInstaller
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo.
    echo [WARN] PyInstaller not installed
    echo Installing PyInstaller...
    pip install pyinstaller
    if errorlevel 1 (
        echo [ERROR] PyInstaller installation failed
        pause
        exit /b 1
    )
)

echo [OK] PyInstaller installed

REM Check dependencies
echo.
echo Checking dependencies...
python -c "import PyQt6" >nul 2>&1
if errorlevel 1 (
    echo [WARN] Missing dependencies, installing...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] Dependency installation failed
        pause
        exit /b 1
    )
)

echo [OK] Dependencies checked

REM Run packaging script
echo.
echo Starting packaging...
python build_windows.py

if errorlevel 1 (
    echo.
    echo [ERROR] Packaging failed
    pause
    exit /b 1
)

echo.
echo ========================================
echo Packaging completed!
echo ========================================
echo.
echo Output file naming convention:
echo   EXE: QiantuTroubleshooter_v0.0.1_Windows-x64.exe
echo   ZIP: QiantuTroubleshooter_v0.0.1_Windows-x64.zip
echo.
pause

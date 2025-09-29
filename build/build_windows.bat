@echo off
REM Windows build script for Exiles Installer
REM Run this on a Windows machine with Python and PyInstaller installed

echo === Building Exiles Installer for Windows ===
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ from python.org
    pause
    exit /b 1
)

REM Install PyInstaller if not present
echo Installing PyInstaller...
pip install pyinstaller
echo.

REM Create the executable
echo Building executable...
pyinstaller --onefile --windowed --name=ExilesInstaller --add-data=../src/apps.json;. --hidden-import=tkinter.ttk --hidden-import=requests --clean --distpath=../dist ../src/main.py

if exist "../dist/ExilesInstaller.exe" (
    echo.
    echo === Build Complete ===
    echo Success! ExilesInstaller.exe has been created in the dist folder.
    echo This single file contains everything needed to install Elite Dangerous applications.
    echo.
    echo File location: dist/ExilesInstaller.exe
    for %%I in ("../dist/ExilesInstaller.exe") do echo File size: %%~zI bytes
    echo.
    echo You can now distribute this single executable file to users!
) else (
    echo.
    echo === Build Failed ===
    echo The executable was not created. Please check the error messages above.
)

echo.
pause
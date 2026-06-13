@echo off
setlocal ENABLEEXTENSIONS

cd /d "%~dp0"

set VENV_DIR=.venv
set PYTHON_EXE=

REM Prefer normal Python if available
python --version >nul 2>&1
if not errorlevel 1 (
    set PYTHON_EXE=python
)

REM Fallback: common official Python install location
if "%PYTHON_EXE%"=="" (
    if exist "%LOCALAPPDATA%\Programs\Python\Python314\python.exe" (
        set PYTHON_EXE=%LOCALAPPDATA%\Programs\Python\Python314\python.exe
    )
)

REM If Python still was not found, show help
if "%PYTHON_EXE%"=="" (
    echo.
    echo ==========================================
    echo THE SCRATCH REQUIRES PYTHON
    echo ==========================================
    echo.
    echo Python was not found on this computer.
    echo.
    echo Download Python from:
    echo https://www.python.org/downloads/
    echo.
    start https://www.python.org/downloads/
    echo.
    pause
    exit /b
)

if not exist "%VENV_DIR%\Scripts\python.exe" (
    "%PYTHON_EXE%" -m venv "%VENV_DIR%"
)

"%VENV_DIR%\Scripts\python.exe" -m ensurepip --upgrade >nul 2>&1

if exist requirements.txt (
    "%VENV_DIR%\Scripts\python.exe" -m pip install -r requirements.txt
)

"%VENV_DIR%\Scripts\python.exe" -m ui.app

echo.
echo Press any key to close...
pause

endlocal
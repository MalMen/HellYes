@echo off
REM Build script for Windows executable
REM This creates a standalone executable that doesn't require Python installation

echo ========================================
echo HellShared Auto Processor - Windows Build
echo ========================================
echo.

REM Check if PyInstaller is installed
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo PyInstaller not found. Installing...
    python -m pip install pyinstaller
    if errorlevel 1 (
        echo ERROR: Failed to install PyInstaller
        echo Please install it manually: pip install pyinstaller
        pause
        exit /b 1
    )
)

echo.
echo Cleaning previous build...
echo Checking if HellSharedAutoProcessor.exe is running...
taskkill /F /IM HellSharedAutoProcessor.exe 2>nul
timeout /t 2 /nobreak >nul

if exist build rmdir /s /q build 2>nul
if exist dist\HellSharedAutoProcessor.exe (
    echo Removing old executable...
    del /f /q dist\HellSharedAutoProcessor.exe 2>nul
    if exist dist\HellSharedAutoProcessor.exe (
        echo WARNING: Could not delete dist\HellSharedAutoProcessor.exe
        echo Please close the application and any file explorers viewing it, then try again.
        pause
        exit /b 1
    )
)
if exist dist\HellSharedAutoProcessor rmdir /s /q dist\HellSharedAutoProcessor 2>nul

echo.
echo Building main application executable...
REM Try to run pyinstaller directly first
pyinstaller --clean allhell3_auto_processor_onefile.spec 2>nul
if errorlevel 1 (
    echo PyInstaller command not found in PATH, trying alternative method...
    REM If that fails, try using python -m PyInstaller
    python -m PyInstaller --clean allhell3_auto_processor_onefile.spec
    if errorlevel 1 (
        echo.
        echo ERROR: Main application build failed!
        pause
        exit /b 1
    )
)

echo.
echo Building native messaging host for browser extension...
pyinstaller --clean native_host.spec 2>nul
if errorlevel 1 (
    python -m PyInstaller --clean native_host.spec
    if errorlevel 1 (
        echo.
        echo ERROR: Native host build failed!
        pause
        exit /b 1
    )
)

echo.
echo ========================================
echo Build completed successfully!
echo ========================================
echo.
echo Built executables:
echo   1. dist\HellSharedAutoProcessor.exe     (Main application)
echo   2. dist\HellSharedNativeHost.exe        (Browser extension host)
echo.
echo Main Application:
echo - All Python dependencies included
echo - allhell3.py bundled
echo - dependency_installer_gui.py bundled
echo - install/ scripts bundled
echo - Application icon embedded in .exe
echo.
echo Native Host:
echo - Communicates with browser extension
echo - Creates JSON files in pending\ folder
echo - Automatically registered during dependency installation
echo.
echo Distribution files:
echo   dist\
echo   ├── HellSharedAutoProcessor.exe       ← Main app
echo   └── HellSharedNativeHost.exe          ← Browser host
echo.
echo IMPORTANT: Users still need:
echo - device.wvd file (place in same directory as exe)
echo - N_m3u8DL-RE.exe (in bin\ subdirectory or system PATH)
echo.
pause

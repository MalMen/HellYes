#!/bin/bash
# Build script for Linux executable
# This creates a standalone executable that doesn't require Python installation

echo "========================================"
echo "HellShared Auto Processor - Linux Build"
echo "========================================"
echo

# Check if PyInstaller is installed
if ! python3 -c "import PyInstaller" 2>/dev/null; then
    echo "PyInstaller not found. Installing..."
    python3 -m pip install pyinstaller
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install PyInstaller"
        echo "Please install it manually: pip3 install pyinstaller"
        exit 1
    fi
fi

echo
echo "Cleaning previous build..."
rm -rf build dist/HellSharedAutoProcessor

echo
echo "Building main application executable..."
pyinstaller --clean allhell3_auto_processor_onefile.spec

if [ $? -ne 0 ]; then
    echo
    echo "ERROR: Main application build failed!"
    exit 1
fi

echo
echo "Building native messaging host for browser extension..."
pyinstaller --clean native_host.spec

if [ $? -ne 0 ]; then
    echo
    echo "ERROR: Native host build failed!"
    exit 1
fi

echo
echo "========================================"
echo "Build completed successfully!"
echo "========================================"
echo
echo "Built executables:"
echo "  1. dist/HellSharedAutoProcessor         (Main application)"
echo "  2. dist/HellSharedNativeHost            (Browser extension host)"
echo
echo "Main Application:"
echo "- All Python dependencies included"
echo "- allhell3.py bundled"
echo "- dependency_installer_gui.py bundled"
echo "- install/ scripts bundled"
echo
echo "Native Host:"
echo "- Communicates with browser extension"
echo "- Creates JSON files in pending/ folder"
echo "- Automatically registered during dependency installation"
echo
echo "Distribution files:"
echo "  dist/"
echo "  ├── HellSharedAutoProcessor       ← Main app"
echo "  └── HellSharedNativeHost          ← Browser host"
echo
echo "You can now:"
echo "1. Copy both executables to any Linux machine"
echo "2. Run ./HellSharedAutoProcessor (no Python installation required)"
echo "3. Make executables if needed: chmod +x HellSharedAutoProcessor HellSharedNativeHost"
echo
echo "IMPORTANT: Users still need:"
echo "- device.wvd file (place in same directory as executable)"
echo "- N_m3u8DL-RE (in bin/ subdirectory or system PATH)"
echo

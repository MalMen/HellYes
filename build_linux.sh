#!/bin/bash
# Build script for Linux executable
# This creates a standalone executable that doesn't require Python installation

echo "========================================"
echo "HellShared Auto Processor - Linux Build"
echo "========================================"
echo

# Try to setup virtual environment, fallback to system Python if it fails
VENV_DIR="venv"
USE_VENV=true

# Check if venv exists and is valid
if [ ! -f "$VENV_DIR/bin/activate" ]; then
    echo "Creating virtual environment..."
    # Remove broken venv if exists
    rm -rf "$VENV_DIR"
    if python3 -m venv "$VENV_DIR" 2>/dev/null; then
        echo "Virtual environment created successfully"
    else
        echo "WARNING: Failed to create virtual environment (filesystem may not support symlinks)"
        echo "Falling back to system Python with --break-system-packages"
        USE_VENV=false
        rm -rf "$VENV_DIR"  # Clean up broken venv
    fi
fi

if [ "$USE_VENV" = true ]; then
    # Activate virtual environment
    echo "Activating virtual environment..."
    source "$VENV_DIR/bin/activate"

    # Check if PyInstaller is installed in venv
    if ! python -c "import PyInstaller" 2>/dev/null; then
        echo "Installing PyInstaller in virtual environment..."
        pip install pyinstaller
        if [ $? -ne 0 ]; then
            echo "ERROR: Failed to install PyInstaller"
            deactivate
            exit 1
        fi
    fi

    # Install project dependencies if requirements.txt exists
    if [ -f "requirements.txt" ]; then
        echo "Installing project dependencies..."
        pip install -r requirements.txt -q
    fi
else
    # Use system Python with --break-system-packages
    # Add user's local bin to PATH
    export PATH="$HOME/.local/bin:$PATH"

    if ! python3 -c "import PyInstaller" 2>/dev/null; then
        echo "Installing PyInstaller with --break-system-packages..."
        python3 -m pip install --break-system-packages pyinstaller
        if [ $? -ne 0 ]; then
            echo "ERROR: Failed to install PyInstaller"
            exit 1
        fi
    fi

    # Install project dependencies if requirements.txt exists
    if [ -f "requirements.txt" ]; then
        echo "Installing project dependencies with --break-system-packages..."
        python3 -m pip install --break-system-packages -r requirements.txt -q
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
    [ "$USE_VENV" = true ] && deactivate
    exit 1
fi

echo
echo "Building native messaging host for browser extension..."
pyinstaller --clean native_host.spec

if [ $? -ne 0 ]; then
    echo
    echo "ERROR: Native host build failed!"
    [ "$USE_VENV" = true ] && deactivate
    exit 1
fi

# Deactivate virtual environment if using one
[ "$USE_VENV" = true ] && deactivate

echo
echo "Installing icon for Linux desktop integration..."
# Install icon to user's local icon directory
ICON_DIR="$HOME/.local/share/icons/hicolor"
mkdir -p "$ICON_DIR/256x256/apps"

if [ -f "browser-extension/logo/hellyes_original.png" ]; then
    cp browser-extension/logo/hellyes_original.png "$ICON_DIR/256x256/apps/hellyes.png"
    echo "✓ Icon installed to $ICON_DIR/256x256/apps/hellyes.png"

    # Update icon cache if available
    if command -v gtk-update-icon-cache &> /dev/null; then
        gtk-update-icon-cache -f -t "$ICON_DIR" 2>/dev/null || true
    fi
else
    echo "⚠ Warning: Icon file not found, skipping icon installation"
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
echo "- Application icon configured"
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
echo "1. Run: ./dist/HellSharedAutoProcessor"
echo "2. Copy both executables to any Linux machine"
echo "3. Window icon automatically loads from bundled resources"
echo
echo "IMPORTANT: Users still need:"
echo "- device.wvd file (place in same directory as executable)"
echo "- N_m3u8DL-RE (in bin/ subdirectory or system PATH)"
echo

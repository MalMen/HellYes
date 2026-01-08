# Building HellYes from Source

This guide explains how to build the HellSharedAutoProcessor executables and browser extensions from source.

## Table of Contents
- [Quick Start](#quick-start)
- [Building Executables](#building-executables)
- [Building Browser Extensions](#building-browser-extensions)
- [GitHub Actions (Automated Builds)](#github-actions-automated-builds)
- [Distribution](#distribution)
- [Troubleshooting](#troubleshooting)

---

## Quick Start

### Windows
```cmd
build_windows.bat
```

### Linux
```bash
./build_linux.sh
```

---

## Building Executables

The build process creates standalone executables that don't require Python installation on the target system.

### Prerequisites

#### Windows
- **Python 3.8+** (with pip)
- **PyInstaller** (auto-installed by build script)
- **Pillow** (auto-installed by build script)

#### Linux
- **Python 3.8+** (with pip)
- **PyInstaller** (auto-installed by build script)
- **Pillow** (auto-installed by build script)
- **Virtual environment support** (optional, script falls back to system Python if unavailable)

### Build Process

#### Windows

1. Open Command Prompt or PowerShell
2. Navigate to the HellYes directory
3. Run the build script:
   ```cmd
   build_windows.bat
   ```

**What the script does:**
- Checks/installs PyInstaller if needed
- Kills any running instances of the app
- Cleans previous build artifacts
- Creates icon file (`hellyes.ico`) from `hellyes_original.png`
- Builds main application using `allhell3_auto_processor_onefile.spec`
- Builds native host using `native_host.spec`

**Output:**
- `dist/HellSharedAutoProcessor.exe` - Main GUI application
- `dist/HellSharedNativeHost.exe` - Browser extension native messaging host

#### Linux

1. Open terminal
2. Navigate to the HellYes directory
3. Make the script executable (first time only):
   ```bash
   chmod +x build_linux.sh
   ```
4. Run the build script:
   ```bash
   ./build_linux.sh
   ```

**What the script does:**
- Attempts to create/use virtual environment (falls back to system Python if unavailable)
- Checks/installs PyInstaller if needed
- Cleans previous build artifacts
- Creates icon file (`hellyes.ico`) from `hellyes_original.png`
- Builds main application using `allhell3_auto_processor_onefile.spec`
- Builds native host using `native_host.spec`
- Installs icon to `~/.local/share/icons/hicolor/256x256/apps/hellyes.png`
- Updates system icon cache (if `gtk-update-icon-cache` available)

**Output:**
- `dist/HellSharedAutoProcessor` - Main GUI application
- `dist/HellSharedNativeHost` - Browser extension native messaging host

### What Gets Bundled

The executables include:
- ✅ All Python dependencies
- ✅ `allhell3.py` (core download script)
- ✅ `dependency_installer_gui.py` (dependency checker/installer)
- ✅ All `install/` scripts (browser manifest installers, etc.)
- ✅ Application icon resources
- ✅ Browser extension logo assets

### What Users Still Need

The executables are **not fully standalone**. Users need:
- **device.wvd** - Widevine CDM file (or `client_id.bin` + `private_key.pem` to generate it)
- **N_m3u8DL-RE** or **dash-mpd-cli** - Video downloader (in `bin/` subdirectory or system PATH)
- **FFmpeg** - Video processing (usually in system PATH)
- **MKVToolNix** (mkvmerge) - For merging video/audio (optional)
- **Bento4** (mp4decrypt) - For decryption (optional, depends on workflow)

The included dependency installer GUI checks for these and guides users through installation.

---

## Building Browser Extensions

### Prerequisites

- **Node.js 18+** (with npm/npx)
- **Chrome Extension Key** (for signing CRX)
- **Firefox API Credentials** (for signing XPI)

### Chrome/Edge/Brave Extension

#### Option 1: Source Distribution (Developer Mode)
```bash
cd browser-extension
zip -r ../hellyes-chrome-source.zip . -x "*.DS_Store" -x "__MACOSX/*"
```

Users install this by:
1. Extract to permanent location
2. Go to `chrome://extensions`
3. Enable "Developer mode"
4. Click "Load unpacked"
5. Select the extracted folder

#### Option 2: Signed CRX (Advanced)
```bash
# Create private key (first time only)
# Save this securely! You need it for updates.
openssl genrsa -out private.pem 2048

# Pack extension
npx crx3 pack browser-extension -p private.pem

# This creates web-extension.crx
```

**Note:** CRX files may show security warnings in browsers if not distributed through Chrome Web Store.

### Firefox Extension

Requires Firefox Add-on credentials:

```bash
npx web-ext sign -s browser-extension \
  --artifacts-dir firefox-artifacts \
  --channel unlisted \
  --api-key YOUR_ISSUER_KEY \
  --api-secret YOUR_SECRET
```

This creates a signed `.xpi` file that users can install directly.

---

## GitHub Actions (Automated Builds)

The repository includes automated builds via GitHub Actions.

### Workflow: `build-and-release.yml`

Triggered on:
- Push to `main` or `feat/*` branches
- Manual workflow dispatch

### What Gets Built

1. **Version Calculation**
   - Checks existing git tags (format: `0.0.X`)
   - Increments patch version automatically
   - Ensures no version conflicts

2. **Chrome Extension**
   - `hellyes-chrome-source.zip` - Source for developer mode
   - `hellyes-chrome-crx.zip` - Signed CRX

3. **Firefox Extension**
   - `hellyes-firefox.xpi` - Signed installable add-on

4. **Windows Executable**
   - `HellSharedAutoProcessor.win.zip` containing:
     - `HellSharedAutoProcessor.exe`
     - `HellSharedNativeHost.exe`
     - `README.md`, `LICENSE`, `BUILDING.md`

5. **Linux Executable**
   - `HellSharedAutoProcessor.linux.tar.gz` containing:
     - `HellSharedAutoProcessor` (executable)
     - `HellSharedNativeHost` (executable)
     - `README.md`, `LICENSE`, `BUILDING.md`

6. **GitHub Release**
   - Creates release with tag `0.0.X`
   - Attaches all 5 artifacts
   - Includes release notes

### Required Secrets

Configure these in GitHub Settings → Secrets:

- `PRIVATE_KEY` - Chrome extension private key (base64 or PEM format)
- `FIREFOX_ISSUER` - Firefox API issuer key
- `FIREFOX_SECRET` - Firefox API secret key
- `GITHUB_TOKEN` - Automatically provided by GitHub Actions

### Manual Trigger

You can manually trigger a build:
1. Go to Actions tab in GitHub
2. Select "Build and Release HellYes" workflow
3. Click "Run workflow"
4. Select branch
5. Click "Run workflow"

---

## Distribution

### Creating Distribution Packages

#### Windows Package

After building, create distribution archive:
```cmd
mkdir HellSharedAutoProcessor
copy dist\HellSharedAutoProcessor.exe HellSharedAutoProcessor\
copy dist\HellSharedNativeHost.exe HellSharedAutoProcessor\
copy README.md HellSharedAutoProcessor\
copy LICENSE HellSharedAutoProcessor\
copy BUILDING.md HellSharedAutoProcessor\
powershell Compress-Archive -Path HellSharedAutoProcessor -DestinationPath HellSharedAutoProcessor.win.zip
```

#### Linux Package

After building, create distribution archive:
```bash
mkdir -p HellSharedAutoProcessor
cp dist/HellSharedAutoProcessor HellSharedAutoProcessor/
cp dist/HellSharedNativeHost HellSharedAutoProcessor/
chmod +x HellSharedAutoProcessor/HellSharedAutoProcessor
chmod +x HellSharedAutoProcessor/HellSharedNativeHost
cp README.md LICENSE BUILDING.md HellSharedAutoProcessor/
tar -czf HellSharedAutoProcessor.linux.tar.gz HellSharedAutoProcessor
```

### Icon Handling

#### Windows
- Icon is **embedded** in `.exe` file during build
- File Explorer shows the icon
- Window/taskbar show the icon
- No additional files needed

#### Linux
- Icon is **bundled** in executable resources
- Window/taskbar show the icon at runtime
- System icon installed to `~/.local/share/icons/` during build (optional, for desktop integration)
- No additional files needed for distribution

---

## Troubleshooting

### Windows Build Issues

**Problem:** `Permission denied` when deleting `dist/HellSharedAutoProcessor.exe`

**Solution:**
1. Close any running instances of `HellSharedAutoProcessor.exe`
2. Close any File Explorer windows viewing the `dist/` folder
3. Run the build script again

The build script attempts to kill running processes automatically, but Windows may lock files if they're being viewed.

---

**Problem:** `PyInstaller not found`

**Solution:**
```cmd
python -m pip install --upgrade pyinstaller
```

---

**Problem:** `No module named 'PIL'`

**Solution:**
```cmd
python -m pip install Pillow
```

---

### Linux Build Issues

**Problem:** `Failed to create virtual environment (filesystem may not support symlinks)`

**Solution:**
The script automatically falls back to system Python with `--break-system-packages`. This is common on certain filesystems (like FAT32, network drives, or Docker volumes).

---

**Problem:** `gtk-update-icon-cache: command not found`

**Solution:**
This is a warning, not an error. The icon is still installed, but the cache isn't updated. Install GTK+ development tools:
```bash
# Ubuntu/Debian
sudo apt install libgtk-3-dev

# Fedora
sudo dnf install gtk3-devel

# Arch
sudo pacman -S gtk3
```

---

**Problem:** Build succeeds but executable doesn't run

**Solution:**
Check dependencies with:
```bash
ldd dist/HellSharedAutoProcessor
```

Most issues are missing shared libraries. The build creates a standalone executable, but some system libraries (like glibc) are still required.

---

### Browser Extension Issues

**Problem:** Firefox rejects signed extension

**Solution:**
- Verify your API credentials are correct
- Check that manifest version is incremented
- Ensure you're signing as "unlisted" (not "listed")
- Firefox rejects duplicate version numbers

---

**Problem:** Chrome shows "Package is invalid: CRX_REQUIRED_PROOF_MISSING"

**Solution:**
This is expected for CRX files not from Chrome Web Store. Users should use the source distribution and load in developer mode instead.

---

### GitHub Actions Issues

**Problem:** Windows job fails with PowerShell syntax error

**Solution:**
Ensure any shell commands use `shell: cmd` for Windows batch syntax:
```yaml
- name: Step name
  shell: cmd
  run: |
    if exist file.txt echo found
```

---

**Problem:** Version number conflict (Firefox: "Version 0.0.X already exists")

**Solution:**
The workflow now uses git tag-based versioning to prevent conflicts. If you see this error:
1. Check existing git tags: `git tag -l "0.0.*"`
2. The workflow should auto-increment, but you can manually create a new tag if needed:
   ```bash
   git tag 0.0.X
   git push origin 0.0.X
   ```

---

## Additional Notes

### PyInstaller Spec Files

The build uses two spec files:

1. **`allhell3_auto_processor_onefile.spec`**
   - Creates single-file executable
   - Bundles all dependencies
   - Includes icon and resources

2. **`native_host.spec`**
   - Creates native messaging host
   - Smaller, focused executable
   - Handles browser ↔ Python communication

You can customize these files to:
- Add/remove bundled resources
- Change executable name
- Modify icon paths
- Exclude unnecessary modules

### Icon Requirements

- **Source:** `browser-extension/logo/hellyes_original.png` (1024x1024 recommended)
- **Windows:** Converted to `hellyes.ico` (multi-resolution)
- **Linux:** Used directly as PNG

The build scripts handle conversion automatically using Pillow.

---

## Questions?

For issues or questions about building:
1. Check the [main README](README.md)
2. Review build script output for specific errors
3. Open an issue on GitHub with build logs

---

**Happy building!**

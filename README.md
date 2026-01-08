# HellYes

A Widevine Downloader with multi-browser support for Linux and Windows
======================================================================

## Overview

HellYes is a powerful tool for downloading DRM-protected content using Widevine L3. This repository extends the original [vinefeeder/HellYes](https://github.com/vinefeeder/HellYes) project by adding:

- **Browser Extension** - Automatically captures MPD URLs and license requests
- **Native Host Application** - Seamless communication between browser and Python scripts
- **Automated Installer** - Guided setup for all dependencies and configurations
- **Multi-Browser Support** - Works with Chrome, Firefox, Edge, and Brave on both Linux and Windows

Instead of manually hunting through browser DevTools for MPD URLs and cURL commands, the HellYes browser extension does this automatically and sends the data directly to the download script.

## Installation

### Quick Start (Recommended)

Download the latest release from the [Releases page](https://github.com/MalMen/HellYes/releases):

#### Windows
1. Download `HellSharedAutoProcessor.win.zip`
2. Extract to your desired location
3. Run `HellSharedAutoProcessor.exe`
4. Follow the guided installer to:
   - Check and install required dependencies
   - Configure browser extension support
   - Set up the native messaging host

#### Linux
1. Download `HellSharedAutoProcessor.linux.tar.gz`
2. Extract: `tar -xzf HellSharedAutoProcessor.linux.tar.gz`
3. Navigate to the directory: `cd HellSharedAutoProcessor`
4. Run: `./HellSharedAutoProcessor`
5. Follow the guided installer to:
   - Check and install required dependencies
   - Configure browser extension support
   - Set up the native messaging host

### Browser Extension Installation

After running the installer, install the browser extension:

#### Chrome/Edge/Brave

**Note:** The HellYes extension is not available on the Chrome Web Store. You must install it manually in developer mode.

1. Download `hellyes-chrome-source.zip` from the [Releases page](https://github.com/MalMen/HellYes/releases)
2. Extract the ZIP file to a **permanent location** (don't delete this folder after installation)
3. Open your browser and navigate to:
   - Chrome: `chrome://extensions`
   - Edge: `edge://extensions`
   - Brave: `brave://extensions`
4. Enable "Developer mode" (toggle in top-right corner)
5. Click "Load unpacked"
6. Select the extracted folder containing the extension files

**Important:** Keep the extension folder in place. If you delete it, the extension will stop working.

**Alternative:** If you have issues with developer mode, you can try `hellyes-chrome-crx.zip` (signed version), but your browser may show security warnings.

#### Firefox
1. Download `hellyes-firefox.xpi` from the [Releases page](https://github.com/MalMen/HellYes/releases)
2. Open Firefox and navigate to `about:addons`
3. Click the gear icon and select "Install Add-on From File..."
4. Select the downloaded `hellyes-firefox.xpi` file
5. Confirm the installation when prompted

### Manual Build (Advanced)

If you prefer to build from source:

#### Windows
```batch
build_windows.bat
```

#### Linux
```bash
./build_linux.sh
```

See [BUILDING.md](BUILDING.md) for detailed build instructions.

## How It Works

### Architecture

```
┌─────────────────┐
│  Browser Tab    │
│  (Website with  │
│   DRM content)  │
└────────┬────────┘
         │
         │ Intercepts network requests
         ↓
┌─────────────────┐
│ HellYes Browser │
│   Extension     │
│ (Captures MPD & │
│  License data)  │
└────────┬────────┘
         │
         │ Native Messaging Protocol
         ↓
┌─────────────────┐
│ Native Host     │
│ (Message Relay) │
└────────┬────────┘
         │
         │ JSON-RPC
         ↓
┌─────────────────┐
│ HellYes Python  │
│     Script      │
│ (Downloads DRM  │
│    content)     │
└─────────────────┘
```

### What the Extension Does

The HellYes browser extension monitors network traffic in your browser and automatically:

1. **Detects MPD URLs** - Identifies MPEG-DASH manifest files (`.mpd` extensions)
2. **Captures License Requests** - Intercepts Widevine license server requests
3. **Extracts Headers** - Records authentication cookies and headers
4. **Sends to Script** - Packages all data and sends it to the Python script via native messaging

This eliminates the need to manually:
- Open browser DevTools
- Set up network filters
- Copy MPD URLs
- Copy cURL commands for license requests

## Usage

### Step 1: Start the Application

Run `HellSharedAutoProcessor` (or `HellSharedAutoProcessor.exe` on Windows).

The GUI will appear, ready to receive data from the browser extension.

### Step 2: Browse to DRM-Protected Content

1. Open your browser with the HellYes extension installed
2. Navigate to a website with DRM-protected video content
3. Start playing the video (or let it load)

### Step 3: Automatic Capture

The extension automatically:
- Detects the MPD manifest URL
- Captures the Widevine license request
- Sends all data to the HellYes application

You'll see the captured data appear in the application window.

### Step 4: Download

1. Review the captured MPD URL and license information
2. Enter a filename for the download
3. Click "Download" to start the process

The script will:
- Fetch decryption keys from the license server
- Download the encrypted video and audio streams
- Decrypt the content
- Mux everything into a single video file

### Extension Settings

Click the extension icon to access settings:

- **Auto-send to script** - Automatically send captured data (default: enabled)
- **Show notifications** - Display browser notifications when data is captured
- **Clear captured data** - Reset the extension state

## Required Dependencies

The installer will check for and guide you through installing:

### Core Dependencies
- **Python 3.8+** - Required for running the download scripts
- **FFmpeg** - For video/audio processing and muxing
- **N_m3u8DL-RE** or **dash-mpd-cli** - For downloading DASH/HLS streams

### Python Packages
- `requests` - HTTP requests
- `pycryptodome` - Cryptographic operations
- `protobuf` - Widevine protocol

All Python dependencies are listed in `requirements.txt` and installed automatically.

## Widevine CDM (Content Decryption Module)

You need a valid Widevine L3 Content Decryption Module to decrypt content.

### Option 1: Use Existing device.wvd
1. Obtain a `device.wvd` file (not included in this repository)
2. Place it in the HellYes root directory
3. The script will use it automatically for decryption

### Option 2: Generate device.wvd from Keys
If you have `client_id.bin` and `private_key.pem` files:

1. Place both files in the HellYes root directory
2. Run the dependency installer
3. The installer will automatically generate `device.wvd` from these files

**Note:** Obtaining a CDM or key files is your responsibility. This project does not provide CDMs or keys.

## Troubleshooting

### Extension Not Connecting

If the extension shows "Not connected" status:

1. Verify the native host is installed:
   - **Windows**: Check `HKEY_CURRENT_USER\Software\Google\Chrome\NativeMessagingHosts\com.hellyes.native`
   - **Linux**: Check `~/.config/google-chrome/NativeMessagingHosts/com.hellyes.native.json`

2. Ensure `HellSharedAutoProcessor` is running

3. Restart your browser

### No Data Being Captured

1. Make sure you're on a page with DRM-protected content
2. Try playing the video to trigger network requests
3. Check the browser console for errors (F12 → Console tab)

### Download Failures

1. Verify all dependencies are installed (run the installer again)
2. Check that you have a valid `device.wvd` file
3. Ensure you have write permissions in the download directory
4. Some content may be protected by additional restrictions

### Windows Build Issues

If you encounter "permission denied" errors when building:

1. Close any running instances of `HellSharedAutoProcessor.exe`
2. Close any File Explorer windows viewing the `dist/` folder
3. Run `build_windows.bat` again

## Advanced Usage

### Command-Line Mode with JSON Input

The modern `allhell3.py` script accepts JSON configuration files:

```bash
python allhell3.py path/to/config.json
```

The JSON file should contain:
```json
{
  "manifestUrl": "https://example.com/manifest.mpd",
  "licenseUrl": "https://example.com/license",
  "bodyBase64": "base64_encoded_license_body",
  "headers": {
    "User-Agent": "...",
    "Cookie": "..."
  },
  "title": "video_name"
}
```

### Legacy Manual Input Mode

For interactive manual input, use `allhell3o.py` (original version):

```bash
python allhell3o.py
```

This will prompt you for:
1. **MPD URL** - Copy from browser DevTools Network tab
2. **cURL command** - Right-click license request → Copy → Copy as cURL (paste without echo)
3. Press **Ctrl+D** (Linux) or **Ctrl+Z** (Windows) to submit the cURL
4. **Filename** - Desired output filename

**Note:** The GUI version (`gui.py`) is deprecated. Use `HellSharedAutoProcessor` for the best graphical experience with full browser extension support.

### Using Different Downloaders

Edit the script to choose your preferred downloader:

- **N_m3u8DL-RE** (default) - Faster, better for HLS/DASH
- **dash-mpd-cli** - Simpler, downloads subtitles separately

## Project Structure

```
HellYes/
├── allhell3.py                    # Core download script (JSON input)
├── allhell3o.py                   # Original script (interactive input)
├── allhell3_auto_processor.py     # GUI application with extension support
├── gui.py                         # Legacy GUI (deprecated)
├── native_host.py                 # Native messaging relay
├── dependency_installer_gui.py    # Guided installer
├── browser-extension/             # Browser extension source
│   ├── manifest.json
│   ├── service-worker.js
│   ├── contentScript.js
│   └── popup/
├── build_windows.bat              # Windows build script
├── build_linux.sh                 # Linux build script
└── requirements.txt               # Python dependencies
```

## Version Compatibility

All components (browser extensions and native applications) share the same version number to ensure compatibility. Always download matching versions from the same release.

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Legal Disclaimer

This tool is for educational and personal use only. Users are responsible for complying with:

- Terms of Service of content providers
- Copyright laws in their jurisdiction
- DRM regulations and anti-circumvention laws

The developers do not condone piracy or illegal content distribution.

## Credits

This version of HellYes is maintained by **[MalMen](https://github.com/MalMen)**.

**Original Project:**
- Original HellYes by [A_n_g_e_l_a (vinefeeder)](https://github.com/vinefeeder/HellYes)
- Original core download functionality and Widevine integration

**This Fork Adds:**
- Browser extension for automatic data capture
- Native messaging host for browser-script communication
- Automated dependency installer with GUI
- Cross-platform build system
- Modern JSON-based workflow

All original HellYes functionality remains available. Thank you to A_n_g_e_l_a for creating the foundation of this project.

## License

This project uses a **dual license** structure:

- **Original HellYes code** by A_n_g_e_l_a: MIT License
- **Browser extension and automation additions** by MalMen: GNU GPL v3

The **combined work is distributed under GNU GPL v3**, which means:
- ✅ You can use, modify, and distribute this software freely
- ✅ You must make source code available for any distributed modifications
- ✅ You must license modifications under GPL v3
- ✅ You must preserve copyright notices

This ensures the project remains open source. See [LICENSE](LICENSE) for full details.

---

**Happy downloading!**
# HellYes
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
browsers_linux.py - Linux/macOS browser native messaging host installer
Installs native messaging host for Chrome, Chromium, Firefox, Brave, and other browsers
"""

import os
import sys
import json
import shutil
from pathlib import Path

def get_script_dir():
    """Get the project root directory (where the executable or scripts are located)"""
    script_file = Path(__file__).absolute()

    # Check if this script is in a temp directory (extracted from executable)
    if 'tmp' in str(script_file).lower():
        # Running from extracted executable
        # The working directory should be where the executables are
        return Path.cwd().absolute()
    else:
        # Running from source - use parent of this script's directory
        return script_file.parent.parent.absolute()

def get_native_script_path():
    """Get the path to native host executable"""
    script_dir = get_script_dir()

    # First, try to find the standalone executable (preferred)
    native_exe = script_dir / "HellSharedNativeHost"
    if native_exe.exists():
        # Make sure it's executable
        native_exe.chmod(0o755)
        return str(native_exe)

    # Fallback: use native.py
    native_py = script_dir / "native.py"

    if not native_py.exists():
        raise FileNotFoundError(
            f"Neither HellSharedNativeHost nor native.py found in {script_dir}\n"
            f"Please run the build script or place native.py in the project directory."
        )

    # Make sure it's executable
    native_py.chmod(0o755)
    return str(native_py)

def build_chrome_manifest(extension_id):
    """Build manifest for Chrome-based browsers"""
    native_path = get_native_script_path()

    return {
        "name": "org.hellyes.hellyes",
        "description": "Native messaging for HellYes",
        "path": native_path,
        "type": "stdio",
        "allowed_origins": [
            f"chrome-extension://{extension_id}/"
        ]
    }

def build_firefox_manifest():
    """Build manifest for Firefox"""
    native_path = get_native_script_path()

    return {
        "name": "org.hellyes.hellyes",
        "description": "Native messaging for HellYes",
        "path": native_path,
        "type": "stdio",
        "allowed_extensions": [
            "hellyes@hellyes.org"
        ]
    }

def create_manifest_file(manifest_data, file_path):
    """Create manifest JSON file"""
    file_path = Path(file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, 'w') as f:
        json.dump(manifest_data, f, indent=2)

    # Make sure it's readable
    file_path.chmod(0o644)

    return file_path

def check_browser_installed(browser_name):
    """Check if a browser is installed by checking if command exists"""
    browser_commands = {
        "Chrome": "google-chrome",
        "Chromium": "chromium",
        "Firefox": "firefox",
        "Brave": "brave-browser",
    }

    if browser_name not in browser_commands:
        return False

    return shutil.which(browser_commands[browser_name]) is not None

def is_snap_installed(browser_command):
    """Check if a browser is installed via snap"""
    browser_path = shutil.which(browser_command)
    if browser_path and '/snap/' in browser_path:
        return True
    return False

def install_chrome_manifest(browser_name, extension_id):
    """Install manifest for Chrome-based browser"""
    browser_dirs = {
        "Chrome": Path.home() / ".config/google-chrome/NativeMessagingHosts",
        "Chromium": Path.home() / ".config/chromium/NativeMessagingHosts",
        "Brave": Path.home() / ".config/BraveSoftware/Brave-Browser/NativeMessagingHosts",
    }

    if browser_name not in browser_dirs:
        return False, f"Unsupported browser: {browser_name}"

    host_dir = browser_dirs[browser_name]
    manifest_path = host_dir / "org.hellyes.hellyes.json"

    try:
        # Create manifest
        chrome_manifest = build_chrome_manifest(extension_id)
        create_manifest_file(chrome_manifest, manifest_path)
        return True, str(manifest_path)
    except Exception as e:
        return False, str(e)

def install_firefox_manifest():
    """Install manifest for Firefox"""
    host_dir = Path.home() / ".mozilla/native-messaging-hosts"
    manifest_path = host_dir / "org.hellyes.hellyes.json"

    try:
        # Create manifest
        firefox_manifest = build_firefox_manifest()
        create_manifest_file(firefox_manifest, manifest_path)
        return True, str(manifest_path)
    except Exception as e:
        return False, str(e)

def install_browsers_manifest(extension_id=None):
    """Install browser manifests for all detected browsers"""
    results = []

    print("=" * 60)
    print("HellYes Browser Native Messaging Host Installer (Linux)")
    print("=" * 60)
    print()

    # Check for Chrome-based browsers
    chrome_browsers = []
    if check_browser_installed("Chrome"):
        chrome_browsers.append("Chrome")
    if check_browser_installed("Chromium"):
        chrome_browsers.append("Chromium")
    if check_browser_installed("Brave"):
        chrome_browsers.append("Brave")

    if chrome_browsers:
        print(f"[+] Detected Chrome-based browsers: {', '.join(chrome_browsers)}")
        print()

        # Check for snap installations
        snap_warnings = []
        for browser in chrome_browsers:
            browser_cmd = {
                "Chrome": "google-chrome",
                "Chromium": "chromium",
                "Brave": "brave-browser"
            }.get(browser)

            if browser_cmd and is_snap_installed(browser_cmd):
                snap_warnings.append(browser)

        if snap_warnings:
            print(f"⚠️  WARNING: {', '.join(snap_warnings)} installed via snap.")
            print("   Native messaging may not work with snap-based installations.")
            print()

        # Ask for extension ID
        if extension_id is None:
            print("Select Chrome extension installation type:")
            print("1) Compiled extension (default) - Official release")
            print("2) Unpacked extension - Development mode")
            print("3) Skip Chrome extension installation")
            print()

            choice = input("Enter 1, 2, or 3 [default 1]: ").strip()

            if choice == "2":
                extension_id = input("Enter your Chrome Extension ID: ").strip()
            elif choice == "3":
                chrome_browsers = []
                print("Skipping Chrome-based browsers.")
            else:
                # Default compiled extension ID
                extension_id = "kiepegiehgkjkbebfagoadghjdfkegpc"

        if chrome_browsers:
            print()
            print(f"Using Extension ID: {extension_id}")
            print()

            # Install for each browser
            for browser in chrome_browsers:
                success, result = install_chrome_manifest(browser, extension_id)
                if success:
                    results.append(f"[OK] Registered for {browser} at {result}")
                else:
                    results.append(f"[FAIL] Failed to register for {browser}: {result}")

    # Check for Firefox
    if check_browser_installed("Firefox"):
        print("[+] Detected Mozilla Firefox")

        # Check for snap installation
        if is_snap_installed("firefox"):
            print("⚠️  WARNING: Firefox installed via snap.")
            print("   Native messaging may not work with snap-based installations.")

        print()

        # Install for Firefox
        success, result = install_firefox_manifest()
        if success:
            results.append(f"[OK] Registered for Mozilla Firefox at {result}")
        else:
            results.append(f"[FAIL] Failed to register for Mozilla Firefox: {result}")

    # Print results
    print()
    print("=" * 60)
    print("Installation Results:")
    print("=" * 60)
    for result in results:
        print(result)

    if not results:
        print("[!] No supported browsers detected!")
        print()
        print("Supported browsers: Chrome, Chromium, Firefox, Brave")

    print()
    print("=" * 60)

    return len([r for r in results if r.startswith("[OK]")]) > 0

def install_browsers_manifest_filtered(extension_id=None, firefox_only=False, chrome_only=False):
    """Install browser manifests with filter for specific browser types"""
    results = []

    print("=" * 60)
    print("HellYes Browser Native Messaging Host Installer (Linux)")
    print("=" * 60)
    print()

    # Firefox installation
    if firefox_only or not chrome_only:
        if check_browser_installed("Firefox"):
            print("[+] Installing for Mozilla Firefox")

            # Check for snap installation
            if is_snap_installed("firefox"):
                print("⚠️  WARNING: Firefox installed via snap.")
                print("   Native messaging may not work with snap-based installations.")

            print()

            # Install for Firefox
            success, result = install_firefox_manifest()
            if success:
                results.append(f"[OK] Registered for Mozilla Firefox at {result}")
            else:
                results.append(f"[FAIL] Failed to register for Mozilla Firefox: {result}")
        else:
            print("[!] Firefox not detected on this system")

    # Chrome-based browsers installation
    if chrome_only or not firefox_only:
        chrome_browsers = []
        if check_browser_installed("Chrome"):
            chrome_browsers.append("Chrome")
        if check_browser_installed("Chromium"):
            chrome_browsers.append("Chromium")
        if check_browser_installed("Brave"):
            chrome_browsers.append("Brave")

        if chrome_browsers:
            print(f"[+] Installing for Chrome-based browsers: {', '.join(chrome_browsers)}")
            print()

            # Check for snap installations
            for browser in chrome_browsers:
                browser_cmd = {
                    "Chrome": "google-chrome",
                    "Chromium": "chromium",
                    "Brave": "brave-browser"
                }.get(browser)

                if browser_cmd and is_snap_installed(browser_cmd):
                    print(f"⚠️  WARNING: {browser} installed via snap.")
                    print("   Native messaging may not work with snap-based installations.")

            if extension_id is None:
                extension_id = "kiepegiehgkjkbebfagoadghjdfkegpc"

            print(f"Using Extension ID: {extension_id}")
            print()

            # Install for each browser
            for browser in chrome_browsers:
                success, result = install_chrome_manifest(browser, extension_id)
                if success:
                    results.append(f"[OK] Registered for {browser} at {result}")
                else:
                    results.append(f"[FAIL] Failed to register for {browser}: {result}")
        else:
            print("[!] No Chrome-based browsers detected on this system")

    # Print results
    print()
    print("=" * 60)
    print("Installation Results:")
    print("=" * 60)
    for result in results:
        print(result)

    if not results:
        print("[!] No browsers were configured!")

    print()
    print("=" * 60)

    return len([r for r in results if r.startswith("[OK]")]) > 0

if __name__ == "__main__":
    import argparse

    # Check if running on Linux/macOS
    if sys.platform == "win32":
        print("This script is for Linux/macOS only!")
        print("On Windows, use: python install/browsers_windows.py")
        sys.exit(1)

    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Install browser native messaging host for Linux/macOS")
    parser.add_argument("--silent", action="store_true", help="Run in silent mode (no prompts)")
    parser.add_argument("--extension-id", type=str, help="Chrome extension ID (default: compiled extension)")
    parser.add_argument("--firefox-only", action="store_true", help="Install only for Firefox")
    parser.add_argument("--chrome-only", action="store_true", help="Install only for Chrome-based browsers")
    args = parser.parse_args()

    try:
        # Determine which browsers to install
        if args.firefox_only and args.chrome_only:
            print("[ERROR] Cannot use both --firefox-only and --chrome-only")
            sys.exit(1)

        # If silent mode or specific browser mode, use appropriate extension ID
        if args.silent or args.firefox_only or args.chrome_only:
            extension_id = args.extension_id or "kiepegiehgkjkbebfagoadghjdfkegpc"

            # Call install function with browser filter
            if args.firefox_only:
                success = install_browsers_manifest_filtered(extension_id=extension_id, firefox_only=True)
            elif args.chrome_only:
                success = install_browsers_manifest_filtered(extension_id=extension_id, chrome_only=True)
            else:
                success = install_browsers_manifest(extension_id=extension_id)
        else:
            success = install_browsers_manifest(extension_id=args.extension_id)

        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nInstallation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

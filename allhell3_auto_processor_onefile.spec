# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for allhell3_auto_processor - SINGLE FILE EDITION
Creates a standalone executable with ALL dependencies bundled into ONE file
"""

import sys
import platform
import os
from pathlib import Path

block_cipher = None

# Determine if we're on Windows
is_windows = platform.system() == 'Windows'

# Get absolute path to icon file
icon_path = os.path.abspath('hellyes.ico')

# Collect all install scripts
install_scripts = []
if os.path.exists('install'):
    for f in os.listdir('install'):
        if f.endswith('.py') or f.endswith('.sh'):
            install_scripts.append((os.path.join('install', f), 'install'))

a = Analysis(
    ['allhell3_auto_processor.py'],
    pathex=[],
    binaries=[],
    datas=[
        # Include the main script that the processor calls
        ('allhell3.py', '.'),
        # Include dependency installer
        ('dependency_installer_gui.py', '.'),
        # Include app icon
        ('browser-extension/logo/hellyes_original.png', 'browser-extension/logo'),
        # Include all install scripts
    ] + install_scripts,
    hiddenimports=[
        # tkinter and GUI
        'tkinter',
        'tkinter.ttk',
        'tkinter.scrolledtext',
        'tkinter.messagebox',
        'tkinter.filedialog',
        # Platform-specific
        'pexpect',
        'pexpect.pty_spawn',
        'pexpect.popen_spawn',
        'shlex',
        # Standard library
        'subprocess',
        'threading',
        'json',
        'pathlib',
        'datetime',
        're',
        'platform',
        'time',
        'io',
        'base64',
        'urllib.parse',
        'xml.etree.ElementTree',
        'webbrowser',
        'tempfile',
        'shutil',
        'atexit',
        'importlib',
        'importlib.util',
        'traceback',
        # Required by allhell3.py
        'httpx',
        'httpx._client',
        'httpx._config',
        'httpx._models',
        'httpx._transports',
        'httpx._types',
        'httpx._content',
        'httpx._decoders',
        'httpx._exceptions',
        'httpx._auth',
        'termcolor',
        'pyfiglet',
        'pyfiglet.fonts',
        'pywidevine',
        'pywidevine.cdm',
        'pywidevine.device',
        'pywidevine.pssh',
        'pywidevine.license_protocol_pb2',
        'pywidevine._structures',
        'pywidevine.deviceconfig',
        'Crypto',
        'Crypto.Cipher',
        'Crypto.Cipher.AES',
        'Crypto.Hash',
        'Crypto.Hash.CMAC',
        'Crypto.Hash.SHA256',
        'Crypto.Random',
        'Crypto.Util',
        'Crypto.Util.Padding',
        'protobuf',
        'google.protobuf',
        # Required by dependency_installer
        'winreg',  # Windows only, but won't break on Linux
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'PyQt5',
        'PyQt6',
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'PIL',
        'IPython',
        'jupyter',
        'notebook',
        'pytest',
        'setuptools',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='HellSharedAutoProcessor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window (GUI only)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_path if os.path.exists(icon_path) else None,  # Windows ICO
)

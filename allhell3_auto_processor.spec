# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for allhell3_auto_processor
Creates a standalone executable with all dependencies bundled
"""

import sys
import platform

block_cipher = None

# Determine if we're on Windows
is_windows = platform.system() == 'Windows'

a = Analysis(
    ['allhell3_auto_processor.py'],
    pathex=[],
    binaries=[],
    datas=[
        # Include the main script that the processor calls
        ('allhell3.py', '.'),
        # Include dependency installer if needed
        ('dependency_installer_gui.py', '.'),
        # Include install scripts if they exist
        ('install/*.py', 'install'),
    ],
    hiddenimports=[
        # tkinter and GUI
        'tkinter',
        'tkinter.ttk',
        'tkinter.scrolledtext',
        'tkinter.messagebox',
        # Platform-specific
        'pexpect',
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
        # Required by allhell3.py
        'httpx',
        'httpx._client',
        'httpx._config',
        'httpx._models',
        'httpx._transports',
        'httpx._types',
        'termcolor',
        'pyfiglet',
        'pywidevine',
        'pywidevine.cdm',
        'pywidevine.device',
        'pywidevine.pssh',
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
    [],
    exclude_binaries=True,
    name='HellSharedAutoProcessor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # No console window (GUI only)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add icon path here if you have one: 'icon.ico' or 'icon.icns'
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='HellSharedAutoProcessor',
)

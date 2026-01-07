# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for native.py - Browser Native Messaging Host
Creates a standalone executable for browser extension communication
"""

import sys
import platform

block_cipher = None

a = Analysis(
    ['native.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'struct',
        'json',
        'subprocess',
        'os',
        'datetime',
        'base64',
        're',
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
        'tkinter',
        'httpx',
        'termcolor',
        'pyfiglet',
        'pywidevine',
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
    name='HellSharedNativeHost',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Console mode for stdio communication
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)

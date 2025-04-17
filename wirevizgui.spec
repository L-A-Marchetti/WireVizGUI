# -*- mode: python ; coding: utf-8 -*-

import os
block_cipher = None

graphviz_bin_path = os.path.join(os.path.dirname(os.path.abspath('__file__')), 'bin')

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('index.html', '.'),
        (os.path.join(graphviz_bin_path, '*'), 'graphviz_bin'),

    ],
    hiddenimports=['wireviz-web', 'graphviz'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
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
    name='WireVizGUI',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    icon='icon.ico' if os.path.exists('icon.ico') else None,
)
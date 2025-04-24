# -*- mode: python ; coding: utf-8 -*-


# Add the dist folder to the bundled data
datas = [
    ('frontend/dist', 'frontend/dist')  # Include the frontend's static files
]

# Update the Analysis section
a = Analysis(
    ['backend_app.py'],
    pathex=[],
    binaries=[],
    datas=datas,  # Include the datas here
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='spotify-bot',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

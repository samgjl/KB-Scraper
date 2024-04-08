# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['../src/scraper_gui.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['_tkinter', 'Tkinter', 'enchant', 'twisted'],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='KB Scraper',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon = ['../src/TDX_logo.ico']
)
coll = COLLECT(
    exe,
    Tree("../src/"),
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='KB Scraper',
)
app = BUNDLE(
    coll,
    name='KB Scraper.app',
    icon=None,
    bundle_identifier=None,
)

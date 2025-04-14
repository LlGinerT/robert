# -*- mode: python ; coding: utf-8 -*-

import sys
import os
from PyInstaller.utils.hooks import collect_all

project_root = os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), '..'))
conda_prefix = os.environ["CONDA_PREFIX"]
conda_bin_dir = os.path.join(conda_prefix, "Library", "bin")

# Lista de paquetes que usamos en collect_all
packages = [
    'PySide6',
    'shap',
    'weasyprint',
    'fitz',
    'rdkit',
    'ansi2html',
    'robert'
]

datas, binaries, hiddenimports = [], [], []

for package in packages:
    pkg_datas, pkg_binaries, pkg_hidden = collect_all(package)
    datas += pkg_datas
    binaries += pkg_binaries
    hiddenimports += pkg_hidden

# DLLs necesarias para WeasyPrint (GTK3 + fonts)
gtk_dlls = [
    "libglib-2.0-0.dll",
    "libgobject-2.0-0.dll",
    "libgdk-3-0.dll",
    "libgtk-3-0.dll",
    "libcairo-2.dll",
    "libpango-1.0-0.dll",
    "libpangocairo-1.0-0.dll",
    "libgdk_pixbuf-2.0-0.dll",
    "msvcrt.dll",  # necesaria en algunos sistemas
]

for dll in gtk_dlls:
    path = os.path.join(conda_bin_dir, dll)
    if os.path.isfile(path):
        binaries.append((path, "."))
    else:
        print(f"[WARNING]: GTK DLL missing: {dll}")

# oneDAL (scikit-learn-intelex)
onedal_dlls = [
    "libmmd.dll",
    "sycl8.dll",
    "svml_dispmd.dll"
]

for dll in onedal_dlls:
    path = os.path.join(conda_bin_dir, dll)
    if os.path.isfile(path):
        binaries.append((path, "."))
    else:
        print(f"[WARNING]: oneDAL DLL missing: {dll}")

a = Analysis(
    [os.path.join(project_root, 'GUI_easyROB', 'easyrob.py')],
    pathex=[project_root],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
)

pyz = PYZ(a.pure, a.zipped_data)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='easyROB',
    debug=True,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    icon=None
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='easyROB'
)

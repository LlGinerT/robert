# PyInstaller “onedir” build, can change to onefile but antivirus are less friendly

from pathlib import Path
block_cipher = None

# --- PROJECT PATHS ----------------------------------------------------------
# Path for main gui script config
MAIN_SCRIPT = Path.cwd()/"easyrob.py" # r".\easyrob.py"  entry‑point script
ICON_FILE = Path.cwd()/"icons"/"Robert_icon.ico"     # application icon

# Folders to bundle with the app
ROBERT_ENV_DIR = r".\robert_env"    # unpacked conda‑pack env
IMAGE_DIR = r".\icons"       # PNG/SVG etc.
RESOURCE_DIR = r"C:\EXAMPLE\assets\resources"    # optional extras if needed add on datas

# Name of the output folder created inside dist\
APP_NAME = "easyRob"


# Helper: collect every file in a folder
def collect_dir(folder, dest_root=""):
    """Return [(src, dest_rel)] for every file under 'folder'."""
    datas = []
    p = Path(folder)
    if p.exists():
        for f in p.rglob("*"):
            if f.is_file():
                rel_dest = Path(dest_root) / f.relative_to(p)
                datas.append((str(f), str(rel_dest.parent)))
    return datas


# --- ANALYSIS ----------------------------------------------------------
a = Analysis(
    [MAIN_SCRIPT],
    pathex=[],
    binaries=[],
    datas=(
        collect_dir(ROBERT_ENV_DIR, "robert_env") +
        collect_dir(IMAGE_DIR,      "images")),
    hiddenimports=[],
    hookspath=[],
    excludes=[],
    cipher=block_cipher,
)

# --- PYZ ---------------------------------------------------------------
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# --- EXE ---------------------------------------------------------------
exe = EXE(
    pyz,
    a.scripts,
    [],
    name=APP_NAME,
    console=True,           # True si necesitas ventana cmd
    debug=True,             # True si necesitas debug  
    icon=ICON_FILE,
    exclude_binaries=False,  
    upx=True,
)

# --- COLLECT ----------------------------------------------------------
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name=APP_NAME,                # crea dist/<APP_NAME>/
)
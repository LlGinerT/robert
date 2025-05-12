from pathlib import Path

block_cipher = None

# --- PROJECT PATHS ----------------------------------------------------------

SPEC_DIR = Path.cwd().resolve()
PROJECT_ROOT = SPEC_DIR.parent.parent

# Path for main gui script config
ENTRY_POINT = PROJECT_ROOT/"GUI_easyROB"/"easyrob.py"               # entry‑point script
ICON_FILE = PROJECT_ROOT/"GUI_easyROB"/"icons"/"Robert_icon.ico"    # application icon


# Folders to bundle with the app
ROBERT_ENV_DIR = SPEC_DIR/"robert_env"                   # unziped conda‑pack env
IMAGE_DIR = PROJECT_ROOT/"GUI_easyROB"/"icons"           # PNG/SVG etc.

# Name of the output folder created inside dist\
APP_NAME = "easyRob"

# --- AUXILIAR FUNCTIONS ------------------------------------------------------

# Helper: collect every file in a folder
def collect_dir(folder, dest_root=""):
    """Return tuple[(src, dest_rel)] for every file under 'folder'."""
    datas = []
    p = Path(folder)
    print(f"INFO: Collecting data from: {p}")
    if p.exists():
        for f in p.rglob("*"):
            if f.is_file():
                rel_dest = Path(dest_root) / f.relative_to(p)
                datas.append((str(f), str(rel_dest.parent)))
    else:
        print(f"WARNING: {p} not found")
    return datas

datas = (
    list(collect_dir(ROBERT_ENV_DIR, "robert_env")) +
    list(collect_dir(IMAGE_DIR, "images"))
)
# --- PYINSTALLER SPECS ----------------------------------------------------------

a = Analysis(
    [ENTRY_POINT],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[],   
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=1,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    name=APP_NAME,
    console=True,          # True if cmd window needed
    debug=True,             # True if debug mode needed(needs console=True)
    icon=ICON_FILE,         # Path to icon.
    exclude_binaries=False,  
    upx=False,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    name=APP_NAME,          # create dist/<APP_NAME>/
)
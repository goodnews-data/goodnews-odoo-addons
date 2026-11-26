"""Build the installable zip of one or more modules (Apps > Import module).

Usage: python tools/empaquetar.py <module_dir> [<module_dir> ...] [--out <dir>]
Each zip holds the module folder at its root, as Odoo expects. Default output: dist/
"""
import os
import sys
import zipfile

SKIP_DIRS = {"__pycache__", ".git"}
SKIP_FILES = {"desktop.ini", "Thumbs.db"}


def build(module_dir, out_dir):
    module_dir = os.path.abspath(module_dir)
    name = os.path.basename(module_dir)
    if not os.path.isfile(os.path.join(module_dir, "__manifest__.py")):
        raise SystemExit(f"{module_dir}: no __manifest__.py")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, name + ".zip")
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(module_dir):
            dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
            for f in sorted(files):
                if f in SKIP_FILES or f.endswith(".pyc"):
                    continue
                path = os.path.join(root, f)
                zf.write(path, os.path.join(name, os.path.relpath(path, module_dir)))
    return target


if __name__ == "__main__":
    args = sys.argv[1:]
    out = "dist"
    if "--out" in args:
        i = args.index("--out")
        out = args[i + 1]
        del args[i:i + 2]
    if not args:
        raise SystemExit(__doc__)
    for module in args:
        print(build(module, out))

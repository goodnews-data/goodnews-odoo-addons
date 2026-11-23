"""Build a TEST VARIANT of gn_base + gn_inventory_planner_base + gn_inventory_planner, every technical name changed.

Why: the real modules keep the Studio names (x_inventory_planner, x_studio_inventory_group_tag...)
so they cannot be installed where the Studio development exists (GoodNews test and production).
The variant renames models, fields, groups, menus and modules, so it installs next to the
real development in TEST, can be tried end to end, and is uninstalled afterwards without
touching the Studio development nor the GN Tools.

Usage: python tools/variante_prueba.py <out_dir>
Writes <out_dir>/gn_base_t.zip and <out_dir>/gn_inventory_planner_t.zip.
In the variant both scheduled actions start switched OFF: run them by hand
(Settings > Technical > Scheduled actions > Run manually) when testing.
"""
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from empaquetar import build  # noqa: E402

# Order matters: longer / more specific names first
MODULES = ["gn_base", "gn_inventory_planner_base", "gn_inventory_planner"]
RENAMES = [
    ("x_studio_inventory_group_tag", "x_t_inventory_group_tag"),
    ("x_studio_assigned_warehouse", "x_t_assigned_warehouse"),
    ("x_studio_assigned_central", "x_t_assigned_central"),
    ("x_inventory_planner", "x_t_inventory_planner"),
    ("x_inventory_history", "x_t_inventory_history"),
    ("x_product_tags", "x_t_product_tags"),
    ('<field name="name">Supply</field>', '<field name="name">Supply (prueba)</field>'),
    ('<field name="name">Data</field>', '<field name="name">Data (prueba)</field>'),
    ("('name', '=', 'Supply')", "('name', '=', 'Supply (prueba)')"),
    ("('name', '=', 'Data')", "('name', '=', 'Data (prueba)')"),
    ('<menuitem id="menu_planner" name="Inventory Planner"', '<menuitem id="menu_planner" name="[PRUEBA] Inventory Planner"'),
    ('<menuitem id="menu_history" name="Inventory History"', '<menuitem id="menu_history" name="[PRUEBA] Inventory History"'),
    ('<menuitem id="menu_tags" name="Inventory Groups"', '<menuitem id="menu_tags" name="[PRUEBA] Inventory Groups"'),
    ('"name": "GoodNews · ', '"name": "[PRUEBA] GoodNews · '),
    ('<field name="name">Ejecutar recuentos programados</field>', '<field name="name">[PRUEBA] Ejecutar recuentos programados</field>'),
    ('<field name="name">Actualizar inventory history</field>', '<field name="name">[PRUEBA] Actualizar inventory history</field>'),
    ('<group string="GoodNews" name="gn_locations">', '<group string="GoodNews (prueba)" name="gn_locations">'),
]
CRON_OFF = ('<field name="active" eval="True"/>', '<field name="active" eval="False"/>')
TEXT = (".py", ".xml", ".md", ".html", ".csv")


def variant(src, out):
    name = os.path.basename(src) + "_t"
    dst = os.path.join(out, name)
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__", "desktop.ini"))
    for root, _dirs, files in os.walk(dst):
        for f in files:
            if not f.endswith(TEXT):
                continue
            p = os.path.join(root, f)
            t = open(p, encoding="utf-8").read()
            for module in MODULES:
                t = re.sub(r"\b%s\b" % module, module + "_t", t)
            for a, b in RENAMES:
                t = t.replace(a, b)
            if f == "actions.xml":
                t = t.replace(*CRON_OFF)
            open(p, "w", encoding="utf-8", newline="\n").write(t)
    return dst


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    out = os.path.abspath(sys.argv[1])
    os.makedirs(out, exist_ok=True)
    for module in MODULES:
        folder = variant(os.path.join(ROOT, module), os.path.join(out, "src"))
        print(build(folder, out))

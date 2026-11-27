"""TEST VARIANT of the mockup modules: every technical name changed, so they install in the
GoodNews TEST database next to the Studio originals, are checked, and are uninstalled.

  - modules      gn_x            -> gn_x_t        (gn_base -> gn_base_t: only its two groups)
  - models/fields x_...           -> x_mq_...      (only the ones the mockup creates)
  - automations, menus and the "Action" buttons of server actions are installed OFF / unbound,
    model and group names get " (maqueta)": nobody in test sees or triggers anything.

Usage: python tools/maqueta_variante.py <generated_dir> <out_dir>
Writes <out_dir>/<module>_t/ folders, <out_dir>/zips/*.zip and <out_dir>/orden.txt (install order).
"""
import ast
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from empaquetar import build  # noqa: E402

SRC, OUT = sys.argv[1], sys.argv[2]
NOT_IN_TEST = {"gn_base", "gn_inventory_planner_base", "gn_valijas_base", "gn_entregas_parciales_base"}
mods = sorted(d for d in os.listdir(SRC) if os.path.isfile(os.path.join(SRC, d, "__manifest__.py")))


def manifest(path):
    return ast.literal_eval(open(path, encoding="utf-8").read().split("\n", 1)[1])


# Names the mockup creates
names = set()
for m in mods:
    for root, _, files in os.walk(os.path.join(SRC, m)):
        for f in files:
            if f.endswith(".xml"):
                s = open(os.path.join(root, f), encoding="utf-8").read()
                for rec in re.finditer(r'<record id="[^"]+" model="(ir\.model|ir\.model\.fields)">(.*?)</record>', s, re.S):
                    for tag in ("model", "name", "relation_table") if rec.group(1) == "ir.model" else ("name", "relation_table"):
                        v = re.search(r'<field name="%s">([^<]+)</field>' % tag, rec.group(2))
                        if v and v.group(1).startswith("x_"):
                            names.add(v.group(1))
NAME_RE = re.compile(r"(?<![A-Za-z0-9])(%s)(?![A-Za-z0-9_])" % "|".join(
    re.escape(n) for n in sorted(names, key=len, reverse=True)))
MOD_RE = re.compile(r"\b(%s)\b(?=\.)" % "|".join(re.escape(m) for m in sorted(mods + ["gn_base"], key=len, reverse=True)))


def transform(s):
    s = NAME_RE.sub(lambda m: "x_mq_" + m.group(1)[2:], s)
    s = MOD_RE.sub(lambda m: m.group(1) + "_t", s)
    s = re.sub(r'(<record id="automation_\d+" model="base.automation">.*?<field name="active" eval=")True', r"\1False", s, flags=re.S)
    s = re.sub(r'(<record id="menu_\d+" model="ir.ui.menu">.*?<field name="active" eval=")True', r"\1False", s, flags=re.S)
    s = re.sub(r'\s*<field name="binding_model_id"[^>]*/>', "", s)
    s = re.sub(r'\s*<field name="binding_view_types">[^<]*</field>', "", s)
    s = re.sub(r'(<record id="(?:model_[^"]+)" model="ir.model">\s*<field name="name">)([^<]+)', r"\1\2 (maqueta)", s)
    s = re.sub(r'(<record id="group_\d+" model="res.groups">\s*<field name="name">)([^<]+)', r"\1\2 (maqueta)", s)
    return s


if os.path.exists(OUT):
    shutil.rmtree(OUT)
os.makedirs(os.path.join(OUT, "zips"))
order, seen = [], set()
deps_of = {}
for m in mods:
    deps_of[m] = manifest(os.path.join(SRC, m, "__manifest__.py"))["depends"]


def visit(m):
    if m in seen:
        return
    seen.add(m)
    for d in deps_of[m]:
        if d in deps_of:
            visit(d)
    order.append(m)


for m in mods:
    visit(m)

# gn_base_t: the two groups of gn_base
gb = os.path.join(OUT, "gn_base_t")
os.makedirs(os.path.join(gb, "security"))
open(os.path.join(gb, "__init__.py"), "w").write("")
open(os.path.join(gb, "__manifest__.py"), "w", encoding="utf-8").write(repr({
    "name": "GoodNews · Base (maqueta, prueba)", "version": "17.0.1.0.0", "license": "LGPL-3",
    "depends": ["stock", "spreadsheet_dashboard"], "data": ["security/groups.xml"], "installable": True}))
open(os.path.join(gb, "security", "groups.xml"), "w", encoding="utf-8").write(
    '<?xml version="1.0" encoding="utf-8"?>\n<odoo>\n'
    '    <record id="group_supply" model="res.groups"><field name="name">Supply (maqueta)</field>'
    '<field name="category_id" ref="base.module_category_inventory"/></record>\n'
    '    <record id="group_data" model="res.groups"><field name="name">Data (maqueta)</field>'
    '<field name="category_id" ref="spreadsheet_dashboard.dashboard_management"/></record>\n</odoo>\n')
build(gb, os.path.join(OUT, "zips"))
final = ["gn_base_t"]
for m in order:
    dst = os.path.join(OUT, m + "_t")
    shutil.copytree(os.path.join(SRC, m), dst)
    for root, _, files in os.walk(dst):
        for f in files:
            p = os.path.join(root, f)
            if f.endswith(".xml"):
                content = transform(open(p, encoding="utf-8").read())
                open(p, "w", encoding="utf-8", newline="\n").write(content)
    mf = manifest(os.path.join(dst, "__manifest__.py"))
    mf["name"] += " (maqueta, prueba)"
    mf["depends"] = [d + "_t" if (d in deps_of or d == "gn_base") else d for d in mf["depends"] if d not in NOT_IN_TEST - {"gn_base"}]
    mf["application"] = False
    open(os.path.join(dst, "__manifest__.py"), "w", encoding="utf-8", newline="\n").write("# variant\n" + repr(mf) + "\n")
    build(dst, os.path.join(OUT, "zips"))
    final.append(m + "_t")
open(os.path.join(OUT, "orden.txt"), "w").write("\n".join(final) + "\n")
print(len(final), "módulos de prueba;", len(names), "nombres cambiados")

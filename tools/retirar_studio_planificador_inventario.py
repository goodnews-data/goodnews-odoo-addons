"""Hand the inventory planner over from Studio to gn_inventory_planner in a database that has both.

Run it AFTER installing gn_inventory_planner (logic module) where the Studio development exists
(GoodNews 2026). Nothing is deleted: the Studio pieces the module replaces are switched off, and a
backup of every touched record is written first so it can be undone.
  - Studio menus of the planner, history and inventory groups -> archived (the module adds its own)
  - Studio server actions bound to the Action menu of those models -> unbound (no duplicated buttons)
  - Studio scheduled actions of those models -> switched off (the module ones run instead)
  - Studio record rules of those models -> switched off (the module has the same ones)
Models, fields and data are NOT touched: they stay the Studio ones (the GN Tools reads them).

Usage (from the GN Tools repo, it reads the Odoo credentials of its .env):
  python retirar_studio_planificador_inventario.py <test|prod>                    dry run: lists what would change
  python retirar_studio_planificador_inventario.py <test|prod> apply              changes it (writes a backup json)
  python retirar_studio_planificador_inventario.py <test|prod> undo <backup.json> puts everything back
"""
import datetime
import json
import os
import sys

sys.path.insert(0, os.getcwd())
from platform_app.modules.proveedores.config import get_settings  # noqa: E402
from platform_app.modules.proveedores.odoo_client import OdooClient  # noqa: E402

MODELS = ["x_inventory_planner", "x_inventory_history", "x_product_tags"]
MODULE = "gn_inventory_planner"

env, mode = sys.argv[1], (sys.argv[2] if len(sys.argv) > 2 else "dry")
st = get_settings()
c = st.odoo_prod_conn() if env == "prod" else st.odoo_conn()
assert ("test" in c.odoo_db) == (env == "test"), c.odoo_db
cl = OdooClient(c.odoo_url, c.odoo_db, c.odoo_username, c.odoo_password, timeout=300)
X = lambda m, meth, *a, **k: cl.execute_kw(m, meth, list(a), k)  # noqa: E731
print("Entorno:", env, c.odoo_db, "| modo:", mode)

if mode == "undo":
    backup = json.load(open(sys.argv[3], encoding="utf-8"))
    for row in backup:
        X(row["model"], "write", [row["id"]], row["before"])
        print("restaurado", row["model"], row["id"], row["before"])
    sys.exit(0)

if not X("ir.module.module", "search_count", [("name", "=", MODULE), ("state", "=", "installed")]):
    raise SystemExit(f"{MODULE} is not installed here: install it first, or the planner is left without buttons and crons.")

own = {}
for r in X("ir.model.data", "search_read", [("module", "=", MODULE)], fields=["model", "res_id"]):
    own.setdefault(r["model"], set()).add(r["res_id"])
mids = X("ir.model", "search", [("model", "in", MODELS)])
windows = X("ir.actions.act_window", "search", [("res_model", "in", MODELS)])
studio_windows = [w for w in windows if w not in own.get("ir.actions.act_window", set())]

plan = []  # (model, id, name, before, after)
for m in X("ir.ui.menu", "search_read", [("action", "in", ["ir.actions.act_window,%d" % w for w in studio_windows])], fields=["name", "active"]):
    plan.append(("ir.ui.menu", m["id"], m["name"], {"active": True}, {"active": False}))
for a in X("ir.actions.server", "search_read", [("model_id", "in", mids), ("binding_model_id", "!=", False)], fields=["name", "binding_model_id"]):
    if a["id"] not in own.get("ir.actions.server", set()):
        plan.append(("ir.actions.server", a["id"], a["name"], {"binding_model_id": a["binding_model_id"][0]}, {"binding_model_id": False}))
for cr in X("ir.cron", "search_read", [("model_id", "in", mids), ("active", "=", True)], fields=["name"]):
    if cr["id"] not in own.get("ir.cron", set()):
        plan.append(("ir.cron", cr["id"], cr["name"], {"active": True}, {"active": False}))
for ru in X("ir.rule", "search_read", [("model_id", "in", mids), ("active", "=", True)], fields=["name"]):
    if ru["id"] not in own.get("ir.rule", set()):
        plan.append(("ir.rule", ru["id"], ru["name"], {"active": True}, {"active": False}))

for model, rid, name, before, after in plan:
    print(f"  {model} {rid} «{name}»: {before} -> {after}")
if mode != "apply":
    print(len(plan), "cambios (no se ha tocado nada; añade 'apply' para hacerlos)")
    sys.exit(0)

stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
path = f"retirar_studio_planificador_{env}_{stamp}.json"
json.dump([{"model": m, "id": i, "name": n, "before": b} for m, i, n, b, _a in plan], open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("copia de seguridad:", os.path.abspath(path))
for model, rid, _name, _before, after in plan:
    X(model, "write", [rid], after)
print(len(plan), "cambios hechos. Para deshacer: undo", path)

"""Hand the valijas over from Studio to gn_valijas in a database that has both (GoodNews 2026).

Run it AFTER installing gn_valijas. Nothing is deleted; a backup of every touched record is
written first so it can be undone.
  - Studio server actions "Programar sin entrega parcial" / "Validar sin entrega parcial" -> unbound
  - Studio scheduled action "Validar sin entrega parcial" -> switched off (the module one runs)
  - Studio view(s) of the transfer form: the old "Programar valija" button and the 4 valija
    fields are removed from the view (the module shows its own); the rest of the view is kept
The fields and their data are NOT touched (x_studio_scheduled_backorder can be deleted later).

Usage (from the GN Tools repo, it reads the Odoo credentials of its .env):
  python retirar_studio_valijas.py <test|prod>                     dry run
  python retirar_studio_valijas.py <test|prod> apply               change (writes a backup json)
  python retirar_studio_valijas.py <test|prod> undo <backup.json>  put everything back
"""
import datetime
import json
import os
import re
import sys

sys.path.insert(0, os.getcwd())
from platform_app.modules.proveedores.config import get_settings  # noqa: E402
from platform_app.modules.proveedores.odoo_client import OdooClient  # noqa: E402

MODULE = "gn_valijas"
FIELDS = ["x_studio_scheduled", "x_studio_locked", "x_studio_validation_date", "x_studio_scheduled_backorder"]

env, mode = sys.argv[1], (sys.argv[2] if len(sys.argv) > 2 else "dry")
st = get_settings()
c = st.odoo_prod_conn() if env == "prod" else st.odoo_conn()
assert ("test" in c.odoo_db) == (env == "test"), c.odoo_db
cl = OdooClient(c.odoo_url, c.odoo_db, c.odoo_username, c.odoo_password, timeout=300)
X = lambda m, meth, *a, **k: cl.execute_kw(m, meth, list(a), k)  # noqa: E731
print("Entorno:", env, c.odoo_db, "| modo:", mode)

if mode == "undo":
    for row in json.load(open(sys.argv[3], encoding="utf-8")):
        X(row["model"], "write", [row["id"]], row["before"])
        print("restaurado", row["model"], row["id"])
    sys.exit(0)

if not X("ir.module.module", "search_count", [("name", "=", MODULE), ("state", "=", "installed")]):
    raise SystemExit(f"{MODULE} is not installed here: install it first.")
own = {}
for r in X("ir.model.data", "search_read", [("module", "=", MODULE)], fields=["model", "res_id"]):
    own.setdefault(r["model"], set()).add(r["res_id"])

plan = []
studio_actions = [a for a in X("ir.actions.server", "search_read",
                               [("model_id.model", "=", "stock.picking"), ("code", "ilike", "x_studio_scheduled")],
                               fields=["name", "binding_model_id"]) if a["id"] not in own.get("ir.actions.server", set())]
for a in studio_actions:
    if a["binding_model_id"]:
        plan.append(("ir.actions.server", a["id"], a["name"], {"binding_model_id": a["binding_model_id"][0]}, {"binding_model_id": False}))
for cr in X("ir.cron", "search_read", [("model_id.model", "=", "stock.picking"), ("code", "ilike", "x_studio_scheduled"), ("active", "=", True)], fields=["name"]):
    if cr["id"] not in own.get("ir.cron", set()):
        plan.append(("ir.cron", cr["id"], cr["name"], {"active": True}, {"active": False}))

ids = [str(a["id"]) for a in studio_actions]
node = re.compile(r'[ \t]*<(?:button[^>]*name="(?:%s)"[^>]*/>|field[^>]*name="(?:%s)"[^>]*/>)[ \t]*\r?\n?' % ("|".join(ids) or "x^", "|".join(FIELDS)))
for v in X("ir.ui.view", "search_read", [("model", "=", "stock.picking"), ("active", "=", True), ("arch_db", "ilike", "x_studio_scheduled")], fields=["name", "arch_db"]):
    if v["id"] in own.get("ir.ui.view", set()):
        continue
    new = node.sub("", v["arch_db"])
    if new != v["arch_db"]:
        removed = len(node.findall(v["arch_db"]))
        plan.append(("ir.ui.view", v["id"], f"{v['name']} (quita {removed} nodos)", {"arch_db": v["arch_db"]}, {"arch_db": new}))

for model, rid, name, before, after in plan:
    shown = {k: (v if k != "arch_db" else f"<{len(v)} caracteres>") for k, v in after.items()}
    print(f"  {model} {rid} «{name}» -> {shown}")
if mode != "apply":
    print(len(plan), "cambios (no se ha tocado nada; añade 'apply')")
    sys.exit(0)
path = f"retirar_studio_valijas_{env}_{datetime.datetime.now():%Y%m%d-%H%M%S}.json"
json.dump([{"model": m, "id": i, "name": n, "before": b} for m, i, n, b, _a in plan], open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("copia de seguridad:", os.path.abspath(path))
for model, rid, _n, _b, after in plan:
    X(model, "write", [rid], after)
print(len(plan), "cambios hechos. Para deshacer: undo", path)

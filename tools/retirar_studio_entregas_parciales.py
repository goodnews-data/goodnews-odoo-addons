"""Hand the partial deliveries over from Studio to gn_entregas_parciales (GoodNews 2026 database).

Run it AFTER installing gn_entregas_parciales. Nothing is deleted; a backup is written first.
  - The two Studio automations (flag the purchase order / cancel Store App backorders) -> switched off
  - The ids they had hard-coded go to the module's system parameters:
      gn_entregas_parciales.tipos_sin_parcial       picking types never flagged
      gn_entregas_parciales.categorias_sin_cancelar  categories whose backorders are never cancelled

Usage (from the GN Tools repo, it reads the Odoo credentials of its .env):
  python retirar_studio_entregas_parciales.py <test|prod>                     dry run
  python retirar_studio_entregas_parciales.py <test|prod> apply               change (backup json)
  python retirar_studio_entregas_parciales.py <test|prod> undo <backup.json>  put everything back
"""
import datetime
import json
import os
import re
import sys

sys.path.insert(0, os.getcwd())
from platform_app.modules.proveedores.config import get_settings  # noqa: E402
from platform_app.modules.proveedores.odoo_client import OdooClient  # noqa: E402

MODULE = "gn_entregas_parciales"
P_TYPES = "gn_entregas_parciales.tipos_sin_parcial"
P_CATEG = "gn_entregas_parciales.categorias_sin_cancelar"

env, mode = sys.argv[1], (sys.argv[2] if len(sys.argv) > 2 else "dry")
st = get_settings()
c = st.odoo_prod_conn() if env == "prod" else st.odoo_conn()
assert ("test" in c.odoo_db) == (env == "test"), c.odoo_db
cl = OdooClient(c.odoo_url, c.odoo_db, c.odoo_username, c.odoo_password, timeout=300)
X = lambda m, meth, *a, **k: cl.execute_kw(m, meth, list(a), k)  # noqa: E731
print("Entorno:", env, c.odoo_db, "| modo:", mode)


def param_id(key):
    r = X("ir.config_parameter", "search_read", [("key", "=", key)], fields=["value"])
    return (r[0]["id"], r[0]["value"]) if r else (None, None)


if mode == "undo":
    for row in json.load(open(sys.argv[3], encoding="utf-8")):
        X(row["model"], "write", [row["id"]], row["before"])
        print("restaurado", row["model"], row["id"])
    sys.exit(0)

if not X("ir.module.module", "search_count", [("name", "=", MODULE), ("state", "=", "installed")]):
    raise SystemExit(f"{MODULE} is not installed here: install it first.")
own = {r["res_id"] for r in X("ir.model.data", "search_read", [("module", "=", MODULE), ("model", "=", "base.automation")], fields=["res_id"])}

plan = []
types, categs = [], []
for a in X("base.automation", "search_read", [("active", "=", True), ("model_id.model", "in", ["purchase.order", "stock.picking"])],
           fields=["name", "model_id", "filter_domain", "action_server_ids"]):
    if a["id"] in own:
        continue
    dom = a["filter_domain"] or ""
    studio_flag = "x_studio_partial_delivery" in dom and a["model_id"][1] and "picking_type_id" in dom
    studio_cancel = "Store App-Creado parcial" in dom
    if not (studio_flag or studio_cancel):
        continue
    if studio_flag:
        m = re.search(r"picking_type_id['\"],\s*['\"]not in['\"],\s*\[([0-9,\s]*)\]", dom)
        types = [int(x) for x in (m.group(1).split(",") if m else []) if x.strip()]
    if studio_cancel:
        m = re.search(r"categ_id['\"],\s*['\"]not in['\"],\s*\[([0-9,\s]*)\]", dom)
        categs = [int(x) for x in (m.group(1).split(",") if m else []) if x.strip()]
    plan.append(("base.automation", a["id"], a["name"], {"active": True}, {"active": False}))

for key, ids in ((P_TYPES, types), (P_CATEG, categs)):
    pid, val = param_id(key)
    if pid and ids:
        plan.append(("ir.config_parameter", pid, key, {"value": val}, {"value": ",".join(str(i) for i in ids)}))

for model, rid, name, before, after in plan:
    print(f"  {model} {rid} «{name}»: {before} -> {after}")
if mode != "apply":
    print(len(plan), "cambios (no se ha tocado nada; añade 'apply')")
    sys.exit(0)
path = f"retirar_studio_entregas_parciales_{env}_{datetime.datetime.now():%Y%m%d-%H%M%S}.json"
json.dump([{"model": m, "id": i, "name": n, "before": b} for m, i, n, b, _a in plan], open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("copia de seguridad:", os.path.abspath(path))
for model, rid, _n, _b, after in plan:
    X(model, "write", [rid], after)
print(len(plan), "cambios hechos. Para deshacer: undo", path)

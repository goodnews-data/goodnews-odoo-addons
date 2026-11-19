"""Remove the old Studio planner (x_planificador_master_) in a safe order.

Run it from a machine with the GN Tools .env (it is NOT part of the Odoo module):

    python -I retirar_planificador_studio.py <path/.env> <test|prod> <dry|apply>

`dry` only lists what would be deleted. Rehearsed on goodnews-test on 17/11/2026.

Order (each step removes what blocks the next one):
  cron -> menus -> window actions -> saved filters -> views (inherited first)
  -> record rules -> server actions -> automations -> computed fields
  -> model (Odoo drops its fields, defaults, access rights and table)
  -> the Studio xmlids that pointed to those records.
"""
import sys
import xmlrpc.client

from dotenv import dotenv_values

MODEL = "x_planificador_master_"
CTX = {"active_test": False}

env = dotenv_values(sys.argv[1])
target, mode = sys.argv[2], sys.argv[3]
assert target in ("test", "prod") and mode in ("dry", "apply")
pre = "ODOO_" if target == "test" else "ODOO_PROD_"
url, db, pwd = env[pre + "URL"], env[pre + "DB"], env[pre + "PASSWORD"]
if target == "test":
    assert "test" in url, "ODOO_URL is not the test database"
uid = xmlrpc.client.ServerProxy(url + "/xmlrpc/2/common").authenticate(db, env[pre + "USERNAME"], pwd, {})
rpc = xmlrpc.client.ServerProxy(url + "/xmlrpc/2/object", allow_none=True)


def x(model, method, *args, **kw):
    return rpc.execute_kw(db, uid, pwd, model, method, list(args), kw)


touched = []  # (model, ids) of everything removed, to clean their xmlids at the end


def step(label, model, ids):
    print("%-24s %-24s %s" % (label, model, ids))
    touched.append((model, ids))
    if ids and mode == "apply":
        x(model, "unlink", ids)


model_ids = x("ir.model", "search", [["model", "=", MODEL]])
if not model_ids:
    print("The old planner is already gone.")
    sys.exit(0)

# Records that disappear together with the model: collect them first for the xmlid cleanup
touched.append(("ir.model.fields", x("ir.model.fields", "search", [["model_id", "in", model_ids]])))
touched.append(("ir.model.access", x("ir.model.access", "search", [["model_id", "in", model_ids]], context=CTX)))

step("cron", "ir.cron", x("ir.cron", "search", [["model_id", "in", model_ids]], context=CTX))
actions = x("ir.actions.act_window", "search", [["res_model", "=", MODEL]])
step("menus", "ir.ui.menu", x("ir.ui.menu", "search", [
    ["action", "in", ["ir.actions.act_window,%s" % a for a in actions]]], context=CTX))
step("window actions", "ir.actions.act_window", actions)
step("saved filters", "ir.filters", x("ir.filters", "search", [["model_id", "=", MODEL]], context=CTX))
views = x("ir.ui.view", "search_read", [["model", "=", MODEL]], fields=["inherit_id"], context=CTX)
step("views (inherited)", "ir.ui.view", [v["id"] for v in views if v["inherit_id"]])
step("views (base)", "ir.ui.view", [v["id"] for v in views if not v["inherit_id"]])
step("record rules", "ir.rule", x("ir.rule", "search", [["model_id", "in", model_ids]], context=CTX))
step("server actions", "ir.actions.server", x("ir.actions.server", "search", [["model_id", "in", model_ids]]))
step("automations", "base.automation", x("base.automation", "search", [["model_id", "in", model_ids]], context=CTX))
# A computed field blocks the model deletion while it depends on another field
step("computed fields", "ir.model.fields", x("ir.model.fields", "search", [
    ["model_id", "in", model_ids], ["state", "=", "manual"], ["compute", "!=", False]]))
step("MODEL", "ir.model", model_ids)

# Studio xmlids of the removed records only (never other dangling ones)
xmlids = []
for model, ids in touched:
    if ids:
        xmlids += x("ir.model.data", "search", [["model", "=", model], ["res_id", "in", ids],
                                               ["module", "=", "studio_customization"]])
if mode == "apply":
    xmlids = [d["id"] for d in x("ir.model.data", "read", xmlids, fields=["model", "res_id"])
              if not x(d["model"], "search", [["id", "=", d["res_id"]]], context=CTX)]
step("studio xmlids", "ir.model.data", xmlids)
if mode == "apply":
    print("Old planner left:", x("ir.model", "search_count", [["model", "=", MODEL]]))

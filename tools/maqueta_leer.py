"""Read every Studio development of GoodNews from Odoo (READ ONLY) into a cache json.

Step 1 of the migration mockup: tools/maqueta_generar.py builds the modules from this cache,
offline. Nothing is written in Odoo.

Which records belong to which development comes from tools/desarrollos.json (the map of the
Manual de Isabella), expanded with everything that hangs from each custom model (fields,
views, access rights, record rules, window actions, menus, actions on the model). What the
map does not cover is read too:
  - custom models of no development -> pseudo development "modelos-sueltos"
  - custom fields of no development -> pseudo development "campos-sueltos"
  - Studio views of no development  -> "vistas_studio_sueltas" (one shared module)
  - custom groups (without a module xml id) referenced by any of the above

Usage (from the GN Tools repo, it reads the Odoo credentials of its .env):
  python <addons>/tools/maqueta_leer.py <test|prod> <out.json>
"""
import json
import os
import sys

sys.path.insert(0, os.getcwd())
from platform_app.modules.proveedores.config import get_settings  # noqa: E402
from platform_app.modules.proveedores.odoo_client import OdooClient  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
env, out_path = sys.argv[1], sys.argv[2]
st = get_settings()
c = st.odoo_prod_conn() if env == "prod" else st.odoo_conn()
assert ("test" in c.odoo_db) == (env == "test"), c.odoo_db
cl = OdooClient(c.odoo_url, c.odoo_db, c.odoo_username, c.odoo_password, timeout=600)
CTX = {"lang": "en_US", "active_test": False}
STUDIO = ("studio_customization", "__export__", "__custom__")


def X(model, method, *args, **kw):
    kw.setdefault("context", CTX)
    return cl.execute_kw(model, method, list(args), kw)


SKIP = {"__last_update", "create_uid", "create_date", "write_uid", "write_date", "display_name"}
cache = {"env": env, "db": c.odoo_db, "records": {}, "xmlids": {}, "devs": {}, "nombres": {}}
fields_of = {}


def readable(model):
    if model not in fields_of:
        meta = X(model, "fields_get", attributes=["type"])
        fields_of[model] = [f for f, m in meta.items()
                            if f not in SKIP and m["type"] != "binary"
                            and not f.startswith(("message_", "activity_", "website_message"))]
    return fields_of[model]


def fetch(model, ids):
    bucket = cache["records"].setdefault(model, {})
    ids = [i for i in set(ids) if str(i) not in bucket]
    if ids:
        for r in X(model, "read", ids, fields=readable(model)):
            bucket[str(r["id"])] = r
    return [bucket[str(i)] for i in ids]


def process(dev_id, nombre, descripcion, piezas):
    want = {}
    for model, rid in piezas:
        want.setdefault(model, set()).add(rid)
    model_ids = sorted(want.get("ir.model", []))
    if model_ids:
        names = [m["model"] for m in X("ir.model", "read", model_ids, fields=["model"])]
        dom_m = [("model_id", "in", model_ids)]
        want.setdefault("ir.model.fields", set()).update(
            X("ir.model.fields", "search", dom_m + [("state", "=", "manual")]))
        want.setdefault("ir.ui.view", set()).update(X("ir.ui.view", "search", [("model", "in", names)]))
        want.setdefault("ir.model.access", set()).update(X("ir.model.access", "search", dom_m))
        want.setdefault("ir.rule", set()).update(X("ir.rule", "search", dom_m))
        acts = X("ir.actions.act_window", "search", [("res_model", "in", names)])
        want.setdefault("ir.actions.act_window", set()).update(acts)
        want.setdefault("ir.actions.server", set()).update(
            X("ir.actions.server", "search", dom_m + [("usage", "=", "ir_actions_server")]))
        want.setdefault("ir.cron", set()).update(X("ir.cron", "search", dom_m))
        want.setdefault("base.automation", set()).update(X("base.automation", "search", dom_m))
        if acts:
            refs = ["ir.actions.act_window,%s" % a for a in acts]
            want.setdefault("ir.ui.menu", set()).update(X("ir.ui.menu", "search", [("action", "in", refs)]))
    for a in fetch("base.automation", want.get("base.automation", [])):
        want.setdefault("ir.actions.server", set()).update(a.get("action_server_ids") or [])
    fetch("base.automation", want.get("base.automation", []))
    menus = fetch("ir.ui.menu", want.get("ir.ui.menu", []))
    while menus:   # Studio parent menus come along (they do not exist in a new base)
        parents = []
        for m in menus:
            if m.get("action"):
                amodel, aid = m["action"].split(",")
                if amodel in ("ir.actions.act_window", "ir.actions.act_url"):
                    want.setdefault(amodel, set()).add(int(aid))
            p = m.get("parent_id") and m["parent_id"][0]
            if p and p not in want["ir.ui.menu"]:
                xs = [r["module"] for r in X("ir.model.data", "search_read",
                                             [("model", "=", "ir.ui.menu"), ("res_id", "=", p)], fields=["module"])]
                if not xs or all(x in ("studio_customization", "__export__", "__custom__") for x in xs):
                    want["ir.ui.menu"].add(p)
                    parents.append(p)
        menus = fetch("ir.ui.menu", parents)
    for model, ids in want.items():
        fetch(model, ids)
    # Fixed selection values written by server actions
    sel_vals = {a["selection_value"][0] for a in cache["records"].get("ir.actions.server", {}).values()
                if a["id"] in want.get("ir.actions.server", set()) and a.get("selection_value")}
    fetch("ir.model.fields.selection", sel_vals)
    sel_fields = [int(i) for i in want.get("ir.model.fields", [])
                  if cache["records"]["ir.model.fields"][str(i)]["ttype"] in ("selection", "reference")]
    if sel_fields:
        sel = X("ir.model.fields.selection", "search", [("field_id", "in", sel_fields)])
        fetch("ir.model.fields.selection", sel)
        want["ir.model.fields.selection"] = set(sel)
    cache["devs"][dev_id] = {"nombre": nombre, "descripcion": descripcion,
                             "piezas": {m: sorted(int(i) for i in ids) for m, ids in want.items() if ids}}
    print(dev_id, {m: len(ids) for m, ids in want.items() if ids})


desarrollos = json.load(open(os.path.join(HERE, "desarrollos.json"), encoding="utf-8"))
for dev in desarrollos:
    process(dev["id"], dev["nombre"], dev["descripcion"], dev["piezas"])

# Custom models of no development
covered = {i for d in cache["devs"].values() for i in d["piezas"].get("ir.model", [])}
loose_models = sorted(set(X("ir.model", "search", [("state", "=", "manual")])) - covered)
if loose_models:
    process("modelos-sueltos", "Modelos sueltos de Studio",
            "Modelos creados con Studio que el mapa del Manual no asigna a ningún desarrollo.",
            [["ir.model", i] for i in loose_models])
# Custom fields of no development
covered = {i for d in cache["devs"].values() for i in d["piezas"].get("ir.model.fields", [])}
loose_fields = sorted(set(X("ir.model.fields", "search", [("state", "=", "manual")])) - covered)
if loose_fields:
    process("campos-sueltos", "Campos sueltos de Studio",
            "Campos creados con Studio en modelos de Odoo que el mapa del Manual no asigna a ningún desarrollo.",
            [["ir.model.fields", i] for i in loose_fields])

# Studio views of no development
studio_views = X("ir.model.data", "search_read",
                 [("module", "=", "studio_customization"), ("model", "=", "ir.ui.view")], fields=["res_id"])
assigned = {i for d in cache["devs"].values() for i in d["piezas"].get("ir.ui.view", [])}
loose = sorted({r["res_id"] for r in studio_views} - assigned)
fetch("ir.ui.view", loose)
cache["vistas_studio_sueltas"] = loose
print("vistas de Studio sin desarrollo:", len(loose))


def xmlids_for(model, ids):
    bucket = cache["xmlids"].setdefault(model, {})
    ids = [i for i in set(ids) if str(i) not in bucket]
    if not ids:
        return
    for i in ids:
        bucket[str(i)] = []
    for r in X("ir.model.data", "search_read", [("model", "=", model), ("res_id", "in", ids)],
               fields=["module", "name", "res_id"]):
        bucket[str(r["res_id"])].append(r["module"] + "." + r["name"])


def relations():
    rel = {}
    for model, rows in cache["records"].items():
        meta = X(model, "fields_get", attributes=["type", "relation"])
        for r in rows.values():
            for f, v in r.items():
                t = meta.get(f, {})
                if t.get("type") == "many2one" and v:
                    rel.setdefault(t["relation"], set()).add(v[0])
                elif t.get("type") == "many2many" and v:
                    rel.setdefault(t["relation"], set()).update(v)
    for model, rows in cache["records"].items():
        rel.setdefault(model, set()).update(int(i) for i in rows)
    for model, ids in rel.items():
        xmlids_for(model, ids)
    return rel


rel = relations()
# Custom groups: no xml id of a real module -> read them so a module can create them
groups = [g for g in rel.get("res.groups", [])
          if not any(not x.startswith(STUDIO) for x in cache["xmlids"]["res.groups"].get(str(g), []))]
fetch("res.groups", groups)
cache["grupos_propios"] = sorted(groups)
rel = relations()
for model, key in (("ir.model", ["model"]), ("res.groups", ["full_name"]), ("ir.model.fields", ["name", "model"])):
    ids = sorted(rel.get(model, []))
    if ids:
        cache["nombres"][model] = {str(r["id"]): r for r in X(model, "read", ids, fields=key)}
json.dump(cache, open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
print("ok", out_path)

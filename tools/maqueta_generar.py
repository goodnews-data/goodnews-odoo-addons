"""Build one installable module per Studio development from the cache of maqueta_leer.py.

Step 2 of the migration mockup (offline, nothing touches Odoo). For every development of
tools/desarrollos.json that is not migrated yet:
  gn_<dev>_base : custom models, custom fields (with their selection values), access rights
  gn_<dev>      : views of its models, window actions, menus, server actions, automations,
                  scheduled actions (installed OFF), record rules
plus the shared pieces:
  gn_studio_grupos : custom groups without a module (the Supply / Data ones live in gn_base)
  gn_studio_vistas : the Studio customisations of standard views (one view mixes fields of
                     several developments, so they go together, installed last)

Technical names are kept (x_studio_..., x_control_de_desecho...): the GN Tools reads them by
name. So, like the other *_base modules, the result installs only in a database WITHOUT the
Studio development (a new or migrated one), never in the current GoodNews ones.

Usage: python tools/maqueta_generar.py <cache.json> [<out_dir>]   (default out_dir: repo root)
Writes the module folders, MAQUETA.md (install order) and maqueta_avisos.txt (what needs a
human look).
"""
import json
import os
import re
import sys
from xml.sax.saxutils import escape, quoteattr

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
cache = json.load(open(sys.argv[1], encoding="utf-8"))
OUT = sys.argv[2] if len(sys.argv) > 2 else ROOT
R, XI, NM = cache["records"], cache["xmlids"], cache.get("nombres", {})
STUDIO = ("studio_customization.", "__export__.", "__custom__.")
VERSION = "17.0.1.0.0"
REPO = "https://github.com/goodnews-data/goodnews-odoo-addons/tree/main/"
desarrollos = json.load(open(os.path.join(HERE, "desarrollos.json"), encoding="utf-8"))
avisos = []

# ---- Developments already migrated by hand: their modules --------------------------------
YA_BASE = {"planificador-inventario": "gn_inventory_planner_base", "validacion-diferida": "gn_valijas_base",
           "entregas-parciales": "gn_entregas_parciales_base", "reglas-contables": "gn_purchase_account_rules",
           "udm-proveedor": "gn_vendor_transition_uom", "master-data": "gn_launch_planner"}
YA_LOGIC = {"planificador-inventario": "gn_inventory_planner", "validacion-diferida": "gn_valijas",
            "entregas-parciales": "gn_entregas_parciales", "reglas-contables": "gn_purchase_account_rules",
            "udm-proveedor": "gn_vendor_transition_uom", "master-data": "gn_launch_planner"}
# Custom groups already created by gn_base (same name)
GROUP_MAP = {"Inventory / Supply": "gn_base.group_supply", "Dashboard / Data": "gn_base.group_data"}
NOMBRE_MODULO = {"modelos-sueltos": "gn_studio_modelos", "campos-sueltos": "gn_studio_campos"}

BASE_KINDS = ("ir.model", "ir.model.fields", "ir.model.access")
LOGIC_KINDS = ("base.automation", "ir.actions.server", "ir.actions.act_window", "ir.actions.act_url", "ir.ui.view",
               "ir.ui.menu", "ir.cron", "ir.rule")
PREFIX = {"ir.model.access": "access_", "ir.rule": "rule_", "ir.ui.view": "view_",
          "ir.actions.act_window": "action_window_", "ir.actions.act_url": "action_url_", "ir.ui.menu": "menu_",
          "ir.actions.server": "action_server_", "base.automation": "automation_", "ir.cron": "cron_",
          "res.groups": "group_"}
CORE = ["base", "web", "mail", "uom", "product", "analytic", "account", "stock", "purchase", "sale",
        "sale_management", "mrp", "point_of_sale", "hr", "hr_attendance", "event", "survey", "helpdesk",
        "quality", "quality_control", "website", "crm", "loyalty", "spreadsheet_dashboard"]


def rec(model, rid):
    return R.get(model, {}).get(str(rid))


def module_of(dev_id):
    return NOMBRE_MODULO.get(dev_id, "gn_" + dev_id.replace("-", "_"))


def studio_like(xmlid):
    """Xml ids that do not come from a module data file (they will not exist in a new base)."""
    # quality worksheets: Odoo generates their model, views and action when the template is created
    return xmlid.startswith(STUDIO) or re.search(
        r"_ir_(model|model_fields?|model_access|ui_view|actions_act_window|ui_menu)_\d+$", xmlid)


def real_xmlids(model, rid):
    return [x for x in XI.get(model, {}).get(str(rid), []) if not studio_like(x)]


def best_xmlid(xs, hint=""):
    mods = {x.split(".")[0]: x for x in xs}
    prefix = hint.split(".")[0]
    if prefix in mods:
        return mods[prefix]
    for m in CORE:
        if m in mods:
            return mods[m]
    return sorted(xs)[0]


def lname(model, r):
    if model == "ir.model":
        return "model_" + r["model"].replace(".", "_")
    if model == "ir.model.fields":
        return "field_%s__%s" % (r["model"].replace(".", "_"), r["name"])
    return PREFIX[model] + str(r["id"])


# ---- 1. Who owns what ----------------------------------------------------------------------
owner = {}          # (model, id) -> (module, local name)
ya = {}             # (model, id) -> dev id of an already migrated development
modules = {}        # module -> {"dev", "nombre", "descripcion", "base": bool, "records": {model: [ids]}}
custom_model_owner = {}   # model name -> module (logic) that owns its views/actions

devs = [(d["id"], d.get("ya_migrado")) for d in desarrollos] + [(k, None) for k in ("modelos-sueltos", "campos-sueltos")]
for dev_id, migrated in devs:
    info = cache["devs"].get(dev_id)
    if not info:
        continue
    if migrated:
        for model, ids in info["piezas"].items():
            for i in ids:
                ya.setdefault((model, i), dev_id)
        continue
    base_mod, logic_mod = module_of(dev_id) + "_base", module_of(dev_id)
    for model in BASE_KINDS + LOGIC_KINDS:
        for i in info["piezas"].get(model, []):
            r = rec(model, i)
            if r is None or (model, i) in owner:
                continue
            if model in ("ir.model", "ir.model.fields") and r.get("state") != "manual":
                continue
            if real_xmlids(model, i):
                continue   # it comes from a real module (gn_*, quality...): nothing to carry
            if model == "ir.ui.view":
                if r["model"] not in custom_model_owner:
                    continue   # Studio customisation of a standard view -> gn_studio_vistas
            mod = base_mod if model in BASE_KINDS else logic_mod
            owner[(model, i)] = (mod, lname(model, r))
            m = modules.setdefault(mod, {"dev": dev_id, "nombre": info["nombre"], "descripcion": info["descripcion"],
                                         "base": mod == base_mod, "records": {}})
            m["records"].setdefault(model, []).append(i)
            if model == "ir.model":
                custom_model_owner[r["model"]] = logic_mod
    # views of the custom models of the development (second pass: needs custom_model_owner)
    for i in info["piezas"].get("ir.ui.view", []):
        r = rec("ir.ui.view", i)
        if r and (("ir.ui.view", i) not in owner) and r["model"] in custom_model_owner and not real_xmlids("ir.ui.view", i):
            mod = custom_model_owner[r["model"]]
            owner[("ir.ui.view", i)] = (mod, lname("ir.ui.view", r))
            modules.setdefault(mod, {"dev": dev_id, "nombre": info["nombre"], "descripcion": info["descripcion"],
                                     "base": False, "records": {}})["records"].setdefault("ir.ui.view", []).append(i)

migrated_models = {rec("ir.model", i)["model"] for (m, i) in ya if m == "ir.model" and rec("ir.model", i)}

# Shared: custom groups
for g in cache.get("grupos_propios", []):
    r = rec("res.groups", g)
    if r and r["full_name"] not in GROUP_MAP:
        owner[("res.groups", g)] = ("gn_studio_grupos", lname("res.groups", r))
        modules.setdefault("gn_studio_grupos", {"dev": None, "nombre": "Grupos propios",
                                                "descripcion": "Grupos de permisos creados a mano en Odoo (Supply y Data van en gn_base).",
                                                "base": True, "records": {}})["records"].setdefault("res.groups", []).append(g)
# Shared: Studio customisations of standard views (of every development not migrated yet)
already = {i for (m, i), _ in ya.items() if m == "ir.ui.view"}
for dev_id, migrated in devs:
    if migrated or dev_id not in cache["devs"]:
        continue
    for i in cache["devs"][dev_id]["piezas"].get("ir.ui.view", []):
        if ("ir.ui.view", i) not in owner and not real_xmlids("ir.ui.view", i):
            cache.setdefault("vistas_studio_sueltas", []).append(i)
for i in sorted(set(cache.get("vistas_studio_sueltas", []))):
    r = rec("ir.ui.view", i)
    if r is None or ("ir.ui.view", i) in owner or i in already or real_xmlids("ir.ui.view", i):
        continue
    if r["model"] in migrated_models:
        continue   # view of a model of a development migrated by hand: its module has its own views
    if re.search(r"in_group_|sel_groups_", r.get("arch_db") or ""):
        avisos.append("no se copia la vista %s (%s): toca la pestaña de permisos del usuario, que Odoo genera según los "
                      "grupos instalados (no es portable); lo que añade (almacén/central asignado) ya lo hace gn_base" % (i, r["name"]))
        continue
    if r["model"].startswith("x_") and r["model"] not in custom_model_owner:
        avisos.append("no se copia la vista %s (%s): su modelo %s ya no existe" % (i, r["name"], r["model"]))
        continue
    if r["model"] in custom_model_owner:
        mod = custom_model_owner[r["model"]]
    else:
        mod = "gn_studio_vistas"
        modules.setdefault(mod, {"dev": None, "nombre": "Vistas de Studio",
                                 "descripcion": "Cambios hechos con Studio en vistas estándar de Odoo (formularios, listas, búsquedas). "
                                                "Una misma vista mezcla campos de varios desarrollos, por eso van juntas y se instalan al final.",
                                 "base": False, "records": {}})
    owner[("ir.ui.view", i)] = (mod, lname("ir.ui.view", r))
    modules[mod]["records"].setdefault("ir.ui.view", []).append(i)

# Studio xml id -> owner (to rewrite references inside arch / code / domains)
studio_ref = {}
for model, bucket in XI.items():
    for rid, xs in bucket.items():
        for x in xs:
            if studio_like(x) and (model, int(rid)) in owner:
                studio_ref[x] = owner[(model, int(rid))]


# ---- 2. References -----------------------------------------------------------------------
class Ctx:
    def __init__(self, mod):
        self.mod, self.deps, self.unres = mod, set(), []

    def ref(self, model, rid, hint=""):
        """xml id usable from self.mod, or None."""
        key = (model, rid)
        if key in owner:
            mod, name = owner[key]
            if mod == self.mod:
                return name
            self.deps.add(mod)
            return mod + "." + name
        if model == "res.groups":
            g = NM.get("res.groups", {}).get(str(rid)) or rec("res.groups", rid) or {}
            if g.get("full_name") in GROUP_MAP:
                self.deps.add("gn_base")
                return GROUP_MAP[g["full_name"]]
        xs = real_xmlids(model, rid)
        if xs:
            x = best_xmlid(xs, hint)
            self.deps.add(x.split(".")[0])
            return x
        if key in ya:
            dev = ya[key]
            self.deps.add(YA_BASE[dev] if model in BASE_KINDS else YA_LOGIC[dev])
        return None

    def model_hint(self, model, rid):
        if model == "ir.model":
            n = NM.get("ir.model", {}).get(str(rid)) or rec("ir.model", rid) or {}
            return n.get("model", "")
        if model == "ir.model.fields":
            n = NM.get("ir.model.fields", {}).get(str(rid)) or rec("ir.model.fields", rid) or {}
            return n.get("model", "")
        return ""

    def m2o(self, field, model, value):
        if not value:
            return None
        rid = value[0]
        x = self.ref(model, rid, self.model_hint(model, rid))
        if x:
            return '<field name="%s" ref="%s"/>' % (field, x)
        if model == "ir.model":
            name = self.model_hint(model, rid)
            return '<field name="%s" search="[(\'model\', \'=\', %r)]"/>' % (field, name)
        if model == "ir.model.fields":
            n = NM.get("ir.model.fields", {}).get(str(rid)) or rec("ir.model.fields", rid)
            return '<field name="%s" search="[(\'model\', \'=\', %r), (\'name\', \'=\', %r)]"/>' % (
                field, n["model"], n["name"])
        self.unres.append("%s -> %s %s %s (sin equivalente: se omite)" % (field, model, rid, value[1] if len(value) > 1 else ""))
        return None

    def m2m(self, field, model, ids):
        if not ids:
            return None
        parts = []
        for rid in ids:
            x = self.ref(model, rid, self.model_hint(model, rid))
            if x:
                parts.append("ref(%r)" % x)
            elif model == "ir.model.fields":
                n = NM.get("ir.model.fields", {}).get(str(rid)) or rec("ir.model.fields", rid)
                parts.append("obj().env['ir.model.fields']._get(%r, %r).id" % (n["model"], n["name"]))
            else:
                self.unres.append("%s -> %s %s (sin equivalente: se omite)" % (field, model, rid))
        if not parts:
            return None
        return '<field name="%s" eval="[Command.set([%s])]"/>' % (field, ", ".join(parts))

    def rewrite(self, text):
        """Rewrite Studio xml ids inside arch / code / domains to the generated ones."""
        if not text:
            return text

        def sub(m):
            x = m.group(0)
            if x in studio_ref:
                mod, name = studio_ref[x]
                if mod != self.mod:
                    self.deps.add(mod)
                return name if mod == self.mod else mod + "." + name
            self.unres.append("referencia de Studio sin equivalente en el texto: " + x)
            return x
        return re.sub(r"studio_customization\.[\w\-]+", sub, text)

    def arch(self, text):
        text = self.rewrite(text)

        def btn(m):
            tag = m.group(0)
            nm = re.search(r'\bname="(\d+)"', tag)
            if not nm or 'type="action"' not in tag:
                return tag
            rid = int(nm.group(1))
            x = None
            for model in ("ir.actions.server", "ir.actions.act_window"):
                if rec(model, rid) is not None or real_xmlids(model, rid) or (model, rid) in owner:
                    x = self.ref(model, rid)
                    if x:
                        break
            if not x:
                self.unres.append("botón con la acción %s sin equivalente (se deja el número)" % rid)
                return tag
            return tag.replace(nm.group(0), 'name="%%(%s)d"' % x)
        return re.sub(r"<button\b[^>]*>", btn, text)


def txt(field, value):
    return '<field name="%s">%s</field>' % (field, escape(str(value)))


def code(field, value):
    value = str(value).replace("]]>", "]]]]><![CDATA[>")
    return '<field name="%s"><![CDATA[%s]]></field>' % (field, value)


def boolean(field, value):
    return '<field name="%s" eval="%s"/>' % (field, bool(value))


def integer(field, value):
    return '<field name="%s" eval="%d"/>' % (field, int(value))


# ---- 3. Record writers ---------------------------------------------------------------------
def w_model(cx, r):
    out = [txt("name", r["name"]), txt("model", r["model"]), txt("state", "manual")]
    out += [boolean("is_mail_thread", r.get("is_mail_thread")), boolean("is_mail_activity", r.get("is_mail_activity"))]
    if r.get("is_mail_thread") or r.get("is_mail_activity"):
        cx.deps.add("mail")
    return out


FIELD_TEXT = ("relation", "relation_field", "relation_table", "column1", "column2", "related", "depends",
              "on_delete", "currency_field")


def w_field(cx, r):
    out = [txt("name", r["name"]), cx.m2o("model_id", "ir.model", r["model_id"]),
           txt("field_description", r["field_description"]), txt("ttype", r["ttype"]), txt("state", "manual")]
    for f in FIELD_TEXT:
        if r.get(f) and not (f == "on_delete" and r["ttype"] != "many2one"):
            out.append(txt(f, r[f]))
    if r.get("domain") and r["domain"] != "[]":
        out.append(txt("domain", cx.rewrite(r["domain"])))
    for f in ("required", "readonly", "index", "copied", "store", "translate", "sanitize", "group_expand"):
        if f in r and isinstance(r[f], bool):
            out.append(boolean(f, r[f]))
    if r.get("size"):
        out.append(integer("size", r["size"]))
    if r.get("tracking"):
        out.append(integer("tracking", r["tracking"]))
    if r.get("help"):
        out.append(txt("help", r["help"]))
    if r.get("compute"):
        out.append(code("compute", r["compute"]))
    if r["ttype"] in ("selection", "reference"):
        sels = sorted((s for s in R.get("ir.model.fields.selection", {}).values() if s["field_id"][0] == r["id"]),
                      key=lambda s: (s["sequence"], s["id"]))
        if sels:
            vals = ", ".join("Command.create({'value': %r, 'name': %r, 'sequence': %d})" % (s["value"], s["name"], s["sequence"])
                             for s in sels)
            out.append('<field name="selection_ids" eval="[%s]"/>' % escape(vals))
        else:
            avisos.append("%s: campo de selección %s.%s sin valores" % (cx.mod, r["model"], r["name"]))
    if r["ttype"] in ("many2one", "one2many", "many2many") and r.get("relation"):
        model_rec = next((m for m in R.get("ir.model", {}).values() if m["model"] == r["relation"]), None)
        if model_rec:
            cx.ref("ir.model", model_rec["id"], r["relation"])
    return out


def w_access(cx, r):
    return [txt("name", r["name"]), cx.m2o("model_id", "ir.model", r["model_id"]),
            cx.m2o("group_id", "res.groups", r.get("group_id")),
            boolean("perm_read", r["perm_read"]), boolean("perm_write", r["perm_write"]),
            boolean("perm_create", r["perm_create"]), boolean("perm_unlink", r["perm_unlink"]),
            boolean("active", r.get("active", True))]


def w_group(cx, r):
    out = [txt("name", r["name"]), cx.m2o("category_id", "ir.module.category", r.get("category_id")),
           cx.m2m("implied_ids", "res.groups", r.get("implied_ids"))]
    if r.get("comment"):
        out.append(txt("comment", r["comment"]))
    return out


def w_rule(cx, r):
    return [txt("name", r["name"]), cx.m2o("model_id", "ir.model", r["model_id"]),
            txt("domain_force", cx.rewrite(r.get("domain_force") or "[]")),
            cx.m2m("groups", "res.groups", r.get("groups")),
            boolean("perm_read", r["perm_read"]), boolean("perm_write", r["perm_write"]),
            boolean("perm_create", r["perm_create"]), boolean("perm_unlink", r["perm_unlink"]),
            boolean("active", r.get("active", True))]


def w_view(cx, r):
    out = [txt("name", r["name"]), txt("model", r["model"])]
    if not r.get("inherit_id") or r.get("mode") == "primary":
        out.append(txt("type", r["type"]))
    out += [cx.m2o("inherit_id", "ir.ui.view", r.get("inherit_id")), integer("priority", r.get("priority") or 16)]
    if r.get("inherit_id"):
        out.append(txt("mode", r.get("mode") or "extension"))
    out += [boolean("active", r.get("active", True)), cx.m2m("groups_id", "res.groups", r.get("groups_id"))]
    if r.get("inherit_id") and not out[2]:
        avisos.append("%s: la vista %s (%s) hereda de una vista que no existe en una base nueva" % (cx.mod, r["id"], r["name"]))
    arch = cx.arch(r.get("arch_db") or r.get("arch") or "")
    out.append('<field name="arch" type="xml">%s</field>' % arch)
    return out


def w_act_window(cx, r, with_views):
    out = [txt("name", r["name"]), txt("res_model", r["res_model"]), txt("view_mode", r.get("view_mode") or "tree,form")]
    for f in ("domain", "context", "binding_view_types"):
        if r.get(f) and r[f] not in ("[]", "{}"):
            out.append(txt(f, cx.rewrite(r[f])))
    if r.get("target") and r["target"] != "current":
        out.append(txt("target", r["target"]))
    if r.get("limit") and r["limit"] != 80:
        out.append(integer("limit", r["limit"]))
    if r.get("help"):
        out.append('<field name="help" type="html">%s</field>' % r["help"])
    out += [cx.m2o("binding_model_id", "ir.model", r.get("binding_model_id")),
            cx.m2m("groups_id", "res.groups", r.get("groups_id"))]
    if with_views:
        out += [cx.m2o("view_id", "ir.ui.view", r.get("view_id")), cx.m2o("search_view_id", "ir.ui.view", r.get("search_view_id"))]
    return out


def w_menu(cx, r):
    out = [txt("name", r["name"]), cx.m2o("parent_id", "ir.ui.menu", r.get("parent_id")),
           integer("sequence", r.get("sequence") or 10), boolean("active", r.get("active", True)),
           cx.m2m("groups_id", "res.groups", r.get("groups_id"))]
    if r.get("action"):
        model, rid = r["action"].split(",")
        x = cx.ref(model, int(rid))
        if x:
            out.append('<field name="action" ref="%s"/>' % x)
        else:
            cx.unres.append("menú %s: acción %s sin equivalente" % (r["id"], r["action"]))
    if r.get("web_icon"):
        out.append(txt("web_icon", r["web_icon"]))
    return out


SERVER_M2O = {"crud_model_id": "ir.model", "link_field_id": "ir.model.fields", "update_field_id": "ir.model.fields",
              "template_id": "mail.template", "base_automation_id": "base.automation",
              "update_related_model_id": "ir.model"}
SERVER_TXT = ("update_path", "update_m2m_operation", "update_boolean_value", "evaluation_type",
              "mail_post_method", "webhook_url", "binding_view_types")


def w_server(cx, r, is_cron=False):
    out = [txt("name", r["name"]), cx.m2o("model_id", "ir.model", r["model_id"]), txt("state", r["state"])]
    if r.get("usage") and r["usage"] not in ("ir_actions_server", "ir_cron"):
        out.append(txt("usage", r["usage"]))
    if r.get("code") and r["state"] == "code":
        out.append(code("code", cx.rewrite(r["code"])))
    if not is_cron:
        out.append(cx.m2o("binding_model_id", "ir.model", r.get("binding_model_id")))
        if r.get("binding_type") and r["binding_type"] != "action":
            out.append(txt("binding_type", r["binding_type"]))
        out.append(cx.m2m("groups_id", "res.groups", r.get("groups_id")))
    if r["state"] != "code":
        for f, model in SERVER_M2O.items():
            if f != "base_automation_id" and r.get(f):
                out.append(cx.m2o(f, model, r[f]))
        for f in SERVER_TXT:
            if r.get(f) and f != "binding_view_types":
                out.append(txt(f, r[f]))
        if r.get("value"):
            out.append(txt("value", cx.rewrite(r["value"])))
        if r.get("selection_value"):
            out.append(selection_value(cx, r))
        out.append(cx.m2m("child_ids", "ir.actions.server", r.get("child_ids")))
    if r.get("binding_view_types") and not is_cron and r.get("binding_model_id"):
        out.append(txt("binding_view_types", r["binding_view_types"]))
    if r.get("base_automation_id"):
        out.append(cx.m2o("base_automation_id", "base.automation", r["base_automation_id"]))
    if r.get("sequence") and r["sequence"] != 5:
        out.append(integer("sequence", r["sequence"]))
    return out


def selection_value(cx, r):
    sid = r["selection_value"][0]
    x = cx.ref("ir.model.fields.selection", sid)
    if x:
        return '<field name="selection_value" ref="%s"/>' % x
    s = rec("ir.model.fields.selection", sid)
    f = r.get("update_field_id") and (NM.get("ir.model.fields", {}).get(str(r["update_field_id"][0]))
                                      or rec("ir.model.fields", r["update_field_id"][0]))
    if not s or not f:
        cx.unres.append("acción %s: valor de selección fijo %s sin equivalente" % (r["id"], r["selection_value"]))
        return None
    return ("<field name=\"selection_value\" search=\"[('field_id.model', '=', %r), ('field_id.name', '=', %r), "
            "('value', '=', %r)]\"/>" % (f["model"], f["name"], s["value"]))


def w_act_url(cx, r):
    return [txt("name", r["name"]), txt("url", r["url"]), txt("target", r.get("target") or "new")]


def w_automation(cx, r):
    out = [txt("name", r["name"]), cx.m2o("model_id", "ir.model", r["model_id"]), txt("trigger", r["trigger"]),
           boolean("active", r.get("active", True))]
    for f in ("filter_pre_domain", "filter_domain"):
        if r.get(f):
            out.append(txt(f, cx.rewrite(r[f])))
    out += [cx.m2m("trigger_field_ids", "ir.model.fields", r.get("trigger_field_ids")),
            cx.m2m("on_change_field_ids", "ir.model.fields", r.get("on_change_field_ids")),
            cx.m2o("trg_selection_field_id", "ir.model.fields.selection", r.get("trg_selection_field_id")),
            cx.m2o("trg_date_id", "ir.model.fields", r.get("trg_date_id")),
            cx.m2o("trg_date_calendar_id", "resource.calendar", r.get("trg_date_calendar_id"))]
    if r.get("trg_date_id"):
        out += [integer("trg_date_range", r.get("trg_date_range") or 0), txt("trg_date_range_type", r.get("trg_date_range_type") or "day")]
    if r.get("trg_field_ref"):
        cx.unres.append("automatización %s: valor de disparo fijo (trg_field_ref=%s, %s): revisar a mano" % (
            r["id"], r["trg_field_ref"], r.get("trg_field_ref_display_name")))
    if r.get("description"):
        out.append(txt("description", r["description"]))
    if r["trigger"] == "on_webhook":
        out.append(txt("record_getter", r.get("record_getter") or ""))
    cx.deps.add("base_automation")
    return out


def w_cron(cx, r):
    out = w_server(cx, r, is_cron=True)
    out += [integer("interval_number", r["interval_number"]), txt("interval_type", r["interval_type"]),
            integer("numbercall", r.get("numbercall", -1)), boolean("doall", r.get("doall")),
            integer("priority", r.get("priority") or 5),
            boolean("active", False)]
    user = cx.m2o("user_id", "res.users", r.get("user_id"))
    if user:
        out.append(user)
    elif r.get("user_id"):
        cx.unres = [u for u in cx.unres if "user_id" not in u]
    return out


# ---- 4. Write the modules -------------------------------------------------------------------
def record_xml(model, name, fields, comment=None):
    lines = []
    if comment:
        lines.append("        <!-- %s -->" % escape(comment).replace("--", "- -"))
    lines.append('        <record id="%s" model="%s">' % (name, model))
    lines += ["            " + f for f in fields if f]
    lines.append("        </record>")
    return "\n".join(lines)


def field_order(r):
    if r.get("related") or r.get("compute"):
        return 3
    return {"one2many": 2, "many2one": 1, "many2many": 1}.get(r["ttype"], 0)


def topo_views(ids, mod):
    ids = list(ids)
    done, out = set(), []

    def visit(i):
        if i in done:
            return
        done.add(i)
        p = rec("ir.ui.view", i).get("inherit_id")
        if p and p[0] in ids and owner.get(("ir.ui.view", p[0]), (None,))[0] == mod:
            visit(p[0])
        out.append(i)
    for i in sorted(ids):
        visit(i)
    return out


def menu_depth(i):
    return (rec("ir.ui.menu", i).get("parent_path") or "").count("/"), i


def xml_file(blocks, noupdate=False):
    head = '<?xml version="1.0" encoding="utf-8"?>\n<odoo>\n'
    body = "\n\n".join(b for b in blocks if b)
    if noupdate:
        return head + '    <data noupdate="1">\n' + body + "\n    </data>\n</odoo>\n"
    return head + body + "\n</odoo>\n"


summary = {}
for mod in sorted(modules):
    m = modules[mod]
    cx = Ctx(mod)
    files = {}
    recs = m["records"]
    lists = {}   # for the README
    if m["base"]:
        blocks = []
        for i in sorted(recs.get("res.groups", [])):
            r = rec("res.groups", i)
            blocks.append(record_xml("res.groups", owner[("res.groups", i)][1], w_group(cx, r), r["full_name"]))
            lists.setdefault("Grupos", []).append(r["full_name"])
        for i in sorted(recs.get("ir.model", [])):
            r = rec("ir.model", i)
            blocks.append(record_xml("ir.model", owner[("ir.model", i)][1], w_model(cx, r)))
            lists.setdefault("Modelos", []).append("%s (%s)" % (r["name"], r["model"]))
        flds = sorted((rec("ir.model.fields", i) for i in recs.get("ir.model.fields", [])),
                      key=lambda r: (field_order(r), r["model"], r["name"]))
        for r in flds:
            blocks.append(record_xml("ir.model.fields", owner[("ir.model.fields", r["id"])][1], w_field(cx, r)))
            lists.setdefault("Campos", []).append("%s.%s (%s, %s)" % (r["model"], r["name"], r["field_description"], r["ttype"]))
        for i in sorted(recs.get("ir.model", [])):   # the order needs the fields: set it last
            r = rec("ir.model", i)
            if r.get("order") and r["order"] != "id":
                blocks.append(record_xml("ir.model", owner[("ir.model", i)][1], [txt("order", r["order"])],
                                         "Orden de la lista (después de crear sus campos)"))
        if blocks:
            files["data/models.xml"] = xml_file(blocks, noupdate=False)
        acc = [record_xml("ir.model.access", owner[("ir.model.access", i)][1], w_access(cx, rec("ir.model.access", i)))
               for i in sorted(recs.get("ir.model.access", []))]
        if acc:
            files["security/access.xml"] = xml_file(acc)
    else:
        base = mod + "_base"
        if base in modules:
            cx.deps.add(base)
        b_actions, b_views, b_menus, b_crons, b_rules = [], [], [], [], []
        for i in sorted(recs.get("base.automation", [])):
            r = rec("base.automation", i)
            b_actions.append(record_xml("base.automation", owner[("base.automation", i)][1], w_automation(cx, r),
                                        "Automatización (activa en prod: %s)" % r.get("active")))
            lists.setdefault("Automatizaciones", []).append("%s (%s, %s)" % (r["name"], r["model_name"], r["trigger"]))
        for i in sorted(recs.get("ir.actions.server", [])):
            r = rec("ir.actions.server", i)
            b_actions.append(record_xml("ir.actions.server", owner[("ir.actions.server", i)][1], w_server(cx, r)))
            lists.setdefault("Acciones de servidor", []).append("%s (%s)" % (r["name"], r["model_name"]))
        for i in sorted(recs.get("ir.actions.act_url", [])):
            r = rec("ir.actions.act_url", i)
            b_actions.append(record_xml("ir.actions.act_url", owner[("ir.actions.act_url", i)][1], w_act_url(cx, r)))
            lists.setdefault("Enlaces (acciones URL)", []).append("%s → %s" % (r["name"], r["url"]))
        for i in sorted(recs.get("ir.actions.act_window", [])):
            r = rec("ir.actions.act_window", i)
            b_actions.append(record_xml("ir.actions.act_window", owner[("ir.actions.act_window", i)][1], w_act_window(cx, r, False)))
            lists.setdefault("Acciones de ventana", []).append("%s (%s)" % (r["name"], r["res_model"]))
        for i in topo_views(recs.get("ir.ui.view", []), mod):
            r = rec("ir.ui.view", i)
            b_views.append(record_xml("ir.ui.view", owner[("ir.ui.view", i)][1], w_view(cx, r)))
            lists.setdefault("Vistas", []).append("%s (%s)" % (r["name"], r["model"]))
        for i in sorted(recs.get("ir.actions.act_window", [])):
            r = rec("ir.actions.act_window", i)
            if r.get("view_id") or r.get("search_view_id"):
                f = [x for x in (cx.m2o("view_id", "ir.ui.view", r.get("view_id")),
                                 cx.m2o("search_view_id", "ir.ui.view", r.get("search_view_id"))) if x]
                if f:
                    b_views.append(record_xml("ir.actions.act_window", owner[("ir.actions.act_window", i)][1], f,
                                              "Vistas de la acción de ventana (después de crear las vistas)"))
        for i in sorted(recs.get("ir.ui.menu", []), key=menu_depth):
            r = rec("ir.ui.menu", i)
            b_menus.append(record_xml("ir.ui.menu", owner[("ir.ui.menu", i)][1], w_menu(cx, r)))
            lists.setdefault("Menús", []).append(r["complete_name"])
        for i in sorted(recs.get("ir.cron", [])):
            r = rec("ir.cron", i)
            b_crons.append(record_xml("ir.cron", owner[("ir.cron", i)][1], w_cron(cx, r),
                                      "Se instala APAGADA. En prod: %s, cada %s %s" % (
                                          "activa" if r.get("active") else "apagada", r["interval_number"], r["interval_type"])))
            lists.setdefault("Acciones planificadas (se instalan apagadas)", []).append(
                "%s (en prod %s, cada %s %s)" % (r["name"], "activa" if r.get("active") else "apagada", r["interval_number"], r["interval_type"]))
        for i in sorted(recs.get("ir.rule", [])):
            r = rec("ir.rule", i)
            b_rules.append(record_xml("ir.rule", owner[("ir.rule", i)][1], w_rule(cx, r)))
            lists.setdefault("Reglas de registro", []).append(r["name"])
        if b_actions:
            files["data/actions.xml"] = xml_file(b_actions)
        if b_views:
            files["views/views.xml"] = xml_file(b_views)
        if b_menus:
            files["views/menus.xml"] = xml_file(b_menus)
        if b_crons:
            files["data/crons.xml"] = xml_file(b_crons, noupdate=True)
        if b_rules:
            files["security/rules.xml"] = xml_file(b_rules)
    if not files:
        continue
    order = ["security/access.xml", "data/models.xml", "data/actions.xml", "views/views.xml",
             "views/menus.xml", "data/crons.xml", "security/rules.xml"]
    if "data/models.xml" in files and "security/access.xml" in files:
        order = ["data/models.xml", "security/access.xml"] + order[2:]
    data = [f for f in order if f in files]
    deps = sorted(d for d in cx.deps if d != mod) or ["base"]
    summary[mod] = {"deps": deps, "lists": lists, "unres": cx.unres, "m": m}
    path = os.path.join(OUT, mod)
    for rel, content in files.items():
        os.makedirs(os.path.dirname(os.path.join(path, rel)), exist_ok=True)
        open(os.path.join(path, rel), "w", encoding="utf-8", newline="\n").write(content)
    open(os.path.join(path, "__init__.py"), "w", encoding="utf-8").write("")
    title = "GoodNews · " + m["nombre"] + (" (modelos)" if m["base"] and mod.endswith("_base") else "")
    manifest = {
        "name": title,
        "summary": m["descripcion"],
        "version": VERSION,
        "category": "Hidden/Tools" if m["base"] else "Productivity",
        "author": "Isabella Maffi",
        "website": REPO + mod,
        "license": "LGPL-3",
        "depends": deps,
        "data": data,
        "application": not m["base"],
        "installable": True,
    }
    open(os.path.join(path, "__manifest__.py"), "w", encoding="utf-8", newline="\n").write(
        "# Generated by tools/maqueta_generar.py from Odoo %s (%s). Migration mockup.\n" % (cache["env"], cache["db"]) +
        json.dumps(manifest, ensure_ascii=False, indent=4).replace(": true", ": True").replace(": false", ": False") + "\n")
    for u in cx.unres:
        avisos.append("%s: %s" % (mod, u))

# ---- 5. Install order, READMEs ---------------------------------------------------------------
gen = set(summary)
order, seen, cycles = [], set(), []


def visit(mod, stack=()):
    if mod in seen:
        return
    if mod in stack:
        cycles.append(" -> ".join(stack + (mod,)))
        return
    for d in summary[mod]["deps"]:
        if d in gen:
            visit(d, stack + (mod,))
    seen.add(mod)
    order.append(mod)


for mod in sorted(gen, key=lambda x: (not x.endswith("_base") and x != "gn_studio_grupos", x == "gn_studio_vistas", x)):
    visit(mod)
for c_ in cycles:
    avisos.append("CICLO de dependencias: " + c_)

for mod, s in summary.items():
    m = s["m"]
    lines = ["# %s" % ("GoodNews · " + m["nombre"] + (" (modelos)" if mod.endswith("_base") else "")), "",
             m["descripcion"], "",
             "> **Maqueta de migración.** Generado automáticamente con `tools/maqueta_generar.py` a partir de Odoo "
             "producción (solo lectura). Copia exacta de lo hecho con Studio, con los mismos nombres técnicos.", "",
             "## Cuándo se instala", "",
             "Solo en una base **sin** este desarrollo (nueva o migrada). En las bases actuales de GoodNews (test y "
             "producción) ya existe con Studio y la instalación fallaría por nombres duplicados.", "",
             "Depende de: " + ", ".join("`%s`" % d for d in s["deps"]) + ".", ""]
    if mod.endswith("_base"):
        lines += ["Va antes que `%s` (la lógica)." % mod[:-5], ""] if mod[:-5] in summary else []
    if s["lists"].get("Acciones planificadas (se instalan apagadas)"):
        lines += ["**Las acciones planificadas se instalan apagadas**: encenderlas a mano (Ajustes → Técnico → "
                  "Acciones planificadas) cuando la base tenga ya los datos. Su usuario será el que instale el módulo; "
                  "en producción eran de GoodNews Buddy.", ""]
    lines += ["## Qué contiene", ""]
    for k, v in s["lists"].items():
        lines += ["**%s** (%d)" % (k, len(v)), ""] + ["- " + x for x in v] + [""]
    if any(x.startswith("x_quality_check_worksheet") for x in s["lists"].get("Modelos", []) + s["lists"].get("Vistas", [])) or             any("x_quality_check_worksheet" in x for v in s["lists"].values() for x in v):
        lines += ["## Hoja de control de calidad", "",
                  "Este modelo es una **hoja de control de calidad** («Recepción»). En Odoo la crea la plantilla de hojas "
                  "(Calidad → Configuración → Plantillas de hojas). Aquí se crea como modelo normal con sus vistas; en la "
                  "base nueva hay que crear la plantilla «Recepción» y enlazarla a este modelo, y asignarla al punto de "
                  "control QCP00001.", ""]
    if s["unres"]:
        lines += ["## Revisar a mano", ""] + ["- " + u for u in s["unres"]] + [""]
    open(os.path.join(OUT, mod, "README.md"), "w", encoding="utf-8", newline="\n").write("\n".join(lines))

md = ["# Maqueta de migración: todos los desarrollos como zips", "",
      "Generado con `tools/maqueta_leer.py` (lee Odoo %s, solo lectura) y `tools/maqueta_generar.py`." % cache["env"], "",
      "Orden de instalación en una base nueva (Aplicaciones → Importar módulo, uno a uno):", "",
      "1. `gn_base`", "2. Los módulos ya migrados a mano: `gn_inventory_planner_base`, `gn_inventory_planner`, "
      "`gn_valijas_base`, `gn_valijas`, `gn_entregas_parciales_base`, `gn_entregas_parciales`, "
      "`gn_purchase_account_rules`, `gn_vendor_transition_uom`, `gn_launch_planner`.", "3. Los de la maqueta, en este orden:", ""]
md += ["   %d. `%s`: %s" % (n + 1, mod, summary[mod]["m"]["nombre"]) for n, mod in enumerate(order)]
md += ["", "Después: pasar los datos de cada modelo (exportar de la base vieja e importar con los mismos nombres de "
       "campo), encender las acciones planificadas y revisar `maqueta_avisos.txt`.", ""]
open(os.path.join(OUT, "MAQUETA.md"), "w", encoding="utf-8", newline="\n").write("\n".join(md))
open(os.path.join(OUT, "maqueta_avisos.txt"), "w", encoding="utf-8", newline="\n").write("\n".join(avisos) + "\n")
print("módulos:", len(summary), "| avisos:", len(avisos), "| ciclos:", len(cycles))
for mod in order:
    print(" ", mod, summary[mod]["deps"])

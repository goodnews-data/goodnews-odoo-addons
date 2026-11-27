"""Install (or uninstall) the TEST VARIANT of the mockup in the GoodNews TEST database, one zip at a
time in order, like Apps > Import module. Refuses to run against production.

Usage (from the GN Tools repo, it reads the Odoo credentials of its .env):
  python <addons>/tools/maqueta_probar.py <variant_dir> install [<first_module>]
  python <addons>/tools/maqueta_probar.py <variant_dir> uninstall
Writes <variant_dir>/resultado.txt.
"""
import base64
import os
import sys
import time

sys.path.insert(0, os.getcwd())
from platform_app.modules.proveedores.config import get_settings  # noqa: E402
from platform_app.modules.proveedores.odoo_client import OdooClient  # noqa: E402

var_dir, mode = sys.argv[1], sys.argv[2]
start = sys.argv[3] if len(sys.argv) > 3 else None
c = get_settings().odoo_conn()
assert "test" in c.odoo_db, "only the TEST database: " + c.odoo_db
cl = OdooClient(c.odoo_url, c.odoo_db, c.odoo_username, c.odoo_password, timeout=900)


def X(model, method, *args, **kw):
    return cl.execute_kw(model, method, list(args), kw)


order = [m.strip() for m in open(os.path.join(var_dir, "orden.txt")) if m.strip()]
log = open(os.path.join(var_dir, "resultado.txt"), "a", encoding="utf-8")


def say(msg):
    print(msg, flush=True)
    log.write(msg + "\n")
    log.flush()


say("== %s %s en %s" % (time.strftime("%d/%m %H:%M"), mode, c.odoo_db))
if mode == "install":
    if start:
        order = order[order.index(start):]
    for m in order:
        state = X("ir.module.module", "search_read", [("name", "=", m)], fields=["state"])
        if state and state[0]["state"] == "installed" and m != start:   # the first one is re-imported (update)
            say("ya instalado  " + m)
            continue
        data = base64.b64encode(open(os.path.join(var_dir, "zips", m + ".zip"), "rb").read()).decode()
        t0 = time.time()
        try:
            wid = X("base.import.module", "create", {"module_file": data, "state": "init"})
            X("base.import.module", "import_module", [wid])
            ok = X("ir.module.module", "search_read", [("name", "=", m)], fields=["state"])
            if not ok or ok[0]["state"] != "installed":
                say("NO INSTALADO %s: estado %s" % (m, ok and ok[0]["state"]))
                break
            say("instalado     %s (%.0f s)" % (m, time.time() - t0))
        except Exception as e:  # noqa: BLE001
            say("ERROR         %s\n%s" % (m, str(e)[-3000:]))
            break
else:
    for m in reversed(order):
        rows = X("ir.module.module", "search_read", [("name", "=", m)], fields=["state"])
        if not rows or rows[0]["state"] != "installed":
            continue
        try:
            X("ir.module.module", "button_immediate_uninstall", [rows[0]["id"]])
            say("desinstalado  " + m)
        except Exception as e:  # noqa: BLE001
            say("ERROR al desinstalar %s\n%s" % (m, str(e)[-2000:]))

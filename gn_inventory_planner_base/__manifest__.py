{
    "name": "GoodNews · Planificador de inventario (modelos)",
    "summary": "Models and fields of the inventory planner, with the Studio technical names. "
               "Only for a new or migrated database",
    "version": "17.0.1.0.0",
    "category": "Inventory/Inventory",
    "author": "Isabella Maffi",
    "website": "https://github.com/goodnews-data/goodnews-odoo-addons/tree/main/gn_inventory_planner_base",
    "license": "LGPL-3",
    "depends": ["stock", "mail", "gn_base"],
    "data": [
        "data/models.xml",
        "views/product_views.xml",
    ],
    "images": ["static/description/icon.png"],
    "application": False,
    "installable": True,
}

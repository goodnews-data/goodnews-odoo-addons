{
    "name": "GoodNews · Planificador de inventario",
    "summary": "Cyclic stock counts: planners request counts per store and inventory group, "
               "and a history follows their progress",
    "version": "17.0.1.0.0",
    "category": "Inventory/Inventory",
    "author": "Isabella Maffi",
    "website": "https://github.com/goodnews-data/goodnews-odoo-addons/tree/main/gn_inventory_planner",
    "license": "LGPL-3",
    "depends": ["stock", "mail", "point_of_sale", "spreadsheet_dashboard"],
    "data": [
        "security/security.xml",
        "data/actions.xml",
        "views/views.xml",
    ],
    "images": ["static/description/icon.png"],
    "application": True,
    "installable": True,
}

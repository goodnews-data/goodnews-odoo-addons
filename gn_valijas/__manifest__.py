{
    "name": "GoodNews · Valijas",
    "summary": "Schedule the fixed shipments (valijas) of the Spanish central warehouses and "
               "validate them automatically at night",
    "version": "17.0.1.0.0",
    "category": "Inventory/Inventory",
    "author": "Isabella Maffi",
    "website": "https://github.com/goodnews-data/goodnews-odoo-addons/tree/main/gn_valijas",
    "license": "LGPL-3",
    "depends": ["stock", "mail"],
    "data": [
        "data/actions.xml",
        "views/stock_picking_views.xml",
    ],
    "images": ["static/description/icon.png"],
    "application": True,
    "installable": True,
}

{
    "name": "GoodNews · Lanzamientos programados",
    "summary": "Schedule product and POS launches (prices, POS availability, categories, combos, "
               "pricelists, names, archiving) by date and time, with validation and undo",
    "version": "17.0.1.0.0",
    "category": "Sales/Point of Sale",
    "author": "Isabella Maffi",
    "website": "https://github.com/bellamaffi/goodnews-odoo-addons/tree/main/gn_launch_planner",
    "license": "LGPL-3",
    "depends": ["point_of_sale", "product", "mail"],
    "data": [
        "data/models.xml",
        "security/security.xml",
        "data/defaults.xml",
        "data/actions.xml",
        "views/views.xml",
    ],
    "images": ["static/description/icon.png"],
    "application": True,
    "installable": True,
}

{
    "name": "GoodNews · Base",
    "summary": "Shared pieces used by several GoodNews developments: Supply and Data groups, "
               "and the store locations assigned to each user",
    "version": "17.0.1.0.0",
    "category": "Hidden",
    "author": "Isabella Maffi",
    "website": "https://github.com/goodnews-data/goodnews-odoo-addons/tree/main/gn_base",
    "license": "LGPL-3",
    "depends": ["stock", "spreadsheet_dashboard"],
    "data": [
        "security/groups.xml",
        "data/fields.xml",
        "views/res_users_views.xml",
    ],
    "images": ["static/description/icon.png"],
    "application": False,
    "installable": True,
}

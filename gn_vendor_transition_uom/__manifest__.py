{
    "name": "GoodNews · Vendor transition UoM",
    "summary": "Vendor-specific purchase UoM on PO lines and one-click switch to a transition UoM from the receipt",
    "version": "17.0.1.0.0",
    "category": "Inventory/Purchase",
    "author": "Isabella Maffi",
    "website": "https://github.com/bellamaffi/goodnews-odoo-addons/tree/main/gn_vendor_transition_uom",
    "license": "LGPL-3",
    "depends": ["purchase_stock", "base_automation"],
    "data": [
        "data/ir_model_fields.xml",
        "views/product_supplierinfo_views.xml",
        "data/automation_vendor_uom.xml",
        "data/action_transition.xml",
    ],
    "images": ["static/description/icon.png"],
    "application": True,
    "installable": True,
}

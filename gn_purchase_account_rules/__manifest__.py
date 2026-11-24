{
    "name": "GN - Purchase Account Rules",
    "summary": "Expense account and purchase VAT per vendor and product",
    "description": """
Data-only module (importable on Odoo Online / Cloudodoo).

Each rule says: when vendor X invoices product Y in company Z, use this
expense account and/or these purchase taxes. Applied automatically on
purchase order lines (taxes) and draft vendor bill lines (account + taxes).
Values set manually by a user are never overwritten.
""",
    "version": "17.0.1.0.0",
    "author": "Isabella Maffi",
    "website": "https://goodnewsco.es",
    "license": "LGPL-3",
    "category": "Accounting",
    "depends": ["account", "purchase", "base_automation", "mail", "product"],
    "data": [
        "data/ir_model.xml",
        "security/ir.model.access.csv",
        "security/ir_rule.xml",
        "views/rule_views.xml",
        "views/partner_views.xml",
        "data/base_automation.xml",
    ],
    "installable": True,
    "application": False,
}

{
    'name': 'POS Due Limit',
    'version':"18.0.1.1",
    'license':"LGPL-3",
    'summary':"""POS""",
    'description':"""User-friendly PoS interface for shops and restaurants""",
    'depends': ['base','sale_management','point_of_sale'],
    'author':"Cybrosys",
    'category':"Point of Sale",
    'website':"www.cybrosys.com",
    'maintainer':"Cybrosys Technology Pvt Ltd <info@cybrosys.com>",
    'sequence':1,
    'data':["security/ir.model.access.csv",
            "views/partner_views.xml"],
    'assets': {'point_of_sale._assets_pos': ["pos_due_limit/static/src/pos_due_limit.js"]},

    'application':True,
    # 'auto_install':True,
    'installable':True
}
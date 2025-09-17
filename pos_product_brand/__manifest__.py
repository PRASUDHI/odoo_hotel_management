{
    'name': 'POS Product Brand',
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
            "views/product_views.xml"],
    'application':True,
    # 'auto_install':True,
    'installable':True
}
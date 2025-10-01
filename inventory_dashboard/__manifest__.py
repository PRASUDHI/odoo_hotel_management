{
    'name': "Inventory Dashboard",
    'version': '1.0',
    'category': 'Inventory Dashboard',
    'sequence': 2,
    'summary': "Inventory Dashboard",
    'depends': ['base','sale','board'],
    'data' :['views/dashboard_views.xml'],

    'assets': {
       'web.assets_backend': [
           'inventory_dashboard/static/src/js/dashboard.js',
           'inventory_dashboard/static/src/xml/dashboard.xml',
           'inventory_dashboard/static/src/css/inventory_dashboard.css',
       ],

    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}

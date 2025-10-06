{
    'name': "sale orderlines",
    'version': '1.0',
    'sequence': 2,
    'depends': ['base','sale_management'],
    'data' :[
        'data/ir_action_data.xml',
        'views/sale_order_views.xml',],


    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}

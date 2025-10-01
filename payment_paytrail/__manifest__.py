# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "Payment Provider: Paytrail",
    'version': '1.0',
    'category': 'Accounting/Payment Providers',
    'sequence': 2,
    'summary': "A payment provider covering India.",
    'description': " ",  # Non-empty string to avoid loading the README file.
    'depends': ['base','payment'],
    'data': [
            'views/paytrail_templates.xml',
            'views/payment_provider_views.xml',
            'data/payment_method_data.xml',
            'data/payment_provider_data.xml',
        ],

    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}

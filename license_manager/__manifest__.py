# -*- coding: utf-8 -*-
{
    'name': "Software License Manager",

    'summary': """ Manage software license keys with an online customer portal. """,

    'description': """
        Manage software license keys with an online customer portal.
    """,

    'author': "Bitlect Technology",
    'website': "bitlect.net",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales',
    'version': '14.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','stock'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/lm_license_views.xml',
        'data/sequence.xml',
    ],
    'images': ['static/description/banner.png'],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'license': 'OPL-1',
    'application': True,
    'installable': True,
    'price': 780,
    'currency': 'USD'
}

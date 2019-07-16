# -*- coding: utf-8 -*-

{
    'name' : 'odoope_ruc_validation update',
    'version' : '1.2.2',
    'author' : 'Facturaloperu',
    'category' : 'Generic Modules/Base',
    'summary': "Módulo que actualiza odoope_ruc_validation",
    'license': 'AGPL-3',
    'website': 'facturaloperu.com',
    'depends' : ['odoope_ruc_validation','pos_ruc_dni_validation'],
    'data': [
        'views/res_partner_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    "sequence": 1,
}
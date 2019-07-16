# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Pos - consulta API: RUC DNI',
    'version': '11.0',
    'author': 'Bitodoo, Facturaloperu',
    'category': 'Point of Sale',
    'summary': 'Pos - consulta de datos dni, ruc',
    'website': 'http://www.facturaloperu.com',
    'license': 'AGPL-3',
    'description': """
        Pos - consulta de datos RUC y DNI para registrar nuevos clientes
    """,
    'depends': ['point_of_sale'],
    'data': [
        'template/template.xml',
    ],
    'qweb': [
        'static/src/xml/*.xml',
    ],
    'installable': True,
    'auto_install': False,
}

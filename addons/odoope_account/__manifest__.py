# -*- coding: utf-8 -*-
{
    'name': "Base contable",
    'summary': """
        Base contable
    """,
    'description': """
    """,
    'author': "",
    'website': "",
    'category': 'account',
    'version': '0.2',
    'depends': [
        'account_invoicing',
        'l10n_pe_sunat_data',
        'odoope_currency'
    ],
    'data': [
        'views/account.xml',
    ],
}

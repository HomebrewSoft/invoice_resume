# -*- coding: utf-8 -*-
{
    'name': 'Invoice Resume',
    'version': '1.7.0',
    'author': 'HomebrewSoft',
    'website': 'https://github.com/HomebrewSoft/invoice_resume',
    'depends': [
        'account',
    ],
    'data': [
        # security
        'security/ir.model.access.csv',
        # data
        'data/account_account.xml',
        'data/account_invoice_subtype.xml',
        'data/account_journal.xml',
        # views
        'views/account_invoice.xml',
        'views/account_invoice_bank_wizard.xml',
    ],
}

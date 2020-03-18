# -*- coding: utf-8 -*-
from odoo import _, api, fields, models


class AccountInvoiceSubtype(models.Model):
    _name = 'account.invoice.subtype'

    name = fields.Char(
        required=True,
    )

    type = fields.Selection(
        [
            ('in', 'Income'),
            ('out', 'Outcome'),
            ('bank', 'Bank'),
        ],
        required=True,
    )

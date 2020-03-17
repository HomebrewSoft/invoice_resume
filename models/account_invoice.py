# -*- coding: utf-8 -*-
from odoo import _, api, fields, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

# -*- coding: utf-8 -*-
from odoo import _, api, fields, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    type = fields.Selection(
        selection_add=[
            ('bank', 'Bank'),
        ],
    )
    subtype_id = fields.Many2one(
        comodel_name='account.invoice.subtype',
        ondelete='restrict',
        required=True,
    )
    real_amount = fields.Float(
        compute='_get_real_amount',
        store=True,
    )

    @api.depends('subtype_id', 'residual')
    def _get_real_amount(self):
        for record in self:
            if record.type in ['out_invoice', 'out_refound']:
                record.real_amount = record.residual
            else:
                record.real_amount = -record.residual

    @api.multi
    def name_get(self):
        TYPES = {
            'out_invoice': _('Invoice'),
            'in_invoice': _('Vendor Bill'),
            'out_refund': _('Refund'),
            'in_refund': _('Vendor Refund'),
            'bank': _('Vendor Refund'),
        }
        result = []
        for inv in self:
            result.append((inv.id, "%s %s" % (inv.number or TYPES[inv.type], inv.name or '')))
        return result

    @api.model
    def create(self, values):
        if values.get('type') in ['out_invoice']:
            values['subtype_id'] = self.env.ref('invoice_resume.subtype_outcome').id
        elif values.get('type') in ['in_invoice']:
            values['subtype_id'] = self.env.ref('invoice_resume.subtype_income').id
        return super(AccountInvoice, self).create(values)

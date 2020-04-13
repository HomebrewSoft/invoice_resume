# -*- coding: utf-8 -*-
from odoo import _, api, fields, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    type = fields.Selection(
        selection_add=[
            ('bank', _('Bank')),
        ],
    )
    type_translated = fields.Selection(
        selection=[
            ('out_invoice', _('Incomes')),
            ('in_invoice', _('Outcomes')),
            ('out_refund', _('Outcomes Refund')),
            ('in_refund', _('Incomes Refund')),
            ('bank', _('Bank')),
        ],
        compute='_get_type_translated',
        store=True,
    )
    subtype_id = fields.Many2one(
        comodel_name='account.invoice.subtype',
        ondelete='restrict',
        required=True,
        default=lambda self: self.relations().get(self._context.get('type')),
    )
    real_amount = fields.Float(
        compute='_get_real_amount',
        store=True,
    )

    @api.depends('type')
    def _get_type_translated(self):
        for record in self:
            record.type_translated = record.type

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
            'bank': _('Bank'),
        }
        result = []
        for inv in self:
            result.append((inv.id, "%s %s" % (inv.number or TYPES[inv.type], inv.name or '')))
        return result

    @api.model
    def create(self, values):
        if not values.get('subtype_id'):
            values['subtype_id'] = self.relations().get(values.get('type', 'in_invoice'))
        return super(AccountInvoice, self).create(values)

    def relations(self):
        return {
            'out_invoice': self.env.ref('invoice_resume.subtype_outcome').id,
            'in_invoice': self.env.ref('invoice_resume.subtype_income').id,
            'out_refund': self.env.ref('invoice_resume.subtype_outcome_refound').id,
            'in_refund': self.env.ref('invoice_resume.subtype_income_refound').id,
            'bank': self.env.ref('invoice_resume.subtype_bank').id,
        }

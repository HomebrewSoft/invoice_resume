# -*- coding: utf-8 -*-
from odoo import _, api, fields, models

from datetime import datetime, timedelta, date
from calendar import monthrange

DATE_FORMAT = "%Y-%m-%d"


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days + 1)):
        yield start_date + timedelta(n)


def get_last_date(self):
    today = datetime.strptime(fields.Date.context_today(self), DATE_FORMAT)
    return today.replace(day=monthrange(today.year, today.month)[1])


class AccountInvoice(models.Model):
    _name = 'account.invoice.bank_wizard'

    start_date = fields.Date(
        default=lambda self: datetime.strptime(fields.Date.context_today(self), DATE_FORMAT).replace(day=1),
        required=True,
    )
    end_date = fields.Date(
        default=get_last_date,
        required=True,
    )
    initial_amount = fields.Float(
        required=True,
    )

    def _create_invoice_bank(self, date, amount):
        invoice_id = self.env['account.invoice'].create({
            'account_id': self.env.ref('invoice_resume.account_bank').id,
            'journal_id': self.env.ref('invoice_resume.journal_bank').id,
            'subtype_id': self.env.ref('invoice_resume.subtype_bank').id,
            'partner_id': self.env.user.company_id.partner_id.id,
            'reference_type': 'none',
            'type': 'bank',
            'date_due': date,
        })
        invoice_id.real_amount = amount
        return invoice_id

    def compute(self):
        Invoice = self.env['account.invoice']
        Invoice.search([
            ('type', '=', 'bank'),
        ]).unlink()

        start_date = datetime.strptime(self.start_date, DATE_FORMAT)
        self._create_invoice_bank(start_date, self.initial_amount)
        prev_date = start_date
        end_date = datetime.strptime(self.end_date, DATE_FORMAT)
        for date in daterange(start_date + timedelta(1), end_date):
            prev_amount = sum(Invoice.search([('date_due', '=', prev_date)]).mapped('real_amount'))
            self._create_invoice_bank(date, prev_amount)
            prev_date = date

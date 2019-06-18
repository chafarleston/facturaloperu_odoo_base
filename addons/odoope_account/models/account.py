# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    l10n_pe_exchange_rate = fields.Float(string='Tipo de cambio', compute='_compute_l10n_pe_exchange_rate', digits=(10, 3))
    l10n_pe_invoice_origin_id = fields.Many2one(comodel_name='account.invoice', string='Documento rectificado', readonly=True)

    @api.model
    def default_get(self, fields_list):
        res = super(AccountInvoice, self).default_get(fields_list)
        res.update({
            'date_invoice': fields.Date().context_today(self)
        })
        return res

    @api.multi
    @api.depends('date_invoice', 'currency_id')
    def _compute_l10n_pe_exchange_rate(self):
        today = fields.Date().context_today(self)
        self.mapped(lambda x: x.update({
            'l10n_pe_exchange_rate': x.currency_id.with_context(date=(x.l10n_pe_invoice_origin_id or x).date_invoice or today).rate_pe
        }))

    def _get_currency_rate_date(self):
        return self.l10n_pe_invoice_origin_id.date_invoice or self.date or self.date_invoice

    @api.model
    def _prepare_refund(self, invoice, date_invoice=None, date=None, description=None, journal_id=None):
        res = super(AccountInvoice, self)._prepare_refund(
            invoice, date_invoice=date_invoice, date=date, description=description, journal_id=journal_id
        )
        res['l10n_pe_invoice_origin_id'] = invoice.id
        res['date_invoice'] = fields.Date().context_today(self)
        return res


class AccountTax(models.Model):
    _inherit = 'account.tax'

    l10n_pe_tax_type_id = fields.Many2one(comodel_name='l10n_pe.datas', domain=[('table_code', '=', 'PE.CPE.CATALOG5')], string='Tipo segun sunat')


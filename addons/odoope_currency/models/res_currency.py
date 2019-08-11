# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


import re
import requests

from bs4 import BeautifulSoup
from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError

SUNAT = 'sunat'
PURCHASE = 'purchase'
SALE = 'sale'

SOURCE_RATE = [
    (SUNAT, 'Sunat')
]

TYPES = [
    (PURCHASE, 'Compra'),
    (SALE, 'Venta')
]


class Currency(models.Model):
    _inherit = "res.currency"
    _description = "Currency"
    
    rate_pe = fields.Float(compute='_compute_current_rate_pe', string='Cambio del dia', digits=(12, 4),
                        help='Tipo de cambio del dia en formato peruano.')
    type = fields.Selection(TYPES,string='Tipo',default='sale')
    l10n_pe_source_rate = fields.Selection(selection=SOURCE_RATE, string='Origen del TC')

    _sql_constraints = [
        ('unique_name', 'unique (name,type)', 'Solo puede existir una moneda con el mismo tipo de cambio!'),
        ('rounding_gt_zero', 'CHECK (rounding>0)', 'The rounding factor must be greater than 0!')
    ]
    
    @api.multi
    def _compute_current_rate_pe(self):
        date = self._context.get('date') or fields.Date.today()
        company_id = self._context.get('company_id') or self.env['res.users']._get_company().id
        # the subquery selects the last rate before 'date' for the given currency/company
        query = """SELECT c.id, (SELECT r.rate_pe FROM res_currency_rate r
                                  WHERE r.currency_id = c.id AND r.name <= %s
                                    AND (r.company_id IS NULL OR r.company_id = %s)
                               ORDER BY r.company_id, r.name DESC
                                  LIMIT 1) AS rate_pe
                   FROM res_currency c
                   WHERE c.id IN %s"""
        self._cr.execute(query, (date, company_id, tuple(self.ids)))
        currency_rates = dict(self._cr.fetchall())
        for currency in self:
            currency.rate_pe = currency_rates.get(currency.id) or 1.0
    
    @api.multi
    def name_get(self):
        return [(currency.id, tools.ustr(currency.name + ' - ' + dict(TYPES)[currency.type])) for currency in self]

    @api.model
    def l10n_pe_get_currency(self):
        currencies = self.search([('l10n_pe_source_rate', '!=', False)])
        currencies.mapped(lambda w: w._l10n_pe_from_sunat() if w.l10n_pe_source_rate == SUNAT else None)

    @api.multi
    def l10n_pe_is_company_currency(self):
        return self == self.env.user.company_id.currency_id

    @api.multi
    def _l10n_pe_from_sunat(self):
        r = requests.get("http://e-consulta.sunat.gob.pe/cl-at-ittipcam/tcS01Alias")
        soup = BeautifulSoup(r.text, "lxml")
        index = -1 if self.type == SALE else -2
        res = soup.find_all("td", {"align": "center", "class": "tne10"})[index]
        value = re.sub("[\r\n\t]", "", res.text)
        if self and value and value.strip() and self.name in ['USD']:
            obj_currency_rate = self.rate_ids.filtered(
                lambda x: fields.Datetime.from_string(x.name).strftime('%Y-%m-%d') == fields.Date().today()
            )
            if not obj_currency_rate:
                self.env['res.currency.rate'].create({
                    'name': fields.Datetime().now(),
                    'rate_pe': float(value.strip()),
                    'currency_id': self.id,
                    'rate': 1 / float(value.strip())
                })

    @api.model
    def _get_conversion_rate(self, from_currency, to_currency):
        # from_currency = from_currency.with_env(self.env)
        # to_currency = to_currency.with_env(self.env)
        return to_currency.rate / from_currency.rate

    @api.multi
    def l10n_pe_get_rate_by_date(self, date):
        if self != self.env.user.company_id.currency_id and date:
            rate_obj = self.env['res.currency.rate'].search([('currency_id', '=', self.id), ('name', '<=', date)], order='name DESC', limit=1)
            if rate_obj:
                return rate_obj.rate_pe
            elif self:
                raise ValidationError('Configure un tipo de cambio para moneda {} con fecha {}'.format(self.name, date))
        else:
            return 1


class CurrencyRate(models.Model):
    _inherit = "res.currency.rate"
    _description = "Currency Rate"

    rate_pe = fields.Float(string='Cambio',digits=(12, 4), help='Tipo de cambio en formato peruano. Ejm: 3.25 si $1 = S/. 3.25')
    type = fields.Selection(related="currency_id.type", store=True)
    
    @api.onchange('rate_pe')
    def onchange_rate_pe(self):
        if self.rate_pe > 0:
            self.rate = 1 / self.rate_pe

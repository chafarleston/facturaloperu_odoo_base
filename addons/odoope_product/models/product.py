# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    l10n_pe_osce_id = fields.Many2one(comodel_name='l10n_pe.datas', domain=[('table_code', 'in', ['PE.CPE.CATALOG25'])],
                                                    string=u"Código osce")


class ProductUom(models.Model):
    _inherit = "product.uom"

    l10n_pe_sunat_code_id = fields.Many2one(comodel_name='l10n_pe.datas', domain=[('table_code', 'in', ['PE.TABLA06'])], string="SUNAT Unit Code",
                                            required=True)


class ProductCategory(models.Model):
    _inherit = 'product.category'

    l10n_pe_valuation_method_id = fields.Many2one(comodel_name='l10n_pe.datas', domain=[('table_code', 'in', ['PE.TABLA14'])],
                                                  string=u"Método de valoración", required=True)

    l10n_pe_existence_type_id = fields.Many2one(comodel_name='l10n_pe.datas', domain=[('table_code', 'in', ['PE.TABLA05'])],
                                                  string=u"Tipo de existencia", required=True)





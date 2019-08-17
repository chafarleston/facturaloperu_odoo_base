# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import Warning

import requests


def get_data_doc_number(tipo_doc, numero_doc, format='json'):
    user, password = 'demorest', 'demo1234'
    url = 'http://py-devs.com/api'
    url = '%s/%s/%s' % (url, tipo_doc, str(numero_doc))
    res = {'error': True, 'message': None, 'data': {}}
    try:
        response = requests.get(url, auth=(user, password))
    except requests.exceptions.ConnectionError as e:
        res['message'] = 'Error en la conexion'
        return res

    if response.status_code == 200:
        res['error'] = False
        res['data'] = response.json()
    else:
        try:
            res['message'] = response.json()['detail']
        except Exception as e:
            res['error'] = True
    return res


class ResPartner(models.Model):
    _inherit = 'res.partner'

    registration_name = fields.Char('Name', size=128, index=True, )
    state = fields.Selection([('habido','Habido'),('nhabido','No Habido')],'State')
    ubigeo = fields.Char(string='Ubigeo', size=6)
    zip = fields.Char(string='Ubigeo', size=6, required=True)

    # default document
    @api.model
    def _default_catalog(self):
        return self.env["einvoice.catalog.06"].search([('code', '=', '6')], limit=1)

    catalog_06_id = fields.Many2one('einvoice.catalog.06','Tipo de Documento', index=True, default=_default_catalog, copy=False)

    @api.onchange('catalog_06_id','vat')
    def vat_change(self):
        self.update_document()
        if not self.name or self.registration_name:
            res = self.get_apiperu_data(self.catalog_06_id.code, self.vat)
            self.update(res)

    @api.one
    def update_document(self):

        if not self.vat:
            return False
        if self.catalog_06_id and self.catalog_06_id.code == '1':
           #Valida DNI
            if self.vat and len(self.vat) != 8:
                raise Warning('El Dni debe tener 8 caracteres')
            else:
                d = get_data_doc_number(
                    'dni', self.vat, format='json')
                if not d['error']:
                    d = d['data']
                    self.name = '%s %s %s' % (d['nombres'],
                                               d['ape_paterno'],
                                               d['ape_materno'])

        elif self.catalog_06_id and self.catalog_06_id.code == '6':
            # Valida RUC
            if self.vat and len(self.vat) != 11:
                raise Warning('El Ruc debe tener 11 caracteres')
            else:
                d = get_data_doc_number(
                    'ruc', self.vat, format='json')
                if d['error']:
                    return True
                d = d['data']
                #~ Busca el distrito
                ditrict_obj = self.env['res.country.state']
                prov_ids = ditrict_obj.search([('name', '=', d['provincia']),
                                               ('province_id', '=', False),
                                               ('state_id', '!=', False)])
                dist_id = ditrict_obj.search([('name', '=', d['distrito']),
                                              ('province_id', '!=', False),
                                              ('state_id', '!=', False),
                                              ('province_id', 'in', [x.id for x in prov_ids])], limit=1)
                if dist_id:
                    self.district_id = dist_id.id
                    self.province_id = dist_id.province_id.id
                    self.state_id = dist_id.state_id.id
                    self.country_id = dist_id.country_id.id

                # Si es HABIDO, caso contrario es NO HABIDO
                tstate = d['condicion_contribuyente']
                if tstate == 'HABIDO':
                    tstate = 'habido'
                else:
                    tstate = 'nhabido'
                self.state = tstate

                self.name = d['nombre_comercial'] != '-' and d['nombre_comercial'] or d['nombre']
                self.registration_name = d['nombre']
                self.street = d['domicilio_fiscal']
                self.vat_subjected = True
                self.is_company = True
                self.ubigeo = d['ubigeo']
                self.zip = d['ubigeo']
        else:
            True

    @api.model
    def get_apiperu_data(self, document_type, document_number):
        url = self.env.user.company_id.apiperu_url
        token = self.env.user.company_id.apiperu_token
        document_type = 'dni' if document_type == '1' else 'ruc' if document_type == '6' else ''
        if not document_type:
            return {}
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {0}'.format(token),
        }
        register_url = u'{}/{}/{}'.format(url, document_type, document_number)
        response = requests.get(register_url, headers=headers)
        if response.status_code != 200:
            return {}
        response = response.json()
        if not response.get('success'):
            return {}
        data = response.get('data', {})

        if document_type == 'dni':
            return {
                'name': data.get('nombre_completo'),
                'registration_name': data.get('nombre_completo')
            }
        else:
            ubigeo = data.get('ubigeo', [])
            ubigeo = len(ubigeo) > 2 and ubigeo[2]
            district = self.env['res.country.state'].search([('code', '=', ubigeo)], limit=1)
            return {
                'name': data.get('nombre_o_razon_social'),
                'registration_name': data.get('nombre_o_razon_social'),
                'street': data.get('direccion_completa'),
                'district_id': district and district.id or False,
                'province_id': district and district.province_id and district.province_id.id or False,
                'state_id': district and district.state_id and district.state_id.id or False,
                'country_id': district and district.state_id and district.state_id.country_id and district.state_id.country_id.id or False,
                'zip': ubigeo,
                'is_company': True,
                'company_type': 'company',
                'image': self._get_default_image('company', 1, False)
            }




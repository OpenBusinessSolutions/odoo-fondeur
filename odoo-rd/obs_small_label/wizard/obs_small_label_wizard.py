# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2013-Present Acespritech Solutions Pvt. Ltd. (<http://acespritech.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api, _
from openerp.exceptions import except_orm, Warning, RedirectWarning
import pdb


class product_small_label_qty(models.Model):
    _name='product.small.label.qty'

    product_id = fields.Many2one('product.product',string='Product')
    qty =  fields.Float(string='Quantity')
    prod_small_wiz_id = fields.Many2one('obs.small.label.wizard', string='Product Wizard')


class obs_small_label_wizard(models.Model):
    _name = 'obs.small.label.wizard'

    @api.multi
    def _get_currency(self):
        currency = self.env['res.currency'].search([('name','=','DOP')])
        if currency:
            return currency[0].id
        else:
            return False

    @api.model
    def default_get(self, fields_list):
        prod_list = []
        res = super(obs_small_label_wizard, self).default_get(fields_list)
        prod_ids = self.env['product.template'].browse(self._context['active_ids'])
        for prod in prod_ids:
            if prod.ean13 or prod.default_code:
                prod_list.append((0, 0, {'product_id' : prod.id, 'qty': prod.virtual_available if prod.virtual_available else 1}))
        if prod_list:
            res.update({'product_ids' : prod_list})
        else:
            raise Warning(_('Selected Product(s) has no EAN13 Number or Internal Reference.'))
        return res

    pricelist_id = fields.Many2one('product.pricelist',string='PriceList')
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  required=True,
                                  default= _get_currency
                                 )  # el numero 74 es el ID de la moneda DOP en la tabla res.currency
    cur_position = fields.Selection([('before', 'Before'), ('after', 'After')], default='after')
    product_ids = fields.One2many('product.small.label.qty', 'prod_small_wiz_id', string='Product List')
    display_price = fields.Boolean(string="Display Price")
    barcode_from = fields.Selection([('ean13', 'EAN13'),('ref','Reference No.')], string="Barcode From", default="ref")


    #Default values that need to be set
    defaults = {
        'currency_id': _get_currency,
    }

    @api.multi
    def small_barcode_report_call(self):
        qty = 0.0
        data = self.read()[0]
        datas = {
            'ids': self._ids,
            'model': 'obs.small.label.wizard',
            'form': data,
        }
        for line in self.product_ids:
            qty += line.qty
        if qty == 0:
            raise Warning(_('Quantity of Product should be greater Zero(0).'))
        return  self.env['report'].get_action(self, 'obs_small_label.obs_small_label_template',data=datas,)
        


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

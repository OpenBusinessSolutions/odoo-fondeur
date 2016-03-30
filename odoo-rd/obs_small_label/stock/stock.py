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
from openerp import models, fields, api,_

class stock_picking(models.Model):
    _inherit = 'stock.picking'

#same method to execute into odoo 8
    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        result = super(stock_picking, self).fields_view_get(view_id=view_id, view_type=view_type,
                                                                     toolbar=toolbar,submenu=False)
        if self._context.get('search_default_picking_type_id'):
            picking_id = self.env['stock.picking.type'].browse(self._context.get('search_default_picking_type_id'))
            if picking_id and picking_id.code != 'incoming':
                if view_type in ['tree','form']:
                    for elm in result.get('toolbar').get('print'):
                        if elm.get('string') == "Small Barcode Label":
                            result['toolbar']['print'].remove(elm)
        return result

class product_product(models.Model):
    _inherit = 'product.product'

    def _check_ean_key(self, cr, uid, ids, context=None):
        print "jhgfdjkghfjkdgh"
        return True

    _constraints = [(_check_ean_key, 'You provided an invalid "EAN13 Barcode" reference. You may use the "Internal Reference" field instead.', ['ean13'])]

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
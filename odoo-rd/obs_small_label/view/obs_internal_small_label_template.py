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

from openerp import models, api, _
from reportlab.graphics.barcode import createBarcodeDrawing
from reportlab.graphics.shapes import Drawing
from base64 import b64encode
from reportlab.graphics import renderPM
from reportlab.lib import units
from datetime import date
from openerp.exceptions import Warning


class obs_internal_small_label_template(models.AbstractModel):
    _name = 'report.obs_small_label.obs_internal_small_label_template'

    @api.multi
    def render_html(self, data=None):
        qty = 0 
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('obs_small_label.obs_internal_small_label_template')
        docargs = {
            'doc_ids': self._ids,
            'doc_model': report.model,
            'docs': self,
            'get_barcode_data' : self._get_barcode_data,
        }
        stock_obj = self.env['stock.picking']
        products = []
        for picking in stock_obj.browse(self._ids):
            if picking.picking_type_id and picking.picking_type_id.code == 'incoming':
                for line in picking.move_lines:
                    if line.product_id.default_code:
                        products.append(line.product_id.id)
        if not products:
            raise Warning(_('No Incoming Shipment found with EAN13 barcode number.'))
        return report_obj.render('obs_small_label.obs_internal_small_label_template', docargs)

    def get_barcode(self, value, width, barWidth = 0.05 * units.inch,
                    fontSize = 12, humanReadable = True):
        # El valor por default de fontSize=60
        barcode = createBarcodeDrawing('Code128', value = value, barWidth = barWidth, fontSize = fontSize, humanReadable = humanReadable)
        drawing_width = width
        barcode_scale = drawing_width / barcode.width
        drawing_height = barcode.height * barcode_scale

        drawing = Drawing(drawing_width, drawing_height)
        drawing.scale(barcode_scale, barcode_scale)
        drawing.add(barcode, name='barcode')
        barcode_encode = b64encode(renderPM.drawToString(drawing, fmt = 'PNG'))
        barcode_str = '<img style="width:320px;height:80px;"  src="data:image/png;base64,{0} : ">'.format(barcode_encode)
        return barcode_str

    def _get_barcode_data(self, picking_ids):
        
        print "_get_barcode_data"
        product_list = []
        prod_obj = self.env['product.product']
        stock_obj = self.env['stock.picking']
        for picking in stock_obj.browse(picking_ids):
            if picking.picking_type_id and picking.picking_type_id.code == 'incoming':
                for line in picking.move_lines:
                    if line.product_id.default_code:
                        barcode_str = self.get_barcode(value=line.product_id.default_code, width=1500)
                        for qty in range(int(line.product_uom_qty)):
                            prod_dict ={}
                            prod_dict = {
                                    'name':line.product_id.name,
                                    'default_code':line.product_id.default_code,
                                    'ean13': barcode_str
                                    }
                            product_list.append(prod_dict)
        return product_list
        
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

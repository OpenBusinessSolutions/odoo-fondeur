# -*- encoding: utf-8 -*-
##############################################################################
#
#    Stock Transfer Split Multi module for Odoo
#    Copyright (C) 2014 Akretion (http://www.akretion.com)
#    @author Alexis de Lattre <alexis.delattre@akretion.com>
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
import openerp.addons.decimal_precision as dp
from openerp.exceptions import Warning


class StockTransferSplitMulti(models.TransientModel):
    _name = "stock.transfer.split.multi"
    _description = "Split by multi units on stock transfer wizard"

    split_qty = fields.Float(
        string="Quantity to Extract",
        digits=dp.get_precision('Product Unit of Measure'), required=True)
    psm = fields.Text(string="Product Serialization Manager", required=False, )

    @api.multi
    def split_multi_quantities(self):
        self.ensure_one()
        assert self.env.context.get('active_model') == \
            'stock.transfer_details_items', 'Wrong underlying model'
        trf_line = self.env['stock.transfer_details_items'].browse(
            self.env.context['active_id'])
        split_qty = self[0].split_qty
        if split_qty > 0:
            
            if split_qty >= trf_line.quantity:
                raise Warning(
                    _("The Quantity to extract (%s) cannot be superior or "
                        "equal to the quantity of the line (%s)")
                    % (split_qty, trf_line.quantity))

            '''
            for each in range(split_qty):
                new_line = trf_line.copy()
                new_line.write({'quantity': 1, 'packop_id': False})
                trf_line.quantity -= 1
            '''

            psm = self.psm
            if psm:
                lines = psm.split('\n')
                lines = list(set(lines))
                if '' in lines:
                    lines.remove('')

                for line in lines:
                    spl_ids = self.env['stock.production.lot'].search([('product_id', '=', trf_line.product_id.id), ('name', '=', line)])
                    if trf_line.product_id.track_incoming or trf_line.product_id.track_outgoing\
                            or trf_line.product_id.track_all:
                        if len(spl_ids) < 1:
                            spl = self.env['stock.production.lot']
                            spl_id = spl.create({'name': line, 'product_id': trf_line.product_id.id})
                            new_line = trf_line.copy()
                            new_line.write({'quantity': 1, 'packop_id': False, 'lot_id': spl_id.id})
                            trf_line.quantity -= 1
                    else:
                        new_line = trf_line.copy()
                        new_line.write({'quantity': 1, 'packop_id': False, 'lot_id': spl_ids.id})
                        trf_line.quantity -= 1
            else:
                lines = []
                split_qty = int(split_qty)
                for each in range(split_qty):
                    #if trf_line.product_id.track_incoming or trf_line.product_id.track_outgoing\
                        #or trf_line.product_id.track_all:
                    new_line = trf_line.copy()
                    new_line.write({'quantity': 1, 'packop_id': False})
                    trf_line.quantity -= 1

        action = trf_line.transfer_id.wizard_view()
        return action

    @api.multi
    def cancel(self):
        """We have to re-call the wizard when the user clicks on Cancel"""
        self.ensure_one()
        assert self.env.context.get('active_model') == \
            'stock.transfer_details_items', 'Wrong underlying model'
        trf_line = self.env['stock.transfer_details_items'].browse(
            self.env.context['active_id'])
        action = trf_line.transfer_id.wizard_view()
        return action

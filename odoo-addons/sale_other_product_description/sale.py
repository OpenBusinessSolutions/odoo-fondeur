# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models


# class sale_order_line(models.Model):
#     _inherit = "sale.order.line"

#     def product_id_change(
#             self, cr, uid, ids, pricelist, product, qty=0,
#             uom=False, qty_uos=0, uos=False, name='', partner_id=False,
#             lang=False, update_tax=True, date_order=False, packaging=False,
#             fiscal_position=False, flag=False, context=None):

#         res = super(sale_order_line, self).product_id_change(
#             cr, uid, ids, pricelist, product, qty=qty, uom=uom,
#             qty_uos=qty_uos, uos=uos, name=name, partner_id=partner_id,
#             lang=lang, update_tax=update_tax, date_order=date_order,
#             packaging=packaging, fiscal_position=fiscal_position, flag=flag,
#             context=context)
#         if not 'value' in res:
#             res['value'] = {}

#         if product:
#             partner_obj = self.pool.get('res.partner')
#             partner = partner_obj.browse(cr, uid, partner_id)
#             lang = partner.lang
#             context_partner = {'lang': lang, 'partner_id': partner_id}
#             product_obj = self.pool.get('product.product')
#             product = product_obj.browse(
#                 cr, uid, product, context=context_partner)
#             if product.other_sale_description:
#                 res['value']['name'] = product.other_sale_description
#         return res

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

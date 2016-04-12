# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp.osv import fields, osv


class product_product(osv.osv):
    _inherit = "product.template"
    _columns = {
        'location_id': fields.dummy(
            string='Location', relation='stock.location', type='many2one'),
        'warehouse_id': fields.dummy(
            string='Warehouse', relation='stock.warehouse', type='many2one'),
    }

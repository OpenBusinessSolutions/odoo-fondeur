# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import fields, models, api


class product(models.Model):

    """"""

    _inherit = 'product.product'

    default_code = fields.Char(
        'Internal reference', required=True)

    def name_search(self, cr, uid, name, args=None,
                    operator='ilike', context=None, limit=100):
        args = args or []
        res = []
        if name:
            recs = self.search(
                cr, uid, [('default_code', operator, name)] + args,
                limit=limit, context=context)
            res = self.name_get(cr, uid, recs)
        res += super(product, self).name_search(
            cr, uid,
            name=name, args=args, operator=operator, limit=limit)
        return res

    @api.model
    def create(self, vals):
        if (
                not vals.get('default_code', False) and
                not self._context.get('default_code', False)):
            vals['default_code'] = self.env[
                'ir.sequence'].get('product.default.code') or '/'
        return super(product, self).create(vals)

    _sql_constraints = {
        ('default_code_uniq', 'unique(default_code)',
            'Internal reference must be unique!')
    }


class product_template(models.Model):

    """"""

    _inherit = 'product.template'

    default_code = fields.Char(
        related='product_variant_ids.default_code',
        string='Internal Code')

    @api.model
    def create(self, vals):
        if vals.get('default_code'):
            self = self.with_context(
                default_code=vals.get('default_code'))
        return super(product_template, self).create(vals)

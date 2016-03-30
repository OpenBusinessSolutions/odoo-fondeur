# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields, api


class account_invoice_refund(models.TransientModel):

    _inherit = 'account.invoice.refund'

    @api.model
    def _get_invoice_id(self):
        return self._context.get('active_id', False)

    # @api.one
    @api.multi
    @api.onchange('invoice_id')
    def _onchange_invoice(self):
        journal_type = False
        if self.invoice_id.type == 'out_refund' or 'out_invoice':
            journal_type = 'sale_refund'
        elif self.invoice_id.type == 'in_refund' or 'in_invoice':
            journal_type = 'purchase_refund'
        # return {'domain': {'journal_id': price}}
        journals = self.env['account.journal'].search(
            [('type', '=', journal_type),
             ('company_id', '=', self.invoice_id.company_id.id)])
        periods = self.env['account.period'].search(
            [('company_id', '=', self.invoice_id.company_id.id)])
        # self.journal_type = journal_type
        if journals:
            self.journal_id = journals[0].id
        return {'domain': {
            'journal_id': [('id', 'in', journals.ids)],
            'period': [('id', 'in', periods.ids)]
        }}

    invoice_id = fields.Many2one(
        'account.invoice',
        'Invoice',
        default=_get_invoice_id,
        store=True)

    def compute_refund(self, cr, uid, ids, data_refund, context=None):
        res = super(account_invoice_refund, self).compute_refund(
            cr, uid, ids, data_refund, context=context)
        domain = res.get('domain', [])
        invoice_ids = context.get('active_ids', [])
        if not invoice_ids:
            return res
        sale_order_ids = self.pool['sale.order'].search(
            cr, uid, [('invoice_ids', 'in', invoice_ids)])
        invoice_obj = self.pool['account.invoice']
        refund_invoice_ids = invoice_obj.search(cr, uid, domain)
        origin = ', '.join([x.number for x in invoice_obj.browse(
            cr, uid, invoice_ids) if x.number])
        invoice_obj.write(cr, uid, refund_invoice_ids, {
            'origin': origin,
        })
        if not self.browse(cr, uid, ids, context=context)[0].period:
            invoice_obj.write(cr, uid, refund_invoice_ids, {
                'period_id': invoice_obj.browse(
                    cr, uid, invoice_ids)[0].period_id.id
            })
        for invoice_id in refund_invoice_ids:
            self.pool['sale.order'].write(
                cr, uid, sale_order_ids, {'invoice_ids': [(4, invoice_id)]})
        return res

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

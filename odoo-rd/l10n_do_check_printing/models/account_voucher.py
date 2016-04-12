#-*- coding: utf-8 -*-

from openerp.osv import orm, fields
import pdb

class AccountVoucher(orm.Model):

    _inherit = 'account.voucher'
    _description = 'Secuencia de Registros'

    _columns = {
        'name': fields.text('Memoria', required=True),
        'voucher_number': fields.char('Number'),
    }

    def create(self, cr, uid, vals, context=None):

        if not vals:
            vals ={}
        journal = vals.get('journal_id',False)

        if journal:
            ir_sequence = self.pool.get('account.journal').browse(cr, uid, journal).internal_sequence_id.code
            seq = self.pool.get('ir.sequence').get(cr, uid, ir_sequence)
            vals.update({
                     'voucher_number': str(seq)
                 })
            return super(AccountVoucher, self).create(cr, uid, vals, context)

AccountVoucher()

# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp.osv import osv


class ir_mail_server(osv.osv):
    _inherit = "ir.mail_server"

    def _get_default_bounce_address(self, cr, uid, context=None):
        mail_server_ids = self.search(
            cr, 1, [], order='sequence asc', limit=1, context=context)
        if mail_server_ids:
            return self.browse(cr, 1, mail_server_ids[0]).smtp_user
        else:
            return super(ir_mail_server, self)._get_default_bounce_address(
                cr, uid, context)
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

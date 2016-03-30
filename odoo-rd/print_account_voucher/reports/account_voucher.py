# -*- encoding: utf-8 -*-
#########################################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2014-TODAY Probuse Consulting Service Pvt. Ltd. (<http://probuse.com>).
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
#########################################################################################

import time

from openerp.osv import osv
from openerp.report import report_sxw
from openerp import pooler

class account_voucher_report(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(account_voucher_report, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
              'time': time,
              'getLines': self._voucher_line_get,
                                  })
        self.context = context
    
    def _voucher_line_get(self, voucher):
        domain = []
        voucherline_obj = pooler.get_pool(self.cr.dbname).get('account.voucher.line')
        domain.append(('voucher_id','=',voucher.id))
        if voucher.type in ('receipt', 'sale'):
            domain.append(('type', '=', 'cr'))
        else:#for supplier payment and supplier receipts.
            domain.append(('type', '=', 'dr'))
        voucherlines = voucherline_obj.search(self.cr, self.uid, domain, context=self.context)
        return voucherline_obj.browse(self.cr, self.uid, voucherlines, context=self.context)
    
class report_test(osv.AbstractModel):
    _name = "report.print_account_voucher.print_voucher_report_all"
    _inherit = "report.abstract_report"
    _template = "print_account_voucher.print_voucher_report_all"
    _wrapped_report_class = account_voucher_report

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

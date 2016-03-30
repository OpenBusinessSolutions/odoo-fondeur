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

{
    'name': 'OBS Small Label',
    'version': '1.0.1',
    'author' : 'Acespritech Solutions Pvt.Ltd.',
    'website': 'http://acespritech.co.in',
    'summary': '',
    'depends': ['base', 'product', 'stock', 'mrp'],
    'description': """
    """,
    'data':[
            'view/obs_small_label_template.xml',
            'view/obs_internal_small_label_template.xml',
            'view/obs_mrp_small_label_template.xml',
            'report_product_barcode_label.xml',
            'wizard/obs_small_label_wizard_view.xml',
            ],
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

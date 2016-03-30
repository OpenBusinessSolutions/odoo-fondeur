# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015  ADHOC SA  (http://www.adhoc.com.ar)
#    All Rights Reserved.
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
    'author': 'ADHOC SA',
    'category': 'Accounting & Finance',
    'demo_xml': [],
    'depends': ['account_voucher'],
    'description': '''
Account Payment Direction
=========================
Extends Account Journal and adds a field direction (in or out) for bank and cash Journals. 
This journals will be shown or not on customer or supplier vouchers depending on the 'in', 'out' config. 
Specially used for journals that are only used on payments (like retentions)
''',
    'installable': True,
    'name': 'Account Payment Direction',
    'test': [],
    'data': [
        'account_journal_view.xml',
        'voucher_payment_receipt_view.xml',
    ],
    'version': '8.0.0.0.0',
    'website': 'www.adhoc.com.ar'}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

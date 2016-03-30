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

{
    'name' : 'Print Receipt/Payment Voucher',
    'version' : '1.0',
    'author': 'Probuse Consulting Service Pvt. Ltd.',
    'category' : 'Accounting & Finance',
    'website': 'https://www.probuse.com',
    'price': 12.0,
    'currency': 'EUR',
    'description': '''
This module allow to print report on account vouchers:
- Print Receipt/Payment
- Print Voucher / Report Voucher

You can find voucher report (Print Receipt/Payment) under Sales Receipts, Customer Payment, Purchase Receipts, Supplier Payments. 

Version Odoo 8.0 - Account Voucher Print Report

    ''',
    'depends' : ['account_voucher'],
    'data' : [
              'reports/print_account_voucher_report.xml',
              'reports/print_account_voucher.xml'
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

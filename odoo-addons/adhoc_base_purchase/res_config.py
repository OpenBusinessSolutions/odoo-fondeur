# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields


class adhoc_base_configuration(models.TransientModel):
    _inherit = 'adhoc.base.config.settings'

    # Fixes
    module_purchase_multic_fix = fields.Boolean(
        'FiX purchase in multi-company father/son environment',
        help="""Installs the purchase_multic_fix module.""")

    # Purchase modules
    module_purchase_double_validation_imp = fields.Boolean(
        'Adds a button for confirmed orders so that you can print the purchase order.',
        help="""Installs the purchase_double_validation_imp module.""")
    module_purchase_usability_extension = fields.Boolean(
        'Display Invoices and Incoming Shipments on Purchase Order form view (in dedicated tabs).',
        help="""Installs the purchase_usability_extension module.""")
    module_purchase_discount = fields.Boolean(
        'Mange disccounts on purchases',
        help="""Installs the purchase_discount module.""")
    module_account_analytic_purchase_contract = fields.Boolean(
        'Manage contracts on Purchase.',
        help="""Installs the account_analytic_purchase_contract module.""")
    module_purchase_uom_prices_uoms = fields.Boolean(
        'Restrict purchase uom to the product uom, purchase product uom and uoms defined in UOM Prices.',
        help="""Installs the purchase_uom_prices_uoms.""")
    module_purchase_line_defaults = fields.Boolean(
        'Set defaults values on purchase orders in order to facilitate file import.',
        help="""Installs the purchase_line_defaults.""")
    module_partner_products_shortcut = fields.Boolean(
        'Adds a shortcut on supplier partner form to the products supplied by this partner.',
        help="""Installs the partner_products_shortcut module.""")
    module_partner_products_shortcut = fields.Boolean(
        'Adds a shortcut on supplier partner form to the products supplied by this partner.',
        help="""Installs the partner_products_shortcut module.""")
    module_purchase_prices_update = fields.Boolean(
        'Adds a button on purchase order view to update prices for the order lines.',
        help="""Installs the purchase_prices_update module.""")

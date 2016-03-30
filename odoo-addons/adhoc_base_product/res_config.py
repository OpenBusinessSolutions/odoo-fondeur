# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields


class adhoc_base_configuration(models.TransientModel):
    _inherit = 'adhoc.base.config.settings'

    # Fixes

    # Product modules
    module_product_share_father_son = fields.Boolean(
        'Share products between fother and son companies',
        help="""Installs the product_share_father_son module: It allowes to see products with company set as a father company.""")
    module_product_template_search_by_ean13 = fields.Boolean(
        'Product Search by ean13 on product template',
        help="""Installs the product_template_search_by_ean13 module: It allows to search products by ean13 in Product Tree view""")
    module_product_pack = fields.Boolean(
        'Mange product packs',
        help="""Installs the product_pack module: I allows to set product combos with prices based on products components or special prices for the combo""")
    module_product_price_currency = fields.Boolean(
        'Manage different currencies on product sale price',
        help="""Installs the product_price_currency module.""")
    module_product_dimensions = fields.Boolean(
        'Manage product  logistic dimmensions',
        help="""Installs the product_dimensions moduele: Add dimensions (length, width and height) products.""")
    module_product_supplier_pricelist = fields.Boolean(
        'Mange easier supplier pricelist',
        help="""Installs the product_supplier_pricelist module: Add sql constraint to restrict: 1. That you can only add one supplier to a product per company 2. That you can add olny one record of same quantity for a supplier pricelist""")
    module_product_unique = fields.Boolean(
        'Validate product unicity per company on ean13 and interal reference fields',
        help="""Installs the product_unique module: It forbides ean13 an internal reference duplications .""")
    module_product_historical_price = fields.Boolean(
        'Historical price for product in a product tab',
        help="""Installs the product_historical_price module.""")
    module_product_salesman_group = fields.Boolean(
        'Restrict salesman to see only authorized products by using salesman groups.',
        help="""Installs the product_salesman_group module.""")
    module_product_uom_prices = fields.Boolean(
        'Allow to define different prices for different UOMs',
        help="""Installs the product_uom_prices module.""")
    module_product_force_create_variants = fields.Boolean(
        'Allow to force create variants on product templates',
        help="""Installs the product_force_create_variants module.""")
    module_product_variant_imp = fields.Boolean(
        'Make Some Improovements in Variants and Attributes management',
        help="""Installs the product_variant_imp module.""")
    module_product_prices_update = fields.Boolean(
        'Update product prices',
        help="""Installs the product_prices_update: It allows to update selected products prices at once by applying a calculation rule.""")
    module_product_catalog_aeroo_report = fields.Boolean(
        'Report Product catalog.',
        help="""Installs the product_catalog_aeroo_report module.""")
    module_product_customer_price = fields.Boolean(
        'Allow to define different prices for different Customers.',
        help="""Installs the product_customer_price module.""")
    module_product_website_categ_search = fields.Boolean(
        'Product Search by Website Category.',
        help="""Installs the product_website_categ_search module: It allows to search products by Website Category in Product Tree view""")
    module_product_variant_csv_import = fields.Boolean(
        'Add a menu entry in *Sales > Configuration > Product Categories and attributes > Product Template CSV Import".',
        help="""Installs the product_variant_csv_import module.""")
    module_product_no_translation = fields.Boolean(
        'Set the translatable fields of the product object (name,descriptions) to non-translatable fields.',
        help="""Installs the product_no_translation module.""")
    module_partner_samples = fields.Boolean(
        'Manage Samples Given to Customers.',
        help="""Installs the partner_samples module.""")
    module_product_reference_required = fields.Boolean(
        'Add required in field reference.',
        help="""Installs the product_reference_required: It makes Reference a mandatory field""")
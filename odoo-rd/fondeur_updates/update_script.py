# -*- encoding: utf-8 -*-
###############################################################################
#                                                                             #
# product_brand for Odoo                                                      #
# Copyright (C) 2009 NetAndCo (<http://www.netandco.net>).                    #
# Copyright (C) 2011 Akretion Benoît Guillot <benoit.guillot@akretion.com>    #
# Copyright (C) 2014 prisnet.ch Seraphine Lantible <s.lantible@gmail.com>     #
# Copyright (C) 2015 Leonardo Donelli                                         #
# Contributors                                                                #
# Mathieu Lemercier, mathieu@netandco.net                                     #
# Franck Bret, franck@netandco.net                                            #
# Seraphine Lantible, s.lantible@gmail.com, http://www.prisnet.ch             #
# Leonardo Donelli, donelli@webmonks.it, http://www.wearemonk.com             #
#                                                                             #
# This program is free software: you can redistribute it and/or modify        #
# it under the terms of the GNU Affero General Public License as              #
# published by the Free Software Foundation, either version 3 of the          #
# License, or (at your option) any later version.                             #
#                                                                             #
# This program is distributed in the hope that it will be useful,             #
# but WITHOUT ANY WARRANTY; without even the implied warranty of              #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the                #
# GNU Affero General Public License for more details.                         #
#                                                                             #
# You should have received a copy of the GNU Affero General Public License    #
# along with this program. If not, see <http://www.gnu.org/licenses/>.        #
#                                                                             #
###############################################################################
###############################################################################
# Product Brand is an Openobject module wich enable Brand management for      #
# products                                                                    #
###############################################################################
from openerp.osv import osv, fields
import csv
import pdb


class res_partner(osv.Model):
    _inherit = 'res.partner'
    _columns = {
        'pyme_id': fields.integer('pyme_id'),
    }

    def update_pyme_id(self, cr, uid, ids, context=None):
#        pdb.set_trace()
        reader = csv.reader(open('/opt/odoo/odoo-rd/fondeur_updates/suplidor.csv', 'rb'))

        res_partner_obj = self.pool.get('res.partner')

        for data in reader:
            name = data[3]
            id = data[0]

            res_partner = res_partner_obj.search(cr, uid, [('name', '=', name), ('supplier', '=', True)])
            res_partners = res_partner_obj.browse(cr, uid, res_partner, context=context)

            for item in res_partners:
                if name == item.name:
                    res_partner_obj.write(cr, uid, item.id, {'pyme_id': id})


class product_product(osv.Model):
    _inherit = 'product.product'
    _columns = {
        'pyme_id': fields.text('pyme_id'),
    }

    def update_pyme_id(self, cr, uid, ids, context=None):
        #pdb.set_trace()
        
        csvf = csv.reader(open('/opt/odoo/odoo-rd/fondeur_updates/producto.csv', 'rb'))

        product_product_obj = self.pool.get('product.product')
        product_template_obj = self.pool.get('product.template')

        for data in csvf:
            id = data[0]

            product_product = product_product_obj.search(cr, uid, [('default_code', '=', id)])
            product_products = product_product_obj.browse(cr, uid, product_product, context=context)
        
            for item in product_products:
                if id == item.default_code:
                    product_product_obj.write(cr, uid, item.id, {'pyme_id': id})
                    
                    product_template = product_template_obj.search(cr, uid, [('id', '=', item.product_tmpl_id.id)])

                    product_templates = product_template_obj.browse(cr, uid, product_template, context=context)

                    product_template_obj.write(cr, uid, product_templates.id, {'pyme_id': id})
            

class product_template(osv.Model):
    _inherit = 'product.template'
    _columns = {
        'pyme_id': fields.text('pyme_id'),
    }


    def update_pyme_id(self, cr, uid, ids, context=None):
        
#        pdb.set_trace()

        csvf = csv.reader(open('/opt/odoo/odoo-rd/fondeur_updates/producto.csv', 'rb'))

        product_product_obj = self.pool.get('product.product')
        product_template_obj = self.pool.get('product.template')

        for data in csvf:
            id = data[0]

            product_product = product_product_obj.search(cr, uid, [('default_code', '=', id)])
            product_products = product_product_obj.browse(cr, uid, product_product, context=context)

            for item in product_products:
                if id == item.default_code:
                    product_product_obj.write(cr, uid, item.id, {'pyme_id': id})

                    product_template = product_template_obj.search(cr, uid, [('id', '=', item.product_tmpl_id.id)])

                    product_templates = product_template_obj.browse(cr, uid, product_template, context=context)

                    product_template_obj.write(cr, uid, product_templates.id, {'pyme_id': id})

class product_supplierinfo(osv.Model):

    _name = 'update.product.supplierinfo'

    def update_product_supplierinfo(self, cr, uid, ids, context=None):
        pdb.set_trace()
        csvf = csv.reader(open('/opt/odoo/odoo-rd/fondeur_updates/IvProductosSuplidor.csv', 'rb'))

        res_partner_obj = self.pool.get('res.partner')
        product_template_obj = self.pool.get('product.template')
        product_supplierinfo_obj = self.pool.get('product.supplierinfo')

        counter = 0
        for data in csvf:
            ProductoID = data[0]
            ConfigID = data[1]
            TallaID = data[2]
            ColorID = data[3]
            SuplidorID = data[4]
            CodigoExterno = data[5]
            DescripcionExterna = data[6]

            if CodigoExterno == 'NULL':
                CodigoExterno == False

            product_template = product_template_obj.search(cr, uid, [('pyme_id', '=', ProductoID)])
            product_template_record = product_template_obj.browse(cr, uid, product_template)

            res_partner = res_partner_obj.search(cr, uid, [('pyme_id', '=', SuplidorID),('supplier', '=', True)])
            res_partner_record = res_partner_obj.browse(cr, uid, res_partner)
            
#            if not product_template_record and res_partner_record:
#               print "No hay registro coincidente para un producto ni su suplidor"
            for rec in product_template_record:

                if product_template_record and res_partner_record:

                    vals = {
                        'product_tmpl_id': rec.id,
                        'name': res_partner_record.id,
                        'sequence': 1,
                        'product_name': DescripcionExterna or False,
                        'product_code': CodigoExterno or False,
                        'qty': 0.00,
                        'min_qty': 0.00,
                        'delay': 1,
                        'product_uom': rec.uom_id.id or False,
               
                    }

                    product_supplierinfo_obj.create(cr, uid, vals)
                    counter += 1
                    print "Se ha creado un registro"
                    print counter


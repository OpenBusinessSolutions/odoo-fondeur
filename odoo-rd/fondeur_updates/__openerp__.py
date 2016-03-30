# -*- encoding: utf-8 -*-
###############################################################################
# #                                                                           #
# This program is free software: you can redistribute it and/or modify #      #
# it under the terms of the GNU Affero General Public License as #            #
# published by the Free Software Foundation, either version 3 of the #        #
# License, or (at your option) any later version. #                           #
# #                                                                           #
# This program is distributed in the hope that it will be useful, #           #
# but WITHOUT ANY WARRANTY; without even the implied warranty of #            #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the #              #
# GNU Affero General Public License for more details. #                       #
# #                                                                           #
# You should have received a copy of the GNU Affero General Public License #  #
# along with this program. If not, see <http://www.gnu.org/licenses/>. #      #
# #                                                                           #
###############################################################################
###############################################################################

{
    'name': 'Electrosistemas Fondeur Updates',
    'version': '0.1',
    'category': 'None',
    #'summary': 'Add brand to products',
    #'author': 'NetAndCo, Akretion, Prisnet Telecommunications SA'
    #          ', MONK Software, Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'depends': ['product', 'mrp'],
    'data': [
        'fondeur_updates_view.xml',
        #'security/ir.model.access.csv'
    ],
    'installable': True,
}

# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp.osv import osv, fields
# class workflow_instance(osv.osv):
#     """"""    
#     _inherit = 'workflow.instance'

#     _columns = {
#         ''
#     }
class workflow_instance(osv.osv):
    """"""    
    _inherit = 'workflow.instance'

    _columns = {
        'workitem_ids': fields.one2many('workflow.workitem', 'inst_id', 'Instances')
    }
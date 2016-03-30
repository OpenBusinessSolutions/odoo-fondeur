 #-*- coding: utf-8 -*-
from openerp.osv import fields, osv


class project_issue(osv.osv):
    _inherit = 'project.issue'

    _columns = {
        'project_issue_solution_id': fields.many2one('project.issue.solution', 'Linked Solution'),
        'issue_description': fields.html('Issue Description'),
        'solution_description': fields.html('Solution Description'),
    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

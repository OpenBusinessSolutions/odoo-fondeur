# -*- coding: utf-8 -*-
# (c) 2015 Antiun Ingeniería S.L. - Sergio Teruel
# (c) 2015 Antiun Ingeniería S.L. - Carlos Dauden
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api
from openerp.tools.float_utils import float_round


class ProjectTaskType(models.Model):
    _inherit = 'project.task.type'

    consume_material = fields.Boolean(
        string='Consume Material',
        help="If you mark this check, when a task goes to this state,"
             "it will consume the associated materials")


class Task(models.Model):
    _inherit = "project.task"

    def _compute_stock_move(self):
        self.stock_move_ids = self.mapped('material_ids.stock_move_id')

    def _compute_analytic_line(self):
        self.analytic_line_ids = self.mapped('material_ids.analytic_line_id')

    @api.depends('stock_move_ids.state')
    def _check_stock_state(self):
        if not self.stock_move_ids:
            self.stock_state = 'pending'
        elif self.stock_move_ids.filtered(lambda r: r.state == 'confirmed'):
            self.stock_state = 'confirmed'
        elif self.stock_move_ids.filtered(lambda r: r.state == 'assigned'):
            self.stock_state = 'assigned'
        elif self.stock_move_ids.filtered(lambda r: r.state == 'done'):
            self.stock_state = 'done'

    stock_move_ids = fields.Many2many(
        comodel_name='stock.move', compute='_compute_stock_move',
        string='Stock Moves')
    analytic_line_ids = fields.Many2many(
        comodel_name='account.analytic.line', compute='_compute_analytic_line',
        string='Analytic Lines')
    consume_material = fields.Boolean(related='stage_id.consume_material')
    stock_state = fields.Selection(
        [('pending', 'Pending'),
         ('confirmed', 'Confirmed'),
         ('assigned', 'Assigned'),
         ('done', 'Done')], compute='_check_stock_state', string='Stock State')

    @api.multi
    def unlink_stock_move(self):
        moves = self.mapped('stock_move_ids')
        moves.filtered(lambda r: r.state == 'assigned').do_unreserve()
        moves.filtered(
            lambda r: r.state in ['waiting', 'confirmed', 'assigned']
        ).write({'state': 'draft'})
        moves.unlink()

    @api.multi
    def write(self, vals):
        for task in self:
            res = super(Task, self).write(vals)
            if 'stage_id' in vals:
                if task.stage_id.consume_material:
                    task.material_ids.create_stock_move()
                    task.material_ids.create_analytic_line()
                else:
                    task.unlink_stock_move()
                    task.analytic_line_ids.unlink()
        return res

    @api.multi
    def unlink(self):
        self.unlink_stock_move()
        self.analytic_line_ids.unlink()
        return super(Task, self).unlink()

    @api.multi
    def action_assign(self):
        self.mapped('stock_move_ids').action_assign()

    @api.multi
    def action_done(self):
        self.mapped('stock_move_ids').action_done()


class ProjectTaskMaterials(models.Model):
    _inherit = "project.task.materials"

    stock_move_id = fields.Many2one(
        comodel_name='stock.move', string='Stock Move')
    analytic_line_id = fields.Many2one(
        comodel_name='account.analytic.line', string='Analytic Line')
    product_uom = fields.Many2one(
        comodel_name='product.uom', string='Unit of Measure')

    @api.onchange('product_id')
    def _onchange_product_id(self):
        self.product_uom = self.product_id.uom_id
        return {'domain': {'product_uom': [
            ('category_id', '=', self.product_id.uom_id.category_id.id)]}}

    def uos_qty(self):
        if self.product_uom and self.product_id.uom_id and \
                (self.product_uom != self.product_id.uom_id):
            res = self.quantity * self.product_id.uom_id.factor
            res = res / self.product_uom.factor
            res = float_round(
                res, precision_rounding=self.product_uom.rounding,
                rounding_method='UP')
        else:
            res = self.quantity
        return res

    def _prepare_stock_move(self):
        product = self.product_id
        res = {
            'product_id': product.id,
            'name': product.partner_ref,
            'state': 'confirmed',
            'product_uom': self.product_uom.id or product.uom_id.id,
            'product_uos': self.product_uom.id,
            'product_uom_qty': self.quantity,
            'product_uos_qty': self.quantity,
            'origin': self.task_id.name,
            'location_id': self.env.ref(
                'stock.stock_location_stock').id,
            'location_dest_id': self.env.ref(
                'stock.stock_location_customers').id,
        }
        return res

    @api.multi
    def create_stock_move(self):
        for line in self:
            move_id = self.env['stock.move'].create(
                line._prepare_stock_move())
            line.stock_move_id = move_id.id

    def _prepare_analytic_line(self):
        product = self.product_id
        company_id = self.env['res.company']._company_default_get(
            'account.analytic.line')
        journal = self.env.ref(
            'project_task_materials_stock.analytic_journal_sale_materials')
        analytic_account = getattr(self.task_id, 'analytic_account_id', False)\
            or self.task_id.project_id.analytic_account_id
        res = {
            'name': self.task_id.name + ': ' + product.name,
            'ref': self.task_id.name,
            'product_id': product.id,
            'journal_id': journal.id,
            'unit_amount': self.quantity,
            'account_id': analytic_account.id,
            'user_id': self._uid,
        }
        analytic_line_obj = self.pool.get('account.analytic.line')
        amount_dic = analytic_line_obj.on_change_unit_amount(
            self._cr, self._uid, self._ids, product.id, self.uos_qty(),
            company_id, False, journal.id, self._context)
        res.update(amount_dic['value'])
        res['product_uom_id'] = self.product_uom.id
        to_invoice = getattr(self.task_id.project_id.analytic_account_id,
                             'to_invoice', None)
        if to_invoice is not None:
            res['to_invoice'] = to_invoice.id
        return res

    @api.multi
    def create_analytic_line(self):
        for line in self:
            move_id = self.env['account.analytic.line'].create(
                line._prepare_analytic_line())
            line.analytic_line_id = move_id.id

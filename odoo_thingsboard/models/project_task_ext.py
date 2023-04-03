import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class ProjectTaskExt(models.Model):
    _inherit = 'project.task'

    vehicle_id = fields.Many2one('fleet.vehicle', string='Charging Vehicle')
    tb_user_id = fields.Many2one(
        'res.users', string='Charging User',
        domain=lambda self: [
            ('groups_id', 'in', self.env.ref('base.group_user').id)],
        default=lambda self: self.env.user)
    charging_date = fields.Date(
        'Charging Date', default=fields.Date.today)
    charging_value = fields.Float('Charging Value')
    charging_cost = fields.Float('Charging Cost')
    task_month_id = fields.Many2one('project.task.month', string='任务月份汇总')

    @api.model_create_multi
    def create(self, vals):
        tasks = super().create(vals)
        for res in tasks:
            month = res.charging_date.strftime("%Y-%m") if res.charging_date else fields.Date.today().strftime("%Y-%m")
            tmp_user_id = res.tb_user_id.id if res.tb_user_id else self.env.uid
            month_records = self.env['project.task.month'].search(
                [('task_month', '=', month), ('tb_user_id', '=', tmp_user_id)])
            if month_records:
                res.task_month_id = month_records[0].id
                month_records.write(
                    {'task_ids': [(4, res.id)], 'charging_cost': float(month_records[0].charging_cost)+float(res.charging_cost)})
            else:
                value = {
                    'task_month': month,
                    'task_ids': [(4, res.id)],
                    'tb_user_id': self.env.uid,
                    'charging_cost': float(res.charging_cost) or 0.00
                }
                new_task_month = self.env['project.task.month'].create(value)
                res.task_month_id = new_task_month.id
        return tasks

class ProjectTaskMonthExt(models.Model):
    _name = 'project.task.month'
    _description = '任务月份汇总'
    _order = 'create_date desc'

    _sql_constraints = [
        ('task_month_uniq', 'unique(task_month)', '月份不能重复!')
    ]

    name = fields.Char()
    task_month = fields.Char()
    charging_cost = fields.Float('Charging Cost')
    task_ids = fields.One2many(
        'project.task', 'task_month_id', string='Tasks')
    tb_user_id = fields.Many2one(
        'res.users', string='Charging User',
        domain=lambda self: [
            ('groups_id', 'in', self.env.ref('base.group_user').id)],
        default=lambda self: self.env.user)

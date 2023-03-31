import logging
from odoo import models, fields

_logger = logging.getLogger(__name__)


class ProjectTaskExt(models.Model):
    _inherit = 'project.task'

    vehicle_id = fields.Many2one('fleet.vehicle', string='Charging Vehicle')
    tb_user_id = fields.Many2one(
        'res.users', string='Charging User',
        domain=lambda self: [
            ('groups_id', 'in', self.env.ref('base.group_user').id)],
        default=lambda self: self.env.user)
    charging_date = fields.Date('Charging Date')
    charging_value = fields.Float('Charging Value')
    charging_cost = fields.Float('Charging Cost')

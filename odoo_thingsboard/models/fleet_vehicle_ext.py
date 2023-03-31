import logging
from odoo import models, fields

_logger = logging.getLogger(__name__)


class FleetVehicleExt(models.Model):
    _inherit = 'fleet.vehicle'

    task_id = fields.Many2one('project.task', string='Charging Booking')

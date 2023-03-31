import logging
from odoo import models, fields

_logger = logging.getLogger(__name__)


class ProjectExt(models.Model):
    _inherit = 'project.project'

    tb_device_id = fields.Char('TB Device ID')

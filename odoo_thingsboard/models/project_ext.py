import logging
import pprint
from odoo import models, fields
from tb_rest_client.rest_client_ce import *
from tb_rest_client.rest import ApiException

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(module)s - %(lineno)d - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


class ProjectExt(models.Model):
    _inherit = 'project.project'

    tb_device_id = fields.Char('TB Device ID')

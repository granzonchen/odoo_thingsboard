from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    tb_url = fields.Char(string="ThingsBoard地址", config_parameter='tb.url')
    tb_username = fields.Char(string="ThingsBoard账号",
                              config_parameter='tb.username')
    tb_password = fields.Char(string="ThingsBoard密码",
                              config_parameter='tb.password')

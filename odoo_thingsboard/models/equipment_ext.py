import logging
import pprint
from odoo import models,fields,api
from tb_rest_client.rest_client_ce import *
from tb_rest_client.rest import ApiException

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(module)s - %(lineno)d - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


class EquipmentExt(models.Model):
    _inherit = 'maintenance.equipment'

    tb_device_id = fields.Char('TB Device ID')
    tb_device_token = fields.Char('TB Device Token')

    def get_tb_client(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('tb.url')
        username = self.env['ir.config_parameter'].sudo().get_param('tb.username')
        password = self.env['ir.config_parameter'].sudo().get_param('tb.password')
        tb_client = RestClientCE(base_url)
        tb_client.login(username=username, password=password)
        return tb_client
    
    def create_tb_asset(self,_name=None):
        if not _name:
            pprint.pprint("No name")
            return False
        tb_client = self.get_tb_client()
        asset = Asset(name=_name, type="building")
        asset = tb_client.save_asset(asset)
        pprint.pprint(asset)
        return asset

    def create_tb_device(self, _name=None, device_name=None, device_profile=None):
        if not _name:
            pprint.pprint("No name")
            return False
        tb_client = self.get_tb_client()
        device_name = device_name or "b0157dd0-aae3-11ed-bd94-5159d5145b59"
        device_profile = device_profile or "DEVICE_PROFILE"
        _device_profile_id = DeviceProfileId(device_name, device_profile)
        device = Device(
            name=_name, device_profile_id=_device_profile_id, type="building")
        device = tb_client.save_device(device)
        pprint.pprint(device)
        return device

    def link_device_asset(self, asset_id=None, device_id=None):
        if not asset_id or not device_id:
            pprint.pprint("No name")
            return False
        tb_client = self.get_tb_client()
        relation = EntityRelation(
            _from=asset_id, to=device_id, type="Contains")
        relation = tb_client.save_relation(relation)
    
    def sync_tb_device_infos_to_equipment(self):
        with self.get_tb_client() as tb_client:
            try:
                create_device = self.create_tb_device(self.name)
                create_device_id = create_device.id.id
                create_device_credentials = tb_client.get_device_credentials_by_device_id(create_device_id)
                if (create_device_credentials.credentials_type == 'ACCESS_TOKEN'):
                    create_device_token = create_device_credentials.credentials_id
                self.sudo().write(
                    {'tb_device_id': create_device_id, 'tb_device_token': create_device_token or False})
            except ApiException as e:
                logging.exception(e)

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        for equipment in res:
            equipment.sync_tb_device_infos_to_equipment()
        return res

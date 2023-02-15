import logging
from tb_rest_client.rest_client_ce import *
from tb_rest_client.rest import ApiException
import pprint

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(module)s - %(lineno)d - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

# ThingsBoard REST API URL
url = "http://hy.wffeitas.com:11091"
# Default Tenant Administrator credentials
username = "charger@wffeitas.com"
password = "feitas2023"
device_name = "b0157dd0-aae3-11ed-bd94-5159d5145b59"
device_profile = "DEVICE_PROFILE"

# # Creating the REST client object with context manager to get auto token refresh
# with RestClientCE(base_url=url) as rest_client:
#     try:
#         # Auth with credentials
#         rest_client.login(username=username, password=password)



#         # Creating relations from device to asset
#         relation = EntityRelation(
#             _from=asset.id, to=device.id, type="Contains")
#         relation = rest_client.save_relation(relation)

#         logging.info(" Relation was created:\n%r\n", relation)
#     except ApiException as e:
#         logging.exception(e)


class RestClientODOO:
    
    def create_asset(self,_name=None):
        if not _name:
            pprint.pprint("No name")
            return False
        else:
            _rc = RestClientCE(url)
            _rc.login(username=username, password=password)
            asset = Asset(name=_name, type="building")
            asset = _rc.save_asset(asset)
            pprint.pprint(asset)
            return asset

    def create_device(self, _name=None):
        if not _name:
            pprint.pprint("No name")
            return False
        else:
            _rc = RestClientCE(url)
            _rc.login(username=username, password=password)
            device = Device(name=_name, device_profile_id=DeviceProfileId(
                device_name, device_profile) , type="building")
            device = _rc.save_device(device)
            pprint.pprint(device)
            return device
    
    def link_device_asset(self, asset_id, device_id):
        _rc = RestClientCE(url)
        relation = EntityRelation(
            _from=asset_id, to=device_id, type="Contains")
        relation = _rc.save_relation(relation)

    # def _login(self, username, password):
    #     self.login(username=username, password=password)
f = RestClientODOO()
f.create_device("Feitas Thermometer 2")

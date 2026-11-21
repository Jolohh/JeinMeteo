
from jeinmeteo.configloader import ConfigLoader
from jeinmeteo.api import JeinMeteoAPI

config = ConfigLoader("broker.config").load()

api = JeinMeteoAPI()

devices = api.get_devices_json()

for device in devices:
    api.get_latest(device["name"])

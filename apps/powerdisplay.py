from jeinmeteo.api import JeinMeteoAPI

api = JeinMeteoAPI()

devices = api.get_devices_json()
for device in devices:
    print(device["name"])

#api.get_data("")

import json
import requests


from config.configloader import ConfigLoader
from config.device_registry import Device, Device_registry

config = ConfigLoader("api.config").load()


class JeinMeteoAPI:
    def __init__(self) -> None:
        self.API_URL = config["api_url"]
        
    def get_data(self,device:Device):
        request = requests.get(self.API_URL,params={"name":device.name})
        response = json.loads(request.content)
        return response
    
    
myapi = JeinMeteoAPI()
registry = Device_registry()

devices = registry.get_devices()
print(devices)


data = myapi.get_data(devices[0])
print(data)
    

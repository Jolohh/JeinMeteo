import json
import requests


from jeinmeteo.configloader import ConfigLoader
from jeinmeteo.device_registry import Device, Device_registry

config = ConfigLoader("api.config").load()


class JeinMeteoAPI:
    def __init__(self) -> None:
        self.API_URL = config["api_url"]
        
    def get_data(self,name):
        request = requests.get(f"{self.API_URL}/device",params={"name":name})
        response = json.loads(request.content)
        return response
    
    def get_devices_json(self):
        request = requests.get(f"{self.API_URL}/devices")
        response = json.loads(request.content)
        return response
    
    def build_device_registry(self):
        devices = self.get_devices_json()
        registry = Device_registry()
        for device in devices:
            try:
                registry.add_device(device["hwid"],device["name"],device["device_type"])
            except Exception as e:
                print(e)
                print("Device already registered, skipping...")
        return registry

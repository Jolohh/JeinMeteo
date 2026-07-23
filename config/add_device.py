from config.device_registry import Device_registry
from config.configloader import ConfigLoader

registry = Device_registry()
config = ConfigLoader("broker.config").load()


print("============================================")
hwid = input("Hardware-ID/Identifier eingeben: ")
print("============================================")
name = input("Namen eingeben: ")
print("============================================")
print("Die möglichen Gerätetypen sind:",config["device_types"])
device_type = input("Gerätetypen eingeben: ")


registry.add_device(hwid,name,device_type)
from jeinmeteo.configloader import ConfigLoader
from jeinmeteo.sensordb import SensorDB

config = ConfigLoader("broker.config").load()

db = SensorDB()

print("============================================")
hwid = input("Hardware-ID/Identifier eingeben: ")
print("============================================")
name = input("Namen eingeben: ")
print("============================================")
print("Die möglichen Gerätetypen sind:",db.get_device_types())
device_type = input("Gerätetypen eingeben: ")


db.add_device(name,hwid,device_type)
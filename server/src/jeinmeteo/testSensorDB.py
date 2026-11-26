from jeinmeteo.sensordb import SensorDB

db = SensorDB()

#print(db.get_devices())
#db.add_device(name="Sensor2",hwid="989bib123",device_type="multisensor")

#print(db.get_by_name("Sensor_1"))

#print(db.get_by_hwid("28463F17F7D0A774"))

dummy_multi = {"battery_level":1.4494,"date":"2026/12/30-00:00:00","humidity":47.04,"pm10":None,"pm2.5":None,"pressure":1087.79,"temperature":22.78}
dummy_power = {"date":"2026/12/30-00:00:00","e_in":8916.781,"e_out":0.0,"power":596.0}


#db.insert_values("28463F17F7D0A774",dummy)

#db.insert_values("WattWaechter_6C6287",dummy_power)

print(db.find_device_name("Sensor1"))


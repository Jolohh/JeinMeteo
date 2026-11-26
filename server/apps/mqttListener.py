import sqlite3
import paho.mqtt.client as mqtt
from typing import Dict
import json
from datetime import datetime
from jeinmeteo.configloader import ConfigLoader


from jeinmeteo.sensordb import SensorDB


config = ConfigLoader("broker.config").load()

db = SensorDB()


def on_connect(client, userdata, flags, rc):
    client.subscribe([("sensor/#",1),("Stromzaehler/+/SENSOR",1)])
    print("Connected with result code "+str(rc))



def on_message(client, userdata, msg):
    #print(datetime.now().strftime("%Y/%m/%d-%H:%M:%S"),": ",msg.topic + " " + str(msg.payload))
    hwid = msg.topic.split("/")[1]
    #data_dict = msg.payload
    data_dict = json.loads(msg.payload)
    
    device = db.find_device_hwid(hwid)
    
    print("============================================")
    print("Hardware-Id:",hwid)
    print("Data:",data_dict)
    print("Topic:",msg.topic)
    print("Userdata:",userdata)
    print("device_type:",device.device_type)
    print("============================================")
    
    if device.device_type == "power_meter":
        data_dict = data_dict["E320"]
        del data_dict["Meter_Number"]
        data_dict = {k.lower(): v for k,v in data_dict.items()}

    data_dict["date"] = datetime.now().strftime("%Y/%m/%d-%H:%M:%S")
    db.insert_values(hwid,data_dict)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(config["username"], config["password"])
client.connect(config["ip"], int(config["port"]), 60)
client.loop_forever()
print("Connected to MQTT broker")

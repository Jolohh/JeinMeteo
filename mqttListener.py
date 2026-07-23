import sqlite3
import paho.mqtt.client as mqtt
from typing import Dict
import json
from datetime import datetime
from config.configloader import ConfigLoader
from device_registry import Device_registry


config = ConfigLoader("broker.config").load()
database_name: str = config["database_name"]
device_registry: str = config["device_registry"]


multisensorTypes = ConfigLoader("multisensor.types").load_dict()
stromzaehlerTypes = ConfigLoader("stromzaehler.types").load_dict()

registry = Device_registry()


def insert_to_table(table_name,data_dict,types):
    con = sqlite3.connect(database_name)
    cur = con.cursor()
    
    values_dict = {}
    
    for key in types:
        if key == "date":
            values_dict[key] = datetime.now().strftime("%Y/%m/%d-%H:%M:%S")
        else:
            values_dict[key] = None
    
    #values_dict = {
    #    "humidity": None,
    #    "pressure": None,
    #    "temperature": None,
    #    "pm2.5": None,
    #    "pm10": None,
    #    "date": datetime.now().strftime("%Y/%m/%d-%H:%M:%S"),
    #    "battery_level": None
    #    }
    
    values_dict.update(data_dict)

    values = tuple(values_dict[col] for col in values_dict)
    #print("values:",values)
    columns_string = ", ".join(f'"{name}" {type}' for name, type in types.items())

    cur.execute(f"CREATE TABLE IF NOT EXISTS `{table_name}` ({columns_string})")

    cur.execute(f"""INSERT INTO "{table_name}" VALUES ({
    ','.join(['?'] * len(values_dict))})""", values)

    con.commit()
    
    
def insert_to_stromzaehler(table_name,data_dict,types):
    con = sqlite3.connect(database_name)
    cur = con.cursor()


def on_connect(client, userdata, flags, rc):
    client.subscribe([("sensor/#",1),("Stromzaehler/+/SENSOR",1)])
    print("Connected with result code "+str(rc))



def on_message(client, userdata, msg):
    #print(datetime.now().strftime("%Y/%m/%d-%H:%M:%S"),": ",msg.topic + " " + str(msg.payload))
    hwid = msg.topic.split("/")[1]
    #data_dict = msg.payload
    data_dict = json.loads(msg.payload)
    identifier = registry.check_hwid(hwid)
    
    print("============================================")
    print("Hardware-Id:",hwid)
    print("Data:",data_dict)
    print("Topic:",msg.topic)
    print("Userdata:",userdata)
    print("Identifier:",identifier)
    print("============================================")

    if identifier[3] == "multisensor":
        insert_to_table(hwid,data_dict,multisensorTypes)
    elif identifier[3] == "stromzaehler":
        data_dict = data_dict["E320"]
        del data_dict["Meter_Number"]
        data_dict = {k.lower(): v for k,v in data_dict.items()}
        insert_to_table(hwid,data_dict,stromzaehlerTypes)
        #insert_to_stromzaehler(hwid,data_dict)
    
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(config["username"], config["password"])
client.connect(config["ip"], int(config["port"]), 60)
client.loop_forever()
print("Connected to MQTT broker")

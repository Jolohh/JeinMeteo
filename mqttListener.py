import sqlite3
import paho.mqtt.client as mqtt
from typing import Dict
import json
from datetime import datetime

import configparser

config = configparser.ConfigParser()
config.read("config.ini")



database_name: str = config["broker.config"]["database_name"]


measurementTypes : Dict[str, str] = {
    "humidity": "REAL",
    "pressure": "REAL",
    "temperature": "REAL",
    "pm2.5": "REAL",
    "pm10": "REAL",
    "date": "TEXT",
    "battery_level":"REAL"
    }





#region global variables
#dataLength = len(measurementTypes)
#dataDict = {}

#endregion


def insert_to_table(table_name,data_dict):
    con = sqlite3.connect(database_name)
    cur = con.cursor()
    
    values_dict = {
        "humidity": None,
        "pressure": None,
        "temperature": None,
        "pm2.5": None,
        "pm10": None,
        "date": datetime.now().strftime("%Y/%m/%d-%H:%M:%S"),
        "battery_level": None
        }
    
    values_dict.update(data_dict)

    values = tuple(values_dict[col] for col in values_dict)
    print("values:",values)
    columns_string = ", ".join(f'"{name}" {type}' for name, type in measurementTypes.items())

    cur.execute(f"CREATE TABLE IF NOT EXISTS `{table_name}` ({columns_string})")

    cur.execute(f"""INSERT INTO "{table_name}" VALUES ({
    ','.join(['?'] * len(values_dict))})""", values)

    con.commit()
    


def on_connect(client, userdata, flags, rc):
    client.subscribe("sensor/#")
    print("Connected with result code "+str(rc))
    
  
    
   


def on_message(client, userdata, msg):
    print(datetime.now().strftime("%Y/%m/%d-%H:%M:%S"),": ",msg.topic + " " + str(msg.payload))
    identifier = msg.topic.split("/")[1]
    
    
    data_dict = json.loads(msg.payload)
    
    insert_to_table(identifier,data_dict)
    
    
    
#region Database setup





    


#endregion



#region MQTT setup


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(config["broker.config"]["username"], config["broker.config"]["password"])
print(config["broker.config"]["password"])
client.connect(config["broker.config"]["ip"], config.getint("broker.config","port"), 60)
client.loop_forever()
print("Connected to MQTT broker")


#endregion
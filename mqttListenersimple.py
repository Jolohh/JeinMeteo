import paho.mqtt.client as mqtt
from datetime import datetime
import configparser

config = configparser.ConfigParser()
config.read("config.ini")


def on_connect(client, userdata, flags, rc):
    client.subscribe("#")
    print("Connected with result code "+str(rc))
    
  
    
   


def on_message(client, userdata, msg):
    now = datetime.now().strftime("%Y/%m/%d-%H:%M:%S")
    print(now,msg.topic + " " + str(msg.payload))
    
    
    

    
    

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(config["broker.config"]["username"], config["broker.config"]["password"])
print(config["broker.config"]["password"])
client.connect(config["broker.config"]["ip"], config.getint("broker.config","port"), 60)
client.loop_forever()
print("Connected to MQTT broker")


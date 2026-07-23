import paho.mqtt.client as mqtt
from datetime import datetime
from config.configloader import ConfigLoader

config = ConfigLoader("broker.config").load()



def on_connect(client, userdata, flags, rc):
    client.subscribe("#")
    print("Connected with result code "+str(rc))
    
  
    
   


def on_message(client, userdata, msg):
    now = datetime.now().strftime("%Y/%m/%d-%H:%M:%S")
    print(now,msg.topic + " " + str(msg.payload))
    
    
    

    
    

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(config["username"], config["password"])
client.connect(config["ip"], int(config["port"]), 60)
client.loop_forever()
print("Connected to MQTT broker")

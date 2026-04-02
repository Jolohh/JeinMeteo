import paho.mqtt.client as mqtt
from config import IP, PORT, AUTH

def on_Myconnect(client, userdata, flags, rc):
    print('Connected with result code '+str(rc))
    client.subscribe('teamB/#')

# Message receiving callback
def on_Mymessage(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_Myconnect
client.on_message = on_Mymessage
client.username_pw_set(AUTH["username"],AUTH["password"])
client.connect(IP, PORT, 60)
client.loop_forever()





















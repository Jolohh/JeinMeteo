import paho.mqtt.client as mqtt

def on_Myconnect(client, userdata, flags, rc):
    print('Connected with result code '+str(rc))
    client.subscribe('teamB/#')

# Message receiving callback
def on_Mymessage(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_Myconnect
client.on_message = on_Mymessage
client.username_pw_set("user1","bouter20XX")
client.connect("147.210.103.14", 1883, 60)
client.loop_forever()





















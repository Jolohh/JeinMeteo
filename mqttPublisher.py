import paho.mqtt.publish as publish
from sense_hat import SenseHat
import time
from datetime import datetime
#Custom Lib: https://github.com/ikalchev/py-sds011.git
from sds011 import SDS011

#Configuration
IP = "147.210.103.14"
PORT = 1883
AUTH = {
    "username":"user1",
    "password":"bouter20XX"
}
QOS = 1

#Measurement Function
def getMeasurement():
    try:
        particleSensor = SDS011("/dev/ttyUSB0", use_query_mode=True)
        particleData = particleSensor.query()
    except Exception as e:
        print("Sensor error:",e)
        particleData = (0,0)

    sense = SenseHat()
    date = datetime.now().strftime("%Y/%m/%d-%H:%M:%S")
    data = [("teamB/temperature", sense.get_temperature(), QOS),
            ("teamB/humidity", sense.get_humidity(), QOS),
            ("teamB/pressure", sense.get_pressure(), QOS),
	    ("teamB/pm2.5", particleData[0], QOS),
	    ("teamB/pm10", particleData[1], QOS),
	    ("teamB/date", date, QOS)
    ]
    print(data)
    return data

#Main loop
while True:
    publish.multiple(msgs=getMeasurement(),
		     hostname=IP,
 		     port=PORT,
		     auth=AUTH)
    time.sleep(5)






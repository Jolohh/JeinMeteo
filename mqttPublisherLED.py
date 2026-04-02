import paho.mqtt.publish as publish
from sense_hat import SenseHat
import time
from datetime import datetime
#Custom Lib: https://github.com/ikalchev/py-sds011.git
from sds011 import SDS011
from config import IP, PORT, AUTH, QOS

MINIMUM = {
    "temperature": 0,
    "humidity": 30,
    "pressure": 0,
    "pm2.5": 0,
    "pm10": 0,
    }

MAXIMUM = {
    "temperature": 40,
    "humidity": 60,
    "pressure": 2000,
    "pm2.5": 25,
    "pm10": 40,
    }

sensorLookup = ["temperature","humidity","pressure","pm2.5","pm10"]


#Create LED List from
def valToLED(val,type):
    rgb = [0,255,0]
    percentage = val/MAXIMUM[type]
    print("Percentage from max:",percentage,"for:",type)

    #if more than 100%, set LED red
    if percentage > 1:
        rgb = [255,0,0]
        percentage = 1
    elif val < MINIMUM[type]:
        rgb = [0,0,255]
        percentage = 1

    #create led list
    percentage = round(percentage * 8)

    ledList = []

    for r in range(percentage):
        ledList.append(rgb)

    #extend the list to 8 elements
    dlen = 8 - len(ledList)
    ledList.extend([[0,0,0]]*dlen)

    return ledList


#Measurement Function
def getMeasurement():
    try:
        particleSensor = SDS011("/dev/ttyUSB0", use_query_mode=True)
        particleData = particleSensor.query()
    except Exception as e:
        print("Sensor error:",e)
        particleData = (0,0)

    sense = SenseHat()
    sensorList = [sense.get_temperature(),sense.get_humidity(),sense.get_pressure(),particleData[0],particleData[1]]

    #create RGB-value list for led matrix
    ledMatrix = []

    for i, e in enumerate(sensorList):
        ledMatrix.extend(valToLED(e,sensorLookup[i]))

    #extend the led list to 64
    dlen = 64 - len(ledMatrix)
    ledMatrix.extend([[0,0,0]] * dlen)

    sense.set_pixels(ledMatrix)

    date = datetime.now().strftime("%Y/%m/%d-%H:%M:%S")
    data = [("teamB/temperature", sensorList[0], QOS),
            ("teamB/humidity", sensorList[1], QOS),
            ("teamB/pressure", sensorList[2], QOS),
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






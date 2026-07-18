import sqlite3
import matplotlib.pyplot as plt
from matplotlibtools import set_xstep, set_ystep, set_xunit, set_yunit
import numpy as np
import requests
import json
from datetime import datetime,timedelta


import matplotlibtools

dev_ids = ["211097D05BECC882","28463F17F7D0A774"]

API_URL = "http://sensornet.fritz.box/api/weather/device?dev_id="



content = {}

for dev_id in dev_ids:
    request = requests.get(API_URL+dev_id)
    response = json.loads(request.content)
    content[dev_id] = response

# region pure matplotlib functions

x0 = []
y0 = []
x1 = []
y1 = []

xd = []
yd = []

dev0= content[dev_ids[0]]
dev1= content[dev_ids[1]]

for row in dev0:
    x0.append(datetime.strptime(row["date"],"%Y/%m/%d-%H:%M:%S"))
    y0.append(row["temperature"])
    
for row in dev1:
    x1.append(datetime.strptime(row["date"],"%Y/%m/%d-%H:%M:%S"))
    y1.append(row["temperature"])



fig, ax = plt.subplots()

plt.plot(x0[:100],y0[:100])
plt.plot(x1[:100],y1[:100])

plt.show()

